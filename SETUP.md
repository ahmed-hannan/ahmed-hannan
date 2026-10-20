# Setup

This is your GitHub **profile README** — the repo has the same name as your
username, so GitHub renders `README.md` at the top of your profile.

```
ahmed-hannan/
├─ README.md
├─ assets/
│  ├─ header.svg          # dark-mode banner
│  └─ header-light.svg    # light-mode banner
├─ .github/workflows/
│  └─ snake.yml           # contribution-snake generator
└─ SETUP.md
```

---

## 1. Create the repo

The repo name must **exactly** match your username: `ahmed-hannan`.

```bash
cd ahmed-hannan            # this folder
git init -b main
git add .
git commit -m "profile readme"

# Create it on GitHub and push (GitHub CLI):
gh repo create ahmed-hannan --public --source=. --remote=origin --push

# …or manually: create an empty public repo named `ahmed-hannan` on GitHub, then:
# git remote add origin git@github.com:ahmed-hannan/ahmed-hannan.git
# git push -u origin main
```

GitHub shows a "special repository" hint when the name matches your username —
that confirms it will render on your profile.

---

## 2. Kick off the snake (one manual run required)

The snake images are served from an `output` branch that **doesn't exist until
the workflow runs once**. Until then those two images in the README will show as
broken — that's expected.

1. Go to the repo's **Actions** tab.
2. If prompted, click **"I understand my workflows, enable them"**.
3. Select **Generate Snake** → **Run workflow** → run it on `main`.
4. Wait ~1 minute. The run creates the `output` branch with `snake-dark.svg` and
   `snake-light.svg`. The README images resolve on the next hard-refresh.

After this, it regenerates automatically every day (03:00 UTC) and on every push
to `main`. No token setup is needed — it uses the built-in `GITHUB_TOKEN`, and
the workflow already grants `contents: write`.

**If the run fails on push:** open **Settings → Actions → General → Workflow
permissions** and select **Read and write permissions**.

---

## 3. Footer links

Open `README.md` and edit the `<sub>` block at the bottom — replace the
placeholders with your real details:

```html
<a href="mailto:you@example.com">Email</a> ·
<a href="https://www.linkedin.com/in/your-handle">LinkedIn</a> ·
<a href="https://your-site.dev">Website</a>
```

Remove any line you don't want.

---

## 4. The activity card

The card under **Activity** is generated in this repo rather than fetched from a
third-party host. `.github/workflows/stats.yml` runs `.github/scripts/render_stats.py`
daily, which queries the GitHub GraphQL API and writes `assets/stats.svg` and
`assets/stats-light.svg`. It commits only when a number actually changes.

It needs a token, and this is the important part: contributions made in **private**
repositories are invisible to any token but your own. A shared host (such as the
`github-readme-stats.vercel.app` instance this card used to use) queries as
*itself*, so it reports `0` pull requests and `0` issues no matter what your
profile settings say.

**Setup — one time:**

1. Create a classic **Personal Access Token** with the **`repo`** scope at
   <https://github.com/settings/tokens>.
2. Add it to this repo as a secret named **`STATS_TOKEN`**
   (Settings → Secrets and variables → Actions → New repository secret).
3. Run **Generate Stats** once by hand from the Actions tab.

Without `STATS_TOKEN` the workflow fails on purpose — falling back to the
built-in workflow token would quietly publish public-only numbers, which is the
problem the card exists to solve.

**Changing which stats appear:** edit the `candidates` list in
`render_stats.py`. Stats that come back as `0` are dropped automatically and the
next candidate takes the slot, so the row never shows an empty figure. Five
cells fit at the current spacing.

---

## 5. Changing the accent

The accent is lime **`#c5d642`** (on near-black `#0a0a0a`). It appears in four
places — swap it in each to restyle the whole profile:

| File | What to change |
|------|----------------|
| `assets/header.svg` | Every `#c5d642` (accent bar, glow gradient stops, eyebrow). Background is `#0a0a0a`. |
| `assets/header-light.svg` | The light-mode counterparts: bar `#a6bd1c`, eyebrow `#586b0d`, glow stops `#c5d642`. |
| `.github/scripts/render_stats.py` | The `PALETTES` dict — `accent`, `bg`, `value`, `label` for both the dark and light cards. Re-run the workflow to apply. |
| `.github/workflows/snake.yml` | `color_snake` / `color_dots` (URL-encoded — `%23` = `#`). Re-run the workflow to apply. |

Tip: pick your new hex, then find-and-replace `c5d642` (and the deeper light
shade `a6bd1c`) across those files. After editing `snake.yml`, trigger the
workflow again so the snake picks up the new colors.

---

## Preview locally

The banners are plain SVG — open `assets/header.svg` in a browser, or rasterize:

```bash
rsvg-convert -w 1000 assets/header.svg -o /tmp/header.png && open /tmp/header.png
```
