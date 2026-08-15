#!/usr/bin/env python3
"""Generate WebP derivatives for project media images.

Run locally and commit the output, exactly like the existing /cards/
avif+webp derivatives. The build only checks whether a derivative exists,
so it never depends on an image toolchain being present in CI.

Produces, alongside each source JPEG:
  <name>.webp       full width, for the <picture> source
  <name>-960.webp   960px wide, for the srcset small candidate
"""
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python3 -m pip install Pillow")

ROOT = "assets/liora/projects"
QUALITY = 72
made = skipped = 0

for slug in sorted(os.listdir(ROOT)):
    media = os.path.join(ROOT, slug, "media")
    if not os.path.isdir(media):
        continue
    for name in sorted(os.listdir(media)):
        if not name.lower().endswith((".jpg", ".jpeg")):
            continue
        src = os.path.join(media, name)
        base = os.path.splitext(src)[0]
        for out, width in ((base + ".webp", None), (base + "-960.webp", 960)):
            if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
                skipped += 1
                continue
            im = Image.open(src).convert("RGB")
            if width and im.width > width:
                im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            im.save(out, "WEBP", quality=QUALITY, method=6)
            made += 1

print(f"image derivatives: {made} generated, {skipped} up to date")
