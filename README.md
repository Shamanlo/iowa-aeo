# Iowa AEO website

Static site for **Iowa AEO** (iowaaeo.com), an Answer Engine Optimization agency serving Des Moines,
Cedar Rapids, Iowa City and the Quad Cities.

## Layout

| Path | What it is |
|---|---|
| `build.py` | Generator. Site settings (phone, booking link, video, Web3Forms key) are at the top. |
| `src/content.py` | All copy: locations and towns, industries, simulator questions, FAQs |
| `src/icons.py` | Inline SVG icons, the corn logo mark and the AI assistant marks |
| `static/` | CSS, JS and images, copied to `docs/assets/` |
| `tools/render-images.cjs` | Re-renders `og.png` and `apple-touch-icon.png` |
| `docs/` | **Generated site.** Don't edit by hand. |

## Build

```sh
python3 build.py                 # regenerates docs/
npx http-server docs -p 8080     # preview at http://localhost:8080
```

No dependencies beyond Python 3. Commit `docs/` after building.

## Hosting (Cloudflare Pages)

`.github/workflows/deploy.yml` deploys every push to `main` to Cloudflare Pages (project `iowa-aeo`).
It creates the project, uploads `docs/`, attaches `iowaaeo.com` and `www.iowaaeo.com`, and points their
DNS at Pages, removing the Namecheap parking records.

One-time setup: add a repository secret under **Settings → Secrets and variables → Actions**:

- `CLOUDFLARE_API_TOKEN`: a custom token with *Account · Cloudflare Pages · Edit*, *Zone · DNS · Edit* and
  *Zone · Zone · Read* (zone: iowaaeo.com)
- `CLOUDFLARE_ACCOUNT_ID` (optional): read from the iowaaeo.com zone when not set

Then re-run the workflow from the **Actions** tab, or push any change.

## Common edits

- **Phone number:** set `PHONE` in `build.py`. The header button switches to a phone pill.
- **Booking link:** set `BOOKING_URL`. "Book a Call" points to the contact form until it's set.
- **Hero video:** put the file in `static/video/` and set `HERO_VIDEO = "/assets/video/hero.mp4"`
  (a YouTube embed URL also works). A play button appears on the hero frame.
- **Media Room videos:** add entries to `MEDIA_VIDEOS`.
- **Forms:** use Web3Forms. Submissions go to the email address registered to the access key.
