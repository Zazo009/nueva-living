# -*- coding: utf-8 -*-
"""The shape an overlay is allowed to have.

Both scaffold.py and assemble.py walk the English project against a "shape"
and skip any key the shape does not have. That gate is what decides which
strings get translated at all.

The shape used to be one sibling's Spanish overlay --
buenas-noches-terrace-residences -- with three hand-patches bolted on for the
keys that sibling happened to lack: media.video from laurel-hill, media.tour
and constructionTimeline.paymentTerms from los-olivos. Twelve identical lines
in each of the two scripts.

That is fine until a project has a section the sibling does not. Then the
section is invisible to both scripts: scaffold never lists it, so nobody
writes a translation, and assemble never walks it, so the English value is
copied into all nine overlays. Nothing fails. The page builds, the overlay is
the right shape, and nine locales quietly serve English.

altos-terrace-residences hit it with five sections at once -- investment,
trustDossier, lifestyle.panels, projectFile and timeline -- 36 strings that
would have shipped in English in nine languages had the translation guard in
build_property_pages not caught them downstream.

So the shape is now the union of every published project's Spanish overlay.
Any section any project has ever translated is covered, and a new project can
only fall through this gate if no project before it had that section either.
The three patches are gone: the union already contains them.
"""
import glob, json, os

def _merge(into, node):
    """Union of two overlay shapes. Lists collapse to one prototype element,
    because the walkers only ever read model[0]."""
    if isinstance(node, dict) and isinstance(into, dict):
        for k, v in node.items():
            into[k] = _merge(into.get(k), v) if k in into else _copy(v)
        return into
    if isinstance(node, list) and isinstance(into, list):
        if node:
            proto = _copy(node[0])
            into[0] = _merge(into[0], proto) if into else proto
            if not into: into.append(proto)
        return into
    # A scalar, or two shapes that disagree on type: either is a fine stand-in,
    # since the walkers only test presence and container kind.
    return into if into is not None else _copy(node)

def _copy(v):
    return json.loads(json.dumps(v))

def overlay_shape(root='content/liora-projects', locale='es'):
    shape = {}
    files = sorted(glob.glob(os.path.join(root, '*', 'project.json')))
    if not files:
        raise SystemExit(f'overlay_shape: no projects under {root}')
    for f in files:
        ov = json.load(open(f, encoding='utf-8')).get('i18n', {}).get(locale)
        if ov: _merge(shape, ov)
    return shape

if __name__ == '__main__':
    s = overlay_shape()
    print(f'{len(s)} top-level keys')
    for k in sorted(s):
        v = s[k]
        print(f'  {k}: {sorted(v) if isinstance(v, dict) else type(v).__name__}')
