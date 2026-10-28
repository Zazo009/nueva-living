# -*- coding: utf-8 -*-
"""Paraiso de Azahar: the strings the translation memory did not have.

Keyed by the English string, as k_olmo.py is, so a change to the English copy cannot silently shift
a translation onto the wrong sentence. Tokens: {E495000} money, {N52.55} decimal number, {U} the area
unit. The unit sizes and the floorplan labels are built from per-locale templates at the bottom of the
file; the tax word is the one the audit holds each language to (IVA, TVA, MwSt., НДС, btw, VAT, mva).
    python3 tools/import/k_paraiso_de_azahar.py <scratch dir>      (writes <dir>/tr_p.json, then run assemble.py)
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


# identifiers: the project's own name and the developer's home codes read the same everywhere
for s in ['Paraíso de Azahar', 'Paraíso de Azahar <em>Estepona</em>', 'Bajo A', 'Bajo B', '1ºA', '1ºB', '1ºC', '1ºD']:
    same(s)

# ---------------------------------------------------------------- the money line and the descriptions
a('From EUR 495,000 + VAT', 'Desde {E495000} + IVA', 'À partir de {E495000} + TVA', 'Ab {E495000} + MwSt.',
  'От {E495000} + НДС', 'ابتداءً من {E495000} + ضريبة القيمة المضافة', 'Vanaf {E495000} + btw', 'Od {E495000} + VAT',
  'Fra {E495000} + mva', 'Från {E495000} + IVA')
a('EUR 495,000 + VAT', '{E495000} + IVA', '{E495000} + TVA', '{E495000} + MwSt.', '{E495000} + НДС',
  '{E495000} + ضريبة القيمة المضافة', '{E495000} + btw', '{E495000} + VAT', '{E495000} + mva', '{E495000} + IVA')
a('EUR 495,000 - EUR 895,000 + VAT', '{E495000} - {E895000} + IVA', '{E495000} - {E895000} + TVA',
  '{E495000} - {E895000} + MwSt.', '{E495000} - {E895000} + НДС', '{E495000} - {E895000} + ضريبة القيمة المضافة',
  '{E495000} - {E895000} + btw', '{E495000} – {E895000} + VAT', '{E495000} - {E895000} + mva', '{E495000} - {E895000} + IVA')
a('47.55 - 83.80 sqm', '{N47.55} - {N83.80} {U}', '{N47.55} - {N83.80} {U}', '{N47.55} - {N83.80} {U}',
  '{N47.55} - {N83.80} {U}', '{N47.55} - {N83.80} {U}', '{N47.55} - {N83.80} {U}', '{N47.55}–{N83.80} {U}',
  '{N47.55} - {N83.80} {U}', '{N47.55} - {N83.80} {U}')
a('52.55 - 94.84 sqm', '{N52.55} - {N94.84} {U}', '{N52.55} - {N94.84} {U}', '{N52.55} - {N94.84} {U}',
  '{N52.55} - {N94.84} {U}', '{N52.55} - {N94.84} {U}', '{N52.55} - {N94.84} {U}', '{N52.55}–{N94.84} {U}',
  '{N52.55} - {N94.84} {U}', '{N52.55} - {N94.84} {U}')

a('6 of 10 apartments with one to three bedrooms in a building in the centre of Estepona, next to the old town, each with a garage space and a storage room, one with a patio and a private pool. The documents give no delivery date. From EUR 495,000 plus VAT.',
  '6 de 10 apartamentos de uno a tres dormitorios en un edificio en el centro de Estepona, junto al casco antiguo, cada uno con plaza de garaje y trastero, uno de ellos con patio y piscina privada. Los documentos no dan fecha de entrega. Desde {E495000} más IVA.',
  '6 des 10 appartements d’une à trois chambres, dans un immeuble du centre d’Estepona, à côté de la vieille ville, chacun avec une place de garage et une cave, dont un avec patio et piscine privée. Les documents ne donnent aucune date de livraison. À partir de {E495000} hors TVA.',
  '6 von 10 Wohnungen mit einem bis drei Schlafzimmern in einem Gebäude im Zentrum von Estepona, direkt an der Altstadt, jeweils mit Garagenstellplatz und Abstellraum, eine davon mit Patio und privatem Pool. Die Unterlagen nennen keinen Übergabetermin. Ab {E495000} zuzüglich MwSt.',
  '6 из 10 квартир с одной–тремя спальнями в доме в центре Эстепоны, рядом со старым городом: у каждой есть место в гараже и кладовая, у одной — патио и частный бассейн. Срок сдачи в документах не указан. От {E495000} без НДС.',
  '6 من أصل 10 شقق بغرفة إلى ثلاث غرف نوم في مبنى وسط إستيبونا بجوار البلدة القديمة، لكل منها موقف في المرآب وغرفة تخزين، وإحداها بفناء ومسبح خاص. لا تذكر الوثائق موعد تسليم. ابتداءً من {E495000} دون ضريبة القيمة المضافة.',
  '6 van de 10 appartementen met één tot drie slaapkamers in een gebouw in het centrum van Estepona, naast de oude stad, elk met een garageplaats en een berging, één met een patio en een privézwembad. De documenten geven geen opleveringsdatum. Vanaf {E495000} excl. btw.',
  '6 z 10 mieszkań z jedną do trzech sypialni w budynku w centrum Estepony, obok starego miasta, każde z miejscem garażowym i komórką lokatorską, jedno z patio i prywatnym basenem. Dokumenty nie podają terminu oddania. Od {E495000} plus VAT.',
  '6 av 10 leiligheter med ett til tre soverom i et bygg i sentrum av Estepona, ved siden av gamlebyen, hver med garasjeplass og bod, én med patio og eget basseng. Dokumentene oppgir ingen overleveringsdato. Fra {E495000} pluss mva.',
  '6 av 10 lägenheter med ett till tre sovrum i en byggnad i centrala Estepona, intill gamla stan, var och en med garageplats och förråd, en med patio och egen pool. Dokumenten anger inget tillträdesdatum. Från {E495000} plus IVA.')
a('6 of 10 one-, two- and three-bedroom apartments next to the old town of Estepona, each with a garage space and a storage room, from EUR 495,000 plus VAT.',
  '6 de 10 apartamentos de uno, dos y tres dormitorios junto al casco antiguo de Estepona, cada uno con plaza de garaje y trastero, desde {E495000} más IVA.',
  '6 des 10 appartements d’une, deux et trois chambres à côté de la vieille ville d’Estepona, chacun avec une place de garage et une cave, à partir de {E495000} hors TVA.',
  '6 von 10 Wohnungen mit einem, zwei und drei Schlafzimmern neben der Altstadt von Estepona, jeweils mit Garagenstellplatz und Abstellraum, ab {E495000} zuzüglich MwSt.',
  '6 из 10 квартир с одной, двумя и тремя спальнями рядом со старым городом Эстепоны: у каждой есть место в гараже и кладовая, от {E495000} без НДС.',
  '6 من أصل 10 شقق بغرفة وغرفتين وثلاث غرف نوم بجوار البلدة القديمة في إستيبونا، لكل منها موقف في المرآب وغرفة تخزين، ابتداءً من {E495000} دون ضريبة القيمة المضافة.',
  '6 van de 10 appartementen met één, twee en drie slaapkamers naast de oude stad van Estepona, elk met een garageplaats en een berging, vanaf {E495000} excl. btw.',
  '6 z 10 mieszkań z jedną, dwiema i trzema sypialniami obok starego miasta w Esteponie, każde z miejscem garażowym i komórką lokatorską, od {E495000} plus VAT.',
  '6 av 10 leiligheter med ett, to og tre soverom ved siden av gamlebyen i Estepona, hver med garasjeplass og bod, fra {E495000} pluss mva.',
  '6 av 10 lägenheter med ett, två och tre sovrum intill gamla stan i Estepona, var och en med garageplats och förråd, från {E495000} plus IVA.')
a('One-, two- and three-bedroom apartments in central Estepona with garage and storage, from EUR 495,000 plus VAT.',
  'Apartamentos de uno, dos y tres dormitorios en el centro de Estepona con garaje y trastero, desde {E495000} más IVA.',
  'Appartements d’une, deux et trois chambres au centre d’Estepona avec garage et cave, à partir de {E495000} hors TVA.',
  'Wohnungen mit einem, zwei und drei Schlafzimmern im Zentrum von Estepona mit Garage und Abstellraum, ab {E495000} zuzüglich MwSt.',
  'Квартиры с одной, двумя и тремя спальнями в центре Эстепоны с гаражом и кладовой, от {E495000} без НДС.',
  'شقق بغرفة وغرفتين وثلاث غرف نوم في وسط إستيبونا مع مرآب وغرفة تخزين، ابتداءً من {E495000} دون ضريبة القيمة المضافة.',
  'Appartementen met één, twee en drie slaapkamers in het centrum van Estepona met garage en berging, vanaf {E495000} excl. btw.',
  'Mieszkania z jedną, dwiema i trzema sypialniami w centrum Estepony z garażem i komórką lokatorską, od {E495000} plus VAT.',
  'Leiligheter med ett, to og tre soverom i sentrum av Estepona med garasje og bod, fra {E495000} pluss mva.',
  'Lägenheter med ett, två och tre sovrum i centrala Estepona med garage och förråd, från {E495000} plus IVA.')
a('Central Estepona', 'Centro de Estepona', 'Centre d’Estepona', 'Zentrum von Estepona', 'Центр Эстепоны',
  'وسط إستيبونا', 'Centrum van Estepona', 'Centrum Estepony', 'Sentrum av Estepona', 'Centrala Estepona')
a('6 of 10 one-, two- and three-bedroom apartments in a building next to the old town of Estepona, each with a garage space and a storage room.',
  '6 de 10 apartamentos de uno, dos y tres dormitorios en un edificio junto al casco antiguo de Estepona, cada uno con plaza de garaje y trastero.',
  '6 des 10 appartements d’une, deux et trois chambres dans un immeuble à côté de la vieille ville d’Estepona, chacun avec une place de garage et une cave.',
  '6 von 10 Wohnungen mit einem, zwei und drei Schlafzimmern in einem Gebäude neben der Altstadt von Estepona, jeweils mit Garagenstellplatz und Abstellraum.',
  '6 из 10 квартир с одной, двумя и тремя спальнями в доме рядом со старым городом Эстепоны: у каждой есть место в гараже и кладовая.',
  '6 من أصل 10 شقق بغرفة وغرفتين وثلاث غرف نوم في مبنى بجوار البلدة القديمة في إستيبونا، لكل منها موقف في المرآب وغرفة تخزين.',
  '6 van de 10 appartementen met één, twee en drie slaapkamers in een gebouw naast de oude stad van Estepona, elk met een garageplaats en een berging.',
  '6 z 10 mieszkań z jedną, dwiema i trzema sypialniami w budynku obok starego miasta w Esteponie, każde z miejscem garażowym i komórką lokatorską.',
  '6 av 10 leiligheter med ett, to og tre soverom i et bygg ved siden av gamlebyen i Estepona, hver med garasjeplass og bod.',
  '6 av 10 lägenheter med ett, två och tre sovrum i en byggnad intill gamla stan i Estepona, var och en med garageplats och förråd.')

# ---------------------------------------------------------------- images
a('Computer-generated view of a white building with clay-tile roofs, sage-green shutters and balconies on a cobbled street',
  'Vista generada por ordenador de un edificio blanco con tejados de teja, contraventanas verde salvia y balcones en una calle empedrada',
  'Vue de synthèse d’un immeuble blanc aux toits de tuiles, aux volets vert sauge et aux balcons, dans une rue pavée',
  'Computergenerierte Ansicht eines weißen Gebäudes mit Ziegeldächern, salbeigrünen Fensterläden und Balkonen an einer Kopfsteinpflasterstraße',
  'Компьютерная визуализация белого здания с черепичными крышами, шалфейно-зелёными ставнями и балконами на мощёной улице',
  'منظر مُولَّد بالحاسوب لمبنى أبيض بأسقف من القرميد وأبواب خشبية بلون أخضر مريمي وشرفات على شارع مرصوف بالحجارة',
  'Computergegenereerd beeld van een wit gebouw met pannendaken, saliegroene luiken en balkons aan een geplaveide straat',
  'Komputerowa wizualizacja białego budynku z dachami z dachówki, szałwiowozielonymi okiennicami i balkonami przy brukowanej ulicy',
  'Datagenerert bilde av en hvit bygning med teglsteinstak, salvegrønne skodder og balkonger langs en brosteinsbelagt gate',
  'Datorgenererad bild av en vit byggnad med tegeltak, salviagröna fönsterluckor och balkonger vid en kullerstensgata')
a('Computer-generated aerial view of the clay-tile roofs with roof terraces and private pools set between them',
  'Vista aérea generada por ordenador de los tejados de teja con terrazas en la azotea y piscinas privadas entre ellos',
  'Vue aérienne de synthèse des toits de tuiles, avec des terrasses sur le toit et des piscines privées entre eux',
  'Computergenerierte Luftansicht der Ziegeldächer mit Dachterrassen und privaten Pools dazwischen',
  'Компьютерная аэровизуализация черепичных крыш с террасами на крыше и частными бассейнами между ними',
  'منظر جوي مُولَّد بالحاسوب لأسقف القرميد مع تراسات على السطح ومسابح خاصة بينها',
  'Computergegenereerd luchtbeeld van de pannendaken met dakterrassen en privézwembaden ertussen',
  'Komputerowa wizualizacja z lotu ptaka dachów z dachówki z tarasami na dachu i prywatnymi basenami pomiędzy nimi',
  'Datagenerert flyfoto av teglsteinstakene med takterrasser og egne basseng imellom',
  'Datorgenererad flygbild av tegeltaken med takterrasser och egna pooler emellan')
a('Computer-generated patio with a private pool, a wall fountain, sunloungers and lounge chairs between planted walls',
  'Patio generado por ordenador con piscina privada, una fuente en la pared, tumbonas y sillones entre muros con plantas',
  'Vue de synthèse d’un patio avec une piscine privée, une fontaine murale, des bains de soleil et des fauteuils entre des murs plantés',
  'Computergeneriertes Patio mit privatem Pool, einem Wandbrunnen, Sonnenliegen und Loungesesseln zwischen bepflanzten Mauern',
  'Компьютерная визуализация патио с частным бассейном, настенным фонтаном, шезлонгами и креслами между стенами с зеленью',
  'فناء مُولَّد بالحاسوب بمسبح خاص ونافورة جدارية وكراسي تشمّس ومقاعد جلوس بين جدران مزروعة بالنباتات',
  'Computergegenereerde patio met een privézwembad, een muurfontein, ligbedden en loungestoelen tussen beplante muren',
  'Komputerowa wizualizacja patio z prywatnym basenem, fontanną ścienną, leżakami i fotelami między obsadzonymi roślinami murami',
  'Datagenerert patio med eget basseng, en veggfontene, solsenger og loungestoler mellom beplantede murer',
  'Datorgenererad patio med egen pool, en väggfontän, solsängar och loungestolar mellan planterade murar')
a('Computer-generated main bedroom with a double bed, a timber ceiling panel and a glazed door with a shutter',
  'Dormitorio principal generado por ordenador con cama doble, un panel de madera en el techo y una puerta acristalada con contraventana',
  'Vue de synthèse d’une chambre principale avec un lit double, un panneau de bois au plafond et une porte vitrée avec volet',
  'Computergeneriertes Hauptschlafzimmer mit Doppelbett, einer Holzverkleidung an der Decke und einer verglasten Tür mit Fensterladen',
  'Компьютерная визуализация главной спальни с двуспальной кроватью, деревянной панелью на потолке и остеклённой дверью со ставней',
  'غرفة نوم رئيسية مُولَّدة بالحاسوب بسرير مزدوج ولوح خشبي في السقف وباب زجاجي بمصراع',
  'Computergegenereerde hoofdslaapkamer met een tweepersoonsbed, een houten plafondpaneel en een glazen deur met luik',
  'Komputerowa wizualizacja sypialni głównej z podwójnym łóżkiem, drewnianym panelem na suficie i przeszklonymi drzwiami z okiennicą',
  'Datagenerert hovedsoverom med dobbeltseng, et tretak-panel i taket og en glassdør med skodde',
  'Datorgenererat huvudsovrum med dubbelsäng, en träpanel i taket och en glasdörr med fönsterlucka')

# ---------------------------------------------------------------- media
a('Computer-generated views of the building and the interiors, and the floorplans of the six homes listed.',
  'Vistas generadas por ordenador del edificio y los interiores, y los planos de las seis viviendas a la venta.',
  'Vues de synthèse de l’immeuble et des intérieurs, et plans des six logements annoncés.',
  'Computergenerierte Ansichten des Gebäudes und der Innenräume sowie die Grundrisse der sechs gelisteten Wohnungen.',
  'Компьютерные визуализации здания и интерьеров, а также планировки шести квартир, находящихся в продаже.',
  'مناظر مُولَّدة بالحاسوب للمبنى والمساحات الداخلية، ومخططات المساكن الستة المعروضة.',
  'Computergegenereerde beelden van het gebouw en de interieurs, en de plattegronden van de zes aangeboden woningen.',
  'Komputerowe wizualizacje budynku i wnętrz oraz rzuty sześciu oferowanych mieszkań.',
  'Datagenererte bilder av bygget og interiørene, og plantegningene til de seks annonserte boligene.',
  'Datorgenererade bilder av byggnaden och interiörerna samt planritningarna för de sex listade bostäderna.')
a('All the views are computer-generated, and the furniture and decoration in them are illustrative and not included. The floorplans are the developer’s sales plans: they are not contractual and the room names on them are in Spanish.',
  'Todas las vistas están generadas por ordenador, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los planos de venta del promotor: no tienen carácter contractual y los nombres de las estancias están en español.',
  'Toutes les vues sont des images de synthèse, et le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont les plans de vente du promoteur : ils n’ont pas valeur contractuelle et le nom des pièces y est en espagnol.',
  'Alle Ansichten sind computergeneriert; die darin gezeigten Möbel und die Dekoration dienen der Veranschaulichung und sind nicht enthalten. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, und die Raumbezeichnungen sind auf Spanisch.',
  'Все изображения созданы на компьютере; мебель и декор на них приведены для иллюстрации и в стоимость не входят. Планировки — это продажные планы застройщика: они не имеют договорной силы, а названия помещений на них даны по-испански.',
  'جميع المناظر مُولَّدة بالحاسوب، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. المخططات هي مخططات البيع الخاصة بالمطوّر: وهي غير ملزمة تعاقديًا، وأسماء الغرف عليها بالإسبانية.',
  'Alle beelden zijn computergegenereerd; de meubels en de inrichting erop zijn illustratief en niet inbegrepen. De plattegronden zijn de verkoopplattegronden van de ontwikkelaar: ze zijn niet contractueel en de ruimtenamen erop zijn in het Spaans.',
  'Wszystkie wizualizacje są wygenerowane komputerowo; widoczne na nich meble i wystrój mają charakter poglądowy i nie są wliczone w cenę. Rzuty to plany sprzedażowe dewelopera: nie mają charakteru umownego, a nazwy pomieszczeń są po hiszpańsku.',
  'Alle bildene er datagenererte, og møblene og innredningen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens salgstegninger: de er ikke kontraktsfestet, og romnavnene på dem er på spansk.',
  'Alla bilder är datorgenererade, och möblerna och inredningen i dem är illustrativa och ingår inte. Planritningarna är exploatörens säljplaner: de är inte avtalsgrundande och rummens namn på dem är på spanska.')
a('The building on the street', 'El edificio en la calle', 'L’immeuble dans la rue', 'Das Gebäude an der Straße', 'Здание на улице',
  'المبنى على الشارع', 'Het gebouw aan de straat', 'Budynek przy ulicy', 'Bygget langs gaten', 'Byggnaden vid gatan')
a('The roofs and terraces from above', 'Los tejados y las terrazas desde arriba', 'Les toits et les terrasses vus d’en haut',
  'Die Dächer und Terrassen von oben', 'Крыши и террасы сверху', 'الأسقف والتراسات من الأعلى',
  'De daken en terrassen van bovenaf', 'Dachy i tarasy z góry', 'Takene og terrassene sett ovenfra', 'Taken och terrasserna uppifrån')
a('Computer-generated entrance hall with a timber stair, a planted corner with cacti and a wall carrying the project name',
  'Vestíbulo de entrada generado por ordenador con una escalera de madera, un rincón con cactus y un muro con el nombre del proyecto',
  'Vue de synthèse du hall d’entrée avec un escalier en bois, un coin planté de cactus et un mur portant le nom du programme',
  'Computergenerierte Eingangshalle mit einer Holztreppe, einer bepflanzten Ecke mit Kakteen und einer Wand mit dem Projektnamen',
  'Компьютерная визуализация входного холла с деревянной лестницей, уголком с кактусами и стеной с названием проекта',
  'ردهة مدخل مُولَّدة بالحاسوب بدرج خشبي وزاوية مزروعة بالصبّار وجدار يحمل اسم المشروع',
  'Computergegenereerde entreehal met een houten trap, een beplante hoek met cactussen en een muur met de naam van het project',
  'Komputerowa wizualizacja holu wejściowego z drewnianymi schodami, narożnikiem z kaktusami i ścianą z nazwą projektu',
  'Datagenerert inngangsparti med en tretrapp, et hjørne med kaktuser og en vegg med prosjektnavnet',
  'Datorgenererad entréhall med en trätrappa, ett hörn med kaktusar och en vägg med projektets namn')
a('The entrance hall', 'El vestíbulo de entrada', 'Le hall d’entrée', 'Die Eingangshalle', 'Входной холл', 'ردهة المدخل',
  'De entreehal', 'Hol wejściowy', 'Inngangspartiet', 'Entréhallen')
a('Computer-generated living room and open kitchen with a marble island and a timber ceiling panel',
  'Salón y cocina abierta generados por ordenador con una isla de mármol y un panel de madera en el techo',
  'Vue de synthèse d’un séjour et d’une cuisine ouverte avec un îlot en marbre et un panneau de bois au plafond',
  'Computergenerierter Wohnraum mit offener Küche, einer Marmorinsel und einer Holzverkleidung an der Decke',
  'Компьютерная визуализация гостиной с открытой кухней, мраморным островом и деревянной панелью на потолке',
  'غرفة معيشة ومطبخ مفتوح مُولَّدان بالحاسوب بجزيرة من الرخام ولوح خشبي في السقف',
  'Computergegenereerde woonkamer met open keuken, een marmeren kookeiland en een houten plafondpaneel',
  'Komputerowa wizualizacja salonu z otwartą kuchnią, marmurową wyspą i drewnianym panelem na suficie',
  'Datagenerert stue med åpent kjøkken, en marmoröy og et tretak-panel i taket',
  'Datorgenererat vardagsrum med öppet kök, en marmorö och en träpanel i taket')
a('Computer-generated living and dining room with a long table, a corner sofa and a timber ceiling panel',
  'Salón comedor generado por ordenador con una mesa larga, un sofá rinconero y un panel de madera en el techo',
  'Vue de synthèse d’un séjour avec salle à manger, une longue table, un canapé d’angle et un panneau de bois au plafond',
  'Computergenerierter Wohn- und Essbereich mit einem langen Tisch, einem Ecksofa und einer Holzverkleidung an der Decke',
  'Компьютерная визуализация гостиной-столовой с длинным столом, угловым диваном и деревянной панелью на потолке',
  'غرفة معيشة وطعام مُولَّدة بالحاسوب بطاولة طويلة وأريكة زاوية ولوح خشبي في السقف',
  'Computergegenereerde woon- en eetkamer met een lange tafel, een hoekbank en een houten plafondpaneel',
  'Komputerowa wizualizacja salonu z jadalnią z długim stołem, narożną sofą i drewnianym panelem na suficie',
  'Datagenerert stue og spisestue med et langt bord, en hjørnesofa og et tretak-panel i taket',
  'Datorgenererat vardagsrum med matplats, ett långt bord, en hörnsoffa och en träpanel i taket')
a('Computer-generated bedroom with two single beds, a panelled wall with a concealed light and a glazed door',
  'Dormitorio generado por ordenador con dos camas individuales, una pared de paneles con luz oculta y una puerta acristalada',
  'Vue de synthèse d’une chambre avec deux lits simples, un mur à panneaux avec un éclairage dissimulé et une porte vitrée',
  'Computergeneriertes Schlafzimmer mit zwei Einzelbetten, einer Paneelwand mit verdeckter Beleuchtung und einer verglasten Tür',
  'Компьютерная визуализация спальни с двумя односпальными кроватями, стеной с панелями со скрытой подсветкой и остеклённой дверью',
  'غرفة نوم مُولَّدة بالحاسوب بسريرين مفردين وجدار مكسو بألواح بإضاءة مخفية وباب زجاجي',
  'Computergegenereerde slaapkamer met twee eenpersoonsbedden, een gepaneelde wand met verborgen verlichting en een glazen deur',
  'Komputerowa wizualizacja sypialni z dwoma pojedynczymi łóżkami, ścianą z paneli z ukrytym oświetleniem i przeszklonymi drzwiami',
  'Datagenerert soverom med to enkeltsenger, en panelvegg med skjult belysning og en glassdør',
  'Datorgenererat sovrum med två enkelsängar, en panelvägg med dold belysning och en glasdörr')
a('Computer-generated bathroom with a walk-in shower, a stone basin and two tall mirrors',
  'Baño generado por ordenador con ducha a ras de suelo, un lavabo de piedra y dos espejos altos',
  'Vue de synthèse d’une salle de bains avec une douche à l’italienne, une vasque en pierre et deux grands miroirs',
  'Computergeneriertes Bad mit bodengleicher Dusche, einem Steinwaschbecken und zwei hohen Spiegeln',
  'Компьютерная визуализация ванной комнаты с душем без поддона, раковиной из камня и двумя высокими зеркалами',
  'حمام مُولَّد بالحاسوب بدش مفتوح وحوض من الحجر ومرآتين طويلتين',
  'Computergegenereerde badkamer met een inloopdouche, een stenen wastafel en twee hoge spiegels',
  'Komputerowa wizualizacja łazienki z prysznicem bez brodzika, kamienną umywalką i dwoma wysokimi lustrami',
  'Datagenerert bad med åpen dusj, en servant i stein og to høye speil',
  'Datorgenererat badrum med duschhörna, ett handfat i sten och två höga speglar')
a('Computer-generated top-floor terrace with a private pool, a dining table, sunloungers and a sliding glass door',
  'Terraza de la planta superior generada por ordenador con piscina privada, una mesa de comedor, tumbonas y una puerta corredera de cristal',
  'Vue de synthèse d’une terrasse du dernier étage avec une piscine privée, une table à manger, des bains de soleil et une porte coulissante vitrée',
  'Computergenerierte Terrasse im obersten Geschoss mit privatem Pool, einem Esstisch, Sonnenliegen und einer gläsernen Schiebetür',
  'Компьютерная визуализация террасы на верхнем этаже с частным бассейном, обеденным столом, шезлонгами и стеклянной раздвижной дверью',
  'تراس في الطابق العلوي مُولَّد بالحاسوب بمسبح خاص وطاولة طعام وكراسي تشمّس وباب زجاجي منزلق',
  'Computergegenereerd terras op de bovenste verdieping met een privézwembad, een eettafel, ligbedden en een glazen schuifdeur',
  'Komputerowa wizualizacja tarasu na najwyższej kondygnacji z prywatnym basenem, stołem jadalnianym, leżakami i przeszklonymi drzwiami przesuwnymi',
  'Datagenerert terrasse i øverste etasje med eget basseng, et spisebord, solsenger og en skyvedør i glass',
  'Datorgenererad terrass på översta våningen med egen pool, ett matbord, solsängar och en skjutdörr i glas')
a('A top-floor terrace with a private pool', 'Una terraza de la planta superior con piscina privada',
  'Une terrasse du dernier étage avec piscine privée', 'Eine Terrasse im obersten Geschoss mit privatem Pool',
  'Терраса на верхнем этаже с частным бассейном', 'تراس في الطابق العلوي بمسبح خاص',
  'Een terras op de bovenste verdieping met een privézwembad', 'Taras na najwyższej kondygnacji z prywatnym basenem',
  'En terrasse i øverste etasje med eget basseng', 'En terrass på översta våningen med egen pool')
a('Computer-generated top-floor terrace with a lit private pool, a dining table and sunloungers at dusk',
  'Terraza de la planta superior generada por ordenador con piscina privada iluminada, una mesa de comedor y tumbonas al anochecer',
  'Vue de synthèse d’une terrasse du dernier étage avec une piscine privée éclairée, une table à manger et des bains de soleil au crépuscule',
  'Computergenerierte Terrasse im obersten Geschoss mit beleuchtetem privatem Pool, einem Esstisch und Sonnenliegen in der Dämmerung',
  'Компьютерная визуализация террасы на верхнем этаже с освещённым частным бассейном, обеденным столом и шезлонгами в сумерках',
  'تراس في الطابق العلوي مُولَّد بالحاسوب بمسبح خاص مضاء وطاولة طعام وكراسي تشمّس عند الغسق',
  'Computergegenereerd terras op de bovenste verdieping met een verlicht privézwembad, een eettafel en ligbedden in de schemering',
  'Komputerowa wizualizacja tarasu na najwyższej kondygnacji z podświetlonym prywatnym basenem, stołem jadalnianym i leżakami o zmierzchu',
  'Datagenerert terrasse i øverste etasje med opplyst eget basseng, et spisebord og solsenger i skumringen',
  'Datorgenererad terrass på översta våningen med upplyst egen pool, ett matbord och solsängar i skymningen')
a('The same terrace at dusk', 'La misma terraza al anochecer', 'La même terrasse au crépuscule', 'Dieselbe Terrasse in der Dämmerung',
  'Та же терраса в сумерках', 'التراس نفسه عند الغسق', 'Hetzelfde terras in de schemering', 'Ten sam taras o zmierzchu',
  'Den samme terrassen i skumringen', 'Samma terrass i skymningen')
a('A patio with a private pool', 'Un patio con piscina privada', 'Un patio avec piscine privée', 'Ein Patio mit privatem Pool',
  'Патио с частным бассейном', 'فناء بمسبح خاص', 'Een patio met een privézwembad', 'Patio z prywatnym basenem',
  'Et patio med eget basseng', 'En patio med egen pool')

# ---------------------------------------------------------------- overview
a('Ten homes, <em>six available</em>', 'Diez viviendas, <em>seis disponibles</em>', 'Dix logements, <em>six disponibles</em>',
  'Zehn Wohnungen, <em>sechs verfügbar</em>', 'Десять квартир, <em>шесть в продаже</em>', 'عشرة مساكن، <em>ستة منها متاحة</em>',
  'Tien woningen, <em>zes beschikbaar</em>', 'Dziesięć mieszkań, <em>sześć dostępnych</em>', 'Ti boliger, <em>seks ledige</em>',
  'Tio bostäder, <em>sex lediga</em>')
a('This is a residential building of 10 homes with one, two and three bedrooms, on the ground, first and second floors and a top floor, in the centre of Estepona, next to the old town. Six homes are listed with a price: a one-bedroom and a three-bedroom home on the ground floor, and four on the first floor, one of them with a patio and a private pool. Each has a garage space and a storage room.',
  'Es un edificio residencial de 10 viviendas de uno, dos y tres dormitorios, en planta baja, primera, segunda y planta superior, en el centro de Estepona, junto al casco antiguo. Seis viviendas figuran con precio: una de un dormitorio y una de tres en planta baja, y cuatro en la primera planta, una de ellas con patio y piscina privada. Cada una tiene plaza de garaje y trastero.',
  'Il s’agit d’un immeuble résidentiel de 10 logements d’une, deux et trois chambres, répartis sur le rez-de-chaussée, le premier et le deuxième étage et un étage supérieur, au centre d’Estepona, à côté de la vieille ville. Six logements sont annoncés avec un prix : un d’une chambre et un de trois chambres au rez-de-chaussée, et quatre au premier étage, dont un avec patio et piscine privée. Chacun comprend une place de garage et une cave.',
  'Es ist ein Wohngebäude mit 10 Wohnungen mit einem, zwei und drei Schlafzimmern, verteilt auf Erdgeschoss, erstes und zweites Obergeschoss und ein oberstes Geschoss, im Zentrum von Estepona, direkt an der Altstadt. Sechs Wohnungen sind mit Preis gelistet: je eine mit einem und mit drei Schlafzimmern im Erdgeschoss sowie vier im ersten Obergeschoss, eine davon mit Patio und privatem Pool. Jede hat einen Garagenstellplatz und einen Abstellraum.',
  'Это жилой дом из 10 квартир с одной, двумя и тремя спальнями, расположенных на четырёх этажах: первом, втором, третьем и верхнем. Дом находится в центре Эстепоны, рядом со старым городом. Шесть квартир указаны с ценой: одна с одной спальней и одна с тремя спальнями на первом этаже и четыре на втором, одна из них с патио и частным бассейном. У каждой есть место в гараже и кладовая.',
  'هذا مبنى سكني من 10 مساكن بغرفة وغرفتين وثلاث غرف نوم، موزعة على الطابق الأرضي والأول والثاني وطابق علوي، في وسط إستيبونا بجوار البلدة القديمة. ستة مساكن معروضة بسعر: مسكن بغرفة نوم ومسكن بثلاث غرف نوم في الطابق الأرضي، وأربعة في الطابق الأول، أحدها بفناء ومسبح خاص. ولكل منها موقف في المرآب وغرفة تخزين.',
  'Dit is een woongebouw met 10 woningen met één, twee en drie slaapkamers, verdeeld over de begane grond, de eerste en tweede verdieping en een bovenste verdieping, in het centrum van Estepona, naast de oude stad. Zes woningen staan met een prijs vermeld: een met één slaapkamer en een met drie slaapkamers op de begane grond, en vier op de eerste verdieping, waarvan een met een patio en een privézwembad. Elk heeft een garageplaats en een berging.',
  'To budynek mieszkalny z 10 mieszkaniami z jedną, dwiema i trzema sypialniami, na parterze, pierwszym i drugim piętrze oraz na najwyższej kondygnacji, w centrum Estepony, obok starego miasta. Sześć mieszkań ma podaną cenę: jedno z jedną sypialnią i jedno z trzema na parterze oraz cztery na pierwszym piętrze, jedno z nich z patio i prywatnym basenem. Każde ma miejsce garażowe i komórkę lokatorską.',
  'Dette er et boligbygg med 10 boliger med ett, to og tre soverom, fordelt på første, andre og tredje etasje og en øverste etasje, i sentrum av Estepona, ved siden av gamlebyen. Seks boliger er annonsert med pris: én med ett soverom og én med tre soverom i første etasje, og fire i andre etasje, én av dem med patio og eget basseng. Hver har garasjeplass og bod.',
  'Det här är ett bostadshus med 10 bostäder med ett, två och tre sovrum, fördelade på bottenvåningen, första och andra våningen samt en översta våning, i centrala Estepona, intill gamla stan. Sex bostäder är listade med pris: en med ett sovrum och en med tre sovrum på bottenvåningen, och fyra på första våningen, en av dem med patio och egen pool. Var och en har en garageplats och ett förråd.')
a('The building has a lift and a car lift down to the garage. The four other homes, on the second floor and the top floor, are marked reserved on the developer’s price list. The developer’s documents give no delivery date.',
  'El edificio tiene ascensor y un ascensor para coches hasta el garaje. Las otras cuatro viviendas, en la segunda planta y en la planta superior, figuran como reservadas en la lista de precios del promotor. Los documentos del promotor no dan fecha de entrega.',
  'L’immeuble dispose d’un ascenseur et d’un monte-voitures jusqu’au garage. Les quatre autres logements, au deuxième étage et à l’étage supérieur, sont indiqués comme réservés dans la liste de prix du promoteur. Les documents du promoteur ne donnent aucune date de livraison.',
  'Das Gebäude hat einen Aufzug und einen Autoaufzug hinunter zur Garage. Die vier übrigen Wohnungen im zweiten Obergeschoss und im obersten Geschoss sind in der Preisliste des Bauträgers als reserviert gekennzeichnet. Die Unterlagen des Bauträgers nennen keinen Übergabetermin.',
  'В доме есть лифт и автомобильный лифт в гараж. Остальные четыре квартиры, на третьем и верхнем этажах, отмечены в прайс-листе застройщика как забронированные. В документах застройщика срок сдачи не указан.',
  'في المبنى مصعد ومصعد للسيارات يصل إلى المرآب. أما المساكن الأربعة الأخرى، في الطابق الثاني والطابق العلوي، فمُدرجة في قائمة أسعار المطوّر على أنها محجوزة. ولا تذكر وثائق المطوّر موعد تسليم.',
  'Het gebouw heeft een lift en een autolift naar de garage. De vier andere woningen, op de tweede en de bovenste verdieping, staan in de prijslijst van de ontwikkelaar als gereserveerd aangemerkt. De documenten van de ontwikkelaar geven geen opleveringsdatum.',
  'W budynku jest winda oraz winda samochodowa do garażu. Pozostałe cztery mieszkania, na drugim piętrze i na najwyższej kondygnacji, są w cenniku dewelopera oznaczone jako zarezerwowane. Dokumenty dewelopera nie podają terminu oddania.',
  'Bygget har heis og en bilheis ned til garasjen. De fire andre boligene, i tredje og øverste etasje, er markert som reservert i utbyggerens prisliste. Utbyggerens dokumenter oppgir ingen overleveringsdato.',
  'Byggnaden har hiss och en bilhiss ner till garaget. De fyra övriga bostäderna, på andra våningen och översta våningen, är markerade som reserverade i exploatörens prislista. Exploatörens dokument anger inget tillträdesdatum.')
a('Terraces, a patio and private pools, by home type', 'Terrazas, un patio y piscinas privadas, según el tipo de vivienda',
  'Terrasses, un patio et des piscines privées, selon le type de logement', 'Terrassen, ein Patio und private Pools, je nach Wohnungstyp',
  'Террасы, патио и частные бассейны — в зависимости от типа квартиры', 'تراسات وفناء ومسابح خاصة، بحسب نوع المسكن',
  'Terrassen, een patio en privézwembaden, afhankelijk van het woningtype', 'Tarasy, patio i prywatne baseny, zależnie od typu mieszkania',
  'Terrasser, et patio og egne basseng, avhengig av boligtype', 'Terrasser, en patio och egna pooler, beroende på bostadstyp')

# ---------------------------------------------------------------- why
a('Ten homes in a building beside the old town, with a garage space and a storage room for each.',
  'Diez viviendas en un edificio junto al casco antiguo, con plaza de garaje y trastero para cada una.',
  'Dix logements dans un immeuble à côté de la vieille ville, avec une place de garage et une cave pour chacun.',
  'Zehn Wohnungen in einem Gebäude neben der Altstadt, jeweils mit Garagenstellplatz und Abstellraum.',
  'Десять квартир в доме рядом со старым городом, у каждой — место в гараже и кладовая.',
  'عشرة مساكن في مبنى بجوار البلدة القديمة، لكل منها موقف في المرآب وغرفة تخزين.',
  'Tien woningen in een gebouw naast de oude stad, elk met een garageplaats en een berging.',
  'Dziesięć mieszkań w budynku obok starego miasta, każde z miejscem garażowym i komórką lokatorską.',
  'Ti boliger i et bygg ved siden av gamlebyen, hver med garasjeplass og bod.',
  'Tio bostäder i en byggnad intill gamla stan, var och en med garageplats och förråd.')
a('Buyers who want a new home in the centre of Estepona, beside the old town, in a building of only ten homes, to live in or as a second home.',
  'Compradores que quieren una vivienda nueva en el centro de Estepona, junto al casco antiguo, en un edificio de solo diez viviendas, para vivir o como segunda residencia.',
  'Acheteurs qui veulent un logement neuf au centre d’Estepona, à côté de la vieille ville, dans un immeuble de dix logements seulement, pour y vivre ou comme résidence secondaire.',
  'Käufer, die eine neue Wohnung im Zentrum von Estepona suchen, direkt an der Altstadt, in einem Gebäude mit nur zehn Wohnungen, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которые хотят новую квартиру в центре Эстепоны, рядом со старым городом, в доме всего из десяти квартир, для постоянного проживания или как вторую недвижимость.',
  'مشترون يريدون مسكنًا جديدًا في وسط إستيبونا بجوار البلدة القديمة، في مبنى من عشرة مساكن فقط، للسكن فيه أو كمنزل ثانٍ.',
  'Kopers die een nieuwe woning willen in het centrum van Estepona, naast de oude stad, in een gebouw met slechts tien woningen, om in te wonen of als tweede woning.',
  'Kupujący, którzy szukają nowego mieszkania w centrum Estepony, obok starego miasta, w budynku z zaledwie dziesięcioma mieszkaniami, do zamieszkania lub jako drugi dom.',
  'Kjøpere som vil ha en ny bolig i sentrum av Estepona, ved siden av gamlebyen, i et bygg med bare ti boliger, til å bo i eller som feriebolig.',
  'Köpare som vill ha en ny bostad i centrala Estepona, intill gamla stan, i en byggnad med bara tio bostäder, att bo i eller som andra bostad.')
a('A garage space reached by a car lift and a storage room with every home, and a private pool on some of them.',
  'Una plaza de garaje a la que se llega con un ascensor para coches y un trastero con cada vivienda, y piscina privada en algunas de ellas.',
  'Une place de garage desservie par un monte-voitures et une cave avec chaque logement, et une piscine privée pour certains.',
  'Ein Garagenstellplatz, den ein Autoaufzug erreicht, und ein Abstellraum zu jeder Wohnung, bei einigen dazu ein privater Pool.',
  'У каждой квартиры есть место в гараже, куда ведёт автомобильный лифт, и кладовая, а у некоторых — частный бассейн.',
  'موقف في المرآب يصل إليه مصعد السيارات وغرفة تخزين مع كل مسكن، ومسبح خاص في بعضها.',
  'Een garageplaats die met een autolift bereikbaar is en een berging bij elke woning, en bij sommige een privézwembad.',
  'Miejsce garażowe, do którego prowadzi winda samochodowa, i komórka lokatorska przy każdym mieszkaniu, a w niektórych prywatny basen.',
  'En garasjeplass som nås med bilheis og en bod til hver bolig, og eget basseng i noen av dem.',
  'En garageplats som nås med bilhiss och ett förråd till varje bostad, och egen pool i några av dem.')
a('The developer’s dossier puts the building next to the old town, with shops, supermarkets, schools and sports facilities around it, and the marina 3 minutes away on its map.',
  'El dosier del promotor sitúa el edificio junto al casco antiguo, rodeado de comercios, supermercados, colegios e instalaciones deportivas, y el puerto deportivo a 3 minutos en su mapa.',
  'Le dossier du promoteur situe l’immeuble à côté de la vieille ville, entouré de commerces, de supermarchés, d’écoles et d’équipements sportifs, avec le port de plaisance à 3 minutes sur sa carte.',
  'Das Dossier des Bauträgers verortet das Gebäude neben der Altstadt, umgeben von Geschäften, Supermärkten, Schulen und Sportanlagen, mit dem Yachthafen auf seiner Karte 3 Minuten entfernt.',
  'В досье застройщика дом расположен рядом со старым городом, вокруг — магазины, супермаркеты, школы и спортивные объекты, а до порта на карте 3 минуты.',
  'يضع ملف المطوّر المبنى بجوار البلدة القديمة، تحيط به المتاجر والأسواق والمدارس والمرافق الرياضية، ويبعد المرسى 3 دقائق على خريطته.',
  'Het dossier van de ontwikkelaar plaatst het gebouw naast de oude stad, omgeven door winkels, supermarkten, scholen en sportvoorzieningen, met de jachthaven op 3 minuten op zijn kaart.',
  'Dossier dewelopera umieszcza budynek obok starego miasta, w otoczeniu sklepów, supermarketów, szkół i obiektów sportowych, a port jachtowy na swojej mapie w odległości 3 minut.',
  'Utbyggerens dossier plasserer bygget ved siden av gamlebyen, med butikker, supermarkeder, skoler og idrettsanlegg rundt, og småbåthavnen 3 minutter unna på kartet.',
  'Exploatörens dossier placerar byggnaden intill gamla stan, med butiker, stormarknader, skolor och idrottsanläggningar runt omkring, och småbåtshamnen 3 minuter bort på kartan.')
a('No document gives a delivery date or the stage of the building, so we ask for the contractual date and the licence before any reservation.',
  'Ningún documento da una fecha de entrega ni el estado del edificio, por lo que pedimos la fecha contractual y la licencia antes de cualquier reserva.',
  'Aucun document ne donne de date de livraison ni l’état d’avancement de l’immeuble ; nous demandons donc la date contractuelle et le permis avant toute réservation.',
  'Kein Dokument nennt einen Übergabetermin oder den Stand des Gebäudes; wir fragen daher vor jeder Reservierung das vertragliche Datum und die Genehmigung an.',
  'Ни в одном документе нет срока сдачи и сведений о стадии строительства здания, поэтому до любого бронирования мы запрашиваем договорную дату и разрешение.',
  'لا توجد وثيقة تذكر موعد تسليم أو مرحلة المبنى، لذلك نطلب التاريخ التعاقدي والرخصة قبل أي حجز.',
  'Geen enkel document noemt een opleveringsdatum of de stand van het gebouw; daarom vragen wij vóór elke reservering de contractuele datum en de vergunning op.',
  'Żaden dokument nie podaje terminu oddania ani etapu budowy, dlatego przed każdą rezerwacją prosimy o termin umowny i pozwolenie.',
  'Ingen dokumenter oppgir en overleveringsdato eller hvor langt bygget har kommet, så vi ber om den kontraktsfestede datoen og tillatelsen før enhver reservasjon.',
  'Inget dokument anger ett tillträdesdatum eller hur långt byggnaden har kommit, så vi ber om det avtalade datumet och bygglovet före varje reservation.')

# ---------------------------------------------------------------- architecture
a('White walls, <em>clay roofs</em> and green shutters', 'Paredes blancas, <em>tejados de teja</em> y contraventanas verdes',
  'Murs blancs, <em>toits de tuiles</em> et volets verts', 'Weiße Wände, <em>Ziegeldächer</em> und grüne Fensterläden',
  'Белые стены, <em>черепичные крыши</em> и зелёные ставни', 'جدران بيضاء، <em>وأسقف من القرميد</em> ومصاريع خضراء',
  'Witte muren, <em>pannendaken</em> en groene luiken', 'Białe ściany, <em>dachy z dachówki</em> i zielone okiennice',
  'Hvite vegger, <em>teglsteinstak</em> og grønne skodder', 'Vita väggar, <em>tegeltak</em> och gröna fönsterluckor')
a('The developer’s dossier describes a building that combines classical elements with contemporary design, with generous rooms, on a ground floor, a first and a second floor and a top floor.',
  'El dosier del promotor describe un edificio que combina elementos clásicos con diseño contemporáneo, con estancias amplias, en planta baja, primera, segunda y planta superior.',
  'Le dossier du promoteur décrit un immeuble qui associe des éléments classiques à un design contemporain, avec des pièces spacieuses, réparti sur un rez-de-chaussée, un premier étage, un deuxième étage et un étage supérieur.',
  'Das Dossier des Bauträgers beschreibt ein Gebäude, das klassische Elemente mit zeitgenössischem Design verbindet, mit großzügigen Räumen, auf Erdgeschoss, erstem und zweitem Obergeschoss und einem obersten Geschoss.',
  'В досье застройщика описано здание, сочетающее классические элементы с современным дизайном и просторными помещениями, на первом, втором, третьем и верхнем этажах.',
  'يصف ملف المطوّر مبنى يجمع بين عناصر كلاسيكية وتصميم معاصر، بغرف رحبة، موزعًا على الطابق الأرضي والطابقين الأول والثاني وطابق علوي.',
  'Het dossier van de ontwikkelaar beschrijft een gebouw dat klassieke elementen combineert met eigentijds design, met ruime vertrekken, op een begane grond, een eerste en een tweede verdieping en een bovenste verdieping.',
  'Dossier dewelopera opisuje budynek łączący elementy klasyczne ze współczesnym designem, z przestronnymi pomieszczeniami, na parterze, pierwszym i drugim piętrze oraz na najwyższej kondygnacji.',
  'Utbyggerens dossier beskriver et bygg som kombinerer klassiske elementer med moderne design, med romslige rom, fordelt på første, andre og tredje etasje og en øverste etasje.',
  'Exploatörens dossier beskriver en byggnad som förenar klassiska element med modern design, med rymliga rum, fördelad på bottenvåning, första och andra våningen och en översta våning.')
a('In the images the building has white walls, clay-tile roofs, balconies with dark railings and sage-green shutters, and the upper homes have terraces with private pools set between the roofs.',
  'En las imágenes, el edificio tiene paredes blancas, tejados de teja, balcones con barandillas oscuras y contraventanas verde salvia, y las viviendas superiores tienen terrazas con piscinas privadas entre los tejados.',
  'Sur les images, l’immeuble a des murs blancs, des toits de tuiles, des balcons à garde-corps sombres et des volets vert sauge, et les logements supérieurs ont des terrasses avec des piscines privées entre les toits.',
  'In den Bildern hat das Gebäude weiße Wände, Ziegeldächer, Balkone mit dunklen Geländern und salbeigrüne Fensterläden, und die oberen Wohnungen haben Terrassen mit privaten Pools zwischen den Dächern.',
  'На изображениях у здания белые стены, черепичные крыши, балконы с тёмными ограждениями и шалфейно-зелёные ставни, а у верхних квартир — террасы с частными бассейнами между крышами.',
  'تظهر في الصور جدران بيضاء وأسقف من القرميد وشرفات بحواجز داكنة ومصاريع بلون أخضر مريمي، وللمساكن العليا تراسات بمسابح خاصة بين الأسقف.',
  'Op de beelden heeft het gebouw witte muren, pannendaken, balkons met donkere hekken en saliegroene luiken, en de bovenste woningen hebben terrassen met privézwembaden tussen de daken.',
  'Na wizualizacjach budynek ma białe ściany, dachy z dachówki, balkony z ciemnymi balustradami i szałwiowozielone okiennice, a górne mieszkania mają tarasy z prywatnymi basenami między dachami.',
  'På bildene har bygget hvite vegger, teglsteinstak, balkonger med mørke rekkverk og salvegrønne skodder, og de øvre boligene har terrasser med egne basseng mellom takene.',
  'På bilderna har byggnaden vita väggar, tegeltak, balkonger med mörka räcken och salviagröna fönsterluckor, och de övre bostäderna har terrasser med egna pooler mellan taken.')
a('Half-brick ceramic masonry, rendered, with a backing wall of double hollow brick and insulation sprayed into the cavity, and a lime-based mortar finish between the windows.',
  'Fábrica de ladrillo cerámico de medio pie, revocada, trasdosada con ladrillo hueco doble y con aislamiento proyectado en las cámaras, y acabado de mortero de base cal entre los huecos de ventana.',
  'Maçonnerie de brique céramique d’une demi-brique, enduite, avec un mur de doublage en brique creuse double et une isolation projetée dans les lames d’air, et une finition en mortier à base de chaux entre les fenêtres.',
  'Halbsteiniges Ziegelmauerwerk aus Keramikziegeln, verputzt, mit einer Vorsatzschale aus doppeltem Hochlochziegel und in die Hohlräume gespritzter Dämmung sowie einem Kalkmörtelputz zwischen den Fenstern.',
  'Кладка из керамического кирпича в полкирпича, оштукатуренная, с внутренней стенкой из двойного пустотелого кирпича и утеплителем, напылённым в полости, и известковой штукатуркой между окнами.',
  'بناء بالطوب الخزفي بسماكة نصف طوبة، مكسو بالملاط، مع جدار تبطين من الطوب المجوّف المزدوج وعزل مرشوش في الفراغات، وطلاء بملاط أساسه الجير بين النوافذ.',
  'Keramisch metselwerk van een halve steen, gepleisterd, met een achterwand van dubbele holle baksteen en in de spouwen gespoten isolatie, en een afwerking van kalkmortel tussen de ramen.',
  'Mur z cegły ceramicznej o grubości pół cegły, otynkowany, z wewnętrzną ścianą z podwójnej cegły dziurawki i izolacją natryskiwaną w szczelinach oraz wykończeniem z zaprawy wapiennej między oknami.',
  'Teglmurverk av keramisk murstein i halv stein, pusset, med en bakvegg av dobbel hulltegl og isolasjon sprøytet inn i hulrommene, og en kalkbasert mørtelfinish mellom vinduene.',
  'Murverk av keramiskt tegel i halv sten, putsat, med en bakvägg av dubbelt hålsten och isolering insprutad i hålrummen, och en kalkbaserad murbruksfasad mellan fönstren.')
a('Aluminium frames with a wood-effect finish and a thermal break, with double glazing and an air chamber.',
  'Carpintería de aluminio con acabado imitación madera y rotura de puente térmico, con doble acristalamiento y cámara de aire.',
  'Menuiseries en aluminium à finition effet bois et rupture de pont thermique, avec double vitrage et lame d’air.',
  'Aluminiumrahmen mit Holzoptik und thermischer Trennung, mit Doppelverglasung und Luftkammer.',
  'Алюминиевые рамы с отделкой под дерево и терморазрывом, с двойным остеклением и воздушной камерой.',
  'إطارات من الألمنيوم بتشطيب بمظهر الخشب وفاصل حراري، بزجاج مزدوج وحجرة هواء.',
  'Aluminium kozijnen met een houtlookafwerking en een thermische onderbreking, met dubbele beglazing en een luchtkamer.',
  'Stolarka aluminiowa z wykończeniem imitującym drewno i przerwą termiczną, z podwójnym szkleniem i komorą powietrzną.',
  'Aluminiumsrammer med trelignende finish og termisk brudd, med dobbeltglass og luftkammer.',
  'Aluminiumkarmar i träutförande med termiskt brott, med dubbelglas och luftspalt.')
a('Lift and garage', 'Ascensor y garaje', 'Ascenseur et garage', 'Aufzug und Garage', 'Лифт и гараж', 'المصعد والمرآب',
  'Lift en garage', 'Winda i garaż', 'Heis og garasje', 'Hiss och garage')
a('A lift for four people that stops at the garage, and a car lift at the garage entrance.',
  'Un ascensor para cuatro personas que para en el garaje, y un ascensor para coches en la entrada del garaje.',
  'Un ascenseur pour quatre personnes qui dessert le garage, et un monte-voitures à l’entrée du garage.',
  'Ein Aufzug für vier Personen, der bis zur Garage fährt, und ein Autoaufzug an der Garageneinfahrt.',
  'Лифт на четыре человека с остановкой в гараже и автомобильный лифт у въезда в гараж.',
  'مصعد يتسع لأربعة أشخاص ويتوقف عند المرآب، ومصعد للسيارات عند مدخل المرآب.',
  'Een lift voor vier personen die tot in de garage rijdt, en een autolift bij de ingang van de garage.',
  'Winda na cztery osoby zatrzymująca się w garażu oraz winda samochodowa przy wjeździe do garażu.',
  'En heis for fire personer som stopper i garasjen, og en bilheis ved garasjeinngangen.',
  'En hiss för fyra personer som stannar i garaget, och en bilhiss vid garageinfarten.')
a('Aerothermal hot water in every home and, according to the dossier, a solar energy system and a high energy rating.',
  'Agua caliente con aerotermia en cada vivienda y, según el dosier, un sistema de energía solar y una alta calificación energética.',
  'Eau chaude par aérothermie dans chaque logement et, selon le dossier, un système d’énergie solaire et une haute performance énergétique.',
  'Warmwasser über Luft-Wasser-Wärmepumpe in jeder Wohnung und laut Dossier eine Solaranlage und eine hohe Energieeffizienzklasse.',
  'Горячая вода от аэротермической системы в каждой квартире и, по данным досье, система солнечной энергии и высокий энергетический класс.',
  'ماء ساخن بنظام حراري هوائي في كل مسكن، وبحسب الملف نظام للطاقة الشمسية وتصنيف طاقة مرتفع.',
  'Warm water via aerothermie in elke woning en volgens het dossier een zonne-energiesysteem en een hoge energieclassificatie.',
  'Ciepła woda z systemu aerotermicznego w każdym mieszkaniu oraz, według dossier, system energii słonecznej i wysoka klasa energetyczna.',
  'Varmtvann fra aerotermisk system i hver bolig og, ifølge dossieret, et solenergianlegg og en høy energiklasse.',
  'Varmvatten från aerotermiskt system i varje bostad och, enligt dossiern, ett solenergisystem och ett högt energibetyg.')

# ---------------------------------------------------------------- quality specification
a('Source: the specification in the developer’s dossier, which is undated. It says that the materials may be changed by the project management if their quality is not reduced, that the images are illustrative and that the furniture shown is not included. For the interior flooring the Spanish text says “tarima de madera de 1.ª calidad” (first-quality timber flooring) and the English text of the same specification says “wood laminate flooring”; we ask which is used.',
  'Fuente: la memoria de calidades del dosier del promotor, que no lleva fecha. Indica que la dirección facultativa puede cambiar los materiales si su calidad no disminuye, que las imágenes son ilustrativas y que el mobiliario mostrado no está incluido. Para el suelo interior, el texto en español dice «tarima de madera de 1.ª calidad» y el texto en inglés de la misma memoria dice «wood laminate flooring» (suelo laminado de madera); preguntamos cuál se utiliza.',
  'Source : le descriptif de qualité du dossier du promoteur, qui n’est pas daté. Il précise que les matériaux peuvent être modifiés par la direction de projet si leur qualité n’est pas réduite, que les images sont illustratives et que le mobilier présenté n’est pas inclus. Pour le revêtement de sol intérieur, le texte espagnol indique « tarima de madera de 1.ª calidad » (parquet en bois de première qualité) et le texte anglais du même descriptif indique « wood laminate flooring » (sol stratifié effet bois) ; nous demandons lequel est utilisé.',
  'Quelle: die Baubeschreibung im Dossier des Bauträgers, die kein Datum trägt. Sie weist darauf hin, dass die Bauleitung die Materialien ändern kann, sofern ihre Qualität nicht gemindert wird, dass die Bilder der Veranschaulichung dienen und dass die gezeigten Möbel nicht enthalten sind. Für den Bodenbelag im Innenraum nennt der spanische Text „tarima de madera de 1.ª calidad“ (Holzdielenboden erster Qualität), der englische Text derselben Beschreibung „wood laminate flooring“ (Laminatboden in Holzoptik); wir fragen nach, welcher verwendet wird.',
  'Источник: спецификация качества в досье застройщика, которая не датирована. В ней сказано, что руководство проекта может менять материалы, если их качество не снижается, что изображения носят иллюстративный характер и что показанная мебель не входит в стоимость. Для напольного покрытия внутри квартир испанский текст указывает «tarima de madera de 1.ª calidad» (деревянное напольное покрытие первого сорта), а английский текст той же спецификации — «wood laminate flooring» (ламинат под дерево); мы уточняем, что именно применяется.',
  'المصدر: مواصفات الجودة في ملف المطوّر، وهي غير مؤرخة. وتذكر أن إدارة المشروع قد تغيّر المواد ما دامت جودتها لا تنخفض، وأن الصور للتوضيح، وأن الأثاث الظاهر غير مشمول. وبالنسبة لأرضيات الداخل، يذكر النص الإسباني «tarima de madera de 1.ª calidad» (أرضية خشبية من الدرجة الأولى) بينما يذكر النص الإنجليزي من المواصفات نفسها «wood laminate flooring» (أرضية لامينات بمظهر الخشب)؛ ونستفسر عن الأرضية المستخدمة.',
  'Bron: de specificatie in het dossier van de ontwikkelaar, die niet is gedateerd. Daarin staat dat de bouwleiding de materialen mag wijzigen zolang de kwaliteit niet afneemt, dat de beelden illustratief zijn en dat de getoonde meubels niet zijn inbegrepen. Voor de vloer binnen noemt de Spaanse tekst “tarima de madera de 1.ª calidad” (houten vloer van eerste kwaliteit) en de Engelse tekst van dezelfde specificatie “wood laminate flooring” (laminaat in houtlook); wij vragen na welke wordt gebruikt.',
  'Źródło: specyfikacja w dossier dewelopera, która nie jest datowana. Podano w niej, że kierownictwo projektu może zmieniać materiały, o ile ich jakość nie ulegnie obniżeniu, że wizualizacje mają charakter poglądowy i że pokazane meble nie są wliczone w cenę. W przypadku podłóg wewnątrz hiszpański tekst podaje „tarima de madera de 1.ª calidad” (podłoga drewniana pierwszej jakości), a angielski tekst tej samej specyfikacji „wood laminate flooring” (laminat drewnopodobny); pytamy, który z nich zostanie zastosowany.',
  'Kilde: spesifikasjonen i utbyggerens dossier, som ikke er datert. Den sier at prosjektledelsen kan endre materialene så lenge kvaliteten ikke reduseres, at bildene er illustrative og at møblene som vises ikke er inkludert. For gulvet innvendig oppgir den spanske teksten «tarima de madera de 1.ª calidad» (tregulv av første kvalitet), mens den engelske teksten i samme spesifikasjon oppgir «wood laminate flooring» (laminatgulv med trelook); vi spør hvilket som brukes.',
  'Källa: beskrivningen i exploatörens dossier, som inte är daterad. Den anger att projektledningen får ändra materialen så länge kvaliteten inte sänks, att bilderna är illustrativa och att de möbler som visas inte ingår. För golvet inomhus anger den spanska texten ”tarima de madera de 1.ª calidad” (trägolv av första klass) medan den engelska texten i samma beskrivning anger ”wood laminate flooring” (laminatgolv med trämönster); vi frågar vilket som används.')
a('Rendered half-brick ceramic masonry on the facades, backed by double hollow brick with insulation sprayed into the cavity, and a lime-based mortar finish between the windows.',
  'Fachadas de fábrica de ladrillo cerámico de medio pie revocada, trasdosada con ladrillo hueco doble y aislamiento proyectado en las cámaras, con acabado de mortero de base cal entre los huecos de ventana.',
  'Façades en maçonnerie de brique céramique d’une demi-brique enduite, doublée de brique creuse double avec isolation projetée dans les lames d’air, et finition en mortier à base de chaux entre les fenêtres.',
  'Fassaden aus verputztem halbsteinigem Keramikziegelmauerwerk, mit Vorsatzschale aus doppeltem Hochlochziegel und in die Hohlräume gespritzter Dämmung, mit Kalkmörtelputz zwischen den Fenstern.',
  'Фасады из оштукатуренной кладки из керамического кирпича в полкирпича с внутренней стенкой из двойного пустотелого кирпича и утеплителем, напылённым в полости, с известковой штукатуркой между окнами.',
  'واجهات من بناء بالطوب الخزفي بسماكة نصف طوبة مكسوّ بالملاط، مع تبطين بالطوب المجوّف المزدوج وعزل مرشوش في الفراغات، وملاط أساسه الجير بين النوافذ.',
  'Gevels van gepleisterd keramisch metselwerk van een halve steen, met een achterwand van dubbele holle baksteen en in de spouwen gespoten isolatie, en een afwerking van kalkmortel tussen de ramen.',
  'Elewacje z otynkowanego muru z cegły ceramicznej o grubości pół cegły, z wewnętrzną ścianą z podwójnej cegły dziurawki i izolacją natryskiwaną w szczelinach oraz wykończeniem z zaprawy wapiennej między oknami.',
  'Fasader av pusset keramisk teglmurverk i halv stein, med en bakvegg av dobbel hulltegl og isolasjon sprøytet inn i hulrommene, og en kalkbasert mørtelfinish mellom vinduene.',
  'Fasader av putsat keramiskt tegelmurverk i halv sten, med en bakvägg av dubbelt hålsten och isolering insprutad i hålrummen, och en kalkbaserad murbruksfasad mellan fönstren.')
a('Partitions inside the home in plasterboard with thermal and acoustic insulation, and between homes in ceramic brick with sprayed insulation.',
  'Tabiquería interior de la vivienda en yeso laminado con aislamiento térmico y acústico, y separación entre viviendas en ladrillo cerámico con aislamiento proyectado.',
  'Cloisons intérieures du logement en plaques de plâtre avec isolation thermique et acoustique, et séparation entre logements en brique céramique avec isolation projetée.',
  'Trennwände innerhalb der Wohnung aus Gipskarton mit Wärme- und Schalldämmung, zwischen den Wohnungen aus Keramikziegeln mit aufgespritzter Dämmung.',
  'Перегородки внутри квартиры из гипсокартона с тепло- и звукоизоляцией, а между квартирами — из керамического кирпича с напылённым утеплителем.',
  'فواصل داخلية في المسكن من ألواح الجبس بعزل حراري وصوتي، وفاصل بين المساكن من الطوب الخزفي بعزل مرشوش.',
  'Scheidingswanden binnen de woning van gipsplaat met thermische en akoestische isolatie, en tussen woningen van keramische baksteen met gespoten isolatie.',
  'Przegrody wewnątrz mieszkania z płyt gipsowo-kartonowych z izolacją cieplną i akustyczną, a między mieszkaniami z cegły ceramicznej z izolacją natryskiwaną.',
  'Skillevegger inne i boligen i gipsplater med varme- og lydisolasjon, og mellom boligene i keramisk tegl med sprøytet isolasjon.',
  'Mellanväggar inne i bostaden av gipsskivor med värme- och ljudisolering, och mellan bostäderna av keramiskt tegel med insprutad isolering.')
a('Aluminium windows with a wood-effect finish and a thermal break, in a colour the project management chooses, with double glazing and an air chamber.',
  'Ventanas de aluminio con acabado imitación madera y rotura de puente térmico, de un color que elige la dirección facultativa, con doble acristalamiento y cámara de aire.',
  'Fenêtres en aluminium à finition effet bois et rupture de pont thermique, dans une teinte choisie par la direction de projet, avec double vitrage et lame d’air.',
  'Aluminiumfenster mit Holzoptik und thermischer Trennung, in einer von der Bauleitung gewählten Farbe, mit Doppelverglasung und Luftkammer.',
  'Алюминиевые окна с отделкой под дерево и терморазрывом, цвет которых выбирает руководство проекта, с двойным остеклением и воздушной камерой.',
  'نوافذ من الألمنيوم بتشطيب بمظهر الخشب وفاصل حراري، بلون تختاره إدارة المشروع، بزجاج مزدوج وحجرة هواء.',
  'Aluminium ramen met een houtlookafwerking en een thermische onderbreking, in een kleur die de bouwleiding kiest, met dubbele beglazing en een luchtkamer.',
  'Okna aluminiowe z wykończeniem imitującym drewno i przerwą termiczną, w kolorze wybranym przez kierownictwo projektu, z podwójnym szkleniem i komorą powietrzną.',
  'Aluminiumsvinduer med trelignende finish og termisk brudd, i en farge prosjektledelsen velger, med dobbeltglass og luftkammer.',
  'Aluminiumfönster i träutförande med termiskt brott, i en färg som projektledningen väljer, med dubbelglas och luftspalt.')
a('An armoured front door panelled on the inside to match the interior doors, with a security lock and anti-lever bolts, smooth interior doors in solid wood or similar, and built-in modular wardrobes lacquered white and lined with melamine, with a luggage shelf and a hanging rail.',
  'Puerta de entrada blindada, panelada por dentro a juego con las puertas interiores, con cerradura de seguridad y pernos antipalanca, puertas interiores lisas de madera maciza o similar, y armarios modulares empotrados lacados en blanco y forrados de melamina por dentro, con balda maletero y barra de colgar.',
  'Porte d’entrée blindée, habillée à l’intérieur en harmonie avec les portes intérieures, avec serrure de sécurité et pênes anti-effraction, portes intérieures lisses en bois massif ou équivalent, et placards modulaires intégrés laqués blanc et doublés de mélaminé à l’intérieur, avec étagère à valises et barre de penderie.',
  'Gepanzerte Wohnungseingangstür, innen passend zu den Innentüren verkleidet, mit Sicherheitsschloss und Aufhebelschutzbolzen, glatte Innentüren aus Massivholz oder gleichwertig sowie modulare Einbauschränke, weiß lackiert und innen mit Melamin ausgekleidet, mit Kofferablage und Kleiderstange.',
  'Бронированная входная дверь с внутренней панелью в тон межкомнатным дверям, с замком безопасности и противовзломными штифтами, гладкие межкомнатные двери из массива дерева или аналогичные, а также встроенные модульные шкафы с белым лаковым покрытием и меламиновой отделкой внутри, с полкой для чемоданов и штангой для одежды.',
  'باب دخول مصفّح مكسو من الداخل بألواح تتناسق مع الأبواب الداخلية، بقفل أمان وأوتاد مضادة للخلع، وأبواب داخلية ملساء من الخشب الصلب أو ما يماثله، وخزائن مدمجة نمطية مطلية بالورنيش الأبيض ومبطنة من الداخل بالميلامين، مع رف للحقائب وعمود تعليق.',
  'Een gepantserde voordeur, aan de binnenkant gepaneeld passend bij de binnendeuren, met een veiligheidsslot en pinnen tegen breken met een koevoet, gladde binnendeuren van massief hout of gelijkwaardig, en modulaire inbouwkasten, wit gelakt en aan de binnenkant bekleed met melamine, met een koffertablet en een kledingstang.',
  'Drzwi wejściowe antywłamaniowe z wewnętrznym panelem dopasowanym do drzwi wewnętrznych, z zamkiem zabezpieczającym i bolcami przeciw podważeniu, gładkie drzwi wewnętrzne z litego drewna lub podobne oraz modułowe szafy w zabudowie, lakierowane na biało i wyłożone w środku melaminą, z półką na walizki i drążkiem na ubrania.',
  'Pansret inngangsdør, panelt innvendig for å matche innerdørene, med sikkerhetslås og bolter mot oppbrekking, glatte innerdører i massivt tre eller tilsvarende, og modulære innebygde garderobeskap, hvitlakkerte og kledd med melamin innvendig, med kofferthylle og kleshengerstang.',
  'Pansrad ytterdörr, panelad på insidan i samma stil som innerdörrarna, med säkerhetslås och bultar mot påbrytning, släta innerdörrar i massivt trä eller likvärdigt, samt modulära inbyggda garderober, vitlackerade och invändigt klädda med melamin, med en resväskehylla och en klädstång.')
a('Floors and finishes', 'Suelos y acabados', 'Sols et finitions', 'Böden und Oberflächen', 'Полы и отделка', 'الأرضيات والتشطيبات',
  'Vloeren en afwerking', 'Podłogi i wykończenia', 'Gulv og overflater', 'Golv och ytskikt')
a('First-quality wood flooring inside the homes, non-slip porcelain stoneware on the terraces and first-quality porcelain tiling in the bathrooms.',
  'Suelo de tarima de madera de primera calidad en el interior de las viviendas, gres porcelánico antideslizante en las terrazas y alicatado porcelánico de primera calidad en los baños.',
  'Sol en bois de première qualité à l’intérieur des logements, grès cérame antidérapant sur les terrasses et carrelage en grès porcelainé de première qualité dans les salles de bains.',
  'Holzboden erster Qualität im Inneren der Wohnungen, rutschhemmendes Feinsteinzeug auf den Terrassen und Feinsteinzeugfliesen erster Qualität in den Bädern.',
  'Деревянное напольное покрытие первого сорта внутри квартир, нескользящий керамогранит на террасах и керамогранитная плитка первого сорта в ванных комнатах.',
  'أرضية خشبية من الدرجة الأولى داخل المساكن، وبورسلان مانع للانزلاق على التراسات، وبلاط بورسلان من الدرجة الأولى في الحمامات.',
  'Houten vloer van eerste kwaliteit in de woningen, antislip porseleinen gres op de terrassen en porseleinen tegels van eerste kwaliteit in de badkamers.',
  'Podłoga drewniana pierwszej jakości wewnątrz mieszkań, antypoślizgowy gres porcelanowy na tarasach i płytki z gresu porcelanowego pierwszej jakości w łazienkach.',
  'Tregulv av første kvalitet inne i boligene, sklisikre porselensfliser på terrassene og porselensfliser av første kvalitet på badene.',
  'Trägolv av första klass inomhus i bostäderna, halkfritt porslinsgods på terrasserna och kakel av porslinsgods av första klass i badrummen.')
a('Plasterboard false ceilings in the kitchen, the main bathrooms and the service areas, plaster and paint on the other ceilings, and a timber coffering on the living-room and main-bedroom ceilings.',
  'Falsos techos de yeso laminado en la cocina, los baños principales y las zonas de paso de instalaciones, enlucido de yeso con pintura en el resto de los techos, y foseado de madera en los techos del salón y del dormitorio principal.',
  'Faux plafonds en plaques de plâtre dans la cuisine, les salles de bains principales et les zones de passage des installations, enduit de plâtre peint sur les autres plafonds, et caissons de bois aux plafonds du séjour et de la chambre principale.',
  'Abgehängte Gipskartondecken in Küche, Hauptbädern und den Bereichen für Installationen, Gipsputz mit Anstrich an den übrigen Decken und eine Holzkassettierung an den Decken von Wohnzimmer und Hauptschlafzimmer.',
  'Подвесные потолки из гипсокартона на кухне, в основных ванных комнатах и в местах прохода коммуникаций, штукатурка с покраской на остальных потолках и деревянная отделка-кессон на потолках гостиной и главной спальни.',
  'أسقف معلّقة من ألواح الجبس في المطبخ والحمامات الرئيسية ومناطق مرور التمديدات، وجصّ مع دهان على بقية الأسقف، وتجويف خشبي في سقفي غرفة المعيشة وغرفة النوم الرئيسية.',
  'Verlaagde plafonds van gipsplaat in de keuken, de hoofdbadkamers en de installatiezones, stucwerk met verf op de overige plafonds, en een houten plafondomlijsting op de plafonds van de woonkamer en de hoofdslaapkamer.',
  'Sufity podwieszane z płyt gipsowo-kartonowych w kuchni, łazienkach głównych i strefach przebiegu instalacji, tynk gipsowy z malowaniem na pozostałych sufitach oraz drewniane obramowanie sufitów w salonie i sypialni głównej.',
  'Nedforede himlinger i gipsplater på kjøkkenet, hovedbadene og områdene for installasjoner, gipspuss med maling på de øvrige himlingene, og en trekassettering i taket i stuen og hovedsoverommet.',
  'Undertak av gipsskivor i köket, huvudbadrummen och utrymmen där installationer går, gipsputs med målning på övriga tak, och en träkassett i taken i vardagsrummet och huvudsovrummet.')
a('A fitted kitchen with upper and lower units, a worktop in natural quartz or similar, and an island with a pull-out table that sits in several positions.',
  'Cocina amueblada con muebles altos y bajos, encimera de cuarzo natural o similar, e isla con mesa extraíble multiposición.',
  'Cuisine équipée avec meubles hauts et bas, plan de travail en quartz naturel ou équivalent, et îlot avec table extractible à plusieurs positions.',
  'Einbauküche mit Ober- und Unterschränken, Arbeitsplatte aus Naturquarz oder gleichwertig und einer Kücheninsel mit ausziehbarem Tisch in mehreren Positionen.',
  'Кухня с верхними и нижними шкафами, столешницей из натурального кварца или аналогичного материала и островом с выдвижным столом, фиксируемым в нескольких положениях.',
  'مطبخ مجهّز بخزائن علوية وسفلية، وسطح عمل من الكوارتز الطبيعي أو ما يماثله، وجزيرة بطاولة قابلة للسحب بأوضاع متعددة.',
  'Een ingerichte keuken met onder- en bovenkasten, een werkblad van natuurkwarts of gelijkwaardig, en een kookeiland met een uitschuifbare tafel in meerdere standen.',
  'Zabudowana kuchnia z szafkami dolnymi i górnymi, blatem z kwarcu naturalnego lub podobnego oraz wyspą z wysuwanym stołem o kilku położeniach.',
  'Innredet kjøkken med over- og underskap, benkeplate i naturkvarts eller tilsvarende, og en øy med uttrekkbart bord i flere posisjoner.',
  'Möblerat kök med över- och underskåp, bänkskiva i naturkvarts eller likvärdigt, och en köksö med utdragbart bord i flera lägen.')
a('An oven, an induction hob, an extractor hood, a washing machine, a dishwasher and a fridge, all from premium brands, are included.',
  'Se incluyen un horno, una placa de inducción, una campana extractora, una lavadora, un lavavajillas y un frigorífico, todos de marcas premium.',
  'Un four, une plaque à induction, une hotte aspirante, un lave-linge, un lave-vaisselle et un réfrigérateur, tous de marques haut de gamme, sont inclus.',
  'Ein Backofen, ein Induktionskochfeld, eine Dunstabzugshaube, eine Waschmaschine, ein Geschirrspüler und ein Kühlschrank, alle von Premiummarken, sind enthalten.',
  'В комплект входят духовой шкаф, индукционная варочная панель, вытяжка, стиральная машина, посудомоечная машина и холодильник, все — премиальных марок.',
  'تشمل التجهيزات فرنًا وموقد حث وشفاطًا وغسالة وغسالة صحون وثلاجة، كلها من علامات تجارية مميزة.',
  'Een oven, een inductiekookplaat, een afzuigkap, een wasmachine, een vaatwasser en een koelkast, allemaal van premiummerken, zijn inbegrepen.',
  'W cenie są piekarnik, płyta indukcyjna, okap, pralka, zmywarka i lodówka, wszystko renomowanych marek.',
  'Ovn, induksjonstopp, avtrekksvifte, vaskemaskin, oppvaskmaskin og kjøleskap, alt fra premiummerker, er inkludert.',
  'Ugn, induktionshäll, spisfläkt, tvättmaskin, diskmaskin och kylskåp, alla av premiummärken, ingår.')
a('White glazed porcelain sanitaryware, a low-profile acrylic-resin shower tray and a tempered-glass shower screen.',
  'Aparatos sanitarios de porcelana blanca esmaltada, plato de ducha de resina acrílica de perfil bajo y mampara de cristal templado.',
  'Appareils sanitaires en porcelaine émaillée blanche, receveur de douche extraplat en résine acrylique et paroi de douche en verre trempé.',
  'Sanitärkeramik aus weiß glasiertem Porzellan, eine flache Duschwanne aus Acrylharz und eine Duschwand aus Einscheibensicherheitsglas.',
  'Сантехника из белого глазурованного фарфора, низкий душевой поддон из акриловой смолы и душевая перегородка из закалённого стекла.',
  'أدوات صحية من الخزف الأبيض المطلي، وحوض دش منخفض الارتفاع من الراتنج الأكريليكي، وحاجز دش من الزجاج المقسّى.',
  'Sanitair van wit geglazuurd porselein, een lage douchebak van acrylhars en een douchewand van gehard glas.',
  'Ceramika sanitarna z białej glazurowanej porcelany, niski brodzik z żywicy akrylowej i kabina prysznicowa ze szkła hartowanego.',
  'Sanitærutstyr i hvitt glasert porselen, en lav dusjkum i akrylharpiks og en dusjvegg i herdet glass.',
  'Sanitetsporslin i vitt glaserat porslin, en låg duschbrunn i akrylharts och en duschvägg i härdat glas.')
a('Single-lever and thermostatic taps, in a finish the project management chooses.',
  'Grifería monomando y termostática, en un acabado que elige la dirección facultativa.',
  'Robinetterie mitigeur et thermostatique, dans une finition choisie par la direction de projet.',
  'Einhebel- und Thermostatarmaturen in einer von der Bauleitung gewählten Ausführung.',
  'Однорычажные и термостатические смесители в отделке, которую выбирает руководство проекта.',
  'صنابير أحادية المقبض وأخرى ترموستاتية، بتشطيب تختاره إدارة المشروع.',
  'Eengreeps- en thermostatische kranen, in een afwerking die de bouwleiding kiest.',
  'Baterie jednouchwytowe i termostatyczne, w wykończeniu wybranym przez kierownictwo projektu.',
  'Énhåndsbatterier og termostatbatterier, i en finish prosjektledelsen velger.',
  'Enhandsblandare och termostatblandare, i ett utförande som projektledningen väljer.')
a('Climate and electrical', 'Climatización y electricidad', 'Climatisation et électricité', 'Klima und Elektro', 'Климат и электрика',
  'التكييف والكهرباء', 'Klimaat en elektra', 'Klimat i elektryka', 'Klima og elektro', 'Klimat och el')
a('An aerothermal system that helps to heat the water, and air conditioning by fan-coils in the bathroom false ceilings, with fibreglass ducts to each room and a programmable thermostat in the living room.',
  'Un sistema de aerotermia que asiste en la producción de agua caliente sanitaria, y climatización mediante fan-coils en los falsos techos de los baños, con conductos de fibra de vidrio hasta cada estancia y un termostato programable en el salón.',
  'Un système aérothermique qui contribue à la production d’eau chaude sanitaire, et une climatisation par ventilo-convecteurs dans les faux plafonds des salles de bains, avec des gaines en fibre de verre vers chaque pièce et un thermostat programmable dans le séjour.',
  'Ein Luft-Wasser-Wärmepumpensystem, das die Warmwasserbereitung unterstützt, und eine Klimatisierung über Fan-Coils in den abgehängten Decken der Bäder, mit Glasfaserkanälen zu jedem Raum und einem programmierbaren Thermostat im Wohnzimmer.',
  'Аэротермическая система, участвующая в нагреве горячей воды, и кондиционирование фанкойлами в подвесных потолках ванных комнат, с воздуховодами из стекловолокна в каждое помещение и программируемым термостатом в гостиной.',
  'نظام حراري هوائي يساعد في إنتاج الماء الساخن، وتكييف عبر وحدات «فان كويل» في الأسقف المعلّقة للحمامات، مع مجارٍ من الألياف الزجاجية إلى كل غرفة ومنظّم حرارة قابل للبرمجة في غرفة المعيشة.',
  'Een aerothermisch systeem dat helpt bij het verwarmen van het water, en airconditioning via fan-coils in de verlaagde plafonds van de badkamers, met glasvezelkanalen naar elke ruimte en een programmeerbare thermostaat in de woonkamer.',
  'System aerotermiczny wspomagający podgrzewanie wody oraz klimatyzacja z klimakonwektorami w sufitach podwieszanych łazienek, z kanałami z włókna szklanego do każdego pomieszczenia i programowalnym termostatem w salonie.',
  'Et aerotermisk system som bidrar til oppvarming av vann, og klimaanlegg med viftekonvektorer i de nedforede himlingene på badene, med glassfiberkanaler til hvert rom og en programmerbar termostat i stuen.',
  'Ett aerotermiskt system som bidrar till uppvärmning av vattnet, och luftkonditionering med fläktkonvektorer i badrummens undertak, med glasfiberkanaler till varje rum och en programmerbar termostat i vardagsrummet.')
a('Pre-installation for electric-car charging in the garage, TV points in the living room and the main bedroom, a light point and a socket on the terraces, and a video intercom.',
  'Preinstalación de carga para coche eléctrico en el garaje, tomas de TV en el salón y el dormitorio principal, punto de luz y toma de corriente en las terrazas, y videoportero.',
  'Pré-équipement pour la recharge de véhicules électriques dans le garage, prises TV dans le séjour et la chambre principale, point lumineux et prise électrique sur les terrasses, et visiophone.',
  'Vorinstallation für das Laden von Elektrofahrzeugen in der Garage, TV-Anschlüsse im Wohnzimmer und im Hauptschlafzimmer, ein Lichtauslass und eine Steckdose auf den Terrassen sowie eine Video-Gegensprechanlage.',
  'Подготовка к зарядке электромобилей в гараже, ТВ-розетки в гостиной и главной спальне, точка освещения и розетка на террасах, видеодомофон.',
  'تجهيز مسبق لشحن السيارات الكهربائية في المرآب، ومخارج تلفاز في غرفة المعيشة وغرفة النوم الرئيسية، ونقطة إضاءة ومخرج كهرباء في التراسات، وجهاز اتصال مرئي.',
  'Voorbereiding voor het opladen van elektrische auto’s in de garage, tv-aansluitingen in de woonkamer en de hoofdslaapkamer, een lichtpunt en een stopcontact op de terrassen, en een videofoon.',
  'Przygotowanie do ładowania pojazdów elektrycznych w garażu, gniazda TV w salonie i sypialni głównej, punkt oświetleniowy i gniazdo elektryczne na tarasach oraz wideodomofon.',
  'Forberedelse for lading av elbil i garasjen, TV-uttak i stuen og hovedsoverommet, et lyspunkt og et strømuttak på terrassene, og en videoporttelefon.',
  'Förberedelse för laddning av elbil i garaget, tv-uttag i vardagsrummet och huvudsovrummet, en ljuspunkt och ett eluttag på terrasserna, och en videotelefon.')
a('Pools and terraces', 'Piscinas y terrazas', 'Piscines et terrasses', 'Pools und Terrassen', 'Бассейны и террасы', 'المسابح والتراسات',
  'Zwembaden en terrassen', 'Baseny i tarasy', 'Basseng og terrasser', 'Pooler och terrasser')
a('Fibre and polyester pools, with a size that the project management sets for each home, clad in natural stone on the outside.',
  'Piscinas de fibra y poliéster, de un tamaño que fija la dirección facultativa para cada vivienda, revestidas de piedra natural por fuera.',
  'Piscines en fibre et polyester, dont la taille est fixée par la direction de projet pour chaque logement, revêtues de pierre naturelle à l’extérieur.',
  'Pools aus Faser und Polyester, deren Größe die Bauleitung für jede Wohnung festlegt, außen mit Naturstein verkleidet.',
  'Бассейны из стекловолокна и полиэфира, размер которых для каждой квартиры определяет руководство проекта, снаружи облицованные натуральным камнем.',
  'مسابح من الألياف والبوليستر، بحجم تحدده إدارة المشروع لكل مسكن، ومكسوّة من الخارج بالحجر الطبيعي.',
  'Zwembaden van vezel en polyester, met een afmeting die de bouwleiding per woning vaststelt, aan de buitenkant bekleed met natuursteen.',
  'Baseny z włókna i poliestru, o rozmiarze ustalanym przez kierownictwo projektu dla każdego mieszkania, od zewnątrz obłożone kamieniem naturalnym.',
  'Basseng i fiber og polyester, i en størrelse prosjektledelsen fastsetter for hver bolig, kledd med naturstein på utsiden.',
  'Pooler av fiber och polyester, i en storlek som projektledningen fastställer för varje bostad, klädda med natursten på utsidan.')
a('An outdoor shower in the homes with a pool.', 'Ducha exterior en las viviendas con piscina.',
  'Douche extérieure dans les logements avec piscine.', 'Eine Außendusche in den Wohnungen mit Pool.',
  'Уличный душ в квартирах с бассейном.', 'دش خارجي في المساكن ذات المسبح.', 'Een buitendouche in de woningen met een zwembad.',
  'Prysznic zewnętrzny w mieszkaniach z basenem.', 'En utendørsdusj i boligene med basseng.', 'En utomhusdusch i bostäderna med pool.')
a('Lift, garage and common areas', 'Ascensor, garaje y zonas comunes', 'Ascenseur, garage et parties communes',
  'Aufzug, Garage und Gemeinschaftsflächen', 'Лифт, гараж и общие зоны', 'المصعد والمرآب والمرافق المشتركة',
  'Lift, garage en gemeenschappelijke ruimtes', 'Winda, garaż i części wspólne', 'Heis, garasje og fellesarealer',
  'Hiss, garage och gemensamma ytor')
a('A lift for four people with automatic doors that stops at the garage, an automatic entrance gate with the safety systems the regulations require, and a car lift at the garage entrance.',
  'Ascensor para cuatro personas con puertas automáticas y parada en el garaje, puerta de acceso automática con las instalaciones de seguridad que exige la normativa, y ascensor para coches en la entrada del garaje.',
  'Ascenseur pour quatre personnes avec portes automatiques et arrêt au garage, portail d’accès automatique avec les dispositifs de sécurité exigés par la réglementation, et monte-voitures à l’entrée du garage.',
  'Ein Aufzug für vier Personen mit automatischen Türen, der bis zur Garage fährt, ein automatisches Einfahrtstor mit den vorgeschriebenen Sicherheitseinrichtungen und ein Autoaufzug an der Garageneinfahrt.',
  'Лифт на четыре человека с автоматическими дверями и остановкой в гараже, автоматические въездные ворота с системами безопасности, которых требуют нормы, и автомобильный лифт у въезда в гараж.',
  'مصعد يتسع لأربعة أشخاص بأبواب آلية ويتوقف عند المرآب، وبوابة دخول آلية بأنظمة الأمان التي تتطلبها الأنظمة، ومصعد للسيارات عند مدخل المرآب.',
  'Een lift voor vier personen met automatische deuren die tot in de garage rijdt, een automatische toegangspoort met de veiligheidsvoorzieningen die de voorschriften eisen, en een autolift bij de ingang van de garage.',
  'Winda na cztery osoby z automatycznymi drzwiami zatrzymująca się w garażu, automatyczna brama wjazdowa z systemami bezpieczeństwa wymaganymi przepisami oraz winda samochodowa przy wjeździe do garażu.',
  'En heis for fire personer med automatiske dører som stopper i garasjen, en automatisk innkjøringsport med sikkerhetssystemene forskriftene krever, og en bilheis ved garasjeinngangen.',
  'En hiss för fyra personer med automatiska dörrar som stannar i garaget, en automatisk infartsport med de säkerhetssystem föreskrifterna kräver, och en bilhiss vid garageinfarten.')
a('Glass balustrades.', 'Barandillas de cristal.', 'Garde-corps en verre.', 'Glasbrüstungen.', 'Стеклянные ограждения.',
  'حواجز زجاجية.', 'Glazen balustrades.', 'Szklane balustrady.', 'Glassrekkverk.', 'Glasräcken.')

# ---------------------------------------------------------------- residences
a('Six homes, <em>four kinds</em>', 'Seis viviendas, <em>cuatro tipos</em>', 'Six logements, <em>quatre types</em>',
  'Sechs Wohnungen, <em>vier Typen</em>', 'Шесть квартир, <em>четыре типа</em>', 'ستة مساكن، <em>أربعة أنواع</em>',
  'Zes woningen, <em>vier soorten</em>', 'Sześć mieszkań, <em>cztery rodzaje</em>', 'Seks boliger, <em>fire typer</em>',
  'Sex bostäder, <em>fyra typer</em>')
a('The six homes fall into four groups by floor, size and outdoor space. The table below lists each one with its price.',
  'Las seis viviendas se dividen en cuatro grupos según la planta, el tamaño y el espacio exterior. La tabla siguiente recoge cada una con su precio.',
  'Les six logements se répartissent en quatre groupes selon l’étage, la taille et l’espace extérieur. Le tableau ci-dessous présente chacun avec son prix.',
  'Die sechs Wohnungen lassen sich nach Etage, Größe und Außenbereich in vier Gruppen einteilen. Die folgende Tabelle führt jede einzelne mit ihrem Preis auf.',
  'Шесть квартир делятся на четыре группы по этажу, размеру и открытому пространству. В таблице ниже указана каждая из них с ценой.',
  'تنقسم المساكن الستة إلى أربع مجموعات بحسب الطابق والحجم والمساحة الخارجية. ويعرض الجدول أدناه كل مسكن مع سعره.',
  'De zes woningen vallen naar verdieping, grootte en buitenruimte uiteen in vier groepen. In de tabel hieronder staat elke woning met haar prijs.',
  'Sześć mieszkań dzieli się na cztery grupy według piętra, wielkości i przestrzeni zewnętrznej. W tabeli poniżej podano każde z nich wraz z ceną.',
  'De seks boligene deles inn i fire grupper etter etasje, størrelse og utendørsareal. Tabellen nedenfor viser hver av dem med pris.',
  'De sex bostäderna delas in i fyra grupper efter våning, storlek och uteplats. Tabellen nedan listar var och en med sitt pris.')
a('Bajo A has one bedroom and one bathroom, with a living room and kitchen of 28.07 sqm and a bedroom of 13.48 sqm, at EUR 495,000.',
  'Bajo A tiene un dormitorio y un baño, con un salón-cocina de {N28.07} {U} y un dormitorio de {N13.48} {U}, por {E495000}.',
  'Bajo A a une chambre et une salle de bains, avec un séjour-cuisine de {N28.07} {U} et une chambre de {N13.48} {U}, à {E495000}.',
  'Bajo A hat ein Schlafzimmer und ein Bad, mit einem Wohn- und Küchenbereich von {N28.07} {U} und einem Schlafzimmer von {N13.48} {U}, für {E495000}.',
  'У Bajo A одна спальня и одна ванная комната, гостиная-кухня {N28.07} {U} и спальня {N13.48} {U}, цена — {E495000}.',
  'يضم Bajo A غرفة نوم وحمامًا واحدًا، مع غرفة معيشة ومطبخ بمساحة {N28.07} {U} وغرفة نوم بمساحة {N13.48} {U}، بسعر {E495000}.',
  'Bajo A heeft één slaapkamer en één badkamer, met een woonkamer met keuken van {N28.07} {U} en een slaapkamer van {N13.48} {U}, voor {E495000}.',
  'Bajo A ma jedną sypialnię i jedną łazienkę, salon z kuchnią o powierzchni {N28.07} {U} i sypialnię o powierzchni {N13.48} {U}, za {E495000}.',
  'Bajo A har ett soverom og ett bad, med en stue og et kjøkken på {N28.07} {U} og et soverom på {N13.48} {U}, til {E495000}.',
  'Bajo A har ett sovrum och ett badrum, med ett vardagsrum och kök på {N28.07} {U} och ett sovrum på {N13.48} {U}, för {E495000}.')
a('Bajo B has three bedrooms and two bathrooms, with a living room and kitchen of 40.13 sqm, at EUR 850,000.',
  'Bajo B tiene tres dormitorios y dos baños, con un salón-cocina de {N40.13} {U}, por {E850000}.',
  'Bajo B a trois chambres et deux salles de bains, avec un séjour-cuisine de {N40.13} {U}, à {E850000}.',
  'Bajo B hat drei Schlafzimmer und zwei Bäder, mit einem Wohn- und Küchenbereich von {N40.13} {U}, für {E850000}.',
  'У Bajo B три спальни и две ванные комнаты, гостиная-кухня {N40.13} {U}, цена — {E850000}.',
  'يضم Bajo B ثلاث غرف نوم وحمامين، مع غرفة معيشة ومطبخ بمساحة {N40.13} {U}، بسعر {E850000}.',
  'Bajo B heeft drie slaapkamers en twee badkamers, met een woonkamer met keuken van {N40.13} {U}, voor {E850000}.',
  'Bajo B ma trzy sypialnie i dwie łazienki, salon z kuchnią o powierzchni {N40.13} {U}, za {E850000}.',
  'Bajo B har tre soverom og to bad, med en stue og et kjøkken på {N40.13} {U}, til {E850000}.',
  'Bajo B har tre sovrum och två badrum, med ett vardagsrum och kök på {N40.13} {U}, för {E850000}.')
a('Neither has a terrace. Each comes with a garage space and a storage room.',
  'Ninguna tiene terraza. Cada una incluye plaza de garaje y trastero.',
  'Aucun n’a de terrasse. Chacun comprend une place de garage et une cave.',
  'Keine hat eine Terrasse. Jede umfasst einen Garagenstellplatz und einen Abstellraum.',
  'Ни у одной нет террасы. К каждой прилагаются место в гараже и кладовая.',
  'ليس لأي منهما تراس. ويأتي كل منهما مع موقف في المرآب وغرفة تخزين.',
  'Geen van beide heeft een terras. Elk wordt geleverd met een garageplaats en een berging.',
  'Żadne nie ma tarasu. Każde ma miejsce garażowe i komórkę lokatorską.',
  'Ingen av dem har terrasse. Hver følger med garasjeplass og bod.',
  'Ingen av dem har någon terrass. Var och en levereras med en garageplats och ett förråd.')
a('First-floor homes with two bedrooms', 'Viviendas de dos dormitorios en la primera planta', 'Logements de deux chambres au premier étage',
  'Wohnungen mit zwei Schlafzimmern im ersten Obergeschoss', 'Квартиры с двумя спальнями на втором этаже',
  'مساكن بغرفتي نوم في الطابق الأول', 'Woningen met twee slaapkamers op de eerste verdieping',
  'Mieszkania z dwiema sypialniami na pierwszym piętrze', 'Boliger med to soverom i andre etasje',
  'Bostäder med två sovrum på första våningen')
a('Homes 1ºB and 1ºC have two bedrooms and two bathrooms and no terrace, at EUR 742,000 and EUR 735,000.',
  'Las viviendas 1ºB y 1ºC tienen dos dormitorios y dos baños y no tienen terraza, por {E742000} y {E735000}.',
  'Les logements 1ºB et 1ºC ont deux chambres et deux salles de bains, sans terrasse, à {E742000} et {E735000}.',
  'Die Wohnungen 1ºB und 1ºC haben zwei Schlafzimmer und zwei Bäder und keine Terrasse, für {E742000} und {E735000}.',
  'У квартир 1ºB и 1ºC по две спальни и по две ванные комнаты, террасы нет, цены — {E742000} и {E735000}.',
  'يضم المسكنان 1ºB و1ºC غرفتي نوم وحمامين ولا تراس لهما، بسعرين هما {E742000} و{E735000}.',
  'De woningen 1ºB en 1ºC hebben twee slaapkamers en twee badkamers en geen terras, voor {E742000} en {E735000}.',
  'Mieszkania 1ºB i 1ºC mają dwie sypialnie i dwie łazienki oraz nie mają tarasu, za {E742000} i {E735000}.',
  'Boligene 1ºB og 1ºC har to soverom og to bad og ingen terrasse, til {E742000} og {E735000}.',
  'Bostäderna 1ºB och 1ºC har två sovrum och två badrum och ingen terrass, för {E742000} och {E735000}.')
a('1ºB has 69.33 sqm interior and 78.02 sqm built, and 1ºC has 67.26 sqm interior and 77.39 sqm built.',
  'La 1ºB tiene {N69.33} {U} interiores y {N78.02} {U} construidos, y la 1ºC tiene {N67.26} {U} interiores y {N77.39} {U} construidos.',
  'Le 1ºB a {N69.33} {U} intérieurs et {N78.02} {U} construits, et le 1ºC a {N67.26} {U} intérieurs et {N77.39} {U} construits.',
  '1ºB hat {N69.33} {U} Innenfläche und {N78.02} {U} bebaute Fläche, 1ºC hat {N67.26} {U} Innenfläche und {N77.39} {U} bebaute Fläche.',
  'У 1ºB внутренняя площадь — {N69.33} {U}, площадь застройки — {N78.02} {U}; у 1ºC — {N67.26} {U} и {N77.39} {U} соответственно.',
  'مساحة 1ºB الداخلية {N69.33} {U} والمبنية {N78.02} {U}، ومساحة 1ºC الداخلية {N67.26} {U} والمبنية {N77.39} {U}.',
  '1ºB heeft {N69.33} {U} binnenoppervlakte en {N78.02} {U} bebouwde oppervlakte, en 1ºC heeft {N67.26} {U} binnenoppervlakte en {N77.39} {U} bebouwde oppervlakte.',
  '1ºB ma {N69.33} {U} powierzchni wewnętrznej i {N78.02} {U} powierzchni zabudowy, a 1ºC ma {N67.26} {U} powierzchni wewnętrznej i {N77.39} {U} powierzchni zabudowy.',
  '1ºB har {N69.33} {U} innvendig areal og {N78.02} {U} bebygd areal, og 1ºC har {N67.26} {U} innvendig areal og {N77.39} {U} bebygd areal.',
  '1ºB har {N69.33} {U} invändig yta och {N78.02} {U} byggyta, och 1ºC har {N67.26} {U} invändig yta och {N77.39} {U} byggyta.')
a('Each comes with a garage space and a storage room.', 'Cada una incluye plaza de garaje y trastero.',
  'Chacun comprend une place de garage et une cave.', 'Jede umfasst einen Garagenstellplatz und einen Abstellraum.',
  'К каждой прилагаются место в гараже и кладовая.', 'ويأتي كل منهما مع موقف في المرآب وغرفة تخزين.',
  'Elk wordt geleverd met een garageplaats en een berging.', 'Każde ma miejsce garażowe i komórkę lokatorską.',
  'Hver følger med garasjeplass og bod.', 'Var och en levereras med en garageplats och ett förråd.')
a('A first-floor home with a patio and a private pool', 'Una vivienda de la primera planta con patio y piscina privada',
  'Un logement du premier étage avec patio et piscine privée', 'Eine Wohnung im ersten Obergeschoss mit Patio und privatem Pool',
  'Квартира на втором этаже с патио и частным бассейном', 'مسكن في الطابق الأول بفناء ومسبح خاص',
  'Een woning op de eerste verdieping met een patio en een privézwembad', 'Mieszkanie na pierwszym piętrze z patio i prywatnym basenem',
  'En bolig i andre etasje med patio og eget basseng', 'En bostad på första våningen med patio och egen pool')
a('Home 1ºA has two bedrooms and two bathrooms, with a patio of 38.56 sqm and a private pool, at EUR 763,000. The price list calls the patio a terrace.',
  'La vivienda 1ºA tiene dos dormitorios y dos baños, con un patio de {N38.56} {U} y una piscina privada, por {E763000}. La lista de precios llama terraza al patio.',
  'Le logement 1ºA a deux chambres et deux salles de bains, avec un patio de {N38.56} {U} et une piscine privée, à {E763000}. La liste de prix appelle le patio une terrasse.',
  'Wohnung 1ºA hat zwei Schlafzimmer und zwei Bäder, mit einem Patio von {N38.56} {U} und einem privaten Pool, für {E763000}. Die Preisliste nennt das Patio eine Terrasse.',
  'У квартиры 1ºA две спальни и две ванные комнаты, патио {N38.56} {U} и частный бассейн, цена — {E763000}. В прайс-листе патио названо террасой.',
  'يضم المسكن 1ºA غرفتي نوم وحمامين، مع فناء بمساحة {N38.56} {U} ومسبح خاص، بسعر {E763000}. وتسمّي قائمة الأسعار الفناء تراسًا.',
  'Woning 1ºA heeft twee slaapkamers en twee badkamers, met een patio van {N38.56} {U} en een privézwembad, voor {E763000}. De prijslijst noemt de patio een terras.',
  'Mieszkanie 1ºA ma dwie sypialnie i dwie łazienki, patio o powierzchni {N38.56} {U} i prywatny basen, za {E763000}. Cennik nazywa patio tarasem.',
  'Bolig 1ºA har to soverom og to bad, med et patio på {N38.56} {U} og eget basseng, til {E763000}. Prislisten kaller patioet en terrasse.',
  'Bostad 1ºA har två sovrum och två badrum, med en patio på {N38.56} {U} och egen pool, för {E763000}. Prislistan kallar pation en terrass.')
a('The plan and the price list give 56.16 sqm interior and 65.44 sqm built. The dossier also gives totals under the Andalusian decree 218/2005 of 61.78 sqm interior and 71.06 sqm built for this home.',
  'El plano y la lista de precios dan {N56.16} {U} interiores y {N65.44} {U} construidos. El dosier da además, conforme al decreto andaluz 218/2005, totales de {N61.78} {U} interiores y {N71.06} {U} construidos para esta vivienda.',
  'Le plan et la liste de prix donnent {N56.16} {U} intérieurs et {N65.44} {U} construits. Le dossier donne aussi, selon le décret andalou 218/2005, des totaux de {N61.78} {U} intérieurs et {N71.06} {U} construits pour ce logement.',
  'Der Grundriss und die Preisliste geben {N56.16} {U} Innenfläche und {N65.44} {U} bebaute Fläche an. Das Dossier nennt für diese Wohnung außerdem nach dem andalusischen Dekret 218/2005 Summen von {N61.78} {U} Innenfläche und {N71.06} {U} bebauter Fläche.',
  'В плане и в прайс-листе указаны внутренняя площадь {N56.16} {U} и площадь застройки {N65.44} {U}. В досье для этой квартиры также приведены итоговые значения по андалусскому декрету 218/2005: внутренняя площадь {N61.78} {U} и площадь застройки {N71.06} {U}.',
  'يذكر المخطط وقائمة الأسعار مساحة داخلية {N56.16} {U} ومساحة مبنية {N65.44} {U}. ويذكر الملف أيضًا لهذا المسكن، وفق المرسوم الأندلسي 218/2005، إجماليين هما {N61.78} {U} داخلية و{N71.06} {U} مبنية.',
  'De plattegrond en de prijslijst geven {N56.16} {U} binnenoppervlakte en {N65.44} {U} bebouwde oppervlakte. Het dossier geeft voor deze woning ook, volgens het Andalusische decreet 218/2005, totalen van {N61.78} {U} binnenoppervlakte en {N71.06} {U} bebouwde oppervlakte.',
  'Rzut i cennik podają {N56.16} {U} powierzchni wewnętrznej i {N65.44} {U} powierzchni zabudowy. Dossier podaje dla tego mieszkania również sumy według andaluzyjskiego dekretu 218/2005: {N61.78} {U} powierzchni wewnętrznej i {N71.06} {U} powierzchni zabudowy.',
  'Plantegningen og prislisten oppgir {N56.16} {U} innvendig areal og {N65.44} {U} bebygd areal. Dossieret oppgir også, etter det andalusiske dekretet 218/2005, summer på {N61.78} {U} innvendig areal og {N71.06} {U} bebygd areal for denne boligen.',
  'Planritningen och prislistan anger {N56.16} {U} invändig yta och {N65.44} {U} byggyta. Dossiern anger också, enligt det andalusiska dekretet 218/2005, summor på {N61.78} {U} invändig yta och {N71.06} {U} byggyta för den här bostaden.')
a('It comes with a garage space and a storage room.', 'Incluye plaza de garaje y trastero.',
  'Il comprend une place de garage et une cave.', 'Sie umfasst einen Garagenstellplatz und einen Abstellraum.',
  'К ней прилагаются место в гараже и кладовая.', 'ويأتي مع موقف في المرآب وغرفة تخزين.',
  'Ze wordt geleverd met een garageplaats en een berging.', 'Ma miejsce garażowe i komórkę lokatorską.',
  'Den følger med garasjeplass og bod.', 'Den levereras med en garageplats och ett förråd.')
a('A three-bedroom home on the first floor', 'Una vivienda de tres dormitorios en la primera planta',
  'Un logement de trois chambres au premier étage', 'Eine Wohnung mit drei Schlafzimmern im ersten Obergeschoss',
  'Квартира с тремя спальнями на втором этаже', 'مسكن بثلاث غرف نوم في الطابق الأول',
  'Een woning met drie slaapkamers op de eerste verdieping', 'Mieszkanie z trzema sypialniami na pierwszym piętrze',
  'En bolig med tre soverom i andre etasje', 'En bostad med tre sovrum på första våningen')
a('Home 1ºD has three bedrooms and two bathrooms, with a living room and kitchen of 36.73 sqm, at EUR 895,000.',
  'La vivienda 1ºD tiene tres dormitorios y dos baños, con un salón-cocina de {N36.73} {U}, por {E895000}.',
  'Le logement 1ºD a trois chambres et deux salles de bains, avec un séjour-cuisine de {N36.73} {U}, à {E895000}.',
  'Wohnung 1ºD hat drei Schlafzimmer und zwei Bäder, mit einem Wohn- und Küchenbereich von {N36.73} {U}, für {E895000}.',
  'У квартиры 1ºD три спальни и две ванные комнаты, гостиная-кухня {N36.73} {U}, цена — {E895000}.',
  'يضم المسكن 1ºD ثلاث غرف نوم وحمامين، مع غرفة معيشة ومطبخ بمساحة {N36.73} {U}، بسعر {E895000}.',
  'Woning 1ºD heeft drie slaapkamers en twee badkamers, met een woonkamer met keuken van {N36.73} {U}, voor {E895000}.',
  'Mieszkanie 1ºD ma trzy sypialnie i dwie łazienki, salon z kuchnią o powierzchni {N36.73} {U}, za {E895000}.',
  'Bolig 1ºD har tre soverom og to bad, med en stue og et kjøkken på {N36.73} {U}, til {E895000}.',
  'Bostad 1ºD har tre sovrum och två badrum, med ett vardagsrum och kök på {N36.73} {U}, för {E895000}.')
a('It has 83.17 sqm interior and 94.84 sqm built, and comes with a garage space and a storage room.',
  'Tiene {N83.17} {U} interiores y {N94.84} {U} construidos, e incluye plaza de garaje y trastero.',
  'Il a {N83.17} {U} intérieurs et {N94.84} {U} construits, et comprend une place de garage et une cave.',
  'Sie hat {N83.17} {U} Innenfläche und {N94.84} {U} bebaute Fläche und umfasst einen Garagenstellplatz und einen Abstellraum.',
  'Внутренняя площадь — {N83.17} {U}, площадь застройки — {N94.84} {U}; к квартире прилагаются место в гараже и кладовая.',
  'مساحتها الداخلية {N83.17} {U} والمبنية {N94.84} {U}، وتأتي مع موقف في المرآب وغرفة تخزين.',
  'Ze heeft {N83.17} {U} binnenoppervlakte en {N94.84} {U} bebouwde oppervlakte en wordt geleverd met een garageplaats en een berging.',
  'Ma {N83.17} {U} powierzchni wewnętrznej i {N94.84} {U} powierzchni zabudowy oraz miejsce garażowe i komórkę lokatorską.',
  'Den har {N83.17} {U} innvendig areal og {N94.84} {U} bebygd areal, og følger med garasjeplass og bod.',
  'Den har {N83.17} {U} invändig yta och {N94.84} {U} byggyta och levereras med en garageplats och ett förråd.')

# ---------------------------------------------------------------- lifestyle
a('A patio, <em>private pools</em> and a lift to the garage', 'Un patio, <em>piscinas privadas</em> y un ascensor hasta el garaje',
  'Un patio, <em>des piscines privées</em> et un ascenseur jusqu’au garage', 'Ein Patio, <em>private Pools</em> und ein Aufzug zur Garage',
  'Патио, <em>частные бассейны</em> и лифт до гаража', 'فناء، <em>ومسابح خاصة</em> ومصعد إلى المرآب',
  'Een patio, <em>privézwembaden</em> en een lift naar de garage', 'Patio, <em>prywatne baseny</em> i winda do garażu',
  'Et patio, <em>egne basseng</em> og heis til garasjen', 'En patio, <em>egna pooler</em> och hiss till garaget')
a('The outdoor space belongs to the individual homes: a patio, terraces and private pools, by home type.',
  'El espacio exterior es de cada vivienda: un patio, terrazas y piscinas privadas, según el tipo de vivienda.',
  'L’espace extérieur est propre à chaque logement : un patio, des terrasses et des piscines privées, selon le type de logement.',
  'Die Außenbereiche gehören zu den einzelnen Wohnungen: ein Patio, Terrassen und private Pools, je nach Wohnungstyp.',
  'Открытое пространство принадлежит отдельным квартирам: патио, террасы и частные бассейны — в зависимости от типа квартиры.',
  'المساحات الخارجية تخص كل مسكن على حدة: فناء وتراسات ومسابح خاصة، بحسب نوع المسكن.',
  'De buitenruimte hoort bij de afzonderlijke woningen: een patio, terrassen en privézwembaden, afhankelijk van het woningtype.',
  'Przestrzeń zewnętrzna należy do poszczególnych mieszkań: patio, tarasy i prywatne baseny, zależnie od typu mieszkania.',
  'Utendørsarealene hører til de enkelte boligene: et patio, terrasser og egne basseng, avhengig av boligtype.',
  'Uteplatserna hör till de enskilda bostäderna: en patio, terrasser och egna pooler, beroende på bostadstyp.')
a('The patio and the pool', 'El patio y la piscina', 'Le patio et la piscine', 'Das Patio und der Pool', 'Патио и бассейн',
  'الفناء والمسبح', 'De patio en het zwembad', 'Patio i basen', 'Patioet og bassenget', 'Pation och poolen')
a('Home 1ºA has a patio of 38.56 sqm with a private pool. The specification describes the pools as fibre and polyester, clad in natural stone, with an outdoor shower.',
  'La vivienda 1ºA tiene un patio de {N38.56} {U} con piscina privada. La memoria de calidades describe las piscinas como de fibra y poliéster, revestidas de piedra natural, con ducha exterior.',
  'Le logement 1ºA a un patio de {N38.56} {U} avec une piscine privée. Le descriptif décrit les piscines comme étant en fibre et polyester, revêtues de pierre naturelle, avec une douche extérieure.',
  'Wohnung 1ºA hat ein Patio von {N38.56} {U} mit privatem Pool. Die Baubeschreibung beschreibt die Pools als aus Faser und Polyester, mit Naturstein verkleidet, mit einer Außendusche.',
  'У квартиры 1ºA патио {N38.56} {U} с частным бассейном. В спецификации бассейны описаны как выполненные из стекловолокна и полиэфира, облицованные натуральным камнем, с уличным душем.',
  'للمسكن 1ºA فناء بمساحة {N38.56} {U} مع مسبح خاص. وتصف المواصفات المسابح بأنها من الألياف والبوليستر ومكسوّة بالحجر الطبيعي، مع دش خارجي.',
  'Woning 1ºA heeft een patio van {N38.56} {U} met een privézwembad. De specificatie beschrijft de zwembaden als van vezel en polyester, bekleed met natuursteen, met een buitendouche.',
  'Mieszkanie 1ºA ma patio o powierzchni {N38.56} {U} z prywatnym basenem. Specyfikacja opisuje baseny jako wykonane z włókna i poliestru, obłożone kamieniem naturalnym, z prysznicem zewnętrznym.',
  'Bolig 1ºA har et patio på {N38.56} {U} med eget basseng. Spesifikasjonen beskriver bassengene som av fiber og polyester, kledd med naturstein, med utendørsdusj.',
  'Bostad 1ºA har en patio på {N38.56} {U} med egen pool. Beskrivningen anger att poolerna är av fiber och polyester, klädda med natursten, med utomhusdusch.')
a('The upper homes', 'Las viviendas superiores', 'Les logements supérieurs', 'Die oberen Wohnungen', 'Верхние квартиры',
  'المساكن العليا', 'De bovenste woningen', 'Górne mieszkania', 'De øvre boligene', 'De övre bostäderna')
a('The four reserved homes on the second and top floors are listed with terraces and pools. They are not available, but they show what the building offers at the top.',
  'Las cuatro viviendas reservadas de la segunda planta y de la planta superior figuran con terrazas y piscinas. No están disponibles, pero muestran lo que ofrece el edificio en las plantas altas.',
  'Les quatre logements réservés du deuxième étage et de l’étage supérieur sont indiqués avec des terrasses et des piscines. Ils ne sont pas disponibles, mais ils montrent ce que l’immeuble offre dans les étages hauts.',
  'Die vier reservierten Wohnungen im zweiten Obergeschoss und im obersten Geschoss sind mit Terrassen und Pools gelistet. Sie sind nicht verfügbar, zeigen aber, was das Gebäude oben bietet.',
  'Четыре забронированные квартиры на третьем и верхнем этажах указаны с террасами и бассейнами. Они недоступны, но показывают, что дом предлагает на верхних этажах.',
  'المساكن الأربعة المحجوزة في الطابق الثاني والطابق العلوي مُدرجة بتراسات ومسابح. وهي غير متاحة، لكنها تُظهر ما يقدّمه المبنى في طوابقه العليا.',
  'De vier gereserveerde woningen op de tweede en de bovenste verdieping staan vermeld met terrassen en zwembaden. Ze zijn niet beschikbaar, maar laten zien wat het gebouw bovenin biedt.',
  'Cztery zarezerwowane mieszkania na drugim piętrze i na najwyższej kondygnacji są wymienione z tarasami i basenami. Nie są dostępne, ale pokazują, co budynek oferuje na górze.',
  'De fire reserverte boligene i tredje og øverste etasje er oppført med terrasser og basseng. De er ikke tilgjengelige, men viser hva bygget tilbyr øverst.',
  'De fyra reserverade bostäderna på andra och översta våningen är listade med terrasser och pooler. De är inte tillgängliga, men visar vad byggnaden erbjuder högst upp.')
a('Timber coffered ceilings in the living room and the main bedroom, and a fitted kitchen with an island, in the images and the specification.',
  'Techos con foseado de madera en el salón y el dormitorio principal, y una cocina amueblada con isla, en las imágenes y en la memoria de calidades.',
  'Plafonds à caissons de bois dans le séjour et la chambre principale, et une cuisine équipée avec îlot, sur les images et dans le descriptif.',
  'Holzkassettendecken im Wohnzimmer und im Hauptschlafzimmer sowie eine Einbauküche mit Insel, in den Bildern und in der Baubeschreibung.',
  'Потолки с деревянными кессонами в гостиной и главной спальне и кухня с островом — на изображениях и в спецификации.',
  'أسقف بتجويف خشبي في غرفة المعيشة وغرفة النوم الرئيسية، ومطبخ مجهّز بجزيرة، في الصور وفي المواصفات.',
  'Houten plafondomlijstingen in de woonkamer en de hoofdslaapkamer, en een ingerichte keuken met een kookeiland, op de beelden en in de specificatie.',
  'Drewniane obramowania sufitów w salonie i sypialni głównej oraz zabudowana kuchnia z wyspą — na wizualizacjach i w specyfikacji.',
  'Trekassettering i taket i stuen og hovedsoverommet, og et innredet kjøkken med øy, på bildene og i spesifikasjonen.',
  'Träkassetter i taken i vardagsrummet och huvudsovrummet, och ett möblerat kök med köksö, på bilderna och i beskrivningen.')
a('Every day', 'Cada día', 'Au quotidien', 'Im Alltag', 'Каждый день', 'كل يوم', 'Elke dag', 'Na co dzień', 'Hver dag', 'Varje dag')
a('A garage space that a car lift reaches, a storage room, and a lift that stops at the garage.',
  'Una plaza de garaje a la que se llega con un ascensor para coches, un trastero y un ascensor que para en el garaje.',
  'Une place de garage desservie par un monte-voitures, une cave et un ascenseur qui dessert le garage.',
  'Ein Garagenstellplatz, den ein Autoaufzug erreicht, ein Abstellraum und ein Aufzug, der bis zur Garage fährt.',
  'Место в гараже, куда ведёт автомобильный лифт, кладовая и лифт с остановкой в гараже.',
  'موقف في المرآب يصل إليه مصعد السيارات، وغرفة تخزين، ومصعد يتوقف عند المرآب.',
  'Een garageplaats die een autolift bereikt, een berging en een lift die tot in de garage rijdt.',
  'Miejsce garażowe, do którego prowadzi winda samochodowa, komórka lokatorska i winda zatrzymująca się w garażu.',
  'En garasjeplass som nås med bilheis, en bod og en heis som stopper i garasjen.',
  'En garageplats som nås med bilhiss, ett förråd och en hiss som stannar i garaget.')

# ---------------------------------------------------------------- location
a('Central Estepona, <em>beside the old town</em>', 'El centro de Estepona, <em>junto al casco antiguo</em>',
  'Le centre d’Estepona, <em>à côté de la vieille ville</em>', 'Zentrum von Estepona, <em>direkt an der Altstadt</em>',
  'Центр Эстепоны, <em>рядом со старым городом</em>', 'وسط إستيبونا، <em>بجوار البلدة القديمة</em>',
  'Het centrum van Estepona, <em>naast de oude stad</em>', 'Centrum Estepony, <em>obok starego miasta</em>',
  'Sentrum av Estepona, <em>ved siden av gamlebyen</em>', 'Centrala Estepona, <em>intill gamla stan</em>')
a('The dossier places the building in the centre of Estepona, next to the old town, among shops, supermarkets, schools and sports facilities. Its map gives the marina as 3 minutes away, Punta Plata beach as 9 and Padrón beach as 10, without saying whether those are minutes on foot or by car. It also names the A-7 and the AP-7, which leads to Málaga airport.',
  'El dosier sitúa el edificio en el centro de Estepona, junto al casco antiguo, entre comercios, supermercados, colegios e instalaciones deportivas. Su mapa da el puerto deportivo a 3 minutos, la playa de Punta Plata a 9 y la playa del Padrón a 10, sin decir si son minutos a pie o en coche. Nombra además la A-7 y la AP-7, que lleva al aeropuerto de Málaga.',
  'Le dossier situe l’immeuble au centre d’Estepona, à côté de la vieille ville, parmi des commerces, des supermarchés, des écoles et des équipements sportifs. Sa carte indique le port de plaisance à 3 minutes, la plage de Punta Plata à 9 et la plage du Padrón à 10, sans préciser s’il s’agit de minutes à pied ou en voiture. Il cite aussi l’A-7 et l’AP-7, qui mène à l’aéroport de Málaga.',
  'Das Dossier verortet das Gebäude im Zentrum von Estepona, direkt an der Altstadt, zwischen Geschäften, Supermärkten, Schulen und Sportanlagen. Seine Karte nennt den Yachthafen in 3 Minuten, den Strand Punta Plata in 9 und den Strand El Padrón in 10, ohne anzugeben, ob es sich um Minuten zu Fuß oder mit dem Auto handelt. Es nennt außerdem die A-7 und die AP-7, die zum Flughafen Málaga führt.',
  'В досье дом расположен в центре Эстепоны, рядом со старым городом, среди магазинов, супермаркетов, школ и спортивных объектов. На карте в досье до порта 3 минуты, до пляжа Пунта-Плата — 9, до пляжа Падрон — 10, но не сказано, идёт ли речь о минутах пешком или на машине. Также названы трассы A-7 и AP-7, которая ведёт к аэропорту Малаги.',
  'يضع الملف المبنى في وسط إستيبونا بجوار البلدة القديمة، بين المتاجر والأسواق والمدارس والمرافق الرياضية. وتذكر خريطته أن المرسى على بُعد 3 دقائق وشاطئ بونتا بلاتا 9 دقائق وشاطئ إل بادرون 10 دقائق، دون أن توضح هل هي دقائق سيرًا أم بالسيارة. ويذكر أيضًا الطريقين A-7 وAP-7 الذي يؤدي إلى مطار مالقة.',
  'Het dossier plaatst het gebouw in het centrum van Estepona, naast de oude stad, tussen winkels, supermarkten, scholen en sportvoorzieningen. Zijn kaart noemt de jachthaven op 3 minuten, het strand van Punta Plata op 9 en het strand van El Padrón op 10, zonder te zeggen of het om minuten te voet of met de auto gaat. Het noemt ook de A-7 en de AP-7, die naar de luchthaven van Málaga leidt.',
  'Dossier umieszcza budynek w centrum Estepony, obok starego miasta, wśród sklepów, supermarketów, szkół i obiektów sportowych. Jego mapa podaje port jachtowy w odległości 3 minut, plażę Punta Plata 9, a plażę El Padrón 10, nie mówiąc, czy są to minuty pieszo, czy samochodem. Wymienia też A-7 i AP-7, która prowadzi na lotnisko w Maladze.',
  'Dossieret plasserer bygget i sentrum av Estepona, ved siden av gamlebyen, blant butikker, supermarkeder, skoler og idrettsanlegg. Kartet oppgir småbåthavnen 3 minutter unna, stranden Punta Plata 9 og stranden El Padrón 10, uten å si om det er minutter til fots eller med bil. Det nevner også A-7 og AP-7, som fører til Málaga lufthavn.',
  'Dossiern placerar byggnaden i centrala Estepona, intill gamla stan, bland butiker, stormarknader, skolor och idrottsanläggningar. Kartan anger småbåtshamnen på 3 minuter, stranden Punta Plata på 9 och stranden El Padrón på 10, utan att säga om det är minuter till fots eller med bil. Den nämner också A-7 och AP-7, som leder till Málagas flygplats.')
a('Central <em>Estepona</em>', 'Centro de <em>Estepona</em>', 'Centre d’<em>Estepona</em>', 'Zentrum von <em>Estepona</em>',
  'Центр <em>Эстепоны</em>', 'وسط <em>إستيبونا</em>', 'Centrum van <em>Estepona</em>', 'Centrum <em>Estepony</em>',
  'Sentrum av <em>Estepona</em>', 'Centrala <em>Estepona</em>')
a('Punta Plata beach', 'Playa de Punta Plata', 'Plage de Punta Plata', 'Strand Punta Plata', 'Пляж Пунта-Плата',
  'شاطئ بونتا بلاتا', 'Strand van Punta Plata', 'Plaża Punta Plata', 'Stranden Punta Plata', 'Stranden Punta Plata')
a('Padrón beach', 'Playa del Padrón', 'Plage du Padrón', 'Strand El Padrón', 'Пляж Падрон', 'شاطئ إل بادرون',
  'Strand van El Padrón', 'Plaża El Padrón', 'Stranden El Padrón', 'Stranden El Padrón')

# ---------------------------------------------------------------- purchase
a('The documents we hold give prices and no payment terms. We confirm the current terms in writing before you reserve.',
  'Los documentos que tenemos dan precios pero no condiciones de pago. Confirmamos por escrito las condiciones actuales antes de que reserve.',
  'Les documents dont nous disposons donnent des prix mais aucune condition de paiement. Nous confirmons par écrit les conditions en vigueur avant votre réservation.',
  'Die uns vorliegenden Dokumente nennen Preise, aber keine Zahlungsbedingungen. Wir bestätigen die aktuellen Bedingungen schriftlich, bevor Sie reservieren.',
  'В имеющихся у нас документах есть цены, но нет условий оплаты. Перед бронированием мы письменно подтверждаем актуальные условия.',
  'تتضمن الوثائق التي بحوزتنا الأسعار دون شروط الدفع. ونؤكد كتابةً الشروط الحالية قبل أن تحجزوا.',
  'De documenten die wij hebben geven prijzen en geen betalingsvoorwaarden. Wij bevestigen de actuele voorwaarden schriftelijk voordat u reserveert.',
  'Posiadane przez nas dokumenty podają ceny, ale nie warunki płatności. Przed rezerwacją potwierdzamy na piśmie aktualne warunki.',
  'Dokumentene vi har oppgir priser, men ingen betalingsvilkår. Vi bekrefter gjeldende vilkår skriftlig før dere reserverer.',
  'De dokument vi har anger priser men inga betalningsvillkor. Vi bekräftar gällande villkor skriftligen innan ni reserverar.')
a('No document we hold gives a reservation amount or a payment schedule, so we ask the developer and put the answer in writing before you reserve.',
  'Ningún documento que tenemos da un importe de reserva ni un calendario de pagos, por lo que lo preguntamos al promotor y ponemos la respuesta por escrito antes de que reserve.',
  'Aucun document dont nous disposons ne donne de montant de réservation ni d’échéancier de paiement ; nous interrogeons donc le promoteur et mettons la réponse par écrit avant votre réservation.',
  'Kein uns vorliegendes Dokument nennt einen Reservierungsbetrag oder einen Zahlungsplan; daher fragen wir beim Bauträger nach und halten die Antwort schriftlich fest, bevor Sie reservieren.',
  'Ни в одном из имеющихся у нас документов нет суммы бронирования или графика платежей, поэтому мы спрашиваем застройщика и фиксируем ответ письменно до вашего бронирования.',
  'لا تذكر أي وثيقة بحوزتنا مبلغ الحجز ولا جدول الدفعات، لذلك نسأل المطوّر ونثبّت الجواب كتابةً قبل أن تحجزوا.',
  'Geen enkel document dat wij hebben noemt een reserveringsbedrag of een betalingsschema; daarom vragen wij het de ontwikkelaar na en leggen wij het antwoord schriftelijk vast voordat u reserveert.',
  'Żaden z posiadanych przez nas dokumentów nie podaje kwoty rezerwacji ani harmonogramu płatności, dlatego pytamy dewelopera i potwierdzamy odpowiedź na piśmie przed rezerwacją.',
  'Ingen av dokumentene vi har oppgir et reservasjonsbeløp eller en betalingsplan, så vi spør utbyggeren og får svaret skriftlig før dere reserverer.',
  'Inget dokument vi har anger ett reservationsbelopp eller en betalningsplan, så vi frågar exploatören och får svaret skriftligt innan ni reserverar.')
a('The price list shows prices without IVA and states the rate as 10%. The prices on this page are the developer’s net figures, and IVA is not added to them.',
  'La lista de precios muestra los precios sin IVA e indica el tipo del 10%. Los precios de esta página son las cifras netas del promotor, y no se les suma el IVA.',
  'La liste de prix présente les prix hors TVA et indique un taux de 10 %. Les prix de cette page sont les montants nets du promoteur, auxquels la TVA n’est pas ajoutée.',
  'Die Preisliste weist die Preise ohne MwSt. aus und nennt einen Satz von 10 %. Die Preise auf dieser Seite sind die Nettobeträge des Bauträgers; die MwSt. wird nicht aufgeschlagen.',
  'В прайс-листе цены указаны без НДС, ставка — 10 %. Цены на этой странице — это нетто-цены застройщика, НДС к ним не добавлен.',
  'تعرض قائمة الأسعار الأسعار دون ضريبة القيمة المضافة وتحدد نسبتها بـ 10%. والأسعار في هذه الصفحة هي أرقام المطوّر الصافية، ولا تُضاف إليها ضريبة القيمة المضافة.',
  'De prijslijst toont de prijzen zonder btw en geeft het tarief aan als 10%. De prijzen op deze pagina zijn de nettobedragen van de ontwikkelaar; er wordt geen btw bij opgeteld.',
  'Cennik podaje ceny bez VAT i wskazuje stawkę 10%. Ceny na tej stronie to kwoty netto dewelopera, do których nie dodano VAT.',
  'Prislisten viser prisene uten mva og oppgir satsen til 10 %. Prisene på denne siden er utbyggerens nettobeløp, og mva er ikke lagt til.',
  'Prislistan visar priserna utan IVA (spansk moms) och anger satsen till 10 %. Priserna på den här sidan är exploatörens nettobelopp, och IVA har inte lagts till.')
a('Each of the six listed homes comes with a garage space and a storage room, and home 1ºA with a private pool. The furniture shown in the images is not included.',
  'Cada una de las seis viviendas a la venta incluye plaza de garaje y trastero, y la 1ºA además piscina privada. El mobiliario que aparece en las imágenes no está incluido.',
  'Chacun des six logements annoncés comprend une place de garage et une cave, et le 1ºA une piscine privée. Le mobilier présenté sur les images n’est pas inclus.',
  'Jede der sechs gelisteten Wohnungen umfasst einen Garagenstellplatz und einen Abstellraum, die Wohnung 1ºA zusätzlich einen privaten Pool. Die auf den Bildern gezeigten Möbel sind nicht enthalten.',
  'К каждой из шести квартир в продаже прилагаются место в гараже и кладовая, а к квартире 1ºA — ещё и частный бассейн. Мебель, показанная на изображениях, в стоимость не входит.',
  'يشمل كل مسكن من المساكن الستة المعروضة موقفًا في المرآب وغرفة تخزين، ويشمل المسكن 1ºA مسبحًا خاصًا أيضًا. والأثاث الظاهر في الصور غير مشمول.',
  'Elk van de zes aangeboden woningen heeft een garageplaats en een berging, en woning 1ºA ook een privézwembad. De meubels op de beelden zijn niet inbegrepen.',
  'Każde z sześciu oferowanych mieszkań ma miejsce garażowe i komórkę lokatorską, a mieszkanie 1ºA także prywatny basen. Meble widoczne na wizualizacjach nie są wliczone w cenę.',
  'Hver av de seks annonserte boligene har garasjeplass og bod, og bolig 1ºA også eget basseng. Møblene som vises på bildene er ikke inkludert.',
  'Var och en av de sex listade bostäderna har en garageplats och ett förråd, och bostad 1ºA även en egen pool. Möblerna som visas på bilderna ingår inte.')
a('Other costs', 'Otros gastos', 'Autres frais', 'Weitere Kosten', 'Прочие расходы', 'مصاريف أخرى', 'Overige kosten',
  'Pozostałe koszty', 'Andre kostnader', 'Övriga kostnader')
a('The price list does not give the other purchase costs, so Nueva Living confirms them in writing.',
  'La lista de precios no indica los demás gastos de compra, por lo que Nueva Living los confirma por escrito.',
  'La liste de prix n’indique pas les autres frais d’achat ; Nueva Living les confirme donc par écrit.',
  'Die Preisliste nennt die übrigen Kaufnebenkosten nicht, daher bestätigt Nueva Living sie schriftlich.',
  'В прайс-листе нет остальных расходов на покупку, поэтому Nueva Living подтверждает их письменно.',
  'لا تذكر قائمة الأسعار مصاريف الشراء الأخرى، لذلك تؤكدها Nueva Living كتابةً.',
  'De prijslijst geeft de overige aankoopkosten niet aan, dus bevestigt Nueva Living ze schriftelijk.',
  'Cennik nie podaje pozostałych kosztów zakupu, dlatego Nueva Living potwierdza je na piśmie.',
  'Prislisten oppgir ikke de øvrige kjøpskostnadene, så Nueva Living bekrefter dem skriftlig.',
  'Prislistan anger inte de övriga köpkostnaderna, så Nueva Living bekräftar dem skriftligen.')

# ---------------------------------------------------------------- what we check
a('The documents we hold do not say whether the building licence has been granted or whether the works have started, so we ask for the licence and for the guarantee that covers amounts paid on account.',
  'Los documentos que tenemos no dicen si se ha concedido la licencia de obras ni si las obras han comenzado, por lo que pedimos la licencia y la garantía que cubre las cantidades entregadas a cuenta.',
  'Les documents dont nous disposons ne disent pas si le permis de construire a été accordé ni si les travaux ont commencé ; nous demandons donc le permis et la garantie qui couvre les sommes versées en acompte.',
  'Die uns vorliegenden Dokumente sagen nicht, ob die Baugenehmigung erteilt wurde und ob die Bauarbeiten begonnen haben; daher fragen wir die Genehmigung an, ebenso die Garantie, die geleistete Anzahlungen absichert.',
  'В имеющихся у нас документах не сказано, получено ли разрешение на строительство и начаты ли работы, поэтому мы запрашиваем разрешение и гарантию, покрывающую суммы, внесённые авансом.',
  'لا تبيّن الوثائق التي بحوزتنا ما إذا كانت رخصة البناء قد صدرت أو ما إذا كانت الأعمال قد بدأت، لذلك نطلب الرخصة والضمان الذي يغطي المبالغ المدفوعة مقدمًا.',
  'De documenten die wij hebben, geven niet aan of de bouwvergunning is verleend of of de werken zijn gestart; daarom vragen wij de vergunning op, en de garantie die vooruitbetaalde bedragen dekt.',
  'Posiadane przez nas dokumenty nie podają, czy pozwolenie na budowę zostało wydane ani czy prace się rozpoczęły, dlatego prosimy o pozwolenie oraz o gwarancję obejmującą wpłacone zaliczki.',
  'Dokumentene vi har sier ikke om byggetillatelsen er gitt eller om byggearbeidene er startet, så vi ber om tillatelsen og om garantien som dekker beløp betalt på forhånd.',
  'De dokument vi har anger inte om bygglovet har beviljats eller om byggarbetena har påbörjats, så vi ber om bygglovet och om garantin som täcker belopp som betalats i förskott.')
a('No document we hold gives a delivery date, so we ask for the contractual date and put it in writing.',
  'Ningún documento que tenemos da una fecha de entrega, por lo que pedimos la fecha contractual y la ponemos por escrito.',
  'Aucun document dont nous disposons ne donne de date de livraison ; nous demandons donc la date contractuelle et la mettons par écrit.',
  'Kein uns vorliegendes Dokument nennt einen Übergabetermin, daher fragen wir das vertragliche Datum an und halten es schriftlich fest.',
  'Ни в одном из имеющихся у нас документов не указан срок сдачи, поэтому мы запрашиваем договорную дату и фиксируем её письменно.',
  'لا تذكر أي من الوثائق التي بحوزتنا موعد تسليم، لذلك نطلب التاريخ التعاقدي ونثبّته كتابةً.',
  'Geen van de documenten die wij hebben noemt een opleveringsdatum, dus vragen wij de contractuele datum op en leggen die schriftelijk vast.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu oddania, dlatego prosimy o termin umowny i potwierdzamy go na piśmie.',
  'Ingen av dokumentene vi har oppgir en overleveringsdato, så vi ber om den kontraktsfestede datoen og får den skriftlig.',
  'Inget av de dokument vi har anger ett tillträdesdatum, så vi ber om det avtalade datumet och får det skriftligen.')
a('The garage and storage numbers', 'Los números de garaje y trastero', 'Les numéros de garage et de cave',
  'Die Nummern der Stellplätze und Abstellräume', 'Номера мест в гараже и кладовых', 'أرقام المواقف وغرف التخزين',
  'De nummers van garageplaatsen en bergingen', 'Numery miejsc garażowych i komórek', 'Numrene på garasjeplasser og boder',
  'Numren på garageplatser och förråd')
a('The price list and the plans number the garage spaces and storage rooms differently. For Bajo A the list gives garage 1 and storage 5 and the plan gives parking space 9 and storage room 11; for 1ºA the list gives 9 and 11 and the plan 10 and 12. All six listed homes differ in the same way. Both documents give every home a garage space and a storage room, and we confirm which ones come with the home you choose.',
  'La lista de precios y los planos numeran de forma distinta las plazas de garaje y los trasteros. Para Bajo A, la lista da garaje 1 y trastero 5, y el plano da plaza de parking 9 y trastero 11; para 1ºA, la lista da 9 y 11 y el plano 10 y 12. Las seis viviendas a la venta difieren del mismo modo. Ambos documentos dan a cada vivienda una plaza de garaje y un trastero, y confirmamos cuáles corresponden a la vivienda que usted elija.',
  'La liste de prix et les plans numérotent différemment les places de garage et les caves. Pour Bajo A, la liste donne garage 1 et cave 5, et le plan donne place de parking 9 et cave 11 ; pour 1ºA, la liste donne 9 et 11 et le plan 10 et 12. Les six logements annoncés diffèrent de la même façon. Les deux documents attribuent à chaque logement une place de garage et une cave, et nous confirmons lesquelles accompagnent le logement que vous choisissez.',
  'Die Preisliste und die Pläne nummerieren die Garagenstellplätze und Abstellräume unterschiedlich. Für Bajo A nennt die Liste Garage 1 und Abstellraum 5, der Plan Stellplatz 9 und Abstellraum 11; für 1ºA nennt die Liste 9 und 11, der Plan 10 und 12. Alle sechs gelisteten Wohnungen weichen auf dieselbe Weise ab. Beide Dokumente ordnen jeder Wohnung einen Garagenstellplatz und einen Abstellraum zu, und wir bestätigen, welche zur von Ihnen gewählten Wohnung gehören.',
  'В прайс-листе и на планах места в гараже и кладовые пронумерованы по-разному. Для Bajo A в прайс-листе указаны гараж 1 и кладовая 5, а на плане — парковочное место 9 и кладовая 11; для 1ºA в прайс-листе 9 и 11, на плане 10 и 12. Все шесть квартир в продаже расходятся таким же образом. В обоих документах к каждой квартире относятся место в гараже и кладовая, и мы уточняем, какие именно относятся к выбранной вами квартире.',
  'تُرقّم قائمة الأسعار والمخططات مواقف المرآب وغرف التخزين بشكل مختلف. ففي Bajo A تذكر القائمة المرآب 1 وغرفة التخزين 5، ويذكر المخطط موقف السيارات 9 وغرفة التخزين 11؛ وفي 1ºA تذكر القائمة 9 و11 ويذكر المخطط 10 و12. وتختلف المساكن الستة المعروضة جميعها بالطريقة نفسها. وتخصص الوثيقتان لكل مسكن موقفًا في المرآب وغرفة تخزين، ونؤكد أيّ منها يأتي مع المسكن الذي تختارونه.',
  'De prijslijst en de plattegronden nummeren de garageplaatsen en bergingen verschillend. Voor Bajo A geeft de lijst garage 1 en berging 5, en de plattegrond parkeerplaats 9 en berging 11; voor 1ºA geeft de lijst 9 en 11 en de plattegrond 10 en 12. Alle zes aangeboden woningen wijken op dezelfde manier af. Beide documenten kennen elke woning een garageplaats en een berging toe, en wij bevestigen welke bij de woning horen die u kiest.',
  'Cennik i rzuty numerują miejsca garażowe i komórki lokatorskie inaczej. Dla Bajo A cennik podaje garaż 1 i komórkę 5, a rzut miejsce parkingowe 9 i komórkę 11; dla 1ºA cennik podaje 9 i 11, a rzut 10 i 12. Wszystkie sześć oferowanych mieszkań różni się w ten sam sposób. Oba dokumenty przypisują każdemu mieszkaniu miejsce garażowe i komórkę lokatorską, a my potwierdzamy, które należą do mieszkania, które Państwo wybiorą.',
  'Prislisten og plantegningene nummererer garasjeplassene og bodene ulikt. For Bajo A oppgir listen garasje 1 og bod 5, og plantegningen parkeringsplass 9 og bod 11; for 1ºA oppgir listen 9 og 11, og plantegningen 10 og 12. Alle de seks annonserte boligene avviker på samme måte. Begge dokumentene gir hver bolig en garasjeplass og en bod, og vi bekrefter hvilke som følger med boligen dere velger.',
  'Prislistan och planritningarna numrerar garageplatserna och förråden olika. För Bajo A anger listan garage 1 och förråd 5, och planritningen parkeringsplats 9 och förråd 11; för 1ºA anger listan 9 och 11 och planritningen 10 och 12. Alla sex listade bostäder avviker på samma sätt. Båda dokumenten ger varje bostad en garageplats och ett förråd, och vi bekräftar vilka som hör till den bostad ni väljer.')
a('The bathrooms', 'Los baños', 'Les salles de bains', 'Die Bäder', 'Ванные комнаты', 'الحمامات', 'De badkamers', 'Łazienki',
  'Badene', 'Badrummen')
a('The dossier says that each home has two bathrooms, one of them en suite, but the plan and the price list give Bajo A one bathroom. We go by the plans and confirm the layout of the home you choose.',
  'El dosier dice que cada vivienda tiene dos baños, uno de ellos en suite, pero el plano y la lista de precios dan un baño para Bajo A. Nos guiamos por los planos y confirmamos la distribución de la vivienda que usted elija.',
  'Le dossier indique que chaque logement a deux salles de bains, dont une en suite, mais le plan et la liste de prix donnent une salle de bains à Bajo A. Nous nous fions aux plans et confirmons la distribution du logement que vous choisissez.',
  'Das Dossier sagt, dass jede Wohnung zwei Bäder hat, eines davon en suite, aber der Plan und die Preisliste geben Bajo A ein Bad. Wir halten uns an die Pläne und bestätigen den Grundriss der von Ihnen gewählten Wohnung.',
  'В досье сказано, что в каждой квартире две ванные комнаты, одна из них при спальне, но на плане и в прайс-листе у Bajo A одна ванная комната. Мы ориентируемся на планы и уточняем планировку выбранной вами квартиры.',
  'يذكر الملف أن لكل مسكن حمامين، أحدهما داخل غرفة النوم، لكن المخطط وقائمة الأسعار يعطيان Bajo A حمامًا واحدًا. ونعتمد على المخططات ونؤكد توزيع المسكن الذي تختارونه.',
  'Het dossier zegt dat elke woning twee badkamers heeft, waarvan een en suite, maar de plattegrond en de prijslijst geven Bajo A één badkamer. Wij gaan uit van de plattegronden en bevestigen de indeling van de woning die u kiest.',
  'Dossier podaje, że każde mieszkanie ma dwie łazienki, w tym jedną przy sypialni, ale rzut i cennik podają dla Bajo A jedną łazienkę. Kierujemy się rzutami i potwierdzamy układ mieszkania, które Państwo wybiorą.',
  'Dossieret sier at hver bolig har to bad, ett av dem en suite, men plantegningen og prislisten gir Bajo A ett bad. Vi legger plantegningene til grunn og bekrefter planløsningen for boligen dere velger.',
  'Dossiern anger att varje bostad har två badrum, ett av dem en suite, men planritningen och prislistan anger ett badrum för Bajo A. Vi går efter planritningarna och bekräftar planlösningen för den bostad ni väljer.')

# ---------------------------------------------------------------- availability
a('6 of 10 homes <em>currently available</em>', '6 de 10 viviendas <em>a la venta actualmente</em>',
  '6 logements sur 10 <em>actuellement annoncés</em>', '6 von 10 Wohnungen <em>derzeit verfügbar</em>',
  '6 из 10 квартир <em>сейчас в продаже</em>', '6 من أصل 10 مساكن <em>معروضة حاليًا</em>',
  '6 van de 10 woningen <em>momenteel beschikbaar</em>', '6 z 10 mieszkań <em>obecnie dostępnych</em>',
  '6 av 10 boliger <em>ledige nå</em>', '6 av 10 bostäder <em>lediga just nu</em>')
a('Six apartments are listed with a price: two on the ground floor and four on the first floor. The other four homes are marked reserved on the developer’s price list of September 2026 and are not listed here. The prices exclude IVA, and we confirm availability and price before any reservation.',
  'Figuran seis apartamentos con precio: dos en planta baja y cuatro en la primera planta. Las otras cuatro viviendas figuran como reservadas en la lista de precios del promotor de septiembre de 2026 y no se muestran aquí. Los precios no incluyen IVA; confirmamos la disponibilidad y el precio antes de cualquier reserva.',
  'Six appartements sont annoncés avec un prix : deux au rez-de-chaussée et quatre au premier étage. Les quatre autres logements sont indiqués comme réservés dans la liste de prix du promoteur de septembre 2026 et ne sont pas présentés ici. Les prix s’entendent hors TVA ; nous confirmons la disponibilité et le prix avant toute réservation.',
  'Sechs Wohnungen sind mit Preis gelistet: zwei im Erdgeschoss und vier im ersten Obergeschoss. Die übrigen vier Wohnungen sind in der Preisliste des Bauträgers vom September 2026 als reserviert gekennzeichnet und hier nicht aufgeführt. Die Preise verstehen sich zuzüglich MwSt.; Verfügbarkeit und Preis bestätigen wir vor jeder Reservierung.',
  'Шесть квартир указаны с ценой: две на первом этаже и четыре на втором. Остальные четыре квартиры отмечены как забронированные в прайс-листе застройщика за сентябрь 2026 года и здесь не приведены. Цены не включают НДС; наличие и цену мы подтверждаем до любого бронирования.',
  'تُعرض ست شقق بسعر: اثنتان في الطابق الأرضي وأربع في الطابق الأول. أما المساكن الأربعة الأخرى فمُدرجة على أنها محجوزة في قائمة أسعار المطوّر لشهر سبتمبر 2026 ولا تظهر هنا. والأسعار لا تشمل ضريبة القيمة المضافة، ونؤكد التوفر والسعر قبل أي حجز.',
  'Zes appartementen staan met een prijs vermeld: twee op de begane grond en vier op de eerste verdieping. De overige vier woningen staan in de prijslijst van de ontwikkelaar van september 2026 als gereserveerd aangemerkt en worden hier niet getoond. De prijzen zijn exclusief btw; wij bevestigen beschikbaarheid en prijs vóór elke reservering.',
  'Sześć mieszkań ma podaną cenę: dwa na parterze i cztery na pierwszym piętrze. Pozostałe cztery są w cenniku dewelopera z września 2026 r. oznaczone jako zarezerwowane i nie są tu wymienione. Ceny nie zawierają VAT; dostępność i cenę potwierdzamy przed każdą rezerwacją.',
  'Seks leiligheter er annonsert med pris: to i første etasje og fire i andre etasje. De fire andre boligene er markert som reservert i utbyggerens prisliste fra september 2026 og vises ikke her. Prisene er eksklusive mva; vi bekrefter tilgjengelighet og pris før enhver reservasjon.',
  'Sex lägenheter är listade med pris: två på bottenvåningen och fyra på första våningen. De fyra övriga bostäderna är markerade som reserverade i exploatörens prislista från september 2026 och visas inte här. Priserna är exklusive IVA (spansk moms); vi bekräftar tillgänglighet och pris före varje reservation.')
a('Prices, bedrooms, bathrooms, areas, garage spaces and storage rooms are transcribed from the developer’s price list of September 2026, which lists 10 homes: the six shown here carry a price and four are marked reserved. The list states that the prices exclude 10% IVA. For these six homes the interior and built areas on the list match those on the developer’s plans, and the terrace shown for 1ºA is the patio of the plan. The list and the plans number the garage spaces and storage rooms differently, so those numbers are not shown.',
  'Los precios, los dormitorios, los baños, las superficies, las plazas de garaje y los trasteros están transcritos de la lista de precios del promotor de septiembre de 2026, que recoge 10 viviendas: las seis que se muestran aquí llevan precio y cuatro figuran como reservadas. La lista indica que los precios no incluyen el 10% de IVA. Para estas seis viviendas, las superficies interiores y construidas de la lista coinciden con las de los planos del promotor, y la terraza que figura para 1ºA es el patio del plano. La lista y los planos numeran de forma distinta las plazas de garaje y los trasteros, por lo que esos números no se muestran.',
  'Les prix, les chambres, les salles de bains, les surfaces, les places de garage et les caves sont transcrits de la liste de prix du promoteur de septembre 2026, qui recense 10 logements : les six présentés ici ont un prix et quatre sont indiqués comme réservés. La liste précise que les prix s’entendent hors TVA de 10 %. Pour ces six logements, les surfaces intérieures et construites de la liste concordent avec celles des plans du promoteur, et la terrasse indiquée pour 1ºA est le patio du plan. La liste et les plans numérotent différemment les places de garage et les caves ; ces numéros ne sont donc pas indiqués.',
  'Preise, Schlafzimmer, Bäder, Flächen, Garagenstellplätze und Abstellräume sind der Preisliste des Bauträgers vom September 2026 entnommen, die 10 Wohnungen aufführt: Die hier gezeigten sechs tragen einen Preis, vier sind als reserviert gekennzeichnet. Die Liste weist die Preise zuzüglich 10% MwSt. aus. Für diese sechs Wohnungen stimmen die Innen- und die bebauten Flächen der Liste mit denen der Pläne des Bauträgers überein, und die für 1ºA angegebene Terrasse ist das Patio des Plans. Die Liste und die Pläne nummerieren die Garagenstellplätze und Abstellräume unterschiedlich, daher werden diese Nummern nicht angegeben.',
  'Цены, количество спален и ванных комнат, площади, места в гараже и кладовые перенесены из прайс-листа застройщика за сентябрь 2026 года, в котором указаны 10 квартир: шесть показанных здесь имеют цену, четыре отмечены как забронированные. В прайс-листе сказано, что цены не включают НДС 10 %. По этим шести квартирам внутренняя площадь и площадь застройки в прайс-листе совпадают с данными на планах застройщика, а терраса, указанная для 1ºA, — это патио с плана. В прайс-листе и на планах места в гараже и кладовые пронумерованы по-разному, поэтому эти номера не приводятся.',
  'الأسعار وغرف النوم والحمامات والمساحات ومواقف المرآب وغرف التخزين منقولة من قائمة أسعار المطوّر لشهر سبتمبر 2026 التي تدرج 10 مساكن: الستة المعروضة هنا لها سعر وأربعة محجوزة. وتنص القائمة على أن الأسعار لا تشمل ضريبة القيمة المضافة 10%. وبالنسبة إلى هذه المساكن الستة، تتطابق المساحات الداخلية والمبنية في القائمة مع مخططات المطوّر، والتراس المذكور للمسكن 1ºA هو الفناء الوارد في المخطط. وتُرقّم القائمة والمخططات مواقف المرآب وغرف التخزين بشكل مختلف، لذلك لا تُذكر هذه الأرقام.',
  'Prijzen, slaapkamers, badkamers, oppervlakten, garageplaatsen en bergingen zijn overgenomen uit de prijslijst van de ontwikkelaar van september 2026, die 10 woningen vermeldt: de zes die hier staan hebben een prijs en vier zijn als gereserveerd aangemerkt. De lijst vermeldt dat de prijzen exclusief 10% btw zijn. Voor deze zes woningen komen de binnen- en bebouwde oppervlakten op de lijst overeen met die op de plattegronden van de ontwikkelaar, en het terras dat voor 1ºA wordt genoemd is de patio van de plattegrond. De lijst en de plattegronden nummeren de garageplaatsen en bergingen verschillend, daarom worden die nummers niet getoond.',
  'Ceny, liczba sypialni i łazienek, powierzchnie, miejsca garażowe i komórki lokatorskie zostały przepisane z cennika dewelopera z września 2026 r., który wymienia 10 mieszkań: sześć pokazanych tu ma podaną cenę, a cztery są oznaczone jako zarezerwowane. Cennik wskazuje, że ceny nie zawierają 10% VAT. Dla tych sześciu mieszkań powierzchnie wewnętrzne i zabudowy z cennika zgadzają się z podanymi na planach dewelopera, a taras podany dla 1ºA to patio z rzutu. Cennik i rzuty numerują miejsca garażowe i komórki lokatorskie inaczej, dlatego tych numerów nie podajemy.',
  'Priser, soverom, bad, arealer, garasjeplasser og boder er hentet fra utbyggerens prisliste fra september 2026, som oppfører 10 boliger: de seks som vises her har en pris, og fire er markert som reservert. Listen oppgir at prisene er eksklusive 10 % mva. For disse seks boligene stemmer innvendig areal og bebygd areal på listen med utbyggerens plantegninger, og terrassen som er oppgitt for 1ºA er patioet på plantegningen. Listen og plantegningene nummererer garasjeplassene og bodene ulikt, så disse numrene vises ikke.',
  'Priser, sovrum, badrum, ytor, garageplatser och förråd är hämtade från exploatörens prislista från september 2026, som upptar 10 bostäder: de sex som visas här har ett pris och fyra är markerade som reserverade. Listan anger att priserna är exklusive 10 % IVA (spansk moms). För dessa sex bostäder stämmer den invändiga ytan och byggytan på listan med exploatörens planritningar, och terrassen som anges för 1ºA är pation på planritningen. Listan och planritningarna numrerar garageplatserna och förråden olika, så de numren visas inte.')

# ---------------------------------------------------------------- next steps
a('The plans of the homes that interest you, the specification and the price list.',
  'Los planos de las viviendas que le interesen, la especificación de calidades y la lista de precios.',
  'Les plans des logements qui vous intéressent, le descriptif de qualité et la liste de prix.',
  'Die Grundrisse der Wohnungen, die Sie interessieren, die Baubeschreibung und die Preisliste.',
  'Планировки интересующих вас квартир, спецификация и прайс-лист.',
  'مخططات المساكن التي تهمك والمواصفات وقائمة الأسعار.',
  'De plattegronden van de woningen die u interesseren, de specificatie en de prijslijst.',
  'Rzuty lokali, które Państwa interesują, specyfikacja i cennik.',
  'Plantegningene til boligene dere er interessert i, spesifikasjonen og prislisten.',
  'Planritningarna för de bostäder som intresserar er, beskrivningen och prislistan.')
a('See the site and the old town with us, and the plans against the building.',
  'Vea el emplazamiento y el casco antiguo con nosotros, y compare los planos con el edificio.',
  'Visitez le site et la vieille ville avec nous, et confrontez les plans au bâtiment.',
  'Sehen Sie sich mit uns das Grundstück und die Altstadt an und vergleichen Sie die Pläne mit dem Gebäude.',
  'Посмотрите участок и старый город вместе с нами и сравните планы со зданием.',
  'شاهد الموقع والبلدة القديمة معنا، وقارن المخططات بالمبنى.',
  'Bekijk de locatie en de oude stad samen met ons en leg de plattegronden naast het gebouw.',
  'Zobaczcie Państwo z nami miejsce budowy i stare miasto oraz porównajcie rzuty z budynkiem.',
  'Se tomten og gamlebyen sammen med oss, og sammenlign plantegningene med bygget.',
  'Se platsen och gamla stan tillsammans med oss, och jämför planritningarna med byggnaden.')
a('The reservation, the payment schedule and the contract are confirmed with the developer in writing before you commit.',
  'La reserva, el calendario de pagos y el contrato se confirman por escrito con el promotor antes de que se comprometa.',
  'La réservation, l’échéancier de paiement et le contrat sont confirmés par écrit avec le promoteur avant votre engagement.',
  'Reservierung, Zahlungsplan und Vertrag werden mit dem Bauträger schriftlich bestätigt, bevor Sie sich binden.',
  'Бронирование, график платежей и договор письменно подтверждаются у застройщика до принятия вами обязательств.',
  'يُؤكَّد الحجز وجدول الدفعات والعقد كتابةً مع المطوّر قبل أن تلتزموا.',
  'De reservering, het betalingsschema en het contract worden schriftelijk met de ontwikkelaar bevestigd voordat u zich vastlegt.',
  'Rezerwacja, harmonogram płatności i umowa są potwierdzane z deweloperem na piśmie, zanim Państwo się zobowiążą.',
  'Reservasjonen, betalingsplanen og kontrakten bekreftes skriftlig med utbyggeren før dere forplikter dere.',
  'Reservationen, betalningsplanen och avtalet bekräftas skriftligen med exploatören innan ni binder er.')
a('See the <em>building and the old town</em>', 'Vea <em>el edificio y el casco antiguo</em>',
  'Découvrez <em>l’immeuble et la vieille ville</em>', 'Erleben Sie <em>das Gebäude und die Altstadt</em>',
  'Осмотрите <em>здание и старый город</em>', 'شاهد <em>المبنى والبلدة القديمة</em>',
  'Bekijk <em>het gebouw en de oude stad</em>', 'Wizyta w <em>budynku i w starym mieście</em>',
  'Se <em>bygget og gamlebyen</em>', 'Se <em>byggnaden och gamla stan</em>')
a('The images show the building as designed, so a visit is about the location, the plans and what the developer can show on site.',
  'Las imágenes muestran el edificio tal como está proyectado, por lo que la visita trata de la ubicación, los planos y lo que el promotor pueda mostrar sobre el terreno.',
  'Les images montrent l’immeuble tel qu’il est conçu ; la visite porte donc sur l’emplacement, les plans et ce que le promoteur peut montrer sur place.',
  'Die Bilder zeigen das Gebäude, wie es geplant ist; bei einer Besichtigung geht es daher um die Lage, die Pläne und das, was der Bauträger vor Ort zeigen kann.',
  'На изображениях показано здание по проекту, поэтому просмотр посвящён расположению, планам и тому, что застройщик может показать на месте.',
  'تُظهر الصور المبنى كما صُمّم، لذلك تتناول الزيارة الموقع والمخططات وما يستطيع المطوّر عرضه في الموقع.',
  'De beelden tonen het gebouw zoals het is ontworpen, dus een bezoek gaat over de ligging, de plattegronden en wat de ontwikkelaar ter plaatse kan laten zien.',
  'Wizualizacje pokazują budynek w kształcie zaprojektowanym, dlatego wizyta dotyczy lokalizacji, rzutów i tego, co deweloper może pokazać na miejscu.',
  'Bildene viser bygget slik det er tegnet, så en visning handler om beliggenheten, plantegningene og det utbyggeren kan vise på stedet.',
  'Bilderna visar byggnaden som den är ritad, så ett besök handlar om läget, planritningarna och vad exploatören kan visa på plats.')
a('See where the building stands and the stage it has reached.', 'Vea dónde se levanta el edificio y el estado en que se encuentra.',
  'Découvrez l’emplacement de l’immeuble et son état d’avancement.', 'Sehen Sie, wo das Gebäude steht und welchen Stand es erreicht hat.',
  'Посмотрите, где стоит здание и на какой стадии оно находится.', 'شاهد موقع المبنى والمرحلة التي بلغها.',
  'Bekijk waar het gebouw staat en welke stand het heeft bereikt.', 'Zobaczcie Państwo, gdzie stoi budynek i na jakim jest etapie.',
  'Se hvor bygget ligger og hvor langt det har kommet.', 'Se var byggnaden ligger och hur långt den har kommit.')
a('We walk to the old town and the marina with you and time it.', 'Caminamos con usted hasta el casco antiguo y el puerto deportivo y medimos el tiempo.',
  'Nous allons à pied avec vous jusqu’à la vieille ville et au port de plaisance et chronométrons le trajet.',
  'Wir gehen mit Ihnen zur Altstadt und zum Yachthafen und stoppen die Zeit.',
  'Мы идём с вами пешком до старого города и порта и засекаем время.', 'نمشي معكم إلى البلدة القديمة والمرسى ونحسب الوقت.',
  'We lopen met u naar de oude stad en de jachthaven en meten de tijd.', 'Idziemy z Państwem pieszo do starego miasta i portu jachtowego i mierzymy czas.',
  'Vi går med dere til gamlebyen og småbåthavnen og tar tiden.', 'Vi går med er till gamla stan och småbåtshamnen och tar tiden.')
a('Ask about <em>Paraíso de Azahar</em>', 'Pregunte por <em>Paraíso de Azahar</em>', 'Renseignez-vous sur <em>Paraíso de Azahar</em>',
  'Fragen Sie nach <em>Paraíso de Azahar</em>', 'Узнайте больше о <em>Paraíso de Azahar</em>', 'استفسروا عن <em>Paraíso de Azahar</em>',
  'Vraag naar <em>Paraíso de Azahar</em>', 'Proszę zapytać o <em>Paraíso de Azahar</em>', 'Spør om <em>Paraíso de Azahar</em>',
  'Fråga om <em>Paraíso de Azahar</em>')
a('Hello Nueva Living, I would like information about Paraíso de Azahar.',
  'Hola Nueva Living, me gustaría recibir información sobre Paraíso de Azahar.',
  'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Paraíso de Azahar.',
  'Guten Tag Nueva Living, ich hätte gerne Informationen zu Paraíso de Azahar.',
  'Здравствуйте, Nueva Living, я хотел бы получить информацию о Paraíso de Azahar.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Paraíso de Azahar.',
  'Hallo Nueva Living, ik wil graag informatie over Paraíso de Azahar.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Paraíso de Azahar.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Paraíso de Azahar.',
  'Hej Nueva Living, jag vill gärna ha information om Paraíso de Azahar.')

# ---------------------------------------------------------------- faq
a('The building has 10 homes and six are currently listed with a price: one one-bedroom home, three two-bedroom homes and two three-bedroom homes, from EUR 495,000 to EUR 895,000 plus VAT. The other four are marked reserved.',
  'El edificio tiene 10 viviendas y seis figuran actualmente con precio: una de un dormitorio, tres de dos dormitorios y dos de tres dormitorios, de {E495000} a {E895000} más IVA. Las otras cuatro figuran como reservadas.',
  'L’immeuble compte 10 logements et six sont actuellement annoncés avec un prix : un d’une chambre, trois de deux chambres et deux de trois chambres, de {E495000} à {E895000} hors TVA. Les quatre autres sont indiqués comme réservés.',
  'Das Gebäude hat 10 Wohnungen, sechs davon sind derzeit mit Preis gelistet: eine mit einem Schlafzimmer, drei mit zwei und zwei mit drei Schlafzimmern, von {E495000} bis {E895000} zuzüglich MwSt. Die anderen vier sind als reserviert gekennzeichnet.',
  'В доме 10 квартир, шесть из них сейчас указаны с ценой: одна с одной спальней, три с двумя и две с тремя, от {E495000} до {E895000} без НДС. Остальные четыре отмечены как забронированные.',
  'يضم المبنى 10 مساكن، ستة منها معروضة حاليًا بسعر: مسكن بغرفة نوم واحدة وثلاثة بغرفتي نوم واثنان بثلاث غرف نوم، من {E495000} إلى {E895000} دون ضريبة القيمة المضافة. أما الأربعة الأخرى فمُدرجة على أنها محجوزة.',
  'Het gebouw heeft 10 woningen en zes staan momenteel met een prijs vermeld: een met één slaapkamer, drie met twee en twee met drie slaapkamers, van {E495000} tot {E895000} excl. btw. De andere vier zijn als gereserveerd aangemerkt.',
  'Budynek ma 10 mieszkań, a sześć ma obecnie podaną cenę: jedno z jedną sypialnią, trzy z dwiema i dwa z trzema, od {E495000} do {E895000} plus VAT. Pozostałe cztery są oznaczone jako zarezerwowane.',
  'Bygget har 10 boliger, og seks er for tiden annonsert med pris: én med ett soverom, tre med to og to med tre soverom, fra {E495000} til {E895000} pluss mva. De fire andre er markert som reservert.',
  'Byggnaden har 10 bostäder och sex är för närvarande listade med pris: en med ett sovrum, tre med två och två med tre sovrum, från {E495000} till {E895000} plus IVA. De fyra övriga är markerade som reserverade.')
a('No. The price list states that the prices exclude IVA and gives the rate as 10%. The prices on this page are the developer’s net figures, and IVA is not added to them.',
  'No. La lista de precios indica que los precios no incluyen IVA y da el tipo del 10%. Los precios de esta página son las cifras netas del promotor, y no se les suma el IVA.',
  'Non. La liste de prix indique que les prix s’entendent hors TVA et donne un taux de 10 %. Les prix de cette page sont les montants nets du promoteur, auxquels la TVA n’est pas ajoutée.',
  'Nein. Laut Preisliste verstehen sich die Preise zuzüglich MwSt., und sie nennt einen Satz von 10 %. Die Preise auf dieser Seite sind die Nettobeträge des Bauträgers; die MwSt. wird nicht aufgeschlagen.',
  'Нет. В прайс-листе сказано, что цены не включают НДС, ставка — 10 %. Цены на этой странице — нетто-цены застройщика, НДС к ним не добавлен.',
  'لا. تذكر قائمة الأسعار أن الأسعار لا تشمل ضريبة القيمة المضافة وتحدد نسبتها بـ 10%. والأسعار في هذه الصفحة هي أرقام المطوّر الصافية، ولا تُضاف إليها ضريبة القيمة المضافة.',
  'Nee. De prijslijst vermeldt dat de prijzen exclusief btw zijn en geeft het tarief aan als 10%. De prijzen op deze pagina zijn de nettobedragen van de ontwikkelaar; er wordt geen btw bij opgeteld.',
  'Nie. Cennik wskazuje, że ceny nie zawierają VAT, i podaje stawkę 10%. Ceny na tej stronie to kwoty netto dewelopera, do których nie dodano VAT.',
  'Nei. Prislisten oppgir at prisene er eksklusive mva, og oppgir satsen til 10 %. Prisene på denne siden er utbyggerens nettobeløp, og mva er ikke lagt til.',
  'Nej. Prislistan anger att priserna är exklusive IVA (spansk moms) och anger satsen till 10 %. Priserna på den här sidan är exploatörens nettobelopp, och IVA har inte lagts till.')
a('Yes. The price list gives each of the six listed homes a garage space and a storage room, and the garage is reached by a car lift. The specification includes pre-installation for electric-car charging.',
  'Sí. La lista de precios asigna a cada una de las seis viviendas a la venta una plaza de garaje y un trastero, y al garaje se llega con un ascensor para coches. La memoria de calidades incluye la preinstalación de carga para coche eléctrico.',
  'Oui. La liste de prix attribue à chacun des six logements annoncés une place de garage et une cave, et le garage est desservi par un monte-voitures. Le descriptif prévoit le pré-équipement pour la recharge de véhicules électriques.',
  'Ja. Laut Preisliste gehören zu jeder der sechs gelisteten Wohnungen ein Garagenstellplatz und ein Abstellraum, und die Garage wird mit einem Autoaufzug erreicht. Die Baubeschreibung umfasst die Vorinstallation für das Laden von Elektrofahrzeugen.',
  'Да. Согласно прайс-листу, к каждой из шести квартир в продаже прилагаются место в гараже и кладовая, а в гараж ведёт автомобильный лифт. Спецификация включает подготовку к зарядке электромобилей.',
  'نعم. تخصص قائمة الأسعار لكل مسكن من المساكن الستة المعروضة موقفًا في المرآب وغرفة تخزين، ويصل مصعد للسيارات إلى المرآب. وتشمل المواصفات تجهيزًا مسبقًا لشحن السيارات الكهربائية.',
  'Ja. De prijslijst kent elk van de zes aangeboden woningen een garageplaats en een berging toe, en de garage is met een autolift bereikbaar. De specificatie omvat de voorbereiding voor het opladen van elektrische auto’s.',
  'Tak. Zgodnie z cennikiem każde z sześciu oferowanych mieszkań ma miejsce garażowe i komórkę lokatorską, a do garażu prowadzi winda samochodowa. Specyfikacja obejmuje przygotowanie do ładowania pojazdów elektrycznych.',
  'Ja. Prislisten gir hver av de seks annonserte boligene en garasjeplass og en bod, og garasjen nås med bilheis. Spesifikasjonen inkluderer forberedelse for lading av elbil.',
  'Ja. Prislistan ger var och en av de sex listade bostäderna en garageplats och ett förråd, och garaget nås med bilhiss. Beskrivningen inkluderar förberedelse för laddning av elbil.')
a('Does any home have a private pool?', '¿Alguna vivienda tiene piscina privada?', 'Un logement a-t-il une piscine privée ?',
  'Hat eine der Wohnungen einen privaten Pool?', 'Есть ли у какой-либо квартиры частный бассейн?',
  'هل يتوفر مسبح خاص في أي من المساكن؟', 'Heeft een van de woningen een privézwembad?', 'Czy któreś mieszkanie ma prywatny basen?',
  'Har noen av boligene eget basseng?', 'Har någon av bostäderna egen pool?')
a('Of the six listed homes, 1ºA has a private pool and a patio of 38.56 sqm. The four reserved homes on the upper floors are listed with pools too, and are not available.',
  'De las seis viviendas a la venta, la 1ºA tiene piscina privada y un patio de {N38.56} {U}. Las cuatro viviendas reservadas de las plantas superiores también figuran con piscina y no están disponibles.',
  'Parmi les six logements annoncés, le 1ºA a une piscine privée et un patio de {N38.56} {U}. Les quatre logements réservés des étages supérieurs sont aussi indiqués avec une piscine, et ne sont pas disponibles.',
  'Von den sechs gelisteten Wohnungen hat 1ºA einen privaten Pool und ein Patio von {N38.56} {U}. Auch die vier reservierten Wohnungen in den oberen Geschossen sind mit Pools gelistet und nicht verfügbar.',
  'Из шести квартир в продаже частный бассейн и патио {N38.56} {U} есть у 1ºA. Четыре забронированные квартиры на верхних этажах тоже указаны с бассейнами и недоступны.',
  'من بين المساكن الستة المعروضة، للمسكن 1ºA مسبح خاص وفناء بمساحة {N38.56} {U}. والمساكن الأربعة المحجوزة في الطوابق العليا مُدرجة هي أيضًا بمسابح وهي غير متاحة.',
  'Van de zes aangeboden woningen heeft 1ºA een privézwembad en een patio van {N38.56} {U}. De vier gereserveerde woningen op de bovenste verdiepingen staan ook met zwembaden vermeld en zijn niet beschikbaar.',
  'Spośród sześciu oferowanych mieszkań 1ºA ma prywatny basen i patio o powierzchni {N38.56} {U}. Cztery zarezerwowane mieszkania na wyższych kondygnacjach są również wymienione z basenami i nie są dostępne.',
  'Av de seks annonserte boligene har 1ºA eget basseng og et patio på {N38.56} {U}. De fire reserverte boligene i de øvre etasjene er også oppført med basseng, og er ikke tilgjengelige.',
  'Av de sex listade bostäderna har 1ºA egen pool och en patio på {N38.56} {U}. De fyra reserverade bostäderna på de övre våningarna är också listade med pooler och är inte tillgängliga.')

# ---------------------------------------------------------------- the last faq answer and the search-engine strings
a('None of the documents we hold gives a delivery date or the stage of the building. We ask for the contractual date and put it in writing.',
  'Ninguno de los documentos que tenemos da una fecha de entrega ni el estado del edificio. Pedimos la fecha contractual y la ponemos por escrito.',
  'Aucun des documents dont nous disposons ne donne de date de livraison ni l’état d’avancement de l’immeuble. Nous demandons la date contractuelle et la mettons par écrit.',
  'Keines der uns vorliegenden Dokumente nennt einen Übergabetermin oder den Stand des Gebäudes. Wir fragen das vertragliche Datum an und halten es schriftlich fest.',
  'Ни в одном из имеющихся у нас документов не указаны срок сдачи и стадия строительства здания. Мы запрашиваем договорную дату и фиксируем её письменно.',
  'لا تذكر أي من الوثائق التي بحوزتنا موعد تسليم أو مرحلة المبنى. نطلب التاريخ التعاقدي ونثبّته كتابةً.',
  'Geen van de documenten die wij hebben noemt een opleveringsdatum of de stand van het gebouw. Wij vragen de contractuele datum op en leggen die schriftelijk vast.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu oddania ani etapu budowy. Prosimy o termin umowny i potwierdzamy go na piśmie.',
  'Ingen av dokumentene vi har oppgir en overleveringsdato eller hvor langt bygget har kommet. Vi ber om den kontraktsfestede datoen og får den skriftlig.',
  'Inget av de dokument vi har anger ett tillträdesdatum eller hur långt byggnaden har kommit. Vi ber om det avtalade datumet och får det skriftligen.')
a('Paraíso de Azahar - New Apartments in Central Estepona', 'Paraíso de Azahar - Apartamentos en el centro de Estepona',
  'Paraíso de Azahar - Appartements neufs au centre d’Estepona', 'Paraíso de Azahar - Neue Wohnungen im Zentrum von Estepona',
  'Paraíso de Azahar - Новые квартиры в центре Эстепоны', 'Paraíso de Azahar - شقق جديدة في وسط إستيبونا',
  'Paraíso de Azahar - Nieuwe appartementen in centrum Estepona', 'Paraíso de Azahar - Nowe mieszkania w centrum Estepony',
  'Paraíso de Azahar - Nye leiligheter i sentrum av Estepona', 'Paraíso de Azahar - Nya lägenheter i centrala Estepona')
for _l, _t in T['Paraíso de Azahar - New Apartments in Central Estepona'].items():
    assert len(_t) <= 62, (_l, len(_t))
a('Paraíso de Azahar: New Apartments Next to the Old Town of Estepona',
  'Paraíso de Azahar: apartamentos nuevos junto al casco antiguo de Estepona',
  'Paraíso de Azahar : appartements neufs à côté de la vieille ville d’Estepona',
  'Paraíso de Azahar: Neue Wohnungen neben der Altstadt von Estepona',
  'Paraíso de Azahar: новые квартиры рядом со старым городом Эстепоны',
  'Paraíso de Azahar: شقق جديدة بجوار البلدة القديمة في إستيبونا',
  'Paraíso de Azahar: nieuwe appartementen naast de oude stad van Estepona',
  'Paraíso de Azahar: nowe mieszkania obok starego miasta w Esteponie',
  'Paraíso de Azahar: nye leiligheter ved siden av gamlebyen i Estepona',
  'Paraíso de Azahar: nya lägenheter intill gamla stan i Estepona')
a('New Apartments Next to the Old Town of Estepona', 'Apartamentos nuevos junto al casco antiguo de Estepona',
  'Appartements neufs à côté de la vieille ville d’Estepona', 'Neue Wohnungen neben der Altstadt von Estepona',
  'Новые квартиры рядом со старым городом Эстепоны', 'شقق جديدة بجوار البلدة القديمة في إستيبونا',
  'Nieuwe appartementen naast de oude stad van Estepona', 'Nowe mieszkania obok starego miasta w Esteponie',
  'Nye leiligheter ved siden av gamlebyen i Estepona', 'Nya lägenheter intill gamla stan i Estepona')

# ---------------------------------------------------------------- templates: unit sizes, plan labels
W = {  # built, interior, terrace -- the forms the zenith-estepona and sotavento-residences overlays already use
 'es': ('construidos', 'interiores', 'de terraza'),
 'fr': ('construits', 'intérieurs', 'de terrasse'),
 'de': ('bebaut', 'Innenfläche', 'Terrasse'),
 'nl': ('bebouwd', 'binnen', 'terras'),
 'pl': ('zabudowy', 'wnętrza', 'tarasu'),
 'no': ('bebygd areal', 'innvendig', 'terrasse'),
 'sv': ('byggyta', 'inomhus', 'terrass'),
}
AR_W = ('مبنية', 'داخلية', 'تراس')
RU_W = ('застроенной площади', 'внутри', 'терраса')
KINDS = ['built', 'interior', 'terrace']


def size_str(src, l):
    out = []
    for p in [p.strip() for p in src.split(',')]:
        m = re.fullmatch(r'([\d.]+) sqm (built|interior|terrace)', p)
        assert m, p
        n, kind = m.group(1), KINDS.index(m.group(2))
        v = num(n, l)
        if l == 'ru':
            out.append(f'{v} м² {RU_W[0]}' if kind == 0 else f'{v} м² {RU_W[1]}' if kind == 1 else f'{RU_W[2]} {v} м²')
        elif l == 'ar':
            out.append(f'{v} م² {AR_W[kind]}')
        else:
            out.append(f'{v} m² {W[l][kind]}')
    return ('، ' if l == 'ar' else ', ').join(out)


SIZES = ['52.55 sqm built, 47.55 sqm interior', '93.83 sqm built, 83.80 sqm interior',
         '65.44 sqm built, 56.16 sqm interior, 38.56 sqm terrace', '78.02 sqm built, 69.33 sqm interior',
         '77.39 sqm built, 67.26 sqm interior', '94.84 sqm built, 83.17 sqm interior']
for s in SIZES:
    T[s] = {l: size_str(s, l) for l in LOCS}

FLOORPLAN = {'es': 'Plano de la vivienda {}', 'fr': 'Plan du logement {}', 'de': 'Grundriss der Wohnung {}', 'ru': 'Планировка квартиры {}',
             'ar': 'مخطط المسكن {}', 'nl': 'Plattegrond van woning {}', 'pl': 'Rzut mieszkania {}', 'no': 'Plantegning av bolig {}',
             'sv': 'Planritning för bostad {}'}
HOME = {'es': 'Vivienda {}', 'fr': 'Logement {}', 'de': 'Wohnung {}', 'ru': 'Квартира {}', 'ar': 'المسكن {}', 'nl': 'Woning {}',
        'pl': 'Mieszkanie {}', 'no': 'Bolig {}', 'sv': 'Bostad {}'}
for u in ['Bajo A', 'Bajo B', '1ºA', '1ºB', '1ºC', '1ºD']:
    T[f'Floorplan of home {u}'] = {l: FLOORPLAN[l].format(u) for l in LOCS}
    T[f'Home {u}'] = {l: HOME[l].format(u) for l in LOCS}

json.dump(T, open(f'{SP}/tr_p.json', 'w'), ensure_ascii=False, indent=1)
print('entries', len(T))
