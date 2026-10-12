# -*- coding: utf-8 -*-
"""Altamira Hills Residences: the strings the translation memory did not have.

Same shape as k_selwo.py. Numbers are written in English form (82.40, 1,004.00) and converted per
locale by conv(); money is {E458000}; {U} is the area unit, {KM} the kilometre. Floor labels are
left to assemble.py (floor_label), the unit size cells and the floorplan alt/captions are templates.
    python3 tools/import/k_altamira.py <scratch dir>      (writes <scratch dir>/tr_a.json)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
DEC = {l: ('.' if l == 'ar' else ',') for l in LOCS}
UNIT = {'es': 'm²', 'fr': 'm²', 'de': 'm²', 'ru': 'м²', 'ar': 'م²', 'nl': 'm²', 'pl': 'm²', 'no': 'm²', 'sv': 'm²'}
KM = {'ru': 'км', 'ar': 'كم'}
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def conv(text, l):
    def one(m):
        s = m.group(0)
        whole, _, frac = s.partition('.')
        whole = whole.replace(',', GROUP[l])
        return whole + (DEC[l] + frac if frac else '')
    return re.sub(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+', one, text)


def expand(text, l):
    text = conv(text, l)
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    return text.replace('{U}', UNIT[l]).replace('{KM}', KM.get(l, 'km'))


def a(hint, *tr):
    hits = [hint] if hint in todo else [t for t in todo if t.startswith(hint)]
    assert len(hits) <= 1, (hint, len(hits))
    assert len(tr) == 9, (hint, len(tr))
    if not hits:
        print('already in the translation memory:', hint[:50])
        return
    T[hits[0]] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---------------------------------------------------------------- templates
HOME = {'es': 'vivienda', 'fr': 'logement', 'de': 'Wohnung', 'ru': 'квартиры', 'ar': 'المسكن', 'nl': 'woning', 'pl': 'lokalu', 'no': 'bolig', 'sv': 'bostad'}
PLANALT = {'es': 'Plano de la vivienda {r}', 'fr': 'Plan du logement {r}', 'de': 'Grundriss der Wohnung {r}', 'ru': 'Планировка квартиры {r}',
           'ar': 'مخطط المسكن {r}', 'nl': 'Plattegrond van woning {r}', 'pl': 'Rzut lokalu {r}', 'no': 'Plantegning av bolig {r}', 'sv': 'Planritning för bostad {r}'}
HOMECAP = {'es': 'Vivienda {r}', 'fr': 'Logement {r}', 'de': 'Wohnung {r}', 'ru': 'Квартира {r}', 'ar': 'المسكن {r}', 'nl': 'Woning {r}',
           'pl': 'Lokal {r}', 'no': 'Bolig {r}', 'sv': 'Bostad {r}'}
# One unit size cell: built / interior / terrace / garden, in the words sotavento-residences already uses.
SIZE = {
    'es': ('{} m² construidos', '{} m² interiores', '{} m² de terraza', '{} m² de jardín'),
    'fr': ('{} m² construits', '{} m² intérieurs', '{} m² de terrasse', '{} m² de jardin'),
    'de': ('{} m² bebaut', '{} m² Innenfläche', '{} m² Terrasse', '{} m² Garten'),
    'ru': ('{} м² застроенной площади', '{} м² внутри', 'терраса {} м²', 'сад {} м²'),
    'ar': ('{} م² مبنية', '{} م² داخلية', '{} م² تراس', '{} م² حديقة'),
    'nl': ('{} m² bebouwd', '{} m² binnen', '{} m² terras', '{} m² tuin'),
    'pl': ('{} m² zabudowy', '{} m² wnętrza', '{} m² tarasu', '{} m² ogrodu'),
    'no': ('{} m² bygd', '{} m² innvendig', '{} m² terrasse', '{} m² hage'),
    'sv': ('{} m² byggyta', '{} m² inomhus', '{} m² terrass', '{} m² trädgård'),
}
SEP = {l: ('، ' if l == 'ar' else ', ') for l in LOCS}

for en in todo:
    m = re.fullmatch(r'Floorplan of home (\w+)', en)
    c = re.fullmatch(r'Home (\w+)', en)
    s = re.fullmatch(r'([\d.]+) sqm built(?:, ([\d.]+) sqm interior)?, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm garden)?', en)
    if m:
        T[en] = {l: PLANALT[l].format(r=m.group(1)) for l in LOCS}
    elif c:
        T[en] = {l: HOMECAP[l].format(r=c.group(1)) for l in LOCS}
    elif s:
        T[en] = {l: SEP[l].join(conv(SIZE[l][i].format(s.group(k)), l) for i, k in enumerate((1, 2, 3, 4)) if s.group(k)) for l in LOCS}

# ---------------------------------------------------------------- names, card, hero
for en in ('Altamira Hills Residences', 'Altamira Hills'):
    T[en] = {l: en for l in LOCS}
T['Altamira Hills <em>Residences</em>'] = {l: 'Altamira Hills <em>Residences</em>' for l in LOCS}
a('18 two- and three-bedroom apartments and penthouses are listed in a resort-style',
  "Hay 18 apartamentos y áticos de dos y tres dormitorios a la venta en una promoción de estilo resort en la parte alta de Los Monteros, en Marbella, con terrazas orientadas al mar, piscinas interior y exterior, spa, gimnasio y zona de coworking. Desde {E458000}.",
  "18 appartements et penthouses de deux et trois chambres sont proposés dans une résidence de style resort dans la partie haute de Los Monteros, à Marbella, avec des terrasses face à la mer, des piscines intérieure et extérieure, un spa, une salle de sport et un espace de coworking. À partir de {E458000}.",
  "18 Wohnungen und Penthouses mit zwei und drei Schlafzimmern werden in einer Anlage im Resort-Stil im oberen Teil von Los Monteros in Marbella angeboten, mit Terrassen zum Meer, Innen- und Außenpool, Spa, Fitnessraum und Coworking-Bereich. Ab {E458000}.",
  "В продаже 18 квартир и пентхаусов с двумя и тремя спальнями в комплексе в стиле курорта в верхней части Лос-Монтероса, Марбелья: террасы с видом на море, внутренний и наружный бассейны, спа, тренажёрный зал и коворкинг. От {E458000}.",
  "18 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم معروضة في مجمّع على طراز المنتجعات في الجزء العلوي من لوس مونتيروس في مربيّا، بتراسات مطلّة على البحر ومسبحين داخلي وخارجي وسبا وصالة رياضية ومساحة للعمل المشترك. ابتداءً من {E458000}.",
  "18 appartementen en penthouses met twee en drie slaapkamers worden aangeboden in een resortachtig complex in het hoger gelegen deel van Los Monteros in Marbella, met terrassen op de zee, een binnen- en buitenzwembad, spa, gym en coworkingruimte. Vanaf {E458000}.",
  "18 apartamentów i penthouse’ów z dwiema i trzema sypialniami jest dostępnych w osiedlu w stylu kurortu w górnej części Los Monteros w Marbelli, z tarasami zwróconymi ku morzu, basenem zewnętrznym i wewnętrznym, spa, siłownią i strefą coworkingu. Od {E458000}.",
  "18 leiligheter og toppleiligheter med to og tre soverom er til salgs i et anlegg i feriestedsstil i den øvre delen av Los Monteros i Marbella, med terrasser mot havet, innendørs og utendørs basseng, spa, treningsrom og coworking-område. Fra {E458000}.",
  "18 lägenheter och takvåningar med två och tre sovrum är till salu i ett resortliknande område i övre delen av Los Monteros i Marbella, med terrasser mot havet, inomhus- och utomhuspool, spa, gym och coworkingyta. Från {E458000}.")
a('18 two- and three-bedroom apartments and penthouses at Altos de los Monteros, Marbella, with large',
  "18 apartamentos y áticos de dos y tres dormitorios en Altos de los Monteros, Marbella, con grandes terrazas, vistas al mar, piscinas interior y exterior, spa y gimnasio, desde {E458000}.",
  "18 appartements et penthouses de deux et trois chambres à Altos de los Monteros, Marbella, avec de grandes terrasses, vue sur la mer, piscines intérieure et extérieure, spa et salle de sport, à partir de {E458000}.",
  "18 Wohnungen und Penthouses mit zwei und drei Schlafzimmern in Altos de los Monteros, Marbella, mit großen Terrassen, Meerblick, Innen- und Außenpool, Spa und Fitnessraum, ab {E458000}.",
  "18 квартир и пентхаусов с двумя и тремя спальнями в Альтос-де-лос-Монтерос, Марбелья: большие террасы, вид на море, внутренний и наружный бассейны, спа и тренажёрный зал, от {E458000}.",
  "18 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم في ألتوس دي لوس مونتيروس بمربيّا، بتراسات واسعة وإطلالات على البحر ومسبحين داخلي وخارجي وسبا وصالة رياضية، ابتداءً من {E458000}.",
  "18 appartementen en penthouses met twee en drie slaapkamers in Altos de los Monteros, Marbella, met grote terrassen, zeezicht, een binnen- en buitenzwembad, spa en gym, vanaf {E458000}.",
  "18 apartamentów i penthouse’ów z dwiema i trzema sypialniami w Altos de los Monteros, Marbella, z dużymi tarasami, widokiem na morze, basenem zewnętrznym i wewnętrznym, spa i siłownią, od {E458000}.",
  "18 leiligheter og toppleiligheter med to og tre soverom i Altos de los Monteros, Marbella, med store terrasser, utsikt mot havet, innendørs og utendørs basseng, spa og treningsrom, fra {E458000}.",
  "18 lägenheter och takvåningar med två och tre sovrum i Altos de los Monteros, Marbella, med stora terrasser, havsutsikt, inomhus- och utomhuspool, spa och gym, från {E458000}.")
a('Two- and three-bedroom apartments and penthouses with sea views at Altos',
  "Apartamentos y áticos de dos y tres dormitorios con vistas al mar en Altos de los Monteros, Marbella, desde {E458000}.",
  "Appartements et penthouses de deux et trois chambres avec vue sur la mer à Altos de los Monteros, Marbella, à partir de {E458000}.",
  "Wohnungen und Penthouses mit zwei und drei Schlafzimmern und Meerblick in Altos de los Monteros, Marbella, ab {E458000}.",
  "Квартиры и пентхаусы с двумя и тремя спальнями и видом на море в Альтос-де-лос-Монтерос, Марбелья, от {E458000}.",
  "شقق وبنتهاوس بغرفتي نوم وثلاث غرف نوم وإطلالات على البحر في ألتوس دي لوس مونتيروس بمربيّا، ابتداءً من {E458000}.",
  "Appartementen en penthouses met twee en drie slaapkamers en zeezicht in Altos de los Monteros, Marbella, vanaf {E458000}.",
  "Apartamenty i penthouse’y z dwiema i trzema sypialniami oraz widokiem na morze w Altos de los Monteros, Marbella, od {E458000}.",
  "Leiligheter og toppleiligheter med to og tre soverom og utsikt mot havet i Altos de los Monteros, Marbella, fra {E458000}.",
  "Lägenheter och takvåningar med två och tre sovrum och havsutsikt i Altos de los Monteros, Marbella, från {E458000}.")
a('18 homes listed', "18 viviendas a la venta", "18 logements proposés", "18 Wohnungen angeboten", "В продаже 18 квартир", "18 مسكنًا معروضًا", "18 woningen aangeboden", "18 lokali w ofercie", "18 boliger til salgs", "18 bostäder till salu")
a('18 two- and three-bedroom apartments and penthouses with large terraces and sea views',
  "18 apartamentos y áticos de dos y tres dormitorios con grandes terrazas y vistas al mar en la parte alta de Los Monteros, con piscinas interior y exterior, spa y gimnasio.",
  "18 appartements et penthouses de deux et trois chambres avec de grandes terrasses et vue sur la mer dans la partie haute de Los Monteros, avec piscines intérieure et extérieure, spa et salle de sport.",
  "18 Wohnungen und Penthouses mit zwei und drei Schlafzimmern, großen Terrassen und Meerblick im oberen Teil von Los Monteros, mit Innen- und Außenpool, Spa und Fitnessraum.",
  "18 квартир и пентхаусов с двумя и тремя спальнями, большими террасами и видом на море в верхней части Лос-Монтероса, с внутренним и наружным бассейнами, спа и тренажёрным залом.",
  "18 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم وتراسات واسعة وإطلالات على البحر في الجزء العلوي من لوس مونتيروس، مع مسبحين داخلي وخارجي وسبا وصالة رياضية.",
  "18 appartementen en penthouses met twee en drie slaapkamers, grote terrassen en zeezicht in het hoger gelegen deel van Los Monteros, met een binnen- en buitenzwembad, spa en gym.",
  "18 apartamentów i penthouse’ów z dwiema i trzema sypialniami, dużymi tarasami i widokiem na morze w górnej części Los Monteros, z basenem zewnętrznym i wewnętrznym, spa i siłownią.",
  "18 leiligheter og toppleiligheter med to og tre soverom, store terrasser og utsikt mot havet i den øvre delen av Los Monteros, med innendørs og utendørs basseng, spa og treningsrom.",
  "18 lägenheter och takvåningar med två och tre sovrum, stora terrasser och havsutsikt i övre delen av Los Monteros, med inomhus- och utomhuspool, spa och gym.")

# ---------------------------------------------------------------- images and media
CG = {'es': 'Imagen generada por ordenador de ', 'fr': 'Image de synthèse de ', 'de': 'Computergenerierte Ansicht von ',
      'ru': 'Компьютерное изображение: ', 'ar': 'صورة مولّدة بالحاسوب لـ', 'nl': 'Computergegenereerd beeld van ',
      'pl': 'Wygenerowany komputerowo widok: ', 'no': 'Datagenerert bilde av ', 'sv': 'Datorgenererad bild av '}


def cg(hint, *tr):
    assert len(tr) == 9
    en = [t for t in todo if t.startswith(hint)]
    assert len(en) == 1, (hint, len(en))
    T[en[0]] = {l: expand(CG[l] + t, l) for l, t in zip(LOCS, tr)}


cg('Computer-generated view of a white stepped apartment building',
   "un edificio de apartamentos blanco y escalonado con largas terrazas, visto a través de jardines cuidados",
   "un immeuble blanc en gradins aux longues terrasses, vu à travers des jardins paysagers",
   "einem weißen, abgestuften Wohngebäude mit langen Terrassen, gesehen über bepflanzte Gärten",
   "белое ступенчатое здание с длинными террасами, вид через ухоженные сады",
   "مبنى سكني أبيض متدرّج بتراسات طويلة، يُرى عبر حدائق مزروعة",
   "een wit, getrapt appartementengebouw met lange terrassen, gezien over aangelegde tuinen",
   "biały schodkowy budynek mieszkalny z długimi tarasami, widziany przez obsadzone ogrody",
   "en hvit, trappetrinnsformet leilighetsbygning med lange terrasser, sett over beplantede hager",
   "en vit, trappstegsformad flerbostadsbyggnad med långa terrasser, sedd över planterade trädgårdar")
cg('Computer-generated aerial view of white apartment blocks stepping down',
   "una vista aérea de bloques de apartamentos blancos que descienden por una ladera, con grandes terrazas en cada planta y el mar al fondo",
   "une vue aérienne de blocs d’appartements blancs en gradins sur une colline, avec de grandes terrasses à chaque étage et la mer derrière",
   "einer Luftaufnahme weißer Wohnblöcke, die an einem Hang abgestuft sind, mit großen Terrassen auf jeder Etage und dem Meer dahinter",
   "белые жилые блоки, ступенями спускающиеся по склону, с большими террасами на каждом этаже и морем позади, вид с воздуха",
   "منظر جوي لمبانٍ سكنية بيضاء تتدرّج على منحدر، بتراسات واسعة في كل طابق والبحر خلفها",
   "een luchtbeeld van witte appartementenblokken die langs een helling afdalen, met grote terrassen op elke verdieping en de zee erachter",
   "widok z lotu ptaka na białe bloki mieszkalne schodzące po zboczu, z dużymi tarasami na każdym piętrze i morzem w tle",
   "et flyfoto av hvite leilighetsbygg som trapper seg nedover en skråning, med store terrasser i hver etasje og havet bak",
   "en flygvy av vita flerbostadshus som trappar ner sig längs en sluttning, med stora terrasser på varje våning och havet bakom")
cg('Computer-generated view of a curved pool with a timber deck',
   "una piscina curva con terraza de madera y un edificio blanco, con el mar en el horizonte",
   "une piscine arrondie avec une terrasse en bois et un bâtiment blanc, la mer à l’horizon",
   "einem geschwungenen Pool mit Holzdeck und einem weißen Gebäude, mit dem Meer am Horizont",
   "бассейн изогнутой формы с деревянным настилом и белое здание, на горизонте море",
   "مسبح منحنٍ بسطح خشبي ومبنى أبيض، والبحر عند الأفق",
   "een gebogen zwembad met een houten terras en een wit gebouw, met de zee aan de horizon",
   "zakrzywiony basen z drewnianym tarasem i biały budynek, z morzem na horyzoncie",
   "et buet basseng med tredekk og en hvit bygning, med havet i horisonten",
   "en böjd pool med trädäck och en vit byggnad, med havet vid horisonten")
cg('Computer-generated living and dining room with a long sofa',
   "un salón comedor con un sofá largo, una mesa de comedor, una chimenea y puertas de cristal con vistas al mar",
   "un séjour-salle à manger avec un long canapé, une table à manger, une cheminée et des portes vitrées sur la mer",
   "einem Wohn- und Essbereich mit langem Sofa, Esstisch, Kamin und Glastüren mit Meerblick",
   "гостиная со столовой: длинный диван, обеденный стол, камин и стеклянные двери с видом на море",
   "غرفة معيشة وطعام بأريكة طويلة وطاولة طعام ومدفأة وأبواب زجاجية تطلّ على البحر",
   "een woon- en eetkamer met een lange bank, een eettafel, een open haard en glazen deuren met zeezicht",
   "salon z jadalnią z długą sofą, stołem jadalnianym, kominkiem i przeszklonymi drzwiami z widokiem na morze",
   "en stue og spisestue med en lang sofa, et spisebord, en peis og glassdører med utsikt mot havet",
   "ett vardagsrum och en matplats med en lång soffa, ett matbord, en öppen spis och glasdörrar med havsutsikt")
a('Computer-generated views of the buildings, the facilities and the interiors',
  "Imágenes generadas por ordenador de los edificios, las instalaciones y los interiores, dos fotografías de la ladera y los planos de 17 de las 18 viviendas a la venta.",
  "Images de synthèse des bâtiments, des équipements et des intérieurs, deux photographies de la colline et les plans de 17 des 18 logements proposés.",
  "Computergenerierte Ansichten der Gebäude, der Einrichtungen und der Innenräume, zwei Fotos des Hangs und die Grundrisse von 17 der 18 angebotenen Wohnungen.",
  "Компьютерные изображения зданий, общих зон и интерьеров, две фотографии склона и планировки 17 из 18 квартир в продаже.",
  "صور مولّدة بالحاسوب للمباني والمرافق والمساحات الداخلية، وصورتان فوتوغرافيتان للمنحدر، ومخططات 17 مسكنًا من أصل 18 مسكنًا معروضًا.",
  "Computergegenereerde beelden van de gebouwen, de voorzieningen en de interieurs, twee foto’s van de helling en de plattegronden van 17 van de 18 aangeboden woningen.",
  "Wygenerowane komputerowo widoki budynków, części wspólnych i wnętrz, dwa zdjęcia zbocza oraz rzuty 17 z 18 oferowanych lokali.",
  "Datagenererte bilder av byggene, fellesfasilitetene og interiørene, to fotografier av åssiden og plantegningene til 17 av de 18 boligene som er til salgs.",
  "Datorgenererade bilder av byggnaderna, de gemensamma anläggningarna och interiörerna, två fotografier av sluttningen och planritningarna för 17 av de 18 bostäderna som är till salu.")
a('Apart from the two photographs of the hillside',
  "Salvo las dos fotografías de la ladera, todas las imágenes están generadas por ordenador, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los del promotor y las superficies que figuran en ellos son aproximadas y están sujetas al proyecto definitivo. Los nombres de las estancias en los planos están en español.",
  "À l’exception des deux photographies de la colline, toutes les images sont des images de synthèse, et le mobilier et la décoration qui y figurent sont indicatifs et non inclus. Les plans sont ceux du promoteur et les surfaces qui y figurent sont approximatives et soumises au projet définitif. Les noms des pièces sur les plans sont en espagnol.",
  "Mit Ausnahme der zwei Fotos des Hangs sind alle Bilder computergeneriert, und die darin gezeigten Möbel und die Dekoration sind illustrativ und nicht enthalten. Die Grundrisse stammen vom Bauträger, und die darauf angegebenen Flächen sind ungefähr und vorbehaltlich des endgültigen Projekts. Die Raumbezeichnungen in den Grundrissen sind spanisch.",
  "Кроме двух фотографий склона, все изображения созданы на компьютере, а мебель и отделка на них носят иллюстративный характер и не входят в стоимость. Планировки принадлежат застройщику, указанные на них площади приблизительны и зависят от окончательного проекта. Названия помещений на планировках даны на испанском языке.",
  "باستثناء الصورتين الفوتوغرافيتين للمنحدر، فإن جميع الصور مولّدة بالحاسوب، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. المخططات من المطوّر، والمساحات المبيّنة عليها تقريبية وتخضع للمشروع النهائي. أسماء الغرف في المخططات بالإسبانية.",
  "Op de twee foto’s van de helling na zijn alle beelden computergegenereerd, en het meubilair en de decoratie erop zijn illustratief en niet inbegrepen. De plattegronden zijn die van de ontwikkelaar en de oppervlaktes erop zijn bij benadering en onder voorbehoud van het definitieve project. De ruimtenamen op de plattegronden zijn in het Spaans.",
  "Poza dwoma zdjęciami zbocza wszystkie obrazy są wygenerowane komputerowo, a widoczne na nich meble i dekoracje mają charakter poglądowy i nie są wliczone. Rzuty pochodzą od dewelopera, a podane na nich powierzchnie są przybliżone i podlegają ostatecznemu projektowi. Nazwy pomieszczeń na rzutach są po hiszpańsku.",
  "Bortsett fra de to fotografiene av åssiden er alle bildene datagenererte, og møblene og dekorasjonen på dem er illustrasjoner og følger ikke med. Plantegningene er utbyggerens, og arealene på dem er omtrentlige og med forbehold om det endelige prosjektet. Romnavnene på plantegningene er på spansk.",
  "Förutom de två fotografierna av sluttningen är alla bilder datorgenererade, och möblerna och inredningen på dem är illustrativa och ingår inte. Planritningarna är exploatörens, och ytorna på dem är ungefärliga och med förbehåll för det slutliga projektet. Rumsnamnen på planritningarna är på spanska.")
a('The building from the gardens', "El edificio visto desde los jardines", "Le bâtiment vu des jardins", "Das Gebäude von den Gärten aus", "Здание со стороны садов", "المبنى من جهة الحدائق", "Het gebouw vanuit de tuinen", "Budynek od strony ogrodów", "Bygningen sett fra hagene", "Byggnaden sedd från trädgårdarna")
a('The terraced blocks from above', "Los bloques con terrazas, desde el aire", "Les blocs à terrasses vus du ciel", "Die Terrassenblöcke von oben", "Террасные блоки сверху", "المباني ذات التراسات من الأعلى", "De terrasblokken van bovenaf", "Tarasowe bloki z lotu ptaka", "De terrassede byggene ovenfra", "De terrasserade husen uppifrån")
cg('Computer-generated aerial view of two stepped apartment buildings',
   "una vista aérea de dos edificios de apartamentos escalonados en una ladera arbolada sobre el mar",
   "une vue aérienne de deux immeubles en gradins sur une colline boisée au-dessus de la mer",
   "einer Luftaufnahme zweier abgestufter Wohngebäude an einem bewaldeten Hang über dem Meer",
   "два ступенчатых жилых здания на лесистом склоне над морем, вид с воздуха",
   "منظر جوي لمبنيين سكنيين متدرّجين على منحدر مشجّر فوق البحر",
   "een luchtbeeld van twee getrapte appartementengebouwen op een beboste helling boven de zee",
   "widok z lotu ptaka na dwa schodkowe budynki mieszkalne na zalesionym zboczu nad morzem",
   "et flyfoto av to trappetrinnsformede leilighetsbygg på en skogkledd åsside over havet",
   "en flygvy av två trappstegsformade flerbostadshus på en skogklädd sluttning ovanför havet")
a('The two buildings in daylight', "Los dos edificios a la luz del día", "Les deux bâtiments en plein jour", "Die beiden Gebäude bei Tageslicht", "Два здания при дневном свете", "المبنيان في ضوء النهار", "De twee gebouwen overdag", "Dwa budynki w świetle dziennym", "De to byggene i dagslys", "De två byggnaderna i dagsljus")
cg('Computer-generated aerial view at dusk of the stepped buildings',
   "una vista aérea al atardecer de los edificios escalonados, con terrazas iluminadas, una piscina y colinas boscosas detrás",
   "une vue aérienne au crépuscule des immeubles en gradins, avec des terrasses éclairées, une piscine et des collines boisées derrière",
   "einer Luftaufnahme der abgestuften Gebäude in der Dämmerung, mit beleuchteten Terrassen, einem Pool und bewaldeten Hügeln dahinter",
   "ступенчатые здания в сумерках с освещёнными террасами, бассейном и лесистыми холмами позади, вид с воздуха",
   "منظر جوي عند الغروب للمباني المتدرّجة بتراساتها المضاءة ومسبحها والتلال المشجّرة خلفها",
   "een luchtbeeld in de schemering van de getrapte gebouwen, met verlichte terrassen, een zwembad en beboste heuvels erachter",
   "widok z lotu ptaka o zmierzchu na schodkowe budynki z oświetlonymi tarasami, basenem i zalesionymi wzgórzami w tle",
   "et flyfoto i skumringen av de trappetrinnsformede byggene, med opplyste terrasser, et basseng og skogkledde åser bak",
   "en flygvy i skymningen av de trappstegsformade byggnaderna, med upplysta terrasser, en pool och skogklädda kullar bakom")
a('The buildings at dusk', "Los edificios al atardecer", "Les bâtiments au crépuscule", "Die Gebäude in der Dämmerung", "Здания в сумерках", "المباني عند الغروب", "De gebouwen in de schemering", "Budynki o zmierzchu", "Byggene i skumringen", "Byggnaderna i skymningen")
cg('Computer-generated view at dusk of a curved outdoor pool',
   "una piscina exterior curva al atardecer, con borde en cascada, tumbonas y un gimnasio iluminado junto a ella",
   "une piscine extérieure arrondie au crépuscule, avec un bord en cascade, des transats et une salle de sport éclairée à côté",
   "einem geschwungenen Außenpool in der Dämmerung, mit Wasserfallkante, Sonnenliegen und einem beleuchteten Fitnessraum daneben",
   "наружный бассейн изогнутой формы в сумерках с каскадным краем, шезлонгами и освещённым тренажёрным залом рядом",
   "مسبح خارجي منحنٍ عند الغروب بحافة شلّالية ومقاعد تشمّس وصالة رياضية مضاءة بجانبه",
   "een gebogen buitenzwembad in de schemering, met een watervalrand, ligbedden en een verlichte gym ernaast",
   "zakrzywiony basen zewnętrzny o zmierzchu, z kaskadową krawędzią, leżakami i oświetloną siłownią obok",
   "et buet utendørs basseng i skumringen, med fossekant, solsenger og et opplyst treningsrom ved siden av",
   "en böjd utomhuspool i skymningen, med vattenfallskant, solstolar och ett upplyst gym intill")
a('The outdoor pool at dusk', "La piscina exterior al atardecer", "La piscine extérieure au crépuscule", "Der Außenpool in der Dämmerung", "Наружный бассейн в сумерках", "المسبح الخارجي عند الغروب", "Het buitenzwembad in de schemering", "Basen zewnętrzny o zmierzchu", "Utendørsbassenget i skumringen", "Utomhuspoolen i skymningen")
a('The pool and the sea', "La piscina y el mar", "La piscine et la mer", "Der Pool und das Meer", "Бассейн и море", "المسبح والبحر", "Het zwembad en de zee", "Basen i morze", "Bassenget og havet", "Poolen och havet")
cg('Computer-generated view across a pool towards planted gardens',
   "una piscina con jardines cuidados al fondo, con árboles en flor y un edificio detrás",
   "une piscine vue vers des jardins paysagers, avec des arbres en fleurs et un bâtiment au fond",
   "einem Blick über einen Pool auf bepflanzte Gärten mit blühenden Bäumen und einem Gebäude dahinter",
   "бассейн и ухоженные сады с цветущими деревьями, за ними здание",
   "منظر عبر مسبح نحو حدائق مزروعة بأشجار مزهرة ومبنى خلفها",
   "een blik over een zwembad naar aangelegde tuinen met bloeiende bomen en een gebouw erachter",
   "widok przez basen na obsadzone ogrody z kwitnącymi drzewami i budynkiem w tle",
   "utsikt over et basseng mot beplantede hager med blomstrende trær og en bygning bak",
   "utsikt över en pool mot planterade trädgårdar med blommande träd och en byggnad bakom")
a('The pool and the gardens', "La piscina y los jardines", "La piscine et les jardins", "Der Pool und die Gärten", "Бассейн и сады", "المسبح والحدائق", "Het zwembad en de tuinen", "Basen i ogrody", "Bassenget og hagene", "Poolen och trädgårdarna")
cg('Computer-generated view of a gym with large glass doors',
   "un gimnasio con grandes puertas de cristal que se abren a una terraza con esterillas de yoga",
   "une salle de sport avec de grandes portes vitrées donnant sur une terrasse garnie de tapis de yoga",
   "einem Fitnessraum mit großen Glastüren zu einer Terrasse mit Yogamatten",
   "тренажёрный зал с большими стеклянными дверями на террасу, где разложены коврики для йоги",
   "صالة رياضية بأبواب زجاجية كبيرة تفتح على تراس مفروش بسجادات اليوغا",
   "een gym met grote glazen deuren naar een terras met yogamatten",
   "siłownia z dużymi przeszklonymi drzwiami na taras z matami do jogi",
   "et treningsrom med store glassdører ut til en terrasse med yogamatter",
   "ett gym med stora glasdörrar mot en terrass med yogamattor")
a('The gym and its terrace', "El gimnasio y su terraza", "La salle de sport et sa terrasse", "Der Fitnessraum und seine Terrasse", "Тренажёрный зал и его терраса", "الصالة الرياضية وتراسها", "De gym en het bijbehorende terras", "Siłownia i jej taras", "Treningsrommet og terrassen", "Gymmet och dess terrass")
cg('Computer-generated view of a lounge and working area',
   "una zona de estar y de trabajo con sillones, mesas altas y una pared de lamas de madera",
   "un espace salon et travail avec des fauteuils, des tables hautes et un mur en lames de bois",
   "einem Aufenthalts- und Arbeitsbereich mit Sesseln, Stehtischen und einer Wand aus Holzlamellen",
   "зона отдыха и работы с креслами, высокими столами и стеной из деревянных реек",
   "منطقة جلوس وعمل بمقاعد وطاولات مرتفعة وجدار من الشرائح الخشبية",
   "een lounge- en werkruimte met fauteuils, hoge tafels en een wand van houten latten",
   "strefa wypoczynku i pracy z fotelami, wysokimi stołami i ścianą z drewnianych lameli",
   "et lounge- og arbeidsområde med lenestoler, høye bord og en vegg av trelameller",
   "en lounge- och arbetsyta med fåtöljer, höga bord och en vägg av träribbor")
a('The coworking area', "La zona de coworking", "L’espace de coworking", "Der Coworking-Bereich", "Зона коворкинга", "مساحة العمل المشترك", "De coworkingruimte", "Strefa coworkingu", "Coworking-området", "Coworkingytan")
cg('Computer-generated living room with sliding glass doors',
   "un salón con puertas correderas de cristal que se abren a una terraza amueblada y al mar",
   "un séjour avec des baies vitrées coulissantes donnant sur une terrasse meublée et la mer",
   "einem Wohnzimmer mit gläsernen Schiebetüren zu einer möblierten Terrasse und dem Meer",
   "гостиная со стеклянными раздвижными дверями на меблированную террасу и море",
   "غرفة معيشة بأبواب زجاجية منزلقة تفتح على تراس مفروش والبحر",
   "een woonkamer met glazen schuifdeuren naar een gemeubileerd terras en de zee",
   "salon z przeszklonymi drzwiami przesuwnymi na umeblowany taras i morze",
   "en stue med skyvedører i glass ut til en møblert terrasse og havet",
   "ett vardagsrum med skjutdörrar i glas mot en möblerad terrass och havet")
a('The living room and the terrace', "El salón y la terraza", "Le séjour et la terrasse", "Das Wohnzimmer und die Terrasse", "Гостиная и терраса", "غرفة المعيشة والتراس", "De woonkamer en het terras", "Salon i taras", "Stuen og terrassen", "Vardagsrummet och terrassen")
cg('Computer-generated white kitchen with an island',
   "una cocina blanca con isla y taburetes, muebles altos efecto madera y una ventana",
   "une cuisine blanche avec îlot et tabourets, des meubles hauts effet bois et une fenêtre",
   "einer weißen Küche mit Kochinsel und Hockern, Hängeschränken in Holzoptik und einem Fenster",
   "белая кухня с островом и барными стульями, навесными шкафами под дерево и окном",
   "مطبخ أبيض بجزيرة ومقاعد مرتفعة وخزائن علوية بتشطيب خشبي ونافذة",
   "een witte keuken met een kookeiland en barkrukken, bovenkasten in houtlook en een raam",
   "biała kuchnia z wyspą i hokerami, szafkami górnymi w wykończeniu drewnopodobnym i oknem",
   "et hvitt kjøkken med øy og barstoler, overskap i trelook og et vindu",
   "ett vitt kök med köksö och barstolar, överskåp i träimitation och ett fönster")
cg('Computer-generated bedroom with a double bed, a walk-in wardrobe',
   "un dormitorio con cama doble, vestidor y una puerta corredera de cristal a una terraza",
   "une chambre avec un lit double, un dressing et une porte coulissante vitrée sur une terrasse",
   "einem Schlafzimmer mit Doppelbett, begehbarem Kleiderschrank und einer gläsernen Schiebetür zur Terrasse",
   "спальня с двуспальной кроватью, гардеробной и стеклянной раздвижной дверью на террасу",
   "غرفة نوم بسرير مزدوج وغرفة ملابس وباب زجاجي منزلق يفتح على تراس",
   "een slaapkamer met een tweepersoonsbed, een inloopkast en een glazen schuifdeur naar een terras",
   "sypialnia z łóżkiem dwuosobowym, garderobą i przeszklonymi drzwiami przesuwnymi na taras",
   "et soverom med dobbeltseng, walk-in-garderobe og en skyvedør i glass ut til en terrasse",
   "ett sovrum med dubbelsäng, walk-in-garderob och en skjutdörr i glas mot en terrass")
cg('Computer-generated bedroom with a double bed, a timber-slat',
   "un dormitorio con cama doble, una pared de cabecero con lamas de madera y una puerta corredera de cristal a una terraza con vistas al mar",
   "une chambre avec un lit double, un mur de tête de lit en lames de bois et une porte coulissante vitrée sur une terrasse avec vue sur la mer",
   "einem Schlafzimmer mit Doppelbett, einer Kopfteilwand aus Holzlamellen und einer gläsernen Schiebetür zu einer Terrasse mit Meerblick",
   "спальня с двуспальной кроватью, стеной изголовья из деревянных реек и стеклянной раздвижной дверью на террасу с видом на море",
   "غرفة نوم بسرير مزدوج وجدار خلف السرير من الشرائح الخشبية وباب زجاجي منزلق يفتح على تراس بإطلالة على البحر",
   "een slaapkamer met een tweepersoonsbed, een hoofdeindwand van houten latten en een glazen schuifdeur naar een terras met zeezicht",
   "sypialnia z łóżkiem dwuosobowym, ścianą za wezgłowiem z drewnianych lameli i przeszklonymi drzwiami przesuwnymi na taras z widokiem na morze",
   "et soverom med dobbeltseng, en hodegavlvegg av trelameller og en skyvedør i glass ut til en terrasse med utsikt mot havet",
   "ett sovrum med dubbelsäng, en sänggavelvägg av träribbor och en skjutdörr i glas mot en terrass med havsutsikt")
cg('Computer-generated bathroom with a double washbasin',
   "un baño con lavabo doble, inodoro suspendido y una ducha a ras de suelo con mampara de cristal",
   "une salle de bains avec double vasque, WC suspendu et une douche à l’italienne avec paroi en verre",
   "einem Bad mit Doppelwaschtisch, wandhängendem WC und einer bodenebenen Dusche mit Glaswand",
   "ванная комната с двойной раковиной, подвесным унитазом и душем с остеклённой перегородкой",
   "حمّام بمغسلة مزدوجة ومرحاض معلّق ودش مع حاجز زجاجي",
   "een badkamer met een dubbele wastafel, een hangend toilet en een inloopdouche met glazen wand",
   "łazienka z podwójną umywalką, podwieszaną toaletą i prysznicem bezbrodzikowym ze szklaną ścianką",
   "et bad med dobbel servant, hengende toalett og en gulvflush dusj med glassvegg",
   "ett badrum med dubbel handfat, vägghängd toalett och en duschplats med glasvägg")
cg('Computer-generated terrace with lounge seating',
   "una terraza con asientos de estar, una barandilla de cristal y una amplia vista de la costa y el mar",
   "une terrasse avec un salon d’extérieur, un garde-corps en verre et une vaste vue sur la côte et la mer",
   "einer Terrasse mit Loungemöbeln, einer Glasbrüstung und weitem Blick auf die Küste und das Meer",
   "терраса с мягкой мебелью, стеклянным ограждением и широким видом на побережье и море",
   "تراس بمقاعد جلوس ودرابزين زجاجي وإطلالة واسعة على الساحل والبحر",
   "een terras met loungemeubilair, een glazen balustrade en een wijds uitzicht over de kust en de zee",
   "taras z meblami wypoczynkowymi, szklaną balustradą i szerokim widokiem na wybrzeże i morze",
   "en terrasse med loungemøbler, et glassrekkverk og vid utsikt over kysten og havet",
   "en terrass med loungemöbler, ett glasräcke och en vid utsikt över kusten och havet")
a('A terrace facing the sea', "Una terraza orientada al mar", "Une terrasse face à la mer", "Eine Terrasse zum Meer", "Терраса с видом на море", "تراس مطلّ على البحر", "Een terras op de zee", "Taras zwrócony ku morzu", "En terrasse mot havet", "En terrass mot havet")
cg('Computer-generated large covered terrace',
   "una gran terraza cubierta con sofás y mesas bajas, que se abre al salón",
   "une grande terrasse couverte avec canapés et tables basses, ouverte sur le séjour",
   "einer großen überdachten Terrasse mit Sofas und niedrigen Tischen, die sich zum Wohnzimmer öffnet",
   "большая крытая терраса с диванами и низкими столиками, переходящая в гостиную",
   "تراس مغطى كبير بأرائك وطاولات منخفضة يفتح على غرفة المعيشة",
   "een groot overdekt terras met banken en lage tafels, dat uitkomt op de woonkamer",
   "duży zadaszony taras z sofami i niskimi stolikami, otwierający się na salon",
   "en stor overbygd terrasse med sofaer og lave bord, som åpner seg mot stuen",
   "en stor täckt terrass med soffor och låga bord, som öppnar sig mot vardagsrummet")
a('A covered terrace', "Una terraza cubierta", "Une terrasse couverte", "Eine überdachte Terrasse", "Крытая терраса", "تراس مغطى", "Een overdekt terras", "Zadaszony taras", "En overbygd terrasse", "En täckt terrass")
cg('Computer-generated solarium terrace',
   "una terraza solárium con un sofá, una mesa de centro y vistas al mar",
   "une terrasse solarium avec un canapé, une table basse et vue sur la mer",
   "einer Solarium-Terrasse mit Sofa, Couchtisch und Meerblick",
   "терраса-солярий с диваном, журнальным столиком и видом на море",
   "تراس سولاريوم بأريكة وطاولة قهوة وإطلالة على البحر",
   "een solariumterras met een bank, een salontafel en zeezicht",
   "taras-solarium z sofą, stolikiem kawowym i widokiem na morze",
   "en solterrasse med en sofa, et salongbord og utsikt mot havet",
   "en solterrass med en soffa, ett soffbord och havsutsikt")
a('A solarium', "Un solárium", "Un solarium", "Ein Solarium", "Солярий", "سولاريوم", "Een solarium", "Solarium", "En solterrasse", "En solterrass")
a('Photograph of a wooded hillside looking over the coast',
  "Fotografía de una ladera boscosa con vistas a la costa, con una carretera y el mar a lo lejos",
  "Photographie d’une colline boisée dominant la côte, avec une route et la mer au loin",
  "Foto eines bewaldeten Hangs mit Blick über die Küste, mit einer Straße und dem Meer in der Ferne",
  "Фотография лесистого склона с видом на побережье: дорога и вдали море",
  "صورة فوتوغرافية لمنحدر مشجّر يطلّ على الساحل، مع طريق والبحر في البعيد",
  "Foto van een beboste helling met uitzicht over de kust, met een weg en in de verte de zee",
  "Zdjęcie zalesionego zbocza z widokiem na wybrzeże, z drogą i morzem w oddali",
  "Fotografi av en skogkledd åsside med utsikt over kysten, med en vei og havet i det fjerne",
  "Fotografi av en skogklädd sluttning med utsikt över kusten, med en väg och havet i fjärran")
a('The hillside above the coast', "La ladera sobre la costa", "La colline au-dessus de la côte", "Der Hang über der Küste", "Склон над побережьем", "المنحدر فوق الساحل", "De helling boven de kust", "Zbocze nad wybrzeżem", "Åssiden over kysten", "Sluttningen ovanför kusten")
a('Photograph of a cleared stretch of hillside',
  "Fotografía de un tramo despejado de la ladera, con matorral y olivos, y el mar en el horizonte",
  "Photographie d’une portion dégagée de la colline, avec broussailles et oliviers, et la mer à l’horizon",
  "Foto eines freigeräumten Hangabschnitts mit Buschwerk und Olivenbäumen und dem Meer am Horizont",
  "Фотография расчищенного участка склона с кустарником и оливами, на горизонте море",
  "صورة فوتوغرافية لجزء مُهيّأ من المنحدر بشجيرات وأشجار زيتون، والبحر عند الأفق",
  "Foto van een vrijgemaakt stuk helling met struikgewas en olijfbomen, met de zee aan de horizon",
  "Zdjęcie oczyszczonego fragmentu zbocza z zaroślami i drzewami oliwnymi, z morzem na horyzoncie",
  "Fotografi av en ryddet del av åssiden med kratt og oliventrær, og havet i horisonten",
  "Fotografi av en röjd del av sluttningen med snår och olivträd, och havet vid horisonten")
a('A cleared stretch of the hillside', "Un tramo despejado de la ladera", "Une portion dégagée de la colline", "Ein freigeräumter Hangabschnitt", "Расчищенный участок склона", "جزء مُهيّأ من المنحدر", "Een vrijgemaakt stuk van de helling", "Oczyszczony fragment zbocza", "En ryddet del av åssiden", "En röjd del av sluttningen")

# ---------------------------------------------------------------- overview, why, architecture
a('Eighteen homes, <em>listed with prices</em>',
  "Dieciocho viviendas, <em>con precio</em>", "Dix-huit logements, <em>avec leur prix</em>", "Achtzehn Wohnungen, <em>mit Preis</em>",
  "Восемнадцать квартир <em>с ценами</em>", "ثمانية عشر مسكنًا <em>بأسعارها</em>", "Achttien woningen, <em>met prijs</em>",
  "Osiemnaście lokali <em>z cenami</em>", "Atten boliger <em>med pris</em>", "Arton bostäder <em>med pris</em>")
a('Altamira Hills Residences is a development of apartments and duplex penthouses',
  "Altamira Hills Residences es una promoción de apartamentos y áticos dúplex en la parte alta de Los Monteros, al este de Marbella. Las viviendas a la venta tienen dos o tres dormitorios, dos baños y grandes terrazas con vistas al mar, y algunas viviendas de planta baja tienen además un jardín privado. Los edificios suben por la ladera en cuatro alturas.",
  "Altamira Hills Residences est un programme d’appartements et de penthouses duplex dans la partie haute de Los Monteros, à l’est de Marbella. Les logements proposés ont deux ou trois chambres, deux salles de bains et de grandes terrasses avec vue sur la mer, et certains logements du rez-de-chaussée ont aussi un jardin privé. Les bâtiments montent la colline sur quatre niveaux.",
  "Altamira Hills Residences ist eine Anlage mit Wohnungen und Maisonette-Penthouses im oberen Teil von Los Monteros, östlich von Marbella. Die angebotenen Wohnungen haben zwei oder drei Schlafzimmer, zwei Bäder und große Terrassen mit Meerblick, und einige Erdgeschosswohnungen haben zusätzlich einen privaten Garten. Die Gebäude steigen in vier Höhen den Hang hinauf.",
  "Altamira Hills Residences — комплекс квартир и двухуровневых пентхаусов в верхней части Лос-Монтероса, к востоку от Марбельи. В продаже квартиры с двумя или тремя спальнями, двумя ванными комнатами и большими террасами с видом на море, а у некоторых квартир на первом этаже есть ещё и частный сад. Здания поднимаются по склону в четыре уровня.",
  "Altamira Hills Residences مجمّع شقق وبنتهاوس دوبلكس في الجزء العلوي من لوس مونتيروس، شرق مربيّا. المساكن المعروضة بغرفتي نوم أو ثلاث غرف نوم وحمّامين وتراسات واسعة بإطلالات على البحر، ولبعض مساكن الطابق الأرضي حديقة خاصة أيضًا. وترتفع المباني على المنحدر بأربعة ارتفاعات.",
  "Altamira Hills Residences is een complex van appartementen en duplexpenthouses in het hoger gelegen deel van Los Monteros, ten oosten van Marbella. De aangeboden woningen hebben twee of drie slaapkamers, twee badkamers en grote terrassen met zeezicht, en enkele woningen op de begane grond hebben ook een eigen tuin. De gebouwen stijgen in vier hoogtes langs de helling.",
  "Altamira Hills Residences to osiedle apartamentów i dwupoziomowych penthouse’ów w górnej części Los Monteros, na wschód od Marbelli. Oferowane lokale mają dwie lub trzy sypialnie, dwie łazienki i duże tarasy z widokiem na morze, a niektóre lokale na parterze mają także prywatny ogród. Budynki wznoszą się po zboczu na czterech wysokościach.",
  "Altamira Hills Residences er et anlegg med leiligheter og toppleiligheter over to plan i den øvre delen av Los Monteros, øst for Marbella. Boligene som er til salgs har to eller tre soverom, to bad og store terrasser med utsikt mot havet, og noen av boligene i første etasje har også en privat hage. Byggene stiger oppover åssiden i fire høyder.",
  "Altamira Hills Residences är ett område med lägenheter och takvåningar i två plan i övre delen av Los Monteros, öster om Marbella. Bostäderna som är till salu har två eller tre sovrum, två badrum och stora terrasser med havsutsikt, och några av bostäderna på bottenvåningen har också en privat trädgård. Byggnaderna stiger uppför sluttningen i fyra höjder.")
a('The community has an outdoor pool, a heated indoor pool',
  "La comunidad tiene una piscina exterior, una piscina interior climatizada, un spa, un gimnasio con terraza propia, un bar de piscina y una zona de coworking, en jardines cuidados. Los documentos del promotor no indican una fecha de entrega.",
  "La résidence compte une piscine extérieure, une piscine intérieure chauffée, un spa, une salle de sport avec sa propre terrasse, un bar de piscine et un espace de coworking, dans des jardins paysagers. Les documents du promoteur ne donnent pas de date de livraison.",
  "Die Gemeinschaftsanlage hat einen Außenpool, einen beheizten Innenpool, ein Spa, einen Fitnessraum mit eigener Terrasse, eine Poolbar und einen Coworking-Bereich in gepflegten Gärten. Die Unterlagen des Bauträgers nennen keinen Fertigstellungstermin.",
  "В комплексе есть наружный бассейн, подогреваемый внутренний бассейн, спа, тренажёрный зал с собственной террасой, бар у бассейна и коворкинг среди ухоженных садов. В документах застройщика срок сдачи не указан.",
  "يضم المجمّع مسبحًا خارجيًا ومسبحًا داخليًا مدفأً وسبا وصالة رياضية بتراس خاص وبار مسبح ومساحة للعمل المشترك، وسط حدائق مهيّأة. ولا تذكر وثائق المطوّر موعدًا للتسليم.",
  "De gemeenschap heeft een buitenzwembad, een verwarmd binnenzwembad, een spa, een gym met eigen terras, een poolbar en een coworkingruimte, in aangelegde tuinen. De documenten van de ontwikkelaar noemen geen opleveringsdatum.",
  "Wspólnota ma basen zewnętrzny, podgrzewany basen wewnętrzny, spa, siłownię z własnym tarasem, bar przy basenie i strefę coworkingu, w pielęgnowanych ogrodach. Dokumenty dewelopera nie podają terminu oddania.",
  "Fellesområdet har et utendørs basseng, et oppvarmet innendørs basseng, et spa, et treningsrom med egen terrasse, en bassengbar og et coworking-område, i opparbeidede hager. Utbyggerens dokumenter oppgir ingen overleveringsdato.",
  "Området har en utomhuspool, en uppvärmd inomhuspool, ett spa, ett gym med egen terrass, en poolbar och en coworkingyta, i anlagda trädgårdar. Exploatörens dokument anger inget leveransdatum.")
a('Listed', "A la venta", "Proposés", "Angeboten", "В продаже", "المعروض", "Aangeboden", "W ofercie", "Til salgs", "Till salu")
a('18 homes', "18 viviendas", "18 logements", "18 Wohnungen", "18 квартир", "18 مسكنًا", "18 woningen", "18 lokali", "18 boliger", "18 bostäder")
a('Large terraces, and gardens on some ground-floor homes',
  "Grandes terrazas, y jardines en algunas viviendas de planta baja", "De grandes terrasses, et des jardins pour certains logements du rez-de-chaussée",
  "Große Terrassen und Gärten bei einigen Erdgeschosswohnungen", "Большие террасы и сады у некоторых квартир на первом этаже",
  "تراسات واسعة وحدائق في بعض مساكن الطابق الأرضي", "Grote terrassen, en tuinen bij enkele woningen op de begane grond",
  "Duże tarasy oraz ogrody przy niektórych lokalach na parterze", "Store terrasser, og hager til noen av boligene i første etasje",
  "Stora terrasser, och trädgårdar till några av bostäderna på bottenvåningen")
a('Large terraces facing the sea in the hills above Marbella',
  "Grandes terrazas orientadas al mar en las colinas sobre Marbella, con las instalaciones de un resort.",
  "De grandes terrasses face à la mer dans les collines au-dessus de Marbella, avec les équipements d’un resort.",
  "Große Terrassen mit Meerblick in den Hügeln über Marbella, mit der Ausstattung eines Resorts.",
  "Большие террасы с видом на море в холмах над Марбельей и инфраструктура курорта.",
  "تراسات واسعة مطلّة على البحر في التلال فوق مربيّا، مع مرافق منتجع.",
  "Grote terrassen op de zee in de heuvels boven Marbella, met de voorzieningen van een resort.",
  "Duże tarasy zwrócone ku morzu na wzgórzach nad Marbellą, z infrastrukturą kurortu.",
  "Store terrasser mot havet i åsene over Marbella, med fasilitetene til et feriested.",
  "Stora terrasser mot havet i kullarna ovanför Marbella, med ett resorts bekvämligheter.")
a('Buyers who want a spacious two- or three-bedroom home',
  "Compradores que buscan una vivienda amplia de dos o tres dormitorios con una gran terraza y vistas al mar, y una piscina, un spa y un gimnasio en la comunidad.",
  "Acheteurs qui souhaitent un logement spacieux de deux ou trois chambres avec une grande terrasse et vue sur la mer, et une piscine, un spa et une salle de sport dans la résidence.",
  "Käufer, die eine geräumige Wohnung mit zwei oder drei Schlafzimmern, großer Terrasse und Meerblick suchen und in der Anlage einen Pool, ein Spa und einen Fitnessraum schätzen.",
  "Покупатели, которым нужна просторная квартира с двумя или тремя спальнями, большой террасой и видом на море, а в комплексе — бассейн, спа и тренажёрный зал.",
  "مشترون يريدون مسكنًا واسعًا بغرفتي نوم أو ثلاث غرف نوم وتراس كبير وإطلالة على البحر، مع مسبح وسبا وصالة رياضية في المجمّع.",
  "Kopers die een ruime woning met twee of drie slaapkamers, een groot terras en zeezicht zoeken, met een zwembad, spa en gym in de gemeenschap.",
  "Kupujący, którzy szukają przestronnego lokalu z dwiema lub trzema sypialniami, dużym tarasem i widokiem na morze oraz basenu, spa i siłowni we wspólnocie.",
  "Kjøpere som vil ha en romslig bolig med to eller tre soverom, en stor terrasse og utsikt mot havet, og et basseng, et spa og et treningsrom i fellesområdet.",
  "Köpare som vill ha en rymlig bostad med två eller tre sovrum, en stor terrass och havsutsikt, och en pool, ett spa och ett gym i området.")
a('Large terraces: 13 of the 18 homes',
  "Grandes terrazas: 13 de las 18 viviendas tienen 49.70 {U} o más, y los áticos hasta 121.90 {U}.",
  "De grandes terrasses : 13 des 18 logements ont 49.70 {U} ou plus, et les penthouses jusqu’à 121.90 {U}.",
  "Große Terrassen: 13 der 18 Wohnungen haben 49.70 {U} oder mehr, die Penthouses bis zu 121.90 {U}.",
  "Большие террасы: у 13 из 18 квартир они занимают 49.70 {U} и больше, а у пентхаусов — до 121.90 {U}.",
  "تراسات واسعة: 13 من أصل 18 مسكنًا مساحة تراسها 49.70 {U} أو أكثر، وتصل في البنتهاوس إلى 121.90 {U}.",
  "Grote terrassen: 13 van de 18 woningen hebben 49.70 {U} of meer, en de penthouses tot 121.90 {U}.",
  "Duże tarasy: 13 z 18 lokali ma 49.70 {U} lub więcej, a penthouse’y do 121.90 {U}.",
  "Store terrasser: 13 av de 18 boligene har 49.70 {U} eller mer, og toppleilighetene opptil 121.90 {U}.",
  "Stora terrasser: 13 av de 18 bostäderna har 49.70 {U} eller mer, och takvåningarna upp till 121.90 {U}.")
a('The development is in the upper part of Los Monteros, about 10 minutes from the centre of Marbella and its old town, on a hillside',
  "La promoción está en la parte alta de Los Monteros, a unos 10 minutos del centro de Marbella y de su casco antiguo, en una ladera con vistas al mar.",
  "Le programme se trouve dans la partie haute de Los Monteros, à environ 10 minutes du centre de Marbella et de sa vieille ville, sur une colline avec vue sur la mer.",
  "Die Anlage liegt im oberen Teil von Los Monteros, etwa 10 Minuten vom Zentrum von Marbella und seiner Altstadt entfernt, an einem Hang mit Meerblick.",
  "Комплекс находится в верхней части Лос-Монтероса, примерно в 10 минутах от центра Марбельи и её старого города, на склоне с видом на море.",
  "يقع المجمّع في الجزء العلوي من لوس مونتيروس، على بعد نحو 10 دقائق من وسط مربيّا وبلدتها القديمة، على منحدر بإطلالة على البحر.",
  "Het complex ligt in het hoger gelegen deel van Los Monteros, op ongeveer 10 minuten van het centrum van Marbella en de oude stad, op een helling met zeezicht.",
  "Osiedle leży w górnej części Los Monteros, około 10 minut od centrum Marbelli i jej starego miasta, na zboczu z widokiem na morze.",
  "Anlegget ligger i den øvre delen av Los Monteros, omtrent 10 minutter fra sentrum av Marbella og gamlebyen, i en åsside med utsikt mot havet.",
  "Området ligger i övre delen av Los Monteros, cirka 10 minuter från Marbellas centrum och gamla stad, i en sluttning med havsutsikt.")
a('The prices come from the developer’s list as shown on its portal in October 2026',
  "Los precios proceden de la lista del promotor tal como aparece en su portal en octubre de 2026, y las viviendas aún no están construidas. Nueva Living vuelve a confirmar precio y disponibilidad antes de cualquier visita.",
  "Les prix proviennent de la liste du promoteur telle qu’elle figure sur son portail en octobre 2026, et les logements ne sont pas encore construits. Nueva Living reconfirme le prix et la disponibilité avant toute visite.",
  "Die Preise stammen aus der Liste des Bauträgers, wie sie im Oktober 2026 auf dessen Portal zu sehen war, und die Wohnungen sind noch nicht gebaut. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung erneut.",
  "Цены взяты из списка застройщика, опубликованного на его портале в октябре 2026 года, и квартиры ещё не построены. Nueva Living повторно подтверждает цену и наличие перед любым просмотром.",
  "الأسعار مأخوذة من قائمة المطوّر كما ظهرت على بوابته في أكتوبر 2026، والمساكن لم تُبنَ بعد. تعيد Nueva Living تأكيد السعر والتوافر قبل أي معاينة.",
  "De prijzen komen uit de lijst van de ontwikkelaar zoals die in oktober 2026 op zijn portaal stond, en de woningen zijn nog niet gebouwd. Nueva Living bevestigt prijs en beschikbaarheid opnieuw vóór elke bezichtiging.",
  "Ceny pochodzą z listy dewelopera widocznej na jego portalu w październiku 2026 roku, a lokale nie są jeszcze zbudowane. Nueva Living ponownie potwierdza cenę i dostępność przed każdym oglądaniem.",
  "Prisene er hentet fra utbyggerens liste slik den sto på portalen i oktober 2026, og boligene er ikke bygget ennå. Nueva Living bekrefter pris og tilgjengelighet på nytt før enhver visning.",
  "Priserna kommer från exploatörens lista så som den visades på dess portal i oktober 2026, och bostäderna är inte byggda ännu. Nueva Living bekräftar pris och tillgänglighet på nytt före varje visning.")
a('White terraces, <em>stepped to the sea</em>',
  "Terrazas blancas, <em>escalonadas hacia el mar</em>", "Des terrasses blanches, <em>en gradins vers la mer</em>", "Weiße Terrassen, <em>zum Meer hin abgestuft</em>",
  "Белые террасы, <em>ступенями к морю</em>", "تراسات بيضاء <em>متدرّجة نحو البحر</em>", "Witte terrassen, <em>getrapt naar de zee</em>",
  "Białe tarasy <em>schodkowo ku morzu</em>", "Hvite terrasser, <em>trappet mot havet</em>", "Vita terrasser, <em>trappande mot havet</em>")
a('The buildings are designed around light and views',
  "Los edificios están diseñados en torno a la luz y las vistas, en cuatro alturas y con un ático dúplex con solárium en la parte superior. Amplias terrazas recorren cada planta, y los salones se abren a ellas mediante grandes puertas correderas.",
  "Les bâtiments sont conçus autour de la lumière et des vues, sur quatre niveaux, avec un penthouse duplex et son solarium au sommet. De larges terrasses courent le long de chaque étage, et les séjours s’ouvrent sur elles par de grandes baies coulissantes.",
  "Die Gebäude sind um Licht und Aussicht herum entworfen, in vier Höhen, mit einem Maisonette-Penthouse mit Solarium als oberem Abschluss. Breite Terrassen laufen an jeder Etage entlang, und die Wohnzimmer öffnen sich über große Schiebetüren zu ihnen.",
  "Здания спроектированы вокруг света и видов, в четыре уровня, а наверху — двухуровневый пентхаус с солярием. Вдоль каждого этажа тянутся широкие террасы, и гостиные выходят на них через большие раздвижные двери.",
  "صُمّمت المباني حول الضوء والإطلالات، بأربعة ارتفاعات وبنتهاوس دوبلكس بسولاريوم في الأعلى. تمتد تراسات عريضة على طول كل طابق، وتفتح غرف المعيشة عليها عبر أبواب منزلقة كبيرة.",
  "De gebouwen zijn ontworpen rond licht en uitzicht, in vier hoogtes, met bovenaan een duplexpenthouse met solarium. Brede terrassen lopen langs elke verdieping en de woonkamers openen zich er via grote schuifdeuren op.",
  "Budynki zaprojektowano wokół światła i widoków, na czterech wysokościach, z dwupoziomowym penthouse’em z solarium na szczycie. Szerokie tarasy biegną wzdłuż każdego piętra, a salony otwierają się na nie dużymi drzwiami przesuwnymi.",
  "Byggene er tegnet rundt lys og utsikt, i fire høyder, med en toppleilighet over to plan med solterrasse øverst. Brede terrasser løper langs hver etasje, og stuene åpner seg mot dem gjennom store skyvedører.",
  "Byggnaderna är ritade kring ljus och utsikt, i fyra höjder, med en takvåning i två plan med solterrass överst. Breda terrasser löper längs varje våning, och vardagsrummen öppnar sig mot dem genom stora skjutdörrar.")
a('The renders show white volumes with dark accents',
  "Las recreaciones muestran volúmenes blancos con detalles oscuros, barandillas de cristal y jardines plantados entre los bloques.",
  "Les images de synthèse montrent des volumes blancs avec des touches sombres, des garde-corps en verre et des jardins plantés entre les blocs.",
  "Die Visualisierungen zeigen weiße Baukörper mit dunklen Akzenten, Glasbrüstungen und bepflanzte Gärten zwischen den Blöcken.",
  "На визуализациях белые объёмы с тёмными акцентами, стеклянные ограждения и озеленённые сады между блоками.",
  "تُظهر الصور المولّدة كتلًا بيضاء بلمسات داكنة ودرابزينات زجاجية وحدائق مزروعة بين المباني.",
  "De beelden tonen witte volumes met donkere accenten, glazen balustrades en beplante tuinen tussen de blokken.",
  "Wizualizacje pokazują białe bryły z ciemnymi akcentami, szklane balustrady i obsadzone ogrody między blokami.",
  "Bildene viser hvite volumer med mørke detaljer, glassrekkverk og beplantede hager mellom byggene.",
  "Bilderna visar vita volymer med mörka accenter, glasräcken och planterade trädgårdar mellan husen.")
a('A continuous mortar coating over high-quality thermal insulation',
  "Un revestimiento continuo de mortero sobre un aislamiento térmico de alta calidad, con un trasdosado de placa de yeso aislado en el interior.",
  "Un enduit de mortier continu sur une isolation thermique de haute qualité, avec une doublure intérieure en plaques de plâtre isolées.",
  "Eine durchgehende Mörtelbeschichtung über hochwertiger Wärmedämmung, innen mit gedämmter Gipskartonverkleidung.",
  "Сплошное растворное покрытие поверх высококачественного утеплителя, внутри — утеплённая облицовка из гипсокартона.",
  "طلاء متواصل من الملاط فوق عزل حراري عالي الجودة، مع تبطين داخلي من ألواح الجبس المعزولة.",
  "Een doorlopende mortellaag over hoogwaardige thermische isolatie, met binnenin een geïsoleerde gipsplaatbekleding.",
  "Ciągła powłoka z zaprawy na wysokiej jakości izolacji termicznej, a od wewnątrz ocieplona okładzina z płyt gipsowo-kartonowych.",
  "Et sammenhengende mørtelbelegg over varmeisolasjon av høy kvalitet, med isolert gipsplatekledning innvendig.",
  "En sammanhängande murbrukbeläggning över högkvalitativ värmeisolering, med isolerad gipsskivebeklädnad invändigt.")
a('Large slabs of non-slip porcelain stoneware',
  "Grandes losas de gres porcelánico antideslizante, con continuidad entre la terraza y el salón.",
  "De grandes dalles de grès cérame antidérapant, avec une continuité entre la terrasse et le séjour.",
  "Große rutschfeste Feinsteinzeugplatten, mit durchgehender Fläche zwischen Terrasse und Wohnzimmer.",
  "Крупные плиты нескользящего керамогранита, с единой поверхностью между террасой и гостиной.",
  "بلاطات كبيرة من خزف البورسلين المانع للانزلاق، مع استمرارية بين التراس وغرفة المعيشة.",
  "Grote platen antislip porseleinen tegels, met een doorlopend vlak tussen terras en woonkamer.",
  "Duże płyty antypoślizgowego gresu porcelanowego, z ciągłością między tarasem a salonem.",
  "Store heller av sklisikker porselensfliser, med en sammenhengende flate mellom terrasse og stue.",
  "Stora plattor av halkfritt porslinsgrés, med en sammanhängande yta mellan terrass och vardagsrum.")
a('Lacquered aluminium frames with a thermal break',
  "Carpintería de aluminio lacado con rotura de puente térmico y doble acristalamiento con aislamiento acústico.",
  "Menuiseries en aluminium laqué à rupture de pont thermique et double vitrage à isolation phonique.",
  "Lackierte Aluminiumrahmen mit thermischer Trennung und schalldämmender Doppelverglasung.",
  "Окрашенные алюминиевые рамы с терморазрывом и двойное остекление с шумоизоляцией.",
  "إطارات من الألمنيوم المطلي بقاطع حراري وزجاج مزدوج عازل للصوت.",
  "Gelakte aluminium kozijnen met thermische onderbreking en geluidwerende dubbele beglazing.",
  "Lakierowane ramy aluminiowe z przerwą termiczną i dźwiękoszczelne podwójne szyby.",
  "Lakkerte aluminiumsrammer med kuldebro-brudd og lydisolerende dobbeltglass.",
  "Lackerade aluminiumkarmar med köldbrygga-brytning och ljudisolerande dubbelglas.")
a('Reinforced concrete foundations and structure',
  "Cimentación y estructura de hormigón armado.", "Fondations et structure en béton armé.", "Fundament und Tragwerk aus Stahlbeton.",
  "Фундамент и каркас из железобетона.", "أساسات وهيكل من الخرسانة المسلّحة.", "Fundering en draagstructuur van gewapend beton.",
  "Fundamenty i konstrukcja z żelbetu.", "Fundament og bæresystem i armert betong.", "Grund och stomme av armerad betong.")

# ---------------------------------------------------------------- quality specification
a('Source: the developer’s quality specification for this development, which is undated',
  "Fuente: la memoria de calidades del promotor para esta promoción, que no lleva fecha. Es orientativa y no contractual, y sus materiales pueden sustituirse por otros de igual o superior calidad.",
  "Source : la notice descriptive du promoteur pour ce programme, qui n’est pas datée. Elle est indicative et non contractuelle, et ses matériaux peuvent être remplacés par d’autres de qualité égale ou supérieure.",
  "Quelle: die Ausstattungsbeschreibung des Bauträgers für diese Anlage, die kein Datum trägt. Sie ist unverbindlich und nicht vertraglich, und ihre Materialien können durch gleich- oder höherwertige ersetzt werden.",
  "Источник: описание качества застройщика для этого комплекса, без даты. Оно носит ориентировочный характер и не является договорным, а материалы могут быть заменены на равноценные или более качественные.",
  "المصدر: مواصفات الجودة الخاصة بالمطوّر لهذا المشروع، وهي غير مؤرَّخة. وهي استرشادية وغير تعاقدية، ويجوز استبدال موادها بمواد مماثلة أو أعلى جودة.",
  "Bron: de kwaliteitsomschrijving van de ontwikkelaar voor dit complex, die geen datum draagt. Zij is indicatief en niet contractueel, en de materialen kunnen worden vervangen door gelijkwaardige of betere.",
  "Źródło: opis jakości dewelopera dla tej inwestycji, bez daty. Ma charakter orientacyjny i nie jest umowny, a użyte materiały mogą zostać zastąpione równorzędnymi lub lepszymi.",
  "Kilde: utbyggerens kvalitetsbeskrivelse for dette anlegget, som ikke er datert. Den er veiledende og ikke kontraktsfestet, og materialene kan byttes ut med likeverdige eller bedre.",
  "Källa: exploatörens kvalitetsbeskrivning för detta område, som saknar datum. Den är vägledande och inte avtalsenlig, och materialen kan bytas ut mot likvärdiga eller bättre.")
a('Large-slab porcelain stoneware floors',
  "Suelos de gres porcelánico de gran formato, en tres opciones de color, con rodapié lacado en blanco, y tabiques interiores de placa de yeso aislada.",
  "Sols en grès cérame grand format, en trois coloris au choix, avec plinthes laquées blanc, et cloisons intérieures en plaques de plâtre isolées.",
  "Bodenbeläge aus großformatigem Feinsteinzeug in drei Farboptionen mit weiß lackierten Sockelleisten und gedämmten Gipskarton-Innenwänden.",
  "Полы из крупноформатного керамогранита в трёх вариантах цвета с белыми окрашенными плинтусами и утеплённые внутренние перегородки из гипсокартона.",
  "أرضيات من خزف البورسلين كبير الحجم بثلاثة خيارات لونية مع أرضيات جدارية مطلية بالأبيض، وجدران داخلية من ألواح الجبس المعزولة.",
  "Vloeren van grootformaat porseleinen tegels in drie kleuropties, met wit gelakte plinten, en geïsoleerde gipsplaat binnenwanden.",
  "Podłogi z wielkoformatowego gresu porcelanowego w trzech wariantach kolorystycznych, z białymi lakierowanymi listwami przypodłogowymi, oraz ocieplone ściany wewnętrzne z płyt gipsowo-kartonowych.",
  "Gulv av storformat porselensfliser i tre fargealternativer, med hvitlakkerte gulvlister, og isolerte innvendige vegger av gipsplater.",
  "Golv av storformat porslinsgrés i tre färgval, med vitlackerade golvlister, och isolerade invändiga väggar av gipsskivor.")
a('A security entrance door with a security lock',
  "Una puerta de entrada de seguridad con cerradura de seguridad, puertas interiores lacadas y armarios modulares lacados con balda superior, barra de colgar y forro interior.",
  "Une porte d’entrée blindée avec serrure de sécurité, des portes intérieures laquées et des placards modulaires laqués avec tablette haute, barre de penderie et habillage intérieur.",
  "Eine Sicherheits-Wohnungseingangstür mit Sicherheitsschloss, lackierte Innentüren und modulare lackierte Kleiderschränke mit Ablage, Kleiderstange und Innenverkleidung.",
  "Бронированная входная дверь с замком повышенной надёжности, окрашенные межкомнатные двери и модульные окрашенные шкафы с верхней полкой, штангой и внутренней отделкой.",
  "باب دخول أمني بقفل أمان، وأبواب داخلية مطلية، وخزائن ملابس مطلية بوحدات مع رف علوي وعمود تعليق وتبطين داخلي.",
  "Een veiligheidsvoordeur met veiligheidsslot, gelakte binnendeuren en modulaire gelakte kasten met bovenplank, kledingstang en binnenbekleding.",
  "Drzwi wejściowe antywłamaniowe z zamkiem bezpieczeństwa, lakierowane drzwi wewnętrzne oraz modułowe lakierowane szafy z półką górną, drążkiem i wewnętrzną okładziną.",
  "En sikkerhetsinngangsdør med sikkerhetslås, lakkerte innerdører og modulære lakkerte garderobeskap med hylle, kleshenger og innvendig kledning.",
  "En säkerhetsentrédörr med säkerhetslås, lackerade innerdörrar och modulära lackerade garderober med hylla, klädstång och invändig beklädnad.")
a('A kitchen with large floor and wall units',
  "Una cocina con grandes muebles bajos y altos y encimera de Solid Surface.", "Une cuisine avec de grands meubles bas et hauts et un plan de travail en Solid Surface.",
  "Eine Küche mit großen Unter- und Oberschränken und einer Arbeitsplatte aus Solid Surface.", "Кухня с большими напольными и навесными шкафами и столешницей из Solid Surface.",
  "مطبخ بخزائن سفلية وعلوية كبيرة وسطح عمل من مادة Solid Surface.", "Een keuken met grote onder- en bovenkasten en een werkblad van Solid Surface.",
  "Kuchnia z dużymi szafkami dolnymi i górnymi oraz blatem z Solid Surface.", "Et kjøkken med store underskap og overskap og en benkeplate i Solid Surface.",
  "Ett kök med stora under- och överskåp och en bänkskiva av Solid Surface.")
a('Appliances included: an oven, a microwave',
  "Electrodomésticos incluidos: horno, microondas, placa de inducción, lavadora, lavavajillas y frigorífico.",
  "Électroménager inclus : four, micro-ondes, plaque à induction, lave-linge, lave-vaisselle et réfrigérateur.",
  "Geräte inklusive: Backofen, Mikrowelle, Induktionskochfeld, Waschmaschine, Geschirrspüler und Kühlschrank.",
  "Бытовая техника включена: духовой шкаф, микроволновая печь, индукционная варочная панель, стиральная машина, посудомоечная машина и холодильник.",
  "الأجهزة مشمولة: فرن وميكروويف وموقد حثّي وغسالة وغسالة صحون وثلاجة.",
  "Inbegrepen apparatuur: oven, magnetron, inductiekookplaat, wasmachine, vaatwasser en koelkast.",
  "W cenie sprzęt: piekarnik, kuchenka mikrofalowa, płyta indukcyjna, pralka, zmywarka i lodówka.",
  "Hvitevarer inkludert: stekeovn, mikrobølgeovn, induksjonstopp, vaskemaskin, oppvaskmaskin og kjøleskap.",
  "Vitvaror ingår: ugn, mikrovågsugn, induktionshäll, tvättmaskin, diskmaskin och kylskåp.")
a('The main bathroom is tiled from floor to ceiling',
  "El baño principal está alicatado del suelo al techo, con lavabo doble de Solid Surface, espejo con luz trasera, inodoro suspendido y plato de ducha de Solid Surface.",
  "La salle de bains principale est carrelée du sol au plafond, avec double vasque en Solid Surface, miroir rétroéclairé, WC suspendu et receveur de douche en Solid Surface.",
  "Das Hauptbad ist vom Boden bis zur Decke gefliest, mit Doppelwaschtisch aus Solid Surface, hinterleuchtetem Spiegel, wandhängendem WC und Duschtasse aus Solid Surface.",
  "Главная ванная комната облицована плиткой от пола до потолка: двойная раковина из Solid Surface, зеркало с подсветкой, подвесной унитаз и душевой поддон из Solid Surface.",
  "الحمّام الرئيسي مكسوّ بالبلاط من الأرض إلى السقف، مع مغسلة مزدوجة من Solid Surface ومرآة بإضاءة خلفية ومرحاض معلّق وقاعدة دش من Solid Surface.",
  "De hoofdbadkamer is van vloer tot plafond betegeld, met een dubbele wastafel van Solid Surface, een achtergrondverlichte spiegel, een hangend toilet en een douchebak van Solid Surface.",
  "Główna łazienka jest wyłożona płytkami od podłogi do sufitu, z podwójną umywalką z Solid Surface, podświetlanym lustrem, podwieszaną toaletą i brodzikiem z Solid Surface.",
  "Hovedbadet er flislagt fra gulv til tak, med dobbel servant i Solid Surface, bakgrunnsbelyst speil, hengende toalett og dusjkar i Solid Surface.",
  "Huvudbadrummet är kaklat från golv till tak, med dubbel handfat i Solid Surface, bakgrundsbelyst spegel, vägghängd toalett och duschbrunn i Solid Surface.")
a('Glass shower screens in every bathroom',
  "Mamparas de cristal en las duchas de todos los baños y grifería termostática de pared en las duchas.",
  "Parois de douche en verre dans toutes les salles de bains et robinetterie thermostatique murale dans les douches.",
  "Glas-Duschwände in allen Bädern und wandmontierte Thermostatarmaturen in den Duschen.",
  "Стеклянные душевые перегородки во всех ванных комнатах и настенные термостатические смесители в душах.",
  "حواجز دش زجاجية في جميع الحمّامات وخلاطات دش حرارية مثبّتة على الجدار.",
  "Glazen douchewanden in alle badkamers en wandmontage thermostaatkranen in de douches.",
  "Szklane ścianki prysznicowe we wszystkich łazienkach i ścienne baterie termostatyczne w prysznicach.",
  "Dusjvegger i glass i alle bad og veggmonterte termostatblandebatterier i dusjene.",
  "Duschväggar i glas i alla badrum och väggmonterade termostatblandare i duscharna.")
a('An aerothermal system for hot water and underfloor heating',
  "Un sistema de aerotermia para el agua caliente y el suelo radiante, y aire acondicionado con bomba de calor, conductos y control por zonas.",
  "Un système aérothermique pour l’eau chaude et le chauffage au sol, et une climatisation avec pompe à chaleur, gaines et régulation par zones.",
  "Ein Luft-Wasser-Wärmepumpensystem für Warmwasser und Fußbodenheizung sowie eine Klimaanlage mit Wärmepumpe, Luftkanälen und zonenweiser Regelung.",
  "Аэротермическая система для горячей воды и тёплого пола, а также кондиционирование с тепловым насосом, воздуховодами и зональным управлением.",
  "نظام هوائي حراري للماء الساخن والتدفئة الأرضية، وتكييف هواء بمضخة حرارية وقنوات وتحكّم بالمناطق.",
  "Een aerothermisch systeem voor warm water en vloerverwarming, en airconditioning met warmtepomp, kanalen en zoneregeling.",
  "System aerotermiczny do ciepłej wody i ogrzewania podłogowego oraz klimatyzacja z pompą ciepła, kanałami i sterowaniem strefowym.",
  "Et aerotermisk system for varmtvann og gulvvarme, og klimaanlegg med varmepumpe, kanaler og sonestyring.",
  "Ett aerotermiskt system för varmvatten och golvvärme, och luftkonditionering med värmepump, kanaler och zonstyrning.")
a('The developer estimates an energy rating of B',
  "El promotor estima una calificación energética B; la certificación está en trámite.", "Le promoteur estime une classe énergétique B ; la certification est en cours.",
  "Der Bauträger rechnet mit der Energieklasse B; die Zertifizierung läuft.", "Застройщик оценивает класс энергоэффективности как B; сертификация ещё не завершена.",
  "يقدّر المطوّر تصنيف الطاقة بالفئة B، والشهادة قيد الإصدار.", "De ontwikkelaar schat het energielabel op B; de certificering loopt.",
  "Deweloper szacuje klasę energetyczną B; certyfikacja jest w toku.", "Utbyggeren anslår energimerke B; sertifiseringen pågår.",
  "Exploatören uppskattar energiklass B; certifieringen pågår.")
a('Electrical and home automation', "Electricidad y domótica", "Électricité et domotique", "Elektrik und Hausautomation", "Электрика и автоматизация", "الكهرباء وأتمتة المنزل", "Elektra en domotica", "Elektryka i automatyka domowa", "Elektrisk og smarthus", "El och hemautomation")
a('Anthracite switches, LED lights on the terraces',
  "Interruptores antracita, luces LED en las terrazas y videoportero.", "Interrupteurs anthracite, éclairage LED sur les terrasses et visiophone.",
  "Anthrazitfarbene Schalter, LED-Beleuchtung auf den Terrassen und eine Video-Gegensprechanlage.", "Выключатели цвета антрацит, светодиодное освещение террас и видеодомофон.",
  "مفاتيح بلون الأنثراسايت وإضاءة LED على التراسات وهاتف مرئي للمدخل.", "Antracietkleurige schakelaars, ledverlichting op de terrassen en een videofoon.",
  "Włączniki w kolorze antracytu, oświetlenie LED na tarasach i wideodomofon.", "Antrasittgrå brytere, LED-lys på terrassene og videodørtelefon.",
  "Antracitgrå strömbrytare, LED-belysning på terrasserna och en videodörrtelefon.")
a('Home automation for the blinds, fire detection',
  "Domótica para las persianas, la detección de incendios y la iluminación del salón, con control desde el móvil o con un asistente de voz.",
  "Domotique pour les stores, la détection d’incendie et l’éclairage du séjour, pilotable depuis un téléphone ou un assistant vocal.",
  "Hausautomation für die Jalousien, die Branderkennung und die Wohnzimmerbeleuchtung, steuerbar per Smartphone oder Sprachassistent.",
  "Автоматизация жалюзи, пожарной сигнализации и освещения гостиной с управлением со смартфона или голосовым помощником.",
  "أتمتة للستائر والكشف عن الحريق وإضاءة غرفة المعيشة، يمكن التحكم بها من الهاتف أو بمساعد صوتي.",
  "Domotica voor de zonwering, de branddetectie en de verlichting van de woonkamer, te bedienen via een telefoon of een spraakassistent.",
  "Automatyka domowa do rolet, wykrywania pożaru i oświetlenia salonu, sterowana z telefonu lub asystentem głosowym.",
  "Smarthusstyring av persienner, brannvarsling og stuebelysning, styrt fra telefon eller med en stemmeassistent.",
  "Hemautomation för persienner, brandvarning och belysning i vardagsrummet, styrd från en telefon eller med en röstassistent.")
a('Community', "Zonas comunes", "Parties communes", "Gemeinschaftsbereiche", "Общие зоны", "المرافق المشتركة", "Gemeenschappelijke delen", "Części wspólne", "Fellesområder", "Gemensamma ytor")
a('A community pool, large garden areas, and a gym',
  "Una piscina comunitaria, amplias zonas ajardinadas y un gimnasio con terraza exterior y una sala para actividades programadas.",
  "Une piscine commune, de vastes espaces verts et une salle de sport avec terrasse extérieure et une salle pour des activités programmées.",
  "Ein Gemeinschaftspool, große Gartenflächen und ein Fitnessraum mit Außenterrasse sowie ein Raum für geplante Aktivitäten.",
  "Общий бассейн, большие садовые зоны, тренажёрный зал с внешней террасой и зал для занятий по расписанию.",
  "مسبح مشترك ومساحات حدائق واسعة وصالة رياضية بتراس خارجي وقاعة للأنشطة المجدولة.",
  "Een gemeenschappelijk zwembad, grote tuingedeelten en een gym met buitenterras en een zaal voor geplande activiteiten.",
  "Basen wspólny, duże tereny zielone oraz siłownia z tarasem zewnętrznym i sala do zajęć według harmonogramu.",
  "Et felles basseng, store hageområder og et treningsrom med utendørs terrasse og et rom for planlagte aktiviteter.",
  "En gemensam pool, stora trädgårdsytor och ett gym med utomhusterrass samt ett rum för schemalagda aktiviteter.")
a('A community garage with an automated door, and storage rooms',
  "Un garaje comunitario con puerta automática y trasteros.", "Un garage commun avec porte automatique et des caves.", "Eine Gemeinschaftsgarage mit automatischem Tor und Abstellräume.",
  "Общий гараж с автоматическими воротами и кладовые.", "مرآب مشترك بباب آلي وغرف تخزين.", "Een gemeenschappelijke garage met automatische deur, en bergingen.",
  "Garaż wspólny z automatyczną bramą oraz komórki lokatorskie.", "Et felles garasjeanlegg med automatisk port, og boder.", "Ett gemensamt garage med automatisk port, och förråd.")

# ---------------------------------------------------------------- residences
a('The homes fall into three groups. The table below',
  "Las viviendas se dividen en tres grupos. La tabla de abajo las enumera todas con sus precios.", "Les logements se répartissent en trois groupes. Le tableau ci-dessous les énumère tous avec leurs prix.",
  "Die Wohnungen gliedern sich in drei Gruppen. Die Tabelle unten führt alle mit ihren Preisen auf.", "Квартиры делятся на три группы. В таблице ниже перечислены все они с ценами.",
  "تنقسم المساكن إلى ثلاث مجموعات. ويسردها الجدول أدناه جميعًا مع أسعارها.", "De woningen vallen in drie groepen. De tabel hieronder somt ze allemaal op met hun prijzen.",
  "Lokale dzielą się na trzy grupy. Poniższa tabela wymienia wszystkie z cenami.", "Boligene faller i tre grupper. Tabellen under viser alle med priser.",
  "Bostäderna delas in i tre grupper. Tabellen nedan listar alla med priser.")
a('Two-bedroom apartments', "Apartamentos de dos dormitorios", "Appartements de deux chambres", "Wohnungen mit zwei Schlafzimmern", "Квартиры с двумя спальнями", "شقق بغرفتي نوم", "Appartementen met twee slaapkamers", "Apartamenty z dwiema sypialniami", "Leiligheter med to soverom", "Lägenheter med två sovrum")
a('10 homes with two bedrooms and two bathrooms',
  "10 viviendas de dos dormitorios y dos baños, de 82.40 a 115.25 {U} construidos según la lista de precios y de 70.90 a 83.60 {U} interiores según los planos de nueve de ellas; la vivienda 150B no tiene plano.",
  "10 logements de deux chambres et deux salles de bains, de 82.40 à 115.25 {U} construits selon la liste de prix et de 70.90 à 83.60 {U} intérieurs selon les plans de neuf d’entre eux ; le logement 150B n’a pas de plan.",
  "10 Wohnungen mit zwei Schlafzimmern und zwei Bädern, von 82.40 bis 115.25 {U} bebaut laut Preisliste und von 70.90 bis 83.60 {U} Innenfläche laut den Grundrissen von neun davon; für Wohnung 150B liegt kein Grundriss vor.",
  "10 квартир с двумя спальнями и двумя ванными комнатами: от 82.40 до 115.25 {U} застроенной площади по прайс-листу и от 70.90 до 83.60 {U} внутренней площади по планировкам девяти из них; для квартиры 150B планировки нет.",
  "10 مساكن بغرفتي نوم وحمّامين، من 82.40 إلى 115.25 {U} مبنية بحسب قائمة الأسعار ومن 70.90 إلى 83.60 {U} داخلية بحسب مخططات تسعة منها؛ والمسكن 150B بلا مخطط.",
  "10 woningen met twee slaapkamers en twee badkamers, van 82.40 tot 115.25 {U} bebouwd volgens de prijslijst en van 70.90 tot 83.60 {U} binnen volgens de plattegronden van negen ervan; voor woning 150B is er geen plattegrond.",
  "10 lokali z dwiema sypialniami i dwiema łazienkami, od 82.40 do 115.25 {U} zabudowy według cennika i od 70.90 do 83.60 {U} wnętrza według rzutów dziewięciu z nich; lokal 150B nie ma rzutu.",
  "10 boliger med to soverom og to bad, fra 82.40 til 115.25 {U} bygd ifølge prislisten og fra 70.90 til 83.60 {U} innvendig ifølge plantegningene til ni av dem; bolig 150B har ingen plantegning.",
  "10 bostäder med två sovrum och två badrum, från 82.40 till 115.25 {U} byggyta enligt prislistan och från 70.90 till 83.60 {U} inomhus enligt planritningarna för nio av dem; bostad 150B saknar planritning.")
a('Terraces of 24.10 to 100.40 sqm, and private gardens',
  "Terrazas de 24.10 a 100.40 {U}, y jardines privados de 63.40, 42.20 y 46.00 {U} en las viviendas 410A, 410B y 420A.",
  "Des terrasses de 24.10 à 100.40 {U}, et des jardins privés de 63.40, 42.20 et 46.00 {U} pour les logements 410A, 410B et 420A.",
  "Terrassen von 24.10 bis 100.40 {U} und private Gärten von 63.40, 42.20 und 46.00 {U} bei den Wohnungen 410A, 410B und 420A.",
  "Террасы от 24.10 до 100.40 {U} и частные сады площадью 63.40, 42.20 и 46.00 {U} у квартир 410A, 410B и 420A.",
  "تراسات من 24.10 إلى 100.40 {U}، وحدائق خاصة بمساحة 63.40 و42.20 و46.00 {U} للمساكن 410A و410B و420A.",
  "Terrassen van 24.10 tot 100.40 {U}, en privétuinen van 63.40, 42.20 en 46.00 {U} bij de woningen 410A, 410B en 420A.",
  "Tarasy od 24.10 do 100.40 {U} oraz prywatne ogrody o powierzchni 63.40, 42.20 i 46.00 {U} przy lokalach 410A, 410B i 420A.",
  "Terrasser fra 24.10 til 100.40 {U}, og private hager på 63.40, 42.20 og 46.00 {U} for boligene 410A, 410B og 420A.",
  "Terrasser från 24.10 till 100.40 {U}, och privata trädgårdar på 63.40, 42.20 och 46.00 {U} för bostäderna 410A, 410B och 420A.")
a('Prices run from EUR 458,000 to EUR 636,000',
  "Los precios van de {E458000} a {E636000}.", "Les prix vont de {E458000} à {E636000}.", "Die Preise reichen von {E458000} bis {E636000}.", "Цены — от {E458000} до {E636000}.",
  "تتراوح الأسعار من {E458000} إلى {E636000}.", "De prijzen lopen van {E458000} tot {E636000}.", "Ceny wahają się od {E458000} do {E636000}.", "Prisene går fra {E458000} til {E636000}.", "Priserna går från {E458000} till {E636000}.")
a('Three-bedroom apartments', "Apartamentos de tres dormitorios", "Appartements de trois chambres", "Wohnungen mit drei Schlafzimmern", "Квартиры с тремя спальнями", "شقق بثلاث غرف نوم", "Appartementen met drie slaapkamers", "Apartamenty z trzema sypialniami", "Leiligheter med tre soverom", "Lägenheter med tre sovrum")
a('3 homes with three bedrooms and two bathrooms: 412B',
  "3 viviendas de tres dormitorios y dos baños: 412B, 162A y 163B, con 101.70, 154.23 y 157.25 {U} construidos y 88.30, 99.30 y 93.80 {U} interiores.",
  "3 logements de trois chambres et deux salles de bains : 412B, 162A et 163B, de 101.70, 154.23 et 157.25 {U} construits et 88.30, 99.30 et 93.80 {U} intérieurs.",
  "3 Wohnungen mit drei Schlafzimmern und zwei Bädern: 412B, 162A und 163B, mit 101.70, 154.23 und 157.25 {U} bebaut und 88.30, 99.30 und 93.80 {U} Innenfläche.",
  "3 квартиры с тремя спальнями и двумя ванными комнатами: 412B, 162A и 163B, с застроенной площадью 101.70, 154.23 и 157.25 {U} и внутренней 88.30, 99.30 и 93.80 {U}.",
  "3 مساكن بثلاث غرف نوم وحمّامين: 412B و162A و163B، بمساحات مبنية 101.70 و154.23 و157.25 {U} ومساحات داخلية 88.30 و99.30 و93.80 {U}.",
  "3 woningen met drie slaapkamers en twee badkamers: 412B, 162A en 163B, met 101.70, 154.23 en 157.25 {U} bebouwd en 88.30, 99.30 en 93.80 {U} binnen.",
  "3 lokale z trzema sypialniami i dwiema łazienkami: 412B, 162A i 163B, o powierzchni zabudowy 101.70, 154.23 i 157.25 {U} oraz wnętrza 88.30, 99.30 i 93.80 {U}.",
  "3 boliger med tre soverom og to bad: 412B, 162A og 163B, med 101.70, 154.23 og 157.25 {U} bygd og 88.30, 99.30 og 93.80 {U} innvendig.",
  "3 bostäder med tre sovrum och två badrum: 412B, 162A och 163B, med 101.70, 154.23 och 157.25 {U} byggyta och 88.30, 99.30 och 93.80 {U} inomhus.")
a('Terraces of 114.70, 100.70 and 50.70 sqm',
  "Terrazas de 114.70, 100.70 y 50.70 {U}.", "Des terrasses de 114.70, 100.70 et 50.70 {U}.", "Terrassen von 114.70, 100.70 und 50.70 {U}.", "Террасы площадью 114.70, 100.70 и 50.70 {U}.",
  "تراسات بمساحة 114.70 و100.70 و50.70 {U}.", "Terrassen van 114.70, 100.70 en 50.70 {U}.", "Tarasy o powierzchni 114.70, 100.70 i 50.70 {U}.", "Terrasser på 114.70, 100.70 og 50.70 {U}.", "Terrasser på 114.70, 100.70 och 50.70 {U}.")
a('Prices run from EUR 721,000 to EUR 829,000',
  "Los precios van de {E721000} a {E829000}.", "Les prix vont de {E721000} à {E829000}.", "Die Preise reichen von {E721000} bis {E829000}.", "Цены — от {E721000} до {E829000}.",
  "تتراوح الأسعار من {E721000} إلى {E829000}.", "De prijzen lopen van {E721000} tot {E829000}.", "Ceny wahają się od {E721000} do {E829000}.", "Prisene går fra {E721000} til {E829000}.", "Priserna går från {E721000} till {E829000}.")
a('Penthouses', "Áticos", "Penthouses", "Penthouses", "Пентхаусы", "بنتهاوس", "Penthouses", "Penthouse’y", "Toppleiligheter", "Takvåningar")
a('5 penthouses with three bedrooms',
  "5 áticos de tres dormitorios, de 117.00 a 197.25 {U} construidos y de 92.40 a 117.60 {U} interiores. Los planos de 154B, 164B, 414B y 424B muestran dos niveles; el plano de 434A muestra uno.",
  "5 penthouses de trois chambres, de 117.00 à 197.25 {U} construits et de 92.40 à 117.60 {U} intérieurs. Les plans de 154B, 164B, 414B et 424B montrent deux niveaux ; celui de 434A en montre un.",
  "5 Penthouses mit drei Schlafzimmern, von 117.00 bis 197.25 {U} bebaut und von 92.40 bis 117.60 {U} Innenfläche. Die Grundrisse von 154B, 164B, 414B und 424B zeigen zwei Ebenen; der von 434A zeigt eine.",
  "5 пентхаусов с тремя спальнями: от 117.00 до 197.25 {U} застроенной площади и от 92.40 до 117.60 {U} внутренней. На планировках 154B, 164B, 414B и 424B два уровня, на планировке 434A — один.",
  "5 بنتهاوس بثلاث غرف نوم، من 117.00 إلى 197.25 {U} مبنية ومن 92.40 إلى 117.60 {U} داخلية. تُظهر مخططات 154B و164B و414B و424B مستويين، ويُظهر مخطط 434A مستوى واحدًا.",
  "5 penthouses met drie slaapkamers, van 117.00 tot 197.25 {U} bebouwd en van 92.40 tot 117.60 {U} binnen. De plattegronden van 154B, 164B, 414B en 424B tonen twee niveaus; die van 434A toont er één.",
  "5 penthouse’ów z trzema sypialniami, od 117.00 do 197.25 {U} zabudowy i od 92.40 do 117.60 {U} wnętrza. Rzuty 154B, 164B, 414B i 424B pokazują dwa poziomy, rzut 434A — jeden.",
  "5 toppleiligheter med tre soverom, fra 117.00 til 197.25 {U} bygd og fra 92.40 til 117.60 {U} innvendig. Plantegningene til 154B, 164B, 414B og 424B viser to plan, plantegningen til 434A viser ett.",
  "5 takvåningar med tre sovrum, från 117.00 till 197.25 {U} byggyta och från 92.40 till 117.60 {U} inomhus. Planritningarna för 154B, 164B, 414B och 424B visar två plan, den för 434A visar ett.")
a('Terraces of 33.00 to 121.90 sqm',
  "Terrazas de 33.00 a 121.90 {U}.", "Des terrasses de 33.00 à 121.90 {U}.", "Terrassen von 33.00 bis 121.90 {U}.", "Террасы от 33.00 до 121.90 {U}.", "تراسات من 33.00 إلى 121.90 {U}.", "Terrassen van 33.00 tot 121.90 {U}.", "Tarasy od 33.00 do 121.90 {U}.", "Terrasser fra 33.00 til 121.90 {U}.", "Terrasser från 33.00 till 121.90 {U}.")
a('Prices run from EUR 861,000 to EUR 1,065,000',
  "Los precios van de {E861000} a {E1065000}.", "Les prix vont de {E861000} à {E1065000}.", "Die Preise reichen von {E861000} bis {E1065000}.", "Цены — от {E861000} до {E1065000}.",
  "تتراوح الأسعار من {E861000} إلى {E1065000}.", "De prijzen lopen van {E861000} tot {E1065000}.", "Ceny wahają się od {E861000} do {E1065000}.", "Prisene går fra {E861000} til {E1065000}.", "Priserna går från {E861000} till {E1065000}.")

# ---------------------------------------------------------------- lifestyle, location
a('Terraces, <em>pools</em> and the sea in view',
  "Terrazas, <em>piscinas</em> y el mar a la vista", "Des terrasses, <em>des piscines</em> et la mer en vue", "Terrassen, <em>Pools</em> und das Meer im Blick",
  "Террасы, <em>бассейны</em> и море перед глазами", "تراسات <em>ومسابح</em> والبحر في الأفق", "Terrassen, <em>zwembaden</em> en de zee in zicht",
  "Tarasy, <em>baseny</em> i morze na horyzoncie", "Terrasser, <em>basseng</em> og havet i sikte", "Terrasser, <em>pooler</em> och havet i sikte")
a('Life here is outdoors and in the community',
  "La vida aquí transcurre al aire libre y en la comunidad, con el mar delante de las terrazas.", "La vie ici se passe en plein air et dans la résidence, avec la mer devant les terrasses.",
  "Das Leben hier spielt sich draußen und in der Anlage ab, mit dem Meer vor den Terrassen.", "Жизнь здесь проходит на открытом воздухе и в самом комплексе, а перед террасами — море.",
  "الحياة هنا في الهواء الطلق وفي المجمّع، والبحر أمام التراسات.", "Het leven hier speelt zich buiten en in de gemeenschap af, met de zee voor de terrassen.",
  "Życie toczy się tu na świeżym powietrzu i we wspólnocie, a przed tarasami rozciąga się morze.", "Livet her foregår ute og i fellesområdet, med havet foran terrassene.",
  "Livet här utspelar sig utomhus och i området, med havet framför terrasserna.")
a('Large terraces that continue the living room',
  "Grandes terrazas que prolongan el salón, con vistas al mar.", "De grandes terrasses qui prolongent le séjour, avec vue sur la mer.", "Große Terrassen, die das Wohnzimmer fortsetzen, mit Meerblick.",
  "Большие террасы, продолжающие гостиную, с видом на море.", "تراسات واسعة تمتد من غرفة المعيشة بإطلالات على البحر.", "Grote terrassen die de woonkamer verlengen, met zeezicht.",
  "Duże tarasy będące przedłużeniem salonu, z widokiem na morze.", "Store terrasser som forlenger stuen, med utsikt mot havet.", "Stora terrasser som förlänger vardagsrummet, med havsutsikt.")
a('An outdoor pool and a heated indoor pool',
  "Una piscina exterior y una piscina interior climatizada, con bar de piscina.", "Une piscine extérieure et une piscine intérieure chauffée, avec un bar de piscine.",
  "Ein Außenpool und ein beheizter Innenpool, mit Poolbar.", "Наружный бассейн и подогреваемый внутренний бассейн, а также бар у бассейна.",
  "مسبح خارجي ومسبح داخلي مدفأ، مع بار للمسبح.", "Een buitenzwembad en een verwarmd binnenzwembad, met een poolbar.",
  "Basen zewnętrzny i podgrzewany basen wewnętrzny oraz bar przy basenie.", "Et utendørs basseng og et oppvarmet innendørs basseng, med en bassengbar.",
  "En utomhuspool och en uppvärmd inomhuspool, med en poolbar.")
a('A spa, and a gym with an outdoor terrace',
  "Un spa y un gimnasio con terraza exterior y una sala para actividades programadas.", "Un spa et une salle de sport avec terrasse extérieure et une salle pour des activités programmées.",
  "Ein Spa und ein Fitnessraum mit Außenterrasse sowie ein Raum für geplante Aktivitäten.", "Спа и тренажёрный зал с внешней террасой, а также зал для занятий по расписанию.",
  "سبا وصالة رياضية بتراس خارجي وقاعة للأنشطة المجدولة.", "Een spa en een gym met buitenterras en een zaal voor geplande activiteiten.",
  "Spa i siłownia z tarasem zewnętrznym oraz sala do zajęć według harmonogramu.", "Et spa og et treningsrom med utendørs terrasse og et rom for planlagte aktiviteter.",
  "Ett spa och ett gym med utomhusterrass samt ett rum för schemalagda aktiviteter.")
a('A coworking area in the community',
  "Una zona de coworking en la comunidad, para que trabajar no obligue a salir de la promoción.", "Un espace de coworking dans la résidence, pour que travailler n’oblige pas à en sortir.",
  "Ein Coworking-Bereich in der Anlage, damit man zum Arbeiten die Anlage nicht verlassen muss.", "Коворкинг в самом комплексе: чтобы работать, не нужно выезжать за его пределы.",
  "مساحة للعمل المشترك داخل المجمّع، فلا يتطلب العمل مغادرته.", "Een coworkingruimte in de gemeenschap, zodat werken niet betekent dat u het complex moet verlaten.",
  "Strefa coworkingu we wspólnocie, aby praca nie wymagała opuszczania osiedla.", "Et coworking-område i fellesområdet, slik at arbeid ikke betyr å forlate anlegget.",
  "En coworkingyta i området, så att arbete inte innebär att lämna området.")
a('The development is in the upper part of Los Monteros, about 10 minutes from the centre of Marbella and its old town. The developer',
  "La promoción está en la parte alta de Los Monteros, a unos 10 minutos del centro de Marbella y de su casco antiguo. La página del promotor sitúa la playa, el campo de golf de Río Real y el centro comercial La Cañada a unos cinco minutos; su folleto da 8 km hasta Río Real Golf y 7 km hasta La Cañada.",
  "Le programme se trouve dans la partie haute de Los Monteros, à environ 10 minutes du centre de Marbella et de sa vieille ville. La page du promoteur place la plage, le golf de Río Real et le centre commercial La Cañada à environ cinq minutes ; sa brochure indique 8 km jusqu’au Río Real Golf et 7 km jusqu’à La Cañada.",
  "Die Anlage liegt im oberen Teil von Los Monteros, etwa 10 Minuten vom Zentrum von Marbella und seiner Altstadt entfernt. Die Seite des Bauträgers nennt Strand, Golfplatz Río Real und Einkaufszentrum La Cañada in etwa fünf Minuten Entfernung; seine Broschüre gibt 8 km bis Río Real Golf und 7 km bis La Cañada an.",
  "Комплекс находится в верхней части Лос-Монтероса, примерно в 10 минутах от центра Марбельи и её старого города. На странице застройщика пляж, гольф-поле Рио-Реал и торговый центр La Cañada указаны в пяти минутах; в его брошюре — 8 км до гольф-клуба Rio Real и 7 км до La Cañada.",
  "يقع المجمّع في الجزء العلوي من لوس مونتيروس، على بعد نحو 10 دقائق من وسط مربيّا وبلدتها القديمة. وتضع صفحة المطوّر الشاطئ وملعب الغولف ريو ريال ومركز لا كانيادا التجاري على بعد نحو خمس دقائق؛ أما كتيّبه فيذكر 8 كم إلى ملعب ريو ريال و7 كم إلى لا كانيادا.",
  "Het complex ligt in het hoger gelegen deel van Los Monteros, op ongeveer 10 minuten van het centrum van Marbella en de oude stad. De pagina van de ontwikkelaar plaatst het strand, de golfbaan Río Real en het winkelcentrum La Cañada op ongeveer vijf minuten; zijn brochure geeft 8 km tot Río Real Golf en 7 km tot La Cañada.",
  "Osiedle leży w górnej części Los Monteros, około 10 minut od centrum Marbelli i jej starego miasta. Strona dewelopera podaje plażę, pole golfowe Río Real i centrum handlowe La Cañada w odległości około pięciu minut; jego broszura podaje 8 km do Río Real Golf i 7 km do La Cañada.",
  "Anlegget ligger i den øvre delen av Los Monteros, omtrent 10 minutter fra sentrum av Marbella og gamlebyen. Utbyggerens side plasserer stranden, golfbanen Río Real og kjøpesenteret La Cañada omtrent fem minutter unna; brosjyren oppgir 8 km til Río Real Golf og 7 km til La Cañada.",
  "Området ligger i övre delen av Los Monteros, cirka 10 minuter från Marbellas centrum och gamla stad. Exploatörens sida placerar stranden, golfbanan Río Real och köpcentrumet La Cañada cirka fem minuter bort; dess broschyr anger 8 km till Río Real Golf och 7 km till La Cañada.")
a('marbellaEast', *(['marbellaEast'] * 9))
a('6 km', *(['6 {KM}'] * 9))
a('16 km', *(['16 {KM}'] * 9))
a('52 km', *(['52 {KM}'] * 9))

# ---------------------------------------------------------------- investment, trust
a('The documents we hold do not set out the developer’s terms',
  "Los documentos de que disponemos no recogen las condiciones del promotor, así que las confirmamos por escrito antes de que usted reserve.",
  "Les documents dont nous disposons n’exposent pas les conditions du promoteur ; nous les confirmons donc par écrit avant votre réservation.",
  "Die uns vorliegenden Unterlagen enthalten die Bedingungen des Bauträgers nicht, deshalb bestätigen wir sie schriftlich, bevor Sie reservieren.",
  "В имеющихся у нас документах условия застройщика не изложены, поэтому мы подтверждаем их письменно до того, как вы забронируете.",
  "لا تتضمّن الوثائق التي لدينا شروط المطوّر، لذلك نؤكدها كتابيًا قبل أن تحجزوا.",
  "De documenten waarover wij beschikken bevatten de voorwaarden van de ontwikkelaar niet, dus wij bevestigen ze schriftelijk voordat u reserveert.",
  "Posiadane przez nas dokumenty nie zawierają warunków dewelopera, dlatego potwierdzamy je na piśmie, zanim Państwo dokonają rezerwacji.",
  "Dokumentene vi har, inneholder ikke utbyggerens vilkår, så vi bekrefter dem skriftlig før reservasjon.",
  "De dokument vi har anger inte exploatörens villkor, så vi bekräftar dem skriftligt innan ni reserverar.")
a('Reservation and payment schedule', "Reserva y calendario de pagos", "Réservation et échéancier de paiement", "Reservierung und Zahlungsplan", "Бронирование и график платежей", "الحجز وجدول الدفعات", "Reservering en betalingsschema", "Rezerwacja i harmonogram płatności", "Reservasjon og betalingsplan", "Reservation och betalningsplan")
a('The documents we hold give no reservation amount',
  "Los documentos de que disponemos no indican importe de reserva ni calendario de pagos. Obtenemos las condiciones del promotor y se las enviamos por escrito antes de que usted reserve.",
  "Les documents dont nous disposons ne donnent ni montant de réservation ni échéancier. Nous obtenons les conditions du promoteur et vous les envoyons par écrit avant votre réservation.",
  "Die uns vorliegenden Unterlagen nennen weder einen Reservierungsbetrag noch einen Zahlungsplan. Wir holen die Bedingungen des Bauträgers ein und senden sie Ihnen schriftlich, bevor Sie reservieren.",
  "В имеющихся у нас документах нет ни суммы бронирования, ни графика платежей. Мы получаем условия застройщика и направляем их вам письменно до бронирования.",
  "لا تذكر الوثائق التي لدينا مبلغ حجز ولا جدول دفعات. نحصل على شروط المطوّر ونرسلها إليكم كتابيًا قبل الحجز.",
  "De documenten waarover wij beschikken noemen geen reserveringsbedrag en geen betalingsschema. Wij vragen de voorwaarden van de ontwikkelaar op en sturen ze u schriftelijk toe voordat u reserveert.",
  "Posiadane przez nas dokumenty nie podają kwoty rezerwacji ani harmonogramu płatności. Uzyskujemy warunki dewelopera i przesyłamy je Państwu na piśmie przed rezerwacją.",
  "Dokumentene vi har, oppgir verken reservasjonsbeløp eller betalingsplan. Vi innhenter utbyggerens vilkår og sender dem skriftlig før reservasjon.",
  "De dokument vi har anger varken reservationsbelopp eller betalningsplan. Vi hämtar exploatörens villkor och skickar dem skriftligt till er innan ni reserverar.")
a('VAT and taxes', "IVA e impuestos", "TVA et taxes", "Mehrwertsteuer und Steuern", "НДС и налоги", "ضريبة القيمة المضافة والضرائب", "Btw en belastingen", "VAT i podatki", "Mva og skatter", "Moms och skatter")
a('The price list does not say whether VAT is included. Nueva Living confirms',
  "La lista de precios no indica si el IVA está incluido. Nueva Living confirma por escrito los impuestos y los gastos de la compra.",
  "La liste de prix n’indique pas si la TVA est incluse. Nueva Living confirme par écrit les taxes et les frais d’achat.",
  "Die Preisliste sagt nicht, ob die Mehrwertsteuer enthalten ist. Nueva Living bestätigt Steuern und Kaufnebenkosten schriftlich.",
  "В прайс-листе не сказано, включён ли НДС. Nueva Living письменно подтверждает налоги и расходы на покупку.",
  "لا تذكر قائمة الأسعار ما إذا كانت ضريبة القيمة المضافة مشمولة. تؤكد Nueva Living الضرائب وتكاليف الشراء كتابيًا.",
  "De prijslijst zegt niet of de btw erin zit. Nueva Living bevestigt de belastingen en de aankoopkosten schriftelijk.",
  "Cennik nie mówi, czy cena zawiera VAT. Nueva Living potwierdza podatki i koszty zakupu na piśmie.",
  "Prislisten sier ikke om mva er inkludert. Nueva Living bekrefter skatter og kjøpskostnader skriftlig.",
  "Prislistan anger inte om momsen ingår. Nueva Living bekräftar skatter och köpkostnader skriftligt.")
a('The specification describes a community garage with an automated door and storage rooms. It does not say',
  "La memoria de calidades describe un garaje comunitario con puerta automática y trasteros. No indica si una plaza o un trastero están incluidos en el precio, así que lo preguntamos para la vivienda que usted elija.",
  "La notice descriptive décrit un garage commun avec porte automatique et des caves. Elle n’indique pas si une place ou une cave est incluse dans le prix ; nous posons la question pour le logement que vous choisirez.",
  "Die Ausstattungsbeschreibung nennt eine Gemeinschaftsgarage mit automatischem Tor und Abstellräume. Sie sagt nicht, ob ein Stellplatz oder ein Abstellraum im Preis enthalten ist, deshalb fragen wir für die Wohnung nach, die Sie wählen.",
  "В описании качества упомянуты общий гараж с автоматическими воротами и кладовые. Не сказано, входят ли парковочное место или кладовая в цену, поэтому мы уточняем это для выбранной вами квартиры.",
  "تصف مواصفات الجودة مرآبًا مشتركًا بباب آلي وغرف تخزين. ولا تذكر ما إذا كان موقف أو غرفة تخزين مشمولين في السعر، لذلك نستفسر عنه للمسكن الذي تختارونه.",
  "De kwaliteitsomschrijving beschrijft een gemeenschappelijke garage met automatische deur en bergingen. Zij zegt niet of een parkeerplaats of berging in de prijs zit, dus wij vragen het na voor de woning die u kiest.",
  "Opis jakości wspomina o garażu wspólnym z automatyczną bramą i komórkach lokatorskich. Nie mówi, czy miejsce postojowe lub komórka są wliczone w cenę, dlatego pytamy o to dla wybranego przez Państwa lokalu.",
  "Kvalitetsbeskrivelsen beskriver et felles garasjeanlegg med automatisk port og boder. Den sier ikke om en plass eller en bod er inkludert i prisen, så vi spør om det for boligen som velges.",
  "Kvalitetsbeskrivningen beskriver ett gemensamt garage med automatisk port och förråd. Den anger inte om en plats eller ett förråd ingår i priset, så vi frågar om det för den bostad ni väljer.")
a('The quality specification says its materials may be replaced',
  "La memoria de calidades indica que sus materiales pueden sustituirse por otros de igual o superior calidad y que no es contractual. Pedimos la memoria definitiva.",
  "La notice descriptive indique que ses matériaux peuvent être remplacés par d’autres de qualité égale ou supérieure et qu’elle n’est pas contractuelle. Nous demandons la notice définitive.",
  "Die Ausstattungsbeschreibung besagt, dass ihre Materialien durch gleich- oder höherwertige ersetzt werden können und dass sie nicht vertraglich ist. Wir fordern die endgültige Beschreibung an.",
  "В описании качества сказано, что материалы могут быть заменены на равноценные или более качественные и что оно не является договорным. Мы запрашиваем окончательное описание.",
  "تذكر مواصفات الجودة أن موادها يجوز استبدالها بمواد مماثلة أو أعلى جودة وأنها غير تعاقدية. نطلب المواصفات النهائية.",
  "De kwaliteitsomschrijving zegt dat de materialen kunnen worden vervangen door gelijkwaardige of betere en dat zij niet contractueel is. Wij vragen de definitieve omschrijving op.",
  "Opis jakości mówi, że materiały mogą zostać zastąpione równorzędnymi lub lepszymi i że nie jest umowny. Prosimy o ostateczny opis.",
  "Kvalitetsbeskrivelsen sier at materialene kan byttes ut med likeverdige eller bedre, og at den ikke er kontraktsfestet. Vi ber om den endelige beskrivelsen.",
  "Kvalitetsbeskrivningen anger att materialen kan bytas ut mot likvärdiga eller bättre och att den inte är avtalsenlig. Vi ber om den slutliga beskrivningen.")
a('The documents we hold do not say whether the building licence',
  "Los documentos de que disponemos no indican si se ha concedido la licencia de obras ni si las obras han comenzado; los planos están elaborados conforme al proyecto básico. Pedimos la licencia, su estado y la fecha de inicio de las obras.",
  "Les documents dont nous disposons ne disent pas si le permis de construire a été délivré ni si les travaux ont commencé ; les plans sont établis d’après le projet de base. Nous demandons le permis, son état et la date de début des travaux.",
  "Die uns vorliegenden Unterlagen sagen nicht, ob die Baugenehmigung erteilt wurde oder ob die Bauarbeiten begonnen haben; die Grundrisse sind nach dem Basisprojekt gezeichnet. Wir fordern die Genehmigung, ihren Stand und den Baubeginn an.",
  "В имеющихся у нас документах не сказано, выдано ли разрешение на строительство и начались ли работы; планировки составлены по базовому проекту. Мы запрашиваем разрешение, его статус и дату начала работ.",
  "لا تذكر الوثائق التي لدينا ما إذا كانت رخصة البناء قد مُنحت أو ما إذا كانت الأعمال قد بدأت؛ والمخططات مرسومة وفق المشروع الأساسي. نطلب الرخصة وحالتها وتاريخ بدء الأعمال.",
  "De documenten waarover wij beschikken zeggen niet of de bouwvergunning is verleend of de werken zijn begonnen; de plattegronden zijn getekend naar het basisproject. Wij vragen de vergunning, de status ervan en de startdatum van de werken op.",
  "Posiadane przez nas dokumenty nie mówią, czy pozwolenie na budowę zostało wydane ani czy prace się rozpoczęły; rzuty sporządzono według projektu podstawowego. Prosimy o pozwolenie, jego status i datę rozpoczęcia prac.",
  "Dokumentene vi har, sier ikke om byggetillatelsen er gitt eller om arbeidene har startet; plantegningene er tegnet etter grunnprosjektet. Vi ber om tillatelsen, statusen og startdatoen for arbeidene.",
  "De dokument vi har säger inte om bygglovet har beviljats eller om arbetena har påbörjats; planritningarna är ritade efter grundprojektet. Vi ber om bygglovet, dess status och startdatum för arbetena.")
a('None of the developer’s documents gives a completion date, so',
  "Ningún documento del promotor indica una fecha de entrega, así que pedimos la fecha contractual antes de cualquier reserva.",
  "Aucun document du promoteur ne donne de date de livraison ; nous demandons donc la date contractuelle avant toute réservation.",
  "Keines der Dokumente des Bauträgers nennt einen Fertigstellungstermin, deshalb fordern wir vor jeder Reservierung den vertraglichen Termin an.",
  "Ни в одном из документов застройщика не указан срок сдачи, поэтому перед любым бронированием мы запрашиваем договорную дату.",
  "لا تذكر أي من وثائق المطوّر موعدًا للتسليم، لذلك نطلب الموعد التعاقدي قبل أي حجز.",
  "Geen van de documenten van de ontwikkelaar noemt een opleveringsdatum, dus wij vragen de contractuele datum op vóór elke reservering.",
  "Żaden z dokumentów dewelopera nie podaje terminu oddania, dlatego przed każdą rezerwacją prosimy o termin umowny.",
  "Ingen av utbyggerens dokumenter oppgir en overleveringsdato, så vi ber om den kontraktfestede datoen før enhver reservasjon.",
  "Inget av exploatörens dokument anger ett leveransdatum, så vi ber om det avtalade datumet före varje reservation.")
a('Which homes, which phase', "Qué viviendas, qué fase", "Quels logements, quelle phase", "Welche Wohnungen, welche Phase", "Какие квартиры, какая очередь", "أي المساكن وأي مرحلة", "Welke woningen, welke fase", "Które lokale, która faza", "Hvilke boliger, hvilken fase", "Vilka bostäder, vilken etapp")
a('The developer’s page presents the release as phase 4',
  "La página del promotor presenta esta comercialización como fase 4. Los planos de 12 de las 18 viviendas llevan el encabezado fase IV, en los bloques 1 a 3; las otras seis tienen referencias de los portales 15 y 16, sus planos no nombran ninguna fase y la vivienda 150B no tiene plano. El folleto describe 39 viviendas en tres bloques como la primera fase. Preguntamos al promotor cuántas viviendas tiene cada fase.",
  "La page du promoteur présente cette commercialisation comme la phase 4. Les plans de 12 des 18 logements portent la mention phase IV, dans les blocs 1 à 3 ; les six autres ont des références des cages 15 et 16, leurs plans ne nomment aucune phase et le logement 150B n’a pas de plan. La brochure décrit 39 logements répartis en trois blocs comme la première phase. Nous demandons au promoteur combien de logements compte chaque phase.",
  "Die Seite des Bauträgers präsentiert diese Vermarktung als Phase 4. Die Grundrisse von 12 der 18 Wohnungen tragen die Überschrift Phase IV, in den Blöcken 1 bis 3; die anderen sechs haben Referenzen der Aufgänge 15 und 16, ihre Grundrisse nennen keine Phase, und für Wohnung 150B gibt es keinen Grundriss. Die Broschüre beschreibt 39 Wohnungen in drei Blöcken als erste Phase. Wir fragen den Bauträger, wie viele Wohnungen jede Phase hat.",
  "На странице застройщика эта продажа названа очередью 4. Планировки 12 из 18 квартир подписаны «очередь IV» и относятся к блокам 1–3; у остальных шести номера подъездов 15 и 16, на их планировках очередь не указана, а для квартиры 150B планировки нет. В брошюре 39 квартир в трёх блоках названы первой очередью. Мы спрашиваем застройщика, сколько квартир в каждой очереди.",
  "تعرض صفحة المطوّر هذا الطرح بوصفه المرحلة 4. مخططات 12 مسكنًا من أصل 18 تحمل عنوان المرحلة IV في المباني من 1 إلى 3؛ أما المساكن الستة الأخرى فمراجعها من المدخلين 15 و16 ولا تذكر مخططاتها أي مرحلة، ولا مخطط للمسكن 150B. ويصف الكتيّب 39 مسكنًا في ثلاثة مبانٍ بأنها المرحلة الأولى. نسأل المطوّر كم مسكنًا تضم كل مرحلة.",
  "De pagina van de ontwikkelaar presenteert deze verkoop als fase 4. De plattegronden van 12 van de 18 woningen dragen de kop fase IV, in de blokken 1 tot 3; de andere zes hebben referenties van portieken 15 en 16, hun plattegronden noemen geen fase en voor woning 150B is er geen plattegrond. De brochure beschrijft 39 woningen in drie blokken als de eerste fase. Wij vragen de ontwikkelaar hoeveel woningen elke fase heeft.",
  "Strona dewelopera przedstawia tę sprzedaż jako fazę 4. Rzuty 12 z 18 lokali mają nagłówek faza IV, w blokach 1–3; pozostałe sześć ma numery z klatek 15 i 16, ich rzuty nie wskazują żadnej fazy, a lokal 150B nie ma rzutu. Broszura opisuje 39 lokali w trzech blokach jako pierwszą fazę. Pytamy dewelopera, ile lokali ma każda faza.",
  "Utbyggerens side presenterer dette salget som fase 4. Plantegningene til 12 av de 18 boligene har overskriften fase IV, i byggene 1 til 3; de seks andre har referanser fra oppgangene 15 og 16, plantegningene deres nevner ingen fase, og bolig 150B har ingen plantegning. Brosjyren beskriver 39 boliger i tre bygg som første fase. Vi spør utbyggeren hvor mange boliger hver fase har.",
  "Exploatörens sida presenterar denna försäljning som etapp 4. Planritningarna för 12 av de 18 bostäderna har rubriken etapp IV, i husen 1 till 3; de andra sex har referenser från uppgångarna 15 och 16, deras planritningar nämner ingen etapp och bostad 150B saknar planritning. Broschyren beskriver 39 bostäder i tre hus som första etappen. Vi frågar exploatören hur många bostäder varje etapp har.")
a('The price list gives one built area and one terrace figure for each home',
  "La lista de precios da una superficie construida y una cifra de terraza por vivienda, pero no sobre la misma base: en las viviendas de los bloques 1 a 3 es la superficie construida interior, y en las de los portales 15 y 16 incluye una parte de las zonas comunes. Los planos dan una cifra mayor con las zonas comunes, y superficies según el Decreto 218/2005. Confirmamos qué cifra usa el contrato.",
  "La liste de prix donne une surface construite et un chiffre de terrasse par logement, mais pas sur la même base : pour les logements des blocs 1 à 3, c’est la surface construite intérieure, et pour ceux des cages 15 et 16, elle inclut une quote-part des parties communes. Les plans donnent un chiffre plus élevé avec les parties communes, et des surfaces selon le décret 218/2005. Nous confirmons quel chiffre le contrat retient.",
  "Die Preisliste nennt je Wohnung eine bebaute Fläche und eine Terrassenangabe, aber nicht auf derselben Grundlage: Bei den Wohnungen der Blöcke 1 bis 3 ist es die bebaute Innenfläche, bei denen der Aufgänge 15 und 16 enthält sie einen Anteil der Gemeinschaftsflächen. Die Grundrisse nennen eine größere Zahl mit den Gemeinschaftsflächen sowie Flächen nach dem Dekret 218/2005. Wir bestätigen, welche Zahl der Vertrag verwendet.",
  "В прайс-листе для каждой квартиры указаны застроенная площадь и площадь террасы, но не на одной основе: для квартир блоков 1–3 это застроенная внутренняя площадь, а для квартир подъездов 15 и 16 она включает долю общих зон. На планировках приведена бо́льшая цифра с общими зонами, а также площади по декрету 218/2005. Мы уточняем, какую цифру использует договор.",
  "تعطي قائمة الأسعار مساحة مبنية ورقم تراس لكل مسكن، لكن ليس على الأساس نفسه: ففي مساكن المباني من 1 إلى 3 هي المساحة المبنية الداخلية، وفي مساكن المدخلين 15 و16 تشمل حصة من المناطق المشتركة. وتعطي المخططات رقمًا أكبر مع المناطق المشتركة، ومساحات وفق المرسوم 218/2005. نؤكد أي رقم يعتمده العقد.",
  "De prijslijst geeft per woning een bebouwde oppervlakte en een terrascijfer, maar niet op dezelfde grondslag: bij de woningen van de blokken 1 tot 3 is het de bebouwde binnenoppervlakte, bij die van de portieken 15 en 16 omvat het een aandeel in de gemeenschappelijke delen. De plattegronden geven een groter cijfer met de gemeenschappelijke delen, en oppervlaktes volgens decreet 218/2005. Wij bevestigen welk cijfer het contract hanteert.",
  "Cennik podaje dla każdego lokalu powierzchnię zabudowy i powierzchnię tarasu, ale nie na tej samej podstawie: dla lokali w blokach 1–3 jest to zabudowana powierzchnia wewnętrzna, a dla lokali w klatkach 15 i 16 zawiera ona udział w częściach wspólnych. Rzuty podają większą wartość z częściami wspólnymi oraz powierzchnie według dekretu 218/2005. Potwierdzamy, którą wartość przyjmuje umowa.",
  "Prislisten oppgir ett bygd areal og ett terrassetall for hver bolig, men ikke på samme grunnlag: for boligene i byggene 1 til 3 er det det bygde innvendige arealet, og for boligene i oppgangene 15 og 16 inkluderer det en andel av fellesarealene. Plantegningene oppgir et større tall med fellesarealene, og arealer etter dekret 218/2005. Vi bekrefter hvilket tall kontrakten bruker.",
  "Prislistan anger en byggyta och en terrassyta för varje bostad, men inte på samma grund: för bostäderna i husen 1 till 3 är det den invändiga byggytan, och för bostäderna i uppgångarna 15 och 16 ingår en andel av de gemensamma ytorna. Planritningarna anger ett större tal med de gemensamma ytorna, och ytor enligt dekret 218/2005. Vi bekräftar vilket tal avtalet använder.")

# ---------------------------------------------------------------- availability, timeline, viewing, enquiry, faq
a('Eighteen homes <em>currently listed</em>',
  "Dieciocho viviendas <em>a la venta ahora</em>", "Dix-huit logements <em>actuellement proposés</em>", "Achtzehn Wohnungen <em>derzeit im Angebot</em>",
  "Восемнадцать квартир <em>сейчас в продаже</em>", "ثمانية عشر مسكنًا <em>معروضة حاليًا</em>", "Achttien woningen <em>momenteel aangeboden</em>",
  "Osiemnaście lokali <em>aktualnie w ofercie</em>", "Atten boliger <em>til salgs nå</em>", "Arton bostäder <em>till salu just nu</em>")
a('Prices are those of the developer’s price list as of October 2026 and are confirmed before reservation. Eighteen',
  "Los precios son los de la lista de precios del promotor a octubre de 2026 y se confirman antes de la reserva. Hay dieciocho viviendas a la venta, de dos o tres dormitorios y dos baños; los documentos del promotor no indican cuántas viviendas tiene el conjunto de la promoción.",
  "Les prix sont ceux de la liste de prix du promoteur à octobre 2026 et sont confirmés avant la réservation. Dix-huit logements sont proposés, de deux ou trois chambres et deux salles de bains ; les documents du promoteur n’indiquent pas le nombre de logements de l’ensemble du programme.",
  "Die Preise entsprechen der Preisliste des Bauträgers vom Oktober 2026 und werden vor der Reservierung bestätigt. Achtzehn Wohnungen mit zwei oder drei Schlafzimmern und zwei Bädern werden angeboten; die Unterlagen des Bauträgers nennen nicht die Zahl der Wohnungen der gesamten Anlage.",
  "Цены соответствуют прайс-листу застройщика на октябрь 2026 года и подтверждаются перед бронированием. В продаже восемнадцать квартир с двумя или тремя спальнями и двумя ванными комнатами; в документах застройщика не указано, сколько квартир во всём комплексе.",
  "الأسعار هي أسعار قائمة المطوّر في أكتوبر 2026 وتُؤكَّد قبل الحجز. هناك ثمانية عشر مسكنًا معروضًا بغرفتي نوم أو ثلاث غرف نوم وحمّامين؛ ولا تذكر وثائق المطوّر عدد المساكن في المشروع كله.",
  "De prijzen zijn die van de prijslijst van de ontwikkelaar van oktober 2026 en worden vóór de reservering bevestigd. Achttien woningen met twee of drie slaapkamers en twee badkamers worden aangeboden; de documenten van de ontwikkelaar noemen niet het aantal woningen van het hele complex.",
  "Ceny pochodzą z cennika dewelopera z października 2026 roku i są potwierdzane przed rezerwacją. W ofercie jest osiemnaście lokali z dwiema lub trzema sypialniami i dwiema łazienkami; dokumenty dewelopera nie podają liczby lokali w całej inwestycji.",
  "Prisene er de i utbyggerens prisliste fra oktober 2026 og bekreftes før reservasjon. Atten boliger med to eller tre soverom og to bad er til salgs; utbyggerens dokumenter oppgir ikke hvor mange boliger hele anlegget har.",
  "Priserna är de i exploatörens prislista från oktober 2026 och bekräftas före reservation. Arton bostäder med två eller tre sovrum och två badrum är till salu; exploatörens dokument anger inte hur många bostäder hela området har.")
a('Prices, built areas and terraces are transcribed from the developer’s price list',
  "Los precios, las superficies construidas y las terrazas están transcritos de la lista de precios del promotor tal como aparece en su portal en octubre de 2026. La lista no indica si el IVA está incluido. Da una terraza de 1,004.00 {U} para la vivienda 422A; el plano de esa vivienda muestra terrazas de 10.6, 51.2 y 38.6 {U}, 100.4 {U} en total, así que la tabla muestra 100.40 {U}. Cuando la lista y un plano difieren ligeramente, la tabla sigue la lista: la vivienda 431D tiene 100.0 {U} construidos en la lista y 100.1 en su plano; la vivienda 434A tiene 117.00 {U} y una terraza de 33.00 {U} en la lista y 117.1 y 33.1 en su plano; la vivienda 420A tiene una terraza y un jardín de 61.00 y 46.00 {U} en la lista y de 61.1 y 46.1 en su plano; y la vivienda 163B tiene 157.25 {U} en la lista y 157.4 en su plano. Los planos de las viviendas 154B y 164B muestran tres baños donde la lista da dos. Las superficies interiores son las superficies útiles interiores de los planos.",
  "Les prix, les surfaces construites et les terrasses sont transcrits de la liste de prix du promoteur telle qu’elle figure sur son portail en octobre 2026. La liste n’indique pas si la TVA est incluse. Elle donne une terrasse de 1,004.00 {U} pour le logement 422A ; le plan de ce logement montre des terrasses de 10.6, 51.2 et 38.6 {U}, soit 100.4 {U} au total, et le tableau indique donc 100.40 {U}. Lorsque la liste et un plan diffèrent légèrement, le tableau suit la liste : le logement 431D fait 100.0 {U} construits sur la liste et 100.1 sur son plan ; le logement 434A fait 117.00 {U} avec une terrasse de 33.00 {U} sur la liste et 117.1 et 33.1 sur son plan ; le logement 420A a une terrasse et un jardin de 61.00 et 46.00 {U} sur la liste et de 61.1 et 46.1 sur son plan ; et le logement 163B fait 157.25 {U} sur la liste et 157.4 sur son plan. Les plans des logements 154B et 164B montrent trois salles de bains là où la liste en donne deux. Les surfaces intérieures sont les surfaces utiles intérieures des plans.",
  "Preise, bebaute Flächen und Terrassen sind der Preisliste des Bauträgers entnommen, wie sie im Oktober 2026 auf dessen Portal zu sehen war. Die Liste sagt nicht, ob die Mehrwertsteuer enthalten ist. Für Wohnung 422A nennt sie eine Terrasse von 1,004.00 {U}; der Grundriss dieser Wohnung zeigt Terrassen von 10.6, 51.2 und 38.6 {U}, zusammen 100.4 {U}, daher zeigt die Tabelle 100.40 {U}. Wo Liste und Grundriss geringfügig abweichen, folgt die Tabelle der Liste: Wohnung 431D hat laut Liste 100.0 {U} bebaut und laut Grundriss 100.1; Wohnung 434A hat laut Liste 117.00 {U} und eine Terrasse von 33.00 {U}, laut Grundriss 117.1 und 33.1; Wohnung 420A hat laut Liste eine Terrasse und einen Garten von 61.00 und 46.00 {U}, laut Grundriss 61.1 und 46.1; und Wohnung 163B hat laut Liste 157.25 {U} und laut Grundriss 157.4. Die Grundrisse der Wohnungen 154B und 164B zeigen drei Bäder, wo die Liste zwei nennt. Die Innenflächen sind die nutzbaren Innenflächen aus den Grundrissen.",
  "Цены, застроенные площади и террасы перенесены из прайс-листа застройщика, опубликованного на его портале в октябре 2026 года. В прайс-листе не сказано, включён ли НДС. Для квартиры 422A в нём указана терраса 1,004.00 {U}; на планировке этой квартиры террасы 10.6, 51.2 и 38.6 {U}, всего 100.4 {U}, поэтому в таблице стоит 100.40 {U}. Где прайс-лист и планировка немного расходятся, таблица следует прайс-листу: квартира 431D — 100.0 {U} застроенной площади по прайс-листу и 100.1 по планировке; квартира 434A — 117.00 {U} и терраса 33.00 {U} по прайс-листу и 117.1 и 33.1 по планировке; у квартиры 420A терраса и сад 61.00 и 46.00 {U} по прайс-листу и 61.1 и 46.1 по планировке; квартира 163B — 157.25 {U} по прайс-листу и 157.4 по планировке. На планировках квартир 154B и 164B три ванные комнаты, а в прайс-листе две. Внутренние площади — это полезные внутренние площади по планировкам.",
  "الأسعار والمساحات المبنية والتراسات منقولة من قائمة أسعار المطوّر كما ظهرت على بوابته في أكتوبر 2026. ولا تذكر القائمة ما إذا كانت ضريبة القيمة المضافة مشمولة. وهي تعطي تراسًا بمساحة 1,004.00 {U} للمسكن 422A؛ ومخطط ذلك المسكن يُظهر تراسات بمساحة 10.6 و51.2 و38.6 {U}، أي 100.4 {U} في المجموع، لذلك يعرض الجدول 100.40 {U}. وحيث تختلف القائمة والمخطط قليلًا يتبع الجدول القائمة: المسكن 431D مساحته المبنية 100.0 {U} في القائمة و100.1 في مخططه؛ والمسكن 434A مساحته 117.00 {U} وتراسه 33.00 {U} في القائمة و117.1 و33.1 في مخططه؛ والمسكن 420A له تراس وحديقة بمساحة 61.00 و46.00 {U} في القائمة و61.1 و46.1 في مخططه؛ والمسكن 163B مساحته 157.25 {U} في القائمة و157.4 في مخططه. وتُظهر مخططات المسكنين 154B و164B ثلاثة حمّامات بينما تذكر القائمة اثنين. والمساحات الداخلية هي المساحات الداخلية القابلة للاستخدام في المخططات.",
  "De prijzen, bebouwde oppervlaktes en terrassen zijn overgenomen uit de prijslijst van de ontwikkelaar zoals die in oktober 2026 op zijn portaal stond. De lijst zegt niet of de btw erin zit. Voor woning 422A geeft zij een terras van 1,004.00 {U}; de plattegrond van die woning toont terrassen van 10.6, 51.2 en 38.6 {U}, samen 100.4 {U}, dus de tabel toont 100.40 {U}. Waar lijst en plattegrond licht verschillen, volgt de tabel de lijst: woning 431D is volgens de lijst 100.0 {U} bebouwd en volgens de plattegrond 100.1; woning 434A is volgens de lijst 117.00 {U} met een terras van 33.00 {U} en volgens de plattegrond 117.1 en 33.1; woning 420A heeft volgens de lijst een terras en een tuin van 61.00 en 46.00 {U} en volgens de plattegrond 61.1 en 46.1; en woning 163B is volgens de lijst 157.25 {U} en volgens de plattegrond 157.4. De plattegronden van de woningen 154B en 164B tonen drie badkamers waar de lijst er twee geeft. De binnenoppervlaktes zijn de bruikbare binnenoppervlaktes uit de plattegronden.",
  "Ceny, powierzchnie zabudowy i tarasy przepisano z cennika dewelopera widocznego na jego portalu w październiku 2026 roku. Cennik nie mówi, czy cena zawiera VAT. Dla lokalu 422A podaje taras o powierzchni 1,004.00 {U}; rzut tego lokalu pokazuje tarasy o powierzchni 10.6, 51.2 i 38.6 {U}, razem 100.4 {U}, dlatego w tabeli widnieje 100.40 {U}. Tam, gdzie cennik i rzut różnią się nieznacznie, tabela podąża za cennikiem: lokal 431D ma według cennika 100.0 {U} zabudowy, a według rzutu 100.1; lokal 434A ma według cennika 117.00 {U} i taras 33.00 {U}, a według rzutu 117.1 i 33.1; lokal 420A ma według cennika taras i ogród o powierzchni 61.00 i 46.00 {U}, a według rzutu 61.1 i 46.1; a lokal 163B ma według cennika 157.25 {U}, a według rzutu 157.4. Rzuty lokali 154B i 164B pokazują trzy łazienki, gdy cennik podaje dwie. Powierzchnie wnętrz to użytkowe powierzchnie wewnętrzne z rzutów.",
  "Prisene, bygde arealer og terrasser er hentet fra utbyggerens prisliste slik den sto på portalen i oktober 2026. Listen sier ikke om mva er inkludert. For bolig 422A oppgir den en terrasse på 1,004.00 {U}; plantegningen til boligen viser terrasser på 10.6, 51.2 og 38.6 {U}, til sammen 100.4 {U}, så tabellen viser 100.40 {U}. Der listen og en plantegning avviker litt, følger tabellen listen: bolig 431D er 100.0 {U} bygd ifølge listen og 100.1 ifølge plantegningen; bolig 434A er 117.00 {U} med en terrasse på 33.00 {U} ifølge listen og 117.1 og 33.1 ifølge plantegningen; bolig 420A har en terrasse og en hage på 61.00 og 46.00 {U} ifølge listen og 61.1 og 46.1 ifølge plantegningen; og bolig 163B er 157.25 {U} ifølge listen og 157.4 ifølge plantegningen. Plantegningene til boligene 154B og 164B viser tre bad der listen oppgir to. De innvendige arealene er de brukbare innvendige arealene fra plantegningene.",
  "Priserna, byggytorna och terrasserna är hämtade från exploatörens prislista så som den visades på dess portal i oktober 2026. Listan anger inte om momsen ingår. För bostad 422A anger den en terrass på 1,004.00 {U}; planritningen för bostaden visar terrasser på 10.6, 51.2 och 38.6 {U}, sammanlagt 100.4 {U}, så tabellen visar 100.40 {U}. Där listan och en planritning skiljer sig något följer tabellen listan: bostad 431D är 100.0 {U} byggyta enligt listan och 100.1 enligt planritningen; bostad 434A är 117.00 {U} med en terrass på 33.00 {U} enligt listan och 117.1 och 33.1 enligt planritningen; bostad 420A har en terrass och en trädgård på 61.00 och 46.00 {U} enligt listan och 61.1 och 46.1 enligt planritningen; och bostad 163B är 157.25 {U} enligt listan och 157.4 enligt planritningen. Planritningarna för bostäderna 154B och 164B visar tre badrum där listan anger två. De invändiga ytorna är de användbara invändiga ytorna från planritningarna.")
a('See this alongside the other Marbella projects we hold',
  "Véalo junto a los demás proyectos de Marbella que tenemos.", "Comparez-le aux autres projets de Marbella que nous suivons.", "Vergleichen Sie es mit den anderen Marbella-Projekten, die wir betreuen.",
  "Сравните его с другими проектами в Марбелье, которые у нас есть.", "قارنوه بمشاريع مربيّا الأخرى لدينا.", "Bekijk het naast de andere Marbella-projecten die wij in portefeuille hebben.",
  "Proszę porównać go z innymi projektami w Marbelli, które mamy w ofercie.", "Se det sammen med de andre prosjektene i Marbella vi har.", "Se det tillsammans med de andra projekten i Marbella som vi har.")
a('See the area with us, and the plans against the stage of the works',
  "Vea la zona con nosotros y los planos frente al estado de las obras.", "Découvrez le secteur avec nous, et confrontez les plans à l’avancement des travaux.",
  "Sehen Sie sich die Umgebung mit uns an und vergleichen Sie die Grundrisse mit dem Baufortschritt.", "Осмотрите район вместе с нами и сравните планировки с ходом работ.",
  "شاهدوا المنطقة معنا، وقارنوا المخططات بمرحلة الأعمال.", "Bekijk de omgeving met ons en leg de plattegronden naast de stand van de werken.",
  "Zobaczą Państwo okolicę razem z nami i porównają rzuty ze stanem prac.", "Se området sammen med oss, og sammenlign plantegningene med byggestatus.",
  "Se området tillsammans med oss och jämför planritningarna med byggstadiet.")
a('We confirm the reservation terms and the payment schedule in writing',
  "Confirmamos por escrito las condiciones de reserva y el calendario de pagos, y después el contrato privado de compraventa.",
  "Nous confirmons par écrit les conditions de réservation et l’échéancier de paiement, puis le contrat de vente privé.",
  "Wir bestätigen die Reservierungsbedingungen und den Zahlungsplan schriftlich, danach folgt der private Kaufvertrag.",
  "Мы письменно подтверждаем условия бронирования и график платежей, затем следует частный договор купли-продажи.",
  "نؤكد كتابيًا شروط الحجز وجدول الدفعات، ثم يأتي عقد الشراء الخاص.",
  "Wij bevestigen de reserveringsvoorwaarden en het betalingsschema schriftelijk, daarna volgt het onderhandse koopcontract.",
  "Potwierdzamy na piśmie warunki rezerwacji i harmonogram płatności, a następnie przychodzi prywatna umowa kupna.",
  "Vi bekrefter reservasjonsvilkårene og betalingsplanen skriftlig, deretter kommer den private kjøpekontrakten.",
  "Vi bekräftar reservationsvillkoren och betalningsplanen skriftligt, därefter följer det privata köpeavtalet.")
a('See the <em>hillside and the area</em>',
  "Vea <em>la ladera y la zona</em>", "Découvrez <em>la colline et le secteur</em>", "Erleben Sie <em>den Hang und die Umgebung</em>", "Осмотрите <em>склон и окрестности</em>",
  "شاهدوا <em>المنحدر والمنطقة</em>", "Bekijk <em>de helling en de omgeving</em>", "Zobaczą Państwo <em>zbocze i okolicę</em>", "Se <em>åssiden og området</em>", "Se <em>sluttningen och området</em>")
a('Walk the hillside and see where the terraces face the sea',
  "Recorra la ladera y vea hacia dónde miran las terrazas al mar.", "Parcourez la colline et voyez où les terrasses font face à la mer.",
  "Gehen Sie über den Hang und sehen Sie, wo die Terrassen zum Meer zeigen.", "Пройдитесь по склону и увидите, где террасы выходят на море.",
  "تجوّلوا في المنحدر وانظروا أين تطلّ التراسات على البحر.", "Loop over de helling en zie waar de terrassen op de zee uitkijken.",
  "Przejdą Państwo po zboczu i zobaczą, gdzie tarasy zwracają się ku morzu.", "Gå over åssiden og se hvor terrassene vender mot havet.", "Gå över sluttningen och se var terrasserna vetter mot havet.")
a('We drive to the centre of Marbella and the beach with you and time it',
  "Vamos en coche con usted al centro de Marbella y a la playa, y cronometramos el trayecto.", "Nous allons en voiture avec vous au centre de Marbella et à la plage, et nous chronométrons le trajet.",
  "Wir fahren mit Ihnen ins Zentrum von Marbella und zum Strand und stoppen die Zeit.", "Мы едем с вами на машине в центр Марбельи и на пляж и засекаем время в пути.",
  "نقود معكم إلى وسط مربيّا والشاطئ ونحتسب زمن الرحلة.", "Wij rijden met u naar het centrum van Marbella en naar het strand en nemen de tijd op.",
  "Jedziemy z Państwem samochodem do centrum Marbelli i na plażę i mierzymy czas przejazdu.", "Vi kjører til sentrum av Marbella og stranden og tar tiden.",
  "Vi kör med er till Marbellas centrum och stranden och tar tid.")
a('Ask about <em>Altamira Hills Residences</em>',
  "Pregunte por <em>Altamira Hills Residences</em>", "Renseignez-vous sur <em>Altamira Hills Residences</em>", "Fragen Sie nach <em>Altamira Hills Residences</em>",
  "Узнайте о <em>Altamira Hills Residences</em>", "اسألوا عن <em>Altamira Hills Residences</em>", "Vraag naar <em>Altamira Hills Residences</em>",
  "Zapytanie o <em>Altamira Hills Residences</em>", "Spør om <em>Altamira Hills Residences</em>", "Fråga om <em>Altamira Hills Residences</em>")
a('Hello Nueva Living, I would like information about Altamira',
  "Hola Nueva Living, quisiera información sobre Altamira Hills Residences.", "Bonjour Nueva Living, je souhaiterais des informations sur Altamira Hills Residences.",
  "Guten Tag Nueva Living, ich hätte gern Informationen zu Altamira Hills Residences.", "Здравствуйте, Nueva Living, прошу прислать информацию об Altamira Hills Residences.",
  "مرحبًا Nueva Living، أودّ الحصول على معلومات عن Altamira Hills Residences.", "Hallo Nueva Living, ik wil graag informatie over Altamira Hills Residences.",
  "Dzień dobry Nueva Living, proszę o informacje o Altamira Hills Residences.", "Hei Nueva Living, jeg vil gjerne ha informasjon om Altamira Hills Residences.",
  "Hej Nueva Living, jag skulle vilja ha information om Altamira Hills Residences.")
a('Eighteen homes are listed with a price',
  "Hay dieciocho viviendas a la venta con precio: diez apartamentos de dos dormitorios, tres apartamentos de tres dormitorios y cinco áticos, de {E458000} a {E1065000}. Los documentos no indican cuántas viviendas tiene el conjunto de la promoción.",
  "Dix-huit logements sont proposés avec un prix : dix appartements de deux chambres, trois appartements de trois chambres et cinq penthouses, de {E458000} à {E1065000}. Les documents n’indiquent pas combien de logements compte l’ensemble du programme.",
  "Achtzehn Wohnungen werden mit Preis angeboten: zehn Wohnungen mit zwei Schlafzimmern, drei Wohnungen mit drei Schlafzimmern und fünf Penthouses, von {E458000} bis {E1065000}. Die Unterlagen nennen nicht, wie viele Wohnungen die gesamte Anlage hat.",
  "В продаже восемнадцать квартир с ценами: десять квартир с двумя спальнями, три с тремя спальнями и пять пентхаусов, от {E458000} до {E1065000}. В документах не указано, сколько квартир во всём комплексе.",
  "هناك ثمانية عشر مسكنًا معروضًا بأسعارها: عشر شقق بغرفتي نوم وثلاث شقق بثلاث غرف نوم وخمسة بنتهاوس، من {E458000} إلى {E1065000}. ولا تذكر الوثائق عدد المساكن في المشروع كله.",
  "Achttien woningen worden met prijs aangeboden: tien appartementen met twee slaapkamers, drie appartementen met drie slaapkamers en vijf penthouses, van {E458000} tot {E1065000}. De documenten noemen niet hoeveel woningen het hele complex heeft.",
  "W ofercie z ceną jest osiemnaście lokali: dziesięć apartamentów z dwiema sypialniami, trzy z trzema sypialniami i pięć penthouse’ów, od {E458000} do {E1065000}. Dokumenty nie podają, ile lokali liczy cała inwestycja.",
  "Atten boliger er til salgs med pris: ti leiligheter med to soverom, tre leiligheter med tre soverom og fem toppleiligheter, fra {E458000} til {E1065000}. Dokumentene oppgir ikke hvor mange boliger hele anlegget har.",
  "Arton bostäder är till salu med pris: tio lägenheter med två sovrum, tre lägenheter med tre sovrum och fem takvåningar, från {E458000} till {E1065000}. Dokumenten anger inte hur många bostäder hela området har.")
a('The price list does not say. We confirm the taxes',
  "La lista de precios no lo indica. Confirmamos por escrito los impuestos y los gastos de la compra antes de que usted reserve.", "La liste de prix ne le dit pas. Nous confirmons par écrit les taxes et les frais d’achat avant votre réservation.",
  "Die Preisliste sagt es nicht. Wir bestätigen Steuern und Kaufnebenkosten schriftlich, bevor Sie reservieren.", "В прайс-листе это не указано. Мы письменно подтверждаем налоги и расходы на покупку до бронирования.",
  "لا تذكر قائمة الأسعار ذلك. نؤكد الضرائب وتكاليف الشراء كتابيًا قبل أن تحجزوا.", "De prijslijst zegt het niet. Wij bevestigen de belastingen en de aankoopkosten schriftelijk voordat u reserveert.",
  "Cennik tego nie mówi. Potwierdzamy podatki i koszty zakupu na piśmie przed rezerwacją.", "Prislisten sier det ikke. Vi bekrefter skatter og kjøpskostnader skriftlig før reservasjon.",
  "Prislistan anger det inte. Vi bekräftar skatter och köpkostnader skriftligt före reservation.")
a('The specification describes a community garage and storage rooms but does not say',
  "La memoria de calidades describe un garaje comunitario y trasteros, pero no indica si una plaza está incluida en el precio. Lo preguntamos para la vivienda que usted elija.",
  "La notice descriptive décrit un garage commun et des caves, mais n’indique pas si une place est incluse dans le prix. Nous posons la question pour le logement que vous choisirez.",
  "Die Ausstattungsbeschreibung nennt eine Gemeinschaftsgarage und Abstellräume, sagt aber nicht, ob ein Stellplatz im Preis enthalten ist. Wir fragen für die Wohnung nach, die Sie wählen.",
  "В описании качества упомянуты общий гараж и кладовые, но не сказано, входит ли парковочное место в цену. Мы уточняем это для выбранной вами квартиры.",
  "تصف مواصفات الجودة مرآبًا مشتركًا وغرف تخزين، لكنها لا تذكر ما إذا كان موقف مشمولًا في السعر. نستفسر عنه للمسكن الذي تختارونه.",
  "De kwaliteitsomschrijving beschrijft een gemeenschappelijke garage en bergingen, maar zegt niet of een parkeerplaats in de prijs zit. Wij vragen het na voor de woning die u kiest.",
  "Opis jakości wspomina o garażu wspólnym i komórkach lokatorskich, ale nie mówi, czy miejsce postojowe jest wliczone w cenę. Pytamy o to dla wybranego przez Państwa lokalu.",
  "Kvalitetsbeskrivelsen beskriver et felles garasjeanlegg og boder, men sier ikke om en plass er inkludert i prisen. Vi spør om det for boligen som velges.",
  "Kvalitetsbeskrivningen beskriver ett gemensamt garage och förråd, men anger inte om en plats ingår i priset. Vi frågar om det för den bostad ni väljer.")
a('None of the developer’s documents gives a completion date. We ask for the contractual date and the stage',
  "Ningún documento del promotor indica una fecha de entrega. Pedimos la fecha contractual y el estado de las obras.", "Aucun document du promoteur ne donne de date de livraison. Nous demandons la date contractuelle et l’avancement des travaux.",
  "Keines der Dokumente des Bauträgers nennt einen Fertigstellungstermin. Wir fordern den vertraglichen Termin und den Baufortschritt an.", "Ни в одном документе застройщика не указан срок сдачи. Мы запрашиваем договорную дату и ход работ.",
  "لا تذكر أي من وثائق المطوّر موعدًا للتسليم. نطلب الموعد التعاقدي ومرحلة الأعمال.", "Geen van de documenten van de ontwikkelaar noemt een opleveringsdatum. Wij vragen de contractuele datum en de stand van de werken op.",
  "Żaden z dokumentów dewelopera nie podaje terminu oddania. Prosimy o termin umowny i stan prac.", "Ingen av utbyggerens dokumenter oppgir en overleveringsdato. Vi ber om den kontraktfestede datoen og byggestatusen.",
  "Inget av exploatörens dokument anger ett leveransdatum. Vi ber om det avtalade datumet och byggstadiet.")
a('What facilities does the community have?',
  "¿Qué instalaciones tiene la comunidad?", "Quels équipements la résidence propose-t-elle ?", "Welche Einrichtungen bietet die Anlage?", "Какая инфраструктура есть в комплексе?",
  "ما المرافق المتوفرة في المجمّع؟", "Welke voorzieningen heeft de gemeenschap?", "Jakie udogodnienia ma wspólnota?", "Hvilke fasiliteter har fellesområdet?", "Vilka bekvämligheter har området?")
a('An outdoor pool, a heated indoor pool, a spa, a gym with an outdoor terrace, a pool bar',
  "Una piscina exterior, una piscina interior climatizada, un spa, un gimnasio con terraza exterior, un bar de piscina y una zona de coworking, en jardines cuidados.",
  "Une piscine extérieure, une piscine intérieure chauffée, un spa, une salle de sport avec terrasse extérieure, un bar de piscine et un espace de coworking, dans des jardins paysagers.",
  "Ein Außenpool, ein beheizter Innenpool, ein Spa, ein Fitnessraum mit Außenterrasse, eine Poolbar und ein Coworking-Bereich in gepflegten Gärten.",
  "Наружный бассейн, подогреваемый внутренний бассейн, спа, тренажёрный зал с внешней террасой, бар у бассейна и коворкинг среди ухоженных садов.",
  "مسبح خارجي ومسبح داخلي مدفأ وسبا وصالة رياضية بتراس خارجي وبار مسبح ومساحة للعمل المشترك، وسط حدائق مهيّأة.",
  "Een buitenzwembad, een verwarmd binnenzwembad, een spa, een gym met buitenterras, een poolbar en een coworkingruimte, in aangelegde tuinen.",
  "Basen zewnętrzny, podgrzewany basen wewnętrzny, spa, siłownia z tarasem zewnętrznym, bar przy basenie i strefa coworkingu, w pielęgnowanych ogrodach.",
  "Et utendørs basseng, et oppvarmet innendørs basseng, et spa, et treningsrom med utendørs terrasse, en bassengbar og et coworking-område, i opparbeidede hager.",
  "En utomhuspool, en uppvärmd inomhuspool, ett spa, ett gym med utomhusterrass, en poolbar och en coworkingyta, i anlagda trädgårdar.")

# every string must be answered, except the floor labels assemble.py builds
left = [t for t in todo if t not in T and not re.fullmatch(r'(Portal \d+|Block \d+), [A-Za-z ]+|(Ground|First|Second|Third) floor', t)]
if left:
    print('NOT COVERED', len(left))
    for t in left: print('  ', repr(t[:110]))
    sys.exit(1)
json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'translations')
