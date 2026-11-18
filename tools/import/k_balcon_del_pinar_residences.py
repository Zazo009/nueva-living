# -*- coding: utf-8 -*-
"""Balcón del Pinar Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_b.json keyed by the English string, as assemble.py expects. Tokens: {E425000}
money, {N65.05} decimal number, {U} the area unit, {T} the tax word.
    python3 tools/import/k_balcon_del_pinar_residences.py <scratch dir>   (writes <dir>/tr_b.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة',
        'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
T = {}
SLUG = 'balcon-del-pinar-residences'
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


CGP = {'es': 'Vista generada por ordenador ', 'fr': 'Vue générée par ordinateur ', 'de': 'Computergenerierte Ansicht ',
       'ru': 'Компьютерная визуализация ', 'ar': 'منظر مولَّد بالحاسوب ', 'nl': 'Computergegenereerd beeld ',
       'pl': 'Wygenerowany komputerowo widok ', 'no': 'Datagenerert bilde ', 'sv': 'Datorgenererad vy '}


def cg(path, *tr):
    assert len(tr) == 9, path
    en = get(path)
    assert en.startswith('Computer-generated view '), en
    put(en, [CGP[l] + t for l, t in zip(LOCS, tr)])


same(get('.name')); same(get('.shortName')); same(get('.titleHtml')); put('Torremolinos', ['Torremolinos', 'Torremolinos', 'Torremolinos', 'Торремолинос', 'توريمولينوس', 'Torremolinos', 'Torremolinos', 'Torremolinos', 'Torremolinos']); same(proj['location']['mapArea'])
for u in proj['availability']['units']:
    same(u['reference'])

# ---- description, SEO, hero, card -------------------------------------------------------------

a('.description',
  'Apartamentos de dos y tres dormitorios y un ático con terrazas en una ladera de Torremolinos, frente a un pinar, con piscina exterior, spa interior, gimnasio y sala de coworking. La lista de precios del promotor del 1 de noviembre de 2026 recoge 16 viviendas, desde {E425000} antes de {T}.',
  'Appartements de deux et trois chambres et un penthouse avec terrasses sur un coteau de Torremolinos, face à une pinède, avec piscine extérieure, spa intérieur, salle de sport et espace de coworking. La liste de prix du promoteur du 1er novembre 2026 compte 16 logements, à partir de {E425000} hors {T}.',
  'Wohnungen mit zwei und drei Schlafzimmern und ein Penthouse mit Terrassen an einem Hang in Torremolinos, gegenüber einem Pinienwald, mit Außenpool, Indoor-Spa, Fitnessraum und Coworking-Raum. Die Preisliste des Bauträgers vom 1. November 2026 führt 16 Wohnungen, ab {E425000} vor {T}.',
  'Апартаменты с двумя и тремя спальнями и пентхаус с террасами на склоне в Торремолиносе, напротив соснового леса, с открытым бассейном, спа в помещении, тренажёрным залом и коворкингом. В прайс-листе застройщика от 1 ноября 2026 года 16 квартир, от {E425000} без {T}.',
  'شقق بغرفتي نوم وثلاث غرف نوم وبنتهاوس مع تراسات على سفح تلة في توريمولينوس، قبالة غابة صنوبر، مع مسبح خارجي وسبا داخلي وصالة رياضية وقاعة للعمل المشترك. تضم قائمة أسعار المطوّر بتاريخ 1 نوفمبر 2026 ستة عشر مسكنًا، ابتداءً من {E425000} قبل {T}.',
  'Appartementen met twee en drie slaapkamers en een penthouse met terrassen op een helling in Torremolinos, tegenover een dennenbos, met een buitenzwembad, een binnenspa, een fitnessruimte en een coworkingruimte. De prijslijst van de ontwikkelaar van 1 november 2026 noemt 16 woningen, vanaf {E425000} exclusief {T}.',
  'Apartamenty z dwiema i trzema sypialniami oraz penthouse z tarasami na zboczu w Torremolinos, naprzeciw lasu sosnowego, z basenem zewnętrznym, spa w budynku, siłownią i salą coworkingową. Cennik dewelopera z 1 listopada 2026 roku obejmuje 16 lokali, od {E425000} bez {T}.',
  'Leiligheter med to og tre soverom og en toppleilighet med terrasser i en skråning i Torremolinos, rett overfor en furuskog, med utendørs basseng, innendørs spa, treningsrom og coworking-rom. Utbyggerens prisliste fra 1. november 2026 har 16 boliger, fra {E425000} før {T}.',
  'Lägenheter med två och tre sovrum och en takvåning med terrasser i en sluttning i Torremolinos, mitt emot en tallskog, med utomhuspool, inomhusspa, gym och coworking-rum. Exploatörens prislista från den 1 november 2026 har 16 bostäder, från {E425000} före {T} (spansk moms).')
a('.seoDescription',
  'Apartamentos nuevos de dos y tres dormitorios con terrazas en Torremolinos, frente a un pinar, con piscina, spa interior, gimnasio y coworking. 16 viviendas en lista desde {E425000} más {T}.',
  'Appartements neufs de deux et trois chambres avec terrasses à Torremolinos, face à une pinède, avec piscine, spa intérieur, salle de sport et coworking. 16 logements listés dès {E425000} hors {T}.',
  'Neue Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Torremolinos, gegenüber einem Pinienwald, mit Pool, Indoor-Spa, Fitnessraum und Coworking. 16 gelistete Wohnungen ab {E425000} zuzüglich {T}.',
  'Новые апартаменты с двумя и тремя спальнями и террасами в Торремолиносе, напротив соснового леса, с бассейном, спа, тренажёрным залом и коворкингом. 16 квартир в списке, от {E425000} плюс {T}.',
  'شقق جديدة بغرفتي نوم وثلاث غرف نوم مع تراسات في توريمولينوس، قبالة غابة صنوبر، مع مسبح وسبا داخلي وصالة رياضية وعمل مشترك. 16 مسكنًا مدرجًا ابتداءً من {E425000} زائد {T}.',
  'Nieuwe appartementen met twee en drie slaapkamers en terrassen in Torremolinos, tegenover een dennenbos, met zwembad, binnenspa, fitnessruimte en coworking. 16 vermelde woningen vanaf {E425000} plus {T}.',
  'Nowe apartamenty z dwiema i trzema sypialniami oraz tarasami w Torremolinos, naprzeciw lasu sosnowego, z basenem, spa, siłownią i coworkingiem. 16 lokali z cennika od {E425000} plus {T}.',
  'Nye leiligheter med to og tre soverom og terrasser i Torremolinos, rett overfor en furuskog, med basseng, innendørs spa, treningsrom og coworking. 16 oppførte boliger fra {E425000} pluss {T}.',
  'Nya lägenheter med två och tre sovrum och terrasser i Torremolinos, mitt emot en tallskog, med pool, inomhusspa, gym och coworking. 16 listade bostäder från {E425000} plus {T}.')
a('.twitterDescription',
  'Apartamentos de dos y tres dormitorios con terrazas en Torremolinos, desde {E425000} más {T}.',
  'Appartements de deux et trois chambres avec terrasses à Torremolinos, à partir de {E425000} hors {T}.',
  'Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Torremolinos, ab {E425000} zuzüglich {T}.',
  'Апартаменты с двумя и тремя спальнями и террасами в Торремолиносе, от {E425000} плюс {T}.',
  'شقق بغرفتي نوم وثلاث غرف نوم مع تراسات في توريمولينوس، ابتداءً من {E425000} زائد {T}.',
  'Appartementen met twee en drie slaapkamers en terrassen in Torremolinos, vanaf {E425000} plus {T}.',
  'Apartamenty z dwiema i trzema sypialniami oraz tarasami w Torremolinos, od {E425000} plus {T}.',
  'Leiligheter med to og tre soverom og terrasser i Torremolinos, fra {E425000} pluss {T}.',
  'Lägenheter med två och tre sovrum och terrasser i Torremolinos, från {E425000} plus {T}.')
a('.hero.eyebrow',
  '16 viviendas en la lista de precios', '16 logements sur la liste de prix', '16 Wohnungen auf der Preisliste',
  '16 квартир в прайс-листе', '16 مسكنًا في قائمة الأسعار', '16 woningen op de prijslijst',
  '16 lokali w cenniku', '16 boliger i prislisten', '16 bostäder i prislistan')
a('.hero.startingPrice',
  'Desde {E425000} + {T}', 'À partir de {E425000} + {T}', 'Ab {E425000} + {T}', 'От {E425000} + {T}', 'ابتداءً من {E425000} + {T}',
  'Vanaf {E425000} + {T}', 'Od {E425000} + {T}', 'Fra {E425000} + mva.', 'Från {E425000} + {T}')
a('.card.description',
  '16 apartamentos de dos y tres dormitorios y un ático con terrazas en Torremolinos, frente a un pinar, con piscina, spa interior, gimnasio y sala de coworking, desde {E425000} + {T}.',
  '16 appartements de deux et trois chambres et un penthouse avec terrasses à Torremolinos, face à une pinède, avec piscine, spa intérieur, salle de sport et espace de coworking, à partir de {E425000} + {T}.',
  '16 gelistete Wohnungen mit zwei und drei Schlafzimmern und ein Penthouse mit Terrassen in Torremolinos, gegenüber einem Pinienwald, mit Pool, Indoor-Spa, Fitnessraum und Coworking-Raum, ab {E425000} + {T}.',
  '16 квартир с двумя и тремя спальнями и пентхаус с террасами в Торремолиносе, напротив соснового леса, с бассейном, спа в помещении, тренажёрным залом и коворкингом, от {E425000} + {T}.',
  '16 شقة مدرجة بغرفتي نوم وثلاث غرف نوم وبنتهاوس مع تراسات في توريمولينوس، قبالة غابة صنوبر، مع مسبح وسبا داخلي وصالة رياضية وقاعة للعمل المشترك، ابتداءً من {E425000} + {T}.',
  '16 vermelde appartementen met twee en drie slaapkamers en een penthouse met terrassen in Torremolinos, tegenover een dennenbos, met zwembad, binnenspa, fitnessruimte en coworkingruimte, vanaf {E425000} + {T}.',
  '16 wymienionych mieszkań z dwiema i trzema sypialniami oraz penthouse z tarasami w Torremolinos, naprzeciw lasu sosnowego, z basenem, spa w budynku, siłownią i salą coworkingową, od {E425000} + {T}.',
  '16 oppførte leiligheter med to og tre soverom og en toppleilighet med terrasser i Torremolinos, rett overfor en furuskog, med basseng, innendørs spa, treningsrom og coworking-rom, fra {E425000} + mva.',
  '16 listade lägenheter med två och tre sovrum och en takvåning med terrasser i Torremolinos, mitt emot en tallskog, med pool, inomhusspa, gym och coworking-rum, från {E425000} + {T}.')
a('.card.meta[0][1]',
  '{E425000} + {T}', '{E425000} + {T}', '{E425000} + {T}', '{E425000} + {T}', '{E425000} + {T}', '{E425000} + {T}', '{E425000} + {T}',
  '{E425000} + mva.', '{E425000} + {T}')
a('.availability.priceRange',
  '{E425000} - {E802000} + {T}', '{E425000} - {E802000} + {T}', '{E425000} - {E802000} + {T}', '{E425000} - {E802000} + {T}',
  '{E425000} - {E802000} + {T}', '{E425000} - {E802000} + {T}', '{E425000} - {E802000} + {T}', '{E425000} - {E802000} + mva.',
  '{E425000} - {E802000} + {T}')

# ---- image alt text ---------------------------------------------------------------------------

cg('.images.hero.alt',
   'de la piscina exterior junto al edificio, con tumbonas a lo largo de un muro de piedra con plantas, terrazas curvas con techos de madera encima y colinas y la costa tras una barandilla de vidrio',
   'de la piscine extérieure au pied du bâtiment, avec des transats le long d’un mur de pierre planté, des terrasses courbes aux sous-faces en bois au-dessus et des collines et la côte derrière un garde-corps en verre',
   'des Außenpools am Gebäude, mit Liegen entlang einer bepflanzten Steinmauer, geschwungenen Terrassen mit Holzuntersichten darüber und Hügeln und der Küste hinter einer Glasbrüstung',
   'открытого бассейна у здания: шезлонги вдоль каменной стены с зеленью, над ними изогнутые террасы с деревянной подшивкой, за стеклянным ограждением холмы и побережье',
   'للمسبح الخارجي بجانب المبنى، مع كراسٍ للاستلقاء بمحاذاة جدار حجري مزروع وتراسات منحنية بأسقف خشبية في الأعلى، والتلال والساحل خلف حاجز زجاجي',
   'van het buitenzwembad naast het gebouw, met ligbedden langs een beplante stenen muur, gebogen terrassen met houten plafonds erboven en heuvels en de kust achter een glazen balustrade',
   'basenu zewnętrznego przy budynku, z leżakami wzdłuż obsadzonego roślinami kamiennego muru, zakrzywionymi tarasami z drewnianymi podsufitkami powyżej oraz wzgórzami i wybrzeżem za szklaną balustradą',
   'av det utendørs bassenget ved bygningen, med solsenger langs en beplantet steinmur, buede terrasser med trehimlinger over og åser og kysten bak et glassrekkverk',
   'av utomhuspoolen vid byggnaden, med solstolar längs en planterad stenmur, böjda terrasser med trätak ovanför och kullar och kusten bakom ett glasräcke')
cg('.images.architecture.alt',
   'del edificio al anochecer, con largas terrazas curvas, barandillas de vidrio, techos de madera iluminados y una pérgola en la planta superior, sobre la piscina y un zócalo de piedra con plantas',
   'du bâtiment au crépuscule, avec de longues terrasses courbes, des garde-corps en verre, des sous-faces en bois éclairées et une pergola au dernier étage, au-dessus de la piscine et d’un socle de pierre planté',
   'des Gebäudes in der Abenddämmerung, mit langen geschwungenen Terrassen, Glasbrüstungen, beleuchteten Holzuntersichten und einer Pergola im obersten Geschoss, über dem Pool und einem bepflanzten Steinsockel',
   'здания в сумерках: длинные изогнутые террасы, стеклянные ограждения, подсвеченная деревянная подшивка и пергола на верхнем этаже над бассейном и каменным цоколем с зеленью',
   'للمبنى عند الغسق، مع تراسات منحنية طويلة وحواجز زجاجية وأسقف خشبية مضاءة وعريشة في الطابق العلوي، فوق المسبح وقاعدة حجرية مزروعة',
   'van het gebouw in de schemering, met lange gebogen terrassen, glazen balustrades, verlichte houten plafonds en een pergola op de bovenste verdieping, boven het zwembad en een beplante stenen sokkel',
   'budynku o zmierzchu, z długimi zakrzywionymi tarasami, szklanymi balustradami, podświetlonymi drewnianymi podsufitkami i pergolą na najwyższym piętrze, nad basenem i obsadzonym roślinami kamiennym cokołem',
   'av bygningen i skumringen, med lange buede terrasser, glassrekkverk, opplyste trehimlinger og en pergola i øverste etasje, over bassenget og en beplantet steinsokkel',
   'av byggnaden i skymningen, med långa böjda terrasser, glasräcken, upplysta trätak och en pergola på översta våningen, ovanför poolen och en planterad stensockel')
cg('.images.lifestyle.alt',
   'del gimnasio, con cintas de correr, bicicletas estáticas, una máquina de remo, pesas libres y esterillas, y un ventanal alargado',
   'de la salle de sport, avec des tapis de course, des vélos d’appartement, un rameur, des poids libres et des tapis, et une longue baie vitrée',
   'des Fitnessraums mit Laufbändern, Heimtrainern, einem Rudergerät, freien Gewichten und Matten sowie einem langen Fensterband',
   'тренажёрного зала: беговые дорожки, велотренажёры, гребной тренажёр, свободные веса и коврики, длинное окно',
   'للصالة الرياضية، مع أجهزة مشي ودراجات ثابتة وجهاز تجديف وأوزان حرة وحُصُر، ونافذة طويلة',
   'van de fitnessruimte, met loopbanden, hometrainers, een roeimachine, losse gewichten en matten, en een lang raam',
   'siłowni z bieżniami, rowerami stacjonarnymi, wioślarzem, wolnymi ciężarami i matami oraz długim oknem',
   'av treningsrommet, med tredemøller, treningssykler, en romaskin, frivekter og matter, og et langt vindu',
   'av gymmet, med löpband, motionscyklar, en roddmaskin, fria vikter och mattor, och ett långt fönster')
cg('.images.privateViewing.alt',
   'de una terraza con pérgola de madera, una cama de día, una mesa baja y una mesa de comedor, con vistas sobre el pinar hasta el mar',
   'd’une terrasse sous une pergola en bois, avec un lit de jour, une table basse et une table à manger, avec vue sur la pinède jusqu’à la mer',
   'einer Terrasse mit Holzpergola, einem Tagesbett, einem niedrigen Tisch und einem Esstisch, mit Blick über den Pinienwald zum Meer',
   'террасы с деревянной перголой, кушеткой, низким столиком и обеденным столом, с видом на сосновый лес и море',
   'لتراس بعريشة خشبية، مع سرير نهاري وطاولة منخفضة وطاولة طعام، بإطلالة على غابة الصنوبر حتى البحر',
   'van een terras met een houten pergola, een daybed, een lage tafel en een eettafel, met uitzicht over het dennenbos op de zee',
   'tarasu z drewnianą pergolą, leżanką, niskim stolikiem i stołem jadalnianym, z widokiem na las sosnowy i morze',
   'av en terrasse med trepergola, en daybed, et lavt bord og et spisebord, med utsikt over furuskogen til havet',
   'av en terrass med träpergola, en dagbädd, ett lågt bord och ett matbord, med utsikt över tallskogen mot havet')

# ---- media ------------------------------------------------------------------------------------

a('.media.copy',
  'Vistas generadas por ordenador del edificio, la piscina, el spa, el gimnasio, las terrazas y los interiores, del conjunto de imágenes del promotor, una fotografía aérea del avance de obra de diciembre de 2025, el vídeo del promotor y los planos de 15 de las 16 viviendas de la lista de precios.',
  'Vues générées par ordinateur du bâtiment, de la piscine, du spa, de la salle de sport, des terrasses et des intérieurs, tirées du jeu d’images du promoteur, une photographie aérienne de l’avancement des travaux de décembre 2025, le film du promoteur et les plans de 15 des 16 logements de la liste de prix.',
  'Computergenerierte Ansichten des Gebäudes, des Pools, des Spas, des Fitnessraums, der Terrassen und der Innenräume aus dem Bildmaterial des Bauträgers, ein Luftbild vom Baufortschritt im Dezember 2025, der Film des Bauträgers und die Grundrisse von 15 der 16 Wohnungen auf der Preisliste.',
  'Компьютерные визуализации здания, бассейна, спа, тренажёрного зала, террас и интерьеров из набора изображений застройщика, аэрофотоснимок хода строительства за декабрь 2025 года, фильм застройщика и планировки 15 из 16 квартир прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمبنى والمسبح والسبا والصالة الرياضية والتراسات والفضاءات الداخلية من مجموعة صور المطوّر، وصورة جوية لتقدّم الأعمال في ديسمبر 2025، وفيلم المطوّر، ومخططات 15 من المساكن الستة عشر الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van het gebouw, het zwembad, de spa, de fitnessruimte, de terrassen en de interieurs uit de beeldenset van de ontwikkelaar, een luchtfoto van de voortgang van de bouw van december 2025, de film van de ontwikkelaar en de plattegronden van 15 van de 16 woningen op de prijslijst.',
  'Wygenerowane komputerowo widoki budynku, basenu, spa, siłowni, tarasów i wnętrz z zestawu obrazów dewelopera, zdjęcie lotnicze postępu budowy z grudnia 2025 roku, film dewelopera oraz rzuty 15 z 16 lokali z cennika.',
  'Datagenererte bilder av bygningen, bassenget, spaet, treningsrommet, terrassene og interiørene fra utbyggerens bildesett, et flyfoto av byggefremdriften fra desember 2025, utbyggerens film og tegningene av 15 av de 16 boligene i prislisten.',
  'Datorgenererade vyer av byggnaden, poolen, spat, gymmet, terrasserna och interiörerna från exploatörens bilduppsättning, ett flygfoto av byggets framsteg från december 2025, exploatörens film och ritningarna för 15 av de 16 bostäderna i prislistan.')
a('.media.note',
  'Las imágenes son ilustraciones generadas por ordenador, no fotografías del edificio terminado; dos de ellas insertan el edificio en una fotografía aérea real. El folleto dice que sus imágenes son orientativas y que el mobiliario que muestran no está incluido. La fotografía aérea es la imagen de avance de obra del promotor, fechada el 15 de diciembre de 2025. Los planos son los del promotor de noviembre de 2025, recortados de sus hojas para que no quede ningún logotipo ni nombre de proyecto; los nombres de las estancias están en español, las superficies son aproximadas y provisionales hasta la licencia de obras, y los planos no son contractuales.',
  'Les images sont des illustrations générées par ordinateur, et non des photographies du bâtiment achevé ; deux d’entre elles insèrent le bâtiment dans une véritable photographie aérienne. La brochure indique que ses images sont données à titre indicatif et que le mobilier qu’elles montrent n’est pas inclus. La photographie aérienne est l’image d’avancement des travaux du promoteur, datée du 15 décembre 2025. Les plans sont ceux du promoteur de novembre 2025, découpés de leurs feuilles afin qu’il ne reste ni logo ni nom de projet ; les noms des pièces sont en espagnol, les surfaces sont approximatives et provisoires jusqu’au permis de construire, et les plans ne sont pas contractuels.',
  'Die Bilder sind computergenerierte Illustrationen, keine Fotografien des fertigen Gebäudes; zwei davon setzen das Gebäude in ein echtes Luftbild ein. Die Broschüre gibt an, dass ihre Bilder nur zur Orientierung dienen und die gezeigten Möbel nicht enthalten sind. Das Luftbild ist das Baufortschrittsbild des Bauträgers vom 15. Dezember 2025. Die Grundrisse sind die Pläne des Bauträgers vom November 2025, aus ihren Blättern ausgeschnitten, sodass weder Logo noch Projektname übrig bleibt; die Raumbezeichnungen sind spanisch, die Flächen sind ungefähre Angaben und bis zur Baugenehmigung vorläufig, und die Pläne sind nicht vertraglich bindend.',
  'Изображения — компьютерные иллюстрации, а не фотографии готового здания; на двух из них здание вписано в настоящий аэрофотоснимок. В брошюре сказано, что её изображения носят ориентировочный характер, а показанная мебель не входит в поставку. Аэрофотоснимок — изображение хода строительства от застройщика, датированное 15 декабря 2025 года. Планировки — планы застройщика за ноябрь 2025 года, вырезанные из листов так, чтобы на них не осталось ни логотипа, ни названия проекта; названия помещений даны по-испански, площади приблизительные и предварительные до получения разрешения на строительство, а планы не носят договорного характера.',
  'الصور رسوم توضيحية مولَّدة بالحاسوب وليست صورًا فوتوغرافية للمبنى بعد اكتماله، واثنتان منها تُدرجان المبنى في صورة جوية حقيقية. يذكر الكتيّب أن صوره للاسترشاد فقط وأن الأثاث الظاهر فيها غير مشمول. أما الصورة الجوية فهي صورة تقدّم الأعمال الصادرة عن المطوّر بتاريخ 15 ديسمبر 2025. والمخططات هي مخططات المطوّر لشهر نوفمبر 2025، مقصوصة من أوراقها بحيث لا يبقى فيها شعار ولا اسم مشروع؛ وأسماء الغرف عليها بالإسبانية، والمساحات تقريبية ومؤقتة حتى صدور رخصة البناء، والمخططات ليست ملزمة تعاقديًا.',
  'De beelden zijn computergegenereerde illustraties, geen foto’s van het afgewerkte gebouw; twee ervan plaatsen het gebouw in een echte luchtfoto. De brochure zegt dat de beelden slechts indicatief zijn en dat het getoonde meubilair niet is inbegrepen. De luchtfoto is het voortgangsbeeld van de ontwikkelaar, gedateerd 15 december 2025. De plattegronden zijn die van de ontwikkelaar van november 2025, uit hun bladen geknipt zodat er geen logo of projectnaam overblijft; de namen van de ruimtes zijn in het Spaans, de oppervlaktes zijn bij benadering en voorlopig tot de bouwvergunning, en de plannen zijn niet contractueel.',
  'Obrazy to ilustracje wygenerowane komputerowo, a nie zdjęcia ukończonego budynku; dwa z nich wstawiają budynek w prawdziwe zdjęcie lotnicze. Broszura zastrzega, że jej obrazy mają charakter orientacyjny, a pokazane meble nie są wliczone w cenę. Zdjęcie lotnicze to obraz postępu budowy od dewelopera, datowany na 15 grudnia 2025 roku. Rzuty to plany dewelopera z listopada 2025 roku, wycięte z arkuszy tak, by nie został na nich żaden logotyp ani nazwa projektu; nazwy pomieszczeń są po hiszpańsku, powierzchnie są przybliżone i tymczasowe do czasu uzyskania pozwolenia na budowę, a plany nie mają charakteru umownego.',
  'Bildene er datagenererte illustrasjoner, ikke fotografier av den ferdige bygningen; to av dem setter bygningen inn i et ekte flyfoto. Brosjyren sier at bildene bare er veiledende, og at møblene som vises ikke er inkludert. Flyfotoet er utbyggerens fremdriftsbilde, datert 15. desember 2025. Tegningene er utbyggerens tegninger fra november 2025, utklipt fra arkene slik at ingen logo eller prosjektnavn er igjen; romnavnene er på spansk, arealene er omtrentlige og foreløpige frem til byggetillatelsen, og tegningene er ikke kontraktsfestet.',
  'Bilderna är datorgenererade illustrationer, inte fotografier av den färdiga byggnaden; två av dem placerar byggnaden i ett verkligt flygfoto. Broschyren anger att dess bilder bara är vägledande och att de möbler som visas inte ingår. Flygfotot är exploatörens bild av byggets framsteg, daterad den 15 december 2025. Ritningarna är exploatörens ritningar från november 2025, utklippta ur sina blad så att ingen logotyp eller något projektnamn finns kvar; rumsnamnen är på spanska, ytorna är ungefärliga och preliminära fram till bygglovet, och ritningarna är inte avtalsbindande.')
a('.media.video.title',
  'El edificio, la piscina y las viviendas', 'Le bâtiment, la piscine et les logements', 'Das Gebäude, der Pool und die Wohnungen',
  'Здание, бассейн и квартиры', 'المبنى والمسبح والمساكن', 'Het gebouw, het zwembad en de woningen',
  'Budynek, basen i mieszkania', 'Bygningen, bassenget og boligene', 'Byggnaden, poolen och bostäderna')
a('.media.video.caption',
  'El vídeo del promotor, acortado: vistas generadas por ordenador del edificio, la piscina, el spa, el gimnasio, las terrazas y los interiores, intercaladas con imágenes de archivo de personas. Sin sonido.',
  'Le film du promoteur, raccourci : vues générées par ordinateur du bâtiment, de la piscine, du spa, de la salle de sport, des terrasses et des intérieurs, entrecoupées d’images d’archives de personnes. Sans son.',
  'Der Film des Bauträgers, gekürzt: computergenerierte Ansichten des Gebäudes, des Pools, des Spas, des Fitnessraums, der Terrassen und der Innenräume, geschnitten mit Archivaufnahmen von Menschen. Ohne Ton.',
  'Фильм застройщика в сокращённом виде: компьютерные визуализации здания, бассейна, спа, тренажёрного зала, террас и интерьеров вперемежку со стоковыми кадрами с людьми. Без звука.',
  'فيلم المطوّر بعد اختصاره: مناظر مولَّدة بالحاسوب للمبنى والمسبح والسبا والصالة الرياضية والتراسات والفضاءات الداخلية، تتخللها لقطات أرشيفية لأشخاص. يُعرض دون صوت.',
  'De film van de ontwikkelaar, ingekort: computergegenereerde beelden van het gebouw, het zwembad, de spa, de fitnessruimte, de terrassen en de interieurs, afgewisseld met stockbeelden van mensen. Zonder geluid.',
  'Film dewelopera w skróconej wersji: wygenerowane komputerowo widoki budynku, basenu, spa, siłowni, tarasów i wnętrz, przeplatane archiwalnymi ujęciami ludzi. Bez dźwięku.',
  'Utbyggerens film, forkortet: datagenererte bilder av bygningen, bassenget, spaet, treningsrommet, terrassene og interiørene, klippet sammen med arkivopptak av mennesker. Uten lyd.',
  'Exploatörens film, förkortad: datorgenererade vyer av byggnaden, poolen, spat, gymmet, terrasserna och interiörerna, varvade med arkivbilder av människor. Utan ljud.')
a('.media.video.alt',
  'Vídeo de vistas generadas por ordenador del edificio, sus zonas comunes y sus viviendas',
  'Film de vues générées par ordinateur du bâtiment, de ses espaces communs et de ses logements',
  'Film mit computergenerierten Ansichten des Gebäudes, seiner Gemeinschaftsbereiche und seiner Wohnungen',
  'Фильм с компьютерными визуализациями здания, его общих зон и квартир',
  'فيلم لمناظر مولَّدة بالحاسوب للمبنى ومرافقه المشتركة ومساكنه',
  'Film met computergegenereerde beelden van het gebouw, de gemeenschappelijke ruimtes en de woningen',
  'Film z wygenerowanymi komputerowo widokami budynku, jego części wspólnych i mieszkań',
  'Film med datagenererte bilder av bygningen, fellesarealene og boligene',
  'Film med datorgenererade vyer av byggnaden, dess gemensamma ytor och bostäder')

AERIAL = {
 'es': 'Imagen generada por ordenador del edificio insertado en una fotografía aérea, ',
 'fr': 'Image générée par ordinateur du bâtiment inséré dans une photographie aérienne, ',
 'de': 'Computergeneriertes Bild des Gebäudes, eingesetzt in ein Luftbild, ',
 'ru': 'Компьютерное изображение здания, вписанного в аэрофотоснимок: ',
 'ar': 'صورة مولَّدة بالحاسوب للمبنى مُدرَجًا في صورة جوية، ',
 'nl': 'Computergegenereerd beeld van het gebouw, ingevoegd in een luchtfoto, ',
 'pl': 'Wygenerowany komputerowo obraz budynku wstawionego w zdjęcie lotnicze, ',
 'no': 'Datagenerert bilde av bygningen satt inn i et flyfoto, ',
 'sv': 'Datorgenererad bild av byggnaden infogad i ett flygfoto, '}


def aerial(path, *tr):
    put(get(path), [AERIAL[l] + t for l, t in zip(LOCS, tr)])


aerial('.media.items[2].alt',
       'junto a una carretera al borde de un pinar, con Torremolinos y el mar al fondo',
       'le long d’une route en lisière d’une pinède, avec Torremolinos et la mer au loin',
       'an einer Straße am Rand eines Pinienwalds, mit Torremolinos und dem Meer dahinter',
       'у дороги на краю соснового леса, за ним Торремолинос и море',
       'بجانب طريق عند طرف غابة صنوبر، وخلفه توريمولينوس والبحر',
       'langs een weg aan de rand van een dennenbos, met Torremolinos en de zee erachter',
       'przy drodze na skraju lasu sosnowego, z Torremolinos i morzem w tle',
       'ved en vei i utkanten av en furuskog, med Torremolinos og havet bak',
       'vid en väg i utkanten av en tallskog, med Torremolinos och havet bortom')
aerial('.media.items[3].alt',
       'con su piscina frente a un pinar, un bloque vecino a la izquierda y colinas detrás',
       'avec sa piscine face à une pinède, un immeuble voisin à gauche et des collines derrière',
       'mit seinem Pool gegenüber einem Pinienwald, einem Nachbarblock links und Hügeln dahinter',
       'бассейн обращён к сосновому лесу, слева соседний корпус, позади холмы',
       'مع مسبحه المواجه لغابة صنوبر، ومبنى مجاور على اليسار، والتلال خلفه',
       'met het zwembad tegenover een dennenbos, een naburig blok links en heuvels erachter',
       'z basenem zwróconym ku lasowi sosnowemu, sąsiednim budynkiem po lewej i wzgórzami w tle',
       'med bassenget mot en furuskog, en nabobygning til venstre og åser bak',
       'med poolen mot en tallskog, ett grannhus till vänster och kullar bakom')
a('.media.items[2].caption',
  'El solar, mirando al mar', 'Le site, côté mer', 'Das Grundstück, Blick zum Meer', 'Участок, вид в сторону моря', 'الموقع باتجاه البحر',
  'Het terrein, richting zee', 'Działka, widok w stronę morza', 'Tomten, mot havet', 'Tomten, mot havet')
a('.media.items[3].caption',
  'El solar, mirando a las colinas', 'Le site, côté collines', 'Das Grundstück, Blick zu den Hügeln', 'Участок, вид в сторону холмов',
  'الموقع باتجاه التلال', 'Het terrein, richting heuvels', 'Działka, widok w stronę wzgórz', 'Tomten, mot åsene', 'Tomten, mot kullarna')
cg('.media.items[4].alt',
   'del spa interior, con tumbonas tras una mampara de vidrio, una piscina climatizada y una pared acristalada hacia el gimnasio',
   'du spa intérieur, avec des transats derrière une paroi de verre, une piscine chauffée et une paroi vitrée donnant sur la salle de sport',
   'des Indoor-Spas mit Liegen hinter einer Glaswand, einem beheizten Pool und einer verglasten Wand zum Fitnessraum',
   'спа в помещении: лежаки за стеклянной перегородкой, подогреваемый бассейн и стеклянная стена в тренажёрный зал',
   'للسبا الداخلي، مع كراسٍ للاستلقاء خلف حاجز زجاجي ومسبح مدفأ وجدار زجاجي يطل على الصالة الرياضية',
   'van de binnenspa, met ligbedden achter een glazen wand, een verwarmd zwembad en een glazen wand naar de fitnessruimte',
   'spa w budynku z leżankami za szklaną ścianką, podgrzewanym basenem i przeszkloną ścianą do siłowni',
   'av innendørs spaet, med liggestoler bak en glassvegg, et oppvarmet basseng og en glassvegg mot treningsrommet',
   'av inomhusspat, med vilstolar bakom en glasvägg, en uppvärmd pool och en glasad vägg mot gymmet')

CGI = {'es': ' generado por ordenador', 'fr': ' générée par ordinateur'}
a('.media.items[6].alt',
  'Salón generado por ordenador con sofá, mesa de comedor y una puerta corredera de vidrio a una terraza cubierta y al mar',
  'Séjour généré par ordinateur avec canapé, table à manger et porte coulissante vitrée ouvrant sur une terrasse couverte et la mer',
  'Computergeneriertes Wohnzimmer mit Sofa, Esstisch und einer Glasschiebetür zu einer überdachten Terrasse und zum Meer',
  'Компьютерная визуализация гостиной с диваном, обеденным столом и раздвижной стеклянной дверью на крытую террасу с видом на море',
  'غرفة معيشة مولَّدة بالحاسوب مع أريكة وطاولة طعام وباب زجاجي منزلق إلى تراس مسقوف والبحر',
  'Computergegenereerde woonkamer met een bank, een eettafel en een glazen schuifdeur naar een overdekt terras en de zee',
  'Wygenerowany komputerowo salon z sofą, stołem jadalnianym i przesuwnymi szklanymi drzwiami na zadaszony taras z widokiem na morze',
  'Datagenerert stue med sofa, spisebord og en skyvedør i glass ut til en overbygd terrasse og havet',
  'Datorgenererat vardagsrum med soffa, matbord och en skjutdörr i glas ut mot en övertäckt terrass och havet')
a('.media.items[7].alt',
  'Cocina abierta generada por ordenador con muebles de madera y gris claro, horno y microondas integrados y una isla efecto mármol junto a la mesa de comedor',
  'Cuisine ouverte générée par ordinateur avec des meubles en bois et gris clair, un four et un micro-ondes encastrés et un îlot effet marbre près de la table à manger',
  'Computergenerierte offene Küche mit Fronten in Holz und Hellgrau, eingebautem Backofen und Mikrowelle und einer Kochinsel in Marmoroptik neben dem Esstisch',
  'Компьютерная визуализация открытой кухни с фасадами под дерево и светло-серыми, встроенными духовкой и микроволновкой и островом под мрамор рядом с обеденным столом',
  'مطبخ مفتوح مولَّد بالحاسوب بخزائن خشبية ورمادية فاتحة وفرن وميكروويف مدمجين وجزيرة بمظهر الرخام بجانب طاولة الطعام',
  'Computergegenereerde open keuken met houten en lichtgrijze kasten, een ingebouwde oven en magnetron en een eiland in marmerlook naast de eettafel',
  'Wygenerowana komputerowo otwarta kuchnia z frontami w drewnie i jasnej szarości, zabudowanym piekarnikiem i mikrofalówką oraz wyspą imitującą marmur obok stołu jadalnianego',
  'Datagenerert åpent kjøkken med skap i tre og lysegrått, integrert stekeovn og mikrobølgeovn og en kjøkkenøy i marmorlook ved spisebordet',
  'Datorgenererat öppet kök med skåp i trä och ljusgrått, inbyggd ugn och mikrovågsugn och en köksö i marmorlook intill matbordet')
a('.media.items[7].caption',
  'Cocina con isla', 'Cuisine avec îlot', 'Küche mit Kochinsel', 'Кухня с островом', 'مطبخ بجزيرة', 'Keuken met eiland',
  'Kuchnia z wyspą', 'Kjøkken med kjøkkenøy', 'Kök med köksö')
a('.media.items[8].alt',
  'Dormitorio generado por ordenador con cama doble, un sillón y una puerta corredera de vidrio a una terraza, con el baño al fondo',
  'Chambre générée par ordinateur avec un lit double, un fauteuil et une porte coulissante vitrée donnant sur une terrasse, avec la salle de bains au fond',
  'Computergeneriertes Schlafzimmer mit Doppelbett, einem Sessel und einer Glasschiebetür zu einer Terrasse, dahinter das Bad',
  'Компьютерная визуализация спальни с двуспальной кроватью, креслом и раздвижной стеклянной дверью на террасу, в глубине ванная',
  'غرفة نوم مولَّدة بالحاسوب مع سرير مزدوج ومقعد وباب زجاجي منزلق إلى تراس، والحمام في الخلف',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een fauteuil en een glazen schuifdeur naar een terras, met de badkamer erachter',
  'Wygenerowana komputerowo sypialnia z podwójnym łóżkiem, fotelem i przesuwnymi szklanymi drzwiami na taras, z łazienką w głębi',
  'Datagenerert soverom med dobbeltseng, en lenestol og en skyvedør i glass ut til en terrasse, med badet innenfor',
  'Datorgenererat sovrum med dubbelsäng, en fåtölj och en skjutdörr i glas ut mot en terrass, med badrummet bortom')
a('.media.items[9].alt',
  'Baño generado por ordenador con mueble de lavabo suspendido, espejo redondo y una ducha a ras de suelo con mampara de vidrio y azulejos efecto mármol',
  'Salle de bains générée par ordinateur avec meuble vasque suspendu, miroir rond et douche à l’italienne avec paroi vitrée et carrelage effet marbre',
  'Computergeneriertes Bad mit wandhängendem Waschtisch, rundem Spiegel und einer bodengleichen Dusche mit Glaswand und Fliesen in Marmoroptik',
  'Компьютерная визуализация ванной с подвесной тумбой, круглым зеркалом и душем без поддона со стеклянной перегородкой и плиткой под мрамор',
  'حمام مولَّد بالحاسوب مع خزانة مغسلة معلقة ومرآة دائرية ودش مفتوح بحاجز زجاجي وبلاط بمظهر الرخام',
  'Computergegenereerde badkamer met een zwevend badmeubel, een ronde spiegel en een inloopdouche met glazen wand en tegels in marmerlook',
  'Wygenerowana komputerowo łazienka z podwieszaną szafką umywalkową, okrągłym lustrem i prysznicem typu walk-in ze szklaną ścianką i płytkami imitującymi marmur',
  'Datagenerert bad med vegghengt servantskap, rundt speil og en walk-in-dusj med glassvegg og fliser i marmorlook',
  'Datorgenererat badrum med vägghängd tvättställsmöbel, rund spegel och en walk-in-dusch med glasvägg och kakel i marmorlook')
a('.media.items[10].alt',
  'Salón abierto generado por ordenador con cocina, mesa de comedor, sillones y un sofá rinconero, con acristalamiento de suelo a techo hacia una terraza y el mar',
  'Séjour ouvert généré par ordinateur avec cuisine, table à manger, fauteuils et canapé d’angle, avec des baies vitrées toute hauteur sur une terrasse et la mer',
  'Computergenerierter offener Wohnbereich mit Küche, Esstisch, Sesseln und einem Ecksofa, mit raumhoher Verglasung zu einer Terrasse und zum Meer',
  'Компьютерная визуализация открытой гостиной с кухней, обеденным столом, креслами и угловым диваном, с остеклением от пола до потолка на террасу и море',
  'غرفة معيشة مفتوحة مولَّدة بالحاسوب مع مطبخ وطاولة طعام ومقاعد وأريكة زاوية، وواجهات زجاجية من الأرض إلى السقف تطل على تراس والبحر',
  'Computergegenereerde open woonkamer met keuken, eettafel, fauteuils en een hoekbank, met kamerhoge beglazing naar een terras en de zee',
  'Wygenerowany komputerowo otwarty salon z kuchnią, stołem jadalnianym, fotelami i narożną sofą, z przeszkleniem od podłogi do sufitu na taras i morze',
  'Datagenerert åpen stue med kjøkken, spisebord, lenestoler og en hjørnesofa, med glass fra gulv til tak ut mot en terrasse og havet',
  'Datorgenererat öppet vardagsrum med kök, matbord, fåtöljer och en hörnsoffa, med glas från golv till tak mot en terrass och havet')
cg('.media.items[11].alt',
   'de una terraza en la azotea bajo una pérgola de madera, con zona de estar, sillones y mesa de comedor, con vistas sobre Torremolinos hasta el mar',
   'd’une terrasse sur le toit sous une pergola en bois, avec un salon, des fauteuils et une table à manger, avec vue sur Torremolinos jusqu’à la mer',
   'einer Dachterrasse unter einer Holzpergola, mit Lounge, Sesseln und Esstisch, mit Blick über Torremolinos zum Meer',
   'террасы на крыше под деревянной перголой, с зоной отдыха, креслами и обеденным столом, с видом на Торремолинос и море',
   'لتراس على السطح تحت عريشة خشبية، مع جلسة ومقاعد وطاولة طعام، بإطلالة على توريمولينوس حتى البحر',
   'van een dakterras onder een houten pergola, met een lounge, fauteuils en een eettafel, met uitzicht over Torremolinos op de zee',
   'tarasu na dachu pod drewnianą pergolą, z częścią wypoczynkową, fotelami i stołem jadalnianym, z widokiem na Torremolinos i morze',
   'av en takterrasse under en trepergola, med sittegruppe, lenestoler og spisebord, med utsikt over Torremolinos til havet',
   'av en takterrass under en träpergola, med loungegrupp, fåtöljer och matbord, med utsikt över Torremolinos mot havet')
a('.media.items[11].caption',
  'Una terraza en la azotea', 'Une terrasse sur le toit', 'Eine Dachterrasse', 'Терраса на крыше', 'تراس على السطح', 'Een dakterras',
  'Taras na dachu', 'En takterrasse', 'En takterrass')
cg('.media.items[12].alt',
   'de una gran terraza cubierta con mesa de comedor, sillones y un sofá rinconero, rodeada de lavanda y pinos',
   'd’une grande terrasse couverte avec une table à manger, des fauteuils et un canapé d’angle, bordée de lavande et de pins',
   'einer großen überdachten Terrasse mit Esstisch, Sesseln und einem Ecksofa, gesäumt von Lavendel und Pinien',
   'большой крытой террасы с обеденным столом, креслами и угловым диваном, окружённой лавандой и соснами',
   'لتراس مسقوف واسع مع طاولة طعام ومقاعد وأريكة زاوية، تحيط به نباتات الخزامى وأشجار الصنوبر',
   'van een groot overdekt terras met een eettafel, fauteuils en een hoekbank, omzoomd door lavendel en dennen',
   'dużego zadaszonego tarasu ze stołem jadalnianym, fotelami i narożną sofą, otoczonego lawendą i sosnami',
   'av en stor overbygd terrasse med spisebord, lenestoler og en hjørnesofa, omgitt av lavendel og furu',
   'av en stor övertäckt terrass med matbord, fåtöljer och en hörnsoffa, omgiven av lavendel och tallar')
a('.media.items[12].caption',
  'Una terraza en planta baja', 'Une terrasse en rez-de-chaussée', 'Eine Terrasse im Erdgeschoss', 'Терраса на первом этаже',
  'تراس في الطابق الأرضي', 'Een terras op de begane grond', 'Taras na parterze', 'En terrasse i første etasje', 'En terrass på bottenvåningen')
a('.media.items[14].alt',
  'Fotografía aérea fechada el 15 de diciembre de 2025: un pinar en primer plano, una parcela desbrozada con maquinaria entre el pinar y una carretera, un bloque en construcción con grúas al otro lado de la carretera y la costa a lo lejos',
  'Photographie aérienne datée du 15 décembre 2025 : une pinède au premier plan, une parcelle dégagée avec des engins entre la pinède et une route, un immeuble en construction avec des grues de l’autre côté de la route et la côte au loin',
  'Luftbild vom 15. Dezember 2025: ein Pinienwald im Vordergrund, ein geräumtes Grundstück mit Baumaschinen zwischen dem Wald und einer Straße, ein Block im Bau mit Kränen jenseits der Straße und die Küste in der Ferne',
  'Аэрофотоснимок от 15 декабря 2025 года: на переднем плане сосновый лес, между лесом и дорогой расчищенный участок с техникой, за дорогой строящийся корпус с кранами, вдали побережье',
  'صورة جوية بتاريخ 15 ديسمبر 2025: غابة صنوبر في المقدمة، وقطعة أرض ممهَّدة عليها آليات بين الغابة وطريق، ومبنى قيد الإنشاء برافعات على الجانب الآخر من الطريق، والساحل في البعيد',
  'Luchtfoto van 15 december 2025: een dennenbos op de voorgrond, een vrijgemaakt perceel met machines tussen het bos en een weg, een blok in aanbouw met kranen aan de overkant van de weg en de kust in de verte',
  'Zdjęcie lotnicze z 15 grudnia 2025 roku: las sosnowy na pierwszym planie, oczyszczona działka z maszynami między lasem a drogą, budynek w budowie z dźwigami po drugiej stronie drogi i wybrzeże w oddali',
  'Flyfoto datert 15. desember 2025: en furuskog i forgrunnen, en ryddet tomt med maskiner mellom skogen og en vei, et bygg under oppføring med kraner på andre siden av veien og kysten i det fjerne',
  'Flygfoto daterat den 15 december 2025: en tallskog i förgrunden, en röjd tomt med maskiner mellan skogen och en väg, ett hus under byggnad med kranar på andra sidan vägen och kusten i fjärran')
a('.media.items[14].caption',
  'El solar desde el aire, 15 de diciembre de 2025', 'Le site vu du ciel, 15 décembre 2025', 'Das Grundstück aus der Luft, 15. Dezember 2025',
  'Участок с воздуха, 15 декабря 2025 года', 'الموقع من الجو، 15 ديسمبر 2025', 'Het terrein vanuit de lucht, 15 december 2025',
  'Działka z lotu ptaka, 15 grudnia 2025 r.', 'Tomten fra luften, 15. desember 2025', 'Tomten från luften, 15 december 2025')

PLAN_ALT = {'es': 'Plano de la vivienda {}', 'fr': 'Plan du logement {}', 'de': 'Grundriss der Wohnung {}', 'ru': 'Планировка квартиры {}',
            'ar': 'مخطط المسكن {}', 'nl': 'Plattegrond van woning {}', 'pl': 'Rzut lokalu {}', 'no': 'Plantegning av bolig {}',
            'sv': 'Planritning för bostad {}'}
PLAN_CAP = {'es': 'Vivienda {}', 'fr': 'Logement {}', 'de': 'Wohnung {}', 'ru': 'Квартира {}', 'ar': 'المسكن {}', 'nl': 'Woning {}',
            'pl': 'Lokal {}', 'no': 'Bolig {}', 'sv': 'Bostad {}'}
for it in proj['media']['items']:
    if it['category'] != 'Floorplans':
        continue
    ref = it['caption'].split(' ', 1)[1]
    put(it['alt'], [PLAN_ALT[l].format(ref) for l in LOCS])
    put(it['caption'], [PLAN_CAP[l].format(ref) for l in LOCS])

# ---- overview, why, architecture ---------------------------------------------------------------

a('.overview.headlineHtml',
  '16 viviendas en la <em>lista de precios</em>', '16 logements sur la <em>liste de prix</em>', '16 Wohnungen auf der <em>Preisliste</em>',
  '16 квартир в <em>прайс-листе</em>', '16 مسكنًا في <em>قائمة الأسعار</em>', '16 woningen op de <em>prijslijst</em>',
  '16 lokali w <em>cenniku</em>', '16 boliger i <em>prislisten</em>', '16 bostäder i <em>prislistan</em>')
a('.overview.copy[0]',
  'El folleto del promotor presenta un edificio de viviendas de dos y tres dormitorios en un solar elevado de Torremolinos, con las zonas comunes orientadas hacia el pinar de enfrente, grandes terrazas y vistas sobre la ciudad y la costa hacia Málaga.',
  'La brochure du promoteur présente un bâtiment de logements de deux et trois chambres sur un terrain surélevé de Torremolinos, avec des espaces communs tournés vers la pinède d’en face, de grandes terrasses et des vues sur la ville et la côte vers Malaga.',
  'Die Broschüre des Bauträgers stellt ein Gebäude mit Wohnungen mit zwei und drei Schlafzimmern auf einem erhöhten Grundstück in Torremolinos vor, die Gemeinschaftsbereiche zum gegenüberliegenden Pinienwald ausgerichtet, mit großen Terrassen und Blick über die Stadt und die Küste in Richtung Málaga.',
  'Брошюра застройщика представляет здание с квартирами с двумя и тремя спальнями на возвышенном участке в Торремолиносе: общие зоны обращены к сосновому лесу напротив, большие террасы, виды на город и побережье в сторону Малаги.',
  'يقدّم كتيّب المطوّر مبنى من مساكن بغرفتي نوم وثلاث غرف نوم على موقع مرتفع في توريمولينوس، مرافقه المشتركة موجهة نحو غابة الصنوبر المقابلة، مع تراسات واسعة وإطلالات على المدينة والساحل باتجاه مالقة.',
  'De brochure van de ontwikkelaar presenteert een gebouw met woningen met twee en drie slaapkamers op een verhoogd terrein in Torremolinos, met de gemeenschappelijke ruimtes gericht op het dennenbos aan de overkant, grote terrassen en uitzicht over de stad en de kust richting Málaga.',
  'Broszura dewelopera przedstawia budynek z mieszkaniami z dwiema i trzema sypialniami na wyniesionej działce w Torremolinos, z częściami wspólnymi zwróconymi ku lasowi sosnowemu naprzeciwko, dużymi tarasami i widokiem na miasto i wybrzeże w stronę Malagi.',
  'Utbyggerens brosjyre presenterer en bygning med boliger med to og tre soverom på en høyt beliggende tomt i Torremolinos, med fellesarealene vendt mot furuskogen på andre siden, store terrasser og utsikt over byen og kysten mot Málaga.',
  'Exploatörens broschyr presenterar en byggnad med bostäder med två och tre sovrum på en upphöjd tomt i Torremolinos, med de gemensamma ytorna vända mot tallskogen mittemot, stora terrasser och utsikt över staden och kusten mot Málaga.')
a('.overview.copy[1]',
  'La lista de precios del 1 de noviembre de 2026 recoge 16 viviendas en seis portales: seis de dos dormitorios, nueve de tres y un ático de tres dormitorios. Cada una incluye una plaza de garaje, dos en tres de ellas, y un trastero. Ningún documento que tengamos indica el número de viviendas del edificio, una licencia, el estado de las obras ni una fecha de entrega.',
  'La liste de prix du 1er novembre 2026 compte 16 logements répartis dans six cages d’escalier : six de deux chambres, neuf de trois et un penthouse de trois chambres. Chacun comprend une place de parking, deux pour trois d’entre eux, et un cellier. Aucun document en notre possession n’indique le nombre de logements du bâtiment, un permis, l’état des travaux ni une date de livraison.',
  'Die Preisliste vom 1. November 2026 führt 16 Wohnungen in sechs Aufgängen: sechs mit zwei Schlafzimmern, neun mit drei und ein Penthouse mit drei Schlafzimmern. Zu jeder gehören ein Stellplatz, bei dreien zwei, und ein Abstellraum. Keines unserer Dokumente nennt die Zahl der Wohnungen im Gebäude, eine Genehmigung, den Stand der Arbeiten oder einen Fertigstellungstermin.',
  'Прайс-лист от 1 ноября 2026 года включает 16 квартир в шести подъездах: шесть с двумя спальнями, девять с тремя и пентхаус с тремя спальнями. К каждой прилагаются машино-место, у трёх из них два, и кладовая. Ни в одном из имеющихся у нас документов не указаны число квартир в здании, разрешение на строительство, стадия работ или дата сдачи.',
  'تضم قائمة الأسعار بتاريخ 1 نوفمبر 2026 ستة عشر مسكنًا في ستة مداخل: ستة بغرفتي نوم، وتسعة بثلاث غرف نوم، وبنتهاوس بثلاث غرف نوم. ولكل منها موقف سيارة، واثنان لثلاثة منها، ومخزن. ولا تذكر أي وثيقة لدينا عدد مساكن المبنى ولا رخصة ولا مرحلة الأعمال ولا موعد التسليم.',
  'De prijslijst van 1 november 2026 noemt 16 woningen in zes portieken: zes met twee slaapkamers, negen met drie en een penthouse met drie slaapkamers. Bij elke woning horen een parkeerplaats, twee bij drie ervan, en een berging. Geen enkel document in ons bezit noemt het aantal woningen in het gebouw, een vergunning, de stand van de werken of een opleverdatum.',
  'Cennik z 1 listopada 2026 roku obejmuje 16 lokali w sześciu klatkach: sześć z dwiema sypialniami, dziewięć z trzema i penthouse z trzema sypialniami. Do każdego należy miejsce parkingowe, w trzech przypadkach dwa, oraz komórka lokatorska. Żaden z posiadanych przez nas dokumentów nie podaje liczby mieszkań w budynku, pozwolenia, etapu prac ani terminu oddania.',
  'Prislisten fra 1. november 2026 har 16 boliger i seks oppganger: seks med to soverom, ni med tre og en toppleilighet med tre soverom. Hver har en parkeringsplass, to for tre av dem, og en bod. Ingen av dokumentene vi har oppgir antall boliger i bygningen, en tillatelse, hvor langt arbeidet har kommet eller en ferdigdato.',
  'Prislistan från den 1 november 2026 har 16 bostäder i sex uppgångar: sex med två sovrum, nio med tre och en takvåning med tre sovrum. Till varje hör en parkeringsplats, två för tre av dem, och ett förråd. Inget dokument vi har anger antalet bostäder i byggnaden, ett tillstånd, hur långt arbetet har kommit eller ett färdigdatum.')
a('.why.copy',
  'Viviendas nuevas de dos y tres dormitorios con terrazas en Torremolinos, cerca del aeropuerto de Málaga, en un solar frente a un pinar, con piscina, spa interior, gimnasio y sala de coworking.',
  'Des logements neufs de deux et trois chambres avec terrasses à Torremolinos, près de l’aéroport de Malaga, sur un terrain face à une pinède, avec piscine, spa intérieur, salle de sport et espace de coworking.',
  'Neue Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Torremolinos, nahe dem Flughafen Málaga, auf einem Grundstück gegenüber einem Pinienwald, mit Pool, Indoor-Spa, Fitnessraum und Coworking-Raum.',
  'Новые квартиры с двумя и тремя спальнями и террасами в Торремолиносе, недалеко от аэропорта Малаги, на участке напротив соснового леса, с бассейном, спа в помещении, тренажёрным залом и коворкингом.',
  'مساكن جديدة بغرفتي نوم وثلاث غرف نوم مع تراسات في توريمولينوس، قرب مطار مالقة، على موقع قبالة غابة صنوبر، مع مسبح وسبا داخلي وصالة رياضية وقاعة للعمل المشترك.',
  'Nieuwe woningen met twee en drie slaapkamers en terrassen in Torremolinos, dicht bij de luchthaven van Málaga, op een terrein tegenover een dennenbos, met zwembad, binnenspa, fitnessruimte en coworkingruimte.',
  'Nowe mieszkania z dwiema i trzema sypialniami oraz tarasami w Torremolinos, blisko lotniska w Maladze, na działce naprzeciw lasu sosnowego, z basenem, spa w budynku, siłownią i salą coworkingową.',
  'Nye boliger med to og tre soverom og terrasser i Torremolinos, nær flyplassen i Málaga, på en tomt rett overfor en furuskog, med basseng, innendørs spa, treningsrom og coworking-rom.',
  'Nya bostäder med två och tre sovrum och terrasser i Torremolinos, nära flygplatsen i Málaga, på en tomt mitt emot en tallskog, med pool, inomhusspa, gym och coworking-rum.')
a('.why.points[0][1]',
  'Compradores que buscan una vivienda nueva de dos o tres dormitorios cerca de Málaga y del aeropuerto, con terraza, plaza de garaje y trastero, para vivir o como segunda residencia.',
  'Les acheteurs qui recherchent un logement neuf de deux ou trois chambres près de Malaga et de l’aéroport, avec terrasse, place de parking et cellier, comme résidence principale ou secondaire.',
  'Käufer, die eine neue Wohnung mit zwei oder drei Schlafzimmern nahe Málaga und dem Flughafen suchen, mit Terrasse, Stellplatz und Abstellraum, zum Wohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужна новая квартира с двумя или тремя спальнями рядом с Малагой и аэропортом, с террасой, машино-местом и кладовой, для жизни или как второй дом.',
  'المشترون الذين يريدون مسكنًا جديدًا بغرفتي نوم أو ثلاث غرف نوم قرب مالقة والمطار، مع تراس وموقف سيارة ومخزن، للسكن أو كمنزل ثانٍ.',
  'Kopers die een nieuwe woning met twee of drie slaapkamers zoeken dicht bij Málaga en de luchthaven, met een terras, een parkeerplaats en een berging, om er te wonen of als tweede woning.',
  'Kupujący, którzy szukają nowego mieszkania z dwiema lub trzema sypialniami blisko Malagi i lotniska, z tarasem, miejscem parkingowym i komórką lokatorską, do zamieszkania lub jako drugi dom.',
  'Kjøpere som vil ha en ny bolig med to eller tre soverom nær Málaga og flyplassen, med terrasse, parkeringsplass og bod, til å bo i eller som feriebolig.',
  'Köpare som vill ha en ny bostad med två eller tre sovrum nära Málaga och flygplatsen, med terrass, parkeringsplats och förråd, att bo i eller som fritidsbostad.')
a('.why.points[1][1]',
  'El folleto describe cada vivienda como un mirador sobre Torremolinos y la costa, con las zonas comunes frente a un pinar y terrazas que dan sombra a las estancias en verano. Las terrazas de la lista de precios van de {N14.42} a {N53.30} {U}.',
  'La brochure décrit chaque logement comme un belvédère sur Torremolinos et la côte, avec les espaces communs face à une pinède et des terrasses qui ombragent les pièces en été. Les terrasses de la liste de prix vont de {N14.42} à {N53.30} {U}.',
  'Die Broschüre beschreibt jede Wohnung als Aussichtsplattform über Torremolinos und die Küste, mit den Gemeinschaftsbereichen gegenüber einem Pinienwald und Terrassen, die die Räume im Sommer beschatten. Die Terrassen auf der Preisliste reichen von {N14.42} bis {N53.30} {U}.',
  'Брошюра описывает каждую квартиру как смотровую площадку над Торремолиносом и побережьем: общие зоны обращены к сосновому лесу, а террасы летом затеняют комнаты. Террасы в прайс-листе — от {N14.42} до {N53.30} {U}.',
  'يصف الكتيّب كل مسكن بأنه منصة مطلة على توريمولينوس والساحل، مع مرافق مشتركة قبالة غابة صنوبر وتراسات تظلّل الغرف صيفًا. وتتراوح مساحة التراسات في قائمة الأسعار بين {N14.42} و{N53.30} {U}.',
  'De brochure beschrijft elke woning als een uitkijkpunt over Torremolinos en de kust, met de gemeenschappelijke ruimtes tegenover een dennenbos en terrassen die de kamers in de zomer schaduw geven. De terrassen op de prijslijst gaan van {N14.42} tot {N53.30} {U}.',
  'Broszura opisuje każde mieszkanie jako punkt widokowy nad Torremolinos i wybrzeżem, z częściami wspólnymi naprzeciw lasu sosnowego i tarasami, które latem ocieniają pokoje. Tarasy w cenniku mają od {N14.42} do {N53.30} {U}.',
  'Brosjyren beskriver hver bolig som en utsiktsplattform over Torremolinos og kysten, med fellesarealene mot en furuskog og terrasser som gir rommene skygge om sommeren. Terrassene i prislisten er fra {N14.42} til {N53.30} {U}.',
  'Broschyren beskriver varje bostad som en utsiktsplats över Torremolinos och kusten, med de gemensamma ytorna mot en tallskog och terrasser som ger rummen skugga på sommaren. Terrasserna i prislistan är från {N14.42} till {N53.30} {U}.')
a('.why.points[2][1]',
  'La lista incluye un ático, 2-AT-B, con tres dormitorios y {N50.29} {U} de terraza, que su plano muestra como dos solárium, uno en cada extremo, por {E802000} con dos plazas de garaje.',
  'La liste comprend un penthouse, 2-AT-B, avec trois chambres et {N50.29} {U} de terrasse, que son plan présente comme deux solariums, un à chaque extrémité, pour {E802000} avec deux places de parking.',
  'Die Liste führt ein Penthouse, 2-AT-B, mit drei Schlafzimmern und {N50.29} {U} Terrasse, die sein Grundriss als zwei Solarien an beiden Enden zeigt, für {E802000} mit zwei Stellplätzen.',
  'В списке один пентхаус, 2-AT-B, с тремя спальнями и террасой {N50.29} {U}, которую его план показывает как два солярия по краям, за {E802000} с двумя машино-местами.',
  'تتضمن القائمة بنتهاوس واحدًا، 2-AT-B، بثلاث غرف نوم وتراس مساحته {N50.29} {U}، يُظهره مخططه سولاريومين، واحدًا في كل طرف، بسعر {E802000} مع موقفي سيارة.',
  'De lijst noemt één penthouse, 2-AT-B, met drie slaapkamers en {N50.29} {U} terras, dat de plattegrond toont als twee solariums, één aan elk uiteinde, voor {E802000} met twee parkeerplaatsen.',
  'Cennik obejmuje jeden penthouse, 2-AT-B, z trzema sypialniami i {N50.29} {U} tarasu, który rzut pokazuje jako dwa solaria, po jednym na każdym końcu, za {E802000} z dwoma miejscami parkingowymi.',
  'Listen har én toppleilighet, 2-AT-B, med tre soverom og {N50.29} {U} terrasse, som tegningen viser som to solterrasser, én i hver ende, for {E802000} med to parkeringsplasser.',
  'Listan har en takvåning, 2-AT-B, med tre sovrum och {N50.29} {U} terrass, som ritningen visar som två solterrasser, en i varje ände, för {E802000} med två parkeringsplatser.')
a('.why.points[3][1]',
  'La lista de precios dice que es meramente informativa, que no tiene valor contractual y que los precios pueden variar según el avance del proyecto y la disponibilidad. Confirmamos precio y disponibilidad antes de cualquier reserva.',
  'La liste de prix indique qu’elle est purement informative, qu’elle n’a aucune valeur contractuelle et que les prix peuvent varier selon l’avancement du projet et la disponibilité. Nous confirmons prix et disponibilité avant toute réservation.',
  'Die Preisliste gibt an, dass sie nur der Information dient, keinen Vertragswert hat und die Preise je nach Projektfortschritt und Verfügbarkeit schwanken können. Wir bestätigen Preis und Verfügbarkeit vor jeder Reservierung.',
  'В прайс-листе сказано, что он носит лишь информационный характер, не имеет договорной силы, а цены могут меняться в зависимости от хода проекта и наличия. Мы подтверждаем цену и наличие до любого бронирования.',
  'تذكر قائمة الأسعار أنها للعلم فقط، وليس لها أي قيمة تعاقدية، وأن الأسعار قد تتغير بحسب تقدّم المشروع والتوفر. نؤكد السعر والتوفر قبل أي حجز.',
  'De prijslijst zegt dat ze alleen ter informatie dient, geen contractuele waarde heeft en dat de prijzen kunnen variëren naargelang de voortgang van het project en de beschikbaarheid. Wij bevestigen prijs en beschikbaarheid vóór elke reservering.',
  'Cennik zastrzega, że ma charakter wyłącznie informacyjny, nie ma wartości umownej, a ceny mogą się zmieniać w zależności od postępu projektu i dostępności. Cenę i dostępność potwierdzamy przed każdą rezerwacją.',
  'Prislisten sier at den bare er til informasjon, ikke har kontraktsverdi og at prisene kan variere med fremdriften i prosjektet og tilgjengeligheten. Vi bekrefter pris og tilgjengelighet før enhver reservasjon.',
  'Prislistan anger att den endast är informativ, saknar avtalsvärde och att priserna kan variera med projektets framsteg och tillgängligheten. Vi bekräftar pris och tillgänglighet före varje bokning.')
a('.architecture.headlineHtml',
  'Terrazas en capas, <em>un pinar enfrente</em>', 'Des terrasses en strates, <em>une pinède en face</em>', 'Terrassen in Schichten, <em>ein Pinienwald gegenüber</em>',
  'Террасы ярусами, <em>сосновый лес напротив</em>', 'تراسات متدرجة، <em>وغابة صنوبر في المقابل</em>', 'Gelaagde terrassen, <em>een dennenbos ertegenover</em>',
  'Tarasy warstwami, <em>las sosnowy naprzeciwko</em>', 'Terrasser i lag, <em>en furuskog rett overfor</em>', 'Terrasser i skikt, <em>en tallskog mittemot</em>')
a('.architecture.copy[0]',
  'El folleto dice que los arquitectos aprovecharon la posición elevada del solar para plantear las viviendas como una sucesión de capas horizontales, cada una un mirador, con las zonas comunes orientadas al pinar de enfrente. Las grandes terrazas funcionan como parasoles: más protección del sol en verano y más luz en invierno.',
  'La brochure indique que les architectes ont tiré parti de la position surélevée du terrain pour concevoir les logements comme une succession de strates horizontales, chacune un belvédère, avec les espaces communs tournés vers la pinède d’en face. Les grandes terrasses font office de pare-soleil : plus de protection contre le soleil en été et plus de lumière en hiver.',
  'Laut Broschüre nutzten die Architekten die erhöhte Lage des Grundstücks, um die Wohnungen als Abfolge horizontaler Schichten zu gestalten, jede eine Aussichtsplattform, mit den Gemeinschaftsbereichen zum gegenüberliegenden Pinienwald. Die großen Terrassen wirken als Sonnenschutz: mehr Schutz vor der Sonne im Sommer und mehr Licht im Winter.',
  'В брошюре сказано, что архитекторы использовали возвышенное положение участка, чтобы выстроить квартиры как последовательность горизонтальных ярусов, каждый из которых — смотровая площадка, а общие зоны обращены к сосновому лесу напротив. Большие террасы работают как солнцезащита: больше тени летом и больше света зимой.',
  'يذكر الكتيّب أن المعماريين استفادوا من الموقع المرتفع للأرض لتصميم المساكن كسلسلة من الطبقات الأفقية، كل منها منصة مطلة، مع توجيه المرافق المشتركة نحو غابة الصنوبر المقابلة. وتعمل التراسات الواسعة كمظلات: حماية أكبر من الشمس صيفًا وضوء أكثر شتاءً.',
  'Volgens de brochure gebruikten de architecten de verhoogde ligging van het terrein om de woningen te ontwerpen als een opeenvolging van horizontale lagen, elk een uitkijkpunt, met de gemeenschappelijke ruimtes gericht op het dennenbos aan de overkant. De grote terrassen werken als zonwering: meer bescherming tegen de zon in de zomer en meer licht in de winter.',
  'Broszura podaje, że architekci wykorzystali wyniesione położenie działki, by zaprojektować mieszkania jako następujące po sobie poziome warstwy, każda będąca punktem widokowym, z częściami wspólnymi zwróconymi ku lasowi sosnowemu naprzeciwko. Duże tarasy działają jak osłony przeciwsłoneczne: więcej ochrony przed słońcem latem i więcej światła zimą.',
  'Brosjyren sier at arkitektene brukte tomtens høye beliggenhet til å utforme boligene som en rekke horisontale lag, hvert av dem en utsiktsplattform, med fellesarealene vendt mot furuskogen på andre siden. De store terrassene fungerer som solskjerming: mer beskyttelse mot solen om sommeren og mer lys om vinteren.',
  'Enligt broschyren utnyttjade arkitekterna tomtens upphöjda läge för att utforma bostäderna som en följd av horisontella skikt, vart och ett en utsiktsplats, med de gemensamma ytorna vända mot tallskogen mittemot. De stora terrasserna fungerar som solskydd: mer skydd mot solen på sommaren och mer ljus på vintern.')
a('.architecture.copy[1]',
  'En las imágenes generadas por ordenador del promotor, el edificio tiene largos forjados curvos de terraza, techos de madera, barandillas de vidrio y una pérgola en la planta superior, sobre un zócalo de piedra encima de la piscina. La lista de precios numera las viviendas por portal, del 1 al 6, de la planta baja a la cuarta, con un ático encima.',
  'Dans les images générées par ordinateur du promoteur, le bâtiment présente de longues dalles de terrasse courbes, des sous-faces en bois, des garde-corps en verre et une pergola au dernier étage, sur un socle de pierre au-dessus de la piscine. La liste de prix numérote les logements par cage d’escalier, de 1 à 6, du rez-de-chaussée au quatrième étage, avec un penthouse au-dessus.',
  'In den computergenerierten Bildern des Bauträgers hat das Gebäude lange, geschwungene Terrassenplatten, Holzuntersichten, Glasbrüstungen und eine Pergola im obersten Geschoss, auf einem Steinsockel über dem Pool. Die Preisliste nummeriert die Wohnungen nach Aufgang, 1 bis 6, vom Erdgeschoss bis zum vierten Obergeschoss, mit einem Penthouse darüber.',
  'На компьютерных визуализациях застройщика у здания длинные изогнутые плиты террас, деревянная подшивка, стеклянные ограждения и пергола на верхнем этаже, а стоит оно на каменном цоколе над бассейном. Прайс-лист нумерует квартиры по подъездам, с 1 по 6, с первого этажа по пятый, с пентхаусом наверху.',
  'في الصور المولَّدة بالحاسوب الصادرة عن المطوّر، للمبنى بلاطات تراس طويلة منحنية وأسقف خشبية وحواجز زجاجية وعريشة في الطابق العلوي، فوق قاعدة حجرية تعلو المسبح. وترقّم قائمة الأسعار المساكن حسب المدخل، من 1 إلى 6، من الطابق الأرضي حتى الطابق الرابع، وفوقها بنتهاوس.',
  'Op de computergegenereerde beelden van de ontwikkelaar heeft het gebouw lange, gebogen terrasplaten, houten plafonds, glazen balustrades en een pergola op de bovenste verdieping, op een stenen sokkel boven het zwembad. De prijslijst nummert de woningen per portiek, 1 tot 6, van de begane grond tot de vierde verdieping, met een penthouse erboven.',
  'Na wygenerowanych komputerowo obrazach dewelopera budynek ma długie, zakrzywione płyty tarasów, drewniane podsufitki, szklane balustrady i pergolę na najwyższym piętrze, na kamiennym cokole nad basenem. Cennik numeruje lokale według klatek, od 1 do 6, od parteru do czwartego piętra, z penthouse’em na górze.',
  'På utbyggerens datagenererte bilder har bygningen lange, buede terrasseplater, trehimlinger, glassrekkverk og en pergola i øverste etasje, på en steinsokkel over bassenget. Prislisten nummererer boligene etter oppgang, 1 til 6, fra første til femte etasje, med en toppleilighet over.',
  'På exploatörens datorgenererade bilder har byggnaden långa, böjda terrassplattor, trätak, glasräcken och en pergola på översta våningen, på en stensockel ovanför poolen. Prislistan numrerar bostäderna efter uppgång, 1 till 6, från bottenvåningen till fjärde våningen, med en takvåning ovanpå.')
a('.architecture.highlights[0][1]',
  'Una fachada de diseño que combina tonos y texturas complementarios, con revestimientos continuos en tonos cálidos y un aislamiento térmico y acústico conforme al Código Técnico de la Edificación.',
  'Une façade signature associant des tons et des textures complémentaires, avec des enduits continus aux teintes chaudes et une isolation thermique et acoustique conforme au Code technique de la construction espagnol.',
  'Eine Designfassade, die sich ergänzende Farbtöne und Texturen verbindet, mit durchgehenden Beschichtungen in warmen Tönen und einer Wärme- und Schalldämmung nach der spanischen Bauordnung.',
  'Авторский фасад, сочетающий дополняющие друг друга оттенки и фактуры, со сплошной отделкой в тёплых тонах и тепло- и звукоизоляцией в соответствии с испанскими строительными нормами.',
  'واجهة مميزة تجمع بين ألوان وملمس متكاملين، مع طلاءات متصلة بألوان دافئة وعزل حراري وصوتي يلبّي متطلبات قانون البناء الإسباني.',
  'Een signatuurgevel die elkaar aanvullende tinten en texturen combineert, met doorlopende afwerkingen in warme tinten en thermische en akoestische isolatie volgens de Spaanse bouwvoorschriften.',
  'Autorska elewacja łącząca uzupełniające się odcienie i faktury, z ciągłymi powłokami w ciepłych barwach oraz izolacją termiczną i akustyczną zgodną z hiszpańskimi przepisami budowlanymi.',
  'En signaturfasade som kombinerer utfyllende toner og teksturer, med sammenhengende belegg i varme farger og varme- og lydisolasjon etter spanske byggeforskrifter.',
  'En signaturfasad som kombinerar kompletterande toner och texturer, med sammanhängande beläggningar i varma färger och värme- och ljudisolering enligt spanska byggregler.')

# ---- quality specification ---------------------------------------------------------------------

a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor, versión del 22 de diciembre de 2025. Dice que es meramente orientativa, que el promotor puede introducir cambios por motivos técnicos, comerciales, jurídicos, de disponibilidad de materiales o de diseño, y que cualquier cambio se hará con materiales de calidad equivalente.',
  'Source : le descriptif de qualité du promoteur, version du 22 décembre 2025. Il précise qu’il est donné à titre indicatif, que le promoteur peut apporter des modifications pour des raisons techniques, commerciales, juridiques, de disponibilité des matériaux ou de conception, et que toute modification se fera avec des matériaux de qualité équivalente.',
  'Quelle: die Bau- und Ausstattungsbeschreibung des Bauträgers, Fassung vom 22. Dezember 2025. Sie gibt an, nur zur Orientierung zu dienen, dass der Bauträger aus technischen, kommerziellen, rechtlichen, gestalterischen Gründen oder wegen der Verfügbarkeit von Materialien Änderungen vornehmen kann und dass jede Änderung mit Materialien gleichwertiger Qualität erfolgt.',
  'Источник: спецификация качества застройщика в редакции от 22 декабря 2025 года. В ней сказано, что она носит ориентировочный характер, что застройщик может вносить изменения по техническим, коммерческим, юридическим причинам, из-за наличия материалов или по соображениям дизайна и что любые замены будут выполнены материалами сопоставимого качества.',
  'المصدر: مواصفات الجودة الصادرة عن المطوّر، نسخة 22 ديسمبر 2025. وتذكر أنها للاسترشاد فقط، وأن للمطوّر إدخال تعديلات لأسباب فنية أو تجارية أو قانونية أو تتعلق بتوفر المواد أو بالتصميم، وأن أي تعديل سيتم بمواد ذات جودة مماثلة.',
  'Bron: de kwaliteitsspecificatie van de ontwikkelaar, versie van 22 december 2025. Daarin staat dat ze slechts indicatief is, dat de ontwikkelaar wijzigingen kan aanbrengen om technische, commerciële, juridische of ontwerpredenen of vanwege de beschikbaarheid van materialen, en dat elke wijziging met materialen van vergelijkbare kwaliteit gebeurt.',
  'Źródło: specyfikacja jakości dewelopera w wersji z 22 grudnia 2025 roku. Zastrzega, że ma charakter orientacyjny, że deweloper może wprowadzać zmiany z przyczyn technicznych, handlowych, prawnych, projektowych lub z powodu dostępności materiałów oraz że każda zmiana zostanie wykonana z materiałów porównywalnej jakości.',
  'Kilde: utbyggerens kvalitetsspesifikasjon, versjon av 22. desember 2025. Den sier at den bare er veiledende, at utbyggeren kan gjøre endringer av tekniske, kommersielle, juridiske eller designmessige grunner eller på grunn av tilgang på materialer, og at enhver endring gjøres med materialer av tilsvarende kvalitet.',
  'Källa: exploatörens kvalitetsspecifikation, version av den 22 december 2025. Den anger att den bara är vägledande, att exploatören kan göra ändringar av tekniska, kommersiella, juridiska eller designmässiga skäl eller på grund av tillgången på material, och att varje ändring görs med material av jämförbar kvalitet.')
a('.qualitySpecs.groups[0].items[0]',
  'Suelo interior de SPC de gama alta en gran formato (1800 x 230 mm), un material resistente al agua, y gres porcelánico en los baños y las terrazas.',
  'Revêtement de sol intérieur en SPC haut de gamme grand format (1800 x 230 mm), un matériau résistant à l’eau, et carrelage en grès cérame dans les salles de bains et sur les terrasses.',
  'Innenboden aus hochwertigem SPC im Großformat (1800 x 230 mm), einem wasserbeständigen Material, und Feinsteinzeug in den Bädern und auf den Terrassen.',
  'Напольное покрытие из SPC премиум-класса крупного формата (1800 x 230 мм), влагостойкого материала, и керамогранит в ванных и на террасах.',
  'أرضيات داخلية من SPC فاخر بمقاس كبير (1800 x 230 مم)، وهي مادة مقاومة للماء، وبلاط بورسلان في الحمامات والتراسات.',
  'Binnenvloeren in hoogwaardig SPC in groot formaat (1800 x 230 mm), een waterbestendig materiaal, en porseleinen tegels in de badkamers en op de terrassen.',
  'Podłogi wewnętrzne z wysokiej klasy SPC w dużym formacie (1800 x 230 mm), materiału odpornego na wodę, oraz gres porcelanowy w łazienkach i na tarasach.',
  'Innvendig gulv i SPC av høy kvalitet i stort format (1800 x 230 mm), et vannbestandig materiale, og porselensfliser på badene og terrassene.',
  'Invändigt golv i SPC av hög kvalitet i stort format (1800 x 230 mm), ett vattentåligt material, och porslinsklinker i badrummen och på terrasserna.')
a('.qualitySpecs.groups[0].items[1]',
  'Pintura lisa en las paredes interiores y revestimiento cerámico de gran formato en las zonas húmedas de los baños.',
  'Peinture lisse sur les murs intérieurs et carrelage céramique grand format sur les zones humides des salles de bains.',
  'Glatter Anstrich an den Innenwänden und großformatige Keramikfliesen in den Nassbereichen der Bäder.',
  'Гладкая окраска внутренних стен и крупноформатная керамическая плитка во влажных зонах ванных комнат.',
  'دهان أملس على الجدران الداخلية وبلاط سيراميك كبير المقاس في المناطق الرطبة من الحمامات.',
  'Gladde verf op de binnenmuren en grootformaat keramische tegels op de natte zones van de badkamers.',
  'Gładka farba na ścianach wewnętrznych i wielkoformatowe płytki ceramiczne w strefach mokrych łazienek.',
  'Glatt maling på innerveggene og storformat keramiske fliser i våtsonene på badene.',
  'Slät målning på innerväggarna och storformatigt keramiskt kakel i badrummens våtzoner.')
a('.qualitySpecs.groups[1].items[0]',
  'Cocina amueblada con muebles altos y bajos que combinan madera, tonos claros y encimeras resistentes, en una de dos opciones de diseño, con isla o península como opción donde la distribución lo permita.',
  'Une cuisine équipée de meubles hauts et bas associant bois, tons clairs et plans de travail résistants, dans l’une de deux options de design, avec un îlot ou une péninsule en option lorsque l’agencement le permet.',
  'Eine Einbauküche mit Ober- und Unterschränken in einer Kombination aus Holz, hellen Tönen und strapazierfähigen Arbeitsplatten, in einer von zwei Designvarianten, mit Kochinsel oder Halbinsel als Option, wo der Grundriss es zulässt.',
  'Встроенная кухня с верхними и нижними шкафами, сочетающими дерево, светлые тона и прочные столешницы, в одном из двух вариантов дизайна, с островом или полуостровом в качестве опции там, где позволяет планировка.',
  'مطبخ مجهز بخزائن علوية وسفلية تجمع بين الخشب والألوان الفاتحة وأسطح العمل المتينة، بأحد خيارين للتصميم، مع جزيرة أو شبه جزيرة كخيار حيث يسمح التصميم.',
  'Een ingerichte keuken met boven- en onderkasten in een combinatie van hout, lichte tinten en duurzame werkbladen, in een van twee ontwerpopties, met een eiland of schiereiland als optie waar de indeling het toelaat.',
  'Kuchnia w zabudowie z szafkami górnymi i dolnymi łączącymi drewno, jasne odcienie i trwałe blaty, w jednym z dwóch wariantów wzorniczych, z wyspą lub półwyspem jako opcją tam, gdzie pozwala na to układ.',
  'Et innredet kjøkken med over- og underskap som kombinerer tre, lyse toner og slitesterke benkeplater, i ett av to designvalg, med kjøkkenøy eller halvøy som tilvalg der planløsningen tillater det.',
  'Ett inrett kök med över- och underskåp som kombinerar trä, ljusa toner och tåliga bänkskivor, i ett av två designalternativ, med köksö eller halvö som tillval där planlösningen tillåter det.')
a('.qualitySpecs.groups[2].items[0]',
  'Inodoros de diseño con cisterna de doble descarga, platos de ducha extraplanos, mampara en el baño principal y mueble de lavabo con cajonera, lavabo sobre encimera y espejo de diseño.',
  'Toilettes design à double chasse, receveurs de douche extra-plats, paroi de douche dans la salle de bains principale et meuble vasque à tiroirs avec vasque à poser et miroir design.',
  'Design-WCs mit Zweimengenspülung, flache Duschtassen, eine Duschabtrennung im Hauptbad und ein Waschtischunterschrank mit Schubladen, Aufsatzwaschbecken und Designspiegel.',
  'Дизайнерские унитазы с двухрежимным смывом, низкие душевые поддоны, душевая перегородка в главной ванной и тумба с ящиками, накладной раковиной и дизайнерским зеркалом.',
  'مراحيض بتصميم مميز بنظام تدفق مزدوج، وقواعد دش منخفضة، وحاجز دش في الحمام الرئيسي، وخزانة مغسلة بأدراج مع حوض علوي ومرآة بتصميم مميز.',
  'Designtoiletten met dubbele spoeling, vlakke douchebakken, een douchewand in de hoofdbadkamer en een badmeubel met lades, een opzetwastafel en een designspiegel.',
  'Designerskie toalety ze spłuczką dwudzielną, płaskie brodziki, kabina prysznicowa w głównej łazience oraz szafka z szufladami, umywalką nablatową i designerskim lustrem.',
  'Designtoaletter med dobbel skylling, lave dusjkar, dusjvegg på hovedbadet og et servantskap med skuffer, en servant på benkeplate og et designspeil.',
  'Designtoaletter med dubbelspolning, låga duschkar, duschvägg i huvudbadrummet och en tvättställsmöbel med lådor, ett tvättställ på bänkskiva och en designspegel.')
a('.qualitySpecs.groups[2].items[1]',
  'Grifería monomando en los lavabos y termostática en las duchas.',
  'Robinetterie mitigeur sur les lavabos et thermostatique dans les douches.',
  'Einhebelmischer an den Waschbecken und Thermostatarmaturen in den Duschen.',
  'Однорычажные смесители на раковинах и термостатические в душевых.',
  'خلاطات بذراع واحدة على المغاسل وخلاطات حرارية في الدشات.',
  'Eenhendelmengkranen op de wastafels en thermostaatkranen in de douches.',
  'Baterie jednouchwytowe przy umywalkach i termostatyczne pod prysznicami.',
  'Ettgrepsbatterier på servantene og termostatbatterier i dusjene.',
  'Engreppsblandare vid tvättställen och termostatblandare i duscharna.')
a('.qualitySpecs.groups[4].items[0]',
  'Sistema de aerotermia de alta eficiencia para el agua caliente y la climatización, con distribución por conductos en el falso techo.',
  'Un système d’aérothermie à haut rendement pour l’eau chaude et la climatisation, avec distribution par gaines dans le faux plafond.',
  'Eine effiziente Luft-Wasser-Wärmepumpe für Warmwasser, Heizung und Kühlung, mit Luftverteilung über Kanäle in der abgehängten Decke.',
  'Энергоэффективный тепловой насос «воздух — вода» для горячего водоснабжения, отопления и охлаждения с воздуховодами в подвесном потолке.',
  'نظام تدفئة وتبريد هوائي حراري عالي الكفاءة للمياه الساخنة والتكييف، مع توزيع عبر مجارٍ في السقف المعلق.',
  'Een energiezuinige lucht-waterwarmtepomp voor warm water, verwarming en koeling, met kanalen in het verlaagde plafond.',
  'Energooszczędna pompa ciepła powietrze–woda do ciepłej wody, ogrzewania i chłodzenia, z kanałami w suficie podwieszanym.',
  'En energieffektiv luft-til-vann-varmepumpe for varmtvann, oppvarming og kjøling, med kanaler i nedforet himling.',
  'En energieffektiv luft-vattenvärmepump för varmvatten, värme och kyla, med kanaler i undertaket.')
a('.qualitySpecs.groups[5].items[0]',
  'Una piscina comunitaria exterior con cloración salina, jardín y solárium, y un spa interior con piscina climatizada, sauna y circuito de duchas, conectado con el gimnasio y los vestuarios.',
  'Une piscine commune extérieure à chloration au sel, avec jardin et solarium, et un spa intérieur avec piscine chauffée, sauna et parcours de douches, relié à la salle de sport et aux vestiaires.',
  'Ein gemeinschaftlicher Außenpool mit Salzelektrolyse, Garten und Sonnenterrasse sowie ein Indoor-Spa mit beheiztem Pool, Sauna und Duschparcours, verbunden mit dem Fitnessraum und den Umkleiden.',
  'Общий открытый бассейн с солевым хлорированием, садом и солярием, а также спа в помещении с подогреваемым бассейном, сауной и душевым контуром, соединённое с тренажёрным залом и раздевалками.',
  'مسبح مشترك خارجي بنظام كلورة ملحية مع حديقة ومنطقة تشمّس، وسبا داخلي بمسبح مدفأ وساونا ومسار دشات، متصل بالصالة الرياضية وغرف تبديل الملابس.',
  'Een gemeenschappelijk buitenzwembad met zoutchlorering, een tuin en een zonneterras, en een binnenspa met een verwarmd zwembad, een sauna en een douchecircuit, verbonden met de fitnessruimte en de kleedkamers.',
  'Wspólny basen zewnętrzny z chlorowaniem solnym, ogrodem i strefą do opalania oraz spa w budynku z podgrzewanym basenem, sauną i ścieżką prysznicową, połączone z siłownią i szatniami.',
  'Et felles utendørs basseng med saltklorering, hage og soltak, og et innendørs spa med oppvarmet basseng, badstue og dusjløype, forbundet med treningsrommet og garderobene.',
  'En gemensam utomhuspool med saltklorering, trädgård och soldäck, och ett inomhusspa med uppvärmd pool, bastu och duschslinga, förbundet med gymmet och omklädningsrummen.')
a('.qualitySpecs.groups[5].items[1]',
  'Un gimnasio totalmente equipado, un espacio de coworking con office y aseos para todos los residentes, jardines con vegetación mediterránea y puerta de garaje motorizada con mando a distancia.',
  'Une salle de sport entièrement équipée, un espace de coworking avec kitchenette et sanitaires pour tous les résidents, des jardins paysagers à la végétation méditerranéenne et une porte de garage motorisée avec télécommande.',
  'Ein voll ausgestatteter Fitnessraum, ein Coworking-Bereich mit Teeküche und Toiletten für alle Bewohner, angelegte Gärten mit mediterraner Bepflanzung und ein motorisiertes Garagentor mit Fernbedienung.',
  'Полностью оборудованный тренажёрный зал, коворкинг с мини-кухней и туалетами для всех жителей, ландшафтные сады со средиземноморскими растениями и моторизованные ворота гаража с пультом.',
  'صالة رياضية مجهزة بالكامل، ومساحة للعمل المشترك مع مطبخ صغير ودورات مياه لجميع السكان، وحدائق منسّقة بنباتات متوسطية، وباب مرآب آلي بجهاز تحكم عن بُعد.',
  'Een volledig uitgeruste fitnessruimte, een coworkingruimte met kitchenette en toiletten voor alle bewoners, aangelegde tuinen met mediterrane beplanting en een gemotoriseerde garagedeur met afstandsbediening.',
  'W pełni wyposażona siłownia, przestrzeń coworkingowa z aneksem kuchennym i toaletami dla wszystkich mieszkańców, ogrody z roślinnością śródziemnomorską i zmotoryzowana brama garażowa z pilotem.',
  'Et fullt utstyrt treningsrom, et coworking-område med tekjøkken og toaletter for alle beboerne, anlagte hager med middelhavsbeplantning og en motorisert garasjeport med fjernkontroll.',
  'Ett fullt utrustat gym, ett coworking-utrymme med pentry och toaletter för alla boende, anlagda trädgårdar med medelhavsväxter och en motoriserad garageport med fjärrkontroll.')

# ---- residences ---------------------------------------------------------------------------------

a('.residences.copy',
  'Las 16 viviendas de la lista de precios figuran abajo con su superficie interior y su terraza. Todas tienen dos baños. Los documentos no dan otro nombre a ningún tipo de vivienda.',
  'Les 16 logements de la liste de prix figurent ci-dessous avec leur surface intérieure et leur terrasse. Tous ont deux salles de bains. Les documents ne donnent aucun autre nom à un type de logement.',
  'Die 16 Wohnungen der Preisliste sind unten mit ihrer Innenfläche und ihrer Terrasse aufgeführt. Jede hat zwei Bäder. Die Unterlagen nennen keinen anderen Namen für einen Wohnungstyp.',
  'Ниже приведены 16 квартир из прайс-листа с внутренней площадью и террасой. В каждой две ванные комнаты. Иных названий типов квартир в документах нет.',
  'ترد أدناه المساكن الستة عشر في قائمة الأسعار مع مساحتها الداخلية وتراسها. ولكل منها حمامان. ولا تعطي الوثائق أي اسم آخر لنوع المسكن.',
  'De 16 woningen van de prijslijst staan hieronder met hun binnenoppervlak en hun terras. Elke woning heeft twee badkamers. De documenten geven geen andere naam voor een woningtype.',
  'Poniżej wymieniono 16 lokali z cennika wraz z powierzchnią wewnętrzną i tarasem. Każdy ma dwie łazienki. Dokumenty nie podają innej nazwy żadnego typu mieszkania.',
  'De 16 boligene i prislisten er oppført nedenfor med innvendig areal og terrasse. Alle har to bad. Dokumentene gir ingen annen betegnelse på en boligtype.',
  'De 16 bostäderna i prislistan anges nedan med invändig yta och terrass. Alla har två badrum. Dokumenten ger inget annat namn på någon bostadstyp.')
a('.residences.items[0].points[0]',
  '6 de las 16 tienen dos dormitorios y dos baños, con {N65.05} a {N78.70} {U} interiores, de {E425000} a {E485000}.',
  '6 des 16 ont deux chambres et deux salles de bains, avec {N65.05} à {N78.70} {U} intérieurs, de {E425000} à {E485000}.',
  '6 der 16 haben zwei Schlafzimmer und zwei Bäder, mit {N65.05} bis {N78.70} {U} Innenfläche, von {E425000} bis {E485000}.',
  '6 из 16 имеют две спальни и две ванные, внутренняя площадь от {N65.05} до {N78.70} {U}, цена от {E425000} до {E485000}.',
  '6 من أصل 16 بغرفتي نوم وحمامين، بمساحة داخلية من {N65.05} إلى {N78.70} {U}، من {E425000} إلى {E485000}.',
  '6 van de 16 hebben twee slaapkamers en twee badkamers, met {N65.05} tot {N78.70} {U} binnenoppervlak, van {E425000} tot {E485000}.',
  '6 z 16 ma dwie sypialnie i dwie łazienki, od {N65.05} do {N78.70} {U} powierzchni wewnętrznej, w cenie od {E425000} do {E485000}.',
  '6 av de 16 har to soverom og to bad, med {N65.05} til {N78.70} {U} innvendig, fra {E425000} til {E485000}.',
  '6 av de 16 har två sovrum och två badrum, med {N65.05} till {N78.70} {U} invändigt, från {E425000} till {E485000}.')
a('.residences.items[0].points[1]',
  'Dos están en planta baja, dos en la primera, una en la segunda y una en la cuarta. Sus terrazas van de {N14.42} {U} (1-4-D) a {N23.14} {U} (3-1-B).',
  'Deux sont au rez-de-chaussée, deux au premier étage, un au deuxième et un au quatrième. Leurs terrasses vont de {N14.42} {U} (1-4-D) à {N23.14} {U} (3-1-B).',
  'Zwei liegen im Erdgeschoss, zwei im ersten, eine im zweiten und eine im vierten Obergeschoss. Ihre Terrassen reichen von {N14.42} {U} (1-4-D) bis {N23.14} {U} (3-1-B).',
  'Две на первом этаже, две на втором, одна на третьем и одна на пятом. Их террасы — от {N14.42} {U} (1-4-D) до {N23.14} {U} (3-1-B).',
  'اثنان في الطابق الأرضي، واثنان في الأول، وواحد في الثاني، وواحد في الرابع. وتتراوح تراساتها بين {N14.42} {U} (1-4-D) و{N23.14} {U} (3-1-B).',
  'Twee liggen op de begane grond, twee op de eerste, een op de tweede en een op de vierde verdieping. Hun terrassen gaan van {N14.42} {U} (1-4-D) tot {N23.14} {U} (3-1-B).',
  'Dwa są na parterze, dwa na pierwszym piętrze, jeden na drugim i jeden na czwartym. Ich tarasy mają od {N14.42} {U} (1-4-D) do {N23.14} {U} (3-1-B).',
  'To ligger i første etasje, to i andre, én i tredje og én i femte. Terrassene er fra {N14.42} {U} (1-4-D) til {N23.14} {U} (3-1-B).',
  'Två ligger på bottenvåningen, två på första, en på andra och en på fjärde våningen. Terrasserna är från {N14.42} {U} (1-4-D) till {N23.14} {U} (3-1-B).')
a('.residences.items[1].name',
  'Apartamentos de tres dormitorios y el ático', 'Appartements de trois chambres et le penthouse', 'Wohnungen mit drei Schlafzimmern und das Penthouse',
  'Квартиры с тремя спальнями и пентхаус', 'شقق بثلاث غرف نوم والبنتهاوس', 'Appartementen met drie slaapkamers en het penthouse',
  'Mieszkania z trzema sypialniami i penthouse', 'Leiligheter med tre soverom og toppleiligheten', 'Lägenheter med tre sovrum och takvåningen')
a('.residences.items[1].points[0]',
  '10 de las 16 tienen tres dormitorios y dos baños, con {N83.04} a {N93.16} {U} interiores, de {E493000} a {E802000}.',
  '10 des 16 ont trois chambres et deux salles de bains, avec {N83.04} à {N93.16} {U} intérieurs, de {E493000} à {E802000}.',
  '10 der 16 haben drei Schlafzimmer und zwei Bäder, mit {N83.04} bis {N93.16} {U} Innenfläche, von {E493000} bis {E802000}.',
  '10 из 16 имеют три спальни и две ванные, внутренняя площадь от {N83.04} до {N93.16} {U}, цена от {E493000} до {E802000}.',
  '10 من أصل 16 بثلاث غرف نوم وحمامين، بمساحة داخلية من {N83.04} إلى {N93.16} {U}، من {E493000} إلى {E802000}.',
  '10 van de 16 hebben drie slaapkamers en twee badkamers, met {N83.04} tot {N93.16} {U} binnenoppervlak, van {E493000} tot {E802000}.',
  '10 z 16 ma trzy sypialnie i dwie łazienki, od {N83.04} do {N93.16} {U} powierzchni wewnętrznej, w cenie od {E493000} do {E802000}.',
  '10 av de 16 har tre soverom og to bad, med {N83.04} til {N93.16} {U} innvendig, fra {E493000} til {E802000}.',
  '10 av de 16 har tre sovrum och två badrum, med {N83.04} till {N93.16} {U} invändigt, från {E493000} till {E802000}.')
a('.residences.items[1].points[1]',
  '2-BJ-C, en planta baja, tiene la mayor terraza de la lista, {N53.30} {U} en dos partes, una cubierta y otra descubierta. El ático, 2-AT-B, tiene {N50.29} {U} de terraza.',
  '2-BJ-C, au rez-de-chaussée, a la plus grande terrasse de la liste, {N53.30} {U} en deux parties, l’une couverte et l’autre découverte. Le penthouse, 2-AT-B, a {N50.29} {U} de terrasse.',
  '2-BJ-C im Erdgeschoss hat die größte Terrasse der Liste, {N53.30} {U} in zwei Teilen, einem überdachten und einem offenen. Das Penthouse 2-AT-B hat {N50.29} {U} Terrasse.',
  'У 2-BJ-C на первом этаже самая большая терраса в списке — {N53.30} {U} из двух частей, крытой и открытой. У пентхауса 2-AT-B терраса {N50.29} {U}.',
  'يملك المسكن 2-BJ-C في الطابق الأرضي أكبر تراس في القائمة، {N53.30} {U} على جزأين، أحدهما مسقوف والآخر مكشوف. وللبنتهاوس 2-AT-B تراس مساحته {N50.29} {U}.',
  '2-BJ-C, op de begane grond, heeft het grootste terras van de lijst, {N53.30} {U} in twee delen, een overdekt en een open. Het penthouse, 2-AT-B, heeft {N50.29} {U} terras.',
  '2-BJ-C na parterze ma największy taras na liście, {N53.30} {U} w dwóch częściach, zadaszonej i otwartej. Penthouse 2-AT-B ma {N50.29} {U} tarasu.',
  '2-BJ-C i første etasje har den største terrassen på listen, {N53.30} {U} i to deler, én overbygd og én åpen. Toppleiligheten, 2-AT-B, har {N50.29} {U} terrasse.',
  '2-BJ-C på bottenvåningen har den största terrassen på listan, {N53.30} {U} i två delar, en övertäckt och en öppen. Takvåningen, 2-AT-B, har {N50.29} {U} terrass.')
a('.residences.items[2].points[0]',
  'Una plaza de garaje y un trastero, que la lista de precios incluye en el precio; tres viviendas, 1-3-C, 5-3-C y 2-AT-B, tienen dos plazas de garaje.',
  'Une place de parking et un cellier, que la liste de prix inclut dans le prix ; trois logements, 1-3-C, 5-3-C et 2-AT-B, ont deux places de parking.',
  'Ein Stellplatz und ein Abstellraum, die laut Preisliste im Preis enthalten sind; drei Wohnungen, 1-3-C, 5-3-C und 2-AT-B, haben zwei Stellplätze.',
  'Машино-место и кладовая, которые прайс-лист включает в цену; у трёх квартир, 1-3-C, 5-3-C и 2-AT-B, по два машино-места.',
  'موقف سيارة ومخزن، تدرجهما قائمة الأسعار ضمن السعر؛ ولثلاثة مساكن، 1-3-C و5-3-C و2-AT-B، موقفا سيارة.',
  'Een parkeerplaats en een berging, die de prijslijst in de prijs opneemt; drie woningen, 1-3-C, 5-3-C en 2-AT-B, hebben twee parkeerplaatsen.',
  'Miejsce parkingowe i komórka lokatorska, które cennik wlicza w cenę; trzy lokale, 1-3-C, 5-3-C i 2-AT-B, mają dwa miejsca parkingowe.',
  'En parkeringsplass og en bod, som prislisten inkluderer i prisen; tre boliger, 1-3-C, 5-3-C og 2-AT-B, har to parkeringsplasser.',
  'En parkeringsplats och ett förråd, som prislistan inkluderar i priset; tre bostäder, 1-3-C, 5-3-C och 2-AT-B, har två parkeringsplatser.')
a('.residences.items[2].points[1]',
  'Una cocina amueblada con los electrodomésticos que enumera la memoria de calidades, y climatización por conductos en el techo.',
  'Une cuisine équipée des appareils énumérés dans le descriptif de qualité, et une climatisation réversible par gaines au plafond.',
  'Eine Einbauküche mit den Geräten, die die Bau- und Ausstattungsbeschreibung aufzählt, und Heizung und Kühlung über Kanäle in der Decke.',
  'Встроенная кухня с техникой, перечисленной в спецификации качества, и отопление и охлаждение через воздуховоды в потолке.',
  'مطبخ مجهز بالأجهزة المذكورة في مواصفات الجودة، وتدفئة وتبريد عبر مجارٍ في السقف.',
  'Een ingerichte keuken met de apparatuur die de kwaliteitsspecificatie noemt, en verwarming en koeling via kanalen in het plafond.',
  'Kuchnia w zabudowie ze sprzętem wymienionym w specyfikacji jakości oraz ogrzewanie i chłodzenie kanałami w suficie.',
  'Et innredet kjøkken med hvitevarene kvalitetsspesifikasjonen lister opp, og oppvarming og kjøling gjennom kanaler i himlingen.',
  'Ett inrett kök med de vitvaror som kvalitetsspecifikationen räknar upp, och värme och kyla via kanaler i taket.')

# ---- lifestyle and location ---------------------------------------------------------------------

a('.lifestyle.headlineHtml',
  'Piscina, spa interior, <em>gimnasio</em> y sala de coworking', 'Une piscine, un spa intérieur, <em>une salle de sport</em> et un espace de coworking',
  'Ein Pool, ein Indoor-Spa, <em>ein Fitnessraum</em> und ein Coworking-Raum', 'Бассейн, спа в помещении, <em>тренажёрный зал</em> и коворкинг',
  'مسبح وسبا داخلي <em>وصالة رياضية</em> وقاعة للعمل المشترك', 'Een zwembad, een binnenspa, <em>een fitnessruimte</em> en een coworkingruimte',
  'Basen, spa w budynku, <em>siłownia</em> i sala coworkingowa', 'Et basseng, et innendørs spa, <em>et treningsrom</em> og et coworking-rom',
  'En pool, ett inomhusspa, <em>ett gym</em> och ett coworking-rum')
a('.lifestyle.panels[0][1]',
  'El folleto cuenta dos piscinas, una exterior y otra climatizada. La memoria de calidades enumera una piscina comunitaria exterior con cloración salina, jardín y solárium, y la piscina climatizada dentro del spa.',
  'La brochure compte deux piscines, l’une extérieure et l’autre chauffée. Le descriptif de qualité mentionne une piscine commune extérieure à chloration au sel, avec jardin et solarium, et la piscine chauffée à l’intérieur du spa.',
  'Die Broschüre nennt zwei Pools, einen Außenpool und einen beheizten. Die Bau- und Ausstattungsbeschreibung führt einen gemeinschaftlichen Außenpool mit Salzelektrolyse, Garten und Sonnenterrasse sowie den beheizten Pool im Spa auf.',
  'В брошюре два бассейна: открытый и подогреваемый. Спецификация качества называет общий открытый бассейн с солевым хлорированием, садом и солярием и подогреваемый бассейн в спа.',
  'يذكر الكتيّب مسبحين، أحدهما خارجي والآخر مدفأ. وتذكر مواصفات الجودة مسبحًا مشتركًا خارجيًا بنظام كلورة ملحية مع حديقة ومنطقة تشمّس، والمسبح المدفأ داخل السبا.',
  'De brochure telt twee zwembaden, een buitenbad en een verwarmd bad. De kwaliteitsspecificatie noemt een gemeenschappelijk buitenzwembad met zoutchlorering, een tuin en een zonneterras, en het verwarmde zwembad in de spa.',
  'Broszura wymienia dwa baseny, zewnętrzny i podgrzewany. Specyfikacja jakości wymienia wspólny basen zewnętrzny z chlorowaniem solnym, ogrodem i strefą do opalania oraz podgrzewany basen w spa.',
  'Brosjyren nevner to basseng, ett utendørs og ett oppvarmet. Kvalitetsspesifikasjonen nevner et felles utendørs basseng med saltklorering, hage og soltak, og det oppvarmede bassenget i spaet.',
  'Broschyren nämner två pooler, en utomhus och en uppvärmd. Kvalitetsspecifikationen nämner en gemensam utomhuspool med saltklorering, trädgård och soldäck, och den uppvärmda poolen i spat.')
a('.lifestyle.panels[1][1]',
  'Un spa interior con piscina climatizada, sauna y circuito de duchas, conectado con el gimnasio y los vestuarios, tal como lo enumera la memoria de calidades.',
  'Un spa intérieur avec piscine chauffée, sauna et parcours de douches, relié à la salle de sport et aux vestiaires, tel que le décrit le descriptif de qualité.',
  'Ein Indoor-Spa mit beheiztem Pool, Sauna und Duschparcours, verbunden mit dem Fitnessraum und den Umkleiden, wie die Bau- und Ausstattungsbeschreibung es aufführt.',
  'Спа в помещении с подогреваемым бассейном, сауной и душевым контуром, соединённое с тренажёрным залом и раздевалками, как указано в спецификации качества.',
  'سبا داخلي بمسبح مدفأ وساونا ومسار دشات، متصل بالصالة الرياضية وغرف تبديل الملابس، كما تذكره مواصفات الجودة.',
  'Een binnenspa met een verwarmd zwembad, een sauna en een douchecircuit, verbonden met de fitnessruimte en de kleedkamers, zoals de kwaliteitsspecificatie het beschrijft.',
  'Spa w budynku z podgrzewanym basenem, sauną i ścieżką prysznicową, połączone z siłownią i szatniami, tak jak opisuje je specyfikacja jakości.',
  'Et innendørs spa med oppvarmet basseng, badstue og dusjløype, forbundet med treningsrommet og garderobene, slik kvalitetsspesifikasjonen beskriver det.',
  'Ett inomhusspa med uppvärmd pool, bastu och duschslinga, förbundet med gymmet och omklädningsrummen, så som kvalitetsspecifikationen beskriver det.')
a('.lifestyle.panels[2][1]',
  'Un gimnasio totalmente equipado y un espacio de coworking con office y aseos, abiertos a todos los residentes. Los documentos no dan superficies ni una lista de equipamiento.',
  'Une salle de sport entièrement équipée et un espace de coworking avec kitchenette et sanitaires, ouverts à tous les résidents. Les documents ne donnent ni surfaces ni liste d’équipements.',
  'Ein voll ausgestatteter Fitnessraum und ein Coworking-Bereich mit Teeküche und Toiletten, offen für alle Bewohner. Die Unterlagen nennen weder Flächen noch eine Ausstattungsliste.',
  'Полностью оборудованный тренажёрный зал и коворкинг с мини-кухней и туалетами, открытые для всех жителей. Площадей и перечня оборудования в документах нет.',
  'صالة رياضية مجهزة بالكامل ومساحة للعمل المشترك مع مطبخ صغير ودورات مياه، مفتوحتان لجميع السكان. ولا تذكر الوثائق مساحات ولا قائمة تجهيزات.',
  'Een volledig uitgeruste fitnessruimte en een coworkingruimte met kitchenette en toiletten, open voor alle bewoners. De documenten geven geen oppervlaktes en geen lijst met apparatuur.',
  'W pełni wyposażona siłownia i przestrzeń coworkingowa z aneksem kuchennym i toaletami, dostępne dla wszystkich mieszkańców. Dokumenty nie podają powierzchni ani listy wyposażenia.',
  'Et fullt utstyrt treningsrom og et coworking-område med tekjøkken og toaletter, åpne for alle beboerne. Dokumentene oppgir verken arealer eller utstyrsliste.',
  'Ett fullt utrustat gym och ett coworking-utrymme med pentry och toaletter, öppna för alla boende. Dokumenten anger varken ytor eller utrustningslista.')
a('.lifestyle.panels[3][1]',
  'Jardines con vegetación mediterránea. El folleto dice que la jardinería emplea especies autóctonas, en sintonía con el pinar junto al solar.',
  'Des jardins paysagers à la végétation méditerranéenne. La brochure indique que les plantations font appel à des espèces locales, en harmonie avec la pinède voisine.',
  'Angelegte Gärten mit mediterraner Bepflanzung. Laut Broschüre setzt die Bepflanzung auf heimische Arten, im Einklang mit dem Pinienwald neben dem Grundstück.',
  'Ландшафтные сады со средиземноморскими растениями. В брошюре сказано, что в озеленении используются местные виды в гармонии с сосновым лесом рядом с участком.',
  'حدائق منسّقة بنباتات متوسطية. ويذكر الكتيّب أن التشجير يعتمد على أنواع محلية، بانسجام مع غابة الصنوبر المجاورة للموقع.',
  'Aangelegde tuinen met mediterrane beplanting. De brochure zegt dat de beplanting inheemse soorten gebruikt, in harmonie met het dennenbos naast het terrein.',
  'Ogrody z roślinnością śródziemnomorską. Broszura podaje, że nasadzenia obejmują gatunki rodzime, w zgodzie z lasem sosnowym obok działki.',
  'Anlagte hager med middelhavsbeplantning. Brosjyren sier at beplantningen bruker stedegne arter, i tråd med furuskogen ved tomten.',
  'Anlagda trädgårdar med medelhavsväxter. Broschyren anger att planteringen använder inhemska arter, i samklang med tallskogen intill tomten.')
a('.location.headlineHtml',
  'Torremolinos, <em>junto a un pinar</em>', 'Torremolinos, <em>près d’une pinède</em>', 'Torremolinos, <em>an einem Pinienwald</em>',
  'Торремолинос, <em>у соснового леса</em>', 'توريمولينوس، <em>بجانب غابة صنوبر</em>', 'Torremolinos, <em>naast een dennenbos</em>',
  'Torremolinos, <em>przy lesie sosnowym</em>', 'Torremolinos, <em>ved en furuskog</em>', 'Torremolinos, <em>vid en tallskog</em>')
a('.location.mapLabelHtml',
  'Torremolinos, <em>junto a un pinar</em>', 'Torremolinos, <em>près d’une pinède</em>', 'Torremolinos, <em>an einem Pinienwald</em>',
  'Торремолинос, <em>у соснового леса</em>', 'توريمولينوس، <em>بجانب غابة صنوبر</em>', 'Torremolinos, <em>naast een dennenbos</em>',
  'Torremolinos, <em>przy lesie sosnowym</em>', 'Torremolinos, <em>ved en furuskog</em>', 'Torremolinos, <em>vid en tallskog</em>')
a('.location.mapLabelPlain',
  'Torremolinos, junto a un pinar', 'Torremolinos, près d’une pinède', 'Torremolinos, an einem Pinienwald',
  'Торремолинос, у соснового леса', 'توريمولينوس، بجانب غابة صنوبر', 'Torremolinos, naast een dennenbos',
  'Torremolinos, przy lesie sosnowym', 'Torremolinos, ved en furuskog', 'Torremolinos, vid en tallskog')
a('.location.copy',
  'El folleto sitúa la promoción en un solar elevado de Torremolinos, frente a un pinar, y su plano de situación marca el solar al suroeste del Pinar Molino del Moro, al oeste del centro. Los documentos no dan coordenadas de la parcela, así que la ubicación del mapa es aproximada. El folleto da unos 5 minutos al aeropuerto de Málaga y 10 minutos al centro de Málaga; la ruta por carretera que hemos medido desde la ubicación hasta el aeropuerto tarda unos 19 minutos. Confirmamos los tiempos de trayecto en una visita.',
  'La brochure situe la résidence sur un terrain surélevé de Torremolinos, face à une pinède, et son plan de situation place le site au sud-ouest du Pinar Molino del Moro, à l’ouest du centre-ville. Les documents ne donnent pas de coordonnées de la parcelle : le repère sur la carte est donc approximatif. La brochure indique environ 5 minutes jusqu’à l’aéroport de Malaga et 10 minutes jusqu’au centre de Malaga ; l’itinéraire routier que nous avons mesuré depuis le repère jusqu’à l’aéroport prend environ 19 minutes. Nous vérifions les temps de trajet lors d’une visite.',
  'Die Broschüre verortet die Anlage auf einem erhöhten Grundstück in Torremolinos gegenüber einem Pinienwald, und ihr Lageplan zeigt das Grundstück südwestlich des Pinar Molino del Moro, westlich des Zentrums. Die Unterlagen nennen keine Koordinaten des Grundstücks, daher ist die Markierung auf der Karte ungefähr. Die Broschüre nennt etwa 5 Minuten zum Flughafen Málaga und 10 Minuten ins Zentrum von Málaga; die von uns gemessene Straßenroute von der Markierung zum Flughafen dauert etwa 19 Minuten. Wir prüfen die Fahrzeiten bei einem Besuch.',
  'Брошюра размещает комплекс на возвышенном участке в Торремолиносе напротив соснового леса, а её ситуационный план отмечает участок к юго-западу от Пинар-Молино-дель-Моро, западнее центра. Координат участка в документах нет, поэтому метка на карте приблизительная. Брошюра указывает около 5 минут до аэропорта Малаги и 10 минут до центра Малаги; измеренный нами маршрут по дороге от метки до аэропорта занимает около 19 минут. Мы проверяем время в пути при визите.',
  'يضع الكتيّب المشروع على موقع مرتفع في توريمولينوس قبالة غابة صنوبر، وتحدد خريطة الموقع فيه الأرض جنوب غرب غابة بينار مولينو ديل مورو، غرب وسط المدينة. ولا تذكر الوثائق إحداثيات قطعة الأرض، لذا فإن الموضع على الخريطة تقريبي. ويذكر الكتيّب نحو 5 دقائق إلى مطار مالقة و10 دقائق إلى وسط مالقة، بينما يستغرق الطريق الذي قسناه من الموضع إلى المطار نحو 19 دقيقة. ونتحقق من أوقات القيادة خلال الزيارة.',
  'De brochure plaatst het project op een verhoogd terrein in Torremolinos, tegenover een dennenbos, en de situatiekaart markeert het terrein ten zuidwesten van het Pinar Molino del Moro, ten westen van het centrum. De documenten geven geen coördinaten van het perceel, dus de markering op de kaart is bij benadering. De brochure noemt ongeveer 5 minuten naar de luchthaven van Málaga en 10 minuten naar het centrum van Málaga; de route over de weg die wij vanaf de markering naar de luchthaven hebben gemeten, duurt ongeveer 19 minuten. Wij controleren de reistijden tijdens een bezoek.',
  'Broszura umieszcza inwestycję na wyniesionej działce w Torremolinos, naprzeciw lasu sosnowego, a jej mapa lokalizacji zaznacza działkę na południowy zachód od Pinar Molino del Moro, na zachód od centrum. Dokumenty nie podają współrzędnych działki, więc znacznik na mapie jest przybliżony. Broszura podaje około 5 minut do lotniska w Maladze i 10 minut do centrum Malagi; zmierzona przez nas trasa drogowa od znacznika do lotniska zajmuje około 19 minut. Czasy dojazdu sprawdzamy podczas wizyty.',
  'Brosjyren plasserer prosjektet på en høyt beliggende tomt i Torremolinos, rett overfor en furuskog, og situasjonskartet viser tomten sørvest for Pinar Molino del Moro, vest for sentrum. Dokumentene oppgir ingen koordinater for tomten, så markøren på kartet er omtrentlig. Brosjyren oppgir omtrent 5 minutter til flyplassen i Málaga og 10 minutter til Málaga sentrum; veiruten vi har målt fra markøren til flyplassen, tar omtrent 19 minutter. Vi sjekker kjøretidene ved en visning.',
  'Broschyren placerar projektet på en upphöjd tomt i Torremolinos, mitt emot en tallskog, och dess lägeskarta markerar tomten sydväst om Pinar Molino del Moro, väster om centrum. Dokumenten anger inga koordinater för tomten, så markören på kartan är ungefärlig. Broschyren anger ungefär 5 minuter till flygplatsen i Málaga och 10 minuter till Málaga centrum; vägrutten vi har mätt från markören till flygplatsen tar ungefär 19 minuter. Vi kontrollerar restiderna vid ett besök.')
a('.location.distances[2][0]',
  'Centro de Málaga', 'Centre de Malaga', 'Stadtzentrum Málaga', 'Центр Малаги', 'وسط مدينة مالقة', 'Centrum van Málaga',
  'Centrum Malagi', 'Málaga sentrum', 'Málaga centrum')
a('.location.distances[2][1]',
  'Unos 10 minutos en coche', 'Environ 10 minutes en voiture', 'Etwa 10 Minuten mit dem Auto', 'Около 10 минут на машине',
  'نحو 10 دقائق بالسيارة', 'Ongeveer 10 minuten met de auto', 'Około 10 minut samochodem', 'Omtrent 10 minutter med bil', 'Ungefär 10 minuter med bil')
a('.location.distances[3][1]',
  'Unos 30 minutos', 'Environ 30 minutes', 'Etwa 30 Minuten', 'Около 30 минут', 'نحو 30 دقيقة', 'Ongeveer 30 minuten',
  'Około 30 minut', 'Omtrent 30 minutter', 'Ungefär 30 minuter')

# ---- investment, trust, availability ------------------------------------------------------------

a('.investment.cards[0][1]',
  'La lista recoge 16 viviendas: seis apartamentos de dos dormitorios de {E425000} a {E485000}, nueve de tres dormitorios de {E493000} a {E601000} y un ático de tres dormitorios por {E802000}.',
  'La liste compte 16 logements : six appartements de deux chambres de {E425000} à {E485000}, neuf de trois chambres de {E493000} à {E601000} et un penthouse de trois chambres à {E802000}.',
  'Die Liste führt 16 Wohnungen: sechs mit zwei Schlafzimmern von {E425000} bis {E485000}, neun mit drei Schlafzimmern von {E493000} bis {E601000} und ein Penthouse mit drei Schlafzimmern für {E802000}.',
  'В списке 16 квартир: шесть с двумя спальнями от {E425000} до {E485000}, девять с тремя спальнями от {E493000} до {E601000} и пентхаус с тремя спальнями за {E802000}.',
  'تضم القائمة 16 مسكنًا: ست شقق بغرفتي نوم من {E425000} إلى {E485000}، وتسع شقق بثلاث غرف نوم من {E493000} إلى {E601000}، وبنتهاوس بثلاث غرف نوم بسعر {E802000}.',
  'De lijst noemt 16 woningen: zes appartementen met twee slaapkamers van {E425000} tot {E485000}, negen met drie slaapkamers van {E493000} tot {E601000} en een penthouse met drie slaapkamers voor {E802000}.',
  'Cennik obejmuje 16 lokali: sześć mieszkań z dwiema sypialniami od {E425000} do {E485000}, dziewięć z trzema sypialniami od {E493000} do {E601000} i penthouse z trzema sypialniami za {E802000}.',
  'Listen har 16 boliger: seks leiligheter med to soverom fra {E425000} til {E485000}, ni med tre soverom fra {E493000} til {E601000} og en toppleilighet med tre soverom til {E802000}.',
  'Listan har 16 bostäder: sex lägenheter med två sovrum från {E425000} till {E485000}, nio med tre sovrum från {E493000} till {E601000} och en takvåning med tre sovrum för {E802000}.')
a('.investment.cards[1][0]',
  'Los impuestos y el precio', 'Les taxes et le prix', 'Steuern und Preis', 'Налоги и цена', 'الضرائب والسعر', 'Belasting en prijs',
  'Podatki a cena', 'Skatt og pris', 'Skatt och pris')
a('.investment.cards[1][1]',
  'La lista de precios titula su última columna «Total €» y no dice si el {T} está incluido. Las demás listas de precios del promotor que tenemos dan sus precios sin {T}, así que esta página los muestra igual. Con un {T} del 10 % y un impuesto de actos jurídicos documentados del {N1.20} %, {E425000} serían unos {E473000}, antes de notaría y registro. Lo confirmamos por escrito.',
  'La liste de prix intitule sa dernière colonne « Total € » et n’indique pas si la {T} est incluse. Les autres listes de prix du promoteur en notre possession donnent leurs prix hors {T} ; cette page les présente donc de la même façon. Avec une {T} de 10 % et un droit de timbre de {N1.20} %, {E425000} deviendraient environ {E473000}, avant les frais de notaire et d’enregistrement. Nous le confirmons par écrit.',
  'Die Preisliste überschreibt ihre letzte Spalte mit „Total €“ und sagt nicht, ob die {T} enthalten ist. Die anderen Preislisten des Bauträgers, die uns vorliegen, nennen ihre Preise vor {T}, daher zeigt diese Seite sie ebenso. Mit 10 % {T} und 1,20 % Stempelsteuer würden aus {E425000} etwa {E473000}, vor Notar- und Grundbuchkosten. Wir bestätigen es schriftlich.',
  'Последний столбец прайс-листа озаглавлен «Total €», и в нём не сказано, включён ли {T}. В других прайс-листах застройщика, которые у нас есть, цены указаны без {T}, поэтому эта страница показывает их так же. С {T} 10 % и гербовым сбором {N1.20} % {E425000} превратились бы примерно в {E473000} до нотариальных и регистрационных расходов. Мы подтверждаем это письменно.',
  'تعنون قائمة الأسعار عمودها الأخير بـ«Total €» ولا تذكر ما إذا كانت {T} مشمولة. أما قوائم أسعار المطوّر الأخرى التي لدينا فتذكر أسعارها قبل {T}، لذا تعرضها هذه الصفحة بالطريقة نفسها. ومع {T} بنسبة 10% ورسم دمغة بنسبة {N1.20}%، يصبح مبلغ {E425000} نحو {E473000}، قبل رسوم الكاتب العدل والسجل العقاري. ونؤكد ذلك كتابيًا.',
  'De prijslijst noemt haar laatste kolom “Total €” en zegt niet of de {T} is inbegrepen. De andere prijslijsten van de ontwikkelaar die wij hebben, geven hun prijzen exclusief {T}, dus deze pagina toont ze op dezelfde manier. Met 10% {T} en {N1.20}% zegelbelasting wordt {E425000} ongeveer {E473000}, vóór notaris- en kadasterkosten. Wij bevestigen het schriftelijk.',
  'Cennik zatytułował ostatnią kolumnę „Total €” i nie podaje, czy {T} jest wliczony. Pozostałe cenniki dewelopera, którymi dysponujemy, podają ceny bez {T}, więc ta strona pokazuje je w ten sam sposób. Przy {T} 10% i opłacie skarbowej {N1.20}% kwota {E425000} wyniosłaby około {E473000}, przed opłatami notarialnymi i wpisem do księgi wieczystej. Potwierdzamy to na piśmie.',
  'Prislisten kaller den siste kolonnen «Total €» og sier ikke om {T} er inkludert. Utbyggerens andre prislister som vi har, oppgir prisene før {T}, så denne siden viser dem på samme måte. Med 10 % {T} og {N1.20} % dokumentavgift ville {E425000} bli omtrent {E473000}, før notar- og tinglysingsgebyrer. Vi bekrefter det skriftlig.',
  'Prislistan rubricerar sin sista kolumn ”Total €” och anger inte om {T} (spansk moms) ingår. Exploatörens övriga prislistor som vi har anger priserna före {T}, så den här sidan visar dem på samma sätt. Med 10 % {T} och {N1.20} % stämpelskatt skulle {E425000} bli omkring {E473000}, före notarie- och registreringsavgifter. Vi bekräftar det skriftligt.')
a('.investment.cards[2][0]',
  'Todavía sin fechas', 'Pas encore de dates', 'Noch keine Termine', 'Сроков пока нет', 'لا مواعيد بعد', 'Nog geen data',
  'Na razie bez terminów', 'Ingen datoer ennå', 'Inga datum ännu')
a('.investment.cards[2][1]',
  'Ningún documento da una licencia, el estado de las obras ni una fecha de entrega, y los planos de noviembre de 2025 dicen que sus superficies son provisionales hasta que se conceda la licencia de obras.',
  'Aucun document ne donne de permis, d’état des travaux ni de date de livraison, et les plans de novembre 2025 précisent que leurs surfaces sont provisoires jusqu’à l’obtention du permis de construire.',
  'Kein Dokument nennt eine Genehmigung, den Stand der Arbeiten oder einen Fertigstellungstermin, und die Pläne vom November 2025 geben an, dass ihre Flächen bis zur Erteilung der Baugenehmigung vorläufig sind.',
  'Ни один документ не указывает разрешения, стадии работ или даты сдачи, а планы ноября 2025 года оговаривают, что их площади предварительны до выдачи разрешения на строительство.',
  'لا تذكر أي وثيقة رخصة ولا مرحلة الأعمال ولا موعد التسليم، وتنص مخططات نوفمبر 2025 على أن مساحاتها مؤقتة حتى منح رخصة البناء.',
  'Geen enkel document noemt een vergunning, de stand van de werken of een opleverdatum, en de plannen van november 2025 zeggen dat hun oppervlaktes voorlopig zijn tot de bouwvergunning is verleend.',
  'Żaden dokument nie podaje pozwolenia, etapu prac ani terminu oddania, a plany z listopada 2025 roku zastrzegają, że ich powierzchnie są tymczasowe do czasu wydania pozwolenia na budowę.',
  'Ingen dokumenter oppgir en tillatelse, hvor langt arbeidet har kommet eller en ferdigdato, og tegningene fra november 2025 sier at arealene er foreløpige til byggetillatelsen er gitt.',
  'Inget dokument anger ett tillstånd, hur långt arbetet har kommit eller ett färdigdatum, och ritningarna från november 2025 anger att ytorna är preliminära tills bygglovet har beviljats.')
a('.investment.cards[3][1]',
  'La lista dice que no tiene valor contractual y que los precios pueden variar según el avance del proyecto y la disponibilidad. Volvemos a confirmar la cifra con el vendedor antes de que usted reserve.',
  'La liste indique qu’elle n’a aucune valeur contractuelle et que les prix peuvent varier selon l’avancement du projet et la disponibilité. Nous reconfirmons le montant auprès du vendeur avant que vous ne réserviez.',
  'Die Liste gibt an, keinen Vertragswert zu haben und dass die Preise je nach Projektfortschritt und Verfügbarkeit schwanken können. Wir bestätigen den Betrag beim Verkäufer erneut, bevor Sie reservieren.',
  'В списке сказано, что он не имеет договорной силы, а цены могут меняться в зависимости от хода проекта и наличия. Мы заново подтверждаем сумму у продавца до того, как вы забронируете.',
  'تذكر القائمة أنها ليست لها قيمة تعاقدية وأن الأسعار قد تتغير بحسب تقدّم المشروع والتوفر. ونعيد تأكيد المبلغ مع البائع قبل أن تحجز.',
  'De lijst zegt dat ze geen contractuele waarde heeft en dat de prijzen kunnen variëren naargelang de voortgang van het project en de beschikbaarheid. Wij bevestigen het bedrag opnieuw bij de verkoper voordat u reserveert.',
  'Cennik zastrzega, że nie ma wartości umownej, a ceny mogą się zmieniać w zależności od postępu projektu i dostępności. Kwotę potwierdzamy ponownie u sprzedającego, zanim Państwo dokonają rezerwacji.',
  'Listen sier at den ikke har kontraktsverdi og at prisene kan variere med fremdriften i prosjektet og tilgjengeligheten. Vi bekrefter beløpet på nytt hos selgeren før du reserverer.',
  'Listan anger att den saknar avtalsvärde och att priserna kan variera med projektets framsteg och tillgängligheten. Vi bekräftar beloppet på nytt hos säljaren innan ni bokar.')
a('.trustDossier.cards[0][0]',
  'El {T}', 'La {T}', 'Die {T}', '{T}', 'ضريبة القيمة المضافة', 'De {T}', 'VAT', 'Mva', 'IVA (spansk moms)')
a('.trustDossier.cards[0][1]',
  'La lista de precios no dice si sus precios incluyen el {T}. Pedimos al promotor que confirme por escrito que son sin {T}, como en sus otras listas.',
  'La liste de prix n’indique pas si ses prix incluent la {T}. Nous demandons au promoteur de confirmer par écrit qu’ils s’entendent hors {T}, comme sur ses autres listes.',
  'Die Preisliste sagt nicht, ob ihre Preise die {T} enthalten. Wir bitten den Bauträger, schriftlich zu bestätigen, dass sie wie auf seinen anderen Listen vor {T} gelten.',
  'В прайс-листе не сказано, включён ли {T} в цены. Мы просим застройщика письменно подтвердить, что они указаны без {T}, как в других его списках.',
  'لا تذكر قائمة الأسعار ما إذا كانت أسعارها تشمل {T}. ونطلب من المطوّر أن يؤكد كتابيًا أنها قبل {T}، كما في قوائمه الأخرى.',
  'De prijslijst zegt niet of de prijzen inclusief {T} zijn. Wij vragen de ontwikkelaar schriftelijk te bevestigen dat ze exclusief {T} zijn, zoals op zijn andere lijsten.',
  'Cennik nie podaje, czy ceny zawierają {T}. Prosimy dewelopera o pisemne potwierdzenie, że są to ceny bez {T}, jak w jego innych cennikach.',
  'Prislisten sier ikke om prisene inkluderer {T}. Vi ber utbyggeren bekrefte skriftlig at de er før {T}, som på de andre listene.',
  'Prislistan anger inte om priserna inkluderar {T}. Vi ber exploatören bekräfta skriftligt att de är före {T}, som på dess övriga listor.')
a('.trustDossier.cards[1][1]',
  'Ningún documento da una licencia de obras, el estado de las obras ni una fecha de entrega. La única fotografía de avance de obra del promotor, del 15 de diciembre de 2025, parece mostrar movimiento de tierras en la parcela. Pedimos la licencia, el programa de obras y la fecha de entrega contractual.',
  'Aucun document ne donne de permis de construire, d’état des travaux ni de date de livraison. L’unique photographie d’avancement du promoteur, datée du 15 décembre 2025, semble montrer des terrassements sur la parcelle. Nous demandons le permis, le planning des travaux et la date de livraison contractuelle.',
  'Kein Dokument nennt eine Baugenehmigung, den Stand der Arbeiten oder einen Fertigstellungstermin. Das einzige Baufortschrittsfoto des Bauträgers vom 15. Dezember 2025 scheint Erdarbeiten auf dem Grundstück zu zeigen. Wir fordern die Genehmigung, den Bauzeitenplan und den vertraglichen Fertigstellungstermin an.',
  'Ни один документ не указывает разрешения на строительство, стадии работ или даты сдачи. Единственный снимок хода работ от застройщика, датированный 15 декабря 2025 года, по-видимому, показывает земляные работы на участке. Мы запрашиваем разрешение, график работ и договорную дату сдачи.',
  'لا تذكر أي وثيقة رخصة بناء ولا مرحلة الأعمال ولا موعد التسليم. ويبدو أن صورة تقدّم الأعمال الوحيدة من المطوّر، بتاريخ 15 ديسمبر 2025، تُظهر أعمال حفر وتسوية على قطعة الأرض. ونطلب الرخصة وجدول الأعمال وموعد التسليم التعاقدي.',
  'Geen enkel document noemt een bouwvergunning, de stand van de werken of een opleverdatum. De enige voortgangsfoto van de ontwikkelaar, van 15 december 2025, lijkt grondwerken op het perceel te tonen. Wij vragen de vergunning, de bouwplanning en de contractuele opleverdatum op.',
  'Żaden dokument nie podaje pozwolenia na budowę, etapu prac ani terminu oddania. Jedyne zdjęcie postępu budowy od dewelopera, z 15 grudnia 2025 roku, zdaje się pokazywać roboty ziemne na działce. Prosimy o pozwolenie, harmonogram prac i umowny termin oddania.',
  'Ingen dokumenter oppgir en byggetillatelse, hvor langt arbeidet har kommet eller en ferdigdato. Utbyggerens eneste fremdriftsbilde, datert 15. desember 2025, ser ut til å vise grunnarbeider på tomten. Vi ber om tillatelsen, fremdriftsplanen og den kontraktsfestede ferdigdatoen.',
  'Inget dokument anger ett bygglov, hur långt arbetet har kommit eller ett färdigdatum. Exploatörens enda bild av byggets framsteg, daterad den 15 december 2025, tycks visa markarbeten på tomten. Vi begär bygglovet, tidsplanen och det avtalade färdigdatumet.')
a('.trustDossier.cards[2][0]',
  'Los planos y la lista', 'Les plans et la liste', 'Die Pläne und die Liste', 'Планы и список', 'المخططات والقائمة', 'De plannen en de lijst',
  'Rzuty i cennik', 'Tegningene og listen', 'Ritningarna och listan')
a('.trustDossier.cards[2][1]',
  'Tenemos planos de 15 de las 16 viviendas; 3-1-C no tiene. En 13 viviendas los planos coinciden con la lista en superficie interior, terraza y superficie construida. En 4-BJ-C la lista da {N110.18} {U} construidos y el plano {N110.88} {U}; en 4-2-C la lista da {N123.37} {U} construidos y una terraza de {N18.67} {U}, el plano {N125.79} {U} y {N18.82} {U}. La columna «útil» de la lista da la superficie interior en unas viviendas y la interior más la terraza en otras, por lo que esta página toma las superficies interiores de los planos.',
  'Nous avons les plans de 15 des 16 logements ; 3-1-C n’en a pas. Pour 13 logements, les plans concordent avec la liste pour la surface intérieure, la terrasse et la surface construite. Pour 4-BJ-C, la liste indique {N110.18} {U} construits et le plan {N110.88} {U} ; pour 4-2-C, la liste indique {N123.37} {U} construits et une terrasse de {N18.67} {U}, le plan {N125.79} {U} et {N18.82} {U}. La colonne « utile » de la liste donne la surface intérieure pour certains logements et la surface intérieure plus la terrasse pour d’autres ; cette page reprend donc les surfaces intérieures des plans.',
  'Wir haben Pläne für 15 der 16 Wohnungen; für 3-1-C gibt es keinen. Bei 13 Wohnungen stimmen die Pläne mit der Liste bei Innenfläche, Terrasse und bebauter Fläche überein. Für 4-BJ-C nennt die Liste {N110.18} {U} bebaut und der Plan {N110.88} {U}; für 4-2-C nennt die Liste {N123.37} {U} bebaut und eine Terrasse von {N18.67} {U}, der Plan {N125.79} {U} und {N18.82} {U}. Die Spalte „Nutzfläche“ der Liste nennt bei manchen Wohnungen die Innenfläche und bei anderen Innenfläche plus Terrasse, daher übernimmt diese Seite die Innenflächen aus den Plänen.',
  'У нас есть планы 15 из 16 квартир; для 3-1-C плана нет. По 13 квартирам планы совпадают со списком по внутренней площади, террасе и площади застройки. Для 4-BJ-C список даёт {N110.18} {U} площади застройки, а план — {N110.88} {U}; для 4-2-C список даёт {N123.37} {U} и террасу {N18.67} {U}, план — {N125.79} {U} и {N18.82} {U}. Столбец «полезная площадь» в списке для одних квартир указывает внутреннюю площадь, а для других — внутреннюю вместе с террасой, поэтому эта страница берёт внутренние площади из планов.',
  'لدينا مخططات 15 من أصل 16 مسكنًا؛ ولا مخطط للمسكن 3-1-C. وفي 13 مسكنًا تتطابق المخططات مع القائمة في المساحة الداخلية والتراس والمساحة المبنية. وفي 4-BJ-C تذكر القائمة {N110.18} {U} مبنية والمخطط {N110.88} {U}؛ وفي 4-2-C تذكر القائمة {N123.37} {U} مبنية وتراسًا مساحته {N18.67} {U}، والمخطط {N125.79} {U} و{N18.82} {U}. ويعطي عمود «المساحة الصافية» في القائمة المساحة الداخلية لبعض المساكن والداخلية مع التراس لبعضها الآخر، لذا تأخذ هذه الصفحة المساحات الداخلية من المخططات.',
  'Wij hebben plattegronden van 15 van de 16 woningen; 3-1-C heeft er geen. Bij 13 woningen komen de plannen met de lijst overeen qua binnenoppervlak, terras en bebouwde oppervlakte. Bij 4-BJ-C geeft de lijst {N110.18} {U} bebouwd en het plan {N110.88} {U}; bij 4-2-C geeft de lijst {N123.37} {U} bebouwd en een terras van {N18.67} {U}, het plan {N125.79} {U} en {N18.82} {U}. De kolom “nuttig” van de lijst geeft bij sommige woningen het binnenoppervlak en bij andere binnenoppervlak plus terras, dus deze pagina neemt de binnenoppervlaktes over uit de plannen.',
  'Mamy rzuty 15 z 16 lokali; 3-1-C go nie ma. W 13 lokalach rzuty zgadzają się z cennikiem co do powierzchni wewnętrznej, tarasu i powierzchni zabudowy. Dla 4-BJ-C cennik podaje {N110.18} {U} zabudowy, a rzut {N110.88} {U}; dla 4-2-C cennik podaje {N123.37} {U} zabudowy i taras {N18.67} {U}, rzut {N125.79} {U} i {N18.82} {U}. Kolumna „użytkowa” w cenniku podaje dla jednych lokali powierzchnię wewnętrzną, a dla innych wewnętrzną z tarasem, dlatego ta strona przyjmuje powierzchnie wewnętrzne z rzutów.',
  'Vi har tegninger for 15 av de 16 boligene; 3-1-C har ingen. For 13 boliger stemmer tegningene med listen for innvendig areal, terrasse og bebygd areal. For 4-BJ-C oppgir listen {N110.18} {U} bebygd og tegningen {N110.88} {U}; for 4-2-C oppgir listen {N123.37} {U} bebygd og en terrasse på {N18.67} {U}, tegningen {N125.79} {U} og {N18.82} {U}. Listens kolonne «nyttig» oppgir innvendig areal for noen boliger og innvendig areal pluss terrasse for andre, så denne siden henter de innvendige arealene fra tegningene.',
  'Vi har ritningar för 15 av de 16 bostäderna; 3-1-C har ingen. För 13 bostäder stämmer ritningarna med listan i fråga om invändig yta, terrass och byggyta. För 4-BJ-C anger listan {N110.18} {U} byggyta och ritningen {N110.88} {U}; för 4-2-C anger listan {N123.37} {U} byggyta och en terrass på {N18.67} {U}, ritningen {N125.79} {U} och {N18.82} {U}. Listans kolumn ”användbar” anger invändig yta för vissa bostäder och invändig yta plus terrass för andra, så den här sidan hämtar de invändiga ytorna från ritningarna.')
a('.trustDossier.cards[3][0]',
  'La terraza del ático', 'La terrasse du penthouse', 'Die Terrasse des Penthouse', 'Терраса пентхауса', 'تراس البنتهاوس', 'Het terras van het penthouse',
  'Taras penthouse’u', 'Terrassen på toppleiligheten', 'Takvåningens terrass')
a('.trustDossier.cards[3][1]',
  'La lista sitúa los {N50.29} {U} de 2-AT-B como terraza cubierta, mientras que su plano muestra dos solárium de {N23.81} y {N26.48} {U}. Preguntamos qué partes están cubiertas.',
  'La liste classe les {N50.29} {U} de 2-AT-B en terrasse couverte, alors que son plan montre deux solariums de {N23.81} et {N26.48} {U}. Nous demandons quelles parties sont couvertes.',
  'Die Liste führt die {N50.29} {U} von 2-AT-B als überdachte Terrasse, während sein Grundriss zwei Solarien von {N23.81} und {N26.48} {U} zeigt. Wir fragen nach, welche Teile überdacht sind.',
  'В списке {N50.29} {U} у 2-AT-B значатся как крытая терраса, а на плане это два солярия по {N23.81} и {N26.48} {U}. Мы уточняем, какие части крытые.',
  'تصنّف القائمة مساحة {N50.29} {U} في 2-AT-B تراسًا مسقوفًا، بينما يُظهر مخططه سولاريومين مساحتهما {N23.81} و{N26.48} {U}. ونسأل عن الأجزاء المسقوفة.',
  'De lijst rekent de {N50.29} {U} van 2-AT-B tot overdekt terras, terwijl de plattegrond twee solariums van {N23.81} en {N26.48} {U} toont. Wij vragen welke delen overdekt zijn.',
  'Cennik zalicza {N50.29} {U} lokalu 2-AT-B do tarasu zadaszonego, podczas gdy rzut pokazuje dwa solaria o powierzchni {N23.81} i {N26.48} {U}. Pytamy, które części są zadaszone.',
  'Listen fører de {N50.29} {U} i 2-AT-B som overbygd terrasse, mens tegningen viser to solterrasser på {N23.81} og {N26.48} {U}. Vi spør hvilke deler som er overbygd.',
  'Listan för de {N50.29} {U} i 2-AT-B som övertäckt terrass, medan ritningen visar två solterrasser på {N23.81} och {N26.48} {U}. Vi frågar vilka delar som är övertäckta.')
a('.trustDossier.cards[4][1]',
  'La lista de precios está fechada el 1 de noviembre de 2026, los planos en noviembre de 2025 y la memoria de calidades el 22 de diciembre de 2025. Las hojas de los planos llevan un sello BREEAM, pero ningún documento indica una certificación. El folleto menciona un sistema domótico que la memoria de calidades no describe; preguntamos qué incluye.',
  'La liste de prix est datée du 1er novembre 2026, les plans de novembre 2025 et le descriptif de qualité du 22 décembre 2025. Les feuilles des plans portent un logo BREEAM, mais aucun document n’indique de certification. La brochure mentionne un système domotique que le descriptif de qualité ne décrit pas ; nous demandons ce qu’il comprend.',
  'Die Preisliste ist vom 1. November 2026, die Pläne vom November 2025 und die Bau- und Ausstattungsbeschreibung vom 22. Dezember 2025. Die Planblätter tragen ein BREEAM-Zeichen, doch kein Dokument nennt eine Zertifizierung. Die Broschüre erwähnt ein Hausautomationssystem, das die Bau- und Ausstattungsbeschreibung nicht beschreibt; wir fragen, was es umfasst.',
  'Прайс-лист датирован 1 ноября 2026 года, планы — ноябрём 2025 года, спецификация качества — 22 декабря 2025 года. На листах планов стоит знак BREEAM, но ни один документ не говорит о сертификации. Брошюра упоминает систему «умный дом», которую спецификация качества не описывает; мы уточняем, что в неё входит.',
  'قائمة الأسعار مؤرخة في 1 نوفمبر 2026، والمخططات في نوفمبر 2025، ومواصفات الجودة في 22 ديسمبر 2025. وتحمل أوراق المخططات علامة BREEAM، لكن لا تذكر أي وثيقة شهادة. ويذكر الكتيّب نظامًا للأتمتة المنزلية لا تصفه مواصفات الجودة؛ ونسأل عمّا يشمله.',
  'De prijslijst is gedateerd 1 november 2026, de plannen november 2025 en de kwaliteitsspecificatie 22 december 2025. De planbladen dragen een BREEAM-logo, maar geen enkel document vermeldt een certificering. De brochure noemt een domoticasysteem dat de kwaliteitsspecificatie niet beschrijft; wij vragen wat het omvat.',
  'Cennik jest datowany na 1 listopada 2026 roku, rzuty na listopad 2025 roku, a specyfikacja jakości na 22 grudnia 2025 roku. Arkusze rzutów mają znak BREEAM, ale żaden dokument nie wspomina o certyfikacji. Broszura wspomina o systemie automatyki domowej, którego specyfikacja jakości nie opisuje; pytamy, co obejmuje.',
  'Prislisten er datert 1. november 2026, tegningene november 2025 og kvalitetsspesifikasjonen 22. desember 2025. Tegningsarkene har et BREEAM-merke, men ingen dokumenter oppgir en sertifisering. Brosjyren nevner et smarthussystem som kvalitetsspesifikasjonen ikke beskriver; vi spør hva det omfatter.',
  'Prislistan är daterad den 1 november 2026, ritningarna november 2025 och kvalitetsspecifikationen den 22 december 2025. Ritningsbladen bär ett BREEAM-märke, men inget dokument anger någon certifiering. Broschyren nämner ett smarthemsystem som kvalitetsspecifikationen inte beskriver; vi frågar vad det omfattar.')
a('.availability.headlineHtml',
  '16 viviendas en la <em>lista de precios</em>', '16 logements sur la <em>liste de prix</em>', '16 Wohnungen auf der <em>Preisliste</em>',
  '16 квартир в <em>прайс-листе</em>', '16 مسكنًا في <em>قائمة الأسعار</em>', '16 woningen op de <em>prijslijst</em>',
  '16 lokali w <em>cenniku</em>', '16 boliger i <em>prislisten</em>', '16 bostäder i <em>prislistan</em>')
a('.availability.copy',
  'La lista de precios del promotor del 1 de noviembre de 2026 recoge 16 viviendas, seis de dos dormitorios, nueve de tres y un ático de tres dormitorios. Disponibilidad y precios según la lista del 1 de noviembre de 2026, que se confirman antes de la reserva.',
  'La liste de prix du promoteur du 1er novembre 2026 compte 16 logements, six de deux chambres, neuf de trois et un penthouse de trois chambres. Disponibilité et prix selon la liste du 1er novembre 2026, confirmés avant la réservation.',
  'Die Preisliste des Bauträgers vom 1. November 2026 führt 16 Wohnungen, sechs mit zwei Schlafzimmern, neun mit drei und ein Penthouse mit drei Schlafzimmern. Verfügbarkeit und Preise laut Liste vom 1. November 2026, die vor der Reservierung bestätigt werden.',
  'Прайс-лист застройщика от 1 ноября 2026 года включает 16 квартир: шесть с двумя спальнями, девять с тремя и пентхаус с тремя спальнями. Наличие и цены — по списку от 1 ноября 2026 года, они подтверждаются до бронирования.',
  'تضم قائمة أسعار المطوّر بتاريخ 1 نوفمبر 2026 ستة عشر مسكنًا: ستة بغرفتي نوم، وتسعة بثلاث غرف نوم، وبنتهاوس بثلاث غرف نوم. التوفر والأسعار وفق القائمة بتاريخ 1 نوفمبر 2026، ويتم تأكيدهما قبل الحجز.',
  'De prijslijst van de ontwikkelaar van 1 november 2026 noemt 16 woningen, zes met twee slaapkamers, negen met drie en een penthouse met drie slaapkamers. Beschikbaarheid en prijzen volgens de lijst van 1 november 2026, bevestigd vóór de reservering.',
  'Cennik dewelopera z 1 listopada 2026 roku obejmuje 16 lokali: sześć z dwiema sypialniami, dziewięć z trzema i penthouse z trzema sypialniami. Dostępność i ceny według cennika z 1 listopada 2026 roku, potwierdzane przed rezerwacją.',
  'Utbyggerens prisliste fra 1. november 2026 har 16 boliger, seks med to soverom, ni med tre og en toppleilighet med tre soverom. Tilgjengelighet og priser etter listen fra 1. november 2026, bekreftet før reservasjon.',
  'Exploatörens prislista från den 1 november 2026 har 16 bostäder, sex med två sovrum, nio med tre och en takvåning med tre sovrum. Tillgänglighet och priser enligt listan från den 1 november 2026, bekräftade före bokning.')
a('.availability.checkedDate',
  '1 de noviembre de 2026', '1er novembre 2026', '1. November 2026', '1 ноября 2026 года', '1 نوفمبر 2026', '1 november 2026',
  '1 listopada 2026 r.', '1. november 2026', '1 november 2026')
a('.availability.sourceNote',
  'Los precios, dormitorios, baños, terrazas y plazas de garaje están transcritos de la lista de precios del promotor fechada el 1 de noviembre de 2026, que tiene 16 filas numeradas del 1 al 18; las filas 3 y 16 no figuran, y la lista no dice por qué. La lista no indica si el {T} está incluido; mostramos los precios sin {T}, como los dan las demás listas del promotor, y lo confirmamos por escrito. Cada vivienda incluye una plaza de garaje, dos en 1-3-C, 5-3-C y 2-AT-B, y un trastero. Las superficies interiores proceden de los planos del promotor de noviembre de 2025 (la de 3-1-C, que no tiene plano, de la lista); la terraza de 4-2-C mide {N18.82} {U} en su plano y {N18.67} {U} en la lista. La superficie construida de la lista, que incluye una parte de las zonas comunes, no se muestra aquí. La lista dice que no tiene valor contractual y que los precios pueden variar según el avance del proyecto y la disponibilidad.',
  'Les prix, chambres, salles de bains, terrasses et places de parking sont repris de la liste de prix du promoteur datée du 1er novembre 2026, qui compte 16 lignes numérotées de 1 à 18 ; les lignes 3 et 16 n’y figurent pas, et la liste ne dit pas pourquoi. La liste n’indique pas si la {T} est incluse ; nous présentons les prix hors {T}, comme les donnent les autres listes du promoteur, et le confirmons par écrit. Chaque logement comprend une place de parking, deux pour 1-3-C, 5-3-C et 2-AT-B, et un cellier. Les surfaces intérieures proviennent des plans du promoteur de novembre 2025 (celle de 3-1-C, qui n’a pas de plan, de la liste) ; la terrasse de 4-2-C mesure {N18.82} {U} sur son plan et {N18.67} {U} sur la liste. La surface construite de la liste, qui comprend une part des parties communes, n’est pas reprise ici. La liste indique qu’elle n’a aucune valeur contractuelle et que les prix peuvent varier selon l’avancement du projet et la disponibilité.',
  'Preise, Schlafzimmer, Bäder, Terrassen und Stellplätze stammen aus der Preisliste des Bauträgers vom 1. November 2026, die 16 Zeilen mit den Nummern 1 bis 18 hat; die Zeilen 3 und 16 fehlen, und die Liste sagt nicht, warum. Die Liste gibt nicht an, ob die {T} enthalten ist; wir zeigen die Preise vor {T}, wie die anderen Listen des Bauträgers sie angeben, und bestätigen es schriftlich. Zu jeder Wohnung gehören ein Stellplatz, bei 1-3-C, 5-3-C und 2-AT-B zwei, und ein Abstellraum. Die Innenflächen stammen aus den Plänen des Bauträgers vom November 2025 (bei 3-1-C, für die es keinen Plan gibt, aus der Liste); die Terrasse von 4-2-C misst laut Plan {N18.82} {U} und laut Liste {N18.67} {U}. Die bebaute Fläche der Liste, die einen Anteil an den Gemeinschaftsflächen enthält, wird hier nicht gezeigt. Die Liste gibt an, keinen Vertragswert zu haben und dass die Preise je nach Projektfortschritt und Verfügbarkeit schwanken können.',
  'Цены, спальни, ванные, террасы и машино-места взяты из прайс-листа застройщика от 1 ноября 2026 года, в котором 16 строк с номерами от 1 до 18; строк 3 и 16 нет, и список не объясняет почему. В списке не указано, включён ли {T}; мы показываем цены без {T}, как в других списках застройщика, и подтверждаем это письменно. К каждой квартире прилагаются машино-место, у 1-3-C, 5-3-C и 2-AT-B два, и кладовая. Внутренние площади взяты из планов застройщика за ноябрь 2025 года (для 3-1-C, у которой плана нет, — из списка); терраса 4-2-C на плане {N18.82} {U}, а в списке {N18.67} {U}. Площадь застройки из списка, включающая долю общих зон, здесь не приводится. В списке сказано, что он не имеет договорной силы, а цены могут меняться в зависимости от хода проекта и наличия.',
  'الأسعار وغرف النوم والحمامات والتراسات ومواقف السيارات منقولة من قائمة أسعار المطوّر المؤرخة في 1 نوفمبر 2026، وفيها 16 صفًا مرقّمة من 1 إلى 18؛ والصفان 3 و16 غير موجودين، ولا تذكر القائمة السبب. ولا تذكر القائمة ما إذا كانت {T} مشمولة؛ ونعرض الأسعار قبل {T} كما تذكرها قوائم المطوّر الأخرى، ونؤكد ذلك كتابيًا. ولكل مسكن موقف سيارة، واثنان للمساكن 1-3-C و5-3-C و2-AT-B، ومخزن. والمساحات الداخلية مأخوذة من مخططات المطوّر لشهر نوفمبر 2025 (ومساحة 3-1-C، الذي لا مخطط له، من القائمة)؛ ويبلغ تراس 4-2-C مساحة {N18.82} {U} في مخططه و{N18.67} {U} في القائمة. ولا تُعرض هنا المساحة المبنية الواردة في القائمة، التي تشمل حصة من المناطق المشتركة. وتذكر القائمة أنها ليست لها قيمة تعاقدية وأن الأسعار قد تتغير بحسب تقدّم المشروع والتوفر.',
  'Prijzen, slaapkamers, badkamers, terrassen en parkeerplaatsen zijn overgenomen uit de prijslijst van de ontwikkelaar van 1 november 2026, die 16 rijen heeft, genummerd van 1 tot 18; de rijen 3 en 16 ontbreken, en de lijst zegt niet waarom. De lijst vermeldt niet of de {T} is inbegrepen; wij tonen de prijzen exclusief {T}, zoals de andere lijsten van de ontwikkelaar ze geven, en bevestigen het schriftelijk. Bij elke woning horen een parkeerplaats, twee bij 1-3-C, 5-3-C en 2-AT-B, en een berging. De binnenoppervlaktes komen uit de plannen van de ontwikkelaar van november 2025 (die van 3-1-C, die geen plan heeft, uit de lijst); het terras van 4-2-C meet {N18.82} {U} op het plan en {N18.67} {U} op de lijst. De bebouwde oppervlakte van de lijst, die een aandeel in de gemeenschappelijke ruimtes omvat, wordt hier niet getoond. De lijst zegt dat ze geen contractuele waarde heeft en dat de prijzen kunnen variëren naargelang de voortgang van het project en de beschikbaarheid.',
  'Ceny, sypialnie, łazienki, tarasy i miejsca parkingowe przepisano z cennika dewelopera z 1 listopada 2026 roku, który ma 16 wierszy ponumerowanych od 1 do 18; wierszy 3 i 16 brak, a cennik nie wyjaśnia dlaczego. Cennik nie podaje, czy {T} jest wliczony; pokazujemy ceny bez {T}, tak jak podają je inne cenniki dewelopera, i potwierdzamy to na piśmie. Do każdego lokalu należy miejsce parkingowe, w 1-3-C, 5-3-C i 2-AT-B dwa, oraz komórka lokatorska. Powierzchnie wewnętrzne pochodzą z rzutów dewelopera z listopada 2025 roku (dla 3-1-C, który nie ma rzutu, z cennika); taras 4-2-C ma {N18.82} {U} na rzucie i {N18.67} {U} w cenniku. Powierzchnia zabudowy z cennika, obejmująca udział w częściach wspólnych, nie jest tu pokazana. Cennik zastrzega, że nie ma wartości umownej, a ceny mogą się zmieniać w zależności od postępu projektu i dostępności.',
  'Priser, soverom, bad, terrasser og parkeringsplasser er hentet fra utbyggerens prisliste datert 1. november 2026, som har 16 rader nummerert fra 1 til 18; radene 3 og 16 mangler, og listen sier ikke hvorfor. Listen oppgir ikke om {T} er inkludert; vi viser prisene før {T}, slik utbyggerens andre lister oppgir dem, og bekrefter det skriftlig. Hver bolig har en parkeringsplass, to for 1-3-C, 5-3-C og 2-AT-B, og en bod. De innvendige arealene er fra utbyggerens tegninger fra november 2025 (for 3-1-C, som ikke har tegning, fra listen); terrassen til 4-2-C er {N18.82} {U} på tegningen og {N18.67} {U} på listen. Listens bebygde areal, som omfatter en andel av fellesarealene, vises ikke her. Listen sier at den ikke har kontraktsverdi og at prisene kan variere med fremdriften i prosjektet og tilgjengeligheten.',
  'Priser, sovrum, badrum, terrasser och parkeringsplatser är hämtade från exploatörens prislista daterad den 1 november 2026, som har 16 rader numrerade från 1 till 18; raderna 3 och 16 saknas, och listan anger inte varför. Listan anger inte om {T} (spansk moms) ingår; vi visar priserna före {T}, så som exploatörens övriga listor anger dem, och bekräftar det skriftligt. Till varje bostad hör en parkeringsplats, två för 1-3-C, 5-3-C och 2-AT-B, och ett förråd. De invändiga ytorna kommer från exploatörens ritningar från november 2025 (för 3-1-C, som saknar ritning, från listan); terrassen i 4-2-C är {N18.82} {U} på ritningen och {N18.67} {U} på listan. Listans byggyta, som inkluderar en andel av de gemensamma ytorna, visas inte här. Listan anger att den saknar avtalsvärde och att priserna kan variera med projektets framsteg och tillgängligheten.')

# unit sizes: every size line is built from the same parts (interior, terrace)
PARTS = {
    'es': {'interior': '{v} {U} interiores', 'terrace': '{v} {U} de terraza'},
    'fr': {'interior': '{v} {U} intérieurs', 'terrace': '{v} {U} de terrasse'},
    'de': {'interior': '{v} {U} Innenfläche', 'terrace': '{v} {U} Terrasse'},
    'ru': {'interior': '{v} {U} внутри', 'terrace': 'терраса {v} {U}'},
    'ar': {'interior': '{v} {U} داخلية', 'terrace': '{v} {U} تراس'},
    'nl': {'interior': '{v} {U} binnen', 'terrace': '{v} {U} terras'},
    'pl': {'interior': '{v} {U} wnętrza', 'terrace': '{v} {U} tarasu'},
    'no': {'interior': '{v} {U} innvendig', 'terrace': '{v} {U} terrasse'},
    'sv': {'interior': '{v} {U} inomhus', 'terrace': '{v} {U} terrass'},
}
for u in proj['availability']['units']:
    vals = []
    for p in [p.strip() for p in u['size'].split(', ')]:
        m = re.fullmatch(r'([\d.]+) sqm (interior|terrace)', p)
        assert m, (u['reference'], p)
        vals.append((m.group(2), m.group(1)))
    out = {}
    for l in LOCS:
        sep = '، ' if l == 'ar' else ', '
        out[l] = sep.join(PARTS[l][k].replace('{v}', num(v, l)).replace('{U}', UNIT[l]) for k, v in vals)
    assert u['size'] not in T or T[u['size']] == out
    T[u['size']] = out

# ---- timeline, enquiry, FAQ, SEO -----------------------------------------------------------------

a('.timeline.items[1][2]',
  'Véala junto a los demás proyectos que tenemos entre Málaga y Marbella.',
  'Comparez-le avec les autres projets que nous proposons entre Malaga et Marbella.',
  'Sehen Sie es neben den anderen Projekten, die wir zwischen Málaga und Marbella anbieten.',
  'Сравните его с другими нашими проектами между Малагой и Марбельей.',
  'قارنه بالمشاريع الأخرى التي نعرضها بين مالقة وماربيا.',
  'Bekijk het naast de andere projecten die wij tussen Málaga en Marbella aanbieden.',
  'Proszę porównać go z innymi naszymi projektami między Malagą a Marbellą.',
  'Se det ved siden av de andre prosjektene vi har mellom Málaga og Marbella.',
  'Se det bredvid de andra projekten vi har mellan Málaga och Marbella.')
a('.enquiry.headlineHtml',
  'Pregunte por <em>Balcón del Pinar Residences</em>', 'Renseignez-vous sur <em>Balcón del Pinar Residences</em>', 'Fragen Sie nach <em>Balcón del Pinar Residences</em>',
  'Узнайте о <em>Balcón del Pinar Residences</em>', 'استفسر عن <em>Balcón del Pinar Residences</em>', 'Vraag naar <em>Balcón del Pinar Residences</em>',
  'Proszę zapytać o <em>Balcón del Pinar Residences</em>', 'Spør om <em>Balcón del Pinar Residences</em>', 'Fråga om <em>Balcón del Pinar Residences</em>')
a('.enquiry.message',
  'Hola Nueva Living, me gustaría recibir información sobre Balcón del Pinar Residences.',
  'Bonjour Nueva Living, je souhaiterais des informations sur Balcón del Pinar Residences.',
  'Hallo Nueva Living, ich hätte gern Informationen zu Balcón del Pinar Residences.',
  'Здравствуйте, Nueva Living! Я хотел бы получить информацию о Balcón del Pinar Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Balcón del Pinar Residences.',
  'Hallo Nueva Living, ik wil graag informatie over Balcón del Pinar Residences.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Balcón del Pinar Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Balcón del Pinar Residences.',
  'Hej Nueva Living, jag skulle vilja ha information om Balcón del Pinar Residences.')
put(get('.contact.whatsappMessage'), [T[get('.enquiry.message')][l] for l in LOCS])
a('.faq[0][1]',
  'La lista de precios del promotor del 1 de noviembre de 2026 recoge 16: seis apartamentos de dos dormitorios de {E425000} a {E485000}, nueve de tres dormitorios de {E493000} a {E601000} y un ático de tres dormitorios por {E802000}.',
  'La liste de prix du promoteur du 1er novembre 2026 en compte 16 : six appartements de deux chambres de {E425000} à {E485000}, neuf de trois chambres de {E493000} à {E601000} et un penthouse de trois chambres à {E802000}.',
  '16 stehen auf der Preisliste des Bauträgers vom 1. November 2026: sechs Wohnungen mit zwei Schlafzimmern von {E425000} bis {E485000}, neun mit drei Schlafzimmern von {E493000} bis {E601000} und ein Penthouse mit drei Schlafzimmern für {E802000}.',
  'В прайс-листе застройщика от 1 ноября 2026 года их 16: шесть квартир с двумя спальнями от {E425000} до {E485000}, девять с тремя спальнями от {E493000} до {E601000} и пентхаус с тремя спальнями за {E802000}.',
  'تضم قائمة أسعار المطوّر بتاريخ 1 نوفمبر 2026 ستة عشر مسكنًا: ست شقق بغرفتي نوم من {E425000} إلى {E485000}، وتسع بثلاث غرف نوم من {E493000} إلى {E601000}، وبنتهاوس بثلاث غرف نوم بسعر {E802000}.',
  'Er staan er 16 op de prijslijst van de ontwikkelaar van 1 november 2026: zes appartementen met twee slaapkamers van {E425000} tot {E485000}, negen met drie slaapkamers van {E493000} tot {E601000} en een penthouse met drie slaapkamers voor {E802000}.',
  'W cenniku dewelopera z 1 listopada 2026 roku jest ich 16: sześć mieszkań z dwiema sypialniami od {E425000} do {E485000}, dziewięć z trzema sypialniami od {E493000} do {E601000} i penthouse z trzema sypialniami za {E802000}.',
  'Utbyggerens prisliste fra 1. november 2026 har 16: seks leiligheter med to soverom fra {E425000} til {E485000}, ni med tre soverom fra {E493000} til {E601000} og en toppleilighet med tre soverom til {E802000}.',
  'Exploatörens prislista från den 1 november 2026 har 16: sex lägenheter med två sovrum från {E425000} till {E485000}, nio med tre sovrum från {E493000} till {E601000} och en takvåning med tre sovrum för {E802000}.')
a('.faq[1][1]',
  'La lista de precios no lo dice. Las demás listas de precios del promotor dan los precios sin {T}, así que esta página los muestra sin {T}. El {T} de una vivienda nueva es del 10 % y el impuesto de actos jurídicos documentados del {N1.20} %, y los gastos de notaría y registro van aparte. Confirmamos los impuestos y los gastos de compra por escrito.',
  'La liste de prix ne le dit pas. Les autres listes de prix du promoteur donnent les prix hors {T} ; cette page les présente donc hors {T}. La {T} sur un logement neuf est de 10 % et le droit de timbre de {N1.20} %, et les frais de notaire et d’enregistrement s’y ajoutent. Nous confirmons les taxes et les frais d’achat par écrit.',
  'Die Preisliste sagt es nicht. Die anderen Preislisten des Bauträgers nennen die Preise vor {T}, daher zeigt diese Seite sie vor {T}. Die {T} auf eine Neubauwohnung beträgt 10 % und die Stempelsteuer 1,20 %, hinzu kommen Notar- und Grundbuchkosten. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'В прайс-листе об этом не сказано. В других прайс-листах застройщика цены указаны без {T}, поэтому эта страница показывает их без {T}. {T} на новое жильё составляет 10 %, гербовый сбор {N1.20} %, а нотариальные и регистрационные расходы оплачиваются отдельно. Мы подтверждаем налоги и расходы на покупку письменно.',
  'لا تذكر قائمة الأسعار ذلك. أما قوائم أسعار المطوّر الأخرى فتذكر الأسعار قبل {T}، لذا تعرضها هذه الصفحة قبل {T}. وتبلغ {T} على المسكن الجديد 10% ورسم الدمغة {N1.20}%، وتُضاف إليهما رسوم الكاتب العدل والسجل العقاري. ونؤكد الضرائب وتكاليف الشراء كتابيًا.',
  'De prijslijst zegt het niet. De andere prijslijsten van de ontwikkelaar geven de prijzen exclusief {T}, dus deze pagina toont ze exclusief {T}. De {T} op een nieuwbouwwoning is 10% en de zegelbelasting {N1.20}%, en notaris- en kadasterkosten komen erbij. Wij bevestigen de belastingen en de aankoopkosten schriftelijk.',
  'Cennik tego nie podaje. Pozostałe cenniki dewelopera podają ceny bez {T}, dlatego ta strona pokazuje je bez {T}. {T} od nowego mieszkania wynosi 10%, opłata skarbowa {N1.20}%, a do tego dochodzą opłaty notarialne i za wpis do księgi wieczystej. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Prislisten sier det ikke. Utbyggerens andre prislister oppgir prisene før {T}, så denne siden viser dem før {T}. {T} på en ny bolig er 10 % og dokumentavgiften {N1.20} %, og notar- og tinglysingsgebyrer kommer i tillegg. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan anger det inte. Exploatörens övriga prislistor anger priserna före {T}, så den här sidan visar dem före {T}. {T} (spansk moms) på en nybyggd bostad är 10 % och stämpelskatten {N1.20} %, och notarie- och registreringsavgifter tillkommer. Vi bekräftar skatter och köpkostnader skriftligt.')
a('.faq[2][1]',
  'Sí, la lista de precios incluye una plaza de garaje y un trastero en cada precio, y dos plazas de garaje en 1-3-C, 5-3-C y 2-AT-B. Se los confirmamos por escrito para la vivienda que usted elija.',
  'Oui, la liste de prix inclut une place de parking et un cellier dans chaque prix, et deux places de parking pour 1-3-C, 5-3-C et 2-AT-B. Nous vous les confirmons par écrit pour le logement que vous choisissez.',
  'Ja, die Preisliste schließt in jeden Preis einen Stellplatz und einen Abstellraum ein, bei 1-3-C, 5-3-C und 2-AT-B zwei Stellplätze. Wir bestätigen sie Ihnen schriftlich für die Wohnung Ihrer Wahl.',
  'Да, прайс-лист включает в каждую цену машино-место и кладовую, а для 1-3-C, 5-3-C и 2-AT-B — два машино-места. Мы подтверждаем их письменно для выбранной вами квартиры.',
  'نعم، تدرج قائمة الأسعار موقف سيارة ومخزنًا في كل سعر، وموقفي سيارة للمساكن 1-3-C و5-3-C و2-AT-B. ونؤكدها لك كتابيًا للمسكن الذي تختاره.',
  'Ja, de prijslijst neemt in elke prijs een parkeerplaats en een berging op, en twee parkeerplaatsen bij 1-3-C, 5-3-C en 2-AT-B. Wij bevestigen ze schriftelijk voor de woning die u kiest.',
  'Tak, cennik wlicza w każdą cenę miejsce parkingowe i komórkę lokatorską, a w lokalach 1-3-C, 5-3-C i 2-AT-B dwa miejsca parkingowe. Potwierdzamy je na piśmie dla wybranego przez Państwa lokalu.',
  'Ja, prislisten inkluderer en parkeringsplass og en bod i hver pris, og to parkeringsplasser for 1-3-C, 5-3-C og 2-AT-B. Vi bekrefter dem skriftlig for boligen du velger.',
  'Ja, prislistan inkluderar en parkeringsplats och ett förråd i varje pris, och två parkeringsplatser för 1-3-C, 5-3-C och 2-AT-B. Vi bekräftar dem skriftligt för den bostad ni väljer.')
a('.faq[4][1]',
  'Para 15 de las 16. La vivienda 3-1-C no tiene, y se lo pedimos al promotor. Los planos son de noviembre de 2025 y sus superficies son provisionales hasta la licencia de obras.',
  'Pour 15 des 16. Le logement 3-1-C n’en a pas, et nous le demandons au promoteur. Les plans datent de novembre 2025 et leurs surfaces sont provisoires jusqu’au permis de construire.',
  'Für 15 der 16. Wohnung 3-1-C hat keinen, und wir fordern ihn beim Bauträger an. Die Pläne sind vom November 2025, und ihre Flächen sind bis zur Baugenehmigung vorläufig.',
  'Для 15 из 16. У квартиры 3-1-C плана нет, и мы запрашиваем его у застройщика. Планы датированы ноябрём 2025 года, и их площади предварительны до выдачи разрешения на строительство.',
  'لـ15 من أصل 16. لا مخطط للمسكن 3-1-C، ونطلبه من المطوّر. والمخططات مؤرخة في نوفمبر 2025، ومساحاتها مؤقتة حتى صدور رخصة البناء.',
  'Voor 15 van de 16. Woning 3-1-C heeft er geen, en wij vragen die op bij de ontwikkelaar. De plannen dateren van november 2025 en hun oppervlaktes zijn voorlopig tot de bouwvergunning.',
  'Dla 15 z 16. Lokal 3-1-C go nie ma, a my prosimy o niego dewelopera. Rzuty pochodzą z listopada 2025 roku, a ich powierzchnie są tymczasowe do czasu wydania pozwolenia na budowę.',
  'For 15 av de 16. Bolig 3-1-C har ingen, og vi ber utbyggeren om den. Tegningene er fra november 2025, og arealene er foreløpige frem til byggetillatelsen.',
  'För 15 av de 16. Bostad 3-1-C har ingen, och vi begär den av exploatören. Ritningarna är från november 2025 och ytorna är preliminära fram till bygglovet.')
a('.faq[6][1]',
  'Sí. La lista dice que no tiene valor contractual y que los precios pueden variar según el avance del proyecto y la disponibilidad. Reconfirmamos el precio antes de que usted reserve.',
  'Oui. La liste indique qu’elle n’a aucune valeur contractuelle et que les prix peuvent varier selon l’avancement du projet et la disponibilité. Nous reconfirmons le prix avant que vous ne réserviez.',
  'Ja. Die Liste gibt an, keinen Vertragswert zu haben und dass die Preise je nach Projektfortschritt und Verfügbarkeit schwanken können. Wir bestätigen den Preis erneut, bevor Sie reservieren.',
  'Да. В списке сказано, что он не имеет договорной силы, а цены могут меняться в зависимости от хода проекта и наличия. Мы заново подтверждаем цену до того, как вы забронируете.',
  'نعم. تذكر القائمة أنها ليست لها قيمة تعاقدية وأن الأسعار قد تتغير بحسب تقدّم المشروع والتوفر. ونعيد تأكيد السعر قبل أن تحجز.',
  'Ja. De lijst zegt dat ze geen contractuele waarde heeft en dat de prijzen kunnen variëren naargelang de voortgang van het project en de beschikbaarheid. Wij bevestigen de prijs opnieuw voordat u reserveert.',
  'Tak. Cennik zastrzega, że nie ma wartości umownej, a ceny mogą się zmieniać w zależności od postępu projektu i dostępności. Cenę potwierdzamy ponownie przed rezerwacją.',
  'Ja. Listen sier at den ikke har kontraktsverdi og at prisene kan variere med fremdriften i prosjektet og tilgjengeligheten. Vi bekrefter prisen på nytt før reservasjon.',
  'Ja. Listan anger att den saknar avtalsvärde och att priserna kan variera med projektets framsteg och tillgängligheten. Vi bekräftar priset på nytt före bokning.')
a('.seo.title',
  'Balcón del Pinar Residences - Apartamentos en Torremolinos', 'Balcón del Pinar Residences - Appartements à Torremolinos',
  'Balcón del Pinar Residences - Wohnungen in Torremolinos', 'Balcón del Pinar Residences - квартиры в Торремолиносе',
  'Balcón del Pinar Residences - شقق في توريمولينوس', 'Balcón del Pinar Residences - Appartementen in Torremolinos',
  'Balcón del Pinar Residences - apartamenty w Torremolinos', 'Balcón del Pinar Residences - leiligheter i Torremolinos',
  'Balcón del Pinar Residences - lägenheter i Torremolinos')
a('.seo.description',
  '16 apartamentos en lista en Torremolinos: viviendas de dos y tres dormitorios y un ático con terrazas, de {E425000} a {E802000}, más {T}.',
  '16 appartements listés à Torremolinos : logements de deux et trois chambres et un penthouse avec terrasses, de {E425000} à {E802000}, hors {T}.',
  '16 gelistete Wohnungen in Torremolinos: zwei und drei Schlafzimmer und ein Penthouse mit Terrassen, von {E425000} bis {E802000}, zuzüglich {T}.',
  '16 квартир из списка в Торремолиносе: две и три спальни и пентхаус с террасами, от {E425000} до {E802000}, плюс {T}.',
  '16 شقة مدرجة في توريمولينوس: مساكن بغرفتي نوم وثلاث غرف نوم وبنتهاوس مع تراسات، من {E425000} إلى {E802000}، زائد {T}.',
  '16 vermelde appartementen in Torremolinos: woningen met twee en drie slaapkamers en een penthouse met terrassen, van {E425000} tot {E802000}, plus {T}.',
  '16 apartamentów z cennika w Torremolinos: lokale z dwiema i trzema sypialniami oraz penthouse z tarasami, od {E425000} do {E802000}, plus {T}.',
  '16 oppførte leiligheter i Torremolinos: boliger med to og tre soverom og en toppleilighet med terrasser, fra {E425000} til {E802000}, pluss {T}.',
  '16 listade lägenheter i Torremolinos: bostäder med två och tre sovrum och en takvåning med terrasser, från {E425000} till {E802000}, plus {T}.')
a('.seo.h1',
  'Balcón del Pinar Residences: apartamentos en Torremolinos', 'Balcón del Pinar Residences : appartements à Torremolinos',
  'Balcón del Pinar Residences: Wohnungen in Torremolinos', 'Balcón del Pinar Residences: квартиры в Торремолиносе',
  'Balcón del Pinar Residences: شقق في توريمولينوس', 'Balcón del Pinar Residences: appartementen in Torremolinos',
  'Balcón del Pinar Residences: apartamenty w Torremolinos', 'Balcón del Pinar Residences: leiligheter i Torremolinos',
  'Balcón del Pinar Residences: lägenheter i Torremolinos')
a('.seo.h1Context',
  'Apartamentos en Torremolinos', 'Appartements à Torremolinos', 'Wohnungen in Torremolinos', 'Квартиры в Торремолиносе', 'شقق في توريمولينوس',
  'Appartementen in Torremolinos', 'Apartamenty w Torremolinos', 'Leiligheter i Torremolinos', 'Lägenheter i Torremolinos')

json.dump(T, open(f'{SP}/tr_b.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings to', f'{SP}/tr_b.json')
