# -*- coding: utf-8 -*-
"""Valle Romano Crest Villas (Valle Romano golf, Estepona): the strings the translation memory did not have.

Same shape as k_golfside_hill_residences.py: a(i, hint, es, fr, de, ru, ar, nl, pl, no, sv). The row is
found by hint, the start of the English string, which must match exactly one string in todo.json; i is
the index scaffold.py printed when the row was written and is kept only as a reading aid. Tokens expand
per language:  {E1295000} money,  {N28.42} a figure with the locale's decimal mark,  {G1002} a whole
number with the locale's thousands separator,  {U} the area unit (m2, ru м², ar م²),  {P20} a percentage
in the locale's spacing,  {Q} the expected completion quarter in the locale's own form (T4 / Q4 / K4 /
4 кв. / IV kw. / الربع الرابع).

The unit size rows are built by size() from the same numbers as the English, with the SIZE_LABELS words
of scripts/build_property_pages.mjs for one word per measure. The availability floor labels are left to
assemble.py, which writes them from FLOOR_PARTS.

Source conflicts are carried into every language as in the English: four bedrooms and four bathrooms on
the price list and the plan sheets' summary, three bedrooms, a dressing room and three bathrooms in the
room schedules of the Villa 1 and 2 floor plans; and the price list states no VAT treatment.

    python3 tools/import/k_valle_romano_crest_villas.py <workdir>
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}
UNIT['ru'] = 'м²'
UNIT['ar'] = 'م²'
# The quarter forms other projects already publish for Q4 2028 (mijas-palm-residences, biubay).
QUARTER = {'es': 'T4 2028', 'fr': 'T4 2028', 'de': 'Q4 2028', 'ru': '4 кв. 2028', 'ar': 'الربع الرابع 2028',
           'nl': 'K4 2028', 'pl': 'IV kw. 2028', 'no': 'K4 2028', 'sv': 'K4 2028'}
# Percent spacing as valle-romano-hilltop-villas writes it in each overlay.
PCT_SPACE = {'es': '', 'fr': ' ', 'de': ' ', 'ru': '', 'ar': '', 'nl': '', 'pl': '', 'no': ' ', 'sv': ' '}
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    text = re.sub(r'\{G(\d+)\}', lambda m: f'{int(m.group(1)):,}'.replace(',', GROUP[l]), text)
    text = re.sub(r'\{P(\d+)\}', lambda m: f'{m.group(1)}{PCT_SPACE[l]}%', text)
    return text.replace('{U}', UNIT[l]).replace('{Q}', QUARTER[l])


def find(hint):
    if hint in todo:
        return hint
    hits = [s for s in todo if s.startswith(hint)]
    assert len(hits) == 1, (hint, len(hits))
    return hits[0]


def a(i, hint, *tr):
    en = find(hint)
    assert len(tr) == 9, (i, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def override(en, *tr):
    """A string the translation memory already has, overridden for this project only."""
    assert len(tr) == 9, en
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    assert en in todo, en
    T[en] = {l: en for l in LOCS}


# ---------------------------------------------------------------- unit sizes
W = {   # total built, interior, terraces, plot -- the SIZE_LABELS words, terraces in the plural
    'es': ('construido total', 'interior', 'terrazas', 'parcela'),
    'fr': ('construit total', 'intérieur', 'terrasses', 'parcelle'),
    'de': ('bebaut gesamt', 'Innenfläche', 'Terrassen', 'Grundstück'),
    'ru': ('общая застройка', 'внутренняя площадь', 'террасы', 'участок'),
    'ar': ('إجمالي المبني', 'مساحة داخلية', 'تراسات', 'قطعة أرض'),
    'nl': ('totaal bebouwd', 'binnenoppervlak', 'terrassen', 'perceel'),
    'pl': ('całkowita powierzchnia zabudowy', 'powierzchnia wewnętrzna', 'tarasy', 'działka'),
    'no': ('totalt bebygd', 'innvendig areal', 'terrasser', 'tomt'),
    'sv': ('total byggyta', 'inneryta', 'terrasser', 'tomt'),
}


def size(total, interior, terr, plot):
    en = find(f'{total} sqm total built, {interior} sqm interior, {terr} sqm terraces, ')
    out = {}
    for l in LOCS:
        tb, it, te, pl = W[l]
        p = f'{int(plot):,}'.replace(',', GROUP[l])
        sep = '، ' if l == 'ar' else ', '   # Arabic writes its comma as U+060C
        out[l] = sep.join([f'{total} {UNIT[l]} {tb}', f'{interior} {UNIT[l]} {it}', f'{terr} {UNIT[l]} {te}', f'{p} {UNIT[l]} {pl}'])
    T[en] = out


size('279', '122', '89', '400')
size('281', '124', '86', '411')
size('370', '182', '128', '555')
size('358', '183', '112', '560')
size('348', '182', '103', '554')
size('328', '167', '108', '533')
size('327', '176', '91', '533')
size('604', '433', '100', '1002')

for en in ('Valle Romano Crest Villas', 'Valle Romano Crest', 'Valle Romano <em>Crest Villas</em>'):
    same(en)

# ---------------------------------------------------------------- top of page
a(3, 'Eight detached villas in three types inside the Valle Romano golf resort in Estepona, sold',
  'Ocho villas independientes de tres tipologías dentro del resort de golf de Valle Romano, en Estepona, a la venta sobre plano: de 122 a 433 {U} interiores en parcelas de 400 a {G1002} {U}, cada una proyectada con piscina privada de borde infinito, y con la finalización prevista para el {Q}.',
  'Huit villas indépendantes de trois types au sein du domaine de golf de Valle Romano, à Estepona, vendues sur plan : de 122 à 433 {U} intérieurs sur des parcelles de 400 à {G1002} {U}, chacune dessinée avec une piscine privée à débordement, pour un achèvement prévu au {Q}.',
  'Acht freistehende Villen in drei Typen im Golfresort Valle Romano in Estepona, Verkauf Off-Plan: 122 bis 433 {U} Innenfläche auf Grundstücken von 400 bis {G1002} {U}, jede mit eigenem Infinity-Pool geplant, die Fertigstellung ist für {Q} vorgesehen.',
  'Восемь отдельных вилл трёх типов на территории гольф-курорта Валле-Романо в Эстепоне, продажа на стадии проекта: от 122 до 433 {U} внутренней площади на участках от 400 до {G1002} {U}, у каждой по проекту собственный бассейн-инфинити; завершение ожидается в {Q}.',
  'ثماني فلل مستقلة من ثلاثة أنماط داخل منتجع غولف فايي رومانو في إستيبونا، تُباع على المخطط: من 122 إلى 433 {U} من المساحة الداخلية على قطع أرض من 400 إلى {G1002} {U}، ولكل منها في المخططات مسبح خاص بحافة لا متناهية، ويُتوقع الإنجاز في {Q}.',
  'Acht vrijstaande villa’s in drie types binnen het golfresort Valle Romano in Estepona, verkocht op plan: 122 tot 433 {U} binnenoppervlak op percelen van 400 tot {G1002} {U}, elk getekend met een eigen infinityzwembad, met de oplevering verwacht in {Q}.',
  'Osiem wolnostojących willi w trzech typach na terenie kurortu golfowego Valle Romano w Esteponie, w sprzedaży z planu: od 122 do 433 {U} powierzchni wewnętrznej na działkach od 400 do {G1002} {U}, każda z prywatnym basenem typu infinity w projekcie; zakończenie przewidziane na {Q}.',
  'Åtte frittstående villaer i tre typer inne på golfanlegget Valle Romano i Estepona, solgt på tegning: 122 til 433 {U} innvendig på tomter på 400 til {G1002} {U}, hver tegnet med eget infinitybasseng, og ferdigstillelse ventet i {Q}.',
  'Åtta fristående villor i tre typer inne på golfanläggningen Valle Romano i Estepona, till salu på ritning: 122 till 433 {U} inneryta på tomter om 400 till {G1002} {U}, var och en ritad med egen infinitypool, och färdigställande väntas {Q}.')
a(4, 'Eight off-plan detached villas at Valle Romano golf',
  'Ocho villas independientes sobre plano en el golf de Valle Romano, Estepona: de 279 a 604 {U} construidos en parcelas de 400 a {G1002} {U}, piscinas de borde infinito. Desde {E1295000}.',
  'Huit villas indépendantes sur plan au golf de Valle Romano, Estepona : 279 à 604 {U} construits sur des parcelles de 400 à {G1002} {U}, piscines à débordement. Dès {E1295000}.',
  'Acht freistehende Off-Plan-Villen am Golfplatz Valle Romano, Estepona: 279 bis 604 {U} bebaut auf Grundstücken von 400 bis {G1002} {U}, Infinity-Pools. Ab {E1295000}.',
  'Восемь отдельных вилл на стадии проекта у гольф-поля Валле-Романо, Эстепона: от 279 до 604 {U} застройки на участках от 400 до {G1002} {U}, бассейны-инфинити. От {E1295000}.',
  'ثماني فلل مستقلة على المخطط في غولف فايي رومانو، إستيبونا: من 279 إلى 604 {U} مبنية على قطع أرض من 400 إلى {G1002} {U}، ومسابح بحافة لا متناهية. ابتداءً من {E1295000}.',
  'Acht vrijstaande villa’s op plan bij golf Valle Romano, Estepona: 279 tot 604 {U} bebouwd op percelen van 400 tot {G1002} {U}, infinityzwembaden. Vanaf {E1295000}.',
  'Osiem wolnostojących willi z planu przy polu golfowym Valle Romano, Estepona: od 279 do 604 {U} zabudowy na działkach od 400 do {G1002} {U}, baseny typu infinity. Od {E1295000}.',
  'Åtte frittstående villaer på tegning ved Valle Romano golf, Estepona: 279 til 604 {U} bebygd på tomter på 400 til {G1002} {U}, infinitybasseng. Fra {E1295000}.',
  'Åtta fristående villor på ritning vid Valle Romano golf, Estepona: 279 till 604 {U} byggyta på tomter om 400 till {G1002} {U}, infinitypooler. Från {E1295000}.')
a(5, 'Eight detached villas with infinity-edge pools at Valle Romano golf',
  'Ocho villas independientes con piscina de borde infinito en el golf de Valle Romano, en Estepona, sobre plano, desde {E1295000}.',
  'Huit villas indépendantes avec piscine à débordement au golf de Valle Romano, à Estepona, sur plan, dès {E1295000}.',
  'Acht freistehende Villen mit Infinity-Pool am Golfplatz Valle Romano in Estepona, Off-Plan, ab {E1295000}.',
  'Восемь отдельных вилл с бассейнами-инфинити у гольф-поля Валле-Романо в Эстепоне, на стадии проекта, от {E1295000}.',
  'ثماني فلل مستقلة بمسابح ذات حافة لا متناهية في غولف فايي رومانو بإستيبونا، على المخطط، ابتداءً من {E1295000}.',
  'Acht vrijstaande villa’s met infinityzwembad bij golf Valle Romano in Estepona, op plan, vanaf {E1295000}.',
  'Osiem wolnostojących willi z basenami typu infinity przy polu golfowym Valle Romano w Esteponie, z planu, od {E1295000}.',
  'Åtte frittstående villaer med infinitybasseng ved Valle Romano golf i Estepona, på tegning, fra {E1295000}.',
  'Åtta fristående villor med infinitypool vid Valle Romano golf i Estepona, på ritning, från {E1295000}.')
a(6, 'Eight villas / off-plan',
  'Ocho villas / sobre plano', 'Huit villas / sur plan', 'Acht Villen / Off-Plan', 'Восемь вилл / на стадии проекта',
  'ثماني فلل / على المخطط', 'Acht villa’s / op plan', 'Osiem willi / z planu', 'Åtte villaer / på tegning', 'Åtta villor / på ritning')
a(7, 'Eight detached villas in three types inside the Valle Romano golf resort, each',
  'Ocho villas independientes de tres tipologías dentro del resort de golf de Valle Romano, cada una con piscina privada de borde infinito, a la venta sobre plano.',
  'Huit villas indépendantes de trois types au sein du domaine de golf de Valle Romano, chacune avec sa piscine privée à débordement, vendues sur plan.',
  'Acht freistehende Villen in drei Typen im Golfresort Valle Romano, jede mit eigenem Infinity-Pool, Verkauf Off-Plan.',
  'Восемь отдельных вилл трёх типов на территории гольф-курорта Валле-Романо, у каждой собственный бассейн-инфинити, продажа на стадии проекта.',
  'ثماني فلل مستقلة من ثلاثة أنماط داخل منتجع غولف فايي رومانو، لكل منها مسبح خاص بحافة لا متناهية، تُباع على المخطط.',
  'Acht vrijstaande villa’s in drie types binnen het golfresort Valle Romano, elk met een eigen infinityzwembad, verkocht op plan.',
  'Osiem wolnostojących willi w trzech typach na terenie kurortu golfowego Valle Romano, każda z prywatnym basenem typu infinity, w sprzedaży z planu.',
  'Åtte frittstående villaer i tre typer inne på golfanlegget Valle Romano, hver med eget infinitybasseng, solgt på tegning.',
  'Åtta fristående villor i tre typer inne på golfanläggningen Valle Romano, var och en med egen infinitypool, till salu på ritning.')
a(8, '3-4 bathrooms',
  '3-4 baños', '3-4 salles de bains', '3-4 Badezimmer', '3-4 ванные комнаты', '3-4 حمامات',
  '3-4 badkamers', '3-4 łazienki', '3-4 bad', '3-4 badrum')
a(9, '8 villas on the price list',
  '8 villas en la lista de precios', '8 villas sur la liste de prix', '8 Villen auf der Preisliste', '8 вилл в прайс-листе',
  '8 فلل في قائمة الأسعار', '8 villa’s op de prijslijst', '8 willi w cenniku', '8 villaer på prislisten', '8 villor på prislistan')

# ---------------------------------------------------------------- image alts
a(10, 'A two-storey villa above its infinity-edge pool',
  'Una villa de dos plantas sobre su piscina de borde infinito, con las colinas al fondo',
  'Une villa de deux niveaux au-dessus de sa piscine à débordement, les collines au loin',
  'Eine zweigeschossige Villa über ihrem Infinity-Pool, dahinter die Hügel',
  'Двухэтажная вилла над собственным бассейном-инфинити, на заднем плане холмы',
  'فيلا من طابقين فوق مسبحها ذي الحافة اللامتناهية، والتلال في الخلفية',
  'Een villa van twee verdiepingen boven haar infinityzwembad, met de heuvels erachter',
  'Dwukondygnacyjna willa nad własnym basenem typu infinity, w tle wzgórza',
  'En villa i to etasjer over infinitybassenget, med åsene bak',
  'En villa i två plan ovanför sin infinitypool, med kullarna i bakgrunden')
a(11, 'A villa with a wood-effect pergola over its dining terrace',
  'Una villa con una pérgola de efecto madera sobre la terraza comedor',
  'Une villa avec une pergola effet bois au-dessus de la terrasse repas',
  'Eine Villa mit einer Pergola in Holzoptik über der Essterrasse',
  'Вилла с перголой под дерево над обеденной террасой',
  'فيلا ببرغولا بمظهر الخشب فوق تراس الطعام',
  'Een villa met een pergola in houtlook boven het eetterras',
  'Willa z pergolą imitującą drewno nad tarasem jadalnianym',
  'En villa med en pergola i treimitasjon over spiseterrassen',
  'En villa med en pergola i träimitation över matterrassen')
a(12, 'Lunch under the pergola beside an infinity-edge pool',
  'Almuerzo bajo la pérgola junto a una piscina de borde infinito, con el mar a lo lejos',
  'Déjeuner sous la pergola au bord d’une piscine à débordement, la mer au loin',
  'Mittagessen unter der Pergola neben einem Infinity-Pool, in der Ferne das Meer',
  'Обед под перголой у бассейна-инфинити, вдали море',
  'غداء تحت البرغولا بجوار مسبح بحافة لا متناهية، والبحر في الأفق',
  'Lunch onder de pergola naast een infinityzwembad, met de zee in de verte',
  'Obiad pod pergolą przy basenie typu infinity, w oddali morze',
  'Lunsj under pergolaen ved et infinitybasseng, med havet i det fjerne',
  'Lunch under pergolan bredvid en infinitypool, med havet i fjärran')
a(13, 'A living room open to a terrace and pool above the golf valley',
  'Un salón abierto a una terraza y a la piscina sobre el valle del golf',
  'Un séjour ouvert sur une terrasse et la piscine, au-dessus de la vallée du golf',
  'Ein Wohnzimmer, offen zur Terrasse und zum Pool über dem Golftal',
  'Гостиная, открытая на террасу и бассейн над долиной с гольф-полем',
  'غرفة معيشة مفتوحة على تراس ومسبح فوق وادي الغولف',
  'Een woonkamer die opent naar een terras en zwembad boven het golfdal',
  'Salon otwarty na taras i basen nad doliną z polem golfowym',
  'En stue som åpner seg mot en terrasse og et basseng over golfdalen',
  'Ett vardagsrum som öppnar sig mot en terrass och pool ovanför golfdalen')
a(15, 'A Type I villa, its upper terrace',
  'Una villa de tipo I, con la terraza superior a la sombra de una pérgola sobre el jardín',
  'Une villa de type I, sa terrasse supérieure ombragée par une pergola au-dessus du jardin',
  'Eine Villa vom Typ I, die obere Terrasse unter einer Pergola über dem Garten',
  'Вилла типа I: верхняя терраса под перголой над садом',
  'فيلا من النمط الأول، تراسها العلوي مظلَّل ببرغولا فوق الحديقة',
  'Een villa van type I, het boventerras beschaduwd door een pergola boven de tuin',
  'Willa typu I, górny taras zacieniony pergolą nad ogrodem',
  'En villa av type I, med den øvre terrassen i skyggen av en pergola over hagen',
  'En villa av typ I, med den övre terrassen i skuggan av en pergola ovanför trädgården')
a(16, 'Type I, Villas 1 and 2',
  'Tipo I, villas 1 y 2', 'Type I, villas 1 et 2', 'Typ I, Villen 1 und 2', 'Тип I, виллы 1 и 2', 'النمط الأول، الفيلتان 1 و2',
  'Type I, villa 1 en 2', 'Typ I, wille 1 i 2', 'Type I, villa 1 og 2', 'Typ I, villa 1 och 2')
a(17, 'A Type II villa, glazed across',
  'Una villa de tipo II, acristalada a lo largo de la planta de día, con la piscina delante',
  'Une villa de type II, vitrée sur toute la largeur du niveau de vie, la piscine devant',
  'Eine Villa vom Typ II, über die ganze Wohnebene verglast, davor der Pool',
  'Вилла типа II с остеклением по всему жилому этажу и бассейном перед ней',
  'فيلا من النمط الثاني، مزججة على امتداد طابق المعيشة، ومسبحها أمامها',
  'Een villa van type II, over de hele woonverdieping beglaasd, met het zwembad ervoor',
  'Willa typu II, przeszklona na całej długości kondygnacji dziennej, z basenem od frontu',
  'En villa av type II, med glass langs hele stueetasjen og bassenget foran',
  'En villa av typ II, inglasad längs hela vardagsplanet, med poolen framför')
a(18, 'Type II, Villas 3 to 7',
  'Tipo II, villas 3 a 7', 'Type II, villas 3 à 7', 'Typ II, Villen 3 bis 7', 'Тип II, виллы 3–7', 'النمط الثاني، الفلل من 3 إلى 7',
  'Type II, villa 3 tot 7', 'Typ II, wille 3–7', 'Type II, villa 3 til 7', 'Typ II, villa 3 till 7')
a(19, 'The Type III villa behind',
  'La villa de tipo III tras una amplia piscina de borde infinito y una pérgola de madera',
  'La villa de type III derrière une large piscine à débordement et une pergola en bois',
  'Die Villa vom Typ III hinter einem breiten Infinity-Pool und einer Holzpergola',
  'Вилла типа III за широким бассейном-инфинити и деревянной перголой',
  'فيلا النمط الثالث خلف مسبح واسع بحافة لا متناهية وبرغولا خشبية',
  'De villa van type III achter een breed infinityzwembad en een houten pergola',
  'Willa typu III za szerokim basenem typu infinity i drewnianą pergolą',
  'Villaen av type III bak et bredt infinitybasseng og en pergola i tre',
  'Villan av typ III bakom en bred infinitypool och en pergola i trä')
a(20, 'Type III, Villa 8',
  'Tipo III, villa 8', 'Type III, villa 8', 'Typ III, Villa 8', 'Тип III, вилла 8', 'النمط الثالث، الفيلا 8',
  'Type III, villa 8', 'Typ III, willa 8', 'Type III, villa 8', 'Typ III, villa 8')
a(21, 'The pergola',
  'La pérgola', 'La pergola', 'Die Pergola', 'Пергола', 'البرغولا', 'De pergola', 'Pergola', 'Pergolaen', 'Pergolan')
a(22, 'Loungers on a pool terrace at first light',
  'Tumbonas en la terraza de la piscina al amanecer, con la costa en el horizonte',
  'Des transats sur une terrasse de piscine au petit matin, la côte à l’horizon',
  'Liegen auf einer Poolterrasse im ersten Morgenlicht, am Horizont die Küste',
  'Шезлонги на террасе у бассейна на рассвете, на горизонте побережье',
  'كراسي استلقاء على تراس المسبح مع أول ضوء، والساحل في الأفق',
  'Ligstoelen op een zwembadterras bij het eerste licht, met de kust aan de horizon',
  'Leżaki na tarasie przy basenie o świcie, na horyzoncie wybrzeże',
  'Solsenger på en bassengterrasse i morgenlyset, med kysten i horisonten',
  'Solstolar på en poolterrass i gryningsljuset, med kusten vid horisonten')
a(23, 'A covered terrace at sunset',
  'Una terraza cubierta al atardecer, con vistas al valle del golf',
  'Une terrasse couverte au coucher du soleil, face à la vallée du golf',
  'Eine überdachte Terrasse bei Sonnenuntergang mit Blick über das Golftal',
  'Крытая терраса на закате с видом на долину с гольф-полем',
  'تراس مغطى عند الغروب يطل على وادي الغولف',
  'Een overdekt terras bij zonsondergang, met uitzicht over het golfdal',
  'Zadaszony taras o zachodzie słońca z widokiem na dolinę z polem golfowym',
  'En overbygd terrasse i solnedgangen, med utsikt over golfdalen',
  'En övertäckt terrass i solnedgången, med utsikt över golfdalen')
a(24, 'A round dining table by an inner planted patio',
  'Una mesa de comedor redonda junto a un patio interior ajardinado, con la escalera y la zona de estar al fondo',
  'Une table ronde près d’un patio intérieur planté, l’escalier et le séjour au fond',
  'Ein runder Esstisch an einem bepflanzten Innenhof, dahinter die Treppe und der Wohnbereich',
  'Круглый обеденный стол у внутреннего озеленённого патио, дальше лестница и гостиная зона',
  'طاولة طعام مستديرة بجانب فناء داخلي مزروع، والدرج ومنطقة الجلوس في الخلفية',
  'Een ronde eettafel bij een beplante binnenpatio, met de trap en de zithoek erachter',
  'Okrągły stół jadalniany przy wewnętrznym patio z roślinnością, w głębi schody i strefa wypoczynkowa',
  'Et rundt spisebord ved en beplantet innergård, med trappen og stuen bak',
  'Ett runt matbord vid en planterad innergård, med trappan och vardagsrummet bakom')
a(25, 'A kitchen island in veined stone',
  'Una isla de cocina en piedra veteada con placa de inducción, acristalada hacia las vistas',
  'Un îlot de cuisine en pierre veinée avec plaque à induction, vitré sur la vue',
  'Eine Kücheninsel aus geädertem Stein mit Induktionskochfeld, verglast zur Aussicht',
  'Кухонный остров из камня с прожилками с индукционной варочной панелью, остекление с видом',
  'جزيرة مطبخ من الحجر المعرّق مع موقد حثّي، وواجهة زجاجية على الإطلالة',
  'Een kookeiland in geaderde steen met inductiekookplaat, beglaasd naar het uitzicht',
  'Wyspa kuchenna z żyłkowanego kamienia z płytą indukcyjną, przeszklenie z widokiem',
  'En kjøkkenøy i årete stein med induksjonstopp, med glassvegger mot utsikten',
  'En köksö i ådrad sten med induktionshäll, med glaspartier mot utsikten')
a(26, 'A bedroom with sliding glass doors',
  'Un dormitorio con puertas correderas de cristal a una terraza y la costa al fondo',
  'Une chambre avec baies coulissantes sur une terrasse, la côte au loin',
  'Ein Schlafzimmer mit gläsernen Schiebetüren zur Terrasse, dahinter die Küste',
  'Спальня с раздвижными стеклянными дверями на террасу, вдали побережье',
  'غرفة نوم بأبواب زجاجية منزلقة على تراس، والساحل في الخلفية',
  'Een slaapkamer met glazen schuifdeuren naar een terras, met de kust in de verte',
  'Sypialnia z przesuwnymi szklanymi drzwiami na taras, w oddali wybrzeże',
  'Et soverom med skyvedører i glass ut mot en terrasse, med kysten bak',
  'Ett sovrum med skjutdörrar i glas mot en terrass, med kusten bortom')
a(27, 'Twin vessel basins beside a freestanding bath',
  'Dos lavabos sobre encimera junto a una bañera exenta y una ducha a ras de suelo',
  'Deux vasques à poser à côté d’une baignoire îlot et d’une douche à l’italienne',
  'Zwei Aufsatzwaschbecken neben einer freistehenden Badewanne und einer bodengleichen Dusche',
  'Две накладные раковины рядом с отдельно стоящей ванной и душем на уровне пола',
  'حوضان فوق سطح المغسلة بجانب حوض استحمام قائم بذاته ودش مفتوح',
  'Twee opzetwastafels naast een vrijstaand bad en een inloopdouche',
  'Dwie umywalki nablatowe obok wolnostojącej wanny i prysznica bez brodzika',
  'To servanter på benkeplaten ved siden av et frittstående badekar og en dusj i gulvnivå',
  'Två tvättställ på bänkskivan bredvid ett fristående badkar och en dusch i golvnivå')
a(28, 'The golf clubhouse at dusk',
  'La casa club del golf al anochecer, sobre la calle', 'Le club-house du golf au crépuscule, au-dessus du fairway',
  'Das Golf-Clubhaus in der Abenddämmerung über dem Fairway', 'Клубный дом гольф-клуба в сумерках над фервеем',
  'مبنى نادي الغولف عند الغسق فوق مسار اللعب', 'Het golfclubhuis bij schemering boven de fairway',
  'Klub golfowy o zmierzchu nad torem gry', 'Golfklubbhuset i skumringen over fairwayen', 'Golfklubbhuset i skymningen ovanför fairwayen')
a(29, 'The golf clubhouse',
  'La casa club del golf', 'Le club-house du golf', 'Das Golf-Clubhaus', 'Клубный дом гольф-клуба', 'مبنى نادي الغولف',
  'Het golfclubhuis', 'Klub golfowy', 'Golfklubbhuset', 'Golfklubbhuset')
a(30, 'Estepona and its beach seen from above',
  'Estepona y su playa vistas desde lo alto, con las montañas detrás',
  'Estepona et sa plage vues d’en haut, les montagnes à l’arrière',
  'Estepona und sein Strand von oben, dahinter die Berge',
  'Эстепона и её пляж с высоты, позади горы',
  'إستيبونا وشاطئها من الأعلى، والجبال خلفها',
  'Estepona en het strand van bovenaf, met de bergen erachter',
  'Estepona i jej plaża z góry, w tle góry',
  'Estepona og stranden sett ovenfra, med fjellene bak',
  'Estepona och stranden sedda ovanifrån, med bergen bakom')

# ---------------------------------------------------------------- plan alts and captions
a(31, 'Site plan of Villa 1',
  'Plano de implantación de la villa 1, con el aparcamiento en lo alto de la parcela, la casa, la terraza y la piscina',
  'Plan de masse de la villa 1, avec le stationnement en haut de la parcelle, la maison, la terrasse et la piscine',
  'Lageplan der Villa 1 mit den Stellplätzen oben auf dem Grundstück, dem Haus, der Terrasse und dem Pool',
  'Генплан виллы 1: парковка в верхней части участка, дом, терраса и бассейн',
  'مخطط موقع الفيلا 1، مع موقف السيارات في أعلى قطعة الأرض، والمنزل، والتراس، والمسبح',
  'Situatietekening van villa 1, met het parkeren bovenaan het perceel, het huis, het terras en het zwembad',
  'Plan zagospodarowania willi 1: miejsca postojowe w górnej części działki, dom, taras i basen',
  'Situasjonsplan for villa 1, med parkeringen øverst på tomten, huset, terrassen og bassenget',
  'Situationsplan för villa 1, med parkeringen högst upp på tomten, huset, terrassen och poolen')
a(32, 'Villa 1, site plan',
  'Villa 1, plano de implantación', 'Villa 1, plan de masse', 'Villa 1, Lageplan', 'Вилла 1, генплан', 'الفيلا 1، مخطط الموقع',
  'Villa 1, situatietekening', 'Willa 1, plan zagospodarowania', 'Villa 1, situasjonsplan', 'Villa 1, situationsplan')
a(33, 'Ground floor plan of Villa 1',
  'Plano de la planta baja de la villa 1, con el salón, la cocina, la terraza cubierta y la piscina',
  'Plan du rez-de-chaussée de la villa 1, avec le séjour, la cuisine, la terrasse couverte et la piscine',
  'Grundriss des Erdgeschosses der Villa 1 mit Wohnzimmer, Küche, überdachter Terrasse und Pool',
  'План первого этажа виллы 1: гостиная, кухня, крытая терраса и бассейн',
  'مخطط الطابق الأرضي للفيلا 1، مع غرفة المعيشة والمطبخ والتراس المغطى والمسبح',
  'Plattegrond van de begane grond van villa 1, met de woonkamer, de keuken, het overdekte terras en het zwembad',
  'Rzut parteru willi 1: salon, kuchnia, zadaszony taras i basen',
  'Plantegning av første etasje i villa 1, med stue, kjøkken, overbygd terrasse og basseng',
  'Planritning över bottenvåningen i villa 1, med vardagsrum, kök, övertäckt terrass och pool')
a(34, 'First floor plan of Villa 1',
  'Plano de la planta primera de la villa 1, con el acceso, el aparcamiento y tres dormitorios',
  'Plan du premier étage de la villa 1, avec l’entrée, le stationnement et trois chambres',
  'Grundriss des Obergeschosses der Villa 1 mit Eingang, Stellplätzen und drei Schlafzimmern',
  'План второго этажа виллы 1: вход, парковка и три спальни',
  'مخطط الطابق الأول للفيلا 1، مع المدخل وموقف السيارات وثلاث غرف نوم',
  'Plattegrond van de eerste verdieping van villa 1, met de entree, het parkeren en drie slaapkamers',
  'Rzut piętra willi 1: wejście, miejsca postojowe i trzy sypialnie',
  'Plantegning av andre etasje i villa 1, med inngang, parkering og tre soverom',
  'Planritning över första våningen i villa 1, med entré, parkering och tre sovrum')
a(35, 'Site plan of Villa 2',
  'Plano de implantación de la villa 2, con el aparcamiento en lo alto de la parcela, la casa, la terraza y la piscina',
  'Plan de masse de la villa 2, avec le stationnement en haut de la parcelle, la maison, la terrasse et la piscine',
  'Lageplan der Villa 2 mit den Stellplätzen oben auf dem Grundstück, dem Haus, der Terrasse und dem Pool',
  'Генплан виллы 2: парковка в верхней части участка, дом, терраса и бассейн',
  'مخطط موقع الفيلا 2، مع موقف السيارات في أعلى قطعة الأرض، والمنزل، والتراس، والمسبح',
  'Situatietekening van villa 2, met het parkeren bovenaan het perceel, het huis, het terras en het zwembad',
  'Plan zagospodarowania willi 2: miejsca postojowe w górnej części działki, dom, taras i basen',
  'Situasjonsplan for villa 2, med parkeringen øverst på tomten, huset, terrassen og bassenget',
  'Situationsplan för villa 2, med parkeringen högst upp på tomten, huset, terrassen och poolen')
a(36, 'Villa 2, site plan',
  'Villa 2, plano de implantación', 'Villa 2, plan de masse', 'Villa 2, Lageplan', 'Вилла 2, генплан', 'الفيلا 2، مخطط الموقع',
  'Villa 2, situatietekening', 'Willa 2, plan zagospodarowania', 'Villa 2, situasjonsplan', 'Villa 2, situationsplan')
a(37, 'Ground floor plan of Villa 2',
  'Plano de la planta baja de la villa 2, con el salón, la cocina, la terraza cubierta y la piscina',
  'Plan du rez-de-chaussée de la villa 2, avec le séjour, la cuisine, la terrasse couverte et la piscine',
  'Grundriss des Erdgeschosses der Villa 2 mit Wohnzimmer, Küche, überdachter Terrasse und Pool',
  'План первого этажа виллы 2: гостиная, кухня, крытая терраса и бассейн',
  'مخطط الطابق الأرضي للفيلا 2، مع غرفة المعيشة والمطبخ والتراس المغطى والمسبح',
  'Plattegrond van de begane grond van villa 2, met de woonkamer, de keuken, het overdekte terras en het zwembad',
  'Rzut parteru willi 2: salon, kuchnia, zadaszony taras i basen',
  'Plantegning av første etasje i villa 2, med stue, kjøkken, overbygd terrasse og basseng',
  'Planritning över bottenvåningen i villa 2, med vardagsrum, kök, övertäckt terrass och pool')
a(38, 'First floor plan of Villa 2',
  'Plano de la planta primera de la villa 2, con el acceso, el aparcamiento y tres dormitorios',
  'Plan du premier étage de la villa 2, avec l’entrée, le stationnement et trois chambres',
  'Grundriss des Obergeschosses der Villa 2 mit Eingang, Stellplätzen und drei Schlafzimmern',
  'План второго этажа виллы 2: вход, парковка и три спальни',
  'مخطط الطابق الأول للفيلا 2، مع المدخل وموقف السيارات وثلاث غرف نوم',
  'Plattegrond van de eerste verdieping van villa 2, met de entree, het parkeren en drie slaapkamers',
  'Rzut piętra willi 2: wejście, miejsca postojowe i trzy sypialnie',
  'Plantegning av andre etasje i villa 2, med inngang, parkering og tre soverom',
  'Planritning över första våningen i villa 2, med entré, parkering och tre sovrum')

# ---------------------------------------------------------------- overview
a(47, 'Eight villas, <em>three types</em>',
  'Ocho villas, <em>tres tipologías</em>', 'Huit villas, <em>trois types</em>', 'Acht Villen, <em>drei Typen</em>',
  'Восемь вилл, <em>три типа</em>', 'ثماني فلل، <em>ثلاثة أنماط</em>', 'Acht villa’s, <em>drie types</em>',
  'Osiem willi, <em>trzy typy</em>', 'Åtte villaer, <em>tre typer</em>', 'Åtta villor, <em>tre typer</em>')
a(48, 'Valle Romano Crest Villas is a group of eight',
  'Valle Romano Crest Villas es un conjunto de ocho casas independientes dentro del resort de golf de Valle Romano, en Estepona, en tres tipologías. Cada una se levanta en su propia parcela de 400 a {G1002} {U} y se proyecta con piscina privada de borde infinito, jardín y aparcamiento.',
  'Valle Romano Crest Villas réunit huit maisons indépendantes au sein du domaine de golf de Valle Romano, à Estepona, en trois types. Chacune occupe sa propre parcelle de 400 à {G1002} {U} et est dessinée avec une piscine privée à débordement, un jardin et un stationnement.',
  'Valle Romano Crest Villas ist eine Gruppe von acht freistehenden Häusern in drei Typen im Golfresort Valle Romano in Estepona. Jedes steht auf einem eigenen Grundstück von 400 bis {G1002} {U} und ist mit eigenem Infinity-Pool, Garten und Stellplätzen geplant.',
  'Valle Romano Crest Villas — это восемь отдельных домов трёх типов на территории гольф-курорта Валле-Романо в Эстепоне. Каждый стоит на собственном участке от 400 до {G1002} {U}, и по проекту у каждого есть бассейн-инфинити, сад и парковка.',
  'Valle Romano Crest Villas مجموعة من ثمانية منازل مستقلة من ثلاثة أنماط داخل منتجع غولف فايي رومانو في إستيبونا. يقوم كل منها على قطعة أرض خاصة به من 400 إلى {G1002} {U}، وتشمل مخططاته مسبحاً خاصاً بحافة لا متناهية وحديقة وموقفاً للسيارات.',
  'Valle Romano Crest Villas is een groep van acht vrijstaande huizen in drie types binnen het golfresort Valle Romano in Estepona. Elk staat op een eigen perceel van 400 tot {G1002} {U} en is getekend met een eigen infinityzwembad, een tuin en parkeerplaats.',
  'Valle Romano Crest Villas to zespół ośmiu wolnostojących domów w trzech typach na terenie kurortu golfowego Valle Romano w Esteponie. Każdy stoi na własnej działce o powierzchni od 400 do {G1002} {U} i ma w projekcie prywatny basen typu infinity, ogród i miejsca postojowe.',
  'Valle Romano Crest Villas er en gruppe på åtte frittstående hus i tre typer inne på golfanlegget Valle Romano i Estepona. Hvert står på egen tomt på 400 til {G1002} {U} og er tegnet med eget infinitybasseng, hage og parkering.',
  'Valle Romano Crest Villas är en grupp om åtta fristående hus i tre typer inne på golfanläggningen Valle Romano i Estepona. Vart och ett står på en egen tomt om 400 till {G1002} {U} och är ritat med egen infinitypool, trädgård och parkering.')
a(49, 'The houses are built on two floors into the slope',
  'Las casas se desarrollan en dos plantas adaptadas a la pendiente, con el salón, la cocina y la piscina en la planta baja y los dormitorios arriba. Las villas 1 y 2 son el compacto tipo I, las villas 3 a 7 el tipo II, y la villa 8 es el único tipo III, más amplio, con 433 {U} interiores en una parcela de {G1002} {U}.',
  'Les maisons s’étagent sur deux niveaux dans la pente, avec le séjour, la cuisine et la piscine au rez-de-chaussée et les chambres à l’étage. Les villas 1 et 2 forment le type I, compact, les villas 3 à 7 le type II, et la villa 8 est l’unique type III, plus vaste, avec 433 {U} intérieurs sur une parcelle de {G1002} {U}.',
  'Die Häuser sind zweigeschossig in den Hang gebaut, mit Wohnzimmer, Küche und Pool im Erdgeschoss und den Schlafzimmern darüber. Die Villen 1 und 2 sind der kompakte Typ I, die Villen 3 bis 7 der Typ II, und Villa 8 ist der einzige, größere Typ III mit 433 {U} Innenfläche auf einem Grundstück von {G1002} {U}.',
  'Дома двухэтажные и встроены в склон: гостиная, кухня и бассейн на первом этаже, спальни этажом выше. Виллы 1 и 2 — компактный тип I, виллы 3–7 — тип II, а вилла 8 — единственный, более просторный тип III с 433 {U} внутренней площади на участке {G1002} {U}.',
  'تتوزع المنازل على طابقين مبنيين في المنحدر، مع غرفة المعيشة والمطبخ والمسبح في الطابق الأرضي وغرف النوم في الأعلى. الفيلتان 1 و2 من النمط الأول المدمج، والفلل من 3 إلى 7 من النمط الثاني، أما الفيلا 8 فهي النمط الثالث الوحيد والأكبر، بمساحة داخلية 433 {U} على قطعة أرض من {G1002} {U}.',
  'De huizen zijn in twee verdiepingen tegen de helling gebouwd, met de woonkamer, de keuken en het zwembad op de begane grond en de slaapkamers erboven. Villa 1 en 2 zijn het compacte type I, villa 3 tot 7 het type II, en villa 8 is het enige, grotere type III, met 433 {U} binnenoppervlak op een perceel van {G1002} {U}.',
  'Domy mają dwie kondygnacje wpisane w zbocze: salon, kuchnia i basen na parterze, sypialnie piętro wyżej. Wille 1 i 2 to kompaktowy typ I, wille 3–7 to typ II, a willa 8 to jedyny, większy typ III, z 433 {U} powierzchni wewnętrznej na działce o powierzchni {G1002} {U}.',
  'Husene er bygget i to etasjer inn i skråningen, med stue, kjøkken og basseng i første etasje og soverommene over. Villa 1 og 2 er den kompakte type I, villa 3 til 7 type II, og villa 8 er den eneste, større type III, med 433 {U} innvendig på en tomt på {G1002} {U}.',
  'Husen är byggda i två plan in i sluttningen, med vardagsrum, kök och pool på bottenvåningen och sovrummen ovanför. Villa 1 och 2 är den kompakta typ I, villa 3 till 7 typ II, och villa 8 är den enda, större typ III, med 433 {U} inneryta på en tomt om {G1002} {U}.')
a(50, 'The project is off-plan.',
  'El proyecto se vende sobre plano. La lista de precios del promotor de octubre de 2026 indica un informe favorable de la licencia de obras con la concesión aún pendiente, la licitación de obra completada y la constructora todavía por elegir, y prevé la finalización para el {Q}.',
  'Le projet est vendu sur plan. La liste de prix du promoteur d’octobre 2026 fait état d’un avis favorable sur le permis de construire, dont l’octroi reste en attente, d’un appel d’offres des travaux achevé et d’une entreprise générale pas encore choisie, et prévoit l’achèvement au {Q}.',
  'Das Projekt wird Off-Plan verkauft. Die Preisliste des Bauträgers vom Oktober 2026 nennt ein positives Gutachten zur Baugenehmigung, deren Erteilung noch aussteht, eine abgeschlossene Bauausschreibung und ein noch nicht ausgewähltes Bauunternehmen, und sieht die Fertigstellung für {Q} vor.',
  'Проект продаётся на стадии проекта. Прайс-лист застройщика за октябрь 2026 года сообщает о положительном заключении по разрешению на строительство, которое ещё не выдано, о завершённом тендере на строительные работы и о том, что подрядчик пока не выбран; завершение ожидается в {Q}.',
  'يُباع المشروع على المخطط. وتذكر قائمة أسعار المطوّر لشهر أكتوبر 2026 صدور تقرير إيجابي بشأن رخصة البناء مع بقاء منحها معلّقاً، واكتمال مناقصة الأعمال، وعدم اختيار المقاول بعد، وتتوقع الإنجاز في {Q}.',
  'Het project wordt op plan verkocht. De prijslijst van de ontwikkelaar van oktober 2026 meldt een gunstig advies over de bouwvergunning, waarvan de verlening nog in behandeling is, een afgeronde aanbesteding van de bouw en een aannemer die nog niet gekozen is, en verwacht de oplevering in {Q}.',
  'Projekt jest sprzedawany z planu. Cennik dewelopera z października 2026 roku podaje pozytywną opinię w sprawie pozwolenia na budowę, którego wydanie wciąż jest w toku, zakończony przetarg na roboty i niewybranego jeszcze wykonawcę, a zakończenie przewiduje na {Q}.',
  'Prosjektet selges på tegning. Utbyggerens prisliste fra oktober 2026 oppgir en positiv uttalelse om byggetillatelsen, der selve tillatelsen ennå ikke er gitt, et avsluttet anbud for byggearbeidene og en entreprenør som ennå ikke er valgt, og venter ferdigstillelse i {Q}.',
  'Projektet säljs på ritning. Exploatörens prislista från oktober 2026 anger ett positivt yttrande om bygglovet, som ännu inte har beviljats, en avslutad upphandling av byggarbetena och en entreprenör som ännu inte är vald, och väntar färdigställande {Q}.')

# ---------------------------------------------------------------- residences
a(51, 'Three types, <em>eight plots</em>',
  'Tres tipologías, <em>ocho parcelas</em>', 'Trois types, <em>huit parcelles</em>', 'Drei Typen, <em>acht Grundstücke</em>',
  'Три типа, <em>восемь участков</em>', 'ثلاثة أنماط، <em>ثماني قطع أرض</em>', 'Drie types, <em>acht percelen</em>',
  'Trzy typy, <em>osiem działek</em>', 'Tre typer, <em>åtte tomter</em>', 'Tre typer, <em>åtta tomter</em>')
a(53, '122 and 124 sqm of interior',
  '122 y 124 {U} interiores, 279 y 281 {U} construidos en total, en parcelas de 400 y 411 {U} orientadas al suroeste.',
  '122 et 124 {U} intérieurs, 279 et 281 {U} construits au total, sur des parcelles de 400 et 411 {U} orientées sud-ouest.',
  '122 und 124 {U} Innenfläche, insgesamt 279 und 281 {U} bebaut, auf Grundstücken von 400 und 411 {U} mit Südwestausrichtung.',
  '122 и 124 {U} внутренней площади, 279 и 281 {U} общей застройки, на участках 400 и 411 {U} с ориентацией на юго-запад.',
  '122 و124 {U} من المساحة الداخلية، و279 و281 {U} مبنية إجمالاً، على قطعتي أرض من 400 و411 {U} بواجهة جنوبية غربية.',
  '122 en 124 {U} binnenoppervlak, in totaal 279 en 281 {U} bebouwd, op percelen van 400 en 411 {U} op het zuidwesten.',
  '122 i 124 {U} powierzchni wewnętrznej, łącznie 279 i 281 {U} zabudowy, na działkach o powierzchni 400 i 411 {U} z ekspozycją południowo-zachodnią.',
  '122 og 124 {U} innvendig, totalt 279 og 281 {U} bebygd, på tomter på 400 og 411 {U} mot sørvest.',
  '122 och 124 {U} inneryta, totalt 279 och 281 {U} byggyta, på tomter om 400 och 411 {U} i sydvästläge.')
a(54, 'Ground floor: an open living room, dining area and kitchen',
  'Planta baja: salón, comedor y cocina abiertos de {N28.42} a {N30.92} {U}, lavadero, un trastero de unos 10 {U} iluminado por un patio inglés, un baño, una terraza cubierta y una piscina de unos 19 {U}.',
  'Rez-de-chaussée : séjour, coin repas et cuisine ouverts de {N28.42} à {N30.92} {U}, une buanderie, un cellier d’environ 10 {U} éclairé par une cour anglaise, une salle de bains, une terrasse couverte et une piscine d’environ 19 {U}.',
  'Erdgeschoss: ein offener Wohn-, Ess- und Küchenbereich von {N28.42} bis {N30.92} {U}, ein Hauswirtschaftsraum, ein Abstellraum von etwa 10 {U} mit Licht aus einem Lichthof, ein Badezimmer, eine überdachte Terrasse und ein Pool von etwa 19 {U}.',
  'Первый этаж: открытая гостиная со столовой и кухней площадью от {N28.42} до {N30.92} {U}, постирочная, кладовая около 10 {U} со светом из приямка, ванная комната, крытая терраса и бассейн около 19 {U}.',
  'الطابق الأرضي: غرفة معيشة وطعام ومطبخ مفتوحة من {N28.42} إلى {N30.92} {U}، وغرفة غسيل، ومخزن بنحو 10 {U} يضيئه فناء منخفض، وحمّام، وتراس مغطى، ومسبح بنحو 19 {U}.',
  'Begane grond: een open woonkamer, eethoek en keuken van {N28.42} tot {N30.92} {U}, een wasruimte, een berging van ongeveer 10 {U} met daglicht uit een lichtschacht, een badkamer, een overdekt terras en een zwembad van ongeveer 19 {U}.',
  'Parter: otwarty salon z jadalnią i kuchnią o powierzchni od {N28.42} do {N30.92} {U}, pralnia, schowek o powierzchni około 10 {U} doświetlony przez angielski dziedziniec, łazienka, zadaszony taras i basen o powierzchni około 19 {U}.',
  'Første etasje: åpen stue, spiseplass og kjøkken på {N28.42} til {N30.92} {U}, vaskerom, en bod på rundt 10 {U} med lys fra en lysgård, et bad, en overbygd terrasse og et basseng på rundt 19 {U}.',
  'Bottenvåning: öppet vardagsrum, matplats och kök om {N28.42} till {N30.92} {U}, tvättstuga, ett förråd på cirka 10 {U} med dagsljus från en ljusgård, ett badrum, en övertäckt terrass och en pool på cirka 19 {U}.')
a(55, 'First floor, at street level: the entrance, parking for two cars',
  'Planta primera, a nivel de calle: el acceso, aparcamiento para dos coches, tres dormitorios, un vestidor, dos baños y una terraza de unos 29 {U} bajo pérgola.',
  'Premier étage, au niveau de la rue : l’entrée, le stationnement pour deux voitures, trois chambres, un dressing, deux salles de bains et une terrasse d’environ 29 {U} sous pergola.',
  'Obergeschoss, auf Straßenniveau: der Eingang, Stellplätze für zwei Autos, drei Schlafzimmer, eine Ankleide, zwei Badezimmer und eine Terrasse von etwa 29 {U} unter einer Pergola.',
  'Второй этаж, на уровне улицы: вход, парковка на две машины, три спальни, гардеробная, две ванные комнаты и терраса около 29 {U} под перголой.',
  'الطابق الأول، على مستوى الشارع: المدخل، وموقف لسيارتين، وثلاث غرف نوم، وغرفة ملابس، وحمّامان، وتراس بنحو 29 {U} تحت برغولا.',
  'Eerste verdieping, op straatniveau: de entree, parkeerplaats voor twee auto’s, drie slaapkamers, een inloopkast, twee badkamers en een terras van ongeveer 29 {U} onder een pergola.',
  'Piętro, na poziomie ulicy: wejście, miejsca postojowe na dwa samochody, trzy sypialnie, garderoba, dwie łazienki i taras o powierzchni około 29 {U} pod pergolą.',
  'Andre etasje, på gatenivå: inngangen, parkering for to biler, tre soverom, en garderobe, to bad og en terrasse på rundt 29 {U} under pergola.',
  'Första våningen, i gatuplan: entrén, parkering för två bilar, tre sovrum, en klädkammare, två badrum och en terrass på cirka 29 {U} under pergola.')
a(57, '167 to 183 sqm of interior',
  'De 167 a 183 {U} interiores y de 327 a 370 {U} construidos en total, en parcelas de 533 a 560 {U}.',
  'De 167 à 183 {U} intérieurs et de 327 à 370 {U} construits au total, sur des parcelles de 533 à 560 {U}.',
  '167 bis 183 {U} Innenfläche und insgesamt 327 bis 370 {U} bebaut, auf Grundstücken von 533 bis 560 {U}.',
  'От 167 до 183 {U} внутренней площади и от 327 до 370 {U} общей застройки, на участках от 533 до 560 {U}.',
  'من 167 إلى 183 {U} من المساحة الداخلية، ومن 327 إلى 370 {U} مبنية إجمالاً، على قطع أرض من 533 إلى 560 {U}.',
  '167 tot 183 {U} binnenoppervlak en in totaal 327 tot 370 {U} bebouwd, op percelen van 533 tot 560 {U}.',
  'Od 167 do 183 {U} powierzchni wewnętrznej i łącznie od 327 do 370 {U} zabudowy, na działkach od 533 do 560 {U}.',
  '167 til 183 {U} innvendig og totalt 327 til 370 {U} bebygd, på tomter på 533 til 560 {U}.',
  '167 till 183 {U} inneryta och totalt 327 till 370 {U} byggyta, på tomter om 533 till 560 {U}.')
a(58, 'Villas 3, 4 and 5 face north-west',
  'Las villas 3, 4 y 5 están orientadas al noroeste; las villas 6 y 7 miran al sureste y tienen un precio más alto.',
  'Les villas 3, 4 et 5 sont orientées nord-ouest ; les villas 6 et 7 sont orientées sud-est et affichent un prix plus élevé.',
  'Die Villen 3, 4 und 5 sind nach Nordwesten ausgerichtet; die Villen 6 und 7 nach Südosten, und sie sind teurer.',
  'Виллы 3, 4 и 5 ориентированы на северо-запад; виллы 6 и 7 — на юго-восток, и их цена выше.',
  'الفلل 3 و4 و5 بواجهة شمالية غربية، أما الفيلتان 6 و7 فبواجهة جنوبية شرقية وبسعر أعلى.',
  'Villa 3, 4 en 5 liggen op het noordwesten; villa 6 en 7 liggen op het zuidoosten en zijn duurder.',
  'Wille 3, 4 i 5 mają ekspozycję północno-zachodnią; wille 6 i 7 są zwrócone na południowy wschód i mają wyższą cenę.',
  'Villa 3, 4 og 5 vender mot nordvest; villa 6 og 7 vender mot sørøst og er priset høyere.',
  'Villa 3, 4 och 5 vetter mot nordväst; villa 6 och 7 vetter mot sydost och är dyrare.')
a(61, '433 sqm of interior and 604 sqm',
  '433 {U} interiores y 604 {U} construidos en total, en una parcela de {G1002} {U} orientada al sureste.',
  '433 {U} intérieurs et 604 {U} construits au total, sur une parcelle de {G1002} {U} orientée sud-est.',
  '433 {U} Innenfläche und insgesamt 604 {U} bebaut, auf einem Grundstück von {G1002} {U} mit Südostausrichtung.',
  '433 {U} внутренней площади и 604 {U} общей застройки на участке {G1002} {U} с ориентацией на юго-восток.',
  '433 {U} من المساحة الداخلية و604 {U} مبنية إجمالاً، على قطعة أرض من {G1002} {U} بواجهة جنوبية شرقية.',
  '433 {U} binnenoppervlak en in totaal 604 {U} bebouwd, op een perceel van {G1002} {U} op het zuidoosten.',
  '433 {U} powierzchni wewnętrznej i łącznie 604 {U} zabudowy, na działce o powierzchni {G1002} {U} z ekspozycją południowo-wschodnią.',
  '433 {U} innvendig og totalt 604 {U} bebygd, på en tomt på {G1002} {U} mot sørøst.',
  '433 {U} inneryta och totalt 604 {U} byggyta, på en tomt om {G1002} {U} i sydostläge.')

# ---------------------------------------------------------------- availability
a(66, 'Eight villas <em>on the price list</em>',
  'Ocho villas <em>en la lista de precios</em>', 'Huit villas <em>sur la liste de prix</em>', 'Acht Villen <em>auf der Preisliste</em>',
  'Восемь вилл <em>в прайс-листе</em>', 'ثماني فلل <em>في قائمة الأسعار</em>', 'Acht villa’s <em>op de prijslijst</em>',
  'Osiem willi <em>w cenniku</em>', 'Åtte villaer <em>på prislisten</em>', 'Åtta villor <em>på prislistan</em>')
a(67, 'The developer\'s price list names eight villas',
  'La lista de precios del promotor recoge ocho villas e indica que describe la promoción, no lo que sigue a la venta. Nueva Living reconfirma precio y disponibilidad antes de cualquier visita o reserva.',
  'La liste de prix du promoteur nomme huit villas et précise qu’elle décrit le programme, non ce qui reste à vendre. Nueva Living reconfirme prix et disponibilité avant toute visite ou réservation.',
  'Die Preisliste des Bauträgers nennt acht Villen und weist darauf hin, dass sie das Projekt beschreibt und nicht, was noch zum Verkauf steht. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung erneut.',
  'Прайс-лист застройщика называет восемь вилл и оговаривает, что описывает проект, а не то, что ещё продаётся. Nueva Living повторно подтверждает цену и наличие перед любым просмотром или бронированием.',
  'تذكر قائمة أسعار المطوّر ثماني فلل، وتوضح أنها تصف المشروع لا ما لا يزال معروضاً للبيع. وتعيد Nueva Living تأكيد السعر والتوفر قبل أي معاينة أو حجز.',
  'De prijslijst van de ontwikkelaar noemt acht villa’s en vermeldt dat zij het project beschrijft en niet wat nog te koop is. Nueva Living bevestigt prijs en beschikbaarheid opnieuw vóór elke bezichtiging of reservering.',
  'Cennik dewelopera wymienia osiem willi i zaznacza, że opisuje inwestycję, a nie to, co jest jeszcze w sprzedaży. Nueva Living ponownie potwierdza cenę i dostępność przed każdą wizytą lub rezerwacją.',
  'Utbyggerens prisliste nevner åtte villaer og opplyser at den beskriver prosjektet, ikke hva som fortsatt er til salgs. Nueva Living bekrefter pris og tilgjengelighet på nytt før enhver visning eller reservasjon.',
  'Exploatörens prislista tar upp åtta villor och anger att den beskriver projektet, inte vad som fortfarande är till salu. Nueva Living bekräftar pris och tillgänglighet på nytt före varje visning eller bokning.')

# ---------------------------------------------------------------- payment terms
a(78, '€10,000, deducted from the first 20%',
  '{E10000}, descontados del primer {P20}', '{E10000}, déduits des premiers {P20}', '{E10000}, angerechnet auf die ersten {P20}',
  '{E10000}, засчитываются в первые {P20}', '{E10000}، تُخصم من أول {P20}', '{E10000}, in mindering op de eerste {P20}',
  '{E10000}, zaliczane na poczet pierwszych {P20}', '{E10000}, trekkes fra de første {P20}', '{E10000}, avräknas från de första {P20}')
a(79, '20% on signing the purchase contract',
  '{P20} a la firma del contrato de compraventa', '{P20} à la signature du contrat de vente', '{P20} bei Unterzeichnung des Kaufvertrags',
  '{P20} при подписании договора купли-продажи', '{P20} عند توقيع عقد البيع', '{P20} bij ondertekening van de koopovereenkomst',
  '{P20} przy podpisaniu umowy kupna', '{P20} ved signering av kjøpekontrakten', '{P20} vid undertecknandet av köpekontraktet')
a(80, '20% when the structure is complete',
  '{P20} al terminar la estructura', '{P20} à l’achèvement du gros œuvre', '{P20} nach Fertigstellung des Rohbaus',
  '{P20} по завершении каркаса', '{P20} عند اكتمال الهيكل', '{P20} bij voltooiing van de ruwbouw',
  '{P20} po ukończeniu konstrukcji', '{P20} når råbygget er ferdig', '{P20} när stommen är klar')
a(81, '60% at the title deed, expected Q4 2028',
  '{P60} en la escritura, prevista para el {Q}', '{P60} à l’acte notarié, prévu au {Q}', '{P60} bei der notariellen Urkunde, erwartet im {Q}',
  '{P60} при подписании купчей, ожидается в {Q}', '{P60} عند توقيع سند الملكية، المتوقع في {Q}', '{P60} bij de notariële akte, verwacht in {Q}',
  '{P60} przy akcie notarialnym, przewidywanym na {Q}', '{P60} ved skjøtet, ventet i {Q}', '{P60} vid lagfarten, väntad {Q}')
override('Structure',
  'Estructura', 'Gros œuvre', 'Rohbau', 'Каркас', 'الهيكل', 'Ruwbouw', 'Konstrukcja', 'Råbygg', 'Stomme')
a(82, 'Transcribed from the developer\'s price list of October 2026.',
  'Transcrito de la lista de precios del promotor de octubre de 2026. La licencia de obras cuenta con informe favorable y está pendiente de concesión, y la constructora aún no se ha elegido. Nueva Living confirma por escrito la licencia, el aval bancario de cada pago anterior a la entrega y el tratamiento del IVA antes de que se mueva dinero.',
  'Transcrit de la liste de prix du promoteur d’octobre 2026. Le permis de construire a reçu un avis favorable et attend son octroi, et l’entreprise générale n’est pas encore choisie. Nueva Living confirme par écrit le permis, la garantie bancaire de chaque versement avant la livraison et le traitement de la TVA avant tout mouvement de fonds.',
  'Übernommen aus der Preisliste des Bauträgers vom Oktober 2026. Für die Baugenehmigung liegt ein positives Gutachten vor, die Erteilung steht aus, und das Bauunternehmen ist noch nicht ausgewählt. Nueva Living bestätigt die Genehmigung, die Bankbürgschaft für jede Zahlung vor Übergabe und die Behandlung der MwSt. schriftlich, bevor Geld fließt.',
  'По прайс-листу застройщика за октябрь 2026 года. По разрешению на строительство есть положительное заключение, выдача ожидается, а подрядчик ещё не выбран. Nueva Living письменно подтверждает разрешение, банковскую гарантию на каждый платёж до сдачи и порядок начисления НДС до перевода любых средств.',
  'منقول من قائمة أسعار المطوّر لشهر أكتوبر 2026. حصلت رخصة البناء على تقرير إيجابي وهي بانتظار المنح، ولم يُختر المقاول بعد. وتؤكد Nueva Living كتابياً الرخصة والضمان المصرفي لكل دفعة قبل التسليم ومعاملة ضريبة القيمة المضافة قبل تحويل أي مبلغ.',
  'Overgenomen uit de prijslijst van de ontwikkelaar van oktober 2026. De bouwvergunning heeft een gunstig advies en wacht op verlening, en de aannemer is nog niet gekozen. Nueva Living bevestigt de vergunning, de bankgarantie op elke betaling vóór oplevering en de behandeling van de btw schriftelijk voordat er geld wordt overgemaakt.',
  'Na podstawie cennika dewelopera z października 2026 roku. Pozwolenie na budowę ma pozytywną opinię i czeka na wydanie, a wykonawca nie został jeszcze wybrany. Nueva Living potwierdza na piśmie pozwolenie, gwarancję bankową dla każdej wpłaty przed odbiorem i sposób naliczenia VAT, zanim zostaną przelane jakiekolwiek środki.',
  'Hentet fra utbyggerens prisliste fra oktober 2026. Byggetillatelsen har en positiv uttalelse og venter på å bli gitt, og entreprenøren er ennå ikke valgt. Nueva Living bekrefter tillatelsen, bankgarantien for hver innbetaling før overtakelse og behandlingen av mva skriftlig før penger overføres.',
  'Hämtat ur exploatörens prislista från oktober 2026. Bygglovet har fått ett positivt yttrande och väntar på att beviljas, och entreprenören är ännu inte vald. Nueva Living bekräftar bygglovet, bankgarantin för varje inbetalning före tillträdet och hur IVA (spansk moms) hanteras skriftligt innan några pengar förs över.')

# ---------------------------------------------------------------- why / investment / trust
a(83, 'Eight detached houses on their own plots inside a golf resort',
  'Ocho casas independientes en parcelas propias dentro de un resort de golf, a la venta antes de elegirse la constructora.',
  'Huit maisons indépendantes sur leurs propres parcelles dans un domaine de golf, vendues avant le choix de l’entreprise générale.',
  'Acht freistehende Häuser auf eigenen Grundstücken in einem Golfresort, verkauft, bevor das Bauunternehmen feststeht.',
  'Восемь отдельных домов на собственных участках на территории гольф-курорта, в продаже ещё до выбора подрядчика.',
  'ثمانية منازل مستقلة على قطع أرض خاصة داخل منتجع غولف، تُباع قبل اختيار المقاول.',
  'Acht vrijstaande huizen op eigen percelen binnen een golfresort, verkocht voordat de aannemer is gekozen.',
  'Osiem wolnostojących domów na własnych działkach na terenie kurortu golfowego, w sprzedaży jeszcze przed wyborem wykonawcy.',
  'Åtte frittstående hus på egne tomter inne på et golfanlegg, solgt før entreprenøren er valgt.',
  'Åtta fristående hus på egna tomter inne på en golfanläggning, till salu innan entreprenören är vald.')
a(84, 'Eight detached villas in three types, each on its own plot',
  'Ocho villas independientes de tres tipologías, cada una en su propia parcela con piscina privada de borde infinito y jardín.',
  'Huit villas indépendantes de trois types, chacune sur sa parcelle avec piscine privée à débordement et jardin.',
  'Acht freistehende Villen in drei Typen, jede auf eigenem Grundstück mit eigenem Infinity-Pool und Garten.',
  'Восемь отдельных вилл трёх типов, каждая на собственном участке с бассейном-инфинити и садом.',
  'ثماني فلل مستقلة من ثلاثة أنماط، كل منها على قطعة أرض خاصة بها مع مسبح خاص بحافة لا متناهية وحديقة.',
  'Acht vrijstaande villa’s in drie types, elk op een eigen perceel met een eigen infinityzwembad en een tuin.',
  'Osiem wolnostojących willi w trzech typach, każda na własnej działce z prywatnym basenem typu infinity i ogrodem.',
  'Åtte frittstående villaer i tre typer, hver på egen tomt med eget infinitybasseng og hage.',
  'Åtta fristående villor i tre typer, var och en på egen tomt med egen infinitypool och trädgård.')
a(85, 'Buyers who want a house of their own beside a golf course',
  'Compradores que buscan una casa propia junto a un campo de golf en lugar de una vivienda en un bloque, en la fase en que aún pueden elegir los acabados.',
  'Les acquéreurs qui souhaitent une maison à eux près d’un golf plutôt qu’un logement en immeuble, au stade où les finitions peuvent encore être choisies.',
  'Käufer, die statt einer Wohnung in einem Block ein eigenes Haus an einem Golfplatz suchen, in der Phase, in der die Ausstattung noch wählbar ist.',
  'Покупателям, которым нужен собственный дом у гольф-поля, а не квартира в доме, на этапе, когда отделку ещё можно выбрать.',
  'للمشترين الراغبين في منزل خاص بهم بجوار ملعب غولف بدلاً من مسكن في مبنى، في المرحلة التي لا يزال فيها اختيار التشطيبات ممكناً.',
  'Kopers die een eigen huis naast een golfbaan zoeken in plaats van een woning in een blok, in de fase waarin de afwerking nog te kiezen is.',
  'Dla kupujących, którzy zamiast mieszkania w bloku szukają własnego domu przy polu golfowym, na etapie, na którym wykończenie można jeszcze wybrać.',
  'Kjøpere som vil ha et eget hus ved en golfbane i stedet for en bolig i en blokk, på det stadiet der du fortsatt kan velge overflatene.',
  'Köpare som vill ha ett eget hus vid en golfbana i stället för en bostad i ett flerbostadshus, i det skede då ni fortfarande kan välja ytskikten.')
a(86, 'The range runs from two compact villas',
  'La gama va de dos villas compactas en parcelas de 400 {U} a una de 433 {U} interiores en {G1002} {U}, todas dentro del mismo pequeño conjunto.',
  'La gamme va de deux villas compactes sur des parcelles de 400 {U} à une villa de 433 {U} intérieurs sur {G1002} {U}, toutes au sein du même petit ensemble.',
  'Die Auswahl reicht von zwei kompakten Villen auf Grundstücken von 400 {U} bis zu einer mit 433 {U} Innenfläche auf {G1002} {U}, alle in derselben kleinen Gruppe.',
  'Выбор — от двух компактных вилл на участках 400 {U} до виллы с 433 {U} внутренней площади на {G1002} {U}, и всё в одной небольшой группе.',
  'تتراوح المجموعة بين فيلتين مدمجتين على قطعتي أرض من 400 {U} وفيلا بمساحة داخلية 433 {U} على {G1002} {U}، وجميعها ضمن المجموعة الصغيرة نفسها.',
  'Het aanbod loopt van twee compacte villa’s op percelen van 400 {U} tot één van 433 {U} binnenoppervlak op {G1002} {U}, allemaal binnen dezelfde kleine groep.',
  'Oferta obejmuje zarówno dwie kompaktowe wille na działkach 400 {U}, jak i jedną z 433 {U} powierzchni wewnętrznej na {G1002} {U}, wszystkie w tym samym niewielkim zespole.',
  'Utvalget spenner fra to kompakte villaer på tomter på 400 {U} til én med 433 {U} innvendig på {G1002} {U}, alle i den samme lille gruppen.',
  'Utbudet sträcker sig från två kompakta villor på tomter om 400 {U} till en med 433 {U} inneryta på {G1002} {U}, alla i samma lilla grupp.')
a(88, 'The houses are priced off-plan',
  'Las casas tienen precio sobre plano, con la finalización prevista para el {Q}, y el {P60} del precio se paga en la escritura.',
  'Les maisons sont vendues sur plan, avec un achèvement prévu au {Q}, et {P60} du prix sont dus à l’acte notarié.',
  'Die Häuser haben Off-Plan-Preise, die Fertigstellung ist für {Q} vorgesehen, und {P60} des Preises werden bei der notariellen Urkunde fällig.',
  'Дома продаются по ценам на стадии проекта, завершение ожидается в {Q}, а {P60} цены оплачивается при подписании купчей.',
  'تُسعّر المنازل على المخطط، ويُتوقع الإنجاز في {Q}، ويُستحق {P60} من السعر عند توقيع سند الملكية.',
  'De huizen zijn geprijsd op plan, met de oplevering verwacht in {Q}, en {P60} van de prijs is verschuldigd bij de notariële akte.',
  'Domy mają ceny z planu, zakończenie przewidziane jest na {Q}, a {P60} ceny płaci się przy akcie notarialnym.',
  'Husene er priset på tegning med ferdigstillelse ventet i {Q}, og {P60} av prisen forfaller ved skjøtet.',
  'Husen är prissatta på ritning med färdigställande väntat {Q}, och {P60} av priset förfaller vid lagfarten.')
a(89, 'Eight houses on an established golf course',
  'Ocho casas en un campo de golf consolidado, un grupo cerrado y no una fase que se repite.',
  'Huit maisons sur un golf établi, un ensemble limité plutôt qu’une tranche qui se répète.',
  'Acht Häuser an einem etablierten Golfplatz, eine abgeschlossene Gruppe statt eines Bauabschnitts, der sich wiederholt.',
  'Восемь домов у давно существующего гольф-поля — ограниченная группа, а не повторяющаяся очередь.',
  'ثمانية منازل على ملعب غولف قائم منذ زمن، مجموعة محدودة لا مرحلة تتكرر.',
  'Acht huizen aan een gevestigde golfbaan, een afgebakende groep en geen fase die zich herhaalt.',
  'Osiem domów przy istniejącym od lat polu golfowym, zamknięty zespół, a nie kolejny powtarzalny etap.',
  'Åtte hus ved en etablert golfbane, en avgrenset gruppe og ikke et byggetrinn som gjentas.',
  'Åtta hus vid en etablerad golfbana, en avgränsad grupp och inte en etapp som upprepas.')
a(90, 'Suits full-time living or a second home',
  'Adecuada para vivir todo el año o como segunda residencia; el alquiler vacacional depende de la licencia local, que comprobamos.',
  'Convient à une résidence principale ou secondaire ; une location saisonnière dépend de la licence locale, que nous vérifions.',
  'Geeignet als Hauptwohnsitz oder Zweitwohnsitz; eine Ferienvermietung hängt von der örtlichen Lizenz ab, die wir prüfen.',
  'Подходит для постоянного проживания или как второй дом; сдача в краткосрочную аренду зависит от местной лицензии, которую мы проверяем.',
  'مناسبة للإقامة الدائمة أو كمنزل ثانٍ؛ ويتوقف التأجير السياحي على الترخيص المحلي، الذي نتحقق منه.',
  'Geschikt om er het hele jaar te wonen of als tweede woning; vakantieverhuur hangt af van de lokale vergunning, die wij controleren.',
  'Nadaje się do stałego zamieszkania lub jako drugi dom; wynajem wakacyjny zależy od lokalnej licencji, którą sprawdzamy.',
  'Passer for helårsbolig eller fritidsbolig; korttidsutleie avhenger av den lokale lisensen, som vi sjekker.',
  'Passar som permanent bostad eller fritidsbostad; korttidsuthyrning beror på den lokala licensen, som vi kontrollerar.')
a(91, 'The price list reports a favourable report on the building licence',
  'La lista de precios indica un informe favorable de la licencia de obras con la concesión pendiente. Confirmamos la concesión por escrito antes de que se mueva dinero.',
  'La liste de prix fait état d’un avis favorable sur le permis de construire, dont l’octroi est en attente. Nous confirmons l’octroi par écrit avant tout mouvement de fonds.',
  'Die Preisliste nennt ein positives Gutachten zur Baugenehmigung, die Erteilung steht aus. Wir bestätigen die Erteilung schriftlich, bevor Geld fließt.',
  'Прайс-лист сообщает о положительном заключении по разрешению на строительство, выдача которого ожидается. Мы письменно подтверждаем выдачу до перевода любых средств.',
  'تذكر قائمة الأسعار صدور تقرير إيجابي بشأن رخصة البناء مع بقاء منحها معلّقاً. ونؤكد المنح كتابياً قبل تحويل أي مبلغ.',
  'De prijslijst meldt een gunstig advies over de bouwvergunning, waarvan de verlening nog in behandeling is. Wij bevestigen de verlening schriftelijk voordat er geld wordt overgemaakt.',
  'Cennik podaje pozytywną opinię w sprawie pozwolenia na budowę, którego wydanie jest w toku. Potwierdzamy jego wydanie na piśmie, zanim zostaną przelane jakiekolwiek środki.',
  'Prislisten oppgir en positiv uttalelse om byggetillatelsen, som ennå ikke er gitt. Vi bekrefter tillatelsen skriftlig før penger overføres.',
  'Prislistan anger ett positivt yttrande om bygglovet, som ännu inte har beviljats. Vi bekräftar bygglovet skriftligt innan några pengar förs över.')
a(92, 'The contractor',
  'La constructora', 'L’entreprise générale', 'Das Bauunternehmen', 'Подрядчик', 'المقاول', 'De aannemer', 'Wykonawca', 'Entreprenøren', 'Entreprenören')
a(93, 'The tender is complete but the contractor is not yet chosen',
  'La licitación está completada, pero la constructora aún no se ha elegido. Preguntamos quién construirá las casas y cuándo empiezan las obras.',
  'L’appel d’offres est terminé, mais l’entreprise générale n’est pas encore choisie. Nous demandons qui construira les maisons et quand les travaux commencent.',
  'Die Ausschreibung ist abgeschlossen, das Bauunternehmen aber noch nicht ausgewählt. Wir fragen, wer die Häuser baut und wann die Arbeiten beginnen.',
  'Тендер завершён, но подрядчик ещё не выбран. Мы выясняем, кто будет строить дома и когда начнутся работы.',
  'اكتملت المناقصة لكن المقاول لم يُختر بعد. نسأل عن الجهة التي ستبني المنازل وموعد بدء الأعمال.',
  'De aanbesteding is afgerond, maar de aannemer is nog niet gekozen. Wij vragen wie de huizen bouwt en wanneer de werken beginnen.',
  'Przetarg jest zakończony, ale wykonawca nie został jeszcze wybrany. Pytamy, kto zbuduje domy i kiedy ruszą prace.',
  'Anbudet er avsluttet, men entreprenøren er ennå ikke valgt. Vi spør hvem som bygger husene og når arbeidene starter.',
  'Upphandlingen är avslutad, men entreprenören är ännu inte vald. Vi frågar vem som bygger husen och när arbetena börjar.')
a(94, 'The room count',
  'El número de estancias', 'Le nombre de pièces', 'Die Zimmerzahl', 'Число комнат', 'عدد الغرف', 'Het aantal kamers', 'Liczba pomieszczeń', 'Antall rom', 'Antalet rum')
a(96, 'Bank guarantee and VAT',
  'Aval bancario e IVA', 'Garantie bancaire et TVA', 'Bankbürgschaft und MwSt.', 'Банковская гарантия и НДС', 'الضمان المصرفي وضريبة القيمة المضافة',
  'Bankgarantie en btw', 'Gwarancja bankowa i VAT', 'Bankgaranti og mva', 'Bankgaranti och IVA (spansk moms)')
a(97, 'Payments made before completion must be covered by a bank guarantee',
  'Los pagos anteriores a la entrega deben estar cubiertos por un aval bancario, y la lista no indica el IVA. Confirmamos ambas cosas.',
  'Les versements effectués avant la livraison doivent être couverts par une garantie bancaire, et la liste ne mentionne pas la TVA. Nous confirmons les deux.',
  'Zahlungen vor der Übergabe müssen durch eine Bankbürgschaft gesichert sein, und die Liste nennt keine MwSt. Wir bestätigen beides.',
  'Платежи до сдачи должны быть покрыты банковской гарантией, а в прайс-листе НДС не указан. Мы подтверждаем и то, и другое.',
  'يجب أن تكون الدفعات المسددة قبل التسليم مغطاة بضمان مصرفي، والقائمة لا تذكر ضريبة القيمة المضافة. نؤكد الأمرين معاً.',
  'Betalingen vóór oplevering moeten gedekt zijn door een bankgarantie, en de lijst vermeldt geen btw. Wij bevestigen beide.',
  'Wpłaty przed odbiorem muszą być objęte gwarancją bankową, a cennik nie podaje VAT. Potwierdzamy jedno i drugie.',
  'Innbetalinger før overtakelse må være sikret med bankgaranti, og listen oppgir ikke mva. Vi bekrefter begge deler.',
  'Inbetalningar före tillträdet ska täckas av en bankgaranti, och listan anger inte IVA. Vi bekräftar båda.')

# ---------------------------------------------------------------- architecture
a(98, 'Contemporary, <em>open to the terraces</em>',
  'Contemporáneas, <em>abiertas a las terrazas</em>', 'Contemporaines, <em>ouvertes sur les terrasses</em>', 'Zeitgenössisch, <em>offen zu den Terrassen</em>',
  'Современные, <em>открытые на террасы</em>', 'معاصرة، <em>مفتوحة على التراسات</em>', 'Eigentijds, <em>open naar de terrassen</em>',
  'Nowoczesne, <em>otwarte na tarasy</em>', 'Moderne, <em>åpne mot terrassene</em>', 'Moderna, <em>öppna mot terrasserna</em>')
a(99, 'The specification describes a silk-grey façade',
  'La memoria de calidades describe una fachada gris seda, carpinterías de aluminio grafito y pérgolas de aluminio con efecto madera, con grandes huecos acristalados que abren los salones a las terrazas y las piscinas.',
  'Le descriptif prévoit une façade gris soie, des menuiseries en aluminium graphite et des pergolas en aluminium effet bois, avec de larges baies vitrées qui ouvrent les séjours sur les terrasses et les piscines.',
  'Die Baubeschreibung sieht eine seidengraue Fassade, Aluminiumrahmen in Graphit und Pergolen aus Aluminium in Holzoptik vor, mit großen Glasflächen von den Wohnräumen zu den Terrassen und Pools.',
  'Спецификация предусматривает фасад цвета серого шёлка, алюминиевые рамы цвета графит и алюминиевые перголы под дерево, а большие остеклённые проёмы открывают гостиные на террасы и бассейны.',
  'تصف المواصفات واجهة بلون الرمادي الحريري، وإطارات ألومنيوم بلون الغرافيت، وبرغولات من الألومنيوم بمظهر الخشب، مع فتحات زجاجية واسعة تفتح غرف المعيشة على التراسات والمسابح.',
  'De technische omschrijving noemt een zijdegrijze gevel, grafietkleurige aluminium kozijnen en pergola’s van aluminium in houtlook, met grote glaspartijen van de woonkamers naar de terrassen en zwembaden.',
  'Specyfikacja przewiduje elewację w kolorze jedwabistej szarości, grafitową stolarkę aluminiową i aluminiowe pergole imitujące drewno oraz duże przeszklenia otwierające salony na tarasy i baseny.',
  'Beskrivelsen angir en silkegrå fasade, grafittfargede aluminiumsrammer og pergolaer i aluminium med treimitasjon, med store glassflater fra stuene ut mot terrassene og bassengene.',
  'Byggbeskrivningen anger en sidengrå fasad, grafitfärgade aluminiumkarmar och pergolor i aluminium med träimitation, med stora glaspartier från vardagsrummen mot terrasserna och poolerna.')
a(100, 'Included finish',
  'Acabado incluido', 'Finition incluse', 'Inbegriffene Ausstattung', 'Включённая отделка', 'التشطيب المشمول',
  'Inbegrepen afwerking', 'Wykończenie w cenie', 'Inkludert standard', 'Ingående standard')
a(101, 'The Contemporary specification:',
  'La memoria Contemporary: suelos de porcelánico Keraben en el interior y en las terrazas, una isla de cocina con electrodomésticos Siemens y placa de inducción con extracción integrada.',
  'Le descriptif Contemporary : sols en grès cérame Keraben à l’intérieur et sur les terrasses, un îlot de cuisine avec électroménager Siemens et une plaque à induction à hotte intégrée.',
  'Die Ausstattungslinie Contemporary: Keraben-Feinsteinzeug innen und auf den Terrassen, eine Kücheninsel mit Siemens-Geräten und ein Induktionskochfeld mit integriertem Dunstabzug.',
  'Спецификация Contemporary: керамогранит Keraben в доме и на террасах, кухонный остров с техникой Siemens и индукционная панель со встроенной вытяжкой.',
  'مواصفات Contemporary: أرضيات من البورسلين Keraben في الداخل وعلى التراسات، وجزيرة مطبخ بأجهزة Siemens وموقد حثّي بشفاط مدمج.',
  'De Contemporary-afwerking: Keraben-tegelvloeren binnen en op de terrassen, een kookeiland met Siemens-apparatuur en een inductiekookplaat met geïntegreerde afzuiging.',
  'Standard Contemporary: posadzki z gresu Keraben wewnątrz i na tarasach, wyspa kuchenna ze sprzętem Siemens i płyta indukcyjna ze zintegrowanym okapem.',
  'Contemporary-standarden: Keraben-flis innendørs og på terrassene, en kjøkkenøy med Siemens-hvitevarer og en induksjonstopp med innebygd avtrekk.',
  'Contemporary-standarden: Keraben-klinker inomhus och på terrasserna, en köksö med vitvaror från Siemens och en induktionshäll med inbyggd fläkt.')
a(102, 'Thermal-break aluminium by Exlabesa',
  'Aluminio con rotura de puente térmico de Exlabesa o similar, con doble acristalamiento y vidrio bajo emisivo.',
  'Aluminium à rupture de pont thermique Exlabesa ou équivalent, avec double vitrage et verre à faible émissivité.',
  'Aluminium mit thermischer Trennung von Exlabesa oder gleichwertig, mit Doppelverglasung und Low-E-Glas.',
  'Алюминий с терморазрывом Exlabesa или аналог, двойное остекление с низкоэмиссионным стеклом.',
  'ألومنيوم بعازل حراري من Exlabesa أو ما يماثله، مع زجاج مزدوج منخفض الانبعاثية.',
  'Thermisch onderbroken aluminium van Exlabesa of gelijkwaardig, met dubbel glas en laag-emissieglas.',
  'Aluminium z przekładką termiczną Exlabesa lub równoważne, z podwójnym szkleniem i szkłem niskoemisyjnym.',
  'Aluminium med kuldebrudd fra Exlabesa eller tilsvarende, med tolags glass og lavemisjonsglass.',
  'Aluminium med köldbryggsbrytning från Exlabesa eller likvärdigt, med tvåglasfönster och lågemissionsglas.')
a(103, 'LG ducted air conditioning with Airzone',
  'Climatización por conductos LG con control por zonas Airzone, ventilación mecánica con recuperación de calor y suelo radiante eléctrico en los baños.',
  'Climatisation gainable LG avec régulation par zones Airzone, ventilation mécanique double flux et plancher chauffant électrique dans les salles de bains.',
  'Kanalklimaanlage von LG mit Airzone-Zonensteuerung, mechanische Lüftung mit Wärmerückgewinnung und elektrische Fußbodenheizung in den Bädern.',
  'Канальное кондиционирование LG с зонным управлением Airzone, механическая вентиляция с рекуперацией тепла и электрический тёплый пол в ванных комнатах.',
  'تكييف هواء بمجارٍ من LG مع تحكم بالمناطق من Airzone، وتهوية ميكانيكية باسترداد الحرارة، وتدفئة أرضية كهربائية في الحمامات.',
  'Kanaalairconditioning van LG met zoneregeling van Airzone, mechanische ventilatie met warmteterugwinning en elektrische vloerverwarming in de badkamers.',
  'Kanałowa klimatyzacja LG ze strefowym sterowaniem Airzone, wentylacja mechaniczna z odzyskiem ciepła i elektryczne ogrzewanie podłogowe w łazienkach.',
  'Kanalbasert klimaanlegg fra LG med sonestyring fra Airzone, balansert ventilasjon med varmegjenvinning og elektriske varmekabler i badene.',
  'Kanalbaserad luftkonditionering från LG med zonstyrning från Airzone, mekanisk ventilation med värmeåtervinning och elektrisk golvvärme i badrummen.')
a(104, 'Aerothermal hot water from a 210-litre Ariston',
  'Agua caliente por aerotermia con bomba de calor Ariston de 210 litros y preinstalación para la carga de vehículos eléctricos. Calificación del proyecto: B en consumo de energía y A en emisiones.',
  'Eau chaude par aérothermie avec une pompe à chaleur Ariston de 210 litres et une pré-installation pour la recharge de véhicules électriques. Classement du projet : B pour la consommation d’énergie et A pour les émissions.',
  'Warmwasser per Luftwärmepumpe von Ariston mit 210 Litern und eine Vorinstallation für das Laden von Elektroautos. Projektbewertung B beim Energieverbrauch und A bei den Emissionen.',
  'Горячая вода от аэротермального теплового насоса Ariston на 210 литров и подготовка для зарядки электромобиля. Рейтинг проекта: B по энергопотреблению и A по выбросам.',
  'مياه ساخنة بنظام الطاقة الهوائية من مضخة حرارية Ariston سعة 210 لترات، وتجهيز مسبق لشحن السيارات الكهربائية. تصنيف المشروع B لاستهلاك الطاقة وA للانبعاثات.',
  'Warm water via een Ariston-luchtwarmtepomp van 210 liter en een voorbereiding voor het laden van elektrische auto’s. Projectlabel B voor energieverbruik en A voor uitstoot.',
  'Ciepła woda z powietrznej pompy ciepła Ariston o pojemności 210 litrów i przygotowanie instalacji do ładowania samochodu elektrycznego. Klasa projektu B w zużyciu energii i A w emisjach.',
  'Varmtvann fra en Ariston luft-til-vann-varmepumpe på 210 liter og forberedelse for lading av elbil. Prosjektets energimerking er B for energibruk og A for utslipp.',
  'Varmvatten från en Ariston luftvärmepump på 210 liter och förberedelse för laddning av elbil. Projektets klassning är B för energianvändning och A för utsläpp.')
a(105, 'Each villa is drawn with an infinity-edge pool in reinforced concrete',
  'Cada villa se proyecta con una piscina de borde infinito de hormigón armado, revestida de gresite color arena y con cloración salina.',
  'Chaque villa est dessinée avec une piscine à débordement en béton armé, revêtue de mosaïque couleur sable, avec électrolyse au sel.',
  'Jede Villa ist mit einem Infinity-Pool aus Stahlbeton geplant, mit sandfarbenem Mosaik ausgekleidet und mit Salzelektrolyse.',
  'Для каждой виллы предусмотрен бассейн-инфинити из железобетона с отделкой мозаикой песочного цвета и солевым хлорированием.',
  'تتضمن مخططات كل فيلا مسبحاً بحافة لا متناهية من الخرسانة المسلحة، مكسواً بفسيفساء بلون الرمل، مع تعقيم بالملح.',
  'Elke villa is getekend met een infinityzwembad in gewapend beton, bekleed met zandkleurig mozaïek en met zoutelektrolyse.',
  'Każda willa ma w projekcie basen typu infinity z żelbetu, wyłożony mozaiką w kolorze piasku, z elektrolizą solną.',
  'Hver villa er tegnet med et infinitybasseng i armert betong, kledd med sandfarget mosaikk og med saltklorering.',
  'Varje villa är ritad med en infinitypool i armerad betong, klädd med sandfärgad mosaik och med saltklorering.')
a(106, 'Options',
  'Opciones', 'Options', 'Optionen', 'Опции', 'الخيارات', 'Opties', 'Opcje', 'Tilvalg', 'Tillval')
a(107, 'At extra cost:',
  'Con coste adicional: sótano, bodega, gimnasio, sauna, sala de cine, simulador de golf, terraza en cubierta, cocina exterior, climatización de la piscina, domótica, placas solares y ascensor donde sea viable.',
  'Avec supplément : sous-sol, cave à vin, salle de sport, sauna, salle de cinéma, simulateur de golf, toit-terrasse, cuisine extérieure, chauffage de la piscine, domotique, panneaux solaires et ascenseur lorsque c’est faisable.',
  'Gegen Aufpreis: Untergeschoss, Weinkeller, Fitnessraum, Sauna, Heimkino, Golfsimulator, Dachterrasse, Außenküche, Poolheizung, Hausautomation, Solarpaneele und ein Aufzug, wo baulich möglich.',
  'За дополнительную плату: подвальный этаж, винный погреб, спортзал, сауна, домашний кинотеатр, гольф-симулятор, терраса на крыше, летняя кухня, подогрев бассейна, система «умный дом», солнечные панели и лифт там, где это возможно.',
  'بتكلفة إضافية: قبو، وقبو للنبيذ، وصالة رياضية، وساونا، وسينما منزلية، وجهاز محاكاة غولف، وتراس على السطح، ومطبخ خارجي، وتدفئة للمسبح، وأتمتة منزلية، وألواح شمسية، ومصعد حيثما أمكن.',
  'Tegen meerprijs: een kelder, wijnkelder, fitnessruimte, sauna, thuisbioscoop, golfsimulator, dakterras, buitenkeuken, zwembadverwarming, domotica, zonnepanelen en een lift waar mogelijk.',
  'Za dopłatą: piwnica, piwniczka na wino, siłownia, sauna, kino domowe, symulator golfa, taras na dachu, kuchnia zewnętrzna, podgrzewanie basenu, automatyka domowa, panele słoneczne i winda tam, gdzie to możliwe.',
  'Mot tillegg: kjeller, vinkjeller, treningsrom, badstue, hjemmekino, golfsimulator, takterrasse, utekjøkken, bassengoppvarming, smarthus, solcellepaneler og heis der det er mulig.',
  'Mot tillägg: källare, vinkällare, gym, bastu, hemmabio, golfsimulator, takterrass, utekök, poolvärme, hemautomation, solpaneler och hiss där det är möjligt.')

# ---------------------------------------------------------------- lifestyle and viewing
a(108, 'Valle Romano, <em>on the golf course</em>',
  'Valle Romano, <em>en el campo de golf</em>', 'Valle Romano, <em>sur le golf</em>', 'Valle Romano, <em>am Golfplatz</em>',
  'Валле-Романо, <em>у гольф-поля</em>', 'فايي رومانو، <em>على ملعب الغولف</em>', 'Valle Romano, <em>aan de golfbaan</em>',
  'Valle Romano, <em>przy polu golfowym</em>', 'Valle Romano, <em>ved golfbanen</em>', 'Valle Romano, <em>vid golfbanan</em>')
a(109, 'Valle Romano is a golf resort on the western edge of Estepona, inland from the coast.',
  'Valle Romano es un resort de golf en el extremo oeste de Estepona, hacia el interior desde la costa.',
  'Valle Romano est un domaine de golf à l’extrémité ouest d’Estepona, dans les terres en retrait de la côte.',
  'Valle Romano ist ein Golfresort am westlichen Rand von Estepona, landeinwärts von der Küste.',
  'Валле-Романо — гольф-курорт на западной окраине Эстепоны, в глубине от побережья.',
  'فايي رومانو منتجع غولف على الطرف الغربي من إستيبونا، في الداخل بعيداً عن الساحل.',
  'Valle Romano is een golfresort aan de westrand van Estepona, landinwaarts van de kust.',
  'Valle Romano to kurort golfowy na zachodnim skraju Estepony, w głębi lądu od wybrzeża.',
  'Valle Romano er et golfanlegg i vestkanten av Estepona, et stykke inn i landet fra kysten.',
  'Valle Romano är en golfanläggning i västra utkanten av Estepona, en bit in i landet från kusten.')
a(110, 'The 18-hole, par 71 course',
  'El recorrido de 18 hoyos y par 71 lo diseñó Cabell B. Robinson y ha acogido pruebas del Challenge Tour y la Escuela de Clasificación del European Tour.',
  'Le parcours de 18 trous, par 71, a été dessiné par Cabell B. Robinson et a accueilli le Challenge Tour et les cartes de qualification de l’European Tour.',
  'Der 18-Loch-Platz mit Par 71 wurde von Cabell B. Robinson entworfen und war Austragungsort der Challenge Tour und der Qualifying School der European Tour.',
  'Поле на 18 лунок, пар 71, спроектировал Кейбелл Б. Робинсон; здесь проходили турниры Challenge Tour и квалификационная школа European Tour.',
  'صمّم الملعب ذا الثماني عشرة حفرة وبار 71 كابيل ب. روبنسون، واستضاف بطولة Challenge Tour ومدرسة التأهيل التابعة لـ European Tour.',
  'De 18-holesbaan met par 71 is ontworpen door Cabell B. Robinson en was gastheer van de Challenge Tour en de Qualifying School van de European Tour.',
  'Pole na 18 dołków, par 71, zaprojektował Cabell B. Robinson; odbywały się tu turnieje Challenge Tour i szkoła kwalifikacyjna European Tour.',
  'Den 18-hulls banen med par 71 er tegnet av Cabell B. Robinson og har vært vertskap for Challenge Tour og European Tours kvalifiseringsskole.',
  'Den 18-håls banan med par 71 är ritad av Cabell B. Robinson och har varit värd för Challenge Tour och European Tours kvalificeringsskola.')
a(111, 'Schools',
  'Colegios', 'Écoles', 'Schulen', 'Школы', 'المدارس', 'Scholen', 'Szkoły', 'Skoler', 'Skolor')
a(112, 'The catalogue names Atalaya',
  'El catálogo menciona Atalaya, en Estepona; Swans, en Marbella, y Sotogrande International School.',
  'Le catalogue cite Atalaya à Estepona, Swans à Marbella et Sotogrande International School.',
  'Der Katalog nennt Atalaya in Estepona, Swans in Marbella und die Sotogrande International School.',
  'Каталог называет школу Atalaya в Эстепоне, Swans в Марбелье и Sotogrande International School.',
  'يذكر الكتالوج مدرسة Atalaya في إستيبونا، وSwans في ماربيا، وSotogrande International School.',
  'De catalogus noemt Atalaya in Estepona, Swans in Marbella en Sotogrande International School.',
  'Katalog wymienia Atalaya w Esteponie, Swans w Marbelli i Sotogrande International School.',
  'Katalogen nevner Atalaya i Estepona, Swans i Marbella og Sotogrande International School.',
  'Katalogen nämner Atalaya i Estepona, Swans i Marbella och Sotogrande International School.')
a(113, 'By the catalogue\'s figures, Sotogrande and Puerto Banús',
  'Según las cifras del catálogo, Sotogrande y Puerto Banús quedan a unos 25 minutos, Marbella a unos 30, el aeropuerto de Gibraltar a unos 40 y el de Málaga a unos 55.',
  'Selon les chiffres du catalogue, Sotogrande et Puerto Banús sont à environ 25 minutes, Marbella à environ 30, l’aéroport de Gibraltar à environ 40 et celui de Málaga à environ 55.',
  'Nach den Angaben des Katalogs liegen Sotogrande und Puerto Banús etwa 25 Minuten entfernt, Marbella etwa 30, der Flughafen Gibraltar etwa 40 und der Flughafen Málaga etwa 55.',
  'По данным каталога, до Сотогранде и Пуэрто-Бануса около 25 минут, до Марбельи около 30, до аэропорта Гибралтара около 40, до аэропорта Малаги около 55.',
  'وفق أرقام الكتالوج، تبعد سوتوغراندي وبويرتو بانوس نحو 25 دقيقة، وماربيا نحو 30، ومطار جبل طارق نحو 40، ومطار مالقة نحو 55.',
  'Volgens de catalogus liggen Sotogrande en Puerto Banús op ongeveer 25 minuten, Marbella op ongeveer 30, de luchthaven van Gibraltar op ongeveer 40 en die van Málaga op ongeveer 55.',
  'Według katalogu do Sotogrande i Puerto Banús jest około 25 minut, do Marbelli około 30, na lotnisko w Gibraltarze około 40, a na lotnisko w Maladze około 55.',
  'Etter katalogens tall ligger Sotogrande og Puerto Banús rundt 25 minutter unna, Marbella rundt 30, flyplassen i Gibraltar rundt 40 og flyplassen i Málaga rundt 55.',
  'Enligt katalogens siffror ligger Sotogrande och Puerto Banús cirka 25 minuter bort, Marbella cirka 30, flygplatsen i Gibraltar cirka 40 och flygplatsen i Málaga cirka 55.')
a(114, 'Eight plots on a slope do not share',
  'Ocho parcelas en pendiente no comparten la misma vista ni la misma orientación. La forma más rápida de distinguirlas es pisarlas.',
  'Huit parcelles en pente n’ont ni la même vue ni la même orientation. Le moyen le plus rapide de les distinguer est de s’y rendre.',
  'Acht Grundstücke am Hang haben weder denselben Ausblick noch dieselbe Ausrichtung. Am schnellsten erkennen Sie den Unterschied vor Ort.',
  'Восемь участков на склоне различаются и видом, и ориентацией. Быстрее всего понять разницу — побывав на них.',
  'لا تتشارك ثماني قطع أرض على منحدر الإطلالة نفسها ولا الاتجاه نفسه. وأسرع طريقة للتمييز بينها هي الوقوف عليها.',
  'Acht percelen op een helling hebben niet hetzelfde uitzicht en niet dezelfde ligging. De snelste manier om ze te onderscheiden is erop te staan.',
  'Osiem działek na zboczu nie ma tego samego widoku ani tej samej ekspozycji. Najszybciej odróżnią je Państwo, stając na miejscu.',
  'Åtte tomter i en skråning har verken samme utsikt eller samme retning. Den raskeste måten å skille dem på er å stå på dem.',
  'Åtta tomter i en sluttning har varken samma utsikt eller samma väderstreck. Det snabbaste sättet att skilja dem åt är att stå på dem.')
a(115, 'Walk the plots and see how each one sits',
  'Recorra las parcelas y vea cómo se asienta cada una en la pendiente y frente al campo.',
  'Parcourez les parcelles et voyez comment chacune s’inscrit dans la pente et face au parcours.',
  'Gehen Sie die Grundstücke ab und sehen Sie, wie jedes am Hang und zum Platz liegt.',
  'Пройдите по участкам и посмотрите, как каждый расположен на склоне и относительно поля.',
  'تجوّلوا في قطع الأرض وانظروا كيف تقع كل منها على المنحدر وبالنسبة إلى الملعب.',
  'Loop de percelen af en zie hoe elk ervan op de helling en ten opzichte van de baan ligt.',
  'Proszę obejść działki i zobaczyć, jak każda z nich leży na zboczu i względem pola.',
  'Gå over tomtene og se hvordan hver av dem ligger i skråningen og mot banen.',
  'Gå runt på tomterna och se hur var och en ligger i sluttningen och mot banan.')
a(116, 'Compare the south-west, north-west and south-east plots',
  'Compare las parcelas al suroeste, al noroeste y al sureste a la hora del día en que usaría la terraza.',
  'Comparez les parcelles orientées sud-ouest, nord-ouest et sud-est à l’heure où vous profiteriez de la terrasse.',
  'Vergleichen Sie die Grundstücke nach Südwesten, Nordwesten und Südosten zu der Tageszeit, zu der Sie die Terrasse nutzen würden.',
  'Сравните участки с ориентацией на юго-запад, северо-запад и юго-восток в то время дня, когда вы пользовались бы террасой.',
  'قارنوا قطع الأرض المتجهة إلى الجنوب الغربي والشمال الغربي والجنوب الشرقي في الوقت الذي تستخدمون فيه التراس.',
  'Vergelijk de percelen op het zuidwesten, noordwesten en zuidoosten op het moment van de dag waarop u het terras zou gebruiken.',
  'Proszę porównać działki z ekspozycją południowo-zachodnią, północno-zachodnią i południowo-wschodnią o tej porze dnia, o której korzystaliby Państwo z tarasu.',
  'Sammenlign tomtene mot sørvest, nordvest og sørøst på det tidspunktet av dagen du ville brukt terrassen.',
  'Jämför tomterna mot sydväst, nordväst och sydost vid den tid på dagen då ni skulle använda terrassen.')
a(117, 'See the access from the road',
  'Vea el acceso desde la calle, dónde queda el aparcamiento y cómo se une la planta de entrada con la calle.',
  'Voyez l’accès depuis la route, l’emplacement du stationnement et la façon dont le niveau d’entrée rejoint la rue.',
  'Sehen Sie die Zufahrt von der Straße, wo die Stellplätze liegen und wie die Eingangsebene an die Straße anschließt.',
  'Посмотрите подъезд с дороги, где расположена парковка и как входной этаж выходит на улицу.',
  'شاهدوا المدخل من الطريق، وموقع موقف السيارات، وكيف يلتقي طابق المدخل بالشارع.',
  'Bekijk de toegang vanaf de weg, waar het parkeren ligt en hoe de entreeverdieping op de straat aansluit.',
  'Proszę zobaczyć dojazd od drogi, położenie miejsc postojowych i to, jak kondygnacja wejściowa łączy się z ulicą.',
  'Se adkomsten fra veien, hvor parkeringen ligger og hvordan inngangsetasjen møter gaten.',
  'Se tillfarten från vägen, var parkeringen ligger och hur entréplanet möter gatan.')
a(118, 'A golf resort on the western edge of Estepona',
  'Un resort de golf en el extremo oeste de Estepona, hacia el interior desde la costa. El promotor solo indica tiempos en coche, y la posición en el mapa es aproximada, tomada del plano de situación del catálogo.',
  'Un domaine de golf à l’extrémité ouest d’Estepona, dans les terres en retrait de la côte. Le promoteur ne donne que des temps de trajet en voiture, et la position sur la carte est approximative, reprise de la carte de situation du catalogue.',
  'Ein Golfresort am westlichen Rand von Estepona, landeinwärts von der Küste. Der Bauträger nennt nur Fahrzeiten, und die Position auf der Karte ist ungefähr, übernommen aus dem Lageplan des Katalogs.',
  'Гольф-курорт на западной окраине Эстепоны, в глубине от побережья. Застройщик приводит только время в пути на машине, а положение на карте приблизительное, по карте расположения из каталога.',
  'منتجع غولف على الطرف الغربي من إستيبونا، في الداخل بعيداً عن الساحل. لا يذكر المطوّر سوى أوقات القيادة، والموقع على الخريطة تقريبي، مأخوذ من خريطة الموقع في الكتالوج.',
  'Een golfresort aan de westrand van Estepona, landinwaarts van de kust. De ontwikkelaar geeft alleen rijtijden, en de positie op de kaart is bij benadering, overgenomen van de situatiekaart in de catalogus.',
  'Kurort golfowy na zachodnim skraju Estepony, w głębi lądu od wybrzeża. Deweloper podaje tylko czasy dojazdu samochodem, a położenie na mapie jest przybliżone, przeniesione z mapy lokalizacji w katalogu.',
  'Et golfanlegg i vestkanten av Estepona, et stykke inn i landet fra kysten. Utbyggeren oppgir bare kjøretider, og plasseringen på kartet er omtrentlig, hentet fra kartet i katalogen.',
  'En golfanläggning i västra utkanten av Estepona, en bit in i landet från kusten. Exploatören anger bara körtider, och placeringen på kartan är ungefärlig, hämtad från lägeskartan i katalogen.')

# ---------------------------------------------------------------- faq
a(119, 'From €1,295,000 to €2,100,000 on the developer',
  'De {E1295000} a {E2100000} según la lista de precios del promotor de octubre de 2026: {E1295000} las villas 1 y 2, {E1495000} las villas 3 a 5, {E1590000} las villas 6 y 7 y {E2100000} la villa 8.',
  'De {E1295000} à {E2100000} selon la liste de prix du promoteur d’octobre 2026 : {E1295000} pour les villas 1 et 2, {E1495000} pour les villas 3 à 5, {E1590000} pour les villas 6 et 7 et {E2100000} pour la villa 8.',
  'Von {E1295000} bis {E2100000} laut der Preisliste des Bauträgers vom Oktober 2026: {E1295000} für die Villen 1 und 2, {E1495000} für die Villen 3 bis 5, {E1590000} für die Villen 6 und 7 und {E2100000} für Villa 8.',
  'От {E1295000} до {E2100000} по прайс-листу застройщика за октябрь 2026 года: {E1295000} за виллы 1 и 2, {E1495000} за виллы 3–5, {E1590000} за виллы 6 и 7 и {E2100000} за виллу 8.',
  'من {E1295000} إلى {E2100000} وفق قائمة أسعار المطوّر لشهر أكتوبر 2026: {E1295000} للفيلتين 1 و2، و{E1495000} للفلل من 3 إلى 5، و{E1590000} للفيلتين 6 و7، و{E2100000} للفيلا 8.',
  'Van {E1295000} tot {E2100000} volgens de prijslijst van de ontwikkelaar van oktober 2026: {E1295000} voor villa 1 en 2, {E1495000} voor villa 3 tot 5, {E1590000} voor villa 6 en 7 en {E2100000} voor villa 8.',
  'Od {E1295000} do {E2100000} według cennika dewelopera z października 2026 roku: {E1295000} za wille 1 i 2, {E1495000} za wille 3–5, {E1590000} za wille 6 i 7 oraz {E2100000} za willę 8.',
  'Fra {E1295000} til {E2100000} ifølge utbyggerens prisliste fra oktober 2026: {E1295000} for villa 1 og 2, {E1495000} for villa 3 til 5, {E1590000} for villa 6 og 7 og {E2100000} for villa 8.',
  'Från {E1295000} till {E2100000} enligt exploatörens prislista från oktober 2026: {E1295000} för villa 1 och 2, {E1495000} för villa 3 till 5, {E1590000} för villa 6 och 7 och {E2100000} för villa 8.')
a(120, 'The price list does not say. On a new-build villa',
  'La lista de precios no lo indica. En una villa de obra nueva en España el IVA del {P10} se suma al precio de compra; confirmamos por escrito cuál se aplica antes de que reserve.',
  'La liste de prix ne le précise pas. Sur une villa neuve en Espagne, la TVA de {P10} s’ajoute au prix d’achat ; nous confirmons par écrit ce qui s’applique avant votre réservation.',
  'Die Preisliste sagt es nicht. Bei einer neu gebauten Villa in Spanien kommen {P10} MwSt. auf den Kaufpreis; wir bestätigen schriftlich, was gilt, bevor Sie reservieren.',
  'В прайс-листе это не указано. При покупке новой виллы в Испании к цене добавляется НДС {P10}; мы письменно подтверждаем, что применяется, до вашего бронирования.',
  'لا تذكر قائمة الأسعار ذلك. في الفيلا الجديدة في إسبانيا تُضاف ضريبة القيمة المضافة بنسبة {P10} إلى سعر الشراء، ونؤكد كتابياً ما ينطبق قبل أن تحجزوا.',
  'De prijslijst vermeldt het niet. Bij een nieuwbouwvilla in Spanje komt {P10} btw bovenop de koopprijs; wij bevestigen schriftelijk wat van toepassing is voordat u reserveert.',
  'Cennik tego nie podaje. Przy nowo wybudowanej willi w Hiszpanii do ceny zakupu dolicza się {P10} VAT; potwierdzamy na piśmie, co obowiązuje, zanim dokonają Państwo rezerwacji.',
  'Prislisten sier det ikke. På en nybygd villa i Spania kommer {P10} mva i tillegg til kjøpesummen; vi bekrefter skriftlig hva som gjelder før du reserverer.',
  'Prislistan anger det inte. På en nybyggd villa i Spanien läggs IVA (spansk moms) om {P10} på köpeskillingen; vi bekräftar skriftligt vad som gäller innan ni bokar.')
a(121, '€10,000 on reservation, deducted from the first payment',
  '{E10000} en la reserva, descontados del primer pago; {P20} a la firma del contrato de compraventa, {P20} al terminar la estructura y {P60} en la escritura.',
  '{E10000} à la réservation, déduits du premier versement ; {P20} à la signature du contrat de vente, {P20} à l’achèvement du gros œuvre et {P60} à l’acte notarié.',
  '{E10000} bei Reservierung, angerechnet auf die erste Zahlung; {P20} bei Unterzeichnung des Kaufvertrags, {P20} nach Fertigstellung des Rohbaus und {P60} bei der notariellen Urkunde.',
  '{E10000} при бронировании, засчитываются в первый платёж; {P20} при подписании договора купли-продажи, {P20} по завершении каркаса и {P60} при подписании купчей.',
  '{E10000} عند الحجز تُخصم من الدفعة الأولى؛ و{P20} عند توقيع عقد البيع، و{P20} عند اكتمال الهيكل، و{P60} عند توقيع سند الملكية.',
  '{E10000} bij reservering, in mindering op de eerste betaling; {P20} bij ondertekening van de koopovereenkomst, {P20} bij voltooiing van de ruwbouw en {P60} bij de notariële akte.',
  '{E10000} przy rezerwacji, zaliczane na poczet pierwszej wpłaty; {P20} przy podpisaniu umowy kupna, {P20} po ukończeniu konstrukcji i {P60} przy akcie notarialnym.',
  '{E10000} ved reservasjon, som trekkes fra første innbetaling; {P20} ved signering av kjøpekontrakten, {P20} når råbygget er ferdig og {P60} ved skjøtet.',
  '{E10000} vid bokning, som avräknas från den första betalningen; {P20} vid undertecknandet av köpekontraktet, {P20} när stommen är klar och {P60} vid lagfarten.')
a(122, 'The price list reports a favourable report with the grant still pending',
  'La lista de precios indica un informe favorable con la concesión aún pendiente. Nueva Living confirma la concesión por escrito antes de que se mueva dinero.',
  'La liste de prix fait état d’un avis favorable, l’octroi restant en attente. Nueva Living confirme l’octroi par écrit avant tout mouvement de fonds.',
  'Die Preisliste nennt ein positives Gutachten, die Erteilung steht noch aus. Nueva Living bestätigt die Erteilung schriftlich, bevor Geld fließt.',
  'Прайс-лист сообщает о положительном заключении, выдача разрешения ещё ожидается. Nueva Living письменно подтверждает выдачу до перевода любых средств.',
  'تذكر قائمة الأسعار صدور تقرير إيجابي مع بقاء المنح معلّقاً. وتؤكد Nueva Living المنح كتابياً قبل تحويل أي مبلغ.',
  'De prijslijst meldt een gunstig advies, terwijl de verlening nog in behandeling is. Nueva Living bevestigt de verlening schriftelijk voordat er geld wordt overgemaakt.',
  'Cennik podaje pozytywną opinię, a wydanie pozwolenia wciąż jest w toku. Nueva Living potwierdza jego wydanie na piśmie, zanim zostaną przelane jakiekolwiek środki.',
  'Prislisten oppgir en positiv uttalelse, mens selve tillatelsen ennå ikke er gitt. Nueva Living bekrefter tillatelsen skriftlig før penger overføres.',
  'Prislistan anger ett positivt yttrande, medan beviljandet fortfarande dröjer. Nueva Living bekräftar bygglovet skriftligt innan några pengar förs över.')
a(123, 'Completion is expected in Q4 2028.',
  'La finalización está prevista para el {Q}. La licitación de obra está completada y la constructora aún no se ha elegido; la fecha que rige es la del contrato de compraventa.',
  'L’achèvement est prévu au {Q}. L’appel d’offres des travaux est terminé et l’entreprise générale n’est pas encore choisie ; la date qui fait foi est celle du contrat de vente.',
  'Die Fertigstellung ist für {Q} vorgesehen. Die Bauausschreibung ist abgeschlossen, das Bauunternehmen noch nicht ausgewählt; maßgeblich ist das Datum im Kaufvertrag.',
  'Завершение ожидается в {Q}. Тендер на строительные работы завершён, подрядчик ещё не выбран; определяющей является дата в договоре купли-продажи.',
  'يُتوقع الإنجاز في {Q}. اكتملت مناقصة الأعمال ولم يُختر المقاول بعد، والتاريخ المعتمد هو الوارد في عقد البيع.',
  'De oplevering wordt verwacht in {Q}. De aanbesteding van de bouw is afgerond en de aannemer is nog niet gekozen; de datum in de koopovereenkomst is bepalend.',
  'Zakończenie przewidziane jest na {Q}. Przetarg na roboty jest zakończony, a wykonawca nie został jeszcze wybrany; wiążąca jest data w umowie kupna.',
  'Ferdigstillelse er ventet i {Q}. Anbudet for byggearbeidene er avsluttet og entreprenøren ennå ikke valgt; det er datoen i kjøpekontrakten som gjelder.',
  'Färdigställandet väntas {Q}. Upphandlingen av byggarbetena är avslutad och entreprenören ännu inte vald; det är datumet i köpekontraktet som gäller.')
a(124, 'How many bedrooms do the villas have?',
  '¿Cuántos dormitorios tienen las villas?', 'Combien de chambres comptent les villas ?', 'Wie viele Schlafzimmer haben die Villen?',
  'Сколько спален в виллах?', 'كم عدد غرف النوم في الفلل؟', 'Hoeveel slaapkamers hebben de villa’s?',
  'Ile sypialni mają wille?', 'Hvor mange soverom har villaene?', 'Hur många sovrum har villorna?')
a(126, 'From 122 to 433 sqm of interior',
  'De 122 a 433 {U} interiores y de 279 a 604 {U} construidos en total, en parcelas de 400 a {G1002} {U}.',
  'De 122 à 433 {U} intérieurs et de 279 à 604 {U} construits au total, sur des parcelles de 400 à {G1002} {U}.',
  'Von 122 bis 433 {U} Innenfläche und insgesamt 279 bis 604 {U} bebaut, auf Grundstücken von 400 bis {G1002} {U}.',
  'От 122 до 433 {U} внутренней площади и от 279 до 604 {U} общей застройки, на участках от 400 до {G1002} {U}.',
  'من 122 إلى 433 {U} من المساحة الداخلية، ومن 279 إلى 604 {U} مبنية إجمالاً، على قطع أرض من 400 إلى {G1002} {U}.',
  'Van 122 tot 433 {U} binnenoppervlak en in totaal 279 tot 604 {U} bebouwd, op percelen van 400 tot {G1002} {U}.',
  'Od 122 do 433 {U} powierzchni wewnętrznej i łącznie od 279 do 604 {U} zabudowy, na działkach od 400 do {G1002} {U}.',
  'Fra 122 til 433 {U} innvendig og totalt 279 til 604 {U} bebygd, på tomter på 400 til {G1002} {U}.',
  'Från 122 till 433 {U} inneryta och totalt 279 till 604 {U} byggyta, på tomter om 400 till {G1002} {U}.')
a(127, 'What is included and what is optional?',
  '¿Qué está incluido y qué es opcional?', 'Qu’est-ce qui est inclus et qu’est-ce qui est en option ?', 'Was ist enthalten und was ist optional?',
  'Что входит в цену, а что — опции?', 'ما المشمول وما الاختياري؟', 'Wat is inbegrepen en wat is optioneel?',
  'Co jest w cenie, a co jest opcją?', 'Hva er inkludert, og hva er tilvalg?', 'Vad ingår och vad är tillval?')
a(128, 'The Contemporary specification is included,',
  'Se incluye la memoria Contemporary, con climatización, ventilación con recuperación de calor, agua caliente por aerotermia y la piscina. El sótano, la bodega, el gimnasio, la sauna, la sala de cine, la terraza en cubierta, la cocina exterior, la climatización de la piscina, la domótica, las placas solares y el ascensor son opciones de pago; el jardín se entrega con tierra vegetal.',
  'Le descriptif Contemporary est inclus, avec la climatisation, la ventilation double flux, l’eau chaude par aérothermie et la piscine. Le sous-sol, la cave, la salle de sport, le sauna, la salle de cinéma, le toit-terrasse, la cuisine extérieure, le chauffage de la piscine, la domotique, les panneaux solaires et l’ascenseur sont des options payantes ; le jardin est livré en terre végétale.',
  'Enthalten ist die Ausstattungslinie Contemporary mit Klimaanlage, Lüftung mit Wärmerückgewinnung, Warmwasser per Luftwärmepumpe und dem Pool. Untergeschoss, Keller, Fitnessraum, Sauna, Heimkino, Dachterrasse, Außenküche, Poolheizung, Hausautomation, Solarpaneele und Aufzug sind kostenpflichtige Optionen; der Garten wird mit Mutterboden übergeben.',
  'В цену входит спецификация Contemporary: кондиционирование, вентиляция с рекуперацией тепла, аэротермальное горячее водоснабжение и бассейн. Подвальный этаж, погреб, спортзал, сауна, кинотеатр, терраса на крыше, летняя кухня, подогрев бассейна, «умный дом», солнечные панели и лифт — платные опции; сад передаётся с растительным грунтом.',
  'تشمل الأسعار مواصفات Contemporary، مع تكييف الهواء والتهوية باسترداد الحرارة والمياه الساخنة بالطاقة الهوائية والمسبح. أما القبو وقبو النبيذ والصالة الرياضية والساونا والسينما والتراس على السطح والمطبخ الخارجي وتدفئة المسبح والأتمتة المنزلية والألواح الشمسية والمصعد فخيارات مدفوعة، وتُسلَّم الحديقة بتربة زراعية.',
  'De Contemporary-afwerking is inbegrepen, met airconditioning, ventilatie met warmteterugwinning, warm water via een luchtwarmtepomp en het zwembad. Een kelder, wijnkelder, fitnessruimte, sauna, thuisbioscoop, dakterras, buitenkeuken, zwembadverwarming, domotica, zonnepanelen en een lift zijn betaalde opties; de tuin wordt opgeleverd met teelaarde.',
  'W cenie jest standard Contemporary z klimatyzacją, wentylacją z odzyskiem ciepła, ciepłą wodą z pompy ciepła i basenem. Piwnica, piwniczka na wino, siłownia, sauna, kino domowe, taras na dachu, kuchnia zewnętrzna, podgrzewanie basenu, automatyka domowa, panele słoneczne i winda to płatne opcje; ogród jest przekazywany z warstwą ziemi urodzajnej.',
  'Contemporary-standarden er inkludert, med klimaanlegg, ventilasjon med varmegjenvinning, varmtvann fra varmepumpe og bassenget. Kjeller, vinkjeller, treningsrom, badstue, hjemmekino, takterrasse, utekjøkken, bassengoppvarming, smarthus, solcellepaneler og heis er tilvalg mot betaling; hagen leveres med matjord.',
  'Contemporary-standarden ingår, med luftkonditionering, ventilation med värmeåtervinning, varmvatten från luftvärmepump och poolen. Källare, vinkällare, gym, bastu, hemmabio, takterrass, utekök, poolvärme, hemautomation, solpaneler och hiss är tillval mot betalning; trädgården lämnas med matjord.')

# ---------------------------------------------------------------- timeline, enquiry, seo
a(129, 'The price list, the plans, the specification and the payment terms.',
  'La lista de precios, los planos, la memoria de calidades y la forma de pago.',
  'La liste de prix, les plans, le descriptif et les conditions de paiement.',
  'Die Preisliste, die Pläne, die Baubeschreibung und die Zahlungsbedingungen.',
  'Прайс-лист, планировки, спецификация и условия оплаты.',
  'قائمة الأسعار والمخططات والمواصفات وشروط الدفع.',
  'De prijslijst, de plattegronden, de technische omschrijving en de betalingsvoorwaarden.',
  'Cennik, rzuty, specyfikacja i warunki płatności.',
  'Prislisten, tegningene, beskrivelsen og betalingsvilkårene.',
  'Prislistan, ritningarna, byggbeskrivningen och betalningsvillkoren.')
a(130, 'Type, orientation and plot size differ',
  'La tipología, la orientación y el tamaño de la parcela cambian de una villa a otra; las comparamos una junto a otra.',
  'Le type, l’orientation et la taille de la parcelle diffèrent d’une villa à l’autre ; nous les comparons côte à côte.',
  'Typ, Ausrichtung und Grundstücksgröße unterscheiden sich von Villa zu Villa; wir stellen sie nebeneinander.',
  'Тип, ориентация и размер участка у вилл разные; мы сравниваем их бок о бок.',
  'يختلف النمط والاتجاه ومساحة قطعة الأرض من فيلا إلى أخرى، ونضعها جنباً إلى جنب.',
  'Type, ligging en perceelgrootte verschillen per villa; wij zetten ze naast elkaar.',
  'Typ, ekspozycja i wielkość działki różnią się w zależności od willi; zestawiamy je obok siebie.',
  'Type, retning og tomtestørrelse varierer fra villa til villa; vi stiller dem opp side om side.',
  'Typ, väderstreck och tomtstorlek skiljer sig från villa till villa; vi ställer dem sida vid sida.')
a(131, 'Licence, guarantee, VAT and contract drawings',
  'Licencia, aval, IVA y planos del contrato revisados antes de firmar.',
  'Permis, garantie, TVA et plans contractuels vérifiés avant la signature.',
  'Genehmigung, Bürgschaft, MwSt. und Vertragspläne geprüft, bevor Sie unterschreiben.',
  'Разрешение, гарантия, НДС и планы к договору проверены до подписания.',
  'مراجعة الرخصة والضمان وضريبة القيمة المضافة ومخططات العقد قبل التوقيع.',
  'Vergunning, garantie, btw en contracttekeningen gecontroleerd voordat u tekent.',
  'Pozwolenie, gwarancja, VAT i rysunki do umowy sprawdzone przed podpisaniem.',
  'Tillatelse, garanti, mva og kontraktstegninger gjennomgått før du signerer.',
  'Bygglov, garanti, IVA och kontraktsritningar granskade innan ni skriver under.')
a(132, 'I would like to receive the latest project information for Valle Romano Crest Villas.',
  'Me gustaría recibir la información actualizada del proyecto Valle Romano Crest Villas.',
  'Je souhaite recevoir les informations à jour sur le projet Valle Romano Crest Villas.',
  'Ich möchte die aktuellen Projektinformationen zu Valle Romano Crest Villas erhalten.',
  'Хочу получить актуальную информацию по проекту Valle Romano Crest Villas.',
  'أرغب في تلقي أحدث معلومات مشروع Valle Romano Crest Villas.',
  'Ik ontvang graag de actuele projectinformatie voor Valle Romano Crest Villas.',
  'Chciałbym otrzymać aktualne informacje o projekcie Valle Romano Crest Villas.',
  'Jeg vil gjerne motta oppdatert prosjektinformasjon om Valle Romano Crest Villas.',
  'Jag vill gärna få aktuell projektinformation om Valle Romano Crest Villas.')
a(133, 'Project context: Valle Romano Crest Villas.',
  'Contexto del proyecto: Valle Romano Crest Villas.', 'Contexte du projet : Valle Romano Crest Villas.',
  'Projektkontext: Valle Romano Crest Villas.', 'Контекст проекта: Valle Romano Crest Villas.', 'سياق المشروع: Valle Romano Crest Villas.',
  'Projectcontext: Valle Romano Crest Villas.', 'Kontekst projektu: Valle Romano Crest Villas.',
  'Prosjektsammenheng: Valle Romano Crest Villas.', 'Projektsammanhang: Valle Romano Crest Villas.')
a(134, 'Valle Romano Crest Villas - 8 Villas, Estepona',
  'Valle Romano Crest Villas - 8 villas, Estepona', 'Valle Romano Crest Villas - 8 villas, Estepona',
  'Valle Romano Crest Villas - 8 Villen, Estepona', 'Valle Romano Crest Villas - 8 вилл, Эстепона',
  'Valle Romano Crest Villas - 8 فلل، إستيبونا', 'Valle Romano Crest Villas - 8 villa’s, Estepona',
  'Valle Romano Crest Villas - 8 willi, Estepona', 'Valle Romano Crest Villas - 8 villaer, Estepona',
  'Valle Romano Crest Villas - 8 villor, Estepona')
a(135, 'Valle Romano Crest Villas: Eight Detached Villas, Estepona',
  'Valle Romano Crest Villas: ocho villas independientes, Estepona', 'Valle Romano Crest Villas : huit villas indépendantes, Estepona',
  'Valle Romano Crest Villas: acht freistehende Villen, Estepona', 'Valle Romano Crest Villas: восемь отдельных вилл, Эстепона',
  'Valle Romano Crest Villas: ثماني فلل مستقلة، إستيبونا', 'Valle Romano Crest Villas: acht vrijstaande villa’s, Estepona',
  'Valle Romano Crest Villas: osiem wolnostojących willi, Estepona', 'Valle Romano Crest Villas: åtte frittstående villaer, Estepona',
  'Valle Romano Crest Villas: åtta fristående villor, Estepona')
a(136, 'Eight Detached Villas, Estepona',
  'Ocho villas independientes, Estepona', 'Huit villas indépendantes, Estepona', 'Acht freistehende Villen, Estepona',
  'Восемь отдельных вилл, Эстепона', 'ثماني فلل مستقلة، إستيبونا', 'Acht vrijstaande villa’s, Estepona',
  'Osiem wolnostojących willi, Estepona', 'Åtte frittstående villaer, Estepona', 'Åtta fristående villor, Estepona')

# ---------------------------------------------------------------- per-villa plan sheets (13 Nov 2026 follow-up)
# Every villa now has its own plan set from the agent intranet: a site plan and one sheet per floor,
# with a basement sheet for Villa 8. The alts and captions are written from one pattern per level.
CAP = {   # site plan, basement, ground floor, first floor
    'es': ('plano de implantación', 'sótano', 'planta baja', 'planta primera'),
    'fr': ('plan de masse', 'sous-sol', 'rez-de-chaussée', 'premier étage'),
    'de': ('Lageplan', 'Untergeschoss', 'Erdgeschoss', 'Obergeschoss'),
    'ru': ('генплан', 'подвальный этаж', 'первый этаж', 'второй этаж'),
    'ar': ('مخطط الموقع', 'القبو', 'الطابق الأرضي', 'الطابق الأول'),
    'nl': ('situatietekening', 'kelder', 'begane grond', 'eerste verdieping'),
    'pl': ('plan zagospodarowania', 'piwnica', 'parter', 'piętro'),
    'no': ('situasjonsplan', 'kjeller', 'første etasje', 'andre etasje'),
    'sv': ('situationsplan', 'källare', 'bottenvåning', 'första våningen'),
}
VNAME = {'es': 'Villa {}', 'fr': 'Villa {}', 'de': 'Villa {}', 'ru': 'Вилла {}', 'ar': 'الفيلا {}',
         'nl': 'Villa {}', 'pl': 'Willa {}', 'no': 'Villa {}', 'sv': 'Villa {}'}
SEP = {l: ('، ' if l == 'ar' else ', ') for l in LOCS}
for n in range(1, 9):
    for k, en in enumerate(('site plan', 'basement', 'ground floor', 'first floor')):
        if en == 'basement' and n != 8:
            continue
        T[f'Villa {n}, {en}'] = {l: VNAME[l].format(n) + SEP[l] + CAP[l][k] for l in LOCS}

SITE = ('Plano de implantación de la villa {n}, con la casa, las terrazas, la piscina y el aparcamiento',
        'Plan de masse de la villa {n}, avec la maison, les terrasses, la piscine et le stationnement',
        'Lageplan der Villa {n} mit Haus, Terrassen, Pool und Stellplätzen',
        'Генплан виллы {n}: дом, террасы, бассейн и парковка',
        'مخطط موقع الفيلا {n}، مع المنزل والتراسات والمسبح وموقف السيارات',
        'Situatietekening van villa {n}, met het huis, de terrassen, het zwembad en het parkeren',
        'Plan zagospodarowania willi {n}: dom, tarasy, basen i miejsca postojowe',
        'Situasjonsplan for villa {n}, med huset, terrassene, bassenget og parkeringen',
        'Situationsplan för villa {n}, med huset, terrasserna, poolen och parkeringen')
GROUND = ('Plano de la planta baja de la villa {n}, con el salón, la cocina, la terraza cubierta y la piscina',
          'Plan du rez-de-chaussée de la villa {n}, avec le séjour, la cuisine, la terrasse couverte et la piscine',
          'Grundriss des Erdgeschosses der Villa {n} mit Wohnzimmer, Küche, überdachter Terrasse und Pool',
          'План первого этажа виллы {n}: гостиная, кухня, крытая терраса и бассейн',
          'مخطط الطابق الأرضي للفيلا {n}، مع غرفة المعيشة والمطبخ والتراس المغطى والمسبح',
          'Plattegrond van de begane grond van villa {n}, met de woonkamer, de keuken, het overdekte terras en het zwembad',
          'Rzut parteru willi {n}: salon, kuchnia, zadaszony taras i basen',
          'Plantegning av første etasje i villa {n}, med stue, kjøkken, overbygd terrasse og basseng',
          'Planritning över bottenvåningen i villa {n}, med vardagsrum, kök, övertäckt terrass och pool')
FIRST_ENTRY = ('Plano de la planta primera de la villa {n}, con el acceso, el aparcamiento y tres dormitorios',
               'Plan du premier étage de la villa {n}, avec l’entrée, le stationnement et trois chambres',
               'Grundriss des Obergeschosses der Villa {n} mit Eingang, Stellplätzen und drei Schlafzimmern',
               'План второго этажа виллы {n}: вход, парковка и три спальни',
               'مخطط الطابق الأول للفيلا {n}، مع المدخل وموقف السيارات وثلاث غرف نوم',
               'Plattegrond van de eerste verdieping van villa {n}, met de entree, het parkeren en drie slaapkamers',
               'Rzut piętra willi {n}: wejście, miejsca postojowe i trzy sypialnie',
               'Plantegning av andre etasje i villa {n}, med inngang, parkering og tre soverom',
               'Planritning över första våningen i villa {n}, med entré, parkering och tre sovrum')
FIRST_BEDS = ('Plano de la planta primera de la villa {n}, con tres dormitorios y sus baños',
              'Plan du premier étage de la villa {n}, avec trois chambres et leurs salles de bains',
              'Grundriss des Obergeschosses der Villa {n} mit drei Schlafzimmern und ihren Badezimmern',
              'План второго этажа виллы {n}: три спальни с ванными комнатами',
              'مخطط الطابق الأول للفيلا {n}، مع ثلاث غرف نوم وحماماتها',
              'Plattegrond van de eerste verdieping van villa {n}, met drie slaapkamers en hun badkamers',
              'Rzut piętra willi {n}: trzy sypialnie z łazienkami',
              'Plantegning av andre etasje i villa {n}, med tre soverom og badene deres',
              'Planritning över första våningen i villa {n}, med tre sovrum och deras badrum')


def plan(en, pattern, n):
    T[en] = {l: t.format(n=n) for l, t in zip(LOCS, pattern)}


for n in range(3, 9):
    plan(f'Site plan of Villa {n}, with the house, the terraces, the pool and the parking', SITE, n)
for n in range(3, 8):
    plan(f'Ground floor plan of Villa {n}, with the living room, kitchen, covered terrace and pool', GROUND, n)
for n in range(3, 6):
    plan(f'First floor plan of Villa {n}, with the entrance, parking and three bedrooms', FIRST_ENTRY, n)
for n in (6, 7):
    plan(f'First floor plan of Villa {n}, with three bedrooms and their bathrooms', FIRST_BEDS, n)

a(71, 'Ground floor plan of Villa 8',
  'Plano de la planta baja de la villa 8, con la cocina, el salón, el espacio a doble altura y la piscina',
  'Plan du rez-de-chaussée de la villa 8, avec la cuisine, le séjour, l’espace en double hauteur et la piscine',
  'Grundriss des Erdgeschosses der Villa 8 mit Küche, Wohnzimmer, doppelter Raumhöhe und Pool',
  'План первого этажа виллы 8: кухня, гостиная, пространство двойной высоты и бассейн',
  'مخطط الطابق الأرضي للفيلا 8، مع المطبخ وغرفة المعيشة والفراغ المزدوج الارتفاع والمسبح',
  'Plattegrond van de begane grond van villa 8, met de keuken, de woonkamer, de vide en het zwembad',
  'Rzut parteru willi 8: kuchnia, salon, przestrzeń o podwójnej wysokości i basen',
  'Plantegning av første etasje i villa 8, med kjøkken, stue, rom med dobbel takhøyde og basseng',
  'Planritning över bottenvåningen i villa 8, med kök, vardagsrum, rum i dubbel höjd och pool')
a(73, 'First floor plan of Villa 8',
  'Plano de la planta primera de la villa 8, con el dormitorio principal y su vestidor, otros dos dormitorios y el aparcamiento',
  'Plan du premier étage de la villa 8, avec la chambre principale et son dressing, deux autres chambres et le stationnement',
  'Grundriss des Obergeschosses der Villa 8 mit Hauptschlafzimmer und Ankleide, zwei weiteren Schlafzimmern und Stellplatz',
  'План второго этажа виллы 8: главная спальня с гардеробной, ещё две спальни и парковка',
  'مخطط الطابق الأول للفيلا 8، مع غرفة النوم الرئيسية وغرفة ملابسها، وغرفتي نوم أخريين، وموقف السيارات',
  'Plattegrond van de eerste verdieping van villa 8, met de hoofdslaapkamer en inloopkast, twee andere slaapkamers en het parkeren',
  'Rzut piętra willi 8: główna sypialnia z garderobą, dwie kolejne sypialnie i miejsce postojowe',
  'Plantegning av andre etasje i villa 8, med hovedsoverom og garderobe, to soverom til og parkering',
  'Planritning över första våningen i villa 8, med huvudsovrum och klädkammare, ytterligare två sovrum och parkering')
a(69, 'Basement plan of Villa 8',
  'Plano del sótano de la villa 8, con dos salas de usos múltiples, un cuarto de instalaciones y un jardín interior',
  'Plan du sous-sol de la villa 8, avec deux pièces polyvalentes, un local technique et un jardin intérieur',
  'Grundriss des Untergeschosses der Villa 8 mit zwei Mehrzweckräumen, einem Technikraum und einem Innengarten',
  'План подвального этажа виллы 8: два многофункциональных помещения, техническое помещение и внутренний сад',
  'مخطط قبو الفيلا 8، مع غرفتين متعددتي الاستخدامات وغرفة للتجهيزات الفنية وحديقة داخلية',
  'Plattegrond van de kelder van villa 8, met twee multifunctionele ruimtes, een technische ruimte en een binnentuin',
  'Rzut piwnicy willi 8: dwa pomieszczenia wielofunkcyjne, pomieszczenie techniczne i ogród wewnętrzny',
  'Plantegning av kjelleren i villa 8, med to flerbruksrom, et teknisk rom og en innvendig hage',
  'Planritning över källaren i villa 8, med två multifunktionsrum, ett teknikrum och en inre trädgård')

# Villa 8's three levels; Arabic joins them with و, the others come from FLOOR_PARTS in assemble.py.
T['Basement, ground floor & first floor'] = {'ar': 'الطابق السفلي والطابق الأرضي والطابق الأول'}

a(14, 'Computer-generated images from the developer',
  'Imágenes generadas por ordenador del catálogo del promotor. Ilustran el proyecto y no son las casas terminadas; el mobiliario, la decoración y la vegetación son orientativos y no se incluyen en la venta. El club de golf y Estepona son fotografías. Los planos están recortados de las fichas de planos del promotor para cada villa.',
  'Images de synthèse issues du catalogue du promoteur. Elles illustrent le projet et ne montrent pas les maisons achevées ; le mobilier, la décoration et les plantations sont indicatifs et ne sont pas inclus dans la vente. Le club-house du golf et Estepona sont des photographies. Les plans sont extraits des fiches de plans du promoteur pour chaque villa.',
  'Computergenerierte Bilder aus dem Katalog des Bauträgers. Sie veranschaulichen das Projekt und zeigen nicht die fertigen Häuser; Möbel, Dekoration und Bepflanzung sind beispielhaft und nicht im Kaufpreis enthalten. Das Golf-Clubhaus und Estepona sind Fotografien. Die Pläne stammen aus den Planblättern des Bauträgers für jede einzelne Villa.',
  'Компьютерные визуализации из каталога застройщика. Они иллюстрируют проект и не являются готовыми домами; мебель, декор и озеленение показаны условно и в продажу не входят. Клубный дом гольф-клуба и Эстепона — фотографии. Планировки взяты из листов планов застройщика по каждой вилле.',
  'صور مُنشأة بالحاسوب من كتالوج المطوّر. وهي توضّح المشروع وليست المنازل المكتملة؛ والأثاث والديكور والنباتات استرشادية ولا تدخل في البيع. أما نادي الغولف وإستيبونا فصور فوتوغرافية. والمخططات مقتطعة من أوراق مخططات المطوّر الخاصة بكل فيلا.',
  'Computergegenereerde beelden uit de catalogus van de ontwikkelaar. Ze illustreren het project en tonen niet de afgewerkte huizen; meubilair, decoratie en beplanting zijn indicatief en niet inbegrepen bij de verkoop. Het golfclubhuis en Estepona zijn foto’s. De plattegronden komen uit de tekeningbladen van de ontwikkelaar voor elke villa.',
  'Wizualizacje komputerowe z katalogu dewelopera. Ilustrują projekt i nie przedstawiają gotowych domów; meble, wystrój i zieleń mają charakter poglądowy i nie są objęte sprzedażą. Klub golfowy i Estepona to fotografie. Rzuty pochodzą z arkuszy rysunków dewelopera dla każdej willi.',
  'Datagenererte bilder fra utbyggerens katalog. De illustrerer prosjektet og viser ikke de ferdige husene; møbler, innredning og beplantning er veiledende og inngår ikke i salget. Golfklubbhuset og Estepona er fotografier. Plantegningene er hentet fra utbyggerens tegningsark for hver villa.',
  'Datorgenererade bilder ur exploatörens katalog. De illustrerar projektet och visar inte de färdiga husen; möbler, inredning och växtlighet är vägledande och ingår inte i köpet. Golfklubbhuset och Estepona är fotografier. Planritningarna är hämtade ur exploatörens ritningsblad för varje villa.')
a(80, 'The areas below are the price list',
  'Las superficies siguientes son las de la lista de precios, redondeadas al metro cuadrado; las estancias siguen las fichas de planos de cada villa, con un plano de implantación y una ficha por planta.',
  'Les surfaces ci-dessous sont celles de la liste de prix, arrondies au mètre carré ; les pièces suivent les fiches de plans propres à chaque villa, un plan de masse et une fiche par niveau.',
  'Die folgenden Flächen stammen aus der Preisliste, auf den Quadratmeter gerundet; die Räume folgen den eigenen Planblättern jeder Villa, einem Lageplan und einem Blatt je Geschoss.',
  'Площади ниже взяты из прайс-листа и округлены до квадратного метра; помещения описаны по собственным листам планов каждой виллы — генплану и листу на каждый этаж.',
  'المساحات أدناه مأخوذة من قائمة الأسعار ومقرّبة إلى المتر المربع، أما الغرف فتتبع أوراق المخططات الخاصة بكل فيلا: مخطط للموقع وورقة لكل طابق.',
  'De oppervlakten hieronder komen uit de prijslijst, afgerond op de vierkante meter; de ruimtes volgen de eigen tekeningbladen van elke villa, een situatietekening en één blad per verdieping.',
  'Poniższe powierzchnie pochodzą z cennika i są zaokrąglone do metra kwadratowego; pomieszczenia opisano według arkuszy rysunków każdej willi: planu zagospodarowania i arkusza dla każdej kondygnacji.',
  'Arealene nedenfor er prislistens, avrundet til nærmeste kvadratmeter; rommene følger hver villas egne tegningsark, en situasjonsplan og ett ark per etasje.',
  'Ytorna nedan är prislistans, avrundade till hela kvadratmeter; rummen följer varje villas egna ritningsblad, en situationsplan och ett blad per våning.')
a(84, 'The price list and the summary on every plan sheet give four bedrooms and four bathrooms;',
  'La lista de precios y el resumen de cada ficha de planos indican cuatro dormitorios y cuatro baños; los cuadros de superficies de los planos de planta de las villas 1 y 2 enumeran tres dormitorios, un vestidor y tres baños.',
  'La liste de prix et le récapitulatif de chaque fiche de plans indiquent quatre chambres et quatre salles de bains ; les tableaux de surfaces des plans d’étage des villas 1 et 2 énumèrent trois chambres, un dressing et trois salles de bains.',
  'Die Preisliste und die Zusammenfassung auf jedem Planblatt nennen vier Schlafzimmer und vier Badezimmer; die Raumtabellen der Grundrisse der Villen 1 und 2 führen drei Schlafzimmer, eine Ankleide und drei Badezimmer auf.',
  'Прайс-лист и сводка на каждом листе планов указывают четыре спальни и четыре ванные комнаты; экспликации на поэтажных планах вилл 1 и 2 перечисляют три спальни, гардеробную и три ванные комнаты.',
  'تذكر قائمة الأسعار وملخص كل ورقة مخططات أربع غرف نوم وأربعة حمامات، بينما تسرد جداول الغرف في مخططات طوابق الفيلتين 1 و2 ثلاث غرف نوم وغرفة ملابس وثلاثة حمامات.',
  'De prijslijst en de samenvatting op elk tekeningblad noemen vier slaapkamers en vier badkamers; de ruimtestaten op de plattegronden van villa 1 en 2 vermelden drie slaapkamers, een inloopkast en drie badkamers.',
  'Cennik i podsumowanie na każdym arkuszu rysunków podają cztery sypialnie i cztery łazienki; zestawienia pomieszczeń na rzutach willi 1 i 2 wymieniają trzy sypialnie, garderobę i trzy łazienki.',
  'Prislisten og sammendraget på hvert tegningsark oppgir fire soverom og fire bad; romskjemaene på plantegningene for villa 1 og 2 lister opp tre soverom, en garderobe og tre bad.',
  'Prislistan och sammanställningen på varje ritningsblad anger fyra sovrum och fyra badrum; rumsförteckningarna på planritningarna för villa 1 och 2 listar tre sovrum, en klädkammare och tre badrum.')
a(87, 'Villas 3 to 5, on their plan sheets',
  'Villas 3 a 5, según sus fichas de planos: en la planta baja, el salón, la cocina, un lavadero, almacenaje, un baño, una terraza cubierta y la piscina; en la planta primera, el acceso, aparcamiento para dos coches, tres dormitorios con baño propio y una terraza bajo pérgola. Los planos de la villa 5 dibujan además un ascensor.',
  'Villas 3 à 5, selon leurs fiches de plans : au rez-de-chaussée, le séjour, la cuisine, une buanderie, des rangements, une salle de bains, une terrasse couverte et la piscine ; au premier étage, l’entrée, le stationnement pour deux voitures, trois chambres avec chacune sa salle de bains et une terrasse sous pergola. Les plans de la villa 5 dessinent aussi un ascenseur.',
  'Villen 3 bis 5, laut ihren Planblättern: im Erdgeschoss Wohnzimmer, Küche, Hauswirtschaftsraum, Abstellflächen, ein Badezimmer, eine überdachte Terrasse und der Pool; im Obergeschoss der Eingang, Stellplätze für zwei Autos, drei Schlafzimmer mit eigenem Bad und eine Terrasse unter einer Pergola. Die Pläne der Villa 5 zeichnen zudem einen Aufzug.',
  'Виллы 3–5, по их листам планов: на первом этаже гостиная, кухня, постирочная, кладовые, ванная комната, крытая терраса и бассейн; на втором этаже вход, парковка на две машины, три спальни с собственными ванными комнатами и терраса под перголой. На планах виллы 5 также показан лифт.',
  'الفلل من 3 إلى 5، وفق أوراق مخططاتها: في الطابق الأرضي غرفة المعيشة والمطبخ وغرفة غسيل ومساحات تخزين وحمّام وتراس مغطى والمسبح؛ وفي الطابق الأول المدخل وموقف لسيارتين وثلاث غرف نوم لكل منها حمّامها وتراس تحت برغولا. وتُظهر مخططات الفيلا 5 مصعداً أيضاً.',
  'Villa 3 tot 5, volgens hun tekeningbladen: op de begane grond de woonkamer, de keuken, een wasruimte, bergruimte, een badkamer, een overdekt terras en het zwembad; op de eerste verdieping de entree, parkeerplaats voor twee auto’s, drie slaapkamers met eigen badkamer en een terras onder een pergola. De plattegronden van villa 5 tekenen ook een lift.',
  'Wille 3–5, według ich arkuszy rysunków: na parterze salon, kuchnia, pralnia, schowki, łazienka, zadaszony taras i basen; na piętrze wejście, miejsca postojowe na dwa samochody, trzy sypialnie z własnymi łazienkami i taras pod pergolą. Rzuty willi 5 pokazują także windę.',
  'Villa 3 til 5, ifølge tegningsarkene: i første etasje stue, kjøkken, vaskerom, bod, et bad, en overbygd terrasse og bassenget; i andre etasje inngangen, parkering for to biler, tre soverom med eget bad og en terrasse under pergola. Tegningene for villa 5 viser også en heis.',
  'Villa 3 till 5, enligt sina ritningsblad: på bottenvåningen vardagsrum, kök, tvättstuga, förråd, ett badrum, en övertäckt terrass och poolen; på första våningen entrén, parkering för två bilar, tre sovrum med eget badrum och en terrass under pergola. Ritningarna för villa 5 visar även en hiss.')
a(88, 'Villas 6 and 7 are entered at ground level',
  'A las villas 6 y 7 se entra a nivel de planta baja, junto al aparcamiento, con el salón, la cocina, un lavadero, almacenaje, un aseo, la piscina y un acceso al sótano, aunque sus fichas no incluyen plano de sótano; los tres dormitorios, cada uno con su baño, están en la planta primera.',
  'On entre dans les villas 6 et 7 de plain-pied à côté du stationnement, avec le séjour, la cuisine, une buanderie, des rangements, un WC invités, la piscine et un accès au sous-sol, bien que leurs fiches ne comportent aucun plan de sous-sol ; les trois chambres, chacune avec sa salle de bains, sont au premier étage.',
  'Die Villen 6 und 7 betritt man ebenerdig neben den Stellplätzen, mit Wohnzimmer, Küche, Hauswirtschaftsraum, Abstellflächen, Gäste-WC, Pool und einem Zugang zum Untergeschoss, obwohl ihre Planblätter keinen Untergeschossplan enthalten; die drei Schlafzimmer mit jeweils eigenem Bad liegen im Obergeschoss.',
  'В виллы 6 и 7 входят на уровне первого этажа рядом с парковкой; здесь гостиная, кухня, постирочная, кладовые, гостевой санузел, бассейн и спуск в подвал, хотя плана подвального этажа в их листах нет; три спальни, каждая со своей ванной комнатой, находятся на втором этаже.',
  'يُدخل إلى الفيلتين 6 و7 من مستوى الطابق الأرضي بجوار موقف السيارات، حيث غرفة المعيشة والمطبخ وغرفة الغسيل ومساحات التخزين ودورة مياه للضيوف والمسبح ومدخل إلى القبو، رغم أن أوراقهما لا تتضمن مخططاً للقبو؛ أما غرف النوم الثلاث، ولكل منها حمّامها، ففي الطابق الأول.',
  'Villa 6 en 7 betreed je gelijkvloers naast het parkeren, met de woonkamer, de keuken, een wasruimte, bergruimte, een gastentoilet, het zwembad en een toegang naar de kelder, al bevatten hun tekeningbladen geen kelderplan; de drie slaapkamers, elk met eigen badkamer, liggen op de eerste verdieping.',
  'Do willi 6 i 7 wchodzi się na poziomie parteru obok miejsc postojowych; są tam salon, kuchnia, pralnia, schowki, toaleta dla gości, basen i zejście do piwnicy, choć ich arkusze nie zawierają rzutu piwnicy; trzy sypialnie, każda z własną łazienką, znajdują się na piętrze.',
  'Villa 6 og 7 har inngang på bakkenivå ved parkeringen, med stue, kjøkken, vaskerom, bod, gjestetoalett, basseng og en nedgang til kjeller, selv om tegningsarkene ikke har noen kjellerplan; de tre soverommene, hvert med eget bad, ligger i andre etasje.',
  'Villa 6 och 7 har entré i markplan intill parkeringen, med vardagsrum, kök, tvättstuga, förråd, gästtoalett, pool och en nedgång till källare, även om ritningsbladen saknar källarplan; de tre sovrummen, vart och ett med eget badrum, ligger på första våningen.')
a(90, 'Ground floor: the kitchen with a pantry',
  'Planta baja: la cocina con despensa, un salón de {N47.43} {U} y un espacio a doble altura, con un baño, un lavadero y almacén, abiertos a una terraza cubierta, una terraza bajo pérgola y una piscina de {N31.74} {U}.',
  'Rez-de-chaussée : la cuisine avec cellier, un séjour de {N47.43} {U} et un espace en double hauteur, avec une salle de bains, une buanderie et un rangement, ouverts sur une terrasse couverte, une terrasse sous pergola et une piscine de {N31.74} {U}.',
  'Erdgeschoss: die Küche mit Speisekammer, ein Wohnzimmer von {N47.43} {U} und ein Raum mit doppelter Höhe, dazu ein Badezimmer, ein Hauswirtschaftsraum und ein Abstellraum, offen zu einer überdachten Terrasse, einer Terrasse unter einer Pergola und einem Pool von {N31.74} {U}.',
  'Первый этаж: кухня с кладовой, гостиная {N47.43} {U} и пространство двойной высоты, а также ванная комната, постирочная и кладовая, с выходом на крытую террасу, террасу под перголой и к бассейну {N31.74} {U}.',
  'الطابق الأرضي: المطبخ مع مخزن للمؤن، وغرفة معيشة بمساحة {N47.43} {U}، وفراغ مزدوج الارتفاع، مع حمّام وغرفة غسيل ومخزن، تنفتح على تراس مغطى وتراس تحت برغولا ومسبح بمساحة {N31.74} {U}.',
  'Begane grond: de keuken met voorraadkamer, een woonkamer van {N47.43} {U} en een vide, met een badkamer, een wasruimte en een berging, uitkomend op een overdekt terras, een terras onder een pergola en een zwembad van {N31.74} {U}.',
  'Parter: kuchnia ze spiżarnią, salon o powierzchni {N47.43} {U} i przestrzeń o podwójnej wysokości, a także łazienka, pralnia i schowek, z wyjściem na zadaszony taras, taras pod pergolą i basen o powierzchni {N31.74} {U}.',
  'Første etasje: kjøkkenet med spiskammer, en stue på {N47.43} {U} og et rom med dobbel takhøyde, med bad, vaskerom og bod, som åpner seg mot en overbygd terrasse, en terrasse under pergola og et basseng på {N31.74} {U}.',
  'Bottenvåning: köket med skafferi, ett vardagsrum på {N47.43} {U} och ett rum i dubbel höjd, med badrum, tvättstuga och förråd, som öppnar sig mot en övertäckt terrass, en terrass under pergola och en pool på {N31.74} {U}.')
a(91, 'First floor, at street level: the entrance and parking',
  'Planta primera, a nivel de calle: el acceso y el aparcamiento, un dormitorio principal con vestidor de {N12.89} {U}, otros dos dormitorios de 18 {U} cada uno y tres baños.',
  'Premier étage, au niveau de la rue : l’entrée et le stationnement, une chambre principale avec un dressing de {N12.89} {U}, deux autres chambres de 18 {U} chacune et trois salles de bains.',
  'Obergeschoss, auf Straßenniveau: Eingang und Stellplatz, ein Hauptschlafzimmer mit einer Ankleide von {N12.89} {U}, zwei weitere Schlafzimmer von je 18 {U} und drei Badezimmer.',
  'Второй этаж, на уровне улицы: вход и парковка, главная спальня с гардеробной {N12.89} {U}, ещё две спальни по 18 {U} и три ванные комнаты.',
  'الطابق الأول، على مستوى الشارع: المدخل وموقف السيارات، وغرفة نوم رئيسية مع غرفة ملابس بمساحة {N12.89} {U}، وغرفتا نوم أخريان مساحة كل منهما 18 {U}، وثلاثة حمامات.',
  'Eerste verdieping, op straatniveau: de entree en het parkeren, een hoofdslaapkamer met een inloopkast van {N12.89} {U}, twee andere slaapkamers van elk 18 {U} en drie badkamers.',
  'Piętro, na poziomie ulicy: wejście i miejsce postojowe, główna sypialnia z garderobą o powierzchni {N12.89} {U}, dwie kolejne sypialnie po 18 {U} i trzy łazienki.',
  'Andre etasje, på gatenivå: inngangen og parkeringen, et hovedsoverom med en garderobe på {N12.89} {U}, to soverom til på 18 {U} hver og tre bad.',
  'Första våningen, i gatuplan: entrén och parkeringen, ett huvudsovrum med en klädkammare på {N12.89} {U}, ytterligare två sovrum på 18 {U} vardera och tre badrum.')
a(92, 'Basement, drawn on its own sheet',
  'Sótano, dibujado en su propia ficha: dos salas de usos múltiples de {N76.46} y {N44.83} {U}, un cuarto de instalaciones y un jardín interior, con {N170.02} {U} construidos. La memoria de calidades incluye el sótano entre las opciones de pago, así que confirmamos por escrito qué incluye el precio.',
  'Sous-sol, dessiné sur sa propre fiche : deux pièces polyvalentes de {N76.46} et {N44.83} {U}, un local technique et un jardin intérieur, pour {N170.02} {U} construits. Le descriptif range le sous-sol parmi les options payantes, nous confirmons donc par écrit ce que comprend le prix.',
  'Untergeschoss, auf einem eigenen Blatt gezeichnet: zwei Mehrzweckräume von {N76.46} und {N44.83} {U}, ein Technikraum und ein Innengarten, {N170.02} {U} bebaut. Die Baubeschreibung führt ein Untergeschoss unter den kostenpflichtigen Optionen, daher bestätigen wir schriftlich, was der Preis enthält.',
  'Подвальный этаж, показанный на отдельном листе: два многофункциональных помещения {N76.46} и {N44.83} {U}, техническое помещение и внутренний сад, {N170.02} {U} застройки. Спецификация относит подвал к платным опциям, поэтому мы письменно подтверждаем, что входит в цену.',
  'القبو، مرسوم على ورقة خاصة به: غرفتان متعددتا الاستخدامات بمساحة {N76.46} و{N44.83} {U}، وغرفة للتجهيزات الفنية، وحديقة داخلية، بمساحة مبنية {N170.02} {U}. وتدرج المواصفات القبو ضمن الخيارات المدفوعة، لذا نؤكد كتابياً ما يشمله السعر.',
  'Kelder, getekend op een eigen blad: twee multifunctionele ruimtes van {N76.46} en {N44.83} {U}, een technische ruimte en een binnentuin, {N170.02} {U} bebouwd. De technische omschrijving noemt een kelder bij de betaalde opties, dus we bevestigen schriftelijk wat de prijs omvat.',
  'Piwnica, pokazana na osobnym arkuszu: dwa pomieszczenia wielofunkcyjne o powierzchni {N76.46} i {N44.83} {U}, pomieszczenie techniczne i ogród wewnętrzny, {N170.02} {U} zabudowy. Specyfikacja wymienia piwnicę wśród płatnych opcji, dlatego potwierdzamy na piśmie, co obejmuje cena.',
  'Kjeller, tegnet på eget ark: to flerbruksrom på {N76.46} og {N44.83} {U}, et teknisk rom og en innvendig hage, {N170.02} {U} bebygd. Beskrivelsen fører en kjeller blant tilleggsvalgene mot betaling, så vi bekrefter skriftlig hva prisen omfatter.',
  'Källare, ritad på ett eget blad: två multifunktionsrum på {N76.46} och {N44.83} {U}, ett teknikrum och en inre trädgård, {N170.02} {U} byggyta. Byggbeskrivningen tar upp en källare bland tillvalen mot betalning, så vi bekräftar skriftligt vad priset omfattar.')
a(96, 'Availability and prices as listed in the developer',
  'Disponibilidad y precios según la lista de precios del promotor de octubre de 2026, que se reconfirman antes de la reserva. La lista indica que describe la promoción y no la disponibilidad actual, y no dice si incluye el IVA: en una villa de obra nueva en España el IVA del {P10} se suma al precio de compra, así que confirmamos por escrito cuál se aplica. Las superficies son las de la lista, redondeadas al metro cuadrado. Su superficie construida total es mayor que la suma del interior y las terrazas, y la lista no explica a qué corresponde la diferencia. Dormitorios y baños: la lista de precios y el resumen de la ficha de planos de cada villa indican cuatro de cada, pero todos los cuadros de superficies enumeran tres dormitorios. Las villas 3 a 8 incluyen tres baños de dormitorio y un cuarto baño o aseo; las villas 1 y 2, tres baños y un vestidor. Las fichas de planos dan las superficies al centímetro: de {N121.83} a {N432.79} {U} construidos interiores, de {N99.08} a {N373.20} {U} útiles, parcelas de {N400.00} a {G1001},88 {U} y piscinas de {N16.74} a {N31.74} {U}. En las villas 3 a 6 las cifras de las fichas quedan hasta aproximadamente 1 {U} por debajo de las de la lista: la parcela de la villa 6, por ejemplo, mide {N532.06} {U} en su ficha y 533 {U} en la lista.',
  'Disponibilité et prix selon la liste de prix du promoteur d’octobre 2026, reconfirmés avant la réservation. La liste précise qu’elle décrit le programme et n’indique pas la disponibilité actuelle, et elle ne dit pas si la TVA est comprise : sur une villa neuve en Espagne, la TVA de {P10} s’ajoute au prix d’achat, nous confirmons donc par écrit ce qui s’applique. Les surfaces sont celles de la liste, arrondies au mètre carré. Sa surface construite totale dépasse l’intérieur et les terrasses réunis, et la liste ne précise pas à quoi correspond la différence. Chambres et salles de bains : la liste de prix et le récapitulatif de la fiche de plans de chaque villa en indiquent quatre de chaque, mais tous les tableaux de surfaces énumèrent trois chambres. Les villas 3 à 8 comptent trois salles de bains attenantes aux chambres et une quatrième salle de bains ou un WC invités ; les villas 1 et 2, trois salles de bains et un dressing. Les fiches de plans donnent les surfaces au centimètre près : de {N121.83} à {N432.79} {U} construits intérieurs, de {N99.08} à {N373.20} {U} utiles, des parcelles de {N400.00} à {G1001},88 {U} et des piscines de {N16.74} à {N31.74} {U}. Pour les villas 3 à 6, les chiffres des fiches sont jusqu’à environ 1 {U} inférieurs à ceux de la liste : la parcelle de la villa 6, par exemple, mesure {N532.06} {U} sur sa fiche et 533 {U} sur la liste.',
  'Verfügbarkeit und Preise laut der Preisliste des Bauträgers vom Oktober 2026, vor der Reservierung erneut bestätigt. Die Liste gibt an, dass sie das Projekt beschreibt und nicht die aktuelle Verfügbarkeit, und sie sagt nicht, ob die MwSt. enthalten ist: Bei einer neu gebauten Villa in Spanien kommen {P10} MwSt. auf den Kaufpreis, daher bestätigen wir schriftlich, was gilt. Die Flächen sind die der Liste, auf den Quadratmeter gerundet. Ihre gesamte bebaute Fläche ist größer als Innenfläche und Terrassen zusammen, und die Liste sagt nicht, was die Differenz umfasst. Schlafzimmer und Badezimmer: Die Preisliste und die Zusammenfassung auf dem Planblatt jeder Villa nennen je vier, aber jede Raumtabelle führt drei Schlafzimmer auf. Die Villen 3 bis 8 haben drei Bäder zu den Schlafzimmern und ein viertes Bad oder Gäste-WC; die Villen 1 und 2 drei Badezimmer und eine Ankleide. Die Planblätter geben die Flächen auf den Zentimeter genau an: {N121.83} bis {N432.79} {U} bebaute Innenfläche, {N99.08} bis {N373.20} {U} Nutzfläche, Grundstücke von {N400.00} bis {G1001},88 {U} und Pools von {N16.74} bis {N31.74} {U}. Bei den Villen 3 bis 6 liegen die Werte der Planblätter bis zu etwa 1 {U} unter denen der Liste: Das Grundstück der Villa 6 etwa misst auf seinem Blatt {N532.06} {U} und in der Liste 533 {U}.',
  'Наличие и цены по прайс-листу застройщика за октябрь 2026 года, повторно подтверждаются перед бронированием. В прайс-листе сказано, что он описывает проект и не отражает текущее наличие, и не указано, включён ли НДС: при покупке новой виллы в Испании НДС {P10} добавляется к цене, поэтому мы письменно подтверждаем, что применяется. Площади взяты из прайс-листа и округлены до квадратного метра. Общая площадь застройки в нём больше суммы внутренней площади и террас, и прайс-лист не объясняет, что составляет разницу. Спальни и ванные комнаты: прайс-лист и сводка на листе планов каждой виллы указывают по четыре, но во всех экспликациях перечислены три спальни. У вилл 3–8 три ванные комнаты при спальнях и четвёртая ванная или гостевой санузел; у вилл 1 и 2 — три ванные комнаты и гардеробная. Листы планов дают площади с точностью до сантиметра: от {N121.83} до {N432.79} {U} внутренней площади застройки, от {N99.08} до {N373.20} {U} полезной площади, участки от {N400.00} до {G1001},88 {U} и бассейны от {N16.74} до {N31.74} {U}. У вилл 3–6 цифры листов примерно на 1 {U} меньше, чем в прайс-листе: например, участок виллы 6 на её листе составляет {N532.06} {U}, а в прайс-листе — 533 {U}.',
  'التوفر والأسعار وفق قائمة أسعار المطوّر لشهر أكتوبر 2026، ويُعاد تأكيدها قبل الحجز. وتذكر القائمة أنها تصف المشروع ولا تبيّن التوفر الحالي، ولا توضح ما إذا كانت ضريبة القيمة المضافة مشمولة: ففي الفيلا الجديدة في إسبانيا تُضاف ضريبة القيمة المضافة بنسبة {P10} إلى سعر الشراء، لذا نؤكد كتابياً ما ينطبق. المساحات هي مساحات القائمة مقرّبة إلى المتر المربع. ومساحتها المبنية الإجمالية أكبر من مجموع المساحة الداخلية والتراسات، ولا توضح القائمة ما يغطيه الفرق. غرف النوم والحمامات: تذكر قائمة الأسعار وملخص ورقة مخططات كل فيلا أربعاً من كل منهما، لكن جميع جداول الغرف تسرد ثلاث غرف نوم. وفي الفلل من 3 إلى 8 ثلاثة حمامات لغرف النوم وحمّام رابع أو دورة مياه للضيوف، وفي الفيلتين 1 و2 ثلاثة حمامات وغرفة ملابس. وتعطي أوراق المخططات المساحات بدقة السنتيمتر: من {N121.83} إلى {N432.79} {U} مساحة داخلية مبنية، ومن {N99.08} إلى {N373.20} {U} مساحة صافية، وقطع أرض من {N400.00} إلى {G1001}.88 {U}، ومسابح من {N16.74} إلى {N31.74} {U}. وفي الفلل من 3 إلى 6 تقل أرقام الأوراق بما يصل إلى نحو 1 {U} عن أرقام القائمة: فقطعة أرض الفيلا 6 مثلاً {N532.06} {U} في ورقتها و533 {U} في القائمة.',
  'Beschikbaarheid en prijzen volgens de prijslijst van de ontwikkelaar van oktober 2026, opnieuw bevestigd vóór reservering. De lijst vermeldt dat zij het project beschrijft en niet de actuele beschikbaarheid, en zegt niet of de btw is inbegrepen: bij een nieuwbouwvilla in Spanje komt {P10} btw bovenop de koopprijs, dus we bevestigen schriftelijk wat van toepassing is. De oppervlakten zijn die van de lijst, afgerond op de vierkante meter. Het totale bebouwde oppervlak is groter dan binnenoppervlak en terrassen samen, en de lijst zegt niet wat het verschil omvat. Slaapkamers en badkamers: de prijslijst en de samenvatting op het tekeningblad van elke villa noemen er elk vier, maar elke ruimtestaat vermeldt drie slaapkamers. Villa 3 tot 8 hebben drie badkamers bij de slaapkamers en een vierde badkamer of gastentoilet; villa 1 en 2 drie badkamers en een inloopkast. De tekeningbladen geven de oppervlakten tot op de centimeter: {N121.83} tot {N432.79} {U} bebouwd binnenoppervlak, {N99.08} tot {N373.20} {U} gebruiksoppervlak, percelen van {N400.00} tot {G1001},88 {U} en zwembaden van {N16.74} tot {N31.74} {U}. Bij villa 3 tot 6 liggen de cijfers van de bladen tot ongeveer 1 {U} onder die van de lijst: het perceel van villa 6 meet bijvoorbeeld {N532.06} {U} op zijn blad en 533 {U} op de lijst.',
  'Dostępność i ceny według cennika dewelopera z października 2026 roku, ponownie potwierdzane przed rezerwacją. Cennik zaznacza, że opisuje inwestycję i nie wskazuje aktualnej dostępności, i nie podaje, czy cena obejmuje VAT: przy nowo wybudowanej willi w Hiszpanii do ceny zakupu dolicza się {P10} VAT, dlatego potwierdzamy na piśmie, co obowiązuje. Powierzchnie pochodzą z cennika i są zaokrąglone do metra kwadratowego. Podana w nim całkowita powierzchnia zabudowy jest większa niż suma powierzchni wewnętrznej i tarasów, a cennik nie wyjaśnia, co obejmuje różnica. Sypialnie i łazienki: cennik i podsumowanie na arkuszu rysunków każdej willi podają po cztery, ale każde zestawienie pomieszczeń wymienia trzy sypialnie. Wille 3–8 mają trzy łazienki przy sypialniach i czwartą łazienkę lub toaletę dla gości; wille 1 i 2 trzy łazienki i garderobę. Arkusze rysunków podają powierzchnie z dokładnością do centymetra: od {N121.83} do {N432.79} {U} wewnętrznej powierzchni zabudowy, od {N99.08} do {N373.20} {U} powierzchni użytkowej, działki od {N400.00} do {G1001},88 {U} i baseny od {N16.74} do {N31.74} {U}. W willach 3–6 wartości z arkuszy są do około 1 {U} niższe niż w cenniku: działka willi 6 ma na przykład na swoim arkuszu {N532.06} {U}, a w cenniku 533 {U}.',
  'Tilgjengelighet og priser ifølge utbyggerens prisliste fra oktober 2026, bekreftet på nytt før reservasjon. Listen opplyser at den beskriver prosjektet og ikke viser dagens tilgjengelighet, og den sier ikke om mva er inkludert: på en nybygd villa i Spania kommer {P10} mva i tillegg til kjøpesummen, så vi bekrefter skriftlig hva som gjelder. Arealene er listens, avrundet til nærmeste kvadratmeter. Det totale bebygde arealet er større enn innvendig areal og terrasser til sammen, og listen sier ikke hva differansen omfatter. Soverom og bad: prislisten og sammendraget på tegningsarket for hver villa oppgir fire av hver, men alle romskjemaene lister opp tre soverom. Villa 3 til 8 har tre bad til soverommene og et fjerde bad eller gjestetoalett; villa 1 og 2 har tre bad og en garderobe. Tegningsarkene gir arealene på centimeteren: {N121.83} til {N432.79} {U} innvendig bebygd, {N99.08} til {N373.20} {U} bruksareal, tomter på {N400.00} til {G1001},88 {U} og basseng på {N16.74} til {N31.74} {U}. For villa 3 til 6 ligger tallene på arkene opptil rundt 1 {U} under listens: tomten til villa 6 er for eksempel {N532.06} {U} på arket og 533 {U} i listen.',
  'Tillgänglighet och priser enligt exploatörens prislista från oktober 2026, bekräftade på nytt före bokning. Listan anger att den beskriver projektet och inte visar aktuell tillgänglighet, och den säger inte om IVA (spansk moms) ingår: på en nybyggd villa i Spanien läggs IVA om {P10} på köpeskillingen, så vi bekräftar skriftligt vad som gäller. Ytorna är listans, avrundade till hela kvadratmeter. Den totala byggytan är större än inneryta och terrasser tillsammans, och listan anger inte vad skillnaden omfattar. Sovrum och badrum: prislistan och sammanställningen på ritningsbladet för varje villa anger fyra av vardera, men alla rumsförteckningar listar tre sovrum. Villa 3 till 8 har tre badrum till sovrummen och ett fjärde badrum eller en gästtoalett; villa 1 och 2 har tre badrum och en klädkammare. Ritningsbladen anger ytorna på centimetern: {N121.83} till {N432.79} {U} invändig byggyta, {N99.08} till {N373.20} {U} boarea, tomter om {N400.00} till {G1001},88 {U} och pooler på {N16.74} till {N31.74} {U}. För villa 3 till 6 ligger bladens siffror upp till cirka 1 {U} under listans: tomten för villa 6 är till exempel {N532.06} {U} på sitt blad och 533 {U} i listan.')
a(115, 'The licence is not yet granted',
  'La licencia aún no está concedida, la constructora no está elegida y los documentos no coinciden en el número de dormitorios. Resolvemos cada punto por escrito.',
  'Le permis n’est pas encore délivré, l’entreprise générale n’est pas choisie et les documents divergent sur le nombre de chambres. Nous réglons chaque point par écrit.',
  'Die Genehmigung ist noch nicht erteilt, das Bauunternehmen nicht ausgewählt, und die Unterlagen weichen bei der Zahl der Schlafzimmer voneinander ab. Wir klären jeden Punkt schriftlich.',
  'Разрешение ещё не выдано, подрядчик не выбран, а документы расходятся в числе спален. Мы проясняем каждый пункт письменно.',
  'لم تُمنح الرخصة بعد، ولم يُختر المقاول، وتختلف الوثائق في عدد غرف النوم. نحسم كل نقطة كتابياً.',
  'De vergunning is nog niet verleend, de aannemer is niet gekozen en de documenten verschillen over het aantal slaapkamers. We leggen elk punt schriftelijk vast.',
  'Pozwolenie nie zostało jeszcze wydane, wykonawca nie jest wybrany, a dokumenty różnią się co do liczby sypialni. Każdą kwestię ustalamy na piśmie.',
  'Tillatelsen er ennå ikke gitt, entreprenøren er ikke valgt, og dokumentene er uenige om antall soverom. Vi avklarer hvert punkt skriftlig.',
  'Bygglovet är ännu inte beviljat, entreprenören är inte vald och handlingarna är oeniga om antalet sovrum. Vi reder ut varje punkt skriftligt.')
a(123, 'Four bedrooms on the price list and the plan summaries',
  'Cuatro dormitorios en la lista de precios y en los resúmenes de los planos, tres en el cuadro de superficies de cada villa. Contrastamos la distribución de la villa que elija con los planos del contrato.',
  'Quatre chambres sur la liste de prix et les récapitulatifs des plans, trois dans le tableau de surfaces de chaque villa. Nous vérifions l’agencement de la villa que vous choisissez au regard des plans contractuels.',
  'Vier Schlafzimmer auf der Preisliste und in den Zusammenfassungen der Pläne, drei in der Raumtabelle jeder Villa. Wir gleichen die Aufteilung der von Ihnen gewählten Villa mit den Vertragsplänen ab.',
  'Четыре спальни в прайс-листе и сводках планов, три в экспликации каждой виллы. Мы сверяем планировку выбранной вами виллы с планами, приложенными к договору.',
  'أربع غرف نوم في قائمة الأسعار وملخصات المخططات، وثلاث في جدول الغرف لكل فيلا. نطابق توزيع الفيلا التي تختارونها مع مخططات العقد.',
  'Vier slaapkamers op de prijslijst en in de samenvattingen van de plannen, drie in de ruimtestaat van elke villa. Wij toetsen de indeling van de villa die u kiest aan de contracttekeningen.',
  'Cztery sypialnie w cenniku i podsumowaniach rzutów, trzy w zestawieniu pomieszczeń każdej willi. Sprawdzamy układ wybranej przez Państwa willi z rysunkami stanowiącymi część umowy.',
  'Fire soverom på prislisten og i sammendragene på tegningene, tre i romskjemaet for hver villa. Vi kontrollerer planløsningen i villaen du velger mot kontraktstegningene.',
  'Fyra sovrum på prislistan och i ritningarnas sammanställningar, tre i varje villas rumsförteckning. Vi stämmer av planlösningen i den villa ni väljer mot kontraktsritningarna.')
a(153, 'The price list and the summary on every plan sheet give four bedrooms and four bathrooms, but',
  'La lista de precios y el resumen de cada ficha de planos indican cuatro dormitorios y cuatro baños, pero los cuadros de superficies de los planos de cada villa enumeran tres dormitorios. Las villas 3 a 8 tienen tres baños de dormitorio y un cuarto baño o aseo; las villas 1 y 2, tres baños y un vestidor, y la villa 8 añade un sótano con dos salas de usos múltiples. Contrastamos la distribución de cada villa con los planos del contrato.',
  'La liste de prix et le récapitulatif de chaque fiche de plans indiquent quatre chambres et quatre salles de bains, mais les tableaux de surfaces des plans de chaque villa énumèrent trois chambres. Les villas 3 à 8 ont trois salles de bains attenantes aux chambres et une quatrième salle de bains ou un WC invités ; les villas 1 et 2, trois salles de bains et un dressing, et la villa 8 ajoute un sous-sol avec deux pièces polyvalentes. Nous vérifions l’agencement de chaque villa au regard des plans contractuels.',
  'Die Preisliste und die Zusammenfassung auf jedem Planblatt nennen vier Schlafzimmer und vier Badezimmer, aber die Raumtabellen in den Grundrissen jeder Villa führen drei Schlafzimmer auf. Die Villen 3 bis 8 haben drei Bäder zu den Schlafzimmern und ein viertes Bad oder Gäste-WC; die Villen 1 und 2 drei Badezimmer und eine Ankleide, und Villa 8 hat zusätzlich ein Untergeschoss mit zwei Mehrzweckräumen. Wir gleichen die Aufteilung jeder Villa mit den Vertragsplänen ab.',
  'Прайс-лист и сводка на каждом листе планов указывают четыре спальни и четыре ванные комнаты, но экспликации на планах каждой виллы перечисляют три спальни. У вилл 3–8 три ванные комнаты при спальнях и четвёртая ванная или гостевой санузел; у вилл 1 и 2 — три ванные комнаты и гардеробная, а у виллы 8 есть ещё подвальный этаж с двумя многофункциональными помещениями. Мы сверяем планировку каждой виллы с планами, приложенными к договору.',
  'تذكر قائمة الأسعار وملخص كل ورقة مخططات أربع غرف نوم وأربعة حمامات، لكن جداول الغرف في مخططات كل فيلا تسرد ثلاث غرف نوم. في الفلل من 3 إلى 8 ثلاثة حمامات لغرف النوم وحمّام رابع أو دورة مياه للضيوف، وفي الفيلتين 1 و2 ثلاثة حمامات وغرفة ملابس، وتضيف الفيلا 8 قبواً بغرفتين متعددتي الاستخدامات. نطابق توزيع كل فيلا مع مخططات العقد.',
  'De prijslijst en de samenvatting op elk tekeningblad noemen vier slaapkamers en vier badkamers, maar de ruimtestaten op de plattegronden van elke villa vermelden drie slaapkamers. Villa 3 tot 8 hebben drie badkamers bij de slaapkamers en een vierde badkamer of gastentoilet; villa 1 en 2 drie badkamers en een inloopkast, en villa 8 heeft daarnaast een kelder met twee multifunctionele ruimtes. Wij toetsen de indeling van elke villa aan de contracttekeningen.',
  'Cennik i podsumowanie na każdym arkuszu rysunków podają cztery sypialnie i cztery łazienki, ale zestawienia pomieszczeń na rzutach każdej willi wymieniają trzy sypialnie. Wille 3–8 mają trzy łazienki przy sypialniach i czwartą łazienkę lub toaletę dla gości; wille 1 i 2 trzy łazienki i garderobę, a willa 8 ma dodatkowo piwnicę z dwiema salami wielofunkcyjnymi. Sprawdzamy układ każdej willi z rysunkami stanowiącymi część umowy.',
  'Prislisten og sammendraget på hvert tegningsark oppgir fire soverom og fire bad, men romskjemaene på plantegningene for hver villa lister opp tre soverom. Villa 3 til 8 har tre bad til soverommene og et fjerde bad eller gjestetoalett; villa 1 og 2 har tre bad og en garderobe, og villa 8 har i tillegg en kjeller med to flerbruksrom. Vi kontrollerer planløsningen i hver villa mot kontraktstegningene.',
  'Prislistan och sammanställningen på varje ritningsblad anger fyra sovrum och fyra badrum, men rumsförteckningarna på planritningarna för varje villa listar tre sovrum. Villa 3 till 8 har tre badrum till sovrummen och ett fjärde badrum eller en gästtoalett; villa 1 och 2 har tre badrum och en klädkammare, och villa 8 har dessutom en källare med två multifunktionsrum. Vi stämmer av planlösningen i varje villa mot kontraktsritningarna.')

# The translation memory spells this one "Pooltrassen" in Swedish; it is "Poolterrassen".
override('The pool terrace',
  'La terraza de la piscina', 'La terrasse de la piscine', 'Die Poolterrasse', 'Терраса у бассейна', 'تراس المسبح',
  'Het zwembadterras', 'Taras przy basenie', 'Bassengterrassen', 'Poolterrassen')

# assemble.py's num() turns "1,002" into "1,002" for the dot-grouping languages (it swaps the comma for
# the group mark, then every dot for the decimal comma), so the plot range is written here.
override('400 - 1,002 sqm',
  '400 - 1.002 m²', '400 - 1 002 m²', '400 - 1.002 m²', '400 - 1 002 м²', '400 - 1,002 م²',
  '400 - 1.002 m²', '400 - 1 002 m²', '400 - 1 002 m²', '400 - 1 002 m²')

# The memory carries three Russian and two Arabic spellings of "Approx."; one per table.
for n in (25, 30, 40, 55):
    en = f'Approx. {n} minutes'
    T[en] = {'ru': f'Около {n} минут', 'ar': f'حوالي {n} دقيقة'}

# Arabic joins the two floors with و, as la-concha-view-villa does; the other languages are written
# by assemble.py from FLOOR_PARTS.
T['Ground floor & first floor'] = {'ar': 'الطابق الأرضي والطابق الأول'}

# The floor label "Ground floor & first floor" is a plain FLOOR_PARTS phrase that assemble.py writes
# itself; availability.phase is empty and passes through.
LEFT = {'Ground floor & first floor', 'Basement, ground floor & first floor', ''}
missing = [(i, s) for i, s in enumerate(todo) if s not in T and s not in LEFT]
assert not missing, missing
json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries to', f'{SP}/tr_a.json')
