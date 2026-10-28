# -*- coding: utf-8 -*-
"""The OAK48: the strings the translation memory did not have.

Keyed by the English string, read from the project file by path so that a typo cannot split a key from its
sentence. Tokens: {E375000} money, {N55.09} decimal number, {U} the area unit. The unit sizes, the floorplan
labels and the unit references are built from per-locale templates at the bottom of the file.
Formal address throughout: es usted, fr vous, de Sie, ru vy, ar plural, nl u, pl Pan/Pani/Panstwo, no neutral, sv ni.
    python3 tools/import/k_the_oak48.py <scratch dir>      (writes <dir>/tr_o.json, then run assemble.py)
The seo block is left to the generated locale titles, as Zenith Estepona and Vitta Marina leave it: the seo
strings get placeholders here so that assemble.py will run, and the seo key is removed from the overlays afterwards.
"""
import json, re, sys
SP = sys.argv[1]
SLUG = 'the-oak48'
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
P = json.load(open(f'content/liora-projects/{SLUG}/project.json'))
TM = json.load(open(f'{SP}/tm.json'))


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


def G(path):
    node = P
    for part in re.findall(r'[^.\[\]]+', path):
        node = node[int(part)] if part.isdigit() else node[part]
    assert isinstance(node, str), path
    return node


def A(path, *tr):
    a(G(path), *tr)


# identifiers: the name, the place and the developer's own home codes read the same everywhere
for s in ['The OAK48', 'The OAK48 <em>Estepona</em>']:
    same(s)
for u in P['availability']['units']:
    same(u['reference'])

# ---------------------------------------------------------------- the money lines
a('From EUR 375,000 + VAT', 'Desde {E375000} + IVA', 'À partir de {E375000} + TVA', 'Ab {E375000} + MwSt.',
  'От {E375000} + НДС', 'ابتداءً من {E375000} + ضريبة القيمة المضافة', 'Vanaf {E375000} + btw', 'Od {E375000} + VAT',
  'Fra {E375000} + mva.', 'Från {E375000} + IVA')
a('EUR 375,000 + VAT', '{E375000} + IVA', '{E375000} + TVA', '{E375000} + MwSt.', '{E375000} + НДС',
  '{E375000} + ضريبة القيمة المضافة', '{E375000} + btw', '{E375000} + VAT', '{E375000} + mva.', '{E375000} + IVA')
a('EUR 375,000 - EUR 890,000 + VAT', '{E375000} - {E890000} + IVA', '{E375000} - {E890000} + TVA',
  '{E375000} - {E890000} + MwSt.', '{E375000} - {E890000} + НДС', '{E375000} - {E890000} + ضريبة القيمة المضافة',
  '{E375000} - {E890000} + btw', '{E375000} – {E890000} + VAT', '{E375000} - {E890000} + mva.', '{E375000} - {E890000} + IVA')

# ---------------------------------------------------------------- the descriptions
A('description',
  '15 de 48 apartamentos y áticos de dos y tres dormitorios, en tres bloques cerca del casco antiguo de Estepona, con piscina, gimnasio y sala de coworking comunitarios. No se indica fecha de entrega. Desde {E375000} más IVA.',
  '15 des 48 appartements et penthouses de deux et trois chambres, répartis en trois blocs près de la vieille ville d’Estepona, avec piscine, salle de sport et espace de coworking communs. Aucune date de livraison n’est indiquée. À partir de {E375000} hors TVA.',
  '15 von 48 Wohnungen und Penthäusern mit zwei und drei Schlafzimmern in drei Blöcken nahe der Altstadt von Estepona, mit gemeinsamem Pool, Fitnessraum und Coworking-Raum. Ein Übergabetermin ist nicht angegeben. Ab {E375000} zuzüglich MwSt.',
  '15 из 48 квартир и пентхаусов с двумя и тремя спальнями в трёх корпусах рядом со старым городом Эстепоны: общий бассейн, тренажёрный зал и коворкинг. Срок сдачи не указан. От {E375000} без НДС.',
  '15 من أصل 48 شقة وبنتهاوس بغرفتين أو ثلاث غرف نوم في ثلاثة مبانٍ قرب البلدة القديمة في إستيبونا، مع مسبح مشترك وصالة رياضية وقاعة عمل مشتركة. لم يُذكر موعد تسليم. ابتداءً من {E375000} دون ضريبة القيمة المضافة.',
  '15 van de 48 appartementen en penthouses met twee en drie slaapkamers in drie blokken vlak bij de oude stad van Estepona, met een gedeeld zwembad, fitnessruimte en coworkingruimte. Er wordt geen opleveringsdatum genoemd. Vanaf {E375000} excl. btw.',
  '15 z 48 mieszkań i penthouse’ów z dwiema i trzema sypialniami w trzech blokach w pobliżu starego miasta w Esteponie, ze wspólnym basenem, siłownią i salą coworkingową. Termin oddania nie jest podany. Od {E375000} plus VAT.',
  '15 av 48 leiligheter og toppleiligheter med to og tre soverom i tre hus nær gamlebyen i Estepona, med felles basseng, treningsrom og coworking-rom. Ingen overleveringsdato er oppgitt. Fra {E375000} pluss mva.',
  '15 av 48 lägenheter och takvåningar med två och tre sovrum i tre hus nära gamla stan i Estepona, med gemensam pool, gemensamt gym och gemensamt coworking-rum. Inget tillträdesdatum anges. Från {E375000} plus IVA.')
A('seoDescription',
  '15 de 48 apartamentos y áticos de dos y tres dormitorios en Estepona, cerca del casco antiguo, con piscina, gimnasio y coworking, desde {E375000} más IVA.',
  '15 des 48 appartements et penthouses de deux et trois chambres à Estepona, près de la vieille ville, avec piscine, salle de sport et coworking, à partir de {E375000} hors TVA.',
  '15 von 48 Wohnungen und Penthäusern mit zwei und drei Schlafzimmern in Estepona, nahe der Altstadt, mit Pool, Fitnessraum und Coworking, ab {E375000} zuzüglich MwSt.',
  '15 из 48 квартир и пентхаусов с двумя и тремя спальнями в Эстепоне, рядом со старым городом, с бассейном, тренажёрным залом и коворкингом, от {E375000} без НДС.',
  '15 من أصل 48 شقة وبنتهاوس بغرفتين أو ثلاث غرف نوم في إستيبونا، قرب البلدة القديمة، مع مسبح وصالة رياضية وقاعة عمل مشتركة، ابتداءً من {E375000} دون ضريبة القيمة المضافة.',
  '15 van de 48 appartementen en penthouses met twee en drie slaapkamers in Estepona, vlak bij de oude stad, met zwembad, fitnessruimte en coworking, vanaf {E375000} excl. btw.',
  '15 z 48 mieszkań i penthouse’ów z dwiema i trzema sypialniami w Esteponie, w pobliżu starego miasta, z basenem, siłownią i coworkingiem, od {E375000} plus VAT.',
  '15 av 48 leiligheter og toppleiligheter med to og tre soverom i Estepona, nær gamlebyen, med basseng, treningsrom og coworking, fra {E375000} pluss mva.',
  '15 av 48 lägenheter och takvåningar med två och tre sovrum i Estepona, nära gamla stan, med pool, gym och coworking, från {E375000} plus IVA.')
A('twitterDescription',
  'Apartamentos y áticos de dos y tres dormitorios cerca del casco antiguo de Estepona, desde {E375000} más IVA.',
  'Appartements et penthouses de deux et trois chambres près de la vieille ville d’Estepona, à partir de {E375000} hors TVA.',
  'Wohnungen und Penthäuser mit zwei und drei Schlafzimmern nahe der Altstadt von Estepona, ab {E375000} zuzüglich MwSt.',
  'Квартиры и пентхаусы с двумя и тремя спальнями рядом со старым городом Эстепоны, от {E375000} без НДС.',
  'شقق وبنتهاوس بغرفتين أو ثلاث غرف نوم قرب البلدة القديمة في إستيبونا، ابتداءً من {E375000} دون ضريبة القيمة المضافة.',
  'Appartementen en penthouses met twee en drie slaapkamers vlak bij de oude stad van Estepona, vanaf {E375000} excl. btw.',
  'Mieszkania i penthouse’y z dwiema i trzema sypialniami w pobliżu starego miasta w Esteponie, od {E375000} plus VAT.',
  'Leiligheter og toppleiligheter med to og tre soverom nær gamlebyen i Estepona, fra {E375000} pluss mva.',
  'Lägenheter och takvåningar med två och tre sovrum nära gamla stan i Estepona, från {E375000} plus IVA.')
A('card.description',
  '15 de 48 apartamentos y áticos de dos y tres dormitorios en tres bloques en Estepona, con piscina comunitaria, gimnasio y sala de coworking.',
  '15 des 48 appartements et penthouses de deux et trois chambres répartis en trois blocs à Estepona, avec piscine commune, salle de sport et espace de coworking.',
  '15 von 48 Wohnungen und Penthäusern mit zwei und drei Schlafzimmern in drei Blöcken in Estepona, mit gemeinsamem Pool, Fitnessraum und Coworking-Raum.',
  '15 из 48 квартир и пентхаусов с двумя и тремя спальнями в трёх корпусах в Эстепоне: общий бассейн, тренажёрный зал и коворкинг.',
  '15 من أصل 48 شقة وبنتهاوس بغرفتين أو ثلاث غرف نوم في ثلاثة مبانٍ في إستيبونا، مع مسبح مشترك وصالة رياضية وقاعة عمل مشتركة.',
  '15 van de 48 appartementen en penthouses met twee en drie slaapkamers in drie blokken in Estepona, met een gedeeld zwembad, fitnessruimte en coworkingruimte.',
  '15 z 48 mieszkań i penthouse’ów z dwiema i trzema sypialniami w trzech blokach w Esteponie, ze wspólnym basenem, siłownią i salą coworkingową.',
  '15 av 48 leiligheter og toppleiligheter med to og tre soverom i tre hus i Estepona, med felles basseng, treningsrom og coworking-rom.',
  '15 av 48 lägenheter och takvåningar med två och tre sovrum i tre hus i Estepona, med gemensam pool, gemensamt gym och gemensamt coworking-rum.')

# ---------------------------------------------------------------- image alts and captions
A('images.hero.alt',
  'Vista generada por ordenador de un bloque de apartamentos de cuatro plantas con terrazas curvas tras celosías verticales, visto desde la calle',
  'Vue de synthèse d’un immeuble de quatre niveaux aux terrasses courbes derrière des claustras verticaux, vu depuis la rue',
  'Computergenerierte Ansicht eines vierstöckigen Wohnhauses mit geschwungenen Terrassen hinter senkrechten Lamellenblenden, von der Straße aus gesehen',
  'Компьютерная визуализация четырёхэтажного жилого дома с изогнутыми террасами за вертикальными рейками, вид с улицы',
  'منظر مُولَّد بالحاسوب لمبنى سكني من أربعة طوابق بتراسات منحنية خلف شرائح رأسية، من جهة الشارع',
  'Computergegenereerd beeld van een appartementengebouw van vier verdiepingen met gebogen terrassen achter verticale lamellen, gezien vanaf de straat',
  'Wizualizacja komputerowa czterokondygnacyjnego budynku z zaokrąglonymi tarasami za pionowymi listwami, widok od strony ulicy',
  'Datagenerert bilde av en leilighetsblokk i fire etasjer med buede terrasser bak vertikale lameller, sett fra gaten',
  'Datorgenererad bild av ett flerbostadshus i fyra våningar med böjda terrasser bakom vertikala lameller, sett från gatan')
A('images.architecture.alt',
  'Vista generada por ordenador de la esquina del edificio, con terrazas curvas tras lamas verticales y paneles imitación madera, palmeras y césped',
  'Vue de synthèse de l’angle du bâtiment, avec terrasses courbes derrière des lames verticales et des panneaux imitation bois, des palmiers et une pelouse',
  'Computergenerierte Ansicht der Gebäudeecke mit geschwungenen Terrassen hinter senkrechten Lamellen und Paneelen in Holzoptik, Palmen und Rasen',
  'Компьютерная визуализация угла здания с изогнутыми террасами за вертикальными рейками и панелями под дерево, пальмами и газоном',
  'منظر مُولَّد بالحاسوب لزاوية المبنى بتراسات منحنية خلف شرائح رأسية وألواح بمظهر الخشب، مع نخيل ومرج',
  'Computergegenereerd beeld van de hoek van het gebouw, met gebogen terrassen achter verticale latten en panelen in houtlook, palmen en een gazon',
  'Wizualizacja komputerowa narożnika budynku z zaokrąglonymi tarasami za pionowymi listwami i panelami imitującymi drewno, palmami i trawnikiem',
  'Datagenerert bilde av hjørnet av bygningen, med buede terrasser bak vertikale lameller og paneler i trelook, palmer og en plen',
  'Datorgenererad bild av byggnadens hörn, med böjda terrasser bakom vertikala lameller och paneler i trälook, palmer och en gräsmatta')
A('images.lifestyle.alt',
  'Solárium de cubierta generado por ordenador, con piscina, tumbonas y un conjunto de comedor, con vistas a la ciudad y al mar',
  'Solarium en toiture de synthèse, avec piscine, transats et ensemble repas, avec vue sur la ville et la mer',
  'Computergeneriertes Dach-Solarium mit Pool, Sonnenliegen und einer Essgruppe, mit Blick über die Stadt auf das Meer',
  'Компьютерная визуализация солярия на крыше с бассейном, шезлонгами и обеденной группой, вид на город и море',
  'سولاريوم على السطح مُولَّد بالحاسوب بمسبح وكراسي استلقاء ومجموعة طعام، بإطلالة على المدينة والبحر',
  'Computergegenereerd dakterras-solarium met een zwembad, ligbedden en een eethoek, met uitzicht over de stad naar de zee',
  'Komputerowa wizualizacja solarium na dachu z basenem, leżakami i zestawem jadalnianym, z widokiem na miasto i morze',
  'Datagenerert solterrasse på taket med basseng, solsenger og en spisegruppe, med utsikt over byen mot havet',
  'Datorgenererad solterrass på taket med pool, solstolar och en matgrupp, med utsikt över staden mot havet')
A('images.privateViewing.alt',
  'Dormitorio principal generado por ordenador, con cama tapizada gris, pared revestida de madera con almacenaje empotrado y puerta acristalada a una terraza',
  'Chambre principale de synthèse avec lit tapissé gris, mur habillé de bois avec rangements intégrés et porte vitrée donnant sur une terrasse',
  'Computergeneriertes Hauptschlafzimmer mit grau gepolstertem Bett, einer holzvertäfelten Wand mit Einbauschränken und einer verglasten Tür zur Terrasse',
  'Компьютерная визуализация главной спальни с серой мягкой кроватью, стеной с деревянной отделкой и встроенными системами хранения и остеклённой дверью на террасу',
  'غرفة النوم الرئيسية مُولَّدة بالحاسوب بسرير مكسو باللون الرمادي وجدار مكسو بالخشب مع تخزين مدمج وباب زجاجي إلى تراس',
  'Computergegenereerde hoofdslaapkamer met een grijs gestoffeerd bed, een met hout bekleedde wand met inbouwkasten en een glazen deur naar een terras',
  'Komputerowa wizualizacja głównej sypialni z szarym tapicerowanym łóżkiem, ścianą wykończoną drewnem z wbudowanymi szafami i przeszklonymi drzwiami na taras',
  'Datagenerert hovedsoverom med grått polstret seng, en trepanelt vegg med innebygd oppbevaring og en glassdør ut til en terrasse',
  'Datorgenererat huvudsovrum med grå klädd säng, en träpanelad vägg med inbyggd förvaring och en glasdörr till en terrass')
A('media.copy',
  'Vistas generadas por ordenador del edificio, de las terrazas de la cubierta y de los interiores, y planos de las 15 viviendas a la venta.',
  'Vues de synthèse du bâtiment, des terrasses en toiture et des intérieurs, et plans des 15 logements annoncés.',
  'Computergenerierte Ansichten des Gebäudes, der Dachterrassen und der Innenräume sowie die Grundrisse der 15 gelisteten Wohnungen.',
  'Компьютерные визуализации здания, террас на крыше и интерьеров, а также планировки 15 квартир, находящихся в продаже.',
  'مناظر مُولَّدة بالحاسوب للمبنى وتراسات السطح والمساحات الداخلية، ومخططات المساكن الخمسة عشر المعروضة.',
  'Computergegenereerde beelden van het gebouw, de dakterrassen en de interieurs, en de plattegronden van de 15 aangeboden woningen.',
  'Komputerowe wizualizacje budynku, tarasów na dachu i wnętrz oraz rzuty 15 oferowanych mieszkań.',
  'Datagenererte bilder av bygningen, takterrassene og interiørene, og plantegningene til de 15 annonserte boligene.',
  'Datorgenererade bilder av byggnaden, takterrasserna och interiörerna samt planritningarna för de 15 listade bostäderna.')
A('media.note',
  'Todas las vistas son ilustraciones generadas por ordenador, no fotografías del edificio terminado, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. El promotor indica que sus imágenes 3D de las fachadas, las zonas comunes y los demás espacios son orientativas y pueden cambiar en los proyectos técnicos. Los planos son los planos de venta del promotor: no tienen carácter contractual, los nombres de las estancias están en español y, en cada ático, la planta de cubierta aparece debajo de la planta de la vivienda.',
  'Toutes les vues sont des illustrations de synthèse, et non des photographies du bâtiment terminé ; le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Le promoteur précise que ses images 3D des façades, des parties communes et des autres espaces sont indicatives et peuvent évoluer dans les projets techniques. Les plans sont les plans de vente du promoteur : ils n’ont pas valeur contractuelle, le nom des pièces y est en espagnol et, pour chaque penthouse, le niveau de la toiture figure sous l’étage.',
  'Alle Ansichten sind computergenerierte Illustrationen und keine Fotos des fertigen Gebäudes; die darin gezeigten Möbel und die Dekoration dienen der Veranschaulichung und sind nicht enthalten. Der Bauträger weist darauf hin, dass seine 3D-Darstellungen der Fassaden, der Gemeinschaftsbereiche und der übrigen Räume unverbindlich sind und sich in den technischen Projekten noch ändern können. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen sind auf Spanisch, und bei jedem Penthouse ist die Dachebene unter dem Wohngeschoss dargestellt.',
  'Все изображения — компьютерные иллюстрации, а не фотографии готового здания; мебель и декор на них приведены для иллюстрации и в стоимость не входят. Застройщик указывает, что его 3D-изображения фасадов, общих зон и других пространств носят ориентировочный характер и могут измениться в технических проектах. Планировки — это продажные планы застройщика: они не имеют договорной силы, названия помещений на них даны по-испански, а уровень крыши каждого пентхауса показан под основным этажом.',
  'جميع المناظر رسوم توضيحية مُولَّدة بالحاسوب وليست صورًا فوتوغرافية للمبنى بعد اكتماله، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. ويذكر المطوّر أن صوره ثلاثية الأبعاد للواجهات والمرافق المشتركة والمساحات الأخرى استرشادية وقد تتغير في المشاريع التقنية. المخططات هي مخططات البيع الخاصة بالمطوّر: وهي غير ملزمة تعاقديًا، وأسماء الغرف عليها بالإسبانية، ويظهر مستوى السطح لكل بنتهاوس أسفل الطابق.',
  'Alle beelden zijn computergegenereerde illustraties en geen foto’s van het afgewerkte gebouw; de meubels en de inrichting erop zijn illustratief en niet inbegrepen. De ontwikkelaar geeft aan dat zijn 3D-beelden van de gevels, de gemeenschappelijke ruimtes en de overige ruimtes indicatief zijn en in de technische projecten kunnen wijzigen. De plattegronden zijn de verkoopplattegronden van de ontwikkelaar: ze zijn niet contractueel, de ruimtenamen erop zijn in het Spaans en bij elk penthouse staat het dakniveau onder de woonverdieping.',
  'Wszystkie wizualizacje są ilustracjami komputerowymi, a nie zdjęciami gotowego budynku; widoczne na nich meble i wystrój mają charakter poglądowy i nie są wliczone w cenę. Deweloper zaznacza, że jego obrazy 3D elewacji, części wspólnych i pozostałych przestrzeni są orientacyjne i mogą się zmienić w projektach technicznych. Rzuty to plany sprzedażowe dewelopera: nie mają charakteru umownego, nazwy pomieszczeń są po hiszpańsku, a przy każdym penthousie poziom dachu pokazano pod kondygnacją mieszkalną.',
  'Alle bildene er datagenererte illustrasjoner, ikke fotografier av den ferdige bygningen, og møblene og innredningen på dem er illustrative og ikke inkludert. Utbyggeren sier at 3D-bildene av fasadene, fellesarealene og de øvrige rommene er veiledende og kan endres i de tekniske prosjektene. Plantegningene er utbyggerens salgstegninger: de er ikke kontraktsfestet, romnavnene på dem er på spansk, og for hver toppleilighet vises takplanet under boligplanet.',
  'Alla bilder är datorgenererade illustrationer, inte fotografier av den färdiga byggnaden, och möblerna och inredningen i dem är illustrativa och ingår inte. Exploatören anger att dess 3D-bilder av fasaderna, de gemensamma ytorna och övriga utrymmen är vägledande och kan ändras i de tekniska projekten. Planritningarna är exploatörens säljplaner: de är inte avtalsgrundande, rummens namn på dem är på spanska, och för varje takvåning visas takplanet under bostadsplanet.')
A('media.items[0].caption', 'La esquina del edificio desde la calle', 'L’angle du bâtiment vu de la rue', 'Die Gebäudeecke von der Straße aus',
  'Угол здания со стороны улицы', 'زاوية المبنى من جهة الشارع', 'De hoek van het gebouw vanaf de straat', 'Narożnik budynku od strony ulicy',
  'Hjørnet av bygningen sett fra gaten', 'Byggnadens hörn sett från gatan')
A('media.items[1].caption', 'Terrazas curvas y celosías de lamas', 'Terrasses courbes et claustras à lames', 'Geschwungene Terrassen und Lamellenblenden',
  'Изогнутые террасы и рейки', 'تراسات منحنية وشرائح رأسية', 'Gebogen terrassen en lamellen', 'Zaokrąglone tarasy i listwy',
  'Buede terrasser og lameller', 'Böjda terrasser och lameller')
A('media.items[2].alt',
  'Vista generada por ordenador de las terrazas escalonadas con lamas sobre un jardín con piscina comunitaria y tumbonas',
  'Vue de synthèse des terrasses en gradins à lames au-dessus d’un jardin avec piscine commune et transats',
  'Computergenerierte Ansicht der gestaffelten Terrassen mit Lamellen über einem Garten mit Gemeinschaftspool und Sonnenliegen',
  'Компьютерная визуализация террас уступами с рейками над садом с общим бассейном и шезлонгами',
  'منظر مُولَّد بالحاسوب لتراسات متدرجة بشرائح رأسية فوق حديقة فيها مسبح مشترك وكراسي استلقاء',
  'Computergegenereerd beeld van de getrapte terrassen met lamellen boven een tuin met gemeenschappelijk zwembad en ligbedden',
  'Wizualizacja komputerowa tarasów schodkowych z listwami nad ogrodem ze wspólnym basenem i leżakami',
  'Datagenerert bilde av trappetrinnsterrassene med lameller over en hage med felles basseng og solsenger',
  'Datorgenererad bild av de trappstegsformade terrasserna med lameller ovanför en trädgård med gemensam pool och solstolar')
A('media.items[2].caption', 'Las terrazas sobre el jardín y la piscina', 'Les terrasses au-dessus du jardin et de la piscine',
  'Die Terrassen über dem Garten und dem Pool', 'Террасы над садом и бассейном', 'التراسات فوق الحديقة والمسبح',
  'De terrassen boven de tuin en het zwembad', 'Tarasy nad ogrodem i basenem', 'Terrassene over hagen og bassenget',
  'Terrasserna ovanför trädgården och poolen')
A('media.items[3].alt',
  'Vista aérea generada por ordenador del edificio, con terrazas, solariums y pequeñas piscinas en la última planta, y la piscina comunitaria y el césped a su lado',
  'Vue aérienne de synthèse du bâtiment, avec terrasses, solariums et petits bassins au dernier niveau, et la piscine commune et la pelouse à côté',
  'Computergenerierte Luftansicht des Gebäudes mit Dachterrassen, Solarien und kleinen Pools auf der obersten Ebene sowie dem Gemeinschaftspool und dem Rasen daneben',
  'Компьютерная аэровизуализация здания с террасами, солярием и небольшими бассейнами на верхнем уровне, а рядом — общий бассейн и газон',
  'منظر جوي مُولَّد بالحاسوب للمبنى مع تراسات وسولاريوم وأحواض سباحة صغيرة في الطابق العلوي، والمسبح المشترك والمرج بجانبه',
  'Computergegenereerd luchtbeeld van het gebouw met dakterrassen, solariums en kleine zwembaden op het bovenste niveau, en daarnaast het gemeenschappelijke zwembad en het gazon',
  'Komputerowa wizualizacja lotnicza budynku z tarasami, solariami i małymi basenami na najwyższym poziomie oraz wspólnym basenem i trawnikiem obok',
  'Datagenerert flybilde av bygningen med takterrasser, solterrasser og små bassenger på øverste nivå, og det felles bassenget og plenen ved siden av',
  'Datorgenererad flygbild av byggnaden med takterrasser, solterrasser och små pooler på översta nivån, och den gemensamma poolen och gräsmattan intill')
A('media.items[3].caption', 'La cubierta vista desde arriba', 'Le niveau de la toiture vu d’en haut', 'Die Dachebene von oben',
  'Уровень крыши сверху', 'مستوى السطح من الأعلى', 'Het dakniveau van boven', 'Poziom dachu z góry', 'Takplanet sett ovenfra', 'Takplanet sett uppifrån')
A('media.items[4].alt',
  'Terraza de planta baja generada por ordenador, con mesa de comedor y sofá, que da a un macizo de arbustos y a un césped',
  'Terrasse de rez-de-chaussée de synthèse, avec table à manger et canapé, ouverte sur une haie d’arbustes et une pelouse',
  'Computergenerierte Erdgeschossterrasse mit Esstisch und Sofa, die sich zu einem Strauchbeet und einem Rasen öffnet',
  'Компьютерная визуализация террасы на первом этаже с обеденным столом и диваном, выходящей на кустарниковую границу и газон',
  'تراس في الطابق الأرضي مُولَّد بالحاسوب بطاولة طعام وأريكة، يطل على حاجز من الشجيرات ومرج',
  'Computergegenereerd terras op de begane grond met een eettafel en een bank, dat uitkomt op een struikenborder en een gazon',
  'Komputerowa wizualizacja tarasu na parterze ze stołem jadalnianym i sofą, otwartego na rabatę z krzewami i trawnik',
  'Datagenerert terrasse i første etasje med spisebord og sofa, som åpner mot en kant av busker og en plen',
  'Datorgenererad terrass på bottenvåningen med matbord och soffa, som öppnar sig mot en buskrabatt och en gräsmatta')
A('media.items[5].caption', 'Un solárium de ático con piscina', 'Un solarium de penthouse avec piscine', 'Ein Penthouse-Solarium mit Pool',
  'Солярий пентхауса с бассейном', 'سولاريوم بنتهاوس مع مسبح', 'Een penthouse-solarium met zwembad', 'Solarium penthouse’u z basenem',
  'Solterrasse på en toppleilighet med basseng', 'En solterrass på en takvåning med pool')
A('media.items[6].alt',
  'Terraza de cubierta generada por ordenador, con mesa de comedor, sofá rinconero, tumbonas y una pequeña piscina, mirando hacia las montañas',
  'Terrasse en toiture de synthèse, avec table à manger, canapé d’angle, transats et petit bassin, tournée vers les montagnes',
  'Computergenerierte Dachterrasse mit Esstisch, Ecksofa, Sonnenliegen und einem kleinen Pool, mit Blick auf die Berge',
  'Компьютерная визуализация террасы на крыше с обеденным столом, угловым диваном, шезлонгами и небольшим бассейном, вид на горы',
  'تراس سطح مُولَّد بالحاسوب بطاولة طعام وأريكة زاوية وكراسي استلقاء وحوض سباحة صغير، بإطلالة نحو الجبال',
  'Computergegenereerd dakterras met een eettafel, een hoekbank, ligbedden en een klein zwembad, met uitzicht op de bergen',
  'Komputerowa wizualizacja tarasu na dachu ze stołem jadalnianym, narożną sofą, leżakami i małym basenem, z widokiem na góry',
  'Datagenerert takterrasse med spisebord, hjørnesofa, solsenger og et lite basseng, med utsikt mot fjellene',
  'Datorgenererad takterrass med matbord, hörnsoffa, solstolar och en liten pool, med utsikt mot bergen')
A('media.items[6].caption', 'Una terraza de cubierta con vistas a las montañas', 'Une terrasse en toiture tournée vers les montagnes',
  'Eine Dachterrasse mit Blick auf die Berge', 'Терраса на крыше с видом на горы', 'تراس سطح بإطلالة نحو الجبال',
  'Een dakterras met uitzicht op de bergen', 'Taras na dachu z widokiem na góry', 'En takterrasse med utsikt mot fjellene',
  'En takterrass med utsikt mot bergen')
A('media.items[7].alt',
  'Terraza de cubierta generada por ordenador, con suelo de madera, tumbonas, un sofá, sillones y jardineras junto a una celosía de lamas',
  'Terrasse en toiture de synthèse, avec platelage en bois, transats, canapé, fauteuils et jardinières à côté d’un claustra à lames',
  'Computergenerierte Dachterrasse mit Holzdeck, Sonnenliegen, einem Sofa, Sesseln und Pflanzgefäßen neben einer Lamellenwand',
  'Компьютерная визуализация террасы на крыше с деревянным настилом, шезлонгами, диваном, креслами и кашпо рядом с экраном из реек',
  'تراس سطح مُولَّد بالحاسوب بأرضية خشبية وكراسي استلقاء وأريكة ومقاعد وأحواض نباتات بجانب حاجز من الشرائح',
  'Computergegenereerd dakterras met een houten vlonder, ligbedden, een bank, fauteuils en plantenbakken naast een lamellenscherm',
  'Komputerowa wizualizacja tarasu na dachu z drewnianym deskowaniem, leżakami, sofą, fotelami i donicami przy ekranie z listew',
  'Datagenerert takterrasse med tregulv, solsenger, en sofa, lenestoler og plantekasser ved en lamellvegg',
  'Datorgenererad takterrass med trädäck, solstolar, en soffa, fåtöljer och planteringskärl intill en lamellvägg')
A('media.items[7].caption', 'Una terraza de cubierta con zona de estar', 'Une terrasse en toiture avec coin salon',
  'Eine Dachterrasse mit Loungebereich', 'Терраса на крыше с зоной отдыха', 'تراس سطح مع ركن جلوس',
  'Een dakterras met loungehoek', 'Taras na dachu ze strefą wypoczynku', 'En takterrasse med loungeområde', 'En takterrass med loungeyta')
A('media.items[8].alt',
  'Salón de planta abierta generado por ordenador, con sofá crema, mesa de comedor de madera, pared multimedia de lamas y puerta corredera de cristal a la terraza',
  'Séjour ouvert de synthèse, avec canapé crème, table à manger en bois, mur multimédia à lames et baie vitrée coulissante vers la terrasse',
  'Computergenerierter offener Wohnbereich mit cremefarbenem Sofa, Esstisch aus Holz, Medienwand mit Lamellen und einer verglasten Schiebetür zur Terrasse',
  'Компьютерная визуализация гостиной открытой планировки с кремовым диваном, деревянным обеденным столом, медиастеной из реек и стеклянной раздвижной дверью на террасу',
  'غرفة معيشة مفتوحة مُولَّدة بالحاسوب بأريكة بلون الكريم وطاولة طعام خشبية وجدار وسائط من الشرائح وباب زجاجي منزلق إلى التراس',
  'Computergegenereerde open woonkamer met een crèmekleurige bank, een houten eettafel, een mediawand met latten en een glazen schuifdeur naar het terras',
  'Komputerowa wizualizacja otwartego salonu z kremową sofą, drewnianym stołem jadalnianym, ścianą multimedialną z listew i przesuwnymi szklanymi drzwiami na taras',
  'Datagenerert åpen stue med kremfarget sofa, spisebord i tre, medievegg med lameller og en skyvedør i glass ut til terrassen',
  'Datorgenererat öppet vardagsrum med krämfärgad soffa, matbord i trä, mediavägg med lameller och en glasskjutdörr till terrassen')
A('media.items[9].alt',
  'Salón de ático generado por ordenador, con sofá rinconero, isla de cocina con taburetes y mesa de comedor bajo una escalera con barandilla de barrotes metálicos verticales',
  'Séjour de penthouse de synthèse, avec canapé d’angle, îlot de cuisine avec tabourets et table à manger sous un escalier à garde-corps à barreaux métalliques verticaux',
  'Computergenerierter Penthouse-Wohnbereich mit Ecksofa, Kücheninsel mit Hockern und einem Esstisch unter einer Treppe mit senkrechten Metallstäben im Geländer',
  'Компьютерная визуализация гостиной пентхауса с угловым диваном, кухонным островом с барными стульями и обеденным столом под лестницей с вертикальными металлическими балясинами',
  'غرفة معيشة بنتهاوس مُولَّدة بالحاسوب بأريكة زاوية وجزيرة مطبخ مع مقاعد عالية وطاولة طعام تحت درج بقضبان معدنية رأسية',
  'Computergegenereerde penthouse-woonkamer met een hoekbank, een keukeneiland met krukken en een eettafel onder een trap met verticale metalen spijlen',
  'Komputerowa wizualizacja salonu w penthousie z narożną sofą, wyspą kuchenną z hokerami i stołem jadalnianym pod schodami z pionowymi metalowymi balustradami',
  'Datagenerert stue i en toppleilighet med hjørnesofa, kjøkkenøy med krakker og et spisebord under en trapp med vertikale metallspiler',
  'Datorgenererat vardagsrum i en takvåning med hörnsoffa, köksö med pallar och ett matbord under en trappa med vertikala metallspjälor')
A('media.items[10].alt',
  'Cocina generada por ordenador con muebles altos blancos, muebles bajos de madera, una isla con tres taburetes y una puerta corredera a la terraza',
  'Cuisine de synthèse avec éléments hauts blancs, éléments bas en bois, un îlot avec trois tabourets et une porte coulissante vers la terrasse',
  'Computergenerierte Küche mit weißen Oberschränken, Unterschränken aus Holz, einer Insel mit drei Hockern und einer Schiebetür zur Terrasse',
  'Компьютерная визуализация кухни с белыми навесными шкафами, деревянными нижними шкафами, островом с тремя барными стульями и раздвижной дверью на террасу',
  'مطبخ مُولَّد بالحاسوب بخزائن علوية بيضاء وخزائن سفلية خشبية وجزيرة مع ثلاثة مقاعد عالية وباب منزلق إلى التراس',
  'Computergegenereerde keuken met witte bovenkasten, houten onderkasten, een eiland met drie krukken en een schuifdeur naar een terras',
  'Komputerowa wizualizacja kuchni z białymi szafkami wiszącymi, drewnianymi szafkami dolnymi, wyspą z trzema hokerami i przesuwnymi drzwiami na taras',
  'Datagenerert kjøkken med hvite overskap, underskap i tre, en øy med tre krakker og en skyvedør ut til en terrasse',
  'Datorgenererat kök med vita väggskåp, underskåp i trä, en köksö med tre pallar och en skjutdörr till en terrass')
A('media.items[12].alt',
  'Baño generado por ordenador con mueble de lavabo de madera, un espejo ancho, un inodoro y una ducha con mampara de cristal con dos rociadores',
  'Salle de bain de synthèse avec meuble vasque en bois, un large miroir, des WC et une douche à paroi de verre avec deux pommes de douche à effet pluie',
  'Computergeneriertes Bad mit Waschtisch aus Holz, einem breiten Spiegel, einem WC und einer Dusche mit Glasabtrennung und zwei Regenduschköpfen',
  'Компьютерная визуализация ванной комнаты с деревянной тумбой под раковину, широким зеркалом, унитазом и душем со стеклянной перегородкой и двумя тропическими лейками',
  'حمام مُولَّد بالحاسوب بخزانة مغسلة خشبية ومرآة عريضة ومرحاض ودش بحاجز زجاجي ورأسي رش مطري',
  'Computergegenereerde badkamer met een houten wastafelmeubel, een brede spiegel, een toilet en een douche met glazen scherm en twee regendouchekoppen',
  'Komputerowa wizualizacja łazienki z drewnianą szafką pod umywalkę, szerokim lustrem, toaletą i prysznicem ze szklaną ścianką i dwiema deszczownicami',
  'Datagenerert bad med servantskap i tre, et bredt speil, et toalett og en dusj med glassvegg og to regndusjhoder',
  'Datorgenererat badrum med tvättställsskåp i trä, en bred spegel, en toalett och en dusch med glasvägg och två regnduschhuvuden')

# ---------------------------------------------------------------- overview and why
A('overview.headlineHtml', 'Cuarenta y ocho viviendas, <em>quince disponibles</em>', 'Quarante-huit logements, <em>quinze disponibles</em>',
  'Achtundvierzig Wohnungen, <em>fünfzehn verfügbar</em>', 'Сорок восемь квартир, <em>пятнадцать доступны</em>',
  'ثمانية وأربعون مسكنًا، <em>خمسة عشر متاحًا</em>', 'Achtenveertig woningen, <em>vijftien beschikbaar</em>',
  'Czterdzieści osiem mieszkań, <em>piętnaście dostępnych</em>', 'Førtiåtte boliger, <em>femten ledige</em>',
  'Fyrtioåtta bostäder, <em>femton lediga</em>')
A('overview.copy[0]',
  'The OAK48 es un edificio residencial de 48 viviendas en tres bloques en Estepona, cerca del casco antiguo. La lista del promotor da precio a 15 de ellas y marca las otras 33 como reservadas. Las 15 son viviendas de dos y tres dormitorios: tres en planta baja con patio, seis en las plantas primera y segunda con terraza y seis áticos con solárium en la cubierta.',
  'The OAK48 est un immeuble résidentiel de 48 logements répartis en trois blocs à Estepona, près de la vieille ville. La liste du promoteur indique un prix pour 15 d’entre eux et marque les 33 autres comme réservés. Ces 15 logements ont deux ou trois chambres : trois au rez-de-chaussée avec patio, six au premier et au deuxième étage avec terrasse, et six penthouses avec solarium en toiture.',
  'The OAK48 ist ein Wohngebäude mit 48 Wohnungen in drei Blöcken in Estepona, nahe der Altstadt. Die Liste des Bauträgers nennt für 15 davon einen Preis und kennzeichnet die übrigen 33 als reserviert. Die 15 haben zwei oder drei Schlafzimmer: drei im Erdgeschoss mit Patio, sechs im ersten und zweiten Obergeschoss mit Terrasse und sechs Penthäuser mit Solarium auf dem Dach.',
  'The OAK48 — жилой дом на 48 квартир в трёх корпусах в Эстепоне, рядом со старым городом. В списке застройщика указана цена для 15 из них, остальные 33 помечены как зарезервированные. Эти 15 — квартиры с двумя и тремя спальнями: три на первом этаже с патио, шесть на втором и третьем этажах с террасой и шесть пентхаусов с солярием на крыше.',
  'The OAK48 مبنى سكني من 48 مسكنًا في ثلاثة مبانٍ في إستيبونا، قرب البلدة القديمة. وتحدد قائمة المطوّر سعرًا لـ15 منها وتُدرج الـ33 الباقية على أنها محجوزة. والمساكن الخمسة عشر بغرفتين أو ثلاث غرف نوم: ثلاثة في الطابق الأرضي مع فناء، وستة في الطابقين الأول والثاني مع تراس، وستة بنتهاوس مع سولاريوم على السطح.',
  'The OAK48 is een woongebouw met 48 woningen in drie blokken in Estepona, vlak bij de oude stad. De lijst van de ontwikkelaar geeft voor 15 ervan een prijs en markeert de andere 33 als gereserveerd. De 15 zijn woningen met twee en drie slaapkamers: drie op de begane grond met een patio, zes op de eerste en tweede verdieping met een terras en zes penthouses met een solarium op het dak.',
  'The OAK48 to budynek mieszkalny z 48 mieszkaniami w trzech blokach w Esteponie, w pobliżu starego miasta. Lista dewelopera podaje cenę 15 z nich, a pozostałe 33 oznacza jako zarezerwowane. Te 15 to mieszkania z dwiema i trzema sypialniami: trzy na parterze z patio, sześć na pierwszym i drugim piętrze z tarasem oraz sześć penthouse’ów z solarium na dachu.',
  'The OAK48 er en boligbygning med 48 boliger i tre hus i Estepona, nær gamlebyen. Utbyggerens liste oppgir pris for 15 av dem og markerer de øvrige 33 som reservert. De 15 er boliger med to og tre soverom: tre i første etasje med patio, seks i andre og tredje etasje med terrasse og seks toppleiligheter med solterrasse på taket.',
  'The OAK48 är en bostadsbyggnad med 48 bostäder i tre hus i Estepona, nära gamla stan. Exploatörens lista anger pris för 15 av dem och markerar de övriga 33 som reserverade. De 15 är bostäder med två och tre sovrum: tre på bottenvåningen med patio, sex på första och andra våningen med terrass och sex takvåningar med solterrass på taket.')
A('overview.copy[1]',
  'Los residentes comparten una piscina, un gimnasio, una sala de coworking y un salón social en zonas ajardinadas, con dos plantas de sótano con plazas de garaje y trasteros. Los documentos del promotor no dan fecha de entrega y las imágenes están generadas por ordenador, por lo que tratamos el proyecto como sobre plano según los documentos que tenemos.',
  'Les résidents partagent une piscine, une salle de sport, un espace de coworking et un salon commun au milieu de jardins paysagers, avec deux niveaux de sous-sol réservés aux places de stationnement et aux caves. Les documents du promoteur ne donnent aucune date de livraison et les images sont de synthèse ; nous considérons donc le projet comme étant sur plan d’après les documents dont nous disposons.',
  'Die Bewohner teilen sich einen Pool, einen Fitnessraum, einen Coworking-Raum und einen Gemeinschaftssalon in begrünten Außenanlagen, dazu zwei Untergeschosse mit Stellplätzen und Abstellräumen. Die Unterlagen des Bauträgers nennen keinen Übergabetermin, und die Bilder sind computergeneriert; deshalb behandeln wir das Projekt nach den uns vorliegenden Unterlagen als Off-Plan-Projekt.',
  'Жители пользуются общим бассейном, тренажёрным залом, коворкингом и общей гостиной среди благоустроенных садов; в двух подземных уровнях находятся парковочные места и кладовые. В документах застройщика нет срока сдачи, а изображения созданы на компьютере, поэтому по имеющимся у нас документам мы считаем проект находящимся на стадии проекта.',
  'يتشارك السكان مسبحًا وصالة رياضية وقاعة عمل مشتركة وصالة اجتماعية ضمن حدائق مُنسَّقة، مع طابقين سفليين لمواقف السيارات وغرف التخزين. ولا تذكر وثائق المطوّر موعد تسليم، والصور مُولَّدة بالحاسوب، لذلك نتعامل مع المشروع على أنه على المخطط بحسب الوثائق التي بحوزتنا.',
  'De bewoners delen een zwembad, een fitnessruimte, een coworkingruimte en een gemeenschappelijke lounge in aangelegde tuinen, met twee ondergrondse niveaus voor parkeerplaatsen en bergingen. De documenten van de ontwikkelaar geven geen opleveringsdatum en de beelden zijn computergegenereerd, dus behandelen wij het project op basis van de documenten die wij hebben als een project op plan.',
  'Mieszkańcy korzystają ze wspólnego basenu, siłowni, sali coworkingowej i salonu w zagospodarowanych ogrodach, a dwa poziomy podziemne mieszczą miejsca postojowe i komórki lokatorskie. Dokumenty dewelopera nie podają terminu oddania, a wizualizacje są komputerowe, dlatego na podstawie posiadanych przez nas dokumentów traktujemy projekt jako sprzedaż z planu.',
  'Beboerne deler et basseng, et treningsrom, et coworking-rom og en felles salong i opparbeidede hager, med to kjellernivåer med parkeringsplasser og boder. Utbyggerens dokumenter oppgir ingen overleveringsdato, og bildene er datagenererte, så vi behandler prosjektet som salg på tegning ut fra dokumentene vi har.',
  'De boende delar en pool, ett gym, ett coworking-rum och en gemensam lounge i anlagda trädgårdar, med två källarplan med parkeringsplatser och förråd. Exploatörens dokument anger inget tillträdesdatum och bilderna är datorgenererade, så vi behandlar projektet som ett projekt på ritning utifrån de dokument vi har.')
A('overview.metrics[0][1]', '48 viviendas', '48 logements', '48 Wohnungen', '48 квартир', '48 مسكنًا', '48 woningen', '48 mieszkań', '48 boliger', '48 bostäder')
A('overview.metrics[1][1]', '15 viviendas', '15 logements', '15 Wohnungen', '15 квартир', '15 مسكنًا', '15 woningen', '15 mieszkań', '15 boliger', '15 bostäder')
A('overview.metrics[3][1]', 'Terrazas, patios, solariums y una piscina comunitaria', 'Terrasses, patios, solariums et une piscine commune',
  'Terrassen, Patios, Solarien und ein Gemeinschaftspool', 'Террасы, патио, солярии и общий бассейн',
  'تراسات وأفنية وسولاريوم ومسبح مشترك', 'Terrassen, patio’s, solariums en een gemeenschappelijk zwembad',
  'Tarasy, patia, solaria i wspólny basen', 'Terrasser, patioer, solterrasser og et felles basseng',
  'Terrasser, patior, solterrasser och en gemensam pool')
A('why.copy',
  'Apartamentos y áticos de dos y tres dormitorios cerca del casco antiguo de Estepona, con piscina comunitaria, gimnasio y sala de coworking.',
  'Appartements et penthouses de deux et trois chambres près de la vieille ville d’Estepona, avec piscine commune, salle de sport et espace de coworking.',
  'Wohnungen und Penthäuser mit zwei und drei Schlafzimmern nahe der Altstadt von Estepona, mit gemeinsamem Pool, Fitnessraum und Coworking-Raum.',
  'Квартиры и пентхаусы с двумя и тремя спальнями рядом со старым городом Эстепоны, с общим бассейном, тренажёрным залом и коворкингом.',
  'شقق وبنتهاوس بغرفتين أو ثلاث غرف نوم قرب البلدة القديمة في إستيبونا، مع مسبح مشترك وصالة رياضية وقاعة عمل مشتركة.',
  'Appartementen en penthouses met twee en drie slaapkamers vlak bij de oude stad van Estepona, met een gemeenschappelijk zwembad, een fitnessruimte en een coworkingruimte.',
  'Mieszkania i penthouse’y z dwiema i trzema sypialniami w pobliżu starego miasta w Esteponie, ze wspólnym basenem, siłownią i salą coworkingową.',
  'Leiligheter og toppleiligheter med to og tre soverom nær gamlebyen i Estepona, med felles basseng, treningsrom og coworking-rom.',
  'Lägenheter och takvåningar med två och tre sovrum nära gamla stan i Estepona, med gemensam pool, gemensamt gym och gemensamt coworking-rum.')
A('why.points[0][1]',
  'Compradores que quieren una vivienda nueva de dos o tres dormitorios en Estepona, desde un apartamento en planta baja con patio hasta un ático con solárium, para vivir o como segunda residencia.',
  'Acheteurs qui souhaitent un logement neuf de deux ou trois chambres à Estepona, d’un appartement au rez-de-chaussée avec patio à un penthouse avec solarium, pour y vivre ou comme résidence secondaire.',
  'Käufer, die in Estepona eine neue Wohnung mit zwei oder drei Schlafzimmern suchen, von der Erdgeschosswohnung mit Patio bis zum Penthouse mit Solarium, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужна новая квартира с двумя или тремя спальнями в Эстепоне — от апартаментов на первом этаже с патио до пентхауса с солярием, для жизни или как вторая недвижимость.',
  'مشترون يرغبون في مسكن جديد بغرفتين أو ثلاث غرف نوم في إستيبونا، من شقة في الطابق الأرضي مع فناء إلى بنتهاوس مع سولاريوم، للسكن أو كمسكن ثانٍ.',
  'Kopers die in Estepona een nieuwe woning met twee of drie slaapkamers zoeken, van een appartement op de begane grond met een patio tot een penthouse met een solarium, om in te wonen of als tweede woning.',
  'Kupujący, którzy szukają nowego mieszkania z dwiema lub trzema sypialniami w Esteponie, od apartamentu na parterze z patio po penthouse z solarium, do zamieszkania lub jako druga nieruchomość.',
  'Kjøpere som vil ha en ny bolig med to eller tre soverom i Estepona, fra en leilighet i første etasje med patio til en toppleilighet med solterrasse, til eget bruk eller som feriebolig.',
  'Köpare som vill ha en ny bostad med två eller tre sovrum i Estepona, från en lägenhet på bottenvåningen med patio till en takvåning med solterrass, för eget boende eller som andrahem.')
A('why.points[1][1]',
  'Áticos con solariums de {N20.57} a {N106.67} {U}, y una piscina, un gimnasio, una sala de coworking y un salón social compartidos por todas las viviendas, con precios de {E375000} a {E890000} más IVA.',
  'Des penthouses avec solariums de {N20.57} à {N106.67} {U}, et une piscine, une salle de sport, un espace de coworking et un salon communs à tous les logements, à des prix de {E375000} à {E890000} hors TVA.',
  'Penthäuser mit Solarien von {N20.57} bis {N106.67} {U} sowie ein Pool, ein Fitnessraum, ein Coworking-Raum und ein Gemeinschaftssalon für alle Wohnungen, zu Preisen von {E375000} bis {E890000} zuzüglich MwSt.',
  'Пентхаусы с солярием от {N20.57} до {N106.67} {U}, а также бассейн, тренажёрный зал, коворкинг и общая гостиная для всех квартир, по ценам от {E375000} до {E890000} без НДС.',
  'بنتهاوس بسولاريوم تبلغ مساحته من {N20.57} إلى {N106.67} {U}، ومسبح وصالة رياضية وقاعة عمل وصالة اجتماعية مشتركة بين جميع المساكن، بأسعار من {E375000} إلى {E890000} دون ضريبة القيمة المضافة.',
  'Penthouses met solariums van {N20.57} tot {N106.67} {U}, en een zwembad, een fitnessruimte, een coworkingruimte en een gemeenschappelijke lounge voor alle woningen, tegen prijzen van {E375000} tot {E890000} excl. btw.',
  'Penthouse’y z solariami od {N20.57} do {N106.67} {U} oraz basen, siłownia, sala coworkingowa i salon wspólne dla wszystkich mieszkań, w cenach od {E375000} do {E890000} plus VAT.',
  'Toppleiligheter med solterrasser på {N20.57} til {N106.67} {U}, og et basseng, et treningsrom, et coworking-rom og en felles salong for alle boligene, til priser fra {E375000} til {E890000} pluss mva.',
  'Takvåningar med solterrasser på {N20.57} till {N106.67} {U}, och en pool, ett gym, ett coworking-rum och en gemensam lounge för alla bostäder, till priser från {E375000} till {E890000} plus IVA.')
A('why.points[2][1]',
  'El dosier sitúa el edificio cerca del casco antiguo y bien comunicado con la A-7 y la AP-7, con el puerto deportivo a 6 minutos en su mapa de ubicación, y describe vistas a Sierra Bermeja y al Mediterráneo.',
  'Le dossier situe le bâtiment près de la vieille ville et bien relié à l’A-7 et à l’AP-7, avec le port de plaisance à 6 minutes sur sa carte de localisation, et décrit des vues sur la Sierra Bermeja et la Méditerranée.',
  'Das Dossier verortet das Gebäude nahe der Altstadt und gut angebunden an die A-7 und die AP-7, mit dem Yachthafen auf seiner Lagekarte in 6 Minuten Entfernung, und beschreibt Ausblicke auf die Sierra Bermeja und das Mittelmeer.',
  'В досье здание расположено рядом со старым городом и с хорошим выездом на трассы A-7 и AP-7; на карте расположения порт находится в 6 минутах, а ещё описаны виды на Сьерра-Бермеху и Средиземное море.',
  'يضع ملف المطوّر المبنى قرب البلدة القديمة وجيد الاتصال بالطريقين A-7 وAP-7، مع الميناء على بُعد 6 دقائق في خريطة الموقع، ويصف إطلالات على سييرا برميخا والبحر المتوسط.',
  'Het dossier plaatst het gebouw vlak bij de oude stad en goed verbonden met de A-7 en de AP-7, met de jachthaven op 6 minuten op zijn locatiekaart, en beschrijft uitzicht op de Sierra Bermeja en de Middellandse Zee.',
  'Dossier umieszcza budynek w pobliżu starego miasta i z dobrym dojazdem do A-7 i AP-7, z portem jachtowym w odległości 6 minut na mapie lokalizacji, i opisuje widoki na Sierra Bermeja i Morze Śródziemne.',
  'Dossieret plasserer bygningen nær gamlebyen og godt forbundet med A-7 og AP-7, med småbåthavnen 6 minutter unna på kartet over beliggenheten, og beskriver utsikt mot Sierra Bermeja og Middelhavet.',
  'Dossiern placerar byggnaden nära gamla stan och med goda förbindelser till A-7 och AP-7, med småbåtshamnen 6 minuter bort på lägeskartan, och beskriver utsikt mot Sierra Bermeja och Medelhavet.')
A('why.points[3][1]',
  'Los documentos no dan fecha de entrega ni estado de las obras, y 33 de las 48 viviendas ya están reservadas, por lo que confirmamos la disponibilidad, la fecha contractual y la licencia antes de cualquier reserva.',
  'Les documents ne donnent ni date de livraison ni avancement des travaux, et 33 des 48 logements sont déjà réservés ; nous confirmons donc la disponibilité, la date contractuelle et le permis avant toute réservation.',
  'Die Unterlagen nennen weder einen Übergabetermin noch einen Baufortschritt, und 33 der 48 Wohnungen sind bereits reserviert; deshalb bestätigen wir vor jeder Reservierung die Verfügbarkeit, den vertraglichen Termin und die Genehmigung.',
  'В документах нет ни срока сдачи, ни сведений о ходе работ, а 33 из 48 квартир уже зарезервированы, поэтому до любого бронирования мы подтверждаем наличие, договорную дату и разрешение.',
  'لا تذكر الوثائق موعد تسليم ولا مرحلة الأعمال، و33 مسكنًا من أصل 48 محجوزة بالفعل، لذلك نؤكد التوافر والموعد التعاقدي والرخصة قبل أي حجز.',
  'De documenten geven geen opleveringsdatum of bouwstand, en 33 van de 48 woningen zijn al gereserveerd, dus bevestigen wij de beschikbaarheid, de contractuele datum en de vergunning vóór elke reservering.',
  'Dokumenty nie podają terminu oddania ani etapu prac, a 33 z 48 mieszkań jest już zarezerwowanych, dlatego przed każdą rezerwacją potwierdzamy dostępność, termin umowny i pozwolenie.',
  'Dokumentene oppgir verken overleveringsdato eller byggestatus, og 33 av de 48 boligene er allerede reservert, så vi bekrefter tilgjengelighet, kontraktsfestet dato og tillatelse før enhver reservasjon.',
  'Dokumenten anger varken tillträdesdatum eller byggstatus, och 33 av de 48 bostäderna är redan reserverade, så vi bekräftar tillgänglighet, avtalat datum och tillstånd före varje reservation.')

# ---------------------------------------------------------------- architecture
A('architecture.headlineHtml', 'Terrazas curvas, <em>celosías de lamas</em>', 'Terrasses courbes, <em>claustras à lames</em>',
  'Geschwungene Terrassen, <em>Lamellenblenden</em>', 'Изогнутые террасы, <em>экраны из реек</em>',
  'تراسات منحنية، <em>وشرائح رأسية</em>', 'Gebogen terrassen, <em>lamellenschermen</em>',
  'Zaokrąglone tarasy, <em>ekrany z listew</em>', 'Buede terrasser, <em>lamellskjermer</em>', 'Böjda terrasser, <em>lamellskärmar</em>')
A('architecture.copy[0]',
  'El dosier del promotor indica que el edificio ha sido diseñado por el estudio Mónaco Arquitectos en torno a cuatro principios: accesibilidad, sostenibilidad, diseño contemporáneo y funcionalidad. Describe una arquitectura contemporánea con grandes terrazas y vistas a Sierra Bermeja y al mar.',
  'Le dossier du promoteur indique que le bâtiment a été conçu par l’agence Mónaco Arquitectos autour de quatre principes : accessibilité, durabilité, design contemporain et fonctionnalité. Il décrit une architecture contemporaine avec de grandes terrasses et des vues sur la Sierra Bermeja et la mer.',
  'Laut dem Dossier des Bauträgers wurde das Gebäude vom Architekturbüro Mónaco Arquitectos nach vier Prinzipien entworfen: Barrierefreiheit, Nachhaltigkeit, zeitgenössisches Design und Funktionalität. Es beschreibt eine zeitgenössische Architektur mit großen Terrassen und Ausblicken auf die Sierra Bermeja und das Meer.',
  'В досье застройщика сказано, что здание спроектировано студией Mónaco Arquitectos на основе четырёх принципов: доступность, устойчивость, современный дизайн и функциональность. Архитектура описана как современная, с большими террасами и видами на Сьерра-Бермеху и море.',
  'يذكر ملف المطوّر أن المبنى صمّمه استوديو Mónaco Arquitectos حول أربعة مبادئ: سهولة الوصول والاستدامة والتصميم المعاصر والوظيفية. ويصف عمارة معاصرة بتراسات كبيرة وإطلالات على سييرا برميخا والبحر.',
  'Het dossier van de ontwikkelaar zegt dat het gebouw is ontworpen door het architectenbureau Mónaco Arquitectos rond vier principes: toegankelijkheid, duurzaamheid, eigentijds ontwerp en functionaliteit. Het beschrijft eigentijdse architectuur met grote terrassen en uitzicht op de Sierra Bermeja en de zee.',
  'Dossier dewelopera podaje, że budynek zaprojektowała pracownia Mónaco Arquitectos w oparciu o cztery zasady: dostępność, zrównoważony rozwój, współczesny design i funkcjonalność. Opisuje architekturę współczesną z dużymi tarasami i widokami na Sierra Bermeja i morze.',
  'Utbyggerens dossier sier at bygningen er tegnet av arkitektstudioet Mónaco Arquitectos ut fra fire prinsipper: tilgjengelighet, bærekraft, moderne design og funksjonalitet. Det beskriver moderne arkitektur med store terrasser og utsikt mot Sierra Bermeja og havet.',
  'Exploatörens dossier anger att byggnaden är ritad av arkitektbyrån Mónaco Arquitectos utifrån fyra principer: tillgänglighet, hållbarhet, modern design och funktionalitet. Den beskriver modern arkitektur med stora terrasser och utsikt mot Sierra Bermeja och havet.')
A('architecture.copy[1]',
  'En las imágenes, los bloques tienen cuatro plantas, con terrazas curvas tras lamas verticales de color gris claro, paneles imitación madera alrededor de los huecos y barandillas de cristal, y una planta de cubierta con solariums en lo alto.',
  'Sur les images, les blocs s’élèvent sur quatre niveaux, avec des terrasses courbes derrière des lames verticales gris clair, des panneaux imitation bois autour des ouvertures et des garde-corps en verre, et un niveau de toiture avec solariums au sommet.',
  'Auf den Bildern haben die Blöcke vier Geschosse, mit geschwungenen Terrassen hinter senkrechten Lamellen in hellem Grau, Paneelen in Holzoptik rund um die Öffnungen und Glasbrüstungen sowie einer Dachebene mit Solarien obenauf.',
  'На изображениях корпуса имеют четыре этажа, с изогнутыми террасами за вертикальными рейками светло-серого цвета, панелями под дерево вокруг проёмов и стеклянными ограждениями; наверху — уровень крыши с солярием.',
  'تظهر المباني في الصور من أربعة طوابق، بتراسات منحنية خلف شرائح رأسية رمادية فاتحة، وألواح بمظهر الخشب حول الفتحات، وحواجز زجاجية، ومستوى سطح بسولاريوم في الأعلى.',
  'Op de beelden hebben de blokken vier verdiepingen, met gebogen terrassen achter verticale latten in lichtgrijs, panelen in houtlook rond de openingen en glazen balustrades, en bovenop een dakniveau met solariums.',
  'Na wizualizacjach bloki mają cztery kondygnacje, z zaokrąglonymi tarasami za pionowymi listwami w jasnoszarym kolorze, panelami imitującymi drewno wokół otworów i szklanymi balustradami, a na szczycie poziom dachu z solariami.',
  'På bildene har byggene fire etasjer, med buede terrasser bak vertikale lameller i lys grå, paneler i trelook rundt åpningene og glassrekkverk, og et takplan med solterrasser øverst.',
  'På bilderna har husen fyra våningar, med böjda terrasser bakom vertikala lameller i ljusgrått, paneler i trälook runt öppningarna och glasräcken, och ett takplan med solterrasser överst.')
A('architecture.highlights[0][1]',
  'Fábrica de ladrillo cerámico de medio pie, revocada y pintada, con ladrillo visto en algunas zonas, trasdosada por el interior con ladrillo hueco doble y aislamiento proyectado en las cámaras, y mortero de cal entre los paños de ventanas.',
  'Maçonnerie de brique céramique de demi-brique, enduite et peinte, avec de la brique apparente par endroits, doublée à l’intérieur de brique creuse double et d’une isolation projetée dans les lames d’air, et mortier à base de chaux entre les panneaux de fenêtres.',
  'Halbsteinmauerwerk aus Ziegeln, verputzt und gestrichen, stellenweise mit Sichtmauerwerk, innen mit doppeltem Hohlziegel und eingespritzter Dämmung in den Hohlräumen verkleidet, sowie Kalkmörtel zwischen den Fensterfeldern.',
  'Кладка из керамического кирпича в полкирпича, оштукатуренная и окрашенная, местами с открытой кирпичной кладкой, с внутренней облицовкой из двойного пустотелого кирпича и напылённым утеплителем в полостях, а между оконными проёмами — известковый раствор.',
  'جدران من الطوب الخزفي بسماكة نصف طوبة، مكسوة بالمونة ومطلية، مع طوب ظاهر في بعض المواضع، ومبطَّنة من الداخل بطوب مجوف مزدوج وعزل مرشوش في الفراغات، وملاط جيري بين ألواح النوافذ.',
  'Metselwerk van keramische baksteen van een halve steen, bepleisterd en geschilderd, met op sommige plaatsen zichtbaar metselwerk, aan de binnenkant bekleed met dubbele holle baksteen en gespoten isolatie in de spouwen, en kalkmortel tussen de raamvelden.',
  'Mur z ceramicznej cegły o grubości pół cegły, otynkowany i pomalowany, miejscami z cegłą licową, wyłożony od wewnątrz podwójną cegłą dziurawką z natryskową izolacją w szczelinach, z zaprawą wapienną między polami okien.',
  'Murverk av keramisk tegl i halv stein, pusset og malt, med synlig tegl enkelte steder, kledd innvendig med dobbel hulltegl og sprøytet isolasjon i hulrommene, og kalkbasert mørtel mellom vindusfeltene.',
  'Murverk av keramiskt tegel i halvsten, putsat och målat, med synligt tegel på sina ställen, invändigt klätt med dubbelt hålltegel och sprutad isolering i hålrummen, och kalkbaserad bruk mellan fönsterpartierna.')
A('architecture.highlights[1][1]',
  'Suelos de gres porcelánico antideslizante, techos de PVC o aluminio con acabados para exteriores, acabados imitación madera y celosías entre las terrazas de viviendas contiguas.',
  'Sols en grès cérame antidérapant, plafonds en PVC ou en aluminium avec finitions pour l’extérieur, finitions imitation bois et claustras entre les terrasses des logements voisins.',
  'Rutschfeste Feinsteinzeugböden, Decken aus PVC oder Aluminium mit Außenfinish, Oberflächen in Holzoptik und Sichtschutzgitter zwischen den Terrassen benachbarter Wohnungen.',
  'Противоскользящий керамогранит на полу, потолки из ПВХ или алюминия с отделкой для наружных работ, отделка под дерево и решётчатые перегородки между террасами соседних квартир.',
  'أرضيات من بورسلان الغريس المانع للانزلاق، وأسقف من PVC أو الألمنيوم بتشطيبات للأماكن الخارجية، وتشطيبات بمظهر الخشب، وفواصل شبكية بين تراسات المساكن المتجاورة.',
  'Antislip porseleinen vloeren, plafonds van pvc of aluminium met buitenafwerking, afwerkingen in houtlook en roosterschermen tussen de terrassen van naburige woningen.',
  'Antypoślizgowe podłogi z gresu porcelanowego, sufity z PVC lub aluminium z wykończeniem zewnętrznym, wykończenia imitujące drewno oraz kratownice między tarasami sąsiednich mieszkań.',
  'Sklisikre gulv i porselenskeramikk, himlinger i PVC eller aluminium med utendørs finish, overflater i trelook og gittervegger mellom terrassene til naboboligene.',
  'Halkfria golv i porslinsgranit, tak i PVC eller aluminium med utomhusfinish, ytor i trälook och gallerskärmar mellan grannbostädernas terrasser.')
A('architecture.highlights[3][1]',
  'Cubiertas privativas transitables con aislamiento térmico y acústico, acabadas en gres porcelánico antideslizante, y una escalera metálica al solárium en los áticos.',
  'Toitures privatives accessibles avec isolation thermique et acoustique, finies en grès cérame antidérapant, et un escalier métallique vers le solarium dans les penthouses.',
  'Begehbare private Dächer mit Wärme- und Schalldämmung, mit rutschfestem Feinsteinzeug belegt, und in den Penthäusern eine Metalltreppe zum Solarium.',
  'Эксплуатируемые частные крыши с тепло- и звукоизоляцией, с покрытием из противоскользящего керамогранита, а в пентхаусах — металлическая лестница на солярий.',
  'أسطح خاصة قابلة للاستخدام بعزل حراري وصوتي، مكسوة ببورسلان الغريس المانع للانزلاق، ودرج معدني يصل إلى السولاريوم في البنتهاوس.',
  'Begaanbare privédaken met thermische en akoestische isolatie, afgewerkt met antislip porselein, en in de penthouses een metalen trap naar het solarium.',
  'Użytkowe prywatne dachy z izolacją termiczną i akustyczną, wykończone antypoślizgowym gresem porcelanowym, oraz metalowe schody na solarium w penthousach.',
  'Gangbare private tak med varme- og lydisolasjon, ferdigstilt i sklisikker porselenskeramikk, og en metalltrapp opp til solterrassen i toppleilighetene.',
  'Gångbara privata tak med värme- och ljudisolering, avslutade i halkfri porslinsgranit, och en metalltrappa upp till solterrassen i takvåningarna.')

# ---------------------------------------------------------------- quality specification
A('qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del dosier del promotor, que no lleva fecha. Indica que los materiales pueden ser modificados por la dirección facultativa siempre que no se reduzca su calidad, que las imágenes no son contractuales y que el mobiliario de las imágenes 3D no está incluido.',
  'Source : le descriptif de qualité du dossier du promoteur, qui n’est pas daté. Il précise que les matériaux peuvent être modifiés par la direction de projet à condition que leur qualité ne soit pas diminuée, que les images n’ont pas valeur contractuelle et que le mobilier des images 3D n’est pas inclus.',
  'Quelle: die Baubeschreibung im Dossier des Bauträgers, die kein Datum trägt. Sie weist darauf hin, dass die Bauleitung die Materialien ändern kann, sofern die Qualität nicht gemindert wird, dass die Bilder nicht vertraglich bindend sind und dass die Möbel in den 3D-Darstellungen nicht enthalten sind.',
  'Источник: спецификация качества в досье застройщика, которая не датирована. В ней сказано, что руководство проекта может менять материалы при условии, что качество не снижается, что изображения не имеют договорной силы и что мебель на 3D-изображениях не входит в стоимость.',
  'المصدر: مواصفات الجودة في ملف المطوّر، وهي غير مؤرخة. وتذكر أن إدارة المشروع قد تغيّر المواد بشرط ألا تنخفض جودتها، وأن الصور غير ملزمة تعاقديًا، وأن الأثاث في الصور ثلاثية الأبعاد غير مشمول.',
  'Bron: de kwaliteitsspecificatie in het dossier van de ontwikkelaar, die niet is gedateerd. Daarin staat dat de bouwleiding de materialen mag wijzigen zolang de kwaliteit niet afneemt, dat de beelden niet contractueel zijn en dat de meubels in de 3D-beelden niet zijn inbegrepen.',
  'Źródło: specyfikacja jakości w dossier dewelopera, która nie jest datowana. Podano w niej, że kierownictwo projektu może zmieniać materiały, o ile nie obniży to ich jakości, że wizualizacje nie mają charakteru umownego i że meble na obrazach 3D nie są wliczone w cenę.',
  'Kilde: kvalitetsspesifikasjonen i utbyggerens dossier, som ikke er datert. Den sier at prosjektledelsen kan endre materialene så lenge kvaliteten ikke reduseres, at bildene ikke er kontraktsfestet og at møblene i 3D-bildene ikke er inkludert.',
  'Källa: kvalitetsbeskrivningen i exploatörens dossier, som inte är daterad. Den anger att projektledningen får ändra materialen så länge kvaliteten inte försämras, att bilderna inte är avtalsgrundande och att möblerna i 3D-bilderna inte ingår.')
A('qualitySpecs.groups[0].items[0]',
  'Tabiquería interior de yeso laminado sobre estructura metálica con aislamiento termoacústico.',
  'Cloisons intérieures en plaques de plâtre sur ossature métallique avec isolation thermique et acoustique.',
  'Innenwände aus Gipskarton auf Metallunterkonstruktion mit Wärme- und Schalldämmung.',
  'Внутренние перегородки из гипсокартона на металлическом каркасе с тепло- и звукоизоляцией.',
  'فواصل داخلية من ألواح الجبس على هيكل معدني مع عزل حراري وصوتي.',
  'Binnenwanden van gipsplaten op een metalen constructie met thermische en akoestische isolatie.',
  'Przegrody wewnętrzne z płyt gipsowo-kartonowych na konstrukcji metalowej z izolacją termiczną i akustyczną.',
  'Innvendige skillevegger i gipsplater på metallkonstruksjon med varme- og lydisolasjon.',
  'Invändiga mellanväggar i gipsskivor på metallstomme med värme- och ljudisolering.')
A('qualitySpecs.groups[0].items[1]',
  'Separación entre viviendas de ladrillo cerámico con aislamiento proyectado.',
  'Séparation entre logements en brique céramique avec isolation projetée.',
  'Wohnungstrennwände aus Ziegel mit eingespritzter Dämmung.',
  'Перегородки между квартирами из керамического кирпича с напылённым утеплителем.',
  'الفصل بين المساكن بطوب خزفي مع عزل مرشوش.',
  'Scheiding tussen woningen in keramische baksteen met gespoten isolatie.',
  'Przegrody między mieszkaniami z cegły ceramicznej z natryskową izolacją.',
  'Skille mellom boliger i keramisk tegl med sprøytet isolasjon.',
  'Avskiljning mellan bostäder i keramiskt tegel med sprutad isolering.')
A('qualitySpecs.groups[1].items[0]',
  'Suelo porcelánico rectificado de primera calidad de 60 x 60 cm en el interior de las viviendas, gres porcelánico en los baños y porcelánico antideslizante en las terrazas.',
  'Sol en grès cérame rectifié de première qualité de 60 x 60 cm à l’intérieur des logements, grès cérame dans les salles de bain et grès cérame antidérapant sur les terrasses.',
  'Rektifizierter Feinsteinzeugboden erster Wahl im Format 60 x 60 cm in den Wohnräumen, Feinsteinzeug in den Bädern und rutschfestes Feinsteinzeug auf den Terrassen.',
  'Ректифицированный керамогранит первого сорта 60 x 60 см внутри квартир, керамогранит в ванных комнатах и противоскользящий керамогранит на террасах.',
  'أرضيات بورسلان مقصوصة بدقة من الدرجة الأولى بقياس 60 × 60 سم داخل المساكن، وبورسلان الغريس في الحمامات، وبورسلان مانع للانزلاق على التراسات.',
  'Gerectificeerde porseleinen vloeren van eerste kwaliteit van 60 x 60 cm in de woningen, porseleinen tegels in de badkamers en antislip porselein op de terrassen.',
  'Szlifowany gres porcelanowy pierwszej jakości o wymiarach 60 x 60 cm wewnątrz mieszkań, gres w łazienkach i antypoślizgowy gres na tarasach.',
  'Rektifisert porselenskeramikk av første kvalitet på 60 x 60 cm inne i boligene, porselenskeramikk på badene og sklisikker porselenskeramikk på terrassene.',
  'Rektifierad porslinsgranit av första kvalitet på 60 x 60 cm inne i bostäderna, porslinsgranit i badrummen och halkfri porslinsgranit på terrasserna.')
A('qualitySpecs.groups[1].items[1]',
  'Falsos techos de yeso laminado en la cocina, los baños principales y los pasos de instalaciones, yeso enlucido y pintado en el resto, y pintura plástica en paredes y techos.',
  'Faux plafonds en plaques de plâtre dans la cuisine, les salles de bain principales et les passages de gaines, plâtre peint ailleurs, et peinture plastique sur les murs et les plafonds.',
  'Abgehängte Decken aus Gipskarton in Küche, Hauptbädern und Installationsführungen, sonst verputzte und gestrichene Decken, und Dispersionsfarbe an Wänden und Decken.',
  'Подвесные потолки из гипсокартона на кухне, в главных ванных комнатах и в зонах прохода коммуникаций, в остальных помещениях — окрашенная штукатурка, стены и потолки покрыты акриловой краской.',
  'أسقف مستعارة من ألواح الجبس في المطبخ والحمامات الرئيسية ومسارات التمديدات، وجص مطلي في بقية الأماكن، ودهان بلاستيكي على الجدران والأسقف.',
  'Verlaagde plafonds van gipsplaten in de keuken, de hoofdbadkamers en de leidingvoeringen, elders gepleisterd en geschilderd, en kunststofverf op wanden en plafonds.',
  'Sufity podwieszane z płyt gipsowo-kartonowych w kuchni, głównych łazienkach i na trasach instalacji, w pozostałych pomieszczeniach tynk malowany, a na ścianach i sufitach farba plastyczna.',
  'Nedsenket himling i gipsplater på kjøkkenet, hovedbadene og i føringsveiene for installasjoner, pusset og malt himling ellers, og plastmaling på vegger og himlinger.',
  'Undertak i gipsskivor i köket, huvudbadrummen och installationsstråken, putsat och målat tak i övrigt, och plastfärg på väggar och tak.')
A('qualitySpecs.groups[2].items[0]',
  'Puerta de entrada blindada con cerradura de seguridad y pernos antipalanca, y puertas interiores lisas de madera maciza.',
  'Porte d’entrée blindée avec serrure de sécurité et pênes anti-effraction, et portes intérieures lisses en bois massif.',
  'Eine gepanzerte Wohnungstür mit Sicherheitsschloss und Hebelschutzbolzen sowie glatte Innentüren aus Massivholz.',
  'Бронированная входная дверь с замком повышенной безопасности и противовзломными штырями и гладкие межкомнатные двери из массива дерева.',
  'باب دخول مصفّح بقفل أمان ومسامير تثبيت مانعة للخلع، وأبواب داخلية ملساء من الخشب الصلب.',
  'Een gepantserde voordeur met een veiligheidsslot en antihefbouten, en gladde binnendeuren van massief hout.',
  'Drzwi wejściowe antywłamaniowe z zamkiem bezpieczeństwa i bolcami antywyważeniowymi oraz gładkie drzwi wewnętrzne z litego drewna.',
  'En panserdør med sikkerhetslås og anti-brekkjernbolter, og glatte innerdører i massivt tre.',
  'En pansardörr med säkerhetslås och bultar mot kofot, och släta innerdörrar i massivt trä.')
A('qualitySpecs.groups[2].items[1]',
  'Armarios empotrados lacados en blanco y forrados interiormente con melamina, con maletero, cajoneras y barra de colgar.',
  'Placards intégrés laqués blanc et revêtus de mélamine à l’intérieur, avec étagère à valises, tiroirs et barre de penderie.',
  'Einbauschränke in Weiß lackiert und innen mit Melamin ausgekleidet, mit Gepäckfach, Schubladen und Kleiderstange.',
  'Встроенные шкафы, лакированные в белый цвет и облицованные внутри меламином, с отделением для чемоданов, ящиками и штангой для одежды.',
  'خزائن ملابس مدمجة مطلية بالورنيش الأبيض ومبطنة من الداخل بالميلامين، مع رف للحقائب وأدراج وقضيب تعليق.',
  'Inbouwkasten in wit gelakt en aan de binnenkant bekleed met melamine, met een koffervak, laden en een kledingstang.',
  'Szafy wnękowe lakierowane na biało i wyłożone w środku melaminą, z półką na walizki, szufladami i drążkiem na ubrania.',
  'Innebygde garderobeskap lakkert hvite og kledd innvendig med melamin, med kofferthylle, skuffer og kleshenger.',
  'Inbyggda garderober lackade i vitt och invändigt klädda med melamin, med resväskhylla, lådor och klädstång.')
A('qualitySpecs.groups[3].items[0]',
  'Cocina amueblada con muebles altos y bajos y encimera de Silestone o similar.',
  'Cuisine équipée avec meubles hauts et bas et plan de travail en Silestone ou équivalent.',
  'Eine Einbauküche mit Ober- und Unterschränken und einer Arbeitsplatte aus Silestone oder gleichwertig.',
  'Кухня с мебелью: верхние и нижние шкафы, столешница из Silestone или аналогичного материала.',
  'مطبخ مُجهَّز بخزائن علوية وسفلية وسطح عمل من Silestone أو ما يماثله.',
  'Een ingerichte keuken met boven- en onderkasten en een werkblad van Silestone of gelijkwaardig.',
  'Wyposażona kuchnia z szafkami wiszącymi i stojącymi oraz blatem z Silestone lub podobnego materiału.',
  'Et møblert kjøkken med over- og underskap og en benkeplate i Silestone eller tilsvarende.',
  'Ett inrett kök med över- och underskåp och en bänkskiva i Silestone eller likvärdigt.')
A('qualitySpecs.groups[3].items[1]',
  'Se incluyen horno, vitrocerámica, campana extractora y lavadora.',
  'Un four, une plaque vitrocéramique, une hotte aspirante et un lave-linge sont inclus.',
  'Backofen, Ceranfeld, Dunstabzugshaube und Waschmaschine sind enthalten.',
  'В комплект входят духовой шкаф, стеклокерамическая варочная панель, вытяжка и стиральная машина.',
  'تشمل التجهيزات فرنًا وموقدًا خزفيًا وشفاط هواء وغسالة.',
  'Een oven, een keramische kookplaat, een afzuigkap en een wasmachine zijn inbegrepen.',
  'W zestawie są piekarnik, płyta ceramiczna, okap i pralka.',
  'Ovn, keramisk kokeplate, avtrekksvifte og vaskemaskin er inkludert.',
  'Ugn, keramikhäll, köksfläkt och tvättmaskin ingår.')
A('qualitySpecs.groups[4].items[0]',
  'Alicatado porcelánico de primera calidad en baños y cocina, de Saloni o similar.',
  'Carrelage mural en grès cérame de première qualité dans les salles de bain et la cuisine, de marque Saloni ou équivalent.',
  'Wandfliesen aus Feinsteinzeug erster Wahl in Bädern und Küche, von Saloni oder gleichwertig.',
  'Плитка из керамогранита первого сорта в ванных комнатах и на кухне, Saloni или аналогичная.',
  'تكسية جدران ببورسلان من الدرجة الأولى في الحمامات والمطبخ، من Saloni أو ما يماثلها.',
  'Wandtegels van porselein van eerste kwaliteit in de badkamers en de keuken, van Saloni of gelijkwaardig.',
  'Płytki porcelanowe pierwszej jakości w łazienkach i kuchni, marki Saloni lub podobne.',
  'Veggfliser i porselenskeramikk av første kvalitet på badene og kjøkkenet, fra Saloni eller tilsvarende.',
  'Kakel i porslinsgranit av första kvalitet i badrummen och köket, från Saloni eller likvärdigt.')
A('qualitySpecs.groups[4].items[1]',
  'Aparatos sanitarios de porcelana blanca esmaltada de Roca o similar, plato de ducha de resina acrílica de perfil bajo con mampara de cristal templado, y grifería monomando y termostática.',
  'Appareils sanitaires en porcelaine blanche émaillée de marque Roca ou équivalent, receveur de douche extra-plat en résine acrylique avec paroi en verre trempé, et robinetterie mitigeur et thermostatique.',
  'Sanitärobjekte aus weißem glasiertem Porzellan von Roca oder gleichwertig, eine flache Duschwanne aus Acrylharz mit Glasabtrennung aus gehärtetem Glas sowie Einhebel- und Thermostatarmaturen.',
  'Сантехника из белого глазурованного фарфора Roca или аналогичная, низкий поддон из акриловой смолы со стеклянной перегородкой из закалённого стекла, однорычажные и термостатические смесители.',
  'أدوات صحية من البورسلين الأبيض المطلي من Roca أو ما يماثلها، وحوض دش منخفض من راتنج الأكريليك مع حاجز من الزجاج المقسّى، وحنفيات بذراع واحد وحنفيات ثرموستاتية.',
  'Sanitair van wit geglazuurd porselein van Roca of gelijkwaardig, een lage douchebak van acrylhars met een scherm van gehard glas, en eengreeps- en thermostatische kranen.',
  'Ceramika sanitarna z białej glazurowanej porcelany marki Roca lub podobna, niski brodzik z żywicy akrylowej ze szklaną ścianką z hartowanego szkła oraz baterie jednouchwytowe i termostatyczne.',
  'Sanitærutstyr i hvit glasert porselen fra Roca eller tilsvarende, en lav dusjkum i akrylharpiks med skjerm i herdet glass, og énhåndtaks og termostatiske armaturer.',
  'Sanitetsporslin i vitt glaserat porslin från Roca eller likvärdigt, ett lågt duschkar i akrylharts med duschvägg i härdat glas, och enhandsblandare och termostatblandare.')
A('qualitySpecs.groups[5].items[0]',
  'El dosier indica aire acondicionado y calefacción en todas las viviendas, y la memoria describe el sistema: fan-coils en los falsos techos de los baños, conductos de fibra de vidrio a cada estancia y un termostato programable en el salón.',
  'Le dossier annonce la climatisation et le chauffage dans chaque logement, et le descriptif détaille le système : ventilo-convecteurs dans les faux plafonds des salles de bain, gaines en fibre de verre vers chaque pièce et thermostat programmable dans le séjour.',
  'Das Dossier nennt in jeder Wohnung Klimatisierung und Heizung, und die Baubeschreibung erläutert das System: Gebläsekonvektoren in den abgehängten Decken der Bäder, Glasfaserkanäle zu jedem Raum und ein programmierbarer Thermostat im Wohnzimmer.',
  'В досье указаны кондиционирование и отопление в каждой квартире, а спецификация описывает систему: фанкойлы в подвесных потолках ванных комнат, воздуховоды из стекловолокна к каждой комнате и программируемый термостат в гостиной.',
  'يذكر ملف المطوّر التكييف والتدفئة في كل مسكن، وتصف المواصفات النظام: وحدات مراوح ملفّات في الأسقف المستعارة للحمامات، ومجاري من الألياف الزجاجية إلى كل غرفة، وثرموستات قابل للبرمجة في غرفة المعيشة.',
  'Het dossier vermeldt airconditioning en verwarming in elke woning, en de specificatie beschrijft het systeem: fan-coilunits in de verlaagde plafonds van de badkamers, glasvezelkanalen naar elke kamer en een programmeerbare thermostaat in de woonkamer.',
  'Dossier podaje klimatyzację i ogrzewanie w każdym mieszkaniu, a specyfikacja opisuje system: fan-coile w sufitach podwieszanych łazienek, kanały z włókna szklanego do każdego pomieszczenia i programowalny termostat w salonie.',
  'Dossieret oppgir klimaanlegg og oppvarming i hver bolig, og spesifikasjonen beskriver systemet: viftekonvektorer i den nedsenkede himlingen på badene, glassfiberkanaler til hvert rom og en programmerbar termostat i stuen.',
  'Dossiern anger luftkonditionering och värme i varje bostad, och beskrivningen redogör för systemet: fläktkonvektorer i badrummens undertak, kanaler av glasfiber till varje rum och en programmerbar termostat i vardagsrummet.')
A('qualitySpecs.groups[5].items[1]',
  'Preinstalación de un sistema comunitario de energía solar térmica que colabora en la producción del agua caliente de cada vivienda, y preinstalación de carga de coche eléctrico en el garaje.',
  'Pré-équipement d’un système solaire thermique collectif qui contribue à produire l’eau chaude de chaque logement, et pré-équipement pour la recharge de voiture électrique au garage.',
  'Vorinstallation einer gemeinschaftlichen Solarthermieanlage, die zur Warmwasserbereitung jeder Wohnung beiträgt, und Vorinstallation für das Laden von Elektroautos in der Garage.',
  'Предусмотрена установка общей солнечной тепловой системы, которая участвует в нагреве горячей воды для каждой квартиры, и подготовка к зарядке электромобилей в гараже.',
  'تجهيز مسبق لنظام شمسي حراري مشترك يسهم في إنتاج الماء الساخن لكل مسكن، وتجهيز مسبق لشحن السيارات الكهربائية في المرآب.',
  'Voorbereiding voor een gemeenschappelijk thermisch zonnesysteem dat bijdraagt aan het warme water van elke woning, en voorbereiding voor het opladen van elektrische auto’s in de garage.',
  'Przygotowanie instalacji pod wspólny system solarny cieplny, który współtworzy ciepłą wodę w każdym mieszkaniu, oraz instalacja przygotowująca do ładowania samochodów elektrycznych w garażu.',
  'Forberedelse for et felles solvarmesystem som bidrar til varmtvannet i hver bolig, og forberedelse for lading av elbil i garasjen.',
  'Förberedelse för ett gemensamt solvärmesystem som bidrar till varmvattnet i varje bostad, och förberedelse för laddning av elbil i garaget.')
A('qualitySpecs.groups[6].items[0]',
  'Tomas de antena de TV en el salón y los dormitorios, punto de luz y toma de corriente en las terrazas, y tomas de teléfono y banda ancha.',
  'Prises d’antenne TV dans le séjour et les chambres, point lumineux et prise de courant sur les terrasses, et prises téléphone et haut débit.',
  'TV-Antennenanschlüsse im Wohnzimmer und in den Schlafzimmern, ein Lichtauslass und eine Steckdose auf den Terrassen sowie Telefon- und Breitbandanschlüsse.',
  'Розетки для телевизионной антенны в гостиной и спальнях, точка освещения и розетка на террасах, а также телефонные и широкополосные розетки.',
  'مآخذ هوائي التلفزيون في غرفة المعيشة وغرف النوم، ونقطة إنارة ومخرج كهرباء في التراسات، ومآخذ الهاتف والإنترنت عريض النطاق.',
  'Tv-aansluitingen in de woonkamer en de slaapkamers, een lichtpunt en een stopcontact op de terrassen, en telefoon- en breedbandaansluitingen.',
  'Gniazda antenowe TV w salonie i sypialniach, punkt świetlny i gniazdko na tarasach oraz gniazda telefoniczne i szerokopasmowe.',
  'TV-antennekontakter i stuen og soverommene, et lyspunkt og en stikkontakt på terrassene, og telefon- og bredbåndskontakter.',
  'TV-antennuttag i vardagsrummet och sovrummen, en ljuspunkt och ett eluttag på terrasserna, och telefon- och bredbandsuttag.')
A('qualitySpecs.groups[6].items[1]',
  'Luces empotradas en la cocina y el baño principal, y videoportero para el control de acceso a la vivienda.',
  'Spots encastrés dans la cuisine et la salle de bain principale, et visiophone pour l’accès au logement.',
  'Einbauleuchten in Küche und Hauptbad sowie eine Video-Gegensprechanlage für den Zugang zur Wohnung.',
  'Встроенные светильники на кухне и в главной ванной комнате и видеодомофон для доступа в квартиру.',
  'إنارة مدمجة في المطبخ والحمام الرئيسي، وجهاز إنتركوم بالفيديو للدخول إلى المسكن.',
  'Inbouwspots in de keuken en de hoofdbadkamer, en een video-intercom voor de toegang tot de woning.',
  'Oprawy wpuszczane w kuchni i głównej łazience oraz wideodomofon do kontroli dostępu do mieszkania.',
  'Innfelte lys på kjøkkenet og hovedbadet, og en videoport for adgang til boligen.',
  'Infällda lampor i köket och huvudbadrummet, och en videodörrtelefon för tillträde till bostaden.')
A('qualitySpecs.groups[7].name', 'Cubiertas de los áticos', 'Toitures des penthouses', 'Dachebenen der Penthäuser', 'Крыши пентхаусов',
  'أسطح البنتهاوس', 'Daken van de penthouses', 'Dachy penthouse’ów', 'Takene på toppleilighetene', 'Takvåningarnas tak')
A('qualitySpecs.groups[7].items[0]',
  'Una cubierta privativa transitable con aislamiento térmico y acústico, acabada en gres porcelánico antideslizante y a la que se accede por una escalera metálica.',
  'Une toiture privative accessible avec isolation thermique et acoustique, finie en grès cérame antidérapant et desservie par un escalier métallique.',
  'Ein privates begehbares Dach mit Wärme- und Schalldämmung, mit rutschfestem Feinsteinzeug belegt und über eine Metalltreppe erreichbar.',
  'Частная эксплуатируемая крыша с тепло- и звукоизоляцией, с покрытием из противоскользящего керамогранита, на которую ведёт металлическая лестница.',
  'سطح خاص قابل للاستخدام بعزل حراري وصوتي، مكسو ببورسلان الغريس المانع للانزلاق، يُوصَل إليه بدرج معدني.',
  'Een privé begaanbaar dak met thermische en akoestische isolatie, afgewerkt met antislip porselein en bereikbaar via een metalen trap.',
  'Prywatny użytkowy dach z izolacją termiczną i akustyczną, wykończony antypoślizgowym gresem porcelanowym, na który prowadzą metalowe schody.',
  'Et privat gangbart tak med varme- og lydisolasjon, ferdigstilt i sklisikker porselenskeramikk og nådd via en metalltrapp.',
  'Ett privat gångbart tak med värme- och ljudisolering, avslutat i halkfri porslinsgranit och nåbart via en metalltrappa.')
A('qualitySpecs.groups[7].items[1]',
  'La memoria indica una piscina de {N3.00} x {N2.00} m y una ducha exterior solo en los áticos; los planos muestran una piscina en dos de los seis áticos a la venta.',
  'Le descriptif indique une piscine de {N3.00} x {N2.00} m et une douche extérieure réservées aux penthouses ; les plans montrent une piscine sur deux des six penthouses annoncés.',
  'Die Baubeschreibung nennt einen Pool von {N3.00} x {N2.00} m und eine Außendusche ausschließlich für Penthäuser; die Planblätter zeigen einen Pool bei zwei der sechs gelisteten Penthäuser.',
  'В спецификации бассейн {N3.00} x {N2.00} м и уличный душ указаны только для пентхаусов; на планировках бассейн показан у двух из шести пентхаусов в продаже.',
  'تذكر المواصفات مسبحًا بقياس {N3.00} × {N2.00} م ودشًا خارجيًا حصريًا للبنتهاوس؛ وتُظهر المخططات مسبحًا في اثنين من البنتهاوس الستة المعروضة.',
  'De specificatie vermeldt een zwembad van {N3.00} x {N2.00} m en een buitendouche uitsluitend bij penthouses; de plattegronden tonen een zwembad bij twee van de zes aangeboden penthouses.',
  'Specyfikacja podaje basen {N3.00} x {N2.00} m i prysznic zewnętrzny wyłącznie dla penthouse’ów; rzuty pokazują basen przy dwóch z sześciu oferowanych penthouse’ów.',
  'Spesifikasjonen oppgir et basseng på {N3.00} x {N2.00} m og en utendørs dusj kun for toppleilighetene; plantegningene viser et basseng på to av de seks annonserte toppleilighetene.',
  'Beskrivningen anger en pool på {N3.00} x {N2.00} m och en utomhusdusch endast för takvåningarna; planritningarna visar en pool på två av de sex listade takvåningarna.')
A('qualitySpecs.groups[8].name', 'Garaje, ascensores y zonas comunes', 'Garage, ascenseurs et parties communes',
  'Garage, Aufzüge und Gemeinschaftsflächen', 'Гараж, лифты и общие зоны', 'المرآب والمصاعد والمرافق المشتركة',
  'Garage, liften en gemeenschappelijke ruimtes', 'Garaż, windy i części wspólne', 'Garasje, heiser og fellesarealer', 'Garage, hissar och gemensamma ytor')
A('qualitySpecs.groups[8].items[0]',
  'Ascensores para cuatro personas con puertas automáticas, con parada en el garaje, puerta automática para vehículos y garaje con las instalaciones de seguridad que exige la normativa.',
  'Ascenseurs de quatre personnes à portes automatiques, desservant le garage, portail automatique pour les véhicules et garage doté des dispositifs de sécurité exigés par la réglementation.',
  'Aufzüge für vier Personen mit automatischen Türen, die bis in die Garage fahren, ein automatisches Tor für Fahrzeuge und eine Garage mit den vorgeschriebenen Sicherheitseinrichtungen.',
  'Лифты на четыре человека с автоматическими дверями и остановкой в гараже, автоматические ворота для въезда и выезда и гараж с системами безопасности, предусмотренными нормативами.',
  'مصاعد تتسع لأربعة أشخاص بأبواب أوتوماتيكية وتتوقف عند المرآب، وبوابة أوتوماتيكية للمركبات، ومرآب مزوّد بأنظمة السلامة التي تشترطها اللوائح.',
  'Liften voor vier personen met automatische deuren, die tot in de garage rijden, een automatische poort voor voertuigen en een garage met de veiligheidsvoorzieningen die de regelgeving vereist.',
  'Windy dla czterech osób z automatycznymi drzwiami, zatrzymujące się w garażu, automatyczna brama wjazdowa dla pojazdów i garaż z systemami bezpieczeństwa wymaganymi przepisami.',
  'Heiser for fire personer med automatiske dører som stopper i garasjen, en automatisk port for kjøretøy og en garasje med sikkerhetssystemene regelverket krever.',
  'Hissar för fyra personer med automatiska dörrar som stannar i garaget, en automatisk port för fordon och ett garage med de säkerhetssystem som föreskrifterna kräver.')
A('qualitySpecs.groups[8].items[1]',
  'Circuito cerrado de cámaras en las zonas comunes y los garajes, patio interior adoquinado, barandillas de cristal, y piscina comunitaria, sala de coworking y zona deportiva.',
  'Vidéosurveillance dans les parties communes et les garages, cour intérieure pavée, garde-corps en verre, et piscine commune, espace de coworking et espace sportif.',
  'Videoüberwachung in den Gemeinschaftsbereichen und den Garagen, gepflasterter Innenhof, Glasbrüstungen sowie Gemeinschaftspool, Coworking-Raum und Sportbereich.',
  'Видеонаблюдение в общих зонах и гаражах, мощёный внутренний двор, стеклянные ограждения, общий бассейн, коворкинг и спортивная зона.',
  'كاميرات مراقبة في المناطق المشتركة والمرائب، وفناء داخلي مرصوف، وحواجز زجاجية، ومسبح مشترك وقاعة عمل مشتركة ومنطقة رياضية.',
  'Camerabewaking in de gemeenschappelijke ruimtes en de garages, een bestrate binnenplaats, glazen balustrades, en een gemeenschappelijk zwembad, een coworkingruimte en een sportzone.',
  'Monitoring w częściach wspólnych i garażach, brukowany dziedziniec wewnętrzny, szklane balustrady oraz wspólny basen, sala coworkingowa i strefa sportowa.',
  'Kameraovervåking i fellesarealene og garasjene, en brulagt innvendig gårdsplass, glassrekkverk, og et felles basseng, et coworking-rom og et sportsområde.',
  'Kameraövervakning i de gemensamma ytorna och garagen, en stenlagd innergård, glasräcken, och en gemensam pool, ett coworking-rum och en idrottsyta.')

# ---------------------------------------------------------------- the four kinds of home
A('residences.headlineHtml', 'Quince viviendas, <em>cuatro tipos</em>', 'Quinze logements, <em>quatre types</em>',
  'Fünfzehn Wohnungen, <em>vier Typen</em>', 'Пятнадцать квартир, <em>четыре типа</em>',
  'خمسة عشر مسكنًا، <em>أربعة أنواع</em>', 'Vijftien woningen, <em>vier soorten</em>',
  'Piętnaście mieszkań, <em>cztery rodzaje</em>', 'Femten boliger, <em>fire typer</em>', 'Femton bostäder, <em>fyra typer</em>')
A('residences.copy',
  'Las quince viviendas se dividen en cuatro grupos por planta y tamaño. La tabla siguiente las lista una a una con su precio.',
  'Les quinze logements se répartissent en quatre groupes selon l’étage et la taille. Le tableau ci-dessous les présente un par un avec leur prix.',
  'Die fünfzehn Wohnungen lassen sich nach Geschoss und Größe in vier Gruppen einteilen. Die Tabelle unten listet jede einzelne mit ihrem Preis auf.',
  'Пятнадцать квартир делятся на четыре группы по этажу и размеру. В таблице ниже каждая указана с ценой.',
  'تنقسم المساكن الخمسة عشر إلى أربع مجموعات بحسب الطابق والمساحة. ويعرض الجدول أدناه كل مسكن مع سعره.',
  'De vijftien woningen vallen naar verdieping en grootte in vier groepen uiteen. De tabel hieronder geeft elke woning met haar prijs.',
  'Piętnaście mieszkań dzieli się na cztery grupy według piętra i wielkości. Tabela poniżej podaje każde z nich wraz z ceną.',
  'De femten boligene faller i fire grupper etter etasje og størrelse. Tabellen nedenfor viser hver enkelt med pris.',
  'De femton bostäderna delas in i fyra grupper efter våning och storlek. Tabellen nedan listar varje bostad med dess pris.')
A('residences.items[0].name', 'Viviendas de planta baja con patio', 'Logements en rez-de-chaussée avec patio',
  'Erdgeschosswohnungen mit Patio', 'Квартиры на первом этаже с патио', 'مساكن في الطابق الأرضي مع فناء',
  'Woningen op de begane grond met een patio', 'Mieszkania na parterze z patio', 'Boliger i første etasje med patio',
  'Bostäder på bottenvåningen med patio')
A('residences.items[0].points[0]',
  'Las viviendas 1-0-D, 2-0-C y 3-0-D tienen dos dormitorios y dos baños, uno de ellos en suite, con {N64.05}, {N65.65} y {N69.81} {U} construidos y {N55.10}, {N55.97} y {N58.48} {U} interiores.',
  'Les logements 1-0-D, 2-0-C et 3-0-D ont deux chambres et deux salles de bain, dont une en suite, avec {N64.05}, {N65.65} et {N69.81} {U} construits et {N55.10}, {N55.97} et {N58.48} {U} intérieurs.',
  'Die Wohnungen 1-0-D, 2-0-C und 3-0-D haben zwei Schlafzimmer und zwei Bäder, eines davon en suite, mit {N64.05}, {N65.65} und {N69.81} {U} bebaut und {N55.10}, {N55.97} und {N58.48} {U} Innenfläche.',
  'У квартир 1-0-D, 2-0-C и 3-0-D по две спальни и две ванные комнаты, одна из них при главной спальне, застроенная площадь {N64.05}, {N65.65} и {N69.81} {U}, внутренняя — {N55.10}, {N55.97} и {N58.48} {U}.',
  'للمساكن 1-0-D و2-0-C و3-0-D غرفتا نوم وحمامان، أحدهما داخل غرفة النوم الرئيسية، بمساحة مبنية {N64.05} و{N65.65} و{N69.81} {U} ومساحة داخلية {N55.10} و{N55.97} و{N58.48} {U}.',
  'De woningen 1-0-D, 2-0-C en 3-0-D hebben twee slaapkamers en twee badkamers, waarvan één en suite, met {N64.05}, {N65.65} en {N69.81} {U} bebouwd en {N55.10}, {N55.97} en {N58.48} {U} binnen.',
  'Mieszkania 1-0-D, 2-0-C i 3-0-D mają dwie sypialnie i dwie łazienki, w tym jedną przy sypialni głównej, o powierzchni zabudowy {N64.05}, {N65.65} i {N69.81} {U} oraz powierzchni wewnętrznej {N55.10}, {N55.97} i {N58.48} {U}.',
  'Boligene 1-0-D, 2-0-C og 3-0-D har to soverom og to bad, ett av dem en suite, med {N64.05}, {N65.65} og {N69.81} {U} bebygd areal og {N55.10}, {N55.97} og {N58.48} {U} innvendig.',
  'Bostäderna 1-0-D, 2-0-C och 3-0-D har två sovrum och två badrum, ett av dem en suite, med {N64.05}, {N65.65} och {N69.81} {U} byggyta och {N55.10}, {N55.97} och {N58.48} {U} inomhus.')
A('residences.items[0].points[1]',
  'Cada una tiene un patio descubierto de {N10.89}, {N10.89} y {N9.96} {U}, con un lavadero de {N2.55} {U} en el plano, y no tienen terraza.',
  'Chacun a un patio découvert de {N10.89}, {N10.89} et {N9.96} {U}, avec une buanderie de {N2.55} {U} sur le plan, et pas de terrasse.',
  'Jede hat einen offenen Patio mit {N10.89}, {N10.89} und {N9.96} {U}, dazu laut Plan einen Wirtschaftsraum von {N2.55} {U}, aber keine Terrasse.',
  'У каждой есть открытое патио площадью {N10.89}, {N10.89} и {N9.96} {U} и, по плану, постирочная {N2.55} {U}; террасы нет.',
  'لكل منها فناء مكشوف بمساحة {N10.89} و{N10.89} و{N9.96} {U}، مع مغسلة بمساحة {N2.55} {U} في المخطط، ولا تراس لها.',
  'Elk heeft een open patio van {N10.89}, {N10.89} en {N9.96} {U}, met op de plattegrond een bijkeuken van {N2.55} {U}, en geen terras.',
  'Każde ma otwarte patio o powierzchni {N10.89}, {N10.89} i {N9.96} {U}, a na rzucie także pomieszczenie gospodarcze o powierzchni {N2.55} {U}, i nie ma tarasu.',
  'Hver har en åpen patio på {N10.89}, {N10.89} og {N9.96} {U}, med et vaskerom på {N2.55} {U} på plantegningen, og ingen terrasse.',
  'Var och en har en öppen patio på {N10.89}, {N10.89} och {N9.96} {U}, med ett tvättutrymme på {N2.55} {U} på planritningen, och ingen terrass.')
A('residences.items[0].points[2]', 'Las tres cuestan {E375000}.', 'Les trois sont à {E375000}.', 'Alle drei kosten {E375000}.',
  'Все три — {E375000}.', 'سعر المساكن الثلاثة {E375000}.', 'Alle drie kosten {E375000}.', 'Wszystkie trzy kosztują {E375000}.',
  'Alle tre koster {E375000}.', 'Alla tre kostar {E375000}.')
A('residences.items[1].name', 'Viviendas de dos dormitorios en las plantas primera y segunda', 'Logements de deux chambres au premier et au deuxième étage',
  'Wohnungen mit zwei Schlafzimmern im ersten und zweiten Obergeschoss', 'Квартиры с двумя спальнями на втором и третьем этажах',
  'مساكن بغرفتي نوم في الطابقين الأول والثاني', 'Woningen met twee slaapkamers op de eerste en tweede verdieping',
  'Mieszkania z dwiema sypialniami na pierwszym i drugim piętrze', 'Boliger med to soverom i andre og tredje etasje',
  'Bostäder med två sovrum på första och andra våningen')
A('residences.items[1].points[0]',
  'Las viviendas 1-1-D, 2-1-D, 2-2-C, 3-1-D y 3-2-D tienen dos dormitorios y dos baños, con {N66.02} a {N76.35} {U} construidos, {N55.09} a {N64.62} {U} interiores y una terraza de {N11.88} a {N15.14} {U}.',
  'Les logements 1-1-D, 2-1-D, 2-2-C, 3-1-D et 3-2-D ont deux chambres et deux salles de bain, avec {N66.02} à {N76.35} {U} construits, {N55.09} à {N64.62} {U} intérieurs et une terrasse de {N11.88} à {N15.14} {U}.',
  'Die Wohnungen 1-1-D, 2-1-D, 2-2-C, 3-1-D und 3-2-D haben zwei Schlafzimmer und zwei Bäder, mit {N66.02} bis {N76.35} {U} bebaut, {N55.09} bis {N64.62} {U} Innenfläche und einer Terrasse von {N11.88} bis {N15.14} {U}.',
  'У квартир 1-1-D, 2-1-D, 2-2-C, 3-1-D и 3-2-D по две спальни и две ванные комнаты, застроенная площадь от {N66.02} до {N76.35} {U}, внутренняя — от {N55.09} до {N64.62} {U}, терраса — от {N11.88} до {N15.14} {U}.',
  'للمساكن 1-1-D و2-1-D و2-2-C و3-1-D و3-2-D غرفتا نوم وحمامان، بمساحة مبنية من {N66.02} إلى {N76.35} {U} ومساحة داخلية من {N55.09} إلى {N64.62} {U} وتراس من {N11.88} إلى {N15.14} {U}.',
  'De woningen 1-1-D, 2-1-D, 2-2-C, 3-1-D en 3-2-D hebben twee slaapkamers en twee badkamers, met {N66.02} tot {N76.35} {U} bebouwd, {N55.09} tot {N64.62} {U} binnen en een terras van {N11.88} tot {N15.14} {U}.',
  'Mieszkania 1-1-D, 2-1-D, 2-2-C, 3-1-D i 3-2-D mają dwie sypialnie i dwie łazienki, o powierzchni zabudowy od {N66.02} do {N76.35} {U}, powierzchni wewnętrznej od {N55.09} do {N64.62} {U} i tarasie od {N11.88} do {N15.14} {U}.',
  'Boligene 1-1-D, 2-1-D, 2-2-C, 3-1-D og 3-2-D har to soverom og to bad, med {N66.02} til {N76.35} {U} bebygd areal, {N55.09} til {N64.62} {U} innvendig og en terrasse på {N11.88} til {N15.14} {U}.',
  'Bostäderna 1-1-D, 2-1-D, 2-2-C, 3-1-D och 3-2-D har två sovrum och två badrum, med {N66.02} till {N76.35} {U} byggyta, {N55.09} till {N64.62} {U} inomhus och en terrass på {N11.88} till {N15.14} {U}.')
A('residences.items[1].points[1]',
  'Los precios van de {E380000} para la 3-1-D a {E410000} para la 2-2-C.', 'Les prix vont de {E380000} pour le 3-1-D à {E410000} pour le 2-2-C.',
  'Die Preise reichen von {E380000} für 3-1-D bis {E410000} für 2-2-C.', 'Цены — от {E380000} за 3-1-D до {E410000} за 2-2-C.',
  'تتراوح الأسعار من {E380000} للمسكن 3-1-D إلى {E410000} للمسكن 2-2-C.', 'De prijzen lopen van {E380000} voor 3-1-D tot {E410000} voor 2-2-C.',
  'Ceny wahają się od {E380000} za 3-1-D do {E410000} za 2-2-C.', 'Prisene går fra {E380000} for 3-1-D til {E410000} for 2-2-C.',
  'Priserna sträcker sig från {E380000} för 3-1-D till {E410000} för 2-2-C.')
A('residences.items[2].name', 'La vivienda de tres dormitorios de la primera planta', 'Le logement de trois chambres au premier étage',
  'Die Wohnung mit drei Schlafzimmern im ersten Obergeschoss', 'Квартира с тремя спальнями на втором этаже',
  'المسكن بثلاث غرف نوم في الطابق الأول', 'De woning met drie slaapkamers op de eerste verdieping',
  'Mieszkanie z trzema sypialniami na pierwszym piętrze', 'Boligen med tre soverom i andre etasje', 'Bostaden med tre sovrum på första våningen')
A('residences.items[2].points[0]',
  'La vivienda 1-1-C tiene tres dormitorios y dos baños, {N91.68} {U} construidos, {N76.89} {U} interiores y una terraza de {N37.54} {U}.',
  'Le logement 1-1-C a trois chambres et deux salles de bain, {N91.68} {U} construits, {N76.89} {U} intérieurs et une terrasse de {N37.54} {U}.',
  'Die Wohnung 1-1-C hat drei Schlafzimmer und zwei Bäder, {N91.68} {U} bebaut, {N76.89} {U} Innenfläche und eine Terrasse von {N37.54} {U}.',
  'У квартиры 1-1-C три спальни и две ванные комнаты, застроенная площадь {N91.68} {U}, внутренняя — {N76.89} {U}, терраса — {N37.54} {U}.',
  'للمسكن 1-1-C ثلاث غرف نوم وحمامان، بمساحة مبنية {N91.68} {U} ومساحة داخلية {N76.89} {U} وتراس بمساحة {N37.54} {U}.',
  'Woning 1-1-C heeft drie slaapkamers en twee badkamers, {N91.68} {U} bebouwd, {N76.89} {U} binnen en een terras van {N37.54} {U}.',
  'Mieszkanie 1-1-C ma trzy sypialnie i dwie łazienki, powierzchnię zabudowy {N91.68} {U}, powierzchnię wewnętrzną {N76.89} {U} i taras o powierzchni {N37.54} {U}.',
  'Bolig 1-1-C har tre soverom og to bad, {N91.68} {U} bebygd areal, {N76.89} {U} innvendig og en terrasse på {N37.54} {U}.',
  'Bostad 1-1-C har tre sovrum och två badrum, {N91.68} {U} byggyta, {N76.89} {U} inomhus och en terrass på {N37.54} {U}.')
A('residences.items[2].points[1]', 'El precio es de {E517000}.', 'Le prix est de {E517000}.', 'Der Preis beträgt {E517000}.',
  'Цена — {E517000}.', 'السعر {E517000}.', 'De prijs is {E517000}.', 'Cena wynosi {E517000}.', 'Prisen er {E517000}.', 'Priset är {E517000}.')
A('residences.items[3].name', 'Áticos con solárium', 'Penthouses avec solarium', 'Penthäuser mit Solarium', 'Пентхаусы с солярием',
  'بنتهاوس مع سولاريوم', 'Penthouses met een solarium', 'Penthouse’y z solarium', 'Toppleiligheter med solterrasse', 'Takvåningar med solterrass')
A('residences.items[3].points[0]',
  'Dos áticos grandes: el 1-3-B tiene dos dormitorios, {N91.36} {U} construidos y un solárium de {N106.67} {U}, y el 3-3-A tiene tres dormitorios, {N89.19} {U} construidos y un solárium de {N97.46} {U}. La lista de precios marca ambos con vista al mar y a la piscina, y sus planos muestran una piscina en la cubierta. Cuestan {E890000} y {E886000}.',
  'Deux grands penthouses : le 1-3-B a deux chambres, {N91.36} {U} construits et un solarium de {N106.67} {U}, et le 3-3-A a trois chambres, {N89.19} {U} construits et un solarium de {N97.46} {U}. La liste de prix les signale tous deux avec vue sur la mer et la piscine, et leurs plans montrent une piscine sur le toit. Ils sont à {E890000} et {E886000}.',
  'Zwei größere Penthäuser: 1-3-B hat zwei Schlafzimmer, {N91.36} {U} bebaut und ein Solarium von {N106.67} {U}, 3-3-A hat drei Schlafzimmer, {N89.19} {U} bebaut und ein Solarium von {N97.46} {U}. Die Preisliste kennzeichnet beide mit Meer- und Poolblick, und ihre Pläne zeigen einen Pool auf dem Dach. Sie kosten {E890000} und {E886000}.',
  'Два крупных пентхауса: у 1-3-B две спальни, застроенная площадь {N91.36} {U} и солярий {N106.67} {U}, у 3-3-A три спальни, застроенная площадь {N89.19} {U} и солярий {N97.46} {U}. В прайс-листе оба отмечены видом на море и бассейн, а на их планировках на крыше показан бассейн. Цены — {E890000} и {E886000}.',
  'بنتهاوسان أكبر حجمًا: للمسكن 1-3-B غرفتا نوم ومساحة مبنية {N91.36} {U} وسولاريوم {N106.67} {U}، وللمسكن 3-3-A ثلاث غرف نوم ومساحة مبنية {N89.19} {U} وسولاريوم {N97.46} {U}. وتشير قائمة الأسعار إلى أن لكليهما إطلالة على البحر والمسبح، وتُظهر مخططاتهما مسبحًا على السطح. سعرهما {E890000} و{E886000}.',
  'Twee grotere penthouses: 1-3-B heeft twee slaapkamers, {N91.36} {U} bebouwd en een solarium van {N106.67} {U}, en 3-3-A heeft drie slaapkamers, {N89.19} {U} bebouwd en een solarium van {N97.46} {U}. De prijslijst markeert beide met zee- en zwembadzicht en hun plattegronden tonen een zwembad op het dak. Ze kosten {E890000} en {E886000}.',
  'Dwa większe penthouse’y: 1-3-B ma dwie sypialnie, powierzchnię zabudowy {N91.36} {U} i solarium o powierzchni {N106.67} {U}, a 3-3-A ma trzy sypialnie, powierzchnię zabudowy {N89.19} {U} i solarium o powierzchni {N97.46} {U}. Cennik oznacza oba widokiem na morze i basen, a ich rzuty pokazują basen na dachu. Kosztują {E890000} i {E886000}.',
  'To større toppleiligheter: 1-3-B har to soverom, {N91.36} {U} bebygd areal og en solterrasse på {N106.67} {U}, og 3-3-A har tre soverom, {N89.19} {U} bebygd areal og en solterrasse på {N97.46} {U}. Prislisten merker begge med utsikt mot havet og bassenget, og plantegningene deres viser et basseng på taket. De koster {E890000} og {E886000}.',
  'Två större takvåningar: 1-3-B har två sovrum, {N91.36} {U} byggyta och en solterrass på {N106.67} {U}, och 3-3-A har tre sovrum, {N89.19} {U} byggyta och en solterrass på {N97.46} {U}. Prislistan markerar båda med havs- och poolutsikt, och deras planritningar visar en pool på taket. De kostar {E890000} och {E886000}.')
A('residences.items[3].points[1]',
  'Cuatro áticos más pequeños de dos dormitorios, 1-3-D, 2-3-C, 2-3-D y 3-3-D, con {N66.02} a {N76.35} {U} construidos, terrazas de {N11.88} a {N15.14} {U} y solariums de {N20.57} a {N25.80} {U}. Sus planos muestran un solárium y ninguna piscina, y los precios van de {E552000} a {E559000}.',
  'Quatre penthouses plus petits de deux chambres, 1-3-D, 2-3-C, 2-3-D et 3-3-D, avec {N66.02} à {N76.35} {U} construits, des terrasses de {N11.88} à {N15.14} {U} et des solariums de {N20.57} à {N25.80} {U}. Leurs plans montrent un solarium et pas de piscine, et les prix vont de {E552000} à {E559000}.',
  'Vier kleinere Penthäuser mit zwei Schlafzimmern, 1-3-D, 2-3-C, 2-3-D und 3-3-D, mit {N66.02} bis {N76.35} {U} bebaut, Terrassen von {N11.88} bis {N15.14} {U} und Solarien von {N20.57} bis {N25.80} {U}. Ihre Pläne zeigen ein Solarium und keinen Pool, die Preise reichen von {E552000} bis {E559000}.',
  'Четыре пентхауса поменьше с двумя спальнями — 1-3-D, 2-3-C, 2-3-D и 3-3-D — с застроенной площадью от {N66.02} до {N76.35} {U}, террасами от {N11.88} до {N15.14} {U} и солярием от {N20.57} до {N25.80} {U}. На их планировках показан солярий без бассейна, цены — от {E552000} до {E559000}.',
  'أربعة بنتهاوس أصغر بغرفتي نوم، هي 1-3-D و2-3-C و2-3-D و3-3-D، بمساحة مبنية من {N66.02} إلى {N76.35} {U} وتراسات من {N11.88} إلى {N15.14} {U} وسولاريوم من {N20.57} إلى {N25.80} {U}. وتُظهر مخططاتها سولاريوم دون مسبح، وتتراوح الأسعار من {E552000} إلى {E559000}.',
  'Vier kleinere penthouses met twee slaapkamers, 1-3-D, 2-3-C, 2-3-D en 3-3-D, met {N66.02} tot {N76.35} {U} bebouwd, terrassen van {N11.88} tot {N15.14} {U} en solariums van {N20.57} tot {N25.80} {U}. Hun plattegronden tonen een solarium en geen zwembad, en de prijzen lopen van {E552000} tot {E559000}.',
  'Cztery mniejsze penthouse’y z dwiema sypialniami, 1-3-D, 2-3-C, 2-3-D i 3-3-D, o powierzchni zabudowy od {N66.02} do {N76.35} {U}, z tarasami od {N11.88} do {N15.14} {U} i solariami od {N20.57} do {N25.80} {U}. Ich rzuty pokazują solarium bez basenu, a ceny wahają się od {E552000} do {E559000}.',
  'Fire mindre toppleiligheter med to soverom, 1-3-D, 2-3-C, 2-3-D og 3-3-D, med {N66.02} til {N76.35} {U} bebygd areal, terrasser på {N11.88} til {N15.14} {U} og solterrasser på {N20.57} til {N25.80} {U}. Plantegningene deres viser en solterrasse uten basseng, og prisene går fra {E552000} til {E559000}.',
  'Fyra mindre takvåningar med två sovrum, 1-3-D, 2-3-C, 2-3-D och 3-3-D, med {N66.02} till {N76.35} {U} byggyta, terrasser på {N11.88} till {N15.14} {U} och solterrasser på {N20.57} till {N25.80} {U}. Deras planritningar visar en solterrass utan pool, och priserna sträcker sig från {E552000} till {E559000}.')

# ---------------------------------------------------------------- lifestyle
A('lifestyle.headlineHtml', 'Una piscina, <em>un gimnasio</em> y un lugar para trabajar', 'Une piscine, <em>une salle de sport</em> et un lieu pour travailler',
  'Ein Pool, <em>ein Fitnessraum</em> und ein Ort zum Arbeiten', 'Бассейн, <em>тренажёрный зал</em> и место для работы',
  'مسبح، <em>وصالة رياضية</em> ومكان للعمل', 'Een zwembad, <em>een fitnessruimte</em> en een plek om te werken',
  'Basen, <em>siłownia</em> i miejsce do pracy', 'Et basseng, <em>et treningsrom</em> og et sted å jobbe',
  'En pool, <em>ett gym</em> och en plats att arbeta på')
A('lifestyle.copy',
  'Las zonas comunes se organizan en torno a una piscina comunitaria, un gimnasio, una sala de coworking y un salón social, en zonas ajardinadas.',
  'Les parties communes s’organisent autour d’une piscine commune, d’une salle de sport, d’un espace de coworking et d’un salon, dans des jardins paysagers.',
  'Die Gemeinschaftsbereiche sind um einen Gemeinschaftspool, einen Fitnessraum, einen Coworking-Raum und einen Gemeinschaftssalon in begrünten Außenanlagen angelegt.',
  'Общие зоны спланированы вокруг общего бассейна, тренажёрного зала, коворкинга и общей гостиной среди благоустроенных садов.',
  'تُنظَّم المرافق المشتركة حول مسبح مشترك وصالة رياضية وقاعة عمل وصالة اجتماعية ضمن حدائق مُنسَّقة.',
  'De gemeenschappelijke ruimtes zijn opgezet rond een gemeenschappelijk zwembad, een fitnessruimte, een coworkingruimte en een gemeenschappelijke lounge, in aangelegde tuinen.',
  'Części wspólne zaplanowano wokół wspólnego basenu, siłowni, sali coworkingowej i salonu, w zagospodarowanych ogrodach.',
  'Fellesarealene er planlagt rundt et felles basseng, et treningsrom, et coworking-rom og en felles salong, i opparbeidede hager.',
  'De gemensamma ytorna är planerade kring en gemensam pool, ett gym, ett coworking-rum och en gemensam lounge, i anlagda trädgårdar.')
A('lifestyle.panels[0][1]',
  'Una piscina comunitaria en el jardín, con {N103.61} {U} de lámina de agua en el plano de planta baja y un vestuario junto a ella.',
  'Une piscine commune dans le jardin, avec {N103.61} {U} de plan d’eau sur le plan du rez-de-chaussée et un vestiaire à côté.',
  'Ein Gemeinschaftspool im Garten, mit {N103.61} {U} Wasserfläche laut Plan des Erdgeschosses und einem Umkleideraum daneben.',
  'Общий бассейн в саду: по плану первого этажа зеркало воды составляет {N103.61} {U}, рядом — раздевалка.',
  'مسبح مشترك في الحديقة، بمساحة سطح مائي {N103.61} {U} في مخطط الطابق الأرضي، وغرفة تبديل ملابس بجانبه.',
  'Een gemeenschappelijk zwembad in de tuin, met {N103.61} {U} wateroppervlak op de plattegrond van de begane grond en een kleedruimte ernaast.',
  'Wspólny basen w ogrodzie, z lustrem wody o powierzchni {N103.61} {U} na rzucie parteru i przebieralnią obok.',
  'Et felles basseng i hagen, med {N103.61} {U} vannflate på plantegningen av første etasje og et garderoberom ved siden av.',
  'En gemensam pool i trädgården, med {N103.61} {U} vattenyta på planritningen av bottenvåningen och ett omklädningsrum intill.')
A('lifestyle.panels[1][1]',
  'Un gimnasio y una zona deportiva para los residentes, tal como los recogen el dosier y la memoria.',
  'Une salle de sport et un espace sportif pour les résidents, tels que le dossier et le descriptif les mentionnent.',
  'Ein Fitnessraum und ein Sportbereich für die Bewohner, wie sie das Dossier und die Baubeschreibung aufführen.',
  'Тренажёрный зал и спортивная зона для жителей — так они указаны в досье и спецификации.',
  'صالة رياضية ومنطقة رياضية للسكان، كما يذكرها ملف المطوّر والمواصفات.',
  'Een fitnessruimte en een sportzone voor de bewoners, zoals het dossier en de specificatie ze vermelden.',
  'Siłownia i strefa sportowa dla mieszkańców, tak jak wymieniają je dossier i specyfikacja.',
  'Et treningsrom og et sportsområde for beboerne, slik dossieret og spesifikasjonen oppgir dem.',
  'Ett gym och en idrottsyta för de boende, så som dossiern och beskrivningen anger dem.')
A('lifestyle.panels[2][0]', 'Coworking y salón social', 'Coworking et salon commun', 'Coworking und Gemeinschaftssalon',
  'Коворкинг и общая гостиная', 'قاعة العمل والصالة الاجتماعية', 'Coworking en de lounge', 'Coworking i salon',
  'Coworking og den felles salongen', 'Coworking och den gemensamma loungen')
A('lifestyle.panels[2][1]',
  'Una sala de coworking y un salón social, que el dosier recoge entre las zonas comunes sin describirlos.',
  'Un espace de coworking et un salon commun, que le dossier cite parmi les parties communes sans les décrire.',
  'Ein Coworking-Raum und ein Gemeinschaftssalon, die das Dossier unter den Gemeinschaftsbereichen aufführt, ohne sie zu beschreiben.',
  'Коворкинг и общая гостиная, которые досье называет среди общих зон, не описывая их.',
  'قاعة عمل وصالة اجتماعية، يذكرهما ملف المطوّر بين المرافق المشتركة دون وصفهما.',
  'Een coworkingruimte en een gemeenschappelijke lounge, die het dossier onder de gemeenschappelijke ruimtes noemt zonder ze te beschrijven.',
  'Sala coworkingowa i salon, które dossier wymienia wśród części wspólnych, nie opisując ich.',
  'Et coworking-rom og en felles salong, som dossieret nevner blant fellesarealene uten å beskrive dem.',
  'Ett coworking-rum och en gemensam lounge, som dossiern nämner bland de gemensamma ytorna utan att beskriva dem.')
A('lifestyle.panels[3][0]', 'Jardines y aparcamiento', 'Jardins et stationnement', 'Gärten und Stellplätze', 'Сады и парковка',
  'الحدائق والمواقف', 'Tuinen en parkeren', 'Ogrody i parking', 'Hager og parkering', 'Trädgårdar och parkering')
A('lifestyle.panels[3][1]',
  'Zonas ajardinadas de {N240.37} {U} en la planta baja, y dos plantas de sótano con plazas de garaje y trasteros.',
  'Espaces paysagers de {N240.37} {U} au rez-de-chaussée, et deux niveaux de sous-sol avec places de stationnement et caves.',
  'Begrünte Außenanlagen von {N240.37} {U} im Erdgeschoss und zwei Untergeschosse mit Stellplätzen und Abstellräumen.',
  'Благоустроенные зоны площадью {N240.37} {U} на первом этаже и два подземных уровня с парковочными местами и кладовыми.',
  'مساحات مُنسَّقة بمساحة {N240.37} {U} في الطابق الأرضي، وطابقان سفليان لمواقف السيارات وغرف التخزين.',
  'Aangelegde zones van {N240.37} {U} op de begane grond en twee ondergrondse niveaus met parkeerplaatsen en bergingen.',
  'Zagospodarowane tereny o powierzchni {N240.37} {U} na parterze oraz dwa poziomy podziemne z miejscami postojowymi i komórkami lokatorskimi.',
  'Opparbeidede områder på {N240.37} {U} i første etasje, og to kjellernivåer med parkeringsplasser og boder.',
  'Anlagda ytor på {N240.37} {U} på bottenvåningen, och två källarplan med parkeringsplatser och förråd.')

# ---------------------------------------------------------------- location
A('location.headlineHtml', 'Estepona, <em>cerca del casco antiguo</em>', 'Estepona, <em>près de la vieille ville</em>',
  'Estepona, <em>nahe der Altstadt</em>', 'Эстепона, <em>рядом со старым городом</em>', 'إستيبونا، <em>قرب البلدة القديمة</em>',
  'Estepona, <em>vlak bij de oude stad</em>', 'Estepona, <em>w pobliżu starego miasta</em>', 'Estepona, <em>nær gamlebyen</em>',
  'Estepona, <em>nära gamla stan</em>')
A('location.copy',
  'El dosier sitúa el edificio en una de las zonas residenciales más distinguidas de Estepona, cerca del casco antiguo y en pleno corazón de la Costa del Sol, bien comunicada con la A-7 y la AP-7, con vistas a Sierra Bermeja y al Mediterráneo. Su mapa de ubicación da el puerto deportivo a 6 minutos, la playa de Punta Plata a 8, la del Padrón a 10 y la bahía de Estepona a 12, y su texto da el aeropuerto de Málaga a 45 minutos. No dice cómo se recorren esos tiempos ni da una dirección postal, por lo que el mapa sitúa el proyecto a nivel de zona.',
  'Le dossier situe le bâtiment dans l’un des quartiers résidentiels les plus distingués d’Estepona, près de la vieille ville et au cœur de la Costa del Sol, bien reliée à l’A-7 et à l’AP-7, avec des vues sur la Sierra Bermeja et la Méditerranée. Sa carte de localisation donne le port de plaisance à 6 minutes, la plage de Punta Plata à 8, celle du Padrón à 10 et la baie d’Estepona à 12, et son texte donne l’aéroport de Málaga à 45 minutes. Il ne dit pas comment ces durées sont parcourues et ne donne aucune adresse postale ; la carte place donc le projet à l’échelle du secteur.',
  'Das Dossier verortet das Gebäude in einer der angesehensten Wohnlagen von Estepona, nahe der Altstadt und mitten an der Costa del Sol, gut angebunden an die A-7 und die AP-7, mit Ausblick auf die Sierra Bermeja und das Mittelmeer. Seine Lagekarte nennt den Yachthafen in 6 Minuten, den Strand Punta Plata in 8, den Strand Padrón in 10 und die Bucht von Estepona in 12 Minuten, und sein Text nennt den Flughafen Málaga in 45 Minuten. Es sagt nicht, wie diese Zeiten zurückgelegt werden, und gibt keine Straßenadresse an, daher verortet die Karte das Projekt nur auf Gebietsebene.',
  'В досье здание расположено в одном из самых престижных жилых районов Эстепоны, рядом со старым городом и в самом сердце Коста-дель-Соль, с хорошим выездом на трассы A-7 и AP-7, с видами на Сьерра-Бермеху и Средиземное море. На карте расположения порт указан в 6 минутах, пляж Пунта-Плата — в 8, пляж Падрон — в 10, бухта Эстепоны — в 12, а в тексте аэропорт Малаги — в 45 минутах. Как преодолеваются эти минуты, не сказано, точного адреса нет, поэтому на карте проект показан на уровне района.',
  'يضع ملف المطوّر المبنى في إحدى أرقى المناطق السكنية في إستيبونا، قرب البلدة القديمة وفي قلب كوستا ديل سول، وجيدة الاتصال بالطريقين A-7 وAP-7، مع إطلالات على سييرا برميخا والبحر المتوسط. وتذكر خريطة الموقع أن الميناء على بُعد 6 دقائق وشاطئ بونتا بلاتا على بُعد 8 وشاطئ بادرون على بُعد 10 وخليج إستيبونا على بُعد 12 دقيقة، ويذكر نصّه أن مطار مالقة على بُعد 45 دقيقة. ولا يبيّن كيف تُقطع هذه الأوقات ولا يذكر عنوانًا بريديًا، لذلك تضع الخريطة المشروع على مستوى المنطقة.',
  'Het dossier plaatst het gebouw in een van de meest gewilde woonwijken van Estepona, vlak bij de oude stad en midden aan de Costa del Sol, goed verbonden met de A-7 en de AP-7, met uitzicht op de Sierra Bermeja en de Middellandse Zee. Zijn locatiekaart noemt de jachthaven op 6 minuten, het strand van Punta Plata op 8, dat van Padrón op 10 en de baai van Estepona op 12, en zijn tekst noemt de luchthaven van Málaga op 45 minuten. Het zegt niet hoe die tijden worden afgelegd en geeft geen straatadres, dus plaatst de kaart het project op gebiedsniveau.',
  'Dossier umieszcza budynek w jednej z najbardziej prestiżowych dzielnic mieszkalnych Estepony, w pobliżu starego miasta i w sercu Costa del Sol, z dobrym dojazdem do A-7 i AP-7, z widokiem na Sierra Bermeja i Morze Śródziemne. Mapa lokalizacji podaje port jachtowy w odległości 6 minut, plażę Punta Plata 8, plażę Padrón 10 i zatokę Estepony 12 minut, a tekst podaje lotnisko w Maladze w odległości 45 minut. Nie mówi, w jaki sposób pokonuje się te odcinki, i nie podaje adresu, dlatego mapa pokazuje projekt na poziomie okolicy.',
  'Dossieret plasserer bygningen i et av de mest ettertraktede boligområdene i Estepona, nær gamlebyen og midt på Costa del Sol, godt forbundet med A-7 og AP-7, med utsikt mot Sierra Bermeja og Middelhavet. Kartet over beliggenheten oppgir småbåthavnen 6 minutter unna, stranden Punta Plata 8, Padrón 10 og bukten i Estepona 12, og teksten oppgir Málaga lufthavn 45 minutter unna. Det sier ikke hvordan tidene tilbakelegges og oppgir ingen gateadresse, så kartet plasserer prosjektet på områdenivå.',
  'Dossiern placerar byggnaden i ett av Esteponas mest eftertraktade bostadsområden, nära gamla stan och mitt på Costa del Sol, med goda förbindelser till A-7 och AP-7, med utsikt mot Sierra Bermeja och Medelhavet. Lägeskartan anger småbåtshamnen på 6 minuter, stranden Punta Plata på 8, Padrón på 10 och Esteponas vik på 12, och texten anger Málagas flygplats på 45 minuter. Den säger inte hur tiderna tillryggaläggs och anger ingen gatuadress, så kartan placerar projektet på områdesnivå.')
A('location.distances[1][0]', 'Playa de Punta Plata', 'Plage de Punta Plata', 'Strand Punta Plata', 'Пляж Пунта-Плата', 'شاطئ بونتا بلاتا',
  'Strand van Punta Plata', 'Plaża Punta Plata', 'Stranden Punta Plata', 'Stranden Punta Plata')
A('location.distances[2][0]', 'Playa del Padrón', 'Plage du Padrón', 'Strand Padrón', 'Пляж Падрон', 'شاطئ بادرون',
  'Strand van Padrón', 'Plaża Padrón', 'Stranden Padrón', 'Stranden Padrón')
A('location.distances[3][0]', 'Bahía de Estepona', 'Baie d’Estepona', 'Bucht von Estepona', 'Бухта Эстепоны', 'خليج إستيبونا',
  'Baai van Estepona', 'Zatoka Estepony', 'Esteponas bukt', 'Esteponas vik')
# one spelling of a minute per table: the English rows are all "N min"
for n, ar in ((6, 'دقائق'), (8, 'دقائق'), (10, 'دقائق'), (12, 'دقيقة'), (45, 'دقيقة')):
    a(f'{n} min', f'{n} min', f'{n} min', f'{n} Min.', f'{n} мин', f'{n} {ar}', f'{n} min', f'{n} min', f'{n} min', f'{n} min')

# ---------------------------------------------------------------- how the purchase works
A('investment.copy',
  'Los documentos que tenemos no recogen ni un importe de reserva ni un calendario de pagos, por lo que los pedimos al promotor y los confirmamos por escrito antes de que reserve.',
  'Les documents dont nous disposons ne précisent ni montant de réservation ni échéancier de paiement ; nous les demandons donc au promoteur et les confirmons par écrit avant que vous ne réserviez.',
  'Die uns vorliegenden Unterlagen enthalten weder einen Reservierungsbetrag noch einen Zahlungsplan; deshalb fragen wir beides beim Bauträger an und bestätigen es Ihnen schriftlich, bevor Sie reservieren.',
  'В имеющихся у нас документах нет ни суммы бронирования, ни графика платежей, поэтому мы запрашиваем и то и другое у застройщика и подтверждаем письменно до того, как вы забронируете.',
  'لا تتضمن الوثائق التي بحوزتنا مبلغ الحجز ولا جدول الدفعات، لذلك نطلبهما من المطوّر ونؤكدهما كتابةً قبل أن تحجزوا.',
  'De documenten die wij hebben, bevatten geen reserveringsbedrag en geen betalingsschema, dus vragen wij beide bij de ontwikkelaar op en bevestigen wij ze schriftelijk voordat u reserveert.',
  'Posiadane przez nas dokumenty nie podają ani kwoty rezerwacji, ani harmonogramu płatności, dlatego prosimy o nie dewelopera i potwierdzamy je Państwu na piśmie przed rezerwacją.',
  'Dokumentene vi har oppgir verken reservasjonsbeløp eller betalingsplan, så vi ber utbyggeren om begge deler og bekrefter dem skriftlig før dere reserverer.',
  'De dokument vi har anger varken reservationsbelopp eller betalningsplan, så vi ber exploatören om båda och bekräftar dem skriftligen innan ni reserverar.')
A('investment.cards[0][0]', 'Reserva y pagos', 'Réservation et paiements', 'Reservierung und Zahlungen', 'Бронирование и платежи',
  'الحجز والدفعات', 'Reservering en betalingen', 'Rezerwacja i płatności', 'Reservasjon og betalinger', 'Reservation och betalningar')
A('investment.cards[0][1]',
  'Ningún documento que tenemos indica el importe de la reserva, los pagos o sus fechas. Los pedimos y ponemos las respuestas por escrito antes de que reserve.',
  'Aucun document dont nous disposons n’indique le montant de la réservation, les échéances ou leurs dates. Nous les demandons et consignons les réponses par écrit avant que vous ne réserviez.',
  'Keine der uns vorliegenden Unterlagen nennt den Reservierungsbetrag, die Raten oder deren Termine. Wir fragen sie an und halten die Antworten schriftlich fest, bevor Sie reservieren.',
  'Ни в одном из имеющихся у нас документов нет суммы бронирования, платежей и их сроков. Мы запрашиваем их и фиксируем ответы письменно до вашего бронирования.',
  'لا تذكر أي وثيقة بحوزتنا مبلغ الحجز أو الدفعات أو مواعيدها. نطلبها ونضع الإجابات كتابةً قبل أن تحجزوا.',
  'Geen van de documenten die wij hebben, geeft het reserveringsbedrag, de termijnen of hun data. Wij vragen ze op en leggen de antwoorden schriftelijk vast voordat u reserveert.',
  'Żaden z posiadanych przez nas dokumentów nie podaje kwoty rezerwacji, rat ani ich terminów. Prosimy o nie i przekazujemy odpowiedzi na piśmie przed rezerwacją.',
  'Ingen av dokumentene vi har oppgir reservasjonsbeløpet, delbetalingene eller datoene for dem. Vi ber om dem og gir svarene skriftlig før dere reserverer.',
  'Inget av de dokument vi har anger reservationsbeloppet, delbetalningarna eller deras datum. Vi ber om dem och ger svaren skriftligen innan ni reserverar.')
A('investment.cards[1][1]',
  'La lista de precios no menciona el IVA. Mostramos los precios como cifras netas más IVA, como es habitual en las viviendas nuevas en España, y confirmamos por escrito el tipo y los demás gastos de compra.',
  'La liste de prix ne mentionne pas la TVA. Nous présentons les prix comme des montants nets hors TVA, comme c’est l’usage pour les logements neufs en Espagne, et confirmons par écrit le taux et les autres frais d’achat.',
  'Die Preisliste erwähnt die MwSt. nicht. Wir zeigen die Preise als Nettobeträge zuzüglich MwSt., wie es bei Neubauwohnungen in Spanien üblich ist, und bestätigen den Satz und die übrigen Kaufnebenkosten schriftlich.',
  'В прайс-листе НДС не упоминается. Мы показываем цены как суммы без НДС, как это принято для новых квартир в Испании, а ставку и другие расходы на покупку подтверждаем письменно.',
  'لا تذكر قائمة الأسعار ضريبة القيمة المضافة. نعرض الأسعار بصفتها مبالغ صافية تُضاف إليها الضريبة، كما هو معتاد في المساكن الجديدة في إسبانيا، ونؤكد النسبة وسائر تكاليف الشراء كتابةً.',
  'De prijslijst vermeldt de btw niet. Wij tonen de prijzen als nettobedragen plus btw, zoals gebruikelijk bij nieuwbouwwoningen in Spanje, en bevestigen het tarief en de overige aankoopkosten schriftelijk.',
  'Cennik nie wspomina o VAT. Pokazujemy ceny jako kwoty netto plus VAT, tak jak to jest zwyczajowo przy nowych mieszkaniach w Hiszpanii, a stawkę i pozostałe koszty zakupu potwierdzamy na piśmie.',
  'Prislisten nevner ikke mva. Vi viser prisene som nettobeløp pluss mva., slik det er vanlig for nye boliger i Spania, og bekrefter satsen og de øvrige kjøpskostnadene skriftlig.',
  'Prislistan nämner inte IVA (spansk moms). Vi visar priserna som nettobelopp plus IVA, så som är brukligt för nya bostäder i Spanien, och bekräftar skattesatsen och de övriga köpkostnaderna skriftligen.')
A('investment.cards[2][1]',
  'La lista de precios da un precio por vivienda y no indica qué incluye. El dosier muestra dos plantas de sótano con plazas de garaje y trasteros, y confirmamos por escrito si una plaza y un trastero van con la vivienda que elija. El mobiliario que aparece en las imágenes no está incluido.',
  'La liste de prix donne un prix par logement et n’indique pas ce qu’il comprend. Le dossier montre deux niveaux de sous-sol avec places de stationnement et caves, et nous confirmons par écrit si une place et une cave sont attribuées au logement que vous choisissez. Le mobilier présenté sur les images n’est pas inclus.',
  'Die Preisliste nennt einen Preis je Wohnung und sagt nicht, was er umfasst. Das Dossier zeigt zwei Untergeschosse mit Stellplätzen und Abstellräumen, und wir bestätigen schriftlich, ob zur gewählten Wohnung ein Stellplatz und ein Abstellraum gehören. Die auf den Bildern gezeigten Möbel sind nicht enthalten.',
  'В прайс-листе указана одна цена на квартиру, и не сказано, что в неё входит. В досье показаны два подземных уровня с парковочными местами и кладовыми, и мы письменно подтверждаем, прилагаются ли к выбранной вами квартире место и кладовая. Мебель на изображениях в стоимость не входит.',
  'تذكر قائمة الأسعار سعرًا واحدًا لكل مسكن ولا تبيّن ما يشمله. ويُظهر ملف المطوّر طابقين سفليين لمواقف السيارات وغرف التخزين، ونؤكد كتابةً ما إذا كان موقف وغرفة تخزين يأتيان مع المسكن الذي تختارونه. والأثاث الظاهر في الصور غير مشمول.',
  'De prijslijst geeft één prijs per woning en zegt niet wat die omvat. Het dossier toont twee ondergrondse niveaus met parkeerplaatsen en bergingen, en wij bevestigen schriftelijk of een plaats en een berging bij de woning van uw keuze horen. De op de beelden getoonde meubels zijn niet inbegrepen.',
  'Cennik podaje jedną cenę za mieszkanie i nie mówi, co ona obejmuje. Dossier pokazuje dwa poziomy podziemne z miejscami postojowymi i komórkami lokatorskimi, a my potwierdzamy na piśmie, czy do wybranego przez Państwa mieszkania należy miejsce i komórka. Meble widoczne na wizualizacjach nie są wliczone w cenę.',
  'Prislisten oppgir én pris per bolig og sier ikke hva den omfatter. Dossieret viser to kjellernivåer med parkeringsplasser og boder, og vi bekrefter skriftlig om en plass og en bod følger med boligen dere velger. Møblene som vises på bildene er ikke inkludert.',
  'Prislistan anger ett pris per bostad och säger inte vad det omfattar. Dossiern visar två källarplan med parkeringsplatser och förråd, och vi bekräftar skriftligen om en plats och ett förråd följer med den bostad ni väljer. Möblerna som visas på bilderna ingår inte.')

# ---------------------------------------------------------------- what we check
A('trustDossier.cards[0][1]',
  'Los documentos que tenemos no indican si la licencia de obras ha sido concedida ni si las obras han comenzado, y las imágenes están generadas por ordenador. Pedimos la licencia, la fecha de inicio de las obras y la garantía bancaria que cubre las cantidades entregadas a cuenta.',
  'Les documents dont nous disposons n’indiquent pas si le permis de construire a été accordé ni si les travaux ont commencé, et les images sont de synthèse. Nous demandons le permis, la date de démarrage des travaux et la garantie bancaire qui couvre les sommes versées en acompte.',
  'Die uns vorliegenden Unterlagen sagen nicht, ob die Baugenehmigung erteilt wurde oder ob die Bauarbeiten begonnen haben, und die Bilder sind computergeneriert. Wir fragen die Genehmigung, den Baubeginn und die Bankgarantie an, die geleistete Anzahlungen absichert.',
  'В имеющихся у нас документах не сказано, выдано ли разрешение на строительство и начаты ли работы, а изображения созданы на компьютере. Мы запрашиваем разрешение, дату начала работ и банковскую гарантию, покрывающую суммы, внесённые авансом.',
  'لا تبيّن الوثائق التي بحوزتنا ما إذا كانت رخصة البناء قد مُنحت أو ما إذا كانت الأعمال قد بدأت، والصور مُولَّدة بالحاسوب. نطلب الرخصة وتاريخ بدء الأعمال والضمان المصرفي الذي يغطي المبالغ المدفوعة مقدمًا.',
  'De documenten die wij hebben, geven niet aan of de bouwvergunning is verleend of dat de werken zijn gestart, en de beelden zijn computergegenereerd. Wij vragen de vergunning, de startdatum van de werken en de bankgarantie die vooruitbetaalde bedragen dekt op.',
  'Posiadane przez nas dokumenty nie podają, czy pozwolenie na budowę zostało wydane ani czy prace się rozpoczęły, a wizualizacje są komputerowe. Prosimy o pozwolenie, datę rozpoczęcia prac oraz gwarancję bankową obejmującą wpłacone zaliczki.',
  'Dokumentene vi har oppgir ikke om byggetillatelsen er gitt eller om byggearbeidene er startet, og bildene er datagenererte. Vi ber om tillatelsen, startdatoen for arbeidene og bankgarantien som dekker beløp betalt på forhånd.',
  'De dokument vi har anger inte om bygglovet har beviljats eller om byggarbetena har påbörjats, och bilderna är datorgenererade. Vi ber om bygglovet, startdatumet för arbetena och bankgarantin som täcker belopp som betalats i förskott.')
A('trustDossier.cards[1][1]',
  'Ningún documento que tenemos da una fecha de entrega, por lo que pedimos la fecha contractual del bloque que elija y la ponemos por escrito.',
  'Aucun document dont nous disposons ne donne de date de livraison ; nous demandons donc la date contractuelle du bloc que vous choisissez et la consignons par écrit.',
  'Keine der uns vorliegenden Unterlagen nennt einen Übergabetermin; deshalb fragen wir den vertraglichen Termin für den von Ihnen gewählten Block an und halten ihn schriftlich fest.',
  'Ни в одном из имеющихся у нас документов нет срока сдачи, поэтому мы запрашиваем договорную дату для выбранного вами корпуса и фиксируем её письменно.',
  'لا تذكر أي وثيقة بحوزتنا موعد تسليم، لذلك نطلب الموعد التعاقدي للمبنى الذي تختارونه ونضعه كتابةً.',
  'Geen van de documenten die wij hebben, geeft een opleveringsdatum, dus vragen wij de contractuele datum voor het blok van uw keuze op en leggen die schriftelijk vast.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu oddania, dlatego prosimy o termin umowny dla wybranego przez Państwa bloku i potwierdzamy go na piśmie.',
  'Ingen av dokumentene vi har oppgir en overleveringsdato, så vi ber om den kontraktsfestede datoen for huset dere velger og setter den skriftlig.',
  'Inget av de dokument vi har anger ett tillträdesdatum, så vi ber om det avtalade datumet för det hus ni väljer och sätter det skriftligen.')
A('trustDossier.cards[2][1]',
  'La lista de precios y los planos de planta coinciden en las superficies construida, interior y de terraza de las 15 viviendas. Las hojas de la planta de cubierta de cinco de los seis áticos imprimen un total interior distinto, {N58.97} {U} frente a {N57.48} en el 3-3-D, y los planos dan el solárium de tres áticos de forma ligeramente distinta: {N106.77} {U} frente a {N106.67} en el 1-3-B, {N22.70} frente a {N22.73} en el 2-3-D y {N20.55} frente a {N20.57} en el 3-3-D. El dosier da además superficies mayores según el Decreto 218/2005, {N87.79} {U} interiores y {N99.66} construidos para la 1-1-C frente a {N76.89} y {N91.68} de la lista. Confirmamos qué cifras utiliza el contrato.',
  'La liste de prix et les plans d’étage concordent sur les surfaces construite, intérieure et de terrasse des 15 logements. Les feuilles du niveau toiture de cinq des six penthouses impriment un total intérieur différent, {N58.97} {U} contre {N57.48} pour le 3-3-D, et les plans donnent le solarium de trois penthouses de façon légèrement différente : {N106.77} {U} contre {N106.67} pour le 1-3-B, {N22.70} contre {N22.73} pour le 2-3-D et {N20.55} contre {N20.57} pour le 3-3-D. Le dossier donne aussi des surfaces plus grandes selon le décret 218/2005, {N87.79} {U} intérieurs et {N99.66} construits pour le 1-1-C contre {N76.89} et {N91.68} sur la liste. Nous confirmons quels chiffres le contrat retient.',
  'Die Preisliste und die Geschosspläne stimmen bei der bebauten Fläche, der Innenfläche und der Terrassenfläche aller 15 Wohnungen überein. Die Dachebenen-Blätter von fünf der sechs Penthäuser weisen eine abweichende Innenfläche in der Summe aus, {N58.97} {U} gegenüber {N57.48} bei 3-3-D, und die Pläne geben das Solarium von drei Penthäusern geringfügig anders an: {N106.77} {U} gegenüber {N106.67} bei 1-3-B, {N22.70} gegenüber {N22.73} bei 2-3-D und {N20.55} gegenüber {N20.57} bei 3-3-D. Das Dossier nennt außerdem größere Flächen nach dem Dekret 218/2005, {N87.79} {U} innen und {N99.66} bebaut bei 1-1-C gegenüber {N76.89} und {N91.68} in der Liste. Wir bestätigen, welche Zahlen der Vertrag verwendet.',
  'Прайс-лист и поэтажные планы совпадают по застроенной, внутренней площади и площади террас всех 15 квартир. На листах уровня крыши пяти из шести пентхаусов напечатан другой итог внутренней площади — {N58.97} {U} против {N57.48} у 3-3-D, а планы указывают солярий трёх пентхаусов немного иначе: {N106.77} {U} против {N106.67} у 1-3-B, {N22.70} против {N22.73} у 2-3-D и {N20.55} против {N20.57} у 3-3-D. Кроме того, в досье приведены бо́льшие площади по Декрету 218/2005 — {N87.79} {U} внутренней и {N99.66} застроенной для 1-1-C против {N76.89} и {N91.68} в прайс-листе. Мы уточняем, какие цифры использует договор.',
  'تتفق قائمة الأسعار ومخططات الطوابق على المساحة المبنية والداخلية ومساحة التراس لجميع المساكن الخمسة عشر. أما أوراق مستوى السطح لخمسة من البنتهاوس الستة فتطبع مجموعًا داخليًا مختلفًا، {N58.97} {U} مقابل {N57.48} للمسكن 3-3-D، وتعطي المخططات سولاريوم ثلاثة بنتهاوس بفروق طفيفة: {N106.77} {U} مقابل {N106.67} للمسكن 1-3-B و{N22.70} مقابل {N22.73} للمسكن 2-3-D و{N20.55} مقابل {N20.57} للمسكن 3-3-D. ويذكر الملف أيضًا مساحات أكبر بموجب المرسوم 218/2005، {N87.79} {U} داخلية و{N99.66} مبنية للمسكن 1-1-C مقابل {N76.89} و{N91.68} في القائمة. ونؤكد أي الأرقام يعتمدها العقد.',
  'De prijslijst en de verdiepingsplattegronden komen overeen voor de bebouwde, binnen- en terrasoppervlakte van alle 15 woningen. De bladen van het dakniveau van vijf van de zes penthouses geven een ander totaal voor de binnenoppervlakte, {N58.97} {U} tegen {N57.48} bij 3-3-D, en de plattegronden geven het solarium van drie penthouses licht afwijkend: {N106.77} {U} tegen {N106.67} bij 1-3-B, {N22.70} tegen {N22.73} bij 2-3-D en {N20.55} tegen {N20.57} bij 3-3-D. Het dossier geeft bovendien grotere oppervlakten volgens Decreet 218/2005, {N87.79} {U} binnen en {N99.66} bebouwd voor 1-1-C tegen {N76.89} en {N91.68} op de lijst. Wij bevestigen welke cijfers het contract gebruikt.',
  'Cennik i rzuty kondygnacji zgadzają się co do powierzchni zabudowy, wewnętrznej i tarasów wszystkich 15 mieszkań. Arkusze poziomu dachu pięciu z sześciu penthouse’ów podają inną sumę powierzchni wewnętrznej, {N58.97} {U} wobec {N57.48} w 3-3-D, a rzuty podają solarium trzech penthouse’ów nieco inaczej: {N106.77} {U} wobec {N106.67} w 1-3-B, {N22.70} wobec {N22.73} w 2-3-D i {N20.55} wobec {N20.57} w 3-3-D. Dossier podaje też większe powierzchnie według dekretu 218/2005, {N87.79} {U} wewnętrznej i {N99.66} zabudowy dla 1-1-C wobec {N76.89} i {N91.68} w cenniku. Potwierdzamy, z jakich wartości korzysta umowa.',
  'Prislisten og etasjeplanene stemmer overens om bebygd areal, innvendig areal og terrasseareal for alle 15 boligene. Arkene for takplanet til fem av de seks toppleilighetene oppgir en annen innvendig sum, {N58.97} {U} mot {N57.48} for 3-3-D, og plantegningene oppgir solterrassen til tre toppleiligheter litt annerledes: {N106.77} {U} mot {N106.67} for 1-3-B, {N22.70} mot {N22.73} for 2-3-D og {N20.55} mot {N20.57} for 3-3-D. Dossieret oppgir dessuten større arealer etter dekret 218/2005, {N87.79} {U} innvendig og {N99.66} bebygd for 1-1-C mot {N76.89} og {N91.68} i listen. Vi bekrefter hvilke tall kontrakten bruker.',
  'Prislistan och våningsplanen stämmer överens om byggyta, inomhusyta och terrassyta för alla 15 bostäderna. Arken för takplanet för fem av de sex takvåningarna anger en annan summa för inomhusytan, {N58.97} {U} mot {N57.48} för 3-3-D, och planritningarna anger solterrassen för tre takvåningar något annorlunda: {N106.77} {U} mot {N106.67} för 1-3-B, {N22.70} mot {N22.73} för 2-3-D och {N20.55} mot {N20.57} för 3-3-D. Dossiern anger dessutom större ytor enligt dekret 218/2005, {N87.79} {U} inomhus och {N99.66} byggyta för 1-1-C mot {N76.89} och {N91.68} i listan. Vi bekräftar vilka siffror avtalet använder.')
A('trustDossier.cards[3][0]', 'Las piscinas de los áticos', 'Les piscines des penthouses', 'Die Penthouse-Pools', 'Бассейны пентхаусов',
  'مسابح البنتهاوس', 'De penthouse-zwembaden', 'Baseny w penthouse’ach', 'Bassengene på toppleilighetene', 'Takvåningarnas pooler')
A('trustDossier.cards[3][1]',
  'La memoria indica una piscina de {N3.00} x {N2.00} m y una ducha exterior exclusivas de los áticos, pero los planos muestran una piscina solo en el 1-3-B y el 3-3-A, que son también los dos que la lista de precios marca con vista a la piscina. Los otros cuatro muestran un solárium sin piscina. Confirmamos por escrito qué áticos incluyen piscina.',
  'Le descriptif indique une piscine de {N3.00} x {N2.00} m et une douche extérieure réservées aux penthouses, mais les plans ne montrent une piscine que sur le 1-3-B et le 3-3-A, qui sont aussi les deux que la liste de prix signale avec vue sur la piscine. Les quatre autres montrent un solarium sans piscine. Nous confirmons par écrit quels penthouses comprennent une piscine.',
  'Die Baubeschreibung nennt einen Pool von {N3.00} x {N2.00} m und eine Außendusche ausschließlich für Penthäuser, doch die Planblätter zeigen nur bei 1-3-B und 3-3-A einen Pool, und das sind auch die beiden, die die Preisliste mit Poolblick kennzeichnet. Die übrigen vier zeigen ein Solarium ohne Pool. Wir bestätigen schriftlich, welche Penthäuser einen Pool haben.',
  'В спецификации бассейн {N3.00} x {N2.00} м и уличный душ указаны только для пентхаусов, но на планировках бассейн показан лишь у 1-3-B и 3-3-A — и именно их прайс-лист отмечает видом на бассейн. У остальных четырёх показан солярий без бассейна. Мы письменно подтверждаем, в каких пентхаусах есть бассейн.',
  'تذكر المواصفات مسبحًا بقياس {N3.00} × {N2.00} م ودشًا خارجيًا حصريًا للبنتهاوس، لكن المخططات تُظهر مسبحًا فقط في 1-3-B و3-3-A، وهما أيضًا اللذان تشير إليهما قائمة الأسعار بإطلالة على المسبح. أما الأربعة الباقية فتُظهر سولاريوم دون مسبح. ونؤكد كتابةً أي البنتهاوس يشمل مسبحًا.',
  'De specificatie vermeldt een zwembad van {N3.00} x {N2.00} m en een buitendouche uitsluitend bij penthouses, maar de plattegronden tonen alleen bij 1-3-B en 3-3-A een zwembad, en dat zijn ook de twee die de prijslijst met zwembadzicht markeert. De overige vier tonen een solarium zonder zwembad. Wij bevestigen schriftelijk welke penthouses een zwembad hebben.',
  'Specyfikacja podaje basen {N3.00} x {N2.00} m i prysznic zewnętrzny wyłącznie dla penthouse’ów, lecz rzuty pokazują basen tylko przy 1-3-B i 3-3-A, które są też jedynymi dwoma oznaczonymi w cenniku widokiem na basen. Pozostałe cztery pokazują solarium bez basenu. Potwierdzamy na piśmie, które penthouse’y mają basen.',
  'Spesifikasjonen oppgir et basseng på {N3.00} x {N2.00} m og en utendørs dusj kun for toppleilighetene, men plantegningene viser bare et basseng på 1-3-B og 3-3-A, som også er de to prislisten merker med bassengutsikt. De fire andre viser en solterrasse uten basseng. Vi bekrefter skriftlig hvilke toppleiligheter som har basseng.',
  'Beskrivningen anger en pool på {N3.00} x {N2.00} m och en utomhusdusch endast för takvåningarna, men planritningarna visar bara en pool på 1-3-B och 3-3-A, som också är de två som prislistan markerar med poolutsikt. De övriga fyra visar en solterrass utan pool. Vi bekräftar skriftligen vilka takvåningar som har pool.')
A('trustDossier.cards[4][1]',
  'El dosier describe las viviendas con dos y tres dormitorios en un pasaje y con uno, dos y tres en otro. La lista de precios tiene una vivienda de un dormitorio, y está reservada; las 15 viviendas a la venta tienen dos o tres dormitorios.',
  'Le dossier décrit les logements comme ayant deux et trois chambres dans un passage et une, deux et trois dans un autre. La liste de prix compte un logement d’une chambre, qui est réservé ; les 15 logements annoncés ont deux ou trois chambres.',
  'Das Dossier beschreibt die Wohnungen an einer Stelle mit zwei und drei Schlafzimmern und an einer anderen mit einem, zwei und drei. Die Preisliste enthält eine Wohnung mit einem Schlafzimmer, und sie ist reserviert; alle 15 gelisteten Wohnungen haben zwei oder drei Schlafzimmer.',
  'В одном месте досье у квартир указаны две и три спальни, в другом — одна, две и три. В прайс-листе есть одна квартира с одной спальней, и она зарезервирована; у всех 15 квартир в продаже две или три спальни.',
  'يصف ملف المطوّر المساكن في موضع بأنها بغرفتين وثلاث غرف نوم، وفي موضع آخر بغرفة وغرفتين وثلاث غرف نوم. وفي قائمة الأسعار مسكن واحد بغرفة نوم واحدة وهو محجوز؛ وجميع المساكن الخمسة عشر المعروضة بغرفتين أو ثلاث غرف نوم.',
  'Het dossier beschrijft de woningen op de ene plaats met twee en drie slaapkamers en op een andere met een, twee en drie. De prijslijst bevat één woning met één slaapkamer, en die is gereserveerd; alle 15 aangeboden woningen hebben twee of drie slaapkamers.',
  'Dossier w jednym miejscu opisuje mieszkania jako mające dwie i trzy sypialnie, w innym — jedną, dwie i trzy. Cennik zawiera jedno mieszkanie z jedną sypialnią i jest ono zarezerwowane; wszystkie 15 oferowanych mieszkań ma dwie lub trzy sypialnie.',
  'Dossieret beskriver boligene med to og tre soverom ett sted og med ett, to og tre et annet sted. Prislisten har én bolig med ett soverom, og den er reservert; alle de 15 annonserte boligene har to eller tre soverom.',
  'Dossiern beskriver bostäderna med två och tre sovrum på ett ställe och med ett, två och tre på ett annat. Prislistan har en bostad med ett sovrum, och den är reserverad; alla 15 listade bostäder har två eller tre sovrum.')
A('trustDossier.cards[5][1]',
  'Los tiempos de esta página son los del promotor, de su mapa de ubicación y su texto, y ninguno dice cómo se recorren. Las cifras por carretera junto al mapa se miden desde un punto aproximado de Estepona y difieren de ellos, por lo que confirmamos las distancias en una visita.',
  'Les durées de cette page sont celles du promoteur, tirées de sa carte de localisation et de son texte, et aucune ne dit comment elle est parcourue. Les chiffres routiers à côté de la carte sont mesurés depuis un point approximatif d’Estepona et en diffèrent ; nous confirmons donc les distances lors d’une visite.',
  'Die Zeiten auf dieser Seite stammen vom Bauträger, aus seiner Lagekarte und seinem Text, und keines der beiden sagt, wie sie zurückgelegt werden. Die Straßenangaben neben der Karte sind von einem ungefähren Punkt in Estepona aus gemessen und weichen davon ab, deshalb bestätigen wir die Entfernungen bei einem Besuch.',
  'Время в пути на этой странице взято у застройщика — с его карты расположения и из текста, и ни там, ни там не сказано, как оно преодолевается. Расстояния по дорогам рядом с картой измерены от приблизительной точки в Эстепоне и отличаются от них, поэтому мы подтверждаем расстояния во время визита.',
  'الأوقات المذكورة في هذه الصفحة هي أوقات المطوّر، من خريطة الموقع ومن نصّه، ولا يبيّن أيٌّ منهما كيف تُقطع. أما أرقام الطرق بجانب الخريطة فمقاسة من نقطة تقريبية في إستيبونا وتختلف عنها، لذلك نؤكد المسافات خلال زيارة.',
  'De tijden op deze pagina zijn die van de ontwikkelaar, uit zijn locatiekaart en tekst, en geen van beide zegt hoe ze worden afgelegd. De wegafstanden naast de kaart zijn gemeten vanaf een bij benadering bepaald punt in Estepona en wijken ervan af, dus bevestigen wij de afstanden bij een bezoek.',
  'Czasy podane na tej stronie pochodzą od dewelopera, z jego mapy lokalizacji i tekstu, i żadne z tych źródeł nie mówi, jak się je pokonuje. Odległości drogowe obok mapy zmierzono od przybliżonego punktu w Esteponie i różnią się od nich, dlatego odległości potwierdzamy podczas wizyty.',
  'Tidene på denne siden er utbyggerens, fra kartet over beliggenheten og teksten, og ingen av dem sier hvordan de tilbakelegges. Veiavstandene ved siden av kartet er målt fra et omtrentlig punkt i Estepona og avviker fra dem, så vi bekrefter avstandene på en visning.',
  'Tiderna på den här sidan är exploatörens, från lägeskartan och texten, och ingen av dem säger hur de tillryggaläggs. Vägavstånden vid sidan av kartan är mätta från en ungefärlig punkt i Estepona och avviker från dem, så vi bekräftar avstånden vid ett besök.')

# ---------------------------------------------------------------- availability
A('availability.headlineHtml', '15 de 48 viviendas <em>a la venta actualmente</em>', '15 logements sur 48 <em>actuellement annoncés</em>',
  '15 von 48 Wohnungen <em>derzeit verfügbar</em>', '15 из 48 квартир <em>сейчас в продаже</em>',
  '15 من أصل 48 مسكنًا <em>معروضة حاليًا</em>', '15 van de 48 woningen <em>momenteel beschikbaar</em>',
  '15 z 48 mieszkań <em>obecnie dostępnych</em>', '15 av 48 boliger <em>ledige nå</em>', '15 av 48 bostäder <em>lediga just nu</em>')
A('availability.copy',
  'Figuran quince viviendas con precio: tres en planta baja con patio, seis en las plantas primera y segunda y seis áticos con solárium. Los precios son los de la lista de precios del promotor titulada noviembre de 2026, sin IVA; la misma lista marca las otras 33 viviendas como reservadas, y confirmamos la disponibilidad y el precio antes de cualquier reserva.',
  'Quinze logements figurent avec un prix : trois au rez-de-chaussée avec patio, six au premier et au deuxième étage et six penthouses avec solarium. Les prix sont ceux de la liste de prix du promoteur intitulée novembre 2026, hors TVA ; la même liste marque les 33 autres logements comme réservés, et nous confirmons la disponibilité et le prix avant toute réservation.',
  'Fünfzehn Wohnungen sind mit Preis gelistet: drei im Erdgeschoss mit Patio, sechs im ersten und zweiten Obergeschoss und sechs Penthäuser mit Solarium. Die Preise sind die der Preisliste des Bauträgers mit der Überschrift November 2026, ohne MwSt.; dieselbe Liste kennzeichnet die übrigen 33 Wohnungen als reserviert, und wir bestätigen Verfügbarkeit und Preis vor jeder Reservierung.',
  'С ценой указаны пятнадцать квартир: три на первом этаже с патио, шесть на втором и третьем этажах и шесть пентхаусов с солярием. Цены взяты из прайс-листа застройщика с заголовком «ноябрь 2026» и приведены без НДС; тот же список помечает остальные 33 квартиры как зарезервированные, а наличие и цену мы подтверждаем до любого бронирования.',
  'يُدرج سعر لخمسة عشر مسكنًا: ثلاثة في الطابق الأرضي مع فناء، وستة في الطابقين الأول والثاني، وستة بنتهاوس مع سولاريوم. والأسعار هي أسعار قائمة المطوّر المعنونة بنوفمبر 2026، دون ضريبة القيمة المضافة؛ وتُدرج القائمة نفسها المساكن الـ33 الباقية على أنها محجوزة، ونؤكد التوافر والسعر قبل أي حجز.',
  'Vijftien woningen staan met een prijs op de lijst: drie op de begane grond met een patio, zes op de eerste en tweede verdieping en zes penthouses met een solarium. De prijzen zijn die van de prijslijst van de ontwikkelaar met de kop november 2026, zonder btw; dezelfde lijst markeert de andere 33 woningen als gereserveerd, en wij bevestigen beschikbaarheid en prijs vóór elke reservering.',
  'Piętnaście mieszkań ma podaną cenę: trzy na parterze z patio, sześć na pierwszym i drugim piętrze oraz sześć penthouse’ów z solarium. Ceny pochodzą z cennika dewelopera z nagłówkiem listopad 2026, bez VAT; ta sama lista oznacza pozostałe 33 mieszkania jako zarezerwowane, a dostępność i cenę potwierdzamy przed każdą rezerwacją.',
  'Femten boliger er oppført med pris: tre i første etasje med patio, seks i andre og tredje etasje og seks toppleiligheter med solterrasse. Prisene er de i utbyggerens prisliste med overskriften november 2026, uten mva.; den samme listen markerer de øvrige 33 boligene som reservert, og vi bekrefter tilgjengelighet og pris før enhver reservasjon.',
  'Femton bostäder är listade med pris: tre på bottenvåningen med patio, sex på första och andra våningen och sex takvåningar med solterrass. Priserna är de i exploatörens prislista med rubriken november 2026, utan IVA; samma lista markerar de övriga 33 bostäderna som reserverade, och vi bekräftar tillgänglighet och pris före varje reservation.')
A('availability.sourceNote',
  'Los precios, los dormitorios y las superficies están transcritos de la lista de precios del promotor titulada noviembre de 2026, para las 15 viviendas de las 48 a las que da precio; marca las otras 33 como reservadas. La lista no menciona el IVA, por lo que mostramos los precios como cifras netas más IVA. Los planos de venta del promotor coinciden con la lista en las superficies construida, interior y de terraza de las 15 viviendas y difieren en tres superficies de solárium, que se detallan en las comprobaciones de arriba; el dosier da además superficies mayores según el Decreto 218/2005, que no utilizamos.',
  'Les prix, les chambres et les surfaces sont transcrits de la liste de prix du promoteur intitulée novembre 2026, pour les 15 logements sur 48 auxquels elle donne un prix ; elle marque les 33 autres comme réservés. La liste ne mentionne pas la TVA ; nous présentons donc les prix comme des montants nets hors TVA. Les plans de vente du promoteur concordent avec la liste sur les surfaces construite, intérieure et de terrasse des 15 logements et diffèrent sur trois surfaces de solarium, détaillées dans les vérifications ci-dessus ; le dossier donne aussi des surfaces plus grandes selon le décret 218/2005, que nous n’utilisons pas.',
  'Preise, Schlafzimmer und Flächen sind der Preisliste des Bauträgers mit der Überschrift November 2026 entnommen, für die 15 von 48 Wohnungen, die sie mit einem Preis aufführt; die übrigen 33 kennzeichnet sie als reserviert. Die Liste erwähnt die MwSt. nicht, daher zeigen wir die Preise als Nettobeträge zuzüglich MwSt. Die Verkaufspläne des Bauträgers stimmen mit der Liste bei der bebauten Fläche, der Innenfläche und der Terrassenfläche aller 15 Wohnungen überein und weichen bei drei Solariumflächen ab, die unter den Prüfpunkten oben aufgeführt sind; das Dossier nennt außerdem größere Flächen nach dem Dekret 218/2005, die wir nicht verwenden.',
  'Цены, число спален и площади перенесены из прайс-листа застройщика с заголовком «ноябрь 2026» для 15 квартир из 48, у которых указана цена; остальные 33 в нём помечены как зарезервированные. В прайс-листе НДС не упоминается, поэтому мы показываем цены как суммы без НДС. Продажные планы застройщика совпадают с прайс-листом по застроенной, внутренней площади и площади террас всех 15 квартир и расходятся по площади солярия у трёх, что описано в проверках выше; в досье также есть бо́льшие площади по Декрету 218/2005, которыми мы не пользуемся.',
  'الأسعار وعدد غرف النوم والمساحات منقولة من قائمة أسعار المطوّر المعنونة بنوفمبر 2026، للمساكن الخمسة عشر من أصل 48 التي تحدد لها سعرًا؛ وتُدرج الباقية، وعددها 33، على أنها محجوزة. ولا تذكر القائمة ضريبة القيمة المضافة، لذلك نعرض الأسعار بصفتها مبالغ صافية تُضاف إليها الضريبة. وتتفق مخططات البيع الخاصة بالمطوّر مع القائمة في المساحة المبنية والداخلية ومساحة التراس للمساكن الخمسة عشر، وتختلف في ثلاث مساحات للسولاريوم، وهي موضحة ضمن عمليات التحقق أعلاه؛ ويذكر الملف أيضًا مساحات أكبر بموجب المرسوم 218/2005، لا نعتمدها.',
  'Prijzen, slaapkamers en oppervlakten zijn overgenomen uit de prijslijst van de ontwikkelaar met de kop november 2026, voor de 15 van de 48 woningen waaraan zij een prijs geeft; de overige 33 markeert zij als gereserveerd. De lijst vermeldt de btw niet, dus tonen wij de prijzen als nettobedragen plus btw. De verkoopplattegronden van de ontwikkelaar komen met de lijst overeen voor de bebouwde, binnen- en terrasoppervlakte van alle 15 woningen en wijken af bij drie solariumoppervlakten, die onder de controles hierboven staan; het dossier geeft bovendien grotere oppervlakten volgens Decreet 218/2005, die wij niet gebruiken.',
  'Ceny, liczba sypialni i powierzchnie zostały przepisane z cennika dewelopera z nagłówkiem listopad 2026, dla 15 z 48 mieszkań, którym podaje on cenę; pozostałe 33 oznacza jako zarezerwowane. Cennik nie wspomina o VAT, dlatego pokazujemy ceny jako kwoty netto plus VAT. Plany sprzedażowe dewelopera zgadzają się z cennikiem co do powierzchni zabudowy, wewnętrznej i tarasów wszystkich 15 mieszkań i różnią się w trzech powierzchniach solariów, co opisano w sprawdzeniach powyżej; dossier podaje też większe powierzchnie według dekretu 218/2005, z których nie korzystamy.',
  'Priser, soverom og arealer er hentet fra utbyggerens prisliste med overskriften november 2026, for de 15 av 48 boligene den oppgir pris for; de øvrige 33 markerer den som reservert. Listen nevner ikke mva., så vi viser prisene som nettobeløp pluss mva. Utbyggerens salgstegninger stemmer med listen på bebygd areal, innvendig areal og terrasseareal for alle 15 boligene og avviker på tre solterrasseareal, som er satt opp under kontrollene ovenfor; dossieret oppgir dessuten større arealer etter dekret 218/2005, som vi ikke bruker.',
  'Priser, sovrum och ytor är hämtade från exploatörens prislista med rubriken november 2026, för de 15 av 48 bostäder den anger pris för; de övriga 33 markerar den som reserverade. Listan nämner inte IVA (spansk moms), så vi visar priserna som nettobelopp plus IVA. Exploatörens säljplaner stämmer med listan på byggyta, inomhusyta och terrassyta för alla 15 bostäderna och avviker på tre solterrassytor, som redovisas under kontrollerna ovan; dossiern anger dessutom större ytor enligt dekret 218/2005, som vi inte använder.')
A('timeline.items[3][2]',
  'Confirmamos por escrito el importe de la reserva y el calendario de pagos, y luego el contrato de compraventa.',
  'Nous confirmons par écrit le montant de la réservation et l’échéancier de paiement, puis le contrat de vente.',
  'Wir bestätigen den Reservierungsbetrag und den Zahlungsplan schriftlich, danach folgt der Kaufvertrag.',
  'Мы письменно подтверждаем сумму бронирования и график платежей, затем — договор купли-продажи.',
  'نؤكد مبلغ الحجز وجدول الدفعات كتابةً، ثم عقد البيع.',
  'Wij bevestigen het reserveringsbedrag en het betalingsschema schriftelijk, daarna volgt de koopovereenkomst.',
  'Potwierdzamy na piśmie kwotę rezerwacji i harmonogram płatności, a następnie umowę kupna.',
  'Vi bekrefter reservasjonsbeløpet og betalingsplanen skriftlig, deretter kjøpekontrakten.',
  'Vi bekräftar reservationsbeloppet och betalningsplanen skriftligen, därefter köpekontraktet.')

# the enquiry strings are Zenith Estepona's, with the name swapped
for path, src in (('enquiry.headlineHtml', 'Ask about <em>Zenith Estepona</em>'),
                  ('enquiry.message', 'Hello Nueva Living, I would like information about Zenith Estepona.')):
    en = G(path)
    T[en] = {l: TM[src][l].replace('Zenith Estepona', 'The OAK48') for l in LOCS}

# ---------------------------------------------------------------- formal address
# The shared strings below come from the translation memory, where Arabic, Polish and Norwegian carry some
# second-person singular forms. This page addresses the reader formally throughout, so those are overridden here.
def formal(en, **fix):
    base = {l: TM[en][l] for l in LOCS}
    base.update(fix)
    T[en] = base


formal('Request the project file', ar='اطلبوا ملف المشروع', pl='Prośba o dossier projektu')
formal('The plans of the homes that interest you, the quality specification and the price list.',
       ar='مخططات المساكن التي تهمكم ومواصفات الجودة وقائمة الأسعار.',
       no='Plantegningene til boligene dere er interessert i, kvalitetsspesifikasjonen og prislisten.')
formal('Compare the options', ar='قارنوا الخيارات', pl='Porównanie opcji')
formal('See this alongside the other Estepona projects we hold.', ar='شاهدوا هذا المشروع إلى جانب مشاريع إستيبونا الأخرى التي نمثّلها.')
formal('Reserve', ar='احجزوا')
formal('Visit the site and its surroundings with us.', ar='زوروا معنا موقع المشروع ومحيطه.')
formal('Tell us what you need and we will come back with current availability, the floorplans and the price list.',
       no='Fortell oss hva dere trenger, så kommer vi tilbake med gjeldende tilgjengelighet, plantegningene og prislisten.')
formal('Thank you. We will come back to you shortly with the project file.',
       ar='شكرًا لكم. سنعود إليكم قريبًا بملف المشروع.',
       pl='Dziękujemy. Wkrótce skontaktujemy się z Państwem i prześlemy dossier projektu.',
       no='Takk. Vi kommer tilbake til dere snart med prosjektdokumentasjonen.')
formal('What we check <em>before you commit</em>', no='Hva vi sjekker <em>før dere forplikter dere</em>')
T[G('enquiry.headlineHtml')]['pl'] = 'Zapytanie o <em>The OAK48</em>'
T[G('enquiry.headlineHtml')]['ar'] = 'استفسروا عن <em>The OAK48</em>'

# ---------------------------------------------------------------- FAQ
A('faq[0][1]',
  'El edificio tiene 48 viviendas y 15 figuran con precio: 13 de dos dormitorios y dos de tres, de {E375000} a {E890000} más IVA. La lista del promotor marca las otras 33 como reservadas.',
  'L’immeuble compte 48 logements et 15 figurent avec un prix : 13 de deux chambres et deux de trois, de {E375000} à {E890000} hors TVA. La liste du promoteur marque les 33 autres comme réservés.',
  'Das Gebäude hat 48 Wohnungen, und 15 sind mit Preis gelistet: 13 mit zwei und zwei mit drei Schlafzimmern, von {E375000} bis {E890000} zuzüglich MwSt. Die Liste des Bauträgers kennzeichnet die übrigen 33 als reserviert.',
  'В здании 48 квартир, и для 15 указана цена: 13 с двумя спальнями и две с тремя, от {E375000} до {E890000} без НДС. В списке застройщика остальные 33 помечены как зарезервированные.',
  'يضم المبنى 48 مسكنًا، ويُدرج سعر لـ15 منها: 13 بغرفتين واثنان بثلاث غرف، من {E375000} إلى {E890000} دون ضريبة القيمة المضافة. وتُدرج قائمة المطوّر الـ33 الباقية على أنها محجوزة.',
  'Het gebouw heeft 48 woningen en 15 staan met een prijs op de lijst: 13 met twee slaapkamers en twee met drie, van {E375000} tot {E890000} excl. btw. De lijst van de ontwikkelaar markeert de andere 33 als gereserveerd.',
  'Budynek ma 48 mieszkań, a 15 z nich ma podaną cenę: 13 z dwiema sypialniami i dwa z trzema, od {E375000} do {E890000} plus VAT. Lista dewelopera oznacza pozostałe 33 jako zarezerwowane.',
  'Bygningen har 48 boliger, og 15 er oppført med pris: 13 med to soverom og to med tre, fra {E375000} til {E890000} pluss mva. Utbyggerens liste markerer de øvrige 33 som reservert.',
  'Byggnaden har 48 bostäder och 15 är listade med pris: 13 med två sovrum och två med tre, från {E375000} till {E890000} plus IVA. Exploatörens lista markerar de övriga 33 som reserverade.')
A('faq[1][1]',
  'La lista de precios no menciona el IVA. Mostramos los precios como cifras netas más IVA, y confirmamos por escrito el tipo y los demás gastos de compra.',
  'La liste de prix ne mentionne pas la TVA. Nous présentons les prix comme des montants nets hors TVA et confirmons par écrit le taux et les autres frais d’achat.',
  'Die Preisliste erwähnt die MwSt. nicht. Wir zeigen die Preise als Nettobeträge zuzüglich MwSt. und bestätigen den Satz und die übrigen Kaufnebenkosten schriftlich.',
  'В прайс-листе НДС не упоминается. Мы показываем цены как суммы без НДС, а ставку и другие расходы на покупку подтверждаем письменно.',
  'لا تذكر قائمة الأسعار ضريبة القيمة المضافة. نعرض الأسعار بصفتها مبالغ صافية تُضاف إليها الضريبة، ونؤكد النسبة وسائر تكاليف الشراء كتابةً.',
  'De prijslijst vermeldt de btw niet. Wij tonen de prijzen als nettobedragen plus btw en bevestigen het tarief en de overige aankoopkosten schriftelijk.',
  'Cennik nie wspomina o VAT. Pokazujemy ceny jako kwoty netto plus VAT, a stawkę i pozostałe koszty zakupu potwierdzamy na piśmie.',
  'Prislisten nevner ikke mva. Vi viser prisene som nettobeløp pluss mva., og bekrefter satsen og de øvrige kjøpskostnadene skriftlig.',
  'Prislistan nämner inte IVA. Vi visar priserna som nettobelopp plus IVA och bekräftar skattesatsen och de övriga köpkostnaderna skriftligen.')
A('faq[2][1]',
  'El dosier muestra dos plantas de sótano con plazas de garaje y trasteros, y la memoria incluye la preinstalación de carga para coche eléctrico. La lista de precios no indica si una plaza y un trastero van con cada vivienda, por lo que lo confirmamos para la vivienda que elija.',
  'Le dossier montre deux niveaux de sous-sol avec places de stationnement et caves, et le descriptif prévoit le pré-équipement pour la recharge de voiture électrique. La liste de prix n’indique pas si une place et une cave sont attribuées à chaque logement ; nous le confirmons donc pour le logement que vous choisissez.',
  'Das Dossier zeigt zwei Untergeschosse mit Stellplätzen und Abstellräumen, und die Baubeschreibung enthält die Vorinstallation für das Laden von Elektroautos. Die Preisliste sagt nicht, ob zu jeder Wohnung ein Stellplatz und ein Abstellraum gehören; wir bestätigen das für die von Ihnen gewählte Wohnung.',
  'В досье показаны два подземных уровня с парковочными местами и кладовыми, а в спецификации предусмотрена подготовка к зарядке электромобилей. В прайс-листе не сказано, прилагаются ли к каждой квартире место и кладовая, поэтому мы подтверждаем это для выбранной вами квартиры.',
  'يُظهر ملف المطوّر طابقين سفليين لمواقف السيارات وغرف التخزين، وتتضمن المواصفات تجهيزًا مسبقًا لشحن السيارات الكهربائية. ولا تبيّن قائمة الأسعار ما إذا كان موقف وغرفة تخزين يأتيان مع كل مسكن، لذلك نؤكد ذلك للمسكن الذي تختارونه.',
  'Het dossier toont twee ondergrondse niveaus met parkeerplaatsen en bergingen, en de specificatie omvat de voorbereiding voor het opladen van elektrische auto’s. De prijslijst zegt niet of bij elke woning een plaats en een berging horen, dus bevestigen wij dat voor de woning van uw keuze.',
  'Dossier pokazuje dwa poziomy podziemne z miejscami postojowymi i komórkami lokatorskimi, a specyfikacja obejmuje przygotowanie do ładowania samochodów elektrycznych. Cennik nie mówi, czy do każdego mieszkania należy miejsce i komórka, dlatego potwierdzamy to dla wybranego przez Państwa mieszkania.',
  'Dossieret viser to kjellernivåer med parkeringsplasser og boder, og spesifikasjonen omfatter forberedelse for lading av elbil. Prislisten sier ikke om en plass og en bod følger med hver bolig, så vi bekrefter det for boligen dere velger.',
  'Dossiern visar två källarplan med parkeringsplatser och förråd, och beskrivningen omfattar förberedelse för laddning av elbil. Prislistan säger inte om en plats och ett förråd följer med varje bostad, så vi bekräftar det för den bostad ni väljer.')
A('faq[3][1]',
  'Ninguno de los documentos que tenemos da una fecha de entrega ni un estado de las obras. Pedimos la fecha contractual y la ponemos por escrito.',
  'Aucun des documents dont nous disposons ne donne de date de livraison ni d’avancement des travaux. Nous demandons la date contractuelle et la consignons par écrit.',
  'Keine der uns vorliegenden Unterlagen nennt einen Übergabetermin oder einen Baufortschritt. Wir fragen den vertraglichen Termin an und halten ihn schriftlich fest.',
  'Ни в одном из имеющихся у нас документов нет срока сдачи или сведений о ходе работ. Мы запрашиваем договорную дату и фиксируем её письменно.',
  'لا تذكر أي من الوثائق التي بحوزتنا موعد تسليم ولا مرحلة الأعمال. نطلب الموعد التعاقدي ونضعه كتابةً.',
  'Geen van de documenten die wij hebben, geeft een opleveringsdatum of een bouwstand. Wij vragen de contractuele datum op en leggen die schriftelijk vast.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu oddania ani etapu prac. Prosimy o termin umowny i potwierdzamy go na piśmie.',
  'Ingen av dokumentene vi har oppgir overleveringsdato eller byggestatus. Vi ber om den kontraktsfestede datoen og setter den skriftlig.',
  'Inget av de dokument vi har anger tillträdesdatum eller byggstatus. Vi ber om det avtalade datumet och sätter det skriftligen.')
A('faq[4][1]',
  'La memoria indica una piscina de {N3.00} x {N2.00} m para los áticos, pero los planos la muestran solo en dos de los seis a la venta, el 1-3-B y el 3-3-A. Confirmamos cuáles la incluyen.',
  'Le descriptif prévoit une piscine de {N3.00} x {N2.00} m pour les penthouses, mais les plans n’en montrent que sur deux des six annoncés, le 1-3-B et le 3-3-A. Nous confirmons lesquels en comprennent une.',
  'Die Baubeschreibung nennt für Penthäuser einen Pool von {N3.00} x {N2.00} m, doch die Pläne zeigen ihn nur bei zwei der sechs gelisteten, 1-3-B und 3-3-A. Wir bestätigen, welche einen haben.',
  'В спецификации для пентхаусов предусмотрен бассейн {N3.00} x {N2.00} м, но на планировках он показан лишь у двух из шести пентхаусов в продаже — 1-3-B и 3-3-A. Мы подтверждаем, в каких он есть.',
  'تذكر المواصفات مسبحًا بقياس {N3.00} × {N2.00} م للبنتهاوس، لكن المخططات تُظهره في اثنين فقط من الستة المعروضة، هما 1-3-B و3-3-A. ونؤكد أيها يشمله.',
  'De specificatie vermeldt een zwembad van {N3.00} x {N2.00} m voor penthouses, maar de plattegronden tonen er maar bij twee van de zes aangeboden, 1-3-B en 3-3-A. Wij bevestigen welke er een hebben.',
  'Specyfikacja podaje dla penthouse’ów basen {N3.00} x {N2.00} m, lecz rzuty pokazują go tylko przy dwóch z sześciu oferowanych, 1-3-B i 3-3-A. Potwierdzamy, które go mają.',
  'Spesifikasjonen oppgir et basseng på {N3.00} x {N2.00} m for toppleilighetene, men plantegningene viser det bare på to av de seks annonserte, 1-3-B og 3-3-A. Vi bekrefter hvilke som har det.',
  'Beskrivningen anger en pool på {N3.00} x {N2.00} m för takvåningarna, men planritningarna visar den bara på två av de sex listade, 1-3-B och 3-3-A. Vi bekräftar vilka som har en.')

# ---------------------------------------------------------------- unit sizes and floorplan labels
# Built from the per-locale pattern Zenith Estepona already uses, so one measurement is one word inside the project.
SIZE = {
  'es': ('{b} m² construidos', '{i} m² interiores', '{t} m² de terraza', '{p} m² de patio', '{s} m² de solárium', ', '),
  'fr': ('{b} m² construits', '{i} m² intérieurs', '{t} m² de terrasse', '{p} m² de patio', '{s} m² de solarium', ', '),
  'de': ('{b} m² bebaut', '{i} m² Innenfläche', '{t} m² Terrasse', '{p} m² Patio', '{s} m² Solarium', ', '),
  'ru': ('{b} м² застроенной площади', '{i} м² внутри', 'терраса {t} м²', 'патио {p} м²', 'солярий {s} м²', ', '),
  'ar': ('{b} م² مبنية', '{i} م² داخلية', '{t} م² تراس', '{p} م² فناء', '{s} م² سولاريوم', '، '),
  'nl': ('{b} m² bebouwd', '{i} m² binnen', '{t} m² terras', '{p} m² patio', '{s} m² solarium', ', '),
  'pl': ('{b} m² zabudowy', '{i} m² wnętrza', '{t} m² tarasu', '{p} m² patia', '{s} m² solarium', ', '),
  'no': ('{b} m² bebygd areal', '{i} m² innvendig', '{t} m² terrasse', '{p} m² patio', '{s} m² solterrasse', ', '),
  'sv': ('{b} m² byggyta', '{i} m² inomhus', '{t} m² terrass', '{p} m² patio', '{s} m² solterrass', ', '),
}
for u in P['availability']['units']:
    en = u['size']
    got = {}
    for seg in en.split(', '):
        m = re.fullmatch(r'([\d.]+) sqm (built|interior|terrace|patio|solarium)', seg)
        assert m, seg
        got[m.group(2)] = m.group(1)
    T[en] = {}
    for l in LOCS:
        tb, ti, tt, tp, ts, sep = SIZE[l]
        parts = [tb.format(b=num(got['built'], l)), ti.format(i=num(got['interior'], l))]
        for key, tpl, name in (('terrace', tt, 't'), ('patio', tp, 'p'), ('solarium', ts, 's')):
            if key in got:
                parts.append(tpl.format(**{name: num(got[key], l)}))
        T[en][l] = sep.join(parts).replace('m²', UNIT[l]) if l in ('ru', 'ar') else sep.join(parts)
for u in P['availability']['units']:
    ref = u['reference']
    for en_t, src in ((f'Floorplan of home {ref}', 'Floorplan of home 1-0-A0'), (f'Home {ref}', 'Home 1-0-A0')):
        T[en_t] = {l: TM[src][l].replace('1-0-A0', ref) for l in LOCS}

# ---------------------------------------------------------------- seo: left to the generated locale titles, placeholders only
for path in ('seo.title', 'seo.h1', 'seo.h1Context'):
    same(G(path))

json.dump(T, open(f'{SP}/tr_o.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', f'{SP}/tr_o.json', len(T), 'entries')
