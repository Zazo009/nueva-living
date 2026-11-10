# -*- coding: utf-8 -*-
"""Estepona West Golf Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_w.json keyed by the English string, as assemble.py expects. Tokens: {E473000}
money, {N66.91} decimal number, {U} the area unit, {T} the tax word.
    python3 tools/import/k_estepona_west_golf_residences.py <scratch dir>   (writes <dir>/tr_w.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة',
        'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
T = {}
SLUG = 'estepona-west-golf-residences'
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


# render prefix per locale: the description that follows carries its own connector (de, d’, van, av ...)
CGP = {'es': 'Vista generada por ordenador ', 'fr': 'Vue générée par ordinateur ', 'de': 'Computergenerierte Ansicht ',
       'ru': 'Компьютерная визуализация ', 'ar': 'منظر مولَّد بالحاسوب ', 'nl': 'Computergegenereerd beeld ',
       'pl': 'Wygenerowany komputerowo widok ', 'no': 'Datagenerert bilde ', 'sv': 'Datorgenererad vy '}


def cg(path, *tr):
    assert len(tr) == 9, path
    en = get(path)
    assert en.startswith('Computer-generated view '), en
    put(en, [CGP[l] + t for l, t in zip(LOCS, tr)])


same(get('.name')); same(get('.shortName')); same(get('.titleHtml'))
for u in proj['availability']['units']:
    same(u['reference'])

# ---- description, SEO, hero, card -------------------------------------------------------------

a('.description',
  'Apartamentos de dos y tres dormitorios con terrazas en Estepona, muy cerca de campos de golf, con un spa interior con piscina climatizada, un gimnasio y una sala de coworking. 17 de las 19 viviendas de la lista de precios del promotor de noviembre de 2026 están disponibles, desde {E473000} antes de {T}.',
  'Appartements de deux et trois chambres avec terrasses à Estepona, tout près de terrains de golf, avec un spa intérieur doté d’une piscine chauffée, une salle de sport et un espace de coworking. 17 des 19 logements de la liste de prix du promoteur de novembre 2026 sont disponibles, à partir de {E473000} hors {T}.',
  'Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Estepona, ganz in der Nähe von Golfplätzen, mit einem Indoor-Spa mit beheiztem Pool, einem Fitnessraum und einem Coworking-Raum. 17 der 19 Wohnungen auf der Preisliste des Bauträgers vom November 2026 sind verfügbar, ab {E473000} vor {T}.',
  'Апартаменты с двумя и тремя спальнями и террасами в Эстепоне, совсем рядом с полями для гольфа, со спа в помещении с подогреваемым бассейном, тренажёрным залом и коворкингом. 17 из 19 квартир в прайс-листе застройщика за ноябрь 2026 года доступны, от {E473000} без {T}.',
  'شقق بغرفتي نوم وثلاث غرف نوم مع تراسات في إستيبونا، على مقربة شديدة من ملاعب الغولف، مع سبا داخلي بمسبح مدفأ وصالة رياضية وقاعة للعمل المشترك. 17 من أصل 19 مسكنًا في قائمة أسعار المطوّر لشهر نوفمبر 2026 متاحة، ابتداءً من {E473000} قبل {T}.',
  'Appartementen met twee en drie slaapkamers en terrassen in Estepona, vlak bij golfbanen, met een binnenspa met verwarmd zwembad, een fitnessruimte en een coworkingruimte. 17 van de 19 woningen op de prijslijst van de ontwikkelaar van november 2026 zijn beschikbaar, vanaf {E473000} exclusief {T}.',
  'Apartamenty z dwiema i trzema sypialniami oraz tarasami w Esteponie, tuż przy polach golfowych, ze spa w budynku z podgrzewanym basenem, siłownią i salą coworkingową. 17 z 19 lokali w cenniku dewelopera z listopada 2026 roku jest dostępnych, od {E473000} bez {T}.',
  'Leiligheter med to og tre soverom og terrasser i Estepona, helt nær golfbaner, med et innendørs spa med oppvarmet basseng, et treningsrom og et coworking-rom. 17 av de 19 boligene i utbyggerens prisliste fra november 2026 er ledige, fra {E473000} før {T}.',
  'Lägenheter med två och tre sovrum och terrasser i Estepona, mycket nära golfbanor, med ett inomhusspa med uppvärmd pool, ett gym och ett coworking-rum. 17 av de 19 bostäderna i exploatörens prislista från november 2026 är lediga, från {E473000} före {T}.')
a('.seoDescription',
  'Apartamentos nuevos de dos y tres dormitorios con terrazas en Estepona, cerca de campos de golf, con spa interior, gimnasio y sala de coworking. 17 de 19 viviendas listadas disponibles desde {E473000} más {T}.',
  'Appartements neufs de deux et trois chambres avec terrasses à Estepona, près de terrains de golf, avec spa intérieur, salle de sport et espace de coworking. 17 logements listés sur 19 disponibles à partir de {E473000} hors {T}.',
  'Neue Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Estepona, nahe Golfplätzen, mit Indoor-Spa, Fitnessraum und Coworking-Raum. 17 von 19 gelisteten Wohnungen verfügbar, ab {E473000} zuzüglich {T}.',
  'Новые апартаменты с двумя и тремя спальнями и террасами в Эстепоне, рядом с полями для гольфа, со спа, тренажёрным залом и коворкингом. Доступны 17 из 19 квартир списка, от {E473000} плюс {T}.',
  'شقق جديدة بغرفتي نوم وثلاث غرف نوم مع تراسات في إستيبونا، قرب ملاعب الغولف، مع سبا داخلي وصالة رياضية وقاعة للعمل المشترك. 17 من 19 مسكنًا مدرجًا متاحة، ابتداءً من {E473000} زائد {T}.',
  'Nieuwe appartementen met twee en drie slaapkamers en terrassen in Estepona, vlak bij golfbanen, met binnenspa, fitnessruimte en coworkingruimte. 17 van de 19 vermelde woningen beschikbaar vanaf {E473000} plus {T}.',
  'Nowe apartamenty z dwiema i trzema sypialniami oraz tarasami w Esteponie, blisko pól golfowych, ze spa, siłownią i salą coworkingową. Dostępnych jest 17 z 19 lokali z listy, od {E473000} plus {T}.',
  'Nye leiligheter med to og tre soverom og terrasser i Estepona, nær golfbaner, med innendørs spa, treningsrom og coworking-rom. 17 av 19 oppførte boliger er ledige fra {E473000} pluss {T}.',
  'Nya lägenheter med två och tre sovrum och terrasser i Estepona, nära golfbanor, med inomhusspa, gym och coworking-rum. 17 av 19 listade bostäder är lediga från {E473000} plus {T}.')
a('.twitterDescription',
  'Apartamentos de dos y tres dormitorios con terrazas en Estepona, desde {E473000} más {T}.',
  'Appartements de deux et trois chambres avec terrasses à Estepona, à partir de {E473000} hors {T}.',
  'Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Estepona, ab {E473000} zuzüglich {T}.',
  'Апартаменты с двумя и тремя спальнями и террасами в Эстепоне, от {E473000} плюс {T}.',
  'شقق بغرفتي نوم وثلاث غرف نوم مع تراسات في إستيبونا، ابتداءً من {E473000} زائد {T}.',
  'Appartementen met twee en drie slaapkamers en terrassen in Estepona, vanaf {E473000} plus {T}.',
  'Apartamenty z dwiema i trzema sypialniami oraz tarasami w Esteponie, od {E473000} plus {T}.',
  'Leiligheter med to og tre soverom og terrasser i Estepona, fra {E473000} pluss {T}.',
  'Lägenheter med två och tre sovrum och terrasser i Estepona, från {E473000} plus {T}.')
a('.hero.eyebrow',
  '17 de 19 viviendas de la lista disponibles', '17 logements sur 19 listés disponibles', '17 von 19 aufgeführten Wohnungen verfügbar',
  '17 из 19 квартир списка доступны', '17 من أصل 19 مسكنًا مدرجًا متاحة', '17 van de 19 vermelde woningen beschikbaar',
  '17 z 19 wymienionych lokali dostępnych', '17 av 19 oppførte boliger tilgjengelige', '17 av 19 listade bostäder tillgängliga')
a('.hero.startingPrice',
  'Desde {E473000} + {T}', 'À partir de {E473000} + {T}', 'Ab {E473000} + {T}', 'От {E473000} + {T}', 'ابتداءً من {E473000} + {T}',
  'Vanaf {E473000} + {T}', 'Od {E473000} + {T}', 'Fra {E473000} + mva.', 'Från {E473000} + {T}')
a('.card.description',
  '17 de 19 apartamentos de dos y tres dormitorios con terrazas en Estepona, con spa interior, gimnasio y sala de coworking, desde {E473000} + {T}.',
  '17 appartements de deux et trois chambres avec terrasses sur 19 listés à Estepona, avec spa intérieur, salle de sport et espace de coworking, à partir de {E473000} + {T}.',
  '17 von 19 aufgeführten Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Estepona, mit Indoor-Spa, Fitnessraum und Coworking-Raum, ab {E473000} + {T}.',
  '17 из 19 квартир с двумя и тремя спальнями и террасами в Эстепоне, со спа в помещении, тренажёрным залом и коворкингом, от {E473000} + {T}.',
  '17 من أصل 19 شقة مدرجة بغرفتي نوم وثلاث غرف نوم مع تراسات في إستيبونا، مع سبا داخلي وصالة رياضية وقاعة للعمل المشترك، ابتداءً من {E473000} + {T}.',
  '17 van de 19 vermelde appartementen met twee en drie slaapkamers en terrassen in Estepona, met een binnenspa, een fitnessruimte en een coworkingruimte, vanaf {E473000} + {T}.',
  '17 z 19 wymienionych mieszkań z dwiema i trzema sypialniami oraz tarasami w Esteponie, ze spa w budynku, siłownią i salą coworkingową, od {E473000} + {T}.',
  '17 av 19 oppførte leiligheter med to og tre soverom og terrasser i Estepona, med innendørs spa, treningsrom og coworking-rom, fra {E473000} + mva.',
  '17 av 19 listade lägenheter med två och tre sovrum och terrasser i Estepona, med inomhusspa, gym och coworking-rum, från {E473000} + {T}.')
a('.card.meta[0][1]',
  '{E473000} + {T}', '{E473000} + {T}', '{E473000} + {T}', '{E473000} + {T}', '{E473000} + {T}', '{E473000} + {T}', '{E473000} + {T}',
  '{E473000} + mva.', '{E473000} + {T}')

# ---- image alt text (hero, architecture, lifestyle, private viewing) ------------------------------

a('.images.hero.alt',
  'Vista aérea generada por ordenador de bloques en terrazas sobre una ladera en torno a dos piscinas, con un campo de golf junto al solar y la costa al fondo',
  'Vue aérienne générée par ordinateur de blocs en terrasses sur un coteau autour de deux piscines, avec un terrain de golf à côté du site et la côte au loin',
  'Computergenerierte Luftaufnahme von terrassierten Blöcken an einem Hang um zwei Pools, mit einem Golfplatz neben dem Grundstück und der Küste dahinter',
  'Компьютерная визуализация с высоты птичьего полёта: террасные корпуса на склоне вокруг двух бассейнов, рядом с участком поле для гольфа, а вдали побережье',
  'منظر جوي مولَّد بالحاسوب لمبانٍ مدرَّجة على سفح تلة حول مسبحين، مع ملعب غولف بجانب الموقع والساحل في الأفق',
  'Computergegenereerd luchtbeeld van terrasvormige blokken op een helling rond twee zwembaden, met een golfbaan naast het terrein en de kust erachter',
  'Wygenerowany komputerowo widok z lotu ptaka na tarasowe budynki na zboczu wokół dwóch basenów, z polem golfowym obok działki i wybrzeżem w tle',
  'Datagenerert flyfoto av terrassebygg i en skråning rundt to basseng, med en golfbane ved siden av tomten og kysten bak',
  'Datorgenererad flygvy av terrasserade hus i en sluttning kring två pooler, med en golfbana intill tomten och kusten bortom')
cg('.images.architecture.alt',
   'desde la carretera de bloques en terrazas con forjados curvos, barandillas de vidrio y falsos techos de madera sobre un muro de piedra y una entrada de garaje',
   'depuis la route de blocs en terrasses aux dalles courbes, garde-corps en verre et sous-faces en bois, au-dessus d’un mur de pierre et d’une entrée de garage',
   'von der Straße auf terrassierte Blöcke mit geschwungenen Decken, Glasbrüstungen und Holzuntersichten über einer Steinmauer und einer Garageneinfahrt',
   'с дороги на террасные корпуса с изогнутыми плитами, стеклянными ограждениями и деревянной подшивкой над каменной стеной и въездом в гараж',
   'من الطريق لمبانٍ مدرَّجة ذات بلاطات منحنية وحواجز زجاجية وأسقف خشبية فوق جدار حجري ومدخل مرآب',
   'vanaf de weg van terrasvormige blokken met gebogen platen, glazen balustrades en houten plafonds boven een stenen muur en een garage-ingang',
   'z drogi na tarasowe budynki z zakrzywionymi płytami, szklanymi balustradami i drewnianymi podsufitkami nad kamiennym murem i wjazdem do garażu',
   'fra veien av terrassebygg med buede plater, glassrekkverk og trehimlinger over en steinmur og en garasjeinnkjøring',
   'från vägen av terrasserade hus med böjda plattor, glasräcken och trätak ovanför en stenmur och en garageinfart')
cg('.images.lifestyle.alt',
   'del spa interior, una piscina climatizada con chorros en la pared, tumbonas junto a un muro de piedra y dos huéspedes en albornoz',
   'du spa intérieur, d’une piscine chauffée avec jets muraux, de transats le long d’un mur de pierre et de deux personnes en peignoir',
   'des Indoor-Spas, eines beheizten Pools mit Wanddüsen, von Liegen an einer Steinmauer und von zwei Gästen im Bademantel',
   'спа в помещении: подогреваемый бассейн с настенными форсунками, шезлонги вдоль каменной стены и двое гостей в халатах',
   'للسبا الداخلي، مع مسبح مدفأ بنفاثات جدارية وكراسٍ للاستلقاء بمحاذاة جدار حجري وضيفين برداءي حمام',
   'van de binnenspa, een verwarmd zwembad met wandstralen, ligbedden langs een stenen muur en twee gasten in badjas',
   'spa w budynku: podgrzewanego basenu z dyszami w ścianie, leżaków wzdłuż kamiennej ściany i dwóch gości w szlafrokach',
   'av innendørs spaet, et oppvarmet basseng med veggdyser, solsenger langs en steinmur og to gjester i badekåpe',
   'av inomhusspat, en uppvärmd pool med väggmunstycken, solstolar längs en stenmur och två gäster i badrock')
cg('.images.privateViewing.alt',
   'de una terraza cubierta con mesa de comedor, sillones y un sofá rinconero, con vistas a las colinas y al mar',
   'd’une terrasse couverte avec une table à manger, des fauteuils et un canapé d’angle, avec vue sur les collines et la mer',
   'einer überdachten Terrasse mit Esstisch, Sesseln und einem Ecksofa, mit Blick über die Hügel zum Meer',
   'крытой террасы с обеденным столом, креслами и угловым диваном, с видом на холмы и море',
   'لتراس مسقوف مع طاولة طعام ومقاعد وأريكة زاوية، مع إطلالة على التلال والبحر',
   'van een overdekt terras met een eettafel, fauteuils en een hoekbank, met uitzicht over de heuvels op de zee',
   'tarasu zadaszonego ze stołem jadalnianym, fotelami i narożną sofą, z widokiem na wzgórza i morze',
   'av en overbygd terrasse med spisebord, lenestoler og en hjørnesofa, med utsikt over åsene til havet',
   'av en övertäckt terrass med matbord, fåtöljer och en hörnsoffa, med utsikt över kullarna mot havet')

# ---- media ------------------------------------------------------------------------------------

a('.media.copy',
  'Vistas generadas por ordenador de los bloques, las piscinas, el spa, las terrazas y los interiores, del folleto y del conjunto de imágenes del promotor, y los planos de cinco de las 17 viviendas de la lista de precios.',
  'Vues générées par ordinateur des blocs, des piscines, du spa, des terrasses et des intérieurs, tirées de la brochure et du jeu d’images du promoteur, et plans de cinq des 17 logements de la liste de prix.',
  'Computergenerierte Ansichten der Blöcke, der Pools, des Spas, der Terrassen und der Innenräume aus der Broschüre und dem Bildmaterial des Bauträgers sowie die Grundrisse von fünf der 17 Wohnungen auf der Preisliste.',
  'Компьютерные визуализации корпусов, бассейнов, спа, террас и интерьеров из брошюры и набора изображений застройщика, а также планировки пяти из 17 квартир прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمباني والمسابح والسبا والتراسات والفضاءات الداخلية، من كتيّب المطوّر ومجموعة صوره، ومخططات خمسة من المساكن السبعة عشر الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van de blokken, de zwembaden, de spa, de terrassen en de interieurs, uit de brochure en de beeldenset van de ontwikkelaar, en de plattegronden van vijf van de 17 woningen op de prijslijst.',
  'Wygenerowane komputerowo widoki budynków, basenów, spa, tarasów i wnętrz z broszury i zestawu obrazów dewelopera oraz rzuty pięciu z 17 lokali z cennika.',
  'Datagenererte bilder av byggene, bassengene, spaet, terrassene og interiørene, fra utbyggerens brosjyre og bildesett, og tegningene av fem av de 17 boligene i prislisten.',
  'Datorgenererade vyer av husen, poolerna, spat, terrasserna och interiörerna, från exploatörens broschyr och bilduppsättning, och ritningarna för fem av de 17 bostäderna i prislistan.')
a('.media.note',
  'Las imágenes son ilustraciones generadas por ordenador, no fotografías del edificio terminado. El folleto dice que sus imágenes son orientativas y que el mobiliario que muestran solo ilustra el uso de los espacios y no está incluido. Los planos son los planos de proyecto del promotor del 16 de octubre de 2026, recortados de sus hojas para que no quede ningún logotipo ni nombre de proyecto; los nombres de las estancias están en español, las superficies son aproximadas y los planos no son contractuales.',
  'Les images sont des illustrations générées par ordinateur, et non des photographies du bâtiment achevé. La brochure indique que ses images sont données à titre indicatif et que le mobilier qu’elles montrent sert seulement à illustrer l’usage des espaces et n’est pas inclus. Les plans sont les plans de projet du promoteur du 16 octobre 2026, découpés de leurs feuilles afin qu’il ne reste ni logo ni nom de projet ; les noms des pièces sont en espagnol, les surfaces sont approximatives et les plans ne sont pas contractuels.',
  'Die Bilder sind computergenerierte Illustrationen, keine Fotografien des fertigen Gebäudes. Die Broschüre gibt an, dass ihre Bilder nur zur Orientierung dienen und dass die darin gezeigten Möbel lediglich die Nutzung der Räume veranschaulichen und nicht enthalten sind. Die Grundrisse sind die Projektpläne des Bauträgers vom 16. Oktober 2026, aus ihren Blättern ausgeschnitten, sodass weder Logo noch Projektname übrig bleibt; die Raumbezeichnungen sind spanisch, die Flächen sind ungefähre Angaben, und die Pläne sind nicht vertraglich bindend.',
  'Изображения — это компьютерные иллюстрации, а не фотографии готового здания. В брошюре сказано, что её изображения носят ориентировочный характер, а показанная на них мебель лишь иллюстрирует использование помещений и не входит в поставку. Планировки — проектные планы застройщика от 16 октября 2026 года, вырезанные из листов так, чтобы на них не осталось ни логотипа, ни названия проекта; названия помещений на них даны по-испански, площади приблизительные, а планы не носят договорного характера.',
  'الصور رسوم توضيحية مولَّدة بالحاسوب وليست صورًا فوتوغرافية للمبنى بعد اكتماله. يذكر الكتيّب أن صوره للاسترشاد فقط، وأن الأثاث الظاهر فيها يوضّح استخدام المساحات فحسب وليس مشمولًا. أما المخططات فهي مخططات مرحلة المشروع الصادرة عن المطوّر بتاريخ 16 أكتوبر 2026، مقصوصة من أوراقها بحيث لا يبقى فيها شعار ولا اسم مشروع؛ وأسماء الغرف عليها بالإسبانية، والمساحات تقريبية، والمخططات ليست ملزمة تعاقديًا.',
  'De beelden zijn computergegenereerde illustraties, geen foto’s van het afgewerkte gebouw. De brochure zegt dat de beelden slechts indicatief zijn en dat het meubilair dat erop staat alleen het gebruik van de ruimtes illustreert en niet is inbegrepen. De plattegronden zijn de projectplannen van de ontwikkelaar van 16 oktober 2026, uit hun bladen geknipt zodat er geen logo of projectnaam overblijft; de namen van de ruimtes zijn in het Spaans, de oppervlaktes zijn bij benadering en de plannen zijn niet contractueel.',
  'Obrazy to ilustracje wygenerowane komputerowo, a nie zdjęcia ukończonego budynku. Broszura zastrzega, że jej obrazy mają charakter orientacyjny, a pokazane na nich meble jedynie ilustrują sposób użytkowania przestrzeni i nie są wliczone w cenę. Rzuty to plany projektowe dewelopera z 16 października 2026 roku, wycięte z arkuszy tak, by nie został na nich żaden logotyp ani nazwa projektu; nazwy pomieszczeń są po hiszpańsku, powierzchnie są przybliżone, a plany nie mają charakteru umownego.',
  'Bildene er datagenererte illustrasjoner, ikke fotografier av den ferdige bygningen. Brosjyren sier at bildene bare er veiledende, og at møblene på dem bare illustrerer bruken av rommene og ikke er inkludert. Tegningene er utbyggerens prosjekttegninger fra 16. oktober 2026, utklipt fra arkene slik at ingen logo eller prosjektnavn er igjen; romnavnene er på spansk, arealene er omtrentlige, og tegningene er ikke kontraktsfestet.',
  'Bilderna är datorgenererade illustrationer, inte fotografier av den färdiga byggnaden. Broschyren anger att dess bilder bara är vägledande och att möblerna på dem endast illustrerar hur ytorna kan användas och inte ingår. Ritningarna är exploatörens projektritningar från den 16 oktober 2026, utklippta ur sina blad så att ingen logotyp eller något projektnamn finns kvar; rumsnamnen är på spanska, ytorna är ungefärliga och ritningarna är inte avtalsbindande.')
a('.media.items[1].alt',
  'Vista aérea generada por ordenador de los bloques al anochecer, con ventanas y terrazas iluminadas, una piscina iluminada y la costa a lo lejos',
  'Vue aérienne générée par ordinateur des blocs au crépuscule, avec fenêtres et terrasses éclairées, une piscine éclairée et la côte au loin',
  'Computergenerierte Luftaufnahme der Blöcke in der Abenddämmerung, mit beleuchteten Fenstern und Terrassen, einem beleuchteten Pool und der Küste in der Ferne',
  'Компьютерная визуализация корпусов в сумерках с высоты птичьего полёта: освещённые окна и террасы, подсвеченный бассейн и вдали побережье',
  'منظر جوي مولَّد بالحاسوب للمباني عند الغسق، مع نوافذ وتراسات مضاءة ومسبح مضاء والساحل في البعيد',
  'Computergegenereerd luchtbeeld van de blokken bij schemering, met verlichte ramen en terrassen, een verlicht zwembad en de kust in de verte',
  'Wygenerowany komputerowo widok z lotu ptaka na budynki o zmierzchu, z oświetlonymi oknami i tarasami, podświetlonym basenem i wybrzeżem w oddali',
  'Datagenerert flyfoto av byggene i skumringen, med opplyste vinduer og terrasser, et opplyst basseng og kysten i det fjerne',
  'Datorgenererad flygvy av husen i skymningen, med upplysta fönster och terrasser, en upplyst pool och kusten i fjärran')
a('.media.items[1].caption', 'El solar al anochecer', 'Le site au crépuscule', 'Das Grundstück in der Abenddämmerung', 'Участок в сумерках',
  'الموقع عند الغسق', 'Het terrein bij schemering', 'Działka o zmierzchu', 'Tomten i skumringen', 'Tomten i skymningen')
a('.media.items[2].caption', 'Los bloques en terrazas vistos desde la carretera', 'Les blocs en terrasses vus depuis la route', 'Die terrassierten Blöcke von der Straße aus',
  'Террасные корпуса, вид с дороги', 'المباني المدرَّجة من الطريق', 'De terrasvormige blokken vanaf de weg', 'Tarasowe budynki widziane z drogi',
  'Terrassebyggene sett fra veien', 'De terrasserade husen sedda från vägen')
cg('.media.items[3].alt',
   'a través de la piscina hacia bloques escalonados sobre un muro de contención de piedra, con tumbonas, sombrillas y palmeras',
   'à travers la piscine vers des blocs en gradins au-dessus d’un mur de soutènement en pierre, avec transats, parasols et palmiers',
   'über den Pool hinweg auf gestaffelte Blöcke über einer Stützmauer aus Stein, mit Liegen, Sonnenschirmen und Palmen',
   'через бассейн на ступенчатые корпуса над каменной подпорной стеной, с шезлонгами, зонтами и пальмами',
   'عبر المسبح نحو مبانٍ متدرجة فوق جدار استنادي حجري، مع كراسٍ للاستلقاء ومظلات ونخيل',
   'over het zwembad naar getrapte blokken boven een stenen keermuur, met ligbedden, parasols en palmen',
   'przez basen na schodkowe budynki nad kamiennym murem oporowym, z leżakami, parasolami i palmami',
   'over bassenget mot trappede bygg over en støttemur av stein, med solsenger, parasoller og palmer',
   'över poolen mot trappstegsformade hus ovanför en stödmur av sten, med solstolar, parasoller och palmer')
cg('.media.items[4].alt',
   'de la piscina con borde de vidrio frente a las colinas, con tumbonas y palmeras a lo largo y un bloque detrás',
   'de la piscine à bord de verre face aux collines, avec transats et palmiers le long et un bloc derrière',
   'des Pools mit Glasrand zu den Hügeln hin, mit Liegen und Palmen entlang und einem Block dahinter',
   'бассейна со стеклянным бортом, обращённого к холмам, с шезлонгами и пальмами вдоль него и корпусом позади',
   'لمسبح بحافة زجاجية مواجه للتلال، مع كراسٍ للاستلقاء ونخيل على امتداده ومبنى خلفه',
   'van het zwembad met glazen rand richting de heuvels, met ligbedden en palmen eromheen en een blok erachter',
   'basenu ze szklaną krawędzią zwróconego ku wzgórzom, z leżakami i palmami wzdłuż niego oraz budynkiem w tle',
   'av bassenget med glasskant mot åsene, med solsenger og palmer langs det og et bygg bak',
   'av poolen med glaskant mot kullarna, med solstolar och palmer längs den och ett hus bakom')
a('.media.items[4].caption', 'La piscina con borde de vidrio', 'La piscine à bord de verre', 'Der Pool mit Glasrand', 'Бассейн со стеклянным бортом',
  'المسبح ذو الحافة الزجاجية', 'Het zwembad met glazen rand', 'Basen ze szklaną krawędzią', 'Bassenget med glasskant', 'Poolen med glaskant')
cg('.media.items[5].alt',
   'de la entrada de un edificio con muros de piedra, un parterre plantado, escalones hasta una cancela y terrazas curvas arriba',
   'd’une entrée d’immeuble avec murs en pierre, un massif planté, des marches menant à un portail et des terrasses courbes au-dessus',
   'eines Gebäudeeingangs mit Steinmauern, einem bepflanzten Beet, Stufen zu einem Tor und geschwungenen Terrassen darüber',
   'входа в здание с каменными стенами, клумбой, ступенями к калитке и изогнутыми террасами наверху',
   'لمدخل مبنى بجدران حجرية وحوض مزروع ودرجات تؤدي إلى بوابة وتراسات منحنية في الأعلى',
   'van een gebouwingang met stenen muren, een beplante border, treden naar een poort en gebogen terrassen erboven',
   'wejścia do budynku z kamiennymi murami, obsadzoną rabatą, schodami do furtki i zakrzywionymi tarasami powyżej',
   'av en bygningsinngang med steinmurer, et beplantet bed, trapper opp til en port og buede terrasser over',
   'av en husentré med stenmurar, en planterad rabatt, trappsteg upp till en grind och böjda terrasser ovanför')
a('.media.items[5].caption', 'La entrada de un edificio', 'L’entrée d’un immeuble', 'Ein Gebäudeeingang', 'Вход в здание',
  'مدخل أحد المباني', 'De ingang van een gebouw', 'Wejście do budynku', 'En bygningsinngang', 'En husentré')
a('.media.items[6].caption', 'El spa interior', 'Le spa intérieur', 'Der Indoor-Spa', 'Спа в помещении',
  'السبا الداخلي', 'De binnenspa', 'Spa w budynku', 'Innendørs spa', 'Inomhusspat')
cg('.media.items[7].alt',
   'del gimnasio con pesas libres, bancos, bicicletas estáticas y cintas de correr, y puertas acristaladas hacia la zona de la piscina',
   'de la salle de sport avec haltères libres, bancs, vélos d’appartement et tapis de course, et portes vitrées donnant sur l’espace piscine',
   'des Fitnessraums mit Freihanteln, Bänken, Heimtrainern und Laufbändern sowie Glastüren zum Poolbereich',
   'тренажёрного зала со свободными весами, скамьями, велотренажёрами и беговыми дорожками и стеклянными дверями к бассейну',
   'للصالة الرياضية مع أوزان حرة ومقاعد ودراجات تمرين وأجهزة جري، وأبواب زجاجية نحو منطقة المسبح',
   'van de fitnessruimte met vrije gewichten, banken, hometrainers en loopbanden, en glazen deuren naar het zwembadgebied',
   'siłowni z wolnymi ciężarami, ławkami, rowerami treningowymi i bieżniami oraz przeszklonymi drzwiami na teren basenu',
   'av treningsrommet med frie vekter, benker, spinningsykler og tredemøller, og glassdører til bassengområdet',
   'av gymmet med fria vikter, bänkar, motionscyklar och löpband, och glasdörrar mot poolområdet')
a('.media.items[8].alt',
  'Vista generada por ordenador de una sala con una mesa larga y sillas, una encimera de cocina con taburetes y lámparas colgantes, bajo un techo de madera',
  'Vue générée par ordinateur d’une salle avec une longue table et des chaises, un plan de travail de cuisine avec tabourets et suspensions, sous un plafond en bois',
  'Computergenerierte Ansicht eines Raums mit einem langen Tisch und Stühlen, einer Küchentheke mit Barhockern und Pendelleuchten, unter einer Holzdecke',
  'Компьютерная визуализация помещения с длинным столом и стульями, кухонной стойкой с барными стульями и подвесными светильниками под деревянным потолком',
  'منظر مولَّد بالحاسوب لقاعة فيها طاولة طويلة وكراسٍ ومنضدة مطبخ مع مقاعد مرتفعة ومصابيح معلَّقة تحت سقف خشبي',
  'Computergegenereerd beeld van een ruimte met een lange tafel en stoelen, een keukenblad met barkrukken en hanglampen, onder een houten plafond',
  'Wygenerowany komputerowo widok pomieszczenia z długim stołem i krzesłami, blatem kuchennym ze stołkami barowymi i lampami wiszącymi, pod drewnianym sufitem',
  'Datagenerert bilde av et rom med et langt bord og stoler, en kjøkkendisk med barkrakker og taklamper, under et trehimling',
  'Datorgenererad vy av ett rum med ett långt bord och stolar, en köksbänk med barstolar och hängande lampor, under ett trätak')
cg('.media.items[9].alt',
   'de un vestíbulo con una pared de lamas de madera, dos puertas marcadas A y B y un ascensor',
   'd’un hall d’entrée avec un mur à lamelles de bois, deux portes marquées A et B et un ascenseur',
   'einer Eingangshalle mit einer Wand aus Holzlamellen, zwei Türen mit den Bezeichnungen A und B und einem Aufzug',
   'вестибюля с деревянной реечной стеной, двумя дверями с обозначениями A и B и лифтом',
   'لبهو مدخل بجدار من شرائح خشبية وبابين يحملان الحرفين A وB ومصعد',
   'van een hal met een wand van houten latten, twee deuren gemarkeerd A en B en een lift',
   'holu z ażurową ścianą z drewnianych listew, dwojgiem drzwi oznaczonych A i B oraz windą',
   'av en lobby med en vegg av trelameller, to dører merket A og B og en heis',
   'av en entréhall med en vägg av träribbor, två dörrar märkta A och B och en hiss')
a('.media.items[9].caption', 'El vestíbulo de un edificio', 'Le hall d’un immeuble', 'Die Eingangshalle eines Gebäudes', 'Вестибюль здания',
  'بهو أحد المباني', 'De hal van een gebouw', 'Hol budynku', 'Lobbyen i et bygg', 'Entréhallen i ett hus')
cg('.media.items[11].alt',
   'de una terraza cubierta bajo un techo de madera, con un sofá, una mesa de comedor y una barandilla de vidrio, con vistas a las colinas y al mar',
   'd’une terrasse couverte sous un plafond en bois, avec un canapé, une table à manger et un garde-corps en verre, avec vue sur les collines et la mer',
   'einer überdachten Terrasse unter einer Holzdecke, mit einem Sofa, einem Esstisch und einer Glasbrüstung, mit Blick über die Hügel zum Meer',
   'крытой террасы под деревянным потолком, с диваном, обеденным столом и стеклянным ограждением, с видом на холмы и море',
   'لتراس مسقوف تحت سقف خشبي، مع أريكة وطاولة طعام وحاجز زجاجي، وإطلالة على التلال والبحر',
   'van een overdekt terras onder een houten plafond, met een bank, een eettafel en een glazen balustrade, met uitzicht over de heuvels op de zee',
   'tarasu zadaszonego pod drewnianym sufitem, z sofą, stołem jadalnianym i szklaną balustradą, z widokiem na wzgórza i morze',
   'av en overbygd terrasse under et trehimling, med en sofa, et spisebord og et glassrekkverk, med utsikt over åsene til havet',
   'av en övertäckt terrass under ett trätak, med en soffa, ett matbord och ett glasräcke, med utsikt över kullarna mot havet')
a('.media.items[12].alt',
  'Salón generado por ordenador con un sofá rinconero, un televisor sobre un mueble largo y una puerta corredera de vidrio hacia una terraza y el mar',
  'Séjour généré par ordinateur avec un canapé d’angle, un téléviseur sur un long meuble et une porte coulissante en verre donnant sur une terrasse et la mer',
  'Computergeneriertes Wohnzimmer mit einem Ecksofa, einem Fernseher auf einem langen Wandmöbel und einer gläsernen Schiebetür zu einer Terrasse und zum Meer',
  'Компьютерная визуализация гостиной с угловым диваном, телевизором на длинной тумбе и стеклянной раздвижной дверью на террасу и к морю',
  'غرفة جلوس مولَّدة بالحاسوب مع أريكة زاوية وتلفاز على وحدة طويلة وباب زجاجي منزلق نحو تراس والبحر',
  'Computergegenereerde woonkamer met een hoekbank, een televisie op een lang meubel en een glazen schuifdeur naar een terras en de zee',
  'Wygenerowany komputerowo salon z narożną sofą, telewizorem na długiej szafce i przeszklonymi drzwiami przesuwnymi na taras i w stronę morza',
  'Datagenerert stue med en hjørnesofa, et fjernsyn på en lang tv-benk og en skyvedør i glass mot en terrasse og havet',
  'Datorgenererat vardagsrum med en hörnsoffa, en tv på en lång bänk och en glasskjutdörr mot en terrass och havet')
a('.media.items[13].alt',
  'Cocina abierta generada por ordenador con armarios grises y de madera, un horno empotrado y una barra de madera con sillas',
  'Cuisine ouverte générée par ordinateur avec des placards gris et en bois, un four encastré et un bar en bois avec des chaises',
  'Computergenerierte offene Küche mit grauen und hölzernen Schränken, einem Einbaubackofen und einer Holztheke mit Stühlen',
  'Компьютерная визуализация открытой кухни с серыми и деревянными шкафами, встроенной духовкой и деревянной барной стойкой со стульями',
  'مطبخ مفتوح مولَّد بالحاسوب بخزائن رمادية وخشبية وفرن مدمج وبار خشبي مع كراسٍ',
  'Computergegenereerde open keuken met grijze en houten kasten, een inbouwoven en een houten bar met stoelen',
  'Wygenerowana komputerowo otwarta kuchnia z szarymi i drewnianymi szafkami, piekarnikiem do zabudowy i drewnianym barem z krzesłami',
  'Datagenerert åpent kjøkken med grå skap og skap i tre, en innebygd stekeovn og en bardisk i tre med stoler',
  'Datorgenererat öppet kök med grå skåp och skåp i trä, en inbyggd ugn och en bardisk i trä med stolar')
a('.media.items[13].caption', 'Cocina y barra de comedor', 'Cuisine et bar-repas', 'Küche und Essbar', 'Кухня и обеденная барная стойка',
  'المطبخ وبار الطعام', 'Keuken en eetbar', 'Kuchnia i bar jadalniany', 'Kjøkken og spisebar', 'Kök och matbar')
a('.media.items[14].alt',
  'Dormitorio generado por ordenador con una cama doble, un televisor en la pared y una puerta corredera de vidrio hacia una terraza y el mar',
  'Chambre générée par ordinateur avec un lit double, un téléviseur mural et une porte coulissante en verre donnant sur une terrasse et la mer',
  'Computergeneriertes Schlafzimmer mit einem Doppelbett, einem Fernseher an der Wand und einer gläsernen Schiebetür zu einer Terrasse und zum Meer',
  'Компьютерная визуализация спальни с двуспальной кроватью, телевизором на стене и стеклянной раздвижной дверью на террасу и к морю',
  'غرفة نوم مولَّدة بالحاسوب مع سرير مزدوج وتلفاز على الجدار وباب زجاجي منزلق نحو تراس والبحر',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een televisie aan de muur en een glazen schuifdeur naar een terras en de zee',
  'Wygenerowana komputerowo sypialnia z podwójnym łóżkiem, telewizorem na ścianie i przeszklonymi drzwiami przesuwnymi na taras i w stronę morza',
  'Datagenerert soverom med en dobbeltseng, et fjernsyn på veggen og en skyvedør i glass mot en terrasse og havet',
  'Datorgenererat sovrum med en dubbelsäng, en tv på väggen och en glasskjutdörr mot en terrass och havet')
a('.media.items[15].alt',
  'Baño generado por ordenador con un lavabo doble, dos espejos ovalados y una ducha a ras de suelo con mampara de vidrio',
  'Salle de bain générée par ordinateur avec une double vasque, deux miroirs ovales et une douche à l’italienne avec paroi en verre',
  'Computergeneriertes Badezimmer mit einem Doppelwaschtisch, zwei ovalen Spiegeln und einer bodengleichen Dusche mit Glaswand',
  'Компьютерная визуализация ванной комнаты с двойной раковиной, двумя овальными зеркалами и душем без поддона со стеклянной перегородкой',
  'حمام مولَّد بالحاسوب مع حوض مزدوج ومرآتين بيضاويتين ودشّ بمستوى الأرض مع حاجز زجاجي',
  'Computergegenereerde badkamer met een dubbele wastafel, twee ovale spiegels en een inloopdouche met glazen wand',
  'Wygenerowana komputerowo łazienka z podwójną umywalką, dwoma owalnymi lustrami i prysznicem bez brodzika ze szklaną ścianką',
  'Datagenerert bad med en dobbel servant, to ovale speil og en dusj i gulvnivå med glassvegg',
  'Datorgenererat badrum med ett dubbelt tvättställ, två ovala speglar och en duschhörna i golvnivå med glasvägg')
a('.media.items[16].alt',
  'Baño generado por ordenador con un inodoro suspendido, un lavabo doble, dos espejos ovalados y una ducha con mampara de vidrio',
  'Salle de bain générée par ordinateur avec un WC suspendu, une double vasque, deux miroirs ovales et une douche avec paroi en verre',
  'Computergeneriertes Badezimmer mit einem Wand-WC, einem Doppelwaschtisch, zwei ovalen Spiegeln und einer Dusche mit Glaswand',
  'Компьютерная визуализация ванной комнаты с подвесным унитазом, двойной раковиной, двумя овальными зеркалами и душем со стеклянной перегородкой',
  'حمام مولَّد بالحاسوب مع مرحاض معلَّق وحوض مزدوج ومرآتين بيضاويتين ودشّ بحاجز زجاجي',
  'Computergegenereerde badkamer met een hangend toilet, een dubbele wastafel, twee ovale spiegels en een douche met glazen wand',
  'Wygenerowana komputerowo łazienka z wiszącą miską ustępową, podwójną umywalką, dwoma owalnymi lustrami i prysznicem ze szklaną ścianką',
  'Datagenerert bad med et veggmontert toalett, en dobbel servant, to ovale speil og en dusj med glassvegg',
  'Datorgenererat badrum med en väggmonterad toalett, ett dubbelt tvättställ, två ovala speglar och en dusch med glasvägg')
a('.media.items[16].caption', 'Un segundo baño', 'Une deuxième salle de bain', 'Ein zweites Badezimmer', 'Вторая ванная комната',
  'حمام ثانٍ', 'Een tweede badkamer', 'Druga łazienka', 'Et andre bad', 'Ett andra badrum')

PLAN_ALT = {'es': 'Plano de la vivienda {}', 'fr': 'Plan du logement {}', 'de': 'Grundriss der Wohnung {}',
            'ru': 'Планировка квартиры {}', 'ar': 'مخطط المسكن {}', 'nl': 'Plattegrond van woning {}',
            'pl': 'Rzut lokalu {}', 'no': 'Plantegning av bolig {}', 'sv': 'Planritning för bostad {}'}
PLAN_CAP = {'es': 'Vivienda {}', 'fr': 'Logement {}', 'de': 'Wohnung {}', 'ru': 'Квартира {}',
            'ar': 'المسكن {}', 'nl': 'Woning {}', 'pl': 'Lokal {}', 'no': 'Bolig {}', 'sv': 'Bostad {}'}
n_plan = 0
for it in proj['media']['items']:
    for key, tpl, rx in (('alt', PLAN_ALT, r'Floorplan of home ([\w-]+)'), ('caption', PLAN_CAP, r'Home ([\w-]+)')):
        m = re.fullmatch(rx, it.get(key, ''))
        if m:
            T[it[key]] = {l: tpl[l].format(m.group(1)) for l in LOCS}
            n_plan += 1
assert n_plan == 10, n_plan

# ---- overview, why, architecture --------------------------------------------------------------

a('.overview.headlineHtml',
  '17 de las 19 viviendas de la lista, <em>disponibles</em>', '17 des 19 logements listés, <em>disponibles</em>', '17 der 19 aufgeführten Wohnungen <em>verfügbar</em>',
  '17 из 19 квартир списка <em>доступны</em>', '17 من أصل 19 مسكنًا مدرجًا <em>متاحة</em>', '17 van de 19 vermelde woningen <em>beschikbaar</em>',
  '17 z 19 wymienionych lokali <em>dostępnych</em>', '17 av de 19 oppførte boligene <em>er ledige</em>', '17 av de 19 listade bostäderna <em>är lediga</em>')
a('.overview.copy[0]',
  'El folleto del promotor presenta viviendas de dos y tres dormitorios en Estepona, entre el mar y las colinas y muy cerca de campos de golf, con grandes terrazas, dos piscinas, un spa, un gimnasio y una zona de coworking.',
  'La brochure du promoteur présente des logements de deux et trois chambres à Estepona, entre la mer et les collines et tout près de terrains de golf, avec de grandes terrasses, deux piscines, un spa, une salle de sport et un espace de coworking.',
  'Die Broschüre des Bauträgers stellt Wohnungen mit zwei und drei Schlafzimmern in Estepona vor, zwischen Meer und Hügeln und ganz in der Nähe von Golfplätzen, mit großen Terrassen, zwei Schwimmbädern, einem Spa, einem Fitnessraum und einem Coworking-Bereich.',
  'В брошюре застройщика представлены квартиры с двумя и тремя спальнями в Эстепоне, между морем и холмами, совсем рядом с полями для гольфа: с большими террасами, двумя бассейнами, спа, тренажёрным залом и зоной коворкинга.',
  'يعرض كتيّب المطوّر مساكن بغرفتي نوم وثلاث غرف نوم في إستيبونا، بين البحر والتلال وعلى مقربة شديدة من ملاعب الغولف، مع تراسات واسعة ومسبحين وسبا وصالة رياضية ومنطقة للعمل المشترك.',
  'De brochure van de ontwikkelaar presenteert woningen met twee en drie slaapkamers in Estepona, tussen de zee en de heuvels en vlak bij golfbanen, met grote terrassen, twee zwembaden, een spa, een fitnessruimte en een coworkingruimte.',
  'Broszura dewelopera przedstawia lokale z dwiema i trzema sypialniami w Esteponie, między morzem a wzgórzami i tuż przy polach golfowych, z dużymi tarasami, dwoma basenami, spa, siłownią i strefą coworkingową.',
  'Utbyggerens brosjyre presenterer boliger med to og tre soverom i Estepona, mellom havet og åsene og helt nær golfbaner, med store terrasser, to svømmebasseng, et spa, et treningsrom og et coworking-område.',
  'Exploatörens broschyr presenterar bostäder med två och tre sovrum i Estepona, mellan havet och kullarna och mycket nära golfbanor, med stora terrasser, två simbassänger, ett spa, ett gym och ett coworking-område.')
a('.overview.copy[1]',
  'La lista de precios de noviembre de 2026 nombra 19 viviendas en cuatro bloques. Muestra 17 con precio y marca 2 como reservadas. Once de las 17 tienen dos dormitorios y seis tienen tres, y cada una se vende con su plaza o plazas de garaje y su trastero. Ningún documento que tengamos da una fecha de entrega, una licencia ni la fase de las obras.',
  'La liste de prix de novembre 2026 nomme 19 logements répartis en quatre blocs. Elle en montre 17 avec un prix et en marque 2 comme réservés. Onze des 17 ont deux chambres et six en ont trois, et chacun est vendu avec sa ou ses places de parking et sa cave. Aucun document en notre possession ne donne de date de livraison, de permis ni l’état d’avancement des travaux.',
  'Die Preisliste vom November 2026 nennt 19 Wohnungen in vier Blöcken. Sie zeigt 17 mit Preis und kennzeichnet 2 als reserviert. Elf der 17 haben zwei Schlafzimmer und sechs haben drei, und jede wird mit ihrem Stellplatz oder ihren Stellplätzen und ihrem Abstellraum verkauft. Kein Dokument, das uns vorliegt, nennt einen Fertigstellungstermin, eine Genehmigung oder den Stand der Bauarbeiten.',
  'В прайс-листе за ноябрь 2026 года названы 19 квартир в четырёх блоках. У 17 из них указана цена, 2 отмечены как забронированные. Одиннадцать из 17 имеют две спальни, шесть — три, и каждая продаётся с машиноместом или машиноместами и кладовой. Ни в одном из имеющихся у нас документов нет срока сдачи, разрешения на строительство или сведений о стадии работ.',
  'تذكر قائمة أسعار نوفمبر 2026 تسعة عشر مسكنًا في أربعة مبانٍ. وتُظهر سبعة عشر منها بسعر وتشير إلى اثنين على أنهما محجوزان. ولدى أحد عشر من السبعة عشر غرفتا نوم ولدى ستة ثلاث غرف نوم، ويُباع كل منها مع موقف السيارات أو مواقفها ومخزنه. ولا يذكر أي مستند لدينا موعد إنجاز ولا رخصة ولا مرحلة الأعمال.',
  'De prijslijst van november 2026 noemt 19 woningen in vier blokken. Ze toont er 17 met een prijs en markeert er 2 als gereserveerd. Elf van de 17 hebben twee slaapkamers en zes hebben er drie, en elke woning wordt verkocht met haar parkeerplaats of parkeerplaatsen en haar berging. Geen enkel document dat wij hebben vermeldt een opleverdatum, een vergunning of de stand van de werken.',
  'Cennik z listopada 2026 roku wymienia 19 lokali w czterech blokach. Pokazuje 17 z ceną i oznacza 2 jako zarezerwowane. Jedenaście z 17 ma dwie sypialnie, a sześć ma trzy, i każdy lokal jest sprzedawany z przypisanym miejscem lub miejscami postojowymi oraz komórką lokatorską. Żaden dokument, którym dysponujemy, nie podaje terminu ukończenia, pozwolenia ani etapu robót.',
  'Prislisten fra november 2026 nevner 19 boliger i fire hus. Den viser 17 med pris og markerer 2 som reservert. Elleve av de 17 har to soverom og seks har tre, og hver selges med sin parkeringsplass eller sine parkeringsplasser og sitt bod. Ingen dokumenter vi har oppgir en ferdigstillelsesdato, en tillatelse eller hvor langt arbeidene har kommet.',
  'Prislistan från november 2026 nämner 19 bostäder i fyra hus. Den visar 17 med pris och markerar 2 som reserverade. Elva av de 17 har två sovrum och sex har tre, och varje säljs med sin parkeringsplats eller sina parkeringsplatser och sitt förråd. Inget dokument vi har anger ett färdigställandedatum, ett bygglov eller hur långt arbetena har kommit.')
a('.why.copy',
  'Apartamentos de dos y tres dormitorios con grandes terrazas en Estepona, con spa interior, gimnasio y sala de coworking, y el 65 % del precio pagadero solo en la escritura.',
  'Des appartements de deux et trois chambres avec de grandes terrasses à Estepona, avec spa intérieur, salle de sport et espace de coworking, et 65 % du prix exigible seulement à l’acte notarié.',
  'Wohnungen mit zwei und drei Schlafzimmern und großen Terrassen in Estepona, mit Indoor-Spa, Fitnessraum und Coworking-Raum, und 65 % des Preises erst bei der notariellen Urkunde fällig.',
  'Апартаменты с двумя и тремя спальнями и большими террасами в Эстепоне, со спа в помещении, тренажёрным залом и коворкингом; 65 % цены подлежат оплате только при нотариальном акте.',
  'شقق بغرفتي نوم وثلاث غرف نوم مع تراسات واسعة في إستيبونا، مع سبا داخلي وصالة رياضية وقاعة للعمل المشترك، و65% من السعر لا يُستحق إلا عند سند الملكية.',
  'Appartementen met twee en drie slaapkamers en grote terrassen in Estepona, met een binnenspa, een fitnessruimte en een coworkingruimte, en 65% van de prijs pas verschuldigd bij de notariële akte.',
  'Apartamenty z dwiema i trzema sypialniami oraz dużymi tarasami w Esteponie, ze spa w budynku, siłownią i salą coworkingową, a 65% ceny płatne dopiero przy akcie notarialnym.',
  'Leiligheter med to og tre soverom og store terrasser i Estepona, med innendørs spa, treningsrom og coworking-rom, og 65 % av prisen forfaller først ved skjøtet.',
  'Lägenheter med två och tre sovrum och stora terrasser i Estepona, med inomhusspa, gym och coworking-rum, och 65 % av priset förfaller först vid lagfarten.')
a('.why.points[0][1]',
  'Compradores que buscan un apartamento nuevo de dos o tres dormitorios en Estepona, con terraza, plaza de garaje y trastero, para vivir en él o como segunda residencia.',
  'Les acheteurs qui veulent un appartement neuf de deux ou trois chambres à Estepona, avec terrasse, place de parking et cave, pour y vivre ou comme résidence secondaire.',
  'Käufer, die in Estepona eine neue Wohnung mit zwei oder drei Schlafzimmern suchen, mit Terrasse, Stellplatz und Abstellraum, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которые ищут новую квартиру с двумя или тремя спальнями в Эстепоне, с террасой, машиноместом и кладовой, для жизни или как второе жильё.',
  'مشترون يبحثون عن شقة جديدة بغرفتي نوم أو ثلاث غرف نوم في إستيبونا، مع تراس وموقف سيارات ومخزن، للسكن فيها أو كمسكن ثانٍ.',
  'Kopers die in Estepona een nieuw appartement met twee of drie slaapkamers zoeken, met een terras, een parkeerplaats en een berging, om er te wonen of als tweede verblijf.',
  'Kupujący, którzy szukają w Esteponie nowego apartamentu z dwiema lub trzema sypialniami, z tarasem, miejscem postojowym i komórką lokatorską, do zamieszkania lub jako druga nieruchomość.',
  'Kjøpere som vil ha en ny leilighet med to eller tre soverom i Estepona, med terrasse, parkeringsplass og bod, til å bo i eller som feriebolig.',
  'Köpare som vill ha en ny lägenhet med två eller tre sovrum i Estepona, med terrass, parkeringsplats och förråd, att bo i eller som andra bostad.')
a('.why.points[1][1]',
  'El folleto sitúa las viviendas entre el mar y las colinas, muy cerca de algunos de los mejores campos de golf de la costa, con terrazas pensadas como espacios de vida al aire libre. Las terrazas de la lista de precios van de {N16.42} a {N79.42} {U}.',
  'La brochure situe les logements entre la mer et les collines, tout près de certains des meilleurs terrains de golf de la côte, avec des terrasses conçues comme des espaces de vie en plein air. Les terrasses de la liste de prix vont de {N16.42} à {N79.42} {U}.',
  'Die Broschüre verortet die Wohnungen zwischen Meer und Hügeln, ganz in der Nähe einiger der besten Golfplätze der Küste, mit Terrassen, die als Wohnbereiche im Freien gedacht sind. Die Terrassen auf der Preisliste reichen von {N16.42} bis {N79.42} {U}.',
  'В брошюре квартиры расположены между морем и холмами, совсем рядом с одними из лучших полей для гольфа на побережье, а террасы задуманы как места для жизни на открытом воздухе. Террасы в прайс-листе — от {N16.42} до {N79.42} {U}.',
  'يضع الكتيّب المساكن بين البحر والتلال، على مقربة شديدة من بعض أفضل ملاعب الغولف على الساحل، مع تراسات مصمّمة كمساحات للعيش في الهواء الطلق. وتتراوح التراسات في قائمة الأسعار بين {N16.42} و{N79.42} {U}.',
  'De brochure plaatst de woningen tussen de zee en de heuvels, vlak bij enkele van de beste golfbanen aan de kust, met terrassen die zijn ontworpen als buitenleefruimtes. De terrassen op de prijslijst variëren van {N16.42} tot {N79.42} {U}.',
  'Broszura umieszcza lokale między morzem a wzgórzami, tuż przy niektórych z najlepszych pól golfowych na wybrzeżu, z tarasami zaprojektowanymi jako przestrzenie do życia na świeżym powietrzu. Tarasy z cennika mają od {N16.42} do {N79.42} {U}.',
  'Brosjyren plasserer boligene mellom havet og åsene, helt nær noen av de beste golfbanene på kysten, med terrasser utformet som uteoppholdsområder. Terrassene i prislisten varierer fra {N16.42} til {N79.42} {U}.',
  'Broschyren placerar bostäderna mellan havet och kullarna, mycket nära några av kustens bästa golfbanor, med terrasser utformade som uterum för vardagslivet. Terrasserna i prislistan varierar från {N16.42} till {N79.42} {U}.')
a('.why.points[2][1]',
  'La reserva es de {E10000} + {T}, el 35 % + {T} vence en el contrato privado y el 65 % + {T} en la firma de la escritura.',
  'La réservation est de {E10000} + {T}, 35 % + {T} sont dus au contrat privé et 65 % + {T} à la signature de l’acte notarié.',
  'Die Reservierung beträgt {E10000} + {T}, 35 % + {T} werden beim privaten Vertrag fällig und 65 % + {T} bei der Unterzeichnung der notariellen Urkunde.',
  'Бронирование — {E10000} + {T}, 35 % + {T} подлежат оплате при частном договоре и 65 % + {T} при подписании нотариального акта.',
  'الحجز {E10000} + {T}، وتُستحق نسبة 35% + {T} عند العقد الخاص و65% + {T} عند توقيع سند الملكية.',
  'De reservering is {E10000} + {T}, 35% + {T} is verschuldigd bij het privécontract en 65% + {T} bij de ondertekening van de notariële akte.',
  'Rezerwacja wynosi {E10000} + {T}, 35% + {T} jest płatne przy umowie prywatnej, a 65% + {T} przy podpisaniu aktu notarialnego.',
  'Reservasjonen er {E10000} + {T}, 35 % + {T} forfaller ved den private kontrakten og 65 % + {T} ved signeringen av skjøtet.',
  'Bokningen är {E10000} + {T}, 35 % + {T} förfaller vid det privata avtalet och 65 % + {T} vid undertecknandet av lagfarten.')
a('.why.points[3][1]',
  '2 de las 19 viviendas de la lista figuran como reservadas, y la lista dice que la disponibilidad y los precios pueden cambiar sin previo aviso. Confirmamos precio y disponibilidad antes de cualquier reserva.',
  '2 des 19 logements de la liste sont marqués comme réservés, et la liste indique que la disponibilité et les prix peuvent changer sans préavis. Nous confirmons le prix et la disponibilité avant toute réservation.',
  '2 der 19 Wohnungen auf der Liste sind als reserviert gekennzeichnet, und die Liste gibt an, dass Verfügbarkeit und Preise ohne Vorankündigung geändert werden können. Wir bestätigen Preis und Verfügbarkeit vor jeder Reservierung.',
  '2 из 19 квартир списка отмечены как забронированные, а в списке сказано, что наличие и цены могут измениться без предварительного уведомления. Мы подтверждаем цену и наличие до любого бронирования.',
  'مسكنان من أصل 19 في القائمة مشار إليهما على أنهما محجوزان، وتذكر القائمة أن التوفر والأسعار قابلان للتغيير دون إشعار مسبق. نؤكد السعر والتوفر قبل أي حجز.',
  '2 van de 19 woningen op de lijst zijn als gereserveerd gemarkeerd, en de lijst zegt dat beschikbaarheid en prijzen zonder voorafgaande kennisgeving kunnen veranderen. Wij bevestigen prijs en beschikbaarheid vóór elke reservering.',
  '2 z 19 lokali na liście są oznaczone jako zarezerwowane, a lista podaje, że dostępność i ceny mogą ulec zmianie bez uprzedzenia. Przed każdą rezerwacją potwierdzamy cenę i dostępność.',
  '2 av de 19 boligene på listen er markert som reservert, og listen sier at tilgjengelighet og priser kan endres uten forvarsel. Vi bekrefter pris og tilgjengelighet før enhver reservasjon.',
  '2 av de 19 bostäderna på listan är markerade som reserverade, och listan anger att tillgänglighet och priser kan ändras utan förvarning. Vi bekräftar pris och tillgänglighet före varje bokning.')
a('.architecture.headlineHtml',
  'Terrazas curvas, <em>piedra, madera y vidrio</em>', 'Terrasses courbes, <em>pierre, bois et verre</em>', 'Geschwungene Terrassen, <em>Stein, Holz und Glas</em>',
  'Изогнутые террасы, <em>камень, дерево и стекло</em>', 'تراسات منحنية، <em>حجر وخشب وزجاج</em>', 'Gebogen terrassen, <em>steen, hout en glas</em>',
  'Zakrzywione tarasy, <em>kamień, drewno i szkło</em>', 'Buede terrasser, <em>stein, tre og glass</em>', 'Böjda terrasser, <em>sten, trä och glas</em>')
a('.architecture.copy[0]',
  'En las imágenes generadas por ordenador del promotor, los bloques tienen largos forjados de terraza curvos en un tono de piedra clara, falsos techos de madera y barandillas de vidrio, sobre una ladera con muros de piedra y vegetación. El folleto describe líneas horizontales, volúmenes equilibrados y terrazas amplias que funcionan como espacios de vida al aire libre.',
  'Dans les images générées par ordinateur du promoteur, les blocs ont de longues dalles de terrasse courbes d’une teinte de pierre claire, des sous-faces en bois et des garde-corps en verre, posés sur un coteau avec des murs de pierre et de la végétation. La brochure décrit des lignes horizontales, des volumes équilibrés et de vastes terrasses qui fonctionnent comme des espaces de vie en plein air.',
  'Auf den computergenerierten Bildern des Bauträgers haben die Blöcke lange, geschwungene Terrassenplatten in hellem Steinton, Holzuntersichten und Glasbrüstungen, auf einem Hang mit Steinmauern und Bepflanzung. Die Broschüre beschreibt horizontale Linien, ausgewogene Baukörper und großzügige Terrassen, die als Wohnbereiche im Freien funktionieren.',
  'На компьютерных изображениях застройщика корпуса имеют длинные изогнутые плиты террас цвета светлого камня, деревянную подшивку и стеклянные ограждения; они расположены на склоне с каменными стенами и озеленением. В брошюре описаны горизонтальные линии, сбалансированные объёмы и просторные террасы, которые служат местом для жизни на открытом воздухе.',
  'في صور المطوّر المولَّدة بالحاسوب تظهر في المباني بلاطات تراسات طويلة منحنية بلون الحجر الفاتح وأسقف خشبية وحواجز زجاجية، على سفح تلة مع جدران حجرية ونباتات. ويصف الكتيّب خطوطًا أفقية وكتلًا متوازنة وتراسات فسيحة تعمل كمساحات للعيش في الهواء الطلق.',
  'Op de computergegenereerde beelden van de ontwikkelaar hebben de blokken lange, gebogen terrasplaten in een lichte steenkleur, houten plafonds en glazen balustrades, op een helling met stenen muren en beplanting. De brochure beschrijft horizontale lijnen, evenwichtige volumes en ruime terrassen die werken als buitenleefruimtes.',
  'Na wygenerowanych komputerowo obrazach dewelopera budynki mają długie, zakrzywione płyty tarasów w kolorze jasnego kamienia, drewniane podsufitki i szklane balustrady, usytuowane na zboczu z kamiennymi murami i zielenią. Broszura opisuje poziome linie, wyważone bryły i przestronne tarasy, które pełnią rolę przestrzeni do życia na świeżym powietrzu.',
  'På utbyggerens datagenererte bilder har byggene lange, buede terrasseplater i en lys steinfarge, trehimlinger og glassrekkverk, plassert i en skråning med steinmurer og beplantning. Brosjyren beskriver horisontale linjer, balanserte volumer og romslige terrasser som fungerer som uteoppholdsområder.',
  'På exploatörens datorgenererade bilder har husen långa, böjda terrassplattor i en ljus stenfärg, trätak och glasräcken, placerade i en sluttning med stenmurar och planteringar. Broschyren beskriver horisontella linjer, balanserade volymer och rymliga terrasser som fungerar som uterum.')
a('.architecture.copy[1]',
  'La lista de precios numera las viviendas por bloque y portal, en cuatro bloques con hasta tres portales cada uno. El folleto dice que los edificios están dispuestos para aprovechar al máximo las vistas y la luz natural. Ninguno de los documentos da el número total de viviendas ni de plantas.',
  'La liste de prix numérote les logements par bloc et par cage, dans quatre blocs comptant jusqu’à trois cages chacun. La brochure indique que les bâtiments sont disposés de façon à tirer le meilleur parti des vues et de la lumière naturelle. Aucun des documents ne donne le nombre total de logements ni d’étages.',
  'Die Preisliste nummeriert die Wohnungen nach Block und Aufgang, in vier Blöcken mit jeweils bis zu drei Aufgängen. Die Broschüre gibt an, dass die Gebäude so angeordnet sind, dass Aussicht und natürliches Licht bestmöglich genutzt werden. Keines der Dokumente nennt die Gesamtzahl der Wohnungen oder der Geschosse.',
  'В прайс-листе квартиры пронумерованы по блокам и подъездам: четыре блока, в каждом до трёх подъездов. В брошюре сказано, что здания расположены так, чтобы наилучшим образом использовать виды и естественный свет. Ни в одном из документов нет общего числа квартир или этажей.',
  'ترقّم قائمة الأسعار المساكن بحسب المبنى والمدخل، في أربعة مبانٍ في كل منها حتى ثلاثة مداخل. ويذكر الكتيّب أن المباني موزّعة بحيث تستفيد أقصى استفادة من الإطلالات والضوء الطبيعي. ولا يذكر أي من المستندات العدد الإجمالي للمساكن أو الطوابق.',
  'De prijslijst nummert de woningen per blok en portiek, in vier blokken met elk maximaal drie portieken. De brochure zegt dat de gebouwen zo zijn gerangschikt dat uitzicht en natuurlijk licht optimaal worden benut. Geen van de documenten geeft het totale aantal woningen of verdiepingen.',
  'Cennik numeruje lokale według bloku i klatki, w czterech blokach z maksymalnie trzema klatkami każdy. Broszura podaje, że budynki rozmieszczono tak, aby jak najlepiej wykorzystać widoki i naturalne światło. Żaden z dokumentów nie podaje łącznej liczby lokali ani kondygnacji.',
  'Prislisten nummererer boligene etter hus og oppgang, i fire hus med opptil tre oppganger hver. Brosjyren sier at byggene er plassert for å utnytte utsikten og dagslyset best mulig. Ingen av dokumentene oppgir det samlede antallet boliger eller etasjer.',
  'Prislistan numrerar bostäderna efter hus och uppgång, i fyra hus med upp till tre uppgångar vardera. Broschyren anger att byggnaderna är placerade för att ta tillvara utsikt och naturligt ljus på bästa sätt. Inget av dokumenten anger det totala antalet bostäder eller våningar.')
a('.architecture.highlights[0][1]',
  'Una fachada a medida que combina diversos acabados con un revestimiento continuo en tonos cálidos, con un aislamiento térmico y acústico que cumple el Código Técnico de la Edificación.',
  'Une façade sur mesure associant plusieurs finitions à un revêtement continu aux tons chauds, avec une isolation thermique et acoustique conforme au Code technique du bâtiment espagnol.',
  'Eine maßgeschneiderte Fassade, die verschiedene Oberflächen mit einer durchgehenden Verkleidung in warmen Tönen verbindet, mit Wärme- und Schalldämmung, die den spanischen Bauvorschriften entspricht.',
  'Фасад по индивидуальному проекту: разные виды отделки в сочетании со сплошной облицовкой тёплых тонов, с тепловой и звукоизоляцией, соответствующей испанскому строительному кодексу.',
  'واجهة مصمَّمة خصيصًا تجمع بين تشطيبات متنوعة وكسوة متصلة بدرجات دافئة، مع عزل حراري وصوتي يستوفي قانون البناء الإسباني.',
  'Een op maat gemaakte gevel die diverse afwerkingen combineert met doorlopende bekleding in warme tinten, met thermische en akoestische isolatie die voldoet aan de Spaanse bouwcode.',
  'Indywidualnie zaprojektowana elewacja łącząca różne wykończenia z ciągłą okładziną w ciepłych tonach, z izolacją termiczną i akustyczną spełniającą wymagania hiszpańskiego kodeksu budowlanego.',
  'En skreddersydd fasade som kombinerer ulike overflater med sammenhengende kledning i varme toner, med varme- og lydisolasjon som oppfyller den spanske byggeforskriften.',
  'En skräddarsydd fasad som kombinerar olika ytskikt med sammanhängande beklädnad i varma toner, med värme- och ljudisolering som uppfyller den spanska byggnormen.')
a('.architecture.highlights[1][1]',
  'Tabiques separadores de ladrillo con alta resistencia acústica, con trasdosado de yeso laminado aislado por ambas caras.',
  'Murs séparatifs en brique à forte isolation phonique, avec doublage en plaques de plâtre isolées sur les deux faces.',
  'Trennwände aus schalldämmendem Ziegel, beidseitig mit gedämmter Gipskartonverkleidung.',
  'Разделяющие стены из звукоизолирующего кирпича с утеплённой облицовкой из гипсокартона с обеих сторон.',
  'جدران فاصلة من الطوب العازل للصوت، مع كسوة من ألواح الجبس المعزولة على الوجهين.',
  'Scheidingsmuren van geluidwerende baksteen, aan beide zijden bekleed met geïsoleerde gipskartonplaten.',
  'Ściany działowe z cegły o wysokiej izolacyjności akustycznej, z izolowaną okładziną z płyt gipsowo-kartonowych po obu stronach.',
  'Skillevegger av lydisolerende murstein, med isolert gipsplatekledning på begge sider.',
  'Mellanväggar av ljudisolerande tegel, med isolerad gipsskivebeklädnad på båda sidor.')
a('.architecture.highlights[2][1]',
  'Carpintería de aluminio con rotura de puente térmico, fija, abatible o corredera, con doble acristalamiento, persianas en el salón y los dormitorios y barandillas de vidrio.',
  'Menuiseries en aluminium à rupture de pont thermique, fixes, battantes ou coulissantes, avec double vitrage, stores dans le séjour et les chambres, et garde-corps en verre.',
  'Aluminiumrahmen mit thermischer Trennung, fest, aufschlagend oder schiebend, mit Doppelverglasung, Jalousien im Wohnzimmer und in den Schlafzimmern und Glasbrüstungen.',
  'Алюминиевые рамы с терморазрывом — неподвижные, поворотные или раздвижные — с двойным остеклением, жалюзи в гостиной и спальнях и стеклянными ограждениями.',
  'إطارات ألومنيوم بقاطع حراري، ثابتة أو مفصلية أو منزلقة، بزجاج مزدوج، مع ستائر في غرفة الجلوس وغرف النوم وحواجز زجاجية.',
  'Aluminium kozijnen met thermische onderbreking, vast, draaiend of schuivend, met dubbele beglazing, jaloezieën in de woonkamer en de slaapkamers en glazen balustrades.',
  'Aluminiowa stolarka z przerwą termiczną, stała, otwierana lub przesuwna, z podwójnym szkleniem, żaluzjami w salonie i sypialniach oraz szklanymi balustradami.',
  'Aluminiumsrammer med termisk brudd, faste, sidehengslede eller skyvbare, med dobbeltglass, persienner i stuen og soverommene og glassrekkverk.',
  'Aluminiumbågar med termiskt brott, fasta, öppningsbara eller skjutbara, med dubbelglas, persienner i vardagsrummet och sovrummen och glasräcken.')
a('.architecture.highlights[3][1]',
  'Cubiertas planas transitables en las viviendas, pavimentadas para uso exterior; las demás cubiertas planas se acaban en grava o un material equivalente.',
  'Toitures-terrasses accessibles sur les logements, revêtues pour un usage extérieur ; les autres toitures plates sont finies en gravier ou équivalent.',
  'Begehbare Flachdachterrassen auf den Wohnungen, für die Nutzung im Freien gepflastert; die übrigen Flachdächer sind mit Kies oder Gleichwertigem abgedeckt.',
  'Эксплуатируемые плоские кровли-террасы на квартирах с покрытием для использования на открытом воздухе; остальные плоские кровли покрыты гравием или аналогичным материалом.',
  'أسطح مستوية قابلة للمشي على المساكن، مرصوفة للاستخدام الخارجي؛ أما الأسطح المستوية الأخرى فمكسوة بالحصى أو ما يعادله.',
  'Begaanbare platte daken met terrassen op de woningen, bestraat voor gebruik buiten; de overige platte daken zijn afgewerkt met grind of iets gelijkwaardigs.',
  'Dachy płaskie z tarasami użytkowymi na lokalach, wyłożone do użytku na zewnątrz; pozostałe dachy płaskie wykończone są żwirem lub równoważnym materiałem.',
  'Gangbare flate tak med terrasser på boligene, belagt for bruk utendørs; de øvrige flate takene er ferdigstilt med grus eller tilsvarende.',
  'Gångbara platta tak med terrasser på bostäderna, belagda för utomhusbruk; de övriga platta taken är avslutade med grus eller motsvarande.')

# ---- quality specification ---------------------------------------------------------------------

a('.qualitySpecs.sourceNote',
  'Fuente: el informe de calidades del promotor, que no lleva fecha impresa. Dice que es solo informativo y que puede cambiar con el desarrollo del proyecto, las decisiones en obra o la disponibilidad de materiales, y que cualquier sustitución será de calidad similar.',
  'Source : le rapport de qualité du promoteur, qui ne porte aucune date imprimée. Il indique qu’il est donné à titre d’information et peut évoluer avec le développement du projet, les décisions de chantier ou la disponibilité des matériaux, et que tout remplacement sera de qualité similaire.',
  'Quelle: der Qualitätsbericht des Bauträgers, der kein aufgedrucktes Datum trägt. Er gibt an, dass er nur zur Information dient und sich mit der Entwicklung des Projekts, Entscheidungen auf der Baustelle oder der Verfügbarkeit von Materialien ändern kann und dass jeder Ersatz von ähnlicher Qualität sein wird.',
  'Источник: отчёт о качестве от застройщика, на котором не напечатана дата. В нём сказано, что он носит информационный характер и может меняться по мере развития проекта, по решениям на площадке или в зависимости от наличия материалов, а любая замена будет сопоставимого качества.',
  'المصدر: تقرير الجودة الصادر عن المطوّر، وهو لا يحمل تاريخًا مطبوعًا. ويذكر أنه للاطلاع فقط وقد يتغير مع تطور المشروع أو بحسب قرارات الموقع أو توفر المواد، وأن أي استبدال سيكون بجودة مماثلة.',
  'Bron: het kwaliteitsrapport van de ontwikkelaar, dat geen gedrukte datum draagt. Het zegt dat het alleen ter informatie is en kan veranderen met de ontwikkeling van het project, beslissingen op de bouwplaats of de beschikbaarheid van materialen, en dat elke vervanging van vergelijkbare kwaliteit zal zijn.',
  'Źródło: raport jakości dewelopera, który nie ma wydrukowanej daty. Podaje on, że służy wyłącznie informacji i może się zmienić wraz z rozwojem projektu, decyzjami na budowie lub dostępnością materiałów, a każdy zamiennik będzie podobnej jakości.',
  'Kilde: utbyggerens kvalitetsrapport, som ikke har trykt dato. Den sier at den bare er til informasjon og kan endres med prosjektets utvikling, beslutninger på byggeplassen eller tilgangen på materialer, og at enhver erstatning vil være av tilsvarende kvalitet.',
  'Källa: exploatörens kvalitetsrapport, som inte har något tryckt datum. Den anger att den bara är till information och kan ändras med projektets utveckling, beslut på byggplatsen eller tillgången på material, och att varje ersättning kommer att vara av liknande kvalitet.')
a('.qualitySpecs.groups[0].items[0]',
  'Suelo interior de SPC de gran formato de gama alta, un material resistente al agua, y gres porcelánico en los baños y en las terrazas.',
  'Revêtement de sol intérieur en SPC grand format de gamme supérieure, un matériau résistant à l’eau, et grès cérame dans les salles de bain et sur les terrasses.',
  'Bodenbelag innen aus großformatigem SPC der gehobenen Klasse, einem wasserbeständigen Material, sowie Feinsteinzeugfliesen in den Bädern und auf den Terrassen.',
  'Напольное покрытие внутри — крупноформатный SPC премиальной серии, водостойкий материал, а в ванных комнатах и на террасах — керамогранит.',
  'أرضيات داخلية من مادة SPC كبيرة القياس من فئة راقية، وهي مادة مقاومة للماء، وبلاط بورسلين في الحمامات وعلى التراسات.',
  'Binnenvloeren van grootformaat SPC uit een premiumreeks, een waterbestendig materiaal, en porseleinen tegels in de badkamers en op de terrassen.',
  'Podłogi wewnątrz z wielkoformatowego SPC z linii premium, materiału odpornego na wodę, oraz gres w łazienkach i na tarasach.',
  'Innvendige gulv i storformat SPC av en premiumserie, et vannbestandig materiale, og porselensfliser på badene og på terrassene.',
  'Inomhusgolv i storformat SPC ur en premiumserie, ett vattentåligt material, och klinker i badrummen och på terrasserna.')
a('.qualitySpecs.groups[0].items[1]',
  'Pintura lisa en las paredes interiores y baldosas cerámicas de gran formato en las paredes húmedas de los baños, en tonos elegidos para integrarse con el diseño.',
  'Peinture lisse sur les murs intérieurs et carreaux de céramique grand format sur les murs humides des salles de bain, dans des teintes choisies pour s’accorder au design.',
  'Glatter Anstrich auf den Innenwänden und großformatige Keramikfliesen an den Nassbereichswänden der Bäder, in Tönen, die zum Design passen.',
  'Гладкая покраска внутренних стен и крупноформатная керамическая плитка на мокрых стенах ванных комнат в тонах, подобранных под дизайн.',
  'طلاء أملس على الجدران الداخلية وبلاط سيراميك كبير القياس على الجدران الرطبة في الحمامات، بدرجات لونية اختيرت لتنسجم مع التصميم.',
  'Gladde verf op de binnenmuren en grootformaat keramische tegels op de natte wanden van de badkamers, in tinten die zijn gekozen om bij het ontwerp te passen.',
  'Gładka farba na ścianach wewnętrznych i wielkoformatowe płytki ceramiczne na mokrych ścianach łazienek, w odcieniach dobranych do projektu.',
  'Glatt maling på innerveggene og storformat keramiske fliser på de våte veggene på badene, i toner valgt for å harmonere med designet.',
  'Slät målning på innerväggarna och storformatsplattor i keramik på de våta väggarna i badrummen, i toner valda för att harmoniera med designen.')
a('.qualitySpecs.groups[1].items[0]',
  'Cocina amueblada con muebles altos y bajos, en una combinación de madera, tonos claros y materiales duraderos para la encimera.',
  'Une cuisine équipée avec meubles hauts et bas, associant bois, teintes claires et matériaux de plan de travail durables.',
  'Eine Einbauküche mit Hänge- und Unterschränken, in einer Kombination aus Holz, hellen Tönen und strapazierfähigen Arbeitsplattenmaterialien.',
  'Встроенная кухня с навесными и напольными шкафами, сочетающая дерево, светлые тона и прочные материалы столешницы.',
  'مطبخ مجهّز بخزائن علوية وسفلية، يجمع بين الخشب والدرجات الفاتحة ومواد متينة لسطح العمل.',
  'Een ingebouwde keuken met hang- en staande kasten, in een combinatie van hout, lichte tinten en duurzame werkbladmaterialen.',
  'Kuchnia w zabudowie z szafkami wiszącymi i stojącymi, łącząca drewno, jasne tony i trwałe materiały blatów.',
  'Et innredet kjøkken med over- og underskap, i en blanding av tre, lyse toner og slitesterke benkeplatematerialer.',
  'Ett inrett kök med över- och underskåp, i en blandning av trä, ljusa toner och slitstarka bänkskivematerial.')
a('.qualitySpecs.groups[1].items[1]',
  'Electrodomésticos de marca premium: placa de inducción, campana extractora, horno eléctrico, frigorífico integrado, lavavajillas integrado, lavadora y microondas.',
  'Électroménager de marque premium : table à induction, hotte aspirante, four électrique, réfrigérateur intégré, lave-vaisselle intégré, lave-linge et four à micro-ondes.',
  'Geräte einer Premiummarke: Induktionskochfeld, Dunstabzugshaube, Elektrobackofen, integrierter Kühlschrank, integrierter Geschirrspüler, Waschmaschine und Mikrowelle.',
  'Техника премиальных марок: индукционная варочная панель, вытяжка, электрическая духовка, встроенный холодильник, встроенная посудомоечная машина, стиральная машина и микроволновая печь.',
  'أجهزة من علامة راقية: موقد حثّي ومدخنة شفط وفرن كهربائي وثلاجة مدمجة وغسالة أطباق مدمجة وغسالة ملابس وميكروويف.',
  'Apparatuur van een premiummerk: een inductiekookplaat, een afzuigkap, een elektrische oven, een ingebouwde koelkast, een ingebouwde vaatwasser, een wasmachine en een magnetron.',
  'Sprzęt marki premium: płyta indukcyjna, okap, piekarnik elektryczny, zintegrowana lodówka, zintegrowana zmywarka, pralka i kuchenka mikrofalowa.',
  'Hvitevarer fra et premiummerke: induksjonstopp, avtrekksvifte, elektrisk stekeovn, integrert kjøleskap, integrert oppvaskmaskin, vaskemaskin og mikrobølgeovn.',
  'Apparater från ett premiummärke: induktionshäll, köksfläkt, elektrisk ugn, integrerat kylskåp, integrerad diskmaskin, tvättmaskin och mikrovågsugn.')
a('.qualitySpecs.groups[2].items[0]',
  'Inodoros de diseño con doble descarga y lavabos empotrados o sobre encimera con grifería y accesorios según el proyecto.',
  'WC design avec chasse d’eau à double commande, et vasques encastrées ou à poser avec robinetterie et accessoires selon le projet.',
  'Design-WCs mit Zweimengen-Spülung sowie Einbau- oder Aufsatzwaschbecken mit Armaturen und Zubehör gemäß Planung.',
  'Дизайнерские унитазы с двойным смывом и встроенные или накладные раковины со смесителями и фурнитурой по проекту.',
  'مراحيض بتصميم عصري بنظام تصريف مزدوج، وأحواض غسل مدمجة أو فوق السطح مع الحنفيات والتجهيزات وفق التصميم.',
  'Designtoiletten met tweestandenspoeling en inbouw- of opbouwwastafels met kranen en fittingen volgens het ontwerp.',
  'Designerskie miski ustępowe z dwustopniowym spłukiwaniem oraz umywalki wpuszczane lub nablatowe z bateriami i armaturą zgodnie z projektem.',
  'Designtoaletter med tosidig spyling og innfelte eller påmonterte servanter med kraner og beslag som angitt i designet.',
  'Designtoaletter med dubbelspolning och infällda eller fristående tvättställ med kranar och beslag enligt designen.')
a('.qualitySpecs.groups[2].items[1]',
  'Plato de ducha de perfil bajo y mampara de ducha en el baño principal, y grifería de marca premium en los lavabos y las duchas.',
  'Un receveur de douche extra-plat et une paroi de douche dans la salle de bain principale, et une robinetterie de marque premium sur les vasques et les douches.',
  'Eine flache Duschwanne und eine Duschabtrennung im Hauptbad sowie Armaturen einer Premiummarke an Waschbecken und Duschen.',
  'Плоский душевой поддон и душевая перегородка в главной ванной комнате, смесители премиальной марки на раковинах и в душевых.',
  'حوض دش منخفض الارتفاع ومقصورة دش في الحمام الرئيسي، وحنفيات من علامة راقية على الأحواض والدشّات.',
  'Een lage douchebak en een douchewand in de hoofdbadkamer, en kranen van een premiummerk op de wastafels en in de douches.',
  'Płaski brodzik i kabina prysznicowa w łazience głównej oraz baterie marki premium przy umywalkach i prysznicach.',
  'En lav dusjkum og en dusjvegg på hovedbadet, og kraner fra et premiummerke på servantene og i dusjene.',
  'En låg duschkar och en duschvägg i huvudbadrummet, och kranar från ett premiummärke på tvättställen och i duscharna.')
a('.qualitySpecs.groups[3].items[0]',
  'Carpintería de aluminio con rotura de puente térmico y doble acristalamiento, persianas en el salón y los dormitorios y barandillas de vidrio fijadas con un perfil.',
  'Menuiseries en aluminium à rupture de pont thermique avec double vitrage, stores dans le séjour et les chambres, et garde-corps en verre fixés par un profilé.',
  'Aluminiumrahmen mit thermischer Trennung und Doppelverglasung, Jalousien im Wohnzimmer und in den Schlafzimmern sowie Glasbrüstungen, die mit einem Profil befestigt sind.',
  'Алюминиевые рамы с терморазрывом и двойным остеклением, жалюзи в гостиной и спальнях и стеклянные ограждения, закреплённые в профиле.',
  'إطارات ألومنيوم بقاطع حراري وزجاج مزدوج، وستائر في غرفة الجلوس وغرف النوم، وحواجز زجاجية مثبتة بواسطة بروفيل.',
  'Aluminium kozijnen met thermische onderbreking en dubbele beglazing, jaloezieën in de woonkamer en de slaapkamers, en glazen balustrades die met een profiel zijn bevestigd.',
  'Aluminiowa stolarka z przerwą termiczną i podwójnym szkleniem, żaluzje w salonie i sypialniach oraz szklane balustrady mocowane w profilu.',
  'Aluminiumsrammer med termisk brudd og dobbeltglass, persienner i stuen og soverommene og glassrekkverk som er festet med en profil.',
  'Aluminiumbågar med termiskt brott och dubbelglas, persienner i vardagsrummet och sovrummen och glasräcken som är fästa med en profil.')
a('.qualitySpecs.groups[3].items[1]',
  'Una puerta de seguridad blindada en cada vivienda, puertas interiores lacadas con manillas de diseño, rodapiés a juego y armarios empotrados forrados por completo, con barra para colgar y espacio de almacenaje.',
  'Une porte de sécurité renforcée pour chaque logement, des portes intérieures laquées avec poignées design, des plinthes assorties et des placards encastrés entièrement habillés, avec une tringle et des rangements.',
  'Eine einbruchhemmende Wohnungstür bei jeder Wohnung, lackierte Innentüren mit Designergriffen, passende Sockelleisten sowie Einbauschränke, die komplett ausgekleidet sind, mit Kleiderstange und Stauraum.',
  'Усиленная входная дверь в каждой квартире, лакированные межкомнатные двери с дизайнерскими ручками, плинтусы в тон и встроенные шкафы с полной внутренней отделкой, со штангой для одежды и местом для хранения.',
  'باب أمان معزَّز لكل مسكن، وأبواب داخلية مطلية بالورنيش بمقابض عصرية، وألواح تنورة متناسقة، وخزائن مدمجة مبطَّنة بالكامل مع عمود للتعليق ومساحة للتخزين.',
  'Een versterkte veiligheidsdeur bij elke woning, gelakte binnendeuren met designhandgrepen, bijpassende plinten en inbouwkasten die volledig zijn bekleed, met een hangstang en opbergruimte.',
  'Wzmocnione drzwi wejściowe w każdym lokalu, lakierowane drzwi wewnętrzne z designerskimi klamkami, pasujące listwy przypodłogowe oraz szafy w zabudowie w pełni wykończone w środku, z drążkiem na ubrania i miejscem do przechowywania.',
  'En forsterket sikkerhetsdør til hver bolig, lakkerte innerdører med designhåndtak, tilpassede gulvlister og innebygde garderobeskap som er kledd helt igjennom, med kleshenger og oppbevaring.',
  'En förstärkt säkerhetsdörr till varje bostad, lackade innerdörrar med designhandtag, matchande golvlister och inbyggda garderober som är klädda genomgående, med klädstång och förvaring.')
a('.qualitySpecs.groups[4].items[0]',
  'Agua caliente con una bomba de calor aerotérmica de alta eficiencia energética, y aire acondicionado por conductos a través del falso techo.',
  'Eau chaude produite par une pompe à chaleur aérothermique à haut rendement énergétique, et climatisation gainable passant par le faux plafond.',
  'Warmwasser aus einer energieeffizienten Luft-Wasser-Wärmepumpe und eine Klimaanlage, deren Kanäle durch die abgehängte Decke verlaufen.',
  'Горячая вода от энергоэффективного теплового насоса «воздух — вода» и кондиционирование с воздуховодами в подвесном потолке.',
  'ماء ساخن من مضخة حرارية هوائية عالية الكفاءة في استهلاك الطاقة، وتكييف هواء بقنوات عبر السقف المعلَّق.',
  'Warm water uit een energiezuinige lucht-waterwarmtepomp en airconditioning met kanalen door het verlaagde plafond.',
  'Ciepła woda z energooszczędnej pompy ciepła powietrze-woda oraz klimatyzacja kanałowa prowadzona w suficie podwieszanym.',
  'Varmtvann fra en energieffektiv luft-til-vann-varmepumpe, og klimaanlegg med kanaler gjennom det nedsenkede taket.',
  'Varmvatten från en energieffektiv luft-vatten-värmepump, och luftkonditionering med kanaler genom undertaket.')
a('.qualitySpecs.groups[4].items[1]',
  'Toma de telecomunicaciones en todas las estancias excepto los baños, y aparatos eléctricos con mecanismos de diseño.',
  'Une prise de télécommunications dans toutes les pièces sauf les salles de bain, et des appareillages électriques à mécanismes design.',
  'Ein Telekommunikationsanschluss in jedem Raum außer den Bädern sowie Elektroinstallationen mit Designerschaltern.',
  'Телекоммуникационная розетка в каждой комнате, кроме ванных, и электрофурнитура с дизайнерскими механизмами.',
  'مأخذ اتصالات في كل غرفة باستثناء الحمامات، وتجهيزات كهربائية بمفاتيح عصرية.',
  'Een telecomaansluiting in elke kamer behalve de badkamers, en elektrische schakelmaterialen met designmechanismen.',
  'Przyłącze telekomunikacyjne w każdym pomieszczeniu poza łazienkami oraz osprzęt elektryczny z designerskimi mechanizmami.',
  'Telekommunikasjonsuttak i alle rom unntatt badene, og elektrisk installasjon med designmekanismer.',
  'Ett telekommunikationsuttag i varje rum utom badrummen, och elinstallation med designmekanismer.')
a('.qualitySpecs.groups[5].items[0]',
  'Piscinas comunitarias exteriores con cloración salina, en jardines ajardinados con una terraza solárium, y un spa interior con piscina climatizada, sauna y duchas de experiencias, conectado con el gimnasio y los vestuarios.',
  'Piscines communes extérieures à électrolyse au sel, dans des jardins paysagers avec une terrasse solarium, et un spa intérieur avec piscine chauffée, sauna et douches sensorielles, relié à la salle de sport et aux vestiaires.',
  'Gemeinschaftspools im Freien mit Salzwasserchlorierung, in angelegten Gärten mit einer Sonnenterrasse, sowie ein Indoor-Spa mit beheiztem Pool, Sauna und Erlebnisduschen, verbunden mit dem Fitnessraum und den Umkleiden.',
  'Общие бассейны на открытом воздухе с хлорированием солью, в благоустроенных садах с солнечной террасой, и спа в помещении с подогреваемым бассейном, сауной и душами впечатлений, соединённое с тренажёрным залом и раздевалками.',
  'مسابح مشتركة خارجية بالكلورة الملحية، في حدائق مُنسَّقة مع تراس للتشمّس، وسبا داخلي بمسبح مدفأ وساونا ودشّات تجريبية، متصل بالصالة الرياضية وغرف تبديل الملابس.',
  'Gemeenschappelijke buitenzwembaden met zoutwaterchlorering, in aangelegde tuinen met een zonneterras, en een binnenspa met een verwarmd zwembad, een sauna en belevingsdouches, verbonden met de fitnessruimte en de kleedkamers.',
  'Wspólne baseny zewnętrzne z chlorowaniem solnym, w zagospodarowanych ogrodach z tarasem słonecznym, oraz spa w budynku z podgrzewanym basenem, sauną i prysznicami wrażeń, połączone z siłownią i szatniami.',
  'Utendørs fellesbasseng med saltvannsklorering, i opparbeidede hager med en solterrasse, og et innendørs spa med oppvarmet basseng, badstue og opplevelsesdusjer, forbundet med treningsrommet og garderobene.',
  'Gemensamma utomhuspooler med saltvattenklorering, i planterade trädgårdar med en solterrass, och ett inomhusspa med uppvärmd pool, bastu och upplevelseduschar, förbundet med gymmet och omklädningsrummen.')
a('.qualitySpecs.groups[5].items[1]',
  'Un gimnasio totalmente equipado, un espacio de coworking con kitchenette y aseo, una puerta de garaje motorizada con mando a distancia y pavimento de calidad superior.',
  'Une salle de sport entièrement équipée, un espace de coworking avec kitchenette et toilettes, une porte de garage motorisée avec télécommande et un dallage haut de gamme.',
  'Ein voll ausgestatteter Fitnessraum, ein Coworking-Bereich mit Küchenzeile und Toilette, ein motorisiertes Garagentor mit Fernbedienung und hochwertiger Bodenbelag.',
  'Полностью оборудованный тренажёрный зал, коворкинг с мини-кухней и санузлом, гаражные ворота с электроприводом и пультом и покрытие премиального класса.',
  'صالة رياضية مجهزة بالكامل، ومساحة للعمل المشترك مع مطبخ صغير ودورة مياه، وباب مرآب آلي بجهاز تحكم عن بعد، وأرضيات رصف راقية.',
  'Een volledig uitgeruste fitnessruimte, een coworkingruimte met kitchenette en toilet, een gemotoriseerde garagedeur met afstandsbediening en hoogwaardige bestrating.',
  'W pełni wyposażona siłownia, przestrzeń coworkingowa z aneksem kuchennym i toaletą, brama garażowa z napędem i pilotem oraz nawierzchnie wysokiej jakości.',
  'Et fullt utstyrt treningsrom, et coworking-område med tekjøkken og toalett, en motorisert garasjeport med fjernkontroll og belegg av høy kvalitet.',
  'Ett fullt utrustat gym, ett coworking-område med pentry och toalett, en motoriserad garageport med fjärrkontroll och markbeläggning av hög kvalitet.')

# ---- residences ---------------------------------------------------------------------------------

a('.residences.copy',
  'Las 17 viviendas con precio se enumeran a continuación con su superficie interior, sus terrazas y, cuando la hay, su jardín. Los documentos no dan otro nombre para un tipo de vivienda.',
  'Les 17 logements avec un prix sont listés ci-dessous avec leur surface intérieure, leurs terrasses et, le cas échéant, leur jardin. Les documents ne donnent aucun autre nom pour un type de logement.',
  'Die 17 Wohnungen mit Preis sind unten mit ihrer Innenfläche, ihren Terrassen und, falls vorhanden, ihrem Garten aufgeführt. Die Dokumente geben keine andere Bezeichnung für einen Wohnungstyp an.',
  'Ниже перечислены 17 квартир с ценой: с внутренней площадью, террасами и, где он есть, садом. Других названий типов квартир в документах нет.',
  'المساكن السبعة عشر التي لها سعر مدرجة أدناه بمساحتها الداخلية وتراساتها وحديقتها حيثما وُجدت. ولا تذكر المستندات أي اسم آخر لنوع المسكن.',
  'De 17 woningen met een prijs staan hieronder met hun binnenoppervlak, hun terrassen en, waar aanwezig, hun tuin. De documenten geven geen andere naam voor een woningtype.',
  'Poniżej wymieniono 17 lokali z ceną, z ich powierzchnią wewnętrzną, tarasami i, jeśli jest, ogrodem. Dokumenty nie podają innej nazwy typu lokalu.',
  'De 17 boligene med pris er oppført nedenfor med innvendig areal, terrasser og, der det finnes, hage. Dokumentene oppgir ikke noe annet navn på en boligtype.',
  'De 17 bostäderna med pris är listade nedan med sin invändiga yta, sina terrasser och, där det finns en, sin trädgård. Dokumenten anger inget annat namn på en bostadstyp.')
a('.residences.items[0].points[0]',
  '11 de las 17 tienen dos dormitorios y dos baños, con entre {N66.91} y {N77.39} {U} interiores, de {E473000} a {E572000}.',
  '11 des 17 ont deux chambres et deux salles de bain, avec de {N66.91} à {N77.39} {U} intérieurs, de {E473000} à {E572000}.',
  '11 der 17 haben zwei Schlafzimmer und zwei Bäder, mit {N66.91} bis {N77.39} {U} Innenfläche, von {E473000} bis {E572000}.',
  '11 из 17 имеют две спальни и две ванные комнаты, с внутренней площадью от {N66.91} до {N77.39} {U}, от {E473000} до {E572000}.',
  '11 من المساكن السبعة عشر لها غرفتا نوم وحمامان، بمساحة داخلية من {N66.91} إلى {N77.39} {U}، بأسعار من {E473000} إلى {E572000}.',
  '11 van de 17 hebben twee slaapkamers en twee badkamers, met {N66.91} tot {N77.39} {U} binnenoppervlak, van {E473000} tot {E572000}.',
  '11 z 17 ma dwie sypialnie i dwie łazienki, z powierzchnią wewnętrzną od {N66.91} do {N77.39} {U}, w cenie od {E473000} do {E572000}.',
  '11 av de 17 har to soverom og to bad, med {N66.91} til {N77.39} {U} innvendig areal, fra {E473000} til {E572000}.',
  '11 av de 17 har två sovrum och två badrum, med {N66.91} till {N77.39} {U} invändig yta, från {E473000} till {E572000}.')
a('.residences.items[0].points[1]',
  'Todas están en la planta baja o en la primera. Sus terrazas van de {N16.42} {U} (02-01-01-C) a {N37.23} {U} (03-02-00-C), y la 03-02-00-A tiene además un jardín de {N26.45} {U}.',
  'Tous sont au rez-de-chaussée ou au premier étage. Leurs terrasses vont de {N16.42} {U} (02-01-01-C) à {N37.23} {U} (03-02-00-C), et le 03-02-00-A a aussi un jardin de {N26.45} {U}.',
  'Alle liegen im Erdgeschoss oder im ersten Obergeschoss. Ihre Terrassen reichen von {N16.42} {U} (02-01-01-C) bis {N37.23} {U} (03-02-00-C), und die 03-02-00-A hat zusätzlich einen Garten von {N26.45} {U}.',
  'Все расположены на первом или втором этаже. Их террасы — от {N16.42} {U} (02-01-01-C) до {N37.23} {U} (03-02-00-C), а у 03-02-00-A есть ещё и сад {N26.45} {U}.',
  'جميعها في الطابق الأرضي أو الأول. وتتراوح تراساتها بين {N16.42} {U} (02-01-01-C) و{N37.23} {U} (03-02-00-C)، ويضم المسكن 03-02-00-A كذلك حديقة بمساحة {N26.45} {U}.',
  'Alle liggen op de begane grond of de eerste verdieping. Hun terrassen variëren van {N16.42} {U} (02-01-01-C) tot {N37.23} {U} (03-02-00-C), en 03-02-00-A heeft ook een tuin van {N26.45} {U}.',
  'Wszystkie znajdują się na parterze lub pierwszym piętrze. Ich tarasy mają od {N16.42} {U} (02-01-01-C) do {N37.23} {U} (03-02-00-C), a lokal 03-02-00-A ma też ogród o powierzchni {N26.45} {U}.',
  'Alle ligger i første eller andre etasje. Terrassene varierer fra {N16.42} {U} (02-01-01-C) til {N37.23} {U} (03-02-00-C), og 03-02-00-A har i tillegg en hage på {N26.45} {U}.',
  'Alla ligger på bottenvåningen eller första våningen. Terrasserna varierar från {N16.42} {U} (02-01-01-C) till {N37.23} {U} (03-02-00-C), och 03-02-00-A har dessutom en trädgård på {N26.45} {U}.')
a('.residences.items[1].points[0]',
  '6 de las 17 tienen tres dormitorios y dos baños, con entre {N85.64} y {N91.29} {U} interiores, de {E560000} a {E687000}.',
  '6 des 17 ont trois chambres et deux salles de bain, avec de {N85.64} à {N91.29} {U} intérieurs, de {E560000} à {E687000}.',
  '6 der 17 haben drei Schlafzimmer und zwei Bäder, mit {N85.64} bis {N91.29} {U} Innenfläche, von {E560000} bis {E687000}.',
  '6 из 17 имеют три спальни и две ванные комнаты, с внутренней площадью от {N85.64} до {N91.29} {U}, от {E560000} до {E687000}.',
  '6 من المساكن السبعة عشر لها ثلاث غرف نوم وحمامان، بمساحة داخلية من {N85.64} إلى {N91.29} {U}، بأسعار من {E560000} إلى {E687000}.',
  '6 van de 17 hebben drie slaapkamers en twee badkamers, met {N85.64} tot {N91.29} {U} binnenoppervlak, van {E560000} tot {E687000}.',
  '6 z 17 ma trzy sypialnie i dwie łazienki, z powierzchnią wewnętrzną od {N85.64} do {N91.29} {U}, w cenie od {E560000} do {E687000}.',
  '6 av de 17 har tre soverom og to bad, med {N85.64} til {N91.29} {U} innvendig areal, fra {E560000} til {E687000}.',
  '6 av de 17 har tre sovrum och två badrum, med {N85.64} till {N91.29} {U} invändig yta, från {E560000} till {E687000}.')
a('.residences.items[1].points[1]',
  'Dos están en la planta baja, tres en la primera y una, la 04-01-02-A, en la segunda. Sus terrazas van de {N25.01} {U} (04-02-00-B) a {N79.42} {U} (04-03-00-A), la mayor de la lista.',
  'Deux sont au rez-de-chaussée, trois au premier étage et un, le 04-01-02-A, au deuxième. Leurs terrasses vont de {N25.01} {U} (04-02-00-B) à {N79.42} {U} (04-03-00-A), la plus grande de la liste.',
  'Zwei liegen im Erdgeschoss, drei im ersten Obergeschoss und eine, die 04-01-02-A, im zweiten. Ihre Terrassen reichen von {N25.01} {U} (04-02-00-B) bis {N79.42} {U} (04-03-00-A), der größten auf der Liste.',
  'Две расположены на первом этаже, три — на втором и одна, 04-01-02-A, — на третьем. Их террасы — от {N25.01} {U} (04-02-00-B) до {N79.42} {U} (04-03-00-A), самой большой в списке.',
  'اثنان منها في الطابق الأرضي وثلاثة في الأول وواحد، هو 04-01-02-A، في الثاني. وتتراوح تراساتها بين {N25.01} {U} (04-02-00-B) و{N79.42} {U} (04-03-00-A)، وهو الأكبر في القائمة.',
  'Twee liggen op de begane grond, drie op de eerste verdieping en één, 04-01-02-A, op de tweede. Hun terrassen variëren van {N25.01} {U} (04-02-00-B) tot {N79.42} {U} (04-03-00-A), het grootste van de lijst.',
  'Dwa znajdują się na parterze, trzy na pierwszym piętrze, a jeden, 04-01-02-A, na drugim. Ich tarasy mają od {N25.01} {U} (04-02-00-B) do {N79.42} {U} (04-03-00-A), czyli największy na liście.',
  'To ligger i første etasje, tre i andre og én, 04-01-02-A, i tredje. Terrassene varierer fra {N25.01} {U} (04-02-00-B) til {N79.42} {U} (04-03-00-A), den største på listen.',
  'Två ligger på bottenvåningen, tre på första våningen och en, 04-01-02-A, på andra. Terrasserna varierar från {N25.01} {U} (04-02-00-B) till {N79.42} {U} (04-03-00-A), den största på listan.')
a('.residences.items[2].points[0]',
  'La plaza o plazas de garaje y el trastero que nombra la lista de precios, en los niveles S-1 y S-2, que según la lista están incluidos en el precio.',
  'La ou les places de parking et la cave que nomme la liste de prix, aux niveaux S-1 et S-2, qui sont compris dans le prix selon la liste.',
  'Der Stellplatz oder die Stellplätze und der Abstellraum, die die Preisliste nennt, auf den Ebenen S-1 und S-2, die laut Liste im Preis enthalten sind.',
  'Машиноместо или машиноместа и кладовая, названные в прайс-листе, на уровнях S-1 и S-2; по сведениям списка, они включены в цену.',
  'موقف السيارات أو مواقفها والمخزن المذكوران في قائمة الأسعار، في المستويين S-1 وS-2، وهي بحسب القائمة مشمولة في السعر.',
  'De parkeerplaats of parkeerplaatsen en de berging die de prijslijst noemt, op de niveaus S-1 en S-2, die volgens de lijst in de prijs zijn inbegrepen.',
  'Miejsce lub miejsca postojowe oraz komórka lokatorska wskazane w cenniku, na poziomach S-1 i S-2, które według cennika są wliczone w cenę.',
  'Parkeringsplassen eller -plassene og bodet som er oppgitt i prislisten, på nivåene S-1 og S-2, som ifølge listen er inkludert i prisen.',
  'Parkeringsplatsen eller -platserna och förrådet som anges i prislistan, på planen S-1 och S-2, som enligt listan ingår i priset.')
a('.residences.items[2].points[1]',
  'Una cocina amueblada con los electrodomésticos que enumera el informe de calidades, y aire acondicionado por conductos a través del techo.',
  'Une cuisine équipée avec l’électroménager que liste le rapport de qualité, et une climatisation gainable passant par le plafond.',
  'Eine Einbauküche mit den im Qualitätsbericht aufgeführten Geräten und eine Klimaanlage, deren Kanäle durch die Decke verlaufen.',
  'Встроенная кухня с техникой, перечисленной в отчёте о качестве, и кондиционирование с воздуховодами в потолке.',
  'مطبخ مجهّز بالأجهزة المذكورة في تقرير الجودة، وتكييف هواء بقنوات عبر السقف.',
  'Een ingebouwde keuken met de apparatuur uit het kwaliteitsrapport en airconditioning met kanalen door het plafond.',
  'Kuchnia w zabudowie ze sprzętem wymienionym w raporcie jakości oraz klimatyzacja kanałowa prowadzona w suficie.',
  'Et innredet kjøkken med apparatene som kvalitetsrapporten oppgir, og klimaanlegg med kanaler gjennom taket.',
  'Ett inrett kök med de apparater som kvalitetsrapporten anger, och luftkonditionering med kanaler genom taket.')

# ---- lifestyle, location -------------------------------------------------------------------------

a('.lifestyle.headlineHtml',
  'Un spa interior, <em>un gimnasio</em> y una sala de coworking', 'Un spa intérieur, <em>une salle de sport</em> et un espace de coworking',
  'Ein Indoor-Spa, <em>ein Fitnessraum</em> und ein Coworking-Raum', 'Спа в помещении, <em>тренажёрный зал</em> и коворкинг',
  'سبا داخلي، <em>وصالة رياضية</em> وقاعة للعمل المشترك', 'Een binnenspa, <em>een fitnessruimte</em> en een coworkingruimte',
  'Spa w budynku, <em>siłownia</em> i sala coworkingowa', 'Et innendørs spa, <em>et treningsrom</em> og et coworking-rom',
  'Ett inomhusspa, <em>ett gym</em> och ett coworking-rum')
a('.lifestyle.copy',
  'El folleto y el informe de calidades enumeran las zonas comunes sin superficies ni horarios, de modo que confirmamos qué está construido y abierto antes de cualquier reserva.',
  'La brochure et le rapport de qualité listent les parties communes sans surfaces ni détails d’ouverture ; nous confirmons donc ce qui est construit et ouvert avant toute réservation.',
  'Die Broschüre und der Qualitätsbericht führen die Gemeinschaftsflächen ohne Größen- oder Öffnungsangaben auf, daher bestätigen wir vor jeder Reservierung, was gebaut und geöffnet ist.',
  'В брошюре и отчёте о качестве общие зоны перечислены без площадей и сведений о режиме работы, поэтому до любого бронирования мы подтверждаем, что построено и открыто.',
  'يسرد الكتيّب وتقرير الجودة المرافق المشتركة دون مساحات أو تفاصيل عن أوقات التشغيل، لذلك نؤكد ما تم بناؤه وما هو مفتوح قبل أي حجز.',
  'De brochure en het kwaliteitsrapport noemen de gemeenschappelijke ruimtes zonder oppervlaktes of openingsgegevens, dus wij bevestigen wat is gebouwd en geopend vóór elke reservering.',
  'Broszura i raport jakości wymieniają części wspólne bez powierzchni i informacji o godzinach otwarcia, dlatego przed każdą rezerwacją potwierdzamy, co zostało zbudowane i jest czynne.',
  'Brosjyren og kvalitetsrapporten lister fellesarealene uten størrelser eller åpningsdetaljer, så vi bekrefter hva som er bygget og åpent før enhver reservasjon.',
  'Broschyren och kvalitetsrapporten listar de gemensamma ytorna utan storlekar eller öppettider, så vi bekräftar vad som är byggt och öppet före varje bokning.')
a('.lifestyle.panels[0][1]',
  'El folleto cuenta dos piscinas. El informe de calidades enumera piscinas comunitarias exteriores con cloración salina, en jardines ajardinados con una terraza solárium. En las imágenes del promotor, las piscinas tienen tumbonas y sombrillas ante una ladera con muros de piedra.',
  'La brochure compte deux piscines. Le rapport de qualité liste des piscines communes extérieures à électrolyse au sel, dans des jardins paysagers avec une terrasse solarium. Sur les images du promoteur, les piscines ont des transats et des parasols devant un talus aux murs de pierre.',
  'Die Broschüre zählt zwei Schwimmbäder. Der Qualitätsbericht führt Gemeinschaftspools im Freien mit Salzwasserchlorierung auf, in angelegten Gärten mit einer Sonnenterrasse. Auf den Bildern des Bauträgers haben die Pools Liegen und Sonnenschirme vor einem Hang mit Steinmauern.',
  'В брошюре указаны два бассейна. В отчёте о качестве перечислены общие бассейны на открытом воздухе с хлорированием солью в благоустроенных садах с солнечной террасой. На изображениях застройщика у бассейнов шезлонги и зонты на фоне склона с каменными стенами.',
  'يذكر الكتيّب مسبحين. ويسرد تقرير الجودة مسابح مشتركة خارجية بالكلورة الملحية في حدائق مُنسَّقة مع تراس للتشمّس. وفي صور المطوّر تحيط بالمسبحين كراسٍ للاستلقاء ومظلات أمام سفح ذي جدران حجرية.',
  'De brochure telt twee zwembaden. Het kwaliteitsrapport noemt gemeenschappelijke buitenzwembaden met zoutwaterchlorering, in aangelegde tuinen met een zonneterras. Op de beelden van de ontwikkelaar hebben de zwembaden ligbedden en parasols tegen een helling met stenen muren.',
  'Broszura wymienia dwa baseny. Raport jakości podaje wspólne baseny zewnętrzne z chlorowaniem solnym, w zagospodarowanych ogrodach z tarasem słonecznym. Na obrazach dewelopera baseny mają leżaki i parasole na tle zbocza z kamiennymi murami.',
  'Brosjyren oppgir to svømmebasseng. Kvalitetsrapporten oppgir utendørs fellesbasseng med saltvannsklorering, i opparbeidede hager med en solterrasse. På utbyggerens bilder har bassengene solsenger og parasoller foran en skråning med steinmurer.',
  'Broschyren anger två simbassänger. Kvalitetsrapporten anger gemensamma utomhuspooler med saltvattenklorering, i planterade trädgårdar med en solterrass. På exploatörens bilder har poolerna solstolar och parasoller framför en sluttning med stenmurar.')
a('.lifestyle.panels[1][1]',
  'Un spa interior con piscina climatizada, sauna y duchas de experiencias, conectado con el gimnasio y los vestuarios, tal como lo enumera el informe de calidades.',
  'Un spa intérieur avec piscine chauffée, sauna et douches sensorielles, relié à la salle de sport et aux vestiaires, tel que le liste le rapport de qualité.',
  'Ein Indoor-Spa mit beheiztem Pool, Sauna und Erlebnisduschen, verbunden mit dem Fitnessraum und den Umkleiden, wie im Qualitätsbericht aufgeführt.',
  'Спа в помещении с подогреваемым бассейном, сауной и душами впечатлений, соединённое с тренажёрным залом и раздевалками, как указано в отчёте о качестве.',
  'سبا داخلي بمسبح مدفأ وساونا ودشّات تجريبية، متصل بالصالة الرياضية وغرف تبديل الملابس، كما يسرده تقرير الجودة.',
  'Een binnenspa met een verwarmd zwembad, een sauna en belevingsdouches, verbonden met de fitnessruimte en de kleedkamers, zoals het kwaliteitsrapport het noemt.',
  'Spa w budynku z podgrzewanym basenem, sauną i prysznicami wrażeń, połączone z siłownią i szatniami, tak jak podaje raport jakości.',
  'Et innendørs spa med oppvarmet basseng, badstue og opplevelsesdusjer, forbundet med treningsrommet og garderobene, slik kvalitetsrapporten oppgir det.',
  'Ett inomhusspa med uppvärmd pool, bastu och upplevelseduschar, förbundet med gymmet och omklädningsrummen, så som kvalitetsrapporten anger det.')
a('.lifestyle.panels[2][1]',
  'Un gimnasio totalmente equipado y un espacio de coworking con kitchenette y aseo, abiertos a todos los residentes. Los documentos no dan superficies ni lista de equipamiento.',
  'Une salle de sport entièrement équipée et un espace de coworking avec kitchenette et toilettes, ouverts à tous les résidents. Les documents ne donnent ni surfaces ni liste d’équipements.',
  'Ein voll ausgestatteter Fitnessraum und ein Coworking-Bereich mit Küchenzeile und Toilette, für alle Bewohner zugänglich. Die Dokumente nennen weder Größen noch eine Geräteliste.',
  'Полностью оборудованный тренажёрный зал и коворкинг с мини-кухней и санузлом, открытые для всех жильцов. В документах нет ни площадей, ни списка оборудования.',
  'صالة رياضية مجهزة بالكامل ومساحة للعمل المشترك مع مطبخ صغير ودورة مياه، مفتوحتان لجميع السكان. ولا تذكر المستندات مساحات ولا قائمة بالمعدات.',
  'Een volledig uitgeruste fitnessruimte en een coworkingruimte met kitchenette en toilet, open voor alle bewoners. De documenten geven geen oppervlaktes en geen lijst met apparatuur.',
  'W pełni wyposażona siłownia oraz przestrzeń coworkingowa z aneksem kuchennym i toaletą, dostępne dla wszystkich mieszkańców. Dokumenty nie podają powierzchni ani listy wyposażenia.',
  'Et fullt utstyrt treningsrom og et coworking-område med tekjøkken og toalett, åpne for alle beboere. Dokumentene oppgir verken størrelser eller utstyrsliste.',
  'Ett fullt utrustat gym och ett coworking-område med pentry och toalett, öppna för alla boende. Dokumenten anger varken storlekar eller utrustningslista.')
a('.lifestyle.panels[3][1]',
  'Jardines ajardinados con vegetación mediterránea típica. El folleto dice que el plan de plantación utiliza especies autóctonas adaptadas al clima para reducir el consumo de agua.',
  'Des jardins paysagers à la végétation méditerranéenne typique. La brochure indique que le plan de plantation utilise des espèces locales adaptées au climat pour réduire la consommation d’eau.',
  'Angelegte Gärten mit typisch mediterraner Bepflanzung. Die Broschüre gibt an, dass der Bepflanzungsplan einheimische, an das Klima angepasste Arten verwendet, um den Wasserverbrauch zu senken.',
  'Благоустроенные сады с типичной средиземноморской растительностью. В брошюре сказано, что в плане озеленения используются местные виды, приспособленные к климату, чтобы сократить расход воды.',
  'حدائق مُنسَّقة بنباتات متوسطية نموذجية. ويذكر الكتيّب أن خطة الزراعة تعتمد أنواعًا محلية متكيّفة مع المناخ لتقليل استهلاك المياه.',
  'Aangelegde tuinen met typisch mediterrane beplanting. De brochure zegt dat het beplantingsplan inheemse, aan het klimaat aangepaste soorten gebruikt om het waterverbruik te verminderen.',
  'Zagospodarowane ogrody z typową śródziemnomorską roślinnością. Broszura podaje, że plan nasadzeń wykorzystuje gatunki rodzime, dostosowane do klimatu, aby ograniczyć zużycie wody.',
  'Opparbeidede hager med typisk middelhavsbeplantning. Brosjyren sier at beplantningsplanen bruker stedegne arter tilpasset klimaet for å redusere vannforbruket.',
  'Planterade trädgårdar med typisk medelhavsväxtlighet. Broschyren anger att planteringsplanen använder inhemska, klimatanpassade arter för att minska vattenförbrukningen.')
a('.location.headlineHtml',
  'Estepona, <em>al oeste del casco urbano</em>', 'Estepona, <em>à l’ouest de la ville</em>', 'Estepona, <em>westlich der Stadt</em>', 'Эстепона, <em>к западу от города</em>',
  'إستيبونا، <em>غرب البلدة</em>', 'Estepona, <em>ten westen van de stad</em>', 'Estepona, <em>na zachód od miasta</em>', 'Estepona, <em>vest for byen</em>', 'Estepona, <em>väster om staden</em>')
a('.location.mapLabelPlain',
  'Estepona, al oeste del casco urbano', 'Estepona, à l’ouest de la ville', 'Estepona, westlich der Stadt', 'Эстепона, к западу от города',
  'إستيبونا، غرب البلدة', 'Estepona, ten westen van de stad', 'Estepona, na zachód od miasta', 'Estepona, vest for byen', 'Estepona, väster om staden')
a('.location.copy',
  'El folleto sitúa la promoción en Estepona, a cinco minutos del centro, y su mapa de ubicación marca el solar al oeste del casco urbano, junto a Valle Romano Golf. Los documentos no dan dirección ni coordenadas de la parcela, de modo que el mapa muestra la zona y las distancias de abajo son las del folleto; confirmamos la posición exacta y los tiempos en coche en una visita.',
  'La brochure situe le programme à Estepona, à cinq minutes du centre-ville, et sa carte de localisation place le site à l’ouest de la ville, à côté de Valle Romano Golf. Les documents ne donnent ni adresse ni coordonnées de la parcelle ; la carte montre donc le secteur et les distances ci-dessous sont celles de la brochure ; nous confirmons la position exacte et les temps de trajet lors d’une visite.',
  'Die Broschüre verortet die Anlage in Estepona, fünf Minuten vom Stadtzentrum entfernt, und ihre Lagekarte markiert das Grundstück westlich der Stadt, neben Valle Romano Golf. Die Dokumente nennen weder Adresse noch Koordinaten des Grundstücks, daher zeigt die Karte das Gebiet, und die Entfernungen unten stammen aus der Broschüre; die genaue Lage und die Fahrzeiten bestätigen wir bei einem Besuch.',
  'В брошюре проект расположен в Эстепоне, в пяти минутах от центра города, а на карте расположения участок отмечен к западу от города, рядом с Valle Romano Golf. В документах нет адреса или координат участка, поэтому на карте показан район, а расстояния ниже взяты из брошюры; точное положение и время в пути мы подтверждаем во время визита.',
  'يضع الكتيّب المشروع في إستيبونا، على بعد خمس دقائق من وسط البلدة، وتشير خريطة الموقع فيه إلى الأرض غرب البلدة بجوار Valle Romano Golf. ولا تذكر المستندات عنوان القطعة ولا إحداثياتها، لذلك تعرض الخريطة المنطقة والمسافات أدناه من الكتيّب؛ ونؤكد الموقع الدقيق وأزمنة القيادة خلال زيارة.',
  'De brochure plaatst de ontwikkeling in Estepona, vijf minuten van het centrum, en de locatiekaart markeert het terrein ten westen van de stad, naast Valle Romano Golf. De documenten geven geen adres of coördinaat van het perceel, dus de kaart toont het gebied en de afstanden hieronder zijn die van de brochure; wij bevestigen de exacte positie en de rijtijden tijdens een bezoek.',
  'Broszura umieszcza inwestycję w Esteponie, pięć minut od centrum miasta, a jej mapa lokalizacji zaznacza działkę na zachód od miasta, obok Valle Romano Golf. Dokumenty nie podają adresu ani współrzędnych działki, więc mapa pokazuje okolicę, a odległości poniżej pochodzą z broszury; dokładną lokalizację i czasy przejazdu potwierdzamy podczas wizyty.',
  'Brosjyren plasserer prosjektet i Estepona, fem minutter fra sentrum, og lokaliseringskartet markerer tomten vest for byen, ved siden av Valle Romano Golf. Dokumentene oppgir ingen adresse eller koordinater for tomten, så kartet viser området, og avstandene nedenfor er brosjyrens; vi bekrefter den nøyaktige plasseringen og kjøretidene på en visning.',
  'Broschyren placerar projektet i Estepona, fem minuter från centrum, och dess lägeskarta markerar tomten väster om staden, bredvid Valle Romano Golf. Dokumenten anger ingen adress eller koordinat för tomten, så kartan visar området och avstånden nedan är broschyrens; vi bekräftar den exakta platsen och körtiderna vid ett besök.')
a('.location.distances[0][1]', 'Unos 5 minutos', 'Environ 5 minutes', 'Etwa 5 Minuten', 'Около 5 минут', 'نحو 5 دقائق', 'Ongeveer 5 minuten', 'Około 5 minut', 'Omtrent 5 minutter', 'Cirka 5 minuter')
a('.location.distances[1][1]', 'Unos 15 minutos', 'Environ 15 minutes', 'Etwa 15 Minuten', 'Около 15 минут', 'نحو 15 دقيقة', 'Ongeveer 15 minuten', 'Około 15 minut', 'Omtrent 15 minutter', 'Cirka 15 minuter')
a('.location.distances[2][1]', 'Unos 20 minutos en coche', 'Environ 20 minutes en voiture', 'Etwa 20 Minuten mit dem Auto', 'Около 20 минут на машине', 'نحو 20 دقيقة بالسيارة',
  'Ongeveer 20 minuten met de auto', 'Około 20 minut samochodem', 'Omtrent 20 minutter med bil', 'Cirka 20 minuter med bil')
a('.location.distances[3][1]', 'Menos de 40 minutos', 'Moins de 40 minutes', 'Unter 40 Minuten', 'Менее 40 минут', 'أقل من 40 دقيقة', 'Minder dan 40 minuten', 'Poniżej 40 minut', 'Under 40 minutter', 'Under 40 minuter')
a('.location.distances[4][1]', 'Unos 50 minutos', 'Environ 50 minutes', 'Etwa 50 Minuten', 'Около 50 минут', 'نحو 50 دقيقة', 'Ongeveer 50 minuten', 'Około 50 minut', 'Omtrent 50 minutter', 'Cirka 50 minuter')

# ---- investment, trust dossier ---------------------------------------------------------------------

a('.investment.cards[0][1]',
  '17 de las 19 viviendas de la lista tienen precio: once apartamentos de dos dormitorios de {E473000} a {E572000} y seis apartamentos de tres dormitorios de {E560000} a {E687000}, más {T}. Las otras 2 figuran como reservadas.',
  '17 des 19 logements de la liste ont un prix : onze appartements de deux chambres de {E473000} à {E572000} et six appartements de trois chambres de {E560000} à {E687000}, hors {T}. Les 2 autres sont marqués comme réservés.',
  '17 der 19 Wohnungen auf der Liste haben einen Preis: elf Wohnungen mit zwei Schlafzimmern von {E473000} bis {E572000} und sechs Wohnungen mit drei Schlafzimmern von {E560000} bis {E687000}, zuzüglich {T}. Die übrigen 2 sind als reserviert gekennzeichnet.',
  '17 из 19 квартир списка имеют цену: одиннадцать апартаментов с двумя спальнями от {E473000} до {E572000} и шесть с тремя спальнями от {E560000} до {E687000}, без {T}. Остальные 2 отмечены как забронированные.',
  'لـ17 من المساكن التسعة عشر في القائمة سعر: أحد عشر شقة بغرفتي نوم من {E473000} إلى {E572000} وست شقق بثلاث غرف نوم من {E560000} إلى {E687000}، زائد {T}. أما المسكنان الآخران فمشار إليهما على أنهما محجوزان.',
  '17 van de 19 woningen op de lijst hebben een prijs: elf appartementen met twee slaapkamers van {E473000} tot {E572000} en zes appartementen met drie slaapkamers van {E560000} tot {E687000}, plus {T}. De overige 2 zijn als gereserveerd gemarkeerd.',
  '17 z 19 lokali na liście ma cenę: jedenaście apartamentów z dwiema sypialniami od {E473000} do {E572000} i sześć apartamentów z trzema sypialniami od {E560000} do {E687000}, plus {T}. Pozostałe 2 są oznaczone jako zarezerwowane.',
  '17 av de 19 boligene på listen har en pris: elleve leiligheter med to soverom fra {E473000} til {E572000} og seks leiligheter med tre soverom fra {E560000} til {E687000}, pluss {T}. De øvrige 2 er markert som reservert.',
  '17 av de 19 bostäderna på listan har ett pris: elva lägenheter med två sovrum från {E473000} till {E572000} och sex lägenheter med tre sovrum från {E560000} till {E687000}, plus {T}. De övriga 2 är markerade som reserverade.')
a('.investment.cards[1][1]',
  'La lista dice que el IVA del 10 por ciento no está incluido. Con el IVA al 10 por ciento y el impuesto de actos jurídicos documentados al {N1.20} por ciento, {E473000} pasan a ser unos {E526000} y {E687000} unos {E764000}, antes de los gastos de notaría y registro.',
  'La liste indique que la TVA à 10 pour cent n’est pas comprise. Avec la TVA à 10 pour cent et le droit de timbre à {N1.20} pour cent, {E473000} deviennent environ {E526000} et {E687000} environ {E764000}, avant les frais de notaire et d’enregistrement.',
  'Die Liste gibt an, dass die MwSt. von 10 Prozent nicht enthalten ist. Mit 10 Prozent MwSt. und {N1.20} Prozent Stempelsteuer werden aus {E473000} etwa {E526000} und aus {E687000} etwa {E764000}, vor Notar- und Grundbuchkosten.',
  'В списке сказано, что НДС 10 процентов не включён. При НДС 10 процентов и гербовом сборе {N1.20} процента {E473000} превращаются примерно в {E526000}, а {E687000} — примерно в {E764000}, до расходов на нотариуса и регистрацию.',
  'تذكر القائمة أن ضريبة القيمة المضافة بنسبة 10 بالمئة غير مشمولة. وبضريبة قيمة مضافة قدرها 10 بالمئة ورسم دمغة قدره {N1.20} بالمئة، يصبح مبلغ {E473000} نحو {E526000} ويصبح {E687000} نحو {E764000}، قبل أتعاب التوثيق والتسجيل.',
  'De lijst geeft aan dat 10 procent btw niet is inbegrepen. Met 10 procent btw en {N1.20} procent overdrachtsbelasting wordt {E473000} ongeveer {E526000} en {E687000} ongeveer {E764000}, vóór notaris- en kadasterkosten.',
  'Cennik podaje, że VAT w wysokości 10 procent nie jest wliczony. Przy VAT 10 procent i podatku od czynności cywilnoprawnych {N1.20} procent kwota {E473000} wzrasta do około {E526000}, a {E687000} do około {E764000}, przed opłatami notarialnymi i wpisem do księgi wieczystej.',
  'Listen oppgir at merverdiavgift på 10 prosent ikke er inkludert. Med merverdiavgift på 10 prosent og dokumentavgift på {N1.20} prosent blir {E473000} til rundt {E526000} og {E687000} til rundt {E764000}, før notar- og tinglysingsgebyrer.',
  'Listan anger att IVA (spansk moms) på 10 procent inte ingår. Med IVA på 10 procent och stämpelskatt på {N1.20} procent blir {E473000} omkring {E526000} och {E687000} omkring {E764000}, före notarie- och registreringsavgifter.')
a('.investment.cards[2][0]',
  'La escritura concentra la mayor parte del precio', 'L’acte notarié porte l’essentiel du prix', 'Die Urkunde trägt den größten Teil des Preises',
  'Основная часть цены приходится на нотариальный акт', 'سند الملكية يحمل معظم السعر', 'De akte draagt het grootste deel van de prijs',
  'Akt notarialny obejmuje większość ceny', 'Skjøtet bærer det meste av prisen', 'Lagfarten bär merparten av priset')
a('.investment.cards[2][1]',
  'El 65 % + {T} vence solo en la firma de la escritura, después de la reserva y del 35 % + {T} en el contrato privado. La lista no da fecha para ninguno de los dos y no dice nada de una garantía bancaria para los pagos a cuenta.',
  '65 % + {T} ne sont dus qu’à la signature de l’acte notarié, après la réservation et 35 % + {T} au contrat privé. La liste ne donne de date pour aucun des deux et ne dit rien d’une garantie bancaire pour les versements d’acompte.',
  '65 % + {T} werden erst bei der Unterzeichnung der notariellen Urkunde fällig, nach der Reservierung und den 35 % + {T} beim privaten Vertrag. Die Liste nennt für keinen von beiden ein Datum und sagt nichts über eine Bankgarantie für Anzahlungen.',
  '65 % + {T} подлежат оплате только при подписании нотариального акта — после бронирования и 35 % + {T} при частном договоре. Ни для одного из платежей в списке нет даты, и ничего не сказано о банковской гарантии для авансовых платежей.',
  'لا تُستحق نسبة 65% + {T} إلا عند توقيع سند الملكية، بعد الحجز ونسبة 35% + {T} عند العقد الخاص. ولا تذكر القائمة تاريخًا لأي منهما ولا تقول شيئًا عن ضمان مصرفي للدفعات المقدمة.',
  '65% + {T} is pas verschuldigd bij de ondertekening van de notariële akte, na de reservering en de 35% + {T} bij het privécontract. De lijst geeft voor geen van beide een datum en zegt niets over een bankgarantie voor vooruitbetalingen.',
  '65% + {T} jest płatne dopiero przy podpisaniu aktu notarialnego, po rezerwacji i po 35% + {T} przy umowie prywatnej. Cennik nie podaje terminu żadnej z tych płatności i nic nie mówi o gwarancji bankowej dla wpłat na poczet ceny.',
  '65 % + {T} forfaller først ved signeringen av skjøtet, etter reservasjonen og de 35 % + {T} ved den private kontrakten. Listen oppgir ingen dato for noen av dem og sier ingenting om en bankgaranti for forskuddsbetalinger.',
  '65 % + {T} förfaller först vid undertecknandet av lagfarten, efter bokningen och de 35 % + {T} vid det privata avtalet. Listan anger inget datum för någon av dem och säger ingenting om en bankgaranti för förskottsbetalningar.')
a('.investment.cards[3][1]',
  'La lista dice que la disponibilidad y los precios pueden cambiar sin previo aviso. Reconfirmamos la cifra con el vendedor antes de que usted reserve, y puede ser distinta para entonces.',
  'La liste indique que la disponibilité et les prix peuvent changer sans préavis. Nous reconfirmons le chiffre auprès du vendeur avant que vous ne réserviez, et il peut être différent d’ici là.',
  'Die Liste gibt an, dass Verfügbarkeit und Preise ohne Vorankündigung geändert werden können. Wir bestätigen den Betrag vor Ihrer Reservierung erneut beim Verkäufer, und er kann bis dahin ein anderer sein.',
  'В списке сказано, что наличие и цены могут измениться без предварительного уведомления. Мы заново подтверждаем сумму у продавца до того, как вы забронируете, и к тому времени она может быть другой.',
  'تذكر القائمة أن التوفر والأسعار قابلان للتغيير دون إشعار مسبق. نعيد تأكيد المبلغ مع البائع قبل أن تحجز، وقد يختلف عندئذٍ.',
  'De lijst zegt dat beschikbaarheid en prijzen zonder voorafgaande kennisgeving kunnen veranderen. Wij bevestigen het bedrag opnieuw bij de verkoper voordat u reserveert, en het kan dan anders zijn.',
  'Cennik podaje, że dostępność i ceny mogą ulec zmianie bez uprzedzenia. Kwotę potwierdzamy ponownie ze sprzedawcą przed rezerwacją i do tego czasu może się ona zmienić.',
  'Listen sier at tilgjengelighet og priser kan endres uten forvarsel. Vi bekrefter beløpet på nytt med selgeren før De reserverer, og det kan være annerledes da.',
  'Listan anger att tillgänglighet och priser kan ändras utan förvarning. Vi bekräftar beloppet på nytt med säljaren innan ni bokar, och det kan vara ett annat då.')
a('.trustDossier.cards[0][1]',
  'Ninguno de los documentos da una licencia de obras, un inicio de obras, una fase de construcción ni una fecha de entrega, y el folleto dice que se basa en el proyecto preliminar. Pedimos por escrito la licencia, el programa de obras y la fecha de entrega contractual.',
  'Aucun des documents ne donne de permis de construire, de début des travaux, d’état d’avancement du chantier ni de date de livraison, et la brochure indique qu’elle repose sur le projet préliminaire. Nous demandons par écrit le permis, le calendrier des travaux et la date de livraison contractuelle.',
  'Keines der Dokumente nennt eine Baugenehmigung, einen Baubeginn, einen Baustand oder einen Fertigstellungstermin, und die Broschüre gibt an, dass sie auf dem Vorprojekt beruht. Wir fordern die Genehmigung, den Bauzeitenplan und den vertraglichen Fertigstellungstermin schriftlich an.',
  'Ни в одном из документов нет строительной лицензии, начала работ, стадии строительства или срока сдачи, а в брошюре сказано, что она основана на предварительном проекте. Мы письменно запрашиваем лицензию, график работ и договорной срок сдачи.',
  'لا يذكر أي من المستندات رخصة بناء ولا بدء أعمال ولا مرحلة بناء ولا موعد إنجاز، ويذكر الكتيّب أنه مبني على المشروع الأولي. نطلب كتابةً الرخصة وبرنامج الأعمال وموعد الإنجاز التعاقدي.',
  'Geen van de documenten vermeldt een bouwvergunning, een start van de werken, een bouwfase of een opleverdatum, en de brochure zegt dat zij op het voorontwerp is gebaseerd. Wij vragen de vergunning, het bouwprogramma en de contractuele opleverdatum schriftelijk op.',
  'Żaden z dokumentów nie podaje pozwolenia na budowę, rozpoczęcia robót, etapu budowy ani terminu ukończenia, a broszura zastrzega, że opiera się na projekcie wstępnym. Prosimy na piśmie o pozwolenie, harmonogram robót i umowny termin ukończenia.',
  'Ingen av dokumentene oppgir en byggetillatelse, en byggestart, et byggetrinn eller en ferdigstillelsesdato, og brosjyren sier at den bygger på det foreløpige prosjektet. Vi ber skriftlig om tillatelsen, fremdriftsplanen og den kontraktsfestede ferdigstillelsesdatoen.',
  'Inget av dokumenten anger ett bygglov, en byggstart, ett byggskede eller ett färdigställandedatum, och broschyren anger att den bygger på det preliminära projektet. Vi begär skriftligen bygglovet, byggplanen och det avtalade färdigställandedatumet.')
a('.trustDossier.cards[1][1]',
  'Tenemos planos de 5 de las 17 viviendas: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A y 04-03-01-B. Sus superficies interiores, terrazas y superficies construidas coinciden exactamente con la lista de precios. Las otras 12 viviendas no tienen plano, y los pedimos.',
  'Nous disposons des plans de 5 des 17 logements : 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A et 04-03-01-B. Leurs surfaces intérieures, terrasses et surfaces construites correspondent exactement à la liste de prix. Les 12 autres logements n’ont pas de plan, et nous les demandons.',
  'Wir haben Grundrisse für 5 der 17 Wohnungen: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A und 04-03-01-B. Ihre Innenflächen, Terrassen und bebauten Flächen stimmen genau mit der Preisliste überein. Für die anderen 12 Wohnungen gibt es keinen Plan, und wir fordern sie an.',
  'У нас есть планировки 5 из 17 квартир: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A и 04-03-01-B. Их внутренние площади, террасы и застроенные площади в точности совпадают с прайс-листом. У остальных 12 квартир планировок нет, и мы их запрашиваем.',
  'لدينا مخططات 5 من المساكن السبعة عشر: 01-03-00-C، 04-01-00-B، 04-01-02-A، 04-03-00-A و04-03-01-B. وتطابق مساحاتها الداخلية وتراساتها ومساحاتها المبنية قائمة الأسعار تمامًا. أما المساكن الاثنا عشر الأخرى فلا مخطط لها، ونطلبها.',
  'Wij hebben plattegronden van 5 van de 17 woningen: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A en 04-03-01-B. Hun binnenoppervlaktes, terrassen en bebouwde oppervlaktes komen exact overeen met de prijslijst. De andere 12 woningen hebben geen plattegrond, en wij vragen ernaar.',
  'Mamy rzuty 5 z 17 lokali: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A i 04-03-01-B. Ich powierzchnie wewnętrzne, tarasy i powierzchnie zabudowy dokładnie zgadzają się z cennikiem. Pozostałe 12 lokali nie ma rzutu i o nie prosimy.',
  'Vi har tegninger for 5 av de 17 boligene: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A og 04-03-01-B. Deres innvendige arealer, terrasser og bruksarealer stemmer nøyaktig med prislisten. De øvrige 12 boligene har ingen tegning, og vi ber om dem.',
  'Vi har ritningar för 5 av de 17 bostäderna: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A och 04-03-01-B. Deras invändiga ytor, terrasser och byggytor stämmer exakt med prislistan. De övriga 12 bostäderna har ingen ritning, och vi begär dem.')
a('.trustDossier.cards[2][1]',
  'El folleto cuenta dos piscinas; el informe de calidades enumera piscinas exteriores en plural y una piscina climatizada en el spa. Preguntamos cuántas piscinas hay y cuáles son exteriores.',
  'La brochure compte deux piscines ; le rapport de qualité liste des piscines extérieures au pluriel et une piscine chauffée dans le spa. Nous demandons combien il y a de piscines et lesquelles sont extérieures.',
  'Die Broschüre zählt zwei Schwimmbäder; der Qualitätsbericht führt Außenpools im Plural und einen beheizten Pool im Spa auf. Wir fragen nach, wie viele Pools es gibt und welche im Freien liegen.',
  'В брошюре указаны два бассейна; в отчёте о качестве — наружные бассейны во множественном числе и подогреваемый бассейн в спа. Мы выясняем, сколько всего бассейнов и какие из них на открытом воздухе.',
  'يذكر الكتيّب مسبحين؛ ويسرد تقرير الجودة مسابح خارجية بصيغة الجمع ومسبحًا مدفأ في السبا. نسأل عن عدد المسابح وأيها خارجي.',
  'De brochure telt twee zwembaden; het kwaliteitsrapport noemt buitenzwembaden in het meervoud en een verwarmd zwembad in de spa. Wij vragen hoeveel zwembaden er zijn en welke buiten liggen.',
  'Broszura wymienia dwa baseny; raport jakości podaje baseny zewnętrzne w liczbie mnogiej oraz podgrzewany basen w spa. Pytamy, ile jest basenów i które z nich są na zewnątrz.',
  'Brosjyren oppgir to svømmebasseng; kvalitetsrapporten oppgir utendørs basseng i flertall og et oppvarmet basseng i spaet. Vi spør hvor mange basseng det er og hvilke som er utendørs.',
  'Broschyren anger två simbassänger; kvalitetsrapporten anger utomhuspooler i plural och en uppvärmd pool i spat. Vi frågar hur många pooler det finns och vilka som ligger utomhus.')
a('.trustDossier.cards[3][0]',
  'Golf y distancias', 'Golf et distances', 'Golf und Entfernungen', 'Гольф и расстояния', 'الغولف والمسافات', 'Golf en afstanden', 'Golf i odległości', 'Golf og avstander', 'Golf och avstånd')
a('.trustDossier.cards[3][1]',
  'El folleto sitúa el solar a pocos minutos en coche de cuatro campos de golf, mientras que su propio mapa dibuja dos de ellos al otro lado del casco urbano de Estepona. Medimos nosotros mismos los tiempos en coche.',
  'La brochure situe le site à quelques minutes en voiture de quatre terrains de golf, alors que sa propre carte en dessine deux de l’autre côté de la ville d’Estepona. Nous mesurons nous-mêmes les temps de trajet.',
  'Die Broschüre verortet das Grundstück wenige Autominuten von vier Golfplätzen entfernt, während ihre eigene Karte zwei davon auf der anderen Seite der Stadt Estepona einzeichnet. Wir messen die Fahrzeiten selbst.',
  'В брошюре участок находится в нескольких минутах езды от четырёх полей для гольфа, тогда как на её собственной карте два из них нарисованы по другую сторону города Эстепона. Время в пути мы измеряем сами.',
  'يضع الكتيّب الموقع على بعد دقائق قليلة بالسيارة من أربعة ملاعب غولف، بينما ترسم خريطته نفسها اثنين منها على الجانب الآخر من بلدة إستيبونا. ونقيس أزمنة القيادة بأنفسنا.',
  'De brochure plaatst het terrein op enkele minuten rijden van vier golfbanen, terwijl de eigen kaart er twee aan de andere kant van de stad Estepona tekent. Wij meten de rijtijden zelf.',
  'Broszura umieszcza działkę kilka minut jazdy od czterech pól golfowych, podczas gdy jej własna mapa rysuje dwa z nich po drugiej stronie miasta Estepona. Czasy przejazdu mierzymy sami.',
  'Brosjyren plasserer tomten noen få minutter med bil fra fire golfbaner, mens brosjyrens eget kart tegner to av dem på den andre siden av Estepona by. Vi måler kjøretidene selv.',
  'Broschyren placerar tomten några minuters bilresa från fyra golfbanor, medan dess egen karta ritar in två av dem på andra sidan av staden Estepona. Vi mäter körtiderna själva.')
a('.trustDossier.cards[4][1]',
  'La lista de precios está fechada en noviembre de 2026, sin día, y los planos llevan la fecha del 16 de octubre de 2026. El folleto, el informe de calidades y los planos dicen todos que son preliminares y no contractuales. Usamos la lista para los precios y la disponibilidad y los demás documentos para describir las viviendas.',
  'La liste de prix est datée de novembre 2026, sans jour, et les plans portent la date du 16 octobre 2026. La brochure, le rapport de qualité et les plans indiquent tous qu’ils sont préliminaires et non contractuels. Nous utilisons la liste pour les prix et la disponibilité et les autres documents pour décrire les logements.',
  'Die Preisliste ist auf November 2026 datiert, ohne Tag, und die Pläne tragen das Datum 16. Oktober 2026. Die Broschüre, der Qualitätsbericht und die Pläne geben alle an, dass sie vorläufig und nicht vertraglich bindend sind. Wir verwenden die Liste für Preise und Verfügbarkeit und die übrigen Dokumente zur Beschreibung der Wohnungen.',
  'Прайс-лист датирован ноябрём 2026 года, без указания дня, а на планировках стоит дата 16 октября 2026 года. В брошюре, отчёте о качестве и планировках сказано, что они предварительные и не носят договорного характера. Прайс-лист мы используем для цен и наличия, а остальные документы — для описания квартир.',
  'قائمة الأسعار مؤرخة بنوفمبر 2026 دون يوم، وتحمل المخططات تاريخ 16 أكتوبر 2026. ويذكر الكتيّب وتقرير الجودة والمخططات جميعًا أنها أولية وغير ملزمة تعاقديًا. ونستخدم القائمة للأسعار والتوفر والمستندات الأخرى لوصف المساكن.',
  'De prijslijst is gedateerd op november 2026, zonder dag, en de plannen dragen de datum 16 oktober 2026. De brochure, het kwaliteitsrapport en de plannen zeggen allemaal dat ze voorlopig en niet contractueel zijn. Wij gebruiken de lijst voor prijzen en beschikbaarheid en de andere documenten om de woningen te beschrijven.',
  'Cennik jest datowany na listopad 2026 roku, bez dnia, a rzuty noszą datę 16 października 2026 roku. Broszura, raport jakości i rzuty podają, że mają charakter wstępny i nie są umowne. Cennik wykorzystujemy do cen i dostępności, a pozostałe dokumenty do opisu lokali.',
  'Prislisten er datert november 2026, uten dag, og tegningene har datoen 16. oktober 2026. Brosjyren, kvalitetsrapporten og tegningene sier alle at de er foreløpige og ikke kontraktsfestet. Vi bruker listen til priser og tilgjengelighet og de andre dokumentene til å beskrive boligene.',
  'Prislistan är daterad november 2026, utan dag, och ritningarna har datumet 16 oktober 2026. Broschyren, kvalitetsrapporten och ritningarna anger alla att de är preliminära och inte avtalsbindande. Vi använder listan för priser och tillgänglighet och de andra dokumenten för att beskriva bostäderna.')

# ---- availability ----------------------------------------------------------------------------------

a('.availability.copy',
  'La lista de precios del promotor de noviembre de 2026 nombra 19 viviendas. Diecisiete tienen precio y están disponibles, once con dos dormitorios y seis con tres; las otras 2 figuran como reservadas. La lista dice que la disponibilidad y los precios pueden cambiar sin previo aviso, de modo que Nueva Living confirma precio y disponibilidad antes de cualquier visita o reserva.',
  'La liste de prix du promoteur de novembre 2026 nomme 19 logements. Dix-sept ont un prix et sont disponibles, onze de deux chambres et six de trois ; les 2 autres sont marqués comme réservés. La liste indique que la disponibilité et les prix peuvent changer sans préavis ; Nueva Living confirme donc le prix et la disponibilité avant toute visite ou réservation.',
  'Die Preisliste des Bauträgers vom November 2026 nennt 19 Wohnungen. Siebzehn haben einen Preis und sind verfügbar, elf mit zwei und sechs mit drei Schlafzimmern; die übrigen 2 sind als reserviert gekennzeichnet. Die Liste gibt an, dass Verfügbarkeit und Preise ohne Vorankündigung geändert werden können, daher bestätigt Nueva Living Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung.',
  'В прайс-листе застройщика за ноябрь 2026 года названы 19 квартир. Семнадцать имеют цену и доступны, одиннадцать с двумя спальнями и шесть с тремя; остальные 2 отмечены как забронированные. В списке сказано, что наличие и цены могут измениться без предварительного уведомления, поэтому Nueva Living подтверждает цену и наличие до любого просмотра или бронирования.',
  'تذكر قائمة أسعار المطوّر لشهر نوفمبر 2026 تسعة عشر مسكنًا. سبعة عشر منها لها سعر ومتاحة، أحد عشر بغرفتي نوم وستة بثلاث غرف نوم؛ أما المسكنان الآخران فمشار إليهما على أنهما محجوزان. وتذكر القائمة أن التوفر والأسعار قابلان للتغيير دون إشعار مسبق، لذلك تؤكد Nueva Living السعر والتوفر قبل أي معاينة أو حجز.',
  'De prijslijst van de ontwikkelaar van november 2026 noemt 19 woningen. Zeventien hebben een prijs en zijn beschikbaar, elf met twee en zes met drie slaapkamers; de overige 2 zijn als gereserveerd gemarkeerd. De lijst zegt dat beschikbaarheid en prijzen zonder voorafgaande kennisgeving kunnen veranderen, dus Nueva Living bevestigt prijs en beschikbaarheid vóór elke bezichtiging of reservering.',
  'Cennik dewelopera z listopada 2026 roku wymienia 19 lokali. Siedemnaście ma cenę i jest dostępnych, jedenaście z dwiema sypialniami i sześć z trzema; pozostałe 2 są oznaczone jako zarezerwowane. Cennik podaje, że dostępność i ceny mogą ulec zmianie bez uprzedzenia, dlatego Nueva Living potwierdza cenę i dostępność przed każdym oglądaniem lub rezerwacją.',
  'Utbyggerens prisliste fra november 2026 nevner 19 boliger. Sytten har en pris og er ledige, elleve med to soverom og seks med tre; de øvrige 2 er markert som reservert. Listen sier at tilgjengelighet og priser kan endres uten forvarsel, så Nueva Living bekrefter pris og tilgjengelighet før enhver visning eller reservasjon.',
  'Exploatörens prislista från november 2026 nämner 19 bostäder. Sjutton har ett pris och är lediga, elva med två sovrum och sex med tre; de övriga 2 är markerade som reserverade. Listan anger att tillgänglighet och priser kan ändras utan förvarning, så Nueva Living bekräftar pris och tillgänglighet före varje visning eller bokning.')
a('.availability.priceRange',
  '{E473000} - {E687000} + {T}', '{E473000} - {E687000} + {T}', '{E473000} - {E687000} + {T}', '{E473000} - {E687000} + {T}', '{E473000} - {E687000} + {T}',
  '{E473000} - {E687000} + {T}', '{E473000} - {E687000} + {T}', '{E473000} - {E687000} + mva.', '{E473000} - {E687000} + {T}')
a('.availability.sourceNote',
  'Los precios, dormitorios y superficies están transcritos de la lista de precios del promotor de noviembre de 2026, que no lleva día. Tiene 19 filas en cuatro bloques: 17 con precio y 2 marcadas como reservadas (01-03-01-B y 03-01-01-B), que no se muestran. La lista dice que los precios excluyen el IVA del 10 %, que cada vivienda se vende con la plaza o plazas de garaje y el trastero indicados frente a ella, en los niveles S-1 y S-2, y que sus superficies interior y de terraza son metros cuadrados útiles. Su superficie construida, que incluye una parte proporcional de las zonas comunes, no se muestra aquí. Los cinco planos que tenemos, fechados el 16 de octubre de 2026 en sus hojas, coinciden con la lista en superficie interior, terrazas y superficie construida; las otras 12 viviendas no tienen plano. Con el IVA al 10 % y el impuesto de actos jurídicos documentados al {N1.20} %, la vivienda de {E473000} cuesta unos {E526000} y la de {E687000} unos {E764000}, antes de los gastos de notaría y registro.',
  'Les prix, les chambres et les surfaces sont repris de la liste de prix du promoteur de novembre 2026, qui ne porte aucun jour. Elle compte 19 lignes réparties en quatre blocs : 17 avec un prix et 2 marquées comme réservées (01-03-01-B et 03-01-01-B), qui ne sont pas affichées. La liste indique que les prix excluent la TVA de 10 %, que chaque logement est vendu avec la ou les places de parking et la cave indiquées en regard, aux niveaux S-1 et S-2, et que ses surfaces intérieure et de terrasse sont des mètres carrés utiles. Sa surface construite, qui inclut une quote-part des parties communes, n’est pas affichée ici. Les cinq plans que nous détenons, datés du 16 octobre 2026 sur leurs feuilles, concordent avec la liste pour la surface intérieure, les terrasses et la surface construite ; les 12 autres logements n’ont pas de plan. Avec la TVA à 10 % et le droit de timbre à {N1.20} %, le logement à {E473000} coûte environ {E526000} et celui à {E687000} environ {E764000}, avant les frais de notaire et d’enregistrement.',
  'Preise, Schlafzimmer und Flächen sind der Preisliste des Bauträgers vom November 2026 entnommen, die keinen Tag trägt. Sie hat 19 Zeilen in vier Blöcken: 17 mit Preis und 2 als reserviert gekennzeichnet (01-03-01-B und 03-01-01-B), die nicht angezeigt werden. Die Liste gibt an, dass die Preise 10 % MwSt. nicht enthalten, dass jede Wohnung mit dem daneben genannten Stellplatz oder den Stellplätzen und dem Abstellraum verkauft wird, auf den Ebenen S-1 und S-2, und dass ihre Innen- und Terrassenflächen Nutzflächen in Quadratmetern sind. Ihre bebaute Fläche, die einen anteiligen Teil der Gemeinschaftsflächen enthält, wird hier nicht angezeigt. Die fünf Pläne, die uns vorliegen und deren Blätter das Datum 16. Oktober 2026 tragen, stimmen mit der Liste in Innenfläche, Terrassen und bebauter Fläche überein; die anderen 12 Wohnungen haben keinen Plan. Mit 10 % MwSt. und {N1.20} % Stempelsteuer kostet die Wohnung zu {E473000} etwa {E526000} und die zu {E687000} etwa {E764000}, vor Notar- und Grundbuchkosten.',
  'Цены, спальни и площади перенесены из прайс-листа застройщика за ноябрь 2026 года, на котором не указан день. В нём 19 строк в четырёх блоках: 17 с ценой и 2, отмеченные как забронированные (01-03-01-B и 03-01-01-B), которые здесь не показаны. В списке сказано, что цены не включают НДС 10 %, что каждая квартира продаётся с указанным напротив машиноместом или машиноместами и кладовой на уровнях S-1 и S-2, а её внутренняя площадь и площадь террас — полезные квадратные метры. Застроенная площадь, включающая пропорциональную долю общих зон, здесь не показана. Пять имеющихся у нас планировок с датой 16 октября 2026 года на листах совпадают со списком по внутренней площади, террасам и застроенной площади; у остальных 12 квартир планировок нет. При НДС 10 % и гербовом сборе {N1.20} % квартира за {E473000} обойдётся примерно в {E526000}, а за {E687000} — примерно в {E764000}, до расходов на нотариуса и регистрацию.',
  'الأسعار وعدد غرف النوم والمساحات منقولة من قائمة أسعار المطوّر لشهر نوفمبر 2026، التي لا تحمل يومًا. وفيها 19 صفًا في أربعة مبانٍ: 17 بسعر واثنان مشار إليهما على أنهما محجوزان (01-03-01-B و03-01-01-B) ولا يظهران هنا. وتذكر القائمة أن الأسعار لا تشمل ضريبة القيمة المضافة بنسبة 10%، وأن كل مسكن يُباع مع موقف السيارات أو مواقفها والمخزن المذكورين أمامه، في المستويين S-1 وS-2، وأن مساحتيه الداخلية والتراس مساحتان صالحتان للاستخدام بالمتر المربع. أما مساحته المبنية، التي تشمل حصة تناسبية من المرافق المشتركة، فلا تظهر هنا. وتتطابق المخططات الخمسة التي لدينا، وعلى أوراقها تاريخ 16 أكتوبر 2026، مع القائمة في المساحة الداخلية والتراسات والمساحة المبنية؛ أما المساكن الاثنا عشر الأخرى فلا مخطط لها. وبضريبة قيمة مضافة بنسبة 10% ورسم دمغة بنسبة {N1.20}%، تبلغ كلفة المسكن البالغ {E473000} نحو {E526000} والمسكن البالغ {E687000} نحو {E764000}، قبل أتعاب التوثيق والتسجيل.',
  'Prijzen, slaapkamers en oppervlaktes zijn overgenomen uit de prijslijst van de ontwikkelaar van november 2026, die geen dag vermeldt. Ze heeft 19 rijen in vier blokken: 17 met een prijs en 2 gemarkeerd als gereserveerd (01-03-01-B en 03-01-01-B), die niet worden getoond. De lijst zegt dat de prijzen exclusief 10% btw zijn, dat elke woning wordt verkocht met de ernaast genoemde parkeerplaats of parkeerplaatsen en berging, op de niveaus S-1 en S-2, en dat de binnen- en terrasoppervlaktes bruikbare vierkante meters zijn. De bebouwde oppervlakte, die een evenredig aandeel in de gemeenschappelijke ruimtes omvat, wordt hier niet getoond. De vijf plattegronden die wij hebben, met op hun bladen de datum 16 oktober 2026, komen met de lijst overeen qua binnenoppervlak, terrassen en bebouwde oppervlakte; de andere 12 woningen hebben geen plattegrond. Met 10% btw en {N1.20}% overdrachtsbelasting kost de woning van {E473000} ongeveer {E526000} en die van {E687000} ongeveer {E764000}, vóór notaris- en kadasterkosten.',
  'Ceny, sypialnie i powierzchnie przepisano z cennika dewelopera z listopada 2026 roku, który nie podaje dnia. Ma 19 wierszy w czterech blokach: 17 z ceną i 2 oznaczone jako zarezerwowane (01-03-01-B i 03-01-01-B), których tu nie pokazujemy. Cennik podaje, że ceny nie zawierają 10% VAT, że każdy lokal jest sprzedawany ze wskazanym obok miejscem lub miejscami postojowymi i komórką lokatorską, na poziomach S-1 i S-2, oraz że powierzchnie wewnętrzna i tarasów to metry kwadratowe użytkowe. Powierzchnia zabudowy, która obejmuje proporcjonalny udział w częściach wspólnych, nie jest tu pokazana. Pięć rzutów, którymi dysponujemy, z datą 16 października 2026 roku na arkuszach, zgadza się z cennikiem co do powierzchni wewnętrznej, tarasów i powierzchni zabudowy; pozostałe 12 lokali nie ma rzutu. Przy VAT 10% i podatku od czynności cywilnoprawnych {N1.20}% lokal za {E473000} kosztuje około {E526000}, a lokal za {E687000} około {E764000}, przed opłatami notarialnymi i wpisem do księgi wieczystej.',
  'Priser, soverom og arealer er hentet fra utbyggerens prisliste fra november 2026, som ikke har noen dag. Den har 19 rader i fire hus: 17 med pris og 2 markert som reservert (01-03-01-B og 03-01-01-B), som ikke vises. Listen sier at prisene ikke inkluderer 10 % mva, at hver bolig selges med parkeringsplassen eller -plassene og bodet som er oppgitt ved siden av, på nivåene S-1 og S-2, og at innvendig areal og terrasseareal er brukbare kvadratmeter. Bruksarealet, som inkluderer en forholdsmessig andel av fellesarealene, vises ikke her. De fem tegningene vi har, med datoen 16. oktober 2026 på arkene, stemmer med listen på innvendig areal, terrasser og bruksareal; de øvrige 12 boligene har ingen tegning. Med 10 % mva og dokumentavgift på {N1.20} % koster boligen til {E473000} rundt {E526000} og boligen til {E687000} rundt {E764000}, før notar- og tinglysingsgebyrer.',
  'Priser, sovrum och ytor är hämtade från exploatörens prislista från november 2026, som inte har någon dag. Den har 19 rader i fyra hus: 17 med pris och 2 markerade som reserverade (01-03-01-B och 03-01-01-B), som inte visas. Listan anger att priserna är exklusive 10 % IVA (spansk moms), att varje bostad säljs med den parkeringsplats eller de parkeringsplatser och det förråd som anges bredvid, på planen S-1 och S-2, och att dess invändiga yta och terrassyta är användbara kvadratmeter. Byggytan, som inkluderar en proportionell andel av de gemensamma ytorna, visas inte här. De fem ritningarna vi har, med datumet 16 oktober 2026 på arken, stämmer med listan i fråga om invändig yta, terrasser och byggyta; de övriga 12 bostäderna har ingen ritning. Med IVA på 10 % och stämpelskatt på {N1.20} % kostar bostaden för {E473000} omkring {E526000} och bostaden för {E687000} omkring {E764000}, före notarie- och registreringsavgifter.')

# unit sizes: every size line is built from the same parts (interior, terrace, garden)
PARTS = {
    'es': {'interior': '{v} {U} interiores', 'terrace': '{v} {U} de terraza', 'garden': '{v} {U} de jardín'},
    'fr': {'interior': '{v} {U} intérieurs', 'terrace': '{v} {U} de terrasse', 'garden': '{v} {U} de jardin'},
    'de': {'interior': '{v} {U} Innenfläche', 'terrace': '{v} {U} Terrasse', 'garden': '{v} {U} Garten'},
    'ru': {'interior': '{v} {U} внутри', 'terrace': 'терраса {v} {U}', 'garden': 'сад {v} {U}'},
    'ar': {'interior': '{v} {U} داخلية', 'terrace': '{v} {U} تراس', 'garden': '{v} {U} حديقة'},
    'nl': {'interior': '{v} {U} binnen', 'terrace': '{v} {U} terras', 'garden': '{v} {U} tuin'},
    'pl': {'interior': '{v} {U} wnętrza', 'terrace': '{v} {U} tarasu', 'garden': '{v} {U} ogrodu'},
    'no': {'interior': '{v} {U} innvendig', 'terrace': '{v} {U} terrasse', 'garden': '{v} {U} hage'},
    'sv': {'interior': '{v} {U} inomhus', 'terrace': '{v} {U} terrass', 'garden': '{v} {U} trädgård'},
}
n_size = 0
for u in proj['availability']['units']:
    vals = []
    for p in [p.strip() for p in u['size'].split(', ')]:
        m = re.fullmatch(r'([\d.]+) sqm (interior|terrace|garden)', p)
        assert m, (u['reference'], p)
        vals.append((m.group(2), m.group(1)))
    out = {}
    for l in LOCS:
        sep = '، ' if l == 'ar' else ', '
        out[l] = sep.join(PARTS[l][k].replace('{v}', num(v, l)).replace('{U}', UNIT[l]) for k, v in vals)
    assert u['size'] not in T or T[u['size']] == out
    T[u['size']] = out
    n_size += 1
print('sizes', n_size)

# ---- payment terms -----------------------------------------------------------------------------------

a('.constructionTimeline.points[2].year',
  'Escritura', 'Acte notarié', 'Notarielle Urkunde', 'Нотариальный акт', 'سند الملكية', 'Notariële akte', 'Akt notarialny', 'Skjøte', 'Lagfart')
a('.constructionTimeline.note',
  'El promotor no da fecha para la licencia, el inicio de las obras ni la entrega, y las condiciones de pago tampoco nombran fechas. Nueva Living pide las fechas por escrito y las incluye en el contrato.',
  'Le promoteur ne donne aucune date pour le permis, le début des travaux ni la livraison, et les conditions de paiement n’en mentionnent pas non plus. Nueva Living demande les dates par écrit et les fait figurer au contrat.',
  'Der Bauträger nennt kein Datum für die Genehmigung, den Baubeginn oder die Übergabe, und auch die Zahlungsbedingungen nennen keine Daten. Nueva Living fragt die Termine schriftlich an und lässt sie in den Vertrag aufnehmen.',
  'Застройщик не указывает дат ни для лицензии, ни для начала работ, ни для сдачи, и в условиях оплаты дат тоже нет. Nueva Living запрашивает даты в письменной форме и вносит их в договор.',
  'لا يذكر المطوّر تاريخًا للرخصة أو لبدء الأعمال أو للتسليم، ولا تذكر شروط الدفع تواريخ كذلك. تطلب Nueva Living التواريخ كتابةً وتدرجها في العقد.',
  'De ontwikkelaar geeft geen datum voor de vergunning, de start van de werken of de oplevering, en ook de betalingsvoorwaarden noemen geen data. Nueva Living vraagt de data schriftelijk op en laat ze in het contract opnemen.',
  'Deweloper nie podaje terminu pozwolenia, rozpoczęcia robót ani odbioru, a warunki płatności również nie wskazują żadnych terminów. Nueva Living prosi o terminy na piśmie i umieszcza je w umowie.',
  'Utbyggeren oppgir ingen dato for tillatelsen, byggestarten eller overleveringen, og betalingsvilkårene nevner heller ingen datoer. Nueva Living ber skriftlig om datoene og tar dem inn i kontrakten.',
  'Exploatören anger inget datum för bygglovet, byggstarten eller tillträdet, och betalningsvillkoren nämner inte heller några datum. Nueva Living begär datumen skriftligen och för in dem i avtalet.')
a('.constructionTimeline.paymentTerms[0][2]',
  '{E11000} con {T}', '{E11000} TVA comprise', '{E11000} inkl. {T}', '{E11000} с {T}', '{E11000} شاملة {T}', '{E11000} incl. {T}', '{E11000} z {T}', '{E11000} inkl. mva.', '{E11000} inkl. {T}')
a('.constructionTimeline.paymentTerms[1][2]',
  'La lista no da fecha y no dice si se descuenta la reserva', 'La liste ne donne pas de date et ne dit pas si la réservation est déduite',
  'Die Liste nennt kein Datum und sagt nicht, ob die Reservierung abgezogen wird', 'В списке нет даты и не сказано, вычитается ли бронирование',
  'لا تذكر القائمة تاريخًا ولا تقول إن كان الحجز يُخصم', 'De lijst geeft geen datum en zegt niet of de reservering wordt afgetrokken',
  'Cennik nie podaje terminu i nie mówi, czy rezerwacja jest odliczana', 'Listen oppgir ingen dato og sier ikke om reservasjonen trekkes fra',
  'Listan anger inget datum och säger inte om bokningen dras av')
a('.constructionTimeline.paymentTerms[2][0]',
  'En la escritura', 'À l’acte notarié', 'Bei der notariellen Urkunde', 'При нотариальном акте', 'عند سند الملكية', 'Bij de notariële akte', 'Przy akcie notarialnym', 'Ved skjøtet', 'Vid lagfarten')
a('.constructionTimeline.paymentTerms[2][2]',
  'Firma de la escritura', 'Signature de l’acte notarié', 'Unterzeichnung der notariellen Urkunde', 'Подписание нотариального акта', 'توقيع سند الملكية',
  'Ondertekening van de notariële akte', 'Podpisanie aktu notarialnego', 'Signering av skjøtet', 'Undertecknande av lagfarten')
a('.constructionTimeline.paymentTermsNote',
  'Los dos porcentajes suman el precio completo, y el {T} se añade a cada uno. La lista no da fechas, no dice si la reserva de {E10000} se descuenta del 35 % y no dice nada de una garantía bancaria para los pagos a cuenta, de modo que Nueva Living pide cada punto por escrito antes de cualquier reserva.',
  'Les deux pourcentages font le prix complet, et la {T} s’ajoute à chacun. La liste ne donne pas de dates, ne dit pas si la réservation de {E10000} est déduite des 35 % et ne dit rien d’une garantie bancaire pour les versements d’acompte ; Nueva Living demande donc chaque point par écrit avant toute réservation.',
  'Die beiden Prozentsätze ergeben zusammen den gesamten Preis, und die {T} kommt auf jeden hinzu. Die Liste nennt keine Daten, sagt nicht, ob die Reservierung von {E10000} von den 35 % abgezogen wird, und sagt nichts über eine Bankgarantie für Anzahlungen, daher fragt Nueva Living jeden Punkt vor jeder Reservierung schriftlich nach.',
  'Оба процента в сумме дают полную цену, а {T} добавляется к каждому. В списке нет дат, не сказано, вычитается ли бронирование в {E10000} из 35 %, и ничего не сказано о банковской гарантии для авансовых платежей, поэтому Nueva Living до любого бронирования запрашивает каждый пункт в письменной форме.',
  'تُشكّل النسبتان معًا السعر الكامل، وتُضاف {T} إلى كل منهما. ولا تذكر القائمة تواريخ، ولا تقول إن كان الحجز البالغ {E10000} يُخصم من نسبة 35%، ولا تقول شيئًا عن ضمان مصرفي للدفعات المقدمة، لذلك تطلب Nueva Living كل بند كتابةً قبل أي حجز.',
  'De twee percentages vormen samen de volledige prijs, en de {T} komt bij elk daarvan. De lijst geeft geen data, zegt niet of de reservering van {E10000} van de 35% wordt afgetrokken en zegt niets over een bankgarantie voor vooruitbetalingen, dus Nueva Living vraagt elk punt vóór elke reservering schriftelijk op.',
  'Oba wskaźniki procentowe razem dają pełną cenę, a do każdego dolicza się {T}. Cennik nie podaje terminów, nie mówi, czy rezerwacja w wysokości {E10000} jest odliczana od 35%, i nic nie mówi o gwarancji bankowej dla wpłat na poczet ceny, dlatego Nueva Living prosi o każdy punkt na piśmie przed każdą rezerwacją.',
  'De to prosentene utgjør hele prisen, og {T} legges til hver av dem. Listen oppgir ingen datoer, sier ikke om reservasjonen på {E10000} trekkes fra de 35 %, og sier ingenting om en bankgaranti for forskuddsbetalinger, så Nueva Living ber skriftlig om hvert punkt før enhver reservasjon.',
  'De två procentsatserna utgör tillsammans hela priset, och {T} läggs till på var och en. Listan anger inga datum, säger inte om bokningen på {E10000} dras av från de 35 %, och säger ingenting om en bankgaranti för förskottsbetalningar, så Nueva Living begär varje punkt skriftligen före varje bokning.')

# ---- enquiry, FAQ, SEO -----------------------------------------------------------------------------------

a('.enquiry.headlineHtml',
  'Pregunte por <em>Estepona West Golf Residences</em>', 'Renseignez-vous sur <em>Estepona West Golf Residences</em>', 'Fragen Sie nach <em>Estepona West Golf Residences</em>',
  'Узнайте о <em>Estepona West Golf Residences</em>', 'استفسر عن <em>Estepona West Golf Residences</em>', 'Vraag naar <em>Estepona West Golf Residences</em>',
  'Zapytanie o <em>Estepona West Golf Residences</em>', 'Spør om <em>Estepona West Golf Residences</em>', 'Fråga om <em>Estepona West Golf Residences</em>')
a('.enquiry.message',
  'Hola, Nueva Living, me gustaría recibir información sobre Estepona West Golf Residences.',
  'Bonjour Nueva Living, je souhaiterais des informations sur Estepona West Golf Residences.',
  'Guten Tag Nueva Living, ich möchte Informationen zu Estepona West Golf Residences erhalten.',
  'Здравствуйте, Nueva Living! Хочу получить информацию о Estepona West Golf Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Estepona West Golf Residences.',
  'Goedendag Nueva Living, ik wil graag informatie over Estepona West Golf Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje o Estepona West Golf Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Estepona West Golf Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Estepona West Golf Residences.')
a('.faq[0][1]',
  '17 de las 19 de la lista de precios del promotor de noviembre de 2026: once apartamentos de dos dormitorios de {E473000} a {E572000} y seis apartamentos de tres dormitorios de {E560000} a {E687000}, más {T}. Las otras 2 figuran como reservadas.',
  '17 des 19 de la liste de prix du promoteur de novembre 2026 : onze appartements de deux chambres de {E473000} à {E572000} et six appartements de trois chambres de {E560000} à {E687000}, hors {T}. Les 2 autres sont marqués comme réservés.',
  '17 der 19 auf der Preisliste des Bauträgers vom November 2026: elf Wohnungen mit zwei Schlafzimmern von {E473000} bis {E572000} und sechs Wohnungen mit drei Schlafzimmern von {E560000} bis {E687000}, zuzüglich {T}. Die übrigen 2 sind als reserviert gekennzeichnet.',
  '17 из 19 в прайс-листе застройщика за ноябрь 2026 года: одиннадцать апартаментов с двумя спальнями от {E473000} до {E572000} и шесть с тремя спальнями от {E560000} до {E687000}, без {T}. Остальные 2 отмечены как забронированные.',
  '17 من أصل 19 في قائمة أسعار المطوّر لشهر نوفمبر 2026: أحد عشر شقة بغرفتي نوم من {E473000} إلى {E572000} وست شقق بثلاث غرف نوم من {E560000} إلى {E687000}، زائد {T}. أما المسكنان الآخران فمشار إليهما على أنهما محجوزان.',
  '17 van de 19 op de prijslijst van de ontwikkelaar van november 2026: elf appartementen met twee slaapkamers van {E473000} tot {E572000} en zes appartementen met drie slaapkamers van {E560000} tot {E687000}, plus {T}. De overige 2 zijn als gereserveerd gemarkeerd.',
  '17 z 19 w cenniku dewelopera z listopada 2026 roku: jedenaście apartamentów z dwiema sypialniami od {E473000} do {E572000} i sześć apartamentów z trzema sypialniami od {E560000} do {E687000}, plus {T}. Pozostałe 2 są oznaczone jako zarezerwowane.',
  '17 av de 19 i utbyggerens prisliste fra november 2026: elleve leiligheter med to soverom fra {E473000} til {E572000} og seks leiligheter med tre soverom fra {E560000} til {E687000}, pluss {T}. De øvrige 2 er markert som reservert.',
  '17 av de 19 i exploatörens prislista från november 2026: elva lägenheter med två sovrum från {E473000} till {E572000} och sex lägenheter med tre sovrum från {E560000} till {E687000}, plus {T}. De övriga 2 är markerade som reserverade.')
a('.faq[1][1]',
  'No. La lista dice que el IVA del 10 % no está incluido. El IVA es del 10 % y el impuesto de actos jurídicos documentados del {N1.20} %, y los gastos de notaría y registro se suman. Confirmamos los impuestos y los gastos de compra por escrito.',
  'Non. La liste indique que la TVA à 10 % n’est pas comprise. La TVA est de 10 % et le droit de timbre de {N1.20} %, et les frais de notaire et d’enregistrement s’y ajoutent. Nous confirmons les taxes et les frais d’achat par écrit.',
  'Nein. Die Liste gibt an, dass die MwSt. von 10 % nicht enthalten ist. Die MwSt. beträgt 10 % und die Stempelsteuer {N1.20} %, hinzu kommen Notar- und Grundbuchkosten. Wir bestätigen die Steuern und die Kaufnebenkosten schriftlich.',
  'Нет. В списке сказано, что НДС 10 % не включён. НДС составляет 10 %, гербовый сбор — {N1.20} %, а расходы на нотариуса и регистрацию добавляются сверху. Налоги и расходы на покупку мы подтверждаем в письменной форме.',
  'لا. تذكر القائمة أن ضريبة القيمة المضافة بنسبة 10% غير مشمولة. وضريبة القيمة المضافة 10% ورسم الدمغة {N1.20}%، وتُضاف إليهما أتعاب التوثيق والتسجيل. نؤكد الضرائب وتكاليف الشراء كتابةً.',
  'Nee. De lijst geeft aan dat 10% btw niet is inbegrepen. De btw is 10% en de overdrachtsbelasting {N1.20}%, en notaris- en kadasterkosten komen daar bovenop. Wij bevestigen de belastingen en de aankoopkosten schriftelijk.',
  'Nie. Cennik podaje, że VAT w wysokości 10% nie jest wliczony. VAT wynosi 10%, a podatek od czynności cywilnoprawnych {N1.20}%, do tego dochodzą opłaty notarialne i wpis do księgi wieczystej. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Listen oppgir at 10 % merverdiavgift ikke er inkludert. Merverdiavgiften er 10 % og dokumentavgiften {N1.20} %, og notar- og tinglysingsgebyrer kommer i tillegg. Vi bekrefter avgiftene og kjøpskostnadene skriftlig.',
  'Nej. Listan anger att IVA (spansk moms) på 10 % inte ingår. IVA är 10 % och stämpelskatten {N1.20} %, och notarie- och registreringsavgifter tillkommer. Vi bekräftar skatter och köpkostnader skriftligen.')
a('.faq[2][1]',
  'Sí, la lista de precios dice que cada precio incluye la plaza o plazas de garaje asignadas y el trastero, que numera por nivel, S-1 o S-2. Los confirmamos por escrito para la vivienda que usted elija.',
  'Oui, la liste de prix indique que chaque prix comprend la ou les places de parking attribuées et la cave, qu’elle numérote par niveau, S-1 ou S-2. Nous les confirmons par écrit pour le logement que vous choisissez.',
  'Ja, die Preisliste gibt an, dass jeder Preis den zugewiesenen Stellplatz oder die Stellplätze und den Abstellraum enthält, die sie nach Ebene nummeriert, S-1 oder S-2. Wir bestätigen sie schriftlich für die Wohnung, die Sie wählen.',
  'Да, в прайс-листе сказано, что каждая цена включает закреплённое машиноместо или машиноместа и кладовую, которые пронумерованы по уровням, S-1 или S-2. Мы подтверждаем их в письменной форме для выбранной вами квартиры.',
  'نعم، تذكر قائمة الأسعار أن كل سعر يشمل موقف السيارات أو مواقفها المخصصة والمخزن، وترقّمها بحسب المستوى، S-1 أو S-2. نؤكدها كتابةً للمسكن الذي تختاره.',
  'Ja, de prijslijst zegt dat elke prijs de toegewezen parkeerplaats of parkeerplaatsen en de berging omvat, die ze per niveau nummert, S-1 of S-2. Wij bevestigen ze schriftelijk voor de woning die u kiest.',
  'Tak, cennik podaje, że każda cena obejmuje przypisane miejsce lub miejsca postojowe i komórkę lokatorską, które numeruje według poziomu, S-1 lub S-2. Potwierdzamy je na piśmie dla wybranego lokalu.',
  'Ja, prislisten sier at hver pris inkluderer den tildelte parkeringsplassen eller -plassene og bodet, som den nummererer etter nivå, S-1 eller S-2. Vi bekrefter dem skriftlig for boligen De velger.',
  'Ja, prislistan anger att varje pris inkluderar den tilldelade parkeringsplatsen eller -platserna och förrådet, som den numrerar efter plan, S-1 eller S-2. Vi bekräftar dem skriftligen för den bostad ni väljer.')
a('.faq[3][1]',
  '{E10000} + {T} en la reserva ({E11000} con {T}), el 35 % + {T} en el contrato privado y el 65 % + {T} en la firma de la escritura. La lista no da fechas.',
  '{E10000} + {T} à la réservation ({E11000} TVA comprise), 35 % + {T} au contrat privé et 65 % + {T} à la signature de l’acte notarié. La liste ne donne pas de dates.',
  '{E10000} + {T} bei der Reservierung ({E11000} inkl. {T}), 35 % + {T} beim privaten Vertrag und 65 % + {T} bei der Unterzeichnung der notariellen Urkunde. Die Liste nennt keine Daten.',
  '{E10000} + {T} при бронировании ({E11000} с {T}), 35 % + {T} при частном договоре и 65 % + {T} при подписании нотариального акта. В списке нет дат.',
  '{E10000} + {T} عند الحجز ({E11000} شاملة {T})، و35% + {T} عند العقد الخاص و65% + {T} عند توقيع سند الملكية. ولا تذكر القائمة تواريخ.',
  '{E10000} + {T} bij de reservering ({E11000} incl. {T}), 35% + {T} bij het privécontract en 65% + {T} bij de ondertekening van de notariële akte. De lijst geeft geen data.',
  '{E10000} + {T} przy rezerwacji ({E11000} z {T}), 35% + {T} przy umowie prywatnej i 65% + {T} przy podpisaniu aktu notarialnego. Cennik nie podaje terminów.',
  '{E10000} + {T} ved reservasjon ({E11000} inkl. mva.), 35 % + {T} ved den private kontrakten og 65 % + {T} ved signeringen av skjøtet. Listen oppgir ingen datoer.',
  '{E10000} + {T} vid bokning ({E11000} inkl. {T}), 35 % + {T} vid det privata avtalet och 65 % + {T} vid undertecknandet av lagfarten. Listan anger inga datum.')
a('.faq[5][0]',
  '¿Hay un plano de cada vivienda?', 'Existe-t-il un plan pour chaque logement ?', 'Gibt es für jede Wohnung einen Grundriss?', 'Есть ли планировка для каждой квартиры?',
  'هل يوجد مخطط لكل مسكن؟', 'Is er voor elke woning een plattegrond?', 'Czy każdy lokal ma rzut?', 'Finnes det en tegning for hver bolig?', 'Finns det en ritning för varje bostad?')
a('.faq[5][1]',
  'No. Hay planos de 5 de las 17: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A y 04-03-01-B. Las otras 12 no tienen, y se los pedimos al promotor. Los planos son preliminares, con superficies aproximadas.',
  'Non. Il existe des plans pour 5 des 17 : 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A et 04-03-01-B. Les 12 autres n’en ont pas, et nous les demandons au promoteur. Les plans sont préliminaires, avec des surfaces approximatives.',
  'Nein. Es gibt Grundrisse für 5 der 17: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A und 04-03-01-B. Die anderen 12 haben keinen, und wir fordern sie beim Bauträger an. Die Pläne sind vorläufig, mit ungefähren Flächen.',
  'Нет. Планировки есть для 5 из 17: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A и 04-03-01-B. У остальных 12 их нет, и мы запрашиваем их у застройщика. Планировки предварительные, с приблизительными площадями.',
  'لا. توجد مخططات لـ5 من المساكن السبعة عشر: 01-03-00-C، 04-01-00-B، 04-01-02-A، 04-03-00-A و04-03-01-B. أما الاثنا عشر الأخرى فليس لها مخططات، ونطلبها من المطوّر. والمخططات أولية بمساحات تقريبية.',
  'Nee. Er zijn plattegronden voor 5 van de 17: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A en 04-03-01-B. De andere 12 hebben er geen, en wij vragen ze op bij de ontwikkelaar. De plattegronden zijn voorlopig, met oppervlaktes bij benadering.',
  'Nie. Rzuty są dla 5 z 17: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A i 04-03-01-B. Pozostałe 12 ich nie ma i prosimy o nie dewelopera. Rzuty są wstępne, z przybliżonymi powierzchniami.',
  'Nei. Det finnes tegninger for 5 av de 17: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A og 04-03-01-B. De øvrige 12 har ingen, og vi ber utbyggeren om dem. Tegningene er foreløpige, med omtrentlige arealer.',
  'Nej. Det finns ritningar för 5 av de 17: 01-03-00-C, 04-01-00-B, 04-01-02-A, 04-03-00-A och 04-03-01-B. De övriga 12 har ingen, och vi begär dem av exploatören. Ritningarna är preliminära, med ungefärliga ytor.')
a('.faq[6][1]',
  'No. El folleto dice que el mobiliario se muestra solo para ilustrar el uso de los espacios y que no está incluido. Las cocinas llevan los electrodomésticos que enumera el informe de calidades.',
  'Non. La brochure indique que le mobilier est montré seulement pour illustrer l’usage des espaces et n’est pas inclus. Les cuisines sont livrées avec les appareils que liste le rapport de qualité.',
  'Nein. Die Broschüre gibt an, dass Möbel nur zur Veranschaulichung der Raumnutzung gezeigt werden und nicht enthalten sind. Die Küchen werden mit den im Qualitätsbericht aufgeführten Geräten geliefert.',
  'Нет. В брошюре сказано, что мебель показана лишь для иллюстрации использования помещений и не входит в поставку. Кухни поставляются с техникой, перечисленной в отчёте о качестве.',
  'لا. يذكر الكتيّب أن الأثاث معروض لتوضيح استخدام المساحات فقط وأنه غير مشمول. وتأتي المطابخ مع الأجهزة المذكورة في تقرير الجودة.',
  'Nee. De brochure zegt dat het meubilair alleen is getoond om het gebruik van de ruimtes te illustreren en niet is inbegrepen. De keukens worden geleverd met de apparatuur uit het kwaliteitsrapport.',
  'Nie. Broszura podaje, że meble pokazano wyłącznie dla zilustrowania sposobu użytkowania przestrzeni i nie są wliczone w cenę. Kuchnie są wyposażone w sprzęt wymieniony w raporcie jakości.',
  'Nei. Brosjyren sier at møblene bare vises for å illustrere bruken av rommene og ikke er inkludert. Kjøkkenene leveres med apparatene som kvalitetsrapporten oppgir.',
  'Nej. Broschyren anger att möblerna bara visas för att illustrera hur ytorna kan användas och inte ingår. Köken levereras med de apparater som kvalitetsrapporten anger.')
a('.faq[7][1]',
  'Sí. La lista dice que la disponibilidad y los precios pueden cambiar sin previo aviso. Reconfirmamos el precio antes de que usted reserve.',
  'Oui. La liste indique que la disponibilité et les prix peuvent changer sans préavis. Nous reconfirmons le prix avant que vous ne réserviez.',
  'Ja. Die Liste gibt an, dass Verfügbarkeit und Preise ohne Vorankündigung geändert werden können. Wir bestätigen den Preis erneut, bevor Sie reservieren.',
  'Да. В списке сказано, что наличие и цены могут измениться без предварительного уведомления. Мы заново подтверждаем цену до того, как вы забронируете.',
  'نعم. تذكر القائمة أن التوفر والأسعار قابلان للتغيير دون إشعار مسبق. نعيد تأكيد السعر قبل أن تحجز.',
  'Ja. De lijst zegt dat beschikbaarheid en prijzen zonder voorafgaande kennisgeving kunnen veranderen. Wij bevestigen de prijs opnieuw voordat u reserveert.',
  'Tak. Cennik podaje, że dostępność i ceny mogą ulec zmianie bez uprzedzenia. Cenę potwierdzamy ponownie przed rezerwacją.',
  'Ja. Listen sier at tilgjengelighet og priser kan endres uten forvarsel. Vi bekrefter prisen på nytt før reservasjon.',
  'Ja. Listan anger att tillgänglighet och priser kan ändras utan förvarning. Vi bekräftar priset på nytt före bokning.')
a('.seo.title',
  'Estepona West Golf Residences - Apartamentos en Estepona', 'Estepona West Golf Residences - Appartements à Estepona', 'Estepona West Golf Residences - Wohnungen in Estepona',
  'Estepona West Golf Residences - квартиры в Эстепоне', 'Estepona West Golf Residences - شقق في إستيبونا', 'Estepona West Golf Residences - Appartementen in Estepona',
  'Estepona West Golf Residences - apartamenty w Esteponie', 'Estepona West Golf Residences - leiligheter i Estepona', 'Estepona West Golf Residences - lägenheter i Estepona')
a('.seo.h1',
  'Estepona West Golf Residences: apartamentos en Estepona', 'Estepona West Golf Residences : appartements à Estepona', 'Estepona West Golf Residences: Wohnungen in Estepona',
  'Estepona West Golf Residences: квартиры в Эстепоне', 'Estepona West Golf Residences: شقق في إستيبونا', 'Estepona West Golf Residences: appartementen in Estepona',
  'Estepona West Golf Residences: apartamenty w Esteponie', 'Estepona West Golf Residences: leiligheter i Estepona', 'Estepona West Golf Residences: lägenheter i Estepona')
a('.seo.h1Context',
  'Apartamentos en Estepona', 'Appartements à Estepona', 'Wohnungen in Estepona', 'Квартиры в Эстепоне', 'شقق في إستيبونا', 'Appartementen in Estepona',
  'Apartamenty w Esteponie', 'Leiligheter i Estepona', 'Lägenheter i Estepona')

json.dump(T, open(f'{SP}/tr_w.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings to', f'{SP}/tr_w.json')
