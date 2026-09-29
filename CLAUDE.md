# nueva-living

Static site for nuevaliving.com: a Costa del Sol new-build advisory. 53 projects,
10 locales, ~890 built pages. Everything is generated from JSON by Node scripts.

This file is the rules that are load-bearing and **not** discoverable by reading the
code. Everything else, read the code — it is commented unusually well, and the commit
messages carry the reasoning.

## The build

Run the whole chain, in this order, or not at all:

```
node scripts/stage_pages.mjs && node scripts/build_footer_pages.mjs && \
node scripts/build_property_pages.mjs && node scripts/build_segment_pages.mjs && \
node scripts/build_homepage_locales.mjs && node scripts/build_developments_locales.mjs && \
node scripts/build_static_page_locales.mjs && node scripts/verify_build_idempotent.mjs && \
node scripts/build_dist.mjs && node scripts/audit_site_consistency.mjs
```

`stage_pages.mjs` restores the five hand-authored pages from `pages/` to the repo root,
and the later builders inject content into them. **A partial run reports failures that
are not real.** If the audit complains about `developments.html`, check you ran the
whole chain before believing it.

It takes about four minutes — longer than the 120 s Bash timeout. Run it in the
background and poll, don't chain `sleep`.

Netlify runs this same command on deploy (`netlify.toml`), so a red audit is a broken
deploy, not a warning.

## What you may edit

| Path | |
| --- | --- |
| `pages/` | The five hand-authored pages. **Edit here.** |
| `/404.html`, `/compare.html`, `/developments.html`, `/nueva-living-home.html`, `/thank-you.html` | Build output of the above, gitignored. Never edit. |
| `dist/` | Generated, gitignored. Never edit. |
| `sv/index.html`, `property-*.html`, the other locale pages at root | Tracked, but generated. Edit the JSON, rebuild. |

## Projects

`content/liora-projects/<slug>/project.json` is the record; images live at
`assets/liora/projects/<slug>/`. English is the source of truth; `i18n` holds nine
overlays (`es fr de ru ar nl pl sv no`).

**`mergeOverlay` merges equal-length arrays positionally.** Changing the length of any
array — `residences.items`, `quickFacts`, `media.items` — requires the same change in
all nine overlays, in the same commit, or the build breaks. This is the rule that is
impossible to infer and expensive to discover.

Facts come from the developer's own documents. Where two sources disagree, publish
neither quietly: name both figures and say which document each came from. A project can
be perfectly self-consistent and entirely wrong — see the Solenne correction of
28 September 2026, which passed every guard in ten languages for months while stating
the wrong town, an invented unit mix and a delivery date two years early.

## Anonymisation

The public project name is invented. `crm.realName` and `crm.realDeveloper` hold the
truth and **must never appear in public copy** — not in prose, alt text, captions,
filenames or schema. A guard checks 520 project pages for the developer's own name.
`netlify/functions/data/projects-catalog.json` is a separate public projection with no
`crm` block; keep it that way.

## Images

Source ≤2000px, quality 82, progressive; `scripts/generate_image_derivatives.py`
makes the webp/avif.

**Every image is reviewed before it ships**, and the audit enforces it. The
anonymisation guard reads text and cannot read pixels: two renders delivered
for `playa-del-angel-residences` carried the developer's name *inside* the
image, engraved on the entrance gate and set in letters on the spa wall, with
every text check green. Look for the developer's own name or logo rendered in
the scene — a gate, a wall, a hoarding, a pool floor, a screen — then record it:

```
node scripts/review_project_images.mjs --project=<slug>            # what is pending
node scripts/review_project_images.mjs --project=<slug> --confirm  # after looking
```

Images are keyed by the hash of their bytes, so replacing or re-cropping a file
drops it out of the manifest and it has to be looked at again.

## Locale conventions — derive them, never guess

Take the format from the value already in that locale and substitute into it. Guessing
costs a four-minute build cycle every time.

- **Quarter:** `T4` (es, fr) · `Q4` (de) · `K4` (nl, sv, no) · `4 кв.` (ru) ·
  `IV kw.` (pl) · `الربع الرابع` (ar)
- **Area unit:** `м²` (ru) · `م²` (ar) · `m²` (rest)
- **Decimal mark:** `.` (ar) · `,` (rest)
- **Prices:** every locale has its own separator and currency placement
- A new `discovery` tag needs an entry in `content/i18n/tags.json` with all nine
- A property type another project already translates must be worded the same way here

## CSS

`assets/liora/nueva-system.css` is **inlined** into every page by `build_dist.mjs`
(`<style data-nueva-system>`), not linked. It is loaded everywhere, homepage included.
`nueva-nav-interactions.css`, `nueva-newsletter.css` and `nueva-shortlist.css` are
linked by every page type.

The homepage carries its own inline `<style>` *after* the inlined system CSS, so its
rules win ties on source order. Beat them with specificity, not `!important`. The
homepage also fixes heights the rest of the site does not — `.dev-img-wrap` and
`#developments .dev-card` — which is where card layouts break first.

## Guards

`scripts/audit_site_consistency.mjs` holds 143 checks; `verify_build_idempotent.mjs`
re-runs the builders and fails on any difference; `build_dist.mjs` runs `verify_cards`.

They catch **disagreement**, not falsehood. A failure is almost always one value in two
places with one of them updated. Fix the data, not the guard.

Adding a guard while it is green is the house habit — it goes in with no cleanup behind
it and only ever fires on drift.

## Handoff bundles

A bundle that ships repo files ships a snapshot of `main`. Never copy its files
wholesale: take its new block, and re-apply anything local it predates. Two bundles this
month would have silently reverted live work.

## Import tooling

`tools/import/` builds a project's nine locale overlays: `tm.py` harvests the
translations already in the repo, `scaffold.py` lists what a new project still needs,
`k_*.py` hold the human translations, `assemble.py` writes the overlays and refuses to
write a partial one. See `tools/import/README.md`.
