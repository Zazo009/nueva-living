# -*- coding: utf-8 -*-
"""La Gaspara Residences: the strings the translation memory did not have.

Keyed by the English string, like k_mirlo.py. Tokens: {E406000} money, {N107.45} decimal number, {U} the
area unit. Unit sizes, references and render alts are built from per-locale templates below; unit floor
labels are left to assemble.py, which builds them from floor_parts.json.
    python3 tools/import/k_la_gaspara_residences.py <scratch dir>   (writes <dir>/tr_g.json, then assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
EN = json.load(open('content/liora-projects/la-gaspara-residences/project.json'))


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


for s in ['La Gaspara Residences', 'La Gaspara', 'La Gaspara <em>Residences</em>', 'La Gaspara, Estepona']:
    same(s)

# ---------------------------------------------------------------- unit table
SIZE = {
    'es': '{b} m² construido, {u} m² superficie útil, {t} m² terraza',
    'fr': '{b} m² construit, {u} m² surface utile, {t} m² terrasse',
    'de': '{b} m² bebaut, {u} m² Wohnfläche, {t} m² Terrasse',
    'ru': '{b} м² застройка, {u} м² полезная площадь, {t} м² терраса',
    'ar': '{b} م² مبنية، {u} م² مساحة صافية، {t} م² تراس',
    'nl': '{b} m² bebouwd, {u} m² nuttige oppervlakte, {t} m² terras',
    'pl': '{b} m² powierzchnia zabudowy, {u} m² powierzchnia użytkowa, {t} m² taras',
    'no': '{b} m² bygget, {u} m² nyttbart areal, {t} m² terrasse',
    'sv': '{b} m² byggyta, {u} m² nyttoyta, {t} m² terrass',
}
for unit in EN['availability']['units']:
    same(unit['reference'])
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm usable, ([\d.]+) sqm terrace', unit['size'])
    assert m, unit['size']
    if unit['size'] not in T:
        T[unit['size']] = {l: SIZE[l].format(b=num(m.group(1), l), u=num(m.group(2), l), t=num(m.group(3), l))
                           for l in LOCS}

# ---------------------------------------------------------------- render alts
CGI = {'es': ', recreación por ordenador', 'fr': ', image de synthèse', 'de': ', Rendering',
       'ru': ', визуализация', 'ar': '، تصميم حاسوبي', 'nl': ', render', 'pl': ', wizualizacja',
       'no': ', datagenerert bilde', 'sv': ', datorgenererad bild'}


def alt(en, *tr):
    assert en.endswith(', a computer-generated image'), en
    assert len(tr) == 9
    T[en] = {l: expand(t, l) + CGI[l] for l, t in zip(LOCS, tr)}


alt('Terraced white blocks above the communal pool and loungers on the lawn, a computer-generated image',
    'Bloques blancos escalonados sobre la piscina comunitaria y las tumbonas en el césped',
    'Immeubles blancs en terrasses au-dessus de la piscine commune et des transats sur la pelouse',
    'Weiße, terrassierte Blöcke über dem Gemeinschaftspool und den Liegen auf dem Rasen',
    'Белые террасные корпуса над общим бассейном и шезлонгами на газоне',
    'مبانٍ بيضاء متدرجة فوق المسبح المشترك ومقاعد التشمس على العشب',
    'Witte terrasvormige blokken boven het gemeenschappelijke zwembad en de ligbedden op het gazon',
    'Białe tarasowe budynki nad wspólnym basenem i leżakami na trawniku',
    'Hvite terrasserte bygg over fellesbassenget og solsengene på plenen',
    'Vita terrasserade hus ovanför den gemensamma poolen och solsängarna på gräsmattan')
alt('The terraced façade stepping back floor by floor above the pool, a computer-generated image',
    'La fachada aterrazada, retranqueada planta a planta sobre la piscina',
    'La façade en terrasses, en retrait d’étage en étage au-dessus de la piscine',
    'Die terrassierte Fassade, Geschoss für Geschoss zurückgesetzt über dem Pool',
    'Террасный фасад, отступающий этаж за этажом над бассейном',
    'الواجهة المتدرجة تتراجع طابقاً بعد طابق فوق المسبح',
    'De terrasgevel die per verdieping terugwijkt boven het zwembad',
    'Tarasowa elewacja cofająca się piętro po piętrze nad basenem',
    'Den terrasserte fasaden, trukket tilbake etasje for etasje over bassenget',
    'Den terrasserade fasaden som drar sig tillbaka våning för våning ovanför poolen')
alt('The communal pool with pergolas and palms, the blocks behind, a computer-generated image',
    'La piscina comunitaria con pérgolas y palmeras, con los bloques detrás',
    'La piscine commune avec pergolas et palmiers, les immeubles en arrière-plan',
    'Der Gemeinschaftspool mit Pergolen und Palmen, dahinter die Blöcke',
    'Общий бассейн с перголами и пальмами, за ним корпуса',
    'المسبح المشترك مع البرغولات والنخيل، والمباني في الخلفية',
    'Het gemeenschappelijke zwembad met pergola’s en palmen, de blokken erachter',
    'Wspólny basen z pergolami i palmami, w tle budynki',
    'Fellesbassenget med pergolaer og palmer, byggene bak',
    'Den gemensamma poolen med pergolor och palmer, husen bakom')
alt('The gardens and the pool at dusk, lit paths between the planting and the sea beyond, a computer-generated image',
    'Los jardines y la piscina al anochecer, con senderos iluminados entre la vegetación y el mar al fondo',
    'Les jardins et la piscine au crépuscule, des allées éclairées entre les plantations et la mer au loin',
    'Die Gärten und der Pool in der Abenddämmerung, beleuchtete Wege zwischen den Pflanzen und dahinter das Meer',
    'Сады и бассейн в сумерках, подсвеченные дорожки среди зелени и море вдали',
    'الحدائق والمسبح عند الغسق، وممرات مضاءة بين النباتات والبحر في الأفق',
    'De tuinen en het zwembad bij schemering, verlichte paden tussen de beplanting en de zee in de verte',
    'Ogrody i basen o zmierzchu, oświetlone ścieżki wśród zieleni i morze w oddali',
    'Hagene og bassenget i skumringen, opplyste stier mellom beplantningen og havet i det fjerne',
    'Trädgårdarna och poolen i skymningen, upplysta gångar mellan planteringarna och havet i fjärran')
alt('A covered terrace with sofas, looking over the coast to the sea, a computer-generated image',
    'Una terraza cubierta con sofás, con vistas a la costa y al mar',
    'Une terrasse couverte avec canapés, donnant sur la côte et la mer',
    'Eine überdachte Terrasse mit Sofas und Blick über die Küste aufs Meer',
    'Крытая терраса с диванами и видом на побережье и море',
    'تراس مسقوف بأرائك، يطل على الساحل والبحر',
    'Een overdekt terras met banken, met uitzicht over de kust op zee',
    'Zadaszony taras z sofami, z widokiem na wybrzeże i morze',
    'En overbygd terrasse med sofaer og utsikt over kysten mot havet',
    'En överbyggd terrass med soffor och utsikt över kusten mot havet')
alt('A long dining table on a covered terrace at sunset, with seating and the sea beyond, a computer-generated image',
    'Una larga mesa de comedor en una terraza cubierta al atardecer, con zona de estar y el mar al fondo',
    'Une longue table à manger sur une terrasse couverte au coucher du soleil, avec un salon et la mer au loin',
    'Ein langer Esstisch auf einer überdachten Terrasse bei Sonnenuntergang, mit Sitzecke und dem Meer im Hintergrund',
    'Длинный обеденный стол на крытой террасе на закате, зона отдыха и море вдали',
    'طاولة طعام طويلة على تراس مسقوف عند الغروب، مع جلسة والبحر في الأفق',
    'Een lange eettafel op een overdekt terras bij zonsondergang, met een zithoek en de zee in de verte',
    'Długi stół jadalniany na zadaszonym tarasie o zachodzie słońca, z wypoczynkiem i morzem w oddali',
    'Et langt spisebord på en overbygd terrasse i solnedgangen, med sittegruppe og havet i det fjerne',
    'Ett långt matbord på en överbyggd terrass i solnedgången, med sittgrupp och havet i fjärran')
alt('The living room with a corner sofa and sliding doors to the terrace, a computer-generated image',
    'El salón con sofá rinconero y puertas correderas a la terraza',
    'Le séjour avec un canapé d’angle et des baies coulissantes sur la terrasse',
    'Der Wohnraum mit Ecksofa und Schiebetüren zur Terrasse',
    'Гостиная с угловым диваном и раздвижными дверями на террасу',
    'صالة المعيشة مع أريكة زاوية وأبواب منزلقة إلى التراس',
    'De woonkamer met een hoekbank en schuifpuien naar het terras',
    'Salon z narożną sofą i przesuwnymi drzwiami na taras',
    'Stuen med hjørnesofa og skyvedører ut til terrassen',
    'Vardagsrummet med hörnsoffa och skjutdörrar ut mot terrassen')
alt('The open kitchen, dining table and living room as one space, a computer-generated image',
    'La cocina abierta, la mesa de comedor y el salón en un mismo espacio',
    'La cuisine ouverte, la table à manger et le séjour en un seul espace',
    'Offene Küche, Esstisch und Wohnraum in einem Raum',
    'Открытая кухня, обеденный стол и гостиная в едином пространстве',
    'المطبخ المفتوح وطاولة الطعام وصالة المعيشة في مساحة واحدة',
    'De open keuken, eettafel en woonkamer als één ruimte',
    'Otwarta kuchnia, stół jadalniany i salon w jednej przestrzeni',
    'Det åpne kjøkkenet, spisebordet og stuen i ett rom',
    'Det öppna köket, matbordet och vardagsrummet i ett rum')
alt('The main bedroom with doors to the terrace and the sea in the distance, a computer-generated image',
    'El dormitorio principal con salida a la terraza y el mar a lo lejos',
    'La chambre principale ouvrant sur la terrasse, avec la mer au loin',
    'Das Hauptschlafzimmer mit Türen zur Terrasse und dem Meer in der Ferne',
    'Главная спальня с выходом на террасу и морем вдали',
    'غرفة النوم الرئيسية مع أبواب إلى التراس والبحر في البعيد',
    'De hoofdslaapkamer met deuren naar het terras en de zee in de verte',
    'Główna sypialnia z wyjściem na taras i morzem w oddali',
    'Hovedsoverommet med dører ut til terrassen og havet i det fjerne',
    'Huvudsovrummet med dörrar ut mot terrassen och havet i fjärran')
alt('A bedroom with a green headboard and a window over the hills, a computer-generated image',
    'Un dormitorio con cabecero verde y una ventana a las colinas',
    'Une chambre avec une tête de lit verte et une fenêtre sur les collines',
    'Ein Schlafzimmer mit grünem Kopfteil und einem Fenster zu den Hügeln',
    'Спальня с зелёным изголовьем и окном на холмы',
    'غرفة نوم بلوح رأس أخضر ونافذة تطل على التلال',
    'Een slaapkamer met een groen hoofdbord en een raam op de heuvels',
    'Sypialnia z zielonym zagłówkiem i oknem na wzgórza',
    'Et soverom med grønn sengegavl og vindu mot åsene',
    'Ett sovrum med grön sänggavel och fönster mot kullarna')
alt('A bathroom in pale stone tile with a walk-in shower and a tall window, a computer-generated image',
    'Un baño en baldosa de tono piedra claro, con ducha de obra y una ventana alta',
    'Une salle de bains en carrelage pierre claire, avec douche à l’italienne et une haute fenêtre',
    'Ein Bad mit hellen Fliesen in Steinoptik, bodengleicher Dusche und einem hohen Fenster',
    'Ванная в светлой плитке под камень, с душем без поддона и высоким окном',
    'حمّام ببلاط حجري فاتح، مع دُش مفتوح ونافذة طويلة',
    'Een badkamer in lichte tegels in steenlook, met inloopdouche en een hoog raam',
    'Łazienka w jasnych płytkach imitujących kamień, z prysznicem typu walk-in i wysokim oknem',
    'Et bad med lyse fliser i steinlook, walk-in-dusj og et høyt vindu',
    'Ett badrum i ljust kakel i stenlook, med walk-in-dusch och ett högt fönster')
alt('A white bathroom with a wall-hung vanity and a glass shower screen, a computer-generated image',
    'Un baño blanco con mueble de lavabo suspendido y mampara de ducha de vidrio',
    'Une salle de bains blanche avec meuble vasque suspendu et paroi de douche en verre',
    'Ein weißes Bad mit wandhängendem Waschtisch und gläserner Duschwand',
    'Белая ванная с подвесной тумбой под раковину и стеклянной душевой перегородкой',
    'حمّام أبيض بخزانة مغسلة معلقة وحاجز دُش زجاجي',
    'Een witte badkamer met een zwevend badmeubel en een glazen douchewand',
    'Biała łazienka z wiszącą szafką umywalkową i szklaną ścianką prysznicową',
    'Et hvitt bad med vegghengt servantskap og dusjvegg i glass',
    'Ett vitt badrum med vägghängt kommodskåp och duschvägg i glas')
alt("The residents' gym, with bikes and a treadmill along a glass wall, a computer-generated image",
    'El gimnasio de los residentes, con bicicletas y una cinta de correr junto a una pared de vidrio',
    'La salle de sport des résidents, avec vélos et tapis de course le long d’une paroi vitrée',
    'Der Fitnessraum der Bewohner mit Fahrrädern und einem Laufband entlang einer Glaswand',
    'Тренажёрный зал для жителей с велотренажёрами и беговой дорожкой вдоль стеклянной стены',
    'صالة الرياضة للسكان، مع دراجات وجهاز مشي بمحاذاة جدار زجاجي',
    'De fitnessruimte voor bewoners, met fietsen en een loopband langs een glazen wand',
    'Siłownia dla mieszkańców z rowerkami i bieżnią wzdłuż szklanej ściany',
    'Beboernes treningsrom med sykler og tredemølle langs en glassvegg',
    'De boendes gym med cyklar och ett löpband längs en glasvägg')

# ---------------------------------------------------------------- identity and summaries
a("Fifteen apartments available in the second phase of a gated scheme in La Gaspara, on the western side of Estepona, of two and three bedrooms and 107.45 to 144.67 sqm built, every home with a terrace of 27.79 to 98.60 sqm, in a scheme with two adult pools, a children's pool, a gym and a social club.",
  'Quince apartamentos disponibles en la segunda fase de un conjunto cerrado en La Gaspara, en la zona oeste de Estepona, de dos y tres dormitorios y de {N107.45} a {N144.67} {U} construidos, todos con terraza de {N27.79} a {N98.60} {U}, en un conjunto con dos piscinas para adultos, una piscina infantil, gimnasio y club social.',
  'Quinze appartements disponibles dans la deuxième phase d’une résidence fermée à La Gaspara, à l’ouest d’Estepona, de deux et trois chambres et de {N107.45} à {N144.67} {U} construits, tous avec une terrasse de {N27.79} à {N98.60} {U}, dans une résidence dotée de deux piscines pour adultes, d’une piscine pour enfants, d’une salle de sport et d’un club social.',
  'Fünfzehn verfügbare Wohnungen im zweiten Bauabschnitt einer geschlossenen Anlage in La Gaspara im Westen von Estepona, mit zwei und drei Schlafzimmern und {N107.45} bis {N144.67} {U} bebauter Fläche, jede mit einer Terrasse von {N27.79} bis {N98.60} {U}, in einer Anlage mit zwei Erwachsenenpools, einem Kinderbecken, einem Fitnessraum und einem Clubraum.',
  'Пятнадцать доступных квартир во второй очереди закрытого комплекса в Ла-Гаспаре, в западной части Эстепоны, с двумя и тремя спальнями, площадью застройки от {N107.45} до {N144.67} {U}, у каждой терраса от {N27.79} до {N98.60} {U}; в комплексе два взрослых бассейна, детский бассейн, тренажёрный зал и клуб для жителей.',
  'خمس عشرة شقة متاحة في المرحلة الثانية من مجمع مغلق في لا غاسبارا، في الجهة الغربية من إستيبونا، بغرفتي نوم أو ثلاث غرف ومساحة مبنية من {N107.45} إلى {N144.67} {U}، ولكل منها تراس من {N27.79} إلى {N98.60} {U}، في مجمع يضم مسبحين للبالغين ومسبحاً للأطفال وصالة رياضة وناديًا اجتماعيًا.',
  'Vijftien beschikbare appartementen in de tweede fase van een besloten complex in La Gaspara, aan de westkant van Estepona, met twee en drie slaapkamers en {N107.45} tot {N144.67} {U} bebouwd, elk met een terras van {N27.79} tot {N98.60} {U}, in een complex met twee zwembaden voor volwassenen, een kinderbad, een fitnessruimte en een clubruimte.',
  'Piętnaście dostępnych apartamentów w drugim etapie osiedla zamkniętego w La Gaspara, w zachodniej części Estepony, z dwiema i trzema sypialniami i powierzchnią zabudowy od {N107.45} do {N144.67} {U}, każdy z tarasem od {N27.79} do {N98.60} {U}, na osiedlu z dwoma basenami dla dorosłych, brodzikiem dla dzieci, siłownią i klubem dla mieszkańców.',
  'Femten ledige leiligheter i andre byggetrinn av et lukket anlegg i La Gaspara, på vestsiden av Estepona, med to og tre soverom og {N107.45} til {N144.67} {U} bygget, alle med terrasse på {N27.79} til {N98.60} {U}, i et anlegg med to voksenbassenger, et barnebasseng, treningsrom og en fellesklubb.',
  'Femton lediga lägenheter i andra etappen av ett slutet område i La Gaspara, på Esteponas västra sida, med två och tre sovrum och {N107.45} till {N144.67} {U} byggyta, alla med en terrass på {N27.79} till {N98.60} {U}, i ett område med två pooler för vuxna, en barnpool, ett gym och en klubblokal.')

a('Fifteen apartments in La Gaspara, Estepona: two and three bedrooms, 107 to 145 sqm built, terraces from 28 sqm, underfloor heating, two pools and a gym.',
  'Quince apartamentos en La Gaspara, Estepona: dos y tres dormitorios, de 107 a 145 {U} construidos, terrazas desde 28 {U}, suelo radiante, dos piscinas y gimnasio.',
  'Quinze appartements à La Gaspara, Estepona : deux et trois chambres, de 107 à 145 {U} construits, terrasses dès 28 {U}, plancher chauffant, deux piscines et salle de sport.',
  'Fünfzehn Wohnungen in La Gaspara, Estepona: zwei und drei Schlafzimmer, 107 bis 145 {U} bebaut, Terrassen ab 28 {U}, Fußbodenheizung, zwei Pools und Fitnessraum.',
  'Пятнадцать квартир в Ла-Гаспаре, Эстепона: две и три спальни, от 107 до 145 {U}, террасы от 28 {U}, тёплые полы, два бассейна и тренажёрный зал.',
  'خمس عشرة شقة في لا غاسبارا، إستيبونا: غرفتا نوم أو ثلاث، من 107 إلى 145 {U} مبنية، تراسات من 28 {U}، تدفئة أرضية، مسبحان وصالة رياضة.',
  'Vijftien appartementen in La Gaspara, Estepona: twee en drie slaapkamers, 107 tot 145 {U} bebouwd, terrassen vanaf 28 {U}, vloerverwarming, twee zwembaden en fitness.',
  'Piętnaście apartamentów w La Gaspara, Estepona: dwie i trzy sypialnie, od 107 do 145 {U} zabudowy, tarasy od 28 {U}, ogrzewanie podłogowe, dwa baseny i siłownia.',
  'Femten leiligheter i La Gaspara, Estepona: to og tre soverom, 107 til 145 {U} bygget, terrasser fra 28 {U}, gulvvarme, to bassenger og treningsrom.',
  'Femton lägenheter i La Gaspara, Estepona: två och tre sovrum, 107 till 145 {U} byggyta, terrasser från 28 {U}, golvvärme, två pooler och gym.')

a('Apartments with deep terraces on the western side of Estepona, in a gated scheme with pools, a gym and a social club. From EUR 406,000 plus IVA.',
  'Apartamentos con amplias terrazas en la zona oeste de Estepona, en un conjunto cerrado con piscinas, gimnasio y club social. Desde {E406000} más IVA.',
  'Appartements avec de grandes terrasses à l’ouest d’Estepona, dans une résidence fermée avec piscines, salle de sport et club social. À partir de {E406000} hors TVA.',
  'Wohnungen mit tiefen Terrassen im Westen von Estepona, in einer geschlossenen Anlage mit Pools, Fitnessraum und Clubraum. Ab {E406000} zuzüglich MwSt.',
  'Квартиры с глубокими террасами в западной части Эстепоны, в закрытом комплексе с бассейнами, тренажёрным залом и клубом. От {E406000} плюс НДС.',
  'شقق بتراسات واسعة في الجهة الغربية من إستيبونا، ضمن مجمع مغلق بمسابح وصالة رياضة ونادٍ اجتماعي. ابتداءً من {E406000} زائد ضريبة القيمة المضافة.',
  'Appartementen met diepe terrassen aan de westkant van Estepona, in een besloten complex met zwembaden, fitness en clubruimte. Vanaf {E406000} plus btw.',
  'Apartamenty z głębokimi tarasami w zachodniej części Estepony, na osiedlu zamkniętym z basenami, siłownią i klubem. Od {E406000} plus VAT.',
  'Leiligheter med dype terrasser på vestsiden av Estepona, i et lukket anlegg med bassenger, treningsrom og fellesklubb. Fra {E406000} pluss mva.',
  'Lägenheter med djupa terrasser på Esteponas västra sida, i ett slutet område med pooler, gym och klubblokal. Från {E406000} plus IVA (spansk moms).')

a('Fifteen homes available / gated scheme',
  'Quince viviendas disponibles / conjunto cerrado', 'Quinze logements disponibles / résidence fermée',
  'Fünfzehn Wohnungen verfügbar / geschlossene Anlage', 'Пятнадцать квартир доступно / закрытый комплекс',
  'خمس عشرة شقة متاحة / مجمع مغلق', 'Vijftien woningen beschikbaar / besloten complex',
  'Piętnaście mieszkań dostępnych / osiedle zamknięte', 'Femten boliger tilgjengelige / lukket anlegg',
  'Femton bostäder tillgängliga / slutet område')

a('Fifteen apartments still available in the second phase of a gated scheme in La Gaspara, on the western side of Estepona, every one with a terrace.',
  'Quince apartamentos aún disponibles en la segunda fase de un conjunto cerrado en La Gaspara, en la zona oeste de Estepona, todos con terraza.',
  'Quinze appartements encore disponibles dans la deuxième phase d’une résidence fermée à La Gaspara, à l’ouest d’Estepona, tous avec terrasse.',
  'Fünfzehn noch verfügbare Wohnungen im zweiten Bauabschnitt einer geschlossenen Anlage in La Gaspara im Westen von Estepona, alle mit Terrasse.',
  'Пятнадцать квартир, ещё доступных во второй очереди закрытого комплекса в Ла-Гаспаре, в западной части Эстепоны, все с террасой.',
  'خمس عشرة شقة لا تزال متاحة في المرحلة الثانية من مجمع مغلق في لا غاسبارا، في الجهة الغربية من إستيبونا، ولكل منها تراس.',
  'Vijftien appartementen nog beschikbaar in de tweede fase van een besloten complex in La Gaspara, aan de westkant van Estepona, alle met terras.',
  'Piętnaście apartamentów wciąż dostępnych w drugim etapie osiedla zamkniętego w La Gaspara, w zachodniej części Estepony, każdy z tarasem.',
  'Femten leiligheter fortsatt ledige i andre byggetrinn av et lukket anlegg i La Gaspara, på vestsiden av Estepona, alle med terrasse.',
  'Femton lägenheter fortfarande lediga i andra etappen av ett slutet område i La Gaspara, på Esteponas västra sida, alla med terrass.')

# ---------------------------------------------------------------- gallery
a("Computer-generated images from the developer's dossier, which covers both phases of the scheme. They illustrate the design and are not the finished building; furniture and decoration are indicative and are not included in the sale.",
  'Recreaciones por ordenador del dossier del promotor, que abarca las dos fases del conjunto. Ilustran el diseño y no son el edificio terminado; el mobiliario y la decoración son orientativos y no se incluyen en la venta.',
  'Images de synthèse issues du dossier du promoteur, qui couvre les deux phases de la résidence. Elles illustrent le projet et ne montrent pas le bâtiment achevé ; le mobilier et la décoration sont indicatifs et ne sont pas inclus dans la vente.',
  'Renderings aus dem Exposé des Bauträgers, das beide Bauabschnitte der Anlage umfasst. Sie veranschaulichen den Entwurf und zeigen nicht das fertige Gebäude; Möbel und Dekoration sind beispielhaft und nicht im Kaufpreis enthalten.',
  'Визуализации из каталога застройщика, охватывающего обе очереди комплекса. Они иллюстрируют проект и не являются готовым зданием; мебель и декор показаны для примера и в продажу не входят.',
  'صور حاسوبية من كتيّب المطوّر الذي يشمل مرحلتي المجمع. وهي توضح التصميم ولا تمثل المبنى المكتمل، والأثاث والديكور للإيضاح فقط وغير مشمولين في البيع.',
  'Computerbeelden uit het dossier van de ontwikkelaar, dat beide fasen van het complex beslaat. Ze illustreren het ontwerp en tonen niet het afgewerkte gebouw; meubilair en decoratie zijn indicatief en niet bij de koop inbegrepen.',
  'Wizualizacje z broszury dewelopera, obejmującej oba etapy osiedla. Ilustrują projekt i nie przedstawiają gotowego budynku; meble i wystrój są poglądowe i nie wchodzą w zakres sprzedaży.',
  'Datagenererte bilder fra utbyggerens salgsprospekt, som dekker begge byggetrinnene. De illustrerer prosjektet og viser ikke det ferdige bygget; møbler og innredning er veiledende og inngår ikke i kjøpet.',
  'Datorgenererade bilder ur exploatörens prospekt, som omfattar båda etapperna. De illustrerar utformningen och visar inte den färdiga byggnaden; möbler och inredning är vägledande och ingår inte i köpet.')
a('The terraces from below',
  'Las terrazas desde abajo', 'Les terrasses vues d’en bas', 'Die Terrassen von unten', 'Террасы снизу',
  'التراسات من الأسفل', 'De terrassen van onderaf', 'Tarasy od dołu', 'Terrassene nedenfra', 'Terrasserna underifrån')
a('The gardens at dusk',
  'Los jardines al anochecer', 'Les jardins au crépuscule', 'Die Gärten in der Abenddämmerung', 'Сады в сумерках',
  'الحدائق عند الغسق', 'De tuinen bij schemering', 'Ogrody o zmierzchu', 'Hagene i skumringen', 'Trädgårdarna i skymningen')
# Corrections to the translation memory for this page: its Arabic "The blocks" is a dual (two buildings)
# and its Swedish "The main bedroom" drops "main".
a('The blocks', 'Los bloques', 'Les immeubles', 'Die Blöcke', 'Корпуса', 'المباني', 'De blokken', 'Budynki', 'Byggene', 'Husen')
a('The main bedroom', 'El dormitorio principal', 'La chambre principale', 'Das Hauptschlafzimmer', 'Главная спальня',
  'غرفة النوم الرئيسية', 'De hoofdslaapkamer', 'Główna sypialnia', 'Hovedsoverommet', 'Huvudsovrummet')

# ---------------------------------------------------------------- overview
a('Fifteen homes, <em>second phase</em>',
  'Quince viviendas, <em>segunda fase</em>', 'Quinze logements, <em>deuxième phase</em>',
  'Fünfzehn Wohnungen, <em>zweiter Bauabschnitt</em>', 'Пятнадцать квартир, <em>вторая очередь</em>',
  'خمس عشرة شقة، <em>المرحلة الثانية</em>', 'Vijftien woningen, <em>tweede fase</em>',
  'Piętnaście mieszkań, <em>drugi etap</em>', 'Femten boliger, <em>andre byggetrinn</em>',
  'Femton bostäder, <em>andra etappen</em>')
a("La Gaspara Residences is the second phase of a gated scheme in La Gaspara, beside the A-7 on the western side of Estepona. The developer's dossier describes 105 homes over the two phases; fifteen apartments in this second phase are available.",
  'La Gaspara Residences es la segunda fase de un conjunto cerrado en La Gaspara, junto a la A-7, en la zona oeste de Estepona. El dossier del promotor describe 105 viviendas en las dos fases; en esta segunda fase hay quince apartamentos disponibles.',
  'La Gaspara Residences est la deuxième phase d’une résidence fermée à La Gaspara, le long de l’A-7, à l’ouest d’Estepona. Le dossier du promoteur décrit 105 logements sur les deux phases ; quinze appartements de cette deuxième phase sont disponibles.',
  'La Gaspara Residences ist der zweite Bauabschnitt einer geschlossenen Anlage in La Gaspara, direkt an der A-7 im Westen von Estepona. Das Exposé des Bauträgers beschreibt 105 Wohnungen in beiden Abschnitten; fünfzehn Wohnungen dieses zweiten Abschnitts sind verfügbar.',
  'La Gaspara Residences — вторая очередь закрытого комплекса в Ла-Гаспаре, у трассы A-7 в западной части Эстепоны. В каталоге застройщика описаны 105 квартир в двух очередях; во второй очереди доступно пятнадцать квартир.',
  'La Gaspara Residences هي المرحلة الثانية من مجمع مغلق في لا غاسبارا، بجوار الطريق A-7 في الجهة الغربية من إستيبونا. يصف كتيّب المطوّر 105 مساكن في المرحلتين، وتتوفر في هذه المرحلة الثانية خمس عشرة شقة.',
  'La Gaspara Residences is de tweede fase van een besloten complex in La Gaspara, langs de A-7 aan de westkant van Estepona. Het dossier van de ontwikkelaar beschrijft 105 woningen in de twee fasen; in deze tweede fase zijn vijftien appartementen beschikbaar.',
  'La Gaspara Residences to drugi etap osiedla zamkniętego w La Gaspara, przy autostradzie A-7, w zachodniej części Estepony. Broszura dewelopera opisuje 105 mieszkań w obu etapach; w tym drugim etapie dostępnych jest piętnaście apartamentów.',
  'La Gaspara Residences er andre byggetrinn av et lukket anlegg i La Gaspara, ved A-7 på vestsiden av Estepona. Utbyggerens salgsprospekt beskriver 105 boliger fordelt på de to byggetrinnene; femten leiligheter i dette andre byggetrinnet er ledige.',
  'La Gaspara Residences är andra etappen av ett slutet område i La Gaspara, vid A-7 på Esteponas västra sida. Exploatörens prospekt beskriver 105 bostäder i de två etapperna; femton lägenheter i denna andra etapp är lediga.')
a('The available homes have two or three bedrooms and two bathrooms, from 107.45 to 144.67 sqm built with 81.35 to 110.67 sqm of usable interior. Every one has a terrace, from 27.79 to 98.60 sqm, and twelve of the fifteen face south-west, the other three south.',
  'Las viviendas disponibles tienen dos o tres dormitorios y dos baños, de {N107.45} a {N144.67} {U} construidos y de {N81.35} a {N110.67} {U} útiles interiores. Todas tienen terraza, de {N27.79} a {N98.60} {U}, y doce de las quince están orientadas al suroeste y las otras tres al sur.',
  'Les logements disponibles ont deux ou trois chambres et deux salles de bains, de {N107.45} à {N144.67} {U} construits pour {N81.35} à {N110.67} {U} de surface utile intérieure. Tous ont une terrasse, de {N27.79} à {N98.60} {U}, et douze des quinze sont orientés au sud-ouest, les trois autres au sud.',
  'Die verfügbaren Wohnungen haben zwei oder drei Schlafzimmer und zwei Bäder, {N107.45} bis {N144.67} {U} bebaute Fläche und {N81.35} bis {N110.67} {U} Wohnfläche innen. Jede hat eine Terrasse von {N27.79} bis {N98.60} {U}; zwölf der fünfzehn sind nach Südwesten ausgerichtet, die übrigen drei nach Süden.',
  'В доступных квартирах две или три спальни и две ванные комнаты, площадь застройки от {N107.45} до {N144.67} {U}, полезная внутренняя площадь от {N81.35} до {N110.67} {U}. У каждой есть терраса от {N27.79} до {N98.60} {U}; двенадцать из пятнадцати ориентированы на юго-запад, остальные три на юг.',
  'تضم الشقق المتاحة غرفتي نوم أو ثلاث غرف وحمّامين، بمساحة مبنية من {N107.45} إلى {N144.67} {U} ومساحة داخلية صافية من {N81.35} إلى {N110.67} {U}. ولكل منها تراس من {N27.79} إلى {N98.60} {U}، واثنتا عشرة من الخمس عشرة تتجه نحو الجنوب الغربي والثلاث الأخرى نحو الجنوب.',
  'De beschikbare woningen hebben twee of drie slaapkamers en twee badkamers, {N107.45} tot {N144.67} {U} bebouwd met {N81.35} tot {N110.67} {U} nuttige binnenoppervlakte. Elke woning heeft een terras van {N27.79} tot {N98.60} {U}; twaalf van de vijftien liggen op het zuidwesten, de andere drie op het zuiden.',
  'Dostępne mieszkania mają dwie lub trzy sypialnie i dwie łazienki, od {N107.45} do {N144.67} {U} powierzchni zabudowy i od {N81.35} do {N110.67} {U} powierzchni użytkowej wewnątrz. Każde ma taras od {N27.79} do {N98.60} {U}; dwanaście z piętnastu ma wystawę południowo-zachodnią, pozostałe trzy południową.',
  'De ledige boligene har to eller tre soverom og to bad, fra {N107.45} til {N144.67} {U} bygget og {N81.35} til {N110.67} {U} nyttbart innvendig areal. Alle har terrasse på {N27.79} til {N98.60} {U}, og tolv av de femten vender mot sørvest, de tre andre mot sør.',
  'De lediga bostäderna har två eller tre sovrum och två badrum, {N107.45} till {N144.67} {U} byggyta och {N81.35} till {N110.67} {U} invändig nyttoyta. Alla har en terrass på {N27.79} till {N98.60} {U}, och tolv av de femton vetter mot sydväst, de övriga tre mot söder.')
a("The communal areas described for the scheme are two adult pools, a children's pool, a gym, a social club, landscaped gardens, bicycle storage and a gatehouse at the entrance. Each home is listed with a parking space and a storeroom, priced as separate lines.",
  'Las zonas comunes descritas para el conjunto son dos piscinas para adultos, una piscina infantil, gimnasio, club social, jardines paisajísticos, aparcamiento de bicicletas y una garita en la entrada. Cada vivienda figura con una plaza de garaje y un trastero, que se cotizan como líneas aparte.',
  'Les espaces communs décrits pour la résidence sont deux piscines pour adultes, une piscine pour enfants, une salle de sport, un club social, des jardins paysagers, un local à vélos et une loge à l’entrée. Chaque logement est listé avec une place de parking et un débarras, chiffrés sur des lignes distinctes.',
  'Für die Anlage beschrieben sind zwei Erwachsenenpools, ein Kinderbecken, ein Fitnessraum, ein Clubraum, angelegte Gärten, ein Fahrradraum und ein Pförtnerhaus an der Einfahrt. Jede Wohnung ist mit einem Stellplatz und einem Abstellraum gelistet, die als eigene Positionen bepreist sind.',
  'Для комплекса описаны два взрослых бассейна, детский бассейн, тренажёрный зал, клуб для жителей, ландшафтные сады, велосипедная комната и пост охраны на въезде. Каждая квартира указана в списке с парковочным местом и кладовой, которые оцениваются отдельными позициями.',
  'المرافق المشتركة الموصوفة للمجمع هي مسبحان للبالغين ومسبح للأطفال وصالة رياضة ونادٍ اجتماعي وحدائق منسّقة ومخزن للدراجات وكشك حراسة عند المدخل. وتُدرج كل شقة مع موقف سيارة ومخزن، يُسعَّران بندين منفصلين.',
  'De gemeenschappelijke voorzieningen die voor het complex worden beschreven, zijn twee zwembaden voor volwassenen, een kinderbad, een fitnessruimte, een clubruimte, aangelegde tuinen, een fietsenstalling en een portiersloge bij de ingang. Elke woning staat op de lijst met een parkeerplaats en een berging, die als aparte posten zijn geprijsd.',
  'Części wspólne opisane dla osiedla to dwa baseny dla dorosłych, brodzik dla dzieci, siłownia, klub dla mieszkańców, zagospodarowane ogrody, rowerownia i portiernia przy wjeździe. Każde mieszkanie figuruje na liście z miejscem postojowym i komórką lokatorską, wycenianymi jako osobne pozycje.',
  'Fellesområdene som beskrives for anlegget, er to voksenbassenger, et barnebasseng, treningsrom, fellesklubb, opparbeidede hager, sykkelbod og et vaktbu ved innkjøringen. Hver bolig står oppført med en parkeringsplass og en bod, priset som egne linjer.',
  'De gemensamma ytor som beskrivs för området är två pooler för vuxna, en barnpool, ett gym, en klubblokal, anlagda trädgårdar, cykelförråd och en vaktkur vid infarten. Varje bostad listas med en parkeringsplats och ett förråd, prissatta som egna rader.')

# ---------------------------------------------------------------- residences
a("Seven two-bedroom and eight three-bedroom apartments, on the ground to third floors of four blocks. The table below follows the developer's current list.",
  'Siete apartamentos de dos dormitorios y ocho de tres, de la planta baja a la tercera, en cuatro bloques. La tabla siguiente sigue el listado actual del promotor.',
  'Sept appartements de deux chambres et huit de trois, du rez-de-chaussée au troisième étage, répartis dans quatre immeubles. Le tableau ci-dessous suit la liste actuelle du promoteur.',
  'Sieben Wohnungen mit zwei und acht mit drei Schlafzimmern, vom Erdgeschoss bis zum dritten Obergeschoss in vier Blöcken. Die Tabelle unten folgt der aktuellen Liste des Bauträgers.',
  'Семь квартир с двумя спальнями и восемь с тремя, с первого по четвёртый этаж, в четырёх корпусах. Таблица ниже повторяет текущий список застройщика.',
  'سبع شقق بغرفتي نوم وثماني شقق بثلاث غرف، من الطابق الأرضي حتى الطابق الثالث في أربعة مبانٍ. ويتبع الجدول أدناه القائمة الحالية للمطوّر.',
  'Zeven appartementen met twee en acht met drie slaapkamers, van de begane grond tot de derde verdieping, in vier blokken. De tabel hieronder volgt de actuele lijst van de ontwikkelaar.',
  'Siedem apartamentów z dwiema sypialniami i osiem z trzema, od parteru do trzeciego piętra, w czterech budynkach. Poniższa tabela odpowiada aktualnej liście dewelopera.',
  'Sju leiligheter med to soverom og åtte med tre, fra første til fjerde etasje, i fire bygg. Tabellen nedenfor følger utbyggerens gjeldende liste.',
  'Sju lägenheter med två sovrum och åtta med tre, från bottenvåningen till tredje våningen, i fyra hus. Tabellen nedan följer exploatörens aktuella lista.')
a('Two or three bedrooms and two bathrooms, with the living room, dining area and kitchen as one room opening to the terrace, and a separate utility room.',
  'Dos o tres dormitorios y dos baños, con salón, comedor y cocina en un solo espacio abierto a la terraza, y un lavadero independiente.',
  'Deux ou trois chambres et deux salles de bains, avec séjour, coin repas et cuisine en une seule pièce ouverte sur la terrasse, et une buanderie séparée.',
  'Zwei oder drei Schlafzimmer und zwei Bäder, Wohn-, Ess- und Küchenbereich in einem Raum mit Zugang zur Terrasse sowie ein separater Hauswirtschaftsraum.',
  'Две или три спальни и две ванные комнаты; гостиная, столовая и кухня объединены в одно пространство с выходом на террасу, есть отдельная постирочная.',
  'غرفتا نوم أو ثلاث غرف وحمّامان، مع صالة المعيشة ومنطقة الطعام والمطبخ في مساحة واحدة تنفتح على التراس، وغرفة غسيل مستقلة.',
  'Twee of drie slaapkamers en twee badkamers, met woonkamer, eethoek en keuken als één ruimte die op het terras uitkomt, en een aparte bijkeuken.',
  'Dwie lub trzy sypialnie i dwie łazienki, z salonem, jadalnią i kuchnią w jednym pomieszczeniu otwartym na taras oraz osobną pralnią.',
  'To eller tre soverom og to bad, med stue, spisestue og kjøkken i ett rom som åpner seg mot terrassen, og et eget vaskerom.',
  'Två eller tre sovrum och två badrum, med vardagsrum, matplats och kök i ett rum som öppnar sig mot terrassen, och en separat tvättstuga.')
a('A terrace on every home, from 27.79 to 98.60 sqm; on some of the drawings a jacuzzi is drawn on the terrace as an option, not included in the price.',
  'Terraza en todas las viviendas, de {N27.79} a {N98.60} {U}; en algunos planos aparece un jacuzzi en la terraza como opción, no incluida en el precio.',
  'Une terrasse pour chaque logement, de {N27.79} à {N98.60} {U} ; sur certains plans, un jacuzzi est dessiné sur la terrasse en option, non compris dans le prix.',
  'Eine Terrasse bei jeder Wohnung, {N27.79} bis {N98.60} {U}; auf einigen Plänen ist ein Whirlpool auf der Terrasse als Option eingezeichnet, nicht im Preis enthalten.',
  'Терраса у каждой квартиры, от {N27.79} до {N98.60} {U}; на некоторых планах на террасе нарисовано джакузи как опция, не входящая в цену.',
  'تراس لكل شقة، من {N27.79} إلى {N98.60} {U}، وفي بعض المخططات يظهر جاكوزي على التراس كخيار غير مشمول في السعر.',
  'Een terras bij elke woning, van {N27.79} tot {N98.60} {U}; op sommige tekeningen staat een jacuzzi op het terras als optie, niet in de prijs inbegrepen.',
  'Taras przy każdym mieszkaniu, od {N27.79} do {N98.60} {U}; na niektórych rzutach na tarasie narysowano jacuzzi jako opcję, niewliczoną w cenę.',
  'Terrasse til alle boligene, fra {N27.79} til {N98.60} {U}; på noen av tegningene er en boblebadstamp tegnet inn på terrassen som tilvalg, ikke inkludert i prisen.',
  'En terrass till varje bostad, från {N27.79} till {N98.60} {U}; på några av ritningarna är en bubbelpool inritad på terrassen som tillval, som inte ingår i priset.')
a("Twelve of the fifteen face south-west and three face south, according to the developer's list.",
  'Doce de las quince están orientadas al suroeste y tres al sur, según el listado del promotor.',
  'Douze des quinze sont orientés au sud-ouest et trois au sud, selon la liste du promoteur.',
  'Laut der Liste des Bauträgers sind zwölf der fünfzehn nach Südwesten und drei nach Süden ausgerichtet.',
  'По списку застройщика двенадцать из пятнадцати квартир ориентированы на юго-запад, три — на юг.',
  'اثنتا عشرة من الخمس عشرة تتجه نحو الجنوب الغربي وثلاث نحو الجنوب، وفق قائمة المطوّر.',
  'Volgens de lijst van de ontwikkelaar liggen twaalf van de vijftien op het zuidwesten en drie op het zuiden.',
  'Według listy dewelopera dwanaście z piętnastu ma wystawę południowo-zachodnią, a trzy południową.',
  'Ifølge utbyggerens liste vender tolv av de femten mot sørvest og tre mot sør.',
  'Enligt exploatörens lista vetter tolv av de femton mot sydväst och tre mot söder.')
a('Warm-water underfloor heating, electric in the bathrooms, with ducted cooling to the living room and bedrooms, and hot water from an aerothermal heat pump.',
  'Suelo radiante por agua templada, eléctrico en los baños, con climatización por conductos en salón y dormitorios, y agua caliente mediante bomba de calor aerotérmica.',
  'Plancher chauffant à eau tiède, électrique dans les salles de bains, rafraîchissement par gaines dans le séjour et les chambres, et eau chaude produite par une pompe à chaleur aérothermique.',
  'Fußbodenheizung mit Warmwasser, in den Bädern elektrisch, Kühlung über Kanäle in Wohnraum und Schlafzimmern sowie Warmwasser aus einer Luft-Wärmepumpe.',
  'Водяные тёплые полы, электрические в ванных, канальное охлаждение в гостиной и спальнях и горячая вода от аэротермального теплового насоса.',
  'تدفئة أرضية بالماء الدافئ، وكهربائية في الحمّامات، مع تبريد بقنوات في صالة المعيشة وغرف النوم، ومياه ساخنة من مضخة حرارية هوائية.',
  'Vloerverwarming op warm water, elektrisch in de badkamers, met koeling via kanalen in woonkamer en slaapkamers, en warm water uit een luchtwarmtepomp.',
  'Wodne ogrzewanie podłogowe, elektryczne w łazienkach, chłodzenie kanałowe w salonie i sypialniach oraz ciepła woda z aerotermicznej pompy ciepła.',
  'Vannbåren gulvvarme, elektrisk på badene, kjøling via kanaler i stue og soverom, og varmtvann fra en luft-til-vann-varmepumpe.',
  'Vattenburen golvvärme, elektrisk i badrummen, kylning via kanaler i vardagsrum och sovrum, och varmvatten från en luft-vatten-värmepump.')
a('A fitted kitchen with induction hob, extractor hood, oven and microwave in a column, panelled dishwasher and fridge, and a washing machine.',
  'Cocina amueblada con placa de inducción, campana extractora, horno y microondas en columna, lavavajillas y frigorífico panelables, y lavadora.',
  'Une cuisine équipée avec plaque à induction, hotte, four et micro-ondes en colonne, lave-vaisselle et réfrigérateur intégrés, et un lave-linge.',
  'Eine Einbauküche mit Induktionskochfeld, Dunstabzugshaube, Backofen und Mikrowelle im Hochschrank, integriertem Geschirrspüler und Kühlschrank sowie einer Waschmaschine.',
  'Встроенная кухня с индукционной варочной панелью, вытяжкой, духовкой и микроволновкой в колонне, встроенными посудомоечной машиной и холодильником, а также стиральная машина.',
  'مطبخ مجهز بموقد حثي وشفاط، وفرن وميكروويف في عمود، وغسالة صحون وثلاجة مدمجتين، وغسالة ملابس.',
  'Een ingerichte keuken met inductiekookplaat, afzuigkap, oven en magnetron in een kolom, ingebouwde vaatwasser en koelkast, en een wasmachine.',
  'Kuchnia w zabudowie z płytą indukcyjną, okapem, piekarnikiem i mikrofalówką w słupku, zabudowaną zmywarką i lodówką oraz pralką.',
  'Et innredet kjøkken med induksjonstopp, ventilator, stekeovn og mikrobølgeovn i høyskap, integrert oppvaskmaskin og kjøleskap, og vaskemaskin.',
  'Ett inrett kök med induktionshäll, köksfläkt, ugn och mikrovågsugn i högskåp, integrerad diskmaskin och kylskåp, samt tvättmaskin.')
a('Motorised insulated blinds in the living room and bedrooms, and basic home automation for lights and blinds, controlled from a phone.',
  'Persianas motorizadas con aislamiento en salón y dormitorios, y domótica básica para luces y persianas, controlada desde el móvil.',
  'Volets roulants motorisés et isolés dans le séjour et les chambres, et une domotique de base pour l’éclairage et les volets, pilotée depuis un smartphone.',
  'Motorisierte, gedämmte Rollläden in Wohnraum und Schlafzimmern sowie eine einfache Hausautomation für Licht und Rollläden, per Smartphone steuerbar.',
  'Моторизованные утеплённые жалюзи в гостиной и спальнях и базовая система «умный дом» для света и жалюзи с управлением со смартфона.',
  'ستائر معدنية معزولة بمحرك في صالة المعيشة وغرف النوم، ونظام منزل ذكي أساسي للإضاءة والستائر يُدار من الهاتف.',
  'Gemotoriseerde, geïsoleerde rolluiken in woonkamer en slaapkamers, en eenvoudige domotica voor verlichting en rolluiken, te bedienen met de telefoon.',
  'Zmotoryzowane, ocieplane rolety w salonie i sypialniach oraz podstawowa automatyka domowa do oświetlenia i rolet, sterowana z telefonu.',
  'Motoriserte, isolerte rullegardiner i stue og soverom, og enkel hjemmeautomasjon for lys og gardiner, styrt fra mobilen.',
  'Motoriserade, isolerade rullgardiner i vardagsrum och sovrum, och enkel hemautomation för belysning och rullgardiner, styrd från mobilen.')

# ---------------------------------------------------------------- availability
a('Fifteen apartments in the second phase are available, and the developer prices each of them. Each is listed with one parking space and one storeroom, sold as separate lines. Nueva Living reconfirms price and availability before any viewing or reservation.',
  'Quince apartamentos de la segunda fase están disponibles y el promotor pone precio a cada uno. Cada uno figura con una plaza de garaje y un trastero, que se venden como líneas aparte. Nueva Living reconfirma precio y disponibilidad antes de cualquier visita o reserva.',
  'Quinze appartements de la deuxième phase sont disponibles, et le promoteur fixe le prix de chacun. Chacun est listé avec une place de parking et un débarras, vendus sur des lignes distinctes. Nueva Living reconfirme le prix et la disponibilité avant toute visite ou réservation.',
  'Fünfzehn Wohnungen des zweiten Bauabschnitts sind verfügbar, und der Bauträger nennt für jede einen Preis. Jede ist mit einem Stellplatz und einem Abstellraum gelistet, die als eigene Positionen verkauft werden. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung erneut.',
  'Во второй очереди доступно пятнадцать квартир, и застройщик указывает цену каждой. Каждая значится с парковочным местом и кладовой, которые продаются отдельными позициями. Nueva Living заново подтверждает цену и наличие перед любым просмотром или бронированием.',
  'تتوفر خمس عشرة شقة في المرحلة الثانية، ويحدد المطوّر سعر كل منها. وتُدرج كل شقة مع موقف سيارة ومخزن يُباعان بندين منفصلين. تعيد Nueva Living تأكيد السعر والتوفر قبل أي معاينة أو حجز.',
  'Vijftien appartementen in de tweede fase zijn beschikbaar, en de ontwikkelaar noemt voor elk een prijs. Elk staat op de lijst met een parkeerplaats en een berging, die als aparte posten worden verkocht. Nueva Living bevestigt prijs en beschikbaarheid opnieuw vóór elke bezichtiging of reservering.',
  'Dostępnych jest piętnaście apartamentów drugiego etapu, a deweloper podaje cenę każdego z nich. Każdy figuruje z miejscem postojowym i komórką lokatorską, sprzedawanymi jako osobne pozycje. Nueva Living ponownie potwierdza cenę i dostępność przed każdą wizytą lub rezerwacją.',
  'Femten leiligheter i andre byggetrinn er ledige, og utbyggeren priser hver av dem. Hver står oppført med en parkeringsplass og en bod, som selges som egne linjer. Nueva Living bekrefter pris og tilgjengelighet på nytt før enhver visning eller reservasjon.',
  'Femton lägenheter i andra etappen är lediga, och exploatören prissätter var och en. Varje lägenhet listas med en parkeringsplats och ett förråd, som säljs som egna rader. Nueva Living bekräftar pris och tillgänglighet på nytt före varje visning eller bokning.')

SOURCE_EN = EN['availability']['sourceNote']
a(SOURCE_EN,
  'Disponibilidad y precios según el portal para agentes del promotor a 13 de noviembre de 2026, que se reconfirman antes de la reserva; plantas, superficies, dormitorios, baños y orientación proceden del mismo listado. El portal indica que su lista de precios es meramente informativa y carece de valor legal. Los precios corresponden solo a la vivienda y no incluyen el IVA ni los gastos de compra. Cada vivienda figura con una plaza de garaje y un trastero, y con ellos el subtotal del listado es {E24000} más alto en todas las líneas, de {E430000} a {E750000}. La superficie construida es la del propio listado: el plano del promotor de la vivienda 6-14-2-A coincide con el listado en la superficie útil interior y en la terraza, pero indica {N147.83} {U} construidos según el decreto andaluz de vivienda y {N173.54} {U} con zonas comunes, frente a {N136.01} {U} en el listado. La vivienda 6-14-2-A se muestra con su propio plano. Las viviendas 4-9-0-B, 4-9-1-B, 4-9-3-B y 5-11-2-A se muestran con el plano de otra vivienda de la misma planta cuya superficie útil y terraza coinciden al centésimo; en esos planos se han ocultado el título y el plano de situación, que ubican la otra vivienda, y la distribución puede estar en simetría. Ese plano de la 4-9-0-B muestra además un jardín de {N69.97} {U} que el listado no menciona, y el de la 5-11-2-A rotula su terraza con {N32.42} {U} en el dibujo frente a {N30.94} {U} en su propio cuadro y en el listado. Las otras diez viviendas no tienen plano en la documentación de que disponemos. Nueva Living reconfirma precio, estado, distribución y condiciones antes de cualquier reserva.',
  'Disponibilité et prix tels qu’indiqués sur le portail agents du promoteur au 13 novembre 2026, à reconfirmer avant réservation ; étages, surfaces, chambres, salles de bains et orientation proviennent de la même liste. Le portail précise que sa liste de prix est purement informative et sans valeur juridique. Les prix concernent le logement seul et s’entendent hors TVA et hors frais d’acquisition. Chaque logement est listé avec une place de parking et un débarras ; avec eux, le sous-total de la liste est supérieur de {E24000} sur chaque ligne, de {E430000} à {E750000}. La surface construite est celle de la liste : le plan du promoteur pour le logement 6-14-2-A concorde avec la liste pour la surface utile intérieure et la terrasse, mais indique {N147.83} {U} construits selon le décret andalou sur le logement et {N173.54} {U} parties communes comprises, contre {N136.01} {U} sur la liste. Le logement 6-14-2-A est présenté avec son propre plan. Les logements 4-9-0-B, 4-9-1-B, 4-9-3-B et 5-11-2-A sont présentés avec le plan d’un autre logement du même étage dont la surface utile et la terrasse sont identiques au centième ; le titre et le plan de situation de ces plans, qui localisent l’autre logement, sont masqués, et la distribution peut être inversée. Ce plan pour le 4-9-0-B montre en outre un jardin de {N69.97} {U} que la liste ne mentionne pas, et celui du 5-11-2-A indique une terrasse de {N32.42} {U} sur le dessin contre {N30.94} {U} dans son propre tableau et sur la liste. Les dix autres logements n’ont pas de plan dans les documents dont nous disposons. Nueva Living reconfirme le prix, le statut, la distribution et les conditions avant toute réservation.',
  'Verfügbarkeit und Preise laut Maklerportal des Bauträgers am 13. November 2026, vor einer Reservierung erneut bestätigt; Geschosse, Flächen, Schlafzimmer, Bäder und Ausrichtung stammen aus derselben Liste. Das Portal weist darauf hin, dass seine Preisliste nur der Information dient und keine Rechtswirkung hat. Die Preise gelten für die Wohnung allein und verstehen sich zuzüglich MwSt. und Erwerbsnebenkosten. Jede Wohnung ist mit einem Stellplatz und einem Abstellraum gelistet; mit beiden liegt die Zwischensumme der Liste in jeder Zeile um {E24000} höher, bei {E430000} bis {E750000}. Die bebaute Fläche ist die der Liste: Der Plan des Bauträgers für die Wohnung 6-14-2-A stimmt bei Wohnfläche innen und Terrasse mit der Liste überein, nennt aber {N147.83} {U} bebaute Fläche nach dem andalusischen Wohnungsdekret und {N173.54} {U} einschließlich Gemeinschaftsflächen, gegenüber {N136.01} {U} auf der Liste. Die Wohnung 6-14-2-A wird mit ihrem eigenen Plan gezeigt. Die Wohnungen 4-9-0-B, 4-9-1-B, 4-9-3-B und 5-11-2-A werden mit dem Plan einer anderen Wohnung desselben Geschosses gezeigt, deren Wohnfläche und Terrasse auf die Hundertstel übereinstimmen; Titel und Lageplan dieser Pläne, die die andere Wohnung verorten, sind abgedeckt, und der Grundriss kann gespiegelt sein. Dieser Plan für 4-9-0-B zeigt zudem einen Garten von {N69.97} {U}, den die Liste nicht erwähnt, und der für 5-11-2-A beschriftet die Terrasse in der Zeichnung mit {N32.42} {U} gegenüber {N30.94} {U} in seiner eigenen Tabelle und auf der Liste. Für die übrigen zehn Wohnungen enthalten unsere Unterlagen keinen Plan. Nueva Living bestätigt Preis, Status, Grundriss und Konditionen vor jeder Reservierung erneut.',
  'Наличие и цены — по порталу застройщика для агентов на 13 ноября 2026 года, с повторным подтверждением перед бронированием; этажи, площади, спальни, ванные комнаты и ориентация взяты из того же списка. Портал указывает, что его прайс-лист носит лишь информационный характер и не имеет юридической силы. Цены указаны только за квартиру, без НДС и расходов на оформление. Каждая квартира значится с парковочным местом и кладовой, и с ними промежуточный итог в каждой строке списка выше на {E24000} — от {E430000} до {E750000}. Площадь застройки взята из списка: план застройщика для квартиры 6-14-2-A совпадает со списком по полезной внутренней площади и террасе, но указывает {N147.83} {U} застройки по андалусскому жилищному декрету и {N173.54} {U} с учётом мест общего пользования против {N136.01} {U} в списке. Квартира 6-14-2-A показана со своим планом. Квартиры 4-9-0-B, 4-9-1-B, 4-9-3-B и 5-11-2-A показаны с планом другой квартиры на том же этаже, полезная площадь и терраса которой совпадают до сотых; заголовок и ситуационный план на этих чертежах, указывающие на другую квартиру, скрыты, а планировка может быть зеркальной. Этот план для 4-9-0-B к тому же показывает сад {N69.97} {U}, которого нет в списке, а на плане для 5-11-2-A терраса подписана как {N32.42} {U} на чертеже против {N30.94} {U} в его собственной таблице и в списке. Для остальных десяти квартир в имеющихся у нас документах планов нет. Nueva Living заново подтверждает цену, статус, планировку и условия перед любым бронированием.',
  'التوفر والأسعار كما وردت في بوابة الوكلاء لدى المطوّر بتاريخ 13 نوفمبر 2026، ويُعاد تأكيدها قبل الحجز، والطوابق والمساحات وغرف النوم والحمّامات والاتجاه مأخوذة من القائمة نفسها. وتنص البوابة على أن قائمة أسعارها للعلم فقط وليست لها قيمة قانونية. الأسعار للشقة وحدها ولا تشمل ضريبة القيمة المضافة ولا مصاريف التملك. وتُدرج كل شقة مع موقف سيارة ومخزن، ومعهما يزيد المجموع الفرعي في القائمة بمقدار {E24000} في كل سطر، من {E430000} إلى {E750000}. والمساحة المبنية هي رقم القائمة نفسها: مخطط المطوّر للشقة 6-14-2-A يطابق القائمة في المساحة الداخلية الصافية والتراس، لكنه يذكر {N147.83} {U} مبنية وفق مرسوم الإسكان الأندلسي و{N173.54} {U} مع المناطق المشتركة، مقابل {N136.01} {U} في القائمة. تُعرض الشقة 6-14-2-A بمخططها الخاص. أما الشقق 4-9-0-B و4-9-1-B و4-9-3-B و5-11-2-A فتُعرض بمخطط شقة أخرى في الطابق نفسه تتطابق مساحتها الصافية وتراسها حتى الجزء من مئة، وقد حُجب في تلك المخططات العنوان ومخطط الموقع اللذان يحددان مكان الشقة الأخرى، وقد يكون التوزيع معكوسًا. ويُظهر ذلك المخطط للشقة 4-9-0-B أيضًا حديقة مساحتها {N69.97} {U} لا تذكرها القائمة، ويكتب المخطط الخاص بالشقة 5-11-2-A مساحة التراس {N32.42} {U} على الرسم مقابل {N30.94} {U} في جدوله وفي القائمة. أما الشقق العشر الأخرى فلا مخطط لها في المستندات المتوفرة لدينا. تعيد Nueva Living تأكيد السعر والحالة والتوزيع والشروط قبل أي حجز.',
  'Beschikbaarheid en prijzen zoals vermeld in het agentenportaal van de ontwikkelaar op 13 november 2026, opnieuw bevestigd vóór reservering; verdiepingen, oppervlakten, slaapkamers, badkamers en oriëntatie komen uit dezelfde lijst. Het portaal vermeldt dat zijn prijslijst alleen ter informatie dient en geen juridische waarde heeft. De prijzen gelden voor de woning alleen en zijn exclusief btw en aankoopkosten. Elke woning staat op de lijst met een parkeerplaats en een berging, en daarmee ligt het subtotaal op elke regel {E24000} hoger, van {E430000} tot {E750000}. De bebouwde oppervlakte is die van de lijst zelf: de tekening van de ontwikkelaar voor woning 6-14-2-A komt met de lijst overeen in nuttige binnenoppervlakte en terras, maar noemt {N147.83} {U} bebouwd volgens het Andalusische woningdecreet en {N173.54} {U} inclusief gemeenschappelijke delen, tegen {N136.01} {U} op de lijst. Woning 6-14-2-A wordt getoond met haar eigen tekening. De woningen 4-9-0-B, 4-9-1-B, 4-9-3-B en 5-11-2-A worden getoond met de tekening van een andere woning op dezelfde verdieping waarvan nuttige oppervlakte en terras tot op de honderdste gelijk zijn; de titel en de situatietekening op die tekeningen, die de andere woning aanwijzen, zijn afgedekt, en de indeling kan gespiegeld zijn. Die tekening voor 4-9-0-B toont bovendien een tuin van {N69.97} {U} die de lijst niet noemt, en die voor 5-11-2-A vermeldt het terras als {N32.42} {U} in de tekening tegen {N30.94} {U} in de eigen tabel en op de lijst. Voor de andere tien woningen zit er geen tekening in de documenten die wij hebben. Nueva Living bevestigt prijs, status, indeling en voorwaarden opnieuw vóór elke reservering.',
  'Dostępność i ceny według portalu dla agentów dewelopera z 13 listopada 2026 r., potwierdzane ponownie przed rezerwacją; piętra, powierzchnie, sypialnie, łazienki i wystawa pochodzą z tej samej listy. Portal zaznacza, że jego cennik ma charakter wyłącznie informacyjny i nie ma mocy prawnej. Ceny dotyczą samego mieszkania i nie zawierają podatku VAT ani kosztów nabycia. Każde mieszkanie figuruje z miejscem postojowym i komórką lokatorską, a wraz z nimi suma częściowa na liście jest w każdym wierszu wyższa o {E24000}, od {E430000} do {E750000}. Powierzchnia zabudowy pochodzi z listy: rzut dewelopera dla mieszkania 6-14-2-A zgadza się z listą co do powierzchni użytkowej wewnątrz i tarasu, ale podaje {N147.83} {U} zabudowy według andaluzyjskiego dekretu mieszkaniowego i {N173.54} {U} z częściami wspólnymi, wobec {N136.01} {U} na liście. Mieszkanie 6-14-2-A pokazano z jego własnym rzutem. Mieszkania 4-9-0-B, 4-9-1-B, 4-9-3-B i 5-11-2-A pokazano z rzutem innego mieszkania na tym samym piętrze, którego powierzchnia użytkowa i taras zgadzają się co do setnej części; tytuł i plan sytuacyjny na tych rzutach, wskazujące inne mieszkanie, zostały zasłonięte, a układ może być lustrzanym odbiciem. Ten rzut dla 4-9-0-B pokazuje ponadto ogród o powierzchni {N69.97} {U}, o którym lista nie wspomina, a rzut dla 5-11-2-A opisuje taras na rysunku jako {N32.42} {U} wobec {N30.94} {U} we własnej tabeli i na liście. Dla pozostałych dziesięciu mieszkań w posiadanych przez nas dokumentach nie ma rzutu. Nueva Living ponownie potwierdza cenę, status, układ i warunki przed każdą rezerwacją.',
  'Tilgjengelighet og priser slik de er oppført i utbyggerens meglerportal 13. november 2026, bekreftet på nytt før reservasjon; etasjer, arealer, soverom, bad og retning kommer fra samme liste. Portalen opplyser at prislisten kun er til informasjon og ikke har juridisk gyldighet. Prisene gjelder boligen alene og er eksklusive mva og kjøpsomkostninger. Hver bolig står oppført med en parkeringsplass og en bod, og med dem er listens delsum {E24000} høyere på hver linje, fra {E430000} til {E750000}. Det bygde arealet er listens eget tall: utbyggerens tegning for bolig 6-14-2-A stemmer med listen for nyttbart innvendig areal og terrasse, men oppgir {N147.83} {U} bygget etter det andalusiske boligdekretet og {N173.54} {U} inkludert fellesarealer, mot {N136.01} {U} på listen. Bolig 6-14-2-A vises med sin egen tegning. Boligene 4-9-0-B, 4-9-1-B, 4-9-3-B og 5-11-2-A vises med tegningen av en annen bolig i samme etasje der nyttbart areal og terrasse er like på hundredelen; tittelen og situasjonsplanen på disse tegningene, som viser hvor den andre boligen ligger, er dekket over, og planløsningen kan være speilvendt. Den tegningen for 4-9-0-B viser dessuten en hage på {N69.97} {U} som listen ikke nevner, og den for 5-11-2-A angir terrassen til {N32.42} {U} på tegningen mot {N30.94} {U} i sin egen tabell og på listen. De ti øvrige boligene har ingen tegning i dokumentene vi har. Nueva Living bekrefter pris, status, planløsning og vilkår på nytt før enhver reservasjon.',
  'Tillgänglighet och priser enligt exploatörens mäklarportal den 13 november 2026, bekräftade på nytt före bokning; våningar, ytor, sovrum, badrum och väderstreck kommer från samma lista. Portalen anger att prislistan endast är informativ och saknar rättslig verkan. Priserna avser enbart bostaden och är exklusive IVA (spansk moms) och köpkostnader. Varje bostad listas med en parkeringsplats och ett förråd, och med dem är listans delsumma {E24000} högre på varje rad, från {E430000} till {E750000}. Byggytan är listans egen siffra: exploatörens ritning för bostad 6-14-2-A stämmer med listan för invändig nyttoyta och terrass, men anger {N147.83} {U} byggyta enligt det andalusiska bostadsdekretet och {N173.54} {U} inklusive gemensamma utrymmen, mot {N136.01} {U} på listan. Bostad 6-14-2-A visas med sin egen ritning. Bostäderna 4-9-0-B, 4-9-1-B, 4-9-3-B och 5-11-2-A visas med ritningen för en annan bostad på samma våning vars nyttoyta och terrass stämmer på hundradelen; rubriken och situationsplanen på de ritningarna, som visar var den andra bostaden ligger, är övertäckta, och planlösningen kan vara spegelvänd. Den ritningen för 4-9-0-B visar dessutom en trädgård på {N69.97} {U} som listan inte nämner, och den för 5-11-2-A anger terrassen till {N32.42} {U} på ritningen mot {N30.94} {U} i sin egen tabell och på listan. De övriga tio bostäderna saknar ritning i de handlingar vi har. Nueva Living bekräftar pris, status, planlösning och villkor på nytt före varje bokning.')

# ---------------------------------------------------------------- timeline and why
a('Second phase', 'Segunda fase', 'Deuxième phase', 'Zweiter Bauabschnitt', 'Вторая очередь', 'المرحلة الثانية',
  'Tweede fase', 'Drugi etap', 'Andre byggetrinn', 'Andra etappen')
a("The documents we hold give no delivery date and no payment schedule for this phase; the developer's portal shows construction as started. Nueva Living asks for both in writing, along with the building licence, before any money moves, and will not quote a date we cannot show you.",
  'La documentación de que disponemos no indica fecha de entrega ni calendario de pagos para esta fase; el portal del promotor muestra la obra como iniciada. Nueva Living solicita ambos por escrito, junto con la licencia de obras, antes de cualquier pago, y no le indicará una fecha que no pueda mostrarle.',
  'Les documents dont nous disposons ne donnent ni date de livraison ni échéancier de paiement pour cette phase ; le portail du promoteur indique que les travaux ont commencé. Nueva Living demande les deux par écrit, avec le permis de construire, avant tout versement, et ne vous annoncera pas une date qu’elle ne peut pas vous montrer.',
  'Die uns vorliegenden Unterlagen nennen für diesen Abschnitt weder einen Übergabetermin noch einen Zahlungsplan; das Portal des Bauträgers zeigt den Bau als begonnen. Nueva Living fordert beides schriftlich an, zusammen mit der Baugenehmigung, bevor Geld fließt, und nennt Ihnen keinen Termin, den wir Ihnen nicht belegen können.',
  'В имеющихся у нас документах нет ни срока сдачи, ни графика платежей для этой очереди; на портале застройщика строительство указано как начатое. Nueva Living запрашивает и то и другое письменно вместе с разрешением на строительство до любых платежей и не назовёт вам дату, которую не может подтвердить документом.',
  'لا تذكر المستندات المتوفرة لدينا موعدًا للتسليم ولا جدولًا للدفعات لهذه المرحلة، وتُظهر بوابة المطوّر أن البناء قد بدأ. تطلب Nueva Living الأمرين كتابةً مع رخصة البناء قبل دفع أي مبلغ، ولن نذكر لكم موعدًا لا نستطيع إثباته.',
  'De documenten die wij hebben noemen voor deze fase geen opleverdatum en geen betalingsschema; het portaal van de ontwikkelaar toont de bouw als gestart. Nueva Living vraagt beide schriftelijk op, samen met de bouwvergunning, voordat er geld wordt overgemaakt, en noemt u geen datum die wij niet kunnen laten zien.',
  'Posiadane przez nas dokumenty nie podają dla tego etapu ani terminu oddania, ani harmonogramu płatności; portal dewelopera pokazuje budowę jako rozpoczętą. Nueva Living występuje o jedno i drugie na piśmie, wraz z pozwoleniem na budowę, zanim nastąpi jakakolwiek płatność, i nie poda Państwu terminu, którego nie może udokumentować.',
  'Dokumentene vi har oppgir verken overtakelsesdato eller betalingsplan for dette byggetrinnet; utbyggerens portal viser byggingen som påbegynt. Nueva Living ber om begge deler skriftlig, sammen med byggetillatelsen, før penger overføres, og oppgir ingen dato vi ikke kan dokumentere.',
  'Handlingarna vi har anger varken tillträdesdatum eller betalningsplan för denna etapp; exploatörens portal visar bygget som påbörjat. Nueva Living begär båda skriftligt, tillsammans med bygglovet, innan några pengar betalas, och anger inget datum vi inte kan visa er.')
a('Fifteen apartments available in the second phase of a gated scheme of 105 homes over two phases.',
  'Quince apartamentos disponibles en la segunda fase de un conjunto cerrado de 105 viviendas en dos fases.',
  'Quinze appartements disponibles dans la deuxième phase d’une résidence fermée de 105 logements en deux phases.',
  'Fünfzehn verfügbare Wohnungen im zweiten Bauabschnitt einer geschlossenen Anlage mit 105 Wohnungen in zwei Abschnitten.',
  'Пятнадцать доступных квартир во второй очереди закрытого комплекса на 105 квартир в двух очередях.',
  'خمس عشرة شقة متاحة في المرحلة الثانية من مجمع مغلق يضم 105 مساكن على مرحلتين.',
  'Vijftien beschikbare appartementen in de tweede fase van een besloten complex met 105 woningen in twee fasen.',
  'Piętnaście dostępnych apartamentów w drugim etapie osiedla zamkniętego liczącego 105 mieszkań w dwóch etapach.',
  'Femten ledige leiligheter i andre byggetrinn av et lukket anlegg med 105 boliger i to byggetrinn.',
  'Femton lediga lägenheter i andra etappen av ett slutet område med 105 bostäder i två etapper.')
a('Buyers who want a deep terrace and a full set of communal amenities on the western side of Estepona.',
  'Compradores que buscan una terraza amplia y unas zonas comunes completas en la zona oeste de Estepona.',
  'Les acquéreurs qui recherchent une grande terrasse et des espaces communs complets à l’ouest d’Estepona.',
  'Käufer, die eine tiefe Terrasse und umfassende Gemeinschaftseinrichtungen im Westen von Estepona suchen.',
  'Покупателям, которым нужна глубокая терраса и полный набор общих удобств в западной части Эстепоны.',
  'للمشترين الذين يريدون تراسًا واسعًا ومرافق مشتركة متكاملة في الجهة الغربية من إستيبونا.',
  'Kopers die een diep terras en een volledig pakket gemeenschappelijke voorzieningen willen aan de westkant van Estepona.',
  'Dla kupujących, którzy chcą głębokiego tarasu i pełnego zestawu udogodnień wspólnych w zachodniej części Estepony.',
  'Kjøpere som ønsker en dyp terrasse og et komplett sett fellesfasiliteter på vestsiden av Estepona.',
  'Köpare som vill ha en djup terrass och ett komplett utbud av gemensamma faciliteter på Esteponas västra sida.')
a("Warm-water underfloor heating, terraces of up to 98.60 sqm, and two adult pools, a children's pool, a gym and a social club inside the gates.",
  'Suelo radiante por agua templada, terrazas de hasta {N98.60} {U} y, dentro del recinto, dos piscinas para adultos, una infantil, gimnasio y club social.',
  'Plancher chauffant à eau tiède, des terrasses jusqu’à {N98.60} {U} et, dans l’enceinte, deux piscines pour adultes, une pour enfants, une salle de sport et un club social.',
  'Fußbodenheizung mit Warmwasser, Terrassen bis {N98.60} {U} und innerhalb der Anlage zwei Erwachsenenpools, ein Kinderbecken, ein Fitnessraum und ein Clubraum.',
  'Водяные тёплые полы, террасы до {N98.60} {U}, а за оградой комплекса — два взрослых бассейна, детский бассейн, тренажёрный зал и клуб.',
  'تدفئة أرضية بالماء الدافئ، وتراسات تصل إلى {N98.60} {U}، وداخل الأسوار مسبحان للبالغين ومسبح للأطفال وصالة رياضة ونادٍ اجتماعي.',
  'Vloerverwarming op warm water, terrassen tot {N98.60} {U} en binnen de poort twee zwembaden voor volwassenen, een kinderbad, een fitnessruimte en een clubruimte.',
  'Wodne ogrzewanie podłogowe, tarasy do {N98.60} {U}, a na terenie osiedla dwa baseny dla dorosłych, brodzik, siłownia i klub dla mieszkańców.',
  'Vannbåren gulvvarme, terrasser på opptil {N98.60} {U}, og innenfor portene to voksenbassenger, et barnebasseng, treningsrom og fellesklubb.',
  'Vattenburen golvvärme, terrasser på upp till {N98.60} {U}, och innanför grindarna två pooler för vuxna, en barnpool, ett gym och en klubblokal.')
a('The beach is about eight minutes on foot, the port of Estepona about seven minutes by car and the town centre about eleven.',
  'La playa está a unos ocho minutos a pie, el puerto de Estepona a unos siete minutos en coche y el centro a unos once.',
  'La plage est à environ huit minutes à pied, le port d’Estepona à environ sept minutes en voiture et le centre-ville à environ onze.',
  'Der Strand ist zu Fuß etwa acht Minuten entfernt, der Hafen von Estepona mit dem Auto etwa sieben Minuten und das Zentrum etwa elf.',
  'До пляжа около восьми минут пешком, до порта Эстепоны около семи минут на машине, до центра города около одиннадцати.',
  'يبعد الشاطئ نحو ثماني دقائق سيرًا على الأقدام، وميناء إستيبونا نحو سبع دقائق بالسيارة، ووسط المدينة نحو إحدى عشرة دقيقة.',
  'Het strand ligt op ongeveer acht minuten lopen, de haven van Estepona op ongeveer zeven minuten met de auto en het centrum op ongeveer elf.',
  'Do plaży jest około ośmiu minut pieszo, do portu w Esteponie około siedmiu minut samochodem, a do centrum około jedenastu.',
  'Stranden ligger omtrent åtte minutter til fots unna, havnen i Estepona omtrent sju minutter med bil og sentrum omtrent elleve.',
  'Stranden ligger ungefär åtta minuter till fots bort, Esteponas hamn ungefär sju minuter med bil och centrum ungefär elva.')

# ---------------------------------------------------------------- investment and trust
a('Western <em>Estepona</em>', 'La zona oeste de <em>Estepona</em>', 'L’ouest d’<em>Estepona</em>',
  'Der Westen von <em>Estepona</em>', 'Запад <em>Эстепоны</em>', 'غرب <em>إستيبونا</em>',
  'De westkant van <em>Estepona</em>', 'Zachodnia <em>Estepona</em>', 'Vestlige <em>Estepona</em>',
  'Västra <em>Estepona</em>')
a('Fifteen homes are listed in this phase, so the choice of floor, terrace and orientation is limited to those.',
  'En esta fase figuran quince viviendas, así que la elección de planta, terraza y orientación se limita a ellas.',
  'Quinze logements sont listés dans cette phase : le choix d’étage, de terrasse et d’orientation se limite donc à ceux-ci.',
  'In diesem Abschnitt sind fünfzehn Wohnungen gelistet, die Wahl von Geschoss, Terrasse und Ausrichtung beschränkt sich also auf diese.',
  'В этой очереди в списке пятнадцать квартир, поэтому выбор этажа, террасы и ориентации ограничен ими.',
  'تُدرج في هذه المرحلة خمس عشرة شقة، لذا يقتصر اختيار الطابق والتراس والاتجاه عليها.',
  'In deze fase staan vijftien woningen op de lijst, dus de keuze in verdieping, terras en oriëntatie is daartoe beperkt.',
  'W tym etapie na liście jest piętnaście mieszkań, więc wybór piętra, tarasu i wystawy ogranicza się do nich.',
  'Femten boliger er oppført i dette byggetrinnet, så valget av etasje, terrasse og retning er begrenset til disse.',
  'Femton bostäder finns listade i denna etapp, så valet av våning, terrass och väderstreck är begränsat till dem.')
a('La Gaspara lies on the western side of Estepona with the A-7 alongside, which puts Marbella one way and Sotogrande the other.',
  'La Gaspara está en la zona oeste de Estepona, junto a la A-7, con Marbella en una dirección y Sotogrande en la otra.',
  'La Gaspara se trouve à l’ouest d’Estepona, le long de l’A-7, avec Marbella d’un côté et Sotogrande de l’autre.',
  'La Gaspara liegt im Westen von Estepona direkt an der A-7, mit Marbella in der einen und Sotogrande in der anderen Richtung.',
  'Ла-Гаспара находится в западной части Эстепоны у трассы A-7: в одну сторону Марбелья, в другую Сотогранде.',
  'تقع لا غاسبارا في الجهة الغربية من إستيبونا بجوار الطريق A-7، فتكون ماربيا في اتجاه وسوتوغراندي في الاتجاه الآخر.',
  'La Gaspara ligt aan de westkant van Estepona langs de A-7, met Marbella aan de ene en Sotogrande aan de andere kant.',
  'La Gaspara leży w zachodniej części Estepony przy A-7, z Marbellą w jedną stronę i Sotogrande w drugą.',
  'La Gaspara ligger på vestsiden av Estepona langs A-7, med Marbella i den ene retningen og Sotogrande i den andre.',
  'La Gaspara ligger på Esteponas västra sida längs A-7, med Marbella åt ena hållet och Sotogrande åt det andra.')
a('That the home, its terrace, its parking space and its storeroom are registered as described.',
  'Que la vivienda, su terraza, su plaza de garaje y su trastero estén inscritos tal como se describen.',
  'Que le logement, sa terrasse, sa place de parking et son débarras sont inscrits tels que décrits.',
  'Dass Wohnung, Terrasse, Stellplatz und Abstellraum wie beschrieben eingetragen sind.',
  'Что квартира, её терраса, парковочное место и кладовая зарегистрированы так, как описано.',
  'أن الشقة وتراسها وموقف سيارتها ومخزنها مسجلة كما هو موصوف.',
  'Dat de woning, het terras, de parkeerplaats en de berging zijn ingeschreven zoals beschreven.',
  'Że mieszkanie, jego taras, miejsce postojowe i komórka lokatorska są wpisane do rejestru zgodnie z opisem.',
  'At boligen, terrassen, parkeringsplassen og boden er tinglyst slik de er beskrevet.',
  'Att bostaden, terrassen, parkeringsplatsen och förrådet är registrerade så som de beskrivs.')
a('The documents give none for this phase; we ask for it in writing and put it in the contract.',
  'La documentación no indica ninguna para esta fase; la solicitamos por escrito y la incluimos en el contrato.',
  'Les documents n’en donnent aucune pour cette phase ; nous la demandons par écrit et l’inscrivons au contrat.',
  'Die Unterlagen nennen für diesen Abschnitt keinen; wir fordern ihn schriftlich an und nehmen ihn in den Vertrag auf.',
  'В документах для этой очереди её нет; мы запрашиваем её письменно и вносим в договор.',
  'لا تذكر المستندات أي موعد لهذه المرحلة، لذا نطلبه كتابةً وندرجه في العقد.',
  'De documenten noemen er geen voor deze fase; wij vragen hem schriftelijk op en nemen hem op in het contract.',
  'Dokumenty nie podają go dla tego etapu; występujemy o niego na piśmie i wpisujemy go do umowy.',
  'Dokumentene oppgir ingen for dette byggetrinnet; vi ber om den skriftlig og tar den inn i kontrakten.',
  'Handlingarna anger inget för denna etapp; vi begär det skriftligt och för in det i avtalet.')

# ---------------------------------------------------------------- architecture
a('Terraces, <em>floor by floor</em>', 'Terrazas, <em>planta a planta</em>', 'Des terrasses, <em>étage par étage</em>',
  'Terrassen, <em>Geschoss für Geschoss</em>', 'Террасы, <em>этаж за этажом</em>', 'تراسات، <em>طابقًا بعد طابق</em>',
  'Terrassen, <em>verdieping na verdieping</em>', 'Tarasy, <em>piętro po piętrze</em>', 'Terrasser, <em>etasje for etasje</em>',
  'Terrasser, <em>våning för våning</em>')
a('Long, low blocks step back floor by floor, so the terraces run the length of each façade. The façades are a painted render over a double leaf of brick and drywall, with an insulated air cavity between them.',
  'Bloques largos y bajos que se retranquean planta a planta, de modo que las terrazas recorren toda la fachada. Las fachadas son de revestimiento continuo pintado sobre una doble hoja de ladrillo y tabiquería seca, con una cámara de aire aislada entre ambas.',
  'De longs immeubles bas en retrait d’étage en étage, de sorte que les terrasses courent sur toute la longueur de chaque façade. Les façades sont en enduit peint sur une double paroi de brique et de plaque de plâtre, avec une lame d’air isolée entre les deux.',
  'Lange, niedrige Blöcke springen Geschoss für Geschoss zurück, sodass die Terrassen über die ganze Länge jeder Fassade laufen. Die Fassaden sind verputzt und gestrichen, auf einer zweischaligen Wand aus Ziegel und Trockenbau mit gedämmter Luftschicht dazwischen.',
  'Длинные невысокие корпуса отступают этаж за этажом, и террасы тянутся вдоль всего фасада. Фасады — окрашенная штукатурка по двойной стене из кирпича и гипсокартона с утеплённой воздушной прослойкой между ними.',
  'مبانٍ طويلة منخفضة تتراجع طابقًا بعد طابق، فتمتد التراسات على طول كل واجهة. والواجهات من لياسة مطلية فوق جدار مزدوج من الطوب والألواح الجافة، بينهما فراغ هوائي معزول.',
  'Lange, lage blokken springen per verdieping terug, zodat de terrassen over de hele lengte van elke gevel lopen. De gevels zijn geschilderd stucwerk op een dubbele wand van baksteen en droogbouw, met een geïsoleerde spouw daartussen.',
  'Długie, niskie budynki cofają się piętro po piętrze, dzięki czemu tarasy biegną przez całą długość każdej elewacji. Elewacje to malowany tynk na ścianie dwuwarstwowej z cegły i płyt gipsowo-kartonowych, z ocieploną pustką powietrzną pomiędzy nimi.',
  'Lange, lave bygg trappes tilbake etasje for etasje, slik at terrassene går langs hele fasaden. Fasadene er malt puss på en dobbel vegg av tegl og gipsplater, med en isolert luftspalte imellom.',
  'Långa, låga hus trappas tillbaka våning för våning, så att terrasserna löper längs hela fasaden. Fasaderna är målad puts på en dubbel vägg av tegel och gipsskivor, med en isolerad luftspalt emellan.')
a('The scheme', 'El conjunto', 'La résidence', 'Die Anlage', 'Комплекс', 'المجمع', 'Het complex', 'Osiedle', 'Anlegget', 'Området')
a("105 homes over two phases in the developer's dossier, of two, three and four bedrooms; this phase lists fifteen apartments of two and three bedrooms.",
  '105 viviendas en dos fases según el dossier del promotor, de dos, tres y cuatro dormitorios; en esta fase figuran quince apartamentos de dos y tres dormitorios.',
  '105 logements en deux phases selon le dossier du promoteur, de deux, trois et quatre chambres ; cette phase liste quinze appartements de deux et trois chambres.',
  'Laut Exposé des Bauträgers 105 Wohnungen in zwei Abschnitten mit zwei, drei und vier Schlafzimmern; dieser Abschnitt listet fünfzehn Wohnungen mit zwei und drei Schlafzimmern.',
  'По каталогу застройщика — 105 квартир в двух очередях, с двумя, тремя и четырьмя спальнями; в этой очереди в списке пятнадцать квартир с двумя и тремя спальнями.',
  '105 مساكن على مرحلتين وفق كتيّب المطوّر، بغرفتين وثلاث وأربع غرف نوم، وتضم قائمة هذه المرحلة خمس عشرة شقة بغرفتين أو ثلاث.',
  '105 woningen in twee fasen volgens het dossier van de ontwikkelaar, met twee, drie en vier slaapkamers; deze fase telt vijftien appartementen met twee en drie slaapkamers.',
  '105 mieszkań w dwóch etapach według broszury dewelopera, z dwiema, trzema i czterema sypialniami; ten etap obejmuje piętnaście apartamentów z dwiema i trzema sypialniami.',
  '105 boliger i to byggetrinn ifølge utbyggerens salgsprospekt, med to, tre og fire soverom; dette byggetrinnet har femten leiligheter med to og tre soverom.',
  '105 bostäder i två etapper enligt exploatörens prospekt, med två, tre och fyra sovrum; denna etapp listar femton lägenheter med två och tre sovrum.')
a('From 27.79 to 98.60 sqm on the available homes, paved in non-slip stoneware, with water, drainage, lighting, a power socket and a TV socket on each.',
  'De {N27.79} a {N98.60} {U} en las viviendas disponibles, solados con gres antideslizante, con toma de agua, desagüe, iluminación, enchufe y toma de televisión en cada una.',
  'De {N27.79} à {N98.60} {U} sur les logements disponibles, en grès antidérapant, avec arrivée d’eau, évacuation, éclairage, prise électrique et prise TV sur chacune.',
  'Bei den verfügbaren Wohnungen {N27.79} bis {N98.60} {U}, mit rutschfestem Feinsteinzeug belegt, jeweils mit Wasseranschluss, Ablauf, Beleuchtung, Steckdose und TV-Anschluss.',
  'От {N27.79} до {N98.60} {U} в доступных квартирах, с противоскользящим керамогранитом, на каждой есть подвод воды, слив, освещение, розетка и ТВ-розетка.',
  'من {N27.79} إلى {N98.60} {U} في الشقق المتاحة، مكسوة ببلاط حجري مانع للانزلاق، وفي كل منها مأخذ ماء وتصريف وإضاءة ومقبس كهرباء ومقبس تلفاز.',
  'Van {N27.79} tot {N98.60} {U} bij de beschikbare woningen, belegd met antislip keramiek, elk met wateraansluiting, afvoer, verlichting, stopcontact en tv-aansluiting.',
  'Od {N27.79} do {N98.60} {U} w dostępnych mieszkaniach, wyłożone antypoślizgowym gresem, każdy z punktem wody, odpływem, oświetleniem, gniazdkiem i gniazdem TV.',
  'Fra {N27.79} til {N98.60} {U} på de ledige boligene, lagt med sklisikre keramiske fliser, hver med vanntilførsel, sluk, belysning, stikkontakt og TV-uttak.',
  'Från {N27.79} till {N98.60} {U} på de lediga bostäderna, belagda med halkfritt stengods, var och en med vattenuttag, avlopp, belysning, eluttag och tv-uttag.')
a('Porcelain stoneware floors, suspended ceilings throughout, white lacquered doors 220 cm high and fitted wardrobes with modular interiors.',
  'Suelos de gres porcelánico, falsos techos en toda la vivienda, puertas lacadas en blanco de 220 cm de altura y armarios empotrados con interior modular.',
  'Sols en grès cérame, faux plafonds partout, portes laquées blanches de 220 cm de haut et placards intégrés à aménagement modulable.',
  'Böden aus Feinsteinzeug, abgehängte Decken überall, weiß lackierte Türen mit 220 cm Höhe und Einbauschränke mit modularer Inneneinteilung.',
  'Полы из керамогранита, подвесные потолки по всей квартире, белые лакированные двери высотой 220 см и встроенные шкафы с модульным наполнением.',
  'أرضيات من البورسلان، وأسقف معلقة في كامل الشقة، وأبواب بيضاء مطلية بارتفاع 220 سم، وخزائن مدمجة بتقسيمات داخلية معيارية.',
  'Vloeren van keramische tegels, verlaagde plafonds overal, wit gelakte deuren van 220 cm hoog en inbouwkasten met modulaire indeling.',
  'Podłogi z gresu porcelanowego, sufity podwieszane w całym mieszkaniu, białe lakierowane drzwi o wysokości 220 cm i szafy wnękowe z modułowym wnętrzem.',
  'Gulv i porselensfliser, nedforede himlinger overalt, hvitlakkerte dører på 220 cm og innebygde garderobeskap med modulær innredning.',
  'Golv av porslinsklinker, undertak i hela bostaden, vitlackerade dörrar på 220 cm och inbyggda garderober med modulär inredning.')
a('Warm-water underfloor heating, electric in the bathrooms, with ducted cooling to the living room and bedrooms.',
  'Suelo radiante por agua templada, eléctrico en los baños, con climatización por conductos en salón y dormitorios.',
  'Plancher chauffant à eau tiède, électrique dans les salles de bains, avec rafraîchissement par gaines dans le séjour et les chambres.',
  'Fußbodenheizung mit Warmwasser, in den Bädern elektrisch, mit Kühlung über Kanäle in Wohnraum und Schlafzimmern.',
  'Водяные тёплые полы, электрические в ванных, с канальным охлаждением в гостиной и спальнях.',
  'تدفئة أرضية بالماء الدافئ، وكهربائية في الحمّامات، مع تبريد بقنوات في صالة المعيشة وغرف النوم.',
  'Vloerverwarming op warm water, elektrisch in de badkamers, met koeling via kanalen in woonkamer en slaapkamers.',
  'Wodne ogrzewanie podłogowe, elektryczne w łazienkach, z chłodzeniem kanałowym w salonie i sypialniach.',
  'Vannbåren gulvvarme, elektrisk på badene, med kjøling via kanaler i stue og soverom.',
  'Vattenburen golvvärme, elektrisk i badrummen, med kylning via kanaler i vardagsrum och sovrum.')
a('An aerothermal heat pump for hot water, thermally broken aluminium with double glazing and motorised insulated blinds; the drawings carry a provisional A rating.',
  'Bomba de calor aerotérmica para el agua caliente, carpintería de aluminio con rotura de puente térmico y doble acristalamiento, y persianas motorizadas con aislamiento; los planos llevan una calificación A provisional.',
  'Pompe à chaleur aérothermique pour l’eau chaude, menuiseries aluminium à rupture de pont thermique avec double vitrage et volets motorisés isolés ; les plans affichent une étiquette A provisoire.',
  'Luft-Wärmepumpe für das Warmwasser, thermisch getrenntes Aluminium mit Doppelverglasung und motorisierte, gedämmte Rollläden; die Pläne tragen eine vorläufige Energieklasse A.',
  'Аэротермальный тепловой насос для горячей воды, алюминиевые рамы с терморазрывом и двойным остеклением, моторизованные утеплённые жалюзи; на планах указан предварительный класс энергоэффективности A.',
  'مضخة حرارية هوائية للمياه الساخنة، ونجارة ألمنيوم بعازل حراري وزجاج مزدوج، وستائر معزولة بمحرك، وتحمل المخططات تصنيف طاقة A مبدئيًا.',
  'Een luchtwarmtepomp voor warm water, thermisch onderbroken aluminium met dubbele beglazing en gemotoriseerde, geïsoleerde rolluiken; de tekeningen vermelden een voorlopig A-label.',
  'Aerotermiczna pompa ciepła do ciepłej wody, aluminiowa stolarka z przekładką termiczną i podwójnym szkleniem oraz zmotoryzowane, ocieplane rolety; rzuty podają tymczasową klasę energetyczną A.',
  'En luft-til-vann-varmepumpe for varmtvann, aluminium med kuldebrudd og doble glass og motoriserte, isolerte rullegardiner; tegningene oppgir en foreløpig energiklasse A.',
  'En luft-vatten-värmepump för varmvatten, aluminium med köldbryggsbrytning och dubbelglas samt motoriserade, isolerade rullgardiner; ritningarna anger en preliminär energiklass A.')
a('Automatic garage doors on a remote control, a parking space and a storeroom listed with every home, and pre-installation for electric vehicle charging.',
  'Puertas de garaje automáticas con mando a distancia, una plaza de garaje y un trastero en el listado de cada vivienda, y preinstalación para la carga de vehículos eléctricos.',
  'Portes de garage automatiques avec télécommande, une place de parking et un débarras listés avec chaque logement, et une pré-installation pour la recharge des véhicules électriques.',
  'Automatische Garagentore mit Fernbedienung, ein Stellplatz und ein Abstellraum zu jeder Wohnung gelistet und eine Vorinstallation für das Laden von Elektrofahrzeugen.',
  'Автоматические ворота гаража с пультом, парковочное место и кладовая в списке для каждой квартиры и подготовка под зарядку электромобилей.',
  'أبواب مرآب آلية بجهاز تحكم عن بعد، وموقف سيارة ومخزن مدرجان مع كل شقة، وتمديدات مسبقة لشحن السيارات الكهربائية.',
  'Automatische garagedeuren met afstandsbediening, een parkeerplaats en een berging bij elke woning op de lijst, en voorbereiding voor het laden van elektrische auto’s.',
  'Automatyczne bramy garażowe na pilota, miejsce postojowe i komórka lokatorska przypisane na liście do każdego mieszkania oraz przygotowanie do ładowania samochodów elektrycznych.',
  'Automatiske garasjeporter med fjernkontroll, en parkeringsplass og en bod oppført med hver bolig, og forberedt for lading av elbil.',
  'Automatiska garageportar med fjärrkontroll, en parkeringsplats och ett förråd listade med varje bostad, och förberett för laddning av elbil.')

# ---------------------------------------------------------------- lifestyle and viewing
a('La Gaspara, <em>western Estepona</em>', 'La Gaspara, <em>al oeste de Estepona</em>',
  'La Gaspara, <em>à l’ouest d’Estepona</em>', 'La Gaspara, <em>im Westen von Estepona</em>',
  'Ла-Гаспара, <em>запад Эстепоны</em>', 'لا غاسبارا، <em>غرب إستيبونا</em>',
  'La Gaspara, <em>westelijk Estepona</em>', 'La Gaspara, <em>zachodnia Estepona</em>',
  'La Gaspara, <em>vestlige Estepona</em>', 'La Gaspara, <em>västra Estepona</em>')
a("The western side of Estepona, with the A-7 alongside, the beach a short walk below and the town and its port a few minutes' drive east.",
  'La zona oeste de Estepona, junto a la A-7, con la playa a un corto paseo y el centro y el puerto a pocos minutos en coche hacia el este.',
  'L’ouest d’Estepona, le long de l’A-7, avec la plage à quelques pas en contrebas et la ville et son port à quelques minutes de voiture vers l’est.',
  'Der Westen von Estepona, direkt an der A-7, mit dem Strand wenige Gehminuten unterhalb und der Stadt mit ihrem Hafen ein paar Autominuten östlich.',
  'Запад Эстепоны у трассы A-7: пляж в нескольких минутах ходьбы внизу, а город и порт в нескольких минутах езды на восток.',
  'الجهة الغربية من إستيبونا بجوار الطريق A-7، والشاطئ على مسافة قصيرة سيرًا في الأسفل، والمدينة ومرساها على بعد دقائق بالسيارة شرقًا.',
  'De westkant van Estepona, langs de A-7, met het strand op korte loopafstand beneden en de stad en de haven een paar minuten rijden naar het oosten.',
  'Zachodnia część Estepony przy A-7, z plażą kilka minut pieszo w dole oraz miastem i portem kilka minut jazdy na wschód.',
  'Vestsiden av Estepona langs A-7, med stranden en kort spasertur nedenfor og byen og havnen noen minutters kjøring østover.',
  'Esteponas västra sida längs A-7, med stranden en kort promenad nedanför och staden och dess hamn några minuters bilresa österut.')
a('The nearest beach is about eight minutes on foot, on the far side of the A-7.',
  'La playa más cercana está a unos ocho minutos a pie, al otro lado de la A-7.',
  'La plage la plus proche est à environ huit minutes à pied, de l’autre côté de l’A-7.',
  'Der nächste Strand liegt etwa acht Gehminuten entfernt auf der anderen Seite der A-7.',
  'Ближайший пляж примерно в восьми минутах ходьбы, по другую сторону трассы A-7.',
  'يبعد أقرب شاطئ نحو ثماني دقائق سيرًا على الأقدام، على الجانب الآخر من الطريق A-7.',
  'Het dichtstbijzijnde strand ligt op ongeveer acht minuten lopen, aan de andere kant van de A-7.',
  'Najbliższa plaża jest około ośmiu minut pieszo, po drugiej stronie A-7.',
  'Nærmeste strand ligger omtrent åtte minutter til fots unna, på den andre siden av A-7.',
  'Närmaste strand ligger ungefär åtta minuter till fots bort, på andra sidan A-7.')
a('Estepona Golf is about eight minutes by car and Finca Cortesín about ten.',
  'Estepona Golf está a unos ocho minutos en coche y Finca Cortesín a unos diez.',
  'Estepona Golf est à environ huit minutes en voiture et Finca Cortesín à environ dix.',
  'Estepona Golf ist mit dem Auto etwa acht Minuten entfernt, Finca Cortesín etwa zehn.',
  'До Estepona Golf около восьми минут на машине, до Finca Cortesín около десяти.',
  'يبعد نادي Estepona Golf نحو ثماني دقائق بالسيارة، وFinca Cortesín نحو عشر دقائق.',
  'Estepona Golf ligt op ongeveer acht minuten rijden en Finca Cortesín op ongeveer tien.',
  'Do Estepona Golf jest około ośmiu minut samochodem, a do Finca Cortesín około dziesięciu.',
  'Estepona Golf ligger omtrent åtte minutter unna med bil og Finca Cortesín omtrent ti.',
  'Estepona Golf ligger ungefär åtta minuter bort med bil och Finca Cortesín ungefär tio.')
a('The port of Estepona is about seven minutes and the town centre about eleven, the A-7 runs alongside towards Marbella and Sotogrande, and Gibraltar airport is about forty-two minutes.',
  'El puerto de Estepona está a unos siete minutos y el centro a unos once; la A-7 pasa junto al conjunto hacia Marbella y Sotogrande, y el aeropuerto de Gibraltar está a unos cuarenta y dos minutos.',
  'Le port d’Estepona est à environ sept minutes et le centre-ville à environ onze ; l’A-7 longe la résidence vers Marbella et Sotogrande, et l’aéroport de Gibraltar est à environ quarante-deux minutes.',
  'Der Hafen von Estepona ist etwa sieben Minuten entfernt, das Zentrum etwa elf; die A-7 führt direkt vorbei Richtung Marbella und Sotogrande, und der Flughafen Gibraltar liegt etwa zweiundvierzig Minuten entfernt.',
  'До порта Эстепоны около семи минут, до центра около одиннадцати; рядом проходит трасса A-7 в сторону Марбельи и Сотогранде, а до аэропорта Гибралтара около сорока двух минут.',
  'يبعد ميناء إستيبونا نحو سبع دقائق ووسط المدينة نحو إحدى عشرة دقيقة، ويمر الطريق A-7 بمحاذاة المجمع نحو ماربيا وسوتوغراندي، ويبعد مطار جبل طارق نحو اثنتين وأربعين دقيقة.',
  'De haven van Estepona ligt op ongeveer zeven minuten en het centrum op ongeveer elf; de A-7 loopt langs het complex richting Marbella en Sotogrande, en de luchthaven van Gibraltar ligt op ongeveer tweeënveertig minuten.',
  'Do portu w Esteponie jest około siedmiu minut, a do centrum około jedenastu; tuż obok biegnie A-7 w stronę Marbelli i Sotogrande, a lotnisko w Gibraltarze jest około czterdziestu dwóch minut drogi.',
  'Havnen i Estepona ligger omtrent sju minutter unna og sentrum omtrent elleve; A-7 går like ved mot Marbella og Sotogrande, og Gibraltar lufthavn ligger omtrent førtito minutter unna.',
  'Esteponas hamn ligger ungefär sju minuter bort och centrum ungefär elva; A-7 går alldeles intill mot Marbella och Sotogrande, och Gibraltars flygplats ligger ungefär fyrtiotvå minuter bort.')
a('Standing on the site is the fastest way to judge what each terrace looks at and how the blocks sit around the pools.',
  'Estar en el lugar es la forma más rápida de valorar hacia dónde mira cada terraza y cómo se sitúan los bloques alrededor de las piscinas.',
  'Se rendre sur place est le moyen le plus rapide de juger de la vue de chaque terrasse et de la disposition des immeubles autour des piscines.',
  'Vor Ort zu stehen ist der schnellste Weg, um zu beurteilen, worauf jede Terrasse blickt und wie die Blöcke um die Pools angeordnet sind.',
  'Побывать на месте — самый быстрый способ понять, куда выходит каждая терраса и как корпуса расположены вокруг бассейнов.',
  'الوقوف في الموقع هو أسرع طريقة لتقدير ما يطل عليه كل تراس وكيف تتوزع المباني حول المسابح.',
  'Ter plaatse staan is de snelste manier om te beoordelen waarop elk terras uitkijkt en hoe de blokken rond de zwembaden liggen.',
  'Wizyta na miejscu to najszybszy sposób, by ocenić, na co wychodzi każdy taras i jak budynki rozmieszczone są wokół basenów.',
  'Å stå på tomten er den raskeste måten å vurdere hva hver terrasse ser ut mot, og hvordan byggene ligger rundt bassengene.',
  'Att stå på platsen är det snabbaste sättet att bedöma vad varje terrass vetter mot och hur husen ligger kring poolerna.')
a('See where the second-phase blocks sit within the scheme and how far apart they are.',
  'Vea dónde se sitúan los bloques de la segunda fase dentro del conjunto y qué distancia hay entre ellos.',
  'Voyez où se situent les immeubles de la deuxième phase dans la résidence et à quelle distance ils sont les uns des autres.',
  'Sehen Sie, wo die Blöcke des zweiten Abschnitts in der Anlage liegen und wie weit sie voneinander entfernt sind.',
  'Посмотрите, где в комплексе расположены корпуса второй очереди и на каком расстоянии друг от друга.',
  'شاهدوا موقع مباني المرحلة الثانية داخل المجمع والمسافة بينها.',
  'Bekijk waar de blokken van de tweede fase in het complex liggen en hoe ver ze uit elkaar staan.',
  'Proszę zobaczyć, gdzie na osiedlu stoją budynki drugiego etapu i jak daleko są od siebie.',
  'Se hvor byggene i andre byggetrinn ligger i anlegget, og hvor langt fra hverandre de står.',
  'Se var husen i andra etappen ligger inom området och hur långt ifrån varandra de står.')
a('Compare what each floor and orientation looks at, towards the sea or the hills.',
  'Compare las vistas de cada planta y orientación, hacia el mar o hacia las colinas.',
  'Comparez ce que voit chaque étage et chaque orientation, vers la mer ou vers les collines.',
  'Vergleichen Sie, worauf jedes Geschoss und jede Ausrichtung blickt, aufs Meer oder auf die Hügel.',
  'Сравните, что видно с каждого этажа и при каждой ориентации — море или холмы.',
  'قارنوا ما يطل عليه كل طابق وكل اتجاه، نحو البحر أو نحو التلال.',
  'Vergelijk waarop elke verdieping en oriëntatie uitkijkt, naar zee of naar de heuvels.',
  'Proszę porównać, na co wychodzi każde piętro i każda wystawa — na morze czy na wzgórza.',
  'Sammenlign hva hver etasje og retning ser ut mot, havet eller åsene.',
  'Jämför vad varje våning och väderstreck vetter mot, havet eller kullarna.')
a('Walk the pools, the gym and the social club.',
  'Recorra las piscinas, el gimnasio y el club social.', 'Parcourez les piscines, la salle de sport et le club social.',
  'Gehen Sie die Pools, den Fitnessraum und den Clubraum ab.', 'Пройдитесь по бассейнам, тренажёрному залу и клубу.',
  'تجولوا في المسابح وصالة الرياضة والنادي الاجتماعي.', 'Loop langs de zwembaden, de fitnessruimte en de clubruimte.',
  'Proszę obejrzeć baseny, siłownię i klub dla mieszkańców.', 'Gå gjennom bassengene, treningsrommet og fellesklubben.',
  'Gå runt bland poolerna, gymmet och klubblokalen.')
a('La Gaspara, <em>Estepona</em>', 'La Gaspara, <em>Estepona</em>', 'La Gaspara, <em>Estepona</em>',
  'La Gaspara, <em>Estepona</em>', 'Ла-Гаспара, <em>Эстепона</em>', 'لا غاسبارا، <em>إستيبونا</em>',
  'La Gaspara, <em>Estepona</em>', 'La Gaspara, <em>Estepona</em>', 'La Gaspara, <em>Estepona</em>',
  'La Gaspara, <em>Estepona</em>')
a('A gated scheme in La Gaspara on the western side of Estepona, beside the A-7, with the coast below.',
  'Un conjunto cerrado en La Gaspara, en la zona oeste de Estepona, junto a la A-7, con la costa a sus pies.',
  'Une résidence fermée à La Gaspara, à l’ouest d’Estepona, le long de l’A-7, avec la côte en contrebas.',
  'Eine geschlossene Anlage in La Gaspara im Westen von Estepona, direkt an der A-7, mit der Küste unterhalb.',
  'Закрытый комплекс в Ла-Гаспаре, в западной части Эстепоны, у трассы A-7, с побережьем внизу.',
  'مجمع مغلق في لا غاسبارا في الجهة الغربية من إستيبونا، بجوار الطريق A-7، والساحل في الأسفل.',
  'Een besloten complex in La Gaspara aan de westkant van Estepona, langs de A-7, met de kust beneden.',
  'Osiedle zamknięte w La Gaspara, w zachodniej części Estepony, przy A-7, z wybrzeżem poniżej.',
  'Et lukket anlegg i La Gaspara på vestsiden av Estepona, ved A-7, med kysten nedenfor.',
  'Ett slutet område i La Gaspara på Esteponas västra sida, vid A-7, med kusten nedanför.')
a('Approx. 8 minutes on foot', 'Aprox. 8 minutos a pie', 'Env. 8 minutes à pied', 'Ca. 8 Minuten zu Fuß',
  'Около 8 минут пешком', 'حوالي 8 دقائق سيراً', 'Ca. 8 minuten lopen', 'Ok. 8 minut pieszo',
  'Ca. 8 minutter til fots', 'Ca 8 minuter till fots')
a('Estepona golf', 'Golf de Estepona', 'Golf d’Estepona', 'Golf Estepona', 'Гольф Эстепоны', 'غولف إستيبونا',
  'Golf van Estepona', 'Pole golfowe Estepona', 'Estepona golf', 'Estepona golf')

# ---------------------------------------------------------------- faq
a('From €406,000 to €726,000 for the home alone, excluding IVA and purchase costs.',
  'De {E406000} a {E726000} solo la vivienda, sin IVA ni gastos de compra.',
  'De {E406000} à {E726000} pour le logement seul, hors TVA et frais d’acquisition.',
  'Von {E406000} bis {E726000} für die Wohnung allein, zuzüglich MwSt. und Erwerbsnebenkosten.',
  'От {E406000} до {E726000} только за квартиру, без НДС и расходов на оформление.',
  'من {E406000} إلى {E726000} للشقة وحدها، دون ضريبة القيمة المضافة ومصاريف التملك.',
  'Van {E406000} tot {E726000} voor de woning alleen, exclusief btw en aankoopkosten.',
  'Od {E406000} do {E726000} za samo mieszkanie, bez podatku VAT i kosztów nabycia.',
  'Fra {E406000} til {E726000} for boligen alene, eksklusive mva og kjøpsomkostninger.',
  'Från {E406000} till {E726000} för enbart bostaden, exklusive IVA (spansk moms) och köpkostnader.')
a('Fifteen apartments in the second phase of the scheme.',
  'Quince apartamentos en la segunda fase del conjunto.', 'Quinze appartements dans la deuxième phase de la résidence.',
  'Fünfzehn Wohnungen im zweiten Bauabschnitt der Anlage.', 'Пятнадцать квартир во второй очереди комплекса.',
  'خمس عشرة شقة في المرحلة الثانية من المجمع.', 'Vijftien appartementen in de tweede fase van het complex.',
  'Piętnaście apartamentów w drugim etapie osiedla.', 'Femten leiligheter i andre byggetrinn av anlegget.',
  'Femton lägenheter i andra etappen av området.')
a('From 107.45 to 144.67 sqm built, with 81.35 to 110.67 sqm of usable interior and terraces of 27.79 to 98.60 sqm.',
  'De {N107.45} a {N144.67} {U} construidos, con {N81.35} a {N110.67} {U} útiles interiores y terrazas de {N27.79} a {N98.60} {U}.',
  'De {N107.45} à {N144.67} {U} construits, avec {N81.35} à {N110.67} {U} de surface utile intérieure et des terrasses de {N27.79} à {N98.60} {U}.',
  'Von {N107.45} bis {N144.67} {U} bebaute Fläche, mit {N81.35} bis {N110.67} {U} Wohnfläche innen und Terrassen von {N27.79} bis {N98.60} {U}.',
  'От {N107.45} до {N144.67} {U} площади застройки, с полезной внутренней площадью от {N81.35} до {N110.67} {U} и террасами от {N27.79} до {N98.60} {U}.',
  'من {N107.45} إلى {N144.67} {U} مبنية، بمساحة داخلية صافية من {N81.35} إلى {N110.67} {U} وتراسات من {N27.79} إلى {N98.60} {U}.',
  'Van {N107.45} tot {N144.67} {U} bebouwd, met {N81.35} tot {N110.67} {U} nuttige binnenoppervlakte en terrassen van {N27.79} tot {N98.60} {U}.',
  'Od {N107.45} do {N144.67} {U} powierzchni zabudowy, z powierzchnią użytkową wewnątrz od {N81.35} do {N110.67} {U} i tarasami od {N27.79} do {N98.60} {U}.',
  'Fra {N107.45} til {N144.67} {U} bygget, med {N81.35} til {N110.67} {U} nyttbart innvendig areal og terrasser på {N27.79} til {N98.60} {U}.',
  'Från {N107.45} till {N144.67} {U} byggyta, med {N81.35} till {N110.67} {U} invändig nyttoyta och terrasser på {N27.79} till {N98.60} {U}.')
a("Each home is listed with one parking space and one storeroom, sold as separate lines. With them the list's subtotal is €24,000 above the price of the home, from €430,000 to €750,000 before IVA.",
  'Cada vivienda figura con una plaza de garaje y un trastero, que se venden como líneas aparte. Con ellos, el subtotal del listado supera en {E24000} el precio de la vivienda, de {E430000} a {E750000} antes de IVA.',
  'Chaque logement est listé avec une place de parking et un débarras, vendus sur des lignes distinctes. Avec eux, le sous-total de la liste dépasse de {E24000} le prix du logement, de {E430000} à {E750000} hors TVA.',
  'Jede Wohnung ist mit einem Stellplatz und einem Abstellraum gelistet, die als eigene Positionen verkauft werden. Mit beiden liegt die Zwischensumme der Liste {E24000} über dem Preis der Wohnung, bei {E430000} bis {E750000} zuzüglich MwSt.',
  'Каждая квартира значится с парковочным местом и кладовой, которые продаются отдельными позициями. С ними промежуточный итог в списке на {E24000} выше цены квартиры — от {E430000} до {E750000} без НДС.',
  'تُدرج كل شقة مع موقف سيارة ومخزن يُباعان بندين منفصلين. ومعهما يزيد المجموع الفرعي في القائمة بمقدار {E24000} على سعر الشقة، من {E430000} إلى {E750000} قبل ضريبة القيمة المضافة.',
  'Elke woning staat op de lijst met een parkeerplaats en een berging, die als aparte posten worden verkocht. Daarmee ligt het subtotaal {E24000} boven de prijs van de woning, van {E430000} tot {E750000} exclusief btw.',
  'Każde mieszkanie figuruje z miejscem postojowym i komórką lokatorską, sprzedawanymi jako osobne pozycje. Wraz z nimi suma częściowa na liście jest o {E24000} wyższa od ceny mieszkania, od {E430000} do {E750000} bez podatku VAT.',
  'Hver bolig står oppført med en parkeringsplass og en bod, som selges som egne linjer. Med dem er listens delsum {E24000} over prisen på boligen, fra {E430000} til {E750000} før mva.',
  'Varje bostad listas med en parkeringsplats och ett förråd, som säljs som egna rader. Med dem är listans delsumma {E24000} över bostadens pris, från {E430000} till {E750000} före IVA (spansk moms).')
a("Twelve face south-west and three face south, according to the developer's list.",
  'Doce están orientadas al suroeste y tres al sur, según el listado del promotor.',
  'Douze sont orientés au sud-ouest et trois au sud, selon la liste du promoteur.',
  'Laut der Liste des Bauträgers zwölf nach Südwesten und drei nach Süden.',
  'По списку застройщика двенадцать ориентированы на юго-запад и три на юг.',
  'اثنتا عشرة تتجه نحو الجنوب الغربي وثلاث نحو الجنوب، وفق قائمة المطوّر.',
  'Volgens de lijst van de ontwikkelaar twaalf op het zuidwesten en drie op het zuiden.',
  'Według listy dewelopera dwanaście ma wystawę południowo-zachodnią, a trzy południową.',
  'Ifølge utbyggerens liste vender tolv mot sørvest og tre mot sør.',
  'Enligt exploatörens lista vetter tolv mot sydväst och tre mot söder.')
a('How are the homes heated and cooled?',
  '¿Cómo se calientan y refrescan las viviendas?', 'Comment les logements sont-ils chauffés et rafraîchis ?',
  'Wie werden die Wohnungen beheizt und gekühlt?', 'Как отапливаются и охлаждаются квартиры?',
  'كيف تُدفّأ الشقق وتُبرّد؟', 'Hoe worden de woningen verwarmd en gekoeld?',
  'Jak mieszkania są ogrzewane i chłodzone?', 'Hvordan varmes og kjøles boligene?',
  'Hur värms och kyls bostäderna?')
a('The documents we hold give no date for this phase. We ask for it in writing before any reservation.',
  'La documentación de que disponemos no indica fecha para esta fase. La solicitamos por escrito antes de cualquier reserva.',
  'Les documents dont nous disposons ne donnent aucune date pour cette phase. Nous la demandons par écrit avant toute réservation.',
  'Die uns vorliegenden Unterlagen nennen für diesen Abschnitt keinen Termin. Wir fordern ihn vor jeder Reservierung schriftlich an.',
  'В имеющихся у нас документах срока для этой очереди нет. Мы запрашиваем его письменно до любого бронирования.',
  'لا تذكر المستندات المتوفرة لدينا موعدًا لهذه المرحلة، ونطلبه كتابةً قبل أي حجز.',
  'De documenten die wij hebben noemen geen datum voor deze fase. Wij vragen die schriftelijk op vóór elke reservering.',
  'Posiadane przez nas dokumenty nie podają terminu dla tego etapu. Występujemy o niego na piśmie przed każdą rezerwacją.',
  'Dokumentene vi har oppgir ingen dato for dette byggetrinnet. Vi ber om den skriftlig før enhver reservasjon.',
  'Handlingarna vi har anger inget datum för denna etapp. Vi begär det skriftligt före varje bokning.')

# ---------------------------------------------------------------- next steps, enquiry, seo
a('The price list, the drawings we hold for the available homes and the payment terms.',
  'La lista de precios, los planos de que disponemos de las viviendas disponibles y las condiciones de pago.',
  'La liste de prix, les plans dont nous disposons pour les logements disponibles et les conditions de paiement.',
  'Die Preisliste, die uns vorliegenden Pläne der verfügbaren Wohnungen und die Zahlungsbedingungen.',
  'Прайс-лист, имеющиеся у нас планы доступных квартир и условия оплаты.',
  'قائمة الأسعار، والمخططات المتوفرة لدينا للشقق المتاحة، وشروط الدفع.',
  'De prijslijst, de tekeningen die wij van de beschikbare woningen hebben en de betalingsvoorwaarden.',
  'Cennik, posiadane przez nas rzuty dostępnych mieszkań i warunki płatności.',
  'Prislisten, tegningene vi har av de ledige boligene og betalingsvilkårene.',
  'Prislistan, de ritningar vi har över de lediga bostäderna och betalningsvillkoren.')
a('We arrange the visit and walk the scheme and the communal areas with you.',
  'Organizamos la visita y recorremos con usted el conjunto y las zonas comunes.',
  'Nous organisons la visite et parcourons avec vous la résidence et les espaces communs.',
  'Wir organisieren den Besuch und gehen mit Ihnen durch die Anlage und die Gemeinschaftsbereiche.',
  'Мы организуем визит и вместе с вами осмотрим комплекс и общие зоны.',
  'نرتب الزيارة ونتجول معكم في المجمع والمرافق المشتركة.',
  'Wij regelen het bezoek en lopen met u door het complex en de gemeenschappelijke ruimtes.',
  'Organizujemy wizytę i oprowadzamy Państwa po osiedlu i częściach wspólnych.',
  'Vi ordner besøket og går gjennom anlegget og fellesområdene sammen med dere.',
  'Vi ordnar besöket och går runt i området och de gemensamma ytorna tillsammans med er.')
a('I would like to receive the latest project information for La Gaspara Residences.',
  'Me gustaría recibir la información más reciente del proyecto La Gaspara Residences.',
  'Je souhaite recevoir les dernières informations sur le projet La Gaspara Residences.',
  'Ich möchte die aktuellen Projektinformationen zu La Gaspara Residences erhalten.',
  'Я хотел бы получить актуальную информацию о проекте La Gaspara Residences.',
  'أرغب في تلقي أحدث معلومات مشروع La Gaspara Residences.',
  'Ik ontvang graag de meest recente projectinformatie over La Gaspara Residences.',
  'Chciałbym otrzymać najnowsze informacje o projekcie La Gaspara Residences.',
  'Jeg ønsker å motta den nyeste prosjektinformasjonen om La Gaspara Residences.',
  'Jag vill gärna få den senaste projektinformationen om La Gaspara Residences.')
a('Project context: La Gaspara Residences.',
  'Contexto del proyecto: La Gaspara Residences.', 'Contexte du projet : La Gaspara Residences.',
  'Projektkontext: La Gaspara Residences.', 'Контекст проекта: La Gaspara Residences.',
  'سياق المشروع: La Gaspara Residences.', 'Projectcontext: La Gaspara Residences.',
  'Kontekst projektu: La Gaspara Residences.', 'Prosjektkontekst: La Gaspara Residences.',
  'Projektkontext: La Gaspara Residences.')
a('La Gaspara Residences - Estepona', 'La Gaspara Residences - Estepona', 'La Gaspara Residences - Estepona',
  'La Gaspara Residences - Estepona', 'La Gaspara Residences - Эстепона', 'La Gaspara Residences - إستيبونا',
  'La Gaspara Residences - Estepona', 'La Gaspara Residences - Estepona', 'La Gaspara Residences - Estepona',
  'La Gaspara Residences - Estepona')
a('La Gaspara Residences: Fifteen Homes, Estepona',
  'La Gaspara Residences: quince viviendas, Estepona', 'La Gaspara Residences : quinze logements, Estepona',
  'La Gaspara Residences: fünfzehn Wohnungen, Estepona', 'La Gaspara Residences: пятнадцать квартир, Эстепона',
  'La Gaspara Residences: خمس عشرة شقة، إستيبونا', 'La Gaspara Residences: vijftien woningen, Estepona',
  'La Gaspara Residences: piętnaście mieszkań, Estepona', 'La Gaspara Residences: femten boliger, Estepona',
  'La Gaspara Residences: femton bostäder, Estepona')
a('Fifteen Homes, Estepona', 'Quince viviendas, Estepona', 'Quinze logements, Estepona', 'Fünfzehn Wohnungen, Estepona',
  'Пятнадцать квартир, Эстепона', 'خمس عشرة شقة، إستيبونا', 'Vijftien woningen, Estepona',
  'Piętnaście mieszkań, Estepona', 'Femten boliger, Estepona', 'Femton bostäder, Estepona')

# ---------------------------------------------------------------- shared strings, Norwegian made neutral
# The memory's Norwegian for these four addresses the reader as "du"; the house register is neutral
# (De/dere or no pronoun). The other eight locales keep the memory's wording.
TM = json.load(open(f'{SP}/tm.json'))


def fix(en, **loc):
    T[en] = {l: TM[en][l] for l in LOCS}
    T[en].update(loc)


fix('What Nueva Living verifies before you commit.', no='Hva Nueva Living kontrollerer før en avtale inngås.')
fix('The developer has not published them for this release. We confirm them in writing before you commit.',
    no='Utbyggeren har ikke publisert dem for dette salgstrinnet. Vi bekrefter dem skriftlig før noen avtale inngås.')
fix('Share your details and we will send you the current project information.',
    no='Legg igjen kontaktopplysningene, så sender vi dere den gjeldende prosjektinformasjonen.')
fix('Thank you. We have received your enquiry and will be in touch.',
    no='Takk. Vi har mottatt henvendelsen og tar kontakt.')

json.dump(T, open(f'{SP}/tr_g.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries to', f'{SP}/tr_g.json')
