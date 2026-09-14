"""Ad creative in the three shapes Meta actually places.

Two sources per project -- the card image and the hero -- because the first
question a test answers is which frame pulls, and those are the two already
chosen as the best single shot of a scheme.

1:1 and 4:5 are centre crops: the loss is 44% and 30% of the width, which
architectural renders survive, since the building is what sits in the middle.

9:16 is NOT cropped. Going from 16:9 to 9:16 keeps 31% of the width and throws
away two thirds of the frame, which turns a considered composition into a
detail of a wall. The full image is placed on a brand-coloured canvas instead,
so a Story shows the photograph the developer actually made.

Output goes outside assets/ on purpose: this is creative for an ad account,
not something the website serves, and 300 JPEGs have no business in the deploy.
"""
import json, os, sys, glob
from PIL import Image

BRAND_DEEP = (47, 36, 23)          # --nueva-deep #2f2417
SHAPES = [('1x1', 1080, 1080, 'crop'), ('4x5', 1080, 1350, 'crop'),
          ('9x16', 1080, 1920, 'fit')]
# What gets placed on the 9:16 canvas. Placing the untouched 16:9 frame filled
# barely a third of a Story and read as a mistake; cropping all the way to 9:16
# keeps 31% of the width and destroys the composition. A 4:5 crop is the
# middle: 70% of the canvas, 30% of the width lost, and the band left top and
# bottom is where a headline goes.
FIT_RATIO = 4 / 5
OUT = sys.argv[1] if len(sys.argv) > 1 else 'ad-creative'


def crop_to(im, w, h):
    target = w / h
    iw, ih = im.size
    if iw / ih > target:
        nw = int(ih * target)
        im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:
        nh = int(iw / target)
        im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
    return im.resize((w, h), Image.LANCZOS)


def fit_to(im, w, h):
    canvas = Image.new('RGB', (w, h), BRAND_DEEP)
    im = crop_to(im, w, int(w / FIT_RATIO))
    scale = min(w / im.size[0], h / im.size[1])
    scaled = im.resize((max(1, int(im.size[0] * scale)),
                        max(1, int(im.size[1] * scale))), Image.LANCZOS)
    canvas.paste(scaled, ((w - scaled.size[0]) // 2, (h - scaled.size[1]) // 2))
    return canvas


made = skipped = 0
projects = 0
for path in sorted(glob.glob('content/liora-projects/*/project.json')):
    d = json.load(open(path))
    slug = d['slug']
    sources = {}
    for key in ('card', 'hero'):
        src = (d.get('images', {}).get(key) or {}).get('src')
        if src and os.path.exists(src):
            sources[key] = src
    if not sources:
        continue
    projects += 1
    os.makedirs(f'{OUT}/{slug}', exist_ok=True)
    for key, src in sources.items():
        im = Image.open(src).convert('RGB')
        for name, w, h, mode in SHAPES:
            out = f'{OUT}/{slug}/{key}-{name}.jpg'
            img = crop_to(im, w, h) if mode == 'crop' else fit_to(im, w, h)
            img.save(out, quality=88, optimize=True, progressive=True)
            made += 1

print(f'{projects} projects -> {made} images in {OUT}/')
print(f'  shapes: {", ".join(f"{n} {w}x{h} ({m})" for n, w, h, m in SHAPES)}')
