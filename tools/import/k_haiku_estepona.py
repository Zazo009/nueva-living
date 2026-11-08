# -*- coding: utf-8 -*-
"""Haiku Estepona: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_h.json keyed by the English string, as assemble.py expects. Tokens: {E505000}
money, {N94.15} decimal number, {U} the area unit.
    python3 tools/import/k_haiku_estepona.py <scratch dir>      (writes <dir>/tr_h.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/haiku-estepona/project.json'))


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


# render prefix per locale: the description that follows carries its own connector (de, d’, van, av ...)
CGP = {'es': 'Vista generada por ordenador ', 'fr': 'Vue générée par ordinateur ', 'de': 'Computergenerierte Ansicht ',
       'ru': 'Компьютерная визуализация ', 'ar': 'منظر مولَّد بالحاسوب ', 'nl': 'Computergegenereerd beeld ',
       'pl': 'Wygenerowany komputerowo widok ', 'no': 'Datagenerert bilde ', 'sv': 'Datorgenererad vy '}


def cg(path, *tr):
    assert len(tr) == 9, path
    en = get(path)
    assert en.startswith('Computer-generated view of '), en
    put(en, [CGP[l] + t for l, t in zip(LOCS, tr)])


same('Haiku Estepona'); same('Haiku <em>Estepona</em>')

# ---- description, SEO, hero, card -------------------------------------------------------------

a('.description',
  '23 de las 51 viviendas de Haiku Estepona, un complejo de apartamentos y adosados en Cancelada, en la Nueva Milla de Oro de Estepona: 13 apartamentos de dos dormitorios desde {E505000} y 10 adosados de tres dormitorios desde {E962000}, más IVA. No se indica fecha de entrega.',
  '23 des 51 logements de Haiku Estepona, un ensemble d’appartements et de maisons mitoyennes à Cancelada, sur la New Golden Mile d’Estepona : 13 appartements de deux chambres à partir de {E505000} et 10 maisons mitoyennes de trois chambres à partir de {E962000}, hors TVA. Aucune date de livraison n’est indiquée.',
  '23 von 51 Immobilien in Haiku Estepona, einer Anlage mit Wohnungen und Reihenhäusern in Cancelada an der New Golden Mile von Estepona: 13 Wohnungen mit zwei Schlafzimmern ab {E505000} und 10 Reihenhäuser mit drei Schlafzimmern ab {E962000}, zuzüglich MwSt. Ein Fertigstellungstermin ist nicht angegeben.',
  '23 из 51 объекта в Haiku Estepona — комплексе квартир и таунхаусов в Канселаде, на Новой Золотой миле Эстепоны: 13 квартир с двумя спальнями от {E505000} и 10 таунхаусов с тремя спальнями от {E962000} без НДС. Срок сдачи не указан.',
  '23 من أصل 51 مسكنًا في Haiku Estepona، وهو مجمّع من الشقق والمنازل المتلاصقة في كانسيلادا، على الميل الذهبي الجديد في إستيبونا: 13 شقة بغرفتي نوم ابتداءً من {E505000} و10 منازل متلاصقة بثلاث غرف نوم ابتداءً من {E962000}، دون ضريبة القيمة المضافة. لم يُذكر موعد إنجاز.',
  '23 van de 51 woningen in Haiku Estepona, een complex met appartementen en herenhuizen in Cancelada, aan de New Golden Mile van Estepona: 13 appartementen met twee slaapkamers vanaf {E505000} en 10 herenhuizen met drie slaapkamers vanaf {E962000}, excl. btw. Er wordt geen opleveringsdatum genoemd.',
  '23 z 51 lokali w Haiku Estepona, kompleksie mieszkań i domów szeregowych w Cancelada, na New Golden Mile w Esteponie: 13 mieszkań z dwiema sypialniami od {E505000} i 10 domów szeregowych z trzema sypialniami od {E962000}, plus VAT. Termin oddania nie jest podany.',
  '23 av 51 boliger i Haiku Estepona, et anlegg med leiligheter og rekkehus i Cancelada, på New Golden Mile i Estepona: 13 leiligheter med to soverom fra {E505000} og 10 rekkehus med tre soverom fra {E962000}, pluss mva. Ingen overleveringsdato er oppgitt.',
  '23 av 51 bostäder i Haiku Estepona, ett område med lägenheter och radhus i Cancelada, på New Golden Mile i Estepona: 13 lägenheter med två sovrum från {E505000} och radhus med tre sovrum från {E962000}, plus IVA (spansk moms). Inget tillträdesdatum anges.')
a('.seoDescription',
  '23 de 51 apartamentos y adosados en Haiku Estepona, Cancelada: apartamentos de dos dormitorios desde {E505000} y adosados de tres dormitorios desde {E962000}, más IVA.',
  '23 appartements et maisons mitoyennes sur 51 à Haiku Estepona, Cancelada : appartements de deux chambres à partir de {E505000} et maisons mitoyennes de trois chambres à partir de {E962000}, hors TVA.',
  '23 von 51 Wohnungen und Reihenhäusern in Haiku Estepona, Cancelada: Wohnungen mit zwei Schlafzimmern ab {E505000} und Reihenhäuser mit drei Schlafzimmern ab {E962000}, zuzüglich MwSt.',
  '23 из 51 квартиры и таунхауса в Haiku Estepona, Канселада: квартиры с двумя спальнями от {E505000} и таунхаусы с тремя спальнями от {E962000} без НДС.',
  '23 من أصل 51 شقة ومنزلًا متلاصقًا في Haiku Estepona، كانسيلادا: شقق بغرفتي نوم ابتداءً من {E505000} ومنازل متلاصقة بثلاث غرف نوم ابتداءً من {E962000}، دون ضريبة القيمة المضافة.',
  '23 van de 51 appartementen en herenhuizen in Haiku Estepona, Cancelada: appartementen met twee slaapkamers vanaf {E505000} en herenhuizen met drie slaapkamers vanaf {E962000}, excl. btw.',
  '23 z 51 mieszkań i domów szeregowych w Haiku Estepona, Cancelada: mieszkania z dwiema sypialniami od {E505000} i domy szeregowe z trzema sypialniami od {E962000}, plus VAT.',
  '23 av 51 leiligheter og rekkehus i Haiku Estepona, Cancelada: leiligheter med to soverom fra {E505000} og rekkehus med tre soverom fra {E962000}, pluss mva.',
  '23 av 51 lägenheter och radhus i Haiku Estepona, Cancelada: lägenheter med två sovrum från {E505000} och radhus med tre sovrum från {E962000}, plus IVA.')
a('.twitterDescription',
  'Apartamentos de dos dormitorios desde {E505000} y adosados de tres dormitorios desde {E962000} en Haiku Estepona, Cancelada, más IVA.',
  'Appartements de deux chambres à partir de {E505000} et maisons mitoyennes de trois chambres à partir de {E962000} à Haiku Estepona, Cancelada, hors TVA.',
  'Wohnungen mit zwei Schlafzimmern ab {E505000} und Reihenhäuser mit drei Schlafzimmern ab {E962000} in Haiku Estepona, Cancelada, zuzüglich MwSt.',
  'Квартиры с двумя спальнями от {E505000} и таунхаусы с тремя спальнями от {E962000} в Haiku Estepona, Канселада, без НДС.',
  'شقق بغرفتي نوم ابتداءً من {E505000} ومنازل متلاصقة بثلاث غرف نوم ابتداءً من {E962000} في Haiku Estepona، كانسيلادا، دون ضريبة القيمة المضافة.',
  'Appartementen met twee slaapkamers vanaf {E505000} en herenhuizen met drie slaapkamers vanaf {E962000} in Haiku Estepona, Cancelada, excl. btw.',
  'Mieszkania z dwiema sypialniami od {E505000} i domy szeregowe z trzema sypialniami od {E962000} w Haiku Estepona, Cancelada, plus VAT.',
  'Leiligheter med to soverom fra {E505000} og rekkehus med tre soverom fra {E962000} i Haiku Estepona, Cancelada, pluss mva.',
  'Lägenheter med två sovrum från {E505000} och radhus med tre sovrum från {E962000} i Haiku Estepona, Cancelada, plus IVA.')
a('.hero.startingPrice', 'Desde {E505000} + IVA', 'À partir de {E505000} + TVA', 'Ab {E505000} + MwSt.', 'От {E505000} + НДС',
  'ابتداءً من {E505000} + ضريبة القيمة المضافة', 'Vanaf {E505000} + btw', 'Od {E505000} + VAT', 'Fra {E505000} + mva.', 'Från {E505000} + IVA')
a('.card.meta[0][1]', '{E505000} + IVA', '{E505000} + TVA', '{E505000} + MwSt.', '{E505000} + НДС',
  '{E505000} + ضريبة القيمة المضافة', '{E505000} + btw', '{E505000} + VAT', '{E505000} + mva.', '{E505000} + IVA')
a('.availability.priceRange', '{E505000} - {E1165000} + IVA', '{E505000} - {E1165000} + TVA', '{E505000} - {E1165000} + MwSt.',
  '{E505000} - {E1165000} + НДС', '{E505000} - {E1165000} + ضريبة القيمة المضافة', '{E505000} - {E1165000} + btw',
  '{E505000} - {E1165000} + VAT', '{E505000} - {E1165000} + mva.', '{E505000} - {E1165000} + IVA')
a('.card.description',
  '23 de 51 viviendas: apartamentos de dos dormitorios y adosados de tres dormitorios en Cancelada, Estepona, con piscina comunitaria y jardines paisajísticos, desde {E505000} + IVA.',
  '23 logements sur 51 : appartements de deux chambres et maisons mitoyennes de trois chambres à Cancelada, Estepona, avec piscine commune et jardins paysagers, à partir de {E505000} + TVA.',
  '23 von 51 Immobilien: Wohnungen mit zwei und Reihenhäuser mit drei Schlafzimmern in Cancelada, Estepona, mit Gemeinschaftspool und gestalteten Gärten, ab {E505000} + MwSt.',
  '23 из 51 объекта: квартиры с двумя спальнями и таунхаусы с тремя спальнями в Канселаде, Эстепона, с общим бассейном и благоустроенными садами, от {E505000} + НДС.',
  '23 من أصل 51 مسكنًا: شقق بغرفتي نوم ومنازل متلاصقة بثلاث غرف نوم في كانسيلادا، إستيبونا، مع مسبح مشترك وحدائق منسّقة، ابتداءً من {E505000} + ضريبة القيمة المضافة.',
  '23 van de 51 woningen: appartementen met twee en herenhuizen met drie slaapkamers in Cancelada, Estepona, met een gemeenschappelijk zwembad en aangelegde tuinen, vanaf {E505000} + btw.',
  '23 z 51 lokali: mieszkania z dwiema sypialniami i domy szeregowe z trzema sypialniami w Cancelada, Estepona, ze wspólnym basenem i zagospodarowanymi ogrodami, od {E505000} + VAT.',
  '23 av 51 boliger: leiligheter med to soverom og rekkehus med tre soverom i Cancelada, Estepona, med felles basseng og opparbeidede hager, fra {E505000} + mva.',
  '23 av 51 bostäder: lägenheter med två sovrum och radhus med tre sovrum i Cancelada, Estepona, med gemensam pool och planterade trädgårdar, från {E505000} + IVA.')

# ---- images and media ---------------------------------------------------------------------------

cg('.images.hero.alt',
   'de un bloque en terrazas sobre la piscina comunitaria, con tumbonas en una tarima de madera y montañas al fondo',
   'd’un immeuble à terrasses au-dessus de la piscine commune, avec des transats sur un deck en bois et des montagnes au loin',
   'eines Terrassenblocks über dem Gemeinschaftspool, mit Sonnenliegen auf einem Holzdeck und Bergen in der Ferne',
   'корпуса с террасами над общим бассейном: шезлонги на деревянном настиле и горы вдали',
   'لمبنى ذي تراسات فوق المسبح المشترك، مع كراسي استلقاء على منصة خشبية وجبال في الأفق',
   'van een terrassenblok boven het gemeenschappelijk zwembad, met ligbedden op een houten dek en bergen in de verte',
   'budynku z tarasami nad wspólnym basenem, z leżakami na drewnianym pokładzie i górami w oddali',
   'av en terrasseblokk over det felles bassenget, med solsenger på et tredekk og fjell i det fjerne',
   'av ett terrasshus ovanför den gemensamma poolen, med solsängar på ett trädäck och berg i fjärran')
cg('.images.architecture.alt',
   'de los dos bloques de apartamentos sobre los jardines, con terrazas escalonadas y ajardinadas y barandillas de vidrio',
   'des deux immeubles d’appartements au-dessus des jardins, avec des terrasses en gradins plantées et des garde-corps en verre',
   'der beiden Wohnblöcke über den Gärten, mit gestaffelten, bepflanzten Terrassen und Glasgeländern',
   'двух жилых корпусов над садами: террасы-уступы с зеленью и стеклянные ограждения',
   'للمبنيين السكنيين فوق الحدائق، مع تراسات متدرجة مزروعة ودرابزينات زجاجية',
   'van de twee appartementenblokken boven de tuinen, met getrapte, beplante terrassen en glazen balustrades',
   'dwóch budynków z mieszkaniami nad ogrodami, ze schodkowymi, obsadzonymi roślinami tarasami i szklanymi balustradami',
   'av de to leilighetsblokkene over hagene, med trappede, beplantede terrasser og glassrekkverk',
   'av de två lägenhetshusen ovanför trädgårdarna, med trappstegsformade, planterade terrasser och glasräcken')
cg('.images.lifestyle.alt',
   'de un solárium en la cubierta con una piscina pequeña, sofás lounge y una mesa de centro, con tejados y el mar al fondo',
   'd’un solarium sur le toit avec une petite piscine, des canapés lounge et une table basse, avec des toits et la mer au loin',
   'eines Dach-Solariums mit kleinem Pool, Lounge-Sofas und Couchtisch, dahinter Dächer und das Meer',
   'солярия на крыше с небольшим бассейном, диванами для отдыха и журнальным столиком; дальше видны крыши и море',
   'لسولاريوم على السطح مع مسبح صغير وكنبات استرخاء وطاولة قهوة، وخلفه أسطح ومنظر للبحر',
   'van een solarium op het dak met een klein zwembad, loungebanken en een salontafel, met daken en de zee erachter',
   'solarium na dachu z małym basenem, sofami wypoczynkowymi i stolikiem kawowym, z dachami i morzem w tle',
   'av en solterrasse på taket med et lite basseng, loungesofaer og et salongbord, med tak og havet bak',
   'av en solterrass på taket med en liten pool, loungesoffor och ett soffbord, med tak och havet bortom')
cg('.images.privateViewing.alt',
   'de un salón comedor con una puerta de ascensor a la izquierda, un sofá y una pared multimedia, y puertas de vidrio a una terraza con vistas al mar',
   'd’un séjour-salle à manger avec une porte d’ascenseur à gauche, un canapé et un mur multimédia, et des portes vitrées sur une terrasse avec vue sur la mer',
   'eines Wohn- und Essbereichs mit einer Aufzugtür links, einem Sofa und einer Medienwand sowie Glastüren zu einer Terrasse mit Meerblick',
   'гостиной-столовой с дверью лифта слева, диваном и медиастеной и стеклянными дверями на террасу с видом на море',
   'لمنطقة جلوس وطعام مع باب مصعد إلى اليسار وكنبة وجدار وسائط وأبواب زجاجية إلى تراس بإطلالة على البحر',
   'van een woon- en eetruimte met links een liftdeur, een bank en een tv-wand, en glazen deuren naar een terras met uitzicht op de zee',
   'salonu z jadalnią, z drzwiami windy po lewej, sofą i ścianą multimedialną oraz przeszklonymi drzwiami na taras z widokiem na morze',
   'av et stue- og spiseområde med en heisdør til venstre, en sofa og en mediavegg, og glassdører til en terrasse med utsikt over havet',
   'av ett vardags- och matrum med en hissdörr till vänster, en soffa och en mediavägg, och glasdörrar till en terrass med havsutsikt')
a('.media.copy',
  'Vistas generadas por ordenador del complejo, los jardines, las terrazas y los interiores, una imagen aérea de la zona y los planos de las 23 viviendas que figuran.',
  'Vues générées par ordinateur de l’ensemble, des jardins, des terrasses et des intérieurs, une image aérienne du secteur et les plans des 23 logements listés.',
  'Computergenerierte Ansichten der Anlage, der Gärten, der Terrassen und der Innenräume, eine Luftaufnahme der Umgebung und die Grundrisse der 23 aufgeführten Immobilien.',
  'Компьютерные визуализации комплекса, садов, террас и интерьеров, аэрофотография района и планировки 23 объектов из списка.',
  'مناظر مولَّدة بالحاسوب للمجمّع والحدائق والتراسات والتصاميم الداخلية، وصورة جوية للمنطقة، ومخططات المساكن الـ23 المدرجة.',
  'Computergegenereerde beelden van het complex, de tuinen, de terrassen en de interieurs, een luchtbeeld van de omgeving en de plattegronden van de 23 woningen op de lijst.',
  'Wygenerowane komputerowo widoki kompleksu, ogrodów, tarasów i wnętrz, zdjęcie lotnicze okolicy oraz rzuty 23 lokali z listy.',
  'Datagenererte bilder av anlegget, hagene, terrassene og interiørene, et flyfoto av området og plantegningene til de 23 boligene som er oppført.',
  'Datorgenererade vyer av området, trädgårdarna, terrasserna och interiörerna, ett flygfoto över omgivningen och planritningarna för de 23 bostäderna som är listade.')
a('.media.note',
  'Las imágenes son ilustraciones generadas por ordenador y no fotografías de los edificios terminados, salvo la imagen aérea, que es una fotografía de la zona con el complejo integrado mediante render. El mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los planos comerciales del promotor: no son contractuales, los nombres de las estancias están en español y las superficies que figuran son aproximadas.',
  'Les images sont des illustrations générées par ordinateur et non des photographies des bâtiments achevés, à l’exception de l’image aérienne, qui est une photographie du secteur dans laquelle l’ensemble a été intégré par rendu. Le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont les plans commerciaux du promoteur : ils n’ont pas de valeur contractuelle, les noms des pièces y sont en espagnol et les surfaces indiquées sont approximatives.',
  'Die Bilder sind computergenerierte Illustrationen und keine Fotos der fertigen Gebäude; Ausnahme ist die Luftaufnahme, ein Foto der Umgebung, in das die Anlage hineingerendert wurde. Möbel und Dekoration darin sind illustrativ und nicht enthalten. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen sind auf Spanisch, und die angegebenen Flächen sind ungefähr.',
  'Изображения — компьютерные иллюстрации, а не фотографии готовых зданий; исключение — аэрофотография: это снимок района, в который визуализирован комплекс. Мебель и декор на них носят иллюстративный характер и не входят в комплектацию. Планировки — коммерческие планы застройщика: они не имеют договорной силы, названия помещений на них даны по-испански, а указанные площади приблизительны.',
  'الصور رسوم توضيحية مولَّدة بالحاسوب وليست صورًا فوتوغرافية للمباني المنجزة، باستثناء الصورة الجوية، وهي صورة فوتوغرافية للمنطقة أُدرج فيها المجمّع بالتصيير. والأثاث والديكور الظاهران فيها توضيحيان وغير مشمولين. أما المخططات فهي مخططات البيع الخاصة بالمطوّر: وهي غير تعاقدية، وأسماء الغرف فيها بالإسبانية، والمساحات المذكورة فيها تقريبية.',
  'De beelden zijn computergegenereerde illustraties en geen foto’s van de afgewerkte gebouwen, behalve het luchtbeeld, een foto van de omgeving waarin het complex is gerenderd. Het meubilair en de inrichting erop zijn illustratief en niet inbegrepen. De plattegronden zijn de verkoopplattegronden van de ontwikkelaar: ze zijn niet contractueel, de namen van de ruimtes erop zijn in het Spaans en de vermelde oppervlaktes zijn bij benadering.',
  'Obrazy są wygenerowanymi komputerowo ilustracjami, a nie zdjęciami ukończonych budynków, z wyjątkiem zdjęcia lotniczego, które jest fotografią okolicy z wkomponowaną wizualizacją kompleksu. Meble i wystrój na nich mają charakter poglądowy i nie wchodzą w cenę. Rzuty to plany sprzedażowe dewelopera: nie mają mocy umownej, nazwy pomieszczeń są po hiszpańsku, a podane powierzchnie są przybliżone.',
  'Bildene er datagenererte illustrasjoner og ikke fotografier av de ferdige byggene, bortsett fra flyfotoet, som er et fotografi av området med anlegget lagt inn som visualisering. Møblene og innredningen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens salgstegninger: de er ikke kontraktsfestet, romnavnene på dem er på spansk, og arealene som er oppgitt er omtrentlige.',
  'Bilderna är datorgenererade illustrationer och inte fotografier av de färdiga byggnaderna, förutom flygfotot, som är ett fotografi av omgivningen där området har lagts in som visualisering. Möbler och inredning på dem är illustrativa och ingår inte. Planritningarna är exploatörens försäljningsritningar: de är inte avtalsbundna, rumsnamnen på dem är på spanska och ytorna som anges är ungefärliga.')

a('.media.items[0].caption', 'La piscina comunitaria y un bloque en terrazas', 'La piscine commune et un immeuble à terrasses', 'Der Gemeinschaftspool und ein Terrassenblock',
  'Общий бассейн и корпус с террасами', 'المسبح المشترك ومبنى ذو تراسات', 'Het gemeenschappelijk zwembad en een terrassenblok',
  'Wspólny basen i budynek z tarasami', 'Det felles bassenget og en terrasseblokk', 'Den gemensamma poolen och ett terrasshus')
a('.media.items[1].caption', 'Los bloques de apartamentos sobre los jardines', 'Les immeubles d’appartements au-dessus des jardins', 'Die Wohnblöcke über den Gärten',
  'Жилые корпуса над садами', 'المباني السكنية فوق الحدائق', 'De appartementenblokken boven de tuinen',
  'Budynki z mieszkaniami nad ogrodami', 'Leilighetsblokkene over hagene', 'Lägenhetshusen ovanför trädgårdarna')
cg('.media.items[2].alt',
   'de los adosados en hilera delante de los bloques de apartamentos, con terrazas ajardinadas',
   'des maisons mitoyennes en rangée devant les immeubles d’appartements, avec des terrasses plantées',
   'der in Reihen stehenden Reihenhäuser vor den Wohnblöcken, mit bepflanzten Terrassen',
   'таунхаусов в ряд перед жилыми корпусами, с озеленёнными террасами',
   'للمنازل المتلاصقة في صفوف أمام المباني السكنية، مع تراسات مزروعة',
   'van de herenhuizen in rijen voor de appartementenblokken, met beplante terrassen',
   'domów szeregowych w rzędach przed budynkami z mieszkaniami, z obsadzonymi roślinami tarasami',
   'av rekkehusene i rader foran leilighetsblokkene, med beplantede terrasser',
   'av radhusen i rader framför lägenhetshusen, med planterade terrasser')
a('.media.items[2].caption', 'Los adosados y los bloques de apartamentos', 'Les maisons mitoyennes et les immeubles d’appartements', 'Die Reihenhäuser und die Wohnblöcke',
  'Таунхаусы и жилые корпуса', 'المنازل المتلاصقة والمباني السكنية', 'De herenhuizen en de appartementenblokken',
  'Domy szeregowe i budynki z mieszkaniami', 'Rekkehusene og leilighetsblokkene', 'Radhusen och lägenhetshusen')
cg('.media.items[3].alt',
   'de las entradas de dos adosados, enmarcadas en pórticos revestidos de madera entre muros blancos',
   'des entrées de deux maisons mitoyennes, encadrées de portiques habillés de bois entre des murs blancs',
   'der Eingänge zweier Reihenhäuser, eingefasst von holzverkleideten Portalen zwischen weißen Wänden',
   'входов в два таунхауса в порталах с деревянной облицовкой между белыми стенами',
   'لمدخلي منزلين متلاصقين داخل بوابات مكسوة بالخشب بين جدران بيضاء',
   'van de ingangen van twee herenhuizen, in met hout beklede portalen tussen witte muren',
   'wejść do dwóch domów szeregowych, osadzonych w portalach obłożonych drewnem między białymi ścianami',
   'av inngangene til to rekkehus, innfattet av trekledde portaler mellom hvite vegger',
   'av ingångarna till två radhus, infattade i träklädda portaler mellan vita väggar')
a('.media.items[3].caption', 'Las entradas de los adosados', 'Les entrées des maisons mitoyennes', 'Die Eingänge der Reihenhäuser',
  'Входы в таунхаусы', 'مداخل المنازل المتلاصقة', 'De ingangen van de herenhuizen', 'Wejścia do domów szeregowych', 'Inngangene til rekkehusene', 'Ingångarna till radhusen')
cg('.media.items[4].alt',
   'de un camino de losas entre jardineras elevadas y árboles en flor, con un pabellón de techo redondo al fondo y un bloque con barandillas de vidrio a la derecha',
   'd’un chemin de dalles entre des jardinières surélevées et des arbres en fleurs, avec un pavillon à toit rond au fond et un immeuble à garde-corps en verre à droite',
   'eines Plattenwegs zwischen Hochbeeten und blühenden Bäumen, mit einem rundgedeckten Pavillon im Hintergrund und einem Block mit Glasgeländern rechts',
   'дорожки из плит между приподнятыми клумбами и цветущими деревьями; вдали павильон с круглой крышей, справа корпус со стеклянными ограждениями',
   'لممر من البلاطات بين أحواض زراعة مرتفعة وأشجار مزهرة، مع جناح بسقف مستدير في البعيد ومبنى بدرابزينات زجاجية إلى اليمين',
   'van een pad van stapstenen tussen verhoogde plantenbakken en bloeiende bomen, met in de verte een paviljoen met rond dak en rechts een blok met glazen balustrades',
   'ścieżki z płyt między podwyższonymi donicami i kwitnącymi drzewami, z pawilonem o okrągłym dachu w oddali i budynkiem ze szklanymi balustradami po prawej',
   'av en sti av heller mellom hevede plantekasser og blomstrende trær, med en paviljong med rundt tak i det fjerne og en blokk med glassrekkverk til høyre',
   'av en stig av stegplattor mellan upphöjda planteringslådor och blommande träd, med en paviljong med runt tak i fjärran och ett hus med glasräcken till höger')
a('.media.items[4].caption', 'El camino del jardín', 'Le chemin du jardin', 'Der Gartenweg', 'Садовая дорожка', 'ممر الحديقة', 'Het tuinpad', 'Ścieżka w ogrodzie', 'Hagestien', 'Trädgårdsstigen')
a('.media.items[5].alt',
  'Fotografía aérea de Cancelada con el complejo integrado mediante render, la costa en el horizonte y los edificios vecinos alrededor',
  'Photographie aérienne de Cancelada avec l’ensemble intégré par rendu, la côte à l’horizon et les bâtiments voisins autour',
  'Luftaufnahme von Cancelada mit der hineingerenderten Anlage, der Küste am Horizont und den Nachbargebäuden ringsum',
  'Аэрофотография Канселады с визуализированным в неё комплексом, береговой линией на горизонте и соседними зданиями вокруг',
  'صورة جوية لكانسيلادا مع المجمّع مُدرَجًا فيها بالتصيير، والساحل عند الأفق والمباني المجاورة حوله',
  'Luchtfoto van Cancelada met het complex erin gerenderd, de kust aan de horizon en de naburige gebouwen eromheen',
  'Zdjęcie lotnicze Cancelady z wkomponowaną wizualizacją kompleksu, wybrzeżem na horyzoncie i sąsiednimi budynkami wokół',
  'Flyfoto av Cancelada med anlegget lagt inn som visualisering, kysten i horisonten og nabobygninger rundt',
  'Flygfoto över Cancelada med komplexet inlagt som visualisering, kusten vid horisonten och grannbyggnader runt omkring')
a('.media.items[5].caption', 'El complejo en su entorno', 'L’ensemble dans son cadre', 'Die Anlage in ihrer Umgebung', 'Комплекс в окружении', 'المجمّع في محيطه',
  'Het complex in zijn omgeving', 'Kompleks w swoim otoczeniu', 'Anlegget i omgivelsene', 'Området i sin miljö')
a('.media.items[6].caption', 'Un solárium con piscina de día', 'Un solarium avec piscine de jour', 'Ein Solarium mit Pool bei Tag', 'Солярий с бассейном днём',
  'سولاريوم مع مسبح في النهار', 'Een solarium met zwembad overdag', 'Solarium z basenem za dnia', 'En solterrasse med basseng på dagtid', 'En solterrass med pool på dagen')
cg('.media.items[7].alt',
   'de un solárium iluminado en la cubierta por la noche, con una piscina pequeña, zona lounge y bloques vecinos',
   'd’un solarium éclairé sur le toit de nuit, avec une petite piscine, un coin lounge et des immeubles voisins',
   'eines beleuchteten Dach-Solariums bei Nacht, mit kleinem Pool, Lounge-Sitzbereich und Nachbargebäuden',
   'освещённого солярия на крыше ночью: небольшой бассейн, зона отдыха и соседние корпуса',
   'لسولاريوم مضاء على السطح ليلًا، مع مسبح صغير ومقاعد استرخاء ومبانٍ مجاورة',
   'van een verlicht solarium op het dak bij nacht, met een klein zwembad, loungezitplekken en naburige blokken',
   'oświetlonego solarium na dachu nocą, z małym basenem, strefą wypoczynkową i sąsiednimi budynkami',
   'av en opplyst solterrasse på taket om natten, med et lite basseng, loungeplasser og nabobygninger',
   'av en upplyst solterrass på taket om natten, med en liten pool, loungemöbler och grannhus')
a('.media.items[7].caption', 'Un solárium con piscina de noche', 'Un solarium avec piscine de nuit', 'Ein Solarium mit Pool bei Nacht', 'Солярий с бассейном ночью',
  'سولاريوم مع مسبح في الليل', 'Een solarium met zwembad bij nacht', 'Solarium z basenem nocą', 'En solterrasse med basseng om natten', 'En solterrass med pool på natten')
cg('.media.items[8].alt',
   'de un solárium en la cubierta con una pérgola, una barra con taburetes, sofás lounge y el mar en el horizonte',
   'd’un solarium sur le toit avec une pergola, un bar avec tabourets, des canapés lounge et la mer à l’horizon',
   'eines Dach-Solariums mit Pergola, Bar mit Barhockern, Lounge-Sofas und dem Meer am Horizont',
   'солярия на крыше с перголой, барной стойкой с высокими стульями, диванами для отдыха и морем на горизонте',
   'لسولاريوم على السطح مع برغولا وبار بكراسٍ عالية وكنبات استرخاء والبحر عند الأفق',
   'van een solarium op het dak met een pergola, een bar met barkrukken, loungebanken en de zee aan de horizon',
   'solarium na dachu z pergolą, barem ze stołkami, sofami wypoczynkowymi i morzem na horyzoncie',
   'av en solterrasse på taket med en pergola, en bar med barstoler, loungesofaer og havet i horisonten',
   'av en solterrass på taket med en pergola, en bar med barstolar, loungesoffor och havet vid horisonten')
a('.media.items[8].caption', 'Un solárium con barra y zona lounge', 'Un solarium avec bar et coin lounge', 'Ein Solarium mit Bar und Lounge', 'Солярий с баром и зоной отдыха',
  'سولاريوم مع بار ومنطقة استرخاء', 'Een solarium met bar en lounge', 'Solarium z barem i strefą wypoczynkową', 'En solterrasse med bar og lounge', 'En solterrass med bar och lounge')
cg('.media.items[9].alt',
   'de una terraza cubierta con techo de lamas de madera, una mesa de comedor larga, sofás lounge y vistas al mar y a una montaña',
   'd’une terrasse couverte avec un plafond à lattes de bois, une longue table à manger, des canapés lounge et une vue sur la mer et une montagne',
   'einer überdachten Terrasse mit Holzlamellendecke, langem Esstisch, Lounge-Sofas und Blick auf das Meer und einen Berg',
   'крытой террасы с потолком из деревянных реек, длинным обеденным столом, диванами для отдыха и видом на море и гору',
   'لتراس مسقوف بسقف من شرائح الخشب وطاولة طعام طويلة وكنبات استرخاء وإطلالة على البحر وجبل',
   'van een overdekt terras met een plafond van houten latten, een lange eettafel, loungebanken en uitzicht op de zee en een berg',
   'zadaszonego tarasu z sufitem z drewnianych listew, długim stołem jadalnym, sofami wypoczynkowymi i widokiem na morze i górę',
   'av en overdekket terrasse med et tak av trelister, et langt spisebord, loungesofaer og utsikt over havet og et fjell',
   'av en övertäckt terrass med ett tak av träribbor, ett långt matbord, loungesoffor och utsikt över havet och ett berg')
a('.media.items[9].caption', 'Una terraza cubierta con mesa de comedor', 'Une terrasse couverte avec table à manger', 'Eine überdachte Terrasse mit Esstisch', 'Крытая терраса с обеденным столом',
  'تراس مسقوف مع طاولة طعام', 'Een overdekt terras met eettafel', 'Zadaszony taras ze stołem jadalnym', 'En overdekket terrasse med spisebord', 'En övertäckt terrass med matbord')
cg('.media.items[10].alt',
   'de una terraza cubierta con un comedor y sofás curvos, con vistas sobre el paisaje hasta el mar',
   'd’une terrasse couverte avec un coin repas et des canapés courbes, avec une vue sur le paysage jusqu’à la mer',
   'einer überdachten Terrasse mit Essgruppe und geschwungenen Sofas, mit Blick über die Landschaft bis zum Meer',
   'крытой террасы с обеденной группой и изогнутыми диванами и видом через ландшафт на море',
   'لتراس مسقوف مع طقم طعام وكنبات منحنية وإطلالة عبر المشهد الطبيعي على البحر',
   'van een overdekt terras met een eethoek en gebogen banken, met uitzicht over het landschap tot aan de zee',
   'zadaszonego tarasu z zestawem jadalnianym i zakrzywionymi sofami, z widokiem przez krajobraz na morze',
   'av en overdekket terrasse med en spisegruppe og buede sofaer, med utsikt over landskapet til havet',
   'av en övertäckt terrass med en matgrupp och böjda soffor, med utsikt över landskapet till havet')
cg('.media.items[11].alt',
   'de una cocina, comedor y salón abiertos entre sí que dan a una terraza cubierta con zona de estar y vistas al mar',
   'd’un espace ouvert réunissant cuisine, salle à manger et séjour, donnant sur une terrasse couverte avec salon et vue sur la mer',
   'eines offenen Küchen-, Ess- und Wohnbereichs mit Zugang zu einer überdachten Terrasse mit Sitzbereich und Meerblick',
   'кухни-столовой-гостиной в едином пространстве с выходом на крытую террасу с зоной отдыха и видом на море',
   'لمطبخ وغرفة طعام وغرفة جلوس مفتوحة على بعضها وتطل على تراس مسقوف فيه مقاعد وإطلالة على البحر',
   'van een open keuken, eet- en woonruimte die uitkomt op een overdekt terras met zitplekken en uitzicht op de zee',
   'otwartej kuchni, jadalni i salonu z wyjściem na zadaszony taras z miejscem do siedzenia i widokiem na morze',
   'av et åpent kjøkken, spise- og stueområde som åpner seg mot en overdekket terrasse med sitteplasser og utsikt over havet',
   'av ett öppet kök, matplats och vardagsrum som öppnar sig mot en övertäckt terrass med sittplatser och havsutsikt')
a('.media.items[11].caption', 'Cocina, comedor y terraza', 'Cuisine, salle à manger et terrasse', 'Küche, Essbereich und Terrasse', 'Кухня, столовая и терраса',
  'المطبخ وغرفة الطعام والتراس', 'Keuken, eetruimte en terras', 'Kuchnia, jadalnia i taras', 'Kjøkken, spiseplass og terrasse', 'Kök, matplats och terrass')
cg('.media.items[12].alt',
   'de un salón con sofá y mesa de comedor que da a una terraza cubierta con un sofá curvo y el mar al fondo',
   'd’un séjour avec canapé et table à manger donnant sur une terrasse couverte avec un canapé courbe et la mer au loin',
   'eines Wohnzimmers mit Sofa und Esstisch, das sich zu einer überdachten Terrasse mit geschwungenem Sofa und dem Meer dahinter öffnet',
   'гостиной с диваном и обеденным столом с выходом на крытую террасу с изогнутым диваном; вдали море',
   'لغرفة جلوس بها كنبة وطاولة طعام تطل على تراس مسقوف فيه كنبة منحنية والبحر في البعيد',
   'van een woonkamer met een bank en een eettafel die uitkomt op een overdekt terras met een gebogen bank en de zee erachter',
   'salonu z sofą i stołem jadalnym, otwartego na zadaszony taras z zakrzywioną sofą i morzem w tle',
   'av en stue med sofa og spisebord som åpner seg mot en overdekket terrasse med en buet sofa og havet bak',
   'av ett vardagsrum med soffa och matbord som öppnar sig mot en övertäckt terrass med en böjd soffa och havet bortom')
a('.media.items[12].caption', 'El salón y su terraza', 'Le séjour et sa terrasse', 'Der Wohnbereich und seine Terrasse', 'Гостиная и её терраса',
  'غرفة الجلوس والتراس الملحق بها', 'De woonkamer en het terras', 'Salon i jego taras', 'Stuen og terrassen', 'Vardagsrummet och dess terrass')
cg('.media.items[13].alt',
   'de una cocina abierta con isla, una mesa de comedor y un salón con grandes puertas de vidrio y vistas a una montaña',
   'd’une cuisine ouverte avec îlot, une table à manger et un séjour aux grandes baies vitrées avec vue sur une montagne',
   'einer offenen Küche mit Kochinsel, einem Esstisch und einem Wohnzimmer mit großen Glastüren und Blick auf einen Berg',
   'открытой кухни с островом, обеденного стола и гостиной с большими стеклянными дверями и видом на гору',
   'لمطبخ مفتوح بجزيرة وطاولة طعام وغرفة جلوس بأبواب زجاجية كبيرة وإطلالة على جبل',
   'van een open keuken met eiland, een eettafel en een woonkamer met grote glazen deuren en uitzicht op een berg',
   'otwartej kuchni z wyspą, stołu jadalnego i salonu z dużymi przeszkleniami oraz widokiem na górę',
   'av et åpent kjøkken med øy, et spisebord og en stue med store glassdører og utsikt mot et fjell',
   'av ett öppet kök med köksö, ett matbord och ett vardagsrum med stora glasdörrar och utsikt mot ett berg')
cg('.media.items[14].alt',
   'de un salón abierto con una pared multimedia de efecto mármol y una cocina con isla y tres taburetes',
   'd’un séjour ouvert avec un mur multimédia effet marbre et une cuisine avec îlot et trois tabourets',
   'eines offenen Wohnzimmers mit einer Medienwand in Marmoroptik und einer Küche mit Kochinsel und drei Barhockern',
   'гостиной в едином пространстве с медиастеной под мрамор и кухней с островом и тремя барными стульями',
   'لغرفة جلوس مفتوحة بجدار وسائط بمظهر الرخام ومطبخ بجزيرة وثلاثة كراسٍ عالية',
   'van een open woonkamer met een tv-wand in marmerlook en een keuken met eiland en drie barkrukken',
   'otwartego salonu ze ścianą multimedialną w kolorze marmuru i kuchni z wyspą i trzema stołkami',
   'av en åpen stue med en mediavegg i marmorlook og et kjøkken med øy og tre barstoler',
   'av ett öppet vardagsrum med en mediavägg i marmorlook och ett kök med köksö och tre barstolar')
cg('.media.items[15].alt',
   'de una isla de cocina en primer plano, con una escalera y una puerta de ascensor a la izquierda y, al fondo, un salón comedor con puertas de vidrio a la terraza',
   'd’un îlot de cuisine au premier plan, avec un escalier et une porte d’ascenseur à gauche et, au fond, un séjour-salle à manger avec des portes vitrées sur la terrasse',
   'einer Kochinsel im Vordergrund, links mit einer Treppe und einer Aufzugtür, dahinter ein Wohn- und Essbereich mit Glastüren zur Terrasse',
   'кухонного острова на переднем плане, слева лестница и дверь лифта, дальше гостиная-столовая со стеклянными дверями на террасу',
   'لجزيرة مطبخ في المقدمة، مع درج وباب مصعد إلى اليسار، وخلفها منطقة جلوس وطعام بأبواب زجاجية إلى التراس',
   'van een keukeneiland op de voorgrond, met links een trap en een liftdeur, en daarachter een woon- en eetruimte met glazen deuren naar het terras',
   'wyspy kuchennej na pierwszym planie, ze schodami i drzwiami windy po lewej oraz salonem z jadalnią i przeszklonymi drzwiami na taras w głębi',
   'av en kjøkkenøy i forgrunnen, med en trapp og en heisdør til venstre og et stue- og spiseområde med glassdører til terrassen bak',
   'av en köksö i förgrunden, med en trappa och en hissdörr till vänster och ett vardags- och matrum med glasdörrar till terrassen bortom')
a('.media.items[15].caption', 'La isla de cocina y la zona de estar', 'L’îlot de cuisine et le séjour', 'Die Kochinsel und der Wohnbereich', 'Кухонный остров и гостиная',
  'جزيرة المطبخ ومنطقة الجلوس', 'Het keukeneiland en de woonruimte', 'Wyspa kuchenna i część dzienna', 'Kjøkkenøya og stueområdet', 'Köksön och vardagsrummet')
cg('.media.items[17].alt',
   'de un dormitorio con cabecero tapizado, cortinas y una puerta corredera de vidrio a la terraza',
   'd’une chambre avec une tête de lit capitonnée, des rideaux et une porte coulissante vitrée donnant sur la terrasse',
   'eines Schlafzimmers mit gepolstertem Kopfteil, Vorhängen und einer Glasschiebetür zur Terrasse',
   'спальни с мягким изголовьем, шторами и стеклянной раздвижной дверью на террасу',
   'لغرفة نوم برأس سرير منجّد وستائر وباب زجاجي منزلق إلى التراس',
   'van een slaapkamer met een gestoffeerd hoofdeinde, gordijnen en een glazen schuifdeur naar het terras',
   'sypialni z tapicerowanym wezgłowiem, zasłonami i przesuwnymi szklanymi drzwiami na taras',
   'av et soverom med polstret sengegavl, gardiner og en skyvedør i glass til terrassen',
   'av ett sovrum med stoppad sänggavel, gardiner och en glasskjutdörr till terrassen')
cg('.media.items[18].alt',
   'de un dormitorio con un mural de motivos vegetales tras la cama, un tocador, un armario abierto a la derecha y puertas correderas de vidrio a una terraza',
   'd’une chambre avec une fresque à motif de feuilles derrière le lit, une coiffeuse, un dressing ouvert à droite et des portes coulissantes vitrées donnant sur une terrasse',
   'eines Schlafzimmers mit einem Wandbild mit Blattmuster hinter dem Bett, einem Schminktisch, einem offenen Kleiderschrank rechts und Glasschiebetüren zu einer Terrasse',
   'спальни с настенным панно с растительным узором за кроватью, туалетным столиком, открытым гардеробом справа и стеклянными раздвижными дверями на террасу',
   'لغرفة نوم بجدارية بنقوش أوراق خلف السرير وطاولة زينة وخزانة مفتوحة إلى اليمين وأبواب زجاجية منزلقة إلى تراس',
   'van een slaapkamer met een muurschildering met bladmotief achter het bed, een kaptafel, rechts een open kleerkast en glazen schuifdeuren naar een terras',
   'sypialni z malowidłem w liście za łóżkiem, toaletką, otwartą szafą po prawej i przesuwnymi szklanymi drzwiami na taras',
   'av et soverom med et veggmaleri med bladmønster bak sengen, et sminkebord, en åpen garderobe til høyre og glassskyvedører til en terrasse',
   'av ett sovrum med en väggmålning med bladmönster bakom sängen, ett sminkbord, en öppen garderob till höger och glasskjutdörrar till en terrass')
a('.media.items[18].caption', 'Un dormitorio con vestidor', 'Une chambre avec dressing', 'Ein Schlafzimmer mit Ankleidebereich', 'Спальня с гардеробной зоной',
  'غرفة نوم مع منطقة تبديل ملابس', 'Een slaapkamer met kleedruimte', 'Sypialnia ze strefą garderoby', 'Et soverom med garderobeområde', 'Ett sovrum med klädrum')
cg('.media.items[19].alt',
   'de un baño con lavabo doble sobre un mueble de efecto madera, dos espejos ovalados retroiluminados y una ducha a ras de suelo, con un armario a la izquierda',
   'd’une salle de bain avec une double vasque sur un meuble effet bois, deux miroirs ovales rétroéclairés et une douche à l’italienne, avec un placard à gauche',
   'eines Badezimmers mit Doppelwaschtisch auf einem Unterschrank in Holzoptik, zwei hinterleuchteten ovalen Spiegeln und einer begehbaren Dusche, links ein Schrank',
   'ванной комнаты с двойной раковиной на тумбе под дерево, двумя овальными зеркалами с подсветкой и душем без поддона; слева шкаф',
   'لحمام بحوض مزدوج على خزانة بمظهر الخشب ومرآتين بيضاويتين بإضاءة خلفية ودش مفتوح، مع خزانة إلى اليسار',
   'van een badkamer met een dubbele wastafel op een kast in houtlook, twee ovale spiegels met achtergrondverlichting en een inloopdouche, met links een kast',
   'łazienki z podwójną umywalką na szafce w kolorze drewna, dwoma owalnymi lustrami z podświetleniem i prysznicem bez brodzika, z szafą po lewej',
   'av et bad med doble servanter på et skap i trelook, to ovale speil med bakgrunnsbelysning og en åpen dusj, med et skap til venstre',
   'av ett badrum med dubbla handfat på ett skåp i trälook, två ovala speglar med bakgrundsbelysning och en öppen dusch, med ett skåp till vänster')

# ---- overview, why, architecture ---------------------------------------------------------------

a('.overview.headlineHtml',
  '23 viviendas <em>disponibles</em>, de dos tipos',
  '23 logements <em>disponibles</em>, de deux types',
  '23 Immobilien <em>verfügbar</em>, in zwei Typen',
  '23 объекта <em>в продаже</em>, двух типов',
  '23 مسكنًا <em>متاحًا</em> من نوعين',
  '23 woningen <em>beschikbaar</em>, van twee typen',
  '23 lokale <em>dostępne</em>, dwóch typów',
  '23 boliger <em>tilgjengelige</em>, av to typer',
  '23 bostäder <em>tillgängliga</em>, av två typer')
a('.overview.copy[0]',
  'Haiku Estepona es un complejo residencial en Cancelada, en la Nueva Milla de Oro de Estepona, con dos tipos de vivienda: 36 apartamentos, llamados Haiku Suites, y 15 adosados, llamados Haiku Residences. El dosier del promotor describe un entorno en ladera donde se encuentran el mar y la montaña, con jardines mediterráneos, senderos para pasear, una piscina, un salón comunitario y un club social. La memoria de calidades añade que las zonas libres ajardinadas forman una franja central que separa los dos tipos.',
  'Haiku Estepona est un ensemble résidentiel à Cancelada, sur la New Golden Mile d’Estepona, avec deux types de logement : 36 appartements, appelés Haiku Suites, et 15 maisons mitoyennes, appelées Haiku Residences. Le dossier du promoteur décrit un site à flanc de colline où la mer et la montagne se rencontrent, avec des jardins méditerranéens, des sentiers de promenade, une piscine, un salon commun et un club social. Le descriptif des prestations ajoute que les espaces libres paysagers forment une zone centrale qui sépare les deux types.',
  'Haiku Estepona ist eine Wohnanlage in Cancelada, an der New Golden Mile von Estepona, mit zwei Haustypen: 36 Wohnungen, die Haiku Suites, und 15 Reihenhäuser, die Haiku Residences. Das Dossier des Bauträgers beschreibt eine Hanglage, in der sich Meer und Berge begegnen, mit mediterranen Gärten, Spazierwegen, einem Swimmingpool, einem Gemeinschaftsraum und einem Social Club. Die Ausstattungsbeschreibung ergänzt, dass die gestalteten Freiflächen eine zentrale Zone bilden, die die beiden Typen trennt.',
  'Haiku Estepona — жилой комплекс в Канселаде, на Новой Золотой миле Эстепоны, с двумя типами жилья: 36 квартир под названием Haiku Suites и 15 таунхаусов под названием Haiku Residences. В досье застройщика описан участок на склоне холма, где встречаются море и горы: средиземноморские сады, прогулочные дорожки, бассейн, общая гостиная и социальный клуб. Спецификация отделки добавляет, что озеленённые открытые пространства образуют центральную зону, которая разделяет два типа жилья.',
  'Haiku Estepona مجمّع سكني في كانسيلادا، على الميل الذهبي الجديد في إستيبونا، بنوعين من المساكن: 36 شقة تحمل اسم Haiku Suites و15 منزلًا متلاصقًا يحمل اسم Haiku Residences. يصف ملف المطوّر موقعًا على سفح تلة يلتقي فيه البحر بالجبال، مع حدائق متوسطية وممرات للمشي ومسبح وصالة مشتركة ونادٍ اجتماعي. وتضيف مواصفات الجودة أن المساحات المفتوحة المنسّقة تشكّل منطقة مركزية تفصل بين النوعين.',
  'Haiku Estepona is een woonproject in Cancelada, aan de New Golden Mile van Estepona, met twee typen woning: 36 appartementen, Haiku Suites genoemd, en 15 herenhuizen, Haiku Residences genoemd. Het dossier van de ontwikkelaar beschrijft een locatie op een heuvelhelling waar de zee en de bergen elkaar ontmoeten, met mediterrane tuinen, wandelpaden, een zwembad, een gemeenschappelijke lounge en een sociale club. De technische omschrijving voegt toe dat de aangelegde open ruimtes een centrale zone vormen die de twee typen scheidt.',
  'Haiku Estepona to kompleks mieszkaniowy w Cancelada, na New Golden Mile w Esteponie, z dwoma typami lokali: 36 mieszkaniami o nazwie Haiku Suites i 15 domami szeregowymi o nazwie Haiku Residences. Dossier dewelopera opisuje położenie na zboczu wzgórza, gdzie spotykają się morze i góry, z ogrodami śródziemnomorskimi, ścieżkami spacerowymi, basenem, wspólnym salonem i klubem towarzyskim. Standard wykończenia dodaje, że zagospodarowane tereny otwarte tworzą strefę centralną, która oddziela oba typy.',
  'Haiku Estepona er et boligkompleks i Cancelada, på New Golden Mile i Estepona, med to typer boliger: 36 leiligheter, kalt Haiku Suites, og 15 rekkehus, kalt Haiku Residences. Utbyggers dossier beskriver en beliggenhet i en li der havet og fjellene møtes, med middelhavshager, turstier, et basseng, en felles lounge og en sosial klubb. Byggebeskrivelsen tilføyer at de opparbeidede uteområdene danner en sentral sone som skiller de to typene.',
  'Haiku Estepona är ett bostadsområde i Cancelada, på New Golden Mile i Estepona, med två typer av bostäder: 36 lägenheter, kallade Haiku Suites, och 15 radhus, kallade Haiku Residences. Exploatörens dossier beskriver ett läge i en sluttning där havet och bergen möts, med medelhavsträdgårdar, promenadstigar, en pool, en gemensam lounge och en social klubb. Byggnadsbeskrivningen tillägger att de planterade friytorna bildar en central zon som skiljer de två typerna åt.')
a('.overview.copy[1]',
  'La lista de precios del 26 de octubre de 2026 marca 28 de las 51 viviendas como reservadas y recoge 23 con precio: 13 apartamentos de dos dormitorios y 10 adosados de tres dormitorios. Ningún documento indica una fecha de entrega.',
  'La liste de prix du 26 octobre 2026 marque 28 des 51 logements comme réservés et en indique 23 avec un prix : 13 appartements de deux chambres et 10 maisons mitoyennes de trois chambres. Aucun document ne donne de date de livraison.',
  'Die Preisliste vom 26. Oktober 2026 kennzeichnet 28 der 51 Immobilien als reserviert und führt 23 mit Preis auf: 13 Wohnungen mit zwei Schlafzimmern und 10 Reihenhäuser mit drei Schlafzimmern. Keines der Dokumente nennt einen Fertigstellungstermin.',
  'В прайс-листе от 26 октября 2026 года 28 из 51 объекта отмечены как забронированные, а у 23 указана цена: 13 квартир с двумя спальнями и 10 таунхаусов с тремя спальнями. Ни в одном из документов нет срока сдачи.',
  'تشير قائمة الأسعار المؤرخة في 26 أكتوبر 2026 إلى أن 28 من أصل 51 مسكنًا محجوزة، وتورد سعرًا لـ 23 منها: 13 شقة بغرفتي نوم و10 منازل متلاصقة بثلاث غرف نوم. ولا تذكر أي من الوثائق موعدًا للإنجاز.',
  'De prijslijst van 26 oktober 2026 markeert 28 van de 51 woningen als gereserveerd en vermeldt 23 met een prijs: 13 appartementen met twee slaapkamers en 10 herenhuizen met drie slaapkamers. Geen van de documenten noemt een opleveringsdatum.',
  'Cennik z 26 października 2026 r. oznacza 28 z 51 lokali jako zarezerwowane i podaje cenę 23 z nich: 13 mieszkań z dwiema sypialniami i 10 domów szeregowych z trzema sypialniami. Żaden z dokumentów nie podaje terminu odbioru.',
  'Prislisten fra 26. oktober 2026 markerer 28 av de 51 boligene som reservert og oppgir pris for 23: 13 leiligheter med to soverom og 10 rekkehus med tre soverom. Ingen av dokumentene oppgir en ferdigstillelsesdato.',
  'Prislistan från den 26 oktober 2026 markerar 28 av de 51 bostäderna som reserverade och anger pris för 23: 13 lägenheter med två sovrum och 10 radhus med tre sovrum. Inget av dokumenten anger ett färdigställandedatum.')
a('.overview.metrics[0][1]', '51 viviendas', '51 logements', '51 Immobilien', '51 объект', '51 مسكنًا', '51 woningen', '51 lokali', '51 boliger', '51 bostäder')

a('.why.copy',
  'Apartamentos de dos dormitorios y adosados de tres dormitorios con amplias terrazas, en Cancelada, en la Nueva Milla de Oro, cerca de los campos de golf.',
  'Appartements de deux chambres et maisons mitoyennes de trois chambres avec de grandes terrasses, à Cancelada, sur la New Golden Mile, près des golfs.',
  'Wohnungen mit zwei und Reihenhäuser mit drei Schlafzimmern und großen Terrassen, in Cancelada an der New Golden Mile, in der Nähe der Golfplätze.',
  'Квартиры с двумя спальнями и таунхаусы с тремя спальнями с большими террасами — в Канселаде, на Новой Золотой миле, рядом с гольф-полями.',
  'شقق بغرفتي نوم ومنازل متلاصقة بثلاث غرف نوم مع تراسات واسعة، في كانسيلادا على الميل الذهبي الجديد، بالقرب من ملاعب الغولف.',
  'Appartementen met twee en herenhuizen met drie slaapkamers en grote terrassen, in Cancelada aan de New Golden Mile, dicht bij de golfbanen.',
  'Mieszkania z dwiema sypialniami i domy szeregowe z trzema sypialniami, z dużymi tarasami, w Cancelada na New Golden Mile, w pobliżu pól golfowych.',
  'Leiligheter med to soverom og rekkehus med tre soverom og store terrasser, i Cancelada på New Golden Mile, nær golfbanene.',
  'Lägenheter med två sovrum och radhus med tre sovrum och stora terrasser, i Cancelada på New Golden Mile, nära golfbanorna.')
a('.why.points[0][1]',
  'Compradores que buscan un apartamento nuevo de dos dormitorios o un adosado de tres dormitorios con solárium en Estepona, cerca de los campos de golf y de la costa, para vivir o como segunda residencia.',
  'Acheteurs qui recherchent un appartement neuf de deux chambres ou une maison mitoyenne de trois chambres avec solarium à Estepona, près des golfs et de la côte, pour y vivre ou comme résidence secondaire.',
  'Käufer, die in Estepona eine neue Wohnung mit zwei Schlafzimmern oder ein Reihenhaus mit drei Schlafzimmern und Solarium suchen, in der Nähe der Golfplätze und der Küste, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужна новая квартира с двумя спальнями или таунхаус с тремя спальнями и солярием в Эстепоне, рядом с гольф-полями и побережьем, для постоянного проживания или как вторая недвижимость.',
  'المشترون الذين يبحثون في إستيبونا عن شقة جديدة بغرفتي نوم أو منزل متلاصق بثلاث غرف نوم مع سولاريوم، قرب ملاعب الغولف والساحل، للسكن أو كمسكن ثانٍ.',
  'Kopers die in Estepona een nieuw appartement met twee slaapkamers of een herenhuis met drie slaapkamers en een solarium zoeken, dicht bij de golfbanen en de kust, om er te wonen of als tweede woning.',
  'Kupujący, którzy szukają w Esteponie nowego mieszkania z dwiema sypialniami lub domu szeregowego z trzema sypialniami i solarium, w pobliżu pól golfowych i wybrzeża, do zamieszkania lub jako drugi dom.',
  'Kjøpere som ønsker en ny leilighet med to soverom eller et rekkehus med tre soverom og solarium i Estepona, nær golfbanene og kysten, til å bo i eller som feriebolig.',
  'Köpare som vill ha en ny lägenhet med två sovrum eller ett radhus med tre sovrum och solterrass i Estepona, nära golfbanorna och kusten, att bo i eller som andra bostad.')
a('.why.points[1][1]',
  'Dos tipos de vivienda en un mismo complejo: apartamentos de 94,15 a 102,08 m² construidos, con terrazas, y adosados de 200,56 a 208,92 m² construidos en cuatro niveles, con garaje en el sótano, jardín y solárium, a uno y otro lado de una zona ajardinada central.',
  'Deux types de logement dans un même ensemble : des appartements de 94,15 à 102,08 m² construits, avec terrasses, et des maisons mitoyennes de 200,56 à 208,92 m² construits sur quatre niveaux, avec garage en sous-sol, jardin et solarium, de part et d’autre d’une zone paysagère centrale.',
  'Zwei Haustypen in einer Anlage: Wohnungen mit 94,15 bis 102,08 m² bebauter Fläche und Terrassen sowie Reihenhäuser mit 200,56 bis 208,92 m² bebauter Fläche auf vier Ebenen, mit Garage im Untergeschoss, Garten und Solarium, zu beiden Seiten einer zentralen Grünanlage.',
  'Два типа жилья в одном комплексе: квартиры площадью застройки от 94,15 до 102,08 м² с террасами и таунхаусы площадью застройки от 200,56 до 208,92 м² на четырёх уровнях, с гаражом в цокольном этаже, садом и солярием, по обе стороны от центральной озеленённой зоны.',
  'نوعان من المساكن في مجمّع واحد: شقق مساحتها المبنية من 94.15 إلى 102.08 م² مع تراسات، ومنازل متلاصقة مساحتها المبنية من 200.56 إلى 208.92 م² على أربعة مستويات، مع مرآب في القبو وحديقة وسولاريوم، على جانبي منطقة خضراء مركزية.',
  'Twee typen woning in één complex: appartementen van 94,15 tot 102,08 m² bebouwd, met terrassen, en herenhuizen van 200,56 tot 208,92 m² bebouwd op vier niveaus, met een garage in de kelder, een tuin en een solarium, aan weerszijden van een centrale aangelegde zone.',
  'Dwa typy lokali w jednym kompleksie: mieszkania o powierzchni zabudowy od 94,15 do 102,08 m² z tarasami oraz domy szeregowe o powierzchni zabudowy od 200,56 do 208,92 m² na czterech poziomach, z garażem w suterenie, ogrodem i solarium, po obu stronach centralnej strefy zieleni.',
  'To typer boliger i ett kompleks: leiligheter på 94,15 til 102,08 m² bebygd areal, med terrasser, og rekkehus på 200,56 til 208,92 m² bebygd areal fordelt på fire plan, med garasje i kjelleren, hage og solarium, på hver sin side av et sentralt opparbeidet område.',
  'Två typer av bostäder i ett område: lägenheter på 94,15 till 102,08 m² byggyta, med terrasser, och radhus på 200,56 till 208,92 m² byggyta fördelade på fyra plan, med garage i källaren, trädgård och solterrass, på var sin sida om en central planterad yta.')
a('.why.points[2][1]',
  'El dosier sitúa Haiku en Cancelada, en la Nueva Milla de Oro de Estepona, entre los campos de golf Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House y Atalaya Golf & Country Club, con el Real Club Valderrama, en Sotogrande, a 20 minutos. No da otras distancias.',
  'Le dossier situe Haiku à Cancelada, sur la New Golden Mile d’Estepona, parmi les golfs Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House et Atalaya Golf & Country Club, avec le Real Club Valderrama, à Sotogrande, à 20 minutes. Il ne donne pas d’autres distances.',
  'Das Dossier verortet Haiku in Cancelada, an der New Golden Mile von Estepona, unter den Golfplätzen Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House und Atalaya Golf & Country Club; der Real Club Valderrama in Sotogrande liegt 20 Minuten entfernt. Weitere Entfernungen nennt es nicht.',
  'В досье Haiku расположен в Канселаде, на Новой Золотой миле Эстепоны, среди гольф-клубов Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House и Atalaya Golf & Country Club; до Real Club Valderrama в Сотогранде — 20 минут. Других расстояний в нём нет.',
  'يضع الملف Haiku في كانسيلادا، على الميل الذهبي الجديد في إستيبونا، بين ملاعب الغولف Flamingos Golf وCancelada Club Golf وEl Campanario Golf & Country House وAtalaya Golf & Country Club، مع Real Club Valderrama في سوتوغراندي على بعد 20 دقيقة. ولا يورد مسافات أخرى.',
  'Het dossier plaatst Haiku in Cancelada, aan de New Golden Mile van Estepona, tussen de golfbanen Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House en Atalaya Golf & Country Club, met de Real Club Valderrama in Sotogrande op 20 minuten. Andere afstanden noemt het niet.',
  'Dossier umieszcza Haiku w Cancelada, na New Golden Mile w Esteponie, wśród pól golfowych Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House i Atalaya Golf & Country Club; Real Club Valderrama w Sotogrande jest oddalony o 20 minut. Innych odległości nie podaje.',
  'Dossieret plasserer Haiku i Cancelada, på New Golden Mile i Estepona, blant golfbanene Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House og Atalaya Golf & Country Club, med Real Club Valderrama i Sotogrande 20 minutter unna. Det oppgir ingen andre avstander.',
  'Dossiern placerar Haiku i Cancelada, på New Golden Mile i Estepona, bland golfbanorna Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House och Atalaya Golf & Country Club, med Real Club Valderrama i Sotogrande 20 minuter bort. Den anger inga andra avstånd.')
a('.why.points[3][1]',
  'La lista del 26 de octubre de 2026 marca 28 de las 51 viviendas como reservadas, y 23 tienen precio. Los documentos no dan fecha de entrega ni fase de las obras, de modo que confirmamos ambas antes de cualquier reserva.',
  'La liste du 26 octobre 2026 marque 28 des 51 logements comme réservés, et 23 ont un prix. Les documents ne donnent ni date de livraison ni état d’avancement des travaux ; nous confirmons les deux avant toute réservation.',
  'Die Liste vom 26. Oktober 2026 kennzeichnet 28 der 51 Immobilien als reserviert, 23 haben einen Preis. Die Dokumente nennen weder einen Fertigstellungstermin noch den Baustand; beides bestätigen wir vor jeder Reservierung.',
  'В списке от 26 октября 2026 года 28 из 51 объекта отмечены как забронированные, у 23 указана цена. В документах нет ни срока сдачи, ни стадии строительства; мы подтверждаем и то и другое до любого бронирования.',
  'تشير القائمة المؤرخة في 26 أكتوبر 2026 إلى أن 28 من أصل 51 مسكنًا محجوزة، ولـ 23 منها سعر. ولا تذكر الوثائق موعد الإنجاز ولا مرحلة الأعمال، ولذلك نؤكد الأمرين قبل أي حجز.',
  'De lijst van 26 oktober 2026 markeert 28 van de 51 woningen als gereserveerd, en 23 hebben een prijs. De documenten noemen geen opleveringsdatum en geen bouwfase; beide bevestigen wij vóór elke reservering.',
  'Lista z 26 października 2026 r. oznacza 28 z 51 lokali jako zarezerwowane, a 23 mają cenę. Dokumenty nie podają terminu odbioru ani etapu prac, więc potwierdzamy oba te elementy przed jakąkolwiek rezerwacją.',
  'Listen fra 26. oktober 2026 markerer 28 av de 51 boligene som reservert, og 23 har pris. Dokumentene oppgir verken ferdigstillelsesdato eller byggetrinn, så vi bekrefter begge deler før enhver reservasjon.',
  'Listan från den 26 oktober 2026 markerar 28 av de 51 bostäderna som reserverade, och 23 har ett pris. Dokumenten anger varken färdigställandedatum eller byggstadium, så vi bekräftar båda före varje reservation.')

a('.architecture.headlineHtml',
  'Diseño contemporáneo, <em>en ladera</em>',
  'Une architecture contemporaine, <em>à flanc de colline</em>',
  'Zeitgenössische Architektur, <em>am Hang</em>',
  'Современная архитектура <em>на склоне холма</em>',
  'تصميم معاصر <em>على سفح تلة</em>',
  'Eigentijds ontwerp, <em>op een heuvelhelling</em>',
  'Współczesny projekt <em>na zboczu wzgórza</em>',
  'Moderne design, <em>i en li</em>',
  'Modern design, <em>i en sluttning</em>')
a('.architecture.copy[0]',
  'El dosier describe un diseño contemporáneo y funcional, con interiores abiertos, grandes ventanales y amplias terrazas orientadas al suroeste, en una ladera mediterránea donde se encuentran el mar y la montaña. En las imágenes generadas por ordenador del promotor, los bloques de apartamentos tienen terrazas escalonadas y ajardinadas con barandillas de vidrio, y los adosados forman hileras escalonadas delante de ellos.',
  'Le dossier décrit un design contemporain et fonctionnel, avec des intérieurs ouverts, de grandes baies vitrées et de vastes terrasses orientées sud-ouest, sur un flanc de colline méditerranéen où se rencontrent la mer et la montagne. Dans les images générées par ordinateur du promoteur, les immeubles d’appartements ont des terrasses en gradins plantées, aux garde-corps en verre, et les maisons mitoyennes forment des rangées étagées devant eux.',
  'Das Dossier beschreibt ein zeitgemäßes, funktionales Design mit offenen Grundrissen, großen Fenstern und weitläufigen Terrassen nach Südwesten, an einem mediterranen Hang, an dem sich Meer und Berge begegnen. In den computergenerierten Bildern des Bauträgers haben die Wohnblöcke abgestufte, bepflanzte Terrassen mit Glasbrüstungen, und die Reihenhäuser stehen in gestaffelten Reihen davor.',
  'В досье описан современный функциональный дизайн с открытой планировкой, большими окнами и просторными террасами, выходящими на юго-запад, на средиземноморском склоне, где встречаются море и горы. На компьютерных изображениях застройщика жилые корпуса имеют ступенчатые озеленённые террасы со стеклянными ограждениями, а перед ними рядами стоят таунхаусы.',
  'يصف الملف تصميمًا معاصرًا وعمليًا بمساحات داخلية مفتوحة ونوافذ كبيرة وتراسات واسعة متجهة نحو الجنوب الغربي، على سفح متوسطي يلتقي فيه البحر بالجبال. وفي الصور المولّدة بالحاسوب لدى المطوّر تظهر في المباني السكنية تراسات متدرجة ومزروعة بحواجز زجاجية، فيما تقف المنازل المتلاصقة في صفوف مدرّجة أمامها.',
  'Het dossier beschrijft een eigentijds en functioneel ontwerp, met open interieurs, grote ramen en ruime terrassen op het zuidwesten, op een mediterrane heuvelhelling waar de zee en de bergen elkaar ontmoeten. In de computergegenereerde beelden van de ontwikkelaar hebben de appartementenblokken getrapte, beplante terrassen met glazen balustrades, en de herenhuizen staan in gestaffelde rijen ervoor.',
  'Dossier opisuje współczesny, funkcjonalny projekt z otwartymi wnętrzami, dużymi oknami i przestronnymi tarasami od strony południowo-zachodniej, na śródziemnomorskim zboczu, gdzie spotykają się morze i góry. Na wygenerowanych komputerowo obrazach dewelopera budynki z mieszkaniami mają schodkowe, obsadzone roślinami tarasy ze szklanymi balustradami, a przed nimi stoją domy szeregowe w ustawionych schodkowo rzędach.',
  'Dossieret beskriver et moderne og funksjonelt design med åpne interiører, store vinduer og romslige terrasser mot sørvest, i en middelhavsli der havet og fjellene møtes. På utbyggers datagenererte bilder har leilighetsblokkene trappetrinnsformede, beplantede terrasser med glassrekkverk, og rekkehusene står i trinnvise rader foran dem.',
  'Dossiern beskriver en modern och funktionell design med öppna interiörer, stora fönster och rymliga terrasser åt sydväst, i en medelhavssluttning där havet och bergen möts. På exploatörens datorgenererade bilder har lägenhetshusen trappstegsformade, planterade terrasser med glasräcken, och radhusen står i förskjutna rader framför dem.')
a('.architecture.copy[1]',
  'El dosier dice que los apartamentos incluyen viviendas en planta baja con jardín o grandes terrazas, dúplex y áticos con solárium, y que los adosados tienen terrazas y solárium. La lista no indica qué apartamentos son dúplex o áticos. En sus planos, los 13 apartamentos con precio tienen dos dormitorios y dos baños, y los adosados, tres dormitorios.',
  'Le dossier indique que les appartements comprennent des logements en rez-de-chaussée avec jardin ou grandes terrasses, des duplex et des penthouses avec solarium, et que les maisons mitoyennes ont des terrasses et des solariums. La liste ne précise pas quels appartements sont des duplex ou des penthouses. Sur leurs plans, les 13 appartements avec prix ont deux chambres et deux salles de bains, et les maisons mitoyennes trois chambres.',
  'Laut Dossier gehören zu den Wohnungen Erdgeschosswohnungen mit Garten oder großen Terrassen sowie Duplex- und Penthouse-Wohnungen mit Solarium, und die Reihenhäuser haben Terrassen und Solarien. Die Liste sagt nicht, welche Wohnungen Duplex- oder Penthouse-Wohnungen sind. Auf ihren Plänen haben die 13 Wohnungen mit Preis zwei Schlafzimmer und zwei Bäder, die Reihenhäuser drei Schlafzimmer.',
  'В досье сказано, что среди квартир есть жильё на первом этаже с садом или большими террасами, дуплексы и пентхаусы с солярием, а у таунхаусов — террасы и солярии. В списке не указано, какие квартиры являются дуплексами или пентхаусами. По планам, у 13 квартир с ценой по две спальни и две ванные комнаты, у таунхаусов — по три спальни.',
  'يذكر الملف أن الشقق تشمل مساكن في الطابق الأرضي مع حديقة أو تراسات كبيرة، ودوبلكس وبنتهاوس مع سولاريوم، وأن المنازل المتلاصقة لها تراسات وسولاريوم. ولا تبيّن القائمة أي الشقق دوبلكس أو بنتهاوس. وبحسب مخططاتها، فإن الشقق الـ 13 المسعّرة لها غرفتا نوم وحمامان، والمنازل المتلاصقة ثلاث غرف نوم.',
  'Het dossier zegt dat de appartementen bestaan uit woningen op de begane grond met tuin of grote terrassen, duplexen en penthouses met solarium, en dat de herenhuizen terrassen en solariums hebben. De lijst vermeldt niet welke appartementen duplexen of penthouses zijn. Op hun plattegronden hebben de 13 appartementen met een prijs twee slaapkamers en twee badkamers, en de herenhuizen drie slaapkamers.',
  'Dossier podaje, że wśród mieszkań są lokale na parterze z ogrodem lub dużymi tarasami, dupleksy i penthouse’y z solarium, a domy szeregowe mają tarasy i solaria. Cennik nie wskazuje, które mieszkania są dupleksami lub penthouse’ami. Na rzutach 13 mieszkań z ceną ma po dwie sypialnie i dwie łazienki, a domy szeregowe po trzy sypialnie.',
  'Dossieret sier at leilighetene omfatter boliger i første etasje med hage eller store terrasser, dupleksleiligheter og toppleiligheter med solarium, og at rekkehusene har terrasser og solarier. Listen sier ikke hvilke leiligheter som er dupleks eller toppleiligheter. På planene har de 13 leilighetene med pris to soverom og to bad, og rekkehusene tre soverom.',
  'Dossiern säger att lägenheterna omfattar bostäder i bottenvåningen med trädgård eller stora terrasser, duplexlägenheter och takvåningar med solterrass, och att radhusen har terrasser och solterrasser. Listan anger inte vilka lägenheter som är duplex eller takvåningar. På ritningarna har de 13 lägenheterna med pris två sovrum och två badrum, och radhusen tre sovrum.')
a('.architecture.highlights[0][1]',
  'Revoco de mortero con acabado de hormigón, con revestimientos de material compuesto o de madera, en acabado metálico o madera.',
  'Enduit de mortier à finition béton, avec des bardages composites ou en bois, à finition métal ou bois.',
  'Mörtelputz in Betonoptik, mit Verkleidungen aus Verbundwerkstoff oder Holz in Metall- oder Holzoptik.',
  'Фасад из штукатурки с бетонной фактурой, с облицовкой из композита или дерева с отделкой под металл или дерево.',
  'واجهة من ملاط بلمسة نهائية تشبه الخرسانة، مع كسوة من مادة مركّبة أو من الخشب بلمسة معدنية أو خشبية.',
  'Gevelpleister met een betonafwerking, met bekleding van composiet of hout in een metaal- of houtafwerking.',
  'Tynk mineralny o fakturze betonu, z okładziną z kompozytu lub drewna w wykończeniu metalowym lub drewnopodobnym.',
  'Mørtelpuss med betongfinish, med kledning av kompositt eller tre i metall- eller trefinish.',
  'Fasadputs med betongfinish, med fasadbeklädnad av komposit eller trä i metall- eller trälook.')
a('.architecture.highlights[1][1]',
  'Puertas y ventanas oscilobatientes o correderas de aluminio lacado de una marca líder, con doble acristalamiento, y barandillas de vidrio con cantos biselados fijadas al forjado.',
  'Portes et fenêtres oscillo-battantes ou coulissantes en aluminium laqué d’une marque de référence, avec double vitrage, et garde-corps en verre à chants biseautés fixés à la dalle.',
  'Dreh-Kipp- oder Schiebetüren und -fenster aus lackiertem Aluminium eines führenden Herstellers, mit Doppelverglasung, sowie Glasbrüstungen mit abgeschrägten Kanten, an der Decke befestigt.',
  'Поворотно-откидные или раздвижные двери и окна из лакированного алюминия ведущего бренда с двойным остеклением и стеклянные ограждения со скошенными кромками, закреплённые на перекрытии.',
  'أبواب ونوافذ قلّابة أو منزلقة من الألمنيوم المطلي لعلامة رائدة، بزجاج مزدوج، وحواجز زجاجية بحواف مشطوفة مثبّتة في البلاطة.',
  'Kantel-draai- of schuifdeuren en -ramen van gelakt aluminium van een toonaangevend merk, met dubbele beglazing, en glazen balustrades met afgeschuinde randen, bevestigd aan de vloerplaat.',
  'Drzwi i okna uchylno-przesuwne lub przesuwne z lakierowanego aluminium wiodącej marki, z podwójnym szkleniem, oraz szklane balustrady ze ściętymi krawędziami, zamocowane do stropu.',
  'Vipp- eller skyvedører og -vinduer i lakkert aluminium fra et ledende merke, med dobbeltglass, og glassrekkverk med skrå kanter festet til dekket.',
  'Vippbara eller skjutbara dörrar och fönster i lackerad aluminium från ett ledande märke, med dubbelglas, och glasräcken med fasade kanter fästa i bjälklaget.')
a('.architecture.highlights[2][1]',
  'Gres porcelánico rectificado de 90 x 90 cm en el interior y, en grado antideslizante C3, en las terrazas, con rodapié de porcelánico de 10 x 90 cm.',
  'Carrelage en grès cérame rectifié de 90 x 90 cm à l’intérieur et, en classe antidérapante C3, sur les terrasses, avec plinthe en grès cérame de 10 x 90 cm.',
  'Rektifizierte Feinsteinzeugfliesen von 90 x 90 cm innen und, in rutschhemmender Klasse C3, auf den Terrassen, mit einer Feinsteinzeugsockelleiste von 10 x 90 cm.',
  'Ректифицированный керамогранит 90 x 90 см внутри и, в противоскользящем исполнении C3, на террасах, с плинтусом из керамогранита 10 x 90 см.',
  'بلاط بورسلين مقصوص بقياس 90 × 90 سم في الداخل، وبدرجة مقاومة الانزلاق C3 على التراسات، مع وزرة من البورسلين بقياس 10 × 90 سم.',
  'Gerectificeerde porseleinen tegels van 90 x 90 cm binnen en, in antislipklasse C3, op de terrassen, met een porseleinen plint van 10 x 90 cm.',
  'Gres porcelanowy rektyfikowany 90 x 90 cm wewnątrz i, w klasie antypoślizgowości C3, na tarasach, z listwą przypodłogową z gresu 10 x 90 cm.',
  'Rektifiserte porselensfliser på 90 x 90 cm inne og, i sklisikker klasse C3, på terrassene, med en list av porselen på 10 x 90 cm.',
  'Rektifierat klinker på 90 x 90 cm inomhus och, i halkskyddsklass C3, på terrasserna, med en list av klinker på 10 x 90 cm.')
a('.architecture.highlights[3][0]', 'Zonas exteriores', 'Espaces extérieurs', 'Außenbereiche', 'Открытые пространства', 'المساحات الخارجية', 'Buitenruimtes', 'Tereny zewnętrzne', 'Uteområder', 'Utomhusytor')
a('.architecture.highlights[3][1]',
  'Una franja central de jardines con grandes palmeras, láminas de agua y una cascada entre los edificios, piscinas de formas orgánicas y zonas de chill-out y yoga con vestuarios.',
  'Une bande centrale de jardins avec de grands palmiers, des plans d’eau et une cascade entre les bâtiments, des piscines aux formes organiques et des espaces de détente et de yoga avec vestiaires.',
  'Ein zentraler Gartenstreifen mit großen Palmen, Wasserspielen und einem Wasserfall zwischen den Gebäuden, Pools in organischen Formen sowie Chill-out- und Yoga-Bereiche mit Umkleiden.',
  'Центральная полоса садов с высокими пальмами, водными элементами и водопадом между зданиями, бассейны органичной формы, а также зоны для отдыха и йоги с раздевалками.',
  'شريط مركزي من الحدائق بنخيل كبير وعناصر مائية وشلال بين المباني، ومسابح بأشكال عضوية، ومناطق للاسترخاء واليوغا مع غرف تبديل ملابس.',
  'Een centrale strook tuinen met grote palmen, waterpartijen en een waterval tussen de gebouwen, zwembaden met organische vormen en chill-out- en yogaruimtes met kleedkamers.',
  'Centralny pas ogrodów z dużymi palmami, elementami wodnymi i wodospadem między budynkami, baseny o organicznych kształtach oraz strefy relaksu i jogi z szatniami.',
  'En sentral stripe med hager med store palmer, vannspeil og en foss mellom byggene, basseng med organiske former og chill-out- og yogaområder med garderober.',
  'En central trädgårdsremsa med stora palmer, vattenspeglar och ett vattenfall mellan byggnaderna, pooler med organiska former samt chill-out- och yogaytor med omklädningsrum.')

# ---- quality specifications ---------------------------------------------------------------------

a('.qualitySpecs.copy',
  'La memoria de calidades del propio promotor, resumida por partes de la vivienda.',
  'Le descriptif des prestations du promoteur, résumé par partie du logement.',
  'Die Ausstattungsbeschreibung des Bauträgers, nach Bereichen der Immobilie zusammengefasst.',
  'Спецификация отделки от самого застройщика, сгруппированная по частям жилья.',
  'مواصفات الجودة الصادرة عن المطوّر نفسه، مُلخَّصة حسب أجزاء المسكن.',
  'De technische omschrijving van de ontwikkelaar zelf, samengevat per deel van de woning.',
  'Standard wykończenia samego dewelopera, podsumowany według części lokalu.',
  'Utbyggerens egen byggebeskrivelse, oppsummert etter del av boligen.',
  'Exploatörens egen byggnadsbeskrivning, sammanfattad efter del av bostaden.')
a('.qualitySpecs.sourceNote',
  'Fuente: las memorias de calidades de Haiku Suites y Haiku Residences, en español, cuyos nombres de archivo indican 18 de agosto y no llevan año. Dicen que son solo orientativas: el promotor puede introducir cambios por razones técnicas, legales o de la administración pública y sustituir partidas por otras de igual o mayor calidad, y las imágenes no son contractuales. Las partidas marcadas como opción están por consultar, de modo que confirmamos lo que se aplica a la vivienda que usted elija.',
  'Source : les descriptifs des prestations de Haiku Suites et de Haiku Residences, en espagnol, dont les noms de fichier indiquent le 18 août et ne portent pas d’année. Ils précisent qu’ils ne sont qu’indicatifs : le promoteur peut y apporter des modifications pour des raisons techniques, juridiques ou imposées par l’administration, et remplacer des éléments par d’autres de qualité égale ou supérieure ; les images ne sont pas contractuelles. Les éléments marqués comme option sont à consulter ; nous confirmons donc ce qui s’applique au logement que vous choisissez.',
  'Quelle: die Ausstattungsbeschreibungen für Haiku Suites und Haiku Residences, auf Spanisch, deren Dateinamen „18. August“ lauten und kein Jahr tragen. Sie weisen darauf hin, dass sie nur ein Anhaltspunkt sind: Der Bauträger darf aus technischen, rechtlichen oder behördlichen Gründen Änderungen vornehmen und Positionen durch gleich- oder höherwertige ersetzen, und die Abbildungen sind nicht vertraglich bindend. Als Option gekennzeichnete Positionen sind noch zu klären; wir bestätigen daher, was für die von Ihnen gewählte Immobilie gilt.',
  'Источник: спецификации отделки Haiku Suites и Haiku Residences на испанском языке, в названиях файлов которых указано 18 августа без года. В них сказано, что они носят лишь ориентировочный характер: застройщик может вносить изменения по техническим, юридическим причинам или по требованию органов власти и заменять позиции равнозначными или более качественными, а изображения не являются договорными. Позиции, помеченные как опции, подлежат уточнению, поэтому мы подтверждаем, что относится к выбранному вами объекту.',
  'المصدر: مواصفات الجودة لـ Haiku Suites وHaiku Residences، بالإسبانية، وتحمل أسماء ملفاتها عبارة «18 أغسطس» دون سنة. وتذكر أنها للاسترشاد فقط: فيجوز للمطوّر إجراء تغييرات لأسباب فنية أو قانونية أو بطلب من الجهات العامة، واستبدال بنود ببنود مماثلة أو أعلى جودة، والصور غير ملزمة تعاقديًا. أما البنود المصنّفة كخيارات فيُرجع إليها للاستفسار، ولذلك نؤكد ما ينطبق على المسكن الذي تختارونه.',
  'Bron: de technische omschrijvingen van Haiku Suites en Haiku Residences, in het Spaans, waarvan de bestandsnamen “18 augustus” vermelden en geen jaartal dragen. Ze zeggen dat ze slechts een richtlijn zijn: de ontwikkelaar mag om technische, juridische of overheidsredenen wijzigingen aanbrengen en onderdelen vervangen door andere van gelijke of betere kwaliteit, en de beelden zijn niet contractueel. Onderdelen die als optie zijn aangemerkt, moeten nog worden nagevraagd; wij bevestigen daarom wat geldt voor de woning die u kiest.',
  'Źródło: standardy wykończenia Haiku Suites i Haiku Residences, w języku hiszpańskim, w których nazwach plików widnieje „18 sierpnia” bez roku. Zastrzegają one, że mają charakter orientacyjny: deweloper może wprowadzać zmiany z przyczyn technicznych, prawnych lub z polecenia organów publicznych oraz zastępować pozycje innymi o równej lub wyższej jakości, a wizualizacje nie mają charakteru umownego. Pozycje oznaczone jako opcje należy dopytać, dlatego potwierdzamy, co dotyczy wybranego przez Pana/Panią lokalu.',
  'Kilde: byggebeskrivelsene for Haiku Suites og Haiku Residences, på spansk, hvis filnavn angir «18. august» uten årstall. De sier at de bare er veiledende: utbygger kan gjøre endringer av tekniske, juridiske eller offentligrettslige grunner og erstatte poster med andre av lik eller bedre kvalitet, og bildene er ikke kontraktsfestet. Poster merket som tilvalg må forhøres om, så vi bekrefter hva som gjelder for boligen De velger.',
  'Källa: byggnadsbeskrivningarna för Haiku Suites och Haiku Residences, på spanska, vars filnamn anger ”18 augusti” utan årtal. De säger att de endast är vägledande: exploatören får göra ändringar av tekniska, juridiska eller myndighetsmässiga skäl och ersätta poster med andra av likvärdig eller bättre kvalitet, och bilderna är inte avtalsenliga. Poster som är markerade som tillval ska efterfrågas, så vi bekräftar vad som gäller för den bostad ni väljer.')

a('.qualitySpecs.groups[0].items[0]',
  'Gres porcelánico rectificado de 90 x 90 cm en toda la vivienda, en grado antideslizante C3 en las terrazas, con rodapié de porcelánico de 10 x 90 cm.',
  'Carrelage en grès cérame rectifié de 90 x 90 cm dans tout le logement, en classe antidérapante C3 sur les terrasses, avec plinthe en grès cérame de 10 x 90 cm.',
  'Rektifizierte Feinsteinzeugfliesen von 90 x 90 cm in der gesamten Immobilie, auf den Terrassen in rutschhemmender Klasse C3, mit einer Feinsteinzeugsockelleiste von 10 x 90 cm.',
  'Ректифицированный керамогранит 90 x 90 см во всём жилье, на террасах — в противоскользящем исполнении C3, с плинтусом из керамогранита 10 x 90 см.',
  'بلاط بورسلين مقصوص بقياس 90 × 90 سم في أرجاء المسكن كله، وبدرجة مقاومة الانزلاق C3 على التراسات، مع وزرة من البورسلين بقياس 10 × 90 سم.',
  'Gerectificeerde porseleinen tegels van 90 x 90 cm in de hele woning, in antislipklasse C3 op de terrassen, met een porseleinen plint van 10 x 90 cm.',
  'Gres porcelanowy rektyfikowany 90 x 90 cm w całym lokalu, w klasie antypoślizgowości C3 na tarasach, z listwą przypodłogową z gresu 10 x 90 cm.',
  'Rektifiserte porselensfliser på 90 x 90 cm i hele boligen, i sklisikker klasse C3 på terrassene, med en list av porselen på 10 x 90 cm.',
  'Rektifierat klinker på 90 x 90 cm i hela bostaden, i halkskyddsklass C3 på terrasserna, med en list av klinker på 10 x 90 cm.')
a('.qualitySpecs.groups[0].items[1]',
  'En los baños, porcelánico rectificado de 60 x 120 cm alrededor del lavabo y de la ducha, con el resto de las paredes pintadas de blanco. El porcelánico rectificado de gran formato de 120 x 280 cm, mate, en beige o dorado, es una opción.',
  'Dans les salles de bains, grès cérame rectifié de 60 x 120 cm autour du lavabo et de la douche, les autres murs étant peints en blanc. Le grès cérame rectifié grand format de 120 x 280 cm, mat, beige ou doré, est proposé en option.',
  'In den Bädern rektifiziertes Feinsteinzeug von 60 x 120 cm um Waschtisch und Dusche, die übrigen Wände weiß gestrichen. Großformatiges rektifiziertes Feinsteinzeug von 120 x 280 cm, matt, in Beige oder Gold, ist eine Option.',
  'В ванных комнатах — ректифицированный керамогранит 60 x 120 см вокруг раковины и душа, остальные стены окрашены в белый цвет. Крупноформатный ректифицированный керамогранит 120 x 280 см, матовый, бежевый или золотистый, предлагается как опция.',
  'في الحمامات بلاط بورسلين مقصوص بقياس 60 × 120 سم حول المغسلة والدش، مع طلاء بقية الجدران باللون الأبيض. أما البورسلين المقصوص كبير القياس 120 × 280 سم، المطفأ، بلون بيج أو ذهبي، فهو خيار.',
  'In de badkamers gerectificeerd porselein van 60 x 120 cm rond de wastafel en de douche, met de overige wanden wit geschilderd. Groot formaat gerectificeerd porselein van 120 x 280 cm, mat, in beige of goud, is een optie.',
  'W łazienkach gres rektyfikowany 60 x 120 cm wokół umywalki i prysznica, pozostałe ściany malowane na biało. Wielkoformatowy gres rektyfikowany 120 x 280 cm, matowy, w kolorze beżowym lub złotym, jest opcją.',
  'På badene rektifisert porselen på 60 x 120 cm rundt servanten og dusjen, med de øvrige veggene malt hvite. Storformat rektifisert porselen på 120 x 280 cm, matt, i beige eller gull, er et tilvalg.',
  'I badrummen rektifierat klinker på 60 x 120 cm runt handfatet och duschen, med övriga väggar målade vita. Storformatigt rektifierat klinker på 120 x 280 cm, matt, i beige eller guld, är ett tillval.')
a('.qualitySpecs.groups[1].items[0]',
  'Grifería negra mate, electrodomésticos Siemens y encimera de gres porcelánico. La mejora a electrodomésticos Gaggenau es una opción.',
  'Robinetterie noir mat, électroménager Siemens et plan de travail en grès cérame. La mise à niveau vers l’électroménager Gaggenau est proposée en option.',
  'Mattschwarze Armaturen, Siemens-Geräte und eine Arbeitsplatte aus Feinsteinzeug. Ein Upgrade auf Gaggenau-Geräte ist eine Option.',
  'Матовые чёрные смесители, техника Siemens и столешница из керамогранита. Замена на технику Gaggenau предлагается как опция.',
  'خلاطات سوداء مطفأة وأجهزة Siemens وسطح عمل من حجر البورسلين. والترقية إلى أجهزة Gaggenau خيار.',
  'Matzwarte kranen, Siemens-apparatuur en een werkblad van porseleinen steengoed. Een upgrade naar Gaggenau-apparatuur is een optie.',
  'Baterie w kolorze matowej czerni, sprzęt Siemens i blat z gresu porcelanowego. Zmiana na sprzęt Gaggenau jest opcją.',
  'Matt svarte armaturer, Siemens-hvitevarer og en benkeplate i porselensstein. Oppgradering til Gaggenau-hvitevarer er et tilvalg.',
  'Matt svarta blandare, Siemens-vitvaror och en bänkskiva i klinker. Uppgradering till Gaggenau-vitvaror är ett tillval.')
a('.qualitySpecs.groups[2].items[0]',
  'Lavabos de superficie sólida sobre muebles de roble: de 70 cm en los baños principales, de 100 cm en los segundos baños y un mueble de 60 cm con lavabo de 60 x 42 cm en los aseos de cortesía.',
  'Vasques en solid surface sur meubles en chêne : 70 cm dans les salles de bains principales, 100 cm dans les secondes salles de bains et un meuble de 60 cm avec vasque de 60 x 42 cm dans les toilettes d’invités.',
  'Waschtische aus Mineralwerkstoff auf Eichenunterschränken: 70 cm in den Hauptbädern, 100 cm in den zweiten Bädern und ein 60-cm-Unterschrank mit einem Becken von 60 x 42 cm in den Gäste-WCs.',
  'Раковины из искусственного камня на тумбах из дуба: 70 см в основных ванных комнатах, 100 см во вторых ванных комнатах и тумба 60 см с раковиной 60 x 42 см в гостевых санузлах.',
  'مغاسل من مادة صلبة على خزائن من خشب البلوط: بعرض 70 سم في الحمامات الرئيسية و100 سم في الحمامات الثانية، وخزانة بعرض 60 سم بحوض 60 × 42 سم في دورات المياه الصغيرة.',
  'Wastafels van solid surface op eikenhouten onderkasten: 70 cm in de hoofdbadkamers, 100 cm in de tweede badkamers en een kast van 60 cm met een wastafel van 60 x 42 cm in de gastentoiletten.',
  'Umywalki z kompozytu mineralnego na dębowych szafkach: 70 cm w łazienkach głównych, 100 cm w drugich łazienkach oraz szafka 60 cm z umywalką 60 x 42 cm w toaletach gościnnych.',
  'Servanter i solid surface på eikeskap: 70 cm på hovedbadene, 100 cm på de andre badene og et skap på 60 cm med en servant på 60 x 42 cm på gjestetoalettene.',
  'Handfat i solid surface på ekskåp: 70 cm i de stora badrummen, 100 cm i de andra badrummen och ett skåp på 60 cm med ett handfat på 60 x 42 cm på gästtoaletterna.')
a('.qualitySpecs.groups[2].items[1]',
  'Inodoros suspendidos con cisterna empotrada, grifería grafito cepillado con ducha termostática y ducha higiénica, plato de ducha de resina con mampara fija de vidrio de 8 mm antical y espejos retroiluminados.',
  'WC suspendus à réservoir encastré, robinetterie graphite brossé avec douche thermostatique et douchette hygiénique, receveur de douche en résine avec paroi fixe en verre de 8 mm anticalcaire et miroirs rétroéclairés.',
  'Wandhängende WCs mit Unterputzspülkasten, Armaturen in gebürstetem Graphit mit Thermostat-Duschsystem und Bidetdusche, eine Duschwanne aus Kunstharz mit fester 8-mm-Glasabtrennung mit Kalkschutz und hinterleuchtete Spiegel.',
  'Подвесные унитазы со скрытым бачком, смесители из матового графита с термостатическим душем и гигиеническим душем, душевой поддон из смолы с неподвижной стеклянной перегородкой 8 мм с защитой от известкового налёта и зеркала с подсветкой.',
  'مراحيض معلّقة بخزان مخفي، وخلاطات بلون الغرافيت المصقول مع دش بمنظّم حراري ودش صحي، وحوض دش من الراتنج مع حاجز زجاجي ثابت بسماكة 8 مم مقاوم للكلس، ومرايا بإضاءة خلفية.',
  'Wandtoiletten met inbouwreservoir, kranen in geborsteld grafiet met een thermostatische douche en een bidetdouche, een douchebak van hars met een vast glazen scherm van 8 mm met kalkbeschermlaag en spiegels met achtergrondverlichting.',
  'Toalety podwieszane z ukrytym spłukiwaniem, baterie w kolorze szczotkowanego grafitu z prysznicem termostatycznym i prysznicem higienicznym, brodzik z żywicy ze stałą szklaną ścianką 8 mm z powłoką antykamienną oraz lustra z podświetleniem.',
  'Veggmonterte toaletter med skjult sisterne, armaturer i børstet grafitt med termostatstyrt dusj og bidédusj, en dusjkum av harpiks med fast 8 mm glassvegg med kalkbeskyttelse og speil med bakgrunnsbelysning.',
  'Väggmonterade toaletter med dold cistern, blandare i borstad grafit med termostatdusch och bidédusch, en duschkar av harts med fast 8 mm glasvägg med kalkskydd och speglar med bakgrundsbelysning.')
a('.qualitySpecs.groups[3].name',
  'Ventanas, puertas y armarios', 'Fenêtres, portes et placards', 'Fenster, Türen und Einbauschränke', 'Окна, двери и шкафы',
  'النوافذ والأبواب والخزائن', 'Ramen, deuren en kasten', 'Okna, drzwi i szafy', 'Vinduer, dører og garderober', 'Fönster, dörrar och garderober')
a('.qualitySpecs.groups[3].items[0]',
  'Puertas y ventanas de aluminio lacado, oscilobatientes o correderas, con doble acristalamiento según indique el fabricante, y barandillas de vidrio con cantos biselados.',
  'Portes et fenêtres en aluminium laqué, oscillo-battantes ou coulissantes, avec double vitrage selon les indications du fabricant, et garde-corps en verre à chants biseautés.',
  'Türen und Fenster aus lackiertem Aluminium, Dreh-Kipp oder Schiebe, mit Doppelverglasung nach Herstellerangabe, und Glasbrüstungen mit abgeschrägten Kanten.',
  'Двери и окна из лакированного алюминия, поворотно-откидные или раздвижные, с двойным остеклением по данным производителя, и стеклянные ограждения со скошенными кромками.',
  'أبواب ونوافذ من الألمنيوم المطلي، قلّابة أو منزلقة، بزجاج مزدوج وفق ما يحدده المصنّع، وحواجز زجاجية بحواف مشطوفة.',
  'Deuren en ramen van gelakt aluminium, kantel-draai of schuivend, met dubbele beglazing zoals de fabrikant aangeeft, en glazen balustrades met afgeschuinde randen.',
  'Drzwi i okna z lakierowanego aluminium, uchylno-przesuwne lub przesuwne, z podwójnym szkleniem zgodnie z danymi producenta, oraz szklane balustrady ze ściętymi krawędziami.',
  'Dører og vinduer i lakkert aluminium, vipp eller skyv, med dobbeltglass slik produsenten angir, og glassrekkverk med skrå kanter.',
  'Dörrar och fönster i lackerad aluminium, vippbara eller skjutbara, med dubbelglas enligt tillverkarens uppgifter, och glasräcken med fasade kanter.')
a('.qualitySpecs.groups[3].items[1]',
  'Armarios con frentes correderos o abatibles en tablero grueso, un vestidor con revestimiento interior en el dormitorio principal y armarios con cajones en los demás, con puertas de paso del mismo material. Los acabados en negro o en madera son opciones.',
  'Placards à façades coulissantes ou battantes en panneau épais, un dressing avec habillage intérieur dans la chambre principale et des placards avec tiroirs dans les autres, avec des portes intérieures du même matériau. Les finitions noires ou bois sont proposées en option.',
  'Einbauschränke mit Schiebe- oder Drehtüren aus starker Platte, ein begehbarer Kleiderschrank mit Innenverkleidung im Hauptschlafzimmer und Schränke mit Schubladen in den übrigen, mit Innentüren aus demselben Material. Schwarze oder holzfarbene Ausführungen sind Optionen.',
  'Шкафы с раздвижными или распашными фасадами из толстой плиты, гардеробная с внутренней отделкой в главной спальне и шкафы с ящиками в остальных, с межкомнатными дверями из того же материала. Чёрная отделка или отделка под дерево предлагаются как опции.',
  'خزائن بواجهات منزلقة أو مفصلية من لوح سميك، وغرفة تبديل ملابس ببطانة داخلية في غرفة النوم الرئيسية، وخزائن بأدراج في بقية الغرف، مع أبواب داخلية من المادة نفسها. والتشطيبات باللون الأسود أو الخشبي خيارات.',
  'Kasten met schuif- of draaideuren van dik plaatmateriaal, een inloopkast met binnenbekleding in de hoofdslaapkamer en kasten met laden in de overige, met binnendeuren van hetzelfde materiaal. Zwarte of houten afwerkingen zijn opties.',
  'Szafy z frontami przesuwnymi lub otwieranymi z grubej płyty, garderoba z wykończeniem wnętrza w sypialni głównej i szafy z szufladami w pozostałych, z drzwiami wewnętrznymi z tego samego materiału. Wykończenia w czerni lub drewnie są opcjami.',
  'Garderober med skyve- eller slagdører av tykk plate, en walk-in-garderobe med innvendig kledning på hovedsoverommet og garderober med skuffer på de andre, med innerdører av samme materiale. Svarte eller trefinérte utførelser er tilvalg.',
  'Garderober med skjut- eller slagdörrar av tjock skiva, ett walk-in-closet med invändig beklädnad i huvudsovrummet och garderober med lådor i de andra, med innerdörrar av samma material. Svarta eller trädekorerade utföranden är tillval.')
a('.qualitySpecs.groups[4].items[0]',
  'Aire acondicionado por expansión directa, con unidades ecoeficientes en el falso techo y rejillas lineales regulables, agua caliente por aerotermia, suelo radiante por agua en toda la vivienda y suelo radiante eléctrico en los baños.',
  'Climatisation par détente directe, avec des unités éco-efficientes dans le faux plafond et des grilles linéaires réglables, eau chaude par aérothermie, plancher chauffant hydraulique dans tout le logement et plancher chauffant électrique dans les salles de bains.',
  'Klimaanlage mit Direktverdampfung, mit energieeffizienten Geräten in der Abhangdecke und verstellbaren Lineargittern, Warmwasser über Aerothermie, Wasser-Fußbodenheizung in der gesamten Immobilie und elektrische Fußbodenheizung in den Bädern.',
  'Кондиционирование прямого расширения с энергоэффективными блоками в подвесном потолке и регулируемыми линейными решётками, горячая вода от аэротермической системы, водяной тёплый пол во всём жилье и электрический тёплый пол в ванных комнатах.',
  'تكييف بالتمدد المباشر مع وحدات موفّرة للطاقة في السقف المستعار وشبكات خطية قابلة للضبط، وماء ساخن بنظام الطاقة الهوائية الحرارية، وتدفئة أرضية بالماء في المسكن كله وتدفئة أرضية كهربائية في الحمامات.',
  'Airconditioning met directe expansie, met zuinige units in het verlaagde plafond en verstelbare lineaire roosters, warm water via aerothermie, waterverwarmde vloerverwarming in de hele woning en elektrische vloerverwarming in de badkamers.',
  'Klimatyzacja z bezpośrednim odparowaniem, z energooszczędnymi jednostkami w suficie podwieszanym i regulowanymi kratkami liniowymi, ciepła woda z systemu aerotermalnego, wodne ogrzewanie podłogowe w całym lokalu i elektryczne ogrzewanie podłogowe w łazienkach.',
  'Klimaanlegg med direkte ekspansjon, med energieffektive enheter i nedsenket himling og justerbare lineære ventiler, varmtvann fra aerotermisk anlegg, vannbåren gulvvarme i hele boligen og elektrisk gulvvarme på badene.',
  'Luftkonditionering med direktexpansion, med energieffektiva enheter i undertaket och justerbara linjära galler, varmvatten från aerotermiskt system, vattenburen golvvärme i hela bostaden och elektrisk golvvärme i badrummen.')
a('.qualitySpecs.groups[4].items[1]',
  'Ventilación mecánica con conductos ocultos en los falsos techos, según las exigencias del Código Técnico de la Edificación. En los apartamentos, paneles fotovoltaicos apoyan el suministro de las zonas comunes.',
  'Ventilation mécanique avec gaines dissimulées dans les faux plafonds, conformément aux exigences du Code technique du bâtiment. Dans les appartements, des panneaux photovoltaïques contribuent à l’alimentation des parties communes.',
  'Mechanische Lüftung mit in den Abhangdecken verborgenen Kanälen, nach den Anforderungen des spanischen Technischen Baugesetzes (CTE). In den Wohnungen unterstützen Photovoltaikmodule die Versorgung der Gemeinschaftsflächen.',
  'Механическая вентиляция со скрытыми в подвесных потолках воздуховодами в соответствии с требованиями Технического строительного кодекса Испании. В квартирах фотоэлектрические панели участвуют в энергоснабжении общих зон.',
  'تهوية ميكانيكية بقنوات مخفية في الأسقف المستعارة، وفق متطلبات الكود الفني للبناء. وفي الشقق تدعم الألواح الكهروضوئية تزويد المناطق المشتركة بالطاقة.',
  'Mechanische ventilatie met kanalen verborgen in de verlaagde plafonds, volgens de eisen van de Spaanse technische bouwcode. In de appartementen ondersteunen zonnepanelen de voeding van de gemeenschappelijke ruimtes.',
  'Wentylacja mechaniczna z kanałami ukrytymi w sufitach podwieszanych, zgodnie z wymogami hiszpańskiego kodeksu technicznego budownictwa. W mieszkaniach panele fotowoltaiczne wspierają zasilanie części wspólnych.',
  'Mekanisk ventilasjon med kanaler skjult i nedsenket himling, i tråd med kravene i den spanske tekniske byggekoden. I leilighetene støtter solcellepaneler forsyningen til fellesarealene.',
  'Mekanisk ventilation med kanaler dolda i undertaken, enligt kraven i den spanska tekniska byggnormen. I lägenheterna stöder solceller försörjningen av de gemensamma utrymmena.')
a('.qualitySpecs.groups[5].name',
  'Iluminación y tecnología', 'Éclairage et technologie', 'Beleuchtung und Technik', 'Освещение и технологии',
  'الإضاءة والتقنيات', 'Verlichting en technologie', 'Oświetlenie i technologia', 'Belysning og teknologi', 'Belysning och teknik')
a('.qualitySpecs.groups[5].items[0]',
  'Falsos techos de placa de yeso laminado con huecos para raíles de cortinas y cabeceros, y preinstalación de tiras LED para iluminación indirecta en los dormitorios.',
  'Faux plafonds en plaques de plâtre avec réservations pour rails de rideaux et têtes de lit, et préinstallation de bandeaux LED pour un éclairage indirect dans les chambres.',
  'Abhangdecken aus Gipskarton mit Aussparungen für Vorhangschienen und Kopfteile sowie eine Vorinstallation für LED-Streifen zur indirekten Beleuchtung in den Schlafzimmern.',
  'Подвесные потолки из гипсокартона с нишами для карнизов и изголовий и подготовкой под светодиодные ленты для непрямого освещения в спальнях.',
  'أسقف مستعارة من ألواح الجبس مع فتحات لمسارات الستائر ورؤوس الأسرّة، وتمديدات مسبقة لأشرطة LED للإضاءة غير المباشرة في غرف النوم.',
  'Verlaagde plafonds van gipsplaat met uitsparingen voor gordijnrails en hoofdeinden, en een voorbereiding voor ledstrips voor indirecte verlichting in de slaapkamers.',
  'Sufity podwieszane z płyt gipsowo-kartonowych z wnękami na karnisze i zagłówki oraz instalacja przygotowana pod taśmy LED do oświetlenia pośredniego w sypialniach.',
  'Nedsenket himling i gipsplater med utsparinger for gardinskinner og sengegavler, og forberedelse for LED-lister til indirekte belysning på soverommene.',
  'Undertak av gipsskivor med urtag för gardinskenor och sänggavlar, och förberedelse för LED-slingor till indirekt belysning i sovrummen.')
a('.qualitySpecs.groups[5].items[1]',
  'Mecanismos Jung LS990 o similares en blanco, videoportero Fermax o similar, tomas de televisión y teléfono en las estancias principales y control de la climatización desde una aplicación del móvil. Otros elementos de domótica son opciones.',
  'Interrupteurs Jung LS990 ou similaires en blanc, visiophone Fermax ou similaire, prises de télévision et de téléphone dans les pièces principales et pilotage de la climatisation depuis une application sur smartphone. Les autres éléments domotiques sont proposés en option.',
  'Jung-LS990-Schalter oder ähnliche in Weiß, eine Fermax-Videosprechanlage oder ähnlich, Fernseh- und Telefonanschlüsse in den Haupträumen und Klimasteuerung per Smartphone-App. Weitere Hausautomationsbauteile sind Optionen.',
  'Выключатели Jung LS990 или аналогичные белого цвета, видеодомофон Fermax или аналогичный, телевизионные и телефонные розетки в основных комнатах и управление климатом через приложение на смартфоне. Прочие элементы «умного дома» предлагаются как опции.',
  'مفاتيح Jung LS990 أو مثيلة بلون أبيض، وجهاز اتصال مرئي من Fermax أو مثيل، ومنافذ تلفزيون وهاتف في الغرف الرئيسية، والتحكم بالتكييف من تطبيق على الهاتف الذكي. أما عناصر الأتمتة المنزلية الأخرى فهي خيارات.',
  'Jung LS990-schakelaars of vergelijkbaar in wit, een Fermax-videofoon of vergelijkbaar, tv- en telefoonaansluitingen in de hoofdvertrekken en klimaatbediening via een smartphone-app. Andere domotica-onderdelen zijn opties.',
  'Łączniki Jung LS990 lub podobne w kolorze białym, wideodomofon Fermax lub podobny, gniazda telewizyjne i telefoniczne w głównych pomieszczeniach oraz sterowanie klimatyzacją z aplikacji na smartfonie. Pozostałe elementy automatyki domowej są opcjami.',
  'Jung LS990-brytere eller tilsvarende i hvitt, Fermax-porttelefon med video eller tilsvarende, TV- og telefonuttak i hovedrommene og klimastyring fra en app på mobilen. Andre elementer for hjemmeautomatisering er tilvalg.',
  'Jung LS990-strömbrytare eller motsvarande i vitt, Fermax-porttelefon med video eller motsvarande, tv- och telefonuttag i huvudrummen och klimatstyrning från en app i mobilen. Andra delar av hemautomation är tillval.')
a('.qualitySpecs.groups[6].name',
  'Opciones y extras', 'Options et extras', 'Optionen und Extras', 'Опции и дополнения',
  'الخيارات والإضافات', 'Opties en extra’s', 'Opcje i dodatki', 'Tilvalg og ekstrautstyr', 'Tillval och extra')
a('.qualitySpecs.groups[6].items[0]',
  'Para los adosados, la memoria incluye como estándar una piscina privada en el solárium, una barra en el solárium, un ascensor privado en cada vivienda y un cerramiento de garaje tipo box en el nivel -1 de la vivienda, y dice que las opciones de piscina están por consultar.',
  'Pour les maisons mitoyennes, le descriptif indique en standard une piscine privée sur le solarium, un bar sur le solarium, un ascenseur privatif dans chaque logement et une fermeture de garage de type box au niveau -1 du logement, et précise que les options de piscine sont à consulter.',
  'Für die Reihenhäuser nennt die Beschreibung als Standard einen privaten Pool auf dem Solarium, eine Bar auf dem Solarium, einen Privataufzug in jeder Immobilie und eine Garagenabtrennung in Boxform auf Ebene -1 der Immobilie, und sie sagt, dass Pooloptionen noch zu klären sind.',
  'Для таунхаусов в спецификации в стандартную комплектацию входят частный бассейн на солярии, бар на солярии, частный лифт в каждом доме и гаражное ограждение типа «бокс» на уровне -1, а варианты бассейна предлагается уточнять.',
  'بالنسبة إلى المنازل المتلاصقة تورد المواصفات ضمن البنود القياسية مسبحًا خاصًا على السولاريوم وبارًا على السولاريوم ومصعدًا خاصًا في كل مسكن وحاجزًا للمرآب من نوع «بوكس» في المستوى -1 من المسكن، وتذكر أن خيارات المسبح يُرجع إليها للاستفسار.',
  'Voor de herenhuizen noemt de omschrijving als standaard een privézwembad op het solarium, een bar op het solarium, een privélift in elke woning en een garageafscheiding van het boxtype op niveau -1 van de woning, en zegt dat zwembadopties nog moeten worden nagevraagd.',
  'Dla domów szeregowych standard obejmuje według opisu prywatny basen na solarium, bar na solarium, prywatną windę w każdym domu i zabudowę garażu typu box na poziomie -1 domu, a w sprawie opcji basenu odsyła do konsultacji.',
  'For rekkehusene oppgir beskrivelsen som standard et eget basseng på solariet, en bar på solariet, en egen heis i hver bolig og en garasjeinnkapsling av boksmodell på plan -1 i boligen, og sier at bassengalternativer må forhøres om.',
  'För radhusen anger beskrivningen som standard en egen pool på solterrassen, en bar på solterrassen, en egen hiss i varje bostad och en garageinklädnad av boxtyp på plan -1 i bostaden, och säger att poolalternativ ska efterfrågas.')
a('.qualitySpecs.groups[6].items[1]',
  'Opciones en ambos tipos: jacuzzis en terrazas o solárium, una barra que se convierte en cocina con barbacoa, un cargador para vehículos eléctricos en los garajes interiores y persianas motorizadas en los dormitorios. En los apartamentos, las piscinas privadas y una barra en el solárium también son opciones, sujetas a la viabilidad de cada vivienda.',
  'Options dans les deux types : jacuzzis sur les terrasses ou les solariums, un bar transformé en cuisine avec barbecue, une borne de recharge pour véhicules électriques dans les garages intérieurs et des stores motorisés dans les chambres. Pour les appartements, les piscines privées et un bar sur le solarium sont aussi des options, sous réserve de faisabilité pour chaque logement.',
  'Optionen in beiden Typen: Whirlpools auf Terrassen oder Solarien, eine zur Küche mit Grill ausgebaute Bar, eine Ladestation für Elektrofahrzeuge in den Innengaragen und motorisierte Jalousien in den Schlafzimmern. Bei den Wohnungen sind auch private Pools und eine Bar auf dem Solarium Optionen, abhängig von der Machbarkeit für die jeweilige Immobilie.',
  'Опции в обоих типах: джакузи на террасах или солярии, бар, преобразованный в кухню с барбекю, зарядное устройство для электромобилей в закрытых гаражах и моторизованные жалюзи в спальнях. Для квартир частные бассейны и бар на солярии также являются опциями при условии технической возможности для каждого объекта.',
  'الخيارات في النوعين: جاكوزي على التراسات أو السولاريوم، وبار تتم ترقيته إلى مطبخ مع شواية، وشاحن للمركبات الكهربائية في المرائب الداخلية، وستائر آلية في غرف النوم. وفي الشقق تُعدّ المسابح الخاصة والبار على السولاريوم خيارات أيضًا، رهنًا بإمكانية التنفيذ في كل مسكن.',
  'Opties bij beide typen: jacuzzi’s op terrassen of solariums, een bar die wordt uitgebreid tot keuken met barbecue, een oplader voor elektrische voertuigen in de binnengarages en gemotoriseerde zonwering in de slaapkamers. Bij de appartementen zijn privézwembaden en een bar op het solarium eveneens opties, afhankelijk van de haalbaarheid per woning.',
  'Opcje w obu typach: jacuzzi na tarasach lub solariach, bar rozbudowany do kuchni z grillem, ładowarka do pojazdów elektrycznych w garażach wewnętrznych oraz rolety z napędem w sypialniach. W mieszkaniach opcjami są także prywatne baseny i bar na solarium, w zależności od możliwości technicznych w danym lokalu.',
  'Tilvalg i begge typer: boblebad på terrasser eller solarier, en bar utvidet til kjøkken med grill, en lader for elbiler i innvendige garasjer og motoriserte persienner på soverommene. For leilighetene er egne basseng og en bar på solariet også tilvalg, avhengig av hva som er gjennomførbart for hver bolig.',
  'Tillval i båda typerna: jacuzzi på terrasser eller solterrasser, en bar utbyggd till kök med grill, en laddare för elbilar i de inre garagen och motoriserade persienner i sovrummen. För lägenheterna är egna pooler och en bar på solterrassen också tillval, beroende på vad som är genomförbart för varje bostad.')

# ---- residences, lifestyle, location ---------------------------------------------------------------

a('.residences.headlineHtml',
  'Dos tipos, <em>apartamentos y adosados</em>',
  'Deux types, <em>appartements et maisons mitoyennes</em>',
  'Zwei Typen, <em>Wohnungen und Reihenhäuser</em>',
  'Два типа: <em>квартиры и таунхаусы</em>',
  'نوعان: <em>شقق ومنازل متلاصقة</em>',
  'Twee typen, <em>appartementen en herenhuizen</em>',
  'Dwa typy: <em>mieszkania i domy szeregowe</em>',
  'To typer, <em>leiligheter og rekkehus</em>',
  'Två typer, <em>lägenheter och radhus</em>')
a('.residences.copy',
  'Las 23 viviendas con precio son de dos tipos, y la tabla de abajo recoge cada una con su precio. Las superficies son las construidas de la lista, con las terrazas y, cuando la hay, el jardín.',
  'Les 23 logements avec prix sont de deux types, et le tableau ci-dessous présente chacun avec son prix. Les surfaces sont les surfaces construites de la liste, avec les terrasses et, le cas échéant, le jardin.',
  'Die 23 Immobilien mit Preis gehören zwei Typen an; die Tabelle unten führt jede mit ihrem Preis auf. Die Flächen sind die bebauten Flächen der Liste, mit den Terrassen und, falls vorhanden, dem Garten.',
  'Объекты, у которых указана цена (23), относятся к двум типам, а в таблице ниже каждый из них указан со своей ценой. Площади — это площади застройки из списка, с террасами и, если есть, садом.',
  'المساكن الـ 23 المسعّرة من نوعين، ويورد الجدول أدناه كل واحد منها بسعره. والمساحات هي المساحات المبنية الواردة في القائمة، مع التراسات والحديقة إن وُجدت.',
  'De 23 woningen met een prijs zijn van twee typen, en de tabel hieronder vermeldt elke woning met haar prijs. De oppervlakten zijn de bebouwde oppervlakten van de lijst, met de terrassen en, indien aanwezig, de tuin.',
  'Dwadzieścia trzy lokale z ceną są dwóch typów, a tabela poniżej podaje każdy z nich wraz z ceną. Powierzchnie to powierzchnie zabudowy z cennika, wraz z tarasami i, jeśli jest, ogrodem.',
  'De 23 boligene med pris er av to typer, og tabellen nedenfor viser hver av dem med pris. Arealene er de bebygde arealene fra listen, med terrassene og, der det finnes, hagen.',
  'De 23 bostäderna med pris är av två typer, och tabellen nedan visar var och en med sitt pris. Ytorna är byggytorna i listan, med terrasserna och, där det finns en, trädgården.')
a('.residences.items[0].name',
  'Haiku Suites: apartamentos de dos dormitorios',
  'Haiku Suites : appartements de deux chambres',
  'Haiku Suites: Wohnungen mit zwei Schlafzimmern',
  'Haiku Suites: квартиры с двумя спальнями',
  'Haiku Suites: شقق بغرفتي نوم',
  'Haiku Suites: appartementen met twee slaapkamers',
  'Haiku Suites: mieszkania z dwiema sypialniami',
  'Haiku Suites: leiligheter med to soverom',
  'Haiku Suites: lägenheter med två sovrum')
a('.residences.items[0].points[0]',
  '13 de los 36 apartamentos tienen precio, todos con dos dormitorios y dos baños. Están en dos edificios de dos escaleras cada uno, en las plantas baja, primera y segunda. La superficie construida es de 94,15 a 102,08 m² y las terrazas, de 27,58 a 94,71 m².',
  '13 des 36 appartements ont un prix, tous avec deux chambres et deux salles de bains. Ils se trouvent dans deux bâtiments de deux cages d’escalier chacun, au rez-de-chaussée, au premier et au deuxième étage. La surface construite va de 94,15 à 102,08 m² et les terrasses de 27,58 à 94,71 m².',
  '13 der 36 Wohnungen haben einen Preis, alle mit zwei Schlafzimmern und zwei Bädern. Sie liegen in zwei Gebäuden mit je zwei Treppenhäusern, im Erdgeschoss sowie im ersten und zweiten Obergeschoss. Die bebaute Fläche beträgt 94,15 bis 102,08 m², die Terrassen 27,58 bis 94,71 m².',
  'Цена указана у 13 из 36 квартир, у всех по две спальни и две ванные комнаты. Они находятся в двух корпусах по два подъезда в каждом, на первом, втором и третьем этажах. Площадь застройки — от 94,15 до 102,08 м², террасы — от 27,58 до 94,71 м².',
  'لـ 13 من أصل 36 شقة سعر، ولكلٍّ منها غرفتا نوم وحمامان. وهي في مبنيين، في كل منهما مدخلان للدرج، في الطوابق الأرضي والأول والثاني. المساحة المبنية من 94.15 إلى 102.08 م² والتراسات من 27.58 إلى 94.71 م².',
  '13 van de 36 appartementen hebben een prijs, allemaal met twee slaapkamers en twee badkamers. Ze liggen in twee gebouwen met elk twee trappenhuizen, op de begane grond en de eerste en tweede verdieping. De bebouwde oppervlakte is 94,15 tot 102,08 m² en de terrassen 27,58 tot 94,71 m².',
  '13 z 36 mieszkań ma cenę, wszystkie z dwiema sypialniami i dwiema łazienkami. Znajdują się w dwóch budynkach, każdy z dwiema klatkami schodowymi, na parterze oraz na pierwszym i drugim piętrze. Powierzchnia zabudowy wynosi od 94,15 do 102,08 m², a tarasy od 27,58 do 94,71 m².',
  '13 av de 36 leilighetene har pris, alle med to soverom og to bad. De ligger i to bygninger med to trappeoppganger hver, i første, andre og tredje etasje. Det bebygde arealet er 94,15 til 102,08 m² og terrassene 27,58 til 94,71 m².',
  '13 av de 36 lägenheterna har pris, alla med två sovrum och två badrum. De ligger i två byggnader med två trapphus vardera, på bottenvåningen samt första och andra våningen. Byggytan är 94,15 till 102,08 m² och terrasserna 27,58 till 94,71 m².')
a('.residences.items[0].points[1]',
  'Los apartamentos 10 y 28, en planta baja, tienen además jardines de 25,13 y 66,27 m². Los precios van desde {E505000} para el apartamento 32 hasta {E675000} para los apartamentos 12 y 28.',
  'Les appartements 10 et 28, au rez-de-chaussée, ont en outre des jardins de 25,13 et 66,27 m². Les prix vont de {E505000} pour l’appartement 32 à {E675000} pour les appartements 12 et 28.',
  'Die Wohnungen 10 und 28 im Erdgeschoss haben zusätzlich Gärten von 25,13 und 66,27 m². Die Preise reichen von {E505000} für Wohnung 32 bis {E675000} für die Wohnungen 12 und 28.',
  'У квартир 10 и 28 на первом этаже есть также сады площадью 25,13 и 66,27 м². Цены — от {E505000} за квартиру 32 до {E675000} за квартиры 12 и 28.',
  'للشقتين 10 و28 في الطابق الأرضي حديقتان أيضًا بمساحة 25.13 و66.27 م². وتتراوح الأسعار من {E505000} للشقة 32 إلى {E675000} للشقتين 12 و28.',
  'De appartementen 10 en 28, op de begane grond, hebben ook tuinen van 25,13 en 66,27 m². De prijzen lopen van {E505000} voor appartement 32 tot {E675000} voor de appartementen 12 en 28.',
  'Mieszkania 10 i 28 na parterze mają dodatkowo ogrody o powierzchni 25,13 i 66,27 m². Ceny wahają się od {E505000} za mieszkanie 32 do {E675000} za mieszkania 12 i 28.',
  'Leilighetene 10 og 28 i første etasje har dessuten hager på 25,13 og 66,27 m². Prisene går fra {E505000} for leilighet 32 til {E675000} for leilighetene 12 og 28.',
  'Lägenheterna 10 och 28 på bottenvåningen har dessutom trädgårdar på 25,13 och 66,27 m². Priserna går från {E505000} för lägenhet 32 till {E675000} för lägenheterna 12 och 28.')
a('.residences.items[0].points[2]',
  'El apartamento 35, en la segunda planta, tiene un segundo plano con una terraza en la cubierta de 45,53 m² con jacuzzi, a la que se sube por una escalera de caracol. En la lista, cada apartamento tiene dos plazas de aparcamiento numeradas y un trastero numerado.',
  'L’appartement 35, au deuxième étage, dispose d’un second plan pour un toit-terrasse de 45,53 m² avec jacuzzi, accessible par un escalier en colimaçon. Dans la liste, chaque appartement a deux places de stationnement numérotées et une cave numérotée.',
  'Die Wohnung 35 im zweiten Obergeschoss hat einen zweiten Plan für eine Dachterrasse von 45,53 m² mit Whirlpool, die über eine Wendeltreppe erreicht wird. In der Liste hat jede Wohnung zwei nummerierte Stellplätze und einen nummerierten Abstellraum.',
  'У квартиры 35 на третьем этаже есть второй план — для террасы на крыше площадью 45,53 м² с джакузи, на которую ведёт винтовая лестница. В списке у каждой квартиры по два пронумерованных парковочных места и пронумерованная кладовая.',
  'للشقة 35 في الطابق الثاني مخطط ثانٍ لتراس على السطح مساحته 45.53 م² مع جاكوزي، يُصعد إليه بدرج حلزوني. وفي القائمة لكل شقة موقفان مرقّمان لوقوف السيارات وغرفة تخزين مرقّمة.',
  'Appartement 35, op de tweede verdieping, heeft een tweede plattegrond voor een dakterras van 45,53 m² met een jacuzzi, bereikbaar via een wenteltrap. In de lijst heeft elk appartement twee genummerde parkeerplaatsen en een genummerde berging.',
  'Mieszkanie 35, na drugim piętrze, ma drugi rzut tarasu na dachu o powierzchni 45,53 m² z jacuzzi, na który prowadzą kręcone schody. W cenniku każde mieszkanie ma dwa numerowane miejsca postojowe i numerowaną komórkę lokatorską.',
  'Leilighet 35, i tredje etasje, har en ekstra plan for en takterrasse på 45,53 m² med boblebad, som nås via en spiraltrapp. På listen har hver leilighet to nummererte parkeringsplasser og en nummerert bod.',
  'Lägenhet 35, på andra våningen, har en andra ritning för en takterrass på 45,53 m² med jacuzzi, som nås via en spiraltrappa. I listan har varje lägenhet två numrerade parkeringsplatser och ett numrerat förråd.')
a('.residences.items[1].name',
  'Haiku Residences: adosados de tres dormitorios',
  'Haiku Residences : maisons mitoyennes de trois chambres',
  'Haiku Residences: Reihenhäuser mit drei Schlafzimmern',
  'Haiku Residences: таунхаусы с тремя спальнями',
  'Haiku Residences: منازل متلاصقة بثلاث غرف نوم',
  'Haiku Residences: herenhuizen met drie slaapkamers',
  'Haiku Residences: domy szeregowe z trzema sypialniami',
  'Haiku Residences: rekkehus med tre soverom',
  'Haiku Residences: radhus med tre sovrum')
a('.residences.items[1].points[0]',
  '10 de los 15 adosados tienen precio, todos con tres dormitorios. En los planos, cada uno tiene cuatro niveles: un sótano con garaje y trastero, un nivel de dormitorios con jardín, un nivel de estar con la cocina y las terrazas, y un solárium con una terraza.',
  '10 des 15 maisons mitoyennes ont un prix, toutes avec trois chambres. Sur les plans, chacune compte quatre niveaux : un sous-sol avec garage et cave, un niveau des chambres avec jardin, un niveau de séjour avec la cuisine et les terrasses, et un solarium avec une terrasse.',
  '10 der 15 Reihenhäuser haben einen Preis, alle mit drei Schlafzimmern. Auf den Plänen hat jedes vier Ebenen: ein Untergeschoss mit Garage und Abstellraum, eine Schlafebene mit Garten, eine Wohnebene mit Küche und Terrassen sowie ein Solarium mit Terrasse.',
  'Цена указана у 10 из 15 таунхаусов, у всех по три спальни. По планам, в каждом четыре уровня: цокольный этаж с гаражом и кладовой, спальный уровень с садом, жилой уровень с кухней и террасами и солярий с террасой.',
  'لـ 10 من أصل 15 منزلًا متلاصقًا سعر، ولكلٍّ منها ثلاث غرف نوم. وبحسب المخططات، لكل منزل أربعة مستويات: قبو فيه مرآب وغرفة تخزين، ومستوى غرف النوم مع حديقة، ومستوى المعيشة مع المطبخ والتراسات، وسولاريوم مع تراس.',
  '10 van de 15 herenhuizen hebben een prijs, allemaal met drie slaapkamers. Op de plattegronden heeft elk vier niveaus: een kelder met garage en berging, een slaapkamerniveau met tuin, een leefniveau met de keuken en de terrassen, en een solarium met een terras.',
  '10 z 15 domów szeregowych ma cenę, wszystkie z trzema sypialniami. Na rzutach każdy ma cztery poziomy: suterenę z garażem i komórką lokatorską, poziom sypialni z ogrodem, poziom dzienny z kuchnią i tarasami oraz solarium z tarasem.',
  '10 av de 15 rekkehusene har pris, alle med tre soverom. På planene har hvert fire plan: en kjeller med garasje og bod, et soveromsplan med hage, et stueplan med kjøkken og terrasser, og et solarium med terrasse.',
  '10 av de 15 radhusen har pris, alla med tre sovrum. På ritningarna har varje radhus fyra plan: en källare med garage och förråd, ett sovrumsplan med trädgård, ett vardagsplan med köket och terrasserna, och en solterrass med terrass.')
a('.residences.items[1].points[1]',
  'La superficie construida es de 200,56 a 208,92 m², las terrazas de 116,59 a 171,84 m² y los jardines de 10,80 a 42,88 m². Los precios van desde {E962000} para R2 hasta {E1165000} para R1, que tiene el jardín más grande.',
  'La surface construite va de 200,56 à 208,92 m², les terrasses de 116,59 à 171,84 m² et les jardins de 10,80 à 42,88 m². Les prix vont de {E962000} pour R2 à {E1165000} pour R1, qui a le plus grand jardin.',
  'Die bebaute Fläche beträgt 200,56 bis 208,92 m², die Terrassen 116,59 bis 171,84 m² und die Gärten 10,80 bis 42,88 m². Die Preise reichen von {E962000} für R2 bis {E1165000} für R1, das den größten Garten hat.',
  'Площадь застройки — от 200,56 до 208,92 м², террасы — от 116,59 до 171,84 м², сады — от 10,80 до 42,88 м². Цены — от {E962000} за R2 до {E1165000} за R1, у которого самый большой сад.',
  'المساحة المبنية من 200.56 إلى 208.92 م²، والتراسات من 116.59 إلى 171.84 م²، والحدائق من 10.80 إلى 42.88 م². وتتراوح الأسعار من {E962000} للمنزل R2 إلى {E1165000} للمنزل R1، صاحب أكبر حديقة.',
  'De bebouwde oppervlakte is 200,56 tot 208,92 m², de terrassen 116,59 tot 171,84 m² en de tuinen 10,80 tot 42,88 m². De prijzen lopen van {E962000} voor R2 tot {E1165000} voor R1, dat de grootste tuin heeft.',
  'Powierzchnia zabudowy wynosi od 200,56 do 208,92 m², tarasy od 116,59 do 171,84 m², a ogrody od 10,80 do 42,88 m². Ceny wahają się od {E962000} za R2 do {E1165000} za R1, który ma największy ogród.',
  'Det bebygde arealet er 200,56 til 208,92 m², terrassene 116,59 til 171,84 m² og hagene 10,80 til 42,88 m². Prisene går fra {E962000} for R2 til {E1165000} for R1, som har den største hagen.',
  'Byggytan är 200,56 till 208,92 m², terrasserna 116,59 till 171,84 m² och trädgårdarna 10,80 till 42,88 m². Priserna går från {E962000} för R2 till {E1165000} för R1, som har den största trädgården.')
a('.residences.items[1].points[2]',
  'La lista asigna a cada adosado un garaje numerado de GR1 a GR15 y marcado «(ext)», y cada plano muestra una plaza de aparcamiento con el mismo número en el sótano.',
  'La liste attribue à chaque maison mitoyenne un garage numéroté de GR1 à GR15 et marqué « (ext) », et chaque plan montre au sous-sol une place de stationnement portant le même numéro.',
  'Die Liste ordnet jedem Reihenhaus eine Garage mit den Nummern GR1 bis GR15 zu, gekennzeichnet mit „(ext)“, und jeder Plan zeigt im Untergeschoss einen Stellplatz mit derselben Nummer.',
  'В списке каждому таунхаусу отведён гараж с номером от GR1 до GR15 и пометкой «(ext)», а на каждом плане в цокольном этаже показано парковочное место с тем же номером.',
  'تخصّص القائمة لكل منزل متلاصق مرآبًا مرقّمًا من GR1 إلى GR15 ومعلَّمًا بعبارة «(ext)»، ويُظهر كل مخطط موقف سيارة بالرقم نفسه في القبو.',
  'De lijst geeft elk herenhuis een garage met een nummer van GR1 tot GR15, gemarkeerd met “(ext)”, en elke plattegrond toont in de kelder een parkeerplaats met hetzelfde nummer.',
  'Cennik przypisuje każdemu domowi szeregowemu garaż o numerze od GR1 do GR15, oznaczony „(ext)”, a na każdym rzucie w suterenie widnieje miejsce postojowe z tym samym numerem.',
  'Listen gir hvert rekkehus en garasje nummerert fra GR1 til GR15 og merket «(ext)», og hver plan viser en parkeringsplass med samme nummer i kjelleren.',
  'Listan ger varje radhus ett garage numrerat från GR1 till GR15 och markerat ”(ext)”, och varje ritning visar en parkeringsplats med samma nummer i källaren.')

a('.lifestyle.headlineHtml',
  'Jardines, <em>una piscina</em> y golf',
  'Jardins, <em>une piscine</em> et golf',
  'Gärten, <em>ein Pool</em> und Golf',
  'Сады, <em>бассейн</em> и гольф',
  'حدائق و<em>مسبح</em> وغولف',
  'Tuinen, <em>een zwembad</em> en golf',
  'Ogrody, <em>basen</em> i golf',
  'Hager, <em>et basseng</em> og golf',
  'Trädgårdar, <em>en pool</em> och golf')
a('.lifestyle.copy',
  'El dosier y la memoria de calidades describen las zonas comunes y el entorno sin dar medidas, de modo que confirmamos lo que está construido y abierto antes de cualquier reserva.',
  'Le dossier et le descriptif des prestations décrivent les parties communes et l’environnement sans donner de dimensions ; nous confirmons donc ce qui est construit et ouvert avant toute réservation.',
  'Das Dossier und die Ausstattungsbeschreibung beschreiben die Gemeinschaftsflächen und die Umgebung ohne Maßangaben; wir bestätigen daher vor jeder Reservierung, was gebaut und geöffnet ist.',
  'В досье и спецификации отделки общие зоны и окружение описаны без указания размеров, поэтому до любого бронирования мы подтверждаем, что построено и открыто.',
  'يصف الملف ومواصفات الجودة المناطق المشتركة والمحيط دون ذكر المقاسات، ولذلك نؤكد ما تم بناؤه وما فُتح قبل أي حجز.',
  'Het dossier en de technische omschrijving beschrijven de gemeenschappelijke ruimtes en de omgeving zonder afmetingen; wij bevestigen daarom vóór elke reservering wat is gebouwd en geopend.',
  'Dossier i standard wykończenia opisują części wspólne i otoczenie bez podawania wymiarów, dlatego przed jakąkolwiek rezerwacją potwierdzamy, co jest wybudowane i otwarte.',
  'Dossieret og byggebeskrivelsen beskriver fellesområdene og omgivelsene uten mål, så vi bekrefter hva som er bygget og åpnet før enhver reservasjon.',
  'Dossiern och byggnadsbeskrivningen beskriver de gemensamma ytorna och omgivningen utan mått, så vi bekräftar vad som är byggt och öppnat före varje reservation.')
a('.lifestyle.panels[0][1]',
  'El dosier incluye una piscina entre las zonas comunes. En las imágenes generadas por ordenador del promotor tiene un borde curvo, una tarima de madera y tumbonas, con los bloques escalonados detrás.',
  'Le dossier mentionne une piscine parmi les parties communes. Dans les images générées par ordinateur du promoteur, elle a un bord incurvé, un deck en bois et des bains de soleil, avec les immeubles en gradins derrière.',
  'Das Dossier nennt einen Swimmingpool unter den Gemeinschaftsflächen. In den computergenerierten Bildern des Bauträgers hat er einen geschwungenen Rand, ein Holzdeck und Sonnenliegen, mit den gestaffelten Blöcken dahinter.',
  'В досье среди общих зон назван бассейн. На компьютерных изображениях застройщика у него изогнутый край, деревянный настил и шезлонги, а позади видны ступенчатые корпуса.',
  'يدرج الملف مسبحًا ضمن المناطق المشتركة. وفي الصور المولّدة بالحاسوب لدى المطوّر له حافة منحنية وأرضية خشبية ومقاعد تشمّس، وخلفه المباني المتدرجة.',
  'Het dossier noemt een zwembad onder de gemeenschappelijke ruimtes. In de computergegenereerde beelden van de ontwikkelaar heeft het een gebogen rand, een houten dek en ligbedden, met de gestaffelde blokken erachter.',
  'Dossier wymienia basen wśród części wspólnych. Na wygenerowanych komputerowo obrazach dewelopera ma on zakrzywiony brzeg, drewniany pokład i leżaki, a w tle widać budynki ustawione schodkowo.',
  'Dossieret nevner et svømmebasseng blant fellesområdene. På utbyggers datagenererte bilder har det en buet kant, et dekk i tre og solsenger, med de trinnvise byggene bak.',
  'Dossiern nämner en pool bland de gemensamma ytorna. På exploatörens datorgenererade bilder har den en böjd kant, ett trädäck och solstolar, med de förskjutna husen bakom.')
a('.lifestyle.panels[1][1]',
  'Una franja central de jardines paisajísticos separa los apartamentos de los adosados, con grandes palmeras, láminas de agua y una cascada entre los edificios, vegetación mediterránea y senderos para pasear.',
  'Une bande centrale de jardins paysagers sépare les appartements des maisons mitoyennes, avec de grands palmiers, des plans d’eau et une cascade entre les bâtiments, une végétation méditerranéenne et des sentiers de promenade.',
  'Ein zentraler Streifen gestalteter Gärten trennt die Wohnungen von den Reihenhäusern, mit großen Palmen, Wasserspielen und einem Wasserfall zwischen den Gebäuden, mediterraner Bepflanzung und Spazierwegen.',
  'Центральная полоса ландшафтных садов отделяет квартиры от таунхаусов: высокие пальмы, водные элементы и водопад между зданиями, средиземноморская растительность и прогулочные дорожки.',
  'يفصل شريط مركزي من الحدائق المنسّقة الشقق عن المنازل المتلاصقة، مع نخيل كبير وعناصر مائية وشلال بين المباني ونباتات متوسطية وممرات للمشي.',
  'Een centrale strook aangelegde tuinen scheidt de appartementen van de herenhuizen, met grote palmen, waterpartijen en een waterval tussen de gebouwen, mediterrane beplanting en wandelpaden.',
  'Centralny pas zagospodarowanych ogrodów oddziela mieszkania od domów szeregowych, z dużymi palmami, elementami wodnymi i wodospadem między budynkami, śródziemnomorską roślinnością i ścieżkami spacerowymi.',
  'En sentral stripe med opparbeidede hager skiller leilighetene fra rekkehusene, med store palmer, vannspeil og en foss mellom byggene, middelhavsbeplantning og turstier.',
  'En central remsa med planterade trädgårdar skiljer lägenheterna från radhusen, med stora palmer, vattenspeglar och ett vattenfall mellan byggnaderna, medelhavsväxter och promenadstigar.')
a('.lifestyle.panels[2][0]',
  'Chill-out y yoga', 'Détente et yoga', 'Chill-out und Yoga', 'Зона отдыха и йоги', 'الاسترخاء واليوغا', 'Chill-out en yoga', 'Strefa relaksu i jogi', 'Chill-out og yoga', 'Chill-out och yoga')
a('.lifestyle.panels[2][1]',
  'La memoria de calidades incluye una zona para la piscina, el chill-out y el yoga, con vestuarios, acabada en mosaico para piscinas y piedra de Bali con tarima técnica.',
  'Le descriptif des prestations mentionne un espace pour la piscine, la détente et le yoga, avec vestiaires, en mosaïque de piscine et pierre de Bali avec deck technique.',
  'Die Ausstattungsbeschreibung nennt einen Bereich für Pool, Chill-out und Yoga mit Umkleiden, ausgeführt in Poolmosaik und Bali-Stein mit technischem Decking.',
  'В спецификации отделки названа зона для бассейна, отдыха и йоги с раздевалками, отделанная бассейной мозаикой и камнем из Бали с техническим настилом.',
  'تورد مواصفات الجودة منطقة للمسبح والاسترخاء واليوغا مع غرف تبديل ملابس، مكسوّة بفسيفساء المسابح وحجر بالي مع أرضية خشبية تقنية.',
  'De technische omschrijving noemt een zone voor het zwembad, chill-out en yoga, met kleedkamers, afgewerkt met zwembadmozaïek en Balinese steen met technisch decking.',
  'Standard wykończenia wymienia strefę basenu, relaksu i jogi z szatniami, wykończoną mozaiką basenową i kamieniem balijskim z pokładem technicznym.',
  'Byggebeskrivelsen nevner en sone for bassenget, chill-out og yoga, med garderober, utført i bassengmosaikk og Bali-stein med teknisk dekk.',
  'Byggnadsbeskrivningen nämner en zon för poolen, chill-out och yoga, med omklädningsrum, utförd i poolmosaik och balistens med tekniskt trädäck.')
a('.lifestyle.panels[3][1]',
  'El dosier incluye un salón comunitario y un club social entre las zonas comunes. No da descripción ni medidas.',
  'Le dossier mentionne un salon commun et un club social parmi les parties communes. Il n’en donne ni description ni dimensions.',
  'Das Dossier nennt einen Gemeinschaftsraum und einen Social Club unter den Gemeinschaftsflächen. Eine Beschreibung oder Maße gibt es nicht.',
  'В досье среди общих зон названы общая гостиная и социальный клуб. Ни описания, ни размеров в нём нет.',
  'يدرج الملف صالة مشتركة ونادٍ اجتماعيًا ضمن المناطق المشتركة. ولا يقدّم وصفًا ولا مقاسات.',
  'Het dossier noemt een gemeenschappelijke lounge en een sociale club onder de gemeenschappelijke ruimtes. Het geeft geen beschrijving en geen afmetingen.',
  'Dossier wymienia wspólny salon i klub towarzyski wśród części wspólnych. Nie podaje ani opisu, ani wymiarów.',
  'Dossieret nevner en felles lounge og en sosial klubb blant fellesområdene. Det gir verken beskrivelse eller mål.',
  'Dossiern nämner en gemensam lounge och en social klubb bland de gemensamma ytorna. Den ger varken beskrivning eller mått.')
a('.lifestyle.panels[4][0]',
  'Golf y mar', 'Golf et mer', 'Golf und Meer', 'Гольф и море', 'الغولف والبحر', 'Golf en zee', 'Golf i morze', 'Golf og havet', 'Golf och havet')
a('.lifestyle.panels[4][1]',
  'El dosier presenta Cancelada como un paraíso para el golf, nombra cuatro campos cercanos y sitúa el Real Club Valderrama, en Sotogrande, a 20 minutos. También menciona una escuela ecuestre acreditada por la British Horse Society y 11 puertos deportivos en la costa, entre ellos Puerto Banús.',
  'Le dossier présente Cancelada comme un paradis du golf, cite quatre parcours à proximité et situe le Real Club Valderrama, à Sotogrande, à 20 minutes. Il mentionne aussi une école d’équitation agréée par la British Horse Society et 11 ports de plaisance sur la côte, dont Puerto Banús.',
  'Das Dossier bezeichnet Cancelada als Paradies für Golfer, nennt vier Plätze in der Nähe und verortet den Real Club Valderrama in Sotogrande 20 Minuten entfernt. Es erwähnt außerdem eine von der British Horse Society anerkannte Reitschule und 11 Yachthäfen an der Küste, darunter Puerto Banús.',
  'В досье Канселада названа раем для гольфа, перечислены четыре поля поблизости, а Real Club Valderrama в Сотогранде находится в 20 минутах. Также упомянуты конная школа, аккредитованная British Horse Society, и 11 яхтенных портов на побережье, среди них Пуэрто-Банус.',
  'يقدّم الملف كانسيلادا بوصفها جنةً لعشاق الغولف، ويسمّي أربعة ملاعب قريبة، ويضع Real Club Valderrama في سوتوغراندي على بعد 20 دقيقة. ويذكر أيضًا مدرسة للفروسية معتمدة من British Horse Society و11 مرفأً لليخوت على الساحل، منها بويرتو بانوس.',
  'Het dossier presenteert Cancelada als een paradijs voor golf, noemt vier banen in de buurt en plaatst de Real Club Valderrama in Sotogrande op 20 minuten. Het vermeldt ook een ruitersportschool die is erkend door de British Horse Society en 11 jachthavens aan de kust, waaronder Puerto Banús.',
  'Dossier przedstawia Cancelada jako raj dla golfa, wymienia cztery pobliskie pola i umieszcza Real Club Valderrama w Sotogrande 20 minut stąd. Wspomina też szkołę jeździecką akredytowaną przez British Horse Society oraz 11 przystani jachtowych na wybrzeżu, w tym Puerto Banús.',
  'Dossieret presenterer Cancelada som et paradis for golf, nevner fire baner i nærheten og plasserer Real Club Valderrama i Sotogrande 20 minutter unna. Det nevner også en ridesko akkreditert av British Horse Society og 11 småbåthavner langs kysten, blant dem Puerto Banús.',
  'Dossiern beskriver Cancelada som ett paradis för golf, nämner fyra banor i närheten och placerar Real Club Valderrama i Sotogrande 20 minuter bort. Den nämner också en ridskola ackrediterad av British Horse Society och 11 småbåtshamnar längs kusten, bland dem Puerto Banús.')

a('.location.copy',
  'El dosier sitúa el complejo en Cancelada, en la Nueva Milla de Oro de Estepona, que describe como una zona tranquila con acceso a los servicios de la Costa del Sol. Nombra los campos de golf Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House y Atalaya Golf & Country Club, y sitúa el Real Club Valderrama, en Sotogrande, a 20 minutos del complejo. Su mapa de ubicación muestra un aeropuerto, una estación de tren, centros médicos, campos de golf, centros comerciales, colegios y puertos deportivos, sin distancias. Los documentos no dan dirección ni coordenadas de la parcela, de modo que el mapa muestra la zona de Cancelada.',
  'Le dossier situe l’ensemble à Cancelada, sur la New Golden Mile d’Estepona, qu’il décrit comme un secteur tranquille avec accès aux services de la Costa del Sol. Il cite les golfs Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House et Atalaya Golf & Country Club, et situe le Real Club Valderrama, à Sotogrande, à 20 minutes de l’ensemble. Sa carte de localisation montre un aéroport, une gare, des centres médicaux, des golfs, des centres commerciaux, des écoles et des ports de plaisance, sans distances. Les documents ne donnent ni adresse ni coordonnées de la parcelle ; la carte montre donc le secteur de Cancelada.',
  'Das Dossier verortet die Anlage in Cancelada, an der New Golden Mile von Estepona, die es als ruhige Gegend mit Zugang zu den Annehmlichkeiten der Costa del Sol beschreibt. Es nennt die Golfplätze Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House und Atalaya Golf & Country Club und verortet den Real Club Valderrama in Sotogrande 20 Minuten von der Anlage entfernt. Seine Lagekarte zeigt einen Flughafen, einen Bahnhof, medizinische Zentren, Golfplätze, Einkaufszentren, Schulen und Yachthäfen, ohne Entfernungen. Die Dokumente nennen weder Adresse noch Koordinaten des Grundstücks, daher zeigt die Karte das Gebiet Cancelada.',
  'В досье комплекс расположен в Канселаде, на Новой Золотой миле Эстепоны, которая описана как тихий район с доступом к инфраструктуре Коста-дель-Соль. Названы гольф-клубы Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House и Atalaya Golf & Country Club, а Real Club Valderrama в Сотогранде находится в 20 минутах от комплекса. На карте расположения в досье отмечены аэропорт, железнодорожная станция, медицинские центры, гольф-поля, торговые центры, школы и яхтенные порты, без расстояний. В документах нет ни адреса, ни координат участка, поэтому на карте показан район Канселады.',
  'يضع الملف المجمّع في كانسيلادا، على الميل الذهبي الجديد في إستيبونا، ويصفها بأنها منطقة هادئة يسهل منها الوصول إلى خدمات كوستا ديل سول. ويسمّي ملاعب الغولف Flamingos Golf وCancelada Club Golf وEl Campanario Golf & Country House وAtalaya Golf & Country Club، ويضع Real Club Valderrama في سوتوغراندي على بعد 20 دقيقة من المجمّع. وتُظهر خريطة الموقع فيه مطارًا ومحطة قطار ومراكز طبية وملاعب غولف ومراكز تسوق ومدارس ومرافئ يخوت، من دون مسافات. ولا تذكر الوثائق عنوانًا ولا إحداثيات للقطعة، ولذلك تعرض الخريطة منطقة كانسيلادا.',
  'Het dossier plaatst het complex in Cancelada, aan de New Golden Mile van Estepona, dat het beschrijft als een rustig gebied met toegang tot de voorzieningen van de Costa del Sol. Het noemt de golfbanen Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House en Atalaya Golf & Country Club, en plaatst de Real Club Valderrama in Sotogrande op 20 minuten van het complex. De locatiekaart toont een luchthaven, een treinstation, medische centra, golfbanen, winkelcentra, scholen en jachthavens, zonder afstanden. De documenten geven geen adres of coördinaten van het perceel, dus de kaart toont het gebied Cancelada.',
  'Dossier umieszcza kompleks w Cancelada, na New Golden Mile w Esteponie, którą opisuje jako spokojną okolicę z dostępem do udogodnień Costa del Sol. Wymienia pola golfowe Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House i Atalaya Golf & Country Club oraz umieszcza Real Club Valderrama w Sotogrande 20 minut od kompleksu. Jego mapa lokalizacji pokazuje lotnisko, stację kolejową, ośrodki medyczne, pola golfowe, centra handlowe, szkoły i przystanie jachtowe, bez odległości. Dokumenty nie podają adresu ani współrzędnych działki, dlatego mapa pokazuje obszar Cancelada.',
  'Dossieret plasserer komplekset i Cancelada, på New Golden Mile i Estepona, som det beskriver som et rolig område med tilgang til Costa del Sols fasiliteter. Det nevner golfbanene Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House og Atalaya Golf & Country Club, og plasserer Real Club Valderrama i Sotogrande 20 minutter fra komplekset. Lokaliseringskartet viser en flyplass, en jernbanestasjon, medisinske sentre, golfbaner, kjøpesentre, skoler og småbåthavner, uten avstander. Dokumentene oppgir verken adresse eller koordinater for tomten, så kartet viser området Cancelada.',
  'Dossiern placerar området i Cancelada, på New Golden Mile i Estepona, som den beskriver som ett lugnt område med tillgång till Costa del Sols bekvämligheter. Den nämner golfbanorna Flamingos Golf, Cancelada Club Golf, El Campanario Golf & Country House och Atalaya Golf & Country Club, och placerar Real Club Valderrama i Sotogrande 20 minuter från området. Dess lägeskarta visar en flygplats, en tågstation, vårdcentraler, golfbanor, köpcentrum, skolor och småbåtshamnar, utan avstånd. Dokumenten anger varken adress eller koordinater för tomten, så kartan visar området Cancelada.')
same('Real Club Valderrama')
a('.location.distances[0][1]',
  '20 minutos, según el promotor', '20 minutes, selon le promoteur', '20 Minuten, laut Bauträger', '20 минут, по данным застройщика',
  '20 دقيقة، بحسب المطوّر', '20 minuten, volgens de ontwikkelaar', '20 minut, według dewelopera', '20 minutter, ifølge utbygger', '20 minuter, enligt exploatören')

# ---- investment, trust ----------------------------------------------------------------------------------

a('.investment.cards[0][1]',
  '28 de las 51 viviendas de la lista figuran como reservadas. 23 tienen precio: 13 apartamentos de {E505000} a {E675000} y 10 adosados de {E962000} a {E1165000}, más IVA.',
  '28 des 51 logements de la liste sont marqués comme réservés. 23 ont un prix : 13 appartements de {E505000} à {E675000} et 10 maisons mitoyennes de {E962000} à {E1165000}, hors TVA.',
  '28 der 51 Immobilien der Liste sind als reserviert gekennzeichnet. 23 haben einen Preis: 13 Wohnungen von {E505000} bis {E675000} und 10 Reihenhäuser von {E962000} bis {E1165000}, zuzüglich MwSt.',
  '28 из 51 объекта в списке отмечены как забронированные. У 23 указана цена: 13 квартир от {E505000} до {E675000} и 10 таунхаусов от {E962000} до {E1165000} без НДС.',
  '28 من أصل 51 مسكنًا في القائمة معلَّمة كمحجوزة. ولـ 23 منها سعر: 13 شقة من {E505000} إلى {E675000} و10 منازل متلاصقة من {E962000} إلى {E1165000}، دون ضريبة القيمة المضافة.',
  '28 van de 51 woningen op de lijst zijn als gereserveerd gemarkeerd. 23 hebben een prijs: 13 appartementen van {E505000} tot {E675000} en 10 herenhuizen van {E962000} tot {E1165000}, excl. btw.',
  '28 z 51 lokali na liście oznaczono jako zarezerwowane. 23 mają cenę: 13 mieszkań od {E505000} do {E675000} i 10 domów szeregowych od {E962000} do {E1165000}, plus VAT.',
  '28 av de 51 boligene på listen er merket som reservert. 23 har pris: 13 leiligheter fra {E505000} til {E675000} og 10 rekkehus fra {E962000} til {E1165000}, pluss mva.',
  '28 av de 51 bostäderna i listan är markerade som reserverade. 23 har ett pris: 13 lägenheter från {E505000} till {E675000} och 10 radhus från {E962000} till {E1165000}, plus IVA (spansk moms).')
a('.investment.cards[2][1]',
  'La lista muestra una reserva de {E9000}, luego un pago a la firma del contrato que lleva el total pagado al 30% del precio de venta con IVA incluido, y el 70% en la escritura. También muestra dos pagos aplazados del 5% cada uno, sin fechas, y no dice si forman parte del 70%, de modo que pedimos el calendario por escrito antes de cualquier reserva.',
  'La liste indique une réservation de {E9000}, puis un paiement à la signature du contrat qui porte le total versé à 30 % du prix de vente TVA comprise, et 70 % à l’acte. Elle indique aussi deux paiements différés de 5 % chacun, sans dates, et ne précise pas s’ils font partie des 70 % ; nous demandons donc l’échéancier par écrit avant toute réservation.',
  'Die Liste zeigt eine Reservierung von {E9000}, dann eine Zahlung bei Vertragsabschluss, mit der die Gesamtzahlung 30 % des Verkaufspreises einschließlich MwSt. erreicht, und 70 % bei der Beurkundung. Sie zeigt außerdem zwei aufgeschobene Raten von je 5 % ohne Datum und sagt nicht, ob sie Teil der 70 % sind; deshalb fordern wir den Zahlungsplan vor jeder Reservierung schriftlich an.',
  'В списке указано бронирование {E9000}, затем платёж при подписании договора, после которого общая сумма составляет 30 % цены продажи с учётом НДС, и 70 % при подписании нотариального акта. Указаны также два отсроченных платежа по 5 % без дат; не сказано, входят ли они в эти 70 %, поэтому до любого бронирования мы запрашиваем график в письменном виде.',
  'تُظهر القائمة حجزًا بمبلغ {E9000}، ثم دفعة عند توقيع العقد يبلغ بها مجموع المدفوع 30% من سعر البيع شاملًا ضريبة القيمة المضافة، و70% عند التوقيع على سند الملكية. وتُظهر أيضًا دفعتين مؤجلتين بنسبة 5% لكل منهما دون تواريخ، ولا تبيّن هل هما جزء من الـ 70%، ولذلك نطلب الجدول كتابةً قبل أي حجز.',
  'De lijst toont een reservering van {E9000}, dan een betaling bij het koopcontract waarmee het totaal betaald op 30% van de verkoopprijs inclusief btw komt, en 70% bij de akte. Ze toont ook twee uitgestelde termijnen van elk 5%, zonder data, en zegt niet of ze deel uitmaken van de 70%; daarom vragen wij het schema schriftelijk aan vóór elke reservering.',
  'Cennik wskazuje rezerwację w wysokości {E9000}, następnie płatność przy umowie, po której łączna wpłata wynosi 30% ceny sprzedaży z VAT, oraz 70% przy akcie notarialnym. Wskazuje też dwie płatności odroczone po 5%, bez dat, i nie mówi, czy wchodzą w skład tych 70%, dlatego przed jakąkolwiek rezerwacją prosimy o harmonogram na piśmie.',
  'Listen viser en reservasjon på {E9000}, deretter en betaling ved kontrakten som bringer det samlede innbetalte beløpet opp i 30 % av salgsprisen inkludert mva., og 70 % ved overtakelsen. Den viser også to utsatte delbetalinger på 5 % hver, uten datoer, og sier ikke om de inngår i de 70 %, så vi ber om betalingsplanen skriftlig før enhver reservasjon.',
  'Listan visar en reservation på {E9000}, sedan en betalning vid kontraktet som för den totala betalningen till 30 % av försäljningspriset inklusive IVA, och 70 % vid lagfarten. Den visar också två uppskjutna delbetalningar på 5 % vardera, utan datum, och säger inte om de ingår i de 70 %, så vi ber om betalningsplanen skriftligt före varje reservation.')
a('.investment.cards[3][1]',
  'La lista asigna a cada apartamento dos plazas de aparcamiento numeradas y un trastero numerado, mientras que el dosier dice que cada vivienda tiene una plaza de aparcamiento y un trastero. Cada adosado tiene un garaje numerado de GR1 a GR15, marcado «(ext)», y una plaza de aparcamiento con el mismo número en su plano del sótano. Confirmamos lo que incluye el precio de la vivienda que usted elija.',
  'La liste attribue à chaque appartement deux places de stationnement numérotées et une cave numérotée, alors que le dossier indique que chaque logement a une place de stationnement et une cave. Chaque maison mitoyenne a un garage numéroté de GR1 à GR15, marqué « (ext) », et une place de stationnement portant le même numéro sur son plan du sous-sol. Nous confirmons ce que comprend le prix du logement que vous choisissez.',
  'Die Liste ordnet jeder Wohnung zwei nummerierte Stellplätze und einen nummerierten Abstellraum zu, während das Dossier sagt, dass jede Immobilie einen Stellplatz und einen Abstellraum hat. Jedes Reihenhaus hat eine Garage mit den Nummern GR1 bis GR15, gekennzeichnet mit „(ext)“, und auf seinem Plan des Untergeschosses einen Stellplatz mit derselben Nummer. Wir bestätigen, was der Preis der von Ihnen gewählten Immobilie umfasst.',
  'В списке за каждой квартирой закреплены два пронумерованных парковочных места и пронумерованная кладовая, тогда как в досье сказано, что у каждого объекта есть одно парковочное место и кладовая. У каждого таунхауса есть гараж с номером от GR1 до GR15 с пометкой «(ext)» и парковочное место с тем же номером на плане цокольного этажа. Мы подтверждаем, что входит в цену выбранного вами объекта.',
  'تخصّص القائمة لكل شقة موقفين مرقّمين لوقوف السيارات وغرفة تخزين مرقّمة، فيما يذكر الملف أن لكل مسكن موقفًا واحدًا وغرفة تخزين. ولكل منزل متلاصق مرآب مرقّم من GR1 إلى GR15 ومعلَّم بعبارة «(ext)»، وموقف سيارة بالرقم نفسه في مخطط القبو. ونؤكد ما يشمله سعر المسكن الذي تختارونه.',
  'De lijst geeft elk appartement twee genummerde parkeerplaatsen en een genummerde berging, terwijl het dossier zegt dat elke woning een parkeerplaats en een berging heeft. Elk herenhuis heeft een garage met een nummer van GR1 tot GR15, gemarkeerd met “(ext)”, en op de plattegrond van de kelder een parkeerplaats met hetzelfde nummer. Wij bevestigen wat de prijs van de woning die u kiest omvat.',
  'Cennik przypisuje każdemu mieszkaniu dwa numerowane miejsca postojowe i numerowaną komórkę lokatorską, podczas gdy dossier podaje, że każdy lokal ma jedno miejsce postojowe i komórkę lokatorską. Każdy dom szeregowy ma garaż o numerze od GR1 do GR15, oznaczony „(ext)”, oraz miejsce postojowe z tym samym numerem na rzucie sutereny. Potwierdzamy, co obejmuje cena wybranego przez Pana/Panią lokalu.',
  'Listen gir hver leilighet to nummererte parkeringsplasser og en nummerert bod, mens dossieret sier at hver bolig har én parkeringsplass og en bod. Hvert rekkehus har en garasje nummerert fra GR1 til GR15, merket «(ext)», og en parkeringsplass med samme nummer på kjelleretasjens plan. Vi bekrefter hva prisen for boligen De velger omfatter.',
  'Listan ger varje lägenhet två numrerade parkeringsplatser och ett numrerat förråd, medan dossiern säger att varje bostad har en parkeringsplats och ett förråd. Varje radhus har ett garage numrerat från GR1 till GR15, markerat ”(ext)”, och en parkeringsplats med samma nummer på källarplanets ritning. Vi bekräftar vad priset för den bostad ni väljer omfattar.')

a('.trustDossier.cards[0][1]',
  'Ninguno de los documentos que tenemos da una fecha de entrega ni una fase de las obras, de modo que esta página dice solo que la entrega está por confirmar. Pedimos la fecha contractual, el estado de la licencia y la fase de las obras antes de cualquier reserva.',
  'Aucun des documents en notre possession ne donne de date de livraison ni d’état d’avancement des travaux ; cette page indique donc seulement que la livraison est à confirmer. Nous demandons la date contractuelle, la situation du permis et l’état d’avancement des travaux avant toute réservation.',
  'Keines der uns vorliegenden Dokumente nennt einen Fertigstellungstermin oder einen Baustand; diese Seite sagt daher nur, dass die Fertigstellung noch offen ist. Wir fragen vor jeder Reservierung den vertraglichen Termin, den Stand der Genehmigung und den Baustand ab.',
  'Ни в одном из имеющихся у нас документов нет срока сдачи или стадии строительства, поэтому на этой странице сказано лишь, что срок сдачи уточняется. До любого бронирования мы запрашиваем договорный срок, статус лицензии и стадию строительства.',
  'لا تذكر أي من الوثائق التي بحوزتنا موعدًا للإنجاز ولا مرحلة للأعمال، ولذلك تكتفي هذه الصفحة بالقول إن موعد الإنجاز قيد التأكيد. ونطلب الموعد التعاقدي وحالة الترخيص ومرحلة الأعمال قبل أي حجز.',
  'Geen van de documenten die wij hebben noemt een opleveringsdatum of een bouwfase, dus deze pagina zegt alleen dat de oplevering nog moet worden bevestigd. Wij vragen vóór elke reservering de contractuele datum, de status van de vergunning en de bouwfase op.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu odbioru ani etapu prac, dlatego ta strona mówi jedynie, że termin odbioru jest do potwierdzenia. Przed jakąkolwiek rezerwacją prosimy o termin umowny, status pozwolenia i etap prac.',
  'Ingen av dokumentene vi har oppgir en ferdigstillelsesdato eller et byggetrinn, så denne siden sier bare at ferdigstillelsen ikke er bekreftet. Vi ber om den kontraktsfestede datoen, tillatelsens status og byggetrinnet før enhver reservasjon.',
  'Inget av de dokument vi har anger ett färdigställandedatum eller ett byggstadium, så den här sidan säger bara att färdigställandet inte är bekräftat. Vi frågar efter det avtalade datumet, bygglovets status och byggstadiet före varje reservation.')
a('.trustDossier.cards[1][0]', 'Los documentos', 'Les documents', 'Die Dokumente', 'Документы', 'الوثائق', 'De documenten', 'Dokumenty', 'Dokumentene', 'Dokumenten')
a('.trustDossier.cards[1][1]',
  'Los dosieres llevan en el nombre de archivo las fechas del 23 de julio de 2026 (inglés) y del 9 de junio de 2026 (español), y las memorias de calidades, el 18 de agosto. La lista de precios es del 26 de octubre de 2026. La usamos para los precios y la disponibilidad, y los demás documentos para describir el proyecto.',
  'Les dossiers portent dans leur nom de fichier les dates du 23 juillet 2026 (anglais) et du 9 juin 2026 (espagnol), et les descriptifs des prestations celle du 18 août. La liste de prix est datée du 26 octobre 2026. Nous l’utilisons pour les prix et la disponibilité, et les autres documents pour décrire le projet.',
  'Die Dossiers tragen in ihren Dateinamen die Daten 23. Juli 2026 (Englisch) und 9. Juni 2026 (Spanisch), die Ausstattungsbeschreibungen den 18. August. Die Preisliste ist auf den 26. Oktober 2026 datiert. Wir verwenden sie für Preise und Verfügbarkeit und die übrigen Dokumente zur Beschreibung des Projekts.',
  'В названиях файлов досье указаны даты 23 июля 2026 года (английская версия) и 9 июня 2026 года (испанская), а в названиях спецификаций отделки — 18 августа. Прайс-лист датирован 26 октября 2026 года. Мы используем его для цен и наличия, а остальные документы — для описания проекта.',
  'تحمل أسماء ملفات الملفات التعريفية تاريخَي 23 يوليو 2026 (بالإنجليزية) و9 يونيو 2026 (بالإسبانية)، وتحمل مواصفات الجودة تاريخ 18 أغسطس. وقائمة الأسعار مؤرخة في 26 أكتوبر 2026. ونستخدمها للأسعار والتوفر، ونستخدم الوثائق الأخرى لوصف المشروع.',
  'De dossiers dragen in hun bestandsnaam de data 23 juli 2026 (Engels) en 9 juni 2026 (Spaans), en de technische omschrijvingen 18 augustus. De prijslijst is gedateerd op 26 oktober 2026. Wij gebruiken die voor prijzen en beschikbaarheid, en de overige documenten om het project te beschrijven.',
  'Dossier mają w nazwach plików daty 23 lipca 2026 r. (angielski) i 9 czerwca 2026 r. (hiszpański), a standardy wykończenia 18 sierpnia. Cennik jest datowany na 26 października 2026 r. Korzystamy z niego w odniesieniu do cen i dostępności, a z pozostałych dokumentów do opisu projektu.',
  'Dossierene har datoene 23. juli 2026 (engelsk) og 9. juni 2026 (spansk) i filnavnet, og byggebeskrivelsene 18. august. Prislisten er datert 26. oktober 2026. Vi bruker den til priser og tilgjengelighet, og de andre dokumentene til å beskrive prosjektet.',
  'Dossierna har datumen 23 juli 2026 (engelska) och 9 juni 2026 (spanska) i filnamnet, och byggnadsbeskrivningarna 18 augusti. Prislistan är daterad den 26 oktober 2026. Vi använder den för priser och tillgänglighet, och de övriga dokumenten för att beskriva projektet.')
a('.trustDossier.cards[2][0]',
  'La oferta de viviendas', 'L’offre de logements', 'Das Angebot an Immobilien', 'Состав объектов', 'تشكيلة المساكن', 'Het aanbod aan woningen', 'Oferta lokali', 'Utvalget av boliger', 'Utbudet av bostäder')
a('.trustDossier.cards[2][1]',
  'El dosier menciona apartamentos de tres dormitorios, dúplex y áticos. Los 13 apartamentos con precio tienen todos dos dormitorios y dos baños en sus planos, y los 12 apartamentos de tres dormitorios de la lista figuran como reservados. El apartamento 35 tiene un segundo plano con una terraza en la cubierta con jacuzzi.',
  'Le dossier mentionne des appartements de trois chambres, des duplex et des penthouses. Les 13 appartements avec prix ont tous deux chambres et deux salles de bains sur leurs plans, et les 12 appartements de trois chambres de la liste sont marqués comme réservés. L’appartement 35 dispose d’un second plan pour un toit-terrasse avec jacuzzi.',
  'Das Dossier erwähnt Wohnungen mit drei Schlafzimmern sowie Duplex- und Penthouse-Wohnungen. Die 13 Wohnungen mit Preis haben auf ihren Plänen alle zwei Schlafzimmer und zwei Bäder, und die 12 Wohnungen mit drei Schlafzimmern auf der Liste sind als reserviert gekennzeichnet. Die Wohnung 35 hat einen zweiten Plan für eine Dachterrasse mit Whirlpool.',
  'В досье упомянуты квартиры с тремя спальнями, дуплексы и пентхаусы. У всех 13 квартир с ценой по планам две спальни и две ванные комнаты, а 12 квартир с тремя спальнями из списка отмечены как забронированные. У квартиры 35 есть второй план — для террасы на крыше с джакузи.',
  'يذكر الملف شققًا بثلاث غرف نوم ودوبلكس وبنتهاوس. وجميع الشقق الـ 13 المسعّرة لها في مخططاتها غرفتا نوم وحمامان، والشقق الـ 12 ذات الغرف الثلاث في القائمة معلَّمة كمحجوزة. وللشقة 35 مخطط ثانٍ لتراس على السطح مع جاكوزي.',
  'Het dossier vermeldt appartementen met drie slaapkamers, duplexen en penthouses. De 13 appartementen met een prijs hebben op hun plattegronden allemaal twee slaapkamers en twee badkamers, en de 12 appartementen met drie slaapkamers op de lijst zijn als gereserveerd gemarkeerd. Appartement 35 heeft een tweede plattegrond voor een dakterras met een jacuzzi.',
  'Dossier wymienia mieszkania z trzema sypialniami, dupleksy i penthouse’y. Na rzutach wszystkie 13 mieszkań z ceną ma dwie sypialnie i dwie łazienki, a 12 mieszkań z trzema sypialniami z cennika oznaczono jako zarezerwowane. Mieszkanie 35 ma drugi rzut tarasu na dachu z jacuzzi.',
  'Dossieret nevner leiligheter med tre soverom, dupleksleiligheter og toppleiligheter. De 13 leilighetene med pris har alle to soverom og to bad på planene, og de 12 leilighetene med tre soverom på listen er merket som reservert. Leilighet 35 har en ekstra plan for en takterrasse med boblebad.',
  'Dossiern nämner lägenheter med tre sovrum, duplexlägenheter och takvåningar. De 13 lägenheterna med pris har alla två sovrum och två badrum på ritningarna, och de 12 lägenheterna med tre sovrum i listan är markerade som reserverade. Lägenhet 35 har en andra ritning för en takterrass med jacuzzi.')
a('.trustDossier.cards[3][0]',
  'Los adosados', 'Les maisons mitoyennes', 'Die Reihenhäuser', 'Таунхаусы', 'المنازل المتلاصقة', 'De herenhuizen', 'Domy szeregowe', 'Rekkehusene', 'Radhusen')
a('.trustDossier.cards[3][1]',
  'El dosier llama a las Residences viviendas unifamiliares. La lista y los planos las muestran en hileras adosadas, numeradas de R1 a R15 en tres grupos de cinco, y esta página las llama adosados.',
  'Le dossier qualifie les Residences de maisons individuelles. La liste et les plans les montrent en rangées mitoyennes, numérotées de R1 à R15 en trois groupes de cinq, et cette page les appelle maisons mitoyennes.',
  'Das Dossier nennt die Residences Einfamilienhäuser. Die Liste und die Pläne zeigen sie in Reihen, nummeriert von R1 bis R15 in drei Gruppen zu je fünf, und diese Seite nennt sie Reihenhäuser.',
  'В досье Residences названы односемейными домами. В списке и на планах они показаны рядами, пронумерованными от R1 до R15 тремя группами по пять, и на этой странице они названы таунхаусами.',
  'يسمّي الملف الـ Residences منازل عائلية مستقلة. أما القائمة والمخططات فتُظهرها في صفوف متلاصقة مرقّمة من R1 إلى R15 في ثلاث مجموعات من خمسة، وتسميها هذه الصفحة منازل متلاصقة.',
  'Het dossier noemt de Residences eengezinswoningen. De lijst en de plattegronden tonen ze in aaneengesloten rijen, genummerd van R1 tot R15 in drie groepen van vijf, en deze pagina noemt ze herenhuizen.',
  'Dossier nazywa Residences domami jednorodzinnymi. Cennik i rzuty pokazują je w zabudowie szeregowej, ponumerowane od R1 do R15 w trzech grupach po pięć, a ta strona nazywa je domami szeregowymi.',
  'Dossieret kaller Residences eneboliger. Listen og planene viser dem i rekker, nummerert fra R1 til R15 i tre grupper på fem, og denne siden kaller dem rekkehus.',
  'Dossiern kallar Residences enfamiljshus. Listan och ritningarna visar dem i rader, numrerade från R1 till R15 i tre grupper om fem, och den här sidan kallar dem radhus.')
a('.trustDossier.cards[4][1]',
  'Para cada vivienda, la lista da una superficie útil, una superficie construida y una tercera superficie construida mayor marcada S/BOJA, por ejemplo 81,07, 94,44 y 117,08 m² para el apartamento 2, y las terrazas de la misma manera. Esta página usa la superficie construida, las terrazas construidas y los jardines de la lista, y confirmamos qué cifras usa el contrato.',
  'Pour chaque logement, la liste donne une surface utile, une surface construite et une troisième surface construite, plus grande, marquée S/BOJA, par exemple 81,07, 94,44 et 117,08 m² pour l’appartement 2, et les terrasses de la même manière. Cette page utilise la surface construite, les terrasses construites et les jardins de la liste, et nous confirmons quels chiffres le contrat retient.',
  'Für jede Immobilie nennt die Liste eine Nutzfläche, eine bebaute Fläche und eine dritte, größere bebaute Fläche mit der Kennzeichnung S/BOJA, zum Beispiel 81,07, 94,44 und 117,08 m² für Wohnung 2, und die Terrassen auf dieselbe Weise. Diese Seite verwendet die bebaute Fläche, die bebauten Terrassen und die Gärten der Liste, und wir bestätigen, welche Zahlen der Vertrag zugrunde legt.',
  'Для каждого объекта в списке указаны полезная площадь, площадь застройки и третья, бо́льшая площадь застройки с пометкой S/BOJA — например, 81,07, 94,44 и 117,08 м² для квартиры 2 — и так же для террас. На этой странице используются площадь застройки, площади террас по застройке и сады из списка, а какие цифры берутся в договоре, мы подтверждаем.',
  'تورد القائمة لكل مسكن مساحة صافية ومساحة مبنية ومساحة مبنية ثالثة أكبر معلَّمة بعبارة S/BOJA، مثل 81.07 و94.44 و117.08 م² للشقة 2، والتراسات بالطريقة نفسها. وتعتمد هذه الصفحة المساحة المبنية والتراسات المبنية والحدائق الواردة في القائمة، ونؤكد أي الأرقام يعتمدها العقد.',
  'Voor elke woning geeft de lijst een gebruiksoppervlakte, een bebouwde oppervlakte en een derde, grotere bebouwde oppervlakte met de aanduiding S/BOJA, bijvoorbeeld 81,07, 94,44 en 117,08 m² voor appartement 2, en de terrassen op dezelfde manier. Deze pagina gebruikt de bebouwde oppervlakte, de bebouwde terrassen en de tuinen van de lijst, en wij bevestigen welke cijfers het contract hanteert.',
  'Dla każdego lokalu cennik podaje powierzchnię użytkową, powierzchnię zabudowy oraz trzecią, większą powierzchnię zabudowy oznaczoną S/BOJA, na przykład 81,07, 94,44 i 117,08 m² dla mieszkania 2, a tarasy w ten sam sposób. Ta strona korzysta z powierzchni zabudowy, tarasów zabudowanych i ogrodów z cennika, a które liczby przyjmuje umowa, potwierdzamy.',
  'For hver bolig gir listen et nettoareal, et bebygd areal og et tredje, større bebygd areal merket S/BOJA, for eksempel 81,07, 94,44 og 117,08 m² for leilighet 2, og terrassene på samme måte. Denne siden bruker listens bebygde areal, bebygde terrasser og hager, og vi bekrefter hvilke tall kontrakten legger til grunn.',
  'För varje bostad anger listan en boyta, en byggyta och en tredje, större byggyta markerad S/BOJA, till exempel 81,07, 94,44 och 117,08 m² för lägenhet 2, och terrasserna på samma sätt. Den här sidan använder listans byggyta, byggda terrasser och trädgårdar, och vi bekräftar vilka siffror avtalet utgår från.')
a('.trustDossier.cards[5][1]',
  'La memoria de los adosados incluye como estándar una piscina privada en el solárium y dice también que las opciones de piscina están por consultar. Sus planos muestran un jacuzzi en el solárium, y la memoria incluye los jacuzzis como opciones. En los apartamentos, las piscinas y los jacuzzis son opciones sujetas a viabilidad. Confirmamos lo que incluye la vivienda que usted elija.',
  'Le descriptif des maisons mitoyennes indique en standard une piscine privée sur le solarium et précise aussi que les options de piscine sont à consulter. Leurs plans montrent un jacuzzi sur le solarium, et le descriptif place les jacuzzis parmi les options. Pour les appartements, les piscines et les jacuzzis sont des options soumises à faisabilité. Nous confirmons ce qu’inclut le logement que vous choisissez.',
  'Die Beschreibung der Reihenhäuser nennt als Standard einen privaten Pool auf dem Solarium und sagt zugleich, dass Pooloptionen noch zu klären sind. Auf ihren Plänen ist ein Whirlpool auf dem Solarium zu sehen, und die Beschreibung führt Whirlpools als Optionen auf. Bei den Wohnungen sind Pools und Whirlpools Optionen, abhängig von der Machbarkeit. Wir bestätigen, was die von Ihnen gewählte Immobilie umfasst.',
  'В спецификации таунхаусов в стандарт входит частный бассейн на солярии, и в ней же сказано, что варианты бассейна нужно уточнять. На их планах на солярии показано джакузи, а в спецификации джакузи указаны как опции. Для квартир бассейны и джакузи — опции при условии технической возможности. Мы подтверждаем, что входит в выбранный вами объект.',
  'تورد مواصفات المنازل المتلاصقة ضمن البنود القياسية مسبحًا خاصًا على السولاريوم، وتقول أيضًا إن خيارات المسبح يُرجع إليها للاستفسار. وتُظهر مخططاتها جاكوزي على السولاريوم، فيما تدرج المواصفات الجاكوزي ضمن الخيارات. أما في الشقق فالمسابح والجاكوزي خيارات رهنًا بإمكانية التنفيذ. ونؤكد ما يشمله المسكن الذي تختارونه.',
  'De omschrijving van de herenhuizen noemt als standaard een privézwembad op het solarium en zegt ook dat zwembadopties nog moeten worden nagevraagd. Hun plattegronden tonen een jacuzzi op het solarium, en de omschrijving noemt jacuzzi’s als opties. Bij de appartementen zijn zwembaden en jacuzzi’s opties, afhankelijk van de haalbaarheid. Wij bevestigen wat de woning die u kiest omvat.',
  'Opis domów szeregowych podaje w standardzie prywatny basen na solarium i jednocześnie mówi, że opcje basenu należy skonsultować. Na ich rzutach widać jacuzzi na solarium, a opis wymienia jacuzzi jako opcje. W mieszkaniach baseny i jacuzzi są opcjami, zależnymi od możliwości technicznych. Potwierdzamy, co obejmuje wybrany przez Pana/Panią lokal.',
  'Beskrivelsen av rekkehusene oppgir som standard et eget basseng på solariet og sier også at bassengalternativer må forhøres om. Planene deres viser et boblebad på solariet, og beskrivelsen oppfører boblebad som tilvalg. For leilighetene er basseng og boblebad tilvalg som avhenger av gjennomførbarhet. Vi bekrefter hva boligen De velger omfatter.',
  'Beskrivningen av radhusen anger som standard en egen pool på solterrassen och säger också att poolalternativ ska efterfrågas. Deras ritningar visar en jacuzzi på solterrassen, och beskrivningen listar jacuzzi som tillval. För lägenheterna är pooler och jacuzzi tillval som beror på genomförbarheten. Vi bekräftar vad den bostad ni väljer omfattar.')
a('.trustDossier.cards[6][0]',
  'Las imágenes', 'Les images', 'Die Bilder', 'Изображения', 'الصور', 'De beelden', 'Wizualizacje', 'Bildene', 'Bilderna')
a('.trustDossier.cards[6][1]',
  'Las imágenes están generadas por ordenador, salvo la imagen aérea, que es una fotografía de la zona con el complejo recreado en ella. Los interiores muestran viviendas amuebladas, y los documentos no dicen qué vivienda muestra cada uno. El mobiliario y la decoración no están incluidos.',
  'Les images sont générées par ordinateur, sauf l’image aérienne, qui est une photographie du secteur dans laquelle l’ensemble a été intégré en image de synthèse. Les intérieurs montrent des logements meublés, et les documents ne disent pas quel logement chacun représente. Le mobilier et la décoration ne sont pas inclus.',
  'Die Bilder sind computergeneriert, mit Ausnahme der Luftaufnahme, die ein Foto der Gegend ist, in das die Anlage als Rendering eingefügt wurde. Die Innenräume zeigen möblierte Immobilien, und die Dokumente sagen nicht, welche Immobilie jeweils zu sehen ist. Möbel und Dekoration sind nicht enthalten.',
  'Изображения созданы на компьютере, кроме аэрофотоснимка, который представляет собой фотографию местности с вмонтированным в неё комплексом. На изображениях интерьеров показано меблированное жильё, и в документах не сказано, какой именно объект на каждом из них. Мебель и декор не входят в цену.',
  'الصور مولّدة بالحاسوب، باستثناء الصورة الجوية التي هي صورة فوتوغرافية للمنطقة أُدرج فيها المجمّع بالتصيير. وتُظهر المساحات الداخلية مساكن مفروشة، ولا تذكر الوثائق أي مسكن تُظهره كل صورة. والأثاث والديكور غير مشمولين.',
  'De beelden zijn computergegenereerd, behalve het luchtbeeld, dat een foto van het gebied is waarin het complex is gerenderd. De interieurs tonen gemeubileerde woningen, en de documenten zeggen niet welke woning elk beeld toont. Het meubilair en de decoratie zijn niet inbegrepen.',
  'Wizualizacje są wygenerowane komputerowo, z wyjątkiem ujęcia z lotu ptaka, które jest zdjęciem okolicy z wmontowanym kompleksem. Wnętrza pokazują umeblowane lokale, a dokumenty nie podają, który lokal przedstawia każde z nich. Meble i dekoracje nie są wliczone.',
  'Bildene er datagenererte, bortsett fra flyfotoet, som er et fotografi av området med komplekset lagt inn som visualisering. Interiørene viser møblerte boliger, og dokumentene sier ikke hvilken bolig hvert bilde viser. Møbler og dekorasjon er ikke inkludert.',
  'Bilderna är datorgenererade, utom flygbilden, som är ett fotografi av området med området inlagt som visualisering. Interiörerna visar möblerade bostäder, och dokumenten säger inte vilken bostad varje bild visar. Möbler och dekoration ingår inte.')
a('.trustDossier.cards[7][1]',
  'Los documentos no dan dirección ni coordenadas, de modo que el marcador del mapa está en Cancelada por zona y no sobre la parcela, y las distancias por carretera junto al mapa se miden desde ese marcador. El dosier da una distancia, 20 minutos hasta el Real Club Valderrama, sin decir cómo se recorre. Confirmamos las distancias en una visita.',
  'Les documents ne donnent ni adresse ni coordonnées ; le repère sur la carte est donc placé à Cancelada, par secteur, et non sur la parcelle, et les distances routières indiquées à côté de la carte sont mesurées depuis ce repère. Le dossier donne une distance, 20 minutes jusqu’au Real Club Valderrama, sans dire comment on la parcourt. Nous confirmons les distances lors d’une visite.',
  'Die Dokumente nennen weder Adresse noch Koordinaten; die Markierung auf der Karte liegt daher in Cancelada nach Gebiet und nicht auf dem Grundstück, und die Straßenentfernungen neben der Karte werden von dieser Markierung aus gemessen. Das Dossier nennt eine Entfernung, 20 Minuten bis zum Real Club Valderrama, ohne zu sagen, wie sie zurückgelegt wird. Die Entfernungen bestätigen wir bei einem Besuch.',
  'В документах нет ни адреса, ни координат, поэтому маркер на карте стоит в Канселаде по району, а не на участке, и расстояния по дорогам рядом с картой отсчитываются от этого маркера. В досье указано одно расстояние — 20 минут до Real Club Valderrama, — без пояснения, как его преодолевать. Расстояния мы подтверждаем во время визита.',
  'لا تذكر الوثائق عنوانًا ولا إحداثيات، ولذلك فإن العلامة على الخريطة موضوعة في كانسيلادا بحسب المنطقة وليست على القطعة، وتُقاس مسافات الطرق المجاورة للخريطة من هذه العلامة. ويذكر الملف مسافة واحدة، 20 دقيقة إلى Real Club Valderrama، دون أن يبيّن كيف تُقطع. ونؤكد المسافات أثناء زيارة.',
  'De documenten geven geen adres of coördinaten, dus de markering op de kaart staat in Cancelada per gebied en niet op het perceel, en de wegafstanden naast de kaart worden vanaf die markering gemeten. Het dossier geeft één afstand, 20 minuten tot de Real Club Valderrama, zonder te zeggen hoe die wordt afgelegd. Wij bevestigen de afstanden tijdens een bezoek.',
  'Dokumenty nie podają adresu ani współrzędnych, dlatego znacznik na mapie znajduje się w Cancelada według obszaru, a nie na działce, a odległości drogowe obok mapy mierzone są od tego znacznika. Dossier podaje jedną odległość, 20 minut do Real Club Valderrama, bez wyjaśnienia, jak ją pokonać. Odległości potwierdzamy podczas wizyty.',
  'Dokumentene oppgir verken adresse eller koordinater, så markøren på kartet står i Cancelada etter område og ikke på tomten, og veiavstandene ved siden av kartet måles fra denne markøren. Dossieret oppgir én avstand, 20 minutter til Real Club Valderrama, uten å si hvordan den tilbakelegges. Vi bekrefter avstandene ved et besøk.',
  'Dokumenten anger varken adress eller koordinater, så markören på kartan står i Cancelada efter område och inte på tomten, och vägavstånden vid sidan av kartan mäts från den markören. Dossiern anger ett avstånd, 20 minuter till Real Club Valderrama, utan att säga hur det tillryggaläggs. Vi bekräftar avstånden vid ett besök.')

# ---- availability, enquiry, FAQ, SEO ------------------------------------------------------------------

a('.availability.copy',
  'Hay 23 viviendas con precio: 13 apartamentos de dos dormitorios y 10 adosados de tres dormitorios. Los precios son los de la lista de precios del promotor del 26 de octubre de 2026 y no incluyen IVA, y confirmamos la disponibilidad y el precio antes de cualquier reserva. Las otras 28 viviendas de la lista figuran como reservadas y no están disponibles.',
  '23 logements sont indiqués avec un prix : 13 appartements de deux chambres et 10 maisons mitoyennes de trois chambres. Les prix sont ceux de la liste de prix du promoteur du 26 octobre 2026 et s’entendent hors TVA ; nous confirmons la disponibilité et le prix avant toute réservation. Les 28 autres logements de la liste sont marqués comme réservés et ne sont pas disponibles.',
  '23 Immobilien sind mit einem Preis aufgeführt: 13 Wohnungen mit zwei Schlafzimmern und 10 Reihenhäuser mit drei Schlafzimmern. Die Preise stammen aus der Preisliste des Bauträgers vom 26. Oktober 2026 und verstehen sich zuzüglich MwSt.; Verfügbarkeit und Preis bestätigen wir vor jeder Reservierung. Die übrigen 28 Immobilien der Liste sind als reserviert gekennzeichnet und nicht verfügbar.',
  'Цена указана у 23 объектов: 13 квартир с двумя спальнями и 10 таунхаусов с тремя спальнями. Цены взяты из прайс-листа застройщика от 26 октября 2026 года и указаны без НДС; наличие и цену мы подтверждаем до любого бронирования. Остальные 28 объектов списка отмечены как забронированные и недоступны.',
  'لـ 23 مسكنًا سعر مدرج: 13 شقة بغرفتي نوم و10 منازل متلاصقة بثلاث غرف نوم. والأسعار هي أسعار قائمة المطوّر المؤرخة في 26 أكتوبر 2026 ولا تشمل ضريبة القيمة المضافة، ونؤكد التوفر والسعر قبل أي حجز. أما المساكن الـ 28 الأخرى في القائمة فهي معلَّمة كمحجوزة وغير متاحة.',
  '23 woningen staan met een prijs op de lijst: 13 appartementen met twee slaapkamers en 10 herenhuizen met drie slaapkamers. De prijzen zijn die van de prijslijst van de ontwikkelaar van 26 oktober 2026 en zijn exclusief btw; wij bevestigen de beschikbaarheid en de prijs vóór elke reservering. De overige 28 woningen op de lijst zijn als gereserveerd gemarkeerd en niet beschikbaar.',
  'Cenę ma 23 lokali: 13 mieszkań z dwiema sypialniami i 10 domów szeregowych z trzema sypialniami. Ceny pochodzą z cennika dewelopera z 26 października 2026 r. i nie zawierają VAT; dostępność i cenę potwierdzamy przed jakąkolwiek rezerwacją. Pozostałe 28 lokali z cennika oznaczono jako zarezerwowane i nie są dostępne.',
  '23 boliger er oppført med pris: 13 leiligheter med to soverom og 10 rekkehus med tre soverom. Prisene er de fra utbyggerens prisliste av 26. oktober 2026 og er eksklusive mva.; vi bekrefter tilgjengelighet og pris før enhver reservasjon. De øvrige 28 boligene på listen er merket som reservert og er ikke tilgjengelige.',
  '23 bostäder är upptagna med pris: 13 lägenheter med två sovrum och 10 radhus med tre sovrum. Priserna är de i exploatörens prislista från den 26 oktober 2026 och är exklusive IVA; vi bekräftar tillgänglighet och pris före varje reservation. De övriga 28 bostäderna i listan är markerade som reserverade och är inte tillgängliga.')
a('.availability.sourceNote',
  'Los precios, los dormitorios y las superficies están transcritos de la lista de precios del promotor del 26 de octubre de 2026, que tiene 51 filas: 36 apartamentos y 15 adosados. 23 filas tienen precio y 28 figuran como reservadas. La lista muestra un importe de IVA del 10% junto a cada precio, de modo que los precios no incluyen IVA. La superficie construida, la terraza y el jardín son las cifras construidas de la lista. Cada vivienda se muestra con su propio plano, y el segundo plano de una vivienda aparece en la galería de arriba.',
  'Les prix, les chambres et les surfaces sont transcrits de la liste de prix du promoteur du 26 octobre 2026, qui compte 51 lignes : 36 appartements et 15 maisons mitoyennes. 23 lignes ont un prix et 28 sont marquées comme réservées. La liste indique un montant de TVA de 10 % à côté de chaque prix, de sorte que les prix s’entendent hors TVA. La surface construite, la terrasse et le jardin sont les chiffres construits de la liste. Chaque logement est présenté avec son propre plan, et le second plan d’un logement figure dans la galerie ci-dessus.',
  'Preise, Schlafzimmer und Flächen sind aus der Preisliste des Bauträgers vom 26. Oktober 2026 übernommen, die 51 Zeilen hat: 36 Wohnungen und 15 Reihenhäuser. 23 Zeilen haben einen Preis, 28 sind als reserviert gekennzeichnet. Die Liste zeigt neben jedem Preis einen MwSt.-Betrag von 10 %, die Preise verstehen sich also zuzüglich MwSt. Die bebaute Fläche, die Terrasse und der Garten sind die bebauten Werte der Liste. Jede Immobilie wird mit ihrem eigenen Plan gezeigt, und der zweite Plan einer Immobilie erscheint in der Galerie oben.',
  'Цены, число спален и площади перенесены из прайс-листа застройщика от 26 октября 2026 года, в котором 51 строка: 36 квартир и 15 таунхаусов. У 23 строк указана цена, 28 отмечены как забронированные. Рядом с каждой ценой в списке указана сумма НДС в размере 10 %, поэтому цены даны без НДС. Площадь застройки, терраса и сад — это значения по застройке из списка. Каждый объект показан со своим планом, а второй план объекта находится в галерее выше.',
  'الأسعار وعدد غرف النوم والمساحات منقولة من قائمة أسعار المطوّر المؤرخة في 26 أكتوبر 2026، وهي تضم 51 صفًا: 36 شقة و15 منزلًا متلاصقًا. لـ 23 صفًا سعر و28 صفًا معلَّم كمحجوز. وتُظهر القائمة مبلغ ضريبة القيمة المضافة بنسبة 10% بجانب كل سعر، ولذلك فالأسعار لا تشمل ضريبة القيمة المضافة. والمساحة المبنية والتراس والحديقة هي الأرقام المبنية الواردة في القائمة. ويُعرض كل مسكن مع مخططه الخاص، ويظهر المخطط الثاني للمسكن في المعرض أعلاه.',
  'De prijzen, slaapkamers en oppervlakten zijn overgenomen uit de prijslijst van de ontwikkelaar van 26 oktober 2026, die 51 regels heeft: 36 appartementen en 15 herenhuizen. 23 regels hebben een prijs en 28 zijn als gereserveerd gemarkeerd. De lijst toont naast elke prijs een btw-bedrag van 10%, dus de prijzen zijn exclusief btw. De bebouwde oppervlakte, het terras en de tuin zijn de bebouwde cijfers van de lijst. Elke woning wordt met haar eigen plattegrond getoond, en de tweede plattegrond van een woning staat in de galerij hierboven.',
  'Ceny, liczba sypialni i powierzchnie zostały przepisane z cennika dewelopera z 26 października 2026 r., który ma 51 wierszy: 36 mieszkań i 15 domów szeregowych. 23 wiersze mają cenę, a 28 oznaczono jako zarezerwowane. Cennik podaje obok każdej ceny kwotę VAT w wysokości 10%, więc ceny nie zawierają VAT. Powierzchnia zabudowy, taras i ogród to wartości zabudowy z cennika. Każdy lokal jest pokazany z własnym rzutem, a drugi rzut lokalu znajduje się w galerii powyżej.',
  'Priser, soverom og arealer er hentet fra utbyggerens prisliste av 26. oktober 2026, som har 51 rader: 36 leiligheter og 15 rekkehus. 23 rader har pris og 28 er merket som reservert. Listen viser et mva.-beløp på 10 % ved siden av hver pris, så prisene er eksklusive mva. Det bebygde arealet, terrassen og hagen er listens bebygde tall. Hver bolig vises med sin egen plan, og den andre planen til en bolig vises i galleriet ovenfor.',
  'Priser, sovrum och ytor är hämtade från exploatörens prislista från den 26 oktober 2026, som har 51 rader: 36 lägenheter och 15 radhus. 23 rader har pris och 28 är markerade som reserverade. Listan visar ett IVA-belopp på 10 % bredvid varje pris, så priserna är exklusive IVA. Byggytan, terrassen och trädgården är listans byggda värden. Varje bostad visas med sin egen ritning, och en bostads andra ritning finns i galleriet ovan.')

a('.enquiry.headlineHtml',
  'Pregunte por <em>Haiku Estepona</em>', 'Renseignez-vous sur <em>Haiku Estepona</em>', 'Fragen Sie nach <em>Haiku Estepona</em>', 'Узнайте о <em>Haiku Estepona</em>',
  'استفسر عن <em>Haiku Estepona</em>', 'Vraag naar <em>Haiku Estepona</em>', 'Zapytanie o <em>Haiku Estepona</em>', 'Spør om <em>Haiku Estepona</em>', 'Fråga om <em>Haiku Estepona</em>')
a('.enquiry.message',
  'Hola, Nueva Living, me gustaría recibir información sobre Haiku Estepona.',
  'Bonjour Nueva Living, je souhaiterais des informations sur Haiku Estepona.',
  'Guten Tag Nueva Living, ich möchte Informationen zu Haiku Estepona erhalten.',
  'Здравствуйте, Nueva Living! Хочу получить информацию о Haiku Estepona.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Haiku Estepona.',
  'Goedendag Nueva Living, ik wil graag informatie over Haiku Estepona.',
  'Dzień dobry, Nueva Living, proszę o informacje o Haiku Estepona.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Haiku Estepona.',
  'Hej Nueva Living, jag vill gärna ha information om Haiku Estepona.')

a('.faq[0][1]',
  '23 de 51: 13 apartamentos de dos dormitorios de {E505000} a {E675000} y 10 adosados de tres dormitorios de {E962000} a {E1165000}, más IVA. Las otras 28 figuran como reservadas.',
  '23 sur 51 : 13 appartements de deux chambres de {E505000} à {E675000} et 10 maisons mitoyennes de trois chambres de {E962000} à {E1165000}, hors TVA. Les 28 autres sont marqués comme réservés.',
  '23 von 51: 13 Wohnungen mit zwei Schlafzimmern von {E505000} bis {E675000} und 10 Reihenhäuser mit drei Schlafzimmern von {E962000} bis {E1165000}, zuzüglich MwSt. Die übrigen 28 sind als reserviert gekennzeichnet.',
  '23 из 51: 13 квартир с двумя спальнями от {E505000} до {E675000} и 10 таунхаусов с тремя спальнями от {E962000} до {E1165000} без НДС. Остальные 28 отмечены как забронированные.',
  '23 من أصل 51: 13 شقة بغرفتي نوم من {E505000} إلى {E675000} و10 منازل متلاصقة بثلاث غرف نوم من {E962000} إلى {E1165000}، دون ضريبة القيمة المضافة. أما الـ 28 الأخرى فمعلَّمة كمحجوزة.',
  '23 van de 51: 13 appartementen met twee slaapkamers van {E505000} tot {E675000} en 10 herenhuizen met drie slaapkamers van {E962000} tot {E1165000}, excl. btw. De overige 28 zijn als gereserveerd gemarkeerd.',
  '23 z 51: 13 mieszkań z dwiema sypialniami od {E505000} do {E675000} i 10 domów szeregowych z trzema sypialniami od {E962000} do {E1165000}, plus VAT. Pozostałe 28 oznaczono jako zarezerwowane.',
  '23 av 51: 13 leiligheter med to soverom fra {E505000} til {E675000} og 10 rekkehus med tre soverom fra {E962000} til {E1165000}, pluss mva. De øvrige 28 er merket som reservert.',
  '23 av 51: 13 lägenheter med två sovrum från {E505000} till {E675000} och 10 radhus med tre sovrum från {E962000} till {E1165000}, plus IVA. De övriga 28 är markerade som reserverade.')
a('.faq[2][1]',
  'En la lista, cada apartamento tiene dos plazas de aparcamiento numeradas y un trastero, aunque el dosier menciona una plaza de aparcamiento. Cada adosado tiene un garaje en su plano del sótano. Confirmamos lo que incluye el precio.',
  'Dans la liste, chaque appartement a deux places de stationnement numérotées et une cave, alors que le dossier mentionne une place de stationnement. Chaque maison mitoyenne a un garage sur son plan du sous-sol. Nous confirmons ce que comprend le prix.',
  'In der Liste hat jede Wohnung zwei nummerierte Stellplätze und einen Abstellraum, obwohl das Dossier einen Stellplatz nennt. Jedes Reihenhaus hat auf seinem Plan des Untergeschosses eine Garage. Wir bestätigen, was der Preis umfasst.',
  'В списке у каждой квартиры по два пронумерованных парковочных места и кладовая, хотя в досье упомянуто одно парковочное место. У каждого таунхауса на плане цокольного этажа есть гараж. Мы подтверждаем, что входит в цену.',
  'في القائمة لكل شقة موقفان مرقّمان لوقوف السيارات وغرفة تخزين، مع أن الملف يذكر موقفًا واحدًا. ولكل منزل متلاصق مرآب في مخطط القبو. ونؤكد ما يشمله السعر.',
  'In de lijst heeft elk appartement twee genummerde parkeerplaatsen en een berging, hoewel het dossier één parkeerplaats noemt. Elk herenhuis heeft een garage op de plattegrond van de kelder. Wij bevestigen wat de prijs omvat.',
  'W cenniku każde mieszkanie ma dwa numerowane miejsca postojowe i komórkę lokatorską, choć dossier wspomina o jednym miejscu postojowym. Każdy dom szeregowy ma garaż na rzucie sutereny. Potwierdzamy, co obejmuje cena.',
  'På listen har hver leilighet to nummererte parkeringsplasser og en bod, selv om dossieret nevner én parkeringsplass. Hvert rekkehus har en garasje på kjellerplanen. Vi bekrefter hva prisen omfatter.',
  'I listan har varje lägenhet två numrerade parkeringsplatser och ett förråd, även om dossiern nämner en parkeringsplats. Varje radhus har ett garage på källarplanets ritning. Vi bekräftar vad priset omfattar.')
a('.faq[3][0]',
  '¿Hay piscina privada o jacuzzi?', 'Y a-t-il une piscine privée ou un jacuzzi ?', 'Gibt es einen privaten Pool oder einen Whirlpool?', 'Есть ли частный бассейн или джакузи?',
  'هل يوجد مسبح خاص أو جاكوزي؟', 'Is er een privézwembad of een jacuzzi?', 'Czy jest prywatny basen lub jacuzzi?', 'Finnes det et eget basseng eller boblebad?', 'Finns det en egen pool eller jacuzzi?')
a('.faq[3][1]',
  'La memoria de calidades de los adosados incluye como estándar una piscina privada en el solárium, mientras que sus planos muestran un jacuzzi, de modo que confirmamos cuál está incluido. En los apartamentos, las piscinas y los jacuzzis son opciones sujetas a viabilidad, y el plano del apartamento 35 muestra un jacuzzi en su terraza de la cubierta.',
  'Le descriptif des maisons mitoyennes indique en standard une piscine privée sur le solarium, alors que leurs plans montrent un jacuzzi ; nous confirmons donc lequel est inclus. Pour les appartements, les piscines et les jacuzzis sont des options soumises à faisabilité, et le plan de l’appartement 35 montre un jacuzzi sur son toit-terrasse.',
  'Die Ausstattungsbeschreibung der Reihenhäuser nennt als Standard einen privaten Pool auf dem Solarium, während ihre Pläne einen Whirlpool zeigen; wir bestätigen daher, was enthalten ist. Bei den Wohnungen sind Pools und Whirlpools Optionen, abhängig von der Machbarkeit, und der Plan der Wohnung 35 zeigt einen Whirlpool auf ihrer Dachterrasse.',
  'В спецификации таунхаусов в стандарт входит частный бассейн на солярии, тогда как на их планах показано джакузи, поэтому мы подтверждаем, что именно включено. Для квартир бассейны и джакузи — опции при условии технической возможности; на плане квартиры 35 джакузи показано на террасе на крыше.',
  'تورد مواصفات الجودة للمنازل المتلاصقة مسبحًا خاصًا على السولاريوم ضمن البنود القياسية، بينما تُظهر مخططاتها جاكوزي، ولذلك نؤكد أيهما مشمول. أما في الشقق فالمسابح والجاكوزي خيارات رهنًا بإمكانية التنفيذ، ويُظهر مخطط الشقة 35 جاكوزي على تراس السطح.',
  'De technische omschrijving van de herenhuizen noemt als standaard een privézwembad op het solarium, terwijl hun plattegronden een jacuzzi tonen; wij bevestigen daarom welke van de twee is inbegrepen. Bij de appartementen zijn zwembaden en jacuzzi’s opties, afhankelijk van de haalbaarheid, en de plattegrond van appartement 35 toont een jacuzzi op het dakterras.',
  'Standard wykończenia domów szeregowych obejmuje prywatny basen na solarium, podczas gdy ich rzuty pokazują jacuzzi, dlatego potwierdzamy, co jest wliczone. W mieszkaniach baseny i jacuzzi są opcjami, zależnymi od możliwości technicznych, a rzut mieszkania 35 pokazuje jacuzzi na tarasie na dachu.',
  'Byggebeskrivelsen for rekkehusene oppgir som standard et eget basseng på solariet, mens planene deres viser et boblebad, så vi bekrefter hva som er inkludert. For leilighetene er basseng og boblebad tilvalg som avhenger av gjennomførbarhet, og planen for leilighet 35 viser et boblebad på takterrassen.',
  'Byggnadsbeskrivningen för radhusen anger som standard en egen pool på solterrassen, medan deras ritningar visar en jacuzzi, så vi bekräftar vilken som ingår. För lägenheterna är pooler och jacuzzi tillval som beror på genomförbarheten, och ritningen för lägenhet 35 visar en jacuzzi på takterrassen.')
a('.faq[6][1]',
  'La lista muestra una reserva de {E9000} y un pago a la firma del contrato que lleva el total al 30%, con el resto en la escritura, y dos pagos aplazados del 5% sin fechas. Confirmamos el calendario por escrito.',
  'La liste indique une réservation de {E9000} et un paiement à la signature du contrat qui porte le total à 30 %, le solde étant dû à l’acte, ainsi que deux paiements différés de 5 % sans dates. Nous confirmons l’échéancier par écrit.',
  'Die Liste zeigt eine Reservierung von {E9000} und eine Zahlung bei Vertragsabschluss, mit der die Gesamtzahlung 30 % erreicht, den Rest bei der Beurkundung, sowie zwei aufgeschobene Raten von je 5 % ohne Datum. Den Zahlungsplan bestätigen wir schriftlich.',
  'В списке указаны бронирование {E9000} и платёж при подписании договора, после которого общая сумма составляет 30 %, остаток при подписании нотариального акта, а также два отсроченных платежа по 5 % без дат. График мы подтверждаем в письменном виде.',
  'تُظهر القائمة حجزًا بمبلغ {E9000} ودفعة عند توقيع العقد يبلغ بها المجموع 30%، على أن يُدفع الباقي عند التوقيع على سند الملكية، ودفعتين مؤجلتين بنسبة 5% دون تواريخ. ونؤكد الجدول كتابةً.',
  'De lijst toont een reservering van {E9000} en een betaling bij het koopcontract waarmee het totaal op 30% komt, met het restant bij de akte, en twee uitgestelde termijnen van 5% zonder data. Wij bevestigen het schema schriftelijk.',
  'Cennik wskazuje rezerwację w wysokości {E9000} i płatność przy umowie, po której łączna wpłata wynosi 30%, resztę przy akcie notarialnym oraz dwie płatności odroczone po 5%, bez dat. Harmonogram potwierdzamy na piśmie.',
  'Listen viser en reservasjon på {E9000} og en betaling ved kontrakten som bringer det samlede beløpet opp i 30 %, med resten ved overtakelsen, og to utsatte delbetalinger på 5 % uten datoer. Vi bekrefter betalingsplanen skriftlig.',
  'Listan visar en reservation på {E9000} och en betalning vid kontraktet som för totalen till 30 %, med resten vid lagfarten, och två uppskjutna delbetalningar på 5 % utan datum. Vi bekräftar betalningsplanen skriftligt.')

a('.seo.title',
  'Haiku Estepona - Apartamentos y adosados', 'Haiku Estepona - Appartements et maisons mitoyennes', 'Haiku Estepona - Wohnungen und Reihenhäuser',
  'Haiku Estepona - квартиры и таунхаусы', 'Haiku Estepona - شقق ومنازل متلاصقة', 'Haiku Estepona - Appartementen en herenhuizen',
  'Haiku Estepona - mieszkania i domy szeregowe', 'Haiku Estepona - leiligheter og rekkehus', 'Haiku Estepona - lägenheter och radhus')
a('.seo.h1',
  'Haiku Estepona: apartamentos y adosados en Cancelada, Estepona',
  'Haiku Estepona : appartements et maisons mitoyennes à Cancelada, Estepona',
  'Haiku Estepona: Wohnungen und Reihenhäuser in Cancelada, Estepona',
  'Haiku Estepona: квартиры и таунхаусы в Канселаде, Эстепона',
  'Haiku Estepona: شقق ومنازل متلاصقة في كانسيلادا، إستيبونا',
  'Haiku Estepona: appartementen en herenhuizen in Cancelada, Estepona',
  'Haiku Estepona: mieszkania i domy szeregowe w Cancelada, Estepona',
  'Haiku Estepona: leiligheter og rekkehus i Cancelada, Estepona',
  'Haiku Estepona: lägenheter och radhus i Cancelada, Estepona')
a('.seo.h1Context',
  'Apartamentos y adosados en Cancelada, Estepona', 'Appartements et maisons mitoyennes à Cancelada, Estepona', 'Wohnungen und Reihenhäuser in Cancelada, Estepona',
  'Квартиры и таунхаусы в Канселаде, Эстепона', 'شقق ومنازل متلاصقة في كانسيلادا، إستيبونا', 'Appartementen en herenhuizen in Cancelada, Estepona',
  'Mieszkania i domy szeregowe w Cancelada, Estepona', 'Leiligheter og rekkehus i Cancelada, Estepona', 'Lägenheter och radhus i Cancelada, Estepona')

# ---- unit sizes and plan labels (templates: every unit and plan follows the same pattern) -------------

SIZE = {  # built, terrace, garden label, per locale; ru and ar put the label before / after differently
    'es': ('{b} {U} construidos, {t} {U} de terraza', ', {g} {U} de jardín'),
    'fr': ('{b} {U} construits, {t} {U} de terrasse', ', {g} {U} de jardin'),
    'de': ('{b} {U} bebaut, {t} {U} Terrasse', ', {g} {U} Garten'),
    'ru': ('{b} {U} застроенной площади, терраса {t} {U}', ', сад {g} {U}'),
    'ar': ('{b} {U} مبنية، {t} {U} تراس', '، {g} {U} حديقة'),
    'nl': ('{b} {U} bebouwd, {t} {U} terras', ', {g} {U} tuin'),
    'pl': ('{b} {U} zabudowy, {t} {U} tarasu', ', {g} {U} ogrodu'),
    'no': ('{b} {U} bebygd, {t} {U} terrasse', ', {g} {U} hage'),
    'sv': ('{b} {U} byggyta, {t} {U} terrass', ', {g} {U} trädgård'),
}
n_size = 0
for u in proj['availability']['units']:
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm garden)?', u['size'])
    assert m, u['size']
    b, t, g = m.groups()
    out = {}
    for l in LOCS:
        head, tail = SIZE[l]
        s = head.replace('{b}', num(b, l)).replace('{t}', num(t, l)).replace('{U}', UNIT[l])
        if g:
            s += tail.replace('{g}', num(g, l)).replace('{U}', UNIT[l])
        out[l] = s
    assert u['size'] not in T or T[u['size']] == out
    T[u['size']] = out
    n_size += 1

PLAN = {  # apartment, townhouse
    'es': ('Plano del apartamento {n}', 'Plano del adosado {n}', 'Apartamento {n}', 'Adosado {n}'),
    'fr': ('Plan de l’appartement {n}', 'Plan de la maison mitoyenne {n}', 'Appartement {n}', 'Maison mitoyenne {n}'),
    'de': ('Grundriss der Wohnung {n}', 'Grundriss des Reihenhauses {n}', 'Wohnung {n}', 'Reihenhaus {n}'),
    'ru': ('Планировка квартиры {n}', 'Планировка таунхауса {n}', 'Квартира {n}', 'Таунхаус {n}'),
    'ar': ('مخطط الشقة {n}', 'مخطط المنزل المتلاصق {n}', 'الشقة {n}', 'المنزل المتلاصق {n}'),
    'nl': ('Plattegrond van appartement {n}', 'Plattegrond van herenhuis {n}', 'Appartement {n}', 'Herenhuis {n}'),
    'pl': ('Rzut mieszkania {n}', 'Rzut domu szeregowego {n}', 'Mieszkanie {n}', 'Dom szeregowy {n}'),
    'no': ('Plantegning av leilighet {n}', 'Plantegning av rekkehus {n}', 'Leilighet {n}', 'Rekkehus {n}'),
    'sv': ('Planritning för lägenhet {n}', 'Planritning för radhus {n}', 'Lägenhet {n}', 'Radhus {n}'),
}
LEVEL = {
    'main floor': dict(es='planta principal', fr='niveau principal', de='Hauptebene', ru='основной уровень', ar='المستوى الرئيسي', nl='hoofdniveau', pl='poziom główny', no='hovedplan', sv='huvudplan'),
    'roof terrace': dict(es='terraza en la cubierta', fr='toit-terrasse', de='Dachterrasse', ru='терраса на крыше', ar='تراس السطح', nl='dakterras', pl='taras na dachu', no='takterrasse', sv='takterrass'),
    'basement and bedroom level': dict(es='sótano y nivel de dormitorios', fr='sous-sol et niveau des chambres', de='Untergeschoss und Schlafebene', ru='цокольный этаж и спальный уровень', ar='القبو ومستوى غرف النوم', nl='kelder en slaapkamerniveau', pl='suterena i poziom sypialni', no='kjeller og soveromsplan', sv='källare och sovrumsplan'),
    'living level and solarium': dict(es='nivel de estar y solárium', fr='niveau de séjour et solarium', de='Wohnebene und Solarium', ru='жилой уровень и солярий', ar='مستوى المعيشة والسولاريوم', nl='leefniveau en solarium', pl='poziom dzienny i solarium', no='stueplan og solarium', sv='vardagsplan och solterrass'),
}
n_plan = 0
for it in proj['media']['items']:
    for key in ('alt', 'caption'):
        s = it.get(key, '')
        m = re.fullmatch(r'Floorplan of (apartment|townhouse) (\S+?)(?:, (.+))?', s) if key == 'alt' else \
            re.fullmatch(r'(Apartment|Townhouse) (\S+?)(?:, (.+))', s)
        if not m:
            continue
        kind, ref, lvl = m.group(1).lower(), m.group(2), m.group(3)
        idx = (0 if kind == 'apartment' else 1) + (0 if key == 'alt' else 2)
        out = {}
        for l in LOCS:
            s2 = PLAN[l][idx].replace('{n}', ref)
            if lvl:
                s2 += ('، ' if l == 'ar' else ', ') + LEVEL[lvl][l]
            out[l] = s2
        assert s not in T or T[s] == out, s
        T[s] = out
        n_plan += 1
print('sizes', n_size, 'plan labels', n_plan)

json.dump(T, open(f'{SP}/tr_h.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings to', f'{SP}/tr_h.json')

