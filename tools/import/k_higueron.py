# -*- coding: utf-8 -*-
"""Higueron Seaside Residences: the 136 strings the translation memory did not have.

Same shape as k_atalaya.py. Tokens expand per language:  {E567000}  {EC1797.50} (money with
cents)  {N22.31}  {U} (m2)  {M} (metre)  {KM}.   Run:  python3 tools/import/k_higueron.py <scratch dir>
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/import_h/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {'es': 'm²', 'fr': 'm²', 'de': 'm²', 'ru': 'м²', 'ar': 'م²', 'nl': 'm²', 'pl': 'm²', 'no': 'm²', 'sv': 'm²'}
METRE = {'ru': 'м', 'ar': 'م'}
KM = {'ru': 'км', 'ar': 'كم'}
T = {}


def money(n, l, cents=None):
    body = f'{n:,}'.replace(',', GROUP[l])
    if cents is not None:
        body += ('.' if l == 'ar' else ',') + cents
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{EC(\d+)\.(\d\d)\}', lambda m: money(int(m.group(1)), l, m.group(2)), text)
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{G(\d+)\}', lambda m: f'{int(m.group(1)):,}'.replace(',', GROUP[l]), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l]).replace('{M}', METRE.get(l, 'm')).replace('{KM}', KM.get(l, 'km'))


def a(i, hint, *tr):
    en = todo[i]
    assert en.startswith(hint), (i, hint, en[:40])
    assert len(tr) == 9, (i, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---------------------------------------------------------------- templates
APT = {'es': 'apartamento', 'fr': 'appartement', 'de': 'Wohnung', 'ru': 'квартиры', 'ar': 'الشقة', 'nl': 'appartement',
       'pl': 'mieszkania', 'no': 'leilighet', 'sv': 'lägenhet'}
LEVEL = {   # ground floor / third floor and solarium (the labels the site already uses for each part)
    'es': ('planta baja', 'tercera planta y solárium'), 'fr': ('rez-de-chaussée', 'troisième étage et solarium'),
    'de': ('Erdgeschoss', 'drittes Obergeschoss und Solarium'), 'ru': ('первый этаж', 'четвёртый этаж и солярий'),
    'ar': ('الطابق الأرضي', 'الطابق الثالث والسولاريوم'), 'nl': ('begane grond', 'derde verdieping en solarium'),
    'pl': ('parter', 'trzecie piętro i solarium'), 'no': ('første etasje', 'fjerde etasje og solterrasse'),
    'sv': ('bottenvåning', 'tredje våningen och solterrass'),
}
PLAN = {'es': ('Plano del apartamento {n}, {lv}', 'Apartamento {n}, {lv}'), 'fr': ('Plan de l\'appartement {n}, {lv}', 'Appartement {n}, {lv}'),
        'de': ('Grundriss Wohnung {n}, {lv}', 'Wohnung {n}, {lv}'), 'ru': ('Планировка квартиры {n}, {lv}', 'Квартира {n}, {lv}'),
        'ar': ('مخطط الشقة {n}، {lv}', 'شقة {n}، {lv}'), 'nl': ('Plattegrond van appartement {n}, {lv}', 'Appartement {n}, {lv}'),
        'pl': ('Rzut mieszkania {n}, {lv}', 'Mieszkanie {n}, {lv}'), 'no': ('Plantegning leilighet {n}, {lv}', 'Leilighet {n}, {lv}'),
        'sv': ('Planritning lägenhet {n}, {lv}', 'Lägenhet {n}, {lv}')}
FLOOR = {   # "Block 1, <floor>": the prefix and the part exactly as FLOOR_PARTS and the other apartment projects write them
    'es': ('Bloque 1', 'planta baja', 'tercera planta'), 'fr': ('Bloc 1', 'rez-de-chaussée', 'troisième étage'),
    'de': ('Block 1', 'Erdgeschoss', 'drittes Obergeschoss'), 'ru': ('Блок 1', 'первый этаж', 'четвёртый этаж'),
    'ar': ('مبنى 1', 'الطابق الأرضي', 'الطابق الثالث'), 'nl': ('Blok 1', 'begane grond', 'derde verdieping'),
    'pl': ('Blok 1', 'parter', 'trzecie piętro'), 'no': ('Hus 1', 'første etasje', 'fjerde etasje'),
    'sv': ('Hus 1', 'bottenvåning', 'tredje våningen')}
for en in todo:
    m = re.fullmatch(r'Floorplan of Apartment (\d+), (ground floor|third floor and solarium)', en)
    c = re.fullmatch(r'Apartment (\d+), (ground floor|third floor and solarium)', en)
    f = re.fullmatch(r'Block 1, (Ground floor|Third floor)', en)
    k = lambda s: 0 if s.startswith('ground') or s.startswith('Ground') else 1
    if m:
        T[en] = {l: PLAN[l][0].format(n=m.group(1), lv=LEVEL[l][k(m.group(2))]) for l in LOCS}
    elif c:
        T[en] = {l: PLAN[l][1].format(n=c.group(1), lv=LEVEL[l][k(c.group(2))]) for l in LOCS}
    elif f:
        T[en] = {l: f'{FLOOR[l][0]}, {FLOOR[l][1 + k(f.group(1))]}' for l in LOCS}

# ---------------------------------------------------------------- names, card, meta
a(0, 'Higueron Seaside Residences', *(['Higueron Seaside Residences'] * 9))
a(1, 'Higueron Seaside', *(['Higueron Seaside'] * 9))
a(2, 'Higueron <em>', *(['Higueron <em>Seaside Residences</em>'] * 9))
a(3, 'Five finished apartments and penthouses available at El Higuerón',
  "Cinco apartamentos y áticos terminados en El Higuerón, Fuengirola, de dos o tres dormitorios, con terrazas o jardín privado, dos plazas de aparcamiento y un trastero cada uno, y una gran piscina comunitaria. Listos para entrar a vivir, desde {E567000}.",
  "Cinq appartements et penthouses achevés à El Higuerón, Fuengirola, de deux ou trois chambres, avec terrasses ou jardin privé, deux places de stationnement et un débarras chacun, et une grande piscine commune. Prêts à habiter, à partir de {E567000}.",
  "Fünf fertiggestellte Wohnungen und Penthouses in El Higuerón, Fuengirola, mit zwei oder drei Schlafzimmern, Terrassen oder privatem Garten, jeweils zwei Stellplätzen und einem Abstellraum sowie einem großen Gemeinschaftspool. Bezugsfertig, ab {E567000}.",
  "Пять готовых квартир и пентхаусов в Эль-Игероне, Фуэнхирола, с двумя или тремя спальнями, террасами или частным садом, двумя парковочными местами и кладовой у каждой, а также большим общим бассейном. Готовы к заселению, от {E567000}.",
  "خمس شقق وبنتهاوس جاهزة في إل إيغيرون بفوينخيرولا، من غرفتي نوم أو ثلاث غرف، بتراسات أو حديقة خاصة، ولكل منها موقفا سيارات ومخزن، مع مسبح مشترك كبير. جاهزة للسكن، ابتداءً من {E567000}.",
  "Vijf afgeronde appartementen en penthouses in El Higuerón, Fuengirola, met twee of drie slaapkamers, terrassen of een privétuin, elk met twee parkeerplaatsen en een berging, en een groot gemeenschappelijk zwembad. Klaar om in te trekken, vanaf {E567000}.",
  "Pięć ukończonych apartamentów i penthouse’ów w El Higuerón, Fuengirola, z dwiema lub trzema sypialniami, tarasami lub prywatnym ogrodem, z dwoma miejscami parkingowymi i komórką lokatorską każdy, oraz dużym basenem wspólnym. Gotowe do zamieszkania, od {E567000}.",
  "Fem ferdigstilte leiligheter og toppleiligheter i El Higuerón, Fuengirola, med to eller tre soverom, terrasser eller privat hage, hver med to parkeringsplasser og en bod, og et stort felles basseng. Klare til innflytting, fra {E567000}.",
  "Fem färdigställda lägenheter och takvåningar i El Higuerón, Fuengirola, med två eller tre sovrum, terrasser eller privat trädgård, var och en med två parkeringsplatser och ett förråd, och en stor gemensam pool. Inflyttningsklara, från {E567000}.")
a(4, 'Five ready-to-move-in apartments and penthouses at El Higuerón, Fuengirola: two or three bedrooms',
  "Cinco apartamentos y áticos listos para entrar a vivir en El Higuerón, Fuengirola: dos o tres dormitorios, de {N83.51} a {N128.28} {U} interiores, terrazas o jardín, dos plazas de aparcamiento y un trastero, desde {E567000}.",
  "Cinq appartements et penthouses prêts à habiter à El Higuerón, Fuengirola : deux ou trois chambres, de {N83.51} à {N128.28} {U} intérieurs, terrasses ou jardin, deux places de stationnement et un débarras, à partir de {E567000}.",
  "Fünf bezugsfertige Wohnungen und Penthouses in El Higuerón, Fuengirola: zwei oder drei Schlafzimmer, {N83.51} bis {N128.28} {U} Innenfläche, Terrassen oder Garten, zwei Stellplätze und ein Abstellraum, ab {E567000}.",
  "Пять готовых к заселению квартир и пентхаусов в Эль-Игероне, Фуэнхирола: две или три спальни, от {N83.51} до {N128.28} {U} внутренней площади, террасы или сад, два парковочных места и кладовая, от {E567000}.",
  "خمس شقق وبنتهاوس جاهزة للسكن في إل إيغيرون بفوينخيرولا: غرفتا نوم أو ثلاث، من {N83.51} إلى {N128.28} {U} مساحة داخلية، تراسات أو حديقة، وموقفا سيارات ومخزن، ابتداءً من {E567000}.",
  "Vijf appartementen en penthouses die klaar zijn om in te trekken in El Higuerón, Fuengirola: twee of drie slaapkamers, {N83.51} tot {N128.28} {U} binnenoppervlak, terrassen of tuin, twee parkeerplaatsen en een berging, vanaf {E567000}.",
  "Pięć apartamentów i penthouse’ów gotowych do zamieszkania w El Higuerón, Fuengirola: dwie lub trzy sypialnie, od {N83.51} do {N128.28} {U} powierzchni wewnętrznej, tarasy lub ogród, dwa miejsca parkingowe i komórka lokatorska, od {E567000}.",
  "Fem leiligheter og toppleiligheter klare til innflytting i El Higuerón, Fuengirola: to eller tre soverom, {N83.51} til {N128.28} {U} innvendig areal, terrasser eller hage, to parkeringsplasser og en bod, fra {E567000}.",
  "Fem inflyttningsklara lägenheter och takvåningar i El Higuerón, Fuengirola: två eller tre sovrum, {N83.51} till {N128.28} {U} invändig yta, terrasser eller trädgård, två parkeringsplatser och ett förråd, från {E567000}.")
a(5, 'Five finished apartments and penthouses at El Higuerón, Fuengirola, ready to move in',
  "Cinco apartamentos y áticos terminados en El Higuerón, Fuengirola, listos para entrar a vivir, desde {E567000}.",
  "Cinq appartements et penthouses achevés à El Higuerón, Fuengirola, prêts à habiter, à partir de {E567000}.",
  "Fünf fertiggestellte Wohnungen und Penthouses in El Higuerón, Fuengirola, bezugsfertig, ab {E567000}.",
  "Пять готовых квартир и пентхаусов в Эль-Игероне, Фуэнхирола, готовы к заселению, от {E567000}.",
  "خمس شقق وبنتهاوس جاهزة في إل إيغيرون بفوينخيرولا، جاهزة للسكن، ابتداءً من {E567000}.",
  "Vijf afgeronde appartementen en penthouses in El Higuerón, Fuengirola, klaar om in te trekken, vanaf {E567000}.",
  "Pięć ukończonych apartamentów i penthouse’ów w El Higuerón, Fuengirola, gotowych do zamieszkania, od {E567000}.",
  "Fem ferdigstilte leiligheter og toppleiligheter i El Higuerón, Fuengirola, klare til innflytting, fra {E567000}.",
  "Fem färdigställda lägenheter och takvåningar i El Higuerón, Fuengirola, inflyttningsklara, från {E567000}.")
a(6, 'Five finished apartments and penthouses at El Higuerón, two or three bedrooms',
  "Cinco apartamentos y áticos terminados en El Higuerón, de dos o tres dormitorios, con dos plazas de aparcamiento y un trastero cada uno y una gran piscina comunitaria.",
  "Cinq appartements et penthouses achevés à El Higuerón, de deux ou trois chambres, avec deux places de stationnement et un débarras chacun et une grande piscine commune.",
  "Fünf fertiggestellte Wohnungen und Penthouses in El Higuerón mit zwei oder drei Schlafzimmern, jeweils mit zwei Stellplätzen und einem Abstellraum und einem großen Gemeinschaftspool.",
  "Пять готовых квартир и пентхаусов в Эль-Игероне с двумя или тремя спальнями, двумя парковочными местами и кладовой у каждой и большим общим бассейном.",
  "خمس شقق وبنتهاوس جاهزة في إل إيغيرون، من غرفتي نوم أو ثلاث، ولكل منها موقفا سيارات ومخزن، مع مسبح مشترك كبير.",
  "Vijf afgeronde appartementen en penthouses in El Higuerón met twee of drie slaapkamers, elk met twee parkeerplaatsen en een berging, en een groot gemeenschappelijk zwembad.",
  "Pięć ukończonych apartamentów i penthouse’ów w El Higuerón z dwiema lub trzema sypialniami, każdy z dwoma miejscami parkingowymi i komórką lokatorską, oraz dużym basenem wspólnym.",
  "Fem ferdigstilte leiligheter og toppleiligheter i El Higuerón med to eller tre soverom, hver med to parkeringsplasser og en bod, og et stort felles basseng.",
  "Fem färdigställda lägenheter och takvåningar i El Higuerón med två eller tre sovrum, var och en med två parkeringsplatser och ett förråd, och en stor gemensam pool.")

# ---------------------------------------------------------------- image alt text and captions
a(7, 'Covered terrace with dining table', "Terraza cubierta con mesa de comedor, zona de estar y vistas al mar", "Terrasse couverte avec table à manger, salon d'extérieur et vue sur la mer",
  "Überdachte Terrasse mit Esstisch, Loungebereich und Blick aufs Meer", "Крытая терраса с обеденным столом, зоной отдыха и видом на море", "تراس مغطى بطاولة طعام ومنطقة جلوس وإطلالة على البحر",
  "Overdekt terras met eettafel, loungehoek en uitzicht op zee", "Zadaszony taras ze stołem jadalnianym, strefą wypoczynku i widokiem na morze", "Overbygd terrasse med spisebord, loungeområde og utsikt mot havet",
  "Övertäckt terrass med matbord, loungeyta och utsikt över havet")
a(8, 'Covered ground-floor terrace with lounge seating', "Terraza cubierta de planta baja con zona de estar, mesa de comedor y césped", "Terrasse couverte de rez-de-chaussée avec salon d'extérieur, table à manger et pelouse",
  "Überdachte Erdgeschossterrasse mit Loungebereich, Esstisch und Rasen", "Крытая терраса на первом этаже с зоной отдыха, обеденным столом и газоном", "تراس مغطى في الطابق الأرضي بمنطقة جلوس وطاولة طعام ومساحة عشبية",
  "Overdekt terras op de begane grond met loungehoek, eettafel en gazon", "Zadaszony taras na parterze ze strefą wypoczynku, stołem jadalnianym i trawnikiem", "Overbygd terrasse i første etasje med loungeområde, spisebord og plen",
  "Övertäckt terrass på bottenvåningen med loungeyta, matbord och gräsmatta")
a(9, 'Aerial view of the blocks on the hillside', "Vista aérea de los bloques en la ladera sobre la costa, con el mar al fondo", "Vue aérienne des blocs sur la colline au-dessus de la côte, avec la mer au loin",
  "Luftaufnahme der Blöcke am Hang über der Küste, dahinter das Meer", "Вид с воздуха на блоки на склоне над побережьем, вдали море", "منظر جوي للمباني على المنحدر فوق الساحل، والبحر في الخلفية",
  "Luchtopname van de blokken op de heuvel boven de kust, met de zee erachter", "Widok z lotu ptaka na bloki na zboczu nad wybrzeżem, w tle morze", "Flyfoto av byggene i skråningen over kysten, med havet bak",
  "Flygvy över husen i sluttningen ovanför kusten, med havet bortom")
a(10, 'Bedroom with a sliding door and a sea view', "Dormitorio con puerta corredera y vistas al mar", "Chambre avec porte coulissante et vue sur la mer",
  "Schlafzimmer mit Schiebetür und Meerblick", "Спальня с раздвижной дверью и видом на море", "غرفة نوم بباب منزلق وإطلالة على البحر",
  "Slaapkamer met schuifdeur en zeezicht", "Sypialnia z drzwiami przesuwnymi i widokiem na morze", "Soverom med skyvedør og utsikt mot havet", "Sovrum med skjutdörr och havsutsikt")
a(11, 'The homes <em>in detail</em>', "Las viviendas <em>al detalle</em>", "Les logements <em>en détail</em>", "Die Wohnungen <em>im Detail</em>", "Квартиры <em>в деталях</em>", "المساكن <em>بالتفصيل</em>",
  "De woningen <em>in detail</em>", "Mieszkania <em>w szczegółach</em>", "Boligene <em>i detalj</em>", "Bostäderna <em>i detalj</em>")
a(12, 'Photographs of a furnished apartment',
  "Fotografías de un apartamento amueblado, dos vistas aéreas y el plano de cada una de las cinco viviendas disponibles.",
  "Photographies d'un appartement meublé, deux vues aériennes et le plan de chacun des cinq logements disponibles.",
  "Fotos einer möblierten Wohnung, zwei Luftaufnahmen und der Grundriss jeder der fünf verfügbaren Wohnungen.",
  "Фотографии меблированной квартиры, два вида с воздуха и планировка каждой из пяти доступных квартир.",
  "صور لشقة مفروشة ومنظران جويان ومخطط كل مسكن من المساكن الخمسة المتاحة.",
  "Foto’s van een gemeubileerd appartement, twee luchtopnamen en de plattegrond van elk van de vijf beschikbare woningen.",
  "Zdjęcia umeblowanego apartamentu, dwa widoki z lotu ptaka i rzut każdego z pięciu dostępnych mieszkań.",
  "Bilder av en møblert leilighet, to flyfoto og plantegningen for hver av de fem tilgjengelige boligene.",
  "Bilder på en möblerad lägenhet, två flygvyer och planritningen för var och en av de fem tillgängliga bostäderna.")
a(13, 'The interior and terrace photographs show a furnished show home',
  "Las fotografías de interiores y terrazas muestran una vivienda piloto amueblada, y su mobiliario no forma parte de la venta estándar. La primera vista aérea es una imagen generada por ordenador. Los planos son los de la promotora, de octubre de 2023, y las superficies que indican son aproximadas.",
  "Les photographies des intérieurs et des terrasses montrent un appartement témoin meublé, dont le mobilier ne fait pas partie de la vente standard. La première vue aérienne est une image de synthèse. Les plans sont ceux du promoteur, datés d'octobre 2023, et les surfaces qui y figurent sont approximatives.",
  "Die Innen- und Terrassenfotos zeigen eine möblierte Musterwohnung, deren Möbel nicht zum Standardverkauf gehören. Die erste Luftaufnahme ist ein computergeneriertes Bild. Die Grundrisse stammen vom Bauträger, datiert Oktober 2023, und die darauf angegebenen Flächen sind ungefähr.",
  "На фотографиях интерьеров и террас показана меблированная демонстрационная квартира, её мебель не входит в стандартную продажу. Первый вид с воздуха — компьютерное изображение. Планировки предоставлены застройщиком, датированы октябрём 2023 года, а указанные на них площади приблизительны.",
  "تُظهر صور المساحات الداخلية والتراسات شقة نموذجية مفروشة، وأثاثها ليس جزءاً من البيع القياسي. المنظر الجوي الأول صورة مولّدة بالحاسوب. المخططات من إعداد المطور وتاريخها أكتوبر 2023، والمساحات المبينة عليها تقريبية.",
  "De foto’s van interieurs en terrassen tonen een gemeubileerd modelappartement, waarvan het meubilair geen deel uitmaakt van de standaardverkoop. De eerste luchtopname is een computergegenereerd beeld. De plattegronden zijn die van de ontwikkelaar, van oktober 2023, en de daarop vermelde oppervlaktes zijn bij benadering.",
  "Zdjęcia wnętrz i tarasów przedstawiają umeblowany apartament pokazowy, a jego meble nie wchodzą w skład standardowej sprzedaży. Pierwszy widok z lotu ptaka to obraz wygenerowany komputerowo. Rzuty pochodzą od dewelopera, z października 2023 roku, a podane na nich powierzchnie są przybliżone.",
  "Bildene av interiør og terrasser viser en møblert visningsleilighet, og møblene er ikke en del av standardsalget. Det første flyfotoet er et datagenerert bilde. Plantegningene er utviklerens, datert oktober 2023, og arealene på dem er omtrentlige.",
  "Bilderna av interiörer och terrasser visar en möblerad visningslägenhet, och dess möbler ingår inte i standardförsäljningen. Den första flygvyn är en datorgenererad bild. Planritningarna är byggherrens, daterade oktober 2023, och ytorna på dem är ungefärliga.")
a(14, 'A covered terrace with a sea view', "Una terraza cubierta con vistas al mar", "Une terrasse couverte avec vue sur la mer", "Eine überdachte Terrasse mit Meerblick", "Крытая терраса с видом на море", "تراس مغطى بإطلالة على البحر",
  "Een overdekt terras met zeezicht", "Zadaszony taras z widokiem na morze", "En overbygd terrasse med utsikt mot havet", "En övertäckt terrass med havsutsikt")
a(15, 'Ground-floor terrace opening onto a lawned private garden', "Terraza de planta baja que se abre a un jardín privado con césped", "Terrasse de rez-de-chaussée donnant sur un jardin privé engazonné",
  "Erdgeschossterrasse mit Zugang zu einem privaten Rasengarten", "Терраса на первом этаже с выходом в частный сад с газоном", "تراس في الطابق الأرضي يفتح على حديقة خاصة معشوشبة",
  "Terras op de begane grond dat uitkomt op een privétuin met gazon", "Taras na parterze otwierający się na prywatny ogród z trawnikiem", "Terrasse i første etasje som åpner seg mot en privat hage med plen",
  "Terrass på bottenvåningen som öppnar sig mot en privat trädgård med gräsmatta")
a(16, 'Terrace and lawn', "Terraza y césped", "Terrasse et pelouse", "Terrasse und Rasen", "Терраса и газон", "التراس والعشب", "Terras en gazon", "Taras i trawnik", "Terrasse og plen", "Terrass och gräsmatta")
a(17, 'Computer-generated aerial view of the three blocks', "Vista aérea generada por ordenador de los tres bloques con la montaña detrás", "Vue aérienne de synthèse des trois blocs avec la montagne derrière",
  "Computergenerierte Luftaufnahme der drei Blöcke mit dem Berg dahinter", "Компьютерное изображение трёх блоков с видом с воздуха и горой позади", "منظر جوي مولّد بالحاسوب للمباني الثلاثة والجبل خلفها",
  "Computergegenereerde luchtopname van de drie blokken met de berg erachter", "Wygenerowany komputerowo widok z lotu ptaka na trzy bloki z górą w tle", "Datagenerert flyfoto av de tre byggene med fjellet bak",
  "Datorgenererad flygvy över de tre husen med berget bakom")
a(18, 'The three blocks and the mountain', "Los tres bloques y la montaña", "Les trois blocs et la montagne", "Die drei Blöcke und der Berg", "Три блока и гора", "المباني الثلاثة والجبل",
  "De drie blokken en de berg", "Trzy bloki i góra", "De tre byggene og fjellet", "De tre husen och berget")
a(19, 'The blocks above the coast', "Los bloques sobre la costa", "Les blocs au-dessus de la côte", "Die Blöcke über der Küste", "Блоки над побережьем", "المباني فوق الساحل",
  "De blokken boven de kust", "Bloki nad wybrzeżem", "Byggene over kysten", "Husen ovanför kusten")
a(20, 'Living and dining room with sliding doors onto the terrace', "Salón comedor con puertas correderas a la terraza", "Séjour-salle à manger avec baies coulissantes sur la terrasse",
  "Wohn- und Essbereich mit Schiebetüren zur Terrasse", "Гостиная-столовая с раздвижными дверями на террасу", "غرفة المعيشة والطعام بأبواب منزلقة تطل على التراس",
  "Woon- en eetkamer met schuifpuien naar het terras", "Salon z jadalnią z drzwiami przesuwnymi na taras", "Stue og spisestue med skyvedører mot terrassen", "Vardagsrum och matplats med skjutdörrar mot terrassen")
a(21, 'Furnished living room with a view through to the dining area', "Salón amueblado con vista hasta el comedor y la cocina", "Séjour meublé avec vue jusqu'à la salle à manger et la cuisine",
  "Möbliertes Wohnzimmer mit Blick bis zum Essbereich und zur Küche", "Меблированная гостиная с видом на столовую и кухню", "غرفة معيشة مفروشة مع إطلالة على منطقة الطعام والمطبخ",
  "Gemeubileerde woonkamer met doorkijk naar de eethoek en de keuken", "Umeblowany salon z widokiem na jadalnię i kuchnię", "Møblert stue med utsikt gjennom til spiseplassen og kjøkkenet",
  "Möblerat vardagsrum med genomsikt till matplatsen och köket")
a(22, 'Open-plan living, dining and kitchen area with a breakfast bar', "Salón, comedor y cocina abiertos, con una barra de desayuno", "Séjour, salle à manger et cuisine ouverts, avec un bar petit-déjeuner",
  "Offener Wohn-, Ess- und Küchenbereich mit Frühstückstheke", "Объединённое пространство гостиной, столовой и кухни с барной стойкой", "منطقة معيشة وطعام ومطبخ مفتوحة مع بار للإفطار",
  "Open woon-, eet- en keukenruimte met een ontbijtbar", "Otwarta przestrzeń salonu, jadalni i kuchni z barkiem śniadaniowym", "Åpen stue, spiseplass og kjøkken med frokostbar", "Öppen vardagsrums-, mat- och köksyta med frukostbar")
a(23, 'Fitted kitchen with a hob', "Cocina equipada con placa, horno y microondas en columna", "Cuisine équipée avec plaque, four et micro-ondes en colonne",
  "Einbauküche mit Kochfeld, Backofen und Mikrowelle im Hochschrank", "Кухня с варочной панелью, духовкой и микроволновой печью в колонне", "مطبخ مجهز بموقد وفرن وميكروويف في وحدة عمودية",
  "Ingerichte keuken met kookplaat, oven en magnetron in een kolom", "Wyposażona kuchnia z płytą, piekarnikiem i mikrofalówką w zabudowie słupkowej", "Utstyrt kjøkken med kokeplate, ovn og mikrobølgeovn i høyskap",
  "Utrustat kök med häll, ugn och mikrovågsugn i högskåp")
a(24, 'Main bedroom with a double bed', "Dormitorio principal con cama doble y armario empotrado", "Chambre principale avec lit double et armoire intégrée",
  "Hauptschlafzimmer mit Doppelbett und Einbauschrank", "Главная спальня с двуспальной кроватью и встроенным шкафом", "غرفة النوم الرئيسية بسرير مزدوج وخزانة مدمجة",
  "Hoofdslaapkamer met tweepersoonsbed en inbouwkast", "Główna sypialnia z łóżkiem dwuosobowym i szafą wnękową", "Hovedsoverom med dobbeltseng og innebygd garderobeskap", "Huvudsovrum med dubbelsäng och inbyggd garderob")
a(25, 'Bedroom with a sliding door onto a covered terrace', "Dormitorio con puerta corredera a una terraza cubierta y el mar", "Chambre avec porte coulissante sur une terrasse couverte et la mer",
  "Schlafzimmer mit Schiebetür zu einer überdachten Terrasse und dem Meer", "Спальня с раздвижной дверью на крытую террасу и море", "غرفة نوم بباب منزلق يفتح على تراس مغطى والبحر",
  "Slaapkamer met schuifdeur naar een overdekt terras en de zee", "Sypialnia z drzwiami przesuwnymi na zadaszony taras i morze", "Soverom med skyvedør mot en overbygd terrasse og havet", "Sovrum med skjutdörr mot en övertäckt terrass och havet")
a(26, 'Bedroom with a sea view', "Dormitorio con vistas al mar", "Chambre avec vue sur la mer", "Schlafzimmer mit Meerblick", "Спальня с видом на море", "غرفة نوم بإطلالة على البحر",
  "Slaapkamer met zeezicht", "Sypialnia z widokiem na morze", "Soverom med utsikt mot havet", "Sovrum med havsutsikt")
a(27, 'Bathroom with a double vanity', "Baño con lavabo doble, ducha a ras de suelo e inodoro suspendido", "Salle de bains avec double vasque, douche à l'italienne et WC suspendu",
  "Bad mit Doppelwaschtisch, begehbarer Dusche und Wand-WC", "Ванная комната с двойной раковиной, душем без поддона и подвесным унитазом", "حمام بمغسلتين ودش مسطح ومرحاض معلق",
  "Badkamer met dubbele wastafel, inloopdouche en hangend toilet", "Łazienka z podwójną umywalką, prysznicem bezprogowym i podwieszaną toaletą", "Bad med dobbel servant, åpen dusj og vegghengt toalett", "Badrum med dubbelt tvättställ, inbyggd dusch och väggmonterad toalett")

# ---------------------------------------------------------------- overview, why, architecture
a(38, 'Sixty homes, <em>five available</em>', "Sesenta viviendas, <em>cinco disponibles</em>", "Soixante logements, <em>cinq disponibles</em>", "Sechzig Wohnungen, <em>fünf verfügbar</em>",
  "Шестьдесят квартир, <em>пять в продаже</em>", "ستون مسكناً، <em>خمسة منها متاحة</em>", "Zestig woningen, <em>vijf beschikbaar</em>", "Sześćdziesiąt mieszkań, <em>pięć dostępnych</em>",
  "Seksti boliger, <em>fem tilgjengelige</em>", "Sextio bostäder, <em>fem tillgängliga</em>")
a(39, 'Higueron Seaside Residences is a finished development',
  "Higueron Seaside Residences es una promoción terminada de sesenta apartamentos y áticos en tres bloques en El Higuerón, Fuengirola, a poca distancia de la playa de Carvajal. Hay cinco viviendas disponibles: tres apartamentos de planta baja con jardín privado y dos áticos en la tercera planta con solárium en la azotea.",
  "Higueron Seaside Residences est un programme achevé de soixante appartements et penthouses répartis en trois blocs à El Higuerón, Fuengirola, à courte distance de la plage de Carvajal. Cinq logements sont actuellement disponibles : trois appartements en rez-de-chaussée avec jardin privé et deux penthouses au troisième étage avec solarium sur le toit.",
  "Higueron Seaside Residences ist ein fertiggestelltes Projekt mit sechzig Wohnungen und Penthouses in drei Blöcken in El Higuerón, Fuengirola, nicht weit vom Strand von Carvajal. Fünf Wohnungen sind derzeit verfügbar: drei Erdgeschosswohnungen mit privatem Garten und zwei Penthouses im dritten Obergeschoss mit Dach-Solarium.",
  "Higueron Seaside Residences — завершённый комплекс из шестидесяти квартир и пентхаусов в трёх блоках в Эль-Игероне, Фуэнхирола, недалеко от пляжа Карвахаль. Сейчас доступны пять квартир: три на первом этаже с частным садом и два пентхауса на четвёртом этаже с солярием на крыше.",
  "Higueron Seaside Residences مشروع مكتمل من ستين شقة وبنتهاوس في ثلاثة مبانٍ في إل إيغيرون بفوينخيرولا، على مسافة قريبة من شاطئ كارفاخال. خمسة مساكن متاحة حالياً: ثلاث شقق في الطابق الأرضي بحديقة خاصة وبنتهاوسان في الطابق الثالث بسولاريوم على السطح.",
  "Higueron Seaside Residences is een afgerond project van zestig appartementen en penthouses in drie blokken in El Higuerón, Fuengirola, op korte afstand van het strand van Carvajal. Vijf woningen zijn momenteel beschikbaar: drie appartementen op de begane grond met een privétuin en twee penthouses op de derde verdieping met een solarium op het dak.",
  "Higueron Seaside Residences to ukończona inwestycja obejmująca sześćdziesiąt apartamentów i penthouse’ów w trzech blokach w El Higuerón, Fuengirola, niedaleko plaży Carvajal. Obecnie dostępnych jest pięć lokali: trzy apartamenty na parterze z prywatnym ogrodem i dwa penthouse’y na trzecim piętrze z solarium na dachu.",
  "Higueron Seaside Residences er et ferdigstilt prosjekt med seksti leiligheter og toppleiligheter i tre bygg i El Higuerón, Fuengirola, like ved stranden i Carvajal. Fem boliger er tilgjengelige nå: tre leiligheter i første etasje med privat hage og to toppleiligheter i fjerde etasje med solterrasse på taket.",
  "Higueron Seaside Residences är ett färdigställt projekt med sextio lägenheter och takvåningar i tre hus i El Higuerón, Fuengirola, nära stranden i Carvajal. Fem bostäder är tillgängliga just nu: tre lägenheter på bottenvåningen med privat trädgård och två takvåningar på tredje våningen med solterrass på taket.")
a(40, 'Every home comes with two parking spaces and a storeroom in the basement',
  "Cada vivienda incluye dos plazas de aparcamiento y un trastero en el sótano, está orientada al suroeste y cuenta con climatización y calefacción por aerotermia con suelo radiante. Las zonas comunes tienen una piscina que se puede climatizar, una piscina infantil, un jacuzzi, un gimnasio y una sala de coworking.",
  "Chaque logement comprend deux places de stationnement et un débarras au sous-sol, est orienté sud-ouest et dispose d'un chauffage et d'une climatisation par aérothermie avec plancher chauffant. Les espaces communs comptent une piscine chauffable, une piscine pour enfants, un jacuzzi, une salle de sport et une salle de coworking.",
  "Jede Wohnung hat zwei Stellplätze und einen Abstellraum im Untergeschoss, ist nach Südwesten ausgerichtet und wird über eine Luft-Wasser-Wärmepumpe mit Fußbodenheizung beheizt und gekühlt. Die Gemeinschaftsanlagen umfassen einen beheizbaren Pool, ein Kinderbecken, einen Whirlpool, einen Fitnessraum und einen Coworking-Raum.",
  "В каждую квартиру входят два парковочных места и кладовая в цоколе; все квартиры ориентированы на юго-запад, отопление и охлаждение — от аэротермальной системы с тёплым полом. На общей территории есть бассейн с возможностью подогрева, детский бассейн, джакузи, тренажёрный зал и коворкинг.",
  "يشمل كل مسكن موقفي سيارات ومخزناً في القبو، ويتجه نحو الجنوب الغربي، ويُدفأ ويُبرَّد بنظام حراري هوائي مع تدفئة أرضية. وتضم المساحات المشتركة مسبحاً يمكن تسخينه ومسبحاً للأطفال وجاكوزي وصالة رياضية وغرفة عمل مشترك.",
  "Elke woning heeft twee parkeerplaatsen en een berging in de kelder, ligt op het zuidwesten en wordt verwarmd en gekoeld door een lucht-waterwarmtepomp met vloerverwarming. In de gemeenschappelijke ruimtes zijn een verwarmbaar zwembad, een kinderbad, een bubbelbad, een gym en een coworkingruimte.",
  "Każdy lokal ma dwa miejsca parkingowe i komórkę lokatorską w piwnicy, jest zwrócony na południowy zachód i jest ogrzewany oraz chłodzony przez pompę ciepła aerotermiczną z ogrzewaniem podłogowym. Na terenie wspólnym są basen z możliwością podgrzewania, basen dla dzieci, jacuzzi, siłownia i sala coworkingowa.",
  "Hver bolig har to parkeringsplasser og en bod i kjelleren, vender mot sørvest og varmes og kjøles av en luft-vann-varmepumpe med gulvvarme. Fellesområdene har et basseng som kan varmes opp, et barnebasseng, et boblebad, et treningsrom og et coworking-rom.",
  "Varje bostad har två parkeringsplatser och ett förråd i källaren, vetter mot sydväst och värms och kyls av en luft-vattenvärmepump med golvvärme. De gemensamma ytorna har en pool som kan värmas, en barnpool, en bubbelpool, ett gym och ett coworking-rum.")
a(41, 'Development', "Promoción", "Programme", "Projekt", "Комплекс", "المشروع", "Project", "Inwestycja", "Prosjekt", "Projekt")
a(42, '60 homes in 3 blocks', "60 viviendas en 3 bloques", "60 logements en 3 blocs", "60 Wohnungen in 3 Blöcken", "60 квартир в 3 блоках", "60 مسكناً في 3 مبانٍ", "60 woningen in 3 blokken", "60 mieszkań w 3 blokach", "60 boliger i 3 bygg", "60 bostäder i 3 hus")
a(43, '5 homes', "5 viviendas", "5 logements", "5 Wohnungen", "5 квартир", "5 مساكن", "5 woningen", "5 mieszkań", "5 boliger", "5 bostäder")
a(44, 'Terraces, private gardens and rooftop solariums', "Terrazas, jardines privados y solariums en la azotea", "Terrasses, jardins privés et solariums sur le toit",
  "Terrassen, private Gärten und Dach-Solarien", "Террасы, частные сады и солярии на крыше", "تراسات وحدائق خاصة وسولاريوم على السطح",
  "Terrassen, privétuinen en solaria op het dak", "Tarasy, prywatne ogrody i solaria na dachu", "Terrasser, private hager og solterrasser på taket", "Terrasser, privata trädgårdar och solterrasser på taket")
a(45, 'A finished apartment close to the beach at Carvajal',
  "Un apartamento terminado cerca de la playa de Carvajal, en una promoción que se puede visitar y ver antes de decidir.",
  "Un appartement achevé près de la plage de Carvajal, dans un programme que l'on peut visiter et voir avant de décider.",
  "Eine fertiggestellte Wohnung nahe dem Strand von Carvajal, in einem Projekt, das Sie vor der Entscheidung besichtigen können.",
  "Готовая квартира рядом с пляжем Карвахаль в комплексе, который можно посетить и увидеть до принятия решения.",
  "شقة مكتملة قرب شاطئ كارفاخال في مشروع يمكن زيارته ومعاينته قبل اتخاذ القرار.",
  "Een afgerond appartement dicht bij het strand van Carvajal, in een project dat u kunt bezoeken en zien voordat u beslist.",
  "Ukończony apartament blisko plaży Carvajal w inwestycji, którą można odwiedzić i zobaczyć przed podjęciem decyzji.",
  "En ferdigstilt leilighet nær stranden i Carvajal, i et prosjekt du kan besøke og se før du bestemmer deg.",
  "En färdigställd lägenhet nära stranden i Carvajal, i ett projekt ni kan besöka och se innan ni bestämmer er.")
a(46, 'Buyers who want to see the home they are buying',
  "Compradores que quieren ver la vivienda que compran, terminada y amueblada, en lugar de juzgarla por un plano.",
  "Acheteurs qui veulent voir le logement qu'ils achètent, achevé et meublé, plutôt que de le juger sur plan.",
  "Käufer, die die Wohnung, die sie kaufen, fertig und möbliert sehen möchten, statt sie anhand eines Plans zu beurteilen.",
  "Покупатели, которые хотят увидеть покупаемую квартиру готовой и меблированной, а не судить о ней по плану.",
  "المشترون الذين يريدون رؤية المسكن الذي يشترونه مكتملاً ومفروشاً بدلاً من الحكم عليه من مخطط.",
  "Kopers die de woning die ze kopen afgewerkt en gemeubileerd willen zien, in plaats van te oordelen op basis van een plattegrond.",
  "Kupujący, którzy chcą zobaczyć kupowane mieszkanie ukończone i umeblowane, zamiast oceniać je na podstawie rzutu.",
  "Kjøpere som vil se boligen de kjøper ferdig og møblert, i stedet for å bedømme den ut fra en tegning.",
  "Köpare som vill se bostaden de köper färdig och möblerad, i stället för att bedöma den utifrån en ritning.")
a(47, 'Five homes are listed in a sixty-home development',
  "Cinco viviendas figuran en una promoción de sesenta ya construida, con dos plazas de aparcamiento y un trastero para cada una.",
  "Cinq logements figurent dans un programme de soixante déjà construit, avec deux places de stationnement et un débarras pour chacun.",
  "Fünf Wohnungen sind in einem bereits gebauten Projekt mit sechzig Wohnungen gelistet, jeweils mit zwei Stellplätzen und einem Abstellraum.",
  "Пять квартир значатся в продаже в уже построенном комплексе из шестидесяти, с двумя парковочными местами и кладовой у каждой.",
  "خمسة مساكن مدرجة في مشروع من ستين مسكناً شُيّد بالفعل، ولكل منها موقفا سيارات ومخزن.",
  "Vijf woningen staan vermeld in een al gebouwd project van zestig woningen, elk met twee parkeerplaatsen en een berging.",
  "Pięć mieszkań figuruje w już wybudowanej inwestycji obejmującej sześćdziesiąt lokali, każde z dwoma miejscami parkingowymi i komórką lokatorską.",
  "Fem boliger er oppført i et allerede bygget prosjekt med seksti boliger, hver med to parkeringsplasser og en bod.",
  "Fem bostäder är angivna i ett redan byggt projekt med sextio bostäder, var och en med två parkeringsplatser och ett förråd.")
a(48, 'Carvajal beach and a commuter-train stop are close',
  "La playa de Carvajal y una parada de tren de cercanías están cerca, Fuengirola queda a unos cinco minutos en coche y el aeropuerto de Málaga a unos veinte.",
  "La plage de Carvajal et un arrêt de train de banlieue sont proches, Fuengirola est à environ cinq minutes en voiture et l'aéroport de Malaga à une vingtaine.",
  "Der Strand von Carvajal und eine Haltestelle der Nahverkehrsbahn sind nah, Fuengirola ist mit dem Auto in etwa fünf Minuten erreichbar und der Flughafen Málaga in etwa zwanzig.",
  "Пляж Карвахаль и остановка пригородного поезда рядом, до Фуэнхиролы около пяти минут на машине, до аэропорта Малаги около двадцати.",
  "شاطئ كارفاخال ومحطة قطار الضواحي قريبان، وفوينخيرولا على بُعد نحو خمس دقائق بالسيارة ومطار مالقة نحو عشرين.",
  "Het strand van Carvajal en een halte van de forenzentrein zijn dichtbij, Fuengirola ligt op ongeveer vijf minuten met de auto en de luchthaven van Málaga op ongeveer twintig.",
  "Plaża Carvajal i przystanek pociągu podmiejskiego są blisko, do Fuengirola jest około pięciu minut samochodem, a do lotniska w Maladze około dwudziestu.",
  "Stranden i Carvajal og et stoppested for lokaltoget ligger nær, Fuengirola er omtrent fem minutter unna med bil og Málaga lufthavn omtrent tjue.",
  "Stranden i Carvajal och en pendeltågshållplats ligger nära, Fuengirola är ungefär fem minuter bort med bil och Málagas flygplats ungefär tjugo.")
a(49, 'Five of the sixty homes are currently listed',
  "Cinco de las sesenta viviendas figuran ahora como disponibles. Nueva Living vuelve a confirmar con la promotora el precio y la disponibilidad antes de cualquier visita.",
  "Cinq des soixante logements figurent actuellement comme disponibles. Nueva Living reconfirme auprès du promoteur le prix et la disponibilité avant toute visite.",
  "Fünf der sechzig Wohnungen sind derzeit als verfügbar gelistet. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung erneut beim Bauträger.",
  "Сейчас в продаже пять из шестидесяти квартир. Nueva Living повторно подтверждает у застройщика цену и наличие до любого просмотра.",
  "خمسة من الستين مسكناً مدرجة حالياً كمتاحة. تعيد Nueva Living تأكيد السعر والتوفر مع المطور قبل أي معاينة.",
  "Vijf van de zestig woningen staan momenteel als beschikbaar vermeld. Nueva Living bevestigt prijs en beschikbaarheid opnieuw bij de ontwikkelaar vóór elke bezichtiging.",
  "Pięć z sześćdziesięciu mieszkań figuruje obecnie jako dostępne. Nueva Living ponownie potwierdza u dewelopera cenę i dostępność przed każdym oglądaniem.",
  "Fem av de seksti boligene er for tiden oppført som tilgjengelige. Nueva Living bekrefter pris og tilgjengelighet på nytt med utvikleren før enhver visning.",
  "Fem av de sextio bostäderna är just nu angivna som tillgängliga. Nueva Living bekräftar pris och tillgänglighet på nytt med byggherren före varje visning.")
a(50, 'Three blocks, <em>stepped down the slope</em>', "Tres bloques, <em>escalonados en la ladera</em>", "Trois blocs, <em>en gradins sur la pente</em>", "Drei Blöcke, <em>gestaffelt am Hang</em>",
  "Три блока, <em>террасами по склону</em>", "ثلاثة مبانٍ، <em>متدرجة على المنحدر</em>", "Drie blokken, <em>trapsgewijs langs de helling</em>", "Trzy bloki, <em>kaskadowo na zboczu</em>", "Tre bygg, <em>trinnvis nedover skråningen</em>", "Tre hus, <em>i trappsteg nedför sluttningen</em>")
a(51, 'The blocks follow the slope in stepped platforms',
  "Los bloques siguen la pendiente en plataformas escalonadas, con grandes terrazas enmarcadas por volúmenes irregulares a modo de pórticos y rematadas con barandillas de vidrio, de modo que la mayoría de las viviendas miran al mar, a las montañas o a los jardines comunes. Parte de las terrazas del último piso están cubiertas por pérgolas que filtran la luz, mientras que las plantas bajas tienen porches cubiertos y terrazas descubiertas.",
  "Les blocs suivent la pente en plateformes étagées, avec de grandes terrasses encadrées par des volumes irréguliers à la manière de portiques et terminées par des garde-corps en verre, de sorte que la plupart des logements donnent sur la mer, les montagnes ou les jardins communs. Une partie des terrasses du dernier étage est couverte de pergolas qui filtrent la lumière, tandis que les rez-de-chaussée ont des porches couverts et des terrasses découvertes.",
  "Die Blöcke folgen dem Hang in gestaffelten Plattformen, mit großen Terrassen, die von unregelmäßigen, portikusartigen Baukörpern gerahmt und mit Glasbrüstungen abgeschlossen sind, sodass die meisten Wohnungen auf das Meer, die Berge oder die gemeinsamen Gärten blicken. Ein Teil der Terrassen im obersten Geschoss ist mit Pergolen überdacht, die das Licht filtern, während die Erdgeschosse überdachte Vorbauten und offene Terrassen haben.",
  "Блоки следуют склону ступенчатыми платформами: большие террасы обрамлены неровными объёмами наподобие портиков и завершены стеклянными ограждениями, поэтому из большинства квартир открывается вид на море, горы или общие сады. Часть террас верхнего этажа закрыта перголами, рассеивающими свет, а на первых этажах есть крытые портики и открытые террасы.",
  "تتبع المباني المنحدر عبر منصات متدرجة، مع تراسات كبيرة تؤطرها كتل غير منتظمة على هيئة أروقة وتنتهي بدرابزينات زجاجية، فتطل معظم المساكن على البحر أو الجبال أو الحدائق المشتركة. وجزء من تراسات الطابق الأخير مغطى ببرغولات تصفّي الضوء، بينما تضم الطوابق الأرضية أروقة مغطاة وتراسات مكشوفة.",
  "De blokken volgen de helling in getrapte platforms, met grote terrassen omlijst door onregelmatige volumes als portieken en afgewerkt met glazen balustrades, zodat de meeste woningen uitkijken op de zee, de bergen of de gemeenschappelijke tuinen. Een deel van de terrassen op de bovenste verdieping is overdekt met pergola’s die het licht filteren, terwijl de begane grond overdekte veranda’s en open terrassen heeft.",
  "Bloki podążają za zboczem w kaskadowych platformach, z dużymi tarasami obramowanymi nieregularnymi bryłami na wzór portyków i wykończonymi szklanymi balustradami, dzięki czemu większość mieszkań ma widok na morze, góry lub wspólne ogrody. Część tarasów na najwyższej kondygnacji przykrywają pergole filtrujące światło, a parter ma zadaszone ganki i otwarte tarasy.",
  "Byggene følger skråningen i trinnvise plattformer, med store terrasser innrammet av uregelmessige volumer som minner om portikuser og avsluttet med glassrekkverk, slik at de fleste boligene vender mot havet, fjellene eller de felles hagene. En del av terrassene i øverste etasje er dekket av pergolaer som filtrerer lyset, mens første etasje har overbygde verandaer og åpne terrasser.",
  "Husen följer sluttningen i trappstegsformade plattformar, med stora terrasser inramade av oregelbundna volymer som liknar portiker och avslutade med glasräcken, så att de flesta bostäderna vetter mot havet, bergen eller de gemensamma trädgårdarna. En del av terrasserna på översta våningen täcks av pergolor som filtrerar ljuset, medan bottenvåningarna har övertäckta verandor och öppna terrasser.")
a(52, 'The facades are cement render and paint',
  "Las fachadas son de enfoscado de cemento y pintura, con celosías metálicas lacadas que destacan algunos volúmenes, núcleos de escaleras y galerías. Los bloques 2 y 3 están situados más abajo en la ladera que el bloque 1, lo que conserva las vistas al mar de las viviendas superiores.",
  "Les façades sont en enduit de ciment et peinture, avec des claustras métalliques laquées qui soulignent certains volumes, cages d'escalier et galeries. Les blocs 2 et 3 sont implantés plus bas sur la pente que le bloc 1, ce qui préserve la vue sur la mer des logements situés au-dessus.",
  "Die Fassaden sind in Zementputz und Anstrich ausgeführt, mit lackierten Metallelementen, die einzelne Baukörper, Treppenhäuser und Galerien hervorheben. Die Blöcke 2 und 3 liegen tiefer am Hang als Block 1, was den Meerblick der darüber liegenden Wohnungen erhält.",
  "Фасады выполнены из цементной штукатурки с покраской; отдельные объёмы, лестничные клетки и галереи подчёркнуты лакированными металлическими экранами. Блоки 2 и 3 расположены ниже по склону, чем блок 1, что сохраняет вид на море из квартир выше.",
  "الواجهات من لياسة الإسمنت والدهان، مع ستائر معدنية مطلية تبرز بعض الكتل وأبراج السلالم والممرات. ويقع المبنى 2 والمبنى 3 في موضع أدنى على المنحدر من المبنى 1، مما يحافظ على إطلالة البحر للمساكن الأعلى.",
  "De gevels zijn uitgevoerd in cementstuc en verf, met gelakte metalen schermen die enkele volumes, trappenhuizen en galerijen benadrukken. Blok 2 en 3 liggen lager op de helling dan blok 1, waardoor de woningen erboven hun zeezicht behouden.",
  "Elewacje wykończono tynkiem cementowym i farbą, a niektóre bryły, klatki schodowe i galerie podkreślają lakierowane metalowe ekrany. Bloki 2 i 3 leżą niżej na zboczu niż blok 1, co zachowuje widok na morze z mieszkań położonych wyżej.",
  "Fasadene er utført i sementpuss og maling, med lakkerte metallskjermer som fremhever enkelte volumer, trappeoppganger og gallerier. Bygg 2 og 3 ligger lavere i skråningen enn bygg 1, noe som bevarer havutsikten fra boligene over.",
  "Fasaderna är utförda i cementputs och färg, med lackerade metallskärmar som framhäver vissa volymer, trapphus och gallerier. Hus 2 och 3 ligger lägre i sluttningen än hus 1, vilket bevarar havsutsikten från bostäderna ovanför.")
a(53, 'Source: the developer’s quality memorandum for this development',
  "Fuente: la memoria de calidades de la promotora para esta promoción, generada el 8 de octubre de 2026. Algunos elementos varían según el tipo de vivienda. La memoria es de la promotora y Nueva Living la pide por escrito antes de cualquier reserva.",
  "Source : le descriptif de la qualité du promoteur pour ce programme, généré le 8 octobre 2026. Certains éléments varient selon le type de logement. Le descriptif est celui du promoteur et Nueva Living le demande par écrit avant toute réservation.",
  "Quelle: die Qualitätsbeschreibung des Bauträgers für dieses Projekt, erstellt am 8. Oktober 2026. Einzelne Punkte hängen vom Wohnungstyp ab. Die Beschreibung stammt vom Bauträger, und Nueva Living fordert sie vor jeder Reservierung schriftlich an.",
  "Источник: описание качества и оснащения от застройщика для этого комплекса, сформированное 8 октября 2026 года. Некоторые пункты зависят от типа квартиры. Документ принадлежит застройщику, и Nueva Living запрашивает его в письменном виде до любого бронирования.",
  "المصدر: مذكرة الجودة الخاصة بالمطور لهذا المشروع، الصادرة في 8 أكتوبر 2026. تختلف بعض البنود بحسب نوع المسكن. المذكرة من إعداد المطور وتطلبها Nueva Living كتابةً قبل أي حجز.",
  "Bron: de kwaliteitsomschrijving van de ontwikkelaar voor dit project, opgesteld op 8 oktober 2026. Sommige onderdelen verschillen per woningtype. De omschrijving is die van de ontwikkelaar en Nueva Living vraagt haar schriftelijk op vóór elke reservering.",
  "Źródło: opis jakości dewelopera dla tej inwestycji, wygenerowany 8 października 2026 roku. Niektóre pozycje różnią się w zależności od typu lokalu. Opis pochodzi od dewelopera, a Nueva Living prosi o niego na piśmie przed jakąkolwiek rezerwacją.",
  "Kilde: utviklerens kvalitetsbeskrivelse for dette prosjektet, generert 8. oktober 2026. Enkelte punkter varierer etter boligtype. Beskrivelsen er utviklerens, og Nueva Living ber om den skriftlig før enhver reservasjon.",
  "Källa: byggherrens kvalitetsbeskrivning för detta projekt, framtagen den 8 oktober 2026. Vissa punkter varierar efter bostadstyp. Beskrivningen är byggherrens, och Nueva Living begär den skriftligt före varje reservation.")

# ---------------------------------------------------------------- quality specification
a(54, 'Rectified porcelain floors throughout', "Suelos de gres porcelánico rectificado en toda la vivienda y alicatado cerámico en los baños.", "Sols en grès cérame rectifié dans tout le logement et faïence murale dans les salles de bains.",
  "Bodenbeläge aus kalibriertem Feinsteinzeug in der gesamten Wohnung und Keramikfliesen an den Wänden der Bäder.", "Полы из ректифицированного керамогранита во всей квартире и керамическая плитка на стенах в ванных комнатах.",
  "أرضيات من البورسلين المقصوص بدقة في كامل المسكن وكسوة جدران من السيراميك في الحمامات.", "Vloeren van gerectificeerd porseleintegels in de hele woning en keramische wandtegels in de badkamers.",
  "Podłogi z gresu porcelanowego rektyfikowanego w całym lokalu i ceramiczna glazura w łazienkach.", "Rektifiserte porselensfliser på gulvet i hele boligen og keramiske veggfliser på badene.",
  "Golv av rektifierat porslinsgolv i hela bostaden och keramiskt kakel på väggarna i badrummen.")
a(55, 'Lacquered interior doors', "Puertas interiores lacadas de {N2.10} {M} de altura, con alma maciza y cierre amortiguado.", "Portes intérieures laquées de {N2.10} {M} de hauteur, à âme pleine et fermeture amortie.",
  "Lackierte Innentüren mit {N2.10} {M} Höhe, mit Vollkern und gedämpftem Schließen.", "Лакированные межкомнатные двери высотой {N2.10} {M} с цельным полотном и плавным закрыванием.",
  "أبواب داخلية مطلية بارتفاع {N2.10} {M} بقلب مصمت وإغلاق هادئ.", "Gelakte binnendeuren van {N2.10} {M} hoog, met massieve kern en zacht sluitende werking.",
  "Lakierowane drzwi wewnętrzne o wysokości {N2.10} {M}, z pełnym rdzeniem i cichym domykaniem.", "Lakkerte innerdører på {N2.10} {M} i høyden, med massiv kjerne og myk lukking.",
  "Lackade innerdörrar med en höjd på {N2.10} {M}, med massiv kärna och mjuk stängning.")
a(56, 'Fitted wardrobes in every bedroom', "Armarios empotrados en todos los dormitorios, con puertas correderas, interior forrado, cajones, baldas y barra.", "Placards intégrés dans toutes les chambres, avec portes coulissantes, intérieur habillé, tiroirs, étagères et barre de penderie.",
  "Einbauschränke in allen Schlafzimmern, mit Schiebetüren, ausgekleidetem Innenraum, Schubladen, Einlegeböden und Kleiderstange.", "Встроенные шкафы во всех спальнях, с раздвижными дверями, отделанным внутри корпусом, ящиками, полками и штангой.",
  "خزائن مدمجة في جميع غرف النوم، بأبواب منزلقة وداخل مبطّن وأدراج ورفوف وعمود تعليق.", "Inbouwkasten in alle slaapkamers, met schuifdeuren, bekleed interieur, laden, planken en een kledingroede.",
  "Szafy wnękowe we wszystkich sypialniach, z drzwiami przesuwnymi, wyłożonym wnętrzem, szufladami, półkami i drążkiem.", "Innebygde garderobeskap i alle soverom, med skyvedører, kledd innside, skuffer, hyller og kleshenger.",
  "Inbyggda garderober i alla sovrum, med skjutdörrar, klätt insida, lådor, hyllor och klädstång.")
a(57, 'Ducted air conditioning, heating and hot water', "Climatización por conductos, calefacción y agua caliente mediante una bomba de calor de aerotermia.", "Climatisation par conduits, chauffage et eau chaude par une pompe à chaleur aérothermique.",
  "Kanalklimaanlage, Heizung und Warmwasser über eine Luft-Wasser-Wärmepumpe.", "Канальное кондиционирование, отопление и горячая вода от аэротермального теплового насоса.",
  "تكييف بالمجاري وتدفئة وماء ساخن من مضخة حرارية هوائية.", "Airconditioning via kanalen, verwarming en warm water via een lucht-waterwarmtepomp.",
  "Klimatyzacja kanałowa, ogrzewanie i ciepła woda z pompy ciepła aerotermicznej.", "Kanalbasert klimaanlegg, oppvarming og varmtvann fra en luft-vann-varmepumpe.",
  "Kanalbaserad luftkonditionering, uppvärmning och varmvatten från en luft-vattenvärmepump.")
a(58, 'Underfloor heating throughout the home', "Suelo radiante en toda la vivienda y suelo radiante eléctrico en los baños.", "Plancher chauffant dans tout le logement et plancher chauffant électrique dans les salles de bains.",
  "Fußbodenheizung in der gesamten Wohnung und elektrische Fußbodenheizung in den Bädern.", "Тёплый пол во всей квартире и электрический тёплый пол в ванных комнатах.",
  "تدفئة أرضية في كامل المسكن وتدفئة أرضية كهربائية في الحمامات.", "Vloerverwarming in de hele woning en elektrische vloerverwarming in de badkamers.",
  "Ogrzewanie podłogowe w całym lokalu i elektryczne ogrzewanie podłogowe w łazienkach.", "Gulvvarme i hele boligen og elektrisk gulvvarme på badene.", "Golvvärme i hela bostaden och elektrisk golvvärme i badrummen.")
a(59, 'Fitted kitchen with a quartz worktop', "Cocina equipada con encimera de cuarzo, fregadero bajo encimera y cajones de cierre amortiguado.", "Cuisine équipée avec plan de travail en quartz, évier sous plan et tiroirs à fermeture amortie.",
  "Einbauküche mit Quarzarbeitsplatte, Unterbauspüle und gedämpft schließenden Schubladen.", "Кухня с кварцевой столешницей, врезной мойкой и ящиками с плавным закрыванием.",
  "مطبخ مجهز بسطح عمل من الكوارتز وحوض مدمج تحت السطح وأدراج بإغلاق هادئ.", "Ingerichte keuken met kwartsblad, onderbouwspoelbak en zacht sluitende laden.",
  "Wyposażona kuchnia z blatem kwarcowym, zlewem podblatowym i szufladami z cichym domykaniem.", "Utstyrt kjøkken med kvartsbenkeplate, nedfelt vask og skuffer med myk lukking.",
  "Utrustat kök med bänkskiva i kvarts, underlimmad diskho och lådor med mjuk stängning.")
a(60, 'Appliances included: extractor hood', "Electrodomésticos incluidos: campana extractora, horno, frigorífico, placa de inducción, lavavajillas, microondas y lavadora en la galería.", "Électroménager inclus : hotte, four, réfrigérateur, plaque à induction, lave-vaisselle, micro-ondes et lave-linge dans la galerie.",
  "Geräte inklusive: Dunstabzugshaube, Backofen, Kühlschrank, Induktionskochfeld, Geschirrspüler, Mikrowelle und Waschmaschine in der Waschküche.", "Техника в комплекте: вытяжка, духовой шкаф, холодильник, индукционная панель, посудомоечная машина, микроволновая печь и стиральная машина в подсобной галерее.",
  "الأجهزة مشمولة: شفاط وفرن وثلاجة وموقد حثي وغسالة أطباق وميكروويف وغسالة ملابس في الرواق الخدمي.", "Apparatuur inbegrepen: afzuigkap, oven, koelkast, inductiekookplaat, vaatwasser, magnetron en een wasmachine in de bijkeuken.",
  "W cenie sprzęt: okap, piekarnik, lodówka, płyta indukcyjna, zmywarka, mikrofalówka i pralka w galerii gospodarczej.", "Hvitevarer inkludert: ventilator, ovn, kjøleskap, induksjonstopp, oppvaskmaskin, mikrobølgeovn og vaskemaskin i vaskegalleriet.",
  "Apparater inkluderade: köksfläkt, ugn, kylskåp, induktionshäll, diskmaskin, mikrovågsugn och tvättmaskin i tvättgalleriet.")
a(61, 'Hansgrohe taps and sanitaryware', "Grifería y sanitarios Hansgrohe, plato de ducha de resina acabado pizarra con mampara y rociador de lluvia de 30 x 30 cm en el baño principal.", "Robinetterie et sanitaires Hansgrohe, receveur de douche en résine finition ardoise avec paroi, et douche de pluie de 30 x 30 cm dans la salle de bains principale.",
  "Armaturen und Sanitärobjekte von Hansgrohe, Duschwanne aus Kunstharz in Schieferoptik mit Duschabtrennung und Regendusche von 30 x 30 cm im Hauptbad.", "Смесители и сантехника Hansgrohe, душевой поддон из смолы под сланец с ограждением и тропический душ 30 x 30 см в главной ванной комнате.",
  "حنفيات وأدوات صحية من Hansgrohe، وحوض دش من الراتنج بلمسة أردواز مع حاجز، ورشاش مطري بقياس 30 × 30 سم في الحمام الرئيسي.", "Kranen en sanitair van Hansgrohe, een douchebak van hars met leisteenafwerking en douchewand, en een regendouche van 30 x 30 cm in de hoofdbadkamer.",
  "Baterie i armatura Hansgrohe, brodzik z żywicy w wykończeniu łupkowym z kabiną oraz deszczownica 30 x 30 cm w głównej łazience.", "Hansgrohe-armaturer og sanitærutstyr, dusjkar i harpiks med skiferfinish og dusjvegg, og en regndusj på 30 x 30 cm i hovedbadet.",
  "Blandare och sanitetsporslin från Hansgrohe, ett duschkar i harts med skiffertextur och duschvägg, och en regndusch på 30 x 30 cm i huvudbadrummet.")
a(62, 'Wall-hung vanity units with a mirror and LED lighting', "Muebles de lavabo suspendidos con espejo e iluminación LED, y cisternas empotradas.", "Meubles de salle de bains suspendus avec miroir et éclairage LED, et réservoirs encastrés.",
  "Wandhängende Waschtischunterschränke mit Spiegel und LED-Beleuchtung sowie Unterputzspülkästen.", "Подвесные тумбы под раковину с зеркалом и светодиодной подсветкой, скрытые бачки.",
  "وحدات مغاسل معلقة بمرآة وإضاءة LED وخزانات مخفية.", "Hangende wastafelmeubels met spiegel en ledverlichting, en inbouwreservoirs.",
  "Podwieszane szafki umywalkowe z lustrem i oświetleniem LED oraz ukryte spłuczki.", "Vegghengte servantskap med speil og LED-belysning, og skjult sisterne.", "Väggmonterade tvättställsskåp med spegel och LED-belysning, och dold cistern.")
a(63, 'High-performance PVC windows', "Carpintería de PVC de altas prestaciones con doble acristalamiento y vidrio laminado de seguridad en las balconeras.", "Menuiseries en PVC hautes performances à double vitrage, avec verre feuilleté de sécurité sur les baies coulissantes.",
  "Hochwertige PVC-Fenster mit Doppelverglasung und Verbundsicherheitsglas in den Schiebetüren.", "Высококачественные окна из ПВХ с двойным остеклением и ламинированным безопасным стеклом в раздвижных дверях.",
  "نوافذ من PVC عالية الأداء بزجاج مزدوج وزجاج مصفّح للأمان في الأبواب المنزلقة.", "Hoogwaardige pvc-kozijnen met dubbele beglazing en gelaagd veiligheidsglas in de schuifpuien.",
  "Wysokiej jakości okna PVC z podwójnym szkleniem i szkłem laminowanym bezpiecznym w drzwiach przesuwnych.", "Høyytelses PVC-vinduer med dobbeltglass og laminert sikkerhetsglass i skyvedørene.",
  "Högpresterande PVC-fönster med dubbelglas och laminerat säkerhetsglas i skjutdörrarna.")
a(64, 'Motorised aluminium roller shutters', "Persianas enrollables de aluminio motorizadas en las puertas correderas del salón y del dormitorio principal.", "Volets roulants en aluminium motorisés sur les baies coulissantes du séjour et de la chambre principale.",
  "Motorisierte Aluminium-Rollläden an den Schiebetüren von Wohnzimmer und Hauptschlafzimmer.", "Электрические алюминиевые рольставни на раздвижных дверях гостиной и главной спальни.",
  "ستائر ألومنيوم قابلة للطي بمحرك على الأبواب المنزلقة في غرفة المعيشة وغرفة النوم الرئيسية.", "Gemotoriseerde aluminium rolluiken op de schuifpuien van de woonkamer en de hoofdslaapkamer.",
  "Rolety aluminiowe na napędzie elektrycznym na drzwiach przesuwnych salonu i głównej sypialni.", "Motoriserte aluminiumspersienner på skyvedørene i stuen og hovedsoverommet.",
  "Motoriserade aluminiumrullgardiner på skjutdörrarna i vardagsrummet och huvudsovrummet.")
a(65, 'A reinforced security door', "Puerta de entrada acorazada.", "Porte d'entrée blindée.", "Eine einbruchhemmende Wohnungseingangstür.", "Бронированная входная дверь.", "باب دخول مدرّع.", "Een pantserdeur als voordeur.", "Drzwi wejściowe antywłamaniowe.", "En sikkerhetsdør til boligen.", "En säkerhetsdörr till bostaden.")
a(66, 'Outdoors and solarium', "Exteriores y solárium", "Extérieurs et solarium", "Außenbereiche und Solarium", "Открытые пространства и солярий", "المساحات الخارجية والسولاريوم", "Buitenruimtes en solarium", "Przestrzenie zewnętrzne i solarium", "Utendørs og solterrasse", "Utomhus och solterrass")
a(67, 'Non-slip porcelain paving', "Solado de gres antideslizante en porches, terrazas, galerías y soláriums.", "Dallage en grès cérame antidérapant sur les porches, terrasses, galeries et solariums.",
  "Rutschhemmende Feinsteinzeugbeläge auf Vorbauten, Terrassen, Galerien und Solarien.", "Нескользящее покрытие из керамогранита на портиках, террасах, галереях и солярии.",
  "أرضيات من البورسلين المانع للانزلاق في الأروقة والتراسات والممرات والسولاريوم.", "Antislip porseleintegels op veranda’s, terrassen, galerijen en solaria.",
  "Antypoślizgowa kostka gresowa na gankach, tarasach, galeriach i solariach.", "Sklisikre porselensfliser på verandaer, terrasser, gallerier og solterrasser.", "Halkfritt porslinsgolv på verandor, terrasser, gallerier och solterrasser.")
a(68, 'Private solariums on the third-floor homes of Block 1',
  "Solariums privados en las viviendas de la tercera planta del bloque 1, a los que se sube por una escalera privada con trampilla de techo motorizada, con barbacoa, ducha de agua fría y caliente, tomas de corriente y de TV y preinstalación para un jacuzzi.",
  "Solariums privés dans les logements du troisième étage du bloc 1, accessibles par un escalier privé à trappe de toit motorisée, avec barbecue, douche d'eau chaude et froide, prises électriques et TV et pré-équipement pour un jacuzzi.",
  "Private Solarien in den Wohnungen im dritten Obergeschoss von Block 1, erreichbar über eine private Treppe mit motorisierter Dachluke, mit Grill, Dusche mit Warm- und Kaltwasser, Strom- und TV-Anschlüssen und Vorinstallation für einen Whirlpool.",
  "Частные солярии в квартирах четвёртого этажа блока 1, на которые ведёт частная лестница с электрическим люком в крыше; на солярии есть гриль, душ с горячей и холодной водой, розетки для электропитания и ТВ и подготовка под джакузи.",
  "سولاريوم خاص في مساكن الطابق الثالث بالمبنى 1، يُصعد إليه بدرج خاص بفتحة سقف بمحرك، مع شواية ودش بماء بارد وساخن ومنافذ كهرباء وتلفزيون وتجهيز مسبق لجاكوزي.",
  "Privésolaria bij de woningen op de derde verdieping van blok 1, bereikbaar via een eigen trap met gemotoriseerd dakluik, met barbecue, douche met warm en koud water, stroom- en tv-aansluitingen en voorbereiding voor een bubbelbad.",
  "Prywatne solaria przy lokalach na trzecim piętrze bloku 1, do których prowadzą prywatne schody z włazem dachowym na napędzie elektrycznym, z grillem, prysznicem z ciepłą i zimną wodą, gniazdami zasilania i TV oraz instalacją pod jacuzzi.",
  "Private solterrasser ved boligene i fjerde etasje i bygg 1, nådd via en privat trapp med motorisert takluke, med grill, dusj med varmt og kaldt vann, strøm- og TV-uttak og forberedelse for boblebad.",
  "Privata solterrasser vid bostäderna på tredje våningen i hus 1, nås via en privat trappa med motoriserad takluck, med grill, dusch med varmt och kallt vatten, el- och TV-uttag och förberedelse för bubbelpool.")
a(69, 'Parking and technology', "Aparcamiento y tecnología", "Stationnement et technologie", "Stellplätze und Technik", "Парковка и технологии", "المواقف والتقنية", "Parkeren en techniek", "Parking i technologia", "Parkering og teknologi", "Parkering och teknik")
a(70, 'Two parking spaces and a storeroom in the basement', "Dos plazas de aparcamiento y un trastero en el sótano para cada vivienda, con canalización para un cargador de coche eléctrico en cada plaza.", "Deux places de stationnement et un débarras au sous-sol pour chaque logement, avec gaine pour une borne de recharge de voiture électrique à chaque place.",
  "Zwei Stellplätze und ein Abstellraum im Untergeschoss für jede Wohnung, mit Leerrohr für eine Ladestation für Elektroautos an jedem Stellplatz.", "Два парковочных места и кладовая в цоколе для каждой квартиры, с подготовкой кабельного канала под зарядку электромобиля на каждом месте.",
  "موقفا سيارات ومخزن في القبو لكل مسكن، مع مجرى لتركيب شاحن سيارة كهربائية في كل موقف.", "Twee parkeerplaatsen en een berging in de kelder voor elke woning, met een leiding voor een laadpunt voor elektrische auto’s bij elke plaats.",
  "Dwa miejsca parkingowe i komórka lokatorska w piwnicy dla każdego lokalu, z kanałem pod ładowarkę samochodu elektrycznego przy każdym miejscu.", "To parkeringsplasser og en bod i kjelleren for hver bolig, med trekkerør for ladepunkt til elbil ved hver plass.",
  "Två parkeringsplatser och ett förråd i källaren för varje bostad, med kanalisation för laddning av elbil vid varje plats.")
a(71, 'Fibre broadband', "Fibra óptica, un router wifi en el salón y wifi comunitario en las zonas comunes.", "Fibre optique, un routeur Wi-Fi dans le séjour et Wi-Fi communautaire dans les espaces communs.",
  "Glasfaser-Internet, ein WLAN-Router im Wohnzimmer und Gemeinschafts-WLAN in den Gemeinschaftsbereichen.", "Оптоволоконный интернет, Wi-Fi-роутер в гостиной и общий Wi-Fi в общественных зонах.",
  "إنترنت بالألياف الضوئية وجهاز واي فاي في غرفة المعيشة وشبكة واي فاي مشتركة في المساحات العامة.", "Glasvezelinternet, een wifirouter in de woonkamer en gemeenschappelijke wifi in de gedeelde ruimtes.",
  "Internet światłowodowy, router Wi-Fi w salonie i wspólne Wi-Fi w częściach wspólnych.", "Fiberbredbånd, en Wi-Fi-ruter i stuen og felles Wi-Fi i fellesområdene.", "Fiberbredband, en wifi-router i vardagsrummet och gemensamt wifi i de gemensamma ytorna.")
a(72, 'Five homes, <em>ground floor or penthouse</em>', "Cinco viviendas, <em>planta baja o ático</em>", "Cinq logements, <em>rez-de-chaussée ou penthouse</em>", "Fünf Wohnungen, <em>Erdgeschoss oder Penthouse</em>",
  "Пять квартир, <em>первый этаж или пентхаус</em>", "خمسة مساكن، <em>في الطابق الأرضي أو بنتهاوس</em>", "Vijf woningen, <em>begane grond of penthouse</em>", "Pięć lokali, <em>parter lub penthouse</em>", "Fem boliger, <em>første etasje eller toppleilighet</em>", "Fem bostäder, <em>bottenvåning eller takvåning</em>")
a(73, 'Three ground-floor apartments, two with two bedrooms',
  "Tres apartamentos de planta baja, dos de dos dormitorios y uno de tres, y dos áticos de la tercera planta con dos dormitorios y solárium en la azotea. Los cinco están en el bloque 1.",
  "Trois appartements en rez-de-chaussée, deux de deux chambres et un de trois, et deux penthouses au troisième étage de deux chambres avec solarium sur le toit. Les cinq sont dans le bloc 1.",
  "Drei Erdgeschosswohnungen, zwei mit zwei Schlafzimmern und eine mit drei, und zwei Penthouses im dritten Obergeschoss mit zwei Schlafzimmern und Dach-Solarium. Alle fünf liegen in Block 1.",
  "Три квартиры на первом этаже, две с двумя спальнями и одна с тремя, и два пентхауса на четвёртом этаже с двумя спальнями и солярием на крыше. Все пять находятся в блоке 1.",
  "ثلاث شقق في الطابق الأرضي، اثنتان بغرفتي نوم وواحدة بثلاث غرف، وبنتهاوسان في الطابق الثالث بغرفتي نوم وسولاريوم على السطح. جميعها الخمسة في المبنى 1.",
  "Drie appartementen op de begane grond, twee met twee slaapkamers en één met drie, en twee penthouses op de derde verdieping met twee slaapkamers en een solarium op het dak. Alle vijf liggen in blok 1.",
  "Trzy apartamenty na parterze, dwa z dwiema sypialniami i jeden z trzema, oraz dwa penthouse’y na trzecim piętrze z dwiema sypialniami i solarium na dachu. Wszystkie pięć znajduje się w bloku 1.",
  "Tre leiligheter i første etasje, to med to soverom og én med tre, og to toppleiligheter i fjerde etasje med to soverom og solterrasse på taket. Alle fem ligger i bygg 1.",
  "Tre lägenheter på bottenvåningen, två med två sovrum och en med tre, och två takvåningar på tredje våningen med två sovrum och solterrass på taket. Alla fem ligger i hus 1.")

# ---------------------------------------------------------------- residences
a(74, 'Ground floor, Block 1, staircase 1.',
  "Planta baja, bloque 1, escalera 1. Salón comedor de {N22.31} {U}, cocina de {N6.29} {U}, dos dormitorios de {N13.06} y {N10.04} {U} y dos baños.",
  "Rez-de-chaussée, bloc 1, cage d'escalier 1. Séjour-salle à manger de {N22.31} {U}, cuisine de {N6.29} {U}, deux chambres de {N13.06} et {N10.04} {U} et deux salles de bains.",
  "Erdgeschoss, Block 1, Treppenhaus 1. Wohn- und Essbereich von {N22.31} {U}, Küche von {N6.29} {U}, zwei Schlafzimmer mit {N13.06} und {N10.04} {U} und zwei Bäder.",
  "Первый этаж, блок 1, подъезд 1. Гостиная-столовая {N22.31} {U}, кухня {N6.29} {U}, две спальни площадью {N13.06} и {N10.04} {U} и две ванные комнаты.",
  "الطابق الأرضي، المبنى 1، الدرج 1. غرفة معيشة وطعام بمساحة {N22.31} {U}، ومطبخ بمساحة {N6.29} {U}، وغرفتا نوم بمساحة {N13.06} و{N10.04} {U}، وحمامان.",
  "Begane grond, blok 1, trappenhuis 1. Woon- en eetkamer van {N22.31} {U}, keuken van {N6.29} {U}, twee slaapkamers van {N13.06} en {N10.04} {U} en twee badkamers.",
  "Parter, blok 1, klatka 1. Salon z jadalnią o powierzchni {N22.31} {U}, kuchnia {N6.29} {U}, dwie sypialnie o powierzchni {N13.06} i {N10.04} {U} oraz dwie łazienki.",
  "Første etasje, bygg 1, oppgang 1. Stue og spisestue på {N22.31} {U}, kjøkken på {N6.29} {U}, to soverom på {N13.06} og {N10.04} {U} og to bad.",
  "Bottenvåning, hus 1, trapphus 1. Vardagsrum och matplats på {N22.31} {U}, kök på {N6.29} {U}, två sovrum på {N13.06} och {N10.04} {U} och två badrum.")
a(75, 'A covered porch of 27.80 sqm and an open terrace',
  "Un porche cubierto de {N27.80} {U} y una terraza descubierta de {N20.55} {U}, con un jardín privado de {N33} {U}.",
  "Un porche couvert de {N27.80} {U} et une terrasse découverte de {N20.55} {U}, avec un jardin privé de {N33} {U}.",
  "Ein überdachter Vorbau von {N27.80} {U} und eine offene Terrasse von {N20.55} {U}, mit einem privaten Garten von {N33} {U}.",
  "Крытый портик {N27.80} {U} и открытая терраса {N20.55} {U}, с частным садом {N33} {U}.",
  "رواق مغطى بمساحة {N27.80} {U} وتراس مكشوف بمساحة {N20.55} {U}، مع حديقة خاصة بمساحة {N33} {U}.",
  "Een overdekte veranda van {N27.80} {U} en een open terras van {N20.55} {U}, met een privétuin van {N33} {U}.",
  "Zadaszony ganek o powierzchni {N27.80} {U} i otwarty taras {N20.55} {U}, z prywatnym ogrodem {N33} {U}.",
  "En overbygd veranda på {N27.80} {U} og en åpen terrasse på {N20.55} {U}, med en privat hage på {N33} {U}.",
  "En övertäckt veranda på {N27.80} {U} och en öppen terrass på {N20.55} {U}, med en privat trädgård på {N33} {U}.")
a(76, 'Ground floor, Block 1, staircase 4.',
  "Planta baja, bloque 1, escalera 4. Salón comedor de {N24.28} {U}, cocina de {N7.70} {U}, dos dormitorios de {N15.55} y {N10.13} {U} y dos baños.",
  "Rez-de-chaussée, bloc 1, cage d'escalier 4. Séjour-salle à manger de {N24.28} {U}, cuisine de {N7.70} {U}, deux chambres de {N15.55} et {N10.13} {U} et deux salles de bains.",
  "Erdgeschoss, Block 1, Treppenhaus 4. Wohn- und Essbereich von {N24.28} {U}, Küche von {N7.70} {U}, zwei Schlafzimmer mit {N15.55} und {N10.13} {U} und zwei Bäder.",
  "Первый этаж, блок 1, подъезд 4. Гостиная-столовая {N24.28} {U}, кухня {N7.70} {U}, две спальни площадью {N15.55} и {N10.13} {U} и две ванные комнаты.",
  "الطابق الأرضي، المبنى 1، الدرج 4. غرفة معيشة وطعام بمساحة {N24.28} {U}، ومطبخ بمساحة {N7.70} {U}، وغرفتا نوم بمساحة {N15.55} و{N10.13} {U}، وحمامان.",
  "Begane grond, blok 1, trappenhuis 4. Woon- en eetkamer van {N24.28} {U}, keuken van {N7.70} {U}, twee slaapkamers van {N15.55} en {N10.13} {U} en twee badkamers.",
  "Parter, blok 1, klatka 4. Salon z jadalnią o powierzchni {N24.28} {U}, kuchnia {N7.70} {U}, dwie sypialnie o powierzchni {N15.55} i {N10.13} {U} oraz dwie łazienki.",
  "Første etasje, bygg 1, oppgang 4. Stue og spisestue på {N24.28} {U}, kjøkken på {N7.70} {U}, to soverom på {N15.55} og {N10.13} {U} og to bad.",
  "Bottenvåning, hus 1, trapphus 4. Vardagsrum och matplats på {N24.28} {U}, kök på {N7.70} {U}, två sovrum på {N15.55} och {N10.13} {U} och två badrum.")
a(77, 'A covered porch of 34.98 sqm, with a private garden of 23 sqm.',
  "Un porche cubierto de {N34.98} {U}, con un jardín privado de {N23} {U}.", "Un porche couvert de {N34.98} {U}, avec un jardin privé de {N23} {U}.",
  "Ein überdachter Vorbau von {N34.98} {U}, mit einem privaten Garten von {N23} {U}.", "Крытый портик {N34.98} {U}, с частным садом {N23} {U}.",
  "رواق مغطى بمساحة {N34.98} {U}، مع حديقة خاصة بمساحة {N23} {U}.", "Een overdekte veranda van {N34.98} {U}, met een privétuin van {N23} {U}.",
  "Zadaszony ganek o powierzchni {N34.98} {U}, z prywatnym ogrodem {N23} {U}.", "En overbygd veranda på {N34.98} {U}, med en privat hage på {N23} {U}.", "En övertäckt veranda på {N34.98} {U}, med en privat trädgård på {N23} {U}.")
a(78, 'Ground floor, Block 1, staircase 5.',
  "Planta baja, bloque 1, escalera 5. Salón comedor de {N29.18} {U}, cocina de {N9.84} {U}, tres dormitorios de {N18.58}, {N11.06} y {N11.06} {U}, dos baños y un trastero dentro de la vivienda.",
  "Rez-de-chaussée, bloc 1, cage d'escalier 5. Séjour-salle à manger de {N29.18} {U}, cuisine de {N9.84} {U}, trois chambres de {N18.58}, {N11.06} et {N11.06} {U}, deux salles de bains et un débarras dans le logement.",
  "Erdgeschoss, Block 1, Treppenhaus 5. Wohn- und Essbereich von {N29.18} {U}, Küche von {N9.84} {U}, drei Schlafzimmer mit {N18.58}, {N11.06} und {N11.06} {U}, zwei Bäder und ein Abstellraum in der Wohnung.",
  "Первый этаж, блок 1, подъезд 5. Гостиная-столовая {N29.18} {U}, кухня {N9.84} {U}, три спальни площадью {N18.58}, {N11.06} и {N11.06} {U}, две ванные комнаты и кладовая внутри квартиры.",
  "الطابق الأرضي، المبنى 1، الدرج 5. غرفة معيشة وطعام بمساحة {N29.18} {U}، ومطبخ بمساحة {N9.84} {U}، وثلاث غرف نوم بمساحة {N18.58} و{N11.06} و{N11.06} {U}، وحمامان، ومخزن داخل المسكن.",
  "Begane grond, blok 1, trappenhuis 5. Woon- en eetkamer van {N29.18} {U}, keuken van {N9.84} {U}, drie slaapkamers van {N18.58}, {N11.06} en {N11.06} {U}, twee badkamers en een berging in de woning.",
  "Parter, blok 1, klatka 5. Salon z jadalnią o powierzchni {N29.18} {U}, kuchnia {N9.84} {U}, trzy sypialnie o powierzchni {N18.58}, {N11.06} i {N11.06} {U}, dwie łazienki i komórka wewnątrz lokalu.",
  "Første etasje, bygg 1, oppgang 5. Stue og spisestue på {N29.18} {U}, kjøkken på {N9.84} {U}, tre soverom på {N18.58}, {N11.06} og {N11.06} {U}, to bad og en bod inne i boligen.",
  "Bottenvåning, hus 1, trapphus 5. Vardagsrum och matplats på {N29.18} {U}, kök på {N9.84} {U}, tre sovrum på {N18.58}, {N11.06} och {N11.06} {U}, två badrum och ett förråd inne i bostaden.")
a(79, 'A covered porch of 57.28 sqm, with a private garden of 68 sqm.',
  "Un porche cubierto de {N57.28} {U}, con un jardín privado de {N68} {U}.", "Un porche couvert de {N57.28} {U}, avec un jardin privé de {N68} {U}.",
  "Ein überdachter Vorbau von {N57.28} {U}, mit einem privaten Garten von {N68} {U}.", "Крытый портик {N57.28} {U}, с частным садом {N68} {U}.",
  "رواق مغطى بمساحة {N57.28} {U}، مع حديقة خاصة بمساحة {N68} {U}.", "Een overdekte veranda van {N57.28} {U}, met een privétuin van {N68} {U}.",
  "Zadaszony ganek o powierzchni {N57.28} {U}, z prywatnym ogrodem {N68} {U}.", "En overbygd veranda på {N57.28} {U}, med en privat hage på {N68} {U}.", "En övertäckt veranda på {N57.28} {U}, med en privat trädgård på {N68} {U}.")
a(80, 'Third floor, Block 1, staircase 3.',
  "Tercera planta, bloque 1, escalera 3. Salón comedor de {N27.93} {U}, cocina de {N7.73} {U}, dos dormitorios de {N14.73} y {N10.44} {U}, dos baños y una escalera privada al solárium.",
  "Troisième étage, bloc 1, cage d'escalier 3. Séjour-salle à manger de {N27.93} {U}, cuisine de {N7.73} {U}, deux chambres de {N14.73} et {N10.44} {U}, deux salles de bains et un escalier privé vers le solarium.",
  "Drittes Obergeschoss, Block 1, Treppenhaus 3. Wohn- und Essbereich von {N27.93} {U}, Küche von {N7.73} {U}, zwei Schlafzimmer mit {N14.73} und {N10.44} {U}, zwei Bäder und eine private Treppe zum Solarium.",
  "Четвёртый этаж, блок 1, подъезд 3. Гостиная-столовая {N27.93} {U}, кухня {N7.73} {U}, две спальни площадью {N14.73} и {N10.44} {U}, две ванные комнаты и частная лестница на солярий.",
  "الطابق الثالث، المبنى 1، الدرج 3. غرفة معيشة وطعام بمساحة {N27.93} {U}، ومطبخ بمساحة {N7.73} {U}، وغرفتا نوم بمساحة {N14.73} و{N10.44} {U}، وحمامان، ودرج خاص إلى السولاريوم.",
  "Derde verdieping, blok 1, trappenhuis 3. Woon- en eetkamer van {N27.93} {U}, keuken van {N7.73} {U}, twee slaapkamers van {N14.73} en {N10.44} {U}, twee badkamers en een eigen trap naar het solarium.",
  "Trzecie piętro, blok 1, klatka 3. Salon z jadalnią o powierzchni {N27.93} {U}, kuchnia {N7.73} {U}, dwie sypialnie o powierzchni {N14.73} i {N10.44} {U}, dwie łazienki i prywatne schody na solarium.",
  "Fjerde etasje, bygg 1, oppgang 3. Stue og spisestue på {N27.93} {U}, kjøkken på {N7.73} {U}, to soverom på {N14.73} og {N10.44} {U}, to bad og en privat trapp til solterrassen.",
  "Tredje våningen, hus 1, trapphus 3. Vardagsrum och matplats på {N27.93} {U}, kök på {N7.73} {U}, två sovrum på {N14.73} och {N10.44} {U}, två badrum och en privat trappa till solterrassen.")
a(81, 'An open terrace of 30.74 sqm and a solarium of 94.75 sqm',
  "Una terraza descubierta de {N30.74} {U} y un solárium de {N94.75} {U} con barbacoa, ducha y preinstalación para un jacuzzi. La lista de precios indica que el mobiliario, el equipamiento, la decoración, el mobiliario de terraza y un jacuzzi están incluidos en este apartamento.",
  "Une terrasse découverte de {N30.74} {U} et un solarium de {N94.75} {U} avec barbecue, douche et pré-équipement pour un jacuzzi. La liste de prix indique que le mobilier, l'équipement, la décoration, le mobilier de terrasse et un jacuzzi sont inclus dans cet appartement.",
  "Eine offene Terrasse von {N30.74} {U} und ein Solarium von {N94.75} {U} mit Grill, Dusche und Vorinstallation für einen Whirlpool. Die Preisliste vermerkt, dass Möbel, Ausstattung, Dekoration, Terrassenmöbel und ein Whirlpool in dieser Wohnung enthalten sind.",
  "Открытая терраса {N30.74} {U} и солярий {N94.75} {U} с грилем, душем и подготовкой под джакузи. В прайс-листе указано, что мебель, оборудование, декор, мебель для террасы и джакузи включены в стоимость этой квартиры.",
  "تراس مكشوف بمساحة {N30.74} {U} وسولاريوم بمساحة {N94.75} {U} مع شواية ودش وتجهيز مسبق لجاكوزي. تشير قائمة الأسعار إلى أن الأثاث والتجهيزات والديكور وأثاث التراس وجاكوزي مشمولة في هذه الشقة.",
  "Een open terras van {N30.74} {U} en een solarium van {N94.75} {U} met barbecue, douche en voorbereiding voor een bubbelbad. De prijslijst vermeldt dat meubilair, uitrusting, decoratie, terrasmeubilair en een bubbelbad bij dit appartement zijn inbegrepen.",
  "Otwarty taras o powierzchni {N30.74} {U} i solarium {N94.75} {U} z grillem, prysznicem i instalacją pod jacuzzi. Lista cen wskazuje, że meble, wyposażenie, dekoracje, meble tarasowe i jacuzzi są w cenie tego apartamentu.",
  "En åpen terrasse på {N30.74} {U} og en solterrasse på {N94.75} {U} med grill, dusj og forberedelse for boblebad. Prislisten oppgir at møbler, utstyr, dekorasjon, terrassemøbler og et boblebad er inkludert i denne leiligheten.",
  "En öppen terrass på {N30.74} {U} och en solterrass på {N94.75} {U} med grill, dusch och förberedelse för bubbelpool. Prislistan anger att möbler, utrustning, dekoration, terrassmöbler och en bubbelpool ingår i den här lägenheten.")
a(82, 'Third floor, Block 1, staircase 1.',
  "Tercera planta, bloque 1, escalera 1. Salón comedor de {N25.23} {U}, cocina de {N7.83} {U}, dos dormitorios de {N15.38} y {N10.24} {U}, dos baños y una escalera privada al solárium.",
  "Troisième étage, bloc 1, cage d'escalier 1. Séjour-salle à manger de {N25.23} {U}, cuisine de {N7.83} {U}, deux chambres de {N15.38} et {N10.24} {U}, deux salles de bains et un escalier privé vers le solarium.",
  "Drittes Obergeschoss, Block 1, Treppenhaus 1. Wohn- und Essbereich von {N25.23} {U}, Küche von {N7.83} {U}, zwei Schlafzimmer mit {N15.38} und {N10.24} {U}, zwei Bäder und eine private Treppe zum Solarium.",
  "Четвёртый этаж, блок 1, подъезд 1. Гостиная-столовая {N25.23} {U}, кухня {N7.83} {U}, две спальни площадью {N15.38} и {N10.24} {U}, две ванные комнаты и частная лестница на солярий.",
  "الطابق الثالث، المبنى 1، الدرج 1. غرفة معيشة وطعام بمساحة {N25.23} {U}، ومطبخ بمساحة {N7.83} {U}، وغرفتا نوم بمساحة {N15.38} و{N10.24} {U}، وحمامان، ودرج خاص إلى السولاريوم.",
  "Derde verdieping, blok 1, trappenhuis 1. Woon- en eetkamer van {N25.23} {U}, keuken van {N7.83} {U}, twee slaapkamers van {N15.38} en {N10.24} {U}, twee badkamers en een eigen trap naar het solarium.",
  "Trzecie piętro, blok 1, klatka 1. Salon z jadalnią o powierzchni {N25.23} {U}, kuchnia {N7.83} {U}, dwie sypialnie o powierzchni {N15.38} i {N10.24} {U}, dwie łazienki i prywatne schody na solarium.",
  "Fjerde etasje, bygg 1, oppgang 1. Stue og spisestue på {N25.23} {U}, kjøkken på {N7.83} {U}, to soverom på {N15.38} og {N10.24} {U}, to bad og en privat trapp til solterrassen.",
  "Tredje våningen, hus 1, trapphus 1. Vardagsrum och matplats på {N25.23} {U}, kök på {N7.83} {U}, två sovrum på {N15.38} och {N10.24} {U}, två badrum och en privat trappa till solterrassen.")
a(83, 'An open terrace of 31.43 sqm and a solarium of 97.48 sqm',
  "Una terraza descubierta de {N31.43} {U} y un solárium de {N97.48} {U} con barbacoa, ducha y preinstalación para un jacuzzi.",
  "Une terrasse découverte de {N31.43} {U} et un solarium de {N97.48} {U} avec barbecue, douche et pré-équipement pour un jacuzzi.",
  "Eine offene Terrasse von {N31.43} {U} und ein Solarium von {N97.48} {U} mit Grill, Dusche und Vorinstallation für einen Whirlpool.",
  "Открытая терраса {N31.43} {U} и солярий {N97.48} {U} с грилем, душем и подготовкой под джакузи.",
  "تراس مكشوف بمساحة {N31.43} {U} وسولاريوم بمساحة {N97.48} {U} مع شواية ودش وتجهيز مسبق لجاكوزي.",
  "Een open terras van {N31.43} {U} en een solarium van {N97.48} {U} met barbecue, douche en voorbereiding voor een bubbelbad.",
  "Otwarty taras o powierzchni {N31.43} {U} i solarium {N97.48} {U} z grillem, prysznicem i instalacją pod jacuzzi.",
  "En åpen terrasse på {N31.43} {U} og en solterrasse på {N97.48} {U} med grill, dusj og forberedelse for boblebad.",
  "En öppen terrass på {N31.43} {U} och en solterrass på {N97.48} {U} med grill, dusch och förberedelse för bubbelpool.")

# ---------------------------------------------------------------- lifestyle, location
a(84, 'A finished home, <em>with the amenities built</em>', "Una vivienda terminada, <em>con las instalaciones ya construidas</em>", "Un logement achevé, <em>avec ses équipements déjà construits</em>", "Eine fertige Wohnung, <em>mit gebauten Gemeinschaftsanlagen</em>",
  "Готовая квартира, <em>с уже построенной инфраструктурой</em>", "مسكن مكتمل، <em>مرافقه المشتركة مبنية بالفعل</em>", "Een afgeronde woning, <em>met voorzieningen die er al staan</em>", "Ukończone mieszkanie, <em>z gotową infrastrukturą</em>",
  "En ferdigstilt bolig, <em>med fellesanleggene bygget</em>", "En färdigställd bostad, <em>med gemensamma anläggningar på plats</em>")
a(85, 'The shared grounds of more than 8,000 sqm are complete',
  "Las zonas comunes, de más de {G8000} {U}, están terminadas, y las piscinas, el gimnasio y la sala de coworking ya se pueden ver.",
  "Les espaces communs, de plus de {G8000} {U}, sont terminés, et les piscines, la salle de sport et la salle de coworking sont déjà visibles.",
  "Die Gemeinschaftsanlagen mit mehr als {G8000} {U} sind fertiggestellt, und Pools, Fitnessraum und Coworking-Raum können bereits besichtigt werden.",
  "Общая территория площадью более {G8000} {U} завершена, бассейны, тренажёрный зал и коворкинг уже можно увидеть своими глазами.",
  "المساحات المشتركة التي تزيد على {G8000} {U} مكتملة، والمسابح والصالة الرياضية وغرفة العمل المشترك يمكن معاينتها الآن.",
  "De gemeenschappelijke ruimtes van meer dan {G8000} {U} zijn klaar, en de zwembaden, de gym en de coworkingruimte zijn al te bezichtigen.",
  "Tereny wspólne o powierzchni ponad {G8000} {U} są ukończone, a baseny, siłownię i salę coworkingową można już zobaczyć.",
  "Fellesområdene på over {G8000} {U} er ferdige, og bassengene, treningsrommet og coworking-rommet kan allerede ses.",
  "De gemensamma ytorna på över {G8000} {U} är färdiga, och poolerna, gymmet och coworking-rummet kan redan ses.")
a(86, 'The pool area', "La zona de piscinas", "L'espace piscines", "Der Poolbereich", "Зона бассейнов", "منطقة المسابح", "Het zwembadgebied", "Strefa basenów", "Bassengområdet", "Poolområdet")
a(87, 'A pool of about 150 sqm that can be heated',
  "Una piscina de unos {N150} {U} que se puede climatizar, con un carril de natación de {N20} {M}, una piscina infantil de unos {N25} {U}, un jacuzzi y duchas, en un recinto vallado.",
  "Une piscine d'environ {N150} {U} qui peut être chauffée, avec un couloir de nage de {N20} {M}, une piscine pour enfants d'environ {N25} {U}, un jacuzzi et des douches, dans un espace clôturé.",
  "Ein Pool von etwa {N150} {U}, der beheizt werden kann, mit einer {N20} {M} langen Schwimmbahn, ein Kinderbecken von etwa {N25} {U}, ein Whirlpool und Duschen in einem eingezäunten Poolbereich.",
  "Бассейн площадью около {N150} {U} с возможностью подогрева и плавательной дорожкой {N20} {M}, детский бассейн около {N25} {U}, джакузи и души на огороженной территории.",
  "مسبح بمساحة نحو {N150} {U} يمكن تسخينه مع مسار سباحة بطول {N20} {M}، ومسبح للأطفال بمساحة نحو {N25} {U}، وجاكوزي ودشات، في منطقة مسوّرة.",
  "Een zwembad van ongeveer {N150} {U} dat verwarmd kan worden, met een zwembaan van {N20} {M}, een kinderbad van ongeveer {N25} {U}, een bubbelbad en douches, in een omheind zwembadgebied.",
  "Basen o powierzchni około {N150} {U} z możliwością podgrzewania i torem pływackim o długości {N20} {M}, basen dla dzieci o powierzchni około {N25} {U}, jacuzzi i prysznice na ogrodzonym terenie.",
  "Et basseng på rundt {N150} {U} som kan varmes opp, med en svømmebane på {N20} {M}, et barnebasseng på rundt {N25} {U}, et boblebad og dusjer, i et inngjerdet bassengområde.",
  "En pool på cirka {N150} {U} som kan värmas, med en simbana på {N20} {M}, en barnpool på cirka {N25} {U}, en bubbelpool och duschar, i ett inhägnat poolområde.")
a(88, 'Gym and coworking', "Gimnasio y coworking", "Salle de sport et coworking", "Fitnessraum und Coworking", "Тренажёрный зал и коворкинг", "الصالة الرياضية والعمل المشترك", "Gym en coworking", "Siłownia i coworking", "Treningsrom og coworking", "Gym och coworking")
a(89, 'A gym of about 38 sqm', "Un gimnasio de unos {N38} {U} con máquinas de cardio, fuerza y flexibilidad, y una sala de coworking de unos {N26} {U} con wifi.",
  "Une salle de sport d'environ {N38} {U} avec des appareils de cardio, de force et de souplesse, et une salle de coworking d'environ {N26} {U} avec Wi-Fi.",
  "Ein Fitnessraum von etwa {N38} {U} mit Geräten für Ausdauer, Kraft und Beweglichkeit und ein Coworking-Raum von etwa {N26} {U} mit WLAN.",
  "Тренажёрный зал около {N38} {U} с оборудованием для кардио-, силовых и растяжных тренировок и коворкинг около {N26} {U} с Wi-Fi.",
  "صالة رياضية بمساحة نحو {N38} {U} بأجهزة للقلب والقوة والمرونة، وغرفة عمل مشترك بمساحة نحو {N26} {U} مع واي فاي.",
  "Een gym van ongeveer {N38} {U} met cardio-, kracht- en flexibiliteitstoestellen, en een coworkingruimte van ongeveer {N26} {U} met wifi.",
  "Siłownia o powierzchni około {N38} {U} ze sprzętem do ćwiczeń cardio, siłowych i rozciągających oraz sala coworkingowa o powierzchni około {N26} {U} z Wi-Fi.",
  "Et treningsrom på rundt {N38} {U} med utstyr for kondisjon, styrke og bevegelighet, og et coworking-rom på rundt {N26} {U} med Wi-Fi.",
  "Ett gym på cirka {N38} {U} med utrustning för kondition, styrka och rörlighet, och ett coworking-rum på cirka {N26} {U} med wifi.")
a(90, 'Gardens and viewpoint', "Jardines y mirador", "Jardins et belvédère", "Gärten und Aussichtsplatz", "Сады и смотровая площадь", "الحدائق والإطلالة", "Tuinen en uitkijkplein", "Ogrody i plac widokowy", "Hager og utsiktsplass", "Trädgårdar och utsiktsplats")
a(91, 'Landscaped gardens with paths and a viewpoint plaza', "Jardines paisajísticos con caminos y una plaza mirador de unos {N127} {U}, iluminada y con riego.", "Jardins paysagers avec chemins et une place belvédère d'environ {N127} {U}, éclairée et irriguée.",
  "Gepflegte Gärten mit Wegen und ein Aussichtsplatz von etwa {N127} {U}, beleuchtet und bewässert.", "Ландшафтные сады с дорожками и смотровая площадь около {N127} {U}, с освещением и поливом.",
  "حدائق مُنسّقة بممرات وساحة إطلالة بمساحة نحو {N127} {U}، مضاءة ومزودة بالري.", "Aangelegde tuinen met paden en een uitkijkplein van ongeveer {N127} {U}, verlicht en bewaterd.",
  "Zagospodarowane ogrody ze ścieżkami i plac widokowy o powierzchni około {N127} {U}, oświetlony i nawadniany.", "Opparbeidede hager med stier og en utsiktsplass på rundt {N127} {U}, belyst og vannet.",
  "Anlagda trädgårdar med stigar och en utsiktsplats på cirka {N127} {U}, belyst och bevattnad.")
a(92, 'Beach and train', "Playa y tren", "Plage et train", "Strand und Bahn", "Пляж и поезд", "الشاطئ والقطار", "Strand en trein", "Plaża i pociąg", "Strand og tog", "Strand och tåg")
a(93, 'Carvajal beach and a commuter-train stop are close', "La playa de Carvajal y una parada de tren de cercanías están cerca, y el paseo marítimo de Fuengirola continúa desde la playa.",
  "La plage de Carvajal et un arrêt de train de banlieue sont proches, et la promenade du front de mer de Fuengirola prolonge la plage.",
  "Der Strand von Carvajal und eine Haltestelle der Nahverkehrsbahn sind nah, und die Strandpromenade von Fuengirola setzt sich vom Strand aus fort.",
  "Пляж Карвахаль и остановка пригородного поезда рядом, а набережная Фуэнхиролы продолжается от пляжа.",
  "شاطئ كارفاخال ومحطة قطار الضواحي قريبان، ويمتد كورنيش فوينخيرولا من الشاطئ.",
  "Het strand van Carvajal en een halte van de forenzentrein zijn dichtbij, en de boulevard van Fuengirola loopt vanaf het strand door.",
  "Plaża Carvajal i przystanek pociągu podmiejskiego są blisko, a promenada nadmorska Fuengirola ciągnie się od plaży.",
  "Stranden i Carvajal og et stoppested for lokaltoget ligger nær, og strandpromenaden i Fuengirola fortsetter fra stranden.",
  "Stranden i Carvajal och en pendeltågshållplats ligger nära, och strandpromenaden i Fuengirola fortsätter från stranden.")
a(94, 'El Higuerón is a residential area of Fuengirola near Carvajal beach',
  "El Higuerón es una zona residencial de Fuengirola cercana a la playa de Carvajal, en la Costa del Sol entre Fuengirola y Benalmádena. La N-340 está a {N450} {M}, la AP-7 a {N2} {KM} y el aeropuerto de Málaga a unos 20 minutos en coche.",
  "El Higuerón est un quartier résidentiel de Fuengirola près de la plage de Carvajal, sur la Costa del Sol entre Fuengirola et Benalmádena. La N-340 est à {N450} {M}, l'AP-7 à {N2} {KM} et l'aéroport de Malaga à environ 20 minutes en voiture.",
  "El Higuerón ist ein Wohngebiet von Fuengirola nahe dem Strand von Carvajal, an der Costa del Sol zwischen Fuengirola und Benalmádena. Die N-340 ist {N450} {M} entfernt, die AP-7 {N2} {KM}, und der Flughafen Málaga ist mit dem Auto in etwa 20 Minuten erreichbar.",
  "Эль-Игерон — жилой район Фуэнхиролы рядом с пляжем Карвахаль, на Коста-дель-Соль между Фуэнхиролой и Бенальмаденой. Трасса N-340 находится в {N450} {M}, AP-7 — в {N2} {KM}, а до аэропорта Малаги около 20 минут на машине.",
  "إل إيغيرون منطقة سكنية في فوينخيرولا قرب شاطئ كارفاخال، على كوستا ديل سول بين فوينخيرولا وبينالمادينا. يبعد الطريق N-340 مسافة {N450} {M}، والطريق AP-7 {N2} {KM}، ومطار مالقة نحو 20 دقيقة بالسيارة.",
  "El Higuerón is een woonwijk van Fuengirola bij het strand van Carvajal, aan de Costa del Sol tussen Fuengirola en Benalmádena. De N-340 ligt op {N450} {M}, de AP-7 op {N2} {KM} en de luchthaven van Málaga is ongeveer 20 minuten met de auto.",
  "El Higuerón to dzielnica mieszkalna Fuengirola w pobliżu plaży Carvajal, na Costa del Sol między Fuengirolą a Benalmádeną. N-340 jest oddalona o {N450} {M}, AP-7 o {N2} {KM}, a lotnisko w Maladze o około 20 minut jazdy samochodem.",
  "El Higuerón er et boligområde i Fuengirola nær stranden i Carvajal, på Costa del Sol mellom Fuengirola og Benalmádena. N-340 ligger {N450} {M} unna, AP-7 {N2} {KM}, og Málaga lufthavn er omtrent 20 minutter unna med bil.",
  "El Higuerón är ett bostadsområde i Fuengirola nära stranden i Carvajal, på Costa del Sol mellan Fuengirola och Benalmádena. N-340 ligger {N450} {M} bort, AP-7 {N2} {KM}, och Málagas flygplats är ungefär 20 minuter bort med bil.")
a(95, 'Carvajal beach', "Playa de Carvajal", "Plage de Carvajal", "Strand von Carvajal", "Пляж Карвахаль", "شاطئ كارفاخال", "Strand van Carvajal", "Plaża Carvajal", "Carvajal-stranden", "Carvajal-stranden")
a(96, '350 m (2023 circular) or 700 m (2025 catalogue)', "{N350} {M} (circular de 2023) o {N700} {M} (catálogo de 2025)", "{N350} {M} (circulaire de 2023) ou {N700} {M} (catalogue de 2025)",
  "{N350} {M} (Informationsschreiben 2023) oder {N700} {M} (Katalog 2025)", "{N350} {M} (письмо 2023 года) или {N700} {M} (каталог 2025 года)", "{N350} {M} (تعميم 2023) أو {N700} {M} (كتيّب 2025)",
  "{N350} {M} (circulaire 2023) of {N700} {M} (catalogus 2025)", "{N350} {M} (pismo z 2023) lub {N700} {M} (katalog z 2025)", "{N350} {M} (skriv fra 2023) eller {N700} {M} (katalog fra 2025)", "{N350} {M} (brev från 2023) eller {N700} {M} (katalog från 2025)")
a(97, 'Carvajal train stop', "Parada de tren de Carvajal", "Arrêt de train de Carvajal", "Bahnhaltestelle Carvajal", "Остановка поезда Карвахаль", "محطة قطار كارفاخال", "Treinhalte Carvajal", "Przystanek kolejowy Carvajal", "Carvajal togstopp", "Carvajal tåghållplats")
a(98, '200 m', "{N200} {M}", "{N200} {M}", "{N200} {M}", "{N200} {M}", "{N200} {M}", "{N200} {M}", "{N200} {M}", "{N200} {M}", "{N200} {M}")

# ---------------------------------------------------------------- investment, trust, availability
a(99, 'The terms are set out in the developer’s sales contract', "Las condiciones figuran en el contrato de compraventa de la promotora. Confirmamos por escrito los importes y las fechas vigentes antes de que reserve.",
  "Les conditions figurent dans le contrat de vente du promoteur. Nous confirmons par écrit les montants et les dates en vigueur avant que vous ne réserviez.",
  "Die Bedingungen sind im Kaufvertrag des Bauträgers festgelegt. Wir bestätigen die aktuellen Beträge und Termine schriftlich, bevor Sie reservieren.",
  "Условия изложены в договоре купли-продажи застройщика. Мы письменно подтверждаем действующие суммы и сроки до того, как вы забронируете.",
  "الشروط مبينة في عقد البيع الخاص بالمطور. نؤكد لك كتابةً المبالغ والتواريخ الحالية قبل أن تحجز.",
  "De voorwaarden staan in de koopovereenkomst van de ontwikkelaar. Wij bevestigen de actuele bedragen en data schriftelijk voordat u reserveert.",
  "Warunki określa umowa sprzedaży dewelopera. Aktualne kwoty i terminy potwierdzamy Państwu na piśmie przed rezerwacją.",
  "Vilkårene er fastsatt i utviklerens kjøpekontrakt. Vi bekrefter gjeldende beløp og datoer skriftlig før du reserverer.",
  "Villkoren framgår av byggherrens köpeavtal. Vi bekräftar gällande belopp och datum skriftligt innan ni reserverar.")
a(100, 'The developer’s February 2023 circular set the reservation deposit',
  "La circular informativa de la promotora de febrero de 2023 fijaba la señal de reserva en {E10000} para apartamentos y {E20000} para áticos; confirmamos el importe vigente.",
  "La circulaire d'information du promoteur de février 2023 fixait le dépôt de réservation à {E10000} pour les appartements et {E20000} pour les penthouses ; nous confirmons le montant en vigueur.",
  "Das Informationsschreiben des Bauträgers vom Februar 2023 setzte die Reservierungsanzahlung auf {E10000} für Wohnungen und {E20000} für Penthouses fest; wir bestätigen den aktuellen Betrag.",
  "Информационное письмо застройщика от февраля 2023 года устанавливало депозит при бронировании в размере {E10000} для квартир и {E20000} для пентхаусов; мы подтверждаем действующую сумму.",
  "حدد التعميم الصادر عن المطور في فبراير 2023 دفعة الحجز بمبلغ {E10000} للشقق و{E20000} للبنتهاوس؛ ونؤكد المبلغ الساري.",
  "De informatiebrief van de ontwikkelaar van februari 2023 stelde de aanbetaling bij reservering vast op {E10000} voor appartementen en {E20000} voor penthouses; wij bevestigen het actuele bedrag.",
  "Pismo informacyjne dewelopera z lutego 2023 roku ustalało zadatek rezerwacyjny na {E10000} dla apartamentów i {E20000} dla penthouse’ów; aktualną kwotę potwierdzamy.",
  "Utviklerens informasjonsskriv fra februar 2023 fastsatte reservasjonsdepositumet til {E10000} for leiligheter og {E20000} for toppleiligheter; vi bekrefter gjeldende beløp.",
  "Byggherrens informationsbrev från februari 2023 fastställde handpenningen vid bokning till {E10000} för lägenheter och {E20000} för takvåningar; vi bekräftar gällande belopp.")
a(101, 'We ask the developer to confirm in writing how amounts paid on account',
  "Pedimos a la promotora que confirme por escrito cómo se avalan mediante un banco las cantidades entregadas a cuenta, como exige la ley de edificación española.",
  "Nous demandons au promoteur de confirmer par écrit comment les sommes versées à valoir sur le prix sont garanties par une banque, comme l'exige la loi espagnole sur la construction.",
  "Wir bitten den Bauträger, schriftlich zu bestätigen, wie die geleisteten Anzahlungen durch eine Bank abgesichert werden, wie es das spanische Baurecht verlangt.",
  "Мы просим застройщика письменно подтвердить, как внесённые в счёт цены суммы обеспечиваются банковской гарантией, как того требует испанское законодательство о строительстве.",
  "نطلب من المطور أن يؤكد كتابةً كيف تُضمن المبالغ المدفوعة على الحساب عبر بنك، كما يقتضي قانون البناء الإسباني.",
  "Wij vragen de ontwikkelaar schriftelijk te bevestigen hoe de vooruitbetaalde bedragen via een bank worden gegarandeerd, zoals de Spaanse bouwwet vereist.",
  "Prosimy dewelopera o pisemne potwierdzenie, jak kwoty wpłacone na poczet ceny są gwarantowane przez bank, zgodnie z wymogami hiszpańskiego prawa budowlanego.",
  "Vi ber utvikleren bekrefte skriftlig hvordan beløp betalt på forskudd garanteres gjennom en bank, slik spansk byggelovgivning krever.",
  "Vi ber byggherren bekräfta skriftligt hur belopp som betalats på förskott garanteras genom en bank, som spansk byggnadslag kräver.")
a(102, 'The price list includes two parking spaces and a storeroom',
  "La lista de precios incluye dos plazas de aparcamiento y un trastero con cada vivienda. También muestra una cifra de equipamiento aparte para cada vivienda ({E31700}, o {E45000} para el apartamento de tres dormitorios), que aquí no está incluida.",
  "La liste de prix inclut deux places de stationnement et un débarras avec chaque logement. Elle indique aussi un montant d'équipement distinct pour chaque logement ({E31700}, ou {E45000} pour l'appartement de trois chambres), qui n'est pas inclus ici.",
  "Die Preisliste enthält zu jeder Wohnung zwei Stellplätze und einen Abstellraum. Sie nennt außerdem für jede Wohnung einen gesonderten Ausstattungsbetrag ({E31700}, bei der Dreizimmerwohnung {E45000}), der hier nicht enthalten ist.",
  "В прайс-лист входят два парковочных места и кладовая для каждой квартиры. Там же указана отдельная сумма за оснащение для каждой квартиры ({E31700}, а для трёхспальной — {E45000}), здесь она не включена.",
  "تشمل قائمة الأسعار موقفي سيارات ومخزناً مع كل مسكن. وتُظهر أيضاً رقم تجهيز منفصلاً لكل مسكن ({E31700}، و{E45000} للشقة ذات الغرف الثلاث)، وهو غير مشمول هنا.",
  "De prijslijst omvat bij elke woning twee parkeerplaatsen en een berging. Ze toont ook voor elke woning een apart uitrustingsbedrag ({E31700}, of {E45000} voor het appartement met drie slaapkamers), dat hier niet is inbegrepen.",
  "Lista cen obejmuje przy każdym lokalu dwa miejsca parkingowe i komórkę lokatorską. Podaje też odrębną kwotę za wyposażenie każdego lokalu ({E31700}, a dla apartamentu z trzema sypialniami {E45000}), której tu nie uwzględniono.",
  "Prislisten inkluderer to parkeringsplasser og en bod med hver bolig. Den viser også et separat utstyrsbeløp for hver bolig ({E31700}, eller {E45000} for leiligheten med tre soverom), som ikke er med her.",
  "Prislistan inkluderar två parkeringsplatser och ett förråd med varje bostad. Den visar också ett separat utrustningsbelopp för varje bostad ({E31700}, eller {E45000} för lägenheten med tre sovrum), som inte ingår här.")
a(103, 'The price list gives an annual community fee', "La lista de precios indica una cuota anual de comunidad para cada una de las cinco viviendas, de {EC1797.50} a {EC2712.24}, según la vivienda.",
  "La liste de prix indique des charges de copropriété annuelles pour chacun des cinq logements, de {EC1797.50} à {EC2712.24} selon le logement.",
  "Die Preisliste nennt für jede der fünf Wohnungen eine jährliche Gemeinschaftsgebühr, je nach Wohnung von {EC1797.50} bis {EC2712.24}.",
  "В прайс-листе указан годовой взнос на содержание общего имущества для каждой из пяти квартир — от {EC1797.50} до {EC2712.24} в зависимости от квартиры.",
  "تذكر قائمة الأسعار رسوم صيانة المجمع السنوية لكل من المساكن الخمسة، من {EC1797.50} إلى {EC2712.24} بحسب المسكن.",
  "De prijslijst geeft voor elk van de vijf woningen een jaarlijkse bijdrage voor de gemeenschap, van {EC1797.50} tot {EC2712.24}, afhankelijk van de woning.",
  "Lista cen podaje roczną opłatę wspólnotową dla każdego z pięciu lokali, od {EC1797.50} do {EC2712.24} w zależności od lokalu.",
  "Prislisten oppgir en årlig fellesavgift for hver av de fem boligene, fra {EC1797.50} til {EC2712.24} avhengig av boligen.",
  "Prislistan anger en årlig samfällighetsavgift för var och en av de fem bostäderna, från {EC1797.50} till {EC2712.24} beroende på bostad.")
a(104, 'Occupation and certificates', "Ocupación y certificados", "Occupation et certificats", "Bezug und Zertifikate", "Заселение и сертификаты", "الإشغال والشهادات", "Ingebruikname en certificaten", "Zasiedlenie i certyfikaty", "Bruk og sertifikater", "Inflyttning och intyg")
a(105, 'The first-occupation licence or declaration', "La licencia o declaración responsable de primera ocupación y el certificado energético de la vivienda concreta que elija.",
  "Le permis ou la déclaration d'occupation et le certificat énergétique du logement précis que vous choisissez.", "Die Erstbezugsgenehmigung oder -erklärung und den Energieausweis der von Ihnen gewählten Wohnung.",
  "Разрешение или декларацию о первичном заселении и энергетический сертификат на выбранную вами квартиру.", "رخصة أو إقرار الإشغال الأول وشهادة الطاقة للمسكن الذي تختاره تحديداً.",
  "De vergunning of verklaring voor eerste ingebruikname en het energiecertificaat van de specifieke woning die u kiest.", "Pozwolenie lub oświadczenie o pierwszym zasiedleniu oraz świadectwo energetyczne wybranego przez Państwa lokalu.",
  "Tillatelsen eller erklæringen om første gangs bruk og energiattesten for den konkrete boligen du velger.", "Tillståndet eller försäkran om första inflyttning och energicertifikatet för den specifika bostad ni väljer.")
a(106, 'The beach distance', "La distancia a la playa", "La distance à la plage", "Die Entfernung zum Strand", "Расстояние до пляжа", "المسافة إلى الشاطئ", "De afstand tot het strand", "Odległość do plaży", "Avstanden til stranden", "Avståndet till stranden")
a(107, 'The developer’s 2023 circular puts Carvajal beach at 350 m', "La circular informativa de la promotora de 2023 sitúa la playa de Carvajal a {N350} {M} y su catálogo de 2025 a {N700} {M}. Medimos el paseo con usted.",
  "La circulaire d'information du promoteur de 2023 situe la plage de Carvajal à {N350} {M} et son catalogue de 2025 à {N700} {M}. Nous mesurons le trajet avec vous.",
  "Das Informationsschreiben des Bauträgers von 2023 nennt für den Strand von Carvajal {N350} {M}, sein Katalog von 2025 {N700} {M}. Wir messen den Weg gemeinsam mit Ihnen.",
  "В информационном письме застройщика 2023 года до пляжа Карвахаль указано {N350} {M}, в его каталоге 2025 года — {N700} {M}. Мы вместе с вами замерим путь пешком.",
  "يضع تعميم المطور لعام 2023 شاطئ كارفاخال على بُعد {N350} {M} ويضعه كتيّبه لعام 2025 على بُعد {N700} {M}. نقيس معك مسافة المشي.",
  "De informatiebrief van de ontwikkelaar uit 2023 plaatst het strand van Carvajal op {N350} {M} en zijn catalogus uit 2025 op {N700} {M}. Wij meten de wandeling samen met u.",
  "Pismo informacyjne dewelopera z 2023 roku podaje odległość do plaży Carvajal {N350} {M}, a jego katalog z 2025 roku {N700} {M}. Odmierzamy tę trasę razem z Państwem.",
  "Utviklerens informasjonsskriv fra 2023 oppgir {N350} {M} til stranden i Carvajal, og katalogen fra 2025 oppgir {N700} {M}. Vi måler gåturen sammen med deg.",
  "Byggherrens informationsbrev från 2023 anger {N350} {M} till stranden i Carvajal, och katalogen från 2025 anger {N700} {M}. Vi mäter promenaden tillsammans med er.")
a(108, 'The equipment figure', "La cifra de equipamiento", "Le montant d'équipement", "Der Ausstattungsbetrag", "Сумма за оснащение", "رقم التجهيز", "Het uitrustingsbedrag", "Kwota za wyposażenie", "Utstyrsbeløpet", "Utrustningsbeloppet")
a(109, 'What the separate equipment figure on the price list contains', "Qué contiene la cifra de equipamiento aparte de la lista de precios y si se suma al precio.",
  "Ce que comprend le montant d'équipement distinct de la liste de prix et s'il s'ajoute au prix.", "Was der gesonderte Ausstattungsbetrag in der Preisliste umfasst und ob er zum Preis hinzukommt.",
  "Что входит в отдельную сумму за оснащение в прайс-листе и добавляется ли она к цене.", "ما الذي يتضمنه رقم التجهيز المنفصل في قائمة الأسعار وهل يُضاف إلى السعر.",
  "Wat het apart vermelde uitrustingsbedrag op de prijslijst omvat en of het bovenop de prijs komt.", "Co obejmuje odrębna kwota za wyposażenie na liście cen i czy dolicza się ją do ceny.",
  "Hva det separate utstyrsbeløpet på prislisten omfatter, og om det kommer i tillegg til prisen.", "Vad det separata utrustningsbeloppet i prislistan omfattar, och om det tillkommer på priset.")
a(110, 'The price list says furniture, equipment and decoration are included free',
  "La lista de precios dice que el mobiliario, el equipamiento y la decoración están incluidos sin coste, pero también muestra un precio con equipamiento. Confirmamos cuál se aplica.",
  "La liste de prix indique que le mobilier, l'équipement et la décoration sont inclus gratuitement, mais elle montre aussi un prix avec équipement. Nous confirmons lequel s'applique.",
  "Die Preisliste sagt, Möbel, Ausstattung und Dekoration seien kostenlos enthalten, nennt aber auch einen Preis mit Ausstattung. Wir bestätigen, welcher gilt.",
  "В прайс-листе сказано, что мебель, оборудование и декор включены бесплатно, но там же указана цена с оснащением. Мы подтверждаем, какая из них действует.",
  "تقول قائمة الأسعار إن الأثاث والتجهيزات والديكور مشمولة مجاناً، لكنها تُظهر أيضاً سعراً مع التجهيز. نؤكد أيهما ينطبق.",
  "De prijslijst zegt dat meubilair, uitrusting en decoratie gratis zijn inbegrepen, maar toont ook een prijs met uitrusting. Wij bevestigen welke geldt.",
  "Lista cen mówi, że meble, wyposażenie i dekoracje są w cenie bezpłatnie, ale podaje też cenę z wyposażeniem. Potwierdzamy, która obowiązuje.",
  "Prislisten sier at møbler, utstyr og dekorasjon er inkludert uten kostnad, men den viser også en pris med utstyr. Vi bekrefter hvilken som gjelder.",
  "Prislistan säger att möbler, utrustning och dekoration ingår utan kostnad, men den visar också ett pris med utrustning. Vi bekräftar vilket som gäller.")
a(111, 'Five homes <em>currently available</em>', "Cinco viviendas <em>disponibles ahora</em>", "Cinq logements <em>actuellement disponibles</em>", "Fünf Wohnungen <em>derzeit verfügbar</em>",
  "Пять квартир <em>сейчас в продаже</em>", "خمسة مساكن <em>متاحة حالياً</em>", "Vijf woningen <em>momenteel beschikbaar</em>", "Pięć mieszkań <em>obecnie dostępnych</em>", "Fem boliger <em>tilgjengelige nå</em>", "Fem bostäder <em>tillgängliga just nu</em>")
a(112, 'Apartments 2, 24 and 33 are on the ground floor',
  "Los apartamentos 2, 24 y 33 están en la planta baja y los apartamentos 8 y 23 son áticos de la tercera planta, todos en el bloque 1. Los precios son los de la lista de precios de la promotora, sin su cifra de equipamiento aparte.",
  "Les appartements 2, 24 et 33 sont au rez-de-chaussée et les appartements 8 et 23 sont des penthouses au troisième étage, tous dans le bloc 1. Les prix sont ceux de la liste de prix du promoteur, hors son montant d'équipement distinct.",
  "Die Wohnungen 2, 24 und 33 liegen im Erdgeschoss, die Wohnungen 8 und 23 sind Penthouses im dritten Obergeschoss, alle in Block 1. Die Preise stammen aus der Preisliste des Bauträgers, ohne den dort gesondert ausgewiesenen Ausstattungsbetrag.",
  "Квартиры 2, 24 и 33 находятся на первом этаже, а квартиры 8 и 23 — пентхаусы на четвёртом этаже, все в блоке 1. Цены взяты из прайс-листа застройщика без указанной в нём отдельной суммы за оснащение.",
  "الشقق 2 و24 و33 في الطابق الأرضي، والشقتان 8 و23 بنتهاوس في الطابق الثالث، وجميعها في المبنى 1. الأسعار هي أسعار قائمة المطور، دون رقم التجهيز المنفصل الوارد فيها.",
  "Appartement 2, 24 en 33 liggen op de begane grond en appartement 8 en 23 zijn penthouses op de derde verdieping, allemaal in blok 1. De prijzen zijn die van de prijslijst van de ontwikkelaar, zonder het daarin apart vermelde uitrustingsbedrag.",
  "Apartamenty 2, 24 i 33 znajdują się na parterze, a apartamenty 8 i 23 to penthouse’y na trzecim piętrze, wszystkie w bloku 1. Ceny pochodzą z listy cen dewelopera, bez odrębnej kwoty za wyposażenie, którą ta lista podaje.",
  "Leilighet 2, 24 og 33 ligger i første etasje, og leilighet 8 og 23 er toppleiligheter i fjerde etasje, alle i bygg 1. Prisene er fra utviklerens prisliste, uten det separate utstyrsbeløpet den oppgir.",
  "Lägenhet 2, 24 och 33 ligger på bottenvåningen, och lägenhet 8 och 23 är takvåningar på tredje våningen, alla i hus 1. Priserna är de i byggherrens prislista, utan det separata utrustningsbelopp den anger.")
a(113, 'Prices, areas and community fees are transcribed',
  "Los precios, las superficies y las cuotas de comunidad están transcritos de la lista de precios de la promotora del 8 de octubre de 2026 para las cinco viviendas que figuran como disponibles, y las superficies de las estancias de los planos de la promotora de octubre de 2023. La lista no indica si el IVA y los gastos de compra están incluidos, y Nueva Living lo confirma antes de cualquier reserva. También muestra una cifra de equipamiento aparte para cada vivienda, que aquí no está incluida. El plano del apartamento 8 lleva un pie que lo describe como de tres dormitorios, pero su dibujo y la lista de precios muestran dos; esta página sigue la lista de precios. La circular informativa de la promotora de febrero de 2023 daba como fecha de entrega el 30 de noviembre de 2024, que sustituye el «llave en mano» de la lista de precios.",
  "Les prix, les surfaces et les charges de copropriété sont transcrits de la liste de prix du promoteur du 8 octobre 2026 pour les cinq logements indiqués comme disponibles, et les surfaces des pièces des plans du promoteur d'octobre 2023. La liste ne précise pas si la TVA et les frais d'achat sont inclus, et Nueva Living le confirme avant toute réservation. Elle indique aussi un montant d'équipement distinct pour chaque logement, qui n'est pas inclus ici. Le plan de l'appartement 8 porte une légende le décrivant comme un trois-chambres, mais son dessin et la liste de prix montrent deux chambres ; cette page suit la liste de prix. La circulaire d'information du promoteur de février 2023 donnait une date de livraison au 30 novembre 2024, que la mention « clés en main » de la liste de prix remplace.",
  "Preise, Flächen und Gemeinschaftsgebühren sind der Preisliste des Bauträgers vom 8. Oktober 2026 für die fünf als verfügbar gelisteten Wohnungen entnommen, die Raumflächen den Plänen des Bauträgers vom Oktober 2023. Die Liste sagt nicht, ob Mehrwertsteuer und Erwerbsnebenkosten enthalten sind, und Nueva Living bestätigt dies vor jeder Reservierung. Sie nennt außerdem für jede Wohnung einen gesonderten Ausstattungsbetrag, der hier nicht enthalten ist. Der Plan der Wohnung 8 trägt eine Beschriftung als Dreizimmerwohnung, doch seine Zeichnung und die Preisliste zeigen zwei Schlafzimmer; diese Seite folgt der Preisliste. Das Informationsschreiben des Bauträgers vom Februar 2023 nannte als Übergabetermin den 30. November 2024, den der Vermerk „schlüsselfertig“ der Preisliste ersetzt.",
  "Цены, площади и взносы на содержание общего имущества перенесены из прайс-листа застройщика от 8 октября 2026 года по пяти квартирам, указанным как доступные, а площади комнат — из планировок застройщика от октября 2023 года. В списке не сказано, включены ли НДС и расходы на покупку, и Nueva Living подтверждает это до любого бронирования. Там же указана отдельная сумма за оснащение для каждой квартиры, здесь она не включена. На планировке квартиры 8 в подписи значатся три спальни, но чертёж и прайс-лист показывают две; эта страница следует прайс-листу. Информационное письмо застройщика от февраля 2023 года называло сроком сдачи 30 ноября 2024 года; его заменяет пометка «под ключ» в прайс-листе.",
  "الأسعار والمساحات ورسوم صيانة المجمع منقولة من قائمة أسعار المطور المؤرخة في 8 أكتوبر 2026 للمساكن الخمسة المدرجة كمتاحة، ومساحات الغرف من مخططات المطور بتاريخ أكتوبر 2023. لا تذكر القائمة ما إذا كانت ضريبة القيمة المضافة وتكاليف الشراء مشمولة، وتؤكد Nueva Living ذلك قبل أي حجز. وتُظهر القائمة أيضاً رقم تجهيز منفصلاً لكل مسكن، وهو غير مشمول هنا. يحمل مخطط الشقة 8 عنواناً يصفها بأنها من ثلاث غرف نوم، لكن رسمه وقائمة الأسعار يُظهران غرفتين؛ وتتبع هذه الصفحة قائمة الأسعار. وكان تعميم المطور الصادر في فبراير 2023 يذكر 30 نوفمبر 2024 موعداً للتسليم، وتحل محله عبارة «جاهز للتسليم» في قائمة الأسعار.",
  "Prijzen, oppervlaktes en bijdragen voor de gemeenschap zijn overgenomen uit de prijslijst van de ontwikkelaar van 8 oktober 2026 voor de vijf woningen die als beschikbaar zijn vermeld, en de ruimteoppervlaktes uit de plattegronden van de ontwikkelaar van oktober 2023. De lijst vermeldt niet of btw en aankoopkosten zijn inbegrepen, en Nueva Living bevestigt dit vóór elke reservering. Ze toont ook voor elke woning een apart uitrustingsbedrag, dat hier niet is inbegrepen. De plattegrond van appartement 8 draagt een onderschrift als woning met drie slaapkamers, maar de tekening en de prijslijst tonen er twee; deze pagina volgt de prijslijst. De informatiebrief van de ontwikkelaar van februari 2023 gaf als opleverdatum 30 november 2024, die de vermelding „sleutelklaar” op de prijslijst vervangt.",
  "Ceny, powierzchnie i opłaty wspólnotowe przepisano z listy cen dewelopera z 8 października 2026 roku dla pięciu mieszkań wskazanych jako dostępne, a powierzchnie pomieszczeń z rzutów dewelopera z października 2023 roku. Lista nie podaje, czy VAT i koszty zakupu są wliczone, a Nueva Living potwierdza to przed jakąkolwiek rezerwacją. Podaje też odrębną kwotę za wyposażenie każdego lokalu, której tu nie uwzględniono. Rzut apartamentu 8 ma podpis opisujący go jako trzypokojowy, ale jego rysunek i lista cen pokazują dwie sypialnie; ta strona podąża za listą cen. Pismo informacyjne dewelopera z lutego 2023 roku podawało termin odbioru 30 listopada 2024 roku, który zastępuje adnotacja „pod klucz” na liście cen.",
  "Prisene, arealene og fellesavgiftene er hentet fra utviklerens prisliste av 8. oktober 2026 for de fem boligene som er oppført som tilgjengelige, og romarealene fra utviklerens plantegninger fra oktober 2023. Listen oppgir ikke om mva. og kjøpskostnader er inkludert, og Nueva Living bekrefter dette før enhver reservasjon. Den viser også et separat utstyrsbeløp for hver bolig, som ikke er med her. Plantegningen av leilighet 8 har en tekst som beskriver den som en tresoveromsbolig, men tegningen og prislisten viser to soverom; denne siden følger prislisten. Utviklerens informasjonsskriv fra februar 2023 oppga overlevering 30. november 2024, som «nøkkelferdig» i prislisten erstatter.",
  "Priserna, ytorna och samfällighetsavgifterna är avskrivna från byggherrens prislista av den 8 oktober 2026 för de fem bostäder som anges som tillgängliga, och rumsytorna från byggherrens planritningar från oktober 2023. Listan anger inte om moms och köpkostnader ingår, och Nueva Living bekräftar det före varje reservation. Den visar också ett separat utrustningsbelopp för varje bostad, som inte ingår här. Planritningen för lägenhet 8 har en bildtext som beskriver den som en bostad med tre sovrum, men ritningen och prislistan visar två sovrum; den här sidan följer prislistan. Byggherrens informationsbrev från februari 2023 angav leverans den 30 november 2024, vilket anteckningen ”nyckelfärdig” i prislistan ersätter.")

# ---------------------------------------------------------------- timeline, viewing, enquiry, faq
a(116, 'Floorplans for all five available homes', "Planos de las cinco viviendas disponibles, la memoria de calidades y la lista de precios.", "Plans des cinq logements disponibles, descriptif de la qualité et liste de prix.",
  "Grundrisse aller fünf verfügbaren Wohnungen, die Ausstattungsbeschreibung und die Preisliste.", "Планировки всех пяти доступных квартир, спецификация и прайс-лист.", "مخططات المساكن الخمسة المتاحة والمواصفات وقائمة الأسعار.",
  "Plattegronden van alle vijf beschikbare woningen, de specificatie en de prijslijst.", "Rzuty wszystkich pięciu dostępnych mieszkań, specyfikacja i lista cen.", "Plantegninger for alle fem tilgjengelige boliger, spesifikasjonen og prislisten.", "Planritningar för alla fem tillgängliga bostäder, specifikationen och prislistan.")
a(117, 'See this alongside the other Fuengirola and Mijas projects', "Véalo junto a los demás proyectos de Fuengirola y Mijas que representamos.", "Découvrez ce programme aux côtés des autres projets de Fuengirola et Mijas que nous représentons.",
  "Sehen Sie dieses Projekt neben den anderen Projekten in Fuengirola und Mijas, die wir vertreten.", "Посмотрите этот проект рядом с другими проектами в Фуэнхироле и Михасе, которые мы представляем.", "شاهد هذا المشروع إلى جانب مشاريع فوينخيرولا وميخاس الأخرى التي نمثّلها.",
  "Bekijk dit project naast de andere projecten in Fuengirola en Mijas die wij vertegenwoordigen.", "Zobacz tę inwestycję obok innych projektów w Fuengirola i Mijas, które reprezentujemy.", "Se dette sammen med de andre prosjektene i Fuengirola og Mijas som vi representerer.", "Se detta tillsammans med de andra projekten i Fuengirola och Mijas som vi representerar.")
a(118, 'Walk the finished blocks', "Recorra con nosotros los bloques terminados, la zona de piscinas y el camino a la playa.", "Parcourez avec nous les blocs achevés, l'espace piscines et le chemin de la plage.",
  "Gehen Sie mit uns durch die fertigen Blöcke, den Poolbereich und den Weg zum Strand.", "Пройдите с нами по готовым блокам, зоне бассейнов и маршруту до пляжа.", "تجوّل معنا في المباني المكتملة ومنطقة المسابح وطريق الشاطئ.",
  "Loop met ons door de afgeronde blokken, het zwembadgebied en de route naar het strand.", "Proszę przejść z nami przez ukończone bloki, strefę basenów i trasę na plażę.", "Gå med oss gjennom de ferdige byggene, bassengområdet og veien til stranden.", "Gå med oss genom de färdiga husen, poolområdet och vägen till stranden.")
a(119, 'See it <em>finished</em>', "Véalo <em>terminado</em>", "Voyez-le <em>achevé</em>", "Sehen Sie es <em>fertig</em>", "Посмотрите <em>на готовое</em>", "شاهده <em>مكتملاً</em>",
  "Bekijk het <em>afgerond</em>", "Zobacz to <em>ukończone</em>", "Se det <em>ferdig</em>", "Se det <em>färdigt</em>")
a(120, 'The homes are built, so a visit is about the apartment itself', "Las viviendas están construidas, así que la visita trata del propio apartamento: la luz, la terraza, la vista y el paseo hasta la playa.",
  "Les logements sont construits, la visite porte donc sur l'appartement lui-même : la lumière, la terrasse, la vue et le trajet à pied jusqu'à la plage.",
  "Die Wohnungen sind gebaut, daher geht es bei einer Besichtigung um die Wohnung selbst: das Licht, die Terrasse, die Aussicht und den Fußweg zum Strand.",
  "Квартиры построены, поэтому просмотр посвящён самой квартире: свету, террасе, виду и пути пешком до пляжа.", "المساكن مبنية، لذا تدور المعاينة حول الشقة نفسها: الضوء والتراس والإطلالة والمشي إلى الشاطئ.",
  "De woningen zijn gebouwd, dus een bezichtiging gaat over het appartement zelf: het licht, het terras, het uitzicht en de wandeling naar het strand.",
  "Mieszkania są wybudowane, więc oglądanie dotyczy samego apartamentu: światła, tarasu, widoku i spaceru na plażę.", "Boligene er bygget, så en visning handler om selve leiligheten: lyset, terrassen, utsikten og gåturen til stranden.", "Bostäderna är byggda, så en visning handlar om själva lägenheten: ljuset, terrassen, utsikten och promenaden till stranden.")
a(121, 'Walk the blocks, the pool area', "Recorra los bloques, la zona de piscinas y la vivienda que está considerando.", "Parcourez les blocs, l'espace piscines et le logement que vous envisagez.",
  "Gehen Sie durch die Blöcke, den Poolbereich und die Wohnung, die Sie in Betracht ziehen.", "Пройдите по блокам, зоне бассейнов и квартире, которую вы рассматриваете.", "تجوّل في المباني ومنطقة المسابح والمسكن الذي تفكر فيه.",
  "Loop door de blokken, het zwembadgebied en de woning die u overweegt.", "Proszę przejść przez bloki, strefę basenów i rozważany lokal.", "Gå gjennom byggene, bassengområdet og boligen du vurderer.", "Gå genom husen, poolområdet och den bostad ni överväger.")
a(122, 'We walk the route to Carvajal beach with you', "Recorremos con usted el camino a la playa de Carvajal y lo cronometramos.", "Nous parcourons avec vous le chemin de la plage de Carvajal et le chronométrons.",
  "Wir gehen mit Ihnen den Weg zum Strand von Carvajal und stoppen die Zeit.", "Мы вместе с вами пройдём путь до пляжа Карвахаль и засечём время.", "نسير معك الطريق إلى شاطئ كارفاخال ونحسب الوقت.",
  "Wij lopen de route naar het strand van Carvajal samen met u en timen die.", "Przechodzimy z Państwem trasę na plażę Carvajal i mierzymy czas.", "Vi går veien til stranden i Carvajal sammen med deg og tar tiden.", "Vi går vägen till stranden i Carvajal tillsammans med er och tar tiden.")
a(123, 'Occupation licence, energy certificate and bank guarantee', "Licencia de ocupación, certificado energético y aval bancario, antes de firmar nada.", "Permis d'occupation, certificat énergétique et garantie bancaire, avant toute signature.",
  "Bezugsgenehmigung, Energieausweis und Bankgarantie, bevor etwas unterschrieben wird.", "Разрешение на заселение, энергетический сертификат и банковская гарантия — до подписания чего-либо.", "رخصة الإشغال وشهادة الطاقة والضمان المصرفي، قبل توقيع أي شيء.",
  "Gebruiksvergunning, energiecertificaat en bankgarantie, vóór er iets wordt ondertekend.", "Pozwolenie na zasiedlenie, świadectwo energetyczne i gwarancja bankowa — zanim cokolwiek zostanie podpisane.", "Bruksbevis, energiattest og bankgaranti, før noe signeres.", "Inflyttningstillstånd, energicertifikat och bankgaranti, innan något skrivs under.")
a(124, 'Ask about <em>Higueron Seaside Residences</em>', "Pregunte por <em>Higueron Seaside Residences</em>", "Renseignez-vous sur <em>Higueron Seaside Residences</em>", "Fragen Sie nach <em>Higueron Seaside Residences</em>",
  "Узнайте больше об <em>Higueron Seaside Residences</em>", "استفسر عن <em>Higueron Seaside Residences</em>", "Vraag naar <em>Higueron Seaside Residences</em>", "Zapytaj o <em>Higueron Seaside Residences</em>", "Spør om <em>Higueron Seaside Residences</em>", "Fråga om <em>Higueron Seaside Residences</em>")
a(125, 'Tell us what you need and we will come back with current availability, the specification and floorplans', "Cuéntenos lo que necesita y le responderemos con la disponibilidad actual, la memoria de calidades y los planos.",
  "Dites-nous ce dont vous avez besoin et nous reviendrons vers vous avec la disponibilité actuelle, le descriptif de la qualité et les plans.",
  "Sagen Sie uns, was Sie brauchen, und wir melden uns mit der aktuellen Verfügbarkeit, der Ausstattungsbeschreibung und den Grundrissen.", "Расскажите, что вам нужно, и мы вернёмся с актуальным наличием, спецификацией и планировками.",
  "أخبرنا بما تحتاجه وسنعود إليك بالتوفر الحالي والمواصفات والمخططات.", "Vertel ons wat u nodig hebt en wij komen terug met de actuele beschikbaarheid, de specificatie en de plattegronden.",
  "Proszę napisać, czego Państwo potrzebują, a wrócimy z aktualną dostępnością, specyfikacją i rzutami.", "Fortell oss hva du trenger, så kommer vi tilbake med aktuell tilgjengelighet, spesifikasjonen og plantegninger.", "Berätta vad ni behöver så återkommer vi med aktuell tillgänglighet, specifikationen och planritningar.")
a(126, 'Hello Nueva Living, I would like information about Higueron Seaside Residences.', "Hola Nueva Living, me gustaría recibir información sobre Higueron Seaside Residences.", "Bonjour Nueva Living, je souhaite recevoir des informations sur Higueron Seaside Residences.",
  "Hallo Nueva Living, ich interessiere mich für Informationen zu Higueron Seaside Residences.", "Здравствуйте, Nueva Living! Я хотел бы получить информацию о Higueron Seaside Residences.", "مرحبًا Nueva Living، أرغب في الحصول على معلومات عن Higueron Seaside Residences.",
  "Hallo Nueva Living, ik ontvang graag informatie over Higueron Seaside Residences.", "Witam Nueva Living, chciałbym/chciałabym otrzymać informacje o Higueron Seaside Residences.", "Hei Nueva Living, jeg ønsker informasjon om Higueron Seaside Residences.", "Hej Nueva Living, jag vill gärna få information om Higueron Seaside Residences.")
a(127, 'How many homes are available?', "¿Cuántas viviendas hay disponibles?", "Combien de logements sont disponibles ?", "Wie viele Wohnungen sind verfügbar?", "Сколько квартир доступно?", "كم مسكناً متاحاً؟",
  "Hoeveel woningen zijn beschikbaar?", "Ile mieszkań jest dostępnych?", "Hvor mange boliger er tilgjengelige?", "Hur många bostäder är tillgängliga?")
a(128, 'The development has sixty homes and five are currently listed', "La promoción tiene sesenta viviendas y cinco figuran ahora como disponibles: los apartamentos 2, 24 y 33 en la planta baja y los áticos, apartamentos 8 y 23, en la tercera planta, desde {E567000} hasta {E881000}.",
  "Le programme compte soixante logements et cinq figurent actuellement comme disponibles : les appartements 2, 24 et 33 au rez-de-chaussée et les penthouses, appartements 8 et 23, au troisième étage, de {E567000} à {E881000}.",
  "Das Projekt hat sechzig Wohnungen, von denen fünf derzeit als verfügbar gelistet sind: die Wohnungen 2, 24 und 33 im Erdgeschoss und die Penthouses, Wohnungen 8 und 23, im dritten Obergeschoss, von {E567000} bis {E881000}.",
  "В комплексе шестьдесят квартир, и пять из них сейчас в продаже: квартиры 2, 24 и 33 на первом этаже и пентхаусы — квартиры 8 и 23 — на четвёртом этаже, по ценам от {E567000} до {E881000}.",
  "يضم المشروع ستين مسكناً وخمسة منها مدرجة حالياً كمتاحة: الشقق 2 و24 و33 في الطابق الأرضي والبنتهاوس، الشقتان 8 و23، في الطابق الثالث، بأسعار من {E567000} إلى {E881000}.",
  "Het project telt zestig woningen, waarvan er vijf momenteel als beschikbaar zijn vermeld: appartement 2, 24 en 33 op de begane grond en de penthouses, appartement 8 en 23, op de derde verdieping, van {E567000} tot {E881000}.",
  "Inwestycja obejmuje sześćdziesiąt mieszkań, z których pięć figuruje obecnie jako dostępne: apartamenty 2, 24 i 33 na parterze oraz penthouse’y, apartamenty 8 i 23, na trzecim piętrze, w cenach od {E567000} do {E881000}.",
  "Prosjektet har seksti boliger, og fem er for øyeblikket oppført som tilgjengelige: leilighet 2, 24 og 33 i første etasje og toppleilighetene, leilighet 8 og 23, i fjerde etasje, fra {E567000} til {E881000}.",
  "Projektet har sextio bostäder och fem är just nu angivna som tillgängliga: lägenhet 2, 24 och 33 på bottenvåningen och takvåningarna, lägenhet 8 och 23, på tredje våningen, från {E567000} till {E881000}.")
a(129, 'Is it finished?', "¿Está terminado?", "Est-il achevé ?", "Ist es fertiggestellt?", "Он завершён?", "هل هو مكتمل؟", "Is het afgerond?", "Czy jest ukończone?", "Er det ferdigstilt?", "Är det färdigställt?")
a(130, 'The developer’s price list gives delivery as key ready', "La lista de precios de la promotora indica la entrega como llave en mano, y su memoria de calidades del 8 de octubre de 2026 dice lo mismo. Su circular informativa de febrero de 2023 daba el 30 de noviembre de 2024 como fecha de entrega. Pedimos la licencia de ocupación y el certificado energético de la vivienda que elija.",
  "La liste de prix du promoteur indique une livraison clés en main, et son descriptif de la qualité du 8 octobre 2026 dit la même chose. Sa circulaire d'information de février 2023 donnait le 30 novembre 2024 comme date de livraison. Nous demandons le permis d'occupation et le certificat énergétique du logement que vous choisissez.",
  "Die Preisliste des Bauträgers nennt die Übergabe als schlüsselfertig, und seine Qualitätsbeschreibung vom 8. Oktober 2026 sagt dasselbe. Sein Informationsschreiben vom Februar 2023 nannte den 30. November 2024 als Übergabetermin. Wir fordern die Bezugsgenehmigung und den Energieausweis der von Ihnen gewählten Wohnung an.",
  "В прайс-листе застройщика сдача указана как «под ключ», и то же сказано в его описании качества от 8 октября 2026 года. В информационном письме от февраля 2023 года сроком сдачи значилось 30 ноября 2024 года. Мы запрашиваем разрешение на заселение и энергетический сертификат на выбранную вами квартиру.",
  "تذكر قائمة أسعار المطور أن التسليم جاهز بالمفتاح، وتقول مذكرة الجودة الصادرة عنه في 8 أكتوبر 2026 الشيء نفسه. وكان تعميمه الصادر في فبراير 2023 يذكر 30 نوفمبر 2024 موعداً للتسليم. نطلب رخصة الإشغال وشهادة الطاقة للمسكن الذي تختاره.",
  "De prijslijst van de ontwikkelaar geeft de oplevering als sleutelklaar, en zijn kwaliteitsomschrijving van 8 oktober 2026 zegt hetzelfde. Zijn informatiebrief van februari 2023 gaf 30 november 2024 als opleverdatum. Wij vragen de gebruiksvergunning en het energiecertificaat van de woning die u kiest op.",
  "Lista cen dewelopera podaje odbiór jako „pod klucz”, a jego opis jakości z 8 października 2026 roku mówi to samo. Jego pismo informacyjne z lutego 2023 roku podawało 30 listopada 2024 roku jako termin odbioru. Prosimy o pozwolenie na zasiedlenie i świadectwo energetyczne wybranego przez Państwa lokalu.",
  "Utviklerens prisliste oppgir overlevering som nøkkelferdig, og kvalitetsbeskrivelsen hans fra 8. oktober 2026 sier det samme. Informasjonsskrivet fra februar 2023 oppga 30. november 2024 som overleveringsdato. Vi ber om bruksbevis og energiattest for boligen du velger.",
  "Byggherrens prislista anger leveransen som nyckelfärdig, och hans kvalitetsbeskrivning från den 8 oktober 2026 säger detsamma. Informationsbrevet från februari 2023 angav den 30 november 2024 som leveransdatum. Vi begär inflyttningstillstånd och energicertifikat för den bostad ni väljer.")
a(131, 'What comes with the price?', "¿Qué incluye el precio?", "Qu'est-ce qui est inclus dans le prix ?", "Was ist im Preis enthalten?", "Что входит в цену?", "ما الذي يشمله السعر؟", "Wat is bij de prijs inbegrepen?", "Co obejmuje cena?", "Hva er inkludert i prisen?", "Vad ingår i priset?")
a(132, 'Each home includes two parking spaces and a storeroom in the basement', "Cada vivienda incluye dos plazas de aparcamiento y un trastero en el sótano. La lista de precios muestra una cifra de equipamiento aparte sobre el precio, {E31700} para las viviendas de dos dormitorios y {E45000} para el apartamento de tres dormitorios, que confirmamos antes de cualquier reserva.",
  "Chaque logement comprend deux places de stationnement et un débarras au sous-sol. La liste de prix indique un montant d'équipement distinct en plus du prix, {E31700} pour les logements de deux chambres et {E45000} pour l'appartement de trois chambres, que nous confirmons avant toute réservation.",
  "Jede Wohnung umfasst zwei Stellplätze und einen Abstellraum im Untergeschoss. Die Preisliste nennt zusätzlich zum Preis einen gesonderten Ausstattungsbetrag, {E31700} für die Zweizimmerwohnungen und {E45000} für die Dreizimmerwohnung, den wir vor jeder Reservierung bestätigen.",
  "В каждую квартиру входят два парковочных места и кладовая в цоколе. В прайс-листе сверх цены указана отдельная сумма за оснащение: {E31700} для квартир с двумя спальнями и {E45000} для квартиры с тремя; мы подтверждаем её до любого бронирования.",
  "يشمل كل مسكن موقفي سيارات ومخزناً في القبو. وتُظهر قائمة الأسعار رقم تجهيز منفصلاً فوق السعر، {E31700} للمساكن ذات الغرفتين و{E45000} للشقة ذات الغرف الثلاث، ونؤكده قبل أي حجز.",
  "Elke woning omvat twee parkeerplaatsen en een berging in de kelder. De prijslijst toont bovenop de prijs een apart uitrustingsbedrag, {E31700} voor de woningen met twee slaapkamers en {E45000} voor het appartement met drie, dat wij vóór elke reservering bevestigen.",
  "Każdy lokal obejmuje dwa miejsca parkingowe i komórkę lokatorską w piwnicy. Lista cen pokazuje ponad cenę odrębną kwotę za wyposażenie, {E31700} dla mieszkań z dwiema sypialniami i {E45000} dla apartamentu z trzema, którą potwierdzamy przed jakąkolwiek rezerwacją.",
  "Hver bolig inkluderer to parkeringsplasser og en bod i kjelleren. Prislisten viser et separat utstyrsbeløp på toppen av prisen, {E31700} for boligene med to soverom og {E45000} for leiligheten med tre, som vi bekrefter før enhver reservasjon.",
  "Varje bostad inkluderar två parkeringsplatser och ett förråd i källaren. Prislistan visar ett separat utrustningsbelopp utöver priset, {E31700} för bostäderna med två sovrum och {E45000} för lägenheten med tre, som vi bekräftar före varje reservation.")
a(133, 'What do the penthouses have?', "¿Qué tienen los áticos?", "Que comprennent les penthouses ?", "Was bieten die Penthouses?", "Что есть в пентхаусах?", "ما الذي تضمه البنتهاوس؟", "Wat hebben de penthouses?", "Co mają penthouse’y?", "Hva har toppleilighetene?", "Vad har takvåningarna?")
a(134, 'Each third-floor penthouse has an open terrace', "Cada ático de la tercera planta tiene una terraza descubierta y un solárium en la azotea de {N94.75} o {N97.48} {U}, al que se sube por una escalera privada, con barbacoa, ducha de agua fría y caliente y preinstalación para un jacuzzi.",
  "Chaque penthouse du troisième étage a une terrasse découverte et un solarium sur le toit de {N94.75} ou {N97.48} {U}, accessible par un escalier privé, avec barbecue, douche d'eau chaude et froide et pré-équipement pour un jacuzzi.",
  "Jedes Penthouse im dritten Obergeschoss hat eine offene Terrasse und ein Dach-Solarium von {N94.75} oder {N97.48} {U}, erreichbar über eine private Treppe, mit Grill, Dusche mit Warm- und Kaltwasser und Vorinstallation für einen Whirlpool.",
  "У каждого пентхауса на четвёртом этаже есть открытая терраса и солярий на крыше площадью {N94.75} или {N97.48} {U}, на который ведёт частная лестница; там есть гриль, душ с горячей и холодной водой и подготовка под джакузи.",
  "لكل بنتهاوس في الطابق الثالث تراس مكشوف وسولاريوم على السطح بمساحة {N94.75} أو {N97.48} {U}، يُصعد إليه بدرج خاص، مع شواية ودش بماء بارد وساخن وتجهيز مسبق لجاكوزي.",
  "Elk penthouse op de derde verdieping heeft een open terras en een solarium op het dak van {N94.75} of {N97.48} {U}, bereikbaar via een eigen trap, met barbecue, douche met warm en koud water en voorbereiding voor een bubbelbad.",
  "Każdy penthouse na trzecim piętrze ma otwarty taras i solarium na dachu o powierzchni {N94.75} lub {N97.48} {U}, na które prowadzą prywatne schody, z grillem, prysznicem z ciepłą i zimną wodą i instalacją pod jacuzzi.",
  "Hver toppleilighet i fjerde etasje har en åpen terrasse og en solterrasse på taket på {N94.75} eller {N97.48} {U}, nådd via en privat trapp, med grill, dusj med varmt og kaldt vann og forberedelse for boblebad.",
  "Varje takvåning på tredje våningen har en öppen terrass och en solterrass på taket på {N94.75} eller {N97.48} {U}, nås via en privat trappa, med grill, dusch med varmt och kallt vatten och förberedelse för bubbelpool.")
a(135, 'The developer’s February 2023 circular says 350 m', "La circular informativa de la promotora de febrero de 2023 dice {N350} {M} hasta la playa de Carvajal y su catálogo de 2025 dice {N700} {M}. Recorremos el camino con usted en una visita.",
  "La circulaire d'information du promoteur de février 2023 indique {N350} {M} jusqu'à la plage de Carvajal et son catalogue de 2025 indique {N700} {M}. Nous parcourons le chemin avec vous lors d'une visite.",
  "Das Informationsschreiben des Bauträgers vom Februar 2023 nennt {N350} {M} bis zum Strand von Carvajal, sein Katalog von 2025 nennt {N700} {M}. Bei einer Besichtigung gehen wir den Weg mit Ihnen ab.",
  "В информационном письме застройщика от февраля 2023 года до пляжа Карвахаль указано {N350} {M}, в его каталоге 2025 года — {N700} {M}. Во время просмотра мы пройдём этот путь вместе с вами.",
  "يذكر تعميم المطور الصادر في فبراير 2023 مسافة {N350} {M} إلى شاطئ كارفاخال، ويذكر كتيّبه لعام 2025 مسافة {N700} {M}. نسير معك الطريق أثناء المعاينة.",
  "De informatiebrief van de ontwikkelaar van februari 2023 noemt {N350} {M} tot het strand van Carvajal en zijn catalogus uit 2025 noemt {N700} {M}. Wij lopen de route bij een bezichtiging met u.",
  "Pismo informacyjne dewelopera z lutego 2023 roku podaje {N350} {M} do plaży Carvajal, a jego katalog z 2025 roku {N700} {M}. Podczas oglądania przechodzimy tę trasę razem z Państwem.",
  "Utviklerens informasjonsskriv fra februar 2023 oppgir {N350} {M} til stranden i Carvajal, og katalogen fra 2025 oppgir {N700} {M}. Vi går veien sammen med deg under en visning.",
  "Byggherrens informationsbrev från februari 2023 anger {N350} {M} till stranden i Carvajal, och katalogen från 2025 anger {N700} {M}. Vi går vägen tillsammans med er under en visning.")

# ---------------------------------------------------------------- write
missing = [i for i, en in enumerate(todo) if en not in T]
assert not missing, f'not translated: {missing}'
json.dump(T, open(f'{SP}/import_h/tr_z.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')

# ---------------------------------------------------------------- after assemble.py
# overlay_shape has no `highlights` key, so assemble leaves them in English; unit references and
# residence names stay English in every overlay (localizedUnitFloor() translates them at render
# time). Run this script a second time after assemble.py to apply both.
H = {
 'Cement render and paint in combined colours, with lacquered metal screens on some volumes, stairwells and galleries.':
  ("Enfoscado de cemento y pintura en colores combinados, con celosías metálicas lacadas en algunos volúmenes, núcleos de escaleras y galerías.",
   "Enduit de ciment et peinture en couleurs combinées, avec des claustras métalliques laquées sur certains volumes, cages d'escalier et galeries.",
   "Zementputz und Anstrich in kombinierten Farben, mit lackierten Metallelementen an einzelnen Baukörpern, Treppenhäusern und Galerien.",
   "Цементная штукатурка и покраска в сочетании цветов, лакированные металлические экраны на отдельных объёмах, лестничных клетках и галереях.",
   "لياسة إسمنتية ودهان بألوان متناسقة، مع ستائر معدنية مطلية على بعض الكتل وأبراج السلالم والممرات.",
   "Cementstuc en verf in gecombineerde kleuren, met gelakte metalen schermen op enkele volumes, trappenhuizen en galerijen.",
   "Tynk cementowy i farba w zestawieniu kolorów, z lakierowanymi metalowymi ekranami na niektórych bryłach, klatkach schodowych i galeriach.",
   "Sementpuss og maling i kombinerte farger, med lakkerte metallskjermer på enkelte volumer, trappeoppganger og gallerier.",
   "Cementputs och färg i kombinerade kulörer, med lackerade metallskärmar på vissa volymer, trapphus och gallerier."),
 'Large terraces and covered porches, glass balustrades, and pergolas that filter the light on the top floor.':
  ("Grandes terrazas y porches cubiertos, barandillas de vidrio y pérgolas que filtran la luz en la última planta.",
   "De grandes terrasses et porches couverts, des garde-corps en verre et des pergolas qui filtrent la lumière au dernier étage.",
   "Große Terrassen und überdachte Vorbauten, Glasbrüstungen und Pergolen, die im obersten Geschoss das Licht filtern.",
   "Большие террасы и крытые портики, стеклянные ограждения и перголы, рассеивающие свет на верхнем этаже.",
   "تراسات كبيرة وأروقة مغطاة ودرابزينات زجاجية وبرغولات تصفّي الضوء في الطابق الأخير.",
   "Grote terrassen en overdekte veranda’s, glazen balustrades en pergola’s die op de bovenste verdieping het licht filteren.",
   "Duże tarasy i zadaszone ganki, szklane balustrady oraz pergole filtrujące światło na najwyższej kondygnacji.",
   "Store terrasser og overbygde verandaer, glassrekkverk og pergolaer som filtrerer lyset i øverste etasje.",
   "Stora terrasser och övertäckta verandor, glasräcken och pergolor som filtrerar ljuset på översta våningen."),
 'Every home faces south-west, with views of the sea, the mountains or the shared gardens depending on the home.':
  ("Todas las viviendas miran al suroeste, con vistas al mar, a las montañas o a los jardines comunes según la vivienda.",
   "Tous les logements sont orientés sud-ouest, avec vue sur la mer, les montagnes ou les jardins communs selon le logement.",
   "Alle Wohnungen sind nach Südwesten ausgerichtet, je nach Wohnung mit Blick auf das Meer, die Berge oder die gemeinsamen Gärten.",
   "Все квартиры ориентированы на юго-запад; в зависимости от квартиры открывается вид на море, горы или общие сады.",
   "تتجه جميع المساكن نحو الجنوب الغربي، مع إطلالة على البحر أو الجبال أو الحدائق المشتركة بحسب المسكن.",
   "Alle woningen liggen op het zuidwesten, met uitzicht op de zee, de bergen of de gemeenschappelijke tuinen, afhankelijk van de woning.",
   "Wszystkie lokale są zwrócone na południowy zachód, z widokiem na morze, góry lub wspólne ogrody, zależnie od lokalu.",
   "Alle boligene vender mot sørvest, med utsikt mot havet, fjellene eller de felles hagene avhengig av boligen.",
   "Alla bostäder vetter mot sydväst, med utsikt över havet, bergen eller de gemensamma trädgårdarna beroende på bostad."),
 'The ground-floor homes have a private garden of artificial lawn, enclosed by a wall and a metal fence with a cypress hedge.':
  ("Las viviendas de planta baja tienen un jardín privado de césped artificial, cerrado con un muro y una verja metálica con seto de ciprés.",
   "Les logements du rez-de-chaussée ont un jardin privé en gazon artificiel, clos par un muret et une grille métallique avec une haie de cyprès.",
   "Die Erdgeschosswohnungen haben einen privaten Garten mit Kunstrasen, eingefasst von einer Mauer und einem Metallzaun mit Zypressenhecke.",
   "У квартир на первом этаже есть частный сад с искусственным газоном, огороженный стеной и металлической решёткой с кипарисовой изгородью.",
   "لمساكن الطابق الأرضي حديقة خاصة بعشب صناعي، محاطة بجدار وسياج معدني وسور من أشجار السرو.",
   "De woningen op de begane grond hebben een privétuin met kunstgras, omsloten door een muur en een metalen hek met een cipressenhaag.",
   "Lokale na parterze mają prywatny ogród ze sztuczną trawą, ogrodzony murem i metalowym płotem z żywopłotem z cyprysów.",
   "Boligene i første etasje har en privat hage med kunstgress, innhegnet av en mur og et metallgjerde med sypresshekk.",
   "Bostäderna på bottenvåningen har en privat trädgård med konstgräs, inhägnad av en mur och ett metallstaket med cypresshäck."),
 'Facades': ("Fachadas", "Façades", "Fassaden", "Фасады", "الواجهات", "Gevels", "Elewacje", "Fasader", "Fasader"),
}
P = f'content/liora-projects/higueron-seaside-residences/project.json'
tm_words = json.load(open(f'{SP}/import_h/tm.json'))
proj = json.load(open(P))
if proj.get('i18n'):
    for l_i, l in enumerate(LOCS):
        ov = proj['i18n'][l]
        for row, src in zip(ov['architecture']['highlights'], proj['architecture']['highlights']):
            for col in (0, 1):
                tr = H.get(src[col])
                if tr is not None:
                    row[col] = tr[l_i]
                elif src[col] in tm_words:
                    row[col] = tm_words[src[col]][l]
        for row, src in zip(ov['residences']['items'], proj['residences']['items']):
            row['name'] = src['name']
        for row, src in zip(ov['availability']['units'], proj['availability']['units']):
            row['reference'] = src['reference']
    json.dump(proj, open(P, 'w'), ensure_ascii=False, indent=2)
    open(P, 'a').write('\n')
    print('overlays patched')
