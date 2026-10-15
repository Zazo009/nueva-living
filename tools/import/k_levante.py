# -*- coding: utf-8 -*-
# Levante Residences, human translations in one pass.
# p(path, es, fr, de, ru, ar, nl, pl, no, sv)
#
# The English string is looked up from the path scaffold.py printed in todo.json, so it is
# never copied here and cannot drift from project.json. The number after the path is what
# scaffold calls its index, kept as a comment for whoever reads this next.
#
# Three tokens are expanded per locale, so a figure is written once and takes its locale's
# own format: €442000 -> "442.000 €" (nl "€ 442.000", fr/ru/pl/no/sv "442 000 €", ar
# "442,000 €"), #93.8 -> "93,8" (ar "93.8"), and [m2] is the area unit: m² everywhere but
# ru "м²" and ar "م²".
#
# The seven unit rows, their references and the floorplan labels are built by function
# below from the same six numbers the English was built from.
#
#   python3 tools/import/k_levante.py <workdir>/tr_z.json <workdir>/todo.json
import json, re, sys

LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}
UNIT['ru'] = 'м²'
UNIT['ar'] = 'م²'


def money(n, loc):
    body = f'{n:,}'.replace(',', GROUP[loc])
    return f'€ {body}' if loc == 'nl' else f'{body} €'


def expand(s, loc):
    s = re.sub(r'€(\d+)', lambda m: money(int(m.group(1)), loc), s)
    s = re.sub(r'#(\d+)\.(\d+)', lambda m: m.group(1) + ('.' if loc == 'ar' else ',') + m.group(2), s)
    return s.replace('[m2]', UNIT[loc])


T = {}
TODO = json.load(open(sys.argv[2]))
BY_PATH = {paths[0]: en for en, paths in TODO.items()}
USED = set()


def p(path, *tr):
    assert len(tr) == 9, path
    en = BY_PATH[path]
    USED.add(path)
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---- identifiers that read the same in every language -------------------------------------
for path, en in BY_PATH.items():
    if re.fullmatch(r'Levante( <em>Residences</em>| Residences)?', en) or re.fullmatch(r'\d\d-\d\d-BJ-[A-C]', en):
        T[en] = {l: en for l in LOCS}
        USED.add(path)

# ---- unit rows: the same words every other project uses, in the same order ----------------
BUILT = {'es': 'm² construidos', 'fr': 'm² construits', 'de': 'm² bebaut', 'ru': 'м² застроенной площади',
         'ar': 'م² مبنية', 'nl': 'm² bebouwd', 'pl': 'm² zabudowy', 'no': 'm² bygd', 'sv': 'm² byggyta'}
INNER = {'es': 'm² interiores', 'fr': 'm² intérieurs', 'de': 'm² Innenfläche', 'ru': 'м² внутри',
         'ar': 'م² داخلية', 'nl': 'm² binnen', 'pl': 'm² wnętrza', 'no': 'm² innvendig', 'sv': 'm² inomhus'}
TERR = {'es': 'm² de terraza', 'fr': 'm² de terrasse', 'de': 'm² Terrasse', 'ru': 'терраса {} м²',
        'ar': 'م² تراس', 'nl': 'm² terras', 'pl': 'm² tarasu', 'no': 'm² terrasse', 'sv': 'm² terrass'}
GARD = {'es': 'm² de jardín', 'fr': 'm² de jardin', 'de': 'm² Garten', 'ru': 'сад {} м²',
        'ar': 'م² حديقة', 'nl': 'm² tuin', 'pl': 'm² ogrodu', 'no': 'm² hage', 'sv': 'm² trädgård'}
SEP = {l: ', ' for l in LOCS}
SEP['ar'] = '، '


def dec(x, loc):
    return f'{x:.1f}'.replace('.', '.' if loc == 'ar' else ',')


def size(built, inner, terr, garden, loc):
    parts = [f'{dec(built, loc)} {BUILT[loc]}', f'{dec(inner, loc)} {INNER[loc]}']
    for x, tpl in ((terr, TERR), (garden, GARD)):
        if x is None:
            continue
        t = tpl[loc]
        parts.append(t.format(dec(x, loc) ) if '{}' in t else f'{dec(x, loc)} {t}')
    return SEP[loc].join(parts)


# (path index in the English units array, built, interior, terrace total, garden)
UNITS = [(0, 98.7, 75.4, 65.7, None), (1, 143.3, 101.3, 11.2, 41.8), (2, 124.3, 92.9, 46.8, None),
         (3, 93.8, 71.7, 69.6, None), (4, 124.1, 92.9, 71.0, None), (5, 119.5, 89.8, 27.1, 175.6),
         (6, 94.6, 72.5, 24.8, 60.2)]
for i, b, n, t, g in UNITS:
    path = f'.availability.units[{i}].size'
    en = BY_PATH[path]
    T[en] = {l: size(b, n, t, g, l) for l in LOCS}
    USED.add(path)

# floorplan alt and caption per unit: a template and the reference
PLAN_ALT = {'es': 'Plano de la vivienda {}', 'fr': 'Plan du logement {}', 'de': 'Grundriss der Wohnung {}',
            'ru': 'Планировка квартиры {}', 'ar': 'مخطط المسكن {}', 'nl': 'Plattegrond van woning {}',
            'pl': 'Rzut lokalu {}', 'no': 'Plantegning av bolig {}', 'sv': 'Planritning för bostad {}'}
PLAN_CAP = {'es': 'Vivienda {}', 'fr': 'Logement {}', 'de': 'Wohnung {}', 'ru': 'Квартира {}',
            'ar': 'المسكن {}', 'nl': 'Woning {}', 'pl': 'Lokal {}', 'no': 'Bolig {}', 'sv': 'Bostad {}'}
for path, en in list(BY_PATH.items()):
    m = re.fullmatch(r'Floorplan of home (\S+)', en)
    if m:
        T[en] = {l: PLAN_ALT[l].format(m.group(1)) for l in LOCS}
        USED.add(path)
    m = re.fullmatch(r'Home (\d\d-\d\d-BJ-[A-C])', en)
    if m:
        T[en] = {l: PLAN_CAP[l].format(m.group(1)) for l in LOCS}
        USED.add(path)

# ---- head and card ------------------------------------------------------------------------
p('.description',  # 3
  'Siete de las 80 viviendas de dos y tres dormitorios de Cancelada, en la Nueva Milla de Oro de Estepona, figuran como disponibles: viviendas en planta baja con jardín o grandes terrazas, una plaza de garaje y un trastero cada una, una de ellas dúplex. La entrega figura para abril de 2028. Desde €442000 más IVA.',
  'Sept des 80 logements de deux et trois chambres de Cancelada, sur la Nouvelle Mille d’Or d’Estepona, sont annoncés comme disponibles : des logements en rez-de-chaussée avec jardin ou grandes terrasses, une place de garage et une cave chacun, dont un duplex. La livraison est annoncée pour avril 2028. À partir de €442000 hors TVA.',
  'Sieben der 80 Wohnungen mit zwei und drei Schlafzimmern in Cancelada an der Neuen Goldenen Meile von Estepona sind als verfügbar gelistet: Wohnungen im Erdgeschoss mit Garten oder großen Terrassen, mit je einem Garagenstellplatz und einem Abstellraum, eine davon eine Maisonette. Die Übergabe ist für April 2028 angegeben. Ab €442000 zuzüglich MwSt.',
  'Семь из 80 квартир с двумя и тремя спальнями в Канселаде, на Новой Золотой миле Эстепоны, указаны как доступные: квартиры на первом этаже с садом или большими террасами, с местом в гараже и кладовой у каждой, одна из них — дуплекс. Срок сдачи указан — апрель 2028 года. От €442000 без НДС.',
  'سبعة من أصل 80 مسكنًا من غرفتي نوم وثلاث غرف نوم في كانسيلادا، على الميل الذهبي الجديد في إستيبونا، مدرجة كمتاحة: مساكن في الطابق الأرضي بحديقة أو تراسات واسعة، ولكل منها موقف سيارة في المرآب وغرفة تخزين، وأحدها دوبلكس. وموعد التسليم المذكور هو أبريل 2028. ابتداءً من €442000 دون ضريبة القيمة المضافة.',
  'Zeven van de 80 woningen met twee en drie slaapkamers in Cancelada, aan de Nieuwe Golden Mile van Estepona, staan als beschikbaar vermeld: woningen op de begane grond met een tuin of grote terrassen, elk met een garageplaats en een berging, waarvan één een duplex. De oplevering staat gepland voor april 2028. Vanaf €442000 excl. btw.',
  'Siedem z 80 mieszkań z dwiema i trzema sypialniami w miejscowości Cancelada, na Nowej Złotej Mili w Esteponie, jest podanych jako dostępne: mieszkania na parterze z ogrodem lub dużymi tarasami, z miejscem w garażu i komórką lokatorską, w tym jedno dwupoziomowe. Termin oddania podano na kwiecień 2028 r. Od €442000 plus VAT.',
  'Sju av de 80 boligene med to og tre soverom i Cancelada, på Estepones Nye Golden Mile, er oppgitt som tilgjengelige: boliger i første etasje med hage eller store terrasser, hver med en garasjeplass og en bod, hvorav én er en duplex. Overtakelse er oppgitt til april 2028. Fra €442000 pluss mva.',
  'Sju av de 80 bostäderna med två och tre sovrum i Cancelada, på Esteponas Nya Golden Mile, är listade som tillgängliga: bostäder i bottenvåningen med trädgård eller stora terrasser, var och en med en garageplats och ett förråd, varav en är en etagelägenhet. Tillträdet anges till april 2028. Från €442000 plus moms.')

p('.seoDescription',  # 4
  'Viviendas de dos y tres dormitorios con jardín o grandes terrazas en Cancelada, Estepona, con piscina, gimnasio y casa club, entrega prevista para abril de 2028, desde €442000 más IVA.',
  'Logements de deux et trois chambres avec jardin ou grandes terrasses à Cancelada, Estepona, avec piscine, salle de sport et club-house, livraison annoncée pour avril 2028, à partir de €442000 hors TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern, Garten oder großen Terrassen in Cancelada, Estepona, mit Pool, Fitnessraum und Clubhaus, Übergabe für April 2028 angegeben, ab €442000 zuzüglich MwSt.',
  'Квартиры с двумя и тремя спальнями, садом или большими террасами в Канселаде, Эстепона, с бассейном, тренажёрным залом и клубным домом, срок сдачи указан — апрель 2028 г., от €442000 без НДС.',
  'مساكن من غرفتي نوم وثلاث غرف نوم بحديقة أو تراسات واسعة في كانسيلادا، إستيبونا، مع مسبح وصالة رياضية ونادي المجمع، وموعد التسليم المذكور أبريل 2028، ابتداءً من €442000 دون ضريبة القيمة المضافة.',
  'Woningen met twee en drie slaapkamers, tuin of grote terrassen in Cancelada, Estepona, met zwembad, fitnessruimte en clubhuis, oplevering gepland voor april 2028, vanaf €442000 excl. btw.',
  'Mieszkania z dwiema i trzema sypialniami, ogrodem lub dużymi tarasami w miejscowości Cancelada, Estepona, z basenem, siłownią i klubem mieszkańców, termin oddania podano na kwiecień 2028 r., od €442000 plus VAT.',
  'Boliger med to og tre soverom, hage eller store terrasser i Cancelada, Estepona, med basseng, treningsrom og klubbhus, overtakelse oppgitt til april 2028, fra €442000 pluss mva.',
  'Bostäder med två och tre sovrum, trädgård eller stora terrasser i Cancelada, Estepona, med pool, gym och klubbhus, tillträde angivet till april 2028, från €442000 plus moms.')

p('.twitterDescription',  # 5
  'Viviendas de dos y tres dormitorios con jardín o grandes terrazas en Cancelada, Estepona, desde €442000 más IVA.',
  'Logements de deux et trois chambres avec jardin ou grandes terrasses à Cancelada, Estepona, à partir de €442000 hors TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern, Garten oder großen Terrassen in Cancelada, Estepona, ab €442000 zuzüglich MwSt.',
  'Квартиры с двумя и тремя спальнями, садом или большими террасами в Канселаде, Эстепона, от €442000 без НДС.',
  'مساكن من غرفتي نوم وثلاث غرف نوم بحديقة أو تراسات واسعة في كانسيلادا، إستيبونا، ابتداءً من €442000 دون ضريبة القيمة المضافة.',
  'Woningen met twee en drie slaapkamers, tuin of grote terrassen in Cancelada, Estepona, vanaf €442000 excl. btw.',
  'Mieszkania z dwiema i trzema sypialniami, ogrodem lub dużymi tarasami w miejscowości Cancelada, Estepona, od €442000 plus VAT.',
  'Boliger med to og tre soverom, hage eller store terrasser i Cancelada, Estepona, fra €442000 pluss mva.',
  'Bostäder med två och tre sovrum, trädgård eller stora terrasser i Cancelada, Estepona, från €442000 plus moms.')

p('.hero.location',  # 6
  'Cancelada, Estepona', 'Cancelada, Estepona', 'Cancelada, Estepona', 'Канселада, Эстепона',
  'كانسيلادا، إستيبونا', 'Cancelada, Estepona', 'Cancelada, Estepona', 'Cancelada, Estepona', 'Cancelada, Estepona')
p('.hero.startingPrice',  # 7
  'Desde €442000 + IVA', 'À partir de €442000 + TVA', 'Ab €442000 + MwSt.', 'От €442000 + НДС',
  'ابتداءً من €442000 + ضريبة القيمة المضافة', 'Vanaf €442000 + btw', 'Od €442000 + VAT', 'Fra €442000 + mva.', 'Från €442000 + moms')
p('.hero.delivery',  # 8
  'abril 2028', 'avril 2028', 'April 2028', 'апрель 2028', 'أبريل 2028', 'april 2028', 'kwiecień 2028', 'april 2028', 'april 2028')
p('.card.locExtended',  # 9
  'Cancelada', 'Cancelada', 'Cancelada', 'Канселада', 'كانسيلادا', 'Cancelada', 'Cancelada', 'Cancelada', 'Cancelada')
p('.card.description',  # 10
  'Viviendas de dos y tres dormitorios con jardín o grandes terrazas en una promoción de 80 viviendas en Cancelada, con piscina, gimnasio y casa club.',
  'Logements de deux et trois chambres avec jardin ou grandes terrasses dans un programme de 80 logements à Cancelada, avec piscine, salle de sport et club-house.',
  'Wohnungen mit zwei und drei Schlafzimmern, Garten oder großen Terrassen in einer Anlage mit 80 Wohnungen in Cancelada, mit Pool, Fitnessraum und Clubhaus.',
  'Квартиры с двумя и тремя спальнями, садом или большими террасами в комплексе из 80 квартир в Канселаде, с бассейном, тренажёрным залом и клубным домом.',
  'مساكن من غرفتي نوم وثلاث غرف نوم بحديقة أو تراسات واسعة في مشروع من 80 مسكنًا في كانسيلادا، مع مسبح وصالة رياضية ونادي المجمع.',
  'Woningen met twee en drie slaapkamers, tuin of grote terrassen in een project van 80 woningen in Cancelada, met zwembad, fitnessruimte en clubhuis.',
  'Mieszkania z dwiema i trzema sypialniami, ogrodem lub dużymi tarasami w inwestycji liczącej 80 lokali w miejscowości Cancelada, z basenem, siłownią i klubem mieszkańców.',
  'Boliger med to og tre soverom, hage eller store terrasser i et prosjekt med 80 boliger i Cancelada, med basseng, treningsrom og klubbhus.',
  'Bostäder med två och tre sovrum, trädgård eller stora terrasser i ett projekt med 80 bostäder i Cancelada, med pool, gym och klubbhus.')
p('.card.meta[0][1]',  # 11
  '€442000 + IVA', '€442000 + TVA', '€442000 + MwSt.', '€442000 + НДС', '€442000 + ضريبة القيمة المضافة', '€442000 + btw',
  '€442000 + VAT', '€442000 + mva.', '€442000 + moms')

# ---- images -------------------------------------------------------------------------------
p('.images.hero.alt',  # 12
  'Vista generada por ordenador de la piscina comunitaria frente a dos edificios blancos y color arena con terrazas escalonadas y palmeras',
  'Vue générée par ordinateur de la piscine commune devant deux bâtiments blancs et sable aux terrasses en gradins, avec des palmiers',
  'Computergenerierte Ansicht des Gemeinschaftspools vor zwei weißen und sandfarbenen Gebäuden mit gestaffelten Terrassen und Palmen',
  'Компьютерная визуализация общего бассейна перед двумя бело-песочными зданиями со ступенчатыми террасами и пальмами',
  'منظر مولَّد بالحاسوب للمسبح المشترك أمام مبنيين أبيض ورملي اللون بتراسات متدرجة وأشجار نخيل',
  'Computergegenereerd beeld van het gemeenschappelijke zwembad voor twee witte en zandkleurige gebouwen met trapsgewijze terrassen en palmbomen',
  'Wygenerowany komputerowo widok wspólnego basenu przed dwoma biało-piaskowymi budynkami z tarasami w układzie schodkowym i palmami',
  'Datagenerert bilde av fellesbassenget foran to hvite og sandfargede bygninger med trappede terrasser og palmer',
  'Datorgenererad bild av den gemensamma poolen framför två vita och sandfärgade byggnader med trappstegsformade terrasser och palmer')
p('.images.architecture.alt',  # 13
  'Vista generada por ordenador de un césped con tumbonas hacia la piscina y los edificios escalonados, con montañas al fondo',
  'Vue générée par ordinateur d’une pelouse avec des transats en direction de la piscine et des bâtiments en gradins, avec des montagnes en arrière-plan',
  'Computergenerierte Ansicht einer Rasenfläche mit Sonnenliegen in Richtung Pool und der gestaffelten Gebäude, mit Bergen im Hintergrund',
  'Компьютерная визуализация газона с шезлонгами, обращённого к бассейну и ступенчатым зданиям, с горами на заднем плане',
  'منظر مولَّد بالحاسوب لمرج به كراسي تشمّس باتجاه المسبح والمباني المتدرجة، والجبال في الخلفية',
  'Computergegenereerd beeld van een gazon met ligbedden richting het zwembad en de trapsgewijze gebouwen, met bergen op de achtergrond',
  'Wygenerowany komputerowo widok trawnika z leżakami w stronę basenu i schodkowych budynków, z górami w tle',
  'Datagenerert bilde av en plen med solsenger mot bassenget og de trappede bygningene, med fjell i bakgrunnen',
  'Datorgenererad bild av en gräsmatta med solstolar mot poolen och de trappstegsformade byggnaderna, med berg i bakgrunden')
p('.images.lifestyle.alt',  # 14
  'Vista generada por ordenador de una terraza con un sofá rinconero, sillones y una mesa de comedor, con colinas verdes al fondo',
  'Vue générée par ordinateur d’une terrasse avec un canapé d’angle, des fauteuils et une table à manger, avec des collines vertes au loin',
  'Computergenerierte Ansicht einer Terrasse mit Ecksofa, Sesseln und Esstisch, mit grünen Hügeln dahinter',
  'Компьютерная визуализация террасы с угловым диваном, креслами и обеденным столом, с зелёными холмами вдали',
  'منظر مولَّد بالحاسوب لتراس فيه أريكة زاوية ومقاعد وطاولة طعام، وتلال خضراء في الأفق',
  'Computergegenereerd beeld van een terras met een hoekbank, fauteuils en een eettafel, met groene heuvels op de achtergrond',
  'Wygenerowany komputerowo widok tarasu z narożną sofą, fotelami i stołem jadalnym, z zielonymi wzgórzami w tle',
  'Datagenerert bilde av en terrasse med hjørnesofa, lenestoler og spisebord, med grønne åser i bakgrunnen',
  'Datorgenererad bild av en terrass med hörnsoffa, fåtöljer och ett matbord, med gröna kullar i bakgrunden')
p('.images.privateViewing.alt',  # 15
  'Dormitorio generado por ordenador con una cama doble y una puerta corredera de cristal a una terraza',
  'Chambre générée par ordinateur avec un lit double et une porte coulissante vitrée donnant sur une terrasse',
  'Computergeneriertes Schlafzimmer mit Doppelbett und einer gläsernen Schiebetür zur Terrasse',
  'Компьютерная визуализация спальни с двуспальной кроватью и стеклянной раздвижной дверью на террасу',
  'غرفة نوم مولَّدة بالحاسوب بسرير مزدوج وباب زجاجي منزلق يؤدي إلى تراس',
  'Computergegenereerde slaapkamer met een tweepersoonsbed en een glazen schuifdeur naar een terras',
  'Wygenerowana komputerowo sypialnia z łóżkiem małżeńskim i szklanymi drzwiami przesuwnymi na taras',
  'Datagenerert soverom med dobbeltseng og en skyvedør i glass ut til en terrasse',
  'Datorgenererat sovrum med dubbelsäng och en glasskjutdörr ut mot en terrass')
p('.media.copy',  # 16
  'Vistas generadas por ordenador de los edificios, las terrazas y los interiores, y planos de las siete viviendas de la lista de precios.',
  'Vues générées par ordinateur des bâtiments, des terrasses et des intérieurs, et plans des sept logements de la liste de prix.',
  'Computergenerierte Ansichten der Gebäude, der Terrassen und der Innenräume sowie Grundrisse der sieben Wohnungen auf der Preisliste.',
  'Компьютерные визуализации зданий, террас и интерьеров, а также планировки семи квартир из прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمباني والتراسات والتصاميم الداخلية، ومخططات المساكن السبعة الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van de gebouwen, de terrassen en de interieurs, en plattegronden van de zeven woningen op de prijslijst.',
  'Wygenerowane komputerowo widoki budynków, tarasów i wnętrz oraz rzuty siedmiu lokali z cennika.',
  'Datagenererte bilder av bygningene, terrassene og interiørene, og plantegninger for de sju boligene på prislisten.',
  'Datorgenererade bilder av byggnaderna, terrasserna och interiörerna, samt planritningar för de sju bostäderna på prislistan.')
p('.media.note',  # 17
  'Todas las imágenes son generadas por ordenador, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los del promotor, en fase de proyecto, las superficies que figuran en ellos son aproximadas y están sujetas al proyecto definitivo, y los nombres de las estancias están en español.',
  'Toutes les images sont générées par ordinateur, et le mobilier et la décoration qui y figurent sont illustratifs et non inclus. Les plans sont ceux du promoteur au stade du projet, les surfaces qui y figurent sont approximatives et sous réserve du projet définitif, et les noms des pièces sont en espagnol.',
  'Alle Bilder sind computergenerierte Darstellungen; die gezeigten Möbel und die Dekoration dienen der Illustration und sind nicht enthalten. Die Grundrisse sind die Pläne des Bauträgers im Projektstadium, die darauf angegebenen Flächen sind ungefähr und vorbehaltlich des endgültigen Projekts, und die Raumbezeichnungen sind auf Spanisch.',
  'Все изображения — компьютерные визуализации; мебель и декор на них носят иллюстративный характер и в стоимость не входят. Планировки — это проектные планы застройщика, указанные на них площади приблизительны и зависят от окончательного проекта, а названия помещений даны на испанском языке.',
  'جميع الصور مولَّدة بالحاسوب، والأثاث والديكور الظاهران فيها توضيحيان وغير مشمولين. المخططات هي مخططات المطوّر في مرحلة المشروع، والمساحات الواردة فيها تقريبية وتخضع للمشروع النهائي، وأسماء الغرف عليها بالإسبانية.',
  'Alle beelden zijn computergegenereerd en het meubilair en de inrichting die erop te zien zijn, dienen ter illustratie en zijn niet inbegrepen. De plattegronden zijn de projectplannen van de ontwikkelaar, de oppervlakten erop zijn bij benadering en onder voorbehoud van het definitieve project, en de ruimtenamen zijn in het Spaans.',
  'Wszystkie zdjęcia są wizualizacjami komputerowymi, a meble i dekoracje na nich mają charakter ilustracyjny i nie są wliczone. Rzuty to plany projektowe dewelopera, podane na nich powierzchnie są przybliżone i zależą od ostatecznego projektu, a nazwy pomieszczeń są po hiszpańsku.',
  'Alle bildene er datagenererte, og møblene og dekorasjonen på dem er illustrasjoner og er ikke inkludert. Plantegningene er utbyggerens prosjektplaner, arealene på dem er omtrentlige og med forbehold om det endelige prosjektet, og romnavnene er på spansk.',
  'Alla bilder är datorgenererade, och möblerna och inredningen på dem är illustrativa och ingår inte. Planritningarna är exploatörens projektplaner, ytorna på dem är ungefärliga och med förbehåll för det slutliga projektet, och rumsnamnen är på spanska.')

p('.media.items[0].caption',  # 18
  'La piscina comunitaria y los edificios', 'La piscine commune et les bâtiments', 'Der Gemeinschaftspool und die Gebäude',
  'Общий бассейн и здания', 'المسبح المشترك والمباني', 'Het gemeenschappelijke zwembad en de gebouwen',
  'Wspólny basen i budynki', 'Fellesbassenget og bygningene', 'Den gemensamma poolen och byggnaderna')
p('.media.items[1].alt',  # 19
  'Vista generada por ordenador de la misma piscina y los mismos edificios al anochecer, con las terrazas iluminadas',
  'Vue générée par ordinateur de la même piscine et des mêmes bâtiments au crépuscule, avec les terrasses éclairées',
  'Computergenerierte Ansicht desselben Pools und derselben Gebäude in der Dämmerung mit beleuchteten Terrassen',
  'Компьютерная визуализация того же бассейна и зданий в сумерках, с освещёнными террасами',
  'منظر مولَّد بالحاسوب للمسبح والمباني نفسها عند الغروب مع تراسات مضاءة',
  'Computergegenereerd beeld van hetzelfde zwembad en dezelfde gebouwen in de schemering, met verlichte terrassen',
  'Wygenerowany komputerowo widok tego samego basenu i budynków o zmierzchu, z oświetlonymi tarasami',
  'Datagenerert bilde av det samme bassenget og de samme bygningene i skumringen, med opplyste terrasser',
  'Datorgenererad bild av samma pool och byggnader i skymningen, med upplysta terrasser')
p('.media.items[1].caption',  # 20
  'La piscina y los edificios al anochecer', 'La piscine et les bâtiments au crépuscule', 'Der Pool und die Gebäude in der Dämmerung',
  'Бассейн и здания в сумерках', 'المسبح والمباني عند الغروب', 'Het zwembad en de gebouwen in de schemering',
  'Basen i budynki o zmierzchu', 'Bassenget og bygningene i skumringen', 'Poolen och byggnaderna i skymningen')
p('.media.items[2].caption',  # 21
  'Los jardines comunitarios', 'Les jardins communs', 'Die Gemeinschaftsgärten',
  'Общие сады', 'الحدائق المشتركة', 'De gemeenschappelijke tuinen',
  'Ogrody wspólne', 'Felleshagene', 'De gemensamma trädgårdarna')
p('.media.items[3].alt',  # 22
  'Vista generada por ordenador de una vivienda en planta baja con césped, una terraza pavimentada y puertas correderas de cristal al salón y a un dormitorio',
  'Vue générée par ordinateur d’un logement en rez-de-chaussée avec pelouse, terrasse dallée et portes coulissantes vitrées vers le séjour et une chambre',
  'Computergenerierte Ansicht einer Erdgeschosswohnung mit Rasen, gepflasterter Terrasse und gläsernen Schiebetüren zu Wohnzimmer und Schlafzimmer',
  'Компьютерная визуализация квартиры на первом этаже с газоном, мощёной террасой и стеклянными раздвижными дверями в гостиную и спальню',
  'منظر مولَّد بالحاسوب لمسكن في الطابق الأرضي بمرج وتراس مبلّط وأبواب زجاجية منزلقة إلى غرفة المعيشة وغرفة نوم',
  'Computergegenereerd beeld van een woning op de begane grond met gazon, een betegeld terras en glazen schuifdeuren naar de woonkamer en een slaapkamer',
  'Wygenerowany komputerowo widok mieszkania na parterze z trawnikiem, wybrukowanym tarasem i szklanymi drzwiami przesuwnymi do salonu i sypialni',
  'Datagenerert bilde av en bolig i første etasje med plen, en flislagt terrasse og skyvedører i glass til stuen og et soverom',
  'Datorgenererad bild av en bostad i bottenvåningen med gräsmatta, en belagd terrass och glasskjutdörrar till vardagsrummet och ett sovrum')
p('.media.items[3].caption',  # 23
  'Una vivienda en planta baja y su jardín', 'Un logement en rez-de-chaussée et son jardin', 'Eine Erdgeschosswohnung und ihr Garten',
  'Квартира на первом этаже и её сад', 'مسكن في الطابق الأرضي وحديقته', 'Een woning op de begane grond en de bijbehorende tuin',
  'Mieszkanie na parterze i jego ogród', 'En bolig i første etasje og hagen til den', 'En bostad i bottenvåningen och dess trädgård')
p('.media.items[4].alt',  # 24
  'Vista generada por ordenador de una casa blanca de dos plantas con césped, una chimenea de jardín y una terraza cubierta',
  'Vue générée par ordinateur d’une maison blanche à deux niveaux avec pelouse, un brasero de jardin et une terrasse couverte',
  'Computergenerierte Ansicht eines weißen zweigeschossigen Hauses mit Rasen, einer Feuerstelle und einer überdachten Terrasse',
  'Компьютерная визуализация двухэтажного белого дома с газоном, садовым очагом и крытой террасой',
  'منظر مولَّد بالحاسوب لمنزل أبيض من طابقين بمرج ومدفأة حديقة وتراس مغطى',
  'Computergegenereerd beeld van een wit huis met twee verdiepingen, een gazon, een vuurplaats en een overdekt terras',
  'Wygenerowany komputerowo widok białego dwukondygnacyjnego domu z trawnikiem, paleniskiem ogrodowym i zadaszonym tarasem',
  'Datagenerert bilde av et hvitt hus i to etasjer med plen, et bålsted og en overbygd terrasse',
  'Datorgenererad bild av ett vitt tvåvåningshus med gräsmatta, en eldstad och en övertäckt terrass')
p('.media.items[4].caption',  # 25
  'Una casa adosada y su jardín', 'Une maison de ville et son jardin', 'Ein Reihenhaus und sein Garten',
  'Таунхаус и его сад', 'منزل متلاصق وحديقته', 'Een rijwoning en de bijbehorende tuin',
  'Dom szeregowy i jego ogród', 'Et rekkehus og hagen til det', 'Ett radhus och dess trädgård')
p('.media.items[5].alt',  # 26
  'Vista generada por ordenador de una larga terraza de planta alta con una zona de descanso y el mar en el horizonte',
  'Vue générée par ordinateur d’une longue terrasse d’étage avec un coin salon et la mer à l’horizon',
  'Computergenerierte Ansicht einer langen Terrasse im Obergeschoss mit Loungebereich und dem Meer am Horizont',
  'Компьютерная визуализация длинной террасы на верхнем этаже с зоной отдыха и морем на горизонте',
  'منظر مولَّد بالحاسوب لتراس طويل في طابق علوي بمنطقة جلوس والبحر في الأفق',
  'Computergegenereerd beeld van een lang terras op een hogere verdieping met een loungehoek en de zee aan de horizon',
  'Wygenerowany komputerowo widok długiego tarasu na wyższej kondygnacji ze strefą wypoczynkową i morzem na horyzoncie',
  'Datagenerert bilde av en lang terrasse i en øvre etasje med en loungekrok og havet i horisonten',
  'Datorgenererad bild av en lång terrass på en övre våning med en loungehörna och havet vid horisonten')
p('.media.items[5].caption',  # 27
  'Una terraza de planta alta con vistas al mar', 'Une terrasse d’étage avec vue sur la mer', 'Eine Terrasse im Obergeschoss mit Meerblick',
  'Терраса на верхнем этаже с видом на море', 'تراس في طابق علوي بإطلالة على البحر', 'Een terras op een hogere verdieping met zeezicht',
  'Taras na wyższej kondygnacji z widokiem na morze', 'En terrasse i en øvre etasje med havutsikt', 'En terrass på en övre våning med havsutsikt')
p('.media.items[6].caption',  # 28
  'Zona de estar y mesa de comedor en la terraza', 'Coin salon et table à manger sur la terrasse', 'Loungebereich und Esstisch auf der Terrasse',
  'Зона отдыха и обеденный стол на террасе', 'منطقة جلوس وطاولة طعام على التراس', 'Loungehoek en eettafel op het terras',
  'Strefa wypoczynkowa i stół jadalny na tarasie', 'Loungekrok og spisebord på terrassen', 'Loungehörna och matbord på terrassen')
p('.media.items[7].alt',  # 29
  'Vista generada por ordenador de una terraza con una larga mesa de comedor al anochecer y el mar en el horizonte',
  'Vue générée par ordinateur d’une terrasse avec une longue table à manger au crépuscule et la mer à l’horizon',
  'Computergenerierte Ansicht einer Terrasse mit langem Esstisch in der Dämmerung und dem Meer am Horizont',
  'Компьютерная визуализация террасы с длинным обеденным столом в сумерках и морем на горизонте',
  'منظر مولَّد بالحاسوب لتراس فيه طاولة طعام طويلة عند الغروب والبحر في الأفق',
  'Computergegenereerd beeld van een terras met een lange eettafel in de schemering en de zee aan de horizon',
  'Wygenerowany komputerowo widok tarasu z długim stołem jadalnym o zmierzchu i morzem na horyzoncie',
  'Datagenerert bilde av en terrasse med et langt spisebord i skumringen og havet i horisonten',
  'Datorgenererad bild av en terrass med ett långt matbord i skymningen och havet vid horisonten')
p('.media.items[7].caption',  # 30
  'Una terraza al anochecer', 'Une terrasse au crépuscule', 'Eine Terrasse in der Dämmerung',
  'Терраса в сумерках', 'تراس عند الغروب', 'Een terras in de schemering',
  'Taras o zmierzchu', 'En terrasse i skumringen', 'En terrass i skymningen')
p('.media.items[8].alt',  # 31
  'Salón generado por ordenador con un sofá, un puf azul, una pared de televisión revestida de madera y una puerta corredera a la terraza',
  'Séjour généré par ordinateur avec un canapé, un pouf bleu, un mur télévision habillé de bois et une porte coulissante vers la terrasse',
  'Computergeneriertes Wohnzimmer mit Sofa, blauem Pouf, holzverkleideter Fernsehwand und einer Schiebetür zur Terrasse',
  'Компьютерная визуализация гостиной с диваном, синим пуфом, деревянной панелью для телевизора и раздвижной дверью на террасу',
  'غرفة معيشة مولَّدة بالحاسوب بأريكة ومقعد أزرق دائري وجدار تلفاز مكسوّ بالخشب وباب منزلق إلى التراس',
  'Computergegenereerde woonkamer met een bank, een blauwe poef, een met hout beklede tv-wand en een schuifdeur naar het terras',
  'Wygenerowany komputerowo salon z sofą, niebieską pufą, drewnianą ścianą telewizyjną i drzwiami przesuwnymi na taras',
  'Datagenerert stue med sofa, en blå puff, en trekledd tv-vegg og en skyvedør ut til terrassen',
  'Datorgenererat vardagsrum med soffa, en blå puff, en träklädd tv-vägg och en skjutdörr ut mot terrassen')
p('.media.items[9].alt',  # 32
  'Cocina de planta abierta generada por ordenador con una barra de desayuno y una mesa de comedor de cristal',
  'Cuisine ouverte générée par ordinateur avec un bar de petit-déjeuner et une table à manger en verre',
  'Computergenerierte offene Küche mit Frühstückstresen und einem Esstisch aus Glas',
  'Компьютерная визуализация кухни открытой планировки с барной стойкой и стеклянным обеденным столом',
  'مطبخ مفتوح مولَّد بالحاسوب بكاونتر إفطار وطاولة طعام زجاجية',
  'Computergegenereerde open keuken met een ontbijtbar en een glazen eettafel',
  'Wygenerowana komputerowo kuchnia otwarta z barkiem śniadaniowym i szklanym stołem jadalnym',
  'Datagenerert åpent kjøkken med en frokostbar og et spisebord i glass',
  'Datorgenererat öppet kök med en frukostbar och ett matbord i glas')
p('.media.items[11].alt',  # 33
  'Dormitorio generado por ordenador con dos camas individuales y una puerta corredera de cristal a la terraza',
  'Chambre générée par ordinateur avec deux lits simples et une porte coulissante vitrée donnant sur la terrasse',
  'Computergeneriertes Schlafzimmer mit zwei Einzelbetten und einer gläsernen Schiebetür zur Terrasse',
  'Компьютерная визуализация спальни с двумя односпальными кроватями и стеклянной раздвижной дверью на террасу',
  'غرفة نوم مولَّدة بالحاسوب بسريرين مفردين وباب زجاجي منزلق إلى التراس',
  'Computergegenereerde slaapkamer met twee eenpersoonsbedden en een glazen schuifdeur naar het terras',
  'Wygenerowana komputerowo sypialnia z dwoma łóżkami pojedynczymi i szklanymi drzwiami przesuwnymi na taras',
  'Datagenerert soverom med to enkeltsenger og en skyvedør i glass ut til terrassen',
  'Datorgenererat sovrum med två enkelsängar och en glasskjutdörr ut mot terrassen')
p('.media.items[11].caption',  # 34
  'Dormitorio con dos camas individuales', 'Chambre avec deux lits simples', 'Schlafzimmer mit zwei Einzelbetten',
  'Спальня с двумя односпальными кроватями', 'غرفة نوم بسريرين مفردين', 'Slaapkamer met twee eenpersoonsbedden',
  'Sypialnia z dwoma łóżkami pojedynczymi', 'Soverom med to enkeltsenger', 'Sovrum med två enkelsängar')
p('.media.items[12].alt',  # 35
  'Baño generado por ordenador con un mueble de lavabo doble y una ducha revestida con baldosas de efecto mármol',
  'Salle de bains générée par ordinateur avec un meuble double vasque et une douche carrelée en effet marbre',
  'Computergeneriertes Badezimmer mit Doppelwaschtisch und einer Dusche mit Fliesen in Marmoroptik',
  'Компьютерная визуализация ванной комнаты с двойной раковиной и душем, отделанным плиткой под мрамор',
  'حمام مولَّد بالحاسوب بوحدة مغسلة مزدوجة ودوش مكسوّ ببلاط بمظهر الرخام',
  'Computergegenereerde badkamer met een dubbel wastafelmeubel en een douche betegeld in marmerlook',
  'Wygenerowana komputerowo łazienka z szafką z podwójną umywalką i prysznicem wyłożonym płytkami w stylu marmuru',
  'Datagenerert bad med en vaskeskap med to servanter og en dusj flislagt i marmorlook',
  'Datorgenererat badrum med en dubbel tvättställsskåpsenhet och en dusch med kakel i marmorlook')
p('.media.items[13].alt',  # 36
  'Baño generado por ordenador con un lavabo suspendido, un inodoro y una ducha revestida con baldosas de efecto mármol',
  'Salle de bains générée par ordinateur avec une vasque suspendue, des toilettes et une douche carrelée en effet marbre',
  'Computergeneriertes Badezimmer mit wandhängendem Waschbecken, WC und einer Dusche mit Fliesen in Marmoroptik',
  'Компьютерная визуализация ванной комнаты с подвесной раковиной, унитазом и душем, отделанным плиткой под мрамор',
  'حمام مولَّد بالحاسوب بمغسلة معلّقة ومرحاض ودوش مكسوّ ببلاط بمظهر الرخام',
  'Computergegenereerde badkamer met een hangende wastafel, een toilet en een douche betegeld in marmerlook',
  'Wygenerowana komputerowo łazienka z umywalką wiszącą, toaletą i prysznicem wyłożonym płytkami w stylu marmuru',
  'Datagenerert bad med en veggmontert servant, et toalett og en dusj flislagt i marmorlook',
  'Datorgenererat badrum med ett väggmonterat tvättställ, en toalett och en dusch med kakel i marmorlook')

# ---- overview, why, architecture ----------------------------------------------------------
p('.overview.headlineHtml',  # 51
  'Ochenta viviendas, <em>siete a la venta actualmente</em>',
  'Quatre-vingts logements, <em>sept actuellement annoncés</em>',
  'Achtzig Wohnungen, <em>sieben derzeit gelistet</em>',
  'Восемьдесят квартир, <em>семь сейчас в продаже</em>',
  'ثمانون مسكنًا، <em>سبعة منها معروضة حاليًا</em>',
  'Tachtig woningen, <em>zeven momenteel te koop</em>',
  'Osiemdziesiąt lokali, <em>siedem obecnie dostępnych</em>',
  'Åtti boliger, <em>sju annonsert nå</em>',
  'Åttio bostäder, <em>sju listade just nu</em>')
p('.overview.copy[0]',  # 52
  'Es una promoción de 80 viviendas de dos o tres dormitorios en Cancelada, en la Nueva Milla de Oro de Estepona, entre Estepona y Marbella. Los edificios tienen hasta cinco plantas e incluyen 10 apartamentos dúplex y 4 casas adosadas, con jardines en la planta baja y grandes terrazas en las plantas superiores.',
  'Il s’agit d’un programme de 80 logements de deux ou trois chambres à Cancelada, sur la Nouvelle Mille d’Or d’Estepona, entre Estepona et Marbella. Les bâtiments comptent jusqu’à cinq niveaux et comprennent 10 appartements duplex et 4 maisons de ville, avec des jardins au rez-de-chaussée et de grandes terrasses aux étages supérieurs.',
  'Es ist eine Anlage mit 80 Wohnungen mit zwei oder drei Schlafzimmern in Cancelada, an der Neuen Goldenen Meile von Estepona, zwischen Estepona und Marbella. Die Gebäude haben bis zu fünf Geschosse und umfassen 10 Maisonette-Apartments und 4 Reihenhäuser, mit Gärten im Erdgeschoss und großen Terrassen in den oberen Geschossen.',
  'Это комплекс из 80 квартир с двумя или тремя спальнями в Канселаде, на Новой Золотой миле Эстепоны, между Эстепоной и Марбельей. Здания имеют до пяти этажей и включают 10 дуплексов и 4 таунхауса, с садами на первом этаже и большими террасами на верхних этажах.',
  'هذا مشروع من 80 مسكنًا من غرفتي نوم أو ثلاث غرف نوم في كانسيلادا، على الميل الذهبي الجديد في إستيبونا، بين إستيبونا وماربيا. ترتفع المباني حتى خمسة طوابق وتضم 10 شقق دوبلكس و4 منازل متلاصقة، بحدائق في الطابق الأرضي وتراسات واسعة في الطوابق العليا.',
  'Dit is een project van 80 woningen met twee of drie slaapkamers in Cancelada, aan de Nieuwe Golden Mile van Estepona, tussen Estepona en Marbella. De gebouwen tellen tot vijf verdiepingen en omvatten 10 duplexappartementen en 4 rijwoningen, met tuinen op de begane grond en grote terrassen op de hogere verdiepingen.',
  'To inwestycja z 80 lokalami z dwiema lub trzema sypialniami w miejscowości Cancelada, na Nowej Złotej Mili w Esteponie, między Esteponą a Marbellą. Budynki mają do pięciu kondygnacji i obejmują 10 apartamentów dwupoziomowych oraz 4 domy szeregowe, z ogrodami na parterze i dużymi tarasami na wyższych kondygnacjach.',
  'Dette er et prosjekt med 80 boliger med to eller tre soverom i Cancelada, på Estepones Nye Golden Mile, mellom Estepona og Marbella. Byggene har opptil fem etasjer og omfatter 10 duplexleiligheter og 4 rekkehus, med hager i første etasje og store terrasser i de øvre etasjene.',
  'Det här är ett projekt med 80 bostäder med två eller tre sovrum i Cancelada, på Esteponas Nya Golden Mile, mellan Estepona och Marbella. Byggnaderna har upp till fem våningar och omfattar 10 etagelägenheter och 4 radhus, med trädgårdar i bottenvåningen och stora terrasser på de övre våningarna.')
p('.overview.copy[1]',  # 53
  'La lista de precios recoge siete de las 80 viviendas, todas en planta baja con jardín o grandes terrazas, y las muestra como disponibles. Cada una incluye un trastero y una o dos plazas de garaje. El anuncio del promotor da la entrega en abril de 2028.',
  'La liste de prix recense sept des 80 logements, tous au rez-de-chaussée avec jardin ou grandes terrasses, et les présente comme disponibles. Chacun comprend une cave et une ou deux places de garage. L’annonce du promoteur indique une livraison en avril 2028.',
  'Die Preisliste nennt sieben der 80 Wohnungen, alle im Erdgeschoss mit Garten oder großen Terrassen, und zeigt sie als verfügbar. Zu jeder gehören ein Abstellraum und ein oder zwei Garagenstellplätze. Der Bauträger gibt die Übergabe für April 2028 an.',
  'В прайс-листе указаны семь из 80 квартир, все на первом этаже с садом или большими террасами, и показаны как доступные. К каждой прилагаются кладовая и одно или два места в гараже. Застройщик указывает срок сдачи — апрель 2028 года.',
  'تدرج قائمة الأسعار سبعة من المساكن الثمانين، جميعها في الطابق الأرضي بحديقة أو تراسات واسعة، وتعرضها كمتاحة. ويرافق كل مسكن غرفة تخزين وموقف أو موقفا سيارة في المرآب. ويذكر إعلان المطوّر موعد التسليم في أبريل 2028.',
  'De prijslijst noemt zeven van de 80 woningen, allemaal op de begane grond met een tuin of grote terrassen, en toont ze als beschikbaar. Bij elke woning hoort een berging en een of twee garageplaatsen. De vermelding van de ontwikkelaar noemt april 2028 als opleveringsdatum.',
  'Cennik wymienia siedem z 80 lokali, wszystkie na parterze z ogrodem lub dużymi tarasami, i podaje je jako dostępne. Do każdego należy komórka lokatorska i jedno lub dwa miejsca w garażu. Deweloper podaje termin oddania na kwiecień 2028 r.',
  'Prislisten viser sju av de 80 boligene, alle i første etasje med hage eller store terrasser, og oppgir dem som tilgjengelige. Hver av dem har en bod og en eller to garasjeplasser. Utbyggeren oppgir overtakelse i april 2028.',
  'Prislistan upptar sju av de 80 bostäderna, alla i bottenvåningen med trädgård eller stora terrasser, och visar dem som tillgängliga. Varje bostad har ett förråd och en eller två garageplatser. Exploatören anger tillträde i april 2028.')
p('.overview.metrics[0][1]',  # 54
  '80 viviendas', '80 logements', '80 Wohnungen', '80 квартир', '80 مسكنًا', '80 woningen', '80 lokali', '80 boliger', '80 bostäder')
p('.overview.metrics[1][1]',  # 55
  '7 viviendas', '7 logements', '7 Wohnungen', '7 квартир', '7 مساكن', '7 woningen', '7 lokali', '7 boliger', '7 bostäder')
p('.why.copy',  # 56
  'Viviendas en planta baja con jardín o grandes terrazas, una plaza de garaje y un trastero, en una promoción con piscina, gimnasio y casa club.',
  'Logements en rez-de-chaussée avec jardin ou grandes terrasses, une place de garage et une cave, dans un programme avec piscine, salle de sport et club-house.',
  'Wohnungen im Erdgeschoss mit Garten oder großen Terrassen, einem Garagenstellplatz und einem Abstellraum, in einer Anlage mit Pool, Fitnessraum und Clubhaus.',
  'Квартиры на первом этаже с садом или большими террасами, местом в гараже и кладовой, в комплексе с бассейном, тренажёрным залом и клубным домом.',
  'مساكن في الطابق الأرضي بحديقة أو تراسات واسعة وموقف سيارة في المرآب وغرفة تخزين، ضمن مشروع فيه مسبح وصالة رياضية ونادي المجمع.',
  'Woningen op de begane grond met een tuin of grote terrassen, een garageplaats en een berging, in een project met zwembad, fitnessruimte en clubhuis.',
  'Mieszkania na parterze z ogrodem lub dużymi tarasami, miejscem w garażu i komórką lokatorską, w inwestycji z basenem, siłownią i klubem mieszkańców.',
  'Boliger i første etasje med hage eller store terrasser, en garasjeplass og en bod, i et prosjekt med basseng, treningsrom og klubbhus.',
  'Bostäder i bottenvåningen med trädgård eller stora terrasser, en garageplats och ett förråd, i ett projekt med pool, gym och klubbhus.')
p('.why.points[0][1]',  # 57
  'Compradores que quieren una vivienda a pie de calle con espacio exterior propio, como segunda residencia o para vivir todo el año, cerca de los campos de golf y del mar.',
  'Acheteurs qui souhaitent un logement de plain-pied avec un espace extérieur à eux, en résidence secondaire ou à l’année, près des golfs et de la mer.',
  'Käufer, die eine ebenerdige Wohnung mit eigenem Außenbereich suchen, als Zweitwohnsitz oder zum Wohnen das ganze Jahr, nahe den Golfplätzen und dem Meer.',
  'Покупатели, которым нужна квартира на уровне земли с собственным открытым пространством — как второе жильё или для постоянного проживания — рядом с полями для гольфа и морем.',
  'المشترون الذين يريدون مسكنًا في مستوى الأرض بمساحة خارجية خاصة، سواء كمسكن ثانٍ أو للإقامة طوال العام، قرب ملاعب الغولف والبحر.',
  'Kopers die een woning op de begane grond met eigen buitenruimte willen, als tweede woning of om het hele jaar in te wonen, dicht bij de golfbanen en de zee.',
  'Kupujący, którzy chcą mieszkania na parterze z własną przestrzenią zewnętrzną, jako drugi dom lub do mieszkania przez cały rok, w pobliżu pól golfowych i morza.',
  'Kjøpere som vil ha en bolig på bakkeplan med egen uteplass, som fritidsbolig eller til å bo i hele året, nær golfbanene og havet.',
  'Köpare som vill ha en bostad i marknivå med egen uteplats, som andra bostad eller för boende året runt, nära golfbanorna och havet.')
p('.why.points[1][1]',  # 58
  'Tres de las siete viviendas tienen jardín privado, de 42, 60 y 176 m², y las otras cuatro tienen terrazas de 47 a 71 m². Todas las viviendas de la lista tienen una plaza de garaje y un trastero.',
  'Trois des sept logements ont un jardin privé, de 42, 60 et 176 m², et les quatre autres ont des terrasses de 47 à 71 m². Tous les logements de la liste ont une place de garage et une cave.',
  'Drei der sieben Wohnungen haben einen privaten Garten mit 42, 60 und 176 m², die anderen vier Terrassen von 47 bis 71 m². Jede Wohnung auf der Liste hat einen Garagenstellplatz und einen Abstellraum.',
  'У трёх из семи квартир есть частный сад площадью 42, 60 и 176 м², у остальных четырёх — террасы от 47 до 71 м². У каждой квартиры из списка есть место в гараже и кладовая.',
  'ثلاثة من المساكن السبعة لها حديقة خاصة مساحتها 42 و60 و176 م²، وللأربعة الأخرى تراسات من 47 إلى 71 م². ولكل مسكن في القائمة موقف سيارة في المرآب وغرفة تخزين.',
  'Drie van de zeven woningen hebben een eigen tuin van 42, 60 en 176 m², en de andere vier hebben terrassen van 47 tot 71 m². Elke woning op de lijst heeft een garageplaats en een berging.',
  'Trzy z siedmiu lokali mają prywatny ogród o powierzchni 42, 60 i 176 m², a pozostałe cztery tarasy o powierzchni od 47 do 71 m². Każdy lokal z listy ma miejsce w garażu i komórkę lokatorską.',
  'Tre av de sju boligene har privat hage på 42, 60 og 176 m², og de fire andre har terrasser på 47 til 71 m². Alle boligene på listen har en garasjeplass og en bod.',
  'Tre av de sju bostäderna har en privat trädgård på 42, 60 och 176 m², och de andra fyra har terrasser på 47 till 71 m². Varje bostad på listan har en garageplats och ett förråd.')
p('.why.points[2][1]',  # 59
  'Cancelada es una zona residencial tranquila de la Nueva Milla de Oro, a 12 km de Estepona y de Puerto Banús y a 21 km de Marbella, con cuatro campos de golf cerca.',
  'Cancelada est un quartier résidentiel calme de la Nouvelle Mille d’Or, à 12 km d’Estepona et de Puerto Banús et à 21 km de Marbella, avec quatre golfs à proximité.',
  'Cancelada ist ein ruhiges Wohngebiet an der Neuen Goldenen Meile, 12 km von Estepona und Puerto Banús und 21 km von Marbella entfernt, mit vier Golfplätzen in der Nähe.',
  'Канселада — тихий жилой район на Новой Золотой миле, в 12 км от Эстепоны и Пуэрто-Банус и в 21 км от Марбельи, с четырьмя полями для гольфа поблизости.',
  'كانسيلادا منطقة سكنية هادئة على الميل الذهبي الجديد، على بعد 12 كم من إستيبونا وبويرتو بانوس و21 كم من ماربيا، وبالقرب منها أربعة ملاعب غولف.',
  'Cancelada is een rustige woonwijk aan de Nieuwe Golden Mile, op 12 km van Estepona en Puerto Banús en op 21 km van Marbella, met vier golfbanen in de buurt.',
  'Cancelada to spokojna dzielnica mieszkaniowa na Nowej Złotej Mili, 12 km od Estepony i Puerto Banús oraz 21 km od Marbelli, z czterema polami golfowymi w pobliżu.',
  'Cancelada er et rolig boligområde på Nye Golden Mile, 12 km fra Estepona og Puerto Banús og 21 km fra Marbella, med fire golfbaner i nærheten.',
  'Cancelada är ett lugnt bostadsområde på Nya Golden Mile, 12 km från Estepona och Puerto Banús och 21 km från Marbella, med fyra golfbanor i närheten.')
p('.why.points[3][1]',  # 60
  'La lista de precios cubre siete de las 80 viviendas y los documentos no dan el estado de la licencia ni de las obras, por lo que pedimos ambos antes de cualquier reserva.',
  'La liste de prix couvre sept des 80 logements et les documents ne donnent ni le statut du permis ni celui des travaux ; nous demandons donc les deux avant toute réservation.',
  'Die Preisliste deckt sieben der 80 Wohnungen ab und die Unterlagen nennen weder Genehmigungs- noch Baustand, daher fragen wir beides vor jeder Reservierung an.',
  'Прайс-лист охватывает семь из 80 квартир, а в документах нет сведений ни о разрешении, ни о ходе работ, поэтому до бронирования мы запрашиваем и то и другое.',
  'تغطي قائمة الأسعار سبعة من المساكن الثمانين ولا تذكر الوثائق حالة الرخصة ولا الأعمال، لذلك نطلب الاثنين قبل أي حجز.',
  'De prijslijst dekt zeven van de 80 woningen en de documenten vermelden geen stand van de vergunning of de werken, dus we vragen beide vóór elke reservering.',
  'Cennik obejmuje siedem z 80 lokali, a w dokumentach nie ma informacji o statusie pozwolenia ani prac, dlatego przed każdą rezerwacją pytamy o jedno i drugie.',
  'Prislisten dekker sju av de 80 boligene, og dokumentene oppgir verken status for tillatelsen eller for arbeidene, så vi ber om begge før en reservasjon.',
  'Prislistan omfattar sju av de 80 bostäderna och dokumenten anger varken status för bygglovet eller för arbetena, så vi ber om båda före varje reservation.')
p('.architecture.headlineHtml',  # 61
  'Edificios escalonados, <em>terrazas hacia la costa</em>',
  'Des bâtiments en gradins, <em>des terrasses tournées vers la côte</em>',
  'Gestaffelte Gebäude, <em>Terrassen zur Küste hin</em>',
  'Ступенчатые здания, <em>террасы, обращённые к побережью</em>',
  'مبانٍ متدرجة، <em>وتراسات تطل على الساحل</em>',
  'Trapsgewijze gebouwen, <em>terrassen op de kust gericht</em>',
  'Schodkowe budynki, <em>tarasy zwrócone ku wybrzeżu</em>',
  'Trappede bygninger, <em>terrasser vendt mot kysten</em>',
  'Trappstegsformade byggnader, <em>terrasser vända mot kusten</em>')
p('.architecture.copy[0]',  # 62
  'Los edificios descienden escalonados por la parcela, y el promotor indica que su disposición y orientación dan a las viviendas vistas despejadas a la sierra y a la costa, con privacidad respecto al entorno y vistas al mar en muchas de ellas. En las imágenes, los bordes de las terrazas son blancos y curvos sobre muros de color arena.',
  'Les bâtiments descendent en gradins le long de la parcelle, et le promoteur indique que leur disposition et leur orientation offrent aux logements une vue dégagée sur la sierra et la côte, avec de l’intimité par rapport à l’environnement et une vue sur la mer pour beaucoup. Sur les images, les rebords des terrasses sont blancs et incurvés au-dessus de murs couleur sable.',
  'Die Gebäude staffeln sich das Grundstück hinab, und der Bauträger gibt an, dass Anordnung und Ausrichtung den Wohnungen freie Sicht auf die Berge und die Küste verschaffen, mit Privatsphäre gegenüber der Umgebung und Meerblick für viele. Auf den Bildern sind die Terrassenkanten weiß und geschwungen über sandfarbenen Wänden.',
  'Здания спускаются уступами по участку, и застройщик указывает, что их расположение и ориентация дают квартирам открытый вид на горы и побережье, уединённость по отношению к окружению и вид на море у многих из них. На визуализациях края террас белые и изогнутые, над стенами песочного цвета.',
  'تنحدر المباني متدرجة على امتداد الأرض، ويذكر المطوّر أن تخطيطها واتجاهها يمنحان المساكن إطلالة مفتوحة على الجبال والساحل، مع خصوصية عن المحيط وإطلالة على البحر لكثير منها. وفي الصور تظهر حواف التراسات بيضاء ومنحنية فوق جدران بلون الرمل.',
  'De gebouwen volgen het perceel in treden naar beneden, en de ontwikkelaar geeft aan dat de indeling en de oriëntatie de woningen vrij zicht op de bergen en de kust geven, met privacy ten opzichte van de omgeving en zeezicht voor veel woningen. Op de beelden zijn de terrasranden wit en gebogen boven zandkleurige muren.',
  'Budynki schodzą schodkowo po działce, a deweloper podaje, że ich układ i orientacja zapewniają lokalom otwarty widok na góry i wybrzeże, prywatność wobec otoczenia, a wielu z nich widok na morze. Na wizualizacjach krawędzie tarasów są białe i zaokrąglone nad piaskowymi ścianami.',
  'Byggene trapper seg nedover tomten, og utbyggeren oppgir at plassering og orientering gir boligene fri utsikt mot fjellene og kysten, med privatliv i forhold til omgivelsene og havutsikt for mange. På bildene er terrassekantene hvite og buede over sandfargede vegger.',
  'Byggnaderna trappar sig nedför tomten, och exploatören anger att placeringen och orienteringen ger bostäderna fri utsikt mot bergen och kusten, med avskildhet från omgivningen och havsutsikt för många. På bilderna är terrasskanterna vita och böjda över sandfärgade väggar.')
p('.architecture.copy[1]',  # 63
  'En la planta baja las viviendas se abren a un jardín o a una gran terraza. Las plantas superiores tienen terrazas aún mayores, y los áticos, un solárium.',
  'Au rez-de-chaussée, les logements s’ouvrent sur un jardin ou une grande terrasse. Les étages supérieurs ont des terrasses plus grandes encore, et les penthouses un solarium.',
  'Im Erdgeschoss öffnen sich die Wohnungen zu einem Garten oder einer großen Terrasse. Die oberen Geschosse haben noch größere Terrassen, die Penthäuser ein Solarium.',
  'На первом этаже квартиры выходят в сад или на большую террасу. На верхних этажах террасы ещё больше, а у пентхаусов есть солярий.',
  'في الطابق الأرضي تُفتح المساكن على حديقة أو تراس واسع. وفي الطوابق العليا تراسات أوسع، وللبنتهاوس سولاريوم.',
  'Op de begane grond openen de woningen zich naar een tuin of een groot terras. De hogere verdiepingen hebben nog grotere terrassen, en de penthouses een solarium.',
  'Na parterze mieszkania otwierają się na ogród lub duży taras. Wyższe kondygnacje mają jeszcze większe tarasy, a penthouse’y solarium.',
  'I første etasje åpner boligene seg mot en hage eller en stor terrasse. De øvre etasjene har enda større terrasser, og toppleilighetene har solterrasse.',
  'I bottenvåningen öppnar sig bostäderna mot en trädgård eller en stor terrass. De övre våningarna har ännu större terrasser, och takvåningarna har en solterrass.')
p('.architecture.highlights[0][1]',  # 64
  'Cimentación y estructura de hormigón armado.', 'Fondations et structure en béton armé.', 'Fundament und Tragwerk aus Stahlbeton.',
  'Фундамент и несущий каркас из железобетона.', 'أساسات وهيكل من الخرسانة المسلحة.', 'Fundering en draagstructuur in gewapend beton.',
  'Fundamenty i konstrukcja z żelbetu.', 'Fundamenter og bærekonstruksjon i armert betong.', 'Grund och stomme i armerad betong.')
p('.architecture.highlights[1][1]',  # 65
  'Fábrica de ladrillo cerámico con revestimiento continuo y pintura blanca, cámara de aire, aislamiento térmico y trasdosado de yeso laminado por el interior.',
  'Maçonnerie en brique céramique avec enduit continu et peinture blanche, lame d’air, isolation thermique et doublage en plaques de plâtre à l’intérieur.',
  'Mauerwerk aus Hochlochziegeln mit durchgehendem Putz und weißem Anstrich, Luftschicht, Wärmedämmung und einer Gipskartonverkleidung innen.',
  'Кладка из керамического кирпича с сплошной штукатуркой и белой краской, воздушной прослойкой, теплоизоляцией и внутренней обшивкой из гипсокартона.',
  'طوب خزفي بطلاء متصل ودهان أبيض، مع فجوة هوائية وعزل حراري وتبطين داخلي بألواح الجبس.',
  'Metselwerk van keramische baksteen met doorlopende bepleistering en witte verf, een spouw, thermische isolatie en een gipsplaatbekleding aan de binnenzijde.',
  'Mur z cegły ceramicznej z ciągłym tynkiem i białą farbą, szczeliną powietrzną, izolacją termiczną i okładziną z płyt gipsowo-kartonowych od wewnątrz.',
  'Murverk av keramisk murstein med sammenhengende puss og hvit maling, luftspalte, varmeisolasjon og en innvendig kledning av gipsplater.',
  'Murverk av keramiktegel med genomgående puts och vit färg, luftspalt, värmeisolering och en invändig klädsel av gipsskivor.')
p('.architecture.highlights[2][1]',  # 66
  'Carpintería de aluminio con rotura de puente térmico y doble acristalamiento termoacústico, con persianas de aluminio aisladas en los dormitorios.',
  'Menuiseries en aluminium à rupture de pont thermique et double vitrage thermo-acoustique, avec des volets roulants en aluminium isolés dans les chambres.',
  'Aluminiumrahmen mit thermischer Trennung und wärme- und schalldämmender Doppelverglasung, mit gedämmten Aluminium-Rollläden in den Schlafzimmern.',
  'Алюминиевые рамы с терморазрывом и тепло- и звукоизолирующими двойными стеклопакетами, с утеплёнными алюминиевыми рольставнями в спальнях.',
  'إطارات من الألومنيوم بقاطع حراري وزجاج مزدوج عازل للحرارة والصوت، مع ستائر ألومنيوم معزولة في غرف النوم.',
  'Aluminium kozijnen met thermische onderbreking en thermisch-akoestische dubbele beglazing, met geïsoleerde aluminium rolluiken in de slaapkamers.',
  'Ramy aluminiowe z przerwą termiczną i termoakustycznym podwójnym szkleniem, z izolowanymi roletami aluminiowymi w sypialniach.',
  'Aluminiumsrammer med termisk brudd og termoakustisk dobbeltglass, med isolerte rullegardiner i aluminium på soverommene.',
  'Aluminiumbågar med köldbrygga och termoakustiskt dubbelglas, med isolerade aluminiumpersienner i sovrummen.')
p('.architecture.highlights[3][1]',  # 67
  'Terrazas privadas solados con gres de exterior y cubiertas técnicas no transitables, con aislamiento térmico y acabado de grava.',
  'Terrasses privatives revêtues de grès cérame d’extérieur et toitures techniques non accessibles, avec isolation thermique et finition en gravier.',
  'Private Terrassen mit Feinsteinzeug für den Außenbereich und nicht begehbare Technikdächer mit Wärmedämmung und Kiesabdeckung.',
  'Частные террасы, выложенные уличным керамогранитом, и неэксплуатируемые технические кровли с теплоизоляцией и гравийной засыпкой.',
  'تراسات خاصة مكسوة ببلاط خزفي للخارج وأسطح فنية غير قابلة للاستعمال بعزل حراري وطبقة حصى.',
  'Privéterrassen betegeld met buitengres en niet-betreedbare technische daken met thermische isolatie en een grindafwerking.',
  'Prywatne tarasy wyłożone gresem zewnętrznym oraz niedostępne dachy techniczne z izolacją termiczną i warstwą żwiru.',
  'Private terrasser belagt med utendørs steingods og tekniske tak som ikke er tilgjengelige, med varmeisolasjon og grusbelegg.',
  'Privata terrasser belagda med utomhusgrés och tekniska tak som inte är åtkomliga, med värmeisolering och ett grusskikt.')

# ---- quality specification ----------------------------------------------------------------
p('.qualitySpecs.sourceNote',  # 68
  'Fuente: la memoria de calidades del promotor, que no lleva fecha ni versión. Indica que no es vinculante contractualmente y que puede modificarse por exigencias técnicas, jurídicas o administrativas sin reducir el nivel general de calidades, y que las imágenes, el mobiliario, la jardinería y los electrodomésticos mostrados son meramente orientativos.',
  'Source : le descriptif technique du promoteur, qui ne porte ni date ni version. Il précise qu’il n’a pas valeur contractuelle et qu’il peut être modifié pour des raisons techniques, juridiques ou administratives sans abaisser le niveau général de qualité, et que les images, le mobilier, les aménagements paysagers et les appareils ménagers présentés sont donnés à titre indicatif.',
  'Quelle: die Baubeschreibung des Bauträgers, die weder Datum noch Version trägt. Sie gibt an, dass sie vertraglich nicht bindend ist und aus technischen, rechtlichen oder behördlichen Gründen geändert werden kann, ohne das allgemeine Qualitätsniveau zu senken, und dass die gezeigten Bilder, Möbel, Gartengestaltung und Geräte nur zur Orientierung dienen.',
  'Источник: спецификация материалов застройщика, в которой нет ни даты, ни номера версии. В ней сказано, что она не имеет договорной силы и может изменяться по техническим, юридическим или административным причинам без снижения общего уровня качества, а изображения, мебель, озеленение и техника на них носят ориентировочный характер.',
  'المصدر: مواصفات الجودة لدى المطوّر، وهي غير مؤرخة وبلا رقم إصدار. وتذكر أنها غير ملزمة تعاقديًا وأنه يجوز تعديلها لأسباب فنية أو قانونية أو إدارية دون خفض المستوى العام للجودة، وأن الصور والأثاث والتنسيق الحدائقي والأجهزة المعروضة استرشادية فقط.',
  'Bron: de kwaliteitsspecificatie van de ontwikkelaar, die geen datum of versienummer draagt. Daarin staat dat ze contractueel niet bindend is en om technische, juridische of administratieve redenen kan worden gewijzigd zonder het algemene kwaliteitsniveau te verlagen, en dat de getoonde beelden, het meubilair, de tuinaanleg en de apparatuur slechts ter oriëntatie dienen.',
  'Źródło: specyfikacja jakości dewelopera, która nie ma daty ani numeru wersji. Zastrzega, że nie ma mocy wiążącej umownie i może być zmieniona z powodów technicznych, prawnych lub administracyjnych bez obniżenia ogólnego poziomu jakości, a pokazane obrazy, meble, zieleń i sprzęty mają charakter orientacyjny.',
  'Kilde: utbyggerens kvalitetsspesifikasjon, som verken har dato eller versjon. Den sier at den ikke er kontraktsmessig bindende og kan endres av tekniske, juridiske eller administrative grunner uten å senke det generelle kvalitetsnivået, og at bildene, møblene, hageanlegget og hvitevarene som vises kun er veiledende.',
  'Källa: exploatörens kvalitetsspecifikation, som varken har datum eller version. Den anger att den inte är avtalsmässigt bindande och kan ändras av tekniska, juridiska eller administrativa skäl utan att den allmänna kvalitetsnivån sänks, och att bilderna, möblerna, trädgårdsutformningen och hushållsapparaterna som visas bara är vägledande.')
p('.qualitySpecs.groups[0].items[0]',  # 69
  'Gres porcelánico rectificado de 75 x 75 cm en blanco, con el marfil como opción, en toda la vivienda, y gres de exterior en las terrazas.',
  'Grès cérame rectifié 75 x 75 cm en blanc, avec l’ivoire en option, dans tout le logement, et grès d’extérieur sur les terrasses.',
  'Rektifizierte Feinsteinzeugfliesen, 75 x 75 cm, in Weiß, wahlweise in Elfenbein, in der ganzen Wohnung und Feinsteinzeug für den Außenbereich auf den Terrassen.',
  'Ректифицированный керамогранит 75 x 75 см белого цвета, по выбору — цвета слоновой кости, во всей квартире и уличный керамогранит на террасах.',
  'بلاط بورسلان مصحَّح الحواف مقاس 75 × 75 سم باللون الأبيض، مع العاجي كخيار، في المسكن كله، وبلاط خزفي للخارج على التراسات.',
  'Gerectificeerde porseleintegels van 75 x 75 cm in wit, met ivoor als optie, in de hele woning, en buitengres op de terrassen.',
  'Gres porcelanowy rektyfikowany 75 x 75 cm w kolorze białym, opcjonalnie kość słoniowa, w całym lokalu oraz gres zewnętrzny na tarasach.',
  'Rektifiserte porselensfliser på 75 x 75 cm i hvitt, med elfenben som tilvalg, i hele boligen, og utendørs steingods på terrassene.',
  'Rektifierat porslinsgrés på 75 x 75 cm i vitt, med elfenben som tillval, i hela bostaden, och utomhusgrés på terrasserna.')
p('.qualitySpecs.groups[0].items[1]',  # 70
  'Paredes de baño alicatadas con gres porcelánico de 40 x 120 cm en blanco mate, con blanco o marfil como opciones, en la zona de ducha y baño, y pintura plástica en el resto de las paredes.',
  'Murs de salle de bains carrelés en grès cérame 40 x 120 cm blanc mat, avec blanc ou ivoire en option, dans la zone de douche et de bain, et peinture plastique sur les autres murs.',
  'Badezimmerwände mit Feinsteinzeug, 40 x 120 cm, in Mattweiß, wahlweise in Weiß oder Elfenbein, im Dusch- und Badbereich gefliest, übrige Wände mit Kunststoffdispersionsfarbe.',
  'Стены ванных комнат в зоне душа и ванны облицованы керамогранитом 40 x 120 см матового белого цвета, по выбору — белого или цвета слоновой кости, остальные стены окрашены краской.',
  'جدران الحمامات مكسوة ببلاط بورسلان مقاس 40 × 120 سم باللون الأبيض غير اللامع، مع الأبيض أو العاجي كخيارين، في منطقة الدوش والاستحمام، ودهان بلاستيكي على بقية الجدران.',
  'Badkamerwanden in de douche- en badzone betegeld met porseleintegels van 40 x 120 cm in mat wit, met wit of ivoor als opties, en kunststofverf op de overige wanden.',
  'Ściany łazienek w strefie prysznica i wanny wyłożone gresem 40 x 120 cm w kolorze matowej bieli, opcjonalnie biel lub kość słoniowa, a pozostałe ściany pomalowane farbą plastyczną.',
  'Baderomsvegger flislagt med porselensfliser på 40 x 120 cm i matt hvitt, med hvitt eller elfenben som tilvalg, i dusj- og badeområdet, og plastmaling på de øvrige veggene.',
  'Badrumsväggar kaklade med porslinsgrés på 40 x 120 cm i matt vitt, med vitt eller elfenben som tillval, i dusch- och badområdet, och plastfärg på övriga väggar.')
p('.qualitySpecs.groups[0].items[2]',  # 71
  'Falsos techos de yeso laminado con registros para las unidades de climatización y ventilación, pintados lisos.',
  'Faux plafonds en plaques de plâtre avec trappes d’accès pour les unités de climatisation et de ventilation, peints lisses.',
  'Abgehängte Gipskartondecken mit Revisionsöffnungen für die Klima- und Lüftungsgeräte, glatt gestrichen.',
  'Подвесные потолки из гипсокартона с ревизионными люками для климатических и вентиляционных блоков, гладко окрашенные.',
  'أسقف مستعارة من ألواح الجبس بفتحات صيانة لوحدات التكييف والتهوية، مدهونة بشكل أملس.',
  'Verlaagde plafonds van gipsplaat met toegangsluiken voor de airco- en ventilatie-eenheden, glad geschilderd.',
  'Sufity podwieszane z płyt gipsowo-kartonowych z rewizjami dla jednostek klimatyzacji i wentylacji, gładko malowane.',
  'Nedforede himlinger i gips med inspeksjonsluker for klima- og ventilasjonsenhetene, malt glatt.',
  'Undertak av gipsskivor med inspektionsluckor för klimat- och ventilationsenheterna, målade släta.')
p('.qualitySpecs.groups[1].items[0]',  # 72
  'Puerta de entrada blindada con cerradura de seguridad, puertas de paso lisas lacadas en blanco y armarios modulares forrados por dentro con maletero y barra para colgar.',
  'Porte d’entrée blindée avec serrure de sécurité, portes intérieures lisses laquées en blanc et placards modulaires doublés à l’intérieur avec étagère à valises et barre de penderie.',
  'Eine gepanzerte Wohnungseingangstür mit Sicherheitsschloss, glatte weiß lackierte Innentüren und modulare, innen ausgekleidete Einbauschränke mit Gepäckablage und Kleiderstange.',
  'Бронированная входная дверь с замком безопасности, гладкие межкомнатные двери, лакированные в белый цвет, и модульные шкафы с отделкой внутри, антресолью для чемоданов и штангой для одежды.',
  'باب دخول مصفَّح بقفل أمان، وأبواب داخلية ملساء مطلية بالورنيش الأبيض، وخزائن ملابس مفصلية مبطَّنة من الداخل برف للحقائب وعمود تعليق.',
  'Een gepantserde voordeur met veiligheidsslot, gladde wit gelakte binnendeuren en modulaire kledingkasten met inwendige bekleding, een bagageplank en een kledingroede.',
  'Drzwi wejściowe antywłamaniowe z zamkiem bezpieczeństwa, gładkie drzwi wewnętrzne lakierowane na biało oraz modułowe szafy wyłożone od środka, z półką na walizki i drążkiem na ubrania.',
  'En pansret inngangsdør med sikkerhetslås, glatte innvendige dører lakkert hvite og modulgarderober kledd innvendig med kofferthylle og kleshenger.',
  'En pansrad ytterdörr med säkerhetslås, släta vitlackerade innerdörrar och modulgarderober klädda invändigt med resväskehylla och klädstång.')
p('.qualitySpecs.groups[2].items[0]',  # 73
  'Cocina amueblada con encimera de cuarzo o porcelánico, equipada con electrodomésticos.',
  'Cuisine équipée avec plan de travail en quartz ou en grès cérame, dotée d’appareils électroménagers.',
  'Einbauküche mit Arbeitsplatte aus Quarz oder Feinsteinzeug, mit Elektrogeräten ausgestattet.',
  'Меблированная кухня со столешницей из кварца или керамогранита, оснащённая бытовой техникой.',
  'مطبخ مجهّز بسطح عمل من الكوارتز أو البورسلان ومزوّد بالأجهزة الكهربائية.',
  'Ingerichte keuken met een werkblad van kwarts of porselein, uitgerust met elektrische apparaten.',
  'Kuchnia z blatem kwarcowym lub z gresu, wyposażona w sprzęt AGD.',
  'Møblert kjøkken med benkeplate i kvarts eller porselen, utstyrt med hvitevarer.',
  'Möblerat kök med bänkskiva i kvarts eller porslin, utrustat med hushållsapparater.')
p('.qualitySpecs.groups[3].items[0]',  # 74
  'Sanitarios de porcelana vitrificada, mueble de lavabo de doble seno en el baño principal y lavabo suspendido en el segundo, grifos monomando con grifería termostática en la ducha y espejo sobre cada lavabo.',
  'Sanitaires en porcelaine vitrifiée, meuble double vasque dans la salle de bains principale et vasque suspendue dans la seconde, mitigeurs avec robinetterie thermostatique à la douche et miroir au-dessus de chaque vasque.',
  'Sanitärkeramik aus Porzellan, Doppelwaschtischmöbel im Hauptbad und wandhängendes Waschbecken im zweiten Bad, Einhebelmischer mit Thermostatarmatur in der Dusche und ein Spiegel über jedem Waschbecken.',
  'Сантехника из витрифицированного фарфора, тумба с двойной раковиной в главной ванной и подвесная раковина во второй, смесители с термостатом в душе и зеркало над каждой раковиной.',
  'أدوات صحية من البورسلان الزجاجي، ووحدة مغسلة بحوضين في الحمام الرئيسي ومغسلة معلّقة في الثاني، وخلاطات مع خلاط حراري في الدوش، ومرآة فوق كل مغسلة.',
  'Sanitair van verglaasd porselein, een wastafelmeubel met dubbele wasbak in de hoofdbadkamer en een hangende wastafel in de tweede, mengkranen met thermostatische kraan in de douche en een spiegel boven elke wastafel.',
  'Ceramika sanitarna z porcelany witryfikowanej, szafka z podwójną umywalką w łazience głównej i umywalka wisząca w drugiej, baterie jednouchwytowe z termostatem w prysznicu oraz lustro nad każdą umywalką.',
  'Sanitærutstyr i vitrifisert porselen, vaskeskap med dobbel servant på hovedbadet og veggmontert servant på det andre, blandebatterier med termostatbatteri i dusjen og et speil over hver servant.',
  'Sanitetsporslin av vitrifierat porslin, ett tvättställsskåp med dubbla handfat i huvudbadrummet och ett väggmonterat handfat i det andra, blandare med termostatblandare i duschen och en spegel ovanför varje handfat.')
p('.qualitySpecs.groups[4].items[0]',  # 75
  'Un sistema de aire acondicionado con bomba de calor para refrigeración y calefacción, con conductos por el falso techo y la unidad exterior en la cubierta técnica, y agua caliente de un sistema de aerotermia individual.',
  'Un système de climatisation par pompe à chaleur pour le froid et le chaud, avec gaines dans le faux plafond et l’unité extérieure sur la toiture technique, et l’eau chaude produite par un système aérothermique individuel.',
  'Eine Wärmepumpen-Klimaanlage zum Kühlen und Heizen mit Kanälen in der abgehängten Decke und dem Außengerät auf dem Technikdach sowie Warmwasser aus einer individuellen Luft-Wasser-Wärmepumpe.',
  'Система кондиционирования с тепловым насосом для охлаждения и отопления, с воздуховодами в подвесном потолке и наружным блоком на технической кровле, а горячая вода — от индивидуальной аэротермической системы.',
  'نظام تكييف بمضخة حرارية للتبريد والتدفئة، بمجارٍ داخل السقف المستعار ووحدة خارجية على السطح الفني، وماء ساخن من نظام الطاقة الهوائية الحرارية الفردي.',
  'Een airconditioningsysteem met warmtepomp voor koeling en verwarming, met kanalen in het verlaagde plafond en de buitenunit op het technische dak, en warm water van een individueel aerothermisch systeem.',
  'System klimatyzacji z pompą ciepła do chłodzenia i ogrzewania, z kanałami w suficie podwieszanym i jednostką zewnętrzną na dachu technicznym, oraz ciepła woda z indywidualnego systemu aerotermicznego.',
  'Et klimaanlegg med varmepumpe for kjøling og oppvarming, med kanaler i det nedforede taket og utedelen på det tekniske taket, og varmtvann fra et individuelt aerotermisk system.',
  'Ett luftkonditioneringssystem med värmepump för kylning och värme, med kanaler i undertaket och utomhusenheten på det tekniska taket, och varmvatten från ett individuellt aerotermiskt system.')
p('.qualitySpecs.groups[4].items[1]',  # 76
  'Renovación controlada del aire, con bocas de extracción en los baños y las cocinas.',
  'Renouvellement d’air contrôlé, avec bouches d’extraction dans les salles de bains et les cuisines.',
  'Kontrollierte Raumlufterneuerung mit Absaugöffnungen in Bädern und Küchen.',
  'Контролируемая вентиляция с вытяжными решётками в ванных комнатах и на кухнях.',
  'تجديد مضبوط للهواء، مع فتحات شفط في الحمامات والمطابخ.',
  'Gecontroleerde luchtverversing, met afzuigpunten in de badkamers en keukens.',
  'Kontrolowana wymiana powietrza, z kratkami wyciągowymi w łazienkach i kuchniach.',
  'Kontrollert luftutskifting, med avtrekk på badene og i kjøkkenene.',
  'Kontrollerad luftväxling, med frånluftsdon i badrum och kök.')
p('.qualitySpecs.groups[4].items[2]',  # 77
  'El dossier otorga a las viviendas la calificación más alta, A, tanto en consumo de energía primaria no renovable como en emisiones de dióxido de carbono.',
  'La brochure attribue aux logements la meilleure note, A, tant pour la consommation d’énergie primaire non renouvelable que pour les émissions de dioxyde de carbone.',
  'Die Broschüre gibt den Wohnungen die höchste Bewertung, A, sowohl beim nicht erneuerbaren Primärenergieverbrauch als auch bei den Kohlendioxidemissionen.',
  'В брошюре квартирам присвоен наивысший класс A как по потреблению невозобновляемой первичной энергии, так и по выбросам углекислого газа.',
  'تمنح النشرة المساكن أعلى تصنيف، A، سواء في استهلاك الطاقة الأولية غير المتجددة أو في انبعاثات ثاني أكسيد الكربون.',
  'De brochure geeft de woningen de hoogste klasse, A, zowel voor het niet-hernieuwbare primaire energieverbruik als voor de koolstofdioxide-uitstoot.',
  'Broszura przypisuje lokalom najwyższą klasę, A, zarówno pod względem zużycia nieodnawialnej energii pierwotnej, jak i emisji dwutlenku węgla.',
  'Brosjyren gir boligene den høyeste klassen, A, både for forbruk av ikke-fornybar primærenergi og for utslipp av karbondioksid.',
  'Broschyren ger bostäderna den högsta klassen, A, både för förbrukning av icke förnybar primärenergi och för koldioxidutsläpp.')
p('.qualitySpecs.groups[5].items[0]',  # 78
  'Instalación eléctrica conforme al reglamento de baja tensión con un alto grado de electrificación, tomas de televisión, teléfono y telecomunicaciones en el salón y los dormitorios, y videoportero en color.',
  'Installation électrique conforme à la réglementation basse tension avec un haut degré d’électrification, prises de télévision, de téléphone et de télécommunications dans le séjour et les chambres, et visiophone couleur.',
  'Elektroinstallation nach der Niederspannungsverordnung mit hohem Elektrifizierungsgrad, Fernseh-, Telefon- und Telekommunikationsanschlüsse im Wohnzimmer und in den Schlafzimmern sowie eine Farb-Videosprechanlage.',
  'Электропроводка по правилам для низкого напряжения с высокой степенью электрификации, розетки для телевидения, телефона и связи в гостиной и спальнях и цветной видеодомофон.',
  'تمديدات كهربائية وفق لائحة الجهد المنخفض بدرجة كهربة عالية، ومقابس التلفاز والهاتف والاتصالات في غرفة المعيشة وغرف النوم، وجهاز اتصال مرئي ملوّن.',
  'Een elektrische installatie volgens het laagspanningsreglement met een hoge graad van elektrificatie, tv-, telefoon- en telecommunicatieaansluitingen in de woonkamer en de slaapkamers, en een kleurenvideofoon.',
  'Instalacja elektryczna zgodna z przepisami niskiego napięcia o wysokim stopniu elektryfikacji, gniazda telewizyjne, telefoniczne i telekomunikacyjne w salonie i sypialniach oraz wideodomofon kolorowy.',
  'Elektrisk anlegg etter lavspenningsforskriften med høy elektrifiseringsgrad, TV-, telefon- og telekommunikasjonsuttak i stuen og på soverommene, og fargevideosamtaleanlegg.',
  'Elinstallation enligt lågspänningsreglerna med hög elektrifieringsgrad, tv-, telefon- och teleuttag i vardagsrummet och sovrummen, och en färgvideoporttelefon.')
p('.qualitySpecs.groups[6].items[0]',  # 79
  'Una piscina comunitaria, un gimnasio equipado comunitario, una zona deportiva exterior y una zona zen, y amplios jardines diseñados para un bajo consumo de agua, con riego automático y áreas para pasear y descansar.',
  'Une piscine commune, une salle de sport équipée commune, un espace sportif extérieur et un espace zen, et de grands jardins conçus pour une faible consommation d’eau, avec arrosage automatique et espaces de promenade et de repos.',
  'Ein Gemeinschaftspool, ein ausgestatteter Gemeinschaftsfitnessraum, ein Sportbereich im Freien und ein Zen-Bereich sowie große, auf geringen Wasserverbrauch ausgelegte Gärten mit automatischer Bewässerung und Geh- und Ruhebereichen.',
  'Общий бассейн, оборудованный общий тренажёрный зал, спортивная площадка на открытом воздухе и зона дзен, а также большие сады с низким потреблением воды, с автоматическим поливом и зонами для прогулок и отдыха.',
  'مسبح مشترك وصالة رياضية مجهزة للاستخدام المشترك ومنطقة رياضية خارجية ومنطقة زِن، وحدائق واسعة مصممة لقلة استهلاك المياه، مع ري آلي ومناطق للمشي والاستراحة.',
  'Een gemeenschappelijk zwembad, een uitgeruste gemeenschappelijke fitnessruimte, een sportzone buiten en een zenzone, en grote tuinen die ontworpen zijn voor een laag waterverbruik, met automatische besproeiing en wandel- en rustzones.',
  'Wspólny basen, wyposażona siłownia dla mieszkańców, zewnętrzna strefa sportowa i strefa zen oraz duże ogrody zaprojektowane z myślą o niskim zużyciu wody, z automatycznym nawadnianiem oraz strefami spacerowymi i wypoczynkowymi.',
  'Et felles basseng, et utstyrt felles treningsrom, et utendørs sportsområde og en zensone, og store hager utformet for lavt vannforbruk, med automatisk vanning og områder for å gå og hvile.',
  'En gemensam pool, ett utrustat gemensamt gym, en idrottsyta utomhus och en zenzon, och stora trädgårdar utformade för låg vattenförbrukning, med automatisk bevattning och ytor för promenader och vila.')
p('.qualitySpecs.groups[6].items[1]',  # 80
  'Aparcamiento para bicicletas en la entrada, una caseta de control de acceso y ascensores con puertas automáticas para ocho personas.',
  'Râteliers à vélos à l’entrée, une guérite de contrôle d’accès et des ascenseurs à portes automatiques pour huit personnes.',
  'Fahrradständer am Eingang, ein Zugangskontrollhäuschen und Aufzüge mit automatischen Türen für acht Personen.',
  'Велопарковка у входа, контрольно-пропускной пункт и лифты с автоматическими дверями на восемь человек.',
  'مواقف للدراجات عند المدخل، وكشك للتحكم في الدخول، ومصاعد بأبواب آلية تتسع لثمانية أشخاص.',
  'Fietsenrekken bij de ingang, een toegangscontrolepost en liften met automatische deuren voor acht personen.',
  'Stojaki na rowery przy wejściu, budka kontroli dostępu oraz windy z automatycznymi drzwiami dla ośmiu osób.',
  'Sykkelstativer ved inngangen, en adgangskontrollbu og heiser med automatiske dører for åtte personer.',
  'Cykelställ vid entrén, en lucka för tillträdeskontroll och hissar med automatiska dörrar för åtta personer.')
p('.qualitySpecs.groups[7].name',  # 81
  'Garaje y trasteros', 'Garage et caves', 'Garage und Abstellräume', 'Гараж и кладовые', 'المرآب وغرف التخزين',
  'Garage en bergingen', 'Garaż i komórki lokatorskie', 'Garasje og boder', 'Garage och förråd')
p('.qualitySpecs.groups[7].items[0]',  # 82
  'Aparcamientos cubiertos y descubiertos con suelo de hormigón y puerta de vehículos automática, puertas de acero con ventilación y cerradura en los trasteros, detección y alarma de incendios en todos los garajes y previsión para la carga de coches eléctricos conforme a la normativa.',
  'Parkings couverts et découverts avec sol en béton et porte véhicules automatique, portes en acier ventilées avec serrure pour les caves, détection et alarme incendie dans tous les garages et prééquipement pour la recharge des véhicules électriques conformément à la réglementation.',
  'Überdachte und offene Stellplätze mit Betonboden und automatischem Fahrzeugtor, Stahltüren mit Belüftung und Schloss an den Abstellräumen, Branderkennung und Alarm in allen Garagen sowie eine Vorbereitung für das Laden von Elektrofahrzeugen entsprechend den Vorschriften.',
  'Крытые и открытые парковки с бетонным полом и автоматическими въездными воротами, стальные двери кладовых с вентиляцией и замком, пожарная сигнализация во всех гаражах и подготовка к установке зарядки для электромобилей в соответствии с нормами.',
  'مواقف سيارات مغطاة ومكشوفة بأرضية خرسانية وبوابة آلية للسيارات، وأبواب فولاذية لغرف التخزين مزودة بتهوية وقفل، وكشف وإنذار للحرائق في جميع المرائب، وتجهيز مسبق لشحن السيارات الكهربائية وفق اللوائح.',
  'Overdekte en open parkeerplaatsen met een betonnen vloer en een automatische voertuigpoort, stalen bergingsdeuren met ventilatie en slot, brandmelding en alarm in alle garages en een voorbereiding voor het laden van elektrische auto’s volgens de regelgeving.',
  'Miejsca postojowe zadaszone i odkryte z betonową posadzką i automatyczną bramą wjazdową, stalowe drzwi komórek lokatorskich z wentylacją i zamkiem, wykrywanie i sygnalizacja pożaru we wszystkich garażach oraz przygotowanie do ładowania pojazdów elektrycznych zgodnie z przepisami.',
  'Overbygde og åpne parkeringsplasser med betonggulv og automatisk kjøretøyport, stålbodører med ventilasjon og lås, brannvarsling og alarm i alle garasjer og tilrettelegging for lading av elbiler i samsvar med forskriftene.',
  'Övertäckta och öppna parkeringsplatser med betonggolv och automatisk fordonsport, stålförrådsdörrar med ventilation och lås, brandlarm i alla garage och förberedelse för laddning av elbilar enligt föreskrifterna.')
p('.qualitySpecs.groups[8].name',  # 83
  'La casa club', 'Le club-house', 'Das Clubhaus', 'Клубный дом', 'نادي المجمع', 'Het clubhuis', 'Klub mieszkańców', 'Klubbhuset', 'Klubbhuset')
p('.qualitySpecs.groups[8].items[0]',  # 84
  'La vivienda incluye una participación de propiedad en un edificio de servicios, la casa club, con spa, sauna, gimnasio equipado y salas comunitarias, gestionado a través de las comunidades de propietarios como ampliación de las zonas comunes.',
  'Le logement comprend une quote-part de propriété d’un bâtiment de services, le club-house, avec spa, sauna, salle de sport équipée et salles communes, géré par les copropriétés comme une extension des parties communes.',
  'Zur Wohnung gehört ein Eigentumsanteil an einem Servicegebäude, dem Clubhaus, mit Spa, Sauna, ausgestattetem Fitnessraum und Gemeinschaftsräumen, verwaltet über die Eigentümergemeinschaften als Erweiterung der Gemeinschaftsflächen.',
  'В квартиру входит доля собственности в сервисном здании — клубном доме, со спа, сауной, оборудованным тренажёрным залом и общими залами; им управляют через товарищества собственников как продолжением общих зон.',
  'يأتي مع المسكن حصة ملكية في مبنى خدمات هو نادي المجمع، وفيه سبا وساونا وصالة رياضية مجهزة وقاعات مشتركة، ويُدار عبر اتحادات الملاك بوصفه امتدادًا للمناطق المشتركة.',
  'Bij de woning hoort een eigendomsaandeel in een dienstengebouw, het clubhuis, met spa, sauna, een uitgeruste fitnessruimte en gemeenschappelijke ruimten, beheerd via de eigenaarsverenigingen als uitbreiding van de gemeenschappelijke ruimten.',
  'Do lokalu należy udział własnościowy w budynku usługowym, czyli klubie mieszkańców, ze strefą spa, sauną, wyposażoną siłownią i salami wspólnymi, zarządzanym przez wspólnoty mieszkaniowe jako rozszerzenie części wspólnych.',
  'Boligen følger med en eierandel i en servicebygning, klubbhuset, med spa, badstue, et utstyrt treningsrom og fellesrom, forvaltet gjennom sameiene som en utvidelse av fellesarealene.',
  'Till bostaden hör en ägarandel i en servicebyggnad, klubbhuset, med spa, bastu, ett utrustat gym och gemensamma rum, som förvaltas via ägarsamfälligheterna som en utvidgning av de gemensamma ytorna.')

# ---- residences ---------------------------------------------------------------------------
p('.residences.copy',  # 85
  'Las siete viviendas de la lista de precios se dividen en tres grupos. La tabla de abajo recoge cada una con su precio.',
  'Les sept logements de la liste de prix se répartissent en trois groupes. Le tableau ci-dessous présente chacun avec son prix.',
  'Die sieben Wohnungen auf der Preisliste lassen sich in drei Gruppen einteilen. Die Tabelle unten führt jede mit ihrem Preis auf.',
  'Семь квартир из прайс-листа делятся на три группы. В таблице ниже перечислены все они с ценами.',
  'تنقسم المساكن السبعة الواردة في قائمة الأسعار إلى ثلاث مجموعات. ويورد الجدول أدناه كلًّا منها مع سعره.',
  'De zeven woningen op de prijslijst vallen in drie groepen. De tabel hieronder toont elke woning met haar prijs.',
  'Siedem lokali z cennika dzieli się na trzy grupy. Tabela poniżej wymienia każdy z nich wraz z ceną.',
  'De sju boligene på prislisten faller i tre grupper. Tabellen nedenfor viser hver av dem med pris.',
  'De sju bostäderna på prislistan delas in i tre grupper. Tabellen nedan listar var och en med sitt pris.')
p('.residences.items[0].name',  # 86
  'Viviendas de dos dormitorios', 'Logements de deux chambres', 'Wohnungen mit zwei Schlafzimmern', 'Квартиры с двумя спальнями',
  'مساكن من غرفتي نوم', 'Woningen met twee slaapkamers', 'Lokale z dwiema sypialniami', 'Boliger med to soverom', 'Bostäder med två sovrum')
p('.residences.items[0].points[0]',  # 87
  '3 viviendas de dos dormitorios y dos baños: de #93.8 a #98.7 [m2] construidos y de #71.7 a #75.4 [m2] interiores.',
  '3 logements de deux chambres et deux salles de bains : de #93.8 à #98.7 [m2] construits et de #71.7 à #75.4 [m2] intérieurs.',
  '3 Wohnungen mit zwei Schlafzimmern und zwei Bädern: #93.8 bis #98.7 [m2] bebaut und #71.7 bis #75.4 [m2] Innenfläche.',
  '3 квартиры с двумя спальнями и двумя ванными комнатами: от #93.8 до #98.7 [m2] застроенной площади и от #71.7 до #75.4 [m2] внутренней.',
  '3 مساكن من غرفتي نوم وحمامين: من #93.8 إلى #98.7 [m2] مبنية ومن #71.7 إلى #75.4 [m2] داخلية.',
  '3 woningen met twee slaapkamers en twee badkamers: #93.8 tot #98.7 [m2] bebouwde oppervlakte en #71.7 tot #75.4 [m2] binnenoppervlakte.',
  '3 lokale z dwiema sypialniami i dwiema łazienkami: od #93.8 do #98.7 [m2] zabudowy i od #71.7 do #75.4 [m2] wnętrza.',
  '3 boliger med to soverom og to bad: #93.8 til #98.7 [m2] bygd og #71.7 til #75.4 [m2] innvendig.',
  '3 bostäder med två sovrum och två badrum: #93.8 till #98.7 [m2] byggyta och #71.7 till #75.4 [m2] inomhus.')
p('.residences.items[0].points[1]',  # 88
  'Terrazas de #65.7 y #69.6 [m2] en dos de ellas, y una terraza cubierta de #24.8 [m2] con un jardín de #60.2 [m2] en la tercera.',
  'Des terrasses de #65.7 et #69.6 [m2] pour deux d’entre eux, et une terrasse couverte de #24.8 [m2] avec un jardin de #60.2 [m2] pour le troisième.',
  'Terrassen von #65.7 und #69.6 [m2] bei zwei von ihnen und eine überdachte Terrasse von #24.8 [m2] mit einem Garten von #60.2 [m2] bei der dritten.',
  'Террасы площадью #65.7 и #69.6 [m2] у двух из них и крытая терраса #24.8 [m2] с садом #60.2 [m2] у третьей.',
  'تراسات مساحتها #65.7 و#69.6 [m2] في اثنين منها، وتراس مغطى مساحته #24.8 [m2] مع حديقة مساحتها #60.2 [m2] في الثالث.',
  'Terrassen van #65.7 en #69.6 [m2] bij twee ervan en een overdekt terras van #24.8 [m2] met een tuin van #60.2 [m2] bij de derde.',
  'Tarasy o powierzchni #65.7 i #69.6 [m2] w dwóch z nich oraz taras zadaszony o powierzchni #24.8 [m2] z ogrodem o powierzchni #60.2 [m2] w trzecim.',
  'Terrasser på #65.7 og #69.6 [m2] for to av dem, og en overbygd terrasse på #24.8 [m2] med en hage på #60.2 [m2] for den tredje.',
  'Terrasser på #65.7 och #69.6 [m2] för två av dem, och en övertäckt terrass på #24.8 [m2] med en trädgård på #60.2 [m2] för den tredje.')
p('.residences.items[0].points[2]',  # 89
  'Cada una tiene una plaza de garaje y un trastero, y los precios van de €442000 a €552000.',
  'Chacun a une place de garage et une cave, et les prix vont de €442000 à €552000.',
  'Jede hat einen Garagenstellplatz und einen Abstellraum, und die Preise reichen von €442000 bis €552000.',
  'У каждой есть место в гараже и кладовая, а цены — от €442000 до €552000.',
  'لكل مسكن موقف سيارة في المرآب وغرفة تخزين، وتتراوح الأسعار من €442000 إلى €552000.',
  'Elke woning heeft een garageplaats en een berging, en de prijzen lopen van €442000 tot €552000.',
  'Każdy ma miejsce w garażu i komórkę lokatorską, a ceny wahają się od €442000 do €552000.',
  'Hver av dem har en garasjeplass og en bod, og prisene går fra €442000 til €552000.',
  'Var och en har en garageplats och ett förråd, och priserna går från €442000 till €552000.')
p('.residences.items[1].name',  # 90
  'Viviendas de tres dormitorios en una planta', 'Logements de trois chambres de plain-pied', 'Wohnungen mit drei Schlafzimmern auf einer Ebene',
  'Квартиры с тремя спальнями на одном уровне', 'مساكن من ثلاث غرف نوم على مستوى واحد', 'Woningen met drie slaapkamers op één niveau',
  'Lokale z trzema sypialniami na jednym poziomie', 'Boliger med tre soverom på ett plan', 'Bostäder med tre sovrum på ett plan')
p('.residences.items[1].points[0]',  # 91
  '3 viviendas de tres dormitorios y dos baños: de #119.5 a #124.3 [m2] construidos y de #89.8 a #92.9 [m2] interiores.',
  '3 logements de trois chambres et deux salles de bains : de #119.5 à #124.3 [m2] construits et de #89.8 à #92.9 [m2] intérieurs.',
  '3 Wohnungen mit drei Schlafzimmern und zwei Bädern: #119.5 bis #124.3 [m2] bebaut und #89.8 bis #92.9 [m2] Innenfläche.',
  '3 квартиры с тремя спальнями и двумя ванными комнатами: от #119.5 до #124.3 [m2] застроенной площади и от #89.8 до #92.9 [m2] внутренней.',
  '3 مساكن من ثلاث غرف نوم وحمامين: من #119.5 إلى #124.3 [m2] مبنية ومن #89.8 إلى #92.9 [m2] داخلية.',
  '3 woningen met drie slaapkamers en twee badkamers: #119.5 tot #124.3 [m2] bebouwde oppervlakte en #89.8 tot #92.9 [m2] binnenoppervlakte.',
  '3 lokale z trzema sypialniami i dwiema łazienkami: od #119.5 do #124.3 [m2] zabudowy i od #89.8 do #92.9 [m2] wnętrza.',
  '3 boliger med tre soverom og to bad: #119.5 til #124.3 [m2] bygd og #89.8 til #92.9 [m2] innvendig.',
  '3 bostäder med tre sovrum och två badrum: #119.5 till #124.3 [m2] byggyta och #89.8 till #92.9 [m2] inomhus.')
p('.residences.items[1].points[1]',  # 92
  'Terrazas de #46.8 y #71.0 [m2] en dos de ellas, y #27.1 [m2] de terraza con un jardín de #175.6 [m2] en la tercera.',
  'Des terrasses de #46.8 et #71.0 [m2] pour deux d’entre eux, et #27.1 [m2] de terrasse avec un jardin de #175.6 [m2] pour le troisième.',
  'Terrassen von #46.8 und #71.0 [m2] bei zweien von ihnen und #27.1 [m2] Terrasse mit einem Garten von #175.6 [m2] bei der dritten.',
  'Террасы площадью #46.8 и #71.0 [m2] у двух из них и терраса #27.1 [m2] с садом #175.6 [m2] у третьей.',
  'تراسات مساحتها #46.8 و#71.0 [m2] في اثنين منها، وتراس مساحته #27.1 [m2] مع حديقة مساحتها #175.6 [m2] في الثالث.',
  'Terrassen van #46.8 en #71.0 [m2] bij twee ervan en #27.1 [m2] terras met een tuin van #175.6 [m2] bij de derde.',
  'Tarasy o powierzchni #46.8 i #71.0 [m2] w dwóch z nich oraz taras o powierzchni #27.1 [m2] z ogrodem o powierzchni #175.6 [m2] w trzecim.',
  'Terrasser på #46.8 og #71.0 [m2] for to av dem, og #27.1 [m2] terrasse med en hage på #175.6 [m2] for den tredje.',
  'Terrasser på #46.8 och #71.0 [m2] för två av dem, och #27.1 [m2] terrass med en trädgård på #175.6 [m2] för den tredje.')
p('.residences.items[1].points[2]',  # 93
  'Una plaza de garaje para la primera y dos para las otras, con un trastero cada una. Los precios van de €451000 a €633000.',
  'Une place de garage pour le premier et deux pour les autres, avec une cave chacun. Les prix vont de €451000 à €633000.',
  'Ein Garagenstellplatz für die erste Wohnung und zwei für die anderen, jeweils mit einem Abstellraum. Die Preise reichen von €451000 bis €633000.',
  'Одно место в гараже у первой и по два у остальных, у каждой — кладовая. Цены — от €451000 до €633000.',
  'موقف سيارة واحد في المرآب للأول وموقفان لكل من الآخرين، مع غرفة تخزين لكل منها. وتتراوح الأسعار من €451000 إلى €633000.',
  'Een garageplaats voor de eerste en twee voor de andere, elk met een berging. De prijzen lopen van €451000 tot €633000.',
  'Jedno miejsce w garażu przy pierwszym i dwa przy pozostałych, każdy z komórką lokatorską. Ceny wahają się od €451000 do €633000.',
  'En garasjeplass for den første og to for de andre, hver med en bod. Prisene går fra €451000 til €633000.',
  'En garageplats för den första och två för de andra, var och en med ett förråd. Priserna går från €451000 till €633000.')
p('.residences.items[2].points[0]',  # 94
  'Una vivienda de tres dormitorios en dos plantas, con tres dormitorios y dos baños en la planta superior y el salón, un aseo y un cuarto de lavado en la inferior: #143.3 [m2] construidos y #101.3 [m2] interiores.',
  'Un logement de trois chambres sur deux niveaux, avec trois chambres et deux salles de bains à l’étage et le séjour, des toilettes et une buanderie au rez-de-chaussée : #143.3 [m2] construits et #101.3 [m2] intérieurs.',
  'Eine Wohnung mit drei Schlafzimmern über Erd- und Obergeschoss, mit drei Schlafzimmern und zwei Bädern oben und dem Wohnbereich, einem WC und einem Hauswirtschaftsraum unten: #143.3 [m2] bebaut und #101.3 [m2] Innenfläche.',
  'Квартира с тремя спальнями на двух уровнях: наверху три спальни и две ванные комнаты, внизу гостиная, туалет и постирочная: #143.3 [m2] застроенной площади и #101.3 [m2] внутренней.',
  'مسكن من ثلاث غرف نوم على طابقين، بثلاث غرف نوم وحمامين في الطابق العلوي، وغرفة المعيشة ودورة مياه وغرفة غسيل في الطابق السفلي: #143.3 [m2] مبنية و#101.3 [m2] داخلية.',
  'Een woning met drie slaapkamers over de begane grond en de eerste verdieping, met drie slaapkamers en twee badkamers boven en de woonruimte, een toilet en een bijkeuken beneden: #143.3 [m2] bebouwde oppervlakte en #101.3 [m2] binnenoppervlakte.',
  'Lokal z trzema sypialniami na dwóch kondygnacjach, z trzema sypialniami i dwiema łazienkami na piętrze oraz częścią dzienną, toaletą i pomieszczeniem gospodarczym na parterze: #143.3 [m2] zabudowy i #101.3 [m2] wnętrza.',
  'En bolig med tre soverom over første og andre etasje, med tre soverom og to bad i øverste etasje og oppholdsrommet, et toalett og et vaskerom i første: #143.3 [m2] bygd og #101.3 [m2] innvendig.',
  'En bostad med tre sovrum över bottenvåningen och första våningen, med tre sovrum och två badrum på övre planet och vardagsrummet, en toalett och ett tvättrum på nedre planet: #143.3 [m2] byggyta och #101.3 [m2] inomhus.')
p('.residences.items[2].points[1]',  # 95
  'Un jardín de #41.8 [m2] y una terraza descubierta de #11.2 [m2].',
  'Un jardin de #41.8 [m2] et une terrasse découverte de #11.2 [m2].',
  'Ein Garten von #41.8 [m2] und eine unüberdachte Terrasse von #11.2 [m2].',
  'Сад площадью #41.8 [m2] и открытая терраса #11.2 [m2].',
  'حديقة مساحتها #41.8 [m2] وتراس مكشوف مساحته #11.2 [m2].',
  'Een tuin van #41.8 [m2] en een open terras van #11.2 [m2].',
  'Ogród o powierzchni #41.8 [m2] i taras odkryty o powierzchni #11.2 [m2].',
  'En hage på #41.8 [m2] og en åpen terrasse på #11.2 [m2].',
  'En trädgård på #41.8 [m2] och en öppen terrass på #11.2 [m2].')
p('.residences.items[2].points[2]',  # 96
  'Una plaza de garaje y un trastero, por €537000.',
  'Une place de garage et une cave, pour €537000.',
  'Ein Garagenstellplatz und ein Abstellraum, für €537000.',
  'Одно место в гараже и кладовая — за €537000.',
  'موقف سيارة واحد في المرآب وغرفة تخزين، بسعر €537000.',
  'Een garageplaats en een berging, voor €537000.',
  'Jedno miejsce w garażu i komórka lokatorska za €537000.',
  'En garasjeplass og en bod, for €537000.',
  'En garageplats och ett förråd, för €537000.')

# ---- lifestyle and location ---------------------------------------------------------------
p('.lifestyle.headlineHtml',  # 97
  'Terrazas, <em>una piscina</em> y el golf cerca',
  'Des terrasses, <em>une piscine</em> et le golf à proximité',
  'Terrassen, <em>ein Pool</em> und der Golfplatz in der Nähe',
  'Террасы, <em>бассейн</em> и гольф рядом',
  'تراسات، <em>ومسبح</em> وملاعب غولف قريبة',
  'Terrassen, <em>een zwembad</em> en golf in de buurt',
  'Tarasy, <em>basen</em> i golf w pobliżu',
  'Terrasser, <em>et basseng</em> og golf i nærheten',
  'Terrasser, <em>en pool</em> och golf i närheten')
p('.lifestyle.copy',  # 98
  'La vida aquí es al aire libre: el jardín o la terraza de la vivienda, la piscina comunitaria y la casa club.',
  'La vie ici se déroule en plein air : le jardin ou la terrasse du logement, la piscine commune et le club-house.',
  'Das Leben hier spielt sich draußen ab: im Garten oder auf der Terrasse der Wohnung, am Gemeinschaftspool und im Clubhaus.',
  'Жизнь здесь проходит на открытом воздухе: сад или терраса квартиры, общий бассейн и клубный дом.',
  'الحياة هنا في الهواء الطلق: حديقة المسكن أو تراسه، والمسبح المشترك، ونادي المجمع.',
  'Het leven hier speelt zich buiten af: de tuin of het terras van de woning, het gemeenschappelijke zwembad en het clubhuis.',
  'Życie toczy się tu na świeżym powietrzu: ogród lub taras lokalu, wspólny basen i klub mieszkańców.',
  'Livet her er utendørs: hagen eller terrassen til boligen, fellesbassenget og klubbhuset.',
  'Livet här är utomhus: bostadens trädgård eller terrass, den gemensamma poolen och klubbhuset.')
p('.lifestyle.panels[0][0]',  # 99
  'El jardín o la terraza', 'Le jardin ou la terrasse', 'Der Garten oder die Terrasse', 'Сад или терраса', 'الحديقة أو التراس',
  'De tuin of het terras', 'Ogród lub taras', 'Hagen eller terrassen', 'Trädgården eller terrassen')
p('.lifestyle.panels[0][1]',  # 100
  'Todas las viviendas de la lista tienen jardín, terraza o ambos, con terrazas de 11 a 71 m² y jardines de 42 a 176 m².',
  'Tous les logements de la liste ont un jardin, une terrasse ou les deux, avec des terrasses de 11 à 71 m² et des jardins de 42 à 176 m².',
  'Jede Wohnung auf der Liste hat einen Garten, eine Terrasse oder beides, mit Terrassen von 11 bis 71 m² und Gärten von 42 bis 176 m².',
  'У каждой квартиры из списка есть сад, терраса или и то и другое: террасы от 11 до 71 м² и сады от 42 до 176 м².',
  'لكل مسكن في القائمة حديقة أو تراس أو كلاهما، بتراسات من 11 إلى 71 م² وحدائق من 42 إلى 176 م².',
  'Elke woning op de lijst heeft een tuin, een terras of allebei, met terrassen van 11 tot 71 m² en tuinen van 42 tot 176 m².',
  'Każdy lokal z listy ma ogród, taras lub jedno i drugie, z tarasami o powierzchni od 11 do 71 m² i ogrodami od 42 do 176 m².',
  'Hver bolig på listen har hage, terrasse eller begge deler, med terrasser på 11 til 71 m² og hager på 42 til 176 m².',
  'Varje bostad på listan har trädgård, terrass eller båda, med terrasser på 11 till 71 m² och trädgårdar på 42 till 176 m².')
p('.lifestyle.panels[1][0]',  # 101
  'La piscina y el gimnasio', 'La piscine et la salle de sport', 'Der Pool und der Fitnessraum', 'Бассейн и тренажёрный зал', 'المسبح والصالة الرياضية',
  'Het zwembad en de fitnessruimte', 'Basen i siłownia', 'Bassenget og treningsrommet', 'Poolen och gymmet')
p('.lifestyle.panels[1][1]',  # 102
  'Una piscina comunitaria y un gimnasio equipado en un espacio acristalado con vistas a las zonas comunes, con una zona deportiva exterior y una zona zen.',
  'Une piscine commune et une salle de sport équipée dans un espace vitré donnant sur les parties communes, avec un espace sportif extérieur et un espace zen.',
  'Ein Gemeinschaftspool und ein ausgestatteter Fitnessraum in einem verglasten Raum mit Blick auf die Gemeinschaftsflächen, dazu ein Sportbereich im Freien und ein Zen-Bereich.',
  'Общий бассейн и оборудованный тренажёрный зал в застеклённом помещении с видом на общие зоны, а также спортивная площадка на открытом воздухе и зона дзен.',
  'مسبح مشترك وصالة رياضية مجهزة في فضاء زجاجي يطل على المناطق المشتركة، مع منطقة رياضية خارجية ومنطقة زِن.',
  'Een gemeenschappelijk zwembad en een uitgeruste fitnessruimte in een glazen ruimte met uitzicht op de gemeenschappelijke ruimten, met een sportzone buiten en een zenzone.',
  'Wspólny basen i wyposażona siłownia w przeszklonej przestrzeni z widokiem na części wspólne, a także zewnętrzna strefa sportowa i strefa zen.',
  'Et felles basseng og et utstyrt treningsrom i et glassrom med utsikt over fellesarealene, med et utendørs sportsområde og en zensone.',
  'En gemensam pool och ett utrustat gym i ett glasat rum med utsikt över de gemensamma ytorna, med en idrottsyta utomhus och en zenzon.')
p('.lifestyle.panels[2][1]',  # 103
  'Una casa club para los residentes con spa, sauna, gimnasio equipado, zonas sociales y una cafetería con terraza, de propiedad compartida mediante una participación que acompaña a la vivienda.',
  'Un club-house pour les résidents avec spa, sauna, salle de sport équipée, espaces conviviaux et un café avec terrasse, détenu en commun grâce à une quote-part qui accompagne le logement.',
  'Ein Clubhaus für die Bewohner mit Spa, Sauna, ausgestattetem Fitnessraum, Aufenthaltsbereichen und einem Café mit Terrasse, gemeinsam besessen über einen Anteil, der zur Wohnung gehört.',
  'Клубный дом для жильцов со спа, сауной, оборудованным тренажёрным залом, общими зонами и кафе с террасой, находящийся в совместной собственности через долю, которая прилагается к квартире.',
  'نادٍ للسكان فيه سبا وساونا وصالة رياضية مجهزة ومناطق اجتماعية ومقهى بتراس، ملكيته مشتركة عبر حصة تأتي مع المسكن.',
  'Een clubhuis voor de bewoners met spa, sauna, een uitgeruste fitnessruimte, sociale ruimten en een café met terras, gezamenlijk bezeten via een aandeel dat bij de woning hoort.',
  'Klub dla mieszkańców ze strefą spa, sauną, wyposażoną siłownią, strefami towarzyskimi i kawiarnią z tarasem, będący współwłasnością dzięki udziałowi, który przysługuje wraz z lokalem.',
  'Et klubbhus for beboerne med spa, badstue, et utstyrt treningsrom, sosiale områder og en kafé med terrasse, eid i fellesskap gjennom en andel som følger med boligen.',
  'Ett klubbhus för de boende med spa, bastu, ett utrustat gym, sociala ytor och ett kafé med terrass, som ägs gemensamt genom en andel som följer med bostaden.')
p('.lifestyle.panels[3][0]',  # 104
  'El golf y los caballos', 'Le golf et les chevaux', 'Golf und Pferde', 'Гольф и лошади', 'الغولف والخيل',
  'Golf en paarden', 'Golf i konie', 'Golf og hester', 'Golf och hästar')
p('.lifestyle.panels[3][1]',  # 105
  'Cerca hay cuatro campos de golf, Flamingos, Cancelada, El Campanario y Atalaya, además de una escuela de arte ecuestre aprobada por la British Horse Society.',
  'Quatre golfs sont proches, Flamingos, Cancelada, El Campanario et Atalaya, ainsi qu’une école d’art équestre agréée par la British Horse Society.',
  'Vier Golfplätze sind nah, Flamingos, Cancelada, El Campanario und Atalaya, dazu eine von der British Horse Society anerkannte Reitkunstschule.',
  'Рядом четыре поля для гольфа — Flamingos, Cancelada, El Campanario и Atalaya, а также школа верховой езды, одобренная British Horse Society.',
  'يوجد بالقرب أربعة ملاعب غولف هي Flamingos وCancelada وEl Campanario وAtalaya، إضافة إلى مدرسة لفنون الفروسية معتمدة من British Horse Society.',
  'Vier golfbanen liggen vlakbij, Flamingos, Cancelada, El Campanario en Atalaya, evenals een ruitersportschool die is goedgekeurd door de British Horse Society.',
  'W pobliżu znajdują się cztery pola golfowe: Flamingos, Cancelada, El Campanario i Atalaya, a także szkoła jazdy konnej zatwierdzona przez British Horse Society.',
  'Fire golfbaner ligger like ved, Flamingos, Cancelada, El Campanario og Atalaya, i tillegg til en rideskole godkjent av British Horse Society.',
  'Fyra golfbanor ligger nära, Flamingos, Cancelada, El Campanario och Atalaya, liksom en ridskola godkänd av British Horse Society.')
p('.location.headlineHtml',  # 106
  'Cancelada, <em>en la Nueva Milla de Oro</em>',
  'Cancelada, <em>sur la Nouvelle Mille d’Or</em>',
  'Cancelada, <em>an der Neuen Goldenen Meile</em>',
  'Канселада, <em>на Новой Золотой миле</em>',
  'كانسيلادا، <em>على الميل الذهبي الجديد</em>',
  'Cancelada, <em>aan de Nieuwe Golden Mile</em>',
  'Cancelada, <em>na Nowej Złotej Mili</em>',
  'Cancelada, <em>på Nye Golden Mile</em>',
  'Cancelada, <em>på Nya Golden Mile</em>')
p('.location.copy',  # 107
  'Las viviendas están en Cancelada, una zona residencial tranquila entre Estepona y Marbella. El dossier del promotor da 12 km hasta Estepona, 12 km hasta Puerto Banús, 21 km hasta Marbella y 58 km hasta Gibraltar, y señala que el aeropuerto de Málaga y la estación del tren de alta velocidad están a unos 45 minutos. En los alrededores hay colegios, supermercados, farmacias, centros de salud y hospitales, y también la ciclosenda de Cancelada.',
  'Les logements sont à Cancelada, un quartier résidentiel calme entre Estepona et Marbella. La brochure du promoteur indique 12 km jusqu’à Estepona, 12 km jusqu’à Puerto Banús, 21 km jusqu’à Marbella et 58 km jusqu’à Gibraltar, et précise que l’aéroport de Málaga et la gare du train à grande vitesse sont à environ 45 minutes. Des écoles, des supermarchés, des pharmacies, des centres de santé et des hôpitaux se trouvent à proximité, tout comme la piste cyclable de Cancelada.',
  'Die Wohnungen liegen in Cancelada, einem ruhigen Wohngebiet zwischen Estepona und Marbella. Die Broschüre des Bauträgers nennt 12 km bis Estepona, 12 km bis Puerto Banús, 21 km bis Marbella und 58 km bis Gibraltar und gibt an, dass der Flughafen Málaga und der Hochgeschwindigkeitsbahnhof etwa 45 Minuten entfernt sind. Schulen, Supermärkte, Apotheken, Gesundheitszentren und Krankenhäuser liegen in der Nähe, ebenso der Radweg von Cancelada.',
  'Квартиры находятся в Канселаде — тихом жилом районе между Эстепоной и Марбельей. В брошюре застройщика указано 12 км до Эстепоны, 12 км до Пуэрто-Банус, 21 км до Марбельи и 58 км до Гибралтара, а также что до аэропорта Малаги и вокзала скоростных поездов около 45 минут. Поблизости есть школы, супермаркеты, аптеки, медицинские центры и больницы, а также велодорожка Канселады.',
  'تقع المساكن في كانسيلادا، وهي منطقة سكنية هادئة بين إستيبونا وماربيا. ويذكر كتيّب المطوّر 12 كم إلى إستيبونا و12 كم إلى بويرتو بانوس و21 كم إلى ماربيا و58 كم إلى جبل طارق، ويشير إلى أن مطار مالقة ومحطة القطار فائق السرعة على بعد نحو 45 دقيقة. وفي المنطقة مدارس وأسواق كبرى وصيدليات ومراكز صحية ومستشفيات، وكذلك مسار الدراجات في كانسيلادا.',
  'De woningen liggen in Cancelada, een rustige woonwijk tussen Estepona en Marbella. De brochure van de ontwikkelaar noemt 12 km naar Estepona, 12 km naar Puerto Banús, 21 km naar Marbella en 58 km naar Gibraltar, en meldt dat de luchthaven van Málaga en het hogesnelheidsstation ongeveer 45 minuten verderop liggen. Scholen, supermarkten, apotheken, gezondheidscentra en ziekenhuizen liggen in de buurt, evenals het fietspad van Cancelada.',
  'Lokale znajdują się w miejscowości Cancelada, spokojnej dzielnicy mieszkaniowej między Esteponą a Marbellą. Broszura dewelopera podaje 12 km do Estepony, 12 km do Puerto Banús, 21 km do Marbelli i 58 km do Gibraltaru oraz że lotnisko w Maladze i stacja kolei dużych prędkości są oddalone o około 45 minut. W pobliżu są szkoły, supermarkety, apteki, ośrodki zdrowia i szpitale, a także ścieżka rowerowa w Cancelada.',
  'Boligene ligger i Cancelada, et rolig boligområde mellom Estepona og Marbella. Utbyggerens brosjyre oppgir 12 km til Estepona, 12 km til Puerto Banús, 21 km til Marbella og 58 km til Gibraltar, og sier at Málaga lufthavn og høyhastighetstogstasjonen ligger omtrent 45 minutter unna. Skoler, supermarkeder, apotek, helsesentre og sykehus ligger i nærheten, og det samme gjør sykkelstien i Cancelada.',
  'Bostäderna ligger i Cancelada, ett lugnt bostadsområde mellan Estepona och Marbella. Exploatörens broschyr anger 12 km till Estepona, 12 km till Puerto Banús, 21 km till Marbella och 58 km till Gibraltar, och säger att Málaga flygplats och höghastighetsstationen ligger omkring 45 minuter bort. Skolor, stormarknader, apotek, vårdcentraler och sjukhus finns i närheten, liksom cykelvägen i Cancelada.')
p('.location.mapLabelHtml',  # 108
  'Cancelada, <em>Estepona</em>', 'Cancelada, <em>Estepona</em>', 'Cancelada, <em>Estepona</em>', 'Канселада, <em>Эстепона</em>',
  'كانسيلادا، <em>إستيبونا</em>', 'Cancelada, <em>Estepona</em>', 'Cancelada, <em>Estepona</em>', 'Cancelada, <em>Estepona</em>', 'Cancelada, <em>Estepona</em>')
p('.location.distances[4][0]',  # 109
  'Gibraltar', 'Gibraltar', 'Gibraltar', 'Гибралтар', 'جبل طارق', 'Gibraltar', 'Gibraltar', 'Gibraltar', 'Gibraltar')

# ---- purchase and checks ------------------------------------------------------------------
p('.investment.cards[0][1]',  # 110
  'La reserva es de €6600, con el IVA incluido.',
  'La réservation est de €6600, TVA incluse.',
  'Die Reservierung beträgt €6600, einschließlich MwSt.',
  'Бронирование стоит €6600 с учётом НДС.',
  'الحجز €6600 شاملًا ضريبة القيمة المضافة.',
  'De reservering bedraagt €6600, inclusief btw.',
  'Rezerwacja wynosi €6600 (z VAT).',
  'Reservasjonen er €6600, inkludert mva.',
  'Reservationen är €6600, inklusive moms.')
p('.investment.cards[1][1]',  # 111
  'El 30% más IVA al firmar el contrato privado de compraventa y el 70% más IVA a la finalización ante notario.',
  '30 % hors TVA à la signature du contrat de vente privé et 70 % hors TVA à l’achèvement chez le notaire.',
  '30 % zuzüglich MwSt. bei Unterzeichnung des privaten Kaufvertrags und 70 % zuzüglich MwSt. bei Fertigstellung beim Notar.',
  '30 % плюс НДС при подписании предварительного договора купли-продажи и 70 % плюс НДС при завершении сделки у нотариуса.',
  '30% زائد ضريبة القيمة المضافة عند توقيع عقد الشراء الخاص، و70% زائد الضريبة عند الإتمام أمام كاتب العدل.',
  '30% plus btw bij ondertekening van de onderhandse koopovereenkomst en 70% plus btw bij oplevering ten overstaan van de notaris.',
  '30% plus VAT przy podpisaniu umowy przedwstępnej i 70% plus VAT u notariusza, przy akcie notarialnym.',
  '30 % pluss mva. ved signering av den private kjøpekontrakten og 70 % pluss mva. ved overtakelse hos notarius.',
  '30 % plus moms vid undertecknandet av det privata köpeavtalet och 70 % plus moms vid tillträdet hos notarien.')
p('.investment.cards[2][1]',  # 112
  'La lista de precios no incluye el IVA. Nueva Living confirma por escrito los impuestos y los gastos de compra.',
  'La liste de prix n’inclut pas la TVA. Nueva Living confirme par écrit les taxes et les frais d’achat.',
  'Die Preisliste enthält keine MwSt. Nueva Living bestätigt Steuern und Kaufnebenkosten schriftlich.',
  'Цены в прайс-листе указаны без НДС. Nueva Living письменно подтверждает налоги и расходы на покупку.',
  'قائمة الأسعار لا تشمل ضريبة القيمة المضافة. وتؤكد Nueva Living الضرائب ومصاريف الشراء كتابةً.',
  'De prijslijst is exclusief btw. Nueva Living bevestigt de belastingen en aankoopkosten schriftelijk.',
  'Cennik nie obejmuje VAT. Nueva Living potwierdza na piśmie podatki i koszty zakupu.',
  'Prislisten inkluderer ikke mva. Nueva Living bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan inkluderar inte moms. Nueva Living bekräftar skatter och köpkostnader skriftligen.')
p('.investment.cards[3][1]',  # 113
  'Los documentos que tenemos no mencionan ninguna garantía para las cantidades entregadas antes de la finalización, por lo que pedimos la póliza y los datos de la cuenta antes de cualquier pago.',
  'Les documents dont nous disposons ne mentionnent aucune garantie pour les sommes versées avant l’achèvement ; nous demandons donc la police et les coordonnées du compte avant tout paiement.',
  'Die uns vorliegenden Unterlagen erwähnen keine Absicherung für Zahlungen vor der Fertigstellung, daher fordern wir die Police und die Kontodaten vor jeder Zahlung an.',
  'В имеющихся у нас документах нет упоминания о гарантии для платежей, внесённых до завершения, поэтому мы запрашиваем полис и реквизиты счёта до любого платежа.',
  'لا تذكر الوثائق التي بحوزتنا أي ضمان للمبالغ المدفوعة قبل الإتمام، لذلك نطلب الوثيقة وبيانات الحساب قبل أي دفعة.',
  'In de documenten waarover we beschikken staat geen waarborg voor betalingen vóór de oplevering, dus we vragen de polis en de rekeninggegevens voordat er iets wordt betaald.',
  'W posiadanych przez nas dokumentach nie ma wzmianki o zabezpieczeniu wpłat dokonywanych przed ukończeniem, dlatego prosimy o polisę i dane rachunku przed jakąkolwiek płatnością.',
  'Dokumentene vi har nevner ingen garanti for innbetalinger før overtakelse, så vi ber om polisen og kontoopplysningene før noen betaling.',
  'Dokumenten vi har nämner ingen garanti för betalningar före tillträdet, så vi ber om polisen och kontouppgifterna före varje betalning.')
p('.trustDossier.cards[0][0]',  # 114
  'Las viviendas de la lista', 'Les logements de la liste', 'Die gelisteten Wohnungen', 'Квартиры из списка', 'المساكن الواردة في القائمة',
  'De vermelde woningen', 'Lokale z listy', 'Boligene på listen', 'Bostäderna på listan')
p('.trustDossier.cards[0][1]',  # 115
  'La lista de precios recoge siete de las 80 viviendas y las marca todas como disponibles. No dice nada de las otras 73, por lo que pedimos la lista completa y el estado de cada vivienda. Junto a cada precio muestra un garaje y un trastero, y confirmamos que están incluidos en él.',
  'La liste de prix recense sept des 80 logements et les marque tous comme disponibles. Elle ne dit rien des 73 autres ; nous demandons donc la liste complète et le statut de chaque logement. Elle indique un garage et une cave à côté de chaque prix, et nous confirmons qu’ils y sont inclus.',
  'Die Preisliste nennt sieben der 80 Wohnungen und kennzeichnet alle sieben als verfügbar. Zu den übrigen 73 sagt sie nichts, daher fragen wir die vollständige Liste und den Status jeder Wohnung an. Neben jedem Preis weist sie einen Garagenstellplatz und einen Abstellraum aus, und wir bestätigen, dass beide darin enthalten sind.',
  'В прайс-листе указаны семь из 80 квартир, и все они отмечены как доступные. Об остальных 73 в нём ничего не сказано, поэтому мы запрашиваем полный список и статус каждой квартиры. Рядом с каждой ценой указаны место в гараже и кладовая, и мы подтверждаем, что они включены в цену.',
  'تدرج قائمة الأسعار سبعة من المساكن الثمانين وتصنفها جميعًا متاحة. ولا تذكر شيئًا عن المساكن الثلاثة والسبعين الأخرى، لذلك نطلب القائمة الكاملة وحالة كل مسكن. وتُظهر بجانب كل سعر موقف سيارة وغرفة تخزين، ونتأكد من أنهما مشمولان به.',
  'De prijslijst noemt zeven van de 80 woningen en markeert alle zeven als beschikbaar. Over de overige 73 zegt ze niets, dus we vragen de volledige lijst en de status van elke woning. Naast elke prijs staat een garageplaats en een berging, en we bevestigen dat die erin zijn begrepen.',
  'Cennik wymienia siedem z 80 lokali i oznacza wszystkie siedem jako dostępne. Nie mówi nic o pozostałych 73, dlatego prosimy o pełną listę i status każdego lokalu. Obok każdej ceny podaje miejsce w garażu i komórkę lokatorską, a my potwierdzamy, że są w niej wliczone.',
  'Prislisten viser sju av de 80 boligene og markerer alle sju som tilgjengelige. Den sier ingenting om de øvrige 73, så vi ber om den fullstendige listen og status for hver bolig. Den viser en garasjeplass og en bod ved siden av hver pris, og vi bekrefter at de er inkludert i den.',
  'Prislistan upptar sju av de 80 bostäderna och markerar alla sju som tillgängliga. Den säger ingenting om de övriga 73, så vi ber om den fullständiga listan och status för varje bostad. Den anger en garageplats och ett förråd bredvid varje pris, och vi bekräftar att de ingår i det.')
p('.trustDossier.cards[1][1]',  # 116
  'El anuncio del promotor da la entrega en abril de 2028. Los documentos que tenemos no indican la licencia de obras ni el estado de las obras, por lo que pedimos la licencia, la fecha de inicio de las obras y la fecha contractual de finalización.',
  'L’annonce du promoteur indique une livraison en avril 2028. Les documents dont nous disposons ne donnent ni le permis de construire ni l’état des travaux ; nous demandons donc le permis, la date de début des travaux et la date d’achèvement contractuelle.',
  'Der Bauträger gibt die Übergabe für April 2028 an. Die uns vorliegenden Unterlagen nennen weder eine Baugenehmigung noch einen Baustand, daher fordern wir die Genehmigung, den Baubeginn und das vertragliche Fertigstellungsdatum an.',
  'Застройщик указывает срок сдачи — апрель 2028 года. В имеющихся у нас документах нет ни разрешения на строительство, ни сведений о ходе работ, поэтому мы запрашиваем разрешение, дату начала работ и договорную дату завершения.',
  'يذكر إعلان المطوّر موعد التسليم في أبريل 2028. ولا تذكر الوثائق التي بحوزتنا رخصة البناء ولا حالة الأعمال، لذلك نطلب الرخصة وتاريخ بدء الأعمال وتاريخ الإتمام التعاقدي.',
  'De vermelding van de ontwikkelaar noemt april 2028 als opleveringsdatum. In de documenten waarover we beschikken staat geen bouwvergunning of stand van de werken, dus we vragen de vergunning, de startdatum van de werken en de contractuele opleveringsdatum.',
  'Deweloper podaje termin oddania na kwiecień 2028 r. W posiadanych przez nas dokumentach nie ma pozwolenia na budowę ani informacji o stanie prac, dlatego prosimy o pozwolenie, termin rozpoczęcia prac i termin ukończenia wskazany w umowie.',
  'Utbyggeren oppgir overtakelse i april 2028. Dokumentene vi har oppgir verken byggetillatelse eller status for arbeidene, så vi ber om tillatelsen, startdatoen for arbeidene og den kontraktsfestede ferdigstillelsesdatoen.',
  'Exploatören anger tillträde i april 2028. Dokumenten vi har anger varken bygglov eller status för byggarbetena, så vi ber om bygglovet, startdatum för arbetena och det avtalade färdigställandedatumet.')
p('.trustDossier.cards[2][1]',  # 117
  'En algunas viviendas, la lista de precios y los planos del promotor difieren en unas décimas de metro cuadrado, y los planos dan además un segundo conjunto de superficies según el decreto andaluz 218/2005. Confirmamos qué cifras utiliza el contrato.',
  'Pour certains logements, la liste de prix et les plans du promoteur diffèrent de quelques dixièmes de mètre carré, et les plans donnent en outre un second jeu de surfaces selon le décret andalou 218/2005. Nous confirmons quels chiffres retient le contrat.',
  'Bei einigen Wohnungen weichen die Preisliste und die Pläne des Bauträgers um wenige Zehntel Quadratmeter voneinander ab, und die Pläne geben außerdem einen zweiten Satz von Flächen nach dem andalusischen Dekret 218/2005 an. Wir klären, welche Zahlen der Vertrag verwendet.',
  'У некоторых квартир прайс-лист и планы застройщика расходятся на несколько десятых квадратного метра, а на планах приведён ещё и второй набор площадей по андалусскому декрету 218/2005. Мы уточняем, какие цифры используются в договоре.',
  'تختلف قائمة الأسعار ومخططات المطوّر في بعض المساكن بعدة أعشار من المتر المربع، وتورد المخططات كذلك مجموعة ثانية من المساحات وفق المرسوم الأندلسي 218/2005. نتحقق من الأرقام التي يعتمدها العقد.',
  'Bij sommige woningen verschillen de prijslijst en de plannen van de ontwikkelaar enkele tienden van een vierkante meter, en de plannen geven bovendien een tweede reeks oppervlakten volgens het Andalusische decreet 218/2005. We bevestigen welke cijfers het contract hanteert.',
  'W przypadku niektórych lokali cennik i plany dewelopera różnią się o kilka dziesiątych metra kwadratowego, a plany podają ponadto drugi zestaw powierzchni według andaluzyjskiego dekretu 218/2005. Potwierdzamy, które wartości przyjmuje umowa.',
  'For noen boliger avviker prislisten og utbyggerens plantegninger med noen tideler av en kvadratmeter, og plantegningene oppgir i tillegg et andre sett med arealer etter det andalusiske dekretet 218/2005. Vi bekrefter hvilke tall kontrakten bruker.',
  'För vissa bostäder skiljer sig prislistan och exploatörens planritningar åt med några tiondelar av en kvadratmeter, och planritningarna anger dessutom en andra uppsättning ytor enligt det andalusiska dekretet 218/2005. Vi bekräftar vilka siffror avtalet använder.')
p('.trustDossier.cards[3][0]',  # 118
  'La participación en la casa club', 'La quote-part du club-house', 'Der Anteil am Clubhaus', 'Доля в клубном доме', 'حصة نادي المجمع',
  'Het aandeel in het clubhuis', 'Udział w klubie mieszkańców', 'Andelen i klubbhuset', 'Andelen i klubbhuset')
p('.trustDossier.cards[3][1]',  # 119
  'El dossier indica que la compra de una vivienda incluye una participación de propiedad en el edificio de servicios de la casa club, gestionado a través de las comunidades de propietarios. No dice qué añade eso al precio ni a los gastos de comunidad, por lo que lo preguntamos.',
  'La brochure indique que l’achat d’un logement comprend une quote-part de propriété du bâtiment de services du club-house, géré par les copropriétés. Elle ne dit pas ce que cela ajoute au prix ni aux charges de copropriété ; nous posons donc la question.',
  'Die Broschüre gibt an, dass zum Kauf einer Wohnung ein Eigentumsanteil am Servicegebäude des Clubhauses gehört, verwaltet über die Eigentümergemeinschaften. Sie sagt nicht, was das zum Preis oder zu den Gemeinschaftskosten hinzufügt, daher fragen wir nach.',
  'В брошюре сказано, что с покупкой квартиры приобретается доля собственности в сервисном здании клубного дома, которым управляют через товарищества собственников. Не сказано, что это добавляет к цене и к расходам на содержание, поэтому мы уточняем.',
  'يذكر الكتيّب أن شراء مسكن يتضمن حصة ملكية في مبنى خدمات نادي المجمع، يُدار عبر اتحادات الملاك. ولا يذكر ما تضيفه هذه الحصة إلى السعر أو إلى رسوم المجتمع السكني، لذلك نستفسر عن ذلك.',
  'De brochure meldt dat bij de aankoop van een woning een eigendomsaandeel in het dienstengebouw van het clubhuis hoort, beheerd via de eigenaarsverenigingen. Ze zegt niet wat dat aan de prijs of aan de servicekosten toevoegt, dus we vragen ernaar.',
  'Broszura podaje, że zakup lokalu obejmuje udział własnościowy w budynku usługowym klubu, zarządzanym przez wspólnoty mieszkaniowe. Nie mówi, co to dodaje do ceny ani do opłat wspólnotowych, dlatego o to pytamy.',
  'Brosjyren sier at kjøp av en bolig omfatter en eierandel i klubbhusets servicebygning, forvaltet gjennom sameiene. Den sier ikke hva det legger til prisen eller til fellesutgiftene, så vi spør om det.',
  'Broschyren anger att köpet av en bostad omfattar en ägarandel i klubbhusets servicebyggnad, som förvaltas via ägarsamfälligheterna. Den säger inte vad det tillför till priset eller till samfällighetsavgifterna, så vi frågar om det.')

# ---- availability -------------------------------------------------------------------------
p('.availability.headlineHtml',  # 120
  '7 viviendas <em>disponibles actualmente</em>',
  '7 logements <em>actuellement disponibles</em>',
  '7 Wohnungen <em>derzeit verfügbar</em>',
  '7 квартир <em>сейчас в продаже</em>',
  '7 مساكن <em>متاحة حاليًا</em>',
  '7 woningen <em>momenteel beschikbaar</em>',
  '7 lokali <em>obecnie dostępnych</em>',
  '7 boliger <em>tilgjengelige nå</em>',
  '7 bostäder <em>tillgängliga just nu</em>')
p('.availability.copy',  # 121
  'Los precios son los de la lista de precios del promotor a octubre de 2026 y no incluyen IVA. La lista recoge 7 de las 80 viviendas y muestra cada una como disponible. Confirmamos los precios y la disponibilidad antes de cualquier reserva.',
  'Les prix sont ceux de la liste de prix du promoteur à octobre 2026 et s’entendent hors TVA. La liste recense 7 des 80 logements et présente chacun comme disponible. Nous confirmons les prix et la disponibilité avant toute réservation.',
  'Die Preise stammen aus der Preisliste des Bauträgers mit Stand Oktober 2026 und verstehen sich zuzüglich MwSt. Die Liste nennt 7 der 80 Wohnungen und zeigt jede als verfügbar. Preise und Verfügbarkeit bestätigen wir vor jeder Reservierung.',
  'Цены взяты из прайс-листа застройщика по состоянию на октябрь 2026 года и не включают НДС. В списке указаны 7 из 80 квартир, и каждая показана как доступная. Цены и наличие мы подтверждаем до любого бронирования.',
  'الأسعار وفق قائمة أسعار المطوّر بحسب وضعها في أكتوبر 2026، ولا تشمل ضريبة القيمة المضافة. وتدرج القائمة 7 من أصل 80 مسكنًا وتعرض كلًّا منها كمتاح. ونؤكد الأسعار والتوفر قبل أي حجز.',
  'De prijzen komen uit de prijslijst van de ontwikkelaar met stand van oktober 2026 en zijn exclusief btw. De lijst noemt 7 van de 80 woningen en toont elk als beschikbaar. We bevestigen prijzen en beschikbaarheid vóór elke reservering.',
  'Ceny pochodzą z cennika dewelopera według stanu na październik 2026 r. i nie zawierają VAT. Lista wymienia 7 z 80 lokali i pokazuje każdy jako dostępny. Ceny i dostępność potwierdzamy przed każdą rezerwacją.',
  'Prisene er de i utbyggerens prisliste per oktober 2026 og er eksklusive mva. Listen viser 7 av de 80 boligene og oppgir hver som tilgjengelig. Vi bekrefter priser og tilgjengelighet før en reservasjon.',
  'Priserna är de i exploatörens prislista per oktober 2026 och är exklusive moms. Listan upptar 7 av de 80 bostäderna och visar var och en som tillgänglig. Vi bekräftar priser och tillgänglighet före varje reservation.')
p('.availability.priceRange',  # 122
  '€442000 - €633000 + IVA', '€442000 - €633000 + TVA', '€442000 - €633000 + MwSt.', '€442000 - €633000 + НДС',
  '€442000 - €633000 + ضريبة القيمة المضافة', '€442000 - €633000 + btw', '€442000 – €633000 + VAT', '€442000 - €633000 + mva.', '€442000 - €633000 + moms')
p('.availability.sourceNote',  # 123
  'Los precios y las superficies están transcritos de la lista de precios del promotor a octubre de 2026, que recoge con precio 7 de las 80 viviendas y muestra cada una como disponible. La lista indica que los precios no incluyen el IVA. La superficie construida incluye una parte proporcional de zonas comunes; la terraza indicada es la cubierta y la descubierta juntas. Cada vivienda figura con un trastero y una plaza de garaje, salvo la 03-06-BJ-C y la 03-07-BJ-A, que tienen dos plazas de garaje. Hay planos de las siete viviendas. Cuando la lista de precios y el plano del promotor difieren, la tabla muestra la lista de precios. Lista / plano: 01-01-BJ-A interior #75.4 / #75.8 [m2], construida #98.7 / #99.3 [m2], terraza descubierta #43.2 / #41.0 [m2]; 01-03-BJ-A interior #101.3 / #101.8 [m2], jardín #41.8 / #41.5 [m2]; 02-04-BJ-C interior #92.9 / #92.8 [m2], construida #124.3 / #124.4 [m2], y una terraza descubierta de #29.4 [m2] en la lista frente a #3.0 [m2] rotulados en el plano, cuyo total exterior de #46.8 [m2] coincide con el de las dos terrazas de la lista; 03-07-BJ-A interior #89.8 / #91.2 [m2], jardín #175.6 / #173.8 [m2], terraza cubierta #23.4 / #23.5 [m2]; 03-07-BJ-C interior #72.5 / #73.0 [m2]. Las cifras de la 03-06-BJ-B y la 03-06-BJ-C son las mismas en ambos documentos.',
  'Les prix et surfaces sont transcrits de la liste de prix du promoteur à octobre 2026, qui recense avec un prix 7 des 80 logements et présente chacun comme disponible. La liste précise que les prix s’entendent hors TVA. La surface construite inclut une quote-part de parties communes ; la terrasse indiquée est la terrasse couverte et la terrasse découverte ensemble. Chaque logement est annoncé avec une cave et une place de garage, sauf les 03-06-BJ-C et 03-07-BJ-A, qui ont deux places de garage. Des plans sont fournis pour les sept logements. Lorsque la liste de prix et le plan du promoteur diffèrent, le tableau montre la liste de prix. Liste / plan : 01-01-BJ-A intérieur #75.4 / #75.8 [m2], construite #98.7 / #99.3 [m2], terrasse découverte #43.2 / #41.0 [m2] ; 01-03-BJ-A intérieur #101.3 / #101.8 [m2], jardin #41.8 / #41.5 [m2] ; 02-04-BJ-C intérieur #92.9 / #92.8 [m2], construite #124.3 / #124.4 [m2], et une terrasse découverte de #29.4 [m2] sur la liste contre #3.0 [m2] indiqués sur le plan, dont le total extérieur de #46.8 [m2] égale celui des deux terrasses de la liste ; 03-07-BJ-A intérieur #89.8 / #91.2 [m2], jardin #175.6 / #173.8 [m2], terrasse couverte #23.4 / #23.5 [m2] ; 03-07-BJ-C intérieur #72.5 / #73.0 [m2]. Les chiffres des 03-06-BJ-B et 03-06-BJ-C sont les mêmes dans les deux documents.',
  'Preise und Flächen sind der Preisliste des Bauträgers mit Stand Oktober 2026 entnommen, die 7 der 80 Wohnungen mit Preis aufführt und jede als verfügbar zeigt. Laut Liste verstehen sich die Preise zuzüglich MwSt. Die bebaute Fläche enthält einen Anteil an Gemeinschaftsflächen; die angegebene Terrasse ist die überdachte und die unüberdachte Terrasse zusammen. Jede Wohnung ist mit einem Abstellraum und einem Garagenstellplatz gelistet, außer 03-06-BJ-C und 03-07-BJ-A, die zwei Garagenstellplätze haben. Für alle sieben Wohnungen liegen Pläne vor. Wo Preisliste und Plan des Bauträgers abweichen, zeigt die Tabelle die Preisliste. Liste / Plan: 01-01-BJ-A Innenfläche #75.4 / #75.8 [m2], bebaut #98.7 / #99.3 [m2], unüberdachte Terrasse #43.2 / #41.0 [m2]; 01-03-BJ-A Innenfläche #101.3 / #101.8 [m2], Garten #41.8 / #41.5 [m2]; 02-04-BJ-C Innenfläche #92.9 / #92.8 [m2], bebaut #124.3 / #124.4 [m2], und eine unüberdachte Terrasse von #29.4 [m2] laut Liste gegenüber #3.0 [m2] im Plan, dessen Außenfläche von insgesamt #46.8 [m2] der Summe der beiden Terrassen der Liste entspricht; 03-07-BJ-A Innenfläche #89.8 / #91.2 [m2], Garten #175.6 / #173.8 [m2], überdachte Terrasse #23.4 / #23.5 [m2]; 03-07-BJ-C Innenfläche #72.5 / #73.0 [m2]. Die Zahlen für 03-06-BJ-B und 03-06-BJ-C sind in beiden Unterlagen gleich.',
  'Цены и площади перенесены из прайс-листа застройщика по состоянию на октябрь 2026 года, в котором указаны с ценой 7 из 80 квартир, и каждая показана как доступная. В прайс-листе сказано, что цены не включают НДС. Застроенная площадь включает долю общих зон; указанная терраса — это крытая и открытая террасы вместе. У каждой квартиры указаны кладовая и одно место в гараже, кроме 03-06-BJ-C и 03-07-BJ-A, у которых по два места в гараже. Планировки есть для всех семи квартир. Если прайс-лист и план застройщика расходятся, в таблице показан прайс-лист. Список / план: 01-01-BJ-A внутренняя площадь #75.4 / #75.8 [m2], застроенная #98.7 / #99.3 [m2], открытая терраса #43.2 / #41.0 [m2]; 01-03-BJ-A внутренняя площадь #101.3 / #101.8 [m2], сад #41.8 / #41.5 [m2]; 02-04-BJ-C внутренняя площадь #92.9 / #92.8 [m2], застроенная #124.3 / #124.4 [m2], а открытая терраса #29.4 [m2] в списке против #3.0 [m2], подписанных на плане, общая наружная площадь которого #46.8 [m2] равна сумме двух террас из списка; 03-07-BJ-A внутренняя площадь #89.8 / #91.2 [m2], сад #175.6 / #173.8 [m2], крытая терраса #23.4 / #23.5 [m2]; 03-07-BJ-C внутренняя площадь #72.5 / #73.0 [m2]. Цифры для 03-06-BJ-B и 03-06-BJ-C в обоих документах совпадают.',
  'الأسعار والمساحات منقولة من قائمة أسعار المطوّر بحسب وضعها في أكتوبر 2026، التي تدرج بسعر 7 من أصل 80 مسكنًا وتعرض كلًّا منها كمتاح. وتنص القائمة على أن الأسعار لا تشمل ضريبة القيمة المضافة. وتشمل المساحة المبنية حصة من المناطق المشتركة؛ والتراس المذكور هو التراس المغطى والمكشوف معًا. ويُدرج كل مسكن بغرفة تخزين وموقف سيارة واحد في المرآب، باستثناء 03-06-BJ-C و03-07-BJ-A اللذين لهما موقفان. وتتوفر مخططات للمساكن السبعة. وحيث تختلف قائمة الأسعار عن مخطط المطوّر يعرض الجدول قائمة الأسعار. القائمة / المخطط: 01-01-BJ-A المساحة الداخلية #75.4 / #75.8 [m2]، المبنية #98.7 / #99.3 [m2]، التراس المكشوف #43.2 / #41.0 [m2]؛ 01-03-BJ-A المساحة الداخلية #101.3 / #101.8 [m2]، الحديقة #41.8 / #41.5 [m2]؛ 02-04-BJ-C المساحة الداخلية #92.9 / #92.8 [m2]، المبنية #124.3 / #124.4 [m2]، وتراس مكشوف مساحته #29.4 [m2] في القائمة مقابل #3.0 [m2] مكتوبة على المخطط، ومجموع مساحته الخارجية #46.8 [m2] يساوي مجموع تراسي القائمة؛ 03-07-BJ-A المساحة الداخلية #89.8 / #91.2 [m2]، الحديقة #175.6 / #173.8 [m2]، التراس المغطى #23.4 / #23.5 [m2]؛ 03-07-BJ-C المساحة الداخلية #72.5 / #73.0 [m2]. أما أرقام 03-06-BJ-B و03-06-BJ-C فهي نفسها في الوثيقتين.',
  'Prijzen en oppervlakten zijn overgenomen uit de prijslijst van de ontwikkelaar met stand van oktober 2026, die 7 van de 80 woningen met een prijs vermeldt en elk als beschikbaar toont. De lijst vermeldt dat de prijzen exclusief btw zijn. De bebouwde oppervlakte bevat een aandeel in de gemeenschappelijke ruimten; het getoonde terras is het overdekte en het open terras samen. Elke woning staat vermeld met een berging en een garageplaats, behalve 03-06-BJ-C en 03-07-BJ-A, die twee garageplaatsen hebben. Er zijn plattegronden voor alle zeven woningen. Waar de prijslijst en de plattegrond van de ontwikkelaar verschillen, toont de tabel de prijslijst. Lijst / plattegrond: 01-01-BJ-A binnen #75.4 / #75.8 [m2], bebouwd #98.7 / #99.3 [m2], open terras #43.2 / #41.0 [m2]; 01-03-BJ-A binnen #101.3 / #101.8 [m2], tuin #41.8 / #41.5 [m2]; 02-04-BJ-C binnen #92.9 / #92.8 [m2], bebouwd #124.3 / #124.4 [m2], en een open terras van #29.4 [m2] volgens de lijst tegenover #3.0 [m2] op de plattegrond, waarvan het totaal buiten van #46.8 [m2] gelijk is aan dat van de twee terrassen op de lijst; 03-07-BJ-A binnen #89.8 / #91.2 [m2], tuin #175.6 / #173.8 [m2], overdekt terras #23.4 / #23.5 [m2]; 03-07-BJ-C binnen #72.5 / #73.0 [m2]. De cijfers voor 03-06-BJ-B en 03-06-BJ-C zijn in beide documenten gelijk.',
  'Ceny i powierzchnie przepisano z cennika dewelopera według stanu na październik 2026 r., który wymienia z ceną 7 z 80 lokali i pokazuje każdy jako dostępny. Cennik zastrzega, że ceny nie zawierają VAT. Powierzchnia zabudowy obejmuje udział w częściach wspólnych; podany taras to taras zadaszony i odkryty łącznie. Każdy lokal figuruje z komórką lokatorską i jednym miejscem w garażu, z wyjątkiem 03-06-BJ-C i 03-07-BJ-A, które mają po dwa miejsca. Rzuty są dostępne dla wszystkich siedmiu lokali. Tam, gdzie cennik i rzut dewelopera się różnią, tabela pokazuje cennik. Cennik / rzut: 01-01-BJ-A wnętrze #75.4 / #75.8 [m2], zabudowa #98.7 / #99.3 [m2], taras odkryty #43.2 / #41.0 [m2]; 01-03-BJ-A wnętrze #101.3 / #101.8 [m2], ogród #41.8 / #41.5 [m2]; 02-04-BJ-C wnętrze #92.9 / #92.8 [m2], zabudowa #124.3 / #124.4 [m2], oraz taras odkryty o powierzchni #29.4 [m2] w cenniku wobec #3.0 [m2] opisanych na rzucie, którego łączna powierzchnia zewnętrzna #46.8 [m2] odpowiada sumie dwóch tarasów z cennika; 03-07-BJ-A wnętrze #89.8 / #91.2 [m2], ogród #175.6 / #173.8 [m2], taras zadaszony #23.4 / #23.5 [m2]; 03-07-BJ-C wnętrze #72.5 / #73.0 [m2]. Wartości dla 03-06-BJ-B i 03-06-BJ-C są w obu dokumentach takie same.',
  'Priser og arealer er gjengitt fra utbyggerens prisliste per oktober 2026, som viser 7 av de 80 boligene med pris og oppgir hver som tilgjengelig. Listen oppgir at prisene er eksklusive mva. Det bebygde arealet inkluderer en andel av fellesarealene; den oppgitte terrassen er den overbygde og den åpne terrassen til sammen. Hver bolig er oppført med en bod og en garasjeplass, bortsett fra 03-06-BJ-C og 03-07-BJ-A, som har to garasjeplasser. Det finnes plantegninger for alle de sju boligene. Der prislisten og utbyggerens plantegning avviker, viser tabellen prislisten. Liste / plantegning: 01-01-BJ-A innvendig #75.4 / #75.8 [m2], bygd #98.7 / #99.3 [m2], åpen terrasse #43.2 / #41.0 [m2]; 01-03-BJ-A innvendig #101.3 / #101.8 [m2], hage #41.8 / #41.5 [m2]; 02-04-BJ-C innvendig #92.9 / #92.8 [m2], bygd #124.3 / #124.4 [m2], og en åpen terrasse på #29.4 [m2] i listen mot #3.0 [m2] påført plantegningen, hvis samlede uteareal på #46.8 [m2] tilsvarer de to terrassene i listen; 03-07-BJ-A innvendig #89.8 / #91.2 [m2], hage #175.6 / #173.8 [m2], overbygd terrasse #23.4 / #23.5 [m2]; 03-07-BJ-C innvendig #72.5 / #73.0 [m2]. Tallene for 03-06-BJ-B og 03-06-BJ-C er de samme i begge dokumentene.',
  'Priser och ytor är hämtade från exploatörens prislista per oktober 2026, som listar 7 av de 80 bostäderna med pris och visar var och en som tillgänglig. Listan anger att priserna är exklusive moms. Den byggda ytan inkluderar en andel av de gemensamma ytorna; den angivna terrassen är den övertäckta och den öppna terrassen tillsammans. Varje bostad är listad med ett förråd och en garageplats, utom 03-06-BJ-C och 03-07-BJ-A, som har två garageplatser. Planritningar finns för alla sju bostäder. Där prislistan och exploatörens planritning skiljer sig åt visar tabellen prislistan. Lista / planritning: 01-01-BJ-A inomhus #75.4 / #75.8 [m2], byggyta #98.7 / #99.3 [m2], öppen terrass #43.2 / #41.0 [m2]; 01-03-BJ-A inomhus #101.3 / #101.8 [m2], trädgård #41.8 / #41.5 [m2]; 02-04-BJ-C inomhus #92.9 / #92.8 [m2], byggyta #124.3 / #124.4 [m2], och en öppen terrass på #29.4 [m2] i listan mot #3.0 [m2] angivna på planritningen, vars totala utomhusyta på #46.8 [m2] motsvarar de två terrasserna i listan; 03-07-BJ-A inomhus #89.8 / #91.2 [m2], trädgård #175.6 / #173.8 [m2], övertäckt terrass #23.4 / #23.5 [m2]; 03-07-BJ-C inomhus #72.5 / #73.0 [m2]. Siffrorna för 03-06-BJ-B och 03-06-BJ-C är desamma i båda dokumenten.')

# ---- timeline, viewing, enquiry, faq ------------------------------------------------------
p('.timeline.items[3][2]',  # 139
  'Una reserva de €6600 y después el contrato privado de compraventa, con la garantía de los pagos a cuenta confirmada por escrito antes.',
  'Une réservation de €6600, puis le contrat de vente privé, avec la garantie des acomptes confirmée par écrit au préalable.',
  'Eine Reservierung von €6600, dann der private Kaufvertrag, wobei die Absicherung der Anzahlungen vorab schriftlich bestätigt wird.',
  'Бронирование €6600, затем предварительный договор купли-продажи; гарантия авансовых платежей предварительно подтверждается письменно.',
  'حجز بمبلغ €6600، ثم عقد الشراء الخاص، مع تأكيد ضمان المدفوعات المقدمة كتابةً قبل ذلك.',
  'Een reservering van €6600, daarna de onderhandse koopovereenkomst, waarbij de waarborg voor de vooruitbetalingen eerst schriftelijk wordt bevestigd.',
  'Rezerwacja €6600, następnie umowa przedwstępna, przy czym zabezpieczenie zaliczek jest wcześniej potwierdzane na piśmie.',
  'En reservasjon på €6600, deretter den private kjøpekontrakten, med garantien for forskuddsbetalingene bekreftet skriftlig først.',
  'En reservation på €6600, sedan det privata köpeavtalet, med garantin för förskottsbetalningarna bekräftad skriftligen först.')
p('.privateViewing.copy',  # 140
  'Las viviendas aún no están construidas, así que la visita trata de la ubicación, los planos y el calendario.',
  'Les logements ne sont pas encore construits ; la visite porte donc sur l’emplacement, les plans et le calendrier.',
  'Die Wohnungen sind noch nicht gebaut, daher geht es beim Besuch um die Lage, die Pläne und den Zeitplan.',
  'Квартиры ещё не построены, поэтому просмотр посвящён расположению, планировкам и срокам.',
  'المساكن لم تُبنَ بعد، لذا تتركز المعاينة على الموقع والمخططات والجدول الزمني.',
  'De woningen zijn nog niet gebouwd, dus een bezoek gaat over de ligging, de plattegronden en de planning.',
  'Lokale nie są jeszcze zbudowane, więc wizyta dotyczy lokalizacji, rzutów i harmonogramu.',
  'Boligene er ikke bygget ennå, så en visning handler om beliggenheten, plantegningene og tidsplanen.',
  'Bostäderna är inte byggda än, så ett besök handlar om läget, planritningarna och tidsplanen.')
p('.privateViewing.insights[0][1]',  # 141
  'Recorra la zona alrededor de la parcela y vea dónde están los campos de golf y el mar.',
  'Parcourez les environs de la parcelle et voyez où se trouvent les golfs et la mer.',
  'Gehen Sie die Umgebung des Grundstücks ab und sehen Sie, wo die Golfplätze und das Meer liegen.',
  'Пройдитесь по окрестностям участка и посмотрите, где находятся поля для гольфа и море.',
  'تجوّل في المنطقة المحيطة بأرض المشروع وانظر أين تقع ملاعب الغولف والبحر.',
  'Loop door de omgeving van het perceel en zie waar de golfbanen en de zee liggen.',
  'Spacer po okolicy działki i sprawdzenie, gdzie leżą pola golfowe i morze.',
  'Gå rundt i området rundt tomten og se hvor golfbanene og havet ligger.',
  'Gå runt i området kring tomten och se var golfbanorna och havet ligger.')
p('.privateViewing.insights[1][1]',  # 142
  'Vamos en coche con usted a Estepona, a Puerto Banús y a la playa y cronometramos el trayecto.',
  'Nous vous emmenons en voiture à Estepona, à Puerto Banús et à la plage, et nous chronométrons le trajet.',
  'Wir fahren mit Ihnen nach Estepona, nach Puerto Banús und zum Strand und messen die Zeit.',
  'Мы отвезём вас в Эстепону, Пуэрто-Банус и на пляж и засечём время в пути.',
  'نرافقكم بالسيارة إلى إستيبونا وبويرتو بانوس والشاطئ ونقيس زمن الوصول.',
  'We rijden met u naar Estepona, Puerto Banús en het strand en meten de reistijd.',
  'Jedziemy z Państwem do Estepony, Puerto Banús i na plażę, mierząc czas dojazdu.',
  'Vi kjører sammen til Estepona, Puerto Banús og stranden og tar tiden.',
  'Vi åker med er till Estepona, Puerto Banús och stranden och tar tiden.')
p('.privateViewing.insights[2][1]',  # 143
  'Disponibilidad, licencia y contrato, antes de firmar nada.',
  'Disponibilité, permis et contrat, avant toute signature.',
  'Verfügbarkeit, Genehmigung und Vertrag, bevor etwas unterschrieben wird.',
  'Наличие, разрешение и договор — до подписания любых бумаг.',
  'التوفر والرخصة والعقد، قبل توقيع أي شيء.',
  'Beschikbaarheid, vergunning en contract, voordat er iets wordt ondertekend.',
  'Dostępność, pozwolenie i umowa, zanim cokolwiek zostanie podpisane.',
  'Tilgjengelighet, tillatelse og kontrakt, før noe signeres.',
  'Tillgänglighet, bygglov och avtal, innan något undertecknas.')
p('.enquiry.headlineHtml',  # 144
  'Pregunte por <em>Levante Residences</em>',
  'Renseignez-vous sur <em>Levante Residences</em>',
  'Fragen Sie nach <em>Levante Residences</em>',
  'Узнайте о <em>Levante Residences</em>',
  'استفسر عن <em>Levante Residences</em>',
  'Vraag naar <em>Levante Residences</em>',
  'Zapytanie o <em>Levante Residences</em>',
  'Spør om <em>Levante Residences</em>',
  'Fråga om <em>Levante Residences</em>')
p('.enquiry.message',  # 145
  'Hola, Nueva Living, me gustaría recibir información sobre Levante Residences.',
  'Bonjour Nueva Living, je souhaiterais des informations sur Levante Residences.',
  'Guten Tag Nueva Living, ich möchte Informationen zu Levante Residences erhalten.',
  'Здравствуйте, Nueva Living! Хочу получить информацию о Levante Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Levante Residences.',
  'Goedendag Nueva Living, ik wil graag informatie over Levante Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje o Levante Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Levante Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Levante Residences.')
p('.faq[0][1]',  # 146
  'La promoción tiene 80 viviendas de dos o tres dormitorios. La lista de precios recoge siete de ellas, todas disponibles, de €442000 a €633000 más IVA: tres de dos dormitorios, tres de tres dormitorios en una planta y un dúplex de tres dormitorios.',
  'Le programme compte 80 logements de deux ou trois chambres. La liste de prix en recense sept, tous disponibles, de €442000 à €633000 hors TVA : trois de deux chambres, trois de trois chambres de plain-pied et un duplex de trois chambres.',
  'Die Anlage hat 80 Wohnungen mit zwei oder drei Schlafzimmern. Die Preisliste nennt sieben davon, alle verfügbar, von €442000 bis €633000 zuzüglich MwSt.: drei mit zwei Schlafzimmern, drei mit drei Schlafzimmern auf einer Ebene und eine Maisonette mit drei Schlafzimmern.',
  'В комплексе 80 квартир с двумя или тремя спальнями. В прайс-листе указаны семь из них, все доступные, от €442000 до €633000 без НДС: три с двумя спальнями, три с тремя спальнями на одном уровне и один дуплекс с тремя спальнями.',
  'يضم المشروع 80 مسكنًا من غرفتي نوم أو ثلاث غرف نوم. وتدرج قائمة الأسعار سبعة منها، كلها متاحة، من €442000 إلى €633000 دون ضريبة القيمة المضافة: ثلاثة من غرفتي نوم وثلاثة من ثلاث غرف نوم على مستوى واحد ودوبلكس من ثلاث غرف نوم.',
  'Het project heeft 80 woningen met twee of drie slaapkamers. De prijslijst noemt er zeven, allemaal beschikbaar, van €442000 tot €633000 excl. btw: drie met twee slaapkamers, drie met drie slaapkamers op één niveau en een duplex met drie slaapkamers.',
  'Inwestycja liczy 80 lokali z dwiema lub trzema sypialniami. Cennik wymienia siedem z nich, wszystkie dostępne, od €442000 do €633000 plus VAT: trzy z dwiema sypialniami, trzy z trzema sypialniami na jednym poziomie i jedno dwupoziomowe z trzema sypialniami.',
  'Prosjektet har 80 boliger med to eller tre soverom. Prislisten viser sju av dem, alle tilgjengelige, fra €442000 til €633000 pluss mva.: tre med to soverom, tre med tre soverom på ett plan og en duplex med tre soverom.',
  'Projektet har 80 bostäder med två eller tre sovrum. Prislistan upptar sju av dem, alla tillgängliga, från €442000 till €633000 plus moms: tre med två sovrum, tre med tre sovrum på ett plan och en etagelägenhet med tre sovrum.')
p('.faq[1][1]',  # 147
  'No. La lista de precios indica que los precios no incluyen el IVA. Confirmamos por escrito los impuestos y los gastos de compra.',
  'Non. La liste de prix indique que les prix s’entendent hors TVA. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Laut Preisliste verstehen sich die Preise zuzüglich MwSt. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе сказано, что цены не включают НДС. Налоги и расходы на покупку мы письменно подтверждаем.',
  'لا. تذكر قائمة الأسعار أن الأسعار لا تشمل ضريبة القيمة المضافة. ونؤكد الضرائب ومصاريف الشراء كتابةً.',
  'Nee. De prijslijst vermeldt dat de prijzen exclusief btw zijn. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Nie. Cennik podaje, że ceny nie zawierają VAT. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Prislisten oppgir at prisene er eksklusive mva. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Nej. Prislistan anger att priserna är exklusive moms. Vi bekräftar skatter och köpkostnader skriftligen.')
p('.faq[2][0]',  # 148
  '¿Están incluidos un garaje y un trastero?', 'Un garage et une cave sont-ils inclus ?', 'Sind ein Garagenstellplatz und ein Abstellraum enthalten?',
  'Входят ли в цену место в гараже и кладовая?', 'هل المرآب وغرفة التخزين مشمولان؟', 'Zijn een garageplaats en een berging inbegrepen?',
  'Czy miejsce w garażu i komórka lokatorska są wliczone?', 'Er en garasjeplass og en bod inkludert?', 'Ingår en garageplats och ett förråd?')
p('.faq[2][1]',  # 149
  'La lista de precios muestra un trastero y una plaza de garaje por cada vivienda de la lista, y dos plazas de garaje en dos de ellas. Confirmamos que están incluidos en el precio.',
  'La liste de prix indique une cave et une place de garage pour chaque logement de la liste, et deux places de garage pour deux d’entre eux. Nous confirmons qu’ils sont inclus dans le prix.',
  'Die Preisliste weist für jede gelistete Wohnung einen Abstellraum und einen Garagenstellplatz aus, für zwei davon zwei Garagenstellplätze. Wir bestätigen, dass sie im Preis enthalten sind.',
  'В прайс-листе для каждой квартиры из списка указаны кладовая и одно место в гараже, а у двух из них — по два места. Мы подтверждаем, что они входят в цену.',
  'تُظهر قائمة الأسعار غرفة تخزين وموقف سيارة واحدًا في المرآب لكل مسكن مدرج، وموقفين في اثنين منها. ونؤكد أنها مشمولة في السعر.',
  'De prijslijst toont voor elke vermelde woning een berging en een garageplaats, en voor twee ervan twee garageplaatsen. We bevestigen dat ze in de prijs zijn begrepen.',
  'Cennik podaje dla każdego lokalu z listy komórkę lokatorską i jedno miejsce w garażu, a dla dwóch z nich dwa miejsca. Potwierdzamy, że są wliczone w cenę.',
  'Prislisten viser en bod og en garasjeplass for hver bolig på listen, og to garasjeplasser for to av dem. Vi bekrefter at de er inkludert i prisen.',
  'Prislistan anger ett förråd och en garageplats för varje bostad på listan, och två garageplatser för två av dem. Vi bekräftar att de ingår i priset.')
p('.faq[3][1]',  # 150
  'El anuncio del promotor da la entrega en abril de 2028. Los documentos que tenemos no indican la licencia de obras ni el estado de las obras, por lo que pedimos la licencia y la fecha contractual.',
  'L’annonce du promoteur indique une livraison en avril 2028. Les documents dont nous disposons ne donnent ni le permis de construire ni l’état des travaux ; nous demandons donc le permis et la date contractuelle.',
  'Der Bauträger gibt die Übergabe für April 2028 an. Die uns vorliegenden Unterlagen nennen weder eine Baugenehmigung noch einen Baustand, daher fragen wir die Genehmigung und das vertragliche Datum an.',
  'Застройщик указывает срок сдачи — апрель 2028 года. В имеющихся у нас документах нет ни разрешения на строительство, ни сведений о ходе работ, поэтому мы запрашиваем разрешение и договорную дату.',
  'يذكر إعلان المطوّر موعد التسليم في أبريل 2028. ولا تذكر الوثائق التي بحوزتنا رخصة البناء ولا حالة الأعمال، لذلك نطلب الرخصة والتاريخ التعاقدي.',
  'De vermelding van de ontwikkelaar noemt april 2028 als opleveringsdatum. In de documenten waarover we beschikken staat geen bouwvergunning of stand van de werken, dus we vragen de vergunning en de contractuele datum.',
  'Deweloper podaje termin oddania na kwiecień 2028 r. W posiadanych przez nas dokumentach nie ma pozwolenia na budowę ani informacji o stanie prac, dlatego prosimy o pozwolenie i termin wskazany w umowie.',
  'Utbyggeren oppgir overtakelse i april 2028. Dokumentene vi har oppgir verken byggetillatelse eller status for arbeidene, så vi ber om tillatelsen og den kontraktsfestede datoen.',
  'Exploatören anger tillträde i april 2028. Dokumenten vi har anger varken bygglov eller status för byggarbetena, så vi ber om bygglovet och det avtalade datumet.')
p('.faq[4][1]',  # 151
  'La reserva es de €6600, con el IVA incluido. Luego, el 30% más IVA con el contrato privado y el 70% más IVA ante notario a la finalización.',
  'La réservation est de €6600, TVA incluse. Ensuite, 30 % hors TVA au contrat privé et 70 % hors TVA chez le notaire à l’achèvement.',
  'Die Reservierung beträgt €6600, einschließlich MwSt. Dann 30 % zuzüglich MwSt. bei Unterzeichnung des privaten Vertrags und 70 % zuzüglich MwSt. bei Fertigstellung beim Notar.',
  'Бронирование стоит €6600 с учётом НДС. Затем 30 % плюс НДС при подписании предварительного договора и 70 % плюс НДС у нотариуса при завершении сделки.',
  'الحجز €6600 شاملًا ضريبة القيمة المضافة. ثم 30% زائد ضريبة القيمة المضافة عند العقد الخاص، و70% زائد الضريبة أمام كاتب العدل عند الإتمام.',
  'De reservering bedraagt €6600, inclusief btw. Daarna 30% plus btw bij de onderhandse overeenkomst en 70% plus btw bij oplevering ten overstaan van de notaris.',
  'Rezerwacja wynosi €6600 (z VAT). Następnie 30% plus VAT przy podpisaniu umowy przedwstępnej i 70% plus VAT u notariusza, przy akcie notarialnym.',
  'Reservasjonen er €6600, inkludert mva. Deretter 30 % pluss mva. ved den private kontrakten og 70 % pluss mva. hos notarius ved overtakelse.',
  'Reservationen är €6600, inklusive moms. Därefter 30 % plus moms vid det privata avtalet och 70 % plus moms hos notarien vid tillträdet.')
p('.faq[5][1]',  # 152
  'Una piscina comunitaria, un gimnasio equipado, una zona deportiva exterior y zen y jardines paisajísticos, además de una casa club con spa, sauna, gimnasio y salas comunitarias que, según el dossier, se adquiere junto con la vivienda.',
  'Une piscine commune, une salle de sport équipée, un espace sportif extérieur et zen et des jardins paysagers, ainsi qu’un club-house avec spa, sauna, salle de sport et salles communes que la brochure dit acquis avec le logement.',
  'Ein Gemeinschaftspool, ein ausgestatteter Fitnessraum, ein Sport- und Zen-Bereich im Freien und gestaltete Gärten, dazu ein Clubhaus mit Spa, Sauna, Fitnessraum und Gemeinschaftsräumen, das laut Broschüre zusammen mit der Wohnung erworben wird.',
  'Общий бассейн, оборудованный тренажёрный зал, спортивная площадка и зона дзен на открытом воздухе и благоустроенные сады, а также клубный дом со спа, сауной, тренажёрным залом и общими залами, который, по словам брошюры, приобретается вместе с квартирой.',
  'مسبح مشترك وصالة رياضية مجهزة ومنطقة رياضية وزِن في الهواء الطلق وحدائق منسقة، إضافة إلى نادي المجمع بسبا وساونا وصالة رياضية وقاعات مشتركة، ويُشترى مع المسكن بحسب الكتيّب.',
  'Een gemeenschappelijk zwembad, een uitgeruste fitnessruimte, een sport- en zenzone buiten en aangelegde tuinen, plus een clubhuis met spa, sauna, fitnessruimte en gemeenschappelijke ruimten dat volgens de brochure samen met de woning wordt gekocht.',
  'Wspólny basen, wyposażona siłownia, zewnętrzna strefa sportowa i strefa zen oraz zaaranżowane ogrody, a także klub ze strefą spa, sauną, siłownią i salami wspólnymi, który według broszury nabywa się razem z lokalem.',
  'Et felles basseng, et utstyrt treningsrom, et utendørs sports- og zenområde og anlagte hager, i tillegg til et klubbhus med spa, badstue, treningsrom og fellesrom som ifølge brosjyren kjøpes sammen med boligen.',
  'En gemensam pool, ett utrustat gym, en idrotts- och zenzon utomhus och anlagda trädgårdar, plus ett klubbhus med spa, bastu, gym och gemensamma rum som enligt broschyren köps tillsammans med bostaden.')

missing = [pa for pa in BY_PATH if pa not in USED]
if missing:
    print('NOT COVERED', len(missing)); [print('  ', m, BY_PATH[m][:80]) for m in missing]
json.dump(T, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
