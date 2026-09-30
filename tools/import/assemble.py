import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# -*- coding: utf-8 -*-
import json, re, glob, collections, sys
from overlay_shape import overlay_shape
SP, SLUG = sys.argv[1], sys.argv[2]
LOCS = ['es','fr','de','ru','ar','nl','pl','no','sv']
tm = json.load(open(f'{SP}/tm.json'))
manual = {}
for f in sorted(glob.glob(f'{SP}/tr_[a-z].json')): manual.update(json.load(open(f)))
print('manual entries', len(manual))

GROUP = {'es':'.','fr':' ','de':'.','ru':' ','ar':',','nl':'.','pl':' ','no':' ','sv':' '}
DEC = {l: ('.' if l=='ar' else ',') for l in LOCS}
FROM = {'es':'Desde {}','fr':'À partir de {}','de':'Ab {}','ru':'От {}','ar':'ابتداءً من {}',
        'nl':'Vanaf {}','pl':'Od {}','no':'Fra {}','sv':'Från {}'}
SQM = {'es':'m²','fr':'m²','de':'m²','ru':'м²','ar':'م²','nl':'m²','pl':'m²','no':'m²','sv':'m²'}
BUILT = {'es':'m² construido','fr':'m² construit','de':'m² bebaut','ru':'м² застройка','ar':'م² مبنية',
         'nl':'m² bebouwd','pl':'m² powierzchnia zabudowy','no':'m² bruksareal','sv':'m² byggyta'}
INTERIOR = {'es':'m² interior','fr':'m² intérieur','de':'m² Innenfläche','ru':'м² внутренняя площадь',
            'ar':'م² داخلية','nl':'m² binnenoppervlak','pl':'m² powierzchni wewnętrznej',
            'no':'m² innvendig','sv':'m² invändigt'}
BEDS = {'es':'dormitorios','fr':'chambres','de':'Schlafzimmer','ru':'спальни','ar':'غرف نوم',
        'nl':'slaapkamers','pl':'sypialnie','no':'soverom','sv':'sovrum'}
AVAIL = {'es':'disponibles','fr':'disponibles','de':'verfügbar','ru':'доступно','ar':'متاح',
         'nl':'beschikbaar','pl':'dostępnych','no':'tilgjengelige','sv':'tillgängliga'}
AVAILOF = {'es':'{} de {} disponibles','fr':'{} disponibles sur {}','de':'{} von {} verfügbar',
           'ru':'{} из {} доступно','ar':'{} من {} متاحة','nl':'{} van de {} beschikbaar',
           'pl':'{} z {} dostępnych','no':'{} av {} ledige','sv':'{} av {} lediga'}
AVAILOF_HOMES = {'es':'{} de {} viviendas disponibles','fr':'{} logements disponibles sur {}',
  'de':'{} von {} Wohnungen verfügbar','ru':'{} из {} квартир доступно','ar':'{} من {} مسكناً متاحاً',
  'nl':'{} van de {} woningen beschikbaar','pl':'{} z {} mieszkań dostępnych',
  'no':'{} av {} boliger ledige','sv':'{} av {} bostäder lediga'}
AVAILOF_VILLAS = {'es':'{} de {} villas disponibles','fr':'{} villas disponibles sur {}',
  'de':'{} von {} Villen verfügbar','ru':'{} из {} вилл доступно','ar':'{} من {} فيلا متاحة',
  'nl':'{} van de {} villa’s beschikbaar','pl':'{} z {} willi dostępnych',
  'no':'{} av {} villaer ledige','sv':'{} av {} villor lediga'}
VILLA = {'es':'Villa','fr':'Villa','de':'Villa','ru':'Вилла','ar':'فيلا','nl':'Villa','pl':'Willa','no':'Villa','sv':'Villa'}
APT = {'es':'Apartamento','fr':'Appartement','de':'Wohnung','ru':'Квартира','ar':'شقة',
       'nl':'Appartement','pl':'Mieszkanie','no':'Leilighet','sv':'Lägenhet'}
# A Spanish block entrance. The developer numbers its six of them, and the unit
# reference is that number plus the door -- "Portal 4 - 2C". Only the noun is
# translated; the numbering is the developer's own and stays as printed.
PORTAL = {'es':'Portal','fr':'Cage','de':'Aufgang','ru':'Подъезд','ar':'مدخل',
          'nl':'Portiek','pl':'Klatka','no':'Oppgang','sv':'Port'}

def money(n, loc):
    body = f'{n:,}'.replace(',', GROUP[loc])
    return f'€ {body}' if loc == 'nl' else f'{body} €'
def num(s, loc):
    return s.replace(',', GROUP[loc]).replace('.', DEC[loc])

def mech(src, loc):
    m = re.fullmatch(r'From EUR ([\d,]+)', src)
    if m: return FROM[loc].format(money(int(m.group(1).replace(',','')), loc))
    m = re.fullmatch(r'EUR ([\d,]+) - EUR ([\d,]+)', src)
    if m: return f"{money(int(m.group(1).replace(',','')),loc)} - {money(int(m.group(2).replace(',','')),loc)}"
    m = re.fullmatch(r'EUR ([\d,]+)', src)
    if m: return money(int(m.group(1).replace(',','')), loc)
    m = re.fullmatch(r'([\d,.]+) - ([\d,.]+) sqm built', src)
    if m: return f'{num(m.group(1),loc)} - {num(m.group(2),loc)} {BUILT[loc]}'
    m = re.fullmatch(r'([\d,.]+) - ([\d,.]+) sqm interior', src)
    if m: return f'{num(m.group(1),loc)} - {num(m.group(2),loc)} {INTERIOR[loc]}'
    m = re.fullmatch(r'([\d,.]+) - ([\d,.]+) sqm', src)
    if m: return f'{num(m.group(1),loc)} - {num(m.group(2),loc)} {SQM[loc]}'
    m = re.fullmatch(r'([\d,.]+) sqm built', src)
    if m: return f'{num(m.group(1),loc)} {BUILT[loc]}'
    m = re.fullmatch(r'([\d,.]+) sqm interior', src)
    if m: return f'{num(m.group(1),loc)} {INTERIOR[loc]}'
    m = re.fullmatch(r'(\d+) bedrooms', src)
    if m: return f'{m.group(1)} {BEDS[loc]}'
    m = re.fullmatch(r'(\d+)-(\d+) bedrooms', src)
    if m: return f'{m.group(1)}-{m.group(2)} {BEDS[loc]}'
    m = re.fullmatch(r'(\d+) of (\d+) available', src)
    if m: return AVAILOF[loc].format(m.group(1), m.group(2))
    m = re.fullmatch(r'(\d+) of (\d+) homes available', src)
    if m: return AVAILOF_HOMES[loc].format(m.group(1), m.group(2))
    m = re.fullmatch(r'(\d+) of (\d+) villas available', src)
    if m: return AVAILOF_VILLAS[loc].format(m.group(1), m.group(2))
    m = re.fullmatch(r'(\d+) available', src)
    if m: return f'{m.group(1)} {AVAIL[loc]}'
    if re.fullmatch(r'\d{1,4}(\.\d{1,3})?', src): return src
    # A developer's own unit code (OV-3, PN-B1) is an identifier, not words.
    if re.fullmatch(r'[A-Z]{1,4}-?\d{1,4}[A-Z]?', src): return src
    if re.fullmatch(r'\d{1,3}(\.\d)?%', src): return src
    # A bare area, such as a plot figure: the number keeps the locale's
    # separators and only the unit changes.
    m = re.fullmatch(r'([\d,.]+) sqm', src)
    if m: return f'{num(m.group(1),loc)} {SQM[loc]}'
    m = re.fullmatch(r'(\d{1,3}(?:\.\d)?%) \+ VAT', src)
    if m: return f'{m.group(1)} + {TAX[loc]}'
    # Unit references stay in English: localizedUnitFloor() rewrites them at
    # render time from FLOOR_PREFIXES and FLOOR_PARTS.
    m = re.fullmatch(r'Villa ([\d.]+)', src)
    if m: return f'{VILLA[loc]} {m.group(1)}'
    m = re.fullmatch(r'Apartment (\d+)', src)
    if m: return f'{APT[loc]} {m.group(1)}'
    # A unit code that leads with its block -- 22A, 30B, 40C. Kept as printed:
    # the numbering is the developer's own, not words.
    if re.fullmatch(r'\d{2,3}[A-Z]', src): return src
    # Anchored to this exact shape so it cannot reach another project's strings.
    m = re.fullmatch(r'Portal (\d+) - (\d[A-F])', src)
    if m: return f'{PORTAL[loc]} {m.group(1)} - {m.group(2)}'
    # "Block 2, portal 3, first floor C". Passed through unchanged, like every
    # other unit reference: localizedUnitFloor() rewrites it at render time.
    if re.fullmatch(r'Block \d+, portal \d+, (?:ground|first|second|third|fourth) floor [A-Z]', src):
        return src
    return None


FLOORS = json.load(open(f'{SP}/floor_parts.json'))
def floor_label(src, loc):
    """Block 2, Penthouse -> the same label in `loc`, part by part."""
    out = []
    for seg in [s.strip() for s in re.split(r',|&', src) if s.strip()]:
        low = seg.lower()
        if low in FLOORS['parts']:
            val = FLOORS['parts'][low][loc]
            # FLOOR_PARTS stores standalone labels, so each is capitalised.
            # Only the first segment still starts the phrase; German
            # capitalises nouns anywhere and Arabic is caseless.
            if out and loc not in ('de', 'ar') and not re.match(r'(Sky|Premium|Deluxe|Superior)\b', val):
                val = val[0].lower() + val[1:]
            out.append(val); continue
        m = re.fullmatch(r'([A-Za-z]+)\s+(\S+)', seg)
        if m and m.group(1).lower() in FLOORS['prefixes']:
            out.append(f"{FLOORS['prefixes'][m.group(1).lower()][loc]} {m.group(2)}"); continue
        return None
    return ', '.join(out)

TAX = {'es':'IVA','fr':'TVA','de':'MwSt.','ru':'НДС','ar':'ضريبة القيمة المضافة',
       'nl':'btw','pl':'VAT','no':'mva','sv':'moms'}

misses = collections.Counter()
def tr(src, loc):
    if not isinstance(src, str) or not src.strip(): return src
    if src in manual and loc in manual[src]: return manual[src][loc]
    got = mech(src, loc)
    if got is not None: return got
    got = floor_label(src, loc)
    if got is not None: return got
    if src in tm and loc in tm[src]: return tm[src][loc]
    misses[src] += 1
    return None

# The shape is the union of every published overlay, not one sibling's.
# See tools/import/overlay_shape.py for what that fixes.
shape = overlay_shape()
d = json.load(open(f'content/liora-projects/{SLUG}/project.json'))
STRUCT = {'href','floorplan','milestone','icon'}
def build(node, model, loc):
    if isinstance(model, dict) and isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k in STRUCT or k not in model: continue
            if k in ('src','width','height','category','desktopSrc','mobileSrc','poster','mobilePoster','url'):
                out[k] = v; continue
            got = build(v, model[k], loc)
            if got is not None: out[k] = got
        return out or None
    if isinstance(model, list) and isinstance(node, list):
        proto = model[0] if model else ''
        out = [build(i, proto, loc) for i in node]
        return out if all(v is not None for v in out) else None
    return tr(node, loc)

i18n = {}
for loc in LOCS:
    built = {}
    for k, v in d.items():
        if k not in shape: continue
        got = build(v, shape[k], loc)
        if got is not None: built[k] = got
    i18n[loc] = built

if misses:
    print('UNTRANSLATED', len(misses))
    for s in list(misses)[:20]: print('  ', repr(s[:110]))
else:
    d['i18n'] = i18n
    json.dump(d, open(f'content/liora-projects/{SLUG}/project.json','w'), ensure_ascii=False, indent=2)
    print('wrote overlays for', ', '.join(LOCS))
