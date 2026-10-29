# -*- coding: utf-8 -*-
"""Arosa: the strings the translation memory did not have.

Same shape as k_las_mesas_blue_horizon.py. Each entry is looked up by its path in the project's English
(so the English is not retyped here) and stored under the English string itself, so the output is keyed
by English like every other tr_*.json. The first words of the English are checked on every entry, so a
change to the copy that moves a string stops the run instead of putting a translation on the wrong
sentence. Tokens: {E705000} money, {N30.33} decimal number, {U} the area unit. Unit sizes, floor labels
and plan captions are built from per-locale templates at the foot of the file.
    python3 tools/import/k_arosa.py <scratch dir>      (writes <dir>/tr_n.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/arosa/project.json'))


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


def at(path):
    """The English string at a path such as .overview.copy[0] or .faq[3][0]."""
    node = proj
    for key, idx in re.findall(r'\.([A-Za-z0-9]+)|\[(\d+)\]', path):
        node = node[key] if key else node[int(idx)]
    assert isinstance(node, str), path
    return node


def p(path, prefix, *tr):
    en = at(path)
    assert en.startswith(prefix), (path, en[:40], prefix)
    assert len(tr) == 9, (path, len(tr))
    assert en not in T, ('duplicate', path)
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    T[en] = {l: en for l in LOCS}


# identifiers: the project name reads the same everywhere
same('Arosa')

# ---- description, SEO, hero, card -------------------------------------------------------------
p('.description', '13 of 54 apartments',
  '13 de 54 apartamentos de uno, dos y tres dormitorios en Arosa, en La Cala de Mijas, con vistas al mar, piscinas exterior e interior, gimnasio y sauna. En construcción, con el fin de obra estimado para el cuarto trimestre de 2028. Desde {E705000} más IVA.',
  '13 des 54 appartements de une, deux et trois chambres à Arosa, à La Cala de Mijas, avec vue sur la mer, piscines extérieure et intérieure, salle de sport et sauna. En construction, avec une fin des travaux estimée au quatrième trimestre 2028. À partir de {E705000} hors TVA.',
  '13 von 54 Wohnungen mit einem, zwei und drei Schlafzimmern in Arosa, in La Cala de Mijas, mit Meerblick, Außen- und Innenpool, Fitnessraum und Sauna. Im Bau, das Bauende ist für das vierte Quartal 2028 geschätzt. Ab {E705000} zuzüglich MwSt.',
  '13 из 54 квартир с одной, двумя и тремя спальнями в Arosa, в Ла-Кала-де-Михас: вид на море, наружный и крытый бассейны, тренажёрный зал и сауна. Строится, окончание строительства ожидается в четвёртом квартале 2028 года. От {E705000} без НДС.',
  '13 من أصل 54 شقة بغرفة نوم وغرفتي نوم وثلاث غرف نوم في Arosa، في لا كالا دي ميخاس، بإطلالة على البحر ومسبحين خارجي وداخلي وصالة رياضية وساونا. قيد الإنشاء، ويُقدَّر انتهاء الإنشاء في الربع الرابع من عام 2028. ابتداءً من {E705000} دون ضريبة القيمة المضافة.',
  '13 van de 54 appartementen met een, twee en drie slaapkamers in Arosa, in La Cala de Mijas, met zeezicht, een buiten- en een binnenzwembad, een fitnessruimte en een sauna. In aanbouw, met het einde van de bouw geschat op het vierde kwartaal van 2028. Vanaf {E705000} excl. btw.',
  '13 z 54 mieszkań z jedną, dwiema i trzema sypialniami w Arosa, w La Cala de Mijas, z widokiem na morze, basenami zewnętrznym i wewnętrznym, siłownią i sauną. W budowie, zakończenie budowy szacowane na czwarty kwartał 2028 roku. Od {E705000} plus VAT.',
  '13 av 54 leiligheter med ett, to og tre soverom i Arosa, i La Cala de Mijas, med utsikt over havet, utendørs og innendørs basseng, treningsrom og badstue. Under bygging, med byggeslutt anslått til fjerde kvartal 2028. Fra {E705000} pluss mva.',
  '13 av 54 lägenheter med ett, två och tre sovrum i Arosa, i La Cala de Mijas, med havsutsikt, pooler utomhus och inomhus, gym och bastu. Under uppförande, med byggslut beräknat till fjärde kvartalet 2028. Från {E705000} plus IVA.')

p('.seoDescription', '13 of 54 one-',
  '13 de 54 apartamentos de uno, dos y tres dormitorios en Arosa, La Cala de Mijas, con vistas al mar, piscinas y gimnasio, fin de obra estimado para el T4 2028, desde {E705000} más IVA.',
  '13 des 54 appartements de une, deux et trois chambres à Arosa, La Cala de Mijas, avec vue sur la mer, piscines et salle de sport, fin des travaux estimée au T4 2028, à partir de {E705000} hors TVA.',
  '13 von 54 Wohnungen mit einem, zwei und drei Schlafzimmern in Arosa, La Cala de Mijas, mit Meerblick, Pools und Fitnessraum, Bauende für Q4 2028 geschätzt, ab {E705000} zuzüglich MwSt.',
  '13 из 54 квартир с одной, двумя и тремя спальнями в Arosa, Ла-Кала-де-Михас: вид на море, бассейны и тренажёрный зал, окончание строительства ожидается в 4 кв. 2028 года, от {E705000} без НДС.',
  '13 من أصل 54 شقة بغرفة نوم وغرفتي نوم وثلاث غرف نوم في Arosa، لا كالا دي ميخاس، بإطلالة على البحر ومسابح وصالة رياضية، ويُقدَّر انتهاء الإنشاء في الربع الرابع 2028، ابتداءً من {E705000} دون ضريبة القيمة المضافة.',
  '13 van de 54 appartementen met een, twee en drie slaapkamers in Arosa, La Cala de Mijas, met zeezicht, zwembaden en een fitnessruimte, einde van de bouw geschat op K4 2028, vanaf {E705000} excl. btw.',
  '13 z 54 mieszkań z jedną, dwiema i trzema sypialniami w Arosa, La Cala de Mijas, z widokiem na morze, basenami i siłownią, zakończenie budowy szacowane na IV kw. 2028, od {E705000} plus VAT.',
  '13 av 54 leiligheter med ett, to og tre soverom i Arosa, La Cala de Mijas, med utsikt over havet, basseng og treningsrom, byggeslutt anslått til K4 2028, fra {E705000} pluss mva.',
  '13 av 54 lägenheter med ett, två och tre sovrum i Arosa, La Cala de Mijas, med havsutsikt, pooler och gym, byggslut beräknat till K4 2028, från {E705000} plus IVA.')

p('.twitterDescription', 'One-, two- and three-bedroom',
  'Apartamentos de uno, dos y tres dormitorios en La Cala de Mijas con vistas al mar, piscinas y gimnasio, desde {E705000} más IVA.',
  'Appartements de une, deux et trois chambres à La Cala de Mijas, avec vue sur la mer, piscines et salle de sport, à partir de {E705000} hors TVA.',
  'Wohnungen mit einem, zwei und drei Schlafzimmern in La Cala de Mijas mit Meerblick, Pools und Fitnessraum, ab {E705000} zuzüglich MwSt.',
  'Квартиры с одной, двумя и тремя спальнями в Ла-Кала-де-Михас: вид на море, бассейны и тренажёрный зал, от {E705000} без НДС.',
  'شقق بغرفة نوم وغرفتي نوم وثلاث غرف نوم في لا كالا دي ميخاس بإطلالة على البحر ومسابح وصالة رياضية، ابتداءً من {E705000} دون ضريبة القيمة المضافة.',
  'Appartementen met een, twee en drie slaapkamers in La Cala de Mijas met zeezicht, zwembaden en een fitnessruimte, vanaf {E705000} excl. btw.',
  'Mieszkania z jedną, dwiema i trzema sypialniami w La Cala de Mijas z widokiem na morze, basenami i siłownią, od {E705000} plus VAT.',
  'Leiligheter med ett, to og tre soverom i La Cala de Mijas med utsikt over havet, basseng og treningsrom, fra {E705000} pluss mva.',
  'Lägenheter med ett, två och tre sovrum i La Cala de Mijas med havsutsikt, pooler och gym, från {E705000} plus IVA.')

p('.hero.startingPrice', 'From EUR',
  'Desde {E705000} + IVA', 'À partir de {E705000} + TVA', 'Ab {E705000} + MwSt.', 'От {E705000} + НДС',
  'ابتداءً من {E705000} + ضريبة القيمة المضافة', 'Vanaf {E705000} + btw', 'Od {E705000} + VAT', 'Fra {E705000} + mva.', 'Från {E705000} + IVA')
p('.card.meta[0][1]', 'EUR 705,000 + VAT',
  '{E705000} + IVA', '{E705000} + TVA', '{E705000} + MwSt.', '{E705000} + НДС',
  '{E705000} + ضريبة القيمة المضافة', '{E705000} + btw', '{E705000} + VAT', '{E705000} + mva.', '{E705000} + IVA')
p('.overview.metrics[3][1]', 'EUR 705,000 - EUR',
  '{E705000} - {E1570000} + IVA', '{E705000} - {E1570000} + TVA', '{E705000} - {E1570000} + MwSt.', '{E705000} - {E1570000} + НДС',
  '{E705000} - {E1570000} + ضريبة القيمة المضافة', '{E705000} - {E1570000} + btw', '{E705000} - {E1570000} + VAT', '{E705000} - {E1570000} + mva.', '{E705000} - {E1570000} + IVA')
# availability.priceRange has the same English as overview.metrics[3][1]; availability.startingPrice the same as card.meta[0][1]

p('.card.description', '13 of 54 one-',
  '13 de 54 apartamentos de uno, dos y tres dormitorios en La Cala de Mijas, con vistas al mar, piscinas exterior e interior y gimnasio.',
  '13 des 54 appartements de une, deux et trois chambres à La Cala de Mijas, avec vue sur la mer, piscines extérieure et intérieure et salle de sport.',
  '13 von 54 Wohnungen mit einem, zwei und drei Schlafzimmern in La Cala de Mijas, mit Meerblick, Außen- und Innenpool und Fitnessraum.',
  '13 из 54 квартир с одной, двумя и тремя спальнями в Ла-Кала-де-Михас: вид на море, наружный и крытый бассейны и тренажёрный зал.',
  '13 من أصل 54 شقة بغرفة نوم وغرفتي نوم وثلاث غرف نوم في لا كالا دي ميخاس، بإطلالة على البحر ومسبحين خارجي وداخلي وصالة رياضية.',
  '13 van de 54 appartementen met een, twee en drie slaapkamers in La Cala de Mijas, met zeezicht, een buiten- en een binnenzwembad en een fitnessruimte.',
  '13 z 54 mieszkań z jedną, dwiema i trzema sypialniami w La Cala de Mijas, z widokiem na morze, basenem zewnętrznym i wewnętrznym oraz siłownią.',
  '13 av 54 leiligheter med ett, to og tre soverom i La Cala de Mijas, med utsikt over havet, utendørs og innendørs basseng og treningsrom.',
  '13 av 54 lägenheter med ett, två och tre sovrum i La Cala de Mijas, med havsutsikt, pooler utomhus och inomhus och gym.')

# ---- images: section images and the gallery ------------------------------------------------------
p('.images.hero.alt', 'Aerial view of the white terraced block',
  'Vista aérea del bloque blanco en terrazas, con sus piscinas y jardines junto a una carretera curva, la costa y el mar al fondo, con el bloque generado por ordenador colocado sobre una fotografía',
  'Vue aérienne du bâtiment blanc en terrasses, avec ses piscines et ses jardins le long d’une route en courbe, la côte et la mer au loin, le bâtiment généré par ordinateur étant placé dans une photographie',
  'Luftaufnahme des weißen Terrassengebäudes mit seinen Pools und Gärten neben einer geschwungenen Straße, dahinter die Küste und das Meer, mit dem computergenerierten Gebäude in ein Foto eingefügt',
  'Вид с воздуха на белый террасный корпус с бассейнами и садами рядом с изогнутой дорогой, за ним побережье и море; компьютерная модель корпуса помещена на фотографию',
  'منظر جوي للمبنى الأبيض المدرّج بتراساته ومسابحه وحدائقه إلى جانب طريق منحنٍ، وخلفه الساحل والبحر، مع وضع المبنى المُنشأ بالحاسوب في صورة فوتوغرافية',
  'Luchtfoto van het witte terrasgebouw met zijn zwembaden en tuinen naast een bochtige weg, met daarachter de kust en de zee, waarbij het computergegenereerde gebouw in een foto is geplaatst',
  'Widok z lotu ptaka na biały taraśny budynek z basenami i ogrodami obok zakręcającej drogi, a za nim wybrzeże i morze; wygenerowany komputerowo budynek umieszczono na fotografii',
  'Flyfoto av den hvite terrassebygningen med bassenger og hager ved siden av en svingete vei, med kysten og havet bak, med den datagenererte bygningen plassert inn i et fotografi',
  'Flygbild av det vita terrasshuset med pooler och trädgårdar intill en böjd väg, med kusten och havet bakom, där det datorgenererade huset har placerats in i ett fotografi')
p('.images.architecture.alt', 'Computer-generated view at dusk',
  'Vista generada por ordenador, al atardecer, del bloque blanco escalonado sobre una piscina turquesa con terraza de madera, tumbonas y vegetación tropical',
  'Vue générée par ordinateur, au crépuscule, du bâtiment blanc en gradins au-dessus d’une piscine turquoise avec une terrasse en bois, des transats et une végétation tropicale',
  'Computergenerierte Ansicht des weißen, gestaffelten Gebäudes in der Dämmerung über einem türkisfarbenen Pool mit Holzdeck, Sonnenliegen und tropischer Bepflanzung',
  'Компьютерная визуализация белого ступенчатого корпуса в сумерках над бирюзовым бассейном с деревянным настилом, шезлонгами и тропическими растениями',
  'منظر مُنشأ بالحاسوب عند الغسق للمبنى الأبيض المتدرّج فوق مسبح بلون فيروزي مع سطح خشبي ومقاعد استلقاء ونباتات استوائية',
  'Computergegenereerd beeld in de schemering van het witte, getrapte gebouw boven een turquoise zwembad met een houten dek, ligbedden en tropische beplanting',
  'Wizualizacja komputerowa o zmierzchu: biały, schodkowy budynek nad turkusowym basenem z drewnianym pokładem, leżakami i tropikalną roślinnością',
  'Datagenerert bilde i skumringen av den hvite, trappetrinnsformede bygningen over et turkist basseng med tredekk, solsenger og tropisk beplantning',
  'Datorgenererad bild i skymningen av det vita, trappstegsformade huset ovanför en turkos pool med trädäck, solstolar och tropisk grönska')
p('.images.lifestyle.alt', 'Computer-generated terrace under a pergola',
  'Terraza generada por ordenador bajo una pérgola, con mesa de comedor y sillones, con vistas al mar por encima de una barandilla de vidrio',
  'Terrasse générée par ordinateur sous une pergola, avec une table à manger et des fauteuils, donnant sur la mer par-dessus un garde-corps en verre',
  'Computergenerierte Terrasse unter einer Pergola mit Esstisch und Loungesesseln, mit Blick über eine Glasbrüstung auf das Meer',
  'Компьютерная визуализация террасы под перголой с обеденным столом и креслами; через стеклянное ограждение открывается вид на море',
  'تراس مُنشأ بالحاسوب تحت بيرغولا مع طاولة طعام ومقاعد استرخاء، يطلّ على البحر من فوق درابزين زجاجي',
  'Computergegenereerd terras onder een pergola met een eettafel en loungestoelen, met uitzicht over een glazen balustrade op de zee',
  'Wizualizacja komputerowa tarasu pod pergolą ze stołem jadalnianym i fotelami, z widokiem na morze ponad szklaną balustradą',
  'Datagenerert terrasse under en pergola med spisebord og loungestoler, med utsikt over et glassrekkverk mot havet',
  'Datorgenererad terrass under en pergola med matbord och loungefåtöljer, med utsikt över ett glasräcke mot havet')
p('.images.privateViewing.alt', 'Computer-generated bedroom with a double bed, a timber-slat',
  'Dormitorio generado por ordenador con cama doble, cabecero de listones de madera, mural de hojas de palmera y puerta corredera de vidrio a la terraza',
  'Chambre générée par ordinateur avec un lit double, une tête de lit à lattes de bois, une fresque de feuilles de palmier et une porte coulissante en verre donnant sur la terrasse',
  'Computergeneriertes Schlafzimmer mit Doppelbett, Kopfteil aus Holzlamellen, Palmblatt-Wandbild und Glasschiebetür zur Terrasse',
  'Компьютерная визуализация спальни с двуспальной кроватью, изголовьем из деревянных реек, фреской с пальмовыми листьями и раздвижной стеклянной дверью на террасу',
  'غرفة نوم مُنشأة بالحاسوب بسرير مزدوج ومسند رأس من شرائح خشبية وجدارية بأوراق النخيل وباب زجاجي منزلق إلى التراس',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een hoofdbord van houten latten, een muurschildering van palmbladeren en een glazen schuifdeur naar het terras',
  'Wizualizacja komputerowa sypialni z łóżkiem dwuosobowym, zagłówkiem z drewnianych listew, muralem z liści palmy i przesuwnymi szklanymi drzwiami na taras',
  'Datagenerert soverom med dobbeltseng, hodegavl av trelister, veggmaleri med palmeblader og glasskyvedør til terrassen',
  'Datorgenererat sovrum med dubbelsäng, sänggavel av träribbor, väggmålning med palmblad och glasskjutdörr till terrassen')

p('.media.copy', 'Computer-generated views of the block',
  'Vistas generadas por ordenador del bloque, las piscinas y los interiores, el plano general y los planos de las trece viviendas listadas.',
  'Vues générées par ordinateur du bâtiment, des piscines et des intérieurs, le plan de masse et les plans des treize logements listés.',
  'Computergenerierte Ansichten des Gebäudes, der Pools und der Innenräume, der Lageplan und die Grundrisse der dreizehn aufgeführten Wohnungen.',
  'Компьютерные визуализации корпуса, бассейнов и интерьеров, генеральный план и планировки тринадцати квартир из списка.',
  'مناظر مُنشأة بالحاسوب للمبنى والمسابح والتصاميم الداخلية، والمخطط العام، ومخططات المساكن الثلاثة عشر المدرجة.',
  'Computergegenereerde beelden van het gebouw, de zwembaden en de interieurs, het situatieplan en de plattegronden van de dertien vermelde woningen.',
  'Wizualizacje komputerowe budynku, basenów i wnętrz, plan zagospodarowania oraz rzuty trzynastu wymienionych lokali.',
  'Datagenererte bilder av bygningen, bassengene og interiørene, situasjonsplanen og plantegningene av de tretten oppførte boligene.',
  'Datorgenererade bilder av huset, poolerna och interiörerna, situationsplanen och planritningarna för de tretton listade bostäderna.')
p('.media.note', 'The images are computer-generated',
  'Las imágenes están generadas por ordenador, salvo las vistas aéreas, que sitúan el bloque generado por ordenador en fotografías de la zona, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los planos de venta del promotor: no tienen carácter contractual, los nombres de las estancias están en español y indican que las superficies son aproximadas.',
  'Les images sont des images de synthèse, à l’exception des vues aériennes, qui placent le bâtiment de synthèse dans des photographies de la zone, et le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont les plans de vente du promoteur : ils n’ont pas valeur contractuelle, le nom des pièces y est en espagnol et ils précisent que les surfaces sont approximatives.',
  'Die Bilder sind computergeneriert, mit Ausnahme der Luftaufnahmen, die das computergenerierte Gebäude in Fotos der Umgebung setzen; die darin gezeigten Möbel und die Dekoration dienen der Veranschaulichung und sind nicht enthalten. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen sind auf Spanisch, und sie weisen darauf hin, dass die Flächen ungefähre Angaben sind.',
  'Все изображения созданы на компьютере, за исключением видов с воздуха, на которых компьютерная модель корпуса помещена в фотографии местности; мебель и декор на них приведены для иллюстрации и в стоимость не входят. Планировки — это продажные планы застройщика: они не имеют договорной силы, названия помещений на них даны по-испански, а площади, как указано на планах, приблизительные.',
  'جميع الصور مُنشأة بالحاسوب، باستثناء المناظر الجوية التي تضع المبنى المُنشأ بالحاسوب داخل صور فوتوغرافية للمنطقة، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. المخططات هي مخططات البيع الخاصة بالمطوّر: وهي غير ملزمة تعاقديًا، وأسماء الغرف عليها بالإسبانية، وتنص على أن المساحات تقريبية.',
  'De beelden zijn computergegenereerd, met uitzondering van de luchtbeelden, die het computergegenereerde gebouw in foto’s van de omgeving plaatsen; de meubels en de inrichting erop zijn illustratief en niet inbegrepen. De plattegronden zijn de verkoopplattegronden van de ontwikkelaar: ze zijn niet contractueel, de ruimtenamen erop zijn in het Spaans en ze vermelden dat de oppervlakten bij benadering zijn.',
  'Obrazy są wygenerowane komputerowo, z wyjątkiem widoków z lotu ptaka, które umieszczają komputerowy model budynku na fotografiach okolicy; widoczne na nich meble i wystrój mają charakter poglądowy i nie są wliczone w cenę. Rzuty to plany sprzedażowe dewelopera: nie mają charakteru umownego, nazwy pomieszczeń są po hiszpańsku, a według rzutów podane powierzchnie są przybliżone.',
  'Bildene er datagenererte, bortsett fra flyfotoene, som plasserer den datagenererte bygningen i fotografier av området, og møblene og innredningen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens salgstegninger: de er ikke kontraktsfestet, romnavnene på dem er på spansk, og de oppgir at arealene er omtrentlige.',
  'Bilderna är datorgenererade, förutom flygbilderna, som placerar den datorgenererade byggnaden i fotografier av området, och möblerna och inredningen i dem är illustrativa och ingår inte. Planritningarna är exploatörens säljplaner: de är inte avtalsgrundande, rummens namn på dem är på spanska och de anger att ytorna är ungefärliga.')

p('.media.items[0].caption', 'The block, the pools',
  'El bloque, las piscinas y la costa, vistos desde arriba', 'Le bâtiment, les piscines et la côte vus du ciel', 'Das Gebäude, die Pools und die Küste von oben',
  'Корпус, бассейны и побережье с высоты', 'المبنى والمسابح والساحل من الأعلى', 'Het gebouw, de zwembaden en de kust van bovenaf',
  'Budynek, baseny i wybrzeże z lotu ptaka', 'Bygningen, bassengene og kysten sett ovenfra', 'Huset, poolerna och kusten sedda uppifrån')
p('.media.items[1].alt', 'Aerial view of the long terraced block',
  'Vista aérea del largo bloque en terrazas desde el frente, con tumbonas junto a las piscinas y los jardines, con el bloque generado por ordenador colocado sobre una fotografía',
  'Vue aérienne du long bâtiment en terrasses vu de face, avec des transats près des piscines et des jardins, le bâtiment généré par ordinateur étant placé dans une photographie',
  'Luftaufnahme des langen Terrassengebäudes von vorn, mit Sonnenliegen neben den Pools und Gärten, mit dem computergenerierten Gebäude in ein Foto eingefügt',
  'Вид с воздуха на длинный террасный корпус спереди, с шезлонгами у бассейнов и садов; компьютерная модель корпуса помещена на фотографию',
  'منظر جوي للمبنى الطويل المدرّج من الأمام، مع مقاعد استلقاء بجانب المسابح والحدائق، مع وضع المبنى المُنشأ بالحاسوب في صورة فوتوغرافية',
  'Luchtfoto van het lange terrasgebouw van voren, met ligbedden naast de zwembaden en de tuinen, waarbij het computergegenereerde gebouw in een foto is geplaatst',
  'Widok z lotu ptaka na długi taraśny budynek od frontu, z leżakami obok basenów i ogrodów; wygenerowany komputerowo budynek umieszczono na fotografii',
  'Flyfoto av den lange terrassebygningen forfra, med solsenger ved siden av bassengene og hagene, med den datagenererte bygningen plassert inn i et fotografi',
  'Flygbild av det långa terrasshuset framifrån, med solstolar intill poolerna och trädgårdarna, där det datorgenererade huset har placerats in i ett fotografi')
p('.media.items[1].caption', 'The block and the pools',
  'El bloque y las piscinas, vistos desde el frente', 'Le bâtiment et les piscines, vus de face', 'Das Gebäude und die Pools von vorn',
  'Корпус и бассейны, вид спереди', 'المبنى والمسابح من الأمام', 'Het gebouw en de zwembaden van voren',
  'Budynek i baseny od frontu', 'Bygningen og bassengene forfra', 'Huset och poolerna framifrån')
p('.media.items[2].caption', 'The block above the pool',
  'El bloque sobre la piscina al atardecer', 'Le bâtiment au-dessus de la piscine au crépuscule', 'Das Gebäude über dem Pool in der Dämmerung',
  'Корпус над бассейном в сумерках', 'المبنى فوق المسبح عند الغسق', 'Het gebouw boven het zwembad in de schemering',
  'Budynek nad basenem o zmierzchu', 'Bygningen over bassenget i skumringen', 'Huset ovanför poolen i skymningen')
p('.media.items[3].alt', 'Aerial view of the corner of the block',
  'Vista aérea de la esquina del bloque con sus terrazas de cubierta y una piscina, con el mar detrás, con el bloque generado por ordenador colocado sobre una fotografía',
  'Vue aérienne de l’angle du bâtiment avec ses toits-terrasses et une piscine, la mer derrière, le bâtiment généré par ordinateur étant placé dans une photographie',
  'Luftaufnahme der Ecke des Gebäudes mit seinen Dachterrassen und einem Pool, dahinter das Meer, mit dem computergenerierten Gebäude in ein Foto eingefügt',
  'Вид с воздуха на угол корпуса с террасами на крыше и бассейном, позади море; компьютерная модель корпуса помещена на фотографию',
  'منظر جوي لزاوية المبنى مع تراسات السطح ومسبح، والبحر خلفه، مع وضع المبنى المُنشأ بالحاسوب في صورة فوتوغرافية',
  'Luchtfoto van de hoek van het gebouw met zijn dakterrassen en een zwembad, met de zee erachter, waarbij het computergegenereerde gebouw in een foto is geplaatst',
  'Widok z lotu ptaka na narożnik budynku z tarasami na dachu i basenem, z morzem w tle; wygenerowany komputerowo budynek umieszczono na fotografii',
  'Flyfoto av hjørnet av bygningen med takterrassene og et basseng, med havet bak, med den datagenererte bygningen plassert inn i et fotografi',
  'Flygbild av husets hörn med takterrasserna och en pool, med havet bakom, där det datorgenererade huset har placerats in i ett fotografi')
p('.media.items[3].caption', 'The corner of the block',
  'La esquina del bloque, con el mar detrás', 'L’angle du bâtiment, avec la mer derrière', 'Die Ecke des Gebäudes mit dem Meer dahinter',
  'Угол корпуса, позади море', 'زاوية المبنى والبحر خلفها', 'De hoek van het gebouw, met de zee erachter',
  'Narożnik budynku z morzem w tle', 'Hjørnet av bygningen, med havet bak', 'Husets hörn, med havet bakom')
p('.media.items[4].alt', 'Aerial view at sunset',
  'Vista aérea al atardecer del bloque con sus jardines iluminados y su piscina sobre la carretera de la costa, con el bloque generado por ordenador colocado sobre una fotografía',
  'Vue aérienne au coucher du soleil du bâtiment avec ses jardins éclairés et sa piscine au-dessus de la route côtière, le bâtiment généré par ordinateur étant placé dans une photographie',
  'Luftaufnahme des Gebäudes bei Sonnenuntergang mit beleuchteten Gärten und Pool oberhalb der Küstenstraße, mit dem computergenerierten Gebäude in ein Foto eingefügt',
  'Вид с воздуха на корпус на закате с освещёнными садами и бассейном над прибрежной дорогой; компьютерная модель корпуса помещена на фотографию',
  'منظر جوي عند الغروب للمبنى مع حدائقه المضاءة ومسبحه فوق الطريق الساحلي، مع وضع المبنى المُنشأ بالحاسوب في صورة فوتوغرافية',
  'Luchtfoto bij zonsondergang van het gebouw met verlichte tuinen en een zwembad boven de kustweg, waarbij het computergegenereerde gebouw in een foto is geplaatst',
  'Widok z lotu ptaka o zachodzie słońca na budynek z oświetlonymi ogrodami i basenem nad drogą wzdłuż wybrzeża; wygenerowany komputerowo budynek umieszczono na fotografii',
  'Flyfoto ved solnedgang av bygningen med opplyste hager og basseng over kystveien, med den datagenererte bygningen plassert inn i et fotografi',
  'Flygbild vid solnedgången av huset med upplysta trädgårdar och pool ovanför kustvägen, där det datorgenererade huset har placerats in i ett fotografi')
p('.media.items[4].caption', 'The block and the coast',
  'El bloque y la costa al atardecer', 'Le bâtiment et la côte au coucher du soleil', 'Das Gebäude und die Küste bei Sonnenuntergang',
  'Корпус и побережье на закате', 'المبنى والساحل عند الغروب', 'Het gebouw en de kust bij zonsondergang',
  'Budynek i wybrzeże o zachodzie słońca', 'Bygningen og kysten ved solnedgang', 'Huset och kusten vid solnedgången')
p('.media.items[5].alt', 'Aerial photograph of the coast',
  'Fotografía aérea de la costa de La Cala de Mijas con el bloque generado por ordenador colocado entre las casas, y las colinas detrás',
  'Photographie aérienne de la côte de La Cala de Mijas avec le bâtiment généré par ordinateur placé parmi les maisons, les collines derrière',
  'Luftaufnahme der Küste von La Cala de Mijas, mit dem computergenerierten Gebäude zwischen den Häusern platziert, dahinter die Hügel',
  'Аэрофотоснимок побережья Ла-Кала-де-Михас с компьютерной моделью корпуса, помещённой среди домов; позади холмы',
  'صورة جوية لساحل لا كالا دي ميخاس مع المبنى المُنشأ بالحاسوب موضوعًا بين المنازل، والتلال خلفه',
  'Luchtfoto van de kust bij La Cala de Mijas met het computergegenereerde gebouw tussen de huizen geplaatst, met de heuvels erachter',
  'Zdjęcie lotnicze wybrzeża La Cala de Mijas z wygenerowanym komputerowo budynkiem umieszczonym wśród domów, a za nim wzgórza',
  'Flyfoto av kysten ved La Cala de Mijas med den datagenererte bygningen plassert blant husene, med åsene bak',
  'Flygfoto av kusten vid La Cala de Mijas med det datorgenererade huset placerat bland husen, med kullarna bakom')
p('.media.items[5].caption', 'The block among its surroundings',
  'El bloque en su entorno', 'Le bâtiment dans son environnement', 'Das Gebäude in seiner Umgebung',
  'Корпус в окружающей застройке', 'المبنى في محيطه', 'Het gebouw in zijn omgeving',
  'Budynek w swoim otoczeniu', 'Bygningen i omgivelsene', 'Huset i sin omgivning')
p('.media.items[6].alt', 'Illustrated site plan',
  'Plano general ilustrado que muestra seis portales numerados en fila, con piscinas, tumbonas y jardines delante',
  'Plan de masse illustré montrant six cages numérotées en ligne, avec des piscines, des transats et des jardins devant',
  'Illustrierter Lageplan mit sechs nummerierten Aufgängen in einer Reihe, davor Pools, Sonnenliegen und Gärten',
  'Иллюстрированный генеральный план с шестью пронумерованными подъездами в ряд, перед ними бассейны, шезлонги и сады',
  'مخطط عام مصوَّر يُظهر ستة مداخل مرقّمة في صف واحد، مع مسابح ومقاعد استلقاء وحدائق أمامها',
  'Geïllustreerd situatieplan met zes genummerde portieken op een rij, met zwembaden, ligbedden en tuinen ervoor',
  'Ilustrowany plan zagospodarowania z sześcioma numerowanymi klatkami w jednym rzędzie, a przed nimi baseny, leżaki i ogrody',
  'Illustrert situasjonsplan med seks nummererte oppganger på rad, med bassenger, solsenger og hager foran',
  'Illustrerad situationsplan med sex numrerade uppgångar på rad, med pooler, solstolar och trädgårdar framför')
p('.media.items[6].caption', 'Site plan of the six portals',
  'Plano general de los seis portales', 'Plan de masse des six cages', 'Lageplan der sechs Aufgänge',
  'Генеральный план шести подъездов', 'المخطط العام للمداخل الستة', 'Situatieplan van de zes portieken',
  'Plan zagospodarowania sześciu klatek', 'Situasjonsplan for de seks oppgangene', 'Situationsplan för de sex uppgångarna')
p('.media.items[8].alt', 'Computer-generated terrace under a white pergola',
  'Terraza generada por ordenador bajo una pérgola blanca, con sofá rinconero, mesa de comedor y tumbonas, y vistas al mar por encima de una barandilla de vidrio',
  'Terrasse générée par ordinateur sous une pergola blanche, avec un canapé d’angle, une table à manger et des bains de soleil, et une vue sur la mer par-dessus un garde-corps en verre',
  'Computergenerierte Terrasse unter einer weißen Pergola mit Ecksofa, Esstisch und Liegen, mit Blick über eine Glasbrüstung auf das Meer',
  'Компьютерная визуализация террасы под белой перголой с угловым диваном, обеденным столом и лежаками, с видом на море через стеклянное ограждение',
  'تراس مُنشأ بالحاسوب تحت بيرغولا بيضاء مع كنبة زاوية وطاولة طعام ومقاعد استلقاء، وإطلالة على البحر من فوق درابزين زجاجي',
  'Computergegenereerd terras onder een witte pergola met een hoekbank, een eettafel en ligstoelen, met uitzicht op de zee over een glazen balustrade',
  'Wizualizacja komputerowa tarasu pod białą pergolą z sofą narożną, stołem jadalnianym i leżakami oraz widokiem na morze ponad szklaną balustradą',
  'Datagenerert terrasse under en hvit pergola med hjørnesofa, spisebord og solsenger, og utsikt over havet over et glassrekkverk',
  'Datorgenererad terrass under en vit pergola med hörnsoffa, matbord och solsängar, och utsikt över havet över ett glasräcke')
p('.media.items[9].alt', 'Computer-generated open-plan living room',
  'Salón de planta abierta generado por ordenador, con sofá, mesa de comedor e isla de cocina, y puertas correderas de vidrio a una terraza y al mar',
  'Séjour ouvert généré par ordinateur, avec un canapé, une table à manger et un îlot de cuisine, et des portes coulissantes en verre donnant sur une terrasse et sur la mer',
  'Computergenerierter offener Wohnbereich mit Sofa, Esstisch und Kücheninsel, mit Glasschiebetüren zu einer Terrasse und zum Meer',
  'Компьютерная визуализация гостиной открытой планировки с диваном, обеденным столом и кухонным островом; раздвижные стеклянные двери ведут на террасу, за которой море',
  'صالة مفتوحة مُنشأة بالحاسوب بأريكة وطاولة طعام وجزيرة مطبخ، مع أبواب زجاجية منزلقة إلى تراس والبحر',
  'Computergegenereerde open woonkamer met een bank, een eettafel en een keukeneiland, met glazen schuifdeuren naar een terras en de zee',
  'Wizualizacja komputerowa salonu w otwartym układzie z sofą, stołem jadalnianym i wyspą kuchenną oraz przesuwnymi szklanymi drzwiami na taras i morze',
  'Datagenerert åpen stue med sofa, spisebord og kjøkkenøy, med glasskyvedører til en terrasse og havet',
  'Datorgenererat öppet vardagsrum med soffa, matbord och köksö, med glasskjutdörrar till en terrass och havet')
p('.media.items[9].caption', 'Living room and dining area',
  'Salón y comedor', 'Séjour et salle à manger', 'Wohn- und Essbereich', 'Гостиная и обеденная зона', 'الصالة ومنطقة الطعام',
  'Woonkamer en eethoek', 'Salon i jadalnia', 'Stue og spiseplass', 'Vardagsrum och matplats')
p('.media.items[10].alt', 'Computer-generated kitchen',
  'Cocina generada por ordenador con isla de piedra y taburetes, horno integrado y placa de inducción, abierta a una terraza con vistas al mar',
  'Cuisine générée par ordinateur avec un îlot à plan de travail en pierre et des tabourets de bar, un four encastré et une plaque à induction, ouverte sur une terrasse avec vue sur la mer',
  'Computergenerierte Küche mit Kücheninsel mit Steinplatte und Barhockern, Einbaubackofen und Induktionskochfeld, die sich zu einer Terrasse mit Meerblick öffnet',
  'Компьютерная визуализация кухни с островом со столешницей из камня и барными стульями, встроенной духовкой и индукционной панелью; кухня выходит на террасу с видом на море',
  'مطبخ مُنشأ بالحاسوب بجزيرة بسطح حجري ومقاعد مرتفعة وفرن مدمج وموقد حثي، يُفتح على تراس بإطلالة على البحر',
  'Computergegenereerde keuken met een eiland met stenen blad en barkrukken, een inbouwoven en een inductiekookplaat, die uitkomt op een terras met uitzicht op de zee',
  'Wizualizacja komputerowa kuchni z wyspą z kamiennym blatem i hokerami, piekarnikiem do zabudowy i płytą indukcyjną, otwartej na taras z widokiem na morze',
  'Datagenerert kjøkken med en kjøkkenøy med steinplate og barkrakker, innebygd ovn og induksjonstopp, som åpner seg mot en terrasse med utsikt over havet',
  'Datorgenererat kök med en köksö med stenskiva och barstolar, inbyggd ugn och induktionshäll, som öppnar sig mot en terrass med utsikt över havet')
p('.media.items[11].caption', 'A bedroom with a timber headboard',
  'Un dormitorio con cabecero de madera', 'Une chambre avec une tête de lit en bois', 'Ein Schlafzimmer mit Kopfteil aus Holz',
  'Спальня с деревянным изголовьем', 'غرفة نوم بمسند رأس خشبي', 'Een slaapkamer met een houten hoofdbord',
  'Sypialnia z drewnianym zagłówkiem', 'Et soverom med hodegavl i tre', 'Ett sovrum med sänggavel i trä')
p('.media.items[12].alt', 'Computer-generated bedroom with a double bed, a padded',
  'Dormitorio generado por ordenador con cama doble, cabecero tapizado, armario empotrado blanco y una ventana alta con cortina',
  'Chambre générée par ordinateur avec un lit double, une tête de lit capitonnée, un placard intégré blanc et une grande fenêtre avec un rideau',
  'Computergeneriertes Schlafzimmer mit Doppelbett, gepolstertem Kopfteil, weißem Einbauschrank und einem hohen Fenster mit Vorhang',
  'Компьютерная визуализация спальни с двуспальной кроватью, мягким изголовьем, белым встроенным шкафом и высоким окном со шторой',
  'غرفة نوم مُنشأة بالحاسوب بسرير مزدوج ومسند رأس مبطّن وخزانة بيضاء مدمجة ونافذة عالية بستارة',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een gestoffeerd hoofdbord, een witte inbouwkast en een hoog raam met een gordijn',
  'Wizualizacja komputerowa sypialni z łóżkiem dwuosobowym, tapicerowanym zagłówkiem, białą szafą w zabudowie i wysokim oknem z zasłoną',
  'Datagenerert soverom med dobbeltseng, polstret hodegavl, hvitt innebygd garderobeskap og et høyt vindu med gardin',
  'Datorgenererat sovrum med dubbelsäng, stoppad sänggavel, inbyggd vit garderob och ett högt fönster med gardin')
p('.media.items[12].caption', 'A bedroom with a built-in wardrobe',
  'Un dormitorio con armario empotrado', 'Une chambre avec un placard intégré', 'Ein Schlafzimmer mit Einbauschrank',
  'Спальня со встроенным шкафом', 'غرفة نوم بخزانة مدمجة', 'Een slaapkamer met een inbouwkast',
  'Sypialnia z szafą w zabudowie', 'Et soverom med innebygd garderobeskap', 'Ett sovrum med inbyggd garderob')
p('.media.items[13].alt', 'Computer-generated bathroom',
  'Baño generado por ordenador con inodoro suspendido, ducha a ras de suelo con grifería negra, mueble de lavabo efecto madera y espejo oval retroiluminado',
  'Salle de bain générée par ordinateur avec un WC suspendu, une douche à l’italienne avec robinetterie noire, un meuble-vasque effet bois et un miroir ovale rétroéclairé',
  'Computergeneriertes Badezimmer mit Wand-WC, ebenerdiger Dusche mit schwarzen Armaturen, Waschtisch in Holzoptik und beleuchtetem ovalem Spiegel',
  'Компьютерная визуализация ванной комнаты с подвесным унитазом, душем без поддона с чёрной арматурой, тумбой под раковину под дерево и овальным зеркалом с подсветкой',
  'حمام مُنشأ بالحاسوب بمرحاض معلّق ودُش مفتوح بتجهيزات سوداء ووحدة مغسلة بمظهر الخشب ومرآة بيضوية بإضاءة خلفية',
  'Computergegenereerde badkamer met een hangend toilet, een inloopdouche met zwarte kranen, een badkamermeubel in houtlook en een ovale spiegel met achtergrondverlichting',
  'Wizualizacja komputerowa łazienki z podwieszaną miską WC, prysznicem bez brodzika z czarną armaturą, szafką pod umywalkę w drewnopodobnym wykończeniu i owalnym lustrem z podświetleniem',
  'Datagenerert bad med veggmontert toalett, en gulvflush dusj med svarte armaturer, en servantskap i trelook og et ovalt speil med baklys',
  'Datorgenererat badrum med väggmonterad toalett, en golvlös dusch med svarta armaturer, ett tvättställsskåp i trälook och en oval spegel med bakgrundsbelysning')
p('.media.items[13].caption', 'Bathroom with black fittings',
  'Baño con grifería negra', 'Salle de bain avec robinetterie noire', 'Badezimmer mit schwarzen Armaturen',
  'Ванная комната с чёрной арматурой', 'حمام بتجهيزات سوداء', 'Badkamer met zwarte kranen',
  'Łazienka z czarną armaturą', 'Bad med svarte armaturer', 'Badrum med svarta armaturer')

# ---- overview, why, architecture -----------------------------------------------------------------
p('.overview.headlineHtml', 'Fifty-four homes',
  'Cincuenta y cuatro viviendas, <em>trece listadas</em>', 'Cinquante-quatre logements, <em>treize listés</em>', 'Vierundfünfzig Wohnungen, <em>dreizehn aufgeführt</em>',
  'Пятьдесят четыре квартиры, <em>тринадцать в списке</em>', 'أربعة وخمسون مسكنًا، <em>ثلاثة عشر مدرجة</em>', 'Vierenvijftig woningen, <em>dertien vermeld</em>',
  'Pięćdziesiąt cztery lokale, <em>trzynaście na liście</em>', 'Femtifire boliger, <em>tretten oppført</em>', 'Femtiofyra bostäder, <em>tretton listade</em>')
p('.overview.copy[0]', 'Arosa is a complex of 54',
  'Arosa es un conjunto de 54 apartamentos en La Cala de Mijas, 13 de un dormitorio, 11 de dos y 30 de tres, según el dosier del promotor. El dosier describe viviendas de planta abierta con luz natural y vistas al mar, orientadas al sur, en seis portales numerados, con jardines paisajísticos, piscinas exteriores, una piscina interior, un gimnasio y zonas chill-out. Trece viviendas figuran con precio: tres de un dormitorio y una de dos en planta baja con jardín, dos de tres dormitorios en la primera planta y siete en la tercera planta con solárium.',
  'Arosa est un ensemble de 54 appartements à La Cala de Mijas, dont 13 de une chambre, 11 de deux et 30 de trois, selon le dossier du promoteur. Le dossier décrit des logements à plan ouvert, lumineux, avec vue sur la mer et orientés au sud, répartis en six cages numérotées, avec des jardins paysagers, des piscines extérieures, une piscine intérieure, une salle de sport et des espaces chill-out. Treize logements sont listés avec un prix : trois de une chambre et un de deux chambres au rez-de-chaussée avec jardin, deux de trois chambres au premier étage et sept au troisième étage avec solarium.',
  'Arosa ist eine Anlage mit 54 Wohnungen in La Cala de Mijas, davon 13 mit einem, 11 mit zwei und 30 mit drei Schlafzimmern, laut der Broschüre des Bauträgers. Die Broschüre beschreibt offen geschnittene, lichtdurchflutete Wohnungen mit Meerblick und Südausrichtung in sechs nummerierten Aufgängen, mit Gartenanlagen, Außenpools, einem Innenpool, einem Fitnessraum und Chill-out-Bereichen. Dreizehn Wohnungen sind mit Preis aufgeführt: drei mit einem Schlafzimmer und eine mit zwei Schlafzimmern im Erdgeschoss mit Garten, zwei mit drei Schlafzimmern im ersten Obergeschoss und sieben im dritten Obergeschoss mit Solarium.',
  'Arosa — комплекс из 54 квартир в Ла-Кала-де-Михас: 13 с одной спальней, 11 с двумя и 30 с тремя, по данным буклета застройщика. Буклет описывает квартиры открытой планировки с естественным светом и видом на море, обращённые на юг, в шести пронумерованных подъездах, с ландшафтными садами, наружными бассейнами, крытым бассейном, тренажёрным залом и зонами отдыха chill-out. С ценой указаны тринадцать квартир: три с одной спальней и одна с двумя спальнями на первом этаже с садом, две с тремя спальнями на втором этаже и семь на четвёртом этаже с солярием.',
  'Arosa مجمّع من 54 شقة في لا كالا دي ميخاس، منها 13 بغرفة نوم و11 بغرفتي نوم و30 بثلاث غرف نوم، بحسب كتيّب المطوّر. يصف الكتيّب مساكن مفتوحة التصميم بإضاءة طبيعية وإطلالات على البحر ومتجهة نحو الجنوب، موزعة على ستة مداخل مرقّمة، مع حدائق مُنسّقة ومسابح خارجية ومسبح داخلي وصالة رياضية ومناطق استرخاء. وردت ثلاثة عشر مسكنًا مع السعر: ثلاثة بغرفة نوم ومسكن بغرفتي نوم في الطابق الأرضي مع حديقة، ومسكنان بثلاث غرف نوم في الطابق الأول، وسبعة مساكن في الطابق الثالث مع سولاريوم.',
  'Arosa is een complex van 54 appartementen in La Cala de Mijas, 13 met een slaapkamer, 11 met twee en 30 met drie, volgens de brochure van de ontwikkelaar. De brochure beschrijft woningen met een open indeling, veel natuurlijk licht en zeezicht, op het zuiden gericht, in zes genummerde portieken, met aangelegde tuinen, buitenzwembaden, een binnenzwembad, een fitnessruimte en chill-outzones. Dertien woningen zijn met een prijs vermeld: drie met een slaapkamer en een met twee slaapkamers op de begane grond met een tuin, twee met drie slaapkamers op de eerste verdieping en zeven op de derde verdieping met een solarium.',
  'Arosa to zespół 54 mieszkań w La Cala de Mijas: 13 z jedną sypialnią, 11 z dwiema i 30 z trzema, według broszury dewelopera. Broszura opisuje mieszkania w otwartym układzie, z naturalnym światłem i widokiem na morze, wystawione na południe, w sześciu numerowanych klatkach, z ogrodami, basenami zewnętrznymi, basenem wewnętrznym, siłownią i strefami chill-out. Trzynaście lokali jest podanych z ceną: trzy z jedną sypialnią i jeden z dwiema na parterze z ogrodem, dwa z trzema sypialniami na pierwszym piętrze i siedem na trzecim piętrze z solarium.',
  'Arosa er et anlegg med 54 leiligheter i La Cala de Mijas, 13 med ett soverom, 11 med to og 30 med tre, ifølge utbyggerens brosjyre. Brosjyren beskriver boliger med åpen planløsning, naturlig lys og utsikt over havet, vendt mot sør, i seks nummererte oppganger, med opparbeidede hager, utendørs basseng, et innendørs basseng, treningsrom og chill-out-områder. Tretten boliger er oppført med pris: tre med ett soverom og én med to soverom i første etasje med hage, to med tre soverom i andre etasje og syv i fjerde etasje med solterrasse.',
  'Arosa är ett område med 54 lägenheter i La Cala de Mijas, 13 med ett sovrum, 11 med två och 30 med tre, enligt exploatörens broschyr. Broschyren beskriver bostäder med öppen planlösning, naturligt ljus och havsutsikt, vända mot söder, i sex numrerade uppgångar, med anlagda trädgårdar, utomhuspooler, en inomhuspool, gym och chill out-ytor. Tretton bostäder är listade med pris: tre med ett sovrum och en med två sovrum på bottenvåningen med trädgård, två med tre sovrum på första våningen och sju på tredje våningen med solterrass.')
p('.overview.copy[1]', 'The infosheet gives the building licence',
  'La ficha informativa indica que la licencia de obras está concedida, el inicio de obra previsto para el segundo trimestre de 2026 y el fin de obra previsto para el cuarto trimestre de 2028, y la lista de disponibilidad da la fase como en construcción. La ficha no lleva fecha de emisión y el fin de obra es una estimación, por lo que preguntamos hasta dónde ha avanzado la obra.',
  'La fiche d’information indique que le permis de construire est accordé, le début des travaux attendu au deuxième trimestre 2026 et la fin des travaux attendue au quatrième trimestre 2028, et la liste de disponibilité donne l’état d’avancement comme en construction. La fiche ne porte pas de date d’émission et la fin des travaux est une estimation ; nous demandons donc où en est le chantier.',
  'Das Infoblatt gibt die Baugenehmigung als erteilt an, den Baubeginn für das zweite Quartal 2026 und das Bauende für das vierte Quartal 2028 als erwartet, und die Verfügbarkeitsliste nennt als Stand „im Bau“. Das Infoblatt trägt kein Ausgabedatum, und das Bauende ist eine Schätzung; wir fragen daher nach, wie weit der Bau fortgeschritten ist.',
  'В информационном листе указано, что разрешение на строительство выдано, начало строительства ожидается во втором квартале 2026 года, а окончание — в четвёртом квартале 2028 года; в списке наличия стадия указана как «строится». В листе нет даты выпуска, а окончание строительства — лишь оценка, поэтому мы уточняем, как далеко продвинулась стройка.',
  'تذكر ورقة المعلومات أن رخصة البناء ممنوحة، وأن بدء الإنشاء متوقع في الربع الثاني من عام 2026 وانتهاءه متوقع في الربع الرابع من عام 2028، وتذكر قائمة التوفر أن المرحلة قيد الإنشاء. ولا تحمل ورقة المعلومات تاريخ إصدار، وانتهاء الإنشاء تقدير، لذلك نستفسر عن مدى تقدّم الأعمال.',
  'Het infoblad geeft aan dat de bouwvergunning is verleend, dat de start van de bouw wordt verwacht in het tweede kwartaal van 2026 en het einde van de bouw in het vierde kwartaal van 2028, en de beschikbaarheidslijst geeft de fase als in aanbouw. Het infoblad vermeldt geen uitgiftedatum en het einde van de bouw is een schatting, dus we vragen hoe ver de bouw is gevorderd.',
  'Karta informacyjna podaje, że pozwolenie na budowę zostało udzielone, rozpoczęcie budowy jest oczekiwane w drugim kwartale 2026 roku, a jej zakończenie w czwartym kwartale 2028 roku, natomiast lista dostępności podaje etap jako w budowie. Karta nie ma daty wydania, a zakończenie budowy jest szacunkiem, dlatego pytamy, jak daleko zaawansowana jest budowa.',
  'Infobladet oppgir at byggetillatelsen er gitt, at byggestart er ventet i andre kvartal 2026 og byggeslutt i fjerde kvartal 2028, og tilgjengelighetslisten oppgir stadiet som under bygging. Infobladet har ingen utstedelsesdato, og byggeslutt er et anslag, så vi spør hvor langt byggingen har kommet.',
  'Informationsbladet anger att bygglovet är beviljat, att byggstart väntas under andra kvartalet 2026 och byggslut under fjärde kvartalet 2028, och tillgänglighetslistan anger skedet som under uppförande. Informationsbladet har inget utfärdandedatum och byggslutet är en uppskattning, så vi frågar hur långt bygget har kommit.')
p('.overview.metrics[0][1]', '54 homes',
  '54 viviendas', '54 logements', '54 Wohnungen', '54 квартиры', '54 مسكنًا', '54 woningen', '54 lokale', '54 boliger', '54 bostäder')
p('.overview.metrics[1][1]', '13 homes',
  '13 viviendas', '13 logements', '13 Wohnungen', '13 квартир', '13 مسكنًا', '13 woningen', '13 lokali', '13 boliger', '13 bostäder')

p('.why.copy', 'One-, two- and three-bedroom apartments with sea views',
  'Apartamentos de uno, dos y tres dormitorios con vistas al mar, piscinas comunitarias y gimnasio en La Cala de Mijas, desde {E705000} más IVA.',
  'Appartements de une, deux et trois chambres avec vue sur la mer, piscines communes et salle de sport à La Cala de Mijas, à partir de {E705000} hors TVA.',
  'Wohnungen mit einem, zwei und drei Schlafzimmern mit Meerblick, Gemeinschaftspools und Fitnessraum in La Cala de Mijas, ab {E705000} zuzüglich MwSt.',
  'Квартиры с одной, двумя и тремя спальнями, видом на море, общими бассейнами и тренажёрным залом в Ла-Кала-де-Михас, от {E705000} без НДС.',
  'شقق بغرفة نوم وغرفتي نوم وثلاث غرف نوم بإطلالة على البحر ومسابح مشتركة وصالة رياضية في لا كالا دي ميخاس، ابتداءً من {E705000} دون ضريبة القيمة المضافة.',
  'Appartementen met een, twee en drie slaapkamers met zeezicht, gemeenschappelijke zwembaden en een fitnessruimte in La Cala de Mijas, vanaf {E705000} excl. btw.',
  'Mieszkania z jedną, dwiema i trzema sypialniami, z widokiem na morze, wspólnymi basenami i siłownią w La Cala de Mijas, od {E705000} plus VAT.',
  'Leiligheter med ett, to og tre soverom, utsikt over havet, felles basseng og treningsrom i La Cala de Mijas, fra {E705000} pluss mva.',
  'Lägenheter med ett, två och tre sovrum, havsutsikt, gemensamma pooler och gym i La Cala de Mijas, från {E705000} plus IVA.')
p('.why.points[0][1]', 'Buyers who want a new apartment',
  'Compradores que quieren un apartamento nuevo en la costa de Mijas con vistas al mar, para vivir en él o como segunda residencia, desde un apartamento de un dormitorio con jardín hasta una vivienda de tres dormitorios con solárium.',
  'Acheteurs qui souhaitent un appartement neuf sur la côte de Mijas avec vue sur la mer, pour y vivre ou comme résidence secondaire, d’un appartement de une chambre avec jardin à un logement de trois chambres avec solarium.',
  'Käufer, die eine neue Wohnung an der Küste von Mijas mit Meerblick suchen, zum Selbstbewohnen oder als Zweitwohnsitz, von der Gartenwohnung mit einem Schlafzimmer bis zur Wohnung mit drei Schlafzimmern und Solarium.',
  'Покупателям, которым нужна новая квартира на побережье Михаса с видом на море, для проживания или как второй дом: от квартиры с одной спальней и садом до квартиры с тремя спальнями и солярием.',
  'للمشترين الذين يريدون شقة جديدة على ساحل ميخاس بإطلالة على البحر، للسكن أو كمنزل ثانٍ، من شقة بغرفة نوم مع حديقة إلى مسكن بثلاث غرف نوم مع سولاريوم.',
  'Kopers die een nieuw appartement aan de kust van Mijas met zeezicht willen, om in te wonen of als tweede woning, van een tuinappartement met een slaapkamer tot een woning met drie slaapkamers en een solarium.',
  'Kupujący, którzy szukają nowego mieszkania na wybrzeżu Mijas z widokiem na morze, do zamieszkania lub jako drugi dom: od mieszkania z jedną sypialnią i ogrodem po lokal z trzema sypialniami i solarium.',
  'Kjøpere som vil ha en ny leilighet på Mijas-kysten med utsikt over havet, til å bo i eller som feriebolig, fra en leilighet med ett soverom og hage til en bolig med tre soverom og solterrasse.',
  'Köpare som vill ha en ny lägenhet på Mijaskusten med havsutsikt, att bo i eller som andra bostad, från en lägenhet med ett sovrum och trädgård till en bostad med tre sovrum och solterrass.')
p('.why.points[1][1]', 'Gardens of 29 to 46',
  'Jardines de 29 a 46 {U} en las cuatro viviendas de planta baja, soláriums de 77 a 104 {U} en las siete viviendas de la tercera planta, y piscinas exterior e interior, gimnasio y sauna en el conjunto.',
  'Des jardins de 29 à 46 {U} pour les quatre logements du rez-de-chaussée, des solariums de 77 à 104 {U} pour les sept logements du troisième étage, et dans l’ensemble des piscines extérieure et intérieure, une salle de sport et un sauna.',
  'Gärten von 29 bis 46 {U} bei den vier Wohnungen im Erdgeschoss, Solarien von 77 bis 104 {U} bei den sieben Wohnungen im dritten Obergeschoss sowie Außen- und Innenpool, Fitnessraum und Sauna in der Anlage.',
  'Сады площадью от 29 до 46 {U} у четырёх квартир первого этажа, солярии от 77 до 104 {U} у семи квартир четвёртого этажа, а в комплексе — наружный и крытый бассейны, тренажёрный зал и сауна.',
  'حدائق بمساحة 29 إلى 46 {U} في المساكن الأربعة بالطابق الأرضي، وسولاريومات بمساحة 77 إلى 104 {U} في المساكن السبعة بالطابق الثالث، ومسبحان خارجي وداخلي وصالة رياضية وساونا في المجمع.',
  'Tuinen van 29 tot 46 {U} bij de vier woningen op de begane grond, solariums van 77 tot 104 {U} bij de zeven woningen op de derde verdieping, en een buiten- en een binnenzwembad, een fitnessruimte en een sauna in het complex.',
  'Ogrody o powierzchni od 29 do 46 {U} przy czterech lokalach na parterze, solaria od 77 do 104 {U} przy siedmiu lokalach na trzecim piętrze oraz baseny zewnętrzne i wewnętrzny, siłownia i sauna na terenie zespołu.',
  'Hager på 29 til 46 {U} ved de fire boligene i første etasje, solterrasser på 77 til 104 {U} ved de syv boligene i fjerde etasje, og utendørs og innendørs basseng, treningsrom og badstue i anlegget.',
  'Trädgårdar på 29 till 46 {U} vid de fyra bostäderna på bottenvåningen, solterrasser på 77 till 104 {U} vid de sju bostäderna på tredje våningen, och pooler utomhus och inomhus, gym och bastu i området.')
p('.why.points[2][1]', 'The developer’s map marks Fuengirola',
  'El mapa del promotor sitúa el centro de Fuengirola a 10, el centro de Marbella a 20 y el aeropuerto de Málaga a 25, que interpretamos como minutos, y muestra varios campos de golf cercanos.',
  'La carte du promoteur indique le centre de Fuengirola à 10, le centre de Marbella à 20 et l’aéroport de Málaga à 25, que nous lisons comme des minutes, et montre plusieurs terrains de golf à proximité.',
  'Die Karte des Bauträgers gibt das Zentrum von Fuengirola mit 10, das Zentrum von Marbella mit 20 und den Flughafen Málaga mit 25 an, was wir als Minuten lesen, und zeigt mehrere Golfplätze in der Nähe.',
  'На карте застройщика центр Фуэнхиролы отмечен как 10, центр Марбельи — как 20, а аэропорт Малаги — как 25, что мы читаем как минуты; рядом показаны несколько полей для гольфа.',
  'تضع خريطة المطوّر وسط فوينخيرولا عند 10 ووسط ماربيا عند 20 ومطار مالقة عند 25، ونقرأ ذلك على أنه دقائق، وتُظهر عدة ملاعب غولف قريبة.',
  'Op de kaart van de ontwikkelaar staat het centrum van Fuengirola op 10, het centrum van Marbella op 20 en de luchthaven van Málaga op 25, wat wij als minuten lezen, en staan er enkele golfbanen in de buurt op.',
  'Na mapie dewelopera centrum Fuengiroli oznaczono jako 10, centrum Marbelli jako 20, a lotnisko w Maladze jako 25, co odczytujemy jako minuty, oraz pokazano kilka pobliskich pól golfowych.',
  'Utbyggerens kart markerer Fuengirola sentrum med 10, Marbella sentrum med 20 og Málaga lufthavn med 25, som vi leser som minutter, og viser flere golfbaner i nærheten.',
  'Exploatörens karta markerar Fuengirola centrum med 10, Marbella centrum med 20 och Málaga flygplats med 25, vilket vi läser som minuter, och visar flera golfbanor i närheten.')
p('.why.points[3][1]', 'The end of construction is an estimate for the fourth quarter',
  'El fin de obra es una estimación para el cuarto trimestre de 2028, y la lista y los planos difieren en la superficie construida de tres viviendas, por lo que confirmamos el estado de la obra y las cifras antes de cualquier reserva.',
  'La fin des travaux est une estimation pour le quatrième trimestre 2028, et la liste et les plans diffèrent sur la surface construite de trois logements ; nous confirmons donc l’état d’avancement du chantier et les chiffres avant toute réservation.',
  'Das Bauende ist eine Schätzung für das vierte Quartal 2028, und die Liste und die Pläne weichen bei der bebauten Fläche von drei Wohnungen voneinander ab; wir bestätigen daher den Baufortschritt und die Zahlen vor jeder Reservierung.',
  'Окончание строительства — это оценка на четвёртый квартал 2028 года, а список и планы расходятся по площади застройки трёх квартир, поэтому до любого бронирования мы уточняем стадию строительства и цифры.',
  'انتهاء الإنشاء تقدير للربع الرابع من عام 2028، وتختلف القائمة والمخططات في المساحة المبنية لثلاثة مساكن، لذلك نؤكد مرحلة الأعمال والأرقام قبل أي حجز.',
  'Het einde van de bouw is een schatting voor het vierde kwartaal van 2028, en de lijst en de plattegronden wijken af voor de bebouwde oppervlakte van drie woningen, dus we bevestigen de bouwfase en de cijfers vóór elke reservering.',
  'Zakończenie budowy to szacunek na czwarty kwartał 2028 roku, a lista i rzuty różnią się co do powierzchni zabudowy trzech lokali, dlatego przed jakąkolwiek rezerwacją potwierdzamy etap budowy i liczby.',
  'Byggeslutt er et anslag for fjerde kvartal 2028, og listen og plantegningene avviker på bebygd areal for tre boliger, så vi bekrefter byggestadiet og tallene før enhver reservasjon.',
  'Byggslutet är en uppskattning för fjärde kvartalet 2028, och listan och planritningarna avviker i byggyta för tre bostäder, så vi bekräftar byggstadiet och siffrorna före varje reservation.')

p('.architecture.headlineHtml', 'Stepped terraces',
  'Terrazas escalonadas, <em>abiertas al mar</em>', 'Terrasses en gradins, <em>ouvertes sur la mer</em>', 'Gestaffelte Terrassen, <em>zum Meer geöffnet</em>',
  'Ступенчатые террасы, <em>открытые к морю</em>', 'تراسات متدرّجة، <em>مفتوحة على البحر</em>', 'Getrapte terrassen, <em>open naar de zee</em>',
  'Schodkowe tarasy, <em>otwarte na morze</em>', 'Trappetrinnsformede terrasser, <em>åpne mot havet</em>', 'Trappstegsformade terrasser, <em>öppna mot havet</em>')
p('.architecture.copy[0]', 'In the renders the block rises',
  'En las infografías el bloque se eleva en terrazas blancas escalonadas con barandillas de vidrio, celosías en tonos madera y pérgolas en los niveles superiores, entre jardines y piscinas.',
  'Dans les images de synthèse, le bâtiment s’élève en terrasses blanches en gradins, avec des garde-corps en verre, des écrans aux tons bois et des pergolas aux niveaux supérieurs, au milieu de jardins et de piscines.',
  'In den Visualisierungen steigt das Gebäude in gestaffelten weißen Terrassen mit Glasbrüstungen, holzfarbenen Sichtschutzelementen und Pergolen auf den oberen Ebenen auf, eingebettet in Gärten und Pools.',
  'На визуализациях корпус поднимается белыми ступенчатыми террасами со стеклянными ограждениями, экранами в тонах дерева и перголами на верхних уровнях среди садов и бассейнов.',
  'في التصاميم المُنشأة بالحاسوب يرتفع المبنى بتراسات بيضاء متدرّجة بدرابزين زجاجي وحواجز بألوان الخشب وبيرغولات في الطوابق العليا، وسط الحدائق والمسابح.',
  'Op de visualisaties rijst het gebouw op in getrapte witte terrassen met glazen balustrades, schermen in houttinten en pergola’s op de bovenste niveaus, te midden van tuinen en zwembaden.',
  'Na wizualizacjach budynek wznosi się schodkowymi białymi tarasami ze szklanymi balustradami, ekranami w odcieniach drewna i pergolami na wyższych poziomach, wśród ogrodów i basenów.',
  'På visualiseringene hever bygningen seg i trappetrinnsformede hvite terrasser med glassrekkverk, skjermer i trefarger og pergolaer på de øvre nivåene, midt i hager og bassenger.',
  'På visualiseringarna reser sig huset i trappstegsformade vita terrasser med glasräcken, skärmar i trätoner och pergolor på de övre nivåerna, mitt bland trädgårdar och pooler.')
p('.architecture.copy[1]', 'The developer’s dossier describes terraces',
  'El dosier del promotor describe terrazas concebidas como una extensión natural del interior, y soláriums orientados al sur con vistas al mar.',
  'Le dossier du promoteur décrit des terrasses conçues comme un prolongement naturel de l’intérieur, et des solariums orientés au sud avec vue sur la mer.',
  'Die Broschüre des Bauträgers beschreibt Terrassen als natürliche Erweiterung des Innenraums sowie nach Süden ausgerichtete Solarien mit Meerblick.',
  'В буклете застройщика террасы описаны как естественное продолжение интерьера, а солярии — как обращённые на юг, с видом на море.',
  'يصف كتيّب المطوّر التراسات بأنها امتداد طبيعي للداخل، والسولاريومات بأنها متجهة نحو الجنوب وبإطلالات على البحر.',
  'De brochure van de ontwikkelaar beschrijft terrassen als een natuurlijke verlenging van het interieur, en op het zuiden gerichte solariums met zeezicht.',
  'Broszura dewelopera opisuje tarasy jako naturalne przedłużenie wnętrza oraz solaria zwrócone na południe, z widokiem na morze.',
  'Utbyggerens brosjyre beskriver terrasser utformet som en naturlig forlengelse av interiøret, og solterrasser vendt mot sør med utsikt over havet.',
  'Exploatörens broschyr beskriver terrasser utformade som en naturlig förlängning av interiören, och solterrasser vända mot söder med havsutsikt.')
p('.architecture.highlights[0][1]', 'Reinforced concrete flat slabs',
  'Forjados planos de hormigón armado, con muros de hormigón armado en el sótano, conforme al Código Técnico de la Edificación.',
  'Dalles planes en béton armé, avec des murs en béton armé au sous-sol, conformes au Code technique du bâtiment.',
  'Flachdecken aus Stahlbeton, mit Kellerwänden aus Stahlbeton, nach dem spanischen Bautechnikkodex.',
  'Плоские железобетонные перекрытия и железобетонные стены в подвале в соответствии с Техническим строительным кодексом.',
  'بلاطات مسطحة من الخرسانة المسلحة، مع جدران من الخرسانة المسلحة في القبو، وفق المدونة التقنية للبناء.',
  'Vlakke vloeren van gewapend beton, met wanden van gewapend beton in de kelder, volgens de Spaanse technische bouwcode.',
  'Płaskie stropy żelbetowe i żelbetowe ściany w piwnicy, zgodnie z hiszpańskim Kodeksem Technicznym Budownictwa.',
  'Flate dekker i armert betong, med kjellervegger i armert betong, i samsvar med den spanske tekniske byggekoden.',
  'Platta bjälklag i armerad betong, med källarväggar i armerad betong, enligt den spanska tekniska byggnormen.')
p('.architecture.highlights[1][1]', 'A double exterior wall',
  'Un doble cerramiento exterior, con ladrillo macizo perforado en la hoja exterior y un trasdosado autoportante en seco con aislamiento térmico en la interior.',
  'Une double paroi extérieure, avec de la brique pleine perforée à l’extérieur et un doublage autoporteur à sec avec isolation thermique à l’intérieur.',
  'Eine doppelte Außenwand mit gelochtem Vollziegel außen und einer selbsttragenden Trockenbau-Vorsatzschale mit Wärmedämmung innen.',
  'Двойная наружная стена: снаружи из перфорированного полнотелого кирпича, внутри — самонесущая сухая облицовка с теплоизоляцией.',
  'جدار خارجي مزدوج، بطوب مصمت مثقّب من الخارج وكسوة جافة ذاتية الحمل بعزل حراري من الداخل.',
  'Een dubbele buitenmuur, met geperforeerde volle baksteen aan de buitenzijde en een zelfdragende droge voorzetwand met thermische isolatie aan de binnenzijde.',
  'Podwójna ściana zewnętrzna: z zewnątrz z perforowanej cegły pełnej, od wewnątrz z samonośną okładziną z płyt suchych z izolacją termiczną.',
  'En dobbel yttervegg, med perforert massivt murstein utvendig og en selvbærende tørrbygget innvendig kledning med varmeisolasjon.',
  'En dubbel yttervägg, med perforerat massivt tegel utvändigt och en självbärande torrbyggd invändig beklädnad med värmeisolering.')
p('.architecture.highlights[2][1]', 'Lacquered aluminium frames with a thermal break and double',
  'Carpintería de aluminio lacado con rotura de puente térmico y doble acristalamiento termoacústico, con puertas correderas empotradas en el suelo hacia las terrazas en la fachada principal.',
  'Menuiseries en aluminium laqué à rupture de pont thermique et double vitrage thermo-acoustique, avec des portes coulissantes encastrées dans le sol vers les terrasses sur la façade principale.',
  'Lackierte Aluminiumrahmen mit thermischer Trennung und thermoakustischer Doppelverglasung, mit im Boden versenkten Schiebetüren zu den Terrassen an der Hauptfassade.',
  'Окрашенные алюминиевые рамы с терморазрывом и двойное термоакустическое остекление, с раздвижными дверями, утопленными в пол, на террасы главного фасада.',
  'إطارات من الألومنيوم المطلي بقاطع حراري وزجاج مزدوج حراري صوتي، مع أبواب منزلقة مدفونة في الأرضية نحو التراسات في الواجهة الرئيسية.',
  'Gelakte aluminium kozijnen met thermische onderbreking en thermo-akoestische dubbele beglazing, met in de vloer verzonken schuifdeuren naar de terrassen aan de hoofdgevel.',
  'Lakierowane ramy aluminiowe z przekładką termiczną i podwójne szyby termoakustyczne, z przesuwnymi drzwiami wpuszczonymi w podłogę prowadzącymi na tarasy w głównej elewacji.',
  'Lakkerte aluminiumsrammer med termisk brudd og termoakustisk dobbeltglass, med skyvedører senket i gulvet mot terrassene på hovedfasaden.',
  'Lackerade aluminiumkarmar med termisk brytning och termoakustiskt dubbelglas, med skjutdörrar infällda i golvet mot terrasserna på huvudfasaden.')
p('.architecture.highlights[3][1]', 'Flat roofs, waterproofed and insulated',
  'Cubiertas planas impermeabilizadas y aisladas, con grava donde no se transita y pavimento cerámico y porcelánico antideslizante en las terrazas.',
  'Toitures plates étanchées et isolées, en gravier là où l’on ne circule pas et avec un revêtement antidérapant en céramique et grès cérame sur les terrasses.',
  'Flachdächer, abgedichtet und gedämmt, mit Kies dort, wo niemand läuft, und rutschhemmendem Keramik- und Feinsteinzeugbelag auf den Terrassen.',
  'Плоские кровли с гидроизоляцией и утеплением: гравий там, где не ходят, и нескользящее покрытие из керамики и керамогранита на террасах.',
  'أسقف مسطحة معزولة مائيًا وحراريًا، بالحصى حيث لا يُسار عليها، وببلاط سيراميك وبورسلان مانع للانزلاق على التراسات.',
  'Platte daken, waterdicht en geïsoleerd, met grind waar niemand loopt en antislip keramische en porseleinen tegels op de terrassen.',
  'Dachy płaskie z hydroizolacją i izolacją, ze żwirem tam, gdzie nikt nie chodzi, oraz antypoślizgową okładziną ceramiczną i z gresu na tarasach.',
  'Flate tak, tettet og isolert, med grus der ingen går og sklisikre keramiske og porselensfliser på terrassene.',
  'Platta tak, tätade och isolerade, med grus där ingen går och halkfri keramik och klinker på terrasserna.')

# ---- quality specification -------------------------------------------------------------------------
p('.qualitySpecs.sourceNote', 'Source: the quality specification',
  'Fuente: la memoria de calidades de los documentos del promotor, que no lleva fecha. Indica que está en fase de desarrollo y que sus referencias pueden cambiar por razones técnicas sin reducir la calidad ni el diseño del resultado.',
  'Source : le descriptif technique figurant dans les documents du promoteur, qui n’est pas daté. Il précise qu’il est au stade du développement et que ses références peuvent changer pour des raisons techniques sans diminuer la qualité ni le design du résultat.',
  'Quelle: die Baubeschreibung in den Unterlagen des Bauträgers, die kein Datum trägt. Sie gibt an, dass sie sich im Entwicklungsstadium befindet und dass ihre Angaben aus technischen Gründen geändert werden können, ohne dass Qualität oder Design des Ergebnisses darunter leiden.',
  'Источник: спецификация материалов и отделки в документах застройщика, не имеющая даты. В ней сказано, что она находится на стадии разработки и что её позиции могут изменяться по техническим причинам без снижения качества и дизайна результата.',
  'المصدر: مواصفات البناء الواردة في وثائق المطوّر، وهي غير مؤرخة. وتذكر أنها في مرحلة التطوير وأن مراجعها قد تتغير لأسباب فنية دون أي انخفاض في جودة النتيجة أو تصميمها.',
  'Bron: het lastenboek in de documenten van de ontwikkelaar, dat geen datum draagt. Het geeft aan dat het zich in de ontwikkelingsfase bevindt en dat de verwijzingen om technische redenen kunnen wijzigen zonder dat de kwaliteit of het ontwerp van het resultaat daaronder lijdt.',
  'Źródło: specyfikacja techniczna w dokumentach dewelopera, niedatowana. Zaznacza ona, że jest na etapie opracowania i że jej odniesienia mogą się zmienić z przyczyn technicznych bez obniżenia jakości ani projektu efektu końcowego.',
  'Kilde: beskrivelsen i utbyggerens dokumenter, som ikke er datert. Den oppgir at den er på utviklingsstadiet og at referansene kan endres av tekniske grunner uten at kvaliteten eller designet på resultatet reduseres.',
  'Källa: byggbeskrivningen i exploatörens dokument, som saknar datum. Den anger att den är på utvecklingsstadiet och att dess referenser kan ändras av tekniska skäl utan att resultatets kvalitet eller design försämras.')
p('.qualitySpecs.groups[0].name', 'Structure and partitions',
  'Estructura y particiones', 'Structure et cloisons', 'Konstruktion und Trennwände', 'Конструкция и перегородки', 'الهيكل والقواطع', 'Structuur en scheidingswanden',
  'Konstrukcja i przegrody', 'Konstruksjon og skillevegger', 'Stomme och mellanväggar')
p('.qualitySpecs.groups[0].items[0]', 'Reinforced concrete basement walls and flat slabs',
  'Muros de sótano y forjados planos de hormigón armado conforme al Código Técnico de la Edificación, con doble cerramiento exterior de ladrillo macizo perforado y trasdosado autoportante en seco con aislamiento térmico.',
  'Murs de sous-sol et dalles planes en béton armé conformes au Code technique du bâtiment, avec une double paroi extérieure en brique pleine perforée et un doublage autoporteur à sec avec isolation thermique.',
  'Kellerwände und Flachdecken aus Stahlbeton nach dem spanischen Bautechnikkodex, mit doppelter Außenwand aus gelochtem Vollziegel und selbsttragender Trockenbau-Vorsatzschale mit Wärmedämmung.',
  'Стены подвала и плоские перекрытия из железобетона в соответствии с Техническим строительным кодексом, двойная наружная стена из перфорированного полнотелого кирпича и самонесущая сухая облицовка с теплоизоляцией.',
  'جدران قبو وبلاطات مسطحة من الخرسانة المسلحة وفق المدونة التقنية للبناء، مع جدار خارجي مزدوج من الطوب المصمت المثقّب وكسوة جافة ذاتية الحمل بعزل حراري.',
  'Kelderwanden en vlakke vloeren van gewapend beton volgens de Spaanse technische bouwcode, met een dubbele buitenmuur van geperforeerde volle baksteen en een zelfdragende droge voorzetwand met thermische isolatie.',
  'Ściany piwnicy i płaskie stropy żelbetowe zgodnie z hiszpańskim Kodeksem Technicznym Budownictwa, z podwójną ścianą zewnętrzną z perforowanej cegły pełnej i samonośną okładziną z płyt suchych z izolacją termiczną.',
  'Kjellervegger og flate dekker i armert betong i samsvar med den spanske tekniske byggekoden, med en dobbel yttervegg av perforert massivt murstein og en selvbærende tørrbygget kledning med varmeisolasjon.',
  'Källarväggar och platta bjälklag i armerad betong enligt den spanska tekniska byggnormen, med en dubbel yttervägg av perforerat massivt tegel och en självbärande torrbyggd beklädnad med värmeisolering.')
p('.qualitySpecs.groups[0].items[1]', 'Homes separated by half a foot',
  'Viviendas separadas por medio pie de ladrillo macizo perforado con doble trasdosado autoportante y aislamiento acústico, y estancias divididas con tabiquería seca autoportante.',
  'Logements séparés par un demi-brique pleine perforée avec un double doublage autoporteur et une isolation acoustique, et pièces séparées par des cloisons sèches autoporteuses.',
  'Wohnungen durch ein halbsteinstarkes Mauerwerk aus gelochtem Vollziegel mit doppelter selbsttragender Vorsatzschale und Schallschutz getrennt, und Räume durch selbsttragende Trockenbauwände unterteilt.',
  'Квартиры разделены стеной в полкирпича из перфорированного полнотелого кирпича с двойной самонесущей облицовкой и звукоизоляцией, а помещения внутри квартир — самонесущими сухими перегородками.',
  'فصل المساكن بنصف قدم من الطوب المصمت المثقّب مع كسوة مزدوجة ذاتية الحمل وعزل صوتي، وتقسيم الغرف بقواطع جافة ذاتية الحمل.',
  'Woningen gescheiden door een halfsteens muur van geperforeerde volle baksteen met een dubbele zelfdragende voorzetwand en geluidsisolatie, en kamers verdeeld met zelfdragende droge scheidingswanden.',
  'Lokale oddzielone ścianą z perforowanej cegły pełnej o grubości pół cegły z podwójną samonośną okładziną i izolacją akustyczną, a pomieszczenia podzielone samonośnymi ściankami działowymi z płyt suchych.',
  'Boligene er skilt med en halvsteins vegg av perforert massivt murstein med dobbel selvbærende kledning og lydisolasjon, og rommene er delt med selvbærende tørrbygde skillevegger.',
  'Bostäderna skiljs åt av en halvstens vägg av perforerat massivt tegel med dubbel självbärande beklädnad och ljudisolering, och rummen delas av självbärande torrbyggda mellanväggar.')
p('.qualitySpecs.groups[1].name', 'Roofs, terraces and insulation',
  'Cubiertas, terrazas y aislamiento', 'Toitures, terrasses et isolation', 'Dächer, Terrassen und Dämmung', 'Кровли, террасы и изоляция', 'الأسقف والتراسات والعزل', 'Daken, terrassen en isolatie',
  'Dachy, tarasy i izolacja', 'Tak, terrasser og isolasjon', 'Tak, terrasser och isolering')
p('.qualitySpecs.groups[1].items[0]', 'Waterproofed roofs and terraces',
  'Cubiertas y terrazas impermeabilizadas, cubiertas planas con grava donde no se transita, y pavimento cerámico y de gres porcelánico antideslizante en porches y terrazas.',
  'Toitures et terrasses étanchées, toitures plates en gravier là où l’on ne circule pas, et revêtement antidérapant en céramique et grès cérame sur les porches et les terrasses.',
  'Abgedichtete Dächer und Terrassen, Flachdächer mit Kies dort, wo niemand läuft, und rutschhemmender Keramik- und Feinsteinzeugbelag auf Veranden und Terrassen.',
  'Гидроизоляция кровель и террас, плоские кровли с гравием там, где не ходят, и нескользящее покрытие из керамики и керамогранита на крыльцах и террасах.',
  'أسقف وتراسات معزولة مائيًا، وأسقف مسطحة بالحصى حيث لا يُسار عليها، وأرضيات من السيراميك وحجر البورسلان المانعة للانزلاق في الشرفات والتراسات.',
  'Waterdichte daken en terrassen, platte daken met grind waar niemand loopt, en antislip keramische en porseleinen tegels op veranda’s en terrassen.',
  'Hydroizolowane dachy i tarasy, dachy płaskie ze żwirem tam, gdzie nikt nie chodzi, oraz antypoślizgowa okładzina ceramiczna i z gresu na werandach i tarasach.',
  'Tettede tak og terrasser, flate tak med grus der ingen går, og sklisikre keramiske fliser og porselensfliser på verandaer og terrasser.',
  'Tätade tak och terrasser, platta tak med grus där ingen går, och halkfri keramik och klinker på altaner och terrasser.')
p('.qualitySpecs.groups[1].items[1]', 'Thermal and acoustic insulation in the exterior walls',
  'Aislamiento térmico y acústico en los cerramientos exteriores y láminas anti-impacto entre plantas.',
  'Isolation thermique et acoustique des murs extérieurs et membranes anti-impact entre les étages.',
  'Wärme- und Schalldämmung der Außenwände und Trittschalldämmbahnen zwischen den Geschossen.',
  'Тепло- и звукоизоляция наружных стен и противоударные звукоизолирующие мембраны между этажами.',
  'عزل حراري وصوتي في الجدران الخارجية وألواح مضادة للصدمات بين الطوابق.',
  'Thermische en akoestische isolatie in de buitenmuren en contactgeluidsisolerende matten tussen de verdiepingen.',
  'Izolacja termiczna i akustyczna ścian zewnętrznych oraz maty przeciwuderzeniowe między kondygnacjami.',
  'Varme- og lydisolasjon i yttervegger og trinnlydsmembraner mellom etasjene.',
  'Värme- och ljudisolering i ytterväggarna och stegljudsisolering mellan våningarna.')
p('.qualitySpecs.groups[2].items[0]', 'Large-format rectified porcelain stoneware',
  'Gres porcelánico rectificado de gran formato con rodapié en las zonas de estar, y suelo vinílico flotante en la zona de dormitorios.',
  'Grès cérame rectifié grand format avec plinthe dans les pièces de vie, et sol vinyle flottant dans la zone des chambres.',
  'Großformatiger rektifizierter Feinsteinzeugbelag mit Sockelleiste in den Wohnbereichen und schwimmend verlegter Vinylboden im Schlafbereich.',
  'Крупноформатный ректифицированный керамогранит с плинтусом в жилых зонах и плавающее виниловое покрытие в зоне спален.',
  'بلاط بورسلان مصقول بحواف مستقيمة بحجم كبير مع وزرة في مناطق المعيشة، وأرضية فينيل عائمة في منطقة غرف النوم.',
  'Gerectificeerde porseleinen tegels in groot formaat met een plint in de woonruimten en een zwevende vinylvloer in het slaapgedeelte.',
  'Wielkoformatowy rektyfikowany gres z listwą przypodłogową w strefach dziennych oraz pływająca podłoga winylowa w strefie sypialnej.',
  'Store, rektifiserte porselensfliser med gulvlist i oppholdsarealene og flytende vinylgulv i soveromsdelen.',
  'Storformat slipad klinker med golvlist i vardagsytorna och flytande vinylgolv i sovdelen.')
p('.qualitySpecs.groups[2].items[1]', 'Suspended ceilings throughout',
  'Falsos techos en toda la vivienda, y baños y aseos alicatados.',
  'Faux plafonds dans tout le logement, et salles de bain et toilettes carrelées.',
  'Abgehängte Decken in der gesamten Wohnung sowie geflieste Bäder und Gäste-WCs.',
  'Подвесные потолки во всей квартире, ванные комнаты и санузлы отделаны плиткой.',
  'أسقف معلّقة في أنحاء المسكن، وحمامات ودورات مياه مكسوّة بالبلاط.',
  'Verlaagde plafonds in de hele woning en betegelde badkamers en toiletten.',
  'Sufity podwieszane w całym lokalu oraz łazienki i toalety wyłożone płytkami.',
  'Nedhengte tak i hele boligen, og flisbelagte bad og toaletter.',
  'Undertak i hela bostaden, och kaklade badrum och toaletter.')
p('.qualitySpecs.groups[3].items[0]', 'A security front door',
  'Puerta de entrada de seguridad con cerradura de tres puntos y bisagras antipalanca, puertas interiores blancas y armarios empotrados forrados en tablero melamínico, con balda, barra de colgar y cajones.',
  'Porte d’entrée de sécurité avec serrure à trois points et paumelles anti-dégondage, portes intérieures blanches et placards intégrés revêtus de panneaux mélaminés, avec tablette, barre de penderie et tiroirs.',
  'Sicherheits-Wohnungseingangstür mit Dreipunktschloss und aushebelsicheren Bändern, weiße Innentüren und Einbauschränke mit Melaminplatten ausgekleidet, mit Ablage, Kleiderstange und Schubladen.',
  'Входная дверь повышенной безопасности с трёхточечным замком и противосъёмными петлями, белые межкомнатные двери и встроенные шкафы с отделкой из меламиновой плиты, с полкой, штангой для одежды и ящиками.',
  'باب دخول أمان بقفل ثلاثي النقاط ومفصلات مقاومة للعتلة، وأبواب داخلية بيضاء، وخزائن مدمجة مبطّنة بألواح الميلامين مع رف وعمود تعليق وأدراج.',
  'Een veiligheidsvoordeur met driepuntssluiting en anti-inbraakscharnieren, witte binnendeuren en inbouwkasten bekleed met melamineplaat, met een legplank, een kledingstang en lades.',
  'Drzwi wejściowe zabezpieczające z zamkiem trzypunktowym i zawiasami zabezpieczonymi przed wyważeniem, białe drzwi wewnętrzne oraz szafy w zabudowie wyłożone płytą melaminową, z półką, drążkiem na ubrania i szufladami.',
  'Sikkerhetsinngangsdør med trepunktslås og brytesikre hengsler, hvite innerdører og innebygde garderobeskap kledd med melaminplater, med hylle, klesstang og skuffer.',
  'Säkerhetsytterdörr med trepunktslås och påbrytningsskyddade gångjärn, vita innerdörrar och inbyggda garderober klädda med melaminskivor, med hylla, klädstång och lådor.')
p('.qualitySpecs.groups[3].items[1]', 'Lacquered aluminium frames with a thermal break, in a colour',
  'Carpintería de aluminio lacado con rotura de puente térmico, en un color que fija el promotor, y doble acristalamiento termoacústico en todas las zonas de estar, con persianas automáticas de lamas de aluminio lacado en los dormitorios.',
  'Menuiseries en aluminium laqué à rupture de pont thermique, dans une couleur choisie par le promoteur, et double vitrage thermo-acoustique dans toutes les pièces de vie, avec des stores à lames en aluminium laqué automatiques dans les chambres.',
  'Lackierte Aluminiumrahmen mit thermischer Trennung in einer vom Bauträger festgelegten Farbe und thermoakustische Doppelverglasung in allen Wohnbereichen, mit automatischen Lamellenrollläden aus lackiertem Aluminium in den Schlafzimmern.',
  'Окрашенные алюминиевые рамы с терморазрывом в цвете, который определяет застройщик, и двойное термоакустическое остекление во всех жилых зонах, с автоматическими жалюзи из окрашенного алюминия в спальнях.',
  'إطارات من الألومنيوم المطلي بقاطع حراري بلون يحدده المطوّر، وزجاج مزدوج حراري صوتي في جميع مناطق المعيشة، مع ستائر آلية من شرائح الألومنيوم المطلي في غرف النوم.',
  'Gelakte aluminium kozijnen met thermische onderbreking, in een kleur die de ontwikkelaar bepaalt, en thermo-akoestische dubbele beglazing in alle woonruimten, met automatische lamellenrolluiken van gelakt aluminium in de slaapkamers.',
  'Lakierowane ramy aluminiowe z przekładką termiczną, w kolorze określonym przez dewelopera, i podwójne szyby termoakustyczne we wszystkich strefach dziennych, z automatycznymi żaluzjami z lakierowanego aluminium w sypialniach.',
  'Lakkerte aluminiumsrammer med termisk brudd, i en farge utbyggeren bestemmer, og termoakustisk dobbeltglass i alle oppholdsarealer, med automatiske lameller i lakkert aluminium i soverommene.',
  'Lackerade aluminiumkarmar med termisk brytning, i en kulör som exploatören bestämmer, och termoakustiskt dubbelglas i alla vardagsytor, med automatiska persienner av lackerat aluminium i sovrummen.')
p('.qualitySpecs.groups[4].items[0]', 'A fitted kitchen with high and low units',
  'Cocina amueblada con muebles altos y bajos, con frigorífico, lavavajillas, microondas, horno, placa de inducción, campana extractora, fregadero y lavadora.',
  'Cuisine aménagée avec meubles hauts et bas, équipée d’un réfrigérateur, d’un lave-vaisselle, d’un micro-ondes, d’un four, d’une plaque à induction, d’une hotte, d’un évier et d’un lave-linge.',
  'Einbauküche mit Hoch- und Unterschränken, ausgestattet mit Kühlschrank, Geschirrspüler, Mikrowelle, Backofen, Induktionskochfeld, Dunstabzug, Spüle und Waschmaschine.',
  'Кухня с мебелью, верхними и нижними шкафами, оснащённая холодильником, посудомоечной машиной, микроволновой печью, духовкой, индукционной панелью, вытяжкой, мойкой и стиральной машиной.',
  'مطبخ مجهّز بوحدات علوية وسفلية، مزوّد بثلاجة وغسالة صحون وميكروويف وفرن وموقد حثي وشفاط وحوض وغسالة ملابس.',
  'Een ingerichte keuken met hoge en lage kasten, uitgerust met een koelkast, een vaatwasser, een magnetron, een oven, een inductiekookplaat, een afzuigkap, een spoelbak en een wasmachine.',
  'Kuchnia w zabudowie z szafkami wiszącymi i stojącymi, wyposażona w lodówkę, zmywarkę, kuchenkę mikrofalową, piekarnik, płytę indukcyjną, okap, zlewozmywak i pralkę.',
  'Innredet kjøkken med over- og underskap, utstyrt med kjøleskap, oppvaskmaskin, mikrobølgeovn, ovn, induksjonstopp, kjøkkenvifte, vask og vaskemaskin.',
  'Inrett kök med över- och underskåp, utrustat med kylskåp, diskmaskin, mikrovågsugn, ugn, induktionshäll, köksfläkt, diskho och tvättmaskin.')
p('.qualitySpecs.groups[5].items[0]', 'Vitrified porcelain sanitary ware',
  'Aparatos sanitarios de porcelana vitrificada, grifería monomando negra y mamparas de ducha de cristal.',
  'Appareils sanitaires en porcelaine vitrifiée, mitigeurs noirs et parois de douche en verre.',
  'Sanitärkeramik aus Vitreous China, schwarze Einhandmischer und Duschwände aus Glas.',
  'Сантехника из глазурованного фарфора, чёрные однорычажные смесители и стеклянные душевые ограждения.',
  'أدوات صحية من البورسلان المزجّج، وخلاطات سوداء أحادية المقبض، وحواجز دش زجاجية.',
  'Sanitair van verglaasd porselein, zwarte eengreepskranen en glazen douchewanden.',
  'Ceramika sanitarna z porcelany witryfikowanej, czarne baterie jednouchwytowe i szklane ścianki prysznicowe.',
  'Sanitærutstyr i glasert porselen, svarte énhåndsblandebatterier og dusjvegger i glass.',
  'Sanitetsporslin av vitrifierat porslin, svarta enhandsblandare och duschväggar av glas.')
p('.qualitySpecs.groups[5].items[1]', 'Water and drainage connections',
  'Conexiones de agua y desagüe para lavadora y lavavajillas.',
  'Arrivées et évacuations d’eau pour un lave-linge et un lave-vaisselle.',
  'Wasser- und Abwasseranschlüsse für Waschmaschine und Geschirrspüler.',
  'Подключения воды и канализации для стиральной и посудомоечной машин.',
  'وصلات مياه وصرف لغسالة الملابس وغسالة الصحون.',
  'Water- en afvoeraansluitingen voor een wasmachine en een vaatwasser.',
  'Przyłącza wody i odpływu do pralki i zmywarki.',
  'Vann- og avløpstilkoblinger for vaskemaskin og oppvaskmaskin.',
  'Vatten- och avloppsanslutningar för tvättmaskin och diskmaskin.')
p('.qualitySpecs.groups[6].items[0]', 'Hot water from an aerothermal system',
  'Agua caliente mediante aerotermia, suelo radiante y aire acondicionado por conductos en los falsos techos del salón y los dormitorios, conectado a la aerotermia.',
  'Eau chaude par aérothermie, plancher chauffant et climatisation par gaines dans les faux plafonds du séjour et des chambres, reliée à l’aérothermie.',
  'Warmwasser über Aerothermie, Fußbodenheizung und Klimaanlage über Kanäle in den abgehängten Decken von Wohnzimmer und Schlafzimmern, angeschlossen an die Aerothermie.',
  'Горячая вода от аэротермии, тёплый пол и кондиционирование по воздуховодам в подвесных потолках гостиной и спален, подключённое к аэротермии.',
  'ماء ساخن من نظام الطاقة الهوائية الحرارية، وتدفئة أرضية، وتكييف عبر مجارٍ في الأسقف المعلّقة للصالة وغرف النوم، موصول بنظام الطاقة الهوائية الحرارية.',
  'Warm water via aerothermie, vloerverwarming en airconditioning via kanalen in de verlaagde plafonds van de woonkamer en de slaapkamers, aangesloten op de aerothermie.',
  'Ciepła woda z aerotermii, ogrzewanie podłogowe oraz klimatyzacja kanałowa w sufitach podwieszanych salonu i sypialni, podłączona do aerotermii.',
  'Varmtvann fra aerotermi, gulvvarme og klimaanlegg via kanaler i de nedhengte takene i stue og soverom, tilkoblet aerotermien.',
  'Varmvatten från aerotermi, golvvärme och luftkonditionering via kanaler i undertaken i vardagsrum och sovrum, kopplad till aerotermin.')
p('.qualitySpecs.groups[6].items[1]', 'Mechanical ventilation',
  'Ventilación mecánica en el interior de las viviendas.', 'Ventilation mécanique à l’intérieur des logements.', 'Mechanische Lüftung in den Wohnungen.',
  'Механическая вентиляция внутри квартир.', 'تهوية ميكانيكية داخل المساكن.', 'Mechanische ventilatie in de woningen.',
  'Wentylacja mechaniczna wewnątrz lokali.', 'Mekanisk ventilasjon inne i boligene.', 'Mekanisk ventilation inne i bostäderna.')
p('.qualitySpecs.groups[7].name', 'Electrical and shared areas',
  'Instalación eléctrica y zonas comunes', 'Électricité et parties communes', 'Elektrik und Gemeinschaftsflächen', 'Электрика и общие зоны', 'الكهرباء والمرافق المشتركة', 'Elektra en gemeenschappelijke ruimten',
  'Elektryka i części wspólne', 'Elektrisk og fellesarealer', 'El och gemensamma ytor')
p('.qualitySpecs.groups[7].items[0]', 'LED lighting designed by the architect',
  'Iluminación LED según el diseño del arquitecto, tomas de TV y teléfono en la cocina, el salón y los dormitorios, enchufes con puertos USB en las estancias principales y videoportero con pantalla.',
  'Éclairage LED conçu par l’architecte, prises TV et téléphone dans la cuisine, le séjour et les chambres, prises avec ports USB dans les pièces principales et interphone vidéo avec écran.',
  'LED-Beleuchtung nach dem Entwurf des Architekten, TV- und Telefonanschlüsse in Küche, Wohnzimmer und Schlafzimmern, Steckdosen mit USB-Anschlüssen in den Haupträumen und eine Videosprechanlage mit Bildschirm.',
  'Светодиодное освещение по проекту архитектора, телевизионные и телефонные розетки на кухне, в гостиной и спальнях, розетки с USB-портами в основных помещениях и видеодомофон с экраном.',
  'إضاءة LED بتصميم المهندس المعماري، ومآخذ تلفاز وهاتف في المطبخ والصالة وغرف النوم، ومقابس بمنافذ USB في الغرف الرئيسية، ونظام اتصال مرئي بشاشة.',
  'Ledverlichting naar ontwerp van de architect, tv- en telefoonaansluitingen in de keuken, de woonkamer en de slaapkamers, stopcontacten met usb-poorten in de hoofdvertrekken en een videofoon met scherm.',
  'Oświetlenie LED według projektu architekta, gniazda TV i telefoniczne w kuchni, salonie i sypialniach, gniazdka z portami USB w głównych pomieszczeniach oraz wideodomofon z ekranem.',
  'LED-belysning etter arkitektens design, TV- og telefonuttak på kjøkkenet, i stuen og i soverommene, stikkontakter med USB-porter i hovedrommene og en videoporttelefon med skjerm.',
  'LED-belysning enligt arkitektens design, tv- och telefonuttag i köket, vardagsrummet och sovrummen, eluttag med USB-portar i huvudrummen och en porttelefon med bildskärm.')
p('.qualitySpecs.groups[7].items[1]', 'An automatic garage door',
  'Puerta de garaje automática, amplios jardines con riego automático, y piscina comunitaria interior y exterior con gimnasio y sauna.',
  'Porte de garage automatique, vastes jardins paysagers avec arrosage automatique, et piscine commune intérieure et extérieure avec salle de sport et sauna.',
  'Automatisches Garagentor, große Gartenanlagen mit automatischer Bewässerung sowie ein Gemeinschaftspool innen und außen mit Fitnessraum und Sauna.',
  'Автоматические гаражные ворота, большие ландшафтные сады с автоматическим поливом и общий бассейн — крытый и наружный — с тренажёрным залом и сауной.',
  'باب مرآب آلي، وحدائق واسعة مُنسّقة بري آلي، ومسبح مشترك داخلي وخارجي مع صالة رياضية وساونا.',
  'Een automatische garagedeur, grote aangelegde tuinen met automatische bewatering, en een gemeenschappelijk binnen- en buitenzwembad met een fitnessruimte en een sauna.',
  'Automatyczna brama garażowa, duże ogrody z automatycznym nawadnianiem oraz wspólny basen wewnętrzny i zewnętrzny z siłownią i sauną.',
  'En automatisk garasjeport, store opparbeidede hager med automatisk vanning, og et felles innendørs og utendørs basseng med treningsrom og badstue.',
  'En automatisk garageport, stora anlagda trädgårdar med automatisk bevattning, och en gemensam inomhus- och utomhuspool med gym och bastu.')

# ---- residences, lifestyle, location ---------------------------------------------------------------
p('.residences.headlineHtml', 'Thirteen homes',
  'Trece viviendas, <em>cuatro tipos</em>', 'Treize logements, <em>quatre types</em>', 'Dreizehn Wohnungen, <em>vier Typen</em>',
  'Тринадцать квартир, <em>четыре типа</em>', 'ثلاثة عشر مسكنًا، <em>أربعة أنواع</em>', 'Dertien woningen, <em>vier soorten</em>',
  'Trzynaście lokali, <em>cztery rodzaje</em>', 'Tretten boliger, <em>fire typer</em>', 'Tretton bostäder, <em>fyra typer</em>')
p('.residences.copy', 'The thirteen listed homes',
  'Las trece viviendas listadas se dividen en cuatro grupos según la planta y el espacio exterior. La tabla de abajo recoge cada una con su precio.',
  'Les treize logements listés se répartissent en quatre groupes selon l’étage et l’espace extérieur. Le tableau ci-dessous présente chacun avec son prix.',
  'Die dreizehn aufgeführten Wohnungen lassen sich nach Geschoss und Außenbereich in vier Gruppen einteilen. Die Tabelle unten führt jede mit ihrem Preis auf.',
  'Тринадцать квартир из списка делятся на четыре группы по этажу и внешним пространствам. В таблице ниже каждая указана с ценой.',
  'تنقسم المساكن الثلاثة عشر المدرجة إلى أربع مجموعات بحسب الطابق والمساحة الخارجية. ويورد الجدول أدناه كل مسكن مع سعره.',
  'De dertien vermelde woningen vallen naar verdieping en buitenruimte uiteen in vier groepen. De tabel hieronder vermeldt elk met zijn prijs.',
  'Trzynaście wymienionych lokali dzieli się na cztery grupy według piętra i przestrzeni zewnętrznej. Tabela poniżej podaje każdy z nich wraz z ceną.',
  'De tretten oppførte boligene deler seg i fire grupper etter etasje og uteareal. Tabellen nedenfor viser hver av dem med pris.',
  'De tretton listade bostäderna delas in i fyra grupper efter våning och uteplats. Tabellen nedan visar var och en med sitt pris.')
p('.residences.items[0].name', 'One-bedroom homes with a garden',
  'Viviendas de un dormitorio con jardín', 'Logements de une chambre avec jardin', 'Wohnungen mit einem Schlafzimmer und Garten',
  'Квартиры с одной спальней и садом', 'مساكن بغرفة نوم مع حديقة', 'Woningen met een slaapkamer en een tuin',
  'Lokale z jedną sypialnią i ogrodem', 'Boliger med ett soverom og hage', 'Bostäder med ett sovrum och trädgård')
p('.residences.items[0].points[0]', 'Three one-bedroom homes on the ground floor',
  'Tres viviendas de un dormitorio en planta baja, 5.0.A y 5.0.C en el portal 5 y 6.0.A en el portal 6, cada una con un baño, una terraza cubierta, una terraza descubierta y un jardín.',
  'Trois logements de une chambre au rez-de-chaussée, 5.0.A et 5.0.C dans la cage 5 et 6.0.A dans la cage 6, chacun avec une salle de bain, une terrasse couverte, une terrasse découverte et un jardin.',
  'Drei Wohnungen mit einem Schlafzimmer im Erdgeschoss, 5.0.A und 5.0.C in Aufgang 5 und 6.0.A in Aufgang 6, jeweils mit einem Bad, einer überdachten Terrasse, einer offenen Terrasse und einem Garten.',
  'Три квартиры с одной спальней на первом этаже — 5.0.A и 5.0.C в подъезде 5 и 6.0.A в подъезде 6, у каждой одна ванная комната, крытая терраса, открытая терраса и сад.',
  'ثلاثة مساكن بغرفة نوم في الطابق الأرضي، 5.0.A و5.0.C في المدخل 5 و6.0.A في المدخل 6، لكل منها حمام واحد وتراس مغطى وتراس مكشوف وحديقة.',
  'Drie woningen met een slaapkamer op de begane grond, 5.0.A en 5.0.C in portiek 5 en 6.0.A in portiek 6, elk met een badkamer, een overdekt terras, een open terras en een tuin.',
  'Trzy lokale z jedną sypialnią na parterze, 5.0.A i 5.0.C w klatce 5 oraz 6.0.A w klatce 6, każdy z jedną łazienką, tarasem zadaszonym, tarasem odkrytym i ogrodem.',
  'Tre boliger med ett soverom i første etasje, 5.0.A og 5.0.C i oppgang 5 og 6.0.A i oppgang 6, hver med ett bad, en overbygd terrasse, en åpen terrasse og en hage.',
  'Tre bostäder med ett sovrum på bottenvåningen, 5.0.A och 5.0.C i uppgång 5 och 6.0.A i uppgång 6, var och en med ett badrum, en övertäckt terrass, en öppen terrass och en trädgård.')
p('.residences.items[0].points[1]', 'Interior areas of 42.45',
  'Superficies interiores de {N42.45} a {N48.92} {U}, terrazas de {N22.23} a {N25.45} {U} y jardines de {N29.17} a {N33.26} {U}.',
  'Surfaces intérieures de {N42.45} à {N48.92} {U}, terrasses de {N22.23} à {N25.45} {U} et jardins de {N29.17} à {N33.26} {U}.',
  'Innenflächen von {N42.45} bis {N48.92} {U}, Terrassen von {N22.23} bis {N25.45} {U} und Gärten von {N29.17} bis {N33.26} {U}.',
  'Внутренняя площадь от {N42.45} до {N48.92} {U}, террасы от {N22.23} до {N25.45} {U} и сады от {N29.17} до {N33.26} {U}.',
  'مساحات داخلية من {N42.45} إلى {N48.92} {U}، وتراسات من {N22.23} إلى {N25.45} {U}، وحدائق من {N29.17} إلى {N33.26} {U}.',
  'Binnenoppervlakten van {N42.45} tot {N48.92} {U}, terrassen van {N22.23} tot {N25.45} {U} en tuinen van {N29.17} tot {N33.26} {U}.',
  'Powierzchnie wewnętrzne od {N42.45} do {N48.92} {U}, tarasy od {N22.23} do {N25.45} {U} i ogrody od {N29.17} do {N33.26} {U}.',
  'Innvendige arealer fra {N42.45} til {N48.92} {U}, terrasser fra {N22.23} til {N25.45} {U} og hager fra {N29.17} til {N33.26} {U}.',
  'Invändiga ytor från {N42.45} till {N48.92} {U}, terrasser från {N22.23} till {N25.45} {U} och trädgårdar från {N29.17} till {N33.26} {U}.')
p('.residences.items[0].points[2]', 'The plans draw a storage room beside each home',
  'Los planos dibujan un trastero junto a cada vivienda, de {N48.62}, {N39.73} y {N40.09} {U} por ese orden. Los precios son {E705000}, {E705000} y {E715000}.',
  'Les plans dessinent une cave à côté de chaque logement, de {N48.62}, {N39.73} et {N40.09} {U} dans cet ordre. Les prix sont de {E705000}, {E705000} et {E715000}.',
  'Die Pläne zeigen neben jeder Wohnung einen Abstellraum von {N48.62}, {N39.73} und {N40.09} {U} in dieser Reihenfolge. Die Preise betragen {E705000}, {E705000} und {E715000}.',
  'На планах рядом с каждой квартирой нарисована кладовая площадью {N48.62}, {N39.73} и {N40.09} {U} соответственно. Цены — {E705000}, {E705000} и {E715000}.',
  'تُظهر المخططات غرفة تخزين بجانب كل مسكن، بمساحة {N48.62} و{N39.73} و{N40.09} {U} على التوالي. والأسعار {E705000} و{E705000} و{E715000}.',
  'De plattegronden tonen naast elke woning een berging van {N48.62}, {N39.73} en {N40.09} {U}, in die volgorde. De prijzen zijn {E705000}, {E705000} en {E715000}.',
  'Na rzutach obok każdego lokalu narysowano komórkę lokatorską o powierzchni {N48.62}, {N39.73} i {N40.09} {U}, w tej kolejności. Ceny wynoszą {E705000}, {E705000} i {E715000}.',
  'Plantegningene viser en bod ved siden av hver bolig, på {N48.62}, {N39.73} og {N40.09} {U} i den rekkefølgen. Prisene er {E705000}, {E705000} og {E715000}.',
  'Planritningarna visar ett förråd intill varje bostad, på {N48.62}, {N39.73} och {N40.09} {U} i den ordningen. Priserna är {E705000}, {E705000} och {E715000}.')
p('.residences.items[1].name', 'A two-bedroom home with a garden',
  'Una vivienda de dos dormitorios con jardín', 'Un logement de deux chambres avec jardin', 'Eine Wohnung mit zwei Schlafzimmern und Garten',
  'Квартира с двумя спальнями и садом', 'مسكن بغرفتي نوم مع حديقة', 'Een woning met twee slaapkamers en een tuin',
  'Lokal z dwiema sypialniami i ogrodem', 'En bolig med to soverom og hage', 'En bostad med två sovrum och trädgård')
p('.residences.items[1].points[0]', 'Home 5.0.B, on the ground floor',
  'La vivienda 5.0.B, en la planta baja del portal 5, tiene dos dormitorios, dos baños, {N67.20} {U} interiores, terrazas de {N35.17} {U} y un jardín de {N45.63} {U}.',
  'Le logement 5.0.B, au rez-de-chaussée de la cage 5, comprend deux chambres, deux salles de bain, {N67.20} {U} intérieurs, des terrasses de {N35.17} {U} et un jardin de {N45.63} {U}.',
  'Die Wohnung 5.0.B im Erdgeschoss von Aufgang 5 hat zwei Schlafzimmer, zwei Bäder, {N67.20} {U} Innenfläche, Terrassen von {N35.17} {U} und einen Garten von {N45.63} {U}.',
  'Квартира 5.0.B на первом этаже подъезда 5: две спальни, две ванные комнаты, {N67.20} {U} внутренней площади, террасы {N35.17} {U} и сад {N45.63} {U}.',
  'المسكن 5.0.B في الطابق الأرضي من المدخل 5 يضم غرفتي نوم وحمامين و{N67.20} {U} مساحة داخلية وتراسات بمساحة {N35.17} {U} وحديقة بمساحة {N45.63} {U}.',
  'Woning 5.0.B, op de begane grond van portiek 5, heeft twee slaapkamers, twee badkamers, {N67.20} {U} binnenoppervlak, terrassen van {N35.17} {U} en een tuin van {N45.63} {U}.',
  'Lokal 5.0.B, na parterze w klatce 5, ma dwie sypialnie, dwie łazienki, {N67.20} {U} powierzchni wewnętrznej, tarasy o powierzchni {N35.17} {U} i ogród o powierzchni {N45.63} {U}.',
  'Bolig 5.0.B, i første etasje i oppgang 5, har to soverom, to bad, {N67.20} {U} innvendig areal, terrasser på {N35.17} {U} og en hage på {N45.63} {U}.',
  'Bostad 5.0.B, på bottenvåningen i uppgång 5, har två sovrum, två badrum, {N67.20} {U} invändig yta, terrasser på {N35.17} {U} och en trädgård på {N45.63} {U}.')
p('.residences.items[1].points[1]', 'The plan draws a storage room of 28.43',
  'El plano dibuja un trastero de {N28.43} {U} junto a la vivienda. El precio es {E805000}.',
  'Le plan dessine une cave de {N28.43} {U} à côté du logement. Le prix est de {E805000}.',
  'Der Plan zeigt neben der Wohnung einen Abstellraum von {N28.43} {U}. Der Preis beträgt {E805000}.',
  'На плане рядом с квартирой нарисована кладовая площадью {N28.43} {U}. Цена — {E805000}.',
  'يُظهر المخطط غرفة تخزين بمساحة {N28.43} {U} بجانب المسكن. والسعر {E805000}.',
  'De plattegrond toont naast de woning een berging van {N28.43} {U}. De prijs is {E805000}.',
  'Na rzucie obok lokalu narysowano komórkę lokatorską o powierzchni {N28.43} {U}. Cena wynosi {E805000}.',
  'Plantegningen viser en bod på {N28.43} {U} ved siden av boligen. Prisen er {E805000}.',
  'Planritningen visar ett förråd på {N28.43} {U} intill bostaden. Priset är {E805000}.')
p('.residences.items[2].name', 'Three-bedroom homes on the first floor',
  'Viviendas de tres dormitorios en la primera planta', 'Logements de trois chambres au premier étage', 'Wohnungen mit drei Schlafzimmern im ersten Obergeschoss',
  'Квартиры с тремя спальнями на втором этаже', 'مساكن بثلاث غرف نوم في الطابق الأول', 'Woningen met drie slaapkamers op de eerste verdieping',
  'Lokale z trzema sypialniami na pierwszym piętrze', 'Boliger med tre soverom i andre etasje', 'Bostäder med tre sovrum på första våningen')
p('.residences.items[2].points[0]', 'Homes 5.1.B in portal 5',
  'Las viviendas 5.1.B, en el portal 5, y 6.1.A, en el portal 6, tienen tres dormitorios, dos baños y {N97.23} y {N97.28} {U} interiores.',
  'Les logements 5.1.B, dans la cage 5, et 6.1.A, dans la cage 6, comptent trois chambres, deux salles de bain et {N97.23} et {N97.28} {U} intérieurs.',
  'Die Wohnungen 5.1.B in Aufgang 5 und 6.1.A in Aufgang 6 haben drei Schlafzimmer, zwei Bäder und {N97.23} und {N97.28} {U} Innenfläche.',
  'Квартиры 5.1.B в подъезде 5 и 6.1.A в подъезде 6: три спальни, две ванные комнаты и {N97.23} и {N97.28} {U} внутренней площади.',
  'المسكنان 5.1.B في المدخل 5 و6.1.A في المدخل 6 يضمان ثلاث غرف نوم وحمامين و{N97.23} و{N97.28} {U} مساحة داخلية.',
  'De woningen 5.1.B in portiek 5 en 6.1.A in portiek 6 hebben drie slaapkamers, twee badkamers en {N97.23} en {N97.28} {U} binnenoppervlak.',
  'Lokale 5.1.B w klatce 5 i 6.1.A w klatce 6 mają trzy sypialnie, dwie łazienki oraz {N97.23} i {N97.28} {U} powierzchni wewnętrznej.',
  'Boligene 5.1.B i oppgang 5 og 6.1.A i oppgang 6 har tre soverom, to bad og {N97.23} og {N97.28} {U} innvendig areal.',
  'Bostäderna 5.1.B i uppgång 5 och 6.1.A i uppgång 6 har tre sovrum, två badrum och {N97.23} och {N97.28} {U} invändig yta.')
p('.residences.items[2].points[1]', 'Each has a terrace of 66.67',
  'Cada una tiene en el plano una terraza de {N66.67} {U}, que incluye un patio de {N7.34} {U}, con una parte cubierta de {N25.99} {U}. Ambas cuestan {E1090000}.',
  'Chacun a sur le plan une terrasse de {N66.67} {U}, qui comprend un patio de {N7.34} {U}, dont une partie couverte de {N25.99} {U}. Les deux sont au prix de {E1090000}.',
  'Jede hat laut Plan eine Terrasse von {N66.67} {U}, die einen Patio von {N7.34} {U} einschließt, mit einem überdachten Teil von {N25.99} {U}. Beide kosten {E1090000}.',
  'У каждой на плане терраса {N66.67} {U}, включающая патио {N7.34} {U}, с крытой частью {N25.99} {U}. Обе стоят {E1090000}.',
  'لكل منهما على المخطط تراس بمساحة {N66.67} {U} يشمل فناءً بمساحة {N7.34} {U}، مع جزء مغطى بمساحة {N25.99} {U}. وسعر كل منهما {E1090000}.',
  'Elk heeft op de plattegrond een terras van {N66.67} {U}, dat een patio van {N7.34} {U} omvat, met een overdekt deel van {N25.99} {U}. Beide kosten {E1090000}.',
  'Każdy ma na rzucie taras o powierzchni {N66.67} {U}, który obejmuje patio o powierzchni {N7.34} {U}, z częścią zadaszoną o powierzchni {N25.99} {U}. Oba kosztują {E1090000}.',
  'Hver av dem har en terrasse på {N66.67} {U} på plantegningen, som omfatter en patio på {N7.34} {U}, med en overbygd del på {N25.99} {U}. Begge koster {E1090000}.',
  'Var och en har en terrass på {N66.67} {U} enligt planritningen, som inkluderar en patio på {N7.34} {U}, med en övertäckt del på {N25.99} {U}. Båda kostar {E1090000}.')
p('.residences.items[3].name', 'Third-floor homes with a solarium',
  'Viviendas en la tercera planta con solárium', 'Logements au troisième étage avec solarium', 'Wohnungen im dritten Obergeschoss mit Solarium',
  'Квартиры на четвёртом этаже с солярием', 'مساكن في الطابق الثالث مع سولاريوم', 'Woningen op de derde verdieping met een solarium',
  'Lokale na trzecim piętrze z solarium', 'Boliger i fjerde etasje med solterrasse', 'Bostäder på tredje våningen med solterrass')
p('.residences.items[3].points[0]', 'Seven homes on the third floor',
  'Siete viviendas en la tercera planta, cada una con un solárium en su propio nivel, al que se accede por la escalera que muestra el plano: 2.3.B en el portal 2, 3.3.A y 3.3.B en el portal 3, 4.3.A y 4.3.B en el portal 4, y 5.3.A y 5.3.B en el portal 5. Dos tienen dos dormitorios, 2.3.B y 3.3.A, y cinco tienen tres, todas con dos baños.',
  'Sept logements au troisième étage, chacun avec un solarium sur son propre niveau, auquel on accède par l’escalier figurant sur le plan : 2.3.B dans la cage 2, 3.3.A et 3.3.B dans la cage 3, 4.3.A et 4.3.B dans la cage 4, et 5.3.A et 5.3.B dans la cage 5. Deux ont deux chambres, 2.3.B et 3.3.A, et cinq en ont trois, tous avec deux salles de bain.',
  'Sieben Wohnungen im dritten Obergeschoss, jede mit einem Solarium auf einer eigenen Ebene, das über die im Plan gezeigte Treppe erreichbar ist: 2.3.B in Aufgang 2, 3.3.A und 3.3.B in Aufgang 3, 4.3.A und 4.3.B in Aufgang 4 sowie 5.3.A und 5.3.B in Aufgang 5. Zwei haben zwei Schlafzimmer, 2.3.B und 3.3.A, und fünf haben drei, alle mit zwei Bädern.',
  'Семь квартир на четвёртом этаже, у каждой — солярий на отдельном уровне, на который ведёт лестница, показанная на плане: 2.3.B в подъезде 2, 3.3.A и 3.3.B в подъезде 3, 4.3.A и 4.3.B в подъезде 4, 5.3.A и 5.3.B в подъезде 5. У двух из них по две спальни — 2.3.B и 3.3.A, у пяти — по три, и у всех по две ванные комнаты.',
  'سبعة مساكن في الطابق الثالث، لكل منها سولاريوم في مستوى خاص به، يُصعد إليه بالدرج المبيّن في المخطط: 2.3.B في المدخل 2، و3.3.A و3.3.B في المدخل 3، و4.3.A و4.3.B في المدخل 4، و5.3.A و5.3.B في المدخل 5. اثنان منها بغرفتي نوم، 2.3.B و3.3.A، وخمسة بثلاث غرف نوم، وجميعها بحمامين.',
  'Zeven woningen op de derde verdieping, elk met een solarium op een eigen niveau, bereikbaar via de trap op de plattegrond: 2.3.B in portiek 2, 3.3.A en 3.3.B in portiek 3, 4.3.A en 4.3.B in portiek 4, en 5.3.A en 5.3.B in portiek 5. Twee hebben twee slaapkamers, 2.3.B en 3.3.A, en vijf hebben er drie, allemaal met twee badkamers.',
  'Siedem lokali na trzecim piętrze, każdy z solarium na osobnym poziomie, do którego prowadzą schody widoczne na rzucie: 2.3.B w klatce 2, 3.3.A i 3.3.B w klatce 3, 4.3.A i 4.3.B w klatce 4 oraz 5.3.A i 5.3.B w klatce 5. Dwa mają dwie sypialnie, 2.3.B i 3.3.A, a pięć ma trzy, wszystkie z dwiema łazienkami.',
  'Syv boliger i fjerde etasje, hver med en solterrasse på et eget nivå, nådd via trappen som vises på plantegningen: 2.3.B i oppgang 2, 3.3.A og 3.3.B i oppgang 3, 4.3.A og 4.3.B i oppgang 4, og 5.3.A og 5.3.B i oppgang 5. To har to soverom, 2.3.B og 3.3.A, og fem har tre, alle med to bad.',
  'Sju bostäder på tredje våningen, var och en med en solterrass på en egen nivå, som nås via trappan på planritningen: 2.3.B i uppgång 2, 3.3.A och 3.3.B i uppgång 3, 4.3.A och 4.3.B i uppgång 4, och 5.3.A och 5.3.B i uppgång 5. Två har två sovrum, 2.3.B och 3.3.A, och fem har tre, alla med två badrum.')
p('.residences.items[3].points[1]', 'Interior areas of 82.51',
  'Superficies interiores de {N82.51} a {N100.35} {U}, terrazas de {N27.87} a {N37.70} {U} y soláriums de {N77.41} a {N104.23} {U}. El plano de todas ellas dibuja una pequeña piscina en el solárium.',
  'Surfaces intérieures de {N82.51} à {N100.35} {U}, terrasses de {N27.87} à {N37.70} {U} et solariums de {N77.41} à {N104.23} {U}. Le plan de chacun dessine un petit bassin sur le solarium.',
  'Innenflächen von {N82.51} bis {N100.35} {U}, Terrassen von {N27.87} bis {N37.70} {U} und Solarien von {N77.41} bis {N104.23} {U}. Der Plan jeder einzelnen zeigt einen kleinen Pool auf dem Solarium.',
  'Внутренняя площадь от {N82.51} до {N100.35} {U}, террасы от {N27.87} до {N37.70} {U} и солярии от {N77.41} до {N104.23} {U}. На плане каждой из них на солярии нарисован небольшой бассейн.',
  'مساحات داخلية من {N82.51} إلى {N100.35} {U}، وتراسات من {N27.87} إلى {N37.70} {U}، وسولاريومات من {N77.41} إلى {N104.23} {U}. ويُظهر مخطط كل منها مسبحًا صغيرًا على السولاريوم.',
  'Binnenoppervlakten van {N82.51} tot {N100.35} {U}, terrassen van {N27.87} tot {N37.70} {U} en solariums van {N77.41} tot {N104.23} {U}. Op de plattegrond van elk ervan staat een klein zwembad op het solarium getekend.',
  'Powierzchnie wewnętrzne od {N82.51} do {N100.35} {U}, tarasy od {N27.87} do {N37.70} {U} i solaria od {N77.41} do {N104.23} {U}. Na rzucie każdego z nich narysowano na solarium niewielki basen.',
  'Innvendige arealer fra {N82.51} til {N100.35} {U}, terrasser fra {N27.87} til {N37.70} {U} og solterrasser fra {N77.41} til {N104.23} {U}. Plantegningen av hver enkelt viser et lite basseng på solterrassen.',
  'Invändiga ytor från {N82.51} till {N100.35} {U}, terrasser från {N27.87} till {N37.70} {U} och solterrasser från {N77.41} till {N104.23} {U}. Planritningen för var och en visar en liten pool på solterrassen.')
p('.residences.items[3].points[2]', 'The prices run from',
  'Los precios van de {E1095000} a {E1570000}.', 'Les prix vont de {E1095000} à {E1570000}.', 'Die Preise reichen von {E1095000} bis {E1570000}.',
  'Цены — от {E1095000} до {E1570000}.', 'تتراوح الأسعار بين {E1095000} و{E1570000}.', 'De prijzen lopen van {E1095000} tot {E1570000}.',
  'Ceny wahają się od {E1095000} do {E1570000}.', 'Prisene varierer fra {E1095000} til {E1570000}.', 'Priserna varierar från {E1095000} till {E1570000}.')

p('.lifestyle.headlineHtml', 'Pools,',
  'Piscinas, <em>gimnasio</em> y sauna', 'Des piscines, <em>une salle de sport</em> et un sauna', 'Pools, <em>Fitnessraum</em> und Sauna',
  'Бассейны, <em>тренажёрный зал</em> и сауна', 'مسابح، <em>وصالة رياضية</em> وساونا', 'Zwembaden, <em>een fitnessruimte</em> en een sauna',
  'Baseny, <em>siłownia</em> i sauna', 'Basseng, <em>treningsrom</em> og badstue', 'Pooler, <em>gym</em> och bastu')
p('.lifestyle.copy', 'The shared areas are planned around outdoor',
  'Las zonas comunes se organizan en torno a piscinas exteriores e interior, un gimnasio, una sauna y zonas chill-out, con jardines paisajísticos.',
  'Les parties communes s’organisent autour de piscines extérieures et intérieure, d’une salle de sport, d’un sauna et d’espaces chill-out, avec des jardins paysagers.',
  'Die Gemeinschaftsbereiche sind um Außen- und Innenpools, einen Fitnessraum, eine Sauna und Chill-out-Bereiche angelegt, mit Gartenanlagen.',
  'Общие зоны построены вокруг наружных и крытого бассейнов, тренажёрного зала, сауны и зон отдыха chill-out, с ландшафтными садами.',
  'تتمحور المرافق المشتركة حول مسابح خارجية ومسبح داخلي وصالة رياضية وساونا ومناطق استرخاء، مع حدائق مُنسّقة.',
  'De gemeenschappelijke ruimten zijn opgezet rond buitenzwembaden en een binnenzwembad, een fitnessruimte, een sauna en chill-outzones, met aangelegde tuinen.',
  'Części wspólne zaplanowano wokół basenów zewnętrznych i wewnętrznego, siłowni, sauny i stref chill-out, z ogrodami.',
  'Fellesarealene er planlagt rundt utendørs og innendørs basseng, treningsrom, badstue og chill-out-områder, med opparbeidede hager.',
  'De gemensamma ytorna är planerade kring pooler utomhus och inomhus, ett gym, en bastu och chill out-ytor, med anlagda trädgårdar.')
p('.lifestyle.panels[0][1]', 'Outdoor pools of turquoise water',
  'Piscinas exteriores de agua turquesa con tumbonas a su lado, y una piscina interior, tal como las describen el dosier y la memoria de calidades. Los documentos no dan medidas.',
  'Des piscines extérieures à l’eau turquoise avec des transats à côté, et une piscine intérieure, telles que les décrivent le dossier et le descriptif technique. Les documents n’en donnent pas les dimensions.',
  'Außenpools mit türkisfarbenem Wasser und Sonnenliegen daneben sowie ein Innenpool, wie sie die Broschüre und die Baubeschreibung beschreiben. Die Unterlagen nennen keine Größen.',
  'Наружные бассейны с бирюзовой водой и шезлонгами рядом и крытый бассейн, как их описывают буклет и спецификация. Размеры в документах не указаны.',
  'مسابح خارجية بمياه فيروزية مع مقاعد استلقاء بجانبها، ومسبح داخلي، كما يصفها الكتيّب ومواصفات البناء. ولا تذكر الوثائق مساحاتها.',
  'Buitenzwembaden met turquoise water en ligbedden ernaast, en een binnenzwembad, zoals de brochure en het lastenboek ze beschrijven. De documenten geven geen afmetingen.',
  'Baseny zewnętrzne z turkusową wodą i leżakami obok oraz basen wewnętrzny, tak jak opisują je broszura i specyfikacja techniczna. Dokumenty nie podają wymiarów.',
  'Utendørs basseng med turkist vann og solsenger ved siden av, og et innendørs basseng, slik brosjyren og beskrivelsen omtaler dem. Dokumentene oppgir ingen størrelser.',
  'Utomhuspooler med turkost vatten och solstolar bredvid, och en inomhuspool, så som broschyren och byggbeskrivningen beskriver dem. Dokumenten anger inga storlekar.')
p('.lifestyle.panels[1][0]', 'The gym and the sauna',
  'El gimnasio y la sauna', 'La salle de sport et le sauna', 'Der Fitnessraum und die Sauna', 'Тренажёрный зал и сауна', 'الصالة الرياضية والساونا',
  'De fitnessruimte en de sauna', 'Siłownia i sauna', 'Treningsrommet og badstuen', 'Gymmet och bastun')
p('.lifestyle.panels[1][1]', 'A fully equipped gym and a sauna',
  'Un gimnasio totalmente equipado y una sauna, tal como los recogen el dosier y la memoria de calidades. Los documentos no dan medidas ni equipamiento.',
  'Une salle de sport entièrement équipée et un sauna, tels que les mentionnent le dossier et le descriptif technique. Les documents n’en donnent ni les dimensions ni l’équipement.',
  'Ein voll ausgestatteter Fitnessraum und eine Sauna, wie sie die Broschüre und die Baubeschreibung auflisten. Die Unterlagen nennen weder Größen noch Ausstattung.',
  'Полностью оборудованный тренажёрный зал и сауна, как их указывают буклет и спецификация. Размеры и оборудование в документах не указаны.',
  'صالة رياضية مجهّزة بالكامل وساونا، كما يوردها الكتيّب ومواصفات البناء. ولا تذكر الوثائق المساحات ولا التجهيزات.',
  'Een volledig uitgeruste fitnessruimte en een sauna, zoals de brochure en het lastenboek ze vermelden. De documenten geven geen afmetingen of uitrusting.',
  'W pełni wyposażona siłownia i sauna, tak jak wymieniają je broszura i specyfikacja techniczna. Dokumenty nie podają wymiarów ani wyposażenia.',
  'Et fullt utstyrt treningsrom og en badstue, slik brosjyren og beskrivelsen oppgir dem. Dokumentene oppgir ingen størrelser eller utstyr.',
  'Ett fullt utrustat gym och en bastu, så som broschyren och byggbeskrivningen anger dem. Dokumenten anger varken storlekar eller utrustning.')
p('.lifestyle.panels[2][0]', 'Chill-out areas and gardens',
  'Zonas chill-out y jardines', 'Espaces chill-out et jardins', 'Chill-out-Bereiche und Gärten', 'Зоны chill-out и сады', 'مناطق الاسترخاء والحدائق',
  'Chill-outzones en tuinen', 'Strefy chill-out i ogrody', 'Chill-out-områder og hager', 'Chill out-ytor och trädgårdar')
p('.lifestyle.panels[2][1]', 'Chill-out areas beside the pools',
  'Zonas chill-out junto a las piscinas y amplios jardines paisajísticos con riego automático.',
  'Des espaces chill-out près des piscines et de vastes jardins paysagers avec arrosage automatique.',
  'Chill-out-Bereiche neben den Pools und große Gartenanlagen mit automatischer Bewässerung.',
  'Зоны chill-out рядом с бассейнами и большие ландшафтные сады с автоматическим поливом.',
  'مناطق استرخاء بجانب المسابح وحدائق واسعة مُنسّقة بري آلي.',
  'Chill-outzones naast de zwembaden en grote aangelegde tuinen met automatische bewatering.',
  'Strefy chill-out obok basenów i duże ogrody z automatycznym nawadnianiem.',
  'Chill-out-områder ved bassengene og store opparbeidede hager med automatisk vanning.',
  'Chill out-ytor vid poolerna och stora anlagda trädgårdar med automatisk bevattning.')
p('.lifestyle.panels[3][0]', 'The neighbourhood tennis club',
  'El club de tenis del vecindario', 'Le club de tennis du quartier', 'Der Tennisclub der Nachbarschaft', 'Теннисный клуб по соседству', 'نادي التنس في الحي',
  'De tennisclub in de buurt', 'Klub tenisowy w sąsiedztwie', 'Tennisklubben i nabolaget', 'Tennisklubben i området')
p('.lifestyle.panels[3][1]', 'The dossier lists the use of the neighbourhood tennis club',
  'El dosier incluye entre las características el uso del club de tenis del vecindario. No dice qué incluye ese uso ni si tiene coste adicional.',
  'Le dossier cite l’usage du club de tennis du quartier parmi les atouts. Il ne précise pas ce que cet usage comprend ni s’il est payant en supplément.',
  'Die Broschüre führt die Nutzung des Tennisclubs der Nachbarschaft unter den Merkmalen auf. Sie sagt nicht, was die Nutzung umfasst oder ob sie extra kostet.',
  'В буклете среди особенностей указано пользование теннисным клубом по соседству. Не сказано, что входит в это пользование и оплачивается ли оно дополнительно.',
  'يذكر الكتيّب ضمن المزايا استخدام نادي التنس في الحي. ولا يوضح ما يشمله هذا الاستخدام ولا ما إذا كان بتكلفة إضافية.',
  'De brochure noemt het gebruik van de tennisclub in de buurt onder de kenmerken. Ze zegt niet wat dat gebruik inhoudt en of het extra kost.',
  'Broszura wymienia korzystanie z klubu tenisowego w sąsiedztwie wśród cech inwestycji. Nie podaje, co obejmuje to korzystanie ani czy wiąże się z dodatkową opłatą.',
  'Brosjyren oppgir bruk av tennisklubben i nabolaget blant egenskapene. Den sier ikke hva bruken omfatter eller om den koster ekstra.',
  'Broschyren anger användning av tennisklubben i området bland egenskaperna. Den säger inte vad användningen omfattar eller om den kostar extra.')

p('.location.copy', 'The infosheet links a map location',
  'La ficha informativa enlaza una ubicación en el mapa en La Cala de Mijas, y el mapa del dosier sitúa la promoción entre Cabopino y Cala de Mijas, junto a la A-7. Ese mapa marca el centro de Fuengirola a 10, el centro de Marbella a 20 y el aeropuerto de Málaga a 25, que interpretamos como minutos, y nombra los campos de golf de Cabopino, La Siesta, Miraflores, Calanova, La Noria y Chaparral. Los tiempos junto al mapa son tiempos por carretera medidos desde esa ubicación, no tomados de los documentos del promotor.',
  'La fiche d’information renvoie à un emplacement sur la carte à La Cala de Mijas, et la carte du dossier situe la promotion entre Cabopino et Cala de Mijas, le long de l’A-7. Cette carte indique le centre de Fuengirola à 10, le centre de Marbella à 20 et l’aéroport de Málaga à 25, que nous lisons comme des minutes, et nomme les golfs de Cabopino, La Siesta, Miraflores, Calanova, La Noria et Chaparral. Les temps affichés à côté de la carte sont des temps de trajet routier mesurés depuis cet emplacement, et non repris des documents du promoteur.',
  'Das Infoblatt verlinkt einen Kartenstandort in La Cala de Mijas, und die Karte der Broschüre verortet die Anlage zwischen Cabopino und Cala de Mijas, neben der A-7. Diese Karte gibt das Zentrum von Fuengirola mit 10, das Zentrum von Marbella mit 20 und den Flughafen Málaga mit 25 an, was wir als Minuten lesen, und nennt die Golfplätze von Cabopino, La Siesta, Miraflores, Calanova, La Noria und Chaparral. Die Zeiten neben der Karte sind Fahrzeiten auf der Straße, gemessen von diesem Standort, und nicht aus den Unterlagen des Bauträgers übernommen.',
  'В информационном листе есть ссылка на точку на карте в Ла-Кала-де-Михас, а на карте в буклете комплекс расположен между Кабопино и Ла-Кала-де-Михас, рядом с автострадой A-7. На этой карте центр Фуэнхиролы отмечен как 10, центр Марбельи — как 20, а аэропорт Малаги — как 25, что мы читаем как минуты, и подписаны гольф-поля Cabopino, La Siesta, Miraflores, Calanova, La Noria и Chaparral. Время рядом с картой — это время в пути по дороге, измеренное от этой точки, а не взятое из документов застройщика.',
  'تربط ورقة المعلومات بموقع على الخريطة في لا كالا دي ميخاس، وتضع خريطة الكتيّب المشروع بين كابوبينو ولا كالا دي ميخاس، بجانب الطريق A-7. وتضع هذه الخريطة وسط فوينخيرولا عند 10 ووسط ماربيا عند 20 ومطار مالقة عند 25، ونقرأ ذلك على أنه دقائق، وتذكر ملاعب الغولف Cabopino وLa Siesta وMiraflores وCalanova وLa Noria وChaparral. والأوقات المعروضة بجانب الخريطة هي أوقات القيادة على الطريق المقاسة من هذا الموقع، وليست مأخوذة من وثائق المطوّر.',
  'Het infoblad verwijst naar een kaartlocatie in La Cala de Mijas, en de kaart in de brochure plaatst het project tussen Cabopino en Cala de Mijas, naast de A-7. Die kaart geeft het centrum van Fuengirola aan op 10, het centrum van Marbella op 20 en de luchthaven van Málaga op 25, wat wij als minuten lezen, en noemt de golfbanen van Cabopino, La Siesta, Miraflores, Calanova, La Noria en Chaparral. De tijden naast de kaart zijn reistijden over de weg, gemeten vanaf die kaartlocatie, en niet overgenomen uit de documenten van de ontwikkelaar.',
  'Karta informacyjna odsyła do lokalizacji na mapie w La Cala de Mijas, a mapa w broszurze umieszcza inwestycję między Cabopino a Cala de Mijas, przy A-7. Ta mapa oznacza centrum Fuengiroli jako 10, centrum Marbelli jako 20, a lotnisko w Maladze jako 25, co odczytujemy jako minuty, i wymienia pola golfowe Cabopino, La Siesta, Miraflores, Calanova, La Noria i Chaparral. Czasy obok mapy to czasy dojazdu drogą zmierzone od tej lokalizacji, a nie przejęte z dokumentów dewelopera.',
  'Infobladet lenker til en kartplassering i La Cala de Mijas, og kartet i brosjyren plasserer prosjektet mellom Cabopino og Cala de Mijas, ved A-7. Kartet markerer Fuengirola sentrum med 10, Marbella sentrum med 20 og Málaga lufthavn med 25, som vi leser som minutter, og nevner golfbanene Cabopino, La Siesta, Miraflores, Calanova, La Noria og Chaparral. Tidene ved siden av kartet er kjøretider på vei målt fra denne plasseringen, ikke hentet fra utbyggerens dokumenter.',
  'Informationsbladet länkar till en kartplats i La Cala de Mijas, och kartan i broschyren placerar projektet mellan Cabopino och Cala de Mijas, intill A-7. Kartan markerar Fuengirola centrum med 10, Marbella centrum med 20 och Málaga flygplats med 25, vilket vi läser som minuter, och nämner golfbanorna Cabopino, La Siesta, Miraflores, Calanova, La Noria och Chaparral. Tiderna vid kartan är körtider på väg mätta från den platsen, inte hämtade från exploatörens dokument.')
p('.location.distances[0][0]', 'Fuengirola city centre',
  'Centro de Fuengirola', 'Centre de Fuengirola', 'Zentrum Fuengirola', 'Центр Фуэнхиролы', 'مركز فوينخيرولا', 'Centrum van Fuengirola', 'Centrum Fuengiroli', 'Fuengirola sentrum', 'Fuengirolas centrum')
p('.location.distances[0][1]', '10 minutes',
  '10 minutos, según el mapa del promotor', '10 minutes, d’après la carte du promoteur', '10 Minuten, laut der Karte des Bauträgers', '10 минут по карте застройщика',
  '10 دقائق، حسب خريطة المطوّر', '10 minuten, volgens de kaart van de ontwikkelaar', '10 minut, według mapy dewelopera', '10 minutter, ifølge utbyggerens kart', '10 minuter, enligt exploatörens karta')
p('.location.distances[1][0]', 'Marbella city centre',
  'Centro de Marbella', 'Centre de Marbella', 'Zentrum Marbella', 'Центр Марбельи', 'مركز ماربيا', 'Centrum van Marbella', 'Centrum Marbelli', 'Marbella sentrum', 'Marbellas centrum')
p('.location.distances[1][1]', '20 minutes',
  '20 minutos, según el mapa del promotor', '20 minutes, d’après la carte du promoteur', '20 Minuten, laut der Karte des Bauträgers', '20 минут по карте застройщика',
  '20 دقيقة، حسب خريطة المطوّر', '20 minuten, volgens de kaart van de ontwikkelaar', '20 minut, według mapy dewelopera', '20 minutter, ifølge utbyggerens kart', '20 minuter, enligt exploatörens karta')
p('.location.distances[2][1]', '25 minutes',
  '25 minutos, según el mapa del promotor', '25 minutes, d’après la carte du promoteur', '25 Minuten, laut der Karte des Bauträgers', '25 минут по карте застройщика',
  '25 دقيقة، حسب خريطة المطوّر', '25 minuten, volgens de kaart van de ontwikkelaar', '25 minut, według mapy dewelopera', '25 minutter, ifølge utbyggerens kart', '25 minuter, enligt exploatörens karta')

# ---- investment, checks, availability -------------------------------------------------------------
p('.investment.cards[0][0]', 'Reservation and payment',
  'Reserva y pago', 'Réservation et paiement', 'Reservierung und Zahlung', 'Бронирование и оплата', 'الحجز والدفع', 'Reservering en betaling',
  'Rezerwacja i płatność', 'Reservasjon og betaling', 'Reservation och betalning')
p('.investment.cards[0][1]', 'The developer sets a reservation and a staged payment plan in its infosheet',
  'El promotor fija en su ficha informativa una reserva y un plan de pagos por fases. Le enviamos por escrito los importes y las fechas vigentes antes de que reserve.',
  'Le promoteur prévoit dans sa fiche d’information une réservation et un échéancier de paiement par étapes. Nous vous envoyons par écrit les montants et les dates en vigueur avant que vous ne réserviez.',
  'Der Bauträger legt in seinem Infoblatt eine Reservierung und einen gestaffelten Zahlungsplan fest. Wir senden Ihnen die aktuellen Beträge und Termine schriftlich, bevor Sie reservieren.',
  'В информационном листе застройщик устанавливает бронирование и поэтапный график платежей. Мы пришлём вам действующие суммы и даты в письменном виде до бронирования.',
  'يحدد المطوّر في ورقة معلوماته مبلغ حجز وخطة دفع على مراحل. نرسل لكم المبالغ والمواعيد الحالية كتابةً قبل أن تحجزوا.',
  'De ontwikkelaar legt in zijn infoblad een reservering en een gefaseerd betalingsplan vast. Wij sturen u de actuele bedragen en data schriftelijk toe voordat u reserveert.',
  'Deweloper określa w swojej karcie informacyjnej rezerwację i etapowy plan płatności. Przed rezerwacją przesyłamy Państwu aktualne kwoty i terminy na piśmie.',
  'Utbyggeren fastsetter en reservasjon og en trinnvis betalingsplan i sitt infoblad. Vi sender de gjeldende beløpene og datoene skriftlig før reservasjon.',
  'Exploatören anger i sitt informationsblad en reservation och en betalningsplan i etapper. Vi skickar er de aktuella beloppen och datumen skriftligen innan ni reserverar.')
p('.investment.cards[1][1]', 'The availability list gives the developer’s net prices',
  'La lista de disponibilidad da los precios netos del promotor y la ficha informativa añade el IVA a cada plazo, por lo que entendemos que los precios no incluyen el IVA. No se indica el tipo, así que confirmamos el tipo y los demás gastos de la compra por escrito.',
  'La liste de disponibilité donne les prix nets du promoteur et la fiche d’information ajoute la TVA à chaque échéance ; nous comprenons donc que les prix s’entendent hors TVA. Le taux n’est pas indiqué ; nous le confirmons, ainsi que les autres frais d’achat, par écrit.',
  'Die Verfügbarkeitsliste nennt die Nettopreise des Bauträgers, und das Infoblatt schlägt die MwSt. auf jede Rate auf; wir lesen die Preise daher als Preise ohne MwSt. Der Satz ist nicht angegeben, daher bestätigen wir ihn und die übrigen Kaufnebenkosten schriftlich.',
  'В списке наличия указаны чистые цены застройщика, а в информационном листе к каждому платежу добавляется НДС, поэтому мы понимаем цены как не включающие НДС. Ставка не указана, поэтому мы письменно подтверждаем её и другие расходы на покупку.',
  'تذكر قائمة التوفر الأسعار الصافية للمطوّر، وتضيف ورقة المعلومات ضريبة القيمة المضافة إلى كل دفعة، لذلك نفهم أن الأسعار لا تشمل ضريبة القيمة المضافة. ولم تُذكر النسبة، فنؤكدها مع سائر تكاليف الشراء كتابةً.',
  'De beschikbaarheidslijst geeft de netto prijzen van de ontwikkelaar en het infoblad rekent btw bij elke termijn, dus we lezen de prijzen als exclusief btw. Het tarief staat er niet bij; wij bevestigen het en de overige aankoopkosten schriftelijk.',
  'Lista dostępności podaje ceny netto dewelopera, a karta informacyjna dolicza VAT do każdej raty, dlatego odczytujemy ceny jako nieuwzględniające VAT. Stawka nie jest podana, więc potwierdzamy ją i pozostałe koszty zakupu na piśmie.',
  'Tilgjengelighetslisten oppgir utbyggerens nettopriser, og infobladet legger mva. til hver termin, så vi leser prisene som eksklusive mva. Satsen er ikke oppgitt, så vi bekrefter den og de øvrige kjøpskostnadene skriftlig.',
  'Tillgänglighetslistan anger exploatörens nettopriser och informationsbladet lägger IVA (spansk moms) på varje delbetalning, så vi läser priserna som exklusive IVA. Satsen anges inte, så vi bekräftar den och de övriga köpkostnaderna skriftligen.')
p('.investment.cards[2][1]', 'The plans of the four ground-floor homes draw a storage room',
  'Los planos de las cuatro viviendas de planta baja dibujan un trastero junto a la vivienda, y la memoria de calidades incluye una cocina amueblada con electrodomésticos y lavadora. Ningún documento dice si un trastero o una plaza de garaje están incluidos en cada precio, ni que el mobiliario de las imágenes esté incluido.',
  'Les plans des quatre logements du rez-de-chaussée dessinent une cave à côté du logement, et le descriptif technique prévoit une cuisine aménagée avec électroménager et lave-linge. Aucun document ne dit si une cave ou une place de garage est comprise dans chaque prix, ni que le mobilier des images est compris.',
  'Die Pläne der vier Erdgeschosswohnungen zeigen neben der Wohnung einen Abstellraum, und die Baubeschreibung nennt eine Einbauküche mit Geräten und Waschmaschine. Keines der Dokumente sagt, ob ein Abstellraum oder ein Garagenstellplatz im jeweiligen Preis enthalten ist, oder dass die Möbel auf den Bildern enthalten sind.',
  'На планах четырёх квартир первого этажа рядом с квартирой нарисована кладовая, а в спецификации указана кухня с техникой и стиральной машиной. Ни в одном документе не сказано, входят ли в каждую цену кладовая или место в гараже, и что мебель на изображениях включена.',
  'تُظهر مخططات المساكن الأربعة في الطابق الأرضي غرفة تخزين بجانب المسكن، وتذكر مواصفات البناء مطبخًا مجهّزًا بالأجهزة وغسالة ملابس. ولا تذكر أي وثيقة ما إذا كانت غرفة التخزين أو موقف في المرآب مشمولًا في كل سعر، ولا أن الأثاث في الصور مشمول.',
  'De plattegronden van de vier woningen op de begane grond tonen naast de woning een berging, en het lastenboek geeft een ingerichte keuken met apparatuur en een wasmachine. Geen enkel document zegt of een berging of een garageplaats in elke prijs is inbegrepen, of dat de meubels op de beelden zijn inbegrepen.',
  'Rzuty czterech lokali na parterze pokazują obok lokalu komórkę lokatorską, a specyfikacja techniczna podaje kuchnię w zabudowie ze sprzętem i pralką. Żaden dokument nie mówi, czy komórka lokatorska lub miejsce garażowe jest wliczone w każdą cenę, ani że meble na obrazach są wliczone.',
  'Plantegningene av de fire boligene i første etasje viser en bod ved siden av boligen, og beskrivelsen oppgir et innredet kjøkken med hvitevarer og vaskemaskin. Ingen dokumenter sier om en bod eller en garasjeplass er inkludert i hver pris, eller at møblene på bildene er inkludert.',
  'Planritningarna för de fyra bostäderna på bottenvåningen visar ett förråd intill bostaden, och byggbeskrivningen anger ett inrett kök med vitvaror och tvättmaskin. Inget dokument anger om ett förråd eller en garageplats ingår i varje pris, eller att möblerna på bilderna ingår.')
p('.investment.cards[3][1]', 'The quality specification is undated and at the development stage',
  'La memoria de calidades no lleva fecha, está en fase de desarrollo y puede cambiar por razones técnicas sin reducir la calidad ni el diseño del resultado. Pedimos la memoria definitiva.',
  'Le descriptif technique n’est pas daté, il est au stade du développement et peut changer pour des raisons techniques sans diminuer la qualité ni le design du résultat. Nous demandons le descriptif définitif.',
  'Die Baubeschreibung trägt kein Datum, befindet sich im Entwicklungsstadium und kann sich aus technischen Gründen ändern, ohne dass Qualität oder Design des Ergebnisses darunter leiden. Wir fordern die endgültige Baubeschreibung an.',
  'Спецификация не датирована, находится на стадии разработки и может изменяться по техническим причинам без снижения качества и дизайна результата. Мы запрашиваем окончательную спецификацию.',
  'مواصفات البناء غير مؤرخة وفي مرحلة التطوير، وقد تتغير لأسباب فنية دون انخفاض في جودة النتيجة أو تصميمها. ونطلب المواصفات النهائية.',
  'Het lastenboek is niet gedateerd, bevindt zich in de ontwikkelingsfase en kan om technische redenen wijzigen zonder dat de kwaliteit of het ontwerp van het resultaat daaronder lijdt. Wij vragen het definitieve lastenboek op.',
  'Specyfikacja techniczna nie jest datowana, jest na etapie opracowania i może się zmienić z przyczyn technicznych bez obniżenia jakości ani projektu efektu końcowego. Prosimy o ostateczną specyfikację.',
  'Beskrivelsen er ikke datert, er på utviklingsstadiet og kan endres av tekniske grunner uten at kvaliteten eller designet på resultatet reduseres. Vi ber om den endelige beskrivelsen.',
  'Byggbeskrivningen saknar datum, är på utvecklingsstadiet och kan ändras av tekniska skäl utan att resultatets kvalitet eller design försämras. Vi begär den slutliga byggbeskrivningen.')

p('.trustDossier.cards[0][1]', 'The infosheet gives the building licence as granted',
  'La ficha informativa indica la licencia de obras como concedida, el inicio de obra previsto para el segundo trimestre de 2026 y el fin previsto para el cuarto trimestre de 2028; la lista de disponibilidad da la fase como en construcción. La ficha no lleva fecha de emisión. Preguntamos hasta dónde ha avanzado la obra y pedimos la licencia y el aval que cubre las cantidades entregadas a cuenta.',
  'La fiche d’information indique le permis de construire comme accordé, le début des travaux attendu au deuxième trimestre 2026 et la fin attendue au quatrième trimestre 2028 ; la liste de disponibilité donne l’état d’avancement comme en construction. La fiche ne porte pas de date d’émission. Nous demandons où en est le chantier, ainsi que le permis et la garantie bancaire qui couvre les sommes versées en acompte.',
  'Das Infoblatt gibt die Baugenehmigung als erteilt an, den Baubeginn als für das zweite Quartal 2026 und das Ende als für das vierte Quartal 2028 erwartet; die Verfügbarkeitsliste nennt als Stand „im Bau“. Das Infoblatt trägt kein Ausgabedatum. Wir fragen nach, wie weit der Bau fortgeschritten ist, und fordern die Genehmigung sowie die Bankgarantie an, die geleistete Anzahlungen absichert.',
  'В информационном листе разрешение на строительство указано как выданное, начало строительства ожидается во втором квартале 2026 года, окончание — в четвёртом квартале 2028 года; в списке наличия стадия указана как «строится». В листе нет даты выпуска. Мы уточняем, как далеко продвинулась стройка, и запрашиваем разрешение и банковскую гарантию, покрывающую суммы, внесённые в счёт оплаты.',
  'تذكر ورقة المعلومات أن رخصة البناء ممنوحة، وأن بدء الإنشاء متوقع في الربع الثاني من عام 2026 وانتهاءه في الربع الرابع من عام 2028؛ وتذكر قائمة التوفر أن المرحلة قيد الإنشاء. ولا تحمل ورقة المعلومات تاريخ إصدار. نستفسر عن مدى تقدّم الأعمال، ونطلب الرخصة والضمان المصرفي الذي يغطي المبالغ المدفوعة على الحساب.',
  'Het infoblad geeft de bouwvergunning als verleend, de start van de bouw als verwacht in het tweede kwartaal van 2026 en het einde als verwacht in het vierde kwartaal van 2028; de beschikbaarheidslijst geeft de fase als in aanbouw. Het infoblad vermeldt geen uitgiftedatum. We vragen hoe ver de bouw is gevorderd, en vragen de vergunning en de bankgarantie die de vooruitbetaalde bedragen dekt op.',
  'Karta informacyjna podaje pozwolenie na budowę jako udzielone, rozpoczęcie budowy jako oczekiwane w drugim kwartale 2026 roku, a zakończenie w czwartym kwartale 2028 roku; lista dostępności podaje etap jako w budowie. Karta nie ma daty wydania. Pytamy, jak daleko zaawansowana jest budowa, i prosimy o pozwolenie oraz gwarancję bankową, która zabezpiecza kwoty wpłacone na poczet zakupu.',
  'Infobladet oppgir byggetillatelsen som gitt, byggestart som ventet i andre kvartal 2026 og byggeslutt som ventet i fjerde kvartal 2028; tilgjengelighetslisten oppgir stadiet som under bygging. Infobladet har ingen utstedelsesdato. Vi spør hvor langt byggingen har kommet, og ber om tillatelsen og bankgarantien som dekker beløp betalt på forskudd.',
  'Informationsbladet anger bygglovet som beviljat, byggstart som väntad under andra kvartalet 2026 och byggslut som väntat under fjärde kvartalet 2028; tillgänglighetslistan anger skedet som under uppförande. Informationsbladet har inget utfärdandedatum. Vi frågar hur långt bygget har kommit och begär bygglovet och bankgarantin som täcker belopp som betalats i förskott.')
p('.trustDossier.cards[1][1]', 'The end of construction is an estimate and no document',
  'El fin de obra es una estimación y ningún documento da una fecha contractual. Pedimos la fecha contractual del portal que elija y la ponemos por escrito.',
  'La fin des travaux est une estimation et aucun document ne donne de date contractuelle. Nous demandons la date contractuelle de la cage que vous choisissez et la mettons par écrit.',
  'Das Bauende ist eine Schätzung, und kein Dokument nennt einen vertraglichen Termin. Wir fragen den vertraglichen Termin für den von Ihnen gewählten Aufgang an und halten ihn schriftlich fest.',
  'Окончание строительства — лишь оценка, и ни в одном документе нет договорной даты. Мы запрашиваем договорную дату для выбранного вами подъезда и фиксируем её письменно.',
  'انتهاء الإنشاء تقدير، ولا تذكر أي وثيقة موعدًا تعاقديًا. نطلب الموعد التعاقدي للمدخل الذي تختارونه ونوثّقه كتابةً.',
  'Het einde van de bouw is een schatting en geen enkel document geeft een contractuele datum. We vragen de contractuele datum op voor de portiek die u kiest en leggen die schriftelijk vast.',
  'Zakończenie budowy to szacunek i żaden dokument nie podaje terminu umownego. Prosimy o termin umowny dla klatki, którą Państwo wybiorą, i potwierdzamy go na piśmie.',
  'Byggeslutt er et anslag, og ingen dokumenter oppgir en kontraktsfestet dato. Vi ber om den kontraktsfestede datoen for den valgte oppgangen, og setter den skriftlig.',
  'Byggslutet är en uppskattning och inget dokument anger ett avtalat datum. Vi begär det avtalade datumet för den uppgång ni väljer och sätter det skriftligen.')
p('.trustDossier.cards[2][0]', 'The built areas',
  'Las superficies construidas', 'Les surfaces construites', 'Die bebauten Flächen', 'Площади застройки', 'المساحات المبنية', 'De bebouwde oppervlakten',
  'Powierzchnie zabudowy', 'Det bebygde arealet', 'Byggytorna')
p('.trustDossier.cards[2][1]', 'The availability list and the plans agree',
  'La lista de disponibilidad y los planos coinciden en la superficie construida de ocho viviendas, y de 4.3.A y 4.3.B con una diferencia de hasta {N0.01} {U}. Difieren en 5.3.A, que figura con {N148.06} {U} frente a {N147.89} {U} en el plano, en 6.0.A, con {N58.48} {U} frente a {N58.54} {U}, y en 6.1.A, con {N133.41} {U} frente a {N133.56} {U}. Los planos dan además superficies según el Decreto 218/2005, por ejemplo {N90.76} {U} de superficie útil y {N110.56} {U} construidos para 2.3.B frente a {N121.33} {U} en la lista. Confirmamos qué cifras emplea el contrato.',
  'La liste de disponibilité et les plans concordent sur la surface construite de huit logements, et de 4.3.A et 4.3.B à {N0.01} {U} près. Ils diffèrent pour 5.3.A, listé à {N148.06} {U} contre {N147.89} {U} sur le plan, pour 6.0.A, listé à {N58.48} {U} contre {N58.54} {U}, et pour 6.1.A, listé à {N133.41} {U} contre {N133.56} {U}. Les plans donnent aussi des surfaces selon le décret 218/2005, par exemple {N90.76} {U} de surface utile et {N110.56} {U} construits pour 2.3.B contre {N121.33} {U} sur la liste. Nous confirmons quels chiffres le contrat retient.',
  'Die Verfügbarkeitsliste und die Pläne stimmen bei der bebauten Fläche von acht Wohnungen überein, bei 4.3.A und 4.3.B bis auf {N0.01} {U}. Sie weichen bei 5.3.A ab, aufgeführt mit {N148.06} {U} gegenüber {N147.89} {U} im Plan, bei 6.0.A mit {N58.48} {U} gegenüber {N58.54} {U} und bei 6.1.A mit {N133.41} {U} gegenüber {N133.56} {U}. Die Pläne nennen außerdem Flächen nach dem Dekret 218/2005, zum Beispiel {N90.76} {U} Wohnfläche und {N110.56} {U} bebaute Fläche für 2.3.B gegenüber {N121.33} {U} in der Liste. Wir bestätigen, welche Zahlen der Vertrag zugrunde legt.',
  'Список наличия и планы совпадают по площади застройки восьми квартир, а по 4.3.A и 4.3.B — с точностью до {N0.01} {U}. Расхождения у 5.3.A: в списке {N148.06} {U}, на плане {N147.89} {U}; у 6.0.A: в списке {N58.48} {U}, на плане {N58.54} {U}; у 6.1.A: в списке {N133.41} {U}, на плане {N133.56} {U}. На планах также даны площади по декрету 218/2005, например {N90.76} {U} полезной площади и {N110.56} {U} площади застройки для 2.3.B против {N121.33} {U} в списке. Мы уточняем, какие цифры принимает договор.',
  'تتفق قائمة التوفر والمخططات في المساحة المبنية لثمانية مساكن، وللمسكنين 4.3.A و4.3.B بفارق لا يتجاوز {N0.01} {U}. وتختلف في 5.3.A المدرج بمساحة {N148.06} {U} مقابل {N147.89} {U} في المخطط، وفي 6.0.A المدرج بمساحة {N58.48} {U} مقابل {N58.54} {U}، وفي 6.1.A المدرج بمساحة {N133.41} {U} مقابل {N133.56} {U}. وتذكر المخططات أيضًا مساحات بموجب المرسوم 218/2005، مثل {N90.76} {U} مساحة صافية و{N110.56} {U} مساحة مبنية للمسكن 2.3.B مقابل {N121.33} {U} في القائمة. ونؤكد أي الأرقام يعتمدها العقد.',
  'De beschikbaarheidslijst en de plattegronden komen overeen qua bebouwde oppervlakte van acht woningen, en van 4.3.A en 4.3.B tot op {N0.01} {U}. Ze wijken af bij 5.3.A, vermeld met {N148.06} {U} tegenover {N147.89} {U} op de plattegrond, bij 6.0.A, vermeld met {N58.48} {U} tegenover {N58.54} {U}, en bij 6.1.A, vermeld met {N133.41} {U} tegenover {N133.56} {U}. De plattegronden geven ook oppervlakten volgens decreet 218/2005, bijvoorbeeld {N90.76} {U} gebruiksoppervlak en {N110.56} {U} bebouwde oppervlakte voor 2.3.B tegenover {N121.33} {U} op de lijst. We bevestigen welke cijfers het contract hanteert.',
  'Lista dostępności i rzuty zgadzają się co do powierzchni zabudowy ośmiu lokali, a w przypadku 4.3.A i 4.3.B z dokładnością do {N0.01} {U}. Różnią się przy 5.3.A, podanym na liście jako {N148.06} {U} wobec {N147.89} {U} na rzucie, przy 6.0.A, podanym jako {N58.48} {U} wobec {N58.54} {U}, i przy 6.1.A, podanym jako {N133.41} {U} wobec {N133.56} {U}. Rzuty podają też powierzchnie według dekretu 218/2005, na przykład {N90.76} {U} użytkowej i {N110.56} {U} zabudowy dla 2.3.B wobec {N121.33} {U} na liście. Potwierdzamy, jakie wartości przyjmuje umowa.',
  'Tilgjengelighetslisten og plantegningene stemmer overens om bebygd areal for åtte boliger, og for 4.3.A og 4.3.B med en forskjell på høyst {N0.01} {U}. De avviker for 5.3.A, oppført med {N148.06} {U} mot {N147.89} {U} på plantegningen, for 6.0.A, oppført med {N58.48} {U} mot {N58.54} {U}, og for 6.1.A, oppført med {N133.41} {U} mot {N133.56} {U}. Plantegningene oppgir også arealer etter dekret 218/2005, for eksempel {N90.76} {U} innvendig areal og {N110.56} {U} bebygd areal for 2.3.B mot {N121.33} {U} på listen. Vi bekrefter hvilke tall kontrakten bruker.',
  'Tillgänglighetslistan och planritningarna stämmer överens om byggytan för åtta bostäder, och för 4.3.A och 4.3.B med högst {N0.01} {U} i skillnad. De avviker för 5.3.A, listad med {N148.06} {U} mot {N147.89} {U} på planritningen, för 6.0.A, listad med {N58.48} {U} mot {N58.54} {U}, och för 6.1.A, listad med {N133.41} {U} mot {N133.56} {U}. Planritningarna anger också ytor enligt dekret 218/2005, till exempel {N90.76} {U} boarea och {N110.56} {U} byggyta för 2.3.B mot {N121.33} {U} på listan. Vi bekräftar vilka siffror avtalet använder.')
p('.trustDossier.cards[3][0]', 'The terraces and solariums',
  'Las terrazas y los soláriums', 'Les terrasses et les solariums', 'Die Terrassen und Solarien', 'Террасы и солярии', 'التراسات والسولاريومات', 'De terrassen en solariums',
  'Tarasy i solaria', 'Terrassene og solterrassene', 'Terrasserna och solterrasserna')
p('.trustDossier.cards[3][1]', 'For 3.3.A the rooms of the plan',
  'En 3.3.A las estancias del plano suman {N105.53} {U} de terraza y solárium, frente a {N105.43} {U} en la tabla del propio plano. La terraza de {N66.67} {U} de 5.1.B y 6.1.A incluye un patio de {N7.34} {U}. Confirmamos qué cifras emplea el contrato.',
  'Pour 3.3.A, les pièces du plan totalisent {N105.53} {U} de terrasse et de solarium, contre {N105.43} {U} dans le tableau du plan lui-même. La terrasse de {N66.67} {U} de 5.1.B et 6.1.A comprend un patio de {N7.34} {U}. Nous confirmons quels chiffres le contrat retient.',
  'Bei 3.3.A ergeben die Räume des Plans zusammen {N105.53} {U} Terrasse und Solarium, gegenüber {N105.43} {U} in der Tabelle des Plans selbst. Die Terrasse von {N66.67} {U} bei 5.1.B und 6.1.A schließt einen Patio von {N7.34} {U} ein. Wir bestätigen, welche Zahlen der Vertrag zugrunde legt.',
  'У 3.3.A помещения на плане в сумме дают {N105.53} {U} террасы и солярия против {N105.43} {U} в таблице самого плана. Терраса {N66.67} {U} у 5.1.B и 6.1.A включает патио {N7.34} {U}. Мы уточняем, какие цифры принимает договор.',
  'في المسكن 3.3.A يبلغ مجموع الغرف على المخطط {N105.53} {U} من التراس والسولاريوم، مقابل {N105.43} {U} في جدول المخطط نفسه. ويشمل التراس البالغ {N66.67} {U} في 5.1.B و6.1.A فناءً بمساحة {N7.34} {U}. ونؤكد أي الأرقام يعتمدها العقد.',
  'Bij 3.3.A tellen de ruimten op de plattegrond op tot {N105.53} {U} terras en solarium, tegenover {N105.43} {U} in de tabel van de plattegrond zelf. Het terras van {N66.67} {U} bij 5.1.B en 6.1.A omvat een patio van {N7.34} {U}. We bevestigen welke cijfers het contract hanteert.',
  'W przypadku 3.3.A pomieszczenia na rzucie sumują się do {N105.53} {U} tarasu i solarium, wobec {N105.43} {U} w tabeli samego rzutu. Taras o powierzchni {N66.67} {U} przy 5.1.B i 6.1.A obejmuje patio o powierzchni {N7.34} {U}. Potwierdzamy, jakie wartości przyjmuje umowa.',
  'For 3.3.A utgjør rommene på plantegningen til sammen {N105.53} {U} terrasse og solterrasse, mot {N105.43} {U} i plantegningens egen tabell. Terrassen på {N66.67} {U} for 5.1.B og 6.1.A omfatter en patio på {N7.34} {U}. Vi bekrefter hvilke tall kontrakten bruker.',
  'För 3.3.A blir rummen på planritningen tillsammans {N105.53} {U} terrass och solterrass, mot {N105.43} {U} i planritningens egen tabell. Terrassen på {N66.67} {U} för 5.1.B och 6.1.A omfattar en patio på {N7.34} {U}. Vi bekräftar vilka siffror avtalet använder.')
p('.trustDossier.cards[4][0]', 'The solarium pools',
  'Las piscinas de los soláriums', 'Les bassins des solariums', 'Die Pools auf den Solarien', 'Бассейны на солярии', 'مسابح السولاريومات', 'De zwembaden op de solariums',
  'Baseny na solariach', 'Bassengene på solterrassene', 'Poolerna på solterrasserna')
p('.trustDossier.cards[4][1]', 'The plans of all seven third-floor homes',
  'Los planos de las siete viviendas de la tercera planta dibujan una pequeña piscina en el solárium, y el dosier muestra una en el solárium de una vivienda de tres dormitorios, pero la lista de disponibilidad no menciona ninguna piscina. Confirmamos si se construye y está incluida.',
  'Les plans des sept logements du troisième étage dessinent un petit bassin sur le solarium, et le dossier en montre un sur le solarium d’un logement de trois chambres, mais la liste de disponibilité ne mentionne aucune piscine. Nous confirmons s’il est réalisé et compris.',
  'Die Pläne aller sieben Wohnungen im dritten Obergeschoss zeigen einen kleinen Pool auf dem Solarium, und die Broschüre zeigt einen auf dem Solarium einer Wohnung mit drei Schlafzimmern, aber die Verfügbarkeitsliste erwähnt keinen Pool. Wir bestätigen, ob er gebaut wird und enthalten ist.',
  'На планах всех семи квартир четвёртого этажа на солярии нарисован небольшой бассейн, и буклет показывает такой бассейн на солярии квартиры с тремя спальнями, но в списке наличия бассейн не упомянут. Мы уточняем, будет ли он построен и включён в цену.',
  'تُظهر مخططات المساكن السبعة في الطابق الثالث مسبحًا صغيرًا على السولاريوم، ويُظهر الكتيّب مسبحًا على سولاريوم مسكن بثلاث غرف نوم، لكن قائمة التوفر لا تذكر أي مسبح. ونؤكد ما إذا كان سيُبنى وما إذا كان مشمولًا.',
  'De plattegronden van alle zeven woningen op de derde verdieping tonen een klein zwembad op het solarium, en de brochure toont er een op het solarium van een woning met drie slaapkamers, maar de beschikbaarheidslijst vermeldt geen zwembad. We bevestigen of het wordt gebouwd en is inbegrepen.',
  'Rzuty wszystkich siedmiu lokali na trzecim piętrze pokazują niewielki basen na solarium, a broszura pokazuje taki basen na solarium lokalu z trzema sypialniami, ale lista dostępności nie wspomina o żadnym basenie. Potwierdzamy, czy zostanie wybudowany i czy jest wliczony.',
  'Plantegningene av alle de syv boligene i fjerde etasje viser et lite basseng på solterrassen, og brosjyren viser et på solterrassen til en bolig med tre soverom, men tilgjengelighetslisten nevner ikke noe basseng. Vi bekrefter om det bygges og er inkludert.',
  'Planritningarna för alla sju bostäder på tredje våningen visar en liten pool på solterrassen, och broschyren visar en på solterrassen till en bostad med tre sovrum, men tillgänglighetslistan nämner ingen pool. Vi bekräftar om den byggs och ingår.')
p('.trustDossier.cards[5][1]', 'The dossier’s map marks Fuengirola',
  'El mapa del dosier marca el centro de Fuengirola a 10, el centro de Marbella a 20 y el aeropuerto de Málaga a 25 con un signo ″ y sin unidad ni medio de transporte. Los interpretamos como minutos y los confirmamos en una visita.',
  'La carte du dossier indique le centre de Fuengirola à 10, le centre de Marbella à 20 et l’aéroport de Málaga à 25 avec un signe ″ et sans unité ni mode de déplacement. Nous les lisons comme des minutes et les confirmons lors d’une visite.',
  'Die Karte der Broschüre gibt das Zentrum von Fuengirola mit 10, das Zentrum von Marbella mit 20 und den Flughafen Málaga mit 25 an, mit einem ″-Zeichen und ohne Einheit oder Verkehrsmittel. Wir lesen sie als Minuten und bestätigen sie bei einem Besuch.',
  'На карте в буклете центр Фуэнхиролы отмечен как 10, центр Марбельи — как 20, а аэропорт Малаги — как 25, со знаком ″, без единицы измерения и без указания способа передвижения. Мы читаем эти числа как минуты и подтверждаем их при визите.',
  'تضع خريطة الكتيّب وسط فوينخيرولا عند 10 ووسط ماربيا عند 20 ومطار مالقة عند 25 بعلامة ″ ومن دون وحدة أو وسيلة تنقّل. ونقرأها على أنها دقائق ونؤكدها خلال زيارة.',
  'De kaart in de brochure geeft het centrum van Fuengirola aan op 10, het centrum van Marbella op 20 en de luchthaven van Málaga op 25, met een ″-teken en zonder eenheid of vervoermiddel. Wij lezen ze als minuten en bevestigen ze tijdens een bezichtiging.',
  'Mapa w broszurze oznacza centrum Fuengiroli jako 10, centrum Marbelli jako 20, a lotnisko w Maladze jako 25, ze znakiem ″, bez jednostki i środka transportu. Odczytujemy je jako minuty i potwierdzamy podczas wizyty.',
  'Kartet i brosjyren markerer Fuengirola sentrum med 10, Marbella sentrum med 20 og Málaga lufthavn med 25, med et ″-tegn og uten enhet eller transportmiddel. Vi leser dem som minutter og bekrefter dem på en visning.',
  'Kartan i broschyren markerar Fuengirola centrum med 10, Marbella centrum med 20 och Málaga flygplats med 25, med ett ″-tecken och utan enhet eller färdsätt. Vi läser dem som minuter och bekräftar dem vid ett besök.')

p('.availability.headlineHtml', '13 of 54 homes',
  '13 de 54 viviendas <em>a la venta actualmente</em>', '13 logements sur 54 <em>actuellement annoncés</em>', '13 von 54 Wohnungen <em>derzeit verfügbar</em>',
  '13 из 54 квартир <em>сейчас в продаже</em>', '13 من أصل 54 مسكنًا <em>معروضة حاليًا</em>', '13 van de 54 woningen <em>momenteel beschikbaar</em>',
  '13 z 54 lokali <em>obecnie dostępnych</em>', '13 av 54 boliger <em>ledige nå</em>', '13 av 54 bostäder <em>lediga just nu</em>')
p('.availability.copy', 'Thirteen homes are listed',
  'Se listan trece viviendas: tres de un dormitorio y una de dos dormitorios en planta baja con jardín, dos de tres dormitorios en la primera planta y siete viviendas en la tercera planta con solárium. La lista no dice nada de las otras 41. La disponibilidad y los precios son los de la lista a 29 de octubre de 2026 y se confirman antes de cualquier reserva.',
  'Treize logements sont listés : trois de une chambre et un de deux chambres au rez-de-chaussée avec jardin, deux de trois chambres au premier étage et sept au troisième étage avec solarium. La liste ne dit rien des 41 autres. La disponibilité et les prix sont ceux de la liste au 29 octobre 2026 et sont confirmés avant toute réservation.',
  'Dreizehn Wohnungen sind aufgeführt: drei mit einem Schlafzimmer und eine mit zwei Schlafzimmern im Erdgeschoss mit Garten, zwei mit drei Schlafzimmern im ersten Obergeschoss und sieben im dritten Obergeschoss mit Solarium. Zu den übrigen 41 sagt die Liste nichts. Verfügbarkeit und Preise entsprechen der Liste vom 29. Oktober 2026 und werden vor jeder Reservierung bestätigt.',
  'В списке указаны тринадцать квартир: три с одной спальней и одна с двумя спальнями на первом этаже с садом, две с тремя спальнями на втором этаже и семь на четвёртом этаже с солярием. О других 41 список ничего не сообщает. Наличие и цены приведены по списку на 29 октября 2026 года и подтверждаются до любого бронирования.',
  'أُدرج ثلاثة عشر مسكنًا: ثلاثة بغرفة نوم ومسكن بغرفتي نوم في الطابق الأرضي مع حديقة، ومسكنان بثلاث غرف نوم في الطابق الأول، وسبعة مساكن في الطابق الثالث مع سولاريوم. ولا تذكر القائمة شيئًا عن المساكن الـ41 الأخرى. التوفر والأسعار وفق القائمة بتاريخ 29 أكتوبر 2026 وتُؤكَّد قبل أي حجز.',
  'Dertien woningen zijn vermeld: drie met een slaapkamer en een met twee slaapkamers op de begane grond met een tuin, twee met drie slaapkamers op de eerste verdieping en zeven op de derde verdieping met een solarium. De lijst zegt niets over de andere 41. Beschikbaarheid en prijzen zijn die van de lijst van 29 oktober 2026 en worden vóór elke reservering bevestigd.',
  'Wymieniono trzynaście lokali: trzy z jedną sypialnią i jeden z dwiema sypialniami na parterze z ogrodem, dwa z trzema sypialniami na pierwszym piętrze i siedem na trzecim piętrze z solarium. Lista nic nie mówi o pozostałych 41. Dostępność i ceny są takie, jak na liście z 29 października 2026 r., i są potwierdzane przed każdą rezerwacją.',
  'Tretten boliger er oppført: tre med ett soverom og én med to soverom i første etasje med hage, to med tre soverom i andre etasje og syv i fjerde etasje med solterrasse. Listen sier ingenting om de øvrige 41. Tilgjengelighet og priser er slik de er oppført per 29. oktober 2026, og bekreftes før enhver reservasjon.',
  'Tretton bostäder är listade: tre med ett sovrum och en med två sovrum på bottenvåningen med trädgård, två med tre sovrum på första våningen och sju på tredje våningen med solterrass. Listan säger ingenting om de övriga 41. Tillgänglighet och priser är som listade den 29 oktober 2026 och bekräftas före varje reservation.')
p('.availability.sourceNote', 'References, bedrooms, built areas and prices',
  'Las referencias, los dormitorios, las superficies construidas y los precios se transcriben de la lista de disponibilidad que se nos facilitó, tal como figuraba el 29 de octubre de 2026, que muestra 13 de las 54 viviendas y no dice nada del resto. La superficie construida es la cifra de la lista, que los planos encabezan como «vivienda + ZZCC», es decir, la vivienda más una parte de las zonas comunes. Las superficies interiores, terrazas, jardines y soláriums proceden de los planos del promotor. Los precios son las cifras netas del promotor y la ficha informativa añade el IVA a sus plazos, por lo que entendemos que no incluyen el IVA. Donde la lista y los planos difieren en la superficie construida, en 5.3.A, 6.0.A y 6.1.A, la tabla sigue la lista y se dan ambas cifras más arriba.',
  'Les références, les chambres, les surfaces construites et les prix sont retranscrits de la liste de disponibilité qui nous a été remise, telle qu’elle figurait le 29 octobre 2026, qui montre 13 des 54 logements et ne dit rien des autres. La surface construite est le chiffre de la liste, que les plans intitulent « vivienda + ZZCC », c’est-à-dire le logement plus une part des parties communes. Les surfaces intérieures, terrasses, jardins et solariums sont tirés des plans du promoteur. Les prix sont les chiffres nets du promoteur et la fiche d’information ajoute la TVA à ses échéances ; nous les comprenons donc hors TVA. Lorsque la liste et les plans diffèrent sur la surface construite, pour 5.3.A, 6.0.A et 6.1.A, le tableau suit la liste et les deux chiffres sont donnés ci-dessus.',
  'Referenzen, Schlafzimmer, bebaute Flächen und Preise sind der uns vorliegenden Verfügbarkeitsliste mit Stand 29. Oktober 2026 entnommen, die 13 der 54 Wohnungen zeigt und zu den übrigen nichts sagt. Die bebaute Fläche ist der Wert der Liste, den die Pläne mit „vivienda + ZZCC“ überschreiben, also die Wohnung plus ein Anteil an den Gemeinschaftsflächen. Die Innenflächen, Terrassen, Gärten und Solarien stammen aus den Plänen des Bauträgers. Die Preise sind die Nettowerte des Bauträgers, und das Infoblatt schlägt die MwSt. auf seine Raten auf; wir lesen sie daher als Preise ohne MwSt. Wo die Liste und die Pläne bei der bebauten Fläche abweichen, bei 5.3.A, 6.0.A und 6.1.A, folgt die Tabelle der Liste, und beide Werte sind oben angegeben.',
  'Номера, число спален, площади застройки и цены перепечатаны из списка наличия, который нам передали, по состоянию на 29 октября 2026 года; в нём показаны 13 из 54 квартир, об остальных ничего не сказано. Площадь застройки — это цифра из списка, которую на планах обозначают как «vivienda + ZZCC», то есть квартира плюс доля общих зон. Внутренние площади, террасы, сады и солярии взяты из планов застройщика. Цены — это чистые цифры застройщика, а информационный лист добавляет НДС к своим платежам, поэтому мы понимаем их как не включающие НДС. Там, где список и планы расходятся по площади застройки, — у 5.3.A, 6.0.A и 6.1.A — таблица следует списку, а обе цифры приведены выше.',
  'نقلنا المراجع وعدد غرف النوم والمساحات المبنية والأسعار من قائمة التوفر التي زُوِّدنا بها، كما وردت بتاريخ 29 أكتوبر 2026، وهي تُظهر 13 من أصل 54 مسكنًا ولا تذكر شيئًا عن الباقي. والمساحة المبنية هي رقم القائمة، وتضعه المخططات تحت عنوان «vivienda + ZZCC»، أي المسكن مضافًا إليه حصة من المرافق المشتركة. أما المساحات الداخلية والتراسات والحدائق والسولاريومات فمأخوذة من مخططات المطوّر. والأسعار هي الأرقام الصافية للمطوّر، وتضيف ورقة المعلومات ضريبة القيمة المضافة إلى دفعاتها، لذلك نفهم أنها لا تشملها. وحيث تختلف القائمة والمخططات في المساحة المبنية، في 5.3.A و6.0.A و6.1.A، يتبع الجدول القائمة وترد الأرقام كلها أعلاه.',
  'De referenties, slaapkamers, bebouwde oppervlakten en prijzen zijn overgenomen uit de beschikbaarheidslijst die we kregen, zoals vermeld op 29 oktober 2026, die 13 van de 54 woningen toont en niets zegt over de rest. De bebouwde oppervlakte is het cijfer van de lijst, dat de plattegronden “vivienda + ZZCC” noemen, de woning plus een aandeel in de gemeenschappelijke ruimten. De binnenoppervlakten, terrassen, tuinen en solariums komen uit de plattegronden van de ontwikkelaar. De prijzen zijn de nettocijfers van de ontwikkelaar en het infoblad rekent btw bij zijn termijnen, dus we lezen ze als exclusief btw. Waar de lijst en de plattegronden afwijken qua bebouwde oppervlakte, bij 5.3.A, 6.0.A en 6.1.A, volgt de tabel de lijst en staan beide cijfers hierboven.',
  'Numery, liczba sypialni, powierzchnie zabudowy i ceny pochodzą z listy dostępności, którą otrzymaliśmy, według stanu na 29 października 2026 r.; pokazuje ona 13 z 54 lokali i nic nie mówi o pozostałych. Powierzchnia zabudowy to wartość z listy, którą rzuty opisują jako „vivienda + ZZCC”, czyli lokal wraz z udziałem w częściach wspólnych. Powierzchnie wewnętrzne, tarasy, ogrody i solaria pochodzą z rzutów dewelopera. Ceny to kwoty netto dewelopera, a karta informacyjna dolicza VAT do swoich rat, dlatego odczytujemy je jako nieuwzględniające VAT. Tam, gdzie lista i rzuty różnią się co do powierzchni zabudowy, przy 5.3.A, 6.0.A i 6.1.A, tabela podąża za listą, a obie wartości podano powyżej.',
  'Referanser, soverom, bebygde arealer og priser er hentet fra tilgjengelighetslisten vi fikk, slik den sto per 29. oktober 2026, som viser 13 av de 54 boligene og ikke sier noe om resten. Det bebygde arealet er listens tall, som plantegningene overskriver «vivienda + ZZCC», altså boligen pluss en andel av fellesarealene. De innvendige arealene, terrassene, hagene og solterrassene er hentet fra utbyggerens plantegninger. Prisene er utbyggerens nettotall, og infobladet legger mva. til terminene, så vi leser dem som eksklusive mva. Der listen og plantegningene avviker på bebygd areal, for 5.3.A, 6.0.A og 6.1.A, følger tabellen listen, og begge tallene er oppgitt ovenfor.',
  'Referenser, sovrum, byggytor och priser är hämtade från tillgänglighetslistan vi fick, så som den stod den 29 oktober 2026, som visar 13 av de 54 bostäderna och inte säger något om resten. Byggytan är listans siffra, som planritningarna rubricerar ”vivienda + ZZCC”, alltså bostaden plus en andel av de gemensamma ytorna. De invändiga ytorna, terrasserna, trädgårdarna och solterrasserna är hämtade från exploatörens planritningar. Priserna är exploatörens nettosiffror och informationsbladet lägger IVA på sina delbetalningar, så vi läser dem som exklusive IVA. Där listan och planritningarna avviker i byggyta, för 5.3.A, 6.0.A och 6.1.A, följer tabellen listan och båda siffrorna anges ovan.')

# ---- viewing, enquiry, FAQ, SEO --------------------------------------------------------------------
p('.privateViewing.insights[1][1]', 'We walk the area with you',
  'Recorremos la zona con usted y cronometramos los trayectos a la playa y a las tiendas más cercanas.',
  'Nous parcourons le quartier avec vous et chronométrons les trajets jusqu’à la plage et aux commerces les plus proches.',
  'Wir gehen die Umgebung mit Ihnen ab und stoppen die Wege zum Strand und zu den nächsten Geschäften.',
  'Мы вместе с вами пройдём по району и засечём время в пути до пляжа и ближайших магазинов.',
  'نتجوّل معكم في المنطقة ونحسب زمن الوصول إلى الشاطئ وأقرب المتاجر.',
  'We lopen het gebied met u door en meten de tijd naar het strand en de dichtstbijzijnde winkels.',
  'Przechodzimy z Państwem okolicę i mierzymy czas dojścia na plażę i do najbliższych sklepów.',
  'Vi går gjennom området sammen og tar tiden til stranden og de nærmeste butikkene.',
  'Vi går igenom området tillsammans med er och tar tid på vägarna till stranden och de närmaste butikerna.')
p('.enquiry.message', 'Hello Nueva Living, I would like information about Arosa',
  'Hola Nueva Living, me gustaría recibir información sobre Arosa.', 'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Arosa.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Arosa.', 'Здравствуйте, Nueva Living! Я хотел бы получить информацию о Arosa.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Arosa.', 'Hallo Nueva Living, ik zou graag informatie ontvangen over Arosa.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Arosa.', 'Hei Nueva Living, jeg vil gjerne ha informasjon om Arosa.',
  'Hej Nueva Living, jag skulle vilja ha information om Arosa.')
p('.enquiry.headlineHtml', 'Ask about',
  'Pregunte por <em>Arosa</em>', 'Renseignez-vous sur <em>Arosa</em>', 'Fragen Sie nach <em>Arosa</em>', 'Узнайте о <em>Arosa</em>',
  'اسأل عن <em>Arosa</em>', 'Vraag naar <em>Arosa</em>', 'Zapytaj o <em>Arosa</em>', 'Spør om <em>Arosa</em>', 'Fråga om <em>Arosa</em>')

p('.faq[0][1]', 'The complex has 54 homes',
  'El conjunto tiene 54 viviendas y 13 figuran con precio: tres de un dormitorio, tres de dos y siete de tres, de {E705000} a {E1570000} más IVA.',
  'L’ensemble compte 54 logements et 13 sont listés avec un prix : trois de une chambre, trois de deux et sept de trois, de {E705000} à {E1570000} hors TVA.',
  'Die Anlage hat 54 Wohnungen, 13 davon sind mit Preis aufgeführt: drei mit einem, drei mit zwei und sieben mit drei Schlafzimmern, von {E705000} bis {E1570000} zuzüglich MwSt.',
  'В комплексе 54 квартиры, 13 из них указаны с ценой: три с одной спальней, три с двумя и семь с тремя, от {E705000} до {E1570000} без НДС.',
  'يضم المجمع 54 مسكنًا، منها 13 مدرجًا مع السعر: ثلاثة بغرفة نوم وثلاثة بغرفتي نوم وسبعة بثلاث غرف نوم، من {E705000} إلى {E1570000} دون ضريبة القيمة المضافة.',
  'Het complex telt 54 woningen en 13 daarvan zijn met een prijs vermeld: drie met een slaapkamer, drie met twee en zeven met drie, van {E705000} tot {E1570000} excl. btw.',
  'Zespół liczy 54 lokale, z czego 13 jest podanych z ceną: trzy z jedną sypialnią, trzy z dwiema i siedem z trzema, od {E705000} do {E1570000} plus VAT.',
  'Anlegget har 54 boliger, og 13 er oppført med pris: tre med ett soverom, tre med to og sju med tre, fra {E705000} til {E1570000} pluss mva.',
  'Området har 54 bostäder och 13 är listade med pris: tre med ett sovrum, tre med två och sju med tre, från {E705000} till {E1570000} plus IVA.')
p('.faq[1][1]', 'No. The list gives the developer’s net prices',
  'No. La lista da los precios netos del promotor y la ficha informativa añade el IVA a cada plazo. No se indica el tipo, así que confirmamos el tipo y los demás gastos de la compra por escrito.',
  'Non. La liste donne les prix nets du promoteur et la fiche d’information ajoute la TVA à chaque échéance. Le taux n’est pas indiqué ; nous le confirmons, ainsi que les autres frais d’achat, par écrit.',
  'Nein. Die Liste nennt die Nettopreise des Bauträgers, und das Infoblatt schlägt die MwSt. auf jede Rate auf. Der Satz ist nicht angegeben, daher bestätigen wir ihn und die übrigen Kaufnebenkosten schriftlich.',
  'Нет. В списке указаны чистые цены застройщика, а информационный лист добавляет НДС к каждому платежу. Ставка не указана, поэтому мы письменно подтверждаем её и другие расходы на покупку.',
  'لا. تذكر القائمة الأسعار الصافية للمطوّر وتضيف ورقة المعلومات ضريبة القيمة المضافة إلى كل دفعة. ولم تُذكر النسبة، فنؤكدها مع سائر تكاليف الشراء كتابةً.',
  'Nee. De lijst geeft de netto prijzen van de ontwikkelaar en het infoblad rekent btw bij elke termijn. Het tarief staat er niet bij; wij bevestigen het en de overige aankoopkosten schriftelijk.',
  'Nie. Lista podaje ceny netto dewelopera, a karta informacyjna dolicza VAT do każdej raty. Stawka nie jest podana, więc potwierdzamy ją i pozostałe koszty zakupu na piśmie.',
  'Nei. Listen oppgir utbyggerens nettopriser, og infobladet legger mva. til hver termin. Satsen er ikke oppgitt, så vi bekrefter den og de øvrige kjøpskostnadene skriftlig.',
  'Nej. Listan anger exploatörens nettopriser och informationsbladet lägger IVA på varje delbetalning. Satsen anges inte, så vi bekräftar den och de övriga köpkostnaderna skriftligen.')
p('.faq[2][1]', 'The plans of the four ground-floor homes draw a storage room beside the home, and the specification mentions',
  'Los planos de las cuatro viviendas de planta baja dibujan un trastero junto a la vivienda, y la memoria de calidades menciona un aparcamiento con puerta automática. Ningún documento dice si un trastero o una plaza de garaje están incluidos en cada precio, y lo confirmamos.',
  'Les plans des quatre logements du rez-de-chaussée dessinent une cave à côté du logement, et le descriptif technique mentionne un parking avec une porte automatique. Aucun document ne dit si une cave ou une place de garage est comprise dans chaque prix ; nous le confirmons.',
  'Die Pläne der vier Erdgeschosswohnungen zeigen neben der Wohnung einen Abstellraum, und die Baubeschreibung erwähnt eine Garage mit automatischem Tor. Kein Dokument sagt, ob ein Abstellraum oder ein Garagenstellplatz im jeweiligen Preis enthalten ist; wir bestätigen das.',
  'На планах четырёх квартир первого этажа рядом с квартирой нарисована кладовая, а в спецификации упомянута парковка с автоматическими воротами. Ни в одном документе не сказано, входит ли кладовая или место в гараже в каждую цену; мы это уточняем.',
  'تُظهر مخططات المساكن الأربعة في الطابق الأرضي غرفة تخزين بجانب المسكن، وتذكر مواصفات البناء موقف سيارات بباب آلي. ولا تذكر أي وثيقة ما إذا كانت غرفة التخزين أو موقف في المرآب مشمولًا في كل سعر، ونؤكد ذلك.',
  'De plattegronden van de vier woningen op de begane grond tonen naast de woning een berging, en het lastenboek vermeldt een parkeerruimte met een automatische deur. Geen enkel document zegt of een berging of een garageplaats in elke prijs is inbegrepen, en wij bevestigen dat.',
  'Rzuty czterech lokali na parterze pokazują obok lokalu komórkę lokatorską, a specyfikacja techniczna wspomina o parkingu z automatyczną bramą. Żaden dokument nie mówi, czy komórka lokatorska lub miejsce garażowe jest wliczone w każdą cenę, i potwierdzamy to.',
  'Plantegningene av de fire boligene i første etasje viser en bod ved siden av boligen, og beskrivelsen nevner et parkeringsareal med automatisk port. Ingen dokumenter sier om en bod eller en garasjeplass er inkludert i hver pris, og vi bekrefter det.',
  'Planritningarna för de fyra bostäderna på bottenvåningen visar ett förråd intill bostaden, och byggbeskrivningen nämner en parkering med automatisk port. Inget dokument anger om ett förråd eller en garageplats ingår i varje pris, och vi bekräftar det.')
p('.faq[3][0]', 'Do the third-floor homes have a private pool?',
  '¿Las viviendas de la tercera planta tienen piscina privada?', 'Les logements du troisième étage ont-ils une piscine privée ?', 'Haben die Wohnungen im dritten Obergeschoss einen privaten Pool?',
  'Есть ли у квартир на четвёртом этаже частный бассейн?', 'هل في مساكن الطابق الثالث مسبح خاص؟', 'Hebben de woningen op de derde verdieping een privézwembad?',
  'Czy lokale na trzecim piętrze mają prywatny basen?', 'Har boligene i fjerde etasje et eget basseng?', 'Har bostäderna på tredje våningen en egen pool?')
p('.faq[3][1]', 'The plans of the seven listed third-floor homes',
  'Los planos de las siete viviendas listadas de la tercera planta dibujan una pequeña piscina en el solárium, pero la lista de disponibilidad no menciona ninguna. Confirmamos si se construye y está incluida.',
  'Les plans des sept logements listés du troisième étage dessinent un petit bassin sur le solarium, mais la liste de disponibilité n’en mentionne aucun. Nous confirmons s’il est réalisé et compris.',
  'Die Pläne der sieben aufgeführten Wohnungen im dritten Obergeschoss zeigen einen kleinen Pool auf dem Solarium, aber die Verfügbarkeitsliste erwähnt keinen. Wir bestätigen, ob er gebaut wird und enthalten ist.',
  'На планах семи указанных в списке квартир четвёртого этажа на солярии нарисован небольшой бассейн, но в списке наличия он не упомянут. Мы уточняем, будет ли он построен и включён в цену.',
  'تُظهر مخططات المساكن السبعة المدرجة في الطابق الثالث مسبحًا صغيرًا على السولاريوم، لكن قائمة التوفر لا تذكر أي مسبح. ونؤكد ما إذا كان سيُبنى وما إذا كان مشمولًا.',
  'De plattegronden van de zeven vermelde woningen op de derde verdieping tonen een klein zwembad op het solarium, maar de beschikbaarheidslijst vermeldt er geen. We bevestigen of het wordt gebouwd en is inbegrepen.',
  'Rzuty siedmiu wymienionych lokali na trzecim piętrze pokazują niewielki basen na solarium, ale lista dostępności o żadnym nie wspomina. Potwierdzamy, czy zostanie wybudowany i czy jest wliczony.',
  'Plantegningene av de syv oppførte boligene i fjerde etasje viser et lite basseng på solterrassen, men tilgjengelighetslisten nevner ikke noe. Vi bekrefter om det bygges og er inkludert.',
  'Planritningarna för de sju listade bostäderna på tredje våningen visar en liten pool på solterrassen, men tillgänglighetslistan nämner ingen. Vi bekräftar om den byggs och ingår.')
p('.faq[4][1]', 'The infosheet gives the end of construction as expected',
  'La ficha informativa da el fin de obra como previsto para el cuarto trimestre de 2028 y no lleva fecha de emisión, por lo que es una estimación. Preguntamos hasta dónde ha avanzado la obra y pedimos la fecha contractual.',
  'La fiche d’information donne la fin des travaux comme attendue au quatrième trimestre 2028 et ne porte pas de date d’émission ; il s’agit donc d’une estimation. Nous demandons où en est le chantier et la date contractuelle.',
  'Das Infoblatt gibt das Bauende als für das vierte Quartal 2028 erwartet an und trägt kein Ausgabedatum, es ist also eine Schätzung. Wir fragen nach, wie weit der Bau fortgeschritten ist, und nach dem vertraglichen Termin.',
  'В информационном листе окончание строительства ожидается в четвёртом квартале 2028 года, а даты выпуска нет, поэтому это оценка. Мы уточняем, как далеко продвинулась стройка, и запрашиваем договорную дату.',
  'تذكر ورقة المعلومات أن انتهاء الإنشاء متوقع في الربع الرابع من عام 2028 ولا تحمل تاريخ إصدار، فهو إذن تقدير. نستفسر عن مدى تقدّم الأعمال ونطلب الموعد التعاقدي.',
  'Het infoblad geeft het einde van de bouw als verwacht in het vierde kwartaal van 2028 en vermeldt geen uitgiftedatum, dus het is een schatting. We vragen hoe ver de bouw is gevorderd en naar de contractuele datum.',
  'Karta informacyjna podaje zakończenie budowy jako oczekiwane w czwartym kwartale 2028 roku i nie ma daty wydania, więc jest to szacunek. Pytamy, jak daleko zaawansowana jest budowa, i prosimy o termin umowny.',
  'Infobladet oppgir byggeslutt som ventet i fjerde kvartal 2028 og har ingen utstedelsesdato, så det er et anslag. Vi spør hvor langt byggingen har kommet og ber om den kontraktsfestede datoen.',
  'Informationsbladet anger byggslutet som väntat under fjärde kvartalet 2028 och har inget utfärdandedatum, så det är en uppskattning. Vi frågar hur långt bygget har kommit och begär det avtalade datumet.')
p('.faq[5][1]', 'The developer sets a reservation and a staged payment plan. We send',
  'El promotor fija una reserva y un plan de pagos por fases. Le enviamos por escrito los importes y las fechas vigentes antes de que reserve.',
  'Le promoteur prévoit une réservation et un échéancier de paiement par étapes. Nous vous envoyons par écrit les montants et les dates en vigueur avant que vous ne réserviez.',
  'Der Bauträger legt eine Reservierung und einen gestaffelten Zahlungsplan fest. Wir senden Ihnen die aktuellen Beträge und Termine schriftlich, bevor Sie reservieren.',
  'Застройщик устанавливает бронирование и поэтапный график платежей. Мы пришлём вам действующие суммы и даты в письменном виде до бронирования.',
  'يحدد المطوّر مبلغ حجز وخطة دفع على مراحل. نرسل لكم المبالغ والمواعيد الحالية كتابةً قبل أن تحجزوا.',
  'De ontwikkelaar legt een reservering en een gefaseerd betalingsplan vast. Wij sturen u de actuele bedragen en data schriftelijk toe voordat u reserveert.',
  'Deweloper określa rezerwację i etapowy plan płatności. Przed rezerwacją przesyłamy Państwu aktualne kwoty i terminy na piśmie.',
  'Utbyggeren fastsetter en reservasjon og en trinnvis betalingsplan. Vi sender de gjeldende beløpene og datoene skriftlig før reservasjon.',
  'Exploatören anger en reservation och en betalningsplan i etapper. Vi skickar er de aktuella beloppen och datumen skriftligen innan ni reserverar.')

p('.seo.title', 'Arosa - New Apartments',
  'Arosa - Apartamentos nuevos en La Cala de Mijas', 'Arosa - Appartements neufs à La Cala de Mijas', 'Arosa - Neubauwohnungen in La Cala de Mijas',
  'Arosa - новые квартиры в Ла-Кала-де-Михас', 'Arosa - شقق جديدة في لا كالا دي ميخاس', 'Arosa - Nieuwbouwappartementen in La Cala de Mijas',
  'Arosa - Nowe mieszkania w La Cala de Mijas', 'Arosa - Nye leiligheter i La Cala de Mijas', 'Arosa - Nya lägenheter i La Cala de Mijas')
p('.seo.h1', 'Arosa: Apartments with Sea Views',
  'Arosa: apartamentos con vistas al mar en La Cala de Mijas', 'Arosa : appartements avec vue sur la mer à La Cala de Mijas', 'Arosa: Wohnungen mit Meerblick in La Cala de Mijas',
  'Arosa: квартиры с видом на море в Ла-Кала-де-Михас', 'Arosa: شقق بإطلالة على البحر في لا كالا دي ميخاس', 'Arosa: appartementen met zeezicht in La Cala de Mijas',
  'Arosa: mieszkania z widokiem na morze w La Cala de Mijas', 'Arosa: leiligheter med utsikt over havet i La Cala de Mijas', 'Arosa: lägenheter med havsutsikt i La Cala de Mijas')
p('.seo.h1Context', 'Apartments with Sea Views in La Cala',
  'Apartamentos con vistas al mar en La Cala de Mijas', 'Appartements avec vue sur la mer à La Cala de Mijas', 'Wohnungen mit Meerblick in La Cala de Mijas',
  'Квартиры с видом на море в Ла-Кала-де-Михас', 'شقق بإطلالة على البحر في لا كالا دي ميخاس', 'Appartementen met zeezicht in La Cala de Mijas',
  'Mieszkania z widokiem na morze w La Cala de Mijas', 'Leiligheter med utsikt over havet i La Cala de Mijas', 'Lägenheter med havsutsikt i La Cala de Mijas')

# ---- templates: unit references, floors, sizes, plan alt and captions ---------------------------------
FL = json.load(open(f'{SP}/floor_parts.json'))
for u in proj['availability']['units']:
    same(u['reference'])

AND = {'es': ' y ', 'fr': ' et ', 'de': ' und ', 'ru': ' и ', 'ar': ' و', 'nl': ' en ', 'pl': ' i ', 'no': ' og ', 'sv': ' och '}


def low(s, l):
    return s if l in ('de', 'ar') else s[0].lower() + s[1:]


def floor_label(src, l):
    m = re.fullmatch(r'Portal (\d), (Ground floor|First floor|Third floor)( & solarium)?', src)
    assert m, src
    n, fl, sol = m.groups()
    sep = '، ' if l == 'ar' else ', '
    out = f"{FL['prefixes']['portal'][l]} {n}{sep}{low(FL['parts'][fl.lower()][l], l)}"
    if sol:
        out += AND[l] + ('السولاريوم' if l == 'ar' else low(FL['parts']['solarium'][l], l))
        if l == 'ar':
            out = out.replace(' والسولاريوم', ' والسولاريوم')
    return out


SIZE = {
    'es': ('{b} {U} construidos', '{i} {U} interiores', '{t} {U} de terraza', '{g} {U} de jardín', '{s} {U} de solárium'),
    'fr': ('{b} {U} construits', '{i} {U} intérieurs', '{t} {U} de terrasse', '{g} {U} de jardin', '{s} {U} de solarium'),
    'de': ('{b} {U} bebaut', '{i} {U} Innenfläche', '{t} {U} Terrasse', '{g} {U} Garten', '{s} {U} Solarium'),
    'ru': ('{b} {U} застроенной площади', '{i} {U} внутри', 'терраса {t} {U}', 'сад {g} {U}', 'солярий {s} {U}'),
    'ar': ('{b} {U} مبنية', '{i} {U} داخلية', '{t} {U} تراس', '{g} {U} حديقة', '{s} {U} سولاريوم'),
    'nl': ('{b} {U} bebouwd', '{i} {U} binnen', '{t} {U} terras', '{g} {U} tuin', '{s} {U} solarium'),
    'pl': ('{b} {U} zabudowy', '{i} {U} wnętrza', '{t} {U} tarasu', '{g} {U} ogrodu', '{s} {U} solarium'),
    'no': ('{b} {U} bebygd areal', '{i} {U} innvendig', '{t} {U} terrasse', '{g} {U} hage', '{s} {U} solterrasse'),
    'sv': ('{b} {U} byggyta', '{i} {U} inomhus', '{t} {U} terrass', '{g} {U} trädgård', '{s} {U} solterrass'),
}
for u in proj['availability']['units']:
    if u['floor'] not in T:
        T[u['floor']] = {l: floor_label(u['floor'], l) for l in LOCS}
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm interior, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm (garden|solarium))?', u['size'])
    assert m, u['size']
    b, i, t, x, kind = m.groups()
    out = {}
    for l in LOCS:
        s = SIZE[l]
        parts = [s[0].format(b='{N%s}' % b, U='{U}'), s[1].format(i='{N%s}' % i, U='{U}'), s[2].format(t='{N%s}' % t, U='{U}')]
        if x:
            parts.append((s[3] if kind == 'garden' else s[4]).format(g='{N%s}' % x, s='{N%s}' % x, U='{U}'))
        out[l] = ('، ' if l == 'ar' else ', ').join(parts)
    T[u['size']] = {l: expand(out[l], l) for l in LOCS}

HOME = {'es': 'Vivienda', 'fr': 'Logement', 'de': 'Wohnung', 'ru': 'Квартира', 'ar': 'المسكن', 'nl': 'Woning', 'pl': 'Lokal', 'no': 'Bolig', 'sv': 'Bostad'}
PLAN = {'es': 'Plano de la vivienda', 'fr': 'Plan du logement', 'de': 'Grundriss der Wohnung', 'ru': 'Планировка квартиры', 'ar': 'مخطط المسكن',
        'nl': 'Plattegrond van woning', 'pl': 'Rzut lokalu', 'no': 'Plantegning av bolig', 'sv': 'Planritning för bostad'}
for it in proj['media']['items']:
    if it.get('category') != 'Floorplans':
        continue
    m = re.fullmatch(r'Home (\d\.\d\.[A-Z])', it['caption'])
    assert m, it['caption']
    ref = m.group(1)
    T[it['caption']] = {l: f'{HOME[l]} {ref}' for l in LOCS}
    T[it['alt']] = {l: f'{PLAN[l]} {ref}' for l in LOCS}

json.dump(T, open(f'{SP}/tr_n.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
