# -*- coding: utf-8 -*-
"""Monteros Garden Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E590000}
money, {N88.4} decimal number, {U} the area unit.
    python3 tools/import/k_monteros_garden.py <scratch dir>      (writes <dir>/tr_a.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/monteros-garden-residences/project.json'))


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


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


same('Monteros Garden Residences'); same('Monteros Garden'); same('Monteros Garden <em>Residences</em>')

# The Norwegian label for the built area is "Bruksareal" here, not the "Bebygd areal" the translation memory holds:
# "bebygd areal" is the footprint of a building, and the figures are floor areas.
put('Built area', ('Superficie construida', 'Surface construite', 'Bebaute Fläche', 'Площадь застройки', 'المساحة المبنية',
                   'Bebouwde oppervlakte', 'Powierzchnia zabudowy', 'Bruksareal', 'Byggyta'))

# ---- description, SEO, card ------------------------------------------------------------------

a('.description',
  '3 de las 57 viviendas de Monteros Garden Residences, en Marbella, figuran como disponibles: una vivienda de dos dormitorios por {E590000} y viviendas de tres dormitorios por {E685000} y {E720000}, más IVA. Cada una tiene una plaza de garaje. No se indica fecha de entrega.',
  '3 des 57 logements de Monteros Garden Residences, à Marbella, sont indiqués comme disponibles : un logement de deux chambres à {E590000} et des logements de trois chambres à {E685000} et {E720000}, plus TVA. Chacun a une place de garage. Aucune date de livraison n’est indiquée.',
  '3 der 57 Wohnungen in Monteros Garden Residences in Marbella sind als verfügbar aufgeführt: eine Wohnung mit zwei Schlafzimmern für {E590000} und Wohnungen mit drei Schlafzimmern für {E685000} und {E720000}, zuzüglich MwSt. Jede hat einen Garagenstellplatz. Ein Fertigstellungstermin ist nicht angegeben.',
  '3 из 57 квартир в Monteros Garden Residences в Марбелье указаны как доступные: квартира с двумя спальнями за {E590000} и квартиры с тремя спальнями за {E685000} и {E720000}, плюс НДС. У каждой есть место в гараже. Срок сдачи не указан.',
  '3 من أصل 57 مسكنًا في Monteros Garden Residences في ماربيا مدرجة على أنها متاحة: مسكن بغرفتي نوم بسعر {E590000} ومسكنان بثلاث غرف نوم بسعر {E685000} و{E720000}، زائد ضريبة القيمة المضافة. لكل منها موقف سيارات في المرآب. لم يُذكر موعد إنجاز.',
  '3 van de 57 woningen in Monteros Garden Residences, in Marbella, staan als beschikbaar vermeld: een woning met twee slaapkamers voor {E590000} en woningen met drie slaapkamers voor {E685000} en {E720000}, plus btw. Elke woning heeft een garageplaats. Er wordt geen opleveringsdatum genoemd.',
  '3 z 57 mieszkań w Monteros Garden Residences, w Marbelli, jest podanych jako dostępne: mieszkanie z dwiema sypialniami za {E590000} oraz mieszkania z trzema sypialniami za {E685000} i {E720000}, plus VAT. Każde ma miejsce w garażu. Termin oddania nie jest podany.',
  '3 av de 57 boligene i Monteros Garden Residences, i Marbella, er oppført som tilgjengelige: en bolig med to soverom til {E590000} og boliger med tre soverom til {E685000} og {E720000}, pluss mva. Hver bolig har en garasjeplass. Ingen overleveringsdato er oppgitt.',
  '3 av de 57 bostäderna i Monteros Garden Residences, i Marbella, är angivna som tillgängliga: en bostad med två sovrum för {E590000} och bostäder med tre sovrum för {E685000} och {E720000}, plus IVA (spansk moms). Varje bostad har en garageplats. Inget tillträdesdatum anges.')
a('.seoDescription',
  'Apartamentos de dos y tres dormitorios con grandes terrazas en Altos de los Monteros, Marbella, desde {E590000} más IVA, con piscina interior climatizada, gimnasio y espacio de coworking.',
  'Appartements de deux et trois chambres avec grandes terrasses à Altos de los Monteros, Marbella, à partir de {E590000} plus TVA, avec piscine intérieure chauffée, salle de sport et espace de coworking.',
  'Wohnungen mit zwei und drei Schlafzimmern und großen Terrassen in Altos de los Monteros, Marbella, ab {E590000} zuzüglich MwSt., mit beheiztem Innenpool, Fitnessraum und Coworking-Bereich.',
  'Апартаменты с двумя и тремя спальнями и большими террасами в Альтос-де-лос-Монтерос, Марбелья, от {E590000} плюс НДС, с крытым подогреваемым бассейном, тренажёрным залом и коворкингом.',
  'شقق بغرفتي نوم وثلاث غرف نوم مع تراسات واسعة في ألتوس دي لوس مونتيروس، ماربيا، ابتداءً من {E590000} زائد ضريبة القيمة المضافة، مع مسبح داخلي مُدفأ وصالة رياضية ومساحة عمل مشتركة.',
  'Appartementen met twee en drie slaapkamers en grote terrassen in Altos de los Monteros, Marbella, vanaf {E590000} plus btw, met een verwarmd binnenzwembad, een fitnessruimte en een coworkingruimte.',
  'Apartamenty z dwiema i trzema sypialniami oraz dużymi tarasami w Altos de los Monteros, Marbella, od {E590000} plus VAT, z podgrzewanym basenem wewnętrznym, siłownią i przestrzenią coworkingową.',
  'Leiligheter med to og tre soverom og store terrasser i Altos de los Monteros, Marbella, fra {E590000} pluss mva, med oppvarmet innendørsbasseng, treningsrom og coworkingområde.',
  'Lägenheter med två och tre sovrum och stora terrasser i Altos de los Monteros, Marbella, från {E590000} plus IVA (spansk moms), med uppvärmd inomhuspool, gym och coworkingyta.')
a('.twitterDescription',
  'Apartamentos nuevos con grandes terrazas en Marbella, tres viviendas disponibles.',
  'Appartements neufs avec grandes terrasses à Marbella, trois logements disponibles.',
  'Neubauwohnungen mit großen Terrassen in Marbella, drei Wohnungen verfügbar.',
  'Новые апартаменты с большими террасами в Марбелье, доступны три квартиры.',
  'شقق جديدة بتراسات واسعة في ماربيا، ثلاثة مساكن متاحة.',
  'Nieuwbouwappartementen met grote terrassen in Marbella, drie woningen beschikbaar.',
  'Nowe apartamenty z dużymi tarasami w Marbelli, dostępne trzy mieszkania.',
  'Nye leiligheter med store terrasser i Marbella, tre boliger tilgjengelige.',
  'Nya lägenheter med stora terrasser i Marbella, tre bostäder tillgängliga.')
a('.hero.startingPrice',
  'Desde {E590000} + IVA', 'À partir de {E590000} + TVA', 'Ab {E590000} + MwSt.', 'От {E590000} + НДС', 'ابتداءً من {E590000} + ضريبة القيمة المضافة',
  'Vanaf {E590000} + btw', 'Od {E590000} + VAT', 'Fra {E590000} + mva.', 'Från {E590000} + IVA')
a('.card.description',
  'Apartamentos de dos y tres dormitorios con grandes terrazas en una promoción de 57 viviendas en Marbella, con piscina interior climatizada, gimnasio y espacio de coworking.',
  'Appartements de deux et trois chambres avec grandes terrasses dans un programme de 57 logements à Marbella, avec piscine intérieure chauffée, salle de sport et espace de coworking.',
  'Wohnungen mit zwei und drei Schlafzimmern und großen Terrassen in einer Anlage mit 57 Wohnungen in Marbella, mit beheiztem Innenpool, Fitnessraum und Coworking-Bereich.',
  'Апартаменты с двумя и тремя спальнями и большими террасами в комплексе из 57 квартир в Марбелье, с крытым подогреваемым бассейном, тренажёрным залом и коворкингом.',
  'شقق بغرفتي نوم وثلاث غرف نوم مع تراسات واسعة في مجمّع من 57 مسكنًا في ماربيا، مع مسبح داخلي مُدفأ وصالة رياضية ومساحة عمل مشتركة.',
  'Appartementen met twee en drie slaapkamers en grote terrassen in een complex van 57 woningen in Marbella, met een verwarmd binnenzwembad, een fitnessruimte en een coworkingruimte.',
  'Apartamenty z dwiema i trzema sypialniami oraz dużymi tarasami w inwestycji liczącej 57 mieszkań w Marbelli, z podgrzewanym basenem wewnętrznym, siłownią i przestrzenią coworkingową.',
  'Leiligheter med to og tre soverom og store terrasser i et anlegg med 57 boliger i Marbella, med oppvarmet innendørsbasseng, treningsrom og coworkingområde.',
  'Lägenheter med två och tre sovrum och stora terrasser i ett område med 57 bostäder i Marbella, med uppvärmd inomhuspool, gym och coworkingyta.')
a('.card.meta[0][1]',
  '{E590000} + IVA', '{E590000} + TVA', '{E590000} + MwSt.', '{E590000} + НДС', '{E590000} + ضريبة القيمة المضافة',
  '{E590000} + btw', '{E590000} + VAT', '{E590000} + mva.', '{E590000} + IVA')

# ---- image alts and captions ------------------------------------------------------------------

a('.images.hero.alt',
  'Vista generada por ordenador a través de la piscina comunitaria al atardecer hacia bloques blancos y un edificio bajo acristalado, con tumbonas, sombrillas y palmeras',
  'Vue générée par ordinateur à travers la piscine commune au crépuscule vers des bâtiments blancs et un bâtiment bas vitré, avec transats, parasols et palmiers',
  'Computergenerierte Ansicht über den Gemeinschaftspool in der Abenddämmerung auf weiße Gebäude und ein niedriges verglastes Gebäude, mit Sonnenliegen, Sonnenschirmen und Palmen',
  'Компьютерная визуализация: вид через общий бассейн в сумерках на белые корпуса и низкое остеклённое здание; шезлонги, зонты и пальмы',
  'منظر مولَّد بالحاسوب عبر المسبح المشترك عند الغروب نحو مبانٍ بيضاء ومبنى منخفض مزجَّج، مع مقاعد تشمّس ومظلات ونخيل',
  'Computergegenereerd beeld over het gemeenschappelijke zwembad bij schemering naar witte blokken en een laag glazen gebouw, met ligstoelen, parasols en palmen',
  'Wygenerowany komputerowo widok przez wspólny basen o zmierzchu na białe budynki i niski przeszklony budynek, z leżakami, parasolami i palmami',
  'Datagenerert bilde over fellesbassenget i skumringen mot hvite blokker og en lav glassbygning, med solsenger, parasoller og palmer',
  'Datorgenererad vy över den gemensamma poolen i skymningen mot vita hus och en låg glasad byggnad, med solstolar, parasoller och palmer')
a('.images.architecture.alt',
  'Vista generada por ordenador a lo largo de la piscina comunitaria de día, con tumbonas sobre el césped, sombrillas, palmeras y una tarima de madera',
  'Vue générée par ordinateur le long de la piscine commune de jour, avec transats sur la pelouse, parasols, palmiers et un deck en bois',
  'Computergenerierte Ansicht entlang des Gemeinschaftspools bei Tag, mit Sonnenliegen auf dem Rasen, Sonnenschirmen, Palmen und einem Holzdeck',
  'Компьютерная визуализация общего бассейна днём: шезлонги на газоне, зонты, пальмы и деревянный настил',
  'منظر مولَّد بالحاسوب على امتداد المسبح المشترك في النهار، مع مقاعد تشمّس على المرج ومظلات ونخيل وأرضية خشبية',
  'Computergegenereerd beeld langs het gemeenschappelijke zwembad overdag, met ligstoelen op het gazon, parasols, palmen en een houten dek',
  'Wygenerowany komputerowo widok wzdłuż wspólnego basenu w dzień, z leżakami na trawniku, parasolami, palmami i drewnianym pomostem',
  'Datagenerert bilde langs fellesbassenget om dagen, med solsenger på plenen, parasoller, palmer og et tredekk',
  'Datorgenererad vy längs den gemensamma poolen på dagen, med solstolar på gräsmattan, parasoller, palmer och ett trädäck')
a('.images.lifestyle.alt',
  'Piscina interior climatizada generada por ordenador, con tumbonas y una pared acristalada que da a un patio ajardinado',
  'Piscine intérieure chauffée générée par ordinateur, avec transats et un mur vitré donnant sur une cour plantée',
  'Computergenerierter beheizter Innenpool mit Liegen und einer Glaswand zu einem begrünten Innenhof',
  'Компьютерная визуализация крытого подогреваемого бассейна с шезлонгами и стеклянной стеной, выходящей во внутренний дворик с зеленью',
  'مسبح داخلي مُدفأ مولَّد بالحاسوب، مع مقاعد استلقاء وجدار زجاجي يطل على فناء مزروع',
  'Computergegenereerd verwarmd binnenzwembad met ligbedden en een glazen wand naar een beplante binnenplaats',
  'Wygenerowany komputerowo podgrzewany basen wewnętrzny z leżakami i przeszkloną ścianą wychodzącą na zielony dziedziniec',
  'Datagenerert oppvarmet innendørsbasseng med solsenger og en glassvegg mot en beplantet bakgård',
  'Datorgenererad uppvärmd inomhuspool med solbäddar och en glasvägg mot en planterad innergård')
a('.images.privateViewing.alt',
  'Salón y comedor abiertos generados por ordenador, con un sofá rinconero, una mesa de comedor, una isla de cocina y armarios empotrados en la pared del fondo',
  'Séjour et salle à manger ouverts générés par ordinateur, avec un canapé d’angle, une table à manger, un îlot de cuisine et des placards intégrés sur le mur du fond',
  'Computergeneriertes offenes Wohn- und Esszimmer mit Ecksofa, Esstisch, Kücheninsel und Einbauschränken an der Rückwand',
  'Компьютерная визуализация открытой гостиной-столовой с угловым диваном, обеденным столом, кухонным островом и встроенными шкафами вдоль задней стены',
  'غرفة معيشة وطعام مفتوحة مولَّدة بالحاسوب بأريكة زاوية وطاولة طعام وجزيرة مطبخ وخزائن مدمجة على الجدار الخلفي',
  'Computergegenereerde open woon- en eetkamer met een hoekbank, een eettafel, een keukeneiland en inbouwkasten langs de achterwand',
  'Wygenerowany komputerowo otwarty salon z jadalnią, z narożną sofą, stołem jadalnianym, wyspą kuchenną i szafami w zabudowie na tylnej ścianie',
  'Datagenerert åpen stue og spisestue med hjørnesofa, spisebord, kjøkkenøy og innebygde skap langs bakveggen',
  'Datorgenererat öppet vardagsrum och matsal med hörnsoffa, matbord, köksö och inbyggda skåp längs bakväggen')

a('.media.copy',
  'Vistas generadas por ordenador de la piscina, una terraza, un salón y las instalaciones comunes.',
  'Vues générées par ordinateur de la piscine, d’une terrasse, d’un séjour et des équipements communs.',
  'Computergenerierte Ansichten des Pools, einer Terrasse, eines Wohnzimmers und der Gemeinschaftseinrichtungen.',
  'Компьютерные визуализации бассейна, террасы, гостиной и общих зон.',
  'مناظر مولَّدة بالحاسوب للمسبح وتراس وغرفة معيشة والمرافق المشتركة.',
  'Computergegenereerde beelden van het zwembad, een terras, een woonkamer en de gemeenschappelijke voorzieningen.',
  'Wygenerowane komputerowo widoki basenu, tarasu, salonu i części wspólnych.',
  'Datagenererte bilder av bassenget, en terrasse, en stue og fellesfasilitetene.',
  'Datorgenererade vyer av poolen, en terrass, ett vardagsrum och de gemensamma faciliteterna.')
a('.media.note',
  'Todas las imágenes están generadas por ordenador, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos.',
  'Toutes les images sont générées par ordinateur, et le mobilier et la décoration qui y figurent sont illustratifs et non inclus.',
  'Alle Bilder sind computergeneriert, und die darin gezeigten Möbel und die Dekoration sind illustrativ und nicht enthalten.',
  'Все изображения созданы на компьютере, а мебель и отделка на них носят иллюстративный характер и в стоимость не входят.',
  'جميع الصور مولَّدة بالحاسوب، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين.',
  'Alle beelden zijn computergegenereerd, en het meubilair en de inrichting op de beelden zijn illustratief en niet inbegrepen.',
  'Wszystkie wizualizacje są wygenerowane komputerowo, a meble i dekoracje na nich mają charakter poglądowy i nie są wliczone.',
  'Alle bildene er datagenerert, og møblene og dekorasjonen på dem er illustrative og ikke inkludert.',
  'Alla bilder är datorgenererade, och möblerna och inredningen på dem är illustrativa och ingår inte.')
a('.media.items[0].caption',
  'La piscina comunitaria al atardecer', 'La piscine commune au crépuscule', 'Der Gemeinschaftspool in der Abenddämmerung',
  'Общий бассейн в сумерках', 'المسبح المشترك عند الغروب', 'Het gemeenschappelijke zwembad bij schemering',
  'Wspólny basen o zmierzchu', 'Fellesbassenget i skumringen', 'Den gemensamma poolen i skymningen')
a('.media.items[1].caption',
  'La piscina comunitaria de día', 'La piscine commune de jour', 'Der Gemeinschaftspool bei Tag',
  'Общий бассейн днём', 'المسبح المشترك في النهار', 'Het gemeenschappelijke zwembad overdag',
  'Wspólny basen w dzień', 'Fellesbassenget om dagen', 'Den gemensamma poolen på dagen')
a('.media.items[2].alt',
  'Vista generada por ordenador de una terraza cubierta con una mesa de comedor y asientos de estar, con vistas a los árboles y al mar',
  'Vue générée par ordinateur d’une terrasse couverte avec une table à manger et un coin salon, donnant sur les arbres et la mer',
  'Computergenerierte Ansicht einer überdachten Terrasse mit Esstisch und Loungemöbeln, mit Blick über Bäume auf das Meer',
  'Компьютерная визуализация крытой террасы с обеденным столом и лаунж-мебелью; вид поверх деревьев на море',
  'منظر مولَّد بالحاسوب لتراس مغطى بطاولة طعام ومقاعد جلوس، يطل على الأشجار والبحر',
  'Computergegenereerd beeld van een overdekt terras met een eettafel en loungemeubilair, met uitzicht over de bomen op de zee',
  'Wygenerowany komputerowo widok zadaszonego tarasu ze stołem jadalnianym i meblami wypoczynkowymi, z widokiem ponad drzewami na morze',
  'Datagenerert bilde av en overbygd terrasse med spisebord og loungemøbler, med utsikt over trærne mot havet',
  'Datorgenererad vy av en täckt terrass med matbord och loungemöbler, med utsikt över träden mot havet')
a('.media.items[2].caption',
  'Una terraza cubierta con vistas al mar', 'Une terrasse couverte avec vue sur la mer', 'Eine überdachte Terrasse mit Meerblick',
  'Крытая терраса с видом на море', 'تراس مغطى بإطلالة على البحر', 'Een overdekt terras met uitzicht op zee',
  'Zadaszony taras z widokiem na morze', 'En overbygd terrasse med utsikt mot havet', 'En täckt terrass med utsikt över havet')
a('.media.items[3].caption',
  'Salón, comedor y cocina', 'Séjour, salle à manger et cuisine', 'Wohnzimmer, Essbereich und Küche',
  'Гостиная, столовая и кухня', 'غرفة المعيشة ومنطقة الطعام والمطبخ', 'Woonkamer, eetruimte en keuken',
  'Salon, jadalnia i kuchnia', 'Stue, spiseområde og kjøkken', 'Vardagsrum, matplats och kök')
a('.media.items[4].alt',
  'Club social generado por ordenador: una sala luminosa con una mesa de comedor, una zona de estar y grandes ventanales al exterior',
  'Salon du club généré par ordinateur : une pièce lumineuse avec une table à manger, un coin salon et de grandes baies donnant sur l’extérieur',
  'Computergenerierte Club-Lounge: ein heller Raum mit Esstisch, Sitzbereich und großen Fenstern ins Freie',
  'Компьютерная визуализация клубного лаунжа: светлое помещение с обеденным столом, зоной отдыха и большими окнами во двор',
  'صالة النادي الاجتماعي مولَّدة بالحاسوب: قاعة مشرقة بطاولة طعام ومنطقة جلوس ونوافذ كبيرة تطل على الخارج',
  'Computergegenereerde clublounge: een lichte ruimte met een eettafel, een zithoek en grote ramen naar buiten',
  'Wygenerowany komputerowo salon klubowy: jasne wnętrze ze stołem jadalnianym, strefą wypoczynku i dużymi oknami na zewnątrz',
  'Datagenerert klubblounge: et lyst rom med spisebord, sittegruppe og store vinduer mot utsiden',
  'Datorgenererad klubblounge: ett ljust rum med matbord, en sittgrupp och stora fönster mot utsidan')
a('.media.items[5].alt',
  'Gimnasio generado por ordenador con bicicletas estáticas y cintas de correr, un techo de lamas de madera y grandes ventanales a un lado',
  'Salle de sport générée par ordinateur avec vélos d’appartement et tapis de course, un plafond à lames de bois et de grandes baies sur un côté',
  'Computergenerierter Fitnessraum mit Fahrrädern und Laufbändern, einer Holzlamellendecke und großen Fenstern an einer Seite',
  'Компьютерная визуализация тренажёрного зала с велотренажёрами и беговыми дорожками, потолком из деревянных реек и большими окнами вдоль одной стены',
  'صالة رياضية مولَّدة بالحاسوب بدراجات تمرين وأجهزة جري وسقف من الشرائح الخشبية ونوافذ كبيرة على أحد الجانبين',
  'Computergegenereerde fitnessruimte met hometrainers en loopbanden, een plafond van houten latten en grote ramen aan een zijde',
  'Wygenerowana komputerowo siłownia z rowerami treningowymi i bieżniami, sufitem z drewnianych lameli i dużymi oknami po jednej stronie',
  'Datagenerert treningsrom med mosjonssykler og tredemøller, et tak av trelameller og store vinduer langs den ene siden',
  'Datorgenererat gym med motionscyklar och löpband, ett tak av trälameller och stora fönster längs ena sidan')
a('.media.items[6].alt',
  'Espacio de coworking generado por ordenador con escritorios, sillas verdes, una zona de sofás y una pared vegetal',
  'Espace de coworking généré par ordinateur avec bureaux, chaises vertes, coin canapés et mur végétal',
  'Computergenerierter Coworking-Bereich mit Schreibtischen, grünen Stühlen, einer Sofazone und einer begrünten Wand',
  'Компьютерная визуализация коворкинга со столами, зелёными стульями, зоной с диванами и стеной из растений',
  'مساحة عمل مشتركة مولَّدة بالحاسوب بمكاتب وكراسٍ خضراء ومنطقة أرائك وجدار نباتي',
  'Computergegenereerde coworkingruimte met bureaus, groene stoelen, een zitgedeelte met banken en een groene wand',
  'Wygenerowana komputerowo przestrzeń coworkingowa z biurkami, zielonymi krzesłami, strefą z sofami i ścianą z roślin',
  'Datagenerert coworkingområde med skrivebord, grønne stoler, en sofakrok og en grønn vegg',
  'Datorgenererad coworkingyta med skrivbord, gröna stolar, en soffgrupp och en grön vägg')

# ---- overview, why, architecture ------------------------------------------------------------------

a('.overview.copy[0]',
  'Monteros Garden Residences es una promoción privada de 57 viviendas en Marbella. El dossier del promotor describe viviendas de uno, dos y tres dormitorios con grandes terrazas e interiores luminosos, entre ellas viviendas en planta baja y áticos. Todos los áticos tienen jacuzzi, y también algunas de las viviendas en planta baja.',
  'Monteros Garden Residences est un programme privé de 57 logements à Marbella. Le dossier du promoteur décrit des logements d’une, deux et trois chambres avec de grandes terrasses et des intérieurs lumineux, dont des logements en rez-de-chaussée et des penthouses. Chaque penthouse a un jacuzzi, tout comme certains logements en rez-de-chaussée.',
  'Monteros Garden Residences ist eine private Anlage mit 57 Wohnungen in Marbella. Die Unterlagen des Bauträgers beschreiben Wohnungen mit einem, zwei und drei Schlafzimmern mit großen Terrassen und hellen Innenräumen, darunter Erdgeschosswohnungen und Penthouses. Jedes Penthouse hat einen Whirlpool, ebenso einige der Erdgeschosswohnungen.',
  'Monteros Garden Residences — закрытый комплекс из 57 квартир в Марбелье. В буклете застройщика описаны квартиры с одной, двумя и тремя спальнями, с большими террасами и светлыми интерьерами, в том числе квартиры на первом этаже и пентхаусы. В каждом пентхаусе есть джакузи, как и в некоторых квартирах на первом этаже.',
  'Monteros Garden Residences مشروع سكني خاص من 57 مسكنًا في ماربيا. يصف كتيّب المطوّر مساكن بغرفة وغرفتين وثلاث غرف نوم مع تراسات واسعة وداخل مضيء، بينها مساكن في الطابق الأرضي وبنتهاوس. في كل بنتهاوس جاكوزي، وكذلك في بعض مساكن الطابق الأرضي.',
  'Monteros Garden Residences is een particulier complex van 57 woningen in Marbella. De brochure van de ontwikkelaar beschrijft woningen met een, twee en drie slaapkamers met grote terrassen en lichte interieurs, waaronder woningen op de begane grond en penthouses. Elk penthouse heeft een jacuzzi, net als enkele woningen op de begane grond.',
  'Monteros Garden Residences to prywatna inwestycja z 57 mieszkaniami w Marbelli. Broszura dewelopera opisuje mieszkania z jedną, dwiema i trzema sypialniami, z dużymi tarasami i jasnymi wnętrzami, wśród nich mieszkania na parterze i penthouse’y. Każdy penthouse ma jacuzzi, podobnie jak niektóre mieszkania na parterze.',
  'Monteros Garden Residences er et privat anlegg med 57 boliger i Marbella. Utbyggerens brosjyre beskriver boliger med ett, to og tre soverom med store terrasser og lyse interiører, blant dem boliger i første etasje og toppleiligheter. Hver toppleilighet har jacuzzi, og det har også noen av boligene i første etasje.',
  'Monteros Garden Residences är en privat anläggning med 57 bostäder i Marbella. Exploatörens broschyr beskriver bostäder med ett, två och tre sovrum med stora terrasser och ljusa interiörer, bland dem bostäder i bottenvåningen och takvåningar. Varje takvåning har jacuzzi, och det har även några av bostäderna i bottenvåningen.')
a('.overview.copy[1]',
  'La lista de precios del 3 de noviembre de 2026 recoge tres de las 57 viviendas y muestra cada una como disponible: una vivienda de dos dormitorios en la segunda planta por {E590000} y dos viviendas de tres dormitorios en la primera planta por {E685000} y {E720000}, más IVA. Ninguno de los documentos indica fecha de entrega.',
  'La liste de prix du 3 novembre 2026 nomme trois des 57 logements et indique chacun comme disponible : un logement de deux chambres au deuxième étage à {E590000} et deux logements de trois chambres au premier étage à {E685000} et {E720000}, plus TVA. Aucun des documents n’indique de date de livraison.',
  'Die Preisliste vom 3. November 2026 nennt drei der 57 Wohnungen und zeigt jede als verfügbar: eine Wohnung mit zwei Schlafzimmern im zweiten Obergeschoss für {E590000} und zwei Wohnungen mit drei Schlafzimmern im ersten Obergeschoss für {E685000} und {E720000}, zuzüglich MwSt. Keines der Dokumente nennt einen Fertigstellungstermin.',
  'В прайс-листе от 3 ноября 2026 года названы три из 57 квартир, и каждая указана как доступная: квартира с двумя спальнями на третьем этаже за {E590000} и две квартиры с тремя спальнями на втором этаже за {E685000} и {E720000}, плюс НДС. Ни в одном из документов нет срока сдачи.',
  'تذكر قائمة الأسعار المؤرخة 3 نوفمبر 2026 ثلاثة من المساكن الـ57 وتُظهر كلًّا منها متاحًا: مسكنًا بغرفتي نوم في الطابق الثاني بسعر {E590000} ومسكنين بثلاث غرف نوم في الطابق الأول بسعر {E685000} و{E720000}، زائد ضريبة القيمة المضافة. ولا تذكر أيٌّ من الوثائق موعد إنجاز.',
  'De prijslijst van 3 november 2026 noemt drie van de 57 woningen en toont elk als beschikbaar: een woning met twee slaapkamers op de tweede verdieping voor {E590000} en twee woningen met drie slaapkamers op de eerste verdieping voor {E685000} en {E720000}, plus btw. Geen van de documenten noemt een opleveringsdatum.',
  'Cennik z 3 listopada 2026 roku wymienia trzy z 57 mieszkań i pokazuje każde jako dostępne: mieszkanie z dwiema sypialniami na drugim piętrze za {E590000} oraz dwa mieszkania z trzema sypialniami na pierwszym piętrze za {E685000} i {E720000}, plus VAT. Żaden z dokumentów nie podaje terminu oddania.',
  'Prislisten fra 3. november 2026 nevner tre av de 57 boligene og viser hver som tilgjengelig: en bolig med to soverom i tredje etasje til {E590000} og to boliger med tre soverom i andre etasje til {E685000} og {E720000}, pluss mva. Ingen av dokumentene oppgir en overleveringsdato.',
  'Prislistan från 3 november 2026 nämner tre av de 57 bostäderna och visar var och en som tillgänglig: en bostad med två sovrum på andra våningen för {E590000} och två bostäder med tre sovrum på första våningen för {E685000} och {E720000}, plus IVA. Inget av dokumenten anger något tillträdesdatum.')
a('.why.copy',
  'Apartamentos nuevos de dos y tres dormitorios con grandes terrazas y plaza de garaje, en un complejo con piscina interior climatizada, gimnasio y espacio de coworking.',
  'Appartements neufs de deux et trois chambres avec grandes terrasses et place de garage, dans une résidence avec piscine intérieure chauffée, salle de sport et espace de coworking.',
  'Neue Wohnungen mit zwei und drei Schlafzimmern, großen Terrassen und Garagenstellplatz, in einer Anlage mit beheiztem Innenpool, Fitnessraum und Coworking-Bereich.',
  'Новые апартаменты с двумя и тремя спальнями, большими террасами и местом в гараже в комплексе с крытым подогреваемым бассейном, тренажёрным залом и коворкингом.',
  'شقق جديدة بغرفتي نوم وثلاث غرف نوم مع تراسات واسعة وموقف سيارات في المرآب، في مجمّع فيه مسبح داخلي مُدفأ وصالة رياضية ومساحة عمل مشتركة.',
  'Nieuwe appartementen met twee en drie slaapkamers, grote terrassen en een garageplaats, in een complex met een verwarmd binnenzwembad, een fitnessruimte en een coworkingruimte.',
  'Nowe apartamenty z dwiema i trzema sypialniami, dużymi tarasami i miejscem w garażu, w kompleksie z podgrzewanym basenem wewnętrznym, siłownią i przestrzenią coworkingową.',
  'Nye leiligheter med to og tre soverom, store terrasser og garasjeplass, i et anlegg med oppvarmet innendørsbasseng, treningsrom og coworkingområde.',
  'Nya lägenheter med två och tre sovrum, stora terrasser och garageplats, i ett område med uppvärmd inomhuspool, gym och coworkingyta.')
a('.why.points[0][1]',
  'Compradores que buscan un apartamento nuevo de dos o tres dormitorios con una gran terraza en Marbella, con instalaciones comunes que incluyen una piscina interior climatizada, un gimnasio y un espacio de coworking.',
  'Acheteurs qui recherchent un appartement neuf de deux ou trois chambres avec une grande terrasse à Marbella, avec des équipements communs comprenant une piscine intérieure chauffée, une salle de sport et un espace de coworking.',
  'Käufer, die in Marbella eine neue Wohnung mit zwei oder drei Schlafzimmern und großer Terrasse suchen, mit Gemeinschaftseinrichtungen wie beheiztem Innenpool, Fitnessraum und Coworking-Bereich.',
  'Покупателям, которым нужны новые апартаменты с двумя или тремя спальнями и большой террасой в Марбелье, с общими зонами, среди которых крытый подогреваемый бассейн, тренажёрный зал и коворкинг.',
  'للمشترين الذين يريدون شقة جديدة بغرفتي نوم أو ثلاث غرف نوم مع تراس واسع في ماربيا، ومرافق مشتركة تشمل مسبحًا داخليًا مُدفأً وصالة رياضية ومساحة عمل مشتركة.',
  'Kopers die in Marbella een nieuw appartement met twee of drie slaapkamers en een groot terras zoeken, met gemeenschappelijke voorzieningen waaronder een verwarmd binnenzwembad, een fitnessruimte en een coworkingruimte.',
  'Dla kupujących, którzy szukają w Marbelli nowego apartamentu z dwiema lub trzema sypialniami i dużym tarasem, ze wspólnymi udogodnieniami, w tym podgrzewanym basenem wewnętrznym, siłownią i przestrzenią coworkingową.',
  'Kjøpere som vil ha en ny leilighet med to eller tre soverom og en stor terrasse i Marbella, med fellesfasiliteter som oppvarmet innendørsbasseng, treningsrom og coworkingområde.',
  'Köpare som vill ha en ny lägenhet med två eller tre sovrum och en stor terrass i Marbella, med gemensamma faciliteter som uppvärmd inomhuspool, gym och coworkingyta.')
a('.why.points[1][1]',
  'La memoria de calidades da a todas las viviendas suelo radiante, aire acondicionado por conductos y un sistema doméstico controlado desde el móvil, y el promotor ofrece un servicio Custom Manager para mejoras y personalización.',
  'Le descriptif donne à tous les logements un chauffage par le sol, une climatisation gainable et un système domotique piloté depuis un smartphone, et le promoteur propose un service Custom Manager pour les options et la personnalisation.',
  'Die Bau- und Ausstattungsbeschreibung sieht für jede Wohnung Fußbodenheizung, eine Klimaanlage mit Kanalsystem und ein per Smartphone gesteuertes Hauskontrollsystem vor, und der Bauträger bietet einen Custom-Manager-Service für Upgrades und individuelle Anpassungen.',
  'Спецификация предусматривает для каждой квартиры тёплые полы, канальный кондиционер и систему «умный дом» с управлением со смартфона, а застройщик предлагает сервис Custom Manager для улучшений и индивидуальной отделки.',
  'تمنح مواصفات البناء كل مسكن تدفئة أرضية وتكييفًا عبر مجارٍ ونظام منزلي يُدار من الهاتف، ويقدّم المطوّر خدمة Custom Manager للترقيات والتخصيص.',
  'De uitvoeringsomschrijving geeft elke woning vloerverwarming, kanaalairconditioning en een met de smartphone bediend domoticasysteem, en de ontwikkelaar biedt een Custom Manager-service voor upgrades en personalisering.',
  'Specyfikacja przewiduje dla każdego mieszkania ogrzewanie podłogowe, klimatyzację kanałową i system domu sterowany ze smartfona, a deweloper oferuje usługę Custom Manager do ulepszeń i personalizacji.',
  'Byggebeskrivelsen gir hver bolig gulvvarme, kanalbasert klimaanlegg og et smarthussystem styrt fra mobilen, og utbyggeren tilbyr en Custom Manager-tjeneste for oppgraderinger og tilpasning.',
  'Byggbeskrivningen ger varje bostad golvvärme, kanalansluten luftkonditionering och ett smartphonestyrt hemsystem, och exploatören erbjuder en Custom Manager-tjänst för uppgraderingar och anpassning.')
a('.why.points[2][1]',
  'El dossier presenta Marbella como un destino cosmopolita con más de 12 km de playas con bandera azul, calles comerciales y una amplia oferta gastronómica, en un entorno seguro y bien comunicado.',
  'Le dossier présente Marbella comme une station cosmopolite avec plus de 12 km de plages Pavillon bleu, des rues commerçantes et une large offre gastronomique, dans un cadre sûr et bien desservi.',
  'Die Unterlagen stellen Marbella als kosmopolitischen Ferienort mit über 12 km Blaue-Flagge-Stränden, Einkaufsstraßen und einem breiten gastronomischen Angebot dar, in sicherer Umgebung mit guter Verkehrsanbindung.',
  'В буклете Марбелья представлена как космополитичный курорт с более чем 12 км пляжей с «Голубым флагом», торговыми улицами и широким выбором ресторанов, в безопасной обстановке и с хорошим транспортным сообщением.',
  'يقدّم الكتيّب ماربيا منتجعًا عالميًا فيه أكثر من 12 كم من الشواطئ الحاصلة على العلم الأزرق وشوارع للتسوق وتنوّع كبير في المطاعم، في بيئة آمنة وجيدة الربط بالمواصلات.',
  'De brochure presenteert Marbella als een kosmopolitisch oord met meer dan 12 km blauwe-vlagstranden, winkelstraten en een breed gastronomisch aanbod, in een veilige omgeving met goede verbindingen.',
  'Broszura przedstawia Marbellę jako kosmopolityczny kurort z ponad 12 km plaż z Błękitną Flagą, ulicami handlowymi i szeroką ofertą gastronomiczną, w bezpiecznym otoczeniu z dobrą komunikacją.',
  'Brosjyren presenterer Marbella som et kosmopolitisk feriested med over 12 km strender med Blått Flagg, handlegater og et bredt kulinarisk tilbud, i trygge omgivelser med gode forbindelser.',
  'Broschyren presenterar Marbella som en kosmopolitisk semesterort med över 12 km blåflaggade stränder, shoppinggator och ett brett utbud av restauranger, i en trygg miljö med goda förbindelser.')
a('.why.points[3][1]',
  'La lista de precios recoge tres de las 57 viviendas y los documentos no indican fecha de entrega, así que confirmamos ambas cosas antes de cualquier reserva.',
  'La liste de prix couvre trois des 57 logements et les documents n’indiquent aucune date de livraison ; nous confirmons les deux avant toute réservation.',
  'Die Preisliste umfasst drei der 57 Wohnungen, und die Unterlagen nennen keinen Fertigstellungstermin; beides bestätigen wir vor jeder Reservierung.',
  'В прайс-листе три из 57 квартир, а в документах нет срока сдачи, поэтому мы уточняем и то и другое до любого бронирования.',
  'تغطي قائمة الأسعار ثلاثة من المساكن الـ57 ولا تذكر الوثائق موعد إنجاز، لذلك نؤكد الأمرين قبل أي حجز.',
  'De prijslijst omvat drie van de 57 woningen en de documenten noemen geen opleveringsdatum, dus we bevestigen beide vóór elke reservering.',
  'Cennik obejmuje trzy z 57 mieszkań, a dokumenty nie podają terminu oddania, dlatego przed każdą rezerwacją potwierdzamy jedno i drugie.',
  'Prislisten dekker tre av de 57 boligene, og dokumentene oppgir ingen overleveringsdato, så vi bekrefter begge deler før enhver reservasjon.',
  'Prislistan omfattar tre av de 57 bostäderna och dokumenten anger inget tillträdesdatum, så vi bekräftar båda delarna före varje bokning.')
a('.architecture.headlineHtml',
  'Líneas limpias, <em>grandes terrazas</em>', 'Des lignes épurées, <em>de grandes terrasses</em>', 'Klare Linien, <em>große Terrassen</em>',
  'Чистые линии, <em>большие террасы</em>', 'خطوط نقية، <em>وتراسات واسعة</em>', 'Zuivere lijnen, <em>grote terrassen</em>',
  'Czyste linie, <em>duże tarasy</em>', 'Rene linjer, <em>store terrasser</em>', 'Rena linjer, <em>stora terrasser</em>')
a('.architecture.copy[0]',
  'El dossier describe líneas limpias y materiales de primera calidad que crean espacios amplios y armoniosos abiertos al exterior, con grandes terrazas e interiores luminosos.',
  'Le dossier décrit des lignes épurées et des matériaux de première qualité qui créent de vastes espaces harmonieux ouverts sur l’extérieur, avec de grandes terrasses et des intérieurs lumineux.',
  'Die Unterlagen beschreiben klare Linien und hochwertigste Materialien, die große, harmonische, zum Freien hin offene Räume schaffen, mit großen Terrassen und hellen Innenräumen.',
  'В буклете описаны чистые линии и материалы высшего качества, создающие просторные гармоничные пространства, открытые наружу, с большими террасами и светлыми интерьерами.',
  'يصف الكتيّب خطوطًا نقية ومواد من أعلى جودة تصنع فضاءات واسعة متناغمة مفتوحة على الخارج، مع تراسات واسعة وداخل مضيء.',
  'De brochure beschrijft zuivere lijnen en materialen van topkwaliteit die grote, harmonieuze ruimtes scheppen die zich naar buiten openen, met grote terrassen en lichte interieurs.',
  'Broszura opisuje czyste linie i materiały najwyższej jakości, które tworzą duże, harmonijne przestrzenie otwarte na zewnątrz, z dużymi tarasami i jasnymi wnętrzami.',
  'Brosjyren beskriver rene linjer og materialer av toppkvalitet som skaper store, harmoniske rom som åpner seg mot det fri, med store terrasser og lyse interiører.',
  'Broschyren beskriver rena linjer och material av högsta kvalitet som skapar stora, harmoniska rum som öppnar sig mot det fria, med stora terrasser och ljusa interiörer.')
a('.architecture.copy[1]',
  'En las recreaciones, bloques blancos y de color arena con profundas terrazas se disponen en torno a la piscina comunitaria.',
  'Sur les images de synthèse, des bâtiments blancs et sable, aux terrasses profondes, se dressent autour de la piscine commune.',
  'In den Renderings stehen weiße und sandfarbene Gebäude mit tiefen Terrassen rund um den Gemeinschaftspool.',
  'На визуализациях белые и песочного цвета корпуса с глубокими террасами окружают общий бассейн.',
  'في المجسّمات تحيط بالمسبح المشترك مبانٍ بيضاء ورملية اللون ذات تراسات عميقة.',
  'In de renders staan witte en zandkleurige blokken met diepe terrassen rond het gemeenschappelijke zwembad.',
  'Na wizualizacjach białe i piaskowe budynki z głębokimi tarasami otaczają wspólny basen.',
  'På illustrasjonene står hvite og sandfargede blokker med dype terrasser rundt fellesbassenget.',
  'På illustrationerna står vita och sandfärgade hus med djupa terrasser runt den gemensamma poolen.')
a('.architecture.highlights[0][1]',
  'Cimentación de hormigón armado según el estudio geotécnico del terreno y forjados de hormigón armado.',
  'Fondations en béton armé conformes à l’étude géotechnique du terrain et dalles en béton armé.',
  'Stahlbetonfundamente gemäß dem geotechnischen Gutachten des Grundstücks und Stahlbetondecken.',
  'Железобетонный фундамент в соответствии с геотехническим исследованием участка и железобетонные перекрытия.',
  'أساسات من الخرسانة المسلحة وفق الدراسة الجيوتقنية للموقع وبلاطات من الخرسانة المسلحة.',
  'Fundering van gewapend beton volgens het geotechnisch onderzoek van het terrein en vloeren van gewapend beton.',
  'Fundamenty żelbetowe zgodne z badaniem geotechnicznym terenu oraz stropy żelbetowe.',
  'Fundamenter i armert betong i samsvar med den geotekniske undersøkelsen av tomten, og dekker i armert betong.',
  'Grundläggning i armerad betong enligt tomtens geotekniska undersökning och bjälklag i armerad betong.')
a('.architecture.highlights[1][1]',
  'Revoco y pintura combinados con revestimiento, con aislamiento térmico de alto rendimiento, cámara de aire y trasdosado de yeso laminado por el interior.',
  'Enduit et peinture associés à un bardage, avec une isolation thermique haute performance, une lame d’air et un doublage en plaques de plâtre à l’intérieur.',
  'Putz und Anstrich in Verbindung mit einer Verkleidung, mit hochwertiger Wärmedämmung, einer Luftschicht und einer Gipskartonverkleidung auf der Innenseite.',
  'Штукатурка и окраска в сочетании с облицовкой, высокоэффективная теплоизоляция, воздушная прослойка и внутренняя обшивка гипсокартоном.',
  'طلاء ودهان مع كسوة، وعزل حراري عالي الأداء وحيّز هوائي وبطانة داخلية من ألواح الجبس.',
  'Stucwerk en verf gecombineerd met bekleding, met hoogwaardige thermische isolatie, een luchtspouw en een gipsplaatafwerking aan de binnenzijde.',
  'Tynk i farba połączone z okładziną, wysokowydajna izolacja termiczna, szczelina powietrzna i obudowa z płyt gipsowo-kartonowych od wewnątrz.',
  'Puss og maling kombinert med kledning, med høytytende varmeisolasjon, et luftrom og en gipsplatekledning på innsiden.',
  'Puts och målning i kombination med fasadbeklädnad, med högpresterande värmeisolering, en luftspalt och gipsskivor på insidan.')
a('.architecture.highlights[2][1]',
  'Ventanas de PVC o de aluminio con rotura de puente térmico, según decida la dirección facultativa, con vidrio termoacústico de baja emisividad y persianas motorizadas aislantes en los dormitorios.',
  'Fenêtres en PVC ou en aluminium à rupture de pont thermique, selon la décision de la maîtrise d’œuvre, avec vitrage thermo-acoustique à faible émissivité et volets roulants motorisés isolants dans les chambres.',
  'Fenster aus PVC oder Aluminium mit thermischer Trennung, je nach Entscheidung der Bauleitung, mit schall- und wärmedämmendem Low-E-Glas und motorisierten, gedämmten Rollläden in den Schlafzimmern.',
  'Окна из ПВХ или алюминия с терморазрывом, по решению руководства проекта, с низкоэмиссионным тепло- и звукоизолирующим остеклением и моторизованными утеплёнными рольставнями в спальнях.',
  'نوافذ من PVC أو الألمنيوم بفاصل حراري بحسب قرار إدارة المشروع، بزجاج حراري صوتي منخفض الانبعاث وستائر ألمنيوم معزولة بمحرّك في غرف النوم.',
  'Kozijnen van pvc of aluminium met thermische onderbreking, naar beslissing van de projectleiding, met thermisch-akoestisch glas met lage emissie en gemotoriseerde geïsoleerde rolluiken in de slaapkamers.',
  'Okna z PCV lub aluminium z przerwą termiczną, według decyzji kierownictwa projektu, z niskoemisyjnym szkleniem termoakustycznym i zmotoryzowanymi, izolowanymi roletami w sypialniach.',
  'Vinduer i PVC eller aluminium med termisk brudd, etter prosjektledelsens avgjørelse, med lavemisjons varme- og lydisolerende glass og motoriserte, isolerte rullegardiner på soverommene.',
  'Fönster i PVC eller aluminium med termisk brytning, enligt projektledningens beslut, med lågemissions värme- och ljudisolerande glas och motoriserade, isolerade rullgardiner i sovrummen.')
a('.architecture.highlights[3][1]',
  'Gres porcelánico antideslizante de gran formato en el exterior y un jacuzzi con ducha en la planta de los áticos.',
  'Carrelage en grès cérame antidérapant grand format en extérieur et un jacuzzi avec douche à l’étage des penthouses.',
  'Großformatige rutschfeste Feinsteinzeugfliesen im Freien und ein Whirlpool mit Dusche auf der Penthouse-Ebene.',
  'Крупноформатная нескользящая керамогранитная плитка на улице и джакузи с душем на уровне пентхаусов.',
  'بلاط بورسلان كبير المقاس مانع للانزلاق في الخارج، وجاكوزي مع دش في طابق البنتهاوس.',
  'Antislip porseleintegels in groot formaat buiten en een jacuzzi met douche op de penthouseverdieping.',
  'Wielkoformatowe antypoślizgowe płytki gresowe na zewnątrz oraz jacuzzi z prysznicem na poziomie penthouse’ów.',
  'Store sklisikre porselensfliser utendørs og en jacuzzi med dusj i toppleilighetsetasjen.',
  'Stora halkfria porslinsplattor utomhus och en jacuzzi med dusch på takvåningsplanet.')

# ---- quality specification ------------------------------------------------------------------

a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor, fechada el 20 de septiembre de 2023. Indica que la dirección facultativa puede modificarla y sustituirla por otras de calidad similar, y que la piedra natural varía en tono y color.',
  'Source : le descriptif du promoteur, daté du 20 septembre 2023. Il précise que la maîtrise d’œuvre peut le modifier et le remplacer par d’autres prestations de qualité similaire, et que la pierre naturelle varie en ton et en couleur.',
  'Quelle: die Bau- und Ausstattungsbeschreibung des Bauträgers vom 20. September 2023. Sie besagt, dass die Bauleitung sie ändern und durch gleichwertige Ausstattung ersetzen kann und dass Naturstein in Farbton und Farbe variiert.',
  'Источник: спецификация застройщика от 20 сентября 2023 года. В ней сказано, что руководство проекта может изменить её и заменить другими материалами аналогичного качества и что натуральный камень различается по тону и цвету.',
  'المصدر: مواصفات البناء لدى المطوّر المؤرخة 20 سبتمبر 2023. تذكر أن لإدارة المشروع تعديلها واستبدالها بمواصفات مماثلة الجودة، وأن الحجر الطبيعي يتفاوت في درجته ولونه.',
  'Bron: de uitvoeringsomschrijving van de ontwikkelaar, gedateerd 20 september 2023. Daarin staat dat de projectleiding haar kan wijzigen en vervangen door gelijkwaardige afwerking, en dat natuursteen in tint en kleur varieert.',
  'Źródło: specyfikacja wykończenia dewelopera z 20 września 2023 roku. Zastrzega ona, że kierownictwo projektu może ją zmienić i zastąpić rozwiązaniami o podobnej jakości oraz że kamień naturalny różni się odcieniem i barwą.',
  'Kilde: utbyggerens byggebeskrivelse datert 20. september 2023. Den sier at prosjektledelsen kan endre den og erstatte den med likeverdige løsninger, og at naturstein varierer i tone og farge.',
  'Källa: exploatörens byggbeskrivning daterad 20 september 2023. Den anger att projektledningen kan ändra den och ersätta den med likvärdiga lösningar, och att natursten varierar i ton och färg.')
a('.qualitySpecs.groups[0].items[0]',
  'Gres porcelánico de gran formato en salones, dormitorios, cocina, vestíbulo y baños, y porcelánico antideslizante en las terrazas.',
  'Grès cérame grand format dans les pièces de vie, les chambres, la cuisine, l’entrée et les salles de bain, et grès antidérapant sur les terrasses.',
  'Großformatiges Feinsteinzeug in Wohnbereichen, Schlafzimmern, Küche, Flur und Bädern sowie rutschfestes Feinsteinzeug auf den Terrassen.',
  'Крупноформатный керамогранит в гостиной, спальнях, кухне, прихожей и ванных комнатах и нескользящий керамогранит на террасах.',
  'بورسلان كبير المقاس في غرف المعيشة وغرف النوم والمطبخ والمدخل والحمامات، وبورسلان مانع للانزلاق على التراسات.',
  'Porseleintegels in groot formaat in de woonruimtes, slaapkamers, keuken, hal en badkamers, en antislipporselein op de terrassen.',
  'Wielkoformatowy gres w pokojach dziennych, sypialniach, kuchni, przedpokoju i łazienkach oraz antypoślizgowy gres na tarasach.',
  'Store porselensfliser i oppholdsrom, soverom, kjøkken, entré og bad, og sklisikre porselensfliser på terrassene.',
  'Stora porslinsplattor i vardagsrum, sovrum, kök, hall och badrum, och halkfritt porslin på terrasserna.')
a('.qualitySpecs.groups[0].items[1]',
  'Duchas revestidas con cerámica de primeras marcas y pintura plástica lisa en el resto de paredes y en los techos.',
  'Douches revêtues de céramique de grandes marques et peinture plastique lisse sur les autres murs et sur les plafonds.',
  'Duschbereiche mit Keramik führender Marken verfliest, glatte Kunststoffdispersionsfarbe an den übrigen Wänden und an den Decken.',
  'Душевые зоны отделаны керамикой ведущих брендов, остальные стены и потолки окрашены гладкой краской.',
  'مناطق الاستحمام مكسوة بالسيراميك من علامات رائدة، ودهان بلاستيكي أملس على بقية الجدران وعلى الأسقف.',
  'Douchegedeelten betegeld met keramiek van topmerken, en gladde kunststofverf op de overige wanden en op de plafonds.',
  'Strefy prysznicowe wyłożone ceramiką czołowych marek, a pozostałe ściany i sufity pomalowane gładką farbą.',
  'Dusjområder flislagt med keramikk fra ledende merker, og glatt plastmaling på de øvrige veggene og i takene.',
  'Duschytor klädda med keramik från ledande märken, och slät plastfärg på övriga väggar och i taken.')
a('.qualitySpecs.groups[1].items[0]',
  'Puerta de entrada blindada con cerradura de seguridad, puertas interiores macizas lacadas en blanco y armarios modulares forrados por dentro, con balda y barra de colgar.',
  'Porte d’entrée blindée avec serrure de sécurité, portes intérieures pleines laquées blanc et placards modulaires garnis à l’intérieur, avec une étagère et une tringle.',
  'Einbruchhemmende Wohnungseingangstür mit Sicherheitsschloss, massive weiß lackierte Innentüren und modulare Schränke, innen ausgekleidet, mit Einlegeboden und Kleiderstange.',
  'Бронированная входная дверь с замком безопасности, массивные межкомнатные двери, окрашенные в белый, и модульные шкафы с внутренней отделкой, полкой и штангой для одежды.',
  'باب دخول مصفّح بقفل أمان، وأبواب داخلية خشبية مصمتة مطلية باللون الأبيض، وخزائن ملابس معيارية مبطّنة من الداخل بها رف وقضيب تعليق.',
  'Gepantserde voordeur met veiligheidsslot, massieve wit gelakte binnendeuren en modulaire kasten, aan de binnenzijde bekleed, met een plank en een kledingstang.',
  'Drzwi wejściowe antywłamaniowe z zamkiem bezpieczeństwa, pełne drzwi wewnętrzne lakierowane na biało oraz modułowe szafy wyłożone w środku, z półką i drążkiem na ubrania.',
  'Pansret inngangsdør med sikkerhetslås, massive hvitlakkerte innerdører og modulgarderober kledd på innsiden, med hylle og klesstang.',
  'Pansardörr med säkerhetslås, massiva vitlackerade innerdörrar och modulgarderober klädda invändigt, med hylla och klädstång.')
a('.qualitySpecs.groups[2].items[0]',
  'Muebles altos y bajos de laminado de alta presión con cajones de cierre amortiguado y encimera de cuarzo tipo Silestone o Neolith.',
  'Meubles hauts et bas en stratifié haute pression avec tiroirs à fermeture amortie et plan de travail en quartz de type Silestone ou Neolith.',
  'Hoch- und Unterschränke aus Hochdrucklaminat mit selbstschließenden Schubladen und einer Quarzarbeitsplatte vom Typ Silestone oder Neolith.',
  'Верхние и нижние шкафы из ламината высокого давления с ящиками с доводчиками и столешница из кварца типа Silestone или Neolith.',
  'خزائن علوية وسفلية من اللامينات عالي الضغط بأدراج ذاتية الإغلاق وسطح عمل من الكوارتز من نوع Silestone أو Neolith.',
  'Hoge en lage kasten van hogedruklaminaat met zelfsluitende laden en een kwarts werkblad van het type Silestone of Neolith.',
  'Szafki górne i dolne z laminatu wysokociśnieniowego z szufladami z samodomykaniem oraz blat z kwarcu typu Silestone lub Neolith.',
  'Over- og underskap i høytrykkslaminat med selvlukkende skuffer og en kvartsbenkeplate av typen Silestone eller Neolith.',
  'Över- och underskåp i högtryckslaminat med mjukstängande lådor och en bänkskiva i kvarts av typen Silestone eller Neolith.')
a('.qualitySpecs.groups[2].items[1]',
  'Placa de inducción, lavavajillas integrado, horno, microondas, frigorífico, campana extractora, lavadora y secadora, y en los áticos una vinoteca y una cafetera.',
  'Plaque à induction, lave-vaisselle intégré, four, micro-ondes, réfrigérateur, hotte aspirante, lave-linge et sèche-linge, et dans les penthouses une cave à vin et une machine à café.',
  'Induktionskochfeld, integrierter Geschirrspüler, Backofen, Mikrowelle, Kühlschrank, Dunstabzugshaube, Waschmaschine und Trockner, und in den Penthouses ein Weinklimaschrank und eine Kaffeemaschine.',
  'Индукционная варочная панель, встроенная посудомоечная машина, духовой шкаф, микроволновая печь, холодильник, вытяжка, стиральная и сушильная машины, а в пентхаусах — винный шкаф и кофемашина.',
  'موقد حثّي وغسالة صحون مدمجة وفرن وميكروويف وثلاجة ومدخنة شفط وغسالة ومجفف ملابس، وفي البنتهاوس خزانة نبيذ وآلة قهوة.',
  'Inductiekookplaat, ingebouwde vaatwasser, oven, magnetron, koelkast, afzuigkap, wasmachine en droger, en in de penthouses een wijnklimaatkast en een koffiemachine.',
  'Płyta indukcyjna, zintegrowana zmywarka, piekarnik, mikrofalówka, lodówka, okap, pralka i suszarka, a w penthouse’ach także winiarka i ekspres do kawy.',
  'Induksjonstopp, integrert oppvaskmaskin, ovn, mikrobølgeovn, kjøleskap, ventilator, vaskemaskin og tørketrommel, og i toppleilighetene et vinskap og en kaffemaskin.',
  'Induktionshäll, integrerad diskmaskin, ugn, mikrovågsugn, kylskåp, köksfläkt, tvättmaskin och torktumlare, och i takvåningarna ett vinskåp och en kaffemaskin.')
a('.qualitySpecs.groups[3].items[0]',
  'Sanitarios de porcelana vitrificada blanca, platos de ducha de resina con mamparas de vidrio de seguridad, lavabo doble en el baño principal y grifería monomando de primera marca con grifos termostáticos en la ducha.',
  'Sanitaires en porcelaine vitrifiée blanche, receveurs de douche en résine avec parois en verre de sécurité, double vasque dans la salle de bain principale et mitigeurs de grandes marques avec robinets thermostatiques à la douche.',
  'Sanitärkeramik aus weißem Vitreous China, Duschwannen aus Kunstharz mit Sicherheitsglas-Duschwänden, ein Doppelwaschtisch im Hauptbad und Einhebelmischer führender Marken mit Thermostatarmaturen in der Dusche.',
  'Сантехника из белого глазурованного фарфора, душевые поддоны из смолы со стеклянными ограждениями из безопасного стекла, двойная раковина в главной ванной и смесители ведущих брендов с термостатами в душе.',
  'أدوات صحية من البورسلان الزجاجي الأبيض، وصواني استحمام من الراتنج مع حواجز من الزجاج الآمن، وحوض مزدوج في الحمام الرئيسي، وخلاطات من علامات رائدة مع خلاطات حرارية في الدش.',
  'Sanitair van wit verglaasd porselein, douchebakken van hars met veiligheidsglazen douchewanden, een dubbele wastafel in de hoofdbadkamer en mengkranen van topmerken met thermostatische douchekranen.',
  'Ceramika sanitarna z białej porcelany witryfikowanej, brodziki z żywicy z szybami prysznicowymi z szkła bezpiecznego, podwójna umywalka w łazience głównej oraz baterie czołowych marek z termostatami przy prysznicu.',
  'Sanitærutstyr i hvitt vitrifisert porselen, dusjkar i harpiks med dusjvegger i sikkerhetsglass, en dobbel servant på hovedbadet og blandebatterier fra ledende merker med termostatkraner i dusjen.',
  'Sanitetsporslin i vitt vitrifierat porslin, duschkar i harts med duschväggar i säkerhetsglas, ett dubbelt handfat i huvudbadrummet och blandare från ledande märken med termostatblandare i duschen.')
a('.qualitySpecs.groups[4].items[0]',
  'Aire acondicionado por conductos con bomba de calor y control por zonas, un termostato en el salón y otro en cada dormitorio, y control remoto desde el móvil.',
  'Climatisation gainable à pompe à chaleur avec régulation par zones, un thermostat dans le séjour et un dans chaque chambre, et commande à distance depuis un smartphone.',
  'Wärmepumpen-Klimaanlage mit Kanalsystem und Zonensteuerung, ein Thermostat im Wohnzimmer und je eines in den Schlafzimmern sowie Fernsteuerung per Smartphone.',
  'Канальный кондиционер с тепловым насосом и зональным управлением, термостат в гостиной и в каждой спальне и дистанционное управление со смартфона.',
  'تكييف عبر مجارٍ بمضخة حرارية مع تحكم بالمناطق، وثرموستات في غرفة المعيشة وآخر في كل غرفة نوم، وتحكم عن بُعد من الهاتف.',
  'Kanaalairconditioning met warmtepomp en zoneregeling, een thermostaat in de woonkamer en een in elke slaapkamer, en bediening op afstand met de smartphone.',
  'Klimatyzacja kanałowa z pompą ciepła i sterowaniem strefowym, termostat w salonie i w każdej sypialni oraz zdalne sterowanie ze smartfona.',
  'Kanalbasert klimaanlegg med varmepumpe og soneregulering, en termostat i stuen og en i hvert soverom, og fjernstyring fra mobilen.',
  'Kanalansluten luftkonditionering med värmepump och zonstyrning, en termostat i vardagsrummet och en i varje sovrum, och fjärrstyrning från mobilen.')
a('.qualitySpecs.groups[4].items[1]',
  'Suelo radiante en toda la vivienda, alimentado por la unidad aerotérmica central, y agua caliente con un sistema aerotérmico de alta calidad.',
  'Chauffage par le sol dans tout le logement, alimenté par l’unité aérothermique centrale, et eau chaude produite par un système aérothermique de haute qualité.',
  'Fußbodenheizung in der gesamten Wohnung, versorgt von der zentralen Luft-Wärmepumpe, und Warmwasser aus einem hochwertigen Aerothermie-System.',
  'Тёплые полы во всей квартире от центрального аэротермального агрегата и горячая вода от высококачественной аэротермальной системы.',
  'تدفئة أرضية في كامل المسكن تغذّيها الوحدة الهوائية الحرارية المركزية، وماء ساخن من نظام هوائي حراري عالي الجودة.',
  'Vloerverwarming in de hele woning, gevoed door de centrale aerothermische unit, en warm water uit een hoogwaardig aerothermisch systeem.',
  'Ogrzewanie podłogowe w całym mieszkaniu, zasilane z centralnej jednostki aerotermalnej, oraz ciepła woda z wysokiej jakości systemu aerotermalnego.',
  'Gulvvarme i hele boligen, forsynt fra det sentrale aerotermiske anlegget, og varmtvann fra et aerotermisk system av høy kvalitet.',
  'Golvvärme i hela bostaden, försörjd från den centrala aerotermiska enheten, och varmvatten från ett aerotermiskt system av hög kvalitet.')
a('.qualitySpecs.groups[5].name',
  'Tecnología y seguridad', 'Technologie et sécurité', 'Technik und Sicherheit', 'Технологии и безопасность', 'التقنية والأمن',
  'Technologie en veiligheid', 'Technologia i bezpieczeństwo', 'Teknologi og sikkerhet', 'Teknik och säkerhet')
a('.qualitySpecs.groups[5].items[0]',
  'Un sistema controlado desde el móvil para el aire acondicionado y la iluminación, videoportero en color, internet por fibra óptica, tomas ethernet en todas las estancias salvo los baños y preinstalación para la recarga de vehículos eléctricos.',
  'Un système piloté depuis un smartphone pour la climatisation et l’éclairage, un visiophone couleur, internet par fibre optique, des prises ethernet dans toutes les pièces sauf les salles de bain et une pré-installation pour la recharge des véhicules électriques.',
  'Ein per Smartphone gesteuertes System für Klimaanlage und Beleuchtung, eine Farb-Videosprechanlage, Glasfaser-Internet, Ethernet-Anschlüsse in allen Räumen außer den Bädern und eine Vorrüstung für das Laden von Elektrofahrzeugen.',
  'Система с управлением со смартфона для кондиционирования и освещения, цветной видеодомофон, оптоволоконный интернет, розетки Ethernet во всех комнатах, кроме ванных, и предусмотренная подводка для зарядки электромобилей.',
  'نظام يُدار من الهاتف للتكييف والإضاءة، وجرس فيديو ملوّن، وإنترنت عبر الألياف الضوئية، ومقابس إيثرنت في جميع الغرف عدا الحمامات، وتجهيز مسبق لشحن السيارات الكهربائية.',
  'Een met de smartphone bediend systeem voor airconditioning en verlichting, een kleurenvideofoon, glasvezelinternet, ethernetaansluitingen in alle ruimtes behalve de badkamers en een voorbereiding voor het laden van elektrische voertuigen.',
  'System sterowany ze smartfona do klimatyzacji i oświetlenia, kolorowy wideodomofon, internet światłowodowy, gniazda Ethernet we wszystkich pomieszczeniach poza łazienkami oraz instalacja przygotowana do ładowania pojazdów elektrycznych.',
  'Et mobilstyrt system for klimaanlegget og belysningen, fargevideointercom, fiberinternett, ethernetuttak i alle rom unntatt badene og forberedelse for lading av elbiler.',
  'Ett smartphonestyrt system för luftkonditionering och belysning, färgvideodörrtelefon, fiberinternet, ethernetuttag i alla rum utom badrummen och förberedelse för laddning av elfordon.')
a('.qualitySpecs.groups[5].items[1]',
  'Un complejo cerrado con acceso privado, conserje exterior, control de accesos y videovigilancia las 24 horas con cámaras perimetrales, y una puerta de garaje motorizada con apertura a distancia.',
  'Une résidence fermée avec accès privé, concierge extérieur, contrôle d’accès et vidéosurveillance 24 h/24 avec caméras périmétriques, et une porte de garage motorisée à ouverture à distance.',
  'Eine geschlossene Anlage mit privater Zufahrt, Concierge im Außenbereich, Zugangskontrolle und 24-Stunden-Videoüberwachung mit Kameras am Grundstücksrand sowie einem motorisierten Garagentor mit Fernbedienung.',
  'Закрытый комплекс с частным въездом, внешним консьержем, контролем доступа и круглосуточным видеонаблюдением с камерами по периметру, а также моторизованные гаражные ворота с дистанционным открыванием.',
  'مجمّع مغلق بمدخل خاص وكونسيرج خارجي وتحكم بالدخول ومراقبة بالفيديو على مدار الساعة بكاميرات محيطية، وباب مرآب بمحرّك يُفتح عن بُعد.',
  'Een besloten complex met eigen toegang, een conciërge buiten, toegangscontrole en 24 uur per dag videobewaking met camera’s langs de omtrek, en een gemotoriseerde garagedeur met afstandsbediening.',
  'Zamknięty kompleks z prywatnym wjazdem, konsjerżem na zewnątrz, kontrolą dostępu i całodobowym monitoringiem wideo z kamerami po obwodzie oraz zmotoryzowana brama garażowa otwierana zdalnie.',
  'Et bevoktet anlegg med privat adkomst, concierge utendørs, adgangskontroll og døgnåpen videoovervåking med kameraer langs tomtegrensen, og en motorisert garasjeport med fjernåpning.',
  'Ett bevakat område med privat tillfart, concierge utomhus, passerkontroll och dygnet-runt-videoövervakning med kameror runt tomten, och en motoriserad garageport med fjärröppning.')
a('.qualitySpecs.groups[6].items[0]',
  'Piscinas con cloración salina, una piscina interior climatizada, una sala social equipada, una sala de coworking y un gimnasio bien equipado.',
  'Piscines à l’électrolyse au sel, une piscine intérieure chauffée, un salon commun équipé, un espace de coworking et une salle de sport bien équipée.',
  'Pools mit Salzelektrolyse, ein beheizter Innenpool, ein ausgestatteter Gemeinschaftsraum, ein Coworking-Raum und ein gut ausgestatteter Fitnessraum.',
  'Бассейны с солевым хлорированием, крытый подогреваемый бассейн, оборудованный общий зал, коворкинг и хорошо оснащённый тренажёрный зал.',
  'مسابح بمعالجة بالكلور الملحي، ومسبح داخلي مُدفأ، وقاعة اجتماعية مجهزة، وغرفة عمل مشتركة، وصالة رياضية جيدة التجهيز.',
  'Zwembaden met zoutelektrolyse, een verwarmd binnenzwembad, een ingerichte gemeenschappelijke ruimte, een coworkingruimte en een goed uitgeruste fitnessruimte.',
  'Baseny z chlorowaniem solnym, podgrzewany basen wewnętrzny, wyposażona sala wspólna, pokój coworkingowy i dobrze wyposażona siłownia.',
  'Basseng med saltklorering, et oppvarmet innendørsbasseng, et utstyrt felles oppholdsrom, et coworkingrom og et godt utstyrt treningsrom.',
  'Pooler med saltklorering, en uppvärmd inomhuspool, ett utrustat gemensamt rum, ett coworkingrum och ett välutrustat gym.')
a('.qualitySpecs.groups[6].items[1]',
  'Jardines con iluminación y riego automático.', 'Jardins avec éclairage et arrosage automatique.', 'Gärten mit Beleuchtung und automatischer Bewässerung.',
  'Сады с освещением и автоматическим поливом.', 'حدائق بإضاءة وري آلي.', 'Tuinen met verlichting en automatische bewatering.',
  'Ogrody z oświetleniem i automatycznym nawadnianiem.', 'Hager med belysning og automatisk vanning.', 'Trädgårdar med belysning och automatisk bevattning.')

# ---- residences, lifestyle, location ------------------------------------------------------------------

a('.residences.headlineHtml',
  'Tres viviendas, <em>dos tipos de planta</em>', 'Trois logements, <em>deux types de plan</em>', 'Drei Wohnungen, <em>zwei Grundrisstypen</em>',
  'Три квартиры, <em>два типа планировки</em>', 'ثلاثة مساكن، <em>ونوعان من المخططات</em>', 'Drie woningen, <em>twee soorten plattegrond</em>',
  'Trzy mieszkania, <em>dwa rodzaje rzutu</em>', 'Tre boliger, <em>to typer plantegning</em>', 'Tre bostäder, <em>två typer av planlösning</em>')
a('.residences.copy',
  'Las tres viviendas de la lista de precios: dos viviendas de tres dormitorios en la primera planta y una vivienda de dos dormitorios en la segunda, cada una con una plaza de garaje.',
  'Les trois logements de la liste de prix : deux logements de trois chambres au premier étage et un logement de deux chambres au deuxième, chacun avec une place de garage.',
  'Die drei Wohnungen der Preisliste: zwei Wohnungen mit drei Schlafzimmern im ersten Obergeschoss und eine Wohnung mit zwei Schlafzimmern im zweiten, jeweils mit einem Garagenstellplatz.',
  'Три квартиры из прайс-листа: две квартиры с тремя спальнями на втором этаже и одна с двумя спальнями на третьем, у каждой есть место в гараже.',
  'المساكن الثلاثة في قائمة الأسعار: مسكنان بثلاث غرف نوم في الطابق الأول ومسكن بغرفتي نوم في الطابق الثاني، ولكل منها موقف سيارات في المرآب.',
  'De drie woningen op de prijslijst: twee woningen met drie slaapkamers op de eerste verdieping en een woning met twee slaapkamers op de tweede, elk met een garageplaats.',
  'Trzy mieszkania z cennika: dwa mieszkania z trzema sypialniami na pierwszym piętrze i jedno z dwiema sypialniami na drugim, każde z miejscem w garażu.',
  'De tre boligene på prislisten: to boliger med tre soverom i andre etasje og en bolig med to soverom i tredje, hver med en garasjeplass.',
  'De tre bostäderna på prislistan: två bostäder med tre sovrum på första våningen och en bostad med två sovrum på andra, var och en med en garageplats.')
a('.residences.items[0].name',
  'Tres dormitorios en la primera planta', 'Trois chambres au premier étage', 'Drei Schlafzimmer im ersten Obergeschoss',
  'Три спальни на втором этаже', 'ثلاث غرف نوم في الطابق الأول', 'Drie slaapkamers op de eerste verdieping',
  'Trzy sypialnie na pierwszym piętrze', 'Tre soverom i andre etasje', 'Tre sovrum på första våningen')
a('.residences.items[0].points[0]',
  'Viviendas 11B en el portal 1, orientada al oeste, y 61B en el portal 6, orientada al este: tres dormitorios y dos baños, {N120.34} y {N120.35} {U} construidos y {N102.61} {U} de superficie útil interior.',
  'Logements 11B dans la cage 1, orienté à l’ouest, et 61B dans la cage 6, orienté à l’est : trois chambres et deux salles de bain, {N120.34} et {N120.35} {U} construits et {N102.61} {U} de surface utile intérieure.',
  'Wohnung 11B im Aufgang 1, nach Westen ausgerichtet, und 61B im Aufgang 6, nach Osten ausgerichtet: drei Schlafzimmer und zwei Bäder, {N120.34} und {N120.35} {U} bebaut sowie {N102.61} {U} nutzbare Innenfläche.',
  'Квартиры 11B в подъезде 1, окна на запад, и 61B в подъезде 6, окна на восток: три спальни и два санузла, {N120.34} и {N120.35} {U} застройки и {N102.61} {U} полезной внутренней площади.',
  'المسكنان 11B في المدخل 1 ويتجه غربًا، و61B في المدخل 6 ويتجه شرقًا: ثلاث غرف نوم وحمّامان، {N120.34} و{N120.35} {U} مبنية و{N102.61} {U} مساحة داخلية صالحة للاستخدام.',
  'Woningen 11B in portiek 1, op het westen gericht, en 61B in portiek 6, op het oosten gericht: drie slaapkamers en twee badkamers, {N120.34} en {N120.35} {U} bebouwd en {N102.61} {U} bruikbare binnenoppervlakte.',
  'Mieszkania 11B w klatce 1, od zachodu, i 61B w klatce 6, od wschodu: trzy sypialnie i dwie łazienki, {N120.34} i {N120.35} {U} zabudowy oraz {N102.61} {U} użytkowej powierzchni wewnętrznej.',
  'Boligene 11B i oppgang 1, mot vest, og 61B i oppgang 6, mot øst: tre soverom og to bad, {N120.34} og {N120.35} {U} bruksareal og {N102.61} {U} nyttbart innvendig areal.',
  'Bostäderna 11B i uppgång 1, mot väster, och 61B i uppgång 6, mot öster: tre sovrum och två badrum, {N120.34} och {N120.35} {U} byggyta och {N102.61} {U} användbar invändig yta.')
a('.residences.items[0].points[1]',
  'Un salón-comedor-cocina abierto de unos {N42.4} {U} y un lavadero.',
  'Un séjour-salle à manger-cuisine ouvert d’environ {N42.4} {U} et une buanderie.',
  'Ein offener Wohn-, Ess- und Küchenbereich von rund {N42.4} {U} und ein Hauswirtschaftsraum.',
  'Открытая гостиная-столовая-кухня около {N42.4} {U} и постирочная.',
  'غرفة معيشة وطعام ومطبخ مفتوحة بنحو {N42.4} {U} وغرفة غسيل.',
  'Een open woon-, eet- en keukenruimte van ongeveer {N42.4} {U} en een wasruimte.',
  'Otwarty salon z jadalnią i kuchnią o powierzchni około {N42.4} {U} oraz pomieszczenie gospodarcze.',
  'Et åpent stue-, spise- og kjøkkenrom på rundt {N42.4} {U} og et vaskerom.',
  'Ett öppet vardagsrum, matplats och kök på cirka {N42.4} {U} och ett tvättrum.')
a('.residences.items[0].points[2]',
  'Una terraza cubierta de {N33.06} {U}.', 'Une terrasse couverte de {N33.06} {U}.', 'Eine überdachte Terrasse von {N33.06} {U}.',
  'Крытая терраса {N33.06} {U}.', 'تراس مغطى بمساحة {N33.06} {U}.', 'Een overdekt terras van {N33.06} {U}.',
  'Zadaszony taras o powierzchni {N33.06} {U}.', 'En overbygd terrasse på {N33.06} {U}.', 'En täckt terrass på {N33.06} {U}.')
a('.residences.items[0].points[3]',
  'Una plaza de garaje cada una, y un trastero solo con la 11B, por {E685000} y {E720000}.',
  'Une place de garage chacun, et une cave seulement avec le 11B, pour {E685000} et {E720000}.',
  'Je ein Garagenstellplatz, und ein Abstellraum nur bei 11B, für {E685000} und {E720000}.',
  'По одному месту в гараже, кладовая только у 11B; цены {E685000} и {E720000}.',
  'موقف سيارات في المرآب لكل منهما، وغرفة تخزين مع 11B فقط، بسعر {E685000} و{E720000}.',
  'Elk een garageplaats, en alleen bij 11B een berging, voor {E685000} en {E720000}.',
  'Po jednym miejscu w garażu, a komórka lokatorska tylko przy 11B, za {E685000} i {E720000}.',
  'En garasjeplass hver, og en bod bare med 11B, til {E685000} og {E720000}.',
  'En garageplats vardera, och ett förråd bara med 11B, för {E685000} och {E720000}.')
a('.residences.items[1].name',
  'Dos dormitorios en la segunda planta', 'Deux chambres au deuxième étage', 'Zwei Schlafzimmer im zweiten Obergeschoss',
  'Две спальни на третьем этаже', 'غرفتا نوم في الطابق الثاني', 'Twee slaapkamers op de tweede verdieping',
  'Dwie sypialnie na drugim piętrze', 'To soverom i tredje etasje', 'Två sovrum på andra våningen')
a('.residences.items[1].points[0]',
  'Vivienda 122B en el portal 12, orientada al este: dos dormitorios y dos baños, {N82.53} {U} construidos y {N71.14} {U} de superficie útil interior.',
  'Logement 122B dans la cage 12, orienté à l’est : deux chambres et deux salles de bain, {N82.53} {U} construits et {N71.14} {U} de surface utile intérieure.',
  'Wohnung 122B im Aufgang 12, nach Osten ausgerichtet: zwei Schlafzimmer und zwei Bäder, {N82.53} {U} bebaut und {N71.14} {U} nutzbare Innenfläche.',
  'Квартира 122B в подъезде 12, окна на восток: две спальни и два санузла, {N82.53} {U} застройки и {N71.14} {U} полезной внутренней площади.',
  'المسكن 122B في المدخل 12 ويتجه شرقًا: غرفتا نوم وحمّامان، {N82.53} {U} مبنية و{N71.14} {U} مساحة داخلية صالحة للاستخدام.',
  'Woning 122B in portiek 12, op het oosten gericht: twee slaapkamers en twee badkamers, {N82.53} {U} bebouwd en {N71.14} {U} bruikbare binnenoppervlakte.',
  'Mieszkanie 122B w klatce 12, od wschodu: dwie sypialnie i dwie łazienki, {N82.53} {U} zabudowy oraz {N71.14} {U} użytkowej powierzchni wewnętrznej.',
  'Bolig 122B i oppgang 12, mot øst: to soverom og to bad, {N82.53} {U} bruksareal og {N71.14} {U} nyttbart innvendig areal.',
  'Bostad 122B i uppgång 12, mot öster: två sovrum och två badrum, {N82.53} {U} byggyta och {N71.14} {U} användbar invändig yta.')
a('.residences.items[1].points[1]',
  'Un salón-comedor-cocina de {N31.41} {U}.', 'Un séjour-salle à manger-cuisine de {N31.41} {U}.', 'Ein Wohn-, Ess- und Küchenbereich von {N31.41} {U}.',
  'Гостиная-столовая-кухня {N31.41} {U}.', 'غرفة معيشة وطعام ومطبخ بمساحة {N31.41} {U}.', 'Een woon-, eet- en keukenruimte van {N31.41} {U}.',
  'Salon z jadalnią i kuchnią o powierzchni {N31.41} {U}.', 'Et stue-, spise- og kjøkkenrom på {N31.41} {U}.', 'Ett vardagsrum, matplats och kök på {N31.41} {U}.')
a('.residences.items[1].points[2]',
  'Espacio exterior de {N78.66} {U}: una terraza cubierta de {N29.37} {U}, una terraza descubierta de {N26.59} {U} y un patio de {N22.70} {U}.',
  'Espace extérieur de {N78.66} {U} : une terrasse couverte de {N29.37} {U}, une terrasse découverte de {N26.59} {U} et un patio de {N22.70} {U}.',
  'Außenfläche von {N78.66} {U}: eine überdachte Terrasse von {N29.37} {U}, eine offene Terrasse von {N26.59} {U} und ein Patio von {N22.70} {U}.',
  'Внешняя площадь {N78.66} {U}: крытая терраса {N29.37} {U}, открытая терраса {N26.59} {U} и патио {N22.70} {U}.',
  'مساحة خارجية قدرها {N78.66} {U}: تراس مغطى {N29.37} {U} وتراس مكشوف {N26.59} {U} وفناء {N22.70} {U}.',
  'Buitenruimte van {N78.66} {U}: een overdekt terras van {N29.37} {U}, een open terras van {N26.59} {U} en een patio van {N22.70} {U}.',
  'Przestrzeń zewnętrzna o powierzchni {N78.66} {U}: zadaszony taras {N29.37} {U}, taras odkryty {N26.59} {U} i patio {N22.70} {U}.',
  'Utendørs areal på {N78.66} {U}: en overbygd terrasse på {N29.37} {U}, en åpen terrasse på {N26.59} {U} og en patio på {N22.70} {U}.',
  'Utomhusyta på {N78.66} {U}: en täckt terrass på {N29.37} {U}, en öppen terrass på {N26.59} {U} och en patio på {N22.70} {U}.')
a('.residences.items[1].points[3]',
  'Una plaza de garaje y un trastero, por {E590000}.', 'Une place de garage et une cave, pour {E590000}.', 'Ein Garagenstellplatz und ein Abstellraum, für {E590000}.',
  'Место в гараже и кладовая; цена {E590000}.', 'موقف سيارات في المرآب وغرفة تخزين، بسعر {E590000}.', 'Een garageplaats en een berging, voor {E590000}.',
  'Miejsce w garażu i komórka lokatorska, za {E590000}.', 'En garasjeplass og en bod, til {E590000}.', 'En garageplats och ett förråd, för {E590000}.')
a('.lifestyle.headlineHtml',
  'Piscinas, <em>un gimnasio</em> y un espacio de coworking', 'Des piscines, <em>une salle de sport</em> et un espace de coworking', 'Pools, <em>ein Fitnessraum</em> und ein Coworking-Bereich',
  'Бассейны, <em>тренажёрный зал</em> и коворкинг', 'مسابح، <em>وصالة رياضية</em> ومساحة عمل مشتركة', 'Zwembaden, <em>een fitnessruimte</em> en een coworkingruimte',
  'Baseny, <em>siłownia</em> i przestrzeń coworkingowa', 'Basseng, <em>et treningsrom</em> og et coworkingområde', 'Pooler, <em>ett gym</em> och en coworkingyta')
a('.lifestyle.copy',
  'Una piscina comunitaria y jardines al aire libre, y en el interior una piscina climatizada, un gimnasio, un espacio de coworking y un salón social.',
  'Une piscine commune et des jardins à l’extérieur, et à l’intérieur une piscine chauffée, une salle de sport, un espace de coworking et un salon du club.',
  'Draußen ein Gemeinschaftspool und Gärten, drinnen ein beheizter Pool, ein Fitnessraum, ein Coworking-Bereich und eine Club-Lounge.',
  'Снаружи — общий бассейн и сады, внутри — подогреваемый бассейн, тренажёрный зал, коворкинг и клубный лаундж.',
  'مسبح مشترك وحدائق في الخارج، وفي الداخل مسبح مُدفأ وصالة رياضية ومساحة عمل مشتركة وصالة النادي الاجتماعي.',
  'Buiten een gemeenschappelijk zwembad en tuinen, binnen een verwarmd zwembad, een fitnessruimte, een coworkingruimte en een clublounge.',
  'Na zewnątrz wspólny basen i ogrody, wewnątrz podgrzewany basen, siłownia, przestrzeń coworkingowa i salon klubowy.',
  'Utendørs et fellesbasseng og hager, innendørs et oppvarmet basseng, et treningsrom, et coworkingområde og en klubblounge.',
  'Utomhus en gemensam pool och trädgårdar, inomhus en uppvärmd pool, ett gym, en coworkingyta och en klubblounge.')
a('.lifestyle.panels[0][1]',
  'Piscinas con cloración salina y jardines paisajísticos con iluminación y riego automático, tal como los recoge la memoria de calidades.',
  'Des piscines à l’électrolyse au sel et des jardins paysagers avec éclairage et arrosage automatique, comme les liste le descriptif.',
  'Pools mit Salzelektrolyse und gestaltete Gärten mit Beleuchtung und automatischer Bewässerung, wie sie die Bau- und Ausstattungsbeschreibung aufführt.',
  'Бассейны с солевым хлорированием и ландшафтные сады с освещением и автоматическим поливом, как указано в спецификации.',
  'مسابح بمعالجة بالكلور الملحي وحدائق منسّقة بإضاءة وري آلي، كما ترد في مواصفات البناء.',
  'Zwembaden met zoutelektrolyse en aangelegde tuinen met verlichting en automatische bewatering, zoals de uitvoeringsomschrijving ze opsomt.',
  'Baseny z chlorowaniem solnym i zagospodarowane ogrody z oświetleniem i automatycznym nawadnianiem, jak wymienia je specyfikacja.',
  'Basseng med saltklorering og anlagte hager med belysning og automatisk vanning, slik byggebeskrivelsen lister dem.',
  'Pooler med saltklorering och anlagda trädgårdar med belysning och automatisk bevattning, som byggbeskrivningen anger dem.')
a('.lifestyle.panels[1][1]',
  'Una piscina interior climatizada y un gimnasio totalmente equipado con instalaciones de última generación.',
  'Une piscine intérieure chauffée et une salle de sport entièrement équipée, avec des équipements de dernière génération.',
  'Ein beheizter Innenpool und ein voll ausgestatteter Fitnessraum mit modernster Ausstattung.',
  'Крытый подогреваемый бассейн и полностью оборудованный тренажёрный зал с современным оснащением.',
  'مسبح داخلي مُدفأ وصالة رياضية مجهزة بالكامل بأحدث التجهيزات.',
  'Een verwarmd binnenzwembad en een volledig uitgeruste fitnessruimte met state-of-the-art apparatuur.',
  'Podgrzewany basen wewnętrzny i w pełni wyposażona siłownia z najnowocześniejszym sprzętem.',
  'Et oppvarmet innendørsbasseng og et fullt utstyrt treningsrom med toppmoderne utstyr.',
  'En uppvärmd inomhuspool och ett fullt utrustat gym med toppmodern utrustning.')
a('.lifestyle.panels[2][0]',
  'Trabajo y reuniones', 'Travail et rencontres', 'Arbeiten und Treffen', 'Работа и общение', 'العمل واللقاء', 'Werken en ontmoeten', 'Praca i spotkania', 'Arbeid og samvær', 'Arbete och samvaro')
a('.lifestyle.panels[2][1]',
  'Un espacio de coworking y un salón social amplio y luminoso para relajarse con amigos.',
  'Un espace de coworking et un salon du club spacieux et lumineux pour se détendre entre amis.',
  'Ein Coworking-Bereich und eine helle, geräumige Club-Lounge zum Entspannen mit Freunden.',
  'Коворкинг и светлый просторный клубный лаундж, где можно отдохнуть с друзьями.',
  'مساحة عمل مشتركة وصالة اجتماعية واسعة ومشرقة للاسترخاء مع الأصدقاء.',
  'Een coworkingruimte en een lichte, ruime clublounge om met vrienden te ontspannen.',
  'Przestrzeń coworkingowa i jasny, przestronny salon klubowy do odpoczynku w gronie przyjaciół.',
  'Et coworkingområde og en lys, romslig klubblounge for å slappe av med venner.',
  'En coworkingyta och en ljus, rymlig klubblounge för att koppla av med vänner.')
a('.lifestyle.panels[3][0]',
  'Su propio espacio', 'Votre propre espace', 'Ihr eigener Raum', 'Ваше личное пространство', 'مساحتك الخاصة', 'Uw eigen ruimte', 'Państwa własna przestrzeń', 'Ditt eget rom', 'Ert eget utrymme')
a('.lifestyle.panels[3][1]',
  'Las tres viviendas de la lista tienen entre {N33.06} y {N78.66} {U} de espacio exterior. Todos los áticos tienen jacuzzi, y también algunas viviendas en planta baja.',
  'Les trois logements de la liste ont de {N33.06} à {N78.66} {U} d’espace extérieur. Chaque penthouse a un jacuzzi, tout comme certains logements en rez-de-chaussée.',
  'Die drei Wohnungen der Liste haben {N33.06} bis {N78.66} {U} Außenfläche. Jedes Penthouse hat einen Whirlpool, ebenso einige Erdgeschosswohnungen.',
  'У трёх квартир из списка от {N33.06} до {N78.66} {U} внешней площади. В каждом пентхаусе есть джакузи, как и в некоторых квартирах на первом этаже.',
  'للمساكن الثلاثة في القائمة مساحة خارجية تتراوح بين {N33.06} و{N78.66} {U}. في كل بنتهاوس جاكوزي، وكذلك في بعض مساكن الطابق الأرضي.',
  'De drie woningen op de lijst hebben {N33.06} tot {N78.66} {U} buitenruimte. Elk penthouse heeft een jacuzzi, net als enkele woningen op de begane grond.',
  'Trzy mieszkania z listy mają od {N33.06} do {N78.66} {U} przestrzeni zewnętrznej. Każdy penthouse ma jacuzzi, podobnie jak niektóre mieszkania na parterze.',
  'De tre boligene på listen har fra {N33.06} til {N78.66} {U} utendørs areal. Hver toppleilighet har jacuzzi, og det har også noen av boligene i første etasje.',
  'De tre bostäderna på listan har från {N33.06} till {N78.66} {U} utomhusyta. Varje takvåning har jacuzzi, och det har även några av bostäderna i bottenvåningen.')
a('.location.headlineHtml',
  'Altos de los Monteros, <em>en Marbella</em>', 'Altos de los Monteros, <em>à Marbella</em>', 'Altos de los Monteros, <em>in Marbella</em>',
  'Альтос-де-лос-Монтерос, <em>в Марбелье</em>', 'ألتوس دي لوس مونتيروس، <em>في ماربيا</em>', 'Altos de los Monteros, <em>in Marbella</em>',
  'Altos de los Monteros, <em>w Marbelli</em>', 'Altos de los Monteros, <em>i Marbella</em>', 'Altos de los Monteros, <em>i Marbella</em>')
a('.location.copy',
  'Los documentos del promotor sitúan las viviendas en Marbella, que el dossier describe como un destino de ritmo de vida relajado y sofisticado y con más de 12 km de playas con bandera azul. No dan dirección ni coordenadas de la parcela, por lo que el mapa muestra la zona de Altos de los Monteros.',
  'Les documents du promoteur situent les logements à Marbella, que le dossier décrit comme une station au rythme de vie détendu et sophistiqué, avec plus de 12 km de plages Pavillon bleu. Ils ne donnent ni adresse ni coordonnées de la parcelle ; la carte montre donc le secteur d’Altos de los Monteros.',
  'Die Unterlagen des Bauträgers verorten die Wohnungen in Marbella, das die Broschüre als Ferienort mit entspanntem, mondänem Lebensstil und über 12 km Blaue-Flagge-Stränden beschreibt. Sie geben weder Adresse noch Koordinaten des Grundstücks an, daher zeigt die Karte das Gebiet von Altos de los Monteros.',
  'В документах застройщика квартиры расположены в Марбелье, который в буклете описан как курорт с расслабленным и изысканным образом жизни и более чем 12 км пляжей с «Голубым флагом». Адреса и координат участка в них нет, поэтому на карте показан район Альтос-де-лос-Монтерос.',
  'تضع وثائق المطوّر المساكن في ماربيا، التي يصفها الكتيّب منتجعًا بإيقاع حياة هادئ وراقٍ وأكثر من 12 كم من الشواطئ الحاصلة على العلم الأزرق. ولا تذكر عنوانًا ولا إحداثيات للقطعة، لذلك تعرض الخريطة منطقة ألتوس دي لوس مونتيروس.',
  'De documenten van de ontwikkelaar plaatsen de woningen in Marbella, dat de brochure beschrijft als een oord met een ontspannen en verfijnd levensritme en meer dan 12 km blauwe-vlagstranden. Ze geven geen adres of coördinaat van het perceel, dus de kaart toont het gebied Altos de los Monteros.',
  'Dokumenty dewelopera umieszczają mieszkania w Marbelli, którą broszura opisuje jako kurort o spokojnym i wyrafinowanym rytmie życia, z ponad 12 km plaż z Błękitną Flagą. Nie podają adresu ani współrzędnych działki, dlatego mapa pokazuje okolicę Altos de los Monteros.',
  'Utbyggerens dokumenter plasserer boligene i Marbella, som brosjyren beskriver som et sted med et avslappet og sofistikert livstempo og over 12 km strender med Blått Flagg. De oppgir verken adresse eller koordinater for tomten, så kartet viser området Altos de los Monteros.',
  'Exploatörens dokument placerar bostäderna i Marbella, som broschyren beskriver som en ort med avslappnat och sofistikerat livstempo och över 12 km blåflaggade stränder. De anger varken adress eller koordinater för tomten, så kartan visar området Altos de los Monteros.')

# ---- investment, trust, availability ------------------------------------------------------------------

a('.investment.cards[0][1]',
  'La lista de precios se expresa antes del IVA. Con un IVA del 10 por ciento y un impuesto de actos jurídicos documentados del 1,20 por ciento, los tipos habituales, la vivienda más barata cuesta unos {E66000} más y la más cara unos {E81000} más, antes de notaría y registro.',
  'La liste de prix s’entend avant TVA. Avec une TVA de 10 pour cent et un droit de timbre de 1,20 pour cent, les taux usuels, le logement le moins cher coûte environ {E66000} de plus et le plus cher environ {E81000} de plus, avant frais de notaire et d’enregistrement.',
  'Die Preisliste versteht sich vor MwSt. Bei 10 Prozent MwSt. und 1,20 Prozent Stempelsteuer, den üblichen Sätzen, kostet die günstigste Wohnung rund {E66000} mehr und die teuerste rund {E81000} mehr, vor Notar- und Grundbuchkosten.',
  'Прайс-лист указан без НДС. При НДС 10 процентов и гербовом сборе 1,20 процента, то есть по обычным ставкам, самая дешёвая квартира обойдётся примерно на {E66000} дороже, а самая дорогая — примерно на {E81000}, до расходов на нотариуса и регистрацию.',
  'قائمة الأسعار قبل ضريبة القيمة المضافة. بنسبة 10 بالمئة لضريبة القيمة المضافة و1.20 بالمئة لرسم الدمغة، وهما النسبتان المعتادتان، يكلّف أرخص مسكن نحو {E66000} إضافية وأغلاها نحو {E81000} إضافية، قبل أتعاب التوثيق والتسجيل.',
  'De prijslijst is exclusief btw. Bij 10 procent btw en 1,20 procent overdrachtsbelasting, de gangbare tarieven, kost de goedkoopste woning ongeveer {E66000} meer en de duurste ongeveer {E81000} meer, vóór notaris- en kadasterkosten.',
  'Cennik podano przed VAT. Przy VAT w wysokości 10 procent i podatku od czynności cywilnoprawnych w wysokości 1,20 procent, czyli standardowych stawkach, najtańsze mieszkanie kosztuje około {E66000} więcej, a najdroższe około {E81000} więcej, przed opłatami notarialnymi i wieczystoksięgowymi.',
  'Prislisten er oppgitt før mva. Med 10 prosent mva. og 1,20 prosent dokumentavgift, de vanlige satsene, koster den rimeligste boligen rundt {E66000} mer og den dyreste rundt {E81000} mer, før notar- og tinglysingsgebyrer.',
  'Prislistan anges före IVA. Med 10 procents IVA och 1,20 procents stämpelskatt, de vanliga satserna, kostar den billigaste bostaden cirka {E66000} mer och den dyraste cirka {E81000} mer, före notarie- och registreringsavgifter.')
a('.investment.cards[1][0]',
  'La entrega no se indica', 'La livraison n’est pas indiquée', 'Der Fertigstellungstermin ist nicht angegeben', 'Срок сдачи не указан',
  'موعد التسليم غير مذكور', 'De oplevering wordt niet genoemd', 'Termin oddania nie jest podany', 'Overleveringen er ikke oppgitt', 'Tillträdet anges inte')
a('.investment.cards[1][1]',
  'Ningún documento indica fecha de entrega, y el 60 por ciento del precio vence en la entrega de llaves. Pregunte qué dice el contrato si la fecha se retrasa.',
  'Aucun document n’indique de date de livraison, et 60 pour cent du prix sont exigibles à l’achèvement et à la remise des clés. Demandez ce que dit le contrat si la date glisse.',
  'Kein Dokument nennt einen Fertigstellungstermin, und 60 Prozent des Preises werden bei Fertigstellung und Schlüsselübergabe fällig. Fragen Sie, was der Vertrag bei einer Verzögerung vorsieht.',
  'Ни в одном документе нет срока сдачи, а 60 процентов цены подлежат оплате при завершении строительства и передаче ключей. Спросите, что говорит договор на случай переноса срока.',
  'لا تذكر أي وثيقة موعد إنجاز، و60 بالمئة من السعر تُستحق عند الإنجاز وتسليم المفاتيح. اسألوا عمّا ينصّ عليه العقد إذا تأخّر الموعد.',
  'Geen enkel document noemt een opleveringsdatum, en 60 procent van de prijs is verschuldigd bij oplevering en sleuteloverdracht. Vraag wat het contract zegt als de datum opschuift.',
  'Żaden dokument nie podaje terminu oddania, a 60 procent ceny staje się wymagalne przy zakończeniu budowy i przekazaniu kluczy. Warto zapytać, co mówi umowa na wypadek przesunięcia terminu.',
  'Ingen dokumenter oppgir en overleveringsdato, og 60 prosent av prisen forfaller ved ferdigstillelse og overlevering av nøklene. Spør hva kontrakten sier hvis datoen forskyves.',
  'Inget dokument anger något tillträdesdatum, och 60 procent av priset förfaller vid färdigställande och nyckelöverlämning. Fråga vad avtalet säger om datumet skjuts upp.')
a('.investment.cards[2][0]',
  'Tres de 57 figuran en la lista', 'Trois logements sur 57 figurent sur la liste', 'Drei von 57 stehen auf der Liste', 'В списке три из 57',
  'ثلاثة من 57 مدرجة في القائمة', 'Drie van de 57 staan op de lijst', 'Na liście są trzy z 57', 'Tre av 57 står på listen', 'Tre av 57 finns på listan')
a('.investment.cards[2][1]',
  'La lista de precios recoge tres viviendas. No se indica cuáles de las demás están vendidas, reservadas o aún sin liberar, así que una visita empieza con la lista completa.',
  'La liste de prix couvre trois logements. Elle n’indique pas lesquels des autres sont vendus, réservés ou pas encore mis en vente ; une visite commence donc par la liste complète.',
  'Die Preisliste umfasst drei Wohnungen. Welche der übrigen verkauft, reserviert oder noch nicht freigegeben sind, ist nicht angegeben; eine Besichtigung beginnt daher mit der vollständigen Liste.',
  'В прайс-листе три квартиры. Какие из остальных проданы, забронированы или ещё не выставлены, не указано, поэтому знакомство с проектом начинается с полного списка.',
  'تغطي قائمة الأسعار ثلاثة مساكن. ولا يُذكر أيٌّ من الباقي مباع أو محجوز أو لم يُطرح بعد، لذلك تبدأ المعاينة بالقائمة الكاملة.',
  'De prijslijst omvat drie woningen. Welke van de andere verkocht, gereserveerd of nog niet vrijgegeven zijn, wordt niet vermeld, dus een bezichtiging begint met de volledige lijst.',
  'Cennik obejmuje trzy mieszkania. Nie wiadomo, które z pozostałych są sprzedane, zarezerwowane lub jeszcze nieudostępnione, dlatego oglądanie zaczyna się od pełnej listy.',
  'Prislisten dekker tre boliger. Hvilke av de andre som er solgt, reservert eller ikke ennå lagt ut, er ikke oppgitt, så en visning begynner med den fullstendige listen.',
  'Prislistan omfattar tre bostäder. Vilka av de övriga som är sålda, reserverade eller ännu inte släppta anges inte, så en visning börjar med den fullständiga listan.')
a('.investment.cards[3][1]',
  'El diez por ciento a los seis meses y el diez por ciento a los doce meses se cuentan desde el contrato privado, no desde el avance de la obra.',
  'Dix pour cent à six mois et dix pour cent à douze mois sont comptés à partir du contrat privé, et non de l’avancement du chantier.',
  'Zehn Prozent nach sechs Monaten und zehn Prozent nach zwölf Monaten werden ab dem privaten Kaufvertrag gerechnet, nicht ab dem Baufortschritt.',
  'Десять процентов через шесть месяцев и десять процентов через двенадцать месяцев отсчитываются от частного договора, а не от хода строительства.',
  'عشرة بالمئة بعد ستة أشهر وعشرة بالمئة بعد اثني عشر شهرًا تُحتسب من تاريخ العقد الخاص لا من تقدّم البناء.',
  'Tien procent na zes maanden en tien procent na twaalf maanden worden gerekend vanaf het onderhandse contract, niet vanaf de voortgang van de bouw.',
  'Dziesięć procent po sześciu miesiącach i dziesięć procent po dwunastu miesiącach liczy się od umowy przedwstępnej, a nie od postępu budowy.',
  'Ti prosent etter seks måneder og ti prosent etter tolv måneder regnes fra den private kontrakten, ikke fra byggets fremdrift.',
  'Tio procent efter sex månader och tio procent efter tolv månader räknas från det privata avtalet, inte från byggets framdrift.')
a('.trustDossier.cards[0][1]',
  'Ninguno de los documentos que tenemos indica fecha de entrega, estado de la licencia ni fase de las obras. La memoria de calidades es del 20 de septiembre de 2023 y los planos son la revisión 02 del 5 de enero de 2024, así que pedimos la licencia, el inicio de las obras y la fecha contractual.',
  'Aucun des documents en notre possession n’indique de date de livraison, de statut du permis ni de phase des travaux. Le descriptif date du 20 septembre 2023 et les plans sont la révision 02 du 5 janvier 2024 ; nous demandons donc le permis, le début des travaux et la date contractuelle.',
  'Keines der Dokumente, die uns vorliegen, nennt einen Fertigstellungstermin, den Stand der Baugenehmigung oder einen Baufortschritt. Die Bau- und Ausstattungsbeschreibung ist vom 20. September 2023 und die Pläne sind die Revision 02 vom 5. Januar 2024, daher fragen wir nach der Genehmigung, dem Baubeginn und dem vertraglichen Termin.',
  'Ни в одном из имеющихся у нас документов нет срока сдачи, статуса разрешения или стадии работ. Спецификация датирована 20 сентября 2023 года, а планы — ревизия 02 от 5 января 2024 года, поэтому мы запрашиваем разрешение, начало работ и договорный срок.',
  'لا تذكر أيٌّ من الوثائق التي بحوزتنا موعد إنجاز أو وضع الرخصة أو مرحلة الأعمال. مواصفات البناء مؤرخة 20 سبتمبر 2023 والمخططات هي المراجعة 02 المؤرخة 5 يناير 2024، لذلك نطلب الرخصة وبدء الأعمال والموعد التعاقدي.',
  'Geen van de documenten die we hebben noemt een opleveringsdatum, de status van de vergunning of een bouwfase. De uitvoeringsomschrijving is van 20 september 2023 en de plattegronden zijn revisie 02 van 5 januari 2024, dus we vragen om de vergunning, de start van de werken en de contractuele datum.',
  'Żaden z dokumentów, które mamy, nie podaje terminu oddania, statusu pozwolenia ani etapu robót. Specyfikacja pochodzi z 20 września 2023 roku, a rzuty to rewizja 02 z 5 stycznia 2024 roku, dlatego prosimy o pozwolenie, rozpoczęcie robót i termin umowny.',
  'Ingen av dokumentene vi har, oppgir en overleveringsdato, byggetillatelsens status eller byggetrinn. Byggebeskrivelsen er datert 20. september 2023, og plantegningene er revisjon 02 av 5. januar 2024, så vi ber om byggetillatelsen, byggestart og den kontraktfestede datoen.',
  'Inget av dokumenten vi har anger något tillträdesdatum, bygglovets status eller byggskede. Byggbeskrivningen är daterad 20 september 2023 och planritningarna är revision 02 av 5 januari 2024, så vi ber om bygglovet, byggstarten och det avtalade datumet.')
a('.trustDossier.cards[1][1]',
  'Los documentos que tenemos no dicen nada sobre un aval para las cantidades entregadas a cuenta. La ley española lo exige en las ventas sobre plano, así que pedimos ver el aval en sí antes de cualquier pago.',
  'Les documents en notre possession ne disent rien d’une garantie pour les sommes versées d’avance. La loi espagnole l’exige pour les ventes sur plan ; nous demandons donc à voir la garantie elle-même avant tout paiement.',
  'Die uns vorliegenden Dokumente sagen nichts über eine Bürgschaft für Anzahlungen. Das spanische Recht verlangt sie bei Verkäufen vom Plan, daher lassen wir uns die Bürgschaft selbst zeigen, bevor etwas gezahlt wird.',
  'В имеющихся у нас документах ничего не сказано о гарантии на внесённые суммы. Испанское право требует её при продаже на стадии проекта, поэтому мы просим показать саму гарантию до любого платежа.',
  'لا تقول الوثائق التي بحوزتنا شيئًا عن كفالة للمبالغ المدفوعة على الحساب. يشترطها القانون الإسباني في البيع على المخطط، لذلك نطلب رؤية الكفالة نفسها قبل أي دفعة.',
  'De documenten die we hebben zeggen niets over een garantie voor voorschotten. De Spaanse wet eist er een bij verkoop op plan, dus we vragen de garantie zelf te zien vóór enige betaling.',
  'Dokumenty, którymi dysponujemy, nic nie mówią o gwarancji dla wpłat na poczet ceny. Prawo hiszpańskie wymaga jej przy sprzedaży z planu, dlatego przed jakąkolwiek płatnością prosimy o wgląd w samą gwarancję.',
  'Dokumentene vi har, sier ingenting om en garanti for innbetalte beløp. Spansk lov krever en slik garanti ved salg på tegning, så vi ber om å se selve garantien før noen betaling.',
  'Dokumenten vi har säger ingenting om en garanti för inbetalda belopp. Spansk lag kräver en sådan vid försäljning på ritning, så vi ber att få se själva garantin före varje betalning.')
a('.trustDossier.cards[2][1]',
  'Los precios y las superficies están transcritos de la lista de precios del 3 de noviembre de 2026 y coinciden con los planos. La lista no dice qué ha pasado con las otras 54 viviendas, así que pedimos la lista completa.',
  'Les prix et les surfaces sont transcrits de la liste de prix du 3 novembre 2026 et concordent avec les plans. La liste ne dit pas ce qu’il est advenu des 54 autres logements ; nous demandons donc la liste complète.',
  'Preise und Flächen sind aus der Preisliste vom 3. November 2026 übernommen und stimmen mit den Plänen überein. Die Liste sagt nicht, was aus den anderen 54 Wohnungen geworden ist, daher fragen wir nach der vollständigen Liste.',
  'Цены и площади переписаны из прайс-листа от 3 ноября 2026 года и совпадают с планами. В списке не сказано, что стало с остальными 54 квартирами, поэтому мы запрашиваем полный список.',
  'الأسعار والمساحات منقولة من قائمة الأسعار المؤرخة 3 نوفمبر 2026 وتتفق مع المخططات. ولا تقول القائمة ما آل إليه المساكن الـ54 الأخرى، لذلك نطلب القائمة الكاملة.',
  'Prijzen en oppervlakten zijn overgenomen uit de prijslijst van 3 november 2026 en komen overeen met de plattegronden. De lijst zegt niet wat er met de andere 54 woningen is gebeurd, dus we vragen om de volledige lijst.',
  'Ceny i powierzchnie są przepisane z cennika z 3 listopada 2026 roku i zgadzają się z rzutami. Cennik nie mówi, co stało się z pozostałymi 54 mieszkaniami, dlatego prosimy o pełną listę.',
  'Priser og arealer er overført fra prislisten av 3. november 2026 og stemmer med plantegningene. Listen sier ikke hva som har skjedd med de andre 54 boligene, så vi ber om den fullstendige listen.',
  'Priser och ytor är avskrivna från prislistan av 3 november 2026 och stämmer med planritningarna. Listan säger inte vad som har hänt med de övriga 54 bostäderna, så vi ber om den fullständiga listan.')
a('.trustDossier.cards[3][1]',
  'La lista de precios indica que sus precios son válidos durante dos días desde su descarga. Reconfirmamos la cifra con el vendedor antes de que usted reserve.',
  'La liste de prix indique que ses prix sont valables deux jours après son téléchargement. Nous reconfirmons le chiffre auprès du vendeur avant que vous ne réserviez.',
  'Die Preisliste gibt an, dass ihre Preise nach dem Herunterladen zwei Tage lang gültig sind. Wir bestätigen die Zahl beim Verkäufer erneut, bevor Sie reservieren.',
  'В прайс-листе сказано, что цены действительны в течение двух дней после его загрузки. Мы повторно подтверждаем цифру у продавца до того, как вы забронируете.',
  'تذكر قائمة الأسعار أن أسعارها صالحة لمدة يومين بعد تنزيلها. نعيد تأكيد الرقم مع البائع قبل أن تحجزوا.',
  'De prijslijst geeft aan dat haar prijzen twee dagen na het downloaden geldig zijn. We bevestigen het bedrag opnieuw bij de verkoper voordat u reserveert.',
  'Cennik podaje, że jego ceny są ważne przez dwa dni od pobrania. Ponownie potwierdzamy kwotę u sprzedawcy, zanim Państwo zarezerwują.',
  'Prislisten oppgir at prisene er gyldige i to dager etter at den er lastet ned. Vi bekrefter beløpet på nytt med selgeren før De reserverer.',
  'Prislistan anger att priserna gäller i två dagar efter nedladdningen. Vi bekräftar beloppet med säljaren på nytt innan ni bokar.')
a('.trustDossier.cards[4][1]',
  'Las imágenes están generadas por ordenador, y los planos indican que pueden cambiar durante las obras por exigencias técnicas o jurídicas. El mobiliario que aparece no está incluido.',
  'Les images sont générées par ordinateur, et les plans précisent qu’ils peuvent changer pendant les travaux pour des raisons techniques ou juridiques. Le mobilier représenté n’est pas inclus.',
  'Die Bilder sind computergeneriert, und die Pläne weisen darauf hin, dass sie sich während der Bauarbeiten aus technischen oder rechtlichen Gründen ändern können. Die gezeigten Möbel sind nicht enthalten.',
  'Изображения созданы на компьютере, а в планах оговорено, что они могут измениться в ходе работ по техническим или юридическим причинам. Показанная мебель не входит в стоимость.',
  'الصور مولَّدة بالحاسوب، وتنصّ المخططات على أنها قد تتغيّر أثناء الأعمال لأسباب فنية أو قانونية. الأثاث الظاهر غير مشمول.',
  'De beelden zijn computergegenereerd, en de plattegronden vermelden dat ze tijdens de werken om technische of juridische redenen kunnen wijzigen. Het getoonde meubilair is niet inbegrepen.',
  'Wizualizacje są wygenerowane komputerowo, a rzuty zastrzegają, że mogą się zmienić w trakcie robót z przyczyn technicznych lub prawnych. Pokazane meble nie są wliczone.',
  'Bildene er datagenerert, og plantegningene sier at de kan endres under byggearbeidene av tekniske eller juridiske grunner. Møblene som vises, er ikke inkludert.',
  'Bilderna är datorgenererade, och planritningarna anger att de kan ändras under arbetena av tekniska eller juridiska skäl. Möblerna som visas ingår inte.')

a('.availability.copy',
  'Los precios son los de la lista de precios del promotor del 3 de noviembre de 2026 y no incluyen IVA. La lista indica que sus precios son válidos durante dos días desde su descarga, así que confirmamos precio y disponibilidad antes de cualquier reserva. Recoge 3 de las 57 viviendas y muestra cada una como disponible.',
  'Les prix sont ceux de la liste de prix du promoteur du 3 novembre 2026 et s’entendent hors TVA. La liste indique que ses prix sont valables deux jours après son téléchargement ; nous confirmons donc prix et disponibilité avant toute réservation. Elle nomme 3 des 57 logements et indique chacun comme disponible.',
  'Die Preise stammen aus der Preisliste des Bauträgers vom 3. November 2026 und verstehen sich ohne MwSt. Die Liste gibt an, dass ihre Preise nach dem Herunterladen zwei Tage lang gültig sind, daher bestätigen wir Preis und Verfügbarkeit vor jeder Reservierung. Sie nennt 3 der 57 Wohnungen und zeigt jede als verfügbar.',
  'Цены взяты из прайс-листа застройщика от 3 ноября 2026 года и указаны без НДС. В списке сказано, что цены действительны в течение двух дней после его загрузки, поэтому мы подтверждаем цену и наличие до любого бронирования. В нём названы 3 из 57 квартир, и каждая указана как доступная.',
  'الأسعار هي أسعار قائمة المطوّر المؤرخة 3 نوفمبر 2026 ولا تشمل ضريبة القيمة المضافة. تذكر القائمة أن أسعارها صالحة لمدة يومين بعد تنزيلها، لذلك نؤكد السعر والتوفر قبل أي حجز. وهي تذكر 3 من المساكن الـ57 وتُظهر كلًّا منها متاحًا.',
  'De prijzen zijn die van de prijslijst van de ontwikkelaar van 3 november 2026 en zijn exclusief btw. De lijst geeft aan dat haar prijzen twee dagen na het downloaden geldig zijn, dus we bevestigen prijs en beschikbaarheid vóór elke reservering. Ze noemt 3 van de 57 woningen en toont elk als beschikbaar.',
  'Ceny pochodzą z cennika dewelopera z 3 listopada 2026 roku i nie zawierają VAT. Cennik podaje, że jego ceny są ważne przez dwa dni od pobrania, dlatego przed każdą rezerwacją potwierdzamy cenę i dostępność. Wymienia 3 z 57 mieszkań i pokazuje każde jako dostępne.',
  'Prisene er de fra utbyggerens prisliste av 3. november 2026 og er uten mva. Listen oppgir at prisene er gyldige i to dager etter at den er lastet ned, så vi bekrefter pris og tilgjengelighet før enhver reservasjon. Den nevner 3 av de 57 boligene og viser hver som tilgjengelig.',
  'Priserna är de i exploatörens prislista av 3 november 2026 och är exklusive IVA. Listan anger att priserna gäller i två dagar efter nedladdningen, så vi bekräftar pris och tillgänglighet före varje bokning. Den nämner 3 av de 57 bostäderna och visar var och en som tillgänglig.')
a('.availability.priceRange',
  '{E590000} - {E720000} + IVA', '{E590000} - {E720000} + TVA', '{E590000} - {E720000} + MwSt.', '{E590000} - {E720000} + НДС', '{E590000} - {E720000} + ضريبة القيمة المضافة',
  '{E590000} - {E720000} + btw', '{E590000} - {E720000} + VAT', '{E590000} - {E720000} + mva.', '{E590000} - {E720000} + IVA')
a('.availability.sourceNote',
  'Los precios y las superficies están transcritos de la lista de precios del promotor del 3 de noviembre de 2026, que recoge tres de las 57 viviendas y muestra cada una como disponible. La lista indica que el IVA no está incluido y que sus precios son válidos durante dos días desde su descarga. Las superficies de la lista coinciden con los planos. Los planos dan además la superficie construida con la parte proporcional de las zonas comunes: {N141.33}, {N141.34} y {N99.64} {U}. La lista llama bloque al portal. Muestra una plaza de garaje por vivienda y un trastero para la 11B y la 122B, pero ninguno para la 61B. El IVA de una vivienda nueva es del 10 por ciento y el impuesto de actos jurídicos documentados en Andalucía del 1,20 por ciento, tipos habituales que los documentos no indican, de modo que la vivienda de {E590000} cuesta unos {E656000} y la de {E720000} unos {E801000} antes de notaría y registro.',
  'Les prix et les surfaces sont transcrits de la liste de prix du promoteur du 3 novembre 2026, qui nomme trois des 57 logements et indique chacun comme disponible. La liste précise que la TVA n’est pas incluse et que ses prix sont valables deux jours après son téléchargement. Les surfaces de la liste concordent avec les plans. Les plans donnent en outre la surface construite avec une quote-part des parties communes : {N141.33}, {N141.34} et {N99.64} {U}. La liste appelle la cage un bloc. Elle indique une place de garage par logement et une cave pour le 11B et le 122B, mais aucune pour le 61B. La TVA sur un logement neuf est de 10 pour cent et le droit de timbre en Andalousie de 1,20 pour cent, des taux usuels que les documents n’indiquent pas ; le logement à {E590000} coûte donc environ {E656000} et celui à {E720000} environ {E801000} avant frais de notaire et d’enregistrement.',
  'Preise und Flächen sind aus der Preisliste des Bauträgers vom 3. November 2026 übernommen, die drei der 57 Wohnungen nennt und jede als verfügbar zeigt. Die Liste besagt, dass die MwSt. nicht enthalten ist und ihre Preise nach dem Herunterladen zwei Tage lang gültig sind. Die Flächen der Liste stimmen mit den Plänen überein. Die Pläne geben zusätzlich die bebaute Fläche mit einem Anteil an den Gemeinschaftsflächen an: {N141.33}, {N141.34} und {N99.64} {U}. Die Liste nennt den Aufgang einen Block. Sie zeigt einen Garagenstellplatz je Wohnung und einen Abstellraum für 11B und 122B, aber keinen für 61B. Die MwSt. beträgt bei einer Neubauwohnung 10 Prozent und die Stempelsteuer in Andalusien 1,20 Prozent, übliche Sätze, die die Dokumente nicht nennen; die Wohnung zu {E590000} kostet damit rund {E656000} und die zu {E720000} rund {E801000}, vor Notar- und Grundbuchkosten.',
  'Цены и площади переписаны из прайс-листа застройщика от 3 ноября 2026 года, в котором названы три из 57 квартир и каждая указана как доступная. В списке сказано, что НДС не включён и что цены действительны в течение двух дней после загрузки. Площади в списке совпадают с планами. В планах также указана площадь застройки с долей общих зон: {N141.33}, {N141.34} и {N99.64} {U}. В списке подъезд назван блоком. Для каждой квартиры указано одно место в гараже, а кладовая — для 11B и 122B, но не для 61B. НДС на новое жильё составляет 10 процентов, а гербовый сбор в Андалусии — 1,20 процента; это обычные ставки, в документах они не указаны, поэтому квартира за {E590000} обойдётся примерно в {E656000}, а за {E720000} — примерно в {E801000}, до расходов на нотариуса и регистрацию.',
  'الأسعار والمساحات منقولة من قائمة المطوّر المؤرخة 3 نوفمبر 2026، وهي تذكر ثلاثة من المساكن الـ57 وتُظهر كلًّا منها متاحًا. تذكر القائمة أن ضريبة القيمة المضافة غير مشمولة وأن أسعارها صالحة لمدة يومين بعد تنزيلها. تتفق مساحات القائمة مع المخططات. وتعطي المخططات أيضًا المساحة المبنية مع حصة من المناطق المشتركة: {N141.33} و{N141.34} و{N99.64} {U}. وتسمّي القائمة المدخل «مبنى». تُظهر موقف سيارات واحدًا لكل مسكن وغرفة تخزين للمسكنين 11B و122B ولا غرفة للمسكن 61B. ضريبة القيمة المضافة على المسكن الجديد 10 بالمئة ورسم الدمغة في الأندلس 1.20 بالمئة، وهما نسبتان معتادتان لا تذكرهما الوثائق، فيكلّف المسكن البالغ {E590000} نحو {E656000} والبالغ {E720000} نحو {E801000} قبل أتعاب التوثيق والتسجيل.',
  'Prijzen en oppervlakten zijn overgenomen uit de prijslijst van de ontwikkelaar van 3 november 2026, die drie van de 57 woningen noemt en elk als beschikbaar toont. De lijst vermeldt dat btw niet is inbegrepen en dat haar prijzen twee dagen na het downloaden geldig zijn. De oppervlakten op de lijst komen overeen met de plattegronden. De plattegronden geven daarnaast de bebouwde oppervlakte met een aandeel in de gemeenschappelijke delen: {N141.33}, {N141.34} en {N99.64} {U}. De lijst noemt de portiek een blok. Ze toont één garageplaats per woning en een berging voor 11B en 122B, maar geen voor 61B. Btw op een nieuwbouwwoning is 10 procent en overdrachtsbelasting in Andalusië 1,20 procent, gangbare tarieven die de documenten niet noemen; de woning van {E590000} kost dus ongeveer {E656000} en die van {E720000} ongeveer {E801000}, vóór notaris- en kadasterkosten.',
  'Ceny i powierzchnie są przepisane z cennika dewelopera z 3 listopada 2026 roku, który wymienia trzy z 57 mieszkań i pokazuje każde jako dostępne. Cennik podaje, że VAT nie jest wliczony, a jego ceny są ważne przez dwa dni od pobrania. Powierzchnie z cennika zgadzają się z rzutami. Rzuty podają ponadto powierzchnię zabudowy z udziałem w częściach wspólnych: {N141.33}, {N141.34} i {N99.64} {U}. Cennik nazywa klatkę blokiem. Pokazuje jedno miejsce w garażu na mieszkanie oraz komórkę lokatorską dla 11B i 122B, ale nie dla 61B. VAT na nowe mieszkanie wynosi 10 procent, a podatek od czynności cywilnoprawnych w Andaluzji 1,20 procent, są to standardowe stawki, których dokumenty nie podają; mieszkanie za {E590000} kosztuje więc około {E656000}, a mieszkanie za {E720000} około {E801000}, przed opłatami notarialnymi i wieczystoksięgowymi.',
  'Priser og arealer er overført fra utbyggerens prisliste av 3. november 2026, som nevner tre av de 57 boligene og viser hver som tilgjengelig. Listen oppgir at mva. ikke er inkludert og at prisene er gyldige i to dager etter at den er lastet ned. Arealene på listen stemmer med plantegningene. Plantegningene oppgir dessuten bruksarealet med en andel av fellesarealene: {N141.33}, {N141.34} og {N99.64} {U}. Listen kaller oppgangen en blokk. Den viser én garasjeplass per bolig og en bod for 11B og 122B, men ingen for 61B. Mva. på en ny bolig er 10 prosent og dokumentavgiften i Andalucía 1,20 prosent, vanlige satser som dokumentene ikke oppgir; boligen til {E590000} koster derfor rundt {E656000} og boligen til {E720000} rundt {E801000}, før notar- og tinglysingsgebyrer.',
  'Priser och ytor är avskrivna från exploatörens prislista av 3 november 2026, som nämner tre av de 57 bostäderna och visar var och en som tillgänglig. Listan anger att IVA inte ingår och att priserna gäller i två dagar efter nedladdningen. Ytorna i listan stämmer med planritningarna. Planritningarna anger dessutom byggytan med en andel av de gemensamma ytorna: {N141.33}, {N141.34} och {N99.64} {U}. Listan kallar uppgången ett hus. Den visar en garageplats per bostad och ett förråd för 11B och 122B, men inget för 61B. IVA på en ny bostad är 10 procent och stämpelskatten i Andalusien 1,20 procent, vanliga satser som dokumenten inte anger; bostaden för {E590000} kostar därför cirka {E656000} och bostaden för {E720000} cirka {E801000}, före notarie- och registreringsavgifter.')
for i, (n, t) in enumerate([('82.53', '78.66'), ('120.34', '33.06'), ('120.35', '33.06')]):
    a(f'.availability.units[{i}].size',
      f'{{N{n}}} {{U}} construidos, {{N{t}}} {{U}} de terraza', f'{{N{n}}} {{U}} construits, {{N{t}}} {{U}} de terrasse',
      f'{{N{n}}} {{U}} bebaut, {{N{t}}} {{U}} Terrasse', f'{{N{n}}} {{U}} застройки, {{N{t}}} {{U}} терраса',
      f'{{N{n}}} {{U}} مبنية، {{N{t}}} {{U}} تراس', f'{{N{n}}} {{U}} bebouwd, {{N{t}}} {{U}} terras',
      f'{{N{n}}} {{U}} zabudowy, {{N{t}}} {{U}} tarasu', f'{{N{n}}} {{U}} bruksareal, {{N{t}}} {{U}} terrasse',
      f'{{N{n}}} {{U}} byggyta, {{N{t}}} {{U}} terrass')

# ---- payment terms, viewing, enquiry, FAQ, SEO ------------------------------------------------------------------

a('.constructionTimeline.note',
  'Ninguno de los documentos indica inicio de obra ni fecha de entrega. El último pago, el 60 por ciento más IVA, vence en la entrega de llaves. Nueva Living pide la fecha de entrega por escrito y la incorpora al contrato.',
  'Aucun des documents n’indique de début de travaux ni de date de livraison. Le dernier paiement, 60 pour cent plus TVA, est exigible à l’achèvement et à la remise des clés. Nueva Living demande la date de livraison par écrit et la fait figurer au contrat.',
  'Keines der Dokumente nennt einen Baubeginn oder einen Fertigstellungstermin. Die letzte Zahlung, 60 Prozent zuzüglich MwSt., wird bei Fertigstellung und Schlüsselübergabe fällig. Nueva Living verlangt den Übergabetermin schriftlich und nimmt ihn in den Vertrag auf.',
  'Ни в одном из документов нет начала строительства или срока сдачи. Последний платёж, 60 процентов плюс НДС, подлежит оплате при завершении строительства и передаче ключей. Nueva Living запрашивает срок сдачи в письменном виде и вносит его в договор.',
  'لا تذكر أيٌّ من الوثائق بدء الأعمال ولا موعد إنجاز. الدفعة الأخيرة، 60 بالمئة زائد ضريبة القيمة المضافة، تُستحق عند الإنجاز وتسليم المفاتيح. تطلب Nueva Living موعد التسليم كتابةً وتدرجه في العقد.',
  'Geen van de documenten noemt een start van de bouw of een opleveringsdatum. De laatste betaling, 60 procent plus btw, is verschuldigd bij oplevering en sleuteloverdracht. Nueva Living vraagt de opleveringsdatum schriftelijk en neemt die op in het contract.',
  'Żaden z dokumentów nie podaje rozpoczęcia budowy ani terminu oddania. Ostatnia płatność, 60 procent plus VAT, staje się wymagalna przy zakończeniu budowy i przekazaniu kluczy. Nueva Living prosi o termin oddania na piśmie i wpisuje go do umowy.',
  'Ingen av dokumentene oppgir byggestart eller overleveringsdato. Den siste betalingen, 60 prosent pluss mva, forfaller ved ferdigstillelse og overlevering av nøklene. Nueva Living ber om overleveringsdatoen skriftlig og tar den inn i kontrakten.',
  'Inget av dokumenten anger byggstart eller tillträdesdatum. Den sista betalningen, 60 procent plus IVA, förfaller vid färdigställande och nyckelöverlämning. Nueva Living ber om tillträdesdatumet skriftligt och tar in det i avtalet.')
a('.constructionTimeline.paymentTerms[0][2]',
  '22.000 € con IVA incluido', '22 000 € TVA incluse', '22.000 € inklusive MwSt.', '22 000 € с учётом НДС', '22,000 € شاملة ضريبة القيمة المضافة',
  '€ 22.000 inclusief btw', '22 000 € z VAT', '22 000 € inkludert mva', '22 000 € inklusive IVA')
a('.constructionTimeline.paymentTerms[2][0]',
  'A los 6 meses', 'Au bout de 6 mois', 'Nach 6 Monaten', 'Через 6 месяцев', 'بعد 6 أشهر', 'Na 6 maanden', 'Po 6 miesiącach', 'Etter 6 måneder', 'Efter 6 månader')
a('.constructionTimeline.paymentTerms[4][2]',
  'Escritura pública, a la finalización y entrega de llaves', 'Acte authentique, à l’achèvement et à la remise des clés',
  'Notarieller Kaufvertrag, bei Fertigstellung und Schlüsselübergabe', 'Нотариальный акт, при завершении строительства и передаче ключей',
  'سند الملكية، عند الإنجاز وتسليم المفاتيح', 'Notariële akte, bij oplevering en sleuteloverdracht',
  'Akt notarialny, przy zakończeniu budowy i przekazaniu kluczy', 'Skjøte, ved ferdigstillelse og overlevering av nøklene',
  'Notariell köpehandling, vid färdigställande och nyckelöverlämning')
a('.constructionTimeline.paymentTermsNote',
  'El 60 por ciento final vence solo en la finalización y entrega de llaves. Los dos plazos intermedios corren desde el contrato privado, no según hitos de obra. Los documentos no dicen si los plazos devengan intereses ni cómo se garantizan los pagos a cuenta; Nueva Living confirma ambas cosas en el contrato de reserva antes de que usted se comprometa.',
  'Les 60 pour cent finaux ne sont exigibles qu’à l’achèvement et à la remise des clés. Les deux échéances intermédiaires courent à partir du contrat privé, non d’étapes de chantier. Les documents ne disent pas si les échéances portent intérêt ni comment les sommes versées d’avance sont garanties ; Nueva Living confirme les deux dans le contrat de réservation avant que vous ne vous engagiez.',
  'Die letzten 60 Prozent werden erst bei Fertigstellung und Schlüsselübergabe fällig. Die beiden mittleren Raten laufen ab dem privaten Kaufvertrag, nicht ab Bauabschnitten. Die Dokumente sagen nicht, ob die Raten verzinst werden oder wie Anzahlungen abgesichert sind; Nueva Living bestätigt beides im Reservierungsvertrag, bevor Sie sich verpflichten.',
  'Последние 60 процентов подлежат оплате только при завершении строительства и передаче ключей. Два промежуточных платежа отсчитываются от частного договора, а не от этапов строительства. В документах не сказано, начисляются ли на платежи проценты и как обеспечены внесённые суммы; Nueva Living подтверждает и то и другое в договоре бронирования до того, как вы примете обязательство.',
  'لا يُستحق الـ60 بالمئة الأخيرة إلا عند الإنجاز وتسليم المفاتيح. القسطان الأوسطان يُحتسبان من العقد الخاص لا من مراحل البناء. لا تقول الوثائق هل تترتب فوائد على الأقساط ولا كيف تُضمن المبالغ المدفوعة على الحساب؛ وتؤكد Nueva Living الأمرين في عقد الحجز قبل أن تلتزموا.',
  'De laatste 60 procent is pas verschuldigd bij oplevering en sleuteloverdracht. De twee tussentijdse termijnen lopen vanaf het onderhandse contract, niet vanaf bouwfasen. De documenten zeggen niet of de termijnen rente dragen of hoe voorschotten zijn gedekt; Nueva Living bevestigt beide in de reserveringsovereenkomst voordat u zich verbindt.',
  'Ostatnie 60 procent staje się wymagalne dopiero przy zakończeniu budowy i przekazaniu kluczy. Dwie środkowe raty liczy się od umowy przedwstępnej, a nie od etapów budowy. Dokumenty nie mówią, czy raty są oprocentowane ani jak zabezpieczone są wpłaty na poczet ceny; Nueva Living potwierdza jedno i drugie w umowie rezerwacyjnej, zanim Państwo się zobowiążą.',
  'De siste 60 prosentene forfaller først ved ferdigstillelse og overlevering av nøklene. De to midtre avdragene løper fra den private kontrakten, ikke fra byggetrinn. Dokumentene sier ikke om avdragene medfører renter eller hvordan innbetalte beløp er sikret; Nueva Living bekrefter begge deler i reservasjonsavtalen før De forplikter Dem.',
  'De sista 60 procenten förfaller först vid färdigställande och nyckelöverlämning. De två mellersta delbetalningarna löper från det privata avtalet, inte från byggetapper. Dokumenten säger inte om delbetalningarna bär ränta eller hur inbetalda belopp är säkrade; Nueva Living bekräftar båda delarna i bokningsavtalet innan ni förbinder er.')
a('.privateViewing.insights[0][0]',
  'Qué viviendas quedan', 'Quels logements restent', 'Welche Wohnungen noch frei sind', 'Какие квартиры остались', 'أي المساكن ما زالت متاحة',
  'Welke woningen nog beschikbaar zijn', 'Które mieszkania zostały', 'Hvilke boliger som gjenstår', 'Vilka bostäder som återstår')
a('.privateViewing.insights[0][1]',
  'La lista completa de las 57 viviendas y cuáles están vendidas o reservadas.',
  'La liste complète des 57 logements et lesquels sont vendus ou réservés.',
  'Die vollständige Liste der 57 Wohnungen und welche davon verkauft oder reserviert sind.',
  'Полный список из 57 квартир и сведения о том, какие из них проданы или забронированы.',
  'القائمة الكاملة للمساكن الـ57 وأيّها مباع أو محجوز.',
  'De volledige lijst van de 57 woningen en welke daarvan verkocht of gereserveerd zijn.',
  'Pełna lista 57 mieszkań i informacja, które z nich są sprzedane lub zarezerwowane.',
  'Den fullstendige listen over de 57 boligene og hvilke av dem som er solgt eller reservert.',
  'Den fullständiga listan över de 57 bostäderna och vilka av dem som är sålda eller reserverade.')
a('.privateViewing.insights[1][0]',
  'Hasta dónde han llegado la obra', 'Où en sont les travaux', 'Wie weit die Arbeiten sind', 'Как далеко продвинулись работы', 'إلى أي مرحلة وصلت الأعمال',
  'Hoe ver de werken zijn', 'Jak daleko zaszły roboty', 'Hvor langt arbeidene har kommet', 'Hur långt arbetena har kommit')
a('.privateViewing.insights[1][1]',
  'La fase de las obras, que los documentos que tenemos no indican.',
  'L’état d’avancement des travaux, que les documents en notre possession n’indiquent pas.',
  'Der Stand der Arbeiten, den die uns vorliegenden Dokumente nicht nennen.',
  'Стадия работ, о которой в имеющихся у нас документах ничего не сказано.',
  'مرحلة الأعمال، التي لا تذكرها الوثائق التي بحوزتنا.',
  'De stand van de werken, die de documenten die we hebben niet vermelden.',
  'Etap robót, którego nie podają dokumenty, którymi dysponujemy.',
  'Byggetrinnet, som dokumentene vi har ikke oppgir.',
  'Byggskedet, som dokumenten vi har inte anger.')
a('.enquiry.message',
  'Me gustaría conocer la disponibilidad y los precios actuales de Monteros Garden Residences.',
  'Je souhaiterais connaître la disponibilité et les prix actuels de Monteros Garden Residences.',
  'Ich möchte die aktuelle Verfügbarkeit und die Preise für Monteros Garden Residences erfahren.',
  'Я хотел бы узнать актуальное наличие и цены по Monteros Garden Residences.',
  'أود معرفة التوفر والأسعار الحالية لـ Monteros Garden Residences.',
  'Ik wil graag de actuele beschikbaarheid en prijzen van Monteros Garden Residences weten.',
  'Chciałbym poznać aktualną dostępność i ceny w Monteros Garden Residences.',
  'Jeg vil gjerne vite gjeldende tilgjengelighet og priser for Monteros Garden Residences.',
  'Jag vill gärna veta aktuell tillgänglighet och aktuella priser för Monteros Garden Residences.')

# ---- FAQ ------------------------------------------------------------------

a('.faq[0][1]',
  'La promoción tiene 57 viviendas de uno, dos o tres dormitorios. La lista de precios recoge tres, todas disponibles: una vivienda de dos dormitorios por {E590000} y viviendas de tres dormitorios por {E685000} y {E720000}, más IVA.',
  'Le programme compte 57 logements d’une, deux ou trois chambres. La liste de prix en nomme trois, toutes disponibles : un logement de deux chambres à {E590000} et des logements de trois chambres à {E685000} et {E720000}, plus TVA.',
  'Die Anlage hat 57 Wohnungen mit einem, zwei oder drei Schlafzimmern. Die Preisliste nennt drei davon, alle verfügbar: eine Wohnung mit zwei Schlafzimmern für {E590000} und Wohnungen mit drei Schlafzimmern für {E685000} und {E720000}, zuzüglich MwSt.',
  'В комплексе 57 квартир с одной, двумя или тремя спальнями. В прайс-листе названы три, все доступны: квартира с двумя спальнями за {E590000} и квартиры с тремя спальнями за {E685000} и {E720000}, плюс НДС.',
  'يضم المشروع 57 مسكنًا بغرفة أو غرفتين أو ثلاث غرف نوم. تذكر قائمة الأسعار ثلاثة منها، كلها متاحة: مسكن بغرفتي نوم بسعر {E590000} ومسكنان بثلاث غرف نوم بسعر {E685000} و{E720000}، زائد ضريبة القيمة المضافة.',
  'Het complex heeft 57 woningen met een, twee of drie slaapkamers. De prijslijst noemt er drie, alle beschikbaar: een woning met twee slaapkamers voor {E590000} en woningen met drie slaapkamers voor {E685000} en {E720000}, plus btw.',
  'Inwestycja ma 57 mieszkań z jedną, dwiema lub trzema sypialniami. Cennik wymienia trzy z nich, wszystkie dostępne: mieszkanie z dwiema sypialniami za {E590000} oraz mieszkania z trzema sypialniami za {E685000} i {E720000}, plus VAT.',
  'Anlegget har 57 boliger med ett, to eller tre soverom. Prislisten nevner tre av dem, alle tilgjengelige: en bolig med to soverom til {E590000} og boliger med tre soverom til {E685000} og {E720000}, pluss mva.',
  'Området har 57 bostäder med ett, två eller tre sovrum. Prislistan nämner tre av dem, alla tillgängliga: en bostad med två sovrum för {E590000} och bostäder med tre sovrum för {E685000} och {E720000}, plus IVA.')
a('.faq[1][1]',
  'No. La lista de precios indica que el IVA no está incluido. El IVA de una vivienda nueva es del 10 por ciento y el impuesto de actos jurídicos documentados en Andalucía del 1,20 por ciento, tipos habituales que los documentos no indican.',
  'Non. La liste de prix précise que la TVA n’est pas incluse. La TVA sur un logement neuf est de 10 pour cent et le droit de timbre en Andalousie de 1,20 pour cent, des taux usuels que les documents n’indiquent pas.',
  'Nein. Die Preisliste besagt, dass die MwSt. nicht enthalten ist. Die MwSt. beträgt bei einer Neubauwohnung 10 Prozent und die Stempelsteuer in Andalusien 1,20 Prozent, übliche Sätze, die die Dokumente nicht nennen.',
  'Нет. В прайс-листе сказано, что НДС не включён. НДС на новое жильё составляет 10 процентов, гербовый сбор в Андалусии — 1,20 процента; это обычные ставки, в документах они не указаны.',
  'لا. تذكر قائمة الأسعار أن ضريبة القيمة المضافة غير مشمولة. ضريبة القيمة المضافة على المسكن الجديد 10 بالمئة ورسم الدمغة في الأندلس 1.20 بالمئة، وهما نسبتان معتادتان لا تذكرهما الوثائق.',
  'Nee. De prijslijst vermeldt dat btw niet is inbegrepen. Btw op een nieuwbouwwoning is 10 procent en overdrachtsbelasting in Andalusië 1,20 procent, gangbare tarieven die de documenten niet noemen.',
  'Nie. Cennik podaje, że VAT nie jest wliczony. VAT na nowe mieszkanie wynosi 10 procent, a podatek od czynności cywilnoprawnych w Andaluzji 1,20 procent; są to standardowe stawki, których dokumenty nie podają.',
  'Nei. Prislisten oppgir at mva. ikke er inkludert. Mva. på en ny bolig er 10 prosent og dokumentavgiften i Andalucía 1,20 prosent, vanlige satser som dokumentene ikke oppgir.',
  'Nej. Prislistan anger att IVA inte ingår. IVA på en ny bostad är 10 procent och stämpelskatten i Andalusien 1,20 procent, vanliga satser som dokumenten inte anger.')
a('.faq[2][1]',
  'La lista de precios muestra una plaza de garaje con cada una de las tres viviendas y un trastero con dos de ellas, la 11B y la 122B. Confirmamos que están incluidos en el precio.',
  'La liste de prix indique une place de garage avec chacun des trois logements et une cave avec deux d’entre eux, le 11B et le 122B. Nous confirmons qu’elles sont incluses dans le prix.',
  'Die Preisliste zeigt zu jeder der drei Wohnungen einen Garagenstellplatz und bei zweien davon, 11B und 122B, einen Abstellraum. Wir bestätigen, dass sie im Preis enthalten sind.',
  'В прайс-листе у каждой из трёх квартир указано место в гараже, а у двух из них, 11B и 122B, — кладовая. Мы подтверждаем, что они включены в цену.',
  'تُظهر قائمة الأسعار موقف سيارات في المرآب مع كل من المساكن الثلاثة وغرفة تخزين مع اثنين منها، 11B و122B. نؤكد أنها مشمولة في السعر.',
  'De prijslijst toont bij elk van de drie woningen een garageplaats en bij twee ervan, 11B en 122B, een berging. We bevestigen dat ze in de prijs zijn inbegrepen.',
  'Cennik pokazuje przy każdym z trzech mieszkań miejsce w garażu, a przy dwóch z nich, 11B i 122B, komórkę lokatorską. Potwierdzamy, że są wliczone w cenę.',
  'Prislisten viser en garasjeplass til hver av de tre boligene og en bod til to av dem, 11B og 122B. Vi bekrefter at de er inkludert i prisen.',
  'Prislistan visar en garageplats till var och en av de tre bostäderna och ett förråd till två av dem, 11B och 122B. Vi bekräftar att de ingår i priset.')
a('.faq[3][1]',
  'Ninguno de los documentos indica fecha de entrega, estado de la licencia ni fase de las obras. Pedimos la licencia y la fecha contractual.',
  'Aucun des documents n’indique de date de livraison, de statut du permis ni de phase des travaux. Nous demandons le permis et la date contractuelle.',
  'Kein Dokument nennt einen Fertigstellungstermin, den Stand der Baugenehmigung oder einen Baufortschritt. Wir fragen nach der Genehmigung und dem vertraglichen Termin.',
  'Ни в одном документе нет срока сдачи, статуса разрешения или стадии работ. Мы запрашиваем разрешение и договорный срок.',
  'لا تذكر أيٌّ من الوثائق موعد إنجاز أو وضع الرخصة أو مرحلة الأعمال. نطلب الرخصة والموعد التعاقدي.',
  'Geen enkel document noemt een opleveringsdatum, de status van de vergunning of een bouwfase. We vragen om de vergunning en de contractuele datum.',
  'Żaden dokument nie podaje terminu oddania, statusu pozwolenia ani etapu robót. Prosimy o pozwolenie i termin umowny.',
  'Ingen dokumenter oppgir en overleveringsdato, byggetillatelsens status eller byggetrinn. Vi ber om byggetillatelsen og den kontraktfestede datoen.',
  'Inget dokument anger något tillträdesdatum, bygglovets status eller byggskede. Vi ber om bygglovet och det avtalade datumet.')
a('.faq[4][1]',
  '20.000 € más IVA al reservar, el 20 por ciento más IVA en el contrato privado 60 días después, menos la reserva, el 10 por ciento a los seis meses y el 10 por ciento a los doce meses del contrato privado, y el 60 por ciento más IVA en la finalización y entrega de llaves.',
  '20 000 € plus TVA à la réservation, 20 pour cent plus TVA au contrat privé 60 jours plus tard, moins la réservation, 10 pour cent à six mois et 10 pour cent à douze mois après le contrat privé, et 60 pour cent plus TVA à l’achèvement et à la remise des clés.',
  '20.000 € zuzüglich MwSt. bei der Reservierung, 20 Prozent zuzüglich MwSt. beim privaten Kaufvertrag 60 Tage später, abzüglich der Reservierung, 10 Prozent nach sechs Monaten und 10 Prozent nach zwölf Monaten ab dem privaten Kaufvertrag sowie 60 Prozent zuzüglich MwSt. bei Fertigstellung und Schlüsselübergabe.',
  '20 000 € плюс НДС при бронировании, 20 процентов плюс НДС по частному договору через 60 дней, за вычетом брони, 10 процентов через шесть месяцев и 10 процентов через двенадцать месяцев после частного договора и 60 процентов плюс НДС при завершении строительства и передаче ключей.',
  '20,000 € زائد ضريبة القيمة المضافة عند الحجز، و20 بالمئة زائد ضريبة القيمة المضافة عند العقد الخاص بعد 60 يومًا، مخصومًا منها مبلغ الحجز، و10 بالمئة بعد ستة أشهر و10 بالمئة بعد اثني عشر شهرًا من العقد الخاص، و60 بالمئة زائد ضريبة القيمة المضافة عند الإنجاز وتسليم المفاتيح.',
  '€ 20.000 plus btw bij reservering, 20 procent plus btw bij het onderhandse contract 60 dagen later, min de reservering, 10 procent na zes maanden en 10 procent na twaalf maanden na het onderhandse contract, en 60 procent plus btw bij oplevering en sleuteloverdracht.',
  '20 000 € plus VAT przy rezerwacji, 20 procent plus VAT przy umowie przedwstępnej 60 dni później, pomniejszone o rezerwację, 10 procent po sześciu miesiącach i 10 procent po dwunastu miesiącach od umowy przedwstępnej oraz 60 procent plus VAT przy zakończeniu budowy i przekazaniu kluczy.',
  '20 000 € pluss mva ved reservasjon, 20 prosent pluss mva ved den private kontrakten 60 dager senere, minus reservasjonen, 10 prosent etter seks måneder og 10 prosent etter tolv måneder fra den private kontrakten, og 60 prosent pluss mva ved ferdigstillelse og overlevering av nøklene.',
  '20 000 € plus IVA vid bokning, 20 procent plus IVA vid det privata avtalet 60 dagar senare, minus bokningen, 10 procent efter sex månader och 10 procent efter tolv månader från det privata avtalet, och 60 procent plus IVA vid färdigställande och nyckelöverlämning.')
a('.faq[5][1]',
  'Piscinas, una piscina interior climatizada, un gimnasio, un espacio de coworking y un salón social, en un complejo cerrado con conserje, control de accesos y videovigilancia las 24 horas.',
  'Des piscines, une piscine intérieure chauffée, une salle de sport, un espace de coworking et un salon du club, dans une résidence fermée avec concierge, contrôle d’accès et vidéosurveillance 24 h/24.',
  'Pools, ein beheizter Innenpool, ein Fitnessraum, ein Coworking-Bereich und eine Club-Lounge, in einer geschlossenen Anlage mit Concierge, Zugangskontrolle und 24-Stunden-Videoüberwachung.',
  'Бассейны, крытый подогреваемый бассейн, тренажёрный зал, коворкинг и клубный лаундж в закрытом комплексе с консьержем, контролем доступа и круглосуточным видеонаблюдением.',
  'مسابح ومسبح داخلي مُدفأ وصالة رياضية ومساحة عمل مشتركة وصالة اجتماعية، في مجمّع مغلق فيه كونسيرج وتحكم بالدخول ومراقبة بالفيديو على مدار الساعة.',
  'Zwembaden, een verwarmd binnenzwembad, een fitnessruimte, een coworkingruimte en een clublounge, in een besloten complex met conciërge, toegangscontrole en 24 uur per dag videobewaking.',
  'Baseny, podgrzewany basen wewnętrzny, siłownia, przestrzeń coworkingowa i salon klubowy, w zamkniętym kompleksie z konsjerżem, kontrolą dostępu i całodobowym monitoringiem wideo.',
  'Basseng, et oppvarmet innendørsbasseng, et treningsrom, et coworkingområde og en klubblounge, i et bevoktet anlegg med concierge, adgangskontroll og døgnåpen videoovervåking.',
  'Pooler, en uppvärmd inomhuspool, ett gym, en coworkingyta och en klubblounge, i ett bevakat område med concierge, passerkontroll och dygnet-runt-videoövervakning.')
a('.faq[6][1]',
  'La lista de precios indica que sus precios son válidos durante dos días desde su descarga, así que reconfirmamos la cifra con el vendedor antes de que usted se comprometa a nada.',
  'La liste de prix indique que ses prix sont valables deux jours après son téléchargement ; nous reconfirmons donc le chiffre auprès du vendeur avant que vous ne vous engagiez.',
  'Die Preisliste gibt an, dass ihre Preise nach dem Herunterladen zwei Tage lang gültig sind, daher bestätigen wir die Zahl beim Verkäufer erneut, bevor Sie sich auf etwas festlegen.',
  'В прайс-листе сказано, что цены действительны в течение двух дней после его загрузки, поэтому мы повторно подтверждаем цифру у продавца до того, как вы на что-либо согласитесь.',
  'تذكر قائمة الأسعار أن أسعارها صالحة لمدة يومين بعد تنزيلها، لذلك نعيد تأكيد الرقم مع البائع قبل أن تلتزموا بأي شيء.',
  'De prijslijst geeft aan dat haar prijzen twee dagen na het downloaden geldig zijn, dus we bevestigen het bedrag opnieuw bij de verkoper voordat u zich aan iets verbindt.',
  'Cennik podaje, że jego ceny są ważne przez dwa dni od pobrania, dlatego ponownie potwierdzamy kwotę u sprzedawcy, zanim Państwo się do czegokolwiek zobowiążą.',
  'Prislisten oppgir at prisene er gyldige i to dager etter at den er lastet ned, så vi bekrefter beløpet på nytt med selgeren før De forplikter Dem til noe.',
  'Prislistan anger att priserna gäller i två dagar efter nedladdningen, så vi bekräftar beloppet med säljaren på nytt innan ni förbinder er till något.')

# ---- SEO ------------------------------------------------------------------

a('.seo.title',
  'Monteros Garden Residences - Apartamentos en Marbella', 'Monteros Garden Residences - Appartements à Marbella',
  'Monteros Garden Residences - Wohnungen in Marbella', 'Monteros Garden Residences - апартаменты в Марбелье',
  'Monteros Garden Residences - شقق في ماربيا', 'Monteros Garden Residences - Appartementen in Marbella',
  'Monteros Garden Residences - apartamenty w Marbelli', 'Monteros Garden Residences - Leiligheter i Marbella',
  'Monteros Garden Residences - Lägenheter i Marbella')
a('.seo.description',
  'Apartamentos de dos y tres dormitorios con grandes terrazas en Altos de los Monteros, Marbella: 3 de 57 viviendas disponibles desde {E590000} más IVA.',
  'Appartements de deux et trois chambres avec grandes terrasses à Altos de los Monteros, Marbella : 3 logements sur 57 disponibles à partir de {E590000} plus TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern und großen Terrassen in Altos de los Monteros, Marbella: 3 von 57 Wohnungen verfügbar ab {E590000} zuzüglich MwSt.',
  'Апартаменты с двумя и тремя спальнями и большими террасами в Альтос-де-лос-Монтерос, Марбелья: доступны 3 из 57 квартир от {E590000} плюс НДС.',
  'شقق بغرفتي نوم وثلاث غرف نوم مع تراسات واسعة في ألتوس دي لوس مونتيروس، ماربيا: 3 من 57 مسكنًا متاحة ابتداءً من {E590000} زائد ضريبة القيمة المضافة.',
  'Appartementen met twee en drie slaapkamers en grote terrassen in Altos de los Monteros, Marbella: 3 van de 57 woningen beschikbaar vanaf {E590000} plus btw.',
  'Apartamenty z dwiema i trzema sypialniami oraz dużymi tarasami w Altos de los Monteros, Marbella: dostępne 3 z 57 mieszkań od {E590000} plus VAT.',
  'Leiligheter med to og tre soverom og store terrasser i Altos de los Monteros, Marbella: 3 av 57 boliger tilgjengelige fra {E590000} pluss mva.',
  'Lägenheter med två och tre sovrum och stora terrasser i Altos de los Monteros, Marbella: 3 av 57 bostäder tillgängliga från {E590000} plus IVA.')
a('.seo.h1',
  'Monteros Garden Residences: 3 de 57 viviendas disponibles, Marbella', 'Monteros Garden Residences : 3 logements disponibles sur 57, Marbella',
  'Monteros Garden Residences: 3 von 57 Wohnungen verfügbar, Marbella', 'Monteros Garden Residences: доступны 3 из 57 квартир, Марбелья',
  'Monteros Garden Residences: 3 من 57 مسكنًا متاحة، ماربيا', 'Monteros Garden Residences: 3 van de 57 woningen beschikbaar, Marbella',
  'Monteros Garden Residences: dostępne 3 z 57 mieszkań, Marbella', 'Monteros Garden Residences: 3 av 57 boliger tilgjengelige, Marbella',
  'Monteros Garden Residences: 3 av 57 bostäder tillgängliga, Marbella')
a('.seo.h1Context',
  '3 de 57 viviendas disponibles, Marbella', '3 logements disponibles sur 57, Marbella', '3 von 57 Wohnungen verfügbar, Marbella',
  'Доступны 3 из 57 квартир, Марбелья', '3 من 57 مسكنًا متاحة، ماربيا', '3 van de 57 woningen beschikbaar, Marbella',
  'Dostępne 3 z 57 mieszkań, Marbella', '3 av 57 boliger tilgjengelige, Marbella', '3 av 57 bostäder tillgängliga, Marbella')

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings to', f'{SP}/tr_a.json')
