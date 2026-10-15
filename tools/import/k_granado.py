# -*- coding: utf-8 -*-
"""Granado Homes: the strings the translation memory did not have.

Same shape as k_selwo.py. The unit size lines, the floorplan captions and the unit references are
templates; the prose is written by hand. Numbers are written in English format and re-formatted
per locale: {E321000} is a price, a decimal with two places (54.66) takes the locale's mark, {U} is m2.
Run once before assemble.py:   python3 tools/import/k_granado.py <scratch dir>
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
tm = json.load(open(f'{SP}/tm.json'))
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
    text = re.sub(r'(?<![\d.])(\d+)\.(\d\d)(?!\d)', lambda m: num(m.group(0), l), text)
    return text.replace('{U}', UNIT[l])


def find(prefix):
    if prefix in todo: return prefix
    hits = [t for t in todo if t.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]


SKIPPED = []
def a(prefix, *tr):
    if not any(t.startswith(prefix) for t in todo):
        SKIPPED.append(prefix); return   # the translation memory already has it
    en = find(prefix)
    assert len(tr) == 9, (prefix, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    T[en] = {l: en for l in LOCS}


# ------------------------------------------------------------ identifiers
for s in ('Granado Homes', 'Granado', 'Granado <em>Homes</em>'):
    if s in todo: same(s)
for t in todo:
    if re.fullmatch(r'\d[AB]\d-P\w\w-[A-C]', t): same(t)

# ------------------------------------------------------------ prices: substitute into a sibling's format
def subst(src, model, nums):
    """Take the translated `model` (a sibling string) and put this project's prices in its place."""
    for l in LOCS:
        v = tm[model][l]
        for old, new in nums:
            v = v.replace(money(old, l), money(new, l))
        T.setdefault(src, {})[l] = v

if 'From EUR 321,000 + VAT' in todo: subst('From EUR 321,000 + VAT', 'From EUR 834,000 + VAT', [(834000, 321000)])
if 'EUR 321,000 + VAT' in todo: subst('EUR 321,000 + VAT', 'EUR 834,000 + VAT', [(834000, 321000)])
if 'EUR 321,000 - EUR 558,000 + VAT' in todo:
    subst('EUR 321,000 - EUR 558,000 + VAT', 'EUR 834,000 - EUR 1,600,000 + VAT', [(1600000, 558000), (834000, 321000)])
for n in ('144', '27'):
    k = f'{n} homes'
    if k in todo:
        for l in LOCS:
            T.setdefault(k, {})[l] = tm['23 homes'][l].replace('23', n)

# ------------------------------------------------------------ floorplan captions, unit size lines
CAP = {'es': 'Vivienda {c}', 'fr': 'Logement {c}', 'de': 'Wohnung {c}', 'ru': 'Квартира {c}', 'ar': 'المسكن {c}',
       'nl': 'Woning {c}', 'pl': 'Lokal {c}', 'no': 'Bolig {c}', 'sv': 'Bostad {c}'}
PLAN = {'es': 'Plano de la vivienda {c}', 'fr': 'Plan du logement {c}', 'de': 'Grundriss der Wohnung {c}',
        'ru': 'Планировка квартиры {c}', 'ar': 'مخطط المسكن {c}', 'nl': 'Plattegrond van woning {c}',
        'pl': 'Rzut lokalu {c}', 'no': 'Plantegning av bolig {c}', 'sv': 'Planritning för bostad {c}'}
for t in todo:
    m = re.fullmatch(r'Home (\S+)', t)
    if m: T[t] = {l: CAP[l].format(c=m.group(1)) for l in LOCS}
    m = re.fullmatch(r'Floorplan of home (\S+)', t)
    if m: T[t] = {l: PLAN[l].format(c=m.group(1)) for l in LOCS}

# "{b} sqm built, {i} sqm interior, ..." in each locale's own words, taken from the Sotavento lines
# (built / interior / garden) and the covered and uncovered terrace words already used in the memory.
SZ = {
    'es': dict(b='{} m² construidos', i='{} m² interiores', c='{} m² de terraza cubierta', u='{} m² de terraza descubierta', p='{} m² de porche', g='{} m² de jardín'),
    'fr': dict(b='{} m² construits', i='{} m² intérieurs', c='{} m² de terrasse couverte', u='{} m² de terrasse découverte', p='{} m² de porche', g='{} m² de jardin'),
    'de': dict(b='{} m² bebaut', i='{} m² Innenfläche', c='{} m² überdachte Terrasse', u='{} m² offene Terrasse', p='{} m² Veranda', g='{} m² Garten'),
    'ru': dict(b='{} м² застроенной площади', i='{} м² внутри', c='крытая терраса {} м²', u='открытая терраса {} м²', p='крытая веранда {} м²', g='сад {} м²'),
    'ar': dict(b='{} م² مبنية', i='{} م² داخلية', c='{} م² تراس مسقوف', u='{} م² تراس مكشوف', p='{} م² رواق', g='{} م² حديقة'),
    'nl': dict(b='{} m² bebouwd', i='{} m² binnen', c='{} m² overdekt terras', u='{} m² open terras', p='{} m² veranda', g='{} m² tuin'),
    'pl': dict(b='{} m² zabudowy', i='{} m² wnętrza', c='{} m² tarasu zadaszonego', u='{} m² tarasu odkrytego', p='{} m² werandy', g='{} m² ogrodu'),
    'no': dict(b='{} m² bygd', i='{} m² innvendig', c='{} m² overbygd terrasse', u='{} m² åpen terrasse', p='{} m² veranda', g='{} m² hage'),
    'sv': dict(b='{} m² byggyta', i='{} m² inomhus', c='{} m² övertäckt terrass', u='{} m² öppen terrass', p='{} m² veranda', g='{} m² trädgård'),
}
KEY = {'built': 'b', 'interior': 'i', 'covered terrace': 'c', 'uncovered terrace': 'u', 'porch': 'p', 'garden': 'g'}
for t in todo:
    if not re.fullmatch(r'[\d.]+ sqm built, .*', t): continue
    parts = [p.strip() for p in t.split(', ')]
    out = {}
    for l in LOCS:
        segs = []
        for p in parts:
            m = re.fullmatch(r'([\d.]+) sqm (.+)', p)
            segs.append(SZ[l][KEY[m.group(2)]].format(num(m.group(1), l)))
        out[l] = ('، ' if l == 'ar' else ', ').join(segs)
    T[t] = out

# ------------------------------------------------------------ prose
# Reading guide: the floor words differ by locale. ru and no count the ground floor as the first
# storey, so "first and second floors" is "второй и третий этаж" / "andre og tredje etasje".

a('27 one-, two- and three-bedroom apartments, ground-floor homes with gardens',
  '27 apartamentos de uno, dos y tres dormitorios, viviendas en planta baja con jardín y áticos a la venta en Estepona, en edificios de baja altura con piscina, gimnasio y sala gourmet, cada uno con una plaza de garaje y un trastero. El anuncio del promotor da la entrega para mayo de 2028. Desde {E321000} más IVA.',
  '27 appartements d’une à trois chambres, logements en rez-de-chaussée avec jardin et penthouses proposés à Estepona, dans des bâtiments de faible hauteur avec piscine, salle de sport et salle gourmet, chacun avec une place de parking et un débarras. L’annonce du promoteur indique une livraison en mai 2028. À partir de {E321000} hors TVA.',
  '27 Wohnungen mit einem bis drei Schlafzimmern, Erdgeschosswohnungen mit Garten und Penthäuser in Estepona, in niedrigen Gebäuden mit Pool, Fitnessraum und Gourmetraum, jeweils mit einem Garagenstellplatz und einem Abstellraum. Laut Bauträger ist die Übergabe für Mai 2028 angegeben. Ab {E321000} zuzüglich MwSt.',
  '27 квартир с одной, двумя и тремя спальнями: квартиры на первом этаже с садом и пентхаусы в Эстепоне, в малоэтажных зданиях с бассейном, тренажёрным залом и гастрономическим залом, к каждой полагаются место в гараже и кладовая. По данным застройщика, сдача указана на май 2028 года. От {E321000} без НДС.',
  '27 شقة من غرفة نوم واحدة إلى ثلاث غرف نوم، ومساكن في الطابق الأرضي مع حديقة وبنتهاوس، معروضة في إستيبونا ضمن مبانٍ منخفضة الارتفاع مع مسبح وصالة رياضية وقاعة طعام راقية، ولكل منها موقف في المرآب ومخزن. يذكر المطوّر أن التسليم في مايو 2028. ابتداءً من {E321000} دون ضريبة القيمة المضافة.',
  '27 appartementen met één tot drie slaapkamers, woningen op de begane grond met tuin en penthouses in Estepona, in laagbouw met zwembad, fitnessruimte en gourmetruimte, elk met een parkeerplaats in de garage en een berging. Volgens de ontwikkelaar is de oplevering gepland voor mei 2028. Vanaf {E321000} excl. btw.',
  '27 mieszkań z jedną, dwiema i trzema sypialniami, lokali na parterze z ogrodem i penthouse’ów w Esteponie, w niskich budynkach z basenem, siłownią i salą gourmet; do każdego należą miejsce w garażu i komórka. Deweloper podaje termin oddania na maj 2028 r. Od {E321000} plus VAT.',
  '27 leiligheter med ett til tre soverom, boliger i første etasje med hage og toppleiligheter i Estepona, i lave bygg med basseng, treningsrom og gourmetrom, hver med en garasjeplass og en bod. Utbyggeren oppgir levering i mai 2028. Fra {E321000} pluss mva.',
  '27 lägenheter med ett till tre sovrum, bostäder i bottenvåningen med trädgård och takvåningar i Estepona, i låga byggnader med pool, gym och gourmetrum, alla med en garageplats och ett förråd. Exploatören anger leverans i maj 2028. Från {E321000} plus moms.')

a('27 of 144 one- to three-bedroom homes at Estepona with views',
  '27 de 144 viviendas de uno a tres dormitorios en Estepona con vistas a la bahía y al campo de golf, piscina, gimnasio, plaza de garaje y trastero, entrega prevista para mayo de 2028, desde {E321000} más IVA.',
  '27 logements sur 144, d’une à trois chambres, à Estepona, avec vue sur la baie et le golf, piscine, salle de sport, place de parking et débarras, livraison annoncée pour mai 2028, à partir de {E321000} hors TVA.',
  '27 von 144 Wohnungen mit einem bis drei Schlafzimmern in Estepona mit Blick auf die Bucht und den Golfplatz, Pool, Fitnessraum, Garagenstellplatz und Abstellraum, Übergabe für Mai 2028 angegeben, ab {E321000} zuzüglich MwSt.',
  '27 из 144 квартир с одной–тремя спальнями в Эстепоне с видом на залив и поле для гольфа, бассейном, тренажёрным залом, местом в гараже и кладовой, сдача указана на май 2028 года, от {E321000} без НДС.',
  '27 من أصل 144 مسكنًا من غرفة نوم واحدة إلى ثلاث غرف نوم في إستيبونا مع إطلالة على الخليج وملعب الغولف ومسبح وصالة رياضية وموقف في المرآب ومخزن، والتسليم مذكور في مايو 2028، ابتداءً من {E321000} دون ضريبة القيمة المضافة.',
  '27 van de 144 woningen met één tot drie slaapkamers in Estepona met uitzicht op de baai en de golfbaan, zwembad, fitnessruimte, garageplaats en berging, oplevering gepland voor mei 2028, vanaf {E321000} excl. btw.',
  '27 ze 144 mieszkań z jedną do trzech sypialni w Esteponie z widokiem na zatokę i pole golfowe, basenem, siłownią, miejscem w garażu i komórką, termin oddania podano na maj 2028 r., od {E321000} plus VAT.',
  '27 av 144 boliger med ett til tre soverom i Estepona med utsikt over bukten og golfbanen, basseng, treningsrom, garasjeplass og bod, levering oppgitt til mai 2028, fra {E321000} pluss mva.',
  '27 av 144 bostäder med ett till tre sovrum i Estepona med utsikt över bukten och golfbanan, pool, gym, garageplats och förråd, leverans angiven till maj 2028, från {E321000} plus moms.')

a('One- to three-bedroom apartments and penthouses at Estepona with a pool',
  'Apartamentos y áticos de uno a tres dormitorios en Estepona con piscina, gimnasio, plaza de garaje y trastero, desde {E321000} más IVA.',
  'Appartements et penthouses d’une à trois chambres à Estepona, avec piscine, salle de sport, place de parking et débarras, à partir de {E321000} hors TVA.',
  'Wohnungen und Penthäuser mit einem bis drei Schlafzimmern in Estepona mit Pool, Fitnessraum, Garagenstellplatz und Abstellraum, ab {E321000} zuzüglich MwSt.',
  'Квартиры и пентхаусы с одной–тремя спальнями в Эстепоне с бассейном, тренажёрным залом, местом в гараже и кладовой, от {E321000} без НДС.',
  'شقق وبنتهاوس من غرفة نوم واحدة إلى ثلاث غرف نوم في إستيبونا مع مسبح وصالة رياضية وموقف في المرآب ومخزن، ابتداءً من {E321000} دون ضريبة القيمة المضافة.',
  'Appartementen en penthouses met één tot drie slaapkamers in Estepona met zwembad, fitnessruimte, garageplaats en berging, vanaf {E321000} excl. btw.',
  'Mieszkania i penthouse’y z jedną do trzech sypialni w Esteponie z basenem, siłownią, miejscem w garażu i komórką, od {E321000} plus VAT.',
  'Leiligheter og toppleiligheter med ett til tre soverom i Estepona med basseng, treningsrom, garasjeplass og bod, fra {E321000} pluss mva.',
  'Lägenheter och takvåningar med ett till tre sovrum i Estepona med pool, gym, garageplats och förråd, från {E321000} plus moms.')

a('27 one-, two- and three-bedroom apartments, garden homes and penthouses at Estepona, with a pool',
  '27 apartamentos de uno, dos y tres dormitorios, viviendas con jardín y áticos en Estepona, con piscina, gimnasio y, en cada vivienda, plaza de garaje y trastero.',
  '27 appartements d’une, deux et trois chambres, logements avec jardin et penthouses à Estepona, avec piscine, salle de sport et, pour chaque logement, une place de parking et un débarras.',
  '27 Wohnungen mit einem, zwei und drei Schlafzimmern, Gartenwohnungen und Penthäuser in Estepona, mit Pool, Fitnessraum sowie Garagenstellplatz und Abstellraum zu jeder Wohnung.',
  '27 квартир с одной, двумя и тремя спальнями, квартиры с садом и пентхаусы в Эстепоне, с бассейном, тренажёрным залом, а также местом в гараже и кладовой при каждой квартире.',
  '27 شقة من غرفة نوم واحدة وغرفتين وثلاث غرف نوم، ومساكن مع حديقة وبنتهاوس في إستيبونا، مع مسبح وصالة رياضية، ومع كل مسكن موقف في المرآب ومخزن.',
  '27 appartementen met één, twee en drie slaapkamers, tuinwoningen en penthouses in Estepona, met zwembad, fitnessruimte en bij elke woning een garageplaats en een berging.',
  '27 mieszkań z jedną, dwiema i trzema sypialniami, lokali z ogrodem i penthouse’ów w Esteponie, z basenem, siłownią oraz miejscem w garażu i komórką przy każdym lokalu.',
  '27 leiligheter med ett, to og tre soverom, hageboliger og toppleiligheter i Estepona, med basseng, treningsrom og garasjeplass og bod til hver bolig.',
  '27 lägenheter med ett, två och tre sovrum, trädgårdsbostäder och takvåningar i Estepona, med pool, gym och en garageplats och ett förråd till varje bostad.')

# images and gallery
a('Computer-generated view of the communal pool in front of a terraced',
  'Imagen generada por ordenador de la piscina comunitaria frente a un bloque escalonado de baja altura bajo un cielo azul',
  'Image de synthèse de la piscine commune devant un bloc de faible hauteur à terrasses étagées, sous un ciel bleu',
  'Computergenerierte Ansicht des Gemeinschaftspools vor einem niedrigen, terrassierten Block unter blauem Himmel',
  'Компьютерная визуализация общего бассейна перед малоэтажным террасным корпусом под голубым небом',
  'صورة مُنشأة بالحاسوب للمسبح المشترك أمام مبنى منخفض الارتفاع متدرج الشرفات تحت سماء زرقاء',
  'Computergegenereerd beeld van het gemeenschappelijke zwembad voor een laag blok met terrassen onder een blauwe lucht',
  'Wizualizacja komputerowa wspólnego basenu przed niskim, tarasowym blokiem pod błękitnym niebem',
  'Datagenerert bilde av fellesbassenget foran et lavt, terrassert bygg under blå himmel',
  'Datorgenererad bild av den gemensamma poolen framför ett lågt terrasserat hus under blå himmel')
a('Computer-generated view of a paved path through planting',
  'Imagen generada por ordenador de un camino pavimentado entre la vegetación junto a los bloques escalonados',
  'Image de synthèse d’un chemin dallé à travers la végétation, le long des blocs à terrasses',
  'Computergenerierte Ansicht eines gepflasterten Wegs durch die Bepflanzung neben den terrassierten Blöcken',
  'Компьютерная визуализация мощёной дорожки среди зелени рядом с террасными корпусами',
  'صورة مُنشأة بالحاسوب لممر مرصوف وسط النباتات بجانب المباني المتدرجة الشرفات',
  'Computergegenereerd beeld van een bestraat pad door de beplanting naast de blokken met terrassen',
  'Wizualizacja komputerowa brukowanej ścieżki wśród zieleni obok tarasowych bloków',
  'Datagenerert bilde av en brolagt sti gjennom beplantningen ved siden av de terrasserte byggene',
  'Datorgenererad bild av en stenlagd stig genom planteringarna intill de terrasserade husen')
a('Computer-generated terrace with lounge furniture and a pergola',
  'Imagen generada por ordenador de una terraza con muebles de exterior y una pérgola, con vistas al campo de golf y al mar',
  'Image de synthèse d’une terrasse avec salon d’extérieur et pergola, face au golf et à la mer',
  'Computergenerierte Ansicht einer Terrasse mit Loungemöbeln und Pergola mit Blick über den Golfplatz und das Meer',
  'Компьютерная визуализация террасы с лаунж-мебелью и перголой, с видом на поле для гольфа и море',
  'صورة مُنشأة بالحاسوب لتراس بأثاث للجلوس وبرغولا تطل على ملعب الغولف والبحر',
  'Computergegenereerd beeld van een terras met loungemeubels en een pergola, met uitzicht over de golfbaan en de zee',
  'Wizualizacja komputerowa tarasu z meblami wypoczynkowymi i pergolą, z widokiem na pole golfowe i morze',
  'Datagenerert bilde av en terrasse med loungemøbler og en pergola, med utsikt over golfbanen og havet',
  'Datorgenererad bild av en terrass med loungemöbler och en pergola, med utsikt över golfbanan och havet')
a('Computer-generated living and dining room opening onto a terrace',
  'Imagen generada por ordenador de un salón comedor que se abre a una terraza con vistas al mar',
  'Image de synthèse d’un séjour avec salle à manger ouvrant sur une terrasse avec vue sur la mer',
  'Computergenerierte Ansicht eines Wohn- und Essbereichs, der sich zu einer Terrasse mit Meerblick öffnet',
  'Компьютерная визуализация гостиной со столовой, выходящей на террасу с видом на море',
  'صورة مُنشأة بالحاسوب لغرفة معيشة وطعام تفتح على تراس يطل على البحر',
  'Computergegenereerd beeld van een woon- en eetkamer die uitkomt op een terras met zeezicht',
  'Wizualizacja komputerowa salonu z jadalnią otwierającego się na taras z widokiem na morze',
  'Datagenerert bilde av en stue og spisestue som åpner seg mot en terrasse med utsikt over havet',
  'Datorgenererad bild av ett vardagsrum med matplats som öppnar sig mot en terrass med havsutsikt')
a('Computer-generated views of the development and its interiors',
  'Imágenes generadas por ordenador de la promoción y de sus interiores, y los planos de las 27 viviendas a la venta.',
  'Images de synthèse du programme et de ses intérieurs, et plans des 27 logements proposés.',
  'Computergenerierte Ansichten der Anlage und ihrer Innenräume sowie die Grundrisse der 27 angebotenen Wohnungen.',
  'Компьютерные визуализации комплекса и его интерьеров, а также планировки 27 предлагаемых квартир.',
  'صور مُنشأة بالحاسوب للمشروع ولمساحاته الداخلية، ومخططات المساكن السبعة والعشرين المعروضة.',
  'Computergegenereerde beelden van het project en de interieurs, en de plattegronden van de 27 aangeboden woningen.',
  'Wizualizacje komputerowe inwestycji i jej wnętrz oraz rzuty 27 oferowanych lokali.',
  'Datagenererte bilder av prosjektet og interiørene, og plantegningene av de 27 boligene som er oppført.',
  'Datorgenererade bilder av projektet och dess interiörer, och planritningarna för de 27 bostäder som är listade.')
a('All the images are computer-generated, and the furniture and decoration',
  'Todas las imágenes están generadas por ordenador, y el mobiliario y la decoración que aparecen en ellas son ilustrativos y no están incluidos. Los planos son del promotor, de abril y diciembre de 2025, y las superficies que figuran en ellos son aproximadas. Los nombres de las estancias en los planos están en español.',
  'Toutes les images sont des images de synthèse, et le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont ceux du promoteur, datés d’avril et de décembre 2025, et les surfaces qui y figurent sont approximatives. Les noms des pièces sur les plans sont en espagnol.',
  'Alle Bilder sind computergeneriert, und die darauf gezeigten Möbel und die Dekoration sind illustrativ und nicht enthalten. Die Grundrisse stammen vom Bauträger, vom April und Dezember 2025, und die darin angegebenen Flächen sind ungefähre Werte. Die Raumbezeichnungen in den Grundrissen sind auf Spanisch.',
  'Все изображения созданы на компьютере, а мебель и декор на них носят иллюстративный характер и не входят в стоимость. Планировки — застройщика, от апреля и декабря 2025 года, указанные на них площади приблизительны. Названия помещений на планах даны по-испански.',
  'جميع الصور مُنشأة بالحاسوب، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. المخططات من المطوّر وتاريخها أبريل وديسمبر 2025، والمساحات المذكورة فيها تقريبية. أسماء الغرف في المخططات بالإسبانية.',
  'Alle beelden zijn computergegenereerd, en het meubilair en de inrichting erop zijn illustratief en niet inbegrepen. De plattegronden zijn van de ontwikkelaar, van april en december 2025, en de oppervlakten erop zijn bij benadering. De kamernamen op de plattegronden zijn in het Spaans.',
  'Wszystkie obrazy są wygenerowane komputerowo, a meble i dekoracje na nich są ilustracyjne i nie wchodzą w zakres sprzedaży. Rzuty pochodzą od dewelopera, z kwietnia i grudnia 2025 r., a podane na nich powierzchnie są przybliżone. Nazwy pomieszczeń na rzutach są po hiszpańsku.',
  'Alle bildene er datagenererte, og møblene og dekorasjonen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens, fra april og desember 2025, og arealene på dem er omtrentlige. Romnavnene på plantegningene er på spansk.',
  'Alla bilder är datorgenererade, och möblerna och inredningen på dem är illustrativa och ingår inte. Planritningarna är exploatörens, från april och december 2025, och ytorna på dem är ungefärliga. Rumsnamnen på ritningarna är på spanska.')
a('Computer-generated view of the gourmet room',
  'Imagen generada por ordenador de la sala gourmet, una sala acristalada en planta baja con mesas de comedor, junto a la piscina al anochecer',
  'Image de synthèse de la salle gourmet, une salle vitrée au rez-de-chaussée avec des tables, à côté de la piscine au crépuscule',
  'Computergenerierte Ansicht des Gourmetraums, eines verglasten Erdgeschossraums mit Esstischen, neben dem Pool in der Dämmerung',
  'Компьютерная визуализация гастрономического зала — застеклённого помещения на первом этаже со столами — у бассейна в сумерках',
  'صورة مُنشأة بالحاسوب لقاعة الطعام الراقية، وهي قاعة زجاجية في الطابق الأرضي فيها طاولات طعام، بجانب المسبح عند الغسق',
  'Computergegenereerd beeld van de gourmetruimte, een beglaasde ruimte op de begane grond met eettafels, naast het zwembad in de schemering',
  'Wizualizacja komputerowa sali gourmet, przeszklonego pomieszczenia na parterze ze stołami, obok basenu o zmierzchu',
  'Datagenerert bilde av gourmetrommet, et glassfasadert rom i første etasje med spisebord, ved bassenget i skumringen',
  'Datorgenererad bild av gourmetrummet, ett glasat rum i bottenvåningen med matbord, intill poolen i skymningen')
a('The gourmet room at dusk',
  'La sala gourmet al anochecer', 'La salle gourmet au crépuscule', 'Der Gourmetraum in der Dämmerung', 'Гастрономический зал в сумерках',
  'قاعة الطعام الراقية عند الغسق', 'De gourmetruimte in de schemering', 'Sala gourmet o zmierzchu', 'Gourmetrommet i skumringen', 'Gourmetrummet i skymningen')
a('Computer-generated view of the glazed gym',
  'Imagen generada por ordenador del gimnasio acristalado bajo los bloques escalonados, con aparatos de ejercicio en su interior',
  'Image de synthèse de la salle de sport vitrée sous les blocs à terrasses, avec des appareils d’entraînement à l’intérieur',
  'Computergenerierte Ansicht des verglasten Fitnessraums unter den terrassierten Blöcken, mit Trainingsgeräten im Inneren',
  'Компьютерная визуализация застеклённого тренажёрного зала под террасными корпусами, с тренажёрами внутри',
  'صورة مُنشأة بالحاسوب للصالة الرياضية الزجاجية تحت المباني المتدرجة الشرفات، وفي داخلها أجهزة تمرين',
  'Computergegenereerd beeld van de beglaasde fitnessruimte onder de blokken met terrassen, met trainingstoestellen binnen',
  'Wizualizacja komputerowa przeszklonej siłowni pod tarasowymi blokami, ze sprzętem do ćwiczeń w środku',
  'Datagenerert bilde av det glassfasadertre treningsrommet under de terrasserte byggene, med treningsapparater inni',
  'Datorgenererad bild av det glasade gymmet under de terrasserade husen, med träningsredskap inuti')
a('A path through the gardens',
  'Un camino entre los jardines', 'Un chemin à travers les jardins', 'Ein Weg durch die Gärten', 'Дорожка среди садов',
  'ممر وسط الحدائق', 'Een pad door de tuinen', 'Ścieżka wśród ogrodów', 'En sti gjennom hagene', 'En stig genom trädgårdarna')
a('Computer-generated open-plan living room and kitchen',
  'Imagen generada por ordenador de un salón y cocina de planta abierta con un sofá curvo y una terraza al fondo',
  'Image de synthèse d’un séjour avec cuisine ouverte, un canapé courbe et une terrasse au fond',
  'Computergenerierte Ansicht eines offenen Wohnzimmers mit Küche, einem geschwungenen Sofa und einer Terrasse im Hintergrund',
  'Компьютерная визуализация гостиной, совмещённой с кухней, с изогнутым диваном и террасой за ней',
  'صورة مُنشأة بالحاسوب لغرفة معيشة ومطبخ مفتوحين مع أريكة منحنية وتراس في الخلف',
  'Computergegenereerd beeld van een open woonkamer met keuken, een gebogen bank en een terras erachter',
  'Wizualizacja komputerowa otwartego salonu z kuchnią, zakrzywioną sofą i tarasem w tle',
  'Datagenerert bilde av en åpen stue med kjøkken, en buet sofa og en terrasse bak',
  'Datorgenererad bild av ett öppet vardagsrum med kök, en svängd soffa och en terrass bakom')
a('Living room towards the terrace',
  'El salón hacia la terraza', 'Le séjour vers la terrasse', 'Das Wohnzimmer zur Terrasse hin', 'Гостиная с выходом на террасу',
  'غرفة المعيشة باتجاه التراس', 'De woonkamer richting het terras', 'Salon z widokiem na taras', 'Stuen mot terrassen', 'Vardagsrummet mot terrassen')
a('Computer-generated main bedroom with a double bed',
  'Imagen generada por ordenador del dormitorio principal con una cama doble, un mural en la pared y una ventana con cortinas',
  'Image de synthèse de la chambre principale avec un lit double, une fresque murale et une fenêtre avec rideaux',
  'Computergenerierte Ansicht des Hauptschlafzimmers mit Doppelbett, einem Wandbild und einem Fenster mit Vorhängen',
  'Компьютерная визуализация главной спальни с двуспальной кроватью, настенной росписью и окном со шторами',
  'صورة مُنشأة بالحاسوب لغرفة النوم الرئيسية مع سرير مزدوج ولوحة جدارية ونافذة بستائر',
  'Computergegenereerd beeld van de hoofdslaapkamer met een tweepersoonsbed, een muurschildering en een raam met gordijnen',
  'Wizualizacja komputerowa głównej sypialni z podwójnym łóżkiem, malowidłem na ścianie i oknem z zasłonami',
  'Datagenerert bilde av hovedsoverommet med en dobbeltseng, et veggmaleri og et vindu med gardiner',
  'Datorgenererad bild av huvudsovrummet med en dubbelsäng, en väggmålning och ett fönster med gardiner')
a('Computer-generated bedroom with two single beds',
  'Imagen generada por ordenador de un dormitorio con dos camas individuales y una ventana a una terraza',
  'Image de synthèse d’une chambre avec deux lits simples et une fenêtre donnant sur une terrasse',
  'Computergenerierte Ansicht eines Schlafzimmers mit zwei Einzelbetten und einem Fenster zu einer Terrasse',
  'Компьютерная визуализация спальни с двумя односпальными кроватями и окном на террасу',
  'صورة مُنشأة بالحاسوب لغرفة نوم بسريرين فرديين ونافذة تطل على تراس',
  'Computergegenereerd beeld van een slaapkamer met twee eenpersoonsbedden en een raam naar een terras',
  'Wizualizacja komputerowa sypialni z dwoma pojedynczymi łóżkami i oknem na taras',
  'Datagenerert bilde av et soverom med to enkeltsenger og et vindu mot en terrasse',
  'Datorgenererad bild av ett sovrum med två enkelsängar och ett fönster mot en terrass')
a('Bedroom with two beds',
  'Dormitorio con dos camas', 'Chambre avec deux lits', 'Schlafzimmer mit zwei Betten', 'Спальня с двумя кроватями',
  'غرفة نوم بسريرين', 'Slaapkamer met twee bedden', 'Sypialnia z dwoma łóżkami', 'Soverom med to senger', 'Sovrum med två sängar')
a('Computer-generated bathroom with a walk-in shower',
  'Imagen generada por ordenador de un baño con ducha a ras de suelo, un lavabo suspendido y un espejo',
  'Image de synthèse d’une salle de bains avec douche à l’italienne, vasque suspendue et miroir',
  'Computergenerierte Ansicht eines Badezimmers mit bodengleicher Dusche, einem wandhängenden Waschtisch und einem Spiegel',
  'Компьютерная визуализация ванной комнаты с душем без поддона, подвесной тумбой с раковиной и зеркалом',
  'صورة مُنشأة بالحاسوب لحمام فيه دش مفتوح وحوض معلّق ومرآة',
  'Computergegenereerd beeld van een badkamer met inloopdouche, een zwevend wastafelmeubel en een spiegel',
  'Wizualizacja komputerowa łazienki z prysznicem bez brodzika, wiszącą szafką z umywalką i lustrem',
  'Datagenerert bilde av et bad med dusj uten kant, en vegghengt servant og et speil',
  'Datorgenererad bild av ett badrum med duschplats utan kant, en vägghängd tvättställsskåp och en spegel')

# overview, why, architecture
a('A development of <em>144 homes</em>',
  'Una promoción de <em>144 viviendas</em>', 'Un programme de <em>144 logements</em>', 'Eine Anlage mit <em>144 Wohnungen</em>',
  'Комплекс из <em>144 квартир</em>', 'مشروع من <em>144 مسكنًا</em>', 'Een project van <em>144 woningen</em>',
  'Inwestycja z <em>144 lokalami</em>', 'Et prosjekt med <em>144 boliger</em>', 'Ett projekt med <em>144 bostäder</em>')
a('Granado Homes is a residential development of 144',
  'Granado Homes es una promoción residencial de 144 viviendas de uno, dos y tres dormitorios en seis edificios de baja altura en Estepona, en la zona que el anuncio del promotor llama la nueva Milla de Oro de Estepona. Las viviendas están orientadas al sur, con amplios ventanales y vistas a la bahía de Estepona y al campo de golf.',
  'Granado Homes est un programme résidentiel de 144 logements d’une, deux et trois chambres répartis dans six bâtiments de faible hauteur à Estepona, dans le secteur que l’annonce du promoteur appelle la nouvelle Mille d’Or d’Estepona. Les logements sont orientés au sud, avec de grandes baies vitrées et une vue sur la baie d’Estepona et le golf.',
  'Granado Homes ist eine Wohnanlage mit 144 Wohnungen mit einem, zwei und drei Schlafzimmern in sechs niedrigen Gebäuden in Estepona, in dem Gebiet, das der Bauträger die neue Goldene Meile von Estepona nennt. Die Wohnungen sind nach Süden ausgerichtet, mit großen Fenstern und Blick auf die Bucht von Estepona und den Golfplatz.',
  'Granado Homes — жилой комплекс из 144 квартир с одной, двумя и тремя спальнями в шести малоэтажных зданиях в Эстепоне, в районе, который застройщик называет Новой Золотой милей Эстепоны. Квартиры обращены на юг, с большими окнами и видом на залив Эстепоны и поле для гольфа.',
  'Granado Homes مشروع سكني من 144 مسكنًا بغرفة نوم واحدة وغرفتين وثلاث غرف نوم في ستة مبانٍ منخفضة الارتفاع في إستيبونا، في المنطقة التي يسميها المطوّر «نيو غولدن مايل» في إستيبونا. المساكن مواجهة للجنوب، بنوافذ واسعة وإطلالة على خليج إستيبونا وملعب الغولف.',
  'Granado Homes is een woonproject van 144 woningen met één, twee en drie slaapkamers in zes laagbouwgebouwen in Estepona, in het gebied dat de ontwikkelaar de nieuwe Golden Mile van Estepona noemt. De woningen liggen op het zuiden, met grote ramen en uitzicht op de baai van Estepona en de golfbaan.',
  'Granado Homes to osiedle 144 lokali z jedną, dwiema i trzema sypialniami w sześciu niskich budynkach w Esteponie, w okolicy, którą deweloper nazywa Nową Złotą Milą Estepony. Lokale są zwrócone na południe, mają duże okna i widok na zatokę Estepony oraz pole golfowe.',
  'Granado Homes er et boligprosjekt med 144 boliger med ett, to og tre soverom i seks lave bygg i Estepona, i området utbyggeren kaller den nye Golden Mile i Estepona. Boligene vender mot sør, med store vinduer og utsikt over bukten i Estepona og golfbanen.',
  'Granado Homes är ett bostadsprojekt med 144 bostäder med ett, två och tre sovrum i sex låga byggnader i Estepona, i det område som exploatören kallar den nya Golden Mile i Estepona. Bostäderna ligger mot söder, med stora fönster och utsikt över bukten vid Estepona och golfbanan.')
a('Residents share a pool, an indoor gym and a gourmet room',
  'Los residentes comparten una piscina, un gimnasio interior y una sala gourmet, rodeados de zonas verdes con especies autóctonas. El complejo es cerrado y está vigilado desde una garita de seguridad, y el precio de cada vivienda incluye una plaza de garaje y un trastero. El anuncio del promotor da la entrega para mayo de 2028.',
  'Les résidents partagent une piscine, une salle de sport intérieure et une salle gourmet, au milieu d’espaces verts plantés d’espèces locales. L’ensemble est clos et surveillé depuis une guérite de sécurité, et le prix de chaque logement comprend une place de parking et un débarras. L’annonce du promoteur indique une livraison en mai 2028.',
  'Die Bewohner teilen sich einen Pool, einen Fitnessraum im Innenbereich und einen Gourmetraum, umgeben von Grünflächen mit heimischen Pflanzen. Die Anlage ist abgeschlossen und wird von einem Sicherheitshäuschen aus überwacht, und im Preis jeder Wohnung sind ein Garagenstellplatz und ein Abstellraum enthalten. Laut Bauträger ist die Übergabe für Mai 2028 angegeben.',
  'Жильцы пользуются общим бассейном, тренажёрным залом в помещении и гастрономическим залом среди зелёных зон с местными растениями. Территория закрытая, её охраняют с поста охраны, а в цену каждой квартиры входят место в гараже и кладовая. По данным застройщика, сдача указана на май 2028 года.',
  'يتشارك السكان مسبحًا وصالة رياضية داخلية وقاعة طعام راقية وسط مساحات خضراء مزروعة بنباتات محلية. المجمّع مغلق وتتم مراقبته من غرفة حراسة، ويشمل سعر كل مسكن موقفًا في المرآب ومخزنًا. يذكر المطوّر أن التسليم في مايو 2028.',
  'De bewoners delen een zwembad, een fitnessruimte binnen en een gourmetruimte, te midden van groenzones met inheemse beplanting. Het complex is afgesloten en wordt bewaakt vanuit een beveiligingshuisje, en in de prijs van elke woning zijn een garageplaats en een berging inbegrepen. Volgens de ontwikkelaar is de oplevering gepland voor mei 2028.',
  'Mieszkańcy korzystają ze wspólnego basenu, siłowni w budynku i sali gourmet, wśród terenów zielonych z roślinnością rodzimą. Osiedle jest zamknięte i pilnowane z portierni, a w cenie każdego lokalu są miejsce w garażu i komórka. Deweloper podaje termin oddania na maj 2028 r.',
  'Beboerne deler et basseng, et innendørs treningsrom og et gourmetrom, omgitt av grøntområder med stedegen beplantning. Anlegget er lukket og overvåkes fra et vaktbod, og prisen på hver bolig inkluderer en garasjeplass og en bod. Utbyggeren oppgir levering i mai 2028.',
  'De boende delar en pool, ett gym inomhus och ett gourmetrum, omgivna av grönytor med inhemska växter. Området är inhägnat och bevakas från en vaktkur, och priset för varje bostad inkluderar en garageplats och ett förråd. Exploatören anger leverans i maj 2028.')
a('New apartments, garden homes and penthouses at Estepona, with a garage space',
  'Apartamentos, viviendas con jardín y áticos nuevos en Estepona, con plaza de garaje y trastero incluidos en el precio.',
  'Appartements, logements avec jardin et penthouses neufs à Estepona, avec place de parking et débarras compris dans le prix.',
  'Neue Wohnungen, Gartenwohnungen und Penthäuser in Estepona, mit Garagenstellplatz und Abstellraum im Preis enthalten.',
  'Новые квартиры, квартиры с садом и пентхаусы в Эстепоне; место в гараже и кладовая входят в цену.',
  'شقق ومساكن مع حديقة وبنتهاوس جديدة في إستيبونا، مع موقف في المرآب ومخزن مشمولين في السعر.',
  'Nieuwe appartementen, tuinwoningen en penthouses in Estepona, met garageplaats en berging inbegrepen in de prijs.',
  'Nowe mieszkania, lokale z ogrodem i penthouse’y w Esteponie, z miejscem w garażu i komórką w cenie.',
  'Nye leiligheter, hageboliger og toppleiligheter i Estepona, med garasjeplass og bod inkludert i prisen.',
  'Nya lägenheter, trädgårdsbostäder och takvåningar i Estepona, med garageplats och förråd inkluderade i priset.')
a('Buyers who want a new home at Estepona, from a one-bedroom',
  'Compradores que buscan una vivienda nueva en Estepona, desde un apartamento de un dormitorio hasta una vivienda de tres, con piscina, gimnasio y sala gourmet dentro del complejo.',
  'Acheteurs qui cherchent un logement neuf à Estepona, de l’appartement d’une chambre au logement de trois chambres, avec piscine, salle de sport et salle gourmet dans la résidence.',
  'Käufer, die in Estepona eine neue Wohnung suchen, vom Apartment mit einem Schlafzimmer bis zur Wohnung mit drei, mit Pool, Fitnessraum und Gourmetraum innerhalb der Anlage.',
  'Покупателям, которые хотят новое жильё в Эстепоне — от квартиры с одной спальней до квартиры с тремя — с бассейном, тренажёрным залом и гастрономическим залом на территории.',
  'للمشترين الذين يريدون مسكنًا جديدًا في إستيبونا، من شقة بغرفة نوم واحدة إلى مسكن بثلاث غرف نوم، مع مسبح وصالة رياضية وقاعة طعام راقية داخل المجمّع.',
  'Kopers die een nieuwe woning in Estepona willen, van een appartement met één slaapkamer tot een woning met drie, met zwembad, fitnessruimte en gourmetruimte binnen het complex.',
  'Dla kupujących, którzy szukają nowego lokalu w Esteponie, od mieszkania z jedną sypialnią po lokal z trzema, z basenem, siłownią i salą gourmet na terenie osiedla.',
  'Kjøpere som vil ha en ny bolig i Estepona, fra en leilighet med ett soverom til en bolig med tre, med basseng, treningsrom og gourmetrom i anlegget.',
  'Köpare som vill ha en ny bostad i Estepona, från en lägenhet med ett sovrum till en bostad med tre, med pool, gym och gourmetrum inom området.')
a('A garage space and a storage room come with every listed home',
  'Cada vivienda a la venta incluye una plaza de garaje y un trastero, y las condiciones del promotor no piden pago de reserva: el primer pago se hace al firmar el contrato de compraventa.',
  'Chaque logement proposé comprend une place de parking et un débarras, et les conditions du promoteur ne demandent aucun versement de réservation : le premier paiement se fait à la signature du contrat de vente.',
  'Zu jeder angebotenen Wohnung gehören ein Garagenstellplatz und ein Abstellraum, und die Konditionen des Bauträgers sehen keine Reservierungszahlung vor: Die erste Zahlung erfolgt bei Unterzeichnung des Kaufvertrags.',
  'К каждой предлагаемой квартире прилагаются место в гараже и кладовая, а по условиям застройщика платёж за бронирование не требуется: первый платёж вносится при подписании договора купли-продажи.',
  'يشمل كل مسكن معروض موقفًا في المرآب ومخزنًا، ولا تطلب شروط المطوّر دفعة حجز: تُسدَّد الدفعة الأولى عند توقيع عقد الشراء.',
  'Bij elke aangeboden woning horen een garageplaats en een berging, en de voorwaarden van de ontwikkelaar vragen geen reserveringsbetaling: de eerste betaling volgt bij ondertekening van de koopovereenkomst.',
  'Do każdego oferowanego lokalu należą miejsce w garażu i komórka, a warunki dewelopera nie przewidują opłaty rezerwacyjnej: pierwsza wpłata następuje przy podpisaniu umowy.',
  'Hver bolig som er oppført har en garasjeplass og en bod, og utbyggerens vilkår krever ingen reservasjonsbetaling: den første betalingen skjer ved signering av kjøpekontrakten.',
  'Till varje listad bostad hör en garageplats och ett förråd, och exploatörens villkor kräver ingen bokningsbetalning: den första betalningen görs när köpeavtalet undertecknas.')
a('The homes face south, with large windows and views of the Bay of Estepona and the golf course, in the area',
  'Las viviendas están orientadas al sur, con amplios ventanales y vistas a la bahía de Estepona y al campo de golf, en la zona que el anuncio del promotor llama la nueva Milla de Oro.',
  'Les logements sont orientés au sud, avec de grandes baies vitrées et une vue sur la baie d’Estepona et le golf, dans le secteur que l’annonce du promoteur appelle la nouvelle Mille d’Or.',
  'Die Wohnungen sind nach Süden ausgerichtet, mit großen Fenstern und Blick auf die Bucht von Estepona und den Golfplatz, in dem Gebiet, das der Bauträger die neue Goldene Meile nennt.',
  'Квартиры обращены на юг, с большими окнами и видом на залив Эстепоны и поле для гольфа, в районе, который застройщик называет Новой Золотой милей.',
  'المساكن مواجهة للجنوب، بنوافذ واسعة وإطلالة على خليج إستيبونا وملعب الغولف، في المنطقة التي يسميها المطوّر «نيو غولدن مايل».',
  'De woningen liggen op het zuiden, met grote ramen en uitzicht op de baai van Estepona en de golfbaan, in het gebied dat de ontwikkelaar de nieuwe Golden Mile noemt.',
  'Lokale są zwrócone na południe, mają duże okna i widok na zatokę Estepony oraz pole golfowe, w okolicy, którą deweloper nazywa Nową Złotą Milą.',
  'Boligene vender mot sør, med store vinduer og utsikt over bukten i Estepona og golfbanen, i området utbyggeren kaller den nye Golden Mile.',
  'Bostäderna ligger mot söder, med stora fönster och utsikt över bukten vid Estepona och golfbanan, i det område som exploatören kallar den nya Golden Mile.')
a('27 of the 144 homes are listed with a price',
  '27 de las 144 viviendas figuran con precio. Nueva Living reconfirma el precio y la disponibilidad con el promotor antes de cualquier visita.',
  '27 des 144 logements sont proposés avec un prix. Nueva Living reconfirme le prix et la disponibilité auprès du promoteur avant toute visite.',
  '27 der 144 Wohnungen sind mit Preis gelistet. Nueva Living bestätigt Preis und Verfügbarkeit beim Bauträger erneut, bevor es zu einer Besichtigung kommt.',
  '27 из 144 квартир указаны с ценой. Nueva Living повторно подтверждает цену и наличие у застройщика перед любым просмотром.',
  'تُعرض 27 من أصل 144 مسكنًا بأسعارها. تعيد Nueva Living تأكيد السعر والتوفر مع المطوّر قبل أي معاينة.',
  '27 van de 144 woningen worden met prijs aangeboden. Nueva Living bevestigt prijs en beschikbaarheid opnieuw bij de ontwikkelaar vóór elke bezichtiging.',
  '27 ze 144 lokali ma podaną cenę. Nueva Living ponownie potwierdza cenę i dostępność u dewelopera przed każdą wizytą.',
  '27 av de 144 boligene er oppført med pris. Nueva Living bekrefter pris og tilgjengelighet på nytt med utbyggeren før enhver visning.',
  '27 av de 144 bostäderna är listade med pris. Nueva Living bekräftar pris och tillgänglighet på nytt med exploatören före varje visning.')
a('Six low-rise buildings, <em>facing south</em>',
  'Seis edificios de baja altura, <em>orientados al sur</em>', 'Six bâtiments de faible hauteur, <em>orientés au sud</em>',
  'Sechs niedrige Gebäude, <em>nach Süden ausgerichtet</em>', 'Шесть малоэтажных зданий, <em>обращённых на юг</em>',
  'ستة مبانٍ منخفضة الارتفاع، <em>مواجهة للجنوب</em>', 'Zes laagbouwgebouwen, <em>op het zuiden gericht</em>',
  'Sześć niskich budynków, <em>zwróconych na południe</em>', 'Seks lave bygg, <em>vendt mot sør</em>', 'Sex låga byggnader, <em>vända mot söder</em>')
a('The development is made up of six low-rise buildings',
  'La promoción se compone de seis edificios de baja altura. Las viviendas están orientadas al sur y sus amplios ventanales miran hacia la bahía y el campo de golf.',
  'Le programme se compose de six bâtiments de faible hauteur. Les logements sont orientés au sud et leurs grandes baies vitrées donnent vers la baie et le golf.',
  'Die Anlage besteht aus sechs niedrigen Gebäuden. Die Wohnungen sind nach Süden ausgerichtet, und ihre großen Fenster blicken zur Bucht und zum Golfplatz.',
  'Комплекс состоит из шести малоэтажных зданий. Квартиры обращены на юг, а их большие окна смотрят на залив и поле для гольфа.',
  'يتكوّن المشروع من ستة مبانٍ منخفضة الارتفاع. المساكن مواجهة للجنوب، وتطل نوافذها الواسعة نحو الخليج وملعب الغولف.',
  'Het project bestaat uit zes laagbouwgebouwen. De woningen liggen op het zuiden en hun grote ramen kijken uit op de baai en de golfbaan.',
  'Inwestycja składa się z sześciu niskich budynków. Lokale są zwrócone na południe, a ich duże okna wychodzą w stronę zatoki i pola golfowego.',
  'Prosjektet består av seks lave bygg. Boligene vender mot sør, og de store vinduene ser mot bukten og golfbanen.',
  'Projektet består av sex låga byggnader. Bostäderna ligger mot söder, och deras stora fönster vetter mot bukten och golfbanan.')
a('The developer’s computer-generated views show terraced blocks',
  'Las imágenes generadas por ordenador del promotor muestran bloques escalonados rodeados de vegetación. Son ilustraciones, no los edificios terminados, y no nos han facilitado ninguna memoria de calidades.',
  'Les images de synthèse du promoteur montrent des blocs à terrasses étagées au milieu de la végétation. Ce sont des illustrations, pas les bâtiments terminés, et aucun descriptif des finitions ne nous a été remis.',
  'Die computergenerierten Ansichten des Bauträgers zeigen terrassierte Blöcke inmitten von Bepflanzung. Es sind Illustrationen, nicht die fertigen Gebäude, und eine Baubeschreibung der Ausstattung liegt uns nicht vor.',
  'Компьютерные визуализации застройщика показывают террасные корпуса среди зелени. Это иллюстрации, а не готовые здания, и спецификации отделки нам не предоставили.',
  'تُظهر الصور المُنشأة بالحاسوب من المطوّر مباني متدرجة الشرفات وسط النباتات. وهي رسوم توضيحية وليست المباني المكتملة، ولم تُسلَّم إلينا أي مواصفات للتشطيبات.',
  'De computergegenereerde beelden van de ontwikkelaar tonen blokken met terrassen te midden van beplanting. Het zijn illustraties, niet de voltooide gebouwen, en een specificatie van de afwerking is ons niet verstrekt.',
  'Wizualizacje komputerowe dewelopera przedstawiają tarasowe bloki wśród zieleni. To ilustracje, a nie gotowe budynki, i nie otrzymaliśmy specyfikacji wykończenia.',
  'Utbyggerens datagenererte bilder viser terrasserte bygg omgitt av beplantning. De er illustrasjoner, ikke de ferdige byggene, og vi har ikke fått noen beskrivelse av ferdigstillelsen.',
  'Exploatörens datorgenererade bilder visar terrasserade hus omgivna av planteringar. De är illustrationer, inte de färdiga byggnaderna, och vi har inte fått någon byggbeskrivning av utförandet.')
a('Buildings',
  'Edificios', 'Bâtiments', 'Gebäude', 'Здания', 'المباني', 'Gebouwen', 'Budynki', 'Bygg', 'Byggnader')
a('Six low-rise buildings.',
  'Seis edificios de baja altura.', 'Six bâtiments de faible hauteur.', 'Sechs niedrige Gebäude.', 'Шесть малоэтажных зданий.',
  'ستة مبانٍ منخفضة الارتفاع.', 'Zes laagbouwgebouwen.', 'Sześć niskich budynków.', 'Seks lave bygg.', 'Sex låga byggnader.')
a('South, with large windows.',
  'Sur, con amplios ventanales.', 'Sud, avec de grandes baies vitrées.', 'Süden, mit großen Fenstern.', 'Юг, с большими окнами.',
  'الجنوب، مع نوافذ واسعة.', 'Zuid, met grote ramen.', 'Południe, z dużymi oknami.', 'Sør, med store vinduer.', 'Söder, med stora fönster.')
a('A pool, an indoor gym and a gourmet room, with green areas',
  'Una piscina, un gimnasio interior y una sala gourmet, con zonas verdes de especies autóctonas.',
  'Une piscine, une salle de sport intérieure et une salle gourmet, avec des espaces verts d’espèces locales.',
  'Ein Pool, ein Fitnessraum im Innenbereich und ein Gourmetraum, mit Grünflächen aus heimischen Pflanzen.',
  'Бассейн, тренажёрный зал в помещении и гастрономический зал, зелёные зоны с местными растениями.',
  'مسبح وصالة رياضية داخلية وقاعة طعام راقية، مع مساحات خضراء بنباتات محلية.',
  'Een zwembad, een fitnessruimte binnen en een gourmetruimte, met groenzones met inheemse beplanting.',
  'Basen, siłownia w budynku i sala gourmet, tereny zielone z roślinnością rodzimą.',
  'Et basseng, et innendørs treningsrom og et gourmetrom, med grøntområder med stedegen beplantning.',
  'En pool, ett gym inomhus och ett gourmetrum, med grönytor med inhemska växter.')
a('Access',
  'Acceso', 'Accès', 'Zugang', 'Доступ', 'الدخول', 'Toegang', 'Dostęp', 'Adkomst', 'Tillträde')
a('An enclosed complex watched from a security gatehouse.',
  'Un complejo cerrado y vigilado desde una garita de seguridad.', 'Un ensemble clos, surveillé depuis une guérite de sécurité.',
  'Eine abgeschlossene Anlage, die von einem Sicherheitshäuschen aus überwacht wird.', 'Закрытая территория, охраняемая с поста охраны.',
  'مجمّع مغلق تتم مراقبته من غرفة حراسة.', 'Een afgesloten complex dat vanuit een beveiligingshuisje wordt bewaakt.',
  'Osiedle zamknięte, pilnowane z portierni.', 'Et lukket anlegg som overvåkes fra et vaktbod.', 'Ett inhägnat område som bevakas från en vaktkur.')

# residences
a('The 27 listed homes fall into three groups by floor',
  'Las 27 viviendas a la venta se dividen en tres grupos según la planta. La tabla siguiente las enumera todas con sus precios.',
  'Les 27 logements proposés se répartissent en trois groupes selon l’étage. Le tableau ci-dessous les énumère tous avec leurs prix.',
  'Die 27 angebotenen Wohnungen gliedern sich nach Geschoss in drei Gruppen. Die Tabelle unten listet sie alle mit ihren Preisen auf.',
  'Предлагаемые 27 квартир делятся на три группы по этажам. В таблице ниже перечислены все они с ценами.',
  'تنقسم المساكن السبعة والعشرون المعروضة إلى ثلاث مجموعات بحسب الطابق. يعرضها الجدول أدناه جميعًا مع أسعارها.',
  'De 27 aangeboden woningen vallen naar verdieping uiteen in drie groepen. De tabel hieronder noemt ze allemaal met hun prijzen.',
  '27 oferowanych lokali dzieli się na trzy grupy według kondygnacji. Poniższa tabela wymienia je wszystkie wraz z cenami.',
  'De 27 boligene som er oppført deles i tre grupper etter etasje. Tabellen under viser alle med priser.',
  'De 27 listade bostäderna delas in i tre grupper efter våning. Tabellen nedan listar alla med deras priser.')
a('Ground-floor homes with a garden',
  'Viviendas en planta baja con jardín', 'Logements en rez-de-chaussée avec jardin', 'Erdgeschosswohnungen mit Garten',
  'Квартиры на первом этаже с садом', 'مساكن في الطابق الأرضي مع حديقة', 'Woningen op de begane grond met tuin',
  'Lokale na parterze z ogrodem', 'Boliger i første etasje med hage', 'Bostäder i bottenvåningen med trädgård')
a('3 homes with one or two bedrooms',
  '3 viviendas de uno o dos dormitorios, de 54.66 a 100.46 {U} interiores y de 76.14 a 138.70 {U} construidos.',
  '3 logements d’une ou deux chambres, de 54.66 à 100.46 {U} intérieurs et de 76.14 à 138.70 {U} construits.',
  '3 Wohnungen mit einem oder zwei Schlafzimmern, 54.66 bis 100.46 {U} Innenfläche und 76.14 bis 138.70 {U} bebaut.',
  '3 квартиры с одной или двумя спальнями, от 54.66 до 100.46 {U} внутри и от 76.14 до 138.70 {U} застроенной площади.',
  '3 مساكن بغرفة نوم واحدة أو غرفتين، من 54.66 إلى 100.46 {U} داخلية ومن 76.14 إلى 138.70 {U} مبنية.',
  '3 woningen met één of twee slaapkamers, van 54.66 tot 100.46 {U} binnen en van 76.14 tot 138.70 {U} bebouwd.',
  '3 lokale z jedną lub dwiema sypialniami, od 54.66 do 100.46 {U} wnętrza i od 76.14 do 138.70 {U} zabudowy.',
  '3 boliger med ett eller to soverom, fra 54.66 til 100.46 {U} innvendig og fra 76.14 til 138.70 {U} bygd.',
  '3 bostäder med ett eller två sovrum, 54.66 till 100.46 {U} inomhus och 76.14 till 138.70 {U} byggyta.')
a('Porches of 27.95 to 35.09 sqm',
  'Porches de 27.95 a 35.09 {U} y jardines privados de 24.71 a 86.12 {U}.',
  'Porches de 27.95 à 35.09 {U} et jardins privés de 24.71 à 86.12 {U}.',
  'Verandas von 27.95 bis 35.09 {U} und private Gärten von 24.71 bis 86.12 {U}.',
  'Крытые веранды от 27.95 до 35.09 {U} и частные сады от 24.71 до 86.12 {U}.',
  'أروقة من 27.95 إلى 35.09 {U} وحدائق خاصة من 24.71 إلى 86.12 {U}.',
  'Veranda’s van 27.95 tot 35.09 {U} en privétuinen van 24.71 tot 86.12 {U}.',
  'Werandy od 27.95 do 35.09 {U} i prywatne ogrody od 24.71 do 86.12 {U}.',
  'Verandaer på 27.95 til 35.09 {U} og private hager på 24.71 til 86.12 {U}.',
  'Verandor på 27.95 till 35.09 {U} och privata trädgårdar på 24.71 till 86.12 {U}.')
a('Prices run from EUR 370,000 to EUR 521,000',
  'Los precios van de {E370000} a {E521000}.', 'Les prix vont de {E370000} à {E521000}.', 'Die Preise reichen von {E370000} bis {E521000}.',
  'Цены — от {E370000} до {E521000}.', 'تتراوح الأسعار من {E370000} إلى {E521000}.', 'De prijzen lopen van {E370000} tot {E521000}.',
  'Ceny wynoszą od {E370000} do {E521000}.', 'Prisene går fra {E370000} til {E521000}.', 'Priserna går från {E370000} till {E521000}.')
a('Apartments on the first and second floors',
  'Apartamentos en la primera y la segunda planta', 'Appartements au premier et au deuxième étage',
  'Wohnungen im ersten und zweiten Obergeschoss', 'Квартиры на втором и третьем этажах', 'شقق في الطابقين الأول والثاني',
  'Appartementen op de eerste en tweede verdieping', 'Mieszkania na pierwszym i drugim piętrze',
  'Leiligheter i andre og tredje etasje', 'Lägenheter på första och andra våningen')
a('21 apartments: 2 with one bedroom',
  '21 apartamentos: 2 de un dormitorio, 17 de dos y 2 de tres, de 46.00 a 94.79 {U} interiores y de 65.26 a 134.23 {U} construidos.',
  '21 appartements : 2 d’une chambre, 17 de deux et 2 de trois, de 46.00 à 94.79 {U} intérieurs et de 65.26 à 134.23 {U} construits.',
  '21 Wohnungen: 2 mit einem Schlafzimmer, 17 mit zwei und 2 mit drei, 46.00 bis 94.79 {U} Innenfläche und 65.26 bis 134.23 {U} bebaut.',
  '21 квартира: 2 с одной спальней, 17 с двумя и 2 с тремя, от 46.00 до 94.79 {U} внутри и от 65.26 до 134.23 {U} застроенной площади.',
  '21 شقة: 2 بغرفة نوم واحدة و17 بغرفتين و2 بثلاث غرف نوم، من 46.00 إلى 94.79 {U} داخلية ومن 65.26 إلى 134.23 {U} مبنية.',
  '21 appartementen: 2 met één slaapkamer, 17 met twee en 2 met drie, van 46.00 tot 94.79 {U} binnen en van 65.26 tot 134.23 {U} bebouwd.',
  '21 mieszkań: 2 z jedną sypialnią, 17 z dwiema i 2 z trzema, od 46.00 do 94.79 {U} wnętrza i od 65.26 do 134.23 {U} zabudowy.',
  '21 leiligheter: 2 med ett soverom, 17 med to og 2 med tre, fra 46.00 til 94.79 {U} innvendig og fra 65.26 til 134.23 {U} bygd.',
  '21 lägenheter: 2 med ett sovrum, 17 med två och 2 med tre, 46.00 till 94.79 {U} inomhus och 65.26 till 134.23 {U} byggyta.')
a('Covered terraces of 14.98 to 31.81 sqm on 12 of them',
  'Terrazas cubiertas de 14.98 a 31.81 {U} en 12 de ellas, y terrazas descubiertas de 3.60 a 20.23 {U}.',
  'Terrasses couvertes de 14.98 à 31.81 {U} pour 12 d’entre eux, et terrasses découvertes de 3.60 à 20.23 {U}.',
  'Überdachte Terrassen von 14.98 bis 31.81 {U} bei 12 davon und offene Terrassen von 3.60 bis 20.23 {U}.',
  'Крытые террасы от 14.98 до 31.81 {U} у 12 из них и открытые террасы от 3.60 до 20.23 {U}.',
  'تراسات مسقوفة من 14.98 إلى 31.81 {U} في 12 منها، وتراسات مكشوفة من 3.60 إلى 20.23 {U}.',
  'Overdekte terrassen van 14.98 tot 31.81 {U} bij 12 ervan en open terrassen van 3.60 tot 20.23 {U}.',
  'Tarasy zadaszone od 14.98 do 31.81 {U} w 12 z nich oraz tarasy odkryte od 3.60 do 20.23 {U}.',
  'Overbygde terrasser på 14.98 til 31.81 {U} i 12 av dem og åpne terrasser på 3.60 til 20.23 {U}.',
  'Övertäckta terrasser på 14.98 till 31.81 {U} i 12 av dem och öppna terrasser på 3.60 till 20.23 {U}.')
a('Prices run from EUR 321,000 to EUR 558,000',
  'Los precios van de {E321000} a {E558000}.', 'Les prix vont de {E321000} à {E558000}.', 'Die Preise reichen von {E321000} bis {E558000}.',
  'Цены — от {E321000} до {E558000}.', 'تتراوح الأسعار من {E321000} إلى {E558000}.', 'De prijzen lopen van {E321000} tot {E558000}.',
  'Ceny wynoszą od {E321000} do {E558000}.', 'Prisene går fra {E321000} til {E558000}.', 'Priserna går från {E321000} till {E558000}.')
a('3 two-bedroom penthouses of 61.89 to 69.48 sqm',
  '3 áticos de dos dormitorios, de 61.89 a 69.48 {U} interiores y de 87.81 a 99.97 {U} construidos.',
  '3 penthouses de deux chambres, de 61.89 à 69.48 {U} intérieurs et de 87.81 à 99.97 {U} construits.',
  '3 Penthäuser mit zwei Schlafzimmern, 61.89 bis 69.48 {U} Innenfläche und 87.81 bis 99.97 {U} bebaut.',
  '3 пентхауса с двумя спальнями, от 61.89 до 69.48 {U} внутри и от 87.81 до 99.97 {U} застроенной площади.',
  '3 بنتهاوس بغرفتي نوم، من 61.89 إلى 69.48 {U} داخلية ومن 87.81 إلى 99.97 {U} مبنية.',
  '3 penthouses met twee slaapkamers, van 61.89 tot 69.48 {U} binnen en van 87.81 tot 99.97 {U} bebouwd.',
  '3 penthouse’y z dwiema sypialniami, od 61.89 do 69.48 {U} wnętrza i od 87.81 do 99.97 {U} zabudowy.',
  '3 toppleiligheter med to soverom, fra 61.89 til 69.48 {U} innvendig og fra 87.81 til 99.97 {U} bygd.',
  '3 takvåningar med två sovrum, 61.89 till 69.48 {U} inomhus och 87.81 till 99.97 {U} byggyta.')
a('Uncovered terraces of 43.66 to 73.47 sqm',
  'Terrazas descubiertas de 43.66 a 73.47 {U}.', 'Terrasses découvertes de 43.66 à 73.47 {U}.', 'Offene Terrassen von 43.66 bis 73.47 {U}.',
  'Открытые террасы от 43.66 до 73.47 {U}.', 'تراسات مكشوفة من 43.66 إلى 73.47 {U}.', 'Open terrassen van 43.66 tot 73.47 {U}.',
  'Tarasy odkryte od 43.66 do 73.47 {U}.', 'Åpne terrasser på 43.66 til 73.47 {U}.', 'Öppna terrasser på 43.66 till 73.47 {U}.')
a('Prices run from EUR 420,000 to EUR 508,000',
  'Los precios van de {E420000} a {E508000}.', 'Les prix vont de {E420000} à {E508000}.', 'Die Preise reichen von {E420000} bis {E508000}.',
  'Цены — от {E420000} до {E508000}.', 'تتراوح الأسعار من {E420000} إلى {E508000}.', 'De prijzen lopen van {E420000} tot {E508000}.',
  'Ceny wynoszą od {E420000} do {E508000}.', 'Prisene går fra {E420000} til {E508000}.', 'Priserna går från {E420000} till {E508000}.')

# lifestyle
a('A pool, <em>a gym</em> and a gourmet room',
  'Una piscina, <em>un gimnasio</em> y una sala gourmet', 'Une piscine, <em>une salle de sport</em> et une salle gourmet',
  'Ein Pool, <em>ein Fitnessraum</em> und ein Gourmetraum', 'Бассейн, <em>тренажёрный зал</em> и гастрономический зал',
  'مسبح <em>وصالة رياضية</em> وقاعة طعام راقية', 'Een zwembad, <em>een fitnessruimte</em> en een gourmetruimte',
  'Basen, <em>siłownia</em> i sala gourmet', 'Et basseng, <em>et treningsrom</em> og et gourmetrom', 'En pool, <em>ett gym</em> och ett gourmetrum')
a('The shared areas sit among green areas',
  'Las zonas comunes están rodeadas de zonas verdes dentro de un complejo cerrado.',
  'Les parties communes sont entourées d’espaces verts, dans un ensemble clos.',
  'Die Gemeinschaftsbereiche liegen inmitten von Grünflächen in einer abgeschlossenen Anlage.',
  'Общие зоны расположены среди зелени на закрытой территории.',
  'تقع المناطق المشتركة وسط المساحات الخضراء داخل مجمّع مغلق.',
  'De gemeenschappelijke ruimten liggen te midden van groenzones in een afgesloten complex.',
  'Części wspólne leżą wśród terenów zielonych na zamkniętym osiedlu.',
  'Fellesområdene ligger blant grøntområder i et lukket anlegg.',
  'De gemensamma ytorna ligger bland grönytor i ett inhägnat område.')
a('A communal pool beside the blocks.',
  'Una piscina comunitaria junto a los bloques.', 'Une piscine commune à côté des blocs.', 'Ein Gemeinschaftspool neben den Blöcken.',
  'Общий бассейн рядом с корпусами.', 'مسبح مشترك بجانب المباني.', 'Een gemeenschappelijk zwembad naast de blokken.',
  'Wspólny basen obok bloków.', 'Et fellesbasseng ved siden av byggene.', 'En gemensam pool intill husen.')
a('An indoor gym inside the complex.',
  'Un gimnasio interior dentro del complejo.', 'Une salle de sport intérieure au sein de l’ensemble.', 'Ein Fitnessraum im Innenbereich innerhalb der Anlage.',
  'Тренажёрный зал в помещении на территории комплекса.', 'صالة رياضية داخلية داخل المجمّع.', 'Een fitnessruimte binnen in het complex.',
  'Siłownia w budynku na terenie osiedla.', 'Et innendørs treningsrom i anlegget.', 'Ett gym inomhus inom området.')
a('The gourmet room',
  'La sala gourmet', 'La salle gourmet', 'Der Gourmetraum', 'Гастрономический зал', 'قاعة الطعام الراقية', 'De gourmetruimte', 'Sala gourmet', 'Gourmetrommet', 'Gourmetrummet')
a('A gourmet room for residents.',
  'Una sala gourmet para los residentes.', 'Une salle gourmet pour les résidents.', 'Ein Gourmetraum für die Bewohner.',
  'Гастрономический зал для жильцов.', 'قاعة طعام راقية للسكان.', 'Een gourmetruimte voor de bewoners.',
  'Sala gourmet dla mieszkańców.', 'Et gourmetrom for beboerne.', 'Ett gourmetrum för de boende.')
a('The grounds',
  'Las zonas exteriores', 'Les espaces extérieurs', 'Die Außenanlagen', 'Территория', 'المساحات الخارجية', 'De buitenruimte', 'Tereny zewnętrzne', 'Uteområdene', 'Utomhusområdena')
a('Green areas planted with native species, in a complex watched',
  'Zonas verdes con especies autóctonas, en un complejo vigilado desde una garita de seguridad.',
  'Des espaces verts plantés d’espèces locales, dans un ensemble surveillé depuis une guérite de sécurité.',
  'Grünflächen mit heimischen Pflanzen, in einer Anlage, die von einem Sicherheitshäuschen aus überwacht wird.',
  'Зелёные зоны с местными растениями на территории, которую охраняют с поста охраны.',
  'مساحات خضراء بنباتات محلية، في مجمّع تتم مراقبته من غرفة حراسة.',
  'Groenzones met inheemse beplanting, in een complex dat vanuit een beveiligingshuisje wordt bewaakt.',
  'Tereny zielone z roślinnością rodzimą, na osiedlu pilnowanym z portierni.',
  'Grøntområder med stedegen beplantning, i et anlegg som overvåkes fra et vaktbod.',
  'Grönytor med inhemska växter, i ett område som bevakas från en vaktkur.')

# location
a('The development is at Estepona, in the area the developer’s listing calls',
  'La promoción está en Estepona, en la zona que el anuncio del promotor llama la nueva Milla de Oro de Estepona, con vistas a la bahía de Estepona y al campo de golf. Las viviendas están orientadas al sur.',
  'Le programme se trouve à Estepona, dans le secteur que l’annonce du promoteur appelle la nouvelle Mille d’Or d’Estepona, avec vue sur la baie d’Estepona et le golf. Les logements sont orientés au sud.',
  'Die Anlage liegt in Estepona, in dem Gebiet, das der Bauträger die neue Goldene Meile von Estepona nennt, mit Blick auf die Bucht von Estepona und den Golfplatz. Die Wohnungen sind nach Süden ausgerichtet.',
  'Комплекс находится в Эстепоне, в районе, который застройщик называет Новой Золотой милей Эстепоны, с видом на залив Эстепоны и поле для гольфа. Квартиры обращены на юг.',
  'يقع المشروع في إستيبونا، في المنطقة التي يسميها المطوّر «نيو غولدن مايل» في إستيبونا، مع إطلالة على خليج إستيبونا وملعب الغولف. المساكن مواجهة للجنوب.',
  'Het project ligt in Estepona, in het gebied dat de ontwikkelaar de nieuwe Golden Mile van Estepona noemt, met uitzicht op de baai van Estepona en de golfbaan. De woningen liggen op het zuiden.',
  'Inwestycja znajduje się w Esteponie, w okolicy, którą deweloper nazywa Nową Złotą Milą Estepony, z widokiem na zatokę Estepony i pole golfowe. Lokale są zwrócone na południe.',
  'Prosjektet ligger i Estepona, i området utbyggeren kaller den nye Golden Mile i Estepona, med utsikt over bukten i Estepona og golfbanen. Boligene vender mot sør.',
  'Projektet ligger i Estepona, i det område som exploatören kallar den nya Golden Mile i Estepona, med utsikt över bukten vid Estepona och golfbanan. Bostäderna ligger mot söder.')
if 'Estepona, New Golden Mile' in todo:
    for l in LOCS:
        T.setdefault('Estepona, New Golden Mile', {})[l] = re.sub(r'</?em>', '', tm['Estepona, <em>New Golden Mile</em>'][l])

# investment
a('The developer’s terms list no reservation payment.',
  'Las condiciones del promotor no recogen ningún pago de reserva.', 'Les conditions du promoteur ne prévoient aucun versement de réservation.',
  'Die Konditionen des Bauträgers sehen keine Reservierungszahlung vor.', 'Условия застройщика не предусматривают платежа за бронирование.',
  'لا تتضمن شروط المطوّر أي دفعة حجز.', 'De voorwaarden van de ontwikkelaar noemen geen reserveringsbetaling.',
  'Warunki dewelopera nie przewidują opłaty rezerwacyjnej.', 'Utbyggerens vilkår oppgir ingen reservasjonsbetaling.',
  'Exploatörens villkor anger ingen bokningsbetalning.')
a('Buyers who are not resident in Spain pay 30% plus VAT',
  'Los compradores no residentes en España pagan el 30% más IVA al firmar el contrato privado de compraventa y el 70% más IVA ante notario al finalizar. Los compradores residentes en España pagan el 20% más IVA y después el 80% más IVA.',
  'Les acheteurs non résidents en Espagne paient 30 % hors TVA à la signature du contrat de vente privé et 70 % hors TVA chez le notaire à l’achèvement. Les acheteurs résidents en Espagne paient 20 % hors TVA, puis 80 % hors TVA.',
  'Käufer ohne Wohnsitz in Spanien zahlen 30 % zuzüglich MwSt. bei Unterzeichnung des privaten Kaufvertrags und 70 % zuzüglich MwSt. bei Fertigstellung beim Notar. Käufer mit Wohnsitz in Spanien zahlen 20 % zuzüglich MwSt., danach 80 % zuzüglich MwSt.',
  'Покупатели, не проживающие в Испании, платят 30 % плюс НДС при подписании предварительного договора купли-продажи и 70 % плюс НДС у нотариуса при завершении сделки. Покупатели, проживающие в Испании, платят 20 % плюс НДС, затем 80 % плюс НДС.',
  'يدفع المشترون غير المقيمين في إسبانيا 30% زائد ضريبة القيمة المضافة عند توقيع عقد الشراء الخاص و70% زائد الضريبة أمام كاتب العدل عند الإتمام. ويدفع المشترون المقيمون في إسبانيا 20% زائد الضريبة، ثم 80% زائد الضريبة.',
  'Kopers die niet in Spanje wonen betalen 30% plus btw bij ondertekening van de onderhandse koopovereenkomst en 70% plus btw ten overstaan van de notaris bij oplevering. Kopers die in Spanje wonen betalen 20% plus btw, daarna 80% plus btw.',
  'Kupujący niebędący rezydentami Hiszpanii płacą 30% plus VAT przy podpisaniu umowy przedwstępnej i 70% plus VAT u notariusza, przy akcie notarialnym. Kupujący będący rezydentami Hiszpanii płacą 20% plus VAT, a następnie 80% plus VAT.',
  'Kjøpere som ikke er bosatt i Spania betaler 30 % pluss mva. ved signering av den private kjøpekontrakten og 70 % pluss mva. hos notarius ved overtakelse. Kjøpere bosatt i Spania betaler 20 % pluss mva., deretter 80 % pluss mva.',
  'Köpare som inte är bosatta i Spanien betalar 30 % plus moms vid undertecknandet av det privata köpeavtalet och 70 % plus moms hos notarien vid tillträdet. Köpare som är bosatta i Spanien betalar 20 % plus moms, därefter 80 % plus moms.')
a('The price list does not include VAT, which on a new home in Spain',
  'La lista de precios no incluye el IVA, que en una vivienda nueva en España suele ser del 10%; la lista no indica el tipo. Nueva Living confirma por escrito los impuestos y los gastos de compra.',
  'La liste de prix n’inclut pas la TVA, qui s’élève normalement à 10 % pour un logement neuf en Espagne ; la liste n’indique pas le taux. Nueva Living confirme par écrit les taxes et les frais d’achat.',
  'Die Preise der Preisliste verstehen sich zuzüglich MwSt., die bei einer neuen Wohnung in Spanien normalerweise 10 % beträgt; die Liste nennt den Satz nicht. Nueva Living bestätigt Steuern und Kaufnebenkosten schriftlich.',
  'Цены в прайс-листе указаны без НДС, который при покупке нового жилья в Испании обычно составляет 10 %; ставка в списке не названа. Nueva Living письменно подтверждает налоги и расходы на покупку.',
  'قائمة الأسعار لا تشمل ضريبة القيمة المضافة، وهي في المسكن الجديد في إسبانيا 10% عادةً، ولا تذكر القائمة النسبة. وتؤكد Nueva Living الضرائب ومصاريف الشراء كتابةً.',
  'De prijslijst is exclusief btw, dat bij een nieuwe woning in Spanje normaal 10% bedraagt; de lijst vermeldt het tarief niet. Nueva Living bevestigt de belastingen en aankoopkosten schriftelijk.',
  'Cennik nie obejmuje VAT, który przy nowym lokalu w Hiszpanii wynosi zwykle 10%; cennik nie podaje stawki. Nueva Living potwierdza na piśmie podatki i koszty zakupu.',
  'Prislisten inkluderer ikke mva., som for en ny bolig i Spania vanligvis er 10 %; listen oppgir ikke satsen. Nueva Living bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan inkluderar inte moms, som för en ny bostad i Spanien normalt är 10 %; listan anger inte satsen. Nueva Living bekräftar skatter och köpkostnader skriftligen.')
a('The price list and the developer’s listing include a garage space',
  'La lista de precios y el anuncio del promotor incluyen una plaza de garaje y un trastero en el precio de cada vivienda.',
  'La liste de prix et l’annonce du promoteur incluent une place de parking et un débarras dans le prix de chaque logement.',
  'Preisliste und Angaben des Bauträgers schließen im Preis jeder Wohnung einen Garagenstellplatz und einen Abstellraum ein.',
  'В прайс-листе и в объявлении застройщика в цену каждой квартиры включены место в гараже и кладовая.',
  'تشمل قائمة الأسعار وبيانات المطوّر موقفًا في المرآب ومخزنًا في سعر كل مسكن.',
  'De prijslijst en de vermelding van de ontwikkelaar omvatten in de prijs van elke woning een garageplaats en een berging.',
  'Cennik i ogłoszenie dewelopera obejmują w cenie każdego lokalu miejsce w garażu i komórkę.',
  'Prislisten og utbyggerens annonse inkluderer en garasjeplass og en bod i prisen på hver bolig.',
  'Prislistan och exploatörens annons inkluderar en garageplats och ett förråd i priset för varje bostad.')

# trust dossier
a('The documents we hold do not state the building licence',
  'Los documentos que tenemos no indican la licencia de obras ni la garantía de las cantidades entregadas a cuenta. Pedimos ambas antes de cualquier pago.',
  'Les documents dont nous disposons n’indiquent ni le permis de construire ni la garantie sur les sommes versées à l’avance. Nous demandons les deux avant tout paiement.',
  'In den uns vorliegenden Unterlagen sind weder die Baugenehmigung noch die Absicherung der Anzahlungen angegeben. Wir fordern beides vor jeder Zahlung an.',
  'В имеющихся у нас документах не указаны ни разрешение на строительство, ни гарантия по суммам, внесённым авансом. Мы запрашиваем и то и другое до любых платежей.',
  'لا تذكر الوثائق التي لدينا رخصة البناء ولا ضمان المبالغ المدفوعة مقدمًا. نطلب الاثنين قبل أي دفعة.',
  'In de documenten die wij hebben staan noch de bouwvergunning noch de waarborg op vooruitbetaalde bedragen. We vragen beide op vóór enige betaling.',
  'W posiadanych przez nas dokumentach nie podano ani pozwolenia na budowę, ani gwarancji na wpłaty z góry. Prosimy o jedno i drugie przed jakąkolwiek płatnością.',
  'Dokumentene vi har oppgir verken byggetillatelsen eller garantien for beløp betalt på forhånd. Vi ber om begge før enhver betaling.',
  'Handlingarna vi har anger varken bygglovet eller garantin för förskottsbetalningar. Vi begär båda före varje betalning.')
a('The developer’s listing gives delivery as May 2028 and no other document states a date, so we ask for the contractual date.',
  'El anuncio del promotor da la entrega para mayo de 2028 y ningún otro documento indica una fecha, por lo que pedimos la fecha contractual.',
  'L’annonce du promoteur indique une livraison en mai 2028 et aucun autre document ne mentionne de date ; nous demandons donc la date contractuelle.',
  'Der Bauträger gibt die Übergabe für Mai 2028 an, und kein anderes Dokument nennt ein Datum, daher fragen wir das vertragliche Datum an.',
  'Застройщик указывает сдачу на май 2028 года, и ни в одном другом документе даты нет, поэтому мы запрашиваем договорную дату.',
  'يذكر المطوّر أن التسليم في مايو 2028، ولا تذكر أي وثيقة أخرى تاريخًا، لذلك نطلب التاريخ التعاقدي.',
  'De ontwikkelaar noemt mei 2028 als oplevering en geen enkel ander document noemt een datum, dus vragen we naar de contractuele datum.',
  'Deweloper podaje termin oddania na maj 2028 r., a żaden inny dokument nie wskazuje daty, dlatego prosimy o termin wskazany w umowie.',
  'Utbyggeren oppgir levering i mai 2028, og ingen andre dokumenter oppgir en dato, så vi ber om den kontraktsfestede datoen.',
  'Exploatören anger leverans i maj 2028, och inga andra handlingar anger ett datum, så vi ber om det avtalade datumet.')
a('The price list gives a built area that includes a share of the communal areas',
  'La lista de precios da una superficie construida que incluye una parte de las zonas comunes, una superficie interior y las terrazas, porches y jardines por separado. En 11 viviendas los planos difieren ligeramente de la lista, y confirmamos qué cifra usa el contrato.',
  'La liste de prix donne une surface construite qui inclut une part des parties communes, une surface intérieure, et les terrasses, porches et jardins séparément. Pour 11 logements, les plans diffèrent légèrement de la liste, et nous confirmons quel chiffre retient le contrat.',
  'Die Preisliste nennt eine bebaute Fläche, die einen Anteil der Gemeinschaftsflächen einschließt, eine Innenfläche sowie Terrassen, Veranden und Gärten getrennt. Bei 11 Wohnungen weichen die Grundrisse leicht von der Liste ab, und wir klären, welchen Wert der Vertrag verwendet.',
  'В прайс-листе указана застроенная площадь, включающая долю общих зон, внутренняя площадь, а террасы, веранды и сады — отдельно. У 11 квартир планировки немного отличаются от списка, и мы уточняем, какая цифра принята в договоре.',
  'تذكر قائمة الأسعار مساحة مبنية تشمل حصة من المناطق المشتركة ومساحة داخلية، والتراسات والأروقة والحدائق كلًّا على حدة. وفي 11 مسكنًا تختلف المخططات قليلًا عن القائمة، ونؤكد أي رقم يعتمده العقد.',
  'De prijslijst geeft een bebouwde oppervlakte inclusief een aandeel in de gemeenschappelijke delen, een binnenoppervlakte en de terrassen, veranda’s en tuinen apart. Bij 11 woningen wijken de plattegronden iets af van de lijst, en we bevestigen welk cijfer de overeenkomst hanteert.',
  'Cennik podaje powierzchnię zabudowy wraz z udziałem w częściach wspólnych, powierzchnię wnętrza oraz osobno tarasy, werandy i ogrody. W 11 lokalach rzuty nieznacznie różnią się od cennika i potwierdzamy, którą wartość przyjmuje umowa.',
  'Prislisten oppgir et bebygd areal som inkluderer en andel av fellesarealene, et innvendig areal og terrasser, verandaer og hager hver for seg. For 11 boliger avviker plantegningene litt fra listen, og vi bekrefter hvilken verdi kontrakten bruker.',
  'Prislistan anger en byggyta som inkluderar en andel av de gemensamma ytorna, en inomhusyta samt terrasser, verandor och trädgårdar var för sig. För 11 bostäder avviker ritningarna något från listan, och vi bekräftar vilket värde avtalet använder.')
a('We hold no quality specification for this development',
  'No tenemos ninguna memoria de calidades de esta promoción, por lo que esta página no describe los acabados ni los equipamientos. La pedimos antes de cualquier reserva.',
  'Nous ne disposons d’aucun descriptif de qualité pour ce programme, de sorte que cette page ne décrit ni les finitions ni les équipements. Nous le demandons avant toute réservation.',
  'Uns liegt keine Baubeschreibung für diese Anlage vor, deshalb werden Ausstattung und Materialien auf dieser Seite nicht beschrieben. Wir fordern sie vor jeder Reservierung an.',
  'У нас нет спецификации качества для этого комплекса, поэтому отделка и оснащение на этой странице не описаны. Мы запрашиваем её до любого бронирования.',
  'لا نملك مواصفات جودة لهذا المشروع، لذلك لا تصف هذه الصفحة التشطيبات ولا التجهيزات. نطلبها قبل أي حجز.',
  'We beschikken niet over een kwaliteitsspecificatie voor dit project, dus afwerking en uitrusting worden op deze pagina niet beschreven. We vragen die op vóór elke reservering.',
  'Nie mamy specyfikacji jakości tej inwestycji, więc ta strona nie opisuje wykończenia ani wyposażenia. Prosimy o nią przed jakąkolwiek rezerwacją.',
  'Vi har ingen kvalitetsbeskrivelse for dette prosjektet, så ferdigstillelsen og utstyret er ikke beskrevet på denne siden. Vi ber om den før enhver reservasjon.',
  'Vi har ingen byggbeskrivning för det här projektet, så utförande och utrustning beskrivs inte på den här sidan. Vi begär den före varje bokning.')

# availability
a('27 homes <em>currently listed</em>',
  '27 viviendas <em>a la venta ahora</em>', '27 logements <em>actuellement proposés</em>', '27 Wohnungen <em>derzeit im Angebot</em>',
  '27 квартир <em>в продаже сейчас</em>', '27 مسكنًا <em>معروضة حاليًا</em>', '27 woningen <em>nu aangeboden</em>',
  '27 lokali <em>obecnie w ofercie</em>', '27 boliger <em>oppført nå</em>', '27 bostäder <em>listade just nu</em>')
a('Prices are those of the developer’s price list, checked in October 2026',
  'Los precios son los de la lista de precios del promotor, consultada en octubre de 2026, y no incluyen el IVA. De las 144 viviendas de la promoción, 27 figuran como disponibles: 3 en planta baja con jardín, 21 apartamentos en la primera y la segunda planta y 3 áticos.',
  'Les prix sont ceux de la liste de prix du promoteur, consultée en octobre 2026, et s’entendent hors TVA. Sur les 144 logements du programme, 27 sont indiqués comme disponibles : 3 en rez-de-chaussée avec jardin, 21 appartements au premier et au deuxième étage et 3 penthouses.',
  'Die Preise stammen aus der Preisliste des Bauträgers, geprüft im Oktober 2026, und verstehen sich zuzüglich MwSt. Von den 144 Wohnungen der Anlage sind 27 als verfügbar aufgeführt: 3 im Erdgeschoss mit Garten, 21 Wohnungen im ersten und zweiten Obergeschoss und 3 Penthäuser.',
  'Цены взяты из прайс-листа застройщика, проверенного в октябре 2026 года, и указаны без НДС. Из 144 квартир комплекса как доступные указаны 27: 3 на первом этаже с садом, 21 квартира на втором и третьем этажах и 3 пентхауса.',
  'الأسعار هي أسعار قائمة المطوّر التي راجعناها في أكتوبر 2026، ولا تشمل ضريبة القيمة المضافة. من بين 144 مسكنًا في المشروع، يُذكر 27 مسكنًا على أنها متاحة: 3 في الطابق الأرضي مع حديقة و21 شقة في الطابقين الأول والثاني و3 بنتهاوس.',
  'De prijzen komen uit de prijslijst van de ontwikkelaar, gecontroleerd in oktober 2026, en zijn exclusief btw. Van de 144 woningen in het project staan er 27 als beschikbaar vermeld: 3 op de begane grond met tuin, 21 appartementen op de eerste en tweede verdieping en 3 penthouses.',
  'Ceny pochodzą z cennika dewelopera, sprawdzonego w październiku 2026 r., i nie obejmują VAT. Spośród 144 lokali w inwestycji 27 jest wskazanych jako dostępne: 3 na parterze z ogrodem, 21 mieszkań na pierwszym i drugim piętrze oraz 3 penthouse’y.',
  'Prisene er fra utbyggerens prisliste, kontrollert i oktober 2026, og er eksklusive mva. Av de 144 boligene i prosjektet er 27 oppført som tilgjengelige: 3 i første etasje med hage, 21 leiligheter i andre og tredje etasje og 3 toppleiligheter.',
  'Priserna är från exploatörens prislista, kontrollerad i oktober 2026, och är exklusive moms. Av de 144 bostäderna i projektet är 27 listade som tillgängliga: 3 i bottenvåningen med trädgård, 21 lägenheter på första och andra våningen och 3 takvåningar.')
a('Prices and areas are transcribed from the developer’s price list, which shows the 27 homes',
  'Los precios y las superficies están transcritos de la lista de precios del promotor, que muestra las 27 viviendas como disponibles y no lleva fecha; la consultamos en octubre de 2026. La lista indica que los precios no incluyen el IVA. La superficie construida incluye una parte de las zonas comunes; las terrazas son la terraza cubierta y la descubierta tal como las da la lista, y las viviendas de planta baja tienen en su lugar un porche y un jardín. La lista muestra una plaza de garaje y un trastero para cada vivienda. En 11 de las viviendas, los planos, de abril y diciembre de 2025, dan superficies ligeramente distintas de las de la lista: entre 0.03 y 0.41 {U} de superficie interior y entre 0.01 y 0.12 {U} construidos, salvo las dos viviendas de un dormitorio 6A1-P01-B y 6A1-P02-B, donde los planos dan 47.02 {U} interiores y 65.52 {U} construidos frente a 46.00 y 65.26 en la lista. Los planos dan además una superficie útil exterior para cada vivienda que no es la misma medida que las terrazas de la lista. La página usa las cifras de la lista. El anuncio del promotor da la entrega para mayo de 2028.',
  'Les prix et les surfaces sont transcrits de la liste de prix du promoteur, qui présente les 27 logements comme disponibles et ne porte pas de date ; nous l’avons consultée en octobre 2026. La liste indique que les prix s’entendent hors TVA. La surface construite inclut une part des parties communes ; les terrasses sont la terrasse couverte et la terrasse découverte telles que la liste les donne, et les logements en rez-de-chaussée ont à la place un porche et un jardin. La liste indique une place de parking et un débarras pour chaque logement. Pour 11 des logements, les plans, d’avril et de décembre 2025, donnent des surfaces légèrement différentes de celles de la liste : de 0.03 à 0.41 {U} de surface intérieure et de 0.01 à 0.12 {U} construits, sauf pour les deux logements d’une chambre 6A1-P01-B et 6A1-P02-B, où les plans donnent 47.02 {U} intérieurs et 65.52 {U} construits contre 46.00 et 65.26 sur la liste. Les plans donnent en outre, pour chaque logement, une surface utile extérieure qui n’est pas la même mesure que les terrasses de la liste. La page reprend les chiffres de la liste. L’annonce du promoteur indique une livraison en mai 2028.',
  'Preise und Flächen sind der Preisliste des Bauträgers entnommen, die die 27 Wohnungen als verfügbar zeigt und kein Datum trägt; wir haben sie im Oktober 2026 geprüft. Die Liste nennt die Preise zuzüglich MwSt. Die bebaute Fläche schließt einen Anteil der Gemeinschaftsflächen ein; die Terrassen sind die überdachte und die offene Terrasse, wie die Liste sie angibt, und die Erdgeschosswohnungen haben stattdessen eine Veranda und einen Garten. Die Liste zeigt für jede Wohnung einen Garagenstellplatz und einen Abstellraum. Bei 11 Wohnungen geben die Grundrisse vom April und Dezember 2025 leicht andere Flächen an als die Liste: 0.03 bis 0.41 {U} Innenfläche und 0.01 bis 0.12 {U} bebaut, außer bei den beiden Einzimmerwohnungen mit einem Schlafzimmer 6A1-P01-B und 6A1-P02-B, wo die Grundrisse 47.02 {U} innen und 65.52 {U} bebaut angeben gegenüber 46.00 und 65.26 in der Liste. Die Grundrisse nennen außerdem für jede Wohnung eine nutzbare Außenfläche, die nicht dasselbe Maß ist wie die Terrassen der Liste. Die Seite verwendet die Werte der Liste. Laut Bauträger ist die Übergabe für Mai 2028 angegeben.',
  'Цены и площади перенесены из прайс-листа застройщика, в котором все 27 квартир показаны как доступные и который не датирован; мы проверили его в октябре 2026 года. В списке указано, что цены не включают НДС. Застроенная площадь включает долю общих зон; террасы — это крытая и открытая терраса в том виде, как их даёт список, а у квартир на первом этаже вместо них веранда и сад. В списке для каждой квартиры указаны одно место в гараже и одна кладовая. У 11 квартир планировки от апреля и декабря 2025 года дают чуть иные площади, чем список: на 0.03–0.41 {U} внутренней площади и на 0.01–0.12 {U} застроенной, кроме двух квартир с одной спальней, 6A1-P01-B и 6A1-P02-B, где на планах 47.02 {U} внутри и 65.52 {U} застроенной площади против 46.00 и 65.26 в списке. Кроме того, на планах для каждой квартиры дана полезная внешняя площадь, которая не совпадает по способу измерения с террасами из списка. На странице используются цифры списка. По данным застройщика, сдача указана на май 2028 года.',
  'الأسعار والمساحات منقولة من قائمة أسعار المطوّر التي تُظهر المساكن السبعة والعشرين على أنها متاحة ولا تحمل تاريخًا؛ راجعناها في أكتوبر 2026. تذكر القائمة أن الأسعار لا تشمل ضريبة القيمة المضافة. المساحة المبنية تشمل حصة من المناطق المشتركة؛ والتراسات هي التراس المسقوف والمكشوف كما تعرضها القائمة، وللمساكن في الطابق الأرضي رواق وحديقة بدلًا منها. تُظهر القائمة موقفًا في المرآب ومخزنًا لكل مسكن. وفي 11 مسكنًا تعطي المخططات، المؤرخة في أبريل وديسمبر 2025، مساحات تختلف قليلًا عن القائمة: من 0.03 إلى 0.41 {U} مساحة داخلية ومن 0.01 إلى 0.12 {U} مبنية، باستثناء المسكنين ذوي غرفة النوم الواحدة 6A1-P01-B و6A1-P02-B، إذ تذكر المخططات 47.02 {U} داخلية و65.52 {U} مبنية مقابل 46.00 و65.26 في القائمة. كما تذكر المخططات لكل مسكن مساحة خارجية صالحة للاستعمال لا تقاس بالطريقة نفسها التي تقاس بها تراسات القائمة. تعتمد الصفحة أرقام القائمة. يذكر المطوّر أن التسليم في مايو 2028.',
  'Prijzen en oppervlakten zijn overgenomen uit de prijslijst van de ontwikkelaar, die de 27 woningen als beschikbaar toont en geen datum draagt; we hebben die in oktober 2026 gecontroleerd. De lijst vermeldt dat de prijzen exclusief btw zijn. De bebouwde oppervlakte omvat een aandeel in de gemeenschappelijke delen; de terrassen zijn het overdekte en het open terras zoals de lijst ze geeft, en de woningen op de begane grond hebben in plaats daarvan een veranda en een tuin. De lijst toont voor elke woning een garageplaats en een berging. Bij 11 woningen geven de plattegronden van april en december 2025 iets andere oppervlakten dan de lijst: 0.03 tot 0.41 {U} binnenoppervlakte en 0.01 tot 0.12 {U} bebouwd, behalve bij de twee woningen met één slaapkamer 6A1-P01-B en 6A1-P02-B, waar de plattegronden 47.02 {U} binnen en 65.52 {U} bebouwd geven tegenover 46.00 en 65.26 op de lijst. De plattegronden geven bovendien voor elke woning een bruikbare buitenoppervlakte die niet dezelfde maat is als de terrassen van de lijst. De pagina gebruikt de cijfers van de lijst. Volgens de ontwikkelaar is de oplevering gepland voor mei 2028.',
  'Ceny i powierzchnie zostały przepisane z cennika dewelopera, który pokazuje 27 lokali jako dostępne i nie nosi daty; sprawdziliśmy go w październiku 2026 r. Cennik podaje, że ceny nie obejmują VAT. Powierzchnia zabudowy obejmuje udział w częściach wspólnych; tarasy to taras zadaszony i odkryty, tak jak podaje cennik, a lokale na parterze mają w ich miejsce werandę i ogród. Cennik wykazuje dla każdego lokalu jedno miejsce w garażu i jedną komórkę. W 11 lokalach rzuty z kwietnia i grudnia 2025 r. podają nieco inne powierzchnie niż cennik: od 0.03 do 0.41 {U} powierzchni wnętrza i od 0.01 do 0.12 {U} zabudowy, z wyjątkiem dwóch lokali z jedną sypialnią, 6A1-P01-B i 6A1-P02-B, gdzie rzuty podają 47.02 {U} wnętrza i 65.52 {U} zabudowy wobec 46.00 i 65.26 w cenniku. Rzuty podają też dla każdego lokalu użytkową powierzchnię zewnętrzną, która nie jest tą samą miarą co tarasy z cennika. Strona używa danych z cennika. Deweloper podaje termin oddania na maj 2028 r.',
  'Prisene og arealene er skrevet av fra utbyggerens prisliste, som viser de 27 boligene som tilgjengelige og ikke har dato; vi kontrollerte den i oktober 2026. Listen oppgir at prisene er eksklusive mva. Det bebygde arealet inkluderer en andel av fellesarealene; terrassene er den overbygde og den åpne terrassen slik listen oppgir dem, og boligene i første etasje har veranda og hage i stedet. Listen viser en garasjeplass og en bod for hver bolig. For 11 av boligene gir plantegningene, fra april og desember 2025, litt andre arealer enn listen: 0.03 til 0.41 {U} innvendig areal og 0.01 til 0.12 {U} bygd, bortsett fra de to boligene med ett soverom, 6A1-P01-B og 6A1-P02-B, der plantegningene oppgir 47.02 {U} innvendig og 65.52 {U} bygd mot 46.00 og 65.26 på listen. Plantegningene oppgir dessuten et nyttbart utvendig areal for hver bolig som ikke er samme mål som terrassene på listen. Siden bruker tallene fra listen. Utbyggeren oppgir levering i mai 2028.',
  'Priser och ytor är avskrivna från exploatörens prislista, som visar de 27 bostäderna som tillgängliga och saknar datum; vi kontrollerade den i oktober 2026. Listan anger att priserna är exklusive moms. Byggytan inkluderar en andel av de gemensamma ytorna; terrasserna är den övertäckta och den öppna terrassen så som listan anger dem, och bostäderna i bottenvåningen har i stället en veranda och en trädgård. Listan visar en garageplats och ett förråd för varje bostad. För 11 av bostäderna ger ritningarna, från april och december 2025, något andra ytor än listan: 0.03 till 0.41 {U} inomhusyta och 0.01 till 0.12 {U} byggyta, utom för de två bostäderna med ett sovrum, 6A1-P01-B och 6A1-P02-B, där ritningarna anger 47.02 {U} inomhus och 65.52 {U} byggyta mot 46.00 och 65.26 på listan. Ritningarna anger dessutom en användbar utomhusyta för varje bostad som inte är samma mått som terrasserna på listan. Sidan använder listans siffror. Exploatören anger leverans i maj 2028.')

# timeline, viewing, enquiry
a('The floorplans of the homes that interest you and the price list.',
  'Los planos de las viviendas que le interesen y la lista de precios.',
  'Les plans des logements qui vous intéressent et la liste de prix.',
  'Die Grundrisse der Wohnungen, die Sie interessieren, und die Preisliste.',
  'Планировки интересующих вас квартир и прайс-лист.',
  'مخططات المساكن التي تهمّك وقائمة الأسعار.',
  'De plattegronden van de woningen die u interesseren en de prijslijst.',
  'Rzuty interesujących Państwa lokali i cennik.',
  'Plantegningene av boligene De er interessert i, og prislisten.',
  'Planritningarna för de bostäder som intresserar er och prislistan.')
a('There is no reservation payment: the first payment',
  'No hay pago de reserva: el primer pago, del 30% (20% para residentes en España) más IVA, se hace al firmar el contrato privado de compraventa.',
  'Il n’y a pas de versement de réservation : le premier paiement, de 30 % (20 % pour les résidents en Espagne) hors TVA, se fait à la signature du contrat de vente privé.',
  'Es gibt keine Reservierungszahlung: Die erste Zahlung von 30 % (20 % für Käufer mit Wohnsitz in Spanien) zuzüglich MwSt. erfolgt bei Unterzeichnung des privaten Kaufvertrags.',
  'Платежа за бронирование нет: первый платёж — 30 % (20 % для проживающих в Испании) плюс НДС — вносится при подписании предварительного договора купли-продажи.',
  'لا توجد دفعة حجز: تُسدَّد الدفعة الأولى، 30% (20% للمقيمين في إسبانيا) زائد ضريبة القيمة المضافة، عند توقيع عقد الشراء الخاص.',
  'Er is geen reserveringsbetaling: de eerste betaling van 30% (20% voor kopers die in Spanje wonen) plus btw volgt bij ondertekening van de onderhandse koopovereenkomst.',
  'Nie ma opłaty rezerwacyjnej: pierwsza wpłata, 30% (20% dla rezydentów Hiszpanii) plus VAT, następuje przy podpisaniu umowy przedwstępnej.',
  'Det er ingen reservasjonsbetaling: den første betalingen, 30 % (20 % for kjøpere bosatt i Spania) pluss mva., skjer ved signering av den private kjøpekontrakten.',
  'Det finns ingen bokningsbetalning: den första betalningen, 30 % (20 % för köpare bosatta i Spanien) plus moms, görs när det privata köpeavtalet undertecknas.')
a('The development is shown only in computer-generated views',
  'La promoción solo se muestra en imágenes generadas por ordenador, por lo que una visita trata de la ubicación, los planos y el avance de las obras.',
  'Le programme n’est montré qu’en images de synthèse ; une visite porte donc sur l’emplacement, les plans et l’avancement des travaux.',
  'Die Anlage ist nur in computergenerierten Ansichten zu sehen, daher geht es bei einem Besuch um die Lage, die Grundrisse und den Baufortschritt.',
  'Комплекс показан только на компьютерных визуализациях, поэтому визит — это знакомство с расположением, планировками и ходом работ.',
  'يُعرض المشروع في صور مُنشأة بالحاسوب فقط، لذلك تتناول الزيارة الموقع والمخططات وتقدّم الأعمال.',
  'Het project wordt alleen in computergegenereerde beelden getoond, dus een bezoek gaat over de ligging, de plattegronden en de voortgang van de werken.',
  'Inwestycja jest pokazana wyłącznie na wizualizacjach komputerowych, dlatego wizyta dotyczy lokalizacji, rzutów i postępu prac.',
  'Prosjektet vises bare i datagenererte bilder, så en visning handler om beliggenheten, plantegningene og fremdriften på byggingen.',
  'Projektet visas bara i datorgenererade bilder, så ett besök handlar om läget, ritningarna och hur arbetet fortskrider.')
a('Stand on the site and see the views towards the bay and the golf course.',
  'Pise el terreno y vea las vistas hacia la bahía y el campo de golf.',
  'Parcourez le terrain et voyez la vue vers la baie et le golf.',
  'Stehen Sie auf dem Grundstück und sehen Sie den Blick zur Bucht und zum Golfplatz.',
  'Побывайте на участке и посмотрите на вид в сторону залива и поля для гольфа.',
  'قف في الموقع وشاهد الإطلالات نحو الخليج وملعب الغولف.',
  'Sta op het terrein en zie het uitzicht naar de baai en de golfbaan.',
  'Stań na działce i zobacz widok w stronę zatoki i pola golfowego.',
  'Stå på tomten og se utsikten mot bukten og golfbanen.',
  'Stå på tomten och se utsikten mot bukten och golfbanan.')
a('See the <em>site and the area</em>',
  'Conozca <em>el terreno y la zona</em>', 'Découvrez <em>le terrain et le quartier</em>', 'Erleben Sie <em>Grundstück und Umgebung</em>',
  'Посмотрите <em>участок и район</em>', 'شاهد <em>الموقع والمنطقة</em>', 'Zie <em>het terrein en de omgeving</em>',
  'Zobacz <em>działkę i okolicę</em>', 'Se <em>tomten og området</em>', 'Se <em>tomten och området</em>')
a('Ask about <em>Granado Homes</em>',
  'Pregunte por <em>Granado Homes</em>', 'Renseignez-vous sur <em>Granado Homes</em>', 'Fragen Sie nach <em>Granado Homes</em>',
  'Узнайте о <em>Granado Homes</em>', 'اسأل عن <em>Granado Homes</em>', 'Vraag naar <em>Granado Homes</em>',
  'Zapytaj o <em>Granado Homes</em>', 'Spør om <em>Granado Homes</em>', 'Fråga om <em>Granado Homes</em>')
a('Hello Nueva Living, I would like information about Granado Homes.',
  'Hola Nueva Living, me gustaría recibir información sobre Granado Homes.',
  'Bonjour Nueva Living, je souhaiterais des informations sur Granado Homes.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Granado Homes.',
  'Здравствуйте, Nueva Living, я хотел(а) бы получить информацию о Granado Homes.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Granado Homes.',
  'Hallo Nueva Living, ik wil graag informatie over Granado Homes.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Granado Homes.',
  'Hej Nueva Living, jag vill gärna ha information om Granado Homes.',
  'Hej Nueva Living, jag vill gärna ha information om Granado Homes.')

# faq
a('The development has 144 homes and 27 are listed with a price',
  'La promoción tiene 144 viviendas y 27 figuran con precio: 3 viviendas en planta baja con jardín, 21 apartamentos en la primera y la segunda planta y 3 áticos, de uno a tres dormitorios, de {E321000} a {E558000} más IVA.',
  'Le programme compte 144 logements et 27 sont proposés avec un prix : 3 logements en rez-de-chaussée avec jardin, 21 appartements au premier et au deuxième étage et 3 penthouses, d’une à trois chambres, de {E321000} à {E558000} hors TVA.',
  'Die Anlage hat 144 Wohnungen, 27 davon sind mit Preis gelistet: 3 Erdgeschosswohnungen mit Garten, 21 Wohnungen im ersten und zweiten Obergeschoss und 3 Penthäuser, mit einem bis drei Schlafzimmern, von {E321000} bis {E558000} zuzüglich MwSt.',
  'В комплексе 144 квартиры, 27 из них указаны с ценой: 3 квартиры на первом этаже с садом, 21 квартира на втором и третьем этажах и 3 пентхауса, с одной–тремя спальнями, от {E321000} до {E558000} без НДС.',
  'يضم المشروع 144 مسكنًا، منها 27 بأسعارها: 3 مساكن في الطابق الأرضي مع حديقة و21 شقة في الطابقين الأول والثاني و3 بنتهاوس، من غرفة نوم واحدة إلى ثلاث غرف نوم، من {E321000} إلى {E558000} دون ضريبة القيمة المضافة.',
  'Het project telt 144 woningen, waarvan er 27 met prijs worden aangeboden: 3 woningen op de begane grond met tuin, 21 appartementen op de eerste en tweede verdieping en 3 penthouses, met één tot drie slaapkamers, van {E321000} tot {E558000} excl. btw.',
  'Inwestycja liczy 144 lokale, z czego 27 ma podaną cenę: 3 lokale na parterze z ogrodem, 21 mieszkań na pierwszym i drugim piętrze oraz 3 penthouse’y, z jedną do trzech sypialni, od {E321000} do {E558000} plus VAT.',
  'Prosjektet har 144 boliger, og 27 er oppført med pris: 3 boliger i første etasje med hage, 21 leiligheter i andre og tredje etasje og 3 toppleiligheter, med ett til tre soverom, fra {E321000} til {E558000} pluss mva.',
  'Projektet har 144 bostäder, och 27 är listade med pris: 3 bostäder i bottenvåningen med trädgård, 21 lägenheter på första och andra våningen och 3 takvåningar, med ett till tre sovrum, från {E321000} till {E558000} plus moms.')
a('No. The price list states that prices do not include VAT, which on a new home',
  'No. La lista de precios indica que los precios no incluyen el IVA, que en una vivienda nueva en España suele ser del 10%; la lista no indica el tipo. Confirmamos por escrito los impuestos y los gastos de compra.',
  'Non. La liste de prix indique que les prix n’incluent pas la TVA, qui s’élève normalement à 10 % pour un logement neuf en Espagne ; la liste n’indique pas le taux. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Laut Preisliste verstehen sich die Preise zuzüglich MwSt., die bei einer neuen Wohnung in Spanien normalerweise 10 % beträgt; die Liste nennt den Satz nicht. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе сказано, что цены не включают НДС, который при покупке нового жилья в Испании обычно составляет 10 %; ставка в списке не названа. Налоги и расходы на покупку мы письменно подтверждаем.',
  'لا. تذكر قائمة الأسعار أن الأسعار لا تشمل ضريبة القيمة المضافة، وهي في المسكن الجديد في إسبانيا 10% عادةً، ولا تذكر القائمة النسبة. ونؤكد الضرائب ومصاريف الشراء كتابةً.',
  'Nee. De prijslijst vermeldt dat de prijzen exclusief btw zijn, dat bij een nieuwe woning in Spanje normaal 10% bedraagt; de lijst vermeldt het tarief niet. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Nie. Cennik podaje, że ceny nie zawierają VAT, który przy nowym lokalu w Hiszpanii wynosi zwykle 10%; cennik nie podaje stawki. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Prislisten oppgir at prisene ikke inkluderer mva., som for en ny bolig i Spania vanligvis er 10 %; listen oppgir ikke satsen. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Nej. Prislistan anger att priserna inte inkluderar moms, som för en ny bostad i Spanien normalt är 10 %; listan anger inte satsen. Vi bekräftar skatter och köpkostnader skriftligen.')
a('Yes. The price list shows a garage space and a storage room',
  'Sí. La lista de precios muestra una plaza de garaje y un trastero para cada vivienda a la venta, y el anuncio del promotor dice que garaje y trastero están incluidos en el precio.',
  'Oui. La liste de prix indique une place de parking et un débarras pour chaque logement proposé, et l’annonce du promoteur précise que le parking et le débarras sont compris dans le prix.',
  'Ja. Die Preisliste zeigt für jede angebotene Wohnung einen Garagenstellplatz und einen Abstellraum, und laut Bauträger sind Garage und Abstellraum im Preis enthalten.',
  'Да. В прайс-листе для каждой предлагаемой квартиры указаны место в гараже и кладовая, а в объявлении застройщика сказано, что гараж и кладовая входят в цену.',
  'نعم. تُظهر قائمة الأسعار موقفًا في المرآب ومخزنًا لكل مسكن معروض، ويذكر المطوّر أن المرآب والمخزن مشمولان في السعر.',
  'Ja. De prijslijst toont voor elke aangeboden woning een garageplaats en een berging, en volgens de ontwikkelaar zijn garage en berging in de prijs inbegrepen.',
  'Tak. Cennik wykazuje dla każdego oferowanego lokalu miejsce w garażu i komórkę, a deweloper podaje, że garaż i komórka są w cenie.',
  'Ja. Prislisten viser en garasjeplass og en bod for hver bolig som er oppført, og utbyggeren oppgir at garasje og bod er inkludert i prisen.',
  'Ja. Prislistan visar en garageplats och ett förråd för varje listad bostad, och exploatören anger att garage och förråd ingår i priset.')
a('The developer’s listing gives delivery as May 2028 and no other document states a date, so we ask for the contractual date and the licence status.',
  'El anuncio del promotor da la entrega para mayo de 2028 y ningún otro documento indica una fecha, por lo que pedimos la fecha contractual y el estado de la licencia.',
  'L’annonce du promoteur indique une livraison en mai 2028 et aucun autre document ne mentionne de date ; nous demandons donc la date contractuelle et l’état du permis.',
  'Der Bauträger gibt die Übergabe für Mai 2028 an, und kein anderes Dokument nennt ein Datum, daher fragen wir das vertragliche Datum und den Stand der Genehmigung an.',
  'Застройщик указывает сдачу на май 2028 года, и ни в одном другом документе даты нет, поэтому мы запрашиваем договорную дату и статус разрешения.',
  'يذكر المطوّر أن التسليم في مايو 2028، ولا تذكر أي وثيقة أخرى تاريخًا، لذلك نطلب التاريخ التعاقدي وحالة الرخصة.',
  'De ontwikkelaar noemt mei 2028 als oplevering en geen enkel ander document noemt een datum, dus vragen we naar de contractuele datum en de stand van de vergunning.',
  'Deweloper podaje termin oddania na maj 2028 r., a żaden inny dokument nie wskazuje daty, dlatego prosimy o termin wskazany w umowie i status pozwolenia.',
  'Utbyggeren oppgir levering i mai 2028, og ingen andre dokumenter oppgir en dato, så vi ber om den kontraktsfestede datoen og status for tillatelsen.',
  'Exploatören anger leverans i maj 2028, och inga andra handlingar anger ett datum, så vi ber om det avtalade datumet och bygglovets status.')
a('There is no reservation payment. Buyers who are not resident',
  'No hay pago de reserva. Los compradores no residentes en España pagan el 30% más IVA al firmar el contrato privado y el 70% más IVA ante notario; los residentes en España pagan el 20% más IVA y después el 80% más IVA.',
  'Il n’y a pas de versement de réservation. Les acheteurs non résidents en Espagne paient 30 % hors TVA à la signature du contrat privé et 70 % hors TVA chez le notaire ; les résidents en Espagne paient 20 % hors TVA, puis 80 % hors TVA.',
  'Es gibt keine Reservierungszahlung. Käufer ohne Wohnsitz in Spanien zahlen 30 % zuzüglich MwSt. bei Unterzeichnung des privaten Vertrags und 70 % zuzüglich MwSt. beim Notar; Käufer mit Wohnsitz in Spanien zahlen 20 % zuzüglich MwSt., danach 80 % zuzüglich MwSt.',
  'Платежа за бронирование нет. Покупатели, не проживающие в Испании, платят 30 % плюс НДС при подписании предварительного договора и 70 % плюс НДС у нотариуса; проживающие в Испании платят 20 % плюс НДС, затем 80 % плюс НДС.',
  'لا توجد دفعة حجز. يدفع المشترون غير المقيمين في إسبانيا 30% زائد ضريبة القيمة المضافة عند توقيع العقد الخاص و70% زائد الضريبة أمام كاتب العدل؛ ويدفع المقيمون في إسبانيا 20% زائد الضريبة، ثم 80% زائد الضريبة.',
  'Er is geen reserveringsbetaling. Kopers die niet in Spanje wonen betalen 30% plus btw bij ondertekening van het onderhandse contract en 70% plus btw bij de notaris; kopers die in Spanje wonen betalen 20% plus btw, daarna 80% plus btw.',
  'Nie ma opłaty rezerwacyjnej. Kupujący niebędący rezydentami Hiszpanii płacą 30% plus VAT przy podpisaniu umowy przedwstępnej i 70% plus VAT u notariusza; rezydenci Hiszpanii płacą 20% plus VAT, a następnie 80% plus VAT.',
  'Det er ingen reservasjonsbetaling. Kjøpere som ikke er bosatt i Spania betaler 30 % pluss mva. ved signering av den private kontrakten og 70 % pluss mva. hos notarius; kjøpere bosatt i Spania betaler 20 % pluss mva., deretter 80 % pluss mva.',
  'Det finns ingen bokningsbetalning. Köpare som inte är bosatta i Spanien betalar 30 % plus moms vid undertecknandet av det privata avtalet och 70 % plus moms hos notarien; köpare bosatta i Spanien betalar 20 % plus moms, därefter 80 % plus moms.')

# ------------------------------------------------------------ report what is still missing
missing = [t for t in todo if t not in T and not re.fullmatch(r'Block \d[AB], portal \d, (?:Ground floor|First floor|Second floor|Penthouse)', t)]
json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
print('skipped (already in memory):', SKIPPED)
print('translated', len(T), 'still missing', len(missing))
for t in missing: print('  MISSING', repr(t[:120]))
