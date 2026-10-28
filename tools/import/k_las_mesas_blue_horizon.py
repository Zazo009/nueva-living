# -*- coding: utf-8 -*-
"""Las Mesas Blue Horizon: the strings the translation memory did not have.

Same shape as k_olmo.py, keyed by the English string instead of by index, so a change to the
English copy cannot silently shift a translation onto the wrong sentence. Tokens: {E789000} money,
{N30.33} decimal number, {U} the area unit. Unit sizes, floor labels and plan captions are built from
per-locale templates at the foot of the file.
    python3 tools/import/k_las_mesas_blue_horizon.py <scratch dir>      (writes <dir>/tr_m.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
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


def a(en, *tr):
    assert len(tr) == 9, (en[:50], len(tr))
    assert en not in T, en[:50]
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    T[en] = {l: en for l in LOCS}


# identifiers: the name of the project and the developer's own home codes read the same everywhere
for s in ['Las Mesas Blue Horizon', 'Las Mesas <em>Blue Horizon</em>']:
    same(s)

# ---- description, SEO, hero, card -------------------------------------------------------------

a('9 of 34 two- and three-bedroom apartments at Las Mesas Blue Horizon, in Las Mesas, Estepona, with views of the sea, a communal pool, a gym, a spa, a coworking room and a cinema. No completion date is stated. From EUR 849,000 plus VAT.',
  '9 de 34 apartamentos de dos y tres dormitorios en Las Mesas Blue Horizon, en Las Mesas, Estepona, con vistas al mar, piscina comunitaria, gimnasio, spa, sala de coworking y sala de cine. No se indica fecha de entrega. Desde {E849000} más IVA.',
  '9 des 34 appartements de deux et trois chambres à Las Mesas Blue Horizon, à Las Mesas, Estepona, avec vue sur la mer, piscine commune, salle de sport, spa, espace de coworking et salle de cinéma. Aucune date de livraison n’est indiquée. À partir de {E849000} hors TVA.',
  '9 von 34 Wohnungen mit zwei und drei Schlafzimmern in Las Mesas Blue Horizon, in Las Mesas, Estepona, mit Meerblick, Gemeinschaftspool, Fitnessraum, Spa, Coworking-Raum und Kino. Ein Fertigstellungstermin ist nicht angegeben. Ab {E849000} zuzüglich MwSt.',
  '9 из 34 квартир с двумя и тремя спальнями в Las Mesas Blue Horizon, в Лас-Месас, Эстепона: вид на море, общий бассейн, тренажёрный зал, спа, коворкинг и кинозал. Срок сдачи не указан. От {E849000} без НДС.',
  '9 من أصل 34 شقة بغرفتي نوم وثلاث غرف نوم في Las Mesas Blue Horizon، في لاس ميساس، إستيبونا، بإطلالة على البحر، مع مسبح مشترك وصالة رياضية ومنتجع صحي وقاعة عمل مشترك وقاعة سينما. لم يُذكر موعد إنجاز. ابتداءً من {E849000} دون ضريبة القيمة المضافة.',
  '9 van de 34 appartementen met twee en drie slaapkamers in Las Mesas Blue Horizon, in Las Mesas, Estepona, met zeezicht, een gemeenschappelijk zwembad, een fitnessruimte, een spa, een coworkingruimte en een bioscoop. Er wordt geen opleveringsdatum genoemd. Vanaf {E849000} excl. btw.',
  '9 z 34 mieszkań z dwiema i trzema sypialniami w Las Mesas Blue Horizon, w Las Mesas, Estepona, z widokiem na morze, wspólnym basenem, siłownią, spa, salą coworkingową i kinem. Termin oddania nie jest podany. Od {E849000} plus VAT.',
  '9 av 34 leiligheter med to og tre soverom i Las Mesas Blue Horizon, i Las Mesas, Estepona, med utsikt over havet, felles basseng, treningsrom, spa, coworking-rom og kino. Ingen overleveringsdato er oppgitt. Fra {E849000} pluss mva.',
  '9 av 34 lägenheter med två och tre sovrum i Las Mesas Blue Horizon, i Las Mesas, Estepona, med havsutsikt, gemensam pool, gym, spa, coworking-rum och biograf. Inget tillträdesdatum anges. Från {E849000} plus IVA.')

a('9 of 34 two- and three-bedroom apartments at Las Mesas Blue Horizon, Estepona, with views of the sea, a pool, a gym, a spa and a cinema, from EUR 849,000 plus VAT.',
  '9 de 34 apartamentos de dos y tres dormitorios en Las Mesas Blue Horizon, Estepona, con vistas al mar, piscina, gimnasio, spa y sala de cine, desde {E849000} más IVA.',
  '9 des 34 appartements de deux et trois chambres à Las Mesas Blue Horizon, Estepona, avec vue sur la mer, piscine, salle de sport, spa et salle de cinéma, à partir de {E849000} hors TVA.',
  '9 von 34 Wohnungen mit zwei und drei Schlafzimmern in Las Mesas Blue Horizon, Estepona, mit Meerblick, Pool, Fitnessraum, Spa und Kino, ab {E849000} zuzüglich MwSt.',
  '9 из 34 квартир с двумя и тремя спальнями в Las Mesas Blue Horizon, Эстепона: вид на море, бассейн, тренажёрный зал, спа и кинозал, от {E849000} без НДС.',
  '9 من أصل 34 شقة بغرفتي نوم وثلاث غرف نوم في Las Mesas Blue Horizon، إستيبونا، بإطلالة على البحر، مع مسبح وصالة رياضية ومنتجع صحي وقاعة سينما، ابتداءً من {E849000} دون ضريبة القيمة المضافة.',
  '9 van de 34 appartementen met twee en drie slaapkamers in Las Mesas Blue Horizon, Estepona, met zeezicht, een zwembad, een fitnessruimte, een spa en een bioscoop, vanaf {E849000} excl. btw.',
  '9 z 34 mieszkań z dwiema i trzema sypialniami w Las Mesas Blue Horizon, Estepona, z widokiem na morze, basenem, siłownią, spa i kinem, od {E849000} plus VAT.',
  '9 av 34 leiligheter med to og tre soverom i Las Mesas Blue Horizon, Estepona, med utsikt over havet, basseng, treningsrom, spa og kino, fra {E849000} pluss mva.',
  '9 av 34 lägenheter med två och tre sovrum i Las Mesas Blue Horizon, Estepona, med havsutsikt, pool, gym, spa och biograf, från {E849000} plus IVA.')

a('Two- and three-bedroom apartments in Las Mesas, Estepona, with views of the sea, a pool, a gym and a spa, from EUR 849,000 plus VAT.',
  'Apartamentos de dos y tres dormitorios en Las Mesas, Estepona, con vistas al mar, piscina, gimnasio y spa, desde {E849000} más IVA.',
  'Appartements de deux et trois chambres à Las Mesas, Estepona, avec vue sur la mer, piscine, salle de sport et spa, à partir de {E849000} hors TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern in Las Mesas, Estepona, mit Meerblick, Pool, Fitnessraum und Spa, ab {E849000} zuzüglich MwSt.',
  'Квартиры с двумя и тремя спальнями в Лас-Месас, Эстепона: вид на море, бассейн, тренажёрный зал и спа, от {E849000} без НДС.',
  'شقق بغرفتي نوم وثلاث غرف نوم في لاس ميساس، إستيبونا، بإطلالة على البحر، مع مسبح وصالة رياضية ومنتجع صحي، ابتداءً من {E849000} دون ضريبة القيمة المضافة.',
  'Appartementen met twee en drie slaapkamers in Las Mesas, Estepona, met zeezicht, een zwembad, een fitnessruimte en een spa, vanaf {E849000} excl. btw.',
  'Mieszkania z dwiema i trzema sypialniami w Las Mesas, Estepona, z widokiem na morze, basenem, siłownią i spa, od {E849000} plus VAT.',
  'Leiligheter med to og tre soverom i Las Mesas, Estepona, med utsikt over havet, basseng, treningsrom og spa, fra {E849000} pluss mva.',
  'Lägenheter med två och tre sovrum i Las Mesas, Estepona, med havsutsikt, pool, gym och spa, från {E849000} plus IVA.')

a('Las Mesas, Estepona',
  'Las Mesas, Estepona', 'Las Mesas, Estepona', 'Las Mesas, Estepona', 'Лас-Месас, Эстепона', 'لاس ميساس، إستيبونا',
  'Las Mesas, Estepona', 'Las Mesas, Estepona', 'Las Mesas, Estepona', 'Las Mesas, Estepona')

a('From EUR 849,000 + VAT', 'Desde {E849000} + IVA', 'À partir de {E849000} + TVA', 'Ab {E849000} + MwSt.', 'От {E849000} + НДС',
  'ابتداءً من {E849000} + ضريبة القيمة المضافة', 'Vanaf {E849000} + btw', 'Od {E849000} + VAT', 'Fra {E849000} + mva.', 'Från {E849000} + IVA')
a('EUR 849,000 + VAT', '{E849000} + IVA', '{E849000} + TVA', '{E849000} + MwSt.', '{E849000} + НДС',
  '{E849000} + ضريبة القيمة المضافة', '{E849000} + btw', '{E849000} + VAT', '{E849000} + mva.', '{E849000} + IVA')
a('EUR 849,000 - EUR 1,245,000 + VAT', '{E849000} - {E1245000} + IVA', '{E849000} - {E1245000} + TVA', '{E849000} - {E1245000} + MwSt.',
  '{E849000} - {E1245000} + НДС', '{E849000} - {E1245000} + ضريبة القيمة المضافة', '{E849000} - {E1245000} + btw',
  '{E849000} - {E1245000} + VAT', '{E849000} - {E1245000} + mva.', '{E849000} - {E1245000} + IVA')

a('9 of 34 two- and three-bedroom apartments in Las Mesas, Estepona, with views of the sea, a communal pool, a gym and a spa, from EUR 849,000 + VAT.',
  '9 de 34 apartamentos de dos y tres dormitorios en Las Mesas, Estepona, con vistas al mar, piscina comunitaria, gimnasio y spa, desde {E849000} + IVA.',
  '9 des 34 appartements de deux et trois chambres à Las Mesas, Estepona, avec vue sur la mer, piscine commune, salle de sport et spa, à partir de {E849000} + TVA.',
  '9 von 34 Wohnungen mit zwei und drei Schlafzimmern in Las Mesas, Estepona, mit Meerblick, Gemeinschaftspool, Fitnessraum und Spa, ab {E849000} + MwSt.',
  '9 из 34 квартир с двумя и тремя спальнями в Лас-Месас, Эстепона: вид на море, общий бассейн, тренажёрный зал и спа, от {E849000} + НДС.',
  '9 من أصل 34 شقة بغرفتي نوم وثلاث غرف نوم في لاس ميساس، إستيبونا، بإطلالة على البحر، مع مسبح مشترك وصالة رياضية ومنتجع صحي، ابتداءً من {E849000} + ضريبة القيمة المضافة.',
  '9 van de 34 appartementen met twee en drie slaapkamers in Las Mesas, Estepona, met zeezicht, een gemeenschappelijk zwembad, een fitnessruimte en een spa, vanaf {E849000} + btw.',
  '9 z 34 mieszkań z dwiema i trzema sypialniami w Las Mesas, Estepona, z widokiem na morze, wspólnym basenem, siłownią i spa, od {E849000} + VAT.',
  '9 av 34 leiligheter med to og tre soverom i Las Mesas, Estepona, med utsikt over havet, felles basseng, treningsrom og spa, fra {E849000} + mva.',
  '9 av 34 lägenheter med två och tre sovrum i Las Mesas, Estepona, med havsutsikt, gemensam pool, gym och spa, från {E849000} + IVA.')

# ---- images: section images and the gallery -----------------------------------------------------

a('Computer-generated view of the terraced white block seen from the road, with palms and olive trees on the slope and the sea to the left',
  'Vista generada por ordenador del bloque blanco en terrazas visto desde la carretera, con palmeras y olivos en la ladera y el mar a la izquierda',
  'Vue générée par ordinateur de l’immeuble blanc à terrasses vu depuis la route, avec des palmiers et des oliviers sur la pente et la mer à gauche',
  'Computergenerierte Ansicht des weißen Terrassenblocks von der Straße aus, mit Palmen und Olivenbäumen am Hang und dem Meer links',
  'Компьютерная визуализация белого корпуса с террасами со стороны дороги: пальмы и оливковые деревья на склоне, слева море',
  'منظر مولَّد بالحاسوب للمبنى الأبيض ذي التراسات من جهة الطريق، مع نخيل وأشجار زيتون على المنحدر والبحر إلى اليسار',
  'Computergegenereerd beeld van het witte terrassenblok vanaf de weg, met palmen en olijfbomen op de helling en de zee links',
  'Wygenerowany komputerowo widok białego budynku z tarasami od strony drogi, z palmami i drzewami oliwnymi na zboczu oraz morzem po lewej',
  'Datagenerert bilde av den hvite terrasseblokken sett fra veien, med palmer og oliventrær i skråningen og havet til venstre',
  'Datorgenererad vy av det vita terrasshuset sett från vägen, med palmer och olivträd i sluttningen och havet till vänster')
a('Computer-generated view of the stepped block from the pool deck, with palms and a rooftop pergola',
  'Vista generada por ordenador del bloque escalonado desde la terraza de la piscina, con palmeras y una pérgola en la cubierta',
  'Vue générée par ordinateur de l’immeuble en gradins depuis la plage de la piscine, avec des palmiers et une pergola sur le toit',
  'Computergenerierte Ansicht des gestaffelten Blocks vom Poolbereich aus, mit Palmen und einer Pergola auf dem Dach',
  'Компьютерная визуализация корпуса с террасами-уступами со стороны бассейна: пальмы и пергола на крыше',
  'منظر مولَّد بالحاسوب للمبنى المتدرج من منصة المسبح، مع نخيل وبرغولا على السطح',
  'Computergegenereerd beeld van het getrapte blok vanaf het zwembaddek, met palmen en een pergola op het dak',
  'Wygenerowany komputerowo widok schodkowego budynku od strony basenu, z palmami i pergolą na dachu',
  'Datagenerert bilde av den trappede blokken sett fra bassengområdet, med palmer og en pergola på taket',
  'Datorgenererad vy av det trappstegsformade huset sett från poolområdet, med palmer och en pergola på taket')
a('The block from the pool deck', 'El bloque desde la terraza de la piscina', 'L’immeuble depuis la plage de la piscine',
  'Der Block vom Poolbereich aus', 'Корпус со стороны бассейна', 'المبنى من منصة المسبح', 'Het blok vanaf het zwembaddek',
  'Budynek od strony basenu', 'Blokken sett fra bassengområdet', 'Huset sett från poolområdet')
a('Computer-generated view of a bedroom with a double bed, a padded wall and a sliding glass door to the terrace',
  'Vista generada por ordenador de un dormitorio con cama doble, una pared tapizada y una puerta corredera de cristal a la terraza',
  'Vue générée par ordinateur d’une chambre avec un lit double, un mur capitonné et une porte coulissante vitrée donnant sur la terrasse',
  'Computergenerierte Ansicht eines Schlafzimmers mit Doppelbett, gepolsterter Wand und gläserner Schiebetür zur Terrasse',
  'Компьютерная визуализация спальни с двуспальной кроватью, мягкой стеновой панелью и стеклянной раздвижной дверью на террасу',
  'منظر مولَّد بالحاسوب لغرفة نوم بسرير مزدوج وجدار مبطّن وباب زجاجي منزلق إلى التراس',
  'Computergegenereerd beeld van een slaapkamer met een tweepersoonsbed, een gestoffeerde wand en een glazen schuifdeur naar het terras',
  'Wygenerowany komputerowo widok sypialni z łóżkiem małżeńskim, tapicerowaną ścianą i przesuwnymi szklanymi drzwiami na taras',
  'Datagenerert bilde av et soverom med dobbeltseng, en polstret vegg og en skyvedør i glass ut til terrassen',
  'Datorgenererad vy av ett sovrum med dubbelsäng, en stoppad vägg och en glasskjutdörr ut mot terrassen')
a('Computer-generated view of the communal pool with a timber deck, sunbeds and parasols, a palm tree and the terraces of the block on the right',
  'Vista generada por ordenador de la piscina comunitaria con solárium de madera, tumbonas y sombrillas, una palmera y las terrazas del bloque a la derecha',
  'Vue générée par ordinateur de la piscine commune avec sa plage en bois, des transats et des parasols, un palmier et les terrasses de l’immeuble à droite',
  'Computergenerierte Ansicht des Gemeinschaftspools mit Holzdeck, Sonnenliegen und Sonnenschirmen, einer Palme und den Terrassen des Blocks rechts',
  'Компьютерная визуализация общего бассейна с деревянным настилом, шезлонгами и зонтами, пальмой и террасами корпуса справа',
  'منظر مولَّد بالحاسوب للمسبح المشترك بمنصة خشبية ومقاعد تشمّس ومظلات ونخلة وتراسات المبنى إلى اليمين',
  'Computergegenereerd beeld van het gemeenschappelijk zwembad met een houten dek, ligbedden en parasols, een palmboom en rechts de terrassen van het blok',
  'Wygenerowany komputerowo widok wspólnego basenu z drewnianym pokładem, leżakami i parasolami, palmą oraz tarasami budynku po prawej',
  'Datagenerert bilde av det felles bassenget med trebrygge, solsenger og parasoller, en palme og terrassene på blokken til høyre',
  'Datorgenererad vy av den gemensamma poolen med trädäck, solstolar och parasoller, en palm och husets terrasser till höger')

a('Computer-generated views of the blocks, the pool, the shared areas and the interiors, and the floorplans of the nine homes that are listed.',
  'Vistas generadas por ordenador de los bloques, la piscina, las zonas comunes y los interiores, y los planos de las nueve viviendas que figuran.',
  'Vues générées par ordinateur des immeubles, de la piscine, des espaces communs et des intérieurs, et plans des neuf logements listés.',
  'Computergenerierte Ansichten der Blöcke, des Pools, der Gemeinschaftsbereiche und der Innenräume sowie die Grundrisse der neun aufgeführten Wohnungen.',
  'Компьютерные визуализации корпусов, бассейна, общих зон и интерьеров, а также планировки девяти квартир из списка.',
  'مناظر مولَّدة بالحاسوب للمباني والمسبح والمناطق المشتركة والتصاميم الداخلية، ومخططات المساكن التسعة المدرجة.',
  'Computergegenereerde beelden van de blokken, het zwembad, de gemeenschappelijke ruimten en de interieurs, en de plattegronden van de negen woningen die op de lijst staan.',
  'Wygenerowane komputerowo widoki budynków, basenu, części wspólnych i wnętrz oraz rzuty dziewięciu lokali z listy.',
  'Datagenererte bilder av blokkene, bassenget, fellesarealene og interiørene, og plantegningene for de ni boligene som er oppført.',
  'Datorgenererade vyer av husen, poolen, de gemensamma ytorna och interiörerna, samt planritningar för de nio bostäder som är listade.')
a('All the images are computer-generated illustrations, not photographs of the finished building, and the furniture and decoration in them are illustrative and not included. The floorplans are the developer’s sales plans: they are not contractual, the room names on them are in Spanish, and the terraces on them differ from the price list.',
  'Todas las imágenes son ilustraciones generadas por ordenador y no fotografías del edificio terminado, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los planos comerciales del promotor: no son contractuales, los nombres de las estancias están en español y las terrazas que figuran en ellos difieren de la lista de precios.',
  'Toutes les images sont des illustrations générées par ordinateur et non des photographies du bâtiment achevé ; le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont les plans commerciaux du promoteur : ils n’ont pas de valeur contractuelle, les noms des pièces y sont en espagnol et les terrasses qui y figurent diffèrent de la liste de prix.',
  'Alle Bilder sind computergenerierte Illustrationen und keine Fotos des fertigen Gebäudes; Möblierung und Dekoration darauf sind illustrativ und nicht enthalten. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen darauf sind auf Spanisch, und die Terrassen darauf weichen von der Preisliste ab.',
  'Все изображения — компьютерные иллюстрации, а не фотографии готового здания; мебель и декор на них носят иллюстративный характер и не входят в комплектацию. Планировки — коммерческие планы застройщика: они не имеют договорной силы, названия помещений на них даны на испанском языке, а площади террас на них отличаются от прайс-листа.',
  'جميع الصور رسوم توضيحية مولَّدة بالحاسوب وليست صورًا فوتوغرافية للمبنى بعد اكتماله، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. المخططات هي مخططات البيع الخاصة بالمطوّر: ليست ملزمة تعاقديًا، وأسماء الغرف عليها بالإسبانية، ومساحات التراسات عليها تختلف عن قائمة الأسعار.',
  'Alle beelden zijn computergegenereerde illustraties en geen foto’s van het voltooide gebouw, en het meubilair en de inrichting erop zijn illustratief en niet inbegrepen. De plattegronden zijn de verkoopplannen van de ontwikkelaar: ze zijn niet contractueel, de namen van de ruimten erop zijn in het Spaans en de terrassen erop wijken af van de prijslijst.',
  'Wszystkie obrazy to ilustracje wygenerowane komputerowo, a nie zdjęcia ukończonego budynku, a meble i wystrój na nich są poglądowe i nie wchodzą w cenę. Rzuty to plany sprzedażowe dewelopera: nie mają mocy umownej, nazwy pomieszczeń na nich są po hiszpańsku, a powierzchnie tarasów na nich różnią się od cennika.',
  'Alle bildene er datagenererte illustrasjoner og ikke fotografier av den ferdige bygningen, og møblene og innredningen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens salgsplaner: de er ikke kontraktsfestet, romnavnene på dem er på spansk, og terrassene på dem avviker fra prislisten.',
  'Alla bilder är datagenererade illustrationer och inte fotografier av den färdiga byggnaden, och möblerna och inredningen på dem är illustrativa och ingår inte. Planritningarna är exploatörens försäljningsritningar: de är inte avtalsbindande, rumsnamnen på dem är på spanska och terrasserna på dem avviker från prislistan.')

a('Computer-generated view of the block with long white curved terraces and dark slatted screens above olive trees, with lawn and pine trees to the left',
  'Vista generada por ordenador del bloque con largas terrazas blancas curvas y celosías oscuras de lamas sobre los olivos, con césped y pinos a la izquierda',
  'Vue générée par ordinateur de l’immeuble avec de longues terrasses blanches incurvées et des brise-soleil sombres à lames au-dessus des oliviers, avec de la pelouse et des pins à gauche',
  'Computergenerierte Ansicht des Blocks mit langen, geschwungenen weißen Terrassen und dunklen Lamellenblenden über Olivenbäumen, links Rasen und Pinien',
  'Компьютерная визуализация корпуса с длинными изогнутыми белыми террасами и тёмными реечными экранами над оливковыми деревьями; слева газон и сосны',
  'منظر مولَّد بالحاسوب للمبنى بتراسات بيضاء منحنية طويلة وستائر خشبية داكنة فوق أشجار الزيتون، مع عشب وأشجار صنوبر إلى اليسار',
  'Computergegenereerd beeld van het blok met lange, gebogen witte terrassen en donkere lamellenschermen boven olijfbomen, met links gazon en dennen',
  'Wygenerowany komputerowo widok budynku z długimi, zakrzywionymi białymi tarasami i ciemnymi żaluzjami lamelowymi nad drzewami oliwnymi, z trawnikiem i sosnami po lewej',
  'Datagenerert bilde av blokken med lange, buede hvite terrasser og mørke lamellskjermer over oliventrær, med gress og furuer til venstre',
  'Datorgenererad vy av huset med långa, böjda vita terrasser och mörka lamellskärmar ovanför olivträd, med gräsmatta och tallar till vänster')
a('The block above the olive trees', 'El bloque sobre los olivos', 'L’immeuble au-dessus des oliviers', 'Der Block über den Olivenbäumen',
  'Корпус над оливковыми деревьями', 'المبنى فوق أشجار الزيتون', 'Het blok boven de olijfbomen', 'Budynek nad drzewami oliwnymi',
  'Blokken over oliventrærne', 'Huset ovanför olivträden')
a('Computer-generated view of a corner of the block with a rooftop pergola above stepped terraces, and the communal pool in the foreground',
  'Vista generada por ordenador de una esquina del bloque con una pérgola en la cubierta sobre terrazas escalonadas, y la piscina comunitaria en primer plano',
  'Vue générée par ordinateur d’un angle de l’immeuble avec une pergola sur le toit au-dessus de terrasses en gradins, et la piscine commune au premier plan',
  'Computergenerierte Ansicht einer Ecke des Blocks mit einer Pergola auf dem Dach über gestaffelten Terrassen, im Vordergrund der Gemeinschaftspool',
  'Компьютерная визуализация угла корпуса с перголой на крыше над террасами-уступами; на переднем плане общий бассейн',
  'منظر مولَّد بالحاسوب لزاوية من المبنى مع برغولا على السطح فوق تراسات متدرجة، والمسبح المشترك في المقدمة',
  'Computergegenereerd beeld van een hoek van het blok met een pergola op het dak boven getrapte terrassen, met op de voorgrond het gemeenschappelijk zwembad',
  'Wygenerowany komputerowo widok narożnika budynku z pergolą na dachu nad schodkowymi tarasami, z wspólnym basenem na pierwszym planie',
  'Datagenerert bilde av et hjørne av blokken med en pergola på taket over trappede terrasser, og det felles bassenget i forgrunnen',
  'Datorgenererad vy av ett hörn av huset med en pergola på taket ovanför trappstegsformade terrasser och den gemensamma poolen i förgrunden')
a('A corner of the block above the pool', 'Una esquina del bloque sobre la piscina', 'Un angle de l’immeuble au-dessus de la piscine',
  'Eine Ecke des Blocks über dem Pool', 'Угол корпуса над бассейном', 'زاوية من المبنى فوق المسبح', 'Een hoek van het blok boven het zwembad',
  'Narożnik budynku nad basenem', 'Et hjørne av blokken over bassenget', 'Ett hörn av huset ovanför poolen')
a('Computer-generated view of the block above a stone retaining wall, with a stair and gate at the entrance, a street in front and mountains behind',
  'Vista generada por ordenador del bloque sobre un muro de contención de piedra, con una escalera y una cancela en la entrada, una calle delante y montañas detrás',
  'Vue générée par ordinateur de l’immeuble au-dessus d’un mur de soutènement en pierre, avec un escalier et un portail à l’entrée, une rue devant et des montagnes derrière',
  'Computergenerierte Ansicht des Blocks über einer Stützmauer aus Naturstein, mit Treppe und Tor am Eingang, davor eine Straße und dahinter Berge',
  'Компьютерная визуализация корпуса над каменной подпорной стеной: у входа лестница и ворота, впереди улица, позади горы',
  'منظر مولَّد بالحاسوب للمبنى فوق جدار استنادي حجري، مع درج وبوابة عند المدخل وشارع في المقدمة وجبال في الخلفية',
  'Computergegenereerd beeld van het blok boven een stenen keermuur, met een trap en een poort bij de ingang, een straat ervoor en bergen erachter',
  'Wygenerowany komputerowo widok budynku nad kamiennym murem oporowym, ze schodami i bramą przy wejściu, ulicą z przodu i górami w tle',
  'Datagenerert bilde av blokken over en støttemur i stein, med en trapp og en port ved inngangen, en gate foran og fjell bak',
  'Datorgenererad vy av huset ovanför en stödmur i sten, med en trappa och en port vid entrén, en gata framför och berg bakom')
a('The block above the entrance', 'El bloque sobre la entrada', 'L’immeuble au-dessus de l’entrée', 'Der Block über dem Eingang',
  'Корпус над входом', 'المبنى فوق المدخل', 'Het blok boven de ingang', 'Budynek nad wejściem', 'Blokken over inngangen', 'Huset ovanför entrén')
a('Computer-generated view of the block at dusk, lit from within, with street lamps and the mountains behind',
  'Vista generada por ordenador del bloque al anochecer, iluminado desde dentro, con farolas y las montañas detrás',
  'Vue générée par ordinateur de l’immeuble au crépuscule, éclairé de l’intérieur, avec des lampadaires et les montagnes derrière',
  'Computergenerierte Ansicht des Blocks in der Dämmerung, von innen beleuchtet, mit Straßenlaternen und den Bergen dahinter',
  'Компьютерная визуализация корпуса в сумерках с внутренней подсветкой: уличные фонари, позади горы',
  'منظر مولَّد بالحاسوب للمبنى عند الغسق، مضاءً من الداخل، مع أعمدة إنارة الشارع والجبال في الخلفية',
  'Computergegenereerd beeld van het blok in de schemering, van binnenuit verlicht, met straatlantaarns en de bergen erachter',
  'Wygenerowany komputerowo widok budynku o zmierzchu, oświetlonego od wewnątrz, z latarniami ulicznymi i górami w tle',
  'Datagenerert bilde av blokken i skumringen, opplyst innenfra, med gatelykter og fjellene bak',
  'Datorgenererad vy av huset i skymningen, upplyst inifrån, med gatlyktor och bergen bakom')
a('The block at dusk', 'El bloque al anochecer', 'L’immeuble au crépuscule', 'Der Block in der Dämmerung', 'Корпус в сумерках',
  'المبنى عند الغسق', 'Het blok in de schemering', 'Budynek o zmierzchu', 'Blokken i skumringen', 'Huset i skymningen')
a('Computer-generated view of the block from above, with rooftop pools and terraces on the upper levels and small pools and lawns at the foot',
  'Vista generada por ordenador del bloque desde arriba, con piscinas y terrazas en las plantas superiores y pequeñas piscinas y césped al pie',
  'Vue générée par ordinateur de l’immeuble vu d’en haut, avec des piscines et des terrasses sur les niveaux supérieurs et de petites piscines et de la pelouse au pied',
  'Computergenerierte Ansicht des Blocks von oben, mit Dachpools und Terrassen auf den oberen Ebenen sowie kleinen Pools und Rasenflächen am Fuß',
  'Компьютерная визуализация корпуса сверху: на верхних уровнях бассейны и террасы, у подножия небольшие бассейны и газоны',
  'منظر مولَّد بالحاسوب للمبنى من الأعلى، مع مسابح وتراسات على الطوابق العليا ومسابح صغيرة ومساحات عشبية عند الأسفل',
  'Computergegenereerd beeld van het blok van bovenaf, met daktuinen met zwembaden en terrassen op de bovenste lagen en kleine zwembaden en gazons aan de voet',
  'Wygenerowany komputerowo widok budynku z góry, z basenami i tarasami na wyższych poziomach oraz małymi basenami i trawnikami u podnóża',
  'Datagenerert bilde av blokken ovenfra, med takbasseng og terrasser på de øvre nivåene og små basseng og plener ved foten',
  'Datorgenererad vy av huset uppifrån, med takpooler och terrasser på de övre planen samt små pooler och gräsmattor vid foten')
a('Aerial view of the block', 'Vista aérea del bloque', 'Vue aérienne de l’immeuble', 'Luftansicht des Blocks', 'Корпус с высоты птичьего полёта',
  'منظر جوي للمبنى', 'Luchtbeeld van het blok', 'Widok budynku z lotu ptaka', 'Flyfoto av blokken', 'Flygvy av huset')
a('Computer-generated view of a ground-floor home with a covered terrace, a lawn with sun loungers and a small private pool',
  'Vista generada por ordenador de una vivienda en planta baja con terraza cubierta, césped con tumbonas y una pequeña piscina privada',
  'Vue générée par ordinateur d’un logement en rez-de-chaussée avec terrasse couverte, pelouse avec transats et petite piscine privée',
  'Computergenerierte Ansicht einer Erdgeschosswohnung mit überdachter Terrasse, Rasen mit Sonnenliegen und einem kleinen privaten Pool',
  'Компьютерная визуализация квартиры на первом этаже с крытой террасой, газоном с шезлонгами и небольшим частным бассейном',
  'منظر مولَّد بالحاسوب لمسكن في الطابق الأرضي بتراس مسقوف وعشب مع مقاعد تشمّس ومسبح خاص صغير',
  'Computergegenereerd beeld van een woning op de begane grond met een overdekt terras, een gazon met ligbedden en een klein privézwembad',
  'Wygenerowany komputerowo widok lokalu na parterze z zadaszonym tarasem, trawnikiem z leżakami i małym prywatnym basenem',
  'Datagenerert bilde av en bolig i første etasje med overdekket terrasse, en plen med solsenger og et lite privat basseng',
  'Datorgenererad vy av en bostad på bottenvåningen med övertäckt terrass, en gräsmatta med solstolar och en liten privat pool')
a('A ground-floor home with a garden and pool', 'Una vivienda en planta baja con jardín y piscina', 'Un logement en rez-de-chaussée avec jardin et piscine',
  'Eine Erdgeschosswohnung mit Garten und Pool', 'Квартира на первом этаже с садом и бассейном', 'مسكن في الطابق الأرضي بحديقة ومسبح',
  'Een woning op de begane grond met tuin en zwembad', 'Lokal na parterze z ogrodem i basenem', 'En bolig i første etasje med hage og basseng',
  'En bostad på bottenvåningen med trädgård och pool')
a('Computer-generated view of a rooftop terrace with a dining table, sun loungers, a small pool and the sea on the horizon',
  'Vista generada por ordenador de una terraza en la cubierta con mesa de comedor, tumbonas, una pequeña piscina y el mar en el horizonte',
  'Vue générée par ordinateur d’une terrasse sur le toit avec table à manger, transats, petite piscine et la mer à l’horizon',
  'Computergenerierte Ansicht einer Dachterrasse mit Esstisch, Sonnenliegen, einem kleinen Pool und dem Meer am Horizont',
  'Компьютерная визуализация террасы на крыше с обеденным столом, шезлонгами, небольшим бассейном и морем на горизонте',
  'منظر مولَّد بالحاسوب لتراس على السطح بطاولة طعام ومقاعد تشمّس ومسبح صغير والبحر عند الأفق',
  'Computergegenereerd beeld van een dakterras met een eettafel, ligbedden, een klein zwembad en de zee aan de horizon',
  'Wygenerowany komputerowo widok tarasu na dachu ze stołem jadalnym, leżakami, małym basenem i morzem na horyzoncie',
  'Datagenerert bilde av en takterrasse med spisebord, solsenger, et lite basseng og havet ved horisonten',
  'Datorgenererad vy av en takterrass med matbord, solstolar, en liten pool och havet vid horisonten')
a('A rooftop terrace with a pool', 'Una terraza en la cubierta con piscina', 'Une terrasse sur le toit avec piscine', 'Eine Dachterrasse mit Pool',
  'Терраса на крыше с бассейном', 'تراس على السطح بمسبح', 'Een dakterras met zwembad', 'Taras na dachu z basenem', 'En takterrasse med basseng', 'En takterrass med pool')
a('Computer-generated view of a stone-walled ramp and stair leading to the garage door, with a gym and a coworking room behind glass',
  'Vista generada por ordenador de una rampa y una escalera con muros de piedra que llevan a la puerta del garaje, con un gimnasio y una sala de coworking tras el cristal',
  'Vue générée par ordinateur d’une rampe et d’un escalier aux murs de pierre menant à la porte du garage, avec une salle de sport et un espace de coworking derrière une paroi vitrée',
  'Computergenerierte Ansicht einer Rampe und Treppe mit Natursteinmauern zum Garagentor, dahinter hinter Glas ein Fitnessraum und ein Coworking-Raum',
  'Компьютерная визуализация рампы и лестницы с каменными стенами, ведущих к гаражным воротам; за стеклом тренажёрный зал и коворкинг',
  'منظر مولَّد بالحاسوب لمنحدر ودرج بجدران حجرية يؤديان إلى باب المرآب، وخلف الزجاج صالة رياضية وقاعة عمل مشترك',
  'Computergegenereerd beeld van een helling en een trap met stenen muren naar de garagedeur, met achter glas een fitnessruimte en een coworkingruimte',
  'Wygenerowany komputerowo widok rampy i schodów z kamiennymi murami prowadzących do bramy garażu, z siłownią i salą coworkingową za szkłem',
  'Datagenerert bilde av en rampe og en trapp med steinmurer som fører til garasjeporten, med et treningsrom og et coworking-rom bak glass',
  'Datorgenererad vy av en ramp och en trappa med stenmurar som leder till garageporten, med ett gym och ett coworking-rum bakom glas')
a('The gym and the coworking room', 'El gimnasio y la sala de coworking', 'La salle de sport et l’espace de coworking',
  'Der Fitnessraum und der Coworking-Raum', 'Тренажёрный зал и коворкинг', 'الصالة الرياضية وقاعة العمل المشترك',
  'De fitnessruimte en de coworkingruimte', 'Siłownia i sala coworkingowa', 'Treningsrommet og coworking-rommet', 'Gymmet och coworking-rummet')
a('Computer-generated view of a gym with two cross-trainers, shelves of exercise balls and weights, and a glass wall',
  'Vista generada por ordenador de un gimnasio con dos elípticas, estanterías con pelotas de ejercicio y pesas, y una pared de cristal',
  'Vue générée par ordinateur d’une salle de sport avec deux vélos elliptiques, des étagères de ballons de fitness et de poids, et une paroi vitrée',
  'Computergenerierte Ansicht eines Fitnessraums mit zwei Crosstrainern, Regalen mit Gymnastikbällen und Gewichten sowie einer Glaswand',
  'Компьютерная визуализация тренажёрного зала с двумя эллиптическими тренажёрами, полками с фитболами и гантелями и стеклянной стеной',
  'منظر مولَّد بالحاسوب لصالة رياضية بجهازي تمرين إهليلجيين ورفوف عليها كرات تمرين وأوزان وجدار زجاجي',
  'Computergegenereerd beeld van een fitnessruimte met twee crosstrainers, planken met gymnastiekballen en gewichten en een glazen wand',
  'Wygenerowany komputerowo widok siłowni z dwoma orbitrekami, półkami z piłkami gimnastycznymi i ciężarkami oraz szklaną ścianą',
  'Datagenerert bilde av et treningsrom med to ellipsemaskiner, hyller med treningsballer og vekter og en glassvegg',
  'Datorgenererad vy av ett gym med två crosstrainers, hyllor med träningsbollar och vikter samt en glasvägg')
a('Computer-generated view of a spa lounge with sunbeds, two bowl armchairs and a narrow pool with water jets',
  'Vista generada por ordenador de una sala de relajación del spa con tumbonas, dos sillones en forma de cuenco y una piscina estrecha con chorros de agua',
  'Vue générée par ordinateur d’un salon de détente du spa avec des lits de repos, deux fauteuils en forme de vasque et un bassin étroit avec des jets d’eau',
  'Computergenerierte Ansicht eines Spa-Ruhebereichs mit Liegen, zwei schalenförmigen Sesseln und einem schmalen Becken mit Wasserdüsen',
  'Компьютерная визуализация зоны отдыха спа с шезлонгами, двумя креслами-чашами и узким бассейном с водяными форсунками',
  'منظر مولَّد بالحاسوب لصالة استرخاء في المنتجع الصحي بمقاعد استلقاء وكرسيين على شكل وعاء ومسبح ضيق بنوافير مياه',
  'Computergegenereerd beeld van een spa-relaxruimte met ligbedden, twee kuipvormige fauteuils en een smal bad met waterstralen',
  'Wygenerowany komputerowo widok strefy relaksu w spa z leżankami, dwoma fotelami w kształcie czaszy i wąskim basenem z dyszami wodnymi',
  'Datagenerert bilde av en hvilesone i spaet med solsenger, to skålformede lenestoler og et smalt basseng med vannstråler',
  'Datorgenererad vy av en vilozon i spat med solsängar, två skålformade fåtöljer och en smal pool med vattenstrålar')
a('The spa lounge', 'La sala de relajación del spa', 'Le salon de détente du spa', 'Der Ruhebereich des Spas', 'Зона отдыха спа',
  'صالة الاسترخاء في المنتجع الصحي', 'De relaxruimte van de spa', 'Strefa relaksu w spa', 'Hvilesonen i spaet', 'Vilozonen i spat')
a('Computer-generated view of the spa seen from above, with a pool, water jets, a round whirlpool and sunbeds',
  'Vista generada por ordenador del spa visto desde arriba, con una piscina, chorros de agua, un jacuzzi redondo y tumbonas',
  'Vue générée par ordinateur du spa vu d’en haut, avec un bassin, des jets d’eau, un jacuzzi rond et des lits de repos',
  'Computergenerierte Ansicht des Spas von oben, mit Becken, Wasserdüsen, rundem Whirlpool und Liegen',
  'Компьютерная визуализация спа сверху: бассейн, водяные форсунки, круглая джакузи и шезлонги',
  'منظر مولَّد بالحاسوب للمنتجع الصحي من الأعلى، مع مسبح ونوافير مياه وجاكوزي دائري ومقاعد استلقاء',
  'Computergegenereerd beeld van de spa van bovenaf, met een bad, waterstralen, een rond bubbelbad en ligbedden',
  'Wygenerowany komputerowo widok spa z góry, z basenem, dyszami wodnymi, okrągłym jacuzzi i leżankami',
  'Datagenerert bilde av spaet ovenfra, med et basseng, vannstråler, et rundt boblebad og solsenger',
  'Datorgenererad vy av spat uppifrån, med en pool, vattenstrålar, ett runt bubbelbad och solsängar')
a('The spa pool and whirlpool', 'La piscina y el jacuzzi del spa', 'Le bassin et le jacuzzi du spa', 'Das Spa-Becken und der Whirlpool',
  'Бассейн и джакузи спа', 'مسبح المنتجع الصحي والجاكوزي', 'Het spabad en het bubbelbad', 'Basen i jacuzzi w spa', 'Spabassenget og boblebadet', 'Spapoolen och bubbelbadet')
a('Computer-generated view of an open-plan living room, dining area and kitchen island with a sliding glass wall to the terrace',
  'Vista generada por ordenador de un salón abierto con zona de comedor e isla de cocina y una pared corredera de cristal hacia la terraza',
  'Vue générée par ordinateur d’un séjour ouvert avec coin repas et îlot de cuisine, et une paroi vitrée coulissante vers la terrasse',
  'Computergenerierte Ansicht eines offenen Wohnbereichs mit Essbereich und Kücheninsel sowie einer gläsernen Schiebewand zur Terrasse',
  'Компьютерная визуализация гостиной свободной планировки с обеденной зоной и кухонным островом и стеклянной раздвижной стеной на террасу',
  'منظر مولَّد بالحاسوب لغرفة معيشة مفتوحة مع منطقة طعام وجزيرة مطبخ وجدار زجاجي منزلق نحو التراس',
  'Computergegenereerd beeld van een open woonkamer met eetgedeelte en keukeneiland en een glazen schuifwand naar het terras',
  'Wygenerowany komputerowo widok otwartego salonu z jadalnią i wyspą kuchenną oraz przesuwną szklaną ścianą na taras',
  'Datagenerert bilde av en åpen stue med spiseplass og kjøkkenøy og en skyvevegg i glass ut til terrassen',
  'Datorgenererad vy av ett öppet vardagsrum med matplats och köksö samt en glasskjutvägg ut mot terrassen')
a('Computer-generated view of a dining table and a kitchen with a timber-slatted island and bar stools, next to a sliding glass wall',
  'Vista generada por ordenador de una mesa de comedor y una cocina con isla de listones de madera y taburetes, junto a una pared corredera de cristal',
  'Vue générée par ordinateur d’une table à manger et d’une cuisine avec un îlot habillé de lames de bois et des tabourets de bar, à côté d’une paroi vitrée coulissante',
  'Computergenerierte Ansicht eines Esstischs und einer Küche mit Holzlamellen-Insel und Barhockern neben einer gläsernen Schiebewand',
  'Компьютерная визуализация обеденного стола и кухни с островом, отделанным деревянными рейками, и барными стульями рядом со стеклянной раздвижной стеной',
  'منظر مولَّد بالحاسوب لطاولة طعام ومطبخ بجزيرة مكسوة بشرائح خشبية ومقاعد مرتفعة، بجوار جدار زجاجي منزلق',
  'Computergegenereerd beeld van een eettafel en een keuken met een eiland van houten latten en barkrukken, naast een glazen schuifwand',
  'Wygenerowany komputerowo widok stołu jadalnego i kuchni z wyspą wykończoną drewnianymi listwami i stołkami barowymi, obok przesuwnej szklanej ściany',
  'Datagenerert bilde av et spisebord og et kjøkken med en øy kledd i trelameller og barstoler, ved siden av en skyvevegg i glass',
  'Datorgenererad vy av ett matbord och ett kök med en köksö klädd i träribbor och barstolar, intill en glasskjutvägg')
a('The kitchen island and dining table', 'La isla de cocina y la mesa de comedor', 'L’îlot de cuisine et la table à manger',
  'Die Kücheninsel und der Esstisch', 'Кухонный остров и обеденный стол', 'جزيرة المطبخ وطاولة الطعام', 'Het keukeneiland en de eettafel',
  'Wyspa kuchenna i stół jadalny', 'Kjøkkenøya og spisebordet', 'Köksön och matbordet')
a('Computer-generated view of a terrace with seating and a dining table, opening onto a living room and kitchen, with the town and green land in the distance',
  'Vista generada por ordenador de una terraza con zona de estar y mesa de comedor, abierta a un salón y una cocina, con la ciudad y campo verde a lo lejos',
  'Vue générée par ordinateur d’une terrasse avec coin salon et table à manger, ouverte sur un séjour et une cuisine, avec la ville et des espaces verts au loin',
  'Computergenerierte Ansicht einer Terrasse mit Sitzbereich und Esstisch, die sich zu Wohnzimmer und Küche öffnet, in der Ferne die Stadt und grünes Land',
  'Компьютерная визуализация террасы с зоной отдыха и обеденным столом, открытой в гостиную и кухню; вдали город и зелёные просторы',
  'منظر مولَّد بالحاسوب لتراس بمقاعد وطاولة طعام يفتح على غرفة معيشة ومطبخ، وفي البعيد المدينة وأراضٍ خضراء',
  'Computergegenereerd beeld van een terras met zitgedeelte en eettafel, dat uitkomt op een woonkamer en keuken, met in de verte de stad en groen land',
  'Wygenerowany komputerowo widok tarasu z częścią wypoczynkową i stołem jadalnym, otwartego na salon i kuchnię, z miastem i zielonymi terenami w oddali',
  'Datagenerert bilde av en terrasse med sittegruppe og spisebord som åpner seg mot en stue og et kjøkken, med byen og grønt landskap i det fjerne',
  'Datorgenererad vy av en terrass med sittgrupp och matbord som öppnar sig mot ett vardagsrum och ett kök, med staden och grön mark i fjärran')
a('A terrace off the living room', 'Una terraza junto al salón', 'Une terrasse attenante au séjour', 'Eine Terrasse am Wohnzimmer',
  'Терраса рядом с гостиной', 'تراس ملاصق لغرفة المعيشة', 'Een terras aan de woonkamer', 'Taras przy salonie', 'En terrasse ved stuen', 'En terrass intill vardagsrummet')
a('Computer-generated view of a living room with a corner sofa, a dining table and a wide sliding glass wall towards the sea',
  'Vista generada por ordenador de un salón con sofá rinconero, mesa de comedor y una amplia pared corredera de cristal hacia el mar',
  'Vue générée par ordinateur d’un séjour avec canapé d’angle, table à manger et une large paroi vitrée coulissante vers la mer',
  'Computergenerierte Ansicht eines Wohnzimmers mit Ecksofa, Esstisch und einer breiten gläsernen Schiebewand zum Meer',
  'Компьютерная визуализация гостиной с угловым диваном, обеденным столом и широкой стеклянной раздвижной стеной в сторону моря',
  'منظر مولَّد بالحاسوب لغرفة معيشة بأريكة زاوية وطاولة طعام وجدار زجاجي منزلق واسع نحو البحر',
  'Computergegenereerd beeld van een woonkamer met een hoekbank, een eettafel en een brede glazen schuifwand richting de zee',
  'Wygenerowany komputerowo widok salonu z narożną sofą, stołem jadalnym i szeroką przesuwną szklaną ścianą w stronę morza',
  'Datagenerert bilde av en stue med hjørnesofa, spisebord og en bred skyvevegg i glass mot havet',
  'Datorgenererad vy av ett vardagsrum med hörnsoffa, matbord och en bred glasskjutvägg mot havet')
a('A bedroom opening onto the terrace', 'Un dormitorio que se abre a la terraza', 'Une chambre ouverte sur la terrasse',
  'Ein Schlafzimmer mit Zugang zur Terrasse', 'Спальня с выходом на террасу', 'غرفة نوم تفتح على التراس', 'Een slaapkamer die uitkomt op het terras',
  'Sypialnia z wyjściem na taras', 'Et soverom med utgang til terrassen', 'Ett sovrum med utgång till terrassen')
a('Computer-generated view of a bedroom with floor-to-ceiling glazing onto a terrace, with the town and the sea beyond',
  'Vista generada por ordenador de un dormitorio con cristaleras de suelo a techo hacia una terraza, con la ciudad y el mar al fondo',
  'Vue générée par ordinateur d’une chambre avec des baies vitrées du sol au plafond donnant sur une terrasse, avec la ville et la mer au-delà',
  'Computergenerierte Ansicht eines Schlafzimmers mit raumhoher Verglasung zur Terrasse, dahinter die Stadt und das Meer',
  'Компьютерная визуализация спальни с остеклением от пола до потолка на террасу; вдали город и море',
  'منظر مولَّد بالحاسوب لغرفة نوم بزجاج من الأرض إلى السقف نحو تراس، وخلفه المدينة والبحر',
  'Computergegenereerd beeld van een slaapkamer met vloer-tot-plafondbeglazing naar een terras, met daarachter de stad en de zee',
  'Wygenerowany komputerowo widok sypialni z przeszkleniem od podłogi do sufitu na taras, z miastem i morzem w tle',
  'Datagenerert bilde av et soverom med glass fra gulv til tak ut mot en terrasse, med byen og havet bak',
  'Datorgenererad vy av ett sovrum med glas från golv till tak ut mot en terrass, med staden och havet bakom')
a('A bedroom with a view of the sea', 'Un dormitorio con vistas al mar', 'Une chambre avec vue sur la mer', 'Ein Schlafzimmer mit Meerblick',
  'Спальня с видом на море', 'غرفة نوم بإطلالة على البحر', 'Een slaapkamer met uitzicht op zee', 'Sypialnia z widokiem na morze',
  'Et soverom med utsikt over havet', 'Ett sovrum med havsutsikt')
a('Computer-generated view of a bathroom with a countertop basin on a timber unit, a round backlit mirror and a glass-screened shower',
  'Vista generada por ordenador de un baño con lavabo sobre encimera en un mueble de madera, un espejo redondo retroiluminado y una ducha con mampara de cristal',
  'Vue générée par ordinateur d’une salle de bain avec une vasque posée sur un meuble en bois, un miroir rond rétroéclairé et une douche à paroi de verre',
  'Computergenerierte Ansicht eines Badezimmers mit Aufsatzwaschbecken auf einem Holzunterschrank, rundem hinterleuchtetem Spiegel und Dusche mit Glasabtrennung',
  'Компьютерная визуализация ванной комнаты с накладной раковиной на деревянной тумбе, круглым зеркалом с подсветкой и душем со стеклянной перегородкой',
  'منظر مولَّد بالحاسوب لحمام بحوض فوق سطح على خزانة خشبية ومرآة دائرية بإضاءة خلفية ودُش بحاجز زجاجي',
  'Computergegenereerd beeld van een badkamer met een opzetwastafel op een houten kast, een ronde verlichte spiegel en een douche met glazen wand',
  'Wygenerowany komputerowo widok łazienki z umywalką nablatową na drewnianej szafce, okrągłym podświetlanym lustrem i prysznicem ze szklaną ścianką',
  'Datagenerert bilde av et bad med en servant på benkeplate på en tremodul, et rundt baklyst speil og en dusj med glassvegg',
  'Datorgenererad vy av ett badrum med en bänkskiva med handfat på ett träskåp, en rund bakgrundsbelyst spegel och en dusch med glasvägg')
a('A bathroom with a glass-screened shower', 'Un baño con ducha con mampara de cristal', 'Une salle de bain avec douche à paroi de verre',
  'Ein Badezimmer mit Dusche und Glasabtrennung', 'Ванная комната со стеклянной душевой перегородкой', 'حمام بدُش بحاجز زجاجي',
  'Een badkamer met een douche met glazen wand', 'Łazienka z prysznicem ze szklaną ścianką', 'Et bad med dusj bak glassvegg', 'Ett badrum med dusch med glasvägg')
a('Computer-generated view of a bathroom with two countertop basins, two oval backlit mirrors and a glass-screened shower',
  'Vista generada por ordenador de un baño con dos lavabos sobre encimera, dos espejos ovalados retroiluminados y una ducha con mampara de cristal',
  'Vue générée par ordinateur d’une salle de bain avec deux vasques posées, deux miroirs ovales rétroéclairés et une douche à paroi de verre',
  'Computergenerierte Ansicht eines Badezimmers mit zwei Aufsatzwaschbecken, zwei ovalen hinterleuchteten Spiegeln und Dusche mit Glasabtrennung',
  'Компьютерная визуализация ванной комнаты с двумя накладными раковинами, двумя овальными зеркалами с подсветкой и душем со стеклянной перегородкой',
  'منظر مولَّد بالحاسوب لحمام بحوضين فوق سطح ومرآتين بيضاويتين بإضاءة خلفية ودُش بحاجز زجاجي',
  'Computergegenereerd beeld van een badkamer met twee opzetwastafels, twee ovale verlichte spiegels en een douche met glazen wand',
  'Wygenerowany komputerowo widok łazienki z dwiema umywalkami nablatowymi, dwoma owalnymi podświetlanymi lustrami i prysznicem ze szklaną ścianką',
  'Datagenerert bilde av et bad med to servanter på benkeplate, to ovale baklyste speil og en dusj med glassvegg',
  'Datorgenererad vy av ett badrum med två handfat på bänkskiva, två ovala bakgrundsbelysta speglar och en dusch med glasvägg')
a('A bathroom with two basins', 'Un baño con dos lavabos', 'Une salle de bain avec deux vasques', 'Ein Badezimmer mit zwei Waschbecken',
  'Ванная комната с двумя раковинами', 'حمام بحوضين', 'Een badkamer met twee wastafels', 'Łazienka z dwiema umywalkami', 'Et bad med to servanter', 'Ett badrum med två handfat')

# ---- overview, why, architecture -----------------------------------------------------------------

a('Nine homes <em>available</em>, in three blocks',
  'Nueve viviendas <em>disponibles</em>, en tres bloques', 'Neuf logements <em>disponibles</em>, dans trois immeubles',
  'Neun Wohnungen <em>verfügbar</em>, in drei Blöcken', 'Девять квартир <em>в продаже</em>, в трёх корпусах',
  'تسعة مساكن <em>متاحة</em>، في ثلاثة مبانٍ', 'Negen woningen <em>beschikbaar</em>, in drie blokken',
  'Dziewięć lokali <em>dostępnych</em>, w trzech budynkach', 'Ni boliger <em>tilgjengelige</em>, i tre blokker',
  'Nio bostäder <em>tillgängliga</em>, i tre hus')
a('Las Mesas Blue Horizon is a residential complex of three blocks in Las Mesas, Estepona, with two- and three-bedroom homes that all have two bathrooms. The developer’s dossier describes large terraces with panoramic views of the Mediterranean. It counts 36 homes, while its plans and the price list show 34, 20 with two bedrooms and 14 with three, and nine of those are listed with a price.',
  'Las Mesas Blue Horizon es un conjunto residencial de tres bloques en Las Mesas, Estepona, con viviendas de dos y tres dormitorios que tienen todas dos baños. El dosier del promotor describe grandes terrazas con vistas panorámicas al Mediterráneo. Cuenta 36 viviendas, mientras que sus planos y la lista de precios muestran 34, 20 de dos dormitorios y 14 de tres, y nueve de ellas figuran con precio.',
  'Las Mesas Blue Horizon est une résidence de trois immeubles à Las Mesas, Estepona, avec des logements de deux et trois chambres qui ont tous deux salles de bain. Le dossier du promoteur décrit de grandes terrasses avec vue panoramique sur la Méditerranée. Il compte 36 logements, alors que ses plans et la liste de prix en montrent 34, dont 20 de deux chambres et 14 de trois, et neuf figurent avec un prix.',
  'Las Mesas Blue Horizon ist eine Wohnanlage aus drei Blöcken in Las Mesas, Estepona, mit Wohnungen mit zwei und drei Schlafzimmern, die alle zwei Badezimmer haben. Die Broschüre des Bauträgers beschreibt große Terrassen mit Panoramablick auf das Mittelmeer. Sie nennt 36 Wohnungen, während ihre Pläne und die Preisliste 34 zeigen, 20 mit zwei und 14 mit drei Schlafzimmern, und neun davon sind mit Preis aufgeführt.',
  'Las Mesas Blue Horizon — жилой комплекс из трёх корпусов в Лас-Месас, Эстепона, с квартирами на две и три спальни, в каждой из которых по два санузла. В брошюре застройщика описаны просторные террасы с панорамным видом на Средиземное море. В ней указаны 36 квартир, тогда как в планах и прайс-листе их 34: 20 с двумя спальнями и 14 с тремя, и девять из них указаны с ценой.',
  'Las Mesas Blue Horizon مجمع سكني من ثلاثة مبانٍ في لاس ميساس، إستيبونا، بمساكن من غرفتي نوم وثلاث غرف نوم، في كل منها حمّامان. ويصف كتيّب المطوّر تراسات واسعة بإطلالة بانورامية على البحر المتوسط. ويذكر 36 مسكنًا، بينما تُظهر مخططاته وقائمة الأسعار 34 مسكنًا، منها 20 بغرفتي نوم و14 بثلاث غرف نوم، وتسعة منها مدرجة بالسعر.',
  'Las Mesas Blue Horizon is een woonwijk van drie blokken in Las Mesas, Estepona, met woningen met twee en drie slaapkamers die allemaal twee badkamers hebben. De brochure van de ontwikkelaar beschrijft grote terrassen met panoramisch uitzicht op de Middellandse Zee. Ze telt 36 woningen, terwijl de plattegronden en de prijslijst er 34 tonen, 20 met twee slaapkamers en 14 met drie, en negen daarvan staan met een prijs op de lijst.',
  'Las Mesas Blue Horizon to zespół mieszkaniowy z trzech budynków w Las Mesas, Estepona, z lokalami z dwiema i trzema sypialniami, z których wszystkie mają dwie łazienki. Broszura dewelopera opisuje duże tarasy z panoramicznym widokiem na Morze Śródziemne. Podaje 36 lokali, podczas gdy jej rzuty i cennik pokazują 34, w tym 20 z dwiema i 14 z trzema sypialniami, a dziewięć z nich ma podaną cenę.',
  'Las Mesas Blue Horizon er et boligkompleks med tre blokker i Las Mesas, Estepona, med boliger med to og tre soverom som alle har to bad. Utbyggerens brosjyre beskriver store terrasser med panoramautsikt over Middelhavet. Den oppgir 36 boliger, mens planene og prislisten viser 34, 20 med to soverom og 14 med tre, og ni av dem er oppført med pris.',
  'Las Mesas Blue Horizon är ett bostadsområde med tre hus i Las Mesas, Estepona, med bostäder med två och tre sovrum som alla har två badrum. Exploatörens broschyr beskriver stora terrasser med panoramautsikt över Medelhavet. Den anger 36 bostäder, medan planritningarna och prislistan visar 34, varav 20 med två sovrum och 14 med tre, och nio av dem är listade med pris.')
a('Residents share a communal pool with night lighting, landscaped areas, a gym, a spa, a coworking room and a cinema, and three basement levels hold the garage and the storage rooms. The developer’s documents give no completion date, and 25 of the 34 homes on the list are marked reserved.',
  'Los residentes comparten una piscina comunitaria con iluminación nocturna, zonas ajardinadas, un gimnasio, un spa, una sala de coworking y una sala de cine, y tres plantas de sótano alojan el garaje y los trasteros. Los documentos del promotor no dan fecha de entrega, y 25 de las 34 viviendas de la lista figuran como reservadas.',
  'Les résidents partagent une piscine commune avec éclairage nocturne, des espaces paysagers, une salle de sport, un spa, un espace de coworking et une salle de cinéma, et trois niveaux de sous-sol abritent le garage et les caves. Les documents du promoteur ne donnent aucune date de livraison, et 25 des 34 logements de la liste sont marqués comme réservés.',
  'Die Bewohner teilen sich einen Gemeinschaftspool mit Nachtbeleuchtung, begrünte Außenbereiche, einen Fitnessraum, ein Spa, einen Coworking-Raum und ein Kino; drei Untergeschosse nehmen die Garage und die Abstellräume auf. Die Unterlagen des Bauträgers nennen keinen Fertigstellungstermin, und 25 der 34 Wohnungen der Liste sind als reserviert gekennzeichnet.',
  'Жители пользуются общим бассейном с ночной подсветкой, благоустроенными территориями, тренажёрным залом, спа, коворкингом и кинозалом; на трёх подземных уровнях находятся гараж и кладовые. В документах застройщика нет срока сдачи, а 25 из 34 квартир списка помечены как зарезервированные.',
  'يتشارك السكان مسبحًا مشتركًا بإضاءة ليلية ومساحات مشجّرة وصالة رياضية ومنتجعًا صحيًا وقاعة عمل مشترك وقاعة سينما، وتضم ثلاثة مستويات سفلية المرآب وغرف التخزين. ولا تذكر وثائق المطوّر موعد إنجاز، و25 من أصل 34 مسكنًا في القائمة مُعلَّمة بأنها محجوزة.',
  'De bewoners delen een gemeenschappelijk zwembad met nachtverlichting, aangelegde buitenruimten, een fitnessruimte, een spa, een coworkingruimte en een bioscoop, en drie kelderlagen herbergen de garage en de bergingen. De documenten van de ontwikkelaar noemen geen opleveringsdatum, en 25 van de 34 woningen op de lijst zijn als gereserveerd aangemerkt.',
  'Mieszkańcy korzystają ze wspólnego basenu z oświetleniem nocnym, zagospodarowanych terenów zielonych, siłowni, spa, sali coworkingowej i kina, a na trzech poziomach podziemnych znajdują się garaż i komórki lokatorskie. Dokumenty dewelopera nie podają terminu oddania, a 25 z 34 lokali z listy oznaczono jako zarezerwowane.',
  'Beboerne deler et felles basseng med nattbelysning, opparbeidede uteområder, et treningsrom, et spa, et coworking-rom og et kino, og tre kjellernivåer rommer garasjen og bodene. Utbyggerens dokumenter oppgir ingen ferdigstillelsesdato, og 25 av de 34 boligene på listen er merket som reservert.',
  'De boende delar en gemensam pool med kvällsbelysning, planterade ytor, ett gym, ett spa, ett coworking-rum och en biograf, och tre källarplan rymmer garaget och förråden. Exploatörens dokument anger inget tillträdesdatum, och 25 av de 34 bostäderna på listan är markerade som reserverade.')
a('34 homes', '34 viviendas', '34 logements', '34 Wohnungen', '34 квартиры', '34 مسكنًا', '34 woningen', '34 lokale', '34 boliger', '34 bostäder')
a('9 homes', '9 viviendas', '9 logements', '9 Wohnungen', '9 квартир', '9 مساكن', '9 woningen', '9 lokali', '9 boliger', '9 bostäder')

a('Two- and three-bedroom apartments with large terraces, a spa, a gym and a cinema on site, in Las Mesas, Estepona.',
  'Apartamentos de dos y tres dormitorios con grandes terrazas, y con spa, gimnasio y sala de cine en el propio conjunto, en Las Mesas, Estepona.',
  'Appartements de deux et trois chambres avec de grandes terrasses, et un spa, une salle de sport et une salle de cinéma sur place, à Las Mesas, Estepona.',
  'Wohnungen mit zwei und drei Schlafzimmern und großen Terrassen, mit Spa, Fitnessraum und Kino in der Anlage, in Las Mesas, Estepona.',
  'Квартиры с двумя и тремя спальнями и просторными террасами, со спа, тренажёрным залом и кинозалом на территории, в Лас-Месас, Эстепона.',
  'شقق بغرفتي نوم وثلاث غرف نوم وتراسات واسعة، مع منتجع صحي وصالة رياضية وقاعة سينما في المجمع نفسه، في لاس ميساس، إستيبونا.',
  'Appartementen met twee en drie slaapkamers en grote terrassen, met een spa, een fitnessruimte en een bioscoop in het complex, in Las Mesas, Estepona.',
  'Mieszkania z dwiema i trzema sypialniami i dużymi tarasami, ze spa, siłownią i kinem na terenie osiedla, w Las Mesas, Estepona.',
  'Leiligheter med to og tre soverom og store terrasser, med spa, treningsrom og kino på stedet, i Las Mesas, Estepona.',
  'Lägenheter med två och tre sovrum och stora terrasser, med spa, gym och biograf i området, i Las Mesas, Estepona.')
a('Buyers who want a new two- or three-bedroom apartment in Estepona with a large terrace and wellness facilities on site, to live in or as a second home.',
  'Compradores que buscan un apartamento nuevo de dos o tres dormitorios en Estepona, con una gran terraza e instalaciones de bienestar en el propio conjunto, para vivir o como segunda residencia.',
  'Acheteurs qui recherchent un appartement neuf de deux ou trois chambres à Estepona, avec une grande terrasse et des équipements de bien-être sur place, pour y vivre ou comme résidence secondaire.',
  'Käufer, die eine neue Wohnung mit zwei oder drei Schlafzimmern in Estepona mit großer Terrasse und Wellnessangebot in der Anlage suchen, zum Wohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужна новая квартира с двумя или тремя спальнями в Эстепоне с просторной террасой и оздоровительными зонами на территории — для постоянного проживания или как вторая недвижимость.',
  'مشترون يريدون شقة جديدة بغرفتي نوم أو ثلاث غرف نوم في إستيبونا مع تراس واسع ومرافق للعناية بالجسم في المجمع نفسه، للسكن أو كمنزل ثانٍ.',
  'Kopers die een nieuw appartement met twee of drie slaapkamers in Estepona willen, met een groot terras en wellnessfaciliteiten in het complex, om in te wonen of als tweede woning.',
  'Kupujący, którzy szukają nowego mieszkania z dwiema lub trzema sypialniami w Esteponie, z dużym tarasem i zapleczem wellness na terenie osiedla, do zamieszkania lub jako drugi dom.',
  'Kjøpere som ønsker en ny leilighet med to eller tre soverom i Estepona med stor terrasse og velværeanlegg på stedet, til å bo i eller som feriebolig.',
  'Köpare som vill ha en ny lägenhet med två eller tre sovrum i Estepona med stor terrass och välmåendeanläggningar i området, att bo i eller som andrahem.')
a('A spa of 46.90 sqm, a gym, a coworking room, a cinema and a communal pool, with a lift and a garage with storage rooms on three basement levels, in a complex of only three blocks.',
  'Un spa de {N46.90} {U}, un gimnasio, una sala de coworking, una sala de cine y una piscina comunitaria, con ascensor y un garaje con trasteros en tres plantas de sótano, en un conjunto de solo tres bloques.',
  'Un spa de {N46.90} {U}, une salle de sport, un espace de coworking, une salle de cinéma et une piscine commune, avec ascenseur et un garage avec caves sur trois niveaux de sous-sol, dans une résidence de seulement trois immeubles.',
  'Ein Spa mit {N46.90} {U}, ein Fitnessraum, ein Coworking-Raum, ein Kino und ein Gemeinschaftspool, mit Aufzug und einer Garage mit Abstellräumen auf drei Untergeschossen, in einer Anlage mit nur drei Blöcken.',
  'Спа площадью {N46.90} {U}, тренажёрный зал, коворкинг, кинозал и общий бассейн, лифт и гараж с кладовыми на трёх подземных уровнях — в комплексе всего из трёх корпусов.',
  'منتجع صحي بمساحة {N46.90} {U}، وصالة رياضية، وقاعة عمل مشترك، وقاعة سينما، ومسبح مشترك، مع مصعد ومرآب وغرف تخزين على ثلاثة مستويات سفلية، في مجمع من ثلاثة مبانٍ فقط.',
  'Een spa van {N46.90} {U}, een fitnessruimte, een coworkingruimte, een bioscoop en een gemeenschappelijk zwembad, met een lift en een garage met bergingen op drie kelderlagen, in een complex van slechts drie blokken.',
  'Spa o powierzchni {N46.90} {U}, siłownia, sala coworkingowa, kino i wspólny basen, a do tego winda oraz garaż z komórkami lokatorskimi na trzech poziomach podziemnych, w osiedlu złożonym z zaledwie trzech budynków.',
  'Et spa på {N46.90} {U}, et treningsrom, et coworking-rom, et kino og et felles basseng, med heis og en garasje med boder på tre kjellernivåer, i et kompleks med bare tre blokker.',
  'Ett spa på {N46.90} {U}, ett gym, ett coworking-rum, en biograf och en gemensam pool, med hiss och ett garage med förråd på tre källarplan, i ett område med bara tre hus.')
a('The developer puts the site on the A-7 and the AP-7, 5 minutes from La Rada beach and 45 minutes from Málaga airport. It does not say whether the 5 minutes are on foot or by car.',
  'El promotor sitúa el conjunto junto a la A-7 y la AP-7, a 5 minutos de la playa de la Rada y a 45 minutos del aeropuerto de Málaga. No indica si los 5 minutos son a pie o en coche.',
  'Le promoteur place le site à proximité de l’A-7 et de l’AP-7, à 5 minutes de la plage de La Rada et à 45 minutes de l’aéroport de Málaga. Il ne précise pas si les 5 minutes se font à pied ou en voiture.',
  'Der Bauträger beschreibt die Lage an der A-7 und der AP-7, 5 Minuten vom Strand La Rada und 45 Minuten vom Flughafen Málaga entfernt. Er sagt nicht, ob die 5 Minuten zu Fuß oder mit dem Auto gemeint sind.',
  'Застройщик указывает, что комплекс находится у автомагистралей A-7 и AP-7, в 5 минутах от пляжа Ла-Рада и в 45 минутах от аэропорта Малаги. Не сказано, идёт ли речь о 5 минутах пешком или на машине.',
  'يضع المطوّر الموقع على الطريقين A-7 وAP-7، على بُعد 5 دقائق من شاطئ لا رادا و45 دقيقة من مطار ملقة. ولا يذكر ما إذا كانت الدقائق الخمس سيرًا على الأقدام أم بالسيارة.',
  'De ontwikkelaar plaatst de locatie aan de A-7 en de AP-7, op 5 minuten van het strand La Rada en op 45 minuten van de luchthaven van Málaga. Hij zegt niet of de 5 minuten te voet of met de auto zijn.',
  'Deweloper umiejscawia osiedle przy A-7 i AP-7, 5 minut od plaży La Rada i 45 minut od lotniska w Maladze. Nie podaje, czy te 5 minut to dojście pieszo, czy dojazd samochodem.',
  'Utbyggeren plasserer området ved A-7 og AP-7, 5 minutter fra stranden La Rada og 45 minutter fra Málaga lufthavn. Den sier ikke om de 5 minuttene er til fots eller med bil.',
  'Exploatören placerar området vid A-7 och AP-7, 5 minuter från stranden La Rada och 45 minuter från Málaga flygplats. Den anger inte om de 5 minuterna är till fots eller med bil.')
a('Twenty-five of the 34 homes on the list are marked reserved and nine have a price. The documents give no completion date, so we confirm the stage of the works and the date before any reservation.',
  'Veinticinco de las 34 viviendas de la lista figuran como reservadas y nueve tienen precio. Los documentos no dan fecha de entrega, así que confirmamos el estado de las obras y la fecha antes de cualquier reserva.',
  'Vingt-cinq des 34 logements de la liste sont marqués comme réservés et neuf ont un prix. Les documents ne donnent aucune date de livraison ; nous confirmons donc l’état d’avancement des travaux et la date avant toute réservation.',
  'Fünfundzwanzig der 34 Wohnungen der Liste sind als reserviert gekennzeichnet, neun haben einen Preis. Die Unterlagen nennen keinen Fertigstellungstermin, daher bestätigen wir den Baustand und den Termin vor jeder Reservierung.',
  'Двадцать пять из 34 квартир списка помечены как зарезервированные, у девяти указана цена. В документах нет срока сдачи, поэтому до любого бронирования мы подтверждаем стадию строительства и дату.',
  'خمسة وعشرون مسكنًا من أصل 34 في القائمة مُعلَّمة بأنها محجوزة، ولتسعة منها سعر. ولا تذكر الوثائق موعد إنجاز، لذلك نؤكد مرحلة الأعمال والموعد قبل أي حجز.',
  'Vijfentwintig van de 34 woningen op de lijst zijn als gereserveerd aangemerkt en negen hebben een prijs. De documenten noemen geen opleveringsdatum, dus we bevestigen de bouwstand en de datum vóór elke reservering.',
  'Dwadzieścia pięć z 34 lokali z listy oznaczono jako zarezerwowane, a dziewięć ma podaną cenę. Dokumenty nie podają terminu oddania, dlatego przed każdą rezerwacją potwierdzamy etap prac i datę.',
  'Tjuefem av de 34 boligene på listen er merket som reservert, og ni har en pris. Dokumentene oppgir ingen ferdigstillelsesdato, så vi bekrefter byggetrinnet og datoen før enhver reservasjon.',
  'Tjugofem av de 34 bostäderna på listan är markerade som reserverade och nio har ett pris. Dokumenten anger inget tillträdesdatum, så vi bekräftar byggstadiet och datumet före varje reservation.')

a('Stepped white terraces, <em>facing the sea</em>',
  'Terrazas blancas escalonadas, <em>frente al mar</em>', 'Terrasses blanches en gradins, <em>face à la mer</em>',
  'Gestaffelte weiße Terrassen, <em>zum Meer hin</em>', 'Белые террасы-уступы, <em>обращённые к морю</em>',
  'تراسات بيضاء متدرجة، <em>في مواجهة البحر</em>', 'Getrapte witte terrassen, <em>gericht op de zee</em>',
  'Schodkowe białe tarasy, <em>zwrócone ku morzu</em>', 'Trappede hvite terrasser, <em>vendt mot havet</em>',
  'Trappstegsformade vita terrasser, <em>vända mot havet</em>')
a('In the developer’s computer-generated images the blocks have long, curved white terraces stacked above dark slatted screens, with pergolas on the top levels and palms and olive trees around them. The dossier calls it a contemporary design facing the sea.',
  'En las imágenes generadas por ordenador del promotor, los bloques tienen largas terrazas blancas curvas apiladas sobre celosías oscuras de lamas, con pérgolas en los niveles superiores y palmeras y olivos alrededor. El dosier lo define como un diseño contemporáneo frente al mar.',
  'Dans les images générées par ordinateur du promoteur, les immeubles présentent de longues terrasses blanches incurvées superposées au-dessus de brise-soleil sombres à lames, avec des pergolas aux niveaux supérieurs et des palmiers et des oliviers autour. Le dossier parle d’un design contemporain face à la mer.',
  'In den computergenerierten Bildern des Bauträgers haben die Blöcke lange, geschwungene weiße Terrassen, die über dunklen Lamellenblenden aufeinandergestapelt sind, mit Pergolen auf den obersten Ebenen und Palmen und Olivenbäumen ringsum. Die Broschüre spricht von einem zeitgenössischen Design mit Blick zum Meer.',
  'На компьютерных изображениях застройщика корпуса имеют длинные изогнутые белые террасы, поставленные друг на друга над тёмными реечными экранами, с перголами на верхних уровнях и пальмами и оливковыми деревьями вокруг. В брошюре это названо современным дизайном, обращённым к морю.',
  'في صور المطوّر المولَّدة بالحاسوب تظهر المباني بتراسات بيضاء منحنية طويلة متراكبة فوق ستائر خشبية داكنة، مع برغولات في الطوابق العليا ونخيل وأشجار زيتون حولها. ويصف الكتيّب ذلك بأنه تصميم معاصر في مواجهة البحر.',
  'In de computergegenereerde beelden van de ontwikkelaar hebben de blokken lange, gebogen witte terrassen die boven donkere lamellenschermen op elkaar zijn gestapeld, met pergola’s op de bovenste lagen en palmen en olijfbomen eromheen. De brochure noemt het een eigentijds ontwerp met uitzicht op zee.',
  'Na wygenerowanych komputerowo obrazach dewelopera budynki mają długie, zakrzywione białe tarasy ułożone jeden nad drugim nad ciemnymi żaluzjami lamelowymi, z pergolami na najwyższych poziomach oraz palmami i drzewami oliwnymi wokół. Broszura nazywa to współczesnym designem zwróconym ku morzu.',
  'I utbyggerens datagenererte bilder har blokkene lange, buede hvite terrasser stablet over mørke lamellskjermer, med pergolaer på de øverste nivåene og palmer og oliventrær rundt. Brosjyren kaller det et moderne design vendt mot havet.',
  'På exploatörens datorgenererade bilder har husen långa, böjda vita terrasser som staplas ovanpå mörka lamellskärmar, med pergolor på de översta planen och palmer och olivträd runtomkring. Broschyren kallar det en modern design vänd mot havet.')
a('The ground-floor homes have a garden and a private pool and the penthouses a solarium with a pool on the roof, according to the dossier. The nine homes listed with a price are on the first to the fourth floor, each with a terrace.',
  'Las viviendas de planta baja tienen jardín y piscina privada y los áticos un solárium con piscina en la cubierta, según el dosier. Las nueve viviendas con precio están entre la primera y la cuarta planta, cada una con terraza.',
  'Les logements du rez-de-chaussée ont un jardin et une piscine privée et les penthouses un solarium avec piscine sur le toit, selon le dossier. Les neuf logements listés avec un prix se situent du premier au quatrième étage, chacun avec une terrasse.',
  'Die Erdgeschosswohnungen haben laut Broschüre einen Garten und einen privaten Pool, die Penthäuser ein Solarium mit Pool auf dem Dach. Die neun Wohnungen mit Preis liegen im ersten bis vierten Obergeschoss, jeweils mit Terrasse.',
  'По данным брошюры, у квартир на первом этаже есть сад и частный бассейн, а у пентхаусов — солярий с бассейном на крыше. Девять квартир с ценой расположены со второго по пятый этаж, и у каждой есть терраса.',
  'وفق الكتيّب، تتمتع مساكن الطابق الأرضي بحديقة ومسبح خاص، وتتمتع البنتهاوس بسولاريوم ومسبح على السطح. والمساكن التسعة المدرجة بالسعر تقع من الطابق الأول إلى الرابع، ولكل منها تراس.',
  'De woningen op de begane grond hebben volgens de brochure een tuin en een privézwembad en de penthouses een solarium met een zwembad op het dak. De negen woningen met een prijs liggen op de eerste tot en met de vierde verdieping, elk met een terras.',
  'Lokale na parterze mają według broszury ogród i prywatny basen, a penthouse’y solarium z basenem na dachu. Dziewięć lokali z podaną ceną znajduje się od pierwszego do czwartego piętra, każdy z tarasem.',
  'Boligene i første etasje har ifølge brosjyren hage og privat basseng, og toppleilighetene har solterrasse med basseng på taket. De ni boligene med pris ligger i andre til femte etasje, hver med terrasse.',
  'Bostäderna på bottenvåningen har enligt broschyren trädgård och privat pool, och takvåningarna har en solterrass med pool på taket. De nio bostäderna med pris ligger på första till fjärde våningen, var och en med terrass.')
a('Reinforced concrete to current regulations and the Technical Building Code, on foundations designed from the geotechnical study.',
  'Hormigón armado conforme a la normativa vigente y al Código Técnico de la Edificación, sobre una cimentación diseñada a partir del estudio geotécnico.',
  'Béton armé conforme à la réglementation en vigueur et au Code technique du bâtiment, sur des fondations conçues à partir de l’étude géotechnique.',
  'Stahlbeton nach den geltenden Vorschriften und dem Technischen Baukodex, auf Fundamenten, die aus dem geotechnischen Gutachten ausgelegt wurden.',
  'Железобетон по действующим нормам и Техническому строительному кодексу, на фундаменте, рассчитанном по геотехническому исследованию.',
  'خرسانة مسلحة وفق الأنظمة المعمول بها والكود الفني للبناء، على أساسات مصمَّمة بحسب الدراسة الجيوتقنية.',
  'Gewapend beton conform de geldende voorschriften en de Technische Bouwcode, op een fundering die is ontworpen op basis van het geotechnisch onderzoek.',
  'Żelbet zgodny z obowiązującymi przepisami i Technicznym Kodeksem Budowlanym, na fundamentach zaprojektowanych na podstawie badania geotechnicznego.',
  'Armert betong etter gjeldende forskrifter og den tekniske byggekoden, på fundamenter utformet etter den geotekniske undersøkelsen.',
  'Armerad betong enligt gällande föreskrifter och den tekniska byggkoden, på grundläggning utformad efter den geotekniska utredningen.')
a('Multilayer brickwork with interior insulation, an air chamber and a plasterboard lining, plastered and finished with lacquered aluminium panels and composite cladding.',
  'Fábrica de ladrillo multicapa con aislamiento interior, cámara de aire y trasdosado de yeso laminado, enfoscada y acabada con paneles de aluminio lacado y revestimiento composite.',
  'Maçonnerie de briques multicouche avec isolation intérieure, lame d’air et doublage en plaques de plâtre, enduite et finie avec des panneaux d’aluminium laqué et un revêtement composite.',
  'Mehrschichtiges Ziegelmauerwerk mit Innendämmung, Luftschicht und Gipskartonvorsatzschale, verputzt und mit lackierten Aluminiumpaneelen und Verbundverkleidung abgeschlossen.',
  'Многослойная кирпичная кладка с внутренним утеплением, воздушной прослойкой и гипсокартонной облицовкой; фасад оштукатурен и отделан панелями из лакированного алюминия и композитной облицовкой.',
  'بناء من الطوب متعدد الطبقات مع عزل داخلي وفراغ هوائي وبطانة من الجبس المقوى، مع لياسة وتشطيب بألواح من الألمنيوم المطلي وكسوة مركّبة.',
  'Meerlagig metselwerk met binnenisolatie, een spouw en een gipsplaatbekleding, gepleisterd en afgewerkt met gelakte aluminium panelen en composietbekleding.',
  'Wielowarstwowy mur z cegły z izolacją od wewnątrz, pustką powietrzną i okładziną z płyt gipsowo-kartonowych, otynkowany i wykończony panelami z lakierowanego aluminium oraz okładziną kompozytową.',
  'Flerlags teglmurverk med innvendig isolasjon, luftspalte og gipsplatekledning, pusset og ferdigstilt med lakkerte aluminiumspaneler og komposittkledning.',
  'Flerskiktsmurverk i tegel med invändig isolering, luftspalt och gipsskivor på insidan, putsat och avslutat med lackerade aluminiumpaneler och kompositbeklädnad.')
a('Dark lacquered aluminium frames with a thermal break, low-emission double glazing and sliding doors to the terraces.',
  'Carpintería de aluminio lacado oscuro con rotura de puente térmico, doble acristalamiento bajo emisivo y puertas correderas a las terrazas.',
  'Menuiseries en aluminium laqué foncé à rupture de pont thermique, double vitrage à faible émissivité et portes coulissantes donnant sur les terrasses.',
  'Dunkel lackierte Aluminiumrahmen mit thermischer Trennung, Wärmeschutz-Doppelverglasung und Schiebetüren zu den Terrassen.',
  'Тёмные рамы из лакированного алюминия с терморазрывом, двойное остекление с низкоэмиссионным покрытием и раздвижные двери на террасы.',
  'إطارات من الألمنيوم المطلي الداكن بفاصل حراري، وزجاج مزدوج منخفض الانبعاثية، وأبواب منزلقة إلى التراسات.',
  'Donker gelakte aluminium kozijnen met thermische onderbreking, dubbele beglazing met lage emissie en schuifdeuren naar de terrassen.',
  'Ciemne ramy z lakierowanego aluminium z przerwą termiczną, podwójne szyby niskoemisyjne i przesuwne drzwi na tarasy.',
  'Mørke lakkerte aluminiumsrammer med kuldebro-brudd, lavemisjons tolagsglass og skyvedører ut til terrassene.',
  'Mörka lackerade aluminiumkarmar med köldbrygga-brytare, lågemissions-tvåglasfönster och skjutdörrar ut mot terrasserna.')
a('Inverted flat roofs, waterproofed and insulated, in gravel where nobody walks and non-slip ceramic tiles where they are walkable.',
  'Cubiertas planas invertidas, impermeabilizadas y aisladas, con grava en las zonas no transitables y baldosas cerámicas antideslizantes en las transitables.',
  'Toitures-terrasses inversées, étanchées et isolées, en gravier là où l’on ne marche pas et en carreaux de céramique antidérapants là où elles sont praticables.',
  'Umkehrdächer, abgedichtet und gedämmt, mit Kies auf den nicht begehbaren Flächen und rutschfesten Keramikfliesen auf den begehbaren.',
  'Инверсионные плоские кровли с гидроизоляцией и утеплением: гравий на неэксплуатируемых участках и нескользящая керамическая плитка там, где по крыше можно ходить.',
  'أسطح مسطحة مقلوبة معزولة مائيًا وحراريًا، بالحصى في المناطق غير المخصصة للسير وببلاط خزفي مانع للانزلاق في المناطق التي يمكن السير عليها.',
  'Omgekeerde platte daken, waterdicht en geïsoleerd, met grind waar niemand loopt en antislip keramische tegels op de betreedbare delen.',
  'Dachy płaskie odwrócone, wodoszczelne i ocieplone, ze żwirem tam, gdzie nikt nie chodzi, i antypoślizgowymi płytkami ceramicznymi na częściach dostępnych.',
  'Omvendte flate tak, tettet og isolert, med grus der ingen går og sklisikre keramiske fliser der de kan betres.',
  'Omvända platta tak, tätade och isolerade, med grus där ingen går och halkfria keramikplattor där de är gångbara.')

# ---- quality specification -------------------------------------------------------------------------

a('Source: the quality specification in the developer’s dossier, which is undated. It says that the materials may change if the quality is not lowered, that the images are not contractual and that the furniture shown is not included.',
  'Fuente: la memoria de calidades del dosier del promotor, que no lleva fecha. Indica que los materiales pueden cambiar si la calidad no se reduce, que las imágenes no son contractuales y que el mobiliario que aparece no está incluido.',
  'Source : le descriptif des prestations du dossier du promoteur, qui n’est pas daté. Il précise que les matériaux peuvent changer si la qualité n’est pas diminuée, que les images n’ont pas de valeur contractuelle et que le mobilier représenté n’est pas inclus.',
  'Quelle: die Baubeschreibung in der Broschüre des Bauträgers, die kein Datum trägt. Sie besagt, dass sich die Materialien ändern können, solange die Qualität nicht gemindert wird, dass die Bilder nicht vertraglich bindend sind und dass die abgebildeten Möbel nicht enthalten sind.',
  'Источник: спецификация качества в брошюре застройщика, без даты. В ней сказано, что материалы могут быть изменены, если качество не снижается, что изображения не имеют договорной силы и что показанная мебель не входит в комплектацию.',
  'المصدر: مواصفات الجودة في كتيّب المطوّر، وهي غير مؤرّخة. وهي تنصّ على أن المواد قابلة للتغيير ما دامت الجودة لا تنخفض، وأن الصور غير ملزمة تعاقديًا، وأن الأثاث الظاهر غير مشمول.',
  'Bron: de kwaliteitsomschrijving in de brochure van de ontwikkelaar, die niet is gedateerd. Daarin staat dat de materialen kunnen wijzigen zolang de kwaliteit niet wordt verlaagd, dat de beelden niet contractueel zijn en dat het getoonde meubilair niet is inbegrepen.',
  'Źródło: opis standardu wykończenia w broszurze dewelopera, bez daty. Zastrzega on, że materiały mogą się zmienić, o ile nie obniży się ich jakości, że obrazy nie mają mocy umownej i że pokazane meble nie wchodzą w cenę.',
  'Kilde: kvalitetsbeskrivelsen i utbyggerens brosjyre, som er udatert. Den sier at materialene kan endres så lenge kvaliteten ikke reduseres, at bildene ikke er kontraktsfestet og at møblene som vises ikke er inkludert.',
  'Källa: kvalitetsbeskrivningen i exploatörens broschyr, som saknar datum. Den anger att materialen kan ändras om kvaliteten inte försämras, att bilderna inte är avtalsbindande och att de möbler som visas inte ingår.')
a('Plasterboard partitions on a metal frame with rock-wool insulation inside the home, water-repellent in the wet areas, and perforated brick between homes and next to the common areas, lined with plasterboard and thermal and acoustic insulation.',
  'Tabiquería de placas de yeso laminado sobre perfilería metálica con aislamiento de lana mineral dentro de la vivienda, hidrófuga en las zonas húmedas, y ladrillo perforado entre viviendas y junto a las zonas comunes, trasdosado con yeso laminado y aislamiento térmico y acústico.',
  'Cloisons en plaques de plâtre sur ossature métallique avec isolation en laine minérale à l’intérieur du logement, hydrofuges dans les pièces humides, et briques perforées entre les logements et le long des parties communes, doublées de plaques de plâtre et d’une isolation thermique et acoustique.',
  'Trennwände aus Gipskarton auf Metallprofilen mit Mineralwolldämmung innerhalb der Wohnung, in den Nassbereichen wasserabweisend, sowie Lochziegel zwischen den Wohnungen und zu den Gemeinschaftsbereichen, mit Gipskartonvorsatzschale und Wärme- und Schalldämmung.',
  'Перегородки из гипсокартона на металлическом каркасе с утеплением минеральной ватой внутри квартиры, влагостойкие в мокрых зонах, и стены из перфорированного кирпича между квартирами и со стороны общих зон, с гипсокартонной облицовкой и тепло- и звукоизоляцией.',
  'حواجز من الجبس المقوى على هيكل معدني مع عزل بالصوف المعدني داخل المسكن، مقاومة للرطوبة في المناطق الرطبة، وطوب مثقّب بين المساكن وبجوار المناطق المشتركة، مع بطانة من الجبس المقوى وعزل حراري وصوتي.',
  'Scheidingswanden van gipsplaten op een metalen frame met steenwolisolatie binnen de woning, waterafstotend in de natte ruimten, en geperforeerde baksteen tussen woningen en naast de gemeenschappelijke ruimten, bekleed met gipsplaten en thermische en akoestische isolatie.',
  'Ścianki działowe z płyt gipsowo-kartonowych na stelażu metalowym z izolacją z wełny mineralnej wewnątrz lokalu, wodoodporne w pomieszczeniach mokrych, oraz cegła perforowana między lokalami i przy częściach wspólnych, z okładziną gipsowo-kartonową oraz izolacją cieplną i akustyczną.',
  'Gipsplatevegger på stålskjelett med mineralullisolasjon inne i boligen, vannavstøtende i våtrommene, og perforert murstein mellom boligene og mot fellesarealene, kledd med gipsplater og termisk og akustisk isolasjon.',
  'Gipsskivor på stålreglar med mineralullsisolering inne i bostaden, fuktresistenta i våtrummen, och hålsten mellan bostäderna och mot de gemensamma ytorna, med gipsskivor på insidan och värme- och ljudisolering.')
a('Double glazing with a dry air chamber and a low-emission coating, sliding doors from the living rooms and bedrooms to the terraces, and a hidden floor track in the living-dining room and the kitchen so that they flow into the outdoors.',
  'Doble acristalamiento con cámara de aire deshidratado y tratamiento bajo emisivo, puertas correderas desde los salones y los dormitorios a las terrazas, y un carril oculto en el suelo en el salón-comedor y la cocina para que se prolonguen hacia el exterior.',
  'Double vitrage avec lame d’air déshydratée et traitement à faible émissivité, portes coulissantes depuis les séjours et les chambres vers les terrasses, et rail encastré dans le sol du séjour-salle à manger et de la cuisine pour qu’ils se prolongent vers l’extérieur.',
  'Doppelverglasung mit trockener Luftkammer und Wärmeschutzbeschichtung, Schiebetüren von den Wohnzimmern und Schlafzimmern zu den Terrassen und eine im Boden versenkte Schiene im Wohn-Essbereich und in der Küche, damit diese nahtlos in den Außenbereich übergehen.',
  'Двойное остекление с осушенной воздушной камерой и низкоэмиссионным покрытием, раздвижные двери из гостиных и спален на террасы, а в гостиной-столовой и на кухне — скрытый напольный профиль, чтобы пространство плавно переходило наружу.',
  'زجاج مزدوج بفراغ هوائي مجفَّف وطلاء منخفض الانبعاثية، وأبواب منزلقة من غرف المعيشة وغرف النوم إلى التراسات، ومسار مخفي في الأرضية في غرفة المعيشة والطعام والمطبخ ليمتدّا نحو الخارج بسلاسة.',
  'Dubbele beglazing met een droge luchtspouw en een coating met lage emissie, schuifdeuren van de woonkamers en slaapkamers naar de terrassen, en een verborgen vloerrail in de woon-eetkamer en de keuken zodat die overlopen in de buitenruimte.',
  'Podwójne szyby z osuszoną komorą powietrzną i powłoką niskoemisyjną, przesuwne drzwi z salonów i sypialni na tarasy oraz ukryta w podłodze prowadnica w salonie z jadalnią i w kuchni, dzięki której te pomieszczenia płynnie łączą się z zewnętrzem.',
  'Tolagsglass med tørr luftspalte og lavemisjonsbelegg, skyvedører fra stuene og soverommene ut til terrassene, og et skjult gulvspor i stuen med spiseplass og i kjøkkenet slik at de går sømløst over i uterommet.',
  'Tvåglasfönster med torr luftspalt och lågemissionsbeläggning, skjutdörrar från vardagsrum och sovrum ut till terrasserna, och ett dolt golvspår i vardagsrummet med matplats och i köket så att de flyter ut mot utomhusytan.')
a('Motorised roller blinds that darken the bedrooms and the living room, with a push button in every room.',
  'Estores enrollables motorizados que oscurecen los dormitorios y el salón, con pulsador en cada estancia.',
  'Stores enrouleurs motorisés qui occultent les chambres et le séjour, avec un bouton-poussoir dans chaque pièce.',
  'Motorisierte Rollos, die die Schlafzimmer und das Wohnzimmer abdunkeln, mit Taster in jedem Raum.',
  'Моторизованные рулонные шторы, затемняющие спальни и гостиную, с кнопкой управления в каждой комнате.',
  'ستائر دوّارة بمحرك تُظلم غرف النوم وغرفة المعيشة، مع زر تشغيل في كل غرفة.',
  'Gemotoriseerde rolgordijnen die de slaapkamers en de woonkamer verduisteren, met een drukknop in elke ruimte.',
  'Zmotoryzowane rolety zaciemniające sypialnie i salon, z przyciskiem w każdym pomieszczeniu.',
  'Motoriserte rullegardiner som mørklegger soverommene og stuen, med trykknapp i hvert rom.',
  'Motordrivna rullgardiner som mörklägger sovrummen och vardagsrummet, med tryckknapp i varje rum.')
a('A metal-reinforced front door with a three-point security lock and a smart lock, floor-to-ceiling interior doors in a minimalist design lacquered in colour, and built-in modular wardrobes lined inside, with a luggage shelf and a hanging rail. Handles and fittings in black or chrome.',
  'Puerta de entrada blindada con cerradura de seguridad de tres puntos de anclaje y cerradura inteligente, puertas interiores de suelo a techo de diseño minimalista lacadas en color, y armarios modulares empotrados con interior revestido, balda maletero y barra de colgar. Herrajes y manillas en negro o cromados.',
  'Porte d’entrée blindée avec serrure de sécurité à trois points d’ancrage et serrure intelligente, portes intérieures du sol au plafond au design minimaliste laquées en couleur, et placards modulaires encastrés avec intérieur habillé, tablette à valises et barre de penderie. Poignées et quincaillerie noires ou chromées.',
  'Eine metallverstärkte Wohnungseingangstür mit Dreipunkt-Sicherheitsschloss und Smart-Lock, raumhohe Innentüren in minimalistischem Design, farbig lackiert, sowie eingebaute modulare Kleiderschränke mit ausgekleidetem Innenraum, Kofferablage und Kleiderstange. Griffe und Beschläge in Schwarz oder Chrom.',
  'Входная дверь с металлическим армированием, трёхточечным замком безопасности и умным замком, межкомнатные двери от пола до потолка в минималистичном дизайне, окрашенные в цвет, и встроенные модульные шкафы с обшитым внутри корпусом, полкой для чемоданов и штангой для одежды. Ручки и фурнитура чёрные или хромированные.',
  'باب دخول معزَّز بالمعدن بقفل أمان بثلاث نقاط تثبيت وقفل ذكي، وأبواب داخلية من الأرض إلى السقف بتصميم بسيط مطلية بلون، وخزائن مدمجة معيارية ببطانة داخلية ورف للحقائب وقضيب تعليق. المقابض والإكسسوارات باللون الأسود أو الكروم.',
  'Een metaalversterkte voordeur met een veiligheidsslot met drie vergrendelpunten en een smartlock, vloer-tot-plafond binnendeuren in een minimalistisch ontwerp, in kleur gelakt, en ingebouwde modulaire kledingkasten met beklede binnenkant, een kofferplank en een kleerstang. Grepen en beslag in zwart of chroom.',
  'Drzwi wejściowe wzmocnione metalem z zamkiem bezpieczeństwa o trzech punktach ryglowania i zamkiem inteligentnym, drzwi wewnętrzne od podłogi do sufitu w minimalistycznym designie, lakierowane na kolor, oraz zabudowane szafy modułowe z wyłożonym wnętrzem, półką na walizki i drążkiem na ubrania. Klamki i okucia w kolorze czarnym lub chromowanym.',
  'En metallforsterket inngangsdør med sikkerhetslås med tre låsepunkter og smartlås, innerdører fra gulv til tak i minimalistisk design, lakkert i farge, og innebygde modulgarderober med kledd innside, bagasjehylle og kleshenger. Håndtak og beslag i sort eller krom.',
  'En metallförstärkt ytterdörr med säkerhetslås med tre låspunkter och smartlås, innerdörrar från golv till tak i minimalistisk design, lackerade i färg, och inbyggda modulgarderober med klädd insida, resväskshylla och klädstång. Handtag och beslag i svart eller krom.')
a('Floors of rectified porcelain stoneware in 120 x 120 cm format or microcement, with a white wood skirting to match the woodwork, and non-slip rectified porcelain stoneware on the terraces.',
  'Suelos de gres porcelánico rectificado en formato 120 x 120 cm o de microcemento, con rodapié de madera blanco a juego con la carpintería, y gres porcelánico rectificado antideslizante en las terrazas.',
  'Sols en grès cérame rectifié au format 120 x 120 cm ou en microciment, avec plinthe en bois blanc assortie aux menuiseries, et grès cérame rectifié antidérapant sur les terrasses.',
  'Böden aus rektifiziertem Feinsteinzeug im Format 120 x 120 cm oder aus Mikrozement, mit weißer Holzsockelleiste passend zur Tischlerarbeit, und rutschfestes rektifiziertes Feinsteinzeug auf den Terrassen.',
  'Полы из ректифицированного керамогранита формата 120 x 120 см или из микроцемента, с белым деревянным плинтусом под цвет столярных изделий; на террасах — нескользящий ректифицированный керамогранит.',
  'أرضيات من البورسلين المصقول المقصوص بمقاس 120 × 120 سم أو من الإسمنت الدقيق، مع وزرة خشبية بيضاء متناسقة مع النجارة، وبورسلين مصقول مانع للانزلاق في التراسات.',
  'Vloeren van gerectificeerd porseleinen gres in het formaat 120 x 120 cm of van microcement, met een witte houten plint passend bij het houtwerk, en antislip gerectificeerd porseleinen gres op de terrassen.',
  'Podłogi z rektyfikowanego gresu porcelanowego w formacie 120 x 120 cm lub z mikrocementu, z białą drewnianą listwą przypodłogową dopasowaną do stolarki, a na tarasach antypoślizgowy rektyfikowany gres porcelanowy.',
  'Gulv av rektifisert porselensflis i formatet 120 x 120 cm eller av mikrosement, med hvit tregulvlist som matcher snekkerarbeidet, og sklisikker rektifisert porselensflis på terrassene.',
  'Golv av rektifierad klinker i formatet 120 x 120 cm eller av mikrocement, med vit träsockel som matchar snickerierna, och halkfri rektifierad klinker på terrasserna.')
a('Bathrooms tiled from floor to ceiling in large-format porcelain stoneware and white-paste cladding, combined with microcement on the other walls, and a speckled finish in grey and cream on the bathroom ceilings.',
  'Baños revestidos de suelo a techo con gres porcelánico de gran formato y revestimiento de pasta blanca, combinados con microcemento en el resto de las paredes, y un acabado moteado en gris y crema en los techos de los baños.',
  'Salles de bain revêtues du sol au plafond de grès cérame grand format et de revêtement en pâte blanche, associés à du microciment sur les autres murs, avec une finition mouchetée gris et crème au plafond.',
  'Badezimmer vom Boden bis zur Decke mit großformatigem Feinsteinzeug und weißen Steingutplatten verkleidet, kombiniert mit Mikrozement an den übrigen Wänden, und eine gesprenkelte Oberfläche in Grau und Creme an den Badezimmerdecken.',
  'Ванные комнаты отделаны от пола до потолка крупноформатным керамогранитом и белой плиткой, в сочетании с микроцементом на остальных стенах, а потолки ванных имеют крапчатую отделку в серо-кремовых тонах.',
  'حمامات مكسوّة من الأرض إلى السقف ببورسلين كبير الحجم وكسوة بيضاء من عجينة السيراميك، مع الإسمنت الدقيق على بقية الجدران، وتشطيب منقّط بالرمادي والكريمي على أسقف الحمامات.',
  'Badkamers van vloer tot plafond betegeld met grootformaat porseleinen gres en wit wandtegelwerk, gecombineerd met microcement op de overige wanden, en een gespikkelde afwerking in grijs en crème op de badkamerplafonds.',
  'Łazienki wyłożone od podłogi do sufitu wielkoformatowym gresem porcelanowym i białą okładziną ceramiczną, w połączeniu z mikrocementem na pozostałych ścianach, a sufity łazienek mają cętkowane wykończenie w odcieniach szarości i kremu.',
  'Bad kledd fra gulv til tak med storformat porselensflis og hvit flisbekledning, kombinert med mikrosement på de øvrige veggene, og en spettet overflate i grått og krem i baderomstakene.',
  'Badrum klädda från golv till tak med storformatsklinker och vit kakelbeklädnad, kombinerat med mikrocement på övriga väggar, och en prickig yta i grått och kräm i badrumstaken.')
a('A furnished kitchen with high and low units of large capacity in a laminated finish, a compact quartz worktop and splashback, a central island with storage below and a quartz worktop, and a sink in the same quartz with a pull-out tap.',
  'Cocina amueblada con muebles altos y bajos de gran capacidad con acabado laminado, encimera y frente de cuarzo compacto, una isla central con almacenaje en la parte inferior y encimera de cuarzo, y un fregadero del mismo cuarzo con grifo de caño extraíble.',
  'Cuisine équipée de meubles hauts et bas de grande capacité en finition stratifiée, plan de travail et crédence en quartz compact, un îlot central avec rangements en partie basse et plan de travail en quartz, et un évier du même quartz avec robinet à douchette extractible.',
  'Eine möblierte Küche mit großen Hoch- und Unterschränken in laminierter Ausführung, Arbeitsplatte und Rückwand aus Kompaktquarz, einer zentralen Insel mit Stauraum darunter und Quarz-Arbeitsplatte sowie einem Spülbecken aus demselben Quarz mit ausziehbarer Armatur.',
  'Меблированная кухня с вместительными верхними и нижними шкафами с ламинированной отделкой, столешницей и фартуком из компактного кварца, центральным островом с шкафами внизу и кварцевой столешницей, а также мойкой из того же кварца с выдвижным смесителем.',
  'مطبخ مؤثث بخزائن عالية ومنخفضة كبيرة السعة بتشطيب مُصفَّح، وسطح عمل وواجهة خلفية من الكوارتز المضغوط، وجزيرة مركزية بخزائن تخزين في الأسفل وسطح من الكوارتز، وحوض من الكوارتز نفسه مع صنبور قابل للسحب.',
  'Een gemeubileerde keuken met hoge en lage kasten van grote capaciteit in gelamineerde afwerking, een werkblad en spatwand van compact kwarts, een centraal eiland met opbergruimte eronder en een kwartsen blad, en een spoelbak van hetzelfde kwarts met een uittrekbare kraan.',
  'Umeblowana kuchnia z pojemnymi szafkami górnymi i dolnymi w wykończeniu laminowanym, blatem i panelem ściennym z kwarcu kompaktowego, centralną wyspą z miejscem do przechowywania poniżej i blatem kwarcowym oraz zlewem z tego samego kwarcu z wyciąganą baterią.',
  'Et møblert kjøkken med høye og lave skap med stor kapasitet i laminert finish, benkeplate og sprutsone i kompakt kvarts, en sentral øy med oppbevaring under og kvartsbenkeplate, og en vask i samme kvarts med uttrekkbar kran.',
  'Ett möblerat kök med höga och låga skåp med stor kapacitet i laminatfinish, bänkskiva och stänkskydd i kompakt kvarts, en central köksö med förvaring under och bänkskiva i kvarts, samt en diskho i samma kvarts med utdragbar blandare.')
a('Appliances: an oven and a microwave in a column, an induction hob with an integrated hood, a dishwasher, a fridge, a washing machine and a wine cooler.',
  'Electrodomésticos: horno y microondas en columna, placa de inducción con campana integrada, lavavajillas, frigorífico, lavadora y vinoteca refrigerada.',
  'Électroménager : four et micro-ondes en colonne, plaque à induction avec hotte intégrée, lave-vaisselle, réfrigérateur, lave-linge et cave à vin.',
  'Geräte: Backofen und Mikrowelle in einer Säule, Induktionskochfeld mit integrierter Dunstabzugshaube, Geschirrspüler, Kühlschrank, Waschmaschine und Weinkühlschrank.',
  'Техника: духовой шкаф и микроволновая печь в колонне, индукционная варочная панель со встроенной вытяжкой, посудомоечная машина, холодильник, стиральная машина и винный шкаф.',
  'الأجهزة: فرن وميكروويف في عمود، وموقد حثّي مع شفاط مدمج، وغسالة صحون، وثلاجة، وغسالة ملابس، وثلاجة للنبيذ.',
  'Apparatuur: een oven en een magnetron in een kolom, een inductiekookplaat met geïntegreerde afzuigkap, een vaatwasser, een koelkast, een wasmachine en een wijnkoeler.',
  'Sprzęt: piekarnik i mikrofalówka w zabudowie słupkowej, płyta indukcyjna z wbudowanym okapem, zmywarka, lodówka, pralka i chłodziarka do wina.',
  'Hvitevarer: en ovn og en mikrobølgeovn i søyle, en induksjonstopp med integrert ventilator, en oppvaskmaskin, et kjøleskap, en vaskemaskin og et vinskap.',
  'Vitvaror: en ugn och en mikrovågsugn i kolonn, en induktionshäll med inbyggd fläkt, en diskmaskin, ett kylskåp, en tvättmaskin och ett vinkylskåp.')
a('In the main and the second bathroom, countertop basins in compact quartz on suspended units, low-profile resin shower trays and glass shower screens with stainless-steel or black frames.',
  'En el baño principal y en el segundo, lavabos sobre encimera de cuarzo compacto en muebles suspendidos, platos de ducha de resina de perfil bajo y mamparas de cristal con marcos de acero inoxidable o negros.',
  'Dans la salle de bain principale et la seconde, des vasques posées en quartz compact sur des meubles suspendus, des receveurs de douche en résine à profil bas et des parois de douche en verre à cadre en acier inoxydable ou noir.',
  'Im Hauptbad und im zweiten Bad Aufsatzwaschbecken aus Kompaktquarz auf Hängeschränken, extraflache Duschwannen aus Kunstharz und Duschabtrennungen aus Glas mit Edelstahl- oder schwarzen Rahmen.',
  'В основной и второй ванной — накладные раковины из компактного кварца на подвесных тумбах, низкопрофильные душевые поддоны из смолы и стеклянные душевые ограждения с рамами из нержавеющей стали или чёрными.',
  'في الحمام الرئيسي والحمام الثاني، أحواض فوق سطح من الكوارتز المضغوط على خزائن معلّقة، وأحواض دُش منخفضة من الراتنج، وحواجز دُش زجاجية بإطارات من الفولاذ المقاوم للصدأ أو سوداء.',
  'In de hoofdbadkamer en de tweede badkamer opzetwastafels van compact kwarts op hangende kasten, lage douchebakken van kunsthars en glazen douchewanden met roestvrijstalen of zwarte kaders.',
  'W łazience głównej i drugiej umywalki nablatowe z kwarcu kompaktowego na szafkach podwieszanych, niskoprofilowe brodziki z żywicy oraz szklane kabiny prysznicowe z ramami ze stali nierdzewnej lub czarnymi.',
  'I hovedbadet og det andre badet servanter på benkeplate i kompakt kvarts på hengende skap, lave dusjkar i harpiks og dusjvegger i glass med rammer i rustfritt stål eller sorte.',
  'I huvudbadrummet och det andra badrummet handfat på bänkskiva i kompakt kvarts på hängande skåp, låga duschkar i harts och duschväggar i glas med ramar i rostfritt stål eller svarta.')
a('Thermostatic shower fittings with a sliding rail and a handheld sprayer, single-lever basin taps in chrome or black, and toilets with a dual flush and a soft-close seat.',
  'Grifería termostática de ducha con barra deslizante y rociador de mano, grifos monomando de lavabo cromados o negros, e inodoros con doble descarga y asiento amortiguado.',
  'Robinetterie de douche thermostatique avec barre coulissante et douchette à main, mitigeurs de lavabo chromés ou noirs, et WC à double chasse avec abattant à fermeture amortie.',
  'Thermostatische Duscharmaturen mit Gleitstange und Handbrause, Einhebelmischer an den Waschbecken in Chrom oder Schwarz sowie WCs mit Zweimengen-Spülung und Absenkautomatik.',
  'Термостатическая душевая арматура со скользящей штангой и ручной лейкой, однорычажные смесители для раковин в хроме или чёрном цвете и унитазы с двойным смывом и сиденьем с плавным закрыванием.',
  'خلاطات دُش ثرموستاتية مع قضيب منزلق ورشاش يدوي، وصنابير أحواض أحادية الذراع بلون الكروم أو الأسود، ومراحيض بسيفون مزدوج ومقعد بإغلاق هادئ.',
  'Thermostatische doucheafwerking met een glijstang en een handdouche, eengreeps wastafelkranen in chroom of zwart, en toiletten met een dubbele spoeling en een soft-close bril.',
  'Termostatyczna armatura prysznicowa z drążkiem przesuwnym i słuchawką ręczną, jednouchwytowe baterie umywalkowe w kolorze chromu lub czarnym oraz toalety z dwudzielnym spłukiwaniem i deską wolnoopadającą.',
  'Termostatiske dusjarmaturer med glidestang og håndtusj, énhåndsblandebatterier til servantene i krom eller sort, og toaletter med dobbel skylling og soft-close-sete.',
  'Termostatiska duschblandare med glidstång och handdusch, enhandsblandare till handfaten i krom eller svart, och toaletter med dubbelspolning och mjukstängande sits.')
a('Hot water from an aerothermal system, and integrated air conditioning divided by room, with a thermostat in the living room.',
  'Agua caliente mediante un sistema de aerotermia, y aire acondicionado integrado dividido por estancias, con termostato en el salón.',
  'Eau chaude produite par un système aérothermique, et climatisation intégrée répartie par pièce, avec thermostat dans le séjour.',
  'Warmwasser über ein aerothermisches System und integrierte Klimaanlage, nach Räumen aufgeteilt, mit Thermostat im Wohnzimmer.',
  'Горячее водоснабжение от аэротермальной системы и встроенное кондиционирование с зонированием по комнатам и термостатом в гостиной.',
  'مياه ساخنة من نظام هوائي حراري، وتكييف هواء مدمج مقسَّم بحسب الغرف، مع منظّم حرارة في غرفة المعيشة.',
  'Warm water uit een aerothermisch systeem en geïntegreerde airconditioning per ruimte, met een thermostaat in de woonkamer.',
  'Ciepła woda z systemu aerotermalnego oraz zintegrowana klimatyzacja z podziałem na pomieszczenia, z termostatem w salonie.',
  'Varmtvann fra et aerotermisk system og integrert klimaanlegg delt opp etter rom, med termostat i stuen.',
  'Varmvatten från ett aerotermiskt system och integrerad luftkonditionering uppdelad per rum, med termostat i vardagsrummet.')
a('Recessed LED lights in the kitchen, the corridors and the bathroom ceilings and LED lights on the terraces, a colour video entry phone, and a digital network of integrated services with sockets in the living rooms, kitchens and bedrooms.',
  'Luces LED empotradas en la cocina, los pasillos y los techos de los baños y luces LED en las terrazas, videoportero automático en color, y una red digital de servicios integrados con tomas en los salones, las cocinas y los dormitorios.',
  'Spots LED encastrés dans la cuisine, les couloirs et les plafonds des salles de bain et éclairage LED sur les terrasses, visiophone couleur, et réseau numérique de services intégrés avec prises dans les séjours, les cuisines et les chambres.',
  'Eingelassene LED-Leuchten in Küche, Fluren und Badezimmerdecken sowie LED-Leuchten auf den Terrassen, eine Farb-Videosprechanlage und ein digitales Netz integrierter Dienste mit Anschlüssen in Wohnzimmern, Küchen und Schlafzimmern.',
  'Встроенные светодиодные светильники на кухне, в коридорах и на потолках ванных, светодиодное освещение террас, цветной видеодомофон и цифровая сеть интегрированных услуг с розетками в гостиных, на кухнях и в спальнях.',
  'إضاءة LED مدمجة في المطبخ والممرات وأسقف الحمامات وإضاءة LED في التراسات، وجهاز اتصال مرئي ملوّن، وشبكة رقمية للخدمات المتكاملة بمقابس في غرف المعيشة والمطابخ وغرف النوم.',
  'Inbouw-ledverlichting in de keuken, de gangen en de badkamerplafonds en ledverlichting op de terrassen, een video-intercom in kleur en een digitaal netwerk van geïntegreerde diensten met aansluitingen in de woonkamers, keukens en slaapkamers.',
  'Wpuszczane oświetlenie LED w kuchni, korytarzach i sufitach łazienek oraz oświetlenie LED na tarasach, kolorowy wideodomofon i cyfrowa sieć usług zintegrowanych z gniazdami w salonach, kuchniach i sypialniach.',
  'Innfelte LED-lys på kjøkkenet, i korridorene og i baderomstakene og LED-lys på terrassene, en fargevideotelefon og et digitalt nett av integrerte tjenester med uttak i stuene, kjøkkenene og soverommene.',
  'Infällda LED-lampor i köket, korridorerna och badrumstaken och LED-belysning på terrasserna, en färgvideotelefon och ett digitalt nät av integrerade tjänster med uttag i vardagsrummen, köken och sovrummen.')
a('Water outlets on the roof terraces and in the ground-floor gardens.',
  'Tomas de agua en las terrazas de la cubierta y en los jardines de planta baja.',
  'Prises d’eau sur les terrasses de toit et dans les jardins du rez-de-chaussée.',
  'Wasseranschlüsse auf den Dachterrassen und in den Erdgeschossgärten.',
  'Водопроводные краны на террасах на крыше и в садах на первом этаже.',
  'نقاط مياه في تراسات السطح وفي حدائق الطابق الأرضي.',
  'Wateraansluitingen op de dakterrassen en in de tuinen op de begane grond.',
  'Punkty poboru wody na tarasach dachowych i w ogrodach na parterze.',
  'Vannuttak på takterrassene og i hagene i første etasje.',
  'Vattenuttag på takterrasserna och i trädgårdarna på bottenvåningen.')
a('A communal pool with night lighting, green areas and a sunbathing area, a gym, a spa, a social club and a cinema.',
  'Una piscina comunitaria con iluminación nocturna, zonas verdes y un área de solárium, un gimnasio, un spa, un club social y una sala de cine.',
  'Une piscine commune avec éclairage nocturne, des espaces verts et une zone de bain de soleil, une salle de sport, un spa, un club social et une salle de cinéma.',
  'Ein Gemeinschaftspool mit Nachtbeleuchtung, Grünflächen und Liegebereich, ein Fitnessraum, ein Spa, ein Social Club und ein Kino.',
  'Общий бассейн с ночной подсветкой, зелёные зоны и солярий, тренажёрный зал, спа, социальный клуб и кинозал.',
  'مسبح مشترك بإضاءة ليلية ومساحات خضراء ومنطقة للتشمّس، وصالة رياضية، ومنتجع صحي، ونادٍ اجتماعي، وقاعة سينما.',
  'Een gemeenschappelijk zwembad met nachtverlichting, groenzones en een zonneterras, een fitnessruimte, een spa, een sociale club en een bioscoop.',
  'Wspólny basen z oświetleniem nocnym, tereny zielone i strefa do opalania, siłownia, spa, klub towarzyski i kino.',
  'Et felles basseng med nattbelysning, grøntarealer og solplass, et treningsrom, et spa, en sosial klubb og et kino.',
  'En gemensam pool med kvällsbelysning, grönytor och en solplats, ett gym, ett spa, en social klubb och en biograf.')
a('Landscaping of native, low-water planting with automatic drip irrigation, entrance doors lit to give a warm welcome, and low-energy lighting with motion detectors and timers at the entrances, on the stairs and on the landings.',
  'Paisajismo con plantas autóctonas de bajo consumo de agua y riego por goteo automático, puertas de entrada iluminadas para dar una cálida bienvenida, e iluminación de bajo consumo con detectores de movimiento y temporizadores en los accesos, las escaleras y los rellanos.',
  'Aménagement paysager de plantes locales à faible besoin en eau avec arrosage goutte à goutte automatique, portes d’entrée éclairées pour un accueil chaleureux, et éclairage basse consommation avec détecteurs de mouvement et minuteries aux entrées, dans les escaliers et sur les paliers.',
  'Begrünung mit heimischen, wassersparenden Pflanzen und automatischer Tröpfchenbewässerung, beleuchtete Eingangstüren für einen warmen Empfang sowie Energiesparbeleuchtung mit Bewegungsmeldern und Zeitschaltuhren an den Eingängen, auf den Treppen und auf den Podesten.',
  'Озеленение местными неприхотливыми к воде растениями с автоматическим капельным поливом, освещённые входные двери для тёплой встречи и энергосберегающее освещение с датчиками движения и таймерами у входов, на лестницах и площадках.',
  'تنسيق حدائق بنباتات محلية قليلة استهلاك المياه مع ري بالتنقيط تلقائي، وأبواب مداخل مضاءة لاستقبال دافئ، وإضاءة موفرة للطاقة بكاشفات حركة ومؤقتات عند المداخل وعلى السلالم والمسطحات.',
  'Beplanting met inheemse, waterzuinige planten met automatische druppelirrigatie, verlichte toegangsdeuren voor een warm onthaal, en spaarverlichting met bewegingsmelders en tijdschakelaars bij de ingangen, op de trappen en op de overlopen.',
  'Zagospodarowanie terenu rodzimymi roślinami o niskim zapotrzebowaniu na wodę z automatycznym nawadnianiem kropelkowym, oświetlone drzwi wejściowe dla ciepłego powitania oraz energooszczędne oświetlenie z czujnikami ruchu i wyłącznikami czasowymi przy wejściach, na klatkach schodowych i spocznikach.',
  'Landskapsarbeid med stedegne, vannsparende planter med automatisk dryppvanning, opplyste inngangsdører for en varm velkomst, og energisparende belysning med bevegelsessensorer og tidsur ved inngangene, i trappene og på avsatsene.',
  'Landskapsarbete med inhemska, vattensnåla växter med automatisk droppbevattning, upplysta entrédörrar för ett varmt mottagande, och lågenergibelysning med rörelsedetektorer och timers vid entréerna, i trapporna och på avsatserna.')
a('A garage with remote-controlled doors, a polished continuous quartz-concrete floor, fire protection to the regulations and a pre-installation for electric-car charging.',
  'Garaje con puertas motorizadas con mando a distancia, suelo continuo de hormigón de cuarzo pulido, protección contra incendios conforme a la normativa y preinstalación para la carga de coche eléctrico.',
  'Garage avec portes motorisées à télécommande, sol continu en béton de quartz poli, protection incendie conforme à la réglementation et pré-équipement pour la recharge de voiture électrique.',
  'Eine Garage mit ferngesteuerten Toren, einem polierten durchgehenden Quarzbetonboden, Brandschutz nach den Vorschriften und einer Vorinstallation für das Laden von Elektroautos.',
  'Гараж с воротами с дистанционным управлением, полированным цельным полом из кварцевого бетона, противопожарной защитой по нормам и подготовкой под зарядку электромобиля.',
  'مرآب بأبواب تعمل بالتحكم عن بُعد، وأرضية متصلة من خرسانة الكوارتز المصقولة، وحماية من الحريق وفق الأنظمة، وتمديدات مسبقة لشحن السيارات الكهربائية.',
  'Een garage met afstandsbediende deuren, een gepolijste doorlopende vloer van kwartsbeton, brandbeveiliging volgens de voorschriften en een voorbereiding voor het laden van elektrische auto’s.',
  'Garaż z bramami sterowanymi pilotem, polerowaną ciągłą posadzką z betonu kwarcowego, ochroną przeciwpożarową zgodną z przepisami i instalacją przygotowującą do ładowania samochodów elektrycznych.',
  'En garasje med fjernstyrte porter, et polert sammenhengende kvartsbetonggulv, brannsikring etter forskriftene og forberedt for lading av elbil.',
  'Ett garage med fjärrstyrda portar, ett polerat sammanhängande golv av kvartsbetong, brandskydd enligt föreskrifterna och förberedelse för laddning av elbil.')
a('Lifts that reach every floor and the garage floors directly, with automatic doors, overload detection and a telephone connection, and a cabin adapted for reduced mobility.',
  'Ascensores que llegan a todas las plantas y directamente a las plantas de garaje, con puertas automáticas, detección de sobrecarga y conexión telefónica, y una cabina adaptada a movilidad reducida.',
  'Ascenseurs desservant tous les étages et directement les niveaux de garage, avec portes automatiques, détection de surcharge et liaison téléphonique, et une cabine adaptée aux personnes à mobilité réduite.',
  'Aufzüge, die jede Etage und direkt die Garagengeschosse erreichen, mit automatischen Türen, Überlasterkennung und Telefonanschluss sowie einer für eingeschränkte Mobilität geeigneten Kabine.',
  'Лифты, которые доходят до каждого этажа и напрямую до уровней гаража, с автоматическими дверями, датчиком перегрузки и телефонной связью, а также кабиной, приспособленной для маломобильных людей.',
  'مصاعد تصل إلى كل الطوابق وإلى مستويات المرآب مباشرة، بأبواب أوتوماتيكية وكشف عن الحمولة الزائدة واتصال هاتفي، وكابينة مهيّأة لذوي الحركة المحدودة.',
  'Liften die alle verdiepingen en rechtstreeks de garageverdiepingen bereiken, met automatische deuren, overbelastingsdetectie en een telefoonverbinding, en een cabine die geschikt is voor personen met beperkte mobiliteit.',
  'Windy docierające na każde piętro i bezpośrednio na poziomy garażowe, z drzwiami automatycznymi, czujnikiem przeciążenia i łącznością telefoniczną oraz kabiną dostosowaną dla osób o ograniczonej mobilności.',
  'Heiser som når alle etasjer og direkte garasjenivåene, med automatiske dører, overlastdeteksjon og telefonforbindelse, og en kabin tilpasset nedsatt mobilitet.',
  'Hissar som når alla våningar och direkt garageplanen, med automatiska dörrar, överlastdetektering och telefonanslutning, och en hytt anpassad för nedsatt rörlighet.')

# ---- residences, lifestyle, location ---------------------------------------------------------------

a('Nine homes, <em>three groups</em>',
  'Nueve viviendas, <em>tres grupos</em>', 'Neuf logements, <em>trois groupes</em>', 'Neun Wohnungen, <em>drei Gruppen</em>',
  'Девять квартир, <em>три группы</em>', 'تسعة مساكن، <em>ثلاث مجموعات</em>', 'Negen woningen, <em>drie groepen</em>',
  'Dziewięć lokali, <em>trzy grupy</em>', 'Ni boliger, <em>tre grupper</em>', 'Nio bostäder, <em>tre grupper</em>')
a('The nine homes listed with a price fall into three groups by size and block. The table below lists each one with its price.',
  'Las nueve viviendas con precio se dividen en tres grupos según su tamaño y su bloque. La tabla siguiente recoge cada una con su precio.',
  'Les neuf logements listés avec un prix se répartissent en trois groupes selon la taille et l’immeuble. Le tableau ci-dessous les présente un à un avec leur prix.',
  'Die neun Wohnungen mit Preis lassen sich nach Größe und Block in drei Gruppen einteilen. Die Tabelle unten führt jede mit ihrem Preis auf.',
  'Девять квартир с ценой делятся на три группы по размеру и корпусу. В таблице ниже каждая указана со своей ценой.',
  'تنقسم المساكن التسعة المدرجة بالسعر إلى ثلاث مجموعات بحسب الحجم والمبنى. ويورد الجدول أدناه كل مسكن مع سعره.',
  'De negen woningen met een prijs vallen naar grootte en blok uiteen in drie groepen. In de tabel hieronder staat elke woning met haar prijs.',
  'Dziewięć lokali z podaną ceną dzieli się na trzy grupy według wielkości i budynku. W tabeli poniżej każdy z nich ma podaną cenę.',
  'De ni boligene med pris deler seg i tre grupper etter størrelse og blokk. Tabellen under viser hver av dem med pris.',
  'De nio bostäderna med pris delas in i tre grupper efter storlek och hus. Tabellen nedan visar var och en med sitt pris.')
a('Two bedrooms, blocks 1 and 2', 'Dos dormitorios, bloques 1 y 2', 'Deux chambres, immeubles 1 et 2', 'Zwei Schlafzimmer, Blöcke 1 und 2',
  'Две спальни, корпуса 1 и 2', 'غرفتا نوم، المبنيان 1 و2', 'Twee slaapkamers, blokken 1 en 2', 'Dwie sypialnie, budynki 1 i 2',
  'To soverom, hus 1 og 2', 'Två sovrum, hus 1 och 2')
a('Four homes with two bedrooms and two bathrooms: 1-2A and 1-3A in block 1, with 76.26 sqm built, and 2-1A and 2-3A in block 2, with 70.93 sqm built. The list gives terraces of 20.40 sqm for the first two and 24.30 sqm for the other two.',
  'Cuatro viviendas de dos dormitorios y dos baños: 1-2A y 1-3A en el bloque 1, con {N76.26} {U} construidos, y 2-1A y 2-3A en el bloque 2, con {N70.93} {U} construidos. La lista da terrazas de {N20.40} {U} para las dos primeras y de {N24.30} {U} para las otras dos.',
  'Quatre logements de deux chambres et deux salles de bain : 1-2A et 1-3A dans l’immeuble 1, avec {N76.26} {U} construits, et 2-1A et 2-3A dans l’immeuble 2, avec {N70.93} {U} construits. La liste donne des terrasses de {N20.40} {U} pour les deux premiers et de {N24.30} {U} pour les deux autres.',
  'Vier Wohnungen mit zwei Schlafzimmern und zwei Badezimmern: 1-2A und 1-3A in Block 1 mit {N76.26} {U} bebauter Fläche sowie 2-1A und 2-3A in Block 2 mit {N70.93} {U} bebauter Fläche. Die Liste gibt für die ersten beiden Terrassen von {N20.40} {U} und für die anderen beiden von {N24.30} {U} an.',
  'Четыре квартиры с двумя спальнями и двумя санузлами: 1-2A и 1-3A в корпусе 1, {N76.26} {U} застроенной площади, и 2-1A и 2-3A в корпусе 2, {N70.93} {U} застроенной площади. По прайс-листу терраса первых двух — {N20.40} {U}, двух других — {N24.30} {U}.',
  'أربعة مساكن بغرفتي نوم وحمّامين: 1-2A و1-3A في المبنى 1 بمساحة مبنية {N76.26} {U}، و2-1A و2-3A في المبنى 2 بمساحة مبنية {N70.93} {U}. وتذكر القائمة تراسات بمساحة {N20.40} {U} للمسكنين الأولين و{N24.30} {U} للآخرين.',
  'Vier woningen met twee slaapkamers en twee badkamers: 1-2A en 1-3A in blok 1, met {N76.26} {U} bebouwd, en 2-1A en 2-3A in blok 2, met {N70.93} {U} bebouwd. De lijst geeft terrassen van {N20.40} {U} voor de eerste twee en van {N24.30} {U} voor de andere twee.',
  'Cztery lokale z dwiema sypialniami i dwiema łazienkami: 1-2A i 1-3A w budynku 1, o powierzchni zabudowy {N76.26} {U}, oraz 2-1A i 2-3A w budynku 2, o powierzchni zabudowy {N70.93} {U}. Cennik podaje tarasy o powierzchni {N20.40} {U} dla pierwszych dwóch i {N24.30} {U} dla pozostałych dwóch.',
  'Fire boliger med to soverom og to bad: 1-2A og 1-3A i hus 1, med {N76.26} {U} bebygd areal, og 2-1A og 2-3A i hus 2, med {N70.93} {U} bebygd areal. Listen oppgir terrasser på {N20.40} {U} for de to første og {N24.30} {U} for de to andre.',
  'Fyra bostäder med två sovrum och två badrum: 1-2A och 1-3A i hus 1, med {N76.26} {U} byggyta, och 2-1A och 2-3A i hus 2, med {N70.93} {U} byggyta. Listan anger terrasser på {N20.40} {U} för de två första och {N24.30} {U} för de två andra.')
a('The prices are EUR 849,000, EUR 879,000, EUR 865,000 and EUR 889,000.',
  'Los precios son {E849000}, {E879000}, {E865000} y {E889000}.',
  'Les prix sont de {E849000}, {E879000}, {E865000} et {E889000}.',
  'Die Preise betragen {E849000}, {E879000}, {E865000} und {E889000}.',
  'Цены — {E849000}, {E879000}, {E865000} и {E889000}.',
  'الأسعار هي {E849000} و{E879000} و{E865000} و{E889000}.',
  'De prijzen zijn {E849000}, {E879000}, {E865000} en {E889000}.',
  'Ceny wynoszą {E849000}, {E879000}, {E865000} i {E889000}.',
  'Prisene er {E849000}, {E879000}, {E865000} og {E889000}.',
  'Priserna är {E849000}, {E879000}, {E865000} och {E889000}.')
a('The plans give interior areas of 70.55 sqm for the block 1 homes and 65.70 sqm for the block 2 homes, and terraces of 18.30, 18.25, 18.00 and 21.70 sqm, in the same order as above.',
  'Los planos dan superficies interiores de {N70.55} {U} para las viviendas del bloque 1 y de {N65.70} {U} para las del bloque 2, y terrazas de {N18.30}, {N18.25}, {N18.00} y {N21.70} {U}, en el mismo orden que arriba.',
  'Les plans donnent des surfaces intérieures de {N70.55} {U} pour les logements de l’immeuble 1 et de {N65.70} {U} pour ceux de l’immeuble 2, et des terrasses de {N18.30}, {N18.25}, {N18.00} et {N21.70} {U}, dans le même ordre que ci-dessus.',
  'Die Pläne geben Innenflächen von {N70.55} {U} für die Wohnungen in Block 1 und {N65.70} {U} für die in Block 2 an sowie Terrassen von {N18.30}, {N18.25}, {N18.00} und {N21.70} {U}, in derselben Reihenfolge wie oben.',
  'По планам внутренняя площадь квартир корпуса 1 — {N70.55} {U}, корпуса 2 — {N65.70} {U}, а террасы — {N18.30}, {N18.25}, {N18.00} и {N21.70} {U} в том же порядке, что и выше.',
  'تذكر المخططات مساحات داخلية {N70.55} {U} لمساكن المبنى 1 و{N65.70} {U} لمساكن المبنى 2، وتراسات بمساحة {N18.30} و{N18.25} و{N18.00} و{N21.70} {U}، بالترتيب نفسه أعلاه.',
  'De plattegronden geven binnenoppervlakten van {N70.55} {U} voor de woningen in blok 1 en {N65.70} {U} voor die in blok 2, en terrassen van {N18.30}, {N18.25}, {N18.00} en {N21.70} {U}, in dezelfde volgorde als hierboven.',
  'Rzuty podają powierzchnię wnętrza {N70.55} {U} dla lokali w budynku 1 i {N65.70} {U} dla lokali w budynku 2 oraz tarasy o powierzchni {N18.30}, {N18.25}, {N18.00} i {N21.70} {U}, w tej samej kolejności co wyżej.',
  'Plantegningene oppgir innvendig areal på {N70.55} {U} for boligene i hus 1 og {N65.70} {U} for boligene i hus 2, og terrasser på {N18.30}, {N18.25}, {N18.00} og {N21.70} {U}, i samme rekkefølge som over.',
  'Planritningarna anger inomhusytor på {N70.55} {U} för bostäderna i hus 1 och {N65.70} {U} för bostäderna i hus 2, och terrasser på {N18.30}, {N18.25}, {N18.00} och {N21.70} {U}, i samma ordning som ovan.')
a('Three bedrooms, block 2', 'Tres dormitorios, bloque 2', 'Trois chambres, immeuble 2', 'Drei Schlafzimmer, Block 2',
  'Три спальни, корпус 2', 'ثلاث غرف نوم، المبنى 2', 'Drie slaapkamers, blok 2', 'Trzy sypialnie, budynek 2', 'Tre soverom, hus 2', 'Tre sovrum, hus 2')
a('Four homes with three bedrooms and two bathrooms on the first to the fourth floor: 2-1B, 2-2B, 2-3B and 2-4B, each with 87.88 sqm built and a terrace of 21.65 sqm on the list.',
  'Cuatro viviendas de tres dormitorios y dos baños entre la primera y la cuarta planta: 2-1B, 2-2B, 2-3B y 2-4B, cada una con {N87.88} {U} construidos y una terraza de {N21.65} {U} según la lista.',
  'Quatre logements de trois chambres et deux salles de bain, du premier au quatrième étage : 2-1B, 2-2B, 2-3B et 2-4B, chacun avec {N87.88} {U} construits et une terrasse de {N21.65} {U} selon la liste.',
  'Vier Wohnungen mit drei Schlafzimmern und zwei Badezimmern im ersten bis vierten Obergeschoss: 2-1B, 2-2B, 2-3B und 2-4B, jeweils mit {N87.88} {U} bebauter Fläche und einer Terrasse von {N21.65} {U} laut Liste.',
  'Четыре квартиры с тремя спальнями и двумя санузлами со второго по пятый этаж: 2-1B, 2-2B, 2-3B и 2-4B, у каждой {N87.88} {U} застроенной площади и терраса {N21.65} {U} по прайс-листу.',
  'أربعة مساكن بثلاث غرف نوم وحمّامين من الطابق الأول إلى الرابع: 2-1B و2-2B و2-3B و2-4B، لكل منها مساحة مبنية {N87.88} {U} وتراس بمساحة {N21.65} {U} بحسب القائمة.',
  'Vier woningen met drie slaapkamers en twee badkamers op de eerste tot en met de vierde verdieping: 2-1B, 2-2B, 2-3B en 2-4B, elk met {N87.88} {U} bebouwd en een terras van {N21.65} {U} volgens de lijst.',
  'Cztery lokale z trzema sypialniami i dwiema łazienkami od pierwszego do czwartego piętra: 2-1B, 2-2B, 2-3B i 2-4B, każdy o powierzchni zabudowy {N87.88} {U} i z tarasem o powierzchni {N21.65} {U} według cennika.',
  'Fire boliger med tre soverom og to bad i andre til femte etasje: 2-1B, 2-2B, 2-3B og 2-4B, hver med {N87.88} {U} bebygd areal og en terrasse på {N21.65} {U} ifølge listen.',
  'Fyra bostäder med tre sovrum och två badrum på första till fjärde våningen: 2-1B, 2-2B, 2-3B och 2-4B, var och en med {N87.88} {U} byggyta och en terrass på {N21.65} {U} enligt listan.')
a('The prices rise with the floor, from EUR 953,000 on the first floor to EUR 1,155,000 on the fourth.',
  'Los precios suben con la planta, desde {E953000} en la primera hasta {E1155000} en la cuarta.',
  'Les prix augmentent avec l’étage, de {E953000} au premier à {E1155000} au quatrième.',
  'Die Preise steigen mit der Etage, von {E953000} im ersten bis {E1155000} im vierten Obergeschoss.',
  'Цены растут с этажом: от {E953000} на втором этаже до {E1155000} на пятом.',
  'ترتفع الأسعار مع ارتفاع الطابق، من {E953000} في الطابق الأول إلى {E1155000} في الطابق الرابع.',
  'De prijzen stijgen met de verdieping, van {E953000} op de eerste tot {E1155000} op de vierde.',
  'Ceny rosną wraz z piętrem: od {E953000} na pierwszym do {E1155000} na czwartym.',
  'Prisene stiger med etasjen, fra {E953000} i andre etasje til {E1155000} i femte.',
  'Priserna stiger med våningen, från {E953000} på första våningen till {E1155000} på fjärde.')
a('The plans give an interior area of 82.30 sqm and terraces of 19.90, 15.90, 15.75 and 19.40 sqm, in the same order as above.',
  'Los planos dan una superficie interior de {N82.30} {U} y terrazas de {N19.90}, {N15.90}, {N15.75} y {N19.40} {U}, en el mismo orden que arriba.',
  'Les plans donnent une surface intérieure de {N82.30} {U} et des terrasses de {N19.90}, {N15.90}, {N15.75} et {N19.40} {U}, dans le même ordre que ci-dessus.',
  'Die Pläne geben eine Innenfläche von {N82.30} {U} und Terrassen von {N19.90}, {N15.90}, {N15.75} und {N19.40} {U} an, in derselben Reihenfolge wie oben.',
  'По планам внутренняя площадь — {N82.30} {U}, а террасы — {N19.90}, {N15.90}, {N15.75} и {N19.40} {U} в том же порядке, что и выше.',
  'تذكر المخططات مساحة داخلية {N82.30} {U} وتراسات بمساحة {N19.90} و{N15.90} و{N15.75} و{N19.40} {U}، بالترتيب نفسه أعلاه.',
  'De plattegronden geven een binnenoppervlakte van {N82.30} {U} en terrassen van {N19.90}, {N15.90}, {N15.75} en {N19.40} {U}, in dezelfde volgorde als hierboven.',
  'Rzuty podają powierzchnię wnętrza {N82.30} {U} oraz tarasy o powierzchni {N19.90}, {N15.90}, {N15.75} i {N19.40} {U}, w tej samej kolejności co wyżej.',
  'Plantegningene oppgir et innvendig areal på {N82.30} {U} og terrasser på {N19.90}, {N15.90}, {N15.75} og {N19.40} {U}, i samme rekkefølge som over.',
  'Planritningarna anger en inomhusyta på {N82.30} {U} och terrasser på {N19.90}, {N15.90}, {N15.75} och {N19.40} {U}, i samma ordning som ovan.')
a('Three bedrooms, block 3', 'Tres dormitorios, bloque 3', 'Trois chambres, immeuble 3', 'Drei Schlafzimmer, Block 3',
  'Три спальни, корпус 3', 'ثلاث غرف نوم، المبنى 3', 'Drie slaapkamers, blok 3', 'Trzy sypialnie, budynek 3', 'Tre soverom, hus 3', 'Tre sovrum, hus 3')
a('Home 3-3A on the third floor, with three bedrooms and two bathrooms, 88.66 sqm built and a terrace of 45.48 sqm on the list.',
  'La vivienda 3-3A, en la tercera planta, con tres dormitorios y dos baños, {N88.66} {U} construidos y una terraza de {N45.48} {U} según la lista.',
  'Le logement 3-3A, au troisième étage, avec trois chambres et deux salles de bain, {N88.66} {U} construits et une terrasse de {N45.48} {U} selon la liste.',
  'Die Wohnung 3-3A im dritten Obergeschoss, mit drei Schlafzimmern und zwei Badezimmern, {N88.66} {U} bebauter Fläche und einer Terrasse von {N45.48} {U} laut Liste.',
  'Квартира 3-3A на четвёртом этаже с тремя спальнями и двумя санузлами, {N88.66} {U} застроенной площади и терраса {N45.48} {U} по прайс-листу.',
  'المسكن 3-3A في الطابق الثالث، بثلاث غرف نوم وحمّامين، ومساحة مبنية {N88.66} {U} وتراس بمساحة {N45.48} {U} بحسب القائمة.',
  'Woning 3-3A op de derde verdieping, met drie slaapkamers en twee badkamers, {N88.66} {U} bebouwd en een terras van {N45.48} {U} volgens de lijst.',
  'Lokal 3-3A na trzecim piętrze, z trzema sypialniami i dwiema łazienkami, o powierzchni zabudowy {N88.66} {U} i z tarasem o powierzchni {N45.48} {U} według cennika.',
  'Bolig 3-3A i fjerde etasje, med tre soverom og to bad, {N88.66} {U} bebygd areal og en terrasse på {N45.48} {U} ifølge listen.',
  'Bostad 3-3A på tredje våningen, med tre sovrum och två badrum, {N88.66} {U} byggyta och en terrass på {N45.48} {U} enligt listan.')
a('The price is EUR 1,245,000.', 'El precio es de {E1245000}.', 'Le prix est de {E1245000}.', 'Der Preis beträgt {E1245000}.', 'Цена — {E1245000}.',
  'السعر هو {E1245000}.', 'De prijs is {E1245000}.', 'Cena wynosi {E1245000}.', 'Prisen er {E1245000}.', 'Priset är {E1245000}.')
a('The plan gives 81.60 sqm interior and a terrace of 45.50 sqm.',
  'El plano da {N81.60} {U} interiores y una terraza de {N45.50} {U}.',
  'Le plan donne {N81.60} {U} intérieurs et une terrasse de {N45.50} {U}.',
  'Der Plan gibt {N81.60} {U} Innenfläche und eine Terrasse von {N45.50} {U} an.',
  'По плану внутренняя площадь — {N81.60} {U}, терраса — {N45.50} {U}.',
  'يذكر المخطط مساحة داخلية {N81.60} {U} وتراسًا بمساحة {N45.50} {U}.',
  'De plattegrond geeft {N81.60} {U} binnen en een terras van {N45.50} {U}.',
  'Rzut podaje powierzchnię wnętrza {N81.60} {U} oraz taras o powierzchni {N45.50} {U}.',
  'Plantegningen oppgir {N81.60} {U} innvendig og en terrasse på {N45.50} {U}.',
  'Planritningen anger {N81.60} {U} inomhus och en terrass på {N45.50} {U}.')

a('A spa, <em>a gym</em> and a pool',
  'Un spa, <em>un gimnasio</em> y una piscina', 'Un spa, <em>une salle de sport</em> et une piscine', 'Ein Spa, <em>ein Fitnessraum</em> und ein Pool',
  'Спа, <em>тренажёрный зал</em> и бассейн', 'منتجع صحي، <em>وصالة رياضية</em> ومسبح', 'Een spa, <em>een fitnessruimte</em> en een zwembad',
  'Spa, <em>siłownia</em> i basen', 'Et spa, <em>et treningsrom</em> og et basseng', 'Ett spa, <em>ett gym</em> och en pool')
a('The shared areas are planned around a pool, a spa and a gym, with a cinema and a coworking room, within the complex.',
  'Las zonas comunes se organizan en torno a una piscina, un spa y un gimnasio, con una sala de cine y una sala de coworking, dentro del conjunto.',
  'Les espaces communs s’organisent autour d’une piscine, d’un spa et d’une salle de sport, avec une salle de cinéma et un espace de coworking, au sein de la résidence.',
  'Die Gemeinschaftsbereiche sind um einen Pool, ein Spa und einen Fitnessraum angelegt, dazu ein Kino und ein Coworking-Raum, innerhalb der Anlage.',
  'Общие зоны построены вокруг бассейна, спа и тренажёрного зала, с кинозалом и коворкингом на территории комплекса.',
  'تتمحور المناطق المشتركة حول مسبح ومنتجع صحي وصالة رياضية، مع قاعة سينما وقاعة عمل مشترك، داخل المجمع.',
  'De gemeenschappelijke ruimten zijn opgezet rond een zwembad, een spa en een fitnessruimte, met een bioscoop en een coworkingruimte, binnen het complex.',
  'Części wspólne zaplanowano wokół basenu, spa i siłowni, z kinem i salą coworkingową na terenie osiedla.',
  'Fellesarealene er planlagt rundt et basseng, et spa og et treningsrom, med et kino og et coworking-rom, innenfor komplekset.',
  'De gemensamma ytorna är planerade kring en pool, ett spa och ett gym, med en biograf och ett coworking-rum, inom området.')
a('A communal pool of 77.65 sqm with night lighting, in a garden of 67.60 sqm with a sunbathing area.',
  'Una piscina comunitaria de {N77.65} {U} con iluminación nocturna, en un jardín de {N67.60} {U} con zona de solárium.',
  'Une piscine commune de {N77.65} {U} avec éclairage nocturne, dans un jardin de {N67.60} {U} avec une zone de bain de soleil.',
  'Ein Gemeinschaftspool von {N77.65} {U} mit Nachtbeleuchtung, in einem Garten von {N67.60} {U} mit Liegebereich.',
  'Общий бассейн площадью {N77.65} {U} с ночной подсветкой в саду площадью {N67.60} {U} с зоной для загара.',
  'مسبح مشترك بمساحة {N77.65} {U} بإضاءة ليلية، في حديقة بمساحة {N67.60} {U} مع منطقة للتشمّس.',
  'Een gemeenschappelijk zwembad van {N77.65} {U} met nachtverlichting, in een tuin van {N67.60} {U} met een zonneterras.',
  'Wspólny basen o powierzchni {N77.65} {U} z oświetleniem nocnym, w ogrodzie o powierzchni {N67.60} {U} ze strefą do opalania.',
  'Et felles basseng på {N77.65} {U} med nattbelysning, i en hage på {N67.60} {U} med solplass.',
  'En gemensam pool på {N77.65} {U} med kvällsbelysning, i en trädgård på {N67.60} {U} med solplats.')
a('A spa of 46.90 sqm. The developer’s images show a lounge with sunbeds, a narrow pool with water jets and a round whirlpool.',
  'Un spa de {N46.90} {U}. Las imágenes del promotor muestran una sala con tumbonas, una piscina estrecha con chorros de agua y un jacuzzi redondo.',
  'Un spa de {N46.90} {U}. Les images du promoteur montrent un salon avec des lits de repos, un bassin étroit avec des jets d’eau et un jacuzzi rond.',
  'Ein Spa mit {N46.90} {U}. Die Bilder des Bauträgers zeigen einen Ruhebereich mit Liegen, ein schmales Becken mit Wasserdüsen und einen runden Whirlpool.',
  'Спа площадью {N46.90} {U}. На изображениях застройщика — зона отдыха с шезлонгами, узкий бассейн с водяными форсунками и круглая джакузи.',
  'منتجع صحي بمساحة {N46.90} {U}. وتُظهر صور المطوّر صالة بمقاعد استلقاء ومسبحًا ضيقًا بنوافير مياه وجاكوزي دائريًا.',
  'Een spa van {N46.90} {U}. De beelden van de ontwikkelaar tonen een ruimte met ligbedden, een smal bad met waterstralen en een rond bubbelbad.',
  'Spa o powierzchni {N46.90} {U}. Obrazy dewelopera pokazują strefę z leżankami, wąski basen z dyszami wodnymi i okrągłe jacuzzi.',
  'Et spa på {N46.90} {U}. Utbyggerens bilder viser en hvilesone med solsenger, et smalt basseng med vannstråler og et rundt boblebad.',
  'Ett spa på {N46.90} {U}. Exploatörens bilder visar en vilozon med solsängar, en smal pool med vattenstrålar och ett runt bubbelbad.')
a('A gym of 31.40 sqm and a coworking room of 33.90 sqm, on the first basement level.',
  'Un gimnasio de {N31.40} {U} y una sala de coworking de {N33.90} {U}, en la primera planta de sótano.',
  'Une salle de sport de {N31.40} {U} et un espace de coworking de {N33.90} {U}, au premier niveau de sous-sol.',
  'Ein Fitnessraum mit {N31.40} {U} und ein Coworking-Raum mit {N33.90} {U}, im ersten Untergeschoss.',
  'Тренажёрный зал площадью {N31.40} {U} и коворкинг площадью {N33.90} {U} на первом подземном уровне.',
  'صالة رياضية بمساحة {N31.40} {U} وقاعة عمل مشترك بمساحة {N33.90} {U}، في المستوى السفلي الأول.',
  'Een fitnessruimte van {N31.40} {U} en een coworkingruimte van {N33.90} {U}, op de eerste kelderlaag.',
  'Siłownia o powierzchni {N31.40} {U} i sala coworkingowa o powierzchni {N33.90} {U} na pierwszym poziomie podziemnym.',
  'Et treningsrom på {N31.40} {U} og et coworking-rom på {N33.90} {U}, på første kjellernivå.',
  'Ett gym på {N31.40} {U} och ett coworking-rum på {N33.90} {U}, på första källarplanet.')
a('The cinema', 'La sala de cine', 'La salle de cinéma', 'Das Kino', 'Кинозал', 'قاعة السينما', 'De bioscoop', 'Kino', 'Kinoen', 'Biografen')
a('A cinema room of 15.40 sqm, on the same level as the spa, the gym and the coworking room.',
  'Una sala de cine de {N15.40} {U}, en la misma planta que el spa, el gimnasio y la sala de coworking.',
  'Une salle de cinéma de {N15.40} {U}, au même niveau que le spa, la salle de sport et l’espace de coworking.',
  'Ein Kinoraum mit {N15.40} {U}, auf derselben Ebene wie Spa, Fitnessraum und Coworking-Raum.',
  'Кинозал площадью {N15.40} {U} на том же уровне, что и спа, тренажёрный зал и коворкинг.',
  'قاعة سينما بمساحة {N15.40} {U}، في المستوى نفسه الذي يضم المنتجع الصحي والصالة الرياضية وقاعة العمل المشترك.',
  'Een bioscoopzaal van {N15.40} {U}, op dezelfde laag als de spa, de fitnessruimte en de coworkingruimte.',
  'Sala kinowa o powierzchni {N15.40} {U} na tym samym poziomie co spa, siłownia i sala coworkingowa.',
  'Et kinorom på {N15.40} {U}, på samme nivå som spaet, treningsrommet og coworking-rommet.',
  'En biosalong på {N15.40} {U}, på samma plan som spat, gymmet och coworking-rummet.')
a('Three basement levels with garage spaces and storage rooms, lifts to every floor and a pre-installation for electric-car charging.',
  'Tres plantas de sótano con plazas de garaje y trasteros, ascensores a todas las plantas y preinstalación para la carga de coche eléctrico.',
  'Trois niveaux de sous-sol avec places de garage et caves, ascenseurs desservant tous les étages et pré-équipement pour la recharge de voiture électrique.',
  'Drei Untergeschosse mit Garagenstellplätzen und Abstellräumen, Aufzüge zu allen Etagen und eine Vorinstallation für das Laden von Elektroautos.',
  'Три подземных уровня с местами в гараже и кладовыми, лифты на все этажи и подготовка под зарядку электромобиля.',
  'ثلاثة مستويات سفلية فيها مواقف مرآب وغرف تخزين، ومصاعد إلى كل الطوابق، وتمديدات مسبقة لشحن السيارات الكهربائية.',
  'Drie kelderlagen met garageplaatsen en bergingen, liften naar alle verdiepingen en een voorbereiding voor het laden van elektrische auto’s.',
  'Trzy poziomy podziemne z miejscami garażowymi i komórkami lokatorskimi, windy na wszystkie piętra i instalacja przygotowująca do ładowania samochodów elektrycznych.',
  'Tre kjellernivåer med garasjeplasser og boder, heiser til alle etasjer og forberedt for lading av elbil.',
  'Tre källarplan med garageplatser och förråd, hissar till alla våningar och förberedelse för laddning av elbil.')

a('Las Mesas, <em>in Estepona</em>', 'Las Mesas, <em>en Estepona</em>', 'Las Mesas, <em>à Estepona</em>', 'Las Mesas, <em>in Estepona</em>',
  'Лас-Месас, <em>Эстепона</em>', 'لاس ميساس، <em>في إستيبونا</em>', 'Las Mesas, <em>in Estepona</em>', 'Las Mesas, <em>w Esteponie</em>',
  'Las Mesas, <em>i Estepona</em>', 'Las Mesas, <em>i Estepona</em>')
a('Las Mesas, <em>Estepona</em>', 'Las Mesas, <em>Estepona</em>', 'Las Mesas, <em>Estepona</em>', 'Las Mesas, <em>Estepona</em>',
  'Лас-Месас, <em>Эстепона</em>', 'لاس ميساس، <em>إستيبونا</em>', 'Las Mesas, <em>Estepona</em>', 'Las Mesas, <em>Estepona</em>',
  'Las Mesas, <em>Estepona</em>', 'Las Mesas, <em>Estepona</em>')
a('The homes are in Las Mesas, which the developer’s dossier calls one of the most distinguished residential areas of Estepona, in the heart of the Costa del Sol. It puts the site on the A-7 and the AP-7, 5 minutes from La Rada beach and 45 minutes from Málaga airport, with health centres, supermarkets and shopping centres in the area. The dossier does not say whether the 5 minutes are on foot or by car.',
  'Las viviendas están en Las Mesas, que el dosier del promotor define como una de las zonas residenciales más distinguidas de Estepona, en pleno corazón de la Costa del Sol. Sitúa el conjunto junto a la A-7 y la AP-7, a 5 minutos de la playa de la Rada y a 45 minutos del aeropuerto de Málaga, con centros de salud, supermercados y centros comerciales en la zona. El dosier no indica si los 5 minutos son a pie o en coche.',
  'Les logements sont à Las Mesas, que le dossier du promoteur présente comme l’un des quartiers résidentiels les plus distingués d’Estepona, au cœur de la Costa del Sol. Il situe le site près de l’A-7 et de l’AP-7, à 5 minutes de la plage de La Rada et à 45 minutes de l’aéroport de Málaga, avec des centres de santé, des supermarchés et des centres commerciaux dans le secteur. Le dossier ne précise pas si les 5 minutes se font à pied ou en voiture.',
  'Die Wohnungen liegen in Las Mesas, das die Broschüre des Bauträgers als eine der vornehmsten Wohngegenden von Estepona im Herzen der Costa del Sol bezeichnet. Sie beschreibt die Lage an der A-7 und der AP-7, 5 Minuten vom Strand La Rada und 45 Minuten vom Flughafen Málaga entfernt, mit Gesundheitszentren, Supermärkten und Einkaufszentren in der Umgebung. Die Broschüre sagt nicht, ob die 5 Minuten zu Fuß oder mit dem Auto gemeint sind.',
  'Квартиры расположены в Лас-Месас — в брошюре застройщика этот район назван одним из самых престижных жилых районов Эстепоны, в самом сердце Коста-дель-Соль. Комплекс находится у автомагистралей A-7 и AP-7, в 5 минутах от пляжа Ла-Рада и в 45 минутах от аэропорта Малаги; поблизости есть медицинские центры, супермаркеты и торговые центры. В брошюре не сказано, идёт ли речь о 5 минутах пешком или на машине.',
  'تقع المساكن في لاس ميساس، التي يصفها كتيّب المطوّر بأنها من أرقى المناطق السكنية في إستيبونا، في قلب كوستا ديل سول. ويضع الموقع على الطريقين A-7 وAP-7، على بُعد 5 دقائق من شاطئ لا رادا و45 دقيقة من مطار ملقة، مع مراكز صحية وأسواق ومراكز تسوق في المنطقة. ولا يذكر الكتيّب ما إذا كانت الدقائق الخمس سيرًا على الأقدام أم بالسيارة.',
  'De woningen liggen in Las Mesas, dat de brochure van de ontwikkelaar een van de meest gedistingeerde woonwijken van Estepona noemt, in het hart van de Costa del Sol. Ze plaatst de locatie aan de A-7 en de AP-7, op 5 minuten van het strand La Rada en op 45 minuten van de luchthaven van Málaga, met gezondheidscentra, supermarkten en winkelcentra in de buurt. De brochure zegt niet of de 5 minuten te voet of met de auto zijn.',
  'Lokale znajdują się w Las Mesas, które broszura dewelopera nazywa jedną z najbardziej prestiżowych dzielnic mieszkaniowych Estepony, w samym sercu Costa del Sol. Umiejscawia osiedle przy A-7 i AP-7, 5 minut od plaży La Rada i 45 minut od lotniska w Maladze, z ośrodkami zdrowia, supermarketami i centrami handlowymi w okolicy. Broszura nie podaje, czy te 5 minut to dojście pieszo, czy dojazd samochodem.',
  'Boligene ligger i Las Mesas, som utbyggerens brosjyre kaller et av de mest distingverte boligområdene i Estepona, midt i hjertet av Costa del Sol. Den plasserer området ved A-7 og AP-7, 5 minutter fra stranden La Rada og 45 minutter fra Málaga lufthavn, med helsesentre, supermarkeder og kjøpesentre i nærheten. Brosjyren sier ikke om de 5 minuttene er til fots eller med bil.',
  'Bostäderna ligger i Las Mesas, som exploatörens broschyr kallar ett av de mest distingerade bostadsområdena i Estepona, mitt i hjärtat av Costa del Sol. Den placerar området vid A-7 och AP-7, 5 minuter från stranden La Rada och 45 minuter från Málaga flygplats, med vårdcentraler, snabbköp och köpcentrum i närheten. Broschyren anger inte om de 5 minuterna är till fots eller med bil.')
a('5 minutes, as the developer says', '5 minutos, según el promotor', '5 minutes, selon le promoteur', '5 Minuten, laut Bauträger',
  '5 минут, по данным застройщика', '5 دقائق، بحسب المطوّر', '5 minuten, volgens de ontwikkelaar', '5 minut, według dewelopera',
  '5 minutter, ifølge utbyggeren', '5 minuter, enligt exploatören')
a('45 minutes, as the developer says', '45 minutos, según el promotor', '45 minutes, selon le promoteur', '45 Minuten, laut Bauträger',
  '45 минут, по данным застройщика', '45 دقيقة، بحسب المطوّر', '45 minuten, volgens de ontwikkelaar', '45 minut, według dewelopera',
  '45 minutter, ifølge utbyggeren', '45 minuter, enligt exploatören')

# ---- investment, checks, availability -------------------------------------------------------------

a('A factual note on what the documents say and do not say; Nueva Living does not promise rental returns or price appreciation.',
  'Una nota objetiva sobre lo que los documentos dicen y no dicen; Nueva Living no promete rentabilidad por alquiler ni revalorización.',
  'Une note factuelle sur ce que les documents disent et ne disent pas ; Nueva Living ne promet ni rendement locatif ni plus-value.',
  'Ein sachlicher Hinweis dazu, was die Unterlagen sagen und was nicht; Nueva Living verspricht weder Mietrenditen noch Wertsteigerungen.',
  'Фактическая справка о том, что сказано и не сказано в документах; Nueva Living не обещает ни доходности от аренды, ни роста цен.',
  'ملاحظة واقعية حول ما تذكره الوثائق وما لا تذكره؛ لا تعد Nueva Living بعوائد إيجارية ولا بارتفاع الأسعار.',
  'Een feitelijke noot over wat de documenten wel en niet zeggen; Nueva Living belooft geen huurrendement of waardestijging.',
  'Rzeczowa uwaga o tym, co dokumenty mówią, a czego nie mówią; Nueva Living nie obiecuje zwrotów z wynajmu ani wzrostu cen.',
  'En saklig merknad om hva dokumentene sier og ikke sier; Nueva Living lover verken leieavkastning eller prisstigning.',
  'En saklig anmärkning om vad dokumenten säger och inte säger; Nueva Living lovar varken hyresavkastning eller prisuppgång.')
a('Twenty-five of the 34 homes on the list are marked reserved. Nine are listed with a price, from EUR 849,000 to EUR 1,245,000 plus VAT.',
  'Veinticinco de las 34 viviendas de la lista figuran como reservadas. Nueve tienen precio, de {E849000} a {E1245000} más IVA.',
  'Vingt-cinq des 34 logements de la liste sont marqués comme réservés. Neuf figurent avec un prix, de {E849000} à {E1245000} hors TVA.',
  'Fünfundzwanzig der 34 Wohnungen der Liste sind als reserviert gekennzeichnet. Neun sind mit Preis aufgeführt, von {E849000} bis {E1245000} zuzüglich MwSt.',
  'Двадцать пять из 34 квартир списка помечены как зарезервированные. Девять указаны с ценой — от {E849000} до {E1245000} без НДС.',
  'خمسة وعشرون مسكنًا من أصل 34 في القائمة مُعلَّمة بأنها محجوزة. وتسعة منها مدرجة بالسعر، من {E849000} إلى {E1245000} دون ضريبة القيمة المضافة.',
  'Vijfentwintig van de 34 woningen op de lijst zijn als gereserveerd aangemerkt. Negen staan met een prijs op de lijst, van {E849000} tot {E1245000} excl. btw.',
  'Dwadzieścia pięć z 34 lokali z listy oznaczono jako zarezerwowane. Dziewięć ma podaną cenę, od {E849000} do {E1245000} plus VAT.',
  'Tjuefem av de 34 boligene på listen er merket som reservert. Ni er oppført med pris, fra {E849000} til {E1245000} pluss mva.',
  'Tjugofem av de 34 bostäderna på listan är markerade som reserverade. Nio är listade med pris, från {E849000} till {E1245000} plus IVA.')
a('The list shows an IVA amount beside each price, 10% of it, in a separate column. The prices exclude VAT, and Nueva Living confirms the rate and the purchase costs in writing.',
  'La lista muestra junto a cada precio un importe de IVA, el 10% del mismo, en una columna aparte. Los precios no incluyen el IVA, y Nueva Living confirma por escrito el tipo y los gastos de compra.',
  'La liste indique à côté de chaque prix un montant de TVA (IVA), égal à 10 % de celui-ci, dans une colonne distincte. Les prix s’entendent hors TVA, et Nueva Living confirme par écrit le taux et les frais d’achat.',
  'Die Liste zeigt neben jedem Preis in einer eigenen Spalte einen IVA-Betrag (spanische Mehrwertsteuer) von 10 % davon. Die Preise verstehen sich zuzüglich MwSt., und Nueva Living bestätigt den Satz und die Kaufnebenkosten schriftlich.',
  'В прайс-листе рядом с каждой ценой в отдельной колонке указана сумма IVA (испанского НДС) — 10 % от цены. Цены указаны без НДС, а ставку и расходы на покупку Nueva Living подтверждает письменно.',
  'تُظهر القائمة بجانب كل سعر مبلغ IVA (ضريبة القيمة المضافة الإسبانية)، وهو 10% منه، في عمود منفصل. والأسعار لا تشمل ضريبة القيمة المضافة، وتؤكد Nueva Living النسبة وتكاليف الشراء كتابةً.',
  'De lijst toont naast elke prijs in een aparte kolom een bedrag aan IVA (Spaanse btw), 10% ervan. De prijzen zijn exclusief btw, en Nueva Living bevestigt het tarief en de aankoopkosten schriftelijk.',
  'Cennik podaje obok każdej ceny w osobnej kolumnie kwotę IVA (hiszpańskiego VAT), równą 10% ceny. Ceny nie zawierają VAT, a stawkę i koszty zakupu Nueva Living potwierdza na piśmie.',
  'Listen viser et IVA-beløp (spansk mva.) ved siden av hver pris, 10 % av den, i en egen kolonne. Prisene inkluderer ikke mva., og Nueva Living bekrefter satsen og kjøpskostnadene skriftlig.',
  'Listan visar ett IVA-belopp (spansk moms) bredvid varje pris, 10 % av priset, i en egen kolumn. Priserna inkluderar inte IVA, och Nueva Living bekräftar skattesatsen och köpkostnaderna skriftligen.')
a('The documents we hold give no reservation amount and no payment schedule, so we ask for them in writing before any reservation.',
  'Los documentos que tenemos no dan importe de reserva ni calendario de pagos, así que los solicitamos por escrito antes de cualquier reserva.',
  'Les documents dont nous disposons ne donnent ni montant de réservation ni échéancier de paiement ; nous les demandons donc par écrit avant toute réservation.',
  'Die uns vorliegenden Unterlagen nennen weder einen Reservierungsbetrag noch einen Zahlungsplan, daher fragen wir beides vor jeder Reservierung schriftlich an.',
  'В имеющихся у нас документах нет ни суммы бронирования, ни графика платежей, поэтому до любого бронирования мы запрашиваем их письменно.',
  'لا تذكر الوثائق التي بحوزتنا مبلغ حجز ولا جدول دفعات، لذلك نطلبهما كتابةً قبل أي حجز.',
  'De documenten waarover we beschikken noemen geen reserveringsbedrag en geen betalingsschema, dus we vragen ze vóór elke reservering schriftelijk op.',
  'Dokumenty, którymi dysponujemy, nie podają kwoty rezerwacji ani harmonogramu płatności, dlatego przed każdą rezerwacją prosimy o nie na piśmie.',
  'Dokumentene vi har oppgir verken reservasjonsbeløp eller betalingsplan, så vi ber om dem skriftlig før enhver reservasjon.',
  'Dokumenten vi har anger varken reservationsbelopp eller betalningsplan, så vi begär dem skriftligen före varje reservation.')
a('The dossier shows garage spaces and storage rooms on three basement levels, but the price list does not say whether one comes with each home. We confirm it for the home you choose.',
  'El dosier muestra plazas de garaje y trasteros en tres plantas de sótano, pero la lista de precios no dice si cada vivienda incluye una. Lo confirmamos para la vivienda que usted elija.',
  'Le dossier montre des places de garage et des caves sur trois niveaux de sous-sol, mais la liste de prix ne dit pas si chaque logement en comprend une. Nous le confirmons pour le logement que vous choisissez.',
  'Die Broschüre zeigt Garagenstellplätze und Abstellräume auf drei Untergeschossen, aber die Preisliste sagt nicht, ob jeder Wohnung einer zugeordnet ist. Wir bestätigen das für die Wohnung, die Sie wählen.',
  'В брошюре показаны места в гараже и кладовые на трёх подземных уровнях, но в прайс-листе не сказано, закреплено ли за каждой квартирой по одному. Для выбранной вами квартиры мы это подтверждаем.',
  'يُظهر الكتيّب مواقف مرآب وغرف تخزين على ثلاثة مستويات سفلية، لكن قائمة الأسعار لا تذكر ما إذا كان لكل مسكن موقف وغرفة. ونؤكد ذلك للمسكن الذي تختارونه.',
  'De brochure toont garageplaatsen en bergingen op drie kelderlagen, maar de prijslijst zegt niet of er bij elke woning een hoort. We bevestigen het voor de woning die u kiest.',
  'Broszura pokazuje miejsca garażowe i komórki lokatorskie na trzech poziomach podziemnych, ale cennik nie mówi, czy do każdego lokalu przypisane jest jedno z nich. Potwierdzamy to dla lokalu wybranego przez Państwa.',
  'Brosjyren viser garasjeplasser og boder på tre kjellernivåer, men prislisten sier ikke om én følger med hver bolig. Vi bekrefter det for boligen som velges.',
  'Broschyren visar garageplatser och förråd på tre källarplan, men prislistan anger inte om en sådan följer med varje bostad. Vi bekräftar det för den bostad ni väljer.')

a('The documents we hold do not say whether the building licence has been granted or what stage the works have reached, and the specification is written in the future tense. We ask for the licence, its status and the start date of the works.',
  'Los documentos que tenemos no dicen si se ha concedido la licencia de obras ni en qué fase están las obras, y la memoria de calidades está redactada en futuro. Solicitamos la licencia, su estado y la fecha de inicio de las obras.',
  'Les documents dont nous disposons ne disent pas si le permis de construire a été accordé ni où en sont les travaux, et le descriptif des prestations est rédigé au futur. Nous demandons le permis, son statut et la date de début des travaux.',
  'Die uns vorliegenden Unterlagen sagen nicht, ob die Baugenehmigung erteilt wurde oder wie weit die Bauarbeiten sind, und die Baubeschreibung ist im Futur verfasst. Wir fragen die Genehmigung, ihren Status und den Baubeginn an.',
  'В имеющихся у нас документах не сказано, выдано ли разрешение на строительство и на какой стадии работы, а спецификация написана в будущем времени. Мы запрашиваем разрешение, его статус и дату начала работ.',
  'لا تذكر الوثائق التي بحوزتنا ما إذا كانت رخصة البناء قد مُنحت ولا المرحلة التي بلغتها الأعمال، كما أن المواصفات مكتوبة بصيغة المستقبل. ونطلب الرخصة وحالتها وتاريخ بدء الأعمال.',
  'De documenten waarover we beschikken zeggen niet of de bouwvergunning is verleend of hoe ver de werken zijn, en de specificatie is in de toekomende tijd geschreven. We vragen de vergunning, de status ervan en de startdatum van de werken op.',
  'Dokumenty, którymi dysponujemy, nie mówią, czy pozwolenie na budowę zostało wydane ani na jakim etapie są prace, a opis standardu jest napisany w czasie przyszłym. Prosimy o pozwolenie, jego status i datę rozpoczęcia prac.',
  'Dokumentene vi har sier ikke om byggetillatelsen er gitt eller hvor langt arbeidene har kommet, og spesifikasjonen er skrevet i futurum. Vi ber om tillatelsen, statusen og startdatoen for arbeidene.',
  'Dokumenten vi har säger inte om bygglovet har beviljats eller hur långt arbetena har kommit, och specifikationen är skriven i futurum. Vi begär bygglovet, dess status och startdatum för arbetena.')
a('The number of homes', 'El número de viviendas', 'Le nombre de logements', 'Die Anzahl der Wohnungen', 'Количество квартир',
  'عدد المساكن', 'Het aantal woningen', 'Liczba lokali', 'Antall boliger', 'Antalet bostäder')
a('The text of the dossier says 36 homes. Its plans and the price list show 34: 11 in block 1, 11 in block 2 and 12 in block 3. This page uses the 34 of the plans and the list, and we ask the developer to confirm the total.',
  'El texto del dosier habla de 36 viviendas. Sus planos y la lista de precios muestran 34: 11 en el bloque 1, 11 en el bloque 2 y 12 en el bloque 3. Esta página usa las 34 de los planos y la lista, y pedimos al promotor que confirme el total.',
  'Le texte du dossier parle de 36 logements. Ses plans et la liste de prix en montrent 34 : 11 dans l’immeuble 1, 11 dans l’immeuble 2 et 12 dans l’immeuble 3. Cette page retient les 34 des plans et de la liste, et nous demandons au promoteur de confirmer le total.',
  'Der Text der Broschüre spricht von 36 Wohnungen. Ihre Pläne und die Preisliste zeigen 34: 11 in Block 1, 11 in Block 2 und 12 in Block 3. Diese Seite verwendet die 34 aus den Plänen und der Liste, und wir bitten den Bauträger, die Gesamtzahl zu bestätigen.',
  'В тексте брошюры говорится о 36 квартирах. В её планах и в прайс-листе их 34: 11 в корпусе 1, 11 в корпусе 2 и 12 в корпусе 3. На этой странице использованы 34 квартиры из планов и списка, а общее число мы просим застройщика подтвердить.',
  'يذكر نص الكتيّب 36 مسكنًا. أما مخططاته وقائمة الأسعار فتُظهران 34: 11 في المبنى 1 و11 في المبنى 2 و12 في المبنى 3. وتعتمد هذه الصفحة الـ34 الواردة في المخططات والقائمة، ونطلب من المطوّر تأكيد العدد الإجمالي.',
  'De tekst van de brochure spreekt van 36 woningen. De plattegronden en de prijslijst tonen er 34: 11 in blok 1, 11 in blok 2 en 12 in blok 3. Deze pagina gebruikt de 34 van de plattegronden en de lijst, en we vragen de ontwikkelaar het totaal te bevestigen.',
  'Tekst broszury mówi o 36 lokalach. Jej rzuty i cennik pokazują 34: 11 w budynku 1, 11 w budynku 2 i 12 w budynku 3. Ta strona przyjmuje 34 z rzutów i listy, a o potwierdzenie łącznej liczby prosimy dewelopera.',
  'Teksten i brosjyren sier 36 boliger. Planene og prislisten viser 34: 11 i hus 1, 11 i hus 2 og 12 i hus 3. Denne siden bruker de 34 fra planene og listen, og vi ber utbyggeren bekrefte det totale antallet.',
  'Texten i broschyren anger 36 bostäder. Planritningarna och prislistan visar 34: 11 i hus 1, 11 i hus 2 och 12 i hus 3. Den här sidan använder de 34 från ritningarna och listan, och vi ber exploatören bekräfta det totala antalet.')
a('The price list and the plans agree on the built area of every home to within 0.02 sqm, but not on the terraces. For home 2-2B the list gives a terrace of 21.65 sqm and the plan 15.90 sqm, and for home 1-2A the list gives 20.40 sqm and the plan 18.30 sqm. The plans also give a second, larger built area under Decree 218/2005, 86.01 sqm for home 1-2A against 76.26 sqm. We confirm which figures the contract uses.',
  'La lista de precios y los planos coinciden en la superficie construida de cada vivienda con una diferencia máxima de {N0.02} {U}, pero no en las terrazas. Para la vivienda 2-2B la lista da una terraza de {N21.65} {U} y el plano de {N15.90} {U}, y para la vivienda 1-2A la lista da {N20.40} {U} y el plano {N18.30} {U}. Los planos dan además una segunda superficie construida, mayor, según el Decreto 218/2005: {N86.01} {U} para la vivienda 1-2A frente a {N76.26} {U}. Confirmamos qué cifras usa el contrato.',
  'La liste de prix et les plans concordent sur la surface construite de chaque logement à {N0.02} {U} près, mais pas sur les terrasses. Pour le logement 2-2B, la liste donne une terrasse de {N21.65} {U} et le plan de {N15.90} {U}, et pour le logement 1-2A la liste donne {N20.40} {U} et le plan {N18.30} {U}. Les plans donnent aussi une seconde surface construite, plus grande, selon le décret 218/2005 : {N86.01} {U} pour le logement 1-2A contre {N76.26} {U}. Nous confirmons quels chiffres retient le contrat.',
  'Die Preisliste und die Pläne stimmen bei der bebauten Fläche jeder Wohnung auf {N0.02} {U} genau überein, nicht aber bei den Terrassen. Für Wohnung 2-2B gibt die Liste eine Terrasse von {N21.65} {U} an und der Plan {N15.90} {U}, für Wohnung 1-2A die Liste {N20.40} {U} und der Plan {N18.30} {U}. Die Pläne nennen außerdem eine zweite, größere bebaute Fläche nach dem Dekret 218/2005: {N86.01} {U} für Wohnung 1-2A gegenüber {N76.26} {U}. Wir bestätigen, welche Zahlen der Vertrag verwendet.',
  'Прайс-лист и планы совпадают по застроенной площади каждой квартиры с точностью до {N0.02} {U}, но не по террасам. Для квартиры 2-2B в прайс-листе терраса {N21.65} {U}, а на плане {N15.90} {U}; для квартиры 1-2A в прайс-листе {N20.40} {U}, на плане {N18.30} {U}. На планах указана и вторая, большая застроенная площадь по декрету 218/2005: {N86.01} {U} для квартиры 1-2A против {N76.26} {U}. Мы уточняем, какие цифры берёт договор.',
  'تتطابق قائمة الأسعار والمخططات في المساحة المبنية لكل مسكن بفارق لا يتجاوز {N0.02} {U}، لكنها تختلف في التراسات. فبالنسبة إلى المسكن 2-2B تذكر القائمة تراسًا بمساحة {N21.65} {U} والمخطط {N15.90} {U}، وبالنسبة إلى المسكن 1-2A تذكر القائمة {N20.40} {U} والمخطط {N18.30} {U}. وتذكر المخططات أيضًا مساحة مبنية ثانية أكبر بموجب المرسوم 218/2005، هي {N86.01} {U} للمسكن 1-2A مقابل {N76.26} {U}. ونؤكد أي الأرقام يعتمدها العقد.',
  'De prijslijst en de plattegronden komen voor elke woning tot op {N0.02} {U} overeen qua bebouwde oppervlakte, maar niet qua terrassen. Voor woning 2-2B geeft de lijst een terras van {N21.65} {U} en de plattegrond {N15.90} {U}, en voor woning 1-2A geeft de lijst {N20.40} {U} en de plattegrond {N18.30} {U}. De plattegronden geven bovendien een tweede, grotere bebouwde oppervlakte volgens decreet 218/2005: {N86.01} {U} voor woning 1-2A tegenover {N76.26} {U}. We bevestigen welke cijfers het contract hanteert.',
  'Cennik i rzuty zgadzają się co do powierzchni zabudowy każdego lokalu z dokładnością do {N0.02} {U}, ale nie co do tarasów. Dla lokalu 2-2B cennik podaje taras o powierzchni {N21.65} {U}, a rzut {N15.90} {U}, natomiast dla lokalu 1-2A cennik podaje {N20.40} {U}, a rzut {N18.30} {U}. Rzuty podają też drugą, większą powierzchnię zabudowy według dekretu 218/2005: {N86.01} {U} dla lokalu 1-2A wobec {N76.26} {U}. Potwierdzamy, jakie wartości przyjmuje umowa.',
  'Prislisten og plantegningene stemmer overens om bebygd areal for hver bolig med et avvik på høyst {N0.02} {U}, men ikke om terrassene. For bolig 2-2B oppgir listen en terrasse på {N21.65} {U} og plantegningen {N15.90} {U}, og for bolig 1-2A oppgir listen {N20.40} {U} og plantegningen {N18.30} {U}. Plantegningene oppgir også et andre, større bebygd areal etter dekret 218/2005: {N86.01} {U} for bolig 1-2A mot {N76.26} {U}. Vi bekrefter hvilke tall kontrakten bruker.',
  'Prislistan och planritningarna stämmer överens om byggytan för varje bostad med högst {N0.02} {U} i skillnad, men inte om terrasserna. För bostad 2-2B anger listan en terrass på {N21.65} {U} och planritningen {N15.90} {U}, och för bostad 1-2A anger listan {N20.40} {U} och planritningen {N18.30} {U}. Planritningarna anger också en andra, större byggyta enligt dekret 218/2005: {N86.01} {U} för bostad 1-2A mot {N76.26} {U}. Vi bekräftar vilka siffror avtalet använder.')
a('The price list is headed “Blue Horizon. Listado de ventas” and carries no date inside it. Its file name reads “October 26”, which we take as October 2026, and we confirm each price before any reservation.',
  'La lista de precios lleva por título «Blue Horizon. Listado de ventas» y no incluye ninguna fecha. El nombre del archivo dice «octubre 26», que entendemos como octubre de 2026, y confirmamos cada precio antes de cualquier reserva.',
  'La liste de prix est intitulée « Blue Horizon. Listado de ventas » et ne porte aucune date. Le nom du fichier indique « octobre 26 », que nous lisons comme octobre 2026, et nous confirmons chaque prix avant toute réservation.',
  'Die Preisliste trägt die Überschrift „Blue Horizon. Listado de ventas“ und enthält kein Datum. Der Dateiname lautet „Oktober 26“, was wir als Oktober 2026 lesen, und wir bestätigen jeden Preis vor jeder Reservierung.',
  'Прайс-лист озаглавлен «Blue Horizon. Listado de ventas» и не содержит даты. В названии файла стоит «октябрь 26», что мы читаем как октябрь 2026 года, и каждую цену мы подтверждаем до любого бронирования.',
  'عنوان قائمة الأسعار «Blue Horizon. Listado de ventas» ولا تحمل أي تاريخ في داخلها. واسم الملف هو «أكتوبر 26»، ونفهمه على أنه أكتوبر 2026، ونؤكد كل سعر قبل أي حجز.',
  'De prijslijst heeft als kop “Blue Horizon. Listado de ventas” en bevat zelf geen datum. De bestandsnaam luidt “oktober 26”, wat we lezen als oktober 2026, en we bevestigen elke prijs vóór elke reservering.',
  'Cennik nosi tytuł „Blue Horizon. Listado de ventas” i nie zawiera daty. Nazwa pliku brzmi „październik 26”, co odczytujemy jako październik 2026 r., a każdą cenę potwierdzamy przed rezerwacją.',
  'Prislisten har overskriften «Blue Horizon. Listado de ventas» og har ingen dato i seg. Filnavnet lyder «oktober 26», som vi leser som oktober 2026, og vi bekrefter hver pris før enhver reservasjon.',
  'Prislistan har rubriken ”Blue Horizon. Listado de ventas” och saknar datum. Filnamnet lyder ”oktober 26”, vilket vi läser som oktober 2026, och vi bekräftar varje pris före varje reservation.')
a('The map and the distances', 'El mapa y las distancias', 'La carte et les distances', 'Die Karte und die Entfernungen', 'Карта и расстояния',
  'الخريطة والمسافات', 'De kaart en de afstanden', 'Mapa i odległości', 'Kartet og avstandene', 'Kartan och avstånden')
a('The documents give no address or coordinates, so the marker on the map is at the centre of Estepona and not on the plot, and the road distances beside the map are measured from that marker. The dossier gives La Rada beach as 5 minutes away without saying whether on foot or by car, and Málaga airport as 45 minutes away; we confirm the distances on a visit.',
  'Los documentos no dan dirección ni coordenadas, así que el marcador del mapa está en el centro de Estepona y no en la parcela, y las distancias por carretera junto al mapa se miden desde ese marcador. El dosier sitúa la playa de la Rada a 5 minutos sin decir si a pie o en coche, y el aeropuerto de Málaga a 45 minutos; confirmamos las distancias en una visita.',
  'Les documents ne donnent ni adresse ni coordonnées ; le repère sur la carte se trouve donc au centre d’Estepona et non sur la parcelle, et les distances routières à côté de la carte sont mesurées depuis ce repère. Le dossier place la plage de La Rada à 5 minutes sans préciser si à pied ou en voiture, et l’aéroport de Málaga à 45 minutes ; nous confirmons les distances lors d’une visite.',
  'Die Unterlagen nennen weder Adresse noch Koordinaten, daher liegt die Markierung auf der Karte im Zentrum von Estepona und nicht auf dem Grundstück, und die Straßenentfernungen neben der Karte sind von dieser Markierung aus gemessen. Die Broschüre nennt den Strand La Rada in 5 Minuten Entfernung, ohne zu sagen, ob zu Fuß oder mit dem Auto, und den Flughafen Málaga in 45 Minuten; die Entfernungen bestätigen wir bei einer Besichtigung.',
  'В документах нет ни адреса, ни координат, поэтому отметка на карте стоит в центре Эстепоны, а не на участке, а расстояния по дорогам рядом с картой измерены от этой отметки. В брошюре пляж Ла-Рада указан в 5 минутах без уточнения, пешком или на машине, а аэропорт Малаги — в 45 минутах; расстояния мы уточняем во время визита.',
  'لا تذكر الوثائق عنوانًا ولا إحداثيات، لذلك فإن العلامة على الخريطة في وسط إستيبونا وليست على قطعة الأرض، وتُقاس مسافات الطرق بجانب الخريطة انطلاقًا من هذه العلامة. ويذكر الكتيّب أن شاطئ لا رادا على بُعد 5 دقائق دون توضيح ما إذا كان ذلك سيرًا على الأقدام أم بالسيارة، وأن مطار ملقة على بُعد 45 دقيقة؛ ونؤكد المسافات أثناء الزيارة.',
  'De documenten geven geen adres of coördinaten, dus de markering op de kaart staat in het centrum van Estepona en niet op het perceel, en de wegafstanden naast de kaart zijn vanaf die markering gemeten. De brochure noemt het strand La Rada op 5 minuten zonder te zeggen of te voet of met de auto, en de luchthaven van Málaga op 45 minuten; de afstanden bevestigen we bij een bezichtiging.',
  'Dokumenty nie podają adresu ani współrzędnych, dlatego znacznik na mapie znajduje się w centrum Estepony, a nie na działce, a odległości drogowe obok mapy są mierzone od tego znacznika. Broszura podaje plażę La Rada w odległości 5 minut bez wskazania, czy pieszo, czy samochodem, a lotnisko w Maladze w odległości 45 minut; odległości potwierdzamy podczas wizyty.',
  'Dokumentene oppgir verken adresse eller koordinater, så markøren på kartet ligger i sentrum av Estepona og ikke på tomten, og veiavstandene ved siden av kartet er målt fra denne markøren. Brosjyren oppgir stranden La Rada 5 minutter unna uten å si om til fots eller med bil, og Málaga lufthavn 45 minutter unna; avstandene bekrefter vi på en visning.',
  'Dokumenten anger varken adress eller koordinater, så markören på kartan ligger i centrala Estepona och inte på tomten, och vägavstånden bredvid kartan är mätta från den markören. Broschyren anger stranden La Rada 5 minuter bort utan att säga om till fots eller med bil, och Málaga flygplats 45 minuter bort; avstånden bekräftar vi vid ett besök.')

a('Nine homes <em>currently available</em>',
  'Nueve viviendas <em>disponibles actualmente</em>', 'Neuf logements <em>actuellement disponibles</em>', 'Neun Wohnungen <em>aktuell verfügbar</em>',
  'Девять квартир <em>сейчас в продаже</em>', 'تسعة مساكن <em>متاحة حاليًا</em>', 'Negen woningen <em>momenteel beschikbaar</em>',
  'Dziewięć lokali <em>obecnie dostępnych</em>', 'Ni boliger <em>for tiden tilgjengelige</em>', 'Nio bostäder <em>för närvarande tillgängliga</em>')
a('Nine apartments are listed with a price: four with two bedrooms and five with three, on the first to the fourth floor of blocks 1, 2 and 3. Prices are those of the developer’s price list as of October 2026 and exclude VAT, and we confirm availability and price before any reservation. The other 25 homes on the list are marked reserved and are not available.',
  'Figuran nueve apartamentos con precio: cuatro de dos dormitorios y cinco de tres, entre la primera y la cuarta planta de los bloques 1, 2 y 3. Los precios son los de la lista de precios del promotor a octubre de 2026 y no incluyen IVA; confirmamos la disponibilidad y el precio antes de cualquier reserva. Las otras 25 viviendas de la lista figuran como reservadas y no están disponibles.',
  'Neuf appartements sont listés avec un prix : quatre de deux chambres et cinq de trois, du premier au quatrième étage des immeubles 1, 2 et 3. Les prix sont ceux de la liste de prix du promoteur à octobre 2026 et s’entendent hors TVA ; nous confirmons la disponibilité et le prix avant toute réservation. Les 25 autres logements de la liste sont marqués comme réservés et ne sont pas disponibles.',
  'Neun Wohnungen sind mit Preis aufgeführt: vier mit zwei und fünf mit drei Schlafzimmern, im ersten bis vierten Obergeschoss der Blöcke 1, 2 und 3. Die Preise stammen aus der Preisliste des Bauträgers mit Stand Oktober 2026 und verstehen sich zuzüglich MwSt.; Verfügbarkeit und Preis bestätigen wir vor jeder Reservierung. Die übrigen 25 Wohnungen der Liste sind als reserviert gekennzeichnet und nicht verfügbar.',
  'С ценой указаны девять квартир: четыре с двумя спальнями и пять с тремя, со второго по пятый этаж корпусов 1, 2 и 3. Цены взяты из прайс-листа застройщика по состоянию на октябрь 2026 года и не включают НДС; наличие и цену мы подтверждаем до любого бронирования. Остальные 25 квартир списка помечены как зарезервированные и недоступны.',
  'تُعرض تسع شقق بالسعر: أربع بغرفتي نوم وخمس بثلاث غرف نوم، من الطابق الأول إلى الرابع في المباني 1 و2 و3. الأسعار وفق قائمة أسعار المطوّر حتى أكتوبر 2026 ولا تشمل ضريبة القيمة المضافة، ونؤكد التوفر والسعر قبل أي حجز. أما المساكن الـ25 الأخرى في القائمة فهي مُعلَّمة بأنها محجوزة وغير متاحة.',
  'Negen appartementen staan met een prijs vermeld: vier met twee slaapkamers en vijf met drie, op de eerste tot en met de vierde verdieping van blok 1, 2 en 3. De prijzen zijn die van de prijslijst van de ontwikkelaar per oktober 2026 en zijn exclusief btw; wij bevestigen beschikbaarheid en prijs vóór elke reservering. De overige 25 woningen op de lijst zijn als gereserveerd aangemerkt en niet beschikbaar.',
  'Dziewięć mieszkań ma podaną cenę: cztery z dwiema sypialniami i pięć z trzema, od pierwszego do czwartego piętra w budynkach 1, 2 i 3. Ceny pochodzą z cennika dewelopera według stanu na październik 2026 r. i nie zawierają VAT; dostępność i cenę potwierdzamy przed każdą rezerwacją. Pozostałe 25 lokali z listy oznaczono jako zarezerwowane i nie są dostępne.',
  'Ni leiligheter er oppført med pris: fire med to soverom og fem med tre, i andre til femte etasje i hus 1, 2 og 3. Prisene er de i utbyggerens prisliste per oktober 2026 og er eksklusive mva.; vi bekrefter tilgjengelighet og pris før enhver reservasjon. De øvrige 25 boligene på listen er merket som reservert og er ikke tilgjengelige.',
  'Nio lägenheter är listade med pris: fyra med två sovrum och fem med tre, på första till fjärde våningen i hus 1, 2 och 3. Priserna är de i exploatörens prislista per oktober 2026 och är exklusive IVA; vi bekräftar tillgänglighet och pris före varje reservation. De övriga 25 bostäderna på listan är markerade som reserverade och är inte tillgängliga.')
a('Prices, bedrooms, built areas and terraces are transcribed from the developer’s price list for the nine homes it shows with a price, out of 34 rows, as of October 2026. The list marks the other 25 rows as reserved. It shows an IVA amount of 10% beside each price, so the prices exclude VAT. The built area on the list matches the plans to within 0.02 sqm; the terraces differ, and both figures are given for each home type above.',
  'Los precios, los dormitorios, las superficies construidas y las terrazas se han transcrito de la lista de precios del promotor para las nueve viviendas que figuran con precio, de un total de 34 filas, a octubre de 2026. La lista marca las otras 25 filas como reservadas. Muestra un importe de IVA del 10% junto a cada precio, por lo que los precios no incluyen el IVA. La superficie construida de la lista coincide con la de los planos con una diferencia máxima de {N0.02} {U}; las terrazas difieren, y se dan ambas cifras para cada tipo de vivienda más arriba.',
  'Les prix, les chambres, les surfaces construites et les terrasses sont transcrits de la liste de prix du promoteur pour les neuf logements qu’elle présente avec un prix, sur 34 lignes, à octobre 2026. La liste marque les 25 autres lignes comme réservées. Elle indique un montant de TVA (IVA) de 10 % à côté de chaque prix, de sorte que les prix s’entendent hors TVA. La surface construite de la liste correspond à celle des plans à {N0.02} {U} près ; les terrasses diffèrent, et les deux chiffres sont donnés pour chaque type de logement ci-dessus.',
  'Preise, Schlafzimmer, bebaute Flächen und Terrassen sind aus der Preisliste des Bauträgers für die neun Wohnungen übernommen, die sie mit Preis zeigt, von 34 Zeilen, mit Stand Oktober 2026. Die Liste kennzeichnet die übrigen 25 Zeilen als reserviert. Sie weist neben jedem Preis einen IVA-Betrag von 10 % aus, die Preise verstehen sich daher zuzüglich MwSt. Die bebaute Fläche der Liste stimmt mit den Plänen auf {N0.02} {U} genau überein; die Terrassen weichen ab, und beide Werte sind oben für jeden Wohnungstyp angegeben.',
  'Цены, спальни, застроенные площади и террасы перенесены из прайс-листа застройщика для девяти квартир, которые в нём указаны с ценой, из 34 строк, по состоянию на октябрь 2026 года. Остальные 25 строк в списке помечены как зарезервированные. Рядом с каждой ценой указана сумма IVA — 10 %, поэтому цены даны без НДС. Застроенная площадь в прайс-листе совпадает с планами с точностью до {N0.02} {U}; террасы различаются, и обе цифры приведены выше для каждого типа квартир.',
  'نُقلت الأسعار وعدد غرف النوم والمساحات المبنية والتراسات من قائمة أسعار المطوّر للمساكن التسعة التي تعرضها بالسعر، من أصل 34 صفًا، حتى أكتوبر 2026. وتُعلِّم القائمة الصفوف الـ25 الأخرى بأنها محجوزة. وتُظهر مبلغ IVA بنسبة 10% بجانب كل سعر، لذلك فالأسعار لا تشمل ضريبة القيمة المضافة. وتتطابق المساحة المبنية في القائمة مع المخططات بفارق لا يتجاوز {N0.02} {U}؛ أما التراسات فتختلف، وقد أُوردت الرقمان لكل نوع من المساكن أعلاه.',
  'Prijzen, slaapkamers, bebouwde oppervlakten en terrassen zijn overgenomen uit de prijslijst van de ontwikkelaar voor de negen woningen die zij met een prijs toont, van 34 rijen, per oktober 2026. De lijst markeert de overige 25 rijen als gereserveerd. Ze toont naast elke prijs een IVA-bedrag van 10%, dus de prijzen zijn exclusief btw. De bebouwde oppervlakte op de lijst komt tot op {N0.02} {U} overeen met de plattegronden; de terrassen wijken af, en beide cijfers staan hierboven bij elk woningtype.',
  'Ceny, liczba sypialni, powierzchnie zabudowy i tarasy zostały przepisane z cennika dewelopera dla dziewięciu lokali, które pokazuje z ceną, spośród 34 wierszy, według stanu na październik 2026 r. Cennik oznacza pozostałe 25 wierszy jako zarezerwowane. Obok każdej ceny podaje kwotę IVA w wysokości 10%, więc ceny nie zawierają VAT. Powierzchnia zabudowy z cennika zgadza się z rzutami z dokładnością do {N0.02} {U}; tarasy się różnią, a obie wartości podano wyżej dla każdego typu lokalu.',
  'Priser, soverom, bebygde arealer og terrasser er hentet fra utbyggerens prisliste for de ni boligene den viser med pris, av 34 rader, per oktober 2026. Listen merker de øvrige 25 radene som reservert. Den viser et IVA-beløp på 10 % ved siden av hver pris, så prisene er eksklusive mva. Bebygd areal på listen stemmer med plantegningene med et avvik på høyst {N0.02} {U}; terrassene avviker, og begge tallene er oppgitt for hver boligtype over.',
  'Priser, sovrum, byggytor och terrasser är hämtade från exploatörens prislista för de nio bostäder som den visar med pris, av 34 rader, per oktober 2026. Listan markerar de övriga 25 raderna som reserverade. Den visar ett IVA-belopp på 10 % bredvid varje pris, så priserna är exklusive IVA. Byggytan på listan stämmer med planritningarna med högst {N0.02} {U} i skillnad; terrasserna avviker, och båda siffrorna anges för varje bostadstyp ovan.')

# ---- timeline, viewing, enquiry, FAQ ------------------------------------------------------------

a('We confirm the reservation amount and the payment schedule in writing, then the purchase contract.',
  'Confirmamos por escrito el importe de la reserva y el calendario de pagos, y después el contrato de compraventa.',
  'Nous confirmons par écrit le montant de la réservation et l’échéancier de paiement, puis le contrat de vente.',
  'Wir bestätigen den Reservierungsbetrag und den Zahlungsplan schriftlich, danach folgt der Kaufvertrag.',
  'Мы письменно подтверждаем сумму бронирования и график платежей, затем следует договор купли-продажи.',
  'نؤكد مبلغ الحجز وجدول الدفعات كتابةً، ثم يأتي عقد الشراء.',
  'We bevestigen het reserveringsbedrag en het betalingsschema schriftelijk, daarna volgt de koopovereenkomst.',
  'Potwierdzamy na piśmie kwotę rezerwacji i harmonogram płatności, a następnie przygotowujemy umowę kupna.',
  'Vi bekrefter reservasjonsbeløpet og betalingsplanen skriftlig, deretter følger kjøpekontrakten.',
  'Vi bekräftar reservationsbeloppet och betalningsplanen skriftligen, därefter följer köpeavtalet.')
a('On the plans', 'En los planos', 'Sur les plans', 'Anhand der Pläne', 'По планам', 'على المخططات', 'Op de plattegronden', 'Na rzutach', 'På plantegningene', 'På ritningarna')
a('We go through the home you choose, room by room, against its floorplan.',
  'Recorremos con usted la vivienda que elija, estancia por estancia, con su plano en la mano.',
  'Nous parcourons avec vous le logement que vous choisissez, pièce par pièce, plan en main.',
  'Wir gehen die Wohnung, die Sie wählen, Raum für Raum anhand ihres Grundrisses mit Ihnen durch.',
  'Мы вместе с вами обходим выбранную квартиру комната за комнатой, сверяясь с её планировкой.',
  'نتجوّل معكم في المسكن الذي تختارونه، غرفةً غرفة، بالاستناد إلى مخططه.',
  'We lopen met u door de woning die u kiest, kamer voor kamer, aan de hand van de plattegrond.',
  'Przechodzimy z Państwem przez wybrany lokal pomieszczenie po pomieszczeniu, z rzutem w ręku.',
  'Vi går gjennom boligen som velges, rom for rom, med plantegningen i hånden.',
  'Vi går igenom den bostad ni väljer, rum för rum, med planritningen i handen.')
a('Ask about <em>Las Mesas Blue Horizon</em>',
  'Pregunte por <em>Las Mesas Blue Horizon</em>', 'Renseignez-vous sur <em>Las Mesas Blue Horizon</em>', 'Fragen Sie nach <em>Las Mesas Blue Horizon</em>',
  'Узнайте о <em>Las Mesas Blue Horizon</em>', 'اسأل عن <em>Las Mesas Blue Horizon</em>', 'Vraag naar <em>Las Mesas Blue Horizon</em>',
  'Zapytaj o <em>Las Mesas Blue Horizon</em>', 'Spør om <em>Las Mesas Blue Horizon</em>', 'Fråga om <em>Las Mesas Blue Horizon</em>')
a('Hello Nueva Living, I would like information about Las Mesas Blue Horizon.',
  'Hola Nueva Living, me gustaría recibir información sobre Las Mesas Blue Horizon.',
  'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Las Mesas Blue Horizon.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Las Mesas Blue Horizon.',
  'Здравствуйте, Nueva Living! Я хотел бы получить информацию о Las Mesas Blue Horizon.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Las Mesas Blue Horizon.',
  'Hallo Nueva Living, ik zou graag informatie ontvangen over Las Mesas Blue Horizon.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Las Mesas Blue Horizon.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Las Mesas Blue Horizon.',
  'Hej Nueva Living, jag skulle vilja ha information om Las Mesas Blue Horizon.')
a('The text of the dossier says 36 homes, but its plans and the price list show 34, with two or three bedrooms. Nine are listed with a price, from EUR 849,000 to EUR 1,245,000 plus VAT, and the other 25 are marked reserved.',
  'El texto del dosier habla de 36 viviendas, pero sus planos y la lista de precios muestran 34, de dos o tres dormitorios. Nueve figuran con precio, de {E849000} a {E1245000} más IVA, y las otras 25 figuran como reservadas.',
  'Le texte du dossier parle de 36 logements, mais ses plans et la liste de prix en montrent 34, de deux ou trois chambres. Neuf figurent avec un prix, de {E849000} à {E1245000} hors TVA, et les 25 autres sont marqués comme réservés.',
  'Der Text der Broschüre spricht von 36 Wohnungen, doch ihre Pläne und die Preisliste zeigen 34, mit zwei oder drei Schlafzimmern. Neun sind mit Preis aufgeführt, von {E849000} bis {E1245000} zuzüglich MwSt., die übrigen 25 sind als reserviert gekennzeichnet.',
  'В тексте брошюры говорится о 36 квартирах, но в её планах и в прайс-листе их 34, с двумя или тремя спальнями. Девять указаны с ценой — от {E849000} до {E1245000} без НДС, остальные 25 помечены как зарезервированные.',
  'يذكر نص الكتيّب 36 مسكنًا، لكن مخططاته وقائمة الأسعار تُظهران 34 مسكنًا بغرفتي نوم أو ثلاث غرف نوم. وتسعة منها مدرجة بالسعر، من {E849000} إلى {E1245000} دون ضريبة القيمة المضافة، والـ25 الأخرى مُعلَّمة بأنها محجوزة.',
  'De tekst van de brochure spreekt van 36 woningen, maar de plattegronden en de prijslijst tonen er 34, met twee of drie slaapkamers. Negen staan met een prijs op de lijst, van {E849000} tot {E1245000} excl. btw, en de andere 25 zijn als gereserveerd aangemerkt.',
  'Tekst broszury mówi o 36 lokalach, ale jej rzuty i cennik pokazują 34, z dwiema lub trzema sypialniami. Dziewięć ma podaną cenę, od {E849000} do {E1245000} plus VAT, a pozostałe 25 oznaczono jako zarezerwowane.',
  'Teksten i brosjyren sier 36 boliger, men planene og prislisten viser 34, med to eller tre soverom. Ni er oppført med pris, fra {E849000} til {E1245000} pluss mva., og de øvrige 25 er merket som reservert.',
  'Texten i broschyren anger 36 bostäder, men planritningarna och prislistan visar 34, med två eller tre sovrum. Nio är listade med pris, från {E849000} till {E1245000} plus IVA, och de övriga 25 är markerade som reserverade.')
a('No. The price list shows an IVA amount of 10% in a separate column, so the prices exclude VAT. We confirm the taxes and the purchase costs in writing.',
  'No. La lista de precios muestra un importe de IVA del 10% en una columna aparte, por lo que los precios no incluyen el IVA. Confirmamos por escrito los impuestos y los gastos de compra.',
  'Non. La liste de prix indique un montant de TVA (IVA) de 10 % dans une colonne distincte, de sorte que les prix s’entendent hors TVA. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Die Preisliste weist in einer eigenen Spalte einen IVA-Betrag von 10 % aus, die Preise verstehen sich daher zuzüglich MwSt. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе в отдельной колонке указана сумма IVA в размере 10 %, поэтому цены даны без НДС. Налоги и расходы на покупку мы подтверждаем письменно.',
  'لا. تُظهر قائمة الأسعار مبلغ IVA بنسبة 10% في عمود منفصل، لذلك فالأسعار لا تشمل ضريبة القيمة المضافة. ونؤكد الضرائب وتكاليف الشراء كتابةً.',
  'Nee. De prijslijst toont in een aparte kolom een IVA-bedrag van 10%, dus de prijzen zijn exclusief btw. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Nie. Cennik podaje w osobnej kolumnie kwotę IVA w wysokości 10%, więc ceny nie zawierają VAT. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Prislisten viser et IVA-beløp på 10 % i en egen kolonne, så prisene er eksklusive mva. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Nej. Prislistan visar ett IVA-belopp på 10 % i en egen kolumn, så priserna är exklusive IVA. Vi bekräftar skatter och köpkostnader skriftligen.')
a('The dossier shows 37 garage spaces and 37 storage rooms on three basement levels. The price list does not say whether one comes with each home, so we confirm it for the home you choose.',
  'El dosier muestra 37 plazas de garaje y 37 trasteros en tres plantas de sótano. La lista de precios no dice si cada vivienda incluye uno, así que lo confirmamos para la vivienda que usted elija.',
  'Le dossier montre 37 places de garage et 37 caves sur trois niveaux de sous-sol. La liste de prix ne dit pas si chaque logement en comprend une, nous le confirmons donc pour le logement que vous choisissez.',
  'Die Broschüre zeigt 37 Garagenstellplätze und 37 Abstellräume auf drei Untergeschossen. Die Preisliste sagt nicht, ob jeder Wohnung einer zugeordnet ist, daher bestätigen wir das für die Wohnung, die Sie wählen.',
  'В брошюре показаны 37 мест в гараже и 37 кладовых на трёх подземных уровнях. В прайс-листе не сказано, закреплено ли за каждой квартирой по одному, поэтому для выбранной вами квартиры мы это подтверждаем.',
  'يُظهر الكتيّب 37 موقفًا في المرآب و37 غرفة تخزين على ثلاثة مستويات سفلية. ولا تذكر قائمة الأسعار ما إذا كان لكل مسكن موقف وغرفة، لذلك نؤكد ذلك للمسكن الذي تختارونه.',
  'De brochure toont 37 garageplaatsen en 37 bergingen op drie kelderlagen. De prijslijst zegt niet of er bij elke woning een hoort, dus we bevestigen het voor de woning die u kiest.',
  'Broszura pokazuje 37 miejsc garażowych i 37 komórek lokatorskich na trzech poziomach podziemnych. Cennik nie mówi, czy do każdego lokalu przypisane jest jedno z nich, dlatego potwierdzamy to dla lokalu wybranego przez Państwa.',
  'Brosjyren viser 37 garasjeplasser og 37 boder på tre kjellernivåer. Prislisten sier ikke om én følger med hver bolig, så vi bekrefter det for boligen som velges.',
  'Broschyren visar 37 garageplatser och 37 förråd på tre källarplan. Prislistan anger inte om en sådan följer med varje bostad, så vi bekräftar det för den bostad ni väljer.')
a('The dossier describes panoramic views of the Mediterranean for the project but does not say which homes have them, so we confirm the view from the home you choose.',
  'El dosier describe vistas panorámicas al Mediterráneo para el conjunto, pero no dice qué viviendas las tienen, así que confirmamos la vista de la vivienda que usted elija.',
  'Le dossier décrit des vues panoramiques sur la Méditerranée pour l’ensemble, mais ne dit pas quels logements en bénéficient ; nous confirmons donc la vue du logement que vous choisissez.',
  'Die Broschüre beschreibt für die Anlage Panoramablick auf das Mittelmeer, sagt aber nicht, welche Wohnungen ihn haben, daher bestätigen wir die Aussicht der Wohnung, die Sie wählen.',
  'В брошюре для комплекса описан панорамный вид на Средиземное море, но не сказано, у каких квартир он есть, поэтому вид из выбранной вами квартиры мы подтверждаем.',
  'يصف الكتيّب إطلالات بانورامية على البحر المتوسط للمشروع دون أن يذكر أي المساكن تتمتع بها، لذلك نؤكد الإطلالة من المسكن الذي تختارونه.',
  'De brochure beschrijft voor het complex panoramisch uitzicht op de Middellandse Zee, maar zegt niet welke woningen dat hebben, dus we bevestigen het uitzicht vanuit de woning die u kiest.',
  'Broszura opisuje dla osiedla panoramiczny widok na Morze Śródziemne, ale nie mówi, które lokale go mają, dlatego potwierdzamy widok z lokalu wybranego przez Państwa.',
  'Brosjyren beskriver panoramautsikt over Middelhavet for prosjektet, men sier ikke hvilke boliger som har den, så vi bekrefter utsikten fra boligen som velges.',
  'Broschyren beskriver panoramautsikt över Medelhavet för området men anger inte vilka bostäder som har den, så vi bekräftar utsikten från den bostad ni väljer.')
a('No. The furniture shown in the images is not included. The kitchen is delivered furnished and with appliances, as the specification says.',
  'No. El mobiliario que aparece en las imágenes no está incluido. La cocina se entrega amueblada y con electrodomésticos, según indica la memoria de calidades.',
  'Non. Le mobilier représenté sur les images n’est pas inclus. La cuisine est livrée équipée et avec électroménager, comme l’indique le descriptif.',
  'Nein. Die auf den Bildern gezeigten Möbel sind nicht enthalten. Die Küche wird möbliert und mit Geräten übergeben, wie es die Baubeschreibung angibt.',
  'Нет. Мебель, показанная на изображениях, не входит в комплектацию. Кухня передаётся меблированной и с техникой, как сказано в спецификации.',
  'لا. الأثاث الظاهر في الصور غير مشمول. ويُسلَّم المطبخ مؤثثًا ومزودًا بالأجهزة، كما تنص المواصفات.',
  'Nee. Het meubilair dat op de beelden te zien is, is niet inbegrepen. De keuken wordt gemeubileerd en met apparatuur opgeleverd, zoals de specificatie aangeeft.',
  'Nie. Meble pokazane na obrazach nie wchodzą w cenę. Kuchnia jest przekazywana umeblowana i ze sprzętem, jak podaje opis standardu.',
  'Nei. Møblene som vises på bildene er ikke inkludert. Kjøkkenet leveres møblert og med hvitevarer, slik spesifikasjonen angir.',
  'Nej. Möblerna som visas på bilderna ingår inte. Köket levereras möblerat och med vitvaror, som specifikationen anger.')
a('The documents we hold give no reservation amount and no payment schedule. We ask for them and put them in writing.',
  'Los documentos que tenemos no dan importe de reserva ni calendario de pagos. Los solicitamos y los ponemos por escrito.',
  'Les documents dont nous disposons ne donnent ni montant de réservation ni échéancier de paiement. Nous les demandons et les mettons par écrit.',
  'Die uns vorliegenden Unterlagen nennen weder einen Reservierungsbetrag noch einen Zahlungsplan. Wir fragen beides an und halten es schriftlich fest.',
  'В имеющихся у нас документах нет ни суммы бронирования, ни графика платежей. Мы запрашиваем их и фиксируем письменно.',
  'لا تذكر الوثائق التي بحوزتنا مبلغ حجز ولا جدول دفعات. نطلبهما ونوثّقهما كتابةً.',
  'De documenten waarover we beschikken noemen geen reserveringsbedrag en geen betalingsschema. We vragen ze op en leggen ze schriftelijk vast.',
  'Dokumenty, którymi dysponujemy, nie podają kwoty rezerwacji ani harmonogramu płatności. Prosimy o nie i potwierdzamy je na piśmie.',
  'Dokumentene vi har oppgir verken reservasjonsbeløp eller betalingsplan. Vi ber om dem og setter dem skriftlig.',
  'Dokumenten vi har anger varken reservationsbelopp eller betalningsplan. Vi begär dem och sätter dem skriftligen.')

# ---- SEO -----------------------------------------------------------------------------------------------

a('Las Mesas Blue Horizon - New Apartments in Estepona', 'Las Mesas Blue Horizon - Apartamentos nuevos en Estepona',
  'Las Mesas Blue Horizon - Appartements neufs à Estepona', 'Las Mesas Blue Horizon - Neubauwohnungen in Estepona',
  'Las Mesas Blue Horizon - новые квартиры в Эстепоне', 'Las Mesas Blue Horizon - شقق جديدة في إستيبونا',
  'Las Mesas Blue Horizon - Nieuwbouwappartementen in Estepona', 'Las Mesas Blue Horizon - Nowe mieszkania w Esteponie',
  'Las Mesas Blue Horizon - Nye leiligheter i Estepona', 'Las Mesas Blue Horizon - Nya lägenheter i Estepona')
a('Las Mesas Blue Horizon: Two- and Three-Bedroom Apartments in Las Mesas, Estepona',
  'Las Mesas Blue Horizon: apartamentos de dos y tres dormitorios en Las Mesas, Estepona',
  'Las Mesas Blue Horizon : appartements de deux et trois chambres à Las Mesas, Estepona',
  'Las Mesas Blue Horizon: Wohnungen mit zwei und drei Schlafzimmern in Las Mesas, Estepona',
  'Las Mesas Blue Horizon: квартиры с двумя и тремя спальнями в Лас-Месас, Эстепона',
  'Las Mesas Blue Horizon: شقق بغرفتي نوم وثلاث غرف نوم في لاس ميساس، إستيبونا',
  'Las Mesas Blue Horizon: appartementen met twee en drie slaapkamers in Las Mesas, Estepona',
  'Las Mesas Blue Horizon: mieszkania z dwiema i trzema sypialniami w Las Mesas, Estepona',
  'Las Mesas Blue Horizon: leiligheter med to og tre soverom i Las Mesas, Estepona',
  'Las Mesas Blue Horizon: lägenheter med två och tre sovrum i Las Mesas, Estepona')
a('Two- and Three-Bedroom Apartments in Las Mesas, Estepona',
  'Apartamentos de dos y tres dormitorios en Las Mesas, Estepona', 'Appartements de deux et trois chambres à Las Mesas, Estepona',
  'Wohnungen mit zwei und drei Schlafzimmern in Las Mesas, Estepona', 'Квартиры с двумя и тремя спальнями в Лас-Месас, Эстепона',
  'شقق بغرفتي نوم وثلاث غرف نوم في لاس ميساس، إستيبونا', 'Appartementen met twee en drie slaapkamers in Las Mesas, Estepona',
  'Mieszkania z dwiema i trzema sypialniami w Las Mesas, Estepona', 'Leiligheter med to og tre soverom i Las Mesas, Estepona',
  'Lägenheter med två och tre sovrum i Las Mesas, Estepona')

# ---- templates: unit references, sizes, plan alt and captions -------------------------------------------

proj = json.load(open('content/liora-projects/las-mesas-blue-horizon/project.json'))
for u in proj['availability']['units']:
    if u['reference'] not in T:
        same(u['reference'])

# built / terrace, per locale (Norwegian: "bebygd", the settled word)
SIZE = {
 'es': ('{b} {U} construidos', '{t} {U} de terraza'),
 'fr': ('{b} {U} construits', '{t} {U} de terrasse'),
 'de': ('{b} {U} bebaut', '{t} {U} Terrasse'),
 'ru': ('{b} {U} застроенной площади', 'терраса {t} {U}'),
 'ar': ('{b} {U} مبنية', '{t} {U} تراس'),
 'nl': ('{b} {U} bebouwd', '{t} {U} terras'),
 'pl': ('{b} {U} zabudowy', '{t} {U} tarasu'),
 'no': ('{b} {U} bebygd', '{t} {U} terrasse'),
 'sv': ('{b} {U} byggyta', '{t} {U} terrass'),
}
for u in proj['availability']['units']:
    if u['size'] in T:
        continue
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm terrace', u['size'])
    assert m, u['size']
    b, t = m.groups()
    out = []
    for l in LOCS:
        parts = [SIZE[l][0].format(b='{N%s}' % b, U='{U}'), SIZE[l][1].format(t='{N%s}' % t, U='{U}')]
        out.append(('، ' if l == 'ar' else ', ').join(parts))
    a(u['size'], *out)

# plan alt and caption: same wording as the sibling floorplan labels
FL = json.load(open(f'{SP}/floor_parts.json'))
HOME = {'es': 'Vivienda', 'fr': 'Logement', 'de': 'Wohnung', 'ru': 'Квартира', 'ar': 'المسكن', 'nl': 'Woning', 'pl': 'Lokal', 'no': 'Bolig', 'sv': 'Bostad'}
PLAN = {'es': 'Plano de la vivienda', 'fr': 'Plan du logement', 'de': 'Grundriss der Wohnung', 'ru': 'Планировка квартиры', 'ar': 'مخطط المسكن',
        'nl': 'Plattegrond van woning', 'pl': 'Rzut lokalu', 'no': 'Plantegning av bolig', 'sv': 'Planritning för bostad'}
for it in proj['media']['items']:
    if it.get('category') != 'Floorplans':
        continue
    m = re.fullmatch(r'Home ([\d]-\d[A-Z]), (\w+ floor), Block (\d)', it['caption'])
    assert m, it['caption']
    ref, floor, blk = m.groups()
    cap, alt = {}, {}
    for l in LOCS:
        fl = FL['parts'][floor.lower()][l]
        fl = fl if l == 'ar' else fl[0].lower() + fl[1:]
        bl = f"{FL['prefixes']['block'][l]} {blk}"
        sep = '، ' if l == 'ar' else ', '
        cap[l] = f'{HOME[l]} {ref}{sep}{fl}{sep}{bl}'
        alt[l] = f'{PLAN[l]} {ref}{sep}{fl}{sep}{bl}'
    T[it['caption']] = cap
    T[it['alt']] = alt

json.dump(T, open(f'{SP}/tr_m.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
