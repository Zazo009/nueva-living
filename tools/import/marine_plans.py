"""Cuts the developer's Marine Hills plan sheets into the plain drawings published.

    python3 tools/import/marine_plans.py <dir of CODE_sheetid.jpg> <planos_map.txt> <out dir>

planos_map.txt is one line per type code: `CODE=sheet:kind,sheet:kind,...` where kind is
A (apartment), T (penthouse or duplex, floor plan and solarium on one sheet) or V (semi-detached
villa), followed by the sheet's own title. Sheets with no title are the developer's paid
terrace-customisation variants of the same plan and are not published. Output names are
`<code>.jpg` (one drawing) or `<code>-ground.jpg` and `<code>-upper.jpg` (villas).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tm_plans import cut, FRAME_MH, TABLE_LEFT

GROUND_TOP_TABLE = {'A0e', 'A0f', 'A0g', 'B0c', 'B0d', 'L0c', 'L0d'}   # table printed above the drawing


def sheets(map_file):
    out = []
    for line in open(map_file):
        code, rest = line.strip().split('=')
        for item in rest.split(','):
            sid, title = item.split(':', 1)
            if title.endswith('Planta Baja') or title.endswith('Planta'):
                out.append((code, sid, title))
    return out


if __name__ == '__main__':
    src, mp, dst = sys.argv[1:4]
    os.makedirs(dst, exist_ok=True)
    for code, sid, title in sheets(mp):
        kind = title[0]
        ground = title.endswith('Planta Baja')
        if kind == 'V':
            name, label = f'{code}-{"ground" if ground else "upper"}', ('Ground floor' if ground else 'First floor and solarium')
        else:
            name = code
            label = 'Ground floor' if ground else ('Floor plan and solarium' if kind == 'T' else 'Floor plan')
        blank = [] if (ground and kind == 'A' and code in GROUND_TOP_TABLE) else [TABLE_LEFT]
        size = cut(f'{src}/{code}_{sid}.jpg', f'{dst}/{name}.jpg', label, blank=blank, frame=FRAME_MH, by_colour=True)
        print(name, size)
