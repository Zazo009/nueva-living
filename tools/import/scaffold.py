import json, collections, sys, re
SP, SLUG = sys.argv[1], sys.argv[2]
tm = json.load(open(f'{SP}/tm.json'))
d = json.load(open(f'content/liora-projects/{SLUG}/project.json'))
sib = json.load(open('content/liora-projects/buenas-noches-terrace-residences/project.json'))
shape = sib['i18n']['es']
sib2 = json.load(open('content/liora-projects/laurel-hill-residences/project.json'))
if 'video' in sib2['i18n']['es'].get('media', {}):
    shape.setdefault('media', {})['video'] = sib2['i18n']['es']['media']['video']
sib3 = json.load(open('content/liora-projects/los-olivos-residences/project.json'))
if 'tour' in sib3['i18n']['es'].get('media', {}):
    shape.setdefault('media', {})['tour'] = sib3['i18n']['es']['media']['tour']
sib4 = json.load(open('content/liora-projects/los-olivos-residences/project.json'))
for key in ('paymentTerms', 'paymentTermsNote'):
    if key in sib4['i18n']['es'].get('constructionTimeline', {}):
        shape.setdefault('constructionTimeline', {})[key] = sib4['i18n']['es']['constructionTimeline'][key]
SKIP = {'src','width','height','category','floorplan','href','desktopSrc','mobileSrc','poster','mobilePoster','url'}
def walk(obj, model, path=''):
    out = []
    if isinstance(model, dict) and isinstance(obj, dict):
        for k in obj:
            if k in SKIP or k not in model: continue
            out += walk(obj[k], model[k], f'{path}.{k}')
    elif isinstance(model, list) and isinstance(obj, list):
        proto = model[0] if model else ''
        for i, v in enumerate(obj): out += walk(v, proto, f'{path}[{i}]')
    elif isinstance(obj, str): out.append((path, obj))
    return out
pairs = []
for k in d:
    if k in shape: pairs += walk(d[k], shape[k], f'.{k}')
uniq = collections.OrderedDict()
for path, v in pairs: uniq.setdefault(v, []).append(path)
MECH = [r'From EUR [\d,]+', r'EUR [\d,]+ - EUR [\d,]+', r'EUR [\d,]+',
        r'[\d,.]+ - [\d,.]+ sqm built', r'[\d,.]+ - [\d,.]+ sqm', r'[\d,.]+ sqm built',
        r'[\d,.]+ - [\d,.]+ sqm interior', r'[\d,.]+ sqm interior',
        r'\d+ of \d+ available', r'\d+ of \d+ homes available', r'\d+ of \d+ villas available',
        r'\d+ available', r'\d+ bedrooms', r'\d+-\d+ bedrooms',
        r'Villa [\d.]+', r'Apartment \d+',
        # Kept in step with mech() in assemble.py. These two lists are the same
        # value in two places: anything assemble can build mechanically must be
        # listed here too, or scaffold reports it as needing a translation that
        # assemble will then overwrite.
        r'Portal \d+ - \d[A-F]',
        # A unit code that leads with its block: 22A, 30B, 40C. Numbering is
        # the developer's own and reads the same in every language.
        r'\d{2,3}[A-Z]',
        # "Block 2, portal 3, first floor C": the renderer rewrites these from
        # FLOOR_PREFIXES and FLOOR_PARTS, so they stay English in the JSON.
        r'Block \d+, portal \d+, (?:ground|first|second|third|fourth) floor [A-Z]',
        r'\d{1,4}(\.\d{1,3})?',
        r'[A-Z]{1,4}-?\d{1,4}[A-Z]?', r'\d{1,3}(\.\d)?%', r'\d{1,3}(\.\d)?% \+ VAT',
        # A bare area, such as a plot figure: only the unit changes per language.
        r'[\d,.]+ sqm']
todo = [v for v in uniq if not (v in tm and len(tm[v]) == 9)
        and not any(re.fullmatch(m, v) for m in MECH)]
print('strings', len(pairs), 'unique', len(uniq), 'need translation', len(todo))
json.dump({v: uniq[v] for v in todo}, open(f'{SP}/todo.json','w'), ensure_ascii=False, indent=1)
for i, v in enumerate(todo): print(f'{i:3d} [{uniq[v][0]}] {v}')
