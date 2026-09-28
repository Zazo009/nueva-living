# Import tooling

How a project's nine locale overlays get built. These scripts wrote the overlays for
the projects published in September 2026; they lived untracked in `~/Downloads` until
28 September 2026, which is why the Helvet Green price-list logic was nearly lost.

Run from the repo root, not from here.

## The flow

```
tm.py  →  scaffold.py  →  k_*.py  →  assemble.py
```

**`tm.py <out.json>`** — builds the translation memory. Walks every
`content/liora-projects/*/project.json`, pairs each English string with what the nine
overlays already say, and keeps the most common translation per locale. About 7 MB of
output, regenerable in seconds, so it is gitignored rather than committed.

Media gallery `category` values are skipped on purpose: they stay English.

**`scaffold.py <workdir> <slug>`** — lists what the new project still needs. Walks its
English against the overlay *shape* of a sibling project
(`buenas-noches-terrace-residences`, plus `laurel-hill-residences` for video,
`los-olivos-residences` for tours and payment terms), skips the keys that never
translate (`src`, `width`, `height`, `category`, `floorplan`, `href`, …), and subtracts
anything the translation memory already knows.

**`k_a.py` … `k_e.py` `<out.json>`** — the human translations, one `a()` call per
string with all nine locales positionally: `a(en, es, fr, de, ru, ar, nl, pl, no, sv)`.
Each writes a `tr_<letter>.json`. These are the irreplaceable part of this directory —
everything else can be regenerated.

**`assemble.py <workdir> <slug>`** — builds the overlays from the translation memory
plus every `tr_[a-z].json` in the workdir, and writes them into the project.

It refuses to write if anything is untranslated, printing `UNTRANSLATED <n>` and the
first twenty strings. That refusal is the point: a partial overlay is how a locale page
ends up with English in the middle of it.

## Why `assemble.py` mirrors a sibling's shape

`mergeOverlay` merges equal-length arrays positionally, so an overlay has to have the
same shape as the English it covers — same keys, same array lengths, in the same order.
Building from a sibling that already satisfies the guards is cheaper than deriving the
shape from the schema.

The corollary, which is in `CLAUDE.md` too: changing the length of any array in a
project means changing it in all nine overlays in the same commit.

## The per-project JSON here

`cs_*`, `ev_*`, `hg_*` and the `tr_*` files are the working data for projects already
published — Helvet Green is `hg_*`. Kept as worked examples of what a complete
translation pass looks like, not as inputs to anything.

`floor_parts.json` is the floor-label vocabulary the audit checks overlay floor labels
against.
