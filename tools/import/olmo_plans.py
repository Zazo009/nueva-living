"""Cuts the plan sheets of Olmo Residences into the plain drawings published.

    python3 tools/import/olmo_plans.py <planos dir> <out dir>

The developer's A4-landscape sheets (3508 x 2479, or 6828 x 4961 for the living-level
sheets of types C to E) all share one layout: the developer's logo top left, the drawing
in the middle, a compass and scale bar bottom left, and the whole right-hand third taken
by the project title, the area table and a site map. Those three zones are fixed, so the
frame below blanks them and tm_plans.cut keeps the largest group of ink, which is the
drawing. Outputs are `<code>-<level>.jpg` with the level printed under the drawing.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tm_plans
from tm_plans import cut

FRAME_OLMO = [
    (0, 0, 280, 150),          # developer logo
    (1415, 0, 2000, 1414),     # title, area table, site map, legal line
    (0, 1180, 430, 1414),      # compass and scale bar
]
LIVING, BED, SOL = 'Living level', 'Bedroom level', 'Solarium'
# code: [(sheet file, output suffix, label)]
SHEETS = {
    'a2': [('A2_1', 'living-level', LIVING), ('A2_2', 'bedroom-level', BED)],
    'a4': [('A4_1', 'living-level', LIVING), ('A4_2', 'bedroom-level', BED)],
    'a5': [('A5_1', 'living-level', LIVING), ('A5_2', 'bedroom-level', BED)],
    'b2': [('B2', 'living-level', LIVING), ('B2_2', 'bedroom-level', BED)],
    'b3': [('B3_1', 'living-level', LIVING), ('B3_2', 'bedroom-level', BED)],
    'c1': [('C1_2', 'bedroom-level', BED), ('C1_3', 'solarium', SOL)],
    'e2': [('E2_2', 'bedroom-level', BED), ('E2_3', 'solarium', SOL)],
}
for c, n in (('c', 5), ('d', 4), ('e', 4)):
    for i in range(1, n + 1):
        k = f'{c}{i}'
        if k in SHEETS or k == 'c1' or k == 'e2':
            continue
        U = k.upper()
        SHEETS[k] = [(f'{U}.1', 'living-level', LIVING), (f'{U}_2', 'bedroom-level', BED), (f'{U}_3', 'solarium', SOL)]
if __name__ == '__main__':
    src, out = sys.argv[1:3]
    os.makedirs(out, exist_ok=True)
    for code, items in sorted(SHEETS.items()):
        for sheet, suffix, label in items:
            print(code, suffix, cut(f'{src}/{sheet}.jpg', f'{out}/{code}-{suffix}.jpg', label, frame=FRAME_OLMO))
