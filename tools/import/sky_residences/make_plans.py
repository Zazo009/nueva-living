# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
import sys, os, re, json, fitz
sys.path.insert(0,'/Users/sasanraftari/Downloads/SkyMarbella_work')
from units_data import apartments, villas
from PIL import Image, ImageChops
R='/Users/sasanraftari/Downloads/SkyMarbella_dropbox/x/'
OUT='/Users/sasanraftari/Downloads/SkyMarbella_work/out/floorplans/'
LEVEL={'SÓTANO':('basement','Basement'),'BAJA':('ground-floor','Ground floor'),'PRIMERA':('first-floor','First floor'),'SEGUNDA':('second-floor','Second floor'),'ÁTICO':('penthouse-floor','Penthouse')}
ORDER=['basement','ground-floor','first-floor','second-floor','penthouse-floor']
def autocrop(im,pad=24):
    bb=ImageChops.difference(im,Image.new('RGB',im.size,(255,255,255))).getbbox()
    x0,y0,x1,y1=bb; return im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
def save(im,path):
    s=2000/max(im.size)
    if s<1: im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    im.save(path,'JPEG',quality=82,progressive=True,optimize=True)
manifest={}
def render(page,clip,dpi_target=2000):
    w=clip.width; h=clip.height; scale=min(3.0,dpi_target*1.15/max(w,h))
    pm=page.get_pixmap(matrix=fitz.Matrix(scale,scale),clip=clip)
    return Image.frombytes('RGB',(pm.width,pm.height),pm.samples)
def level_of(page):
    t=page.get_text()
    m=re.search(r'//\s*PLANTA\s+([A-ZÓÁÉÍÚ]+)',t) or re.search(r'PLANTA\s+([A-ZÓÁÉÍÚ]+)\s+_\s+VIVIENDA',t)
    return m.group(1)
for a in apartments:
    if not a['price']: continue
    d=fitz.open(R+f"Apartments/Floor plans/{a['door']}.pdf")
    lv=[]
    for pg in d:
        key,label=LEVEL[level_of(pg)]
        clip=fitz.Rect(0,0,1815,1612)
        im=autocrop(render(pg,clip))
        name=f"apartment-{a['door'].lower()}-{key}.jpg"; save(im,OUT+name); lv.append((key,label,name))
    lv.sort(key=lambda x:ORDER.index(x[0])); manifest['apt:'+a['door']]=lv
for v in villas:
    if not v['price']: continue
    d=fitz.open(R+f"Villas/Floor plans/{v['file']}.pdf")
    lv=[]
    for pg in d:
        t=pg.get_text()
        code=re.search(r'V(\d\d) - MOBILIARIO',t).group(1)
        assert f'V{code}'==v['code'],(v,code)
        assert v['usable'] in t,(v['no'],v['usable'])
        if 'PLANTA\nBAJA' in t or re.search(r'PLANTA\s*\nBAJA',t): key,label='ground-floor','Ground floor'
        elif 'PRIMERA' in t: key,label='first-floor','First floor'
        elif 'SÓTANO' in t: key,label='basement','Basement'
        else: raise SystemExit(('level?',v['no']))
        clip=fitz.Rect(0,0,976,pg.rect.height)
        im=autocrop(render(pg,clip))
        name=f"villa-{v['no']}-{key}.jpg"; save(im,OUT+name); lv.append((key,label,name))
    lv.sort(key=lambda x:ORDER.index(x[0])); manifest['villa:'+str(v['no'])]=lv
json.dump(manifest,open('/Users/sasanraftari/Downloads/SkyMarbella_work/plans_manifest.json','w'),indent=1)
print(len(manifest), sum(len(x) for x in manifest.values()))
