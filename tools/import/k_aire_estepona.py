# -*- coding: utf-8 -*-
"""Aire Estepona: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E492000}
money, {N88.4} decimal number, {U} the area unit.
    python3 tools/import/k_aire_estepona.py <scratch dir>      (writes <dir>/tr_a.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/aire-estepona/project.json'))
tm = json.load(open(f'{SP}/tm.json'))


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


same('Aire Estepona'); same('Aire <em>Estepona</em>')
for u in proj['availability']['units']:
    same(u['reference'])

# ---- description, SEO, card ------------------------------------------------------------------

a('.description',
  '3 de las 57 viviendas de dos y tres dormitorios de Aire Estepona, en Cancelada, en la Nueva Milla de Oro de Estepona, figuran como disponibles: una vivienda de dos dormitorios con jardín por {E492000} y viviendas de tres dormitorios por {E487500} y {E922000}. Cada una incluye una plaza de garaje y un trastero. No se indica fecha de entrega.',
  '3 des 57 logements de deux et trois chambres d’Aire Estepona, à Cancelada, sur la Nouvelle Mille d’Or d’Estepona, sont indiqués comme disponibles : un logement de deux chambres avec jardin à {E492000} et des logements de trois chambres à {E487500} et {E922000}. Chacun comprend une place de garage et une cave. Aucune date de livraison n’est indiquée.',
  '3 der 57 Wohnungen mit zwei und drei Schlafzimmern in Aire Estepona, in Cancelada an der Neuen Goldenen Meile von Estepona, sind als verfügbar aufgeführt: eine Wohnung mit zwei Schlafzimmern und Garten für {E492000} und Wohnungen mit drei Schlafzimmern für {E487500} und {E922000}. Jede hat einen Garagenstellplatz und einen Abstellraum. Ein Fertigstellungstermin ist nicht angegeben.',
  '3 из 57 квартир с двумя и тремя спальнями в Aire Estepona, в Канселаде на Новой Золотой миле Эстепоны, указаны в списке как доступные: квартира с двумя спальнями и садом за {E492000} и квартиры с тремя спальнями за {E487500} и {E922000}. У каждой есть место в гараже и кладовая. Срок сдачи не указан.',
  '3 من أصل 57 مسكنًا بغرفتي نوم وثلاث غرف نوم في Aire Estepona، في كانسيلادا على الميل الذهبي الجديد في إستيبونا، مدرجة على أنها متاحة: مسكن بغرفتي نوم مع حديقة بسعر {E492000} ومسكنان بثلاث غرف نوم بسعر {E487500} و{E922000}. لكل منها موقف سيارات في المرآب ومخزن. لم يُذكر موعد إنجاز.',
  '3 van de 57 woningen met twee en drie slaapkamers in Aire Estepona, in Cancelada aan de Nieuwe Golden Mile van Estepona, staan als beschikbaar vermeld: een woning met twee slaapkamers en tuin voor {E492000} en woningen met drie slaapkamers voor {E487500} en {E922000}. Elke woning heeft een garageplaats en een berging. Er wordt geen opleveringsdatum genoemd.',
  '3 z 57 lokali z dwiema i trzema sypialniami w Aire Estepona, w Cancelada na Nowej Złotej Mili w Esteponie, jest podanych jako dostępne: lokal z dwiema sypialniami i ogrodem za {E492000} oraz lokale z trzema sypialniami za {E487500} i {E922000}. Każdy ma miejsce w garażu i komórkę lokatorską. Termin oddania nie jest podany.',
  '3 av de 57 boligene med to og tre soverom i Aire Estepona, i Cancelada på Nye Golden Mile i Estepona, er oppført som tilgjengelige: en bolig med to soverom og hage til {E492000} og boliger med tre soverom til {E487500} og {E922000}. Hver bolig har en garasjeplass og en bod. Ingen overleveringsdato er oppgitt.',
  '3 av de 57 bostäderna med två och tre sovrum i Aire Estepona, i Cancelada på Nya Golden Mile i Estepona, är angivna som tillgängliga: en bostad med två sovrum och trädgård för {E492000} och bostäder med tre sovrum för {E487500} och {E922000}. Varje bostad har en garageplats och ett förråd. Inget tillträdesdatum anges.')
a('.seoDescription',
  'Viviendas de dos y tres dormitorios con terrazas o jardín en Cancelada, Estepona, con piscina, gimnasio y casa club, desde {E487500}.',
  'Logements de deux et trois chambres avec terrasses ou jardin à Cancelada, Estepona, avec piscine, salle de sport et club-house, à partir de {E487500}.',
  'Wohnungen mit zwei und drei Schlafzimmern, Terrassen oder Garten in Cancelada, Estepona, mit Pool, Fitnessraum und Clubhaus, ab {E487500}.',
  'Квартиры с двумя и тремя спальнями, террасами или садом в Канселаде, Эстепона, с бассейном, спортзалом и клубным домом, от {E487500}.',
  'مساكن بغرفتي نوم وثلاث غرف نوم مع تراسات أو حديقة في كانسيلادا، إستيبونا، مع مسبح وصالة رياضية ونادي المجمع، ابتداءً من {E487500}.',
  'Woningen met twee en drie slaapkamers, terrassen of een tuin in Cancelada, Estepona, met zwembad, fitnessruimte en clubhuis, vanaf {E487500}.',
  'Lokale z dwiema i trzema sypialniami, tarasami lub ogrodem w Cancelada, Estepona, z basenem, siłownią i klubem mieszkańców, od {E487500}.',
  'Boliger med to og tre soverom, terrasser eller hage i Cancelada, Estepona, med basseng, treningsrom og klubbhus, fra {E487500}.',
  'Bostäder med två och tre sovrum, terrasser eller trädgård i Cancelada, Estepona, med pool, gym och klubbhus, från {E487500}.')
a('.twitterDescription',
  'Viviendas de dos y tres dormitorios con terrazas o jardín en Cancelada, Estepona, desde {E487500}.',
  'Logements de deux et trois chambres avec terrasses ou jardin à Cancelada, Estepona, à partir de {E487500}.',
  'Wohnungen mit zwei und drei Schlafzimmern, Terrassen oder Garten in Cancelada, Estepona, ab {E487500}.',
  'Квартиры с двумя и тремя спальнями, террасами или садом в Канселаде, Эстепона, от {E487500}.',
  'مساكن بغرفتي نوم وثلاث غرف نوم مع تراسات أو حديقة في كانسيلادا، إستيبونا، ابتداءً من {E487500}.',
  'Woningen met twee en drie slaapkamers, terrassen of een tuin in Cancelada, Estepona, vanaf {E487500}.',
  'Lokale z dwiema i trzema sypialniami, tarasami lub ogrodem w Cancelada, Estepona, od {E487500}.',
  'Boliger med to og tre soverom, terrasser eller hage i Cancelada, Estepona, fra {E487500}.',
  'Bostäder med två och tre sovrum, terrasser eller trädgård i Cancelada, Estepona, från {E487500}.')
a('.card.description',
  'Viviendas de dos y tres dormitorios con terrazas o jardín en una promoción de 57 viviendas en Cancelada, con piscina, gimnasio y casa club.',
  'Logements de deux et trois chambres avec terrasses ou jardin dans un programme de 57 logements à Cancelada, avec piscine, salle de sport et club-house.',
  'Wohnungen mit zwei und drei Schlafzimmern, Terrassen oder Garten in einer Anlage mit 57 Wohnungen in Cancelada, mit Pool, Fitnessraum und Clubhaus.',
  'Квартиры с двумя и тремя спальнями, террасами или садом в комплексе из 57 квартир в Канселаде, с бассейном, спортзалом и клубным домом.',
  'مساكن بغرفتي نوم وثلاث غرف نوم مع تراسات أو حديقة في مجمّع من 57 مسكنًا في كانسيلادا، مع مسبح وصالة رياضية ونادي المجمع.',
  'Woningen met twee en drie slaapkamers, terrassen of een tuin in een complex van 57 woningen in Cancelada, met zwembad, fitnessruimte en clubhuis.',
  'Lokale z dwiema i trzema sypialniami, tarasami lub ogrodem w inwestycji liczącej 57 lokali w Cancelada, z basenem, siłownią i klubem mieszkańców.',
  'Boliger med to og tre soverom, terrasser eller hage i et anlegg med 57 boliger i Cancelada, med basseng, treningsrom og klubbhus.',
  'Bostäder med två och tre sovrum, terrasser eller trädgård i ett område med 57 bostäder i Cancelada, med pool, gym och klubbhus.')

# ---- image alts and captions ------------------------------------------------------------------

a('.images.hero.alt',
  'Vista generada por ordenador a través de la piscina comunitaria hacia un bloque blanco con terrazas escalonadas, barandillas de cristal y tumbonas sobre el césped',
  'Vue générée par ordinateur à travers la piscine commune vers un bâtiment blanc aux terrasses en gradins, aux garde-corps en verre et aux transats sur la pelouse',
  'Computergenerierte Ansicht über den Gemeinschaftspool hinweg auf ein weißes Gebäude mit gestaffelten Terrassen, Glasbrüstungen und Sonnenliegen auf dem Rasen',
  'Компьютерная визуализация: вид через общий бассейн на белый корпус со ступенчатыми террасами, стеклянными ограждениями и шезлонгами на газоне',
  'منظر مولَّد بالحاسوب عبر المسبح المشترك نحو مبنى أبيض بتراسات متدرجة وحواجز زجاجية ومقاعد تشمّس على المرج',
  'Computergegenereerd beeld over het gemeenschappelijke zwembad naar een wit blok met trapsgewijze terrassen, glazen balustrades en ligstoelen op een gazon',
  'Wygenerowany komputerowo widok przez wspólny basen na biały budynek z tarasami schodkowymi, szklanymi balustradami i leżakami na trawniku',
  'Datagenerert bilde over fellesbassenget mot en hvit blokk med trappede terrasser, glassrekkverk og solsenger på en plen',
  'Datorgenererad vy över den gemensamma poolen mot ett vitt hus med trappstegsformade terrasser, glasräcken och solstolar på en gräsmatta')
a('.images.architecture.alt',
  'Vista generada por ordenador de un bloque blanco con terrazas escalonadas y barandillas de cristal sobre jardines de planta baja tras un seto, con un camino peatonal delante',
  'Vue générée par ordinateur d’un bâtiment blanc aux terrasses en gradins et aux garde-corps en verre au-dessus de jardins de rez-de-chaussée derrière une haie, avec un chemin piéton devant',
  'Computergenerierte Ansicht eines weißen Gebäudes mit gestaffelten Terrassen und Glasbrüstungen über Erdgeschossgärten hinter einer Hecke, davor ein Fußweg',
  'Компьютерная визуализация белого корпуса со ступенчатыми террасами и стеклянными ограждениями над садами первого этажа за живой изгородью; впереди пешеходная дорожка',
  'منظر مولَّد بالحاسوب لمبنى أبيض بتراسات متدرجة وحواجز زجاجية فوق حدائق الطابق الأرضي خلف سياج نباتي، ويظهر في المقدمة ممر للمشاة',
  'Computergegenereerd beeld van een wit blok met trapsgewijze terrassen en glazen balustrades boven tuinen op de begane grond achter een haag, met een voetpad ervoor',
  'Wygenerowany komputerowo widok białego budynku z tarasami schodkowymi i szklanymi balustradami nad ogrodami na parterze za żywopłotem, z chodnikiem z przodu',
  'Datagenerert bilde av en hvit blokk med trappede terrasser og glassrekkverk over hager i første etasje bak en hekk, med en gangvei foran',
  'Datorgenererad vy av ett vitt hus med trappstegsformade terrasser och glasräcken ovanför trädgårdar i bottenvåningen bakom en häck, med en gångväg framför')
a('.images.lifestyle.alt',
  'Salón generado por ordenador con un sofá rinconero, que se abre por una puerta corredera a una terraza cubierta con un conjunto de estar y el mar en el horizonte',
  'Séjour généré par ordinateur avec un canapé d’angle, s’ouvrant par une porte coulissante sur une terrasse couverte avec un salon de jardin et la mer à l’horizon',
  'Computergeneriertes Wohnzimmer mit Ecksofa, das sich durch eine Schiebetür auf eine überdachte Terrasse mit Loungemöbeln öffnet, mit dem Meer am Horizont',
  'Компьютерная визуализация гостиной с угловым диваном, которая через раздвижную дверь выходит на крытую террасу с лаунж-мебелью; на горизонте море',
  'غرفة معيشة مولَّدة بالحاسوب بأريكة زاوية تنفتح عبر باب منزلق على تراس مغطى بطقم جلوس، والبحر في الأفق',
  'Computergegenereerde woonkamer met een hoekbank, die via een schuifdeur uitkomt op een overdekt terras met een loungeset en de zee aan de horizon',
  'Wygenerowany komputerowo salon z narożną sofą, otwierający się przez przesuwne drzwi na zadaszony taras z zestawem wypoczynkowym i morzem na horyzoncie',
  'Datagenerert stue med en hjørnesofa som åpner seg gjennom en skyvedør mot en overbygd terrasse med en loungegruppe og havet i horisonten',
  'Datorgenererat vardagsrum med en hörnsoffa som öppnar sig genom en skjutdörr mot en täckt terrass med en loungegrupp och havet i horisonten')
a('.images.privateViewing.alt',
  'Dormitorio generado por ordenador con una cama doble, una puerta corredera de cristal a una terraza y una puerta al baño',
  'Chambre générée par ordinateur avec un lit double, une porte coulissante vitrée donnant sur une terrasse et une porte vers la salle de bain',
  'Computergeneriertes Schlafzimmer mit Doppelbett, gläserner Schiebetür zur Terrasse und einer Tür zum Bad',
  'Компьютерная визуализация спальни с двуспальной кроватью, стеклянной раздвижной дверью на террасу и дверью в ванную',
  'غرفة نوم مولَّدة بالحاسوب بسرير مزدوج وباب زجاجي منزلق يؤدي إلى تراس وباب إلى الحمام',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een glazen schuifdeur naar een terras en een deur naar de badkamer',
  'Wygenerowana komputerowo sypialnia z łóżkiem dwuosobowym, przesuwnymi szklanymi drzwiami na taras i drzwiami do łazienki',
  'Datagenerert soverom med en dobbeltseng, en skyvedør i glass til en terrasse og en dør til badet',
  'Datorgenererat sovrum med en dubbelsäng, en skjutdörr i glas till en terrass och en dörr till badrummet')
a('.media.copy',
  'Vistas generadas por ordenador de los edificios, la piscina y los interiores, y los planos de las tres viviendas de la lista de precios.',
  'Vues générées par ordinateur des bâtiments, de la piscine et des intérieurs, et plans des trois logements de la liste de prix.',
  'Computergenerierte Ansichten der Gebäude, des Pools und der Innenräume sowie die Grundrisse der drei Wohnungen auf der Preisliste.',
  'Компьютерные визуализации корпусов, бассейна и интерьеров и планировки трёх квартир из прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمباني والمسبح والتصاميم الداخلية، ومخططات المساكن الثلاثة الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van de gebouwen, het zwembad en de interieurs, en de plattegronden van de drie woningen op de prijslijst.',
  'Wizualizacje komputerowe budynków, basenu i wnętrz oraz rzuty trzech lokali z cennika.',
  'Datagenererte bilder av bygningene, bassenget og interiørene, og plantegninger for de tre boligene på prislisten.',
  'Datorgenererade bilder av byggnaderna, poolen och interiörerna, samt planritningar för de tre bostäderna på prislistan.')
a('.media.items[0].caption',
  'La piscina comunitaria y el bloque', 'La piscine commune et le bâtiment', 'Der Gemeinschaftspool und das Gebäude',
  'Общий бассейн и корпус', 'المسبح المشترك والمبنى', 'Het gemeenschappelijke zwembad en het blok',
  'Wspólny basen i budynek', 'Fellesbassenget og blokken', 'Den gemensamma poolen och huset')
a('.media.items[1].alt',
  'Vista generada por ordenador, al atardecer, de edificios blancos con terrazas escalonadas junto a la piscina comunitaria, con la costa en el horizonte',
  'Vue générée par ordinateur au coucher du soleil de bâtiments blancs aux terrasses en gradins près de la piscine commune, avec la côte à l’horizon',
  'Computergenerierte Ansicht bei Sonnenuntergang auf weiße Gebäude mit gestaffelten Terrassen neben dem Gemeinschaftspool, mit der Küste am Horizont',
  'Компьютерная визуализация на закате: белые здания со ступенчатыми террасами рядом с общим бассейном, на горизонте побережье',
  'منظر مولَّد بالحاسوب عند الغروب لمبانٍ بيضاء بتراسات متدرجة بجوار المسبح المشترك، والساحل في الأفق',
  'Computergegenereerd beeld bij zonsondergang van witte gebouwen met trapsgewijze terrassen naast het gemeenschappelijke zwembad, met de kust aan de horizon',
  'Wygenerowany komputerowo widok o zachodzie słońca na białe budynki z tarasami schodkowymi przy wspólnym basenie, z wybrzeżem na horyzoncie',
  'Datagenerert bilde ved solnedgang av hvite bygninger med trappede terrasser ved fellesbassenget, med kysten i horisonten',
  'Datorgenererad vy vid solnedgången av vita byggnader med trappstegsformade terrasser vid den gemensamma poolen, med kusten i horisonten')
a('.media.items[1].caption',
  'Los edificios y la piscina al atardecer', 'Les bâtiments et la piscine au coucher du soleil', 'Die Gebäude und der Pool bei Sonnenuntergang',
  'Корпуса и бассейн на закате', 'المباني والمسبح عند الغروب', 'De gebouwen en het zwembad bij zonsondergang',
  'Budynki i basen o zachodzie słońca', 'Bygningene og bassenget ved solnedgang', 'Byggnaderna och poolen vid solnedgången')
a('.media.items[2].caption',
  'El bloque sobre los jardines de planta baja', 'Le bâtiment au-dessus des jardins de rez-de-chaussée', 'Das Gebäude über den Erdgeschossgärten',
  'Корпус над садами первого этажа', 'المبنى فوق حدائق الطابق الأرضي', 'Het blok boven de tuinen op de begane grond',
  'Budynek nad ogrodami na parterze', 'Blokken over hagene i første etasje', 'Huset ovanför trädgårdarna i bottenvåningen')
a('.media.items[3].caption',
  'Salón y terraza cubierta', 'Séjour et terrasse couverte', 'Wohnzimmer und überdachte Terrasse',
  'Гостиная и крытая терраса', 'غرفة المعيشة والتراس المغطى', 'Woonkamer en overdekt terras',
  'Salon i zadaszony taras', 'Stue og overbygd terrasse', 'Vardagsrum och täckt terrass')
a('.media.items[4].alt',
  'Salón de planta abierta generado por ordenador con un sofá rinconero y una pared de televisión revestida de madera, y la cocina y la mesa de comedor al fondo',
  'Séjour ouvert généré par ordinateur avec un canapé d’angle et un mur télé habillé de bois, avec la cuisine et la table à manger au fond',
  'Computergeneriertes offenes Wohnzimmer mit Ecksofa und einer holzvertäfelten Fernsehwand, dahinter die Küche und der Esstisch',
  'Компьютерная визуализация гостиной открытой планировки с угловым диваном и стеной для телевизора с деревянной отделкой; позади кухня и обеденный стол',
  'غرفة معيشة مفتوحة مولَّدة بالحاسوب بأريكة زاوية وجدار للتلفزيون مكسو بالخشب، ومن خلفها المطبخ وطاولة الطعام',
  'Computergegenereerde open woonkamer met een hoekbank en een met hout bekleedde tv-wand, met de keuken en de eettafel erachter',
  'Wygenerowany komputerowo otwarty salon z narożną sofą i ścianą telewizyjną wykończoną drewnem, z kuchnią i stołem jadalnianym w głębi',
  'Datagenerert åpen stue med en hjørnesofa og en TV-vegg kledd med tre, med kjøkkenet og spisebordet bak',
  'Datorgenererat öppet vardagsrum med en hörnsoffa och en tv-vägg i trä, med köket och matbordet bakom')
a('.media.items[5].alt',
  'Salón generado por ordenador con una gran puerta corredera de cristal a una terraza y vistas a las montañas',
  'Séjour généré par ordinateur avec une grande porte coulissante vitrée donnant sur une terrasse et une vue sur les montagnes',
  'Computergeneriertes Wohnzimmer mit einer großen gläsernen Schiebetür zur Terrasse und Blick auf die Berge',
  'Компьютерная визуализация гостиной с большой стеклянной раздвижной дверью на террасу и видом на горы',
  'غرفة معيشة مولَّدة بالحاسوب بباب زجاجي منزلق كبير يؤدي إلى تراس وإطلالة على الجبال',
  'Computergegenereerde woonkamer met een grote glazen schuifdeur naar een terras en uitzicht op de bergen',
  'Wygenerowany komputerowo salon z dużymi przesuwnymi szklanymi drzwiami na taras i widokiem na góry',
  'Datagenerert stue med en stor skyvedør i glass til en terrasse og utsikt mot fjellene',
  'Datorgenererat vardagsrum med en stor skjutdörr i glas till en terrass och utsikt över bergen')
a('.media.items[5].caption',
  'Salón con vistas a las montañas', 'Séjour avec vue sur les montagnes', 'Wohnzimmer mit Blick auf die Berge',
  'Гостиная с видом на горы', 'غرفة معيشة بإطلالة على الجبال', 'Woonkamer met uitzicht op de bergen',
  'Salon z widokiem na góry', 'Stue med utsikt mot fjellene', 'Vardagsrum med utsikt över bergen')
a('.media.items[6].alt',
  'Cocina generada por ordenador con muebles blancos y de roble y una mesa de comedor con sillas tapizadas',
  'Cuisine générée par ordinateur avec des meubles blancs et en chêne et une table à manger avec des chaises rembourrées',
  'Computergenerierte Küche mit weißen und eichenfarbenen Schränken und einem Esstisch mit gepolsterten Stühlen',
  'Компьютерная визуализация кухни с белыми и дубовыми шкафами и обеденным столом с мягкими стульями',
  'مطبخ مولَّد بالحاسوب بخزائن بيضاء وأخرى من خشب البلوط وطاولة طعام بكراسٍ منجّدة',
  'Computergegenereerde keuken met witte en eikenhouten kastjes en een eettafel met gestoffeerde stoelen',
  'Wygenerowana komputerowo kuchnia z białymi i dębowymi szafkami oraz stołem jadalnianym z tapicerowanymi krzesłami',
  'Datagenerert kjøkken med hvite og eikefargede skap og et spisebord med stoppede stoler',
  'Datorgenererat kök med vita och ekfärgade skåp och ett matbord med stoppade stolar')
a('.media.items[6].caption',
  'Cocina y mesa de comedor', 'Cuisine et table à manger', 'Küche und Esstisch',
  'Кухня и обеденный стол', 'المطبخ وطاولة الطعام', 'Keuken en eettafel',
  'Kuchnia i stół jadalniany', 'Kjøkken og spisebord', 'Kök och matbord')
a('.media.items[8].alt',
  'Baño generado por ordenador con una ducha a ras de suelo, un lavabo suspendido con espejo y un inodoro',
  'Salle de bain générée par ordinateur avec une douche à l’italienne, un lavabo suspendu avec miroir et des toilettes',
  'Computergeneriertes Bad mit begehbarer Dusche, Wandwaschbecken mit Spiegel und WC',
  'Компьютерная визуализация ванной комнаты с душем без поддона, подвесной раковиной с зеркалом и унитазом',
  'حمام مولَّد بالحاسوب بدشّ واسع مفتوح ومغسلة معلقة بالجدار مع مرآة ومرحاض',
  'Computergegenereerde badkamer met een inloopdouche, een wandwastafel met spiegel en een toilet',
  'Wygenerowana komputerowo łazienka z prysznicem bez brodzika, umywalką wiszącą z lustrem i toaletą',
  'Datagenerert bad med en åpen dusj, en veggmontert servant med speil og et toalett',
  'Datorgenererat badrum med en duschhörna utan kar, ett väggmonterat handfat med spegel och en toalett')

# ---- unit rows and plan labels, built from the same numbers the English was built from ---------

INNER = {'es': 'm² interiores', 'fr': 'm² intérieurs', 'de': 'm² Innenfläche', 'ru': 'м² внутри',
         'ar': 'م² داخلية', 'nl': 'm² binnen', 'pl': 'm² wnętrza', 'no': 'm² innvendig', 'sv': 'm² inomhus'}
TERR = {'es': 'm² de terraza', 'fr': 'm² de terrasse', 'de': 'm² Terrasse', 'ru': 'терраса {} м²',
        'ar': 'م² تراس', 'nl': 'm² terras', 'pl': 'm² tarasu', 'no': 'm² terrasse', 'sv': 'm² terrass'}
GARD = {'es': 'm² de jardín', 'fr': 'm² de jardin', 'de': 'm² Garten', 'ru': 'сад {} м²',
        'ar': 'م² حديقة', 'nl': 'm² tuin', 'pl': 'm² ogrodu', 'no': 'm² hage', 'sv': 'm² trädgård'}
SEP = {l: ', ' for l in LOCS}; SEP['ar'] = '، '


def dec(x, loc):
    return f'{x:.1f}'.replace('.', '.' if loc == 'ar' else ',')


def size(inner, terr, garden, loc):
    parts = [f'{dec(inner, loc)} {INNER[loc]}']
    for x, tpl in ((terr, TERR), (garden, GARD)):
        if x is None:
            continue
        t = tpl[loc]
        parts.append(t.format(dec(x, loc)) if '{}' in t else f'{dec(x, loc)} {t}')
    return SEP[loc].join(parts)


# (index in the English units array, interior, terrace total, garden)
for i, n, t, g in [(0, 88.4, 27.8, None), (1, 73.6, 48.5, 44.9), (2, 106.0, 142.9, None)]:
    en = get(f'.availability.units[{i}].size')
    assert en == f'{n} sqm interior, {t} sqm terrace' + (f', {g} sqm garden' if g else ''), en
    T[en] = {l: size(n, t, g, l) for l in LOCS}

PLAN_ALT = {'es': 'Plano de la vivienda {}', 'fr': 'Plan du logement {}', 'de': 'Grundriss der Wohnung {}',
            'ru': 'Планировка квартиры {}', 'ar': 'مخطط المسكن {}', 'nl': 'Plattegrond van woning {}',
            'pl': 'Rzut lokalu {}', 'no': 'Plantegning av bolig {}', 'sv': 'Planritning för bostad {}'}
PLAN_CAP = {'es': 'Vivienda {}', 'fr': 'Logement {}', 'de': 'Wohnung {}', 'ru': 'Квартира {}',
            'ar': 'المسكن {}', 'nl': 'Woning {}', 'pl': 'Lokal {}', 'no': 'Bolig {}', 'sv': 'Bostad {}'}
n_plan = 0
for it in proj['media']['items']:
    for key, tpl, rx in (('alt', PLAN_ALT, r'Floorplan of home (\d-\d-\d-B)'), ('caption', PLAN_CAP, r'Home (\d-\d-\d-B)')):
        m = re.fullmatch(rx, it.get(key, ''))
        if m:
            T[it[key]] = {l: tpl[l].format(m.group(1)) for l in LOCS}
            n_plan += 1
assert n_plan == 6, n_plan

# ---- overview ------------------------------------------------------------------------------------

a('.overview.headlineHtml',
  'Cincuenta y siete viviendas, <em>tres en la lista</em>', 'Cinquante-sept logements, <em>trois sur la liste</em>',
  'Siebenundfünfzig Wohnungen, <em>drei auf der Liste</em>', 'Пятьдесят семь квартир, <em>три в списке</em>',
  'سبعة وخمسون مسكنًا، <em>ثلاثة منها في القائمة</em>', 'Zevenenvijftig woningen, <em>drie op de lijst</em>',
  'Pięćdziesiąt siedem lokali, <em>trzy na liście</em>', 'Femtisju boliger, <em>tre på listen</em>',
  'Femtiosju bostäder, <em>tre på listan</em>')
a('.overview.copy[0]',
  'Aire es una promoción de 57 viviendas de dos o tres dormitorios en dos bloques residenciales en Cancelada, en la Nueva Milla de Oro de Estepona, entre Estepona y Marbella. El dosier describe viviendas en planta baja con jardín privado, viviendas en plantas intermedias con grandes terrazas y áticos con solárium, y señala que todas las viviendas tienen una plaza de garaje y un trastero.',
  'Aire est un ensemble de 57 logements de deux ou trois chambres répartis en deux blocs résidentiels à Cancelada, sur la Nouvelle Mille d’Or d’Estepona, entre Estepona et Marbella. Le dossier décrit des logements en rez-de-chaussée avec jardin privatif, des logements aux étages intermédiaires avec de grandes terrasses et des penthouses avec solarium, et indique que chaque logement dispose d’une place de garage et d’une cave.',
  'Aire ist eine Anlage mit 57 Wohnungen mit zwei oder drei Schlafzimmern in zwei Wohnblöcken in Cancelada, an der Neuen Goldenen Meile von Estepona, zwischen Estepona und Marbella. Das Dossier beschreibt Erdgeschosswohnungen mit privatem Garten, Wohnungen in den mittleren Geschossen mit großen Terrassen und Penthouses mit Solarium und gibt an, dass jede Wohnung einen Garagenstellplatz und einen Abstellraum hat.',
  'Aire — комплекс из 57 квартир с двумя или тремя спальнями в двух жилых блоках в Канселаде, на Новой Золотой миле Эстепоны, между Эстепоной и Марбельей. В досье описаны квартиры на первом этаже с отдельным садом, квартиры на средних этажах с большими террасами и пентхаусы с солярием; сказано также, что у каждой квартиры есть место в гараже и кладовая.',
  'Aire مجمّع من 57 مسكنًا بغرفتي نوم أو ثلاث غرف نوم في مبنيين سكنيين في كانسيلادا، على الميل الذهبي الجديد في إستيبونا، بين إستيبونا وماربيا. ويصف ملف المطوّر مساكن في الطابق الأرضي بحديقة خاصة، ومساكن في الطوابق الوسطى بتراسات كبيرة، وبنتهاوسات بسولاريوم، ويذكر أن لكل مسكن موقف سيارات في المرآب ومخزنًا.',
  'Aire is een complex van 57 woningen met twee of drie slaapkamers in twee woonblokken in Cancelada, aan de Nieuwe Golden Mile van Estepona, tussen Estepona en Marbella. Het dossier beschrijft woningen op de begane grond met een eigen tuin, woningen op de middelste verdiepingen met grote terrassen en penthouses met een solarium, en vermeldt dat elke woning een garageplaats en een berging heeft.',
  'Aire to inwestycja obejmująca 57 lokali z dwiema lub trzema sypialniami w dwóch blokach mieszkalnych w Cancelada, na Nowej Złotej Mili w Esteponie, między Esteponą a Marbellą. Dossier opisuje lokale na parterze z prywatnym ogrodem, lokale na środkowych piętrach z dużymi tarasami oraz penthouse’y z solarium i podaje, że każdy lokal ma miejsce w garażu i komórkę lokatorską.',
  'Aire er et anlegg med 57 boliger med to eller tre soverom i to boligblokker i Cancelada, på Nye Golden Mile i Estepona, mellom Estepona og Marbella. Dossieret beskriver boliger i første etasje med privat hage, boliger i de midtre etasjene med store terrasser og toppleiligheter med solterrasse, og oppgir at hver bolig har en garasjeplass og en bod.',
  'Aire är ett område med 57 bostäder med två eller tre sovrum i två bostadshus i Cancelada, på Nya Golden Mile i Estepona, mellan Estepona och Marbella. Dossiern beskriver bostäder i bottenvåningen med privat trädgård, bostäder på mellanvåningarna med stora terrasser och takvåningar med solterrass, och anger att varje bostad har en garageplats och ett förråd.')
a('.overview.copy[1]',
  'La lista de precios nombra tres de las 57 viviendas y las marca todas como disponibles: una vivienda de tres dormitorios por {E487500}, una de dos dormitorios con jardín por {E492000} y una de tres dormitorios en la sexta planta con una terraza de {N142.9} {U} por {E922000}. Ninguno de los documentos que tenemos da una fecha de entrega.',
  'La liste de prix nomme trois des 57 logements et les indique tous trois comme disponibles : un logement de trois chambres à {E487500}, un logement de deux chambres avec jardin à {E492000} et un logement de trois chambres au sixième étage avec une terrasse de {N142.9} {U} à {E922000}. Aucun des documents que nous détenons ne donne de date de livraison.',
  'Die Preisliste nennt drei der 57 Wohnungen und weist alle drei als verfügbar aus: eine Wohnung mit drei Schlafzimmern für {E487500}, eine Wohnung mit zwei Schlafzimmern und Garten für {E492000} und eine Wohnung mit drei Schlafzimmern im sechsten Stock mit einer Terrasse von {N142.9} {U} für {E922000}. Keines der uns vorliegenden Dokumente nennt einen Fertigstellungstermin.',
  'В прайс-листе названы три из 57 квартир, и все три отмечены как доступные: квартира с тремя спальнями за {E487500}, квартира с двумя спальнями и садом за {E492000} и квартира с тремя спальнями на шестом этаже с террасой {N142.9} {U} за {E922000}. Ни в одном из имеющихся у нас документов срок сдачи не указан.',
  'تذكر قائمة الأسعار ثلاثة من المساكن الـ57 وتضعها جميعًا على أنها متاحة: مسكن بثلاث غرف نوم بسعر {E487500}، ومسكن بغرفتي نوم مع حديقة بسعر {E492000}، ومسكن بثلاث غرف نوم في الطابق السادس مع تراس مساحته {N142.9} {U} بسعر {E922000}. ولا تذكر أيٌّ من الوثائق التي بحوزتنا موعدًا للإنجاز.',
  'De prijslijst noemt drie van de 57 woningen en vermeldt alle drie als beschikbaar: een woning met drie slaapkamers voor {E487500}, een woning met twee slaapkamers en tuin voor {E492000} en een woning met drie slaapkamers op de zesde verdieping met een terras van {N142.9} {U} voor {E922000}. Geen van de documenten die wij hebben noemt een opleveringsdatum.',
  'Cennik wymienia trzy z 57 lokali i oznacza wszystkie trzy jako dostępne: lokal z trzema sypialniami za {E487500}, lokal z dwiema sypialniami i ogrodem za {E492000} oraz lokal z trzema sypialniami na szóstym piętrze z tarasem o powierzchni {N142.9} {U} za {E922000}. Żaden z posiadanych przez nas dokumentów nie podaje terminu oddania.',
  'Prislisten nevner tre av de 57 boligene og markerer alle tre som tilgjengelige: en bolig med tre soverom til {E487500}, en bolig med to soverom og hage til {E492000} og en bolig med tre soverom i sjette etasje med en terrasse på {N142.9} {U} til {E922000}. Ingen av dokumentene vi har oppgir en overleveringsdato.',
  'Prislistan nämner tre av de 57 bostäderna och markerar alla tre som tillgängliga: en bostad med tre sovrum för {E487500}, en bostad med två sovrum och trädgård för {E492000} och en bostad med tre sovrum på sjätte våningen med en terrass på {N142.9} {U} för {E922000}. Inget av dokumenten vi har anger ett tillträdesdatum.')
a('.overview.metrics[0][1]',
  '57 viviendas', '57 logements', '57 Wohnungen', '57 квартир', '57 مسكنًا', '57 woningen', '57 lokali', '57 boliger', '57 bostäder')

# ---- why -------------------------------------------------------------------------------------------

a('.why.copy',
  'Viviendas nuevas de dos y tres dormitorios con jardín o una gran terraza, plaza de garaje y trastero, en una promoción con piscina, gimnasio y acceso a la casa club.',
  'Des logements neufs de deux et trois chambres avec jardin ou grande terrasse, place de garage et cave, dans un ensemble avec piscine, salle de sport et accès au club-house.',
  'Neue Wohnungen mit zwei und drei Schlafzimmern, mit Garten oder großer Terrasse, Garagenstellplatz und Abstellraum, in einer Anlage mit Pool, Fitnessraum und Zugang zum Clubhaus.',
  'Новые квартиры с двумя и тремя спальнями, с садом или большой террасой, местом в гараже и кладовой, в комплексе с бассейном, спортзалом и доступом в клубный дом.',
  'مساكن جديدة بغرفتي نوم وثلاث غرف نوم مع حديقة أو تراس كبير وموقف سيارات في المرآب ومخزن، في مجمّع فيه مسبح وصالة رياضية وإمكانية الدخول إلى نادي المجمع.',
  'Nieuwe woningen met twee en drie slaapkamers met een tuin of een groot terras, een garageplaats en een berging, in een complex met zwembad, fitnessruimte en toegang tot het clubhuis.',
  'Nowe lokale z dwiema i trzema sypialniami, z ogrodem lub dużym tarasem, miejscem w garażu i komórką lokatorską, w inwestycji z basenem, siłownią i dostępem do klubu mieszkańców.',
  'Nye boliger med to og tre soverom, med hage eller stor terrasse, garasjeplass og bod, i et anlegg med basseng, treningsrom og tilgang til klubbhuset.',
  'Nya bostäder med två och tre sovrum, med trädgård eller stor terrass, garageplats och förråd, i ett område med pool, gym och tillgång till klubbhuset.')
a('.why.points[0][1]',
  'Compradores que buscan una vivienda nueva de dos o tres dormitorios con jardín o una gran terraza, plaza de garaje y trastero en la Nueva Milla de Oro, para vivir en ella o como segunda residencia.',
  'Les acheteurs qui recherchent un logement neuf de deux ou trois chambres avec jardin ou grande terrasse, place de garage et cave sur la Nouvelle Mille d’Or, pour y vivre ou comme résidence secondaire.',
  'Käufer, die an der Neuen Goldenen Meile eine neue Wohnung mit zwei oder drei Schlafzimmern mit Garten oder großer Terrasse, Garagenstellplatz und Abstellraum suchen, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужна новая квартира с двумя или тремя спальнями, с садом или большой террасой, местом в гараже и кладовой на Новой Золотой миле — для постоянного проживания или как вторая недвижимость.',
  'المشترون الذين يبحثون عن مسكن جديد بغرفتي نوم أو ثلاث غرف نوم مع حديقة أو تراس كبير وموقف سيارات في المرآب ومخزن على الميل الذهبي الجديد، للسكن الدائم أو كمسكن ثانٍ.',
  'Kopers die op de Nieuwe Golden Mile een nieuwe woning met twee of drie slaapkamers zoeken, met een tuin of een groot terras, een garageplaats en een berging, om er te wonen of als tweede woning.',
  'Kupujący, którzy szukają na Nowej Złotej Mili nowego lokalu z dwiema lub trzema sypialniami, z ogrodem lub dużym tarasem, miejscem w garażu i komórką lokatorską, do zamieszkania lub jako drugi dom.',
  'Kjøpere som vil ha en ny bolig med to eller tre soverom, med hage eller stor terrasse, garasjeplass og bod på Nye Golden Mile, til å bo i eller som fritidsbolig.',
  'Köpare som vill ha en ny bostad med två eller tre sovrum, med trädgård eller stor terrass, garageplats och förråd på Nya Golden Mile, att bo i eller som fritidsbostad.')
a('.why.points[1][1]',
  'Las tres viviendas de la lista son de tres tipos distintos: una en la segunda planta con una terraza cubierta, una en la primera planta con una terraza cubierta, una terraza descubierta y un jardín de {N44.9} {U}, y una en la sexta planta con una terraza descubierta de {N142.9} {U}. Cada una tiene una plaza de garaje y un trastero.',
  'Les trois logements de la liste sont de trois types différents : un logement au deuxième étage avec une terrasse couverte, un logement au premier étage avec une terrasse couverte, une terrasse découverte et un jardin de {N44.9} {U}, et un logement au sixième étage avec une terrasse découverte de {N142.9} {U}. Chacun dispose d’une place de garage et d’une cave.',
  'Die drei Wohnungen auf der Liste sind drei verschiedene Typen: eine Wohnung im zweiten Stock mit überdachter Terrasse, eine Wohnung im ersten Stock mit einer überdachten und einer nicht überdachten Terrasse und einem Garten von {N44.9} {U} sowie eine Wohnung im sechsten Stock mit einer nicht überdachten Terrasse von {N142.9} {U}. Jede hat einen Garagenstellplatz und einen Abstellraum.',
  'Три квартиры из списка относятся к трём разным типам: квартира на втором этаже с крытой террасой, квартира на первом этаже с крытой и открытой террасами и садом {N44.9} {U} и квартира на шестом этаже с открытой террасой {N142.9} {U}. У каждой есть место в гараже и кладовая.',
  'المساكن الثلاثة في القائمة من ثلاثة أنواع مختلفة: مسكن في الطابق الثاني بتراس مغطى، ومسكن في الطابق الأول بتراس مغطى وآخر مكشوف وحديقة مساحتها {N44.9} {U}، ومسكن في الطابق السادس بتراس مكشوف مساحته {N142.9} {U}. ولكل منها موقف سيارات في المرآب ومخزن.',
  'De drie woningen op de lijst zijn drie verschillende soorten: een woning op de tweede verdieping met een overdekt terras, een woning op de eerste verdieping met een overdekt en een open terras en een tuin van {N44.9} {U}, en een woning op de zesde verdieping met een open terras van {N142.9} {U}. Elke woning heeft een garageplaats en een berging.',
  'Trzy lokale z listy to trzy różne typy: lokal na drugim piętrze z zadaszonym tarasem, lokal na pierwszym piętrze z tarasem zadaszonym i odkrytym oraz ogrodem o powierzchni {N44.9} {U} i lokal na szóstym piętrze z odkrytym tarasem o powierzchni {N142.9} {U}. Każdy ma miejsce w garażu i komórkę lokatorską.',
  'De tre boligene på listen er tre ulike typer: en bolig i andre etasje med en overbygd terrasse, en bolig i første etasje med en overbygd og en åpen terrasse og en hage på {N44.9} {U}, og en bolig i sjette etasje med en åpen terrasse på {N142.9} {U}. Hver har en garasjeplass og en bod.',
  'De tre bostäderna på listan är av tre olika slag: en bostad på andra våningen med en täckt terrass, en bostad på första våningen med en täckt och en öppen terrass och en trädgård på {N44.9} {U}, och en bostad på sjätte våningen med en öppen terrass på {N142.9} {U}. Varje bostad har en garageplats och ett förråd.')
a('.why.points[2][1]',
  'Cancelada es una zona residencial entre Estepona y Marbella. El dosier sitúa un gran parque arbolado delante de la promoción, la ciclosenda de Cancelada a su lado y la casa club a 450 m, y nombra campos de golf desde 2 km.',
  'Cancelada est un quartier résidentiel entre Estepona et Marbella. Le dossier place un grand parc arboré devant l’ensemble, la piste cyclable de Cancelada à côté et le club-house à 450 m, et cite des golfs à partir de 2 km.',
  'Cancelada ist ein Wohngebiet zwischen Estepona und Marbella. Laut Dossier liegen ein großer, baumbestandener Park vor der Anlage, der Radweg von Cancelada daneben und das Clubhaus 450 m entfernt, und es nennt Golfplätze ab 2 km.',
  'Канселада — жилой район между Эстепоной и Марбельей. В досье указаны большой парк с деревьями перед комплексом, велодорожка Канселады рядом с ним и клубный дом в 450 м; там же названы поля для гольфа от 2 км.',
  'كانسيلادا منطقة سكنية بين إستيبونا وماربيا. ويضع ملف المطوّر حديقة كبيرة مشجرة أمام المجمّع ومسار دراجات كانسيلادا بجانبه ونادي المجمع على بعد 450 م، ويذكر ملاعب غولف ابتداءً من 2 كم.',
  'Cancelada is een woonwijk tussen Estepona en Marbella. Het dossier plaatst een groot park met bomen voor het complex, het fietspad van Cancelada ernaast en het clubhuis op 450 m, en noemt golfbanen vanaf 2 km.',
  'Cancelada to dzielnica mieszkalna między Esteponą a Marbellą. Dossier umieszcza duży park z drzewami przed inwestycją, ścieżkę rowerową w Cancelada obok niej i klub mieszkańców w odległości 450 m oraz wymienia pola golfowe od 2 km.',
  'Cancelada er et boligområde mellom Estepona og Marbella. Dossieret plasserer en stor, trebevokst park foran anlegget, sykkelstien i Cancelada ved siden av og klubbhuset 450 m unna, og nevner golfbaner fra 2 km.',
  'Cancelada är ett bostadsområde mellan Estepona och Marbella. Dossiern placerar en stor trädplanterad park framför området, cykelvägen i Cancelada intill det och klubbhuset 450 m bort, och nämner golfbanor från 2 km.')
a('.why.points[3][1]',
  'La lista de precios recoge tres de las 57 viviendas y no dice nada de las otras 54. Los documentos no dan fecha de entrega, estado de la licencia ni tratamiento del IVA, por lo que pedimos los tres datos antes de cualquier reserva.',
  'La liste de prix couvre trois des 57 logements et ne dit rien des 54 autres. Les documents ne donnent ni date de livraison, ni état du permis, ni régime de TVA ; nous demandons les trois avant toute réservation.',
  'Die Preisliste umfasst drei der 57 Wohnungen und sagt nichts über die anderen 54. Die Unterlagen nennen weder einen Fertigstellungstermin noch den Stand der Genehmigung noch die MwSt.-Behandlung, daher fordern wir alle drei vor jeder Reservierung an.',
  'Прайс-лист охватывает три из 57 квартир и ничего не говорит об остальных 54. В документах нет ни срока сдачи, ни статуса разрешения, ни режима НДС, поэтому мы запрашиваем все три сведения до любого бронирования.',
  'تشمل قائمة الأسعار ثلاثة من المساكن الـ57 ولا تقول شيئًا عن الـ54 الأخرى. ولا تذكر الوثائق موعد الإنجاز ولا وضع الرخصة ولا معاملة ضريبة القيمة المضافة، لذلك نطلب الثلاثة قبل أي حجز.',
  'De prijslijst omvat drie van de 57 woningen en zegt niets over de andere 54. De documenten geven geen opleveringsdatum, geen status van de vergunning en geen btw-behandeling, dus we vragen alle drie op vóór een reservering.',
  'Cennik obejmuje trzy z 57 lokali i nic nie mówi o pozostałych 54. Dokumenty nie podają terminu oddania, statusu pozwolenia ani sposobu traktowania VAT, dlatego prosimy o wszystkie trzy informacje przed jakąkolwiek rezerwacją.',
  'Prislisten omfatter tre av de 57 boligene og sier ingenting om de andre 54. Dokumentene oppgir ingen overleveringsdato, ingen status for tillatelsen og ingen mva-behandling, så vi ber om alle tre før enhver reservasjon.',
  'Prislistan omfattar tre av de 57 bostäderna och säger ingenting om de övriga 54. Dokumenten anger varken tillträdesdatum, bygglovets status eller IVA-behandling (spansk moms), så vi ber om alla tre före varje reservation.')

# ---- architecture --------------------------------------------------------------------------------

a('.architecture.headlineHtml',
  'Bloques escalonados, <em>terrazas abiertas a las vistas</em>', 'Des blocs en gradins, <em>des terrasses ouvertes sur la vue</em>',
  'Gestaffelte Gebäude, <em>Terrassen zur Aussicht hin geöffnet</em>', 'Ступенчатые блоки, <em>террасы с открытым видом</em>',
  'مبانٍ متدرجة، <em>وتراسات مفتوحة على الإطلالة</em>', 'Trapsgewijze blokken, <em>terrassen open naar het uitzicht</em>',
  'Schodkowe budynki, <em>tarasy otwarte na widok</em>', 'Trappede blokker, <em>terrasser åpne mot utsikten</em>',
  'Trappstegsformade hus, <em>terrasser öppna mot utsikten</em>')
a('.architecture.copy[0]',
  'El dosier describe dos bloques residenciales de arquitectura contemporánea y señala que todas las viviendas tienen vistas despejadas y una orientación elegida para captar la luz. En las imágenes, los bordes blancos de las terrazas retroceden planta a planta, con barandillas de cristal sobre muros de color arena.',
  'Le dossier décrit deux blocs résidentiels d’architecture contemporaine et indique que chaque logement a des vues dégagées et une orientation choisie pour capter la lumière. Sur les images, les rebords blancs des terrasses reculent étage par étage, avec des garde-corps en verre sur des murs de couleur sable.',
  'Das Dossier beschreibt zwei Wohnblöcke zeitgenössischer Architektur und gibt an, dass jede Wohnung offene Ausblicke und eine auf den Lichteinfall abgestimmte Ausrichtung hat. Auf den Visualisierungen springen die weißen Terrassenkanten Geschoss für Geschoss zurück, mit Glasbrüstungen vor sandfarbenen Wänden.',
  'В досье описаны два жилых блока современной архитектуры и сказано, что у каждой квартиры открытый вид и ориентация, выбранная так, чтобы ловить свет. На визуализациях белые края террас отступают от этажа к этажу, со стеклянными ограждениями на фоне стен песочного цвета.',
  'يصف ملف المطوّر مبنيين سكنيين بعمارة معاصرة، ويذكر أن لكل مسكن إطلالات مفتوحة واتجاهًا اختير لالتقاط الضوء. وفي الصور المولَّدة تتراجع حواف التراسات البيضاء طابقًا بعد طابق، مع حواجز زجاجية فوق جدران بلون الرمل.',
  'Het dossier beschrijft twee woonblokken met eigentijdse architectuur en vermeldt dat elke woning open uitzichten heeft en een oriëntatie die is gekozen om het licht op te vangen. Op de beelden springen de witte terrasranden verdieping na verdieping terug, met glazen balustrades voor zandkleurige muren.',
  'Dossier opisuje dwa bloki mieszkalne o współczesnej architekturze i podaje, że każdy lokal ma otwarty widok i usytuowanie dobrane tak, by łapać światło. Na wizualizacjach białe krawędzie tarasów cofają się piętro po piętrze, ze szklanymi balustradami na tle ścian w kolorze piasku.',
  'Dossieret beskriver to boligblokker med moderne arkitektur og oppgir at hver bolig har åpen utsikt og en orientering valgt for å fange lyset. På visualiseringene trapper de hvite terrassekantene seg tilbake etasje for etasje, med glassrekkverk foran sandfargede vegger.',
  'Dossiern beskriver två bostadshus med modern arkitektur och anger att varje bostad har öppen utsikt och ett läge valt för att fånga ljuset. På bilderna trappar de vita terrasskanterna av våning för våning, med glasräcken framför sandfärgade väggar.')
a('.architecture.copy[1]',
  'Las viviendas de planta baja se abren a un jardín privado, las de plantas intermedias tienen grandes terrazas y los áticos un solárium privado, tal como los enumera el dosier.',
  'Les logements de rez-de-chaussée s’ouvrent sur un jardin privatif, ceux des étages intermédiaires ont de grandes terrasses et les penthouses un solarium privatif, comme le dossier les énumère.',
  'Die Erdgeschosswohnungen öffnen sich zu einem privaten Garten, die Wohnungen in den mittleren Geschossen haben große Terrassen und die Penthouses ein privates Solarium, wie das Dossier sie aufführt.',
  'Квартиры на первом этаже выходят в собственный сад, квартиры на средних этажах имеют большие террасы, а пентхаусы — собственный солярий, как это перечислено в досье.',
  'تنفتح مساكن الطابق الأرضي على حديقة خاصة، وللمساكن في الطوابق الوسطى تراسات كبيرة، وللبنتهاوسات سولاريوم خاص، كما يوردها ملف المطوّر.',
  'De woningen op de begane grond openen naar een eigen tuin, de woningen op de middelste verdiepingen hebben grote terrassen en de penthouses een eigen solarium, zoals het dossier ze opsomt.',
  'Lokale na parterze otwierają się na prywatny ogród, lokale na środkowych piętrach mają duże tarasy, a penthouse’y prywatne solarium, tak jak wymienia je dossier.',
  'Boligene i første etasje åpner seg mot en privat hage, boligene i de midtre etasjene har store terrasser og toppleilighetene en privat solterrasse, slik dossieret lister dem opp.',
  'Bostäderna i bottenvåningen öppnar sig mot en privat trädgård, bostäderna på mellanvåningarna har stora terrasser och takvåningarna en privat solterrass, så som dossiern räknar upp dem.')
a('.architecture.highlights[2][1]',
  'Ventanas y puertas exteriores con rotura de puente térmico y doble acristalamiento termoacústico, con persianas aisladas en los dormitorios.',
  'Fenêtres et portes extérieures à rupture de pont thermique et double vitrage thermo-acoustique, avec des volets isolés dans les chambres.',
  'Fenster und Außentüren mit thermischer Trennung und thermo-akustischer Doppelverglasung, mit gedämmten Rollläden in den Schlafzimmern.',
  'Окна и наружные двери с терморазрывом и теплозвукоизолирующим стеклопакетом, с утеплёнными жалюзи в спальнях.',
  'نوافذ وأبواب خارجية بقطع حراري وزجاج مزدوج حراري صوتي، مع ستائر معزولة في غرف النوم.',
  'Ramen en buitendeuren met thermische onderbreking en thermo-akoestisch dubbel glas, met geïsoleerde rolluiken in de slaapkamers.',
  'Okna i drzwi zewnętrzne z przerwą termiczną i termoakustycznym podwójnym szkleniem oraz izolowanymi roletami w sypialniach.',
  'Vinduer og ytterdører med termisk brudd og termoakustisk tolagsglass, med isolerte persienner på soverommene.',
  'Fönster och ytterdörrar med termiskt brott och termoakustiskt tvåglas, med isolerade persienner i sovrummen.')

# ---- quality specification -----------------------------------------------------------------------

a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor y las páginas de calidades de su dosier, ninguna de las cuales lleva fecha. Indican que no son contractuales y que pueden modificarse por razones técnicas, legales o administrativas sin reducir el nivel general de calidad, y que las imágenes, el mobiliario, la jardinería y los electrodomésticos mostrados son orientativos.',
  'Source : le descriptif de qualité du promoteur et les pages de descriptif de son dossier, qui ne portent ni l’un ni l’autre de date. Ils précisent qu’ils n’ont pas de valeur contractuelle et qu’ils peuvent être modifiés pour des raisons techniques, juridiques ou administratives sans baisse du niveau général de qualité, et que les images, le mobilier, l’aménagement paysager et l’électroménager représentés sont donnés à titre indicatif.',
  'Quelle: die Qualitätsbeschreibung des Bauträgers und die Ausstattungsseiten seines Dossiers, von denen keine ein Datum trägt. Sie geben an, dass sie vertraglich nicht bindend sind und aus technischen, rechtlichen oder administrativen Gründen geändert werden können, ohne das allgemeine Qualitätsniveau zu senken, und dass die gezeigten Bilder, Möbel, Gartengestaltung und Geräte nur zur Orientierung dienen.',
  'Источник: спецификация качества застройщика и страницы со спецификацией в его досье, ни одна из которых не датирована. В них сказано, что они не имеют договорной силы и могут быть изменены по техническим, юридическим или административным причинам без снижения общего уровня качества, а показанные изображения, мебель, озеленение и техника носят ориентировочный характер.',
  'المصدر: مواصفات الجودة لدى المطوّر وصفحات المواصفات في ملفه، وليس على أيٍّ منهما تاريخ. وتذكر أنها غير ملزمة تعاقديًا وأنه يمكن تعديلها لأسباب فنية أو قانونية أو إدارية دون خفض المستوى العام للجودة، وأن الصور والأثاث والتنسيق النباتي والأجهزة المعروضة للاسترشاد فقط.',
  'Bron: de kwaliteitsomschrijving van de ontwikkelaar en de specificatiepagina’s van zijn dossier, waarvan geen van beide een datum draagt. Ze vermelden dat ze contractueel niet bindend zijn en om technische, juridische of administratieve redenen kunnen worden gewijzigd zonder het algemene kwaliteitsniveau te verlagen, en dat de getoonde beelden, het meubilair, de tuinaanleg en de apparatuur slechts ter oriëntatie dienen.',
  'Źródło: specyfikacja jakości dewelopera i strony ze specyfikacją w jego dossier, z których żadne nie jest opatrzone datą. Podają one, że nie mają mocy umownej i mogą zostać zmienione z przyczyn technicznych, prawnych lub administracyjnych bez obniżania ogólnego poziomu jakości, a pokazane wizualizacje, meble, zagospodarowanie zieleni i sprzęty mają charakter poglądowy.',
  'Kilde: utbyggers kvalitetsbeskrivelse og spesifikasjonssidene i dossieret, og ingen av dem er datert. De oppgir at de ikke er kontraktsfestet og kan endres av tekniske, juridiske eller administrative grunner uten at det generelle kvalitetsnivået senkes, og at bildene, møblene, hagearbeidet og apparatene som vises, bare er veiledende.',
  'Källa: exploatörens kvalitetsbeskrivning och specifikationssidorna i dess dossier, varav ingen är daterad. De anger att de inte är avtalsbindande och kan ändras av tekniska, juridiska eller administrativa skäl utan att den allmänna kvalitetsnivån sänks, och att bilderna, möblerna, trädgårdsarbetet och apparaterna som visas bara är vägledande.')
a('.qualitySpecs.groups[0].items[0]',
  'Baldosa de gres porcelánico rectificado de 90 x 90 cm, en color crema, con el gris como opción, en toda la vivienda, y gres de exterior en las terrazas.',
  'Carrelage en grès cérame rectifié de 90 x 90 cm, de couleur crème, avec le gris en option, dans tout le logement, et grès cérame d’extérieur sur les terrasses.',
  'Rektifizierte Feinsteinfliesen, 90 x 90 cm, in Creme, optional in Grau, in der gesamten Wohnung und Außensteinzeug auf den Terrassen.',
  'Ректифицированная керамогранитная плитка 90 x 90 см кремового цвета, серая — по выбору, по всей квартире и уличный керамогранит на террасах.',
  'بلاط بورسلين مقصوص بدقة مقاس 90 x 90 سم بلون كريمي، مع الرمادي كخيار، في أرجاء المسكن، وبلاط خارجي من الحجر الخزفي على التراسات.',
  'Gerectificeerde porseleinen tegels van 90 x 90 cm in crème, met grijs als optie, in de hele woning, en buitengres op de terrassen.',
  'Rektyfikowane płytki gresowe 90 x 90 cm w kolorze kremowym, z szarym jako opcją, w całym lokalu oraz gres zewnętrzny na tarasach.',
  'Rektifiserte porselensfliser på 90 x 90 cm i krem, med grå som tilvalg, i hele boligen, og utendørs steingods på terrassene.',
  'Rektifierat porslinsklinker på 90 x 90 cm i crème, med grått som tillval, i hela bostaden, och utomhusklinker på terrasserna.')
a('.qualitySpecs.groups[0].items[1]',
  'Paredes del baño revestidas de porcelánico, en blanco mate de 40 x 120 cm o en crema o gris de 30 x 90 cm, en la zona de la ducha y la bañera, y pintura plástica en el resto de las paredes.',
  'Murs de salle de bain revêtus de grès cérame, en blanc mat de 40 x 120 cm ou en crème ou gris de 30 x 90 cm, dans la zone de douche et de baignoire, et peinture plastique sur les autres murs.',
  'Badezimmerwände mit Feinsteinzeug gefliest, in mattem Weiß 40 x 120 cm oder in Creme oder Grau 30 x 90 cm, im Dusch- und Badebereich, und Kunststoffdispersionsfarbe an den übrigen Wänden.',
  'Стены ванных комнат в зоне душа и ванны облицованы керамогранитом: матовым белым 40 x 120 см либо кремовым или серым 30 x 90 см; остальные стены окрашены акриловой краской.',
  'جدران الحمام مكسوة ببلاط البورسلين، بالأبيض غير اللامع مقاس 40 x 120 سم أو بالكريمي أو الرمادي مقاس 30 x 90 سم، في منطقة الدش والحوض، وطلاء بلاستيكي على بقية الجدران.',
  'Badkamerwanden betegeld met porselein, in mat wit van 40 x 120 cm of in crème of grijs van 30 x 90 cm, in de douche- en badzone, en kunststofverf op de overige wanden.',
  'Ściany łazienek wyłożone płytkami gresowymi, w białym macie 40 x 120 cm lub w kolorze kremowym albo szarym 30 x 90 cm, w strefie prysznica i wanny, oraz farba plastyczna na pozostałych ścianach.',
  'Baderomsvegger flislagt med porselen, i matt hvitt 40 x 120 cm eller i krem eller grått 30 x 90 cm, i dusj- og badekarsonen, og plastmaling på de andre veggene.',
  'Badrumsväggar klädda med porslinsklinker, i matt vitt 40 x 120 cm eller i crème eller grått 30 x 90 cm, i dusch- och badkarsområdet, och plastfärg på de övriga väggarna.')
a('.qualitySpecs.groups[2].items[1]',
  'Las opciones sin coste adicional son la combinación de colores de los muebles y el modelo de encimera; entre las opciones con coste adicional figuran el panelado de los electrodomésticos, la iluminación LED bajo los muebles altos, mejores electrodomésticos, una isla, un equipo de ósmosis y una vinoteca.',
  'Les options sans supplément sont l’association de couleurs des meubles et le modèle de plan de travail ; parmi les options payantes figurent l’habillage des appareils, l’éclairage LED sous les meubles hauts, de meilleurs appareils, un îlot, un système d’osmose et une cave à vin.',
  'Ohne Aufpreis wählbar sind die Farbkombination der Schränke und das Arbeitsplattenmodell; gegen Aufpreis gibt es unter anderem Geräteverkleidungen, LED-Beleuchtung unter den Hängeschränken, hochwertigere Geräte, eine Kücheninsel, eine Osmoseanlage und einen Weinkühler.',
  'Без доплаты можно выбрать цветовое сочетание шкафов и модель столешницы; за доплату доступны фасады для встроенной техники, светодиодная подсветка под навесными шкафами, техника получше, остров, система обратного осмоса и винный шкаф.',
  'الخيارات دون تكلفة إضافية هي تركيبة ألوان الخزائن وطراز سطح العمل؛ أما الخيارات بتكلفة إضافية فتشمل تغطية الأجهزة بواجهات، وإضاءة LED تحت الخزائن العلوية، وأجهزة أفضل، وجزيرة، ووحدة تناضح عكسي، وثلاجة نبيذ.',
  'Opties zonder meerprijs zijn de kleurcombinatie van de kasten en het model van het werkblad; opties tegen meerprijs zijn onder meer afwerking van de apparaten, led-verlichting onder de bovenkasten, betere apparaten, een eiland, een osmose-unit en een wijnklimaatkast.',
  'Opcje bez dopłaty to zestawienie kolorów szafek i model blatu; opcje płatne obejmują zabudowę sprzętów, oświetlenie LED pod szafkami wiszącymi, lepszy sprzęt, wyspę, system odwróconej osmozy i chłodziarkę do wina.',
  'Tilvalg uten ekstra kostnad er fargekombinasjonen på skapene og modellen på benkeplaten; tilvalg mot tillegg omfatter dekking av apparatene, LED-belysning under overskapene, bedre apparater, en øy, et osmoseanlegg og et vinskap.',
  'Tillval utan extra kostnad är färgkombinationen på skåpen och modellen på bänkskivan; tillval mot tillägg omfattar infodring av apparaterna, LED-belysning under väggskåpen, bättre apparater, en köksö, ett osmosfilter och ett vinkylskåp.')
a('.qualitySpecs.groups[3].items[0]',
  'Sanitarios de porcelana vitrificada, un lavabo suspendido con grifería integrada y un espejo encima en los baños principal y secundario, un plato de ducha en los baños principales y una bañera en los secundarios, y grifería termostática en la ducha.',
  'Sanitaires en porcelaine vitrifiée, un lavabo suspendu avec robinetterie intégrée et un miroir au-dessus dans les salles de bain principale et secondaire, un receveur de douche dans les salles de bain principales et une baignoire dans les secondaires, et une robinetterie thermostatique dans la douche.',
  'Sanitärkeramik aus Porzellan, ein wandhängendes Waschbecken mit integrierter Armatur und einem Spiegel darüber im Hauptbad und in den Nebenbädern, eine Duschwanne in den Hauptbädern und eine Badewanne in den Nebenbädern sowie Thermostatarmaturen in der Dusche.',
  'Сантехника из глазурованного фарфора, подвесная раковина со встроенным смесителем и зеркалом над ней в основной и второстепенной ванных комнатах, душевой поддон в основных ванных комнатах и ванна во второстепенных, а также термостатические смесители в душе.',
  'أدوات صحية من البورسلين المزجَّج، ومغسلة معلقة بالجدار بخلاطات مدمجة ومرآة فوقها في الحمامين الرئيسي والثانوي، وحوض دش في الحمامات الرئيسية وحوض استحمام في الثانوية، وخلاطات ثرموستاتية في الدش.',
  'Sanitair van verglaasd porselein, een hangende wastafel met ingebouwde kranen en een spiegel erboven in de hoofd- en de tweede badkamer, een douchebak in de hoofdbadkamers en een bad in de tweede badkamers, en thermostatische kranen in de douche.',
  'Ceramika sanitarna z porcelany witryfikowanej, umywalka wisząca z wbudowanymi bateriami i lustrem nad nią w łazience głównej i dodatkowej, brodzik w łazienkach głównych i wanna w dodatkowych oraz baterie termostatyczne w prysznicu.',
  'Sanitærutstyr i vitrifisert porselen, en veggmontert servant med innebygde armaturer og et speil over i hoved- og sekundærbadene, en dusjkum i hovedbadene og et badekar i sekundærbadene, og termostatarmaturer i dusjen.',
  'Sanitetsgods i förglasat porslin, ett väggmonterat handfat med inbyggda blandare och en spegel ovanför i de primära och sekundära badrummen, ett duschkar i de primära badrummen och ett badkar i de sekundära, och termostatblandare i duschen.')
a('.qualitySpecs.groups[3].items[1]',
  'Entre las opciones con coste adicional figuran un espejo retroiluminado, grifería negra, una mampara de ducha, un grifo de bidé y el alicatado completo del baño.',
  'Parmi les options payantes figurent un miroir rétroéclairé, une robinetterie noire, une paroi de douche, une robinetterie de bidet et le carrelage complet de la salle de bain.',
  'Gegen Aufpreis gibt es unter anderem einen hinterleuchteten Spiegel, schwarze Armaturen, eine Duschwand, eine Bidetarmatur und die vollständige Verfliesung des Bades.',
  'За доплату доступны зеркало с подсветкой, чёрные смесители, душевая перегородка, смеситель для биде и облицовка плиткой всей ванной комнаты.',
  'تشمل الخيارات بتكلفة إضافية مرآة بإضاءة خلفية وخلاطات سوداء وحاجز دش وخلاط بيديه وتكسية الحمام بالكامل بالبلاط.',
  'Opties tegen meerprijs zijn onder meer een spiegel met verlichting, zwarte kranen, een douchewand, een bidetkraan en het volledig betegelen van de badkamer.',
  'Opcje płatne obejmują lustro z podświetleniem, czarne baterie, kabinę prysznicową, baterię do bidetu i pełne wyłożenie łazienki płytkami.',
  'Tilvalg mot tillegg omfatter et bakbelyst speil, svarte armaturer, en dusjvegg, en bidétut og full flislegging av badet.',
  'Tillval mot tillägg omfattar en bakgrundsbelyst spegel, svarta blandare, en duschvägg, en bidéblandare och full kakelsättning av badrummet.')
a('.qualitySpecs.groups[4].items[2]',
  'La memoria de calidades otorga a las viviendas la máxima calificación, A, tanto en consumo de energía primaria no renovable como en emisiones de carbono, y los planos señalan que la calificación definitiva de los sellos de sostenibilidad solo se obtiene tras el proyecto de ejecución.',
  'Le descriptif de qualité attribue aux logements la meilleure note, A, tant pour la consommation d’énergie primaire non renouvelable que pour les émissions de carbone, et les plans précisent que la note définitive des labels de durabilité n’est obtenue qu’après le projet d’exécution.',
  'Die Qualitätsbeschreibung weist den Wohnungen die höchste Bewertung A zu, sowohl beim nicht erneuerbaren Primärenergieverbrauch als auch bei den Kohlenstoffemissionen, und die Pläne vermerken, dass die endgültige Bewertung der Nachhaltigkeitssiegel erst nach dem Ausführungsprojekt erteilt wird.',
  'Спецификация качества присваивает квартирам высший класс A как по потреблению невозобновляемой первичной энергии, так и по выбросам углерода, а в планах отмечено, что окончательная оценка знаков устойчивости будет получена только после рабочего проекта.',
  'تمنح مواصفات الجودة المساكن أعلى تصنيف، A، لكلٍّ من استهلاك الطاقة الأولية غير المتجددة وانبعاثات الكربون، وتشير المخططات إلى أن التصنيف النهائي لأختام الاستدامة لا يُحصل عليه إلا بعد مشروع التنفيذ.',
  'De kwaliteitsomschrijving geeft de woningen de hoogste beoordeling, A, voor zowel het niet-hernieuwbare primaire energiegebruik als de koolstofemissies, en de plattegronden vermelden dat de definitieve beoordeling van de duurzaamheidskeuren pas na het uitvoeringsproject wordt verkregen.',
  'Specyfikacja jakości przyznaje lokalom najwyższą ocenę, A, zarówno za zużycie nieodnawialnej energii pierwotnej, jak i za emisje dwutlenku węgla, a rzuty zawierają informację, że ostateczna ocena certyfikatów zrównoważonego budownictwa jest uzyskiwana dopiero po projekcie wykonawczym.',
  'Kvalitetsbeskrivelsen gir boligene høyeste vurdering, A, både for bruk av ikke-fornybar primærenergi og for karbonutslipp, og planene opplyser at den endelige vurderingen av bærekraftsmerkene først oppnås etter gjennomføringsprosjektet.',
  'Kvalitetsbeskrivningen ger bostäderna högsta betyg, A, både för användning av icke-förnybar primärenergi och för koldioxidutsläpp, och planritningarna anger att det slutliga betyget för hållbarhetsmärkena först erhålls efter genomförandeprojektet.')

# ---- residences ----------------------------------------------------------------------------------

a('.residences.headlineHtml',
  'Tres viviendas, <em>tres tipos de espacio exterior</em>', 'Trois logements, <em>trois types d’espace extérieur</em>',
  'Drei Wohnungen, <em>drei Arten von Außenbereich</em>', 'Три квартиры, <em>три вида открытого пространства</em>',
  'ثلاثة مساكن، <em>ثلاثة أنواع من المساحات الخارجية</em>', 'Drie woningen, <em>drie soorten buitenruimte</em>',
  'Trzy lokale, <em>trzy rodzaje przestrzeni zewnętrznej</em>', 'Tre boliger, <em>tre slags uteområder</em>',
  'Tre bostäder, <em>tre slags utomhusytor</em>')
a('.residences.copy',
  'Las tres viviendas de la lista de precios están en dos bloques y difieren en tamaño y espacio exterior. La tabla de abajo recoge cada una con su precio.',
  'Les trois logements de la liste de prix se trouvent dans deux blocs et diffèrent par leur taille et leur espace extérieur. Le tableau ci-dessous les présente chacun avec son prix.',
  'Die drei Wohnungen auf der Preisliste liegen in zwei Blöcken und unterscheiden sich in Größe und Außenbereich. Die Tabelle unten führt jede mit ihrem Preis auf.',
  'Три квартиры из прайс-листа находятся в двух блоках и различаются размером и открытым пространством. В таблице ниже приведена каждая из них с ценой.',
  'تقع المساكن الثلاثة الواردة في قائمة الأسعار في مبنيين وتختلف في المساحة والمساحات الخارجية. ويورد الجدول أدناه كلًّا منها مع سعره.',
  'De drie woningen op de prijslijst liggen in twee blokken en verschillen in grootte en buitenruimte. De tabel hieronder vermeldt elk ervan met zijn prijs.',
  'Trzy lokale z cennika znajdują się w dwóch blokach i różnią się wielkością oraz przestrzenią zewnętrzną. Tabela poniżej podaje każdy z nich wraz z ceną.',
  'De tre boligene på prislisten ligger i to blokker og er ulike i størrelse og uteområde. Tabellen nedenfor viser hver av dem med pris.',
  'De tre bostäderna på prislistan ligger i två hus och skiljer sig i storlek och utomhusyta. Tabellen nedan listar var och en med sitt pris.')
a('.residences.items[0].name',
  'Una vivienda de tres dormitorios en la segunda planta', 'Un logement de trois chambres au deuxième étage',
  'Eine Wohnung mit drei Schlafzimmern im zweiten Stock', 'Квартира с тремя спальнями на втором этаже',
  'مسكن بثلاث غرف نوم في الطابق الثاني', 'Een woning met drie slaapkamers op de tweede verdieping',
  'Lokal z trzema sypialniami na drugim piętrze', 'En bolig med tre soverom i andre etasje',
  'En bostad med tre sovrum på andra våningen')
a('.residences.items[0].points[0]',
  'Vivienda 2-4-2-B, en el bloque 2, portal 4: tres dormitorios y dos baños, con {N88.4} {U} interiores.',
  'Logement 2-4-2-B, dans le bloc 2, cage 4 : trois chambres et deux salles de bain, avec {N88.4} {U} intérieurs.',
  'Wohnung 2-4-2-B, in Block 2, Aufgang 4: drei Schlafzimmer und zwei Bäder, mit {N88.4} {U} Innenfläche.',
  'Квартира 2-4-2-B, блок 2, подъезд 4: три спальни и две ванные комнаты, внутренняя площадь {N88.4} {U}.',
  'المسكن 2-4-2-B، في المبنى 2، المدخل 4: ثلاث غرف نوم وحمامان، بمساحة داخلية {N88.4} {U}.',
  'Woning 2-4-2-B, in blok 2, portiek 4: drie slaapkamers en twee badkamers, met {N88.4} {U} binnen.',
  'Lokal 2-4-2-B, w bloku 2, klatka 4: trzy sypialnie i dwie łazienki, z {N88.4} {U} powierzchni wewnętrznej.',
  'Bolig 2-4-2-B, i hus 2, oppgang 4: tre soverom og to bad, med {N88.4} {U} innvendig.',
  'Bostad 2-4-2-B, i hus 2, uppgång 4: tre sovrum och två badrum, med {N88.4} {U} inomhus.')
a('.residences.items[0].points[1]',
  'Una terraza cubierta de {N27.8} {U} a lo largo de todo el ancho de la vivienda.',
  'Une terrasse couverte de {N27.8} {U} sur toute la largeur du logement.',
  'Eine überdachte Terrasse von {N27.8} {U} über die gesamte Breite der Wohnung.',
  'Крытая терраса {N27.8} {U} вдоль всей ширины квартиры.',
  'تراس مغطى مساحته {N27.8} {U} على امتداد عرض المسكن كله.',
  'Een overdekt terras van {N27.8} {U} over de hele breedte van de woning.',
  'Zadaszony taras o powierzchni {N27.8} {U} na całej szerokości lokalu.',
  'En overbygd terrasse på {N27.8} {U} langs hele boligens bredde.',
  'En täckt terrass på {N27.8} {U} längs hela bostadens bredd.')
a('.residences.items[0].points[2]',
  'Una plaza de garaje y un trastero, por {E487500}.', 'Une place de garage et une cave, pour {E487500}.',
  'Ein Garagenstellplatz und ein Abstellraum, für {E487500}.', 'Одно место в гараже и одна кладовая, за {E487500}.',
  'موقف سيارات واحد في المرآب ومخزن واحد، بسعر {E487500}.', 'Eén garageplaats en één berging, voor {E487500}.',
  'Jedno miejsce w garażu i jedna komórka lokatorska, za {E487500}.', 'Én garasjeplass og én bod, for {E487500}.',
  'En garageplats och ett förråd, för {E487500}.')
a('.residences.items[1].points[0]',
  'Vivienda 2-5-1-B, en el bloque 2, portal 5, en la primera planta: dos dormitorios y dos baños, con {N73.6} {U} interiores.',
  'Logement 2-5-1-B, dans le bloc 2, cage 5, au premier étage : deux chambres et deux salles de bain, avec {N73.6} {U} intérieurs.',
  'Wohnung 2-5-1-B, in Block 2, Aufgang 5, im ersten Stock: zwei Schlafzimmer und zwei Bäder, mit {N73.6} {U} Innenfläche.',
  'Квартира 2-5-1-B, блок 2, подъезд 5, первый этаж: две спальни и две ванные комнаты, внутренняя площадь {N73.6} {U}.',
  'المسكن 2-5-1-B، في المبنى 2، المدخل 5، في الطابق الأول: غرفتا نوم وحمامان، بمساحة داخلية {N73.6} {U}.',
  'Woning 2-5-1-B, in blok 2, portiek 5, op de eerste verdieping: twee slaapkamers en twee badkamers, met {N73.6} {U} binnen.',
  'Lokal 2-5-1-B, w bloku 2, klatka 5, na pierwszym piętrze: dwie sypialnie i dwie łazienki, z {N73.6} {U} powierzchni wewnętrznej.',
  'Bolig 2-5-1-B, i hus 2, oppgang 5, i første etasje: to soverom og to bad, med {N73.6} {U} innvendig.',
  'Bostad 2-5-1-B, i hus 2, uppgång 5, på första våningen: två sovrum och två badrum, med {N73.6} {U} inomhus.')
a('.residences.items[1].points[1]',
  'Una terraza cubierta de {N25.5} {U}, una terraza descubierta de {N23.0} {U} y un jardín de {N44.9} {U}.',
  'Une terrasse couverte de {N25.5} {U}, une terrasse découverte de {N23.0} {U} et un jardin de {N44.9} {U}.',
  'Eine überdachte Terrasse von {N25.5} {U}, eine nicht überdachte Terrasse von {N23.0} {U} und ein Garten von {N44.9} {U}.',
  'Крытая терраса {N25.5} {U}, открытая терраса {N23.0} {U} и сад {N44.9} {U}.',
  'تراس مغطى مساحته {N25.5} {U} وتراس مكشوف مساحته {N23.0} {U} وحديقة مساحتها {N44.9} {U}.',
  'Een overdekt terras van {N25.5} {U}, een open terras van {N23.0} {U} en een tuin van {N44.9} {U}.',
  'Zadaszony taras o powierzchni {N25.5} {U}, taras odkryty o powierzchni {N23.0} {U} i ogród o powierzchni {N44.9} {U}.',
  'En overbygd terrasse på {N25.5} {U}, en åpen terrasse på {N23.0} {U} og en hage på {N44.9} {U}.',
  'En täckt terrass på {N25.5} {U}, en öppen terrass på {N23.0} {U} och en trädgård på {N44.9} {U}.')
a('.residences.items[1].points[2]',
  'Una plaza de garaje y un trastero, por {E492000}.', 'Une place de garage et une cave, pour {E492000}.',
  'Ein Garagenstellplatz und ein Abstellraum, für {E492000}.', 'Одно место в гараже и одна кладовая, за {E492000}.',
  'موقف سيارات واحد في المرآب ومخزن واحد، بسعر {E492000}.', 'Eén garageplaats en één berging, voor {E492000}.',
  'Jedno miejsce w garażu i jedna komórka lokatorska, za {E492000}.', 'Én garasjeplass og én bod, for {E492000}.',
  'En garageplats och ett förråd, för {E492000}.')
a('.residences.items[2].name',
  'Una vivienda de tres dormitorios en la sexta planta', 'Un logement de trois chambres au sixième étage',
  'Eine Wohnung mit drei Schlafzimmern im sechsten Stock', 'Квартира с тремя спальнями на шестом этаже',
  'مسكن بثلاث غرف نوم في الطابق السادس', 'Een woning met drie slaapkamers op de zesde verdieping',
  'Lokal z trzema sypialniami na szóstym piętrze', 'En bolig med tre soverom i sjette etasje',
  'En bostad med tre sovrum på sjätte våningen')
a('.residences.items[2].points[0]',
  'Vivienda 1-2-6-B, en el bloque 1, portal 2: tres dormitorios y dos baños, con {N106.0} {U} interiores.',
  'Logement 1-2-6-B, dans le bloc 1, cage 2 : trois chambres et deux salles de bain, avec {N106.0} {U} intérieurs.',
  'Wohnung 1-2-6-B, in Block 1, Aufgang 2: drei Schlafzimmer und zwei Bäder, mit {N106.0} {U} Innenfläche.',
  'Квартира 1-2-6-B, блок 1, подъезд 2: три спальни и две ванные комнаты, внутренняя площадь {N106.0} {U}.',
  'المسكن 1-2-6-B، في المبنى 1، المدخل 2: ثلاث غرف نوم وحمامان، بمساحة داخلية {N106.0} {U}.',
  'Woning 1-2-6-B, in blok 1, portiek 2: drie slaapkamers en twee badkamers, met {N106.0} {U} binnen.',
  'Lokal 1-2-6-B, w bloku 1, klatka 2: trzy sypialnie i dwie łazienki, z {N106.0} {U} powierzchni wewnętrznej.',
  'Bolig 1-2-6-B, i hus 1, oppgang 2: tre soverom og to bad, med {N106.0} {U} innvendig.',
  'Bostad 1-2-6-B, i hus 1, uppgång 2: tre sovrum och två badrum, med {N106.0} {U} inomhus.')
a('.residences.items[2].points[1]',
  'Una terraza descubierta de {N142.9} {U} según la lista de precios, que el plano muestra como {N128.3} y {N4.9} {U}.',
  'Une terrasse découverte de {N142.9} {U} selon la liste de prix, indiquée sur le plan comme {N128.3} et {N4.9} {U}.',
  'Eine nicht überdachte Terrasse von {N142.9} {U} laut Preisliste, auf dem Plan mit {N128.3} und {N4.9} {U} ausgewiesen.',
  'Открытая терраса {N142.9} {U} по прайс-листу; на плане указаны {N128.3} и {N4.9} {U}.',
  'تراس مكشوف مساحته {N142.9} {U} بحسب قائمة الأسعار، ويظهر في المخطط بمساحتي {N128.3} و{N4.9} {U}.',
  'Een open terras van {N142.9} {U} volgens de prijslijst, op de plattegrond aangegeven als {N128.3} en {N4.9} {U}.',
  'Odkryty taras o powierzchni {N142.9} {U} według cennika, na rzucie podany jako {N128.3} i {N4.9} {U}.',
  'En åpen terrasse på {N142.9} {U} ifølge prislisten, vist på planen som {N128.3} og {N4.9} {U}.',
  'En öppen terrass på {N142.9} {U} enligt prislistan, som på planritningen anges som {N128.3} och {N4.9} {U}.')
a('.residences.items[2].points[2]',
  'Una plaza de garaje y un trastero, por {E922000}.', 'Une place de garage et une cave, pour {E922000}.',
  'Ein Garagenstellplatz und ein Abstellraum, für {E922000}.', 'Одно место в гараже и одна кладовая, за {E922000}.',
  'موقف سيارات واحد في المرآب ومخزن واحد، بسعر {E922000}.', 'Eén garageplaats en één berging, voor {E922000}.',
  'Jedno miejsce w garażu i jedna komórka lokatorska, za {E922000}.', 'Én garasjeplass og én bod, for {E922000}.',
  'En garageplats och ett förråd, för {E922000}.')

# ---- lifestyle -----------------------------------------------------------------------------------

a('.lifestyle.headlineHtml',
  'Terrazas, <em>una piscina</em> y una casa club', 'Des terrasses, <em>une piscine</em> et un club-house',
  'Terrassen, <em>ein Pool</em> und ein Clubhaus', 'Террасы, <em>бассейн</em> и клубный дом',
  'تراسات، <em>ومسبح</em> ونادٍ للمجمع', 'Terrassen, <em>een zwembad</em> en een clubhuis',
  'Tarasy, <em>basen</em> i klub mieszkańców', 'Terrasser, <em>et basseng</em> og et klubbhus',
  'Terrasser, <em>en pool</em> och ett klubbhus')
a('.lifestyle.copy',
  'La vida aquí es al aire libre: la terraza o el jardín de la vivienda, la piscina comunitaria, el parque frente a la promoción y la casa club a poca distancia a pie.',
  'La vie ici se passe dehors : la terrasse ou le jardin du logement, la piscine commune, le parc devant l’ensemble et le club-house à quelques pas.',
  'Das Leben hier spielt sich draußen ab: auf der Terrasse oder im Garten der Wohnung, am Gemeinschaftspool, im Park vor der Anlage und im Clubhaus, das nur einen kurzen Spaziergang entfernt liegt.',
  'Жизнь здесь проходит на открытом воздухе: терраса или сад квартиры, общий бассейн, парк перед комплексом и клубный дом в нескольких минутах ходьбы.',
  'الحياة هنا في الهواء الطلق: تراس المسكن أو حديقته، والمسبح المشترك، والحديقة العامة أمام المجمّع، ونادي المجمع على مسافة قصيرة سيرًا.',
  'Het leven hier speelt zich buiten af: het terras of de tuin van de woning, het gemeenschappelijke zwembad, het park voor het complex en het clubhuis op korte loopafstand.',
  'Życie toczy się tu na zewnątrz: taras lub ogród lokalu, wspólny basen, park przed inwestycją i klub mieszkańców w krótkim spacerze.',
  'Livet her er utendørs: terrassen eller hagen til boligen, fellesbassenget, parken foran anlegget og klubbhuset et kort stykke unna til fots.',
  'Livet här är utomhus: bostadens terrass eller trädgård, den gemensamma poolen, parken framför området och klubbhuset en kort promenad bort.')
a('.lifestyle.panels[0][0]',
  'La terraza o el jardín', 'La terrasse ou le jardin', 'Die Terrasse oder der Garten', 'Терраса или сад',
  'التراس أو الحديقة', 'Het terras of de tuin', 'Taras lub ogród', 'Terrassen eller hagen', 'Terrassen eller trädgården')
a('.lifestyle.panels[0][1]',
  'Las tres viviendas de la lista tienen terrazas de {N27.8}, {N48.5} y {N142.9} {U}, y una de ellas tiene un jardín de {N44.9} {U}.',
  'Les trois logements de la liste ont des terrasses de {N27.8}, {N48.5} et {N142.9} {U}, et l’un d’eux a un jardin de {N44.9} {U}.',
  'Die drei Wohnungen auf der Liste haben Terrassen von {N27.8}, {N48.5} und {N142.9} {U}, und eine davon hat einen Garten von {N44.9} {U}.',
  'У трёх квартир из списка террасы {N27.8}, {N48.5} и {N142.9} {U}, а у одной из них есть сад {N44.9} {U}.',
  'للمساكن الثلاثة في القائمة تراسات مساحتها {N27.8} و{N48.5} و{N142.9} {U}، ولأحدها حديقة مساحتها {N44.9} {U}.',
  'De drie woningen op de lijst hebben terrassen van {N27.8}, {N48.5} en {N142.9} {U}, en een ervan heeft een tuin van {N44.9} {U}.',
  'Trzy lokale z listy mają tarasy o powierzchni {N27.8}, {N48.5} i {N142.9} {U}, a jeden z nich ma ogród o powierzchni {N44.9} {U}.',
  'De tre boligene på listen har terrasser på {N27.8}, {N48.5} og {N142.9} {U}, og én av dem har en hage på {N44.9} {U}.',
  'De tre bostäderna på listan har terrasser på {N27.8}, {N48.5} och {N142.9} {U}, och en av dem har en trädgård på {N44.9} {U}.')
a('.lifestyle.panels[1][1]',
  'Una piscina comunitaria con zona de natación, jardines paisajísticos, un gimnasio equipado con zona interior y exterior, una zona deportiva y una zona zen, tal como los enumera el dosier.',
  'Une piscine commune avec une zone de nage, des jardins paysagers, une salle de sport équipée avec un espace intérieur et un espace extérieur, une aire de sport et un espace zen, comme le dossier les énumère.',
  'Ein Gemeinschaftspool mit Schwimmbereich, gestaltete Gärten, ein ausgestatteter Fitnessraum mit Innen- und Außenbereich, ein Sportbereich und ein Zen-Bereich, wie das Dossier sie aufführt.',
  'Общий бассейн с зоной для плавания, ландшафтные сады, оборудованный тренажёрный зал с помещением и площадкой на открытом воздухе, спортивная зона и зона дзен, как их перечисляет досье.',
  'مسبح مشترك بمنطقة للسباحة وحدائق منسّقة وصالة رياضية مجهزة بمنطقة داخلية وأخرى خارجية ومنطقة رياضية ومنطقة زِن، كما يوردها ملف المطوّر.',
  'Een gemeenschappelijk zwembad met een zwemzone, aangelegde tuinen, een uitgeruste fitnessruimte met een binnen- en een buitengedeelte, een sportzone en een zenzone, zoals het dossier ze opsomt.',
  'Wspólny basen ze strefą do pływania, zagospodarowane ogrody, wyposażona siłownia ze strefą wewnętrzną i zewnętrzną, strefa sportowa i strefa zen, tak jak wymienia je dossier.',
  'Et felles svømmebasseng med en svømmesone, anlagte hager, et utstyrt treningsrom med et innendørs og et utendørs område, et sportsområde og et zenområde, slik dossieret lister dem opp.',
  'En gemensam pool med en simzon, anlagda trädgårdar, ett utrustat gym med en inomhus- och en utomhusyta, en idrottsyta och en zenzon, så som dossiern räknar upp dem.')
a('.lifestyle.panels[2][1]',
  'Una casa club para los residentes a 450 m de la promoción, a siete minutos a pie, que el dosier describe como ya abierta, con gimnasio, sauna, spa, vestuarios, una zona de cafetería o restaurante y una terraza elevada con vistas al mar. Es de propiedad compartida mediante una participación que acompaña a la vivienda.',
  'Un club-house réservé aux résidents à 450 m de l’ensemble, à sept minutes à pied, que le dossier décrit comme déjà ouvert, avec une salle de sport, un sauna, un spa, des vestiaires, un espace café ou restaurant et une terrasse surélevée avec vue sur la mer. Il est détenu en copropriété au moyen d’une quote-part qui accompagne le logement.',
  'Ein Clubhaus für die Bewohner, 450 m von der Anlage entfernt, sieben Minuten zu Fuß, das laut Dossier bereits geöffnet ist, mit Fitnessraum, Sauna, Spa, Umkleiden, einem Café- oder Restaurantbereich und einer erhöhten Terrasse mit Meerblick. Es wird gemeinsam besessen über einen Anteil, der zur Wohnung gehört.',
  'Клубный дом для жильцов в 450 м от комплекса, в семи минутах ходьбы; по описанию в досье, он уже открыт; в нём тренажёрный зал, сауна, спа, раздевалки, зона кафе или ресторана и приподнятая терраса с видом на море. Он находится в совместной собственности через долю, которая прилагается к квартире.',
  'نادٍ للسكان على بعد 450 م من المجمّع، أي سبع دقائق سيرًا، يصفه ملف المطوّر بأنه مفتوح بالفعل، وفيه صالة رياضية وساونا وسبا وغرف تبديل الملابس ومنطقة مقهى أو مطعم وتراس مرتفع بإطلالة على البحر. وملكيته مشتركة عبر حصة تأتي مع المسكن.',
  'Een clubhuis voor de bewoners op 450 m van het complex, zeven minuten lopen, dat het dossier beschrijft als al geopend, met een fitnessruimte, een sauna, een spa, kleedkamers, een café- of restaurantgedeelte en een verhoogd terras met uitzicht op zee. Het is gezamenlijk eigendom via een aandeel dat bij de woning hoort.',
  'Klub mieszkańców w odległości 450 m od inwestycji, siedem minut pieszo, który dossier opisuje jako już otwarty, z siłownią, sauną, spa, szatniami, strefą kawiarni lub restauracji i podwyższonym tarasem z widokiem na morze. Jest współwłasnością poprzez udział, który przysługuje wraz z lokalem.',
  'Et klubbhus for beboerne 450 m fra anlegget, sju minutters gange, som dossieret beskriver som allerede åpent, med treningsrom, badstue, spa, garderober, et kafé- eller restaurantområde og en hevet terrasse med havutsikt. Det eies i fellesskap gjennom en andel som følger med boligen.',
  'Ett klubbhus för de boende 450 m från området, sju minuters promenad, som dossiern beskriver som redan öppet, med gym, bastu, spa, omklädningsrum, en kafé- eller restaurangyta och en upphöjd terrass med havsutsikt. Det ägs gemensamt genom en andel som följer med bostaden.')
a('.lifestyle.panels[3][0]',
  'El parque y la ciclosenda', 'Le parc et la piste cyclable', 'Der Park und der Radweg', 'Парк и велодорожка',
  'الحديقة العامة ومسار الدراجات', 'Het park en het fietspad', 'Park i ścieżka rowerowa', 'Parken og sykkelstien', 'Parken och cykelvägen')
a('.lifestyle.panels[3][1]',
  'Un gran parque arbolado se extiende delante de la promoción, y los aparcamientos de bicicletas conectan con la ciclosenda que rodea la parcela.',
  'Un grand parc arboré s’étend devant l’ensemble, et les racks à vélos se raccordent à la piste cyclable qui longe la parcelle.',
  'Vor der Anlage liegt ein großer, baumbestandener Park, und die Fahrradständer sind an den Radweg angebunden, der um das Grundstück führt.',
  'Перед комплексом расположен большой парк с деревьями, а велопарковки соединены с велодорожкой, которая идёт вокруг участка.',
  'تمتد حديقة كبيرة مشجرة أمام المجمّع، وتتصل مواقف الدراجات بمسار الدراجات الذي يحيط بالقطعة.',
  'Voor het complex ligt een groot park met bomen, en de fietsenstallingen sluiten aan op het fietspad dat rond het perceel loopt.',
  'Przed inwestycją rozciąga się duży park z drzewami, a stojaki rowerowe łączą się ze ścieżką rowerową biegnącą wokół działki.',
  'Det ligger en stor, trebevokst park foran anlegget, og sykkelstativene er koblet til sykkelstien som går rundt tomten.',
  'En stor trädplanterad park ligger framför området, och cykelställen ansluter till cykelvägen som går runt tomten.')
a('.lifestyle.panels[4][1]',
  'El dosier enumera nueve campos de golf en un radio de 11 km: Alferini Golf a 2 km, El Paraíso a 5 km, Atalaya a 6 km, y Marbella Golf Club, El Campanario y El Coto a 7 km.',
  'Le dossier énumère neuf golfs dans un rayon de 11 km : Alferini Golf à 2 km, El Paraíso à 5 km, Atalaya à 6 km, et Marbella Golf Club, El Campanario et El Coto à 7 km.',
  'Das Dossier nennt neun Golfplätze im Umkreis von 11 km: Alferini Golf in 2 km, El Paraíso in 5 km, Atalaya in 6 km sowie Marbella Golf Club, El Campanario und El Coto in 7 km.',
  'В досье перечислено девять полей для гольфа в радиусе 11 км: Alferini Golf в 2 км, El Paraíso в 5 км, Atalaya в 6 км, а также Marbella Golf Club, El Campanario и El Coto в 7 км.',
  'يذكر ملف المطوّر تسعة ملاعب غولف في نطاق 11 كم: Alferini Golf على بعد 2 كم، وEl Paraíso على 5 كم، وAtalaya على 6 كم، وMarbella Golf Club وEl Campanario وEl Coto على 7 كم.',
  'Het dossier noemt negen golfbanen binnen 11 km: Alferini Golf op 2 km, El Paraíso op 5 km, Atalaya op 6 km, en Marbella Golf Club, El Campanario en El Coto op 7 km.',
  'Dossier wymienia dziewięć pól golfowych w promieniu 11 km: Alferini Golf w odległości 2 km, El Paraíso 5 km, Atalaya 6 km oraz Marbella Golf Club, El Campanario i El Coto 7 km.',
  'Dossieret nevner ni golfbaner innen 11 km: Alferini Golf på 2 km, El Paraíso på 5 km, Atalaya på 6 km, og Marbella Golf Club, El Campanario og El Coto på 7 km.',
  'Dossiern nämner nio golfbanor inom 11 km: Alferini Golf på 2 km, El Paraíso på 5 km, Atalaya på 6 km, samt Marbella Golf Club, El Campanario och El Coto på 7 km.')

# ---- location ------------------------------------------------------------------------------------

a('.location.copy',
  'Las viviendas están en Cancelada, una zona residencial entre Estepona y Marbella. El dosier del promotor señala que el aeropuerto de Málaga y la estación del tren de alta velocidad están a menos de 45 minutos, da 8 km hasta San Pedro de Alcántara y 58 km hasta el aeropuerto de Gibraltar, y menciona colegios, centros de salud, supermercados y farmacias cerca, un instituto a 190 m y la ciclosenda de Cancelada. Los documentos no dan dirección ni coordenadas de la parcela, por lo que el mapa muestra la zona de Cancelada.',
  'Les logements se trouvent à Cancelada, un quartier résidentiel entre Estepona et Marbella. Le dossier du promoteur indique que l’aéroport de Malaga et la gare du train à grande vitesse sont à moins de 45 minutes, donne 8 km jusqu’à San Pedro de Alcántara et 58 km jusqu’à l’aéroport de Gibraltar, et mentionne à proximité des écoles, des centres de santé, des supermarchés et des pharmacies, un lycée à 190 m et la piste cyclable de Cancelada. Les documents ne donnent ni adresse ni coordonnées de la parcelle ; la carte montre donc le quartier de Cancelada.',
  'Die Wohnungen liegen in Cancelada, einem Wohngebiet zwischen Estepona und Marbella. Das Dossier des Bauträgers gibt an, dass der Flughafen Málaga und der Hochgeschwindigkeitsbahnhof weniger als 45 Minuten entfernt sind, nennt 8 km bis San Pedro de Alcántara und 58 km bis zum Flughafen Gibraltar und erwähnt in der Nähe Schulen, Gesundheitszentren, Supermärkte und Apotheken, eine weiterführende Schule in 190 m Entfernung und den Radweg von Cancelada. Die Unterlagen nennen weder Adresse noch Koordinaten des Grundstücks, daher zeigt die Karte das Gebiet Cancelada.',
  'Квартиры находятся в Канселаде — жилом районе между Эстепоной и Марбельей. В досье застройщика сказано, что до аэропорта Малаги и вокзала скоростных поездов менее 45 минут; указано 8 км до Сан-Педро-де-Алькантара и 58 км до аэропорта Гибралтара; упомянуты поблизости школы, медицинские центры, супермаркеты и аптеки, средняя школа в 190 м и велодорожка Канселады. Адреса и координат участка в документах нет, поэтому на карте показан район Канселады.',
  'تقع المساكن في كانسيلادا، وهي منطقة سكنية بين إستيبونا وماربيا. ويذكر ملف المطوّر أن مطار مالقة ومحطة القطار فائق السرعة على بعد أقل من 45 دقيقة، ويورد 8 كم إلى سان بيدرو دي ألكانتارا و58 كم إلى مطار جبل طارق، ويشير إلى وجود مدارس ومراكز صحية وأسواق كبرى وصيدليات في الجوار، ومدرسة ثانوية على بعد 190 م، ومسار الدراجات في كانسيلادا. ولا تذكر الوثائق عنوانًا للقطعة ولا إحداثيات لها، لذلك تعرض الخريطة منطقة كانسيلادا.',
  'De woningen liggen in Cancelada, een woonwijk tussen Estepona en Marbella. Het dossier van de ontwikkelaar vermeldt dat de luchthaven van Málaga en het station van de hogesnelheidstrein op minder dan 45 minuten liggen, geeft 8 km tot San Pedro de Alcántara en 58 km tot de luchthaven van Gibraltar en noemt in de buurt scholen, gezondheidscentra, supermarkten en apotheken, een middelbare school op 190 m en het fietspad van Cancelada. De documenten geven geen adres of coördinaten van het perceel, dus de kaart toont de wijk Cancelada.',
  'Lokale znajdują się w Cancelada, dzielnicy mieszkalnej między Esteponą a Marbellą. Dossier dewelopera podaje, że lotnisko w Maladze i stacja kolei dużych prędkości są oddalone o mniej niż 45 minut, podaje 8 km do San Pedro de Alcántara i 58 km do lotniska w Gibraltarze oraz wspomina w pobliżu szkoły, ośrodki zdrowia, supermarkety i apteki, liceum w odległości 190 m i ścieżkę rowerową w Cancelada. Dokumenty nie podają adresu ani współrzędnych działki, dlatego mapa pokazuje okolicę Cancelada.',
  'Boligene ligger i Cancelada, et boligområde mellom Estepona og Marbella. Utbyggers dossier oppgir at Málaga lufthavn og høyhastighetstogstasjonen ligger under 45 minutter unna, gir 8 km til San Pedro de Alcántara og 58 km til Gibraltar lufthavn, og nevner skoler, helsesentre, supermarkeder og apotek i nærheten, en videregående skole 190 m unna og sykkelstien i Cancelada. Dokumentene oppgir verken adresse eller koordinater for tomten, så kartet viser området Cancelada.',
  'Bostäderna ligger i Cancelada, ett bostadsområde mellan Estepona och Marbella. Exploatörens dossier anger att Málaga flygplats och höghastighetsstationen ligger under 45 minuter bort, ger 8 km till San Pedro de Alcántara och 58 km till Gibraltars flygplats, och nämner skolor, vårdcentraler, stormarknader och apotek i närheten, en gymnasieskola 190 m bort och cykelvägen i Cancelada. Dokumenten anger varken adress eller koordinater för tomten, så kartan visar området Cancelada.')
a('.location.distances[0][1]', '8 km', '8 km', '8 km', '8 км', '8 كم', '8 km', '8 km', '8 km', '8 km')
same('Alferini Golf')
a('.location.distances[1][1]', '2 km', '2 km', '2 km', '2 км', '2 كم', '2 km', '2 km', '2 km', '2 km')

# ---- investment ----------------------------------------------------------------------------------

a('.investment.copy',
  'Los documentos que tenemos dan un precio para cada vivienda y ninguna condición de pago, por lo que obtenemos las condiciones por escrito antes de que reserve.',
  'Les documents que nous détenons donnent un prix pour chaque logement et aucune modalité de paiement ; nous obtenons donc les conditions par écrit avant que vous ne réserviez.',
  'Die uns vorliegenden Dokumente nennen einen Preis für jede Wohnung und keine Zahlungsbedingungen, daher holen wir die Bedingungen schriftlich ein, bevor Sie reservieren.',
  'В имеющихся у нас документах указана цена каждой квартиры, но нет условий оплаты, поэтому мы получаем условия в письменном виде до того, как вы забронируете.',
  'تذكر الوثائق التي بحوزتنا سعرًا لكل مسكن ولا تذكر شروط دفع، لذلك نحصل على الشروط كتابةً قبل أن تحجزوا.',
  'De documenten die wij hebben geven een prijs voor elke woning en geen betalingsvoorwaarden, dus we verkrijgen de voorwaarden schriftelijk voordat u reserveert.',
  'Posiadane przez nas dokumenty podają cenę każdego lokalu i nie podają warunków płatności, dlatego uzyskujemy te warunki na piśmie przed rezerwacją.',
  'Dokumentene vi har oppgir en pris for hver bolig og ingen betalingsvilkår, så vi innhenter vilkårene skriftlig før dere reserverer.',
  'Dokumenten vi har anger ett pris för varje bostad och inga betalningsvillkor, så vi inhämtar villkoren skriftligen innan ni reserverar.')
a('.investment.cards[0][1]',
  'La lista de precios no indica si el IVA está incluido. Esta página muestra sus precios tal como figuran, y confirmamos por escrito el tratamiento del IVA y los gastos de compra antes de cualquier reserva.',
  'La liste de prix n’indique pas si la TVA est incluse. Cette page reprend ses prix tels qu’ils figurent, et nous confirmons par écrit le régime de TVA et les frais d’achat avant toute réservation.',
  'Die Preisliste gibt nicht an, ob die MwSt. enthalten ist. Diese Seite zeigt ihre Preise wie aufgeführt, und wir bestätigen die MwSt.-Behandlung und die Kaufnebenkosten schriftlich vor jeder Reservierung.',
  'В прайс-листе не сказано, включён ли НДС. На этой странице цены приведены так, как они указаны в списке, а режим НДС и расходы на покупку мы подтверждаем письменно до любого бронирования.',
  'لا تذكر قائمة الأسعار ما إذا كانت ضريبة القيمة المضافة مشمولة. وتعرض هذه الصفحة أسعارها كما وردت، ونؤكد كتابةً معاملة ضريبة القيمة المضافة ومصاريف الشراء قبل أي حجز.',
  'De prijslijst zegt niet of de btw is inbegrepen. Deze pagina toont de prijzen zoals vermeld, en we bevestigen de btw-behandeling en de aankoopkosten schriftelijk vóór een reservering.',
  'Cennik nie podaje, czy VAT jest wliczony. Ta strona pokazuje ceny tak, jak są podane, a sposób traktowania VAT i koszty zakupu potwierdzamy na piśmie przed jakąkolwiek rezerwacją.',
  'Prislisten oppgir ikke om mva. er inkludert. Denne siden viser prisene slik de er oppført, og vi bekrefter mva-behandlingen og kjøpskostnadene skriftlig før enhver reservasjon.',
  'Prislistan anger inte om IVA ingår. Den här sidan visar priserna som de står på listan, och vi bekräftar IVA-behandlingen och köpkostnaderna skriftligen före varje reservation.')
a('.investment.cards[1][1]',
  'Los documentos que tenemos no dan ningún importe de reserva ni calendario de pagos. Pedimos ambos, con las fechas, antes de cualquier reserva.',
  'Les documents que nous détenons ne donnent ni montant de réservation ni échéancier de paiement. Nous demandons les deux, avec les dates, avant toute réservation.',
  'Die uns vorliegenden Dokumente nennen weder einen Reservierungsbetrag noch einen Zahlungsplan. Wir fordern beides samt Terminen vor jeder Reservierung an.',
  'В имеющихся у нас документах нет ни суммы бронирования, ни графика платежей. Мы запрашиваем и то и другое, с датами, до любого бронирования.',
  'لا تذكر الوثائق التي بحوزتنا مبلغ حجز ولا جدول دفعات. نطلب الاثنين مع التواريخ قبل أي حجز.',
  'De documenten die wij hebben geven geen reserveringsbedrag en geen betalingsschema. We vragen beide op, met de data, vóór een reservering.',
  'Posiadane przez nas dokumenty nie podają kwoty rezerwacji ani harmonogramu płatności. Prosimy o oba, wraz z terminami, przed jakąkolwiek rezerwacją.',
  'Dokumentene vi har oppgir verken et reservasjonsbeløp eller en betalingsplan. Vi ber om begge, med datoer, før enhver reservasjon.',
  'Dokumenten vi har anger varken något reservationsbelopp eller någon betalningsplan. Vi ber om båda, med datum, före varje reservation.')
a('.investment.cards[2][1]',
  'El dosier señala que las cantidades entregadas a cuenta están garantizadas conforme a la ley, y que la entidad garante y el aval o la póliza de seguro aún se están gestionando. Pedimos la póliza y los datos de la cuenta antes de cualquier pago.',
  'Le dossier indique que les sommes versées à l’avance sont garanties conformément à la loi, et que l’établissement garant et la caution ou la police d’assurance sont encore en cours de mise en place. Nous demandons la police et les coordonnées du compte avant tout paiement.',
  'Das Dossier gibt an, dass im Voraus gezahlte Beträge gesetzeskonform abgesichert sind und dass das garantierende Institut sowie die Bürgschaft oder Versicherungspolice noch eingerichtet werden. Wir fordern die Police und die Kontodaten vor jeder Zahlung an.',
  'В досье сказано, что суммы, внесённые авансом, гарантируются в соответствии с законом, а гарантирующая организация и банковская гарантия или страховой полис ещё оформляются. Мы запрашиваем полис и реквизиты счёта до любого платежа.',
  'يذكر ملف المطوّر أن المبالغ المدفوعة مقدمًا مضمونة وفق القانون، وأن الجهة الضامنة والكفالة أو بوليصة التأمين لا تزال قيد الترتيب. نطلب الوثيقة وبيانات الحساب قبل أي دفعة.',
  'Het dossier vermeldt dat vooraf betaalde bedragen overeenkomstig de wet gewaarborgd zijn, en dat de garanderende instelling en de bankgarantie of verzekeringspolis nog worden geregeld. We vragen de polis en de rekeninggegevens op vóór enige betaling.',
  'Dossier podaje, że kwoty wpłacone z góry są gwarantowane zgodnie z prawem, a instytucja gwarantująca oraz gwarancja bankowa lub polisa ubezpieczeniowa są jeszcze w trakcie ustalania. Prosimy o polisę i dane rachunku przed jakąkolwiek płatnością.',
  'Dossieret oppgir at beløp betalt på forhånd er garantert i samsvar med loven, og at garantistillende institusjon og bankgarantien eller forsikringspolisen fortsatt er under ordning. Vi ber om polisen og kontodetaljene før enhver betaling.',
  'Dossiern anger att belopp som betalas i förskott garanteras i enlighet med lagen, och att den garanterande institutionen och bankgarantin eller försäkringspolisen fortfarande ordnas. Vi ber om polisen och kontouppgifterna före varje betalning.')
a('.investment.cards[3][1]',
  'La lista de precios muestra una plaza de garaje y un trastero para cada vivienda, y el dosier señala que todas las viviendas tienen ambos. Confirmamos que están incluidos en el precio.',
  'La liste de prix indique une place de garage et une cave pour chaque logement, et le dossier précise que chaque logement a les deux. Nous confirmons qu’ils sont inclus dans le prix.',
  'Die Preisliste weist für jede Wohnung einen Garagenstellplatz und einen Abstellraum aus, und das Dossier gibt an, dass jede Wohnung beides hat. Wir bestätigen, dass sie im Preis enthalten sind.',
  'В прайс-листе для каждой квартиры указаны одно место в гараже и одна кладовая, а в досье сказано, что они есть у каждой квартиры. Мы подтверждаем, что они включены в цену.',
  'تُظهر قائمة الأسعار موقف سيارات واحدًا في المرآب ومخزنًا واحدًا لكل مسكن، ويذكر ملف المطوّر أن لكل مسكن الاثنين. ونؤكد أنهما مشمولان في السعر.',
  'De prijslijst vermeldt voor elke woning één garageplaats en één berging, en het dossier vermeldt dat elke woning beide heeft. We bevestigen dat ze in de prijs zijn inbegrepen.',
  'Cennik podaje dla każdego lokalu jedno miejsce w garażu i jedną komórkę lokatorską, a dossier podaje, że każdy lokal ma jedno i drugie. Potwierdzamy, że są wliczone w cenę.',
  'Prislisten viser én garasjeplass og én bod for hver bolig, og dossieret oppgir at hver bolig har begge deler. Vi bekrefter at de er inkludert i prisen.',
  'Prislistan visar en garageplats och ett förråd för varje bostad, och dossiern anger att varje bostad har båda. Vi bekräftar att de ingår i priset.')

# ---- trust ---------------------------------------------------------------------------------------

a('.trustDossier.cards[0][1]',
  'La lista de precios nombra tres de las 57 viviendas y las marca todas como disponibles. No dice nada de las otras 54, por lo que pedimos la lista completa y el estado de cada vivienda. No lleva más fecha que septiembre de 2026 en el nombre del archivo.',
  'La liste de prix nomme trois des 57 logements et les indique tous trois comme disponibles. Elle ne dit rien des 54 autres ; nous demandons donc la liste complète et le statut de chaque logement. Elle ne porte pas d’autre date que septembre 2026 dans le nom de son fichier.',
  'Die Preisliste nennt drei der 57 Wohnungen und weist alle drei als verfügbar aus. Über die anderen 54 sagt sie nichts, daher fordern wir die vollständige Liste und den Status jeder Wohnung an. Sie trägt kein anderes Datum als September 2026 im Dateinamen.',
  'В прайс-листе названы три из 57 квартир, и все три отмечены как доступные. Об остальных 54 в нём ничего не сказано, поэтому мы запрашиваем полный список и статус каждой квартиры. Кроме сентября 2026 года в названии файла, никакой даты в нём нет.',
  'تذكر قائمة الأسعار ثلاثة من المساكن الـ57 وتضعها جميعًا على أنها متاحة. ولا تقول شيئًا عن الـ54 الأخرى، لذلك نطلب القائمة الكاملة وحالة كل مسكن. ولا تحمل أي تاريخ سوى سبتمبر 2026 في اسم الملف.',
  'De prijslijst noemt drie van de 57 woningen en vermeldt alle drie als beschikbaar. Over de andere 54 zegt ze niets, dus we vragen de volledige lijst en de status van elke woning op. Ze draagt geen andere datum dan september 2026 in de bestandsnaam.',
  'Cennik wymienia trzy z 57 lokali i oznacza wszystkie trzy jako dostępne. Nic nie mówi o pozostałych 54, dlatego prosimy o pełną listę i status każdego lokalu. Nie ma innej daty niż wrzesień 2026 w nazwie pliku.',
  'Prislisten nevner tre av de 57 boligene og markerer alle tre som tilgjengelige. Den sier ingenting om de andre 54, så vi ber om den fullstendige listen og statusen for hver bolig. Den har ingen annen dato enn september 2026 i filnavnet.',
  'Prislistan nämner tre av de 57 bostäderna och markerar alla tre som tillgängliga. Den säger ingenting om de övriga 54, så vi ber om den fullständiga listan och statusen för varje bostad. Den har inget annat datum än september 2026 i filnamnet.')
a('.trustDossier.cards[1][1]',
  'Ninguno de los documentos que tenemos da una fecha de entrega. El dosier indica que se redactó a partir del proyecto básico presentado para obtener la licencia de obras y no dice si la licencia se ha concedido, por lo que pedimos la licencia, el inicio de las obras y la fecha de entrega contractual.',
  'Aucun des documents que nous détenons ne donne de date de livraison. Le dossier indique qu’il a été établi à partir du projet de base déposé pour obtenir le permis de construire, et ne dit pas si le permis a été accordé ; nous demandons donc le permis, le début des travaux et la date de livraison contractuelle.',
  'Keines der uns vorliegenden Dokumente nennt einen Fertigstellungstermin. Das Dossier gibt an, auf Grundlage des Basisprojekts erstellt worden zu sein, das zur Erlangung der Baugenehmigung eingereicht wurde, und sagt nicht, ob die Genehmigung erteilt wurde; daher fordern wir die Genehmigung, den Baubeginn und den vertraglichen Fertigstellungstermin an.',
  'Ни в одном из имеющихся у нас документов не указан срок сдачи. В досье сказано, что оно составлено по базовому проекту, поданному для получения разрешения на строительство, и не сказано, выдано ли разрешение, поэтому мы запрашиваем разрешение, дату начала работ и договорной срок сдачи.',
  'لا تذكر أيٌّ من الوثائق التي بحوزتنا موعدًا للإنجاز. ويذكر ملف المطوّر أنه أُعدّ استنادًا إلى المشروع الأساسي المقدَّم للحصول على رخصة البناء، ولا يذكر ما إذا كانت الرخصة قد مُنحت، لذلك نطلب الرخصة وبدء الأعمال وموعد الإنجاز التعاقدي.',
  'Geen van de documenten die wij hebben geeft een opleveringsdatum. Het dossier vermeldt dat het is opgesteld op basis van het basisproject dat is ingediend om de bouwvergunning te verkrijgen, en zegt niet of de vergunning is verleend, dus we vragen de vergunning, de start van de werken en de contractuele opleveringsdatum op.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu oddania. Dossier podaje, że sporządzono je na podstawie projektu podstawowego złożonego w celu uzyskania pozwolenia na budowę, i nie mówi, czy pozwolenie zostało udzielone, dlatego prosimy o pozwolenie, datę rozpoczęcia prac i umowny termin oddania.',
  'Ingen av dokumentene vi har oppgir en overleveringsdato. Dossieret oppgir at det er utarbeidet på grunnlag av det grunnleggende prosjektet som ble innsendt for å få byggetillatelsen, og sier ikke om tillatelsen er innvilget, så vi ber om tillatelsen, byggestart og den avtalte overleveringsdatoen.',
  'Inget av dokumenten vi har anger ett tillträdesdatum. Dossiern anger att den har utarbetats utifrån det grundprojekt som lämnades in för att få bygglovet, och säger inte om bygglovet har beviljats, så vi ber om bygglovet, byggstarten och det avtalade tillträdesdatumet.')
a('.trustDossier.cards[2][1]',
  'Para las viviendas 1-2-6-B y 2-4-2-B, la lista de precios da superficies construidas de {N121.9} y {N100.6} {U}, mientras que sus planos dan {N150.8} y {N120.9} {U}, la superficie interior más una parte de las zonas comunes. Para la vivienda 2-5-1-B ambos dan {N100.7} {U}. Los planos dan además un segundo conjunto de superficies según el decreto andaluz 218/2005. Confirmamos qué cifras utiliza el contrato.',
  'Pour les logements 1-2-6-B et 2-4-2-B, la liste de prix donne des surfaces construites de {N121.9} et {N100.6} {U}, alors que leurs plans donnent {N150.8} et {N120.9} {U}, soit la surface intérieure plus une quote-part des parties communes. Pour le logement 2-5-1-B, les deux donnent {N100.7} {U}. Les plans donnent en outre un second jeu de surfaces selon le décret andalou 218/2005. Nous confirmons quels chiffres retient le contrat.',
  'Für die Wohnungen 1-2-6-B und 2-4-2-B nennt die Preisliste bebaute Flächen von {N121.9} und {N100.6} {U}, während ihre Pläne {N150.8} und {N120.9} {U} angeben, die Innenfläche zuzüglich eines Anteils an den Gemeinschaftsflächen. Für die Wohnung 2-5-1-B nennen beide {N100.7} {U}. Die Pläne geben außerdem einen zweiten Satz an Flächen nach dem andalusischen Dekret 218/2005 an. Wir bestätigen, welche Zahlen der Vertrag verwendet.',
  'Для квартир 1-2-6-B и 2-4-2-B в прайс-листе указана застроенная площадь {N121.9} и {N100.6} {U}, тогда как в их планах — {N150.8} и {N120.9} {U}: внутренняя площадь плюс доля общих зон. Для квартиры 2-5-1-B оба источника дают {N100.7} {U}. В планах приведён также второй набор площадей по андалусскому декрету 218/2005. Мы подтверждаем, какие цифры использует договор.',
  'بالنسبة إلى المسكنين 1-2-6-B و2-4-2-B تذكر قائمة الأسعار مساحتين مبنيتين هما {N121.9} و{N100.6} {U}، بينما تذكر مخططاتهما {N150.8} و{N120.9} {U}، أي المساحة الداخلية مضافًا إليها حصة من المناطق المشتركة. أما بالنسبة إلى المسكن 2-5-1-B فكلاهما يذكر {N100.7} {U}. وتورد المخططات أيضًا مجموعة ثانية من المساحات بموجب المرسوم الأندلسي 218/2005. ونؤكد أي الأرقام يعتمدها العقد.',
  'Voor de woningen 1-2-6-B en 2-4-2-B geeft de prijslijst bebouwde oppervlakten van {N121.9} en {N100.6} {U}, terwijl hun plattegronden {N150.8} en {N120.9} {U} geven, het binnenoppervlak plus een aandeel in de gemeenschappelijke ruimten. Voor woning 2-5-1-B geven beide {N100.7} {U}. De plattegronden geven bovendien een tweede reeks oppervlakten volgens het Andalusische decreet 218/2005. We bevestigen welke cijfers het contract hanteert.',
  'Dla lokali 1-2-6-B i 2-4-2-B cennik podaje powierzchnie zabudowy {N121.9} i {N100.6} {U}, podczas gdy ich rzuty podają {N150.8} i {N120.9} {U}, czyli powierzchnię wewnętrzną plus udział w częściach wspólnych. Dla lokalu 2-5-1-B oba źródła podają {N100.7} {U}. Rzuty podają ponadto drugi zestaw powierzchni według andaluzyjskiego dekretu 218/2005. Potwierdzamy, jakie liczby przyjmuje umowa.',
  'For boligene 1-2-6-B og 2-4-2-B oppgir prislisten bygde arealer på {N121.9} og {N100.6} {U}, mens planene deres oppgir {N150.8} og {N120.9} {U}, det innvendige arealet pluss en andel av fellesarealene. For bolig 2-5-1-B oppgir begge {N100.7} {U}. Planene oppgir også et andre sett med arealer etter det andalusiske dekretet 218/2005. Vi bekrefter hvilke tall kontrakten bruker.',
  'För bostäderna 1-2-6-B och 2-4-2-B anger prislistan byggytor på {N121.9} och {N100.6} {U}, medan deras planritningar anger {N150.8} och {N120.9} {U}, den invändiga ytan plus en andel av de gemensamma ytorna. För bostad 2-5-1-B anger båda {N100.7} {U}. Planritningarna anger också en andra uppsättning ytor enligt det andalusiska dekretet 218/2005. Vi bekräftar vilka siffror avtalet använder.')
a('.trustDossier.cards[3][1]',
  'El dosier y la memoria de calidades señalan que la compra de una vivienda incluye una participación en la propiedad del edificio de servicios de la casa club, gestionado a través de las comunidades de propietarios. No dicen cuánto añade eso al precio ni a los gastos de comunidad, por lo que lo preguntamos.',
  'Le dossier et le descriptif indiquent que l’achat d’un logement comprend une quote-part de propriété du bâtiment de services du club-house, géré par l’intermédiaire des syndicats de copropriétaires. Ils ne disent pas ce que cela ajoute au prix ni aux charges de copropriété ; nous posons donc la question.',
  'Das Dossier und die Ausstattungsbeschreibung geben an, dass der Kauf einer Wohnung einen Eigentumsanteil am Servicegebäude des Clubhauses einschließt, das über die Eigentümergemeinschaften verwaltet wird. Sie sagen nicht, was das zum Preis oder zu den Gemeinschaftskosten hinzufügt, daher fragen wir nach.',
  'В досье и спецификации сказано, что при покупке квартиры в собственность переходит доля в здании служб клубного дома, которое управляется через ассоциации собственников. Сколько это добавляет к цене и к взносам сообщества собственников, не сказано, поэтому мы спрашиваем.',
  'يذكر ملف المطوّر والمواصفات أن شراء المسكن يشمل حصة ملكية في مبنى الخدمات التابع لنادي المجمع، يُدار عبر اتحادات الملاك. ولا يذكران ما تضيفه هذه الحصة إلى السعر أو إلى رسوم المجمع، لذلك نستفسر عن ذلك.',
  'Het dossier en de specificatie vermelden dat de aankoop van een woning een eigendomsaandeel in het servicegebouw van het clubhuis omvat, dat wordt beheerd via de verenigingen van eigenaars. Ze zeggen niet wat dat aan de prijs of aan de servicekosten toevoegt, dus we vragen het na.',
  'Dossier i specyfikacja podają, że zakup lokalu obejmuje udział we własności budynku usługowego klubu mieszkańców, zarządzanego przez wspólnoty właścicieli. Nie podają, ile to dodaje do ceny ani do opłat wspólnoty, dlatego o to pytamy.',
  'Dossieret og spesifikasjonen oppgir at kjøpet av en bolig omfatter en eierandel i klubbhusets servicebygg, som forvaltes gjennom eierforeningene. De sier ikke hva dette legger til prisen eller til fellesutgiftene, så vi spør om det.',
  'Dossiern och specifikationen anger att köpet av en bostad omfattar en ägarandel i klubbhusets servicebyggnad, som förvaltas genom ägarsamfälligheterna. De säger inte vad detta lägger till priset eller till samfällighetsavgifterna, så vi frågar om det.')
a('.trustDossier.cards[4][0]',
  'La orientación', 'L’orientation', 'Die Ausrichtung', 'Ориентация', 'الاتجاه', 'De oriëntatie', 'Usytuowanie', 'Orienteringen', 'Orienteringen')
a('.trustDossier.cards[4][1]',
  'La lista de precios da la orientación de dos viviendas como oeste y la de la vivienda 2-4-2-B como «NO», que puede interpretarse como noroeste o como ausencia de orientación. La confirmamos con los planos y sobre el terreno.',
  'La liste de prix donne l’orientation de deux logements comme ouest et celle du logement 2-4-2-B comme « NO », qui peut se lire comme nord-ouest ou comme aucune. Nous la confirmons d’après les plans et sur place.',
  'Die Preisliste gibt die Ausrichtung von zwei Wohnungen als West und die der Wohnung 2-4-2-B als „NO“ an, was sich als Nordwest oder als „keine“ lesen lässt. Wir bestätigen sie anhand der Pläne und vor Ort.',
  'В прайс-листе ориентация двух квартир указана как запад, а ориентация квартиры 2-4-2-B — как «NO», что можно прочесть как северо-запад или как отсутствие ориентации. Мы подтверждаем её по планам и на месте.',
  'تذكر قائمة الأسعار اتجاه مسكنين على أنه الغرب واتجاه المسكن 2-4-2-B على أنه «NO»، وهو ما يمكن قراءته شمالًا غربيًا أو انعدام الاتجاه. ونؤكده من المخططات وفي الموقع.',
  'De prijslijst geeft de oriëntatie van twee woningen als west en die van woning 2-4-2-B als „NO”, wat gelezen kan worden als noordwest of als geen. We bevestigen die aan de hand van de plattegronden en ter plaatse.',
  'Cennik podaje usytuowanie dwóch lokali jako zachodnie, a lokalu 2-4-2-B jako „NO”, co można odczytać jako północny zachód lub jako brak. Potwierdzamy je na podstawie rzutów i na miejscu.',
  'Prislisten oppgir orienteringen til to boliger som vest og orienteringen til bolig 2-4-2-B som «NO», som kan leses som nordvest eller som ingen. Vi bekrefter den ut fra planene og på stedet.',
  'Prislistan anger orienteringen för två bostäder som väster och för bostad 2-4-2-B som ”NO”, vilket kan läsas som nordväst eller som ingen. Vi bekräftar den utifrån planritningarna och på plats.')
a('.trustDossier.cards[5][0]',
  'Las imágenes y los planos', 'Les images et les plans', 'Die Bilder und die Pläne', 'Изображения и планы',
  'الصور والمخططات', 'De beelden en de plattegronden', 'Wizualizacje i rzuty', 'Bildene og planene', 'Bilderna och planritningarna')
a('.trustDossier.cards[5][1]',
  'Las imágenes están generadas por ordenador, y los planos son planos en fase de proyecto que el promotor indica que no son definitivos y pueden cambiar por razones técnicas o legales. El mobiliario de las imágenes no está incluido.',
  'Les images sont générées par ordinateur, et les plans sont des plans au stade du projet que le promoteur indique comme non définitifs et susceptibles de changer pour des raisons techniques ou juridiques. Le mobilier des images n’est pas inclus.',
  'Die Bilder sind computergeneriert, und die Pläne sind Projektpläne, die laut Bauträger nicht endgültig sind und sich aus technischen oder rechtlichen Gründen ändern können. Die Möbel auf den Bildern sind nicht enthalten.',
  'Изображения созданы на компьютере, а планы — это проектные планы, которые, по словам застройщика, не являются окончательными и могут измениться по техническим или юридическим причинам. Мебель на изображениях не входит в стоимость.',
  'الصور مولَّدة بالحاسوب، والمخططات مخططات بمرحلة المشروع يقول المطوّر إنها غير نهائية وقد تتغير لأسباب فنية أو قانونية. والأثاث الظاهر في الصور غير مشمول.',
  'De beelden zijn computergegenereerd en de plattegronden zijn projectplannen die volgens de ontwikkelaar niet definitief zijn en om technische of juridische redenen kunnen wijzigen. Het meubilair op de beelden is niet inbegrepen.',
  'Wizualizacje są generowane komputerowo, a rzuty to plany na etapie projektu, które według dewelopera nie są ostateczne i mogą się zmienić z przyczyn technicznych lub prawnych. Meble na wizualizacjach nie są wliczone.',
  'Bildene er datagenererte, og planene er prosjektplaner som utbyggeren sier ikke er endelige og kan endres av tekniske eller juridiske grunner. Møblene på bildene er ikke inkludert.',
  'Bilderna är datorgenererade, och planritningarna är projektplaner som exploatören säger inte är slutgiltiga och kan ändras av tekniska eller juridiska skäl. Möblerna på bilderna ingår inte.')

# ---- availability --------------------------------------------------------------------------------

a('.availability.headlineHtml',
  '3 viviendas <em>disponibles actualmente</em>', '3 logements <em>actuellement disponibles</em>',
  '3 Wohnungen <em>derzeit verfügbar</em>', '3 квартиры <em>сейчас в продаже</em>',
  '3 مساكن <em>متاحة حاليًا</em>', '3 woningen <em>nu beschikbaar</em>',
  '3 lokale <em>obecnie dostępne</em>', '3 boliger <em>tilgjengelige nå</em>',
  '3 bostäder <em>tillgängliga just nu</em>')
a('.availability.copy',
  'Los precios son los de la lista de precios del promotor, cuyo nombre de archivo indica septiembre de 2026, y confirmamos precios y disponibilidad antes de cualquier reserva. La lista nombra 3 de las 57 viviendas y muestra cada una como disponible. No dice si el IVA está incluido.',
  'Les prix sont ceux de la liste de prix du promoteur, dont le nom de fichier indique septembre 2026, et nous confirmons prix et disponibilité avant toute réservation. La liste nomme 3 des 57 logements et indique chacun comme disponible. Elle ne dit pas si la TVA est incluse.',
  'Die Preise sind die der Preisliste des Bauträgers, deren Dateiname September 2026 nennt, und wir bestätigen Preise und Verfügbarkeit vor jeder Reservierung. Die Liste nennt 3 der 57 Wohnungen und weist jede als verfügbar aus. Sie gibt nicht an, ob die MwSt. enthalten ist.',
  'Цены взяты из прайс-листа застройщика, в названии файла которого указан сентябрь 2026 года; цены и наличие мы подтверждаем до любого бронирования. В списке названы 3 из 57 квартир, и каждая показана как доступная. В нём не сказано, включён ли НДС.',
  'الأسعار هي أسعار قائمة المطوّر التي يشير اسم ملفها إلى سبتمبر 2026، ونؤكد الأسعار والتوافر قبل أي حجز. تذكر القائمة 3 من المساكن الـ57 وتُظهر كلًّا منها متاحًا. ولا تذكر ما إذا كانت ضريبة القيمة المضافة مشمولة.',
  'De prijzen zijn die van de prijslijst van de ontwikkelaar, waarvan de bestandsnaam september 2026 vermeldt, en we bevestigen prijzen en beschikbaarheid vóór een reservering. De lijst noemt 3 van de 57 woningen en toont elke woning als beschikbaar. Ze zegt niet of de btw is inbegrepen.',
  'Ceny pochodzą z cennika dewelopera, w którego nazwie pliku widnieje wrzesień 2026, a ceny i dostępność potwierdzamy przed jakąkolwiek rezerwacją. Cennik wymienia 3 z 57 lokali i pokazuje każdy jako dostępny. Nie podaje, czy VAT jest wliczony.',
  'Prisene er de i utbyggers prisliste, der filnavnet oppgir september 2026, og vi bekrefter priser og tilgjengelighet før enhver reservasjon. Listen nevner 3 av de 57 boligene og viser hver som tilgjengelig. Den oppgir ikke om mva. er inkludert.',
  'Priserna är de i exploatörens prislista, vars filnamn anger september 2026, och vi bekräftar priser och tillgänglighet före varje reservation. Listan nämner 3 av de 57 bostäderna och visar var och en som tillgänglig. Den anger inte om IVA ingår.')
a('.availability.sourceNote',
  'Los precios y las superficies están transcritos de la lista de precios del promotor, que no lleva más fecha que septiembre de 2026 en el nombre del archivo, nombra 3 de las 57 viviendas con su precio y muestra cada una como disponible. La lista no dice si el IVA está incluido. Cada vivienda figura con una plaza de garaje y un trastero. La tabla muestra las superficies interiores y las terrazas, en las que la lista y los planos coinciden, y omite la superficie construida, en la que no coinciden: la lista da {N121.9} {U} para 1-2-6-B y {N100.6} {U} para 2-4-2-B, donde los planos dan {N150.8} y {N120.9} {U}, y {N100.7} {U} para 2-5-1-B, donde ambos coinciden. La terraza que se muestra para 2-5-1-B es la terraza cubierta de {N25.5} {U} y la descubierta de {N23.0} {U} juntas, con un jardín de {N44.9} {U}. La terraza de 1-2-6-B es de {N142.9} {U} en la lista y de {N142.8} {U} en la tabla de superficies del plano, cuyas estancias indican {N128.3} y {N4.9} {U}.',
  'Les prix et les surfaces sont transcrits de la liste de prix du promoteur, qui ne porte pas d’autre date que septembre 2026 dans le nom de son fichier, nomme 3 des 57 logements avec un prix et indique chacun comme disponible. La liste ne dit pas si la TVA est incluse. Chaque logement figure avec une place de garage et une cave. Le tableau présente les surfaces intérieures et les terrasses, sur lesquelles la liste et les plans concordent, et omet la surface construite, sur laquelle ils divergent : la liste donne {N121.9} {U} pour 1-2-6-B et {N100.6} {U} pour 2-4-2-B, là où les plans donnent {N150.8} et {N120.9} {U}, et {N100.7} {U} pour 2-5-1-B, où les deux concordent. La terrasse indiquée pour 2-5-1-B est la terrasse couverte de {N25.5} {U} et la terrasse découverte de {N23.0} {U} réunies, avec un jardin de {N44.9} {U}. La terrasse de 1-2-6-B est de {N142.9} {U} dans la liste et de {N142.8} {U} dans le tableau des surfaces du plan, dont les pièces indiquent {N128.3} et {N4.9} {U}.',
  'Preise und Flächen sind der Preisliste des Bauträgers entnommen, die kein anderes Datum als September 2026 im Dateinamen trägt, 3 der 57 Wohnungen mit Preis nennt und jede als verfügbar ausweist. Die Liste gibt nicht an, ob die MwSt. enthalten ist. Jede Wohnung ist mit einem Garagenstellplatz und einem Abstellraum aufgeführt. Die Tabelle zeigt Innenflächen und Terrassen, bei denen Liste und Pläne übereinstimmen, und lässt die bebaute Fläche weg, bei der sie abweichen: Die Liste nennt {N121.9} {U} für 1-2-6-B und {N100.6} {U} für 2-4-2-B, wo die Pläne {N150.8} und {N120.9} {U} angeben, und {N100.7} {U} für 2-5-1-B, wo beide übereinstimmen. Die für 2-5-1-B gezeigte Terrasse ist die überdachte Terrasse von {N25.5} {U} und die nicht überdachte von {N23.0} {U} zusammen, mit einem Garten von {N44.9} {U}. Die Terrasse von 1-2-6-B hat laut Liste {N142.9} {U} und laut Flächentabelle des Plans {N142.8} {U}, dessen Räume {N128.3} und {N4.9} {U} ausweisen.',
  'Цены и площади перенесены из прайс-листа застройщика, в котором нет иной даты, кроме сентября 2026 года в названии файла; в нём названы 3 из 57 квартир с ценой, и каждая показана как доступная. В списке не сказано, включён ли НДС. Для каждой квартиры указаны одно место в гараже и одна кладовая. В таблице приведены внутренние площади и террасы, по которым список и планы совпадают, и опущена застроенная площадь, по которой они расходятся: в списке {N121.9} {U} для 1-2-6-B и {N100.6} {U} для 2-4-2-B, тогда как в планах {N150.8} и {N120.9} {U}, и {N100.7} {U} для 2-5-1-B, где оба источника совпадают. Терраса, показанная для 2-5-1-B, — это крытая терраса {N25.5} {U} и открытая терраса {N23.0} {U} вместе, с садом {N44.9} {U}. Терраса квартиры 1-2-6-B составляет {N142.9} {U} по списку и {N142.8} {U} в таблице площадей плана, где в экспликации помещений указаны {N128.3} и {N4.9} {U}.',
  'الأسعار والمساحات منقولة من قائمة أسعار المطوّر التي لا تحمل تاريخًا سوى سبتمبر 2026 في اسم ملفها، وتذكر 3 من المساكن الـ57 مع سعرها وتُظهر كلًّا منها متاحًا. ولا تذكر القائمة ما إذا كانت ضريبة القيمة المضافة مشمولة. ويرد لكل مسكن موقف سيارات واحد في المرآب ومخزن واحد. ويعرض الجدول المساحات الداخلية والتراسات، وهي التي تتفق عليها القائمة والمخططات، ويستبعد المساحة المبنية التي لا تتفقان عليها: تذكر القائمة {N121.9} {U} للمسكن 1-2-6-B و{N100.6} {U} للمسكن 2-4-2-B بينما تذكر المخططات {N150.8} و{N120.9} {U}، و{N100.7} {U} للمسكن 2-5-1-B حيث يتفق الاثنان. والتراس المعروض للمسكن 2-5-1-B هو التراس المغطى البالغ {N25.5} {U} والتراس المكشوف البالغ {N23.0} {U} معًا، مع حديقة مساحتها {N44.9} {U}. وتراس المسكن 1-2-6-B مساحته {N142.9} {U} في القائمة و{N142.8} {U} في جدول المساحات بالمخطط، الذي تذكر غرفه {N128.3} و{N4.9} {U}.',
  'Prijzen en oppervlakten zijn overgenomen uit de prijslijst van de ontwikkelaar, die geen andere datum draagt dan september 2026 in de bestandsnaam, 3 van de 57 woningen met een prijs noemt en elke woning als beschikbaar toont. De lijst zegt niet of de btw is inbegrepen. Elke woning staat vermeld met één garageplaats en één berging. De tabel toont binnenoppervlakten en terrassen, waarover de lijst en de plattegronden het eens zijn, en laat het bebouwde oppervlak weg, waarover ze het oneens zijn: de lijst geeft {N121.9} {U} voor 1-2-6-B en {N100.6} {U} voor 2-4-2-B, waar de plattegronden {N150.8} en {N120.9} {U} geven, en {N100.7} {U} voor 2-5-1-B, waar beide overeenkomen. Het getoonde terras voor 2-5-1-B is het overdekte terras van {N25.5} {U} en het open terras van {N23.0} {U} samen, met een tuin van {N44.9} {U}. Het terras van 1-2-6-B is {N142.9} {U} volgens de lijst en {N142.8} {U} in de oppervlaktetabel van de plattegrond, waarvan de ruimten {N128.3} en {N4.9} {U} vermelden.',
  'Ceny i powierzchnie przepisano z cennika dewelopera, który nie ma innej daty niż wrzesień 2026 w nazwie pliku, wymienia 3 z 57 lokali z ceną i pokazuje każdy jako dostępny. Cennik nie podaje, czy VAT jest wliczony. Każdy lokal jest podany z jednym miejscem w garażu i jedną komórką lokatorską. Tabela pokazuje powierzchnie wewnętrzne i tarasy, co do których cennik i rzuty są zgodne, i pomija powierzchnię zabudowy, co do której się różnią: cennik podaje {N121.9} {U} dla 1-2-6-B i {N100.6} {U} dla 2-4-2-B, gdzie rzuty podają {N150.8} i {N120.9} {U}, oraz {N100.7} {U} dla 2-5-1-B, gdzie oba źródła się zgadzają. Taras pokazany dla 2-5-1-B to taras zadaszony o powierzchni {N25.5} {U} i taras odkryty o powierzchni {N23.0} {U} razem, z ogrodem o powierzchni {N44.9} {U}. Taras lokalu 1-2-6-B ma {N142.9} {U} według cennika i {N142.8} {U} w tabeli powierzchni na rzucie, w której pomieszczenia mają {N128.3} i {N4.9} {U}.',
  'Prisene og arealene er hentet fra utbyggers prisliste, som ikke har noen annen dato enn september 2026 i filnavnet, nevner 3 av de 57 boligene med pris og viser hver som tilgjengelig. Listen oppgir ikke om mva. er inkludert. Hver bolig er oppført med én garasjeplass og én bod. Tabellen viser innvendige arealer og terrasser, som listen og planene er enige om, og utelater bygd areal, som de ikke er enige om: listen oppgir {N121.9} {U} for 1-2-6-B og {N100.6} {U} for 2-4-2-B, der planene oppgir {N150.8} og {N120.9} {U}, og {N100.7} {U} for 2-5-1-B, der begge stemmer. Terrassen som vises for 2-5-1-B er den overbygde terrassen på {N25.5} {U} og den åpne terrassen på {N23.0} {U} til sammen, med en hage på {N44.9} {U}. Terrassen til 1-2-6-B er {N142.9} {U} ifølge listen og {N142.8} {U} i planens arealtabell, der rommene oppgir {N128.3} og {N4.9} {U}.',
  'Priser och ytor är hämtade ur exploatörens prislista, som inte har något annat datum än september 2026 i filnamnet, nämner 3 av de 57 bostäderna med pris och visar var och en som tillgänglig. Listan anger inte om IVA ingår. Varje bostad anges med en garageplats och ett förråd. Tabellen visar invändiga ytor och terrasser, som listan och planritningarna är överens om, och utelämnar byggytan, som de inte är överens om: listan anger {N121.9} {U} för 1-2-6-B och {N100.6} {U} för 2-4-2-B, där planritningarna anger {N150.8} och {N120.9} {U}, och {N100.7} {U} för 2-5-1-B, där båda stämmer. Terrassen som visas för 2-5-1-B är den täckta terrassen på {N25.5} {U} och den öppna terrassen på {N23.0} {U} tillsammans, med en trädgård på {N44.9} {U}. Terrassen för 1-2-6-B är {N142.9} {U} enligt listan och {N142.8} {U} i planritningens ytetabell, vars rum anger {N128.3} och {N4.9} {U}.')

# ---- enquiry, FAQ, SEO ---------------------------------------------------------------------------

for key in ('.enquiry.headlineHtml', '.enquiry.message'):
    en = get(key)
    src = en.replace('Aire Estepona', 'Levante Residences')
    assert src in tm, src
    T[en] = {l: tm[src][l].replace('Levante Residences', 'Aire Estepona') for l in LOCS}

a('.faq[0][1]',
  'La promoción tiene 57 viviendas de dos o tres dormitorios en dos bloques. La lista de precios nombra tres, todas disponibles: viviendas de tres dormitorios por {E487500} y {E922000} y una vivienda de dos dormitorios con jardín por {E492000}.',
  'L’ensemble compte 57 logements de deux ou trois chambres répartis en deux blocs. La liste de prix en nomme trois, tous disponibles : des logements de trois chambres à {E487500} et {E922000} et un logement de deux chambres avec jardin à {E492000}.',
  'Die Anlage hat 57 Wohnungen mit zwei oder drei Schlafzimmern in zwei Blöcken. Die Preisliste nennt drei davon, alle verfügbar: Wohnungen mit drei Schlafzimmern für {E487500} und {E922000} sowie eine Wohnung mit zwei Schlafzimmern und Garten für {E492000}.',
  'В комплексе 57 квартир с двумя или тремя спальнями в двух блоках. В прайс-листе названы три из них, все доступны: квартиры с тремя спальнями за {E487500} и {E922000} и квартира с двумя спальнями и садом за {E492000}.',
  'يضم المجمّع 57 مسكنًا بغرفتي نوم أو ثلاث غرف نوم في مبنيين. وتذكر قائمة الأسعار ثلاثة منها، وكلها متاحة: مسكنان بثلاث غرف نوم بسعر {E487500} و{E922000} ومسكن بغرفتي نوم مع حديقة بسعر {E492000}.',
  'Het complex heeft 57 woningen met twee of drie slaapkamers in twee blokken. De prijslijst noemt er drie, allemaal beschikbaar: woningen met drie slaapkamers voor {E487500} en {E922000} en een woning met twee slaapkamers en tuin voor {E492000}.',
  'Inwestycja obejmuje 57 lokali z dwiema lub trzema sypialniami w dwóch blokach. Cennik wymienia trzy z nich, wszystkie dostępne: lokale z trzema sypialniami za {E487500} i {E922000} oraz lokal z dwiema sypialniami i ogrodem za {E492000}.',
  'Anlegget har 57 boliger med to eller tre soverom i to blokker. Prislisten nevner tre av dem, alle tilgjengelige: boliger med tre soverom til {E487500} og {E922000} og en bolig med to soverom og hage til {E492000}.',
  'Området har 57 bostäder med två eller tre sovrum i två hus. Prislistan nämner tre av dem, alla tillgängliga: bostäder med tre sovrum för {E487500} och {E922000} och en bostad med två sovrum och trädgård för {E492000}.')
a('.faq[1][1]',
  'La lista de precios no lo dice. Confirmamos por escrito el tratamiento del IVA y los gastos de compra antes de cualquier reserva.',
  'La liste de prix ne le dit pas. Nous confirmons par écrit le régime de TVA et les frais d’achat avant toute réservation.',
  'Die Preisliste gibt das nicht an. Wir bestätigen die MwSt.-Behandlung und die Kaufnebenkosten schriftlich vor jeder Reservierung.',
  'В прайс-листе этого не сказано. Режим НДС и расходы на покупку мы подтверждаем письменно до любого бронирования.',
  'لا تذكر قائمة الأسعار ذلك. ونؤكد كتابةً معاملة ضريبة القيمة المضافة ومصاريف الشراء قبل أي حجز.',
  'De prijslijst zegt dat niet. We bevestigen de btw-behandeling en de aankoopkosten schriftelijk vóór een reservering.',
  'Cennik tego nie podaje. Sposób traktowania VAT i koszty zakupu potwierdzamy na piśmie przed jakąkolwiek rezerwacją.',
  'Prislisten oppgir det ikke. Vi bekrefter mva-behandlingen og kjøpskostnadene skriftlig før enhver reservasjon.',
  'Prislistan anger det inte. Vi bekräftar IVA-behandlingen och köpkostnaderna skriftligen före varje reservation.')
a('.faq[2][1]',
  'La lista de precios muestra una plaza de garaje y un trastero para cada vivienda recogida, y el dosier señala que todas las viviendas tienen ambos. Confirmamos que están incluidos en el precio.',
  'La liste de prix indique une place de garage et une cave pour chaque logement répertorié, et le dossier précise que chaque logement a les deux. Nous confirmons qu’ils sont inclus dans le prix.',
  'Die Preisliste weist für jede aufgeführte Wohnung einen Garagenstellplatz und einen Abstellraum aus, und das Dossier gibt an, dass jede Wohnung beides hat. Wir bestätigen, dass sie im Preis enthalten sind.',
  'В прайс-листе для каждой квартиры из списка указаны одно место в гараже и одна кладовая, а в досье сказано, что они есть у каждой квартиры. Мы подтверждаем, что они включены в цену.',
  'تُظهر قائمة الأسعار موقف سيارات واحدًا في المرآب ومخزنًا واحدًا لكل مسكن مدرج، ويذكر ملف المطوّر أن لكل مسكن الاثنين. ونؤكد أنهما مشمولان في السعر.',
  'De prijslijst vermeldt voor elke woning op de lijst één garageplaats en één berging, en het dossier vermeldt dat elke woning beide heeft. We bevestigen dat ze in de prijs zijn inbegrepen.',
  'Cennik podaje dla każdego lokalu z listy jedno miejsce w garażu i jedną komórkę lokatorską, a dossier podaje, że każdy lokal ma jedno i drugie. Potwierdzamy, że są wliczone w cenę.',
  'Prislisten viser én garasjeplass og én bod for hver bolig på listen, og dossieret oppgir at hver bolig har begge deler. Vi bekrefter at de er inkludert i prisen.',
  'Prislistan visar en garageplats och ett förråd för varje bostad på listan, och dossiern anger att varje bostad har båda. Vi bekräftar att de ingår i priset.')
a('.faq[3][1]',
  'Ninguno de los documentos que tenemos da una fecha de entrega ni el estado de la licencia. Pedimos la licencia y la fecha contractual.',
  'Aucun des documents que nous détenons ne donne de date de livraison ni l’état du permis. Nous demandons le permis et la date contractuelle.',
  'Keines der uns vorliegenden Dokumente nennt einen Fertigstellungstermin oder den Stand der Genehmigung. Wir fordern die Genehmigung und den vertraglichen Termin an.',
  'Ни в одном из имеющихся у нас документов не указаны срок сдачи и статус разрешения на строительство. Мы запрашиваем разрешение и договорной срок.',
  'لا تذكر أيٌّ من الوثائق التي بحوزتنا موعد إنجاز ولا وضع الرخصة. نطلب الرخصة والموعد التعاقدي.',
  'Geen van de documenten die wij hebben geeft een opleveringsdatum of de status van de vergunning. We vragen de vergunning en de contractuele datum op.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu oddania ani statusu pozwolenia. Prosimy o pozwolenie i umowny termin.',
  'Ingen av dokumentene vi har oppgir en overleveringsdato eller status for tillatelsen. Vi ber om tillatelsen og den avtalte datoen.',
  'Inget av dokumenten vi har anger ett tillträdesdatum eller bygglovets status. Vi ber om bygglovet och det avtalade datumet.')
a('.faq[4][1]',
  'Los documentos que tenemos no dan ninguno. Pedimos por escrito el importe de la reserva y las fechas de los plazos.',
  'Les documents que nous détenons n’en donnent aucune. Nous demandons par écrit le montant de la réservation et les dates des échéances.',
  'Die uns vorliegenden Dokumente nennen keine. Wir fordern den Reservierungsbetrag und die Termine der Raten schriftlich an.',
  'В имеющихся у нас документах таких условий нет. Мы запрашиваем в письменном виде сумму бронирования и даты платежей.',
  'لا تذكر الوثائق التي بحوزتنا أيًّا منها. نطلب كتابةً مبلغ الحجز وتواريخ الدفعات.',
  'De documenten die wij hebben geven er geen. We vragen het reserveringsbedrag en de data van de termijnen schriftelijk op.',
  'Posiadane przez nas dokumenty ich nie podają. Prosimy na piśmie o kwotę rezerwacji i terminy rat.',
  'Dokumentene vi har oppgir ingen. Vi ber skriftlig om reservasjonsbeløpet og datoene for delbetalingene.',
  'Dokumenten vi har anger inga. Vi ber skriftligen om reservationsbeloppet och datumen för delbetalningarna.')
a('.faq[5][1]',
  'Una piscina comunitaria, un gimnasio equipado, una zona deportiva y zen exterior y jardines paisajísticos, además de una casa club con spa, sauna, gimnasio y salas comunitarias que, según los documentos, se adquiere junto con la vivienda.',
  'Une piscine commune, une salle de sport équipée, un espace sportif et zen extérieur et des jardins paysagers, ainsi qu’un club-house avec spa, sauna, salle de sport et salles communes que, selon les documents, l’on acquiert avec le logement.',
  'Ein Gemeinschaftspool, ein ausgestatteter Fitnessraum, ein Sport- und Zen-Bereich im Freien und gestaltete Gärten, dazu ein Clubhaus mit Spa, Sauna, Fitnessraum und Gemeinschaftsräumen, das laut den Unterlagen zusammen mit der Wohnung erworben wird.',
  'Общий бассейн, оборудованный тренажёрный зал, спортивная зона и зона дзен на открытом воздухе и ландшафтные сады, а также клубный дом со спа, сауной, тренажёрным залом и общими помещениями, который, согласно документам, приобретается вместе с квартирой.',
  'مسبح مشترك وصالة رياضية مجهزة ومنطقة رياضية ومنطقة زِن خارجية وحدائق منسّقة، إضافة إلى نادٍ للمجمع فيه سبا وساونا وصالة رياضية وقاعات مشتركة، تقول الوثائق إنه يُشترى مع المسكن.',
  'Een gemeenschappelijk zwembad, een uitgeruste fitnessruimte, een sport- en zenzone buiten en aangelegde tuinen, plus een clubhuis met spa, sauna, fitnessruimte en gemeenschappelijke ruimtes dat volgens de documenten samen met de woning wordt gekocht.',
  'Wspólny basen, wyposażona siłownia, plenerowa strefa sportu i zen oraz zagospodarowane ogrody, a także klub mieszkańców ze spa, sauną, siłownią i salami wspólnymi, który według dokumentów kupuje się razem z lokalem.',
  'Et felles basseng, et utstyrt treningsrom, et utendørs sports- og zenområde og anlagte hager, pluss et klubbhus med spa, badstue, treningsrom og fellesrom som ifølge dokumentene kjøpes sammen med boligen.',
  'En gemensam pool, ett utrustat gym, en utomhusyta för sport och zen och anlagda trädgårdar, plus ett klubbhus med spa, bastu, gym och gemensamma rum som enligt dokumenten köps tillsammans med bostaden.')
a('.seo.title',
  'Aire Estepona - Viviendas con terrazas en Cancelada', 'Aire Estepona - Logements avec terrasses à Cancelada',
  'Aire Estepona - Wohnungen mit Terrassen in Cancelada', 'Aire Estepona - квартиры с террасами в Канселаде',
  'Aire Estepona - مساكن بتراسات في كانسيلادا', 'Aire Estepona - Woningen met terrassen in Cancelada',
  'Aire Estepona - lokale z tarasami w Cancelada', 'Aire Estepona - Boliger med terrasser i Cancelada',
  'Aire Estepona - Bostäder med terrasser i Cancelada')
a('.seo.h1',
  'Aire Estepona: viviendas con terrazas y jardines en Cancelada, Estepona', 'Aire Estepona : logements avec terrasses et jardins à Cancelada, Estepona',
  'Aire Estepona: Wohnungen mit Terrassen und Gärten in Cancelada, Estepona', 'Aire Estepona: квартиры с террасами и садами в Канселаде, Эстепона',
  'Aire Estepona: مساكن بتراسات وحدائق في كانسيلادا، إستيبونا', 'Aire Estepona: woningen met terrassen en tuinen in Cancelada, Estepona',
  'Aire Estepona: lokale z tarasami i ogrodami w Cancelada, Estepona', 'Aire Estepona: boliger med terrasser og hager i Cancelada, Estepona',
  'Aire Estepona: bostäder med terrasser och trädgårdar i Cancelada, Estepona')
a('.seo.h1Context',
  'Viviendas con terrazas y jardines en Cancelada, Estepona', 'Logements avec terrasses et jardins à Cancelada, Estepona',
  'Wohnungen mit Terrassen und Gärten in Cancelada, Estepona', 'Квартиры с террасами и садами в Канселаде, Эстепона',
  'مساكن بتراسات وحدائق في كانسيلادا، إستيبونا', 'Woningen met terrassen en tuinen in Cancelada, Estepona',
  'Lokale z tarasami i ogrodami w Cancelada, Estepona', 'Boliger med terrasser og hager i Cancelada, Estepona',
  'Bostäder med terrasser och trädgårdar i Cancelada, Estepona')

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings to', f'{SP}/tr_a.json')
