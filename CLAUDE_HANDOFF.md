# Liora Living Handoff

This is a static HTML/CSS/JS website for Liora Living.

## Main Entry Point

- `Liora_Living_COLOR_SKETCH_HOME.html` is the current homepage and should be treated as the active version.
- Open it directly in a browser with a `file://` URL, or host the folder as static files.

## Secondary Pages

- `liora-about.html`
- `liora-approach.html`
- `liora-developments.html`
- `liora-areas.html`
- `liora-advisory.html`
- `liora-access.html`
- `liora-legal-notice.html`
- `liora-privacy-policy.html`
- `liora-cookie-policy.html`

These pages share styling from `assets/liora/liora-pages.css`.

## Important Assets

- Brand logos: `assets/liora/brand/`
- Area imagery: `assets/liora/areas/`
- Private viewing sequence imagery: `assets/liora/viewing/`
- Favicons and legacy logo exports: `assets/liora/`

## Current Brand / Contact

- Contact email: `contact@liora-living.com`
- Current homepage nav/footer logo assets use the modern Liora Living wordmark in `assets/liora/brand/`.

## Notes For The Next Developer

- The site is currently built as static files, not a framework app.
- Most homepage CSS and JS is embedded directly inside `Liora_Living_COLOR_SKETCH_HOME.html`.
- Footer/secondary pages can be regenerated from `scripts/build_footer_pages.mjs`.
- Private viewing-related helper scripts live in `scripts/`.
- `artifacts/liora/` contains verification screenshots/reports and can be useful context, but is not required for production hosting.

## Suggested Production Cleanup

- Decide whether to keep or remove `artifacts/liora/` before final deployment.
- Consider moving inline homepage CSS/JS into separate files before long-term maintenance.
- Configure the purchased domain through a static host such as Netlify, Vercel, Cloudflare Pages, or traditional web hosting.
