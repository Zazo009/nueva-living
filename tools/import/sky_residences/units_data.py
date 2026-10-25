# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
# -*- coding: utf-8 -*-
import json
APT=json.load(open('/Users/sasanraftari/Downloads/SkyMarbella_work/apt_rows_raw.json'))
def f(s): return s.replace('.','').replace(',','.') if s and ',' in s and False else s
def n(s):  # '1.234,56' or '216,02' -> float
    s=s.strip().replace('.','').replace(',','.'); return float(s)
def fmt(s):  # price-list decimal string '216,02' -> '216.02'
    return s.strip().replace(',','.')
apartments=[]
for r in APT:
    if r.get('door') is None or r['door'].startswith('AVISO') or 'type' not in r or 'bed' not in r: continue
    door=r['door'].replace(' ','')
    price=r['price']
    apartments.append(dict(door=door,block=int(r['block']),type=r['type'],interior=fmt(r['interior']),terrace=fmt(r['terrace']) if r.get('terrace') else None,
        porche=fmt(r['porche']) if r.get('porche') else None, ext=fmt(r['ext']), garden=fmt(r['garden']) if r.get('garden') else None, total=fmt(r['total']),
        bed=int(r['bed']), bath=r['bath'], price=None if price.startswith('Reserved') else int(price.replace('€','').replace('.','').strip())))
VIL=[ # no, plot, interior, terraces, usable, beds, baths, price(None=reserved), plan file, internal code
 (1,935,924,198,'862.91',6,'6+2',None,'Villa 1','V01'),(2,870,881,248,'862.28',6,'6+2',6895000,'Villa 2','V02'),
 (3,913,822,209,'746.60',5,'5+2',None,'Villa 13','V03'),(4,1045,824,208,'786.74',5,'5+2',6495000,'Villa 4','V04'),
 (5,1058,920,234,'867.89',6,'6+2',7495000,'Villa 9','V05'),(6,846,818,186,'753.42',5,'5+2',7350000,'Villa 6','V06'),
 (7,979,863,183,'743.96',6,'6+2',8495000,'Villa 7','V07'),(8,1017,896,249,'867.49',6,'6+2',None,'Villa 8','V08'),
 (9,690,920,195,'830.61',6,'6+2',None,'Villa 10','V09'),(10,1614,937,247,'887.79',6,'6+2',8450000,'Villa 18','V10'),
 (11,1185,920,233,'867.42',6,'6+2',8495000,'Villa 11','V11'),(12,1128,829,223,'774.42',5,'5+2',7950000,'Villa 12','V12'),
 (18,1705,920,233,'863.26',6,'6+2',None,None,None),(14,859,811,211,'768.58',5,'5+2',8495000,'Villa 17','V14'),
 (15,818,822,224,'768.58',5,'5+2',8350000,'Villa 15','V15'),(16,1021,921,233,'869.85',6,'6+2',8950000,'Villa 16','V16')]
villas=[dict(no=a,plot=b,interior=c,terr=d,usable=e,bed=g,bath=h,price=i,file=j,code=k) for a,b,c,d,e,g,h,i,j,k in VIL]
if __name__=='__main__':
    print(len(apartments), sum(1 for a in apartments if a['price']), len(villas), sum(1 for v in villas if v['price']))
    ap=[a for a in apartments if a['price']]; print(min(a['price'] for a in ap),max(a['price'] for a in ap))
    vp=[v for v in villas if v['price']]; print(min(v['price'] for v in vp),max(v['price'] for v in vp))
    # check ext = terrace + porche
    for a in apartments:
        t=float(a['terrace'] or 0)+float(a['porche'] or 0)
        tot=float(a['interior'])+float(a['ext'])+float(a['garden'] or 0)
        if abs(t-float(a['ext']))>0.02 or abs(tot-float(a['total']))>0.02: print('MISMATCH',a['door'],t,a['ext'],tot,a['total'])
