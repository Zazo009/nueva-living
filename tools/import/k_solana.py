# -*- coding: utf-8 -*-
"""Solana Residences: the 158 strings the translation memory did not have.

Same shape as k_higueron.py. Tokens expand per language:  {E1254700} (money)  {N46.47}  {U} (m2).
The unit-specific sentences (plan captions, room lists, terrace lists, size lines) are built from
per-language parts below instead of being typed 40 times. Run:
    python3 tools/import/k_solana.py <scratch dir>        (reads <dir>/todo.json, writes <dir>/tr_a.json)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {'es': 'm²', 'fr': 'm²', 'de': 'm²', 'ru': 'м²', 'ar': 'م²', 'nl': 'm²', 'pl': 'm²', 'no': 'm²', 'sv': 'm²'}
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


PL8 = {
 'Bedroom with a double bed and a sliding glass door to a terrace with a sea view': "Sypialnia z łóżkiem dwuosobowym i przesuwnymi szklanymi drzwiami na taras z widokiem na morze",
 'The pool and the sea': 'Basen i morze',
 'The terraced block above the pool': 'Tarasowy budynek nad basenem',
 'Aerial view straight down on the outdoor pool': 'Widok z lotu ptaka prosto z góry na basen zewnętrzny, jego schody i taras basenowy z leżakami',
 'The outdoor pool from above': 'Basen zewnętrzny z góry',
 'Covered terrace with a sofa and armchairs': 'Zadaszony taras z sofą i fotelami oraz widokiem ponad dachami na morze',
 'A covered terrace with a sea view': 'Zadaszony taras z widokiem na morze',
 'Terrace with an outdoor kitchen and a built-in barbecue': 'Taras z kuchnią zewnętrzną i wbudowanym grillem oraz przesuwnymi szklanymi drzwiami do mieszkania',
 'Terrace with an outdoor kitchen': 'Taras z kuchnią zewnętrzną',
 'Terrace with a raised plunge pool and wide steps beside it': 'Taras z podwyższonym małym basenem i szerokimi schodami obok',
 'Terrace with a raised plunge pool': 'Taras z podwyższonym małym basenem',
 'Living and dining room with a sea view': 'Salon z jadalnią z widokiem na morze',
 'Dining table, kitchen island and living area in an open-plan room': 'Stół jadalny, wyspa kuchenna i część wypoczynkowa we wnętrzu o otwartym układzie',
 'Dining table and kitchen island': 'Stół jadalny i wyspa kuchenna',
 'Living room with a sofa, a television': 'Salon z sofą i telewizorem, a w głębi jadalnia i kuchnia',
 'Fitted kitchen with a tall unit holding an oven': 'Kuchnia z zabudową: wysoka szafa z piekarnikiem i kuchenką mikrofalową oraz blat ze zlewem',
 'Bedroom with a double bed and a sliding glass door onto a terrace and the sea': 'Sypialnia z łóżkiem dwuosobowym i przesuwnymi szklanymi drzwiami na taras i morze',
 'Bathroom with a walk-in shower, a wall-hung toilet': 'Łazienka z prysznicem bez brodzika, wiszącą toaletą i wiszącą szafką z umywalką i lustrem',
 'Indoor pool with a sauna behind a glass wall': 'Basen wewnętrzny z sauną za szklaną ścianą i sprzętem do ćwiczeń w głębi',
 'The indoor pool': 'Basen wewnętrzny',
 'Gym with a rack of dumbbells': 'Siłownia ze stojakiem na hantle, ławką i wyciągiem linowym oraz ścianą luster',
 'The gym': 'Siłownia',
 'Gym with a treadmill and a cross trainer': 'Siłownia z bieżnią i orbitrekiem oraz basenem wewnętrznym za szklaną ścianą',
 'Gym and indoor pool': 'Siłownia i basen wewnętrzny',
 'Shared room with a long marble table': 'Pomieszczenie wspólne z długim marmurowym stołem, krzesłami i fotelami oraz oknem na ogród',
 'A shared room with a long table': 'Pomieszczenie wspólne z długim stołem',
 'Meeting room with a long wooden table': 'Sala spotkań z długim drewnianym stołem, skórzanymi krzesłami i dwiema lampami wiszącymi',
 'A meeting room': 'Sala spotkań',
}

PL8.update({
 'Why check the details': 'Dlaczego sprawdzać szczegóły', 'Views': 'Widoki', 'Social room and gardens': 'Sala towarzyska i ogrody',
 'Beaches and golf': 'Plaże i golf', 'Prices': 'Ceny', 'Furniture and decoration': 'Meble i dekoracje',
 'Reservation and guarantee': 'Rezerwacja i gwarancja', 'Completion and certificates': 'Ukończenie i certyfikaty',
 'Two terrace areas': 'Dwie powierzchnie tarasów', 'Which area counts': 'Która powierzchnia się liczy', 'The private pools': 'Prywatne baseny',
})

SV8 = {'Views': 'Utsikt', 'Social room and gardens': 'Gemensamt rum och trädgårdar', 'Beaches and golf': 'Stränder och golf', 'Prices': 'Priser',
       'Furniture and decoration': 'Möbler och dekor', 'Reservation and guarantee': 'Reservation och garanti',
       'Completion and certificates': 'Färdigställande och certifikat', 'Two terrace areas': 'Två terrassytor',
       'Which area counts': 'Vilken yta som gäller', 'The private pools': 'De privata poolerna'}


def a(hint, *tr):
    hits = [i for i, s in enumerate(todo) if s == hint] or [i for i, s in enumerate(todo) if s.startswith(hint)]
    if not hits:
        print('NOT IN TODO (tm has it)', hint[:60]); return
    if len(tr) == 8 and hint in SV8:   # short labels written without the Swedish line
        tr = tr + (SV8[hint],)
    if len(tr) == 8:   # a Polish line was left out: take it from PL8, keyed by the hint
        if hint not in PL8:
            print('NEED PL', hint[:60]); return
        tr = tr[:6] + (PL8[hint],) + tr[6:]
    assert len(hits) == 1, (hint, len(hits))
    if len(tr) != 9:
        print('BAD ARGS', len(tr), hint[:70]); return
    T[todo[hits[0]]] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ------------------------------------------------------------------ per-unit templates
AND = dict(zip(LOCS, ['y', 'et', 'und', 'и', 'و', 'en', 'i', 'og', 'och']))
def lst(nums, l):
    ns = [f'{{N{n}}}' for n in nums]
    sep = '،' if l == 'ar' else ','
    if len(ns) == 1: return ns[0]
    if len(ns) == 2: return f'{ns[0]} {AND[l]}{"" if l == "ar" else " "}{ns[1]}'
    return f'{ns[0]}{sep} {ns[1]} {AND[l]}{"" if l == "ar" else " "}{ns[2]}'

BLK = dict(zip(LOCS, ['Bloque', 'Bloc', 'Block', 'Блок', 'مبنى', 'Blok', 'Blok', 'Hus', 'Hus']))
# floor labels as FLOOR_PARTS writes them, lower-case for mid-sentence use (de and ar as is)
LV = {
 'ground':  dict(zip(LOCS, ['planta baja', 'rez-de-chaussée', 'Erdgeschoss', 'первый этаж', 'الطابق الأرضي', 'begane grond', 'parter', 'første etasje', 'bottenvåning'])),
 'first':   dict(zip(LOCS, ['primera planta', 'premier étage', 'erstes Obergeschoss', 'второй этаж', 'الطابق الأول', 'eerste verdieping', 'pierwsze piętro', 'andre etasje', 'första våningen'])),
 'second':  dict(zip(LOCS, ['segunda planta', 'deuxième étage', 'zweites Obergeschoss', 'третий этаж', 'الطابق الثاني', 'tweede verdieping', 'drugie piętro', 'tredje etasje', 'andra våningen'])),
 'pent':    dict(zip(LOCS, ['ático de la cuarta planta', 'penthouse du quatrième étage', 'Penthouse im vierten Obergeschoss', 'пентхаус на пятом этаже', 'بنتهاوس في الطابق الرابع', 'penthouse op de vierde verdieping', 'penthouse na czwartym piętrze', 'toppleilighet i femte etasje', 'takvåning på fjärde våningen'])),
}
def cap(s, l):   # sentence-initial capital (not for Arabic)
    return s if l == 'ar' else s[0].upper() + s[1:]
FP = dict(zip(LOCS, ['Plano de la vivienda', 'Plan du logement', 'Grundriss der Wohnung', 'Планировка квартиры', 'مخطط المسكن', 'Plattegrond van woning', 'Rzut lokalu', 'Plantegning av bolig', 'Planritning för bostad']))
HM = dict(zip(LOCS, ['Vivienda', 'Logement', 'Wohnung', 'Квартира', 'المسكن', 'Woning', 'Lokal', 'Bolig', 'Bostad']))
KEY = {'ground floor': 'ground', 'first floor': 'first', 'second floor': 'second', 'fourth floor penthouse': 'pent'}

LIVING = {
 'es': 'Salón-comedor-cocina de {L} {U}, {NB} de {LST} {U} y dos baños de {B1} y {B2} {U}.',
 'fr': 'Séjour avec salle à manger et cuisine de {L} {U}, {NB} de {LST} {U} et deux salles de bains de {B1} et {B2} {U}.',
 'de': 'Wohn-, Ess- und Kochbereich mit {L} {U}, {NB} mit {LST} {U} und zwei Bäder mit {B1} und {B2} {U}.',
 'ru': 'Гостиная, столовая и кухня {L} {U}, {NB} площадью {LST} {U} и две ванные комнаты площадью {B1} и {B2} {U}.',
 'ar': 'تضم منطقة معيشة وطعام ومطبخ بمساحة {L} {U}، و{NB} بمساحة {LST} {U}، وحمامين بمساحة {B1} و{B2} {U}.',
 'nl': 'Woon-, eet- en keukengedeelte van {L} {U}, {NB} van {LST} {U} en twee badkamers van {B1} en {B2} {U}.',
 'pl': 'Salon z jadalnią i kuchnią o powierzchni {L} {U}, {NB} o powierzchni {LST} {U} oraz dwie łazienki o powierzchni {B1} i {B2} {U}.',
 'no': 'Stue, spiseplass og kjøkken på {L} {U}, {NB} på {LST} {U} og to bad på {B1} og {B2} {U}.',
 'sv': 'Vardagsrum, matplats och kök på {L} {U}, {NB} på {LST} {U} och två badrum på {B1} och {B2} {U}.',
}
BEDS = {  # 3 / 2 bedrooms
 3: dict(zip(LOCS, ['tres dormitorios', 'trois chambres', 'drei Schlafzimmer', 'три спальни', 'ثلاث غرف نوم', 'drie slaapkamers', 'trzy sypialnie', 'tre soverom', 'tre sovrum'])),
 2: dict(zip(LOCS, ['dos dormitorios', 'deux chambres', 'zwei Schlafzimmer', 'две спальни', 'غرفتي نوم', 'twee slaapkamers', 'dwie sypialnie', 'to soverom', 'två sovrum'])),
}
TER_A = {  # base: one covered + one uncovered terrace
 'es': 'Una terraza cubierta de {C} {U} y una terraza descubierta de {D} {U}',
 'fr': 'Une terrasse couverte de {C} {U} et une terrasse découverte de {D} {U}',
 'de': 'Eine überdachte Terrasse von {C} {U} und eine offene Terrasse von {D} {U}',
 'ru': 'Крытая терраса {C} {U} и открытая терраса {D} {U}',
 'ar': 'تراس مسقوف بمساحة {C} {U} وتراس مكشوف بمساحة {D} {U}',
 'nl': 'Een overdekt terras van {C} {U} en een open terras van {D} {U}',
 'pl': 'Taras zadaszony o powierzchni {C} {U} i taras odkryty o powierzchni {D} {U}',
 'no': 'En overbygd terrasse på {C} {U} og en åpen terrasse på {D} {U}',
 'sv': 'En övertäckt terrass på {C} {U} och en öppen terrass på {D} {U}',
}
TER_B = {  # one covered + two uncovered
 'es': 'Una terraza cubierta de {C} {U} y terrazas descubiertas de {D} y {E} {U}',
 'fr': 'Une terrasse couverte de {C} {U} et des terrasses découvertes de {D} et {E} {U}',
 'de': 'Eine überdachte Terrasse von {C} {U} und offene Terrassen von {D} und {E} {U}',
 'ru': 'Крытая терраса {C} {U} и открытые террасы {D} и {E} {U}',
 'ar': 'تراس مسقوف بمساحة {C} {U} وتراسان مكشوفان بمساحة {D} و{E} {U}',
 'nl': 'Een overdekt terras van {C} {U} en open terrassen van {D} en {E} {U}',
 'pl': 'Taras zadaszony o powierzchni {C} {U} i tarasy odkryte o powierzchni {D} i {E} {U}',
 'no': 'En overbygd terrasse på {C} {U} og åpne terrasser på {D} og {E} {U}',
 'sv': 'En övertäckt terrass på {C} {U} och öppna terrasser på {D} och {E} {U}',
}
SUMC = {
 'es': ', que suman {S} {U}', 'fr': ', soit {S} {U} au total', 'de': ', zusammen {S} {U}', 'ru': ', в сумме {S} {U}',
 'ar': '، أي ما مجموعه {S} {U}', 'nl': ', samen {S} {U}', 'pl': ', razem {S} {U}', 'no': ', til sammen {S} {U}', 'sv': ', tillsammans {S} {U}'}
POOLC = {
 'es': ', con una piscina privada dibujada en el plano', 'fr': ', avec une piscine privée dessinée sur le plan',
 'de': ', mit einem im Grundriss eingezeichneten privaten Pool', 'ru': ', с частным бассейном, показанным на плане',
 'ar': '، مع مسبح خاص مرسوم في المخطط', 'nl': ', met een privézwembad op de plattegrond',
 'pl': ', z prywatnym basenem zaznaczonym na rzucie', 'no': ', med et privat basseng tegnet inn på plantegningen',
 'sv': ', med en privat pool inritad på planritningen'}
PRICEC = {
 'es': '; la lista de precios indica {P} {U}', 'fr': '; la liste de prix indique {P} {U}', 'de': '; die Preisliste nennt {P} {U}',
 'ru': '; в прайс-листе указано {P} {U}', 'ar': '؛ وتذكر قائمة الأسعار {P} {U}', 'nl': '; de prijslijst noemt {P} {U}',
 'pl': '; cennik podaje {P} {U}', 'no': '; prislisten oppgir {P} {U}', 'sv': '; prislistan anger {P} {U}'}
SIZE = {
 'es': '{B} {U} construidos, {I} {U} interiores, {T} {U} de terraza',
 'fr': '{B} {U} construits, {I} {U} intérieurs, {T} {U} de terrasse',
 'de': '{B} {U} bebaut, {I} {U} Innenfläche, {T} {U} Terrasse',
 'ru': '{B} {U} застроенной площади, {I} {U} внутри, терраса {T} {U}',
 'ar': '{B} {U} مبنية، {I} {U} داخلية، {T} {U} تراس',
 'nl': '{B} {U} bebouwd, {I} {U} binnen, {T} {U} terras',
 'pl': '{B} {U} zabudowy, {I} {U} wnętrza, {T} {U} tarasu',
 'no': '{B} {U} bygd, {I} {U} innvendig, {T} {U} terrasse',
 'sv': '{B} {U} byggyta, {I} {U} inomhus, {T} {U} terrass'}


def fill(t, **kw):
    for k, v in kw.items(): t = t.replace('{' + k + '}', str(v))
    return t


for en in todo:
    m = re.fullmatch(r'(Floorplan of home|Home) (\w+), (ground floor|first floor|second floor|fourth floor penthouse), Block (\d)', en)
    if m:
        kind, ref, lv, b = m.groups()
        T[en] = {l: (f'{FP[l]} {ref}' if kind.startswith('Floorplan') else f'{HM[l]} {ref}') + (f'، {LV[KEY[lv]][l]}، {BLK[l]} {b}' if l == 'ar' else f', {LV[KEY[lv]][l]}, {BLK[l]} {b}') for l in LOCS}
        continue
    m = re.fullmatch(r'Home (\w+)', en)
    if m:
        T[en] = {l: f'{HM[l]} {m.group(1)}' for l in LOCS}
        continue
    m = re.fullmatch(r'(Ground floor|First floor|Second floor|Fourth floor penthouse), Block (\d)\. Living, dining and kitchen area of ([\d.]+) sqm, (three|two) bedrooms of ([\d., and]+) sqm and two bathrooms of ([\d.]+) and ([\d.]+) sqm\.', en)
    if m:
        lv, b, L, nb, beds, b1, b2 = m.groups()
        beds = re.findall(r'\d+\.\d+', beds)
        out = {}
        for l in LOCS:
            head = f'{cap(LV[KEY[lv.lower()]][l], l)}{"،" if l == "ar" else ","} {BLK[l]} {b}. '
            out[l] = expand(head + fill(LIVING[l], L='{N%s}' % L, NB=BEDS[3 if nb == 'three' else 2][l], LST=lst(beds, l), B1='{N%s}' % b1, B2='{N%s}' % b2), l)
        T[en] = out
        continue
    m = re.fullmatch(r'A covered terrace of ([\d.]+) sqm and (an uncovered terrace of ([\d.]+) sqm|uncovered terraces of ([\d.]+) and ([\d.]+) sqm)(, which add up to ([\d.]+) sqm)?(, with a private pool drawn on the plan)?(; the price list gives ([\d.]+) sqm)?\.', en)
    if m:
        C, _, D1, D2, E2, _s, S, pool, _p, P = m.groups()
        out = {}
        for l in LOCS:
            w = lambda v: '{N%s}' % v
            s = fill(TER_A[l], C=w(C), D=w(D1)) if D1 else fill(TER_B[l], C=w(C), D=w(D2), E=w(E2))
            if S: s += fill(SUMC[l], S=w(S))
            if pool: s += POOLC[l]
            if P: s += fill(PRICEC[l], P=w(P))
            out[l] = expand(s + '.', l)
        T[en] = out
        continue
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm interior, ([\d.]+) sqm terrace', en)
    if m:
        B, I, Tt = m.groups()
        T[en] = {l: expand(fill(SIZE[l], B='{N%s}' % B, I='{N%s}' % I, T='{N%s}' % Tt), l) for l in LOCS}
        continue

# ------------------------------------------------------------------ names, card, hero
a('Solana Residences', *(['Solana Residences'] * 9))
a('Solana', *(['Solana'] * 9))
a('Solana <em>', *(['Solana <em>Residences</em>'] * 9))
a('Eight finished apartments and penthouses with two or three bedrooms, large terraces and sea views at El Higuerón, between',
  "Ocho apartamentos y áticos terminados de dos o tres dormitorios, con grandes terrazas y vistas al mar, en El Higuerón, entre Fuengirola y Benalmádena, con piscina exterior, piscina interior climatizada, gimnasio y espacio de coworking. Terminados y listos para entrar a vivir, desde {E645000}.",
  "Huit appartements et penthouses achevés de deux ou trois chambres, avec de grandes terrasses et vue sur la mer, à El Higuerón, entre Fuengirola et Benalmádena, avec une piscine extérieure, une piscine intérieure chauffée, une salle de sport et un espace de coworking. Achevés et prêts à habiter, à partir de {E645000}.",
  "Acht fertiggestellte Wohnungen und Penthouses mit zwei oder drei Schlafzimmern, großen Terrassen und Meerblick in El Higuerón zwischen Fuengirola und Benalmádena, mit Außenpool, beheiztem Innenpool, Fitnessraum und Coworking-Bereich. Fertiggestellt und bezugsfertig, ab {E645000}.",
  "Восемь готовых квартир и пентхаусов с двумя или тремя спальнями, большими террасами и видом на море в Эль-Игероне, между Фуэнхиролой и Бенальмаденой, с открытым бассейном, крытым подогреваемым бассейном, тренажёрным залом и коворкингом. Построены и готовы к заселению, от {E645000}.",
  "ثماني شقق وبنتهاوس جاهزة من غرفتي نوم أو ثلاث غرف، بتراسات واسعة وإطلالات على البحر، في إل إيغيرون بين فوينخيرولا وبينالمادينا، مع مسبح خارجي ومسبح داخلي مُدفّأ وصالة رياضية ومساحة عمل مشتركة. مكتملة البناء وجاهزة للسكن، ابتداءً من {E645000}.",
  "Acht afgeronde appartementen en penthouses met twee of drie slaapkamers, grote terrassen en zeezicht in El Higuerón, tussen Fuengirola en Benalmádena, met een buitenzwembad, een verwarmd binnenzwembad, een gym en een coworkingruimte. Opgeleverd en klaar om in te trekken, vanaf {E645000}.",
  "Osiem ukończonych apartamentów i penthouse’ów z dwiema lub trzema sypialniami, dużymi tarasami i widokiem na morze w El Higuerón, między Fuengirolą a Benalmádeną, z basenem zewnętrznym, ogrzewanym basenem wewnętrznym, siłownią i przestrzenią coworkingową. Ukończone i gotowe do zamieszkania, od {E645000}.",
  "Åtte ferdigstilte leiligheter og toppleiligheter med to eller tre soverom, store terrasser og havutsikt i El Higuerón, mellom Fuengirola og Benalmádena, med utendørs basseng, oppvarmet innendørs basseng, treningsrom og coworking-område. Ferdigstilt og klare til innflytting, fra {E645000}.",
  "Åtta färdigställda lägenheter och takvåningar med två eller tre sovrum, stora terrasser och havsutsikt i El Higuerón, mellan Fuengirola och Benalmádena, med utomhuspool, uppvärmd inomhuspool, gym och coworkingyta. Färdigställda och inflyttningsklara, från {E645000}.")
a('Eight ready-to-move-in apartments and penthouses at El Higuerón: two or three bedrooms, 73.45',
  "Ocho apartamentos y áticos listos para entrar a vivir en El Higuerón: dos o tres dormitorios, de {N73.45} a {N116.74} {U} interiores, grandes terrazas, vistas al mar, piscina interior climatizada y gimnasio, desde {E645000}.",
  "Huit appartements et penthouses prêts à habiter à El Higuerón : deux ou trois chambres, de {N73.45} à {N116.74} {U} intérieurs, grandes terrasses, vue sur la mer, piscine intérieure chauffée et salle de sport, à partir de {E645000}.",
  "Acht bezugsfertige Wohnungen und Penthouses in El Higuerón: zwei oder drei Schlafzimmer, {N73.45} bis {N116.74} {U} Innenfläche, große Terrassen, Meerblick, beheizter Innenpool und Fitnessraum, ab {E645000}.",
  "Восемь готовых к заселению квартир и пентхаусов в Эль-Игероне: две или три спальни, от {N73.45} до {N116.74} {U} внутренней площади, большие террасы, вид на море, крытый подогреваемый бассейн и тренажёрный зал, от {E645000}.",
  "ثماني شقق وبنتهاوس جاهزة للسكن في إل إيغيرون: غرفتا نوم أو ثلاث، من {N73.45} إلى {N116.74} {U} مساحة داخلية، تراسات واسعة، إطلالات على البحر، مسبح داخلي مُدفّأ وصالة رياضية، ابتداءً من {E645000}.",
  "Acht appartementen en penthouses die klaar zijn om in te trekken in El Higuerón: twee of drie slaapkamers, {N73.45} tot {N116.74} {U} binnenoppervlak, grote terrassen, zeezicht, een verwarmd binnenzwembad en een gym, vanaf {E645000}.",
  "Osiem apartamentów i penthouse’ów gotowych do zamieszkania w El Higuerón: dwie lub trzy sypialnie, od {N73.45} do {N116.74} {U} powierzchni wewnętrznej, duże tarasy, widok na morze, ogrzewany basen wewnętrzny i siłownia, od {E645000}.",
  "Åtte leiligheter og toppleiligheter klare til innflytting i El Higuerón: to eller tre soverom, {N73.45} til {N116.74} {U} innvendig areal, store terrasser, havutsikt, oppvarmet innendørs basseng og treningsrom, fra {E645000}.",
  "Åtta inflyttningsklara lägenheter och takvåningar i El Higuerón: två eller tre sovrum, {N73.45} till {N116.74} {U} invändig yta, stora terrasser, havsutsikt, uppvärmd inomhuspool och gym, från {E645000}.")
a('Eight finished apartments and penthouses with large terraces and sea views at El Higuerón, ready to move in',
  "Ocho apartamentos y áticos terminados con grandes terrazas y vistas al mar en El Higuerón, listos para entrar a vivir, desde {E645000}.",
  "Huit appartements et penthouses achevés avec de grandes terrasses et vue sur la mer à El Higuerón, prêts à habiter, à partir de {E645000}.",
  "Acht fertiggestellte Wohnungen und Penthouses mit großen Terrassen und Meerblick in El Higuerón, bezugsfertig, ab {E645000}.",
  "Восемь готовых квартир и пентхаусов с большими террасами и видом на море в Эль-Игероне, готовы к заселению, от {E645000}.",
  "ثماني شقق وبنتهاوس جاهزة بتراسات واسعة وإطلالات على البحر في إل إيغيرون، جاهزة للسكن، ابتداءً من {E645000}.",
  "Acht afgeronde appartementen en penthouses met grote terrassen en zeezicht in El Higuerón, klaar om in te trekken, vanaf {E645000}.",
  "Osiem ukończonych apartamentów i penthouse’ów z dużymi tarasami i widokiem na morze w El Higuerón, gotowych do zamieszkania, od {E645000}.",
  "Åtte ferdigstilte leiligheter og toppleiligheter med store terrasser og havutsikt i El Higuerón, klare til innflytting, fra {E645000}.",
  "Åtta färdigställda lägenheter och takvåningar med stora terrasser och havsutsikt i El Higuerón, inflyttningsklara, från {E645000}.")
a('8 homes available',
  "8 viviendas disponibles", "8 logements disponibles", "8 Wohnungen verfügbar", "8 квартир доступно", "8 مساكن متاحة",
  "8 woningen beschikbaar", "8 mieszkań dostępnych", "8 boliger tilgjengelige", "8 bostäder tillgängliga")
a('El Higuerón', 'El Higuerón', 'El Higuerón', 'El Higuerón', 'Эль-Игерон', 'إل إيغيرون', 'El Higuerón', 'El Higuerón', 'El Higuerón', 'El Higuerón')
a('Eight finished two- and three-bedroom apartments and penthouses at El Higuerón, with large terraces',
  "Ocho apartamentos y áticos terminados de dos y tres dormitorios en El Higuerón, con grandes terrazas, vistas al mar, piscina exterior, piscina interior climatizada, gimnasio y espacio de coworking.",
  "Huit appartements et penthouses achevés de deux et trois chambres à El Higuerón, avec de grandes terrasses, vue sur la mer, une piscine extérieure, une piscine intérieure chauffée, une salle de sport et un espace de coworking.",
  "Acht fertiggestellte Wohnungen und Penthouses mit zwei und drei Schlafzimmern in El Higuerón, mit großen Terrassen, Meerblick, Außenpool, beheiztem Innenpool, Fitnessraum und Coworking-Bereich.",
  "Восемь готовых двух- и трёхспальных квартир и пентхаусов в Эль-Игероне с большими террасами, видом на море, открытым бассейном, крытым подогреваемым бассейном, тренажёрным залом и коворкингом.",
  "ثماني شقق وبنتهاوس جاهزة من غرفتي نوم وثلاث غرف في إل إيغيرون، بتراسات واسعة وإطلالات على البحر ومسبح خارجي ومسبح داخلي مُدفّأ وصالة رياضية ومساحة عمل مشتركة.",
  "Acht afgeronde appartementen en penthouses met twee en drie slaapkamers in El Higuerón, met grote terrassen, zeezicht, een buitenzwembad, een verwarmd binnenzwembad, een gym en een coworkingruimte.",
  "Osiem ukończonych apartamentów i penthouse’ów z dwiema i trzema sypialniami w El Higuerón, z dużymi tarasami, widokiem na morze, basenem zewnętrznym, ogrzewanym basenem wewnętrznym, siłownią i przestrzenią coworkingową.",
  "Åtte ferdigstilte leiligheter og toppleiligheter med to og tre soverom i El Higuerón, med store terrasser, havutsikt, utendørs basseng, oppvarmet innendørs basseng, treningsrom og coworking-område.",
  "Åtta färdigställda lägenheter och takvåningar med två och tre sovrum i El Higuerón, med stora terrasser, havsutsikt, utomhuspool, uppvärmd inomhuspool, gym och coworkingyta.")

# ------------------------------------------------------------------ images: alt text and captions
a('Outdoor pool with the sea and the coast in the distance',
  "Piscina exterior con el mar y la costa a lo lejos y un bloque blanco escalonado a la derecha",
  "Piscine extérieure avec la mer et la côte au loin et un bâtiment blanc en terrasses à droite",
  "Außenpool mit dem Meer und der Küste in der Ferne und einem weißen, terrassierten Gebäude rechts",
  "Открытый бассейн, вдали море и побережье, справа белый ступенчатый корпус",
  "مسبح خارجي يظهر خلفه البحر والساحل في الأفق، ومبنى أبيض متدرج على اليمين",
  "Buitenzwembad met de zee en de kust in de verte en rechts een wit, getrapt gebouw",
  "Basen zewnętrzny z morzem i wybrzeżem w oddali oraz białym, tarasowym budynkiem po prawej",
  "Utendørs basseng med havet og kysten i det fjerne og en hvit, terrassert bygning til høyre",
  "Utomhuspool med havet och kusten i fjärran och en vit, terrasserad byggnad till höger")
a('Terraced white block with timber-clad bays',
  "Bloque blanco escalonado con módulos revestidos de madera y barandillas de vidrio sobre la piscina exterior, con una ladera detrás",
  "Bâtiment blanc en terrasses avec des travées habillées de bois et des garde-corps en verre au-dessus de la piscine extérieure, avec une colline derrière",
  "Weißes, terrassiertes Gebäude mit holzverkleideten Achsen und Glasbrüstungen über dem Außenpool, dahinter ein Hang",
  "Белый ступенчатый корпус с секциями, отделанными деревом, и стеклянными ограждениями над открытым бассейном, позади склон холма",
  "مبنى أبيض متدرج بوحدات مكسوة بالخشب وحواجز زجاجية فوق المسبح الخارجي، وخلفه سفح تلة",
  "Wit, getrapt gebouw met houtbeklede delen en glazen balustrades boven het buitenzwembad, met een heuvel erachter",
  "Biały, tarasowy budynek z drewnianymi okładzinami i szklanymi balustradami nad basenem zewnętrznym, za nim zbocze wzgórza",
  "Hvit, terrassert bygning med trekledde partier og glassrekkverk over utendørsbassenget, med en li bak",
  "Vit, terrasserad byggnad med träklädda partier och glasräcken ovanför utomhuspoolen, med en bergssluttning bakom")
a('Open-plan living and dining room with a sliding glass wall onto a terrace and the sea',
  "Salón comedor de planta abierta con una pared de vidrio corredera hacia una terraza y el mar",
  "Séjour et salle à manger ouverts avec une paroi vitrée coulissante donnant sur une terrasse et la mer",
  "Offener Wohn- und Essbereich mit einer Glasschiebewand zu einer Terrasse und zum Meer",
  "Гостиная-столовая открытой планировки с раздвижной стеклянной стеной на террасу и море",
  "صالة معيشة وطعام مفتوحة بجدار زجاجي منزلق يطل على تراس والبحر",
  "Open woon- en eetkamer met een glazen schuifwand naar een terras en de zee",
  "Salon z jadalnią w otwartym układzie ze szklaną ścianą przesuwną na taras i morze",
  "Åpen stue og spiseplass med en skyvbar glassvegg mot en terrasse og havet",
  "Öppet vardagsrum och matplats med en glidande glasvägg mot en terrass och havet")
a('Bedroom with a double bed and a sliding glass door to a terrace with a sea view',
  "Dormitorio con cama doble y una puerta corredera de vidrio hacia una terraza con vistas al mar",
  "Chambre avec un lit double et une porte coulissante en verre donnant sur une terrasse avec vue sur la mer",
  "Schlafzimmer mit Doppelbett und einer Glasschiebetür zu einer Terrasse mit Meerblick",
  "Спальня с двуспальной кроватью и раздвижной стеклянной дверью на террасу с видом на море",
  "غرفة نوم بسرير مزدوج وباب زجاجي منزلق يؤدي إلى تراس بإطلالة على البحر",
  "Slaapkamer met een tweepersoonsbed en een glazen schuifdeur naar een terras met zeezicht",
  "Soverom med dobbeltseng og en skyvbar glassdør til en terrasse med havutsikt",
  "Sovrum med dubbelsäng och en glidande glasdörr till en terrass med havsutsikt")
a('Photographs of the show apartment, the finished building',
  "Fotografías del piso piloto, del edificio terminado y de las zonas comunes, y el plano de cada una de las ocho viviendas disponibles.",
  "Photographies de l’appartement témoin, du bâtiment achevé et des espaces communs, et plan de chacun des huit logements disponibles.",
  "Fotos der Musterwohnung, des fertiggestellten Gebäudes und der Gemeinschaftsbereiche sowie der Grundriss jeder der acht verfügbaren Wohnungen.",
  "Фотографии демонстрационной квартиры, готового здания и общих зон, а также планировка каждой из восьми доступных квартир.",
  "صور للشقة النموذجية والمبنى المكتمل والمرافق المشتركة، ومخطط كل واحدة من المساكن الثمانية المتاحة.",
  "Foto’s van het showappartement, het opgeleverde gebouw en de gedeelde voorzieningen, en de plattegrond van elk van de acht beschikbare woningen.",
  "Zdjęcia lokalu pokazowego, ukończonego budynku i wspólnych udogodnień oraz rzut każdego z ośmiu dostępnych mieszkań.",
  "Bilder av visningsleiligheten, den ferdigstilte bygningen og fellesfasilitetene, og plantegningen for hver av de åtte tilgjengelige boligene.",
  "Bilder av visningslägenheten, den färdiga byggnaden och de gemensamma bekvämligheterna, och planritningen för var och en av de åtta tillgängliga bostäderna.")
a('The interior and terrace photographs show a furnished show apartment',
  "Las fotografías de interiores y terrazas muestran un piso piloto amueblado, y el aviso del promotor indica que el mobiliario, la decoración y el paisajismo de sus imágenes no están incluidos en el precio. Los planos son del promotor y las superficies que figuran en ellos son orientativas y pueden variar por razones técnicas, legales o de ejecución. Los nombres de las estancias en los planos están en español.",
  "Les photographies des intérieurs et des terrasses montrent un appartement témoin meublé, et l’avis du promoteur précise que le mobilier, la décoration et l’aménagement paysager de ses images ne sont pas inclus dans le prix. Les plans sont ceux du promoteur, et les surfaces qui y figurent sont indicatives et peuvent varier pour des raisons techniques, légales ou d’exécution. Les noms des pièces sur les plans sont en espagnol.",
  "Die Fotos der Innenräume und Terrassen zeigen eine möblierte Musterwohnung, und laut dem Hinweis des Bauträgers sind Möbel, Dekoration und Landschaftsgestaltung in seinen Bildern nicht im Preis enthalten. Die Grundrisse stammen vom Bauträger, und die darin angegebenen Flächen sind Richtwerte, die sich aus technischen, rechtlichen oder baulichen Gründen ändern können. Die Raumbezeichnungen in den Grundrissen sind auf Spanisch.",
  "На фотографиях интерьеров и террас показана меблированная демонстрационная квартира, а в уведомлении застройщика сказано, что мебель, декор и благоустройство на его изображениях в цену не входят. Планировки принадлежат застройщику, указанные на них площади ориентировочные и могут измениться по техническим, юридическим или строительным причинам. Названия помещений на планах даны на испанском языке.",
  "تعرض صور الداخل والتراسات شقة نموذجية مفروشة، ويذكر إشعار المطوّر أن الأثاث والديكور وتنسيق الحدائق في صوره غير مشمولة في السعر. المخططات من إعداد المطوّر، والمساحات المذكورة عليها تقريبية وقد تتغير لأسباب فنية أو قانونية أو تنفيذية. أسماء الغرف على المخططات بالإسبانية.",
  "De foto’s van de interieurs en terrassen tonen een gemeubileerd showappartement, en volgens de mededeling van de ontwikkelaar zijn het meubilair, de decoratie en de landschapsinrichting op zijn beelden niet in de prijs inbegrepen. De plattegronden zijn van de ontwikkelaar en de oppervlaktes erop zijn indicatief en kunnen om technische, juridische of bouwkundige redenen wijzigen. De ruimtenamen op de plattegronden zijn in het Spaans.",
  "Zdjęcia wnętrz i tarasów przedstawiają umeblowany lokal pokazowy, a według zawiadomienia dewelopera meble, dekoracje i zagospodarowanie terenu na jego obrazach nie są wliczone w cenę. Rzuty pochodzą od dewelopera, a podane na nich powierzchnie są orientacyjne i mogą ulec zmianie z przyczyn technicznych, prawnych lub wykonawczych. Nazwy pomieszczeń na rzutach są po hiszpańsku.",
  "Bildene av interiørene og terrassene viser en møblert visningsleilighet, og utbyggerens merknad sier at møbler, dekor og landskapsutforming på bildene ikke er inkludert i prisen. Plantegningene er utbyggerens, og arealene på dem er veiledende og kan endres av tekniske, juridiske eller byggemessige grunner. Romnavnene på plantegningene er på spansk.",
  "Bilderna av interiörer och terrasser visar en möblerad visningslägenhet, och exploatörens meddelande säger att möbler, dekor och landskapsutformning i dess bilder inte ingår i priset. Planritningarna är exploatörens, och ytorna på dem är ungefärliga och kan ändras av tekniska, juridiska eller byggmässiga skäl. Rumsnamnen på planritningarna är på spanska.")
a('The pool and the sea', "La piscina y el mar", "La piscine et la mer", "Der Pool und das Meer", "Бассейн и море", "المسبح والبحر", "Het zwembad en de zee", "Bassenget og havet", "Poolen och havet")
a('The terraced block above the pool', "El bloque escalonado sobre la piscina", "Le bâtiment en terrasses au-dessus de la piscine", "Das terrassierte Gebäude über dem Pool", "Ступенчатый корпус над бассейном", "المبنى المتدرج فوق المسبح", "Het getrapte gebouw boven het zwembad", "Den terrasserte bygningen over bassenget", "Den terrasserade byggnaden ovanför poolen")
a('Aerial view straight down on the outdoor pool',
  "Vista aérea cenital de la piscina exterior, sus escalones y la zona de baño con tumbonas",
  "Vue aérienne à la verticale de la piscine extérieure, de ses marches et de la plage avec transats",
  "Luftaufnahme senkrecht von oben auf den Außenpool, seine Stufen und die Poolterrasse mit Sonnenliegen",
  "Вид сверху на открытый бассейн, его ступени и площадку с шезлонгами",
  "منظر جوي عمودي للمسبح الخارجي ودرجاته وساحة المسبح مع كراسي التشمس",
  "Luchtfoto recht van boven op het buitenzwembad, de trap en het zwembadterras met ligbedden",
  "Luftfoto rett ovenfra av utendørsbassenget, trappene og bassengterrassen med solsenger",
  "Flygbild rakt uppifrån av utomhuspoolen, dess trappsteg och poolterrassen med solstolar")
a('The outdoor pool from above', "La piscina exterior desde el aire", "La piscine extérieure vue d’en haut", "Der Außenpool von oben", "Открытый бассейн сверху", "المسبح الخارجي من الأعلى", "Het buitenzwembad van bovenaf", "Utendørsbassenget sett ovenfra", "Utomhuspoolen uppifrån")
a('Covered terrace with a sofa and armchairs',
  "Terraza cubierta con un sofá y sillones y una vista sobre los tejados hasta el mar",
  "Terrasse couverte avec un canapé et des fauteuils, et une vue par-dessus les toits jusqu’à la mer",
  "Überdachte Terrasse mit Sofa und Sesseln und Blick über die Dächer bis zum Meer",
  "Крытая терраса с диваном и креслами, вид поверх крыш на море",
  "تراس مسقوف مع أريكة ومقاعد وإطلالة فوق الأسطح حتى البحر",
  "Overdekt terras met een bank en fauteuils en uitzicht over de daken tot aan de zee",
  "Overbygd terrasse med sofa og lenestoler og utsikt over takene til havet",
  "Övertäckt terrass med soffa och fåtöljer och utsikt över hustaken mot havet")
a('A covered terrace with a sea view', "Una terraza cubierta con vistas al mar", "Une terrasse couverte avec vue sur la mer", "Eine überdachte Terrasse mit Meerblick", "Крытая терраса с видом на море", "تراس مسقوف بإطلالة على البحر", "Een overdekt terras met zeezicht", "En overbygd terrasse med havutsikt", "En övertäckt terrass med havsutsikt")
a('Terrace with an outdoor kitchen and a built-in barbecue',
  "Terraza con cocina exterior y barbacoa integrada, y una puerta corredera de vidrio hacia la vivienda",
  "Terrasse avec cuisine d’été et barbecue intégré, et une porte coulissante en verre vers le logement",
  "Terrasse mit Außenküche und eingebautem Grill sowie einer Glasschiebetür in die Wohnung",
  "Терраса с летней кухней и встроенным барбекю и раздвижной стеклянной дверью в квартиру",
  "تراس مع مطبخ خارجي وشواية مدمجة وباب زجاجي منزلق إلى داخل المسكن",
  "Terras met een buitenkeuken en een ingebouwde barbecue en een glazen schuifdeur naar de woning",
  "Terrasse med utekjøkken og innebygd grill og en skyvbar glassdør inn til boligen",
  "Terrass med utekök och inbyggd grill och en glidande glasdörr in till bostaden")
a('Terrace with an outdoor kitchen', "Terraza con cocina exterior", "Terrasse avec cuisine d’été", "Terrasse mit Außenküche", "Терраса с летней кухней", "تراس مع مطبخ خارجي", "Terras met een buitenkeuken", "Terrasse med utekjøkken", "Terrass med utekök")
a('Terrace with a raised plunge pool and wide steps beside it',
  "Terraza con una piscina pequeña elevada y unos amplios escalones a su lado",
  "Terrasse avec un petit bassin surélevé et de larges marches à côté",
  "Terrasse mit einem erhöhten Tauchbecken und breiten Stufen daneben",
  "Терраса с приподнятым небольшим бассейном и широкими ступенями рядом",
  "تراس مع مسبح صغير مرتفع ودرجات عريضة بجانبه",
  "Terras met een verhoogd plonsbad en brede treden ernaast",
  "Terrasse med et hevet stupebasseng og brede trapper ved siden av",
  "Terrass med en upphöjd doppool och breda trappsteg bredvid")
a('Terrace with a raised plunge pool', "Terraza con una piscina pequeña elevada", "Terrasse avec un petit bassin surélevé", "Terrasse mit einem erhöhten Tauchbecken", "Терраса с приподнятым небольшим бассейном", "تراس مع مسبح صغير مرتفع", "Terras met een verhoogd plonsbad", "Terrasse med et hevet stupebasseng", "Terrass med en upphöjd doppool")
a('Living and dining room with a sea view', "Salón comedor con vistas al mar", "Séjour et salle à manger avec vue sur la mer", "Wohn- und Essbereich mit Meerblick", "Гостиная-столовая с видом на море", "صالة معيشة وطعام بإطلالة على البحر", "Woon- en eetkamer met zeezicht", "Stue og spiseplass med havutsikt", "Vardagsrum och matplats med havsutsikt")
a('Dining table, kitchen island and living area in an open-plan room',
  "Mesa de comedor, isla de cocina y zona de estar en una estancia de planta abierta",
  "Table à manger, îlot de cuisine et coin salon dans une pièce ouverte",
  "Esstisch, Kücheninsel und Wohnbereich in einem offenen Raum",
  "Обеденный стол, кухонный остров и гостиная зона в помещении открытой планировки",
  "طاولة طعام وجزيرة مطبخ ومنطقة جلوس في مساحة مفتوحة",
  "Eettafel, keukeneiland en zithoek in een open ruimte",
  "Spisebord, kjøkkenøy og stuedel i et åpent rom",
  "Matbord, köksö och vardagsrumsdel i ett öppet rum")
a('Dining table and kitchen island', "Mesa de comedor e isla de cocina", "Table à manger et îlot de cuisine", "Esstisch und Kücheninsel", "Обеденный стол и кухонный остров", "طاولة الطعام وجزيرة المطبخ", "Eettafel en keukeneiland", "Spisebord og kjøkkenøy", "Matbord och köksö")
a('Living room with a sofa, a television',
  "Salón con sofá y televisor, y el comedor y la cocina al fondo",
  "Séjour avec un canapé et un téléviseur, avec la salle à manger et la cuisine au fond",
  "Wohnzimmer mit Sofa und Fernseher, dahinter Essbereich und Küche",
  "Гостиная с диваном и телевизором, за ней столовая и кухня",
  "غرفة معيشة مع أريكة وتلفاز، وخلفها منطقة الطعام والمطبخ",
  "Woonkamer met een bank en een televisie, met daarachter de eetkamer en de keuken",
  "Stue med sofa og TV, med spiseplass og kjøkken bakenfor",
  "Vardagsrum med soffa och tv, med matplats och kök bakom")
a('Fitted kitchen with a tall unit holding an oven',
  "Cocina equipada con una columna que alberga un horno y un microondas, y una encimera con fregadero",
  "Cuisine équipée avec une colonne abritant un four et un micro-ondes, et un plan de travail avec évier",
  "Einbauküche mit einem Hochschrank für Backofen und Mikrowelle und einer Arbeitsplatte mit Spüle",
  "Кухня с высоким шкафом, в котором встроены духовой шкаф и микроволновая печь, и столешницей с мойкой",
  "مطبخ مجهز بخزانة طويلة تضم فرنًا وميكروويف، وسطح عمل مع حوض",
  "Ingerichte keuken met een hoge kast met oven en magnetron en een werkblad met spoelbak",
  "Møblert kjøkken med et høyskap med ovn og mikrobølgeovn og en benkeplate med vask",
  "Utrustat kök med ett högskåp med ugn och mikrovågsugn och en bänkskiva med diskho")
a('Bedroom with a double bed and a sliding glass door onto a terrace and the sea',
  "Dormitorio con cama doble y una puerta corredera de vidrio hacia una terraza y el mar",
  "Chambre avec un lit double et une porte coulissante en verre donnant sur une terrasse et la mer",
  "Schlafzimmer mit Doppelbett und einer Glasschiebetür zu einer Terrasse und zum Meer",
  "Спальня с двуспальной кроватью и раздвижной стеклянной дверью на террасу и море",
  "غرفة نوم بسرير مزدوج وباب زجاجي منزلق يؤدي إلى تراس والبحر",
  "Slaapkamer met een tweepersoonsbed en een glazen schuifdeur naar een terras en de zee",
  "Soverom med dobbeltseng og en skyvbar glassdør til en terrasse og havet",
  "Sovrum med dubbelsäng och en glidande glasdörr till en terrass och havet")
a('Bathroom with a walk-in shower, a wall-hung toilet',
  "Baño con ducha a ras de suelo, inodoro suspendido y mueble de lavabo suspendido con espejo",
  "Salle de bains avec douche à l’italienne, WC suspendu et meuble vasque suspendu avec miroir",
  "Bad mit bodengleicher Dusche, Wand-WC und hängendem Waschtisch mit Spiegel",
  "Ванная комната с душем без поддона, подвесным унитазом и подвесной тумбой с умывальником и зеркалом",
  "حمام بدش مفتوح ومرحاض معلّق ووحدة مغسلة معلّقة مع مرآة",
  "Badkamer met een inloopdouche, een hangend toilet en een hangend badkamermeubel met spiegel",
  "Bad med åpen dusj, vegghengt toalett og veggmontert servantskap med speil",
  "Badrum med en öppen dusch, en väggmonterad toalett och ett väggmonterat badrumsskåp med spegel")
a('Indoor pool with a sauna behind a glass wall',
  "Piscina interior con una sauna tras una pared de vidrio y equipos de gimnasio al fondo",
  "Piscine intérieure avec un sauna derrière une paroi vitrée et des appareils de sport au fond",
  "Innenpool mit einer Sauna hinter einer Glaswand und Fitnessgeräten dahinter",
  "Крытый бассейн с сауной за стеклянной стеной и тренажёрами в глубине",
  "مسبح داخلي مع ساونا خلف جدار زجاجي ومعدات رياضية في الخلف",
  "Binnenzwembad met een sauna achter een glazen wand en fitnessapparatuur daarachter",
  "Innendørs basseng med en badstue bak en glassvegg og treningsutstyr bakenfor",
  "Inomhuspool med en bastu bakom en glasvägg och träningsutrustning bortom")
a('The indoor pool', "La piscina interior", "La piscine intérieure", "Der Innenpool", "Крытый бассейн", "المسبح الداخلي", "Het binnenzwembad", "Innendørsbassenget", "Inomhuspoolen")
a('Gym with a rack of dumbbells',
  "Gimnasio con un soporte de mancuernas, un banco y una máquina de poleas, y una pared de espejos",
  "Salle de sport avec un rack d’haltères, un banc et un appareil à câbles, et un mur de miroirs",
  "Fitnessraum mit Hantelständer, Bank und Kabelzug sowie einer Spiegelwand",
  "Тренажёрный зал со стойкой гантелей, скамьёй, блочным тренажёром и зеркальной стеной",
  "صالة رياضية فيها حامل أثقال وبنش وجهاز كابلات وجدار من المرايا",
  "Gym met een rek met dumbbells, een bank en een kabeltoestel, en een spiegelwand",
  "Treningsrom med et stativ med manualer, en benk og en kabelmaskin, og en speilvegg",
  "Gym med ett ställ med hantlar, en bänk och en kabelmaskin, och en spegelvägg")
a('The gym', "El gimnasio", "La salle de sport", "Der Fitnessraum", "Тренажёрный зал", "الصالة الرياضية", "De gym", "Treningsrommet", "Gymmet")
a('Gym with a treadmill and a cross trainer',
  "Gimnasio con una cinta de correr y una elíptica, y la piscina interior tras una pared de vidrio",
  "Salle de sport avec un tapis de course et un vélo elliptique, et la piscine intérieure derrière une paroi vitrée",
  "Fitnessraum mit Laufband und Crosstrainer, dahinter der Innenpool hinter einer Glaswand",
  "Тренажёрный зал с беговой дорожкой и эллиптическим тренажёром, за стеклянной стеной крытый бассейн",
  "صالة رياضية فيها جهاز جري وجهاز إهليلجي، ومن خلفها المسبح الداخلي وراء جدار زجاجي",
  "Gym met een loopband en een crosstrainer, met het binnenzwembad achter een glazen wand",
  "Treningsrom med en tredemølle og en crosstrainer, med innendørsbassenget bak en glassvegg",
  "Gym med ett löpband och en crosstrainer, med inomhuspoolen bakom en glasvägg")
a('Gym and indoor pool', "Gimnasio y piscina interior", "Salle de sport et piscine intérieure", "Fitnessraum und Innenpool", "Тренажёрный зал и крытый бассейн", "الصالة الرياضية والمسبح الداخلي", "Gym en binnenzwembad", "Treningsrom og innendørsbasseng", "Gym och inomhuspool")
a('Shared room with a long marble table',
  "Sala común con una larga mesa de mármol, sillas y sillones y una ventana al jardín",
  "Salle commune avec une longue table en marbre, des chaises et des fauteuils et une fenêtre sur le jardin",
  "Gemeinschaftsraum mit langem Marmortisch, Stühlen und Sesseln und einem Fenster zum Garten",
  "Общая комната с длинным мраморным столом, стульями и креслами и окном в сад",
  "غرفة مشتركة بطاولة رخامية طويلة وكراسٍ ومقاعد ونافذة على الحديقة",
  "Gedeelde ruimte met een lange marmeren tafel, stoelen en fauteuils en een raam op de tuin",
  "Fellesrom med et langt marmorbord, stoler og lenestoler og et vindu mot hagen",
  "Gemensamt rum med ett långt marmorbord, stolar och fåtöljer och ett fönster mot trädgården")
a('A shared room with a long table', "Una sala común con una larga mesa", "Une salle commune avec une longue table", "Ein Gemeinschaftsraum mit langem Tisch", "Общая комната с длинным столом", "غرفة مشتركة بطاولة طويلة", "Een gedeelde ruimte met een lange tafel", "Et fellesrom med et langt bord", "Ett gemensamt rum med ett långt bord")
a('Meeting room with a long wooden table',
  "Sala de reuniones con una larga mesa de madera, sillas de cuero y dos lámparas colgantes",
  "Salle de réunion avec une longue table en bois, des chaises en cuir et deux suspensions",
  "Besprechungsraum mit langem Holztisch, Lederstühlen und zwei Pendelleuchten",
  "Переговорная с длинным деревянным столом, кожаными стульями и двумя подвесными светильниками",
  "غرفة اجتماعات بطاولة خشبية طويلة وكراسي جلدية ومصباحين معلّقين",
  "Vergaderruimte met een lange houten tafel, leren stoelen en twee hanglampen",
  "Møterom med et langt trebord, lærstoler og to taklamper",
  "Mötesrum med ett långt träbord, skinnstolar och två taklampor")
a('A meeting room', "Una sala de reuniones", "Une salle de réunion", "Ein Besprechungsraum", "Переговорная", "غرفة اجتماعات", "Een vergaderruimte", "Et møterom", "Ett mötesrum")

# ------------------------------------------------------------------ overview, why, architecture
a('Eight homes, <em>finished and available</em>',
  "Ocho viviendas, <em>terminadas y disponibles</em>", "Huit logements, <em>achevés et disponibles</em>", "Acht Wohnungen, <em>fertig und verfügbar</em>",
  "Восемь квартир, <em>готовых и доступных</em>", "ثمانية مساكن، <em>مكتملة ومتاحة</em>", "Acht woningen, <em>opgeleverd en beschikbaar</em>",
  "Osiem mieszkań, <em>ukończonych i dostępnych</em>", "Åtte boliger, <em>ferdigstilte og tilgjengelige</em>", "Åtta bostäder, <em>färdiga och tillgängliga</em>")
a('Eight apartments and penthouses are available in three blocks',
  "Hay ocho apartamentos y áticos disponibles en tres bloques en El Higuerón, entre Fuengirola y Benalmádena. El folleto del promotor los describe como viviendas terminadas de disponibilidad inmediata, y su portal los presenta como listos para entrar a vivir. Cinco tienen tres dormitorios y tres tienen dos, todos con dos baños y grandes terrazas.",
  "Huit appartements et penthouses sont disponibles dans trois blocs à El Higuerón, entre Fuengirola et Benalmádena. La brochure du promoteur les décrit comme des logements achevés, disponibles immédiatement, et son portail les présente comme prêts à habiter. Cinq ont trois chambres et trois en ont deux, tous avec deux salles de bains et de grandes terrasses.",
  "In drei Blöcken in El Higuerón, zwischen Fuengirola und Benalmádena, sind acht Wohnungen und Penthouses verfügbar. Die Broschüre des Bauträgers beschreibt sie als fertiggestellte Wohnungen mit sofortiger Verfügbarkeit, und sein Portal führt sie als bezugsfertig auf. Fünf haben drei Schlafzimmer und drei haben zwei, alle mit zwei Bädern und großen Terrassen.",
  "В трёх корпусах в Эль-Игероне, между Фуэнхиролой и Бенальмаденой, доступны восемь квартир и пентхаусов. В брошюре застройщика они названы готовыми резиденциями с немедленной передачей, а на его портале указаны как готовые к заселению. У пяти из них три спальни, у трёх — две, у всех по две ванные комнаты и большие террасы.",
  "تتوفر ثماني شقق وبنتهاوس في ثلاثة مبانٍ في إل إيغيرون بين فوينخيرولا وبينالمادينا. يصفها كتيّب المطوّر بأنها مساكن مكتملة متاحة للتسليم الفوري، ويعرضها موقعه الإلكتروني على أنها جاهزة للسكن. خمسة منها بثلاث غرف نوم وثلاثة بغرفتي نوم، وجميعها بحمامين وتراسات واسعة.",
  "In drie blokken in El Higuerón, tussen Fuengirola en Benalmádena, zijn acht appartementen en penthouses beschikbaar. De brochure van de ontwikkelaar beschrijft ze als opgeleverde woningen die direct beschikbaar zijn, en zijn portaal vermeldt ze als klaar om in te trekken. Vijf hebben drie slaapkamers en drie hebben er twee, allemaal met twee badkamers en grote terrassen.",
  "W trzech blokach w El Higuerón, między Fuengirolą a Benalmádeną, dostępnych jest osiem apartamentów i penthouse’ów. Broszura dewelopera opisuje je jako ukończone rezydencje dostępne od ręki, a jego portal podaje je jako gotowe do zamieszkania. Pięć z nich ma trzy sypialnie, a trzy mają dwie; wszystkie mają dwie łazienki i duże tarasy.",
  "Åtte leiligheter og toppleiligheter er tilgjengelige i tre bygg i El Higuerón, mellom Fuengirola og Benalmádena. Utbyggerens brosjyre beskriver dem som ferdigstilte boliger med umiddelbar tilgjengelighet, og portalen deres oppgir dem som klare til innflytting. Fem har tre soverom og tre har to, alle med to bad og store terrasser.",
  "Åtta lägenheter och takvåningar är tillgängliga i tre hus i El Higuerón, mellan Fuengirola och Benalmádena. Exploatörens broschyr beskriver dem som färdiga bostäder med omedelbar tillgång, och dess portal anger dem som inflyttningsklara. Fem har tre sovrum och tre har två, alla med två badrum och stora terrasser.")
a('The shared facilities listed by the developer are an outdoor pool',
  "Las zonas comunes que enumera el promotor son una piscina exterior, una piscina interior climatizada, un gimnasio, un espacio de coworking, una sala social y jardines, y la promoción cuenta con un piso piloto que se puede visitar.",
  "Les espaces communs listés par le promoteur sont une piscine extérieure, une piscine intérieure chauffée, une salle de sport, un espace de coworking, un salon commun et des jardins, et le programme dispose d’un appartement témoin que l’on peut visiter.",
  "Die vom Bauträger aufgeführten Gemeinschaftsbereiche sind ein Außenpool, ein beheizter Innenpool, ein Fitnessraum, ein Coworking-Bereich, ein Gemeinschaftsraum und Gärten, und die Anlage hat eine Musterwohnung, die besichtigt werden kann.",
  "Общие зоны, указанные застройщиком: открытый бассейн, крытый подогреваемый бассейн, тренажёрный зал, коворкинг, общий зал и сады; в комплексе есть демонстрационная квартира, которую можно посмотреть.",
  "المرافق المشتركة التي يذكرها المطوّر هي مسبح خارجي ومسبح داخلي مُدفّأ وصالة رياضية ومساحة عمل مشتركة وقاعة اجتماعية وحدائق، ويضم المشروع شقة نموذجية يمكن زيارتها.",
  "De gedeelde voorzieningen die de ontwikkelaar vermeldt zijn een buitenzwembad, een verwarmd binnenzwembad, een gym, een coworkingruimte, een gemeenschappelijke ruimte en tuinen, en het project heeft een showappartement dat te bezichtigen is.",
  "Udogodnienia wspólne wymienione przez dewelopera to basen zewnętrzny, ogrzewany basen wewnętrzny, siłownia, przestrzeń coworkingowa, sala towarzyska i ogrody, a w inwestycji jest lokal pokazowy, który można zwiedzić.",
  "Fellesfasilitetene utbyggeren oppgir er et utendørs basseng, et oppvarmet innendørs basseng, et treningsrom, et coworking-område, et felles oppholdsrom og hager, og prosjektet har en visningsleilighet som kan besøkes.",
  "De gemensamma bekvämligheter som exploatören anger är en utomhuspool, en uppvärmd inomhuspool, ett gym, en coworkingyta, ett gemensamt rum och trädgårdar, och projektet har en visningslägenhet som kan besökas.")
a('Large terraces, and a private pool on three of the homes',
  "Grandes terrazas y una piscina privada en tres de las viviendas", "De grandes terrasses et une piscine privée dans trois des logements",
  "Große Terrassen und ein privater Pool bei drei der Wohnungen", "Большие террасы и частный бассейн у трёх квартир",
  "تراسات واسعة ومسبح خاص في ثلاثة من المساكن", "Grote terrassen en een privézwembad bij drie van de woningen",
  "Duże tarasy i prywatny basen przy trzech mieszkaniach", "Store terrasser og et privat basseng ved tre av boligene",
  "Stora terrasser och en privat pool vid tre av bostäderna")
a('Finished homes with big terraces and sea views',
  "Viviendas terminadas con grandes terrazas y vistas al mar, que puede recorrer en un piso piloto en lugar de juzgar a partir de una infografía.",
  "Des logements achevés avec de grandes terrasses et vue sur la mer, que vous pouvez parcourir dans un appartement témoin plutôt que de les juger sur une image de synthèse.",
  "Fertige Wohnungen mit großen Terrassen und Meerblick, die Sie in einer Musterwohnung besichtigen können, statt sie anhand eines Renderings zu beurteilen.",
  "Готовые квартиры с большими террасами и видом на море, которые можно осмотреть в демонстрационной квартире, а не оценивать по визуализации.",
  "مساكن مكتملة بتراسات واسعة وإطلالات على البحر، يمكنكم التجول فيها في شقة نموذجية بدلاً من الحكم عليها من خلال صورة تصميم.",
  "Opgeleverde woningen met grote terrassen en zeezicht, die u in een showappartement kunt doorlopen in plaats van op een render te beoordelen.",
  "Ukończone mieszkania z dużymi tarasami i widokiem na morze, które można obejrzeć w lokalu pokazowym zamiast oceniać na podstawie wizualizacji.",
  "Ferdigstilte boliger med store terrasser og havutsikt, som kan gås gjennom i en visningsleilighet i stedet for å vurderes ut fra en illustrasjon.",
  "Färdiga bostäder med stora terrasser och havsutsikt, som går att gå igenom i en visningslägenhet i stället för att bedömas utifrån en illustration.")
a('Buyers who want to move in soon',
  "Compradores que quieren mudarse pronto y prefieren ver una vivienda terminada y sus instalaciones antes de comprometerse.",
  "Acheteurs qui souhaitent emménager bientôt et préfèrent voir un logement achevé et ses équipements avant de s’engager.",
  "Käufer, die bald einziehen möchten und eine fertige Wohnung und ihre Einrichtungen sehen wollen, bevor sie sich binden.",
  "Покупатели, которые хотят скоро заселиться и предпочитают увидеть готовую квартиру и инфраструктуру, прежде чем принять решение.",
  "مشترون يريدون الانتقال قريباً ويفضلون رؤية مسكن مكتمل ومرافقه قبل الالتزام.",
  "Kopers die snel willen intrekken en een opgeleverde woning en de voorzieningen liever zien voordat ze zich vastleggen.",
  "Kupujący, którzy chcą wkrótce się wprowadzić i wolą zobaczyć ukończone mieszkanie i jego udogodnienia, zanim się zobowiążą.",
  "Kjøpere som vil flytte inn snart og helst vil se en ferdigstilt bolig og fasilitetene før de forplikter seg.",
  "Köpare som vill flytta in snart och hellre ser en färdig bostad och dess bekvämligheter innan de binder sig.")
a('Large terraces on every home, from 46 sqm',
  "Grandes terrazas en todas las viviendas, de 46 m² en los áticos a 177 m² en la planta baja, y tres viviendas de planta baja con una piscina privada en el plano.",
  "De grandes terrasses dans chaque logement, de 46 m² pour les penthouses à 177 m² au rez-de-chaussée, et trois logements en rez-de-chaussée avec une piscine privée sur le plan.",
  "Große Terrassen bei jeder Wohnung, von 46 m² bei den Penthouses bis 177 m² im Erdgeschoss, und drei Erdgeschosswohnungen mit einem im Grundriss eingezeichneten privaten Pool.",
  "Большие террасы у каждой квартиры — от 46 м² у пентхаусов до 177 м² на первом этаже — и три квартиры на первом этаже с частным бассейном на плане.",
  "تراسات واسعة في كل مسكن، من 46 م² في البنتهاوس إلى 177 م² في الطابق الأرضي، وثلاثة مساكن في الطابق الأرضي بمسبح خاص مرسوم في المخطط.",
  "Grote terrassen bij elke woning, van 46 m² bij de penthouses tot 177 m² op de begane grond, en drie woningen op de begane grond met een privézwembad op de plattegrond.",
  "Duże tarasy przy każdym mieszkaniu, od 46 m² w penthouse’ach do 177 m² na parterze, oraz trzy mieszkania na parterze z prywatnym basenem na rzucie.",
  "Store terrasser ved hver bolig, fra 46 m² på toppleilighetene til 177 m² i første etasje, og tre boliger i første etasje med et privat basseng på plantegningen.",
  "Stora terrasser vid varje bostad, från 46 m² på takvåningarna till 177 m² på bottenvåningen, och tre bostäder på bottenvåningen med en privat pool på planritningen.")
a('El Higuerón sits between Fuengirola and Benalmádena, beside the AP-7',
  "El Higuerón está entre Fuengirola y Benalmádena, junto a la AP-7 en el mapa del promotor, con varias playas y campos de golf señalados a su alrededor.",
  "El Higuerón se situe entre Fuengirola et Benalmádena, près de l’AP-7 sur la carte du promoteur, avec plusieurs plages et terrains de golf indiqués alentour.",
  "El Higuerón liegt zwischen Fuengirola und Benalmádena, auf der Karte des Bauträgers neben der AP-7, mit mehreren Stränden und Golfplätzen in der Umgebung.",
  "Эль-Игерон находится между Фуэнхиролой и Бенальмаденой, на карте застройщика рядом с автострадой AP-7; вокруг отмечены несколько пляжей и полей для гольфа.",
  "تقع إل إيغيرون بين فوينخيرولا وبينالمادينا، بجوار الطريق السريع AP-7 على خريطة المطوّر، وتظهر حولها عدة شواطئ وملاعب غولف.",
  "El Higuerón ligt tussen Fuengirola en Benalmádena, op de kaart van de ontwikkelaar naast de AP-7, met meerdere stranden en golfbanen in de omgeving.",
  "El Higuerón leży między Fuengirolą a Benalmádeną, na mapie dewelopera obok autostrady AP-7, a wokół zaznaczono kilka plaż i pól golfowych.",
  "El Higuerón ligger mellom Fuengirola og Benalmádena, ved siden av AP-7 på utbyggerens kart, med flere strender og golfbaner markert rundt.",
  "El Higuerón ligger mellan Fuengirola och Benalmádena, bredvid AP-7 på exploatörens karta, med flera stränder och golfbanor markerade runt omkring.")
a('Why check the details', "Por qué comprobar los detalles", "Pourquoi vérifier les détails", "Warum die Details prüfen", "Почему нужно проверить детали", "لماذا نتحقق من التفاصيل", "Waarom de details controleren", "Hvorfor sjekke detaljene", "Varför kontrollera detaljerna")
a('The developer’s documents give no completion date, licence or payment terms',
  "Los documentos del promotor no indican fecha de finalización, licencia ni condiciones de pago, y dos superficies de terraza difieren entre la lista de precios y los planos, por lo que confirmamos cada punto antes de cualquier reserva.",
  "Les documents du promoteur n’indiquent ni date d’achèvement, ni licence, ni conditions de paiement, et deux surfaces de terrasse diffèrent entre la liste de prix et les plans ; nous confirmons donc chaque point avant toute réservation.",
  "Die Unterlagen des Bauträgers nennen weder ein Fertigstellungsdatum noch eine Genehmigung oder Zahlungsbedingungen, und zwei Terrassenflächen weichen zwischen Preisliste und Grundrissen ab; wir klären daher jeden Punkt vor einer Reservierung.",
  "В документах застройщика нет ни даты завершения, ни лицензии, ни условий оплаты, а две площади террас в прайс-листе и на планах различаются, поэтому мы уточняем каждый пункт до любого бронирования.",
  "لا تذكر وثائق المطوّر تاريخ الإنجاز ولا الرخصة ولا شروط الدفع، كما تختلف مساحتا تراسين بين قائمة الأسعار والمخططات، لذلك نؤكد كل بند قبل أي حجز.",
  "In de documenten van de ontwikkelaar staan geen opleverdatum, vergunning of betalingsvoorwaarden, en twee terrasoppervlaktes verschillen tussen de prijslijst en de plattegronden; wij bevestigen daarom elk punt vóór een reservering.",
  "W dokumentach dewelopera nie ma daty ukończenia, pozwolenia ani warunków płatności, a dwie powierzchnie tarasów różnią się w cenniku i na rzutach, dlatego potwierdzamy każdy punkt przed jakąkolwiek rezerwacją.",
  "Utbyggerens dokumenter oppgir verken ferdigstillelsesdato, tillatelse eller betalingsvilkår, og to terrasseareal er forskjellige i prislisten og på plantegningene, så vi bekrefter hvert punkt før en eventuell reservasjon.",
  "Exploatörens dokument anger varken färdigställandedatum, tillstånd eller betalningsvillkor, och två terrassytor skiljer sig mellan prislistan och planritningarna, så vi bekräftar varje punkt före en eventuell reservation.")
a('Contemporary blocks, <em>open to the sea</em>',
  "Bloques contemporáneos, <em>abiertos al mar</em>", "Des blocs contemporains, <em>ouverts sur la mer</em>", "Zeitgenössische Blöcke, <em>zum Meer geöffnet</em>",
  "Современные корпуса, <em>открытые морю</em>", "مبانٍ معاصرة، <em>مفتوحة على البحر</em>", "Eigentijdse blokken, <em>open naar de zee</em>",
  "Współczesne bloki, <em>otwarte na morze</em>", "Moderne bygg, <em>åpne mot havet</em>", "Moderna hus, <em>öppna mot havet</em>")
a('The developer describes contemporary architecture',
  "El promotor describe una arquitectura contemporánea de líneas elegantes y grandes terrazas privadas que prolongan la vivienda hacia el exterior. En las fotografías, los bloques se escalonan en terrazas blancas con barandillas de vidrio, orientados al Mediterráneo.",
  "Le promoteur décrit une architecture contemporaine aux lignes élégantes et de grandes terrasses privées qui prolongent le logement vers l’extérieur. Sur les photographies, les blocs s’étagent en terrasses blanches à garde-corps en verre, face à la Méditerranée.",
  "Der Bauträger beschreibt eine zeitgenössische Architektur mit eleganten Linien und großen privaten Terrassen, die die Wohnung nach außen verlängern. Auf den Fotos staffeln sich die Blöcke in weißen Terrassen mit Glasbrüstungen zum Mittelmeer hin.",
  "Застройщик описывает современную архитектуру с элегантными линиями и большими частными террасами, продолжающими квартиру на улицу. На фотографиях корпуса поднимаются белыми террасами со стеклянными ограждениями, обращёнными к Средиземному морю.",
  "يصف المطوّر عمارة معاصرة بخطوط أنيقة وتراسات خاصة واسعة تمتد بالمسكن إلى الخارج. وتظهر في الصور المباني متدرجة بتراسات بيضاء وحواجز زجاجية مطلّة على البحر المتوسط.",
  "De ontwikkelaar beschrijft een eigentijdse architectuur met elegante lijnen en grote privéterrassen die de woning naar buiten verlengen. Op de foto’s lopen de blokken getrapt af in witte terrassen met glazen balustrades, gericht op de Middellandse Zee.",
  "Deweloper opisuje współczesną architekturę o eleganckich liniach i duże prywatne tarasy, które przedłużają mieszkanie na zewnątrz. Na zdjęciach bloki schodzą białymi tarasami ze szklanymi balustradami, zwrócone ku Morzu Śródziemnemu.",
  "Utbyggeren beskriver en moderne arkitektur med elegante linjer og store private terrasser som forlenger boligen utendørs. På bildene trapper byggene seg ned i hvite terrasser med glassrekkverk, vendt mot Middelhavet.",
  "Exploatören beskriver en modern arkitektur med eleganta linjer och stora privata terrasser som förlänger bostaden utomhus. På bilderna trappar husen av i vita terrasser med glasräcken, vända mot Medelhavet.")
a('The homes are in Blocks 1, 2 and 3',
  "Las viviendas están en los Bloques 1, 2 y 3, en la planta baja, la primera y la segunda, y en áticos en la cuarta planta.",
  "Les logements se trouvent dans les blocs 1, 2 et 3, au rez-de-chaussée, au premier et au deuxième étage, et en penthouses au quatrième étage.",
  "Die Wohnungen liegen in den Blöcken 1, 2 und 3, im Erdgeschoss sowie im ersten und zweiten Obergeschoss und als Penthouses im vierten Obergeschoss.",
  "Квартиры находятся в блоках 1, 2 и 3 — на первом, втором и третьем этажах, а пентхаусы — на пятом этаже.",
  "تقع المساكن في المباني 1 و2 و3، في الطابق الأرضي والأول والثاني، وفي بنتهاوس بالطابق الرابع.",
  "De woningen liggen in blok 1, 2 en 3, op de begane grond, de eerste en de tweede verdieping, en als penthouses op de vierde verdieping.",
  "Mieszkania znajdują się w blokach 1, 2 i 3, na parterze oraz na pierwszym i drugim piętrze, a penthouse’y na czwartym piętrze.",
  "Boligene ligger i Hus 1, 2 og 3, i første, andre og tredje etasje, og som toppleiligheter i femte etasje.",
  "Bostäderna ligger i Hus 1, 2 och 3, på bottenvåningen samt första och andra våningen, och som takvåningar på fjärde våningen.")
a('Contemporary architecture with elegant lines, in the developer’s words.',
  "Arquitectura contemporánea de líneas elegantes, según el promotor.", "Une architecture contemporaine aux lignes élégantes, selon le promoteur.",
  "Zeitgenössische Architektur mit eleganten Linien, so der Bauträger.", "Современная архитектура с элегантными линиями — по словам застройщика.",
  "عمارة معاصرة بخطوط أنيقة، بحسب وصف المطوّر.", "Eigentijdse architectuur met elegante lijnen, in de woorden van de ontwikkelaar.",
  "Współczesna architektura o eleganckich liniach, według dewelopera.", "Moderne arkitektur med elegante linjer, med utbyggerens ord.",
  "Modern arkitektur med eleganta linjer, med exploatörens ord.")
a('Large private terraces, with the covered and uncovered parts measured separately on each plan.',
  "Grandes terrazas privadas, con la parte cubierta y la descubierta medidas por separado en cada plano.",
  "De grandes terrasses privées, dont la partie couverte et la partie découverte sont mesurées séparément sur chaque plan.",
  "Große private Terrassen, deren überdachter und offener Teil in jedem Grundriss getrennt ausgewiesen ist.",
  "Большие частные террасы; крытая и открытая части измерены на каждом плане отдельно.",
  "تراسات خاصة واسعة، يُقاس الجزء المسقوف والجزء المكشوف منها بشكل منفصل في كل مخطط.",
  "Grote privéterrassen, waarvan het overdekte en het open deel op elke plattegrond apart zijn gemeten.",
  "Duże prywatne tarasy, na rzutach których część zadaszona i odkryta są podane osobno.",
  "Store private terrasser, der den overbygde og den åpne delen er målt hver for seg på hver plantegning.",
  "Stora privata terrasser, där den övertäckta och den öppna delen är mätta var för sig på varje planritning.")
a('Three ground-floor homes, 10A, 20B and 30A',
  "Tres viviendas de planta baja, la 10A, la 20B y la 30A, tienen una piscina privada dibujada en la terraza de su plano.",
  "Trois logements en rez-de-chaussée, le 10A, le 20B et le 30A, ont une piscine privée dessinée sur la terrasse de leur plan.",
  "Drei Erdgeschosswohnungen, 10A, 20B und 30A, haben einen privaten Pool, der im Grundriss auf der Terrasse eingezeichnet ist.",
  "У трёх квартир на первом этаже — 10A, 20B и 30A — на плане террасы нарисован частный бассейн.",
  "ثلاثة مساكن في الطابق الأرضي، وهي 10A و20B و30A، فيها مسبح خاص مرسوم على التراس في مخططها.",
  "Drie woningen op de begane grond, 10A, 20B en 30A, hebben een privézwembad dat op het terras van hun plattegrond is getekend.",
  "Trzy mieszkania na parterze, 10A, 20B i 30A, mają prywatny basen narysowany na tarasie na ich rzucie.",
  "Tre boliger i første etasje, 10A, 20B og 30A, har et privat basseng tegnet inn på terrassen på plantegningen.",
  "Tre bostäder på bottenvåningen, 10A, 20B och 30A, har en privat pool inritad på terrassen på planritningen.")
a('Views', "Vistas", "Vues", "Aussicht", "Виды", "الإطلالات", "Uitzicht", "Widoki", "Utsikt")
a('Sea views, which the brochure calls panoramic Mediterranean views.',
  "Vistas al mar, que el folleto describe como vistas panorámicas al Mediterráneo.", "Une vue sur la mer, que la brochure qualifie de vue panoramique sur la Méditerranée.",
  "Meerblick, den die Broschüre als Panoramablick auf das Mittelmeer beschreibt.", "Вид на море, который в брошюре назван панорамным видом на Средиземное море.",
  "إطلالات على البحر، يصفها الكتيّب بأنها إطلالات بانورامية على البحر المتوسط.", "Zeezicht, dat de brochure een panoramisch uitzicht op de Middellandse Zee noemt.",
  "Widok na morze, który broszura nazywa panoramicznym widokiem na Morze Śródziemne.", "Havutsikt, som brosjyren kaller panoramautsikt over Middelhavet.",
  "Havsutsikt, som broschyren kallar panoramautsikt över Medelhavet.")

# ------------------------------------------------------------------ residences, lifestyle
a('Eight homes, <em>ground floor to penthouse</em>',
  "Ocho viviendas, <em>de la planta baja al ático</em>", "Huit logements, <em>du rez-de-chaussée au penthouse</em>", "Acht Wohnungen, <em>vom Erdgeschoss bis zum Penthouse</em>",
  "Восемь квартир, <em>от первого этажа до пентхауса</em>", "ثمانية مساكن، <em>من الطابق الأرضي إلى البنتهاوس</em>", "Acht woningen, <em>van begane grond tot penthouse</em>",
  "Osiem mieszkań, <em>od parteru po penthouse</em>", "Åtte boliger, <em>fra første etasje til toppleilighet</em>", "Åtta bostäder, <em>från bottenvåning till takvåning</em>")
a('Five homes have three bedrooms and three have two.',
  "Cinco viviendas tienen tres dormitorios y tres tienen dos. Las tres viviendas de planta baja con tres dormitorios tienen las terrazas más grandes y una piscina privada en el plano, y los áticos están en la cuarta planta de los Bloques 2 y 3.",
  "Cinq logements ont trois chambres et trois en ont deux. Les trois logements de rez-de-chaussée à trois chambres ont les plus grandes terrasses et une piscine privée sur le plan, et les penthouses se trouvent au quatrième étage des blocs 2 et 3.",
  "Fünf Wohnungen haben drei Schlafzimmer, drei haben zwei. Die drei Erdgeschosswohnungen mit drei Schlafzimmern haben die größten Terrassen und im Grundriss einen privaten Pool, und die Penthouses liegen im vierten Obergeschoss der Blöcke 2 und 3.",
  "У пяти квартир три спальни, у трёх — две. Три трёхспальные квартиры на первом этаже имеют самые большие террасы и частный бассейн на плане, а пентхаусы расположены на пятом этаже блоков 2 и 3.",
  "خمسة من المساكن بثلاث غرف نوم وثلاثة بغرفتي نوم. أما المساكن الثلاثة ذات الغرف الثلاث في الطابق الأرضي فلها أكبر التراسات ومسبح خاص مرسوم في المخطط، وتقع البنتهاوسات في الطابق الرابع من المبنيين 2 و3.",
  "Vijf woningen hebben drie slaapkamers en drie hebben er twee. De drie woningen met drie slaapkamers op de begane grond hebben de grootste terrassen en een privézwembad op de plattegrond, en de penthouses liggen op de vierde verdieping van blok 2 en 3.",
  "Pięć mieszkań ma trzy sypialnie, a trzy mają dwie. Trzy trzysypialniowe mieszkania na parterze mają największe tarasy i prywatny basen na rzucie, a penthouse’y znajdują się na czwartym piętrze bloków 2 i 3.",
  "Fem boliger har tre soverom og tre har to. De tre treromsboligene i første etasje har de største terrassene og et privat basseng på plantegningen, og toppleilighetene ligger i femte etasje i Hus 2 og 3.",
  "Fem bostäder har tre sovrum och tre har två. De tre bostäderna med tre sovrum på bottenvåningen har de största terrasserna och en privat pool på planritningen, och takvåningarna ligger på fjärde våningen i Hus 2 och 3.")
a('Pools, <em>a gym</em> and the coast around',
  "Piscinas, <em>un gimnasio</em> y la costa alrededor", "Des piscines, <em>une salle de sport</em> et la côte alentour", "Pools, <em>ein Fitnessraum</em> und die Küste ringsum",
  "Бассейны, <em>тренажёрный зал</em> и побережье вокруг", "مسابح، <em>وصالة رياضية</em> والساحل من حولها", "Zwembaden, <em>een gym</em> en de kust eromheen",
  "Baseny, <em>siłownia</em> i wybrzeże wokół", "Basseng, <em>treningsrom</em> og kysten rundt", "Pooler, <em>ett gym</em> och kusten runt omkring")
a('The developer lists the shared facilities below',
  "El promotor enumera las zonas comunes que se indican abajo, y las fotografías muestran la piscina, la piscina interior y el gimnasio ya construidos.",
  "Le promoteur liste les espaces communs ci-dessous, et les photographies montrent la piscine, la piscine intérieure et la salle de sport telles que construites.",
  "Der Bauträger führt die untenstehenden Gemeinschaftsbereiche auf, und die Fotos zeigen den Pool, den Innenpool und den Fitnessraum, wie sie gebaut sind.",
  "Застройщик перечисляет общие зоны ниже, а на фотографиях бассейн, крытый бассейн и тренажёрный зал показаны в том виде, в каком они построены.",
  "يذكر المطوّر المرافق المشتركة أدناه، وتُظهر الصور المسبح والمسبح الداخلي والصالة الرياضية كما بُنيت.",
  "De ontwikkelaar noemt hieronder de gedeelde voorzieningen, en de foto’s tonen het zwembad, het binnenzwembad en de gym zoals ze zijn gebouwd.",
  "Deweloper wymienia poniżej udogodnienia wspólne, a zdjęcia pokazują basen, basen wewnętrzny i siłownię w stanie, w jakim zostały zbudowane.",
  "Utbyggeren oppgir fellesfasilitetene nedenfor, og bildene viser bassenget, innendørsbassenget og treningsrommet slik de er bygget.",
  "Exploatören anger de gemensamma bekvämligheterna nedan, och bilderna visar poolen, inomhuspoolen och gymmet som de är byggda.")
a('An outdoor pool and a heated indoor pool, with a sauna',
  "Una piscina exterior y una piscina interior climatizada; en la fotografía se ve una sauna junto a la piscina interior.",
  "Une piscine extérieure et une piscine intérieure chauffée ; sur la photographie, on voit un sauna à côté de la piscine intérieure.",
  "Ein Außenpool und ein beheizter Innenpool; auf dem Foto ist neben dem Innenpool eine Sauna zu sehen.",
  "Открытый бассейн и крытый подогреваемый бассейн; на фотографии рядом с крытым бассейном видна сауна.",
  "مسبح خارجي ومسبح داخلي مُدفّأ، وتظهر في الصورة ساونا بجانب المسبح الداخلي.",
  "Een buitenzwembad en een verwarmd binnenzwembad; op de foto is naast het binnenzwembad een sauna te zien.",
  "Basen zewnętrzny i ogrzewany basen wewnętrzny; na zdjęciu obok basenu wewnętrznego widać saunę.",
  "Et utendørs basseng og et oppvarmet innendørs basseng; på bildet ses en badstue ved siden av innendørsbassenget.",
  "En utomhuspool och en uppvärmd inomhuspool; på fotografiet syns en bastu bredvid inomhuspoolen.")
a('A gym with cardio and weights equipment',
  "Un gimnasio con equipos de cardio y de pesas y un espacio de coworking, ambos indicados por el promotor.",
  "Une salle de sport avec des appareils de cardio et de musculation et un espace de coworking, tous deux indiqués par le promoteur.",
  "Ein Fitnessraum mit Cardio- und Kraftgeräten und ein Coworking-Bereich, beides vom Bauträger aufgeführt.",
  "Тренажёрный зал с кардио- и силовым оборудованием и коворкинг — оба указаны застройщиком.",
  "صالة رياضية بأجهزة كارديو وأثقال ومساحة عمل مشتركة، وكلاهما مذكور لدى المطوّر.",
  "Een gym met cardio- en krachtapparatuur en een coworkingruimte, beide door de ontwikkelaar vermeld.",
  "Siłownia ze sprzętem do cardio i ćwiczeń siłowych oraz przestrzeń coworkingowa, obie wymienione przez dewelopera.",
  "Et treningsrom med kondisjons- og styrkeutstyr og et coworking-område, begge oppgitt av utbyggeren.",
  "Ett gym med kondition- och styrkeutrustning och en coworkingyta, båda angivna av exploatören.")
a('Social room and gardens', "Sala social y jardines", "Salon commun et jardins", "Gemeinschaftsraum und Gärten", "Общий зал и сады", "القاعة الاجتماعية والحدائق", "Gemeenschappelijke ruimte en tuinen", "Sala towarzyska i ogrody", "Felles oppholdsrom og hager")
a('A social room and gardens are listed by the developer',
  "El promotor indica una sala social y jardines, y se puede visitar el piso piloto.",
  "Le promoteur indique un salon commun et des jardins, et l’appartement témoin peut être visité.",
  "Der Bauträger führt einen Gemeinschaftsraum und Gärten auf, und die Musterwohnung kann besichtigt werden.",
  "Застройщик указывает общий зал и сады, а демонстрационную квартиру можно посмотреть.",
  "يذكر المطوّر قاعة اجتماعية وحدائق، ويمكن زيارة الشقة النموذجية.",
  "De ontwikkelaar vermeldt een gemeenschappelijke ruimte en tuinen, en het showappartement kan worden bezichtigd.",
  "Deweloper wymienia salę towarzyską i ogrody, a lokal pokazowy można zwiedzić.",
  "Utbyggeren oppgir et felles oppholdsrom og hager, og visningsleiligheten kan besøkes.",
  "Exploatören anger ett gemensamt rum och trädgårdar, och visningslägenheten kan besökas.")
a('Beaches and golf', "Playas y golf", "Plages et golf", "Strände und Golf", "Пляжи и гольф", "الشواطئ والغولف", "Stranden en golf", "Plaże i golf", "Strender og golf")
a('The developer’s map marks Carvajal',
  "El mapa del promotor señala las playas de Carvajal, Torreblanca, Fuengirola y Torremuelle y seis campos de golf alrededor de la promoción, sin indicar distancias.",
  "La carte du promoteur indique les plages de Carvajal, Torreblanca, Fuengirola et Torremuelle et six terrains de golf autour du site, sans donner de distances.",
  "Die Karte des Bauträgers verzeichnet die Strände Carvajal, Torreblanca, Fuengirola und Torremuelle sowie sechs Golfplätze rund um die Anlage, ohne Entfernungen anzugeben.",
  "На карте застройщика вокруг комплекса отмечены пляжи Карвахаль, Торребланка, Фуэнхирола и Торремуэлье и шесть полей для гольфа, расстояния не указаны.",
  "تحدد خريطة المطوّر شواطئ كارفاخال وتوريبلانكا وفوينخيرولا وتوريموييه وستة ملاعب غولف حول المشروع، دون ذكر المسافات.",
  "De kaart van de ontwikkelaar toont de stranden van Carvajal, Torreblanca, Fuengirola en Torremuelle en zes golfbanen rond het project, zonder afstanden te vermelden.",
  "Mapa dewelopera zaznacza plaże Carvajal, Torreblanca, Fuengirola i Torremuelle oraz sześć pól golfowych wokół inwestycji, bez podawania odległości.",
  "Utbyggerens kart markerer strendene Carvajal, Torreblanca, Fuengirola og Torremuelle og seks golfbaner rundt prosjektet, uten å oppgi avstander.",
  "Exploatörens karta markerar stränderna Carvajal, Torreblanca, Fuengirola och Torremuelle och sex golfbanor runt projektet, utan att ange avstånd.")

# ------------------------------------------------------------------ location
a('El Higuerón, <em>between Fuengirola and Benalmádena</em>',
  "El Higuerón, <em>entre Fuengirola y Benalmádena</em>", "El Higuerón, <em>entre Fuengirola et Benalmádena</em>", "El Higuerón, <em>zwischen Fuengirola und Benalmádena</em>",
  "Эль-Игерон, <em>между Фуэнхиролой и Бенальмаденой</em>", "إل إيغيرون، <em>بين فوينخيرولا وبينالمادينا</em>", "El Higuerón, <em>tussen Fuengirola en Benalmádena</em>",
  "El Higuerón, <em>między Fuengirolą a Benalmádeną</em>", "El Higuerón, <em>mellom Fuengirola og Benalmádena</em>", "El Higuerón, <em>mellan Fuengirola och Benalmádena</em>")
a('The developer’s portal places the homes at El Higuerón',
  "El portal del promotor sitúa las viviendas en El Higuerón, entre Fuengirola y Benalmádena. En su mapa, la promoción queda junto a la AP-7, con Mijas al oeste, el aeropuerto de Málaga al noreste y Marbella señalada a 20 km.",
  "Le portail du promoteur situe les logements à El Higuerón, entre Fuengirola et Benalmádena. Sur sa carte, le site se trouve près de l’AP-7, avec Mijas à l’ouest, l’aéroport de Malaga au nord-est et Marbella indiquée à 20 km.",
  "Das Portal des Bauträgers verortet die Wohnungen in El Higuerón, zwischen Fuengirola und Benalmádena. Auf seiner Karte liegt die Anlage neben der AP-7, mit Mijas im Westen, dem Flughafen Málaga im Nordosten und Marbella mit 20 km Entfernung.",
  "Портал застройщика размещает квартиры в Эль-Игероне, между Фуэнхиролой и Бенальмаденой. На его карте комплекс находится рядом с автострадой AP-7: Михас — к западу, аэропорт Малаги — к северо-востоку, а Марбелья отмечена в 20 км.",
  "يضع موقع المطوّر المساكن في إل إيغيرون بين فوينخيرولا وبينالمادينا. وعلى خريطته يقع المشروع بجوار الطريق السريع AP-7، مع ميخاس إلى الغرب ومطار مالقة إلى الشمال الشرقي، وتظهر ماربيا على بُعد 20 كم.",
  "Het portaal van de ontwikkelaar plaatst de woningen in El Higuerón, tussen Fuengirola en Benalmádena. Op zijn kaart ligt het project naast de AP-7, met Mijas in het westen, de luchthaven van Málaga in het noordoosten en Marbella aangegeven op 20 km.",
  "Portal dewelopera umieszcza mieszkania w El Higuerón, między Fuengirolą a Benalmádeną. Na jego mapie inwestycja leży obok autostrady AP-7, z Mijas na zachodzie, lotniskiem w Maladze na północnym wschodzie i Marbellą oznaczoną w odległości 20 km.",
  "Utbyggerens portal plasserer boligene i El Higuerón, mellom Fuengirola og Benalmádena. På kartet ligger prosjektet ved siden av AP-7, med Mijas i vest, Málaga lufthavn i nordøst og Marbella markert 20 km unna.",
  "Exploatörens portal placerar bostäderna i El Higuerón, mellan Fuengirola och Benalmádena. På dess karta ligger projektet bredvid AP-7, med Mijas i väster, Málagas flygplats i nordost och Marbella markerad 20 km bort.")
a('El Higuerón, <em>Costa del Sol</em>',
  "El Higuerón, <em>Costa del Sol</em>", "El Higuerón, <em>Costa del Sol</em>", "El Higuerón, <em>Costa del Sol</em>", "Эль-Игерон, <em>Коста-дель-Соль</em>",
  "إل إيغيرون، <em>كوستا ديل سول</em>", "El Higuerón, <em>Costa del Sol</em>", "El Higuerón, <em>Costa del Sol</em>", "El Higuerón, <em>Costa del Sol</em>", "El Higuerón, <em>Costa del Sol</em>")
a('El Higuerón, Costa del Sol',
  "El Higuerón, Costa del Sol", "El Higuerón, Costa del Sol", "El Higuerón, Costa del Sol", "Эль-Игерон, Коста-дель-Соль",
  "إل إيغيرون، كوستا ديل سول", "El Higuerón, Costa del Sol", "El Higuerón, Costa del Sol", "El Higuerón, Costa del Sol", "El Higuerón, Costa del Sol")
a('20 km, as marked on the developer’s map',
  "20 km, según el mapa del promotor", "20 km, selon la carte du promoteur", "20 km, laut Karte des Bauträgers", "20 км по карте застройщика",
  "20 كم بحسب خريطة المطوّر", "20 km, volgens de kaart van de ontwikkelaar", "20 km, według mapy dewelopera", "20 km, ifølge utbyggerens kart", "20 km, enligt exploatörens karta")
a('Described as a few minutes away; no figure given',
  "Descrito como a pocos minutos; no se indica ninguna cifra", "Décrit comme à quelques minutes ; aucun chiffre n’est donné",
  "Als wenige Minuten entfernt beschrieben; keine Angabe", "Описан как находящийся в нескольких минутах; точных данных нет",
  "موصوف بأنه على بُعد دقائق قليلة؛ دون ذكر رقم", "Omschreven als enkele minuten verwijderd; er wordt geen cijfer genoemd",
  "Opisane jako kilka minut stąd; bez podania wartości", "Beskrevet som noen minutter unna; ingen tall oppgis", "Beskrivet som några minuter bort; inget exakt värde anges")

# ------------------------------------------------------------------ purchase, checks
a('The developer’s documents do not set out payment terms',
  "Los documentos del promotor no recogen las condiciones de pago, por lo que las solicitamos y confirmamos por escrito los importes y plazos vigentes antes de que reserve.",
  "Les documents du promoteur ne précisent pas les conditions de paiement ; nous les demandons et nous confirmons par écrit les montants et les dates en vigueur avant que vous ne réserviez.",
  "Die Unterlagen des Bauträgers nennen keine Zahlungsbedingungen; wir fragen sie an und bestätigen Ihnen die aktuellen Beträge und Termine schriftlich, bevor Sie reservieren.",
  "В документах застройщика условия оплаты не указаны, поэтому мы запрашиваем их и письменно подтверждаем действующие суммы и сроки до того, как вы забронируете.",
  "لا تتضمن وثائق المطوّر شروط الدفع، لذلك نطلبها ونؤكد لكم كتابةً المبالغ والمواعيد السارية قبل أن تحجزوا.",
  "De documenten van de ontwikkelaar vermelden geen betalingsvoorwaarden; wij vragen ze op en bevestigen de actuele bedragen en data schriftelijk voordat u reserveert.",
  "Dokumenty dewelopera nie podają warunków płatności, dlatego o nie pytamy i przed rezerwacją potwierdzamy na piśmie aktualne kwoty i terminy.",
  "Utbyggerens dokumenter oppgir ikke betalingsvilkår, så vi ber om dem og bekrefter gjeldende beløp og datoer skriftlig før noen reserverer.",
  "Exploatörens dokument anger inga betalningsvillkor, så vi begär dem och bekräftar gällande belopp och datum skriftligen innan ni reserverar.")
a('Prices', "Precios", "Prix", "Preise", "Цены", "الأسعار", "Prijzen", "Ceny", "Priser")
a('The prices are those of the developer’s portal',
  "Los precios son los del portal del promotor, y los documentos no indican si el IVA y los gastos de compra están incluidos. Lo confirmamos por escrito.",
  "Les prix sont ceux du portail du promoteur, et les documents n’indiquent pas si la TVA et les frais d’achat sont inclus. Nous le confirmons par écrit.",
  "Die Preise stammen aus dem Portal des Bauträgers, und die Unterlagen geben nicht an, ob MwSt. und Erwerbsnebenkosten enthalten sind. Wir bestätigen dies schriftlich.",
  "Цены взяты с портала застройщика, а в документах не сказано, включены ли НДС и расходы на покупку. Мы подтверждаем это письменно.",
  "الأسعار هي أسعار موقع المطوّر، ولا تذكر الوثائق ما إذا كانت ضريبة القيمة المضافة وتكاليف الشراء مشمولة. نؤكد ذلك كتابةً.",
  "De prijzen zijn die van het portaal van de ontwikkelaar, en de documenten vermelden niet of btw en aankoopkosten zijn inbegrepen. Wij bevestigen dit schriftelijk.",
  "Ceny pochodzą z portalu dewelopera, a dokumenty nie podają, czy VAT i koszty zakupu są wliczone. Potwierdzamy to na piśmie.",
  "Prisene er de fra utbyggerens portal, og dokumentene oppgir ikke om mva og kjøpskostnader er inkludert. Vi bekrefter dette skriftlig.",
  "Priserna är de från exploatörens portal, och dokumenten anger inte om moms och köpkostnader ingår. Vi bekräftar detta skriftligen.")
a('Furniture and decoration', "Mobiliario y decoración", "Mobilier et décoration", "Möbel und Dekoration", "Мебель и декор", "الأثاث والديكور", "Meubilair en decoratie", "Meble i dekoracje", "Møbler og dekor")
a('The developer’s notice says the furniture, decorative items',
  "El aviso del promotor indica que el mobiliario, los elementos decorativos y el paisajismo de sus imágenes no están incluidos en el precio de la vivienda.",
  "L’avis du promoteur précise que le mobilier, les éléments décoratifs et l’aménagement paysager de ses images ne sont pas inclus dans le prix du logement.",
  "Laut dem Hinweis des Bauträgers sind Möbel, Dekorationselemente und Landschaftsgestaltung in seinen Bildern nicht im Preis der Wohnung enthalten.",
  "В уведомлении застройщика сказано, что мебель, декоративные элементы и благоустройство на его изображениях в цену квартиры не входят.",
  "يذكر إشعار المطوّر أن الأثاث والعناصر الزخرفية وتنسيق الحدائق في صوره غير مشمولة في سعر المسكن.",
  "Volgens de mededeling van de ontwikkelaar zijn het meubilair, de decoratieve elementen en de landschapsinrichting op zijn beelden niet in de prijs van de woning inbegrepen.",
  "Według zawiadomienia dewelopera meble, elementy dekoracyjne i zagospodarowanie terenu na jego obrazach nie są wliczone w cenę mieszkania.",
  "Utbyggerens merknad sier at møbler, dekorelementer og landskapsutforming på bildene ikke er inkludert i prisen på boligen.",
  "Exploatörens meddelande säger att möbler, dekorationselement och landskapsutformning i dess bilder inte ingår i bostadens pris.")
a('The documents do not say whether a parking space',
  "Los documentos no indican si cada vivienda incluye una plaza de aparcamiento o un trastero. Confirmamos qué está incluido.",
  "Les documents n’indiquent pas si une place de stationnement ou un débarras est fourni avec chaque logement. Nous confirmons ce qui est inclus.",
  "Die Unterlagen geben nicht an, ob zu jeder Wohnung ein Stellplatz oder ein Abstellraum gehört. Wir bestätigen, was enthalten ist.",
  "В документах не сказано, входят ли в каждую квартиру парковочное место или кладовая. Мы уточняем, что включено.",
  "لا تذكر الوثائق ما إذا كان مع كل مسكن موقف سيارات أو مخزن. نؤكد ما هو مشمول.",
  "De documenten vermelden niet of er bij elke woning een parkeerplaats of een berging hoort. Wij bevestigen wat is inbegrepen.",
  "Dokumenty nie podają, czy do każdego mieszkania należy miejsce parkingowe lub komórka lokatorska. Potwierdzamy, co jest wliczone.",
  "Dokumentene oppgir ikke om hver bolig har en parkeringsplass eller en bod. Vi bekrefter hva som er inkludert.",
  "Dokumenten anger inte om varje bostad har en parkeringsplats eller ett förråd. Vi bekräftar vad som ingår.")
a('Reservation and guarantee', "Reserva y garantía", "Réservation et garantie", "Reservierung und Absicherung", "Бронирование и гарантия", "الحجز والضمان", "Reservering en garantie", "Rezerwacja i gwarancja", "Reservasjon og garanti")
a('No reservation amount or schedule is given.',
  "No se indica ningún importe de reserva ni calendario de pagos. Los solicitamos, y también cómo se garantiza cada pago a través de un banco, antes de efectuar cualquier pago.",
  "Aucun montant de réservation ni calendrier n’est indiqué. Nous les demandons, ainsi que la manière dont chaque paiement est garanti par une banque, avant tout paiement.",
  "Weder ein Reservierungsbetrag noch ein Zahlungsplan wird genannt. Wir fragen beides an, ebenso wie jede Zahlung über eine Bank abgesichert wird, bevor eine Zahlung erfolgt.",
  "Ни сумма бронирования, ни график платежей не указаны. Мы запрашиваем их, а также способ банковской гарантии платежей, до любой оплаты.",
  "لا يُذكر مبلغ حجز ولا جدول دفعات. نطلب ذلك، وكذلك كيفية ضمان أي دفعة عبر بنك، قبل أي دفعة.",
  "Er wordt geen reserveringsbedrag of betalingsschema genoemd. Wij vragen dat op, en ook hoe elke betaling via een bank is gewaarborgd, vóór enige betaling.",
  "Nie podano kwoty rezerwacji ani harmonogramu płatności. Pytamy o nie oraz o to, jak każda wpłata jest zabezpieczona przez bank, przed jakąkolwiek wpłatą.",
  "Verken reservasjonsbeløp eller betalingsplan oppgis. Vi ber om dem, og om hvordan hver betaling garanteres gjennom en bank, før noen betaling.",
  "Varken reservationsbelopp eller betalningsplan anges. Vi begär dem, och hur varje betalning garanteras via en bank, före någon betalning.")
a('Completion and certificates', "Finalización y certificados", "Achèvement et certificats", "Fertigstellung und Bescheinigungen", "Завершение и сертификаты", "الإنجاز والشهادات", "Oplevering en certificaten", "Ukończenie i certyfikaty", "Ferdigstillelse og sertifikater")
a('The brochure and the portal both describe the homes as completed',
  "El folleto y el portal describen las viviendas como terminadas, pero ninguno indica una fecha de finalización ni menciona una licencia. Solicitamos la licencia de primera ocupación y el certificado energético de la vivienda que elija.",
  "La brochure et le portail décrivent tous deux les logements comme achevés, mais aucun n’indique de date d’achèvement ni ne mentionne de licence. Nous demandons la licence de première occupation et le certificat énergétique du logement que vous choisissez.",
  "Broschüre und Portal beschreiben die Wohnungen beide als fertiggestellt, nennen aber weder ein Fertigstellungsdatum noch eine Genehmigung. Wir fragen die Erstbezugsgenehmigung und den Energieausweis der von Ihnen gewählten Wohnung an.",
  "И брошюра, и портал описывают квартиры как завершённые, но ни там, ни там нет даты завершения и не упомянута лицензия. Мы запрашиваем лицензию на первое заселение и энергетический сертификат выбранной вами квартиры.",
  "يصف الكتيّب والموقع الإلكتروني المساكن بأنها مكتملة، لكن أياً منهما لا يذكر تاريخ الإنجاز ولا رخصة. نطلب رخصة الإشغال الأولى وشهادة الطاقة للمسكن الذي تختارونه.",
  "De brochure en het portaal beschrijven de woningen allebei als opgeleverd, maar geen van beide noemt een opleverdatum of vermeldt een vergunning. Wij vragen de vergunning voor eerste ingebruikname en het energiecertificaat van de woning van uw keuze op.",
  "Broszura i portal opisują mieszkania jako ukończone, ale żadne z nich nie podaje daty ukończenia ani nie wspomina o pozwoleniu. Prosimy o pozwolenie na pierwsze zamieszkanie i świadectwo energetyczne wybranego mieszkania.",
  "Brosjyren og portalen beskriver begge boligene som ferdigstilte, men ingen av dem oppgir en ferdigstillelsesdato eller nevner en tillatelse. Vi ber om tillatelsen til første bruk og energisertifikatet for den boligen som velges.",
  "Broschyren och portalen beskriver båda bostäderna som färdiga, men ingen av dem anger ett färdigställandedatum eller nämner ett tillstånd. Vi begär tillståndet för första ibruktagande och energicertifikatet för den bostad som väljs.")
a('Two terrace areas', "Dos superficies de terraza", "Deux surfaces de terrasse", "Zwei Terrassenflächen", "Две площади террас", "مساحتا تراسين", "Twee terrasoppervlaktes", "Dwie powierzchnie tarasów", "To terrasseareal")
a('The price list gives the terraces of home 24A',
  "La lista de precios indica para las terrazas de la vivienda 24A {N44.47} {U} y para las de la 20B {N117.29} {U}; los planos indican {N46.47} y {N177.29} {U}. Confirmamos qué cifras utiliza el contrato.",
  "La liste de prix indique pour les terrasses du logement 24A {N44.47} {U} et pour celles du 20B {N117.29} {U} ; les plans indiquent {N46.47} et {N177.29} {U}. Nous confirmons quels chiffres le contrat retient.",
  "Die Preisliste nennt für die Terrassen der Wohnung 24A {N44.47} {U} und für die der 20B {N117.29} {U}; die Grundrisse nennen {N46.47} und {N177.29} {U}. Wir klären, welche Werte der Vertrag verwendet.",
  "В прайс-листе площадь террас квартиры 24A указана как {N44.47} {U}, а квартиры 20B — {N117.29} {U}; на планах — {N46.47} и {N177.29} {U}. Мы уточняем, какие цифры использует договор.",
  "تذكر قائمة الأسعار مساحة تراسات المسكن 24A بـ {N44.47} {U} والمسكن 20B بـ {N117.29} {U}، بينما تذكر المخططات {N46.47} و{N177.29} {U}. نؤكد أي الأرقام يعتمدها العقد.",
  "De prijslijst noemt voor de terrassen van woning 24A {N44.47} {U} en voor die van 20B {N117.29} {U}; de plattegronden noemen {N46.47} en {N177.29} {U}. Wij bevestigen welke cijfers het contract hanteert.",
  "Cennik podaje dla tarasów mieszkania 24A {N44.47} {U}, a dla 20B {N117.29} {U}; rzuty podają {N46.47} i {N177.29} {U}. Potwierdzamy, których wartości używa umowa.",
  "Prislisten oppgir {N44.47} {U} for terrassene i bolig 24A og {N117.29} {U} for 20B; plantegningene oppgir {N46.47} og {N177.29} {U}. Vi bekrefter hvilke tall kontrakten bruker.",
  "Prislistan anger {N44.47} {U} för terrasserna i bostad 24A och {N117.29} {U} för 20B; planritningarna anger {N46.47} och {N177.29} {U}. Vi bekräftar vilka siffror avtalet använder.")
a('Which area counts', "Qué superficie cuenta", "Quelle surface compte", "Welche Fläche zählt", "Какая площадь считается", "أي مساحة تُحتسب", "Welke oppervlakte telt", "Która powierzchnia się liczy", "Hvilket areal som teller")
a('The built area on the price list is the decree 218/2005 figure',
  "La superficie construida de la lista de precios es la cifra del Decreto 218/2005 que figura en cada plano, y la superficie interior es otra cifra, menor. Confirmamos cuál utiliza el contrato.",
  "La surface construite de la liste de prix est le chiffre du décret 218/2005 figurant sur chaque plan, et la surface intérieure est un autre chiffre, plus petit. Nous confirmons lequel le contrat retient.",
  "Die bebaute Fläche der Preisliste ist der Wert nach Dekret 218/2005 aus dem jeweiligen Grundriss, und die Innenfläche ist ein anderer, kleinerer Wert. Wir klären, welcher im Vertrag gilt.",
  "Площадь застройки в прайс-листе — это значение по декрету 218/2005 с каждого плана, а внутренняя площадь — другое, меньшее значение. Мы уточняем, какое из них используется в договоре.",
  "المساحة المبنية في قائمة الأسعار هي رقم المرسوم 218/2005 المذكور في كل مخطط، أما المساحة الداخلية فرقم آخر أصغر. نؤكد أيهما يعتمده العقد.",
  "De bebouwde oppervlakte in de prijslijst is het cijfer volgens decreet 218/2005 op elke plattegrond, en de binnenoppervlakte is een ander, kleiner cijfer. Wij bevestigen welke het contract hanteert.",
  "Powierzchnia zabudowy w cenniku to wartość według dekretu 218/2005 z każdego rzutu, a powierzchnia wewnętrzna to inna, mniejsza wartość. Potwierdzamy, której używa umowa.",
  "Bygd areal i prislisten er tallet etter dekret 218/2005 fra hver plantegning, og det innvendige arealet er et annet, mindre tall. Vi bekrefter hvilket kontrakten bruker.",
  "Byggytan i prislistan är siffran enligt dekret 218/2005 från varje planritning, och den invändiga ytan är en annan, mindre siffra. Vi bekräftar vilken som används i avtalet.")
a('The private pools', "Las piscinas privadas", "Les piscines privées", "Die privaten Pools", "Частные бассейны", "المسابح الخاصة", "De privézwembaden", "Prywatne baseny", "De private bassengene")
a('The plans of homes 10A, 20B and 30A draw a private pool',
  "Los planos de las viviendas 10A, 20B y 30A dibujan una piscina privada en la terraza, pero la lista de precios no la menciona. Confirmamos que está construida e incluida.",
  "Les plans des logements 10A, 20B et 30A dessinent une piscine privée sur la terrasse, mais la liste de prix n’en mentionne pas. Nous confirmons qu’elle est construite et incluse.",
  "Die Grundrisse der Wohnungen 10A, 20B und 30A zeichnen auf der Terrasse einen privaten Pool ein, die Preisliste erwähnt aber keinen. Wir bestätigen, dass er gebaut und enthalten ist.",
  "На планах квартир 10A, 20B и 30A на террасе нарисован частный бассейн, но в прайс-листе о нём ничего не сказано. Мы подтверждаем, что он построен и включён в цену.",
  "تُظهر مخططات المساكن 10A و20B و30A مسبحاً خاصاً مرسوماً على التراس، لكن قائمة الأسعار لا تذكره. نؤكد أنه مبني ومشمول.",
  "De plattegronden van woning 10A, 20B en 30A tonen een privézwembad op het terras, maar de prijslijst vermeldt er geen. Wij bevestigen dat het is gebouwd en inbegrepen.",
  "Rzuty mieszkań 10A, 20B i 30A przedstawiają na tarasie prywatny basen, ale cennik go nie wspomina. Potwierdzamy, że jest zbudowany i wliczony.",
  "Plantegningene for bolig 10A, 20B og 30A viser et privat basseng på terrassen, men prislisten nevner det ikke. Vi bekrefter at det er bygget og inkludert.",
  "Planritningarna för bostad 10A, 20B och 30A visar en privat pool på terrassen, men prislistan nämner ingen. Vi bekräftar att den är byggd och ingår.")

# ------------------------------------------------------------------ availability, timeline, viewing, enquiry, faq
a('Eight homes <em>currently available</em>',
  "Ocho viviendas <em>disponibles actualmente</em>", "Huit logements <em>actuellement disponibles</em>", "Acht Wohnungen <em>derzeit verfügbar</em>",
  "Восемь квартир <em>доступны сейчас</em>", "ثمانية مساكن <em>متاحة حالياً</em>", "Acht woningen <em>nu beschikbaar</em>",
  "Osiem mieszkań <em>dostępnych obecnie</em>", "Åtte boliger <em>tilgjengelige nå</em>", "Åtta bostäder <em>tillgängliga just nu</em>")
a('Homes 10A, 20B, 30A, 31A, 32A, 34A, 34B and 24A are available',
  "Las viviendas 10A, 20B, 30A, 31A, 32A, 34A, 34B y 24A están disponibles en los Bloques 1, 2 y 3. Los precios son los del portal del promotor, a fecha de hoy, octubre de 2026, y los confirmamos antes de cualquier reserva.",
  "Les logements 10A, 20B, 30A, 31A, 32A, 34A, 34B et 24A sont disponibles dans les blocs 1, 2 et 3. Les prix sont ceux du portail du promoteur, à la date d’aujourd’hui, octobre 2026, et nous les confirmons avant toute réservation.",
  "Die Wohnungen 10A, 20B, 30A, 31A, 32A, 34A, 34B und 24A sind in den Blöcken 1, 2 und 3 verfügbar. Die Preise stammen aus dem Portal des Bauträgers, Stand heute, Oktober 2026, und wir bestätigen sie vor jeder Reservierung.",
  "Квартиры 10A, 20B, 30A, 31A, 32A, 34A, 34B и 24A доступны в блоках 1, 2 и 3. Цены взяты с портала застройщика на сегодняшний день, октябрь 2026 года, и мы подтверждаем их до любого бронирования.",
  "المساكن 10A و20B و30A و31A و32A و34A و34B و24A متاحة في المباني 1 و2 و3. الأسعار هي أسعار موقع المطوّر اليوم، أكتوبر 2026، ونؤكدها قبل أي حجز.",
  "De woningen 10A, 20B, 30A, 31A, 32A, 34A, 34B en 24A zijn beschikbaar in blok 1, 2 en 3. De prijzen zijn die van het portaal van de ontwikkelaar, per vandaag, oktober 2026, en wij bevestigen ze vóór elke reservering.",
  "Mieszkania 10A, 20B, 30A, 31A, 32A, 34A, 34B i 24A są dostępne w blokach 1, 2 i 3. Ceny pochodzą z portalu dewelopera, stan na dziś, październik 2026, i potwierdzamy je przed każdą rezerwacją.",
  "Boligene 10A, 20B, 30A, 31A, 32A, 34A, 34B og 24A er tilgjengelige i Hus 1, 2 og 3. Prisene er de fra utbyggerens portal, per i dag, oktober 2026, og vi bekrefter dem før enhver reservasjon.",
  "Bostäderna 10A, 20B, 30A, 31A, 32A, 34A, 34B och 24A är tillgängliga i Hus 1, 2 och 3. Priserna är de från exploatörens portal, per i dag, oktober 2026, och vi bekräftar dem före varje reservation.")
a('Prices, built areas and terrace areas are transcribed',
  "Los precios, las superficies construidas y las de terraza están transcritos de la lista de precios del portal del promotor, copiada el 12 de octubre de 2026, que indica ocho viviendas de la fase 2 como disponibles; el folleto dice que quedan ocho viviendas. Las superficies interiores y las de las estancias proceden de los planos del promotor. La superficie construida es la cifra del cuadro del Decreto 218/2005 de cada plano, y la terraza es la terraza cubierta y la descubierta juntas. En seis viviendas, la cifra de terraza del portal coincide con la suma de las dos terrazas del plano; en la vivienda 24A el portal indica {N44.47} {U} frente a {N46.47} {U} en el plano, y en la 20B {N117.29} {U} frente a {N177.29} {U} en el plano, y esta página muestra la cifra del plano. El portal no indica si el IVA está incluido. El estado de finalización procede del folleto, que describe las viviendas como terminadas y de entrega inmediata, y del portal, que dice llave en mano y listo para entrar a vivir; ninguno indica una fecha.",
  "Les prix, les surfaces construites et les surfaces de terrasse sont transcrits de la liste de prix du portail du promoteur, copiée le 12 octobre 2026, qui indique huit logements de la phase 2 comme disponibles ; la brochure indique qu’il reste huit logements. Les surfaces intérieures et celles des pièces proviennent des plans du promoteur. La surface construite est le chiffre du tableau du décret 218/2005 de chaque plan, et la terrasse est la terrasse couverte et la terrasse découverte réunies. Pour six logements, le chiffre de terrasse du portail est égal à la somme des deux terrasses du plan ; pour le logement 24A, le portail indique {N44.47} {U} contre {N46.47} {U} sur le plan, et pour le 20B {N117.29} {U} contre {N177.29} {U} sur le plan, et cette page affiche le chiffre du plan. Le portail n’indique pas si la TVA est incluse. L’état d’achèvement provient de la brochure, qui décrit les logements comme achevés et livrables immédiatement, et du portail, qui indique clés en main et prêts à habiter ; ni l’un ni l’autre ne donne de date.",
  "Preise, bebaute Flächen und Terrassenflächen sind der Preisliste im Portal des Bauträgers entnommen, kopiert am 12. Oktober 2026, die acht Wohnungen der Phase 2 als verfügbar aufführt; die Broschüre nennt acht verbleibende Wohnungen. Innenflächen und Raumflächen stammen aus den Grundrissen des Bauträgers. Die bebaute Fläche ist der Wert der Tabelle nach Dekret 218/2005 in jedem Grundriss, und die Terrasse ist die überdachte und die offene Terrasse zusammen. Bei sechs Wohnungen entspricht der Terrassenwert des Portals der Summe der beiden Terrassen im Grundriss; bei Wohnung 24A nennt das Portal {N44.47} {U} gegenüber {N46.47} {U} im Grundriss, bei 20B {N117.29} {U} gegenüber {N177.29} {U} im Grundriss, und diese Seite zeigt den Wert aus dem Grundriss. Das Portal gibt nicht an, ob die MwSt. enthalten ist. Der Fertigstellungsstatus stammt aus der Broschüre, die die Wohnungen als fertiggestellt und sofort übergabebereit beschreibt, und aus dem Portal, das schlüsselfertig und bezugsfertig angibt; keines nennt ein Datum.",
  "Цены, площади застройки и площади террас взяты из прайс-листа на портале застройщика, скопированного 12 октября 2026 года; в нём восемь квартир очереди 2 указаны как доступные, а в брошюре сказано, что осталось восемь квартир. Внутренние площади и площади помещений взяты с планов застройщика. Площадь застройки — это значение из таблицы по декрету 218/2005 на каждом плане, а терраса — крытая и открытая террасы вместе. У шести квартир значение террасы на портале равно сумме двух террас на плане; у квартиры 24A портал указывает {N44.47} {U} против {N46.47} {U} на плане, а у 20B — {N117.29} {U} против {N177.29} {U} на плане; на этой странице приведено значение с плана. Портал не сообщает, включён ли НДС. Статус завершения взят из брошюры, где квартиры названы готовыми с немедленной передачей, и с портала, где указано «под ключ» и «готово к заселению»; дата не указана ни там, ни там.",
  "الأسعار والمساحات المبنية ومساحات التراسات منقولة من قائمة أسعار موقع المطوّر المنسوخة في 12 أكتوبر 2026، والتي تذكر ثمانية مساكن من المرحلة 2 على أنها متاحة، ويذكر الكتيّب أن ثمانية مساكن متبقية. المساحات الداخلية ومساحات الغرف من مخططات المطوّر. المساحة المبنية هي رقم جدول المرسوم 218/2005 في كل مخطط، والتراس هو التراس المسقوف والمكشوف معاً. في ستة مساكن يساوي رقم التراس في الموقع مجموع التراسين في المخطط؛ وفي المسكن 24A يذكر الموقع {N44.47} {U} مقابل {N46.47} {U} في المخطط، وفي 20B يذكر {N117.29} {U} مقابل {N177.29} {U} في المخطط، وتعرض هذه الصفحة رقم المخطط. لا يذكر الموقع ما إذا كانت ضريبة القيمة المضافة مشمولة. حالة الإنجاز مأخوذة من الكتيّب الذي يصف المساكن بأنها مكتملة وجاهزة للتسليم الفوري، ومن الموقع الذي يذكر أنها جاهزة للسكن؛ ولا يذكر أيٌّ منهما تاريخاً.",
  "Prijzen, bebouwde oppervlaktes en terrasoppervlaktes zijn overgenomen uit de prijslijst op het portaal van de ontwikkelaar, gekopieerd op 12 oktober 2026, waarin acht woningen van fase 2 als beschikbaar staan; de brochure zegt dat er acht woningen over zijn. Binnenoppervlaktes en kamermaten komen uit de plattegronden van de ontwikkelaar. De bebouwde oppervlakte is het cijfer uit de tabel volgens decreet 218/2005 op elke plattegrond, en het terras is het overdekte en het open terras samen. Bij zes woningen is het terrascijfer van het portaal gelijk aan de som van de twee terrassen op de plattegrond; bij woning 24A noemt het portaal {N44.47} {U} tegen {N46.47} {U} op de plattegrond, en bij 20B {N117.29} {U} tegen {N177.29} {U} op de plattegrond, en deze pagina toont het cijfer van de plattegrond. Het portaal vermeldt niet of btw is inbegrepen. De opleverstatus komt uit de brochure, die de woningen beschrijft als opgeleverd en direct beschikbaar, en uit het portaal, dat sleutelklaar en klaar om in te trekken vermeldt; geen van beide noemt een datum.",
  "Ceny, powierzchnie zabudowy i powierzchnie tarasów zostały przepisane z cennika na portalu dewelopera, skopiowanego 12 października 2026 r., który podaje osiem mieszkań etapu 2 jako dostępne; broszura mówi, że zostało osiem mieszkań. Powierzchnie wewnętrzne i powierzchnie pomieszczeń pochodzą z rzutów dewelopera. Powierzchnia zabudowy to wartość z tabeli według dekretu 218/2005 na każdym rzucie, a taras to taras zadaszony i odkryty łącznie. W sześciu mieszkaniach wartość tarasu na portalu równa się sumie dwóch tarasów na rzucie; w mieszkaniu 24A portal podaje {N44.47} {U} wobec {N46.47} {U} na rzucie, a w 20B {N117.29} {U} wobec {N177.29} {U} na rzucie, i ta strona pokazuje wartość z rzutu. Portal nie podaje, czy VAT jest wliczony. Status ukończenia pochodzi z broszury, która opisuje mieszkania jako ukończone i dostępne od ręki, oraz z portalu, który podaje „pod klucz” i gotowość do zamieszkania; żadne z nich nie podaje daty.",
  "Priser, bygde areal og terrasseareal er hentet fra prislisten på utbyggerens portal, kopiert 12. oktober 2026, som oppgir åtte boliger i fase 2 som tilgjengelige; brosjyren sier at åtte boliger gjenstår. Innvendige areal og romareal er fra utbyggerens plantegninger. Bygd areal er tallet i tabellen etter dekret 218/2005 på hver plantegning, og terrassen er den overbygde og den åpne terrassen til sammen. For seks boliger er terrassetallet på portalen lik summen av de to terrassene på plantegningen; for bolig 24A oppgir portalen {N44.47} {U} mot {N46.47} {U} på plantegningen, og for 20B {N117.29} {U} mot {N177.29} {U} på plantegningen, og denne siden viser tallet fra plantegningen. Portalen oppgir ikke om mva er inkludert. Ferdigstillelsesstatusen er fra brosjyren, som beskriver boligene som ferdigstilte og umiddelbart tilgjengelige, og fra portalen, som oppgir nøkkelferdig og klar til innflytting; ingen av dem oppgir en dato.",
  "Priser, byggytor och terrassytor är hämtade från prislistan på exploatörens portal, kopierad den 12 oktober 2026, som anger åtta bostäder i fas 2 som tillgängliga; broschyren säger att åtta bostäder återstår. Invändiga ytor och rumsytor är från exploatörens planritningar. Byggytan är siffran i tabellen enligt dekret 218/2005 på varje planritning, och terrassen är den övertäckta och den öppna terrassen tillsammans. För sex bostäder är portalens terrasssiffra lika med summan av de två terrasserna på planritningen; för bostad 24A anger portalen {N44.47} {U} mot {N46.47} {U} på planritningen, och för 20B {N117.29} {U} mot {N177.29} {U} på planritningen, och den här sidan visar siffran från planritningen. Portalen anger inte om moms ingår. Färdigställandestatusen kommer från broschyren, som beskriver bostäderna som färdiga och omedelbart tillgängliga, och från portalen, som anger nyckelfärdigt och inflyttningsklart; ingen av dem anger ett datum.")
a('Floorplans for all eight available homes and the price list.',
  "Los planos de las ocho viviendas disponibles y la lista de precios.", "Les plans des huit logements disponibles et la liste de prix.",
  "Die Grundrisse aller acht verfügbaren Wohnungen und die Preisliste.", "Планировки всех восьми доступных квартир и прайс-лист.",
  "مخططات المساكن الثمانية المتاحة وقائمة الأسعار.", "De plattegronden van alle acht beschikbare woningen en de prijslijst.",
  "Rzuty wszystkich ośmiu dostępnych mieszkań i cennik.", "Plantegningene for alle åtte tilgjengelige boliger og prislisten.",
  "Planritningarna för alla åtta tillgängliga bostäder och prislistan.")
a('Visit the show apartment and the shared facilities with us.',
  "Visite con nosotros el piso piloto y las zonas comunes.", "Visitez avec nous l’appartement témoin et les espaces communs.",
  "Besichtigen Sie mit uns die Musterwohnung und die Gemeinschaftsbereiche.", "Осмотрите вместе с нами демонстрационную квартиру и общие зоны.",
  "زوروا معنا الشقة النموذجية والمرافق المشتركة.", "Bezoek met ons het showappartement en de gedeelde voorzieningen.",
  "Zwiedzimy razem z Państwem lokal pokazowy i wspólne udogodnienia.", "Besøk visningsleiligheten og fellesfasilitetene sammen med oss.",
  "Besök visningslägenheten och de gemensamma bekvämligheterna tillsammans med oss.")
a('We confirm the reservation terms and the bank guarantee in writing',
  "Confirmamos por escrito las condiciones de reserva y la garantía bancaria, y después el contrato de compraventa.",
  "Nous confirmons par écrit les conditions de réservation et la garantie bancaire, puis le contrat d’achat.",
  "Wir bestätigen die Reservierungsbedingungen und die Bankgarantie schriftlich, danach folgt der Kaufvertrag.",
  "Мы письменно подтверждаем условия бронирования и банковскую гарантию, затем следует договор купли-продажи.",
  "نؤكد كتابةً شروط الحجز والضمان المصرفي، ثم عقد الشراء.",
  "Wij bevestigen de reserveringsvoorwaarden en de bankgarantie schriftelijk, daarna volgt het koopcontract.",
  "Potwierdzamy na piśmie warunki rezerwacji i gwarancję bankową, a następnie umowę zakupu.",
  "Vi bekrefter reservasjonsvilkårene og bankgarantien skriftlig, deretter kjøpskontrakten.",
  "Vi bekräftar reservationsvillkoren och bankgarantin skriftligen, därefter köpeavtalet.")
a('The homes are built, and the developer offers a show apartment',
  "Las viviendas están construidas y el promotor ofrece un piso piloto, así que la visita trata de la luz, la terraza y las vistas.",
  "Les logements sont construits et le promoteur propose un appartement témoin ; la visite porte donc sur la lumière, la terrasse et la vue.",
  "Die Wohnungen sind gebaut, und der Bauträger bietet eine Musterwohnung an; bei einer Besichtigung geht es also um das Licht, die Terrasse und die Aussicht.",
  "Квартиры построены, а застройщик предлагает демонстрационную квартиру, поэтому осмотр посвящён свету, террасе и виду.",
  "المساكن مبنية ويوفر المطوّر شقة نموذجية، لذا تتمحور الزيارة حول الضوء والتراس والإطلالة.",
  "De woningen zijn gebouwd en de ontwikkelaar biedt een showappartement aan, dus een bezoek gaat over het licht, het terras en het uitzicht.",
  "Mieszkania są zbudowane, a deweloper oferuje lokal pokazowy, więc wizyta dotyczy światła, tarasu i widoku.",
  "Boligene er bygget og utbyggeren tilbyr en visningsleilighet, så et besøk handler om lyset, terrassen og utsikten.",
  "Bostäderna är byggda och exploatören erbjuder en visningslägenhet, så ett besök handlar om ljuset, terrassen och utsikten.")
a('Walk the show apartment, the pools and the gym.',
  "Recorra el piso piloto, las piscinas y el gimnasio.", "Parcourez l’appartement témoin, les piscines et la salle de sport.",
  "Gehen Sie durch die Musterwohnung, die Pools und den Fitnessraum.", "Пройдитесь по демонстрационной квартире, бассейнам и тренажёрному залу.",
  "تجولوا في الشقة النموذجية والمسابح والصالة الرياضية.", "Loop door het showappartement, langs de zwembaden en de gym.",
  "Przejdziemy przez lokal pokazowy, baseny i siłownię.", "Gå gjennom visningsleiligheten, bassengene og treningsrommet.",
  "Gå igenom visningslägenheten, poolerna och gymmet.")
a('See the size of the terrace and the view of the sea.',
  "Compruebe el tamaño de la terraza y la vista del mar.", "Constatez la taille de la terrasse et la vue sur la mer.",
  "Sehen Sie die Größe der Terrasse und den Blick aufs Meer.", "Оцените размер террасы и вид на море.",
  "شاهدوا حجم التراس والإطلالة على البحر.", "Zie hoe groot het terras is en hoe het uitzicht op zee is.",
  "Zobaczą Państwo wielkość tarasu i widok na morze.", "Se hvor stor terrassen er og utsikten over havet.",
  "Se terrassens storlek och havsutsikten.")
a('Ask about <em>Solana Residences</em>',
  "Pregunte por <em>Solana Residences</em>", "Renseignez-vous sur <em>Solana Residences</em>", "Fragen Sie nach <em>Solana Residences</em>",
  "Узнайте о <em>Solana Residences</em>", "استفسروا عن <em>Solana Residences</em>", "Vraag naar <em>Solana Residences</em>",
  "Zapytaj o <em>Solana Residences</em>", "Spør om <em>Solana Residences</em>", "Fråga om <em>Solana Residences</em>")
a('Tell us what you need and we will come back with current availability and the floorplans.',
  "Cuéntenos lo que necesita y le responderemos con la disponibilidad actual y los planos.",
  "Dites-nous ce dont vous avez besoin et nous reviendrons vers vous avec la disponibilité actuelle et les plans.",
  "Sagen Sie uns, was Sie suchen, und wir melden uns mit der aktuellen Verfügbarkeit und den Grundrissen.",
  "Расскажите, что вам нужно, и мы вернёмся с актуальной информацией о наличии и планировками.",
  "أخبرونا بما تحتاجونه وسنعود إليكم بالتوافر الحالي والمخططات.",
  "Laat ons weten wat u zoekt en wij komen bij u terug met de actuele beschikbaarheid en de plattegronden.",
  "Proszę napisać, czego Państwo potrzebują, a odpowiemy z aktualną dostępnością i rzutami.",
  "Fortell oss hva som trengs, så kommer vi tilbake med gjeldende tilgjengelighet og plantegningene.",
  "Berätta vad ni behöver så återkommer vi med aktuell tillgänglighet och planritningarna.")
a('Hello Nueva Living, I would like information about Solana Residences.',
  "Hola Nueva Living, me gustaría recibir información sobre Solana Residences.", "Bonjour Nueva Living, je souhaite recevoir des informations sur Solana Residences.",
  "Guten Tag Nueva Living, ich hätte gern Informationen zu Solana Residences.", "Здравствуйте, Nueva Living, я хотел бы получить информацию о Solana Residences.",
  "مرحباً Nueva Living، أود الحصول على معلومات حول Solana Residences.", "Hallo Nueva Living, ik ontvang graag informatie over Solana Residences.",
  "Dzień dobry, Nueva Living, proszę o informacje o Solana Residences.", "Hei Nueva Living, jeg vil gjerne ha informasjon om Solana Residences.",
  "Hej Nueva Living, jag vill gärna ha information om Solana Residences.")
a('Eight are listed as available',
  "Hay ocho disponibles: de 3 dormitorios las viviendas 10A, 20B, 30A, 32A y 34B, y de 2 dormitorios las 24A, 31A y 34A, desde {E645000} hasta {E1254700}. Los documentos no indican cuántas viviendas tiene la promoción en total.",
  "Huit sont indiqués comme disponibles : à 3 chambres les logements 10A, 20B, 30A, 32A et 34B, et à 2 chambres les 24A, 31A et 34A, de {E645000} à {E1254700}. Les documents n’indiquent pas combien de logements compte le programme au total.",
  "Acht sind als verfügbar aufgeführt: mit 3 Schlafzimmern die Wohnungen 10A, 20B, 30A, 32A und 34B, mit 2 Schlafzimmern 24A, 31A und 34A, von {E645000} bis {E1254700}. Die Unterlagen geben nicht an, wie viele Wohnungen die Anlage insgesamt hat.",
  "Восемь указаны как доступные: с 3 спальнями — квартиры 10A, 20B, 30A, 32A и 34B, с 2 спальнями — 24A, 31A и 34A, от {E645000} до {E1254700}. В документах не сказано, сколько всего квартир в комплексе.",
  "ثمانية مساكن مذكورة كمتاحة: بثلاث غرف نوم المساكن 10A و20B و30A و32A و34B، وبغرفتي نوم 24A و31A و34A، من {E645000} إلى {E1254700}. لا تذكر الوثائق إجمالي عدد المساكن في المشروع.",
  "Acht staan er als beschikbaar vermeld: met 3 slaapkamers de woningen 10A, 20B, 30A, 32A en 34B, en met 2 slaapkamers 24A, 31A en 34A, van {E645000} tot {E1254700}. De documenten vermelden niet hoeveel woningen het project in totaal heeft.",
  "Osiem jest podanych jako dostępne: z 3 sypialniami mieszkania 10A, 20B, 30A, 32A i 34B, z 2 sypialniami 24A, 31A i 34A, od {E645000} do {E1254700}. Dokumenty nie podają, ile mieszkań liczy cała inwestycja.",
  "Åtte er oppført som tilgjengelige: med 3 soverom boligene 10A, 20B, 30A, 32A og 34B, og med 2 soverom 24A, 31A og 34A, fra {E645000} til {E1254700}. Dokumentene oppgir ikke hvor mange boliger prosjektet har til sammen.",
  "Åtta är angivna som tillgängliga: med 3 sovrum bostäderna 10A, 20B, 30A, 32A och 34B, och med 2 sovrum 24A, 31A och 34A, från {E645000} till {E1254700}. Dokumenten anger inte hur många bostäder projektet har totalt.")
a('The developer’s brochure describes completed residences with immediate delivery',
  "El folleto del promotor describe viviendas terminadas de entrega inmediata, y su portal dice llave en mano y listo para entrar a vivir. Ninguno indica una fecha de finalización, por lo que solicitamos la licencia de ocupación y el certificado energético de la vivienda que elija.",
  "La brochure du promoteur décrit des logements achevés livrables immédiatement, et son portail indique clés en main et prêts à habiter. Aucun ne donne de date d’achèvement ; nous demandons donc la licence d’occupation et le certificat énergétique du logement que vous choisissez.",
  "Die Broschüre des Bauträgers beschreibt fertiggestellte Wohnungen mit sofortiger Übergabe, und sein Portal nennt sie schlüsselfertig und bezugsfertig. Keines gibt ein Fertigstellungsdatum an, daher fragen wir die Bezugsgenehmigung und den Energieausweis der von Ihnen gewählten Wohnung an.",
  "В брошюре застройщика квартиры описаны как завершённые с немедленной передачей, а на его портале указано «под ключ» и «готово к заселению». Даты завершения нет ни там, ни там, поэтому мы запрашиваем лицензию на заселение и энергетический сертификат выбранной вами квартиры.",
  "يصف كتيّب المطوّر مساكن مكتملة جاهزة للتسليم الفوري، ويذكر موقعه أنها جاهزة للسكن. لا يذكر أيٌّ منهما تاريخ إنجاز، لذلك نطلب رخصة الإشغال وشهادة الطاقة للمسكن الذي تختارونه.",
  "De brochure van de ontwikkelaar beschrijft opgeleverde woningen met directe oplevering, en zijn portaal vermeldt sleutelklaar en klaar om in te trekken. Geen van beide noemt een opleverdatum, dus wij vragen de bewoningsvergunning en het energiecertificaat van de woning van uw keuze op.",
  "Broszura dewelopera opisuje ukończone mieszkania z natychmiastowym przekazaniem, a jego portal podaje „pod klucz” i gotowość do zamieszkania. Żadne z nich nie podaje daty ukończenia, dlatego prosimy o pozwolenie na użytkowanie i świadectwo energetyczne wybranego mieszkania.",
  "Utbyggerens brosjyre beskriver ferdigstilte boliger med umiddelbar overlevering, og portalen deres oppgir nøkkelferdig og klar til innflytting. Ingen av dem oppgir en ferdigstillelsesdato, så vi ber om brukstillatelsen og energisertifikatet for den boligen som velges.",
  "Exploatörens broschyr beskriver färdiga bostäder med omedelbar tillträde, och dess portal anger nyckelfärdigt och inflyttningsklart. Ingen av dem anger ett färdigställandedatum, så vi begär brukstillståndet och energicertifikatet för den bostad som väljs.")
a('The portal does not say. We confirm in writing whether the prices include VAT',
  "El portal no lo indica. Confirmamos por escrito si los precios incluyen IVA y qué gastos de compra se añaden.",
  "Le portail ne le précise pas. Nous confirmons par écrit si les prix incluent la TVA et quels frais d’achat s’y ajoutent.",
  "Das Portal gibt es nicht an. Wir bestätigen schriftlich, ob die Preise die MwSt. enthalten und welche Erwerbsnebenkosten hinzukommen.",
  "Портал этого не указывает. Мы письменно подтверждаем, включён ли НДС в цены и какие расходы на покупку добавляются.",
  "لا يذكر الموقع ذلك. نؤكد كتابةً ما إذا كانت الأسعار تشمل ضريبة القيمة المضافة وما هي تكاليف الشراء الإضافية.",
  "Het portaal vermeldt dat niet. Wij bevestigen schriftelijk of de prijzen btw bevatten en welke aankoopkosten erbovenop komen.",
  "Portal tego nie podaje. Potwierdzamy na piśmie, czy ceny zawierają VAT i jakie koszty zakupu dochodzą.",
  "Portalen oppgir det ikke. Vi bekrefter skriftlig om prisene inkluderer mva og hvilke kjøpskostnader som kommer i tillegg.",
  "Portalen anger det inte. Vi bekräftar skriftligen om priserna inkluderar moms och vilka köpkostnader som tillkommer.")
a('Which areas differ between the documents?',
  "¿Qué superficies difieren entre los documentos?", "Quelles surfaces diffèrent entre les documents ?", "Welche Flächen weichen zwischen den Unterlagen ab?",
  "Какие площади различаются в документах?", "ما المساحات التي تختلف بين الوثائق؟", "Welke oppervlaktes verschillen tussen de documenten?",
  "Które powierzchnie różnią się w dokumentach?", "Hvilke areal er forskjellige mellom dokumentene?", "Vilka ytor skiljer sig mellan dokumenten?")
a('The terraces of home 24A are 44.47 sqm on the price list',
  "Las terrazas de la vivienda 24A miden {N44.47} {U} en la lista de precios y {N46.47} {U} en el plano, y las de la 20B miden {N117.29} {U} en la lista de precios y {N177.29} {U} en el plano. Esta página muestra las cifras de los planos.",
  "Les terrasses du logement 24A mesurent {N44.47} {U} sur la liste de prix et {N46.47} {U} sur le plan, et celles du 20B {N117.29} {U} sur la liste de prix et {N177.29} {U} sur le plan. Cette page affiche les chiffres des plans.",
  "Die Terrassen der Wohnung 24A messen in der Preisliste {N44.47} {U} und im Grundriss {N46.47} {U}, die der 20B in der Preisliste {N117.29} {U} und im Grundriss {N177.29} {U}. Diese Seite zeigt die Werte aus den Grundrissen.",
  "Террасы квартиры 24A в прайс-листе составляют {N44.47} {U}, а на плане — {N46.47} {U}; террасы 20B — {N117.29} {U} в прайс-листе и {N177.29} {U} на плане. На этой странице приведены значения с планов.",
  "تبلغ مساحة تراسات المسكن 24A في قائمة الأسعار {N44.47} {U} وفي المخطط {N46.47} {U}، وتراسات 20B في قائمة الأسعار {N117.29} {U} وفي المخطط {N177.29} {U}. تعرض هذه الصفحة أرقام المخططات.",
  "De terrassen van woning 24A meten {N44.47} {U} in de prijslijst en {N46.47} {U} op de plattegrond, en die van 20B {N117.29} {U} in de prijslijst en {N177.29} {U} op de plattegrond. Deze pagina toont de cijfers van de plattegronden.",
  "Tarasy mieszkania 24A mają {N44.47} {U} w cenniku i {N46.47} {U} na rzucie, a mieszkania 20B {N117.29} {U} w cenniku i {N177.29} {U} na rzucie. Ta strona pokazuje wartości z rzutów.",
  "Terrassene i bolig 24A er {N44.47} {U} i prislisten og {N46.47} {U} på plantegningen, og de i 20B er {N117.29} {U} i prislisten og {N177.29} {U} på plantegningen. Denne siden viser tallene fra plantegningene.",
  "Terrasserna i bostad 24A är {N44.47} {U} i prislistan och {N46.47} {U} på planritningen, och de i 20B är {N117.29} {U} i prislistan och {N177.29} {U} på planritningen. Den här sidan visar siffrorna från planritningarna.")
a('What shared facilities are there?',
  "¿Qué zonas comunes hay?", "Quels espaces communs y a-t-il ?", "Welche Gemeinschaftsbereiche gibt es?", "Какие общие зоны есть?",
  "ما المرافق المشتركة المتوفرة؟", "Welke gedeelde voorzieningen zijn er?", "Jakie udogodnienia wspólne są dostępne?", "Hvilke fellesfasiliteter finnes?", "Vilka gemensamma bekvämligheter finns?")
a('The developer lists an outdoor pool, a heated indoor pool',
  "El promotor indica una piscina exterior, una piscina interior climatizada, un gimnasio, un espacio de coworking, una sala social y jardines, y ofrece un piso piloto.",
  "Le promoteur indique une piscine extérieure, une piscine intérieure chauffée, une salle de sport, un espace de coworking, un salon commun et des jardins, et propose un appartement témoin.",
  "Der Bauträger nennt einen Außenpool, einen beheizten Innenpool, einen Fitnessraum, einen Coworking-Bereich, einen Gemeinschaftsraum und Gärten und bietet eine Musterwohnung an.",
  "Застройщик указывает открытый бассейн, крытый подогреваемый бассейн, тренажёрный зал, коворкинг, общий зал и сады и предлагает демонстрационную квартиру.",
  "يذكر المطوّر مسبحاً خارجياً ومسبحاً داخلياً مُدفّأً وصالة رياضية ومساحة عمل مشتركة وقاعة اجتماعية وحدائق، ويوفر شقة نموذجية.",
  "De ontwikkelaar noemt een buitenzwembad, een verwarmd binnenzwembad, een gym, een coworkingruimte, een gemeenschappelijke ruimte en tuinen, en biedt een showappartement aan.",
  "Deweloper wymienia basen zewnętrzny, ogrzewany basen wewnętrzny, siłownię, przestrzeń coworkingową, salę towarzyską i ogrody oraz oferuje lokal pokazowy.",
  "Utbyggeren oppgir et utendørs basseng, et oppvarmet innendørs basseng, et treningsrom, et coworking-område, et felles oppholdsrom og hager, og tilbyr en visningsleilighet.",
  "Exploatören anger en utomhuspool, en uppvärmd inomhuspool, ett gym, en coworkingyta, ett gemensamt rum och trädgårdar, och erbjuder en visningslägenhet.")

a('8 homes', "8 viviendas", "8 logements", "8 Wohnungen", "8 квартир", "8 مساكن", "8 woningen", "8 mieszkań", "8 boliger", "8 bostäder")

# ------------------------------------------------------------------ done
missing = [s for s in todo if s not in T]
print('translated', len(T), 'of', len(todo), 'missing', len(missing))
for s in missing: print('  MISSING', s[:100])
for s, tr in T.items():
    for l in LOCS:
        assert l in tr and tr[l].strip(), (s, l)
json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
