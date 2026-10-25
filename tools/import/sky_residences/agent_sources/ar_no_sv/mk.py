import json,sys,glob,os,re
W='/Users/sasanraftari/Downloads/SkyMarbella_work'
S=os.path.dirname(os.path.abspath(__file__))
prose=json.load(open(f'{W}/prose.json'))
keys=list(prose.keys())
for loc in ['ar','no','sv']:
    n=0
    for f in sorted(glob.glob(f'{S}/{loc}_*.txt')):
        out={}
        for line in open(f,encoding='utf-8').read().split('\n'):
            if not line.strip(): continue
            i,_,t=line.partition('|')
            out[keys[int(i)]]=t.strip()
        name=os.path.basename(f)[:-4]  # e.g. no_01
        l,num=name.split('_')
        json.dump(out,open(f'{W}/agents/tr_{l}_{num}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        n+=len(out)
    print(loc,n)
