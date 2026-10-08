"""Cuts the five plan sheets of Higuerón Bay Residences into the plain drawings published.

    python3 tools/import/hbr_plans.py <sheet dir> <out dir>

The sheets are the developer's October 2023 template (see FRAME_HBR in tm_plans.py). Two
need more than the frame: B0a, whose right side carries the variants of three other
units (B0b, B0c, B0d), and H3, whose floor plan and solarium plan sit side by side far
enough apart to read as two groups.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tm_plans import cut, FRAME_HBR

SHEETS = {   # sheet id: (output name, label, extra blank zones, groups to keep)
    'COB781388': ('b0a-ground-floor', 'Ground floor', [(1120, 215, 1966, 1292)], 1),
    'COB781409': ('d0-ground-floor', 'Ground floor', [], 1),
    'COB781445': ('f0-ground-floor', 'Ground floor', [], 1),
    'COB781405': ('c3-third-floor-and-solarium', 'Third floor and solarium', [], 1),
    'COB781414': ('h3-third-floor-and-solarium', 'Third floor and solarium', [], 2),
}
if __name__ == '__main__':
    src, out = sys.argv[1:3]
    os.makedirs(out, exist_ok=True)
    for sheet, (name, label, blank, keep) in SHEETS.items():
        print(name, cut(f'{src}/{sheet}.jpg', f'{out}/{name}.jpg', label, blank=blank, frame=FRAME_HBR, keep=keep))
