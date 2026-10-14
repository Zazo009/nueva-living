"""Cuts the plain drawings out of the 13 per-home plan sheets of Mirlo Residences.

Each sheet (A4-ish portrait, 614 x 692 pt) carries a dark banner with the developer's logo and the
real project name, the drawing, a room-area table, a cross-section sketch and two small floor
sketches of the building. Only the drawing is published, so the banner, the table and the sketches
are whited out and the biggest group of ink that is left is the drawing (tm_plans.cut, same method).
The area table is dropped: its figures go into the project's text where they differ from the list.

    python3 tools/import/mirlo_plans.py <sheet.pdf> <out.jpg> "Ground floor"

The sheet is rendered at 230 dpi first. Every output has to be looked at before it ships.
"""
import os
import sys
import tempfile

import fitz

sys.path.insert(0, os.path.dirname(__file__))
import tm_plans  # noqa: E402

# Display coordinates (2000 wide) of what is never the drawing.
FRAME = [
    (0, 0, 2000, 357),         # banner: logo and the project name
    (1355, 340, 2000, 900),    # room-area table
    (1090, 1330, 2000, 2250),  # section sketch and the two floor sketches
]


def below_scale_bar(png):
    """Display rectangle covering everything under the sheet's graphic scale bar.

    The floor sketches sit under the scale bar on every sheet but close enough to it for the
    grouping to join them to the drawing, so the "ESCALA GRAFICA" caption is located by OCR and
    everything below its number row is blanked. Returns [] when the caption is not found."""
    from rapidocr_onnxruntime import RapidOCR
    res, _ = RapidOCR()(png)
    for box, text, _score in res or []:
        if text.upper().replace(' ', '').startswith('ESCALA'):
            bottom = max(p[1] for p in box)
            return [(0, (bottom + 55) * 2000 / 1964, 2000, 2250)]
    return []


def cut_sheet(pdf, out, label, join=5, extra=()):
    page = fitz.open(pdf)[0]
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, 'sheet.png')
        page.get_pixmap(dpi=230).save(png)
        size = tm_plans.cut(png, out, label, join=join,
                            blank=list(extra) + below_scale_bar(png), frame=FRAME)
    drop_sketch_captions(out)
    return size


def drop_sketch_captions(path):
    """A floor sketch's caption ("ESQUEMA SOTANO -1") can survive the cut when the sketch itself was
    blanked: OCR the result and white everything from the caption to the right and below it."""
    from PIL import Image
    from rapidocr_onnxruntime import RapidOCR
    res, _ = RapidOCR()(path)
    img = Image.open(path).convert('RGB')
    changed = False
    for box, text, _score in res or []:
        if text.upper().startswith('ESQUEMA'):
            x0 = max(0, int(min(p[0] for p in box)) - 40)
            y0 = max(0, int(min(p[1] for p in box)) - 45)
            y1 = int(max(p[1] for p in box)) + 40
            img.paste((255, 255, 255), (x0, y0, img.width, min(img.height - 60, y1)))
            changed = True
    if changed:
        img.save(path, 'JPEG', quality=82, progressive=True, optimize=True)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    print(cut_sheet(*sys.argv[1:4]))
