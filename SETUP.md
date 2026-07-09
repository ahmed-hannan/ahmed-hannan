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

## 4. The stats card (if it shows broken)

The activity card is served by the **free, shared** `github-readme-stats.vercel.app`
instance. That host is frequently rate-limited and returns `503` for everyone
(including the project's own demo) during busy periods — when that happens the
card shows as a broken image for a while, then recovers on its own. Nothing in
this repo is misconfigured; the URL and color params are correct.

If you want it reliably up, deploy your **own** instance (~5 min, free):

1. Fork <https://github.com/anuraghazra/github-readme-stats>.
2. Create a GitHub **Personal Access Token** (classic, no scopes needed for
   public stats) and deploy the fork to Vercel, setting `PAT_1` to that token.
3. In `README.md`, swap the host in the stats URL from
   `github-readme-stats.vercel.app` to your `your-app.vercel.app` — keep every
   query param as-is.

Self-hosting also removes the rate limits and lets `count_private=true` actually
count your private contributions.

---

## 5. Changing the accent

The accent is lime **`#c5d642`** (on near-black `#0a0a0a`). It appears in four
places — swap it in each to restyle the whole profile:

| File | What to change |
|------|----------------|
| `assets/header.svg` | Every `#c5d642` (accent bar, glow gradient stops, eyebrow). Background is `#0a0a0a`. |
| `assets/header-light.svg` | The light-mode counterparts: bar `#a6bd1c`, eyebrow `#586b0d`, glow stops `#c5d642`. |
| `README.md` | The stats-card URL params: `title_color`, `icon_color` = `c5d642`, `bg_color` = `0a0a0a`, `text_color` = `f5f5f5` (no `#` in URLs). |
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
