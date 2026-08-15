#!/usr/bin/env python3
"""Generate WebP derivatives for project imagery.

Run locally and commit the output, exactly like the existing /cards/
avif+webp derivatives. The build only checks whether a derivative exists,
so it never depends on an image toolchain being present in CI.

Covers both the gallery folder and the project root, where the section
images live (hero.jpg, architecture.jpg, lifestyle.jpg, ...). The hero is
the LCP element on every property page, so it must not be missed.

Produces, alongside each source JPEG:
  <name>.webp       full width, largest <picture> candidate
  <name>-960.webp   960px wide, mid candidate
  <name>-640.webp   640px wide, for cards and media tiles -- those render
                    around 300-400 CSS px, so 640px still covers 2x
                    displays while the untouched source is ~2000px.
"""
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python3 -m pip install Pillow")

ROOT = "assets/liora/projects"
QUALITY = 72
WIDTHS = ((".webp", None), ("-960.webp", 960), ("-640.webp", 640))

sources = []
for slug in sorted(os.listdir(ROOT)):
    project_dir = os.path.join(ROOT, slug)
    if not os.path.isdir(project_dir):
        continue
    for folder in (project_dir, os.path.join(project_dir, "media")):
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            if name.lower().endswith((".jpg", ".jpeg")):
                sources.append(os.path.join(folder, name))

made = skipped = 0
for src in sources:
    base = os.path.splitext(src)[0]
    for suffix, width in WIDTHS:
        out = base + suffix
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
            skipped += 1
            continue
        im = Image.open(src).convert("RGB")
        if width and im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=QUALITY, method=6)
        made += 1

print(f"image derivatives: {made} generated, {skipped} up to date ({len(sources)} sources)")
