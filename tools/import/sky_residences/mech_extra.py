# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
# -*- coding: utf-8 -*-
"""Mechanical translations for the strings assemble.py cannot build: multi-part unit sizes and prices that carry '+ VAT'.
Word tables copied from assemble.py / SIZE_LABELS in scripts/build_property_pages.mjs."""
import json, re
LOCS=['es','fr','de','ru','ar','nl','pl','no','sv']
GROUP={'es':'.','fr':' ','de':'.','ru':' ','ar':',','nl':'.','pl':' ','no':' ','sv':' '}
DEC={l:('.' if l=='ar' else ',') for l in LOCS}
UNIT={l:'m²' for l in LOCS}; UNIT['ru']='м²'; UNIT['ar']='م²'
FROM={'es':'Desde {}','fr':'À partir de {}','de':'Ab {}','ru':'От {}','ar':'ابتداءً من {}','nl':'Vanaf {}','pl':'Od {}','no':'Fra {}','sv':'Från {}'}
TAX={'es':'IVA','fr':'TVA','de':'MwSt.','ru':'НДС','ar':'ضريبة القيمة المضافة','nl':'btw','pl':'VAT','no':'mva','sv':'moms'}
LAB={
 'built':dict(es='construido',fr='construit',de='bebaut',ru='застройка',ar='مبنية',nl='bebouwd',pl='powierzchnia zabudowy',sv='byggyta',no='bebygd'),
 'usable':dict(es='superficie útil',fr='surface utile',de='Wohnfläche',ru='полезная площадь',ar='مساحة صافية',nl='gebruiksoppervlak',pl='powierzchnia użytkowa',sv='boarea',no='innvendig areal'),
 'terrace':dict(es='terraza',fr='terrasse',de='Terrasse',ru='терраса',ar='تراس',nl='terras',pl='taras',sv='terrass',no='terrasse'),
 'plot':dict(es='parcela',fr='parcelle',de='Grundstück',ru='участок',ar='قطعة أرض',nl='perceel',pl='działka',sv='tomt',no='tomt'),
 'garden':dict(es='jardín',fr='jardin',de='Garten',ru='сад',ar='حديقة',nl='tuin',pl='ogród',sv='trädgård',no='hage')}
def num(s,l): return s.replace(',',GROUP[l]).replace('.',DEC[l])
def money(n,l):
    b=f'{n:,}'.replace(',',GROUP[l]); return f'€ {b}' if l=='nl' else f'{b} €'
def size(src,l):
    out=[]
    for seg in re.split(r',\s+',src):
        m=re.fullmatch(r'([\d.,]+) sqm (built|usable|terrace|plot|garden)',seg.strip()); assert m,seg
        out.append(f'{num(m.group(1),l)} {UNIT[l]} {LAB[m.group(2)][l]}')
    return ', '.join(out)
def mech(src):
    r={}
    if re.fullmatch(r'[\d.,]+ sqm (built|usable|terrace|plot|garden)(, [\d.,]+ sqm (built|usable|terrace|plot|garden))+',src):
        return {l:size(src,l) for l in LOCS}
    m=re.fullmatch(r'From EUR ([\d,]+) \+ VAT',src)
    if m: return {l:FROM[l].format(money(int(m.group(1).replace(',','')),l))+' + '+TAX[l] for l in LOCS}
    m=re.fullmatch(r'EUR ([\d,]+) \+ VAT',src)
    if m: return {l:money(int(m.group(1).replace(',','')),l)+' + '+TAX[l] for l in LOCS}
    m=re.fullmatch(r'EUR ([\d,]+) - EUR ([\d,]+) \+ VAT',src)
    if m: return {l:money(int(m.group(1).replace(',','')),l)+' - '+money(int(m.group(2).replace(',','')),l)+' + '+TAX[l] for l in LOCS}
    return None
if __name__=='__main__':
    todo=json.load(open('todo.json')); tr={}; prose={}
    for en,paths in todo.items():
        got=mech(en)
        if got: tr[en]=got
        else: prose[en]=paths
    json.dump(tr,open('tr_m.json','w'),ensure_ascii=False,indent=1)
    json.dump(prose,open('prose.json','w'),ensure_ascii=False,indent=1)
    print(len(tr),'mechanical;',len(prose),'prose')
