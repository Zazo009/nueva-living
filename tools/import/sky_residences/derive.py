# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
import os
from PIL import Image
S='la-quinta-summit-residences-villas'
base='/Users/sasanraftari/Projects/nueva-living/assets/liora/projects/'+S
made=0
for folder,narrow in (('media',False),('floorplans',True)):
    d=f'{base}/{folder}'
    for n in sorted(os.listdir(d)):
        if not n.endswith('.jpg'): continue
        src=f'{d}/{n}'; b=src[:-4]
        for suf,w in ([('.webp',None)] if not narrow else [])+[('-960.webp',960),('-640.webp',640)]:
            out=b+suf
            if os.path.exists(out) and os.path.getmtime(out)>=os.path.getmtime(src): continue
            im=Image.open(src).convert('RGB')
            if w and im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
            im.save(out,'WEBP',quality=72,method=6); made+=1
print('made',made)
