# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
# -*- coding: utf-8 -*-
"""python3 check_tr.py <loc> : checks agents/tr_<loc>*.json against prose.json"""
import json, re, sys, glob
W='/Users/sasanraftari/Downloads/SkyMarbella_work'
loc=sys.argv[1]
prose=json.load(open(f'{W}/prose.json'))
tr={}
for f in sorted(glob.glob(f'{W}/agents/tr_{loc}*.json')): tr.update(json.load(open(f)))
NUM=re.compile(r'\d+(?:[.,   ]\d{3}(?!\d))*(?:[.,]\d+)?')
def nums(s): return sorted(re.sub(r'\D','',m) for m in NUM.findall(s))
BAD=re.compile(r'\bsky\b|rivestia|marlo|palmera|burgos|cabrilla|domus|alborada|\bsotomar\b',re.I)
missing=[k for k in prose if k not in tr]; extra=[k for k in tr if k not in prose]
print(loc,'translated',len(tr),'of',len(prose),'missing',len(missing),'extra',len(extra))
for k in missing[:5]: print('  MISSING',k[:80])
bad=0
for k,v in tr.items():
    if k not in prose: continue
    probs=[]
    if not isinstance(v,str) or not v.strip(): probs.append('empty')
    else:
        if nums(k)!=nums(v): probs.append(f'numbers {nums(k)} vs {nums(v)}')
        if BAD.search(v): probs.append('banned name')
        if k.count('<em>')!=v.count('<em>') or k.count('</em>')!=v.count('</em>'): probs.append('em tags')
        if ('&amp;' in k)!=('&amp;' in v): probs.append('&amp;')
        if re.search(r'[A-Za-z]{3}',v) is None and loc not in ('ru','ar'): probs.append('?')
        if '  ' in v or v!=v.strip(): probs.append('spaces')
        if loc!='ar' and re.search(r'[؀-ۿ]',v): probs.append('arabic letters')
        if loc!='ru' and re.search(r'[Ѐ-ӿ]',v): probs.append('cyrillic letters')
        if 'EUR' in v or re.search(r'\bsqm\b',v): probs.append('EUR/sqm left')
    if probs: bad+=1; print('  PROBLEM',k[:60].replace('\n',' '),'->',v[:60] if isinstance(v,str) else v, probs)
print('problems',bad)
