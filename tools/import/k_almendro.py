# -*- coding: utf-8 -*-
"""Almendro Homes: the strings the translation memory did not have.

Keyed by the path of the first occurrence in the English project.json, as scaffold.py prints
them, so the script reads the English from <dir>/todo.json instead of repeating it. If the
English moves, the path still finds the new sentence; if a path disappears the assert fires.
Tokens: {E332000} money, {N107.82} decimal number, {U} the area unit.

    python3 tools/import/scaffold.py <dir> almendro-homes     (writes <dir>/todo.json)
    python3 tools/import/k_almendro.py <dir>                  (writes <dir>/tr_z.json)
    python3 tools/import/assemble.py <dir> almendro-homes

Unit sizes, references and floors are not translated here: the page renders them in the
reader's language from SIZE_LABELS and FLOOR_PARTS, as for Guadalmansa Terrace, so the unit
overlay is stripped after assemble (they are only given a pass-through value so that
assemble does not refuse).
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TODO = json.load(open(f'{SP}/todo.json'))
BY_PATH = {paths[0]: en for en, paths in TODO.items()}
ALL_PATHS = {p: en for en, paths in TODO.items() for p in paths}
T = {}
USED = set()


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


def P(path, *tr):
    assert len(tr) == 9, (path, len(tr))
    en = ALL_PATHS[path]
    assert en not in T, path
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}
    USED.add(en)


def same(path):
    en = ALL_PATHS[path]
    T[en] = {l: en for l in LOCS}
    USED.add(en)


# identifiers: the invented name reads the same everywhere
same('.name'); same('.shortName'); same('.titleHtml')

P('.description',
  "12 apartamentos y áticos de dos dormitorios a la venta en una urbanización cerrada de viviendas contemporáneas junto a un club de golf en Estepona, con piscina comunitaria, gimnasio y jardines. Los documentos del promotor no indican fecha de finalización. Desde {E332000} más IVA.",
  "12 appartements et penthouses de deux chambres annoncés dans une résidence fermée de logements contemporains à côté d’un club de golf à Estepona, avec piscine commune, salle de sport et jardins. Les documents du promoteur ne donnent aucune date d’achèvement. À partir de {E332000} hors TVA.",
  "12 Wohnungen und Penthäuser mit zwei Schlafzimmern in einer geschlossenen Wohnanlage mit zeitgenössischen Wohnungen neben einem Golfclub in Estepona, mit Gemeinschaftspool, Fitnessraum und Gärten. Die Unterlagen des Bauträgers nennen keinen Fertigstellungstermin. Ab {E332000} zuzüglich MwSt.",
  "12 апартаментов и пентхаусов с двумя спальнями в закрытом комплексе современных жилых домов рядом с гольф-клубом в Эстепоне: общий бассейн, тренажёрный зал и сады. В документах застройщика нет срока завершения. От {E332000} плюс НДС.",
  "12 شقة وبنتهاوس بغرفتي نوم معروضة في مجمع مغلق من المنازل المعاصرة بجوار نادي غولف في إستيبونا، مع مسبح مشترك وصالة رياضية وحدائق. لا تذكر وثائق المطوّر موعد الإنجاز. ابتداءً من {E332000} زائد ضريبة القيمة المضافة.",
  "12 appartementen en penthouses met twee slaapkamers in een besloten complex met eigentijdse woningen naast een golfclub in Estepona, met een gemeenschappelijk zwembad, een fitnessruimte en tuinen. De documenten van de ontwikkelaar noemen geen opleveringsdatum. Vanaf {E332000} plus btw.",
  "12 apartamentów i penthouse’ów z dwiema sypialniami w zamkniętym osiedlu nowoczesnych domów obok klubu golfowego w Esteponie, ze wspólnym basenem, siłownią i ogrodami. Dokumenty dewelopera nie podają terminu ukończenia. Od {E332000} plus VAT.",
  "12 leiligheter og toppleiligheter med to soverom annonsert i et bevoktet område med moderne boliger ved siden av en golfklubb i Estepona, med felles basseng, treningsrom og hager. Utbyggerens dokumenter oppgir ingen ferdigstillelsesdato. Fra {E332000} pluss mva.",
  "12 lägenheter och takvåningar med två sovrum listade i ett bevakat område med moderna bostäder intill en golfklubb i Estepona, med gemensam pool, gym och trädgårdar. Exploatörens dokument anger inget färdigställandedatum. Från {E332000} plus moms.")

P('.seoDescription',
  "12 apartamentos y áticos de dos dormitorios en una urbanización cerrada junto a un club de golf en Estepona, de {N107.82} a {N126.50} {U} construidos, con piscina comunitaria y gimnasio, desde {E332000} más IVA.",
  "12 appartements et penthouses de deux chambres dans une résidence fermée à côté d’un club de golf à Estepona, de {N107.82} à {N126.50} {U} construits, avec piscine commune et salle de sport, à partir de {E332000} hors TVA.",
  "12 Wohnungen und Penthäuser mit zwei Schlafzimmern in einer geschlossenen Wohnanlage neben einem Golfclub in Estepona, {N107.82} bis {N126.50} {U} bebaut, mit Gemeinschaftspool und Fitnessraum, ab {E332000} zuzüglich MwSt.",
  "12 апартаментов и пентхаусов с двумя спальнями в закрытом комплексе рядом с гольф-клубом в Эстепоне, от {N107.82} до {N126.50} {U} застройки, общий бассейн и тренажёрный зал, от {E332000} плюс НДС.",
  "12 شقة وبنتهاوس بغرفتي نوم في مجمع مغلق بجوار نادي غولف في إستيبونا، من {N107.82} إلى {N126.50} {U} مبنية، مع مسبح مشترك وصالة رياضية، ابتداءً من {E332000} زائد ضريبة القيمة المضافة.",
  "12 appartementen en penthouses met twee slaapkamers in een besloten complex naast een golfclub in Estepona, {N107.82} tot {N126.50} {U} bebouwd, met een gemeenschappelijk zwembad en een fitnessruimte, vanaf {E332000} plus btw.",
  "12 apartamentów i penthouse’ów z dwiema sypialniami w zamkniętym osiedlu obok klubu golfowego w Esteponie, od {N107.82} do {N126.50} {U} powierzchni zabudowy, ze wspólnym basenem i siłownią, od {E332000} plus VAT.",
  "12 leiligheter og toppleiligheter med to soverom i et bevoktet område ved siden av en golfklubb i Estepona, {N107.82} til {N126.50} {U} bygd, med felles basseng og treningsrom, fra {E332000} pluss mva.",
  "12 lägenheter och takvåningar med två sovrum i ett bevakat område intill en golfklubb i Estepona, {N107.82} till {N126.50} {U} byggyta, med gemensam pool och gym, från {E332000} plus moms.")

P('.twitterDescription',
  "Apartamentos y áticos de dos dormitorios junto a un club de golf en Estepona, desde {E332000} más IVA.",
  "Appartements et penthouses de deux chambres à côté d’un club de golf à Estepona, à partir de {E332000} hors TVA.",
  "Wohnungen und Penthäuser mit zwei Schlafzimmern neben einem Golfclub in Estepona, ab {E332000} zuzüglich MwSt.",
  "Апартаменты и пентхаусы с двумя спальнями рядом с гольф-клубом в Эстепоне, от {E332000} плюс НДС.",
  "شقق وبنتهاوس بغرفتي نوم بجوار نادي غولف في إستيبونا، ابتداءً من {E332000} زائد ضريبة القيمة المضافة.",
  "Appartementen en penthouses met twee slaapkamers naast een golfclub in Estepona, vanaf {E332000} plus btw.",
  "Apartamenty i penthouse’y z dwiema sypialniami obok klubu golfowego w Esteponie, od {E332000} plus VAT.",
  "Leiligheter og toppleiligheter med to soverom ved siden av en golfklubb i Estepona, fra {E332000} pluss mva.",
  "Lägenheter och takvåningar med två sovrum intill en golfklubb i Estepona, från {E332000} plus moms.")

P('.hero.eyebrow',
  "12 viviendas a la venta", "12 logements annoncés", "12 Wohnungen gelistet", "В продаже 12 квартир",
  "12 منزلًا معروضًا", "12 woningen te koop", "Dostępnych 12 mieszkań", "12 boliger annonsert", "12 bostäder listade")

P('.hero.startingPrice',
  "Desde {E332000} + IVA", "À partir de {E332000} + TVA", "Ab {E332000} + MwSt.", "От {E332000} + НДС",
  "ابتداءً من {E332000} + ضريبة القيمة المضافة", "Vanaf {E332000} + btw", "Od {E332000} + VAT", "Fra {E332000} + mva.", "Från {E332000} + moms")

P('.card.description',
  "12 apartamentos y áticos de dos dormitorios en una urbanización cerrada junto a un club de golf en Estepona, con piscina comunitaria y gimnasio.",
  "12 appartements et penthouses de deux chambres dans une résidence fermée à côté d’un club de golf à Estepona, avec piscine commune et salle de sport.",
  "12 Wohnungen und Penthäuser mit zwei Schlafzimmern in einer geschlossenen Wohnanlage neben einem Golfclub in Estepona, mit Gemeinschaftspool und Fitnessraum.",
  "12 апартаментов и пентхаусов с двумя спальнями в закрытом комплексе рядом с гольф-клубом в Эстепоне, с общим бассейном и тренажёрным залом.",
  "12 شقة وبنتهاوس بغرفتي نوم في مجمع مغلق بجوار نادي غولف في إستيبونا، مع مسبح مشترك وصالة رياضية.",
  "12 appartementen en penthouses met twee slaapkamers in een besloten complex naast een golfclub in Estepona, met een gemeenschappelijk zwembad en een fitnessruimte.",
  "12 apartamentów i penthouse’ów z dwiema sypialniami w zamkniętym osiedlu obok klubu golfowego w Esteponie, ze wspólnym basenem i siłownią.",
  "12 leiligheter og toppleiligheter med to soverom i et bevoktet område ved siden av en golfklubb i Estepona, med felles basseng og treningsrom.",
  "12 lägenheter och takvåningar med två sovrum i ett bevakat område intill en golfklubb i Estepona, med gemensam pool och gym.")

P('.card.meta[0][1]',
  "{E332000} + IVA", "{E332000} + TVA", "{E332000} + MwSt.", "{E332000} + НДС",
  "{E332000} + ضريبة القيمة المضافة", "{E332000} + btw", "{E332000} + VAT", "{E332000} + mva.", "{E332000} + moms")

# ---- the four section images and the gallery
P('.images.hero.alt',
  "Vista generada por ordenador de un bloque de apartamentos de tres niveles con largas terrazas, visto a través de una piscina comunitaria y un césped",
  "Vue générée par ordinateur d’un immeuble de trois niveaux aux longues terrasses, vu au-delà d’une piscine commune et d’une pelouse",
  "Computergenerierte Ansicht eines dreigeschossigen Wohnblocks mit langen Terrassen, gesehen über einen Gemeinschaftspool und einen Rasen hinweg",
  "Компьютерная визуализация трёхэтажного жилого корпуса с длинными террасами, вид через общий бассейн и газон",
  "منظر مولَّد بالحاسوب لمبنى سكني من ثلاثة طوابق بتراسات طويلة، يُرى عبر مسبح مشترك ومساحة عشبية",
  "Computergegenereerd beeld van een appartementengebouw met drie bouwlagen en lange terrassen, gezien over een gemeenschappelijk zwembad en een gazon",
  "Wygenerowany komputerowo widok trzykondygnacyjnego bloku apartamentów z długimi tarasami, widziany ponad wspólnym basenem i trawnikiem",
  "Datagenerert bilde av en leilighetsblokk i tre etasjer med lange terrasser, sett over et felles basseng og en plen",
  "Datorgenererad vy av ett flerbostadshus i tre våningar med långa terrasser, sett över en gemensam pool och en gräsmatta")

P('.images.architecture.alt',
  "Vista generada por ordenador de un largo bloque de apartamentos de cuatro niveles con terrazas de antepechos de cristal, visto a través de un césped",
  "Vue générée par ordinateur d’un long immeuble de quatre niveaux aux terrasses à garde-corps en verre, vu au-delà d’une pelouse",
  "Computergenerierte Ansicht eines langen viergeschossigen Wohnblocks mit Glasbrüstungen an den Terrassen, gesehen über einen Rasen hinweg",
  "Компьютерная визуализация длинного четырёхэтажного жилого корпуса с террасами со стеклянным ограждением, вид через газон",
  "منظر مولَّد بالحاسوب لمبنى سكني طويل من أربعة طوابق بتراسات بحواجز زجاجية، يُرى عبر مساحة عشبية",
  "Computergegenereerd beeld van een lang appartementengebouw met vier bouwlagen en terrassen met glazen balustrades, gezien over een gazon",
  "Wygenerowany komputerowo widok długiego czterokondygnacyjnego bloku apartamentów z tarasami o szklanych balustradach, widziany ponad trawnikiem",
  "Datagenerert bilde av en lang leilighetsblokk i fire etasjer med terrasser med glassrekkverk, sett over en plen",
  "Datorgenererad vy av ett långt flerbostadshus i fyra våningar med terrasser med glasräcken, sett över en gräsmatta")

P('.images.lifestyle.alt',
  "Vista generada por ordenador de una terraza cubierta con mobiliario de descanso y vistas al mar y a la costa",
  "Vue générée par ordinateur d’une terrasse couverte avec salon d’extérieur et vue sur la mer et la côte",
  "Computergenerierte Ansicht einer überdachten Terrasse mit Loungemöbeln und Blick auf das Meer und die Küste",
  "Компьютерная визуализация крытой террасы с мебелью для отдыха и видом на море и побережье",
  "منظر مولَّد بالحاسوب لتراس مغطى بأثاث جلوس وإطلالة على البحر والساحل",
  "Computergegenereerd beeld van een overdekt terras met loungemeubilair en uitzicht op de zee en de kust",
  "Wygenerowany komputerowo widok zadaszonego tarasu z meblami wypoczynkowymi i widokiem na morze i wybrzeże",
  "Datagenerert bilde av en overbygd terrasse med loungemøbler og utsikt over havet og kysten",
  "Datorgenererad vy av en övertäckt terrass med loungemöbler och utsikt över havet och kusten")

P('.images.privateViewing.alt',
  "Vista generada por ordenador de una terraza al anochecer con dos tumbonas, un sofá y jardineras iluminadas, frente a un salón acristalado",
  "Vue générée par ordinateur d’une terrasse au crépuscule avec deux bains de soleil, un canapé et des jardinières éclairées, devant un séjour vitré",
  "Computergenerierte Ansicht einer Terrasse in der Abenddämmerung mit zwei Sonnenliegen, einem Sofa und beleuchteten Pflanzgefäßen vor einem verglasten Wohnbereich",
  "Компьютерная визуализация террасы в сумерках с двумя шезлонгами, диваном и подсвеченными кадками с растениями перед остеклённой гостиной",
  "منظر مولَّد بالحاسوب لتراس عند الغسق مع كرسيين للاسترخاء وأريكة وأحواض نباتات مضاءة، أمام غرفة معيشة زجاجية",
  "Computergegenereerd beeld van een terras bij schemering met twee ligbedden, een bank en verlichte plantenbakken, voor een glazen woonkamer",
  "Wygenerowany komputerowo widok tarasu o zmierzchu z dwoma leżakami, sofą i podświetlonymi donicami, przed przeszklonym salonem",
  "Datagenerert bilde av en terrasse i skumringen med to solsenger, en sofa og opplyste plantekasser, foran en glassfasade til stuen",
  "Datorgenererad vy av en terrass i skymningen med två solsängar, en soffa och upplysta planteringslådor, framför ett glasat vardagsrum")

P('.media.copy',
  "Vistas generadas por ordenador del conjunto y de los interiores, y planos de las 12 viviendas que figuran en la lista.",
  "Vues générées par ordinateur de la résidence et des intérieurs, et plans des 12 logements annoncés.",
  "Computergenerierte Ansichten der Anlage und der Innenräume sowie Grundrisse der 12 gelisteten Wohnungen.",
  "Компьютерные визуализации комплекса и интерьеров, а также планировки 12 квартир из списка.",
  "مناظر مولَّدة بالحاسوب للمجمع وللتصاميم الداخلية، ومخططات المنازل الـ12 المعروضة.",
  "Computergegenereerde beelden van het complex en van de interieurs, en plattegronden van de 12 woningen op de lijst.",
  "Wygenerowane komputerowo widoki osiedla i wnętrz oraz rzuty 12 mieszkań z listy.",
  "Datagenererte bilder av anlegget og interiørene, og plantegninger for de 12 boligene som er oppført.",
  "Datorgenererade bilder av området och interiörerna, samt planritningar för de 12 bostäder som är listade.")

P('.media.note',
  "Todas las imágenes son ilustraciones generadas por ordenador, no fotografías del edificio terminado, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los del promotor en fase de proyecto: las hojas de planta baja llevan fecha de abril de 2024 y las demás de diciembre de 2024, y las superficies que figuran en ellos son aproximadas y están sujetas al proyecto definitivo. Los nombres de las estancias en los planos están en español.",
  "Toutes les images sont des illustrations générées par ordinateur, et non des photographies du bâtiment achevé, et le mobilier et la décoration qui y figurent sont illustratifs et non inclus. Les plans sont ceux du promoteur au stade du projet : les feuilles du rez-de-chaussée sont datées d’avril 2024 et les autres de décembre 2024, et les surfaces qui y figurent sont approximatives et sous réserve du projet définitif. Les noms des pièces sur les plans sont en espagnol.",
  "Alle Bilder sind computergenerierte Darstellungen und keine Fotografien des fertigen Gebäudes; die gezeigten Möbel und die Dekoration dienen der Illustration und sind nicht enthalten. Die Grundrisse sind die Pläne des Bauträgers im Projektstadium: Die Blätter der Erdgeschosswohnungen sind auf April 2024 datiert, die übrigen auf Dezember 2024, und die darauf angegebenen Flächen sind ungefähr und vorbehaltlich des endgültigen Projekts. Die Raumbezeichnungen in den Plänen sind auf Spanisch.",
  "Все изображения — компьютерные визуализации, а не фотографии готового здания; мебель и декор на них носят иллюстративный характер и в стоимость не входят. Планировки — это проектные планы застройщика: листы первого этажа датированы апрелем 2024 года, остальные — декабрём 2024 года; указанные на них площади приблизительны и зависят от окончательного проекта. Названия помещений на планах даны на испанском языке.",
  "جميع الصور رسوم مولَّدة بالحاسوب وليست صورًا فوتوغرافية للمبنى المكتمل، والأثاث والديكور الظاهران فيها توضيحيان وغير مشمولين. المخططات هي مخططات المطوّر في مرحلة المشروع: مخططات الطابق الأرضي مؤرخة في أبريل 2024 والبقية في ديسمبر 2024، والمساحات الواردة فيها تقريبية وتخضع للمشروع النهائي. أسماء الغرف في المخططات بالإسبانية.",
  "Alle beelden zijn computergegenereerde illustraties en geen foto’s van het afgewerkte gebouw, en het meubilair en de inrichting die erop te zien zijn, dienen ter illustratie en zijn niet inbegrepen. De plattegronden zijn de projectplannen van de ontwikkelaar: de bladen van de begane grond zijn gedateerd april 2024 en de overige december 2024, en de oppervlakten erop zijn bij benadering en onder voorbehoud van het definitieve project. De ruimtenamen op de plattegronden zijn in het Spaans.",
  "Wszystkie obrazy to wizualizacje komputerowe, a nie zdjęcia ukończonego budynku, a meble i dekoracje na nich mają charakter ilustracyjny i nie są wliczone. Rzuty to plany projektowe dewelopera: arkusze parteru są datowane na kwiecień 2024 r., pozostałe na grudzień 2024 r., a podane na nich powierzchnie są przybliżone i zależą od ostatecznego projektu. Nazwy pomieszczeń na rzutach są po hiszpańsku.",
  "Alle bildene er datagenererte illustrasjoner, ikke fotografier av den ferdige bygningen, og møblene og dekorasjonen på dem er illustrasjoner og er ikke inkludert. Plantegningene er utbyggerens prosjektplaner: arkene for første etasje er datert april 2024 og de øvrige desember 2024, og arealene på dem er omtrentlige og med forbehold om det endelige prosjektet. Romnavnene på plantegningene er på spansk.",
  "Alla bilder är datorgenererade illustrationer, inte fotografier av den färdiga byggnaden, och möblerna och inredningen på dem är illustrativa och ingår inte. Planritningarna är exploatörens projektplaner: ritningarna för bottenvåningen är daterade april 2024 och de övriga december 2024, och ytorna på dem är ungefärliga och med förbehåll för det slutliga projektet. Rumsnamnen på ritningarna är på spanska.")

P('.media.items[0].caption',
  "La piscina y los bloques en terrazas", "La piscine et les immeubles en terrasses", "Der Pool und die Terrassenblöcke",
  "Бассейн и террасные корпуса", "المسبح والمباني المتدرجة بالتراسات", "Het zwembad en de gebouwen met terrassen",
  "Basen i tarasowe bloki", "Bassenget og blokkene med terrasser", "Poolen och husen med terrasser")

P('.media.items[1].alt',
  "Vista aérea generada por ordenador de bloques de apartamentos blancos junto a un campo de golf, con el mar y la costa al fondo",
  "Vue aérienne générée par ordinateur d’immeubles blancs à côté d’un terrain de golf, avec la mer et la côte au loin",
  "Computergenerierte Luftaufnahme weißer Wohnblöcke neben einem Golfplatz, mit dem Meer und der Küste in der Ferne",
  "Компьютерная визуализация с высоты: белые жилые корпуса рядом с полем для гольфа, вдали видны море и побережье",
  "منظر جوي مولَّد بالحاسوب لمبانٍ سكنية بيضاء بجوار ملعب غولف، ويظهر البحر والساحل في البعيد",
  "Computergegenereerde luchtfoto van witte appartementengebouwen naast een golfbaan, met de zee en de kust in de verte",
  "Wygenerowany komputerowo widok z lotu ptaka na białe bloki apartamentów obok pola golfowego, z morzem i wybrzeżem w oddali",
  "Datagenerert luftbilde av hvite leilighetsblokker ved siden av en golfbane, med havet og kysten i det fjerne",
  "Datorgenererad flygvy av vita flerbostadshus intill en golfbana, med havet och kusten i fjärran")

P('.media.items[1].caption',
  "Los bloques junto al campo de golf", "Les immeubles à côté du golf", "Die Blöcke neben dem Golfplatz",
  "Корпуса рядом с полем для гольфа", "المباني بجوار ملعب الغولف", "De gebouwen naast de golfbaan",
  "Bloki obok pola golfowego", "Blokkene ved siden av golfbanen", "Husen intill golfbanan")

P('.media.items[2].alt',
  "Vista aérea generada por ordenador de los bloques de apartamentos alrededor de una piscina, con colinas arboladas y montañas detrás",
  "Vue aérienne générée par ordinateur des immeubles autour d’une piscine, avec des collines boisées et des montagnes derrière",
  "Computergenerierte Luftaufnahme der Wohnblöcke rund um einen Pool, dahinter bewaldete Hügel und Berge",
  "Компьютерная визуализация с высоты: жилые корпуса вокруг бассейна, позади — лесистые холмы и горы",
  "منظر جوي مولَّد بالحاسوب للمباني السكنية حول مسبح، وخلفها تلال حرجية وجبال",
  "Computergegenereerde luchtfoto van de appartementengebouwen rond een zwembad, met bebost heuvelland en bergen erachter",
  "Wygenerowany komputerowo widok z lotu ptaka na bloki apartamentów wokół basenu, z zalesionymi wzgórzami i górami w tle",
  "Datagenerert luftbilde av leilighetsblokkene rundt et basseng, med skogkledde åser og fjell bak",
  "Datorgenererad flygvy av flerbostadshusen kring en pool, med skogklädda kullar och berg bakom")

P('.media.items[2].caption',
  "El conjunto desde el aire", "La résidence vue du ciel", "Die Anlage aus der Luft",
  "Комплекс с высоты", "المجمع من الجو", "Het complex vanuit de lucht",
  "Osiedle z lotu ptaka", "Anlegget fra luften", "Området från luften")

P('.media.items[3].caption',
  "Los bloques desde el césped", "Les immeubles vus depuis la pelouse", "Die Blöcke vom Rasen aus",
  "Корпуса со стороны газона", "المباني من جهة المساحة العشبية", "De gebouwen vanaf het gazon",
  "Bloki widziane od strony trawnika", "Blokkene sett fra plenen", "Husen sedda från gräsmattan")

P('.media.items[4].alt',
  "Vista generada por ordenador al anochecer de los bloques de apartamentos con un edificio acristalado para el gimnasio en los jardines",
  "Vue générée par ordinateur au crépuscule des immeubles avec un bâtiment vitré abritant la salle de sport dans les jardins",
  "Computergenerierte Abendansicht der Wohnblöcke mit einem verglasten Fitnessgebäude in den Gärten",
  "Компьютерная визуализация жилых корпусов в сумерках с остеклённым зданием тренажёрного зала в садах",
  "منظر مولَّد بالحاسوب عند الغسق للمباني السكنية مع مبنى زجاجي للصالة الرياضية في الحدائق",
  "Computergegenereerd beeld bij schemering van de appartementengebouwen met een glazen fitnessgebouw in de tuinen",
  "Wygenerowany komputerowo widok bloków apartamentów o zmierzchu z przeszklonym budynkiem siłowni w ogrodach",
  "Datagenerert bilde i skumringen av leilighetsblokkene med en glassbygning for treningsrommet i hagene",
  "Datorgenererad skymningsvy av flerbostadshusen med en glasad gymbyggnad i trädgårdarna")

P('.media.items[4].caption',
  "El gimnasio y los bloques al anochecer", "La salle de sport et les immeubles au crépuscule", "Der Fitnessraum und die Blöcke in der Abenddämmerung",
  "Тренажёрный зал и корпуса в сумерках", "الصالة الرياضية والمباني عند الغسق", "De fitnessruimte en de gebouwen bij schemering",
  "Siłownia i bloki o zmierzchu", "Treningsrommet og blokkene i skumringen", "Gymmet och husen i skymningen")

P('.media.items[5].caption',
  "Una terraza con vistas a la costa", "Une terrasse avec vue sur la côte", "Eine Terrasse mit Blick auf die Küste",
  "Терраса с видом на побережье", "تراس بإطلالة على الساحل", "Een terras met uitzicht op de kust",
  "Taras z widokiem na wybrzeże", "En terrasse med utsikt over kysten", "En terrass med utsikt över kusten")

P('.media.items[6].caption',
  "Una terraza al anochecer", "Une terrasse au crépuscule", "Eine Terrasse in der Abenddämmerung",
  "Терраса в сумерках", "تراس عند الغسق", "Een terras bij schemering",
  "Taras o zmierzchu", "En terrasse i skumringen", "En terrass i skymningen")

P('.media.items[7].alt',
  "Salón-comedor de planta abierta generado por ordenador, con isla de cocina, sofá rinconero y puertas correderas a la terraza",
  "Séjour-salle à manger ouvert généré par ordinateur, avec îlot de cuisine, canapé d’angle et portes coulissantes vers la terrasse",
  "Computergenerierter offener Wohn- und Essbereich mit Kochinsel, Ecksofa und Schiebetüren zur Terrasse",
  "Компьютерная визуализация гостиной-столовой открытой планировки с кухонным островом, угловым диваном и раздвижными дверями на террасу",
  "غرفة معيشة وطعام مفتوحة مولَّدة بالحاسوب مع جزيرة مطبخ وأريكة زاوية وأبواب منزلقة إلى التراس",
  "Computergegenereerde open woon- en eetkamer met een keukeneiland, een hoekbank en schuifdeuren naar het terras",
  "Wygenerowany komputerowo otwarty salon z jadalnią, wyspą kuchenną, sofą narożną i przesuwnymi drzwiami na taras",
  "Datagenerert åpen stue og spisestue med kjøkkenøy, hjørnesofa og skyvedører til terrassen",
  "Datorgenererat vardagsrum och matplats i öppen planlösning med köksö, hörnsoffa och skjutdörrar till terrassen")

P('.media.items[8].alt',
  "Dormitorio generado por ordenador con cama doble, armario empotrado y puerta de cristal a una terraza",
  "Chambre générée par ordinateur avec lit double, placard intégré et porte vitrée donnant sur une terrasse",
  "Computergeneriertes Schlafzimmer mit Doppelbett, Einbauschrank und Glastür zu einer Terrasse",
  "Компьютерная визуализация спальни с двуспальной кроватью, встроенным шкафом и стеклянной дверью на террасу",
  "غرفة نوم مولَّدة بالحاسوب بسرير مزدوج وخزانة مدمجة وباب زجاجي إلى تراس",
  "Computergegenereerde slaapkamer met een tweepersoonsbed, een inbouwkast en een glazen deur naar een terras",
  "Wygenerowana komputerowo sypialnia z łóżkiem małżeńskim, zabudowaną szafą i szklanymi drzwiami na taras",
  "Datagenerert soverom med dobbeltseng, innebygd garderobeskap og glassdør til en terrasse",
  "Datorgenererat sovrum med dubbelsäng, inbyggd garderob och glasdörr till en terrass")

P('.media.items[9].alt',
  "Dormitorio generado por ordenador con cama doble frente a una pared con estampado de palmeras y armario empotrado",
  "Chambre générée par ordinateur avec lit double devant un mur à motif de palmiers et placard intégré",
  "Computergeneriertes Schlafzimmer mit Doppelbett vor einer Wand mit Palmenmotiv und Einbauschrank",
  "Компьютерная визуализация спальни с двуспальной кроватью у стены с принтом из пальм и встроенным шкафом",
  "غرفة نوم مولَّدة بالحاسوب بسرير مزدوج أمام جدار بنقوش النخيل وخزانة مدمجة",
  "Computergegenereerde slaapkamer met een tweepersoonsbed tegen een wand met palmenprint en een inbouwkast",
  "Wygenerowana komputerowo sypialnia z łóżkiem małżeńskim przy ścianie z motywem palm i zabudowaną szafą",
  "Datagenerert soverom med dobbeltseng mot en vegg med palmemotiv og innebygd garderobeskap",
  "Datorgenererat sovrum med dubbelsäng mot en vägg med palmmotiv och inbyggd garderob")

P('.media.items[10].alt',
  "Baño generado por ordenador con mueble de lavabo suspendido, inodoro y ducha a ras de suelo tras una mampara de cristal",
  "Salle de bains générée par ordinateur avec meuble-vasque suspendu, WC et douche à l’italienne derrière une paroi en verre",
  "Computergeneriertes Badezimmer mit wandhängendem Waschtisch, Toilette und bodengleicher Dusche hinter einer Glasscheibe",
  "Компьютерная визуализация ванной комнаты с подвесной тумбой с раковиной, унитазом и душевой зоной за стеклянной перегородкой",
  "حمام مولَّد بالحاسوب بوحدة مغسلة معلّقة ومرحاض ودش مفتوح خلف حاجز زجاجي",
  "Computergegenereerde badkamer met een zwevend wastafelmeubel, een toilet en een inloopdouche achter een glazen wand",
  "Wygenerowana komputerowo łazienka z wiszącą szafką umywalkową, toaletą i prysznicem walk-in za szklaną ścianką",
  "Datagenerert bad med veggmontert servantskap, toalett og dusj med glassvegg",
  "Datorgenererat badrum med väggmonterat tvättskåp, toalett och duschhörna bakom en glasvägg")

# floorplan alt/caption: "Floorplan of home 2-2-BAJ-A" / "Home 2-2-BAJ-A"
ALT = ["Plano de la vivienda {r}", "Plan du logement {r}", "Grundriss der Wohnung {r}", "Планировка квартиры {r}", "مخطط المسكن {r}",
       "Plattegrond van woning {r}", "Rzut mieszkania {r}", "Plantegning av bolig {r}", "Planritning för bostad {r}"]
CAP = ["Vivienda {r}", "Logement {r}", "Wohnung {r}", "Квартира {r}", "المسكن {r}",
       "Woning {r}", "Mieszkanie {r}", "Bolig {r}", "Bostad {r}"]
REFS = ['2-2-BAJ-A', '2-2-BAJ-B', '3-1-ATC-A', '3-2-BAJ-A', '3-3-ATC-B', '5-1-BAJ-A', '5-1-1-A', '5-2-ATC-C', '5-3-ATC-A',
        '7-3-2-B', '8-3-2-B', '9-2-ATC-A']
for i, r in enumerate(REFS):
    P(f'.media.items[{11 + i}].alt', *[a.format(r=r) for a in ALT])
    P(f'.media.items[{11 + i}].caption', *[c.format(r=r) for c in CAP])

# ---- overview
P('.overview.headlineHtml',
  "Doce viviendas <em>en la lista</em>", "Douze logements <em>sur la liste</em>", "Zwölf Wohnungen <em>auf der Liste</em>",
  "Двенадцать квартир <em>в списке</em>", "اثنا عشر منزلًا <em>على القائمة</em>", "Twaalf woningen <em>op de lijst</em>",
  "Dwanaście mieszkań <em>na liście</em>", "Tolv boliger <em>på listen</em>", "Tolv bostäder <em>på listan</em>")

P('.overview.copy[0]',
  "Es una urbanización cerrada de apartamentos y áticos contemporáneos junto a un club de golf en Estepona. El portal del promotor la describe como 135 viviendas de uno, dos y tres dormitorios, orientadas al sur, con jardines en las viviendas de planta baja, solárium en los áticos, una piscina con zona de solárium, un gimnasio y jardines plantados con especies autóctonas. Llama a esta la primera fase y no indica cuántas de las 135 viviendas le corresponden.",
  "C’est une résidence fermée d’appartements et de penthouses contemporains à côté d’un club de golf à Estepona. Le portail du promoteur la décrit comme 135 logements d’une, deux et trois chambres, orientés au sud, avec des jardins pour les logements du rez-de-chaussée, des solariums pour les penthouses, une piscine avec solarium, une salle de sport et des jardins plantés d’espèces locales. Il la présente comme la première phase et n’indique pas combien des 135 logements en font partie.",
  "Die Anlage ist eine geschlossene Wohnanlage mit zeitgenössischen Wohnungen und Penthäusern neben einem Golfclub in Estepona. Das Portal des Bauträgers beschreibt sie als 135 Wohnungen mit einem, zwei und drei Schlafzimmern, nach Süden ausgerichtet, mit Gärten für die Erdgeschosswohnungen, Solarien für die Penthäuser, einem Pool mit Sonnenterrasse, einem Fitnessraum und mit einheimischen Pflanzen bepflanzten Gärten. Es nennt dies die erste Bauphase und gibt nicht an, wie viele der 135 Wohnungen dazugehören.",
  "Это закрытый комплекс современных апартаментов и пентхаусов рядом с гольф-клубом в Эстепоне. Портал застройщика описывает его как 135 квартир с одной, двумя и тремя спальнями, ориентированных на юг, с садами у квартир первого этажа, солярием у пентхаусов, бассейном с солярием, тренажёрным залом и садами с местными видами растений. Эта очередь названа первой, а сколько из 135 квартир к ней относится, не сказано.",
  "هذا مجمع مغلق من الشقق والبنتهاوس المعاصرة بجوار نادي غولف في إستيبونا. يصفه موقع المطوّر بأنه 135 منزلًا بغرفة نوم وغرفتين وثلاث غرف نوم، مواجهة للجنوب، مع حدائق لمنازل الطابق الأرضي وسولاريوم للبنتهاوس ومسبح بمنطقة تشمس وصالة رياضية وحدائق مزروعة بنباتات محلية. ويسمّي هذه المرحلة الأولى ولا يذكر كم من المنازل الـ135 تنتمي إليها.",
  "Dit is een besloten complex van eigentijdse appartementen en penthouses naast een golfclub in Estepona. Het portaal van de ontwikkelaar beschrijft het als 135 woningen met een, twee en drie slaapkamers, op het zuiden gericht, met tuinen bij de woningen op de begane grond, solariums bij de penthouses, een zwembad met zonneterras, een fitnessruimte en tuinen met inheemse beplanting. Het noemt dit de eerste fase en zegt niet hoeveel van de 135 woningen daarbij horen.",
  "To zamknięte osiedle nowoczesnych apartamentów i penthouse’ów obok klubu golfowego w Esteponie. Portal dewelopera opisuje je jako 135 mieszkań z jedną, dwiema i trzema sypialniami, o orientacji południowej, z ogrodami przy mieszkaniach na parterze, solariami przy penthouse’ach, basenem z tarasem słonecznym, siłownią i ogrodami obsadzonymi rodzimymi gatunkami roślin. Nazywa ten etap pierwszym i nie podaje, ile z tych 135 mieszkań do niego należy.",
  "Dette er et bevoktet område med moderne leiligheter og toppleiligheter ved siden av en golfklubb i Estepona. Utbyggerens portal beskriver det som 135 boliger med ett, to og tre soverom, vendt mot sør, med hager til boligene i første etasje, solterrasser til toppleilighetene, et basseng med solterrasse, et treningsrom og hager beplantet med stedegne arter. Den kaller dette første byggetrinn og sier ikke hvor mange av de 135 boligene som hører til det.",
  "Det här är ett bevakat område med moderna lägenheter och takvåningar intill en golfklubb i Estepona. Exploatörens portal beskriver det som 135 bostäder med ett, två och tre sovrum, vända mot söder, med trädgårdar till bostäderna på bottenvåningen, solterrasser till takvåningarna, en pool med solterrass, ett gym och trädgårdar planterade med inhemska arter. Den kallar detta första etappen och anger inte hur många av de 135 bostäderna som hör till den.")

P('.overview.copy[1]',
  "La lista de precios de esta fase recoge 12 viviendas, todas de dos dormitorios y dos baños: cuatro en planta baja, una en la primera planta, dos en la segunda y cinco áticos, en los bloques 2, 3, 5, 7, 8 y 9. Cada una figura con una plaza de garaje y un trastero. Ninguno de los documentos del promotor indica una fecha de finalización.",
  "La liste de prix de cette phase recense 12 logements, tous de deux chambres et deux salles de bain : quatre au rez-de-chaussée, un au premier étage, deux au deuxième étage et cinq penthouses, dans les blocs 2, 3, 5, 7, 8 et 9. Chacun est annoncé avec une place de garage et un local de rangement. Aucun des documents du promoteur ne donne de date d’achèvement.",
  "Die Preisliste dieser Bauphase führt 12 Wohnungen auf, alle mit zwei Schlafzimmern und zwei Bädern: vier im Erdgeschoss, eine im ersten Obergeschoss, zwei im zweiten Obergeschoss und fünf Penthäuser, in den Blöcken 2, 3, 5, 7, 8 und 9. Jede ist mit einem Garagenstellplatz und einem Abstellraum aufgeführt. Keines der Dokumente des Bauträgers nennt einen Fertigstellungstermin.",
  "В прайс-листе этой очереди указано 12 квартир, все с двумя спальнями и двумя ванными комнатами: четыре на первом этаже, одна на втором, две на третьем и пять пентхаусов, в блоках 2, 3, 5, 7, 8 и 9. У каждой указаны одно гаражное место и одна кладовая. Ни в одном из документов застройщика не указан срок завершения.",
  "تُظهر قائمة أسعار هذه المرحلة 12 منزلًا، جميعها بغرفتي نوم وحمامين: أربعة في الطابق الأرضي وواحد في الطابق الأول واثنان في الطابق الثاني وخمسة بنتهاوس، في المباني 2 و3 و5 و7 و8 و9. ويُدرج لكل منها موقف سيارات واحد في المرآب وغرفة تخزين واحدة. لا تذكر أي من وثائق المطوّر موعدًا للإنجاز.",
  "De prijslijst van deze fase toont 12 woningen, allemaal met twee slaapkamers en twee badkamers: vier op de begane grond, een op de eerste verdieping, twee op de tweede verdieping en vijf penthouses, in de blokken 2, 3, 5, 7, 8 en 9. Elk staat vermeld met een garageplaats en een berging. In geen van de documenten van de ontwikkelaar staat een opleveringsdatum.",
  "Cennik tego etapu wymienia 12 mieszkań, wszystkie z dwiema sypialniami i dwiema łazienkami: cztery na parterze, jedno na pierwszym piętrze, dwa na drugim piętrze i pięć penthouse’ów, w blokach 2, 3, 5, 7, 8 i 9. Każde jest podane z jednym miejscem w garażu i jedną komórką lokatorską. W żadnym z dokumentów dewelopera nie ma terminu ukończenia.",
  "Prislisten for dette byggetrinnet viser 12 boliger, alle med to soverom og to bad: fire i første etasje, én i andre etasje, to i tredje etasje og fem toppleiligheter, i hus 2, 3, 5, 7, 8 og 9. Hver er oppført med én garasjeplass og ett bod. Ingen av utbyggerens dokumenter oppgir en ferdigstillelsesdato.",
  "Prislistan för den här etappen visar 12 bostäder, alla med två sovrum och två badrum: fyra på bottenvåningen, en på första våningen, två på andra våningen och fem takvåningar, i hus 2, 3, 5, 7, 8 och 9. Varje bostad är listad med en garageplats och ett förråd. Inget av exploatörens dokument anger ett färdigställandedatum.")

P('.overview.metrics[0][0]',
  "Viviendas a la venta", "Logements annoncés", "Gelistete Wohnungen", "Квартир в списке", "المنازل المعروضة",
  "Woningen op de lijst", "Mieszkania na liście", "Oppførte boliger", "Listade bostäder")
P('.overview.metrics[0][1]',
  "12 viviendas", "12 logements", "12 Wohnungen", "12 квартир", "12 منزلًا", "12 woningen", "12 mieszkań", "12 boliger", "12 bostäder")

# ---- why
P('.why.copy',
  "Viviendas de dos dormitorios junto a un club de golf en Estepona, desde viviendas en planta baja con porche hasta áticos, cada una con una plaza de garaje y un trastero.",
  "Logements de deux chambres à côté d’un club de golf à Estepona, des logements du rez-de-chaussée avec porche aux penthouses, chacun annoncé avec une place de garage et un local de rangement.",
  "Wohnungen mit zwei Schlafzimmern neben einem Golfclub in Estepona, von Erdgeschosswohnungen mit überdachter Terrasse bis zu Penthäusern, jede mit einem Garagenstellplatz und einem Abstellraum aufgeführt.",
  "Квартиры с двумя спальнями рядом с гольф-клубом в Эстепоне — от квартир первого этажа с крытой террасой до пентхаусов; у каждой указаны гаражное место и кладовая.",
  "منازل بغرفتي نوم بجوار نادي غولف في إستيبونا، من منازل الطابق الأرضي ذات الرواق إلى البنتهاوس، ويُدرج لكل منها موقف في المرآب وغرفة تخزين.",
  "Woningen met twee slaapkamers naast een golfclub in Estepona, van woningen op de begane grond met een overdekt terras tot penthouses, elk vermeld met een garageplaats en een berging.",
  "Mieszkania z dwiema sypialniami obok klubu golfowego w Esteponie, od mieszkań na parterze z werandą po penthouse’y, każde podane z miejscem w garażu i komórką lokatorską.",
  "Boliger med to soverom ved siden av en golfklubb i Estepona, fra boliger i første etasje med overbygd terrasse til toppleiligheter, hver oppført med en garasjeplass og et bod.",
  "Bostäder med två sovrum intill en golfklubb i Estepona, från bostäder på bottenvåningen med veranda till takvåningar, var och en listad med en garageplats och ett förråd.")

P('.why.points[0][1]',
  "Compradores que quieren una vivienda nueva de dos dormitorios y dos baños con una gran terraza o porche, y piscina y gimnasio en la urbanización, con un club de golf al lado.",
  "Acheteurs qui souhaitent un logement neuf de deux chambres et deux salles de bain avec une grande terrasse ou un porche, une piscine et une salle de sport dans la résidence, et un club de golf à côté.",
  "Käufer, die eine neue Wohnung mit zwei Schlafzimmern und zwei Bädern, einer großen Terrasse oder überdachten Veranda sowie Pool und Fitnessraum in der Anlage und einen Golfclub nebenan suchen.",
  "Покупатели, которым нужна новая квартира с двумя спальнями и двумя ванными комнатами, большой террасой или крытой верандой, бассейном и тренажёрным залом в комплексе и гольф-клубом по соседству.",
  "المشترون الذين يريدون منزلًا جديدًا بغرفتي نوم وحمامين مع تراس كبير أو رواق ومسبح وصالة رياضية في المجمع ونادي غولف مجاور.",
  "Kopers die een nieuwe woning met twee slaapkamers en twee badkamers willen, met een groot terras of een overdekt terras, een zwembad en een fitnessruimte in het complex en een golfclub naast de deur.",
  "Kupujący, którzy chcą nowego mieszkania z dwiema sypialniami i dwiema łazienkami, z dużym tarasem lub werandą, basenem i siłownią na osiedlu oraz klubem golfowym obok.",
  "Kjøpere som vil ha en ny bolig med to soverom og to bad med stor terrasse eller overbygd uteplass, basseng og treningsrom i anlegget og en golfklubb ved siden av.",
  "Köpare som vill ha en ny bostad med två sovrum och två badrum med en stor terrass eller veranda, pool och gym i området och en golfklubb alldeles intill.")

P('.why.points[1][1]',
  "Porches de unos 56 {U} o un jardín en la planta baja, terrazas en el resto de plantas, orientación sur y precios desde {E332000} más IVA.",
  "Porches d’environ 56 {U} ou jardin au rez-de-chaussée, terrasses à tous les autres étages, orientation sud et prix à partir de {E332000} hors TVA.",
  "Überdachte Terrassen von etwa 56 {U} oder ein Garten im Erdgeschoss, Terrassen auf allen anderen Etagen, Südausrichtung und Preise ab {E332000} zuzüglich MwSt.",
  "Крытые террасы около 56 {U} или сад на первом этаже, террасы на остальных этажах, ориентация на юг и цены от {E332000} плюс НДС.",
  "أروقة بنحو 56 {U} أو حديقة في الطابق الأرضي، وتراسات في بقية الطوابق، وواجهة جنوبية، وأسعار ابتداءً من {E332000} زائد ضريبة القيمة المضافة.",
  "Overdekte terrassen van ongeveer 56 {U} of een tuin op de begane grond, terrassen op alle andere verdiepingen, een zuidoriëntatie en prijzen vanaf {E332000} plus btw.",
  "Werandy o powierzchni około 56 {U} lub ogród na parterze, tarasy na pozostałych piętrach, orientacja południowa i ceny od {E332000} plus VAT.",
  "Overbygde uteplasser på omtrent 56 {U} eller en hage i første etasje, terrasser i de øvrige etasjene, sørvendt beliggenhet og priser fra {E332000} pluss mva.",
  "Verandor på cirka 56 {U} eller en trädgård på bottenvåningen, terrasser på övriga våningar, sydläge och priser från {E332000} plus moms.")

P('.why.points[2][1]',
  "El portal sitúa la urbanización junto a un club de golf en Estepona. Los documentos del promotor no indican distancias, así que medimos con usted el trayecto en coche a la playa, al centro y al aeropuerto.",
  "Le portail situe la résidence à côté d’un club de golf à Estepona. Les documents du promoteur n’indiquent aucune distance ; nous mesurons donc avec vous le trajet en voiture jusqu’à la plage, au centre-ville et à l’aéroport.",
  "Das Portal verortet die Anlage neben einem Golfclub in Estepona. Die Unterlagen des Bauträgers nennen keine Entfernungen, daher messen wir mit Ihnen die Fahrzeit zum Strand, zur Stadt und zum Flughafen.",
  "Портал указывает, что комплекс находится рядом с гольф-клубом в Эстепоне. В документах застройщика нет расстояний, поэтому время в пути до пляжа, города и аэропорта мы замеряем вместе с вами.",
  "يضع موقع المطوّر المجمع بجوار نادي غولف في إستيبونا. ولا تذكر وثائق المطوّر مسافات، لذا نقيس معك زمن الوصول بالسيارة إلى الشاطئ والمدينة والمطار.",
  "Het portaal plaatst het complex naast een golfclub in Estepona. De documenten van de ontwikkelaar noemen geen afstanden, dus we meten samen met u de rit naar het strand, de stad en het vliegveld.",
  "Portal umieszcza osiedle obok klubu golfowego w Esteponie. Dokumenty dewelopera nie podają odległości, dlatego razem z Państwem mierzymy czas dojazdu na plażę, do miasta i na lotnisko.",
  "Portalen plasserer anlegget ved siden av en golfklubb i Estepona. Utbyggerens dokumenter oppgir ingen avstander, så vi måler kjøretiden til stranden, byen og flyplassen sammen med deg.",
  "Portalen placerar området intill en golfklubb i Estepona. Exploatörens dokument anger inga avstånd, så vi mäter körtiden till stranden, staden och flygplatsen tillsammans med er.")

P('.why.points[3][1]',
  "Los documentos no indican fecha de finalización, y el portal menciona solárium en los áticos mientras que los planos de los que figuran en la lista muestran terrazas, así que confirmamos ambas cosas antes de cualquier reserva.",
  "Les documents ne donnent aucune date d’achèvement, et le portail mentionne des solariums sur les penthouses alors que les plans de ceux qui sont annoncés montrent des terrasses ; nous confirmons donc les deux points avant toute réservation.",
  "Die Unterlagen nennen keinen Fertigstellungstermin, und das Portal erwähnt Solarien bei den Penthäusern, während die Pläne der gelisteten Penthäuser Terrassen zeigen; beides klären wir vor jeder Reservierung.",
  "В документах нет срока завершения, а портал упоминает солярии у пентхаусов, тогда как на планах пентхаусов из списка показаны террасы, поэтому до бронирования мы уточняем и то и другое.",
  "لا تذكر الوثائق موعدًا للإنجاز، ويذكر موقع المطوّر سولاريوم للبنتهاوس بينما تُظهر مخططات المنازل المعروضة تراسات، لذا نؤكد الأمرين قبل أي حجز.",
  "In de documenten staat geen opleveringsdatum, en het portaal noemt solariums bij de penthouses terwijl de plattegronden van de vermelde penthouses terrassen tonen. Beide bevestigen we vóór elke reservering.",
  "Dokumenty nie podają terminu ukończenia, a portal wspomina o solariach przy penthouse’ach, podczas gdy rzuty wymienionych penthouse’ów pokazują tarasy, dlatego przed każdą rezerwacją potwierdzamy jedno i drugie.",
  "Dokumentene oppgir ingen ferdigstillelsesdato, og portalen nevner solterrasser på toppleilighetene mens plantegningene for de oppførte viser terrasser, så vi bekrefter begge deler før en reservasjon.",
  "Dokumenten anger inget färdigställandedatum, och portalen nämner solterrasser på takvåningarna medan planritningarna för de listade visar terrasser, så vi bekräftar båda delarna före varje reservation.")

# ---- architecture
P('.architecture.headlineHtml',
  "Bloques contemporáneos, <em>construidos en torno a las terrazas</em>",
  "Des immeubles contemporains, <em>organisés autour des terrasses</em>",
  "Zeitgenössische Blöcke, <em>um Terrassen herum gebaut</em>",
  "Современные корпуса, <em>построенные вокруг террас</em>",
  "مبانٍ معاصرة، <em>مبنية حول التراسات</em>",
  "Eigentijdse gebouwen, <em>gebouwd rond terrassen</em>",
  "Nowoczesne bloki, <em>zbudowane wokół tarasów</em>",
  "Moderne blokker, <em>bygget rundt terrassene</em>",
  "Moderna hus, <em>byggda kring terrasserna</em>")

P('.architecture.copy[0]',
  "El portal del promotor describe el diseño como contemporáneo. En las vistas generadas por ordenador, los bloques se elevan tres y cuatro niveles en largas bandas de terrazas con frentes de cristal, entre céspedes, con una piscina y un edificio acristalado para el gimnasio en los jardines.",
  "Le portail du promoteur décrit le design comme contemporain. Dans les vues générées par ordinateur, les immeubles s’élèvent sur trois et quatre niveaux en longues bandes de terrasses à façade vitrée, au milieu de pelouses, avec une piscine et un bâtiment vitré abritant la salle de sport dans les jardins.",
  "Das Portal des Bauträgers beschreibt das Design als zeitgenössisch. In den computergenerierten Ansichten erheben sich die Blöcke über drei und vier Ebenen in langen Terrassenbändern mit Glasfronten, eingebettet in Rasenflächen, mit einem Pool und einem verglasten Fitnessgebäude in den Gärten.",
  "Портал застройщика описывает дизайн как современный. На компьютерных визуализациях корпуса поднимаются на три и четыре уровня длинными лентами террас со стеклянным ограждением среди газонов, а в садах расположены бассейн и остеклённое здание тренажёрного зала.",
  "يصف موقع المطوّر التصميم بأنه معاصر. وفي المناظر المولَّدة بالحاسوب ترتفع المباني ثلاثة وأربعة مستويات بأشرطة طويلة من التراسات ذات الواجهات الزجاجية، وسط مساحات عشبية، مع مسبح ومبنى زجاجي للصالة الرياضية في الحدائق.",
  "Het portaal van de ontwikkelaar beschrijft het ontwerp als eigentijds. In de computergegenereerde beelden rijzen de gebouwen op tot drie en vier bouwlagen met lange stroken terrassen met glazen balustrades, te midden van gazons, met een zwembad en een glazen fitnessgebouw in de tuinen.",
  "Portal dewelopera opisuje projekt jako nowoczesny. Na wizualizacjach komputerowych bloki mają trzy i cztery kondygnacje z długimi pasami tarasów o szklanych balustradach, wśród trawników, z basenem i przeszklonym budynkiem siłowni w ogrodach.",
  "Utbyggerens portal beskriver designet som moderne. I de datagenererte bildene hever blokkene seg tre og fire etasjer med lange bånd av terrasser med glassfronter, omgitt av plener, med et basseng og en glassbygning for treningsrommet i hagene.",
  "Exploatörens portal beskriver designen som modern. I de datorgenererade bilderna reser sig husen tre och fyra våningar med långa band av terrasser med glasfronter, omgivna av gräsmattor, med en pool och en glasad gymbyggnad i trädgårdarna.")

P('.architecture.copy[1]',
  "En los planos, las viviendas de planta baja se abren a un porche y, en algunas, a una zona sombreada en verde, y las plantas superiores a una terraza. Las hojas de diciembre de 2024 indican que las zonas sombreadas en verde se ejecutan con césped artificial sobre estructura.",
  "Sur les plans, les logements du rez-de-chaussée s’ouvrent sur un porche et, pour certains, sur une zone ombrée en vert, et les étages supérieurs sur une terrasse. Les feuilles de décembre 2024 précisent que les zones ombrées en vert sont réalisées en gazon artificiel sur structure.",
  "Auf den Plänen öffnen sich die Erdgeschosswohnungen zu einer überdachten Terrasse und teils zu einer grün schraffierten Fläche, die oberen Etagen zu einer Terrasse. Die Blätter vom Dezember 2024 vermerken, dass die grün schraffierten Flächen mit Kunstrasen auf einer Tragkonstruktion ausgeführt werden.",
  "На планах квартиры первого этажа выходят на крытую террасу, а некоторые — и на зону, закрашенную зелёным; квартиры верхних этажей выходят на террасу. В листах за декабрь 2024 года отмечено, что закрашенные зелёным зоны выполняются из искусственного газона на конструкции.",
  "في المخططات تُطل منازل الطابق الأرضي على رواق، وبعضها على منطقة مظللة بالأخضر، بينما تُطل الطوابق العليا على تراس. وتشير مخططات ديسمبر 2024 إلى أن المناطق المظللة بالأخضر تُنفَّذ بعشب صناعي فوق هيكل.",
  "Op de plattegronden komen de woningen op de begane grond uit op een overdekt terras en sommige ook op een groen gearceerd gedeelte, de hogere verdiepingen op een terras. De bladen van december 2024 vermelden dat de groen gearceerde delen worden uitgevoerd met kunstgras op een constructie.",
  "Na rzutach mieszkania na parterze otwierają się na werandę, a niektóre także na zaznaczony na zielono obszar, mieszkania na wyższych piętrach na taras. Arkusze z grudnia 2024 r. zawierają uwagę, że zaznaczone na zielono obszary będą wykonane ze sztucznej trawy na konstrukcji.",
  "På plantegningene åpner boligene i første etasje seg mot en overbygd uteplass og enkelte mot et grønnskravert område, og de øvre etasjene mot en terrasse. Arkene fra desember 2024 oppgir at de grønnskraverte områdene utføres med kunstgress på en konstruksjon.",
  "På planritningarna öppnar sig bostäderna på bottenvåningen mot en veranda och några mot ett grönskrafferat område, och de övre våningarna mot en terrass. Ritningarna från december 2024 anger att de grönskrafferade ytorna utförs med konstgräs på en konstruktion.")

P('.architecture.highlights[0][1]',
  "Dos dormitorios, dos baños, un recibidor y un salón-comedor con cocina, en {N76.44} a {N87.71} {U} de superficie interior.",
  "Deux chambres, deux salles de bain, une entrée et un séjour-salle à manger avec cuisine, sur {N76.44} à {N87.71} {U} de surface intérieure.",
  "Zwei Schlafzimmer, zwei Bäder, ein Eingangsbereich und ein Wohn- und Essbereich mit Küche auf {N76.44} bis {N87.71} {U} Innenfläche.",
  "Две спальни, две ванные комнаты, прихожая и гостиная-столовая с кухней на внутренней площади от {N76.44} до {N87.71} {U}.",
  "غرفتا نوم وحمامان ومدخل وغرفة معيشة وطعام مع المطبخ، على مساحة داخلية من {N76.44} إلى {N87.71} {U}.",
  "Twee slaapkamers, twee badkamers, een hal en een woon- en eetkamer met keuken, op {N76.44} tot {N87.71} {U} binnenoppervlak.",
  "Dwie sypialnie, dwie łazienki, przedpokój oraz salon z jadalnią i kuchnią na powierzchni wewnętrznej od {N76.44} do {N87.71} {U}.",
  "To soverom, to bad, en entré og en stue og spisestue med kjøkken, på {N76.44} til {N87.71} {U} innvendig areal.",
  "Två sovrum, två badrum, en hall samt ett vardagsrum och en matplats med kök, på {N76.44} till {N87.71} {U} inneryta.")

P('.architecture.highlights[1][1]',
  "Las viviendas de planta baja tienen un porche de {N56.54} a {N56.61} {U}, o un porche de {N38.87} {U} y un jardín de {N31.00} {U}. Las plantas superiores tienen terrazas de {N15.83} a {N39.75} {U}.",
  "Les logements du rez-de-chaussée ont un porche de {N56.54} à {N56.61} {U}, ou un porche de {N38.87} {U} et un jardin de {N31.00} {U}. Les étages supérieurs ont des terrasses de {N15.83} à {N39.75} {U}.",
  "Die Erdgeschosswohnungen haben eine überdachte Terrasse von {N56.54} bis {N56.61} {U} oder eine von {N38.87} {U} und einen Garten von {N31.00} {U}. Die oberen Etagen haben Terrassen von {N15.83} bis {N39.75} {U}.",
  "У квартир первого этажа крытая терраса от {N56.54} до {N56.61} {U} либо терраса {N38.87} {U} и сад {N31.00} {U}. У квартир верхних этажей террасы от {N15.83} до {N39.75} {U}.",
  "لمنازل الطابق الأرضي رواق مساحته من {N56.54} إلى {N56.61} {U}، أو رواق مساحته {N38.87} {U} وحديقة مساحتها {N31.00} {U}. وللطوابق العليا تراسات من {N15.83} إلى {N39.75} {U}.",
  "De woningen op de begane grond hebben een overdekt terras van {N56.54} tot {N56.61} {U}, of een van {N38.87} {U} met een tuin van {N31.00} {U}. De hogere verdiepingen hebben terrassen van {N15.83} tot {N39.75} {U}.",
  "Mieszkania na parterze mają werandę o powierzchni od {N56.54} do {N56.61} {U} albo werandę {N38.87} {U} i ogród {N31.00} {U}. Mieszkania na wyższych piętrach mają tarasy od {N15.83} do {N39.75} {U}.",
  "Boligene i første etasje har en overbygd uteplass på {N56.54} til {N56.61} {U}, eller en på {N38.87} {U} og en hage på {N31.00} {U}. De øvre etasjene har terrasser på {N15.83} til {N39.75} {U}.",
  "Bostäderna på bottenvåningen har en veranda på {N56.54} till {N56.61} {U}, eller en på {N38.87} {U} och en trädgård på {N31.00} {U}. De övre våningarna har terrasser på {N15.83} till {N39.75} {U}.")

P('.architecture.highlights[2][1]',
  "Una piscina con zona de solárium, un gimnasio y jardines plantados con especies autóctonas, dentro de una urbanización cerrada, tal como los describe el portal.",
  "Une piscine avec solarium, une salle de sport et des jardins plantés d’espèces locales, dans une résidence fermée, tels que les décrit le portail.",
  "Ein Pool mit Sonnenterrasse, ein Fitnessraum und mit einheimischen Pflanzen bepflanzte Gärten in einer geschlossenen Wohnanlage, wie das Portal sie beschreibt.",
  "Бассейн с солярием, тренажёрный зал и сады с местными видами растений в закрытом комплексе — так их описывает портал.",
  "مسبح بمنطقة تشمس وصالة رياضية وحدائق مزروعة بنباتات محلية، داخل مجمع مغلق، كما يصفها موقع المطوّر.",
  "Een zwembad met zonneterras, een fitnessruimte en tuinen met inheemse beplanting, binnen een besloten complex, zoals het portaal ze beschrijft.",
  "Basen z tarasem słonecznym, siłownia i ogrody obsadzone rodzimymi gatunkami roślin na zamkniętym osiedlu, tak jak opisuje je portal.",
  "Et basseng med solterrasse, et treningsrom og hager beplantet med stedegne arter, i et bevoktet område, slik portalen beskriver dem.",
  "En pool med solterrass, ett gym och trädgårdar planterade med inhemska arter, i ett bevakat område, så som portalen beskriver dem.")

P('.architecture.highlights[3][1]',
  "Cada vivienda figura con una plaza de garaje y un trastero.",
  "Chaque logement est annoncé avec une place de garage et un local de rangement.",
  "Zu jeder Wohnung sind ein Garagenstellplatz und ein Abstellraum aufgeführt.",
  "У каждой квартиры указаны одно гаражное место и одна кладовая.",
  "يُدرج لكل منزل موقف واحد في المرآب وغرفة تخزين واحدة.",
  "Bij elke woning staan een garageplaats en een berging vermeld.",
  "Przy każdym mieszkaniu podano jedno miejsce w garażu i jedną komórkę lokatorską.",
  "Hver bolig er oppført med én garasjeplass og ett bod.",
  "Varje bostad är listad med en garageplats och ett förråd.")

# ---- residences
P('.residences.headlineHtml',
  "Tres tipos de vivienda, <em>todas de dos dormitorios</em>",
  "Trois types de logement, <em>tous de deux chambres</em>",
  "Drei Arten von Wohnungen, <em>alle mit zwei Schlafzimmern</em>",
  "Три типа квартир, <em>в каждой две спальни</em>",
  "ثلاثة أنواع من المنازل، <em>كلها بغرفتي نوم</em>",
  "Drie soorten woningen, <em>elk met twee slaapkamers</em>",
  "Trzy rodzaje mieszkań, <em>każde z dwiema sypialniami</em>",
  "Tre typer boliger, <em>alle med to soverom</em>",
  "Tre typer av bostäder, <em>alla med två sovrum</em>")

P('.residences.copy',
  "Las 12 viviendas de la lista tienen todas dos dormitorios y dos baños y se dividen en tres grupos según la planta. La tabla de abajo recoge todas con su precio.",
  "Les 12 logements annoncés ont tous deux chambres et deux salles de bain et se répartissent en trois groupes selon l’étage. Le tableau ci-dessous les présente tous avec leur prix.",
  "Die 12 gelisteten Wohnungen haben alle zwei Schlafzimmer und zwei Bäder und gliedern sich nach Etage in drei Gruppen. Die Tabelle unten führt alle mit ihren Preisen auf.",
  "Все 12 квартир из списка имеют две спальни и две ванные комнаты и делятся на три группы по этажам. В таблице ниже приведены все они с ценами.",
  "جميع المنازل الـ12 المعروضة بغرفتي نوم وحمامين، وتنقسم إلى ثلاث مجموعات بحسب الطابق. ويُدرج الجدول أدناه جميعها مع أسعارها.",
  "De 12 vermelde woningen hebben allemaal twee slaapkamers en twee badkamers en vallen naar verdieping uiteen in drie groepen. De tabel hieronder toont ze allemaal met hun prijzen.",
  "Wszystkie 12 mieszkań z listy ma dwie sypialnie i dwie łazienki i dzieli się na trzy grupy według piętra. Tabela poniżej zawiera je wszystkie wraz z cenami.",
  "De 12 oppførte boligene har alle to soverom og to bad og deler seg i tre grupper etter etasje. Tabellen nedenfor viser alle med priser.",
  "De 12 listade bostäderna har alla två sovrum och två badrum och delas in i tre grupper efter våning. Tabellen nedan listar alla med deras priser.")

P('.residences.items[0].name',
  "Planta baja, con porche o jardín", "Rez-de-chaussée, avec porche ou jardin", "Erdgeschoss, mit überdachter Terrasse oder Garten",
  "Первый этаж, с крытой террасой или садом", "الطابق الأرضي، برواق أو حديقة", "Begane grond, met overdekt terras of tuin",
  "Parter, z werandą lub ogrodem", "Første etasje, med overbygd uteplass eller hage", "Bottenvåning, med veranda eller trädgård")

P('.residences.items[0].points[0]',
  "Cuatro viviendas: 2-2-BAJ-A y 2-2-BAJ-B con {N111.86} y {N111.85} {U} construidos, 3-2-BAJ-A con {N110.62} {U} y 5-1-BAJ-A con {N115.18} {U}.",
  "Quatre logements : 2-2-BAJ-A et 2-2-BAJ-B de {N111.86} et {N111.85} {U} construits, 3-2-BAJ-A de {N110.62} {U} et 5-1-BAJ-A de {N115.18} {U}.",
  "Vier Wohnungen: 2-2-BAJ-A und 2-2-BAJ-B mit {N111.86} und {N111.85} {U} bebauter Fläche, 3-2-BAJ-A mit {N110.62} {U} und 5-1-BAJ-A mit {N115.18} {U}.",
  "Четыре квартиры: 2-2-BAJ-A и 2-2-BAJ-B с площадью застройки {N111.86} и {N111.85} {U}, 3-2-BAJ-A — {N110.62} {U} и 5-1-BAJ-A — {N115.18} {U}.",
  "أربعة منازل: 2-2-BAJ-A و2-2-BAJ-B بمساحة مبنية {N111.86} و{N111.85} {U}، و3-2-BAJ-A بمساحة {N110.62} {U}، و5-1-BAJ-A بمساحة {N115.18} {U}.",
  "Vier woningen: 2-2-BAJ-A en 2-2-BAJ-B met {N111.86} en {N111.85} {U} bebouwd, 3-2-BAJ-A met {N110.62} {U} en 5-1-BAJ-A met {N115.18} {U}.",
  "Cztery mieszkania: 2-2-BAJ-A i 2-2-BAJ-B o powierzchni zabudowy {N111.86} i {N111.85} {U}, 3-2-BAJ-A o powierzchni {N110.62} {U} i 5-1-BAJ-A o powierzchni {N115.18} {U}.",
  "Fire boliger: 2-2-BAJ-A og 2-2-BAJ-B med {N111.86} og {N111.85} {U} bygd, 3-2-BAJ-A med {N110.62} {U} og 5-1-BAJ-A med {N115.18} {U}.",
  "Fyra bostäder: 2-2-BAJ-A och 2-2-BAJ-B med {N111.86} och {N111.85} {U} byggyta, 3-2-BAJ-A med {N110.62} {U} och 5-1-BAJ-A med {N115.18} {U}.")

P('.residences.items[0].points[1]',
  "Tres de ellas tienen un porche de {N56.54} a {N56.61} {U}; la 5-1-BAJ-A tiene un porche de {N38.87} {U} y un jardín de {N31.00} {U}.",
  "Trois d’entre eux ont un porche de {N56.54} à {N56.61} {U} ; le 5-1-BAJ-A a un porche de {N38.87} {U} et un jardin de {N31.00} {U}.",
  "Drei davon haben eine überdachte Terrasse von {N56.54} bis {N56.61} {U}; 5-1-BAJ-A hat eine von {N38.87} {U} und einen Garten von {N31.00} {U}.",
  "У трёх из них крытая терраса от {N56.54} до {N56.61} {U}; у 5-1-BAJ-A — терраса {N38.87} {U} и сад {N31.00} {U}.",
  "لثلاثة منها رواق مساحته من {N56.54} إلى {N56.61} {U}؛ أما 5-1-BAJ-A فله رواق مساحته {N38.87} {U} وحديقة مساحتها {N31.00} {U}.",
  "Drie ervan hebben een overdekt terras van {N56.54} tot {N56.61} {U}; 5-1-BAJ-A heeft een van {N38.87} {U} en een tuin van {N31.00} {U}.",
  "Trzy z nich mają werandę o powierzchni od {N56.54} do {N56.61} {U}; 5-1-BAJ-A ma werandę {N38.87} {U} i ogród {N31.00} {U}.",
  "Tre av dem har en overbygd uteplass på {N56.54} til {N56.61} {U}; 5-1-BAJ-A har en på {N38.87} {U} og en hage på {N31.00} {U}.",
  "Tre av dem har en veranda på {N56.54} till {N56.61} {U}; 5-1-BAJ-A har en på {N38.87} {U} och en trädgård på {N31.00} {U}.")

P('.residences.items[0].points[2]',
  "Los precios van de {E332000} a {E370000}.", "Les prix vont de {E332000} à {E370000}.", "Die Preise reichen von {E332000} bis {E370000}.",
  "Цены — от {E332000} до {E370000}.", "تتراوح الأسعار من {E332000} إلى {E370000}.", "De prijzen lopen van {E332000} tot {E370000}.",
  "Ceny wahają się od {E332000} do {E370000}.", "Prisene går fra {E332000} til {E370000}.", "Priserna sträcker sig från {E332000} till {E370000}.")

P('.residences.items[1].name',
  "Primera y segunda planta", "Premier et deuxième étages", "Erstes und zweites Obergeschoss",
  "Второй и третий этажи", "الطابقان الأول والثاني", "Eerste en tweede verdieping",
  "Pierwsze i drugie piętro", "Andre og tredje etasje", "Första och andra våningen")

P('.residences.items[1].points[0]',
  "Tres viviendas: la 5-1-1-A, en la primera planta, con {N115.31} {U} construidos y una terraza de {N39.75} {U}, y la 7-3-2-B y la 8-3-2-B, en la segunda planta, con {N114.12} y {N114.16} {U} construidos y una terraza de {N29.91} {U}.",
  "Trois logements : le 5-1-1-A au premier étage, de {N115.31} {U} construits avec une terrasse de {N39.75} {U}, et le 7-3-2-B et le 8-3-2-B au deuxième étage, de {N114.12} et {N114.16} {U} construits avec une terrasse de {N29.91} {U}.",
  "Drei Wohnungen: 5-1-1-A im ersten Obergeschoss mit {N115.31} {U} bebauter Fläche und einer Terrasse von {N39.75} {U} sowie 7-3-2-B und 8-3-2-B im zweiten Obergeschoss mit {N114.12} und {N114.16} {U} bebauter Fläche und einer Terrasse von {N29.91} {U}.",
  "Три квартиры: 5-1-1-A на втором этаже с площадью застройки {N115.31} {U} и террасой {N39.75} {U}, а также 7-3-2-B и 8-3-2-B на третьем этаже с площадью застройки {N114.12} и {N114.16} {U} и террасой {N29.91} {U}.",
  "ثلاثة منازل: 5-1-1-A في الطابق الأول بمساحة مبنية {N115.31} {U} وتراس مساحته {N39.75} {U}، و7-3-2-B و8-3-2-B في الطابق الثاني بمساحة مبنية {N114.12} و{N114.16} {U} وتراس مساحته {N29.91} {U}.",
  "Drie woningen: 5-1-1-A op de eerste verdieping met {N115.31} {U} bebouwd en een terras van {N39.75} {U}, en 7-3-2-B en 8-3-2-B op de tweede verdieping met {N114.12} en {N114.16} {U} bebouwd en een terras van {N29.91} {U}.",
  "Trzy mieszkania: 5-1-1-A na pierwszym piętrze o powierzchni zabudowy {N115.31} {U} z tarasem {N39.75} {U} oraz 7-3-2-B i 8-3-2-B na drugim piętrze o powierzchni zabudowy {N114.12} i {N114.16} {U} z tarasem {N29.91} {U}.",
  "Tre boliger: 5-1-1-A i andre etasje med {N115.31} {U} bygd og en terrasse på {N39.75} {U}, og 7-3-2-B og 8-3-2-B i tredje etasje med {N114.12} og {N114.16} {U} bygd og en terrasse på {N29.91} {U}.",
  "Tre bostäder: 5-1-1-A på första våningen med {N115.31} {U} byggyta och en terrass på {N39.75} {U}, samt 7-3-2-B och 8-3-2-B på andra våningen med {N114.12} och {N114.16} {U} byggyta och en terrass på {N29.91} {U}.")

P('.residences.items[1].points[1]',
  "La vivienda de la primera planta cuesta {E373000} y cada una de la segunda planta, {E408000}.",
  "Le logement du premier étage coûte {E373000} et chacun de ceux du deuxième étage {E408000}.",
  "Die Wohnung im ersten Obergeschoss kostet {E373000}, jede Wohnung im zweiten Obergeschoss {E408000}.",
  "Квартира на втором этаже стоит {E373000}, а каждая квартира на третьем этаже — {E408000}.",
  "يبلغ سعر منزل الطابق الأول {E373000} وسعر كل منزل في الطابق الثاني {E408000}.",
  "De woning op de eerste verdieping kost {E373000} en elke woning op de tweede verdieping {E408000}.",
  "Mieszkanie na pierwszym piętrze kosztuje {E373000}, a każde mieszkanie na drugim piętrze {E408000}.",
  "Boligen i andre etasje koster {E373000}, og hver av boligene i tredje etasje {E408000}.",
  "Bostaden på första våningen kostar {E373000} och varje bostad på andra våningen {E408000}.")

P('.residences.items[2].points[0]',
  "Cinco áticos de {N107.82} a {N126.50} {U} construidos y de {N76.44} a {N87.71} {U} interiores.",
  "Cinq penthouses de {N107.82} à {N126.50} {U} construits et de {N76.44} à {N87.71} {U} intérieurs.",
  "Fünf Penthäuser mit {N107.82} bis {N126.50} {U} bebauter Fläche und {N76.44} bis {N87.71} {U} Innenfläche.",
  "Пять пентхаусов с площадью застройки от {N107.82} до {N126.50} {U} и внутренней площадью от {N76.44} до {N87.71} {U}.",
  "خمسة بنتهاوس بمساحة مبنية من {N107.82} إلى {N126.50} {U} ومساحة داخلية من {N76.44} إلى {N87.71} {U}.",
  "Vijf penthouses van {N107.82} tot {N126.50} {U} bebouwd en {N76.44} tot {N87.71} {U} binnenoppervlak.",
  "Pięć penthouse’ów o powierzchni zabudowy od {N107.82} do {N126.50} {U} i powierzchni wewnętrznej od {N76.44} do {N87.71} {U}.",
  "Fem toppleiligheter på {N107.82} til {N126.50} {U} bygd og {N76.44} til {N87.71} {U} innvendig areal.",
  "Fem takvåningar på {N107.82} till {N126.50} {U} byggyta och {N76.44} till {N87.71} {U} inneryta.")

P('.residences.items[2].points[1]',
  "Los dos del bloque 3 tienen una terraza de {N29.32} {U}; los tres de los bloques 5 y 9 tienen terrazas de {N15.83} a {N15.91} {U}.",
  "Les deux du bloc 3 ont une terrasse de {N29.32} {U} ; les trois des blocs 5 et 9 ont des terrasses de {N15.83} à {N15.91} {U}.",
  "Die beiden in Block 3 haben eine Terrasse von {N29.32} {U}; die drei in den Blöcken 5 und 9 haben Terrassen von {N15.83} bis {N15.91} {U}.",
  "У двух пентхаусов в блоке 3 терраса {N29.32} {U}; у трёх в блоках 5 и 9 террасы от {N15.83} до {N15.91} {U}.",
  "للاثنين في المبنى 3 تراس مساحته {N29.32} {U}؛ وللثلاثة في المبنيين 5 و9 تراسات من {N15.83} إلى {N15.91} {U}.",
  "De twee in blok 3 hebben een terras van {N29.32} {U}; de drie in de blokken 5 en 9 hebben terrassen van {N15.83} tot {N15.91} {U}.",
  "Dwa w bloku 3 mają taras o powierzchni {N29.32} {U}; trzy w blokach 5 i 9 mają tarasy od {N15.83} do {N15.91} {U}.",
  "De to i hus 3 har en terrasse på {N29.32} {U}; de tre i hus 5 og 9 har terrasser på {N15.83} til {N15.91} {U}.",
  "De två i hus 3 har en terrass på {N29.32} {U}; de tre i hus 5 och 9 har terrasser på {N15.83} till {N15.91} {U}.")

P('.residences.items[2].points[2]',
  "Los precios van de {E360000} a {E455000}. El texto del portal menciona solárium en los áticos, pero los planos de estos cinco muestran solo terrazas.",
  "Les prix vont de {E360000} à {E455000}. Le texte du portail mentionne des solariums sur les penthouses, mais les plans de ces cinq montrent uniquement des terrasses.",
  "Die Preise reichen von {E360000} bis {E455000}. Der Portaltext erwähnt Solarien bei den Penthäusern, die Pläne dieser fünf zeigen jedoch nur Terrassen.",
  "Цены — от {E360000} до {E455000}. В тексте портала у пентхаусов упомянуты солярии, но на планах этих пяти показаны только террасы.",
  "تتراوح الأسعار من {E360000} إلى {E455000}. يذكر نص موقع المطوّر سولاريوم للبنتهاوس، لكن مخططات هذه الخمسة تُظهر تراسات فقط.",
  "De prijzen lopen van {E360000} tot {E455000}. De tekst van het portaal noemt solariums bij de penthouses, maar de plattegronden van deze vijf tonen alleen terrassen.",
  "Ceny wahają się od {E360000} do {E455000}. Tekst portalu wspomina o solariach przy penthouse’ach, ale rzuty tych pięciu pokazują wyłącznie tarasy.",
  "Prisene går fra {E360000} til {E455000}. Portalteksten nevner solterrasser på toppleilighetene, men plantegningene for disse fem viser bare terrasser.",
  "Priserna sträcker sig från {E360000} till {E455000}. Portaltexten nämner solterrasser på takvåningarna, men planritningarna för dessa fem visar bara terrasser.")

# ---- lifestyle
P('.lifestyle.headlineHtml',
  "Una piscina, un gimnasio <em>y el golf al lado</em>", "Une piscine, une salle de sport <em>et le golf à côté</em>",
  "Ein Pool, ein Fitnessraum <em>und der Golfplatz nebenan</em>", "Бассейн, тренажёрный зал <em>и гольф по соседству</em>",
  "مسبح وصالة رياضية <em>والغولف في الجوار</em>", "Een zwembad, een fitnessruimte <em>en de golf naast de deur</em>",
  "Basen, siłownia <em>i golf tuż obok</em>", "Et basseng, et treningsrom <em>og golfen ved siden av</em>",
  "En pool, ett gym <em>och golfen alldeles intill</em>")

P('.lifestyle.copy',
  "El portal del promotor describe una urbanización cerrada con instalaciones comunes para los residentes, junto a un club de golf.",
  "Le portail du promoteur décrit une résidence fermée dotée d’équipements communs pour les résidents, à côté d’un club de golf.",
  "Das Portal des Bauträgers beschreibt eine geschlossene Wohnanlage mit Gemeinschaftseinrichtungen für die Bewohner, neben einem Golfclub.",
  "Портал застройщика описывает закрытый комплекс с общими удобствами для жителей рядом с гольф-клубом.",
  "يصف موقع المطوّر مجمعًا مغلقًا بمرافق مشتركة للسكان بجوار نادي غولف.",
  "Het portaal van de ontwikkelaar beschrijft een besloten complex met gedeelde voorzieningen voor de bewoners, naast een golfclub.",
  "Portal dewelopera opisuje zamknięte osiedle ze wspólnymi udogodnieniami dla mieszkańców, obok klubu golfowego.",
  "Utbyggerens portal beskriver et bevoktet område med felles fasiliteter for beboerne, ved siden av en golfklubb.",
  "Exploatörens portal beskriver ett bevakat område med gemensamma faciliteter för de boende, intill en golfklubb.")

P('.lifestyle.panels[0][1]',
  "Una piscina comunitaria con zona de solárium, con los bloques a su alrededor en las vistas generadas por ordenador.",
  "Une piscine commune avec solarium, entourée des immeubles dans les vues générées par ordinateur.",
  "Ein Gemeinschaftspool mit Sonnenterrasse, in den computergenerierten Ansichten von den Blöcken umgeben.",
  "Общий бассейн с солярием; на компьютерных визуализациях вокруг него расположены корпуса.",
  "مسبح مشترك بمنطقة تشمس، تحيط به المباني في المناظر المولَّدة بالحاسوب.",
  "Een gemeenschappelijk zwembad met zonneterras, in de computergegenereerde beelden omringd door de gebouwen.",
  "Wspólny basen z tarasem słonecznym, otoczony blokami na wizualizacjach komputerowych.",
  "Et felles basseng med solterrasse, omgitt av blokkene i de datagenererte bildene.",
  "En gemensam pool med solterrass, omgiven av husen i de datorgenererade bilderna.")

P('.lifestyle.panels[1][1]',
  "El portal indica un gimnasio; la vista generada por ordenador lo muestra en un edificio acristalado en los jardines.",
  "Le portail mentionne une salle de sport ; la vue générée par ordinateur la montre dans un bâtiment vitré au milieu des jardins.",
  "Das Portal nennt einen Fitnessraum; die computergenerierte Ansicht zeigt ihn in einem verglasten Gebäude in den Gärten.",
  "Портал упоминает тренажёрный зал; на компьютерной визуализации он размещён в остеклённом здании среди садов.",
  "يذكر موقع المطوّر صالة رياضية؛ ويُظهرها المنظر المولَّد بالحاسوب في مبنى زجاجي وسط الحدائق.",
  "Het portaal vermeldt een fitnessruimte; het computergegenereerde beeld toont die in een glazen gebouw in de tuinen.",
  "Portal wymienia siłownię; wizualizacja komputerowa pokazuje ją w przeszklonym budynku w ogrodach.",
  "Portalen oppgir et treningsrom; det datagenererte bildet viser det i en glassbygning i hagene.",
  "Portalen anger ett gym; den datorgenererade bilden visar det i en glasad byggnad i trädgårdarna.")

P('.lifestyle.panels[2][1]',
  "Jardines plantados con especies autóctonas, dentro de una urbanización cerrada.",
  "Des jardins plantés d’espèces locales, dans une résidence fermée.",
  "Mit einheimischen Pflanzen bepflanzte Gärten innerhalb einer geschlossenen Wohnanlage.",
  "Сады с местными видами растений в закрытом комплексе.",
  "حدائق مزروعة بنباتات محلية داخل مجمع مغلق.",
  "Tuinen met inheemse beplanting binnen een besloten complex.",
  "Ogrody obsadzone rodzimymi gatunkami roślin na zamkniętym osiedlu.",
  "Hager beplantet med stedegne arter, i et bevoktet område.",
  "Trädgårdar planterade med inhemska arter, i ett bevakat område.")

P('.lifestyle.panels[3][1]',
  "El portal sitúa la urbanización junto a un club de golf en Estepona.",
  "Le portail situe la résidence à côté d’un club de golf à Estepona.",
  "Das Portal verortet die Anlage neben einem Golfclub in Estepona.",
  "Портал указывает, что комплекс находится рядом с гольф-клубом в Эстепоне.",
  "يضع موقع المطوّر المجمع بجوار نادي غولف في إستيبونا.",
  "Het portaal plaatst het complex naast een golfclub in Estepona.",
  "Portal umieszcza osiedle obok klubu golfowego w Esteponie.",
  "Portalen plasserer anlegget ved siden av en golfklubb i Estepona.",
  "Portalen placerar området intill en golfklubb i Estepona.")

# ---- location
P('.location.headlineHtml',
  "Estepona, <em>junto a un club de golf</em>", "Estepona, <em>à côté d’un club de golf</em>", "Estepona, <em>neben einem Golfclub</em>",
  "Эстепона, <em>рядом с гольф-клубом</em>", "إستيبونا، <em>بجوار نادي غولف</em>", "Estepona, <em>naast een golfclub</em>",
  "Estepona, <em>obok klubu golfowego</em>", "Estepona, <em>ved siden av en golfklubb</em>", "Estepona, <em>intill en golfklubb</em>")

P('.location.copy',
  "El portal sitúa la urbanización junto a un club de golf en Estepona y dice que las viviendas están orientadas al sur. Los documentos del promotor no indican dirección, posición de la parcela ni distancias, por lo que el mapa sitúa el proyecto a nivel de zona y los tiempos por carretera se miden desde allí; confirmamos la posición exacta y los tiempos de trayecto durante una visita.",
  "Le portail situe la résidence à côté d’un club de golf à Estepona et indique que les logements sont orientés au sud. Les documents du promoteur ne donnent ni adresse, ni position de la parcelle, ni distances ; la carte situe donc le projet à l’échelle du quartier et les temps de trajet routier sont mesurés à partir de ce point ; nous confirmons la position exacte et les temps de trajet lors d’une visite.",
  "Das Portal verortet die Anlage neben einem Golfclub in Estepona und gibt an, dass die Wohnungen nach Süden ausgerichtet sind. Die Unterlagen des Bauträgers nennen weder Adresse noch Lage des Grundstücks noch Entfernungen; die Karte verortet das Projekt daher auf Gebietsebene, und die Fahrzeiten werden von dort aus gemessen. Die genaue Lage und die Fahrzeiten bestätigen wir bei einer Besichtigung.",
  "Портал указывает, что комплекс находится рядом с гольф-клубом в Эстепоне, а квартиры ориентированы на юг. В документах застройщика нет ни адреса, ни положения участка, ни расстояний, поэтому на карте проект отмечен на уровне района, а время в пути рассчитано от этой точки; точное положение и время в пути мы подтверждаем во время просмотра.",
  "يضع موقع المطوّر المجمع بجوار نادي غولف في إستيبونا ويذكر أن المنازل تواجه الجنوب. ولا تذكر وثائق المطوّر عنوانًا ولا موضع الأرض ولا مسافات، لذلك تضع الخريطة المشروع على مستوى المنطقة وتُقاس أزمنة الطريق من هذه النقطة؛ ونؤكد الموقع الدقيق وأزمنة التنقل أثناء المعاينة.",
  "Het portaal plaatst het complex naast een golfclub in Estepona en zegt dat de woningen op het zuiden liggen. De documenten van de ontwikkelaar geven geen adres, perceelpositie of afstanden, dus de kaart plaatst het project op gebiedsniveau en de reistijden worden vanaf dat punt gemeten; de exacte positie en de reistijden bevestigen we tijdens een bezoek.",
  "Portal umieszcza osiedle obok klubu golfowego w Esteponie i podaje, że mieszkania mają orientację południową. Dokumenty dewelopera nie podają adresu, położenia działki ani odległości, dlatego mapa wskazuje projekt na poziomie okolicy, a czasy dojazdu są liczone od tego punktu; dokładne położenie i czasy dojazdu potwierdzamy podczas wizyty.",
  "Portalen plasserer anlegget ved siden av en golfklubb i Estepona og sier at boligene vender mot sør. Utbyggerens dokumenter oppgir ingen adresse, tomteplassering eller avstander, så kartet plasserer prosjektet på områdenivå og kjøretidene måles herfra; den nøyaktige plasseringen og kjøretidene bekrefter vi under en visning.",
  "Portalen placerar området intill en golfklubb i Estepona och anger att bostäderna är vända mot söder. Exploatörens dokument anger ingen adress, tomtplacering eller avstånd, så kartan placerar projektet på områdesnivå och körtiderna mäts därifrån; den exakta placeringen och körtiderna bekräftar vi vid en visning.")

P('.location.mapLabelPlain',
  "Estepona, junto a un club de golf", "Estepona, à côté d’un club de golf", "Estepona, neben einem Golfclub",
  "Эстепона, рядом с гольф-клубом", "إستيبونا، بجوار نادي غولف", "Estepona, naast een golfclub",
  "Estepona, obok klubu golfowego", "Estepona, ved siden av en golfklubb", "Estepona, intill en golfklubb")

P('.location.distances[0][0]',
  "Club de golf", "Club de golf", "Golfclub", "Гольф-клуб", "نادي الغولف", "Golfclub", "Klub golfowy", "Golfklubb", "Golfklubb")
P('.location.distances[0][1]',
  "Junto a la urbanización", "Attenant à la résidence", "Direkt an der Anlage", "Рядом с комплексом", "ملاصق للمجمع",
  "Grenst aan het complex", "Sąsiaduje z kompleksem", "Inntil anlegget", "Intill området")

# ---- investment
P('.investment.copy',
  "Las condiciones son las del portal del promotor. Confirmamos por escrito los importes y las fechas antes de que se comprometa.",
  "Les conditions sont celles du portail du promoteur. Nous confirmons par écrit les montants et les dates avant votre engagement.",
  "Die Bedingungen sind die des Portals des Bauträgers. Wir bestätigen Beträge und Termine schriftlich, bevor Sie sich verpflichten.",
  "Условия — те, что указаны на портале застройщика. Суммы и даты мы письменно подтверждаем до того, как вы примете решение.",
  "الشروط هي الواردة في موقع المطوّر. ونؤكد كتابةً المبالغ والتواريخ قبل أن تلتزموا.",
  "De voorwaarden zijn die van het portaal van de ontwikkelaar. We bevestigen de bedragen en data schriftelijk voordat u zich vastlegt.",
  "Warunki są takie, jak na portalu dewelopera. Przed zobowiązaniem się potwierdzamy na piśmie kwoty i terminy.",
  "Vilkårene er de på utbyggerens portal. Vi bekrefter beløp og datoer skriftlig før du forplikter deg.",
  "Villkoren är de på exploatörens portal. Vi bekräftar belopp och datum skriftligen innan ni förbinder er.")

P('.investment.cards[0][1]',
  "El portal no indica ningún pago de reserva.", "Le portail n’indique aucun versement de réservation.", "Das Portal nennt keine Reservierungszahlung.",
  "На портале не указан платёж за бронирование.", "لا يذكر موقع المطوّر أي دفعة حجز.", "Het portaal vermeldt geen reserveringsbetaling.",
  "Portal nie podaje opłaty rezerwacyjnej.", "Portalen oppgir ingen reservasjonsbetaling.", "Portalen anger ingen reservationsbetalning.")

P('.investment.cards[1][0]',
  "Compradores residentes fuera de España", "Acheteurs résidant hors d’Espagne", "Käufer mit Wohnsitz außerhalb Spaniens",
  "Покупатели, проживающие за пределами Испании", "المشترون المقيمون خارج إسبانيا", "Kopers die buiten Spanje wonen",
  "Kupujący mieszkający poza Hiszpanią", "Kjøpere bosatt utenfor Spania", "Köpare bosatta utanför Spanien")
P('.investment.cards[1][1]',
  "El 30% más IVA al firmar el contrato privado de compraventa y el 70% más IVA a la finalización ante notario.",
  "30 % hors TVA à la signature du contrat de vente privé et 70 % hors TVA à l’achèvement chez le notaire.",
  "30 % zuzüglich MwSt. bei Unterzeichnung des privaten Kaufvertrags und 70 % zuzüglich MwSt. bei Fertigstellung beim Notar.",
  "30 % плюс НДС при подписании предварительного договора купли-продажи и 70 % плюс НДС при завершении сделки у нотариуса.",
  "30% زائد ضريبة القيمة المضافة عند توقيع عقد الشراء الخاص و70% زائد الضريبة عند الإتمام أمام كاتب العدل.",
  "30% plus btw bij ondertekening van de onderhandse koopovereenkomst en 70% plus btw bij oplevering ten overstaan van de notaris.",
  "30% plus VAT przy podpisaniu umowy przedwstępnej i 70% plus VAT u notariusza, przy akcie notarialnym.",
  "30 % pluss mva. ved signering av den private kjøpekontrakten og 70 % pluss mva. ved overtakelse hos notarius.",
  "30 % plus moms vid undertecknandet av det privata köpeavtalet och 70 % plus moms vid tillträdet hos notarien.")
P('.investment.cards[2][0]',
  "Compradores residentes en España", "Acheteurs résidant en Espagne", "Käufer mit Wohnsitz in Spanien",
  "Покупатели, проживающие в Испании", "المشترون المقيمون في إسبانيا", "Kopers die in Spanje wonen",
  "Kupujący mieszkający w Hiszpanii", "Kjøpere bosatt i Spania", "Köpare bosatta i Spanien")
P('.investment.cards[2][1]',
  "El 20% más IVA al firmar el contrato privado de compraventa y el 80% más IVA a la finalización ante notario.",
  "20 % hors TVA à la signature du contrat de vente privé et 80 % hors TVA à l’achèvement chez le notaire.",
  "20 % zuzüglich MwSt. bei Unterzeichnung des privaten Kaufvertrags und 80 % zuzüglich MwSt. bei Fertigstellung beim Notar.",
  "20 % плюс НДС при подписании предварительного договора купли-продажи и 80 % плюс НДС при завершении сделки у нотариуса.",
  "20% زائد ضريبة القيمة المضافة عند توقيع عقد الشراء الخاص و80% زائد الضريبة عند الإتمام أمام كاتب العدل.",
  "20% plus btw bij ondertekening van de onderhandse koopovereenkomst en 80% plus btw bij oplevering ten overstaan van de notaris.",
  "20% plus VAT przy podpisaniu umowy przedwstępnej i 80% plus VAT u notariusza, przy akcie notarialnym.",
  "20 % pluss mva. ved signering av den private kjøpekontrakten og 80 % pluss mva. ved overtakelse hos notarius.",
  "20 % plus moms vid undertecknandet av det privata köpeavtalet och 80 % plus moms vid tillträdet hos notarien.")
P('.investment.cards[3][0]',
  "IVA y garantía", "TVA et garantie", "MwSt. und Absicherung", "НДС и гарантия", "ضريبة القيمة المضافة والضمان",
  "Btw en waarborg", "VAT i gwarancja", "Mva. og garanti", "Moms och garanti")
P('.investment.cards[3][1]',
  "La lista de precios no incluye el IVA y no indica el tipo. Los documentos no mencionan ninguna garantía sobre los pagos a cuenta, por lo que pedimos la póliza antes de cualquier pago.",
  "La liste de prix n’inclut pas la TVA et n’en indique pas le taux. Les documents ne mentionnent aucune garantie sur les acomptes ; nous demandons donc la police avant tout paiement.",
  "Die Preisliste enthält keine MwSt. und nennt den Satz nicht. Die Unterlagen erwähnen keine Absicherung von Anzahlungen, daher fordern wir die Police vor jeder Zahlung an.",
  "Цены в прайс-листе указаны без НДС, ставка не названа. В документах не упоминается гарантия на авансовые платежи, поэтому мы запрашиваем полис до любого платежа.",
  "قائمة الأسعار لا تشمل ضريبة القيمة المضافة ولا تذكر نسبتها. ولا تذكر الوثائق أي ضمان للمبالغ المدفوعة مقدمًا، لذلك نطلب الوثيقة قبل أي دفعة.",
  "De prijslijst is exclusief btw en vermeldt het tarief niet. De documenten vermelden geen waarborg op vooruitbetalingen, dus we vragen de polis voordat er iets wordt betaald.",
  "Cennik nie obejmuje VAT i nie podaje stawki. Dokumenty nie wspominają o gwarancji na zaliczki, dlatego prosimy o polisę przed jakąkolwiek płatnością.",
  "Prislisten inkluderer ikke mva. og oppgir ikke satsen. Dokumentene nevner ingen garanti for forskuddsbetalinger, så vi ber om polisen før noen betaling.",
  "Prislistan inkluderar inte moms och anger inte satsen. Dokumenten nämner ingen garanti för förskottsbetalningar, så vi ber om polisen före varje betalning.")

# ---- trust dossier
P('.trustDossier.cards[0][0]',
  "Licencia, obras y finalización", "Permis, travaux et achèvement", "Genehmigung, Bauarbeiten und Fertigstellung",
  "Разрешение, работы и завершение", "الرخصة والأعمال والإنجاز", "Vergunning, werken en oplevering",
  "Pozwolenie, prace i ukończenie", "Tillatelse, arbeider og ferdigstillelse", "Bygglov, arbeten och färdigställande")
P('.trustDossier.cards[0][1]',
  "Los documentos de que disponemos no indican fecha de finalización ni dicen si la licencia de obras está concedida ni hasta dónde han llegado las obras. El portal tiene una página del estado de las obras que no formaba parte de lo que recibimos. Pedimos la licencia, el estado de las obras y la fecha contractual.",
  "Les documents dont nous disposons ne donnent aucune date d’achèvement et ne disent pas si le permis de construire est accordé ni où en sont les travaux. Le portail comporte une page sur l’avancement des travaux qui ne faisait pas partie de ce que nous avons reçu. Nous demandons le permis, l’état d’avancement des travaux et la date contractuelle.",
  "Die uns vorliegenden Unterlagen nennen keinen Fertigstellungstermin und sagen nicht, ob die Baugenehmigung erteilt ist oder wie weit die Bauarbeiten fortgeschritten sind. Das Portal hat eine Seite zum Baufortschritt, die nicht Teil dessen war, was wir erhalten haben. Wir fordern die Genehmigung, den Baustand und den vertraglichen Termin an.",
  "В имеющихся у нас документах нет срока завершения и не сказано, выдано ли разрешение на строительство и как продвинулись работы. На портале есть страница о ходе работ, которой не было среди полученных нами материалов. Мы запрашиваем разрешение, стадию работ и договорную дату.",
  "لا تذكر الوثائق التي لدينا موعدًا للإنجاز ولا تبيّن ما إذا كانت رخصة البناء ممنوحة أو إلى أي مدى تقدمت الأعمال. ويضم موقع المطوّر صفحة لحالة الأعمال لم تكن ضمن ما تلقيناه. نطلب الرخصة ومرحلة الأعمال والتاريخ التعاقدي.",
  "De documenten waarover we beschikken geven geen opleveringsdatum en zeggen niet of de bouwvergunning is verleend of hoe ver de werken zijn. Het portaal heeft een pagina over de voortgang van de werken die niet bij ons materiaal zat. We vragen om de vergunning, de stand van de werken en de contractuele datum.",
  "Dokumenty, którymi dysponujemy, nie podają terminu ukończenia i nie mówią, czy pozwolenie na budowę zostało wydane ani jak daleko posunęły się prace. Portal zawiera stronę o stanie prac, która nie była częścią otrzymanych przez nas materiałów. Prosimy o pozwolenie, stan prac i termin wskazany w umowie.",
  "Dokumentene vi har oppgir ingen ferdigstillelsesdato og sier ikke om byggetillatelsen er gitt eller hvor langt arbeidene har kommet. Portalen har en side om framdriften i arbeidene som ikke var med i det vi fikk. Vi ber om tillatelsen, status for arbeidene og den kontraktsfestede datoen.",
  "Dokumenten vi har anger inget färdigställandedatum och säger inte om bygglovet är beviljat eller hur långt byggarbetena har kommit. Portalen har en sida om byggstatus som inte ingick i det vi fick. Vi ber om bygglovet, byggstatus och det avtalade datumet.")
P('.trustDossier.cards[1][1]',
  "Las superficies construida e interior de la lista de precios coinciden con las de los planos con una diferencia de como máximo {N0.01} {U}, pero las cifras de terraza y porche de la lista son entre {N0.6} y {N4.2} {U} mayores que las superficies exteriores de los planos: para la vivienda 5-1-1-A la lista da {N33.24} {U} de terraza cubierta y {N6.51} {U} de descubierta ({N39.75} {U}), y el plano {N35.53} {U}. Los planos también dan superficies mayores según el Decreto 218/2005, por ejemplo {N120.94} {U} construidos para la vivienda 2-2-BAJ-B frente a {N111.85} {U}. Confirmamos qué cifra utiliza el contrato.",
  "Les surfaces construite et intérieure de la liste de prix correspondent à celles des plans à {N0.01} {U} près, mais les chiffres de terrasse et de porche de la liste dépassent de {N0.6} à {N4.2} {U} les surfaces extérieures des plans : pour le logement 5-1-1-A, la liste donne {N33.24} {U} de terrasse couverte et {N6.51} {U} de terrasse découverte ({N39.75} {U}), le plan {N35.53} {U}. Les plans donnent aussi des surfaces plus grandes selon le décret 218/2005, par exemple {N120.94} {U} construits pour le logement 2-2-BAJ-B contre {N111.85} {U}. Nous confirmons quel chiffre retient le contrat.",
  "Die bebaute Fläche und die Innenfläche der Preisliste stimmen mit den Plänen auf bis zu {N0.01} {U} überein, aber die Terrassen- und Verandawerte der Liste liegen {N0.6} bis {N4.2} {U} über den Außenflächen der Pläne: Für Wohnung 5-1-1-A nennt die Liste {N33.24} {U} überdachte und {N6.51} {U} offene Terrasse ({N39.75} {U}), der Plan {N35.53} {U}. Die Pläne nennen außerdem größere Flächen nach dem Dekret 218/2005, zum Beispiel {N120.94} {U} bebaute Fläche für Wohnung 2-2-BAJ-B gegenüber {N111.85} {U}. Wir klären, welche Zahl der Vertrag verwendet.",
  "Застроенная и внутренняя площади в прайс-листе совпадают с планами с точностью до {N0.01} {U}, но значения террас и крытых террас в прайс-листе на {N0.6}–{N4.2} {U} больше внешних площадей на планах: для квартиры 5-1-1-A в прайс-листе указано {N33.24} {U} крытой и {N6.51} {U} открытой террасы ({N39.75} {U}), на плане — {N35.53} {U}. На планах также указаны большие площади по Декрету 218/2005, например {N120.94} {U} застройки для квартиры 2-2-BAJ-B против {N111.85} {U}. Мы уточняем, какая цифра используется в договоре.",
  "تتطابق المساحتان المبنية والداخلية في قائمة الأسعار مع المخططات بفارق لا يتجاوز {N0.01} {U}، لكن أرقام التراس والرواق في القائمة أكبر بما يتراوح بين {N0.6} و{N4.2} {U} من المساحات الخارجية في المخططات: فبالنسبة للمنزل 5-1-1-A تذكر القائمة {N33.24} {U} من التراس المغطى و{N6.51} {U} من المكشوف ({N39.75} {U})، أما المخطط فيذكر {N35.53} {U}. كما تذكر المخططات مساحات أكبر بموجب المرسوم 218/2005، مثل {N120.94} {U} مبنية للمنزل 2-2-BAJ-B مقابل {N111.85} {U}. نتحقق من الرقم الذي يعتمده العقد.",
  "De bebouwde en binnenoppervlakten op de prijslijst komen met de plattegronden overeen tot op {N0.01} {U}, maar de terras- en verandacijfers van de lijst zijn {N0.6} tot {N4.2} {U} groter dan de buitenoppervlakten op de plattegronden: voor woning 5-1-1-A geeft de lijst {N33.24} {U} overdekt en {N6.51} {U} open terras ({N39.75} {U}), de plattegrond {N35.53} {U}. De plattegronden geven ook grotere oppervlakten volgens Decreet 218/2005, bijvoorbeeld {N120.94} {U} bebouwd voor woning 2-2-BAJ-B tegenover {N111.85} {U}. We bevestigen welk cijfer het contract hanteert.",
  "Powierzchnia zabudowy i powierzchnia wewnętrzna w cenniku zgadzają się z rzutami z dokładnością do {N0.01} {U}, ale wartości tarasów i wer w cenniku są o {N0.6}–{N4.2} {U} większe niż powierzchnie zewnętrzne na rzutach: dla mieszkania 5-1-1-A cennik podaje {N33.24} {U} tarasu zadaszonego i {N6.51} {U} odkrytego ({N39.75} {U}), a rzut {N35.53} {U}. Rzuty podają też większe powierzchnie według dekretu 218/2005, na przykład {N120.94} {U} zabudowy dla mieszkania 2-2-BAJ-B wobec {N111.85} {U}. Potwierdzamy, którą wartość przyjmuje umowa.",
  "Det bygde arealet og det innvendige arealet i prislisten stemmer med plantegningene med et avvik på høyst {N0.01} {U}, men listens terrasse- og uteplasstall er {N0.6} til {N4.2} {U} større enn de utvendige arealene på plantegningene: for bolig 5-1-1-A oppgir listen {N33.24} {U} overbygd og {N6.51} {U} åpen terrasse ({N39.75} {U}), plantegningen {N35.53} {U}. Plantegningene oppgir også større arealer etter dekret 218/2005, for eksempel {N120.94} {U} bygd for bolig 2-2-BAJ-B mot {N111.85} {U}. Vi bekrefter hvilket tall kontrakten bruker.",
  "Den byggda ytan och inre ytan i prislistan stämmer med planritningarna med en marginal på högst {N0.01} {U}, men listans siffror för terrass och veranda är {N0.6} till {N4.2} {U} större än de utvändiga ytorna på planritningarna: för bostad 5-1-1-A anger listan {N33.24} {U} övertäckt och {N6.51} {U} öppen terrass ({N39.75} {U}), planritningen {N35.53} {U}. Planritningarna anger också större ytor enligt dekret 218/2005, till exempel {N120.94} {U} byggyta för bostad 2-2-BAJ-B mot {N111.85} {U}. Vi bekräftar vilken siffra avtalet använder.")
P('.trustDossier.cards[2][0]',
  "Solárium en los áticos", "Solariums sur les penthouses", "Solarien bei den Penthäusern", "Солярии у пентхаусов", "سولاريوم للبنتهاوس",
  "Solariums bij de penthouses", "Solaria przy penthouse’ach", "Solterrasser på toppleilighetene", "Solterrasser på takvåningarna")
P('.trustDossier.cards[2][1]',
  "El texto del portal menciona áticos con solárium. Los planos de los cinco áticos de la lista muestran una planta con terraza y sin solárium. Preguntamos si alguno de los áticos de la lista lo tiene.",
  "Le texte du portail mentionne des penthouses avec solarium. Les plans des cinq penthouses annoncés montrent un seul niveau avec une terrasse et sans solarium. Nous demandons si l’un des penthouses annoncés en possède un.",
  "Der Portaltext erwähnt Penthäuser mit Solarium. Die Pläne der fünf gelisteten Penthäuser zeigen eine Ebene mit Terrasse und kein Solarium. Wir fragen nach, ob eines der gelisteten Penthäuser eines hat.",
  "В тексте портала упомянуты пентхаусы с солярием. На планах пяти пентхаусов из списка показан один уровень с террасой и нет солярия. Мы выясняем, есть ли солярий у какого-либо из пентхаусов в списке.",
  "يذكر نص موقع المطوّر بنتهاوس مع سولاريوم. وتُظهر مخططات البنتهاوس الخمسة المعروضة مستوى واحدًا بتراس ودون سولاريوم. نسأل عمّا إذا كان أي من البنتهاوس المعروضة يملك سولاريوم.",
  "De tekst van het portaal noemt penthouses met een solarium. De plattegronden van de vijf vermelde penthouses tonen één niveau met een terras en geen solarium. We vragen of een van de vermelde penthouses er een heeft.",
  "Tekst portalu wspomina o penthouse’ach z solarium. Rzuty pięciu wymienionych penthouse’ów pokazują jeden poziom z tarasem i brak solarium. Pytamy, czy któryś z wymienionych penthouse’ów je ma.",
  "Portalteksten nevner toppleiligheter med solterrasse. Plantegningene for de fem oppførte toppleilighetene viser ett plan med en terrasse og ingen solterrasse. Vi spør om noen av de oppførte toppleilighetene har en.",
  "Portaltexten nämner takvåningar med solterrass. Planritningarna för de fem listade takvåningarna visar ett plan med en terrass och ingen solterrass. Vi frågar om någon av de listade takvåningarna har en.")
P('.trustDossier.cards[3][0]',
  "Los planos y la fase", "Les plans et la phase", "Die Pläne und die Bauphase", "Планы и очередь", "المخططات والمرحلة",
  "De plattegronden en de fase", "Rzuty i etap", "Plantegningene og byggetrinnet", "Planritningarna och etappen")
P('.trustDossier.cards[3][1]',
  "Los planos indican que no son definitivos. Las hojas de planta baja son de abril de 2024 y siguen el proyecto básico; las demás son de diciembre de 2024 y siguen el proyecto de ejecución. El portal describe 135 viviendas sin decir cuántas pertenecen a esta fase.",
  "Les plans indiquent qu’ils ne sont pas définitifs. Les feuilles du rez-de-chaussée datent d’avril 2024 et suivent le projet de base ; les autres datent de décembre 2024 et suivent le projet d’exécution. Le portail décrit 135 logements sans dire combien font partie de cette phase.",
  "Die Pläne weisen darauf hin, dass sie nicht endgültig sind. Die Blätter der Erdgeschosswohnungen sind auf April 2024 datiert und folgen dem Basisprojekt; die übrigen sind auf Dezember 2024 datiert und folgen dem Ausführungsprojekt. Das Portal beschreibt 135 Wohnungen, ohne anzugeben, wie viele davon zu dieser Bauphase gehören.",
  "На планах указано, что они не окончательные. Листы первого этажа датированы апрелем 2024 года и соответствуют базовому проекту, остальные — декабрём 2024 года и соответствуют рабочему проекту. Портал описывает 135 квартир, не сообщая, сколько из них относится к этой очереди.",
  "تذكر المخططات أنها غير نهائية. مخططات الطابق الأرضي مؤرخة في أبريل 2024 وتتبع المشروع الأساسي، والبقية مؤرخة في ديسمبر 2024 وتتبع مشروع التنفيذ. ويصف موقع المطوّر 135 منزلًا دون أن يذكر كم منها في هذه المرحلة.",
  "De plattegronden zeggen dat ze niet definitief zijn. De bladen van de begane grond zijn gedateerd april 2024 en volgen het basisproject; de overige zijn gedateerd december 2024 en volgen het uitvoeringsproject. Het portaal beschrijft 135 woningen zonder te zeggen hoeveel er in deze fase zitten.",
  "Rzuty zastrzegają, że nie są ostateczne. Arkusze parteru są datowane na kwiecień 2024 r. i odpowiadają projektowi podstawowemu, pozostałe na grudzień 2024 r. i odpowiadają projektowi wykonawczemu. Portal opisuje 135 mieszkań, nie podając, ile z nich należy do tego etapu.",
  "Plantegningene sier at de ikke er endelige. Arkene for første etasje er datert april 2024 og følger grunnprosjektet; de øvrige er datert desember 2024 og følger gjennomføringsprosjektet. Portalen beskriver 135 boliger uten å si hvor mange som hører til dette byggetrinnet.",
  "Planritningarna anger att de inte är slutgiltiga. Ritningarna för bottenvåningen är daterade april 2024 och följer grundprojektet; de övriga är daterade december 2024 och följer genomförandeprojektet. Portalen beskriver 135 bostäder utan att säga hur många som ingår i den här etappen.")

# ---- availability
P('.availability.headlineHtml',
  "12 viviendas <em>a la venta actualmente</em>", "12 logements <em>actuellement annoncés</em>", "12 Wohnungen <em>derzeit gelistet</em>",
  "12 квартир <em>сейчас в продаже</em>", "12 منزلًا <em>معروضة حاليًا</em>", "12 woningen <em>momenteel te koop</em>",
  "12 mieszkań <em>obecnie dostępnych</em>", "12 boliger <em>annonsert nå</em>", "12 bostäder <em>listade just nu</em>")

P('.availability.copy',
  "Los precios son los de la lista de precios del promotor a octubre de 2026 y se confirman antes de la reserva. Las 12 viviendas de abajo son todas apartamentos y áticos de dos dormitorios y dos baños.",
  "Les prix sont ceux de la liste de prix du promoteur à octobre 2026 et sont confirmés avant la réservation. Les 12 logements ci-dessous sont tous des appartements et penthouses de deux chambres et deux salles de bain.",
  "Die Preise stammen aus der Preisliste des Bauträgers mit Stand Oktober 2026 und werden vor der Reservierung bestätigt. Die 12 Wohnungen unten sind durchweg Wohnungen und Penthäuser mit zwei Schlafzimmern und zwei Bädern.",
  "Цены взяты из прайс-листа застройщика на октябрь 2026 года и подтверждаются перед бронированием. Все 12 перечисленных ниже объектов — апартаменты и пентхаусы с двумя спальнями и двумя ванными комнатами.",
  "الأسعار هي أسعار قائمة المطوّر في أكتوبر 2026 وتُؤكَّد قبل الحجز. جميع المنازل الـ12 أدناه شقق وبنتهاوس بغرفتي نوم وحمامين.",
  "De prijzen komen uit de prijslijst van de ontwikkelaar per oktober 2026 en worden vóór de reservering bevestigd. De 12 woningen hieronder zijn allemaal appartementen en penthouses met twee slaapkamers en twee badkamers.",
  "Ceny pochodzą z cennika dewelopera z października 2026 r. i są potwierdzane przed rezerwacją. Wszystkie 12 mieszkań poniżej to apartamenty i penthouse’y z dwiema sypialniami i dwiema łazienkami.",
  "Prisene er fra utbyggerens prisliste per oktober 2026 og bekreftes før reservasjon. De 12 boligene nedenfor er alle leiligheter og toppleiligheter med to soverom og to bad.",
  "Priserna kommer från exploatörens prislista per oktober 2026 och bekräftas före reservation. De 12 bostäderna nedan är alla lägenheter och takvåningar med två sovrum och två badrum.")

P('.availability.priceRange',
  "{E332000} - {E455000} + IVA", "{E332000} - {E455000} + TVA", "{E332000} - {E455000} + MwSt.", "{E332000} - {E455000} + НДС",
  "{E332000} - {E455000} + ضريبة القيمة المضافة", "{E332000} - {E455000} + btw", "{E332000} - {E455000} + VAT",
  "{E332000} - {E455000} + mva.", "{E332000} - {E455000} + moms")

P('.availability.sourceNote',
  "Los precios, las superficies y la disponibilidad están transcritos de la lista de precios del promotor para la primera fase, tal como figura en su portal en octubre de 2026, que marca las 12 viviendas como disponibles e indica que los precios no incluyen el IVA sin dar el tipo. La superficie construida incluye una parte proporcional de zonas comunes, como indican los planos. La terraza indicada es la cifra de porche de la lista para las viviendas de planta baja y su cifra de terraza para las demás; cuando la lista da una terraza cubierta y otra descubierta (viviendas 5-1-1-A, 5-2-ATC-C, 5-3-ATC-A y 9-2-ATC-A) la tabla las suma, y la vivienda 5-1-BAJ-A tiene además un jardín de {N31.00} {U}. Las cifras de terraza de la lista son entre {N0.6} y {N4.2} {U} mayores que las superficies exteriores de los planos. La lista indica una plaza de garaje y un trastero por vivienda y no dice si están incluidos en el precio. Las referencias se leen bloque, portal, planta y puerta, como en los planos.",
  "Les prix, les surfaces et la disponibilité sont transcrits de la liste de prix du promoteur pour la première phase, telle qu’elle figure sur son portail en octobre 2026, qui indique les 12 logements comme disponibles et précise que les prix s’entendent hors TVA sans en donner le taux. La surface construite inclut une quote-part de parties communes, comme l’indiquent les plans. La terrasse indiquée est le chiffre de porche de la liste pour les logements du rez-de-chaussée et son chiffre de terrasse pour les autres ; lorsque la liste donne une terrasse couverte et une terrasse découverte (logements 5-1-1-A, 5-2-ATC-C, 5-3-ATC-A et 9-2-ATC-A), le tableau les additionne, et le logement 5-1-BAJ-A a en outre un jardin de {N31.00} {U}. Les chiffres de terrasse de la liste dépassent de {N0.6} à {N4.2} {U} les surfaces extérieures des plans. La liste indique une place de garage et un local de rangement par logement et ne dit pas s’ils sont compris dans le prix. Les références se lisent bloc, cage, étage et porte, comme sur les plans.",
  "Preise, Flächen und Verfügbarkeit sind der Preisliste des Bauträgers für die erste Bauphase entnommen, wie sie im Oktober 2026 auf seinem Portal stand; sie weist alle 12 Wohnungen als verfügbar aus und nennt die Preise ohne MwSt., ohne den Satz anzugeben. Die bebaute Fläche enthält einen Anteil an Gemeinschaftsflächen, wie die Pläne angeben. Die angegebene Terrasse ist bei den Erdgeschosswohnungen der Verandawert der Liste und bei den übrigen ihr Terrassenwert; wo die Liste eine überdachte und eine offene Terrasse nennt (Wohnungen 5-1-1-A, 5-2-ATC-C, 5-3-ATC-A und 9-2-ATC-A), addiert die Tabelle beide, und Wohnung 5-1-BAJ-A hat zusätzlich einen Garten von {N31.00} {U}. Die Terrassenwerte der Liste liegen {N0.6} bis {N4.2} {U} über den Außenflächen der Pläne. Die Liste nennt je Wohnung einen Garagenstellplatz und einen Abstellraum und sagt nicht, ob sie im Preis enthalten sind. Die Referenzen lesen sich als Block, Aufgang, Etage und Tür, wie auf den Plänen.",
  "Цены, площади и наличие перенесены из прайс-листа застройщика по первой очереди, как он был показан на его портале в октябре 2026 года; в нём все 12 квартир отмечены как доступные, а цены указаны без НДС, ставка не названа. Застроенная площадь включает долю общих зон, как указано на планах. Указанная терраса — это значение «porche» (крытая терраса) из прайс-листа у квартир первого этажа и значение террасы у остальных; если в прайс-листе указаны крытая и открытая террасы (квартиры 5-1-1-A, 5-2-ATC-C, 5-3-ATC-A и 9-2-ATC-A), в таблице они сложены, а у квартиры 5-1-BAJ-A есть ещё и сад {N31.00} {U}. Значения террас в прайс-листе на {N0.6}–{N4.2} {U} больше внешних площадей на планах. В прайс-листе у каждой квартиры указаны одно гаражное место и одна кладовая, а входят ли они в цену, не сказано. Обозначения читаются как блок, подъезд, этаж и дверь, как на планах.",
  "الأسعار والمساحات والتوفر منقولة من قائمة أسعار المطوّر للمرحلة الأولى كما ظهرت على موقعه في أكتوبر 2026، وهي تضع علامة «متاح» على المنازل الـ12 كلها وتنص على أن الأسعار لا تشمل ضريبة القيمة المضافة دون ذكر نسبتها. وتشمل المساحة المبنية حصة من المناطق المشتركة كما تذكر المخططات. والتراس المذكور هو رقم الرواق في القائمة لمنازل الطابق الأرضي ورقم التراس فيها لبقية المنازل؛ وحيث تذكر القائمة تراسًا مغطى وآخر مكشوفًا (المنازل 5-1-1-A و5-2-ATC-C و5-3-ATC-A و9-2-ATC-A) يجمعهما الجدول، وللمنزل 5-1-BAJ-A حديقة إضافية مساحتها {N31.00} {U}. وأرقام التراس في القائمة أكبر بما يتراوح بين {N0.6} و{N4.2} {U} من المساحات الخارجية في المخططات. وتذكر القائمة موقف سيارات واحدًا في المرآب وغرفة تخزين واحدة لكل منزل ولا تبيّن إن كانا ضمن السعر. وتُقرأ المراجع: مبنى ومدخل وطابق وباب، كما في المخططات.",
  "Prijzen, oppervlakten en beschikbaarheid zijn overgenomen uit de prijslijst van de ontwikkelaar voor de eerste fase zoals die in oktober 2026 op zijn portaal stond; die markeert alle 12 woningen als beschikbaar en vermeldt dat de prijzen exclusief btw zijn, zonder het tarief te noemen. De bebouwde oppervlakte bevat een aandeel in de gemeenschappelijke ruimten, zoals de plattegronden aangeven. Het getoonde terras is bij de woningen op de begane grond het cijfer voor ‘porche’ (overdekt terras) van de lijst en bij de overige het terrascijfer; waar de lijst een overdekt en een open terras geeft (woningen 5-1-1-A, 5-2-ATC-C, 5-3-ATC-A en 9-2-ATC-A) telt de tabel ze op, en woning 5-1-BAJ-A heeft daarnaast een tuin van {N31.00} {U}. De terrascijfers van de lijst zijn {N0.6} tot {N4.2} {U} groter dan de buitenoppervlakten op de plattegronden. De lijst vermeldt per woning een garageplaats en een berging en zegt niet of die in de prijs zijn inbegrepen. De referenties lezen als blok, portiek, verdieping en deur, zoals op de plattegronden.",
  "Ceny, powierzchnie i dostępność przepisano z cennika dewelopera dla pierwszego etapu, tak jak widniał na jego portalu w październiku 2026 r.; oznacza on wszystkie 12 mieszkań jako dostępne i podaje, że ceny nie zawierają VAT, nie wskazując stawki. Powierzchnia zabudowy obejmuje udział w częściach wspólnych, jak podają rzuty. Podany taras to w przypadku mieszkań na parterze wartość z cennika dla werandy („porche”), a w pozostałych wartość tarasu; tam, gdzie cennik podaje taras zadaszony i odkryty (mieszkania 5-1-1-A, 5-2-ATC-C, 5-3-ATC-A i 9-2-ATC-A), tabela je sumuje, a mieszkanie 5-1-BAJ-A ma dodatkowo ogród o powierzchni {N31.00} {U}. Wartości tarasów w cenniku są o {N0.6}–{N4.2} {U} większe niż powierzchnie zewnętrzne na rzutach. Cennik podaje dla każdego mieszkania jedno miejsce w garażu i jedną komórkę lokatorską i nie mówi, czy są wliczone w cenę. Oznaczenia czyta się jako blok, klatka, piętro i drzwi, tak jak na rzutach.",
  "Priser, arealer og tilgjengelighet er gjengitt fra utbyggerens prisliste for første byggetrinn slik den sto på portalen i oktober 2026, som markerer alle 12 boligene som ledige og oppgir at prisene er eksklusive mva., uten å oppgi satsen. Det bygde arealet inkluderer en andel av fellesarealene, slik plantegningene angir. Terrassen som vises er listens tall for «porche» (overbygd uteplass) for boligene i første etasje og listens terrassetall for de øvrige; der listen oppgir en overbygd og en åpen terrasse (boligene 5-1-1-A, 5-2-ATC-C, 5-3-ATC-A og 9-2-ATC-A) legger tabellen dem sammen, og bolig 5-1-BAJ-A har i tillegg en hage på {N31.00} {U}. Listens terrassetall er {N0.6} til {N4.2} {U} større enn de utvendige arealene på plantegningene. Listen oppgir én garasjeplass og ett bod per bolig og sier ikke om de er inkludert i prisen. Referansene leses som hus, oppgang, etasje og dør, som på plantegningene.",
  "Priser, ytor och tillgänglighet är hämtade från exploatörens prislista för första etappen, så som den stod på portalen i oktober 2026, som markerar alla 12 bostäderna som lediga och anger att priserna är exklusive moms, utan att ange satsen. Den byggda ytan inkluderar en andel av de gemensamma ytorna, som planritningarna anger. Terrassen som visas är listans siffra för ”porche” (veranda) för bostäderna på bottenvåningen och listans terrasssiffra för övriga; där listan anger en övertäckt och en öppen terrass (bostäderna 5-1-1-A, 5-2-ATC-C, 5-3-ATC-A och 9-2-ATC-A) summerar tabellen dem, och bostad 5-1-BAJ-A har dessutom en trädgård på {N31.00} {U}. Listans terrasssiffror är {N0.6} till {N4.2} {U} större än de utvändiga ytorna på planritningarna. Listan anger en garageplats och ett förråd per bostad och säger inte om de ingår i priset. Referenserna läses som hus, uppgång, våning och dörr, som på planritningarna.")

# unit references, floors and sizes: pass-through; the unit overlay is stripped after assemble
for path, en in ALL_PATHS.items():
    if '.availability.units[' in path and path.endswith(('.reference', '.size', '.floor')):
        if en not in T:
            T[en] = {l: en for l in LOCS}
            USED.add(en)

# ---- timeline, viewing, enquiry, faq
P('.timeline.items[3][2]',
  "Confirmamos por escrito las condiciones y el calendario de pagos, y después el contrato privado de compraventa.",
  "Nous confirmons par écrit les conditions et l’échéancier de paiement, puis vient le contrat de vente privé.",
  "Wir bestätigen die Bedingungen und den Zahlungsplan schriftlich, dann folgt der private Kaufvertrag.",
  "Мы письменно подтверждаем условия и график платежей, затем следует предварительный договор купли-продажи.",
  "نؤكد كتابةً الشروط وجدول الدفعات، ثم يأتي عقد الشراء الخاص.",
  "We bevestigen de voorwaarden en het betalingsschema schriftelijk, daarna volgt de onderhandse koopovereenkomst.",
  "Potwierdzamy na piśmie warunki i harmonogram płatności, a następnie podpisywana jest umowa przedwstępna.",
  "Vi bekrefter vilkårene og betalingsplanen skriftlig, deretter den private kjøpekontrakten.",
  "Vi bekräftar villkoren och betalningsplanen skriftligen, därefter det privata köpeavtalet.")

P('.privateViewing.insights[0][1]',
  "Recorra con nosotros la zona junto al club de golf y vea hasta dónde han llegado las obras.",
  "Parcourez avec nous le quartier à côté du club de golf et voyez où en sont les travaux.",
  "Besuchen Sie mit uns die Umgebung neben dem Golfclub und sehen Sie, wie weit die Bauarbeiten sind.",
  "Осмотрите вместе с нами район рядом с гольф-клубом и посмотрите, как продвинулись работы.",
  "زر معنا المنطقة المجاورة لنادي الغولف وانظر إلى أي مدى تقدمت الأعمال.",
  "Bezoek met ons de omgeving naast de golfclub en zie hoe ver de werken zijn.",
  "Wizyta w okolicy obok klubu golfowego i sprawdzenie, jak daleko posunęły się prace.",
  "Besøk området ved siden av golfklubben med oss og se hvor langt arbeidene har kommet.",
  "Besök området intill golfklubben med oss och se hur långt byggarbetena har kommit.")

P('.enquiry.headlineHtml',
  "Pregunte por <em>Almendro Homes</em>", "Renseignez-vous sur <em>Almendro Homes</em>", "Fragen Sie nach <em>Almendro Homes</em>",
  "Узнайте о <em>Almendro Homes</em>", "استفسر عن <em>Almendro Homes</em>", "Vraag naar <em>Almendro Homes</em>",
  "Zapytanie o <em>Almendro Homes</em>", "Spør om <em>Almendro Homes</em>", "Fråga om <em>Almendro Homes</em>")

P('.enquiry.message',
  "Hola, Nueva Living, me gustaría recibir información sobre Almendro Homes.",
  "Bonjour Nueva Living, je souhaiterais des informations sur Almendro Homes.",
  "Guten Tag Nueva Living, ich möchte Informationen zu Almendro Homes erhalten.",
  "Здравствуйте, Nueva Living! Хочу получить информацию о Almendro Homes.",
  "مرحبًا Nueva Living، أودّ الحصول على معلومات عن Almendro Homes.",
  "Goedendag Nueva Living, ik wil graag informatie over Almendro Homes.",
  "Dzień dobry, Nueva Living, proszę o informacje o Almendro Homes.",
  "Hei Nueva Living, jeg vil gjerne ha informasjon om Almendro Homes.",
  "Hej Nueva Living, jag vill gärna ha information om Almendro Homes.")

P('.faq[0][1]',
  "El portal del promotor describe el conjunto como 135 viviendas de uno, dos y tres dormitorios. La lista de precios de esta fase recoge 12, todas de dos dormitorios y dos baños, de {E332000} a {E455000} más IVA.",
  "Le portail du promoteur décrit la résidence comme 135 logements d’une, deux et trois chambres. La liste de prix de cette phase en recense 12, tous de deux chambres et deux salles de bain, de {E332000} à {E455000} hors TVA.",
  "Das Portal des Bauträgers beschreibt die Anlage als 135 Wohnungen mit einem, zwei und drei Schlafzimmern. Die Preisliste dieser Bauphase führt 12 auf, alle mit zwei Schlafzimmern und zwei Bädern, von {E332000} bis {E455000} zuzüglich MwSt.",
  "Портал застройщика описывает комплекс как 135 квартир с одной, двумя и тремя спальнями. В прайс-листе этой очереди указаны 12, все с двумя спальнями и двумя ванными комнатами, от {E332000} до {E455000} без НДС.",
  "يصف موقع المطوّر المجمع بأنه 135 منزلًا بغرفة نوم وغرفتين وثلاث غرف نوم. وتُدرج قائمة أسعار هذه المرحلة 12 منها، جميعها بغرفتي نوم وحمامين، من {E332000} إلى {E455000} دون ضريبة القيمة المضافة.",
  "Het portaal van de ontwikkelaar beschrijft het complex als 135 woningen met een, twee en drie slaapkamers. De prijslijst van deze fase toont er 12, allemaal met twee slaapkamers en twee badkamers, van {E332000} tot {E455000} excl. btw.",
  "Portal dewelopera opisuje osiedle jako 135 mieszkań z jedną, dwiema i trzema sypialniami. Cennik tego etapu wymienia 12, wszystkie z dwiema sypialniami i dwiema łazienkami, od {E332000} do {E455000} plus VAT.",
  "Utbyggerens portal beskriver anlegget som 135 boliger med ett, to og tre soverom. Prislisten for dette byggetrinnet viser 12, alle med to soverom og to bad, fra {E332000} til {E455000} pluss mva.",
  "Exploatörens portal beskriver området som 135 bostäder med ett, två och tre sovrum. Prislistan för den här etappen visar 12, alla med två sovrum och två badrum, från {E332000} till {E455000} plus moms.")

P('.faq[1][1]',
  "No. La lista de precios indica que los precios no incluyen el IVA y no da el tipo. Confirmamos por escrito los impuestos y los gastos de compra.",
  "Non. La liste de prix indique que les prix n’incluent pas la TVA et n’en donne pas le taux. Nous confirmons par écrit les taxes et les frais d’achat.",
  "Nein. Laut Preisliste verstehen sich die Preise zuzüglich MwSt.; den Satz nennt sie nicht. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.",
  "Нет. В прайс-листе сказано, что цены не включают НДС; ставка не названа. Налоги и расходы на покупку мы письменно подтверждаем.",
  "لا. تذكر قائمة الأسعار أن الأسعار لا تشمل ضريبة القيمة المضافة ولا تذكر نسبتها. ونؤكد الضرائب ومصاريف الشراء كتابةً.",
  "Nee. De prijslijst vermeldt dat de prijzen exclusief btw zijn en geeft het tarief niet. We bevestigen de belastingen en aankoopkosten schriftelijk.",
  "Nie. Cennik podaje, że ceny nie zawierają VAT, i nie wskazuje stawki. Podatki i koszty zakupu potwierdzamy na piśmie.",
  "Nei. Prislisten oppgir at prisene ikke inkluderer mva., og oppgir ikke satsen. Vi bekrefter skatter og kjøpskostnader skriftlig.",
  "Nej. Prislistan anger att priserna inte inkluderar moms och anger inte satsen. Vi bekräftar skatter och köpkostnader skriftligen.")

P('.faq[2][1]',
  "La lista de precios indica una plaza de garaje y un trastero por vivienda. No dice si están incluidos en el precio, así que lo confirmamos.",
  "La liste de prix indique une place de garage et un local de rangement par logement. Elle ne dit pas s’ils sont compris dans le prix ; nous le confirmons donc.",
  "Die Preisliste nennt je Wohnung einen Garagenstellplatz und einen Abstellraum. Sie sagt nicht, ob sie im Preis enthalten sind, daher klären wir das.",
  "В прайс-листе у каждой квартиры указаны одно гаражное место и одна кладовая. Входят ли они в цену, не сказано, поэтому мы это уточняем.",
  "تذكر قائمة الأسعار موقف سيارات واحدًا في المرآب وغرفة تخزين واحدة لكل منزل. ولا تبيّن إن كانا ضمن السعر، لذلك نؤكد ذلك.",
  "De prijslijst vermeldt per woning een garageplaats en een berging. Ze zegt niet of die in de prijs zijn inbegrepen, dus we bevestigen dat.",
  "Cennik podaje dla każdego mieszkania jedno miejsce w garażu i jedną komórkę lokatorską. Nie mówi, czy są wliczone w cenę, dlatego to potwierdzamy.",
  "Prislisten oppgir én garasjeplass og ett bod per bolig. Den sier ikke om de er inkludert i prisen, så det bekrefter vi.",
  "Prislistan anger en garageplats och ett förråd per bostad. Den säger inte om de ingår i priset, så det bekräftar vi.")

P('.faq[3][1]',
  "Ningún documento de que disponemos da una fecha de finalización. El portal tiene una página del estado de las obras que no recibimos, así que pedimos el estado de las obras y la fecha contractual.",
  "Aucun document dont nous disposons ne donne de date d’achèvement. Le portail comporte une page sur l’avancement des travaux que nous n’avons pas reçue ; nous demandons donc l’état d’avancement et la date contractuelle.",
  "Kein uns vorliegendes Dokument nennt einen Fertigstellungstermin. Das Portal hat eine Seite zum Baufortschritt, die wir nicht erhalten haben, daher fragen wir den Baustand und den vertraglichen Termin an.",
  "Ни в одном из имеющихся у нас документов нет срока завершения. На портале есть страница о ходе работ, которую мы не получили, поэтому мы запрашиваем стадию работ и договорную дату.",
  "لا تذكر أي وثيقة لدينا موعدًا للإنجاز. ويضم موقع المطوّر صفحة لحالة الأعمال لم نتلقَّها، لذلك نطلب مرحلة الأعمال والتاريخ التعاقدي.",
  "In geen enkel document waarover we beschikken staat een opleveringsdatum. Het portaal heeft een pagina over de voortgang van de werken die we niet hebben ontvangen, dus we vragen naar de stand van de werken en de contractuele datum.",
  "Żaden z dokumentów, którymi dysponujemy, nie podaje terminu ukończenia. Portal zawiera stronę o stanie prac, której nie otrzymaliśmy, dlatego prosimy o stan prac i termin wskazany w umowie.",
  "Ingen av dokumentene vi har oppgir en ferdigstillelsesdato. Portalen har en side om framdriften i arbeidene som vi ikke fikk, så vi ber om status for arbeidene og den kontraktsfestede datoen.",
  "Inget av dokumenten vi har anger ett färdigställandedatum. Portalen har en sida om byggstatus som vi inte fick, så vi ber om byggstatus och det avtalade datumet.")

P('.faq[4][1]',
  "El portal no indica ningún pago de reserva. Los compradores residentes fuera de España pagan el 30% más IVA al firmar el contrato privado de compraventa y el 70% más IVA a la finalización ante notario; los residentes en España pagan el 20% más IVA y el 80% más IVA.",
  "Le portail n’indique aucun versement de réservation. Les acheteurs résidant hors d’Espagne paient 30 % hors TVA à la signature du contrat de vente privé et 70 % hors TVA à l’achèvement chez le notaire ; ceux qui résident en Espagne paient 20 % et 80 % hors TVA.",
  "Das Portal nennt keine Reservierungszahlung. Käufer mit Wohnsitz außerhalb Spaniens zahlen 30 % zuzüglich MwSt. bei Unterzeichnung des privaten Kaufvertrags und 70 % zuzüglich MwSt. bei Fertigstellung beim Notar; Käufer mit Wohnsitz in Spanien zahlen 20 % zuzüglich MwSt. und 80 % zuzüglich MwSt.",
  "На портале не указан платёж за бронирование. Покупатели, проживающие за пределами Испании, платят 30 % плюс НДС при подписании предварительного договора купли-продажи и 70 % плюс НДС при завершении сделки у нотариуса; проживающие в Испании — 20 % плюс НДС и 80 % плюс НДС.",
  "لا يذكر موقع المطوّر أي دفعة حجز. يدفع المشترون المقيمون خارج إسبانيا 30% زائد ضريبة القيمة المضافة عند توقيع عقد الشراء الخاص و70% زائد الضريبة عند الإتمام أمام كاتب العدل؛ ويدفع المقيمون في إسبانيا 20% زائد الضريبة و80% زائد الضريبة.",
  "Het portaal vermeldt geen reserveringsbetaling. Kopers die buiten Spanje wonen betalen 30% plus btw bij ondertekening van de onderhandse koopovereenkomst en 70% plus btw bij oplevering ten overstaan van de notaris; kopers die in Spanje wonen betalen 20% plus btw en 80% plus btw.",
  "Portal nie podaje opłaty rezerwacyjnej. Kupujący mieszkający poza Hiszpanią płacą 30% plus VAT przy podpisaniu umowy przedwstępnej i 70% plus VAT u notariusza, przy akcie notarialnym; kupujący mieszkający w Hiszpanii płacą 20% plus VAT i 80% plus VAT.",
  "Portalen oppgir ingen reservasjonsbetaling. Kjøpere bosatt utenfor Spania betaler 30 % pluss mva. ved signering av den private kjøpekontrakten og 70 % pluss mva. ved overtakelse hos notarius; kjøpere bosatt i Spania betaler 20 % pluss mva. og 80 % pluss mva.",
  "Portalen anger ingen reservationsbetalning. Köpare bosatta utanför Spanien betalar 30 % plus moms vid undertecknandet av det privata köpeavtalet och 70 % plus moms vid tillträdet hos notarien; köpare bosatta i Spanien betalar 20 % plus moms och 80 % plus moms.")

P('.faq[5][0]',
  "¿Los áticos tienen solárium?", "Les penthouses ont-ils un solarium ?", "Haben die Penthäuser ein Solarium?", "Есть ли у пентхаусов солярий?",
  "هل للبنتهاوس سولاريوم؟", "Hebben de penthouses een solarium?", "Czy penthouse’y mają solarium?", "Har toppleilighetene en solterrasse?",
  "Har takvåningarna en solterrass?")
P('.faq[5][1]',
  "El texto del portal menciona áticos con solárium, pero los planos de los cinco áticos de la lista muestran una terraza y ninguna planta de solárium. Lo confirmamos antes de cualquier reserva.",
  "Le texte du portail mentionne des penthouses avec solarium, mais les plans des cinq penthouses annoncés montrent une terrasse et aucun niveau de solarium. Nous le confirmons avant toute réservation.",
  "Der Portaltext erwähnt Penthäuser mit Solarium, doch die Pläne der fünf gelisteten Penthäuser zeigen eine Terrasse und keine Solarium-Ebene. Wir klären das vor jeder Reservierung.",
  "В тексте портала упомянуты пентхаусы с солярием, но на планах пяти пентхаусов из списка показаны терраса и нет уровня с солярием. Мы уточняем это до любого бронирования.",
  "يذكر نص موقع المطوّر بنتهاوس مع سولاريوم، لكن مخططات البنتهاوس الخمسة المعروضة تُظهر تراسًا ولا تُظهر مستوى للسولاريوم. نؤكد ذلك قبل أي حجز.",
  "De tekst van het portaal noemt penthouses met een solarium, maar de plattegronden van de vijf vermelde penthouses tonen een terras en geen solariumniveau. We bevestigen dit vóór elke reservering.",
  "Tekst portalu wspomina o penthouse’ach z solarium, ale rzuty pięciu wymienionych penthouse’ów pokazują taras i brak poziomu solarium. Potwierdzamy to przed każdą rezerwacją.",
  "Portalteksten nevner toppleiligheter med solterrasse, men plantegningene for de fem oppførte toppleilighetene viser en terrasse og ikke noe plan for solterrasse. Vi bekrefter det før en reservasjon.",
  "Portaltexten nämner takvåningar med solterrass, men planritningarna för de fem listade takvåningarna visar en terrass och inget plan för solterrass. Vi bekräftar det före varje reservation.")

# ---- coverage: every English string in todo.json that is not a floor label must have been given
missing = [en for en in TODO if en not in T and not re.fullmatch(r'Block \d+, Portal \d+, [A-Za-z ]+', en)]
if missing:
    print('NOT COVERED', len(missing))
    for m in missing: print('  ', m[:110], TODO[m][:1])
    sys.exit(1)
json.dump(T, open(f'{SP}/tr_z.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries to', f'{SP}/tr_z.json')
