"""Altamira Hills Residences: cuts the developer plan sheets down to the drawing (Phase IV template with the logo top left and the table and site map on the right; the older portal sheets with a logo box and a thumbnail column). Run from the folder holding planos/; writes plans/home-<ref>.jpg, drawing plus a label, nothing else. Every output was looked at."""
import numpy as np, sys, os
from PIL import Image, ImageDraw, ImageFont
P='../planos/'
S=4960/1800
T4=[(215,72,1365,1140)]; T1=[(215,262,1345,1175),(315,5,1345,262)]
def region(path,box):
    im=Image.open(path).convert('RGB'); s=im.width/1800
    a=np.asarray(im); ink=a.min(axis=2)<244
    m=np.zeros_like(ink)
    for b in box:
        x0,y0,x1,y1=[round(v*s) for v in b]; m[y0:y1,x0:x1]=True
    ink&=m
    ys,xs=np.nonzero(ink); pad=round(30*s)
    bx0,bx1,by0,by1=xs.min(),xs.max(),ys.min(),ys.max()
    touch=[n for n,c in (('L',bx0<=x0+3),('R',bx1>=x1-3),('T',by0<=y0+3),('B',by1>=y1-3)) if c] if len(box)==1 else []
    white=np.full_like(a,255); white[m]=a[m]
    out=Image.fromarray(white).crop((max(0,bx0-pad),max(0,by0-pad),min(im.width,bx1+pad),min(im.height,by1+pad)))
    return out,touch
def font(sz):
    for p in ('/System/Library/Fonts/Helvetica.ttc','/Library/Fonts/Arial.ttf'):
        try: return ImageFont.truetype(p,sz)
        except OSError: pass
def build(files,box,label,out):
    parts=[];tt=[]
    for f in files:
        o,t=region(P+f,box); parts.append(o); tt.append(t)
    h=max(p.height for p in parts); w=sum(p.width for p in parts)+80*(len(parts)-1)
    c=Image.new('RGB',(w,h),'white'); x=0
    for p in parts: c.paste(p,(x,0)); x+=p.width+80
    lab=Image.new('RGB',(w,170),'white'); ImageDraw.Draw(lab).text((40,40),label,fill=(40,40,40),font=font(95))
    full=Image.new('RGB',(w,h+170),'white'); full.paste(c,(0,0)); full.paste(lab,(0,h))
    full.thumbnail((2000,2000),Image.LANCZOS)
    full.save(out,quality=82,progressive=True,optimize=True)
    return tt,full.size
M={ # ref: (files, template)
'154B':(['154B_-_2-5-15_N02_N03_B.jpg'],T1),'164B':(['164B_-_2-6-16_N02_N03_B.jpg'],T1),
'160B':(['160B_-_2-6-16_N-02_B.jpg'],T1),'162A':(['162A_-_2-6-16_N00_A.jpg'],T1),'163B':(['COM-04-163B_-_2-6-16_N01_B.jpg'],T1),
'410A':(['10A.jpg'],T4),'410B':(['10B.jpg'],T4),'412B':(['12B.jpg'],T4),'413A':(['13A.jpg'],T4),
'414B':(['14b_2__floor.jpg','14B.jpg'],T4),'420A':(['20A.jpg'],T4),'422A':(['22A.jpg'],T4),
'424B':(['24B_2__floor.jpg','24B.jpg'],T4),'430A':(['30A.jpg'],T4),'430B':(['30B.jpg'],T4),'431D':(['31D.jpg'],T4),'434A':(['34A.jpg'],T4)}
if __name__=='__main__':
    os.makedirs('plans',exist_ok=True)
    for r,(f,b) in M.items():
        print(r,build(f,b,'HOME '+r,f'plans/home-{r.lower()}.jpg'))
