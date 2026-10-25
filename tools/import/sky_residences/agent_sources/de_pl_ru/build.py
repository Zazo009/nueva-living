import json,sys,glob,re
W='/Users/sasanraftari/Downloads/SkyMarbella_work'
loc=sys.argv[1]
keys=list(json.load(open(f'{W}/prose.json')))
tr={}
for f in sorted(glob.glob(f'{W}/agents/_src/{loc}_*.txt')):
    for ln in open(f,encoding='utf-8').read().split('\n'):
        if not ln.strip(): continue
        m=re.match(r'(\d+)\|(.*)$',ln)
        assert m,ln[:50]
        i=int(m.group(1)); assert i not in tr,('dup',i)
        tr[i]=m.group(2)
miss=[i for i in range(len(keys)) if i not in tr and keys[i]!='']
print(loc,'have',len(tr),'missing',miss)
for f in glob.glob(f'{W}/agents/tr_{loc}_*.json'):
    import os; os.remove(f)
N=56
idx=[i for i in range(len(keys)) if i in tr or keys[i]=='']
for n in range(0,len(keys),N):
    chunk={}
    for i in range(n,min(n+N,len(keys))):
        if i in tr: chunk[keys[i]]=tr[i]
        elif keys[i]=='': chunk[keys[i]]=''
    if chunk:
        json.dump(chunk,open(f'{W}/agents/tr_{loc}_{n//N+1:02d}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
