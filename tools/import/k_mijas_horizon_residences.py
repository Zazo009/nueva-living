# -*- coding: utf-8 -*-
"""Mijas Horizon Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E365000}
money, {N66.86} decimal number, {N13,000} grouped number, {U} the area unit, {T} the tax word.
    python3 tools/import/k_mijas_horizon_residences.py <scratch dir>   (writes <dir>/tr_a.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة',
        'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
T = {}
SLUG = 'mijas-horizon-residences'
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


same('Mijas Horizon Residences'); same('Mijas Horizon'); same('Mijas Horizon <em>Residences</em>')
same('Gran Parque de la Costa del Sol'); same('Cerrado del Águila Golf Resort')
for u in proj['availability']['units']:
    same(u['reference'])

# ---- description, SEO, card ------------------------------------------------------------------

a('.description',
  'Setenta y cinco viviendas de dos y tres dormitorios en Mijas Costa, con piscina central, gimnasio, club social y más de {N13,000} {U} de jardines. Tres figuran como disponibles en la lista de precios del promotor, desde {E365000} antes de {T}.',
  'Soixante-quinze logements de deux et trois chambres à Mijas Costa, avec piscine centrale, salle de sport, club social et plus de {N13,000} {U} de jardins. Trois figurent comme disponibles sur la liste de prix du promoteur, à partir de {E365000} hors {T}.',
  'Fünfundsiebzig Wohnungen mit zwei und drei Schlafzimmern in Mijas Costa, mit zentralem Pool, Fitnessraum, Social Club und mehr als {N13,000} {U} Gärten. Drei sind in der Preisliste des Bauträgers als verfügbar geführt, ab {E365000} vor {T}.',
  'Семьдесят пять квартир с двумя и тремя спальнями в Михас-Коста: центральный бассейн, тренажёрный зал, клуб для жильцов и сады площадью более {N13,000} {U}. Три указаны в прайс-листе застройщика как доступные, от {E365000} без {T}.',
  'خمسة وسبعون مسكناً بغرفتي نوم وثلاث غرف نوم في ميخاس كوستا، مع مسبح مركزي وصالة رياضية ونادٍ اجتماعي وحدائق تزيد مساحتها على {N13,000} {U}. ثلاثة منها مدرجة على أنها متاحة في قائمة أسعار المطوّر، ابتداءً من {E365000} قبل {T}.',
  'Vijfenzeventig woningen met twee en drie slaapkamers in Mijas Costa, met een centraal zwembad, een fitnessruimte, een sociale club en meer dan {N13,000} {U} tuinen. Drie staan als beschikbaar op de prijslijst van de ontwikkelaar, vanaf {E365000} vóór {T}.',
  'Siedemdziesiąt pięć lokali z dwiema i trzema sypialniami w Mijas Costa, z centralnym basenem, siłownią, klubem dla mieszkańców i ogrodami o powierzchni ponad {N13,000} {U}. Trzy figurują w cenniku dewelopera jako dostępne, od {E365000} przed {T}.',
  'Syttifem boliger med to og tre soverom i Mijas Costa, med sentralt basseng, treningsrom, sosial klubb og mer enn {N13,000} {U} hager. Tre er oppført som ledige i utbyggerens prisliste, fra {E365000} før {T}.',
  'Sjuttiofem bostäder med två och tre sovrum i Mijas Costa, med en central pool, ett gym, en social klubb och mer än {N13,000} {U} trädgårdar. Tre finns med som lediga i exploatörens prislista, från {E365000} före {T} (spansk moms).')
a('.seoDescription',
  'Apartamentos y áticos nuevos de dos y tres dormitorios con terrazas en Mijas Costa, con piscina, gimnasio y club social. Tres figuran como disponibles desde {E365000} más {T}.',
  'Appartements et penthouses neufs de deux et trois chambres avec terrasses à Mijas Costa, avec piscine, salle de sport et club social. Trois indiqués comme disponibles à partir de {E365000} hors {T}.',
  'Neue Wohnungen und Penthouses mit zwei und drei Schlafzimmern und Terrassen in Mijas Costa, mit Pool, Fitnessraum und Social Club. Drei als verfügbar aufgeführt, ab {E365000} zuzüglich {T}.',
  'Новые апартаменты и пентхаусы с двумя и тремя спальнями и террасами в Михас-Коста, с бассейном, тренажёрным залом и клубом для жильцов. Три указаны как доступные, от {E365000} плюс {T}.',
  'شقق وبنتهاوس جديدة بغرفتي نوم وثلاث غرف نوم مع تراسات في ميخاس كوستا، مع مسبح وصالة رياضية ونادٍ اجتماعي. ثلاثة منها مدرجة على أنها متاحة ابتداءً من {E365000} زائد {T}.',
  'Nieuwe appartementen en penthouses met twee en drie slaapkamers en terrassen in Mijas Costa, met zwembad, fitnessruimte en sociale club. Drie vermeld als beschikbaar, vanaf {E365000} plus {T}.',
  'Nowe apartamenty i penthouse’y z dwiema i trzema sypialniami oraz tarasami w Mijas Costa, z basenem, siłownią i klubem dla mieszkańców. Trzy podane jako dostępne, od {E365000} plus {T}.',
  'Nye leiligheter og toppleiligheter med to og tre soverom og terrasser i Mijas Costa, med basseng, treningsrom og sosial klubb. Tre oppført som ledige, fra {E365000} pluss {T}.',
  'Nya lägenheter och takvåningar med två och tre sovrum och terrasser i Mijas Costa, med pool, gym och social klubb. Tre angivna som lediga, från {E365000} plus {T}.')
a('.twitterDescription',
  'Viviendas de dos y tres dormitorios con terrazas en Mijas Costa, desde {E365000} más {T}.',
  'Logements de deux et trois chambres avec terrasses à Mijas Costa, à partir de {E365000} hors {T}.',
  'Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Mijas Costa, ab {E365000} zuzüglich {T}.',
  'Квартиры с двумя и тремя спальнями и террасами в Михас-Коста, от {E365000} плюс {T}.',
  'مساكن بغرفتي نوم وثلاث غرف نوم مع تراسات في ميخاس كوستا، ابتداءً من {E365000} زائد {T}.',
  'Woningen met twee en drie slaapkamers en terrassen in Mijas Costa, vanaf {E365000} plus {T}.',
  'Lokale z dwiema i trzema sypialniami oraz tarasami w Mijas Costa, od {E365000} plus {T}.',
  'Boliger med to og tre soverom og terrasser i Mijas Costa, fra {E365000} pluss {T}.',
  'Bostäder med två och tre sovrum och terrasser i Mijas Costa, från {E365000} plus {T}.')
a('.card.description',
  'Viviendas de dos y tres dormitorios con terrazas en una promoción de 75 viviendas en Mijas Costa, con piscina central, gimnasio y club social.',
  'Logements de deux et trois chambres avec terrasses dans un ensemble de 75 logements à Mijas Costa, avec piscine centrale, salle de sport et club social.',
  'Wohnungen mit zwei und drei Schlafzimmern und Terrassen in einer Anlage mit 75 Wohnungen in Mijas Costa, mit zentralem Pool, Fitnessraum und Social Club.',
  'Квартиры с двумя и тремя спальнями и террасами в комплексе из 75 квартир в Михас-Коста, с центральным бассейном, тренажёрным залом и клубом для жильцов.',
  'مساكن بغرفتي نوم وثلاث غرف نوم مع تراسات في مشروع من 75 مسكناً في ميخاس كوستا، مع مسبح مركزي وصالة رياضية ونادٍ اجتماعي.',
  'Woningen met twee en drie slaapkamers en terrassen in een project van 75 woningen in Mijas Costa, met een centraal zwembad, een fitnessruimte en een sociale club.',
  'Lokale z dwiema i trzema sypialniami oraz tarasami w inwestycji obejmującej 75 lokali w Mijas Costa, z centralnym basenem, siłownią i klubem dla mieszkańców.',
  'Boliger med to og tre soverom og terrasser i et prosjekt med 75 boliger i Mijas Costa, med sentralt basseng, treningsrom og sosial klubb.',
  'Bostäder med två och tre sovrum och terrasser i ett projekt med 75 bostäder i Mijas Costa, med en central pool, ett gym och en social klubb.')

# ---- images, media ---------------------------------------------------------------------------

a('.images.hero.alt',
  'Vista generada por ordenador a través de la piscina comunitaria y sus tumbonas hacia un bloque de terrazas escalonadas con barandillas de cristal, con palmeras y un paisaje ondulado al fondo',
  'Vue générée par ordinateur à travers la piscine commune et ses transats vers un bloc de terrasses en gradins à garde-corps en verre, avec des palmiers et un paysage vallonné à l’arrière-plan',
  'Computergenerierte Ansicht über den Gemeinschaftspool und seine Liegen auf einen Block mit gestaffelten Terrassen und Glasbrüstungen, dahinter Palmen und eine Hügellandschaft',
  'Компьютерная визуализация: вид через общий бассейн с шезлонгами на корпус со ступенчатыми террасами и стеклянными ограждениями, позади пальмы и холмистый пейзаж',
  'منظر مولَّد بالحاسوب عبر المسبح المشترك ومقاعده الطويلة نحو مبنى بتراسات متدرّجة وحواجز زجاجية، وخلفه نخيل ومناظر تلال متموّجة',
  'Computergegenereerd beeld over het gemeenschappelijke zwembad en de ligbedden naar een blok met trapsgewijze terrassen en glazen balustrades, met palmen en een glooiend landschap erachter',
  'Wygenerowany komputerowo widok przez wspólny basen i leżaki na blok z tarasami schodkowymi i szklanymi balustradami, z palmami i pofałdowanym krajobrazem w tle',
  'Datagenerert bilde over fellesbassenget og solsengene mot en blokk med trappede terrasser og glassrekkverk, med palmer og et kupert landskap bak',
  'Datorgenererad vy över den gemensamma poolen och solstolarna mot ett hus med trappade terrasser och glasräcken, med palmer och ett böljande landskap bakom')
a('.images.architecture.alt',
  'Vista generada por ordenador de una tarima de madera con un hogar hundido, la piscina y las tumbonas detrás y bloques crema y gris con balcones alrededor de un césped',
  'Vue générée par ordinateur d’un deck en bois avec un foyer encastré, la piscine et les transats au-delà et des blocs crème et gris avec balcons autour d’une pelouse',
  'Computergenerierte Ansicht eines Holzdecks mit versenkter Feuerstelle, dahinter Pool und Liegen sowie cremefarbene und graue Blöcke mit Balkonen rund um einen Rasen',
  'Компьютерная визуализация: деревянный настил с углублённым очагом, за ним бассейн и шезлонги, вокруг газона кремовые и серые корпуса с балконами',
  'منظر مولَّد بالحاسوب لسطح خشبي فيه موقد نار غائر، وخلفه المسبح ومقاعده الطويلة، وحول مرج أخضر مبانٍ بلونَي الكريمي والرمادي بشرفات',
  'Computergegenereerd beeld van een houten terrasvloer met een verzonken vuurplaats, daarachter het zwembad en de ligbedden en crèmekleurige en grijze blokken met balkons rond een gazon',
  'Wygenerowany komputerowo widok drewnianego podestu z zagłębionym paleniskiem, za nim basen i leżaki oraz kremowo-szare bloki z balkonami wokół trawnika',
  'Datagenerert bilde av et tredekk med nedsenket bålpanne, bassenget og solsengene bak og kremfargede og grå blokker med balkonger rundt en plen',
  'Datorgenererad vy av ett trädäck med en nedsänkt eldstad, med poolen och solstolarna bakom och krämfärgade och grå hus med balkonger kring en gräsmatta')
a('.images.lifestyle.alt',
  'Vista generada por ordenador del club social, una sala larga con dos mesas de comedor de madera, butacas, una encimera de cocina y una apertura acristalada a una terraza',
  'Vue générée par ordinateur du club social, une longue salle avec deux tables à manger en bois, des fauteuils, un plan de cuisine et une ouverture vitrée sur une terrasse',
  'Computergenerierte Ansicht des Social Clubs, eines langen Raums mit zwei Holzesstischen, Sesseln, einer Küchenzeile und einer verglasten Öffnung zu einer Terrasse',
  'Компьютерная визуализация клуба для жильцов: длинный зал с двумя деревянными обеденными столами, креслами, кухонной стойкой и остеклённым выходом на террасу',
  'منظر مولَّد بالحاسوب للنادي الاجتماعي، وهو قاعة طويلة فيها طاولتا طعام خشبيتان ومقاعد وثيرة ومنضدة مطبخ وفتحة زجاجية على تراس',
  'Computergegenereerd beeld van de sociale club, een lange ruimte met twee houten eettafels, fauteuils, een keukenblok en een glazen opening naar een terras',
  'Wygenerowany komputerowo widok klubu dla mieszkańców, długiego pomieszczenia z dwoma drewnianymi stołami jadalnianymi, fotelami, blatem kuchennym i przeszklonym wyjściem na taras',
  'Datagenerert bilde av den sosiale klubben, et langt rom med to spiseborder i tre, lenestoler, en kjøkkenbenk og en glassåpning mot en terrasse',
  'Datorgenererad vy av den sociala klubben, ett långt rum med två matbord i trä, fåtöljer, en köksbänk och en glasad öppning mot en terrass')
a('.images.privateViewing.alt',
  'Vista generada por ordenador de una terraza con un sofá de exterior, una mesa de comedor y una sombrilla, con vistas a colinas arboladas y al mar',
  'Vue générée par ordinateur d’une terrasse avec un canapé lounge, une table à manger et un parasol, donnant sur des collines boisées et la mer',
  'Computergenerierte Ansicht einer Terrasse mit Loungesofa, Esstisch und Sonnenschirm mit Blick über bewaldete Hügel zum Meer',
  'Компьютерная визуализация террасы с диваном, обеденным столом и зонтом, вид на лесистые холмы и море',
  'منظر مولَّد بالحاسوب لتراس فيه أريكة جلوس وطاولة طعام ومظلة، يطل على تلال مشجّرة والبحر',
  'Computergegenereerd beeld van een terras met een loungebank, een eettafel en een parasol, met uitzicht over beboste heuvels naar de zee',
  'Wygenerowany komputerowo widok tarasu z sofą wypoczynkową, stołem jadalnianym i parasolem, z widokiem na zalesione wzgórza i morze',
  'Datagenerert bilde av en terrasse med loungesofa, spisebord og parasoll, med utsikt over skogkledde åser til sjøen',
  'Datorgenererad vy av en terrass med loungesoffa, matbord och parasoll, med utsikt över skogsklädda kullar mot havet')
a('.media.copy',
  'Vistas generadas por ordenador de los bloques, la piscina, las terrazas y los interiores, una vista aérea del solar y los planos de las tres viviendas de la lista de precios.',
  'Vues générées par ordinateur des blocs, de la piscine, des terrasses et des intérieurs, une vue aérienne du terrain et les plans des trois logements de la liste de prix.',
  'Computergenerierte Ansichten der Blöcke, des Pools, der Terrassen und der Innenräume, eine Luftaufnahme des Grundstücks und die Grundrisse der drei Wohnungen der Preisliste.',
  'Компьютерные визуализации корпусов, бассейна, террас и интерьеров, вид участка с воздуха и планировки трёх квартир из прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمباني والمسبح والتراسات والمساحات الداخلية، ومنظر جوي للموقع، ومخططات المساكن الثلاثة الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van de blokken, het zwembad, de terrassen en de interieurs, een luchtfoto van het terrein en de plattegronden van de drie woningen op de prijslijst.',
  'Wygenerowane komputerowo widoki bloków, basenu, tarasów i wnętrz, widok terenu z lotu ptaka oraz rzuty trzech lokali z cennika.',
  'Datagenererte bilder av blokkene, bassenget, terrassene og interiørene, et flyfoto av tomten og plantegningene for de tre boligene i prislisten.',
  'Datorgenererade vyer av husen, poolen, terrasserna och interiörerna, en flygvy över tomten och planritningarna för de tre bostäderna i prislistan.')
a('.media.note',
  'Las imágenes están generadas por ordenador, salvo la vista aérea, en la que los edificios previstos se añaden a una fotografía del solar. El mobiliario, la decoración y la vegetación que muestran son ilustrativos y no están incluidos. Los planos son los planos de proyecto del promotor de abril de 2024, sin los logotipos del promotor; las superficies que figuran en ellos son aproximadas y están sujetas al proyecto final, y los nombres de las estancias están en inglés.',
  'Les images sont générées par ordinateur, à l’exception de la vue aérienne, où les bâtiments prévus sont ajoutés à une photographie du terrain. Le mobilier, la décoration et la végétation qu’elles montrent sont illustratifs et ne sont pas inclus. Les plans sont les plans de projet du promoteur d’avril 2024, sans les logos du promoteur ; les surfaces qui y figurent sont approximatives et soumises au projet définitif, et les noms des pièces y sont en anglais.',
  'Die Bilder sind computergeneriert, mit Ausnahme der Luftaufnahme, in der die geplanten Gebäude in ein Foto des Grundstücks eingefügt sind. Möblierung, Dekoration und Bepflanzung darin sind Illustration und nicht enthalten. Die Grundrisse sind die Entwurfspläne des Bauträgers vom April 2024, ohne die Logos des Bauträgers; die darin angegebenen Flächen sind ungefähre Werte und stehen unter dem Vorbehalt des endgültigen Projekts, die Raumbezeichnungen sind auf Englisch.',
  'Изображения созданы на компьютере, кроме вида с воздуха, на котором проектные здания добавлены к фотографии участка. Мебель, оформление и озеленение на них — иллюстрация и в стоимость не входят. Планировки — проектные планы застройщика от апреля 2024 года, без логотипов застройщика; указанные на них площади приблизительны и зависят от окончательного проекта, названия помещений даны на английском.',
  'الصور مولَّدة بالحاسوب، باستثناء المنظر الجوي الذي أُضيفت فيه المباني المخطط لها إلى صورة فوتوغرافية للموقع. أما الأثاث والديكور والمزروعات فيها فللتوضيح فقط وغير مشمولة. المخططات هي مخططات مرحلة المشروع الصادرة عن المطوّر في أبريل 2024، بعد إزالة شعارات المطوّر منها؛ والمساحات الواردة عليها تقريبية وخاضعة للمشروع النهائي، وأسماء الغرف فيها بالإنجليزية.',
  'De beelden zijn computergegenereerd, behalve de luchtfoto, waarin de geplande gebouwen aan een foto van het terrein zijn toegevoegd. Het meubilair, de inrichting en de beplanting erop zijn illustratief en niet inbegrepen. De plattegronden zijn de projectplannen van de ontwikkelaar van april 2024, zonder de logo’s van de ontwikkelaar; de oppervlakten erop zijn bij benadering en onder voorbehoud van het definitieve project, en de ruimtenamen staan in het Engels.',
  'Obrazy są wygenerowane komputerowo, z wyjątkiem widoku z lotu ptaka, na którym planowane budynki dodano do fotografii terenu. Meble, wystrój i roślinność na nich mają charakter ilustracyjny i nie są wliczone. Rzuty to plany projektowe dewelopera z kwietnia 2024 roku, bez logo dewelopera; podane na nich powierzchnie są przybliżone i zależą od ostatecznego projektu, a nazwy pomieszczeń są po angielsku.',
  'Bildene er datagenererte, bortsett fra flyfotoet, der de planlagte byggene er lagt inn i et fotografi av tomten. Møbler, dekor og beplantning på dem er illustrasjoner og ikke inkludert. Plantegningene er utbyggerens prosjektplaner fra april 2024, uten utbyggerens logoer; arealene på dem er omtrentlige og avhenger av det endelige prosjektet, og romnavnene er på engelsk.',
  'Bilderna är datorgenererade, utom flygvyn, där de planerade husen har lagts in i ett fotografi av tomten. Möbler, inredning och växtlighet på dem är illustrationer och ingår inte. Planritningarna är exploatörens projektplaner från april 2024, utan exploatörens logotyper; ytorna på dem är ungefärliga och beroende av det slutliga projektet, och rumsnamnen är på engelska.')
a('.media.items[1].caption',
  'La tarima, el hogar y la piscina', 'Le deck, le foyer et la piscine', 'Das Deck, die Feuerstelle und der Pool',
  'Настил, очаг и бассейн', 'السطح الخشبي وموقد النار والمسبح', 'De terrasvloer, de vuurplaats en het zwembad',
  'Podest, palenisko i basen', 'Dekket, bålpannen og bassenget', 'Däcket, eldstaden och poolen')
a('.media.items[2].alt',
  'Vista aérea del solar con los edificios previstos añadidos, una piscina junto al bloque más cercano, un hipódromo y el mar a lo lejos',
  'Vue aérienne du terrain avec les bâtiments prévus ajoutés, une piscine à côté du bloc le plus proche, un hippodrome et la mer au loin',
  'Luftaufnahme des Grundstücks mit den geplanten Gebäuden, einem Pool neben dem nächstgelegenen Block, einer Pferderennbahn und dem Meer in der Ferne',
  'Вид с воздуха на участок с добавленными проектными зданиями, бассейном рядом с ближайшим корпусом, ипподромом и морем вдали',
  'منظر جوي للموقع مع إضافة المباني المخطط لها، ومسبح بجوار أقرب مبنى، وحلبة سباق خيل، والبحر في البعيد',
  'Luchtfoto van het terrein met de geplande gebouwen toegevoegd, een zwembad naast het dichtstbijzijnde blok, een renbaan en in de verte de zee',
  'Widok z lotu ptaka na teren z dodanymi planowanymi budynkami, basenem obok najbliższego bloku, torem wyścigowym i morzem w oddali',
  'Flyfoto av tomten med de planlagte byggene lagt til, et basseng ved siden av den nærmeste blokken, en hesteveddeløpsbane og havet i det fjerne',
  'Flygvy över tomten med de planerade husen inlagda, en pool intill det närmaste huset, en galoppbana och havet i fjärran')
a('.media.items[4].alt',
  'Salón generado por ordenador con un sofá y dos sillones redondos, una puerta corredera de cristal a una terraza cubierta y la costa al fondo',
  'Séjour généré par ordinateur avec un canapé et deux fauteuils ronds, une porte coulissante vitrée donnant sur une terrasse couverte et la côte au loin',
  'Computergenerierter Wohnraum mit Sofa und zwei runden Sesseln, einer gläsernen Schiebetür zu einer überdachten Terrasse und der Küste dahinter',
  'Компьютерная визуализация гостиной с диваном и двумя круглыми креслами, стеклянной раздвижной дверью на крытую террасу и побережьем вдали',
  'غرفة معيشة مولَّدة بالحاسوب فيها أريكة ومقعدان مستديران، وباب زجاجي منزلق إلى تراس مسقوف، والساحل في البعيد',
  'Computergegenereerde woonkamer met een bank en twee ronde fauteuils, een glazen schuifdeur naar een overdekt terras en de kust op de achtergrond',
  'Wygenerowany komputerowo salon z sofą i dwoma okrągłymi fotelami, szklanymi drzwiami przesuwnymi na zadaszony taras i wybrzeżem w tle',
  'Datagenerert stue med en sofa og to runde lenestoler, en skyvedør i glass til en overdekket terrasse og kysten bak',
  'Datorgenererat vardagsrum med en soffa och två runda fåtöljer, en skjutdörr i glas till en övertäckt terrass och kusten bortom')
a('.media.items[5].alt',
  'Salón generado por ordenador con una pared de listones para el televisor, un sofá y sillones, y una puerta corredera a una terraza con vistas al mar',
  'Séjour généré par ordinateur avec un mur télévision à lames, un canapé et des fauteuils, et une porte coulissante donnant sur une terrasse avec vue sur la mer',
  'Computergenerierter Wohnraum mit einer Fernsehwand aus Holzlamellen, Sofa und Sesseln sowie einer Schiebetür zu einer Terrasse mit Meerblick',
  'Компьютерная визуализация гостиной со стеной для телевизора из реек, диваном и креслами и раздвижной дверью на террасу с видом на море',
  'غرفة معيشة مولَّدة بالحاسوب فيها جدار تلفزيون بألواح خشبية متوازية وأريكة ومقاعد، وباب منزلق إلى تراس بإطلالة على البحر',
  'Computergegenereerde woonkamer met een televisiewand van latten, een bank en fauteuils en een schuifdeur naar een terras met zeezicht',
  'Wygenerowany komputerowo salon z listwową ścianą telewizyjną, sofą i fotelami oraz drzwiami przesuwnymi na taras z widokiem na morze',
  'Datagenerert stue med en TV-vegg av lister, en sofa og lenestoler, og en skyvedør til en terrasse med havutsikt',
  'Datorgenererat vardagsrum med en tv-vägg av spjälor, en soffa och fåtöljer samt en skjutdörr till en terrass med havsutsikt')
a('.media.items[5].caption',
  'Salón con la pared del televisor', 'Séjour avec le mur télévision', 'Wohnzimmer mit der Fernsehwand',
  'Гостиная со стеной для телевизора', 'غرفة المعيشة مع جدار التلفزيون', 'Woonkamer met de televisiewand',
  'Salon ze ścianą telewizyjną', 'Stue med TV-veggen', 'Vardagsrum med tv-väggen')
a('.media.items[6].alt',
  'Cocina abierta generada por ordenador con muebles blancos y una mesa de comedor ovalada con sillas tapizadas',
  'Cuisine ouverte générée par ordinateur avec des meubles blancs et une table à manger ovale avec des chaises rembourrées',
  'Computergenerierte offene Küche mit weißen Fronten und einem ovalen Esstisch mit gepolsterten Stühlen',
  'Компьютерная визуализация открытой кухни с белыми фасадами и овальным обеденным столом с мягкими стульями',
  'مطبخ مفتوح مولَّد بالحاسوب بخزائن بيضاء وطاولة طعام بيضاوية مع كراسٍ منجّدة',
  'Computergegenereerde open keuken met witte kasten en een ovale eettafel met beklede stoelen',
  'Wygenerowana komputerowo otwarta kuchnia z białymi szafkami i owalnym stołem jadalnianym z tapicerowanymi krzesłami',
  'Datagenerert åpent kjøkken med hvite skap og et ovalt spisebord med polstrede stoler',
  'Datorgenererat öppet kök med vita skåp och ett ovalt matbord med stoppade stolar')
a('.media.items[7].alt',
  'Dormitorio generado por ordenador con una cama doble contra una pared cabecero de listones de madera y una puerta corredera de cristal a una terraza',
  'Chambre générée par ordinateur avec un lit double contre un mur tête de lit en lames de bois et une porte coulissante vitrée donnant sur une terrasse',
  'Computergeneriertes Schlafzimmer mit einem Doppelbett vor einer Kopfteilwand aus Holzlamellen und einer gläsernen Schiebetür zu einer Terrasse',
  'Компьютерная визуализация спальни с двуспальной кроватью у стены с изголовьем из деревянных реек и стеклянной раздвижной дверью на террасу',
  'غرفة نوم مولَّدة بالحاسوب فيها سرير مزدوج أمام جدار رأس السرير من ألواح خشبية متوازية، وباب زجاجي منزلق إلى تراس',
  'Computergegenereerde slaapkamer met een tweepersoonsbed tegen een hoofdbordwand van houten latten en een glazen schuifdeur naar een terras',
  'Wygenerowana komputerowo sypialnia z łóżkiem dwuosobowym przy ścianie z zagłówkiem z drewnianych listew i szklanymi drzwiami przesuwnymi na taras',
  'Datagenerert soverom med en dobbeltseng mot en hodegavlvegg av trelister og en skyvedør i glass til en terrasse',
  'Datorgenererat sovrum med en dubbelsäng mot en sänggavelvägg av träspjälor och en skjutdörr i glas till en terrass')
a('.media.items[8].alt',
  'Baño generado por ordenador con una ducha a ras de suelo, un mueble suspendido con lavabo sobre encimera y un espejo redondo',
  'Salle de bain générée par ordinateur avec une douche à l’italienne, un meuble suspendu avec vasque à poser et un miroir rond',
  'Computergeneriertes Badezimmer mit bodengleicher Dusche, einem wandhängenden Waschtisch mit Aufsatzbecken und einem runden Spiegel',
  'Компьютерная визуализация ванной комнаты с душем без поддона, подвесной тумбой с накладной раковиной и круглым зеркалом',
  'حمّام مولَّد بالحاسوب فيه دش مفتوح وخزانة معلّقة بحوض فوق سطحها ومرآة مستديرة',
  'Computergegenereerde badkamer met een inloopdouche, een wandmeubel met opzetwastafel en een ronde spiegel',
  'Wygenerowana komputerowo łazienka z prysznicem bez brodzika, szafką podwieszaną z umywalką nablatową i okrągłym lustrem',
  'Datagenerert bad med en dusj uten kant, en veggmontert servantskap med opplagt vask og et rundt speil',
  'Datorgenererat badrum med en duschhörna utan tröskel, ett väggmonterat tvättställsskåp med ett ovanpåliggande handfat och en rund spegel')
a('.media.items[10].alt',
  'Vista generada por ordenador del gimnasio con cintas de correr y bicicletas estáticas, una pared de listones de madera y puertas acristaladas a una terraza y al mar',
  'Vue générée par ordinateur de la salle de sport avec tapis de course et vélos d’exercice, un mur en lames de bois et des portes vitrées donnant sur une terrasse et la mer',
  'Computergenerierte Ansicht des Fitnessraums mit Laufbändern und Fahrradergometern, einer Holzlamellenwand und verglasten Türen zu einer Terrasse und zum Meer',
  'Компьютерная визуализация тренажёрного зала с беговыми дорожками и велотренажёрами, стеной из деревянных реек и остеклёнными дверями на террасу и к морю',
  'منظر مولَّد بالحاسوب للصالة الرياضية فيها أجهزة مشي ودرّاجات تمرين وجدار من ألواح خشبية وأبواب زجاجية تطل على تراس والبحر',
  'Computergegenereerd beeld van de fitnessruimte met loopbanden en hometrainers, een wand van houten latten en glazen deuren naar een terras en de zee',
  'Wygenerowany komputerowo widok siłowni z bieżniami i rowerami treningowymi, ścianą z drewnianych listew i przeszklonymi drzwiami na taras i w stronę morza',
  'Datagenerert bilde av treningsrommet med tredemøller og mosjonssykler, en vegg av trelister og glassdører mot en terrasse og havet',
  'Datorgenererad vy av gymmet med löpband och motionscyklar, en vägg av träspjälor och glasdörrar mot en terrass och havet')

# ---- unit rows and plan labels, built from the numbers the English was built from ----------------

INNER = {'es': 'm² interiores', 'fr': 'm² intérieurs', 'de': 'm² Innenfläche', 'ru': 'м² внутри',
         'ar': 'م² داخلية', 'nl': 'm² binnen', 'pl': 'm² wnętrza', 'no': 'm² innvendig', 'sv': 'm² inomhus'}
TERR = {'es': 'm² de terraza', 'fr': 'm² de terrasse', 'de': 'm² Terrasse', 'ru': 'терраса {} м²',
        'ar': 'م² تراس', 'nl': 'm² terras', 'pl': 'm² tarasu', 'no': 'm² terrasse', 'sv': 'm² terrass'}
SEP = {l: ', ' for l in LOCS}; SEP['ar'] = '، '


def dec2(x, loc):
    return f'{x:.2f}'.replace('.', '.' if loc == 'ar' else ',')


def size(inner, terr, loc):
    t = TERR[loc]
    terr_part = t.format(dec2(terr, loc)) if '{}' in t else f'{dec2(terr, loc)} {t}'
    return SEP[loc].join([f'{dec2(inner, loc)} {INNER[loc]}', terr_part])


for i, n, t in [(0, 66.86, 24.89), (1, 84.52, 18.87), (2, 73.46, 37.03)]:
    en = get(f'.availability.units[{i}].size')
    assert en == f'{n} sqm interior, {t} sqm terrace', en
    T[en] = {l: size(n, t, l) for l in LOCS}

PLAN_ALT = {'es': 'Plano de la vivienda {}', 'fr': 'Plan du logement {}', 'de': 'Grundriss der Wohnung {}',
            'ru': 'Планировка квартиры {}', 'ar': 'مخطط المسكن {}', 'nl': 'Plattegrond van woning {}',
            'pl': 'Rzut lokalu {}', 'no': 'Plantegning av bolig {}', 'sv': 'Planritning för bostad {}'}
PLAN_CAP = {'es': 'Vivienda {}', 'fr': 'Logement {}', 'de': 'Wohnung {}', 'ru': 'Квартира {}',
            'ar': 'المسكن {}', 'nl': 'Woning {}', 'pl': 'Lokal {}', 'no': 'Bolig {}', 'sv': 'Bostad {}'}
n_plan = 0
for it in proj['media']['items']:
    for key, tpl, rx in (('alt', PLAN_ALT, r'Floorplan of home ([\w-]+)'), ('caption', PLAN_CAP, r'Home ([\w-]+)')):
        m = re.fullmatch(rx, it.get(key, ''))
        if m:
            T[it[key]] = {l: tpl[l].format(m.group(1)) for l in LOCS}
            n_plan += 1
assert n_plan == 6, n_plan

# ---- overview, why, architecture -------------------------------------------------------------

a('.overview.headlineHtml',
  'Setenta y cinco viviendas, <em>tres figuran hoy en la lista</em>',
  'Soixante-quinze logements, <em>trois figurent aujourd’hui sur la liste</em>',
  'Fünfundsiebzig Wohnungen, <em>drei derzeit gelistet</em>',
  'Семьдесят пять квартир, <em>три сейчас в списке</em>',
  'خمسة وسبعون مسكناً، <em>ثلاثة مدرجة حالياً</em>',
  'Vijfenzeventig woningen, <em>drie momenteel vermeld</em>',
  'Siedemdziesiąt pięć lokali, <em>trzy obecnie w wykazie</em>',
  'Syttifem boliger, <em>tre oppført nå</em>',
  'Sjuttiofem bostäder, <em>tre för närvarande listade</em>')
a('.overview.copy[0]',
  'Mijas Horizon Residences es una promoción de 75 viviendas de dos o tres dormitorios en Mijas Costa, rodeada de naturaleza y con vistas al mar y a la montaña. El catálogo del promotor describe una zona central en la que confluyen los espacios comunes y que termina en la piscina, y más de {N13,000} {U} de jardines.',
  'Mijas Horizon Residences est un ensemble de 75 logements de deux ou trois chambres à Mijas Costa, entouré de nature, avec vue sur la mer et la montagne. Le catalogue du promoteur décrit une zone centrale où se rejoignent les espaces communs et qui se termine par la piscine, ainsi que plus de {N13,000} {U} de jardins.',
  'Mijas Horizon Residences ist eine Anlage mit 75 Wohnungen mit zwei oder drei Schlafzimmern in Mijas Costa, umgeben von Natur und mit Blick auf Meer und Berge. Der Katalog des Bauträgers beschreibt einen zentralen Bereich, in dem die Gemeinschaftsflächen zusammenlaufen und der am Pool endet, sowie mehr als {N13,000} {U} Gärten.',
  'Mijas Horizon Residences — комплекс из 75 квартир с двумя или тремя спальнями в Михас-Коста, окружённый природой, с видом на море и горы. В каталоге застройщика описана центральная зона, где сходятся общие пространства и которая заканчивается бассейном, а также более {N13,000} {U} садов.',
  'مشروع Mijas Horizon Residences مجمّع من 75 مسكناً بغرفتي نوم أو ثلاث غرف نوم في ميخاس كوستا، تحيط به الطبيعة وتطل مساكنه على البحر والجبال. ويصف كتالوج المطوّر منطقة مركزية تلتقي فيها المرافق المشتركة وتنتهي بالمسبح، ومساحة حدائق تزيد على {N13,000} {U}.',
  'Mijas Horizon Residences is een project van 75 woningen met twee of drie slaapkamers in Mijas Costa, omgeven door natuur en met uitzicht op de zee en de bergen. De catalogus van de ontwikkelaar beschrijft een centraal gebied waar de gemeenschappelijke ruimten samenkomen en dat eindigt bij het zwembad, en meer dan {N13,000} {U} tuinen.',
  'Mijas Horizon Residences to inwestycja obejmująca 75 lokali z dwiema lub trzema sypialniami w Mijas Costa, otoczona naturą, z widokiem na morze i góry. Katalog dewelopera opisuje centralną strefę, w której schodzą się części wspólne i która kończy się basenem, oraz ponad {N13,000} {U} ogrodów.',
  'Mijas Horizon Residences er et prosjekt med 75 boliger med to eller tre soverom i Mijas Costa, omgitt av natur og med utsikt over havet og fjellene. Utbyggerens katalog beskriver et sentralt område der fellesarealene møtes og som ender i bassenget, og mer enn {N13,000} {U} hager.',
  'Mijas Horizon Residences är ett projekt med 75 bostäder med två eller tre sovrum i Mijas Costa, omgivet av natur och med utsikt över havet och bergen. Exploatörens katalog beskriver ett centralt område där de gemensamma ytorna möts och som slutar i poolen, samt mer än {N13,000} {U} trädgårdar.')
a('.overview.copy[1]',
  'La lista de precios nombra cuatro de las 75 viviendas. Tres están disponibles: un apartamento de dos dormitorios en planta baja por {E365000}, un apartamento de tres dormitorios en planta primera por {E480000} y un ático de dos dormitorios por {E530000}, todos antes de {T}. La cuarta figura como reservada. Las condiciones de pago sitúan la escritura y la entrega de llaves en el cuarto trimestre de 2027.',
  'La liste de prix nomme quatre des 75 logements. Trois sont disponibles : un appartement de deux chambres au rez-de-chaussée à {E365000}, un appartement de trois chambres au premier étage à {E480000} et un penthouse de deux chambres à {E530000}, tous hors {T}. Le quatrième est indiqué comme réservé. Les conditions de paiement placent l’acte authentique et la remise des clés au quatrième trimestre 2027.',
  'Die Preisliste nennt vier der 75 Wohnungen. Drei sind verfügbar: ein Apartment mit zwei Schlafzimmern im Erdgeschoss für {E365000}, ein Apartment mit drei Schlafzimmern im ersten Obergeschoss für {E480000} und ein Penthouse mit zwei Schlafzimmern für {E530000}, jeweils vor {T}. Die vierte ist als reserviert gekennzeichnet. Die Zahlungsbedingungen setzen Beurkundung und Schlüsselübergabe auf das vierte Quartal 2027.',
  'В прайс-листе названы четыре из 75 квартир. Три доступны: двухспальные апартаменты на первом этаже за {E365000}, трёхспальные апартаменты на втором этаже за {E480000} и двухспальный пентхаус за {E530000}, все цены без {T}. Четвёртая отмечена как забронированная. По условиям оплаты нотариальный акт и передача ключей приходятся на четвёртый квартал 2027 года.',
  'تذكر قائمة الأسعار أربعة مساكن من أصل 75. ثلاثة منها متاحة: شقة بغرفتي نوم في الطابق الأرضي بسعر {E365000}، وشقة بثلاث غرف نوم في الطابق الأول بسعر {E480000}، وبنتهاوس بغرفتي نوم بسعر {E530000}، وكلها قبل {T}. أما الرابع فمشار إليه على أنه محجوز. وتحدد شروط الدفع موعد سند الملكية وتسليم المفاتيح في الربع الرابع من عام 2027.',
  'De prijslijst noemt vier van de 75 woningen. Drie zijn beschikbaar: een appartement met twee slaapkamers op de begane grond voor {E365000}, een appartement met drie slaapkamers op de eerste verdieping voor {E480000} en een penthouse met twee slaapkamers voor {E530000}, alle exclusief {T}. De vierde is als gereserveerd aangemerkt. De betalingsvoorwaarden plaatsen de notariële akte en de sleuteloverdracht in het vierde kwartaal van 2027.',
  'Cennik wymienia cztery z 75 lokali. Trzy są dostępne: dwupokojowy apartament na parterze za {E365000}, trzysypialniowy apartament na pierwszym piętrze za {E480000} i dwusypialniowy penthouse za {E530000}, wszystkie ceny bez {T}. Czwarty jest oznaczony jako zarezerwowany. Warunki płatności wyznaczają akt notarialny i przekazanie kluczy na czwarty kwartał 2027 roku.',
  'Prislisten nevner fire av de 75 boligene. Tre er ledige: en leilighet med to soverom i første etasje for {E365000}, en leilighet med tre soverom i andre etasje for {E480000} og en toppleilighet med to soverom for {E530000}, alle før {T}. Den fjerde er markert som reservert. Betalingsvilkårene legger skjøtet og nøkkeloverleveringen til fjerde kvartal 2027.',
  'Prislistan nämner fyra av de 75 bostäderna. Tre är lediga: en lägenhet med två sovrum i bottenvåningen för {E365000}, en lägenhet med tre sovrum på första våningen för {E480000} och en takvåning med två sovrum för {E530000}, alla före {T}. Den fjärde är markerad som reserverad. Betalningsvillkoren lägger lagfarten och nyckelöverlämnandet i fjärde kvartalet 2027.')
a('.overview.metrics[0][1]',
  '75 viviendas', '75 logements', '75 Wohnungen', '75 квартир', '75 مسكناً', '75 woningen', '75 lokali', '75 boliger', '75 bostäder')
a('.why.copy',
  'Viviendas nuevas de dos y tres dormitorios con terraza, plaza de garaje y trastero, piscina, gimnasio y club social, y un calendario de pagos que deja el 70 % para la escritura.',
  'Des logements neufs de deux et trois chambres avec terrasse, place de garage et cave, une piscine, une salle de sport et un club social, et un échéancier qui garde 70 % pour l’acte.',
  'Neue Wohnungen mit zwei und drei Schlafzimmern, Terrasse, Garagenstellplatz und Abstellraum, Pool, Fitnessraum und Social Club sowie ein Zahlungsplan, der 70 % für die Beurkundung lässt.',
  'Новые квартиры с двумя и тремя спальнями, террасой, машиноместом и кладовой, бассейн, тренажёрный зал, клуб для жильцов и график платежей, при котором 70 % приходится на сделку.',
  'مساكن جديدة بغرفتي نوم وثلاث غرف نوم مع تراس وموقف سيارات في المرآب ومخزن، ومسبح وصالة رياضية ونادٍ اجتماعي، وجدول دفعات يترك 70% لمرحلة سند الملكية.',
  'Nieuwe woningen met twee en drie slaapkamers, een terras, een garageplaats en een berging, een zwembad, een fitnessruimte en een sociale club, en een betalingsschema dat 70% voor de akte overlaat.',
  'Nowe lokale z dwiema i trzema sypialniami, tarasem, miejscem garażowym i komórką lokatorską, basen, siłownia i klub dla mieszkańców oraz harmonogram płatności, który zostawia 70% na akt notarialny.',
  'Nye boliger med to og tre soverom, terrasse, garasjeplass og bod, basseng, treningsrom og sosial klubb, og en betalingsplan som holder 70 % igjen til skjøtet.',
  'Nya bostäder med två och tre sovrum, terrass, garageplats och förråd, pool, gym och social klubb, och ett betalningsschema som sparar 70 % till lagfarten.')
a('.why.points[0][1]',
  'Compradores que buscan un apartamento o ático nuevo de dos o tres dormitorios en Mijas Costa, con terraza y una plaza de garaje y un trastero numerados, para vivir o como segunda residencia.',
  'Acheteurs qui cherchent un appartement ou un penthouse neuf de deux ou trois chambres à Mijas Costa, avec terrasse et une place de garage et une cave numérotées, pour y vivre ou comme résidence secondaire.',
  'Käufer, die ein neues Apartment oder Penthouse mit zwei oder drei Schlafzimmern in Mijas Costa suchen, mit Terrasse sowie nummeriertem Garagenstellplatz und Abstellraum, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужны новые апартаменты или пентхаус с двумя или тремя спальнями в Михас-Коста, с террасой, пронумерованным машиноместом и кладовой, для жизни или как вторая резиденция.',
  'مشترون يبحثون عن شقة أو بنتهاوس جديد بغرفتي نوم أو ثلاث غرف نوم في ميخاس كوستا، مع تراس وموقف سيارات ومخزن مرقّمين، للسكن الدائم أو كمسكن ثانٍ.',
  'Kopers die een nieuw appartement of penthouse met twee of drie slaapkamers in Mijas Costa zoeken, met een terras en een genummerde garageplaats en berging, om er te wonen of als tweede woning.',
  'Kupujący szukający nowego apartamentu lub penthouse’u z dwiema lub trzema sypialniami w Mijas Costa, z tarasem oraz numerowanym miejscem garażowym i komórką lokatorską, do zamieszkania lub jako drugi dom.',
  'Kjøpere som vil ha en ny leilighet eller toppleilighet med to eller tre soverom i Mijas Costa, med terrasse og nummerert garasjeplass og bod, til å bo i eller som andrebolig.',
  'Köpare som vill ha en ny lägenhet eller takvåning med två eller tre sovrum i Mijas Costa, med terrass och numrerad garageplats och förråd, att bo i eller som andrabostad.')
a('.why.points[1][0]',
  'La mayor parte del precio se paga en la escritura', 'L’essentiel du prix se règle à l’acte',
  'Der größte Teil des Preises fällt bei der Beurkundung an', 'Основная часть цены оплачивается при сделке',
  'معظم الثمن يُدفع عند سند الملكية', 'Het grootste deel van de prijs valt bij de akte',
  'Większość ceny płaci się przy akcie notarialnym', 'Mesteparten av prisen forfaller ved skjøtet',
  'Största delen av priset infaller vid lagfarten')
a('.why.points[1][1]',
  'El setenta por ciento más {T} se paga al terminar y entregar las llaves, tras una reserva, un 15 % en el contrato privado y un 15 % el 5 de mayo de 2027.',
  'Soixante-dix pour cent hors {T} sont dus à l’achèvement et à la remise des clés, après une réservation, 15 % au contrat privé et 15 % le 5 mai 2027.',
  'Siebzig Prozent zuzüglich {T} fallen bei Fertigstellung und Schlüsselübergabe an, nach einer Reservierung, 15 % beim privaten Vertrag und 15 % am 5. Mai 2027.',
  'Семьдесят процентов плюс {T} оплачиваются при завершении и передаче ключей, после бронирования, 15 % при частном договоре и 15 % 5 мая 2027 года.',
  'سبعون في المئة زائد {T} تُدفع عند الإنجاز وتسليم المفاتيح، بعد الحجز، و15% عند العقد الخاص و15% في 5 مايو 2027.',
  'Zeventig procent plus {T} valt bij oplevering en sleuteloverdracht, na een reservering, 15% bij het onderhandse contract en 15% op 5 mei 2027.',
  'Siedemdziesiąt procent plus {T} płaci się przy zakończeniu i przekazaniu kluczy, po rezerwacji, 15% przy umowie przedwstępnej i 15% 5 maja 2027 roku.',
  'Sytti prosent pluss {T} forfaller ved ferdigstillelse og nøkkeloverlevering, etter en reservasjon, 15 % ved den private kontrakten og 15 % den 5. mai 2027.',
  'Sjuttio procent plus {T} infaller vid färdigställande och nyckelöverlämnande, efter en reservation, 15 % vid det privata avtalet och 15 % den 5 maj 2027.')
a('.why.points[2][0]',
  'Una terraza en cada vivienda de la lista', 'Une terrasse sur chaque logement de la liste',
  'Eine Terrasse bei jeder gelisteten Wohnung', 'Терраса у каждой квартиры из списка',
  'تراس في كل مسكن من القائمة', 'Een terras bij elke vermelde woning',
  'Taras przy każdym lokalu z wykazu', 'Terrasse på hver oppført bolig',
  'Terrass vid varje listad bostad')
a('.why.points[2][1]',
  'Las tres viviendas de la lista tienen terrazas de {N24.89}, {N18.87} y {N37.03} {U}, y los renders del promotor las muestran como lugares para sentarse y comer al aire libre.',
  'Les trois logements de la liste ont des terrasses de {N24.89}, {N18.87} et {N37.03} {U}, et les rendus du promoteur les montrent comme des lieux où s’asseoir et manger dehors.',
  'Die drei gelisteten Wohnungen haben Terrassen von {N24.89}, {N18.87} und {N37.03} {U}, und die Renderings des Bauträgers zeigen sie als Orte zum Sitzen und Essen im Freien.',
  'У трёх квартир из списка террасы площадью {N24.89}, {N18.87} и {N37.03} {U}, а визуализации застройщика показывают их как места, где можно сидеть и обедать на открытом воздухе.',
  'للمساكن الثلاثة المدرجة تراسات مساحتها {N24.89} و{N18.87} و{N37.03} {U}، وتُظهرها صور المطوّر على أنها أماكن للجلوس وتناول الطعام في الهواء الطلق.',
  'De drie vermelde woningen hebben terrassen van {N24.89}, {N18.87} en {N37.03} {U}, en de renders van de ontwikkelaar tonen ze als plekken om buiten te zitten en te eten.',
  'Trzy lokale z wykazu mają tarasy o powierzchni {N24.89}, {N18.87} i {N37.03} {U}, a wizualizacje dewelopera pokazują je jako miejsca do siedzenia i jedzenia na świeżym powietrzu.',
  'De tre oppførte boligene har terrasser på {N24.89}, {N18.87} og {N37.03} {U}, og utbyggerens egne bilder viser dem som steder å sitte og spise ute.',
  'De tre listade bostäderna har terrasser på {N24.89}, {N18.87} och {N37.03} {U}, och exploatörens egna bilder visar dem som platser att sitta och äta utomhus.')
a('.why.points[3][1]',
  'El promotor presenta el solar como un lugar rodeado de naturaleza con vistas al mar y a la montaña. La vista de cada vivienda depende de su bloque y su planta, y la comprobamos en los planos y sobre el terreno.',
  'Le promoteur présente le terrain comme un site entouré de nature avec vue sur la mer et la montagne. La vue de chaque logement dépend de son bloc et de son étage, que nous vérifions sur les plans et sur place.',
  'Der Bauträger stellt das Grundstück als von Natur umgeben mit Blick auf Meer und Berge dar. Welche Aussicht eine Wohnung hat, hängt von Block und Etage ab; das prüfen wir anhand der Pläne und vor Ort.',
  'Застройщик представляет участок как место среди природы с видом на море и горы. Какой вид у конкретной квартиры, зависит от корпуса и этажа, и мы проверяем это по планам и на месте.',
  'يقدّم المطوّر الموقع على أنه محاط بالطبيعة وتطل مساكنه على البحر والجبال. وتتوقف الإطلالة التي يتمتع بها كل مسكن على مبناه وطابقه، ونتحقق منها على المخططات وفي الموقع.',
  'De ontwikkelaar presenteert het terrein als omgeven door natuur met uitzicht op de zee en de bergen. Welk uitzicht een woning heeft, hangt af van het blok en de verdieping, wat wij op de plattegronden en ter plaatse controleren.',
  'Deweloper przedstawia teren jako otoczony naturą, z widokiem na morze i góry. Jaki widok ma dany lokal, zależy od bloku i piętra, co sprawdzamy na rzutach i na miejscu.',
  'Utbyggeren presenterer tomten som omgitt av natur med utsikt over havet og fjellene. Hvilken utsikt en bolig har, avhenger av blokk og etasje, noe vi sjekker på tegningene og på stedet.',
  'Exploatören presenterar tomten som omgiven av natur med utsikt över havet och bergen. Vilken utsikt en bostad har beror på huset och våningen, vilket vi kontrollerar på ritningarna och på plats.')
a('.architecture.headlineHtml',
  'Bloques en torno a <em>una piscina central</em>', 'Des blocs autour <em>d’une piscine centrale</em>',
  'Blöcke rund um <em>einen zentralen Pool</em>', 'Корпуса вокруг <em>центрального бассейна</em>',
  'مبانٍ حول <em>مسبح مركزي</em>', 'Blokken rond <em>een centraal zwembad</em>',
  'Bloki wokół <em>centralnego basenu</em>', 'Blokker rundt <em>et sentralt basseng</em>',
  'Hus kring <em>en central pool</em>')
a('.architecture.copy[0]',
  'El catálogo describe las zonas comunes como un espacio central que termina en la piscina, a modo de centro de ocio dentro de su propia casa. En los renders, los bloques tienen terrazas profundas con barandillas de cristal, accesos revestidos de piedra y palmeras alrededor de la piscina y del césped.',
  'Le catalogue décrit les parties communes comme un espace central qui se termine par la piscine, comme un centre de loisirs au sein de votre logement. Dans les rendus, les blocs ont de profondes terrasses à garde-corps en verre, des entrées habillées de pierre et des palmiers autour de la piscine et de la pelouse.',
  'Der Katalog beschreibt die Gemeinschaftsbereiche als zentralen Raum, der am Pool endet, wie ein Freizeitzentrum innerhalb Ihres Zuhauses. In den Renderings haben die Blöcke tiefe Terrassen mit Glasbrüstungen, steinverkleidete Eingangsbereiche und Palmen rund um Pool und Rasen.',
  'В каталоге общие зоны описаны как центральное пространство, заканчивающееся бассейном, — словно центр досуга внутри вашего дома. На визуализациях у корпусов глубокие террасы со стеклянными ограждениями, входные группы с каменной облицовкой и пальмы вокруг бассейна и газона.',
  'يصف الكتالوج المناطق المشتركة بأنها فضاء مركزي ينتهي بالمسبح، كأنه مركز ترفيه داخل منزلك. وفي الصور المولَّدة تظهر المباني بتراسات عميقة ذات حواجز زجاجية ومداخل مكسوة بالحجر ونخيل حول المسبح والمرج.',
  'De catalogus beschrijft de gemeenschappelijke ruimten als een centrale ruimte die eindigt bij het zwembad, als een recreatiecentrum binnen uw eigen woning. In de renders hebben de blokken diepe terrassen met glazen balustrades, met steen beklede entrees en palmen rond het zwembad en het gazon.',
  'Katalog opisuje części wspólne jako centralną przestrzeń kończącą się basenem, niczym centrum rekreacji we własnym domu. Na wizualizacjach bloki mają głębokie tarasy ze szklanymi balustradami, wejścia wykończone kamieniem oraz palmy wokół basenu i trawnika.',
  'Katalogen beskriver fellesarealene som et sentralt rom som ender i bassenget, som et fritidssenter inne i ditt eget hjem. På bildene har blokkene dype terrasser med glassrekkverk, steinkledde inngangspartier og palmer rundt bassenget og plenen.',
  'Katalogen beskriver de gemensamma ytorna som ett centralt rum som slutar i poolen, som ett fritidscenter inom ditt eget hem. På bilderna har husen djupa terrasser med glasräcken, stenklädda entréer och palmer kring poolen och gräsmattan.')
a('.architecture.copy[1]',
  'La lista de precios y los planos numeran los bloques y los portales: las tres viviendas de la lista están en los bloques 2 y 3, en los portales 4 y 6, y la reservada está en el bloque 1, portal 2. Los documentos no indican el número de plantas.',
  'La liste de prix et les plans numérotent les blocs et les entrées : les trois logements de la liste se trouvent dans les blocs 2 et 3, aux entrées 4 et 6, et le logement réservé dans le bloc 1, entrée 2. Les documents n’indiquent pas le nombre d’étages.',
  'Preisliste und Pläne nummerieren die Blöcke und Eingänge: Die drei gelisteten Wohnungen liegen in den Blöcken 2 und 3, an den Eingängen 4 und 6, die reservierte in Block 1, Eingang 2. Die Anzahl der Geschosse geben die Unterlagen nicht an.',
  'В прайс-листе и на планах корпуса и подъезды пронумерованы: три квартиры из списка находятся в корпусах 2 и 3, в подъездах 4 и 6, а забронированная — в корпусе 1, подъезд 2. Число этажей в документах не указано.',
  'تُرقّم قائمة الأسعار والمخططات المباني والمداخل: المساكن الثلاثة المدرجة في المبنيين 2 و3 عند المدخلين 4 و6، والمسكن المحجوز في المبنى 1 عند المدخل 2. ولا تذكر الوثائق عدد الطوابق.',
  'De prijslijst en de plattegronden nummeren de blokken en portieken: de drie vermelde woningen liggen in blok 2 en 3, bij portiek 4 en 6, en de gereserveerde in blok 1, portiek 2. De documenten vermelden het aantal verdiepingen niet.',
  'Cennik i rzuty numerują bloki i klatki schodowe: trzy lokale z wykazu znajdują się w blokach 2 i 3, w klatkach 4 i 6, a zarezerwowany w bloku 1, klatka 2. Dokumenty nie podają liczby kondygnacji.',
  'Prislisten og tegningene nummererer blokkene og oppgangene: de tre oppførte boligene ligger i blokk 2 og 3, i oppgang 4 og 6, og den reserverte i blokk 1, oppgang 2. Dokumentene oppgir ikke antall etasjer.',
  'Prislistan och ritningarna numrerar husen och trapphusen: de tre listade bostäderna ligger i hus 2 och 3, i trapphus 4 och 6, och den reserverade i hus 1, trapphus 2. Dokumenten anger inte antalet våningar.')
a('.architecture.highlights[0]',
  'Un conjunto residencial cerrado con acceso privado, un videoportero automático para la urbanización y las puertas de entrada, y llaves maestras para la cancela, las viviendas y el garaje.',
  'Un ensemble résidentiel fermé à accès privé, un visiophone automatique pour la résidence et les portes d’entrée, et des clés maîtresses pour le portail, les logements et le garage.',
  'Eine geschlossene Wohnanlage mit privatem Zugang, eine automatische Videosprechanlage für die Anlage und die Wohnungstüren sowie Generalschlüssel für das Tor, die Wohnungen und die Garage.',
  'Закрытый жилой комплекс с частным въездом, автоматический видеодомофон для комплекса и входных дверей и мастер-ключи от ворот, квартир и гаража.',
  'مجمّع سكني مسوَّر بمدخل خاص، وجهاز اتصال مرئي آلي للمجمّع وأبواب المساكن، ومفاتيح رئيسية للبوابة والمساكن والمرآب.',
  'Een afgesloten woonwijk met privétoegang, een automatische videofoon voor het complex en de voordeuren, en hoofdsleutels voor het hek, de woningen en de garage.',
  'Zamknięty kompleks mieszkaniowy z prywatnym dostępem, automatyczny wideodomofon dla osiedla i drzwi wejściowych oraz klucze generalne do bramy, lokali i garażu.',
  'Et lukket boligområde med privat adkomst, en automatisk videoporttelefon for anlegget og inngangsdørene, og hovednøkler til porten, boligene og garasjen.',
  'Ett inhägnat bostadsområde med privat infart, en automatisk videodörrtelefon för området och ytterdörrarna, och huvudnycklar till porten, bostäderna och garaget.')
a('.architecture.highlights[1]',
  'Ascensores con puertas automáticas, aptos para usuarios con discapacidad.',
  'Ascenseurs à portes automatiques, adaptés aux personnes handicapées.',
  'Aufzüge mit automatischen Türen, geeignet für Menschen mit Behinderung.',
  'Лифты с автоматическими дверями, подходящие для людей с ограниченными возможностями.',
  'مصاعد بأبواب آلية، مناسبة لذوي الإعاقة.',
  'Liften met automatische deuren, geschikt voor gebruikers met een beperking.',
  'Windy z automatycznymi drzwiami, przystosowane dla osób niepełnosprawnych.',
  'Heiser med automatiske dører, egnet for brukere med nedsatt funksjonsevne.',
  'Hissar med automatiska dörrar, lämpliga för användare med funktionsnedsättning.')
a('.architecture.highlights[2]',
  'Puerta de garaje motorizada con mando a distancia y preinstalación para la recarga de vehículos eléctricos.',
  'Porte de garage motorisée avec télécommande et pré-installation pour la recharge des véhicules électriques.',
  'Motorisiertes Garagentor mit Fernbedienung und Vorinstallation für das Laden von Elektrofahrzeugen.',
  'Гаражные ворота с электроприводом и пультом и предустановка для зарядки электромобилей.',
  'باب مرآب بمحرك مع جهاز تحكم عن بعد، وتجهيز مسبق لشحن المركبات الكهربائية.',
  'Een gemotoriseerde garagedeur met afstandsbediening en een voorbereiding voor het laden van elektrische voertuigen.',
  'Napędzana brama garażowa z pilotem oraz instalacja przygotowawcza do ładowania pojazdów elektrycznych.',
  'En motorisert garasjeport med fjernkontroll og forberedelse for lading av elbiler.',
  'En motoriserad garageport med fjärrkontroll och förberedelse för laddning av elfordon.')
a('.architecture.highlights[3]',
  'Doble acristalamiento de PVC tipo Climalit en marrón, con vidrio laminado de seguridad en las puertas de terraza y vidrio antiintrusión en las ventanas de planta baja.',
  'Double vitrage de type Climalit en PVC brun, avec verre feuilleté de sécurité aux portes de terrasse et verre anti-effraction aux fenêtres du rez-de-chaussée.',
  'Doppelverglasung vom Typ Climalit in braunem PVC, mit Verbundsicherheitsglas an den Terrassentüren und einbruchhemmendem Glas in den Erdgeschossfenstern.',
  'Двойное остекление типа Climalit в коричневом ПВХ, с многослойным безопасным стеклом в дверях на террасу и противовзломным стеклом в окнах первого этажа.',
  'زجاج مزدوج من نوع Climalit في إطارات PVC بنية اللون، مع زجاج رقائقي للأمان في أبواب التراسات وزجاج مقاوم للاقتحام في نوافذ الطابق الأرضي.',
  'Dubbel glas van het type Climalit in bruin pvc, met gelaagd veiligheidsglas bij de terrasdeuren en inbraakwerend glas in de ramen op de begane grond.',
  'Podwójne szyby typu Climalit w brązowych ramach z PVC, ze szkłem laminowanym bezpiecznym w drzwiach tarasowych i szkłem antywłamaniowym w oknach parteru.',
  'Tolags vinduer av typen Climalit i brun PVC, med laminert sikkerhetsglass i terrassedørene og innbruddshemmende glass i vinduene i første etasje.',
  'Tvåglasfönster av typen Climalit i brun PVC, med laminerat säkerhetsglas i altandörrarna och inbrottshämmande glas i fönstren i bottenvåningen.')

# ---- quality specs ---------------------------------------------------------------------------

a('.qualitySpecs.copy',
  'La memoria de calidades del propio promotor, resumida por zonas de la vivienda.',
  'Le descriptif de qualité du promoteur lui-même, résumé par partie du logement.',
  'Die Baubeschreibung des Bauträgers selbst, zusammengefasst nach Bereichen der Wohnung.',
  'Собственное описание качества отделки от застройщика, сгруппированное по частям квартиры.',
  'وثيقة المواصفات الصادرة عن المطوّر نفسه، ملخّصة بحسب أجزاء المسكن.',
  'De eigen technische omschrijving van de ontwikkelaar, samengevat per onderdeel van de woning.',
  'Standard wykończenia opracowany przez samego dewelopera, podsumowany według części lokalu.',
  'Utbyggerens egen byggebeskrivelse, oppsummert etter deler av boligen.',
  'Exploatörens egen byggbeskrivning, sammanfattad efter delar av bostaden.')
a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor, que no lleva fecha impresa. Indica que la dirección facultativa puede modificar las calidades y sustituirlas por otras de nivel similar, y que la piedra natural y la madera varían en color y tono.',
  'Source : le descriptif de qualité du promoteur, qui ne porte aucune date imprimée. Il précise que la direction du projet peut modifier les prestations et les remplacer par d’autres de niveau similaire, et que la pierre naturelle et le bois varient en couleur et en nuance.',
  'Quelle: die Baubeschreibung des Bauträgers, die kein aufgedrucktes Datum trägt. Sie besagt, dass die Projektleitung die Ausstattung ändern und durch gleichwertige ersetzen kann und dass Naturstein und Holz in Farbe und Ton variieren.',
  'Источник: описание качества отделки застройщика, на котором нет напечатанной даты. В нём сказано, что руководство проекта может изменять материалы и заменять их равноценными и что природный камень и дерево различаются по цвету и тону.',
  'المصدر: وثيقة المواصفات الصادرة عن المطوّر، وهي لا تحمل تاريخاً مطبوعاً. وتنص على أن إدارة المشروع قد تعدّل المواصفات وتستبدلها بأخرى من مستوى مماثل، وأن الحجر الطبيعي والخشب يختلفان في اللون والدرجة.',
  'Bron: de technische omschrijving van de ontwikkelaar, die geen gedrukte datum draagt. Daarin staat dat de projectleiding de afwerking mag wijzigen en door gelijkwaardige afwerking mag vervangen, en dat natuursteen en hout in kleur en tint verschillen.',
  'Źródło: standard wykończenia dewelopera, który nie ma wydrukowanej daty. Zastrzega on, że kierownictwo projektu może zmieniać wykończenie i zastępować je równorzędnym oraz że kamień naturalny i drewno różnią się kolorem i odcieniem.',
  'Kilde: utbyggerens byggebeskrivelse, som ikke har trykt dato. Den sier at prosjektledelsen kan endre standarden og erstatte den med likeverdig, og at naturstein og tre varierer i farge og tone.',
  'Källa: exploatörens byggbeskrivning, som saknar tryckt datum. Den anger att projektledningen kan ändra standarden och ersätta den med likvärdig, och att natursten och trä varierar i färg och ton.')
a('.qualitySpecs.groups[0].name',
  'Suelos y revestimientos', 'Sols et revêtements', 'Böden und Fliesen', 'Полы и плитка', 'الأرضيات والبلاط',
  'Vloeren en tegels', 'Podłogi i płytki', 'Gulv og fliser', 'Golv och kakel')
a('.qualitySpecs.groups[0].items[0]',
  'Suelo laminado muy resistente a arañazos y golpes en salón, dormitorios, cocinas, pasillos y rellanos, con rodapié blanco a juego con las puertas.',
  'Sol stratifié très résistant aux rayures et aux chocs dans les pièces de vie, les chambres, les cuisines, les couloirs et les paliers, avec plinthes blanches assorties aux portes.',
  'Laminatboden, sehr widerstandsfähig gegen Kratzer und Stöße, in Wohnbereichen, Schlafzimmern, Küchen, Fluren und Treppenabsätzen, mit weißen Sockelleisten passend zu den Türen.',
  'Ламинат, очень стойкий к царапинам и ударам, в жилых зонах, спальнях, кухнях, коридорах и на площадках, с белыми плинтусами в тон дверям.',
  'أرضية لامينيت شديدة المقاومة للخدوش والصدمات في مناطق المعيشة وغرف النوم والمطابخ والممرات والبسطات، مع وزرات بيضاء تتناسق مع الأبواب.',
  'Laminaatvloer, zeer krasbestendig en slagvast, in de woonruimtes, slaapkamers, keukens, gangen en overlopen, met witte plinten passend bij de deuren.',
  'Podłoga laminowana, bardzo odporna na zarysowania i uderzenia, w częściach dziennych, sypialniach, kuchniach, korytarzach i na podestach, z białymi listwami przypodłogowymi dopasowanymi do drzwi.',
  'Laminatgulv som tåler riper og slag svært godt, i oppholdsrom, soverom, kjøkken, ganger og avsatser, med hvite gulvlister som matcher dørene.',
  'Laminatgolv som är mycket tåligt mot repor och slag, i vardagsrum, sovrum, kök, hallar och trapplan, med vita golvlister som matchar dörrarna.')
a('.qualitySpecs.groups[0].items[1]',
  'Suelo de baldosas en baños y aseos, de 60 x 60 cm en blanco o marfil, y baldosas grises de 60 x 60 cm antideslizantes y resistentes a las heladas en las terrazas.',
  'Carrelage au sol dans les salles de bain et les WC, en 60 x 60 cm blanc ou ivoire, et carreaux gris de 60 x 60 cm antidérapants et résistants au gel sur les terrasses.',
  'Fliesenboden in Bädern und Toiletten, 60 x 60 cm in Weiß oder Elfenbein, und rutschfeste, frostbeständige graue Fliesen 60 x 60 cm auf den Terrassen.',
  'Плиточный пол в ванных комнатах и туалетах, плитка 60 x 60 см белого или цвета слоновой кости, а на террасах — нескользящая морозостойкая серая плитка 60 x 60 см.',
  'أرضيات من البلاط في الحمّامات ودورات المياه بمقاس 60 × 60 سم باللون الأبيض أو العاجي، وبلاط رمادي بمقاس 60 × 60 سم مانع للانزلاق ومقاوم للصقيع في التراسات.',
  'Tegelvloeren in de badkamers en toiletten, 60 x 60 cm in wit of ivoor, en antislip, vorstbestendige grijze tegels van 60 x 60 cm op de terrassen.',
  'Podłogi z płytek w łazienkach i toaletach, o wymiarach 60 x 60 cm, w kolorze białym lub kości słoniowej, oraz antypoślizgowe, mrozoodporne szare płytki 60 x 60 cm na tarasach.',
  'Fliser på gulvet i bad og toaletter, 60 x 60 cm i hvitt eller elfenben, og sklisikre, frostbestandige grå fliser på 60 x 60 cm på terrassene.',
  'Kakelgolv i badrum och toaletter, 60 x 60 cm i vitt eller elfenben, och halkfritt, frostbeständigt grått kakel på 60 x 60 cm på terrasserna.')
a('.qualitySpecs.groups[1].items[0]',
  'Sanitarios de porcelana vitrificada blanca, platos de ducha de resina en ambos baños, grifería monomando y lavabo integrado en el mueble.',
  'Appareils sanitaires en porcelaine émaillée blanche, receveurs de douche en résine dans les deux salles de bain, mitigeurs et vasque intégrée au meuble.',
  'Sanitärobjekte aus weißem glasiertem Porzellan, Duschwannen aus Kunstharz in beiden Bädern, Einhebelmischer und ein in den Waschtisch integriertes Becken.',
  'Белая глазурованная фарфоровая сантехника, смоляные душевые поддоны в обеих ванных комнатах, смесители и раковина, встроенная в тумбу.',
  'تجهيزات صحية من الخزف الأبيض المزجَّج، وأحواض دش من الراتنج في الحمّامين، وخلاطات مياه، وحوض غسل مدمج في الخزانة.',
  'Wit geglazuurd porseleinen sanitair, kunstharsdouchebakken in beide badkamers, mengkranen en een in het meubel verwerkte wastafel.',
  'Biała szkliwiona armatura sanitarna z porcelany, brodziki z żywicy w obu łazienkach, baterie jednouchwytowe i umywalka wbudowana w szafkę.',
  'Hvitt glassert porselensutstyr, dusjkar av harpiks i begge baderom, blandebatterier og en servant innfelt i skapet.',
  'Vit glaserad porslinssanitet, duschkar av harts i båda badrummen, blandare och ett tvättställ inbyggt i skåpet.')
a('.qualitySpecs.groups[1].items[1]',
  'Alicatado cerámico en la zona de ducha y en el suelo, con pintura plástica lisa en el resto de las paredes.',
  'Faïence céramique dans la zone de douche et au sol, avec une peinture lisse sur les autres murs.',
  'Keramische Fliesen im Duschbereich und auf dem Boden, glatter Dispersionsanstrich an den übrigen Wänden.',
  'Керамическая плитка в душевой зоне и на полу, гладкая водоэмульсионная краска на остальных стенах.',
  'تكسية بالبلاط الخزفي في منطقة الدش وعلى الأرضية، مع دهان أملس على بقية الجدران.',
  'Keramische tegels in de douchezone en op de vloer, met gladde muurverf op de overige wanden.',
  'Płytki ceramiczne w strefie prysznica i na podłodze, gładka farba emulsyjna na pozostałych ścianach.',
  'Keramiske fliser i dusjområdet og på gulvet, med glatt plastmaling på de øvrige veggene.',
  'Keramiskt kakel i duschzonen och på golvet, med slät plastfärg på de övriga väggarna.')
a('.qualitySpecs.groups[2].items[0]',
  'Muebles altos y bajos de laminado de alta presión, con encimera de Silestone y fregadero integrado, y ventilación mecánica.',
  'Meubles hauts et bas en stratifié haute pression, avec plan de travail en Silestone et évier intégré, et ventilation mécanique.',
  'Hoch- und Unterschränke aus Hochdrucklaminat, mit Arbeitsplatte aus Silestone und eingebautem Spülbecken sowie mechanischer Lüftung.',
  'Верхние и нижние шкафы из ламината высокого давления, столешница из Silestone со встроенной мойкой и механическая вентиляция.',
  'خزائن علوية وسفلية من اللامينيت عالي الضغط، مع سطح عمل من Silestone وحوض مدمج، وتهوية ميكانيكية.',
  'Hoge en lage kasten van hogedruklaminaat, met een werkblad van Silestone en een ingebouwde spoelbak, en mechanische ventilatie.',
  'Szafki wiszące i stojące z laminatu wysokociśnieniowego, blat z Silestone i wbudowany zlew oraz wentylacja mechaniczna.',
  'Over- og underskap i høytrykkslaminat, med benkeplate i Silestone og innfelt vask, og mekanisk ventilasjon.',
  'Över- och underskåp i högtryckslaminat, med bänkskiva i Silestone och infälld diskho, samt mekanisk ventilation.')
a('.qualitySpecs.groups[2].items[1]',
  'Se incluyen nevera, lavadora, lavavajillas, placa de inducción, horno, microondas y campana extractora.',
  'Un réfrigérateur, un lave-linge, un lave-vaisselle, une plaque à induction, un four, un micro-ondes et une hotte aspirante sont inclus.',
  'Kühlschrank, Waschmaschine, Geschirrspüler, Induktionskochfeld, Backofen, Mikrowelle und Dunstabzugshaube sind enthalten.',
  'В комплект входят холодильник, стиральная машина, посудомоечная машина, индукционная варочная панель, духовой шкаф, микроволновая печь и вытяжка.',
  'تشمل التجهيزات ثلاجة وغسالة وغسالة صحون وموقد حثّي وفرناً وميكروويف ومروحة شفط.',
  'Een koelkast, een wasmachine, een vaatwasser, een inductiekookplaat, een oven, een magnetron en een afzuigkap zijn inbegrepen.',
  'W cenie jest lodówka, pralka, zmywarka, płyta indukcyjna, piekarnik, kuchenka mikrofalowa i okap.',
  'Kjøleskap, vaskemaskin, oppvaskmaskin, induksjonstopp, ovn, mikrobølgeovn og kjøkkenvifte er inkludert.',
  'Kylskåp, tvättmaskin, diskmaskin, induktionshäll, ugn, mikrovågsugn och köksfläkt ingår.')
a('.qualitySpecs.groups[3].name',
  'Carpintería', 'Menuiserie', 'Tischlerarbeiten', 'Столярные изделия', 'النجارة',
  'Timmerwerk', 'Stolarka', 'Snekkerarbeid', 'Snickerier')
a('.qualitySpecs.groups[3].items[0]',
  'Puertas interiores de madera lacadas en blanco con manillas de acero, y armarios tipo bloque con balda separadora y barra de colgar.',
  'Portes intérieures en bois laquées blanc avec poignées en acier, et placards en bloc avec tablette séparatrice et tringle de penderie.',
  'Innentüren aus weiß lackiertem Holz mit Stahlgriffen sowie Blockschränke mit Trennboden und Kleiderstange.',
  'Межкомнатные двери из дерева, лакированные белым, со стальными ручками, и шкафы блочного типа с разделительной полкой и штангой.',
  'أبواب داخلية خشبية مطلية باللك الأبيض بمقابض فولاذية، وخزائن ملابس من النوع الكتلي مع رف فاصل وعمود تعليق.',
  'Binnendeuren van wit gelakt hout met stalen kinken, en blokkasten met een scheidingsplank en een kledingstang.',
  'Drewniane drzwi wewnętrzne lakierowane na biało ze stalowymi klamkami oraz szafy blokowe z półką dzielącą i drążkiem na ubrania.',
  'Innerdører i hvitlakkert tre med stålhåndtak, og blokkgarderober med skillehylle og kleshenger.',
  'Innerdörrar i vitlackerat trä med ståldörrhandtag och blockgarderober med mellanhylla och klädstång.')
a('.qualitySpecs.groups[3].items[1]',
  'Doble acristalamiento abatible, corredera u oscilobatiente de PVC marrón, vidrio laminado de seguridad en las puertas de terraza y persianas enrollables manuales con aislamiento térmico en los dormitorios.',
  'Double vitrage battant, coulissant ou oscillo-battant en PVC brun, verre feuilleté de sécurité aux portes de terrasse et volets roulants manuels à isolation thermique dans les chambres.',
  'Doppelverglasung als Dreh-, Schiebe- oder Kippfenster in braunem PVC, Verbundsicherheitsglas an den Terrassentüren und manuelle Rollläden mit Wärmedämmung in den Schlafzimmern.',
  'Двойное остекление в коричневом ПВХ — распашное, раздвижное или поворотно-откидное, многослойное безопасное стекло в дверях на террасу и ручные рольставни с теплоизоляцией в спальнях.',
  'زجاج مزدوج بإطارات PVC بنية اللون، قابل للطي أو المنزلق أو المائل، وزجاج رقائقي للأمان في أبواب التراسات، وستائر لفّ يدوية معزولة حرارياً في غرف النوم.',
  'Dubbel glas in bruin pvc, draaiend, schuivend of kiepend, gelaagd veiligheidsglas bij de terrasdeuren en handbediende rolluiken met thermische isolatie in de slaapkamers.',
  'Podwójne szyby w brązowych ramach z PVC, uchylne, przesuwne lub rozwierane, szkło laminowane bezpieczne w drzwiach tarasowych oraz ręczne rolety z izolacją termiczną w sypialniach.',
  'Tolags vinduer i brun PVC, som kan åpnes, skyves eller tiltes, laminert sikkerhetsglass i terrassedørene og manuelle rullegardiner med varmeisolasjon på soverommene.',
  'Tvåglasfönster i brun PVC, öppningsbara, skjutbara eller tippbara, laminerat säkerhetsglas i altandörrarna och manuella rullgardiner med värmeisolering i sovrummen.')
a('.qualitySpecs.groups[4].items[0]',
  'Aire acondicionado frío y calor con bomba de calor, por conductos al salón, los dormitorios y la cocina.',
  'Climatisation réversible chaud et froid avec pompe à chaleur, gainée vers le séjour, les chambres et la cuisine.',
  'Klimaanlage für Kühlen und Heizen mit Wärmepumpe, über Kanäle zu Wohnzimmer, Schlafzimmern und Küche geführt.',
  'Кондиционирование на тепло и холод с тепловым насосом, с воздуховодами в гостиную, спальни и кухню.',
  'تكييف للتبريد والتدفئة بمضخة حرارية، موزَّع عبر مجارٍ هوائية إلى غرفة المعيشة وغرف النوم والمطبخ.',
  'Airconditioning voor koelen en verwarmen met een warmtepomp, via kanalen naar de woonkamer, de slaapkamers en de keuken.',
  'Klimatyzacja chłodząca i grzejąca z pompą ciepła, kanałowa, doprowadzona do salonu, sypialni i kuchni.',
  'Klimaanlegg for kjøling og oppvarming med varmepumpe, kanalført til stuen, soverommene og kjøkkenet.',
  'Luftkonditionering för kyla och värme med värmepump, kanalburen till vardagsrummet, sovrummen och köket.')
a('.qualitySpecs.groups[4].items[1]',
  'Agua caliente con caldera eléctrica con intercambiador solar alimentado por paneles solares comunitarios, o con un sistema de aerotermia solo para agua caliente, según el proyecto de ejecución.',
  'Eau chaude par chaudière électrique avec échangeur solaire alimenté par des panneaux solaires communs, ou par un système aérothermique réservé à l’eau chaude, selon le projet d’exécution.',
  'Warmwasser über einen Elektrokessel mit Solarwärmetauscher, gespeist von gemeinschaftlichen Solarpaneelen, oder über ein Aerothermie-System nur für Warmwasser, je nach Ausführungsprojekt.',
  'Горячая вода от электрического котла с солнечным теплообменником, питаемым общими солнечными панелями, или от аэротермической системы только для горячей воды, в зависимости от исполнительного проекта.',
  'ماء ساخن من سخان كهربائي بمبادل شمسي تغذّيه ألواح شمسية مشتركة، أو من نظام حراري هوائي للمياه الساخنة فقط، بحسب مشروع التنفيذ.',
  'Warm water via een elektrische boiler met zonnewarmtewisselaar, gevoed door gemeenschappelijke zonnepanelen, of via een aerothermisch systeem alleen voor warm water, afhankelijk van het uitvoeringsproject.',
  'Ciepła woda z kotła elektrycznego z wymiennikiem słonecznym zasilanym wspólnymi panelami słonecznymi lub z systemu aerotermalnego wyłącznie do ciepłej wody, zależnie od projektu wykonawczego.',
  'Varmtvann fra en elektrisk kjele med solvarmeveksler matet av felles solcellepaneler, eller fra et aerotermisk system kun for varmtvann, avhengig av gjennomføringsprosjektet.',
  'Varmvatten från en elpanna med solvärmeväxlare som matas av gemensamma solpaneler, eller från ett aerotermiskt system enbart för varmvatten, beroende på genomförandeprojektet.')
a('.qualitySpecs.groups[5].name',
  'Seguridad e instalaciones', 'Sécurité et installations', 'Sicherheit und Installationen',
  'Безопасность и инженерные системы', 'الأمان والتمديدات', 'Beveiliging en installaties',
  'Bezpieczeństwo i instalacje', 'Sikkerhet og installasjoner', 'Säkerhet och installationer')
a('.qualitySpecs.groups[5].items[0]',
  'Puerta de entrada blindada con mirilla y cerradura de seguridad, videoportero automático y llaves maestras de distintos niveles de seguridad.',
  'Porte d’entrée blindée avec judas et serrure de sécurité, visiophone automatique et clés maîtresses de différents niveaux de sécurité.',
  'Gepanzerte Wohnungseingangstür mit Türspion und Sicherheitsschloss, automatische Videosprechanlage und Generalschlüssel mit unterschiedlichen Sicherheitsstufen.',
  'Бронированная входная дверь с глазком и замком безопасности, автоматический видеодомофон и мастер-ключи разных уровней доступа.',
  'باب مدخل مدرّع بعين سحرية وقفل أمان، وجهاز اتصال مرئي آلي، ومفاتيح رئيسية بمستويات أمان مختلفة.',
  'Een gepantserde voordeur met kijkgat en veiligheidsslot, een automatische videofoon en hoofdsleutels met verschillende beveiligingsniveaus.',
  'Pancerne drzwi wejściowe z wizjerem i zamkiem bezpieczeństwa, automatyczny wideodomofon oraz klucze generalne o różnych poziomach zabezpieczenia.',
  'Panserdør med kikkhull og sikkerhetslås, automatisk videoporttelefon og hovednøkler med ulike sikkerhetsnivåer.',
  'Pansardörr med titthål och säkerhetslås, automatisk videodörrtelefon och huvudnycklar med olika säkerhetsnivåer.')
a('.qualitySpecs.groups[5].items[1]',
  'Tomas de TV y Ethernet en salón, cocina y dormitorios, iluminación exterior en terrazas y patios y un grifo de agua en los patios de planta baja y en los áticos, según proyecto.',
  'Prises TV et Ethernet dans le séjour, la cuisine et les chambres, éclairage extérieur sur les terrasses et les patios, et un robinet d’eau sur les patios du rez-de-chaussée et les penthouses, selon le projet.',
  'TV- und Ethernet-Anschlüsse in Wohnzimmer, Küche und Schlafzimmern, Außenbeleuchtung auf Terrassen und Patios sowie ein Wasserhahn auf den Erdgeschosspatios und bei den Penthouses, laut Projekt.',
  'Розетки для ТВ и Ethernet в гостиной, кухне и спальнях, наружное освещение на террасах и патио и водопроводный кран на патио первого этажа и у пентхаусов, согласно проекту.',
  'مآخذ تلفزيون وإيثرنت في غرفة المعيشة والمطبخ وغرف النوم، وإنارة خارجية في التراسات والباحات، وصنبور ماء في باحات الطابق الأرضي والبنتهاوس، بحسب المشروع.',
  'TV- en ethernetaansluitingen in de woonkamer, de keuken en de slaapkamers, buitenverlichting op de terrassen en patio’s en een waterkraan op de patio’s op de begane grond en bij de penthouses, volgens het project.',
  'Gniazda TV i Ethernet w salonie, kuchni i sypialniach, oświetlenie zewnętrzne na tarasach i patio oraz kran z wodą na patio na parterze i przy penthouse’ach, zgodnie z projektem.',
  'TV- og Ethernet-uttak i stuen, på kjøkkenet og på soverommene, utebelysning på terrassene og uteplassene og en vannkran på uteplassene i første etasje og ved toppleilighetene, i henhold til prosjektet.',
  'Tv- och Ethernet-uttag i vardagsrummet, köket och sovrummen, utebelysning på terrasserna och uteplatserna och en vattenkran på uteplatserna i bottenvåningen och vid takvåningarna, enligt projektet.')
a('.qualitySpecs.groups[6].items[0]',
  'Piscina splash de agua salada, gimnasio equipado y sala de coworking, y jardines comunitarios con iluminación y riego automático.',
  'Piscine splash à l’eau salée, salle de sport équipée et espace de coworking, et jardins communs avec éclairage et arrosage automatique.',
  'Splash-Pool mit Salzwasser, ausgestatteter Fitnessraum und Coworking-Raum sowie Gemeinschaftsgärten mit Beleuchtung und automatischer Bewässerung.',
  'Бассейн типа «сплэш» с солёной водой, оборудованный тренажёрный зал и зал коворкинга, общие сады с освещением и автоматическим поливом.',
  'مسبح من نوع سبلاش بالمياه المالحة، وصالة رياضية مجهّزة، وقاعة عمل مشترك، وحدائق مشتركة بإنارة وري آلي.',
  'Een splashzwembad met zout water, een ingerichte fitnessruimte en een coworkingruimte, en gemeenschappelijke tuinen met verlichting en automatische bewatering.',
  'Basen typu splash ze słoną wodą, wyposażona siłownia i sala coworkingowa oraz wspólne ogrody z oświetleniem i automatycznym podlewaniem.',
  'Et splashbasseng med saltvann, et utstyrt treningsrom og et coworking-rom, og felleshager med belysning og automatisk vanning.',
  'En splashpool med saltvatten, ett utrustat gym och ett coworkingrum, samt gemensamma trädgårdar med belysning och automatisk bevattning.')
a('.qualitySpecs.groups[6].items[1]',
  'Trasteros con toma de luz y desfibrilador portátil en las zonas comunes.',
  'Caves avec prise d’éclairage et défibrillateur portable dans les parties communes.',
  'Abstellräume mit Lichtanschluss und ein tragbarer Defibrillator in den Gemeinschaftsbereichen.',
  'Кладовые с выводом для освещения и портативный дефибриллятор в общих зонах.',
  'مخازن بنقطة إنارة، وجهاز إزالة رجفان محمول في المناطق المشتركة.',
  'Bergingen met een lichtaansluiting en een draagbare defibrillator in de gemeenschappelijke ruimten.',
  'Komórki lokatorskie z punktem oświetleniowym oraz przenośny defibrylator w częściach wspólnych.',
  'Boder med lysuttak og en bærbar hjertestarter i fellesarealene.',
  'Förråd med ljusuttag och en bärbar hjärtstartare i de gemensamma utrymmena.')

# ---- residences, lifestyle -------------------------------------------------------------------

a('.residences.headlineHtml',
  'Tres viviendas, <em>tres niveles</em>', 'Trois logements, <em>trois niveaux</em>',
  'Drei Wohnungen, <em>drei Ebenen</em>', 'Три квартиры, <em>три уровня</em>',
  'ثلاثة مساكن، <em>ثلاثة مستويات</em>', 'Drie woningen, <em>drie niveaus</em>',
  'Trzy lokale, <em>trzy poziomy</em>', 'Tre boliger, <em>tre nivåer</em>',
  'Tre bostäder, <em>tre nivåer</em>')
a('.residences.copy',
  'Las tres viviendas de la lista de precios están en la planta baja, la planta primera y el nivel de ático. La tabla siguiente recoge cada una con su precio.',
  'Les trois logements de la liste de prix sont au rez-de-chaussée, au premier étage et au niveau penthouse. Le tableau ci-dessous les présente chacun avec son prix.',
  'Die drei Wohnungen der Preisliste liegen im Erdgeschoss, im ersten Obergeschoss und auf der Penthouse-Ebene. Die Tabelle unten führt jede mit ihrem Preis auf.',
  'Три квартиры из прайс-листа находятся на первом этаже, на втором этаже и на уровне пентхауса. В таблице ниже каждая указана с ценой.',
  'المساكن الثلاثة الواردة في قائمة الأسعار تقع في الطابق الأرضي والطابق الأول وطابق البنتهاوس. ويعرض الجدول أدناه كلاً منها مع سعره.',
  'De drie woningen op de prijslijst liggen op de begane grond, de eerste verdieping en het penthouseniveau. De tabel hieronder toont elk met zijn prijs.',
  'Trzy lokale z cennika znajdują się na parterze, na pierwszym piętrze i na poziomie penthouse’u. Poniższa tabela podaje każdy z nich wraz z ceną.',
  'De tre boligene i prislisten ligger i første etasje, andre etasje og toppleilighetsnivået. Tabellen under viser hver av dem med pris.',
  'De tre bostäderna i prislistan ligger i bottenvåningen, på första våningen och på takvåningsnivån. Tabellen nedan visar var och en med sitt pris.')
a('.residences.items[0].name',
  'Una vivienda de dos dormitorios en planta baja', 'Un logement de deux chambres au rez-de-chaussée',
  'Eine Wohnung mit zwei Schlafzimmern im Erdgeschoss', 'Квартира с двумя спальнями на первом этаже',
  'مسكن بغرفتي نوم في الطابق الأرضي', 'Een woning met twee slaapkamers op de begane grond',
  'Lokal z dwiema sypialniami na parterze', 'En bolig med to soverom i første etasje',
  'En bostad med två sovrum i bottenvåningen')
a('.residences.items[0].points[0]',
  'Vivienda 2-4-0-B, en el bloque 2, portal 4, orientada al suroeste: dos dormitorios y dos baños, con {N66.86} {U} interiores.',
  'Logement 2-4-0-B, dans le bloc 2, entrée 4, orienté sud-ouest : deux chambres et deux salles de bain, avec {N66.86} {U} intérieurs.',
  'Wohnung 2-4-0-B, in Block 2, Eingang 4, nach Südwesten ausgerichtet: zwei Schlafzimmer und zwei Bäder, mit {N66.86} {U} Innenfläche.',
  'Квартира 2-4-0-B, в корпусе 2, подъезд 4, окна на юго-запад: две спальни и две ванные комнаты, {N66.86} {U} внутри.',
  'المسكن 2-4-0-B، في المبنى 2 عند المدخل 4، باتجاه الجنوب الغربي: غرفتا نوم وحمّامان، بمساحة داخلية {N66.86} {U}.',
  'Woning 2-4-0-B, in blok 2, portiek 4, op het zuidwesten gericht: twee slaapkamers en twee badkamers, met {N66.86} {U} binnenruimte.',
  'Lokal 2-4-0-B, w bloku 2, klatka 4, z orientacją południowo-zachodnią: dwie sypialnie i dwie łazienki, z {N66.86} {U} powierzchni wnętrza.',
  'Bolig 2-4-0-B, i blokk 2, oppgang 4, vendt mot sørvest: to soverom og to bad, med {N66.86} {U} innvendig.',
  'Bostad 2-4-0-B, i hus 2, trapphus 4, vänd mot sydväst: två sovrum och två badrum, med {N66.86} {U} inomhus.')
a('.residences.items[0].points[1]',
  'Una terraza cubierta de {N13.00} {U} y una terraza descubierta de {N11.89} {U}, una junto a otra.',
  'Une terrasse couverte de {N13.00} {U} et une terrasse découverte de {N11.89} {U}, côte à côte.',
  'Eine überdachte Terrasse von {N13.00} {U} und eine unüberdachte Terrasse von {N11.89} {U}, nebeneinander.',
  'Крытая терраса {N13.00} {U} и открытая терраса {N11.89} {U} рядом друг с другом.',
  'تراس مسقوف مساحته {N13.00} {U} وتراس مكشوف مساحته {N11.89} {U}، متجاوران.',
  'Een overdekt terras van {N13.00} {U} en een open terras van {N11.89} {U}, naast elkaar.',
  'Taras zadaszony o powierzchni {N13.00} {U} i taras niezadaszony o powierzchni {N11.89} {U}, obok siebie.',
  'En overdekket terrasse på {N13.00} {U} og en åpen terrasse på {N11.89} {U}, side om side.',
  'En övertäckt terrass på {N13.00} {U} och en öppen terrass på {N11.89} {U}, sida vid sida.')
a('.residences.items[0].points[2]',
  'Una plaza de garaje y un trastero numerados en la lista, por {E365000} antes de {T}.',
  'Une place de garage et une cave numérotées sur la liste, pour {E365000} hors {T}.',
  'Ein nummerierter Garagenstellplatz und Abstellraum laut Liste, für {E365000} vor {T}.',
  'Пронумерованные машиноместо и кладовая в списке, за {E365000} без {T}.',
  'موقف سيارات في المرآب ومخزن مرقّمان في القائمة، بسعر {E365000} قبل {T}.',
  'Een genummerde garageplaats en berging op de lijst, voor {E365000} exclusief {T}.',
  'Numerowane miejsce garażowe i komórka lokatorska w wykazie, za {E365000} bez {T}.',
  'En nummerert garasjeplass og bod i listen, for {E365000} før {T}.',
  'En numrerad garageplats och ett förråd i listan, för {E365000} före {T}.')
a('.residences.items[1].points[0]',
  'Vivienda 2-4-1-A, en el bloque 2, portal 4, orientada al suroeste: tres dormitorios y dos baños, con {N84.52} {U} interiores.',
  'Logement 2-4-1-A, dans le bloc 2, entrée 4, orienté sud-ouest : trois chambres et deux salles de bain, avec {N84.52} {U} intérieurs.',
  'Wohnung 2-4-1-A, in Block 2, Eingang 4, nach Südwesten ausgerichtet: drei Schlafzimmer und zwei Bäder, mit {N84.52} {U} Innenfläche.',
  'Квартира 2-4-1-A, в корпусе 2, подъезд 4, окна на юго-запад: три спальни и две ванные комнаты, {N84.52} {U} внутри.',
  'المسكن 2-4-1-A، في المبنى 2 عند المدخل 4، باتجاه الجنوب الغربي: ثلاث غرف نوم وحمّامان، بمساحة داخلية {N84.52} {U}.',
  'Woning 2-4-1-A, in blok 2, portiek 4, op het zuidwesten gericht: drie slaapkamers en twee badkamers, met {N84.52} {U} binnenruimte.',
  'Lokal 2-4-1-A, w bloku 2, klatka 4, z orientacją południowo-zachodnią: trzy sypialnie i dwie łazienki, z {N84.52} {U} powierzchni wnętrza.',
  'Bolig 2-4-1-A, i blokk 2, oppgang 4, vendt mot sørvest: tre soverom og to bad, med {N84.52} {U} innvendig.',
  'Bostad 2-4-1-A, i hus 2, trapphus 4, vänd mot sydväst: tre sovrum och två badrum, med {N84.52} {U} inomhus.')
a('.residences.items[1].points[1]',
  'Una terraza cubierta de {N18.87} {U}.', 'Une terrasse couverte de {N18.87} {U}.',
  'Eine überdachte Terrasse von {N18.87} {U}.', 'Крытая терраса {N18.87} {U}.',
  'تراس مسقوف مساحته {N18.87} {U}.', 'Een overdekt terras van {N18.87} {U}.',
  'Taras zadaszony o powierzchni {N18.87} {U}.', 'En overdekket terrasse på {N18.87} {U}.',
  'En övertäckt terrass på {N18.87} {U}.')
a('.residences.items[1].points[2]',
  'Una plaza de garaje y un trastero numerados en la lista, por {E480000} antes de {T}.',
  'Une place de garage et une cave numérotées sur la liste, pour {E480000} hors {T}.',
  'Ein nummerierter Garagenstellplatz und Abstellraum laut Liste, für {E480000} vor {T}.',
  'Пронумерованные машиноместо и кладовая в списке, за {E480000} без {T}.',
  'موقف سيارات في المرآب ومخزن مرقّمان في القائمة، بسعر {E480000} قبل {T}.',
  'Een genummerde garageplaats en berging op de lijst, voor {E480000} exclusief {T}.',
  'Numerowane miejsce garażowe i komórka lokatorska w wykazie, za {E480000} bez {T}.',
  'En nummerert garasjeplass og bod i listen, for {E480000} før {T}.',
  'En numrerad garageplats och ett förråd i listan, för {E480000} före {T}.')
a('.residences.items[2].name',
  'Un ático de dos dormitorios', 'Un penthouse de deux chambres', 'Ein Penthouse mit zwei Schlafzimmern',
  'Пентхаус с двумя спальнями', 'بنتهاوس بغرفتي نوم', 'Een penthouse met twee slaapkamers',
  'Penthouse z dwiema sypialniami', 'En toppleilighet med to soverom', 'En takvåning med två sovrum')
a('.residences.items[2].points[0]',
  'Vivienda 3-6-PH-B, en el bloque 3, portal 6, orientada al sureste: dos dormitorios y dos baños, con {N73.46} {U} interiores.',
  'Logement 3-6-PH-B, dans le bloc 3, entrée 6, orienté sud-est : deux chambres et deux salles de bain, avec {N73.46} {U} intérieurs.',
  'Wohnung 3-6-PH-B, in Block 3, Eingang 6, nach Südosten ausgerichtet: zwei Schlafzimmer und zwei Bäder, mit {N73.46} {U} Innenfläche.',
  'Квартира 3-6-PH-B, в корпусе 3, подъезд 6, окна на юго-восток: две спальни и две ванные комнаты, {N73.46} {U} внутри.',
  'المسكن 3-6-PH-B، في المبنى 3 عند المدخل 6، باتجاه الجنوب الشرقي: غرفتا نوم وحمّامان، بمساحة داخلية {N73.46} {U}.',
  'Woning 3-6-PH-B, in blok 3, portiek 6, op het zuidoosten gericht: twee slaapkamers en twee badkamers, met {N73.46} {U} binnenruimte.',
  'Lokal 3-6-PH-B, w bloku 3, klatka 6, z orientacją południowo-wschodnią: dwie sypialnie i dwie łazienki, z {N73.46} {U} powierzchni wnętrza.',
  'Bolig 3-6-PH-B, i blokk 3, oppgang 6, vendt mot sørøst: to soverom og to bad, med {N73.46} {U} innvendig.',
  'Bostad 3-6-PH-B, i hus 3, trapphus 6, vänd mot sydost: två sovrum och två badrum, med {N73.46} {U} inomhus.')
a('.residences.items[2].points[1]',
  'Una terraza de ático de {N37.03} {U}, indicada como descubierta.',
  'Une terrasse de penthouse de {N37.03} {U}, indiquée comme découverte.',
  'Eine Penthouse-Terrasse von {N37.03} {U}, als unüberdacht angegeben.',
  'Терраса пентхауса {N37.03} {U}, в списке указана как открытая.',
  'تراس بنتهاوس مساحته {N37.03} {U}، مدرج على أنه مكشوف.',
  'Een penthouseterras van {N37.03} {U}, vermeld als open.',
  'Taras penthouse’u o powierzchni {N37.03} {U}, podany jako niezadaszony.',
  'En toppleilighetsterrasse på {N37.03} {U}, oppført som åpen.',
  'En takvåningsterrass på {N37.03} {U}, listad som öppen.')
a('.residences.items[2].points[2]',
  'Una plaza de garaje y un trastero numerados en la lista, por {E530000} antes de {T}.',
  'Une place de garage et une cave numérotées sur la liste, pour {E530000} hors {T}.',
  'Ein nummerierter Garagenstellplatz und Abstellraum laut Liste, für {E530000} vor {T}.',
  'Пронумерованные машиноместо и кладовая в списке, за {E530000} без {T}.',
  'موقف سيارات في المرآب ومخزن مرقّمان في القائمة، بسعر {E530000} قبل {T}.',
  'Een genummerde garageplaats en berging op de lijst, voor {E530000} exclusief {T}.',
  'Numerowane miejsce garażowe i komórka lokatorska w wykazie, za {E530000} bez {T}.',
  'En nummerert garasjeplass og bod i listen, for {E530000} før {T}.',
  'En numrerad garageplats och ett förråd i listan, för {E530000} före {T}.')
a('.lifestyle.headlineHtml',
  'Una piscina central, <em>un gimnasio y un club social</em>',
  'Une piscine centrale, <em>une salle de sport et un club social</em>',
  'Ein zentraler Pool, <em>ein Fitnessraum und ein Social Club</em>',
  'Центральный бассейн, <em>тренажёрный зал и клуб для жильцов</em>',
  'مسبح مركزي، <em>وصالة رياضية ونادٍ اجتماعي</em>',
  'Een centraal zwembad, <em>een fitnessruimte en een sociale club</em>',
  'Centralny basen, <em>siłownia i klub dla mieszkańców</em>',
  'Et sentralt basseng, <em>et treningsrom og en sosial klubb</em>',
  'En central pool, <em>ett gym och en social klubb</em>')
a('.lifestyle.copy',
  'Los espacios comunes se agrupan en torno a una piscina central, en jardines de más de {N13,000} {U}, con gimnasio, sala de coworking y club social.',
  'Les espaces communs sont regroupés autour d’une piscine centrale, dans des jardins de plus de {N13,000} {U}, avec salle de sport, espace de coworking et club social.',
  'Die Gemeinschaftsflächen gruppieren sich um einen zentralen Pool, in Gärten von mehr als {N13,000} {U}, mit Fitnessraum, Coworking-Raum und Social Club.',
  'Общие пространства сгруппированы вокруг центрального бассейна, в садах площадью более {N13,000} {U}, с тренажёрным залом, залом коворкинга и клубом для жильцов.',
  'تتجمع المرافق المشتركة حول مسبح مركزي، في حدائق تزيد مساحتها على {N13,000} {U}، مع صالة رياضية وقاعة عمل مشترك ونادٍ اجتماعي.',
  'De gemeenschappelijke ruimten zijn gegroepeerd rond een centraal zwembad, in tuinen van meer dan {N13,000} {U}, met een fitnessruimte, een coworkingruimte en een sociale club.',
  'Części wspólne skupiają się wokół centralnego basenu, w ogrodach o powierzchni ponad {N13,000} {U}, z siłownią, salą coworkingową i klubem dla mieszkańców.',
  'Fellesarealene er samlet rundt et sentralt basseng, i hager på mer enn {N13,000} {U}, med treningsrom, coworking-rom og sosial klubb.',
  'De gemensamma ytorna är samlade kring en central pool, i trädgårdar på mer än {N13,000} {U}, med gym, coworkingrum och social klubb.')
a('.lifestyle.panels[0][1]',
  'Una piscina central con zona chill-out y tumbonas, que la memoria de calidades describe como piscina splash de agua salada.',
  'Une piscine centrale avec espace chill-out et transats, que le descriptif de qualité décrit comme une piscine splash à l’eau salée.',
  'Ein zentraler Pool mit Chill-out-Bereich und Liegen, den die Baubeschreibung als Splash-Pool mit Salzwasser beschreibt.',
  'Центральный бассейн с зоной отдыха и шезлонгами; в описании качества он назван бассейном типа «сплэш» с солёной водой.',
  'مسبح مركزي مع ركن استرخاء ومقاعد طويلة، تصفه وثيقة المواصفات بأنه مسبح من نوع سبلاش بالمياه المالحة.',
  'Een centraal zwembad met een chill-outzone en ligbedden, dat de technische omschrijving beschrijft als een splashzwembad met zout water.',
  'Centralny basen ze strefą relaksu i leżakami, który standard wykończenia opisuje jako basen typu splash ze słoną wodą.',
  'Et sentralt basseng med chill-out-sone og solsenger, som byggebeskrivelsen beskriver som et splashbasseng med saltvann.',
  'En central pool med chill-out-zon och solstolar, som byggbeskrivningen beskriver som en splashpool med saltvatten.')
a('.lifestyle.panels[1][1]',
  'Un gimnasio equipado y una sala de coworking que la memoria de calidades incluye entre las zonas comunes.',
  'Une salle de sport équipée et un espace de coworking que le descriptif de qualité range parmi les parties communes.',
  'Ein ausgestatteter Fitnessraum und ein Coworking-Raum, den die Baubeschreibung zu den Gemeinschaftsbereichen zählt.',
  'Оборудованный тренажёрный зал и зал коворкинга, который в описании качества отнесён к общим зонам.',
  'صالة رياضية مجهّزة وقاعة عمل مشترك تدرجها وثيقة المواصفات ضمن المناطق المشتركة.',
  'Een ingerichte fitnessruimte en een coworkingruimte die de technische omschrijving onder de gemeenschappelijke ruimten rekent.',
  'Wyposażona siłownia i sala coworkingowa, którą standard wykończenia zalicza do części wspólnych.',
  'Et utstyrt treningsrom og et coworking-rom som byggebeskrivelsen regner blant fellesarealene.',
  'Ett utrustat gym och ett coworkingrum som byggbeskrivningen räknar bland de gemensamma ytorna.')
a('.lifestyle.panels[2][1]',
  'Un club social que los renders muestran como una sala larga con una encimera de cocina, dos mesas grandes y una apertura acristalada a una terraza.',
  'Un club social que les rendus montrent comme une longue salle avec un plan de cuisine, deux grandes tables et une ouverture vitrée sur une terrasse.',
  'Ein Social Club, den die Renderings als langen Raum mit Küchenzeile, zwei großen Tischen und einer verglasten Öffnung zu einer Terrasse zeigen.',
  'Клуб для жильцов, который на визуализациях выглядит как длинный зал с кухонной стойкой, двумя большими столами и остеклённым выходом на террасу.',
  'نادٍ اجتماعي تُظهره الصور المولَّدة قاعة طويلة فيها منضدة مطبخ وطاولتان كبيرتان وفتحة زجاجية على تراس.',
  'Een sociale club die de renders tonen als een lange ruimte met een keukenblok, twee grote tafels en een glazen opening naar een terras.',
  'Klub dla mieszkańców, który wizualizacje pokazują jako długie pomieszczenie z blatem kuchennym, dwoma dużymi stołami i przeszklonym wyjściem na taras.',
  'En sosial klubb som bildene viser som et langt rom med en kjøkkenbenk, to store bord og en glassåpning mot en terrasse.',
  'En social klubb som bilderna visar som ett långt rum med en köksbänk, två stora bord och en glasad öppning mot en terrass.')
a('.lifestyle.panels[3][0]',
  'Jardines y barbacoas', 'Jardins et barbecues', 'Gärten und Grillplätze', 'Сады и барбекю',
  'الحدائق وأماكن الشواء', 'Tuinen en barbecues', 'Ogrody i grille', 'Hager og grillplasser', 'Trädgårdar och grillplatser')
a('.lifestyle.panels[3][1]',
  'Más de {N13,000} {U} de jardines con iluminación y riego automático, y una zona de barbacoa y pícnic para reunirse con amigos o familia.',
  'Plus de {N13,000} {U} de jardins avec éclairage et arrosage automatique, et un espace barbecue et pique-nique pour se retrouver entre amis ou en famille.',
  'Mehr als {N13,000} {U} Gärten mit Beleuchtung und automatischer Bewässerung sowie ein Grill- und Picknickbereich für Treffen mit Freunden oder Familie.',
  'Более {N13,000} {U} садов с освещением и автоматическим поливом, а также зона барбекю и пикника для встреч с друзьями или семьёй.',
  'أكثر من {N13,000} {U} من الحدائق بإنارة وري آلي، ومنطقة شواء ونزهات للقاءات مع الأصدقاء أو العائلة.',
  'Meer dan {N13,000} {U} tuinen met verlichting en automatische bewatering, en een barbecue- en picknickzone om vrienden of familie te ontvangen.',
  'Ponad {N13,000} {U} ogrodów z oświetleniem i automatycznym podlewaniem oraz strefa grillowa i piknikowa na spotkania z przyjaciółmi lub rodziną.',
  'Mer enn {N13,000} {U} hager med belysning og automatisk vanning, og et grill- og piknikområde for sammenkomster med venner eller familie.',
  'Mer än {N13,000} {U} trädgårdar med belysning och automatisk bevattning, och en grill- och picknickyta för sammankomster med vänner eller familj.')
a('.lifestyle.panels[4][0]',
  'El parque de al lado', 'Le parc voisin', 'Der Park nebenan', 'Парк по соседству',
  'الحديقة المجاورة', 'Het park ernaast', 'Park obok', 'Parken ved siden av', 'Parken intill')
a('.lifestyle.panels[4][1]',
  'El catálogo sitúa junto a la promoción un gran parque, el Gran Parque de la Costa del Sol, con más de {N2,000} árboles, y dice que tendrá un anfiteatro al aire libre, una pista de atletismo, un carril bici, un skate park, un lago navegable y un rocódromo.',
  'Le catalogue place à côté de l’ensemble un grand parc, le Gran Parque de la Costa del Sol, avec plus de {N2,000} arbres, et indique qu’il aura un amphithéâtre en plein air, une piste de course, une piste cyclable, un skatepark, un lac navigable et un mur d’escalade.',
  'Der Katalog verortet neben der Anlage einen großen Park, den Gran Parque de la Costa del Sol, mit mehr als {N2,000} Bäumen, und nennt ein Freilufttheater, eine Laufbahn, einen Radweg, einen Skatepark, einen befahrbaren See und eine Kletterwand.',
  'В каталоге рядом с комплексом указан большой парк, Gran Parque de la Costa del Sol, с более чем {N2,000} деревьев, и сказано, что в нём будут амфитеатр под открытым небом, беговая дорожка, велодорожка, скейт-парк, озеро для катания на лодках и скалодром.',
  'يضع الكتالوج بجوار المشروع حديقة كبيرة هي Gran Parque de la Costa del Sol، فيها أكثر من {N2,000} شجرة، ويذكر أنها ستضم مسرحاً مفتوحاً ومضمار جري ومسار دراجات ومتنزهاً للتزلج وبحيرة صالحة للإبحار وجداراً للتسلق.',
  'De catalogus plaatst naast het project een groot park, het Gran Parque de la Costa del Sol, met meer dan {N2,000} bomen, en zegt dat het een openluchtamfitheater, een looppiste, een fietspad, een skatepark, een bevaarbaar meer en een klimwand zal krijgen.',
  'Katalog umieszcza obok inwestycji duży park, Gran Parque de la Costa del Sol, z ponad {N2,000} drzew, i podaje, że znajdą się w nim amfiteatr na wolnym powietrzu, bieżnia, ścieżka rowerowa, skatepark, żeglowne jezioro i ścianka wspinaczkowa.',
  'Katalogen plasserer en stor park ved siden av prosjektet, Gran Parque de la Costa del Sol, med mer enn {N2,000} trær, og sier at den skal få et amfi under åpen himmel, en løpebane, en sykkelsti, en skatepark, en seilbar innsjø og en klatrevegg.',
  'Katalogen placerar en stor park intill projektet, Gran Parque de la Costa del Sol, med mer än {N2,000} träd, och anger att den ska få en friluftsamfiteater, en löparbana, en cykelbana, en skatepark, en segelbar sjö och en klättervägg.')

# ---- location, investment, trust ---------------------------------------------------------------

a('.location.headlineHtml',
  'Mijas Costa, <em>entre el parque y la costa</em>', 'Mijas Costa, <em>entre le parc et la côte</em>',
  'Mijas Costa, <em>zwischen Park und Küste</em>', 'Михас-Коста, <em>между парком и побережьем</em>',
  'ميخاس كوستا، <em>بين الحديقة والساحل</em>', 'Mijas Costa, <em>tussen het park en de kust</em>',
  'Mijas Costa, <em>między parkiem a wybrzeżem</em>', 'Mijas Costa, <em>mellom parken og kysten</em>',
  'Mijas Costa, <em>mellan parken och kusten</em>')
a('.location.copy',
  'El catálogo sitúa las viviendas en Mijas Costa, con la autovía a menos de diez minutos en dirección a Marbella y Estepona. Su plano dibuja círculos a 800 m y 2 km alrededor del solar: el parque, un club de pádel, un hipódromo y centro hípico y el Cerrado del Águila Golf Resort quedan en el círculo de 800 m o dentro de él, Chaparral Golf queda dentro del de 2 km y los dos centros comerciales de Miramar quedan a unos 2 km. Los documentos no dan dirección ni coordenadas de la parcela, así que nuestro mapa muestra la zona de Mijas Costa.',
  'Le catalogue situe les logements à Mijas Costa, l’autoroute étant à moins de dix minutes en direction de Marbella et d’Estepona. Sa carte trace des cercles à 800 m et 2 km autour du terrain : le parc, un club de padel, un hippodrome et centre équestre et le Cerrado del Águila Golf Resort se trouvent sur le cercle de 800 m ou à l’intérieur, Chaparral Golf à l’intérieur de celui de 2 km et les deux centres commerciaux de Miramar à environ 2 km. Les documents ne donnent ni adresse ni coordonnées de la parcelle ; notre carte montre donc la zone de Mijas Costa.',
  'Der Katalog verortet die Wohnungen in Mijas Costa, mit der Autobahn weniger als zehn Minuten entfernt in Richtung Marbella und Estepona. Seine Karte zieht Ringe von 800 m und 2 km um das Grundstück: Der Park, ein Padelclub, eine Pferderennbahn mit Reitzentrum und das Cerrado del Águila Golf Resort liegen auf oder innerhalb des 800-m-Rings, Chaparral Golf innerhalb des 2-km-Rings und die beiden Einkaufszentren Miramar bei etwa 2 km. Die Unterlagen nennen weder Adresse noch Koordinaten des Grundstücks; unsere Karte zeigt daher das Gebiet Mijas Costa.',
  'В каталоге квартиры расположены в Михас-Коста, а до автомагистрали менее десяти минут в сторону Марбельи и Эстепоны. На его карте вокруг участка проведены круги в 800 м и 2 км: парк, падел-клуб, ипподром с конным центром и Cerrado del Águila Golf Resort находятся на круге в 800 м или внутри него, Chaparral Golf — внутри круга в 2 км, а два торговых центра Miramar — примерно в 2 км. В документах нет ни адреса, ни координат участка, поэтому на нашей карте показан район Михас-Коста.',
  'يضع الكتالوج المساكن في ميخاس كوستا، والطريق السريع على بعد أقل من عشر دقائق باتجاه ماربيا وإستيبونا. وترسم خريطته دوائر على بعد 800 م و2 كم حول الموقع: فالحديقة ونادي بادل وحلبة سباق خيل ومركز فروسية ومنتجع Cerrado del Águila للغولف تقع عند دائرة الـ800 م أو داخلها، ويقع Chaparral Golf داخل دائرة الـ2 كم، ويقع مركزا Miramar التجاريان على بعد نحو 2 كم. ولا تعطي الوثائق عنواناً أو إحداثيات للقطعة، لذلك تُظهر خريطتنا منطقة ميخاس كوستا.',
  'De catalogus plaatst de woningen in Mijas Costa, met de snelweg op minder dan tien minuten richting Marbella en Estepona. Op de kaart staan cirkels van 800 m en 2 km rond het terrein: het park, een padelclub, een renbaan met paardensportcentrum en het Cerrado del Águila Golf Resort liggen op of binnen de cirkel van 800 m, Chaparral Golf ligt binnen de cirkel van 2 km en de twee winkelcentra van Miramar liggen op ongeveer 2 km. De documenten geven geen adres of coördinaten van het perceel, dus onze kaart toont het gebied Mijas Costa.',
  'Katalog umieszcza lokale w Mijas Costa, z autostradą w mniej niż dziesięć minut w stronę Marbelli i Estepony. Jego mapa rysuje okręgi 800 m i 2 km wokół terenu: park, klub padla, tor wyścigowy z ośrodkiem jeździeckim i Cerrado del Águila Golf Resort leżą na okręgu 800 m lub wewnątrz niego, Chaparral Golf wewnątrz okręgu 2 km, a dwa centra handlowe Miramar około 2 km od inwestycji. Dokumenty nie podają adresu ani współrzędnych działki, więc nasza mapa pokazuje obszar Mijas Costa.',
  'Katalogen plasserer boligene i Mijas Costa, med motorveien mindre enn ti minutter unna i retning Marbella og Estepona. Kartet tegner ringer på 800 m og 2 km rundt tomten: parken, en padelklubb, en travbane med ridesenter og Cerrado del Águila Golf Resort ligger på eller innenfor ringen på 800 m, Chaparral Golf innenfor ringen på 2 km og de to kjøpesentrene Miramar på omtrent 2 km. Dokumentene oppgir ingen adresse eller koordinater for tomten, så kartet vårt viser området Mijas Costa.',
  'Katalogen placerar bostäderna i Mijas Costa, med motorvägen mindre än tio minuter bort mot Marbella och Estepona. Dess karta ritar ringar på 800 m och 2 km kring tomten: parken, en padelklubb, en galoppbana med ridcenter och Cerrado del Águila Golf Resort ligger på eller innanför ringen på 800 m, Chaparral Golf innanför ringen på 2 km och de två köpcentren Miramar cirka 2 km bort. Dokumenten anger ingen adress eller koordinat för tomten, så vår karta visar området Mijas Costa.')
a('.location.distances[0][1]',
  'Unos 800 m en el plano del promotor', 'Environ 800 m sur la carte du promoteur',
  'Etwa 800 m auf der Karte des Bauträgers', 'Около 800 м по карте застройщика',
  'نحو 800 م على خريطة المطوّر', 'Ongeveer 800 m op de kaart van de ontwikkelaar',
  'Około 800 m na mapie dewelopera', 'Omtrent 800 m på utbyggerens kart',
  'Cirka 800 m på exploatörens karta')
a('.location.distances[1][1]',
  'A menos de 800 m en el plano del promotor', 'À moins de 800 m sur la carte du promoteur',
  'Innerhalb von 800 m auf der Karte des Bauträgers', 'В пределах 800 м по карте застройщика',
  'ضمن 800 م على خريطة المطوّر', 'Binnen 800 m op de kaart van de ontwikkelaar',
  'W promieniu 800 m na mapie dewelopera', 'Innenfor 800 m på utbyggerens kart',
  'Inom 800 m på exploatörens karta')
a('.location.distances[2][0]',
  'Centros comerciales de Miramar', 'Centres commerciaux de Miramar', 'Einkaufszentren Miramar',
  'Торговые центры Miramar', 'مراكز Miramar التجارية', 'Winkelcentra Miramar',
  'Centra handlowe Miramar', 'Kjøpesentrene Miramar', 'Köpcentren Miramar')
a('.location.distances[2][1]',
  'Unos 2 km en el plano del promotor', 'Environ 2 km sur la carte du promoteur',
  'Etwa 2 km auf der Karte des Bauträgers', 'Около 2 км по карте застройщика',
  'نحو 2 كم على خريطة المطوّر', 'Ongeveer 2 km op de kaart van de ontwikkelaar',
  'Około 2 km na mapie dewelopera', 'Omtrent 2 km på utbyggerens kart',
  'Cirka 2 km på exploatörens karta')
a('.location.distances[3][1]', '40 km', '40 km', '40 km', '40 км', '40 كم', '40 km', '40 km', '40 km', '40 km')
a('.location.distances[4][1]', '41 km', '41 km', '41 km', '41 км', '41 كم', '41 km', '41 km', '41 km', '41 km')
a('.investment.copy',
  'Lo que dicen los documentos del promotor sobre el precio, los pagos y las fechas, y lo que dejan fuera.',
  'Ce que disent les documents du promoteur sur le prix, les paiements et les dates, et ce qu’ils laissent de côté.',
  'Was die Unterlagen des Bauträgers zu Preis, Zahlungen und Terminen sagen und was sie offenlassen.',
  'Что говорят документы застройщика о цене, платежах и сроках и о чём они умалчивают.',
  'ما تقوله وثائق المطوّر عن السعر والدفعات والمواعيد، وما تتركه دون ذكر.',
  'Wat de documenten van de ontwikkelaar zeggen over de prijs, de betalingen en de data, en wat ze weglaten.',
  'Co dokumenty dewelopera mówią o cenie, płatnościach i terminach i czego nie mówią.',
  'Hva utbyggerens dokumenter sier om prisen, betalingene og datoene, og hva de utelater.',
  'Vad exploatörens dokument säger om priset, betalningarna och datumen, och vad de utelämnar.')
a('.investment.cards[0][1]',
  'La lista de precios dice que el {T} no está incluido. El {T} del 10 % y el impuesto de actos jurídicos documentados del 1,20 % suponen unos {E41000} más para la vivienda más barata y unos {E59000} más para el ático, antes de los gastos de notaría y registro.',
  'La liste de prix précise que la {T} n’est pas incluse. La {T} à 10 % et le droit de timbre à 1,20 % ajoutent environ {E41000} au logement le moins cher et environ {E59000} au penthouse, avant les frais de notaire et de registre foncier.',
  'Die Preisliste besagt, dass die {T} nicht enthalten ist. {T} von 10 % und Stempelsteuer von 1,20 % erhöhen die günstigste Wohnung um rund {E41000} und das Penthouse um rund {E59000}, vor Notar- und Grundbuchgebühren.',
  'В прайс-листе сказано, что {T} не включён. {T} по ставке 10 % и гербовый сбор 1,20 % добавляют около {E41000} к самой недорогой квартире и около {E59000} к пентхаусу, до расходов на нотариуса и регистрацию.',
  'تنص قائمة الأسعار على أن {T} غير مشمولة. وتضيف {T} بنسبة 10% وضريبة الدمغة بنسبة 1.20% نحو {E41000} إلى أرخص مسكن ونحو {E59000} إلى البنتهاوس، قبل رسوم الكاتب العدل والسجل العقاري.',
  'De prijslijst zegt dat de {T} niet is inbegrepen. {T} van 10% en zegelrecht van 1,20% voegen ongeveer {E41000} toe aan de goedkoopste woning en ongeveer {E59000} aan het penthouse, vóór de kosten van notaris en kadaster.',
  'Cennik podaje, że {T} nie jest wliczony. {T} w wysokości 10% i podatek od czynności dokumentowanych w wysokości 1,20% dodają około {E41000} do najtańszego lokalu i około {E59000} do penthouse’u, przed opłatami notarialnymi i wpisem do księgi wieczystej.',
  'Prislisten sier at {T} ikke er inkludert. {T} på 10 % og dokumentavgift på 1,20 % legger til omtrent {E41000} på den billigste boligen og omtrent {E59000} på toppleiligheten, før notar- og tinglysingsgebyrer.',
  'Prislistan anger att {T} inte ingår. {T} på 10 % och stämpelskatt på 1,20 % lägger till cirka {E41000} på den billigaste bostaden och cirka {E59000} på takvåningen, före notarie- och fastighetsregisteravgifter.')
a('.investment.cards[1][0]',
  'La fecha de entrega solo figura en las condiciones de pago', 'La date de livraison ne figure que dans les conditions de paiement',
  'Das Lieferdatum steht nur in den Zahlungsbedingungen', 'Срок сдачи указан только в условиях оплаты',
  'موعد التسليم وارد في شروط الدفع فقط', 'De opleverdatum staat alleen in de betalingsvoorwaarden',
  'Termin oddania jest podany tylko w warunkach płatności', 'Leveringsdatoen står bare i betalingsvilkårene',
  'Leveransdatumet finns bara i betalningsvillkoren')
a('.investment.cards[1][1]',
  'El cuarto trimestre de 2027 aparece como fecha de la escritura, al terminar y entregar las llaves. No figura en el catálogo, la memoria de calidades ni la lista de precios, así que lo pedimos en el contrato, junto con lo que ocurre si se retrasa.',
  'Le quatrième trimestre 2027 apparaît comme date de l’acte, à l’achèvement et à la remise des clés. Il ne figure ni dans le catalogue, ni dans le descriptif de qualité, ni dans la liste de prix ; nous le demandons donc dans le contrat, avec ce qui se passe en cas de retard.',
  'Das vierte Quartal 2027 erscheint als Datum der Beurkundung, bei Fertigstellung und Schlüsselübergabe. Im Katalog, in der Baubeschreibung und in der Preisliste steht es nicht, daher verlangen wir es im Vertrag, samt der Regelung für den Fall einer Verzögerung.',
  'Четвёртый квартал 2027 года указан как дата нотариального акта, при завершении и передаче ключей. В каталоге, описании качества и прайс-листе его нет, поэтому мы просим закрепить его в договоре вместе с последствиями задержки.',
  'يرد الربع الرابع من عام 2027 موعداً لسند الملكية، عند الإنجاز وتسليم المفاتيح. وهو غير مذكور في الكتالوج ولا في وثيقة المواصفات ولا في قائمة الأسعار، لذلك نطلبه في العقد مع ما يترتب على التأخر.',
  'Het vierde kwartaal van 2027 staat als datum van de akte, bij oplevering en sleuteloverdracht. Het staat niet in de catalogus, de technische omschrijving of de prijslijst, dus we vragen het in het contract, met wat er gebeurt als het uitloopt.',
  'Czwarty kwartał 2027 roku pojawia się jako termin aktu notarialnego, przy zakończeniu i przekazaniu kluczy. Nie ma go w katalogu, w standardzie wykończenia ani w cenniku, więc prosimy o jego wpisanie do umowy wraz z zapisem, co się stanie w razie opóźnienia.',
  'Fjerde kvartal 2027 står som dato for skjøtet, ved ferdigstillelse og nøkkeloverlevering. Det står ikke i katalogen, byggebeskrivelsen eller prislisten, så vi ber om det i kontrakten, sammen med hva som skjer hvis det forsinkes.',
  'Fjärde kvartalet 2027 anges som datum för lagfarten, vid färdigställande och nyckelöverlämnande. Det står inte i katalogen, byggbeskrivningen eller prislistan, så vi ber om det i avtalet, tillsammans med vad som händer om det försenas.')
a('.investment.cards[2][0]',
  'Una cuota tiene fecha fija', 'Une échéance est fixée par date', 'Eine Rate ist datumsfest',
  'Один платёж привязан к дате', 'دفعة واحدة محددة بتاريخ', 'Eén termijn ligt vast op een datum',
  'Jedna rata jest ustalona co do dnia', 'Én termin er fastsatt etter dato', 'En delbetalning är bunden till datum')
a('.investment.cards[2][1]',
  'El segundo 15 % más {T} vence el 5 de mayo de 2027, sea cual sea el estado de las obras. Preguntamos qué dice el contrato si las obras van con retraso.',
  'Les 15 % suivants hors {T} sont dus le 5 mai 2027, quel que soit l’avancement des travaux. Nous demandons ce que dit le contrat si les travaux sont en retard.',
  'Die zweiten 15 % zuzüglich {T} fallen am 5. Mai 2027 an, unabhängig vom Baustand. Wir fragen, was der Vertrag regelt, wenn die Bauarbeiten im Rückstand sind.',
  'Вторые 15 % плюс {T} подлежат оплате 5 мая 2027 года независимо от стадии строительства. Мы уточняем, что говорит договор, если работы отстают.',
  'تُستحق الدفعة الثانية البالغة 15% زائد {T} في 5 مايو 2027 أياً كانت مرحلة الأعمال. ونسأل عما ينص عليه العقد إذا تأخرت الأعمال.',
  'De tweede 15% plus {T} valt op 5 mei 2027, wat de stand van de werken ook is. We vragen wat het contract zegt als de werken achterlopen.',
  'Druga transza 15% plus {T} przypada 5 maja 2027 roku, niezależnie od etapu prac. Pytamy, co mówi umowa, jeśli prace są opóźnione.',
  'Den andre terminen på 15 % pluss {T} forfaller 5. mai 2027, uansett hvor langt arbeidene er kommet. Vi spør hva kontrakten sier hvis arbeidene ligger etter.',
  'Den andra delbetalningen på 15 % plus {T} förfaller den 5 maj 2027, oavsett hur långt arbetena har kommit. Vi frågar vad avtalet säger om arbetena ligger efter.')
a('.investment.cards[3][0]',
  'Cuatro de 75 viviendas figuran en la lista', 'Quatre logements sur 75 figurent sur la liste',
  'Vier von 75 Wohnungen sind gelistet', 'В списке четыре квартиры из 75',
  'أربعة مساكن من أصل 75 مدرجة في القائمة', 'Vier van de 75 woningen staan op de lijst',
  'Na liście są cztery z 75 lokali', 'Fire av 75 boliger står i listen', 'Fyra av 75 bostäder finns i listan')
a('.investment.cards[3][1]',
  'La lista de precios no menciona las otras 71 viviendas. Sus precios pueden ser distintos, y el promotor puede revisar los precios de la lista antes de una reserva.',
  'La liste de prix ne mentionne pas les 71 autres logements. Leurs prix peuvent différer, et le promoteur peut réviser les prix de la liste avant une réservation.',
  'Die Preisliste erwähnt die übrigen 71 Wohnungen nicht. Deren Preise können abweichen, und der Bauträger kann die gelisteten Preise vor einer Reservierung anpassen.',
  'В прайс-листе остальные 71 квартира не упомянуты. Их цены могут отличаться, а застройщик может пересмотреть цены из списка до бронирования.',
  'لا تذكر قائمة الأسعار المساكن الـ71 الأخرى. وقد تختلف أسعارها، ويمكن للمطوّر مراجعة الأسعار المدرجة قبل الحجز.',
  'De prijslijst vermeldt de andere 71 woningen niet. Hun prijzen kunnen afwijken, en de ontwikkelaar kan de vermelde prijzen vóór een reservering herzien.',
  'Cennik nie wspomina o pozostałych 71 lokalach. Ich ceny mogą się różnić, a deweloper może zmienić ceny z wykazu przed rezerwacją.',
  'Prislisten nevner ikke de øvrige 71 boligene. Prisene på disse kan avvike, og utbyggeren kan revidere de oppførte prisene før en reservasjon.',
  'Prislistan nämner inte de övriga 71 bostäderna. Priserna på dem kan avvika, och exploatören kan revidera de listade priserna före en reservation.')
a('.trustDossier.headlineHtml',
  'Lo que <em>comprobamos antes de que se comprometa</em>', 'Ce que nous <em>vérifions avant que vous vous engagiez</em>',
  'Was wir <em>prüfen, bevor Sie sich festlegen</em>', 'Что мы <em>проверяем, прежде чем вы примете решение</em>',
  'ما <em>نتحقق منه قبل أن تلتزم</em>', 'Wat wij <em>controleren voordat u zich vastlegt</em>',
  'Co <em>sprawdzamy, zanim się Państwo zobowiążą</em>', 'Hva vi <em>sjekker før du forplikter deg</em>',
  'Vad vi <em>kontrollerar innan ni förbinder er</em>')
a('.trustDossier.copy',
  'Confirmamos cada punto con el promotor antes de cualquier reserva y ponemos las respuestas por escrito.',
  'Nous confirmons chaque point auprès du promoteur avant toute réservation et mettons les réponses par écrit.',
  'Wir klären jeden Punkt mit dem Bauträger vor jeder Reservierung und halten die Antworten schriftlich fest.',
  'Мы уточняем каждый пункт у застройщика до любого бронирования и фиксируем ответы письменно.',
  'نؤكد كل نقطة مع المطوّر قبل أي حجز، ونوثّق الإجابات كتابةً.',
  'We bevestigen elk punt bij de ontwikkelaar vóór elke reservering en leggen de antwoorden schriftelijk vast.',
  'Każdy punkt potwierdzamy z deweloperem przed jakąkolwiek rezerwacją, a odpowiedzi spisujemy na piśmie.',
  'Vi bekrefter hvert punkt med utbyggeren før enhver reservasjon og får svarene skriftlig.',
  'Vi bekräftar varje punkt med exploatören före varje reservation och får svaren skriftligt.')
a('.trustDossier.cards[0][0]',
  'La licencia y las obras', 'Le permis et les travaux', 'Die Genehmigung und die Bauarbeiten',
  'Разрешение и строительство', 'الرخصة والأعمال', 'De vergunning en de werken',
  'Pozwolenie i prace budowlane', 'Tillatelsen og byggearbeidene', 'Bygglovet och arbetena')
a('.trustDossier.cards[0][1]',
  'Ninguno de los documentos que tenemos recoge una licencia de obra, un inicio de obras ni una fase de construcción. El catálogo dice que sus imágenes se basan en un proyecto inicial, así que pedimos la licencia y el programa de obra.',
  'Aucun des documents en notre possession ne mentionne de permis de construire, de début des travaux ni d’état d’avancement. Le catalogue précise que ses images sont fondées sur un projet initial ; nous demandons donc le permis et le calendrier des travaux.',
  'In keinem der uns vorliegenden Dokumente stehen eine Baugenehmigung, ein Baubeginn oder ein Bauabschnitt. Der Katalog sagt, dass seine Bilder auf einem ersten Entwurf beruhen, daher verlangen wir die Genehmigung und den Bauzeitenplan.',
  'Ни в одном из имеющихся у нас документов нет разрешения на строительство, начала работ или стадии строительства. В каталоге сказано, что его изображения основаны на первоначальном проекте, поэтому мы запрашиваем разрешение и график работ.',
  'لا تذكر أي من الوثائق التي لدينا رخصة بناء أو بدء أعمال أو مرحلة إنشاء. ويذكر الكتالوج أن صوره مبنية على مشروع أولي، لذلك نطلب الرخصة وبرنامج الأعمال.',
  'In geen van de documenten die wij hebben staat een bouwvergunning, een start van de werken of een bouwfase. De catalogus zegt dat de beelden op een eerste ontwerp zijn gebaseerd, dus we vragen de vergunning en het werkprogramma.',
  'Żaden z posiadanych przez nas dokumentów nie podaje pozwolenia na budowę, rozpoczęcia prac ani etapu budowy. Katalog zastrzega, że jego obrazy opierają się na początkowym projekcie, więc prosimy o pozwolenie i harmonogram prac.',
  'Ingen av dokumentene vi har oppgir en byggetillatelse, en byggestart eller et byggetrinn. Katalogen sier at bildene bygger på et første prosjekt, så vi ber om tillatelsen og fremdriftsplanen.',
  'Inget av dokumenten vi har anger ett bygglov, en byggstart eller ett byggskede. Katalogen säger att dess bilder bygger på ett första projekt, så vi ber om bygglovet och tidsplanen för arbetena.')
a('.trustDossier.cards[1][1]',
  'Los documentos no dicen si las cantidades entregadas a cuenta están garantizadas. Pedimos ver el propio aval bancario antes de cualquier pago.',
  'Les documents ne disent pas si les sommes versées en acompte sont garanties. Nous demandons à voir la garantie bancaire elle-même avant tout paiement.',
  'Die Unterlagen sagen nicht, ob Anzahlungen abgesichert sind. Wir verlangen, die Bankbürgschaft selbst zu sehen, bevor etwas gezahlt wird.',
  'В документах не сказано, гарантированы ли суммы, внесённые в счёт оплаты. Мы просим показать саму банковскую гарантию до любого платежа.',
  'لا تذكر الوثائق ما إذا كانت المبالغ المدفوعة على الحساب مضمونة. ونطلب الاطلاع على الكفالة المصرفية نفسها قبل أي دفعة.',
  'De documenten zeggen niet of bedragen die vooruit worden betaald gewaarborgd zijn. We vragen de bankgarantie zelf te zien vóór elke betaling.',
  'Dokumenty nie mówią, czy kwoty wpłacane na poczet ceny są zabezpieczone. Prosimy o okazanie samej gwarancji bankowej przed jakąkolwiek płatnością.',
  'Dokumentene sier ikke om beløp som betales på forskudd er garantert. Vi ber om å få se selve bankgarantien før noen betaling.',
  'Dokumenten anger inte om belopp som betalas i förskott är garanterade. Vi ber att få se själva bankgarantin före varje betalning.')
a('.trustDossier.cards[2][1]',
  'Los precios y las superficies están transcritos de la lista de precios, que no lleva fecha impresa. Sus superficies interiores y de terraza coinciden exactamente con los planos, y sus superficies construidas son las superficies construidas internas de los planos.',
  'Les prix et les surfaces sont transcrits de la liste de prix, qui ne porte aucune date imprimée. Ses surfaces intérieures et de terrasse correspondent exactement aux plans, et ses surfaces construites sont les surfaces construites internes des plans.',
  'Preise und Flächen sind aus der Preisliste übernommen, die kein aufgedrucktes Datum trägt. Ihre Innen- und Terrassenflächen stimmen genau mit den Plänen überein, und ihre bebauten Flächen sind die inneren bebauten Flächen der Pläne.',
  'Цены и площади перенесены из прайс-листа, на котором нет напечатанной даты. Его площади внутри и террас в точности совпадают с планами, а застроенные площади — это внутренние застроенные площади с планов.',
  'الأسعار والمساحات منقولة عن قائمة الأسعار التي لا تحمل تاريخاً مطبوعاً. وتطابق مساحاتها الداخلية ومساحات التراسات المخططات تماماً، ومساحاتها المبنية هي المساحات المبنية الداخلية الواردة في المخططات.',
  'Prijzen en oppervlakten zijn overgenomen uit de prijslijst, die geen gedrukte datum draagt. De binnen- en terrasoppervlakten komen exact overeen met de plattegronden, en de bebouwde oppervlakten zijn de interne bebouwde oppervlakten van de plattegronden.',
  'Ceny i powierzchnie są przepisane z cennika, który nie ma wydrukowanej daty. Jego powierzchnie wnętrz i tarasów dokładnie zgadzają się z rzutami, a powierzchnie zabudowy to wewnętrzne powierzchnie zabudowy z rzutów.',
  'Priser og arealer er hentet fra prislisten, som ikke har trykt dato. Dens innvendige arealer og terrasseareal stemmer nøyaktig med tegningene, og de bebygde arealene er de interne bebygde arealene på tegningene.',
  'Priser och ytor är hämtade från prislistan, som saknar tryckt datum. Dess inomhus- och terrassytor stämmer exakt med ritningarna, och de byggda ytorna är de interna byggda ytorna på ritningarna.')
a('.trustDossier.cards[3][1]',
  'Cada vivienda de la lista tiene una plaza de garaje y un trastero numerados en la misma línea que su precio. Los documentos no dicen con palabras que ambos estén incluidos, así que lo confirmamos.',
  'Chaque logement de la liste a une place de garage et une cave numérotées sur la même ligne que son prix. Les documents ne disent pas en toutes lettres que les deux sont inclus ; nous le confirmons donc.',
  'Jede gelistete Wohnung hat einen nummerierten Garagenstellplatz und Abstellraum in derselben Zeile wie ihren Preis. Die Unterlagen sagen nicht in Worten, dass beides enthalten ist, daher lassen wir es uns bestätigen.',
  'У каждой квартиры из списка пронумерованные машиноместо и кладовая указаны в той же строке, что и цена. В документах прямо не сказано, что оба входят в цену, поэтому мы это уточняем.',
  'لكل مسكن في القائمة موقف سيارات في المرآب ومخزن مرقّمان في السطر نفسه الذي يرد فيه سعره. ولا تذكر الوثائق صراحةً أن كليهما مشمول، لذلك نؤكد ذلك.',
  'Elke vermelde woning heeft een genummerde garageplaats en berging op dezelfde regel als haar prijs. De documenten zeggen niet met zoveel woorden dat beide inbegrepen zijn, dus we laten het bevestigen.',
  'Każdy lokal z wykazu ma numerowane miejsce garażowe i komórkę lokatorską w tym samym wierszu co cena. Dokumenty nie mówią wprost, że obie rzeczy są wliczone, więc prosimy o potwierdzenie.',
  'Hver oppførte bolig har en nummerert garasjeplass og bod på samme linje som prisen. Dokumentene sier ikke med ord at begge er inkludert, så vi får det bekreftet.',
  'Varje listad bostad har en numrerad garageplats och ett förråd på samma rad som priset. Dokumenten säger inte med ord att båda ingår, så vi låter bekräfta det.')
a('.trustDossier.cards[4][1]',
  'Las imágenes están generadas por ordenador, los planos son planos de proyecto de abril de 2024 con superficies aproximadas, y el mobiliario que aparece no está incluido.',
  'Les images sont générées par ordinateur, les plans sont des plans de projet d’avril 2024 aux surfaces approximatives, et le mobilier représenté n’est pas inclus.',
  'Die Bilder sind computergeneriert, die Pläne sind Entwurfspläne vom April 2024 mit ungefähren Flächen, und die abgebildeten Möbel sind nicht enthalten.',
  'Изображения созданы на компьютере, планировки — проектные планы апреля 2024 года с приблизительными площадями, а показанная мебель в стоимость не входит.',
  'الصور مولَّدة بالحاسوب، والمخططات مخططات مرحلة المشروع في أبريل 2024 بمساحات تقريبية، والأثاث الظاهر فيها غير مشمول.',
  'De beelden zijn computergegenereerd, de plattegronden zijn projectplannen van april 2024 met benaderde oppervlakten, en het getoonde meubilair is niet inbegrepen.',
  'Obrazy są wygenerowane komputerowo, rzuty to plany projektowe z kwietnia 2024 roku z przybliżonymi powierzchniami, a pokazane meble nie są wliczone.',
  'Bildene er datagenererte, tegningene er prosjektplaner fra april 2024 med omtrentlige arealer, og møblene som vises er ikke inkludert.',
  'Bilderna är datorgenererade, ritningarna är projektplaner från april 2024 med ungefärliga ytor, och möblerna som visas ingår inte.')

# ---- availability, payment terms, timeline --------------------------------------------------------

a('.availability.copy',
  'Los precios proceden de la lista de precios del promotor, que no lleva fecha impresa; su archivo se generó el 29 de octubre de 2026. La lista nombra 4 de las 75 viviendas: 3 están disponibles y 1 está reservada. Confirmamos precios y disponibilidad antes de cualquier reserva. Los precios no incluyen el {T}.',
  'Les prix proviennent de la liste de prix du promoteur, qui ne porte aucune date imprimée ; son fichier a été produit le 29 octobre 2026. La liste nomme 4 des 75 logements : 3 sont disponibles et 1 est réservé. Nous confirmons les prix et la disponibilité avant toute réservation. Les prix s’entendent hors {T}.',
  'Die Preise stammen aus der Preisliste des Bauträgers, die kein aufgedrucktes Datum trägt; ihre Datei wurde am 29. Oktober 2026 erstellt. Die Liste nennt 4 der 75 Wohnungen: 3 sind verfügbar und 1 ist reserviert. Wir bestätigen Preise und Verfügbarkeit vor jeder Reservierung. Die Preise verstehen sich vor {T}.',
  'Цены взяты из прайс-листа застройщика, на котором нет напечатанной даты; его файл создан 29 октября 2026 года. В списке названы 4 из 75 квартир: 3 доступны и 1 забронирована. Мы подтверждаем цены и наличие до любого бронирования. Цены указаны без {T}.',
  'الأسعار مأخوذة من قائمة أسعار المطوّر التي لا تحمل تاريخاً مطبوعاً؛ وقد أُنشئ ملفها في 29 أكتوبر 2026. تذكر القائمة 4 مساكن من أصل 75: 3 متاحة وواحد محجوز. نؤكد الأسعار والتوافر قبل أي حجز. الأسعار قبل {T}.',
  'De prijzen komen uit de prijslijst van de ontwikkelaar, die geen gedrukte datum draagt; het bestand is gemaakt op 29 oktober 2026. De lijst noemt 4 van de 75 woningen: 3 zijn beschikbaar en 1 is gereserveerd. We bevestigen prijzen en beschikbaarheid vóór elke reservering. De prijzen zijn exclusief {T}.',
  'Ceny pochodzą z cennika dewelopera, który nie ma wydrukowanej daty; jego plik powstał 29 października 2026 roku. Cennik wymienia 4 z 75 lokali: 3 są dostępne, a 1 jest zarezerwowany. Ceny i dostępność potwierdzamy przed jakąkolwiek rezerwacją. Ceny nie zawierają {T}.',
  'Prisene er hentet fra utbyggerens prisliste, som ikke har trykt dato; filen ble laget 29. oktober 2026. Listen nevner 4 av de 75 boligene: 3 er ledige og 1 er reservert. Vi bekrefter priser og tilgjengelighet før enhver reservasjon. Prisene er før {T}.',
  'Priserna är hämtade från exploatörens prislista, som saknar tryckt datum; filen skapades den 29 oktober 2026. Listan nämner 4 av de 75 bostäderna: 3 är lediga och 1 är reserverad. Vi bekräftar priser och tillgänglighet före varje reservation. Priserna är före {T}.')
a('.availability.sourceNote',
  'Todas las cifras están transcritas de la lista de precios del promotor. No lleva fecha impresa; aquí se usa la fecha de su archivo, el 29 de octubre de 2026. Nombra cuatro de las 75 viviendas, marca una de ellas (bloque 1, portal 2, segunda planta A) como reservada, pone precio a las otras tres e indica que el {T} no está incluido. En Andalucía se aplica el {T} del 10 % y el impuesto de actos jurídicos documentados del 1,20 %, así que el apartamento de {E365000} cuesta unos {E406000} y el ático de {E530000} unos {E589000} antes de los gastos de notaría y registro. Cada vivienda de la lista tiene una plaza de garaje y un trastero numerados en la misma línea que su precio; los documentos no dicen con palabras que ambos estén incluidos. La superficie construida de la lista es la superficie construida interna de los planos; los planos dan además una superficie bruta con zonas comunes y un conjunto de superficies según el decreto andaluz 218/2005, que no publicamos. La orientación mal escrita de la vivienda 2-4-1-A en la lista, «Soth-West», se interpreta como suroeste.',
  'Tous les chiffres sont transcrits de la liste de prix du promoteur. Elle ne porte aucune date imprimée ; la date de son fichier, le 29 octobre 2026, est utilisée ici. Elle nomme quatre des 75 logements, indique l’un d’eux (bloc 1, entrée 2, deuxième étage A) comme réservé, fixe le prix des trois autres et précise que la {T} n’est pas incluse. La {T} à 10 % et le droit de timbre à 1,20 % s’appliquent en Andalousie, de sorte que l’appartement à {E365000} revient à environ {E406000} et le penthouse à {E530000} à environ {E589000}, avant les frais de notaire et de registre foncier. Chaque logement de la liste a une place de garage et une cave numérotées sur la même ligne que son prix ; les documents ne disent pas en toutes lettres que les deux sont inclus. La surface construite de la liste est la surface construite interne des plans ; les plans donnent aussi une surface brute avec parties communes et un jeu de surfaces selon le décret andalou 218/2005, que nous ne publions pas. L’orientation mal orthographiée du logement 2-4-1-A dans la liste, « Soth-West », est lue comme sud-ouest.',
  'Alle Zahlen sind aus der Preisliste des Bauträgers übernommen. Sie trägt kein aufgedrucktes Datum; verwendet wird hier das Datum ihrer Datei, der 29. Oktober 2026. Sie nennt vier der 75 Wohnungen, kennzeichnet eine davon (Block 1, Eingang 2, zweite Etage A) als reserviert, bepreist die anderen drei und gibt an, dass die {T} nicht enthalten ist. In Andalusien fallen {T} von 10 % und Stempelsteuer von 1,20 % an, sodass das Apartment für {E365000} rund {E406000} und das Penthouse für {E530000} rund {E589000} kostet, vor Notar- und Grundbuchgebühren. Jede gelistete Wohnung hat einen nummerierten Garagenstellplatz und Abstellraum in derselben Zeile wie ihren Preis; die Unterlagen sagen nicht in Worten, dass beides enthalten ist. Die bebaute Fläche der Liste ist die innere bebaute Fläche der Pläne; die Pläne geben außerdem eine Bruttofläche mit Gemeinschaftsflächen und eine Reihe von Flächen nach dem andalusischen Dekret 218/2005 an, die wir nicht veröffentlichen. Die falsch geschriebene Ausrichtung der Wohnung 2-4-1-A in der Liste, „Soth-West“, wird als Südwest gelesen.',
  'Все цифры перенесены из прайс-листа застройщика. На нём нет напечатанной даты; здесь использована дата его файла — 29 октября 2026 года. В нём названы четыре из 75 квартир, одна из них (корпус 1, подъезд 2, второй этаж A) отмечена как забронированная, у остальных трёх указана цена, а также сказано, что {T} не включён. В Андалусии действуют {T} 10 % и гербовый сбор 1,20 %, поэтому апартаменты за {E365000} обходятся примерно в {E406000}, а пентхаус за {E530000} — примерно в {E589000}, до расходов на нотариуса и регистрацию. У каждой квартиры из списка пронумерованные машиноместо и кладовая указаны в той же строке, что и цена; в документах прямо не сказано, что оба входят в цену. Застроенная площадь в списке — это внутренняя застроенная площадь с планов; на планах есть также общая площадь с местами общего пользования и набор площадей по андалусскому декрету 218/2005, которые мы не публикуем. Неверно написанная в списке ориентация квартиры 2-4-1-A, «Soth-West», прочитана как юго-запад.',
  'جميع الأرقام منقولة عن قائمة أسعار المطوّر. وهي لا تحمل تاريخاً مطبوعاً؛ ويُستخدم هنا تاريخ ملفها، 29 أكتوبر 2026. تذكر أربعة مساكن من أصل 75، وتشير إلى أحدها (المبنى 1، المدخل 2، الطابق الثاني A) على أنه محجوز، وتحدد أسعار الثلاثة الأخرى، وتنص على أن {T} غير مشمولة. وفي الأندلس تُطبَّق {T} بنسبة 10% وضريبة الدمغة بنسبة 1.20%، فتبلغ كلفة الشقة المسعّرة {E365000} نحو {E406000}، وكلفة البنتهاوس المسعّر {E530000} نحو {E589000}، قبل رسوم الكاتب العدل والسجل العقاري. لكل مسكن في القائمة موقف سيارات في المرآب ومخزن مرقّمان في السطر نفسه الذي يرد فيه سعره؛ ولا تذكر الوثائق صراحةً أن كليهما مشمول. والمساحة المبنية في القائمة هي المساحة المبنية الداخلية الواردة في المخططات؛ وتعطي المخططات أيضاً مساحة إجمالية تشمل المناطق المشتركة ومجموعة مساحات بموجب المرسوم الأندلسي 218/2005، ولا ننشرها. أما اتجاه المسكن 2-4-1-A المكتوب خطأً في القائمة، «Soth-West»، فيُقرأ جنوباً غربياً.',
  'Alle cijfers zijn overgenomen uit de prijslijst van de ontwikkelaar. Die draagt geen gedrukte datum; hier wordt de datum van het bestand gebruikt, 29 oktober 2026. Ze noemt vier van de 75 woningen, markeert er een (blok 1, portiek 2, tweede verdieping A) als gereserveerd, prijst de andere drie en geeft aan dat de {T} niet is inbegrepen. In Andalusië gelden {T} van 10% en zegelrecht van 1,20%, zodat het appartement van {E365000} ongeveer {E406000} kost en het penthouse van {E530000} ongeveer {E589000}, vóór de kosten van notaris en kadaster. Elke vermelde woning heeft een genummerde garageplaats en berging op dezelfde regel als haar prijs; de documenten zeggen niet met zoveel woorden dat beide inbegrepen zijn. De bebouwde oppervlakte op de lijst is de interne bebouwde oppervlakte van de plattegronden; de plattegronden geven ook een bruto-oppervlakte met gemeenschappelijke ruimten en een reeks oppervlakten volgens het Andalusische decreet 218/2005, die we niet publiceren. De verkeerd gespelde oriëntatie van woning 2-4-1-A op de lijst, “Soth-West”, wordt gelezen als zuidwest.',
  'Wszystkie liczby są przepisane z cennika dewelopera. Nie ma on wydrukowanej daty; użyto tu daty jego pliku, 29 października 2026 roku. Wymienia cztery z 75 lokali, jeden z nich (blok 1, klatka 2, drugie piętro A) oznacza jako zarezerwowany, podaje ceny pozostałych trzech i zastrzega, że {T} nie jest wliczony. W Andaluzji obowiązuje {T} w wysokości 10% i podatek od czynności dokumentowanych w wysokości 1,20%, więc apartament za {E365000} kosztuje około {E406000}, a penthouse za {E530000} około {E589000}, przed opłatami notarialnymi i wpisem do księgi wieczystej. Każdy lokal z wykazu ma numerowane miejsce garażowe i komórkę lokatorską w tym samym wierszu co cena; dokumenty nie mówią wprost, że obie rzeczy są wliczone. Powierzchnia zabudowy w cenniku to wewnętrzna powierzchnia zabudowy z rzutów; rzuty podają też powierzchnię brutto z częściami wspólnymi oraz zestaw powierzchni według andaluzyjskiego dekretu 218/2005, których nie publikujemy. Błędnie zapisana w cenniku orientacja lokalu 2-4-1-A, „Soth-West”, jest odczytywana jako południowy zachód.',
  'Alle tall er hentet fra utbyggerens prisliste. Den har ingen trykt dato; her brukes datoen på filen, 29. oktober 2026. Den nevner fire av de 75 boligene, markerer én av dem (blokk 1, oppgang 2, andre etasje A) som reservert, setter pris på de tre andre og oppgir at {T} ikke er inkludert. I Andalucía gjelder {T} på 10 % og dokumentavgift på 1,20 %, slik at leiligheten til {E365000} koster omtrent {E406000} og toppleiligheten til {E530000} omtrent {E589000}, før notar- og tinglysingsgebyrer. Hver oppførte bolig har en nummerert garasjeplass og bod på samme linje som prisen; dokumentene sier ikke med ord at begge er inkludert. Det bebygde arealet i listen er det interne bebygde arealet på tegningene; tegningene oppgir også et bruttoareal med fellesarealer og et sett arealer etter det andalusiske dekretet 218/2005, som vi ikke publiserer. Den feilstavede retningen for bolig 2-4-1-A i listen, «Soth-West», leses som sørvest.',
  'Alla siffror är hämtade från exploatörens prislista. Den saknar tryckt datum; här används datumet på filen, den 29 oktober 2026. Den nämner fyra av de 75 bostäderna, markerar en av dem (hus 1, trapphus 2, andra våningen A) som reserverad, prissätter de andra tre och anger att {T} inte ingår. I Andalusien gäller {T} på 10 % och stämpelskatt på 1,20 %, så lägenheten för {E365000} kostar cirka {E406000} och takvåningen för {E530000} cirka {E589000}, före notarie- och fastighetsregisteravgifter. Varje listad bostad har en numrerad garageplats och ett förråd på samma rad som priset; dokumenten säger inte med ord att båda ingår. Den byggda ytan i listan är den interna byggda ytan på ritningarna; ritningarna anger också en bruttoyta med gemensamma ytor och en uppsättning ytor enligt det andalusiska dekretet 218/2005, som vi inte publicerar. Den felstavade orienteringen för bostad 2-4-1-A i listan, «Soth-West», läses som sydväst.')
a('.constructionTimeline.headlineHtml',
  'De la reserva <em>a las llaves</em>', 'De la réservation <em>aux clés</em>', 'Von der Reservierung <em>bis zu den Schlüsseln</em>',
  'От бронирования <em>до ключей</em>', 'من الحجز <em>إلى المفاتيح</em>', 'Van reservering <em>tot sleutels</em>',
  'Od rezerwacji <em>do kluczy</em>', 'Fra reservasjon <em>til nøkler</em>', 'Från reservation <em>till nycklar</em>')
a('.constructionTimeline.points[0].year',
  'Mayo 2027', 'Mai 2027', 'Mai 2027', 'Май 2027', 'مايو 2027', 'Mei 2027', 'Maj 2027', 'Mai 2027', 'Maj 2027')
a('.constructionTimeline.points[0].label',
  'Cuota aplazada', 'Échéance différée', 'Aufgeschobene Rate', 'Отсроченный платёж', 'دفعة مؤجلة',
  'Uitgestelde termijn', 'Rata odroczona', 'Utsatt termin', 'Uppskjuten delbetalning')
a('.constructionTimeline.points[1].label',
  'Escritura y llaves', 'Acte et clés', 'Beurkundung und Schlüssel', 'Сделка и ключи', 'سند الملكية والمفاتيح',
  'Akte en sleutels', 'Akt notarialny i klucze', 'Skjøte og nøkler', 'Lagfart och nycklar')
a('.constructionTimeline.note',
  'Las condiciones de pago sitúan la escritura y la entrega de llaves en el cuarto trimestre de 2027, cuando vence el último 70 %, y una cuota del 15 % el 5 de mayo de 2027. Ningún documento que tenemos recoge una licencia de obra, un inicio de obras ni una fase de construcción, el catálogo dice que sus imágenes se basan en un proyecto inicial y los planos son de abril de 2024. Nueva Living pide por escrito la licencia, el programa de obra y la fecha de entrega, y hace constar la fecha en el contrato.',
  'Les conditions de paiement placent l’acte et la remise des clés au quatrième trimestre 2027, date à laquelle les derniers 70 % sont exigibles, et une échéance de 15 % le 5 mai 2027. Aucun document en notre possession ne mentionne de permis de construire, de début des travaux ni d’état d’avancement, le catalogue précise que ses images sont fondées sur un projet initial, et les plans datent d’avril 2024. Nueva Living demande par écrit le permis, le calendrier des travaux et la date de livraison, et fait inscrire la date au contrat.',
  'Die Zahlungsbedingungen setzen Beurkundung und Schlüsselübergabe auf das vierte Quartal 2027, wenn die letzten 70 % fällig werden, und eine Rate von 15 % auf den 5. Mai 2027. In keinem der uns vorliegenden Dokumente stehen eine Baugenehmigung, ein Baubeginn oder ein Bauabschnitt, der Katalog sagt, dass seine Bilder auf einem ersten Entwurf beruhen, und die Pläne stammen vom April 2024. Nueva Living verlangt Genehmigung, Bauzeitenplan und Übergabetermin schriftlich und lässt den Termin in den Vertrag aufnehmen.',
  'По условиям оплаты нотариальный акт и передача ключей приходятся на четвёртый квартал 2027 года, когда подлежат оплате последние 70 %, а платёж 15 % — на 5 мая 2027 года. Ни в одном из имеющихся у нас документов нет разрешения на строительство, начала работ или стадии строительства, в каталоге сказано, что его изображения основаны на первоначальном проекте, а планы датированы апрелем 2024 года. Nueva Living письменно запрашивает разрешение, график работ и срок сдачи и вносит срок в договор.',
  'تحدد شروط الدفع موعد سند الملكية وتسليم المفاتيح في الربع الرابع من عام 2027، حين تُستحق الدفعة الأخيرة البالغة 70%، ودفعة بنسبة 15% في 5 مايو 2027. ولا تذكر أي من الوثائق التي لدينا رخصة بناء أو بدء أعمال أو مرحلة إنشاء، ويذكر الكتالوج أن صوره مبنية على مشروع أولي، وتعود المخططات إلى أبريل 2024. تطلب Nueva Living كتابةً الرخصة وبرنامج الأعمال وموعد التسليم، وتُدرج الموعد في العقد.',
  'De betalingsvoorwaarden plaatsen de akte en de sleuteloverdracht in het vierde kwartaal van 2027, wanneer de laatste 70% verschuldigd is, en een termijn van 15% op 5 mei 2027. In geen van de documenten die wij hebben staat een bouwvergunning, een start van de werken of een bouwfase, de catalogus zegt dat de beelden op een eerste ontwerp zijn gebaseerd, en de plattegronden zijn van april 2024. Nueva Living vraagt de vergunning, het werkprogramma en de opleverdatum schriftelijk en laat de datum in het contract opnemen.',
  'Warunki płatności wyznaczają akt notarialny i przekazanie kluczy na czwarty kwartał 2027 roku, gdy przypada ostatnie 70%, oraz ratę 15% na 5 maja 2027 roku. Żaden z posiadanych przez nas dokumentów nie podaje pozwolenia na budowę, rozpoczęcia prac ani etapu budowy, katalog zastrzega, że jego obrazy opierają się na początkowym projekcie, a rzuty pochodzą z kwietnia 2024 roku. Nueva Living prosi na piśmie o pozwolenie, harmonogram prac i termin oddania i wpisuje termin do umowy.',
  'Betalingsvilkårene legger skjøtet og nøkkeloverleveringen til fjerde kvartal 2027, når de siste 70 % forfaller, og en termin på 15 % den 5. mai 2027. Ingen av dokumentene vi har oppgir en byggetillatelse, en byggestart eller et byggetrinn, katalogen sier at bildene bygger på et første prosjekt, og tegningene er fra april 2024. Nueva Living ber skriftlig om tillatelsen, fremdriftsplanen og leveringsdatoen og får datoen inn i kontrakten.',
  'Betalningsvillkoren lägger lagfarten och nyckelöverlämnandet i fjärde kvartalet 2027, då de sista 70 % förfaller, och en delbetalning på 15 % den 5 maj 2027. Inget av dokumenten vi har anger ett bygglov, en byggstart eller ett byggskede, katalogen säger att dess bilder bygger på ett första projekt, och ritningarna är från april 2024. Nueva Living ber skriftligen om bygglovet, tidsplanen för arbetena och leveransdatumet och låter datumet föras in i avtalet.')
a('.constructionTimeline.paymentTerms[0][1]',
  '{E6000} + {T}', '{E6000} + {T}', '{E6000} + {T}', '{E6000} + {T}', '{E6000} + {T}',
  '{E6000} + {T}', '{E6000} + {T}', '{E6000} + {T}', '{E6000} + {T}')
a('.constructionTimeline.paymentTerms[0][2]',
  '{E6600} al firmar', '{E6600} à la signature', '{E6600} bei Unterzeichnung', '{E6600} при подписании',
  '{E6600} عند التوقيع', '{E6600} bij ondertekening', '{E6600} przy podpisaniu', '{E6600} ved signering', '{E6600} vid underskrift')
a('.constructionTimeline.paymentTerms[2][0]',
  'Cuota aplazada', 'Échéance différée', 'Aufgeschobene Rate', 'Отсроченный платёж', 'دفعة مؤجلة',
  'Uitgestelde termijn', 'Rata odroczona', 'Utsatt termin', 'Uppskjuten delbetalning')
a('.constructionTimeline.paymentTerms[2][2]',
  'El 5 de mayo de 2027', 'Le 5 mai 2027', 'Am 5. Mai 2027', '5 мая 2027 года', 'في 5 مايو 2027',
  'Op 5 mei 2027', '5 maja 2027 roku', 'Den 5. mai 2027', 'Den 5 maj 2027')
a('.constructionTimeline.paymentTerms[3][2]',
  'Escritura en el cuarto trimestre de 2027, al terminar y entregar las llaves',
  'Acte authentique au quatrième trimestre 2027, à l’achèvement et à la remise des clés',
  'Beurkundung im vierten Quartal 2027, bei Fertigstellung und Schlüsselübergabe',
  'Нотариальный акт в четвёртом квартале 2027 года, при завершении и передаче ключей',
  'سند الملكية في الربع الرابع من عام 2027، عند الإنجاز وتسليم المفاتيح',
  'Notariële akte in het vierde kwartaal van 2027, bij oplevering en sleuteloverdracht',
  'Akt notarialny w czwartym kwartale 2027 roku, przy zakończeniu i przekazaniu kluczy',
  'Skjøte i fjerde kvartal 2027, ved ferdigstillelse og nøkkeloverlevering',
  'Lagfart i fjärde kvartalet 2027, vid färdigställande och nyckelöverlämnande')
a('.constructionTimeline.paymentTermsNote',
  'Los tres porcentajes suman el precio completo, y el {T} se añade a cada uno. Los documentos no dicen si las cantidades entregadas a cuenta están garantizadas, si el aplazamiento lleva intereses ni a cuánto ascienden los gastos de la compra además del precio. Nueva Living pide cada punto por escrito antes de que usted reserve.',
  'Les trois pourcentages totalisent le prix complet, et la {T} s’ajoute à chacun. Les documents ne disent pas si les sommes versées en acompte sont garanties, si le report porte intérêt, ni à combien s’élèvent les frais d’achat en plus du prix. Nueva Living demande chaque point par écrit avant que vous ne réserviez.',
  'Die drei Prozentsätze ergeben den vollen Preis, und die {T} kommt auf jeden hinzu. Die Unterlagen sagen nicht, ob Anzahlungen abgesichert sind, ob die Stundung verzinst wird oder wie hoch die Kaufnebenkosten zusätzlich zum Preis ausfallen. Nueva Living verlangt jeden Punkt schriftlich, bevor Sie reservieren.',
  'Три доли в процентах в сумме дают полную цену, и к каждой добавляется {T}. В документах не сказано, гарантированы ли суммы, внесённые в счёт оплаты, начисляются ли проценты на отсрочку и каковы расходы на покупку сверх цены. Nueva Living запрашивает каждый пункт письменно до того, как вы забронируете.',
  'تبلغ النسب الثلاث معاً السعر كاملاً، وتُضاف {T} إلى كل منها. ولا تذكر الوثائق ما إذا كانت المبالغ المدفوعة على الحساب مضمونة، ولا ما إذا كان التأجيل يحمل فوائد، ولا مقدار نفقات الشراء فوق السعر. تطلب Nueva Living كل نقطة كتابةً قبل أن تحجز.',
  'De drie percentages vormen samen de volledige prijs, en de {T} komt over elk daarvan. De documenten zeggen niet of vooruitbetaalde bedragen gewaarborgd zijn, of het uitstel rente kost, of hoe hoog de aankoopkosten bovenop de prijs uitvallen. Nueva Living vraagt elk punt schriftelijk voordat u reserveert.',
  'Trzy wartości procentowe sumują się do pełnej ceny, a do każdej dolicza się {T}. Dokumenty nie mówią, czy kwoty wpłacane na poczet ceny są zabezpieczone, czy odroczenie wiąże się z odsetkami ani ile wynoszą koszty zakupu ponad cenę. Nueva Living prosi o każdy punkt na piśmie, zanim Państwo zarezerwują.',
  'De tre prosentene utgjør hele prisen, og {T} kommer på hver av dem. Dokumentene sier ikke om beløp som betales på forskudd er garantert, om utsettelsen medfører renter, eller hva kjøpskostnadene kommer på toppen av prisen. Nueva Living ber om hvert punkt skriftlig før du reserverer.',
  'De tre procenttalen utgör hela priset, och {T} läggs på var och en. Dokumenten anger inte om belopp som betalas i förskott är garanterade, om uppskovet medför ränta eller hur stora köpkostnaderna blir utöver priset. Nueva Living ber om varje punkt skriftligen innan ni reserverar.')

# ---- timeline, private viewing, enquiry, faq, seo ------------------------------------------------

a('.timeline.items[0][1]',
  'Cuéntenos lo que necesita', 'Dites-nous ce dont vous avez besoin', 'Sagen Sie uns, was Sie brauchen',
  'Расскажите, что вам нужно', 'أخبرنا بما تحتاجه', 'Vertel ons wat u nodig hebt',
  'Powiedzcie nam Państwo, czego potrzebują', 'Fortell oss hva du trenger', 'Berätta vad ni behöver')
a('.timeline.items[0][2]',
  'El número de dormitorios, la planta y lo que quiere que haga la terraza.',
  'Le nombre de chambres, l’étage et ce que vous attendez de la terrasse.',
  'Die Zahl der Schlafzimmer, das Geschoss und was die Terrasse leisten soll.',
  'Количество спален, этаж и то, для чего вам нужна терраса.',
  'عدد غرف النوم والطابق وما تريده من التراس.',
  'Het aantal slaapkamers, de verdieping en wat u met het terras wilt doen.',
  'Liczba sypialni, piętro i to, do czego ma służyć taras.',
  'Antall soverom, etasjen og hva du vil bruke terrassen til.',
  'Antalet sovrum, våningen och vad ni vill att terrassen ska användas till.')
a('.timeline.items[1][1]',
  'Confirmamos la lista', 'Nous confirmons la liste', 'Wir bestätigen die Liste', 'Мы подтверждаем список',
  'نؤكد القائمة', 'Wij bevestigen de lijst', 'Potwierdzamy wykaz', 'Vi bekrefter listen', 'Vi bekräftar listan')
a('.timeline.items[1][2]',
  'Disponibilidad y precios actuales del promotor, con el {T} y el impuesto de actos jurídicos documentados añadidos para que vea la cifra real.',
  'Disponibilité et prix actuels auprès du promoteur, avec la {T} et le droit de timbre ajoutés pour que vous voyiez le chiffre réel.',
  'Aktuelle Verfügbarkeit und Preise vom Bauträger, mit {T} und Stempelsteuer, damit Sie die tatsächliche Summe sehen.',
  'Актуальные наличие и цены от застройщика, с добавлением {T} и гербового сбора, чтобы вы видели реальную сумму.',
  'التوافر والأسعار الحالية من المطوّر، مع إضافة {T} وضريبة الدمغة لتري الرقم الحقيقي.',
  'Actuele beschikbaarheid en prijzen van de ontwikkelaar, met {T} en zegelrecht erbij zodat u het werkelijke bedrag ziet.',
  'Aktualna dostępność i ceny od dewelopera, z doliczonym {T} i podatkiem od czynności dokumentowanych, aby widzieli Państwo rzeczywistą kwotę.',
  'Gjeldende tilgjengelighet og priser fra utbyggeren, med {T} og dokumentavgift lagt til slik at du ser det reelle beløpet.',
  'Aktuell tillgänglighet och aktuella priser från exploatören, med {T} och stämpelskatt tillagda så att ni ser den verkliga summan.')
a('.timeline.items[2][1]',
  'Vea el solar y la zona', 'Découvrez le terrain et la zone', 'Sehen Sie Grundstück und Umgebung',
  'Посмотрите участок и район', 'شاهد الموقع والمنطقة', 'Bekijk het terrein en de omgeving',
  'Zobaczcie Państwo teren i okolicę', 'Se tomten og området', 'Se tomten och området')
a('.timeline.items[2][2]',
  'Recorremos con usted la parcela y la zona, y trasladamos al promotor las preguntas sobre la licencia, el aval y la fecha.',
  'Nous parcourons avec vous la parcelle et la zone, et posons au promoteur les questions sur le permis, la garantie et la date.',
  'Wir gehen mit Ihnen über das Grundstück und durch die Umgebung und stellen dem Bauträger die Fragen zu Genehmigung, Bürgschaft und Termin.',
  'Мы проходим с вами по участку и району и задаём застройщику вопросы о разрешении, гарантии и сроке.',
  'نتجوّل معك في القطعة والمنطقة، ونوجّه إلى المطوّر الأسئلة المتعلقة بالرخصة والكفالة والموعد.',
  'We lopen met u over het perceel en door de omgeving en leggen de vragen over de vergunning, de garantie en de datum aan de ontwikkelaar voor.',
  'Przechodzimy z Państwem po działce i okolicy oraz kierujemy do dewelopera pytania o pozwolenie, gwarancję i termin.',
  'Vi går over tomten og gjennom området sammen med deg, og stiller utbyggeren spørsmålene om tillatelsen, garantien og datoen.',
  'Vi går över tomten och genom området tillsammans med er och ställer frågorna om bygglovet, garantin och datumet till exploatören.')
a('.timeline.items[3][2]',
  'Confirmamos por escrito el importe de la reserva y las fechas de pago antes del contrato privado.',
  'Nous confirmons par écrit le montant de la réservation et les dates de paiement avant le contrat privé.',
  'Wir bestätigen den Reservierungsbetrag und die Zahlungstermine schriftlich vor dem privaten Vertrag.',
  'Мы письменно подтверждаем сумму бронирования и даты платежей до частного договора.',
  'نؤكد كتابةً مبلغ الحجز ومواعيد الدفع قبل العقد الخاص.',
  'We bevestigen het reserveringsbedrag en de betaaldata schriftelijk vóór het onderhandse contract.',
  'Kwotę rezerwacji i terminy płatności potwierdzamy na piśmie przed umową przedwstępną.',
  'Vi bekrefter reservasjonsbeløpet og betalingsdatoene skriftlig før den private kontrakten.',
  'Vi bekräftar reservationsbeloppet och betalningsdatumen skriftligen före det privata avtalet.')
a('.privateViewing.insights[0][1]',
  'Recorra la parcela y la zona que la rodea, y compruebe a qué distancia están el parque, los campos de golf y el mar.',
  'Parcourez la parcelle et la zone qui l’entoure, et voyez à quelle distance se trouvent le parc, les golfs et la mer.',
  'Gehen Sie über das Grundstück und durch die Umgebung und sehen Sie, wie weit Park, Golfplätze und Meer entfernt sind.',
  'Пройдитесь по участку и окрестностям и посмотрите, как далеко парк, поля для гольфа и море.',
  'تجوّل في القطعة والمنطقة المحيطة بها، وتحقق من بُعد الحديقة وملاعب الغولف والبحر.',
  'Loop over het perceel en door de omgeving en zie hoe ver het park, de golfbanen en de zee liggen.',
  'Przejdźcie Państwo po działce i okolicy i zobaczcie, jak daleko są park, pola golfowe i morze.',
  'Gå over tomten og området rundt, og se hvor langt det er til parken, golfbanene og havet.',
  'Gå över tomten och området runt omkring och se hur långt det är till parken, golfbanorna och havet.')
a('.privateViewing.insights[1][0]',
  'En la carretera', 'Sur la route', 'Auf der Straße', 'В дороге', 'على الطريق', 'Onderweg', 'W drodze', 'På veien', 'På vägen')
a('.privateViewing.insights[1][1]',
  'Recorremos con usted las carreteras hasta la autovía y la costa, y las cronometramos.',
  'Nous parcourons avec vous les routes jusqu’à l’autoroute et à la côte, chronomètre en main.',
  'Wir fahren mit Ihnen die Straßen zur Autobahn und zur Küste und stoppen die Zeit.',
  'Мы проезжаем с вами по дорогам до автомагистрали и побережья и засекаем время.',
  'نقود معك على الطرق المؤدية إلى الطريق السريع والساحل ونحتسب الوقت.',
  'We rijden met u over de wegen naar de snelweg en de kust en nemen de tijd op.',
  'Przejeżdżamy z Państwem drogami do autostrady i na wybrzeże i mierzymy czas.',
  'Vi kjører veiene til motorveien og kysten sammen med deg og tar tiden.',
  'Vi kör vägarna till motorvägen och kusten tillsammans med er och tar tid.')
a('.privateViewing.insights[2][1]',
  'La licencia, el aval y la fecha de entrega, antes de firmar nada.',
  'Le permis, la garantie et la date de livraison, avant de signer quoi que ce soit.',
  'Genehmigung, Bürgschaft und Übergabetermin, bevor etwas unterschrieben wird.',
  'Разрешение, гарантия и срок сдачи — до подписания чего-либо.',
  'الرخصة والكفالة وموعد التسليم، قبل توقيع أي شيء.',
  'De vergunning, de garantie en de opleverdatum, voordat er iets wordt ondertekend.',
  'Pozwolenie, gwarancja i termin oddania, zanim cokolwiek zostanie podpisane.',
  'Tillatelsen, garantien og leveringsdatoen, før noe signeres.',
  'Bygglovet, garantin och leveransdatumet, innan något skrivs under.')
a('.enquiry.headlineHtml',
  'Pregunte por <em>Mijas Horizon Residences</em>', 'Renseignez-vous sur <em>Mijas Horizon Residences</em>',
  'Fragen Sie nach <em>Mijas Horizon Residences</em>', 'Узнайте о <em>Mijas Horizon Residences</em>',
  'استفسر عن <em>Mijas Horizon Residences</em>', 'Vraag naar <em>Mijas Horizon Residences</em>',
  'Zapytaj o <em>Mijas Horizon Residences</em>', 'Spør om <em>Mijas Horizon Residences</em>',
  'Fråga om <em>Mijas Horizon Residences</em>')
a('.enquiry.message',
  'Quisiera conocer la disponibilidad y los precios actuales de Mijas Horizon Residences.',
  'Je souhaite connaître la disponibilité et les prix actuels de Mijas Horizon Residences.',
  'Ich möchte die aktuelle Verfügbarkeit und die Preise für Mijas Horizon Residences erfahren.',
  'Хочу узнать актуальное наличие и цены на Mijas Horizon Residences.',
  'أرغب في معرفة التوافر والأسعار الحالية لمشروع Mijas Horizon Residences.',
  'Ik wil graag de actuele beschikbaarheid en prijzen van Mijas Horizon Residences weten.',
  'Chciałbym poznać aktualną dostępność i ceny w Mijas Horizon Residences.',
  'Jeg vil gjerne ha gjeldende tilgjengelighet og priser for Mijas Horizon Residences.',
  'Jag skulle vilja få aktuell tillgänglighet och aktuella priser för Mijas Horizon Residences.')
a('.faq[0][1]',
  'La promoción tiene 75 viviendas de dos o tres dormitorios. La lista de precios nombra cuatro: tres están disponibles, un apartamento de dos dormitorios por {E365000}, un apartamento de tres dormitorios por {E480000} y un ático de dos dormitorios por {E530000}, y una está reservada.',
  'L’ensemble compte 75 logements de deux ou trois chambres. La liste de prix en nomme quatre : trois sont disponibles, un appartement de deux chambres à {E365000}, un appartement de trois chambres à {E480000} et un penthouse de deux chambres à {E530000}, et un est réservé.',
  'Die Anlage hat 75 Wohnungen mit zwei oder drei Schlafzimmern. Die Preisliste nennt vier: Drei sind verfügbar, ein Apartment mit zwei Schlafzimmern für {E365000}, ein Apartment mit drei Schlafzimmern für {E480000} und ein Penthouse mit zwei Schlafzimmern für {E530000}, und eine ist reserviert.',
  'В комплексе 75 квартир с двумя или тремя спальнями. В прайс-листе названы четыре: три доступны — двухспальные апартаменты за {E365000}, трёхспальные апартаменты за {E480000} и двухспальный пентхаус за {E530000}, а одна забронирована.',
  'يضم المشروع 75 مسكناً بغرفتي نوم أو ثلاث غرف نوم. وتذكر قائمة الأسعار أربعة منها: ثلاثة متاحة، هي شقة بغرفتي نوم بسعر {E365000}، وشقة بثلاث غرف نوم بسعر {E480000}، وبنتهاوس بغرفتي نوم بسعر {E530000}، وواحد محجوز.',
  'Het project heeft 75 woningen met twee of drie slaapkamers. De prijslijst noemt er vier: drie zijn beschikbaar, een appartement met twee slaapkamers voor {E365000}, een appartement met drie slaapkamers voor {E480000} en een penthouse met twee slaapkamers voor {E530000}, en een is gereserveerd.',
  'Inwestycja obejmuje 75 lokali z dwiema lub trzema sypialniami. Cennik wymienia cztery: trzy są dostępne, apartament z dwiema sypialniami za {E365000}, apartament z trzema sypialniami za {E480000} i penthouse z dwiema sypialniami za {E530000}, a jeden jest zarezerwowany.',
  'Prosjektet har 75 boliger med to eller tre soverom. Prislisten nevner fire: tre er ledige, en leilighet med to soverom for {E365000}, en leilighet med tre soverom for {E480000} og en toppleilighet med to soverom for {E530000}, og én er reservert.',
  'Projektet har 75 bostäder med två eller tre sovrum. Prislistan nämner fyra: tre är lediga, en lägenhet med två sovrum för {E365000}, en lägenhet med tre sovrum för {E480000} och en takvåning med två sovrum för {E530000}, och en är reserverad.')
a('.faq[1][1]',
  'No. La lista de precios dice que el {T} no está incluido. Se añaden el {T} del 10 % y el impuesto de actos jurídicos documentados del 1,20 %, además de los gastos de notaría y registro.',
  'Non. La liste de prix précise que la {T} n’est pas incluse. La {T} à 10 % et le droit de timbre à 1,20 % s’ajoutent, ainsi que les frais de notaire et de registre foncier.',
  'Nein. Die Preisliste besagt, dass die {T} nicht enthalten ist. Hinzu kommen {T} von 10 % und Stempelsteuer von 1,20 % sowie Notar- und Grundbuchgebühren.',
  'Нет. В прайс-листе сказано, что {T} не включён. Добавляются {T} 10 % и гербовый сбор 1,20 %, а также расходы на нотариуса и регистрацию.',
  'لا. تنص قائمة الأسعار على أن {T} غير مشمولة. وتُضاف {T} بنسبة 10% وضريبة الدمغة بنسبة 1.20%، إضافة إلى رسوم الكاتب العدل والسجل العقاري.',
  'Nee. De prijslijst zegt dat de {T} niet is inbegrepen. Er komen {T} van 10% en zegelrecht van 1,20% bij, plus de kosten van notaris en kadaster.',
  'Nie. Cennik podaje, że {T} nie jest wliczony. Dolicza się {T} w wysokości 10% i podatek od czynności dokumentowanych w wysokości 1,20% oraz opłaty notarialne i za wpis do księgi wieczystej.',
  'Nei. Prislisten sier at {T} ikke er inkludert. {T} på 10 % og dokumentavgift på 1,20 % kommer i tillegg, sammen med notar- og tinglysingsgebyrer.',
  'Nej. Prislistan anger att {T} inte ingår. {T} på 10 % och stämpelskatt på 1,20 % tillkommer, tillsammans med notarie- och fastighetsregisteravgifter.')
a('.faq[2][0]',
  '¿Están incluidos una plaza de garaje y un trastero?', 'Une place de garage et une cave sont-elles incluses ?',
  'Sind ein Garagenstellplatz und ein Abstellraum enthalten?', 'Входят ли в цену машиноместо и кладовая?',
  'هل يشمل السعر موقف سيارات في المرآب ومخزناً؟', 'Zijn een garageplaats en een berging inbegrepen?',
  'Czy miejsce garażowe i komórka lokatorska są wliczone?', 'Er garasjeplass og bod inkludert?',
  'Ingår en garageplats och ett förråd?')
a('.faq[2][1]',
  'Cada vivienda de la lista tiene una plaza de garaje y un trastero numerados en la misma línea que su precio, y la memoria de calidades recoge trasteros con toma de luz y una puerta de garaje motorizada. Los documentos no dicen con palabras que ambos estén en el precio, así que lo confirmamos por escrito.',
  'Chaque logement de la liste a une place de garage et une cave numérotées sur la même ligne que son prix, et le descriptif de qualité mentionne des caves avec prise d’éclairage et une porte de garage motorisée. Les documents ne disent pas en toutes lettres que les deux sont dans le prix ; nous le confirmons donc par écrit.',
  'Jede gelistete Wohnung hat einen nummerierten Garagenstellplatz und Abstellraum in derselben Zeile wie ihren Preis, und die Baubeschreibung nennt Abstellräume mit Lichtanschluss und ein motorisiertes Garagentor. Die Unterlagen sagen nicht in Worten, dass beides im Preis enthalten ist, daher lassen wir es uns schriftlich bestätigen.',
  'У каждой квартиры из списка пронумерованные машиноместо и кладовая указаны в той же строке, что и цена, а в описании качества упомянуты кладовые с выводом для освещения и гаражные ворота с электроприводом. В документах прямо не сказано, что оба входят в цену, поэтому мы подтверждаем это письменно.',
  'لكل مسكن في القائمة موقف سيارات في المرآب ومخزن مرقّمان في السطر نفسه الذي يرد فيه سعره، وتذكر وثيقة المواصفات مخازن بنقطة إنارة وباب مرآب بمحرك. ولا تذكر الوثائق صراحةً أن كليهما داخل السعر، لذلك نؤكد ذلك كتابةً.',
  'Elke vermelde woning heeft een genummerde garageplaats en berging op dezelfde regel als haar prijs, en de technische omschrijving noemt bergingen met een lichtaansluiting en een gemotoriseerde garagedeur. De documenten zeggen niet met zoveel woorden dat beide in de prijs zitten, dus we laten het schriftelijk bevestigen.',
  'Każdy lokal z wykazu ma numerowane miejsce garażowe i komórkę lokatorską w tym samym wierszu co cena, a standard wykończenia wymienia komórki z punktem oświetleniowym i napędzaną bramę garażową. Dokumenty nie mówią wprost, że obie rzeczy są w cenie, więc potwierdzamy to na piśmie.',
  'Hver oppførte bolig har en nummerert garasjeplass og bod på samme linje som prisen, og byggebeskrivelsen nevner boder med lysuttak og en motorisert garasjeport. Dokumentene sier ikke med ord at begge er med i prisen, så vi får det bekreftet skriftlig.',
  'Varje listad bostad har en numrerad garageplats och ett förråd på samma rad som priset, och byggbeskrivningen nämner förråd med ljusuttag och en motoriserad garageport. Dokumenten säger inte med ord att båda ingår i priset, så vi låter bekräfta det skriftligen.')
a('.faq[3][1]',
  'Las condiciones de pago dan el cuarto trimestre de 2027 para la escritura y la entrega de llaves. Ningún otro documento da una fecha, una licencia ni una fase de obra, así que los pedimos, junto con lo que dice el contrato si la fecha se retrasa.',
  'Les conditions de paiement donnent le quatrième trimestre 2027 pour l’acte et la remise des clés. Aucun autre document ne donne de date, de permis ni d’état d’avancement ; nous les demandons donc, ainsi que ce que dit le contrat si la date glisse.',
  'Die Zahlungsbedingungen nennen das vierte Quartal 2027 für Beurkundung und Schlüsselübergabe. Kein anderes Dokument nennt einen Termin, eine Genehmigung oder einen Bauabschnitt, daher verlangen wir sie, ebenso wie die vertragliche Regelung für den Fall einer Verzögerung.',
  'В условиях оплаты нотариальный акт и передача ключей назначены на четвёртый квартал 2027 года. Ни один другой документ не называет ни срока, ни разрешения, ни стадии строительства, поэтому мы запрашиваем их, а также условия договора на случай переноса срока.',
  'تحدد شروط الدفع الربع الرابع من عام 2027 لسند الملكية وتسليم المفاتيح. ولا تذكر أي وثيقة أخرى موعداً أو رخصة أو مرحلة أعمال، لذلك نطلبها، مع ما ينص عليه العقد إذا تأخر الموعد.',
  'De betalingsvoorwaarden noemen het vierde kwartaal van 2027 voor de akte en de sleuteloverdracht. Geen enkel ander document noemt een datum, een vergunning of een bouwfase, dus we vragen ze op, met wat het contract zegt als de datum uitloopt.',
  'Warunki płatności podają czwarty kwartał 2027 roku na akt notarialny i przekazanie kluczy. Żaden inny dokument nie podaje terminu, pozwolenia ani etapu prac, więc o nie prosimy, wraz z zapisem umowy na wypadek opóźnienia terminu.',
  'Betalingsvilkårene oppgir fjerde kvartal 2027 for skjøtet og nøkkeloverleveringen. Ingen andre dokumenter oppgir en dato, en tillatelse eller et byggetrinn, så vi ber om dem, sammen med hva kontrakten sier hvis datoen forsinkes.',
  'Betalningsvillkoren anger fjärde kvartalet 2027 för lagfarten och nyckelöverlämnandet. Inget annat dokument anger ett datum, ett bygglov eller ett byggskede, så vi ber om dem, tillsammans med vad avtalet säger om datumet försenas.')
a('.faq[4][1]',
  '{E6000} más {T} en la reserva, un 15 % más {T} en el contrato privado 60 días después, descontada la reserva, un 15 % más {T} el 5 de mayo de 2027 y un 70 % más {T} en la escritura, al terminar y entregar las llaves.',
  '{E6000} hors {T} à la réservation, 15 % hors {T} au contrat privé 60 jours plus tard, déduction faite de la réservation, 15 % hors {T} le 5 mai 2027 et 70 % hors {T} à l’acte, à l’achèvement et à la remise des clés.',
  '{E6000} zuzüglich {T} bei der Reservierung, 15 % zuzüglich {T} beim privaten Vertrag 60 Tage später, abzüglich der Reservierung, 15 % zuzüglich {T} am 5. Mai 2027 und 70 % zuzüglich {T} bei der Beurkundung, bei Fertigstellung und Schlüsselübergabe.',
  '{E6000} плюс {T} при бронировании, 15 % плюс {T} при частном договоре через 60 дней за вычетом бронирования, 15 % плюс {T} 5 мая 2027 года и 70 % плюс {T} при сделке, при завершении и передаче ключей.',
  '{E6000} زائد {T} عند الحجز، و15% زائد {T} عند العقد الخاص بعد 60 يوماً مع خصم مبلغ الحجز، و15% زائد {T} في 5 مايو 2027، و70% زائد {T} عند سند الملكية، عند الإنجاز وتسليم المفاتيح.',
  '{E6000} plus {T} bij de reservering, 15% plus {T} bij het onderhandse contract 60 dagen later, na aftrek van de reservering, 15% plus {T} op 5 mei 2027 en 70% plus {T} bij de akte, bij oplevering en sleuteloverdracht.',
  '{E6000} plus {T} przy rezerwacji, 15% plus {T} przy umowie przedwstępnej 60 dni później, pomniejszone o rezerwację, 15% plus {T} 5 maja 2027 roku i 70% plus {T} przy akcie notarialnym, przy zakończeniu i przekazaniu kluczy.',
  '{E6000} pluss {T} ved reservasjon, 15 % pluss {T} ved den private kontrakten 60 dager senere, fratrukket reservasjonen, 15 % pluss {T} den 5. mai 2027 og 70 % pluss {T} ved skjøtet, ved ferdigstillelse og nøkkeloverlevering.',
  '{E6000} plus {T} vid reservation, 15 % plus {T} vid det privata avtalet 60 dagar senare, med avdrag för reservationen, 15 % plus {T} den 5 maj 2027 och 70 % plus {T} vid lagfarten, vid färdigställande och nyckelöverlämnande.')
a('.faq[5][1]',
  'Una piscina central con zona chill-out, un gimnasio equipado, una sala de coworking, un club social, una zona de barbacoa y pícnic y más de {N13,000} {U} de jardines, tal como los recogen el catálogo y la memoria de calidades.',
  'Une piscine centrale avec espace chill-out, une salle de sport équipée, un espace de coworking, un club social, un espace barbecue et pique-nique et plus de {N13,000} {U} de jardins, tels que les listent le catalogue et le descriptif de qualité.',
  'Ein zentraler Pool mit Chill-out-Bereich, ein ausgestatteter Fitnessraum, ein Coworking-Raum, ein Social Club, ein Grill- und Picknickbereich und mehr als {N13,000} {U} Gärten, wie Katalog und Baubeschreibung sie aufführen.',
  'Центральный бассейн с зоной отдыха, оборудованный тренажёрный зал, зал коворкинга, клуб для жильцов, зона барбекю и пикника и более {N13,000} {U} садов — так их перечисляют каталог и описание качества.',
  'مسبح مركزي مع ركن استرخاء، وصالة رياضية مجهّزة، وقاعة عمل مشترك، ونادٍ اجتماعي، ومنطقة شواء ونزهات، وحدائق تزيد على {N13,000} {U}، كما يوردها الكتالوج ووثيقة المواصفات.',
  'Een centraal zwembad met chill-outzone, een ingerichte fitnessruimte, een coworkingruimte, een sociale club, een barbecue- en picknickzone en meer dan {N13,000} {U} tuinen, zoals de catalogus en de technische omschrijving ze opsommen.',
  'Centralny basen ze strefą relaksu, wyposażona siłownia, sala coworkingowa, klub dla mieszkańców, strefa grillowa i piknikowa oraz ponad {N13,000} {U} ogrodów, tak jak wymieniają je katalog i standard wykończenia.',
  'Et sentralt basseng med chill-out-sone, et utstyrt treningsrom, et coworking-rom, en sosial klubb, et grill- og piknikområde og mer enn {N13,000} {U} hager, slik katalogen og byggebeskrivelsen oppgir dem.',
  'En central pool med chill-out-zon, ett utrustat gym, ett coworkingrum, en social klubb, en grill- och picknickyta och mer än {N13,000} {U} trädgårdar, så som katalogen och byggbeskrivningen listar dem.')
a('.faq[6][1]',
  'La lista de precios es la del promotor y puede revisarse antes de firmar una reserva. Nueva Living reconfirma la cifra con el promotor antes de que usted se comprometa a nada.',
  'La liste de prix est celle du promoteur et peut être révisée avant la signature d’une réservation. Nueva Living reconfirme le chiffre auprès du promoteur avant que vous ne vous engagiez à quoi que ce soit.',
  'Die Preisliste stammt vom Bauträger und kann vor der Unterzeichnung einer Reservierung angepasst werden. Nueva Living lässt sich die Zahl vom Bauträger erneut bestätigen, bevor Sie sich zu irgendetwas verpflichten.',
  'Прайс-лист принадлежит застройщику и может быть пересмотрен до подписания бронирования. Nueva Living заново подтверждает сумму у застройщика, прежде чем вы на что-либо согласитесь.',
  'قائمة الأسعار هي قائمة المطوّر ويمكن مراجعتها قبل توقيع الحجز. تعيد Nueva Living تأكيد الرقم مع المطوّر قبل أن تلتزم بأي شيء.',
  'De prijslijst is die van de ontwikkelaar en kan worden herzien voordat een reservering wordt getekend. Nueva Living laat het bedrag opnieuw bij de ontwikkelaar bevestigen voordat u zich ergens toe verbindt.',
  'Cennik jest cennikiem dewelopera i może zostać zmieniony przed podpisaniem rezerwacji. Nueva Living ponownie potwierdza kwotę u dewelopera, zanim Państwo się do czegokolwiek zobowiążą.',
  'Prislisten er utbyggerens og kan revideres før en reservasjon signeres. Nueva Living får beløpet bekreftet på nytt av utbyggeren før du forplikter deg til noe.',
  'Prislistan är exploatörens och kan revideras innan en reservation skrivs under. Nueva Living låter exploatören bekräfta beloppet på nytt innan ni förbinder er till något.')
a('.seo.title',
  'Mijas Horizon Residences - Viviendas con terraza en Mijas Costa',
  'Mijas Horizon Residences - Logements avec terrasse à Mijas Costa',
  'Mijas Horizon Residences - Wohnungen mit Terrasse in Mijas Costa',
  'Mijas Horizon Residences - Квартиры с террасой в Михас-Коста',
  'Mijas Horizon Residences - مساكن بتراس في ميخاس كوستا',
  'Mijas Horizon Residences - Woningen met terras in Mijas Costa',
  'Mijas Horizon Residences - Lokale z tarasem w Mijas Costa',
  'Mijas Horizon Residences - Boliger med terrasse i Mijas Costa',
  'Mijas Horizon Residences - Bostäder med terrass i Mijas Costa')
a('.seo.h1',
  'Mijas Horizon Residences: viviendas con terraza en Mijas Costa',
  'Mijas Horizon Residences : logements avec terrasse à Mijas Costa',
  'Mijas Horizon Residences: Wohnungen mit Terrasse in Mijas Costa',
  'Mijas Horizon Residences: квартиры с террасой в Михас-Коста',
  'Mijas Horizon Residences: مساكن بتراس في ميخاس كوستا',
  'Mijas Horizon Residences: woningen met terras in Mijas Costa',
  'Mijas Horizon Residences: lokale z tarasem w Mijas Costa',
  'Mijas Horizon Residences: boliger med terrasse i Mijas Costa',
  'Mijas Horizon Residences: bostäder med terrass i Mijas Costa')
a('.seo.h1Context',
  'Viviendas con terraza en Mijas Costa', 'Logements avec terrasse à Mijas Costa', 'Wohnungen mit Terrasse in Mijas Costa',
  'Квартиры с террасой в Михас-Коста', 'مساكن بتراس في ميخاس كوستا', 'Woningen met terras in Mijas Costa',
  'Lokale z tarasem w Mijas Costa', 'Boliger med terrasse i Mijas Costa', 'Bostäder med terrass i Mijas Costa')

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings')
