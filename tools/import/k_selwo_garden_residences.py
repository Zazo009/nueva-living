# -*- coding: utf-8 -*-
"""Selwo Garden Residences: the strings the translation memory did not have.

Same shape as k_estepona_west_golf_residences.py: keyed by the path of the English string in
project.json (looked up here, never retyped) and written to tr_s.json keyed by the English string,
as assemble.py expects. Unit sizes are built from one template per locale, using the words
la-resina-hillside-residences already publishes (Norwegian takes "bebygd areal" and "bruksareal").
Tokens: {E338000} money, {N87.89} decimal number, {U} the area unit, {T} the tax word.
    python3 tools/import/k_selwo_garden_residences.py <scratch dir>   (writes <dir>/tr_s.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة',
        'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
T = {}
SLUG = 'selwo-garden-residences'
proj = json.load(open(f'content/liora-projects/{SLUG}/project.json'))


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.translate({ord(','): GROUP[l], ord('.'): '.' if l == 'ar' else ','})


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.,]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l]).replace('{T}', TAXW[l])


def get(path):
    node = proj
    for part in re.findall(r'\.([A-Za-z0-9_]+)|\[(\d+)\]', path):
        node = node[part[0]] if part[0] else node[int(part[1])]
    return node


def put(en, tr):
    assert len(tr) == 9, (en[:60], len(tr))
    new = {l: expand(t, l) for l, t in zip(LOCS, tr)}
    assert en not in T or T[en] == new, en[:60]
    T[en] = new


def a(path, *tr):
    """Translate the English string found at `path`."""
    put(get(path), tr)


def same(en):
    T[en] = {l: en for l in LOCS}


same(get('.name')); same(get('.shortName')); same(get('.titleHtml'))

# ---- units: the reference is the developer's own numbering; sizes from one template --------------
SIZE = {  # built, usable, terrace, garden
    'es': ('construido', 'superficie útil', 'terraza', 'jardín'),
    'fr': ('construit', 'surface utile', 'terrasse', 'jardin'),
    'de': ('bebaut', 'Wohnfläche', 'Terrasse', 'Garten'),
    'ru': ('застройка', 'полезная площадь', 'терраса', 'сад'),
    'ar': ('مبنية', 'مساحة صافية', 'تراس', 'حديقة'),
    'nl': ('bebouwd', 'nuttige oppervlakte', 'terras', 'tuin'),
    'pl': ('powierzchnia zabudowy', 'powierzchnia użytkowa', 'taras', 'ogród'),
    'no': ('bebygd areal', 'bruksareal', 'terrasse', 'hage'),
    'sv': ('byggyta', 'nyttoyta', 'terrass', 'trädgård'),
}
for u in proj['availability']['units']:
    same(u['reference'])
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm usable, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm garden)?', u['size'])
    assert m, u['size']
    out = []
    for l in LOCS:
        parts = [f'{num(v, l)} {UNIT[l]} {w}' for v, w in zip(m.groups(), SIZE[l]) if v]
        out.append(('، ' if l == 'ar' else ', ').join(parts))
    T[u['size']] = dict(zip(LOCS, out))

# ---- description, SEO, hero, card -------------------------------------------------------------

a('.description',
  'Veintiséis apartamentos disponibles en un conjunto cerrado junto a Selwo Aventura, en Estepona, de uno, dos y tres dormitorios y de {N87.89} a {N148.27} {U} construidos, todos con terraza y cinco viviendas en planta baja con jardín en sus planos, con piscinas, spa, gimnasio y sala de coworking, desde {E338000} + {T}.',
  'Vingt-six appartements disponibles dans une résidence fermée à côté de Selwo Aventura, à Estepona, d’une, deux ou trois chambres et de {N87.89} à {N148.27} {U} construits, tous avec terrasse et cinq logements en rez-de-chaussée avec jardin sur leur plan, avec piscines, spa, salle de sport et espace de coworking, à partir de {E338000} + {T}.',
  'Sechsundzwanzig verfügbare Wohnungen in einer geschlossenen Anlage neben Selwo Aventura in Estepona, mit einem, zwei oder drei Schlafzimmern und {N87.89} bis {N148.27} {U} bebauter Fläche, alle mit Terrasse und fünf Erdgeschosswohnungen laut Grundriss mit Garten, mit Pools, Spa, Fitnessraum und Coworking-Raum, ab {E338000} + {T}',
  'Двадцать шесть свободных квартир в закрытом комплексе рядом с Selwo Aventura в Эстепоне, с одной, двумя или тремя спальнями, площадью застройки от {N87.89} до {N148.27} {U}, у каждой есть терраса, а у пяти квартир на первом этаже по планировкам есть сад; бассейны, спа, тренажёрный зал и коворкинг, от {E338000} + {T}.',
  'ست وعشرون شقة متاحة في مجمع مغلق بجوار سيلوو أفينتورا في إستيبونا، بغرفة أو غرفتين أو ثلاث غرف نوم ومساحة مبنية من {N87.89} إلى {N148.27} {U}، لكل منها تراس، ولخمس شقق في الطابق الأرضي حديقة بحسب مخططاتها، مع مسابح وسبا وصالة رياضية ومساحة عمل مشتركة، ابتداءً من {E338000} + {T}.',
  'Zesentwintig beschikbare appartementen in een omheind complex naast Selwo Aventura in Estepona, met één, twee of drie slaapkamers en {N87.89} tot {N148.27} {U} bebouwd, alle met een terras en vijf benedenwoningen met een tuin op hun plattegrond, met zwembaden, een spa, een fitnessruimte en een coworkingruimte, vanaf {E338000} + {T}.',
  'Dwadzieścia sześć dostępnych apartamentów na zamkniętym osiedlu obok Selwo Aventura w Esteponie, z jedną, dwiema lub trzema sypialniami i powierzchnią zabudowy od {N87.89} do {N148.27} {U}, każdy z tarasem, a pięć mieszkań na parterze według rzutów z ogrodem; baseny, spa, siłownia i coworking, od {E338000} + {T}.',
  'Tjueseks ledige leiligheter i et inngjerdet anlegg ved Selwo Aventura i Estepona, med ett, to eller tre soverom og {N87.89} til {N148.27} {U} bebygd areal, alle med terrasse og fem leiligheter i første etasje med hage på plantegningen, med bassenger, spa, treningsrom og kontorfellesskap, fra {E338000} + {T}.',
  'Tjugosex lediga lägenheter i ett inhägnat område intill Selwo Aventura i Estepona, med ett, två eller tre sovrum och {N87.89} till {N148.27} {U} byggyta, alla med terrass och fem bottenvåningar med trädgård enligt planritningen, med pooler, spa, gym och coworkingrum, från {E338000} + {T} (spansk moms).')

a('.seoDescription',
  'Veintiséis apartamentos junto a Selwo Aventura, Estepona: de uno a tres dormitorios, de 88 a 148 {U} construidos, terraza en todas las viviendas, piscinas, spa, gimnasio y coworking.',
  'Vingt-six appartements à côté de Selwo Aventura, Estepona : une à trois chambres, 88 à 148 {U} construits, terrasse pour chaque logement, piscines, spa, salle de sport et coworking.',
  'Sechsundzwanzig Wohnungen neben Selwo Aventura, Estepona: ein bis drei Schlafzimmer, 88 bis 148 {U} bebaut, Terrasse bei jeder Wohnung, Pools, Spa, Fitnessraum und Coworking.',
  'Двадцать шесть квартир рядом с Selwo Aventura, Эстепона: от одной до трёх спален, от 88 до 148 {U} застройки, терраса у каждой квартиры, бассейны, спа, тренажёрный зал и коворкинг.',
  'ست وعشرون شقة بجوار سيلوو أفينتورا، إستيبونا: من غرفة إلى ثلاث غرف نوم، ومن 88 إلى 148 {U} مبنية، وتراس لكل شقة، ومسابح وسبا وصالة رياضية ومساحة عمل مشتركة.',
  'Zesentwintig appartementen naast Selwo Aventura, Estepona: één tot drie slaapkamers, 88 tot 148 {U} bebouwd, een terras bij elke woning, zwembaden, spa, fitness en coworking.',
  'Dwadzieścia sześć apartamentów obok Selwo Aventura, Estepona: od jednej do trzech sypialni, od 88 do 148 {U} zabudowy, taras przy każdym mieszkaniu, baseny, spa, siłownia i coworking.',
  'Tjueseks leiligheter ved Selwo Aventura, Estepona: ett til tre soverom, 88 til 148 {U} bebygd areal, terrasse til hver bolig, bassenger, spa, treningsrom og kontorfellesskap.',
  'Tjugosex lägenheter intill Selwo Aventura, Estepona: ett till tre sovrum, 88 till 148 {U} byggyta, terrass till varje bostad, pooler, spa, gym och coworking.')

a('.twitterDescription',
  'Apartamentos en un conjunto cerrado junto a Selwo Aventura, en Estepona, con terrazas, jardín en algunas viviendas de planta baja, piscinas y spa. Desde {E338000} + {T}.',
  'Appartements dans une résidence fermée à côté de Selwo Aventura, à Estepona, avec terrasses, jardin pour certains rez-de-chaussée, piscines et spa. À partir de {E338000} + {T}.',
  'Wohnungen in einer geschlossenen Anlage neben Selwo Aventura in Estepona, mit Terrassen, Garten bei einigen Erdgeschosswohnungen, Pools und Spa. Ab {E338000} + {T}',
  'Квартиры в закрытом комплексе рядом с Selwo Aventura в Эстепоне: террасы, сад у части квартир на первом этаже, бассейны и спа. От {E338000} + {T}.',
  'شقق في مجمع مغلق بجوار سيلوو أفينتورا في إستيبونا، مع تراسات وحديقة لبعض شقق الطابق الأرضي ومسابح وسبا. ابتداءً من {E338000} + {T}.',
  'Appartementen in een omheind complex naast Selwo Aventura in Estepona, met terrassen, een tuin bij enkele benedenwoningen, zwembaden en een spa. Vanaf {E338000} + {T}.',
  'Apartamenty na zamkniętym osiedlu obok Selwo Aventura w Esteponie, z tarasami, ogrodem przy części mieszkań na parterze, basenami i spa. Od {E338000} + {T}.',
  'Leiligheter i et inngjerdet anlegg ved Selwo Aventura i Estepona, med terrasser, hage til noen leiligheter i første etasje, bassenger og spa. Fra {E338000} + {T}.',
  'Lägenheter i ett inhägnat område intill Selwo Aventura i Estepona, med terrasser, trädgård till några bottenvåningar, pooler och spa. Från {E338000} + {T}.')

a('.hero.eyebrow',
  'Veintiséis viviendas disponibles / conjunto cerrado', 'Vingt-six logements disponibles / résidence fermée',
  'Sechsundzwanzig Wohnungen verfügbar / geschlossene Anlage', 'Двадцать шесть квартир в продаже / закрытый комплекс',
  'ست وعشرون شقة متاحة / مجمع مغلق', 'Zesentwintig woningen beschikbaar / omheind complex',
  'Dwadzieścia sześć mieszkań dostępnych / osiedle zamknięte', 'Tjueseks boliger ledige / inngjerdet anlegg',
  'Tjugosex bostäder lediga / inhägnat område')

for p in ('.hero.startingPrice', '.quickFacts[0][1]'):
    a(p, 'Desde {E338000} + {T}', 'À partir de {E338000} + {T}', 'Ab {E338000} + {T}', 'От {E338000} + {T}',
      'ابتداءً من {E338000} + {T}', 'Vanaf {E338000} + {T}', 'Od {E338000} + {T}', 'Fra {E338000} + {T}', 'Från {E338000} + {T}')
a('.card.meta[0][1]', '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}',
  '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}')
a('.availability.startingPrice', '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}',
  '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}', '{E338000} + {T}')
a('.availability.priceRange', '{E338000} - {E686000} + {T}', '{E338000} - {E686000} + {T}', '{E338000} - {E686000} + {T}',
  '{E338000} - {E686000} + {T}', '{E338000} - {E686000} + {T}', '{E338000} - {E686000} + {T}', '{E338000} - {E686000} + {T}',
  '{E338000} - {E686000} + {T}', '{E338000} - {E686000} + {T}')

a('.card.description',
  'Veintiséis apartamentos de uno a tres dormitorios con terraza junto a Selwo Aventura, en Estepona, con piscinas, spa, gimnasio y sala de coworking, desde {E338000} + {T}.',
  'Vingt-six appartements d’une à trois chambres avec terrasse à côté de Selwo Aventura, à Estepona, avec piscines, spa, salle de sport et espace de coworking, à partir de {E338000} + {T}.',
  'Sechsundzwanzig Wohnungen mit einem bis drei Schlafzimmern und Terrasse neben Selwo Aventura in Estepona, mit Pools, Spa, Fitnessraum und Coworking-Raum, ab {E338000} + {T}',
  'Двадцать шесть квартир с одной–тремя спальнями и террасой рядом с Selwo Aventura в Эстепоне: бассейны, спа, тренажёрный зал и коворкинг, от {E338000} + {T}.',
  'ست وعشرون شقة من غرفة إلى ثلاث غرف نوم مع تراس بجوار سيلوو أفينتورا في إستيبونا، مع مسابح وسبا وصالة رياضية ومساحة عمل مشتركة، ابتداءً من {E338000} + {T}.',
  'Zesentwintig appartementen met één tot drie slaapkamers en een terras naast Selwo Aventura in Estepona, met zwembaden, een spa, een fitnessruimte en een coworkingruimte, vanaf {E338000} + {T}.',
  'Dwadzieścia sześć apartamentów z jedną do trzech sypialni i tarasem obok Selwo Aventura w Esteponie, z basenami, spa, siłownią i coworkingiem, od {E338000} + {T}.',
  'Tjueseks leiligheter med ett til tre soverom og terrasse ved Selwo Aventura i Estepona, med bassenger, spa, treningsrom og kontorfellesskap, fra {E338000} + {T}.',
  'Tjugosex lägenheter med ett till tre sovrum och terrass intill Selwo Aventura i Estepona, med pooler, spa, gym och coworkingrum, från {E338000} + {T}.')

# ---- images -----------------------------------------------------------------------------------
BI = {'es': 'Imagen del folleto del conjunto: ', 'fr': 'Image de la brochure de la résidence : ',
      'de': 'Bild aus der Broschüre der Anlage: ', 'ru': 'Изображение из буклета комплекса: ',
      'ar': 'صورة من كتيّب المجمع: ', 'nl': 'Beeld uit de brochure van het complex: ',
      'pl': 'Zdjęcie z broszury osiedla: ', 'no': 'Bilde fra anleggets brosjyre: ', 'sv': 'Bild ur områdets broschyr: '}
CG = {'es': 'Vista generada por ordenador ', 'fr': 'Vue générée par ordinateur ', 'de': 'Computergenerierte Ansicht ',
      'ru': 'Компьютерная визуализация: ', 'ar': 'منظر مولَّد بالحاسوب ', 'nl': 'Computergegenereerd beeld ',
      'pl': 'Wygenerowany komputerowo widok ', 'no': 'Datagenerert bilde ', 'sv': 'Datorgenererad vy '}


def bi(en, *tr):
    assert en.startswith('Brochure image of the scheme: '), en
    put(en, [BI[l] + t for l, t in zip(LOCS, tr)])


def cg(en, *tr):
    assert en.startswith('Computer-generated view '), en
    put(en, [CG[l] + t for l, t in zip(LOCS, tr)])


IM = {i['src'].rsplit('/', 1)[1][:-4]: i['alt'] for i in proj['media']['items']}
bi(IM['pool-and-blocks-with-parasols'],
   'bloques blancos escalonados sobre una piscina comunitaria con dos sombrillas de brezo',
   'des immeubles blancs en terrasses au-dessus d’une piscine commune avec deux parasols en paille',
   'weiße Terrassenblöcke über einem Gemeinschaftspool mit zwei Strohschirmen',
   'белые террасные корпуса над общим бассейном с двумя соломенными зонтами',
   'مبانٍ بيضاء متدرجة فوق مسبح مشترك مع مظلتين من القش',
   'witte terrasblokken boven een gemeenschappelijk zwembad met twee rieten parasols',
   'białe tarasowe budynki nad wspólnym basenem z dwoma parasolami ze strzechy',
   'hvite terrassebygg over et felles basseng med to stråparasoller',
   'vita terrasshus ovanför en gemensam pool med två halmparasoller')
bi(IM['blocks-above-the-pool'],
   'bloques blancos con terrazas profundas sobre una pequeña piscina, con las colinas detrás',
   'des immeubles blancs aux terrasses profondes au-dessus d’un petit bassin, les collines derrière',
   'weiße Blöcke mit tiefen Terrassen über einem kleinen Pool, dahinter die Hügel',
   'белые корпуса с глубокими террасами над небольшим бассейном, позади холмы',
   'مبانٍ بيضاء بتراسات عميقة فوق مسبح صغير، والتلال في الخلفية',
   'witte blokken met diepe terrassen boven een klein zwembad, de heuvels erachter',
   'białe budynki z głębokimi tarasami nad małym basenem, w tle wzgórza',
   'hvite bygg med dype terrasser over et lite basseng, åsene bak',
   'vita hus med djupa terrasser ovanför en liten pool, kullarna bakom')
bi(IM['blocks-and-the-sierra'],
   'bloques en torno a las piscinas y los jardines, con la sierra al fondo',
   'des immeubles autour des piscines et des jardins, la sierra au loin',
   'Blöcke rund um die Pools und Gärten, im Hintergrund die Sierra',
   'корпуса вокруг бассейнов и садов, вдали горы',
   'مبانٍ حول المسابح والحدائق، والجبال في الأفق',
   'blokken rond de zwembaden en tuinen, met de sierra op de achtergrond',
   'budynki wokół basenów i ogrodów, w tle góry',
   'bygg rundt bassengene og hagene, med fjellene i bakgrunnen',
   'hus runt poolerna och trädgårdarna, med bergen i bakgrunden')
bi(IM['pool-and-planted-terraces'],
   'una piscina comunitaria bajo terrazas ajardinadas y bloques blancos',
   'une piscine commune sous des terrasses plantées et des immeubles blancs',
   'ein Gemeinschaftspool unter bepflanzten Terrassen und weißen Blöcken',
   'общий бассейн под озеленёнными террасами и белыми корпусами',
   'مسبح مشترك أسفل تراسات مزروعة ومبانٍ بيضاء',
   'een gemeenschappelijk zwembad onder beplante terrassen en witte blokken',
   'wspólny basen pod zazielenionymi tarasami i białymi budynkami',
   'et felles basseng under beplantede terrasser og hvite bygg',
   'en gemensam pool nedanför planterade terrasser och vita hus')
bi(IM['pool-with-loungers'],
   'tumbonas y una sombrilla de brezo junto a la piscina',
   'des transats et un parasol en paille au bord de la piscine',
   'Liegen und ein Strohschirm am Pool',
   'шезлонги и соломенный зонт у бассейна',
   'كراسي استلقاء ومظلة من القش بجانب المسبح',
   'ligbedden en een rieten parasol bij het zwembad',
   'leżaki i parasol ze strzechy przy basenie',
   'solsenger og en stråparasoll ved bassenget',
   'solsängar och en halmparasoll vid poolen')
cg(IM['terrace-to-the-sea'],
   'de una terraza de la planta superior con sofás de exterior y buganvilla, con el mar al fondo',
   'd’une terrasse du dernier étage avec canapés d’extérieur et bougainvillier, la mer au loin',
   'einer Terrasse im obersten Geschoss mit Outdoor-Sofas und Bougainvillea, dahinter das Meer',
   'терраса верхнего этажа с уличными диванами и бугенвиллеей, вдали море',
   'لتراس في الطابق العلوي مع أرائك خارجية وجهنمية، والبحر في الأفق',
   'van een terras op de bovenste verdieping met buitenbanken en bougainville, de zee op de achtergrond',
   'tarasu na najwyższym piętrze z sofami ogrodowymi i bugenwillą, w tle morze',
   'av en terrasse i øverste etasje med utesofaer og bougainvillea, havet i bakgrunnen',
   'av en terrass på översta våningen med utesoffor och bougainvillea, havet i bakgrunden')
cg(IM['porch-and-garden'],
   'del porche y el césped privado de una vivienda en planta baja, con dos tumbonas',
   'du porche et de la pelouse privative d’un rez-de-chaussée, avec deux transats',
   'der Veranda und des privaten Rasens einer Erdgeschosswohnung mit zwei Liegen',
   'веранда и частный газон квартиры на первом этаже с двумя шезлонгами',
   'لشرفة مسقوفة وعشب خاص لشقة في الطابق الأرضي مع كرسيَّي استلقاء',
   'van de veranda en het eigen gazon van een benedenwoning, met twee ligbedden',
   'werandy i prywatnego trawnika mieszkania na parterze z dwoma leżakami',
   'av verandaen og den private plenen til en leilighet i første etasje, med to solsenger',
   'av verandan och den egna gräsmattan till en bottenvåning, med två solsängar')
cg(IM['living-room'],
   'de un salón abierto a la cocina y a la mesa de comedor',
   'd’un séjour ouvert sur la cuisine et la table à manger',
   'eines Wohnzimmers, offen zur Küche und zum Esstisch',
   'гостиная, открытая на кухню и обеденный стол',
   'لغرفة معيشة مفتوحة على المطبخ وطاولة الطعام',
   'van een woonkamer die openloopt naar de keuken en de eettafel',
   'salonu otwartego na kuchnię i stół jadalny',
   'av en stue åpen mot kjøkkenet og spisebordet',
   'av ett vardagsrum öppet mot köket och matbordet')
cg(IM['dining-area'],
   'del comedor junto a la cocina abierta',
   'de l’espace repas à côté de la cuisine ouverte',
   'des Essbereichs neben der offenen Küche',
   'обеденная зона рядом с открытой кухней',
   'لمنطقة الطعام بجانب المطبخ المفتوح',
   'van de eethoek naast de open keuken',
   'jadalni obok otwartej kuchni',
   'av spiseplassen ved det åpne kjøkkenet',
   'av matplatsen vid det öppna köket')
cg(IM['kitchen'],
   'de la cocina con muebles altos en acabado madera y barra de desayuno',
   'de la cuisine avec meubles hauts façon bois et bar',
   'der Küche mit Hängeschränken in Holzoptik und Frühstückstheke',
   'кухня с верхними шкафами под дерево и барной стойкой',
   'للمطبخ مع خزائن علوية بلمسة خشبية ومنضدة إفطار',
   'van de keuken met bovenkasten in houtlook en een ontbijtbar',
   'kuchni z górnymi szafkami w wykończeniu drewnopodobnym i barkiem',
   'av kjøkkenet med overskap i treutførelse og frokostbar',
   'av köket med överskåp i träfinish och frukostbar')
cg(IM['bedroom'],
   'de un dormitorio con puerta corredera a la terraza',
   'd’une chambre avec porte coulissante sur la terrasse',
   'eines Schlafzimmers mit Schiebetür zur Terrasse',
   'спальня с раздвижной дверью на террасу',
   'لغرفة نوم بباب منزلق إلى التراس',
   'van een slaapkamer met een schuifpui naar het terras',
   'sypialni z przesuwnymi drzwiami na taras',
   'av et soverom med skyvedør ut til terrassen',
   'av ett sovrum med skjutdörr ut mot terrassen')
cg(IM['bathroom'],
   'de un baño con mueble de lavabo y ducha a ras de suelo',
   'd’une salle de bains avec meuble vasque et douche à l’italienne',
   'eines Bades mit Waschtischunterschrank und bodengleicher Dusche',
   'ванная с тумбой под раковину и душем без поддона',
   'لحمّام مع خزانة مغسلة ودش مفتوح',
   'van een badkamer met een wastafelmeubel en een inloopdouche',
   'łazienki z szafką pod umywalką i prysznicem typu walk-in',
   'av et bad med servantskap og dusjhjørne',
   'av ett badrum med tvättställsskåp och dusch i golvnivå')
cg(IM['spa-pool'],
   'de la piscina cubierta del spa bajo un lucernario, con un jacuzzi en primer plano',
   'de la piscine intérieure du spa sous une verrière, avec un jacuzzi au premier plan',
   'des Innenpools im Spa unter einem Oberlicht, vorne ein Whirlpool',
   'крытый бассейн спа под световым фонарём, на переднем плане джакузи',
   'لمسبح السبا الداخلي تحت كوة سقفية، مع جاكوزي في المقدمة',
   'van het binnenzwembad van de spa onder een lichtkoepel, met een bubbelbad op de voorgrond',
   'krytego basenu w spa pod świetlikiem, na pierwszym planie jacuzzi',
   'av innendørsbassenget i spaet under et takvindu, med boblebad i forgrunnen',
   'av spaets inomhuspool under ett takfönster, med bubbelpool i förgrunden')

a('.media.items[1].caption', 'Hacia la sierra', 'Vers la sierra', 'Zur Sierra', 'Вид на горы', 'نحو الجبال',
  'Richting de sierra', 'W stronę gór', 'Mot fjellene', 'Mot bergen')
a('.media.items[4].caption', 'Junto a la piscina', 'Au bord de la piscine', 'Am Pool', 'У бассейна', 'بجانب المسبح',
  'Bij het zwembad', 'Przy basenie', 'Ved bassenget', 'Vid poolen')
a('.media.headlineHtml', 'El conjunto en <em>detalle</em>', 'La résidence en <em>détail</em>', 'Die Anlage im <em>Detail</em>',
  'Комплекс <em>в деталях</em>', 'المجمع <em>بالتفصيل</em>', 'Het complex in <em>detail</em>',
  'Osiedle <em>w szczegółach</em>', 'Anlegget i <em>detalj</em>', 'Området i <em>detalj</em>')
a('.media.copy',
  'Imágenes del folleto y de la memoria de calidades del promotor: los bloques, las piscinas y los jardines, el spa, las terrazas y los interiores.',
  'Images de la brochure et du descriptif technique du promoteur : les immeubles, les piscines et les jardins, le spa, les terrasses et les intérieurs.',
  'Bilder aus der Broschüre und der Baubeschreibung des Bauträgers: die Blöcke, die Pools und Gärten, das Spa, die Terrassen und die Innenräume.',
  'Изображения из буклета и спецификации застройщика: корпуса, бассейны и сады, спа, террасы и интерьеры.',
  'صور من كتيّب المطوّر ومواصفات البناء: المباني والمسابح والحدائق والسبا والتراسات والتصاميم الداخلية.',
  'Beelden uit de brochure en de technische omschrijving van de ontwikkelaar: de blokken, de zwembaden en tuinen, de spa, de terrassen en de interieurs.',
  'Zdjęcia z broszury i specyfikacji technicznej dewelopera: budynki, baseny i ogrody, spa, tarasy i wnętrza.',
  'Bilder fra utbyggerens brosjyre og byggebeskrivelse: byggene, bassengene og hagene, spaet, terrassene og interiørene.',
  'Bilder ur exploatörens broschyr och byggbeskrivning: husen, poolerna och trädgårdarna, spaet, terrasserna och interiörerna.')
a('.media.note',
  'Las imágenes proceden del folleto del promotor para todo el conjunto. Son ilustraciones, no fotografías de las viviendas en venta, y el folleto indica que el mobiliario no está incluido y que los edificios terminados pueden diferir. Los planos son las fichas provisionales del propio promotor para cada vivienda, sin el logotipo ni el nombre del proyecto; los nombres de las estancias están en español y no son contractuales.',
  'Les images proviennent de la brochure du promoteur pour l’ensemble de la résidence. Ce sont des illustrations, non des photographies des logements en vente, et la brochure précise que le mobilier n’est pas inclus et que les bâtiments achevés peuvent différer. Les plans sont les fiches provisoires du promoteur pour chaque logement, sans le logo ni le nom du projet ; les pièces y sont nommées en espagnol et ils ne sont pas contractuels.',
  'Die Bilder stammen aus der Broschüre des Bauträgers für die gesamte Anlage. Es sind Illustrationen, keine Fotos der angebotenen Wohnungen; laut Broschüre sind die Möbel nicht enthalten, und die fertigen Gebäude können abweichen. Die Grundrisse sind die vorläufigen Blätter des Bauträgers für jede Wohnung, ohne Logo und Projektnamen; die Raumbezeichnungen sind spanisch, und die Pläne sind nicht vertraglich bindend.',
  'Изображения взяты из буклета застройщика по всему комплексу. Это иллюстрации, а не фотографии продаваемых квартир; в буклете указано, что мебель не входит в стоимость, а готовые здания могут отличаться. Планировки — предварительные листы застройщика для каждой квартиры без логотипа и названия проекта; названия помещений на испанском, договорной силы они не имеют.',
  'الصور مأخوذة من كتيّب المطوّر للمجمع بأكمله. وهي رسوم توضيحية وليست صوراً فوتوغرافية للشقق المعروضة للبيع، ويذكر الكتيّب أن الأثاث غير مشمول وأن المباني المنجزة قد تختلف. أما المخططات فهي أوراق المطوّر المؤقتة لكل شقة بعد إزالة الشعار واسم المشروع، وأسماء الغرف فيها بالإسبانية، وهي غير ملزمة تعاقدياً.',
  'De beelden komen uit de brochure van de ontwikkelaar voor het hele complex. Het zijn illustraties, geen foto’s van de woningen die te koop staan; volgens de brochure is het meubilair niet inbegrepen en kunnen de afgewerkte gebouwen afwijken. De plattegronden zijn de voorlopige bladen van de ontwikkelaar per woning, zonder logo en projectnaam; de ruimtenamen zijn Spaans en de plannen zijn niet contractueel.',
  'Zdjęcia pochodzą z broszury dewelopera dla całego osiedla. Są to ilustracje, a nie fotografie mieszkań w sprzedaży; broszura zaznacza, że meble nie są wliczone, a gotowe budynki mogą się różnić. Rzuty to tymczasowe karty dewelopera dla każdego mieszkania, bez logo i nazwy projektu; nazwy pomieszczeń są po hiszpańsku i nie mają mocy umownej.',
  'Bildene er hentet fra utbyggerens brosjyre for hele anlegget. De er illustrasjoner, ikke fotografier av boligene som selges, og brosjyren sier at møbler ikke er inkludert og at de ferdige byggene kan avvike. Plantegningene er utbyggerens foreløpige ark for hver bolig, uten logo og prosjektnavn; romnavnene er på spansk, og tegningene er ikke kontraktsfestet.',
  'Bilderna kommer från exploatörens broschyr för hela området. De är illustrationer, inte fotografier av bostäderna som säljs, och broschyren anger att möbler inte ingår och att de färdiga husen kan avvika. Planritningarna är exploatörens preliminära blad för varje bostad, utan logotyp och projektnamn; rumsnamnen är på spanska och ritningarna är inte kontraktsbindande.')

# ---- overview ---------------------------------------------------------------------------------
a('.overview.headlineHtml', 'Veintiséis viviendas, <em>seis bloques</em>', 'Vingt-six logements, <em>six immeubles</em>',
  'Sechsundzwanzig Wohnungen, <em>sechs Blöcke</em>', 'Двадцать шесть квартир, <em>шесть корпусов</em>',
  'ست وعشرون شقة، <em>ستة مبانٍ</em>', 'Zesentwintig woningen, <em>zes blokken</em>',
  'Dwadzieścia sześć mieszkań, <em>sześć budynków</em>', 'Tjueseks boliger, <em>seks bygg</em>',
  'Tjugosex bostäder, <em>sex hus</em>')
a('.overview.copy[0]',
  'Selwo Garden Residences es el nombre que damos a dos fases posteriores de un conjunto cerrado más amplio en Estepona, junto al parque Selwo Aventura, con bloques blancos de poca altura en torno a jardines y piscinas. Veintiséis apartamentos de seis de sus bloques figuran como disponibles en el portal para agentes del promotor.',
  'Selwo Garden Residences est le nom que nous donnons à deux phases ultérieures d’une résidence fermée plus vaste à Estepona, à côté du parc animalier Selwo Aventura, avec des immeubles blancs de faible hauteur autour de jardins et de piscines. Vingt-six appartements répartis dans six de ses immeubles figurent comme disponibles sur le portail agents du promoteur.',
  'Selwo Garden Residences ist unser Name für zwei spätere Bauabschnitte einer größeren geschlossenen Anlage in Estepona, neben dem Tierpark Selwo Aventura, mit niedrigen weißen Blöcken rund um Gärten und Pools. Sechsundzwanzig Wohnungen in sechs ihrer Blöcke sind im Maklerportal des Bauträgers als verfügbar geführt.',
  'Selwo Garden Residences — так мы называем две более поздние очереди большого закрытого комплекса в Эстепоне рядом с парком Selwo Aventura: невысокие белые корпуса среди садов и бассейнов. На агентском портале застройщика свободными значатся двадцать шесть квартир в шести его корпусах.',
  'سيلوو غاردن ريزيدنسز هو الاسم الذي نطلقه على مرحلتين لاحقتين من مجمع مغلق أكبر في إستيبونا، بجوار حديقة سيلوو أفينتورا للحيوانات، بمبانٍ بيضاء منخفضة حول الحدائق والمسابح. وتظهر ست وعشرون شقة في ستة من مبانيه متاحةً على بوابة الوكلاء لدى المطوّر.',
  'Selwo Garden Residences is de naam die wij geven aan twee latere fasen van een groter omheind complex in Estepona, naast het dierenpark Selwo Aventura, met lage witte blokken rond tuinen en zwembaden. Zesentwintig appartementen in zes van de blokken staan in het makelaarsportaal van de ontwikkelaar als beschikbaar.',
  'Selwo Garden Residences to nazwa, którą nadajemy dwóm późniejszym etapom większego zamkniętego osiedla w Esteponie, obok parku zwierząt Selwo Aventura, z niskimi białymi budynkami wśród ogrodów i basenów. Na portalu dla agentów dewelopera jako dostępne figuruje dwadzieścia sześć apartamentów w sześciu budynkach.',
  'Selwo Garden Residences er navnet vi gir to senere byggetrinn i et større inngjerdet anlegg i Estepona, ved dyreparken Selwo Aventura, med lave hvite bygg rundt hager og bassenger. Tjueseks leiligheter i seks av byggene står som ledige i utbyggerens meglerportal.',
  'Selwo Garden Residences är namnet vi ger två senare etapper av ett större inhägnat område i Estepona, intill djurparken Selwo Aventura, med låga vita hus kring trädgårdar och pooler. Tjugosex lägenheter i sex av husen står som lediga i exploatörens mäklarportal.')
a('.overview.copy[1]',
  'Las viviendas disponibles tienen uno, dos o tres dormitorios y van de {N87.89} a {N148.27} {U} construidos, con {N63.20} a {N105.52} {U} útiles. Todas tienen terraza, de {N18.37} a {N155.46} {U}. Según sus planos, cinco de las viviendas en planta baja suman un jardín privado de {N8.78} a {N82.23} {U}.',
  'Les logements disponibles ont une, deux ou trois chambres et vont de {N87.89} à {N148.27} {U} construits, pour {N63.20} à {N105.52} {U} de surface utile. Tous ont une terrasse, de {N18.37} à {N155.46} {U}. Selon leur plan, cinq des logements en rez-de-chaussée y ajoutent un jardin privatif de {N8.78} à {N82.23} {U}.',
  'Die verfügbaren Wohnungen haben ein, zwei oder drei Schlafzimmer und {N87.89} bis {N148.27} {U} bebaute Fläche bei {N63.20} bis {N105.52} {U} Wohnfläche. Alle haben eine Terrasse von {N18.37} bis {N155.46} {U}. Laut Grundriss haben fünf der Erdgeschosswohnungen zusätzlich einen privaten Garten von {N8.78} bis {N82.23} {U}.',
  'В свободных квартирах одна, две или три спальни, площадь застройки от {N87.89} до {N148.27} {U} при полезной площади от {N63.20} до {N105.52} {U}. У каждой есть терраса площадью от {N18.37} до {N155.46} {U}. По планировкам у пяти квартир на первом этаже есть ещё частный сад от {N8.78} до {N82.23} {U}.',
  'تضم الشقق المتاحة غرفة أو غرفتين أو ثلاث غرف نوم، وتتراوح مساحتها المبنية بين {N87.89} و{N148.27} {U}، والصافية بين {N63.20} و{N105.52} {U}. ولكل منها تراس من {N18.37} إلى {N155.46} {U}. وبحسب المخططات، تضيف خمس شقق في الطابق الأرضي حديقة خاصة من {N8.78} إلى {N82.23} {U}.',
  'De beschikbare woningen hebben één, twee of drie slaapkamers en meten {N87.89} tot {N148.27} {U} bebouwd, met {N63.20} tot {N105.52} {U} nuttige oppervlakte. Elke woning heeft een terras van {N18.37} tot {N155.46} {U}. Volgens hun plattegrond hebben vijf benedenwoningen daarnaast een eigen tuin van {N8.78} tot {N82.23} {U}.',
  'Dostępne mieszkania mają jedną, dwie lub trzy sypialnie i od {N87.89} do {N148.27} {U} powierzchni zabudowy przy {N63.20} do {N105.52} {U} powierzchni użytkowej. Każde ma taras od {N18.37} do {N155.46} {U}. Według rzutów pięć mieszkań na parterze ma dodatkowo prywatny ogród od {N8.78} do {N82.23} {U}.',
  'De ledige boligene har ett, to eller tre soverom og {N87.89} til {N148.27} {U} bebygd areal, med {N63.20} til {N105.52} {U} bruksareal. Alle har terrasse, fra {N18.37} til {N155.46} {U}. Etter plantegningene har fem av leilighetene i første etasje i tillegg en privat hage på {N8.78} til {N82.23} {U}.',
  'De lediga bostäderna har ett, två eller tre sovrum och {N87.89} till {N148.27} {U} byggyta, med {N63.20} till {N105.52} {U} nyttoyta. Alla har terrass, från {N18.37} till {N155.46} {U}. Enligt planritningarna har fem av bottenvåningarna dessutom en egen trädgård på {N8.78} till {N82.23} {U}.')
a('.overview.copy[2]',
  'Los documentos del promotor incluyen entre las zonas comunes dos piscinas exteriores para adultos y niños, un spa, un gimnasio, una sala de coworking, una sala de cine y un Youth Club. Cada vivienda figura con al menos una plaza de garaje y un trastero, con precio en líneas aparte.',
  'Les documents du promoteur comptent parmi les espaces communs deux piscines extérieures pour adultes et enfants, un spa, une salle de sport, un espace de coworking, une salle de cinéma et un club pour les jeunes. Chaque logement est listé avec au moins une place de parking et une cave, chiffrées sur des lignes séparées.',
  'Die Unterlagen des Bauträgers nennen als Gemeinschaftsbereiche zwei Außenpools für Erwachsene und Kinder, ein Spa, einen Fitnessraum, einen Coworking-Raum, einen Kinoraum und einen Jugendclub. Jede Wohnung ist mit mindestens einem Stellplatz und einem Abstellraum gelistet, die als eigene Positionen bepreist sind.',
  'В документах застройщика среди общих зон указаны два открытых бассейна для взрослых и детей, спа, тренажёрный зал, коворкинг, кинозал и молодёжный клуб. Каждая квартира значится как минимум с одним машиноместом и одной кладовой, цены на которые указаны отдельными строками.',
  'تذكر وثائق المطوّر ضمن المرافق المشتركة مسبحين خارجيين للكبار والأطفال، وسبا، وصالة رياضية، ومساحة عمل مشتركة، وقاعة سينما، ونادياً للشباب. وتُدرج كل شقة مع موقف سيارة واحد ومخزن واحد على الأقل، بسعر مستقل لكل منهما.',
  'De documenten van de ontwikkelaar noemen als gemeenschappelijke voorzieningen twee buitenzwembaden voor volwassenen en kinderen, een spa, een fitnessruimte, een coworkingruimte, een bioscoopzaal en een jongerenclub. Elke woning staat vermeld met ten minste één parkeerplaats en één berging, apart geprijsd.',
  'Dokumenty dewelopera wymieniają wśród części wspólnych dwa baseny zewnętrzne dla dorosłych i dzieci, spa, siłownię, coworking, salę kinową i klub młodzieżowy. Każde mieszkanie figuruje z co najmniej jednym miejscem parkingowym i jedną komórką lokatorską, wycenionymi w osobnych pozycjach.',
  'Utbyggerens dokumenter nevner blant fellesarealene to utendørs bassenger for voksne og barn, et spa, et treningsrom, et kontorfellesskap, et kinorom og en ungdomsklubb. Hver bolig er oppført med minst én parkeringsplass og én bod, priset på egne linjer.',
  'Exploatörens dokument nämner bland de gemensamma ytorna två utomhuspooler för vuxna och barn, ett spa, ett gym, ett coworkingrum, en biosalong och en ungdomsklubb. Varje bostad listas med minst en parkeringsplats och ett förråd, prissatta på egna rader.')
a('.overview.metrics[0][1]', '26 viviendas', '26 logements', '26 Wohnungen', '26 квартир', '26 شقة', '26 woningen',
  '26 mieszkań', '26 boliger', '26 bostäder')

# ---- residences -------------------------------------------------------------------------------
a('.residences.headlineHtml', 'De uno <em>a tres dormitorios</em>', 'D’une <em>à trois chambres</em>',
  'Ein bis <em>drei Schlafzimmer</em>', 'От одной <em>до трёх спален</em>', 'من غرفة <em>إلى ثلاث غرف نوم</em>',
  'Eén tot <em>drie slaapkamers</em>', 'Od jednej <em>do trzech sypialni</em>', 'Ett til <em>tre soverom</em>',
  'Ett till <em>tre sovrum</em>')
a('.residences.copy',
  'Apartamentos en planta baja, primera y segunda de bloques de tres plantas, que varían en superficie, terraza y orientación. La tabla sigue el portal para agentes del promotor.',
  'Des appartements en rez-de-chaussée, au premier et au deuxième étage d’immeubles de trois niveaux, qui varient par la surface, la terrasse et l’orientation. Le tableau suit le portail agents du promoteur.',
  'Wohnungen im Erdgeschoss, ersten und zweiten Obergeschoss dreigeschossiger Blöcke, unterschiedlich in Fläche, Terrasse und Ausrichtung. Die Tabelle folgt dem Maklerportal des Bauträgers.',
  'Квартиры на первом, втором и третьем этажах трёхэтажных корпусов, различающиеся площадью, террасой и ориентацией. Таблица составлена по агентскому порталу застройщика.',
  'شقق في الطابق الأرضي والأول والثاني من مبانٍ من ثلاثة طوابق، تختلف في المساحة والتراس والاتجاه. ويتبع الجدول بوابة الوكلاء لدى المطوّر.',
  'Appartementen op de begane grond, eerste en tweede verdieping van blokken met drie bouwlagen, verschillend in oppervlakte, terras en oriëntatie. De tabel volgt het makelaarsportaal van de ontwikkelaar.',
  'Mieszkania na parterze, pierwszym i drugim piętrze trzykondygnacyjnych budynków, różniące się powierzchnią, tarasem i orientacją. Tabela odpowiada portalowi dla agentów dewelopera.',
  'Leiligheter i første, andre og tredje etasje i bygg med tre etasjer, med ulik størrelse, terrasse og retning. Tabellen følger utbyggerens meglerportal.',
  'Lägenheter på botten-, första och andra våningen i hus med tre våningar, med olika storlek, terrass och väderstreck. Tabellen följer exploatörens mäklarportal.')
a('.residences.items[0].points[0]',
  'Una vivienda en planta baja de un dormitorio, doce de dos dormitorios y trece de tres. La de un dormitorio tiene un baño y las demás dos; cuatro viviendas de tres dormitorios en segunda planta suman un tercero, que los planos que tenemos muestran como aseo.',
  'Un logement d’une chambre en rez-de-chaussée, douze de deux chambres et treize de trois. Celui d’une chambre a une salle d’eau et les autres deux ; quatre logements de trois chambres au deuxième étage en ajoutent une troisième, que les plans en notre possession montrent comme un WC invités.',
  'Eine Erdgeschosswohnung mit einem Schlafzimmer, zwölf mit zwei und dreizehn mit drei Schlafzimmern. Die Einzimmerwohnung hat ein Bad, die übrigen zwei; vier Dreizimmerwohnungen im zweiten Obergeschoss haben ein drittes, das die uns vorliegenden Grundrisse als Gäste-WC zeigen.',
  'Одна квартира с одной спальней на первом этаже, двенадцать с двумя и тринадцать с тремя спальнями. В квартире с одной спальней один санузел, в остальных по два; в четырёх трёхспальных квартирах на третьем этаже есть третий, который на имеющихся у нас планировках показан как гостевой туалет.',
  'شقة واحدة بغرفة نوم واحدة في الطابق الأرضي، واثنتا عشرة بغرفتين، وثلاث عشرة بثلاث غرف. للشقة ذات الغرفة الواحدة حمّام واحد وللبقية حمّامان، وتضيف أربع شقق بثلاث غرف في الطابق الثاني حمّاماً ثالثاً تُظهره المخططات المتوفرة لدينا كدورة مياه للضيوف.',
  'Eén benedenwoning met één slaapkamer, twaalf met twee en dertien met drie slaapkamers. De woning met één slaapkamer heeft één badkamer, de andere twee; vier driekamerwoningen op de tweede verdieping hebben een derde, die de plattegronden die wij hebben als gastentoilet tonen.',
  'Jedno mieszkanie z jedną sypialnią na parterze, dwanaście z dwiema i trzynaście z trzema sypialniami. Mieszkanie z jedną sypialnią ma jedną łazienkę, pozostałe dwie; cztery mieszkania z trzema sypialniami na drugim piętrze mają trzecią, którą posiadane przez nas rzuty pokazują jako toaletę dla gości.',
  'Én leilighet med ett soverom i første etasje, tolv med to og tretten med tre soverom. Leiligheten med ett soverom har ett bad og de øvrige to; fire treromsleiligheter i tredje etasje har et tredje, som plantegningene vi har viser som gjestetoalett.',
  'En bottenvåning med ett sovrum, tolv med två och tretton med tre sovrum. Bostaden med ett sovrum har ett badrum och de övriga två; fyra treor på andra våningen har ett tredje, som planritningarna vi har visar som gästtoalett.')
a('.residences.items[0].points[1]',
  'Terraza en todas las viviendas, de {N18.37} a {N155.46} {U}. Las mayores corresponden a cuatro viviendas de tres dormitorios en segunda planta, y en las dos de las que tenemos planos la terraza es una cubierta privada de unos 138 {U}.',
  'Une terrasse pour chaque logement, de {N18.37} à {N155.46} {U}. Les plus grandes appartiennent à quatre logements de trois chambres au deuxième étage ; sur les deux dont nous avons le plan, il s’agit d’un toit-terrasse privatif d’environ 138 {U}.',
  'Eine Terrasse bei jeder Wohnung, von {N18.37} bis {N155.46} {U}. Die größten gehören zu vier Dreizimmerwohnungen im zweiten Obergeschoss; bei den beiden, deren Grundriss uns vorliegt, ist es eine private Dachterrasse von rund 138 {U}.',
  'Терраса у каждой квартиры, от {N18.37} до {N155.46} {U}. Самые большие — у четырёх трёхспальных квартир на третьем этаже; у двух из них, планировки которых у нас есть, это частная терраса на крыше площадью около 138 {U}.',
  'تراس لكل شقة من {N18.37} إلى {N155.46} {U}. والأكبر منها لأربع شقق بثلاث غرف في الطابق الثاني، وفي الشقتين اللتين نملك مخططيهما يكون التراس سطحاً خاصاً بمساحة نحو 138 {U}.',
  'Een terras bij elke woning, van {N18.37} tot {N155.46} {U}. De grootste horen bij vier driekamerwoningen op de tweede verdieping; bij de twee waarvan wij de plattegrond hebben, is het een eigen dakterras van ongeveer 138 {U}.',
  'Taras przy każdym mieszkaniu, od {N18.37} do {N155.46} {U}. Największe należą do czterech mieszkań z trzema sypialniami na drugim piętrze; w dwóch, których rzuty posiadamy, jest to prywatny taras na dachu o powierzchni około 138 {U}.',
  'Terrasse til hver bolig, fra {N18.37} til {N155.46} {U}. De største hører til fire treromsleiligheter i tredje etasje, og på de to vi har plantegning for, er terrassen en privat takterrasse på rundt 138 {U}.',
  'Terrass till varje bostad, från {N18.37} till {N155.46} {U}. De största hör till fyra treor på andra våningen, och på de två vi har planritning för är terrassen en egen takterrass på omkring 138 {U}.')
a('.residences.items[0].points[2]',
  'En los planos de cinco viviendas en planta baja, un jardín privado de {N8.78} a {N82.23} {U} más allá de la terraza.',
  'Sur le plan de cinq logements en rez-de-chaussée, un jardin privatif de {N8.78} à {N82.23} {U} au-delà de la terrasse.',
  'Laut Grundriss von fünf Erdgeschosswohnungen ein privater Garten von {N8.78} bis {N82.23} {U} jenseits der Terrasse.',
  'На планировках пяти квартир первого этажа — частный сад от {N8.78} до {N82.23} {U} за террасой.',
  'في مخططات خمس شقق في الطابق الأرضي، حديقة خاصة من {N8.78} إلى {N82.23} {U} بعد التراس.',
  'Op de plattegrond van vijf benedenwoningen een eigen tuin van {N8.78} tot {N82.23} {U} achter het terras.',
  'Na rzutach pięciu mieszkań na parterze prywatny ogród od {N8.78} do {N82.23} {U} za tarasem.',
  'På plantegningene til fem leiligheter i første etasje, en privat hage på {N8.78} til {N82.23} {U} utenfor terrassen.',
  'På planritningarna för fem bottenvåningar en egen trädgård på {N8.78} till {N82.23} {U} bortom terrassen.')
a('.residences.items[0].points[3]',
  'La mayoría de las viviendas disponibles está orientada al este o al sureste, según el listado; una mira al sur y otra al noreste.',
  'La plupart des logements disponibles sont orientés est ou sud-est, selon la liste ; un est orienté sud et un nord-est.',
  'Die meisten verfügbaren Wohnungen sind laut Liste nach Osten oder Südosten ausgerichtet; eine nach Süden und eine nach Nordosten.',
  'Большинство свободных квартир, согласно списку, ориентированы на восток или юго-восток; одна — на юг и одна — на северо-восток.',
  'معظم الشقق المتاحة موجهة نحو الشرق أو الجنوب الشرقي بحسب القائمة، وواحدة نحو الجنوب وأخرى نحو الشمال الشرقي.',
  'De meeste beschikbare woningen liggen volgens de lijst op het oosten of zuidoosten; één op het zuiden en één op het noordoosten.',
  'Większość dostępnych mieszkań ma według listy orientację wschodnią lub południowo-wschodnią; jedno południową, a jedno północno-wschodnią.',
  'De fleste ledige boligene vender mot øst eller sørøst, ifølge listen; én vender mot sør og én mot nordøst.',
  'De flesta lediga bostäderna vetter mot öster eller sydost enligt listan; en mot söder och en mot nordost.')
a('.residences.items[0].points[4]',
  'Cocina equipada con placa de inducción, horno eléctrico, campana extractora, lavavajillas panelado, frigorífico y lavadora.',
  'Une cuisine équipée avec plaque à induction, four électrique, hotte, lave-vaisselle intégré, réfrigérateur et lave-linge.',
  'Eine Einbauküche mit Induktionskochfeld, Elektrobackofen, Dunstabzugshaube, integriertem Geschirrspüler, Kühlschrank und Waschmaschine.',
  'Оборудованная кухня с индукционной варочной панелью, электрической духовкой, вытяжкой, встроенной посудомоечной машиной, холодильником и стиральной машиной.',
  'مطبخ مجهّز بموقد حثّي وفرن كهربائي وشفاط وغسالة صحون مدمجة وثلاجة وغسالة ملابس.',
  'Een ingerichte keuken met inductiekookplaat, elektrische oven, afzuigkap, ingebouwde vaatwasser, koelkast en wasmachine.',
  'Wyposażona kuchnia z płytą indukcyjną, piekarnikiem elektrycznym, okapem, zabudowaną zmywarką, lodówką i pralką.',
  'Et innredet kjøkken med induksjonstopp, elektrisk stekeovn, kjøkkenvifte, integrert oppvaskmaskin, kjøleskap og vaskemaskin.',
  'Ett utrustat kök med induktionshäll, elektrisk ugn, köksfläkt, integrerad diskmaskin, kylskåp och tvättmaskin.')
a('.residences.items[0].points[5]',
  'Aire acondicionado por conductos frío-calor, bomba de calor aerotérmica para el agua caliente y persianas motorizadas en los dormitorios.',
  'Climatisation gainable chaud-froid, pompe à chaleur aérothermique pour l’eau chaude et volets roulants motorisés dans les chambres.',
  'Kanalklimaanlage für Wärme und Kühlung, Luftwärmepumpe für das Warmwasser und motorisierte Rollläden in den Schlafzimmern.',
  'Канальный кондиционер на тепло и холод, аэротермальный тепловой насос для горячей воды и моторизованные рольставни в спальнях.',
  'تكييف بمجارٍ للتدفئة والتبريد، ومضخة حرارية هوائية للمياه الساخنة، وستائر دوّارة آلية في غرف النوم.',
  'Kanaalairconditioning voor verwarming en koeling, een luchtwarmtepomp voor warm water en gemotoriseerde rolluiken in de slaapkamers.',
  'Kanałowa klimatyzacja z funkcją grzania i chłodzenia, powietrzna pompa ciepła do ciepłej wody i zmotoryzowane rolety w sypialniach.',
  'Kanalbasert klimaanlegg for varme og kjøling, luft-til-vann-varmepumpe for varmtvann og motoriserte rullesjalusier på soverommene.',
  'Kanalbaserad luftkonditionering för värme och kyla, luftvärmepump för varmvatten och motoriserade rullgardiner i sovrummen.')

# ---- quality specs ------------------------------------------------------------------------------
a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor, sin fecha impresa, que indica que sus imágenes son una aproximación al resultado final, que pueden introducirse cambios por motivos técnicos o jurídicos y que el mobiliario no está incluido. Se facilitó el mismo documento para ambas fases.',
  'Source : le descriptif technique du promoteur, sans date imprimée, qui précise que ses images sont une approximation du résultat final, que des modifications peuvent intervenir pour des raisons techniques ou juridiques et que le mobilier n’est pas inclus. Le même document a été fourni pour les deux phases.',
  'Quelle: die Baubeschreibung des Bauträgers ohne aufgedrucktes Datum. Sie nennt ihre Bilder eine Annäherung an das Endergebnis, behält Änderungen aus technischen oder rechtlichen Gründen vor und schließt Möbel aus. Für beide Bauabschnitte wurde dasselbe Dokument geliefert.',
  'Источник: спецификация застройщика без даты, в которой сказано, что изображения лишь приближённо передают итоговый результат, что возможны изменения по техническим или юридическим причинам и что мебель не входит в стоимость. Для обеих очередей предоставлен один и тот же документ.',
  'المصدر: مواصفات البناء لدى المطوّر، وهي غير مؤرخة، وتذكر أن صورها تقريبية للنتيجة النهائية، وأن تغييرات قد تُدخل لأسباب فنية أو قانونية، وأن الأثاث غير مشمول. وقد قُدّمت الوثيقة نفسها للمرحلتين.',
  'Bron: de technische omschrijving van de ontwikkelaar, zonder gedrukte datum, die vermeldt dat de beelden een benadering van het eindresultaat zijn, dat er om technische of juridische redenen wijzigingen kunnen komen en dat het meubilair niet is inbegrepen. Voor beide fasen is hetzelfde document aangeleverd.',
  'Źródło: specyfikacja techniczna dewelopera bez nadrukowanej daty, która podaje, że zdjęcia są przybliżeniem efektu końcowego, że możliwe są zmiany z przyczyn technicznych lub prawnych i że meble nie są wliczone. Dla obu etapów dostarczono ten sam dokument.',
  'Kilde: utbyggerens byggebeskrivelse, uten trykt dato, som sier at bildene er en tilnærming til sluttresultatet, at det kan gjøres endringer av tekniske eller juridiske grunner, og at møbler ikke er inkludert. Det samme dokumentet ble levert for begge byggetrinn.',
  'Källa: exploatörens byggbeskrivning, utan tryckt datum, som anger att bilderna är en uppskattning av slutresultatet, att ändringar kan göras av tekniska eller juridiska skäl och att möbler inte ingår. Samma dokument lämnades för båda etapperna.')
a('.qualitySpecs.groups[0].items[0]',
  'Suelos de gres porcelánico en vestíbulo, salón, dormitorios y pasillo, con rodapié blanco a juego con la carpintería interior.',
  'Sols en grès cérame dans l’entrée, le séjour, les chambres et le couloir, avec plinthes blanches assorties aux portes intérieures.',
  'Feinsteinzeugböden in Diele, Wohnzimmer, Schlafzimmern und Flur, mit weißen Sockelleisten passend zu den Innentüren.',
  'Полы из керамогранита в прихожей, гостиной, спальнях и коридоре, с белым плинтусом в тон межкомнатным дверям.',
  'أرضيات من البورسلان في المدخل وغرفة المعيشة وغرف النوم والممر، مع وزرات بيضاء متناسقة مع الأبواب الداخلية.',
  'Vloeren van keramisch porselein in hal, woonkamer, slaapkamers en gang, met witte plinten passend bij de binnendeuren.',
  'Podłogi z gresu porcelanowego w przedpokoju, salonie, sypialniach i korytarzu, z białymi listwami dopasowanymi do drzwi wewnętrznych.',
  'Gulv i porselensflis i entré, stue, soverom og gang, med hvite fotlister som matcher innerdørene.',
  'Golv av porslinsklinker i hall, vardagsrum, sovrum och korridor, med vita golvlister som matchar innerdörrarna.')
a('.qualitySpecs.groups[0].items[1]',
  'Pintura plástica lisa en las paredes y falso techo en toda la vivienda.',
  'Peinture lisse sur les murs et faux plafonds dans tout le logement.',
  'Glatter Dispersionsanstrich an den Wänden und abgehängte Decken in der ganzen Wohnung.',
  'Гладкая водоэмульсионная окраска стен и подвесные потолки во всей квартире.',
  'طلاء أملس على الجدران وأسقف معلّقة في كامل الشقة.',
  'Gladde latexverf op de wanden en verlaagde plafonds in de hele woning.',
  'Gładka farba emulsyjna na ścianach i sufity podwieszane w całym mieszkaniu.',
  'Glatt plastmaling på veggene og nedsenket himling i hele boligen.',
  'Slät plastfärg på väggarna och undertak i hela bostaden.')
a('.qualitySpecs.groups[1].items[0]',
  'Amueblada con muebles altos y bajos de diseño actual, suelo porcelánico, encimera con entrecalle entre muebles y fregadero con grifería monomando.',
  'Équipée de meubles hauts et bas au design actuel, sol en grès cérame, plan de travail avec crédence entre les meubles et évier avec mitigeur.',
  'Mit Ober- und Unterschränken in zeitgemäßem Design, Feinsteinzeugboden, Arbeitsplatte mit Rückwand zwischen den Schränken und Spüle mit Einhebelmischer.',
  'Мебель — верхние и нижние шкафы в современном дизайне, пол из керамогранита, столешница с фартуком между шкафами и мойка со смесителем.',
  'مزوّد بخزائن علوية وسفلية بتصميم عصري، وأرضية من البورسلان، وسطح عمل مع تكسية بين الخزائن، ومغسلة بخلاط أحادي الذراع.',
  'Ingericht met boven- en onderkasten in eigentijds design, porseleinen vloer, een werkblad met achterwand tussen de kasten en een spoelbak met eengreepsmengkraan.',
  'Wyposażona w szafki górne i dolne o nowoczesnym wzornictwie, podłoga z gresu, blat z panelem między szafkami i zlew z baterią jednouchwytową.',
  'Innredet med over- og underskap i moderne design, gulv i porselensflis, benkeplate med sprutplate mellom skapene og vask med ettgrepsbatteri.',
  'Inrett med över- och underskåp i modern design, golv av porslinsklinker, bänkskiva med stänkskydd mellan skåpen och diskho med engreppsblandare.')
a('.qualitySpecs.groups[1].items[1]',
  'Placa de inducción, campana extractora o grupo filtrante, horno eléctrico, lavavajillas panelado, frigorífico y lavadora.',
  'Plaque à induction, hotte ou groupe filtrant, four électrique, lave-vaisselle intégré, réfrigérateur et lave-linge.',
  'Induktionskochfeld, Dunstabzugshaube oder Umluftmodul, Elektrobackofen, integrierter Geschirrspüler, Kühlschrank und Waschmaschine.',
  'Индукционная панель, вытяжка или фильтрующий блок, электрическая духовка, встроенная посудомоечная машина, холодильник и стиральная машина.',
  'موقد حثّي، وشفاط أو وحدة ترشيح، وفرن كهربائي، وغسالة صحون مدمجة، وثلاجة، وغسالة ملابس.',
  'Inductiekookplaat, afzuigkap of filterunit, elektrische oven, ingebouwde vaatwasser, koelkast en wasmachine.',
  'Płyta indukcyjna, okap lub moduł filtrujący, piekarnik elektryczny, zabudowana zmywarka, lodówka i pralka.',
  'Induksjonstopp, kjøkkenvifte eller filterenhet, elektrisk stekeovn, integrert oppvaskmaskin, kjøleskap og vaskemaskin.',
  'Induktionshäll, köksfläkt eller filterenhet, elektrisk ugn, integrerad diskmaskin, kylskåp och tvättmaskin.')
a('.qualitySpecs.groups[2].items[0]',
  'Paredes revestidas de baldosa cerámica y suelos de gres porcelánico en ambos baños.',
  'Murs en carrelage céramique et sols en grès cérame dans les deux salles de bains.',
  'Wände mit Keramikfliesen und Böden aus Feinsteinzeug in beiden Bädern.',
  'Стены, облицованные керамической плиткой, и полы из керамогранита в обеих ванных.',
  'جدران مكسوّة بالبلاط الخزفي وأرضيات من البورسلان في الحمّامين.',
  'Wanden met keramische tegels en vloeren van keramisch porselein in beide badkamers.',
  'Ściany wyłożone płytkami ceramicznymi i podłogi z gresu porcelanowego w obu łazienkach.',
  'Vegger med keramiske fliser og gulv i porselensflis på begge bad.',
  'Väggar med keramiska plattor och golv av porslinsklinker i båda badrummen.')
a('.qualitySpecs.groups[2].items[1]',
  'Grifería termostática con columna de ducha, platos de ducha de resina con mampara, sanitarios blancos y lavabo cerámico con mueble.',
  'Robinetterie thermostatique avec colonne de douche, receveurs en résine avec paroi, sanitaires blancs et vasque en céramique sur meuble.',
  'Thermostatarmaturen mit Duschsäule, Duschwannen aus Mineralguss mit Duschwand, weiße Sanitärobjekte und Keramikwaschbecken mit Unterschrank.',
  'Термостатические смесители с душевой стойкой, поддоны из искусственного камня со стеклянной перегородкой, белая сантехника и керамическая раковина с тумбой.',
  'خلاطات بثرموستات مع عمود دش، وأحواض دش من الراتنج مع حاجز زجاجي، وأدوات صحية بيضاء، ومغسلة خزفية مع خزانة.',
  'Thermostatische kranen met douchezuil, douchebakken van kunsthars met douchewand, wit sanitair en een keramische wastafel op een meubel.',
  'Baterie termostatyczne z kolumną prysznicową, brodziki z żywicy z kabiną, biała ceramika sanitarna i umywalka ceramiczna z szafką.',
  'Termostatbatterier med dusjsøyle, dusjkar i kompositt med dusjvegg, hvitt sanitærutstyr og keramisk servant med skap.',
  'Termostatblandare med duschpelare, duschtråg i komposit med duschvägg, vitt sanitetsporslin och keramiskt tvättställ med skåp.')
a('.qualitySpecs.groups[3].name', 'Terrazas y jardines', 'Terrasses et jardins', 'Terrassen und Gärten',
  'Террасы и сады', 'التراسات والحدائق', 'Terrassen en tuinen', 'Tarasy i ogrody', 'Terrasser og hager', 'Terrasser och trädgårdar')
a('.qualitySpecs.groups[3].items[0]',
  'Pavimento de gres antideslizante, con toma de agua, desagüe, iluminación, toma de corriente y toma de televisión en todas las terrazas.',
  'Revêtement en grès antidérapant, avec point d’eau, évacuation, éclairage, prise électrique et prise TV sur chaque terrasse.',
  'Rutschfeste Feinsteinzeugbeläge, mit Wasseranschluss, Entwässerung, Beleuchtung, Steckdose und TV-Anschluss auf jeder Terrasse.',
  'Противоскользящая керамическая плитка, на каждой террасе — точка водоснабжения, водоотвод, освещение, электрическая и телевизионная розетки.',
  'أرضيات من البلاط المانع للانزلاق، مع نقطة مياه وتصريف وإنارة ومقبس كهرباء ومقبس تلفاز في كل تراس.',
  'Antislip tegelvloer, met een waterpunt, afvoer, verlichting, een stopcontact en een tv-aansluiting op elk terras.',
  'Antypoślizgowe płytki gresowe, a na każdym tarasie punkt wodny, odpływ, oświetlenie, gniazdko elektryczne i gniazdo telewizyjne.',
  'Sklisikre fliser, med vannuttak, avløp, belysning, stikkontakt og TV-uttak på hver terrasse.',
  'Halksäkra klinkers, med vattenuttag, avlopp, belysning, eluttag och tv-uttag på varje terrass.')
a('.qualitySpecs.groups[3].items[1]',
  'La memoria asigna a las viviendas de la planta superior un amplio solárium.',
  'Le descriptif attribue aux logements du dernier étage une vaste terrasse-solarium.',
  'Die Baubeschreibung sieht für die Wohnungen im obersten Geschoss ein großes Sonnendeck vor.',
  'Спецификация предусматривает для квартир верхнего этажа просторный солярий.',
  'تخصّص المواصفات للشقق في الطابق العلوي سولاريوم واسعاً.',
  'Volgens de omschrijving krijgen de woningen op de bovenste verdieping een ruim zonneterras.',
  'Specyfikacja przewiduje dla mieszkań na najwyższym piętrze obszerne solarium.',
  'Beskrivelsen gir boligene i øverste etasje en romslig solterrasse.',
  'Beskrivningen ger bostäderna på översta våningen en rymlig solterrass.')
a('.qualitySpecs.groups[4].items[0]',
  'Carpintería de aluminio con rotura de puente térmico y doble acristalamiento, y persianas enrollables de lamas de aluminio con aislamiento inyectado y motorizadas en los dormitorios.',
  'Menuiseries en aluminium à rupture de pont thermique avec double vitrage, et volets roulants motorisés à lames d’aluminium isolées dans les chambres.',
  'Aluminiumrahmen mit thermischer Trennung und Doppelverglasung sowie motorisierte, gedämmte Aluminium-Rollläden in den Schlafzimmern.',
  'Алюминиевые рамы с терморазрывом и двойным остеклением, моторизованные утеплённые алюминиевые рольставни в спальнях.',
  'نوافذ ألمنيوم بعازل حراري وزجاج مزدوج، وستائر دوّارة آلية من شرائح ألمنيوم معزولة في غرف النوم.',
  'Aluminium kozijnen met thermische onderbreking en dubbele beglazing, en gemotoriseerde geïsoleerde aluminium rolluiken in de slaapkamers.',
  'Stolarka aluminiowa z przekładką termiczną i podwójnymi szybami oraz zmotoryzowane, ocieplane rolety aluminiowe w sypialniach.',
  'Aluminiumsvinduer med kuldebrobryter og tolags glass, og motoriserte isolerte rullesjalusier i aluminium på soverommene.',
  'Aluminiumpartier med köldbrygga och tvåglasfönster, och motoriserade isolerade rullgardiner i aluminium i sovrummen.')
a('.qualitySpecs.groups[4].items[1]',
  'Puerta de entrada blindada con mirilla, puertas interiores lacadas en blanco con tiradores cromados y armarios con barra, balda y cajonera.',
  'Porte d’entrée blindée avec judas, portes intérieures laquées blanc avec poignées chromées et placards avec penderie, étagère et tiroirs.',
  'Sicherheitseingangstür mit Türspion, weiß lackierte Innentüren mit verchromten Griffen und Einbauschränke mit Kleiderstange, Fachboden und Schubladen.',
  'Бронированная входная дверь с глазком, белые лакированные межкомнатные двери с хромированными ручками и шкафы со штангой, полкой и ящиками.',
  'باب مدخل مصفّح بعين سحرية، وأبواب داخلية مطلية بالأبيض بمقابض كرومية، وخزائن بقضيب تعليق ورف وأدراج.',
  'Een veiligheidsvoordeur met spion, wit gelakte binnendeuren met verchroomde grepen en kasten met roede, legplank en lades.',
  'Drzwi wejściowe antywłamaniowe z wizjerem, białe lakierowane drzwi wewnętrzne z chromowanymi klamkami i szafy z drążkiem, półką i szufladami.',
  'Sikkerhetsdør med kikkhull, hvitlakkerte innerdører med forkrommede håndtak og garderobeskap med kleshengerstang, hylle og skuffer.',
  'Säkerhetsdörr med titthål, vitlackerade innerdörrar med förkromade handtag och garderober med klädstång, hylla och lådor.')
a('.qualitySpecs.groups[5].items[0]',
  'Aire acondicionado frío-calor por conductos con termostato, y agua caliente mediante bomba de calor aerotérmica de alta eficiencia.',
  'Climatisation gainable chaud-froid avec thermostat, et eau chaude produite par une pompe à chaleur aérothermique à haut rendement.',
  'Kanalklimaanlage für Wärme und Kühlung mit Thermostat sowie Warmwasser über eine hocheffiziente Luftwärmepumpe.',
  'Канальный кондиционер на тепло и холод с термостатом и горячая вода от высокоэффективного аэротермального теплового насоса.',
  'تكييف بمجارٍ للتدفئة والتبريد مع ثرموستات، ومياه ساخنة من مضخة حرارية هوائية عالية الكفاءة.',
  'Kanaalairconditioning voor verwarming en koeling met thermostaat, en warm water uit een zeer efficiënte luchtwarmtepomp.',
  'Klimatyzacja kanałowa z funkcją grzania i chłodzenia z termostatem oraz ciepła woda z wysokowydajnej powietrznej pompy ciepła.',
  'Kanalbasert klimaanlegg for varme og kjøling med termostat, og varmtvann fra en svært effektiv luft-til-vann-varmepumpe.',
  'Kanalbaserad luftkonditionering för värme och kyla med termostat, och varmvatten från en högeffektiv luftvärmepump.')
a('.qualitySpecs.groups[5].items[1]',
  'Sistema de ventilación, videoportero con los portales y el acceso a la urbanización, iluminación LED en baños, cocina y pasillos, y preinstalación para la recarga de vehículos eléctricos.',
  'Système de ventilation, visiophone relié aux halls et à l’entrée de la résidence, éclairage LED dans les salles de bains, la cuisine et les couloirs, et pré-installation pour la recharge de véhicules électriques.',
  'Lüftungsanlage, Video-Gegensprechanlage zu den Hauseingängen und zum Tor der Anlage, LED-Beleuchtung in Bädern, Küche und Fluren sowie Vorinstallation für das Laden von Elektrofahrzeugen.',
  'Система вентиляции, видеодомофон со связью с подъездами и въездом в комплекс, светодиодное освещение в ванных, на кухне и в коридорах, а также подготовка под зарядку электромобилей.',
  'نظام تهوية، وجهاز اتصال مرئي بالمداخل وبوابة المجمع، وإنارة LED في الحمّامات والمطبخ والممرات، وتمديدات مسبقة لشحن السيارات الكهربائية.',
  'Een ventilatiesysteem, een video-intercom naar de portieken en de poort van het complex, ledverlichting in badkamers, keuken en gangen, en voorbereiding voor het laden van elektrische auto’s.',
  'System wentylacji, wideodomofon połączony z klatkami i bramą osiedla, oświetlenie LED w łazienkach, kuchni i korytarzach oraz instalacja przygotowawcza do ładowania samochodów elektrycznych.',
  'Ventilasjonsanlegg, porttelefon med video til oppgangene og porten inn til anlegget, LED-belysning på bad, kjøkken og i ganger, og forberedt for lading av elbil.',
  'Ventilationssystem, porttelefon med video till uppgångarna och områdets grind, LED-belysning i badrum, kök och korridorer, och förberett för laddning av elbil.')
a('.qualitySpecs.groups[6].name', 'El edificio y la comunidad', 'L’immeuble et la copropriété', 'Gebäude und Gemeinschaft',
  'Здание и общая территория', 'المبنى والمجمع', 'Het gebouw en de gemeenschap', 'Budynek i części wspólne',
  'Bygget og fellesarealene', 'Huset och de gemensamma ytorna')
a('.qualitySpecs.groups[6].items[0]',
  'Urbanización cerrada, con suelos porcelánicos e iluminación con detectores de presencia en las zonas comunes interiores, y ascensores de puertas automáticas.',
  'Résidence fermée, avec sols en grès cérame et éclairage à détecteurs de présence dans les parties communes intérieures, et ascenseurs à portes automatiques.',
  'Eine geschlossene Anlage mit Feinsteinzeugböden und Bewegungsmeldern für die Beleuchtung in den inneren Gemeinschaftsbereichen sowie Aufzügen mit automatischen Türen.',
  'Закрытый комплекс: полы из керамогранита и освещение с датчиками движения во внутренних общих зонах, лифты с автоматическими дверями.',
  'مجمع مغلق بأرضيات من البورسلان وإنارة بحساسات حركة في المناطق المشتركة الداخلية، ومصاعد بأبواب آلية.',
  'Een omheind complex, met porseleinen vloeren en verlichting met bewegingsmelders in de gemeenschappelijke binnenruimten, en liften met automatische deuren.',
  'Osiedle zamknięte, z podłogami z gresu i oświetleniem z czujnikami ruchu w wewnętrznych częściach wspólnych oraz windami z automatycznymi drzwiami.',
  'Et inngjerdet anlegg, med porselensflis og belysning med bevegelsessensorer i fellesarealene innendørs, og heiser med automatiske dører.',
  'Ett inhägnat område, med klinkergolv och belysning med rörelsesensorer i de gemensamma utrymmena inomhus, och hissar med automatiska dörrar.')
a('.qualitySpecs.groups[6].items[1]',
  'Garaje subterráneo con puertas automáticas accionadas por mando a distancia, y trasteros pintados con puerta metálica.',
  'Parking souterrain à portes automatiques commandées à distance, et caves peintes avec porte métallique.',
  'Tiefgarage mit automatischen Toren per Fernbedienung und gestrichenen Abstellräumen mit Metalltür.',
  'Подземный паркинг с автоматическими воротами на пульте и окрашенные кладовые с металлической дверью.',
  'مرآب تحت الأرض بأبواب آلية تعمل بجهاز تحكم عن بُعد، ومخازن مطلية بأبواب معدنية.',
  'Een ondergrondse garage met automatische deuren met afstandsbediening, en geschilderde bergingen met een metalen deur.',
  'Garaż podziemny z automatycznymi bramami na pilota i malowane komórki lokatorskie z metalowymi drzwiami.',
  'Parkeringskjeller med automatiske porter med fjernkontroll, og malte boder med ståldør.',
  'Garage under mark med automatiska portar med fjärrkontroll, och målade förråd med ståldörr.')

# ---- availability -------------------------------------------------------------------------------
a('.availability.headlineHtml', '26 viviendas <em>disponibles</em>', '26 logements <em>disponibles</em>',
  '26 Wohnungen <em>verfügbar</em>', '26 квартир <em>в продаже</em>', '26 شقة <em>متاحة</em>',
  '26 woningen <em>beschikbaar</em>', '26 mieszkań <em>dostępnych</em>', '26 boliger <em>ledige</em>',
  '26 bostäder <em>lediga</em>')
a('.availability.checkedDate', '13 de noviembre de 2026', '13 novembre 2026', '13. November 2026', '13 ноября 2026 года',
  '13 نوفمبر 2026', '13 november 2026', '13 listopada 2026', '13. november 2026', '13 november 2026')
a('.availability.copy',
  'Disponibilidad y precios según el portal para agentes del promotor a 13 de noviembre de 2026, que reconfirmamos antes de cualquier reserva. Cada vivienda figura con al menos una plaza de garaje y un trastero, con precio en líneas aparte.',
  'Disponibilités et prix tels qu’indiqués sur le portail agents du promoteur au 13 novembre 2026, reconfirmés avant toute réservation. Chaque logement est listé avec au moins une place de parking et une cave, chiffrées sur des lignes séparées.',
  'Verfügbarkeit und Preise laut Maklerportal des Bauträgers vom 13. November 2026, vor jeder Reservierung erneut bestätigt. Jede Wohnung ist mit mindestens einem Stellplatz und einem Abstellraum gelistet, die als eigene Positionen bepreist sind.',
  'Наличие и цены по агентскому порталу застройщика на 13 ноября 2026 года; перед бронированием мы их перепроверяем. Каждая квартира значится как минимум с одним машиноместом и одной кладовой, цены на которые указаны отдельными строками.',
  'التوفر والأسعار كما وردت في بوابة الوكلاء لدى المطوّر في 13 نوفمبر 2026، ويُعاد تأكيدها قبل أي حجز. وتُدرج كل شقة مع موقف سيارة واحد ومخزن واحد على الأقل، بسعر مستقل لكل منهما.',
  'Beschikbaarheid en prijzen zoals vermeld in het makelaarsportaal van de ontwikkelaar op 13 november 2026, opnieuw bevestigd vóór reservering. Elke woning staat vermeld met ten minste één parkeerplaats en één berging, apart geprijsd.',
  'Dostępność i ceny według portalu dla agentów dewelopera z 13 listopada 2026, potwierdzane ponownie przed rezerwacją. Każde mieszkanie figuruje z co najmniej jednym miejscem parkingowym i jedną komórką lokatorską, wycenionymi w osobnych pozycjach.',
  'Tilgjengelighet og priser slik de står i utbyggerens meglerportal 13. november 2026, bekreftet på nytt før reservasjon. Hver bolig er oppført med minst én parkeringsplass og én bod, priset på egne linjer.',
  'Tillgänglighet och priser enligt exploatörens mäklarportal den 13 november 2026, bekräftade på nytt före reservation. Varje bostad listas med minst en parkeringsplats och ett förråd, prissatta på egna rader.')
a('.availability.sourceNote',
  'Precios, plantas, dormitorios y superficies transcritos del portal para agentes del promotor a 13 de noviembre de 2026, que recoge 26 viviendas disponibles en dos fases e indica que sus precios son meramente informativos, sin valor legal y sujetos a disponibilidad. Los precios mostrados son los de la vivienda sola, sin {T}. El portal asigna a cada vivienda una o dos plazas de garaje de {E15000} cada una y uno o dos trasteros de {E6000} cada uno, con un subtotal que va de {E359000} a {E722000}. La terraza es la cifra del portal; los jardines proceden de los planos, ya que el portal no los da. Tenemos planos de 14 de las 26 viviendas, cada uno la ficha provisional del promotor para esa vivienda; en tres de ellos la superficie construida es {N0.01} {U} menor que en el portal (20-2-0-B, 20-2-2-B y 21-1-0-A), y la tabla recoge la del portal. Las otras 12 viviendas no tienen plano en la documentación que tenemos. Los precios no incluyen {T} ni gastos de compra. Nueva Living reconfirma precio, estado y condiciones antes de cualquier reserva.',
  'Prix, étages, chambres et surfaces transcrits du portail agents du promoteur au 13 novembre 2026, qui liste 26 logements disponibles sur deux phases et précise que ses prix sont donnés à titre indicatif, sans valeur légale et sous réserve de disponibilité. Les prix indiqués sont ceux du logement seul, hors {T}. Le portail associe à chaque logement une ou deux places de parking à {E15000} chacune et une ou deux caves à {E6000} chacune, avec un sous-total de {E359000} à {E722000}. La terrasse est le chiffre du portail ; les jardins viennent des plans, le portail n’en donnant pas. Nous avons les plans de 14 des 26 logements, chacun la fiche provisoire du promoteur pour ce logement ; sur trois d’entre eux, la surface construite est inférieure de {N0.01} {U} à celle du portail (20-2-0-B, 20-2-2-B et 21-1-0-A), et le tableau reprend celle du portail. Les 12 autres logements n’ont pas de plan dans les documents dont nous disposons. Les prix s’entendent hors {T} et hors frais d’acquisition. Nueva Living reconfirme le prix, le statut et les conditions avant toute réservation.',
  'Preise, Etagen, Schlafzimmer und Flächen sind aus dem Maklerportal des Bauträgers vom 13. November 2026 übernommen, das 26 verfügbare Wohnungen in zwei Bauabschnitten führt und angibt, dass seine Preise nur zur Information dienen, keine rechtliche Gültigkeit haben und unter Verfügbarkeitsvorbehalt stehen. Die angegebenen Preise gelten für die Wohnung allein, ohne {T} Das Portal ordnet jeder Wohnung einen oder zwei Stellplätze zu je {E15000} und einen oder zwei Abstellräume zu je {E6000} zu, mit einer Zwischensumme von {E359000} bis {E722000}. Die Terrasse ist der Wert des Portals; die Gärten stammen aus den Grundrissen, da das Portal keine nennt. Uns liegen Grundrisse für 14 der 26 Wohnungen vor, jeweils das vorläufige Blatt des Bauträgers für diese Wohnung; bei dreien ist die bebaute Fläche {N0.01} {U} kleiner als im Portal (20-2-0-B, 20-2-2-B und 21-1-0-A), und die Tabelle nennt den Wert des Portals. Für die übrigen 12 Wohnungen enthalten unsere Unterlagen keinen Grundriss. Preise ohne {T} und Kaufnebenkosten. Nueva Living bestätigt Preis, Status und Konditionen vor jeder Reservierung erneut.',
  'Цены, этажи, спальни и площади перенесены с агентского портала застройщика на 13 ноября 2026 года, где указаны 26 свободных квартир в двух очередях и сказано, что цены носят справочный характер, не имеют юридической силы и зависят от наличия. Указанные цены — за квартиру без машиноместа и кладовой, без {T}. Портал закрепляет за каждой квартирой одно или два машиноместа по {E15000} и одну или две кладовые по {E6000}, с промежуточным итогом от {E359000} до {E722000}. Площадь террасы — по порталу; площади садов взяты из планировок, на портале их нет. У нас есть планировки 14 из 26 квартир — предварительные листы застройщика для каждой из них; в трёх из них площадь застройки на {N0.01} {U} меньше, чем на портале (20-2-0-B, 20-2-2-B и 21-1-0-A), и в таблице приведена цифра портала. Для остальных 12 квартир планировок в имеющихся у нас документах нет. Цены указаны без {T} и расходов на покупку. Nueva Living перепроверяет цену, статус и условия перед любым бронированием.',
  'الأسعار والطوابق وغرف النوم والمساحات منقولة من بوابة الوكلاء لدى المطوّر في 13 نوفمبر 2026، التي تُدرج 26 شقة متاحة في مرحلتين وتذكر أن أسعارها للعلم فقط وليست لها قيمة قانونية وتخضع للتوفر. والأسعار المعروضة للشقة وحدها دون {T}. وتخصّص البوابة لكل شقة موقفاً أو موقفين بسعر {E15000} للموقف، ومخزناً أو مخزنين بسعر {E6000} للمخزن، مع مجموع فرعي من {E359000} إلى {E722000}. ومساحة التراس هي رقم البوابة، أما الحدائق فمن المخططات إذ لا تذكرها البوابة. ولدينا مخططات 14 من الشقق الست والعشرين، وكل منها ورقة المطوّر المؤقتة لتلك الشقة؛ وفي ثلاث منها تقل المساحة المبنية بمقدار {N0.01} {U} عن البوابة (20-2-0-B و20-2-2-B و21-1-0-A)، ويذكر الجدول رقم البوابة. أما الشقق الاثنتا عشرة الأخرى فلا مخطط لها في الوثائق المتوفرة لدينا. الأسعار لا تشمل {T} ولا تكاليف الشراء. وتعيد نويفا ليفينغ تأكيد السعر والحالة والشروط قبل أي حجز.',
  'Prijzen, verdiepingen, slaapkamers en oppervlakten zijn overgenomen uit het makelaarsportaal van de ontwikkelaar op 13 november 2026, dat 26 beschikbare woningen in twee fasen vermeldt en aangeeft dat de prijzen alleen ter informatie zijn, geen juridische waarde hebben en onder voorbehoud van beschikbaarheid gelden. De getoonde prijzen gelden voor de woning alleen, exclusief {T}. Het portaal koppelt aan elke woning één of twee parkeerplaatsen van {E15000} per stuk en één of twee bergingen van {E6000} per stuk, met een subtotaal van {E359000} tot {E722000}. Het terras is het cijfer van het portaal; de tuinen komen van de plattegronden, omdat het portaal ze niet geeft. Wij hebben plattegronden van 14 van de 26 woningen, telkens het voorlopige blad van de ontwikkelaar voor die woning; op drie daarvan is de bebouwde oppervlakte {N0.01} {U} kleiner dan in het portaal (20-2-0-B, 20-2-2-B en 21-1-0-A), en de tabel volgt het portaal. Voor de andere 12 woningen bevatten onze documenten geen plattegrond. Prijzen exclusief {T} en aankoopkosten. Nueva Living bevestigt prijs, status en voorwaarden opnieuw vóór elke reservering.',
  'Ceny, piętra, sypialnie i powierzchnie przepisano z portalu dla agentów dewelopera z 13 listopada 2026, który wymienia 26 dostępnych mieszkań w dwóch etapach i podaje, że ceny mają charakter wyłącznie informacyjny, nie mają mocy prawnej i zależą od dostępności. Podane ceny dotyczą samego mieszkania, bez {T}. Portal przypisuje każdemu mieszkaniu jedno lub dwa miejsca parkingowe po {E15000} i jedną lub dwie komórki lokatorskie po {E6000}, z sumą częściową od {E359000} do {E722000}. Taras to wartość z portalu; ogrody pochodzą z rzutów, bo portal ich nie podaje. Mamy rzuty 14 z 26 mieszkań, każdy to tymczasowa karta dewelopera dla danego mieszkania; w trzech z nich powierzchnia zabudowy jest o {N0.01} {U} mniejsza niż w portalu (20-2-0-B, 20-2-2-B i 21-1-0-A), a tabela podaje wartość z portalu. Dla pozostałych 12 mieszkań posiadane przez nas dokumenty nie zawierają rzutów. Ceny bez {T} i kosztów zakupu. Nueva Living ponownie potwierdza cenę, status i warunki przed każdą rezerwacją.',
  'Priser, etasjer, soverom og arealer er hentet fra utbyggerens meglerportal 13. november 2026, som viser 26 ledige boliger i to byggetrinn og sier at prisene kun er veiledende, ikke har juridisk gyldighet og gjelder så langt boligene er ledige. Prisene som vises, gjelder boligen alene, uten {T}. Portalen knytter én eller to parkeringsplasser à {E15000} og én eller to boder à {E6000} til hver bolig, med en delsum fra {E359000} til {E722000}. Terrassen er portalens tall; hagene kommer fra plantegningene, siden portalen ikke oppgir dem. Vi har plantegninger for 14 av de 26 boligene, hver av dem utbyggerens foreløpige ark for boligen; på tre av dem er det bebygde arealet {N0.01} {U} mindre enn i portalen (20-2-0-B, 20-2-2-B og 21-1-0-A), og tabellen følger portalen. De øvrige 12 boligene har ingen plantegning i dokumentene vi har. Prisene er uten {T} og kjøpskostnader. Nueva Living bekrefter pris, status og vilkår på nytt før enhver reservasjon.',
  'Priser, våningar, sovrum och ytor är hämtade ur exploatörens mäklarportal den 13 november 2026, som listar 26 lediga bostäder i två etapper och anger att priserna endast är vägledande, saknar rättslig verkan och gäller i mån av tillgång. De visade priserna gäller bostaden ensam, utan {T}. Portalen kopplar en eller två parkeringsplatser à {E15000} och ett eller två förråd à {E6000} till varje bostad, med en delsumma från {E359000} till {E722000}. Terrassen är portalens siffra; trädgårdarna kommer från planritningarna, eftersom portalen inte anger dem. Vi har planritningar för 14 av de 26 bostäderna, var och en exploatörens preliminära blad för bostaden; på tre av dem är byggytan {N0.01} {U} mindre än i portalen (20-2-0-B, 20-2-2-B och 21-1-0-A), och tabellen följer portalen. De övriga 12 bostäderna saknar planritning i de dokument vi har. Priserna är utan {T} och köpkostnader. Nueva Living bekräftar pris, status och villkor på nytt före varje reservation.')

# ---- construction timeline ------------------------------------------------------------------------
a('.constructionTimeline.points[0].label', 'Veintiséis viviendas', 'Vingt-six logements', 'Sechsundzwanzig Wohnungen',
  'Двадцать шесть квартир', 'ست وعشرون شقة', 'Zesentwintig woningen', 'Dwadzieścia sześć mieszkań', 'Tjueseks boliger',
  'Tjugosex bostäder')
a('.constructionTimeline.note',
  'El portal del promotor indica que la construcción ha comenzado en la primera de las dos fases y no da la situación de la segunda. Ningún documento indica licencia de obra, fecha de entrega ni calendario de pagos. Nueva Living pide los tres por escrito antes de que se mueva dinero, y no le daremos una fecha que no podamos mostrarle.',
  'Le portail du promoteur indique que la construction a commencé sur la première des deux phases et ne donne pas l’état de la seconde. Aucun document n’indique de permis de construire, de date de livraison ni d’échéancier de paiement. Nueva Living demande les trois par écrit avant tout versement, et ne vous annoncera pas une date qu’elle ne peut pas vous montrer.',
  'Das Portal des Bauträgers meldet für den ersten der beiden Bauabschnitte Baubeginn und nennt für den zweiten keinen Stand. Kein Dokument nennt eine Baugenehmigung, einen Übergabetermin oder einen Zahlungsplan. Nueva Living verlangt alle drei schriftlich, bevor Geld fließt, und nennt Ihnen kein Datum, das wir nicht belegen können.',
  'Портал застройщика сообщает, что строительство первой из двух очередей началось, а о второй сведений не даёт. Ни один документ не указывает разрешение на строительство, дату сдачи или график платежей. Nueva Living запрашивает всё это письменно до любых платежей и не назовёт вам дату, которую не может подтвердить.',
  'تذكر بوابة المطوّر أن البناء قد بدأ في المرحلة الأولى من المرحلتين، ولا تذكر وضع الثانية. ولا تذكر أي وثيقة رخصة بناء أو موعد تسليم أو جدول دفعات. وتطلب نويفا ليفينغ الثلاثة كتابياً قبل دفع أي مبلغ، ولن نذكر لكم موعداً لا نستطيع إثباته.',
  'Het portaal van de ontwikkelaar meldt dat de bouw van de eerste van de twee fasen is begonnen en geeft geen stand voor de tweede. Geen enkel document noemt een bouwvergunning, een opleverdatum of een betalingsschema. Nueva Living vraagt alle drie schriftelijk op voordat er geld wordt betaald, en noemt u geen datum die wij niet kunnen aantonen.',
  'Portal dewelopera podaje, że budowa pierwszego z dwóch etapów się rozpoczęła, a o drugim nie podaje informacji. Żaden dokument nie wskazuje pozwolenia na budowę, terminu oddania ani harmonogramu płatności. Nueva Living prosi o wszystkie trzy na piśmie, zanim zostaną wpłacone jakiekolwiek pieniądze, i nie poda Państwu daty, której nie może udokumentować.',
  'Utbyggerens portal sier at byggingen av det første av de to byggetrinnene har startet, og oppgir ingen status for det andre. Ingen dokumenter oppgir byggetillatelse, overleveringsdato eller betalingsplan. Nueva Living ber om alle tre skriftlig før penger overføres, og oppgir ingen dato vi ikke kan dokumentere.',
  'Exploatörens portal anger att bygget av den första av de två etapperna har startat och anger ingen status för den andra. Inget dokument anger bygglov, tillträdesdatum eller betalningsplan. Nueva Living begär alla tre skriftligen innan några pengar betalas, och anger inget datum vi inte kan visa er.')

# ---- why, investment, trust -----------------------------------------------------------------------
a('.why.points[0][1]',
  'Veintiséis apartamentos disponibles en dos fases posteriores de un conjunto cerrado más amplio en Estepona.',
  'Vingt-six appartements disponibles dans deux phases ultérieures d’une résidence fermée plus vaste à Estepona.',
  'Sechsundzwanzig verfügbare Wohnungen in zwei späteren Bauabschnitten einer größeren geschlossenen Anlage in Estepona.',
  'Двадцать шесть свободных квартир в двух более поздних очередях большого закрытого комплекса в Эстепоне.',
  'ست وعشرون شقة متاحة في مرحلتين لاحقتين من مجمع مغلق أكبر في إستيبونا.',
  'Zesentwintig beschikbare appartementen in twee latere fasen van een groter omheind complex in Estepona.',
  'Dwadzieścia sześć dostępnych apartamentów w dwóch późniejszych etapach większego zamkniętego osiedla w Esteponie.',
  'Tjueseks ledige leiligheter i to senere byggetrinn i et større inngjerdet anlegg i Estepona.',
  'Tjugosex lediga lägenheter i två senare etapper av ett större inhägnat område i Estepona.')
a('.why.points[1][1]',
  'Compradores que buscan un apartamento nuevo con terraza y con piscinas, spa y gimnasio compartidos, para vivir o como segunda residencia.',
  'Les acquéreurs qui cherchent un appartement neuf avec terrasse, piscines, spa et salle de sport partagés, pour y vivre ou en résidence secondaire.',
  'Käufer, die eine neue Wohnung mit Terrasse und gemeinsamen Pools, Spa und Fitnessraum suchen, zum Wohnen oder als Zweitwohnsitz.',
  'Покупателям, которым нужна новая квартира с террасой и общими бассейнами, спа и тренажёрным залом — для жизни или как второе жильё.',
  'للمشترين الباحثين عن شقة جديدة مع تراس ومسابح وسبا وصالة رياضية مشتركة، للسكن أو كمنزل ثانٍ.',
  'Kopers die een nieuw appartement met terras en gedeelde zwembaden, spa en fitness zoeken, om er te wonen of als tweede woning.',
  'Dla kupujących, którzy szukają nowego mieszkania z tarasem oraz wspólnymi basenami, spa i siłownią — do zamieszkania lub jako drugi dom.',
  'Kjøpere som ønsker en ny leilighet med terrasse og felles bassenger, spa og treningsrom, som helårsbolig eller fritidsbolig.',
  'Köpare som vill ha en ny lägenhet med terrass och gemensamma pooler, spa och gym, som permanentbostad eller fritidsbostad.')
a('.why.points[2][1]',
  'Las zonas comunes son las de un gran conjunto, con spa, gimnasio, sala de coworking, sala de cine y Youth Club, y algunas viviendas en planta baja tienen jardín propio.',
  'Les espaces communs sont ceux d’une grande résidence, avec spa, salle de sport, coworking, salle de cinéma et club pour les jeunes, et certains rez-de-chaussée ont leur propre jardin.',
  'Die Gemeinschaftsbereiche sind die einer großen Anlage, mit Spa, Fitnessraum, Coworking-Raum, Kinoraum und Jugendclub, und einige Erdgeschosswohnungen haben einen eigenen Garten.',
  'Общие зоны — как у большого комплекса: спа, тренажёрный зал, коворкинг, кинозал и молодёжный клуб, а у некоторых квартир на первом этаже есть собственный сад.',
  'المرافق المشتركة هي مرافق مجمع كبير، مع سبا وصالة رياضية ومساحة عمل مشتركة وقاعة سينما ونادٍ للشباب، ولبعض شقق الطابق الأرضي حديقة خاصة.',
  'De gemeenschappelijke voorzieningen zijn die van een groot complex, met spa, fitness, coworking, bioscoopzaal en jongerenclub, en enkele benedenwoningen hebben een eigen tuin.',
  'Części wspólne to części dużego osiedla: spa, siłownia, coworking, sala kinowa i klub młodzieżowy, a część mieszkań na parterze ma własny ogród.',
  'Fellesarealene er et stort anleggs, med spa, treningsrom, kontorfellesskap, kinorom og ungdomsklubb, og noen leiligheter i første etasje har egen hage.',
  'De gemensamma ytorna är ett stort områdes, med spa, gym, coworkingrum, biosalong och ungdomsklubb, och några bottenvåningar har egen trädgård.')
a('.why.points[3][1]',
  'El conjunto está junto a Selwo Aventura, en Estepona, con La Resina Golf cerca y la costa a sus pies.',
  'La résidence se trouve à côté de Selwo Aventura, à Estepona, avec La Resina Golf à proximité et la côte en contrebas.',
  'Die Anlage liegt neben Selwo Aventura in Estepona, mit La Resina Golf in der Nähe und der Küste unterhalb.',
  'Комплекс находится рядом с Selwo Aventura в Эстепоне, поблизости гольф-клуб La Resina, ниже — побережье.',
  'يقع المجمع بجوار سيلوو أفينتورا في إستيبونا، وبالقرب منه لا ريسينا غولف، والساحل في الأسفل.',
  'Het complex ligt naast Selwo Aventura in Estepona, met La Resina Golf in de buurt en de kust beneden.',
  'Osiedle leży obok Selwo Aventura w Esteponie, w pobliżu pola La Resina Golf, z wybrzeżem poniżej.',
  'Anlegget ligger ved Selwo Aventura i Estepona, med La Resina Golf i nærheten og kysten nedenfor.',
  'Området ligger intill Selwo Aventura i Estepona, med La Resina Golf i närheten och kusten nedanför.')
a('.investment.cards[0][1]',
  'El portal recoge veintiséis viviendas: una de un dormitorio por {E338000}, doce de dos dormitorios de {E411000} a {E483000} y trece de tres dormitorios de {E489000} a {E686000}, más {T}.',
  'Le portail liste vingt-six logements : un d’une chambre à {E338000}, douze de deux chambres de {E411000} à {E483000} et treize de trois chambres de {E489000} à {E686000}, plus {T}.',
  'Das Portal führt sechsundzwanzig Wohnungen: eine mit einem Schlafzimmer für {E338000}, zwölf mit zwei Schlafzimmern von {E411000} bis {E483000} und dreizehn mit drei Schlafzimmern von {E489000} bis {E686000}, zuzüglich {T}',
  'На портале двадцать шесть квартир: одна с одной спальней за {E338000}, двенадцать с двумя спальнями от {E411000} до {E483000} и тринадцать с тремя спальнями от {E489000} до {E686000}, плюс {T}.',
  'تُدرج البوابة ست وعشرين شقة: واحدة بغرفة نوم بسعر {E338000}، واثنتا عشرة بغرفتين من {E411000} إلى {E483000}، وثلاث عشرة بثلاث غرف من {E489000} إلى {E686000}، مع إضافة {T}.',
  'Het portaal vermeldt zesentwintig woningen: één met één slaapkamer voor {E338000}, twaalf met twee slaapkamers van {E411000} tot {E483000} en dertien met drie slaapkamers van {E489000} tot {E686000}, plus {T}.',
  'Portal wymienia dwadzieścia sześć mieszkań: jedno z jedną sypialnią za {E338000}, dwanaście z dwiema sypialniami od {E411000} do {E483000} i trzynaście z trzema sypialniami od {E489000} do {E686000}, plus {T}.',
  'Portalen viser tjueseks boliger: én med ett soverom til {E338000}, tolv med to soverom fra {E411000} til {E483000} og tretten med tre soverom fra {E489000} til {E686000}, pluss {T}.',
  'Portalen listar tjugosex bostäder: en med ett sovrum för {E338000}, tolv med två sovrum från {E411000} till {E483000} och tretton med tre sovrum från {E489000} till {E686000}, plus {T}.')
a('.investment.cards[1][0]', 'Garaje y trastero', 'Parking et cave', 'Stellplatz und Abstellraum', 'Машиноместо и кладовая',
  'الموقف والمخزن', 'Parkeren en berging', 'Parking i komórka lokatorska', 'Parkering og bod', 'Parkering och förråd')
a('.investment.cards[1][1]',
  'El portal asigna a cada vivienda una o dos plazas de garaje de {E15000} cada una y uno o dos trasteros de {E6000} cada uno, de modo que el total con ellos va de {E359000} a {E722000} antes de {T}.',
  'Le portail associe à chaque logement une ou deux places de parking à {E15000} chacune et une ou deux caves à {E6000} chacune, si bien que le total va de {E359000} à {E722000} hors {T}.',
  'Das Portal ordnet jeder Wohnung einen oder zwei Stellplätze zu je {E15000} und einen oder zwei Abstellräume zu je {E6000} zu, sodass die Summe von {E359000} bis {E722000} vor {T} reicht.',
  'Портал закрепляет за каждой квартирой одно или два машиноместа по {E15000} и одну или две кладовые по {E6000}, так что общая сумма составляет от {E359000} до {E722000} без {T}.',
  'تخصّص البوابة لكل شقة موقفاً أو موقفين بسعر {E15000} للموقف، ومخزناً أو مخزنين بسعر {E6000} للمخزن، فيتراوح المجموع بين {E359000} و{E722000} قبل {T}.',
  'Het portaal koppelt aan elke woning één of twee parkeerplaatsen van {E15000} per stuk en één of twee bergingen van {E6000} per stuk, zodat het totaal van {E359000} tot {E722000} loopt, exclusief {T}.',
  'Portal przypisuje każdemu mieszkaniu jedno lub dwa miejsca parkingowe po {E15000} i jedną lub dwie komórki po {E6000}, więc łączna kwota wynosi od {E359000} do {E722000} bez {T}.',
  'Portalen knytter én eller to parkeringsplasser à {E15000} og én eller to boder à {E6000} til hver bolig, slik at totalen blir fra {E359000} til {E722000} før {T}.',
  'Portalen kopplar en eller två parkeringsplatser à {E15000} och ett eller två förråd à {E6000} till varje bostad, så att summan blir från {E359000} till {E722000} före {T}.')
a('.investment.cards[2][0]', 'Aún sin fecha', 'Pas encore de date', 'Noch kein Termin', 'Даты пока нет', 'لا موعد بعد',
  'Nog geen datum', 'Brak terminu', 'Ingen dato ennå', 'Inget datum ännu')
a('.investment.cards[2][1]',
  'Ningún documento indica fecha de entrega ni calendario de pagos. Pedimos ambos por escrito y hacemos constar la fecha en el contrato.',
  'Aucun document n’indique de date de livraison ni d’échéancier de paiement. Nous demandons les deux par écrit et faisons inscrire la date au contrat.',
  'Kein Dokument nennt einen Übergabetermin oder einen Zahlungsplan. Wir verlangen beides schriftlich und lassen den Termin in den Vertrag aufnehmen.',
  'Ни один документ не указывает дату сдачи или график платежей. Мы запрашиваем и то и другое письменно и вносим дату в договор.',
  'لا تذكر أي وثيقة موعد تسليم أو جدول دفعات. ونطلب الاثنين كتابياً وندرج الموعد في العقد.',
  'Geen enkel document noemt een opleverdatum of een betalingsschema. Wij vragen beide schriftelijk op en laten de datum in het contract opnemen.',
  'Żaden dokument nie podaje terminu oddania ani harmonogramu płatności. Prosimy o oba na piśmie i wpisujemy termin do umowy.',
  'Ingen dokumenter oppgir overleveringsdato eller betalingsplan. Vi ber om begge skriftlig og får datoen inn i kontrakten.',
  'Inget dokument anger tillträdesdatum eller betalningsplan. Vi begär båda skriftligen och för in datumet i kontraktet.')
a('.investment.cards[3][1]',
  'Adecuado como vivienda habitual o segunda residencia; el alquiler depende de las normas de la comunidad y de la licencia local, que comprobamos.',
  'Convient comme résidence principale ou secondaire ; la location dépend du règlement de copropriété et de la licence locale, que nous vérifions.',
  'Geeignet als Erst- oder Zweitwohnsitz; die Vermietung hängt von der Gemeinschaftsordnung und der örtlichen Lizenz ab, die wir prüfen.',
  'Подходит для постоянного проживания или как второе жильё; сдача в аренду зависит от правил сообщества и местной лицензии, которые мы проверяем.',
  'مناسب كسكن دائم أو منزل ثانٍ، ويتوقف التأجير على أنظمة المجمع والترخيص المحلي، وكلاهما نتحقق منه.',
  'Geschikt als eerste of tweede woning; verhuur hangt af van het reglement van de gemeenschap en de lokale vergunning, die wij beide controleren.',
  'Nadaje się na stałe miejsce zamieszkania lub drugi dom; wynajem zależy od regulaminu wspólnoty i lokalnej licencji, które sprawdzamy.',
  'Passer som helårsbolig eller fritidsbolig; utleie avhenger av sameiets regler og den lokale lisensen, som vi sjekker.',
  'Passar som permanentbostad eller fritidsbostad; uthyrning beror på samfällighetens regler och den lokala licensen, som vi kontrollerar.')
a('.trustDossier.cards[0][0]', 'La licencia y la obra', 'Le permis et les travaux', 'Genehmigung und Bauarbeiten',
  'Разрешение и стройка', 'الرخصة والأعمال', 'De vergunning en de bouw', 'Pozwolenie i budowa',
  'Tillatelsen og byggearbeidet', 'Bygglovet och bygget')
a('.trustDossier.cards[0][1]',
  'La licencia de obra, el estado de la obra en cada fase y la fecha de entrega, por escrito antes de que se mueva dinero.',
  'Le permis de construire, l’avancement des travaux de chaque phase et la date de livraison, par écrit avant tout versement.',
  'Die Baugenehmigung, der Baufortschritt in jedem Bauabschnitt und der Übergabetermin, schriftlich, bevor Geld fließt.',
  'Разрешение на строительство, ход работ по каждой очереди и дату сдачи — письменно до любых платежей.',
  'رخصة البناء، ومرحلة الأعمال في كل مرحلة، وموعد التسليم، كتابياً قبل دفع أي مبلغ.',
  'De bouwvergunning, de stand van de bouw per fase en de opleverdatum, schriftelijk voordat er geld wordt betaald.',
  'Pozwolenie na budowę, stan prac na każdym etapie i termin oddania — na piśmie, zanim zostaną wpłacone pieniądze.',
  'Byggetillatelsen, fremdriften i hvert byggetrinn og overleveringsdatoen, skriftlig før penger overføres.',
  'Bygglovet, hur långt bygget kommit i varje etapp och tillträdesdatumet, skriftligen innan några pengar betalas.')
a('.trustDossier.cards[1][1]',
  'Tenemos los planos provisionales del promotor de 14 de las 26 viviendas y pedimos el resto. En tres de ellos la superficie construida difiere del portal en {N0.01} {U}.',
  'Nous avons les plans provisoires du promoteur pour 14 des 26 logements et demandons les autres. Sur trois d’entre eux, la surface construite diffère de {N0.01} {U} de celle du portail.',
  'Uns liegen die vorläufigen Grundrisse des Bauträgers für 14 der 26 Wohnungen vor; die übrigen fordern wir an. Bei dreien weicht die bebaute Fläche um {N0.01} {U} vom Portal ab.',
  'У нас есть предварительные планировки застройщика для 14 из 26 квартир, остальные мы запрашиваем. В трёх из них площадь застройки отличается от портала на {N0.01} {U}.',
  'لدينا مخططات المطوّر المؤقتة لـ14 من الشقق الست والعشرين، ونطلب البقية. وفي ثلاث منها تختلف المساحة المبنية عن البوابة بمقدار {N0.01} {U}.',
  'Wij hebben de voorlopige plattegronden van de ontwikkelaar voor 14 van de 26 woningen en vragen de rest op. Op drie ervan wijkt de bebouwde oppervlakte {N0.01} {U} af van het portaal.',
  'Mamy tymczasowe rzuty dewelopera dla 14 z 26 mieszkań i prosimy o pozostałe. W trzech z nich powierzchnia zabudowy różni się od portalu o {N0.01} {U}.',
  'Vi har utbyggerens foreløpige plantegninger for 14 av de 26 boligene og ber om resten. På tre av dem avviker det bebygde arealet med {N0.01} {U} fra portalen.',
  'Vi har exploatörens preliminära planritningar för 14 av de 26 bostäderna och begär resten. På tre av dem skiljer sig byggytan med {N0.01} {U} från portalen.')
a('.trustDossier.cards[2][0]', 'Garaje y trastero', 'Parking et cave', 'Stellplatz und Abstellraum', 'Машиноместо и кладовая',
  'الموقف والمخزن', 'Parkeren en berging', 'Parking i komórka lokatorska', 'Parkering og bod', 'Parkering och förråd')
a('.trustDossier.cards[2][1]',
  'Qué plaza de garaje y qué trastero corresponden a la vivienda, y que están inscritos tal como se describen.',
  'Quelle place de parking et quelle cave vont avec le logement, et qu’elles sont enregistrées comme décrit.',
  'Welcher Stellplatz und welcher Abstellraum zur Wohnung gehören und dass sie wie beschrieben eingetragen sind.',
  'Какое машиноместо и какая кладовая относятся к квартире и зарегистрированы ли они так, как описано.',
  'أي موقف وأي مخزن يتبعان الشقة، وأنهما مسجلان كما هو موصوف.',
  'Welke parkeerplaats en welke berging bij de woning horen, en dat ze ingeschreven zijn zoals beschreven.',
  'Które miejsce parkingowe i która komórka należą do mieszkania oraz czy są zarejestrowane zgodnie z opisem.',
  'Hvilken parkeringsplass og hvilken bod som hører til boligen, og at de er tinglyst slik de er beskrevet.',
  'Vilken parkeringsplats och vilket förråd som hör till bostaden, och att de är registrerade så som de beskrivs.')
a('.trustDossier.cards[3][1]',
  'La reserva, el contrato privado y el resto del pago, y el aval bancario de las cantidades entregadas a cuenta, confirmados antes de la reserva.',
  'La réservation, le contrat privé et le solde, ainsi que la garantie bancaire des sommes versées d’avance, confirmés avant la réservation.',
  'Reservierung, privater Kaufvertrag und Restzahlung sowie die Bankbürgschaft für Anzahlungen, vor der Reservierung bestätigt.',
  'Бронирование, частный договор и остаток платежа, а также банковская гарантия на авансовые платежи — подтверждаются до бронирования.',
  'الحجز والعقد الخاص والرصيد، والضمان المصرفي للدفعات المقدّمة، مؤكدة قبل الحجز.',
  'De reservering, het koopcontract en het restant, en de bankgarantie voor vooruitbetalingen, bevestigd vóór de reservering.',
  'Rezerwacja, umowa prywatna i pozostała płatność oraz gwarancja bankowa dla wpłat zaliczkowych — potwierdzone przed rezerwacją.',
  'Reservasjonen, den private kontrakten og restbeløpet, og bankgarantien for forskuddsbetalinger, bekreftet før reservasjon.',
  'Reservationen, det privata avtalet och slutbetalningen, och bankgarantin för förskottsbetalningar, bekräftade före reservation.')

# ---- architecture -------------------------------------------------------------------------------
a('.architecture.headlineHtml', 'Bloques blancos, <em>terrazas profundas</em>', 'Immeubles blancs, <em>terrasses profondes</em>',
  'Weiße Blöcke, <em>tiefe Terrassen</em>', 'Белые корпуса, <em>глубокие террасы</em>', 'مبانٍ بيضاء، <em>تراسات عميقة</em>',
  'Witte blokken, <em>diepe terrassen</em>', 'Białe budynki, <em>głębokie tarasy</em>', 'Hvite bygg, <em>dype terrasser</em>',
  'Vita hus, <em>djupa terrasser</em>')
a('.architecture.copy[0]',
  'En las imágenes del promotor los bloques son bajos y blancos, con terrazas profundas enmarcadas en blanco y gris, barandillas de vidrio y plantas en las terrazas superiores, sobre los jardines y las piscinas y muros revestidos de piedra.',
  'Sur les images du promoteur, les immeubles sont bas et blancs, avec des terrasses profondes encadrées de blanc et de gris, des garde-corps en verre et des plantations sur les terrasses hautes, au-dessus des jardins et des piscines et de murs parés de pierre.',
  'In den Bildern des Bauträgers sind die Blöcke niedrig und weiß, mit tiefen, weiß und grau gerahmten Terrassen, Glasbrüstungen und Bepflanzung auf den oberen Terrassen, über den Gärten und Pools auf steinverkleideten Mauern.',
  'На изображениях застройщика корпуса невысокие и белые, с глубокими террасами в бело-серых рамах, стеклянными ограждениями и зеленью на верхних террасах, над садами и бассейнами на облицованных камнем стенах.',
  'تظهر المباني في صور المطوّر منخفضة وبيضاء، بتراسات عميقة بإطارات بيضاء ورمادية، ودرابزين زجاجي، ونباتات على التراسات العليا، فوق الحدائق والمسابح على جدران مكسوّة بالحجر.',
  'Op de beelden van de ontwikkelaar zijn de blokken laag en wit, met diepe terrassen in witte en grijze kaders, glazen balustrades en beplanting op de bovenste terrassen, boven de tuinen en zwembaden op met steen beklede muren.',
  'Na zdjęciach dewelopera budynki są niskie i białe, z głębokimi tarasami w białych i szarych ramach, szklanymi balustradami i zielenią na górnych tarasach, ponad ogrodami i basenami, na murach obłożonych kamieniem.',
  'På utbyggerens bilder er byggene lave og hvite, med dype terrasser innrammet i hvitt og grått, glassrekkverk og beplantning på de øvre terrassene, over hagene og bassengene på steinkledde murer.',
  'På exploatörens bilder är husen låga och vita, med djupa terrasser inramade i vitt och grått, glasräcken och planteringar på de övre terrasserna, ovanför trädgårdarna och poolerna på stenklädda murar.')
a('.architecture.copy[1]',
  'Las viviendas están en bloques de tres plantas sobre un garaje subterráneo. El promotor las numera por bloque, portal, planta y puerta, y así las identifica la tabla.',
  'Les logements sont répartis dans des immeubles de trois niveaux sur un parking souterrain. Le promoteur les numérote par immeuble, cage, étage et porte, et c’est ainsi que le tableau les désigne.',
  'Die Wohnungen liegen in dreigeschossigen Blöcken über einer Tiefgarage. Der Bauträger nummeriert sie nach Block, Aufgang, Etage und Tür, und so bezeichnet sie auch die Tabelle.',
  'Квартиры расположены в трёхэтажных корпусах над подземным паркингом. Застройщик нумерует их по корпусу, подъезду, этажу и двери, и так же они обозначены в таблице.',
  'تقع الشقق في مبانٍ من ثلاثة طوابق فوق مرآب تحت الأرض. ويرقّمها المطوّر بحسب المبنى والمدخل والطابق والباب، وبهذا يشير إليها الجدول.',
  'De woningen liggen in blokken met drie bouwlagen boven een ondergrondse garage. De ontwikkelaar nummert ze per blok, portiek, verdieping en deur, en zo verwijst ook de tabel ernaar.',
  'Mieszkania znajdują się w trzykondygnacyjnych budynkach nad garażem podziemnym. Deweloper numeruje je według budynku, klatki, piętra i drzwi i tak też oznacza je tabela.',
  'Leilighetene ligger i bygg med tre etasjer over en parkeringskjeller. Utbyggeren nummererer dem etter bygg, oppgang, etasje og dør, og slik viser også tabellen til dem.',
  'Lägenheterna ligger i hus med tre våningar ovanför ett garage under mark. Exploatören numrerar dem efter hus, uppgång, våning och dörr, och så hänvisar även tabellen till dem.')
a('.architecture.highlights[0][1]',
  'Planta baja y dos plantas altas, con ascensores, sobre un garaje subterráneo con trasteros.',
  'Rez-de-chaussée et deux étages, avec ascenseurs, sur un parking souterrain avec caves.',
  'Erdgeschoss und zwei Obergeschosse mit Aufzügen über einer Tiefgarage mit Abstellräumen.',
  'Первый этаж и два верхних, с лифтами, над подземным паркингом с кладовыми.',
  'طابق أرضي وطابقان علويان، مع مصاعد، فوق مرآب تحت الأرض مع مخازن.',
  'Begane grond en twee verdiepingen, met liften, boven een ondergrondse garage met bergingen.',
  'Parter i dwa piętra, z windami, nad garażem podziemnym z komórkami lokatorskimi.',
  'Første etasje og to etasjer over, med heis, over en parkeringskjeller med boder.',
  'Bottenvåning och två våningar till, med hissar, ovanför ett garage under mark med förråd.')
a('.architecture.highlights[1][1]',
  'De {N18.37} a {N155.46} {U}, con toma de agua, desagüe, iluminación, toma de corriente y toma de televisión en cada una.',
  'De {N18.37} à {N155.46} {U}, avec point d’eau, évacuation, éclairage, prise électrique et prise TV sur chacune.',
  'Von {N18.37} bis {N155.46} {U}, jeweils mit Wasseranschluss, Entwässerung, Beleuchtung, Steckdose und TV-Anschluss.',
  'От {N18.37} до {N155.46} {U}, на каждой — вода, водоотвод, освещение, электрическая и телевизионная розетки.',
  'من {N18.37} إلى {N155.46} {U}، مع نقطة مياه وتصريف وإنارة ومقبس كهرباء ومقبس تلفاز في كل منها.',
  'Van {N18.37} tot {N155.46} {U}, elk met een waterpunt, afvoer, verlichting, een stopcontact en een tv-aansluiting.',
  'Od {N18.37} do {N155.46} {U}, na każdym punkt wodny, odpływ, oświetlenie, gniazdko elektryczne i gniazdo telewizyjne.',
  'Fra {N18.37} til {N155.46} {U}, hver med vannuttak, avløp, belysning, stikkontakt og TV-uttak.',
  'Från {N18.37} till {N155.46} {U}, var och en med vattenuttag, avlopp, belysning, eluttag och tv-uttag.')
a('.architecture.highlights[2][1]',
  'Cinco de las viviendas disponibles en planta baja tienen jardín privado en sus planos, de {N8.78} a {N82.23} {U}.',
  'Cinq des logements disponibles en rez-de-chaussée ont un jardin privatif sur leur plan, de {N8.78} à {N82.23} {U}.',
  'Fünf der verfügbaren Erdgeschosswohnungen haben laut Grundriss einen privaten Garten von {N8.78} bis {N82.23} {U}.',
  'У пяти свободных квартир на первом этаже по планировкам есть частный сад от {N8.78} до {N82.23} {U}.',
  'لخمس من الشقق المتاحة في الطابق الأرضي حديقة خاصة في مخططاتها، من {N8.78} إلى {N82.23} {U}.',
  'Vijf van de beschikbare benedenwoningen hebben op hun plattegrond een eigen tuin van {N8.78} tot {N82.23} {U}.',
  'Pięć dostępnych mieszkań na parterze ma na rzutach prywatny ogród od {N8.78} do {N82.23} {U}.',
  'Fem av de ledige leilighetene i første etasje har privat hage på plantegningen, på {N8.78} til {N82.23} {U}.',
  'Fem av de lediga bottenvåningarna har egen trädgård på planritningen, på {N8.78} till {N82.23} {U}.')
a('.architecture.highlights[3][1]',
  'Fachadas de doble hoja de ladrillo con cámara de aire aislada, enfoscadas y pintadas para exterior.',
  'Façades en brique à double paroi avec lame d’air isolée, enduites et peintes pour l’extérieur.',
  'Zweischalige Ziegelfassaden mit gedämmter Luftschicht, verputzt und mit Außenfarbe gestrichen.',
  'Двухслойные кирпичные фасады с утеплённой воздушной прослойкой, оштукатуренные и окрашенные фасадной краской.',
  'واجهات من الطوب بطبقتين مع فراغ هوائي معزول، مكسوّة بالملاط ومطلية للخارج.',
  'Spouwmuren van baksteen met een geïsoleerde luchtspouw, gepleisterd en geschilderd voor buiten.',
  'Dwuwarstwowe ceglane elewacje z ocieploną pustką powietrzną, otynkowane i pomalowane farbą elewacyjną.',
  'Tosjikts murfasader med isolert luftspalte, pusset og malt for utendørs bruk.',
  'Tvåskaliga tegelfasader med isolerad luftspalt, putsade och målade för utomhusbruk.')
a('.architecture.highlights[4][1]',
  'Carpintería de aluminio con rotura de puente térmico y doble acristalamiento, y persianas motorizadas en los dormitorios.',
  'Menuiseries en aluminium à rupture de pont thermique avec double vitrage, et volets motorisés dans les chambres.',
  'Aluminiumrahmen mit thermischer Trennung und Doppelverglasung sowie motorisierte Rollläden in den Schlafzimmern.',
  'Алюминиевые рамы с терморазрывом и двойным остеклением, моторизованные рольставни в спальнях.',
  'نوافذ ألمنيوم بعازل حراري وزجاج مزدوج، وستائر آلية في غرف النوم.',
  'Aluminium kozijnen met thermische onderbreking en dubbele beglazing, en gemotoriseerde rolluiken in de slaapkamers.',
  'Stolarka aluminiowa z przekładką termiczną i podwójnymi szybami oraz zmotoryzowane rolety w sypialniach.',
  'Aluminiumsvinduer med kuldebrobryter og tolags glass, og motoriserte sjalusier på soverommene.',
  'Aluminiumpartier med köldbrygga och tvåglasfönster, och motoriserade rullgardiner i sovrummen.')
a('.architecture.highlights[5][1]',
  'Agua caliente mediante bomba de calor aerotérmica, fachadas aisladas y grandes ventanales para la luz natural.',
  'Eau chaude par pompe à chaleur aérothermique, façades isolées et grandes baies pour la lumière naturelle.',
  'Warmwasser über eine Luftwärmepumpe, gedämmte Fassaden und große Fenster für Tageslicht.',
  'Горячая вода от аэротермального теплового насоса, утеплённые фасады и большие окна для естественного света.',
  'مياه ساخنة من مضخة حرارية هوائية، وواجهات معزولة، ونوافذ كبيرة للضوء الطبيعي.',
  'Warm water uit een luchtwarmtepomp, geïsoleerde gevels en grote ramen voor daglicht.',
  'Ciepła woda z powietrznej pompy ciepła, ocieplone elewacje i duże okna wpuszczające światło dzienne.',
  'Varmtvann fra luft-til-vann-varmepumpe, isolerte fasader og store vinduer for dagslys.',
  'Varmvatten från luftvärmepump, isolerade fasader och stora fönster för dagsljus.')

# ---- lifestyle ----------------------------------------------------------------------------------
a('.lifestyle.headlineHtml', 'Junto a <em>Selwo</em>', 'À côté de <em>Selwo</em>', 'Neben <em>Selwo</em>',
  'Рядом с <em>Selwo</em>', 'بجوار <em>سيلوو</em>', 'Naast <em>Selwo</em>', 'Obok <em>Selwo</em>', 'Ved <em>Selwo</em>',
  'Intill <em>Selwo</em>')
a('.lifestyle.copy',
  'Los documentos del promotor enumeran las zonas comunes sin superficies ni horarios, así que confirmamos qué está construido y en uso antes de cualquier reserva.',
  'Les documents du promoteur énumèrent les espaces communs sans surfaces ni horaires ; nous confirmons donc ce qui est construit et ouvert avant toute réservation.',
  'Die Unterlagen des Bauträgers nennen die Gemeinschaftsbereiche ohne Flächen oder Öffnungszeiten; wir bestätigen daher vor jeder Reservierung, was gebaut und geöffnet ist.',
  'В документах застройщика общие зоны перечислены без площадей и часов работы, поэтому до бронирования мы уточняем, что построено и работает.',
  'تذكر وثائق المطوّر المرافق المشتركة دون مساحات أو مواعيد، لذا نتحقق مما بُني وما هو مفتوح قبل أي حجز.',
  'De documenten van de ontwikkelaar noemen de gemeenschappelijke voorzieningen zonder oppervlakten of openingstijden, dus wij bevestigen vóór elke reservering wat gebouwd en open is.',
  'Dokumenty dewelopera wymieniają części wspólne bez powierzchni i godzin otwarcia, dlatego przed rezerwacją potwierdzamy, co jest wybudowane i czynne.',
  'Utbyggerens dokumenter lister fellesarealene uten arealer eller åpningstider, så vi bekrefter hva som er bygget og i drift før enhver reservasjon.',
  'Exploatörens dokument räknar upp de gemensamma ytorna utan ytor eller öppettider, så vi bekräftar vad som är byggt och öppet före varje reservation.')
a('.lifestyle.panels[0][0]', 'Las piscinas y los jardines', 'Les piscines et les jardins', 'Die Pools und Gärten',
  'Бассейны и сады', 'المسابح والحدائق', 'De zwembaden en tuinen', 'Baseny i ogrody', 'Bassengene og hagene',
  'Poolerna och trädgårdarna')
a('.lifestyle.panels[0][1]',
  'Piscinas exteriores para adultos y niños en jardines ajardinados, con tumbonas y sombrillas de brezo en las imágenes del promotor.',
  'Des piscines extérieures pour adultes et enfants dans des jardins paysagers, avec transats et parasols en paille sur les images du promoteur.',
  'Außenpools für Erwachsene und Kinder in angelegten Gärten, mit Liegen und Strohschirmen in den Bildern des Bauträgers.',
  'Открытые бассейны для взрослых и детей в ландшафтных садах, с шезлонгами и соломенными зонтами на изображениях застройщика.',
  'مسابح خارجية للكبار والأطفال في حدائق منسّقة، مع كراسي استلقاء ومظلات من القش في صور المطوّر.',
  'Buitenzwembaden voor volwassenen en kinderen in aangelegde tuinen, met ligbedden en rieten parasols op de beelden van de ontwikkelaar.',
  'Baseny zewnętrzne dla dorosłych i dzieci w zagospodarowanych ogrodach, z leżakami i parasolami ze strzechy na zdjęciach dewelopera.',
  'Utendørs bassenger for voksne og barn i opparbeidede hager, med solsenger og stråparasoller på utbyggerens bilder.',
  'Utomhuspooler för vuxna och barn i anlagda trädgårdar, med solsängar och halmparasoller på exploatörens bilder.')
a('.lifestyle.panels[1][1]',
  'Un spa con piscina cubierta y un gimnasio, entre las zonas comunes que enumera el promotor.',
  'Un spa avec piscine intérieure et une salle de sport, parmi les espaces communs listés par le promoteur.',
  'Ein Spa mit Innenpool und ein Fitnessraum, unter den Gemeinschaftsbereichen, die der Bauträger nennt.',
  'Спа с крытым бассейном и тренажёрный зал — среди общих зон, перечисленных застройщиком.',
  'سبا مع مسبح داخلي وصالة رياضية، ضمن المرافق المشتركة التي يذكرها المطوّر.',
  'Een spa met binnenzwembad en een fitnessruimte, onder de gemeenschappelijke voorzieningen die de ontwikkelaar noemt.',
  'Spa z krytym basenem i siłownia, wśród części wspólnych wymienionych przez dewelopera.',
  'Et spa med innendørsbasseng og et treningsrom, blant fellesarealene utbyggeren lister opp.',
  'Ett spa med inomhuspool och ett gym, bland de gemensamma ytor exploatören räknar upp.')
a('.lifestyle.panels[2][0]', 'Trabajo y ocio', 'Travail et loisirs', 'Arbeit und Freizeit', 'Работа и досуг', 'العمل والترفيه',
  'Werk en vrije tijd', 'Praca i wypoczynek', 'Arbeid og fritid', 'Arbete och fritid')
a('.lifestyle.panels[2][1]',
  'Una sala de coworking, una sala de cine y un Youth Club para los más jóvenes, tal como los describe el folleto.',
  'Un espace de coworking, une salle de cinéma et un club pour les plus jeunes, tels que la brochure les décrit.',
  'Ein Coworking-Raum, ein Kinoraum und ein Jugendclub für die jüngeren Bewohner, wie die Broschüre sie beschreibt.',
  'Коворкинг, кинозал и молодёжный клуб для младших жителей — так их описывает буклет.',
  'مساحة عمل مشتركة وقاعة سينما ونادٍ للشباب من السكان الأصغر سناً، كما يصفها الكتيّب.',
  'Een coworkingruimte, een bioscoopzaal en een jongerenclub voor de jongere bewoners, zoals de brochure ze beschrijft.',
  'Coworking, sala kinowa i klub młodzieżowy dla młodszych mieszkańców, jak opisuje je broszura.',
  'Et kontorfellesskap, et kinorom og en ungdomsklubb for de yngre beboerne, slik brosjyren beskriver dem.',
  'Ett coworkingrum, en biosalong och en ungdomsklubb för de yngre boende, så som broschyren beskriver dem.')

# ---- private viewing, location ------------------------------------------------------------------
a('.privateViewing.copy',
  'Una visita es la forma más rápida de valorar cómo avanza la obra y qué ve cada terraza.',
  'Une visite est le moyen le plus rapide de juger l’avancement des travaux et la vue de chaque terrasse.',
  'Ein Besuch ist der schnellste Weg, den Baufortschritt und den Blick jeder Terrasse zu beurteilen.',
  'Визит — самый быстрый способ оценить ход стройки и вид с каждой террасы.',
  'الزيارة أسرع طريقة لتقدير تقدّم الأعمال وما يطل عليه كل تراس.',
  'Een bezoek is de snelste manier om te zien hoe ver de bouw is en waar elk terras op uitkijkt.',
  'Wizyta to najszybszy sposób, by ocenić postęp prac i widok z każdego tarasu.',
  'Et besøk er den raskeste måten å se hvor langt byggearbeidet har kommet og hva hver terrasse ser ut over.',
  'Ett besök är det snabbaste sättet att bedöma hur långt bygget kommit och vad varje terrass har utsikt över.')
a('.privateViewing.insights[0][1]',
  'Vea con nosotros los bloques, los jardines y el estado de la obra.',
  'Découvrez avec nous les immeubles, les jardins et l’avancement des travaux.',
  'Sehen Sie mit uns die Blöcke, die Gärten und den Stand der Bauarbeiten.',
  'Осмотрите вместе с нами корпуса, сады и ход строительства.',
  'شاهدوا معنا المباني والحدائق ومرحلة الأعمال.',
  'Bekijk met ons de blokken, de tuinen en de stand van de bouw.',
  'Obejrzyjcie Państwo z nami budynki, ogrody i stan prac.',
  'Se byggene, hagene og byggearbeidet sammen med oss.',
  'Se husen, trädgårdarna och hur långt bygget kommit tillsammans med oss.')
a('.privateViewing.insights[2][1]',
  'Recorra las piscinas, el spa, el gimnasio y la sala de coworking.',
  'Parcourez les piscines, le spa, la salle de sport et l’espace de coworking.',
  'Gehen Sie durch die Pools, das Spa, den Fitnessraum und den Coworking-Raum.',
  'Пройдите по бассейнам, спа, тренажёрному залу и коворкингу.',
  'تجوّلوا في المسابح والسبا والصالة الرياضية ومساحة العمل المشتركة.',
  'Loop langs de zwembaden, de spa, de fitnessruimte en de coworkingruimte.',
  'Prosimy obejrzeć baseny, spa, siłownię i coworking.',
  'Gå gjennom bassengene, spaet, treningsrommet og kontorfellesskapet.',
  'Gå igenom poolerna, spaet, gymmet och coworkingrummet.')
a('.location.copy',
  'El folleto sitúa el conjunto junto al parque Selwo Aventura, en Estepona, con La Resina Golf cerca. El mapa muestra el emplazamiento según el propio mapa de situación del folleto, y las distancias son las del folleto; confirmamos los tiempos en coche en la visita.',
  'La brochure situe la résidence à côté du parc animalier Selwo Aventura, à Estepona, avec La Resina Golf à proximité. La carte montre le terrain d’après le plan de situation de la brochure, et les distances sont celles de la brochure ; nous confirmons les temps de trajet lors de la visite.',
  'Die Broschüre verortet die Anlage neben dem Tierpark Selwo Aventura in Estepona, mit La Resina Golf in der Nähe. Die Karte zeigt das Grundstück nach dem Lageplan der Broschüre, und die Entfernungen sind die der Broschüre; die Fahrzeiten bestätigen wir beim Besuch.',
  'Буклет помещает комплекс рядом с парком Selwo Aventura в Эстепоне, недалеко от гольф-клуба La Resina. Участок на карте показан по схеме из буклета, расстояния тоже взяты из буклета; время в пути мы уточняем при визите.',
  'يضع الكتيّب المجمع بجوار حديقة سيلوو أفينتورا في إستيبونا، وبالقرب منه لا ريسينا غولف. وتُظهر الخريطة الموقع وفق خريطة الموقع في الكتيّب نفسه، والمسافات أدناه مأخوذة من الكتيّب، ونؤكد أوقات القيادة خلال الزيارة.',
  'De brochure situeert het complex naast het dierenpark Selwo Aventura in Estepona, met La Resina Golf in de buurt. De kaart toont het terrein volgens de situatiekaart van de brochure en de afstanden zijn die van de brochure; de rijtijden bevestigen wij tijdens het bezoek.',
  'Broszura umieszcza osiedle obok parku zwierząt Selwo Aventura w Esteponie, w pobliżu pola La Resina Golf. Mapa pokazuje działkę według planu sytuacyjnego z broszury, a odległości pochodzą z broszury; czasy dojazdu potwierdzamy podczas wizyty.',
  'Brosjyren plasserer anlegget ved dyreparken Selwo Aventura i Estepona, med La Resina Golf i nærheten. Kartet viser tomten etter brosjyrens eget situasjonskart, og avstandene er brosjyrens; kjøretidene bekrefter vi på visningen.',
  'Broschyren placerar området intill djurparken Selwo Aventura i Estepona, med La Resina Golf i närheten. Kartan visar tomten efter broschyrens egen lägeskarta, och avstånden är broschyrens; körtiderna bekräftar vi vid besöket.')
a('.location.distances[0][0]', 'Selwo Aventura', 'Selwo Aventura', 'Selwo Aventura', 'Selwo Aventura', 'سيلوو أفينتورا',
  'Selwo Aventura', 'Selwo Aventura', 'Selwo Aventura', 'Selwo Aventura')
a('.location.distances[0][1]', 'Junto al conjunto', 'À côté de la résidence', 'Neben der Anlage', 'Рядом с комплексом',
  'بجوار المجمع', 'Naast het complex', 'Obok osiedla', 'Ved anlegget', 'Intill området')
a('.location.distances[1][0]', 'Aeropuertos de Málaga y Gibraltar', 'Aéroports de Málaga et de Gibraltar',
  'Flughäfen Málaga und Gibraltar', 'Аэропорты Малаги и Гибралтара', 'مطارا مالقة وجبل طارق',
  'Luchthavens van Málaga en Gibraltar', 'Lotniska w Maladze i Gibraltarze', 'Flyplassene i Málaga og Gibraltar',
  'Flygplatserna i Málaga och Gibraltar')
a('.location.distances[1][1]', 'Unos 45 minutos', 'Environ 45 minutes', 'Etwa 45 Minuten', 'Около 45 минут', 'نحو 45 دقيقة',
  'Ongeveer 45 minuten', 'Około 45 minut', 'Rundt 45 minutter', 'Cirka 45 minuter')

# ---- faq ----------------------------------------------------------------------------------------
a('.faq[0][1]',
  'De {E338000} a {E686000} por la vivienda, más {T} y gastos de compra, según el portal para agentes del promotor a 13 de noviembre de 2026.',
  'De {E338000} à {E686000} pour le logement, plus {T} et frais d’acquisition, selon le portail agents du promoteur au 13 novembre 2026.',
  'Von {E338000} bis {E686000} für die Wohnung, zuzüglich {T} und Kaufnebenkosten, laut Maklerportal des Bauträgers vom 13. November 2026.',
  'От {E338000} до {E686000} за квартиру, плюс {T} и расходы на покупку, по агентскому порталу застройщика на 13 ноября 2026 года.',
  'من {E338000} إلى {E686000} للشقة، مع إضافة {T} وتكاليف الشراء، بحسب بوابة الوكلاء لدى المطوّر في 13 نوفمبر 2026.',
  'Van {E338000} tot {E686000} voor de woning, plus {T} en aankoopkosten, volgens het makelaarsportaal van de ontwikkelaar op 13 november 2026.',
  'Od {E338000} do {E686000} za mieszkanie, plus {T} i koszty zakupu, według portalu dla agentów dewelopera z 13 listopada 2026.',
  'Fra {E338000} til {E686000} for boligen, pluss {T} og kjøpskostnader, ifølge utbyggerens meglerportal 13. november 2026.',
  'Från {E338000} till {E686000} för bostaden, plus {T} och köpkostnader, enligt exploatörens mäklarportal den 13 november 2026.')
a('.faq[1][1]',
  'Veintiséis: una de un dormitorio, doce de dos y trece de tres.',
  'Vingt-six : un d’une chambre, douze de deux et treize de trois.',
  'Sechsundzwanzig: eine mit einem Schlafzimmer, zwölf mit zwei und dreizehn mit drei.',
  'Двадцать шесть: одна с одной спальней, двенадцать с двумя и тринадцать с тремя.',
  'ست وعشرون: واحدة بغرفة نوم، واثنتا عشرة بغرفتين، وثلاث عشرة بثلاث غرف.',
  'Zesentwintig: één met één slaapkamer, twaalf met twee en dertien met drie.',
  'Dwadzieścia sześć: jedno z jedną sypialnią, dwanaście z dwiema i trzynaście z trzema.',
  'Tjueseks: én med ett soverom, tolv med to og tretten med tre.',
  'Tjugosex: en med ett sovrum, tolv med två och tretton med tre.')
a('.faq[2][1]',
  'De {N87.89} a {N148.27} {U} construidos, con {N63.20} a {N105.52} {U} útiles y terrazas de {N18.37} a {N155.46} {U}.',
  'De {N87.89} à {N148.27} {U} construits, avec {N63.20} à {N105.52} {U} de surface utile et des terrasses de {N18.37} à {N155.46} {U}.',
  'Von {N87.89} bis {N148.27} {U} bebaut, mit {N63.20} bis {N105.52} {U} Wohnfläche und Terrassen von {N18.37} bis {N155.46} {U}.',
  'От {N87.89} до {N148.27} {U} площади застройки, с полезной площадью от {N63.20} до {N105.52} {U} и террасами от {N18.37} до {N155.46} {U}.',
  'من {N87.89} إلى {N148.27} {U} مبنية، مع {N63.20} إلى {N105.52} {U} صافية، وتراسات من {N18.37} إلى {N155.46} {U}.',
  'Van {N87.89} tot {N148.27} {U} bebouwd, met {N63.20} tot {N105.52} {U} nuttige oppervlakte en terrassen van {N18.37} tot {N155.46} {U}.',
  'Od {N87.89} do {N148.27} {U} zabudowy, z {N63.20} do {N105.52} {U} powierzchni użytkowej i tarasami od {N18.37} do {N155.46} {U}.',
  'Fra {N87.89} til {N148.27} {U} bebygd areal, med {N63.20} til {N105.52} {U} bruksareal og terrasser på {N18.37} til {N155.46} {U}.',
  'Från {N87.89} till {N148.27} {U} byggyta, med {N63.20} till {N105.52} {U} nyttoyta och terrasser på {N18.37} till {N155.46} {U}.')
a('.faq[3][1]',
  'Sí. Según sus planos, cinco de las viviendas disponibles en planta baja tienen un jardín privado de {N8.78} a {N82.23} {U}.',
  'Oui. Selon leur plan, cinq des logements disponibles en rez-de-chaussée ont un jardin privatif de {N8.78} à {N82.23} {U}.',
  'Ja. Laut Grundriss haben fünf der verfügbaren Erdgeschosswohnungen einen privaten Garten von {N8.78} bis {N82.23} {U}.',
  'Да. По планировкам у пяти свободных квартир на первом этаже есть частный сад от {N8.78} до {N82.23} {U}.',
  'نعم. بحسب المخططات، لخمس من الشقق المتاحة في الطابق الأرضي حديقة خاصة من {N8.78} إلى {N82.23} {U}.',
  'Ja. Volgens hun plattegrond hebben vijf van de beschikbare benedenwoningen een eigen tuin van {N8.78} tot {N82.23} {U}.',
  'Tak. Według rzutów pięć dostępnych mieszkań na parterze ma prywatny ogród od {N8.78} do {N82.23} {U}.',
  'Ja. Etter plantegningene har fem av de ledige leilighetene i første etasje privat hage på {N8.78} til {N82.23} {U}.',
  'Ja. Enligt planritningarna har fem av de lediga bottenvåningarna egen trädgård på {N8.78} till {N82.23} {U}.')
a('.faq[4][1]',
  'No está en el precio indicado. Cada vivienda figura con una o dos plazas de garaje de {E15000} cada una y uno o dos trasteros de {E6000} cada uno, con precio en líneas aparte además de la vivienda.',
  'Pas dans le prix indiqué. Chaque logement est listé avec une ou deux places de parking à {E15000} chacune et une ou deux caves à {E6000} chacune, chiffrées sur des lignes séparées en plus du logement.',
  'Nicht im angegebenen Preis. Jede Wohnung ist mit einem oder zwei Stellplätzen zu je {E15000} und einem oder zwei Abstellräumen zu je {E6000} gelistet, die als eigene Positionen zum Wohnungspreis hinzukommen.',
  'Не входит в указанную цену. Каждая квартира значится с одним или двумя машиноместами по {E15000} и одной или двумя кладовыми по {E6000}, цены на которые указаны отдельными строками сверх цены квартиры.',
  'لا، ليس ضمن السعر المعروض. تُدرج كل شقة مع موقف أو موقفين بسعر {E15000} للموقف، ومخزن أو مخزنين بسعر {E6000} للمخزن، بسعر مستقل يُضاف إلى سعر الشقة.',
  'Niet in de getoonde prijs. Elke woning staat vermeld met één of twee parkeerplaatsen van {E15000} per stuk en één of twee bergingen van {E6000} per stuk, apart geprijsd bovenop de woning.',
  'Nie w podanej cenie. Każde mieszkanie figuruje z jednym lub dwoma miejscami parkingowymi po {E15000} i jedną lub dwiema komórkami po {E6000}, wycenionymi w osobnych pozycjach ponad cenę mieszkania.',
  'Ikke i prisen som vises. Hver bolig er oppført med én eller to parkeringsplasser à {E15000} og én eller to boder à {E6000}, priset på egne linjer i tillegg til boligen.',
  'Inte i det visade priset. Varje bostad listas med en eller två parkeringsplatser à {E15000} och ett eller två förråd à {E6000}, prissatta på egna rader utöver bostaden.')
a('.faq[5][1]',
  'El promotor no ha publicado fecha. Su portal indica que la construcción ha comenzado en la primera fase. Pedimos la fecha por escrito antes de cualquier reserva.',
  'Le promoteur n’a pas publié de date. Son portail indique que la construction a commencé sur la première phase. Nous demandons la date par écrit avant toute réservation.',
  'Der Bauträger hat keinen Termin veröffentlicht. Sein Portal meldet Baubeginn für den ersten Bauabschnitt. Wir verlangen den Termin vor jeder Reservierung schriftlich.',
  'Застройщик дату не опубликовал. На его портале указано, что строительство первой очереди началось. Мы запрашиваем дату письменно до любого бронирования.',
  'لم ينشر المطوّر موعداً. وتذكر بوابته أن البناء قد بدأ في المرحلة الأولى. ونطلب الموعد كتابياً قبل أي حجز.',
  'De ontwikkelaar heeft geen datum gepubliceerd. Zijn portaal meldt dat de bouw van de eerste fase is begonnen. Wij vragen de datum schriftelijk op vóór elke reservering.',
  'Deweloper nie podał daty. Jego portal informuje, że budowa pierwszego etapu się rozpoczęła. Prosimy o datę na piśmie przed każdą rezerwacją.',
  'Utbyggeren har ikke oppgitt noen dato. Portalen sier at byggingen av første byggetrinn har startet. Vi ber om datoen skriftlig før enhver reservasjon.',
  'Exploatören har inte angett något datum. Portalen anger att bygget av den första etappen har startat. Vi begär datumet skriftligen före varje reservation.')
a('.faq[6][1]',
  'El promotor no las ha publicado para estas viviendas. Se las confirmamos por escrito antes de que usted se comprometa.',
  'Le promoteur ne les a pas publiées pour ces logements. Nous vous les confirmons par écrit avant tout engagement.',
  'Der Bauträger hat sie für diese Wohnungen nicht veröffentlicht. Wir bestätigen sie Ihnen schriftlich, bevor Sie sich binden.',
  'Застройщик не опубликовал их для этих квартир. Мы подтвердим их вам письменно до того, как вы возьмёте на себя обязательства.',
  'لم ينشرها المطوّر لهذه الشقق. ونؤكدها لكم كتابياً قبل أي التزام.',
  'De ontwikkelaar heeft ze voor deze woningen niet gepubliceerd. Wij bevestigen ze u schriftelijk voordat u zich vastlegt.',
  'Deweloper nie opublikował ich dla tych mieszkań. Potwierdzimy je Państwu na piśmie przed podjęciem zobowiązania.',
  'Utbyggeren har ikke offentliggjort dem for disse boligene. Vi bekrefter dem skriftlig før De binder Dem.',
  'Exploatören har inte publicerat dem för dessa bostäder. Vi bekräftar dem skriftligen innan ni binder er.')

# ---- timeline, enquiry, seo ---------------------------------------------------------------------
a('.timeline.items[0][2]',
  'La lista de precios, los planos que tenemos de las viviendas que le interesan y la memoria de calidades.',
  'La liste de prix, les plans dont nous disposons pour les logements qui vous intéressent et le descriptif technique.',
  'Die Preisliste, die uns vorliegenden Grundrisse der Wohnungen, die Sie interessieren, und die Baubeschreibung.',
  'Прайс-лист, имеющиеся у нас планировки интересующих вас квартир и спецификация.',
  'قائمة الأسعار، والمخططات المتوفرة لدينا للشقق التي تهمّكم، ومواصفات البناء.',
  'De prijslijst, de plattegronden die wij hebben van de woningen die u interesseren, en de technische omschrijving.',
  'Cennik, posiadane przez nas rzuty interesujących Państwa mieszkań i specyfikacja techniczna.',
  'Prislisten, plantegningene vi har av boligene De er interessert i, og byggebeskrivelsen.',
  'Prislistan, de planritningar vi har för de bostäder ni är intresserade av, och byggbeskrivningen.')
a('.timeline.items[1][2]',
  'Organizamos la visita y recorremos con usted los jardines y las zonas comunes.',
  'Nous organisons la visite et parcourons avec vous les jardins et les espaces communs.',
  'Wir organisieren den Besuch und gehen mit Ihnen durch die Gärten und Gemeinschaftsbereiche.',
  'Мы организуем визит и вместе с вами осмотрим сады и общие зоны.',
  'ننظّم الزيارة ونتجوّل معكم في الحدائق والمرافق المشتركة.',
  'Wij regelen het bezoek en lopen met u door de tuinen en de gemeenschappelijke ruimten.',
  'Organizujemy wizytę i razem z Państwem obchodzimy ogrody i części wspólne.',
  'Vi ordner visningen og går gjennom hagene og fellesarealene sammen med Dem.',
  'Vi ordnar besöket och går igenom trädgårdarna och de gemensamma ytorna tillsammans med er.')
a('.enquiry.message',
  'Me gustaría recibir la información más reciente del proyecto Selwo Garden Residences.',
  'Je souhaite recevoir les dernières informations sur le projet Selwo Garden Residences.',
  'Ich möchte die aktuellen Projektinformationen zu Selwo Garden Residences erhalten.',
  'Я хотел(а) бы получить актуальную информацию о проекте Selwo Garden Residences.',
  'أرغب في الحصول على أحدث المعلومات عن مشروع Selwo Garden Residences.',
  'Ik ontvang graag de meest recente projectinformatie over Selwo Garden Residences.',
  'Chciałbym/Chciałabym otrzymać najnowsze informacje o projekcie Selwo Garden Residences.',
  'Jeg ønsker å motta den nyeste prosjektinformasjonen om Selwo Garden Residences.',
  'Jag vill gärna få den senaste projektinformationen om Selwo Garden Residences.')
a('.enquiry.note', 'Contexto del proyecto: Selwo Garden Residences.', 'Contexte du projet : Selwo Garden Residences.',
  'Projektkontext: Selwo Garden Residences.', 'Контекст проекта: Selwo Garden Residences.', 'سياق المشروع: Selwo Garden Residences.',
  'Projectcontext: Selwo Garden Residences.', 'Kontekst projektu: Selwo Garden Residences.', 'Prosjektkontekst: Selwo Garden Residences.',
  'Projektsammanhang: Selwo Garden Residences.')
a('.seo.title', 'Selwo Garden Residences - Estepona', 'Selwo Garden Residences - Estepona', 'Selwo Garden Residences - Estepona',
  'Selwo Garden Residences - Эстепона', 'Selwo Garden Residences - إستيبونا', 'Selwo Garden Residences - Estepona',
  'Selwo Garden Residences - Estepona', 'Selwo Garden Residences - Estepona', 'Selwo Garden Residences - Estepona')
a('.seo.h1', 'Selwo Garden Residences: veintiséis viviendas, Estepona', 'Selwo Garden Residences : vingt-six logements, Estepona',
  'Selwo Garden Residences: sechsundzwanzig Wohnungen, Estepona', 'Selwo Garden Residences: двадцать шесть квартир, Эстепона',
  'Selwo Garden Residences: ست وعشرون شقة، إستيبونا', 'Selwo Garden Residences: zesentwintig woningen, Estepona',
  'Selwo Garden Residences: dwadzieścia sześć mieszkań, Estepona', 'Selwo Garden Residences: tjueseks boliger, Estepona',
  'Selwo Garden Residences: tjugosex bostäder, Estepona')
a('.seo.h1Context', 'Veintiséis viviendas, Estepona', 'Vingt-six logements, Estepona', 'Sechsundzwanzig Wohnungen, Estepona',
  'Двадцать шесть квартир, Эстепона', 'ست وعشرون شقة، إستيبونا', 'Zesentwintig woningen, Estepona',
  'Dwadzieścia sześć mieszkań, Estepona', 'Tjueseks boliger, Estepona', 'Tjugosex bostäder, Estepona')

json.dump(T, open(f'{SP}/tr_s.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'strings to', f'{SP}/tr_s.json')
