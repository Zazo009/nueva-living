#!/usr/bin/env python3
"""Share images: one 1200x630 picture per page, unique to that page, small enough for WhatsApp.

A link pasted into WhatsApp, iMessage, Slack or LinkedIn is shown with the page's og:image. The
pages used to point it at their full hero image, 450-1000 KB and up to 2048 px wide, and WhatsApp
quietly drops a preview image that large: the Design Hills and Ocho de Oro links went out with no
picture at all while Tyrian, a little smaller, came through. And 38 pages that had no image of their
own all shared one fallback, so every guide looked like every other guide in a chat.

This script picks a picture for every English page in dist/, crops it to 1200x630 (the 1.91:1 that
every preview renders), saves it as a baseline JPEG under 200 KB in assets/liora/share/<page>.jpg,
and records the choice in content/share-images.json. build_dist.mjs points og:image and
twitter:image at that file on the page and on its nine translations; the audit fails a page whose
share image is missing, too large, or the same picture as another page's.

Choosing: the page's current og:image if it is its own (a project's hero); otherwise the first
picture in the page that no other page has already taken. A choice once made is kept, so
re-running only adds pages, and the picture someone shared last week does not change under them.

    python3 scripts/make_share_images.py          # after a build, adds what is missing
    python3 scripts/make_share_images.py --force  # recrops every page from its recorded source
"""
import hashlib
import io
import json
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
OUT_DIR = os.path.join(ROOT, 'assets', 'liora', 'share')
MANIFEST = os.path.join(ROOT, 'content', 'share-images.json')
SITE = 'https://nuevaliving.com/'
FALLBACK = 'assets/liora/viewing/scene-08.jpg'
W, H = 1200, 630
MAX_BYTES = 200_000

# Pages that are not shared and need no picture of their own.
SKIP = {'404.html', 'thank-you.html'}


def english_pages():
    for name in sorted(os.listdir(DIST)):
        if name.endswith('.html') and name not in SKIP:
            yield name


def og_image(html):
    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if not m:
        return None
    url = m.group(1).split('?')[0]
    return url[len(SITE):] if url.startswith(SITE) else None


def page_images(html):
    """Local raster images in the page, in document order."""
    seen = []
    for m in re.finditer(r'<img[^>]+src="([^"]+)"', html):
        src = m.group(1).split('?')[0].lstrip('./')
        if src.startswith(SITE):
            src = src[len(SITE):]
        if src.startswith(('http', 'data:')) or not re.search(r'\.(jpe?g|png|webp)$', src, re.I):
            continue
        if '/brand/' in src or 'favicon' in src or '/icons/' in src or '/team/' in src:
            continue
        if src not in seen:
            seen.append(src)
    return seen


def usable(src):
    path = os.path.join(ROOT, src)
    if not os.path.exists(path):
        # a derivative named in the page; fall back to the original jpg beside it
        alt = re.sub(r'(-\d+)?\.(webp|avif)$', '.jpg', path)
        if os.path.exists(alt):
            return os.path.relpath(alt, ROOT)
        return None
    try:
        with Image.open(path) as im:
            if im.width < 800 or im.height < 420:
                return None
    except Exception:
        return None
    return src


def file_sha(src):
    with open(os.path.join(ROOT, src), 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def render(src, dest):
    with Image.open(os.path.join(ROOT, src)) as im:
        im = im.convert('RGB')
        scale = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        left = (im.width - W) // 2
        top = (im.height - H) // 2
        im = im.crop((left, top, left + W, top + H))
        for quality in (82, 76, 70, 64, 58):
            buf = io.BytesIO()
            im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=False)
            if buf.tell() <= MAX_BYTES:
                break
        with open(dest, 'wb') as fh:
            fh.write(buf.getvalue())
        return buf.tell()


def main():
    force = '--force' in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = {}
    if os.path.exists(MANIFEST):
        with open(MANIFEST) as fh:
            manifest = json.load(fh)
    taken = {entry['source'] for entry in manifest.values()}
    # the same picture is sometimes kept under two paths (a hero copied from the gallery), so
    # a source is taken when its bytes are, not only its name
    taken_bytes = {file_sha(entry['source']) for entry in manifest.values()}
    pages = list(english_pages())

    # A project hero is the page's own picture; claim those first so a guide that happens to
    # show a project's render does not take it from the project's page.
    order = sorted(pages, key=lambda p: (not p.startswith('property-'), p))
    added = 0
    for page in order:
        if page in manifest and not force:
            continue
        html = open(os.path.join(DIST, page), encoding='utf-8', errors='ignore').read()
        candidates = []
        own = og_image(html)
        if own and own != FALLBACK:
            candidates.append(own)
        candidates += page_images(html)
        # A page whose own pictures are all taken (a guide, a filtered list) borrows from the
        # projects it links to, then from the site's own viewing scenes.
        for slug in dict.fromkeys(re.findall(r'href="property-([a-z0-9-]+)\.html"', html)):
            media = os.path.join(ROOT, 'assets', 'liora', 'projects', slug, 'media')
            if os.path.isdir(media):
                files = [f for f in sorted(os.listdir(media)) if f.lower().endswith(('.jpg', '.jpeg'))
                         and not re.search(r'plan|bath|shower|kitchen|bedroom|toilet|wardrobe', f, re.I)]
                # outside first: a chat thumbnail of a bathroom says nothing about a page of homes
                files.sort(key=lambda f: not re.search(r'exterior|aerial|facade|pool|terrace|view|garden|sea', f, re.I))
                candidates += [f'assets/liora/projects/{slug}/media/{f}' for f in files]
        viewing = os.path.join(ROOT, 'assets', 'liora', 'viewing')
        candidates += [f'assets/liora/viewing/{f}' for f in sorted(os.listdir(viewing))
                       if f.startswith('scene-') and f.endswith('.jpg') and f'assets/liora/viewing/{f}' != FALLBACK]
        source = None
        for cand in candidates:
            cand = usable(cand)
            if cand and (manifest.get(page, {}).get('source') == cand
                         or (cand not in taken and file_sha(cand) not in taken_bytes)):
                source = cand
                break
        if not source:
            print(f'no unused picture for {page}; add one to the page or to the manifest by hand')
            continue
        stem = page[:-5]
        dest = os.path.join(OUT_DIR, f'{stem}.jpg')
        size = render(source, dest)
        with open(dest, 'rb') as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()[:16]
        manifest[page] = {'source': source, 'file': f'assets/liora/share/{stem}.jpg', 'sha': digest}
        taken.add(source)
        taken_bytes.add(file_sha(source))
        added += 1
        print(f'{page}: {source} -> {size // 1024} KB')

    with open(MANIFEST, 'w') as fh:
        json.dump(dict(sorted(manifest.items())), fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    print(f'{added} share images written, {len(manifest)} pages in the manifest')


if __name__ == '__main__':
    main()
