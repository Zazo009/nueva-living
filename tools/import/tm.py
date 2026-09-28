import json, glob, collections, sys
LOCS = ['es','fr','de','ru','ar','nl','pl','no','sv']
def flatten(o, p=''):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'i18n': continue
            out.update(flatten(v, f'{p}.{k}'))
    elif isinstance(o, list):
        for i, v in enumerate(o): out.update(flatten(v, f'{p}[{i}]'))
    elif isinstance(o, str): out[p] = o
    return out
counts = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for path in glob.glob('content/liora-projects/*/project.json'):
    d = json.load(open(path)); en = flatten(d)
    for loc in LOCS:
        if loc not in d.get('i18n', {}): continue
        for k, v in flatten(d['i18n'][loc]).items():
            # media gallery categories are keys that stay English on purpose
            if k.endswith('.category'): continue
            if k in en and en[k] and v: counts[en[k]][loc][v] += 1
out = {e: {loc: c.most_common(1)[0][0] for loc, c in per.items()} for e, per in counts.items()}
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False)
print('TM entries', len(out))
