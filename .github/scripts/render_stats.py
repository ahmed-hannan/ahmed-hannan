#!/usr/bin/env python3
"""Render the profile activity card (dark + light) from the GitHub GraphQL API.

Run by .github/workflows/stats.yml. Uses STATS_TOKEN when it is set so that
contributions in private repositories are counted; falls back to the workflow
token, which can only see public activity. To restyle, edit PALETTES below —
the colors mirror assets/header.svg.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
    pullRequests { totalCount }
    openIssues: issues(states: OPEN) { totalCount }
    closedIssues: issues(states: CLOSED) { totalCount }
    repositoriesContributedTo(
      contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]
    ) { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100) {
      totalCount
      nodes { stargazerCount }
    }
    privateRepos: repositories(ownerAffiliations: OWNER, privacy: PRIVATE) {
      totalCount
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
    }
  }
}
"""

PALETTES = {
    "assets/stats.svg": {
        "bg": "#0a0a0a", "grid": "#ffffff", "grid_opacity": "0.028",
        "accent": "#c5d642", "value": "#f5f5f5", "label": "#8b8b8b",
        "muted": "#5f5f5f", "glow": "0.16",
    },
    "assets/stats-light.svg": {
        "bg": "#f7f8f4", "grid": "#0a0a0a", "grid_opacity": "0.04",
        "accent": "#586b0d", "value": "#0a0a0a", "label": "#5b5f57",
        "muted": "#7b7f77", "glow": "0.10",
    },
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def fetch(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        API, data=body,
        headers={"Authorization": f"bearer {token}",
                 "Content-Type": "application/json",
                 "User-Agent": "profile-stats-card"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        sys.exit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def assert_token_sees_private(user):
    """Fail if STATS_TOKEN cannot see private repositories.

    A fine-grained PAT, or a classic one missing the `repo` scope, still
    reports the aggregate restricted contribution count — that figure is
    public once private contributions are enabled on the profile — but it
    returns 0 private repos and silently omits private PRs and issues.
    Publishing that understates activity, which is the thing this card exists
    to avoid, so refuse rather than render it.
    """
    restricted = user["contributionsCollection"]["restrictedContributionsCount"]
    private_repos = user["privateRepos"]["totalCount"]
    if restricted > 0 and private_repos == 0:
        sys.exit(
            f"STATS_TOKEN cannot see private repositories: {restricted:,} private "
            "contributions are reported, but 0 private repos are visible, so "
            "private PRs and issues would be missing from the card. Use a "
            "CLASSIC personal access token with the 'repo' scope — fine-grained "
            "tokens do not expose private PRs and issues on the user object."
        )


def collect(user):
    """Pick the five most meaningful non-empty stats.

    A stat showing 0 reads worse than one left out, so empty ones are dropped
    and the next candidate takes the slot. MAX_CELLS is what the card's row
    fits at the current spacing.
    """
    MAX_CELLS = 5
    contrib = user["contributionsCollection"]
    # Private contributions arrive as a single restricted count rather than
    # itemized, so add it back in to reflect real volume.
    commits = contrib["totalCommitContributions"] + contrib["restrictedContributionsCount"]
    issues = user["openIssues"]["totalCount"] + user["closedIssues"]["totalCount"]
    stars = sum(r["stargazerCount"] for r in user["repositories"]["nodes"])

    candidates = [
        (commits, "Commits"),
        (user["pullRequests"]["totalCount"], "Pull Requests"),
        (issues, "Issues"),
        (stars, "Stars Earned"),
        (user["repositoriesContributedTo"]["totalCount"], "Contributed To"),
        (user["repositories"]["totalCount"], "Repositories"),
    ]
    kept = [c for c in candidates if c[0] > 0][:MAX_CELLS]
    return kept or candidates[:MAX_CELLS]


def render(stats, palette, updated):
    cells = []
    for i, (value, label) in enumerate(stats):
        x = 156 + i * 200
        cells.append(
            f'  <text x="{x}" y="158" font-family="{SANS}" font-size="46" '
            f'font-weight="700" letter-spacing="-1" fill="{palette["value"]}">{value:,}</text>\n'
            f'  <text x="{x}" y="186" font-family="{MONO}" font-size="12" '
            f'letter-spacing="2.2" fill="{palette["label"]}">{label.upper()}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="240" viewBox="0 0 1200 240" fill="none" role="img" aria-label="GitHub activity for the last 12 months">
  <defs>
    <radialGradient id="glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse"
      gradientTransform="translate(150 120) rotate(0) scale(560 300)">
      <stop offset="0" stop-color="{palette['accent']}" stop-opacity="{palette['glow']}"/>
      <stop offset="0.55" stop-color="{palette['accent']}" stop-opacity="0.04"/>
      <stop offset="1" stop-color="{palette['accent']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
      <path d="M34 0H0V34" fill="none" stroke="{palette['grid']}" stroke-width="1" stroke-opacity="{palette['grid_opacity']}"/>
    </pattern>
  </defs>

  <rect width="1200" height="240" fill="{palette['bg']}"/>
  <rect width="1200" height="240" fill="url(#grid)"/>
  <rect width="1200" height="240" fill="url(#glow)"/>

  <rect x="128" y="52" width="4" height="36" rx="2" fill="{palette['accent']}"/>
  <text x="156" y="78" font-family="{MONO}" font-size="14" letter-spacing="3.5"
    fill="{palette['accent']}">ACTIVITY · LAST 12 MONTHS</text>
  <text x="1072" y="78" text-anchor="end" font-family="{MONO}" font-size="12"
    fill="{palette['muted']}">updated {updated}</text>

{chr(10).join(cells)}
</svg>
'''


def main():
    token = os.environ.get("STATS_TOKEN")
    login = os.environ.get("STATS_LOGIN") or os.environ["GITHUB_REPOSITORY_OWNER"]
    if not token:
        # Deliberately fatal: the workflow token can only see public activity,
        # so falling back to it would quietly publish understated numbers.
        sys.exit("STATS_TOKEN is not set. Add a classic PAT with the 'repo' "
                 "scope as a repository secret — see SETUP.md section 4.")

    user = fetch(login, token)
    assert_token_sees_private(user)
    stats = collect(user)
    print("rendered stats:", ", ".join(f"{label}={value:,}" for value, label in stats))
    if all(value == 0 for value, _ in stats):
        print("::warning::Every count is zero — STATS_TOKEN probably lacks the 'repo' scope.")

    # Month granularity keeps the card from changing (and committing) daily.
    updated = datetime.now(timezone.utc).strftime("%b %Y")
    for path, palette in PALETTES.items():
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(render(stats, palette, updated))
        print("wrote", path)


if __name__ == "__main__":
    main()
