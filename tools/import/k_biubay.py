# -*- coding: utf-8 -*-
"""Biubay: the strings the translation memory did not have.

Same shape as k_las_mesas_blue_horizon.py: keyed by the English string, read from project.json by its
path so a typo in the English cannot silently drop a translation. Tokens: {E6500000} money, {N285.64}
decimal number, {U} the area unit, {Q4}/{Q3} the locale's own quarter form, {T29.October.2026} a full
date in the form dates.mjs writes it. Unit sizes and plan captions are built from per-locale templates
at the foot of the file.
    python3 tools/import/k_biubay.py <scratch dir>      (writes <dir>/tr_n.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
QUARTER = {
    'Q3': {'es': 'T3', 'fr': 'T3', 'de': 'Q3', 'ru': '3 кв.', 'ar': 'الربع الثالث', 'nl': 'K3', 'pl': 'III kw.', 'no': 'K3', 'sv': 'K3'},
    'Q4': {'es': 'T4', 'fr': 'T4', 'de': 'Q4', 'ru': '4 кв.', 'ar': 'الربع الرابع', 'nl': 'K4', 'pl': 'IV kw.', 'no': 'K4', 'sv': 'K4'},
}
MONTH = {  # MONTH_NAMES of scripts/lib/dates.mjs, the three this page uses
    'September': {'es': 'septiembre', 'fr': 'septembre', 'de': 'September', 'ru': 'сентября', 'ar': 'سبتمبر', 'nl': 'september', 'pl': 'września', 'sv': 'september', 'no': 'september'},
    'October': {'es': 'octubre', 'fr': 'octobre', 'de': 'Oktober', 'ru': 'октября', 'ar': 'أكتوبر', 'nl': 'oktober', 'pl': 'października', 'sv': 'oktober', 'no': 'oktober'},
}
P = json.load(open('content/liora-projects/biubay/project.json'))
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def date(day, month, year, l):
    m = MONTH[month][l]
    if l == 'es': return f'{day} de {m} de {year}'
    if l == 'de': return f'{day}. {m} {year}'
    return f'{day} {m} {year}'


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    text = re.sub(r'\{Q([34])\}', lambda m: QUARTER['Q' + m.group(1)][l], text)
    text = re.sub(r'\{T(\d+)\.(\w+)\.(\d{4})\}', lambda m: date(m.group(1), m.group(2), m.group(3), l), text)
    return text.replace('{U}', UNIT[l])


def en(path):
    node = P
    for part in path.split('.'):
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def a(path_or_en, *tr):
    assert len(tr) == 9, (path_or_en[:60], len(tr))
    key = en(path_or_en) if re.fullmatch(r'[A-Za-z]+(\.[A-Za-z0-9]+)*', path_or_en) else path_or_en
    assert isinstance(key, str), path_or_en
    assert key not in T, key[:60]
    T[key] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(s):
    T[s] = {l: s for l in LOCS}


# identifiers: the project's name and its places read the same everywhere
for s in ['Biubay', 'Biubay <em>Estepona</em>']:
    same(s)

# ---- description, SEO, hero, card -------------------------------------------------------------------

a('description',
  '5 de 10 apartamentos de cuatro dormitorios en primera línea de mar en Estepona, cada uno con ascensor privado y una gran terraza, con piscinas, spa, gimnasio, sala de cine y simulador de golf comunes. En construcción, con entrega en {Q4} 2028 según la hoja informativa del promotor. Desde {E6500000} más IVA.',
  '5 appartements de quatre chambres sur 10, en bord de mer à Estepona, chacun avec ascenseur privé et grande terrasse, avec piscines, spa, salle de sport, salle de cinéma et simulateur de golf communs. En construction, livraison au {Q4} 2028 selon la fiche d’information du promoteur. À partir de {E6500000} hors TVA.',
  '5 von 10 Wohnungen mit vier Schlafzimmern direkt am Meer in Estepona, jeweils mit privatem Aufzug und großer Terrasse, mit gemeinsamen Pools, Spa, Fitnessraum, Kinoraum und Golfsimulator. Im Bau, Übergabe laut Infoblatt des Bauträgers im {Q4} 2028. Ab {E6500000} zuzüglich MwSt.',
  '5 из 10 квартир с четырьмя спальнями на берегу моря в Эстепоне, у каждой — частный лифт и большая терраса; общие бассейны, спа, тренажёрный зал, кинозал и гольф-симулятор. Строится, сдача в {Q4} 2028 года по информационному листу застройщика. От {E6500000} без НДС.',
  '5 من 10 شقق بأربع غرف نوم على الواجهة البحرية في إستيبونا، لكل منها مصعد خاص وتراس واسع، مع مسابح وسبا وصالة رياضية وغرفة سينما ومحاكي غولف مشتركة. قيد الإنشاء، والتسليم في {Q4} 2028 وفق النشرة التعريفية للمطوّر. ابتداءً من {E6500000} دون ضريبة القيمة المضافة.',
  '5 van de 10 appartementen met vier slaapkamers aan zee in Estepona, elk met eigen lift en een groot terras, met gemeenschappelijke zwembaden, spa, fitnessruimte, bioscoopzaal en golfsimulator. In aanbouw, oplevering in {Q4} 2028 volgens het infoblad van de ontwikkelaar. Vanaf {E6500000} excl. btw.',
  '5 z 10 apartamentów z czterema sypialniami przy morzu w Esteponie, każdy z prywatną windą i dużym tarasem, ze wspólnymi basenami, spa, siłownią, salą kinową i symulatorem golfa. W budowie, odbiór w {Q4} 2028 według karty informacyjnej dewelopera. Od {E6500000} plus VAT.',
  '5 av 10 leiligheter med fire soverom ved sjøen i Estepona, hver med egen heis og en stor terrasse, med felles basseng, spa, treningsrom, kinosal og golfsimulator. Under bygging, overlevering i {Q4} 2028 ifølge utbyggerens infoark. Fra {E6500000} pluss mva.',
  '5 av 10 lägenheter med fyra sovrum vid havet i Estepona, var och en med egen hiss och en stor terrass, med gemensamma pooler, spa, gym, biosalong och golfsimulator. Under uppförande, tillträde i {Q4} 2028 enligt exploatörens infoblad. Från {E6500000} plus IVA.')
a('seoDescription',
  '5 de 10 apartamentos de cuatro dormitorios en primera línea de mar en Estepona, cada uno con ascensor privado y una gran terraza, con piscinas, spa, gimnasio y sala de cine, en construcción, desde {E6500000} más IVA.',
  '5 appartements de quatre chambres sur 10, en bord de mer à Estepona, chacun avec ascenseur privé et grande terrasse, avec piscines, spa, salle de sport et salle de cinéma, en construction, à partir de {E6500000} hors TVA.',
  '5 von 10 Wohnungen mit vier Schlafzimmern direkt am Meer in Estepona, jeweils mit privatem Aufzug und großer Terrasse, mit Pools, Spa, Fitnessraum und Kinoraum, im Bau, ab {E6500000} zuzüglich MwSt.',
  '5 из 10 квартир с четырьмя спальнями на берегу моря в Эстепоне, у каждой — частный лифт и большая терраса; бассейны, спа, тренажёрный зал и кинозал, строится, от {E6500000} без НДС.',
  '5 من 10 شقق بأربع غرف نوم على الواجهة البحرية في إستيبونا، لكل منها مصعد خاص وتراس واسع، مع مسابح وسبا وصالة رياضية وغرفة سينما، قيد الإنشاء، ابتداءً من {E6500000} دون ضريبة القيمة المضافة.',
  '5 van de 10 appartementen met vier slaapkamers aan zee in Estepona, elk met eigen lift en een groot terras, met zwembaden, spa, fitnessruimte en bioscoopzaal, in aanbouw, vanaf {E6500000} excl. btw.',
  '5 z 10 apartamentów z czterema sypialniami przy morzu w Esteponie, każdy z prywatną windą i dużym tarasem, z basenami, spa, siłownią i salą kinową, w budowie, od {E6500000} plus VAT.',
  '5 av 10 leiligheter med fire soverom ved sjøen i Estepona, hver med egen heis og en stor terrasse, med basseng, spa, treningsrom og kinosal, under bygging, fra {E6500000} pluss mva.',
  '5 av 10 lägenheter med fyra sovrum vid havet i Estepona, var och en med egen hiss och en stor terrass, med pooler, spa, gym och biosalong, under uppförande, från {E6500000} plus IVA.')
a('twitterDescription',
  'Apartamentos de cuatro dormitorios en primera línea de mar en Estepona, con ascensor privado y grandes terrazas, desde {E6500000} más IVA.',
  'Appartements de quatre chambres en bord de mer à Estepona, avec ascenseur privé et grandes terrasses, à partir de {E6500000} hors TVA.',
  'Wohnungen mit vier Schlafzimmern direkt am Meer in Estepona, mit privatem Aufzug und großen Terrassen, ab {E6500000} zuzüglich MwSt.',
  'Квартиры с четырьмя спальнями на берегу моря в Эстепоне, с частным лифтом и большими террасами, от {E6500000} без НДС.',
  'شقق بأربع غرف نوم على الواجهة البحرية في إستيبونا، بمصعد خاص وتراسات واسعة، ابتداءً من {E6500000} دون ضريبة القيمة المضافة.',
  'Appartementen met vier slaapkamers aan zee in Estepona, met eigen lift en grote terrassen, vanaf {E6500000} excl. btw.',
  'Apartamenty z czterema sypialniami przy morzu w Esteponie, z prywatną windą i dużymi tarasami, od {E6500000} plus VAT.',
  'Leiligheter med fire soverom ved sjøen i Estepona, med egen heis og store terrasser, fra {E6500000} pluss mva.',
  'Lägenheter med fyra sovrum vid havet i Estepona, med egen hiss och stora terrasser, från {E6500000} plus IVA.')
a('hero.startingPrice',
  'Desde {E6500000} + IVA', 'À partir de {E6500000} + TVA', 'Ab {E6500000} + MwSt.', 'От {E6500000} + НДС', 'ابتداءً من {E6500000} + ضريبة القيمة المضافة',
  'Vanaf {E6500000} + btw', 'Od {E6500000} + VAT', 'Fra {E6500000} + mva.', 'Från {E6500000} + IVA')
a('card.meta.0.1', '{E6500000} + IVA', '{E6500000} + TVA', '{E6500000} + MwSt.', '{E6500000} + НДС', '{E6500000} + ضريبة القيمة المضافة',
  '{E6500000} + btw', '{E6500000} + VAT', '{E6500000} + mva.', '{E6500000} + IVA')
a('card.description',
  '5 de 10 apartamentos de cuatro dormitorios en primera línea de mar en Estepona, cada uno con ascensor privado y una gran terraza, con piscina exterior, spa, gimnasio y sala de cine.',
  '5 appartements de quatre chambres sur 10, en bord de mer à Estepona, chacun avec ascenseur privé et grande terrasse, avec piscine extérieure, spa, salle de sport et salle de cinéma.',
  '5 von 10 Wohnungen mit vier Schlafzimmern direkt am Meer in Estepona, jeweils mit privatem Aufzug und großer Terrasse, mit Außenpool, Spa, Fitnessraum und Kinoraum.',
  '5 из 10 квартир с четырьмя спальнями на берегу моря в Эстепоне, у каждой — частный лифт и большая терраса; открытый бассейн, спа, тренажёрный зал и кинозал.',
  '5 من 10 شقق بأربع غرف نوم على الواجهة البحرية في إستيبونا، لكل منها مصعد خاص وتراس واسع، مع مسبح خارجي وسبا وصالة رياضية وغرفة سينما.',
  '5 van de 10 appartementen met vier slaapkamers aan zee in Estepona, elk met eigen lift en een groot terras, met buitenzwembad, spa, fitnessruimte en bioscoopzaal.',
  '5 z 10 apartamentów z czterema sypialniami przy morzu w Esteponie, każdy z prywatną windą i dużym tarasem, z basenem zewnętrznym, spa, siłownią i salą kinową.',
  '5 av 10 leiligheter med fire soverom ved sjøen i Estepona, hver med egen heis og en stor terrasse, med utendørsbasseng, spa, treningsrom og kinosal.',
  '5 av 10 lägenheter med fyra sovrum vid havet i Estepona, var och en med egen hiss och en stor terrass, med utomhuspool, spa, gym och biosalong.')
a('quickFacts.5.1', 'Piscinas, spa, gimnasio, cine', 'Piscines, spa, salle de sport, cinéma', 'Pools, Spa, Fitnessraum, Kino',
  'Бассейны, спа, тренажёрный зал, кинозал', 'مسابح، سبا، صالة رياضية، سينما', 'Zwembaden, spa, fitnessruimte, bioscoop',
  'Baseny, spa, siłownia, kino', 'Basseng, spa, treningsrom, kino', 'Pooler, spa, gym, bio')

# ---- images -----------------------------------------------------------------------------------------
# alt text: the same "computer-generated" prefix every sibling uses, per language.

a('images.hero.alt',
  'Vista generada por ordenador del edificio con sus terrazas escalonadas blancas, una base de piedra y el jardín y la piscina delante',
  'Vue de synthèse du bâtiment avec ses terrasses blanches en gradins, un soubassement en pierre, et le jardin et la piscine au premier plan',
  'Computergenerierte Ansicht des Gebäudes mit seinen gestaffelten weißen Terrassen, einem Steinsockel sowie Garten und Pool davor',
  'Компьютерная визуализация здания с белыми террасами-уступами, каменным основанием, садом и бассейном на переднем плане',
  'منظر مُولَّد بالحاسوب للمبنى بتراساته البيضاء المتدرجة وقاعدته الحجرية، وأمامه الحديقة والمسبح',
  'Computergegenereerd beeld van het gebouw met zijn getrapte witte terrassen, een stenen plint en de tuin en het zwembad op de voorgrond',
  'Komputerowa wizualizacja budynku z białymi tarasami schodkowymi, kamienną podstawą oraz ogrodem i basenem na pierwszym planie',
  'Datagenerert bilde av bygningen med de trappetrinnsformede hvite terrassene, en steinsokkel og hagen og bassenget foran',
  'Datorgenererad bild av byggnaden med dess trappstegsformade vita terrasser, en stensockel samt trädgården och poolen framför')
a('images.architecture.alt',
  'Vista generada por ordenador del edificio al anochecer, con las terrazas iluminadas, un largo estanque reflectante y la piscina exterior',
  'Vue de synthèse du bâtiment au crépuscule, avec les terrasses éclairées, un long miroir d’eau et la piscine extérieure',
  'Computergenerierte Ansicht des Gebäudes in der Dämmerung, mit beleuchteten Terrassen, einem langen Spiegelbecken und dem Außenpool',
  'Компьютерная визуализация здания в сумерках: подсвеченные террасы, длинный отражающий бассейн и открытый бассейн',
  'منظر مُولَّد بالحاسوب للمبنى عند الغسق، بتراسات مضاءة وبركة عاكسة طويلة والمسبح الخارجي',
  'Computergegenereerd beeld van het gebouw in de schemering, met verlichte terrassen, een lange spiegelvijver en het buitenzwembad',
  'Komputerowa wizualizacja budynku o zmierzchu, z podświetlonymi tarasami, długim basenem refleksyjnym i basenem zewnętrznym',
  'Datagenerert bilde av bygningen i skumringen, med opplyste terrasser, et langt speilbasseng og utendørsbassenget',
  'Datorgenererad bild av byggnaden i skymningen, med upplysta terrasser, en lång spegeldamm och utomhuspoolen')
a('images.lifestyle.alt',
  'Vista generada por ordenador de la terraza de la piscina con tumbonas y una cama balinesa, el jardín y la costa al fondo',
  'Vue de synthèse de la terrasse de la piscine avec transats et lit de repos, le jardin et la côte au loin',
  'Computergenerierte Ansicht des Pooldecks mit Sonnenliegen und einem Daybed, dem Garten und der Küste dahinter',
  'Компьютерная визуализация террасы у бассейна с шезлонгами и кушеткой, садом и побережьем вдали',
  'منظر مُولَّد بالحاسوب لمنطقة المسبح بكراسي تشمّس وأريكة استلقاء، والحديقة والساحل في الخلفية',
  'Computergegenereerd beeld van het zwembaddek met ligbedden en een daybed, de tuin en de kust daarachter',
  'Komputerowa wizualizacja tarasu przy basenie z leżakami i leżanką, ogrodem i wybrzeżem w tle',
  'Datagenerert bilde av bassengområdet med solsenger og en daybed, hagen og kysten bak',
  'Datorgenererad bild av poolterrassen med solsängar och en daybed, trädgården och kusten bortom')
a('images.privateViewing.alt',
  'Vista generada por ordenador de una terraza cubierta con zona de estar, ventiladores de techo y el mar tras una barandilla de cristal',
  'Vue de synthèse d’une terrasse couverte avec salon, ventilateurs de plafond et la mer derrière un garde-corps en verre',
  'Computergenerierte Ansicht einer überdachten Terrasse mit Loungemöbeln, Deckenventilatoren und dem Meer hinter einer Glasbrüstung',
  'Компьютерная визуализация крытой террасы с зоной отдыха, потолочными вентиляторами и морем за стеклянным ограждением',
  'منظر مُولَّد بالحاسوب لتراس مسقوف بمقاعد جلوس ومراوح سقفية والبحر خلف حاجز زجاجي',
  'Computergegenereerd beeld van een overdekt terras met loungeplekken, plafondventilatoren en de zee achter een glazen balustrade',
  'Komputerowa wizualizacja zadaszonego tarasu ze strefą wypoczynku, wentylatorami sufitowymi i morzem za szklaną balustradą',
  'Datagenerert bilde av en overbygd terrasse med loungemøbler, takvifter og havet bak et glassrekkverk',
  'Datorgenererad bild av en övertäckt terrass med loungemöbler, takfläktar och havet bakom ett glasräcke')
a('media.note',
  'Todas las imágenes son ilustraciones generadas por ordenador, no fotografías del edificio terminado. El mobiliario, la decoración y los elementos que aparecen en ellas, como el jacuzzi de una terraza, son ilustrativos, y los documentos que tenemos no los indican como incluidos. Los planos son los planos comerciales del promotor: no son contractuales, los nombres de las estancias del BY-06 están en español y algunas superficies difieren de la lista de disponibilidad.',
  'Toutes les images sont des illustrations de synthèse, et non des photographies du bâtiment achevé. Le mobilier, la décoration et les équipements qui y figurent, comme le bain à remous d’une terrasse, sont illustratifs, et les documents dont nous disposons ne les indiquent pas comme inclus. Les plans sont les plans commerciaux du promoteur : ils n’ont pas de valeur contractuelle, les noms des pièces du BY-06 sont en espagnol et certaines surfaces diffèrent de la liste de disponibilité.',
  'Alle Bilder sind computergenerierte Illustrationen und keine Fotos des fertigen Gebäudes. Die darin gezeigten Möbel, die Dekoration und die Ausstattung, etwa der Whirlpool auf einer Terrasse, dienen der Veranschaulichung, und die uns vorliegenden Unterlagen führen sie nicht als enthalten auf. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen im BY-06 sind auf Spanisch, und einige Flächen weichen von der Verfügbarkeitsliste ab.',
  'Все изображения — компьютерные иллюстрации, а не фотографии готового здания. Мебель, декор и оснащение на них, например джакузи на террасе, носят иллюстративный характер, и в имеющихся у нас документах они не указаны как входящие в стоимость. Планировки — это коммерческие планы застройщика: они не имеют договорной силы, названия помещений на плане BY-06 даны по-испански, а некоторые площади отличаются от списка наличия.',
  'جميع الصور رسوم توضيحية مُولَّدة بالحاسوب وليست صورًا فوتوغرافية للمبنى بعد اكتماله. والأثاث والديكور والتجهيزات الظاهرة فيها، مثل حوض الجاكوزي على أحد التراسات، توضيحية، ولا تذكرها الوثائق التي بحوزتنا ضمن المشمولات. والمخططات هي مخططات البيع الصادرة عن المطوّر: وهي غير ملزمة تعاقديًا، وأسماء الغرف في مخطط BY-06 بالإسبانية، وتختلف بعض المساحات فيها عن قائمة التوفر.',
  'Alle beelden zijn computergegenereerde illustraties en geen foto’s van het opgeleverde gebouw. Het meubilair, de inrichting en de voorzieningen die erop te zien zijn, zoals het bubbelbad op een terras, zijn illustratief, en de documenten waarover we beschikken vermelden ze niet als inbegrepen. De plattegronden zijn de verkoopplattegronden van de ontwikkelaar: ze zijn niet contractueel, de kamernamen op BY-06 staan in het Spaans en sommige oppervlakten wijken af van de beschikbaarheidslijst.',
  'Wszystkie obrazy to komputerowe ilustracje, a nie zdjęcia ukończonego budynku. Meble, wystrój i wyposażenie widoczne na nich, takie jak jacuzzi na tarasie, mają charakter poglądowy, a dokumenty, którymi dysponujemy, nie wymieniają ich jako wliczonych w cenę. Rzuty to plany sprzedażowe dewelopera: nie są wiążące umownie, nazwy pomieszczeń na rzucie BY-06 są po hiszpańsku, a niektóre powierzchnie różnią się od listy dostępności.',
  'Alle bildene er datagenererte illustrasjoner og ikke fotografier av den ferdige bygningen. Møblene, innredningen og utstyret som vises, for eksempel boblebadet på en terrasse, er illustrative, og dokumentene vi har oppgir dem ikke som inkludert. Plantegningene er utbyggerens salgsplaner: de er ikke kontraktsfestet, romnavnene på BY-06 er på spansk, og noen arealer avviker fra tilgjengelighetslisten.',
  'Alla bilder är datorgenererade illustrationer och inte fotografier av den färdiga byggnaden. Möblerna, inredningen och utrustningen som visas, till exempel bubbelpoolen på en terrass, är illustrativa, och dokumenten vi har anger dem inte som inkluderade. Planritningarna är exploatörens säljplaner: de är inte avtalsbindande, rumsnamnen på BY-06 är på spanska och vissa ytor avviker från tillgänglighetslistan.')

# media items: alt (all but the first, whose alt is already known) and captions
ALT = {
 'media.items.1.alt': (
  'Vista generada por ordenador de la fachada a la calle, con bandas horizontales, lamas de madera y una entrada de doble altura',
  'Vue de synthèse de la façade sur la rue, avec des bandeaux horizontaux, des lames de bois et une entrée à double hauteur',
  'Computergenerierte Ansicht der Fassade zur Straße, mit horizontalen Bändern, Holzlamellen und einem doppelgeschossigen Eingang',
  'Компьютерная визуализация фасада со стороны улицы: горизонтальные пояса, деревянные рейки и вход в два света',
  'منظر مُولَّد بالحاسوب للواجهة المطلة على الشارع، بأشرطة أفقية وشرائح خشبية ومدخل بارتفاع مزدوج',
  'Computergegenereerd beeld van de gevel aan de straat, met horizontale banden, houten latten en een entree van dubbele hoogte',
  'Komputerowa wizualizacja elewacji od strony ulicy, z poziomymi pasami, drewnianymi listwami i wejściem o podwójnej wysokości',
  'Datagenerert bilde av fasaden mot gaten, med horisontale bånd, trelameller og en inngang i to etasjers høyde',
  'Datorgenererad bild av fasaden mot gatan, med horisontella band, träribbor och en entré i dubbel höjd'),
 'media.items.2.alt': (
  'Vista generada por ordenador de la entrada al anochecer, con una puerta acristalada alta, una escultura y láminas de agua iluminadas',
  'Vue de synthèse de l’entrée au crépuscule, avec une haute porte vitrée, une sculpture et des miroirs d’eau éclairés',
  'Computergenerierte Ansicht des Eingangs in der Dämmerung, mit einer hohen Glastür, einer Skulptur und beleuchteten Wasserflächen',
  'Компьютерная визуализация входа в сумерках: высокая остеклённая дверь, скульптура и подсвеченные водные зеркала',
  'منظر مُولَّد بالحاسوب للمدخل عند الغسق، بباب زجاجي عالٍ ومنحوتة وأحواض مياه مضاءة',
  'Computergegenereerd beeld van de entree in de schemering, met een hoge glazen deur, een sculptuur en verlichte waterpartijen',
  'Komputerowa wizualizacja wejścia o zmierzchu, z wysokimi przeszklonymi drzwiami, rzeźbą i podświetlonymi lustrami wody',
  'Datagenerert bilde av inngangen i skumringen, med en høy glassdør, en skulptur og opplyste vannspeil',
  'Datorgenererad bild av entrén i skymningen, med en hög glasdörr, en skulptur och upplysta vattenspeglar'),
 'media.items.4.alt': (
  'Vista generada por ordenador del vestíbulo de entrada de doble altura, con un mostrador de recepción y una cascada de luces en forma de anillo',
  'Vue de synthèse du hall d’entrée à double hauteur, avec un comptoir de réception et une cascade de lumières en forme d’anneaux',
  'Computergenerierte Ansicht der doppelgeschossigen Eingangshalle, mit einem Empfangstresen und einer Kaskade ringförmiger Leuchten',
  'Компьютерная визуализация входного холла в два света со стойкой ресепшена и каскадом светильников в форме колец',
  'منظر مُولَّد بالحاسوب لردهة المدخل بارتفاع مزدوج، بمكتب استقبال وسلسلة من الإضاءات الحلقية',
  'Computergegenereerd beeld van de entreehal van dubbele hoogte, met een receptiebalie en een cascade van ringvormige lampen',
  'Komputerowa wizualizacja holu wejściowego o podwójnej wysokości, z recepcją i kaskadą okrągłych lamp',
  'Datagenerert bilde av inngangspartiet i to etasjers høyde, med en resepsjonsdisk og en kaskade av ringformede lamper',
  'Datorgenererad bild av entréhallen i dubbel höjd, med en receptionsdisk och en kaskad av ringformade lampor'),
 'media.items.6.alt': (
  'Vista generada por ordenador del spa, con tumbonas junto a una piscina interior, paneles de mosaico y plantas de bambú',
  'Vue de synthèse du spa, avec des transats au bord d’une piscine intérieure, des panneaux de mosaïque et des bambous',
  'Computergenerierte Ansicht des Spas, mit Liegen neben einem Innenpool, Mosaikpaneelen und Bambusbepflanzung',
  'Компьютерная визуализация спа: шезлонги у крытого бассейна, мозаичные панно и бамбук',
  'منظر مُولَّد بالحاسوب للسبا، بكراسي استلقاء بجانب مسبح داخلي ولوحات فسيفساء ونباتات الخيزران',
  'Computergegenereerd beeld van de spa, met ligbedden naast een binnenzwembad, mozaïekpanelen en bamboebeplanting',
  'Komputerowa wizualizacja spa, z leżakami przy basenie wewnętrznym, panelami z mozaiki i bambusami',
  'Datagenerert bilde av spaet, med solsenger ved et innendørsbasseng, mosaikkpaneler og bambusplanter',
  'Datorgenererad bild av spaet, med solsängar vid en inomhuspool, mosaikpaneler och bambu'),
 'media.items.7.alt': (
  'Vista generada por ordenador de la piscina interior, con tumbonas, una cama redonda y una sauna al fondo',
  'Vue de synthèse de la piscine intérieure, avec des transats, un lit de repos rond et un sauna au fond',
  'Computergenerierte Ansicht des Innenpools, mit Liegen, einem runden Daybed und einer Sauna im Hintergrund',
  'Компьютерная визуализация крытого бассейна с шезлонгами, круглой кушеткой и сауной вдали',
  'منظر مُولَّد بالحاسوب للمسبح الداخلي، بكراسي استلقاء وأريكة دائرية وساونا في الخلفية',
  'Computergegenereerd beeld van het binnenzwembad, met ligbedden, een ronde daybed en een sauna op de achtergrond',
  'Komputerowa wizualizacja basenu wewnętrznego, z leżakami, okrągłą leżanką i sauną w głębi',
  'Datagenerert bilde av innendørsbassenget, med solsenger, en rund daybed og en badstue bak',
  'Datorgenererad bild av inomhuspoolen, med solsängar, en rund daybed och en bastu bortom'),
 'media.items.8.alt': (
  'Vista generada por ordenador del gimnasio, con máquinas de cardio, pesas libres y una zona de estudio',
  'Vue de synthèse de la salle de sport, avec appareils de cardio, poids libres et un espace studio',
  'Computergenerierte Ansicht des Fitnessraums, mit Cardiogeräten, Hanteln und einem Studiobereich',
  'Компьютерная визуализация тренажёрного зала с кардиотренажёрами, свободными весами и зоной студии',
  'منظر مُولَّد بالحاسوب للصالة الرياضية، بأجهزة كارديو وأوزان حرة ومنطقة استوديو',
  'Computergegenereerd beeld van de fitnessruimte, met cardioapparaten, losse gewichten en een studioruimte',
  'Komputerowa wizualizacja siłowni, ze sprzętem cardio, ciężarkami i strefą studia',
  'Datagenerert bilde av treningsrommet, med kondisjonsapparater, frie vekter og et studioområde',
  'Datorgenererad bild av gymmet, med konditionsmaskiner, fria vikter och en studioyta'),
 'media.items.9.alt': (
  'Vista generada por ordenador de un salón alargado con sofá rinconero, una barra y una mesa de billar',
  'Vue de synthèse d’un long salon avec canapé d’angle, un bar et une table de billard',
  'Computergenerierte Ansicht einer langen Lounge mit Ecksofa, einer Bar und einem Billardtisch',
  'Компьютерная визуализация длинной гостиной с угловым диваном, баром и бильярдным столом',
  'منظر مُولَّد بالحاسوب لصالة طويلة بأريكة زاوية وبار وطاولة بلياردو',
  'Computergegenereerd beeld van een lange lounge met een hoekbank, een bar en een biljarttafel',
  'Komputerowa wizualizacja długiego salonu z narożną sofą, barem i stołem bilardowym',
  'Datagenerert bilde av en lang lounge med hjørnesofa, en bar og et biljardbord',
  'Datorgenererad bild av en lång lounge med hörnsoffa, en bar och ett biljardbord'),
 'media.items.10.alt': (
  'Vista generada por ordenador de la sala de cine, con sillones, una pantalla grande y un techo estrellado',
  'Vue de synthèse de la salle de cinéma, avec fauteuils, un grand écran et un plafond étoilé',
  'Computergenerierte Ansicht des Kinoraums, mit Sesseln, einer großen Leinwand und einer Sternendecke',
  'Компьютерная визуализация кинозала с креслами, большим экраном и потолком со звёздами',
  'منظر مُولَّد بالحاسوب لغرفة السينما، بمقاعد وشاشة كبيرة وسقف مرصّع بالنجوم',
  'Computergegenereerd beeld van de bioscoopzaal, met fauteuils, een groot scherm en een sterrenplafond',
  'Komputerowa wizualizacja sali kinowej, z fotelami, dużym ekranem i gwiaździstym sufitem',
  'Datagenerert bilde av kinosalen, med lenestoler, en stor skjerm og et stjerneklart tak',
  'Datorgenererad bild av biosalongen, med fåtöljer, en stor skärm och ett stjärnklart tak'),
 'media.items.11.alt': (
  'Vista generada por ordenador de la sala del simulador de golf, con dos sillones y una pantalla grande',
  'Vue de synthèse de la salle du simulateur de golf, avec deux fauteuils et un grand écran',
  'Computergenerierte Ansicht des Golfsimulator-Raums, mit zwei Sesseln und einer großen Leinwand',
  'Компьютерная визуализация комнаты гольф-симулятора с двумя креслами и большим экраном',
  'منظر مُولَّد بالحاسوب لغرفة محاكي الغولف، بمقعدين وشاشة كبيرة',
  'Computergegenereerd beeld van de golfsimulatorruimte, met twee fauteuils en een groot scherm',
  'Komputerowa wizualizacja pomieszczenia z symulatorem golfa, z dwoma fotelami i dużym ekranem',
  'Datagenerert bilde av rommet med golfsimulator, med to lenestoler og en stor skjerm',
  'Datorgenererad bild av rummet med golfsimulatorn, med två fåtöljer och en stor skärm'),
 'media.items.12.alt': (
  'Vista generada por ordenador de un salón de planta abierta con sofás, una vinoteca y la cocina al fondo',
  'Vue de synthèse d’un séjour ouvert avec des canapés, une cave à vin vitrée et la cuisine au fond',
  'Computergenerierte Ansicht eines offenen Wohnbereichs mit Sofas, einer Weinwand und der Küche im Hintergrund',
  'Компьютерная визуализация гостиной открытой планировки с диванами, винотекой и кухней вдали',
  'منظر مُولَّد بالحاسوب لغرفة معيشة مفتوحة بأرائك وجدار للنبيذ، والمطبخ في الخلفية',
  'Computergegenereerd beeld van een open woonkamer met banken, een wijnwand en de keuken op de achtergrond',
  'Komputerowa wizualizacja otwartego salonu z sofami, ścianą na wino i kuchnią w głębi',
  'Datagenerert bilde av en åpen stue med sofaer, en vinvegg og kjøkkenet bak',
  'Datorgenererad bild av ett öppet vardagsrum med soffor, en vinvägg och köket bortom'),
 'media.items.13.alt': (
  'Vista generada por ordenador de una cocina con una gran isla, taburetes de barra y electrodomésticos integrados',
  'Vue de synthèse d’une cuisine avec un grand îlot, des tabourets de bar et des appareils encastrés',
  'Computergenerierte Ansicht einer Küche mit großer Kochinsel, Barhockern und Einbaugeräten',
  'Компьютерная визуализация кухни с большим островом, барными стульями и встроенной техникой',
  'منظر مُولَّد بالحاسوب لمطبخ بجزيرة كبيرة وكراسي بار وأجهزة مدمجة',
  'Computergegenereerd beeld van een keuken met een groot eiland, barkrukken en inbouwapparatuur',
  'Komputerowa wizualizacja kuchni z dużą wyspą, hokerami i sprzętem do zabudowy',
  'Datagenerert bilde av et kjøkken med en stor øy, barkrakker og integrerte hvitevarer',
  'Datorgenererad bild av ett kök med en stor köksö, barstolar och inbyggda vitvaror'),
 'media.items.14.alt': (
  'Vista generada por ordenador de un rincón de estudio con un escritorio y una obra de arte, y el salón al fondo',
  'Vue de synthèse d’un coin bureau avec un bureau et une œuvre d’art, et le séjour au fond',
  'Computergenerierte Ansicht einer Arbeitsecke mit Schreibtisch und einem Kunstwerk, dahinter der Wohnbereich',
  'Компьютерная визуализация рабочего уголка со столом и произведением искусства, вдали гостиная',
  'منظر مُولَّد بالحاسوب لركن دراسة بمكتب وعمل فني، وغرفة المعيشة في الخلفية',
  'Computergegenereerd beeld van een studiehoek met een bureau en een kunstwerk, met de woonkamer erachter',
  'Komputerowa wizualizacja kącika do pracy z biurkiem i dziełem sztuki, a w głębi salon',
  'Datagenerert bilde av en arbeidskrok med et skrivebord og et kunstverk, og stuen bak',
  'Datorgenererad bild av ett arbetshörn med ett skrivbord och ett konstverk, och vardagsrummet bortom'),
 'media.items.16.alt': (
  'Vista generada por ordenador de una terraza con una larga mesa de comedor y vistas a lo largo de la costa',
  'Vue de synthèse d’une terrasse avec une longue table à manger et une vue le long de la côte',
  'Computergenerierte Ansicht einer Terrasse mit langem Esstisch und Blick die Küste entlang',
  'Компьютерная визуализация террасы с длинным обеденным столом и видом вдоль побережья',
  'منظر مُولَّد بالحاسوب لتراس بطاولة طعام طويلة وإطلالة على امتداد الساحل',
  'Computergegenereerd beeld van een terras met een lange eettafel en uitzicht langs de kust',
  'Komputerowa wizualizacja tarasu z długim stołem jadalnianym i widokiem wzdłuż wybrzeża',
  'Datagenerert bilde av en terrasse med et langt spisebord og utsikt langs kysten',
  'Datorgenererad bild av en terrass med ett långt matbord och utsikt längs kusten'),
 'media.items.17.alt': (
  'Vista generada por ordenador de una terraza con un jacuzzi elevado, plantas y vistas al mar',
  'Vue de synthèse d’une terrasse avec un bain à remous surélevé, des plantations et une vue sur la mer',
  'Computergenerierte Ansicht einer Terrasse mit erhöhtem Whirlpool, Bepflanzung und Blick aufs Meer',
  'Компьютерная визуализация террасы с приподнятой джакузи, зеленью и видом на море',
  'منظر مُولَّد بالحاسوب لتراس بحوض جاكوزي مرتفع ونباتات وإطلالة على البحر',
  'Computergegenereerd beeld van een terras met een verhoogd bubbelbad, beplanting en uitzicht op zee',
  'Komputerowa wizualizacja tarasu z podwyższonym jacuzzi, zielenią i widokiem na morze',
  'Datagenerert bilde av en terrasse med et hevet boblebad, beplantning og utsikt mot havet',
  'Datorgenererad bild av en terrass med en upphöjd bubbelpool, växter och utsikt över havet'),
 'media.items.18.alt': (
  'Vista panorámica generada por ordenador de un comedor en la terraza que se abre al salón y a la cocina',
  'Vue panoramique de synthèse d’un coin repas sur la terrasse ouvrant sur le séjour et la cuisine',
  'Computergenerierte Breitansicht eines Essbereichs auf der Terrasse, der sich zu Wohnbereich und Küche öffnet',
  'Компьютерная панорамная визуализация обеденной зоны на террасе с выходом в гостиную и на кухню',
  'منظر بانورامي مُولَّد بالحاسوب لمنطقة طعام على التراس تفتح على غرفة المعيشة والمطبخ',
  'Computergegenereerd breed beeld van een eethoek op het terras die uitkomt op de woonkamer en de keuken',
  'Szeroka wizualizacja komputerowa jadalni na tarasie otwierającej się na salon i kuchnię',
  'Datagenerert bredt bilde av en spiseplass på terrassen som åpner seg mot stuen og kjøkkenet',
  'Datorgenererad bred bild av en matplats på terrassen som öppnar sig mot vardagsrummet och köket'),
 'media.items.19.alt': (
  'Vista generada por ordenador de un dormitorio principal con una cama baja, lámparas colgantes y una pared de cristal corredera hacia la terraza',
  'Vue de synthèse d’une chambre principale avec un lit bas, des suspensions et une baie vitrée coulissante vers la terrasse',
  'Computergeneriertes Hauptschlafzimmer mit niedrigem Bett, Pendelleuchten und einer verglasten Schiebewand zur Terrasse',
  'Компьютерная визуализация главной спальни с низкой кроватью, подвесными светильниками и раздвижной стеклянной стеной на террасу',
  'غرفة نوم رئيسية مُولَّدة بالحاسوب بسرير منخفض ومصابيح معلّقة وجدار زجاجي منزلق نحو التراس',
  'Computergegenereerde hoofdslaapkamer met een laag bed, hanglampen en een glazen schuifwand naar het terras',
  'Komputerowa wizualizacja sypialni głównej z niskim łóżkiem, lampami wiszącymi i przesuwną szklaną ścianą na taras',
  'Datagenerert hovedsoverom med en lav seng, taklamper og en glassvegg som kan skyves til siden mot terrassen',
  'Datorgenererat huvudsovrum med en låg säng, pendellampor och en glasvägg som kan skjutas åt sidan mot terrassen'),
 'media.items.20.alt': (
  'Vista generada por ordenador de un dormitorio con un escritorio, un sillón y vistas al mar a través de una ventana en esquina',
  'Vue de synthèse d’une chambre avec un bureau, un fauteuil et une vue sur la mer par une fenêtre d’angle',
  'Computergeneriertes Schlafzimmer mit Schreibtisch, einem Sessel und Meerblick durch ein Eckfenster',
  'Компьютерная визуализация спальни с письменным столом, креслом и видом на море через угловое окно',
  'غرفة نوم مُولَّدة بالحاسوب بمكتب ومقعد وإطلالة على البحر عبر نافذة زاوية',
  'Computergegenereerde slaapkamer met een bureau, een fauteuil en zeezicht door een hoekraam',
  'Komputerowa wizualizacja sypialni z biurkiem, fotelem i widokiem na morze przez okno narożne',
  'Datagenerert soverom med et skrivebord, en lenestol og utsikt mot havet gjennom et hjørnevindu',
  'Datorgenererat sovrum med ett skrivbord, en fåtölj och havsutsikt genom ett hörnfönster'),
 'media.items.21.alt': (
  'Baño generado por ordenador con una bañera exenta, una ventana redonda y un lavabo doble de piedra',
  'Vue de synthèse d’une salle de bains avec une baignoire îlot, une fenêtre ronde et une double vasque en pierre',
  'Computergeneriertes Bad mit freistehender Badewanne, einem runden Fenster und einem doppelten Steinwaschtisch',
  'Компьютерная визуализация ванной комнаты с отдельно стоящей ванной, круглым окном и двойной каменной раковиной',
  'حمام مُولَّد بالحاسوب بحوض استحمام قائم بذاته ونافذة دائرية ومغسلة حجرية مزدوجة',
  'Computergegenereerde badkamer met een vrijstaand bad, een rond raam en een dubbele stenen wastafel',
  'Komputerowa wizualizacja łazienki z wolnostojącą wanną, okrągłym oknem i podwójną kamienną umywalką',
  'Datagenerert bad med et frittstående badekar, et rundt vindu og en dobbel steinservant',
  'Datorgenererat badrum med ett fristående badkar, ett runt fönster och en dubbel stentvättställ'),
 'media.items.22.alt': (
  'Baño generado por ordenador con una ducha acristalada, una bañera exenta y un lavabo doble',
  'Vue de synthèse d’une salle de bains avec une douche vitrée, une baignoire îlot et une double vasque',
  'Computergeneriertes Bad mit verglaster Dusche, freistehender Badewanne und Doppelwaschtisch',
  'Компьютерная визуализация ванной комнаты с застеклённым душем, отдельно стоящей ванной и двойной раковиной',
  'حمام مُولَّد بالحاسوب بدش زجاجي وحوض استحمام قائم بذاته ومغسلة مزدوجة',
  'Computergegenereerde badkamer met een glazen douche, een vrijstaand bad en een dubbele wastafel',
  'Komputerowa wizualizacja łazienki z przeszkloną kabiną prysznicową, wolnostojącą wanną i podwójną umywalką',
  'Datagenerert bad med en glassdusj, et frittstående badekar og en dobbel servant',
  'Datorgenererat badrum med en glasdusch, ett fristående badkar och ett dubbelt tvättställ'),
}
for path, tr in ALT.items():
    a(path, *tr)
# the ALT strings read straight from project.json, so the captions below must too
CAP = {
 'media.items.1.caption': ('La fachada a la calle', 'La façade sur la rue', 'Die Fassade zur Straße', 'Фасад со стороны улицы', 'الواجهة المطلة على الشارع', 'De gevel aan de straat', 'Elewacja od strony ulicy', 'Fasaden mot gaten', 'Fasaden mot gatan'),
 'media.items.2.caption': ('La entrada al anochecer', 'L’entrée au crépuscule', 'Der Eingang in der Dämmerung', 'Вход в сумерках', 'المدخل عند الغسق', 'De entree in de schemering', 'Wejście o zmierzchu', 'Inngangen i skumringen', 'Entrén i skymningen'),
 'media.items.5.caption': ('La terraza de la piscina', 'La terrasse de la piscine', 'Das Pooldeck', 'Терраса у бассейна', 'منطقة المسبح', 'Het zwembaddek', 'Taras przy basenie', 'Bassengområdet', 'Poolterrassen'),
 'media.items.6.caption': ('Tumbonas junto a la piscina interior', 'Des transats au bord de la piscine intérieure', 'Liegen neben dem Innenpool', 'Шезлонги у крытого бассейна', 'كراسي استلقاء بجانب المسبح الداخلي', 'Ligbedden naast het binnenzwembad', 'Leżaki przy basenie wewnętrznym', 'Solsenger ved innendørsbassenget', 'Solsängar vid inomhuspoolen'),
 'media.items.7.caption': ('La piscina interior y la sauna', 'La piscine intérieure et le sauna', 'Der Innenpool und die Sauna', 'Крытый бассейн и сауна', 'المسبح الداخلي والساونا', 'Het binnenzwembad en de sauna', 'Basen wewnętrzny i sauna', 'Innendørsbassenget og badstuen', 'Inomhuspoolen och bastun'),
 'media.items.11.caption': ('El simulador de golf', 'Le simulateur de golf', 'Der Golfsimulator', 'Гольф-симулятор', 'محاكي الغولف', 'De golfsimulator', 'Symulator golfa', 'Golfsimulatoren', 'Golfsimulatorn'),
 'media.items.14.caption': ('Rincón de estudio', 'Coin bureau', 'Arbeitsecke', 'Рабочий уголок', 'ركن الدراسة', 'Studiehoek', 'Kącik do pracy', 'Arbeidskrok', 'Arbetshörn'),
 'media.items.15.caption': ('Una terraza cubierta frente al mar', 'Une terrasse couverte face à la mer', 'Eine überdachte Terrasse mit Blick aufs Meer', 'Крытая терраса с видом на море', 'تراس مسقوف مطل على البحر', 'Een overdekt terras met uitzicht op zee', 'Zadaszony taras z widokiem na morze', 'En overbygd terrasse mot havet', 'En övertäckt terrass mot havet'),
 'media.items.17.caption': ('Una terraza con jacuzzi', 'Une terrasse avec bain à remous', 'Eine Terrasse mit Whirlpool', 'Терраса с джакузи', 'تراس بحوض جاكوزي', 'Een terras met bubbelbad', 'Taras z jacuzzi', 'En terrasse med boblebad', 'En terrass med bubbelpool'),
 'media.items.18.caption': ('Comedor en la terraza', 'Coin repas sur la terrasse', 'Essbereich auf der Terrasse', 'Обеденная зона на террасе', 'منطقة الطعام على التراس', 'Eethoek op het terras', 'Jadalnia na tarasie', 'Spiseplass på terrassen', 'Matplats på terrassen'),
 'media.items.22.caption': ('Baño con ducha acristalada', 'Salle de bains avec douche vitrée', 'Bad mit verglaster Dusche', 'Ванная комната с застеклённым душем', 'حمام بدش زجاجي', 'Badkamer met glazen douche', 'Łazienka z przeszkloną kabiną prysznicową', 'Bad med glassdusj', 'Badrum med glasdusch'),
}
for path, tr in CAP.items():
    a(path, *tr)

# ---- overview, why, architecture --------------------------------------------------------------------

a('overview.headlineHtml', 'Diez viviendas, <em>cinco disponibles</em>', 'Dix logements, <em>cinq disponibles</em>', 'Zehn Wohnungen, <em>fünf verfügbar</em>',
  'Десять квартир, <em>пять доступны</em>', 'عشرة مساكن، <em>خمسة متاحة</em>', 'Tien woningen, <em>vijf beschikbaar</em>', 'Dziesięć lokali, <em>pięć dostępnych</em>',
  'Ti boliger, <em>fem ledige</em>', 'Tio bostäder, <em>fem lediga</em>')
a('overview.copy.0',
  'Biubay es una promoción frente al mar de diez apartamentos de tres o cuatro dormitorios en Estepona, cerca del puerto deportivo según la hoja informativa del promotor. Las cinco viviendas con precio tienen todas cuatro dormitorios, cuatro baños y un aseo, ascensor privado y una terraza de {N108.52} a {N191.37} {U} en los planos con una pequeña piscina dibujada, y cuestan de {E6500000} a {E9000000} más IVA.',
  'Biubay est une résidence en bord de mer de dix appartements de trois ou quatre chambres à Estepona, près du port de plaisance selon la fiche d’information du promoteur. Les cinq logements affichés avec un prix ont tous quatre chambres, quatre salles de bain et des toilettes, un ascenseur privé et une terrasse de {N108.52} à {N191.37} {U} sur les plans, avec une petite piscine dessinée, et coûtent de {E6500000} à {E9000000} hors TVA.',
  'Biubay ist eine Anlage direkt am Meer mit zehn Wohnungen mit drei oder vier Schlafzimmern in Estepona, laut Infoblatt des Bauträgers in der Nähe des Yachthafens. Die fünf Wohnungen mit Preis haben alle vier Schlafzimmer, vier Bäder und eine Toilette, einen privaten Aufzug und eine Terrasse von {N108.52} bis {N191.37} {U} laut Plänen, auf der ein kleiner Pool eingezeichnet ist, und kosten von {E6500000} bis {E9000000} zuzüglich MwSt.',
  'Biubay — жилой комплекс на берегу моря из десяти апартаментов с тремя или четырьмя спальнями в Эстепоне, по информационному листу застройщика, вблизи порта-марины. Все пять квартир с указанной ценой имеют четыре спальни, четыре ванные комнаты и туалет, частный лифт и террасу от {N108.52} до {N191.37} {U} по планам с нарисованным небольшим бассейном; стоят они от {E6500000} до {E9000000} без НДС.',
  'Biubay مشروع على الواجهة البحرية من عشر شقق بثلاث أو أربع غرف نوم في إستيبونا، وبحسب النشرة التعريفية للمطوّر فهو قريب من المرسى. وللمساكن الخمسة المدرجة بسعر أربع غرف نوم وأربعة حمامات ودورة مياه ومصعد خاص وتراس تتراوح مساحته بين {N108.52} و{N191.37} {U} على المخططات، ويظهر عليه مسبح صغير مرسوم، وتتراوح أسعارها بين {E6500000} و{E9000000} دون ضريبة القيمة المضافة.',
  'Biubay is een project aan zee met tien appartementen met drie of vier slaapkamers in Estepona, volgens het infoblad van de ontwikkelaar vlak bij de jachthaven. De vijf woningen met een prijs hebben allemaal vier slaapkamers, vier badkamers en een toilet, een eigen lift en een terras van {N108.52} tot {N191.37} {U} volgens de plattegronden, met een klein zwembad erop getekend, en kosten van {E6500000} tot {E9000000} excl. btw.',
  'Biubay to osiedle przy morzu z dziesięcioma apartamentami z trzema lub czterema sypialniami w Esteponie, według karty informacyjnej dewelopera w pobliżu mariny. Pięć lokali z podaną ceną ma po cztery sypialnie, cztery łazienki i toaletę, prywatną windę oraz taras o powierzchni od {N108.52} do {N191.37} {U} według rzutów, z narysowanym małym basenem, a ich ceny wynoszą od {E6500000} do {E9000000} plus VAT.',
  'Biubay er et prosjekt ved sjøen med ti leiligheter med tre eller fire soverom i Estepona, ifølge utbyggerens infoark nær marinaen. De fem boligene med pris har alle fire soverom, fire bad og et toalett, egen heis og en terrasse på {N108.52} til {N191.37} {U} etter planene, med et lite basseng tegnet inn, og koster fra {E6500000} til {E9000000} pluss mva.',
  'Biubay är ett projekt vid havet med tio lägenheter med tre eller fyra sovrum i Estepona, enligt exploatörens infoblad nära marinan. De fem bostäderna med pris har alla fyra sovrum, fyra badrum och en toalett, egen hiss och en terrass på {N108.52} till {N191.37} {U} enligt planritningarna, med en liten pool inritad, och kostar från {E6500000} till {E9000000} plus IVA.')
a('overview.copy.1',
  'Los residentes comparten una piscina exterior orientada al mar, un spa con piscina interior en las recreaciones, un gimnasio, una sala de cine, un simulador de golf, una sala de juegos y una sala polivalente, en la planta de servicios de los planos. La hoja informativa indica que la licencia de obras está concedida y que las obras empezaron en marzo de 2026, con entrega en {Q4} 2028.',
  'Les résidents partagent une piscine extérieure tournée vers la mer, un spa avec piscine intérieure sur les visuels de synthèse, une salle de sport, une salle de cinéma, un simulateur de golf, une salle de jeux et une salle polyvalente, au niveau des équipements des plans. La fiche d’information indique que le permis de construire est accordé et que les travaux ont commencé en mars 2026, avec une livraison au {Q4} 2028.',
  'Die Bewohner teilen sich einen Außenpool mit Blick aufs Meer, ein Spa mit Innenpool in den Renderings, einen Fitnessraum, einen Kinoraum, einen Golfsimulator, ein Spielzimmer und einen Mehrzweckraum, auf der Ausstattungsebene der Pläne. Laut Infoblatt ist die Baugenehmigung erteilt und haben die Bauarbeiten im März 2026 begonnen, die Übergabe ist für {Q4} 2028 angegeben.',
  'Жители пользуются общим открытым бассейном, обращённым к морю, спа с крытым бассейном на визуализациях, тренажёрным залом, кинозалом, гольф-симулятором, игровой комнатой и многофункциональным помещением на уровне удобств, показанном на планах. В информационном листе сказано, что разрешение на строительство выдано, а работы начались в марте 2026 года; сдача указана на {Q4} 2028 года.',
  'يتشارك السكان مسبحًا خارجيًا مطلًّا على البحر، وسبا بمسبح داخلي في الصور المُولَّدة، وصالة رياضية، وغرفة سينما، ومحاكي غولف، وغرفة ألعاب، وغرفة متعددة الاستعمالات، في طابق المرافق الظاهر في المخططات. وتذكر النشرة التعريفية أن رخصة البناء ممنوحة وأن الأعمال بدأت في مارس 2026، مع التسليم في {Q4} 2028.',
  'De bewoners delen een buitenzwembad dat op zee uitkijkt, een spa met binnenzwembad op de renderings, een fitnessruimte, een bioscoopzaal, een golfsimulator, een spelkamer en een multifunctionele ruimte, op de voorzieningenlaag van de plattegronden. Volgens het infoblad is de bouwvergunning verleend en zijn de werken in maart 2026 gestart, met oplevering in {Q4} 2028.',
  'Mieszkańcy korzystają ze wspólnego basenu zewnętrznego zwróconego ku morzu, spa z basenem wewnętrznym na wizualizacjach, siłowni, sali kinowej, symulatora golfa, sali gier i sali wielofunkcyjnej, na poziomie udogodnień widocznym na rzutach. Karta informacyjna podaje, że pozwolenie na budowę zostało udzielone, a prace rozpoczęły się w marcu 2026 r., z odbiorem w {Q4} 2028.',
  'Beboerne deler et utendørsbasseng som vender mot havet, et spa med innendørsbasseng på visualiseringene, et treningsrom, en kinosal, en golfsimulator, et spillrom og et flerbruksrom, på fasilitetsnivået i planene. Ifølge infoarket er byggetillatelsen innvilget og arbeidene startet i mars 2026, med overlevering i {Q4} 2028.',
  'De boende delar en utomhuspool som vetter mot havet, ett spa med inomhuspool på visualiseringarna, ett gym, en biosalong, en golfsimulator, ett spelrum och ett flexibelt rum, på bekvämlighetsplanet i planritningarna. Enligt infobladet är bygglovet beviljat och arbetena påbörjades i mars 2026, med tillträde i {Q4} 2028.')
a('why.copy',
  'Apartamentos de cuatro dormitorios frente al mar con ascensor privado, grandes terrazas y una planta con piscina, spa y gimnasio, en un edificio de diez viviendas.',
  'Des appartements de quatre chambres en bord de mer avec ascenseur privé, grandes terrasses et un niveau avec piscine, spa et salle de sport, dans un bâtiment de dix logements.',
  'Wohnungen mit vier Schlafzimmern direkt am Meer, mit privatem Aufzug, großen Terrassen und einer Ebene mit Pool, Spa und Fitnessraum, in einem Gebäude mit zehn Wohnungen.',
  'Квартиры с четырьмя спальнями на берегу моря, с частным лифтом, большими террасами и уровнем с бассейном, спа и тренажёрным залом, в доме на десять квартир.',
  'شقق بأربع غرف نوم على الواجهة البحرية، بمصعد خاص وتراسات واسعة وطابق للمسبح والسبا والصالة الرياضية، في مبنى من عشرة مساكن.',
  'Appartementen met vier slaapkamers aan zee, met eigen lift, grote terrassen en een laag met zwembad, spa en fitnessruimte, in een gebouw met tien woningen.',
  'Apartamenty z czterema sypialniami przy morzu, z prywatną windą, dużymi tarasami i poziomem z basenem, spa i siłownią, w budynku z dziesięcioma lokalami.',
  'Leiligheter med fire soverom ved sjøen, med egen heis, store terrasser og et nivå med basseng, spa og treningsrom, i en bygning med ti boliger.',
  'Lägenheter med fyra sovrum vid havet, med egen hiss, stora terrasser och ett plan med pool, spa och gym, i en byggnad med tio bostäder.')
a('why.points.0.1',
  'Compradores que quieren una vivienda nueva y amplia frente al mar en Estepona, para vivir en ella o como segunda residencia, con piscinas, spa y gimnasio en el propio edificio.',
  'Les acheteurs qui souhaitent un grand logement neuf en bord de mer à Estepona, pour y vivre ou comme résidence secondaire, avec piscines, spa et salle de sport dans le bâtiment même.',
  'Käufer, die eine große neue Wohnung direkt am Meer in Estepona suchen, zum Selbstbewohnen oder als Zweitwohnsitz, mit Pools, Spa und Fitnessraum im Gebäude selbst.',
  'Покупатели, которым нужна просторная новая квартира на берегу моря в Эстепоне — для жизни или как второе жильё, — с бассейнами, спа и тренажёрным залом в самом здании.',
  'مشترون يبحثون عن مسكن جديد واسع على الواجهة البحرية في إستيبونا، للسكن أو كمنزل ثانٍ، مع مسابح وسبا وصالة رياضية في المبنى نفسه.',
  'Kopers die een ruime nieuwe woning aan zee in Estepona zoeken, om in te wonen of als tweede woning, met zwembaden, spa en fitnessruimte in het gebouw zelf.',
  'Kupujący, którzy szukają dużego nowego lokalu przy morzu w Esteponie, do zamieszkania lub jako drugi dom, z basenami, spa i siłownią w samym budynku.',
  'Kjøpere som vil ha en stor ny bolig ved sjøen i Estepona, til eget bruk eller som feriebolig, med basseng, spa og treningsrom i selve bygningen.',
  'Köpare som vill ha en stor ny bostad vid havet i Estepona, för eget boende eller som andrahem, med pooler, spa och gym i själva byggnaden.')
a('why.points.1.1',
  'Solo diez viviendas en el edificio, superficies construidas de {N285.64} a {N299.19} {U} según la lista, un ascensor privado en cada una de las cinco viviendas listadas y terrazas de {N108.52} a {N191.37} {U} según los planos.',
  'Seulement dix logements dans le bâtiment, des surfaces construites de {N285.64} à {N299.19} {U} selon la liste, un ascenseur privé dans chacun des cinq logements listés et des terrasses de {N108.52} à {N191.37} {U} selon les plans.',
  'Nur zehn Wohnungen im Gebäude, bebaute Flächen von {N285.64} bis {N299.19} {U} laut Liste, ein privater Aufzug in jeder der fünf aufgeführten Wohnungen und Terrassen von {N108.52} bis {N191.37} {U} laut Plänen.',
  'Всего десять квартир в доме, площадь застройки от {N285.64} до {N299.19} {U} по списку, частный лифт в каждой из пяти указанных квартир и террасы от {N108.52} до {N191.37} {U} по планам.',
  'عشرة مساكن فقط في المبنى، ومساحات مبنية من {N285.64} إلى {N299.19} {U} بحسب القائمة، ومصعد خاص في كل من المساكن الخمسة المدرجة، وتراسات من {N108.52} إلى {N191.37} {U} بحسب المخططات.',
  'Slechts tien woningen in het gebouw, bebouwde oppervlakten van {N285.64} tot {N299.19} {U} volgens de lijst, een eigen lift in elk van de vijf vermelde woningen en terrassen van {N108.52} tot {N191.37} {U} volgens de plattegronden.',
  'Tylko dziesięć lokali w budynku, powierzchnie zabudowy od {N285.64} do {N299.19} {U} według listy, prywatna winda w każdym z pięciu wymienionych lokali i tarasy od {N108.52} do {N191.37} {U} według rzutów.',
  'Bare ti boliger i bygningen, bebygd areal fra {N285.64} til {N299.19} {U} ifølge listen, egen heis i hver av de fem oppførte boligene og terrasser fra {N108.52} til {N191.37} {U} etter planene.',
  'Bara tio bostäder i byggnaden, byggyta på {N285.64} till {N299.19} {U} enligt listan, egen hiss i var och en av de fem listade bostäderna och terrasser på {N108.52} till {N191.37} {U} enligt planritningarna.')
a('why.points.2.1',
  'El promotor sitúa el edificio directamente frente al mar en Estepona, cerca del puerto deportivo. Su folleto da Puerto Banús a 20 minutos y Málaga a 50, sin decir cómo se recorren.',
  'Le promoteur situe le bâtiment directement en bord de mer à Estepona, près du port de plaisance. Sa brochure donne Puerto Banús à 20 minutes et Málaga à 50, sans dire comment on les parcourt.',
  'Der Bauträger legt das Gebäude direkt ans Meer in Estepona, in die Nähe des Yachthafens. Seine Broschüre nennt Puerto Banús 20 Minuten und Málaga 50 Minuten entfernt, ohne zu sagen, womit man sie zurücklegt.',
  'Застройщик помещает здание прямо на берегу моря в Эстепоне, вблизи порта-марины. В его брошюре до Пуэрто-Баная указано 20 минут, до Малаги — 50, но не сказано, как их преодолевают.',
  'يضع المطوّر المبنى مباشرةً على الواجهة البحرية في إستيبونا، قرب المرسى. ويذكر كتيّبه أن بويرتو بانوس تبعد 20 دقيقة ومالقة 50 دقيقة، دون أن يوضح وسيلة التنقل.',
  'De ontwikkelaar plaatst het gebouw direct aan zee in Estepona, vlak bij de jachthaven. In de brochure ligt Puerto Banús op 20 minuten en Málaga op 50, zonder te zeggen hoe die worden afgelegd.',
  'Deweloper umiejscawia budynek bezpośrednio nad morzem w Esteponie, w pobliżu mariny. W jego broszurze Puerto Banús jest oddalone o 20 minut, a Málaga o 50, bez informacji, jak się je pokonuje.',
  'Utbyggeren plasserer bygningen rett ved sjøen i Estepona, nær marinaen. Brosjyren oppgir Puerto Banús 20 minutter unna og Málaga 50, uten å si hvordan de tilbakelegges.',
  'Exploatören placerar byggnaden direkt vid havet i Estepona, nära marinan. Dess broschyr anger Puerto Banús på 20 minuters avstånd och Málaga på 50, utan att säga hur de färdas.')
a('why.points.3.1',
  'La hoja informativa indica que la licencia está concedida y que las obras empezaron en marzo de 2026, con entrega en {Q4} 2028. No lleva fecha, así que pedimos la fecha contractual y el estado de las obras antes de cualquier reserva.',
  'La fiche d’information indique que le permis est accordé et que les travaux ont commencé en mars 2026, avec une livraison au {Q4} 2028. Elle n’est pas datée, nous demandons donc la date contractuelle et l’état d’avancement des travaux avant toute réservation.',
  'Laut Infoblatt ist die Genehmigung erteilt und haben die Bauarbeiten im März 2026 begonnen, die Übergabe ist für {Q4} 2028 angegeben. Es trägt kein Datum, daher fragen wir vor jeder Reservierung das vertragliche Datum und den Baustand an.',
  'В информационном листе сказано, что разрешение выдано и работы начались в марте 2026 года, сдача — {Q4} 2028 года. Лист не датирован, поэтому перед любым бронированием мы запрашиваем договорную дату и стадию работ.',
  'تذكر النشرة التعريفية أن الرخصة ممنوحة وأن الأعمال بدأت في مارس 2026، مع التسليم في {Q4} 2028. وهي غير مؤرخة، لذلك نطلب الموعد التعاقدي ومرحلة الأعمال قبل أي حجز.',
  'Volgens het infoblad is de vergunning verleend en zijn de werken in maart 2026 gestart, met oplevering in {Q4} 2028. Het is niet gedateerd, dus we vragen vóór elke reservering de contractuele datum en de stand van de werken op.',
  'Karta informacyjna podaje, że pozwolenie zostało udzielone, a prace rozpoczęły się w marcu 2026 r., z odbiorem w {Q4} 2028. Nie ma daty, dlatego przed każdą rezerwacją prosimy o termin umowny i stan prac.',
  'Infoarket oppgir at tillatelsen er innvilget og at arbeidene startet i mars 2026, med overlevering i {Q4} 2028. Det er udatert, så vi ber om den kontraktfestede datoen og byggestatusen før enhver reservasjon.',
  'Infobladet anger att bygglovet är beviljat och att arbetena påbörjades i mars 2026, med tillträde i {Q4} 2028. Det är odaterat, så vi begär det avtalade datumet och byggstatusen före varje reservation.')
a('architecture.headlineHtml', 'Terrazas escalonadas, <em>frente al mar</em>', 'Des terrasses en gradins, <em>face à la mer</em>', 'Gestaffelte Terrassen, <em>zum Meer hin</em>',
  'Террасы-уступы <em>с видом на море</em>', 'تراسات متدرجة <em>تواجه البحر</em>', 'Getrapte terrassen, <em>gericht op zee</em>', 'Tarasy schodkowe, <em>zwrócone ku morzu</em>',
  'Trappetrinnsterrasser <em>mot havet</em>', 'Trappstegsformade terrasser <em>mot havet</em>')
a('architecture.copy.0',
  'En las imágenes generadas por ordenador del promotor, el edificio se eleva en bandas blancas escalonadas, con amplias terrazas tras barandillas de cristal, una base de piedra y jardines con largos estanques reflectantes que se dirigen hacia el mar.',
  'Sur les images de synthèse du promoteur, le bâtiment s’élève en bandeaux blancs en gradins, avec de larges terrasses derrière des garde-corps en verre, un soubassement en pierre et des jardins aux longs miroirs d’eau qui s’étendent vers la mer.',
  'In den computergenerierten Bildern des Bauträgers steigt das Gebäude in gestaffelten weißen Bändern auf, mit tiefen Terrassen hinter Glasbrüstungen, einem Steinsockel und Gärten mit langen Spiegelbecken, die zum Meer hinführen.',
  'На компьютерных изображениях застройщика здание поднимается ступенчатыми белыми поясами, с глубокими террасами за стеклянными ограждениями, каменным основанием и садами с длинными отражающими бассейнами, ведущими к морю.',
  'في الصور المُولَّدة بالحاسوب الصادرة عن المطوّر يرتفع المبنى بأشرطة بيضاء متدرجة، مع تراسات عميقة خلف حواجز زجاجية وقاعدة حجرية وحدائق تمتد فيها بِرك عاكسة طويلة باتجاه البحر.',
  'Op de computergegenereerde beelden van de ontwikkelaar rijst het gebouw op in getrapte witte banden, met diepe terrassen achter glazen balustrades, een stenen plint en tuinen met lange spiegelvijvers die naar zee lopen.',
  'Na komputerowych obrazach dewelopera budynek wznosi się w schodkowych białych pasach, z głębokimi tarasami za szklanymi balustradami, kamienną podstawą i ogrodami z długimi basenami refleksyjnymi prowadzącymi ku morzu.',
  'På utbyggerens datagenererte bilder reiser bygningen seg i trappetrinnsformede hvite bånd, med dype terrasser bak glassrekkverk, en steinsokkel og hager med lange speilbasseng som fører mot havet.',
  'På exploatörens datorgenererade bilder reser sig byggnaden i trappstegsformade vita band, med djupa terrasser bakom glasräcken, en stensockel och trädgårdar med långa spegeldammar som leder mot havet.')
a('architecture.copy.1',
  'La entrada desde la calle es una puerta acristalada de doble altura enmarcada en piedra, con lamas de madera, y da a un vestíbulo alto con un mostrador de recepción. El folleto dice que todas las viviendas están orientadas al sur.',
  'L’entrée côté rue est une porte vitrée à double hauteur encadrée de pierre, avec des lames de bois, qui donne sur un haut hall d’entrée avec un comptoir de réception. La brochure indique que tous les logements sont orientés au sud.',
  'Der Eingang an der Straße ist eine doppelgeschossige Glastür in Steinrahmen mit Holzlamellen und führt in eine hohe Eingangshalle mit Empfangstresen. Laut Broschüre sind alle Wohnungen nach Süden ausgerichtet.',
  'Вход со стороны улицы — остеклённая дверь в два света в каменной раме, с деревянными рейками; она ведёт в высокий входной холл со стойкой ресепшена. В брошюре сказано, что все квартиры ориентированы на юг.',
  'مدخل الشارع باب زجاجي بارتفاع مزدوج بإطار حجري وشرائح خشبية، ويفتح على ردهة عالية بمكتب استقبال. ويذكر الكتيّب أن جميع المساكن تواجه الجنوب.',
  'De entree aan de straat is een glazen deur van dubbele hoogte in een stenen omlijsting, met houten latten, en komt uit op een hoge entreehal met een receptiebalie. Volgens de brochure kijken alle woningen op het zuiden uit.',
  'Wejście od strony ulicy to przeszklone drzwi o podwójnej wysokości w kamiennej ramie, z drewnianymi listwami, prowadzące do wysokiego holu z recepcją. Broszura podaje, że wszystkie lokale są zwrócone na południe.',
  'Inngangen mot gaten er en glassdør i to etasjers høyde i en steinramme, med trelameller, og den åpner seg mot et høyt inngangsparti med resepsjonsdisk. Brosjyren sier at alle boligene vender mot sør.',
  'Entrén mot gatan är en glasdörr i dubbel höjd i en stenram, med träribbor, och den leder in till en hög entréhall med receptionsdisk. Broschyren säger att alla bostäder vetter mot söder.')
a('architecture.highlights.0.1',
  'El folleto dice que todas las viviendas tienen orientación sur.', 'La brochure indique que tous les logements ont une orientation sud.',
  'Laut Broschüre hat jede Wohnung eine Südausrichtung.', 'В брошюре сказано, что все квартиры ориентированы на юг.',
  'يذكر الكتيّب أن جميع المساكن تواجه الجنوب.', 'Volgens de brochure hebben alle woningen een zuidelijke oriëntatie.',
  'Broszura podaje, że wszystkie lokale mają orientację południową.', 'Brosjyren sier at alle boligene har sørvendt orientering.',
  'Broschyren säger att alla bostäder har söderläge.')
a('architecture.highlights.1.0', 'Luces interiores', 'Portées intérieures', 'Raumspannweiten', 'Пролёты внутри', 'البحور الداخلية', 'Overspanningen binnen', 'Rozpiętości wnętrz', 'Spennvidder innvendig', 'Spännvidder invändigt')
a('architecture.highlights.1.1',
  'El folleto da luces interiores de hasta 20 metros.', 'La brochure indique des portées intérieures pouvant atteindre 20 mètres.',
  'Die Broschüre nennt Raumspannweiten von bis zu 20 Metern.', 'В брошюре указаны пролёты внутри до 20 метров.',
  'يذكر الكتيّب بحورًا داخلية تصل إلى 20 مترًا.', 'De brochure noemt overspanningen binnen tot 20 meter.',
  'Broszura podaje rozpiętości wnętrz do 20 metrów.', 'Brosjyren oppgir innvendige spenn på opptil 20 meter.',
  'Broschyren anger invändiga spännvidder på upp till 20 meter.')
a('architecture.highlights.2.0', 'Ascensor privado', 'Ascenseur privé', 'Privater Aufzug', 'Частный лифт', 'مصعد خاص', 'Eigen lift', 'Prywatna winda', 'Egen heis', 'Egen hiss')
a('architecture.highlights.2.1',
  'Los planos de las cinco viviendas listadas muestran un ascensor privado que se abre a la vivienda.',
  'Les plans des cinq logements listés montrent un ascenseur privé qui s’ouvre dans le logement.',
  'Die Pläne aller fünf aufgeführten Wohnungen zeigen einen privaten Aufzug, der sich in die Wohnung öffnet.',
  'На планах всех пяти указанных квартир показан частный лифт, открывающийся прямо в квартиру.',
  'تُظهر مخططات المساكن الخمسة المدرجة مصعدًا خاصًا يفتح مباشرةً على المسكن.',
  'De plattegronden van alle vijf vermelde woningen tonen een eigen lift die in de woning uitkomt.',
  'Rzuty wszystkich pięciu wymienionych lokali pokazują prywatną windę otwierającą się wprost do lokalu.',
  'Planene for alle de fem oppførte boligene viser en egen heis som åpner seg inn i boligen.',
  'Planritningarna för alla fem listade bostäder visar en egen hiss som öppnar sig in i bostaden.')
a('architecture.highlights.3.1',
  'El folleto presenta las amplias terrazas con vistas al mar como un rasgo definitorio, y los planos dibujan una pequeña piscina en cada una.',
  'La brochure présente les grandes terrasses face à la mer comme un trait distinctif, et les plans dessinent une petite piscine sur chacune.',
  'Die Broschüre stellt die großen Terrassen mit Meerblick als prägendes Merkmal dar, und die Pläne zeichnen auf jeder einen kleinen Pool ein.',
  'В брошюре большие террасы с видом на море названы определяющей особенностью, а на планах на каждой нарисован небольшой бассейн.',
  'يقدّم الكتيّب التراسات الواسعة المطلة على البحر بوصفها سمة مميزة، وترسم المخططات مسبحًا صغيرًا على كل منها.',
  'De brochure presenteert de grote terrassen met zeezicht als een bepalend kenmerk, en de plattegronden tekenen op elk ervan een klein zwembad.',
  'Broszura przedstawia duże tarasy z widokiem na morze jako cechę wyróżniającą, a rzuty rysują na każdym z nich mały basen.',
  'Brosjyren presenterer de store terrassene mot havet som et kjennetegn, og planene tegner et lite basseng på hver av dem.',
  'Broschyren presenterar de stora terrasserna mot havet som ett kännetecken, och planritningarna ritar in en liten pool på var och en.')

# ---- residences ------------------------------------------------------------------------------------

a('residences.headlineHtml', 'Cinco viviendas, <em>tres distribuciones</em>', 'Cinq logements, <em>trois plans</em>', 'Fünf Wohnungen, <em>drei Grundrisse</em>',
  'Пять квартир, <em>три планировки</em>', 'خمسة مساكن، <em>ثلاثة مخططات</em>', 'Vijf woningen, <em>drie plattegronden</em>', 'Pięć lokali, <em>trzy układy</em>',
  'Fem boliger, <em>tre planløsninger</em>', 'Fem bostäder, <em>tre planlösningar</em>')
a('residences.copy',
  'Las cinco viviendas listadas se dividen en tres grupos según su plano. La tabla de abajo recoge cada una con su precio.',
  'Les cinq logements listés se répartissent en trois groupes selon leur plan. Le tableau ci-dessous présente chacun avec son prix.',
  'Die fünf aufgeführten Wohnungen gliedern sich nach ihrem Grundriss in drei Gruppen. Die Tabelle unten nennt jede mit ihrem Preis.',
  'Пять указанных квартир делятся на три группы по планировке. В таблице ниже каждая приведена с ценой.',
  'تنقسم المساكن الخمسة المدرجة إلى ثلاث مجموعات بحسب مخططاتها. ويعرض الجدول أدناه كل مسكن مع سعره.',
  'De vijf vermelde woningen vallen naar plattegrond uiteen in drie groepen. De tabel hieronder toont elke woning met haar prijs.',
  'Pięć wymienionych lokali dzieli się według rzutu na trzy grupy. Tabela poniżej podaje każdy z nich wraz z ceną.',
  'De fem oppførte boligene deler seg i tre grupper etter planløsning. Tabellen under viser hver bolig med pris.',
  'De fem listade bostäderna delas in i tre grupper efter planlösning. Tabellen nedan visar varje bostad med dess pris.')
a('residences.items.0.name', 'Viviendas BY-02 y BY-04', 'Logements BY-02 et BY-04', 'Wohnungen BY-02 und BY-04', 'Квартиры BY-02 и BY-04', 'المسكنان BY-02 وBY-04',
  'Woningen BY-02 en BY-04', 'Lokale BY-02 i BY-04', 'Boligene BY-02 og BY-04', 'Bostäderna BY-02 och BY-04')
a('residences.items.0.points.0',
  'Dos viviendas de cuatro dormitorios con {N288.94} {U} construidos según la lista, con una terraza cubierta de {N121.50} {U} y una terraza descubierta de {N47.20} {U} en sus fichas técnicas, tres plazas de aparcamiento y un ascensor privado.',
  'Deux logements de quatre chambres de {N288.94} {U} construits selon la liste, avec une terrasse couverte de {N121.50} {U} et une terrasse découverte de {N47.20} {U} sur leurs fiches techniques, trois places de stationnement et un ascenseur privé.',
  'Zwei Wohnungen mit vier Schlafzimmern und {N288.94} {U} bebauter Fläche laut Liste, mit einer überdachten Terrasse von {N121.50} {U} und einer offenen Terrasse von {N47.20} {U} laut ihren Datenblättern, drei Stellplätzen und einem privaten Aufzug.',
  'Две квартиры с четырьмя спальнями и площадью застройки {N288.94} {U} по списку, с крытой террасой {N121.50} {U} и открытой террасой {N47.20} {U} по их листам с характеристиками, тремя парковочными местами и частным лифтом.',
  'مسكنان بأربع غرف نوم بمساحة مبنية {N288.94} {U} بحسب القائمة، بتراس مسقوف مساحته {N121.50} {U} وتراس مكشوف مساحته {N47.20} {U} بحسب صفحات بياناتهما، وثلاثة مواقف سيارات ومصعد خاص.',
  'Twee woningen met vier slaapkamers en {N288.94} {U} bebouwd volgens de lijst, met een overdekt terras van {N121.50} {U} en een open terras van {N47.20} {U} volgens hun gegevensbladen, drie parkeerplaatsen en een eigen lift.',
  'Dwa lokale z czterema sypialniami o powierzchni zabudowy {N288.94} {U} według listy, z tarasem zadaszonym o powierzchni {N121.50} {U} i tarasem odkrytym o powierzchni {N47.20} {U} według ich kart danych, trzema miejscami parkingowymi i prywatną windą.',
  'To boliger med fire soverom og {N288.94} {U} bebygd areal ifølge listen, med en overbygd terrasse på {N121.50} {U} og en åpen terrasse på {N47.20} {U} ifølge databladene, tre parkeringsplasser og egen heis.',
  'Två bostäder med fyra sovrum och {N288.94} {U} byggyta enligt listan, med en övertäckt terrass på {N121.50} {U} och en öppen terrass på {N47.20} {U} enligt deras datablad, tre parkeringsplatser och egen hiss.')
a('residences.items.0.points.1',
  'Los precios son {E9000000} para el BY-02 y {E7500000} para el BY-04.', 'Les prix sont de {E9000000} pour le BY-02 et de {E7500000} pour le BY-04.',
  'Die Preise betragen {E9000000} für BY-02 und {E7500000} für BY-04.', 'Цены — {E9000000} за BY-02 и {E7500000} за BY-04.',
  'سعر BY-02 هو {E9000000} وسعر BY-04 هو {E7500000}.', 'De prijzen zijn {E9000000} voor BY-02 en {E7500000} voor BY-04.',
  'Ceny wynoszą {E9000000} za BY-02 i {E7500000} za BY-04.', 'Prisene er {E9000000} for BY-02 og {E7500000} for BY-04.',
  'Priserna är {E9000000} för BY-02 och {E7500000} för BY-04.')
a('residences.items.0.points.2',
  'Cada plano tiene un salón-comedor con cocina de {N117.62} {U} (BY-02) y {N116.80} {U} (BY-04), un despacho y cuatro dormitorios, el principal de {N42.56} {U} (BY-02) y {N42.22} {U} (BY-04), y dibuja un trastero de {N82.11} {U}.',
  'Chaque plan comprend un séjour-salle à manger avec cuisine de {N117.62} {U} (BY-02) et de {N116.80} {U} (BY-04), un bureau et quatre chambres, la principale de {N42.56} {U} (BY-02) et de {N42.22} {U} (BY-04), et dessine une cave de {N82.11} {U}.',
  'Jeder Grundriss hat einen Wohn-Essbereich mit Küche von {N117.62} {U} (BY-02) und {N116.80} {U} (BY-04), ein Büro und vier Schlafzimmer, das Hauptschlafzimmer mit {N42.56} {U} (BY-02) und {N42.22} {U} (BY-04), und zeichnet einen Abstellraum von {N82.11} {U} ein.',
  'В каждой планировке есть гостиная-столовая с кухней площадью {N117.62} {U} (BY-02) и {N116.80} {U} (BY-04), кабинет и четыре спальни, главная из них — {N42.56} {U} (BY-02) и {N42.22} {U} (BY-04); на плане нарисована кладовая {N82.11} {U}.',
  'يضم كل مخطط غرفة معيشة وطعام مع مطبخ بمساحة {N117.62} {U} (BY-02) و{N116.80} {U} (BY-04)، ومكتبًا وأربع غرف نوم، الرئيسية منها {N42.56} {U} (BY-02) و{N42.22} {U} (BY-04)، ويرسم غرفة تخزين مساحتها {N82.11} {U}.',
  'Elke plattegrond heeft een woon-eetkamer met keuken van {N117.62} {U} (BY-02) en {N116.80} {U} (BY-04), een kantoor en vier slaapkamers, de hoofdslaapkamer van {N42.56} {U} (BY-02) en {N42.22} {U} (BY-04), en tekent een berging van {N82.11} {U}.',
  'Każdy rzut ma salon z jadalnią i kuchnią o powierzchni {N117.62} {U} (BY-02) i {N116.80} {U} (BY-04), gabinet i cztery sypialnie, w tym główną o powierzchni {N42.56} {U} (BY-02) i {N42.22} {U} (BY-04), oraz rysuje komórkę lokatorską o powierzchni {N82.11} {U}.',
  'Hver plan har en stue med spisestue og kjøkken på {N117.62} {U} (BY-02) og {N116.80} {U} (BY-04), et kontor og fire soverom, hovedsoverommet på {N42.56} {U} (BY-02) og {N42.22} {U} (BY-04), og tegner inn en bod på {N82.11} {U}.',
  'Varje planritning har ett vardagsrum med matplats och kök på {N117.62} {U} (BY-02) och {N116.80} {U} (BY-04), ett kontor och fyra sovrum, huvudsovrummet på {N42.56} {U} (BY-02) och {N42.22} {U} (BY-04), och ritar in ett förråd på {N82.11} {U}.')
a('residences.items.0.points.3',
  'Las fichas técnicas dan las mismas superficies para ambas viviendas, mientras que los planos dibujan una terraza de {N150.60} {U} para el BY-02 y de {N108.52} {U} para el BY-04. La ficha del BY-02 no indica trastero y su plano dibuja uno.',
  'Les fiches techniques donnent les mêmes surfaces pour les deux logements, alors que les plans dessinent une terrasse de {N150.60} {U} pour le BY-02 et de {N108.52} {U} pour le BY-04. La fiche du BY-02 n’indique pas de cave et son plan en dessine une.',
  'Die Datenblätter geben für beide Wohnungen dieselben Flächen an, während die Pläne für BY-02 eine Terrasse von {N150.60} {U} und für BY-04 eine von {N108.52} {U} zeichnen. Das Datenblatt von BY-02 nennt keinen Abstellraum, und sein Plan zeichnet einen ein.',
  'В листах с характеристиками для обеих квартир указаны одинаковые площади, тогда как на планах нарисована терраса {N150.60} {U} для BY-02 и {N108.52} {U} для BY-04. В листе BY-02 кладовая не указана, а на его плане она нарисована.',
  'تعطي صفحات البيانات المساحات نفسها للمسكنين، بينما ترسم المخططات تراسًا مساحته {N150.60} {U} للمسكن BY-02 و{N108.52} {U} للمسكن BY-04. ولا تذكر صفحة بيانات BY-02 غرفة تخزين، بينما يرسم مخططه واحدة.',
  'De gegevensbladen geven voor beide woningen dezelfde oppervlakten, terwijl de plattegronden een terras van {N150.60} {U} voor BY-02 en van {N108.52} {U} voor BY-04 tekenen. Het gegevensblad van BY-02 noemt geen berging en de plattegrond tekent er een.',
  'Karty danych podają dla obu lokali te same powierzchnie, podczas gdy rzuty rysują taras o powierzchni {N150.60} {U} dla BY-02 i {N108.52} {U} dla BY-04. Karta danych BY-02 nie podaje komórki lokatorskiej, a jego rzut ją rysuje.',
  'Databladene oppgir de samme arealene for begge boligene, mens planene tegner en terrasse på {N150.60} {U} for BY-02 og {N108.52} {U} for BY-04. Databladet for BY-02 oppgir ingen bod, og planen tegner inn en.',
  'Databladen anger samma ytor för båda bostäderna, medan planritningarna ritar in en terrass på {N150.60} {U} för BY-02 och {N108.52} {U} för BY-04. Databladet för BY-02 anger inget förråd, och dess planritning ritar in ett.')
a('residences.items.1.name', 'Vivienda BY-06', 'Logement BY-06', 'Wohnung BY-06', 'Квартира BY-06', 'المسكن BY-06', 'Woning BY-06', 'Lokal BY-06', 'Bolig BY-06', 'Bostad BY-06')
a('residences.items.1.points.0',
  'Una vivienda de cuatro dormitorios con {N299.19} {U} construidos, {N261.42} {U} de superficie interior, una parte de {N92.53} {U} de las zonas comunes, lo que suma {N391.72} {U} en total, y un trastero de {N28.42} {U} en la planta de servicios.',
  'Un logement de quatre chambres de {N299.19} {U} construits, avec {N261.42} {U} de surface intérieure, une quote-part de {N92.53} {U} des parties communes, soit {N391.72} {U} au total, et une cave de {N28.42} {U} au niveau des équipements.',
  'Eine Wohnung mit vier Schlafzimmern und {N299.19} {U} bebauter Fläche, mit {N261.42} {U} Innenfläche, einem Anteil von {N92.53} {U} an den Gemeinschaftsflächen, zusammen {N391.72} {U}, und einem Abstellraum von {N28.42} {U} auf der Ausstattungsebene.',
  'Квартира с четырьмя спальнями и площадью застройки {N299.19} {U}, внутренней площадью {N261.42} {U}, долей общих зон {N92.53} {U} — всего {N391.72} {U} — и кладовой {N28.42} {U} на уровне удобств.',
  'مسكن بأربع غرف نوم بمساحة مبنية {N299.19} {U}، ومساحة داخلية {N261.42} {U}، وحصة من المناطق المشتركة قدرها {N92.53} {U}، فيبلغ المجموع {N391.72} {U}، وغرفة تخزين مساحتها {N28.42} {U} في طابق المرافق.',
  'Een woning met vier slaapkamers en {N299.19} {U} bebouwd, met {N261.42} {U} binnenoppervlak, een aandeel van {N92.53} {U} in de gemeenschappelijke ruimten, samen {N391.72} {U}, en een berging van {N28.42} {U} op de voorzieningenlaag.',
  'Lokal z czterema sypialniami o powierzchni zabudowy {N299.19} {U}, z powierzchnią wewnętrzną {N261.42} {U}, udziałem {N92.53} {U} w częściach wspólnych, co daje łącznie {N391.72} {U}, i komórką lokatorską o powierzchni {N28.42} {U} na poziomie udogodnień.',
  'En bolig med fire soverom og {N299.19} {U} bebygd areal, med {N261.42} {U} innvendig areal, en andel på {N92.53} {U} av fellesarealene, til sammen {N391.72} {U}, og en bod på {N28.42} {U} på fasilitetsnivået.',
  'En bostad med fyra sovrum och {N299.19} {U} byggyta, med {N261.42} {U} invändig yta, en andel på {N92.53} {U} av de gemensamma ytorna, tillsammans {N391.72} {U}, och ett förråd på {N28.42} {U} på bekvämlighetsplanet.')
a('residences.items.1.points.1', 'El precio es de {E6500000}.', 'Le prix est de {E6500000}.', 'Der Preis beträgt {E6500000}.', 'Цена — {E6500000}.', 'السعر {E6500000}.',
  'De prijs is {E6500000}.', 'Cena wynosi {E6500000}.', 'Prisen er {E6500000}.', 'Priset är {E6500000}.')
a('residences.items.1.points.2',
  'Su plano tiene un salón-comedor con cocina de {N121.13} {U}, un dormitorio principal de {N32.51} {U}, un lavadero y una cocina sucia.',
  'Son plan comprend un séjour-salle à manger avec cuisine de {N121.13} {U}, une chambre principale de {N32.51} {U}, une buanderie et une cuisine de service.',
  'Sein Plan hat einen Wohn-Essbereich mit Küche von {N121.13} {U}, ein Hauptschlafzimmer von {N32.51} {U}, eine Waschküche und eine Schmutzküche.',
  'На его плане — гостиная-столовая с кухней {N121.13} {U}, главная спальня {N32.51} {U}, прачечная и чёрная кухня.',
  'يضم مخططه غرفة معيشة وطعام مع مطبخ بمساحة {N121.13} {U}، وغرفة نوم رئيسية بمساحة {N32.51} {U}، وغرفة غسيل ومطبخًا خلفيًا.',
  'De plattegrond heeft een woon-eetkamer met keuken van {N121.13} {U}, een hoofdslaapkamer van {N32.51} {U}, een washok en een bijkeuken.',
  'Jego rzut ma salon z jadalnią i kuchnią o powierzchni {N121.13} {U}, sypialnię główną o powierzchni {N32.51} {U}, pralnię i kuchnię pomocniczą.',
  'Planen har en stue med spisestue og kjøkken på {N121.13} {U}, et hovedsoverom på {N32.51} {U}, et vaskerom og et bikjøkken.',
  'Planritningen har ett vardagsrum med matplats och kök på {N121.13} {U}, ett huvudsovrum på {N32.51} {U}, ett tvättrum och ett skitkök.')
a('residences.items.1.points.3',
  'La tabla de su plano da porches de {N118.50} {U} y terrazas de {N137.73} {U}, mientras que el dibujo rotula una terraza de {N191.37} {U} y una terraza de acceso de {N41.81} {U}.',
  'Le tableau de son plan donne des porches de {N118.50} {U} et des terrasses de {N137.73} {U}, alors que le dessin indique une terrasse de {N191.37} {U} et une terrasse d’accès de {N41.81} {U}.',
  'Die Tabelle auf seinem Plan nennt Vorbauten von {N118.50} {U} und Terrassen von {N137.73} {U}, während die Zeichnung eine Terrasse von {N191.37} {U} und eine Zugangsterrasse von {N41.81} {U} beschriftet.',
  'В таблице на его плане указаны крытые галереи (porches) {N118.50} {U} и террасы {N137.73} {U}, а на чертеже подписаны терраса {N191.37} {U} и входная терраса {N41.81} {U}.',
  'يعطي الجدول على مخططه أروقة (porches) بمساحة {N118.50} {U} وتراسات بمساحة {N137.73} {U}، بينما يشير الرسم إلى تراس بمساحة {N191.37} {U} وتراس مدخل بمساحة {N41.81} {U}.',
  'De tabel op de plattegrond geeft overdekte galerijen (porches) van {N118.50} {U} en terrassen van {N137.73} {U}, terwijl de tekening een terras van {N191.37} {U} en een toegangsterras van {N41.81} {U} aanduidt.',
  'Tabela na jego rzucie podaje ganki (porches) o powierzchni {N118.50} {U} i tarasy o powierzchni {N137.73} {U}, a rysunek opisuje taras o powierzchni {N191.37} {U} i taras wejściowy o powierzchni {N41.81} {U}.',
  'Tabellen på planen oppgir overbygde gallerier (porches) på {N118.50} {U} og terrasser på {N137.73} {U}, mens tegningen merker en terrasse på {N191.37} {U} og en inngangsterrasse på {N41.81} {U}.',
  'Tabellen på planritningen anger överbyggda gallerier (porches) på {N118.50} {U} och terrasser på {N137.73} {U}, medan ritningen anger en terrass på {N191.37} {U} och en entréterrass på {N41.81} {U}.')
a('residences.items.2.name', 'Viviendas BY-07 y BY-08', 'Logements BY-07 et BY-08', 'Wohnungen BY-07 und BY-08', 'Квартиры BY-07 и BY-08', 'المسكنان BY-07 وBY-08',
  'Woningen BY-07 en BY-08', 'Lokale BY-07 i BY-08', 'Boligene BY-07 og BY-08', 'Bostäderna BY-07 och BY-08')
a('residences.items.2.points.0',
  'Dos viviendas de cuatro dormitorios con la misma distribución: un salón-comedor con cocina de {N121.13} {U}, una cocina sucia, un lavadero, cuatro dormitorios de {N17.52} a {N28.52} {U} y una terraza de {N118.87} {U} en los planos.',
  'Deux logements de quatre chambres au même plan : un séjour-salle à manger avec cuisine de {N121.13} {U}, une cuisine de service, une buanderie, quatre chambres de {N17.52} à {N28.52} {U} et une terrasse de {N118.87} {U} sur les plans.',
  'Zwei Wohnungen mit vier Schlafzimmern und gleichem Grundriss: ein Wohn-Essbereich mit Küche von {N121.13} {U}, eine Schmutzküche, eine Waschküche, vier Schlafzimmer von {N17.52} bis {N28.52} {U} und eine Terrasse von {N118.87} {U} laut Plänen.',
  'Две квартиры с четырьмя спальнями и одинаковой планировкой: гостиная-столовая с кухней {N121.13} {U}, чёрная кухня, прачечная, четыре спальни от {N17.52} до {N28.52} {U} и терраса {N118.87} {U} по планам.',
  'مسكنان بأربع غرف نوم ومخطط واحد: غرفة معيشة وطعام مع مطبخ بمساحة {N121.13} {U}، ومطبخ خلفي، وغرفة غسيل، وأربع غرف نوم من {N17.52} إلى {N28.52} {U}، وتراس بمساحة {N118.87} {U} بحسب المخططات.',
  'Twee woningen met vier slaapkamers en dezelfde plattegrond: een woon-eetkamer met keuken van {N121.13} {U}, een bijkeuken, een washok, vier slaapkamers van {N17.52} tot {N28.52} {U} en een terras van {N118.87} {U} volgens de plattegronden.',
  'Dwa lokale z czterema sypialniami i takim samym układem: salon z jadalnią i kuchnią o powierzchni {N121.13} {U}, kuchnia pomocnicza, pralnia, cztery sypialnie od {N17.52} do {N28.52} {U} i taras o powierzchni {N118.87} {U} według rzutów.',
  'To boliger med fire soverom og samme planløsning: en stue med spisestue og kjøkken på {N121.13} {U}, et bikjøkken, et vaskerom, fire soverom på {N17.52} til {N28.52} {U} og en terrasse på {N118.87} {U} etter planene.',
  'Två bostäder med fyra sovrum och samma planlösning: ett vardagsrum med matplats och kök på {N121.13} {U}, ett skitkök, ett tvättrum, fyra sovrum på {N17.52} till {N28.52} {U} och en terrass på {N118.87} {U} enligt planritningarna.')
a('residences.items.2.points.1',
  'Sus fichas técnicas dan una terraza cubierta de {N69.37} {U}, una terraza descubierta de {N62.50} {U}, tres plazas de aparcamiento y un trastero de {N28.42} {U} (BY-07) y de {N28.07} {U} (BY-08).',
  'Leurs fiches techniques donnent une terrasse couverte de {N69.37} {U}, une terrasse découverte de {N62.50} {U}, trois places de stationnement et une cave de {N28.42} {U} (BY-07) et de {N28.07} {U} (BY-08).',
  'Ihre Datenblätter nennen eine überdachte Terrasse von {N69.37} {U}, eine offene Terrasse von {N62.50} {U}, drei Stellplätze und einen Abstellraum von {N28.42} {U} (BY-07) und {N28.07} {U} (BY-08).',
  'В их листах с характеристиками указаны крытая терраса {N69.37} {U}, открытая терраса {N62.50} {U}, три парковочных места и кладовая {N28.42} {U} (BY-07) и {N28.07} {U} (BY-08).',
  'تذكر صفحتا بياناتهما تراسًا مسقوفًا بمساحة {N69.37} {U}، وتراسًا مكشوفًا بمساحة {N62.50} {U}، وثلاثة مواقف سيارات، وغرفة تخزين بمساحة {N28.42} {U} (BY-07) و{N28.07} {U} (BY-08).',
  'Hun gegevensbladen geven een overdekt terras van {N69.37} {U}, een open terras van {N62.50} {U}, drie parkeerplaatsen en een berging van {N28.42} {U} (BY-07) en {N28.07} {U} (BY-08).',
  'Ich karty danych podają taras zadaszony o powierzchni {N69.37} {U}, taras odkryty o powierzchni {N62.50} {U}, trzy miejsca parkingowe i komórkę lokatorską o powierzchni {N28.42} {U} (BY-07) i {N28.07} {U} (BY-08).',
  'Databladene deres oppgir en overbygd terrasse på {N69.37} {U}, en åpen terrasse på {N62.50} {U}, tre parkeringsplasser og en bod på {N28.42} {U} (BY-07) og {N28.07} {U} (BY-08).',
  'Deras datablad anger en övertäckt terrass på {N69.37} {U}, en öppen terrass på {N62.50} {U}, tre parkeringsplatser och ett förråd på {N28.42} {U} (BY-07) och {N28.07} {U} (BY-08).')
a('residences.items.2.points.2', 'Cada una cuesta {E6900000}.', 'Chacun coûte {E6900000}.', 'Jede kostet {E6900000}.', 'Каждая стоит {E6900000}.', 'يبلغ سعر كل منهما {E6900000}.',
  'Elk kost {E6900000}.', 'Każdy kosztuje {E6900000}.', 'Hver koster {E6900000}.', 'Var och en kostar {E6900000}.')
a('residences.items.2.points.3',
  'La lista da {N285.64} {U} construidos para ambas. La ficha del BY-08 coincide, y la del BY-07 da {N249.46} {U}.',
  'La liste donne {N285.64} {U} construits pour les deux. La fiche du BY-08 concorde, et celle du BY-07 donne {N249.46} {U}.',
  'Die Liste nennt für beide {N285.64} {U} bebaute Fläche. Das Datenblatt von BY-08 stimmt damit überein, das von BY-07 nennt {N249.46} {U}.',
  'В списке для обеих указана площадь застройки {N285.64} {U}. Лист BY-08 с этим совпадает, а лист BY-07 даёт {N249.46} {U}.',
  'تعطي القائمة {N285.64} {U} مبنية للمسكنين. وتتفق صفحة بيانات BY-08 مع ذلك، بينما تعطي صفحة BY-07 {N249.46} {U}.',
  'De lijst geeft voor beide {N285.64} {U} bebouwd. Het gegevensblad van BY-08 komt daarmee overeen, dat van BY-07 geeft {N249.46} {U}.',
  'Lista podaje dla obu {N285.64} {U} powierzchni zabudowy. Karta danych BY-08 jest zgodna, a karta BY-07 podaje {N249.46} {U}.',
  'Listen oppgir {N285.64} {U} bebygd areal for begge. Databladet for BY-08 stemmer, og databladet for BY-07 oppgir {N249.46} {U}.',
  'Listan anger {N285.64} {U} byggyta för båda. Databladet för BY-08 stämmer, och databladet för BY-07 anger {N249.46} {U}.')

# ---- lifestyle -------------------------------------------------------------------------------------

a('lifestyle.headlineHtml', 'Piscinas, spa <em>y una sala de cine</em>', 'Des piscines, un spa <em>et une salle de cinéma</em>', 'Pools, Spa <em>und ein Kinoraum</em>',
  'Бассейны, спа <em>и кинозал</em>', 'مسابح وسبا <em>وغرفة سينما</em>', 'Zwembaden, spa <em>en een bioscoopzaal</em>', 'Baseny, spa <em>i sala kinowa</em>',
  'Basseng, spa <em>og en kinosal</em>', 'Pooler, spa <em>och en biosalong</em>')
a('lifestyle.copy',
  'El folleto describe las zonas comunes como un club privado en casa. Los planos las dibujan en una sola planta, y las recreaciones muestran la piscina exterior, el spa y las salas.',
  'La brochure décrit les parties communes comme un club privé à domicile. Les plans les dessinent sur un seul niveau, et les visuels de synthèse montrent la piscine extérieure, le spa et les salles.',
  'Die Broschüre beschreibt die Gemeinschaftsbereiche als privaten Club zu Hause. Die Pläne zeichnen sie auf einer Ebene, und die Renderings zeigen den Außenpool, das Spa und die Räume.',
  'В брошюре общие зоны описаны как частный клуб у себя дома. На планах они нарисованы на одном уровне, а на визуализациях показаны открытый бассейн, спа и помещения.',
  'يصف الكتيّب المناطق المشتركة بأنها نادٍ خاص في المنزل. وترسمها المخططات في طابق واحد، وتُظهر الصور المُولَّدة المسبح الخارجي والسبا والقاعات.',
  'De brochure beschrijft de gemeenschappelijke ruimten als een privéclub aan huis. De plattegronden tekenen ze op één laag, en de renderings tonen het buitenzwembad, de spa en de ruimten.',
  'Broszura opisuje części wspólne jako prywatny klub w domu. Rzuty rysują je na jednym poziomie, a wizualizacje pokazują basen zewnętrzny, spa i pomieszczenia.',
  'Brosjyren beskriver fellesarealene som en privat klubb hjemme. Planene tegner dem på ett nivå, og visualiseringene viser utendørsbassenget, spaet og rommene.',
  'Broschyren beskriver de gemensamma ytorna som en privat klubb hemma. Planritningarna ritar in dem på ett plan, och visualiseringarna visar utomhuspoolen, spaet och rummen.')
a('lifestyle.panels.0.1',
  'Una piscina exterior que se abre hacia el mar, con estanques reflectantes y vegetación mediterránea, según el folleto.',
  'Une piscine extérieure qui s’ouvre vers la mer, avec des miroirs d’eau et une végétation méditerranéenne, selon la brochure.',
  'Ein Außenpool, der sich zum Meer hin öffnet, mit Spiegelbecken und mediterraner Bepflanzung, laut Broschüre.',
  'Открытый бассейн, обращённый к морю, с отражающими бассейнами и средиземноморской зеленью, согласно брошюре.',
  'مسبح خارجي ينفتح نحو البحر، مع برك عاكسة ونباتات متوسطية، بحسب الكتيّب.',
  'Een buitenzwembad dat uitkijkt op zee, met spiegelvijvers en mediterrane beplanting, volgens de brochure.',
  'Basen zewnętrzny otwarty ku morzu, z basenami refleksyjnymi i śródziemnomorską roślinnością, według broszury.',
  'Et utendørsbasseng som åpner seg mot havet, med speilbasseng og middelhavsbeplantning, ifølge brosjyren.',
  'En utomhuspool som öppnar sig mot havet, med spegeldammar och medelhavsväxter, enligt broschyren.')
a('lifestyle.panels.1.1',
  'Los planos recogen un spa con sauna y baño de vapor, y las recreaciones muestran una piscina interior con tumbonas y paneles de mosaico.',
  'Les plans indiquent un spa avec sauna et bain de vapeur, et les visuels de synthèse montrent une piscine intérieure avec transats et panneaux de mosaïque.',
  'Die Pläne führen ein Spa mit Sauna und Dampfbad auf, und die Renderings zeigen einen Innenpool mit Liegen und Mosaikpaneelen.',
  'На планах указано спа с сауной и паровой баней, а на визуализациях показан крытый бассейн с шезлонгами и мозаичными панно.',
  'تذكر المخططات سبا بساونا وحمام بخار، وتُظهر الصور المُولَّدة مسبحًا داخليًا بكراسي استلقاء ولوحات فسيفساء.',
  'De plattegronden vermelden een spa met sauna en stoombad, en de renderings tonen een binnenzwembad met ligbedden en mozaïekpanelen.',
  'Rzuty wymieniają spa z sauną i łaźnią parową, a wizualizacje pokazują basen wewnętrzny z leżakami i panelami z mozaiki.',
  'Planene oppfører et spa med badstue og dampbad, og visualiseringene viser et innendørsbasseng med solsenger og mosaikkpaneler.',
  'Planritningarna anger ett spa med bastu och ångbastu, och visualiseringarna visar en inomhuspool med solsängar och mosaikpaneler.')
a('lifestyle.panels.2.1',
  'Un gimnasio en la planta de servicios, y un estudio de fitness que aparece en el folleto.',
  'Une salle de sport au niveau des équipements, et un studio de fitness que montre la brochure.',
  'Ein Fitnessraum auf der Ausstattungsebene und ein Fitnessstudio, das in der Broschüre gezeigt wird.',
  'Тренажёрный зал на уровне удобств и фитнес-студия, показанная в брошюре.',
  'صالة رياضية في طابق المرافق، واستوديو لياقة يظهر في الكتيّب.',
  'Een fitnessruimte op de voorzieningenlaag en een fitnessstudio die in de brochure te zien is.',
  'Siłownia na poziomie udogodnień oraz studio fitness pokazane w broszurze.',
  'Et treningsrom på fasilitetsnivået og et treningsstudio som vises i brosjyren.',
  'Ett gym på bekvämlighetsplanet och en träningsstudio som visas i broschyren.')
a('lifestyle.panels.3.0', 'Cine y golf', 'Cinéma et golf', 'Kino und Golf', 'Кино и гольф', 'السينما والغولف', 'Bioscoop en golf', 'Kino i golf', 'Kino og golf', 'Bio och golf')
a('lifestyle.panels.3.1',
  'Una sala de cine y un simulador de golf, ambos en el plano de servicios.', 'Une salle de cinéma et un simulateur de golf, tous deux sur le plan des équipements.',
  'Ein Kinoraum und ein Golfsimulator, beide auf dem Plan der Ausstattungsebene.', 'Кинозал и гольф-симулятор — оба на плане уровня удобств.',
  'غرفة سينما ومحاكي غولف، وكلاهما في مخطط طابق المرافق.', 'Een bioscoopzaal en een golfsimulator, beide op de plattegrond van de voorzieningenlaag.',
  'Sala kinowa i symulator golfa, oba na rzucie poziomu udogodnień.', 'En kinosal og en golfsimulator, begge på planen for fasilitetsnivået.',
  'En biosalong och en golfsimulator, båda på planritningen för bekvämlighetsplanet.')
a('lifestyle.panels.4.0', 'Juegos y encuentros', 'Jeux et rencontres', 'Spielen und Zusammenkommen', 'Игры и встречи', 'الألعاب واللقاءات', 'Spelen en samenkomen', 'Gry i spotkania', 'Spill og samvær', 'Spel och samvaro')
a('lifestyle.panels.4.1',
  'Una sala de juegos, un salón social y una sala polivalente.', 'Une salle de jeux, un salon commun et une salle polyvalente.',
  'Ein Spielzimmer, eine Gemeinschaftslounge und ein Mehrzweckraum.', 'Игровая комната, общая гостиная и многофункциональное помещение.',
  'غرفة ألعاب وصالة اجتماعية وغرفة متعددة الاستعمالات.', 'Een spelkamer, een gemeenschappelijke lounge en een multifunctionele ruimte.',
  'Sala gier, salon wspólny i sala wielofunkcyjna.', 'Et spillrom, en fellesstue og et flerbruksrom.', 'Ett spelrum, ett gemensamhetsrum och ett flexibelt rum.')

# ---- location --------------------------------------------------------------------------------------

a('location.headlineHtml', 'Frente al mar, <em>en Estepona</em>', 'En bord de mer, <em>à Estepona</em>', 'Direkt am Meer, <em>in Estepona</em>',
  'На берегу моря, <em>в Эстепоне</em>', 'على الواجهة البحرية، <em>في إستيبونا</em>', 'Aan zee, <em>in Estepona</em>', 'Przy morzu, <em>w Esteponie</em>',
  'Ved sjøen, <em>i Estepona</em>', 'Vid havet, <em>i Estepona</em>')
a('location.copy',
  'El promotor sitúa Biubay directamente frente al mar en Estepona, cerca del puerto deportivo, con vistas a un tramo tranquilo y rocoso de costa, alejado de las playas de baño más concurridas. Los documentos no dan dirección postal, así que el marcador del mapa está en el centro de Estepona y no en la parcela, y las distancias por carretera junto al mapa se miden desde ese marcador.',
  'Le promoteur situe Biubay directement en bord de mer à Estepona, près du port de plaisance, face à un tronçon de côte calme et rocheux, à l’écart des plages de baignade les plus fréquentées. Les documents ne donnent pas d’adresse postale : le repère de la carte se trouve donc au centre d’Estepona et non sur la parcelle, et les distances routières à côté de la carte sont mesurées depuis ce repère.',
  'Der Bauträger legt Biubay direkt ans Meer in Estepona, in die Nähe des Yachthafens, mit Blick auf einen ruhigen, felsigen Küstenabschnitt abseits der belebteren Badestrände. Die Unterlagen nennen keine Straßenadresse, daher liegt die Markierung auf der Karte im Zentrum von Estepona und nicht auf dem Grundstück, und die Straßenentfernungen neben der Karte werden von dieser Markierung aus gemessen.',
  'Застройщик помещает Biubay прямо на берегу моря в Эстепоне, вблизи порта-марины, с видом на спокойный скалистый участок побережья вдали от самых оживлённых пляжей. В документах нет почтового адреса, поэтому маркер на карте стоит в центре Эстепоны, а не на участке, и расстояния по дорогам рядом с картой отсчитываются от этого маркера.',
  'يضع المطوّر Biubay مباشرةً على الواجهة البحرية في إستيبونا، قرب المرسى، مطلًّا على امتداد هادئ وصخري من الساحل بعيدًا عن شواطئ الاستحمام الأكثر ازدحامًا. ولا تعطي الوثائق عنوانًا بريديًا، لذلك فإن العلامة على الخريطة في وسط إستيبونا وليست على القطعة، وتُقاس مسافات الطرق بجانب الخريطة من هذه العلامة.',
  'De ontwikkelaar plaatst Biubay direct aan zee in Estepona, vlak bij de jachthaven, met uitzicht op een rustig, rotsachtig stuk kust, ver van de drukkere zwemstranden. De documenten geven geen postadres, dus de markering op de kaart staat in het centrum van Estepona en niet op het perceel, en de wegafstanden naast de kaart worden vanaf die markering gemeten.',
  'Deweloper umiejscawia Biubay bezpośrednio nad morzem w Esteponie, w pobliżu mariny, z widokiem na spokojny, skalisty odcinek wybrzeża, z dala od najbardziej uczęszczanych plaż kąpielowych. Dokumenty nie podają adresu, więc znacznik na mapie stoi w centrum Estepony, a nie na działce, a odległości drogowe obok mapy liczone są od tego znacznika.',
  'Utbyggeren plasserer Biubay rett ved sjøen i Estepona, nær marinaen, med utsikt over en rolig, svaberget kyststripe, vekk fra de mest travle badestrendene. Dokumentene oppgir ingen postadresse, så markøren på kartet står i sentrum av Estepona og ikke på tomten, og veiavstandene ved siden av kartet måles fra denne markøren.',
  'Exploatören placerar Biubay direkt vid havet i Estepona, nära marinan, med utsikt över en lugn, klippig kuststräcka, långt från de mest besökta badstränderna. Dokumenten anger ingen postadress, så markören på kartan står i centrala Estepona och inte på tomten, och vägavstånden bredvid kartan mäts från den markören.')
a('location.mapLabelHtml', 'Frente al mar, <em>Estepona</em>', 'Bord de mer, <em>Estepona</em>', 'Am Meer, <em>Estepona</em>', 'У моря, <em>Эстепона</em>',
  'الواجهة البحرية، <em>إستيبونا</em>', 'Aan zee, <em>Estepona</em>', 'Przy morzu, <em>Estepona</em>', 'Ved sjøen, <em>Estepona</em>', 'Vid havet, <em>Estepona</em>')
a('location.mapLabelPlain', 'Frente al mar, Estepona', 'Bord de mer, Estepona', 'Am Meer, Estepona', 'У моря, Эстепона', 'الواجهة البحرية، إستيبونا',
  'Aan zee, Estepona', 'Przy morzu, Estepona', 'Ved sjøen, Estepona', 'Vid havet, Estepona')
DIST = {  # "<n> minutes, as the brochure says"
 'es': '{n} minutos, según el folleto', 'fr': '{n} minutes, selon la brochure', 'de': '{n} Minuten, laut Broschüre',
 'ru': '{n} минут, по данным брошюры', 'ar': '{n} دقيقة، بحسب الكتيّب', 'nl': '{n} minuten, volgens de brochure',
 'pl': '{n} minut, według broszury', 'no': '{n} minutter, ifølge brosjyren', 'sv': '{n} minuter, enligt broschyren'}
for i, n in enumerate(['20', '25', '35', '50', '60', '70']):
    a(f'location.distances.{i}.1', *[DIST[l].format(n=n) for l in LOCS])
a('location.distances.5.0', 'Tarifa', 'Tarifa', 'Tarifa', 'Тарифа', 'طريفة', 'Tarifa', 'Tarifa', 'Tarifa', 'Tarifa')

# ---- investment, trust dossier ---------------------------------------------------------------------

a('investment.cards.0.1',
  'Cinco de las diez viviendas figuran en la lista del promotor con precio, de {E6500000} a {E9000000} más IVA. Los documentos que tenemos no dicen si las otras cinco están vendidas, reservadas o aún sin lanzar.',
  'Cinq des dix logements figurent sur la liste du promoteur avec un prix, de {E6500000} à {E9000000} hors TVA. Les documents dont nous disposons ne disent pas si les cinq autres sont vendus, réservés ou pas encore commercialisés.',
  'Fünf der zehn Wohnungen stehen mit Preis auf der Liste des Bauträgers, von {E6500000} bis {E9000000} zuzüglich MwSt. Die uns vorliegenden Unterlagen sagen nicht, ob die übrigen fünf verkauft, reserviert oder noch nicht freigegeben sind.',
  'Пять из десяти квартир указаны в списке застройщика с ценой — от {E6500000} до {E9000000} без НДС. В имеющихся у нас документах не сказано, проданы ли остальные пять, зарезервированы или ещё не выставлены.',
  'خمسة من المساكن العشرة مدرجة في قائمة المطوّر بسعر، من {E6500000} إلى {E9000000} دون ضريبة القيمة المضافة. ولا تذكر الوثائق التي بحوزتنا ما إذا كانت الخمسة الأخرى مباعة أو محجوزة أو لم تُطرح بعد.',
  'Vijf van de tien woningen staan met een prijs op de lijst van de ontwikkelaar, van {E6500000} tot {E9000000} excl. btw. De documenten waarover we beschikken zeggen niet of de andere vijf verkocht, gereserveerd of nog niet vrijgegeven zijn.',
  'Pięć z dziesięciu lokali jest na liście dewelopera z ceną, od {E6500000} do {E9000000} plus VAT. Dokumenty, którymi dysponujemy, nie mówią, czy pozostałe pięć jest sprzedanych, zarezerwowanych czy jeszcze nieudostępnionych.',
  'Fem av de ti boligene står med pris på utbyggerens liste, fra {E6500000} til {E9000000} pluss mva. Dokumentene vi har sier ikke om de øvrige fem er solgt, reservert eller ennå ikke lansert.',
  'Fem av de tio bostäderna står med pris på exploatörens lista, från {E6500000} till {E9000000} plus IVA. Dokumenten vi har anger inte om de övriga fem är sålda, reserverade eller ännu inte släppta.')
a('investment.cards.1.1',
  'La lista da la cifra neta del promotor y la hoja informativa añade el IVA a cada pago, de modo que los precios son más IVA. Los documentos que tenemos no indican el tipo, y Nueva Living lo confirma por escrito junto con los demás gastos de compra.',
  'La liste donne le montant net du promoteur et la fiche d’information ajoute la TVA (IVA) à chaque versement : les prix s’entendent donc hors TVA. Les documents dont nous disposons n’indiquent pas le taux, et Nueva Living le confirme par écrit avec les autres frais d’achat.',
  'Die Liste nennt den Nettobetrag des Bauträgers, und das Infoblatt rechnet bei jeder Rate die MwSt. hinzu, die Preise verstehen sich daher zuzüglich MwSt. Die uns vorliegenden Unterlagen nennen den Satz nicht, und Nueva Living bestätigt ihn und die übrigen Kaufnebenkosten schriftlich.',
  'В списке указана чистая цена застройщика, а в информационном листе к каждому платежу добавляется НДС, поэтому цены даны без НДС. В имеющихся у нас документах ставка не указана, и Nueva Living подтверждает её и прочие расходы на покупку письменно.',
  'تعطي القائمة المبلغ الصافي للمطوّر وتضيف النشرة التعريفية ضريبة القيمة المضافة إلى كل دفعة، لذلك فالأسعار دون الضريبة. ولا تذكر الوثائق التي بحوزتنا النسبة، وتؤكدها Nueva Living كتابةً مع سائر تكاليف الشراء.',
  'De lijst geeft het nettobedrag van de ontwikkelaar en het infoblad voegt btw toe aan elke termijn, dus de prijzen zijn exclusief btw. De documenten waarover we beschikken noemen het tarief niet, en Nueva Living bevestigt het en de overige aankoopkosten schriftelijk.',
  'Lista podaje kwotę netto dewelopera, a karta informacyjna dolicza VAT do każdej raty, więc ceny są podane bez VAT. Dokumenty, którymi dysponujemy, nie podają stawki, a Nueva Living potwierdza ją i pozostałe koszty zakupu na piśmie.',
  'Listen oppgir utbyggerens nettobeløp, og infoarket legger mva. til hver innbetaling, så prisene er eksklusive mva. Dokumentene vi har oppgir ikke satsen, og Nueva Living bekrefter den og de øvrige kjøpskostnadene skriftlig.',
  'Listan anger exploatörens nettobelopp, och infobladet lägger IVA (spansk moms) på varje betalning, så priserna är exklusive IVA. Dokumenten vi har anger inte skattesatsen, och Nueva Living bekräftar den och de övriga köpkostnaderna skriftligen.')
a('investment.cards.2.1',
  'El promotor fija un importe de reserva y un calendario de pagos escalonado. Confirmamos por escrito las condiciones vigentes antes de cualquier reserva.',
  'Le promoteur fixe un montant de réservation et un échéancier de paiement échelonné. Nous confirmons par écrit les conditions en vigueur avant toute réservation.',
  'Der Bauträger legt einen Reservierungsbetrag und einen gestaffelten Zahlungsplan fest. Wir bestätigen die geltenden Bedingungen vor jeder Reservierung schriftlich.',
  'Застройщик устанавливает сумму бронирования и поэтапный график платежей. Перед любым бронированием мы письменно подтверждаем действующие условия.',
  'يحدد المطوّر مبلغ الحجز وجدول دفعات مرحليًا. ونؤكد الشروط السارية كتابةً قبل أي حجز.',
  'De ontwikkelaar stelt een reserveringsbedrag en een gefaseerd betalingsschema vast. We bevestigen de geldende voorwaarden vóór elke reservering schriftelijk.',
  'Deweloper ustala kwotę rezerwacji i etapowy harmonogram płatności. Przed każdą rezerwacją potwierdzamy obowiązujące warunki na piśmie.',
  'Utbyggeren fastsetter et reservasjonsbeløp og en trinnvis betalingsplan. Vi bekrefter gjeldende vilkår skriftlig før enhver reservasjon.',
  'Exploatören fastställer ett reservationsbelopp och en stegvis betalningsplan. Vi bekräftar gällande villkor skriftligen före varje reservation.')
a('investment.cards.3.1',
  'Las fichas técnicas dan tres plazas de aparcamiento para el BY-02, BY-04, BY-07 y BY-08, y los planos muestran un trastero de {N28.07} a {N82.11} {U}. La ficha del BY-06 no indica aparcamiento, así que confirmamos qué incluye cada vivienda.',
  'Les fiches techniques donnent trois places de stationnement pour les BY-02, BY-04, BY-07 et BY-08, et les plans montrent une cave de {N28.07} à {N82.11} {U}. La fiche du BY-06 n’indique pas de stationnement, nous confirmons donc ce que comprend chaque logement.',
  'Die Datenblätter nennen drei Stellplätze für BY-02, BY-04, BY-07 und BY-08, und die Pläne zeigen einen Abstellraum von {N28.07} bis {N82.11} {U}. Das Datenblatt von BY-06 nennt keinen Stellplatz, daher bestätigen wir, was jede Wohnung umfasst.',
  'В листах с характеристиками для BY-02, BY-04, BY-07 и BY-08 указаны три парковочных места, а на планах показана кладовая от {N28.07} до {N82.11} {U}. В листе BY-06 парковка не указана, поэтому мы подтверждаем, что входит в каждую квартиру.',
  'تذكر صفحات البيانات ثلاثة مواقف سيارات للمساكن BY-02 وBY-04 وBY-07 وBY-08، وتُظهر المخططات غرفة تخزين من {N28.07} إلى {N82.11} {U}. ولا تذكر صفحة BY-06 مواقف، لذلك نؤكد ما يشمله كل مسكن.',
  'De gegevensbladen geven drie parkeerplaatsen voor BY-02, BY-04, BY-07 en BY-08, en de plattegronden tonen een berging van {N28.07} tot {N82.11} {U}. Het blad van BY-06 noemt geen parkeerplaats, dus we bevestigen wat elke woning omvat.',
  'Karty danych podają trzy miejsca parkingowe dla BY-02, BY-04, BY-07 i BY-08, a rzuty pokazują komórkę lokatorską o powierzchni od {N28.07} do {N82.11} {U}. Karta BY-06 nie podaje parkingu, więc potwierdzamy, co obejmuje każdy lokal.',
  'Databladene oppgir tre parkeringsplasser for BY-02, BY-04, BY-07 og BY-08, og planene viser en bod på {N28.07} til {N82.11} {U}. Databladet for BY-06 oppgir ingen parkering, så vi bekrefter hva hver bolig omfatter.',
  'Databladen anger tre parkeringsplatser för BY-02, BY-04, BY-07 och BY-08, och planritningarna visar ett förråd på {N28.07} till {N82.11} {U}. Databladet för BY-06 anger ingen parkering, så vi bekräftar vad varje bostad omfattar.')
a('trustDossier.cards.0.1',
  'La hoja informativa indica que la licencia de obras está concedida y que las obras empezaron en marzo de 2026. No lleva fecha, así que pedimos la licencia y el estado de las obras tal como están.',
  'La fiche d’information indique que le permis de construire est accordé et que les travaux ont commencé en mars 2026. Elle n’est pas datée, nous demandons donc le permis et l’état d’avancement des travaux tels qu’ils sont.',
  'Das Infoblatt nennt die Baugenehmigung als erteilt und den Baubeginn im März 2026. Es trägt kein Datum, daher fordern wir die Genehmigung und den aktuellen Baustand an.',
  'В информационном листе сказано, что разрешение на строительство выдано, а работы начались в марте 2026 года. Лист не датирован, поэтому мы запрашиваем само разрешение и актуальную стадию работ.',
  'تذكر النشرة التعريفية أن رخصة البناء ممنوحة وأن الأعمال بدأت في مارس 2026. وهي غير مؤرخة، لذلك نطلب الرخصة ومرحلة الأعمال كما هي الآن.',
  'Het infoblad vermeldt de bouwvergunning als verleend en de start van de werken in maart 2026. Het is niet gedateerd, dus we vragen de vergunning en de huidige stand van de werken op.',
  'Karta informacyjna podaje pozwolenie na budowę jako udzielone, a rozpoczęcie prac w marcu 2026 r. Nie ma daty, dlatego prosimy o samo pozwolenie i aktualny stan prac.',
  'Infoarket oppgir byggetillatelsen som innvilget og at arbeidene startet i mars 2026. Det er udatert, så vi ber om tillatelsen og om byggestatusen slik den er nå.',
  'Infobladet anger bygglovet som beviljat och att arbetena påbörjades i mars 2026. Det är odaterat, så vi begär bygglovet och byggstatusen som den är nu.')
a('trustDossier.cards.1.1',
  'La hoja informativa da el fin de obra en el {Q3} 2028 y la entrega en el {Q4} 2028. Pedimos la fecha de entrega contractual y la ponemos por escrito.',
  'La fiche d’information donne la fin des travaux au {Q3} 2028 et la livraison au {Q4} 2028. Nous demandons la date de livraison contractuelle et la mettons par écrit.',
  'Das Infoblatt nennt das Bauende im {Q3} 2028 und die Übergabe im {Q4} 2028. Wir fragen den vertraglichen Übergabetermin an und halten ihn schriftlich fest.',
  'В информационном листе окончание строительства указано на {Q3} 2028 года, сдача — на {Q4} 2028 года. Мы запрашиваем договорную дату сдачи и фиксируем её письменно.',
  'تذكر النشرة التعريفية نهاية البناء في {Q3} 2028 والتسليم في {Q4} 2028. نطلب موعد التسليم التعاقدي ونوثّقه كتابةً.',
  'Het infoblad geeft het einde van de bouw in {Q3} 2028 en de oplevering in {Q4} 2028. We vragen de contractuele opleveringsdatum op en leggen die schriftelijk vast.',
  'Karta informacyjna podaje zakończenie budowy w {Q3} 2028 i odbiór w {Q4} 2028. Prosimy o umowny termin odbioru i potwierdzamy go na piśmie.',
  'Infoarket oppgir byggeslutt i {Q3} 2028 og overlevering i {Q4} 2028. Vi ber om den kontraktfestede leveringsdatoen og setter den skriftlig.',
  'Infobladet anger byggslut i {Q3} 2028 och tillträde i {Q4} 2028. Vi begär det avtalade tillträdesdatumet och sätter det skriftligen.')
a('trustDossier.cards.2.1',
  'La hoja informativa y el folleto hablan de diez viviendas, de tres o cuatro dormitorios. La lista de disponibilidad muestra cinco, todas de cuatro dormitorios, y ninguno de los documentos dice qué ha sido de las otras cinco.',
  'La fiche d’information et la brochure parlent de dix logements, de trois ou quatre chambres. La liste de disponibilité en montre cinq, toutes de quatre chambres, et aucun des documents ne dit ce qu’il en est des cinq autres.',
  'Das Infoblatt und die Broschüre sprechen von zehn Wohnungen mit drei oder vier Schlafzimmern. Die Verfügbarkeitsliste zeigt fünf, alle mit vier Schlafzimmern, und keines der Dokumente sagt, was aus den übrigen fünf geworden ist.',
  'В информационном листе и в брошюре говорится о десяти квартирах с тремя или четырьмя спальнями. В списке наличия — пять, все с четырьмя спальнями, и ни в одном документе не сказано, что с остальными пятью.',
  'تتحدث النشرة التعريفية والكتيّب عن عشرة مساكن بثلاث أو أربع غرف نوم. وتُظهر قائمة التوفر خمسة، جميعها بأربع غرف نوم، ولا تذكر أي من الوثائق ما آل إليه حال الخمسة الأخرى.',
  'Het infoblad en de brochure spreken van tien woningen met drie of vier slaapkamers. De beschikbaarheidslijst toont er vijf, allemaal met vier slaapkamers, en geen van de documenten zegt wat er met de andere vijf is.',
  'Karta informacyjna i broszura mówią o dziesięciu lokalach z trzema lub czterema sypialniami. Lista dostępności pokazuje pięć, wszystkie z czterema sypialniami, a żaden z dokumentów nie mówi, co z pozostałymi pięcioma.',
  'Infoarket og brosjyren snakker om ti boliger med tre eller fire soverom. Tilgjengelighetslisten viser fem, alle med fire soverom, og ingen av dokumentene sier hva som har skjedd med de øvrige fem.',
  'Infobladet och broschyren talar om tio bostäder med tre eller fyra sovrum. Tillgänglighetslistan visar fem, alla med fyra sovrum, och inget av dokumenten säger vad som hänt med de övriga fem.')
a('trustDossier.cards.3.1',
  'La lista y los planos coinciden en la superficie construida del BY-02, BY-04, BY-06 y BY-08. Para el BY-07 la lista da {N285.64} {U} y la ficha de su plano da {N249.46} {U}. Las fichas del BY-02 y del BY-04 dan las mismas cifras para dos planos distintos, y el plano del BY-06 da terrazas de {N137.73} {U} en su tabla frente a {N191.37} {U} en su dibujo. Confirmamos qué cifras usa el contrato.',
  'La liste et les plans concordent sur la surface construite des BY-02, BY-04, BY-06 et BY-08. Pour le BY-07, la liste donne {N285.64} {U} et la fiche de son plan donne {N249.46} {U}. Les fiches des BY-02 et BY-04 donnent les mêmes chiffres pour deux plans différents, et le plan du BY-06 donne des terrasses de {N137.73} {U} dans son tableau contre {N191.37} {U} sur son dessin. Nous confirmons quels chiffres retient le contrat.',
  'Die Liste und die Pläne stimmen bei der bebauten Fläche von BY-02, BY-04, BY-06 und BY-08 überein. Für BY-07 nennt die Liste {N285.64} {U} und das Datenblatt seines Plans {N249.46} {U}. Die Datenblätter von BY-02 und BY-04 geben für zwei verschiedene Pläne dieselben Zahlen an, und der Plan von BY-06 nennt in seiner Tabelle Terrassen von {N137.73} {U} gegenüber {N191.37} {U} auf der Zeichnung. Wir bestätigen, welche Zahlen der Vertrag verwendet.',
  'Список и планы совпадают по площади застройки BY-02, BY-04, BY-06 и BY-08. Для BY-07 в списке указано {N285.64} {U}, а в листе его плана — {N249.46} {U}. В листах BY-02 и BY-04 для двух разных планировок указаны одни и те же цифры, а на плане BY-06 в таблице террасы составляют {N137.73} {U}, тогда как на чертеже — {N191.37} {U}. Мы подтверждаем, какие цифры использует договор.',
  'تتفق القائمة والمخططات على المساحة المبنية للمساكن BY-02 وBY-04 وBY-06 وBY-08. أما BY-07 فتعطي القائمة {N285.64} {U} وتعطي صفحة بيانات مخططه {N249.46} {U}. وتعطي صفحتا BY-02 وBY-04 الأرقام نفسها لمخططين مختلفين، ويعطي مخطط BY-06 تراسات بمساحة {N137.73} {U} في جدوله مقابل {N191.37} {U} في رسمه. ونؤكد الأرقام التي يعتمدها العقد.',
  'De lijst en de plattegronden komen overeen voor de bebouwde oppervlakte van BY-02, BY-04, BY-06 en BY-08. Voor BY-07 geeft de lijst {N285.64} {U} en het gegevensblad van de plattegrond {N249.46} {U}. De gegevensbladen van BY-02 en BY-04 geven dezelfde cijfers voor twee verschillende plattegronden, en de plattegrond van BY-06 geeft in zijn tabel terrassen van {N137.73} {U} tegenover {N191.37} {U} op de tekening. We bevestigen welke cijfers het contract hanteert.',
  'Lista i rzuty są zgodne co do powierzchni zabudowy BY-02, BY-04, BY-06 i BY-08. Dla BY-07 lista podaje {N285.64} {U}, a karta danych jego rzutu {N249.46} {U}. Karty danych BY-02 i BY-04 podają te same liczby dla dwóch różnych rzutów, a rzut BY-06 podaje w tabeli tarasy o powierzchni {N137.73} {U}, podczas gdy na rysunku {N191.37} {U}. Potwierdzamy, z jakich liczb korzysta umowa.',
  'Listen og planene stemmer overens om bebygd areal for BY-02, BY-04, BY-06 og BY-08. For BY-07 oppgir listen {N285.64} {U} og databladet til planen {N249.46} {U}. Databladene for BY-02 og BY-04 oppgir de samme tallene for to ulike planer, og planen for BY-06 oppgir terrasser på {N137.73} {U} i tabellen mot {N191.37} {U} på tegningen. Vi bekrefter hvilke tall kontrakten bruker.',
  'Listan och planritningarna stämmer överens om byggytan för BY-02, BY-04, BY-06 och BY-08. För BY-07 anger listan {N285.64} {U} och databladet till dess planritning {N249.46} {U}. Databladen för BY-02 och BY-04 anger samma siffror för två olika planritningar, och planritningen för BY-06 anger terrasser på {N137.73} {U} i tabellen mot {N191.37} {U} på ritningen. Vi bekräftar vilka siffror avtalet använder.')
a('trustDossier.cards.4.0', 'Los archivos de planos', 'Les fichiers de plans', 'Die Plandateien', 'Файлы планировок', 'ملفات المخططات', 'De plattegrondbestanden', 'Rzutowe pliki', 'Plantegningsfilene', 'Planritningsfilerna')
a('trustDossier.cards.4.1',
  'El BY-02 nos llegó en dos versiones: una con fecha del {T28.September.2026} que llama superficie útil a los {N288.94} {U}, y otra con fecha del {T19.October.2026} que los llama superficie construida, que es la que usa esta página. Los dibujos de la planta de servicios también difieren entre archivos: el spa mide {N195.95} {U} en los archivos del BY-02 y del BY-04 y {N201.71} {U} en los del BY-07 y del BY-08.',
  'Le BY-02 nous est parvenu en deux versions : l’une datée du {T28.September.2026} appelle surface utile les {N288.94} {U}, l’autre datée du {T19.October.2026} les appelle surface construite, et c’est celle que cette page retient. Les dessins du niveau des équipements diffèrent aussi d’un fichier à l’autre : le spa mesure {N195.95} {U} dans les fichiers des BY-02 et BY-04 et {N201.71} {U} dans ceux des BY-07 et BY-08.',
  'BY-02 liegt uns in zwei Fassungen vor: Die eine, datiert auf den {T28.September.2026}, nennt {N288.94} {U} die Nutzfläche, die andere, datiert auf den {T19.October.2026}, nennt sie bebaute Fläche; diese verwendet diese Seite. Auch die Zeichnungen der Ausstattungsebene weichen zwischen den Dateien ab: Das Spa misst {N195.95} {U} in den Dateien von BY-02 und BY-04 und {N201.71} {U} in denen von BY-07 und BY-08.',
  'Квартира BY-02 пришла к нам в двух версиях: в одной, от {T28.September.2026}, {N288.94} {U} названы полезной площадью, в другой, от {T19.October.2026}, — площадью застройки; эта страница использует вторую. Чертежи уровня удобств тоже различаются между файлами: спа занимает {N195.95} {U} в файлах BY-02 и BY-04 и {N201.71} {U} в файлах BY-07 и BY-08.',
  'وصلنا المسكن BY-02 بنسختين: إحداهما بتاريخ {T28.September.2026} تسمّي {N288.94} {U} المساحة الصافية، والأخرى بتاريخ {T19.October.2026} تسمّيها المساحة المبنية، وهي التي تعتمدها هذه الصفحة. كما تختلف رسوم طابق المرافق بين الملفات: فمساحة السبا {N195.95} {U} في ملفي BY-02 وBY-04 و{N201.71} {U} في ملفي BY-07 وBY-08.',
  'BY-02 bereikte ons in twee versies: de ene, gedateerd {T28.September.2026}, noemt {N288.94} {U} de gebruiksoppervlakte, de andere, gedateerd {T19.October.2026}, noemt het de bebouwde oppervlakte, en die gebruikt deze pagina. De tekeningen van de voorzieningenlaag verschillen ook tussen de bestanden: de spa meet {N195.95} {U} in de bestanden van BY-02 en BY-04 en {N201.71} {U} in die van BY-07 en BY-08.',
  'BY-02 dotarł do nas w dwóch wersjach: jedna, z datą {T28.September.2026}, nazywa {N288.94} {U} powierzchnią użytkową, a druga, z datą {T19.October.2026}, powierzchnią zabudowy i z niej korzysta ta strona. Rysunki poziomu udogodnień również różnią się między plikami: spa ma {N195.95} {U} w plikach BY-02 i BY-04 oraz {N201.71} {U} w plikach BY-07 i BY-08.',
  'BY-02 kom til oss i to versjoner: den ene, datert {T28.September.2026}, kaller {N288.94} {U} bruksareal, og den andre, datert {T19.October.2026}, kaller det bebygd areal, og det er den denne siden bruker. Tegningene av fasilitetsnivået avviker også mellom filene: spaet er {N195.95} {U} i filene for BY-02 og BY-04 og {N201.71} {U} i filene for BY-07 og BY-08.',
  'BY-02 kom till oss i två versioner: den ena, daterad {T28.September.2026}, kallar {N288.94} {U} boyta, och den andra, daterad {T19.October.2026}, kallar det byggyta, och det är den som den här sidan använder. Ritningarna av bekvämlighetsplanet skiljer sig också mellan filerna: spaet är {N195.95} {U} i filerna för BY-02 och BY-04 och {N201.71} {U} i filerna för BY-07 och BY-08.')
a('trustDossier.cards.5.1',
  'Los documentos no dan dirección postal, así que el marcador del mapa está en el centro de Estepona y no en la parcela. El folleto da sus tiempos de trayecto sin decir cómo se recorren, y los confirmamos en una visita.',
  'Les documents ne donnent pas d’adresse postale : le repère de la carte se trouve donc au centre d’Estepona et non sur la parcelle. La brochure donne ses temps de trajet sans dire comment on les parcourt, et nous les confirmons lors d’une visite.',
  'Die Unterlagen nennen keine Straßenadresse, daher liegt die Markierung auf der Karte im Zentrum von Estepona und nicht auf dem Grundstück. Die Broschüre nennt ihre Fahrzeiten, ohne zu sagen, womit man sie zurücklegt, und wir bestätigen sie bei einem Besuch.',
  'В документах нет почтового адреса, поэтому маркер на карте стоит в центре Эстепоны, а не на участке. В брошюре время в пути указано без уточнения, как его преодолевают, и мы подтверждаем его во время визита.',
  'لا تعطي الوثائق عنوانًا بريديًا، لذلك فإن العلامة على الخريطة في وسط إستيبونا وليست على القطعة. ويذكر الكتيّب أوقات التنقل دون أن يوضح وسيلة التنقل، ونؤكدها خلال الزيارة.',
  'De documenten geven geen postadres, dus de markering op de kaart staat in het centrum van Estepona en niet op het perceel. De brochure geeft haar reistijden zonder te zeggen hoe die worden afgelegd, en we bevestigen ze bij een bezoek.',
  'Dokumenty nie podają adresu, więc znacznik na mapie stoi w centrum Estepony, a nie na działce. Broszura podaje czasy dojazdu bez informacji, jak się je pokonuje, a my potwierdzamy je podczas wizyty.',
  'Dokumentene oppgir ingen postadresse, så markøren på kartet står i sentrum av Estepona og ikke på tomten. Brosjyren oppgir reisetidene uten å si hvordan de tilbakelegges, og vi bekrefter dem ved et besøk.',
  'Dokumenten anger ingen postadress, så markören på kartan står i centrala Estepona och inte på tomten. Broschyren anger restiderna utan att säga hur de färdas, och vi bekräftar dem vid ett besök.')

# ---- availability, timeline, enquiry, FAQ, SEO ------------------------------------------------------

a('availability.copy',
  'Cinco apartamentos figuran con precio, todos de cuatro dormitorios. La disponibilidad y los precios son los de la lista del {T29.October.2026} y no incluyen el IVA, y los confirmamos antes de cualquier reserva.',
  'Cinq appartements sont listés avec un prix, tous de quatre chambres. La disponibilité et les prix sont ceux de la liste du {T29.October.2026} et s’entendent hors TVA, et nous les confirmons avant toute réservation.',
  'Fünf Wohnungen sind mit Preis aufgeführt, alle mit vier Schlafzimmern. Verfügbarkeit und Preise entsprechen der Liste vom {T29.October.2026} und verstehen sich zuzüglich MwSt.; wir bestätigen sie vor jeder Reservierung.',
  'Пять апартаментов указаны с ценой, все с четырьмя спальнями. Наличие и цены даны по списку от {T29.October.2026} и не включают НДС; перед любым бронированием мы их подтверждаем.',
  'خمس شقق مدرجة بسعر، وجميعها بأربع غرف نوم. التوفر والأسعار هي المذكورة في قائمة {T29.October.2026} ولا تشمل ضريبة القيمة المضافة، ونؤكدها قبل أي حجز.',
  'Vijf appartementen staan met een prijs op de lijst, allemaal met vier slaapkamers. Beschikbaarheid en prijzen zijn die van de lijst van {T29.October.2026} en zijn exclusief btw, en we bevestigen ze vóór elke reservering.',
  'Pięć apartamentów ma podaną cenę, wszystkie z czterema sypialniami. Dostępność i ceny pochodzą z listy z {T29.October.2026} i nie zawierają VAT, a przed każdą rezerwacją je potwierdzamy.',
  'Fem leiligheter er oppført med pris, alle med fire soverom. Tilgjengelighet og priser er de på listen fra {T29.October.2026} og er eksklusive mva., og vi bekrefter dem før enhver reservasjon.',
  'Fem lägenheter är listade med pris, alla med fyra sovrum. Tillgänglighet och priser är de på listan från {T29.October.2026} och är exklusive IVA, och vi bekräftar dem före varje reservation.')
a('availability.priceRange', '{E6500000} - {E9000000} + IVA', '{E6500000} - {E9000000} + TVA', '{E6500000} - {E9000000} + MwSt.', '{E6500000} - {E9000000} + НДС',
  '{E6500000} - {E9000000} + ضريبة القيمة المضافة', '{E6500000} - {E9000000} + btw', '{E6500000} - {E9000000} + VAT', '{E6500000} - {E9000000} + mva.', '{E6500000} - {E9000000} + IVA')
a('availability.sourceNote',
  'Los precios, dormitorios y superficies construidas están transcritos de la lista de disponibilidad del promotor a fecha {T29.October.2026}, que muestra cinco viviendas. La lista da la cifra neta del promotor y la hoja informativa añade el IVA a cada pago, por lo que los precios no incluyen el IVA. Las terrazas, los trasteros y los tamaños de las estancias proceden de los planos del promotor, que en algunos puntos difieren de la lista; en las secciones anteriores se dan ambas cifras.',
  'Les prix, les chambres et les surfaces construites sont transcrits de la liste de disponibilité du promoteur à la date du {T29.October.2026}, qui montre cinq logements. La liste donne le montant net du promoteur et la fiche d’information ajoute la TVA à chaque versement : les prix s’entendent donc hors TVA. Les terrasses, les caves et la taille des pièces proviennent des plans du promoteur, qui diffèrent par endroits de la liste ; les deux chiffres sont donnés dans les sections ci-dessus.',
  'Preise, Schlafzimmer und bebaute Flächen sind der Verfügbarkeitsliste des Bauträgers mit Stand {T29.October.2026} entnommen, die fünf Wohnungen zeigt. Die Liste nennt den Nettobetrag des Bauträgers, und das Infoblatt rechnet bei jeder Rate die MwSt. hinzu, die Preise verstehen sich daher zuzüglich MwSt. Terrassen, Abstellräume und Raumgrößen stammen aus den Plänen des Bauträgers, die stellenweise von der Liste abweichen; in den Abschnitten oben sind beide Angaben genannt.',
  'Цены, спальни и площади застройки перенесены из списка наличия застройщика по состоянию на {T29.October.2026}, в котором пять квартир. В списке указана чистая цена застройщика, а в информационном листе к каждому платежу добавляется НДС, поэтому цены не включают НДС. Террасы, кладовые и размеры помещений взяты из планов застройщика, которые местами отличаются от списка; в разделах выше приведены обе цифры.',
  'نُقلت الأسعار وغرف النوم والمساحات المبنية من قائمة التوفر لدى المطوّر بتاريخ {T29.October.2026}، وهي تُظهر خمسة مساكن. تعطي القائمة المبلغ الصافي للمطوّر وتضيف النشرة التعريفية ضريبة القيمة المضافة إلى كل دفعة، لذلك فالأسعار لا تشمل الضريبة. أما التراسات وغرف التخزين وأحجام الغرف فمصدرها مخططات المطوّر التي تختلف عن القائمة في بعض المواضع؛ وتُذكر الأرقام كلها في الأقسام أعلاه.',
  'De prijzen, slaapkamers en bebouwde oppervlakten zijn overgenomen uit de beschikbaarheidslijst van de ontwikkelaar per {T29.October.2026}, die vijf woningen toont. De lijst geeft het nettobedrag van de ontwikkelaar en het infoblad voegt btw toe aan elke termijn, dus de prijzen zijn exclusief btw. De terrassen, bergingen en kamermaten komen uit de plattegronden van de ontwikkelaar, die op punten van de lijst afwijken; beide cijfers staan in de secties hierboven.',
  'Ceny, sypialnie i powierzchnie zabudowy zostały przepisane z listy dostępności dewelopera na dzień {T29.October.2026}, która pokazuje pięć lokali. Lista podaje kwotę netto dewelopera, a karta informacyjna dolicza VAT do każdej raty, więc ceny nie zawierają VAT. Tarasy, komórki lokatorskie i wymiary pomieszczeń pochodzą z rzutów dewelopera, które miejscami różnią się od listy; obie liczby podano w sekcjach powyżej.',
  'Prisene, soverommene og bebygde arealene er hentet fra utbyggerens tilgjengelighetsliste per {T29.October.2026}, som viser fem boliger. Listen oppgir utbyggerens nettobeløp, og infoarket legger mva. til hver innbetaling, så prisene er eksklusive mva. Terrassene, bodene og romstørrelsene kommer fra utbyggerens planer, som enkelte steder avviker fra listen; begge tallene er oppgitt i seksjonene ovenfor.',
  'Priser, sovrum och byggytor är hämtade från exploatörens tillgänglighetslista per {T29.October.2026}, som visar fem bostäder. Listan anger exploatörens nettobelopp, och infobladet lägger IVA (spansk moms) på varje betalning, så priserna är exklusive IVA. Terrasserna, förråden och rumsstorlekarna kommer från exploatörens planritningar, som på några ställen avviker från listan; båda siffrorna anges i avsnitten ovan.')
a('timeline.items.0.2',
  'Los planos de las viviendas que le interesan y la lista de precios actual.', 'Les plans des logements qui vous intéressent et la liste de prix actuelle.',
  'Die Pläne der Wohnungen, die Sie interessieren, und die aktuelle Preisliste.', 'Планировки интересующих вас квартир и актуальный прайс-лист.',
  'مخططات المساكن التي تهمكم وقائمة الأسعار الحالية.', 'De plattegronden van de woningen die u interesseren en de actuele prijslijst.',
  'Rzuty interesujących Państwa lokali i aktualny cennik.', 'Planene for boligene som er av interesse og gjeldende prisliste.',
  'Planritningarna för de bostäder som intresserar er och den aktuella prislistan.')
a('enquiry.headlineHtml', 'Pregunte por <em>Biubay</em>', 'Renseignez-vous sur <em>Biubay</em>', 'Fragen Sie nach <em>Biubay</em>', 'Узнайте о <em>Biubay</em>',
  'اسأل عن <em>Biubay</em>', 'Vraag naar <em>Biubay</em>', 'Zapytaj o <em>Biubay</em>', 'Spør om <em>Biubay</em>', 'Fråga om <em>Biubay</em>')
a('enquiry.message',
  'Hola Nueva Living, me gustaría recibir información sobre Biubay.', 'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Biubay.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Biubay.', 'Здравствуйте, Nueva Living! Я хотел бы получить информацию о Biubay.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Biubay.', 'Hallo Nueva Living, ik zou graag informatie ontvangen over Biubay.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Biubay.', 'Hei Nueva Living, jeg vil gjerne ha informasjon om Biubay.',
  'Hej Nueva Living, jag skulle vilja ha information om Biubay.')
a('faq.0.1',
  'Diez, según la hoja informativa y el folleto, de tres o cuatro dormitorios. Cinco figuran con precio, todas de cuatro dormitorios, de {E6500000} a {E9000000} más IVA.',
  'Dix, selon la fiche d’information et la brochure, de trois ou quatre chambres. Cinq sont listés avec un prix, tous de quatre chambres, de {E6500000} à {E9000000} hors TVA.',
  'Zehn laut Infoblatt und Broschüre, mit drei oder vier Schlafzimmern. Fünf sind mit Preis aufgeführt, alle mit vier Schlafzimmern, von {E6500000} bis {E9000000} zuzüglich MwSt.',
  'Десять, согласно информационному листу и брошюре, с тремя или четырьмя спальнями. Пять указаны с ценой, все с четырьмя спальнями, — от {E6500000} до {E9000000} без НДС.',
  'عشرة، بحسب النشرة التعريفية والكتيّب، بثلاث أو أربع غرف نوم. وخمسة منها مدرجة بسعر، جميعها بأربع غرف نوم، من {E6500000} إلى {E9000000} دون ضريبة القيمة المضافة.',
  'Tien, volgens het infoblad en de brochure, met drie of vier slaapkamers. Vijf staan met een prijs op de lijst, allemaal met vier slaapkamers, van {E6500000} tot {E9000000} excl. btw.',
  'Dziesięć, według karty informacyjnej i broszury, z trzema lub czterema sypialniami. Pięć ma podaną cenę, wszystkie z czterema sypialniami, od {E6500000} do {E9000000} plus VAT.',
  'Ti, ifølge infoarket og brosjyren, med tre eller fire soverom. Fem er oppført med pris, alle med fire soverom, fra {E6500000} til {E9000000} pluss mva.',
  'Tio, enligt infobladet och broschyren, med tre eller fyra sovrum. Fem är listade med pris, alla med fyra sovrum, från {E6500000} till {E9000000} plus IVA.')
a('faq.1.1',
  'No. La lista da la cifra neta del promotor y la hoja informativa añade el IVA a cada pago, así que los precios son más IVA. Confirmamos por escrito el tipo y los gastos de compra.',
  'Non. La liste donne le montant net du promoteur et la fiche d’information ajoute la TVA à chaque versement : les prix s’entendent donc hors TVA. Nous confirmons par écrit le taux et les frais d’achat.',
  'Nein. Die Liste nennt den Nettobetrag des Bauträgers, und das Infoblatt rechnet bei jeder Rate die MwSt. hinzu, die Preise verstehen sich also zuzüglich MwSt. Wir bestätigen den Satz und die Kaufnebenkosten schriftlich.',
  'Нет. В списке указана чистая цена застройщика, а в информационном листе к каждому платежу добавляется НДС, поэтому цены даны без НДС. Ставку и расходы на покупку мы подтверждаем письменно.',
  'لا. تعطي القائمة المبلغ الصافي للمطوّر وتضيف النشرة التعريفية ضريبة القيمة المضافة إلى كل دفعة، فالأسعار دون الضريبة. ونؤكد النسبة وتكاليف الشراء كتابةً.',
  'Nee. De lijst geeft het nettobedrag van de ontwikkelaar en het infoblad voegt btw toe aan elke termijn, dus de prijzen zijn exclusief btw. We bevestigen het tarief en de aankoopkosten schriftelijk.',
  'Nie. Lista podaje kwotę netto dewelopera, a karta informacyjna dolicza VAT do każdej raty, więc ceny nie zawierają VAT. Stawkę i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Listen oppgir utbyggerens nettobeløp, og infoarket legger mva. til hver innbetaling, så prisene er eksklusive mva. Vi bekrefter satsen og kjøpskostnadene skriftlig.',
  'Nej. Listan anger exploatörens nettobelopp, och infobladet lägger IVA på varje betalning, så priserna är exklusive IVA. Vi bekräftar skattesatsen och köpkostnaderna skriftligen.')
a('faq.2.1',
  'Las fichas técnicas dan tres plazas de aparcamiento para cuatro de las cinco viviendas, y los planos muestran un trastero de {N28.07} a {N82.11} {U}. Confirmamos qué incluye la vivienda que usted elija.',
  'Les fiches techniques donnent trois places de stationnement pour quatre des cinq logements, et les plans montrent une cave de {N28.07} à {N82.11} {U}. Nous confirmons ce que comprend le logement que vous choisissez.',
  'Die Datenblätter nennen drei Stellplätze für vier der fünf Wohnungen, und die Pläne zeigen einen Abstellraum von {N28.07} bis {N82.11} {U}. Wir bestätigen, was die Wohnung, die Sie wählen, umfasst.',
  'В листах с характеристиками для четырёх из пяти квартир указаны три парковочных места, а на планах показана кладовая от {N28.07} до {N82.11} {U}. Мы подтверждаем, что входит в выбранную вами квартиру.',
  'تذكر صفحات البيانات ثلاثة مواقف سيارات لأربعة من المساكن الخمسة، وتُظهر المخططات غرفة تخزين من {N28.07} إلى {N82.11} {U}. ونؤكد ما يشمله المسكن الذي تختارونه.',
  'De gegevensbladen geven drie parkeerplaatsen voor vier van de vijf woningen, en de plattegronden tonen een berging van {N28.07} tot {N82.11} {U}. We bevestigen wat de woning die u kiest omvat.',
  'Karty danych podają trzy miejsca parkingowe dla czterech z pięciu lokali, a rzuty pokazują komórkę lokatorską o powierzchni od {N28.07} do {N82.11} {U}. Potwierdzamy, co obejmuje lokal wybrany przez Państwa.',
  'Databladene oppgir tre parkeringsplasser for fire av de fem boligene, og planene viser en bod på {N28.07} til {N82.11} {U}. Vi bekrefter hva boligen som velges omfatter.',
  'Databladen anger tre parkeringsplatser för fyra av de fem bostäderna, och planritningarna visar ett förråd på {N28.07} till {N82.11} {U}. Vi bekräftar vad den bostad ni väljer omfattar.')
a('faq.3.1',
  'El folleto dice que todas las viviendas están orientadas al sur y describe amplias terrazas con vistas al mar, pero no describe la vista de cada vivienda, así que la confirmamos para la vivienda que usted elija.',
  'La brochure indique que tous les logements sont orientés au sud et décrit de grandes terrasses face à la mer, mais ne décrit pas la vue de chaque logement ; nous la confirmons donc pour le logement que vous choisissez.',
  'Die Broschüre sagt, dass alle Wohnungen nach Süden ausgerichtet sind, und beschreibt große Terrassen mit Meerblick, nennt aber nicht die Aussicht jeder einzelnen Wohnung, daher bestätigen wir sie für die Wohnung, die Sie wählen.',
  'В брошюре сказано, что все квартиры ориентированы на юг, и описаны большие террасы с видом на море, но вид из каждой квартиры не описан, поэтому для выбранной вами квартиры мы его подтверждаем.',
  'يذكر الكتيّب أن جميع المساكن تواجه الجنوب ويصف تراسات واسعة مطلة على البحر، لكنه لا يصف الإطلالة من كل مسكن، لذلك نؤكد الإطلالة للمسكن الذي تختارونه.',
  'De brochure zegt dat alle woningen op het zuiden liggen en beschrijft grote terrassen met zeezicht, maar beschrijft niet het uitzicht vanuit elke woning, dus we bevestigen het voor de woning die u kiest.',
  'Broszura podaje, że wszystkie lokale są zwrócone na południe, i opisuje duże tarasy z widokiem na morze, ale nie opisuje widoku z każdego lokalu, dlatego potwierdzamy go dla lokalu wybranego przez Państwa.',
  'Brosjyren sier at alle boligene vender mot sør og beskriver store terrasser mot havet, men beskriver ikke utsikten fra hver bolig, så vi bekrefter den for boligen som velges.',
  'Broschyren säger att alla bostäder vetter mot söder och beskriver stora terrasser mot havet, men beskriver inte utsikten från varje bostad, så vi bekräftar den för den bostad ni väljer.')
a('faq.4.1',
  'El mobiliario y la decoración de las imágenes generadas por ordenador son ilustrativos. Los documentos que tenemos no indican el mobiliario como incluido, así que confirmamos qué está incluido.',
  'Le mobilier et la décoration des images de synthèse sont illustratifs. Les documents dont nous disposons n’indiquent pas le mobilier comme inclus, nous confirmons donc ce qui est inclus.',
  'Die Möbel und die Dekoration in den computergenerierten Bildern dienen der Veranschaulichung. Die uns vorliegenden Unterlagen führen Möbel nicht als enthalten auf, daher bestätigen wir, was enthalten ist.',
  'Мебель и декор на компьютерных изображениях носят иллюстративный характер. В имеющихся у нас документах мебель не указана как входящая в стоимость, поэтому мы подтверждаем, что именно включено.',
  'الأثاث والديكور في الصور المُولَّدة بالحاسوب توضيحيان. ولا تذكر الوثائق التي بحوزتنا الأثاث ضمن المشمولات، لذلك نؤكد ما هو مشمول.',
  'Het meubilair en de inrichting op de computergegenereerde beelden zijn illustratief. De documenten waarover we beschikken vermelden meubilair niet als inbegrepen, dus we bevestigen wat is inbegrepen.',
  'Meble i wystrój na obrazach komputerowych mają charakter poglądowy. Dokumenty, którymi dysponujemy, nie wymieniają mebli jako wliczonych w cenę, więc potwierdzamy, co jest wliczone.',
  'Møblene og innredningen på de datagenererte bildene er illustrative. Dokumentene vi har oppgir ikke møbler som inkludert, så vi bekrefter hva som er inkludert.',
  'Möblerna och inredningen på de datorgenererade bilderna är illustrativa. Dokumenten vi har anger inte möbler som inkluderade, så vi bekräftar vad som ingår.')
a('faq.5.1',
  'La hoja informativa da la entrega en el {Q4} 2028, con las obras empezando en marzo de 2026 y terminando en el {Q3} 2028. No lleva fecha, así que pedimos la fecha contractual y la ponemos por escrito.',
  'La fiche d’information donne la livraison au {Q4} 2028, avec des travaux commençant en mars 2026 et se terminant au {Q3} 2028. Elle n’est pas datée, nous demandons donc la date contractuelle et la mettons par écrit.',
  'Das Infoblatt nennt die Übergabe im {Q4} 2028, mit Baubeginn im März 2026 und Bauende im {Q3} 2028. Es trägt kein Datum, daher fragen wir den vertraglichen Termin an und halten ihn schriftlich fest.',
  'В информационном листе сдача указана на {Q4} 2028 года, начало работ — март 2026 года, окончание — {Q3} 2028 года. Лист не датирован, поэтому мы запрашиваем договорную дату и фиксируем её письменно.',
  'تذكر النشرة التعريفية التسليم في {Q4} 2028، مع بدء الأعمال في مارس 2026 وانتهائها في {Q3} 2028. وهي غير مؤرخة، لذلك نطلب الموعد التعاقدي ونوثّقه كتابةً.',
  'Het infoblad geeft de oplevering in {Q4} 2028, met de start van de werken in maart 2026 en het einde in {Q3} 2028. Het is niet gedateerd, dus we vragen de contractuele datum op en leggen die schriftelijk vast.',
  'Karta informacyjna podaje odbiór w {Q4} 2028, z rozpoczęciem prac w marcu 2026 r. i zakończeniem w {Q3} 2028. Nie ma daty, dlatego prosimy o termin umowny i potwierdzamy go na piśmie.',
  'Infoarket oppgir overlevering i {Q4} 2028, med arbeidene som starter i mars 2026 og avsluttes i {Q3} 2028. Det er udatert, så vi ber om den kontraktfestede datoen og setter den skriftlig.',
  'Infobladet anger tillträde i {Q4} 2028, med arbeten som påbörjas i mars 2026 och avslutas i {Q3} 2028. Det är odaterat, så vi begär det avtalade datumet och sätter det skriftligen.')
a('faq.6.1',
  'El promotor fija un importe de reserva y un calendario de pagos escalonado. Le enviamos las condiciones vigentes por escrito antes de cualquier reserva.',
  'Le promoteur fixe un montant de réservation et un échéancier de paiement échelonné. Nous vous envoyons les conditions en vigueur par écrit avant toute réservation.',
  'Der Bauträger legt einen Reservierungsbetrag und einen gestaffelten Zahlungsplan fest. Wir senden Ihnen die geltenden Bedingungen vor jeder Reservierung schriftlich zu.',
  'Застройщик устанавливает сумму бронирования и поэтапный график платежей. Действующие условия мы присылаем вам письменно перед любым бронированием.',
  'يحدد المطوّر مبلغ الحجز وجدول دفعات مرحليًا. ونرسل إليكم الشروط السارية كتابةً قبل أي حجز.',
  'De ontwikkelaar stelt een reserveringsbedrag en een gefaseerd betalingsschema vast. We sturen u de geldende voorwaarden vóór elke reservering schriftelijk toe.',
  'Deweloper ustala kwotę rezerwacji i etapowy harmonogram płatności. Obowiązujące warunki przesyłamy Państwu na piśmie przed każdą rezerwacją.',
  'Utbyggeren fastsetter et reservasjonsbeløp og en trinnvis betalingsplan. Vi sender gjeldende vilkår skriftlig før enhver reservasjon.',
  'Exploatören fastställer ett reservationsbelopp och en stegvis betalningsplan. Vi skickar gällande villkor skriftligen före varje reservation.')
a('seo.title', 'Biubay - Apartamentos frente al mar en Estepona', 'Biubay - Appartements en bord de mer à Estepona', 'Biubay - Wohnungen direkt am Meer in Estepona',
  'Biubay - апартаменты на берегу моря в Эстепоне', 'Biubay - شقق على الواجهة البحرية في إستيبونا', 'Biubay - Appartementen aan zee in Estepona',
  'Biubay - Apartamenty przy morzu w Esteponie', 'Biubay - Leiligheter ved sjøen i Estepona', 'Biubay - Lägenheter vid havet i Estepona')
a('seo.h1', 'Biubay: apartamentos de cuatro dormitorios frente al mar en Estepona', 'Biubay : appartements de quatre chambres en bord de mer à Estepona',
  'Biubay: Wohnungen mit vier Schlafzimmern direkt am Meer in Estepona', 'Biubay: квартиры с четырьмя спальнями на берегу моря в Эстепоне',
  'Biubay: شقق بأربع غرف نوم على الواجهة البحرية في إستيبونا', 'Biubay: appartementen met vier slaapkamers aan zee in Estepona',
  'Biubay: apartamenty z czterema sypialniami przy morzu w Esteponie', 'Biubay: leiligheter med fire soverom ved sjøen i Estepona',
  'Biubay: lägenheter med fyra sovrum vid havet i Estepona')
a('seo.h1Context', 'Apartamentos de cuatro dormitorios frente al mar en Estepona', 'Appartements de quatre chambres en bord de mer à Estepona',
  'Wohnungen mit vier Schlafzimmern direkt am Meer in Estepona', 'Квартиры с четырьмя спальнями на берегу моря в Эстепоне',
  'شقق بأربع غرف نوم على الواجهة البحرية في إستيبونا', 'Appartementen met vier slaapkamers aan zee in Estepona',
  'Apartamenty z czterema sypialniami przy morzu w Esteponie', 'Leiligheter med fire soverom ved sjøen i Estepona',
  'Lägenheter med fyra sovrum vid havet i Estepona')

# ---- templates: unit sizes, plan alt and captions --------------------------------------------------
# Labels are read from Granado Homes, the sibling that already carries built / interior / covered /
# uncovered terrace in all nine languages, so the wording matches and the one-word-per-label check holds.
g = json.load(open('content/liora-projects/granado-homes/project.json'))
g_en = g['availability']['units'][0]['size']
assert g_en.count('sqm') == 4 and 'covered terrace' in g_en and 'uncovered terrace' in g_en
LABEL = {}
for l in LOCS:
    segs = re.split(r'،\s|,\s', g['i18n'][l]['availability']['units'][0]['size'])
    assert len(segs) == 4, (l, segs)
    # built, interior, covered, uncovered. The number is replaced wherever it stands: Russian puts the
    # noun first ("крытая терраса 16,18 м²") and the others put it first.
    LABEL[l] = [re.sub(r'\d[\d.,]*\d|\d', '{n}', s, count=1).strip() for s in segs]
FIELD = {'built': 0, 'interior': 1, 'covered terrace': 2, 'uncovered terrace': 3}


def seg(l, kind, n):
    tpl = LABEL[l][FIELD[kind]]
    # the template keeps the area unit of Granado's text: "{n} м² ..." or "... {n} м²"
    return tpl.replace('{n}', num(n, l))


for u in P['availability']['units']:
    if u['size'] in T:
        continue
    parts = [s for s in u['size'].split(', ')]
    out = {}
    for l in LOCS:
        row = []
        for p in parts:
            m = re.fullmatch(r'([\d.]+) sqm (built|interior|covered terrace|uncovered terrace)', p)
            assert m, p
            row.append(seg(l, m.group(2), m.group(1)))
        out[l] = ('، ' if l == 'ar' else ', ').join(row)
    T[u['size']] = out

HOME = {'es': 'Vivienda', 'fr': 'Logement', 'de': 'Wohnung', 'ru': 'Квартира', 'ar': 'المسكن', 'nl': 'Woning', 'pl': 'Lokal', 'no': 'Bolig', 'sv': 'Bostad'}
PLAN = {'es': 'Plano de la vivienda', 'fr': 'Plan du logement', 'de': 'Grundriss der Wohnung', 'ru': 'Планировка квартиры', 'ar': 'مخطط المسكن',
        'nl': 'Plattegrond van woning', 'pl': 'Rzut lokalu', 'no': 'Plantegning av bolig', 'sv': 'Planritning för bostad'}
for it in P['media']['items']:
    if it.get('category') != 'Floorplans':
        continue
    ref = it['caption'].split()[-1]
    T[it['caption']] = {l: f'{HOME[l]} {ref}' for l in LOCS}
    T[it['alt']] = {l: f'{PLAN[l]} {ref}' for l in LOCS}
for u in P['availability']['units']:
    if u['reference'] not in T:
        same(u['reference'])


# ---- the rest: take the wording of the newest sibling projects, not the translation memory's majority --------
# The memory returns the most common translation per string, and for "How many homes are there?" or
# "What we check before you commit" that is an older villa project's wording ("Häuser", "antes de que le
# comprometa", a "du" in Norwegian). The four projects published on 28 October 2026 carry the settled forms.
NEWEST = ['las-mesas-blue-horizon', 'the-privilege', 'paraiso-de-azahar', 'the-oak48', 'zenith-estepona']
LATEST = {}
for slug in NEWEST:
    d = json.load(open(f'content/liora-projects/{slug}/project.json'))

    def pair(e, ovs):
        if isinstance(e, str):
            if e.strip() and all(isinstance(ovs.get(l), str) for l in LOCS):
                LATEST.setdefault(e, {l: ovs[l] for l in LOCS})
        elif isinstance(e, dict):
            for k, v in e.items():
                if all(isinstance(ovs.get(l), dict) and k in ovs[l] for l in LOCS):
                    pair(v, {l: ovs[l][k] for l in LOCS})
        elif isinstance(e, list):
            for i, v in enumerate(e):
                if all(isinstance(ovs.get(l), list) and len(ovs[l]) > i for l in LOCS):
                    pair(v, {l: ovs[l][i] for l in LOCS})
    pair(d, d['i18n'])


def english(node, out):
    if isinstance(node, str):
        out.add(node)
    elif isinstance(node, dict):
        for k, v in node.items():
            if k not in ('i18n', 'src', 'floorplan', 'href', 'category', 'slug', 'canonical', 'output', 'schema', 'crm', 'contact', 'discovery'):
                english(v, out)
    elif isinstance(node, list):
        for v in node:
            english(v, out)


ALL = set(); english(P, ALL)
taken = 0
for s in sorted(ALL):
    if s in T or s not in LATEST or re.fullmatch(r'[\d .,%-]+', s):
        continue
    T[s] = LATEST[s]; taken += 1
print('taken from the newest siblings:', taken)

# Where the inherited wording is wrong for this page, say so here, one locale at a time: a villa project's
# "How many homes" is "Häuser" and "maisons" and "domów", Norwegian has a "du" the house style avoids
# (De/dere neutral, so the sentence is made impersonal), and one Spanish line says "la promotora".
OVR = {
 'faq.0.0': {'fr': 'Combien y a-t-il de logements ?', 'de': 'Wie viele Wohnungen gibt es?', 'ru': 'Сколько квартир в комплексе?', 'ar': 'كم عدد المساكن؟', 'pl': 'Ile jest lokali?'},
 'faq.3.0': {'ar': 'هل لجميع المساكن إطلالة على البحر؟'},
 'trustDossier.headlineHtml': {'es': 'Lo que comprobamos <em>antes de comprometerse</em>', 'ar': 'ما نتحقق منه <em>قبل أن تلتزموا</em>', 'no': 'Hva vi sjekker <em>før noe forpliktes</em>'},
 'trustDossier.copy': {'es': 'Confirmamos con el promotor el estado actual de cada punto antes de cualquier reserva, y ponemos las respuestas por escrito.',
                       'fr': 'Nous confirmons l’état actuel de chaque point auprès du promoteur avant toute réservation, et nous mettons les réponses par écrit.'},
 'investment.headlineHtml': {'fr': 'Ce qu’il faut <em>évaluer</em>', 'no': 'Hva som bør <em>vurderes</em>', 'ar': 'ما الذي ينبغي <em>الموازنة بينه</em>'},
 'why.points.0.0': {'fr': 'À qui s’adresse ce projet'},
 'why.points.2.0': {'fr': 'Pourquoi l’emplacement compte'},
 'enquiry.copy': {'no': 'Fortell oss hva som trengs, så kommer vi tilbake med gjeldende tilgjengelighet, plantegningene og prislisten.'},
 'enquiry.sentMessage': {'no': 'Takk. Vi kommer snart tilbake med prosjektdokumentasjonen.'},
}
for path, per in OVR.items():
    for l, text in per.items():
        T[en(path)][l] = expand(text, l)

json.dump(T, open(f'{SP}/tr_n.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
