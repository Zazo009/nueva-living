# -*- coding: utf-8 -*-
"""Dunique Marbella: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_m.json keyed by the English string, as assemble.py expects. Tokens: {E5200000}
money, {N30.33} decimal number, {U} the area unit.
    python3 tools/import/k_dunique_marbella.py <scratch dir>      (writes <dir>/tr_m.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/dunique-marbella/project.json'))


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


# photo prefix per locale: the description that follows carries its own connector (de, d’, van, av ...)
PH = {'es': 'Fotografía ', 'fr': 'Photographie ', 'de': 'Foto ', 'ru': 'Фотография ', 'ar': 'صورة ',
      'nl': 'Foto ', 'pl': 'Zdjęcie ', 'no': 'Fotografi ', 'sv': 'Fotografi '}


def ph(path, *tr):
    assert len(tr) == 9, path
    en = get(path)
    assert en.startswith('Photograph ') or en.startswith('Photograph'), en
    put(en, [PH[l] + t for l, t in zip(LOCS, tr)])


same('Dunique Marbella'); same('Dunique <em>Marbella</em>')

# ---- description, SEO, hero, card -------------------------------------------------------------

a('.description',
  'Dos viviendas disponibles en Dunique Marbella, un complejo en primera línea de playa en Marbella junto a un sistema dunar protegido: una villa pareada de cuatro dormitorios y un apartamento en planta baja de tres dormitorios, cada uno con piscina y jardín privados. No se indica fecha de entrega. Desde {E5200000} más IVA.',
  'Deux logements disponibles à Dunique Marbella, un ensemble en bord de mer à Marbella, à côté d’un système dunaire protégé : une villa jumelée de quatre chambres et un appartement de plain-pied de trois chambres, chacun avec piscine et jardin privés. Aucune date de livraison n’est indiquée. À partir de {E5200000} hors TVA.',
  'Zwei verfügbare Immobilien in Dunique Marbella, einer Anlage direkt am Strand von Marbella neben einem geschützten Dünensystem: eine Doppelhaushälfte mit vier Schlafzimmern und eine Erdgeschosswohnung mit drei Schlafzimmern, jeweils mit privatem Pool und Garten. Ein Fertigstellungstermin ist nicht angegeben. Ab {E5200000} zuzüglich MwSt.',
  'Два доступных объекта в Dunique Marbella — комплексе на первой линии у пляжа в Марбелье рядом с охраняемой системой дюн: парный дом с четырьмя спальнями и квартира на первом этаже с тремя спальнями, у каждого — собственный бассейн и сад. Срок сдачи не указан. От {E5200000} без НДС.',
  'مسكنان متاحان في Dunique Marbella، وهو مجمّع على الواجهة البحرية في ماربيا بجوار نظام كثبان رملية محمي: فيلا شبه منفصلة بأربع غرف نوم وشقة في الطابق الأرضي بثلاث غرف نوم، لكلٍّ منهما مسبح وحديقة خاصان. لم يُذكر موعد إنجاز. ابتداءً من {E5200000} دون ضريبة القيمة المضافة.',
  'Twee beschikbare woningen in Dunique Marbella, een complex direct aan het strand in Marbella naast een beschermd duinsysteem: een halfvrijstaande villa met vier slaapkamers en een appartement op de begane grond met drie slaapkamers, elk met een privézwembad en een tuin. Er wordt geen opleveringsdatum genoemd. Vanaf {E5200000} excl. btw.',
  'Dwa dostępne lokale w Dunique Marbella, kompleksie tuż przy plaży w Marbelli, obok chronionego systemu wydm: dom bliźniaczy z czterema sypialniami i mieszkanie na parterze z trzema sypialniami, każdy z prywatnym basenem i ogrodem. Termin oddania nie jest podany. Od {E5200000} plus VAT.',
  'To ledige boliger i Dunique Marbella, et anlegg helt ved stranden i Marbella ved siden av et vernet dynesystem: en tomannsvilla med fire soverom og en leilighet i første etasje med tre soverom, begge med privat basseng og hage. Ingen overleveringsdato er oppgitt. Fra {E5200000} pluss mva.',
  'Två lediga bostäder i Dunique Marbella, ett område vid stranden i Marbella intill ett skyddat dynsystem: ett parhus med fyra sovrum och en lägenhet på bottenvåningen med tre sovrum, båda med egen pool och trädgård. Inget tillträdesdatum anges. Från {E5200000} plus IVA (spansk moms).')
a('.seoDescription',
  'Dos viviendas en Dunique Marbella, un complejo en primera línea de playa junto a un sistema dunar protegido: una villa de cuatro dormitorios y un apartamento de tres dormitorios con piscinas privadas, desde {E5200000} más IVA.',
  'Deux logements à Dunique Marbella, un ensemble en bord de mer à côté d’un système dunaire protégé : une villa de quatre chambres et un appartement de trois chambres avec piscines privées, à partir de {E5200000} hors TVA.',
  'Zwei Immobilien in Dunique Marbella, einer Anlage direkt am Strand neben einem geschützten Dünensystem: eine Villa mit vier und eine Wohnung mit drei Schlafzimmern, jeweils mit privatem Pool, ab {E5200000} zuzüglich MwSt.',
  'Два объекта в Dunique Marbella — комплексе на первой линии у пляжа рядом с охраняемой системой дюн: вилла с четырьмя спальнями и квартира с тремя спальнями, у обеих собственные бассейны. От {E5200000} без НДС.',
  'مسكنان في Dunique Marbella، وهو مجمّع على الواجهة البحرية بجوار نظام كثبان رملية محمي: فيلا بأربع غرف نوم وشقة بثلاث غرف نوم، بمسبحين خاصين، ابتداءً من {E5200000} دون ضريبة القيمة المضافة.',
  'Twee woningen in Dunique Marbella, een complex direct aan het strand naast een beschermd duinsysteem: een villa met vier slaapkamers en een appartement met drie slaapkamers, met privézwembaden, vanaf {E5200000} excl. btw.',
  'Dwa lokale w Dunique Marbella, kompleksie tuż przy plaży obok chronionego systemu wydm: willa z czterema sypialniami i mieszkanie z trzema sypialniami z prywatnymi basenami, od {E5200000} plus VAT.',
  'To boliger i Dunique Marbella, et anlegg helt ved stranden ved siden av et vernet dynesystem: en villa med fire soverom og en leilighet med tre soverom med private bassenger, fra {E5200000} pluss mva.',
  'Två bostäder i Dunique Marbella, ett område vid stranden intill ett skyddat dynsystem: en villa med fyra sovrum och en lägenhet med tre sovrum med egna pooler, från {E5200000} plus IVA.')
a('.twitterDescription',
  'Una villa de cuatro dormitorios y un apartamento de tres con piscinas privadas en Dunique Marbella, junto a las dunas, desde {E5200000} más IVA.',
  'Une villa de quatre chambres et un appartement de trois chambres avec piscines privées à Dunique Marbella, à côté des dunes, à partir de {E5200000} hors TVA.',
  'Eine Villa mit vier und eine Wohnung mit drei Schlafzimmern, jeweils mit privatem Pool, in Dunique Marbella, neben den Dünen, ab {E5200000} zuzüglich MwSt.',
  'Вилла с четырьмя спальнями и квартира с тремя спальнями с собственными бассейнами в Dunique Marbella, рядом с дюнами. От {E5200000} без НДС.',
  'فيلا بأربع غرف نوم وشقة بثلاث غرف نوم بمسبحين خاصين في Dunique Marbella، بجوار الكثبان الرملية، ابتداءً من {E5200000} دون ضريبة القيمة المضافة.',
  'Een villa met vier slaapkamers en een appartement met drie slaapkamers met privézwembaden in Dunique Marbella, naast de duinen, vanaf {E5200000} excl. btw.',
  'Willa z czterema sypialniami i mieszkanie z trzema sypialniami z prywatnymi basenami w Dunique Marbella, obok wydm, od {E5200000} plus VAT.',
  'En villa med fire soverom og en leilighet med tre soverom med private bassenger i Dunique Marbella, ved siden av dynene, fra {E5200000} pluss mva.',
  'En villa med fyra sovrum och en lägenhet med tre sovrum med egna pooler i Dunique Marbella, intill dynerna, från {E5200000} plus IVA.')
a('.hero.startingPrice', 'Desde {E5200000} + IVA', 'À partir de {E5200000} + TVA', 'Ab {E5200000} + MwSt.', 'От {E5200000} + НДС',
  'ابتداءً من {E5200000} + ضريبة القيمة المضافة', 'Vanaf {E5200000} + btw', 'Od {E5200000} + VAT', 'Fra {E5200000} + mva.', 'Från {E5200000} + IVA')
a('.card.meta[0][1]', '{E5200000} + IVA', '{E5200000} + TVA', '{E5200000} + MwSt.', '{E5200000} + НДС',
  '{E5200000} + ضريبة القيمة المضافة', '{E5200000} + btw', '{E5200000} + VAT', '{E5200000} + mva.', '{E5200000} + IVA')
a('.availability.priceRange', '{E5200000} - {E5400000} + IVA', '{E5200000} - {E5400000} + TVA', '{E5200000} - {E5400000} + MwSt.',
  '{E5200000} - {E5400000} + НДС', '{E5200000} - {E5400000} + ضريبة القيمة المضافة', '{E5200000} - {E5400000} + btw',
  '{E5200000} - {E5400000} + VAT', '{E5200000} - {E5400000} + mva.', '{E5200000} - {E5400000} + IVA')
a('.card.description',
  'Dos viviendas en Dunique Marbella, un complejo en primera línea de playa junto a un sistema dunar protegido: una villa de cuatro dormitorios y un apartamento de tres, cada uno con piscina y jardín privados, desde {E5200000} + IVA.',
  'Deux logements à Dunique Marbella, un ensemble en bord de mer à côté d’un système dunaire protégé : une villa de quatre chambres et un appartement de trois chambres, chacun avec piscine et jardin privés, à partir de {E5200000} + TVA.',
  'Zwei Immobilien in Dunique Marbella, einer Anlage direkt am Strand neben einem geschützten Dünensystem: eine Villa mit vier und eine Wohnung mit drei Schlafzimmern, jeweils mit privatem Pool und Garten, ab {E5200000} + MwSt.',
  'Два объекта в Dunique Marbella — комплексе на первой линии у пляжа рядом с охраняемой системой дюн: вилла с четырьмя спальнями и квартира с тремя спальнями, у каждого — собственный бассейн и сад. От {E5200000} + НДС.',
  'مسكنان في Dunique Marbella، وهو مجمّع على الواجهة البحرية بجوار نظام كثبان رملية محمي: فيلا بأربع غرف نوم وشقة بثلاث غرف نوم، لكلٍّ منهما مسبح وحديقة خاصان، ابتداءً من {E5200000} + ضريبة القيمة المضافة.',
  'Twee woningen in Dunique Marbella, een complex direct aan het strand naast een beschermd duinsysteem: een villa met vier slaapkamers en een appartement met drie slaapkamers, elk met een privézwembad en een tuin, vanaf {E5200000} + btw.',
  'Dwa lokale w Dunique Marbella, kompleksie tuż przy plaży obok chronionego systemu wydm: willa z czterema sypialniami i mieszkanie z trzema sypialniami, każdy z prywatnym basenem i ogrodem, od {E5200000} + VAT.',
  'To boliger i Dunique Marbella, et anlegg helt ved stranden ved siden av et vernet dynesystem: en villa med fire soverom og en leilighet med tre soverom, begge med privat basseng og hage, fra {E5200000} + mva.',
  'Två bostäder i Dunique Marbella, ett område vid stranden intill ett skyddat dynsystem: en villa med fyra sovrum och en lägenhet med tre sovrum, båda med egen pool och trädgård, från {E5200000} + IVA.')

# ---- images: section images and the gallery -----------------------------------------------------

ph('.images.hero.alt',
   'al atardecer de una terraza blanca curva con puertas de cristal iluminadas y, encima, la terraza de la cubierta con una zona de estar y un jacuzzi, con montañas al fondo',
   'au crépuscule d’une terrasse blanche incurvée aux portes vitrées éclairées et, au-dessus, de la terrasse sur le toit avec un salon et un jacuzzi, avec des montagnes en arrière-plan',
   'in der Dämmerung von einer geschwungenen weißen Terrasse mit beleuchteten Glastüren und darüber der Dachterrasse mit Loungebereich und Whirlpool, im Hintergrund Berge',
   'в сумерках: белая изогнутая терраса с освещёнными стеклянными дверями, над ней терраса на крыше с зоной отдыха и джакузи, на заднем плане горы',
   'عند الغروب لتراس أبيض منحنٍ بأبواب زجاجية مضاءة، وفوقه تراس السطح بمنطقة جلوس وجاكوزي، والجبال في الخلفية',
   'bij schemering van een gebogen wit terras met verlichte glazen deuren en daarboven het dakterras met een loungehoek en een jacuzzi, met bergen op de achtergrond',
   'o zmierzchu: biały zaokrąglony taras z oświetlonymi szklanymi drzwiami, nad nim taras na dachu ze strefą wypoczynku i jacuzzi, w tle góry',
   'i skumringen av en buet hvit terrasse med opplyste glassdører og takterrassen over med en sofagruppe og en jacuzzi, med fjell i bakgrunnen',
   'i skymningen av en böjd vit terrass med upplysta glasdörrar och takterrassen ovanför med en soffgrupp och en jacuzzi, med berg i bakgrunden')
ph('.images.architecture.alt',
   'de día de una terraza blanca curva con pérgola, puertas correderas de cristal y una mesa de comedor, con la terraza de la cubierta encima',
   'de jour d’une terrasse blanche incurvée avec pergola, portes coulissantes vitrées et table à manger, avec la terrasse sur le toit au-dessus',
   'bei Tag von einer geschwungenen weißen Terrasse mit Pergola, gläsernen Schiebetüren und einem Esstisch, darüber die Dachterrasse',
   'днём: белая изогнутая терраса с перголой, стеклянными раздвижными дверями и обеденным столом, над ней терраса на крыше',
   'نهارًا لتراس أبيض منحنٍ ببرغولا وأبواب زجاجية منزلقة وطاولة طعام، وفوقه تراس السطح',
   'overdag van een gebogen wit terras met een pergola, glazen schuifdeuren en een eettafel, met het dakterras erboven',
   'za dnia: biały zaokrąglony taras z pergolą, szklanymi drzwiami przesuwnymi i stołem jadalnianym, nad nim taras na dachu',
   'på dagtid av en buet hvit terrasse med pergola, skyvedører i glass og et spisebord, med takterrassen over',
   'på dagen av en böjd vit terrass med pergola, skjutdörrar av glas och ett matbord, med takterrassen ovanför')
ph('.images.lifestyle.alt',
   'de una terraza en la cubierta con una piscina de borde de cristal y el mar en el horizonte',
   'd’une terrasse sur le toit avec une piscine à bord de verre et la mer à l’horizon',
   'einer Dachterrasse mit einem Pool mit Glasrand und dem Meer am Horizont',
   'террасы на крыше с бассейном со стеклянным бортом и морем на горизонте',
   'لتراس على السطح بمسبح بحافة زجاجية والبحر في الأفق',
   'van een dakterras met een zwembad met glazen rand en de zee aan de horizon',
   'tarasu na dachu z basenem ze szklaną krawędzią i morzem na horyzoncie',
   'av en takterrasse med et basseng med glasskant og havet i horisonten',
   'av en takterrass med en pool med glaskant och havet vid horisonten')
ph('.images.privateViewing.alt',
   'de un salón con techo de lamas de madera, un sofá, sillones y un mueble multimedia, con cristaleras a una terraza',
   'd’un séjour avec un plafond à lattes de bois, un canapé, des fauteuils et un meuble multimédia, avec des baies vitrées sur une terrasse',
   'eines Wohnzimmers mit einer Holzlamellendecke, einem Sofa, Sesseln und einer Medienwand, mit Glasfronten zu einer Terrasse',
   'гостиной с потолком из деревянных реек, диваном, креслами и мультимедийной стенкой, со стеклянными стенами на террасу',
   'لغرفة جلوس بسقف من شرائح الخشب وأريكة ومقاعد وجدار للوسائط المتعددة، مع واجهات زجاجية نحو التراس',
   'van een woonkamer met een plafond van houten latten, een bank, fauteuils en een mediawand, met glaspartijen naar een terras',
   'salonu z sufitem z drewnianych lameli, sofą, fotelami i zabudową multimedialną, z przeszkleniami na taras',
   'av en stue med et himling av trelameller, en sofa, lenestoler og en mediavegg, med glassfelt mot en terrasse',
   'av ett vardagsrum med ett undertak av trälameller, en soffa, fåtöljer och en mediavägg, med glaspartier mot en terrass')
a('.media.headlineHtml', 'El complejo <em>al detalle</em>', 'L’ensemble <em>en détail</em>', 'Die Anlage <em>im Detail</em>', 'Комплекс <em>в деталях</em>',
  'المجمّع <em>بالتفصيل</em>', 'Het complex <em>in detail</em>', 'Kompleksiet <em>i detalj</em>', 'Anlegget <em>i detalj</em>', 'Området <em>i detalj</em>')
a('.media.copy',
  'Fotografías de una vivienda amueblada del complejo, una imagen aérea de la parcela y los planos de las dos viviendas publicadas.',
  'Photographies d’un logement meublé de l’ensemble, image aérienne du site et plans des deux logements présentés.',
  'Fotos einer möblierten Wohnung der Anlage, eine Luftaufnahme des Grundstücks und die Grundrisse der beiden gelisteten Immobilien.',
  'Фотографии меблированного жилья в комплексе, аэроснимок участка и планировки двух объектов из списка.',
  'صور لمسكن مفروش في المجمّع، وصورة جوية للموقع، ومخططات المسكنين المدرجين.',
  'Foto’s van een gemeubileerde woning in het complex, een luchtbeeld van het terrein en de plattegronden van de twee vermelde woningen.',
  'Zdjęcia umeblowanego lokalu w kompleksie, zdjęcie lotnicze terenu oraz rzuty dwóch lokali z listy.',
  'Bilder av en møblert bolig i anlegget, et luftbilde av tomten og plantegningene for de to boligene som er oppført.',
  'Bilder av en möblerad bostad i området, en flygbild av tomten och planritningarna för de två bostäder som är listade.')
a('.media.note',
  'Las fotografías muestran una vivienda amueblada del complejo. La galería no indica de qué vivienda o tipo se trata, por lo que no son fotografías de las dos viviendas publicadas, y el mobiliario y la decoración que aparecen no están incluidos. La imagen aérea procede del plano general del promotor y muestra el complejo según el proyecto. Los planos son los planos comerciales del promotor: no son contractuales, los nombres de las estancias están en español y las superficies que figuran en ellos son aproximadas.',
  'Les photographies montrent un logement meublé de l’ensemble. La galerie ne précise ni de quel logement ni de quel type il s’agit ; ce ne sont donc pas des photographies des deux logements présentés, et le mobilier et la décoration qui y figurent ne sont pas inclus. L’image aérienne provient du plan général du promoteur et montre l’ensemble tel que prévu. Les plans sont les plans commerciaux du promoteur : ils n’ont pas de valeur contractuelle, les noms des pièces y sont en espagnol et les surfaces qui y figurent sont approximatives.',
  'Die Fotos zeigen eine möblierte Wohnung der Anlage. Die Galerie sagt nicht, um welche Wohnung oder welchen Typ es sich handelt; es sind also keine Fotos der beiden gelisteten Immobilien, und Möblierung und Dekoration darauf sind nicht enthalten. Die Luftaufnahme stammt aus dem Gesamtplan des Bauträgers und zeigt die Anlage wie geplant. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen darauf sind auf Spanisch, und die Flächenangaben darauf sind ungefähr.',
  'На фотографиях — меблированное жильё в комплексе. В галерее не указано, какое это жильё и какого типа, поэтому это не фотографии двух объектов из списка; мебель и декор на них не входят в комплектацию. Аэроснимок взят из генерального плана застройщика и показывает комплекс таким, каким он задуман. Планировки — коммерческие планы застройщика: они не имеют договорной силы, названия помещений на них даны на испанском языке, а указанные площади приблизительны.',
  'تُظهر الصور مسكنًا مفروشًا في المجمّع. لا يذكر المعرض أي مسكن أو أي نوع هو، لذلك فهي ليست صورًا للمسكنين المدرجين، والأثاث والديكور الظاهران فيها غير مشمولين. الصورة الجوية مأخوذة من المخطط العام للمطوّر وتُظهر المجمّع كما هو مخطط له. المخططات هي مخططات البيع الخاصة بالمطوّر: ليست ملزمة تعاقديًا، وأسماء الغرف عليها بالإسبانية، والمساحات الظاهرة عليها تقريبية.',
  'De foto’s tonen een gemeubileerde woning in het complex. De galerij zegt niet om welke woning of welk type het gaat, dus het zijn geen foto’s van de twee vermelde woningen, en het meubilair en de inrichting erop zijn niet inbegrepen. Het luchtbeeld komt uit het algemene plan van de ontwikkelaar en toont het complex zoals gepland. De plattegronden zijn de verkoopplannen van de ontwikkelaar: ze zijn niet contractueel, de namen van de ruimten erop zijn in het Spaans en de oppervlakten erop zijn bij benadering.',
  'Zdjęcia przedstawiają umeblowany lokal w kompleksie. Galeria nie podaje, o jaki lokal lub typ chodzi, więc nie są to zdjęcia dwóch lokali z listy, a meble i wystrój na nich nie wchodzą w cenę. Zdjęcie lotnicze pochodzi z planu generalnego dewelopera i pokazuje kompleks w kształcie, w jakim jest zaplanowany. Rzuty to plany sprzedażowe dewelopera: nie mają mocy umownej, nazwy pomieszczeń na nich są po hiszpańsku, a podane na nich powierzchnie są przybliżone.',
  'Bildene viser en møblert bolig i anlegget. Galleriet oppgir ikke hvilken bolig eller hvilken type det er, så de er ikke fotografier av de to boligene som er oppført, og møblene og innredningen på dem er ikke inkludert. Luftbildet er hentet fra utbyggerens generalplan og viser anlegget slik det er planlagt. Plantegningene er utbyggerens salgsplaner: de er ikke kontraktsfestet, romnavnene på dem er på spansk, og arealene på dem er omtrentlige.',
  'Bilderna visar en möblerad bostad i området. Galleriet anger inte vilken bostad eller vilken typ det är, så det är inte fotografier av de två bostäder som är listade, och möblerna och inredningen på dem ingår inte. Flygbilden kommer från exploatörens generalplan och visar området som det är planerat. Planritningarna är exploatörens försäljningsritningar: de är inte avtalsbindande, rumsnamnen på dem är på spanska och areorna på dem är ungefärliga.')

# gallery: captions and alts, in the order of media.items
def cap(i, *tr): a(f'.media.items[{i}].caption', *tr)
def alt(i, *tr): ph(f'.media.items[{i}].alt', *tr)

cap(0, 'Las terrazas al atardecer', 'Les terrasses au crépuscule', 'Die Terrassen in der Dämmerung', 'Террасы в сумерках', 'التراسات عند الغروب', 'De terrassen bij schemering', 'Tarasy o zmierzchu', 'Terrassene i skumringen', 'Terrasserna i skymningen')
alt(1, 'al atardecer de la terraza blanca curva y del salón iluminado tras sus puertas de cristal',
    'au crépuscule de la terrasse blanche incurvée et du séjour éclairé derrière ses portes vitrées',
    'in der Dämmerung von der geschwungenen weißen Terrasse und dem beleuchteten Wohnzimmer hinter den Glastüren',
    'в сумерках: белая изогнутая терраса и освещённая гостиная за стеклянными дверями',
    'عند الغروب للتراس الأبيض المنحني وغرفة الجلوس المضاءة خلف أبوابه الزجاجية',
    'bij schemering van het gebogen witte terras en de verlichte woonkamer achter de glazen deuren',
    'o zmierzchu: zaokrąglony biały taras i oświetlony salon za szklanymi drzwiami',
    'i skumringen av den buede hvite terrassen og den opplyste stuen bak glassdørene',
    'i skymningen av den böjda vita terrassen och det upplysta vardagsrummet bakom glasdörrarna')
cap(1, 'Una terraza y el salón al atardecer', 'Une terrasse et le séjour au crépuscule', 'Eine Terrasse und das Wohnzimmer in der Dämmerung', 'Терраса и гостиная в сумерках', 'تراس وغرفة جلوس عند الغروب', 'Een terras en de woonkamer bij schemering', 'Taras i salon o zmierzchu', 'En terrasse og stuen i skumringen', 'En terrass och vardagsrummet i skymningen')
cap(2, 'La terraza curva de día', 'La terrasse incurvée de jour', 'Die geschwungene Terrasse bei Tag', 'Изогнутая терраса днём', 'التراس المنحني نهارًا', 'Het gebogen terras overdag', 'Zaokrąglony taras za dnia', 'Den buede terrassen på dagtid', 'Den böjda terrassen på dagen')
a('.media.items[3].alt',
  'Imagen aérea del plano general del promotor, que muestra el complejo según el proyecto junto a la playa, con las calles y las casas de los alrededores',
  'Image aérienne tirée du plan général du promoteur, montrant l’ensemble tel que prévu à côté de la plage, avec les rues et les maisons alentour',
  'Luftaufnahme aus dem Gesamtplan des Bauträgers, die die Anlage wie geplant am Strand zeigt, mit den umliegenden Straßen und Häusern',
  'Аэроснимок из генерального плана застройщика: комплекс, каким он задуман, рядом с пляжем, с окружающими улицами и домами',
  'صورة جوية من المخطط العام للمطوّر تُظهر المجمّع كما هو مخطط له بجوار الشاطئ، مع الشوارع والمنازل المحيطة',
  'Luchtbeeld uit het algemene plan van de ontwikkelaar, dat het complex zoals gepland naast het strand toont, met de omliggende straten en huizen',
  'Zdjęcie lotnicze z planu generalnego dewelopera, pokazujące kompleks w zaplanowanym kształcie obok plaży, z otaczającymi ulicami i domami',
  'Luftbilde fra utbyggerens generalplan som viser anlegget slik det er planlagt ved siden av stranden, med gatene og husene rundt',
  'Flygbild från exploatörens generalplan som visar området som det är planerat intill stranden, med omgivande gator och hus')
a('.media.items[3].caption', 'La parcela desde el aire', 'Le site vu du ciel', 'Das Grundstück aus der Luft', 'Участок с воздуха', 'الموقع من الجو', 'Het terrein vanuit de lucht', 'Teren z lotu ptaka', 'Tomten fra luften', 'Tomten från luften')
alt(4, 'desde arriba de una cubierta con una piscina alargada, un césped, un jacuzzi, una mesa de comedor y una pérgola',
    'vue d’en haut d’un toit-terrasse avec un long bassin, une pelouse, un jacuzzi, une table à manger et une pergola',
    'von oben auf ein Dachdeck mit einem langen Pool, einem Rasen, einem Whirlpool, einem Esstisch und einer Pergola',
    'сверху: крыша с длинным бассейном, газоном, джакузи, обеденным столом и перголой',
    'من الأعلى لسطح فيه مسبح طويل ومرج وجاكوزي وطاولة طعام وبرغولا',
    'van bovenaf van een dakdek met een lang zwembad, een gazon, een jacuzzi, een eettafel en een pergola',
    'z góry: dach z długim basenem, trawnikiem, jacuzzi, stołem jadalnianym i pergolą',
    'ovenfra av et takdekk med et langt basseng, en plen, en jacuzzi, et spisebord og en pergola',
    'uppifrån av ett takdäck med en lång pool, en gräsmatta, en jacuzzi, ett matbord och en pergola')
cap(4, 'La cubierta vista desde arriba', 'Le toit-terrasse vu d’en haut', 'Das Dachdeck von oben', 'Крыша сверху', 'السطح من الأعلى', 'Het dakdek van bovenaf', 'Dach z góry', 'Takdekket ovenfra', 'Takdäcket uppifrån')
alt(5, 'de una terraza en la cubierta con un pabellón revestido de madera, un jacuzzi sobre una plataforma elevada, una cama balinesa naranja y montañas al fondo',
    'd’une terrasse sur le toit avec un pavillon habillé de bois, un jacuzzi sur une plateforme surélevée, un lit de repos orange et des montagnes en arrière-plan',
    'einer Dachterrasse mit einem holzverkleideten Pavillon, einem Whirlpool auf einem erhöhten Deck, einem orangefarbenen Daybed und Bergen im Hintergrund',
    'террасы на крыше с павильоном, обшитым деревом, джакузи на приподнятом настиле, оранжевой кушеткой и горами на заднем плане',
    'لتراس على السطح بجناح مكسو بالخشب وجاكوزي على منصة مرتفعة وأريكة نهارية برتقالية والجبال في الخلفية',
    'van een dakterras met een met hout bekleed paviljoen, een jacuzzi op een verhoogd dek, een oranje daybed en bergen op de achtergrond',
    'tarasu na dachu z pawilonem wykończonym drewnem, jacuzzi na podwyższonym pomoście, pomarańczową leżanką i górami w tle',
    'av en takterrasse med et trekledd paviljongbygg, en jacuzzi på et hevet dekk, en oransje dagseng og fjell i bakgrunnen',
    'av en takterrass med en träklädd paviljong, en jacuzzi på ett upphöjt däck, en orange dagbädd och berg i bakgrunden')
cap(5, 'Una terraza en la cubierta con jacuzzi', 'Une terrasse sur le toit avec jacuzzi', 'Eine Dachterrasse mit Whirlpool', 'Терраса на крыше с джакузи', 'تراس على السطح مع جاكوزي', 'Een dakterras met een jacuzzi', 'Taras na dachu z jacuzzi', 'En takterrasse med jacuzzi', 'En takterrass med jacuzzi')
cap(6, 'Una piscina en la cubierta frente al mar', 'Une piscine sur le toit face à la mer', 'Ein Dachpool mit Meerblick', 'Бассейн на крыше с видом на море', 'مسبح على السطح مقابل البحر', 'Een dakzwembad met zicht op zee', 'Basen na dachu z widokiem na morze', 'Et takbasseng mot havet', 'En takpool mot havet')
alt(7, 'de una piscina en la cubierta con tarima de madera, tumbonas y sombrillas',
    'd’une piscine sur le toit avec un deck en bois, des chaises longues et des parasols',
    'eines Dachpools mit Holzdeck, Sonnenliegen und Sonnenschirmen',
    'бассейна на крыше с деревянным настилом, шезлонгами и зонтами',
    'لمسبح على السطح بأرضية خشبية ومقاعد تشمّس ومظلات',
    'van een dakzwembad met een houten dek, ligbedden en parasols',
    'basenu na dachu z drewnianym pomostem, leżakami i parasolami',
    'av et takbasseng med tredekk, solsenger og parasoller',
    'av en takpool med trädäck, solstolar och parasoller')
cap(7, 'Una piscina en la cubierta y su tarima', 'Une piscine sur le toit et son deck', 'Ein Dachpool mit Holzdeck', 'Бассейн на крыше и деревянный настил', 'مسبح على السطح وأرضيته الخشبية', 'Een dakzwembad en een houten dek', 'Basen na dachu i drewniany pomost', 'Et takbasseng og tredekket', 'En takpool och trädäcket')
alt(8, 'al atardecer de una piscina iluminada en la cubierta, una tarima de madera, tumbonas y una sombrilla',
    'au crépuscule d’une piscine éclairée sur le toit, d’un deck en bois, de chaises longues et d’un parasol',
    'in der Dämmerung von einem beleuchteten Dachpool, einem Holzdeck, Sonnenliegen und einem Sonnenschirm',
    'в сумерках: освещённый бассейн на крыше, деревянный настил, шезлонги и зонт',
    'عند الغروب لمسبح مضاء على السطح وأرضية خشبية ومقاعد تشمّس ومظلة',
    'bij schemering van een verlicht dakzwembad, een houten dek, ligbedden en een parasol',
    'o zmierzchu: oświetlony basen na dachu, drewniany pomost, leżaki i parasol',
    'i skumringen av et opplyst takbasseng, et tredekk, solsenger og en parasoll',
    'i skymningen av en upplyst takpool, ett trädäck, solstolar och ett parasoll')
cap(8, 'Una piscina en la cubierta al atardecer', 'Une piscine sur le toit au crépuscule', 'Ein Dachpool in der Dämmerung', 'Бассейн на крыше в сумерках', 'مسبح على السطح عند الغروب', 'Een dakzwembad bij schemering', 'Basen na dachu o zmierzchu', 'Et takbasseng i skumringen', 'En takpool i skymningen')
alt(9, 'de una terraza cubierta con sofás, una mesa de centro redonda, un olivo en una maceta y el mar a lo lejos',
    'd’une terrasse couverte avec des canapés, une table basse ronde, un olivier en pot et la mer au loin',
    'einer überdachten Terrasse mit Sofas, einem runden Couchtisch, einem Olivenbaum im Topf und dem Meer in der Ferne',
    'крытой террасы с диванами, круглым журнальным столиком, оливковым деревом в кадке и морем вдали',
    'لتراس مسقوف بأرائك وطاولة وسطية مستديرة وشجرة زيتون في وعاء والبحر في البعيد',
    'van een overdekt terras met banken, een ronde salontafel, een olijfboom in een pot en de zee in de verte',
    'tarasu zadaszonego z sofami, okrągłym stolikiem kawowym, drzewkiem oliwnym w donicy i morzem w oddali',
    'av en overdekket terrasse med sofaer, et rundt salongbord, et oliventre i en potte og havet i det fjerne',
    'av en övertäckt terrass med soffor, ett runt soffbord, ett olivträd i en kruka och havet i fjärran')
cap(9, 'Una terraza cubierta con vistas al mar', 'Une terrasse couverte avec vue sur la mer', 'Eine überdachte Terrasse mit Meerblick', 'Крытая терраса с видом на море', 'تراس مسقوف بإطلالة على البحر', 'Een overdekt terras met zicht op zee', 'Zadaszony taras z widokiem na morze', 'En overdekket terrasse med utsikt over havet', 'En övertäckt terrass med havsutsikt')
alt(10, 'de una terraza con un sofá, una mesa de centro de piedra, un olivo y una barandilla de cristal, con el mar más allá',
    'd’une terrasse avec un canapé, une table basse en pierre, un olivier et un garde-corps en verre, avec la mer au-delà',
    'einer Terrasse mit einem Sofa, einem Couchtisch aus Stein, einem Olivenbaum und einem Glasgeländer, dahinter das Meer',
    'террасы с диваном, каменным журнальным столиком, оливковым деревом и стеклянным ограждением, за ней море',
    'لتراس بأريكة وطاولة وسطية حجرية وشجرة زيتون ودرابزين زجاجي، والبحر خلفه',
    'van een terras met een bank, een stenen salontafel, een olijfboom en een glazen balustrade, met de zee erachter',
    'tarasu z sofą, kamiennym stolikiem kawowym, drzewkiem oliwnym i szklaną balustradą, za którym widać morze',
    'av en terrasse med en sofa, et salongbord i stein, et oliventre og et glassrekkverk, med havet bak',
    'av en terrass med en soffa, ett soffbord i sten, ett olivträd och ett glasräcke, med havet bakom')
cap(10, 'Una terraza sobre la costa', 'Une terrasse au-dessus de la côte', 'Eine Terrasse über der Küste', 'Терраса над побережьем', 'تراس مطل على الساحل', 'Een terras boven de kust', 'Taras nad wybrzeżem', 'En terrasse over kysten', 'En terrass ovanför kusten')
alt(11, 'de una terraza en la cubierta con un sofá cama blanco, una mesa de comedor y el mar en el horizonte',
    'd’une terrasse sur le toit avec un canapé de repos blanc, une table à manger et la mer à l’horizon',
    'einer Dachterrasse mit einem weißen Daybed-Sofa, einem Esstisch und dem Meer am Horizont',
    'террасы на крыше с белым диваном-кушеткой, обеденным столом и морем на горизонте',
    'لتراس على السطح بأريكة نهارية بيضاء وطاولة طعام والبحر في الأفق',
    'van een dakterras met een witte daybedbank, een eettafel en de zee aan de horizon',
    'tarasu na dachu z białą sofą-leżanką, stołem jadalnianym i morzem na horyzoncie',
    'av en takterrasse med en hvit dagsengsofa, et spisebord og havet i horisonten',
    'av en takterrass med en vit dagbäddssoffa, ett matbord och havet vid horisonten')
cap(11, 'Una zona de estar en la cubierta', 'Un salon sur le toit', 'Ein Loungebereich auf dem Dach', 'Зона отдыха на крыше', 'منطقة جلوس على السطح', 'Een loungehoek op het dak', 'Strefa wypoczynku na dachu', 'En sofagruppe på taket', 'En soffgrupp på taket')
alt(12, 'de una terraza en la cubierta con una mesa de comedor puesta, una barra con taburetes y el mar más allá',
    'd’une terrasse sur le toit avec une table à manger dressée, un comptoir avec des tabourets et la mer au-delà',
    'einer Dachterrasse mit einem gedeckten Esstisch, einer Bartheke mit Hockern und dem Meer dahinter',
    'террасы на крыше с накрытым обеденным столом, барной стойкой с табуретами и морем вдали',
    'لتراس على السطح بطاولة طعام معدّة ومنضدة بار بمقاعد عالية والبحر خلفها',
    'van een dakterras met een gedekte eettafel, een bar met krukken en de zee erachter',
    'tarasu na dachu z nakrytym stołem jadalnianym, barem z hokerami i morzem w oddali',
    'av en takterrasse med et dekket spisebord, en bardisk med barstoler og havet bak',
    'av en takterrass med ett dukat matbord, en bardisk med barstolar och havet bakom')
cap(12, 'Cenar en la terraza de la cubierta', 'Dîner sur la terrasse du toit', 'Essen auf der Dachterrasse', 'Обед на террасе на крыше', 'تناول الطعام على تراس السطح', 'Dineren op het dakterras', 'Posiłek na tarasie na dachu', 'Middag på takterrassen', 'Middag på takterrassen')
alt(13, 'de un jacuzzi sobre una plataforma elevada de madera con una cama balinesa naranja y un muro revestido de piedra',
    'd’un jacuzzi sur une plateforme surélevée en bois avec un lit de repos orange et un mur habillé de pierre',
    'eines Whirlpools auf einem erhöhten Holzdeck mit einem orangefarbenen Daybed und einer Steinverkleidung an der Wand',
    'джакузи на приподнятом деревянном настиле с оранжевой кушеткой и стеной, облицованной камнем',
    'لجاكوزي على منصة خشبية مرتفعة مع أريكة نهارية برتقالية وجدار مكسو بالحجر',
    'van een jacuzzi op een verhoogd houten dek met een oranje daybed en een met steen beklede muur',
    'jacuzzi na podwyższonym drewnianym pomoście z pomarańczową leżanką i ścianą wykończoną kamieniem',
    'av en jacuzzi på et hevet tredekk med en oransje dagseng og en steinkledd vegg',
    'av en jacuzzi på ett upphöjt trädäck med en orange dagbädd och en stenklädd vägg')
cap(13, 'Un jacuzzi en el solárium', 'Un jacuzzi sur le solarium', 'Ein Whirlpool auf dem Solarium', 'Джакузи на солярии', 'جاكوزي على السولاريوم', 'Een jacuzzi op het solarium', 'Jacuzzi na solarium', 'En jacuzzi på solterrassen', 'En jacuzzi på solterrassen')
alt(14, 'de una cocina exterior bajo una pérgola de madera, con encimera de piedra, una placa y vistas al mar',
    'd’une cuisine d’extérieur sous une pergola en bois, avec un plan de travail en pierre, une plaque de cuisson et une vue sur la mer',
    'einer Außenküche unter einer Holzpergola, mit einer Steinarbeitsplatte, einem Kochfeld und Blick auf das Meer',
    'уличной кухни под деревянной перголой с каменной столешницей, варочной панелью и видом на море',
    'لمطبخ خارجي تحت برغولا خشبية بسطح عمل حجري وموقد وإطلالة على البحر',
    'van een buitenkeuken onder een houten pergola, met een stenen werkblad, een kookplaat en zicht op de zee',
    'kuchni zewnętrznej pod drewnianą pergolą z kamiennym blatem, płytą grzewczą i widokiem na morze',
    'av et utekjøkken under en tre-pergola, med en benkeplate i stein, en kokeplate og utsikt over havet',
    'av ett utekök under en pergola av trä, med en bänkskiva i sten, en spishäll och utsikt över havet')
cap(14, 'Una cocina exterior', 'Une cuisine d’extérieur', 'Eine Außenküche', 'Уличная кухня', 'مطبخ خارجي', 'Een buitenkeuken', 'Kuchnia zewnętrzna', 'Et utekjøkken', 'Ett utekök')
alt(15, 'al atardecer de una terraza cubierta con una mesa de comedor redonda y una zona de estar, con el mar en el horizonte',
    'au coucher du soleil d’une terrasse couverte avec une table à manger ronde et un coin salon, avec la mer à l’horizon',
    'bei Sonnenuntergang von einer überdachten Terrasse mit einem runden Esstisch und einem Loungebereich, mit dem Meer am Horizont',
    'на закате: крытая терраса с круглым обеденным столом и зоной отдыха, на горизонте море',
    'عند الغروب لتراس مسقوف بطاولة طعام مستديرة ومنطقة جلوس والبحر في الأفق',
    'bij zonsondergang van een overdekt terras met een ronde eettafel en een zithoek, met de zee aan de horizon',
    'o zachodzie słońca: zadaszony taras z okrągłym stołem jadalnianym i strefą wypoczynku, na horyzoncie morze',
    'ved solnedgang av en overdekket terrasse med et rundt spisebord og en sofagruppe, med havet i horisonten',
    'vid solnedgången av en övertäckt terrass med ett runt matbord och en soffgrupp, med havet vid horisonten')
cap(15, 'Una terraza cubierta al atardecer', 'Une terrasse couverte au coucher du soleil', 'Eine überdachte Terrasse bei Sonnenuntergang', 'Крытая терраса на закате', 'تراس مسقوف عند الغروب', 'Een overdekt terras bij zonsondergang', 'Zadaszony taras o zachodzie słońca', 'En overdekket terrasse ved solnedgang', 'En övertäckt terrass vid solnedgången')
alt(17, 'de una cocina con una isla larga, hornos integrados y una mesa de comedor redonda, abierta a una terraza',
    'd’une cuisine avec un long îlot, des fours encastrés et une table à manger ronde, ouverte sur une terrasse',
    'einer Küche mit einer langen Kochinsel, Einbaubacköfen und einem runden Esstisch, offen zu einer Terrasse',
    'кухни с длинным островом, встроенными духовыми шкафами и круглым обеденным столом, открытой на террасу',
    'لمطبخ بجزيرة طويلة وأفران مدمجة وطاولة طعام مستديرة، مفتوح على التراس',
    'van een keuken met een lang eiland, ingebouwde ovens en een ronde eettafel, open naar een terras',
    'kuchni z długą wyspą, zabudowanymi piekarnikami i okrągłym stołem jadalnianym, otwartej na taras',
    'av et kjøkken med en lang øy, innebygde ovner og et rundt spisebord, åpent mot en terrasse',
    'av ett kök med en lång köksö, inbyggda ugnar och ett runt matbord, öppet mot en terrass')
cap(17, 'La cocina y la mesa de comedor', 'La cuisine et la table à manger', 'Die Küche und der Esstisch', 'Кухня и обеденный стол', 'المطبخ وطاولة الطعام', 'De keuken en de eettafel', 'Kuchnia i stół jadalniany', 'Kjøkkenet og spisebordet', 'Köket och matbordet')
alt(18, 'de un salón y comedor de planta abierta con una amplia cristalera corredera hacia la terraza',
    'd’un séjour et salle à manger en espace ouvert avec une large baie vitrée coulissante vers la terrasse',
    'eines offenen Wohn- und Essbereichs mit einer breiten gläsernen Schiebewand zur Terrasse',
    'гостиной и столовой открытой планировки с широкой стеклянной раздвижной стеной на террасу',
    'لغرفة جلوس وطعام مفتوحة المخطط مع جدار زجاجي منزلق عريض نحو التراس',
    'van een open woon- en eetkamer met een brede glazen schuifwand naar het terras',
    'salonu z jadalnią w otwartym układzie z szeroką przesuwną szklaną ścianą na taras',
    'av en åpen stue og spisestue med en bred glassvegg på skinner mot terrassen',
    'av ett öppet vardagsrum och matrum med en bred skjutbar glasvägg mot terrassen')
cap(18, 'Salón y comedor abiertos a la terraza', 'Séjour et salle à manger ouverts sur la terrasse', 'Wohnen und Essen, offen zur Terrasse', 'Гостиная и столовая с выходом на террасу', 'غرفة جلوس وطعام مفتوحتان على التراس', 'Wonen en eten, open naar het terras', 'Salon i jadalnia otwarte na taras', 'Stue og spisestue åpne mot terrassen', 'Vardagsrum och matrum öppna mot terrassen')
alt(19, 'por la tarde de una isla de cocina con una balda empotrada y un salpicadero de espejo',
    'en soirée d’un îlot de cuisine avec une niche encastrée et une crédence en miroir',
    'am Abend von einer Kochinsel mit einer eingelassenen Ablage und einer Spiegelrückwand',
    'вечером: кухонный остров со встроенной нишей-полкой и зеркальным фартуком',
    'في المساء لجزيرة مطبخ برف مدمج وواجهة خلفية من المرايا',
    'in de avond van een keukeneiland met een inbouwnis en een spiegelachterwand',
    'wieczorem: wyspa kuchenna z wbudowaną półką i lustrzanym panelem ściennym',
    'om kvelden av en kjøkkenøy med en innfelt hylle og en speilbakvegg',
    'på kvällen av en köksö med en inbyggd hylla och ett speglat stänkskydd')
cap(19, 'La isla de cocina por la tarde', 'L’îlot de cuisine en soirée', 'Die Kochinsel am Abend', 'Кухонный остров вечером', 'جزيرة المطبخ في المساء', 'Het keukeneiland in de avond', 'Wyspa kuchenna wieczorem', 'Kjøkkenøya om kvelden', 'Köksön på kvällen')
alt(20, 'de una escalera con peldaños negros y una barandilla de cristal ante una pared de lamas de madera',
    'd’un escalier à marches noires et garde-corps en verre devant un mur à lattes de bois',
    'einer Treppe mit schwarzen Stufen und einem Glasgeländer vor einer Wand aus Holzlamellen',
    'лестницы с чёрными ступенями и стеклянным ограждением на фоне стены из деревянных реек',
    'لدرج بدرجات سوداء ودرابزين زجاجي أمام جدار من شرائح الخشب',
    'van een trap met zwarte treden en een glazen balustrade voor een wand van houten latten',
    'schodów z czarnymi stopniami i szklaną balustradą przed ścianą z drewnianych lameli',
    'av en trapp med svarte trinn og et glassrekkverk foran en vegg av trelameller',
    'av en trappa med svarta steg och ett glasräcke framför en vägg av trälameller')
cap(20, 'La escalera', 'L’escalier', 'Die Treppe', 'Лестница', 'الدرج', 'De trap', 'Schody', 'Trappen', 'Trappan')
alt(21, 'de un dormitorio con un cabecero de lamas, una pared con motivos de bambú y una ventana al jardín',
    'd’une chambre avec une tête de lit à lattes, un mur au motif de bambous et une fenêtre sur le jardin',
    'eines Schlafzimmers mit einem Kopfteil aus Lamellen, einer Wand mit Bambusmotiv und einem Fenster zum Garten',
    'спальни с изголовьем из реек, стеной с рисунком из бамбука и окном в сад',
    'لغرفة نوم بلوح رأس من الشرائح وجدار بنقش الخيزران ونافذة نحو الحديقة',
    'van een slaapkamer met een hoofdbord van latten, een wand met bamboemotief en een raam naar de tuin',
    'sypialni z zagłówkiem z lameli, ścianą z motywem bambusa i oknem na ogród',
    'av et soverom med en hodegavl av lameller, en vegg med bambusmotiv og et vindu mot hagen',
    'av ett sovrum med en sänggavel av lameller, en vägg med bambumotiv och ett fönster mot trädgården')
cap(21, 'Un dormitorio con cabecero de lamas', 'Une chambre avec tête de lit à lattes', 'Ein Schlafzimmer mit Lamellen-Kopfteil', 'Спальня с изголовьем из реек', 'غرفة نوم بلوح رأس من الشرائح', 'Een slaapkamer met een hoofdbord van latten', 'Sypialnia z zagłówkiem z lameli', 'Et soverom med hodegavl av lameller', 'Ett sovrum med sänggavel av lameller')
alt(22, 'de un dormitorio con un cabecero de cuero, un banco y una ventana con vistas a las palmeras',
    'd’une chambre avec une tête de lit en cuir, un banc et une fenêtre sur des palmiers',
    'eines Schlafzimmers mit einem Lederkopfteil, einer Bank und einem Fenster mit Blick auf Palmen',
    'спальни с кожаным изголовьем, банкеткой и окном с видом на пальмы',
    'لغرفة نوم بلوح رأس من الجلد ومقعد طويل ونافذة تطل على أشجار النخيل',
    'van een slaapkamer met een leren hoofdbord, een bank en een raam met uitzicht op palmbomen',
    'sypialni ze skórzanym zagłówkiem, ławką i oknem z widokiem na palmy',
    'av et soverom med en hodegavl i skinn, en benk og et vindu med utsikt over palmer',
    'av ett sovrum med en sänggavel i läder, en bänk och ett fönster med utsikt över palmer')
cap(22, 'Un dormitorio con cabecero de cuero', 'Une chambre avec tête de lit en cuir', 'Ein Schlafzimmer mit Leder-Kopfteil', 'Спальня с кожаным изголовьем', 'غرفة نوم بلوح رأس من الجلد', 'Een slaapkamer met een leren hoofdbord', 'Sypialnia ze skórzanym zagłówkiem', 'Et soverom med hodegavl i skinn', 'Ett sovrum med sänggavel i läder')
alt(23, 'de un dormitorio con una pared tapizada tras la cama, un escritorio y una ventana',
    'd’une chambre avec un mur capitonné derrière le lit, un bureau et une fenêtre',
    'eines Schlafzimmers mit einer gepolsterten Wand hinter dem Bett, einem Schreibtisch und einem Fenster',
    'спальни с мягкой обивкой стены за кроватью, письменным столом и окном',
    'لغرفة نوم بجدار مكسو بالنسيج خلف السرير ومكتب ونافذة',
    'van een slaapkamer met een gestoffeerde wand achter het bed, een bureau en een raam',
    'sypialni z tapicerowaną ścianą za łóżkiem, biurkiem i oknem',
    'av et soverom med en polstret vegg bak sengen, et skrivebord og et vindu',
    'av ett sovrum med en klädd vägg bakom sängen, ett skrivbord och ett fönster')
cap(23, 'Un dormitorio con pared tapizada', 'Une chambre avec mur capitonné', 'Ein Schlafzimmer mit gepolsterter Wand', 'Спальня с мягкой стеной', 'غرفة نوم بجدار مكسو بالنسيج', 'Een slaapkamer met een gestoffeerde wand', 'Sypialnia z tapicerowaną ścianą', 'Et soverom med polstret vegg', 'Ett sovrum med klädd vägg')
alt(24, 'de un vestidor con puertas de cristal ahumado e interiores de madera',
    'd’un dressing avec des portes en verre fumé et des intérieurs en bois',
    'eines begehbaren Ankleidezimmers mit Rauchglastüren und Holzeinbauten',
    'гардеробной с дверями из дымчатого стекла и деревянной отделкой внутри',
    'لغرفة ملابس بأبواب من الزجاج المدخّن وتجهيزات داخلية خشبية',
    'van een inloopkleedkamer met rookglazen deuren en houten interieurs',
    'garderoby z drzwiami z szkła dymionego i drewnianym wnętrzem',
    'av et walk-in-garderobe med røykglassdører og interiør i tre',
    'av ett walk-in-closet med rökglasdörrar och inredning i trä')
alt(25, 'de un baño con un lavabo doble sobre un mueble suspendido, paredes de aspecto travertino y puertas de cristal con marco negro',
    'd’une salle de bain avec une double vasque sur un meuble suspendu, des murs aspect travertin et des portes vitrées à cadre noir',
    'eines Badezimmers mit einem Doppelwaschtisch auf einem Hängeschrank, Wänden in Travertinoptik und Glastüren mit schwarzem Rahmen',
    'ванной комнаты с двойной раковиной на подвесной тумбе, стенами под травертин и стеклянными дверями в чёрных рамах',
    'لحمام بحوض مزدوج على وحدة معلّقة وجدران بمظهر الترافرتين وأبواب زجاجية بإطار أسود',
    'van een badkamer met een dubbele wastafel op een hangend meubel, wanden in travertijnlook en glazen deuren met een zwart kader',
    'łazienki z podwójną umywalką na wiszącej szafce, ścianami o wyglądzie trawertynu i szklanymi drzwiami w czarnych ramach',
    'av et bad med en dobbel servant på et hengende skap, vegger i travertinlook og glassdører med svart ramme',
    'av ett badrum med ett dubbelt handfat på ett hängande underskåp, väggar i travertinlook och glasdörrar med svart ram')
cap(25, 'Un baño con lavabo doble', 'Une salle de bain avec double vasque', 'Ein Badezimmer mit Doppelwaschtisch', 'Ванная комната с двойной раковиной', 'حمام بحوض مزدوج', 'Een badkamer met een dubbele wastafel', 'Łazienka z podwójną umywalką', 'Et bad med dobbel servant', 'Ett badrum med dubbelt handfat')

# ---- overview, why, architecture -----------------------------------------------------------------

a('.overview.headlineHtml', 'Dos viviendas <em>disponibles</em>, junto a las dunas', 'Deux logements <em>disponibles</em>, à côté des dunes',
  'Zwei Immobilien <em>verfügbar</em>, neben den Dünen', 'Два <em>доступных</em> объекта рядом с дюнами', 'مسكنان <em>متاحان</em> بجوار الكثبان الرملية',
  'Twee woningen <em>beschikbaar</em>, naast de duinen', 'Dwa <em>dostępne</em> lokale obok wydm', 'To <em>ledige</em> boliger ved siden av dynene', 'Två <em>lediga</em> bostäder intill dynerna')
a('.overview.copy[0]',
  'Dunique Marbella es un complejo residencial de villas pareadas y apartamentos en Marbella, junto al sistema dunar protegido de El Barronal de la Morena. El folleto del promotor, fechado en agosto de 2024, describe 32 villas pareadas y 64 apartamentos, un centro social con spa, gimnasios, un espacio de coworking y un lounge en la azotea, y jardines escalonados de vegetación autóctona. Esas cifras son las del folleto, no actuales: la lista de ventas que tenemos recoge dos viviendas.',
  'Dunique Marbella est un ensemble résidentiel de villas jumelées et d’appartements à Marbella, à côté du système dunaire protégé d’El Barronal de la Morena. La brochure du promoteur, datée d’août 2024, décrit 32 villas jumelées et 64 appartements, un centre social avec spa, salles de sport, espace de coworking et lounge sur le toit, et des jardins en terrasses plantés d’espèces locales. Ces chiffres sont ceux de la brochure et non des chiffres actuels : la liste de vente dont nous disposons indique deux logements.',
  'Dunique Marbella ist eine Wohnanlage aus Doppelhaushälften und Wohnungen in Marbella, neben dem geschützten Dünensystem El Barronal de la Morena. Die Broschüre des Bauträgers, datiert auf August 2024, beschreibt 32 Doppelhaushälften und 64 Wohnungen, ein Social Hub mit Spa, Fitnessräumen, einem Coworking-Bereich und einer Rooftop-Lounge sowie terrassierte Gärten mit heimischer Bepflanzung. Diese Zahlen stammen aus der Broschüre und sind nicht aktuell: Die Verkaufsliste, die uns vorliegt, nennt zwei Immobilien.',
  'Dunique Marbella — жилой комплекс из парных домов и квартир в Марбелье, рядом с охраняемой системой дюн Эль-Баррональ-де-ла-Морена. В брошюре застройщика, датированной августом 2024 года, описаны 32 парных дома и 64 квартиры, социальный центр со спа, тренажёрными залами, коворкингом и лаунжем на крыше, а также террасные сады с местными растениями. Эти цифры взяты из брошюры и не являются актуальными: в имеющемся у нас списке продаж два объекта.',
  'Dunique Marbella مجمّع سكني من الفلل شبه المنفصلة والشقق في ماربيا، بجوار نظام الكثبان الرملية المحمي «إل بارونال دي لا مورينا». يصف كتيّب المطوّر، المؤرّخ في أغسطس 2024، 32 فيلا شبه منفصلة و64 شقة، ومركزًا اجتماعيًا يضم منتجعًا صحيًا وصالات رياضية ومساحة عمل مشترك وصالة على السطح، وحدائق مدرّجة بنباتات محلية. هذه الأرقام من الكتيّب وليست حديثة: فقائمة المبيعات التي بين أيدينا تضم مسكنين.',
  'Dunique Marbella is een woonwijk met halfvrijstaande villa’s en appartementen in Marbella, naast het beschermde duinsysteem El Barronal de la Morena. De brochure van de ontwikkelaar, gedateerd augustus 2024, beschrijft 32 halfvrijstaande villa’s en 64 appartementen, een sociaal centrum met spa, fitnessruimten, een coworkingruimte en een lounge op het dak, en terrasvormige tuinen met inheemse beplanting. Die aantallen komen uit de brochure en zijn niet actueel: de verkooplijst die wij hebben, vermeldt twee woningen.',
  'Dunique Marbella to kompleks mieszkaniowy domów bliźniaczych i apartamentów w Marbelli, obok chronionego systemu wydm El Barronal de la Morena. Broszura dewelopera z sierpnia 2024 r. opisuje 32 domy bliźniacze i 64 apartamenty, centrum społeczne ze spa, siłowniami, przestrzenią coworkingową i lounge’em na dachu oraz tarasowe ogrody z rodzimą roślinnością. To liczby z broszury, a nie aktualne: lista sprzedażowa, którą mamy, podaje dwa lokale.',
  'Dunique Marbella er et boligkompleks med tomannsvillaer og leiligheter i Marbella, ved siden av det vernede dynesystemet El Barronal de la Morena. Utbyggerens brosjyre, datert august 2024, beskriver 32 tomannsvillaer og 64 leiligheter, et sosialt senter med spa, treningsrom, en coworking-sone og en lounge på taket, og terrasserte hager med stedegen beplantning. Disse tallene er brosjyrens, ikke aktuelle: salgslisten vi har oppgir to boliger.',
  'Dunique Marbella är ett bostadsområde med parhus och lägenheter i Marbella, intill det skyddade dynsystemet El Barronal de la Morena. Exploatörens broschyr, daterad augusti 2024, beskriver 32 parhus och 64 lägenheter, ett socialt centrum med spa, gym, en coworkingyta och en lounge på taket, och terrasserade trädgårdar med inhemsk växtlighet. Siffrorna är broschyrens, inte aktuella: den försäljningslista vi har anger två bostäder.')
a('.overview.copy[1]',
  'Las dos viviendas publicadas son la villa Nr. 04, de cuatro dormitorios, y el apartamento Nr. 202, en planta baja y de tres dormitorios, cada uno con piscina y jardín privados. Ningún documento indica una fecha de entrega, y la lista de ventas muestra el proyecto como en construcción.',
  'Les deux logements présentés sont la villa Nr. 04, de quatre chambres, et l’appartement Nr. 202, de plain-pied et de trois chambres, chacun avec piscine et jardin privés. Aucun document n’indique de date de livraison, et la liste de vente présente le projet comme en construction.',
  'Die beiden gelisteten Immobilien sind die Villa Nr. 04 mit vier Schlafzimmern und die Erdgeschosswohnung Nr. 202 mit drei Schlafzimmern, jeweils mit privatem Pool und Garten. Keines der Dokumente nennt einen Fertigstellungstermin, und die Verkaufsliste zeigt das Projekt als im Bau.',
  'В списке два объекта: вилла Nr. 04 с четырьмя спальнями и квартира Nr. 202 на первом этаже с тремя спальнями; у каждого — собственный бассейн и сад. Ни в одном документе не указан срок сдачи, а в списке продаж проект значится как строящийся.',
  'المسكنان المدرجان هما الفيلا Nr. 04 بأربع غرف نوم، والشقة Nr. 202 في الطابق الأرضي بثلاث غرف نوم، ولكلٍّ منهما مسبح وحديقة خاصان. لا تذكر أي وثيقة موعدًا للتسليم، وتُظهر قائمة المبيعات المشروع قيد الإنشاء.',
  'De twee vermelde woningen zijn villa Nr. 04 met vier slaapkamers en appartement Nr. 202 op de begane grond met drie slaapkamers, elk met een privézwembad en een tuin. Geen enkel document noemt een opleveringsdatum, en de verkooplijst toont het project als in aanbouw.',
  'Dwa lokale z listy to willa Nr. 04 z czterema sypialniami i mieszkanie Nr. 202 na parterze z trzema sypialniami, każdy z prywatnym basenem i ogrodem. Żaden dokument nie podaje terminu oddania, a lista sprzedażowa pokazuje projekt jako w budowie.',
  'De to boligene som er oppført er villa Nr. 04 med fire soverom og leilighet Nr. 202 i første etasje med tre soverom, begge med privat basseng og hage. Ingen av dokumentene oppgir en overleveringsdato, og salgslisten viser prosjektet som under bygging.',
  'De två bostäder som är listade är villa Nr. 04 med fyra sovrum och lägenhet Nr. 202 på bottenvåningen med tre sovrum, båda med egen pool och trädgård. Inget av dokumenten anger ett leveransdatum, och försäljningslistan visar projektet som under byggnation.')
a('.overview.metrics[0][1]', '96 viviendas según el folleto de 2024', '96 logements selon la brochure de 2024', '96 Einheiten laut Broschüre von 2024',
  '96 объектов по брошюре 2024 года', '96 مسكنًا وفق كتيّب 2024', '96 woningen volgens de brochure van 2024', '96 lokali według broszury z 2024 r.',
  '96 boliger ifølge brosjyren fra 2024', '96 bostäder enligt broschyren från 2024')
a('.why.copy', 'Viviendas amplias con piscina y jardín privados, junto a un sistema dunar protegido en la costa de Marbella.',
  'De grands logements avec piscine et jardin privés, à côté d’un système dunaire protégé sur la côte de Marbella.',
  'Großzügige Immobilien mit privatem Pool und Garten, neben einem geschützten Dünensystem an der Küste von Marbella.',
  'Просторные объекты с собственным бассейном и садом рядом с охраняемой системой дюн на побережье Марбельи.',
  'مساكن واسعة بمسبح وحديقة خاصين، بجوار نظام كثبان رملية محمي على ساحل ماربيا.',
  'Ruime woningen met een privézwembad en een tuin, naast een beschermd duinsysteem aan de kust van Marbella.',
  'Obszerne lokale z prywatnym basenem i ogrodem, obok chronionego systemu wydm na wybrzeżu Marbelli.',
  'Store boliger med privat basseng og hage, ved siden av et vernet dynesystem på kysten av Marbella.',
  'Stora bostäder med egen pool och trädgård, intill ett skyddat dynsystem vid Marbellas kust.')
a('.why.points[0][1]',
  'Compradores que buscan una vivienda nueva y amplia en Marbella con piscina y jardín privados, junto a un sistema dunar protegido y a la playa, para vivir o como segunda residencia.',
  'Acheteurs qui recherchent un grand logement neuf à Marbella avec piscine et jardin privés, à côté d’un système dunaire protégé et de la plage, pour y vivre ou comme résidence secondaire.',
  'Käufer, die in Marbella eine große neue Immobilie mit privatem Pool und Garten suchen, neben einem geschützten Dünensystem und dem Strand, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужно просторное новое жильё в Марбелье с собственным бассейном и садом, рядом с охраняемой системой дюн и пляжем, — для постоянного проживания или как вторая недвижимость.',
  'مشترون يريدون مسكنًا جديدًا واسعًا في ماربيا بمسبح وحديقة خاصين، بجوار نظام كثبان رملية محمي والشاطئ، للإقامة أو كمسكن ثانٍ.',
  'Kopers die een grote nieuwe woning in Marbella zoeken met een privézwembad en een tuin, naast een beschermd duinsysteem en het strand, om er te wonen of als tweede woning.',
  'Kupujący, którzy szukają dużego nowego lokalu w Marbelli z prywatnym basenem i ogrodem, obok chronionego systemu wydm i plaży, do zamieszkania lub jako druga nieruchomość.',
  'Kjøpere som ønsker en stor ny bolig i Marbella med privat basseng og hage, ved siden av et vernet dynesystem og stranden, til å bo i eller som feriebolig.',
  'Köpare som vill ha en stor ny bostad i Marbella med egen pool och trädgård, intill ett skyddat dynsystem och stranden, för att bo i eller som andra bostad.')
a('.why.points[1][1]',
  'Viviendas de 447,13 y 483,98 m² construidos, cada una con sótano, garaje privado para dos coches, sala multiusos y piscina privada, en un complejo que el folleto describe con spa, gimnasios, un espacio de coworking y un lounge en la azotea.',
  'Des logements de 447,13 et 483,98 m² construits, chacun avec sous-sol, garage privé pour deux voitures, salle polyvalente et piscine privée, dans un ensemble que la brochure décrit avec spa, salles de sport, espace de coworking et lounge sur le toit.',
  'Immobilien mit 447,13 und 483,98 m² Baufläche, jeweils mit Untergeschoss, privater Garage für zwei Autos, Mehrzweckraum und privatem Pool, in einer Anlage, die die Broschüre mit Spa, Fitnessräumen, einem Coworking-Bereich und einer Rooftop-Lounge beschreibt.',
  'Объекты площадью застройки 447,13 и 483,98 м², у каждого — подвальный этаж, частный гараж на две машины, многофункциональный зал и собственный бассейн, в комплексе, который в брошюре описан со спа, тренажёрными залами, коворкингом и лаунжем на крыше.',
  'مسكنان بمساحة مبنية 447.13 و483.98 م²، لكلٍّ منهما طابق سفلي ومرآب خاص لسيارتين وقاعة متعددة الاستعمالات ومسبح خاص، في مجمّع يصفه الكتيّب بمنتجع صحي وصالات رياضية ومساحة عمل مشترك وصالة على السطح.',
  'Woningen van 447,13 en 483,98 m² bebouwd, elk met een kelder, een privégarage voor twee auto’s, een multifunctionele ruimte en een privézwembad, in een complex dat de brochure beschrijft met een spa, fitnessruimten, een coworkingruimte en een lounge op het dak.',
  'Lokale o powierzchni zabudowy 447,13 i 483,98 m², każdy z piwnicą, prywatnym garażem na dwa samochody, salą wielofunkcyjną i prywatnym basenem, w kompleksie, który broszura opisuje ze spa, siłowniami, przestrzenią coworkingową i lounge’em na dachu.',
  'Boliger på 447,13 og 483,98 m² bebygd, begge med kjeller, privat garasje for to biler, et flerbruksrom og privat basseng, i et anlegg som brosjyren beskriver med spa, treningsrom, en coworking-sone og en lounge på taket.',
  'Bostäder på 447,13 och 483,98 m² byggyta, båda med källare, privat garage för två bilar, ett flerfunktionsrum och egen pool, i ett område som broschyren beskriver med spa, gym, en coworkingyta och en lounge på taket.')
a('.why.points[2][1]',
  'El folleto sitúa el complejo junto a El Barronal de la Morena, un sistema dunar de unos 36.000 m² y 200 m de longitud, paralelo a la playa, y muestra en un mapa de ubicación el centro de Marbella, Puerto Banús y campos de golf. No da distancias.',
  'La brochure situe l’ensemble à côté d’El Barronal de la Morena, un système dunaire d’environ 36 000 m² et de 200 m de long, parallèle à la plage, et montre sur une carte de situation le centre de Marbella, Puerto Banús et des golfs. Elle ne donne aucune distance.',
  'Die Broschüre verortet die Anlage neben El Barronal de la Morena, einem Dünensystem von etwa 36.000 m² und 200 m Länge parallel zum Strand, und zeigt auf einer Lagekarte das Zentrum von Marbella, Puerto Banús und Golfplätze. Entfernungen nennt sie nicht.',
  'В брошюре комплекс расположен рядом с Эль-Баррональ-де-ла-Морена — системой дюн площадью около 36 000 м² и длиной 200 м вдоль пляжа; на карте местоположения показаны центр Марбельи, Пуэрто-Банус и поля для гольфа. Расстояния не указаны.',
  'يضع الكتيّب المجمّع بجوار «إل بارونال دي لا مورينا»، وهو نظام كثبان رملية بمساحة نحو 36,000 م² وطول 200 م موازٍ للشاطئ، ويُظهر على خريطة الموقع وسط ماربيا وبويرتو بانوس وملاعب غولف. ولا يذكر مسافات.',
  'De brochure plaatst het complex naast El Barronal de la Morena, een duinsysteem van ongeveer 36.000 m² en 200 m lang, evenwijdig aan het strand, en toont op een locatiekaart het centrum van Marbella, Puerto Banús en golfbanen. Afstanden noemt ze niet.',
  'Broszura umiejscawia kompleks obok El Barronal de la Morena, systemu wydm o powierzchni około 36 000 m² i długości 200 m, równoległego do plaży, a na mapie lokalizacji pokazuje centrum Marbelli, Puerto Banús i pola golfowe. Nie podaje odległości.',
  'Brosjyren plasserer anlegget ved siden av El Barronal de la Morena, et dynesystem på omtrent 36 000 m² og 200 m langt, parallelt med stranden, og viser sentrum av Marbella, Puerto Banús og golfbaner på et lokaliseringskart. Den oppgir ingen avstander.',
  'Broschyren placerar området intill El Barronal de la Morena, ett dynsystem på cirka 36 000 m² och 200 m långt, parallellt med stranden, och visar Marbellas centrum, Puerto Banús och golfbanor på en lägeskarta. Den anger inga avstånd.')
a('.why.points[3][1]',
  'La lista del 29 de octubre de 2026 recoge las dos viviendas como disponibles, pero la lista de precios del 1 de julio de 2026 marcaba la Nr. 04 como reservada. El folleto es de 2024 y ningún documento indica una fecha de entrega, así que confirmamos la disponibilidad, el estado de las obras y la fecha antes de cualquier reserva.',
  'La liste du 29 octobre 2026 présente les deux logements comme disponibles, mais la liste de prix du 1er juillet 2026 marquait la Nr. 04 comme réservée. La brochure date de 2024 et aucun document ne donne de date de livraison ; nous confirmons donc la disponibilité, l’état d’avancement du chantier et la date avant toute réservation.',
  'Die Liste vom 29. Oktober 2026 zeigt beide Immobilien als verfügbar, doch die Preisliste vom 1. Juli 2026 kennzeichnete Nr. 04 als reserviert. Die Broschüre stammt von 2024 und kein Dokument nennt einen Fertigstellungstermin, deshalb bestätigen wir Verfügbarkeit, Baufortschritt und Termin vor jeder Reservierung.',
  'В списке от 29 октября 2026 года оба объекта значатся доступными, но в прайс-листе от 1 июля 2026 года Nr. 04 была отмечена как забронированная. Брошюра датирована 2024 годом, и ни в одном документе не указан срок сдачи, поэтому перед любым бронированием мы подтверждаем наличие, стадию строительства и дату.',
  'تُظهر قائمة 29 أكتوبر 2026 المسكنين كمتاحين، لكن قائمة الأسعار بتاريخ 1 يوليو 2026 كانت تضع Nr. 04 كمحجوزة. الكتيّب من عام 2024 ولا تذكر أي وثيقة موعدًا للتسليم، لذلك نؤكد التوفر ومرحلة الأعمال والموعد قبل أي حجز.',
  'De lijst van 29 oktober 2026 toont beide woningen als beschikbaar, maar de prijslijst van 1 juli 2026 markeerde Nr. 04 als gereserveerd. De brochure is van 2024 en geen enkel document noemt een opleveringsdatum, dus wij bevestigen de beschikbaarheid, de bouwfase en de datum vóór elke reservering.',
  'Lista z 29 października 2026 r. pokazuje oba lokale jako dostępne, ale cennik z 1 lipca 2026 r. oznaczał Nr. 04 jako zarezerwowany. Broszura pochodzi z 2024 r., a żaden dokument nie podaje terminu oddania, dlatego przed każdą rezerwacją potwierdzamy dostępność, etap prac i termin.',
  'Listen fra 29. oktober 2026 viser begge boligene som ledige, men prislisten fra 1. juli 2026 markerte Nr. 04 som reservert. Brosjyren er fra 2024, og ingen dokumenter oppgir en overleveringsdato, så vi bekrefter tilgjengelighet, byggestadium og dato før enhver reservasjon.',
  'Listan från den 29 oktober 2026 visar båda bostäderna som lediga, men prislistan från den 1 juli 2026 markerade Nr. 04 som reserverad. Broschyren är från 2024 och inget dokument anger ett leveransdatum, så vi bekräftar tillgänglighet, byggstadium och datum före varje reservation.')
a('.architecture.headlineHtml', 'Líneas contemporáneas, <em>junto al mar</em>', 'Des lignes contemporaines, <em>à côté de la mer</em>', 'Zeitgenössische Linien, <em>direkt am Meer</em>',
  'Современные линии <em>рядом с морем</em>', 'خطوط معاصرة <em>بجوار البحر</em>', 'Eigentijdse lijnen, <em>naast de zee</em>', 'Współczesne linie, <em>obok morza</em>', 'Moderne linjer, <em>ved havet</em>', 'Moderna linjer, <em>intill havet</em>')
a('.architecture.copy[0]',
  'El folleto describe un complejo contemporáneo de villas pareadas y apartamentos con grandes terrazas, en jardines escalonados que descienden hacia el mar, con vegetación autóctona de bajo consumo de agua, estanques y pequeñas cascadas.',
  'La brochure décrit un ensemble contemporain de villas jumelées et d’appartements avec de grandes terrasses, dans des jardins en terrasses qui descendent vers la mer, avec une végétation locale peu gourmande en eau, des bassins et de petites cascades.',
  'Die Broschüre beschreibt eine zeitgenössische Anlage aus Doppelhaushälften und Wohnungen mit großen Terrassen, in terrassierten Gärten, die zum Meer hin abfallen, mit heimischer, wassersparender Bepflanzung, Teichen und kleinen Wasserfällen.',
  'В брошюре описан современный комплекс из парных домов и квартир с большими террасами, в террасных садах, спускающихся к морю, с местными растениями, не требующими много воды, прудами и небольшими водопадами.',
  'يصف الكتيّب مجمّعًا معاصرًا من الفلل شبه المنفصلة والشقق بتراسات واسعة، في حدائق مدرّجة تنحدر نحو البحر، بنباتات محلية قليلة استهلاك المياه وبرك وشلالات صغيرة.',
  'De brochure beschrijft een eigentijds complex met halfvrijstaande villa’s en appartementen met grote terrassen, in terrasvormige tuinen die naar de zee aflopen, met inheemse, waterzuinige beplanting, vijvers en kleine watervallen.',
  'Broszura opisuje współczesny kompleks domów bliźniaczych i apartamentów z dużymi tarasami, w tarasowych ogrodach opadających ku morzu, z rodzimą, mało wymagającą wody roślinnością, stawami i niewielkimi wodospadami.',
  'Brosjyren beskriver et moderne anlegg med tomannsvillaer og leiligheter med store terrasser, i terrasserte hager som skråner ned mot havet, med stedegen, vannsparende beplantning, dammer og små fossefall.',
  'Broschyren beskriver ett modernt område med parhus och lägenheter med stora terrasser, i terrasserade trädgårdar som sluttar ned mot havet, med inhemsk, vattensnål växtlighet, dammar och små vattenfall.')
a('.architecture.copy[1]',
  'Según sus planos, la villa Nr. 04 tiene cuatro niveles: sótano, planta baja, primera planta y un solárium con una piscina de 23,18 m². El apartamento Nr. 202 tiene sótano y planta baja, con una terraza de 146,70 m², un jardín de 79,46 m² y una piscina de 34,84 m².',
  'D’après ses plans, la villa Nr. 04 compte quatre niveaux : un sous-sol, un rez-de-chaussée, un premier étage et un solarium avec une piscine de 23,18 m². L’appartement Nr. 202 compte un sous-sol et un rez-de-chaussée, avec une terrasse de 146,70 m², un jardin de 79,46 m² et une piscine de 34,84 m².',
  'Nach ihren Plänen hat die Villa Nr. 04 vier Ebenen: ein Untergeschoss, ein Erdgeschoss, ein erstes Obergeschoss und ein Solarium mit einem Pool von 23,18 m². Die Wohnung Nr. 202 hat ein Untergeschoss und ein Erdgeschoss, mit einer Terrasse von 146,70 m², einem Garten von 79,46 m² und einem Pool von 34,84 m².',
  'По планам вилла Nr. 04 имеет четыре уровня: подвальный этаж, первый этаж, второй этаж и солярий с бассейном 23,18 м². Квартира Nr. 202 занимает подвальный и первый этажи: терраса 146,70 м², сад 79,46 м² и бассейн 34,84 м².',
  'وفق مخططاتها، للفيلا Nr. 04 أربعة مستويات: طابق سفلي وطابق أرضي وطابق أول وسولاريوم بمسبح مساحته 23.18 م². وللشقة Nr. 202 طابق سفلي وطابق أرضي، مع تراس مساحته 146.70 م² وحديقة مساحتها 79.46 م² ومسبح مساحته 34.84 م².',
  'Volgens de plattegronden heeft villa Nr. 04 vier niveaus: een kelder, een begane grond, een eerste verdieping en een solarium met een zwembad van 23,18 m². Appartement Nr. 202 heeft een kelder en een begane grond, met een terras van 146,70 m², een tuin van 79,46 m² en een zwembad van 34,84 m².',
  'Według rzutów willa Nr. 04 ma cztery poziomy: piwnicę, parter, pierwsze piętro i solarium z basenem o powierzchni 23,18 m². Mieszkanie Nr. 202 ma piwnicę i parter, z tarasem o powierzchni 146,70 m², ogrodem o powierzchni 79,46 m² i basenem o powierzchni 34,84 m².',
  'Ifølge plantegningene har villa Nr. 04 fire plan: en kjeller, en første etasje, en andre etasje og en solterrasse med et basseng på 23,18 m². Leilighet Nr. 202 har en kjeller og en første etasje, med en terrasse på 146,70 m², en hage på 79,46 m² og et basseng på 34,84 m².',
  'Enligt planritningarna har villa Nr. 04 fyra plan: en källare, en bottenvåning, en första våning och en solterrass med en pool på 23,18 m². Lägenhet Nr. 202 har en källare och en bottenvåning, med en terrass på 146,70 m², en trädgård på 79,46 m² och en pool på 34,84 m².')

a('.architecture.highlights[0][1]',
  'Revoco exterior sobre un sistema de aislamiento térmico y acústico, con acabado de mortero pintado, revestimiento compuesto en las caras verticales de las primeras plantas y voladizos revestidos con paneles prefabricados de resina mineral.',
  'Enduit extérieur sur un système d’isolation thermique et acoustique, avec une finition en mortier peint, un revêtement composite sur les faces verticales des premiers étages et des débords habillés de panneaux préfabriqués en résine minérale.',
  'Außenputz auf einem Wärme- und Schalldämmsystem mit gestrichener Mörtelfinish, Verbundverkleidung an den senkrechten Flächen der ersten Obergeschosse und Dachüberständen mit vorgefertigten Mineralharzplatten.',
  'Наружная штукатурка по системе тепло- и звукоизоляции с окрашенной растворной отделкой, композитная облицовка вертикальных поверхностей вторых этажей и свесы, облицованные сборными панелями из минеральной смолы.',
  'بياض خارجي فوق نظام عزل حراري وصوتي بتشطيب من الملاط المطلي، وكسوة مركّبة على الواجهات العمودية للطوابق الأولى، وبروزات مكسوة بألواح جاهزة من الراتنج المعدني.',
  'Buitenpleisterwerk op een thermisch en akoestisch isolatiesysteem met een geschilderde mortelafwerking, composietbekleding op de verticale vlakken van de eerste verdiepingen en overstekken bekleed met geprefabriceerde mineraalharspanelen.',
  'Tynk zewnętrzny na systemie izolacji termicznej i akustycznej z malowanym wykończeniem zaprawą, okładziną kompozytową na pionowych płaszczyznach pierwszych pięter oraz okapami wykończonymi prefabrykowanymi panelami z żywicy mineralnej.',
  'Utvendig puss på et system for varme- og lydisolering med malt mørtelfinish, komposittkledning på de loddrette flatene i første etasje og takutstikk kledd med prefabrikkerte mineralharpiksplater.',
  'Utvändig puts på ett system för värme- och ljudisolering med målad murbruksyta, kompositbeklädnad på de lodräta ytorna på första våningarna och takutsprång klädda med prefabricerade mineralhartspaneler.')
a('.architecture.highlights[1][1]',
  'Perfiles de aluminio con rotura de puente térmico, doble acristalamiento de control solar y baja emisividad, y ventanas de suelo a techo, con la carpintería enrasada con el suelo en los salones.',
  'Menuiseries en aluminium à rupture de pont thermique, double vitrage à contrôle solaire et basse émissivité, et fenêtres du sol au plafond, avec des cadres encastrés au ras du sol dans les séjours.',
  'Aluminiumrahmen mit thermischer Trennung, Doppelverglasung mit Sonnenschutz und niedriger Emissivität sowie raumhohe Fenster, in den Wohnzimmern mit bodenbündigen Rahmen.',
  'Алюминиевые рамы с терморазрывом, двойное остекление с солнцезащитным и низкоэмиссионным покрытием и окна от пола до потолка; в гостиных рамы заподлицо с полом.',
  'إطارات ألومنيوم بقاطع حراري، وزجاج مزدوج للتحكم بالشمس ومنخفض الانبعاثية، ونوافذ من الأرضية إلى السقف، مع إطارات مستوية مع الأرضية في غرف الجلوس.',
  'Aluminium kozijnen met thermische onderbreking, dubbele beglazing met zonwerende en laag-emissiecoating en ramen van vloer tot plafond, met in de woonkamers kozijnen die gelijk met de vloer liggen.',
  'Aluminiowe ramy z przerwą termiczną, podwójne szyby z powłoką przeciwsłoneczną i niskoemisyjną oraz okna od podłogi do sufitu, w salonach z ramami zlicowanymi z podłogą.',
  'Aluminiumsrammer med termisk brudd, dobbeltglass med solkontroll og lav emisjon og vinduer fra gulv til tak, med rammer i flukt med gulvet i stuene.',
  'Aluminiumbågar med köldbrygga, dubbla glas med solskydd och låg emissivitet och fönster från golv till tak, med bågar i nivå med golvet i vardagsrummen.')
a('.architecture.highlights[2][1]',
  'Baldosas de gres porcelánico antideslizante de gran formato a juego con el interior, pérgolas y cubiertas de aluminio o material compuesto efecto madera, y barandillas de vidrio laminado de seguridad.',
  'Grandes carreaux de grès cérame antidérapants assortis à l’intérieur, pergolas et toitures en aluminium ou composite aspect bois, et garde-corps en verre feuilleté de sécurité.',
  'Großformatige rutschhemmende Feinsteinzeugfliesen passend zum Innenbereich, Pergolen und Überdachungen aus Aluminium oder Verbundmaterial in Holzoptik sowie Geländer aus Verbundsicherheitsglas.',
  'Крупноформатная нескользящая керамогранитная плитка в тон интерьеру, перголы и навесы из алюминия или композита под дерево и ограждения из многослойного безопасного стекла.',
  'بلاط بورسلين كبير الحجم مانع للانزلاق ينسجم مع الداخل، وبرغولات وأسقف من الألومنيوم أو المواد المركبة بمظهر الخشب، ودرابزينات من الزجاج المصفّح الآمن.',
  'Antislip porseleinen tegels in groot formaat die bij het interieur passen, pergola’s en daken van aluminium of composiet in houtlook en balustrades van gelaagd veiligheidsglas.',
  'Wielkoformatowe antypoślizgowe płytki gresowe pasujące do wnętrz, pergole i zadaszenia z aluminium lub kompozytu w kolorze drewna oraz balustrady ze szkła laminowanego bezpiecznego.',
  'Sklisikre porselensfliser i stort format som matcher interiøret, pergolaer og tak i aluminium eller kompositt i trelook og rekkverk i laminert sikkerhetsglass.',
  'Halksäkra porslinsplattor i stort format som matchar interiören, pergolor och tak i aluminium eller kompositmaterial i trälook och räcken i laminerat säkerhetsglas.')
a('.architecture.highlights[3][1]',
  'Cloración salina en las piscinas y los jacuzzis, tarima tecnológica en las plataformas de piscina y jacuzzi, y revestimiento de gres porcelánico en el vaso de la piscina.',
  'Chloration saline dans les piscines et les jacuzzis, decking technique sur les plateformes de piscine et de jacuzzi, et revêtement en grès cérame dans le bassin.',
  'Salzwasserchlorierung in den Pools und Whirlpools, technisches Decking auf den Pool- und Whirlpoolplattformen und Feinsteinzeugverkleidung im Poolbecken.',
  'Солевая хлорация в бассейнах и джакузи, технологический декинг на площадках у бассейнов и джакузи и облицовка чаши бассейна керамогранитом.',
  'معالجة المياه بالكلور الملحي في المسابح والجاكوزي، وأرضية تكنولوجية على منصات المسابح والجاكوزي، وكسوة من البورسلين لحوض المسبح.',
  'Zoutwaterchlorering in de zwembaden en jacuzzi’s, technisch decking op de zwembad- en jacuzziplatforms en een bekleding van porselein in het zwembadbassin.',
  'Chlorowanie solne w basenach i jacuzzi, technologiczny decking na platformach basenów i jacuzzi oraz okładzina z gresu na dnie i ścianach niecki basenu.',
  'Saltvannsklorering i bassengene og jacuzziene, teknisk dekk på basseng- og jacuzziplattformene og porselensfliser i bassengkaret.',
  'Saltklorering i poolerna och jacuzzierna, tekniskt däck på pool- och jacuzziplattformarna och porslinsplattor i poolbassängen.')

# ---- quality specification -------------------------------------------------------------------------

a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades de los documentos del promotor, fechada el 7 de agosto de 2024. Indica que la memoria y sus imágenes son orientativas, que el promotor puede modificar elementos por razones técnicas o legales y sustituirlos por otros de calidad similar, y que el mobiliario, la decoración y los electrodomésticos que no describe no están incluidos. Abarca villas y apartamentos, y algunos elementos dependen del tipo, por lo que confirmamos cuáles corresponden a la vivienda que usted elija.',
  'Source : le descriptif des prestations des documents du promoteur, daté du 7 août 2024. Il précise que le descriptif et ses images sont indicatifs, que le promoteur peut modifier des éléments pour des raisons techniques ou légales et les remplacer par d’autres de qualité similaire, et que le mobilier, la décoration et l’électroménager qu’il ne décrit pas ne sont pas inclus. Il couvre les villas et les appartements, et certains éléments dépendent du type ; nous confirmons donc lesquels s’appliquent au logement que vous choisissez.',
  'Quelle: die Baubeschreibung in den Unterlagen des Bauträgers, datiert auf den 7. August 2024. Sie besagt, dass die Baubeschreibung und ihre Bilder unverbindlich sind, dass der Bauträger aus technischen oder rechtlichen Gründen Positionen ändern und durch gleichwertige ersetzen darf und dass Möbel, Dekoration und Geräte, die sie nicht beschreibt, nicht enthalten sind. Sie gilt für Villen und Wohnungen, und einige Positionen hängen vom Typ ab; wir bestätigen daher, welche für die von Ihnen gewählte Immobilie gelten.',
  'Источник: спецификация качества из документов застройщика, датированная 7 августа 2024 года. В ней сказано, что спецификация и её изображения носят ориентировочный характер, что застройщик вправе по техническим или юридическим причинам менять позиции, заменяя их равноценными, и что мебель, декор и техника, которые в ней не описаны, не входят в комплектацию. Она охватывает виллы и квартиры, а некоторые позиции зависят от типа, поэтому мы подтверждаем, какие из них относятся к выбранному вами жилью.',
  'المصدر: مواصفات الجودة في وثائق المطوّر، المؤرّخة في 7 أغسطس 2024. وهي تنصّ على أن المواصفات وصورها استرشادية، وأن للمطوّر أن يغيّر بنودًا لأسباب تقنية أو قانونية ويستبدلها ببنود مماثلة في الجودة، وأن الأثاث والديكور والأجهزة التي لا تصفها غير مشمولة. وهي تشمل الفلل والشقق، وبعض البنود تتوقف على النوع، لذلك نؤكد أيها ينطبق على المسكن الذي تختاره.',
  'Bron: de kwaliteitsomschrijving in de documenten van de ontwikkelaar, gedateerd 7 augustus 2024. Daarin staat dat de omschrijving en de beelden richtinggevend zijn, dat de ontwikkelaar om technische of juridische redenen onderdelen mag wijzigen en door gelijkwaardige mag vervangen, en dat meubilair, inrichting en apparatuur die niet worden omschreven niet zijn inbegrepen. Ze geldt voor villa’s en appartementen, en sommige onderdelen hangen af van het type, dus wij bevestigen welke gelden voor de woning die u kiest.',
  'Źródło: opis standardu wykończenia w dokumentach dewelopera, z datą 7 sierpnia 2024 r. Zastrzega on, że opis i jego obrazy mają charakter orientacyjny, że deweloper może z przyczyn technicznych lub prawnych zmieniać elementy i zastępować je równorzędnymi oraz że meble, wystrój i sprzęt, których nie opisuje, nie wchodzą w cenę. Obejmuje wille i apartamenty, a niektóre elementy zależą od typu, dlatego potwierdzamy, które dotyczą wybranego lokalu.',
  'Kilde: kvalitetsbeskrivelsen i utbyggerens dokumenter, datert 7. august 2024. Den sier at beskrivelsen og bildene er veiledende, at utbyggeren av tekniske eller juridiske grunner kan endre elementer og erstatte dem med likeverdige, og at møbler, innredning og hvitevarer den ikke beskriver ikke er inkludert. Den gjelder villaer og leiligheter, og noen elementer avhenger av typen, så vi bekrefter hvilke som gjelder for boligen dere velger.',
  'Källa: kvalitetsbeskrivningen i exploatörens dokument, daterad den 7 augusti 2024. Den anger att beskrivningen och bilderna är vägledande, att exploatören av tekniska eller juridiska skäl får ändra delar och ersätta dem med likvärdiga, och att möbler, inredning och vitvaror som den inte beskriver inte ingår. Den gäller villor och lägenheter, och vissa delar beror på typen, så vi bekräftar vilka som gäller för bostaden ni väljer.')
a('.qualitySpecs.groups[0].items[0]',
  'Baldosas de gres porcelánico de gran formato de 120 x 120 cm en toda la vivienda y el sótano, con rodapié de aluminio antracita empotrado en la pared, y gres porcelánico rectificado de 60 x 60 cm u hormigón pulido en el garaje privado, según el tipo.',
  'Carreaux de grès cérame grand format de 120 x 120 cm dans tout le logement et le sous-sol, avec une plinthe en aluminium anthracite encastrée dans le mur, et grès cérame rectifié de 60 x 60 cm ou béton poli dans le garage privé, selon le type.',
  'Großformatige Feinsteinzeugfliesen von 120 x 120 cm im gesamten Haus und im Untergeschoss, mit einer in die Wand eingelassenen anthrazitfarbenen Aluminiumsockelleiste, und rektifiziertes Feinsteinzeug von 60 x 60 cm oder polierter Beton in der privaten Garage, je nach Typ.',
  'Крупноформатная керамогранитная плитка 120 x 120 см во всём доме и в подвальном этаже, с антрацитовым алюминиевым плинтусом, встроенным в стену, а в частном гараже — ректифицированный керамогранит 60 x 60 см или полированный бетон, в зависимости от типа.',
  'بلاط بورسلين كبير الحجم 120 × 120 سم في المنزل كله والطابق السفلي، مع وزرة من الألومنيوم بلون الأنثراسيت مدمجة في الجدار، وبورسلين مقصوص 60 × 60 سم أو خرسانة مصقولة في المرآب الخاص، بحسب النوع.',
  'Porseleintegels in groot formaat van 120 x 120 cm in de hele woning en de kelder, met een antracietkleurige aluminium plint die in de wand is ingewerkt, en gerectificeerd porselein van 60 x 60 cm of gepolijst beton in de privégarage, afhankelijk van het type.',
  'Wielkoformatowe płytki gresowe 120 x 120 cm w całym domu i w piwnicy, z antracytową aluminiową listwą przypodłogową wpuszczoną w ścianę, oraz rektyfikowany gres 60 x 60 cm lub polerowany beton w prywatnym garażu, zależnie od typu.',
  'Porselensfliser i stort format på 120 x 120 cm i hele boligen og kjelleren, med en antrasittfarget gulvlist i aluminium som er felt inn i veggen, og rektifisert porselen på 60 x 60 cm eller polert betong i den private garasjen, avhengig av typen.',
  'Porslinsplattor i stort format på 120 x 120 cm i hela bostaden och källaren, med en antracitfärgad golvlist av aluminium som är infälld i väggen, och rektifierat porslin på 60 x 60 cm eller polerad betong i det privata garaget, beroende på typ.')
a('.qualitySpecs.groups[0].items[1]',
  'Falsos techos de yeso laminado en toda la vivienda, techos con cajón y esquinas redondeadas en el salón y el dormitorio principal, y cortineros en las ventanas que dan al exterior.',
  'Faux plafonds en plaques de plâtre dans tout le logement, plafonds à caisson aux angles arrondis dans le séjour et la chambre principale, et cache-rideaux aux fenêtres donnant sur l’extérieur.',
  'Abgehängte Decken aus Gipskarton im gesamten Haus, Voutendecken mit abgerundeten Ecken im Wohnzimmer und im Hauptschlafzimmer sowie Gardinenblenden an den Fenstern zur Außenseite.',
  'Подвесные потолки из гипсокартона во всём доме, потолки с нишей и скруглёнными углами в гостиной и главной спальне и карнизные ниши на окнах, выходящих наружу.',
  'أسقف معلّقة من ألواح الجبس في المنزل كله، وأسقف بتجويف وزوايا مستديرة في غرفة الجلوس وغرفة النوم الرئيسية، وصناديق ستائر على النوافذ المطلة إلى الخارج.',
  'Verlaagde plafonds van gipsplaten in de hele woning, plafonds met een verdiepte rand en afgeronde hoeken in de woonkamer en de hoofdslaapkamer, en gordijnkokers boven de ramen aan de buitenzijde.',
  'Sufity podwieszane z płyt gipsowo-kartonowych w całym domu, sufity kasetonowe z zaokrąglonymi narożnikami w salonie i sypialni głównej oraz karnisze ukryte nad oknami wychodzącymi na zewnątrz.',
  'Nedforede himlinger i gipsplater i hele boligen, himlinger med forsenket felt og avrundede hjørner i stuen og hovedsoverommet, og gardinbokser ved vinduene mot utsiden.',
  'Undertak av gipsskivor i hela bostaden, undertak med nedsänkt fält och rundade hörn i vardagsrummet och huvudsovrummet, och gardinkappor vid fönstren mot utsidan.')
a('.qualitySpecs.groups[1].items[0]',
  'Perfiles de aluminio Cortizo con rotura de puente térmico y doble acristalamiento de control solar, de suelo a techo, con la carpintería enrasada con el suelo en los salones, y persianas automáticas de seguridad en los dormitorios traseros.',
  'Menuiseries en aluminium Cortizo à rupture de pont thermique et double vitrage à contrôle solaire, du sol au plafond, avec des cadres au ras du sol dans les séjours, et des stores de sécurité automatiques dans les chambres côté arrière.',
  'Aluminiumrahmen von Cortizo mit thermischer Trennung und Doppelverglasung mit Sonnenschutz, raumhoch, in den Wohnzimmern mit bodenbündigen Rahmen, sowie automatische Sicherheitsrollläden in den rückwärtigen Schlafzimmern.',
  'Алюминиевые рамы Cortizo с терморазрывом и двойное остекление с солнцезащитным покрытием от пола до потолка, в гостиных рамы заподлицо с полом, и автоматические защитные жалюзи в задних спальнях.',
  'إطارات ألومنيوم من Cortizo بقاطع حراري وزجاج مزدوج للتحكم بالشمس من الأرضية إلى السقف، مع إطارات مستوية مع الأرضية في غرف الجلوس، وستائر أمان آلية في غرف النوم الخلفية.',
  'Aluminium kozijnen van Cortizo met thermische onderbreking en dubbele beglazing met zonwering, van vloer tot plafond, in de woonkamers met kozijnen gelijk met de vloer, en automatische veiligheidsrolluiken in de achterste slaapkamers.',
  'Aluminiowe ramy Cortizo z przerwą termiczną i podwójnymi szybami z powłoką przeciwsłoneczną od podłogi do sufitu, w salonach zlicowane z podłogą, oraz automatyczne rolety bezpieczeństwa w tylnych sypialniach.',
  'Aluminiumsrammer fra Cortizo med termisk brudd og dobbeltglass med solkontroll, fra gulv til tak, i stuene med rammer i flukt med gulvet, og automatiske sikkerhetsrullegardiner i soverommene på baksiden.',
  'Aluminiumbågar från Cortizo med köldbrygga och dubbla glas med solskydd, från golv till tak, i vardagsrummen med bågar i nivå med golvet, och automatiska säkerhetsrullgardiner i sovrummen på baksidan.')
a('.qualitySpecs.groups[2].items[0]',
  'Puerta de entrada de roble blanco de al menos 2,50 m de altura, con apertura por lector de huella dactilar, y puertas interiores hasta el techo, de al menos 2,50 m de altura en las plantas superiores.',
  'Porte d’entrée en chêne blanc d’au moins 2,50 m de haut, avec ouverture par lecteur d’empreintes digitales, et portes intérieures jusqu’au plafond, d’au moins 2,50 m de haut aux étages.',
  'Eine Haustür aus Weißeiche von mindestens 2,50 m Höhe mit Fingerabdruck-Öffnung und raumhohe Innentüren, in den oberen Geschossen mindestens 2,50 m hoch.',
  'Входная дверь из белого дуба высотой не менее 2,50 м с открыванием по отпечатку пальца и межкомнатные двери до потолка, на верхних этажах высотой не менее 2,50 м.',
  'باب مدخل من البلوط الأبيض بارتفاع لا يقل عن 2.50 م يُفتح ببصمة الإصبع، وأبواب داخلية حتى السقف بارتفاع لا يقل عن 2.50 م في الطوابق العليا.',
  'Een voordeur van wit eikenhout van minstens 2,50 m hoog, met vingerafdrukopening, en binnendeuren tot aan het plafond, op de bovenverdiepingen minstens 2,50 m hoog.',
  'Drzwi wejściowe z białego dębu o wysokości co najmniej 2,50 m, otwierane czytnikiem linii papilarnych, oraz drzwi wewnętrzne do sufitu, na wyższych kondygnacjach o wysokości co najmniej 2,50 m.',
  'En ytterdør i hvit eik på minst 2,50 m i høyden, med åpning med fingeravtrykkleser, og innvendige dører helt opp til taket, på minst 2,50 m i høyden i etasjene over.',
  'En ytterdörr i vitek på minst 2,50 m i höjd, med öppning med fingeravtrycksläsare, och innerdörrar ända upp till taket, minst 2,50 m höga på de övre våningarna.')
a('.qualitySpecs.groups[2].items[1]',
  'Armarios forrados por dentro, con cajones, baldas, barra para colgar e iluminación LED con sensor de apertura, y puertas de cristal ahumado en el dormitorio principal.',
  'Placards doublés à l’intérieur, avec tiroirs, étagères, tringle et éclairage LED à détecteur d’ouverture, et portes en verre fumé dans la chambre principale.',
  'Innen ausgekleidete Einbauschränke mit Schubladen, Regalböden, Kleiderstange und LED-Beleuchtung mit Öffnungssensor sowie Rauchglastüren im Hauptschlafzimmer.',
  'Шкафы с внутренней отделкой, ящиками, полками, штангой для одежды и светодиодной подсветкой с датчиком открывания, а в главной спальне — двери из дымчатого стекла.',
  'خزائن مبطّنة من الداخل بأدراج ورفوف وقضيب تعليق وإضاءة LED بحساس فتح، وأبواب من الزجاج المدخّن في غرفة النوم الرئيسية.',
  'Van binnen bekleedde kasten met laden, planken, een kledingroede en ledverlichting met openingssensor, en rookglazen deuren in de hoofdslaapkamer.',
  'Szafy wykończone w środku, z szufladami, półkami, drążkiem na ubrania i oświetleniem LED z czujnikiem otwarcia, oraz drzwi ze szkła dymionego w sypialni głównej.',
  'Skap kledd innvendig, med skuffer, hyller, kleshenger og LED-belysning med åpningssensor, og røykglassdører på hovedsoverommet.',
  'Garderober klädda invändigt, med lådor, hyllor, klädstång och LED-belysning med öppningssensor, och rökglasdörrar i huvudsovrummet.')
a('.qualitySpecs.groups[3].items[0]',
  'En el baño principal, revestimiento de gres porcelánico de gran formato de suelo a techo; en el segundo baño, revestimiento de suelo a techo en las zonas húmedas y media altura con papel pintado o pintura en el resto.',
  'Dans la salle de bain principale, un carrelage grand format en grès cérame du sol au plafond ; dans la deuxième salle de bain, un carrelage du sol au plafond dans les zones humides et à mi-hauteur avec papier peint ou peinture ailleurs.',
  'Im Hauptbad großformatige Feinsteinzeugfliesen vom Boden bis zur Decke; im zweiten Bad raumhohe Fliesen in den Nassbereichen und halbhohe Fliesen mit Tapete oder Farbe an den übrigen Wänden.',
  'В главной ванной — крупноформатная керамогранитная плитка от пола до потолка; во второй ванной — плитка от пола до потолка в мокрых зонах и на половину высоты с обоями или краской на остальных стенах.',
  'في الحمام الرئيسي كسوة من البورسلين كبير الحجم من الأرضية إلى السقف، وفي الحمام الثاني كسوة من الأرضية إلى السقف في المناطق الرطبة وبنصف الارتفاع مع ورق جدران أو دهان في بقية الجدران.',
  'In de hoofdbadkamer porseleintegels in groot formaat van vloer tot plafond; in de tweede badkamer tegels van vloer tot plafond in de natte zones en tegels tot halve hoogte met behang of verf op de overige wanden.',
  'W łazience głównej wielkoformatowe płytki gresowe od podłogi do sufitu; w drugiej łazience płytki od podłogi do sufitu w strefach mokrych i do połowy wysokości z tapetą lub farbą na pozostałych ścianach.',
  'På hovedbadet porselensfliser i stort format fra gulv til tak; på det andre badet fliser fra gulv til tak i de våte sonene og fliser til halv høyde med tapet eller maling på de øvrige veggene.',
  'I huvudbadrummet porslinsplattor i stort format från golv till tak; i det andra badrummet plattor från golv till tak i de våta zonerna och plattor till halv höjd med tapet eller färg på övriga väggar.')
a('.qualitySpecs.groups[3].items[1]',
  'Bañera exenta de superficie sólida, inodoros y bidés suspendidos Duravit, con inodoro Sensowash solo en los baños principales, lavabos dobles de resina mineral en los baños principales, grifería negro mate con ducha termostática y ducha de mano, y espejo antivaho con iluminación trasera.',
  'Baignoire îlot en solid surface, WC et bidets suspendus Duravit, avec un WC Sensowash uniquement dans les salles de bain principales, doubles vasques en résine minérale dans les salles de bain principales, robinetterie noir mat avec douche thermostatique et douchette, et miroir antibuée rétroéclairé.',
  'Eine freistehende Badewanne aus Mineralwerkstoff, hängende Duravit-WCs und -Bidets mit einem Sensowash-WC nur in den Hauptbädern, Doppelwaschtische aus Mineralharz in den Hauptbädern, mattschwarze Armaturen mit Thermostat-Dusche und Handbrause sowie ein beschlagfreier Spiegel mit Hinterleuchtung.',
  'Отдельно стоящая ванна из искусственного камня, подвесные унитазы и биде Duravit, причём унитаз Sensowash — только в главных ванных, двойные раковины из минеральной смолы в главных ванных, матовые чёрные смесители с термостатическим душем и ручной лейкой и зеркало с подсветкой и защитой от запотевания.',
  'حوض استحمام قائم بذاته من المادة الصلبة، ومراحيض وبيديهات معلّقة من Duravit مع مرحاض Sensowash في الحمامات الرئيسية فقط، وأحواض مزدوجة من الراتنج المعدني في الحمامات الرئيسية، وحنفيات بلون أسود مطفأ مع دش بترموستات ودش يدوي، ومرآة مضادة للضباب بإضاءة خلفية.',
  'Een vrijstaand bad van solid surface, hangende toiletten en bidets van Duravit, met een Sensowash-toilet alleen in de hoofdbadkamers, dubbele wastafels van mineraalhars in de hoofdbadkamers, mat zwarte kranen met een thermostatische douche en een handdouche, en een antibeslagspiegel met achtergrondverlichting.',
  'Wolnostojąca wanna z materiału solid surface, wiszące toalety i bidety Duravit, z toaletą Sensowash tylko w łazienkach głównych, podwójne umywalki z żywicy mineralnej w łazienkach głównych, matowe czarne baterie z prysznicem termostatycznym i słuchawką prysznicową oraz lustro z podświetleniem i funkcją antypara.',
  'Et frittstående badekar i solid surface, hengende toaletter og bidet fra Duravit, med et Sensowash-toalett bare på hovedbadene, doble servanter i mineralharpiks på hovedbadene, matt svarte armaturer med termostatdusj og håndsprayer, og et speil med bakgrunnsbelysning mot dugg.',
  'Ett fristående badkar i solid surface, hängande toaletter och bidéer från Duravit, med en Sensowash-toalett bara i huvudbadrummen, dubbla handfat i mineralharts i huvudbadrummen, matt svarta blandare med termostatdusch och handdusch, och en spegel med bakgrundsbelysning mot imma.')
a('.qualitySpecs.groups[4].items[0]',
  'Muebles de cocina de melamina de clase E1 con frentes lacados mate de 20 mm y electrodomésticos Gaggenau serie 200: horno, microondas, placa de inducción con extracción integrada según el tipo, lavavajillas, frigorífico y congelador, con vinoteca.',
  'Meubles de cuisine en mélaminé de classe E1 avec façades laquées mates de 20 mm et électroménager Gaggenau série 200 : four, micro-ondes, plaque à induction avec extraction intégrée selon le type, lave-vaisselle, réfrigérateur et congélateur, avec cave à vin.',
  'Küchenmöbel aus Melamin der Klasse E1 mit mattlackierten Fronten von 20 mm und Gaggenau-Geräte der Serie 200: Backofen, Mikrowelle, Induktionskochfeld mit integriertem Abzug je nach Typ, Geschirrspüler, Kühlschrank und Gefrierschrank, dazu ein Weinkühlschrank.',
  'Кухонная мебель из меламина класса E1 с матовыми лакированными фасадами 20 мм и техника Gaggenau серии 200: духовой шкаф, микроволновая печь, индукционная варочная панель со встроенной вытяжкой (в зависимости от типа), посудомоечная машина, холодильник и морозильник, а также винный шкаф.',
  'وحدات مطبخ من الميلامين من الفئة E1 بواجهات مطلية بلاكر مطفأ بسماكة 20 مم، وأجهزة Gaggenau من السلسلة 200: فرن وميكروويف وموقد حثّي بشفاط مدمج بحسب النوع وغسالة صحون وثلاجة ومجمّد، مع ثلاجة للنبيذ.',
  'Keukenmeubels van melamine van klasse E1 met mat gelakte fronten van 20 mm en Gaggenau-apparatuur uit de 200-serie: een oven, een magnetron, een inductiekookplaat met geïntegreerde afzuiging naargelang het type, een vaatwasser, een koelkast en een vriezer, met een wijnkoeler.',
  'Meble kuchenne z melaminy klasy E1 z matowymi lakierowanymi frontami o grubości 20 mm oraz sprzęt Gaggenau serii 200: piekarnik, mikrofalówka, płyta indukcyjna ze zintegrowanym okapem zależnie od typu, zmywarka, lodówka i zamrażarka, a także chłodziarka do wina.',
  'Kjøkkenskap i melamin av klasse E1 med matt lakkerte fronter på 20 mm og Gaggenau-apparater i serie 200: en ovn, en mikrobølgeovn, en induksjonstopp med integrert ventilator avhengig av typen, en oppvaskmaskin, et kjøleskap og en fryser, med et vinskap.',
  'Köksluckor och skåp i melamin av klass E1 med mattlackerade fronter på 20 mm och Gaggenau-apparater i serie 200: en ugn, en mikrovågsugn, en induktionshäll med inbyggd fläkt beroende på typ, en diskmaskin, ett kylskåp och en frys, med ett vinkylskåp.')
a('.qualitySpecs.groups[4].items[1]',
  'Cocinas exteriores con encimera de gres porcelánico, fregadero de acero inoxidable y tomas de agua y electricidad, y un lavadero con secadora de bomba de calor y lavadora.',
  'Cuisines d’extérieur avec plan de travail en grès cérame, évier en acier inoxydable et prises d’eau et d’électricité, et une buanderie avec sèche-linge à pompe à chaleur et lave-linge.',
  'Außenküchen mit Arbeitsplatte aus Feinsteinzeug, Edelstahlspüle sowie Wasser- und Stromanschlüssen und ein Hauswirtschaftsraum mit Wärmepumpentrockner und Waschmaschine.',
  'Уличные кухни с керамогранитной столешницей, мойкой из нержавеющей стали и точками подключения воды и электричества, а также прачечная с сушильной машиной с тепловым насосом и стиральной машиной.',
  'مطابخ خارجية بسطح عمل من البورسلين وحوض من الفولاذ المقاوم للصدأ ونقاط مياه وكهرباء، وغرفة غسيل بمجفف بمضخة حرارية وغسالة.',
  'Buitenkeukens met een werkblad van porselein, een roestvrijstalen spoelbak en water- en stroompunten, en een bijkeuken met een warmtepompdroger en een wasmachine.',
  'Kuchnie zewnętrzne z blatem z gresu, zlewem ze stali nierdzewnej i przyłączami wody i prądu oraz pralnia z suszarką z pompą ciepła i pralką.',
  'Utekjøkken med benkeplate i porselen, en vask i rustfritt stål og vann- og strømuttak, og et vaskerom med en varmepumpetørketrommel og en vaskemaskin.',
  'Utekök med bänkskiva i porslin, en diskho i rostfritt stål och vatten- och eluttag, och ett tvättrum med en värmepumpstork och en tvättmaskin.')
a('.qualitySpecs.groups[5].items[0]',
  'Un sistema Iddero basado en el estándar KNX que controla la iluminación, las persianas y la climatización, con un panel táctil de 10,1 pulgadas en la entrada que hace también de pantalla del videoportero, un panel de 4,3 pulgadas en cada estancia y alarmas de inundación con corte general del agua.',
  'Un système Iddero basé sur la norme KNX qui commande l’éclairage, les stores et la climatisation, avec un écran tactile de 10,1 pouces à l’entrée qui sert aussi d’écran de visiophone, un écran de 4,3 pouces dans chaque pièce et des alarmes d’inondation avec coupure générale de l’eau.',
  'Ein Iddero-System auf KNX-Standard, das Beleuchtung, Jalousien und Klima steuert, mit einem 10,1-Zoll-Touchpanel am Eingang, das zugleich als Bildschirm der Videosprechanlage dient, einem 4,3-Zoll-Panel in jedem Raum und Wasseralarmen mit zentraler Wasserabsperrung.',
  'Система Iddero на стандарте KNX управляет освещением, жалюзи и климатом: сенсорная панель 10,1 дюйма у входа служит и экраном видеодомофона, в каждой комнате — панель 4,3 дюйма, а сигнализация протечек перекрывает воду во всём доме.',
  'نظام Iddero على معيار KNX يتحكم بالإضاءة والستائر والتكييف، مع لوحة لمس مقاس 10.1 بوصة عند المدخل تعمل أيضًا كشاشة للاتصال المرئي، ولوحة مقاس 4.3 بوصة في كل غرفة، وإنذارات فيضان مع قطع عام للمياه.',
  'Een Iddero-systeem op KNX-standaard dat de verlichting, de zonwering en het klimaat bedient, met een touchscreen van 10,1 inch bij de ingang dat ook als scherm van de videofoon dient, een paneel van 4,3 inch in elke ruimte en wateralarmen met een algemene waterafsluiting.',
  'System Iddero w standardzie KNX sterujący oświetleniem, roletami i klimatem, z dotykowym panelem 10,1 cala przy wejściu, który służy też jako ekran wideodomofonu, panelem 4,3 cala w każdym pomieszczeniu oraz alarmami zalania z ogólnym odcięciem wody.',
  'Et Iddero-system på KNX-standarden som styrer belysning, solskjerming og klima, med et berøringspanel på 10,1 tommer ved inngangen som også fungerer som skjerm for videoporttelefonen, et panel på 4,3 tommer i hvert rom og vannalarmer med generell avstengning av vannet.',
  'Ett Iddero-system på KNX-standard som styr belysning, solskydd och klimat, med en pekpanel på 10,1 tum vid entrén som också fungerar som skärm för videodörrtelefonen, en panel på 4,3 tum i varje rum och vattenlarm med allmän vattenavstängning.')
a('.qualitySpecs.groups[6].items[0]',
  'Aire acondicionado Mitsubishi con zonificación de temperatura y difusores lineales ocultos, suelo radiante en toda la vivienda excepto el sótano, y agua caliente con bomba de calor aerotérmica.',
  'Climatisation Mitsubishi avec zonage de température et diffuseurs linéaires dissimulés, plancher chauffant dans tout le logement sauf le sous-sol, et eau chaude produite par une pompe à chaleur aérothermique.',
  'Mitsubishi-Klimaanlage mit Temperaturzonierung und verdeckten Linearauslässen, Fußbodenheizung im gesamten Haus außer im Untergeschoss und Warmwasser über eine Luft-Wasser-Wärmepumpe.',
  'Кондиционирование Mitsubishi с зонированием температуры и скрытыми линейными диффузорами, тёплый пол во всём доме, кроме подвального этажа, и горячая вода от аэротермального теплового насоса.',
  'تكييف Mitsubishi مع تقسيم درجات الحرارة إلى مناطق ونواشر خطية مخفية، وتدفئة أرضية في المنزل كله عدا الطابق السفلي، وماء ساخن من مضخة حرارية هوائية.',
  'Mitsubishi-airconditioning met temperatuurzonering en verborgen lineaire roosters, vloerverwarming in de hele woning behalve in de kelder, en warm water via een aerothermische warmtepomp.',
  'Klimatyzacja Mitsubishi ze strefowaniem temperatury i ukrytymi dyfuzorami liniowymi, ogrzewanie podłogowe w całym domu poza piwnicą oraz ciepła woda z aerotermicznej pompy ciepła.',
  'Mitsubishi klimaanlegg med temperatursoner og skjulte lineære diffusorer, gulvvarme i hele boligen unntatt kjelleren, og varmtvann fra en aerotermisk varmepumpe.',
  'Mitsubishi luftkonditionering med temperaturzoner och dolda linjära don, golvvärme i hela bostaden utom källaren, och varmvatten från en aerotermisk värmepump.')
a('.qualitySpecs.groups[6].items[1]',
  'Ventilación con recuperación de calor, descalcificador electrónico, un sistema que trata las aguas grises para las cisternas y un punto de carga para vehículos eléctricos en el garaje.',
  'Ventilation avec récupération de chaleur, adoucisseur d’eau électronique, un système qui traite les eaux grises pour les chasses d’eau et une borne de recharge pour véhicule électrique dans le garage.',
  'Lüftung mit Wärmerückgewinnung, eine elektronische Wasserenthärtung, ein System, das Grauwasser für die Spülkästen aufbereitet, und eine Ladestation für Elektrofahrzeuge in der Garage.',
  'Вентиляция с рекуперацией тепла, электронный умягчитель воды, система очистки серой воды для сливных бачков и точка зарядки электромобилей в гараже.',
  'تهوية مع استرداد الحرارة، ومنعّم إلكتروني للمياه، ونظام لمعالجة المياه الرمادية لصناديق الطرد، ونقطة شحن للسيارات الكهربائية في المرآب.',
  'Ventilatie met warmteterugwinning, een elektronische waterontharder, een systeem dat grijs water voor de stortbakken behandelt en een oplaadpunt voor elektrische voertuigen in de garage.',
  'Wentylacja z odzyskiem ciepła, elektroniczny zmiękczacz wody, system oczyszczający wodę szarą do spłuczek oraz punkt ładowania pojazdów elektrycznych w garażu.',
  'Ventilasjon med varmegjenvinning, en elektronisk vannavhardner, et system som behandler gråvann til sisternene og et ladepunkt for elbiler i garasjen.',
  'Ventilation med värmeåtervinning, en elektronisk vattenavhärdare, ett system som renar gråvatten till cisternerna och en laddpunkt för elbilar i garaget.')
a('.qualitySpecs.groups[7].name', 'Seguridad, garaje y ascensores', 'Sécurité, garage et ascenseurs', 'Sicherheit, Garage und Aufzüge', 'Безопасность, гараж и лифты',
  'الأمن والمرآب والمصاعد', 'Beveiliging, garage en liften', 'Bezpieczeństwo, garaż i windy', 'Sikkerhet, garasje og heiser', 'Säkerhet, garage och hissar')
a('.qualitySpecs.groups[7].items[0]',
  'Un sistema de seguridad perimetral con cámaras y sensores de calor, vigilado por el equipo de seguridad de la urbanización, y CCTV en las zonas comunes, los garajes y los ascensores.',
  'Un système de sécurité périmétrique avec caméras et détecteurs de chaleur, surveillé par l’équipe de sécurité de la résidence, et une vidéosurveillance dans les parties communes, les garages et les ascenseurs.',
  'Eine Perimeter-Sicherheitsanlage mit Kameras und Wärmesensoren, überwacht vom Sicherheitsteam der Anlage, sowie Videoüberwachung in den Gemeinschaftsbereichen, den Garagen und den Aufzügen.',
  'Система периметральной охраны с камерами и тепловыми датчиками, которую контролирует служба безопасности комплекса, а также видеонаблюдение в общих зонах, гаражах и лифтах.',
  'نظام أمن محيطي بكاميرات وحساسات حرارة يراقبه فريق أمن المجمّع، وكاميرات مراقبة في المناطق المشتركة والمرائب والمصاعد.',
  'Een perimeterbeveiligingssysteem met camera’s en warmtesensoren, bewaakt door het beveiligingsteam van het complex, en camerabewaking in de gemeenschappelijke ruimten, de garages en de liften.',
  'System ochrony obwodowej z kamerami i czujnikami ciepła, nadzorowany przez zespół ochrony kompleksu, oraz monitoring w częściach wspólnych, garażach i windach.',
  'Et perimetersikkerhetssystem med kameraer og varmesensorer, overvåket av anleggets sikkerhetsteam, og kameraovervåking i fellesarealene, garasjene og heisene.',
  'Ett perimeterskydd med kameror och värmesensorer, övervakat av områdets säkerhetsteam, och kameraövervakning i de gemensamma ytorna, garagen och hissarna.')
a('.qualitySpecs.groups[7].items[1]',
  'Un garaje en el sótano con puertas con mando a distancia, suelo de hormigón pulido impermeabilizado para el lavado a presión y acceso peatonal directo a la vivienda, y ascensores eléctricos de cuatro paradas: para seis personas en las villas, según el tipo, y para ocho en los apartamentos.',
  'Un garage en sous-sol avec portes télécommandées, un sol en béton poli étanche pour le nettoyage à haute pression et un accès piéton direct au logement, et des ascenseurs électriques à quatre arrêts : pour six personnes dans les villas, selon le type, et pour huit dans les appartements.',
  'Eine Garage im Untergeschoss mit ferngesteuerten Toren, einem polierten Betonboden, der für die Hochdruckreinigung abgedichtet ist, und einem direkten Fußgängerzugang zum Haus sowie Elektroaufzüge mit vier Haltestellen: für sechs Personen in den Villen, je nach Typ, und für acht in den Wohnungen.',
  'Гараж в подвальном этаже с дверями на дистанционном управлении, полом из полированного бетона с гидроизоляцией для мойки под давлением и прямым пешеходным входом в дом, а также электрические лифты на четыре остановки: на шесть человек в виллах, в зависимости от типа, и на восемь в квартирах.',
  'مرآب في الطابق السفلي بأبواب بالتحكم عن بُعد وأرضية من الخرسانة المصقولة معزولة للغسل بالضغط ومدخل مشاة مباشر إلى المسكن، ومصاعد كهربائية بأربع محطات: لستة أشخاص في الفلل بحسب النوع، ولثمانية في الشقق.',
  'Een garage in de kelder met afstandsbediende deuren, een gepolijste betonvloer die is afgedicht voor reiniging met hogedruk en een directe voetgangerstoegang tot de woning, en elektrische liften met vier haltes: voor zes personen in de villa’s, afhankelijk van het type, en voor acht in de appartementen.',
  'Garaż w piwnicy z drzwiami sterowanymi pilotem, polerowaną posadzką betonową uszczelnioną pod mycie ciśnieniowe i bezpośrednim wejściem dla pieszych do domu oraz elektryczne windy z czterema przystankami: na sześć osób w willach, zależnie od typu, i na osiem w apartamentach.',
  'En garasje i kjelleren med fjernstyrte porter, et polert betonggulv som er tettet for høytrykksspyling og en direkte gangadkomst til boligen, og elektriske heiser med fire stopp: for seks personer i villaene, avhengig av typen, og for åtte i leilighetene.',
  'Ett garage i källaren med fjärrstyrda portar, ett polerat betonggolv som är tätat för högtryckstvätt och en direkt gångentré till bostaden, och eldrivna hissar med fyra stopp: för sex personer i villorna, beroende på typ, och för åtta i lägenheterna.')

# ---- residences, lifestyle, location ---------------------------------------------------------------

a('.residences.headlineHtml', 'Dos viviendas, <em>una villa y un apartamento</em>', 'Deux logements, <em>une villa et un appartement</em>',
  'Zwei Immobilien, <em>eine Villa und eine Wohnung</em>', 'Два объекта: <em>вилла и квартира</em>', 'مسكنان، <em>فيلا وشقة</em>',
  'Twee woningen, <em>een villa en een appartement</em>', 'Dwa lokale: <em>willa i mieszkanie</em>', 'To boliger, <em>en villa og en leilighet</em>', 'Två bostäder, <em>en villa och en lägenhet</em>')
a('.residences.copy',
  'Las dos viviendas publicadas con precio son de tipos distintos, y la tabla siguiente recoge cada una con su precio. Las superficies son las de los planos del promotor.',
  'Les deux logements présentés avec un prix sont de types différents, et le tableau ci-dessous présente chacun avec son prix. Les surfaces sont celles des plans du promoteur.',
  'Die beiden mit Preis gelisteten Immobilien sind von unterschiedlichem Typ; die Tabelle unten führt jede mit ihrem Preis auf. Die Flächen sind die der Pläne des Bauträgers.',
  'Два объекта, указанные с ценой, относятся к разным типам; в таблице ниже каждый показан со своей ценой. Площади — по планам застройщика.',
  'المسكنان المدرجان بسعر من نوعين مختلفين، ويعرض الجدول أدناه كلًّا منهما مع سعره. المساحات هي المذكورة في مخططات المطوّر.',
  'De twee woningen met een prijs zijn van verschillend type, en de tabel hieronder toont elk met zijn prijs. De oppervlakten zijn die van de plattegronden van de ontwikkelaar.',
  'Dwa lokale z podaną ceną są różnych typów, a poniższa tabela przedstawia każdy z jego ceną. Powierzchnie pochodzą z rzutów dewelopera.',
  'De to boligene med pris er av ulike typer, og tabellen nedenfor viser hver av dem med pris. Arealene er de fra utbyggerens plantegninger.',
  'De två bostäder som har ett pris är av olika typ, och tabellen nedan visar var och en med dess pris. Areorna är de från exploatörens planritningar.')
a('.residences.items[0].name', 'Villa Nr. 04, cuatro dormitorios', 'Villa Nr. 04, quatre chambres', 'Villa Nr. 04, vier Schlafzimmer', 'Вилла Nr. 04, четыре спальни',
  'الفيلا Nr. 04، أربع غرف نوم', 'Villa Nr. 04, vier slaapkamers', 'Willa Nr. 04, cztery sypialnie', 'Villa Nr. 04, fire soverom', 'Villa Nr. 04, fyra sovrum')
a('.residences.items[0].points[0]',
  'Una villa pareada de tipo A2 en la parcela R2, con cuatro dormitorios. Los planos indican 447,13 m² construidos, 168,15 m² de ellos en el sótano, 354,43 m² útiles y 280,89 m² útiles exteriores.',
  'Une villa jumelée de type A2 sur la parcelle R2, avec quatre chambres. Les plans indiquent 447,13 m² construits, dont 168,15 m² en sous-sol, 354,43 m² utiles et 280,89 m² utiles extérieurs.',
  'Eine Doppelhaushälfte vom Typ A2 auf Parzelle R2 mit vier Schlafzimmern. Die Pläne geben 447,13 m² Baufläche an, davon 168,15 m² im Untergeschoss, 354,43 m² Nutzfläche und 280,89 m² Außennutzfläche.',
  'Парный дом типа A2 на участке R2 с четырьмя спальнями. По планам площадь застройки — 447,13 м², из них 168,15 м² в подвальном этаже, полезная площадь — 354,43 м², полезная площадь вне дома — 280,89 м².',
  'فيلا شبه منفصلة من النوع A2 على القطعة R2، بأربع غرف نوم. تذكر المخططات 447.13 م² مبنية، منها 168.15 م² في الطابق السفلي، و354.43 م² صافية، و280.89 م² صافية خارجية.',
  'Een halfvrijstaande villa van type A2 op perceel R2, met vier slaapkamers. De plattegronden geven 447,13 m² bebouwd, waarvan 168,15 m² in de kelder, 354,43 m² nuttig en 280,89 m² nuttig buiten.',
  'Dom bliźniaczy typu A2 na działce R2, z czterema sypialniami. Rzuty podają 447,13 m² zabudowy, w tym 168,15 m² w piwnicy, 354,43 m² powierzchni użytkowej i 280,89 m² powierzchni użytkowej zewnętrznej.',
  'En tomannsvilla av type A2 på tomt R2, med fire soverom. Plantegningene oppgir 447,13 m² bebygd, hvorav 168,15 m² i kjelleren, 354,43 m² bruksareal og 280,89 m² utvendig bruksareal.',
  'Ett parhus av typ A2 på tomt R2, med fyra sovrum. Planritningarna anger 447,13 m² byggyta, varav 168,15 m² i källaren, 354,43 m² boarea och 280,89 m² användbar yta utomhus.')
a('.residences.items[0].points[1]',
  'El sótano tiene un garaje de 46,54 m² para dos coches y una sala multiusos de 50,46 m². La planta baja tiene una zona de salón, comedor y cocina de 79,96 m², un dormitorio de 12,10 m² y una terraza de 89,36 m² con jacuzzi.',
  'Le sous-sol compte un garage de 46,54 m² pour deux voitures et une salle polyvalente de 50,46 m². Le rez-de-chaussée compte un espace séjour, salle à manger et cuisine de 79,96 m², une chambre de 12,10 m² et une terrasse de 89,36 m² avec jacuzzi.',
  'Im Untergeschoss befinden sich eine Garage von 46,54 m² für zwei Autos und ein Mehrzweckraum von 50,46 m². Das Erdgeschoss hat einen Wohn-, Ess- und Küchenbereich von 79,96 m², ein Schlafzimmer von 12,10 m² und eine Terrasse von 89,36 m² mit Whirlpool.',
  'В подвальном этаже — гараж 46,54 м² на две машины и многофункциональный зал 50,46 м². На первом этаже — гостиная, столовая и кухня общей площадью 79,96 м², спальня 12,10 м² и терраса 89,36 м² с джакузи.',
  'في الطابق السفلي مرآب مساحته 46.54 م² لسيارتين وقاعة متعددة الاستعمالات مساحتها 50.46 م². وفي الطابق الأرضي منطقة جلوس وطعام ومطبخ مساحتها 79.96 م² وغرفة نوم مساحتها 12.10 م² وتراس مساحته 89.36 م² مع جاكوزي.',
  'In de kelder zijn een garage van 46,54 m² voor twee auto’s en een multifunctionele ruimte van 50,46 m². De begane grond heeft een woon-, eet- en keukenruimte van 79,96 m², een slaapkamer van 12,10 m² en een terras van 89,36 m² met een jacuzzi.',
  'W piwnicy znajdują się garaż o powierzchni 46,54 m² na dwa samochody i sala wielofunkcyjna o powierzchni 50,46 m². Na parterze jest część dzienna z jadalnią i kuchnią o powierzchni 79,96 m², sypialnia o powierzchni 12,10 m² i taras o powierzchni 89,36 m² z jacuzzi.',
  'Kjelleren har en garasje på 46,54 m² for to biler og et flerbruksrom på 50,46 m². Første etasje har et område med stue, spisestue og kjøkken på 79,96 m², et soverom på 12,10 m² og en terrasse på 89,36 m² med jacuzzi.',
  'Källaren har ett garage på 46,54 m² för två bilar och ett flerfunktionsrum på 50,46 m². Bottenvåningen har en yta med vardagsrum, matrum och kök på 79,96 m², ett sovrum på 12,10 m² och en terrass på 89,36 m² med jacuzzi.')
a('.residences.items[0].points[2]',
  'La primera planta tiene el dormitorio principal de 30,33 m² y dos dormitorios más, y el solárium tiene una terraza de 81,72 m² y una piscina de 23,18 m². El precio es de {E5400000}, según la lista del 29 de octubre de 2026.',
  'Le premier étage compte la chambre principale de 30,33 m² et deux autres chambres, et le solarium compte une terrasse de 81,72 m² et une piscine de 23,18 m². Le prix est de {E5400000}, selon la liste du 29 octobre 2026.',
  'Das erste Obergeschoss hat das Hauptschlafzimmer von 30,33 m² und zwei weitere Schlafzimmer, und das Solarium hat eine Terrasse von 81,72 m² und einen Pool von 23,18 m². Der Preis beträgt {E5400000} laut Liste vom 29. Oktober 2026.',
  'На втором этаже — главная спальня 30,33 м² и ещё две спальни, на солярии — терраса 81,72 м² и бассейн 23,18 м². Цена — {E5400000} по списку от 29 октября 2026 года.',
  'في الطابق الأول غرفة النوم الرئيسية بمساحة 30.33 م² وغرفتا نوم أخريان، وفي السولاريوم تراس مساحته 81.72 م² ومسبح مساحته 23.18 م². السعر {E5400000} وفق قائمة 29 أكتوبر 2026.',
  'De eerste verdieping heeft de hoofdslaapkamer van 30,33 m² en twee andere slaapkamers, en het solarium heeft een terras van 81,72 m² en een zwembad van 23,18 m². De prijs is {E5400000}, volgens de lijst van 29 oktober 2026.',
  'Na pierwszym piętrze jest sypialnia główna o powierzchni 30,33 m² i dwie kolejne sypialnie, a na solarium taras o powierzchni 81,72 m² i basen o powierzchni 23,18 m². Cena wynosi {E5400000} według listy z 29 października 2026 r.',
  'Andre etasje har hovedsoverommet på 30,33 m² og to soverom til, og solterrassen har en terrasse på 81,72 m² og et basseng på 23,18 m². Prisen er {E5400000}, ifølge listen fra 29. oktober 2026.',
  'Första våningen har huvudsovrummet på 30,33 m² och två sovrum till, och solterrassen har en terrass på 81,72 m² och en pool på 23,18 m². Priset är {E5400000}, enligt listan från den 29 oktober 2026.')
a('.residences.items[1].name', 'Apartamento Nr. 202, tres dormitorios', 'Appartement Nr. 202, trois chambres', 'Wohnung Nr. 202, drei Schlafzimmer', 'Квартира Nr. 202, три спальни',
  'الشقة Nr. 202، ثلاث غرف نوم', 'Appartement Nr. 202, drie slaapkamers', 'Mieszkanie Nr. 202, trzy sypialnie', 'Leilighet Nr. 202, tre soverom', 'Lägenhet Nr. 202, tre sovrum')
a('.residences.items[1].points[0]',
  'Un apartamento en planta baja de tipo B2, en el bloque 2, portal 2, con tres dormitorios, jardín privado y piscina privada. Los planos indican 483,98 m² construidos, que incluyen 198,29 m² de sótano y 40,81 m² de zonas comunes, 378,22 m² útiles y 261,00 m² útiles exteriores.',
  'Un appartement de plain-pied de type B2, dans le bloc 2, cage 2, avec trois chambres, un jardin privé et une piscine privée. Les plans indiquent 483,98 m² construits, dont 198,29 m² de sous-sol et 40,81 m² de parties communes, 378,22 m² utiles et 261,00 m² utiles extérieurs.',
  'Eine Erdgeschosswohnung vom Typ B2 in Block 2, Aufgang 2, mit drei Schlafzimmern, privatem Garten und privatem Pool. Die Pläne geben 483,98 m² Baufläche an, einschließlich 198,29 m² Untergeschoss und 40,81 m² Gemeinschaftsflächen, 378,22 m² Nutzfläche und 261,00 m² Außennutzfläche.',
  'Квартира типа B2 на первом этаже в блоке 2, подъезд 2, с тремя спальнями, собственным садом и собственным бассейном. По планам площадь застройки — 483,98 м², включая 198,29 м² подвального этажа и 40,81 м² общих зон, полезная площадь — 378,22 м², полезная площадь вне дома — 261,00 м².',
  'شقة في الطابق الأرضي من النوع B2، في المبنى 2، المدخل 2، بثلاث غرف نوم وحديقة خاصة ومسبح خاص. تذكر المخططات 483.98 م² مبنية، تشمل 198.29 م² من الطابق السفلي و40.81 م² من المناطق المشتركة، و378.22 م² صافية، و261.00 م² صافية خارجية.',
  'Een appartement op de begane grond van type B2, in blok 2, portiek 2, met drie slaapkamers, een privétuin en een privézwembad. De plattegronden geven 483,98 m² bebouwd, inclusief 198,29 m² kelder en 40,81 m² gemeenschappelijke ruimten, 378,22 m² nuttig en 261,00 m² nuttig buiten.',
  'Mieszkanie na parterze typu B2, w bloku 2, klatka 2, z trzema sypialniami, prywatnym ogrodem i prywatnym basenem. Rzuty podają 483,98 m² zabudowy, w tym 198,29 m² piwnicy i 40,81 m² części wspólnych, 378,22 m² powierzchni użytkowej i 261,00 m² powierzchni użytkowej zewnętrznej.',
  'En leilighet i første etasje av type B2, i blokk 2, oppgang 2, med tre soverom, privat hage og privat basseng. Plantegningene oppgir 483,98 m² bebygd, som inkluderer 198,29 m² kjeller og 40,81 m² fellesarealer, 378,22 m² bruksareal og 261,00 m² utvendig bruksareal.',
  'En lägenhet på bottenvåningen av typ B2, i block 2, port 2, med tre sovrum, egen trädgård och egen pool. Planritningarna anger 483,98 m² byggyta, som inkluderar 198,29 m² källare och 40,81 m² gemensamma ytor, 378,22 m² boarea och 261,00 m² användbar yta utomhus.')
a('.residences.items[1].points[1]',
  'La zona de salón, cocina y comedor mide 72,30 m², el dormitorio principal 46,35 m² y los otros dos dormitorios 22,40 y 20,03 m². La terraza mide 146,70 m², el jardín 79,46 m² y la piscina 34,84 m².',
  'L’espace séjour, cuisine et salle à manger mesure 72,30 m², la chambre principale 46,35 m² et les deux autres chambres 22,40 et 20,03 m². La terrasse mesure 146,70 m², le jardin 79,46 m² et la piscine 34,84 m².',
  'Der Wohn-, Koch- und Essbereich misst 72,30 m², das Hauptschlafzimmer 46,35 m² und die beiden anderen Schlafzimmer 22,40 und 20,03 m². Die Terrasse misst 146,70 m², der Garten 79,46 m² und der Pool 34,84 m².',
  'Гостиная, кухня и столовая занимают 72,30 м², главная спальня — 46,35 м², две другие спальни — 22,40 и 20,03 м². Терраса — 146,70 м², сад — 79,46 м², бассейн — 34,84 м².',
  'تبلغ مساحة منطقة الجلوس والمطبخ والطعام 72.30 م²، وغرفة النوم الرئيسية 46.35 م²، وغرفتا النوم الأخريان 22.40 و20.03 م². ومساحة التراس 146.70 م²، والحديقة 79.46 م²، والمسبح 34.84 م².',
  'De woon-, keuken- en eetruimte meet 72,30 m², de hoofdslaapkamer 46,35 m² en de twee andere slaapkamers 22,40 en 20,03 m². Het terras meet 146,70 m², de tuin 79,46 m² en het zwembad 34,84 m².',
  'Część dzienna z kuchnią i jadalnią ma 72,30 m², sypialnia główna 46,35 m², a pozostałe dwie sypialnie 22,40 i 20,03 m². Taras ma 146,70 m², ogród 79,46 m², a basen 34,84 m².',
  'Stue, kjøkken og spisestue måler 72,30 m², hovedsoverommet 46,35 m² og de to andre soverommene 22,40 og 20,03 m². Terrassen måler 146,70 m², hagen 79,46 m² og bassenget 34,84 m².',
  'Vardagsrum, kök och matrum mäter 72,30 m², huvudsovrummet 46,35 m² och de två andra sovrummen 22,40 och 20,03 m². Terrassen mäter 146,70 m², trädgården 79,46 m² och poolen 34,84 m².')
a('.residences.items[1].points[2]',
  'El sótano tiene un garaje privado de 38,00 m² para dos coches y una sala multiusos de 93,35 m². El precio es de {E5200000}, según la lista del 29 de octubre de 2026 y la lista de precios del 1 de julio de 2026.',
  'Le sous-sol compte un garage privé de 38,00 m² pour deux voitures et une salle polyvalente de 93,35 m². Le prix est de {E5200000}, selon la liste du 29 octobre 2026 et la liste de prix du 1er juillet 2026.',
  'Im Untergeschoss befinden sich eine private Garage von 38,00 m² für zwei Autos und ein Mehrzweckraum von 93,35 m². Der Preis beträgt {E5200000} laut Liste vom 29. Oktober 2026 und laut Preisliste vom 1. Juli 2026.',
  'В подвальном этаже — частный гараж 38,00 м² на две машины и многофункциональный зал 93,35 м². Цена — {E5200000} по списку от 29 октября 2026 года и по прайс-листу от 1 июля 2026 года.',
  'في الطابق السفلي مرآب خاص مساحته 38.00 م² لسيارتين وقاعة متعددة الاستعمالات مساحتها 93.35 م². السعر {E5200000} وفق قائمة 29 أكتوبر 2026 وقائمة الأسعار بتاريخ 1 يوليو 2026.',
  'In de kelder zijn een privégarage van 38,00 m² voor twee auto’s en een multifunctionele ruimte van 93,35 m². De prijs is {E5200000}, volgens de lijst van 29 oktober 2026 en de prijslijst van 1 juli 2026.',
  'W piwnicy znajdują się prywatny garaż o powierzchni 38,00 m² na dwa samochody i sala wielofunkcyjna o powierzchni 93,35 m². Cena wynosi {E5200000} według listy z 29 października 2026 r. i cennika z 1 lipca 2026 r.',
  'Kjelleren har en privat garasje på 38,00 m² for to biler og et flerbruksrom på 93,35 m². Prisen er {E5200000}, ifølge listen fra 29. oktober 2026 og prislisten fra 1. juli 2026.',
  'Källaren har ett privat garage på 38,00 m² för två bilar och ett flerfunktionsrum på 93,35 m². Priset är {E5200000}, enligt listan från den 29 oktober 2026 och prislistan från den 1 juli 2026.')
a('.lifestyle.headlineHtml', 'Un spa, <em>jardines</em> y las dunas', 'Un spa, <em>des jardins</em> et les dunes', 'Ein Spa, <em>Gärten</em> und die Dünen', 'Спа, <em>сады</em> и дюны',
  'منتجع صحي و<em>حدائق</em> والكثبان الرملية', 'Een spa, <em>tuinen</em> en de duinen', 'Spa, <em>ogrody</em> i wydmy', 'Et spa, <em>hager</em> og dynene', 'Ett spa, <em>trädgårdar</em> och dynerna')
a('.lifestyle.copy',
  'El folleto describe las zonas comunes y el entorno. Está fechado en agosto de 2024, por lo que confirmamos qué está construido y abierto antes de cualquier reserva.',
  'La brochure décrit les parties communes et le cadre. Elle est datée d’août 2024 ; nous confirmons donc ce qui est construit et ouvert avant toute réservation.',
  'Die Broschüre beschreibt die Gemeinschaftsbereiche und die Umgebung. Sie ist auf August 2024 datiert, deshalb bestätigen wir vor jeder Reservierung, was gebaut und geöffnet ist.',
  'В брошюре описаны общие зоны и окружение. Она датирована августом 2024 года, поэтому перед любым бронированием мы уточняем, что построено и открыто.',
  'يصف الكتيّب المناطق المشتركة والمحيط. وهو مؤرّخ في أغسطس 2024، لذلك نؤكد ما تم بناؤه وما فُتح قبل أي حجز.',
  'De brochure beschrijft de gemeenschappelijke ruimten en de omgeving. Ze is gedateerd augustus 2024, dus wij bevestigen wat er is gebouwd en geopend vóór elke reservering.',
  'Broszura opisuje części wspólne i otoczenie. Pochodzi z sierpnia 2024 r., dlatego przed każdą rezerwacją potwierdzamy, co jest zbudowane i otwarte.',
  'Brosjyren beskriver fellesarealene og omgivelsene. Den er datert august 2024, så vi bekrefter hva som er bygget og åpnet før enhver reservasjon.',
  'Broschyren beskriver de gemensamma ytorna och omgivningen. Den är daterad augusti 2024, så vi bekräftar vad som är byggt och öppet före varje reservation.')
a('.lifestyle.panels[0][0]', 'El centro social', 'Le centre social', 'Der Social Hub', 'Социальный центр', 'المركز الاجتماعي', 'Het sociale centrum', 'Centrum społeczne', 'Det sosiale senteret', 'Det sociala centret')
a('.lifestyle.panels[0][1]',
  'Un complejo de bienestar con baño turco y sauna, una piscina interior climatizada, un gimnasio interior y otro exterior, una zona de meditación y yoga, un espacio de coworking y un lounge y bar en la azotea.',
  'Un espace bien-être avec hammam et sauna, une piscine intérieure chauffée, une salle de sport intérieure et une extérieure, un espace de méditation et de yoga, un espace de coworking et un lounge-bar sur le toit.',
  'Ein Wellnessbereich mit Dampfbad und Sauna, einem beheizten Innenpool, einem Indoor- und einem Outdoor-Fitnessbereich, einem Meditations- und Yogabereich, einem Coworking-Bereich sowie einer Lounge mit Bar auf dem Dach.',
  'Оздоровительный комплекс с турецкой баней и сауной, крытым бассейном с подогревом, тренажёрным залом в помещении и под открытым небом, зоной для медитации и йоги, коворкингом и лаунж-баром на крыше.',
  'مجمّع للعافية يضم حمامًا تركيًا وساونا ومسبحًا داخليًا مدفأً وصالة رياضية داخلية وأخرى خارجية ومنطقة للتأمل واليوغا ومساحة عمل مشترك وصالة وبارًا على السطح.',
  'Een welnesscomplex met een Turks bad en een sauna, een verwarmd binnenzwembad, een fitnessruimte binnen en een buiten, een meditatie- en yogaruimte, een coworkingruimte en een loungebar op het dak.',
  'Kompleks wellness z łaźnią turecką i sauną, podgrzewanym basenem wewnętrznym, siłownią wewnętrzną i zewnętrzną, strefą medytacji i jogi, przestrzenią coworkingową oraz lounge-barem na dachu.',
  'Et velværeanlegg med tyrkisk bad og badstue, et oppvarmet innendørsbasseng, et treningsrom inne og et ute, en sone for meditasjon og yoga, en coworking-sone og en loungebar på taket.',
  'Ett välmåendecenter med turkiskt bad och bastu, en uppvärmd inomhuspool, ett gym inomhus och ett utomhus, en yta för meditation och yoga, en coworkingyta och en loungebar på taket.')
a('.lifestyle.panels[1][1]',
  'El folleto describe un spa profesional a pocos pasos de las viviendas, con vestuarios, terapia geotérmica, aromaterapia, una sauna, un baño turco y una piscina interior de dimensiones casi olímpicas.',
  'La brochure décrit un spa professionnel à quelques pas des logements, avec vestiaires, thérapie géothermique, aromathérapie, un sauna, un hammam et une piscine intérieure aux dimensions presque olympiques.',
  'Die Broschüre beschreibt ein professionelles Spa wenige Schritte von den Immobilien entfernt, mit Umkleiden, Geothermie-Therapie, Aromatherapie, einer Sauna, einem Dampfbad und einem Innenpool in fast olympischen Maßen.',
  'В брошюре описано профессиональное спа в нескольких шагах от жилья: раздевалки, геотермальная терапия, ароматерапия, сауна, турецкая баня и крытый бассейн почти олимпийских размеров.',
  'يصف الكتيّب منتجعًا صحيًا احترافيًا على بُعد خطوات من المساكن، مع غرف تبديل ملابس وعلاج جيوحراري وعلاج بالروائح وساونا وحمام تركي ومسبح داخلي بأبعاد شبه أولمبية.',
  'De brochure beschrijft een professionele spa op een paar stappen van de woningen, met kleedkamers, geothermische therapie, aromatherapie, een sauna, een Turks bad en een binnenzwembad met bijna olympische afmetingen.',
  'Broszura opisuje profesjonalne spa kilka kroków od lokali, z szatniami, terapią geotermalną, aromaterapią, sauną, łaźnią turecką i basenem wewnętrznym o niemal olimpijskich wymiarach.',
  'Brosjyren beskriver et profesjonelt spa noen få skritt fra boligene, med garderober, geotermisk terapi, aromaterapi, en badstue, et tyrkisk bad og et innendørsbasseng med nesten olympiske mål.',
  'Broschyren beskriver ett professionellt spa några steg från bostäderna, med omklädningsrum, geotermisk terapi, aromaterapi, en bastu, ett turkiskt bad och en inomhuspool med nästan olympiska mått.')
a('.lifestyle.panels[2][0]', 'El lounge de la azotea', 'Le lounge sur le toit', 'Die Rooftop-Lounge', 'Лаунж на крыше', 'الصالة على السطح', 'De lounge op het dak', 'Lounge na dachu', 'Loungen på taket', 'Loungen på taket')
a('.lifestyle.panels[2][1]',
  'Un lounge y bar en la azotea del centro social, con una piscina infinita suspendida a más de 8 m del suelo y camas balinesas.',
  'Un lounge-bar sur le toit du centre social, avec une piscine à débordement suspendue à plus de 8 m du sol et des lits balinais.',
  'Eine Lounge mit Bar auf dem Dach des Social Hub, mit einem Infinity-Pool, der mehr als 8 m über dem Boden schwebt, und balinesischen Liegen.',
  'Лаунж-бар на крыше социального центра с бесконечным бассейном, подвешенным более чем на 8 м над землёй, и балийскими кроватями.',
  'صالة وبار على سطح المركز الاجتماعي، مع مسبح لا متناهٍ معلّق على ارتفاع يزيد على 8 م عن الأرض وأسرّة بالية.',
  'Een lounge met bar op het dak van het sociale centrum, met een zwevend infinity-zwembad op meer dan 8 m boven de grond en Balinese bedden.',
  'Lounge z barem na dachu centrum społecznego, z basenem typu infinity zawieszonym ponad 8 m nad ziemią i balijskimi łóżkami.',
  'En lounge med bar på taket av det sosiale senteret, med et uendelighetsbasseng som henger mer enn 8 m over bakken og balinesiske senger.',
  'En lounge med bar på taket av det sociala centret, med en infinitypool som hänger mer än 8 m över marken och balinesiska bäddar.')
a('.lifestyle.panels[3][1]',
  'Jardines escalonados que descienden hacia el mar, con vegetación autóctona de bajo consumo de agua, un prado, zonas de sombra, miradores y agua que discurre entre los niveles en estanques, pequeñas cascadas y charcas.',
  'Des jardins en terrasses qui descendent vers la mer, avec une végétation locale peu gourmande en eau, une prairie, des zones d’ombre, des belvédères et de l’eau qui circule entre les niveaux dans des bassins, de petites cascades et des mares.',
  'Terrassierte Gärten, die zum Meer hin abfallen, mit heimischer, wassersparender Bepflanzung, einer Wiese, Schattenbereichen, Aussichtspunkten und Wasser, das zwischen den Ebenen in Becken, kleinen Wasserfällen und Teichen fließt.',
  'Террасные сады, спускающиеся к морю, с местными растениями, не требующими много воды, лугом, тенистыми зонами, смотровыми площадками и водой, которая течёт между уровнями — водоёмы, небольшие водопады и пруды.',
  'حدائق مدرّجة تنحدر نحو البحر، بنباتات محلية قليلة استهلاك المياه ومرج ومناطق ظل وأماكن للإطلالة ومياه تجري بين المستويات في برك وشلالات صغيرة وبحيرات.',
  'Terrasvormige tuinen die naar de zee aflopen, met inheemse, waterzuinige beplanting, een weide, schaduwplekken, uitkijkpunten en water dat tussen de niveaus stroomt in poelen, kleine watervallen en vijvers.',
  'Tarasowe ogrody opadające ku morzu, z rodzimą, mało wymagającą wody roślinnością, łąką, strefami cienia, punktami widokowymi i wodą płynącą między poziomami w oczkach, małych wodospadach i stawach.',
  'Terrasserte hager som skråner ned mot havet, med stedegen, vannsparende beplantning, en eng, skyggefulle områder, utsiktspunkter og vann som renner mellom nivåene i dammer, små fossefall og tjern.',
  'Terrasserade trädgårdar som sluttar ned mot havet, med inhemsk, vattensnål växtlighet, en äng, skuggiga ytor, utsiktspunkter och vatten som rinner mellan nivåerna i dammar, små vattenfall och tjärnar.')
a('.lifestyle.panels[4][0]', 'Las dunas', 'Les dunes', 'Die Dünen', 'Дюны', 'الكثبان الرملية', 'De duinen', 'Wydmy', 'Dynene', 'Dynerna')
a('.lifestyle.panels[4][1]',
  'El Barronal de la Morena, un sistema dunar protegido de unos 36.000 m² y 200 m de longitud, paralelo a la playa, rico en especies animales y vegetales, con el que el folleto dice que el complejo está integrado.',
  'El Barronal de la Morena, un système dunaire protégé d’environ 36 000 m² et de 200 m de long, parallèle à la plage, riche en espèces animales et végétales, auquel la brochure dit que l’ensemble est intégré.',
  'El Barronal de la Morena, ein geschütztes Dünensystem von etwa 36.000 m² und 200 m Länge parallel zum Strand, reich an Tier- und Pflanzenarten, in das die Anlage laut Broschüre integriert ist.',
  'Эль-Баррональ-де-ла-Морена — охраняемая система дюн площадью около 36 000 м² и длиной 200 м вдоль пляжа, богатая видами животных и растений; по словам брошюры, комплекс органично вписан в неё.',
  '«إل بارونال دي لا مورينا»، نظام كثبان رملية محمي بمساحة نحو 36,000 م² وطول 200 م موازٍ للشاطئ، غني بالأنواع الحيوانية والنباتية، ويقول الكتيّب إن المجمّع مندمج معه.',
  'El Barronal de la Morena, een beschermd duinsysteem van ongeveer 36.000 m² en 200 m lang, evenwijdig aan het strand, rijk aan dier- en plantensoorten, waarin het complex volgens de brochure is geïntegreerd.',
  'El Barronal de la Morena, chroniony system wydm o powierzchni około 36 000 m² i długości 200 m, równoległy do plaży, bogaty w gatunki zwierząt i roślin, z którym kompleks według broszury jest zintegrowany.',
  'El Barronal de la Morena, et vernet dynesystem på omtrent 36 000 m² og 200 m langt, parallelt med stranden, rikt på dyre- og plantearter, som anlegget ifølge brosjyren er integrert med.',
  'El Barronal de la Morena, ett skyddat dynsystem på cirka 36 000 m² och 200 m långt, parallellt med stranden, rikt på djur- och växtarter, som området enligt broschyren är integrerat med.')
a('.location.headlineHtml', 'Marbella, <em>junto a las dunas</em>', 'Marbella, <em>à côté des dunes</em>', 'Marbella, <em>neben den Dünen</em>', 'Марбелья, <em>рядом с дюнами</em>',
  'ماربيا، <em>بجوار الكثبان الرملية</em>', 'Marbella, <em>naast de duinen</em>', 'Marbella, <em>obok wydm</em>', 'Marbella, <em>ved siden av dynene</em>', 'Marbella, <em>intill dynerna</em>')
a('.location.copy',
  'El folleto sitúa el complejo en Marbella, junto al sistema dunar protegido de El Barronal de la Morena, que ubica en la zona de El Rosario - Las Chapas, y presenta el proyecto como vida en primera línea de playa. Su mapa de ubicación muestra el centro de Marbella, el puerto deportivo de Marbella, el puerto deportivo de Cabopino, Puerto Banús, Nueva Andalucía y varios clubes de golf, sin distancias. Los documentos no dan dirección ni coordenadas de la parcela, por lo que el mapa muestra la zona de El Rosario.',
  'La brochure situe l’ensemble à Marbella, à côté du système dunaire protégé d’El Barronal de la Morena, qu’elle place dans le secteur d’El Rosario - Las Chapas, et présente le projet comme un art de vivre en bord de mer. Sa carte de situation montre le centre de Marbella, le port de plaisance de Marbella, le port de plaisance de Cabopino, Puerto Banús, Nueva Andalucía et plusieurs clubs de golf, sans distances. Les documents ne donnent ni adresse ni coordonnées de la parcelle ; la carte montre donc le secteur d’El Rosario.',
  'Die Broschüre verortet die Anlage in Marbella, neben dem geschützten Dünensystem El Barronal de la Morena, das sie im Gebiet El Rosario - Las Chapas ansiedelt, und beschreibt das Projekt als Wohnen direkt am Strand. Ihre Lagekarte zeigt das Zentrum von Marbella, den Yachthafen Marbella, den Yachthafen Cabopino, Puerto Banús, Nueva Andalucía und mehrere Golfclubs, ohne Entfernungen. Die Unterlagen nennen weder Adresse noch Koordinaten des Grundstücks, daher zeigt die Karte das Gebiet El Rosario.',
  'В брошюре комплекс расположен в Марбелье, рядом с охраняемой системой дюн Эль-Баррональ-де-ла-Морена, которую она относит к району Эль-Росарио — Лас-Чапас; проект подан как жизнь на первой линии у пляжа. На её карте местоположения показаны центр Марбельи, порт Марбельи, порт Кабопино, Пуэрто-Банус, Нуэва-Андалусия и несколько гольф-клубов, без расстояний. В документах нет ни адреса, ни координат участка, поэтому карта показывает район Эль-Росарио.',
  'يضع الكتيّب المجمّع في ماربيا، بجوار نظام الكثبان الرملية المحمي «إل بارونال دي لا مورينا» الذي يحدد موقعه في منطقة إل روساريو - لاس تشاباس، ويقدّم المشروع بوصفه حياة على الواجهة البحرية. وتُظهر خريطة الموقع فيه وسط ماربيا وميناء ماربيا ومرسى كابوبينو وبويرتو بانوس ونويفا أندلوثيا وعددًا من نوادي الغولف، دون مسافات. ولا تذكر الوثائق عنوانًا ولا إحداثيات لقطعة الأرض، لذلك تُظهر الخريطة منطقة إل روساريو.',
  'De brochure plaatst het complex in Marbella, naast het beschermde duinsysteem El Barronal de la Morena, dat ze situeert in het gebied El Rosario - Las Chapas, en presenteert het project als wonen direct aan het strand. Haar locatiekaart toont het centrum van Marbella, de jachthaven van Marbella, de jachthaven van Cabopino, Puerto Banús, Nueva Andalucía en meerdere golfclubs, zonder afstanden. De documenten geven geen adres of coördinaten van het perceel, dus de kaart toont het gebied El Rosario.',
  'Broszura umiejscawia kompleks w Marbelli, obok chronionego systemu wydm El Barronal de la Morena, który lokalizuje w rejonie El Rosario - Las Chapas, i przedstawia projekt jako życie tuż przy plaży. Jej mapa lokalizacji pokazuje centrum Marbelli, przystań w Marbelli, przystań w Cabopino, Puerto Banús, Nueva Andalucía i kilka klubów golfowych, bez odległości. Dokumenty nie podają adresu ani współrzędnych działki, dlatego mapa pokazuje rejon El Rosario.',
  'Brosjyren plasserer anlegget i Marbella, ved siden av det vernede dynesystemet El Barronal de la Morena, som den plasserer i området El Rosario - Las Chapas, og presenterer prosjektet som liv helt ved stranden. Lokaliseringskartet viser sentrum av Marbella, marinaen i Marbella, marinaen i Cabopino, Puerto Banús, Nueva Andalucía og flere golfklubber, uten avstander. Dokumentene oppgir verken adresse eller koordinater for tomten, så kartet viser området El Rosario.',
  'Broschyren placerar området i Marbella, intill det skyddade dynsystemet El Barronal de la Morena, som den placerar i området El Rosario - Las Chapas, och presenterar projektet som boende vid stranden. Lägeskartan visar Marbellas centrum, marinan i Marbella, marinan i Cabopino, Puerto Banús, Nueva Andalucía och flera golfklubbar, utan avstånd. Dokumenten anger varken adress eller koordinater för tomten, så kartan visar området El Rosario.')

# ---- investment, checks, availability -------------------------------------------------------------

a('.investment.cards[0][1]',
  'Hay dos viviendas publicadas: la villa Nr. 04 por {E5400000} y el apartamento Nr. 202 por {E5200000}, ambos más IVA. La lista de precios del 1 de julio de 2026 marcaba la Nr. 04 como reservada, por lo que confirmamos que sigue disponible.',
  'Deux logements sont présentés : la villa Nr. 04 à {E5400000} et l’appartement Nr. 202 à {E5200000}, tous deux hors TVA. La liste de prix du 1er juillet 2026 marquait la Nr. 04 comme réservée ; nous confirmons donc qu’elle est toujours disponible.',
  'Zwei Immobilien sind gelistet: die Villa Nr. 04 für {E5400000} und die Wohnung Nr. 202 für {E5200000}, beide zuzüglich MwSt. Die Preisliste vom 1. Juli 2026 kennzeichnete Nr. 04 als reserviert, deshalb bestätigen wir, dass sie weiterhin verfügbar ist.',
  'В списке два объекта: вилла Nr. 04 за {E5400000} и квартира Nr. 202 за {E5200000}, оба без НДС. В прайс-листе от 1 июля 2026 года Nr. 04 была отмечена как забронированная, поэтому мы подтверждаем, что она по-прежнему доступна.',
  'هناك مسكنان مدرجان: الفيلا Nr. 04 بسعر {E5400000} والشقة Nr. 202 بسعر {E5200000}، كلاهما دون ضريبة القيمة المضافة. كانت قائمة الأسعار بتاريخ 1 يوليو 2026 تضع Nr. 04 كمحجوزة، لذلك نؤكد أنها ما زالت متاحة.',
  'Twee woningen zijn vermeld: villa Nr. 04 voor {E5400000} en appartement Nr. 202 voor {E5200000}, beide excl. btw. De prijslijst van 1 juli 2026 markeerde Nr. 04 als gereserveerd, dus wij bevestigen dat ze nog beschikbaar is.',
  'Na liście są dwa lokale: willa Nr. 04 za {E5400000} i mieszkanie Nr. 202 za {E5200000}, oba plus VAT. Cennik z 1 lipca 2026 r. oznaczał Nr. 04 jako zarezerwowany, dlatego potwierdzamy, że nadal jest dostępny.',
  'To boliger er oppført: villa Nr. 04 til {E5400000} og leilighet Nr. 202 til {E5200000}, begge pluss mva. Prislisten fra 1. juli 2026 markerte Nr. 04 som reservert, så vi bekrefter at den fortsatt er ledig.',
  'Två bostäder är listade: villa Nr. 04 för {E5400000} och lägenhet Nr. 202 för {E5200000}, båda plus IVA. Prislistan från den 1 juli 2026 markerade Nr. 04 som reserverad, så vi bekräftar att den fortfarande är ledig.')
a('.investment.cards[1][1]',
  'La lista de precios indica que sus precios son netos y no incluyen el IVA ni los impuestos de transmisión de la propiedad. Nueva Living confirma por escrito el tipo y los gastos de compra.',
  'La liste de prix indique que ses prix sont nets et n’incluent ni la TVA (IVA) ni les droits de mutation. Nueva Living confirme par écrit le taux et les frais d’achat.',
  'Die Preisliste besagt, dass ihre Preise netto sind und weder die MwSt. (IVA) noch die Grunderwerbsteuern enthalten. Nueva Living bestätigt den Satz und die Kaufnebenkosten schriftlich.',
  'В прайс-листе сказано, что цены указаны нетто и не включают испанский НДС и налоги на переход права собственности. Ставку и расходы на покупку Nueva Living подтверждает письменно.',
  'تنصّ قائمة الأسعار على أن أسعارها صافية ولا تشمل ضريبة القيمة المضافة (IVA) ولا ضرائب نقل الملكية. وتؤكد Nueva Living النسبة وتكاليف الشراء كتابةً.',
  'De prijslijst zegt dat haar prijzen netto zijn en geen Spaanse btw en geen overdrachtsbelasting bevatten. Nueva Living bevestigt het tarief en de aankoopkosten schriftelijk.',
  'Cennik zastrzega, że jego ceny są netto i nie zawierają hiszpańskiego VAT ani podatków od przeniesienia własności. Stawkę i koszty zakupu Nueva Living potwierdza na piśmie.',
  'Prislisten sier at prisene er netto og ikke inkluderer spansk mva. eller dokumentavgift ved overdragelse. Nueva Living bekrefter satsen og kjøpskostnadene skriftlig.',
  'Prislistan anger att priserna är nettopriser och inte inkluderar IVA (spansk moms) eller skatter vid överlåtelse av fastigheten. Nueva Living bekräftar skattesatsen och köpkostnaderna skriftligen.')
a('.investment.cards[3][1]',
  'La lista de precios indica 2 plazas de aparcamiento para la Nr. 04 y 2+1 para la Nr. 202, con trastero en ambas. El plano de la Nr. 202 muestra una plaza abierta y un trastero exterior marcados como extra, por lo que confirmamos qué incluye el precio.',
  'La liste de prix indique 2 places de stationnement pour la Nr. 04 et 2+1 pour la Nr. 202, avec un cellier pour les deux. Le plan de la Nr. 202 montre une place ouverte et un cellier extérieur marqués comme supplément ; nous confirmons donc ce que le prix comprend.',
  'Die Preisliste gibt 2 Stellplätze für Nr. 04 und 2+1 für Nr. 202 an, jeweils mit Abstellraum. Der Plan von Nr. 202 zeigt einen offenen Stellplatz und einen Außenabstellraum, die als Extra gekennzeichnet sind; wir bestätigen daher, was der Preis umfasst.',
  'В прайс-листе указаны 2 парковочных места для Nr. 04 и 2+1 для Nr. 202, с кладовой в обоих случаях. На плане Nr. 202 открытое парковочное место и наружная кладовая помечены как дополнительные, поэтому мы уточняем, что входит в цену.',
  'تذكر قائمة الأسعار موقفَي سيارات لـ Nr. 04 و2+1 لـ Nr. 202، مع غرفة تخزين لكليهما. ويُظهر مخطط Nr. 202 موقفًا مكشوفًا وغرفة تخزين خارجية موسومين بأنهما إضافيان، لذلك نؤكد ما يشمله السعر.',
  'De prijslijst geeft 2 parkeerplaatsen voor Nr. 04 en 2+1 voor Nr. 202, met een berging voor beide. De plattegrond van Nr. 202 toont een open parkeerplaats en een buitenberging die als extra zijn gemarkeerd, dus wij bevestigen wat de prijs omvat.',
  'Cennik podaje 2 miejsca parkingowe dla Nr. 04 i 2+1 dla Nr. 202, z komórką lokatorską w obu przypadkach. Rzut Nr. 202 pokazuje otwarte miejsce parkingowe i zewnętrzną komórkę oznaczone jako dodatkowe, dlatego potwierdzamy, co obejmuje cena.',
  'Prislisten oppgir 2 parkeringsplasser for Nr. 04 og 2+1 for Nr. 202, med bod for begge. Plantegningen av Nr. 202 viser en åpen parkeringsplass og en utvendig bod som er merket som tillegg, så vi bekrefter hva prisen omfatter.',
  'Prislistan anger 2 parkeringsplatser för Nr. 04 och 2+1 för Nr. 202, med förråd för båda. Planritningen för Nr. 202 visar en öppen parkeringsplats och ett utvändigt förråd som är markerade som extra, så vi bekräftar vad priset omfattar.')
a('.trustDossier.cards[0][0]', 'La antigüedad de los documentos', 'L’ancienneté des documents', 'Das Alter der Unterlagen', 'Возраст документов', 'عمر الوثائق', 'De ouderdom van de documenten', 'Wiek dokumentów', 'Dokumentenes alder', 'Dokumentens ålder')
a('.trustDossier.cards[0][1]',
  'El folleto y la memoria de calidades son de agosto de 2024. Los usamos para describir el proyecto y no como prueba de lo que está disponible o construido hoy, y pedimos los actuales.',
  'La brochure et le descriptif des prestations datent d’août 2024. Nous les utilisons pour décrire le projet et non comme preuve de ce qui est disponible ou construit aujourd’hui, et nous demandons les documents actuels.',
  'Die Broschüre und die Baubeschreibung stammen von August 2024. Wir nutzen sie, um das Projekt zu beschreiben, und nicht als Beleg dafür, was heute verfügbar oder gebaut ist, und fordern die aktuellen Unterlagen an.',
  'Брошюра и спецификация качества датированы августом 2024 года. Мы используем их для описания проекта, а не как подтверждение того, что доступно или построено сегодня, и запрашиваем актуальные документы.',
  'الكتيّب ومواصفات الجودة من أغسطس 2024. نستخدمهما لوصف المشروع وليس كدليل على ما هو متاح أو مبني اليوم، ونطلب الوثائق الحالية.',
  'De brochure en de kwaliteitsomschrijving zijn van augustus 2024. Wij gebruiken ze om het project te beschrijven en niet als bewijs van wat er vandaag beschikbaar of gebouwd is, en vragen de actuele documenten op.',
  'Broszura i opis standardu wykończenia pochodzą z sierpnia 2024 r. Używamy ich do opisu projektu, a nie jako dowodu tego, co jest dziś dostępne lub zbudowane, i prosimy o aktualne dokumenty.',
  'Brosjyren og kvalitetsbeskrivelsen er fra august 2024. Vi bruker dem til å beskrive prosjektet og ikke som bevis på hva som er tilgjengelig eller bygget i dag, og vi ber om de aktuelle dokumentene.',
  'Broschyren och kvalitetsbeskrivningen är från augusti 2024. Vi använder dem för att beskriva projektet och inte som bevis på vad som är tillgängligt eller byggt i dag, och vi begär de aktuella dokumenten.')
a('.trustDossier.cards[1][1]',
  'Ningún documento del promotor indica una fecha de entrega. La lista de ventas muestra el proyecto como en construcción, así que pedimos la fecha contractual, el estado de la licencia y el estado de las obras.',
  'Aucun document du promoteur ne donne de date de livraison. La liste de vente présente le projet comme en construction ; nous demandons donc la date contractuelle, le statut du permis et l’état d’avancement du chantier.',
  'Keines der Dokumente des Bauträgers nennt einen Fertigstellungstermin. Die Verkaufsliste zeigt das Projekt als im Bau, deshalb fordern wir den vertraglichen Termin, den Stand der Baugenehmigung und den Baufortschritt an.',
  'Ни в одном документе застройщика не указан срок сдачи. В списке продаж проект значится как строящийся, поэтому мы запрашиваем договорную дату, статус разрешения на строительство и стадию работ.',
  'لا تذكر أي من وثائق المطوّر موعدًا للتسليم. وتُظهر قائمة المبيعات المشروع قيد الإنشاء، لذلك نطلب الموعد التعاقدي وحالة الرخصة ومرحلة الأعمال.',
  'Geen van de documenten van de ontwikkelaar noemt een opleveringsdatum. De verkooplijst toont het project als in aanbouw, dus wij vragen de contractuele datum, de status van de vergunning en de bouwfase op.',
  'Żaden z dokumentów dewelopera nie podaje terminu oddania. Lista sprzedażowa pokazuje projekt jako w budowie, dlatego prosimy o termin umowny, status pozwolenia na budowę i etap prac.',
  'Ingen av utbyggerens dokumenter oppgir en overleveringsdato. Salgslisten viser prosjektet som under bygging, så vi ber om den kontraktfestede datoen, status for byggetillatelsen og byggestadiet.',
  'Inget av exploatörens dokument anger ett leveransdatum. Försäljningslistan visar projektet som under byggnation, så vi begär det avtalade datumet, bygglovets status och byggstadiet.')
a('.trustDossier.cards[2][0]', '¿Está disponible la Nr. 04?', 'La Nr. 04 est-elle disponible ?', 'Ist Nr. 04 verfügbar?', 'Доступна ли Nr. 04?', 'هل Nr. 04 متاحة؟', 'Is Nr. 04 beschikbaar?', 'Czy Nr. 04 jest dostępna?', 'Er Nr. 04 ledig?', 'Är Nr. 04 ledig?')
a('.trustDossier.cards[2][1]',
  'La lista del 29 de octubre de 2026 muestra la Nr. 04 por {E5400000} como disponible. La lista de precios del 1 de julio de 2026 la marca como reservada y no da precio. Esta página sigue la lista más reciente, y confirmamos el estado antes de cualquier reserva.',
  'La liste du 29 octobre 2026 présente la Nr. 04 à {E5400000} comme disponible. La liste de prix du 1er juillet 2026 la marque comme réservée et n’indique pas de prix. Cette page suit la liste la plus récente, et nous confirmons le statut avant toute réservation.',
  'Die Liste vom 29. Oktober 2026 zeigt Nr. 04 für {E5400000} als verfügbar. Die Preisliste vom 1. Juli 2026 kennzeichnet sie als reserviert und nennt keinen Preis. Diese Seite folgt der späteren Liste, und wir bestätigen den Status vor jeder Reservierung.',
  'В списке от 29 октября 2026 года Nr. 04 значится доступной по цене {E5400000}. В прайс-листе от 1 июля 2026 года она отмечена как забронированная, и цена не указана. Эта страница следует более позднему списку, а статус мы подтверждаем перед любым бронированием.',
  'تُظهر قائمة 29 أكتوبر 2026 المسكن Nr. 04 بسعر {E5400000} كمتاح. وتضعه قائمة الأسعار بتاريخ 1 يوليو 2026 كمحجوز ولا تذكر له سعرًا. تتبع هذه الصفحة القائمة الأحدث، ونؤكد الحالة قبل أي حجز.',
  'De lijst van 29 oktober 2026 toont Nr. 04 voor {E5400000} als beschikbaar. De prijslijst van 1 juli 2026 markeert haar als gereserveerd en geeft geen prijs. Deze pagina volgt de latere lijst, en wij bevestigen de status vóór elke reservering.',
  'Lista z 29 października 2026 r. pokazuje Nr. 04 za {E5400000} jako dostępną. Cennik z 1 lipca 2026 r. oznacza ją jako zarezerwowaną i nie podaje ceny. Ta strona opiera się na późniejszej liście, a status potwierdzamy przed każdą rezerwacją.',
  'Listen fra 29. oktober 2026 viser Nr. 04 til {E5400000} som ledig. Prislisten fra 1. juli 2026 markerer den som reservert og oppgir ingen pris. Denne siden følger den senere listen, og vi bekrefter statusen før enhver reservasjon.',
  'Listan från den 29 oktober 2026 visar Nr. 04 för {E5400000} som ledig. Prislistan från den 1 juli 2026 markerar den som reserverad och anger inget pris. Den här sidan följer den senare listan, och vi bekräftar statusen före varje reservation.')
a('.trustDossier.cards[3][1]',
  'La lista del 29 de octubre de 2026 indica 397,7 m² construidos para la Nr. 04 y 285,69 m² para la Nr. 202. Los planos y la lista de precios del 1 de julio de 2026 indican 447,13 y 483,98 m², y el folleto de 2024 indica 436,96 m² para su tipo de villa A2 y 487,08 m² para su tipo de apartamento con jardín B2. Esta página usa los planos, que coinciden con la lista de precios, y confirmamos qué cifras usa el contrato. Para la Nr. 04, la lista de precios indica 355,90 m² útiles y 320,34 m² útiles exteriores, y el plano 354,43 y 280,89 m².',
  'La liste du 29 octobre 2026 indique 397,7 m² construits pour la Nr. 04 et 285,69 m² pour la Nr. 202. Les plans et la liste de prix du 1er juillet 2026 indiquent 447,13 et 483,98 m², et la brochure de 2024 indique 436,96 m² pour son type de villa A2 et 487,08 m² pour son type d’appartement avec jardin B2. Cette page utilise les plans, qui concordent avec la liste de prix, et nous confirmons les chiffres retenus par le contrat. Pour la Nr. 04, la liste de prix indique 355,90 m² utiles et 320,34 m² utiles extérieurs, et le plan 354,43 et 280,89 m².',
  'Die Liste vom 29. Oktober 2026 gibt 397,7 m² Baufläche für Nr. 04 und 285,69 m² für Nr. 202 an. Die Pläne und die Preisliste vom 1. Juli 2026 geben 447,13 und 483,98 m² an, und die Broschüre von 2024 nennt 436,96 m² für ihren Villentyp A2 und 487,08 m² für ihren Gartenwohnungstyp B2. Diese Seite verwendet die Pläne, die mit der Preisliste übereinstimmen, und wir bestätigen, welche Werte der Vertrag zugrunde legt. Für Nr. 04 gibt die Preisliste 355,90 m² Nutzfläche und 320,34 m² Außennutzfläche an, der Plan 354,43 und 280,89 m².',
  'В списке от 29 октября 2026 года для Nr. 04 указано 397,7 м² застройки, для Nr. 202 — 285,69 м². В планах и в прайс-листе от 1 июля 2026 года — 447,13 и 483,98 м², а в брошюре 2024 года — 436,96 м² для её типа вилл A2 и 487,08 м² для её типа садовых квартир B2. Эта страница использует планы, которые совпадают с прайс-листом, а какие цифры берёт за основу договор, мы уточняем. Для Nr. 04 в прайс-листе указано 355,90 м² полезной площади и 320,34 м² полезной площади вне дома, на плане — 354,43 и 280,89 м².',
  'تذكر قائمة 29 أكتوبر 2026 مساحة مبنية 397.7 م² لـ Nr. 04 و285.69 م² لـ Nr. 202. أما المخططات وقائمة الأسعار بتاريخ 1 يوليو 2026 فتذكر 447.13 و483.98 م²، ويذكر كتيّب 2024 مساحة 436.96 م² لنوع الفلل A2 فيه و487.08 م² لنوع شقق الحدائق B2 فيه. تعتمد هذه الصفحة المخططات التي تتفق مع قائمة الأسعار، ونؤكد الأرقام التي يعتمدها العقد. وبالنسبة إلى Nr. 04، تذكر قائمة الأسعار 355.90 م² صافية و320.34 م² صافية خارجية، والمخطط 354.43 و280.89 م².',
  'De lijst van 29 oktober 2026 geeft 397,7 m² bebouwd voor Nr. 04 en 285,69 m² voor Nr. 202. De plattegronden en de prijslijst van 1 juli 2026 geven 447,13 en 483,98 m², en de brochure van 2024 geeft 436,96 m² voor haar villatype A2 en 487,08 m² voor haar tuinappartementtype B2. Deze pagina gebruikt de plattegronden, die overeenkomen met de prijslijst, en wij bevestigen welke cijfers het contract hanteert. Voor Nr. 04 geeft de prijslijst 355,90 m² nuttig en 320,34 m² nuttig buiten, en de plattegrond 354,43 en 280,89 m².',
  'Lista z 29 października 2026 r. podaje 397,7 m² zabudowy dla Nr. 04 i 285,69 m² dla Nr. 202. Rzuty i cennik z 1 lipca 2026 r. podają 447,13 i 483,98 m², a broszura z 2024 r. podaje 436,96 m² dla typu willi A2 i 487,08 m² dla typu mieszkania z ogrodem B2. Ta strona opiera się na rzutach, które zgadzają się z cennikiem, a które liczby przyjmuje umowa, potwierdzamy. Dla Nr. 04 cennik podaje 355,90 m² powierzchni użytkowej i 320,34 m² powierzchni użytkowej zewnętrznej, a rzut 354,43 i 280,89 m².',
  'Listen fra 29. oktober 2026 oppgir 397,7 m² bebygd for Nr. 04 og 285,69 m² for Nr. 202. Plantegningene og prislisten fra 1. juli 2026 oppgir 447,13 og 483,98 m², og brosjyren fra 2024 oppgir 436,96 m² for villatypen A2 og 487,08 m² for hageleilighetstypen B2. Denne siden bruker plantegningene, som stemmer med prislisten, og vi bekrefter hvilke tall kontrakten legger til grunn. For Nr. 04 oppgir prislisten 355,90 m² bruksareal og 320,34 m² utvendig bruksareal, og plantegningen 354,43 og 280,89 m².',
  'Listan från den 29 oktober 2026 anger 397,7 m² byggyta för Nr. 04 och 285,69 m² för Nr. 202. Planritningarna och prislistan från den 1 juli 2026 anger 447,13 och 483,98 m², och broschyren från 2024 anger 436,96 m² för sin villatyp A2 och 487,08 m² för sin trädgårdslägenhetstyp B2. Den här sidan använder planritningarna, som stämmer med prislistan, och vi bekräftar vilka siffror avtalet utgår från. För Nr. 04 anger prislistan 355,90 m² boarea och 320,34 m² användbar yta utomhus, och planritningen 354,43 och 280,89 m².')
a('.trustDossier.cards[4][0]', 'Las fotografías', 'Les photographies', 'Die Fotos', 'Фотографии', 'الصور', 'De foto’s', 'Zdjęcia', 'Fotografiene', 'Fotografierna')
a('.trustDossier.cards[4][1]',
  'Las fotografías muestran una vivienda amueblada con terraza y piscina en la azotea. La galería no indica de qué vivienda o tipo se trata, por lo que no damos por hecho que muestren la Nr. 04 o la Nr. 202, y confirmamos los acabados de la vivienda que usted elija con la memoria de calidades.',
  'Les photographies montrent un logement meublé avec une terrasse et une piscine sur le toit. La galerie ne précise ni de quel logement ni de quel type il s’agit ; nous ne supposons donc pas qu’elles montrent la Nr. 04 ou la Nr. 202, et nous confirmons les finitions du logement que vous choisissez par rapport au descriptif.',
  'Die Fotos zeigen eine möblierte Wohnung mit Dachterrasse und Pool. Die Galerie sagt nicht, um welche Wohnung oder welchen Typ es sich handelt; wir gehen daher nicht davon aus, dass sie Nr. 04 oder Nr. 202 zeigen, und gleichen die Ausstattung der von Ihnen gewählten Immobilie mit der Baubeschreibung ab.',
  'На фотографиях — меблированное жильё с террасой и бассейном на крыше. В галерее не указано, какое это жильё и какого типа, поэтому мы не считаем, что на них Nr. 04 или Nr. 202, и сверяем отделку выбранного вами жилья со спецификацией.',
  'تُظهر الصور مسكنًا مفروشًا بتراس ومسبح على السطح. لا يذكر المعرض أي مسكن أو أي نوع هو، لذلك لا نفترض أنها تُظهر Nr. 04 أو Nr. 202، ونؤكد تشطيبات المسكن الذي تختاره بالرجوع إلى المواصفات.',
  'De foto’s tonen een gemeubileerde woning met een dakterras en een zwembad. De galerij zegt niet om welke woning of welk type het gaat, dus wij gaan er niet van uit dat ze Nr. 04 of Nr. 202 tonen, en wij toetsen de afwerking van de woning die u kiest aan de kwaliteitsomschrijving.',
  'Zdjęcia przedstawiają umeblowany lokal z tarasem i basenem na dachu. Galeria nie podaje, o jaki lokal lub typ chodzi, dlatego nie zakładamy, że pokazują Nr. 04 lub Nr. 202, a wykończenie wybranego lokalu potwierdzamy z opisem standardu.',
  'Bildene viser en møblert bolig med takterrasse og basseng. Galleriet oppgir ikke hvilken bolig eller hvilken type det er, så vi antar ikke at de viser Nr. 04 eller Nr. 202, og vi bekrefter ferdigstillelsen av boligen dere velger mot kvalitetsbeskrivelsen.',
  'Bilderna visar en möblerad bostad med takterrass och pool. Galleriet anger inte vilken bostad eller vilken typ det är, så vi utgår inte från att de visar Nr. 04 eller Nr. 202, och vi bekräftar finishen i bostaden ni väljer mot kvalitetsbeskrivningen.')
a('.trustDossier.cards[5][0]', 'Cambios en la distribución', 'Modifier la distribution', 'Änderung des Grundrisses', 'Изменение планировки', 'تعديل التوزيع', 'De indeling wijzigen', 'Zmiana układu', 'Endring av planløsningen', 'Ändring av planlösningen')
a('.trustDossier.cards[5][1]',
  'El folleto dice que los compradores de la primera fase pueden elegir la distribución de los espacios. No dice si eso se aplica a estas dos viviendas, así que lo preguntamos.',
  'La brochure indique que les acheteurs de la première phase peuvent choisir la distribution des espaces. Elle ne précise pas si cela s’applique à ces deux logements ; nous posons donc la question.',
  'Die Broschüre sagt, dass Käufer der ersten Phase die Aufteilung der Räume wählen können. Sie sagt nicht, ob das für diese beiden Immobilien gilt, deshalb fragen wir nach.',
  'В брошюре сказано, что покупатели первой очереди могут выбрать распределение помещений. Не сказано, относится ли это к этим двум объектам, поэтому мы уточняем.',
  'يقول الكتيّب إن مشتري المرحلة الأولى يمكنهم اختيار توزيع المساحات. ولا يذكر ما إذا كان ذلك ينطبق على هذين المسكنين، لذلك نسأل.',
  'De brochure zegt dat kopers in de eerste fase de indeling van de ruimten kunnen kiezen. Ze zegt niet of dat voor deze twee woningen geldt, dus wij vragen het na.',
  'Broszura mówi, że kupujący z pierwszego etapu mogą wybrać rozkład pomieszczeń. Nie podaje, czy dotyczy to tych dwóch lokali, dlatego o to pytamy.',
  'Brosjyren sier at kjøpere i første fase kan velge fordelingen av rommene. Den sier ikke om det gjelder for disse to boligene, så vi spør.',
  'Broschyren säger att köpare i den första fasen kan välja fördelningen av utrymmena. Den säger inte om det gäller för dessa två bostäder, så vi frågar.')
a('.trustDossier.cards[6][0]', 'La memoria de calidades y la certificación', 'Le descriptif et la certification', 'Die Baubeschreibung und die Zertifizierung', 'Спецификация и сертификация', 'مواصفات الجودة والشهادة', 'De kwaliteitsomschrijving en de certificering', 'Opis standardu i certyfikacja', 'Kvalitetsbeskrivelsen og sertifiseringen', 'Kvalitetsbeskrivningen och certifieringen')
a('.trustDossier.cards[6][1]',
  'La memoria de calidades se abre con una página que explica la certificación BREEAM. No indica una calificación ni un certificado para este proyecto, por lo que esta página no los enumera.',
  'Le descriptif s’ouvre sur une page qui explique la certification BREEAM. Il n’indique ni note ni certificat pour ce projet ; cette page n’en mentionne donc aucun.',
  'Die Baubeschreibung beginnt mit einer Seite, die die BREEAM-Zertifizierung erklärt. Sie nennt für dieses Projekt weder eine Bewertung noch ein Zertifikat, daher führt diese Seite keines auf.',
  'Спецификация качества начинается со страницы, где объясняется сертификация BREEAM. Рейтинг или сертификат для этого проекта в ней не указаны, поэтому на этой странице они не перечислены.',
  'تبدأ مواصفات الجودة بصفحة تشرح شهادة BREEAM. ولا تذكر تقييمًا ولا شهادة لهذا المشروع، لذلك لا تدرجهما هذه الصفحة.',
  'De kwaliteitsomschrijving opent met een pagina die de BREEAM-certificering uitlegt. Ze noemt geen beoordeling en geen certificaat voor dit project, dus deze pagina vermeldt er geen.',
  'Opis standardu wykończenia otwiera strona wyjaśniająca certyfikację BREEAM. Nie podaje oceny ani certyfikatu dla tego projektu, dlatego ta strona żadnego nie wymienia.',
  'Kvalitetsbeskrivelsen åpner med en side som forklarer BREEAM-sertifisering. Den oppgir verken en vurdering eller et sertifikat for dette prosjektet, så denne siden lister ingen.',
  'Kvalitetsbeskrivningen inleds med en sida som förklarar BREEAM-certifiering. Den anger varken ett betyg eller ett certifikat för det här projektet, så den här sidan listar inget.')
a('.trustDossier.cards[7][0]', 'El mapa', 'La carte', 'Die Karte', 'Карта', 'الخريطة', 'De kaart', 'Mapa', 'Kartet', 'Kartan')
a('.trustDossier.cards[7][1]',
  'Los documentos no dan dirección ni coordenadas, por lo que el marcador del mapa está en El Rosario según la zona y no en la parcela, y las distancias por carretera junto al mapa se miden desde ese marcador. El folleto presenta el proyecto en primera línea de playa, por lo que la distancia a la playa en particular no es la de la parcela, y el folleto no da distancias propias. Las confirmamos en una visita.',
  'Les documents ne donnent ni adresse ni coordonnées ; le repère sur la carte se trouve donc à El Rosario, par secteur, et non sur la parcelle, et les distances routières à côté de la carte sont mesurées depuis ce repère. La brochure présente le projet en bord de mer ; la distance à la plage en particulier n’est donc pas celle de la parcelle, et la brochure ne donne pas de distances propres. Nous les confirmons lors d’une visite.',
  'Die Unterlagen nennen weder Adresse noch Koordinaten, daher liegt die Markierung auf der Karte nach Gebiet in El Rosario und nicht auf dem Grundstück, und die Straßenentfernungen neben der Karte sind von dieser Markierung aus gemessen. Die Broschüre beschreibt das Projekt als direkt am Strand gelegen, daher ist besonders die Entfernung zum Strand nicht die vom Grundstück, und die Broschüre nennt selbst keine Entfernungen. Wir bestätigen sie bei einer Besichtigung.',
  'В документах нет ни адреса, ни координат, поэтому отметка на карте стоит в районе Эль-Росарио, а не на участке, а расстояния по дорогам рядом с картой измерены от этой отметки. В брошюре проект назван расположенным на первой линии у пляжа, поэтому прежде всего расстояние до пляжа — не расстояние от участка, а собственных расстояний брошюра не приводит. Мы уточняем их во время визита.',
  'لا تذكر الوثائق عنوانًا ولا إحداثيات، لذلك فإن العلامة على الخريطة في إل روساريو بحسب المنطقة وليست على قطعة الأرض، وتُقاس مسافات الطرق بجانب الخريطة انطلاقًا من هذه العلامة. ويقدّم الكتيّب المشروع على الواجهة البحرية، لذلك فإن المسافة إلى الشاطئ خصوصًا ليست مسافة قطعة الأرض، ولا يذكر الكتيّب مسافات من عنده. ونؤكدها أثناء الزيارة.',
  'De documenten geven geen adres of coördinaten, dus de markering op de kaart staat per gebied in El Rosario en niet op het perceel, en de wegafstanden naast de kaart zijn vanaf die markering gemeten. De brochure beschrijft het project als direct aan het strand, dus met name de afstand tot het strand is niet die vanaf het perceel, en de brochure geeft zelf geen afstanden. Die bevestigen we bij een bezichtiging.',
  'Dokumenty nie podają adresu ani współrzędnych, dlatego znacznik na mapie znajduje się według rejonu w El Rosario, a nie na działce, a odległości drogowe obok mapy są mierzone od tego znacznika. Broszura opisuje projekt jako położony tuż przy plaży, więc zwłaszcza odległość do plaży nie jest odległością od działki, a sama broszura nie podaje odległości. Potwierdzamy je podczas wizyty.',
  'Dokumentene oppgir verken adresse eller koordinater, så markøren på kartet ligger etter område i El Rosario og ikke på tomten, og veiavstandene ved siden av kartet er målt fra denne markøren. Brosjyren beskriver prosjektet som helt ved stranden, så særlig avstanden til stranden er ikke avstanden fra tomten, og brosjyren oppgir ingen egne avstander. Dem bekrefter vi på en visning.',
  'Dokumenten anger varken adress eller koordinater, så markören på kartan ligger efter område i El Rosario och inte på tomten, och vägavstånden bredvid kartan är mätta från den markören. Broschyren beskriver projektet som beläget vid stranden, så särskilt avståndet till stranden är inte avståndet från tomten, och broschyren anger inga egna avstånd. Dem bekräftar vi vid ett besök.')
put('29 October 2026', ['29 de octubre de 2026', '29 octobre 2026', '29. Oktober 2026', '29 октября 2026 года', '29 أكتوبر 2026',
                        '29 oktober 2026', '29 października 2026', '29. oktober 2026', '29 oktober 2026'])
a('.availability.copy',
  'Hay dos viviendas publicadas con precio: la villa Nr. 04, de cuatro dormitorios, y el apartamento Nr. 202, de tres. Los precios son los de la lista del 29 de octubre de 2026 y no incluyen el IVA, y confirmamos la disponibilidad y el precio antes de cualquier reserva. La lista de precios del 1 de julio de 2026 mostraba la Nr. 04 como reservada.',
  'Deux logements sont présentés avec un prix : la villa Nr. 04, de quatre chambres, et l’appartement Nr. 202, de trois. Les prix sont ceux de la liste du 29 octobre 2026 et s’entendent hors TVA ; nous confirmons la disponibilité et le prix avant toute réservation. La liste de prix du 1er juillet 2026 présentait la Nr. 04 comme réservée.',
  'Zwei Immobilien sind mit Preis gelistet: die Villa Nr. 04 mit vier und die Wohnung Nr. 202 mit drei Schlafzimmern. Die Preise stammen aus der Liste vom 29. Oktober 2026 und verstehen sich zuzüglich MwSt.; Verfügbarkeit und Preis bestätigen wir vor jeder Reservierung. Die Preisliste vom 1. Juli 2026 zeigte Nr. 04 als reserviert.',
  'Два объекта указаны с ценой: вилла Nr. 04 с четырьмя спальнями и квартира Nr. 202 с тремя. Цены взяты из списка от 29 октября 2026 года и указаны без НДС; наличие и цену мы подтверждаем перед любым бронированием. В прайс-листе от 1 июля 2026 года Nr. 04 была показана как забронированная.',
  'هناك مسكنان مدرجان بسعر: الفيلا Nr. 04 بأربع غرف نوم والشقة Nr. 202 بثلاث. الأسعار هي المذكورة في قائمة 29 أكتوبر 2026 ولا تشمل ضريبة القيمة المضافة، ونؤكد التوفر والسعر قبل أي حجز. وكانت قائمة الأسعار بتاريخ 1 يوليو 2026 تُظهر Nr. 04 كمحجوزة.',
  'Twee woningen zijn met een prijs vermeld: villa Nr. 04 met vier slaapkamers en appartement Nr. 202 met drie. De prijzen zijn die van de lijst van 29 oktober 2026 en zijn exclusief btw, en wij bevestigen de beschikbaarheid en de prijs vóór elke reservering. De prijslijst van 1 juli 2026 toonde Nr. 04 als gereserveerd.',
  'Dwa lokale mają podaną cenę: willa Nr. 04 z czterema sypialniami i mieszkanie Nr. 202 z trzema. Ceny pochodzą z listy z 29 października 2026 r. i nie zawierają VAT; dostępność i cenę potwierdzamy przed każdą rezerwacją. Cennik z 1 lipca 2026 r. pokazywał Nr. 04 jako zarezerwowaną.',
  'To boliger er oppført med pris: villa Nr. 04 med fire soverom og leilighet Nr. 202 med tre. Prisene er de fra listen fra 29. oktober 2026 og inkluderer ikke mva.; vi bekrefter tilgjengelighet og pris før enhver reservasjon. Prislisten fra 1. juli 2026 viste Nr. 04 som reservert.',
  'Två bostäder är listade med pris: villa Nr. 04 med fyra sovrum och lägenhet Nr. 202 med tre. Priserna är de från listan från den 29 oktober 2026 och inkluderar inte IVA; tillgänglighet och pris bekräftar vi före varje reservation. Prislistan från den 1 juli 2026 visade Nr. 04 som reserverad.')
a('.availability.sourceNote',
  'La disponibilidad, los precios y los dormitorios proceden de la lista de ventas del 29 de octubre de 2026, que recoge dos viviendas. Las superficies construidas, las terrazas y las estancias proceden de los planos del promotor, que coinciden con la lista de precios del 1 de julio de 2026; la lista de ventas indica superficies construidas menores para ambas viviendas. Esa lista de precios indica que sus precios son netos y no incluyen el IVA, y marca la Nr. 04 como reservada.',
  'La disponibilité, les prix et les chambres proviennent de la liste de vente du 29 octobre 2026, qui comporte deux logements. Les surfaces construites, les terrasses et les pièces proviennent des plans du promoteur, qui concordent avec la liste de prix du 1er juillet 2026 ; la liste de vente indique des surfaces construites plus petites pour les deux logements. Cette liste de prix indique que ses prix sont nets et n’incluent pas la TVA, et elle marque la Nr. 04 comme réservée.',
  'Verfügbarkeit, Preise und Schlafzimmer stammen aus der Verkaufsliste vom 29. Oktober 2026, die zwei Immobilien enthält. Die Bauflächen, Terrassen und Räume stammen aus den Plänen des Bauträgers, die mit der Preisliste vom 1. Juli 2026 übereinstimmen; die Verkaufsliste nennt für beide Immobilien kleinere Bauflächen. Diese Preisliste besagt, dass ihre Preise netto sind und die MwSt. nicht enthalten, und kennzeichnet Nr. 04 als reserviert.',
  'Наличие, цены и число спален взяты из списка продаж от 29 октября 2026 года, в котором два объекта. Площади застройки, террасы и помещения взяты из планов застройщика, которые совпадают с прайс-листом от 1 июля 2026 года; в списке продаж для обоих объектов указаны меньшие площади застройки. В этом прайс-листе сказано, что цены указаны нетто и не включают НДС, и Nr. 04 отмечена в нём как забронированная.',
  'التوفر والأسعار وغرف النوم مأخوذة من قائمة المبيعات بتاريخ 29 أكتوبر 2026، وفيها مسكنان. أما المساحات المبنية والتراسات والغرف فمن مخططات المطوّر، وهي تتفق مع قائمة الأسعار بتاريخ 1 يوليو 2026؛ وتذكر قائمة المبيعات مساحات مبنية أصغر للمسكنين. وتنصّ قائمة الأسعار تلك على أن أسعارها صافية ولا تشمل ضريبة القيمة المضافة، وتضع Nr. 04 كمحجوزة.',
  'De beschikbaarheid, de prijzen en de slaapkamers komen uit de verkooplijst van 29 oktober 2026, met twee woningen. De bebouwde oppervlakten, de terrassen en de ruimten komen uit de plattegronden van de ontwikkelaar, die overeenkomen met de prijslijst van 1 juli 2026; de verkooplijst geeft voor beide woningen kleinere bebouwde oppervlakten. Die prijslijst zegt dat haar prijzen netto zijn en de btw niet bevatten, en markeert Nr. 04 als gereserveerd.',
  'Dostępność, ceny i liczba sypialni pochodzą z listy sprzedażowej z 29 października 2026 r., która zawiera dwa lokale. Powierzchnie zabudowy, tarasy i pomieszczenia pochodzą z rzutów dewelopera, które zgadzają się z cennikiem z 1 lipca 2026 r.; lista sprzedażowa podaje dla obu lokali mniejsze powierzchnie zabudowy. Ten cennik zastrzega, że jego ceny są netto i nie zawierają VAT, i oznacza Nr. 04 jako zarezerwowaną.',
  'Tilgjengelighet, priser og soverom er hentet fra salgslisten fra 29. oktober 2026, som har to boliger. De bebygde arealene, terrassene og rommene er hentet fra utbyggerens plantegninger, som stemmer med prislisten fra 1. juli 2026; salgslisten oppgir mindre bebygde arealer for begge boligene. Den prislisten sier at prisene er netto og ikke inkluderer mva., og markerer Nr. 04 som reservert.',
  'Tillgänglighet, priser och sovrum är hämtade från försäljningslistan från den 29 oktober 2026, som har två bostäder. Byggytorna, terrasserna och rummen är hämtade från exploatörens planritningar, som stämmer med prislistan från den 1 juli 2026; försäljningslistan anger mindre byggytor för båda bostäderna. Den prislistan anger att priserna är nettopriser och inte inkluderar IVA, och markerar Nr. 04 som reserverad.')
a('.enquiry.headlineHtml', 'Pregunte por <em>Dunique Marbella</em>', 'Renseignez-vous sur <em>Dunique Marbella</em>', 'Fragen Sie nach <em>Dunique Marbella</em>',
  'Спросите о <em>Dunique Marbella</em>', 'استفسر عن <em>Dunique Marbella</em>', 'Vraag naar <em>Dunique Marbella</em>', 'Zapytaj o <em>Dunique Marbella</em>',
  'Spør om <em>Dunique Marbella</em>', 'Fråga om <em>Dunique Marbella</em>')
a('.enquiry.message',
  'Hola Nueva Living, me gustaría recibir información sobre Dunique Marbella.',
  'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Dunique Marbella.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Dunique Marbella.',
  'Здравствуйте, Nueva Living! Я хотел бы получить информацию о Dunique Marbella.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Dunique Marbella.',
  'Hallo Nueva Living, ik wil graag informatie over Dunique Marbella.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Dunique Marbella.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Dunique Marbella.',
  'Hej Nueva Living, jag skulle vilja få information om Dunique Marbella.')
a('.faq[0][1]',
  'Hay dos publicadas: la villa Nr. 04, de cuatro dormitorios, por {E5400000} y el apartamento Nr. 202, de tres dormitorios, por {E5200000}, ambos más IVA. El folleto de 2024 describe 32 villas y 64 apartamentos en total.',
  'Deux logements sont présentés : la villa Nr. 04, de quatre chambres, à {E5400000} et l’appartement Nr. 202, de trois chambres, à {E5200000}, tous deux hors TVA. La brochure de 2024 décrit 32 villas et 64 appartements au total.',
  'Zwei sind gelistet: die Villa Nr. 04 mit vier Schlafzimmern für {E5400000} und die Wohnung Nr. 202 mit drei Schlafzimmern für {E5200000}, beide zuzüglich MwSt. Die Broschüre von 2024 beschreibt insgesamt 32 Villen und 64 Wohnungen.',
  'В списке два объекта: вилла Nr. 04 с четырьмя спальнями за {E5400000} и квартира Nr. 202 с тремя спальнями за {E5200000}, оба без НДС. В брошюре 2024 года всего описаны 32 виллы и 64 квартиры.',
  'هناك مسكنان مدرجان: الفيلا Nr. 04 بأربع غرف نوم بسعر {E5400000} والشقة Nr. 202 بثلاث غرف نوم بسعر {E5200000}، كلاهما دون ضريبة القيمة المضافة. ويصف كتيّب 2024 ما مجموعه 32 فيلا و64 شقة.',
  'Twee zijn vermeld: villa Nr. 04 met vier slaapkamers voor {E5400000} en appartement Nr. 202 met drie slaapkamers voor {E5200000}, beide excl. btw. De brochure van 2024 beschrijft in totaal 32 villa’s en 64 appartementen.',
  'Na liście są dwa lokale: willa Nr. 04 z czterema sypialniami za {E5400000} i mieszkanie Nr. 202 z trzema sypialniami za {E5200000}, oba plus VAT. Broszura z 2024 r. opisuje łącznie 32 wille i 64 apartamenty.',
  'To er oppført: villa Nr. 04 med fire soverom til {E5400000} og leilighet Nr. 202 med tre soverom til {E5200000}, begge pluss mva. Brosjyren fra 2024 beskriver til sammen 32 villaer og 64 leiligheter.',
  'Två är listade: villa Nr. 04 med fyra sovrum för {E5400000} och lägenhet Nr. 202 med tre sovrum för {E5200000}, båda plus IVA. Broschyren från 2024 beskriver sammanlagt 32 villor och 64 lägenheter.')
a('.faq[1][0]', '¿Sigue disponible la Nr. 04?', 'La Nr. 04 est-elle toujours disponible ?', 'Ist Nr. 04 noch verfügbar?', 'Nr. 04 всё ещё доступна?', 'هل ما زالت Nr. 04 متاحة؟',
  'Is Nr. 04 nog beschikbaar?', 'Czy Nr. 04 jest nadal dostępna?', 'Er Nr. 04 fortsatt ledig?', 'Är Nr. 04 fortfarande ledig?')
a('.faq[1][1]',
  'La lista del 29 de octubre de 2026 la muestra como disponible, pero la lista de precios del 1 de julio de 2026 la marcaba como reservada. Confirmamos su estado antes de cualquier reserva.',
  'La liste du 29 octobre 2026 la présente comme disponible, mais la liste de prix du 1er juillet 2026 la marquait comme réservée. Nous confirmons son statut avant toute réservation.',
  'Die Liste vom 29. Oktober 2026 zeigt sie als verfügbar, doch die Preisliste vom 1. Juli 2026 kennzeichnete sie als reserviert. Wir bestätigen ihren Status vor jeder Reservierung.',
  'В списке от 29 октября 2026 года она значится доступной, но в прайс-листе от 1 июля 2026 года была отмечена как забронированная. Мы подтверждаем её статус перед любым бронированием.',
  'تُظهرها قائمة 29 أكتوبر 2026 كمتاحة، لكن قائمة الأسعار بتاريخ 1 يوليو 2026 كانت تضعها كمحجوزة. نؤكد حالتها قبل أي حجز.',
  'De lijst van 29 oktober 2026 toont haar als beschikbaar, maar de prijslijst van 1 juli 2026 markeerde haar als gereserveerd. Wij bevestigen haar status vóór elke reservering.',
  'Lista z 29 października 2026 r. pokazuje ją jako dostępną, ale cennik z 1 lipca 2026 r. oznaczał ją jako zarezerwowaną. Status potwierdzamy przed każdą rezerwacją.',
  'Listen fra 29. oktober 2026 viser den som ledig, men prislisten fra 1. juli 2026 markerte den som reservert. Vi bekrefter statusen før enhver reservasjon.',
  'Listan från den 29 oktober 2026 visar den som ledig, men prislistan från den 1 juli 2026 markerade den som reserverad. Vi bekräftar statusen före varje reservation.')
a('.faq[2][1]',
  'No. La lista de precios indica que sus precios son netos y no incluyen el IVA ni los impuestos de transmisión de la propiedad. Confirmamos por escrito los impuestos y los gastos de compra.',
  'Non. La liste de prix indique que ses prix sont nets et n’incluent ni la TVA (IVA) ni les droits de mutation. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Die Preisliste besagt, dass ihre Preise netto sind und weder die MwSt. (IVA) noch die Grunderwerbsteuern enthalten. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе сказано, что цены указаны нетто и не включают испанский НДС и налоги на переход права собственности. Налоги и расходы на покупку мы подтверждаем письменно.',
  'لا. تنصّ قائمة الأسعار على أن أسعارها صافية ولا تشمل ضريبة القيمة المضافة (IVA) ولا ضرائب نقل الملكية. ونؤكد الضرائب وتكاليف الشراء كتابةً.',
  'Nee. De prijslijst zegt dat haar prijzen netto zijn en geen Spaanse btw en geen overdrachtsbelasting bevatten. Wij bevestigen de belastingen en de aankoopkosten schriftelijk.',
  'Nie. Cennik zastrzega, że jego ceny są netto i nie zawierają hiszpańskiego VAT ani podatków od przeniesienia własności. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Prislisten sier at prisene er netto og ikke inkluderer spansk mva. eller dokumentavgift ved overdragelse. Vi bekrefter avgiftene og kjøpskostnadene skriftlig.',
  'Nej. Prislistan anger att priserna är nettopriser och inte inkluderar IVA (spansk moms) eller skatter vid överlåtelse av fastigheten. Vi bekräftar skatterna och köpkostnaderna skriftligen.')
a('.faq[3][1]',
  'Según sus planos, ambas viviendas tienen un garaje privado en el sótano para dos coches, y la lista de precios indica un trastero para ambas. La Nr. 202 tiene además una plaza abierta y un trastero exterior que su plano marca como extra, por lo que confirmamos qué incluye el precio.',
  'D’après leurs plans, les deux logements ont un garage privé en sous-sol pour deux voitures, et la liste de prix indique un cellier pour les deux. La Nr. 202 a en outre une place ouverte et un cellier extérieur que son plan marque comme supplément ; nous confirmons donc ce que le prix comprend.',
  'Nach ihren Plänen haben beide Immobilien eine private Garage im Untergeschoss für zwei Autos, und die Preisliste nennt für beide einen Abstellraum. Nr. 202 hat zusätzlich einen offenen Stellplatz und einen Außenabstellraum, die ihr Plan als Extra kennzeichnet; wir bestätigen daher, was der Preis umfasst.',
  'По планам у обоих объектов есть частный гараж в подвальном этаже на две машины, а в прайс-листе для обоих указана кладовая. У Nr. 202 есть также открытое парковочное место и наружная кладовая, которые на плане помечены как дополнительные, поэтому мы уточняем, что входит в цену.',
  'وفق مخططاتهما، لكلا المسكنين مرآب خاص في الطابق السفلي لسيارتين، وتذكر قائمة الأسعار غرفة تخزين لكليهما. وللمسكن Nr. 202 أيضًا موقف مكشوف وغرفة تخزين خارجية يضعهما مخططه كإضافيين، لذلك نؤكد ما يشمله السعر.',
  'Volgens hun plattegronden hebben beide woningen een privégarage in de kelder voor twee auto’s, en de prijslijst noemt voor beide een berging. Nr. 202 heeft daarnaast een open parkeerplaats en een buitenberging die haar plattegrond als extra markeert, dus wij bevestigen wat de prijs omvat.',
  'Według rzutów oba lokale mają prywatny garaż w piwnicy na dwa samochody, a cennik podaje dla obu komórkę lokatorską. Nr. 202 ma ponadto otwarte miejsce parkingowe i zewnętrzną komórkę, które jej rzut oznacza jako dodatkowe, dlatego potwierdzamy, co obejmuje cena.',
  'Ifølge plantegningene har begge boligene en privat garasje i kjelleren for to biler, og prislisten oppgir en bod for begge. Nr. 202 har i tillegg en åpen parkeringsplass og en utvendig bod som plantegningen markerer som tillegg, så vi bekrefter hva prisen omfatter.',
  'Enligt planritningarna har båda bostäderna ett privat garage i källaren för två bilar, och prislistan anger ett förråd för båda. Nr. 202 har dessutom en öppen parkeringsplats och ett utvändigt förråd som dess planritning markerar som extra, så vi bekräftar vad priset omfattar.')
a('.faq[4][1]',
  'No. El mobiliario y la decoración que aparecen en las imágenes no están incluidos. Las cocinas se entregan con los electrodomésticos que indica la memoria de calidades.',
  'Non. Le mobilier et la décoration représentés sur les images ne sont pas inclus. Les cuisines sont livrées avec l’électroménager indiqué dans le descriptif.',
  'Nein. Die auf den Bildern gezeigten Möbel und die Dekoration sind nicht enthalten. Die Küchen werden mit den in der Baubeschreibung genannten Geräten übergeben.',
  'Нет. Мебель и декор, показанные на изображениях, не входят в комплектацию. Кухни передаются с техникой, указанной в спецификации.',
  'لا. الأثاث والديكور الظاهران في الصور غير مشمولين. وتُسلَّم المطابخ مع الأجهزة المذكورة في المواصفات.',
  'Nee. Het meubilair en de inrichting op de beelden zijn niet inbegrepen. De keukens worden opgeleverd met de apparatuur uit de kwaliteitsomschrijving.',
  'Nie. Meble i wystrój pokazane na obrazach nie wchodzą w cenę. Kuchnie są przekazywane ze sprzętem wymienionym w opisie standardu.',
  'Nei. Møblene og innredningen som vises på bildene er ikke inkludert. Kjøkkenene leveres med hvitevarene som er oppgitt i kvalitetsbeskrivelsen.',
  'Nej. Möblerna och inredningen som visas på bilderna ingår inte. Köken levereras med de vitvaror som anges i kvalitetsbeskrivningen.')

# ---- SEO -----------------------------------------------------------------------------------------------

a('.seo.title', 'Dunique Marbella - Villa y apartamento frente al mar', 'Dunique Marbella - Villa et appartement en bord de mer',
  'Dunique Marbella - Villa und Wohnung am Strand', 'Dunique Marbella - вилла и квартира у пляжа', 'Dunique Marbella - فيلا وشقة على الواجهة البحرية',
  'Dunique Marbella - Villa en appartement aan het strand', 'Dunique Marbella - Willa i mieszkanie przy plaży', 'Dunique Marbella - Villa og leilighet ved stranden',
  'Dunique Marbella - Villa och lägenhet vid stranden')
a('.seo.h1', 'Dunique Marbella: villa y apartamento con piscinas privadas en Marbella', 'Dunique Marbella : villa et appartement avec piscines privées à Marbella',
  'Dunique Marbella: Villa und Wohnung mit privaten Pools in Marbella', 'Dunique Marbella: вилла и квартира с собственными бассейнами в Марбелье',
  'Dunique Marbella: فيلا وشقة بمسبحين خاصين في ماربيا', 'Dunique Marbella: villa en appartement met privézwembaden in Marbella',
  'Dunique Marbella: willa i mieszkanie z prywatnymi basenami w Marbelli', 'Dunique Marbella: villa og leilighet med private bassenger i Marbella',
  'Dunique Marbella: villa och lägenhet med egna pooler i Marbella')
a('.seo.h1Context', 'Villa y apartamento con piscinas privadas en Marbella', 'Villa et appartement avec piscines privées à Marbella',
  'Villa und Wohnung mit privaten Pools in Marbella', 'Вилла и квартира с собственными бассейнами в Марбелье', 'فيلا وشقة بمسبحين خاصين في ماربيا',
  'Villa en appartement met privézwembaden in Marbella', 'Willa i mieszkanie z prywatnymi basenami w Marbelli', 'Villa og leilighet med private bassenger i Marbella',
  'Villa och lägenhet med egna pooler i Marbella')

# ---- templates: unit references, sizes, plan alt and captions -------------------------------------------

for u in proj['availability']['units']:
    if u['reference'] not in T:
        same(u['reference'])
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
    put(u['size'], out)

# plan alt and caption: "<type> <code>, <levels>"
KIND = {'Villa': {'es': 'Villa', 'fr': 'Villa', 'de': 'Villa', 'ru': 'Вилла', 'ar': 'الفيلا', 'nl': 'Villa', 'pl': 'Willa', 'no': 'Villa', 'sv': 'Villa'},
        'Apartment': {'es': 'Apartamento', 'fr': 'Appartement', 'de': 'Wohnung', 'ru': 'Квартира', 'ar': 'الشقة', 'nl': 'Appartement', 'pl': 'Mieszkanie', 'no': 'Leilighet', 'sv': 'Lägenhet'}}
LEVELS = {
 'basement and ground floor': {'es': 'sótano y planta baja', 'fr': 'sous-sol et rez-de-chaussée', 'de': 'Untergeschoss und Erdgeschoss', 'ru': 'подвальный и первый этаж',
                               'ar': 'الطابق السفلي والطابق الأرضي', 'nl': 'kelder en begane grond', 'pl': 'piwnica i parter', 'no': 'kjeller og første etasje', 'sv': 'källare och bottenvåning'},
 'first floor and solarium': {'es': 'primera planta y solárium', 'fr': 'premier étage et solarium', 'de': 'erstes Obergeschoss und Solarium', 'ru': 'второй этаж и солярий',
                              'ar': 'الطابق الأول والسولاريوم', 'nl': 'eerste verdieping en solarium', 'pl': 'pierwsze piętro i solarium', 'no': 'andre etasje og solterrasse', 'sv': 'första våningen och solterrass'},
}
PLAN = {'es': 'Plano de', 'fr': 'Plan de', 'de': 'Grundriss von', 'ru': 'Планировка:', 'ar': 'مخطط', 'nl': 'Plattegrond van', 'pl': 'Rzut:', 'no': 'Plantegning av', 'sv': 'Planritning för'}
for it in proj['media']['items']:
    if it.get('category') != 'Floorplans':
        continue
    m = re.fullmatch(r'(Villa|Apartment) (DU-\d+), (.+)', it['caption'])
    assert m, it['caption']
    kind, code, lv = m.groups()
    cap_, alt_ = {}, {}
    for l in LOCS:
        sep = '، ' if l == 'ar' else ', '
        k = KIND[kind][l]
        cap_[l] = f'{k} {code}{sep}{LEVELS[lv][l]}'
        alt_[l] = f'{PLAN[l]} {k[0].lower() + k[1:] if l in ("es", "fr", "nl", "no", "sv", "pl") else k} {code}{sep}{LEVELS[lv][l]}'
    T[it['caption']] = cap_
    T[it['alt']] = alt_

json.dump(T, open(f'{SP}/tr_m.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
