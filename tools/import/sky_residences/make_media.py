# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
import sys, os
sys.path.insert(0,'/Users/sasanraftari/Downloads/SkyMarbella_work')
from gallery_def import GALLERY
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS=None
R='/Users/sasanraftari/Downloads/SkyMarbella_dropbox/x/'
OUT='/Users/sasanraftari/Downloads/SkyMarbella_work/out/media/'
for src,name,cat,cap,alt in GALLERY:
    o=OUT+name+'.jpg'
    if os.path.exists(o) and '--force' not in sys.argv: continue
    if src=='MODEL':
        import fitz, io, PIL.ImageChops as C
        x=fitz.open(R+'Villas/Floor plans/3D Masterplan villas with numbers.pdf').extract_image(5)
        im=Image.open(io.BytesIO(x['image'])).convert('RGB')
        im=im.crop(C.difference(im,Image.new('RGB',im.size,(255,255,255))).getbbox())
    else:
        im=Image.open(R+src); im=ImageOps.exif_transpose(im).convert('RGB')
    im.thumbnail((2000,2000), Image.LANCZOS)
    im.save(o,'JPEG',quality=82,progressive=True,optimize=True)   # no exif passed => stripped
    print(name, im.size, os.path.getsize(o)//1024,'KB')
