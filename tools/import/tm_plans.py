"""Turns a developer's branded plan sheets into the plain drawings the site publishes.

The sheets this was written for (a Costa del Sol developer, 2024 template, A3
landscape at 3309 x 2339) carry the developer's logo, the real project name set in
large type, a street-name site map, a table of room areas and a footer, all around
the drawing. The anonymisation rule is that the developer's name or logo must never
appear in an image that ships, so the drawing is cut out and everything else is
dropped. That is also what the existing villa plans (Cortijo Blanco) look like: the
drawing, a floor label, nothing else.

The first version cropped fixed rectangles. It worked for one villa and failed on the
next four, because the layout moves from villa to villa and from floor to floor: the
area table is sometimes beside the drawing and sometimes above it, and the site map
sits in a different corner on almost every sheet. A rectangle that excluded "Avenida
Pernet" on one sheet included it on the next, and a street name left in an image is
exactly what this exists to stop.

So it does not measure positions. The drawing is the largest connected mass of ink on
the sheet; tables, maps and legends are separate blocks, and the logo, the wordmark and
the footer sit in the same place on every sheet because they belong to the frame, not
the drawing. The frame zones are excluded, the rest is grouped by proximity, the
biggest group is kept, and everything outside it is whited out.

    python3 tools/import/tm_plans.py <sheet.jpg> <out.jpg> "Ground floor"

`blank` takes extra rectangles to remove before grouping, for the rare sheet where a
table sits against the drawing.

Two limits, both found by looking at the output. A part of the drawing that sits more
than about 30 px of display away from the rest is treated as a separate block and
dropped. And a table printed closer than that to the drawing would be kept with it.
Every output has to be looked at before it ships -- this removes what it knows to look
for and nothing else.

The room-area table is dropped with the rest. Those figures go into the project's
`residences.items[].features` as text, as Cortijo Blanco does.
"""
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFont

DISPLAY_W = 2000      # coordinates below are on a 2000-px-wide display of the sheet
BLOCK = 8             # grouping grid, in real pixels
JOIN = 5              # blocks of dilation: ~40 real px, ~24 display px; 4 starts cutting real drawing
PAD = 36              # white margin around the drawing, in display px
MAX_SIDE = 2000       # source images are at most 2000 px, quality 82, progressive
INK = 244             # a pixel darker than this is not paper

# Frame zones: the same on every sheet, never part of the drawing.
FRAME = [
    (0, 0, 2000, 45), (0, 0, 45, 1414), (1955, 0, 2000, 1414), (0, 1380, 2000, 1414),  # border
    (1590, 20, 1990, 232),     # logo block
    (30, 50, 570, 160),        # wordmark and its "by" line
    (0, 1238, 2000, 1414),     # footer: type, date, the developer's legal line
]

# The 2023 template of a second developer sheet (A3 landscape, 2483 x 1757): the logo, the
# north arrow, the street-name site map, the block key and the room-area table all sit in
# the left 560-630 px, the other developer's logo top right, the legal line along the
# foot. A one-storey unit's drawing starts at x ~ 650; the angled bedroom of the third-
# floor type C3 reaches x ~ 580, which is why the left zones stop short of 570.
FRAME_HBR = [
    (0, 0, 2000, 30), (0, 0, 30, 1414), (1968, 0, 2000, 1414),      # border
    (40, 40, 560, 870),        # logo, north arrow, site map, block key
    (40, 875, 632, 1290),      # room-area table
    (1650, 40, 1966, 200),     # the developer's logo
    (0, 1293, 2000, 1414),     # type, date, scale bar, legal line
    (1450, 1270, 2000, 1414),  # the date rides higher than the rest of the foot
]


def _font(size):
    for path in ('/System/Library/Fonts/Helvetica.ttc', '/Library/Fonts/Arial.ttf',
                 '/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _largest_group(ink, join=JOIN, keep=1):
    """Boolean mask, at pixel size, of the `keep` biggest groups of ink on the sheet."""
    h, w = ink.shape
    gh, gw = h // BLOCK, w // BLOCK
    cells = ink[:gh * BLOCK, :gw * BLOCK].reshape(gh, BLOCK, gw, BLOCK)
    weight = cells.sum(axis=(1, 3))
    grid = weight > 0

    near = np.zeros_like(grid)
    padded = np.pad(grid, join)
    for dy in range(2 * join + 1):
        for dx in range(2 * join + 1):
            near |= padded[dy:dy + gh, dx:dx + gw]

    label = np.zeros(near.shape, dtype=np.int32)
    weights, count = {}, 0
    for sy, sx in zip(*np.nonzero(near)):
        if label[sy, sx]:
            continue
        count += 1
        total, queue = 0, deque([(sy, sx)])
        label[sy, sx] = count
        while queue:
            y, x = queue.popleft()
            total += weight[y, x]
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= ny < gh and 0 <= nx < gw and near[ny, nx] and not label[ny, nx]:
                    label[ny, nx] = count
                    queue.append((ny, nx))
        weights[count] = total

    chosen = sorted(weights, key=weights.get, reverse=True)[:keep]
    mask = np.repeat(np.repeat(np.isin(label, chosen), BLOCK, axis=0), BLOCK, axis=1)
    full = np.zeros((h, w), dtype=bool)
    full[:mask.shape[0], :mask.shape[1]] = mask
    return full


def cut(sheet_path, out_path, label, join=JOIN, blank=(), frame=FRAME, keep=1):
    sheet = Image.open(sheet_path).convert('RGB')
    s = sheet.width / DISPLAY_W
    pixels = np.asarray(sheet)
    ink = pixels.min(axis=2) < INK
    # `blank` is for a sheet where a table sits so close to the drawing that no grouping
    # distance separates them (the 3-bedroom villa E, ground floor); display coordinates.
    for zx0, zy0, zx1, zy1 in list(frame) + list(blank):
        ink[round(zy0 * s):round(zy1 * s), round(zx0 * s):round(zx1 * s)] = False

    group = _largest_group(ink, join, keep)
    mine = ink & group
    ys, xs = np.nonzero(mine)
    if not len(ys):
        raise SystemExit(f'{sheet_path}: no drawing found')
    pad = round(PAD * s)
    x0, x1 = max(0, xs.min() - pad), min(sheet.width, xs.max() + pad)
    y0, y1 = max(0, ys.min() - pad), min(sheet.height, ys.max() + pad)

    # Whatever is inside the box but not in the drawing's group (a table printed in
    # the box's corner, a street name) goes white.
    out = pixels.copy()
    out[~group] = 255
    # The group is grown to join the drawing's parts, so it can reach a few blocks into a
    # frame zone beside the drawing. Whatever the zone holds is the logo, the wordmark or
    # the footer, never the drawing: white it, so nothing branded survives by proximity.
    for zx0, zy0, zx1, zy1 in list(frame) + list(blank):    # not x0..y1: those hold the crop
        out[round(zy0 * s):round(zy1 * s), round(zx0 * s):round(zx1 * s)] = 255
    drawing = Image.fromarray(out[y0:y1, x0:x1])

    label_h = round(70 * s)
    canvas = Image.new('RGB', (drawing.width, drawing.height + label_h), 'white')
    canvas.paste(drawing, (0, 0))
    ImageDraw.Draw(canvas).text((round(24 * s), drawing.height + round(14 * s)), label.upper(),
                                fill=(60, 60, 60), font=_font(round(30 * s)))

    if max(canvas.size) > MAX_SIDE:
        r = MAX_SIDE / max(canvas.size)
        canvas = canvas.resize((round(canvas.width * r), round(canvas.height * r)), Image.LANCZOS)
    canvas.save(out_path, 'JPEG', quality=82, progressive=True, optimize=True)
    return canvas.size


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    print(cut(*sys.argv[1:4]))
