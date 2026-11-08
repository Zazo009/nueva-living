# -*- coding: utf-8 -*-
"""Mijas Olive Townhouses: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E505000}
money, {N94.15} decimal number, {U} the area unit.
    python3 tools/import/k_mijas_olive_townhouses.py <scratch dir>   (writes <dir>/tr_a.json, then run assemble.py)

Wording follows what the siblings already say in each language: townhouses as the translation
memory has them (adosados, maisons mitoyennes, Reihenhäuser, таунхаусы, rijwoningen, domy szeregowe,
rekkehus, radhus), the tax word the audit wants (IVA, TVA, MwSt., НДС, ضريبة القيمة المضافة, btw, VAT,
mva, IVA), and a price only ever as a {E...} token so that it takes the locale's own shape.
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/mijas-olive-townhouses/project.json'))


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


# ---- name ---------------------------------------------------------------------------------------
same('Mijas Olive Townhouses'); same('Mijas Olive'); same('Mijas Olive <em>Townhouses</em>')

# ---- description, SEO, hero, card ---------------------------------------------------------------

a('.description',
  'Adosados de tres dormitorios con jardín privado en una urbanización cerrada de 140 viviendas en Mijas Costa, frente a un espacio natural de frondosos pinos. Tres viviendas de la primera fase figuran en la lista de precios, desde {E495000} más IVA.',
  'Maisons mitoyennes de trois chambres avec jardin privatif, dans une résidence fermée de 140 logements à Mijas Costa, face à un espace naturel de pins denses. Trois logements de la première phase figurent sur la liste de prix, à partir de {E495000} hors TVA.',
  'Reihenhäuser mit drei Schlafzimmern und Privatgarten in einer geschlossenen Wohnanlage mit 140 Häusern in Mijas Costa, gegenüber einem Naturraum mit dichtem Kiefernbestand. Drei Häuser der ersten Phase stehen auf der Preisliste, ab {E495000} zuzüglich MwSt.',
  'Таунхаусы с тремя спальнями и собственным садом в закрытом комплексе из 140 домов в Михас-Коста, напротив природной зоны с густым сосновым лесом. В прайс-листе первой фазы указаны три дома, от {E495000} без НДС.',
  'منازل متلاصقة بثلاث غرف نوم وحديقة خاصة في مجمع مغلق من 140 مسكناً في ميخاس كوستا، مقابل مساحة طبيعية كثيفة بأشجار الصنوبر. ثلاثة مساكن من المرحلة الأولى مدرجة في قائمة الأسعار، ابتداءً من {E495000} دون ضريبة القيمة المضافة.',
  'Rijwoningen met drie slaapkamers en een privétuin in een besloten complex van 140 woningen in Mijas Costa, tegenover een natuurgebied met dichte dennen. Drie woningen van de eerste fase staan op de prijslijst, vanaf {E495000} excl. btw.',
  'Domy szeregowe z trzema sypialniami i prywatnym ogrodem w zamkniętym osiedlu liczącym 140 domów w Mijas Costa, naprzeciw terenu naturalnego z gęstym sosnowym lasem. Trzy domy pierwszego etapu są w cenniku, od {E495000} plus VAT.',
  'Rekkehus med tre soverom og egen hage i et bevoktet område med 140 boliger i Mijas Costa, vendt mot et naturområde med tett furuskog. Tre boliger i første fase står på prislisten, fra {E495000} pluss mva.',
  'Radhus med tre sovrum och egen trädgård i ett bevakat område med 140 bostäder i Mijas Costa, vända mot ett naturområde med tät tallskog. Tre bostäder i den första fasen finns i prislistan, från {E495000} plus IVA (spansk moms).')
a('.seoDescription',
  'Adosados de obra nueva de tres dormitorios con jardín privado en Mijas Costa, con tres piscinas, gimnasio y club social, desde {E495000} más IVA.',
  'Maisons mitoyennes neuves de trois chambres avec jardin privatif à Mijas Costa, avec trois piscines, une salle de sport et un club social, à partir de {E495000} hors TVA.',
  'Neubau-Reihenhäuser mit drei Schlafzimmern und Privatgarten in Mijas Costa, mit drei Pools, Fitnessraum und Clubraum, ab {E495000} zuzüglich MwSt.',
  'Новые таунхаусы с тремя спальнями и собственным садом в Михас-Коста, с тремя бассейнами, тренажёрным залом и клубом, от {E495000} без НДС.',
  'منازل متلاصقة جديدة بثلاث غرف نوم وحدائق خاصة في ميخاس كوستا، مع ثلاثة مسابح وصالة رياضية ونادٍ اجتماعي، ابتداءً من {E495000} دون ضريبة القيمة المضافة.',
  'Nieuwbouwrijwoningen met drie slaapkamers en privétuin in Mijas Costa, met drie zwembaden, een fitnessruimte en een sociale club, vanaf {E495000} excl. btw.',
  'Nowe domy szeregowe z trzema sypialniami i prywatnym ogrodem w Mijas Costa, z trzema basenami, siłownią i klubem, od {E495000} plus VAT.',
  'Nye rekkehus med tre soverom og egen hage i Mijas Costa, med tre basseng, treningsrom og sosial klubb, fra {E495000} pluss mva.',
  'Nybyggda radhus med tre sovrum och egen trädgård i Mijas Costa, med tre pooler, gym och klubblokal, från {E495000} plus IVA.')
a('.twitterDescription',
  'Adosados de tres dormitorios con jardín en Mijas Costa, desde {E495000} más IVA.',
  'Maisons mitoyennes de trois chambres avec jardin à Mijas Costa, à partir de {E495000} hors TVA.',
  'Reihenhäuser mit drei Schlafzimmern und Garten in Mijas Costa, ab {E495000} zuzüglich MwSt.',
  'Таунхаусы с тремя спальнями и садом в Михас-Коста, от {E495000} без НДС.',
  'منازل متلاصقة بثلاث غرف نوم وحدائق في ميخاس كوستا، ابتداءً من {E495000} دون ضريبة القيمة المضافة.',
  'Rijwoningen met drie slaapkamers en tuin in Mijas Costa, vanaf {E495000} excl. btw.',
  'Domy szeregowe z trzema sypialniami i ogrodem w Mijas Costa, od {E495000} plus VAT.',
  'Rekkehus med tre soverom og hage i Mijas Costa, fra {E495000} pluss mva.',
  'Radhus med tre sovrum och trädgård i Mijas Costa, från {E495000} plus IVA.')
a('.hero.eyebrow', '3 de 140 viviendas disponibles', '3 logements disponibles sur 140', '3 von 140 Häusern verfügbar',
  '3 из 140 домов доступно', '3 من 140 منزلاً متاحاً', '3 van de 140 woningen beschikbaar', '3 z 140 domów dostępnych',
  '3 av 140 boliger ledige', '3 av 140 bostäder lediga')
a('.quickFacts[6][1]', '3 de 140 viviendas disponibles', '3 logements disponibles sur 140', '3 von 140 Häusern verfügbar',
  '3 из 140 домов доступно', '3 من 140 منزلاً متاحاً', '3 van de 140 woningen beschikbaar', '3 z 140 domów dostępnych',
  '3 av 140 boliger ledige', '3 av 140 bostäder lediga')
a('.hero.location', 'Mijas Costa, Mijas', 'Mijas Costa, Mijas', 'Mijas Costa, Mijas', 'Михас-Коста, Михас',
  'ميخاس كوستا، ميخاس', 'Mijas Costa, Mijas', 'Mijas Costa, Mijas', 'Mijas Costa, Mijas', 'Mijas Costa, Mijas')
a('.hero.startingPrice', 'Desde {E495000} + IVA', 'À partir de {E495000} + TVA', 'Ab {E495000} + MwSt.', 'От {E495000} + НДС',
  'ابتداءً من {E495000} + ضريبة القيمة المضافة', 'Vanaf {E495000} + btw', 'Od {E495000} + VAT', 'Fra {E495000} + mva', 'Från {E495000} + IVA')
a('.card.meta[0][1]', '{E495000} + IVA', '{E495000} + TVA', '{E495000} + MwSt.', '{E495000} + НДС',
  '{E495000} + ضريبة القيمة المضافة', '{E495000} + btw', '{E495000} + VAT', '{E495000} + mva', '{E495000} + IVA')
a('.hero.delivery', 'Entrega T3 2028', 'Livraison T3 2028', 'Fertigstellung Q3 2028', 'Сдача 3 кв. 2028',
  'الإنجاز الربع الثالث 2028', 'Oplevering K3 2028', 'Odbiór III kw. 2028', 'Ferdigstillelse K3 2028', 'Färdigställande K3 2028')
a('.card.description',
  'Adosados de tres dormitorios con jardín privado en una urbanización cerrada de 140 viviendas en Mijas Costa, con tres piscinas, gimnasio y club social.',
  'Maisons mitoyennes de trois chambres avec jardin privatif dans une résidence fermée de 140 logements à Mijas Costa, avec trois piscines, une salle de sport et un club social.',
  'Reihenhäuser mit drei Schlafzimmern und Privatgarten in einer geschlossenen Wohnanlage mit 140 Häusern in Mijas Costa, mit drei Pools, Fitnessraum und Clubraum.',
  'Таунхаусы с тремя спальнями и собственным садом в закрытом комплексе из 140 домов в Михас-Коста: три бассейна, тренажёрный зал и клуб.',
  'منازل متلاصقة بثلاث غرف نوم وحديقة خاصة في مجمع مغلق من 140 مسكناً في ميخاس كوستا، مع ثلاثة مسابح وصالة رياضية ونادٍ اجتماعي.',
  'Rijwoningen met drie slaapkamers en een privétuin in een besloten complex van 140 woningen in Mijas Costa, met drie zwembaden, een fitnessruimte en een sociale club.',
  'Domy szeregowe z trzema sypialniami i prywatnym ogrodem w zamkniętym osiedlu liczącym 140 domów w Mijas Costa, z trzema basenami, siłownią i klubem.',
  'Rekkehus med tre soverom og egen hage i et bevoktet område med 140 boliger i Mijas Costa, med tre basseng, treningsrom og sosial klubb.',
  'Radhus med tre sovrum och egen trädgård i ett bevakat område med 140 bostäder i Mijas Costa, med tre pooler, gym och klubblokal.')

# ---- images and media ---------------------------------------------------------------------------

a('.images.hero.alt',
  'Vista aérea generada por ordenador de hileras de adosados blancos con paneles de aspecto madera alrededor de una piscina comunitaria, con colinas arboladas al fondo',
  'Vue aérienne générée par ordinateur de rangées de maisons mitoyennes blanches à panneaux effet bois autour d’une piscine commune, avec des collines boisées en arrière-plan',
  'Computergenerierte Luftansicht weißer Reihenhauszeilen mit holzähnlichen Verkleidungen rund um einen Gemeinschaftspool, dahinter bewaldete Hügel',
  'Компьютерная визуализация с высоты: ряды белых таунхаусов с панелями под дерево вокруг общего бассейна, за ними лесистые холмы',
  'منظر جوي مولَّد بالحاسوب لصفوف من المنازل المتلاصقة البيضاء بألواح تحاكي الخشب حول مسبح مشترك، وخلفها تلال مكسوة بالأشجار',
  'Computergegenereerd luchtbeeld van rijen witte rijwoningen met houtlookpanelen rond een gemeenschappelijk zwembad, met beboste heuvels erachter',
  'Wygenerowany komputerowo widok z lotu ptaka na rzędy białych domów szeregowych z panelami imitującymi drewno wokół wspólnego basenu, za nimi zalesione wzgórza',
  'Datagenerert luftbilde av rader med hvite rekkehus med trelignende paneler rundt et felles basseng, med skogkledde åser bak',
  'Datorgenererad flygvy över rader av vita radhus med träliknande paneler runt en gemensam pool, med skogsklädda kullar bakom')
a('.images.architecture.alt',
  'Vista generada por ordenador de la piscina, una zona de descanso con suelo de arena y dos camas balinesas con dosel, y una hilera de adosados al fondo',
  'Vue générée par ordinateur de la piscine, d’un espace détente au sol de sable avec deux lits de repos à baldaquin et, au-delà, une rangée de maisons mitoyennes',
  'Computergenerierte Ansicht des Pools, einer Lounge mit Sandboden und zwei Liegen mit Baldachin und dahinter einer Reihe von Reihenhäusern',
  'Компьютерная визуализация бассейна, зоны отдыха с песчаным покрытием и двумя кушетками под балдахином, а за ними — ряда таунхаусов',
  'منظر مولَّد بالحاسوب للمسبح ومنطقة استرخاء أرضيتها من الرمل وفيها سريرا استلقاء بمظلة، وخلفها صف من المنازل المتلاصقة',
  'Computergegenereerd beeld van het zwembad, een loungeplek met zandvloer en twee ligbedden met luifel, en daarachter een rij rijwoningen',
  'Wygenerowany komputerowo widok na basen, strefę wypoczynku z piaskową podłogą i dwoma łóżkami plażowymi z baldachimem oraz rząd domów szeregowych w tle',
  'Datagenerert bilde av bassenget, en loungesone med sandgulv og to solsenger med baldakin, og en rekke rekkehus bak',
  'Datorgenererad vy av poolen, en loungeyta med sandgolv och två solsängar med baldakin, och en rad radhus bakom')
a('.images.lifestyle.alt',
  'Vista generada por ordenador al anochecer a través de la piscina comunitaria hacia palmeras y un edificio de dos plantas con terraza cubierta y tumbonas',
  'Vue générée par ordinateur au crépuscule, par-dessus la piscine commune, vers des palmiers et un bâtiment de deux niveaux avec terrasse couverte et bains de soleil',
  'Computergenerierte Ansicht in der Dämmerung über den Gemeinschaftspool hinweg zu Palmen und einem zweigeschossigen Gebäude mit überdachter Terrasse und Sonnenliegen',
  'Компьютерная визуализация в сумерках: общий бассейн, пальмы и двухэтажное здание с крытой террасой и шезлонгами',
  'منظر مولَّد بالحاسوب عند الغسق عبر المسبح المشترك نحو أشجار النخيل ومبنى من طابقين بشرفة مسقوفة وكراسي استلقاء',
  'Computergegenereerd beeld bij schemering over het gemeenschappelijke zwembad naar palmbomen en een gebouw met twee verdiepingen, met overdekt terras en ligbedden',
  'Wygenerowany komputerowo widok o zmierzchu znad wspólnego basenu na palmy i dwukondygnacyjny budynek z zadaszonym tarasem i leżakami',
  'Datagenerert bilde i skumringen over det felles bassenget mot palmer og en bygning i to etasjer med overbygd terrasse og solsenger',
  'Datorgenererad vy i skymning över den gemensamma poolen mot palmer och en byggnad i två våningar med överbyggd terrass och solstolar')
a('.images.privateViewing.alt',
  'Cocina abierta generada por ordenador, con muebles blancos y una barra de desayuno, y una mesa de comedor al lado',
  'Cuisine ouverte générée par ordinateur, avec des meubles blancs et un bar de petit-déjeuner, et une table à manger à côté',
  'Computergenerierte offene Küche mit weißen Fronten und einer Frühstücksbar, daneben ein Esstisch',
  'Компьютерная визуализация открытой кухни с белыми фасадами и барной стойкой, рядом обеденный стол',
  'مطبخ مفتوح مولَّد بالحاسوب بوحدات بيضاء وطاولة إفطار، وبجانبه طاولة طعام',
  'Computergegenereerde open keuken met witte kasten en een ontbijtbar, met een eettafel ernaast',
  'Wygenerowana komputerowo otwarta kuchnia z białymi szafkami i barkiem śniadaniowym oraz stołem jadalnianym obok',
  'Datagenerert åpent kjøkken med hvite skap og en frokostbar, og et spisebord ved siden av',
  'Datorgenererat öppet kök med vita skåp och en frukostbar, och ett matbord bredvid')
a('.media.copy',
  'Vistas generadas por ordenador de la promoción, las piscinas y los interiores, y los planos de las tres viviendas de la lista de precios.',
  'Vues générées par ordinateur de l’ensemble, des piscines et des intérieurs, et plans des trois logements de la liste de prix.',
  'Computergenerierte Ansichten der Anlage, der Pools und der Innenräume sowie die Grundrisse der drei Häuser auf der Preisliste.',
  'Компьютерные визуализации комплекса, бассейнов и интерьеров и планировки трёх домов из прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمشروع والمسابح والتصاميم الداخلية، ومخططات المساكن الثلاثة الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van het complex, de zwembaden en de interieurs, en de plattegronden van de drie woningen op de prijslijst.',
  'Wygenerowane komputerowo widoki inwestycji, basenów i wnętrz oraz rzuty trzech domów z cennika.',
  'Datagenererte bilder av området, bassengene og interiørene, og plantegningene av de tre boligene på prislisten.',
  'Datorgenererade vyer av området, poolerna och interiörerna samt planritningarna för de tre bostäderna i prislistan.')
a('.media.note',
  'Todas las imágenes están generadas por ordenador y son meramente orientativas, y el mobiliario, la decoración y la vegetación que muestran no forman parte de la oferta. Los planos son los planos de proyecto del promotor, con fecha 23 de julio de 2026 (28 de octubre de 2025 para la vivienda 10); las superficies que figuran en ellos son aproximadas y pueden cambiar por exigencias técnicas o legales, y los nombres de las estancias están en inglés.',
  'Toutes les images sont générées par ordinateur et données à titre indicatif, et le mobilier, la décoration et la végétation qu’elles montrent ne font pas partie de l’offre. Les plans sont les plans de projet du promoteur, datés du 23 juillet 2026 (28 octobre 2025 pour le logement 10) ; les surfaces qui y figurent sont approximatives et peuvent changer pour des raisons techniques ou légales, et le nom des pièces y est en anglais.',
  'Alle Bilder sind computergeneriert und dienen nur zur Orientierung; Möbel, Dekoration und Bepflanzung darauf gehören nicht zum Angebot. Die Grundrisse sind die Projektpläne des Bauträgers vom 23. Juli 2026 (28. Oktober 2025 für Haus 10); die darauf angegebenen Flächen sind ungefähre Werte und können sich aus technischen oder rechtlichen Gründen ändern, und die Raumbezeichnungen sind auf Englisch.',
  'Все изображения созданы на компьютере и носят ориентировочный характер; мебель, отделка и озеленение на них не входят в предложение. Планировки — проектные планы застройщика от 23 июля 2026 года (28 октября 2025 года для дома 10); площади на них приблизительные и могут измениться по техническим или юридическим причинам, а названия помещений даны на английском.',
  'جميع الصور مولَّدة بالحاسوب وللاسترشاد فقط، والأثاث والديكور والنباتات الظاهرة فيها ليست جزءاً من العرض. المخططات هي مخططات المشروع الصادرة عن المطوّر بتاريخ 23 يوليو 2026 (28 أكتوبر 2025 للمنزل 10)، والمساحات المبيّنة عليها تقريبية وقد تتغير لأسباب فنية أو قانونية، وأسماء الغرف عليها بالإنجليزية.',
  'Alle beelden zijn computergegenereerd en uitsluitend ter indicatie, en het meubilair, de inrichting en de beplanting erop maken geen deel uit van het aanbod. De plattegronden zijn de projectplannen van de ontwikkelaar van 23 juli 2026 (28 oktober 2025 voor woning 10); de oppervlakken erop zijn bij benadering en kunnen om technische of juridische redenen wijzigen, en de namen van de ruimtes staan in het Engels.',
  'Wszystkie obrazy są wygenerowane komputerowo i mają charakter orientacyjny, a meble, wystrój i zieleń na nich nie wchodzą w skład oferty. Rzuty to plany projektowe dewelopera z 23 lipca 2026 r. (28 października 2025 r. dla domu 10); podane na nich powierzchnie są przybliżone i mogą się zmienić z przyczyn technicznych lub prawnych, a nazwy pomieszczeń są po angielsku.',
  'Alle bildene er datagenererte og kun veiledende, og møbler, innredning og beplantning på dem er ikke en del av tilbudet. Plantegningene er utbyggerens prosjektplaner datert 23. juli 2026 (28. oktober 2025 for bolig 10); arealene på dem er omtrentlige og kan endres av tekniske eller juridiske grunner, og romnavnene er på engelsk.',
  'Alla bilder är datorgenererade och endast vägledande, och möbler, inredning och planteringar på dem ingår inte i erbjudandet. Planritningarna är exploatörens projektritningar daterade 23 juli 2026 (28 oktober 2025 för bostad 10); ytorna på dem är ungefärliga och kan ändras av tekniska eller juridiska skäl, och rumsnamnen är på engelska.')
a('.media.items[0].caption', 'Los adosados y la piscina comunitaria', 'Les maisons mitoyennes et la piscine commune',
  'Die Reihenhäuser und der Gemeinschaftspool', 'Таунхаусы и общий бассейн', 'المنازل المتلاصقة والمسبح المشترك',
  'De rijwoningen en het gemeenschappelijke zwembad', 'Domy szeregowe i wspólny basen', 'Rekkehusene og det felles bassenget',
  'Radhusen och den gemensamma poolen')
a('.media.items[1].caption', 'La piscina y la terraza de arena', 'La piscine et la terrasse de sable', 'Der Pool und die Sandterrasse',
  'Бассейн и песчаная терраса', 'المسبح وشرفة الرمل', 'Het zwembad en het zandterras', 'Basen i piaskowy taras',
  'Bassenget og sandterrassen', 'Poolen och sandterrassen')
a('.media.items[2].caption', 'La terraza de la piscina al anochecer', 'La terrasse de la piscine au crépuscule',
  'Die Poolterrasse in der Dämmerung', 'Терраса у бассейна в сумерках', 'شرفة المسبح عند الغسق',
  'Het zwembadterras bij schemering', 'Taras przy basenie o zmierzchu', 'Bassengterrassen i skumringen', 'Poolterrassen i skymning')
a('.media.items[3].alt',
  'Vista generada por ordenador de un adosado con terraza pavimentada y césped tras setos recortados, y el salón tras puertas correderas de cristal',
  'Vue générée par ordinateur d’une maison mitoyenne avec terrasse dallée et pelouse derrière des haies taillées, et le séjour derrière des portes vitrées coulissantes',
  'Computergenerierte Ansicht eines Reihenhauses mit gepflasterter Terrasse und Rasen hinter geschnittenen Hecken und mit dem Wohnzimmer hinter gläsernen Schiebetüren',
  'Компьютерная визуализация таунхауса с вымощенной террасой и газоном за подстриженными живыми изгородями, гостиная видна за стеклянными раздвижными дверями',
  'منظر مولَّد بالحاسوب لمنزل متلاصق بشرفة مرصوفة ومرج خلف سياجات نباتية مشذّبة، وغرفة المعيشة خلف أبواب زجاجية منزلقة',
  'Computergegenereerd beeld van een rijwoning met een bestraat terras en een gazon achter geknipte hagen, en de woonkamer achter glazen schuifdeuren',
  'Wygenerowany komputerowo widok domu szeregowego z brukowanym tarasem i trawnikiem za przystrzyżonymi żywopłotami oraz salonem za przesuwnymi szklanymi drzwiami',
  'Datagenerert bilde av et rekkehus med flislagt terrasse og plen bak klipte hekker, og stuen bak skyvedører i glass',
  'Datorgenererad vy av ett radhus med stenlagd terrass och gräsmatta bakom klippta häckar, och vardagsrummet bakom skjutdörrar i glas')
a('.media.items[3].caption', 'Terraza y jardín de un adosado', 'Terrasse et jardin d’une maison mitoyenne',
  'Terrasse und Garten eines Reihenhauses', 'Терраса и сад таунхауса', 'شرفة وحديقة منزل متلاصق',
  'Terras en tuin van een rijwoning', 'Taras i ogród domu szeregowego', 'Terrasse og hage til et rekkehus', 'Terrass och trädgård till ett radhus')
a('.media.items[4].alt',
  'Sala del club social generada por ordenador, con mesas de madera, sillas de ratán y lámparas colgantes, que se abre con puertas correderas a la terraza de la piscina',
  'Salle du club social générée par ordinateur, avec tables en bois, chaises en rotin et suspensions, s’ouvrant par des portes coulissantes sur la terrasse de la piscine',
  'Computergenerierter Clubraum mit Holztischen, Rattanstühlen und Hängeleuchten, der sich über Schiebetüren zur Poolterrasse öffnet',
  'Компьютерная визуализация клубного зала с деревянными столами, ротанговыми стульями и подвесными светильниками, раздвижные двери ведут на террасу у бассейна',
  'قاعة النادي الاجتماعي مولَّدة بالحاسوب بطاولات خشبية وكراسٍ من الروطان ومصابيح معلّقة، تُفتح عبر أبواب منزلقة على شرفة المسبح',
  'Computergegenereerde ruimte van de sociale club met houten tafels, rotanstoelen en hanglampen, die via schuifdeuren uitkomt op het zwembadterras',
  'Wygenerowana komputerowo sala klubu z drewnianymi stołami, rattanowymi krzesłami i lampami wiszącymi, otwierająca się przesuwnymi drzwiami na taras przy basenie',
  'Datagenerert rom i den sosiale klubben med trebord, rottingstoler og taklamper, som åpner seg med skyvedører mot bassengterrassen',
  'Datorgenererad lokal i klubben med trabord, rottingstolar och hänglampor, som öppnar sig med skjutdörrar mot poolterrassen')
a('.media.items[5].alt',
  'Salón-comedor generado por ordenador, con un sofá y una mesa de comedor redonda, que se abre con una puerta corredera de cristal a un jardín',
  'Séjour-salle à manger généré par ordinateur, avec un canapé et une table à manger ronde, ouvrant par une porte vitrée coulissante sur un jardin',
  'Computergenerierter Wohn- und Essbereich mit Sofa und rundem Esstisch, der sich über eine gläserne Schiebetür zu einem Garten öffnet',
  'Компьютерная визуализация гостиной-столовой с диваном и круглым обеденным столом; стеклянная раздвижная дверь ведёт в сад',
  'غرفة معيشة وطعام مولَّدة بالحاسوب بأريكة وطاولة طعام مستديرة، تُفتح عبر باب زجاجي منزلق على حديقة',
  'Computergegenereerde woon- en eetkamer met een bank en een ronde eettafel, die via een glazen schuifdeur uitkomt op een tuin',
  'Wygenerowany komputerowo salon z jadalnią z sofą i okrągłym stołem, otwierający się przesuwnymi szklanymi drzwiami na ogród',
  'Datagenerert stue og spisestue med sofa og rundt spisebord, som åpner seg med en skyvedør i glass mot en hage',
  'Datorgenererat vardagsrum och matplats med soffa och runt matbord, som öppnar sig med en skjutdörr i glas mot en trädgård')
a('.media.items[7].alt',
  'Dormitorio generado por ordenador con una cama doble frente a una pared de cabecero revestida de paneles, un sillón y una ventana',
  'Chambre générée par ordinateur avec un lit double contre un mur de tête de lit habillé de panneaux, un fauteuil et une fenêtre',
  'Computergeneriertes Schlafzimmer mit Doppelbett vor einer paneelierten Kopfteilwand, einem Sessel und einem Fenster',
  'Компьютерная визуализация спальни с двуспальной кроватью у стены с панелями за изголовьем, креслом и окном',
  'غرفة نوم مولَّدة بالحاسوب بسرير مزدوج أمام جدار مكسو بألواح خلف رأس السرير ومقعد ونافذة',
  'Computergegenereerde slaapkamer met een tweepersoonsbed tegen een gepaneelde hoofdeindwand, een fauteuil en een raam',
  'Wygenerowana komputerowo sypialnia z łóżkiem dwuosobowym przy ścianie z panelami za wezgłowiem, fotelem i oknem',
  'Datagenerert soverom med dobbeltseng mot en panelt hodegavlvegg, en lenestol og et vindu',
  'Datorgenererat sovrum med dubbelsäng mot en panelklädd sänggavelvägg, en fåtölj och ett fönster')
a('.media.items[8].alt',
  'Baño generado por ordenador con ducha a ras de suelo, un lavabo sobre encimera en una repisa suspendida y un espejo',
  'Salle de bains générée par ordinateur avec douche à l’italienne, une vasque posée sur une tablette suspendue et un miroir',
  'Computergeneriertes Badezimmer mit bodengleicher Dusche, einem Aufsatzwaschbecken auf einer Wandablage und einem Spiegel',
  'Компьютерная визуализация ванной комнаты с душевой без поддона, накладной раковиной на подвесной полке и зеркалом',
  'حمام مولَّد بالحاسوب بدشّ مفتوح بمستوى الأرضية وحوض موضوع على رف معلّق ومرآة',
  'Computergegenereerde badkamer met een inloopdouche, een opzetwastafel op een zwevende plank en een spiegel',
  'Wygenerowana komputerowo łazienka z prysznicem bez brodzika, umywalką nablatową na wiszącej półce i lustrem',
  'Datagenerert bad med flush dusj, en opplagt vask på en veggmontert hylle og et speil',
  'Datorgenererat badrum med inbyggd dusch, ett ovanpåliggande handfat på en väggmonterad hylla och en spegel')
for path, n in (('[9]', '31'), ('[10]', '39'), ('[11]', '10')):
    a(f'.media.items{path}.alt', f'Plano del adosado {n}', f'Plan de la maison mitoyenne {n}', f'Grundriss des Reihenhauses {n}',
      f'Планировка таунхауса {n}', f'مخطط المنزل المتلاصق {n}', f'Plattegrond van rijwoning {n}', f'Rzut domu szeregowego {n}',
      f'Plantegning av rekkehus {n}', f'Planritning för radhus {n}')
    a(f'.media.items{path}.caption', f'Adosado {n}', f'Maison mitoyenne {n}', f'Reihenhaus {n}', f'Таунхаус {n}',
      f'منزل متلاصق {n}', f'Rijwoning {n}', f'Dom szeregowy {n}', f'Rekkehus {n}', f'Radhus {n}')

# ---- overview, residences -----------------------------------------------------------------------

a('.overview.headlineHtml',
  '140 adosados, <em>tres de ellos en la lista</em>', '140 maisons mitoyennes, <em>trois sur la liste</em>',
  '140 Reihenhäuser, <em>drei derzeit gelistet</em>', '140 таунхаусов, <em>три сейчас в прайс-листе</em>',
  '140 منزلاً متلاصقاً، <em>ثلاثة منها مدرجة حالياً</em>', '140 rijwoningen, <em>drie momenteel op de lijst</em>',
  '140 domów szeregowych, <em>trzy obecnie w cenniku</em>', '140 rekkehus, <em>tre oppført nå</em>',
  '140 radhus, <em>tre upptagna just nu</em>')
a('.overview.copy[0]',
  'Una urbanización de 140 adosados de tres o cuatro dormitorios en Mijas Costa, frente a un espacio natural de frondosos pinos. El dosier la presenta como un complejo de estilo resort con piscinas comunitarias, gimnasio, club social y zona chill-out, y las hojas de pago muestran dos fases.',
  'Une résidence de 140 maisons mitoyennes de trois ou quatre chambres à Mijas Costa, face à un espace naturel de pins denses. Le dossier la présente comme une résidence de style resort avec piscines communes, salle de sport, club social et espace chill-out, et les fiches de paiement montrent deux phases.',
  'Eine Anlage mit 140 Reihenhäusern mit drei oder vier Schlafzimmern in Mijas Costa, gegenüber einem Naturraum mit dichtem Kiefernbestand. Das Dossier stellt sie als Anlage im Resort-Stil mit Gemeinschaftspools, Fitnessraum, Clubraum und Chill-out-Bereich vor, und die Zahlungspläne zeigen zwei Phasen.',
  'Комплекс из 140 таунхаусов с тремя или четырьмя спальнями в Михас-Коста, напротив природной зоны с густым сосновым лесом. Досье представляет его как комплекс в стиле курорта с общими бассейнами, тренажёрным залом, клубом и зоной отдыха, а графики платежей показывают два этапа.',
  'مجمع من 140 منزلاً متلاصقاً بثلاث أو أربع غرف نوم في ميخاس كوستا، مقابل مساحة طبيعية كثيفة بأشجار الصنوبر. يقدّمه الملف التعريفي كمجمع بأسلوب المنتجعات يضم مسابح مشتركة وصالة رياضية ونادياً اجتماعياً ومنطقة استرخاء، وتُظهر جداول الدفع مرحلتين.',
  'Een complex van 140 rijwoningen met drie of vier slaapkamers in Mijas Costa, tegenover een natuurgebied met dichte dennen. Het dossier presenteert het als een complex in resortstijl met gemeenschappelijke zwembaden, een fitnessruimte, een sociale club en een chill-outzone, en de betalingsschema’s tonen twee fasen.',
  'Osiedle 140 domów szeregowych z trzema lub czterema sypialniami w Mijas Costa, naprzeciw terenu naturalnego z gęstym sosnowym lasem. Broszura przedstawia je jako osiedle w stylu kurortu ze wspólnymi basenami, siłownią, klubem i strefą chill-out, a harmonogramy płatności pokazują dwa etapy.',
  'Et område med 140 rekkehus med tre eller fire soverom i Mijas Costa, vendt mot et naturområde med tett furuskog. Brosjyren presenterer det som et område i resortstil med felles basseng, treningsrom, sosial klubb og chill-out-sone, og betalingsplanene viser to faser.',
  'Ett område med 140 radhus med tre eller fyra sovrum i Mijas Costa, vända mot ett naturområde med tät tallskog. Broschyren presenterar det som ett område i resortstil med gemensamma pooler, gym, klubblokal och chill-out-yta, och betalningsplanerna visar två faser.')
a('.overview.copy[1]',
  'La lista de precios de la fase 1 recoge tres viviendas, todas de tres dormitorios y con jardín privado: dos a {E495000} y una a {E505000}, más IVA. No cubre la fase 2 ni las demás viviendas de la fase 1, y los documentos no indican cuántas viviendas tiene cada fase.',
  'La liste de prix de la phase 1 recense trois logements, tous de trois chambres et avec jardin privatif : deux à {E495000} et un à {E505000}, hors TVA. Elle ne couvre ni la phase 2 ni les autres logements de la phase 1, et les documents n’indiquent pas combien de logements compte chaque phase.',
  'Die Preisliste der Phase 1 nennt drei Häuser, alle mit drei Schlafzimmern und Privatgarten: zwei zu {E495000} und eines zu {E505000}, jeweils zuzüglich MwSt. Sie deckt weder Phase 2 noch die übrigen Häuser der Phase 1 ab, und die Unterlagen sagen nicht, wie viele Häuser jede Phase hat.',
  'В прайс-листе первой фазы указаны три дома, все с тремя спальнями и собственным садом: два по {E495000} и один за {E505000}, без НДС. Он не охватывает ни вторую фазу, ни остальные дома первой, а документы не сообщают, сколько домов в каждой фазе.',
  'تذكر قائمة أسعار المرحلة الأولى ثلاثة مساكن، جميعها بثلاث غرف نوم وحديقة خاصة: اثنان بسعر {E495000} وواحد بسعر {E505000}، دون ضريبة القيمة المضافة. ولا تشمل المرحلة الثانية ولا بقية مساكن المرحلة الأولى، ولا تذكر الوثائق عدد المساكن في كل مرحلة.',
  'De prijslijst van fase 1 noemt drie woningen, alle met drie slaapkamers en een privétuin: twee van {E495000} en één van {E505000}, excl. btw. Ze omvat fase 2 en de overige woningen van fase 1 niet, en de documenten vermelden niet hoeveel woningen elke fase heeft.',
  'Cennik etapu 1 wymienia trzy domy, wszystkie z trzema sypialniami i prywatnym ogrodem: dwa po {E495000} i jeden za {E505000}, plus VAT. Nie obejmuje etapu 2 ani pozostałych domów etapu 1, a dokumenty nie podają, ile domów liczy każdy etap.',
  'Prislisten for fase 1 nevner tre boliger, alle med tre soverom og egen hage: to til {E495000} og én til {E505000}, pluss mva. Den dekker verken fase 2 eller de øvrige boligene i fase 1, og dokumentene oppgir ikke hvor mange boliger hver fase har.',
  'Prislistan för fas 1 nämner tre bostäder, alla med tre sovrum och egen trädgård: två för {E495000} och en för {E505000}, plus IVA. Den omfattar varken fas 2 eller de övriga bostäderna i fas 1, och handlingarna anger inte hur många bostäder varje fas har.')
a('.overview.metrics[0][1]', '140 adosados', '140 maisons mitoyennes', '140 Reihenhäuser', '140 таунхаусов', '140 منزلاً متلاصقاً',
  '140 rijwoningen', '140 domów szeregowych', '140 rekkehus', '140 radhus')
a('.overview.metrics[3][1]', '{E495000} - {E505000} + IVA', '{E495000} - {E505000} + TVA', '{E495000} - {E505000} + MwSt.',
  '{E495000} - {E505000} + НДС', '{E495000} - {E505000} + ضريبة القيمة المضافة', '{E495000} - {E505000} + btw',
  '{E495000} - {E505000} + VAT', '{E495000} - {E505000} + mva', '{E495000} - {E505000} + IVA')
a('.residences.headlineHtml', 'Tres viviendas, <em>un solo tipo de casa</em>', 'Trois logements, <em>un seul type de maison</em>',
  'Drei Häuser, <em>ein Haustyp</em>', 'Три дома, <em>один тип дома</em>', 'ثلاثة مساكن، <em>طراز واحد للمنزل</em>',
  'Drie woningen, <em>één woningtype</em>', 'Trzy domy, <em>jeden typ domu</em>', 'Tre boliger, <em>én boligtype</em>',
  'Tre bostäder, <em>en bostadstyp</em>')
a('.residences.copy',
  'Las tres viviendas de la lista de precios comparten una misma distribución en dos plantas, con tres dormitorios y jardín privado, y se diferencian en la posición, la orientación y el tamaño del jardín.',
  'Les trois logements de la liste de prix partagent une même distribution sur deux niveaux, avec trois chambres et un jardin privatif, et diffèrent par leur emplacement, leur orientation et la taille du jardin.',
  'Die drei Häuser der Preisliste teilen sich einen Grundriss über zwei Geschosse mit drei Schlafzimmern und Privatgarten und unterscheiden sich in Lage, Ausrichtung und Gartengröße.',
  'Три дома из прайс-листа имеют одну планировку на двух этажах с тремя спальнями и собственным садом и различаются расположением, ориентацией и размером сада.',
  'تشترك المساكن الثلاثة في قائمة الأسعار في تصميم واحد على طابقين بثلاث غرف نوم وحديقة خاصة، وتختلف في الموقع والاتجاه ومساحة الحديقة.',
  'De drie woningen op de prijslijst delen één indeling over twee verdiepingen, met drie slaapkamers en een privétuin, en verschillen in ligging, oriëntatie en tuingrootte.',
  'Trzy domy z cennika mają ten sam układ na dwóch kondygnacjach, z trzema sypialniami i prywatnym ogrodem, i różnią się położeniem, orientacją oraz wielkością ogrodu.',
  'De tre boligene på prislisten deler én planløsning over to etasjer, med tre soverom og egen hage, og skiller seg i beliggenhet, orientering og hagestørrelse.',
  'De tre bostäderna i prislistan delar en planlösning över två våningar, med tre sovrum och egen trädgård, och skiljer sig i läge, väderstreck och trädgårdens storlek.')
a('.residences.items[0].name', 'El adosado de tres dormitorios', 'La maison mitoyenne de trois chambres', 'Das Reihenhaus mit drei Schlafzimmern',
  'Таунхаус с тремя спальнями', 'المنزل المتلاصق بثلاث غرف نوم', 'De rijwoning met drie slaapkamers', 'Dom szeregowy z trzema sypialniami',
  'Rekkehuset med tre soverom', 'Radhuset med tre sovrum')
a('.residences.items[0].points[0]',
  'El salón, la cocina, el vestíbulo y un aseo en la planta baja; tres dormitorios, dos baños y un vestidor en la primera.',
  'Le séjour, la cuisine, l’entrée et des toilettes au rez-de-chaussée ; trois chambres, deux salles de bains et un dressing à l’étage.',
  'Wohnzimmer, Küche, Diele und ein Gäste-WC im Erdgeschoss; drei Schlafzimmer, zwei Bäder und ein Ankleidezimmer im Obergeschoss.',
  'Гостиная, кухня, холл и туалет на первом этаже; три спальни, две ванные комнаты и гардеробная на втором.',
  'غرفة المعيشة والمطبخ والمدخل ودورة مياه في الطابق الأرضي؛ وثلاث غرف نوم وحمامان وغرفة ملابس في الطابق الأول.',
  'De woonkamer, keuken, hal en een toilet op de begane grond; drie slaapkamers, twee badkamers en een inloopkast op de eerste verdieping.',
  'Salon, kuchnia, przedpokój i toaleta na parterze; trzy sypialnie, dwie łazienki i garderoba na piętrze.',
  'Stue, kjøkken, entré og et toalett i første etasje; tre soverom, to bad og en garderobe i andre etasje.',
  'Vardagsrum, kök, hall och en toalett på bottenplanet; tre sovrum, två badrum och ett klädrum på övervåningen.')
a('.residences.items[0].points[1]',
  '{N100.37} {U} de superficie interior, {N53.05} {U} en la planta baja y {N47.32} {U} en la primera, y {N124.05} o {N124.08} {U} construidos.',
  '{N100.37} {U} de surface intérieure, {N53.05} {U} au rez-de-chaussée et {N47.32} {U} à l’étage, et {N124.05} ou {N124.08} {U} construits.',
  '{N100.37} {U} Wohnfläche innen, davon {N53.05} {U} im Erdgeschoss und {N47.32} {U} im Obergeschoss, und {N124.05} oder {N124.08} {U} bebaut.',
  '{N100.37} {U} внутренней площади: {N53.05} {U} на первом этаже и {N47.32} {U} на втором; застроенная площадь {N124.05} или {N124.08} {U}.',
  '{N100.37} {U} مساحة داخلية، منها {N53.05} {U} في الطابق الأرضي و{N47.32} {U} في الطابق الأول، و{N124.05} أو {N124.08} {U} مساحة مبنية.',
  '{N100.37} {U} binnenoppervlak, waarvan {N53.05} {U} op de begane grond en {N47.32} {U} op de eerste verdieping, en {N124.05} of {N124.08} {U} bebouwd.',
  '{N100.37} {U} powierzchni wewnętrznej, w tym {N53.05} {U} na parterze i {N47.32} {U} na piętrze, oraz {N124.05} lub {N124.08} {U} powierzchni zabudowy.',
  '{N100.37} {U} innvendig areal, {N53.05} {U} i første etasje og {N47.32} {U} i andre, og {N124.05} eller {N124.08} {U} bebygd.',
  '{N100.37} {U} inomhusyta, {N53.05} {U} på bottenplanet och {N47.32} {U} på övervåningen, och {N124.05} eller {N124.08} {U} byggd yta.')
a('.residences.items[0].points[2]',
  'Una terraza descubierta de {N9.15} o {N11.55} {U} y un jardín privado, y una plaza de aparcamiento frontal de unos {N26} {U} dibujada en la parcela.',
  'Une terrasse découverte de {N9.15} ou {N11.55} {U} et un jardin privatif, et une place de stationnement frontale d’environ {N26} {U} dessinée sur la parcelle.',
  'Eine unüberdachte Terrasse von {N9.15} oder {N11.55} {U} und ein Privatgarten sowie ein frontaler Stellplatz von etwa {N26} {U}, der auf dem Grundstück eingezeichnet ist.',
  'Открытая терраса {N9.15} или {N11.55} {U} и собственный сад, а также фронтальное парковочное место около {N26} {U}, нарисованное на участке.',
  'شرفة مكشوفة مساحتها {N9.15} أو {N11.55} {U} وحديقة خاصة، ومكان لوقوف السيارة في المقدمة بنحو {N26} {U} مرسوم على القطعة.',
  'Een onoverdekt terras van {N9.15} of {N11.55} {U} en een privétuin, en een parkeerplaats aan de voorzijde van ongeveer {N26} {U} die op het perceel is getekend.',
  'Odkryty taras o powierzchni {N9.15} lub {N11.55} {U} i prywatny ogród oraz miejsce parkingowe z przodu o powierzchni około {N26} {U}, narysowane na działce.',
  'En åpen terrasse på {N9.15} eller {N11.55} {U} og egen hage, og en parkeringsplass foran på omtrent {N26} {U} tegnet inn på tomten.',
  'En öppen terrass på {N9.15} eller {N11.55} {U} och en egen trädgård, och en parkeringsplats framför på cirka {N26} {U} som är ritad på tomten.')
a('.residences.items[1].name', 'Lo que distingue a las tres', 'Ce qui distingue les trois', 'Was die drei unterscheidet',
  'Чем различаются три дома', 'ما يميّز المساكن الثلاثة', 'Wat de drie onderscheidt', 'Czym różnią się te trzy', 'Hva som skiller de tre', 'Vad som skiljer de tre åt')
a('.residences.items[1].points[0]',
  'El adosado 31, en el bloque 3, está orientado al nordeste y tiene un jardín de {N21.34} {U}, por {E495000} + IVA.',
  'La maison mitoyenne 31, dans le bloc 3, est orientée nord-est et a un jardin de {N21.34} {U}, pour {E495000} + TVA.',
  'Reihenhaus 31 im Block 3 ist nach Nordosten ausgerichtet und hat einen Garten von {N21.34} {U}, für {E495000} + MwSt.',
  'Таунхаус 31 в блоке 3 ориентирован на северо-восток, сад {N21.34} {U}, цена {E495000} + НДС.',
  'المنزل المتلاصق 31 في المبنى 3 متجه نحو الشمال الشرقي وله حديقة بمساحة {N21.34} {U}، بسعر {E495000} + ضريبة القيمة المضافة.',
  'Rijwoning 31 in blok 3 ligt op het noordoosten en heeft een tuin van {N21.34} {U}, voor {E495000} + btw.',
  'Dom szeregowy 31 w bloku 3 jest zwrócony na północny wschód i ma ogród o powierzchni {N21.34} {U}, za {E495000} + VAT.',
  'Rekkehus 31 i blokk 3 vender mot nordøst og har en hage på {N21.34} {U}, til {E495000} + mva.',
  'Radhus 31 i kvarter 3 vetter mot nordost och har en trädgård på {N21.34} {U}, för {E495000} + IVA.')
a('.residences.items[1].points[1]',
  'El adosado 39, en el bloque 4, está orientado al nordeste y tiene un jardín de {N29.51} {U}, por {E495000} + IVA.',
  'La maison mitoyenne 39, dans le bloc 4, est orientée nord-est et a un jardin de {N29.51} {U}, pour {E495000} + TVA.',
  'Reihenhaus 39 im Block 4 ist nach Nordosten ausgerichtet und hat einen Garten von {N29.51} {U}, für {E495000} + MwSt.',
  'Таунхаус 39 в блоке 4 ориентирован на северо-восток, сад {N29.51} {U}, цена {E495000} + НДС.',
  'المنزل المتلاصق 39 في المبنى 4 متجه نحو الشمال الشرقي وله حديقة بمساحة {N29.51} {U}، بسعر {E495000} + ضريبة القيمة المضافة.',
  'Rijwoning 39 in blok 4 ligt op het noordoosten en heeft een tuin van {N29.51} {U}, voor {E495000} + btw.',
  'Dom szeregowy 39 w bloku 4 jest zwrócony na północny wschód i ma ogród o powierzchni {N29.51} {U}, za {E495000} + VAT.',
  'Rekkehus 39 i blokk 4 vender mot nordøst og har en hage på {N29.51} {U}, til {E495000} + mva.',
  'Radhus 39 i kvarter 4 vetter mot nordost och har en trädgård på {N29.51} {U}, för {E495000} + IVA.')
a('.residences.items[1].points[2]',
  'El adosado 10, en el bloque 1, está orientado al suroeste y tiene un jardín de {N15.86} {U}, por {E505000} + IVA.',
  'La maison mitoyenne 10, dans le bloc 1, est orientée sud-ouest et a un jardin de {N15.86} {U}, pour {E505000} + TVA.',
  'Reihenhaus 10 im Block 1 ist nach Südwesten ausgerichtet und hat einen Garten von {N15.86} {U}, für {E505000} + MwSt.',
  'Таунхаус 10 в блоке 1 ориентирован на юго-запад, сад {N15.86} {U}, цена {E505000} + НДС.',
  'المنزل المتلاصق 10 في المبنى 1 متجه نحو الجنوب الغربي وله حديقة بمساحة {N15.86} {U}، بسعر {E505000} + ضريبة القيمة المضافة.',
  'Rijwoning 10 in blok 1 ligt op het zuidwesten en heeft een tuin van {N15.86} {U}, voor {E505000} + btw.',
  'Dom szeregowy 10 w bloku 1 jest zwrócony na południowy zachód i ma ogród o powierzchni {N15.86} {U}, za {E505000} + VAT.',
  'Rekkehus 10 i blokk 1 vender mot sørvest og har en hage på {N15.86} {U}, til {E505000} + mva.',
  'Radhus 10 i kvarter 1 vetter mot sydväst och har en trädgård på {N15.86} {U}, för {E505000} + IVA.')

# ---- quality specification ---------------------------------------------------------------------

a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor en inglés, con fecha 6 de febrero de 2026 (revisión 02). Indica que la dirección facultativa puede cambiar los materiales por otros de calidad similar o superior, y que la piedra natural y la madera varían de tono y color.',
  'Source : le descriptif de qualité du promoteur en anglais, daté du 6 février 2026 (révision 02). Il indique que la direction de projet peut modifier les matériaux et les remplacer par d’autres de qualité similaire ou supérieure, et que la pierre naturelle et le bois varient de teinte et de couleur.',
  'Quelle: die Bau- und Ausstattungsbeschreibung des Bauträgers auf Englisch vom 6. Februar 2026 (Revision 02). Sie besagt, dass die Materialien nach Ermessen der Projektleitung geändert und durch gleich- oder höherwertige ersetzt werden können und dass Naturstein und Holz in Ton und Farbe variieren.',
  'Источник: описание качества отделки от застройщика на английском языке от 6 февраля 2026 года (редакция 02). В нём сказано, что материалы могут быть изменены по решению руководства проекта и заменены другими, не уступающими по качеству, а натуральный камень и дерево различаются по оттенку и цвету.',
  'المصدر: مواصفات الجودة الصادرة عن المطوّر بالإنجليزية بتاريخ 6 فبراير 2026 (المراجعة 02). تنص على أنه يجوز تغيير المواد بتقدير إدارة المشروع واستبدالها بأخرى مماثلة أو أعلى جودة، وأن الحجر الطبيعي والخشب يتفاوتان في الدرجة واللون.',
  'Bron: de kwaliteitsbeschrijving van de ontwikkelaar in het Engels, gedateerd 6 februari 2026 (revisie 02). Daarin staat dat de materialen naar goeddunken van de projectleiding mogen worden gewijzigd en vervangen door andere van gelijke of hogere kwaliteit, en dat natuursteen en hout in tint en kleur verschillen.',
  'Źródło: opis jakości dewelopera w języku angielskim z 6 lutego 2026 r. (rewizja 02). Zastrzega on, że materiały mogą zostać zmienione według uznania kierownictwa projektu i zastąpione innymi o podobnej lub wyższej jakości oraz że kamień naturalny i drewno różnią się odcieniem i kolorem.',
  'Kilde: utbyggerens kvalitetsbeskrivelse på engelsk, datert 6. februar 2026 (revisjon 02). Den sier at materialene kan endres etter prosjektledelsens skjønn og erstattes med andre av lignende eller høyere kvalitet, og at naturstein og tre varierer i nyanse og farge.',
  'Källa: exploatörens kvalitetsbeskrivning på engelska, daterad 6 februari 2026 (revision 02). Den anger att materialen kan ändras efter projektledningens bedömning och ersättas med andra av liknande eller högre kvalitet, och att natursten och trä varierar i nyans och färg.')
a('.qualitySpecs.groups[0].items[0]',
  'Cimentación de hormigón armado, según exige el estudio geotécnico, y estructura de hormigón armado.',
  'Fondations en béton armé, comme l’exige l’étude géotechnique, et structure en béton armé.',
  'Fundament aus Stahlbeton, wie es das Bodengutachten verlangt, und Stahlbetontragwerk.',
  'Железобетонный фундамент, как требует геотехническое заключение, и железобетонный каркас.',
  'أساسات من الخرسانة المسلحة كما تتطلب الدراسة الجيوتقنية، وهيكل من الخرسانة المسلحة.',
  'Een fundering van gewapend beton, zoals het geotechnisch onderzoek vereist, en een constructie van gewapend beton.',
  'Fundament żelbetowy, zgodnie z wymogami badania geotechnicznego, i konstrukcja żelbetowa.',
  'Fundament i armert betong, slik den geotekniske undersøkelsen krever, og en konstruksjon i armert betong.',
  'En grund av armerad betong, som markundersökningen kräver, och en stomme av armerad betong.')
a('.qualitySpecs.groups[0].items[1]',
  'Fachada de ladrillo perforado con aislamiento de poliuretano proyectado o XPS, cámara de aire y trasdosado de placa de yeso laminado sobre una estructura de acero galvanizado con aislamiento de lana mineral.',
  'Façade en brique perforée avec isolation en polyuréthane projeté ou en XPS, lame d’air et doublage en plaques de plâtre sur ossature en acier galvanisé avec isolation en laine minérale.',
  'Fassade aus Lochziegeln mit aufgespritzter Polyurethan- oder XPS-Dämmung, Luftschicht und Gipskartonvorsatzschale auf einer verzinkten Stahlunterkonstruktion mit Mineralwolldämmung.',
  'Фасад из перфорированного кирпича с напылённым полиуретановым или XPS-утеплителем, воздушным зазором и гипсокартонной облицовкой на оцинкованном стальном каркасе с минераловатным утеплителем.',
  'واجهة من الطوب المثقب مع عزل من البولي يوريثان المرشوش أو XPS وفراغ هوائي وبطانة من ألواح الجبس على هيكل من الفولاذ المجلفن مع عزل بالصوف المعدني.',
  'Een gevel van geperforeerde baksteen met gespoten polyurethaan- of XPS-isolatie, een luchtspouw en een gipsplaatbekleding op een verzinkt stalen frame met minerale wol als isolatie.',
  'Elewacja z cegły dziurawki z natryskową izolacją poliuretanową lub XPS, pustką powietrzną i okładziną z płyt gipsowo-kartonowych na ocynkowanym stalowym szkielecie z izolacją z wełny mineralnej.',
  'Fasade av hullmur med sprøytet polyuretan- eller XPS-isolasjon, luftspalte og gipsplatekledning på en forsinket stålramme med mineralullisolasjon.',
  'Fasad av håltegel med sprutad polyuretan- eller XPS-isolering, luftspalt och gipsskivor på ett galvaniserat stålstomme med mineralullsisolering.')
a('.qualitySpecs.groups[0].items[2]',
  'Cubierta invertida no transitable, impermeabilizada y aislada.',
  'Toiture inversée non accessible, étanchée et isolée.',
  'Ein nicht begehbares Umkehrdach, abgedichtet und gedämmt.',
  'Неэксплуатируемая инверсионная кровля с гидроизоляцией и утеплением.',
  'سقف مقلوب غير قابل للسير عليه، معزول مائياً وحرارياً.',
  'Een niet-begaanbaar omgekeerd dak, waterdicht en geïsoleerd.',
  'Niedostępny dach odwrócony, uszczelniony i ocieplony.',
  'Et ikke-gangbart omvendt tak, tettet og isolert.',
  'Ett icke gångbart omvänt tak, tätat och isolerat.')
a('.qualitySpecs.groups[1].items[0]',
  'Suelo laminado en el salón, los dormitorios, la cocina, los pasillos y el vestíbulo, con rodapié blanco.',
  'Sol stratifié dans le séjour, les chambres, la cuisine, les couloirs et l’entrée, avec plinthes blanches.',
  'Laminatboden in Wohnzimmer, Schlafzimmern, Küche, Fluren und Diele mit weißen Sockelleisten.',
  'Ламинат в гостиной, спальнях, кухне, коридорах и холле, белые плинтусы.',
  'أرضية من اللامينيت في غرفة المعيشة وغرف النوم والمطبخ والممرات والمدخل، مع وزرات بيضاء.',
  'Laminaatvloer in de woonkamer, slaapkamers, keuken, gangen en hal, met witte plinten.',
  'Podłoga laminowana w salonie, sypialniach, kuchni, korytarzach i przedpokoju, z białymi listwami przypodłogowymi.',
  'Laminatgulv i stue, soverom, kjøkken, ganger og entré, med hvite gulvlister.',
  'Laminatgolv i vardagsrum, sovrum, kök, korridorer och hall, med vita golvlister.')
a('.qualitySpecs.groups[1].items[1]',
  'Baldosas cerámicas en el suelo de los baños, en la escalera y en las paredes de las duchas, y pintura plástica en el resto de paredes y en los techos de placa de yeso laminado.',
  'Carrelage céramique au sol des salles de bains, dans l’escalier et sur les murs des douches, et peinture plastique sur les autres murs et sur les plafonds en plaques de plâtre.',
  'Keramikfliesen auf den Badezimmerböden, auf der Treppe und an den Duschwänden sowie Kunststoffdispersionsfarbe an den übrigen Wänden und den Gipskartondecken.',
  'Керамическая плитка на полу ванных комнат, на лестнице и на стенах душевых, на остальных стенах и гипсокартонных потолках — пластиковая краска.',
  'بلاط خزفي على أرضيات الحمامات وفي الدرج وعلى جدران الدشّ، ودهان بلاستيكي على بقية الجدران وأسقف ألواح الجبس.',
  'Keramische tegels op de badkamervloeren, op de trap en op de douchewanden, en kunststofverf op de overige wanden en de gipsplaatplafonds.',
  'Płytki ceramiczne na podłogach łazienek, na schodach i na ścianach pryszniców oraz farba plastyczna na pozostałych ścianach i sufitach z płyt gipsowo-kartonowych.',
  'Keramiske fliser på baderomsgulvene, i trappen og på dusjveggene, og plastmaling på de øvrige veggene og gipstakene.',
  'Keramiska plattor på badrumsgolven, i trappan och på duschväggarna, och plastfärg på övriga väggar och gipstak.')
a('.qualitySpecs.groups[1].items[2]',
  'Baldosas antideslizantes de exterior en los patios.',
  'Carrelage extérieur antidérapant sur les patios.',
  'Rutschhemmende Außenfliesen auf den Terrassen.',
  'Противоскользящая уличная плитка на патио.',
  'بلاط خارجي مانع للانزلاق في الباحات.',
  'Antislip buitentegels op de patio’s.',
  'Antypoślizgowe płytki zewnętrzne na patiach.',
  'Sklisikre utendørsfliser på uteplassene.',
  'Halkfria utomhusplattor på uteplatserna.')
a('.qualitySpecs.groups[2].name', 'Puertas, ventanas y seguridad', 'Portes, fenêtres et sécurité', 'Türen, Fenster und Sicherheit',
  'Двери, окна и безопасность', 'الأبواب والنوافذ والأمان', 'Deuren, ramen en veiligheid', 'Drzwi, okna i bezpieczeństwo',
  'Dører, vinduer og sikkerhet', 'Dörrar, fönster och säkerhet')
a('.qualitySpecs.groups[2].items[0]',
  'Ventanas de PVC con doble acristalamiento, abatibles, correderas u oscilobatientes, vidrio laminado de seguridad en las puertas de los patios y persianas aislantes de accionamiento manual en los dormitorios.',
  'Fenêtres en PVC à double vitrage, battantes, coulissantes ou oscillo-battantes, verre feuilleté de sécurité aux portes des patios et volets roulants isolants à commande manuelle dans les chambres.',
  'PVC-Fenster mit Doppelverglasung als Dreh-, Schiebe- oder Dreh-Kipp-Fenster, Verbundsicherheitsglas in den Terrassentüren und manuell bediente, gedämmte Rollläden in den Schlafzimmern.',
  'Окна из ПВХ с двойным остеклением — распашные, раздвижные или поворотно-откидные, закалённое ламинированное стекло в дверях на патио и теплоизолированные рольставни с ручным приводом в спальнях.',
  'نوافذ من PVC بزجاج مزدوج، مفصلية أو منزلقة أو قابلة للإمالة والفتح، وزجاج أمان مصفّح في أبواب الباحات، وستائر أسطوانية معزولة تُدار يدوياً في غرف النوم.',
  'PVC-ramen met dubbele beglazing, draaiend, schuivend of draai-kiepend, gelaagd veiligheidsglas in de patiodeuren en handbediende, geïsoleerde rolluiken in de slaapkamers.',
  'Okna z PVC z podwójnym szkleniem, uchylne, przesuwne lub rozwierano-uchylne, bezpieczne szkło laminowane w drzwiach na patio oraz ręcznie obsługiwane izolowane rolety w sypialniach.',
  'PVC-vinduer med dobbeltglass, sidehengslede, skyvbare eller vippe-/dreievinduer, laminert sikkerhetsglass i uteplassdørene og manuelt betjente, isolerte rullegardiner på soverommene.',
  'PVC-fönster med dubbelglas, sidohängda, skjutbara eller vridbara, laminerat säkerhetsglas i uteplatsdörrarna och manuellt manövrerade, isolerade rullgardiner i sovrummen.')
a('.qualitySpecs.groups[2].items[1]',
  'Puertas interiores lacadas en blanco y armarios modulares con balda y barra de colgar.',
  'Portes intérieures laquées blanc et placards modulaires avec étagère et tringle.',
  'Weiß lackierte Innentüren und modulare Kleiderschränke mit Ablage und Kleiderstange.',
  'Межкомнатные двери, окрашенные в белый, и модульные шкафы с полкой и штангой.',
  'أبواب داخلية مطلية بالأبيض وخزائن ملابس وحدوية برف وعمود تعليق.',
  'Wit gelakte binnendeuren en modulaire kasten met een plank en een kledingroede.',
  'Białe lakierowane drzwi wewnętrzne i modułowe szafy z półką i drążkiem.',
  'Hvitlakkerte innerdører og modulære garderobeskap med hylle og kleshenger.',
  'Vitlackerade innerdörrar och moduluppbyggda garderober med hylla och klädstång.')
a('.qualitySpecs.groups[2].items[2]',
  'Puerta de entrada de seguridad con mirilla y cerradura, y herrajes antipalanca y vidrio de seguridad en las ventanas y puertas de la planta baja.',
  'Porte d’entrée de sécurité avec judas et serrure, et ferrures anti-arrachement et verre de sécurité aux fenêtres et portes du rez-de-chaussée.',
  'Sicherheitshaustür mit Spion und Schloss sowie Aufhebelschutzbeschlägen und Sicherheitsglas an den Fenstern und Türen im Erdgeschoss.',
  'Входная дверь повышенной безопасности с глазком и замком, противовзломная фурнитура и защитное стекло на окнах и дверях первого этажа.',
  'باب مدخل أمني بعين سحرية وقفل، ومفصلات مقاومة للخلع وزجاج أمان في نوافذ وأبواب الطابق الأرضي.',
  'Een veiligheidsvoordeur met kijkgat en slot, en inbraakwerende beslagen en veiligheidsglas in de ramen en deuren op de begane grond.',
  'Drzwi wejściowe antywłamaniowe z wizjerem i zamkiem oraz okucia zabezpieczające przed wyważeniem i szkło bezpieczne w oknach i drzwiach na parterze.',
  'En sikkerhetsytterdør med dørspion og lås, og innbruddshindrende beslag og sikkerhetsglass i vinduer og dører i første etasje.',
  'En säkerhetsytterdörr med titthål och lås, och inbrottsskyddande beslag och säkerhetsglas i fönster och dörrar på bottenplanet.')
a('.qualitySpecs.groups[3].items[0]',
  'Muebles altos y bajos de laminado de alta presión, con encimera y fregadero Silestone.',
  'Meubles hauts et bas en stratifié haute pression, avec plan de travail et évier en Silestone.',
  'Hoch- und Unterschränke aus Hochdrucklaminat mit Arbeitsplatte und Spüle aus Silestone.',
  'Верхние и нижние шкафы из ламината высокого давления, столешница и мойка из Silestone.',
  'وحدات علوية وسفلية من اللامينيت عالي الضغط، مع سطح عمل وحوض من Silestone.',
  'Hoge en lage kasten van hogedruklaminaat, met een Silestone werkblad en spoelbak.',
  'Szafki górne i dolne z laminatu wysokociśnieniowego, z blatem i zlewozmywakiem z Silestone.',
  'Over- og underskap i høytrykkslaminat, med benkeplate og vask i Silestone.',
  'Över- och underskåp i högtryckslaminat, med bänkskiva och diskho i Silestone.')
a('.qualitySpecs.groups[3].items[1]',
  'Nevera, lavadora, lavavajillas, placa de inducción, horno, microondas y campana extractora.',
  'Réfrigérateur, lave-linge, lave-vaisselle, plaque à induction, four, micro-ondes et hotte aspirante.',
  'Kühlschrank, Waschmaschine, Geschirrspüler, Induktionskochfeld, Backofen, Mikrowelle und Dunstabzugshaube.',
  'Холодильник, стиральная машина, посудомоечная машина, индукционная варочная панель, духовой шкаф, микроволновая печь и вытяжка.',
  'ثلاجة وغسالة وغسالة صحون وموقد حثّي وفرن وميكروويف وشفاط.',
  'Koelkast, wasmachine, vaatwasser, inductiekookplaat, oven, magnetron en afzuigkap.',
  'Lodówka, pralka, zmywarka, płyta indukcyjna, piekarnik, kuchenka mikrofalowa i okap.',
  'Kjøleskap, vaskemaskin, oppvaskmaskin, induksjonstopp, ovn, mikrobølgeovn og kjøkkenvifte.',
  'Kylskåp, tvättmaskin, diskmaskin, induktionshäll, ugn, mikrovågsugn och köksfläkt.')
a('.qualitySpecs.groups[4].items[0]',
  'Aparatos sanitarios de porcelana vitrificada blanca, platos de ducha de resina en los dos baños y grifos monomando.',
  'Appareils sanitaires en porcelaine vitrifiée blanche, receveurs de douche en résine dans les deux salles de bains et robinets mitigeurs.',
  'Sanitärkeramik aus weißem Porzellan, Duschwannen aus Kunstharz in beiden Bädern und Einhebelarmaturen.',
  'Сантехника из белого глазурованного фарфора, душевые поддоны из смолы в обеих ванных комнатах и однорычажные смесители.',
  'أدوات صحية من البورسلين الأبيض المزجَّج، وأحواض دشّ من الراتنج في الحمامين، وخلاطات بذراع واحدة.',
  'Wit porseleinen sanitair, kunstharsdouchebakken in beide badkamers en eengreepskranen.',
  'Biała ceramika sanitarna z porcelany witryfikowanej, brodziki żywiczne w obu łazienkach i baterie jednouchwytowe.',
  'Hvitt sanitærporselen, dusjkar i harpiks på begge bad og énhåndsblandebatterier.',
  'Vit sanitetsporslin, duschkar av harts i båda badrummen och enhandsblandare.')
a('.qualitySpecs.groups[4].items[1]',
  'El lavabo va integrado en un mueble en el baño principal y suspendido en el segundo baño y en el aseo.',
  'La vasque est intégrée à un meuble dans la salle de bains principale et suspendue dans la seconde salle de bains et aux toilettes.',
  'Das Waschbecken ist im Hauptbad in einen Waschtisch eingebaut und im zweiten Bad sowie im Gäste-WC wandhängend.',
  'Раковина встроена в тумбу в главной ванной комнате и подвешена к стене во второй ванной и в туалете.',
  'الحوض مدمج في خزانة في الحمام الرئيسي ومعلّق على الجدار في الحمام الثاني ودورة المياه.',
  'De wastafel is in de hoofdbadkamer ingebouwd in een badkamermeubel en hangt aan de muur in de tweede badkamer en in het toilet.',
  'Umywalka jest wbudowana w szafkę w głównej łazience, a w drugiej łazience i w toalecie jest podwieszana.',
  'Vasken er bygget inn i en servantskap på hovedbadet og veggmontert på det andre badet og toalettet.',
  'Handfatet är infällt i ett underskåp i huvudbadrummet och väggmonterat i det andra badrummet och på toaletten.')
a('.qualitySpecs.groups[5].items[1]',
  'Aire frío y caliente por conductos en el salón, los dormitorios y la cocina, con solo la cocina atendida por bomba de calor, y ventilación mecánica en las cocinas y los baños.',
  'Air chaud et froid par gaines dans le séjour, les chambres et la cuisine, la seule cuisine étant desservie par une pompe à chaleur, et ventilation mécanique dans les cuisines et les salles de bains.',
  'Warme und kalte Luft über Kanäle in Wohnzimmer, Schlafzimmern und Küche, wobei nur die Küche über eine Wärmepumpe versorgt wird, und mechanische Lüftung in Küchen und Bädern.',
  'Тёплый и холодный воздух по воздуховодам в гостиную, спальни и кухню, причём только кухня обслуживается тепловым насосом, и механическая вентиляция на кухнях и в ванных комнатах.',
  'هواء ساخن وبارد عبر مجاري التهوية إلى غرفة المعيشة وغرف النوم والمطبخ، مع خدمة المطبخ وحده بمضخة حرارية، وتهوية ميكانيكية في المطابخ والحمامات.',
  'Warme en koude lucht via kanalen naar de woonkamer, slaapkamers en keuken, waarbij alleen de keuken door een warmtepomp wordt bediend, en mechanische ventilatie in de keukens en badkamers.',
  'Ciepłe i zimne powietrze kanałami do salonu, sypialni i kuchni, przy czym tylko kuchnię obsługuje pompa ciepła, oraz wentylacja mechaniczna w kuchniach i łazienkach.',
  'Varm og kald luft gjennom kanaler til stue, soverom og kjøkken, der bare kjøkkenet betjenes av en varmepumpe, og mekanisk ventilasjon på kjøkken og bad.',
  'Varm och kall luft genom kanaler till vardagsrum, sovrum och kök, där endast köket betjänas av en värmepump, och mekanisk ventilation i kök och badrum.')
a('.qualitySpecs.groups[5].items[2]',
  'Paneles fotovoltaicos en las cubiertas de las viviendas para autoconsumo, como exige el Código Técnico de la Edificación.',
  'Panneaux photovoltaïques sur les toits des logements pour l’autoconsommation, comme l’exige le Code technique du bâtiment espagnol.',
  'Photovoltaikmodule auf den Dächern der Häuser zum Eigenverbrauch, wie es der spanische Technische Baukodex verlangt.',
  'Фотоэлектрические панели на крышах домов для собственного потребления, как требует испанский Технический строительный кодекс.',
  'ألواح كهروضوئية على أسطح المساكن للاستهلاك الذاتي، كما تتطلب المدونة الفنية الإسبانية للبناء.',
  'Fotovoltaïsche panelen op de daken van de woningen voor eigen verbruik, zoals de Spaanse technische bouwcode vereist.',
  'Panele fotowoltaiczne na dachach domów na potrzeby własne, zgodnie z hiszpańskim Kodeksem Technicznym Budownictwa.',
  'Solcellepaneler på boligenes tak for eget forbruk, slik den spanske tekniske byggekoden krever.',
  'Solcellspaneler på bostädernas tak för egenanvändning, som den spanska tekniska byggkoden kräver.')
a('.qualitySpecs.groups[6].items[0]',
  'Conexiones de TV y ethernet según el estándar de telecomunicaciones ICT 2 en el salón, la cocina y los dormitorios, y un punto de carga para coche eléctrico preinstalado.',
  'Prises TV et ethernet selon la norme de télécommunications ICT 2 dans le séjour, la cuisine et les chambres, et une borne de recharge pour voiture électrique préinstallée.',
  'TV- und Ethernet-Anschlüsse nach dem Telekommunikationsstandard ICT 2 in Wohnzimmer, Küche und Schlafzimmern sowie ein vorinstallierter Ladepunkt für Elektroautos.',
  'Телевизионные и ethernet-розетки по стандарту связи ICT 2 в гостиной, кухне и спальнях и заранее подготовленная точка зарядки электромобиля.',
  'وصلات تلفزيون وإيثرنت وفق معيار الاتصالات ICT 2 في غرفة المعيشة والمطبخ وغرف النوم، ونقطة شحن مجهّزة مسبقاً للسيارة الكهربائية.',
  'TV- en ethernetaansluitingen volgens de telecommunicatienorm ICT 2 in de woonkamer, keuken en slaapkamers, en een voorbereid laadpunt voor een elektrische auto.',
  'Gniazda TV i ethernet zgodne ze standardem telekomunikacyjnym ICT 2 w salonie, kuchni i sypialniach oraz wstępnie przygotowany punkt ładowania samochodu elektrycznego.',
  'TV- og ethernet-tilkoblinger etter telekommunikasjonsstandarden ICT 2 i stue, kjøkken og soverom, og et forhåndsinstallert ladepunkt for elbil.',
  'TV- och ethernetuttag enligt telekommunikationsstandarden ICT 2 i vardagsrum, kök och sovrum, och en förberedd laddpunkt för elbil.')
a('.qualitySpecs.groups[6].items[1]',
  'Iluminación en las paredes que dan al jardín, y una toma de TV, enchufes y un grifo de agua en el patio.',
  'Éclairage sur les murs donnant sur le jardin, et une prise TV, des prises électriques et un robinet d’eau sur le patio.',
  'Beleuchtung an den zum Garten gerichteten Wänden sowie ein TV-Anschluss, Steckdosen und ein Wasserhahn auf der Terrasse.',
  'Освещение на стенах, выходящих в сад, а также телевизионная розетка, электрические розетки и водопроводный кран на патио.',
  'إضاءة على الجدران المطلة على الحديقة، ووصلة تلفزيون ومقابس كهربائية وصنبور ماء في الباحة.',
  'Verlichting op de muren aan de tuinzijde, en een tv-aansluiting, stopcontacten en een waterkraan op de patio.',
  'Oświetlenie na ścianach od strony ogrodu oraz gniazdo TV, gniazdka elektryczne i kran z wodą na patio.',
  'Belysning på veggene mot hagen, og en TV-tilkobling, stikkontakter og en vannkran på uteplassen.',
  'Belysning på väggarna mot trädgården, och ett TV-uttag, eluttag och en vattenkran på uteplatsen.')
a('.qualitySpecs.groups[7].items[0]',
  'Tres piscinas de cloración salina, de las cuales la memoria describe una para nadar y otra para relajarse, un gimnasio totalmente equipado y un club social.',
  'Trois piscines à chloration saline, dont le descriptif présente une pour nager et une pour se détendre, une salle de sport entièrement équipée et un club social.',
  'Drei Salzwasserpools, von denen die Beschreibung einen zum Schwimmen und einen zur Entspannung nennt, ein voll ausgestatteter Fitnessraum und ein Clubraum.',
  'Три бассейна с солевой хлоринацией, из которых описание называет один для плавания и один для отдыха, полностью оборудованный тренажёрный зал и клуб.',
  'ثلاثة مسابح بالتعقيم الملحي، تصف المواصفات أحدها للسباحة وآخر للاسترخاء، وصالة رياضية مجهّزة بالكامل ونادٍ اجتماعي.',
  'Drie zoutwaterzwembaden, waarvan de beschrijving er één om in te zwemmen en één om te ontspannen noemt, een volledig uitgeruste fitnessruimte en een sociale club.',
  'Trzy baseny z chlorowaniem solnym, z których opis wymienia jeden do pływania i jeden do relaksu, w pełni wyposażona siłownia i klub.',
  'Tre saltvannsbasseng, hvorav beskrivelsen nevner ett for svømming og ett for avslapning, et fullt utstyrt treningsrom og en sosial klubb.',
  'Tre saltvattenpooler, varav beskrivningen nämner en för simning och en för avkoppling, ett fullt utrustat gym och en klubblokal.')
a('.qualitySpecs.groups[7].items[1]',
  'Jardines con iluminación y riego automático, y un desfibrilador portátil.',
  'Jardins avec éclairage et arrosage automatique, et un défibrillateur portable.',
  'Gärten mit Beleuchtung und automatischer Bewässerung sowie ein tragbarer Defibrillator.',
  'Сады с освещением и автоматическим поливом и портативный дефибриллятор.',
  'حدائق مزوّدة بالإضاءة والري الآلي، وجهاز إزالة رجفان محمول.',
  'Tuinen met verlichting en automatische irrigatie, en een draagbare defibrillator.',
  'Ogrody z oświetleniem i automatycznym nawadnianiem oraz przenośny defibrylator.',
  'Hager med belysning og automatisk vanning, og en bærbar defibrillator.',
  'Trädgårdar med belysning och automatisk bevattning, och en bärbar defibrillator.')
a('.qualitySpecs.groups[7].items[2]',
  'Urbanización cerrada con acceso privado únicamente y caseta de control de acceso, videoportero en la entrada, llaves maestras con varios niveles de seguridad y puerta de entrada automática con apertura a distancia.',
  'Résidence fermée à accès privé uniquement, avec poste de contrôle d’accès, vidéophone à l’entrée, clés maîtresses à plusieurs niveaux de sécurité et portail d’entrée automatique à ouverture à distance.',
  'Geschlossene Anlage mit ausschließlich privatem Zugang und Zugangskontrollhäuschen, Videosprechanlage am Eingang, Generalschlüsseln mit mehreren Sicherheitsstufen und automatischem Einfahrtstor mit Fernöffnung.',
  'Закрытый комплекс только с частным въездом и постом контроля доступа, видеодомофон у входа, мастер-ключи с несколькими уровнями доступа и автоматические въездные ворота с дистанционным открыванием.',
  'مجمع مغلق بمدخل خاص فقط وكشك للتحكم في الدخول، وجرس مرئي عند المدخل، ومفاتيح رئيسية بعدة مستويات أمنية، وبوابة دخول آلية تُفتح عن بُعد.',
  'Een besloten complex met uitsluitend privétoegang en een toegangscontrolepost, een videofoon bij de ingang, loper-sleutels met meerdere beveiligingsniveaus en een automatische toegangspoort met afstandsbediening.',
  'Zamknięte osiedle wyłącznie z prywatnym dojazdem i budką kontroli wjazdu, wideodomofon przy wejściu, klucze główne o kilku poziomach zabezpieczeń i automatyczna brama wjazdowa otwierana zdalnie.',
  'Et bevoktet område med kun privat adkomst og en adgangskontrollbod, videoport ved inngangen, hovednøkler med flere sikkerhetsnivåer og en automatisk inngangsport med fjernåpning.',
  'Ett bevakat område med enbart privat infart och en bevakningsbod, videoporttelefon vid entrén, huvudnycklar på flera säkerhetsnivåer och en automatisk grind med fjärröppning.')

# ---- availability, unit sizes, timeline and payment ---------------------------------------------

a('.availability.copy',
  'La lista de precios de la fase 1 recoge tres viviendas con precio. La segunda fase tiene su propia hoja de pago pero todavía no tiene lista de precios, así que no se muestra ninguna vivienda de la fase 2. Los precios son los del promotor y no incluyen IVA, y confirmamos precio y disponibilidad antes de cualquier reserva.',
  'La liste de prix de la phase 1 recense trois logements avec un prix. La seconde phase a sa propre fiche de paiement mais pas encore de liste de prix, de sorte qu’aucun logement de la phase 2 n’est présenté ici. Les prix sont ceux du promoteur et s’entendent hors TVA, et nous confirmons prix et disponibilité avant toute réservation.',
  'Die Preisliste der Phase 1 nennt drei Häuser mit Preis. Die zweite Phase hat einen eigenen Zahlungsplan, aber noch keine Preisliste, daher wird hier kein Haus der Phase 2 gezeigt. Die Preise stammen vom Bauträger und verstehen sich ohne MwSt., und wir bestätigen Preis und Verfügbarkeit vor jeder Reservierung.',
  'В прайс-листе первой фазы указаны три дома с ценой. У второй фазы есть собственный график платежей, но пока нет прайс-листа, поэтому дома второй фазы здесь не показаны. Цены — застройщика и не включают НДС; цену и наличие мы подтверждаем до любого бронирования.',
  'تذكر قائمة أسعار المرحلة الأولى ثلاثة مساكن لها سعر. وللمرحلة الثانية جدول دفع خاص بها لكن ليس لها قائمة أسعار بعد، لذلك لا يُعرض هنا أي مسكن من المرحلة الثانية. الأسعار هي أسعار المطوّر ولا تشمل ضريبة القيمة المضافة، ونؤكد السعر والتوافر قبل أي حجز.',
  'De prijslijst van fase 1 noemt drie woningen met een prijs. De tweede fase heeft een eigen betalingsschema maar nog geen prijslijst, dus er wordt hier geen woning van fase 2 getoond. De prijzen zijn die van de ontwikkelaar en exclusief btw, en we bevestigen prijs en beschikbaarheid vóór elke reservering.',
  'Cennik etapu 1 wymienia trzy domy z ceną. Drugi etap ma własny harmonogram płatności, ale jeszcze nie ma cennika, dlatego nie pokazujemy tu żadnego domu z etapu 2. Ceny pochodzą od dewelopera i nie zawierają VAT, a cenę i dostępność potwierdzamy przed każdą rezerwacją.',
  'Prislisten for fase 1 nevner tre boliger med pris. Fase 2 har sin egen betalingsplan, men ingen prisliste ennå, så ingen bolig i fase 2 vises her. Prisene er utbyggerens og er uten mva, og vi bekrefter pris og tilgjengelighet før enhver reservasjon.',
  'Prislistan för fas 1 nämner tre bostäder med pris. Fas 2 har en egen betalningsplan men ännu ingen prislista, så ingen bostad i fas 2 visas här. Priserna är exploatörens och är exklusive IVA, och vi bekräftar pris och tillgänglighet före varje reservation.')
a('.availability.sourceNote',
  'Los precios, las superficies y las orientaciones están transcritos de la lista de precios de la fase 1 del promotor, que no lleva fecha impresa (su archivo se creó el 9 de septiembre de 2026) y recoge tres adosados con precio y sin columna de estado. La lista indica que el IVA no está incluido. Sus superficies construidas y jardines coinciden con los planos. El IVA del 10% y el impuesto de timbre del 1,20% llevan una vivienda de {E495000} a unos {E550000} y la de {E505000} a unos {E562000}, antes de los gastos de notaría y registro. La lista no indica si la plaza de aparcamiento dibujada en cada parcela está incluida en el precio.',
  'Les prix, les surfaces et les orientations sont retranscrits de la liste de prix de la phase 1 du promoteur, qui ne porte aucune date imprimée (son fichier a été créé le 9 septembre 2026) et recense trois maisons mitoyennes avec un prix et sans colonne de statut. La liste précise que la TVA n’est pas incluse. Ses surfaces construites et ses jardins concordent avec les plans. La TVA à 10 % et le droit de timbre à 1,20 % portent un logement à {E495000} à environ {E550000} et celui à {E505000} à environ {E562000}, avant les frais de notaire et de registre. La liste ne dit pas si la place de stationnement dessinée sur chaque parcelle est comprise dans le prix.',
  'Preise, Flächen und Ausrichtungen sind aus der Preisliste der Phase 1 des Bauträgers übernommen, die kein aufgedrucktes Datum trägt (ihre Datei wurde am 9. September 2026 erstellt) und drei Reihenhäuser mit Preis, aber ohne Statusspalte aufführt. Die Liste gibt an, dass die MwSt. nicht enthalten ist. Ihre bebauten Flächen und Gärten stimmen mit den Plänen überein. 10 % MwSt. und 1,20 % Stempelsteuer bringen ein Haus zu {E495000} auf etwa {E550000} und das zu {E505000} auf etwa {E562000}, vor Notar- und Grundbuchkosten. Die Liste sagt nicht, ob der auf jedem Grundstück eingezeichnete Stellplatz im Preis enthalten ist.',
  'Цены, площади и ориентация перенесены из прайс-листа первой фазы от застройщика, на котором нет напечатанной даты (файл создан 9 сентября 2026 года) и в котором указаны три таунхауса с ценой, без колонки статуса. В прайс-листе сказано, что НДС не включён. Застроенные площади и сады в нём совпадают с планировками. НДС 10 % и гербовый сбор 1,20 % доводят цену дома за {E495000} примерно до {E550000}, а дома за {E505000} — примерно до {E562000}, до расходов на нотариуса и регистрацию. В прайс-листе не сказано, включено ли в цену парковочное место, нарисованное на каждом участке.',
  'الأسعار والمساحات والاتجاهات منقولة من قائمة أسعار المرحلة الأولى الصادرة عن المطوّر، وهي لا تحمل تاريخاً مطبوعاً (أُنشئ ملفها في 9 سبتمبر 2026) وتذكر ثلاثة منازل متلاصقة بسعر ودون عمود للحالة. وتذكر القائمة أن ضريبة القيمة المضافة غير مشمولة. وتتفق مساحاتها المبنية وحدائقها مع المخططات. وتصل ضريبة القيمة المضافة 10% وضريبة الطابع 1.20% بمسكن سعره {E495000} إلى نحو {E550000}، وبالمسكن البالغ {E505000} إلى نحو {E562000}، قبل رسوم الموثّق والتسجيل العقاري. ولا تذكر القائمة ما إذا كان موقف السيارة المرسوم في كل قطعة مشمولاً بالسعر.',
  'Prijzen, oppervlakten en oriëntaties zijn overgenomen uit de prijslijst van fase 1 van de ontwikkelaar, die geen gedrukte datum draagt (het bestand is op 9 september 2026 aangemaakt) en drie rijwoningen met een prijs en zonder statuskolom vermeldt. De lijst zegt dat btw niet is inbegrepen. De bebouwde oppervlakten en tuinen komen overeen met de plattegronden. 10% btw en 1,20% zegelrecht brengen een woning van {E495000} op ongeveer {E550000} en die van {E505000} op ongeveer {E562000}, vóór notaris- en kadasterkosten. De lijst zegt niet of de op elk perceel getekende parkeerplaats in de prijs is inbegrepen.',
  'Ceny, powierzchnie i orientacje przepisano z cennika etapu 1 dewelopera, który nie ma wydrukowanej daty (jego plik utworzono 9 września 2026 r.) i wymienia trzy domy szeregowe z ceną, bez kolumny statusu. Cennik podaje, że VAT nie jest wliczony. Powierzchnie zabudowy i ogrody zgadzają się z rzutami. VAT w wysokości 10% i opłata skarbowa 1,20% podnoszą cenę domu za {E495000} do około {E550000}, a domu za {E505000} do około {E562000}, przed kosztami notariusza i rejestru. Cennik nie mówi, czy miejsce parkingowe narysowane na każdej działce jest wliczone w cenę.',
  'Priser, arealer og orienteringer er hentet fra utbyggerens prisliste for fase 1, som ikke har trykt dato (filen ble opprettet 9. september 2026) og oppfører tre rekkehus med pris og uten statuskolonne. Listen sier at mva ikke er inkludert. De bebygde arealene og hagene stemmer med plantegningene. Mva på 10 % og dokumentavgift på 1,20 % bringer en bolig til {E495000} opp i omtrent {E550000} og boligen til {E505000} opp i omtrent {E562000}, før notar- og tinglysingsgebyrer. Listen sier ikke om parkeringsplassen som er tegnet inn på hver tomt er inkludert i prisen.',
  'Priser, ytor och väderstreck är hämtade från exploatörens prislista för fas 1, som saknar tryckt datum (filen skapades den 9 september 2026) och upptar tre radhus med pris och utan statuskolumn. Listan anger att IVA inte ingår. De byggda ytorna och trädgårdarna stämmer med planritningarna. IVA på 10 % och stämpelskatt på 1,20 % för en bostad på {E495000} till omkring {E550000} och bostaden på {E505000} till omkring {E562000}, före notarie- och lagfartsavgifter. Listan anger inte om parkeringsplatsen som är ritad på varje tomt ingår i priset.')

SIZES = {
    'es': '{N%s} {U} interiores, {N%s} {U} de terraza, {N%s} {U} de jardín',
    'fr': '{N%s} {U} intérieurs, {N%s} {U} de terrasse, {N%s} {U} de jardin',
    'de': '{N%s} {U} Innenfläche, {N%s} {U} Terrasse, {N%s} {U} Garten',
    'ru': '{N%s} {U} внутри, терраса {N%s} {U}, сад {N%s} {U}',
    'ar': '{N%s} {U} داخلية، {N%s} {U} تراس، {N%s} {U} حديقة',
    'nl': '{N%s} {U} binnen, {N%s} {U} terras, {N%s} {U} tuin',
    'pl': '{N%s} {U} wnętrza, {N%s} {U} tarasu, {N%s} {U} ogrodu',
    'no': '{N%s} {U} innvendig, {N%s} {U} terrasse, {N%s} {U} hage',
    'sv': '{N%s} {U} inomhus, {N%s} {U} terrass, {N%s} {U} trädgård',
}
for i, trio in enumerate((('100.37', '9.15', '21.34'), ('100.37', '9.15', '29.51'), ('100.37', '11.55', '15.86'))):
    a(f'.availability.units[{i}].size', *[SIZES[l] % trio for l in LOCS])

a('.constructionTimeline.points[0].label', 'Escritura de la fase 1', 'Acte de la phase 1', 'Beurkundung Phase 1',
  'Нотариальная сделка, фаза 1', 'سند ملكية المرحلة 1', 'Notariële akte fase 1', 'Akt notarialny, etap 1', 'Skjøte fase 1', 'Köpebrev fas 1')
a('.constructionTimeline.points[1].year', 'T2 2029', 'T2 2029', 'Q2 2029', '2 кв. 2029', 'الربع الثاني 2029', 'K2 2029',
  'II kw. 2029', 'K2 2029', 'K2 2029')
a('.constructionTimeline.points[1].label', 'Escritura de la fase 2', 'Acte de la phase 2', 'Beurkundung Phase 2',
  'Нотариальная сделка, фаза 2', 'سند ملكية المرحلة 2', 'Notariële akte fase 2', 'Akt notarialny, etap 2', 'Skjøte fase 2', 'Köpebrev fas 2')
a('.constructionTimeline.note',
  'Las hojas de pago sitúan la escritura, con la entrega de llaves y el último pago, en el tercer trimestre de 2028 en la fase 1 y en el segundo trimestre de 2029 en la fase 2. No mencionan licencia de obra, inicio de obras ni fecha contractual de terminación, así que Nueva Living pide los tres por escrito y fija la fecha en el contrato.',
  'Les fiches de paiement placent l’acte, avec la remise des clés et le dernier paiement, au troisième trimestre 2028 pour la phase 1 et au deuxième trimestre 2029 pour la phase 2. Elles ne mentionnent ni permis de construire, ni démarrage des travaux, ni date contractuelle d’achèvement : Nueva Living demande les trois par écrit et fait inscrire la date au contrat.',
  'Die Zahlungspläne legen die Beurkundung samt Schlüsselübergabe und letzter Zahlung in Phase 1 auf das dritte Quartal 2028 und in Phase 2 auf das zweite Quartal 2029. Eine Baugenehmigung, einen Baubeginn oder ein vertragliches Fertigstellungsdatum erwähnen sie nicht; Nueva Living verlangt alle drei schriftlich und lässt das Datum im Vertrag festhalten.',
  'Графики платежей относят нотариальную сделку с передачей ключей и последним платежом к третьему кварталу 2028 года в первой фазе и ко второму кварталу 2029 года во второй. Разрешение на строительство, начало работ и договорную дату завершения они не упоминают, поэтому Nueva Living запрашивает все три письменно и закрепляет дату в договоре.',
  'تحدد جداول الدفع موعد سند الملكية مع تسليم المفاتيح والدفعة الأخيرة في الربع الثالث من 2028 للمرحلة الأولى وفي الربع الثاني من 2029 للمرحلة الثانية. ولا تذكر رخصة بناء ولا بدء أعمال ولا تاريخ إنجاز تعاقدياً، لذلك تطلب Nueva Living الثلاثة كتابةً وتثبّت التاريخ في العقد.',
  'De betalingsschema’s plaatsen de notariële akte, met de sleuteloverdracht en de laatste betaling, in het derde kwartaal van 2028 voor fase 1 en in het tweede kwartaal van 2029 voor fase 2. Ze vermelden geen bouwvergunning, geen start van de werken en geen contractuele opleverdatum, dus Nueva Living vraagt alle drie schriftelijk op en laat de datum in het contract vastleggen.',
  'Harmonogramy płatności umieszczają akt notarialny wraz z przekazaniem kluczy i ostatnią płatnością w trzecim kwartale 2028 r. w etapie 1 i w drugim kwartale 2029 r. w etapie 2. Nie wspominają o pozwoleniu na budowę, rozpoczęciu robót ani umownym terminie ukończenia, dlatego Nueva Living prosi o wszystkie trzy na piśmie i wpisuje termin do umowy.',
  'Betalingsplanene legger skjøtet, med nøkkeloverleveringen og siste betaling, til tredje kvartal 2028 i fase 1 og andre kvartal 2029 i fase 2. De nevner verken byggetillatelse, byggestart eller en avtalt ferdigstillelsesdato, så Nueva Living ber om alle tre skriftlig og får datoen inn i kontrakten.',
  'Betalningsplanerna lägger köpebrevet, med nyckelöverlämningen och den sista betalningen, till tredje kvartalet 2028 i fas 1 och andra kvartalet 2029 i fas 2. De nämner varken bygglov, byggstart eller ett avtalat färdigställandedatum, så Nueva Living begär alla tre skriftligt och får in datumet i kontraktet.')

TAXW = dict(zip(LOCS, ['IVA', 'TVA', 'MwSt.', 'НДС', 'ضريبة القيمة المضافة', 'btw', 'VAT', 'mva', 'IVA']))
a('.constructionTimeline.paymentTerms[0][1]', *[f'{{E6000}} + {TAXW[l]}' for l in LOCS])
a('.constructionTimeline.paymentTerms[0][2]',
  '{E6600} con IVA', '{E6600} TVA incluse', '{E6600} mit MwSt.', '{E6600} с НДС', '{E6600} شاملة ضريبة القيمة المضافة',
  '{E6600} incl. btw', '{E6600} z VAT', '{E6600} med mva', '{E6600} med IVA')
for pct in ('20', '15', '65'):
    put(f'{pct}% + VAT', [f'{pct}% + {TAXW[l]}' for l in LOCS])
a('.constructionTimeline.paymentTerms[1][2]',
  'En los 60 días siguientes a la reserva, menos el importe de la reserva', 'Dans les 60 jours suivant la réservation, moins le montant de la réservation',
  'Innerhalb von 60 Tagen nach der Reservierung, abzüglich des Reservierungsbetrags', 'В течение 60 дней после бронирования, за вычетом суммы бронирования',
  'خلال 60 يوماً من الحجز، ناقص مبلغ الحجز', 'Binnen 60 dagen na de reservering, minus het reserveringsbedrag',
  'W ciągu 60 dni od rezerwacji, pomniejszone o kwotę rezerwacji', 'Innen 60 dager etter reservasjonen, fratrukket reservasjonsbeløpet',
  'Inom 60 dagar efter reservationen, minus reservationsbeloppet')
a('.constructionTimeline.paymentTerms[2][0]', 'Pagos aplazados', 'Paiements différés', 'Aufgeschobene Zahlungen', 'Отложенные платежи',
  'دفعات مؤجلة', 'Uitgestelde betalingen', 'Płatności odroczone', 'Utsatte betalinger', 'Uppskjutna betalningar')
a('.constructionTimeline.paymentTerms[2][2]',
  'Tres pagos: el 5 de febrero de 2027, el 5 de agosto de 2027 y el 5 de febrero de 2028',
  'Trois paiements : le 5 février 2027, le 5 août 2027 et le 5 février 2028',
  'Drei Zahlungen: am 5. Februar 2027, am 5. August 2027 und am 5. Februar 2028',
  'Три платежа: 5 февраля 2027 года, 5 августа 2027 года и 5 февраля 2028 года',
  'ثلاث دفعات: في 5 فبراير 2027 و5 أغسطس 2027 و5 فبراير 2028',
  'Drie betalingen: op 5 februari 2027, 5 augustus 2027 en 5 februari 2028',
  'Trzy płatności: 5 lutego 2027 r., 5 sierpnia 2027 r. i 5 lutego 2028 r.',
  'Tre betalinger: 5. februar 2027, 5. august 2027 og 5. februar 2028',
  'Tre betalningar: den 5 februari 2027, den 5 augusti 2027 och den 5 februari 2028')
a('.constructionTimeline.paymentTerms[3][2]',
  'En la escritura, en el tercer trimestre de 2028, con la entrega de llaves', 'À l’acte, au troisième trimestre 2028, avec la remise des clés',
  'Bei der Beurkundung im dritten Quartal 2028, mit der Schlüsselübergabe', 'При нотариальной сделке в третьем квартале 2028 года, с передачей ключей',
  'عند سند الملكية في الربع الثالث من 2028، مع تسليم المفاتيح', 'Bij de notariële akte in het derde kwartaal van 2028, bij de sleuteloverdracht',
  'Przy akcie notarialnym w trzecim kwartale 2028 r., z przekazaniem kluczy', 'Ved skjøtet i tredje kvartal 2028, med nøkkeloverleveringen',
  'Vid köpebrevet under tredje kvartalet 2028, med nyckelöverlämningen')
a('.constructionTimeline.paymentTermsNote',
  'Estas son las condiciones de la fase 1. La fase 2 tiene su propia hoja, con los mismos porcentajes, plazos el 5 de abril de 2027, el 5 de octubre de 2027 y el 5 de abril de 2028, y la escritura en el segundo trimestre de 2029. Las hojas no indican cómo se garantizan los pagos a cuenta ni si el aplazamiento lleva intereses, así que Nueva Living pide ambas cosas por escrito antes de que reserve.',
  'Voici les conditions de la phase 1. La phase 2 a sa propre fiche, avec les mêmes pourcentages, des échéances au 5 avril 2027, au 5 octobre 2027 et au 5 avril 2028, et l’acte au deuxième trimestre 2029. Les fiches n’indiquent pas comment les versements sont garantis ni si le report porte intérêt : Nueva Living demande les deux par écrit avant que vous ne réserviez.',
  'Dies sind die Bedingungen der Phase 1. Phase 2 hat einen eigenen Plan mit denselben Prozentsätzen, Raten am 5. April 2027, 5. Oktober 2027 und 5. April 2028 sowie der Beurkundung im zweiten Quartal 2029. Die Pläne sagen nicht, wie die Anzahlungen abgesichert sind und ob die Stundung verzinst wird; Nueva Living verlangt beides schriftlich, bevor Sie reservieren.',
  'Это условия первой фазы. У второй фазы собственный график с теми же процентами, платежами 5 апреля 2027 года, 5 октября 2027 года и 5 апреля 2028 года и нотариальной сделкой во втором квартале 2029 года. В графиках не сказано, чем гарантированы авансовые платежи и начисляются ли проценты на отсрочку, поэтому Nueva Living запрашивает оба ответа письменно до вашего бронирования.',
  'هذه شروط المرحلة الأولى. وللمرحلة الثانية جدول خاص بها بالنسب نفسها، ودفعات في 5 أبريل 2027 و5 أكتوبر 2027 و5 أبريل 2028، وسند الملكية في الربع الثاني من 2029. ولا تذكر الجداول كيف تُضمن الدفعات المقدمة ولا ما إذا كان التأجيل بفائدة، لذلك تطلب Nueva Living الأمرين كتابةً قبل أن تحجزوا.',
  'Dit zijn de voorwaarden van fase 1. Fase 2 heeft een eigen schema met dezelfde percentages, termijnen op 5 april 2027, 5 oktober 2027 en 5 april 2028, en de notariële akte in het tweede kwartaal van 2029. De schema’s zeggen niet hoe de vooruitbetalingen worden gewaarborgd en of het uitstel rente kost; Nueva Living vraagt beide schriftelijk op voordat u reserveert.',
  'To warunki etapu 1. Etap 2 ma własny harmonogram z tymi samymi procentami, ratami 5 kwietnia 2027 r., 5 października 2027 r. i 5 kwietnia 2028 r. oraz aktem notarialnym w drugim kwartale 2029 r. Harmonogramy nie podają, jak zabezpieczone są wpłaty na poczet ceny ani czy odroczenie jest oprocentowane, dlatego Nueva Living prosi o oba te dane na piśmie, zanim nastąpi rezerwacja.',
  'Dette er vilkårene for fase 1. Fase 2 har sin egen plan med de samme prosentene, avdrag 5. april 2027, 5. oktober 2027 og 5. april 2028, og skjøtet i andre kvartal 2029. Planene sier ikke hvordan forskuddsbetalingene er sikret eller om utsettelsen har renter, så Nueva Living ber om begge deler skriftlig før du reserverer.',
  'Detta är villkoren för fas 1. Fas 2 har en egen plan med samma procentsatser, delbetalningar den 5 april 2027, den 5 oktober 2027 och den 5 april 2028, och köpebrevet under andra kvartalet 2029. Planerna anger inte hur förskottsbetalningarna garanteras eller om uppskovet medför ränta, så Nueva Living begär båda skriftligt innan ni reserverar.')

# ---- why, investment, trust ---------------------------------------------------------------------

a('.why.copy',
  'Adosados de tres dormitorios con jardín propio y una plaza de aparcamiento en la parcela, en una urbanización cerrada con tres piscinas, gimnasio y club social.',
  'Maisons mitoyennes de trois chambres avec jardin et une place de stationnement sur la parcelle, dans une résidence fermée avec trois piscines, une salle de sport et un club social.',
  'Reihenhäuser mit drei Schlafzimmern, eigenem Garten und einem Stellplatz auf dem Grundstück in einer geschlossenen Anlage mit drei Pools, Fitnessraum und Clubraum.',
  'Таунхаусы с тремя спальнями, собственным садом и парковочным местом на участке в закрытом комплексе с тремя бассейнами, тренажёрным залом и клубом.',
  'منازل متلاصقة بثلاث غرف نوم وحديقة خاصة وموقف سيارة في القطعة، داخل مجمع مغلق فيه ثلاثة مسابح وصالة رياضية ونادٍ اجتماعي.',
  'Rijwoningen met drie slaapkamers, een eigen tuin en een parkeerplaats op het perceel, in een besloten complex met drie zwembaden, een fitnessruimte en een sociale club.',
  'Domy szeregowe z trzema sypialniami, własnym ogrodem i miejscem parkingowym na działce, w zamkniętym osiedlu z trzema basenami, siłownią i klubem.',
  'Rekkehus med tre soverom, egen hage og en parkeringsplass på tomten, i et bevoktet område med tre basseng, treningsrom og sosial klubb.',
  'Radhus med tre sovrum, egen trädgård och en parkeringsplats på tomten, i ett bevakat område med tre pooler, gym och klubblokal.')
a('.why.points[0][1]',
  'Compradores que quieren una casa de tres dormitorios con jardín propio en lugar de un apartamento, para vivir o como segunda residencia en la costa de Mijas.',
  'Acheteurs qui veulent une maison de trois chambres avec son propre jardin plutôt qu’un appartement, pour y vivre ou comme résidence secondaire sur la côte de Mijas.',
  'Käufer, die statt einer Wohnung ein Haus mit drei Schlafzimmern und eigenem Garten suchen, zum Selbstbewohnen oder als Zweitwohnsitz an der Küste von Mijas.',
  'Покупатели, которым нужен дом с тремя спальнями и собственным садом, а не квартира, для постоянного проживания или как вторая недвижимость на побережье Михаса.',
  'المشترون الذين يريدون منزلاً بثلاث غرف نوم وحديقة خاصة بدلاً من شقة، للسكن أو كمسكن ثانٍ على ساحل ميخاس.',
  'Kopers die liever een huis met drie slaapkamers en een eigen tuin willen dan een appartement, om zelf te bewonen of als tweede woning aan de kust van Mijas.',
  'Kupujący, którzy zamiast mieszkania chcą dom z trzema sypialniami i własnym ogrodem, do zamieszkania lub jako drugi dom na wybrzeżu Mijas.',
  'Kjøpere som vil ha et hus med tre soverom og egen hage fremfor en leilighet, til å bo i eller som feriebolig på kysten av Mijas.',
  'Köpare som vill ha ett hus med tre sovrum och egen trädgård i stället för en lägenhet, att bo i eller som andrabostad på Mijas kust.')
a('.why.points[1][0]', 'Un jardín propio', 'Un jardin bien à vous', 'Ein eigener Garten', 'Собственный сад', 'حديقة خاصة بكم',
  'Een eigen tuin', 'Własny ogród', 'Egen hage', 'En egen trädgård')
a('.why.points[1][1]',
  'Las tres viviendas de la lista tienen cada una un jardín privado de {N15.86} a {N29.51} {U} y una terraza descubierta de {N9.15} a {N11.55} {U}, en la planta baja junto al salón.',
  'Les trois logements de la liste ont chacun un jardin privatif de {N15.86} à {N29.51} {U} et une terrasse découverte de {N9.15} à {N11.55} {U}, au rez-de-chaussée à côté du séjour.',
  'Die drei Häuser der Liste haben jeweils einen Privatgarten von {N15.86} bis {N29.51} {U} und eine unüberdachte Terrasse von {N9.15} bis {N11.55} {U}, im Erdgeschoss neben dem Wohnzimmer.',
  'У каждого из трёх домов в списке есть собственный сад от {N15.86} до {N29.51} {U} и открытая терраса от {N9.15} до {N11.55} {U} на первом этаже рядом с гостиной.',
  'لكل من المساكن الثلاثة في القائمة حديقة خاصة مساحتها من {N15.86} إلى {N29.51} {U} وشرفة مكشوفة من {N9.15} إلى {N11.55} {U}، في الطابق الأرضي بجوار غرفة المعيشة.',
  'De drie woningen op de lijst hebben elk een privétuin van {N15.86} tot {N29.51} {U} en een onoverdekt terras van {N9.15} tot {N11.55} {U}, op de begane grond naast de woonkamer.',
  'Każdy z trzech domów z listy ma prywatny ogród o powierzchni od {N15.86} do {N29.51} {U} i odkryty taras od {N9.15} do {N11.55} {U}, na parterze obok salonu.',
  'De tre boligene på listen har hver en egen hage på {N15.86} til {N29.51} {U} og en åpen terrasse på {N9.15} til {N11.55} {U}, i første etasje ved siden av stuen.',
  'De tre bostäderna på listan har var och en en egen trädgård på {N15.86} till {N29.51} {U} och en öppen terrass på {N9.15} till {N11.55} {U}, på bottenplanet bredvid vardagsrummet.')
a('.why.points[2][0]', 'Instalaciones comunes', 'Équipements communs', 'Gemeinschaftseinrichtungen', 'Общие удобства', 'مرافق مشتركة',
  'Gemeenschappelijke voorzieningen', 'Wspólne udogodnienia', 'Felles fasiliteter', 'Gemensamma bekvämligheter')
a('.why.points[2][1]',
  'Tres piscinas de cloración salina, un gimnasio totalmente equipado, un club social y una zona chill-out, en jardines paisajísticos dentro de una urbanización cerrada con acceso controlado.',
  'Trois piscines à chloration saline, une salle de sport entièrement équipée, un club social et un espace chill-out, dans des jardins paysagers à l’intérieur d’une résidence fermée à accès contrôlé.',
  'Drei Salzwasserpools, ein voll ausgestatteter Fitnessraum, ein Clubraum und ein Chill-out-Bereich, in gestalteten Gärten innerhalb einer geschlossenen Anlage mit Zugangskontrolle.',
  'Три бассейна с солевой хлоринацией, полностью оборудованный тренажёрный зал, клуб и зона отдыха в ландшафтных садах внутри закрытого комплекса с контролируемым въездом.',
  'ثلاثة مسابح بالتعقيم الملحي وصالة رياضية مجهّزة بالكامل ونادٍ اجتماعي ومنطقة استرخاء، في حدائق منسّقة داخل مجمع مغلق بمدخل مراقَب.',
  'Drie zoutwaterzwembaden, een volledig uitgeruste fitnessruimte, een sociale club en een chill-outzone, in aangelegde tuinen binnen een besloten complex met toegangscontrole.',
  'Trzy baseny z chlorowaniem solnym, w pełni wyposażona siłownia, klub i strefa chill-out, w zaaranżowanych ogrodach wewnątrz zamkniętego osiedla z kontrolą wjazdu.',
  'Tre saltvannsbasseng, et fullt utstyrt treningsrom, en sosial klubb og en chill-out-sone, i opparbeidede hager i et bevoktet område med adgangskontroll.',
  'Tre saltvattenpooler, ett fullt utrustat gym, en klubblokal och en chill-out-yta, i anlagda trädgårdar inne i ett bevakat område med kontrollerad infart.')
a('.why.points[3][0]', 'La mayor parte del precio se paga en la escritura', 'L’essentiel du prix se règle à l’acte',
  'Der größte Teil des Preises fällt bei der Beurkundung an', 'Большая часть цены оплачивается при нотариальной сделке',
  'معظم الثمن يُدفع عند سند الملكية', 'Het grootste deel van de prijs valt bij de akte', 'Większość ceny płaci się przy akcie notarialnym',
  'Mesteparten av prisen forfaller ved skjøtet', 'Största delen av priset förfaller vid köpebrevet')
a('.why.points[3][1]',
  'El 65% del precio se paga en la escritura, en el tercer trimestre de 2028, tras el 20% en el contrato privado y el 15% en tres plazos en 2027 y 2028.',
  '65 % du prix se règle à l’acte, au troisième trimestre 2028, après 20 % au contrat privé et 15 % en trois échéances en 2027 et 2028.',
  '65 % des Preises fallen bei der Beurkundung im dritten Quartal 2028 an, nach 20 % beim Privatvertrag und 15 % in drei Raten in den Jahren 2027 und 2028.',
  '65 % цены оплачиваются при нотариальной сделке в третьем квартале 2028 года — после 20 % при частном договоре и 15 % тремя платежами в 2027 и 2028 годах.',
  'يُدفع 65% من الثمن عند سند الملكية في الربع الثالث من 2028، بعد 20% عند العقد الخاص و15% على ثلاث دفعات في 2027 و2028.',
  '65% van de prijs valt bij de notariële akte in het derde kwartaal van 2028, na 20% bij het onderhandse contract en 15% in drie termijnen in 2027 en 2028.',
  '65% ceny płaci się przy akcie notarialnym w trzecim kwartale 2028 r., po 20% przy umowie przedwstępnej i 15% w trzech ratach w latach 2027 i 2028.',
  '65 % av prisen forfaller ved skjøtet i tredje kvartal 2028, etter 20 % ved privatkontrakten og 15 % i tre avdrag i 2027 og 2028.',
  '65 % av priset förfaller vid köpebrevet under tredje kvartalet 2028, efter 20 % vid det privata avtalet och 15 % i tre delbetalningar 2027 och 2028.')
a('.investment.cards[0][1]',
  'La lista de precios se da antes de IVA. El IVA del 10% y el impuesto de timbre del 1,20% suman unos {E55000} a una vivienda de {E495000} y {E57000} a la de {E505000}, antes de los gastos de notaría y registro.',
  'La liste de prix est donnée hors TVA. La TVA à 10 % et le droit de timbre à 1,20 % ajoutent environ {E55000} à un logement à {E495000} et {E57000} à celui à {E505000}, avant les frais de notaire et de registre.',
  'Die Preisliste versteht sich ohne MwSt. 10 % MwSt. und 1,20 % Stempelsteuer erhöhen ein Haus zu {E495000} um etwa {E55000} und das zu {E505000} um {E57000}, vor Notar- und Grundbuchkosten.',
  'Прайс-лист указан без НДС. НДС 10 % и гербовый сбор 1,20 % добавляют около {E55000} к дому за {E495000} и {E57000} к дому за {E505000}, до расходов на нотариуса и регистрацию.',
  'قائمة الأسعار مذكورة قبل ضريبة القيمة المضافة. وتضيف ضريبة القيمة المضافة 10% وضريبة الطابع 1.20% نحو {E55000} إلى مسكن سعره {E495000} ونحو {E57000} إلى المسكن البالغ {E505000}، قبل رسوم الموثّق والتسجيل.',
  'De prijslijst is vóór btw. 10% btw en 1,20% zegelrecht voegen ongeveer {E55000} toe aan een woning van {E495000} en {E57000} aan die van {E505000}, vóór notaris- en kadasterkosten.',
  'Cennik podano bez VAT. VAT w wysokości 10% i opłata skarbowa 1,20% dodają około {E55000} do domu za {E495000} i {E57000} do domu za {E505000}, przed kosztami notariusza i rejestru.',
  'Prislisten oppgis før mva. Mva på 10 % og dokumentavgift på 1,20 % legger til omtrent {E55000} på en bolig til {E495000} og {E57000} på boligen til {E505000}, før notar- og tinglysingsgebyrer.',
  'Prislistan anges före IVA. IVA på 10 % och stämpelskatt på 1,20 % lägger till omkring {E55000} på en bostad på {E495000} och {E57000} på bostaden på {E505000}, före notarie- och lagfartsavgifter.')
a('.investment.cards[1][0]', 'Solo la fase 1 tiene precio', 'Seule la phase 1 a un prix', 'Nur Phase 1 hat einen Preis',
  'Цена есть только у первой фазы', 'المرحلة الأولى وحدها لها سعر', 'Alleen fase 1 heeft een prijs', 'Tylko etap 1 ma cenę',
  'Bare fase 1 har pris', 'Bara fas 1 har ett pris')
a('.investment.cards[1][1]',
  'La fase 2 tiene su propia hoja de pago, con la escritura en el segundo trimestre de 2029, pero todavía no tiene lista de precios. No mostramos ningún precio de la fase 2 ni lo estimamos.',
  'La phase 2 a sa propre fiche de paiement, avec l’acte au deuxième trimestre 2029, mais pas encore de liste de prix. Nous n’affichons aucun prix de la phase 2 et n’en estimons aucun.',
  'Phase 2 hat einen eigenen Zahlungsplan mit der Beurkundung im zweiten Quartal 2029, aber noch keine Preisliste. Wir zeigen keinen Preis für Phase 2 und schätzen auch keinen.',
  'У второй фазы есть собственный график платежей с нотариальной сделкой во втором квартале 2029 года, но пока нет прайс-листа. Мы не показываем цен второй фазы и не оцениваем их.',
  'للمرحلة الثانية جدول دفع خاص بها وسند الملكية في الربع الثاني من 2029، لكن ليس لها قائمة أسعار بعد. لا نعرض أي سعر للمرحلة الثانية ولا نقدّره.',
  'Fase 2 heeft een eigen betalingsschema, met de notariële akte in het tweede kwartaal van 2029, maar nog geen prijslijst. We tonen geen prijs voor fase 2 en schatten er ook geen.',
  'Etap 2 ma własny harmonogram płatności z aktem notarialnym w drugim kwartale 2029 r., ale jeszcze nie ma cennika. Nie pokazujemy żadnej ceny etapu 2 i jej nie szacujemy.',
  'Fase 2 har sin egen betalingsplan, med skjøtet i andre kvartal 2029, men ingen prisliste ennå. Vi viser ingen pris for fase 2 og anslår heller ingen.',
  'Fas 2 har en egen betalningsplan, med köpebrevet under andra kvartalet 2029, men ännu ingen prislista. Vi visar inget pris för fas 2 och uppskattar inget heller.')
a('.investment.cards[2][1]',
  'Los planos dibujan una plaza de aparcamiento frontal de unos {N26} {U} en cada parcela. La lista de precios no dice qué incluye el precio, así que lo confirmamos por escrito.',
  'Les plans dessinent une place de stationnement frontale d’environ {N26} {U} sur chaque parcelle. La liste de prix ne dit pas ce que le prix comprend, nous le confirmons donc par écrit.',
  'Die Pläne zeichnen auf jedem Grundstück einen frontalen Stellplatz von etwa {N26} {U} ein. Die Preisliste sagt nicht, was im Preis enthalten ist, daher bestätigen wir es schriftlich.',
  'На планах на каждом участке нарисовано фронтальное парковочное место около {N26} {U}. В прайс-листе не сказано, что входит в цену, поэтому мы подтверждаем это письменно.',
  'تُظهر المخططات في كل قطعة موقف سيارة أمامياً بنحو {N26} {U}. ولا تذكر قائمة الأسعار ما يشمله السعر، لذلك نؤكد ذلك كتابةً.',
  'De plattegronden tekenen op elk perceel een parkeerplaats aan de voorzijde van ongeveer {N26} {U}. De prijslijst zegt niet wat de prijs omvat, dus we bevestigen dat schriftelijk.',
  'Plany rysują na każdej działce miejsce parkingowe z przodu o powierzchni około {N26} {U}. Cennik nie mówi, co obejmuje cena, więc potwierdzamy to na piśmie.',
  'Plantegningene tegner inn en parkeringsplass foran på omtrent {N26} {U} på hver tomt. Prislisten sier ikke hva prisen omfatter, så vi bekrefter det skriftlig.',
  'Planritningarna ritar in en parkeringsplats framför på cirka {N26} {U} på varje tomt. Prislistan anger inte vad priset omfattar, så vi bekräftar det skriftligt.')
a('.investment.cards[3][1]',
  'La hoja de pago da el tercer trimestre de 2028 para la escritura de la fase 1. Ningún documento indica el estado de la licencia ni el inicio de obras, así que pregunte qué dice el contrato si la fecha se retrasa.',
  'La fiche de paiement donne le troisième trimestre 2028 pour l’acte de la phase 1. Aucun document n’indique l’état du permis ni le démarrage des travaux : demandez ce que prévoit le contrat si la date glisse.',
  'Der Zahlungsplan nennt für die Beurkundung der Phase 1 das dritte Quartal 2028. Kein Dokument gibt den Stand der Genehmigung oder einen Baubeginn an; fragen Sie, was der Vertrag bei einer Verzögerung des Termins vorsieht.',
  'В графике платежей нотариальная сделка первой фазы указана на третий квартал 2028 года. Ни в одном документе нет сведений о статусе разрешения или начале работ, поэтому спросите, что говорит договор при переносе срока.',
  'يحدد جدول الدفع الربع الثالث من 2028 لسند ملكية المرحلة الأولى. ولا توجد في أي وثيقة حالة الرخصة أو بدء الأعمال، فاسألوا عمّا ينص عليه العقد إذا تأخر الموعد.',
  'Het betalingsschema geeft het derde kwartaal van 2028 voor de notariële akte van fase 1. Geen enkel document geeft de stand van de vergunning of een start van de werken, dus vraag wat het contract zegt als de datum opschuift.',
  'Harmonogram płatności podaje trzeci kwartał 2028 r. dla aktu notarialnego etapu 1. Żaden dokument nie podaje statusu pozwolenia ani rozpoczęcia robót, dlatego należy zapytać, co mówi umowa, jeśli termin się przesunie.',
  'Betalingsplanen oppgir tredje kvartal 2028 for skjøtet i fase 1. Ingen dokumenter oppgir status for tillatelsen eller byggestart, så spør hva kontrakten sier hvis datoen skyves.',
  'Betalningsplanen anger tredje kvartalet 2028 för köpebrevet i fas 1. Inget dokument anger status för bygglovet eller byggstart, så fråga vad avtalet säger om datumet glider.')
a('.trustDossier.cards[0][1]',
  'La lista de precios de la fase 1 recoge tres viviendas y tiene una cuarta fila en blanco. No tiene columna de estado ni fecha, y no dice nada de las demás viviendas de la fase 1 ni de la fase 2, así que pedimos la lista completa y el estado de cada vivienda.',
  'La liste de prix de la phase 1 recense trois logements et comporte une quatrième ligne vide. Elle n’a ni colonne de statut ni date, et ne dit rien des autres logements de la phase 1 ni de la phase 2 : nous demandons la liste complète et le statut de chaque logement.',
  'Die Preisliste der Phase 1 nennt drei Häuser und hat eine leere vierte Zeile. Sie hat weder eine Statusspalte noch ein Datum und sagt nichts zu den übrigen Häusern der Phase 1 oder zu Phase 2; deshalb verlangen wir die vollständige Liste und den Status jedes Hauses.',
  'В прайс-листе первой фазы указаны три дома и пустая четвёртая строка. В нём нет ни колонки статуса, ни даты, и ничего не сказано об остальных домах первой фазы и о второй фазе, поэтому мы запрашиваем полный список и статус каждого дома.',
  'تذكر قائمة أسعار المرحلة الأولى ثلاثة مساكن وفيها صف رابع فارغ. ليس فيها عمود للحالة ولا تاريخ، ولا تقول شيئاً عن بقية مساكن المرحلة الأولى ولا عن المرحلة الثانية، لذلك نطلب القائمة الكاملة وحالة كل مسكن.',
  'De prijslijst van fase 1 noemt drie woningen en heeft een lege vierde rij. Ze heeft geen statuskolom en geen datum, en zegt niets over de overige woningen van fase 1 of over fase 2, dus we vragen de volledige lijst en de status van elke woning.',
  'Cennik etapu 1 wymienia trzy domy i ma pusty czwarty wiersz. Nie ma kolumny statusu ani daty i nic nie mówi o pozostałych domach etapu 1 ani o etapie 2, dlatego prosimy o pełną listę i status każdego domu.',
  'Prislisten for fase 1 nevner tre boliger og har en tom fjerde rad. Den har ingen statuskolonne og ingen dato, og sier ingenting om de øvrige boligene i fase 1 eller om fase 2, så vi ber om den fullstendige listen og statusen for hver bolig.',
  'Prislistan för fas 1 nämner tre bostäder och har en tom fjärde rad. Den saknar statuskolumn och datum och säger inget om de övriga bostäderna i fas 1 eller om fas 2, så vi begär hela listan och status för varje bostad.')
a('.trustDossier.cards[1][0]', 'Tres dormitorios o cuatro', 'Trois chambres ou quatre', 'Drei Schlafzimmer oder vier', 'Три спальни или четыре',
  'ثلاث غرف نوم أم أربع', 'Drie slaapkamers of vier', 'Trzy sypialnie czy cztery', 'Tre soverom eller fire', 'Tre sovrum eller fyra')
a('.trustDossier.cards[1][1]',
  'El dosier describe adosados de tres y cuatro dormitorios. Las tres viviendas de la lista de precios, y todos los planos que tenemos, son de tres dormitorios, así que preguntamos dónde están las viviendas de cuatro dormitorios y cuándo tendrán precio.',
  'Le dossier décrit des maisons mitoyennes de trois et quatre chambres. Les trois logements de la liste de prix, et tous les plans que nous détenons, comptent trois chambres : nous demandons où sont les logements de quatre chambres et quand ils seront chiffrés.',
  'Das Dossier beschreibt Reihenhäuser mit drei und vier Schlafzimmern. Die drei Häuser der Preisliste und alle Pläne, die wir haben, haben drei Schlafzimmer; wir fragen daher, wo die Häuser mit vier Schlafzimmern liegen und wann sie einen Preis bekommen.',
  'В досье описаны таунхаусы с тремя и четырьмя спальнями. Три дома из прайс-листа и все имеющиеся у нас планировки — с тремя спальнями, поэтому мы спрашиваем, где дома с четырьмя спальнями и когда у них появится цена.',
  'يصف الملف التعريفي منازل متلاصقة بثلاث وأربع غرف نوم. والمساكن الثلاثة في قائمة الأسعار وجميع المخططات التي لدينا بثلاث غرف نوم، لذلك نسأل أين توجد المساكن بأربع غرف نوم ومتى يُحدَّد سعرها.',
  'Het dossier beschrijft rijwoningen met drie en vier slaapkamers. De drie woningen op de prijslijst, en alle plattegronden die we hebben, hebben drie slaapkamers, dus we vragen waar de woningen met vier slaapkamers liggen en wanneer ze een prijs krijgen.',
  'Broszura opisuje domy szeregowe z trzema i czterema sypialniami. Trzy domy z cennika i wszystkie posiadane przez nas rzuty mają trzy sypialnie, dlatego pytamy, gdzie są domy z czterema sypialniami i kiedy będą miały cenę.',
  'Brosjyren beskriver rekkehus med tre og fire soverom. De tre boligene på prislisten, og alle plantegningene vi har, har tre soverom, så vi spør hvor boligene med fire soverom ligger og når de får pris.',
  'Broschyren beskriver radhus med tre och fyra sovrum. De tre bostäderna i prislistan, och alla planritningar vi har, har tre sovrum, så vi frågar var bostäderna med fyra sovrum ligger och när de får ett pris.')
a('.trustDossier.cards[2][0]', 'La licencia y las obras', 'Le permis et les travaux', 'Die Genehmigung und die Bauarbeiten',
  'Разрешение и работы', 'الرخصة والأعمال', 'De vergunning en de werken', 'Pozwolenie i roboty', 'Tillatelsen og arbeidene', 'Bygglovet och arbetena')
a('.trustDossier.cards[2][1]',
  'Ninguno de los documentos que tenemos indica el estado de la licencia de obra ni de las obras. Las hojas de pago solo dan el trimestre de la escritura, así que pedimos la licencia, el inicio de obras y la fecha contractual de terminación.',
  'Aucun des documents que nous détenons n’indique l’état du permis de construire ni des travaux. Les fiches de paiement ne donnent que le trimestre de l’acte : nous demandons le permis, le démarrage des travaux et la date contractuelle d’achèvement.',
  'Keines der Dokumente, die wir haben, gibt den Stand der Baugenehmigung oder der Bauarbeiten an. Die Zahlungspläne nennen nur das Quartal der Beurkundung; wir verlangen daher die Genehmigung, den Baubeginn und das vertragliche Fertigstellungsdatum.',
  'Ни в одном из имеющихся у нас документов нет сведений о статусе разрешения на строительство и о ходе работ. Графики платежей указывают лишь квартал нотариальной сделки, поэтому мы запрашиваем разрешение, начало работ и договорную дату завершения.',
  'لا تذكر أي من الوثائق التي لدينا حالة رخصة البناء ولا الأعمال. وجداول الدفع تذكر فقط ربع سند الملكية، لذلك نطلب الرخصة وبدء الأعمال وتاريخ الإنجاز التعاقدي.',
  'Geen van de documenten die we hebben geeft de stand van de bouwvergunning of van de werken. De betalingsschema’s geven alleen het kwartaal van de akte, dus we vragen de vergunning, de start van de werken en de contractuele opleverdatum op.',
  'Żaden z posiadanych przez nas dokumentów nie podaje statusu pozwolenia na budowę ani robót. Harmonogramy płatności podają tylko kwartał aktu notarialnego, dlatego prosimy o pozwolenie, rozpoczęcie robót i umowny termin ukończenia.',
  'Ingen av dokumentene vi har oppgir status for byggetillatelsen eller arbeidene. Betalingsplanene gir bare kvartalet for skjøtet, så vi ber om tillatelsen, byggestarten og den avtalte ferdigstillelsesdatoen.',
  'Inget av de dokument vi har anger status för bygglovet eller arbetena. Betalningsplanerna anger bara kvartalet för köpebrevet, så vi begär bygglovet, byggstarten och det avtalade färdigställandedatumet.')
a('.trustDossier.cards[3][1]',
  'Las hojas de pago no dicen cómo se garantizan los pagos a cuenta. Pedimos ver la propia garantía, y los datos de la cuenta, antes de cualquier pago.',
  'Les fiches de paiement ne disent pas comment les versements sont garantis. Nous demandons à voir la garantie elle-même, et les coordonnées du compte, avant tout paiement.',
  'Die Zahlungspläne sagen nicht, wie die Anzahlungen abgesichert sind. Wir verlangen, vor jeder Zahlung die Garantie selbst und die Kontodaten zu sehen.',
  'В графиках платежей не сказано, чем гарантированы авансовые платежи. Мы просим показать саму гарантию и реквизиты счёта до любого платежа.',
  'لا تذكر جداول الدفع كيف تُضمن الدفعات المقدمة. نطلب الاطلاع على الضمان نفسه وعلى بيانات الحساب قبل أي دفعة.',
  'De betalingsschema’s zeggen niet hoe de vooruitbetalingen worden gewaarborgd. We vragen de garantie zelf en de rekeninggegevens te zien vóór elke betaling.',
  'Harmonogramy płatności nie mówią, jak zabezpieczone są wpłaty na poczet ceny. Prosimy o okazanie samej gwarancji oraz danych rachunku przed jakąkolwiek płatnością.',
  'Betalingsplanene sier ikke hvordan forskuddsbetalingene er sikret. Vi ber om å få se selve garantien, og kontodetaljene, før noen betaling.',
  'Betalningsplanerna anger inte hur förskottsbetalningarna garanteras. Vi begär att få se själva garantin, och kontouppgifterna, före varje betalning.')
a('.trustDossier.cards[4][1]',
  'Las imágenes están generadas por ordenador y son meramente orientativas, y el mobiliario, la decoración y la vegetación que muestran no forman parte de la oferta. Los planos son planos de proyecto que, según el promotor, pueden cambiar por exigencias técnicas o legales.',
  'Les images sont générées par ordinateur et données à titre indicatif, et le mobilier, la décoration et la végétation qu’elles montrent ne font pas partie de l’offre. Les plans sont des plans de projet que, selon le promoteur, des contraintes techniques ou légales peuvent modifier.',
  'Die Bilder sind computergeneriert und dienen nur zur Orientierung; Möbel, Dekoration und Bepflanzung darauf gehören nicht zum Angebot. Die Pläne sind Projektpläne, die sich laut Bauträger aus technischen oder rechtlichen Gründen ändern können.',
  'Изображения созданы на компьютере и носят ориентировочный характер; мебель, отделка и озеленение на них не входят в предложение. Планировки — проектные планы, которые, по словам застройщика, могут измениться по техническим или юридическим причинам.',
  'الصور مولَّدة بالحاسوب وللاسترشاد فقط، والأثاث والديكور والنباتات الظاهرة فيها ليست جزءاً من العرض. والمخططات هي مخططات مشروع يقول المطوّر إنها قد تتغير لأسباب فنية أو قانونية.',
  'De beelden zijn computergegenereerd en uitsluitend ter indicatie, en het meubilair, de inrichting en de beplanting erop maken geen deel uit van het aanbod. De plattegronden zijn projectplannen die volgens de ontwikkelaar om technische of juridische redenen kunnen wijzigen.',
  'Obrazy są wygenerowane komputerowo i mają charakter orientacyjny, a meble, wystrój i zieleń na nich nie wchodzą w skład oferty. Rzuty to plany projektowe, które według dewelopera mogą się zmienić z przyczyn technicznych lub prawnych.',
  'Bildene er datagenererte og kun veiledende, og møbler, innredning og beplantning på dem er ikke en del av tilbudet. Plantegningene er prosjektplaner som ifølge utbyggeren kan endres av tekniske eller juridiske grunner.',
  'Bilderna är datorgenererade och endast vägledande, och möbler, inredning och planteringar på dem ingår inte i erbjudandet. Planritningarna är projektritningar som enligt exploatören kan ändras av tekniska eller juridiska skäl.')

# ---- architecture, lifestyle, viewing, location, faq, seo ---------------------------------------

a('.architecture.headlineHtml',
  'Hileras de adosados, <em>cada uno con su jardín</em>', 'Des rangées de maisons mitoyennes, <em>chacune avec son jardin</em>',
  'Reihenhauszeilen, <em>jedes mit eigenem Garten</em>', 'Ряды таунхаусов, <em>у каждого свой сад</em>',
  'صفوف من المنازل المتلاصقة، <em>لكل منها حديقتها</em>', 'Rijen rijwoningen, <em>elk met een eigen tuin</em>',
  'Rzędy domów szeregowych, <em>każdy z własnym ogrodem</em>', 'Rader med rekkehus, <em>hvert med sin egen hage</em>',
  'Rader av radhus, <em>vart och ett med egen trädgård</em>')
a('.architecture.copy[0]',
  'El dosier describe 140 adosados frente a un espacio natural de frondosos pinos, diseñados para realzar el entorno, con servicios comunes a escala de resort y buenas calidades en cada vivienda.',
  'Le dossier décrit 140 maisons mitoyennes face à un espace naturel de pins denses, conçues pour mettre en valeur le cadre, avec des services communs à l’échelle d’un resort et de belles prestations dans chaque logement.',
  'Das Dossier beschreibt 140 Reihenhäuser gegenüber einem Naturraum mit dichtem Kiefernbestand, entworfen, um die Umgebung zur Geltung zu bringen, mit Gemeinschaftseinrichtungen im Resort-Maßstab und guter Ausstattung in jedem Haus.',
  'В досье описаны 140 таунхаусов напротив природной зоны с густым сосновым лесом, спроектированных так, чтобы подчеркнуть окружение, с общими удобствами уровня курорта и качественной отделкой в каждом доме.',
  'يصف الملف التعريفي 140 منزلاً متلاصقاً مقابل مساحة طبيعية كثيفة بأشجار الصنوبر، صُمّمت لإبراز المحيط، مع خدمات مشتركة بمقياس المنتجعات وتجهيزات جيدة في كل منزل.',
  'Het dossier beschrijft 140 rijwoningen tegenover een natuurgebied met dichte dennen, ontworpen om de omgeving tot haar recht te laten komen, met gemeenschappelijke voorzieningen op resortschaal en goede afwerking in elke woning.',
  'Broszura opisuje 140 domów szeregowych naprzeciw terenu naturalnego z gęstym sosnowym lasem, zaprojektowanych tak, by podkreślić otoczenie, ze wspólnymi udogodnieniami na skalę kurortu i dobrym wyposażeniem w każdym domu.',
  'Brosjyren beskriver 140 rekkehus vendt mot et naturområde med tett furuskog, utformet for å fremheve omgivelsene, med felles fasiliteter i resortskala og god standard i hver bolig.',
  'Broschyren beskriver 140 radhus vända mot ett naturområde med tät tallskog, utformade för att framhäva omgivningen, med gemensamma bekvämligheter i resortskala och god standard i varje bostad.')
a('.architecture.copy[1]',
  'En las imágenes, las viviendas forman hileras blancas de dos plantas con paneles de aspecto madera y cubiertas planas, y las terrazas de la planta baja se abren a céspedes tras setos recortados. El dosier dice que las viviendas están colocadas para captar la luz a lo largo del día.',
  'Sur les images, les logements forment des rangées blanches de deux niveaux avec des panneaux effet bois et des toits plats, et les terrasses du rez-de-chaussée s’ouvrent sur des pelouses derrière des haies taillées. Le dossier indique que les logements sont positionnés pour capter la lumière tout au long de la journée.',
  'Auf den Bildern bilden die Häuser weiße, zweigeschossige Zeilen mit holzähnlichen Verkleidungen und Flachdächern, und die Terrassen im Erdgeschoss öffnen sich zu Rasenflächen hinter geschnittenen Hecken. Das Dossier sagt, die Häuser seien so angeordnet, dass sie das Licht im Tagesverlauf einfangen.',
  'На визуализациях дома образуют белые двухэтажные ряды с панелями под дерево и плоскими крышами, а террасы первого этажа выходят на газоны за подстриженными изгородями. В досье сказано, что дома расположены так, чтобы ловить свет в течение дня.',
  'في الصور تشكّل المنازل صفوفاً بيضاء من طابقين بألواح تحاكي الخشب وأسطح مستوية، وتُفتح شرفات الطابق الأرضي على مروج خلف سياجات مشذّبة. ويذكر الملف التعريفي أن المنازل موضوعة بحيث تلتقط الضوء على مدار اليوم.',
  'In de beelden vormen de woningen witte rijen van twee verdiepingen met houtlookpanelen en platte daken, en de terrassen op de begane grond openen naar gazons achter geknipte hagen. Het dossier zegt dat de woningen zo zijn geplaatst dat ze het licht de hele dag opvangen.',
  'Na wizualizacjach domy tworzą białe, dwukondygnacyjne rzędy z panelami imitującymi drewno i płaskimi dachami, a tarasy na parterze otwierają się na trawniki za przystrzyżonymi żywopłotami. Broszura podaje, że domy są ustawione tak, by łapać światło przez cały dzień.',
  'På bildene danner boligene hvite rader i to etasjer med trelignende paneler og flate tak, og terrassene i første etasje åpner seg mot plener bak klipte hekker. Brosjyren sier at boligene er plassert for å fange lyset gjennom dagen.',
  'På bilderna bildar bostäderna vita rader i två våningar med träliknande paneler och platta tak, och terrasserna på bottenplanet öppnar sig mot gräsmattor bakom klippta häckar. Broschyren säger att bostäderna är placerade för att fånga ljuset under hela dagen.')
a('.architecture.highlights[0]',
  'Dos plantas: las zonas de día y el jardín en la planta baja, los dormitorios en la primera.',
  'Deux niveaux : les pièces de jour et le jardin au rez-de-chaussée, les chambres à l’étage.',
  'Zwei Geschosse: die Wohnbereiche und der Garten im Erdgeschoss, die Schlafzimmer im Obergeschoss.',
  'Два этажа: жилые зоны и сад на первом, спальни на втором.',
  'طابقان: مناطق المعيشة والحديقة في الطابق الأرضي وغرف النوم في الأول.',
  'Twee verdiepingen: de leefruimtes en de tuin op de begane grond, de slaapkamers op de eerste verdieping.',
  'Dwie kondygnacje: strefa dzienna i ogród na parterze, sypialnie na piętrze.',
  'To etasjer: oppholdsrommene og hagen i første etasje, soverommene i andre.',
  'Två våningar: dagytorna och trädgården på bottenplanet, sovrummen på övervåningen.')
a('.architecture.highlights[1]',
  'Una plaza de aparcamiento frontal de unos {N26} {U} dibujada en la parcela de cada una de las tres viviendas de la lista.',
  'Une place de stationnement frontale d’environ {N26} {U} dessinée sur la parcelle de chacun des trois logements de la liste.',
  'Ein frontaler Stellplatz von etwa {N26} {U}, auf dem Grundstück jedes der drei gelisteten Häuser eingezeichnet.',
  'Фронтальное парковочное место около {N26} {U}, нарисованное на участке каждого из трёх домов из списка.',
  'موقف سيارة أمامي بنحو {N26} {U} مرسوم على قطعة كل من المساكن الثلاثة المدرجة.',
  'Een parkeerplaats aan de voorzijde van ongeveer {N26} {U}, getekend op het perceel van elk van de drie genoteerde woningen.',
  'Miejsce parkingowe z przodu o powierzchni około {N26} {U}, narysowane na działce każdego z trzech domów z listy.',
  'En parkeringsplass foran på omtrent {N26} {U}, tegnet inn på tomten til hver av de tre oppførte boligene.',
  'En parkeringsplats framför på cirka {N26} {U}, ritad på tomten för var och en av de tre upptagna bostäderna.')
a('.architecture.highlights[2]',
  'Paneles fotovoltaicos en las cubiertas de las viviendas para autoconsumo y un punto de carga para coche eléctrico preinstalado.',
  'Panneaux photovoltaïques sur les toits des logements pour l’autoconsommation et borne de recharge pour voiture électrique préinstallée.',
  'Photovoltaikmodule auf den Hausdächern zum Eigenverbrauch und ein vorinstallierter Ladepunkt für Elektroautos.',
  'Фотоэлектрические панели на крышах домов для собственного потребления и заранее подготовленная точка зарядки электромобиля.',
  'ألواح كهروضوئية على أسطح المنازل للاستهلاك الذاتي ونقطة شحن مجهّزة مسبقاً للسيارة الكهربائية.',
  'Fotovoltaïsche panelen op de daken van de woningen voor eigen verbruik en een voorbereid laadpunt voor een elektrische auto.',
  'Panele fotowoltaiczne na dachach domów na potrzeby własne i wstępnie przygotowany punkt ładowania samochodu elektrycznego.',
  'Solcellepaneler på hustakene for eget forbruk og et forhåndsinstallert ladepunkt for elbil.',
  'Solcellspaneler på hustaken för egenanvändning och en förberedd laddpunkt för elbil.')
a('.architecture.highlights[3]',
  'Urbanización cerrada con caseta de control de acceso y videoportero en la entrada.',
  'Résidence fermée avec poste de contrôle d’accès et vidéophone à l’entrée.',
  'Geschlossene Anlage mit Zugangskontrollhäuschen und Videosprechanlage am Eingang.',
  'Закрытый комплекс с постом контроля доступа и видеодомофоном у входа.',
  'مجمع مغلق بكشك للتحكم في الدخول وجرس مرئي عند المدخل.',
  'Besloten complex met een toegangscontrolepost en een videofoon bij de ingang.',
  'Zamknięte osiedle z budką kontroli wjazdu i wideodomofonem przy wejściu.',
  'Bevoktet område med adgangskontrollbod og videoport ved inngangen.',
  'Bevakat område med bevakningsbod och videoporttelefon vid entrén.')
a('.lifestyle.headlineHtml',
  'Piscinas, gimnasio <em>y club social</em>', 'Piscines, salle de sport <em>et club social</em>', 'Pools, Fitnessraum <em>und Clubraum</em>',
  'Бассейны, тренажёрный зал <em>и клуб</em>', 'مسابح وصالة رياضية <em>ونادٍ اجتماعي</em>', 'Zwembaden, fitnessruimte <em>en sociale club</em>',
  'Baseny, siłownia <em>i klub</em>', 'Basseng, treningsrom <em>og sosial klubb</em>', 'Pooler, gym <em>och klubblokal</em>')
a('.lifestyle.copy',
  'Tres piscinas, un gimnasio, un club social y una zona chill-out dentro de la urbanización cerrada, con campos de golf, la playa y Málaga al alcance.',
  'Trois piscines, une salle de sport, un club social et un espace chill-out dans la résidence fermée, avec golfs, plage et Málaga à portée.',
  'Drei Pools, ein Fitnessraum, ein Clubraum und ein Chill-out-Bereich in der geschlossenen Anlage, mit Golfplätzen, Strand und Málaga in Reichweite.',
  'Три бассейна, тренажёрный зал, клуб и зона отдыха внутри закрытого комплекса, а гольф-поля, пляж и Малага — рядом.',
  'ثلاثة مسابح وصالة رياضية ونادٍ اجتماعي ومنطقة استرخاء داخل المجمع المغلق، مع ملاعب الغولف والشاطئ ومالقة في المتناول.',
  'Drie zwembaden, een fitnessruimte, een sociale club en een chill-outzone binnen het besloten complex, met golfbanen, het strand en Málaga binnen bereik.',
  'Trzy baseny, siłownia, klub i strefa chill-out w zamkniętym osiedlu, z polami golfowymi, plażą i Málagą w zasięgu.',
  'Tre basseng, et treningsrom, en sosial klubb og en chill-out-sone i det bevoktede området, med golfbaner, stranden og Málaga innen rekkevidde.',
  'Tre pooler, ett gym, en klubblokal och en chill-out-yta inne i det bevakade området, med golfbanor, stranden och Málaga inom räckhåll.')
a('.lifestyle.panels[0][1]',
  'Tres piscinas de cloración salina, una para nadar y otra para relajarse según las describe la memoria, con solárium y zona chill-out, tal como las enumeran el dosier y la memoria.',
  'Trois piscines à chloration saline, une pour nager et une pour se détendre selon le descriptif, avec solarium et espace chill-out, comme les listent le dossier et le descriptif.',
  'Drei Salzwasserpools, einer zum Schwimmen und einer zur Entspannung, wie die Beschreibung sie nennt, mit Solarium und Chill-out-Bereich, so wie Dossier und Beschreibung sie aufführen.',
  'Три бассейна с солевой хлоринацией, один для плавания и один для отдыха, как их описывает спецификация, с солярием и зоной отдыха — так их перечисляют досье и спецификация.',
  'ثلاثة مسابح بالتعقيم الملحي، أحدها للسباحة وآخر للاسترخاء كما تصفها المواصفات، مع سولاريوم ومنطقة استرخاء، كما يذكرها الملف التعريفي والمواصفات.',
  'Drie zoutwaterzwembaden, één om in te zwemmen en één om te ontspannen zoals de beschrijving ze noemt, met een solarium en een chill-outzone, zoals het dossier en de beschrijving ze opsommen.',
  'Trzy baseny z chlorowaniem solnym, jeden do pływania i jeden do relaksu, jak opisuje je specyfikacja, z solarium i strefą chill-out, tak jak wymieniają je broszura i specyfikacja.',
  'Tre saltvannsbasseng, ett for svømming og ett for avslapning slik beskrivelsen presenterer dem, med solterrasse og chill-out-sone, slik brosjyren og beskrivelsen lister dem opp.',
  'Tre saltvattenpooler, en för simning och en för avkoppling som beskrivningen presenterar dem, med solterrass och chill-out-yta, så som broschyren och beskrivningen listar dem.')
a('.lifestyle.panels[1][0]', 'El gimnasio y el club social', 'La salle de sport et le club social', 'Der Fitnessraum und der Clubraum',
  'Тренажёрный зал и клуб', 'الصالة الرياضية والنادي الاجتماعي', 'De fitnessruimte en de sociale club', 'Siłownia i klub',
  'Treningsrommet og den sosiale klubben', 'Gymmet och klubblokalen')
a('.lifestyle.panels[1][1]',
  'Un gimnasio totalmente equipado y un club social que el dosier presenta como lugar de eventos y encuentros con vecinos, familia y amigos, y que en las imágenes se abre a la terraza de la piscina.',
  'Une salle de sport entièrement équipée et un club social que le dossier présente comme un lieu d’événements et de rencontres avec voisins, famille et amis, et qui s’ouvre sur la terrasse de la piscine dans les images.',
  'Ein voll ausgestatteter Fitnessraum und ein Clubraum, den das Dossier als Ort für Veranstaltungen und Treffen mit Nachbarn, Familie und Freunden vorstellt und der sich auf den Bildern zur Poolterrasse öffnet.',
  'Полностью оборудованный тренажёрный зал и клуб, который в досье представлен как место для мероприятий и встреч с соседями, семьёй и друзьями и который на визуализациях открывается на террасу у бассейна.',
  'صالة رياضية مجهّزة بالكامل ونادٍ اجتماعي يقدّمه الملف التعريفي مكاناً للفعاليات واللقاءات مع الجيران والعائلة والأصدقاء، ويُفتح في الصور على شرفة المسبح.',
  'Een volledig uitgeruste fitnessruimte en een sociale club die het dossier presenteert als plek voor evenementen en ontmoetingen met buren, familie en vrienden, en die in de beelden uitkomt op het zwembadterras.',
  'W pełni wyposażona siłownia i klub, który broszura przedstawia jako miejsce wydarzeń i spotkań z sąsiadami, rodziną i przyjaciółmi i który na wizualizacjach otwiera się na taras przy basenie.',
  'Et fullt utstyrt treningsrom og en sosial klubb som brosjyren presenterer som et sted for arrangementer og møter med naboer, familie og venner, og som åpner seg mot bassengterrassen på bildene.',
  'Ett fullt utrustat gym och en klubblokal som broschyren presenterar som en plats för evenemang och möten med grannar, familj och vänner, och som öppnar sig mot poolterrassen på bilderna.')
a('.lifestyle.panels[2][1]',
  'La urbanización da a un espacio natural de frondosos pinos. El mapa del dosier marca cerca campos de golf, un club de pádel, un club hípico, el hipódromo de la Costa del Sol y las playas de La Cala de Mijas y El Ejido.',
  'La résidence fait face à un espace naturel de pins denses. La carte du dossier signale à proximité des golfs, un club de padel, un club équestre, l’hippodrome de la Costa del Sol et les plages de La Cala de Mijas et d’El Ejido.',
  'Die Anlage liegt gegenüber einem Naturraum mit dichtem Kiefernbestand. Die Karte im Dossier verzeichnet in der Nähe Golfplätze, einen Padelclub, einen Reitclub, die Pferderennbahn der Costa del Sol und die Strände von La Cala de Mijas und El Ejido.',
  'Комплекс выходит на природную зону с густым сосновым лесом. На карте в досье поблизости отмечены гольф-поля, падел-клуб, конный клуб, ипподром Коста-дель-Соль и пляжи Ла-Кала-де-Михас и Эль-Эхидо.',
  'يطل المجمع على مساحة طبيعية كثيفة بأشجار الصنوبر. وتشير خريطة الملف التعريفي إلى ملاعب غولف ونادي بادل ونادٍ للفروسية وحلبة سباق كوستا ديل سول وشاطئي لا كالا دي ميخاس والإيخيدو في الجوار.',
  'Het complex kijkt uit op een natuurgebied met dichte dennen. De kaart in het dossier markeert in de buurt golfbanen, een padelclub, een paardensportclub, de renbaan van de Costa del Sol en de stranden van La Cala de Mijas en El Ejido.',
  'Osiedle sąsiaduje z terenem naturalnym z gęstym sosnowym lasem. Mapa w broszurze zaznacza w pobliżu pola golfowe, klub padla, klub jeździecki, tor wyścigów konnych Costa del Sol oraz plaże La Cala de Mijas i El Ejido.',
  'Området vender mot et naturområde med tett furuskog. Kartet i brosjyren markerer golfbaner, en padelklubb, en rideklubb, travbanen Costa del Sol og strendene La Cala de Mijas og El Ejido i nærheten.',
  'Området vetter mot ett naturområde med tät tallskog. Kartan i broschyren markerar golfbanor, en padelklubb, en ridklubb, travbanan Costa del Sol och stränderna La Cala de Mijas och El Ejido i närheten.')
a('.privateViewing.copy',
  'Los documentos que tenemos son imágenes generadas por ordenador y planos de proyecto, así que la visita trata de la ubicación, los planos y el programa.',
  'Les documents que nous détenons sont des images de synthèse et des plans de projet : la visite porte donc sur l’emplacement, les plans et le programme.',
  'Die Unterlagen, die wir haben, sind Renderings und Projektpläne; bei einem Besuch geht es daher um Lage, Pläne und Programm.',
  'Имеющиеся у нас документы — это компьютерные визуализации и проектные планы, поэтому визит посвящён расположению, планировкам и программе.',
  'الوثائق التي لدينا صور مولَّدة بالحاسوب ومخططات مشروع، لذلك تتناول الزيارة الموقع والمخططات والبرنامج.',
  'De documenten die we hebben zijn renders en projectplannen, dus een bezoek gaat over de ligging, de plattegronden en het programma.',
  'Dokumenty, które posiadamy, to wizualizacje i plany projektowe, dlatego wizyta dotyczy lokalizacji, rzutów i programu.',
  'Dokumentene vi har er illustrasjoner og prosjektplaner, så et besøk handler om beliggenheten, plantegningene og programmet.',
  'Handlingarna vi har är renderingar och projektritningar, så ett besök handlar om läget, planritningarna och programmet.')
a('.privateViewing.insights[1][1]',
  'Conducimos con usted a Mijas Costa, La Cala y la playa y medimos el tiempo.',
  'Nous roulons avec vous jusqu’à Mijas Costa, La Cala et la plage, et chronométrons le trajet.',
  'Wir fahren mit Ihnen nach Mijas Costa, La Cala und zum Strand und stoppen die Zeit.',
  'Мы едем с вами в Михас-Коста, Ла-Калу и на пляж и засекаем время.',
  'نقود معكم إلى ميخاس كوستا ولا كالا والشاطئ ونحتسب الوقت.',
  'We rijden met u naar Mijas Costa, La Cala en het strand en nemen de tijd op.',
  'Jedziemy z Państwem do Mijas Costa, La Cali i na plażę i mierzymy czas.',
  'Vi kjører med deg til Mijas Costa, La Cala og stranden og tar tiden.',
  'Vi kör med er till Mijas Costa, La Cala och stranden och tar tid.')
a('.location.headlineHtml',
  'Mijas Costa, <em>junto a los pinos</em>', 'Mijas Costa, <em>au bord des pins</em>', 'Mijas Costa, <em>neben den Kiefern</em>',
  'Михас-Коста, <em>рядом с соснами</em>', 'ميخاس كوستا، <em>بجوار أشجار الصنوبر</em>', 'Mijas Costa, <em>naast de dennen</em>',
  'Mijas Costa, <em>obok sosen</em>', 'Mijas Costa, <em>ved furuene</em>', 'Mijas Costa, <em>vid tallarna</em>')
a('.location.copy',
  'La urbanización está en Mijas Costa, en la costa de Mijas. El mapa del dosier la sitúa junto al hipódromo de la Costa del Sol, entre campos de golf, y da 41 km hasta Málaga y 40 km hasta Marbella. Los documentos no dan dirección, así que el mapa muestra la posición que marca el dosier, no una parcela medida.',
  'La résidence se trouve à Mijas Costa, sur la côte de Mijas. La carte du dossier la place à côté de l’hippodrome de la Costa del Sol, parmi les golfs, et indique 41 km jusqu’à Málaga et 40 km jusqu’à Marbella. Les documents ne donnent pas d’adresse : la carte montre donc la position que marque le dossier, non une parcelle relevée.',
  'Die Anlage liegt in Mijas Costa, an der Küste von Mijas. Die Karte im Dossier verortet sie neben der Pferderennbahn der Costa del Sol, zwischen Golfplätzen, und nennt 41 km bis Málaga und 40 km bis Marbella. Die Unterlagen nennen keine Adresse, daher zeigt die Karte die im Dossier markierte Position, kein vermessenes Grundstück.',
  'Комплекс находится в Михас-Коста, на побережье Михаса. На карте в досье он отмечен рядом с ипподромом Коста-дель-Соль, среди гольф-полей, и указано 41 км до Малаги и 40 км до Марбельи. Адреса в документах нет, поэтому на карте показано положение, отмеченное в досье, а не измеренный участок.',
  'يقع المجمع في ميخاس كوستا على ساحل ميخاس. وتضعه خريطة الملف التعريفي بجوار حلبة سباق كوستا ديل سول، بين ملاعب الغولف، وتذكر 41 كم إلى مالقة و40 كم إلى ماربيا. ولا تذكر الوثائق عنواناً، لذلك تُظهر الخريطة الموضع الذي يحدده الملف التعريفي لا قطعة مقيسة.',
  'Het complex ligt in Mijas Costa, aan de kust van Mijas. De kaart in het dossier plaatst het naast de renbaan van de Costa del Sol, tussen golfbanen, en geeft 41 km naar Málaga en 40 km naar Marbella. De documenten geven geen adres, dus de kaart toont de positie die het dossier aanduidt, geen opgemeten perceel.',
  'Osiedle leży w Mijas Costa, na wybrzeżu Mijas. Mapa w broszurze umieszcza je obok toru wyścigów konnych Costa del Sol, wśród pól golfowych, i podaje 41 km do Málagi oraz 40 km do Marbelli. Dokumenty nie podają adresu, dlatego mapa pokazuje położenie zaznaczone w broszurze, a nie zmierzoną działkę.',
  'Området ligger i Mijas Costa, på kysten av Mijas. Kartet i brosjyren plasserer det ved siden av travbanen Costa del Sol, blant golfbaner, og oppgir 41 km til Málaga og 40 km til Marbella. Dokumentene oppgir ingen adresse, så kartet viser posisjonen brosjyren markerer, ikke en oppmålt tomt.',
  'Området ligger i Mijas Costa, på Mijas kust. Kartan i broschyren placerar det intill travbanan Costa del Sol, bland golfbanor, och anger 41 km till Málaga och 40 km till Marbella. Handlingarna anger ingen adress, så kartan visar den position broschyren markerar, inte en uppmätt tomt.')
a('.location.mapLabelHtml', 'Mijas Costa, <em>Mijas</em>', 'Mijas Costa, <em>Mijas</em>', 'Mijas Costa, <em>Mijas</em>',
  'Михас-Коста, <em>Михас</em>', 'ميخاس كوستا، <em>ميخاس</em>', 'Mijas Costa, <em>Mijas</em>', 'Mijas Costa, <em>Mijas</em>',
  'Mijas Costa, <em>Mijas</em>', 'Mijas Costa, <em>Mijas</em>')
KM = {l: 'km' for l in LOCS}; KM['ru'] = 'км'; KM['ar'] = 'كم'
a('.location.distances[0][1]', *[f'41 {KM[l]}' for l in LOCS])
a('.location.distances[1][1]', *[f'40 {KM[l]}' for l in LOCS])

a('.faq[0][1]',
  'La urbanización tiene 140 adosados de tres o cuatro dormitorios, en dos fases. La lista de precios de la fase 1 recoge tres, todos de tres dormitorios: dos a {E495000} y uno a {E505000}, más IVA.',
  'La résidence compte 140 maisons mitoyennes de trois ou quatre chambres, en deux phases. La liste de prix de la phase 1 en recense trois, toutes de trois chambres : deux à {E495000} et une à {E505000}, hors TVA.',
  'Die Anlage hat 140 Reihenhäuser mit drei oder vier Schlafzimmern in zwei Phasen. Die Preisliste der Phase 1 nennt drei, alle mit drei Schlafzimmern: zwei zu {E495000} und eines zu {E505000}, zuzüglich MwSt.',
  'В комплексе 140 таунхаусов с тремя или четырьмя спальнями в двух фазах. В прайс-листе первой фазы указаны три, все с тремя спальнями: два по {E495000} и один за {E505000}, без НДС.',
  'يضم المجمع 140 منزلاً متلاصقاً بثلاث أو أربع غرف نوم على مرحلتين. وتذكر قائمة أسعار المرحلة الأولى ثلاثة منها، جميعها بثلاث غرف نوم: اثنان بسعر {E495000} وواحد بسعر {E505000}، دون ضريبة القيمة المضافة.',
  'Het complex heeft 140 rijwoningen met drie of vier slaapkamers, in twee fasen. De prijslijst van fase 1 noemt er drie, alle met drie slaapkamers: twee van {E495000} en één van {E505000}, excl. btw.',
  'Osiedle liczy 140 domów szeregowych z trzema lub czterema sypialniami, w dwóch etapach. Cennik etapu 1 wymienia trzy, wszystkie z trzema sypialniami: dwa po {E495000} i jeden za {E505000}, plus VAT.',
  'Området har 140 rekkehus med tre eller fire soverom, i to faser. Prislisten for fase 1 nevner tre, alle med tre soverom: to til {E495000} og én til {E505000}, pluss mva.',
  'Området har 140 radhus med tre eller fyra sovrum, i två faser. Prislistan för fas 1 nämner tre, alla med tre sovrum: två för {E495000} och en för {E505000}, plus IVA.')
a('.faq[1][1]',
  'No. La lista de precios dice que el IVA no está incluido. Se suman el IVA del 10% y el impuesto de timbre del 1,20%, además de los gastos de notaría y registro.',
  'Non. La liste de prix précise que la TVA n’est pas incluse. Viennent s’ajouter la TVA à 10 % et le droit de timbre à 1,20 %, ainsi que les frais de notaire et de registre.',
  'Nein. Die Preisliste sagt, dass die MwSt. nicht enthalten ist. Hinzu kommen 10 % MwSt. und 1,20 % Stempelsteuer sowie Notar- und Grundbuchkosten.',
  'Нет. В прайс-листе сказано, что НДС не включён. Добавляются НДС 10 % и гербовый сбор 1,20 %, а также расходы на нотариуса и регистрацию.',
  'لا. تذكر قائمة الأسعار أن ضريبة القيمة المضافة غير مشمولة. وتُضاف ضريبة القيمة المضافة 10% وضريبة الطابع 1.20%، إضافة إلى رسوم الموثّق والتسجيل العقاري.',
  'Nee. De prijslijst zegt dat btw niet is inbegrepen. Daar komen 10% btw en 1,20% zegelrecht bij, plus notaris- en kadasterkosten.',
  'Nie. Cennik podaje, że VAT nie jest wliczony. Dochodzą VAT w wysokości 10% i opłata skarbowa 1,20% oraz koszty notariusza i rejestru.',
  'Nei. Prislisten sier at mva ikke er inkludert. Det kommer mva på 10 % og dokumentavgift på 1,20 % i tillegg, samt notar- og tinglysingsgebyrer.',
  'Nej. Prislistan anger att IVA inte ingår. IVA på 10 % och stämpelskatt på 1,20 % tillkommer, liksom notarie- och lagfartsavgifter.')
a('.faq[2][1]',
  'La hoja de pago de la fase 1 da la escritura y la entrega de llaves para el tercer trimestre de 2028, y la de la fase 2 para el segundo trimestre de 2029. Ningún documento indica el estado de la licencia ni el inicio de obras, así que Nueva Living pide la fecha por escrito y que el contrato diga qué pasa si se retrasa.',
  'La fiche de paiement de la phase 1 donne l’acte et la remise des clés pour le troisième trimestre 2028, et celle de la phase 2 pour le deuxième trimestre 2029. Aucun document n’indique l’état du permis ni le démarrage des travaux : Nueva Living demande la date par écrit et que le contrat prévoie ce qui se passe en cas de retard.',
  'Der Zahlungsplan der Phase 1 nennt Beurkundung und Schlüsselübergabe für das dritte Quartal 2028, der der Phase 2 für das zweite Quartal 2029. Kein Dokument gibt den Stand der Genehmigung oder einen Baubeginn an; Nueva Living verlangt den Termin schriftlich und dass der Vertrag regelt, was bei einer Verzögerung gilt.',
  'График платежей первой фазы называет нотариальную сделку и передачу ключей на третий квартал 2028 года, второй фазы — на второй квартал 2029 года. Ни в одном документе нет сведений о статусе разрешения или начале работ, поэтому Nueva Living запрашивает дату письменно и требует, чтобы договор определял, что будет при задержке.',
  'يحدد جدول دفع المرحلة الأولى سند الملكية وتسليم المفاتيح في الربع الثالث من 2028، وجدول المرحلة الثانية في الربع الثاني من 2029. ولا توجد في أي وثيقة حالة الرخصة أو بدء الأعمال، لذلك تطلب Nueva Living الموعد كتابةً وأن ينص العقد على ما يحدث عند التأخير.',
  'Het betalingsschema van fase 1 geeft de akte en de sleuteloverdracht voor het derde kwartaal van 2028, dat van fase 2 voor het tweede kwartaal van 2029. Geen enkel document geeft de stand van de vergunning of een start van de werken, dus Nueva Living vraagt de datum schriftelijk op en dat het contract zegt wat er gebeurt bij vertraging.',
  'Harmonogram płatności etapu 1 podaje akt notarialny i przekazanie kluczy na trzeci kwartał 2028 r., a etapu 2 na drugi kwartał 2029 r. Żaden dokument nie podaje statusu pozwolenia ani rozpoczęcia robót, dlatego Nueva Living prosi o termin na piśmie i o to, by umowa określała, co się dzieje w razie opóźnienia.',
  'Betalingsplanen for fase 1 oppgir skjøte og nøkkeloverlevering til tredje kvartal 2028, og planen for fase 2 til andre kvartal 2029. Ingen dokumenter oppgir status for tillatelsen eller byggestart, så Nueva Living ber om datoen skriftlig og om at kontrakten sier hva som skjer ved forsinkelse.',
  'Betalningsplanen för fas 1 anger köpebrev och nyckelöverlämning till tredje kvartalet 2028, och planen för fas 2 till andra kvartalet 2029. Inget dokument anger status för bygglovet eller byggstart, så Nueva Living begär datumet skriftligt och att avtalet anger vad som gäller vid försening.')
a('.faq[3][1]',
  'Una reserva de {E6000} más IVA, luego el 20% más IVA en el contrato privado en 60 días, menos la reserva, el 15% más IVA en tres plazos el 5 de febrero de 2027, el 5 de agosto de 2027 y el 5 de febrero de 2028, y el 65% más IVA en la escritura, en el tercer trimestre de 2028.',
  'Une réservation de {E6000} hors TVA, puis 20 % hors TVA au contrat privé sous 60 jours, moins la réservation, 15 % hors TVA en trois échéances les 5 février 2027, 5 août 2027 et 5 février 2028, et 65 % hors TVA à l’acte, au troisième trimestre 2028.',
  'Eine Reservierung von {E6000} zuzüglich MwSt., dann 20 % zuzüglich MwSt. beim Privatvertrag innerhalb von 60 Tagen, abzüglich der Reservierung, 15 % zuzüglich MwSt. in drei Raten am 5. Februar 2027, 5. August 2027 und 5. Februar 2028 sowie 65 % zuzüglich MwSt. bei der Beurkundung im dritten Quartal 2028.',
  'Бронирование {E6000} без НДС, затем 20 % без НДС при частном договоре в течение 60 дней за вычетом суммы бронирования, 15 % без НДС тремя платежами 5 февраля 2027 года, 5 августа 2027 года и 5 февраля 2028 года и 65 % без НДС при нотариальной сделке в третьем квартале 2028 года.',
  'حجز بمبلغ {E6000} دون ضريبة القيمة المضافة، ثم 20% دونها عند العقد الخاص خلال 60 يوماً ناقص الحجز، و15% دونها على ثلاث دفعات في 5 فبراير 2027 و5 أغسطس 2027 و5 فبراير 2028، و65% دونها عند سند الملكية في الربع الثالث من 2028.',
  'Een reservering van {E6000} excl. btw, daarna 20% excl. btw bij het onderhandse contract binnen 60 dagen, minus de reservering, 15% excl. btw in drie termijnen op 5 februari 2027, 5 augustus 2027 en 5 februari 2028, en 65% excl. btw bij de notariële akte in het derde kwartaal van 2028.',
  'Rezerwacja {E6000} plus VAT, potem 20% plus VAT przy umowie przedwstępnej w ciągu 60 dni, pomniejszone o rezerwację, 15% plus VAT w trzech ratach 5 lutego 2027 r., 5 sierpnia 2027 r. i 5 lutego 2028 r. oraz 65% plus VAT przy akcie notarialnym w trzecim kwartale 2028 r.',
  'En reservasjon på {E6000} pluss mva, deretter 20 % pluss mva ved privatkontrakten innen 60 dager, fratrukket reservasjonen, 15 % pluss mva i tre avdrag 5. februar 2027, 5. august 2027 og 5. februar 2028, og 65 % pluss mva ved skjøtet i tredje kvartal 2028.',
  'En reservation på {E6000} plus IVA, därefter 20 % plus IVA vid det privata avtalet inom 60 dagar, minus reservationen, 15 % plus IVA i tre delbetalningar den 5 februari 2027, den 5 augusti 2027 och den 5 februari 2028, och 65 % plus IVA vid köpebrevet under tredje kvartalet 2028.')
a('.faq[4][0]', '¿Hay lista de precios de la fase 2?', 'Existe-t-il une liste de prix pour la phase 2 ?', 'Gibt es eine Preisliste für Phase 2?',
  'Есть ли прайс-лист второй фазы?', 'هل توجد قائمة أسعار للمرحلة الثانية؟', 'Is er een prijslijst voor fase 2?', 'Czy jest cennik etapu 2?',
  'Finnes det en prisliste for fase 2?', 'Finns det en prislista för fas 2?')
a('.faq[4][1]',
  'Todavía no. La fase 2 tiene una hoja de pago pero no una lista de precios, así que no mostramos ninguna vivienda ni precio de la fase 2. Los añadiremos cuando el promotor publique una.',
  'Pas encore. La phase 2 a une fiche de paiement mais pas de liste de prix : nous n’affichons donc ni logement ni prix de la phase 2. Nous les ajouterons lorsque le promoteur en publiera une.',
  'Noch nicht. Phase 2 hat einen Zahlungsplan, aber keine Preisliste, daher zeigen wir kein Haus und keinen Preis der Phase 2. Wir ergänzen sie, sobald der Bauträger eine veröffentlicht.',
  'Пока нет. У второй фазы есть график платежей, но нет прайс-листа, поэтому мы не показываем ни домов, ни цен второй фазы. Мы добавим их, когда застройщик выпустит прайс-лист.',
  'ليس بعد. للمرحلة الثانية جدول دفع لكن ليس لها قائمة أسعار، لذلك لا نعرض أي مسكن أو سعر من المرحلة الثانية. وسنضيفها عندما يصدر المطوّر قائمة.',
  'Nog niet. Fase 2 heeft een betalingsschema maar geen prijslijst, dus we tonen geen woning of prijs van fase 2. We voegen ze toe zodra de ontwikkelaar er een uitgeeft.',
  'Jeszcze nie. Etap 2 ma harmonogram płatności, ale nie ma cennika, dlatego nie pokazujemy żadnego domu ani ceny z etapu 2. Dodamy je, gdy deweloper wyda cennik.',
  'Ikke ennå. Fase 2 har en betalingsplan, men ingen prisliste, så vi viser ingen bolig eller pris i fase 2. Vi legger dem til når utbyggeren utgir en.',
  'Inte ännu. Fas 2 har en betalningsplan men ingen prislista, så vi visar ingen bostad eller något pris i fas 2. Vi lägger till dem när exploatören ger ut en.')
a('.faq[5][0]', '¿Cada vivienda tiene plaza de aparcamiento?', 'Chaque logement a-t-il une place de stationnement ?', 'Hat jedes Haus einen Stellplatz?',
  'Есть ли у каждого дома парковочное место?', 'هل لكل مسكن موقف سيارة؟', 'Heeft elke woning een parkeerplaats?', 'Czy każdy dom ma miejsce parkingowe?',
  'Har hver bolig en parkeringsplass?', 'Har varje bostad en parkeringsplats?')
a('.faq[5][1]',
  'Los planos dibujan una plaza de aparcamiento frontal de unos {N26} {U} en cada parcela. La lista de precios no dice si está incluida en el precio, así que lo confirmamos por escrito.',
  'Les plans dessinent une place de stationnement frontale d’environ {N26} {U} sur chaque parcelle. La liste de prix ne dit pas si elle est comprise dans le prix, nous le confirmons donc par écrit.',
  'Die Pläne zeichnen auf jedem Grundstück einen frontalen Stellplatz von etwa {N26} {U} ein. Die Preisliste sagt nicht, ob er im Preis enthalten ist, daher bestätigen wir es schriftlich.',
  'На планах на каждом участке нарисовано фронтальное парковочное место около {N26} {U}. В прайс-листе не сказано, включено ли оно в цену, поэтому мы подтверждаем это письменно.',
  'تُظهر المخططات في كل قطعة موقف سيارة أمامياً بنحو {N26} {U}. ولا تذكر قائمة الأسعار ما إذا كان مشمولاً بالسعر، لذلك نؤكد ذلك كتابةً.',
  'De plattegronden tekenen op elk perceel een parkeerplaats aan de voorzijde van ongeveer {N26} {U}. De prijslijst zegt niet of die in de prijs is inbegrepen, dus we bevestigen dat schriftelijk.',
  'Plany rysują na każdej działce miejsce parkingowe z przodu o powierzchni około {N26} {U}. Cennik nie mówi, czy jest ono wliczone w cenę, więc potwierdzamy to na piśmie.',
  'Plantegningene tegner inn en parkeringsplass foran på omtrent {N26} {U} på hver tomt. Prislisten sier ikke om den er inkludert i prisen, så vi bekrefter det skriftlig.',
  'Planritningarna ritar in en parkeringsplats framför på cirka {N26} {U} på varje tomt. Prislistan anger inte om den ingår i priset, så vi bekräftar det skriftligt.')
a('.faq[6][1]',
  'Tres piscinas de cloración salina, un gimnasio totalmente equipado, un club social, una zona chill-out y un solárium, en jardines paisajísticos dentro de una urbanización cerrada con acceso controlado.',
  'Trois piscines à chloration saline, une salle de sport entièrement équipée, un club social, un espace chill-out et un solarium, dans des jardins paysagers à l’intérieur d’une résidence fermée à accès contrôlé.',
  'Drei Salzwasserpools, ein voll ausgestatteter Fitnessraum, ein Clubraum, ein Chill-out-Bereich und ein Solarium, in gestalteten Gärten innerhalb einer geschlossenen Anlage mit Zugangskontrolle.',
  'Три бассейна с солевой хлоринацией, полностью оборудованный тренажёрный зал, клуб, зона отдыха и солярий в ландшафтных садах внутри закрытого комплекса с контролируемым въездом.',
  'ثلاثة مسابح بالتعقيم الملحي وصالة رياضية مجهّزة بالكامل ونادٍ اجتماعي ومنطقة استرخاء وسولاريوم، في حدائق منسّقة داخل مجمع مغلق بمدخل مراقَب.',
  'Drie zoutwaterzwembaden, een volledig uitgeruste fitnessruimte, een sociale club, een chill-outzone en een solarium, in aangelegde tuinen binnen een besloten complex met toegangscontrole.',
  'Trzy baseny z chlorowaniem solnym, w pełni wyposażona siłownia, klub, strefa chill-out i solarium, w zaaranżowanych ogrodach wewnątrz zamkniętego osiedla z kontrolą wjazdu.',
  'Tre saltvannsbasseng, et fullt utstyrt treningsrom, en sosial klubb, en chill-out-sone og en solterrasse, i opparbeidede hager i et bevoktet område med adgangskontroll.',
  'Tre saltvattenpooler, ett fullt utrustat gym, en klubblokal, en chill-out-yta och en solterrass, i anlagda trädgårdar inne i ett bevakat område med kontrollerad infart.')
a('.timeline.items[0][2]',
  'Qué adosado, qué tamaño de jardín y cómo piensa usar la casa.', 'Quelle maison mitoyenne, quelle taille de jardin et comment vous comptez utiliser la maison.',
  'Welches Reihenhaus, wie groß der Garten und wie Sie das Haus nutzen möchten.', 'Какой таунхаус, какого размера сад и как вы планируете использовать дом.',
  'أي منزل متلاصق، وما مساحة الحديقة، وكيف تنوون استخدام المنزل.', 'Welke rijwoning, hoe groot de tuin en hoe u het huis wilt gebruiken.',
  'Który dom szeregowy, jak duży ogród i jak chcą Państwo korzystać z domu.', 'Hvilket rekkehus, hvor stor hage og hvordan du planlegger å bruke huset.',
  'Vilket radhus, hur stor trädgård och hur ni planerar att använda huset.')
a('.enquiry.message',
  'Me gustaría conocer la disponibilidad y los precios actuales de Mijas Olive Townhouses.',
  'Je souhaiterais connaître la disponibilité et les prix actuels de Mijas Olive Townhouses.',
  'Ich hätte gern die aktuelle Verfügbarkeit und die Preise für Mijas Olive Townhouses.',
  'Хочу узнать актуальное наличие и цены на Mijas Olive Townhouses.',
  'أودّ معرفة التوافر والأسعار الحالية لمشروع Mijas Olive Townhouses.',
  'Ik wil graag de actuele beschikbaarheid en prijzen van Mijas Olive Townhouses weten.',
  'Proszę o informacje o aktualnej dostępności i cenach Mijas Olive Townhouses.',
  'Jeg vil gjerne vite gjeldende tilgjengelighet og priser for Mijas Olive Townhouses.',
  'Jag vill gärna få veta aktuell tillgänglighet och aktuella priser för Mijas Olive Townhouses.')
same('Mijas Olive Townhouses - Mijas Costa')
CTX = ['Adosados de tres dormitorios con jardín, Mijas Costa', 'Maisons mitoyennes de trois chambres avec jardin, Mijas Costa',
       'Reihenhäuser mit drei Schlafzimmern und Garten, Mijas Costa', 'Таунхаусы с тремя спальнями и садом, Михас-Коста',
       'منازل متلاصقة بثلاث غرف نوم وحدائق، ميخاس كوستا', 'Rijwoningen met drie slaapkamers en tuin, Mijas Costa',
       'Domy szeregowe z trzema sypialniami i ogrodem, Mijas Costa', 'Rekkehus med tre soverom og hage, Mijas Costa',
       'Radhus med tre sovrum och trädgård, Mijas Costa']
a('.seo.h1Context', *CTX)
a('.seo.h1', *[f'Mijas Olive Townhouses: {c}' for c in CTX])

# ---- write --------------------------------------------------------------------------------------
json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries to', f'{SP}/tr_a.json')
