# -*- coding: utf-8 -*-
"""Monteros Heights Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E575000}
money, {N88.4} decimal number, {U} the area unit.
    python3 tools/import/k_monteros_heights.py <scratch dir>      (writes <dir>/tr_a.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/monteros-heights-residences/project.json'))


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.,]+)\}', lambda m: num(m.group(1), l), text)
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


same('Monteros Heights Residences'); same('Monteros Heights'); same('Monteros Heights <em>Residences</em>')

# ---- unit sizes: "93.28 sqm built, 82.56 sqm interior, 42.19 sqm terrace[, 49.60 sqm solarium]" ----------
# One word per measurement per language, as the newest projects (haiku-estepona, aire-estepona) set them.
SIZE_WORDS = {
    'built': {'es': 'm² construidos', 'fr': 'm² construits', 'de': 'm² bebaut', 'ru': 'м² застроенной площади', 'ar': 'م² مبنية',
              'nl': 'm² bebouwd', 'pl': 'm² zabudowy', 'no': 'm² bebygd', 'sv': 'm² byggyta'},
    'interior': {'es': 'm² interiores', 'fr': 'm² intérieurs', 'de': 'm² Innenfläche', 'ru': 'м² внутри', 'ar': 'م² داخلية',
                 'nl': 'm² binnen', 'pl': 'm² wnętrza', 'no': 'm² innvendig', 'sv': 'm² inomhus'},
    'terrace': {'es': 'm² de terraza', 'fr': 'm² de terrasse', 'de': 'm² Terrasse', 'ru': 'терраса {n} м²', 'ar': 'م² تراس',
                'nl': 'm² terras', 'pl': 'm² tarasu', 'no': 'm² terrasse', 'sv': 'm² terrass'},
    'solarium': {'es': 'm² de solárium', 'fr': 'm² de solarium', 'de': 'm² Solarium', 'ru': 'солярий {n} м²', 'ar': 'م² سولاريوم',
                 'nl': 'm² solarium', 'pl': 'm² solarium', 'no': 'm² solterrasse', 'sv': 'm² solterrass'},
}


def size_tr(en, loc):
    parts = []
    for seg in en.split(', '):
        n, label = re.fullmatch(r'([\d.]+) sqm (\w+)', seg).groups()
        n = num(n, loc)
        w = SIZE_WORDS[label][loc]
        parts.append(w.replace('{n}', n) if '{n}' in w else f"{n} {w}")
    return ('، ' if loc == 'ar' else ', ').join(parts)


for u in proj['availability']['units']:
    same(u['reference'])
    en = u['size']
    T[en] = {l: size_tr(en, l) for l in LOCS}

# ---- description, SEO, card ------------------------------------------------------------------

a('.description',
  'Diez de las catorce viviendas de la lista de precios del promotor del 3 de noviembre de 2026 están disponibles en esta promoción de 96 viviendas en Marbella: apartamentos y áticos de dos y tres dormitorios desde {E575000} antes de impuestos, con tres piscinas comunitarias, un spa y dos gimnasios.',
  'Dix des quatorze logements de la liste de prix du promoteur du 3 novembre 2026 sont disponibles dans ce programme de 96 logements à Marbella : appartements et penthouses de deux et trois chambres à partir de {E575000} avant taxes, avec trois piscines communes, un spa et deux salles de sport.',
  'Zehn der vierzehn Wohnungen auf der Preisliste des Bauträgers vom 3. November 2026 sind in dieser Anlage mit 96 Wohnungen in Marbella verfügbar: Wohnungen und Penthäuser mit zwei und drei Schlafzimmern ab {E575000} vor Steuern, mit drei Gemeinschaftspools, einem Spa und zwei Fitnessräumen.',
  'Десять из четырнадцати квартир прайс-листа застройщика от 3 ноября 2026 года доступны в этом комплексе из 96 квартир в Марбелье: апартаменты и пентхаусы с двумя и тремя спальнями от {E575000} до налогов, с тремя общими бассейнами, спа и двумя спортзалами.',
  'عشرة من المساكن الأربعة عشر الواردة في قائمة أسعار المطوّر بتاريخ 3 نوفمبر 2026 متاحة في هذا المشروع المؤلف من 96 مسكنًا في ماربيا: شقق وبنتهاوس بغرفتي نوم وثلاث غرف نوم ابتداءً من {E575000} قبل الضرائب، مع ثلاثة مسابح مشتركة وسبا وصالتين رياضيتين.',
  'Tien van de veertien woningen op de prijslijst van de ontwikkelaar van 3 november 2026 zijn beschikbaar in dit complex van 96 woningen in Marbella: appartementen en penthouses met twee en drie slaapkamers vanaf {E575000} vóór belasting, met drie gemeenschappelijke zwembaden, een spa en twee fitnessruimtes.',
  'Dziesięć z czternastu lokali z cennika dewelopera z 3 listopada 2026 jest dostępnych w tej inwestycji liczącej 96 lokali w Marbelli: apartamenty i penthouse’y z dwiema i trzema sypialniami od {E575000} przed opodatkowaniem, z trzema wspólnymi basenami, spa i dwiema siłowniami.',
  'Ti av de fjorten boligene på utbyggerens prisliste av 3. november 2026 er tilgjengelige i dette anlegget med 96 boliger i Marbella: leiligheter og toppleiligheter med to og tre soverom fra {E575000} før skatter og avgifter, med tre fellesbasseng, et spa og to treningsrom.',
  'Tio av de fjorton bostäderna på exploatörens prislista från 3 november 2026 är tillgängliga i detta område med 96 bostäder i Marbella: lägenheter och takvåningar med två och tre sovrum från {E575000} före skatt, med tre gemensamma pooler, ett spa och två gym.')
a('.seoDescription',
  'Apartamentos y áticos de dos y tres dormitorios en una promoción de 96 viviendas en Marbella: diez viviendas disponibles desde {E575000} más IVA, con piscinas comunitarias, un spa y dos gimnasios.',
  'Appartements et penthouses de deux et trois chambres dans un programme de 96 logements à Marbella : dix logements disponibles à partir de {E575000} hors TVA, avec piscines communes, un spa et deux salles de sport.',
  'Wohnungen und Penthäuser mit zwei und drei Schlafzimmern in einer Anlage mit 96 Wohnungen in Marbella: zehn Wohnungen verfügbar ab {E575000} zuzüglich MwSt., mit Gemeinschaftspools, einem Spa und zwei Fitnessräumen.',
  'Апартаменты и пентхаусы с двумя и тремя спальнями в комплексе из 96 квартир в Марбелье: десять квартир доступны от {E575000} плюс НДС, с общими бассейнами, спа и двумя спортзалами.',
  'شقق وبنتهاوس بغرفتي نوم وثلاث غرف نوم في مشروع من 96 مسكنًا في ماربيا: عشرة مساكن متاحة ابتداءً من {E575000} بالإضافة إلى ضريبة القيمة المضافة، مع مسابح مشتركة وسبا وصالتين رياضيتين.',
  'Appartementen en penthouses met twee en drie slaapkamers in een complex van 96 woningen in Marbella: tien woningen beschikbaar vanaf {E575000} plus btw, met gemeenschappelijke zwembaden, een spa en twee fitnessruimtes.',
  'Apartamenty i penthouse’y z dwiema i trzema sypialniami w inwestycji liczącej 96 lokali w Marbelli: dziesięć dostępnych lokali od {E575000} plus VAT, ze wspólnymi basenami, spa i dwiema siłowniami.',
  'Leiligheter og toppleiligheter med to og tre soverom i et anlegg med 96 boliger i Marbella: ti boliger tilgjengelige fra {E575000} pluss mva, med fellesbasseng, et spa og to treningsrom.',
  'Lägenheter och takvåningar med två och tre sovrum i ett område med 96 bostäder i Marbella: tio bostäder tillgängliga från {E575000} plus IVA, med gemensamma pooler, ett spa och två gym.')
a('.twitterDescription',
  'Apartamentos y áticos en Marbella, diez viviendas disponibles desde {E575000}.',
  'Appartements et penthouses à Marbella, dix logements disponibles à partir de {E575000}.',
  'Wohnungen und Penthäuser in Marbella, zehn Wohnungen verfügbar ab {E575000}.',
  'Апартаменты и пентхаусы в Марбелье, десять квартир доступны от {E575000}.',
  'شقق وبنتهاوس في ماربيا، عشرة مساكن متاحة ابتداءً من {E575000}.',
  'Appartementen en penthouses in Marbella, tien woningen beschikbaar vanaf {E575000}.',
  'Apartamenty i penthouse’y w Marbelli, dziesięć dostępnych lokali od {E575000}.',
  'Leiligheter og toppleiligheter i Marbella, ti boliger tilgjengelige fra {E575000}.',
  'Lägenheter och takvåningar i Marbella, tio bostäder tillgängliga från {E575000}.')
a('.card.description',
  'Apartamentos y áticos de dos y tres dormitorios con grandes terrazas en una promoción de 96 viviendas en Marbella, con tres piscinas comunitarias, un spa y dos gimnasios.',
  'Appartements et penthouses de deux et trois chambres avec de grandes terrasses dans un programme de 96 logements à Marbella, avec trois piscines communes, un spa et deux salles de sport.',
  'Wohnungen und Penthäuser mit zwei und drei Schlafzimmern und großen Terrassen in einer Anlage mit 96 Wohnungen in Marbella, mit drei Gemeinschaftspools, einem Spa und zwei Fitnessräumen.',
  'Апартаменты и пентхаусы с двумя и тремя спальнями и большими террасами в комплексе из 96 квартир в Марбелье, с тремя общими бассейнами, спа и двумя спортзалами.',
  'شقق وبنتهاوس بغرفتي نوم وثلاث غرف نوم وتراسات واسعة في مشروع من 96 مسكنًا في ماربيا، مع ثلاثة مسابح مشتركة وسبا وصالتين رياضيتين.',
  'Appartementen en penthouses met twee en drie slaapkamers en grote terrassen in een complex van 96 woningen in Marbella, met drie gemeenschappelijke zwembaden, een spa en twee fitnessruimtes.',
  'Apartamenty i penthouse’y z dwiema i trzema sypialniami oraz dużymi tarasami w inwestycji liczącej 96 lokali w Marbelli, z trzema wspólnymi basenami, spa i dwiema siłowniami.',
  'Leiligheter og toppleiligheter med to og tre soverom og store terrasser i et anlegg med 96 boliger i Marbella, med tre fellesbasseng, et spa og to treningsrom.',
  'Lägenheter och takvåningar med två och tre sovrum och stora terrasser i ett område med 96 bostäder i Marbella, med tre gemensamma pooler, ett spa och två gym.')
a('.quickFacts[4][1]',
  '96 en 12 bloques', '96 dans 12 blocs', '96 in 12 Blöcken', '96 в 12 блоках', '96 في 12 مبنى', '96 in 12 blokken', '96 w 12 budynkach', '96 i 12 blokker', '96 i 12 hus')

# ---- image alts and captions ------------------------------------------------------------------

a('.images.hero.alt',
  'Vista generada por ordenador de un bloque con terrazas escalonadas al atardecer, sobre la piscina comunitaria y su césped',
  'Vue générée par ordinateur d’un bloc aux terrasses en gradins au coucher du soleil, au-dessus de la piscine commune et de sa pelouse',
  'Computergenerierte Ansicht eines Blocks mit gestaffelten Terrassen bei Sonnenuntergang über dem Gemeinschaftspool und seinem Rasen',
  'Компьютерная визуализация корпуса со ступенчатыми террасами на закате над общим бассейном и его газоном',
  'منظر مولَّد بالحاسوب لمبنى بتراسات متدرجة عند الغروب فوق المسبح المشترك ومرجه',
  'Computergegenereerd beeld van een blok met trapsgewijze terrassen bij zonsondergang, boven het gemeenschappelijke zwembad en het gazon',
  'Wygenerowany komputerowo widok budynku z tarasami schodkowymi o zachodzie słońca nad wspólnym basenem i trawnikiem',
  'Datagenerert bilde av en blokk med trappede terrasser i solnedgangen, over fellesbassenget og plenen',
  'Datorgenererad vy av ett hus med trappstegsformade terrasser i solnedgången, ovanför den gemensamma poolen och gräsmattan')
a('.images.architecture.alt',
  'Vista aérea generada por ordenador de dos bloques sobre la piscina, sus cenadores y el césped',
  'Vue aérienne générée par ordinateur de deux blocs au-dessus de la piscine, de ses cabanes et de la pelouse',
  'Computergenerierte Luftansicht zweier Blöcke über dem Pool, seinen Cabanas und dem Rasen',
  'Компьютерная визуализация с высоты: два корпуса над бассейном, его кабанами и газоном',
  'منظر جوي مولَّد بالحاسوب لمبنيين فوق المسبح وأكشاكه والمرج',
  'Computergegenereerd luchtbeeld van twee blokken boven het zwembad, de cabana’s en het gazon',
  'Wygenerowany komputerowo widok z lotu ptaka na dwa budynki nad basenem, jego altanami i trawnikiem',
  'Datagenerert flyfoto av to blokker over bassenget, cabanaene og plenen',
  'Datorgenererad flygvy av två hus ovanför poolen, dess cabanas och gräsmattan')
a('.images.lifestyle.alt',
  'Salón del club social generado por ordenador, con sillones y acristalado hacia el césped y el mar',
  'Salon du club social généré par ordinateur, avec des fauteuils et une baie vitrée sur la pelouse et la mer',
  'Computergenerierte Lounge des Social Clubs mit Sesseln, verglast zum Rasen und zum Meer',
  'Компьютерная визуализация гостиной общественного клуба с креслами и остеклением в сторону газона и моря',
  'صالة النادي الاجتماعي مولَّدة بالحاسوب بمقاعد وزجاج مفتوح على المرج والبحر',
  'Computergegenereerde lounge van de sociale club met fauteuils, beglaasd naar het gazon en de zee',
  'Wygenerowany komputerowo salon klubu mieszkańców z fotelami, przeszklony w stronę trawnika i morza',
  'Datagenerert lounge i sosialklubben med lenestoler og glassvegg mot plenen og havet',
  'Datorgenererad lounge i den sociala klubben med fåtöljer och glasvägg mot gräsmattan och havet')
a('.images.privateViewing.alt',
  'Salón-comedor generado por ordenador con el mar en la ventana',
  'Séjour-salle à manger généré par ordinateur avec la mer dans la fenêtre',
  'Computergeneriertes Wohn- und Esszimmer mit dem Meer im Fenster',
  'Компьютерная визуализация гостиной-столовой с морем в окне',
  'غرفة معيشة وطعام مولَّدة بالحاسوب والبحر في النافذة',
  'Computergegenereerde woon- en eetkamer met de zee in het raam',
  'Wygenerowany komputerowo salon z jadalnią z morzem w oknie',
  'Datagenerert stue og spisestue med havet i vinduet',
  'Datorgenererat vardagsrum med matplats och havet i fönstret')
a('.media.copy',
  'Imágenes generadas por ordenador y fotografías de los dosieres del promotor: los bloques, las terrazas, las viviendas y las zonas comunes. El promotor indica que las imágenes se basan en un proyecto inicial y pueden cambiar durante las obras.',
  'Visuels générés par ordinateur et photographies tirés des dossiers du promoteur : les blocs, les terrasses, les logements et les espaces communs. Le promoteur précise que les visuels reposent sur un projet initial et peuvent évoluer pendant les travaux.',
  'Computergenerierte Visualisierungen und Fotografien aus den Dossiers des Bauträgers: die Blöcke, die Terrassen, die Wohnungen und die Gemeinschaftsbereiche. Der Bauträger weist darauf hin, dass die Visualisierungen auf einem ursprünglichen Projekt beruhen und sich während der Bauarbeiten ändern können.',
  'Компьютерные визуализации и фотографии из досье застройщика: корпуса, террасы, квартиры и общие зоны. Застройщик указывает, что визуализации основаны на первоначальном проекте и могут измениться в ходе строительства.',
  'صور مولَّدة بالحاسوب وصور فوتوغرافية من ملفات المطوّر: المباني والتراسات والمساكن والمناطق المشتركة. يذكر المطوّر أن الصور مبنية على مشروع أوّلي وقد تتغيّر أثناء الأعمال.',
  'Computergegenereerde visuals en foto’s uit de dossiers van de ontwikkelaar: de blokken, de terrassen, de woningen en de gemeenschappelijke ruimtes. De ontwikkelaar geeft aan dat de visuals zijn gebaseerd op een eerste ontwerp en tijdens de werkzaamheden kunnen veranderen.',
  'Wizualizacje komputerowe i fotografie z materiałów dewelopera: budynki, tarasy, lokale i części wspólne. Deweloper zaznacza, że wizualizacje opierają się na pierwotnym projekcie i mogą się zmienić w trakcie robót.',
  'Datagenererte visualiseringer og fotografier fra utbyggerens dossierer: blokkene, terrassene, boligene og fellesområdene. Utbyggeren oppgir at visualiseringene bygger på et opprinnelig prosjekt og kan endres under byggearbeidet.',
  'Datorgenererade visualiseringar och fotografier ur exploatörens dossierer: husen, terrasserna, bostäderna och de gemensamma ytorna. Exploatören anger att visualiseringarna bygger på ett ursprungligt projekt och kan ändras under arbetets gång.')
a('.media.items[1].alt',
  'Vista generada por ordenador de la piscina comunitaria con cenadores, bajo los bloques escalonados',
  'Vue générée par ordinateur de la piscine commune et de ses cabanes, sous les blocs en gradins',
  'Computergenerierte Ansicht des Gemeinschaftspools mit Cabanas unterhalb der gestaffelten Blöcke',
  'Компьютерная визуализация общего бассейна с кабанами под ступенчатыми корпусами',
  'منظر مولَّد بالحاسوب للمسبح المشترك مع الأكشاك، تحت المباني المتدرجة',
  'Computergegenereerd beeld van het gemeenschappelijke zwembad met cabana’s, onder de trapsgewijze blokken',
  'Wygenerowany komputerowo widok wspólnego basenu z altanami, poniżej schodkowych budynków',
  'Datagenerert bilde av fellesbassenget med cabanaer, under de trappede blokkene',
  'Datorgenererad vy av den gemensamma poolen med cabanas, under de trappstegsformade husen')
a('.media.items[3].alt',
  'Fotografía aérea de los bloques en la ladera, con la costa y Marbella al fondo',
  'Photographie aérienne des blocs sur le coteau, avec la côte et Marbella au loin',
  'Luftaufnahme der Blöcke am Hang, dahinter die Küste und Marbella',
  'Аэрофотография корпусов на склоне; вдали видны побережье и Марбелья',
  'صورة جوية للمباني على المنحدر، وخلفها الساحل وماربيا',
  'Luchtfoto van de blokken op de helling, met de kust en Marbella op de achtergrond',
  'Zdjęcie lotnicze budynków na zboczu, w tle wybrzeże i Marbella',
  'Flyfoto av blokkene i skråningen, med kysten og Marbella bak',
  'Flygfoto av husen i sluttningen, med kusten och Marbella bakom')
a('.media.items[4].alt',
  'Fotografía de una piscina comunitaria y su césped frente a un bloque con balcones revestidos de madera',
  'Photographie d’une piscine commune et de sa pelouse devant un bloc aux balcons habillés de bois',
  'Foto eines Gemeinschaftspools mit Rasen vor einem Block mit holzverkleideten Balkonen',
  'Фотография общего бассейна с газоном перед корпусом с балконами в деревянной отделке',
  'صورة لمسبح مشترك ومرجه أمام مبنى بشرفات مكسوّة بالخشب',
  'Foto van een gemeenschappelijk zwembad met gazon voor een blok met houten bekleding op de balkons',
  'Zdjęcie wspólnego basenu z trawnikiem przed budynkiem z balkonami wykończonymi drewnem',
  'Foto av et fellesbasseng og en plen foran en blokk med trekledde balkonger',
  'Foto av en gemensam pool och en gräsmatta framför ett hus med trädbeklädda balkonger')
a('.media.items[5].alt',
  'Solárium de ático generado por ordenador, con césped, asientos y una pequeña piscina; la piscina es una opción con coste adicional',
  'Solarium de penthouse généré par ordinateur, avec pelouse, sièges et petit bassin ; le bassin est une option payante',
  'Computergeneriertes Penthouse-Solarium mit Rasen, Sitzmöbeln und einem kleinen Pool; der Pool ist eine Option gegen Aufpreis',
  'Компьютерная визуализация солярия пентхауса с газоном, местами для отдыха и небольшим бассейном; бассейн — опция за дополнительную плату',
  'سولاريوم بنتهاوس مولَّد بالحاسوب بمرج ومقاعد ومسبح صغير؛ والمسبح خيار بتكلفة إضافية',
  'Computergegenereerd penthouse-solarium met gazon, zitplekken en een klein zwembad; het zwembad is een optie tegen meerprijs',
  'Wygenerowane komputerowo solarium penthouse’u z trawnikiem, miejscami do siedzenia i małym basenem; basen jest opcją za dopłatą',
  'Datagenerert solterrasse på en toppleilighet med plen, sitteplasser og et lite basseng; bassenget er et tilvalg mot tillegg',
  'Datorgenererad solterrass på en takvåning med gräsmatta, sittplatser och en liten pool; poolen är ett tillval mot extra kostnad')
a('.media.items[6].alt',
  'Terraza de ático generada por ordenador, con mesa de comedor, asientos de lounge y el mar al fondo',
  'Terrasse de penthouse générée par ordinateur, avec table à manger, salon d’extérieur et la mer au loin',
  'Computergenerierte Penthouse-Terrasse mit Esstisch, Loungemöbeln und dem Meer dahinter',
  'Компьютерная визуализация террасы пентхауса с обеденным столом, лаунж-мебелью и морем вдали',
  'تراس بنتهاوس مولَّد بالحاسوب بطاولة طعام ومقاعد جلوس والبحر في الخلفية',
  'Computergegenereerd penthouseterras met eettafel, loungemeubilair en de zee op de achtergrond',
  'Wygenerowany komputerowo taras penthouse’u ze stołem jadalnianym, meblami wypoczynkowymi i morzem w tle',
  'Datagenerert terrasse på en toppleilighet med spisebord, loungemøbler og havet bak',
  'Datorgenererad terrass på en takvåning med matbord, loungemöbler och havet bakom')
a('.media.items[7].alt',
  'Terraza cubierta generada por ordenador con una zona de estar y el mar en el horizonte',
  'Terrasse couverte générée par ordinateur avec un coin salon et la mer à l’horizon',
  'Computergenerierte überdachte Terrasse mit Sitzbereich und dem Meer am Horizont',
  'Компьютерная визуализация крытой террасы с зоной отдыха и морем на горизонте',
  'تراس مغطى مولَّد بالحاسوب بمنطقة جلوس والبحر في الأفق',
  'Computergegenereerd overdekt terras met een zithoek en de zee aan de horizon',
  'Wygenerowany komputerowo zadaszony taras ze strefą wypoczynku i morzem na horyzoncie',
  'Datagenerert overbygd terrasse med sittegruppe og havet i horisonten',
  'Datorgenererad täckt terrass med en sittgrupp och havet i horisonten')
a('.media.items[8].alt',
  'Fotografía de una terraza de ático con barandilla de cristal y el mar en el horizonte',
  'Photographie d’une terrasse de penthouse avec garde-corps en verre et la mer à l’horizon',
  'Foto einer Penthouse-Terrasse mit Glasbrüstung und dem Meer am Horizont',
  'Фотография террасы пентхауса со стеклянным ограждением и морем на горизонте',
  'صورة لتراس بنتهاوس بحاجز زجاجي والبحر في الأفق',
  'Foto van een penthouseterras met glazen balustrade en de zee aan de horizon',
  'Zdjęcie tarasu penthouse’u ze szklaną balustradą i morzem na horyzoncie',
  'Foto av en terrasse på en toppleilighet med glassrekkverk og havet i horisonten',
  'Foto av en terrass på en takvåning med glasräcke och havet i horisonten')
a('.media.items[9].alt',
  'Fotografía de una terraza de ático bajo una pérgola, con un antepecho revestido de madera y el mar al fondo',
  'Photographie d’une terrasse de penthouse sous une pergola, avec un parapet habillé de bois et la mer au loin',
  'Foto einer Penthouse-Terrasse unter einer Pergola, mit holzverkleideter Brüstung und dem Meer dahinter',
  'Фотография террасы пентхауса под перголой с парапетом в деревянной отделке и морем вдали',
  'صورة لتراس بنتهاوس تحت برغولا، بدرابزين مكسوّ بالخشب والبحر في الخلفية',
  'Foto van een penthouseterras onder een pergola, met een houten bekleed borstwering en de zee daarachter',
  'Zdjęcie tarasu penthouse’u pod pergolą, z attyką wykończoną drewnem i morzem w tle',
  'Foto av en terrasse på en toppleilighet under en pergola, med trekledd brystning og havet bak',
  'Foto av en terrass på en takvåning under en pergola, med trädbeklätt bröstvärn och havet bakom')
a('.media.items[10].alt',
  'Fotografía de una terraza de ático embaldosada junto a un antepecho revestido de madera, con vistas al mar',
  'Photographie d’une terrasse de penthouse carrelée le long d’un parapet habillé de bois, face à la mer',
  'Foto einer gefliesten Penthouse-Terrasse entlang einer holzverkleideten Brüstung mit Blick aufs Meer',
  'Фотография террасы пентхауса с плиточным покрытием вдоль парапета в деревянной отделке, вид на море',
  'صورة لتراس بنتهاوس مكسوّ بالبلاط بمحاذاة درابزين مكسوّ بالخشب، بإطلالة على البحر',
  'Foto van een betegeld penthouseterras langs een houten bekleed borstwering, met uitzicht op zee',
  'Zdjęcie wyłożonego płytkami tarasu penthouse’u wzdłuż attyki wykończonej drewnem, z widokiem na morze',
  'Foto av en flislagt terrasse på en toppleilighet langs en trekledd brystning, med utsikt mot havet',
  'Foto av en kaklad terrass på en takvåning längs ett trädbeklätt bröstvärn, med utsikt mot havet')
a('.media.items[12].alt',
  'Dormitorio generado por ordenador con un cabecero revestido de listones y una puerta corredera a la terraza',
  'Chambre générée par ordinateur avec une tête de lit habillée de lattes et une porte coulissante vers la terrasse',
  'Computergeneriertes Schlafzimmer mit paneelverkleideter Kopfwand und Schiebetür zur Terrasse',
  'Компьютерная визуализация спальни с изголовьем из реечных панелей и раздвижной дверью на террасу',
  'غرفة نوم مولَّدة بالحاسوب بجدار رأس سرير مكسوّ بألواح وباب منزلق إلى التراس',
  'Computergegenereerde slaapkamer met een met panelen bekleed hoofdeinde en een schuifdeur naar het terras',
  'Wygenerowana komputerowo sypialnia ze ścianą zagłówka wykończoną panelami i przesuwnymi drzwiami na taras',
  'Datagenerert soverom med en panelt hodegavlvegg og en skyvedør ut til terrassen',
  'Datorgenererat sovrum med en panelbeklädd huvudgavel och en skjutdörr till terrassen')
a('.media.items[13].alt',
  'Spa generado por ordenador con una piscina climatizada, un surtidor de agua y tumbonas frente a un muro vegetal',
  'Spa généré par ordinateur avec un bassin chauffé, une cascade et des bains de soleil face à un mur végétal',
  'Computergeneriertes Spa mit beheiztem Pool, Wasserspiel und Liegen vor einer begrünten Wand',
  'Компьютерная визуализация спа с подогреваемым бассейном, водяной струёй и шезлонгами напротив зелёной стены',
  'سبا مولَّد بالحاسوب بمسبح مُدفأ ونافورة مياه ومقاعد استرخاء قبالة جدار نباتي',
  'Computergegenereerde spa met een verwarmd zwembad, een waterpartij en ligbedden voor een beplante wand',
  'Wygenerowane komputerowo spa z podgrzewanym basenem, kaskadą wody i leżakami przed ścianą z roślinnością',
  'Datagenerert spa med et oppvarmet basseng, en vannfontene og solsenger foran en beplantet vegg',
  'Datorgenererat spa med en uppvärmd pool, en vattenstråle och solbäddar framför en bevuxen vägg')
a('.media.items[15].alt',
  'Gimnasio generado por ordenador con cintas de correr y bancos, acristalado hacia un muro vegetal',
  'Salle de sport générée par ordinateur avec des tapis de course et des bancs, vitrée sur un mur végétal',
  'Computergenerierter Fitnessraum mit Laufbändern und Bänken, verglast zu einer begrünten Wand',
  'Компьютерная визуализация спортзала с беговыми дорожками и скамьями, остеклённого в сторону зелёной стены',
  'صالة رياضية مولَّدة بالحاسوب بأجهزة مشي ومقاعد، بزجاج مفتوح على جدار نباتي',
  'Computergegenereerde fitnessruimte met loopbanden en banken, beglaasd naar een beplante wand',
  'Wygenerowana komputerowo siłownia z bieżniami i ławkami, przeszklona w stronę ściany z roślinnością',
  'Datagenerert treningsrom med tredemøller og benker, med glassvegg mot en beplantet vegg',
  'Datorgenererat gym med löpband och bänkar, med glasvägg mot en bevuxen vägg')
a('.media.items[16].alt',
  'Fotografía de la piscina cubierta con tumbonas a lo largo de su lado más lejano',
  'Photographie du bassin intérieur avec des bains de soleil le long de son côté le plus éloigné',
  'Foto des Hallenbads mit Liegen entlang der gegenüberliegenden Seite',
  'Фотография крытого бассейна с шезлонгами вдоль дальней стороны',
  'صورة للمسبح الداخلي بمقاعد استرخاء على طول جانبه البعيد',
  'Foto van het binnenzwembad met ligbedden langs de verste zijde',
  'Zdjęcie krytego basenu z leżakami wzdłuż dalszej strony',
  'Foto av innendørsbassenget med solsenger langs den fjerneste siden',
  'Foto av inomhuspoolen med solbäddar längs den bortre sidan')
a('.media.items[17].alt',
  'Fotografía de un gimnasio con máquinas de cardio, bancos y mancuernas',
  'Photographie d’une salle de sport avec des appareils de cardio, des bancs et des haltères',
  'Foto eines Fitnessraums mit Cardiogeräten, Bänken und Hanteln',
  'Фотография спортзала с кардиотренажёрами, скамьями и гантелями',
  'صورة لصالة رياضية بأجهزة كارديو ومقاعد وأثقال',
  'Foto van een fitnessruimte met cardiotoestellen, banken en dumbbells',
  'Zdjęcie siłowni ze sprzętem cardio, ławkami i hantlami',
  'Foto av et treningsrom med kondisjonsapparater, benker og manualer',
  'Foto av ett gym med konditionsmaskiner, bänkar och hantlar')
a('.media.items[18].alt',
  'Sala de coworking generada por ordenador con una mesa larga, abierta a una terraza con piscina',
  'Espace de coworking généré par ordinateur avec une longue table, ouvert sur une terrasse avec piscine',
  'Computergenerierter Coworking-Raum mit langem Tisch, offen zu einer Poolterrasse',
  'Компьютерная визуализация коворкинга с длинным столом, выходящего на террасу с бассейном',
  'غرفة عمل مشترك مولَّدة بالحاسوب بطاولة طويلة، تنفتح على تراس المسبح',
  'Computergegenereerde coworkingruimte met een lange tafel, open naar een zwembadterras',
  'Wygenerowana komputerowo sala coworkingowa z długim stołem, otwarta na taras przy basenie',
  'Datagenerert coworking-rom med et langt bord, åpent mot en bassengterrasse',
  'Datorgenererat coworkingrum med ett långt bord, öppet mot en poolterrass')

# ---- overview, residences ----------------------------------------------------------------------

a('.overview.headlineHtml',
  '96 viviendas, <em>doce bloques</em>', '96 logements, <em>douze blocs</em>', '96 Wohnungen, <em>zwölf Blöcke</em>', '96 квартир, <em>двенадцать корпусов</em>',
  '96 مسكنًا، <em>اثنا عشر مبنى</em>', '96 woningen, <em>twaalf blokken</em>', '96 lokali, <em>dwanaście budynków</em>', '96 boliger, <em>tolv blokker</em>', '96 bostäder, <em>tolv hus</em>')
a('.overview.copy[0]',
  'Una promoción de 96 viviendas en 12 bloques de hasta tres alturas en Marbella, rodeada de más de {N20,000} {U} de jardines. El promotor la sitúa a cinco minutos de Marbella, con el mar a la vista desde las viviendas.',
  'Un programme de 96 logements répartis en 12 blocs de trois niveaux au plus à Marbella, entouré de plus de {N20,000} {U} de jardins. Le promoteur le situe à cinq minutes de Marbella, avec la mer en vue depuis les logements.',
  'Eine Anlage mit 96 Wohnungen in 12 Blöcken mit höchstens drei Geschossen in Marbella, umgeben von mehr als {N20,000} {U} Gärten. Der Bauträger verortet sie fünf Minuten von Marbella entfernt, mit Meerblick aus den Wohnungen.',
  'Комплекс из 96 квартир в 12 корпусах высотой не более трёх этажей в Марбелье, среди более чем {N20,000} {U} садов. Застройщик помещает его в пяти минутах от Марбельи, с видом на море из квартир.',
  'مشروع من 96 مسكنًا في 12 مبنى لا يزيد ارتفاع أيٍّ منها على ثلاثة طوابق في ماربيا، تحيط به حدائق تتجاوز مساحتها {N20,000} {U}. يضعه المطوّر على بُعد خمس دقائق من ماربيا، مع إطلالة على البحر من المساكن.',
  'Een complex van 96 woningen in 12 blokken van hooguit drie bouwlagen in Marbella, omgeven door meer dan {N20,000} {U} tuinen. De ontwikkelaar plaatst het op vijf minuten van Marbella, met zicht op zee vanuit de woningen.',
  'Inwestycja z 96 lokalami w 12 budynkach o wysokości najwyżej trzech kondygnacji w Marbelli, otoczona ponad {N20,000} {U} ogrodów. Deweloper umieszcza ją pięć minut od Marbelli, z widokiem na morze z lokali.',
  'Et anlegg med 96 boliger i 12 blokker på høyst tre etasjer i Marbella, omgitt av mer enn {N20,000} {U} hage. Utbyggeren plasserer det fem minutter fra Marbella, med utsikt mot havet fra boligene.',
  'Ett område med 96 bostäder i 12 hus på högst tre våningar i Marbella, omgivet av mer än {N20,000} {U} trädgårdar. Exploatören placerar det fem minuter från Marbella, med utsikt mot havet från bostäderna.')
a('.overview.copy[1]',
  'Las viviendas son apartamentos en planta baja y primera y áticos por encima, cada ático con un solárium privado sobre su terraza.',
  'Les logements sont des appartements au rez-de-chaussée et au premier étage, et des penthouses au-dessus, chacun avec un solarium privé au-dessus de sa terrasse.',
  'Die Wohnungen sind Apartments im Erd- und Obergeschoss und darüber Penthäuser, jedes mit einem privaten Solarium über seiner Terrasse.',
  'Это квартиры на первом и втором этажах и пентхаусы над ними, у каждого пентхауса частный солярий над террасой.',
  'المساكن شقق في الطابقين الأرضي والأول وبنتهاوس فوقها، ولكل بنتهاوس سولاريوم خاص فوق تراسه.',
  'De woningen zijn appartementen op de begane grond en de eerste verdieping en daarboven penthouses, elk met een privésolarium boven het terras.',
  'Lokale to apartamenty na parterze i pierwszym piętrze oraz penthouse’y nad nimi, każdy z prywatnym solarium nad tarasem.',
  'Boligene er leiligheter i første og andre etasje og toppleiligheter over dem, hver med en privat solterrasse over terrassen.',
  'Bostäderna är lägenheter i bottenvåningen och på första våningen och takvåningar ovanför, var och en med en privat solterrass ovanpå sin terrass.')
a('.residences.copy',
  'Apartamentos de dos dormitorios en planta baja y primera, y áticos de dos y tres dormitorios con solárium privado.',
  'Des appartements de deux chambres au rez-de-chaussée et au premier étage, et des penthouses de deux et trois chambres avec solarium privé.',
  'Apartments mit zwei Schlafzimmern im Erd- und Obergeschoss sowie Penthäuser mit zwei und drei Schlafzimmern und privatem Solarium.',
  'Апартаменты с двумя спальнями на первом и втором этажах и пентхаусы с двумя и тремя спальнями и частным солярием.',
  'شقق بغرفتي نوم في الطابقين الأرضي والأول، وبنتهاوس بغرفتي نوم وثلاث غرف نوم مع سولاريوم خاص.',
  'Appartementen met twee slaapkamers op de begane grond en de eerste verdieping, en penthouses met twee en drie slaapkamers en een privésolarium.',
  'Dwupokojowe apartamenty na parterze i pierwszym piętrze oraz penthouse’y z dwiema i trzema sypialniami z prywatnym solarium.',
  'Leiligheter med to soverom i første og andre etasje, og toppleiligheter med to og tre soverom og privat solterrasse.',
  'Lägenheter med två sovrum i bottenvåningen och på första våningen, och takvåningar med två och tre sovrum och privat solterrass.')
a('.residences.items[0].points[0]',
  'Dos dormitorios, de {N80.59} a {N82.56} {U} de superficie interior útil y de {N91.31} a {N93.28} {U} construidos.',
  'Deux chambres, de {N80.59} à {N82.56} {U} de surface intérieure et de {N91.31} à {N93.28} {U} construits.',
  'Zwei Schlafzimmer, {N80.59} bis {N82.56} {U} Innenfläche und {N91.31} bis {N93.28} {U} bebaut.',
  'Две спальни, от {N80.59} до {N82.56} {U} внутренней площади и от {N91.31} до {N93.28} {U} площади застройки.',
  'غرفتا نوم، من {N80.59} إلى {N82.56} {U} من المساحة الداخلية ومن {N91.31} إلى {N93.28} {U} مساحة مبنية.',
  'Twee slaapkamers, {N80.59} tot {N82.56} {U} binnenoppervlak en {N91.31} tot {N93.28} {U} bebouwd.',
  'Dwie sypialnie, od {N80.59} do {N82.56} {U} powierzchni wewnętrznej i od {N91.31} do {N93.28} {U} powierzchni zabudowy.',
  'To soverom, {N80.59} til {N82.56} {U} innvendig areal og {N91.31} til {N93.28} {U} bebygd areal.',
  'Två sovrum, {N80.59} till {N82.56} {U} invändig yta och {N91.31} till {N93.28} {U} byggyta.')
a('.residences.items[0].points[1]',
  'Terrazas de {N32.00} a {N46.72} {U}, cubiertas, abiertas o ambas.',
  'Des terrasses de {N32.00} à {N46.72} {U}, couvertes, ouvertes ou les deux.',
  'Terrassen von {N32.00} bis {N46.72} {U}, überdacht, offen oder beides.',
  'Террасы от {N32.00} до {N46.72} {U}, крытые, открытые или и те и другие.',
  'تراسات من {N32.00} إلى {N46.72} {U}، مغطاة أو مكشوفة أو كلتاهما.',
  'Terrassen van {N32.00} tot {N46.72} {U}, overdekt, open of allebei.',
  'Tarasy od {N32.00} do {N46.72} {U}, zadaszone, otwarte lub jedne i drugie.',
  'Terrasser på {N32.00} til {N46.72} {U}, overbygde, åpne eller begge deler.',
  'Terrasser på {N32.00} till {N46.72} {U}, täckta, öppna eller både och.')
a('.residences.items[0].points[2]',
  'La lista de precios asigna una plaza de aparcamiento y un trastero a cada apartamento, y no indica si están incluidos en el precio.',
  'La liste de prix attribue une place de parking et un débarras à chaque appartement, sans préciser s’ils sont compris dans le prix.',
  'Die Preisliste weist jeder Wohnung einen Stellplatz und einen Abstellraum zu und sagt nicht, ob sie im Preis enthalten sind.',
  'Прайс-лист закрепляет за каждой квартирой одно машиноместо и кладовую и не уточняет, входят ли они в цену.',
  'تخصّص قائمة الأسعار لكل شقة موقف سيارة ومخزنًا، ولا تذكر ما إذا كانا مشمولين في السعر.',
  'De prijslijst wijst bij elk appartement één parkeerplaats en een berging toe en vermeldt niet of die in de prijs zijn inbegrepen.',
  'Cennik przypisuje każdemu apartamentowi jedno miejsce postojowe i komórkę lokatorską i nie podaje, czy są wliczone w cenę.',
  'Prislisten tildeler hver leilighet én parkeringsplass og en bod, og sier ikke om de er inkludert i prisen.',
  'Prislistan tilldelar varje lägenhet en parkeringsplats och ett förråd och anger inte om de ingår i priset.')
a('.residences.items[0].points[3]',
  'El dosier de 2022 describe viviendas en planta baja con jardín y piscina privada. La lista de precios no muestra jardín ni piscina para la 20B, la única vivienda de planta baja que figura en ella.',
  'Le dossier de 2022 décrit des logements de rez-de-chaussée avec jardin et piscine privée. La liste de prix n’indique ni jardin ni piscine pour le 20B, le seul logement de rez-de-chaussée qui y figure.',
  'Das Dossier von 2022 beschreibt Erdgeschosswohnungen mit Garten und privatem Pool. Die Preisliste zeigt für die 20B, die einzige Erdgeschosswohnung auf der Liste, weder Garten noch Pool.',
  'Досье 2022 года описывает квартиры на первом этаже с садом и частным бассейном. В прайс-листе для 20B, единственной квартиры первого этажа в нём, не указано ни сада, ни бассейна.',
  'يصف ملف عام 2022 مساكن في الطابق الأرضي بحديقة ومسبح خاص. أما قائمة الأسعار فلا تُظهر حديقة ولا مسبحًا للمسكن 20B، وهو المسكن الوحيد في الطابق الأرضي الوارد فيها.',
  'Het dossier van 2022 beschrijft woningen op de begane grond met tuin en privézwembad. De prijslijst toont geen tuin en geen zwembad voor 20B, de enige woning op de begane grond op de lijst.',
  'Materiał z 2022 roku opisuje lokale na parterze z ogrodem i prywatnym basenem. Cennik nie podaje ogrodu ani basenu dla 20B, jedynego lokalu na parterze, który się na nim znajduje.',
  'Dossieret fra 2022 beskriver boliger i første etasje med hage og privat basseng. Prislisten viser verken hage eller basseng for 20B, den eneste boligen i første etasje på listen.',
  'Dossiern från 2022 beskriver bostäder i bottenvåningen med trädgård och privat pool. Prislistan visar varken trädgård eller pool för 20B, den enda bostaden i bottenvåningen på listan.')
a('.residences.items[1].points[0]',
  'Tres dormitorios, salvo la 82B, que tiene dos: de {N84.44} a {N107.96} {U} de superficie interior útil.',
  'Trois chambres, sauf le 82B qui en compte deux : de {N84.44} à {N107.96} {U} de surface intérieure.',
  'Drei Schlafzimmer, außer der 82B mit zweien: {N84.44} bis {N107.96} {U} Innenfläche.',
  'Три спальни, кроме 82B с двумя: от {N84.44} до {N107.96} {U} внутренней площади.',
  'ثلاث غرف نوم، باستثناء 82B التي لها غرفتا نوم: من {N84.44} إلى {N107.96} {U} من المساحة الداخلية.',
  'Drie slaapkamers, behalve 82B met twee: {N84.44} tot {N107.96} {U} binnenoppervlak.',
  'Trzy sypialnie, z wyjątkiem 82B z dwiema: od {N84.44} do {N107.96} {U} powierzchni wewnętrznej.',
  'Tre soverom, unntatt 82B med to: {N84.44} til {N107.96} {U} innvendig areal.',
  'Tre sovrum, utom 82B med två: {N84.44} till {N107.96} {U} invändig yta.')
a('.residences.items[1].points[1]',
  'Un solárium privado de {N49.60} a {N71.20} {U} y terrazas de {N96.41} a {N120.75} {U} según la lista de precios.',
  'Un solarium privé de {N49.60} à {N71.20} {U} et des terrasses de {N96.41} à {N120.75} {U} selon la liste de prix.',
  'Ein privates Solarium von {N49.60} bis {N71.20} {U} und Terrassen von {N96.41} bis {N120.75} {U} laut Preisliste.',
  'Частный солярий от {N49.60} до {N71.20} {U} и террасы от {N96.41} до {N120.75} {U} по прайс-листу.',
  'سولاريوم خاص من {N49.60} إلى {N71.20} {U} وتراسات من {N96.41} إلى {N120.75} {U} بحسب قائمة الأسعار.',
  'Een privésolarium van {N49.60} tot {N71.20} {U} en terrassen van {N96.41} tot {N120.75} {U} volgens de prijslijst.',
  'Prywatne solarium od {N49.60} do {N71.20} {U} i tarasy od {N96.41} do {N120.75} {U} według cennika.',
  'En privat solterrasse på {N49.60} til {N71.20} {U} og terrasser på {N96.41} til {N120.75} {U} ifølge prislisten.',
  'En privat solterrass på {N49.60} till {N71.20} {U} och terrasser på {N96.41} till {N120.75} {U} enligt prislistan.')
a('.residences.items[1].points[2]',
  'Dos plazas de aparcamiento y un trastero asignados a cada ático en la lista de precios, que no indica si están incluidos en el precio.',
  'Deux places de parking et un débarras attribués à chaque penthouse dans la liste de prix, qui ne précise pas s’ils sont compris dans le prix.',
  'Zwei Stellplätze und ein Abstellraum sind in der Preisliste jedem Penthouse zugewiesen; sie sagt nicht, ob sie im Preis enthalten sind.',
  'В прайс-листе за каждым пентхаусом закреплены два машиноместа и кладовая; входят ли они в цену, не сказано.',
  'موقفا سيارات ومخزن مخصصة لكل بنتهاوس في قائمة الأسعار، التي لا تذكر ما إذا كانت مشمولة في السعر.',
  'Twee parkeerplaatsen en een berging zijn op de prijslijst aan elk penthouse toegewezen; de lijst vermeldt niet of ze in de prijs zijn inbegrepen.',
  'Dwa miejsca postojowe i komórka lokatorska przypisane do każdego penthouse’u w cenniku, który nie podaje, czy są wliczone w cenę.',
  'To parkeringsplasser og en bod er tildelt hver toppleilighet i prislisten, som ikke sier om de er inkludert i prisen.',
  'Två parkeringsplatser och ett förråd är tilldelade varje takvåning i prislistan, som inte anger om de ingår i priset.')
a('.residences.items[1].points[3]',
  'El dosier de junio de 2026 muestra un jacuzzi en el solárium. Las hojas de planos dicen que la piscina dibujada en la planta del solárium no forma parte del proyecto ni del precio y es una opción a cargo del comprador. Ningún documento dice si el jacuzzi está incluido.',
  'Le dossier de juin 2026 montre un jacuzzi sur le solarium. Les planches de plans précisent que le bassin dessiné à l’étage du solarium ne fait partie ni du projet ni du prix et constitue une option à la charge de l’acquéreur. Aucun document ne dit si le jacuzzi est inclus.',
  'Das Dossier vom Juni 2026 zeigt einen Whirlpool auf dem Solarium. Die Planblätter besagen, dass der auf der Solarium-Ebene eingezeichnete Pool weder zum Projekt noch zum Preis gehört und eine Option auf Kosten des Käufers ist. Kein Dokument sagt, ob der Whirlpool enthalten ist.',
  'В досье июня 2026 года на солярии показано джакузи. В планировочных листах сказано, что бассейн, нарисованный на уровне солярия, не входит ни в проект, ни в цену и является опцией за счёт покупателя. Ни один документ не говорит, включено ли джакузи.',
  'يُظهر ملف يونيو 2026 جاكوزي على السولاريوم. وتذكر أوراق المخططات أن المسبح المرسوم في طابق السولاريوم ليس جزءًا من المشروع ولا من السعر وهو خيار على نفقة المشتري. ولا تذكر أي وثيقة ما إذا كان الجاكوزي مشمولًا.',
  'Het dossier van juni 2026 toont een jacuzzi op het solarium. De plattegrondbladen zeggen dat het zwembad dat op de solariumverdieping is getekend geen deel uitmaakt van het project of de prijs en een optie is voor rekening van de koper. Geen enkel document zegt of de jacuzzi is inbegrepen.',
  'Materiał z czerwca 2026 roku pokazuje jacuzzi na solarium. Arkusze rzutów podają, że basen narysowany na poziomie solarium nie należy do projektu ani do ceny i jest opcją na koszt kupującego. Żaden dokument nie mówi, czy jacuzzi jest wliczone.',
  'Dossieret fra juni 2026 viser en jacuzzi på solterrassen. Plantegningsarkene sier at bassenget som er tegnet inn på solterrasseplanet verken er en del av prosjektet eller prisen og er et tilvalg for kjøperens regning. Ingen dokumenter sier om jacuzzien er inkludert.',
  'Dossiern från juni 2026 visar ett badkar med bubbelfunktion på solterrassen. Planritningsbladen anger att poolen som ritats in på solterrassplanet varken ingår i projektet eller priset och är ett tillval på köparens bekostnad. Inget dokument anger om jacuzzin ingår.')

# ---- availability --------------------------------------------------------------------------------

a('.availability.headlineHtml',
  '10 de las 14 viviendas de la lista, <em>disponibles</em>', '10 des 14 logements de la liste, <em>disponibles</em>', '10 der 14 gelisteten Wohnungen <em>verfügbar</em>',
  '10 из 14 квартир списка <em>доступны</em>', '10 من أصل 14 مسكنًا مدرجًا <em>متاحة</em>', '10 van de 14 vermelde woningen <em>beschikbaar</em>',
  '10 z 14 lokali z listy <em>dostępnych</em>', '10 av de 14 oppførte boligene <em>tilgjengelige</em>', '10 av de 14 upptagna bostäderna <em>tillgängliga</em>')
a('.availability.copy',
  'La lista de precios del promotor del 3 de noviembre de 2026 muestra catorce de las 96 viviendas de la promoción. Diez están disponibles, dos vendidas y dos reservadas. Nueva Living reconfirma el precio y la disponibilidad antes de cualquier visita o reserva.',
  'La liste de prix du promoteur du 3 novembre 2026 présente quatorze des 96 logements du programme. Dix sont disponibles, deux sont vendus et deux sont réservés. Nueva Living reconfirme le prix et la disponibilité avant toute visite ou réservation.',
  'Die Preisliste des Bauträgers vom 3. November 2026 zeigt vierzehn der 96 Wohnungen der Anlage. Zehn sind verfügbar, zwei verkauft und zwei reserviert. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung erneut.',
  'В прайс-листе застройщика от 3 ноября 2026 года указаны четырнадцать из 96 квартир комплекса. Десять доступны, две проданы и две забронированы. Nueva Living повторно подтверждает цену и наличие перед любым просмотром или бронированием.',
  'تعرض قائمة أسعار المطوّر بتاريخ 3 نوفمبر 2026 أربعة عشر مسكنًا من أصل 96 في المشروع. عشرة منها متاحة واثنان مباعان واثنان محجوزان. تعيد نويفا ليفينغ تأكيد السعر والتوافر قبل أي معاينة أو حجز.',
  'De prijslijst van de ontwikkelaar van 3 november 2026 toont veertien van de 96 woningen van het complex. Tien zijn beschikbaar, twee verkocht en twee gereserveerd. Nueva Living bevestigt prijs en beschikbaarheid opnieuw vóór een bezichtiging of reservering.',
  'Cennik dewelopera z 3 listopada 2026 pokazuje czternaście z 96 lokali inwestycji. Dziesięć jest dostępnych, dwa sprzedane i dwa zarezerwowane. Nueva Living ponownie potwierdza cenę i dostępność przed każdym oglądaniem lub rezerwacją.',
  'Utbyggerens prisliste av 3. november 2026 viser fjorten av anleggets 96 boliger. Ti er tilgjengelige, to er solgt og to er reservert. Nueva Living bekrefter pris og tilgjengelighet på nytt før enhver visning eller reservasjon.',
  'Exploatörens prislista från 3 november 2026 visar fjorton av områdets 96 bostäder. Tio är tillgängliga, två är sålda och två är reserverade. Nueva Living bekräftar pris och tillgänglighet på nytt före varje visning eller bokning.')
a('.availability.sourceNote',
  'Todas las cifras están transcritas de la lista de precios del promotor fechada el 3 de noviembre de 2026, que indica que los precios no incluyen IVA y que la lista es válida durante dos días desde su descarga. Están vendidas la 22A y la 32B; están reservadas la 72A y la 92A. «Construidos» es la superficie construida interior de la lista, «interiores» su superficie interior, y terraza y solárium figuran como en la lista. Cuando un plano difiere de la lista, la tabla sigue la lista: el plano de la 62B da {N98.89} {U} de superficie exterior frente a los {N96.41} de la lista, y el de la 72B {N108.46} frente a {N108.51}. El promotor no ha emitido plano para la 12A, la 61B ni la 102A. La 61B y la 62B figuran como pisos piloto amueblados. El IVA es del 10 por ciento y el impuesto de actos jurídicos documentados del 1,20 por ciento, de modo que el apartamento de {N575,000} euros cuesta unos {N639,000} euros antes de notaría y registro, y el ático de {N1,375,000} euros unos {N1,529,000}.',
  'Tous les chiffres sont transcrits de la liste de prix du promoteur datée du 3 novembre 2026, qui précise que les prix s’entendent hors TVA et que la liste est valable deux jours à compter de son téléchargement. Sont vendus le 22A et le 32B ; sont réservés le 72A et le 92A. « Construits » est la surface construite intérieure de la liste, « intérieurs » sa surface intérieure, et la terrasse et le solarium figurent comme dans la liste. Lorsqu’un plan diffère de la liste, le tableau suit la liste : le plan du 62B donne {N98.89} {U} de surface extérieure contre {N96.41} dans la liste, et celui du 72B {N108.46} contre {N108.51}. Le promoteur n’a émis aucun plan pour le 12A, le 61B et le 102A. Le 61B et le 62B sont indiqués comme appartements témoins meublés. La TVA est de 10 pour cent et le droit de timbre de 1,20 pour cent, de sorte que l’appartement à {N575,000} euros revient à environ {N639,000} euros avant frais de notaire et d’enregistrement, et le penthouse à {N1,375,000} euros à environ {N1,529,000}.',
  'Alle Angaben sind der Preisliste des Bauträgers vom 3. November 2026 entnommen, die besagt, dass die Preise ohne MwSt. verstanden sind und dass die Liste zwei Tage ab dem Herunterladen gültig ist. Verkauft sind 22A und 32B; reserviert sind 72A und 92A. „Bebaut“ ist die Innenbaufläche der Liste, „Innenfläche“ ihre Innenfläche, Terrasse und Solarium stehen wie in der Liste. Weicht ein Plan von der Liste ab, folgt die Tabelle der Liste: Der Plan der 62B nennt {N98.89} {U} Außenfläche gegenüber {N96.41} in der Liste, der der 72B {N108.46} gegenüber {N108.51}. Für 12A, 61B und 102A hat der Bauträger keinen Plan herausgegeben. 61B und 62B sind als möblierte Musterwohnungen gekennzeichnet. Die Mehrwertsteuer beträgt 10 Prozent, die Stempelsteuer 1,20 Prozent, sodass die Wohnung für {N575,000} Euro vor Notar- und Grundbuchkosten rund {N639,000} Euro kostet und das Penthouse für {N1,375,000} Euro rund {N1,529,000}.',
  'Все цифры перенесены из прайс-листа застройщика от 3 ноября 2026 года, в котором указано, что цены даны без НДС и что список действителен два дня с момента скачивания. Проданы 22A и 32B; забронированы 72A и 92A. «Застроенная площадь» — внутренняя застроенная площадь из списка, «внутри» — его внутренняя площадь, терраса и солярий указаны как в списке. Если планировка расходится со списком, таблица следует списку: по планировке 62B внешняя площадь составляет {N98.89} {U} против {N96.41} в списке, по планировке 72B — {N108.46} против {N108.51}. Планировок для 12A, 61B и 102A застройщик не выпускал. 61B и 62B отмечены как меблированные демонстрационные квартиры. НДС составляет 10 процентов, гербовый сбор — 1,20 процента, поэтому квартира за {N575,000} € обходится примерно в {N639,000} € до нотариуса и регистрации, а пентхаус за {N1,375,000} € — примерно в {N1,529,000}.',
  'جميع الأرقام منقولة من قائمة أسعار المطوّر المؤرخة في 3 نوفمبر 2026، التي تنص على أن الأسعار لا تشمل ضريبة القيمة المضافة وأن القائمة صالحة لمدة يومين من تنزيلها. المباع هو 22A و32B، والمحجوز هو 72A و92A. «المبنية» هي المساحة المبنية الداخلية في القائمة، و«الداخلية» مساحتها الداخلية، ويرد التراس والسولاريوم كما في القائمة. وحيث يختلف مخطط عن القائمة يتبع الجدول القائمة: يعطي مخطط 62B مساحة خارجية قدرها {N98.89} {U} مقابل {N96.41} في القائمة، ومخطط 72B {N108.46} مقابل {N108.51}. ولم يُصدر المطوّر مخططًا لـ 12A و61B و102A. ويُشار إلى 61B و62B كشقتين نموذجيتين مفروشتين. ضريبة القيمة المضافة 10 بالمئة ورسم الدمغة 1.20 بالمئة، فتصبح الشقة بسعر {N575,000} € نحو {N639,000} € قبل أتعاب التوثيق والتسجيل، والبنتهاوس بسعر {N1,375,000} € نحو {N1,529,000}.',
  'Alle cijfers zijn overgenomen uit de prijslijst van de ontwikkelaar van 3 november 2026, die vermeldt dat de prijzen exclusief btw zijn en dat de lijst twee dagen na het downloaden geldig is. Verkocht zijn 22A en 32B; gereserveerd zijn 72A en 92A. „Bebouwd” is het binnenbebouwde oppervlak van de lijst, „binnen” het binnenoppervlak, en terras en solarium staan zoals in de lijst. Waar een plattegrond van de lijst afwijkt, volgt de tabel de lijst: de plattegrond van 62B geeft {N98.89} {U} buitenoppervlak tegenover {N96.41} in de lijst, die van 72B {N108.46} tegenover {N108.51}. Voor 12A, 61B en 102A heeft de ontwikkelaar geen plattegrond uitgegeven. 61B en 62B staan aangemerkt als gemeubileerde modelwoningen. De btw bedraagt 10 procent en de overdrachtsbelasting 1,20 procent, zodat het appartement van {N575,000} euro ongeveer {N639,000} euro kost vóór notaris- en kadasterkosten, en het penthouse van {N1,375,000} euro ongeveer {N1,529,000}.',
  'Wszystkie dane są przepisane z cennika dewelopera z 3 listopada 2026, który podaje, że ceny nie zawierają VAT i że lista jest ważna dwa dni od pobrania. Sprzedane są 22A i 32B; zarezerwowane są 72A i 92A. „Zabudowy” to wewnętrzna powierzchnia zabudowy z listy, „wnętrza” to jej powierzchnia wewnętrzna, a taras i solarium podano jak na liście. Gdy rzut różni się od listy, tabela idzie za listą: rzut 62B podaje {N98.89} {U} powierzchni zewnętrznej wobec {N96.41} na liście, a rzut 72B {N108.46} wobec {N108.51}. Dla 12A, 61B i 102A deweloper nie wydał rzutów. 61B i 62B oznaczono jako umeblowane mieszkania pokazowe. VAT wynosi 10 procent, a podatek od czynności cywilnoprawnych 1,20 procent, więc apartament za {N575,000} euro kosztuje około {N639,000} euro przed opłatami notarialnymi i wpisem do księgi wieczystej, a penthouse za {N1,375,000} euro około {N1,529,000}.',
  'Alle tall er overført fra utbyggerens prisliste datert 3. november 2026, som oppgir at prisene er uten mva og at listen gjelder i to dager fra nedlasting. Solgt er 22A og 32B; reservert er 72A og 92A. «Bebygd» er listens innvendige bebygde areal, «innvendig» er listens innvendige areal, og terrasse og solterrasse er som på listen. Der en plantegning avviker fra listen, følger tabellen listen: plantegningen for 62B oppgir {N98.89} {U} utvendig areal mot {N96.41} på listen, og den for 72B {N108.46} mot {N108.51}. Utbyggeren har ikke utstedt plantegning for 12A, 61B og 102A. 61B og 62B er oppført som møblerte visningsleiligheter. Merverdiavgiften er 10 prosent og dokumentavgiften 1,20 prosent, slik at leiligheten til {N575,000} euro koster rundt {N639,000} euro før notar- og tinglysingsgebyrer, og toppleiligheten til {N1,375,000} euro rundt {N1,529,000}.',
  'Alla siffror är överförda från exploatörens prislista daterad 3 november 2026, som anger att priserna är exklusive IVA (spansk moms) och att listan gäller i två dagar från nedladdningen. Sålda är 22A och 32B; reserverade är 72A och 92A. ”Byggyta” är listans invändiga byggyta, ”inomhus” dess invändiga yta, och terrass och solterrass anges som i listan. Där en planritning avviker från listan följer tabellen listan: planritningen för 62B anger {N98.89} {U} utvändig yta mot {N96.41} i listan, och den för 72B {N108.46} mot {N108.51}. För 12A, 61B och 102A har exploatören inte utfärdat någon planritning. 61B och 62B är angivna som möblerade visningsbostäder. IVA är 10 procent och stämpelskatten 1,20 procent, så lägenheten för {N575,000} euro kostar omkring {N639,000} euro före notarie- och registreringsavgifter, och takvåningen för {N1,375,000} euro omkring {N1,529,000}.')

# ---- construction timeline and payment terms -----------------------------------------------------

a('.constructionTimeline.points[0].label',
  'Fecha no indicada', 'Date non indiquée', 'Termin nicht angegeben', 'Срок не указан', 'الموعد غير مذكور', 'Datum niet opgegeven', 'Termin nie podano', 'Dato ikke oppgitt', 'Datum ej angivet')
a('.constructionTimeline.points[1].year',
  'Escritura', 'Acte authentique', 'Beurkundung', 'Нотариальный акт', 'سند الملكية', 'Notariële akte', 'Akt notarialny', 'Skjøte', 'Notarieakt')
a('.constructionTimeline.points[1].label',
  '60 o 90 días tras la reserva', '60 ou 90 jours après la réservation', '60 oder 90 Tage nach der Reservierung', '60 или 90 дней после бронирования', '60 أو 90 يومًا بعد الحجز',
  '60 of 90 dagen na de reservering', '60 lub 90 dni po rezerwacji', '60 eller 90 dager etter reservasjonen', '60 eller 90 dagar efter bokningen')
a('.constructionTimeline.note',
  'Los documentos del promotor no dan fecha de entrega, estado de las licencias ni fase de las obras. Las dos hojas de condiciones de pago sitúan la escritura 60 o 90 días después de la reserva, el dosier de junio de 2026 muestra fotografías de bloques construidos y la lista de precios marca dos viviendas como pisos piloto amueblados, por lo que algunas viviendas podrían estar terminadas. Nueva Living pregunta qué viviendas están terminadas y pide por escrito las licencias y la fecha de entrega antes de que usted se comprometa.',
  'Les documents du promoteur ne donnent ni date de livraison, ni état des licences, ni stade des travaux. Les deux feuilles de conditions de paiement fixent l’acte authentique 60 ou 90 jours après la réservation, le dossier de juin 2026 montre des photographies de blocs construits et la liste de prix désigne deux logements comme appartements témoins meublés : certains logements pourraient donc être achevés. Nueva Living demande quels logements sont achevés, ainsi que les licences et la date de livraison par écrit, avant que vous vous engagiez.',
  'Die Unterlagen des Bauträgers nennen weder einen Fertigstellungstermin noch den Stand der Genehmigungen oder der Bauarbeiten. Die beiden Zahlungsblätter legen die Beurkundung 60 oder 90 Tage nach der Reservierung fest, das Dossier vom Juni 2026 zeigt Fotos fertiggestellter Blöcke und die Preisliste kennzeichnet zwei Wohnungen als möblierte Musterwohnungen, sodass einige Wohnungen fertig sein könnten. Nueva Living fragt nach, welche Wohnungen fertig sind, und verlangt Genehmigungen und Fertigstellungstermin schriftlich, bevor Sie sich binden.',
  'В документах застройщика нет ни срока сдачи, ни статуса разрешений, ни стадии строительства. Два листа условий оплаты назначают нотариальный акт через 60 или 90 дней после бронирования, в досье июня 2026 года есть фотографии построенных корпусов, а прайс-лист отмечает две квартиры как меблированные демонстрационные, поэтому часть квартир может быть уже готова. Nueva Living выясняет, какие квартиры готовы, и запрашивает разрешения и срок сдачи в письменном виде, прежде чем вы примете обязательства.',
  'لا تذكر وثائق المطوّر موعد تسليم ولا وضع التراخيص ولا مرحلة الأعمال. وتحدد ورقتا شروط الدفع سند الملكية بعد 60 أو 90 يومًا من الحجز، ويعرض ملف يونيو 2026 صورًا لمبانٍ منجزة، وتشير قائمة الأسعار إلى مسكنين كشقتين نموذجيتين مفروشتين، فقد تكون بعض المساكن منجزة. تسأل نويفا ليفينغ عن المساكن المنجزة وتطلب كتابةً التراخيص وموعد التسليم قبل أن تلتزم.',
  'De documenten van de ontwikkelaar geven geen opleverdatum, geen stand van de vergunningen en geen bouwfase. De twee betalingsbladen leggen de notariële akte 60 of 90 dagen na de reservering, het dossier van juni 2026 toont foto’s van voltooide blokken en de prijslijst markeert twee woningen als gemeubileerde modelwoningen, dus sommige woningen kunnen al klaar zijn. Nueva Living vraagt welke woningen klaar zijn en vraagt de vergunningen en de opleverdatum schriftelijk op voordat u zich bindt.',
  'Dokumenty dewelopera nie podają terminu odbioru, stanu pozwoleń ani etapu robót. Dwa arkusze warunków płatności wyznaczają akt notarialny na 60 lub 90 dni po rezerwacji, materiał z czerwca 2026 roku pokazuje zdjęcia ukończonych budynków, a cennik oznacza dwa lokale jako umeblowane mieszkania pokazowe, więc część lokali może być już gotowa. Nueva Living pyta, które lokale są ukończone, i żąda na piśmie pozwoleń oraz terminu odbioru, zanim Państwo się zobowiążą.',
  'Utbyggerens dokumenter oppgir verken ferdigstillelsesdato, status for tillatelsene eller byggetrinn. De to betalingsarkene setter skjøtet 60 eller 90 dager etter reservasjonen, dossieret fra juni 2026 viser fotografier av ferdige blokker, og prislisten markerer to boliger som møblerte visningsleiligheter, så noen boliger kan være ferdige. Nueva Living spør hvilke boliger som er ferdige, og ber skriftlig om tillatelsene og ferdigstillelsesdatoen før De forplikter dere.',
  'Exploatörens dokument anger varken tillträdesdatum, status för tillstånden eller byggskede. De två betalningsbladen sätter den notariella överlåtelsen 60 eller 90 dagar efter bokningen, dossiern från juni 2026 visar fotografier av färdiga hus och prislistan markerar två bostäder som möblerade visningsbostäder, så vissa bostäder kan vara färdiga. Nueva Living frågar vilka bostäder som är färdiga och begär tillstånden och tillträdesdatumet skriftligen innan ni förbinder er.')
a('.constructionTimeline.paymentTerms[0][0]',
  'Reserva, Fase I y bloques 5 y 6', 'Réservation, phase I et blocs 5 et 6', 'Reservierung, Phase I und Blöcke 5 und 6', 'Бронирование, очередь I и блоки 5 и 6',
  'الحجز، المرحلة الأولى والمبنيان 5 و6', 'Reservering, fase I en blokken 5 en 6', 'Rezerwacja, etap I i budynki 5 i 6', 'Reservasjon, fase I og blokk 5 og 6', 'Bokning, fas I och hus 5 och 6')
a('.constructionTimeline.paymentTerms[0][2]',
  '{E11000} a la firma', '{E11000} à la signature', '{E11000} bei Unterzeichnung', '{E11000} при подписании', '{E11000} عند التوقيع', '{E11000} bij ondertekening', '{E11000} przy podpisaniu', '{E11000} ved signering', '{E11000} vid undertecknandet') if False else None
T[proj['constructionTimeline']['paymentTerms'][0][2]] = {l: v for l, v in zip(LOCS, [
    expand(x, l) for l, x in zip(LOCS, ['{E11000} a la firma', '{E11000} à la signature', '{E11000} bei Unterzeichnung', '{E11000} при подписании',
                                        '{E11000} عند التوقيع', '{E11000} bij ondertekening', '{E11000} przy podpisaniu', '{E11000} ved signering',
                                        '{E11000} vid undertecknandet'])])}
a('.constructionTimeline.paymentTerms[1][0]',
  'Escritura, Fase I y bloques 5 y 6', 'Acte authentique, phase I et blocs 5 et 6', 'Beurkundung, Phase I und Blöcke 5 und 6', 'Нотариальный акт, очередь I и блоки 5 и 6',
  'سند الملكية، المرحلة الأولى والمبنيان 5 و6', 'Notariële akte, fase I en blokken 5 en 6', 'Akt notarialny, etap I i budynki 5 i 6', 'Skjøte, fase I og blokk 5 og 6', 'Notarieakt, fas I och hus 5 och 6')
a('.constructionTimeline.paymentTerms[1][1]',
  'Saldo + IVA', 'Solde + TVA', 'Restbetrag + MwSt.', 'Остаток + НДС', 'الرصيد + ضريبة القيمة المضافة', 'Restant + btw', 'Reszta + VAT', 'Restbeløp + mva', 'Restbelopp + IVA')
a('.constructionTimeline.paymentTerms[1][2]',
  'El precio más el IVA, menos la reserva, como máximo 90 días tras la reserva',
  'Le prix plus la TVA, moins la réservation, au plus 90 jours après la réservation',
  'Der Preis zuzüglich MwSt., abzüglich der Reservierung, spätestens 90 Tage nach der Reservierung',
  'Цена плюс НДС за вычетом бронирования, не позднее 90 дней после бронирования',
  'السعر زائد ضريبة القيمة المضافة مطروحًا منه الحجز، بحد أقصى 90 يومًا بعد الحجز',
  'De prijs plus btw, min de reservering, uiterlijk 90 dagen na de reservering',
  'Cena plus VAT, pomniejszona o rezerwację, najpóźniej 90 dni po rezerwacji',
  'Prisen pluss mva, minus reservasjonen, senest 90 dager etter reservasjonen',
  'Priset plus IVA, minus bokningen, senast 90 dagar efter bokningen')
a('.constructionTimeline.paymentTerms[2][0]',
  'Reserva, condiciones generales', 'Réservation, conditions générales', 'Reservierung, allgemeine Bedingungen', 'Бронирование, общие условия',
  'الحجز، الشروط العامة', 'Reservering, algemene voorwaarden', 'Rezerwacja, warunki ogólne', 'Reservasjon, generelle vilkår', 'Bokning, allmänna villkor')
T[proj['constructionTimeline']['paymentTerms'][2][1]] = {l: expand(x, l) for l, x in zip(LOCS, [
    '{E30000} + IVA', '{E30000} + TVA', '{E30000} + MwSt.', '{E30000} + НДС', '{E30000} + ضريبة القيمة المضافة', '{E30000} + btw', '{E30000} + VAT', '{E30000} + mva', '{E30000} + IVA'])}
T[proj['constructionTimeline']['paymentTerms'][2][2]] = {l: expand(x, l) for l, x in zip(LOCS, [
    '{E33000} a la firma', '{E33000} à la signature', '{E33000} bei Unterzeichnung', '{E33000} при подписании', '{E33000} عند التوقيع',
    '{E33000} bij ondertekening', '{E33000} przy podpisaniu', '{E33000} ved signering', '{E33000} vid undertecknandet'])}
a('.constructionTimeline.paymentTerms[3][0]',
  'Escritura, condiciones generales', 'Acte authentique, conditions générales', 'Beurkundung, allgemeine Bedingungen', 'Нотариальный акт, общие условия',
  'سند الملكية، الشروط العامة', 'Notariële akte, algemene voorwaarden', 'Akt notarialny, warunki ogólne', 'Skjøte, generelle vilkår', 'Notarieakt, allmänna villkor')
a('.constructionTimeline.paymentTerms[3][2]',
  'El precio más el IVA, menos la reserva, a la finalización y entrega de llaves, como máximo 60 días tras la reserva',
  'Le prix plus la TVA, moins la réservation, à l’achèvement et à la remise des clés, au plus 60 jours après la réservation',
  'Der Preis zuzüglich MwSt., abzüglich der Reservierung, bei Fertigstellung und Schlüsselübergabe, spätestens 60 Tage nach der Reservierung',
  'Цена плюс НДС за вычетом бронирования, при завершении строительства и передаче ключей, не позднее 60 дней после бронирования',
  'السعر زائد ضريبة القيمة المضافة مطروحًا منه الحجز، عند الإنجاز وتسليم المفاتيح، بحد أقصى 60 يومًا بعد الحجز',
  'De prijs plus btw, min de reservering, bij oplevering en sleuteloverdracht, uiterlijk 60 dagen na de reservering',
  'Cena plus VAT, pomniejszona o rezerwację, przy ukończeniu i wydaniu kluczy, najpóźniej 60 dni po rezerwacji',
  'Prisen pluss mva, minus reservasjonen, ved ferdigstillelse og nøkkeloverlevering, senest 60 dager etter reservasjonen',
  'Priset plus IVA, minus bokningen, vid färdigställande och nyckelöverlämning, senast 60 dagar efter bokningen')
# the first payment row's amount is already in the memory, but with another word for the tax in Arabic
T[proj['constructionTimeline']['paymentTerms'][0][1]] = {l: expand(x, l) for l, x in zip(LOCS, [
    '{E10000} + IVA', '{E10000} + TVA', '{E10000} + MwSt.', '{E10000} + НДС', '{E10000} + ضريبة القيمة المضافة', '{E10000} + btw', '{E10000} + VAT', '{E10000} + mva', '{E10000} + IVA'])}
a('.constructionTimeline.paymentTermsNote',
  'El promotor emite dos hojas de condiciones de pago. Una lleva el título Fase I y bloques 5 y 6; la otra no tiene título de fase. La lista de precios sitúa la 20B en la fase 1 y la 61B y la 62B en el bloque 6, y las hojas no dicen cuál se aplica a cada una de las demás viviendas, por lo que Nueva Living confirma por escrito la hoja que corresponde a la vivienda que usted elija. Ninguna de las hojas muestra pagos fraccionados entre la reserva y la escritura. Nueva Living confirma las condiciones exactas en el contrato de reserva antes de que usted se comprometa.',
  'Le promoteur émet deux feuilles de conditions de paiement. L’une est intitulée Phase I et blocs 5 et 6 ; l’autre ne porte aucun intitulé de phase. La liste de prix place le 20B en phase 1 et le 61B et le 62B dans le bloc 6, et les feuilles ne disent pas laquelle s’applique à chacun des autres logements ; Nueva Living confirme donc par écrit la feuille qui correspond au logement que vous choisissez. Aucune des feuilles ne montre de versements échelonnés entre la réservation et l’acte. Nueva Living confirme les conditions exactes dans le contrat de réservation avant que vous vous engagiez.',
  'Der Bauträger gibt zwei Zahlungsblätter heraus. Eines trägt die Überschrift Phase I und Blöcke 5 und 6; das andere hat keine Phasenüberschrift. Die Preisliste ordnet 20B der Phase 1 und 61B und 62B dem Block 6 zu, und die Blätter sagen nicht, welches für jede andere Wohnung gilt; Nueva Living bestätigt daher schriftlich das Blatt für die von Ihnen gewählte Wohnung. Keines der Blätter zeigt Raten zwischen Reservierung und Beurkundung. Nueva Living bestätigt die genauen Bedingungen im Reservierungsvertrag, bevor Sie sich binden.',
  'Застройщик выпускает два листа условий оплаты. Один озаглавлен «очередь I и блоки 5 и 6», у другого заголовка очереди нет. Прайс-лист относит 20B к очереди 1, а 61B и 62B — к блоку 6, а какой лист действует для каждой из остальных квартир, листы не говорят, поэтому Nueva Living письменно подтверждает лист для выбранной вами квартиры. Ни в одном из листов нет платежей в рассрочку между бронированием и нотариальным актом. Nueva Living подтверждает точные условия в договоре бронирования, прежде чем вы примете обязательства.',
  'يُصدر المطوّر ورقتين لشروط الدفع. إحداهما بعنوان المرحلة الأولى والمبنيان 5 و6، والأخرى بلا عنوان مرحلة. تضع قائمة الأسعار 20B في المرحلة 1 و61B و62B في المبنى 6، ولا تذكر الورقتان أيهما تنطبق على كل مسكن آخر، لذا تؤكد نويفا ليفينغ كتابةً الورقة الخاصة بالمسكن الذي تختاره. ولا تُظهر أي من الورقتين دفعات مجزّأة بين الحجز وسند الملكية. تؤكد نويفا ليفينغ الشروط الدقيقة في اتفاقية الحجز قبل أن تلتزم.',
  'De ontwikkelaar geeft twee betalingsbladen uit. Eén draagt de kop Fase I en blokken 5 en 6; het andere heeft geen fasekop. De prijslijst plaatst 20B in fase 1 en 61B en 62B in blok 6, en de bladen zeggen niet welk blad voor elke andere woning geldt; Nueva Living bevestigt daarom schriftelijk het blad voor de woning die u kiest. Geen van de bladen toont termijnen tussen reservering en akte. Nueva Living bevestigt de exacte voorwaarden in de reserveringsovereenkomst voordat u zich bindt.',
  'Deweloper wydaje dwa arkusze warunków płatności. Jeden nosi tytuł Etap I i budynki 5 i 6; drugi nie ma tytułu etapu. Cennik umieszcza 20B w etapie 1, a 61B i 62B w budynku 6, a arkusze nie mówią, który dotyczy każdego z pozostałych lokali, dlatego Nueva Living potwierdza na piśmie arkusz właściwy dla wybranego przez Państwa lokalu. Żaden z arkuszy nie pokazuje rat między rezerwacją a aktem. Nueva Living potwierdza dokładne warunki w umowie rezerwacyjnej, zanim Państwo się zobowiążą.',
  'Utbyggeren utsteder to betalingsark. Det ene har overskriften Fase I og blokk 5 og 6; det andre har ingen faseoverskrift. Prislisten plasserer 20B i fase 1 og 61B og 62B i blokk 6, og arkene sier ikke hvilket som gjelder for hver av de andre boligene, så Nueva Living bekrefter skriftlig arket for boligen De velger. Ingen av arkene viser delbetalinger mellom reservasjon og skjøte. Nueva Living bekrefter de nøyaktige vilkårene i reservasjonsavtalen før De forplikter dere.',
  'Exploatören utfärdar två betalningsblad. Det ena har rubriken Fas I och hus 5 och 6; det andra har ingen fasrubrik. Prislistan placerar 20B i fas 1 och 61B och 62B i hus 6, och bladen anger inte vilket som gäller för var och en av de andra bostäderna, så Nueva Living bekräftar skriftligen bladet för den bostad ni väljer. Inget av bladen visar delbetalningar mellan bokning och notarieakt. Nueva Living bekräftar de exakta villkoren i bokningsavtalet innan ni förbinder er.')

# ---- why, investment, trust ----------------------------------------------------------------------

a('.why.copy',
  'Un camino corto de la reserva a la escritura y un conjunto de instalaciones de estilo resort dentro de la promoción.',
  'Un chemin court de la réservation à l’acte et un ensemble d’équipements de style resort au sein du programme.',
  'Ein kurzer Weg von der Reservierung zur Beurkundung und Resort-Einrichtungen innerhalb der Anlage.',
  'Короткий путь от бронирования до нотариального акта и набор удобств в стиле курорта внутри комплекса.',
  'طريق قصير من الحجز إلى سند الملكية ومرافق بأسلوب المنتجعات داخل المشروع.',
  'Een korte weg van reservering naar akte en een resortachtig aanbod aan voorzieningen binnen het complex.',
  'Krótka droga od rezerwacji do aktu i zestaw udogodnień w stylu kurortu na terenie inwestycji.',
  'En kort vei fra reservasjon til skjøte og et resortpreget tilbud av fasiliteter i anlegget.',
  'En kort väg från bokning till notarieakt och en resortliknande uppsättning faciliteter inom området.')
a('.why.points[0][0]',
  'Un camino corto hasta la escritura', 'Un chemin court jusqu’à l’acte', 'Ein kurzer Weg zur Beurkundung', 'Короткий путь к нотариальному акту',
  'طريق قصير إلى سند الملكية', 'Een korte weg naar de akte', 'Krótka droga do aktu', 'En kort vei til skjøtet', 'En kort väg till notarieakten')
a('.why.points[0][1]',
  'Las dos hojas de condiciones de pago piden el saldo en la escritura, 60 o 90 días después de la reserva, sin pagos intermedios.',
  'Les deux feuilles de conditions de paiement demandent le solde à l’acte, 60 ou 90 jours après la réservation, sans versement intermédiaire.',
  'Beide Zahlungsblätter verlangen den Restbetrag bei der Beurkundung, 60 oder 90 Tage nach der Reservierung, ohne Raten dazwischen.',
  'Оба листа условий оплаты требуют остаток при нотариальном акте, через 60 или 90 дней после бронирования, без промежуточных платежей.',
  'تطلب ورقتا شروط الدفع كلتاهما الرصيد عند سند الملكية بعد 60 أو 90 يومًا من الحجز، دون دفعات وسيطة.',
  'Beide betalingsbladen vragen het restant bij de akte, 60 of 90 dagen na de reservering, zonder termijnen ertussen.',
  'Oba arkusze warunków płatności wymagają reszty ceny przy akcie, 60 lub 90 dni po rezerwacji, bez rat pośrednich.',
  'Begge betalingsarkene ber om restbeløpet ved skjøtet, 60 eller 90 dager etter reservasjonen, uten delbetalinger imellom.',
  'Båda betalningsbladen begär restbeloppet vid notarieakten, 60 eller 90 dagar efter bokningen, utan delbetalningar emellan.')
a('.why.points[1][0]',
  'Áticos con solárium privado', 'Des penthouses avec solarium privé', 'Penthäuser mit privatem Solarium', 'Пентхаусы с частным солярием',
  'بنتهاوس بسولاريوم خاص', 'Penthouses met privésolarium', 'Penthouse’y z prywatnym solarium', 'Toppleiligheter med privat solterrasse', 'Takvåningar med privat solterrass')
a('.why.points[1][1]',
  'Cada ático de la lista tiene un solárium de {N49.60} a {N71.20} {U} sobre su terraza, con el mar en el horizonte en las fotografías del promotor.',
  'Chaque penthouse de la liste a un solarium de {N49.60} à {N71.20} {U} au-dessus de sa terrasse, avec la mer à l’horizon sur les photographies du promoteur.',
  'Jedes Penthouse der Liste hat über seiner Terrasse ein Solarium von {N49.60} bis {N71.20} {U}, auf den Fotos des Bauträgers mit dem Meer am Horizont.',
  'У каждого пентхауса в списке над террасой есть солярий от {N49.60} до {N71.20} {U}; на фотографиях застройщика на горизонте видно море.',
  'لكل بنتهاوس في القائمة سولاريوم من {N49.60} إلى {N71.20} {U} فوق تراسه، والبحر في الأفق في صور المطوّر.',
  'Elk penthouse op de lijst heeft boven het terras een solarium van {N49.60} tot {N71.20} {U}, met de zee aan de horizon op de foto’s van de ontwikkelaar.',
  'Każdy penthouse na liście ma nad tarasem solarium od {N49.60} do {N71.20} {U}, z morzem na horyzoncie na zdjęciach dewelopera.',
  'Hver toppleilighet på listen har en solterrasse på {N49.60} til {N71.20} {U} over terrassen, med havet i horisonten på utbyggerens fotografier.',
  'Varje takvåning på listan har en solterrass på {N49.60} till {N71.20} {U} ovanpå terrassen, med havet i horisonten på exploatörens fotografier.')
a('.why.points[2][0]',
  'Tres piscinas, un spa y dos gimnasios', 'Trois piscines, un spa et deux salles de sport', 'Drei Pools, ein Spa und zwei Fitnessräume', 'Три бассейна, спа и два спортзала',
  'ثلاثة مسابح وسبا وصالتان رياضيتان', 'Drie zwembaden, een spa en twee fitnessruimtes', 'Trzy baseny, spa i dwie siłownie', 'Tre basseng, et spa og to treningsrom', 'Tre pooler, ett spa och två gym')
a('.why.points[2][1]',
  'El dosier de junio de 2026 describe tres piscinas comunitarias, un spa de más de {N200} {U}, dos gimnasios, una sala de coworking y un club social.',
  'Le dossier de juin 2026 décrit trois piscines communes, un spa de plus de {N200} {U}, deux salles de sport, un espace de coworking et un club social.',
  'Das Dossier vom Juni 2026 beschreibt drei Gemeinschaftspools, ein Spa von mehr als {N200} {U}, zwei Fitnessräume, einen Coworking-Raum und einen Social Club.',
  'В досье июня 2026 года описаны три общих бассейна, спа площадью более {N200} {U}, два спортзала, коворкинг и общественный клуб.',
  'يصف ملف يونيو 2026 ثلاثة مسابح مشتركة وسبا تتجاوز مساحته {N200} {U} وصالتين رياضيتين وغرفة عمل مشترك ونادياً اجتماعياً.',
  'Het dossier van juni 2026 beschrijft drie gemeenschappelijke zwembaden, een spa van meer dan {N200} {U}, twee fitnessruimtes, een coworkingruimte en een sociale club.',
  'Materiał z czerwca 2026 roku opisuje trzy wspólne baseny, spa o powierzchni ponad {N200} {U}, dwie siłownie, salę coworkingową i klub mieszkańców.',
  'Dossieret fra juni 2026 beskriver tre fellesbasseng, et spa på mer enn {N200} {U}, to treningsrom, et coworking-rom og en sosialklubb.',
  'Dossiern från juni 2026 beskriver tre gemensamma pooler, ett spa på mer än {N200} {U}, två gym, ett coworkingrum och en social klubb.')
a('.why.points[3][0]',
  'Sus acabados, su elección', 'Vos finitions, votre choix', 'Ihre Ausstattung, Ihre Wahl', 'Ваша отделка — ваш выбор',
  'تشطيباتك، خيارك', 'Uw afwerking, uw keuze', 'Państwa wykończenie, Państwa wybór', 'Dine overflater, ditt valg', 'Era ytskikt, ert val') if False else None
T[proj['why']['points'][3][0]] = {l: v for l, v in zip(LOCS, [
    'Sus acabados, su elección', 'Vos finitions, votre choix', 'Ihre Ausstattung, Ihre Wahl', 'Ваша отделка — ваш выбор',
    'تشطيباتك باختيارك', 'Uw afwerking, uw keuze', 'Wykończenie według Państwa wyboru', 'Overflatene velger De selv', 'Ytskikten väljer ni själva'])}
a('.why.points[3][1]',
  'El dosier de 2022 dice que los revestimientos de paredes y suelos pueden elegirse de un catálogo sin coste adicional.',
  'Le dossier de 2022 indique que les revêtements des murs et des sols peuvent être choisis dans un catalogue sans supplément.',
  'Das Dossier von 2022 sagt, dass Wand- und Bodenbeläge ohne Aufpreis aus einem Katalog gewählt werden können.',
  'В досье 2022 года сказано, что отделку стен и полов можно выбрать из каталога без доплаты.',
  'يذكر ملف عام 2022 أن كسوة الجدران والأرضيات يمكن اختيارها من كتالوج دون تكلفة إضافية.',
  'Het dossier van 2022 zegt dat wand- en vloerafwerkingen zonder meerprijs uit een catalogus kunnen worden gekozen.',
  'Materiał z 2022 roku podaje, że wykończenia ścian i podłóg można wybrać z katalogu bez dopłaty.',
  'Dossieret fra 2022 sier at vegg- og gulvbelegg kan velges fra en katalog uten tillegg.',
  'Dossiern från 2022 säger att vägg- och golvbeklädnad kan väljas ur en katalog utan extra kostnad.')
a('.investment.cards[0][1]',
  'La lista de precios se expresa antes de IVA. El IVA del diez por ciento y el impuesto de actos jurídicos documentados del 1,20 por ciento suman unos sesenta y cuatro mil euros al apartamento más barato y ciento cincuenta y cuatro mil al ático más caro, antes de notaría y registro.',
  'La liste de prix s’entend hors TVA. La TVA à dix pour cent et le droit de timbre à 1,20 pour cent ajoutent environ soixante-quatre mille euros à l’appartement le moins cher et cent cinquante-quatre mille au penthouse le plus cher, avant frais de notaire et d’enregistrement.',
  'Die Preisliste versteht sich ohne MwSt. Zehn Prozent Mehrwertsteuer und 1,20 Prozent Stempelsteuer kommen bei der günstigsten Wohnung auf rund vierundsechzigtausend Euro und beim teuersten Penthouse auf hundertvierundfünfzigtausend, vor Notar- und Grundbuchkosten.',
  'Прайс-лист указан без НДС. НДС десять процентов и гербовый сбор 1,20 процента добавляют около шестидесяти четырёх тысяч евро к самой дешёвой квартире и сто пятьдесят четыре тысячи к самому дорогому пентхаусу, до нотариуса и регистрации.',
  'قائمة الأسعار قبل ضريبة القيمة المضافة. تضيف ضريبة القيمة المضافة بنسبة عشرة بالمئة ورسم الدمغة بنسبة 1.20 بالمئة نحو أربعة وستين ألف يورو إلى أرخص شقة ومئة وأربعة وخمسين ألفًا إلى أغلى بنتهاوس، قبل أتعاب التوثيق والتسجيل.',
  'De prijslijst is exclusief btw. Tien procent btw en 1,20 procent overdrachtsbelasting leggen ongeveer vierenzestigduizend euro bij op het goedkoopste appartement en honderdvierenvijftigduizend op het duurste penthouse, vóór notaris- en kadasterkosten.',
  'Cennik podano przed doliczeniem VAT. Dziesięcioprocentowy VAT i 1,20-procentowy podatek od czynności cywilnoprawnych dokładają około sześćdziesięciu czterech tysięcy euro do najtańszego apartamentu i sto pięćdziesiąt cztery tysiące do najdroższego penthouse’u, przed opłatami notarialnymi i wieczystoksięgowymi.',
  'Prislisten er oppgitt før mva. Ti prosent merverdiavgift og 1,20 prosent dokumentavgift legger rundt sekstifire tusen euro på den rimeligste leiligheten og hundre og femtifire tusen på den dyreste toppleiligheten, før notar- og tinglysingsgebyrer.',
  'Prislistan anges före IVA. Tio procents IVA och 1,20 procents stämpelskatt lägger cirka sextiofyratusen euro på den billigaste lägenheten och hundrafemtiofyra tusen på den dyraste takvåningen, före notarie- och registreringsavgifter.')
a('.investment.cards[1][0]',
  'No se indica fecha de entrega', 'Aucune date de livraison n’est indiquée', 'Kein Fertigstellungstermin angegeben', 'Срок сдачи не указан',
  'لا يُذكر موعد تسليم', 'Geen opleverdatum vermeld', 'Brak podanego terminu odbioru', 'Ingen ferdigstillelsesdato er oppgitt', 'Inget tillträdesdatum anges')
a('.investment.cards[1][1]',
  'Los documentos no dan ninguna. Pregunte qué viviendas están terminadas, qué dice el contrato sobre la fecha de entrega y qué ocurre si se retrasa.',
  'Les documents n’en donnent aucune. Demandez quels logements sont achevés, ce que dit le contrat sur la date de livraison et ce qui se passe en cas de retard.',
  'Die Unterlagen nennen keinen. Fragen Sie, welche Wohnungen fertig sind, was der Vertrag zum Fertigstellungstermin sagt und was bei einer Verzögerung geschieht.',
  'В документах его нет. Спросите, какие квартиры готовы, что говорит договор о сроке сдачи и что будет при задержке.',
  'لا تذكر الوثائق أي موعد. اسأل عن المساكن المنجزة وعمّا يقوله العقد بشأن موعد التسليم وما يحدث إذا تأخر.',
  'De documenten geven er geen. Vraag welke woningen klaar zijn, wat het contract zegt over de opleverdatum en wat er gebeurt als die verschuift.',
  'Dokumenty go nie podają. Warto zapytać, które lokale są ukończone, co umowa mówi o terminie odbioru i co się dzieje w razie opóźnienia.',
  'Dokumentene oppgir ingen. Spør hvilke boliger som er ferdige, hva kontrakten sier om ferdigstillelsesdatoen og hva som skjer hvis den forskyves.',
  'Dokumenten anger inget. Fråga vilka bostäder som är färdiga, vad avtalet säger om tillträdesdatumet och vad som händer om det försenas.')
a('.investment.cards[2][0]',
  'Dos hojas de condiciones de pago', 'Deux feuilles de conditions de paiement', 'Zwei Blätter mit Zahlungsbedingungen', 'Два листа условий оплаты',
  'ورقتان لشروط الدفع', 'Twee bladen met betalingsvoorwaarden', 'Dwa arkusze warunków płatności', 'To ark med betalingsvilkår', 'Två blad med betalningsvillkor')
a('.investment.cards[2][1]',
  'Una reserva de {E10000} se aplica a un conjunto de viviendas y {E30000} al otro. La hoja que se aplique a su vivienda decide cuánto entrega y de cuánto tiempo dispone hasta la escritura.',
  'Une réservation de {E10000} s’applique à un groupe de logements et {E30000} à l’autre. La feuille qui s’applique à votre logement détermine la somme que vous versez et le délai dont vous disposez avant l’acte.',
  'Eine Reservierung von {E10000} gilt für eine Gruppe von Wohnungen, {E30000} für die andere. Welches Blatt für Ihre Wohnung gilt, entscheidet, wie viel Sie anzahlen und wie viel Zeit Sie bis zur Beurkundung haben.',
  'Бронирование в {E10000} относится к одной группе квартир, а {E30000} — к другой. Какой лист действует для вашей квартиры, определяет, сколько вы внесёте и сколько времени у вас до нотариального акта.',
  'ينطبق حجز بقيمة {E10000} على مجموعة من المساكن و{E30000} على المجموعة الأخرى. والورقة المنطبقة على مسكنك هي التي تحدد كم تدفع وكم من الوقت لديك حتى سند الملكية.',
  'Een reservering van {E10000} geldt voor de ene groep woningen en {E30000} voor de andere. Welk blad voor uw woning geldt, bepaalt hoeveel u vooraf betaalt en hoeveel tijd u hebt tot de akte.',
  'Rezerwacja w wysokości {E10000} dotyczy jednej grupy lokali, a {E30000} drugiej. To, który arkusz dotyczy Państwa lokalu, decyduje o tym, ile wpłacają Państwo z góry i ile mają czasu do aktu.',
  'En reservasjon på {E10000} gjelder for den ene gruppen boliger og {E30000} for den andre. Hvilket ark som gjelder for boligen din avgjør hvor mye du betaler først og hvor lang tid du har til skjøtet.',
  'En bokning på {E10000} gäller för den ena gruppen bostäder och {E30000} för den andra. Vilket blad som gäller för er bostad avgör hur mycket ni betalar först och hur lång tid ni har till notarieakten.')
a('.investment.cards[3][0]',
  'La lista de precios caduca pronto', 'La liste de prix a une courte durée de vie', 'Die Preisliste ist kurzlebig', 'Прайс-лист быстро устаревает',
  'قائمة الأسعار قصيرة الأجل', 'De prijslijst is van korte duur', 'Cennik szybko traci ważność', 'Prislisten er kortlivet', 'Prislistan är kortlivad')
a('.investment.cards[3][1]',
  'La lista dice que es válida durante dos días desde su descarga. Los precios pueden cambiar y las viviendas pasar a reservadas o vendidas, por lo que reconfirmamos antes de que usted se comprometa.',
  'La liste indique qu’elle est valable deux jours à compter de son téléchargement. Les prix peuvent changer et les logements passer à réservé ou vendu ; nous reconfirmons donc avant votre engagement.',
  'Die Liste sagt, dass sie zwei Tage ab dem Herunterladen gültig ist. Preise können sich ändern und Wohnungen auf reserviert oder verkauft wechseln, daher bestätigen wir erneut, bevor Sie sich binden.',
  'В списке сказано, что он действителен два дня с момента скачивания. Цены могут измениться, а квартиры — перейти в статус забронированных или проданных, поэтому мы подтверждаем данные повторно, прежде чем вы примете обязательства.',
  'تذكر القائمة أنها صالحة لمدة يومين من تنزيلها. قد تتغيّر الأسعار وقد تتحوّل المساكن إلى محجوزة أو مباعة، لذا نعيد التأكيد قبل أن تلتزم.',
  'De lijst zegt dat ze twee dagen na het downloaden geldig is. Prijzen kunnen veranderen en woningen kunnen gereserveerd of verkocht raken, dus we bevestigen opnieuw voordat u zich bindt.',
  'Lista podaje, że jest ważna dwa dni od pobrania. Ceny mogą się zmienić, a lokale przejść do statusu zarezerwowanych lub sprzedanych, dlatego potwierdzamy dane ponownie, zanim Państwo się zobowiążą.',
  'Listen oppgir at den gjelder i to dager fra nedlasting. Prisene kan endre seg og boliger kan bli reservert eller solgt, så vi bekrefter på nytt før De forplikter dere.',
  'Listan anger att den gäller i två dagar från nedladdningen. Priserna kan ändras och bostäder kan bli reserverade eller sålda, så vi bekräftar på nytt innan ni förbinder er.')
a('.trustDossier.cards[0][0]',
  'Las licencias', 'Les licences', 'Die Genehmigungen', 'Разрешения', 'التراخيص', 'De vergunningen', 'Pozwolenia', 'Tillatelsene', 'Tillstånden')
a('.trustDossier.cards[0][1]',
  'Los documentos no indican licencia de obra, licencia de primera ocupación ni fecha de entrega. Las pedimos por escrito.',
  'Les documents n’indiquent ni permis de construire, ni licence de première occupation, ni date de livraison. Nous les demandons par écrit.',
  'Die Unterlagen nennen weder eine Baugenehmigung noch eine Erstbezugsgenehmigung noch einen Fertigstellungstermin. Wir fordern sie schriftlich an.',
  'В документах не указаны ни разрешение на строительство, ни лицензия на первое заселение, ни срок сдачи. Мы запрашиваем их в письменном виде.',
  'لا تذكر الوثائق رخصة بناء ولا رخصة أول إشغال ولا موعد تسليم. نطلبها كتابةً.',
  'De documenten vermelden geen bouwvergunning, geen vergunning voor eerste ingebruikname en geen opleverdatum. Wij vragen ze schriftelijk op.',
  'Dokumenty nie podają pozwolenia na budowę, pozwolenia na pierwsze zasiedlenie ani terminu odbioru. Prosimy o nie na piśmie.',
  'Dokumentene oppgir verken byggetillatelse, tillatelse for første bruk eller ferdigstillelsesdato. Vi ber skriftlig om dem.',
  'Dokumenten anger varken bygglov, tillstånd för första ibruktagande eller tillträdesdatum. Vi begär dem skriftligen.')
a('.trustDossier.cards[1][1]',
  'Las hojas de condiciones de pago no dicen nada sobre cómo se custodia o protege la reserva. Lo pedimos en el contrato de reserva.',
  'Les feuilles de conditions de paiement ne disent rien sur la manière dont la réservation est conservée ou protégée. Nous le demandons dans le contrat de réservation.',
  'Die Zahlungsblätter sagen nichts darüber, wie die Reservierung verwahrt oder abgesichert wird. Wir verlangen das im Reservierungsvertrag.',
  'В листах условий оплаты ничего не сказано о том, как хранится и чем защищено бронирование. Мы запрашиваем это в договоре бронирования.',
  'لا تقول ورقتا شروط الدفع شيئًا عن كيفية حفظ مبلغ الحجز أو حمايته. نطلب ذلك في اتفاقية الحجز.',
  'De betalingsbladen zeggen niets over hoe de reservering wordt bewaard of beschermd. Wij vragen dat in de reserveringsovereenkomst.',
  'Arkusze warunków płatności nic nie mówią o tym, jak przechowywana lub chroniona jest rezerwacja. Prosimy o to w umowie rezerwacyjnej.',
  'Betalingsarkene sier ingenting om hvordan reservasjonen oppbevares eller beskyttes. Vi ber om det i reservasjonsavtalen.',
  'Betalningsbladen säger inget om hur bokningen förvaras eller skyddas. Vi begär det i bokningsavtalet.')
a('.trustDossier.cards[2][1]',
  'Las superficies y los precios están transcritos de la lista de precios del 3 de noviembre de 2026. Cuando un plano difiere, como en la 62B y la 72B, la tabla sigue la lista y lo indica. No hay plano de la 12A, la 61B ni la 102A.',
  'Les surfaces et les prix sont transcrits de la liste de prix du 3 novembre 2026. Lorsqu’un plan diffère, comme pour le 62B et le 72B, le tableau suit la liste et le signale. Il n’y a pas de plan pour le 12A, le 61B ni le 102A.',
  'Flächen und Preise sind der Preisliste vom 3. November 2026 entnommen. Weicht ein Plan ab, wie bei 62B und 72B, folgt die Tabelle der Liste und sagt es. Für 12A, 61B und 102A gibt es keinen Plan.',
  'Площади и цены перенесены из прайс-листа от 3 ноября 2026 года. Если планировка расходится со списком, как для 62B и 72B, таблица следует списку и сообщает об этом. Планировок для 12A, 61B и 102A нет.',
  'المساحات والأسعار منقولة من قائمة الأسعار بتاريخ 3 نوفمبر 2026. وحيث يختلف مخطط، كما في 62B و72B، يتبع الجدول القائمة ويذكر ذلك. ولا يوجد مخطط لـ 12A و61B و102A.',
  'Oppervlakten en prijzen zijn overgenomen uit de prijslijst van 3 november 2026. Waar een plattegrond afwijkt, zoals bij 62B en 72B, volgt de tabel de lijst en zegt dat erbij. Voor 12A, 61B en 102A is er geen plattegrond.',
  'Powierzchnie i ceny są przepisane z cennika z 3 listopada 2026. Gdy rzut się różni, jak w 62B i 72B, tabela idzie za listą i to zaznacza. Dla 12A, 61B i 102A nie ma rzutu.',
  'Arealer og priser er overført fra prislisten av 3. november 2026. Der en plantegning avviker, som for 62B og 72B, følger tabellen listen og sier fra om det. Det finnes ingen plantegning for 12A, 61B og 102A.',
  'Ytor och priser är överförda från prislistan av 3 november 2026. Där en planritning avviker, som för 62B och 72B, följer tabellen listan och säger det. Det finns ingen planritning för 12A, 61B och 102A.')
a('.trustDossier.cards[3][0]',
  'Qué incluye el ático', 'Ce que comprend le penthouse', 'Was das Penthouse enthält', 'Что входит в пентхаус', 'ما يشمله البنتهاوس', 'Wat het penthouse omvat', 'Co obejmuje penthouse', 'Hva toppleiligheten omfatter', 'Vad takvåningen omfattar')
a('.trustDossier.cards[3][1]',
  'El dosier de junio de 2026 muestra un jacuzzi en el solárium, mientras que las hojas de planos llaman a la piscina del solárium una opción con coste adicional. Preguntamos qué incluye cada precio.',
  'Le dossier de juin 2026 montre un jacuzzi sur le solarium, alors que les planches de plans qualifient le bassin du solarium d’option payante. Nous demandons ce que comprend chaque prix.',
  'Das Dossier vom Juni 2026 zeigt einen Whirlpool auf dem Solarium, während die Planblätter den Solarium-Pool als Option gegen Aufpreis bezeichnen. Wir fragen nach, was in jedem Preis enthalten ist.',
  'В досье июня 2026 года на солярии показано джакузи, а в планировочных листах бассейн на солярии назван опцией за доплату. Мы выясняем, что входит в каждую цену.',
  'يعرض ملف يونيو 2026 جاكوزي على السولاريوم، بينما تصف أوراق المخططات مسبح السولاريوم بأنه خيار بتكلفة إضافية. نسأل عمّا يشمله كل سعر.',
  'Het dossier van juni 2026 toont een jacuzzi op het solarium, terwijl de plattegrondbladen het solariumzwembad een optie tegen meerprijs noemen. Wij vragen wat in elke prijs zit.',
  'Materiał z czerwca 2026 roku pokazuje jacuzzi na solarium, podczas gdy arkusze rzutów nazywają basen na solarium opcją za dopłatą. Pytamy, co obejmuje każda cena.',
  'Dossieret fra juni 2026 viser en jacuzzi på solterrassen, mens plantegningsarkene kaller bassenget på solterrassen et tilvalg mot tillegg. Vi spør hva hver pris omfatter.',
  'Dossiern från juni 2026 visar ett badkar med bubbelfunktion på solterrassen, medan planritningsbladen kallar poolen på solterrassen ett tillval mot extra kostnad. Vi frågar vad varje pris omfattar.')

# ---- architecture, lifestyle ---------------------------------------------------------------------

a('.architecture.headlineHtml',
  'Doce bloques, <em>tres alturas como máximo</em>', 'Douze blocs, <em>trois niveaux au plus</em>', 'Zwölf Blöcke, <em>höchstens drei Geschosse</em>', 'Двенадцать корпусов, <em>не выше трёх этажей</em>',
  'اثنا عشر مبنى، <em>بثلاثة طوابق كحد أقصى</em>', 'Twaalf blokken, <em>hooguit drie bouwlagen</em>', 'Dwanaście budynków, <em>najwyżej trzy kondygnacje</em>', 'Tolv blokker, <em>høyst tre etasjer</em>', 'Tolv hus, <em>högst tre våningar</em>')
a('.architecture.copy[0]',
  'El dosier de 2022 describe 96 viviendas en 12 bloques de tres alturas como máximo: viviendas en planta baja, viviendas en planta primera con grandes terrazas y áticos con solárium.',
  'Le dossier de 2022 décrit 96 logements répartis en 12 blocs de trois niveaux au plus : des logements au rez-de-chaussée, des logements au premier étage avec de grandes terrasses et des penthouses avec solarium.',
  'Das Dossier von 2022 beschreibt 96 Wohnungen in 12 Blöcken mit höchstens drei Geschossen: Erdgeschosswohnungen, Wohnungen im ersten Obergeschoss mit großen Terrassen und Penthäuser mit Solarium.',
  'В досье 2022 года описаны 96 квартир в 12 корпусах не выше трёх этажей: квартиры на первом этаже, квартиры на втором этаже с большими террасами и пентхаусы с солярием.',
  'يصف ملف عام 2022 ستة وتسعين مسكنًا في 12 مبنى لا يتجاوز ارتفاع أيٍّ منها ثلاثة طوابق: مساكن في الطابق الأرضي ومساكن في الطابق الأول بتراسات واسعة وبنتهاوس بسولاريوم.',
  'Het dossier van 2022 beschrijft 96 woningen in 12 blokken van hooguit drie bouwlagen: woningen op de begane grond, woningen op de eerste verdieping met grote terrassen en penthouses met solarium.',
  'Materiał z 2022 roku opisuje 96 lokali w 12 budynkach o wysokości najwyżej trzech kondygnacji: lokale na parterze, lokale na pierwszym piętrze z dużymi tarasami i penthouse’y z solarium.',
  'Dossieret fra 2022 beskriver 96 boliger i 12 blokker på høyst tre etasjer: boliger i første etasje, boliger i andre etasje med store terrasser og toppleiligheter med solterrasse.',
  'Dossiern från 2022 beskriver 96 bostäder i 12 hus på högst tre våningar: bostäder i bottenvåningen, bostäder på första våningen med stora terrasser och takvåningar med solterrass.')
a('.architecture.copy[1]',
  'Califica el diseño de moderno y minimalista, con estancias luminosas y diáfanas, y sitúa más de {N20,000} {U} de jardines con plantas y árboles mediterráneos alrededor de los bloques. Dice que la primera fase construye los bloques residenciales, las zonas comunes y los jardines.',
  'Il qualifie le design de moderne et minimaliste, avec des pièces lumineuses et ouvertes, et place plus de {N20,000} {U} de jardins plantés d’essences méditerranéennes autour des blocs. Il précise que la première phase construit les blocs résidentiels, les espaces communs et les jardins.',
  'Es nennt das Design modern und minimalistisch, mit hellen, offenen Räumen, und legt mehr als {N20,000} {U} Gärten mit mediterranen Pflanzen und Bäumen um die Blöcke. Die erste Phase baue die Wohnblöcke, die Gemeinschaftsbereiche und die Gärten.',
  'Дизайн назван современным и минималистичным, с светлыми и открытыми помещениями, а вокруг корпусов размещено более {N20,000} {U} садов со средиземноморскими растениями и деревьями. Сказано, что первая очередь строит жилые корпуса, общие зоны и сады.',
  'يصف التصميم بأنه حديث وبسيط، بغرف مضيئة ومفتوحة، ويضع حول المباني أكثر من {N20,000} {U} من الحدائق بنباتات وأشجار متوسطية. ويذكر أن المرحلة الأولى تبني المباني السكنية والمناطق المشتركة والحدائق.',
  'Het noemt het ontwerp modern en minimalistisch, met lichte, open ruimtes, en legt meer dan {N20,000} {U} tuinen met mediterrane planten en bomen rond de blokken. De eerste fase bouwt de woonblokken, de gemeenschappelijke ruimtes en de tuinen.',
  'Określa projekt jako nowoczesny i minimalistyczny, z jasnymi, otwartymi wnętrzami, a wokół budynków umieszcza ponad {N20,000} {U} ogrodów ze śródziemnomorskimi roślinami i drzewami. Podaje, że pierwszy etap obejmuje budynki mieszkalne, części wspólne i ogrody.',
  'Det kaller designet moderne og minimalistisk, med lyse, åpne rom, og legger mer enn {N20,000} {U} hager med middelhavsplanter og -trær rundt blokkene. Det sier at første fase bygger boligblokkene, fellesområdene og hagene.',
  'Den kallar designen modern och minimalistisk, med ljusa, öppna rum, och lägger mer än {N20,000} {U} trädgårdar med medelhavsväxter och träd runt husen. Den säger att den första fasen bygger bostadshusen, de gemensamma ytorna och trädgårdarna.')
a('.architecture.highlights[0]',
  '96 viviendas en 12 bloques de no más de tres alturas.', '96 logements répartis en 12 blocs de trois niveaux au plus.', '96 Wohnungen in 12 Blöcken mit höchstens drei Geschossen.',
  '96 квартир в 12 корпусах не выше трёх этажей.', '96 مسكنًا في 12 مبنى لا يزيد ارتفاع أيٍّ منها على ثلاثة طوابق.', '96 woningen in 12 blokken van hooguit drie bouwlagen.',
  '96 lokali w 12 budynkach o wysokości najwyżej trzech kondygnacji.', '96 boliger i 12 blokker på høyst tre etasjer.', '96 bostäder i 12 hus på högst tre våningar.')
a('.architecture.highlights[1]',
  'Viviendas en planta baja, viviendas en planta primera con grandes terrazas y áticos con solárium privado.',
  'Des logements au rez-de-chaussée, des logements au premier étage avec de grandes terrasses et des penthouses avec solarium privé.',
  'Erdgeschosswohnungen, Wohnungen im ersten Obergeschoss mit großen Terrassen und Penthäuser mit privatem Solarium.',
  'Квартиры на первом этаже, квартиры на втором этаже с большими террасами и пентхаусы с частным солярием.',
  'مساكن في الطابق الأرضي ومساكن في الطابق الأول بتراسات واسعة وبنتهاوس بسولاريوم خاص.',
  'Woningen op de begane grond, woningen op de eerste verdieping met grote terrassen en penthouses met privésolarium.',
  'Lokale na parterze, lokale na pierwszym piętrze z dużymi tarasami i penthouse’y z prywatnym solarium.',
  'Boliger i første etasje, boliger i andre etasje med store terrasser og toppleiligheter med privat solterrasse.',
  'Bostäder i bottenvåningen, bostäder på första våningen med stora terrasser och takvåningar med privat solterrass.')
a('.architecture.highlights[2]',
  'Más de {N20,000} {U} de jardines con plantas y árboles mediterráneos alrededor de los bloques.',
  'Plus de {N20,000} {U} de jardins plantés d’essences méditerranéennes autour des blocs.',
  'Mehr als {N20,000} {U} Gärten mit mediterranen Pflanzen und Bäumen rund um die Blöcke.',
  'Более {N20,000} {U} садов со средиземноморскими растениями и деревьями вокруг корпусов.',
  'أكثر من {N20,000} {U} من الحدائق بنباتات وأشجار متوسطية حول المباني.',
  'Meer dan {N20,000} {U} tuinen met mediterrane planten en bomen rond de blokken.',
  'Ponad {N20,000} {U} ogrodów ze śródziemnomorskimi roślinami i drzewami wokół budynków.',
  'Mer enn {N20,000} {U} hager med middelhavsplanter og -trær rundt blokkene.',
  'Mer än {N20,000} {U} trädgårdar med medelhavsväxter och träd runt husen.')
a('.architecture.highlights[3]',
  'Acabados de paredes y suelos a elegir del catálogo del promotor, sin coste adicional.',
  'Finitions des murs et des sols à choisir dans le catalogue du promoteur, sans supplément.',
  'Wand- und Bodenausführungen zur Wahl aus dem Katalog des Bauträgers, ohne Aufpreis.',
  'Отделка стен и полов на выбор из каталога застройщика, без доплаты.',
  'تشطيبات للجدران والأرضيات تُختار من كتالوج المطوّر دون تكلفة إضافية.',
  'Wand- en vloerafwerkingen naar keuze uit de catalogus van de ontwikkelaar, zonder meerprijs.',
  'Wykończenia ścian i podłóg do wyboru z katalogu dewelopera, bez dopłaty.',
  'Vegg- og gulvbelegg etter valg fra utbyggerens katalog, uten tillegg.',
  'Vägg- och golvytskikt att välja ur exploatörens katalog, utan extra kostnad.')
a('.lifestyle.headlineHtml',
  'Un club, un spa y <em>tres piscinas</em>', 'Un club, un spa et <em>trois piscines</em>', 'Ein Club, ein Spa und <em>drei Pools</em>', 'Клуб, спа и <em>три бассейна</em>',
  'نادٍ وسبا و<em>ثلاثة مسابح</em>', 'Een club, een spa en <em>drie zwembaden</em>', 'Klub, spa i <em>trzy baseny</em>', 'En klubb, et spa og <em>tre basseng</em>', 'En klubb, ett spa och <em>tre pooler</em>')
a('.lifestyle.copy',
  'Tres piscinas comunitarias, un spa, dos gimnasios, una sala de coworking y un club social, tal como los describe el dosier de junio de 2026.',
  'Trois piscines communes, un spa, deux salles de sport, un espace de coworking et un club social, tels que les décrit le dossier de juin 2026.',
  'Drei Gemeinschaftspools, ein Spa, zwei Fitnessräume, ein Coworking-Raum und ein Social Club, wie sie das Dossier vom Juni 2026 beschreibt.',
  'Три общих бассейна, спа, два спортзала, коворкинг и общественный клуб — так их описывает досье июня 2026 года.',
  'ثلاثة مسابح مشتركة وسبا وصالتان رياضيتان وغرفة عمل مشترك ونادٍ اجتماعي، كما يصفها ملف يونيو 2026.',
  'Drie gemeenschappelijke zwembaden, een spa, twee fitnessruimtes, een coworkingruimte en een sociale club, zoals het dossier van juni 2026 ze beschrijft.',
  'Trzy wspólne baseny, spa, dwie siłownie, sala coworkingowa i klub mieszkańców, tak jak opisuje je materiał z czerwca 2026 roku.',
  'Tre fellesbasseng, et spa, to treningsrom, et coworking-rom og en sosialklubb, slik dossieret fra juni 2026 beskriver dem.',
  'Tre gemensamma pooler, ett spa, två gym, ett coworkingrum och en social klubb, så som dossiern från juni 2026 beskriver dem.')
a('.lifestyle.panels[0][1]',
  'Tres piscinas comunitarias con zona de tumbonas y un bar de piscina que se instalará junto a la piscina central. Más de {N20,000} {U} de jardines pensados para pasear.',
  'Trois piscines communes avec un espace de bains de soleil et un bar de piscine qui sera installé près de la piscine centrale. Plus de {N20,000} {U} de jardins pensés pour la promenade.',
  'Drei Gemeinschaftspools mit Liegebereich und eine Poolbar, die am zentralen Pool eingerichtet werden soll. Mehr als {N20,000} {U} Gärten zum Spazierengehen.',
  'Три общих бассейна с зоной шезлонгов и бар у бассейна, который будет установлен у центрального бассейна. Более {N20,000} {U} садов для прогулок.',
  'ثلاثة مسابح مشتركة مع منطقة لمقاعد التشمّس وبار مسبح سيُركَّب عند المسبح المركزي. وأكثر من {N20,000} {U} من الحدائق المخصصة للتنزه.',
  'Drie gemeenschappelijke zwembaden met ligbedden en een poolbar die bij het centrale zwembad komt. Meer dan {N20,000} {U} tuinen om te wandelen.',
  'Trzy wspólne baseny ze strefą leżaków i bar przy basenie, który ma zostać zainstalowany przy basenie centralnym. Ponad {N20,000} {U} ogrodów do spacerów.',
  'Tre fellesbasseng med solsengområde og en poolbar som skal installeres ved det sentrale bassenget. Mer enn {N20,000} {U} hager lagt ut for spaserturer.',
  'Tre gemensamma pooler med solbäddsområde och en poolbar som ska installeras vid den centrala poolen. Mer än {N20,000} {U} trädgårdar att promenera i.')
a('.lifestyle.panels[1][1]',
  'Un spa de más de {N200} {U} con piscina climatizada, ducha de agua fría, sauna y baño turco, y dos gimnasios interiores.',
  'Un spa de plus de {N200} {U} avec bassin chauffé, douche froide, sauna et hammam, et deux salles de sport intérieures.',
  'Ein Spa von mehr als {N200} {U} mit beheiztem Pool, Kaltdusche, Sauna und Dampfbad sowie zwei Fitnessräume im Innenbereich.',
  'Спа площадью более {N200} {U} с подогреваемым бассейном, холодным душем, сауной и турецкой баней, а также два спортзала в помещении.',
  'سبا تتجاوز مساحته {N200} {U} بمسبح مُدفأ ودش بارد وساونا وحمّام تركي، وصالتان رياضيتان داخليتان.',
  'Een spa van meer dan {N200} {U} met verwarmd zwembad, koude douche, sauna en Turks bad, en twee fitnessruimtes binnen.',
  'Spa o powierzchni ponad {N200} {U} z podgrzewanym basenem, zimnym prysznicem, sauną i łaźnią turecką oraz dwie siłownie wewnątrz.',
  'Et spa på mer enn {N200} {U} med oppvarmet basseng, kald dusj, badstue og tyrkisk bad, og to innendørs treningsrom.',
  'Ett spa på mer än {N200} {U} med uppvärmd pool, kall dusch, bastu och turkiskt bad, och två gym inomhus.')
a('.lifestyle.panels[2][1]',
  'Una sala de coworking flexible y un club social decorado en tonos crema y madera clara con un suave toque costero.',
  'Un espace de coworking flexible et un club social décoré dans des tons crème et bois clair, avec une touche côtière légère.',
  'Ein flexibler Coworking-Raum und ein Social Club, eingerichtet in Cremetönen und hellem Holz mit einem sanften Küstenflair.',
  'Гибкий коворкинг и общественный клуб, оформленный в кремовых тонах и светлом дереве с лёгким прибрежным акцентом.',
  'غرفة عمل مشترك مرنة ونادٍ اجتماعي مزيّن بدرجات الكريمي والخشب الفاتح مع لمسة ساحلية هادئة.',
  'Een flexibele coworkingruimte en een sociale club, ingericht in crèmetinten en licht hout met een zachte kustsfeer.',
  'Elastyczna sala coworkingowa i klub mieszkańców urządzony w kremowych tonach i jasnym drewnie z delikatnym akcentem nadmorskim.',
  'Et fleksibelt coworking-rom og en sosialklubb innredet i kremtoner og lyst tre med et mykt kystpreg.',
  'Ett flexibelt coworkingrum och en social klubb inredd i gräddtoner och ljust trä med en mjuk kustprägel.')

# ---- private viewing, location, faq ---------------------------------------------------------------

a('.privateViewing.insights[0][0]',
  'Qué viviendas están terminadas', 'Quels logements sont achevés', 'Welche Wohnungen fertig sind', 'Какие квартиры готовы',
  'أي المساكن منجزة', 'Welke woningen klaar zijn', 'Które lokale są ukończone', 'Hvilke boliger som er ferdige', 'Vilka bostäder som är färdiga')
a('.privateViewing.insights[0][1]',
  'Qué viviendas y qué zonas comunes están construidas, y qué muestran los pisos piloto amueblados.',
  'Quels logements et quels espaces communs sont construits, et ce que montrent les appartements témoins meublés.',
  'Welche Wohnungen und welche Gemeinschaftsbereiche gebaut sind und was die möblierten Musterwohnungen zeigen.',
  'Какие квартиры и общие зоны построены и что показывают меблированные демонстрационные квартиры.',
  'أي المساكن والمناطق المشتركة قد بُنيت، وماذا تُظهر الشقق النموذجية المفروشة.',
  'Welke woningen en gemeenschappelijke ruimtes gebouwd zijn en wat de gemeubileerde modelwoningen laten zien.',
  'Które lokale i części wspólne są wybudowane oraz co pokazują umeblowane mieszkania pokazowe.',
  'Hvilke boliger og fellesområder som er bygget, og hva de møblerte visningsleilighetene viser.',
  'Vilka bostäder och gemensamma ytor som är byggda och vad de möblerade visningsbostäderna visar.')
a('.privateViewing.insights[1][0]',
  'La hoja que se aplica', 'La feuille qui s’applique', 'Das Blatt, das gilt', 'Какой лист действует', 'الورقة المنطبقة', 'Het blad dat geldt', 'Który arkusz obowiązuje', 'Arket som gjelder', 'Bladet som gäller')
a('.privateViewing.insights[1][1]',
  'Cuál de las dos hojas de condiciones de pago se aplica a la vivienda que usted elija.',
  'Laquelle des deux feuilles de conditions de paiement s’applique au logement que vous choisissez.',
  'Welches der beiden Zahlungsblätter für die von Ihnen gewählte Wohnung gilt.',
  'Какой из двух листов условий оплаты действует для выбранной вами квартиры.',
  'أيّ ورقتي شروط الدفع تنطبق على المسكن الذي تختاره.',
  'Welk van de twee betalingsbladen geldt voor de woning die u kiest.',
  'Który z dwóch arkuszy warunków płatności obowiązuje dla wybranego przez Państwa lokalu.',
  'Hvilket av de to betalingsarkene som gjelder for boligen De velger.',
  'Vilket av de två betalningsbladen som gäller för den bostad ni väljer.')
a('.privateViewing.insights[2][1]',
  'Qué incluye el solárium del ático y cuánto costarían la piscina y el jacuzzi.',
  'Ce que comprend le solarium du penthouse, et ce que coûteraient le bassin et le jacuzzi.',
  'Was das Penthouse-Solarium enthält und was Pool und Whirlpool kosten würden.',
  'Что входит в солярий пентхауса и сколько стоили бы бассейн и джакузи.',
  'ما الذي يشمله سولاريوم البنتهاوس، وكم ستبلغ تكلفة المسبح والجاكوزي.',
  'Wat het solarium van het penthouse omvat en wat het zwembad en de jacuzzi zouden kosten.',
  'Co obejmuje solarium penthouse’u i ile kosztowałyby basen i jacuzzi.',
  'Hva solterrassen på toppleiligheten omfatter, og hva bassenget og jacuzzien ville koste.',
  'Vad takvåningens solterrass omfattar och vad poolen och jacuzzin skulle kosta.')
a('.location.headlineHtml',
  'Marbella, <em>a pocos minutos del centro</em>', 'Marbella, <em>à quelques minutes du centre</em>', 'Marbella, <em>wenige Minuten vom Ort</em>', 'Марбелья, <em>в нескольких минутах от города</em>',
  'ماربيا، <em>على بُعد دقائق من البلدة</em>', 'Marbella, <em>op enkele minuten van het centrum</em>', 'Marbella, <em>kilka minut od miasta</em>', 'Marbella, <em>få minutter fra sentrum</em>', 'Marbella, <em>några minuter från centrum</em>')
a('.location.copy',
  'El promotor sitúa las viviendas en Marbella: a cinco minutos del centro en su dosier de 2022 y a un paso del centro en el de junio de 2026, con el paseo marítimo, las playas y los campos de golf de la Costa del Sol al alcance. Su mapa de ubicación nombra Sierra Blanca, la Milla de Oro, el centro comercial La Cañada y el puerto. Los documentos no dan dirección, coordenadas ni distancias en kilómetros, por lo que el mapa muestra la zona de Altos de los Monteros, en Marbella, que Nueva Living confirma sobre el terreno.',
  'Le promoteur situe les logements à Marbella : à cinq minutes de la ville dans son dossier de 2022, à deux pas du centre dans celui de juin 2026, avec le front de mer, les plages et les golfs de la Costa del Sol à portée. Sa carte de situation nomme la Sierra Blanca, le Golden Mile, le centre commercial La Cañada et le port. Les documents ne donnent ni adresse, ni coordonnées, ni distances en kilomètres ; la carte montre donc le secteur d’Altos de los Monteros, à Marbella, que Nueva Living confirme sur place.',
  'Der Bauträger verortet die Wohnungen in Marbella: fünf Minuten vom Ort entfernt in seinem Dossier von 2022, einen Katzensprung vom Zentrum im Dossier vom Juni 2026, mit Strandpromenade, Stränden und Golfplätzen der Costa del Sol in Reichweite. Seine Lagekarte nennt Sierra Blanca, die Goldene Meile, das Einkaufszentrum La Cañada und den Hafen. Die Unterlagen nennen weder Adresse noch Koordinaten noch Entfernungen in Kilometern, daher zeigt die Karte das Gebiet Altos de los Monteros in Marbella, das Nueva Living vor Ort bestätigt.',
  'Застройщик помещает квартиры в Марбелье: в пяти минутах от города в досье 2022 года и в двух шагах от центра в досье июня 2026 года, с набережной, пляжами и полями для гольфа Коста-дель-Соль в досягаемости. На его карте расположения названы Сьерра-Бланка, Золотая миля, торговый центр La Cañada и порт. В документах нет ни адреса, ни координат, ни расстояний в километрах, поэтому на карте показан район Альтос-де-лос-Монтеросе в Марбелье, который Nueva Living подтверждает на месте.',
  'يضع المطوّر المساكن في ماربيا: على بُعد خمس دقائق من البلدة في ملف 2022 وعلى مقربة من المركز في ملف يونيو 2026، مع الواجهة البحرية والشواطئ وملاعب الغولف في كوستا ديل سول في المتناول. وتذكر خريطة الموقع لديه سييرا بلانكا والميل الذهبي ومركز لا كانيادا التجاري والميناء. لا تذكر الوثائق عنوانًا ولا إحداثيات ولا مسافات بالكيلومترات، لذا تُظهر الخريطة منطقة ألتوس دي لوس مونتيروس في ماربيا، وتؤكدها نويفا ليفينغ في الموقع.',
  'De ontwikkelaar plaatst de woningen in Marbella: op vijf minuten van het centrum in zijn dossier van 2022, op een steenworp afstand van het centrum in dat van juni 2026, met de boulevard, de stranden en de golfbanen van de Costa del Sol binnen bereik. Zijn locatiekaart noemt Sierra Blanca, de Golden Mile, winkelcentrum La Cañada en de haven. De documenten geven geen adres, geen coördinaten en geen afstanden in kilometers, dus de kaart toont het gebied Altos de los Monteros in Marbella, dat Nueva Living ter plaatse bevestigt.',
  'Deweloper umieszcza lokale w Marbelli: pięć minut od miasta w materiale z 2022 roku i o krok od centrum w materiale z czerwca 2026 roku, z promenadą, plażami i polami golfowymi Costa del Sol w zasięgu. Jego mapa lokalizacji wymienia Sierra Blanca, Złotą Milę, centrum handlowe La Cañada i port. Dokumenty nie podają adresu, współrzędnych ani odległości w kilometrach, dlatego mapa pokazuje okolice Altos de los Monteros w Marbelli, co Nueva Living potwierdza na miejscu.',
  'Utbyggeren plasserer boligene i Marbella: fem minutter fra sentrum i dossieret fra 2022 og et steinkast fra sentrum i dossieret fra juni 2026, med strandpromenaden, strendene og golfbanene på Costa del Sol innen rekkevidde. Lokaliseringskartet nevner Sierra Blanca, Golden Mile, kjøpesenteret La Cañada og havnen. Dokumentene oppgir verken adresse, koordinater eller avstander i kilometer, så kartet viser området Altos de los Monteros i Marbella, som Nueva Living bekrefter på stedet.',
  'Exploatören placerar bostäderna i Marbella: fem minuter från centrum i dossiern från 2022 och ett stenkast från centrum i dossiern från juni 2026, med strandpromenaden, stränderna och golfbanorna på Costa del Sol inom räckhåll. Dess lägeskarta nämner Sierra Blanca, Golden Mile, köpcentret La Cañada och hamnen. Dokumenten anger varken adress, koordinater eller avstånd i kilometer, så kartan visar området Altos de los Monteros i Marbella, vilket Nueva Living bekräftar på plats.')
a('.faq[0][1]',
  'La lista de precios asigna a cada vivienda una plaza de aparcamiento numerada (dos para un ático, una para un apartamento) y un trastero, y no indica si están incluidos en el precio. Los impuestos no están incluidos: se añaden el IVA del 10 por ciento y el impuesto de actos jurídicos documentados del 1,20 por ciento, además de los gastos de notaría y registro.',
  'La liste de prix attribue à chaque logement une place de parking numérotée (deux pour un penthouse, une pour un appartement) et un débarras, sans préciser s’ils sont compris dans le prix. Les taxes ne sont pas comprises : la TVA à 10 pour cent et le droit de timbre à 1,20 pour cent s’ajoutent, ainsi que les frais de notaire et d’enregistrement.',
  'Die Preisliste weist jeder Wohnung einen nummerierten Stellplatz (zwei bei einem Penthouse, einen bei einer Wohnung) und einen Abstellraum zu und sagt nicht, ob sie im Preis enthalten sind. Steuern sind nicht enthalten: 10 Prozent Mehrwertsteuer und 1,20 Prozent Stempelsteuer kommen hinzu, dazu Notar- und Grundbuchkosten.',
  'Прайс-лист закрепляет за каждой квартирой пронумерованное машиноместо (два у пентхауса, одно у квартиры) и кладовую и не уточняет, входят ли они в цену. Налоги не включены: сверху добавляются НДС 10 процентов и гербовый сбор 1,20 процента, а также расходы на нотариуса и регистрацию.',
  'تخصّص قائمة الأسعار لكل مسكن موقف سيارة مرقّمًا (اثنين للبنتهاوس وواحدًا للشقة) ومخزنًا، ولا تذكر ما إذا كانت مشمولة في السعر. الضرائب غير مشمولة: تُضاف ضريبة القيمة المضافة 10 بالمئة ورسم الدمغة 1.20 بالمئة، إلى جانب أتعاب التوثيق والتسجيل العقاري.',
  'De prijslijst wijst elke woning een genummerde parkeerplaats (twee bij een penthouse, één bij een appartement) en een berging toe en vermeldt niet of die in de prijs zijn inbegrepen. Belasting is niet inbegrepen: 10 procent btw en 1,20 procent overdrachtsbelasting komen erbij, samen met notaris- en kadasterkosten.',
  'Cennik przypisuje każdemu lokalowi numerowane miejsce postojowe (dwa przy penthousie, jedno przy apartamencie) i komórkę lokatorską i nie podaje, czy są wliczone w cenę. Podatek nie jest wliczony: doliczany jest VAT w wysokości 10 procent i podatek od czynności cywilnoprawnych 1,20 procent, a także opłaty notarialne i wieczystoksięgowe.',
  'Prislisten tildeler hver bolig en nummerert parkeringsplass (to for en toppleilighet, én for en leilighet) og en bod, og sier ikke om de er inkludert i prisen. Skatter og avgifter er ikke inkludert: mva på 10 prosent og dokumentavgift på 1,20 prosent kommer i tillegg, sammen med notar- og tinglysingsgebyrer.',
  'Prislistan tilldelar varje bostad en numrerad parkeringsplats (två för en takvåning, en för en lägenhet) och ett förråd och anger inte om de ingår i priset. IVA ingår inte: IVA på 10 procent och stämpelskatt på 1,20 procent tillkommer, liksom notarie- och registreringsavgifter.')
a('.faq[1][1]',
  'Ningún documento da una fecha de entrega. Las hojas de condiciones de pago sitúan la escritura 60 o 90 días después de la reserva, lo que sugiere viviendas terminadas o casi terminadas. Nueva Living pregunta qué viviendas están terminadas y pide la fecha por escrito.',
  'Aucun document ne donne de date de livraison. Les feuilles de conditions de paiement fixent l’acte 60 ou 90 jours après la réservation, ce qui suggère des logements achevés ou presque. Nueva Living demande quels logements sont achevés et réclame la date par écrit.',
  'Kein Dokument nennt einen Fertigstellungstermin. Die Zahlungsblätter legen die Beurkundung 60 oder 90 Tage nach der Reservierung fest, was auf fertige oder fast fertige Wohnungen schließen lässt. Nueva Living fragt nach, welche Wohnungen fertig sind, und verlangt den Termin schriftlich.',
  'Ни один документ не называет срок сдачи. Листы условий оплаты назначают нотариальный акт через 60 или 90 дней после бронирования, что наводит на мысль о готовых или почти готовых квартирах. Nueva Living выясняет, какие квартиры готовы, и запрашивает срок в письменном виде.',
  'لا تذكر أي وثيقة موعد تسليم. تحدد ورقتا شروط الدفع سند الملكية بعد 60 أو 90 يومًا من الحجز، مما يوحي بمساكن منجزة أو شبه منجزة. تسأل نويفا ليفينغ عن المساكن المنجزة وتطلب الموعد كتابةً.',
  'Geen enkel document geeft een opleverdatum. De betalingsbladen leggen de akte 60 of 90 dagen na de reservering, wat wijst op afgewerkte of bijna afgewerkte woningen. Nueva Living vraagt welke woningen klaar zijn en vraagt de datum schriftelijk op.',
  'Żaden dokument nie podaje terminu odbioru. Arkusze warunków płatności wyznaczają akt na 60 lub 90 dni po rezerwacji, co sugeruje lokale ukończone lub prawie ukończone. Nueva Living pyta, które lokale są ukończone, i żąda terminu na piśmie.',
  'Ingen dokumenter oppgir en ferdigstillelsesdato. Betalingsarkene setter skjøtet 60 eller 90 dager etter reservasjonen, noe som tyder på ferdige eller nesten ferdige boliger. Nueva Living spør hvilke boliger som er ferdige, og ber skriftlig om datoen.',
  'Inget dokument anger något tillträdesdatum. Betalningsbladen sätter notarieakten 60 eller 90 dagar efter bokningen, vilket tyder på färdiga eller nästan färdiga bostäder. Nueva Living frågar vilka bostäder som är färdiga och begär datumet skriftligen.')
a('.faq[2][1]',
  'La promoción tiene 96 viviendas. La lista de precios del 3 de noviembre de 2026 muestra catorce: diez disponibles, dos vendidas (22A y 32B) y dos reservadas (72A y 92A). No muestra las otras 82.',
  'Le programme compte 96 logements. La liste de prix du 3 novembre 2026 en présente quatorze : dix disponibles, deux vendus (22A et 32B) et deux réservés (72A et 92A). Elle ne présente pas les 82 autres.',
  'Die Anlage hat 96 Wohnungen. Die Preisliste vom 3. November 2026 zeigt vierzehn davon: zehn verfügbar, zwei verkauft (22A und 32B) und zwei reserviert (72A und 92A). Die anderen 82 zeigt sie nicht.',
  'В комплексе 96 квартир. В прайс-листе от 3 ноября 2026 года указаны четырнадцать: десять доступны, две проданы (22A и 32B) и две забронированы (72A и 92A). Остальные 82 в нём не показаны.',
  'يضم المشروع 96 مسكنًا. تعرض قائمة الأسعار بتاريخ 3 نوفمبر 2026 أربعة عشر منها: عشرة متاحة واثنان مباعان (22A و32B) واثنان محجوزان (72A و92A). ولا تعرض المساكن الاثنين والثمانين الأخرى.',
  'Het complex telt 96 woningen. De prijslijst van 3 november 2026 toont er veertien: tien beschikbaar, twee verkocht (22A en 32B) en twee gereserveerd (72A en 92A). De andere 82 toont ze niet.',
  'Inwestycja liczy 96 lokali. Cennik z 3 listopada 2026 pokazuje czternaście z nich: dziesięć dostępnych, dwa sprzedane (22A i 32B) i dwa zarezerwowane (72A i 92A). Pozostałych 82 nie pokazuje.',
  'Anlegget har 96 boliger. Prislisten av 3. november 2026 viser fjorten av dem: ti tilgjengelige, to solgt (22A og 32B) og to reservert (72A og 92A). Den viser ikke de øvrige 82.',
  'Området har 96 bostäder. Prislistan från 3 november 2026 visar fjorton av dem: tio tillgängliga, två sålda (22A och 32B) och två reserverade (72A och 92A). De övriga 82 visas inte.')
a('.faq[3][1]',
  'En la hoja de Fase I y bloques 5 y 6, {E10000} más IVA en la reserva y el saldo más IVA en la escritura, como máximo 90 días después de la reserva. En la hoja general, {E30000} más IVA en la reserva y el saldo más IVA a la finalización y entrega de llaves, como máximo 60 días después de la reserva.',
  'Sur la feuille de la phase I et des blocs 5 et 6, {E10000} plus TVA à la réservation et le solde plus TVA à l’acte, au plus 90 jours après la réservation. Sur la feuille générale, {E30000} plus TVA à la réservation et le solde plus TVA à l’achèvement et à la remise des clés, au plus 60 jours après la réservation.',
  'Auf dem Blatt für Phase I und Blöcke 5 und 6: {E10000} zuzüglich MwSt. bei der Reservierung und der Restbetrag zuzüglich MwSt. bei der Beurkundung, spätestens 90 Tage nach der Reservierung. Auf dem allgemeinen Blatt: {E30000} zuzüglich MwSt. bei der Reservierung und der Restbetrag zuzüglich MwSt. bei Fertigstellung und Schlüsselübergabe, spätestens 60 Tage nach der Reservierung.',
  'По листу очереди I и блоков 5 и 6: {E10000} плюс НДС при бронировании и остаток плюс НДС при нотариальном акте, не позднее 90 дней после бронирования. По общему листу: {E30000} плюс НДС при бронировании и остаток плюс НДС при завершении строительства и передаче ключей, не позднее 60 дней после бронирования.',
  'في ورقة المرحلة الأولى والمبنيين 5 و6: {E10000} زائد ضريبة القيمة المضافة عند الحجز والرصيد زائد الضريبة عند سند الملكية، بحد أقصى 90 يومًا بعد الحجز. وفي الورقة العامة: {E30000} زائد ضريبة القيمة المضافة عند الحجز والرصيد زائد الضريبة عند الإنجاز وتسليم المفاتيح، بحد أقصى 60 يومًا بعد الحجز.',
  'Op het blad voor fase I en blokken 5 en 6: {E10000} plus btw bij de reservering en het restant plus btw bij de akte, uiterlijk 90 dagen na de reservering. Op het algemene blad: {E30000} plus btw bij de reservering en het restant plus btw bij oplevering en sleuteloverdracht, uiterlijk 60 dagen na de reservering.',
  'Na arkuszu dla etapu I i budynków 5 i 6: {E10000} plus VAT przy rezerwacji i reszta ceny plus VAT przy akcie, najpóźniej 90 dni po rezerwacji. Na arkuszu ogólnym: {E30000} plus VAT przy rezerwacji i reszta ceny plus VAT przy ukończeniu i wydaniu kluczy, najpóźniej 60 dni po rezerwacji.',
  'På arket for fase I og blokk 5 og 6: {E10000} pluss mva ved reservasjon og restbeløpet pluss mva ved skjøtet, senest 90 dager etter reservasjonen. På det generelle arket: {E30000} pluss mva ved reservasjon og restbeløpet pluss mva ved ferdigstillelse og nøkkeloverlevering, senest 60 dager etter reservasjonen.',
  'På bladet för fas I och hus 5 och 6: {E10000} plus IVA vid bokning och restbeloppet plus IVA vid notarieakten, senast 90 dagar efter bokningen. På det allmänna bladet: {E30000} plus IVA vid bokning och restbeloppet plus IVA vid färdigställande och nyckelöverlämning, senast 60 dagar efter bokningen.')
a('.faq[4][0]',
  '¿Está incluida la piscina del ático?', 'La piscine du penthouse est-elle comprise ?', 'Ist der Penthouse-Pool enthalten?', 'Входит ли бассейн пентхауса в цену?',
  'هل مسبح البنتهاوس مشمول؟', 'Is het zwembad van het penthouse inbegrepen?', 'Czy basen przy penthousie jest wliczony?', 'Er penthouse-bassenget inkludert?', 'Ingår poolen i takvåningen?')
a('.faq[4][1]',
  'No según los planos: las hojas de planos dicen que la piscina dibujada en la planta del solárium no forma parte del proyecto ni del precio de venta y es una opción a cargo del comprador. El dosier de junio de 2026 muestra un jacuzzi en el solárium, y la lista de precios marca la columna de piscina con YES en todos los áticos. Preguntamos qué incluye cada precio.',
  'Pas d’après les plans : les planches de plans précisent que le bassin dessiné à l’étage du solarium ne fait partie ni du projet ni du prix de vente et constitue une option à la charge de l’acquéreur. Le dossier de juin 2026 montre un jacuzzi sur le solarium, et la liste de prix indique YES dans la colonne piscine pour tous les penthouses. Nous demandons ce que comprend chaque prix.',
  'Nach den Plänen nicht: Die Planblätter besagen, dass der auf der Solarium-Ebene eingezeichnete Pool weder zum Projekt noch zum Verkaufspreis gehört und eine Option auf Kosten des Käufers ist. Das Dossier vom Juni 2026 zeigt einen Whirlpool auf dem Solarium, und die Preisliste setzt in der Pool-Spalte bei jedem Penthouse YES. Wir fragen nach, was in jedem Preis enthalten ist.',
  'По планировкам — нет: в планировочных листах сказано, что бассейн, нарисованный на уровне солярия, не входит ни в проект, ни в цену продажи и является опцией за счёт покупателя. В досье июня 2026 года на солярии показано джакузи, а в прайс-листе в колонке бассейна у каждого пентхауса стоит YES. Мы выясняем, что входит в каждую цену.',
  'ليس بحسب المخططات: تذكر أوراق المخططات أن المسبح المرسوم في طابق السولاريوم ليس جزءًا من المشروع ولا من سعر البيع وهو خيار على نفقة المشتري. ويعرض ملف يونيو 2026 جاكوزي على السولاريوم، وتضع قائمة الأسعار YES في عمود المسبح لكل بنتهاوس. نسأل عمّا يشمله كل سعر.',
  'Volgens de plattegronden niet: de plattegrondbladen zeggen dat het zwembad dat op de solariumverdieping is getekend geen deel uitmaakt van het project of de verkoopprijs en een optie is voor rekening van de koper. Het dossier van juni 2026 toont een jacuzzi op het solarium, en de prijslijst zet in de zwembadkolom bij elk penthouse YES. Wij vragen wat in elke prijs zit.',
  'Według rzutów nie: arkusze rzutów podają, że basen narysowany na poziomie solarium nie należy do projektu ani do ceny sprzedaży i jest opcją na koszt kupującego. Materiał z czerwca 2026 roku pokazuje jacuzzi na solarium, a cennik w kolumnie basenu przy każdym penthousie podaje YES. Pytamy, co obejmuje każda cena.',
  'Ikke ifølge plantegningene: plantegningsarkene sier at bassenget som er tegnet inn på solterrasseplanet verken er en del av prosjektet eller salgsprisen og er et tilvalg for kjøperens regning. Dossieret fra juni 2026 viser en jacuzzi på solterrassen, og prislisten har YES i bassengkolonnen for hver toppleilighet. Vi spør hva hver pris omfatter.',
  'Inte enligt planritningarna: planritningsbladen säger att poolen som ritats in på solterrassplanet varken ingår i projektet eller försäljningspriset och är ett tillval på köparens bekostnad. Dossiern från juni 2026 visar ett badkar med bubbelfunktion på solterrassen, och prislistan har YES i poolkolumnen för varje takvåning. Vi frågar vad varje pris omfattar.')
a('.faq[5][1]',
  'Los dosieres hablan de vistas al mar y muestran fotografías desde terrazas de ático con el mar en el horizonte. La vista concreta de cada vivienda depende de su bloque y su planta, y la lista de precios no la indica, por lo que conviene comprobarla sobre el terreno.',
  'Les dossiers parlent de vues sur la mer et montrent des photographies prises depuis des terrasses de penthouse avec la mer à l’horizon. La vue précise de chaque logement dépend de son bloc et de son étage, et la liste de prix ne l’indique pas ; mieux vaut la vérifier sur place.',
  'Die Dossiers sprechen von Meerblick und zeigen Fotos von Penthouse-Terrassen mit dem Meer am Horizont. Welche Aussicht eine bestimmte Wohnung hat, hängt von Block und Geschoss ab, und die Preisliste nennt sie nicht, daher lohnt sich eine Prüfung vor Ort.',
  'В досье говорится о видах на море и приведены фотографии с террас пентхаусов с морем на горизонте. Какой именно вид у конкретной квартиры, зависит от корпуса и этажа, а прайс-лист этого не указывает, поэтому стоит проверить на месте.',
  'تتحدث الملفات عن إطلالات على البحر وتعرض صورًا من تراسات البنتهاوس والبحر في الأفق. والإطلالة الفعلية لكل مسكن تتوقف على مبناه وطابقه، ولا تذكرها قائمة الأسعار، لذا يستحق الأمر التحقق منها في الموقع.',
  'De dossiers spreken van zeezicht en tonen foto’s vanaf penthouseterrassen met de zee aan de horizon. Welk uitzicht een bepaalde woning heeft, hangt af van blok en verdieping, en de prijslijst vermeldt het niet, dus het loont om het ter plaatse te controleren.',
  'Materiały mówią o widokach na morze i pokazują zdjęcia z tarasów penthouse’ów z morzem na horyzoncie. Jaki widok ma konkretny lokal, zależy od budynku i piętra, a cennik tego nie podaje, więc warto to sprawdzić na miejscu.',
  'Dossierene taler om utsikt mot havet og viser fotografier fra terrasser på toppleiligheter med havet i horisonten. Hvilken utsikt en bestemt bolig har, avhenger av blokk og etasje, og prislisten oppgir den ikke, så det lønner seg å sjekke på stedet.',
  'Dossierna talar om havsutsikt och visar fotografier från terrasser på takvåningar med havet i horisonten. Vilken utsikt en viss bostad har beror på hus och våning, och prislistan anger den inte, så det är värt att kontrollera på plats.')
a('.faq[6][1]',
  'Sí. La lista de precios dice que es válida durante dos días desde su descarga, y el promotor puede revisar precios y disponibilidad en cualquier momento antes de firmar una reserva. Nueva Living reconfirma la cifra antes de que usted se comprometa a nada.',
  'Oui. La liste de prix indique qu’elle est valable deux jours à compter de son téléchargement, et le promoteur peut réviser prix et disponibilité à tout moment avant la signature d’une réservation. Nueva Living reconfirme le montant avant que vous vous engagiez à quoi que ce soit.',
  'Ja. Die Preisliste sagt, dass sie zwei Tage ab dem Herunterladen gültig ist, und der Bauträger kann Preise und Verfügbarkeit jederzeit vor der Unterzeichnung einer Reservierung ändern. Nueva Living bestätigt den Betrag erneut, bevor Sie sich auf irgendetwas festlegen.',
  'Да. В прайс-листе сказано, что он действителен два дня с момента скачивания, а застройщик может пересмотреть цены и наличие в любой момент до подписания бронирования. Nueva Living подтверждает сумму повторно, прежде чем вы к чему-либо обяжетесь.',
  'نعم. تذكر قائمة الأسعار أنها صالحة لمدة يومين من تنزيلها، ويجوز للمطوّر مراجعة الأسعار والتوافر في أي وقت قبل توقيع الحجز. تعيد نويفا ليفينغ تأكيد الرقم قبل أن تلتزم بأي شيء.',
  'Ja. De prijslijst zegt dat ze twee dagen na het downloaden geldig is, en de ontwikkelaar kan prijzen en beschikbaarheid op elk moment vóór de ondertekening van een reservering herzien. Nueva Living bevestigt het bedrag opnieuw voordat u zich tot iets verbindt.',
  'Tak. Cennik podaje, że jest ważny dwa dni od pobrania, a deweloper może zmienić ceny i dostępność w dowolnym momencie przed podpisaniem rezerwacji. Nueva Living ponownie potwierdza kwotę, zanim Państwo do czegokolwiek się zobowiążą.',
  'Ja. Prislisten oppgir at den gjelder i to dager fra nedlasting, og utbyggeren kan endre priser og tilgjengelighet når som helst før en reservasjon signeres. Nueva Living bekrefter beløpet på nytt før De forplikter dere til noe.',
  'Ja. Prislistan anger att den gäller i två dagar från nedladdningen, och exploatören kan ändra priser och tillgänglighet när som helst innan en bokning undertecknas. Nueva Living bekräftar summan på nytt innan ni förbinder er till något.')
a('.enquiry.message',
  'Quisiera conocer la disponibilidad y los precios actuales de Monteros Heights Residences.',
  'Je souhaiterais connaître la disponibilité et les prix actuels de Monteros Heights Residences.',
  'Ich möchte die aktuelle Verfügbarkeit und die Preise für Monteros Heights Residences erfahren.',
  'Я хотел бы узнать актуальное наличие и цены по Monteros Heights Residences.',
  'أودّ معرفة التوافر والأسعار الحالية لمشروع Monteros Heights Residences.',
  'Ik ontvang graag de actuele beschikbaarheid en prijzen van Monteros Heights Residences.',
  'Chciałbym poznać aktualną dostępność i ceny Monteros Heights Residences.',
  'Jeg vil gjerne ha oppdatert tilgjengelighet og priser for Monteros Heights Residences.',
  'Jag skulle vilja ha aktuell tillgänglighet och aktuella priser för Monteros Heights Residences.')
a('.seo.title',
  'Monteros Heights Residences - viviendas nuevas en Marbella', 'Monteros Heights Residences - logements neufs à Marbella',
  'Monteros Heights Residences - Neubau in Marbella', 'Monteros Heights Residences - новые квартиры в Марбелье',
  'Monteros Heights Residences - مساكن جديدة في ماربيا', 'Monteros Heights Residences - nieuwbouw in Marbella',
  'Monteros Heights Residences - nowe lokale w Marbelli', 'Monteros Heights Residences - nye boliger i Marbella',
  'Monteros Heights Residences - nya bostäder i Marbella')
a('.seo.h1',
  'Monteros Heights Residences: 10 de 14 viviendas listadas, Marbella', 'Monteros Heights Residences : 10 logements sur 14 listés, Marbella',
  'Monteros Heights Residences: 10 von 14 gelisteten Wohnungen, Marbella', 'Monteros Heights Residences: 10 из 14 квартир списка, Марбелья',
  'Monteros Heights Residences: 10 من أصل 14 مسكنًا مدرجًا، ماربيا', 'Monteros Heights Residences: 10 van 14 vermelde woningen, Marbella',
  'Monteros Heights Residences: 10 z 14 lokali z listy, Marbella', 'Monteros Heights Residences: 10 av 14 oppførte boliger, Marbella',
  'Monteros Heights Residences: 10 av 14 upptagna bostäder, Marbella')
a('.seo.h1Context',
  '10 de 14 viviendas listadas, Marbella', '10 logements sur 14 listés, Marbella', '10 von 14 gelisteten Wohnungen, Marbella', '10 из 14 квартир списка, Марбелья',
  '10 من أصل 14 مسكنًا مدرجًا، ماربيا', '10 van 14 vermelde woningen, Marbella', '10 z 14 lokali z listy, Marbella', '10 av 14 oppførte boliger, Marbella', '10 av 14 upptagna bostäder, Marbella')

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings to', f'{SP}/tr_a.json')
