import json
W='/Users/sasanraftari/Downloads/SkyMarbella_work'
prose=json.load(open(f'{W}/prose.json'))
KEYS=list(prose.keys())
def emit(n, entries):
    out={'es':{},'fr':{},'nl':{}}
    for e in entries:
        idx,es,fr,nl=e
        k=KEYS[idx]
        out['es'][k]=es; out['fr'][k]=fr; out['nl'][k]=nl
    for l in out:
        json.dump(out[l],open(f'{W}/agents/tr_{l}_{n:02d}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('chunk',n,len(entries),'entries; idx',entries[0][0],'-',entries[-1][0])
