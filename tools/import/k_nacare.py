# -*- coding: utf-8 -*-
"""Nacare (Estepona): the strings the translation memory did not have, written by path.

p(path, es, fr, de, ru, ar, nl, pl, no, sv)

The English string is looked up from the path scaffold.py printed in todo.json, so it is never copied
here and cannot drift from project.json. Tokens, expanded per locale so a figure is written once and
takes its locale's own format: {E3700000} money ("3.700.000 €", nl "€ 3.700.000", fr/ru/pl/no/sv
"3 700 000 €", ar "3,700,000 €"), {N230.07} a decimal number (ar keeps the point), {U} the area unit.

The six unit rows and the plan alts and captions are built from templates at the foot of the file,
with the same words las-mesas-blue-horizon uses.

    python3 tools/import/k_nacare.py <workdir>/tr_n.json <workdir>/todo.json
"""
import json, re, sys

LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}
UNIT['ru'] = 'м²'
UNIT['ar'] = 'م²'


def money(n, loc):
    body = f'{n:,}'.replace(',', GROUP[loc])
    return f'€ {body}' if loc == 'nl' else f'{body} €'


def num(s, loc):
    return s.replace(',', GROUP[loc]).replace('.', '.' if loc == 'ar' else ',')


def expand(s, loc):
    s = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), loc), s)
    s = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), loc), s)
    return s.replace('{U}', UNIT[loc])


BAD = []
SKIPPED = []
T = {}
TODO = json.load(open(sys.argv[2]))
BY_PATH = {paths[0]: en for en, paths in TODO.items()}
USED = set()


def p(path, *tr):
    if len(tr) != 9:
        BAD.append((path, len(tr)))
        return
    if path not in BY_PATH:
        SKIPPED.append(path)
        return
    en = BY_PATH[path]
    USED.add(path)
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---- identifiers that read the same in every language --------------------------------------------
for path, en in BY_PATH.items():
    if en in ('Nacare', 'Nacare <em>Estepona</em>', 'Ronda'):
        T[en] = {l: en for l in LOCS}
        USED.add(path)
    if path.endswith('.phase') and en == '':
        T[en] = {l: '' for l in LOCS}
        USED.add(path)

# ---- description, SEO, hero, card ------------------------------------------------------------------
p('.description',
  '6 de 20 apartamentos y áticos de tres y cuatro dormitorios en un edificio nuevo en Estepona, con vistas al mar y a la montaña, spa con piscina interior climatizada, skypool y salón en la azotea, gimnasio y club de propietarios, y de dos a cuatro plazas de garaje con cada vivienda listada. La licencia de obras está pendiente y no se indica fecha de finalización. Desde {E2500000} más IVA.',
  '6 appartements et penthouses sur 20, de trois et quatre chambres, dans un nouvel immeuble à Estepona, avec vue sur la mer et la montagne, un spa avec piscine intérieure chauffée, une skypool et un salon sur le toit, une salle de sport et un club des propriétaires, et de deux à quatre places de garage avec chaque logement annoncé. Le permis de construire est en attente et aucune date d’achèvement n’est indiquée. À partir de {E2500000} hors TVA.',
  '6 von 20 Wohnungen und Penthäusern mit drei und vier Schlafzimmern in einem neuen Gebäude in Estepona, mit Meer- und Bergblick, einem Spa mit beheiztem Innenpool, einem Skypool und einer Dachlounge, einem Fitnessraum und einem Eigentümerclub sowie zwei bis vier Garagenstellplätzen bei jeder gelisteten Wohnung. Die Baugenehmigung steht noch aus, und ein Fertigstellungstermin wird nicht genannt. Ab {E2500000} zuzüglich MwSt.',
  '6 из 20 апартаментов и пентхаусов с тремя и четырьмя спальнями в новом здании в Эстепоне: вид на море и горы, спа с подогреваемым крытым бассейном, скайпул и лаунж на крыше, тренажёрный зал и клуб владельцев, а к каждому объекту в списке — от двух до четырёх мест в гараже. Разрешение на строительство ещё ожидается, срок завершения не указан. От {E2500000} без НДС.',
  '6 من أصل 20 شقة وبنتهاوس بثلاث وأربع غرف نوم في مبنى جديد في إستيبونا، بإطلالة على البحر والجبال، مع سبا ومسبح داخلي مدفأ ومسبح سكاي وصالة على السطح وصالة رياضية ونادٍ للملاك، ومن موقفين إلى أربعة مواقف في المرآب مع كل مسكن مدرج. رخصة البناء قيد الانتظار ولم يُذكر موعد للإنجاز. ابتداءً من {E2500000} دون ضريبة القيمة المضافة.',
  '6 van de 20 appartementen en penthouses met drie en vier slaapkamers in een nieuw gebouw in Estepona, met zeezicht en uitzicht op de bergen, een spa met verwarmd binnenzwembad, een skypool en een lounge op het dak, een fitnessruimte en een eigenarenclub, en twee tot vier garageplaatsen bij elke aangeboden woning. De bouwvergunning is nog in afwachting en er wordt geen opleveringsdatum genoemd. Vanaf {E2500000} excl. btw.',
  '6 z 20 apartamentów i penthouse’ów z trzema i czterema sypialniami w nowym budynku w Esteponie, z widokiem na morze i góry, spa z podgrzewanym basenem wewnętrznym, skypoolem i lounge’em na dachu, siłownią i klubem właścicieli oraz z dwoma do czterech miejsc garażowych przy każdym oferowanym lokalu. Pozwolenie na budowę jest w toku, a termin ukończenia nie jest podany. Od {E2500000} plus VAT.',
  '6 av 20 leiligheter og toppleiligheter med tre og fire soverom i en ny bygning i Estepona, med utsikt over havet og fjellene, et spa med oppvarmet innendørsbasseng, en skypool og en lounge på taket, treningsrom og eierklubb, og to til fire garasjeplasser til hver oppførte bolig. Byggetillatelsen er ikke på plass ennå, og ingen ferdigstillelsesdato er oppgitt. Fra {E2500000} pluss mva.',
  '6 av 20 lägenheter och takvåningar med tre och fyra sovrum i en ny byggnad i Estepona, med utsikt över havet och bergen, ett spa med uppvärmd inomhuspool, en skypool och en lounge på taket, ett gym och en ägarklubb samt två till fyra garageplatser till varje listad bostad. Bygglovet är ännu inte beviljat och inget färdigställandedatum anges. Från {E2500000} plus IVA (spansk moms).')

p('.seoDescription',
  '6 de 20 apartamentos y áticos de tres y cuatro dormitorios en Estepona con vistas al mar, spa, piscina interior, skypool y gimnasio, sin fecha de finalización indicada, desde {E2500000} más IVA.',
  '6 appartements et penthouses sur 20, de trois et quatre chambres, à Estepona avec vue sur la mer, spa, piscine intérieure, skypool et salle de sport, date d’achèvement non indiquée, à partir de {E2500000} hors TVA.',
  '6 von 20 Wohnungen und Penthäusern mit drei und vier Schlafzimmern in Estepona mit Meerblick, Spa, Innenpool, Skypool und Fitnessraum, Fertigstellungstermin nicht angegeben, ab {E2500000} zuzüglich MwSt.',
  '6 из 20 апартаментов и пентхаусов с тремя и четырьмя спальнями в Эстепоне: вид на море, спа, крытый бассейн, скайпул и тренажёрный зал, срок завершения не указан, от {E2500000} без НДС.',
  '6 من أصل 20 شقة وبنتهاوس بثلاث وأربع غرف نوم في إستيبونا بإطلالة على البحر، مع سبا ومسبح داخلي ومسبح سكاي وصالة رياضية، دون ذكر موعد الإنجاز، ابتداءً من {E2500000} دون ضريبة القيمة المضافة.',
  '6 van de 20 appartementen en penthouses met drie en vier slaapkamers in Estepona met zeezicht, een spa, een binnenzwembad, een skypool en een fitnessruimte, opleveringsdatum niet vermeld, vanaf {E2500000} excl. btw.',
  '6 z 20 apartamentów i penthouse’ów z trzema i czterema sypialniami w Esteponie z widokiem na morze, spa, basenem wewnętrznym, skypoolem i siłownią, bez podanego terminu ukończenia, od {E2500000} plus VAT.',
  '6 av 20 leiligheter og toppleiligheter med tre og fire soverom i Estepona med utsikt over havet, spa, innendørsbasseng, skypool og treningsrom, ferdigstillelsesdato ikke oppgitt, fra {E2500000} pluss mva.',
  '6 av 20 lägenheter och takvåningar med tre och fyra sovrum i Estepona med havsutsikt, spa, inomhuspool, skypool och gym, färdigställandedatum anges inte, från {E2500000} plus IVA.')

p('.twitterDescription',
  'Apartamentos y áticos de tres y cuatro dormitorios en Estepona con vistas al mar, spa y skypool, desde {E2500000} más IVA.',
  'Appartements et penthouses de trois et quatre chambres à Estepona avec vue sur la mer, spa et skypool, à partir de {E2500000} hors TVA.',
  'Wohnungen und Penthäuser mit drei und vier Schlafzimmern in Estepona mit Meerblick, Spa und Skypool, ab {E2500000} zuzüglich MwSt.',
  'Апартаменты и пентхаусы с тремя и четырьмя спальнями в Эстепоне: вид на море, спа и скайпул, от {E2500000} без НДС.',
  'شقق وبنتهاوس بثلاث وأربع غرف نوم في إستيبونا بإطلالة على البحر، مع سبا ومسبح سكاي، ابتداءً من {E2500000} دون ضريبة القيمة المضافة.',
  'Appartementen en penthouses met drie en vier slaapkamers in Estepona met zeezicht, een spa en een skypool, vanaf {E2500000} excl. btw.',
  'Apartamenty i penthouse’y z trzema i czterema sypialniami w Esteponie z widokiem na morze, spa i skypoolem, od {E2500000} plus VAT.',
  'Leiligheter og toppleiligheter med tre og fire soverom i Estepona med utsikt over havet, spa og skypool, fra {E2500000} pluss mva.',
  'Lägenheter och takvåningar med tre och fyra sovrum i Estepona med havsutsikt, spa och skypool, från {E2500000} plus IVA.')

p('.hero.startingPrice', 'Desde {E2500000} + IVA', 'À partir de {E2500000} + TVA', 'Ab {E2500000} + MwSt.', 'От {E2500000} + НДС',
  'ابتداءً من {E2500000} + ضريبة القيمة المضافة', 'Vanaf {E2500000} + btw', 'Od {E2500000} + VAT', 'Fra {E2500000} + mva.', 'Från {E2500000} + IVA')
p('.card.meta[0][1]', '{E2500000} + IVA', '{E2500000} + TVA', '{E2500000} + MwSt.', '{E2500000} + НДС', '{E2500000} + ضريبة القيمة المضافة',
  '{E2500000} + btw', '{E2500000} + VAT', '{E2500000} + mva.', '{E2500000} + IVA')
p('.availability.priceRange',
  '{E2500000} - {E4800000} + IVA', '{E2500000} - {E4800000} + TVA', '{E2500000} - {E4800000} + MwSt.', '{E2500000} - {E4800000} + НДС',
  '{E2500000} - {E4800000} + ضريبة القيمة المضافة', '{E2500000} - {E4800000} + btw', '{E2500000} - {E4800000} + VAT',
  '{E2500000} - {E4800000} + mva.', '{E2500000} - {E4800000} + IVA')

p('.card.description',
  '6 de 20 apartamentos y áticos de tres y cuatro dormitorios en Estepona, con vistas al mar, spa, piscina interior y skypool.',
  '6 appartements et penthouses sur 20, de trois et quatre chambres, à Estepona, avec vue sur la mer, spa, piscine intérieure et skypool.',
  '6 von 20 Wohnungen und Penthäusern mit drei und vier Schlafzimmern in Estepona, mit Meerblick, Spa, Innenpool und Skypool.',
  '6 из 20 апартаментов и пентхаусов с тремя и четырьмя спальнями в Эстепоне: вид на море, спа, крытый бассейн и скайпул.',
  '6 من أصل 20 شقة وبنتهاوس بثلاث وأربع غرف نوم في إستيبونا، بإطلالة على البحر، مع سبا ومسبح داخلي ومسبح سكاي.',
  '6 van de 20 appartementen en penthouses met drie en vier slaapkamers in Estepona, met zeezicht, een spa, een binnenzwembad en een skypool.',
  '6 z 20 apartamentów i penthouse’ów z trzema i czterema sypialniami w Esteponie, z widokiem na morze, spa, basenem wewnętrznym i skypoolem.',
  '6 av 20 leiligheter og toppleiligheter med tre og fire soverom i Estepona, med utsikt over havet, spa, innendørsbasseng og skypool.',
  '6 av 20 lägenheter och takvåningar med tre och fyra sovrum i Estepona, med havsutsikt, spa, inomhuspool och skypool.')

# ---- image alts and captions ------------------------------------------------------------------------
p('.images.hero.alt',
  'Vista generada por ordenador del edificio en terrazas desde la carretera, con forjados curvos de color arena, barandillas de cristal, vegetación en cada planta y palmeras',
  'Vue générée par ordinateur de l’immeuble en terrasses depuis la route, avec des dalles courbes couleur sable, des garde-corps en verre, de la végétation à chaque niveau et des palmiers',
  'Computergenerierte Ansicht des Terrassengebäudes von der Straße aus, mit geschwungenen sandfarbenen Geschossdecken, Glasbrüstungen, Bepflanzung auf jeder Ebene und Palmen',
  'Компьютерная визуализация здания с террасами со стороны дороги: изогнутые перекрытия песочного цвета, стеклянные ограждения, озеленение на каждом уровне и пальмы',
  'منظر مولَّد بالحاسوب للمبنى المتدرج من جهة الطريق، مع بلاطات منحنية بلون الرمل وحواجز زجاجية ونباتات في كل طابق ونخيل',
  'Computergegenereerd beeld van het terrassengebouw vanaf de weg, met gebogen zandkleurige vloerplaten, glazen balustrades, beplanting op elke verdieping en palmbomen',
  'Wygenerowany komputerowo widok tarasowego budynku od strony drogi, z zaokrąglonymi piaskowymi stropami, szklanymi balustradami, zielenią na każdej kondygnacji i palmami',
  'Datagenerert bilde av terrassebygningen sett fra veien, med buede sandfargede dekker, glassrekkverk, beplantning i hver etasje og palmer',
  'Datorgenererad vy av terrasshuset sett från vägen, med böjda sandfärgade bjälklag, glasräcken, grönska på varje våning och palmer')
p('.images.architecture.alt',
  'Vista generada por ordenador de la fachada al anochecer, con terrazas iluminadas bajo forjados voladizos de color arena y jardineras en cada planta',
  'Vue générée par ordinateur de la façade au crépuscule, avec des terrasses éclairées sous des dalles en porte-à-faux couleur sable et des jardinières à chaque niveau',
  'Computergenerierte Ansicht der Fassade in der Abenddämmerung, mit beleuchteten Terrassen unter auskragenden sandfarbenen Geschossdecken und Pflanzkästen auf jeder Ebene',
  'Компьютерная визуализация фасада в сумерках: освещённые террасы под выступающими перекрытиями песочного цвета и кашпо на каждом уровне',
  'منظر مولَّد بالحاسوب للواجهة عند الغسق، مع تراسات مضاءة تحت بلاطات بارزة بلون الرمل وأحواض نباتات في كل طابق',
  'Computergegenereerd beeld van de gevel bij valavond, met verlichte terrassen onder uitkragende zandkleurige vloerplaten en plantenbakken op elke verdieping',
  'Wygenerowany komputerowo widok fasady o zmierzchu, z oświetlonymi tarasami pod wysuniętymi piaskowymi stropami i donicami na każdej kondygnacji',
  'Datagenerert bilde av fasaden i skumringen, med opplyste terrasser under fremspringende sandfargede dekker og plantekasser i hver etasje',
  'Datorgenererad vy av fasaden i skymningen, med upplysta terrasser under utskjutande sandfärgade bjälklag och planteringslådor på varje våning')
p('.images.lifestyle.alt',
  'Piscina en la azotea generada por ordenador al atardecer, con tumbonas, sombrillas, una barandilla de cristal, palmeras y el mar al fondo',
  'Piscine sur le toit générée par ordinateur au coucher du soleil, avec des bains de soleil, des parasols, un garde-corps en verre, des palmiers et la mer au loin',
  'Computergenerierter Dachpool bei Sonnenuntergang, mit Sonnenliegen, Sonnenschirmen, einer Glasbrüstung, Palmen und dem Meer dahinter',
  'Компьютерная визуализация бассейна на крыше на закате: шезлонги, зонты, стеклянное ограждение, пальмы и море вдали',
  'مسبح على السطح مولَّد بالحاسوب عند الغروب، مع كراسي استلقاء ومظلات وحاجز زجاجي ونخيل والبحر في الأفق',
  'Computergegenereerd zwembad op het dak bij zonsondergang, met ligbedden, parasols, een glazen balustrade, palmbomen en de zee op de achtergrond',
  'Wygenerowany komputerowo basen na dachu o zachodzie słońca, z leżakami, parasolami, szklaną balustradą, palmami i morzem w tle',
  'Datagenerert takbasseng ved solnedgang, med solsenger, parasoller, glassrekkverk, palmer og havet i bakgrunnen',
  'Datorgenererad takpool i solnedgången, med solstolar, parasoller, ett glasräcke, palmer och havet i bakgrunden')
p('.images.privateViewing.alt',
  'Dormitorio principal generado por ordenador con una cama doble, un sofá a los pies y un baño con paredes de cristal con bañera exenta',
  'Chambre principale générée par ordinateur avec un lit double, un canapé au pied du lit et une salle de bains aux parois vitrées avec baignoire îlot',
  'Computergeneriertes Hauptschlafzimmer mit einem Doppelbett, einem Sofa am Fußende und einem verglasten Bad mit freistehender Badewanne',
  'Компьютерная визуализация главной спальни с двуспальной кроватью, диваном в изножье и ванной комнатой со стеклянными стенами и отдельно стоящей ванной',
  'غرفة نوم رئيسية مولَّدة بالحاسوب بسرير مزدوج وأريكة عند أسفله وحمام بجدران زجاجية فيه حوض استحمام قائم بذاته',
  'Computergegenereerde hoofdslaapkamer met een tweepersoonsbed, een bank aan het voeteneinde en een badkamer met glazen wanden en een vrijstaand bad',
  'Wygenerowana komputerowo sypialnia główna z łóżkiem małżeńskim, sofą w nogach łóżka i łazienką ze szklanymi ścianami z wolnostojącą wanną',
  'Datagenerert hovedsoverom med dobbeltseng, en sofa ved fotenden og et baderom med glassvegger og et frittstående badekar',
  'Datorgenererat huvudsovrum med dubbelsäng, en soffa vid fotändan och ett badrum med glasväggar och ett fristående badkar')

p('.media.copy',
  'Vistas generadas por ordenador del edificio, los interiores y las zonas comunes, los planos de las seis viviendas listadas y un plano aéreo de la parcela.',
  'Vues générées par ordinateur de l’immeuble, des intérieurs et des espaces communs, plans des six logements annoncés et plan aérien de la parcelle.',
  'Computergenerierte Ansichten des Gebäudes, der Innenräume und der Gemeinschaftsbereiche, die Grundrisse der sechs gelisteten Wohnungen und ein Luftplan des Grundstücks.',
  'Компьютерные визуализации здания, интерьеров и общих зон, планировки шести объектов из списка и аэроплан участка.',
  'مناظر مولَّدة بالحاسوب للمبنى والداخل والمرافق المشتركة، ومخططات المساكن الستة المدرجة، ومخطط جوي للأرض.',
  'Computergegenereerde beelden van het gebouw, de interieurs en de gemeenschappelijke ruimtes, de plattegronden van de zes aangeboden woningen en een luchtplan van het perceel.',
  'Wizualizacje komputerowe budynku, wnętrz i części wspólnych, rzuty sześciu oferowanych lokali oraz plan lotniczy działki.',
  'Datagenererte bilder av bygningen, interiørene og fellesarealene, plantegningene av de seks oppførte boligene og en luftplan av tomten.',
  'Datorgenererade vyer av byggnaden, interiörerna och de gemensamma ytorna, planritningarna för de sex listade bostäderna och en flygplan över tomten.')
p('.media.note',
  'Todas las imágenes están generadas por ordenador, salvo la vista aérea, que sitúa el edificio generado por ordenador en una fotografía; el mobiliario, la decoración y la vegetación que muestran son ilustrativos y no están incluidos. Los planos son los del promotor, versión del 14 de abril de 2026: no son contractuales y las superficies que indican son aproximadas y están sujetas al proyecto definitivo.',
  'Toutes les images sont générées par ordinateur, à l’exception de la vue aérienne, qui place l’immeuble généré par ordinateur dans une photographie ; le mobilier, la décoration et la végétation qu’elles montrent sont illustratifs et ne sont pas inclus. Les plans sont ceux du promoteur, version du 14 avril 2026 : ils n’ont pas de valeur contractuelle et les surfaces indiquées sont approximatives et soumises au projet définitif.',
  'Alle Bilder sind computergeneriert, mit Ausnahme der Luftaufnahme, die das computergenerierte Gebäude in ein Foto einfügt; Möbel, Dekoration und Bepflanzung darin dienen der Veranschaulichung und sind nicht enthalten. Die Grundrisse sind die des Bauträgers, Stand 14. April 2026: Sie sind nicht vertraglich bindend, und die darin angegebenen Flächen sind ungefähr und stehen unter dem Vorbehalt des endgültigen Projekts.',
  'Все изображения созданы компьютером, кроме аэрофотосъёмки, где компьютерное здание помещено на фотографию; мебель, декор и озеленение на них носят иллюстративный характер и не входят в стоимость. Планировки — застройщика, версия от 14 апреля 2026 года: они не имеют договорной силы, а указанные на них площади приблизительны и зависят от окончательного проекта.',
  'جميع الصور مولَّدة بالحاسوب، باستثناء المنظر الجوي الذي يضع المبنى المولَّد بالحاسوب داخل صورة فوتوغرافية، والأثاث والديكور والنباتات فيها توضيحية وغير مشمولة. المخططات هي مخططات المطوّر، إصدار 14 أبريل 2026: ليست تعاقدية، والمساحات المبيّنة عليها تقريبية وخاضعة للمشروع النهائي.',
  'Alle beelden zijn computergegenereerd, behalve het luchtbeeld, dat het computergegenereerde gebouw in een foto plaatst; het meubilair, de decoratie en de beplanting daarop zijn illustratief en niet inbegrepen. De plattegronden zijn die van de ontwikkelaar, versie van 14 april 2026: ze zijn niet contractueel en de oppervlakten erop zijn bij benadering en onder voorbehoud van het definitieve project.',
  'Wszystkie obrazy są wygenerowane komputerowo, z wyjątkiem widoku z lotu ptaka, który umieszcza komputerowo wygenerowany budynek na fotografii; meble, wystrój i roślinność na nich mają charakter poglądowy i nie są wliczone. Rzuty są rzutami dewelopera, wersja z 14 kwietnia 2026 r.: nie mają mocy umownej, a podane na nich powierzchnie są przybliżone i zależą od ostatecznego projektu.',
  'Alle bilder er datagenererte, bortsett fra flyfotoet, som plasserer den datagenererte bygningen i et fotografi; møbler, dekor og beplantning på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens, versjon av 14. april 2026: de er ikke kontraktsfestet, og arealene på dem er omtrentlige og med forbehold om det endelige prosjektet.',
  'Alla bilder är datorgenererade, utom flygvyn som placerar den datorgenererade byggnaden i ett fotografi; möbler, inredning och planteringar i dem är illustrativa och ingår inte. Planritningarna är exploatörens, version av den 14 april 2026: de är inte avtalsbundna och ytorna på dem är ungefärliga och med förbehåll för det slutliga projektet.')

p('.media.items[1].caption', 'La fachada al anochecer', 'La façade au crépuscule', 'Die Fassade in der Abenddämmerung', 'Фасад в сумерках', 'الواجهة عند الغسق',
  'De gevel bij valavond', 'Fasada o zmierzchu', 'Fasaden i skumringen', 'Fasaden i skymningen')
p('.media.items[2].alt',
  'Vista generada por ordenador del edificio desde un camino de grava entre palmeras, con arbustos en flor y césped',
  'Vue générée par ordinateur de l’immeuble depuis un chemin de gravier entre des palmiers, avec des arbustes en fleurs et de la pelouse',
  'Computergenerierte Ansicht des Gebäudes von einem Kiesweg zwischen Palmen aus, mit blühenden Sträuchern und Rasen',
  'Компьютерная визуализация здания с гравийной дорожки между пальмами: цветущие кустарники и газон',
  'منظر مولَّد بالحاسوب للمبنى من ممر حصوي بين النخيل، مع شجيرات مزهرة ومرج',
  'Computergegenereerd beeld van het gebouw vanaf een grindpad tussen palmbomen, met bloeiende struiken en gazon',
  'Wygenerowany komputerowo widok budynku od strony żwirowej ścieżki między palmami, z kwitnącymi krzewami i trawnikiem',
  'Datagenerert bilde av bygningen sett fra en grussti mellom palmer, med blomstrende busker og plen',
  'Datorgenererad vy av byggnaden från en grusgång mellan palmer, med blommande buskar och gräsmatta')
p('.media.items[2].caption', 'La llegada a través de los jardines', 'L’arrivée à travers les jardins', 'Die Zufahrt durch die Gärten', 'Подход через сады', 'الوصول عبر الحدائق',
  'De aanloop door de tuinen', 'Dojście przez ogrody', 'Tilkomsten gjennom hagene', 'Ankomsten genom trädgårdarna')
p('.media.items[3].alt',
  'Vista generada por ordenador de la explanada de entrada con un patio pavimentado, un elemento de agua, palmeras y el edificio en terrazas al fondo',
  'Vue générée par ordinateur du parvis d’entrée avec une cour dallée, un bassin, des palmiers et l’immeuble en terrasses en arrière-plan',
  'Computergenerierte Ansicht des Eingangsbereichs mit einem gepflasterten Hof, einem Wasserelement, Palmen und dem Terrassengebäude dahinter',
  'Компьютерная визуализация входной площади с мощёным двором, водным элементом, пальмами и зданием с террасами позади',
  'منظر مولَّد بالحاسوب لباحة المدخل بفناء مبلّط وعنصر مائي ونخيل والمبنى المتدرج خلفها',
  'Computergegenereerd beeld van het entreeplein met een bestraat plein, een waterpartij, palmbomen en het terrassengebouw erachter',
  'Wygenerowany komputerowo widok placu wejściowego z brukowanym dziedzińcem, elementem wodnym, palmami i tarasowym budynkiem w tle',
  'Datagenerert bilde av inngangsplassen med en brolagt gårdsplass, et vannelement, palmer og terrassebygningen bak',
  'Datorgenererad vy av entréplanen med en stensatt gård, ett vattenelement, palmer och terrasshuset bakom')
p('.media.items[3].caption', 'La explanada de entrada', 'Le parvis d’entrée', 'Der Eingangsbereich', 'Входная площадь', 'باحة المدخل',
  'Het entreeplein', 'Plac wejściowy', 'Inngangsplassen', 'Entréplanen')
p('.media.items[4].alt',
  'Fotografía aérea de la costa de Estepona, con el edificio generado por ordenador situado en la parcela, la playa y la ciudad al fondo y el mar a la izquierda',
  'Photographie aérienne de la côte d’Estepona, avec l’immeuble généré par ordinateur placé sur la parcelle, la plage et la ville au loin et la mer à gauche',
  'Luftaufnahme der Küste von Estepona, mit dem computergenerierten Gebäude auf dem Grundstück, dem Strand und der Stadt dahinter und dem Meer links',
  'Аэрофотография побережья Эстепоны: компьютерное здание помещено на участок, вдали пляж и город, слева море',
  'صورة جوية لساحل إستيبونا، مع المبنى المولَّد بالحاسوب موضوعاً على الأرض، والشاطئ والمدينة في الخلفية والبحر إلى اليسار',
  'Luchtfoto van de kust van Estepona, met het computergegenereerde gebouw op het perceel geplaatst, het strand en de stad erachter en de zee links',
  'Zdjęcie lotnicze wybrzeża Estepony z komputerowo wygenerowanym budynkiem umieszczonym na działce, plażą i miastem w tle oraz morzem po lewej',
  'Flyfoto av kysten ved Estepona, med den datagenererte bygningen plassert på tomten, stranden og byen bak og havet til venstre',
  'Flygfoto över kusten vid Estepona, med den datorgenererade byggnaden placerad på tomten, stranden och staden bakom och havet till vänster')
p('.media.items[4].caption', 'La parcela en la costa de Estepona', 'La parcelle sur la côte d’Estepona', 'Das Grundstück an der Küste von Estepona', 'Участок на побережье Эстепоны', 'الأرض على ساحل إستيبونا',
  'Het perceel aan de kust van Estepona', 'Działka na wybrzeżu Estepony', 'Tomten på kysten ved Estepona', 'Tomten på kusten vid Estepona')
p('.media.items[5].alt',
  'Salón-comedor generado por ordenador con un sofá curvo, ventanales de suelo a techo y vistas a las montañas',
  'Séjour et salle à manger générés par ordinateur avec un canapé courbe, des baies vitrées du sol au plafond et une vue sur les montagnes',
  'Computergeneriertes Wohn- und Esszimmer mit einem geschwungenen Sofa, raumhohen Fenstern und Blick auf die Berge',
  'Компьютерная визуализация гостиной со столовой: изогнутый диван, панорамные окна от пола до потолка и вид на горы',
  'غرفة معيشة وطعام مولَّدة بالحاسوب بأريكة منحنية ونوافذ من الأرض إلى السقف وإطلالة على الجبال',
  'Computergegenereerde woon- en eetkamer met een gebogen bank, vloerhoge ramen en uitzicht op de bergen',
  'Wygenerowany komputerowo salon z jadalnią, z zakrzywioną sofą, oknami od podłogi do sufitu i widokiem na góry',
  'Datagenerert stue og spisestue med en buet sofa, vinduer fra gulv til tak og utsikt over fjellene',
  'Datorgenererat vardagsrum med matplats, med en böjd soffa, fönster från golv till tak och utsikt över bergen')
p('.media.items[5].caption', 'Salón con vistas a la montaña', 'Séjour avec vue sur la montagne', 'Wohnzimmer mit Bergblick', 'Гостиная с видом на горы', 'غرفة المعيشة بإطلالة جبلية',
  'Woonkamer met uitzicht op de bergen', 'Salon z widokiem na góry', 'Stue med utsikt over fjellene', 'Vardagsrum med bergsutsikt')
p('.media.items[6].alt',
  'Salón-comedor amplio generado por ordenador con una pared de bloques de vidrio, una mesa con sillas de director, un sofá y una pared de televisión',
  'Grand séjour et salle à manger générés par ordinateur avec un mur en briques de verre, une table avec des chaises de réalisateur, un canapé et un mur télévision',
  'Computergeneriertes weitläufiges Wohn- und Esszimmer mit einer Glasbausteinwand, einem Tisch mit Regiestühlen, einem Sofa und einer Fernsehwand',
  'Компьютерная визуализация просторной гостиной со столовой: стена из стеклоблоков, стол со складными стульями, диван и стена с телевизором',
  'غرفة معيشة وطعام واسعة مولَّدة بالحاسوب بجدار من كتل الزجاج وطاولة بكراسي المخرج وأريكة وجدار للتلفزيون',
  'Computergegenereerde ruime woon- en eetkamer met een wand van glasbouwstenen, een tafel met regisseursstoelen, een bank en een televisiewand',
  'Wygenerowany komputerowo przestronny salon z jadalnią, ze ścianą z luksferów, stołem z krzesłami reżyserskimi, sofą i ścianą telewizyjną',
  'Datagenerert romslig stue og spisestue med en vegg av glassblokker, et bord med regissørstoler, en sofa og en TV-vegg',
  'Datorgenererat rymligt vardagsrum med matplats, med en vägg av glasbetong, ett bord med regissörsstolar, en soffa och en tv-vägg')
p('.media.items[7].alt',
  'Cocina generada por ordenador con una isla de piedra y dos taburetes, armarios de chapa de madera, un estante iluminado y el mar visible por una ventana',
  'Cuisine générée par ordinateur avec un îlot en pierre et deux tabourets, des meubles en placage bois, une étagère éclairée et la mer visible par une fenêtre',
  'Computergenerierte Küche mit einer Steininsel und zwei Hockern, Holzfurnierschränken, einem beleuchteten Regal und dem Meer, das durch ein Fenster zu sehen ist',
  'Компьютерная визуализация кухни с каменным островом и двумя барными стульями, шкафами из шпона, подсвеченной полкой и видом на море из окна',
  'مطبخ مولَّد بالحاسوب بجزيرة حجرية ومقعدين عاليين وخزائن من القشرة الخشبية ورف مضاء والبحر ظاهر من نافذة',
  'Computergegenereerde keuken met een stenen eiland en twee krukken, kasten met houtfineer, een verlicht plankje en de zee zichtbaar door een raam',
  'Wygenerowana komputerowo kuchnia z kamienną wyspą i dwoma stołkami, szafkami we fornirze, podświetloną półką i morzem widocznym przez okno',
  'Datagenerert kjøkken med en steinøy og to krakker, skap i trefiner, en opplyst hylle og havet synlig gjennom et vindu',
  'Datorgenererat kök med en stenö och två barstolar, skåp i träfaner, en upplyst hylla och havet synligt genom ett fönster')
p('.media.items[8].alt',
  'Vestíbulo de entrada circular generado por ordenador con dos sofás curvos, lamas verticales de madera, cortinas y una puerta de cristal al jardín',
  'Hall d’entrée circulaire généré par ordinateur avec deux canapés courbes, des lames de bois verticales, des rideaux et une porte vitrée donnant sur le jardin',
  'Computergenerierte runde Eingangshalle mit zwei geschwungenen Sofas, senkrechten Holzlamellen, Vorhängen und einer Glastür zum Garten',
  'Компьютерная визуализация круглого входного холла с двумя изогнутыми диванами, вертикальными деревянными рейками, шторами и стеклянной дверью в сад',
  'ردهة مدخل دائرية مولَّدة بالحاسوب بأريكتين منحنيتين وشرائح خشبية رأسية وستائر وباب زجاجي إلى الحديقة',
  'Computergegenereerde ronde inkomhal met twee gebogen banken, verticale houten lamellen, gordijnen en een glazen deur naar de tuin',
  'Wygenerowany komputerowo okrągły hol wejściowy z dwiema zakrzywionymi sofami, pionowymi drewnianymi listwami, zasłonami i szklanymi drzwiami do ogrodu',
  'Datagenerert rund inngangshall med to buede sofaer, vertikale trelameller, gardiner og en glassdør til hagen',
  'Datorgenererad rund entréhall med två böjda soffor, vertikala träribbor, gardiner och en glasdörr till trädgården')
p('.media.items[8].caption', 'El vestíbulo de entrada', 'Le hall d’entrée', 'Die Eingangshalle', 'Входной холл', 'ردهة المدخل',
  'De inkomhal', 'Hol wejściowy', 'Inngangshallen', 'Entréhallen')
p('.media.items[9].alt',
  'Dormitorio principal generado por ordenador con una cama doble baja, un tocador con espejo redondo y armarios con puertas de cristal',
  'Chambre principale générée par ordinateur avec un lit double bas, une coiffeuse avec un miroir rond et des armoires vitrées',
  'Computergeneriertes Hauptschlafzimmer mit einem niedrigen Doppelbett, einem Schminktisch mit rundem Spiegel und Kleiderschränken mit Glastüren',
  'Компьютерная визуализация главной спальни с низкой двуспальной кроватью, туалетным столиком с круглым зеркалом и шкафами со стеклянными дверцами',
  'غرفة نوم رئيسية مولَّدة بالحاسوب بسرير مزدوج منخفض وطاولة زينة بمرآة مستديرة وخزائن بأبواب زجاجية',
  'Computergegenereerde hoofdslaapkamer met een laag tweepersoonsbed, een kaptafel met een ronde spiegel en kasten met glazen deuren',
  'Wygenerowana komputerowo sypialnia główna z niskim łóżkiem małżeńskim, toaletką z okrągłym lustrem i szafami ze szklanymi drzwiami',
  'Datagenerert hovedsoverom med en lav dobbeltseng, en sminkebord med rundt speil og skap med glassdører',
  'Datorgenererat huvudsovrum med en låg dubbelsäng, ett sminkbord med rund spegel och garderober med glasdörrar')
p('.media.items[10].caption', 'Dormitorio principal y baño', 'Chambre principale et salle de bains', 'Hauptschlafzimmer und Bad', 'Главная спальня и ванная комната', 'غرفة النوم الرئيسية والحمام',
  'Hoofdslaapkamer en badkamer', 'Sypialnia główna i łazienka', 'Hovedsoverom og bad', 'Huvudsovrum och badrum')
p('.media.items[11].alt',
  'Aseo de cortesía generado por ordenador con un lavabo de piedra suspendido, un espejo, apliques y un inodoro suspendido',
  'Toilettes d’invités générées par ordinateur avec une vasque en pierre suspendue, un miroir, des appliques et des WC suspendus',
  'Computergeneriertes Gäste-WC mit einem schwebenden Steinwaschbecken, einem Spiegel, Wandleuchten und einem Wand-WC',
  'Компьютерная визуализация гостевого санузла с подвесной каменной раковиной, зеркалом, настенными светильниками и подвесным унитазом',
  'دورة مياه للضيوف مولَّدة بالحاسوب بحوض حجري معلّق ومرآة ومصابيح جدارية ومرحاض معلّق',
  'Computergegenereerd gastentoilet met een zwevende stenen wastafel, een spiegel, wandlampen en een hangend toilet',
  'Wygenerowana komputerowo toaleta dla gości z wiszącą kamienną umywalką, lustrem, kinkietami i wiszącą miską ustępową',
  'Datagenerert gjestetoalett med en svevende stenvask, et speil, vegglamper og et veggmontert toalett',
  'Datorgenererad gästtoalett med ett svävande stenhandfat, en spegel, vägglampor och en vägghängd toalett')
p('.media.items[11].caption', 'Aseo de cortesía', 'Toilettes d’invités', 'Gäste-WC', 'Гостевой санузел', 'دورة مياه الضيوف',
  'Gastentoilet', 'Toaleta dla gości', 'Gjestetoalett', 'Gästtoalett')
p('.media.items[12].alt',
  'Terraza cubierta generada por ordenador con sillones y sofás, una mesa de comedor tras la vegetación y vistas al mar a la derecha',
  'Terrasse couverte générée par ordinateur avec des fauteuils et des canapés, une table à manger derrière la végétation et une vue sur la mer à droite',
  'Computergenerierte überdachte Terrasse mit Sesseln und Sofas, einem Esstisch hinter der Bepflanzung und Meerblick rechts',
  'Компьютерная визуализация крытой террасы с креслами и диванами, обеденным столом за зеленью и видом на море справа',
  'تراس مغطى مولَّد بالحاسوب بمقاعد وأرائك وطاولة طعام خلف النباتات وإطلالة على البحر إلى اليمين',
  'Computergegenereerd overdekt terras met fauteuils en banken, een eettafel achter de beplanting en zicht op zee rechts',
  'Wygenerowany komputerowo zadaszony taras z fotelami i sofami, stołem jadalnym za roślinnością i widokiem na morze po prawej',
  'Datagenerert overbygd terrasse med lenestoler og sofaer, et spisebord bak beplantningen og utsikt over havet til høyre',
  'Datorgenererad övertäckt terrass med fåtöljer och soffor, ett matbord bakom växtligheten och havsutsikt till höger')
p('.media.items[13].alt',
  'Terraza en la azotea generada por ordenador con asientos de salón y una barra entre palmeras, con montañas a lo lejos',
  'Toit-terrasse généré par ordinateur avec des assises de salon et un comptoir de bar parmi les palmiers, avec des montagnes au loin',
  'Computergenerierte Dachterrasse mit Loungemöbeln und einer Bartheke zwischen Palmen, mit Bergen in der Ferne',
  'Компьютерная визуализация террасы на крыше с лаунж-мебелью и барной стойкой среди пальм, вдали горы',
  'تراس على السطح مولَّد بالحاسوب بمقاعد جلوس وبار بين النخيل وجبال في البعيد',
  'Computergegenereerd dakterras met loungemeubilair en een bar tussen palmbomen, met bergen in de verte',
  'Wygenerowany komputerowo taras na dachu z meblami wypoczynkowymi i barem wśród palm, z górami w oddali',
  'Datagenerert takterrasse med loungemøbler og en bardisk blant palmer, med fjell i det fjerne',
  'Datorgenererad takterrass med loungemöbler och en bardisk bland palmer, med berg i fjärran')
p('.media.items[13].caption', 'El salón de la azotea', 'Le salon sur le toit', 'Die Dachlounge', 'Лаунж на крыше', 'صالة السطح',
  'De lounge op het dak', 'Lounge na dachu', 'Loungen på taket', 'Loungen på taket')
p('.media.items[14].alt',
  'Solárium en la azotea generado por ordenador con tumbonas, sombrillas y una cama balinesa con cortinas, con una piscina al fondo y colinas a lo lejos',
  'Solarium sur le toit généré par ordinateur avec des bains de soleil, des parasols et un lit de repos à rideaux, avec une piscine au fond et des collines au loin',
  'Computergeneriertes Dachsolarium mit Sonnenliegen, Sonnenschirmen und einer Tagesliege mit Vorhängen, mit einem Pool dahinter und Hügeln in der Ferne',
  'Компьютерная визуализация солярия на крыше с шезлонгами, зонтами и кушеткой с занавесками, вдали бассейн и холмы',
  'سولاريوم على السطح مولَّد بالحاسوب بكراسي استلقاء ومظلات وسرير نهاري بستائر ومسبح في الخلفية وتلال في البعيد',
  'Computergegenereerd daksolarium met ligbedden, parasols en een daybed met gordijnen, met een zwembad erachter en heuvels in de verte',
  'Wygenerowane komputerowo solarium na dachu z leżakami, parasolami i łóżkiem wypoczynkowym z zasłonami, z basenem w tle i wzgórzami w oddali',
  'Datagenerert solterrasse på taket med solsenger, parasoller og en daybed med gardiner, med et basseng bak og åser i det fjerne',
  'Datorgenererad solterrass på taket med solstolar, parasoller och en dagbädd med gardiner, med en pool bakom och kullar i fjärran')
p('.media.items[14].caption', 'El solárium de la azotea', 'Le solarium sur le toit', 'Das Dachsolarium', 'Солярий на крыше', 'سولاريوم السطح',
  'Het daksolarium', 'Solarium na dachu', 'Solterrassen på taket', 'Solterrassen på taket')
p('.media.items[15].alt',
  'Terraza en la azotea generada por ordenador con un gran sofá en esquina, pufs y vegetación, y una zona de estar cubierta al fondo',
  'Toit-terrasse généré par ordinateur avec un grand canapé d’angle, des poufs et de la végétation, et un espace de vie couvert à l’arrière',
  'Computergenerierte Dachterrasse mit einem großen Ecksofa, Poufs und Bepflanzung und einem überdachten Wohnbereich dahinter',
  'Компьютерная визуализация террасы на крыше с большим угловым диваном, пуфами и зеленью, позади крытая жилая зона',
  'تراس على السطح مولَّد بالحاسوب بأريكة ركنية كبيرة ومقاعد وسادية ونباتات ومنطقة جلوس مغطاة في الخلف',
  'Computergegenereerd dakterras met een grote hoekbank, poefs en beplanting, en een overdekte woonruimte erachter',
  'Wygenerowany komputerowo taras na dachu z dużą sofą narożną, pufami i roślinnością oraz zadaszoną strefą dzienną w tle',
  'Datagenerert takterrasse med en stor hjørnesofa, puffer og beplantning, og et overbygd oppholdsrom bak',
  'Datorgenererad takterrass med en stor hörnsoffa, sittpuffar och växtlighet, och en övertäckt vardagsyta bakom')
p('.media.items[15].caption', 'Una terraza en la azotea con zona de estar', 'Une terrasse sur le toit avec un coin salon', 'Eine Dachterrasse mit Sitzbereich', 'Терраса на крыше с зоной отдыха', 'تراس على السطح مع منطقة جلوس',
  'Een dakterras met zithoek', 'Taras na dachu ze strefą wypoczynku', 'En takterrasse med sittegruppe', 'En takterrass med sittgrupp')
p('.media.items[16].caption', 'La skypool al atardecer', 'La skypool au coucher du soleil', 'Der Skypool bei Sonnenuntergang', 'Скайпул на закате', 'مسبح السكاي عند الغروب',
  'De skypool bij zonsondergang', 'Skypool o zachodzie słońca', 'Skypoolen ved solnedgang', 'Skypoolen i solnedgången')
p('.media.items[17].alt',
  'Spa interior generado por ordenador con una piscina climatizada, jacuzzis redondos bajo claraboyas, tumbonas y farolillos',
  'Spa intérieur généré par ordinateur avec une piscine chauffée, des bains à remous ronds sous des verrières, des chaises longues et des lanternes',
  'Computergeneriertes Innen-Spa mit einem beheizten Pool, runden Whirlpools unter Oberlichtern, Liegen und Laternen',
  'Компьютерная визуализация крытого спа с подогреваемым бассейном, круглыми джакузи под световыми фонарями, шезлонгами и фонарями',
  'سبا داخلي مولَّد بالحاسوب بمسبح مدفأ وأحواض جاكوزي مستديرة تحت فتحات سقفية وكراسي استلقاء وفوانيس',
  'Computergegenereerde binnenspa met een verwarmd zwembad, ronde bubbelbaden onder dakramen, ligbedden en lantaarns',
  'Wygenerowane komputerowo wnętrze spa z podgrzewanym basenem, okrągłymi jacuzzi pod świetlikami, leżakami i latarniami',
  'Datagenerert innendørs spa med et oppvarmet basseng, runde boblebad under takvinduer, solsenger og lykter',
  'Datorgenererat inomhusspa med en uppvärmd pool, runda bubbelpooler under takfönster, solstolar och lyktor')
p('.media.items[17].caption', 'El spa y la piscina interior', 'Le spa et la piscine intérieure', 'Das Spa und der Innenpool', 'Спа и крытый бассейн', 'السبا والمسبح الداخلي',
  'De spa en het binnenzwembad', 'Spa i basen wewnętrzny', 'Spaen og innendørsbassenget', 'Spat och inomhuspoolen')
p('.media.items[18].alt',
  'Gimnasio generado por ordenador con máquinas de fuerza y cardio, espejos, columnas revestidas de azul y un patio ajardinado al lado',
  'Salle de sport générée par ordinateur avec des appareils de musculation et de cardio, des miroirs, des colonnes revêtues de bleu et une cour paysagère à côté',
  'Computergenerierter Fitnessraum mit Kraft- und Cardiogeräten, Spiegeln, blau verkleideten Säulen und einem begrünten Hof daneben',
  'Компьютерная визуализация тренажёрного зала с силовыми и кардиотренажёрами, зеркалами, колоннами с синей облицовкой и озеленённым двориком рядом',
  'صالة رياضية مولَّدة بالحاسوب بأجهزة قوة وكارديو ومرايا وأعمدة مكسوة بالأزرق وفناء مزروع بجانبها',
  'Computergegenereerde fitnessruimte met kracht- en cardiotoestellen, spiegels, blauw betegelde zuilen en een tuinpatio ernaast',
  'Wygenerowana komputerowo siłownia z maszynami siłowymi i do cardio, lustrami, kolumnami wyłożonymi niebieską okładziną i zielonym patio obok',
  'Datagenerert treningsrom med styrke- og kondisjonsapparater, speil, søyler kledd i blått og en grønn gårdsplass ved siden av',
  'Datorgenererat gym med styrke- och konditionsmaskiner, speglar, blåklädda pelare och en grön innergård bredvid')
p('.media.items[19].alt',
  'Sala de masajes generada por ordenador con dos camillas y una pared con un dibujo de hierbas',
  'Salle de massage générée par ordinateur avec deux tables de soin et un mur au motif d’herbes',
  'Computergeneriertes Massagezimmer mit zwei Behandlungsliegen und einer Wand mit Gräsermotiv',
  'Компьютерная визуализация массажного кабинета с двумя массажными столами и стеной с рисунком из трав',
  'غرفة مساج مولَّدة بالحاسوب بسريرين للعلاج وجدار بنقش أعشاب',
  'Computergegenereerde massageruimte met twee behandeltafels en een wand met een grassenpatroon',
  'Wygenerowany komputerowo gabinet masażu z dwoma stołami i ścianą z motywem traw',
  'Datagenerert massasjerom med to behandlingsbenker og en vegg med gressmønster',
  'Datorgenererat massagerum med två behandlingsbänkar och en vägg med gräsmönster')
p('.media.items[19].caption', 'Una sala de masajes', 'Une salle de massage', 'Ein Massageraum', 'Массажный кабинет', 'غرفة مساج',
  'Een massageruimte', 'Gabinet masażu', 'Et massasjerom', 'Ett massagerum')
p('.media.items[26].alt',
  'Plano aéreo ilustrado de la parcela junto a la carretera costera, con el edificio señalado, la entrada y la rotonda, y el mar y la playa debajo',
  'Plan aérien illustré de la parcelle à côté de la route côtière, avec l’immeuble entouré, l’entrée et le rond-point, et la mer et la plage en dessous',
  'Illustrierter Luftplan des Grundstücks neben der Küstenstraße, mit dem umrandeten Gebäude, dem Eingang und dem Kreisverkehr sowie dem Meer und dem Strand darunter',
  'Иллюстрированный аэроплан участка рядом с прибрежной дорогой: здание обведено, показаны въезд и кольцевая развязка, внизу море и пляж',
  'مخطط جوي مصوَّر للأرض بجانب الطريق الساحلي، مع المبنى محدداً والمدخل والدوّار، والبحر والشاطئ في الأسفل',
  'Geïllustreerd luchtplan van het perceel naast de kustweg, met het omlijnde gebouw, de ingang en de rotonde, en de zee en het strand eronder',
  'Ilustrowany plan lotniczy działki przy drodze nadmorskiej, z zaznaczonym budynkiem, wjazdem i rondem oraz morzem i plażą poniżej',
  'Illustrert luftplan av tomten ved kystveien, med bygningen markert, inngangen og rundkjøringen, og havet og stranden nedenfor',
  'Illustrerad flygplan över tomten vid kustvägen, med byggnaden markerad, entrén och rondellen, och havet och stranden nedanför')

# ---- overview, why, architecture -----------------------------------------------------------------
p('.overview.headlineHtml', 'Veinte viviendas, <em>seis disponibles</em>', 'Vingt logements, <em>six disponibles</em>', 'Zwanzig Wohnungen, <em>sechs verfügbar</em>',
  'Двадцать квартир, <em>шесть доступны</em>', 'عشرون مسكناً، <em>ستة متاحة</em>', 'Twintig woningen, <em>zes beschikbaar</em>', 'Dwadzieścia lokali, <em>sześć dostępnych</em>',
  'Tjue boliger, <em>seks ledige</em>', 'Tjugo bostäder, <em>sex lediga</em>')
p('.overview.copy[0]',
  'Nacare es un edificio de 20 apartamentos y áticos de tres y cuatro dormitorios en Estepona, con vistas al mar y a la montaña. El folleto describe viviendas orientadas al sur con ventilación cruzada, distribuciones abiertas y terrazas generosas. Hay seis viviendas listadas como disponibles: cinco apartamentos en la primera planta y un ático.',
  'Nacare est un immeuble de 20 appartements et penthouses de trois et quatre chambres à Estepona, avec vue sur la mer et la montagne. La brochure décrit des logements orientés au sud avec ventilation traversante, des plans ouverts et de généreuses terrasses. Six logements sont annoncés comme disponibles : cinq appartements au premier étage et un penthouse.',
  'Nacare ist ein Gebäude mit 20 Wohnungen und Penthäusern mit drei und vier Schlafzimmern in Estepona, mit Blick auf das Meer und die Berge. Die Broschüre beschreibt nach Süden ausgerichtete Wohnungen mit Querlüftung, offene Grundrisse und großzügige Terrassen. Sechs Wohnungen sind als verfügbar gelistet: fünf Wohnungen im ersten Obergeschoss und ein Penthouse.',
  'Nacare — здание с 20 апартаментами и пентхаусами с тремя и четырьмя спальнями в Эстепоне, с видом на море и горы. В брошюре описаны квартиры с южной ориентацией и сквозным проветриванием, открытой планировкой и просторными террасами. Шесть объектов указаны как доступные: пять апартаментов на втором этаже и один пентхаус.',
  'Nacare مبنى من 20 شقة وبنتهاوس بثلاث وأربع غرف نوم في إستيبونا، بإطلالة على البحر والجبال. يصف الكتيّب مساكن متجهة نحو الجنوب مع تهوية متقاطعة وتصاميم مفتوحة وتراسات واسعة. ستة مساكن مدرجة على أنها متاحة: خمس شقق في الطابق الأول وبنتهاوس واحد.',
  'Nacare is een gebouw met 20 appartementen en penthouses met drie en vier slaapkamers in Estepona, met uitzicht op de zee en de bergen. De brochure beschrijft op het zuiden gerichte woningen met doorstroomventilatie, open indelingen en royale terrassen. Zes woningen staan vermeld als beschikbaar: vijf appartementen op de eerste verdieping en één penthouse.',
  'Nacare to budynek z 20 apartamentami i penthouse’ami z trzema i czterema sypialniami w Esteponie, z widokiem na morze i góry. Broszura opisuje lokale o południowej ekspozycji ze skrośnym przewietrzaniem, otwarte układy i duże tarasy. Sześć lokali jest wymienionych jako dostępne: pięć apartamentów na pierwszym piętrze i jeden penthouse.',
  'Nacare er et bygg med 20 leiligheter og toppleiligheter med tre og fire soverom i Estepona, med utsikt over havet og fjellene. Brosjyren beskriver sørvendte boliger med gjennomlufting, åpne planløsninger og romslige terrasser. Seks boliger er oppført som ledige: fem leiligheter i andre etasje og én toppleilighet.',
  'Nacare är en byggnad med 20 lägenheter och takvåningar med tre och fyra sovrum i Estepona, med utsikt över havet och bergen. Broschyren beskriver söderläge, genomluftning, öppna planlösningar och generösa terrasser. Sex bostäder är listade som lediga: fem lägenheter på första våningen och en takvåning.')
p('.overview.copy[1]',
  'Las zonas comunes incluyen un spa con piscina interior climatizada, un gimnasio, un salón y bar para propietarios, y una skypool con salón en la azotea, junto con un club de propietarios y una lista de servicios. La ficha del promotor indica que la licencia de obras y la licencia de primera ocupación están pendientes y que el inicio y el fin de la construcción están por confirmar.',
  'Les espaces communs comprennent un spa avec piscine intérieure chauffée, une salle de sport, un salon et un bar pour les propriétaires, et une skypool avec un salon sur le toit, ainsi qu’un club des propriétaires et une liste de services. La fiche du promoteur indique que le permis de construire et la licence de première occupation sont en attente et que le début et la fin des travaux restent à confirmer.',
  'Zu den Gemeinschaftsbereichen gehören ein Spa mit beheiztem Innenpool, ein Fitnessraum, eine Lounge mit Bar für die Eigentümer und ein Skypool mit Dachlounge, dazu ein Eigentümerclub und eine Liste von Serviceleistungen. Laut Datenblatt des Bauträgers stehen die Baugenehmigung und die Erstbezugsgenehmigung noch aus, und Baubeginn und Bauende sind noch zu bestätigen.',
  'Общие зоны включают спа с подогреваемым крытым бассейном, тренажёрный зал, лаунж с баром для владельцев и скайпул с лаунжем на крыше, а также клуб владельцев и список услуг. В справке застройщика указано, что разрешение на строительство и лицензия на первое заселение ещё ожидаются, а начало и окончание строительства предстоит уточнить.',
  'تشمل المرافق المشتركة سباً ومسبحاً داخلياً مدفأً وصالة رياضية وصالة وبار للملاك ومسبح سكاي مع صالة على السطح، إلى جانب نادٍ للملاك وقائمة بالخدمات. وتذكر ورقة المطوّر أن رخصة البناء ورخصة الإشغال الأول قيد الانتظار وأن بدء البناء وانتهاءه لم يتحددا بعد.',
  'Tot de gemeenschappelijke ruimtes behoren een spa met verwarmd binnenzwembad, een fitnessruimte, een lounge met bar voor de eigenaren en een skypool met een lounge op het dak, plus een eigenarenclub en een lijst met diensten. Het informatieblad van de ontwikkelaar vermeldt dat de bouwvergunning en de vergunning voor eerste ingebruikname nog in afwachting zijn en dat de start en het einde van de bouw nog bevestigd moeten worden.',
  'Do części wspólnych należą spa z podgrzewanym basenem wewnętrznym, siłownia, salon z barem dla właścicieli oraz skypool z lounge’em na dachu, a także klub właścicieli i lista usług. Arkusz dewelopera podaje, że pozwolenie na budowę i pozwolenie na pierwsze zasiedlenie są w toku, a rozpoczęcie i zakończenie budowy mają zostać potwierdzone.',
  'Fellesarealene omfatter et spa med oppvarmet innendørsbasseng, et treningsrom, en lounge med bar for eierne og en skypool med lounge på taket, sammen med en eierklubb og en liste over tjenester. Utbyggerens ark oppgir at byggetillatelsen og brukstillatelsen ikke er på plass ennå, og at start og slutt for byggingen skal bekreftes.',
  'De gemensamma ytorna omfattar ett spa med uppvärmd inomhuspool, ett gym, en lounge med bar för ägarna och en skypool med lounge på taket, tillsammans med en ägarklubb och en lista över tjänster. Exploatörens blad anger att bygglovet och tillståndet för första ibruktagande ännu inte har beviljats och att byggstart och byggslut ska bekräftas.')
p('.overview.metrics[0][1]', '20 viviendas', '20 logements', '20 Wohnungen', '20 квартир', '20 مسكناً', '20 woningen', '20 lokali', '20 boliger', '20 bostäder')
p('.why.copy',
  'Viviendas grandes con vistas al mar, grandes terrazas y un spa y una skypool en el edificio.',
  'De grands logements avec vue sur la mer, de vastes terrasses, un spa et une skypool dans l’immeuble.',
  'Große Wohnungen mit Meerblick, großen Terrassen sowie einem Spa und einem Skypool im Gebäude.',
  'Просторные квартиры с видом на море, большими террасами, а также спа и скайпулом в здании.',
  'مساكن واسعة بإطلالة على البحر وتراسات كبيرة وسبا ومسبح سكاي داخل المبنى.',
  'Grote woningen met zeezicht, grote terrassen en een spa en een skypool in het gebouw.',
  'Duże lokale z widokiem na morze, dużymi tarasami oraz spa i skypoolem w budynku.',
  'Store boliger med utsikt over havet, store terrasser og et spa og en skypool i bygningen.',
  'Stora bostäder med havsutsikt, stora terrasser samt ett spa och en skypool i byggnaden.')
p('.why.points[0][1]',
  'Compradores que buscan una vivienda grande de tres o cuatro dormitorios en Estepona, con vistas al mar e instalaciones de bienestar en el propio edificio, para vivir o como segunda residencia.',
  'Acheteurs qui recherchent un grand logement de trois ou quatre chambres à Estepona, avec vue sur la mer et des équipements de bien-être sur place, pour y vivre ou comme résidence secondaire.',
  'Käufer, die in Estepona eine große Wohnung mit drei oder vier Schlafzimmern suchen, mit Meerblick und Wellnessangeboten im Haus, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужна просторная квартира с тремя или четырьмя спальнями в Эстепоне, с видом на море и велнес-зонами в самом здании, для постоянного проживания или как второй дом.',
  'مشترون يبحثون عن مسكن كبير بثلاث أو أربع غرف نوم في إستيبونا، بإطلالة على البحر ومرافق عافية داخل المبنى، للسكن أو كمنزل ثانٍ.',
  'Kopers die in Estepona een grote woning met drie of vier slaapkamers zoeken, met zeezicht en wellnessvoorzieningen in het gebouw, om er te wonen of als tweede woning.',
  'Kupujący, którzy szukają w Esteponie dużego lokalu z trzema lub czterema sypialniami, z widokiem na morze i zapleczem wellness w budynku, do zamieszkania lub jako drugi dom.',
  'Kjøpere som vil ha en stor bolig med tre eller fire soverom i Estepona, med utsikt over havet og velværetilbud i selve bygget, til å bo i eller som feriebolig.',
  'Köpare som vill ha en stor bostad med tre eller fyra sovrum i Estepona, med havsutsikt och wellnessfaciliteter i själva byggnaden, att bo i eller som andra bostad.')
p('.why.points[1][1]',
  'Viviendas de 186 a 230 {U} construidos con terrazas cubiertas de 67 a 133 {U}, un spa con piscina interior, una skypool, y de dos a cuatro plazas de garaje con cada vivienda listada.',
  'Des logements de 186 à 230 {U} construits avec des terrasses couvertes de 67 à 133 {U}, un spa avec piscine intérieure, une skypool, et de deux à quatre places de garage avec chaque logement annoncé.',
  'Wohnungen mit 186 bis 230 {U} bebauter Fläche und überdachten Terrassen von 67 bis 133 {U}, ein Spa mit Innenpool, ein Skypool und zwei bis vier Garagenstellplätze bei jeder gelisteten Wohnung.',
  'Квартиры от 186 до 230 {U} застроенной площади с крытыми террасами от 67 до 133 {U}, спа с крытым бассейном, скайпул и от двух до четырёх мест в гараже у каждого объекта в списке.',
  'مساكن من 186 إلى 230 {U} مبنية مع تراسات مغطاة من 67 إلى 133 {U}، وسبا بمسبح داخلي ومسبح سكاي، ومن موقفين إلى أربعة مواقف في المرآب مع كل مسكن مدرج.',
  'Woningen van 186 tot 230 {U} bebouwd met overdekte terrassen van 67 tot 133 {U}, een spa met binnenzwembad, een skypool en twee tot vier garageplaatsen bij elke aangeboden woning.',
  'Lokale o powierzchni zabudowy od 186 do 230 {U} z zadaszonymi tarasami od 67 do 133 {U}, spa z basenem wewnętrznym, skypool oraz od dwóch do czterech miejsc garażowych przy każdym oferowanym lokalu.',
  'Boliger på 186 til 230 {U} bebygd areal med overbygde terrasser på 67 til 133 {U}, et spa med innendørsbasseng, en skypool og to til fire garasjeplasser til hver oppførte bolig.',
  'Bostäder på 186 till 230 {U} byggyta med övertäckta terrasser på 67 till 133 {U}, ett spa med inomhuspool, en skypool och två till fyra garageplatser till varje listad bostad.')
p('.why.points[2][1]',
  'El folleto sitúa el edificio en Estepona, con el mar y las montañas alrededor, a 20 minutos de Marbella y a 25 de Sotogrande. El plano de situación del promotor muestra la parcela frente a una carretera costera, con el mar al otro lado.',
  'La brochure situe l’immeuble à Estepona, entouré par la mer et les montagnes, à 20 minutes de Marbella et à 25 de Sotogrande. Le plan de situation du promoteur montre la parcelle face à une route côtière, avec la mer au-delà.',
  'Die Broschüre verortet das Gebäude in Estepona, umgeben von Meer und Bergen, 20 Minuten von Marbella und 25 von Sotogrande entfernt. Der Lageplan des Bauträgers zeigt das Grundstück an einer Küstenstraße, dahinter das Meer.',
  'Брошюра помещает здание в Эстепоне, между морем и горами, в 20 минутах от Марбельи и в 25 от Сотогранде. На плане участка застройщика участок обращён к прибрежной дороге, а за ней море.',
  'يضع الكتيّب المبنى في إستيبونا، بين البحر والجبال، على بعد 20 دقيقة من ماربيا و25 دقيقة من سوتوغراندي. ويُظهر مخطط الموقع الذي أعدّه المطوّر الأرض مقابل طريق ساحلي والبحر خلفه.',
  'De brochure plaatst het gebouw in Estepona, met de zee en de bergen eromheen, op 20 minuten van Marbella en 25 van Sotogrande. De situatieplattegrond van de ontwikkelaar toont het perceel tegenover een kustweg, met de zee daarachter.',
  'Broszura umieszcza budynek w Esteponie, w otoczeniu morza i gór, 20 minut od Marbelli i 25 od Sotogrande. Plan sytuacyjny dewelopera pokazuje działkę przy drodze nadmorskiej, a za nią morze.',
  'Brosjyren plasserer bygningen i Estepona, med havet og fjellene rundt, 20 minutter fra Marbella og 25 fra Sotogrande. Utbyggerens situasjonsplan viser tomten ved en kystvei, med havet bak.',
  'Broschyren placerar byggnaden i Estepona, med havet och bergen runtomkring, 20 minuter från Marbella och 25 från Sotogrande. Exploatörens situationsplan visar tomten vid en kustväg, med havet bortom.')
p('.why.points[3][1]',
  'La ficha del promotor marca la licencia de obras y la licencia de primera ocupación como pendientes y no da fecha de inicio ni de fin de las obras, por lo que pedimos el estado de la licencia y la fecha contractual de finalización antes de cualquier reserva.',
  'La fiche du promoteur indique que le permis de construire et la licence de première occupation sont en attente et ne donne aucune date de début ni de fin des travaux ; nous demandons donc l’état du permis et la date d’achèvement contractuelle avant toute réservation.',
  'Das Datenblatt des Bauträgers markiert die Baugenehmigung und die Erstbezugsgenehmigung als ausstehend und nennt weder Beginn noch Ende der Bauarbeiten; deshalb fragen wir vor jeder Reservierung den Stand der Genehmigung und den vertraglichen Fertigstellungstermin ab.',
  'В справке застройщика разрешение на строительство и лицензия на первое заселение отмечены как ожидаемые, а дат начала и окончания работ нет, поэтому до любого бронирования мы запрашиваем статус разрешения и договорный срок завершения.',
  'تضع ورقة المطوّر رخصة البناء ورخصة الإشغال الأول في خانة قيد الانتظار ولا تذكر تاريخ بدء الأعمال ولا انتهائها، لذلك نطلب حالة الرخصة وموعد الإنجاز التعاقدي قبل أي حجز.',
  'Het informatieblad van de ontwikkelaar markeert de bouwvergunning en de vergunning voor eerste ingebruikname als in afwachting en geeft geen begin- of einddatum van de werken, dus vragen wij vóór elke reservering naar de stand van de vergunning en de contractuele opleverdatum.',
  'Arkusz dewelopera oznacza pozwolenie na budowę i pozwolenie na pierwsze zasiedlenie jako oczekujące i nie podaje daty rozpoczęcia ani zakończenia prac, dlatego przed każdą rezerwacją pytamy o stan pozwolenia i umowny termin ukończenia.',
  'Utbyggerens ark markerer byggetillatelsen og brukstillatelsen som ikke på plass og oppgir verken start eller slutt for arbeidene, så vi ber om status for tillatelsen og den kontraktsfestede ferdigstillelsesdatoen før enhver reservasjon.',
  'Exploatörens blad markerar bygglovet och tillståndet för första ibruktagande som ännu inte beviljade och anger varken start eller slut för arbetena, så vi begär status för bygglovet och det avtalade färdigställandedatumet före varje bokning.')

p('.architecture.headlineHtml', 'Un edificio en terrazas, <em>abierto al mar</em>', 'Un immeuble en terrasses, <em>ouvert sur la mer</em>',
  'Ein Terrassengebäude, <em>offen zum Meer</em>', 'Здание с террасами, <em>открытое морю</em>', 'مبنى متدرج، <em>مفتوح على البحر</em>',
  'Een terrassengebouw, <em>open naar de zee</em>', 'Budynek tarasowy, <em>otwarty na morze</em>', 'En terrassebygning, <em>åpen mot havet</em>', 'Ett terrasshus, <em>öppet mot havet</em>')
p('.architecture.copy[0]',
  'En las imágenes el edificio es un bloque en terrazas con forjados curvos de color arena que vuelan sobre las terrazas, barandillas de cristal, vegetación en cada planta y jardines alrededor.',
  'Sur les images, l’immeuble est un bloc en terrasses aux dalles courbes couleur sable qui surplombent les terrasses, avec des garde-corps en verre, de la végétation à chaque niveau et des jardins tout autour.',
  'Auf den Bildern ist das Gebäude ein Terrassenblock mit geschwungenen sandfarbenen Geschossdecken, die über die Terrassen auskragen, mit Glasbrüstungen, Bepflanzung auf jeder Ebene und Gärten ringsum.',
  'На изображениях здание — корпус с террасами: изогнутые перекрытия песочного цвета нависают над террасами, стеклянные ограждения, озеленение на каждом уровне и сады вокруг.',
  'في الصور يظهر المبنى كتلة متدرجة ببلاطات منحنية بلون الرمل تبرز فوق التراسات، وحواجز زجاجية ونباتات في كل طابق وحدائق حوله.',
  'Op de beelden is het gebouw een terrassenblok met gebogen zandkleurige vloerplaten die boven de terrassen uitsteken, glazen balustrades, beplanting op elke verdieping en tuinen eromheen.',
  'Na wizualizacjach budynek jest tarasową bryłą z zaokrąglonymi piaskowymi stropami wysuniętymi nad tarasy, szklanymi balustradami, zielenią na każdej kondygnacji i ogrodami wokół.',
  'På bildene er bygningen en terrasseblokk med buede sandfargede dekker som stikker ut over terrassene, glassrekkverk, beplantning i hver etasje og hager rundt.',
  'På bilderna är byggnaden ett terrasshus med böjda sandfärgade bjälklag som skjuter ut över terrasserna, glasräcken, grönska på varje våning och trädgårdar runtomkring.')
p('.architecture.copy[1]',
  'El folleto describe una arquitectura definida por una esencia mediterránea: viviendas orientadas al sur con ventilación cruzada, distribuciones abiertas con terrazas generosas y áticos con acceso directo en ascensor desde el nivel del garaje.',
  'La brochure décrit une architecture définie par une essence méditerranéenne : des logements orientés au sud avec ventilation traversante, des plans ouverts avec de généreuses terrasses et des penthouses accessibles directement en ascenseur depuis le niveau du parking.',
  'Die Broschüre beschreibt eine von mediterranem Wesen geprägte Architektur: nach Süden ausgerichtete Wohnungen mit Querlüftung, offene Grundrisse mit großzügigen Terrassen und Penthäuser mit direktem Aufzugszugang von der Parkebene.',
  'В брошюре архитектура описана как определяемая средиземноморской сутью: квартиры с южной ориентацией и сквозным проветриванием, открытая планировка с просторными террасами и пентхаусы с прямым доступом на лифте с уровня парковки.',
  'يصف الكتيّب عمارة يحددها الطابع المتوسطي: مساكن متجهة نحو الجنوب مع تهوية متقاطعة وتصاميم مفتوحة وتراسات واسعة، وبنتهاوس بوصول مباشر بالمصعد من مستوى المرآب.',
  'De brochure beschrijft een architectuur die wordt bepaald door een mediterrane essentie: op het zuiden gerichte woningen met doorstroomventilatie, open indelingen met royale terrassen en penthouses met directe liftverbinding vanaf het parkeerniveau.',
  'Broszura opisuje architekturę określoną przez śródziemnomorską istotę: lokale o południowej ekspozycji ze skrośnym przewietrzaniem, otwarte układy z dużymi tarasami oraz penthouse’y z bezpośrednim dojazdem windą z poziomu garażu.',
  'Brosjyren beskriver en arkitektur definert av en middelhavsaktig egenart: sørvendte boliger med gjennomlufting, åpne planløsninger med romslige terrasser og toppleiligheter med direkte heistilgang fra parkeringsnivået.',
  'Broschyren beskriver en arkitektur som definieras av en medelhavsprägel: bostäder i söderläge med genomluftning, öppna planlösningar med generösa terrasser och takvåningar med direkt hisstillgång från garagenivån.')
p('.architecture.highlights[0][0]', 'Distribución', 'Agencement', 'Grundrisse', 'Планировка', 'التوزيع', 'Indeling', 'Układ', 'Planløsning', 'Planlösning')
p('.architecture.highlights[0][1]',
  'Zonas abiertas de salón, cocina y comedor de 69 a 86 {U}, con una gran terraza junto a ellas, según los planos.',
  'Des espaces ouverts séjour, cuisine et salle à manger de 69 à 86 {U}, avec une grande terrasse à côté, d’après les plans.',
  'Offene Wohn-, Koch- und Essbereiche von 69 bis 86 {U} mit einer großen Terrasse daneben, laut Plänen.',
  'Открытые зоны гостиной, кухни и столовой площадью от 69 до 86 {U} с большой террасой рядом — по планам.',
  'مناطق مفتوحة للمعيشة والمطبخ والطعام من 69 إلى 86 {U} يجاورها تراس كبير، بحسب المخططات.',
  'Open woon-, keuken- en eetruimtes van 69 tot 86 {U} met een groot terras ernaast, volgens de plattegronden.',
  'Otwarte strefy salonu, kuchni i jadalni o powierzchni od 69 do 86 {U} z dużym tarasem obok, według rzutów.',
  'Åpne områder for stue, kjøkken og spisestue på 69 til 86 {U} med en stor terrasse ved siden av, ifølge plantegningene.',
  'Öppna ytor för vardagsrum, kök och matplats på 69 till 86 {U} med en stor terrass intill, enligt planritningarna.')
p('.architecture.highlights[1][1]',
  'Un dormitorio principal de 27 a 34 {U} con baño propio, y dos o tres dormitorios más de 18 a 22 {U}.',
  'Une chambre principale de 27 à 34 {U} avec sa propre salle de bains, et deux ou trois autres chambres de 18 à 22 {U}.',
  'Ein Hauptschlafzimmer von 27 bis 34 {U} mit eigenem Bad und zwei oder drei weitere Schlafzimmer von 18 bis 22 {U}.',
  'Главная спальня площадью от 27 до 34 {U} с собственной ванной комнатой и ещё две или три спальни от 18 до 22 {U}.',
  'غرفة نوم رئيسية من 27 إلى 34 {U} مع حمام خاص، وغرفتا نوم أو ثلاث غرف أخرى من 18 إلى 22 {U}.',
  'Een hoofdslaapkamer van 27 tot 34 {U} met eigen badkamer en twee of drie andere slaapkamers van 18 tot 22 {U}.',
  'Sypialnia główna o powierzchni od 27 do 34 {U} z własną łazienką oraz dwie lub trzy dalsze sypialnie o powierzchni od 18 do 22 {U}.',
  'Et hovedsoverom på 27 til 34 {U} med eget bad og to eller tre soverom til på 18 til 22 {U}.',
  'Ett huvudsovrum på 27 till 34 {U} med eget badrum och två eller tre sovrum till på 18 till 22 {U}.')
p('.architecture.highlights[2][0]', 'Ascensores y garaje', 'Ascenseurs et parking', 'Aufzüge und Garage', 'Лифты и гараж', 'المصاعد والمرآب', 'Liften en garage', 'Windy i garaż', 'Heiser og garasje', 'Hissar och garage')
p('.architecture.highlights[2][1]',
  'Los ascensores sirven a las viviendas y los áticos tienen acceso directo en ascensor desde el nivel del garaje. Los planos muestran plantas de garaje subterráneas.',
  'Les ascenseurs desservent les logements et les penthouses sont accessibles directement en ascenseur depuis le niveau du parking. Les plans montrent des niveaux de garage souterrains.',
  'Aufzüge erschließen die Wohnungen, und die Penthäuser haben direkten Aufzugszugang von der Parkebene. Die Pläne zeigen unterirdische Garagengeschosse.',
  'Лифты обслуживают квартиры, а пентхаусы имеют прямой доступ на лифте с уровня парковки. На планах показаны подземные гаражные этажи.',
  'تخدم المصاعد المساكن، وللبنتهاوس وصول مباشر بالمصعد من مستوى المرآب. وتُظهر المخططات طوابق مرآب تحت الأرض.',
  'Liften bedienen de woningen en de penthouses hebben directe liftverbinding vanaf het parkeerniveau. De plattegronden tonen ondergrondse garageverdiepingen.',
  'Windy obsługują lokale, a penthouse’y mają bezpośredni dojazd windą z poziomu garażu. Rzuty pokazują podziemne kondygnacje garażowe.',
  'Heiser betjener boligene, og toppleilighetene har direkte heistilgang fra parkeringsnivået. Plantegningene viser underjordiske garasjeplan.',
  'Hissar betjänar bostäderna och takvåningarna har direkt hisstillgång från garagenivån. Planritningarna visar underjordiska garageplan.')
p('.architecture.highlights[3][0]', 'Azotea', 'Toit', 'Dach', 'Крыша', 'السطح', 'Dak', 'Dach', 'Tak', 'Tak')
p('.architecture.highlights[3][1]',
  'El folleto menciona una skypool y un salón en la azotea, y el plano del ático 12 añade una planta de azotea propia con un solárium descubierto, un salón cubierto y un jacuzzi.',
  'La brochure mentionne une skypool et un salon sur le toit, et le plan du penthouse 12 ajoute un niveau de toit propre avec un solarium découvert, un séjour couvert et un jacuzzi.',
  'Die Broschüre nennt einen Skypool und eine Dachlounge, und der Plan von Penthouse 12 ergänzt eine eigene Dachebene mit einem unüberdachten Solarium, einem überdachten Wohnbereich und einem Whirlpool.',
  'В брошюре упомянуты скайпул и лаунж на крыше, а на плане пентхауса 12 добавлен собственный уровень на крыше с открытым солярием, крытой гостиной и джакузи.',
  'يذكر الكتيّب مسبح سكاي وصالة على السطح، ويضيف مخطط البنتهاوس 12 طابق سطح خاصاً به مع سولاريوم مكشوف وصالة معيشة مغطاة وجاكوزي.',
  'De brochure noemt een skypool en een lounge op het dak, en het plan van penthouse 12 voegt een eigen dakverdieping toe met een onoverdekt solarium, een overdekte woonkamer en een jacuzzi.',
  'Broszura wymienia skypool i lounge na dachu, a rzut penthouse’u 12 dodaje własną kondygnację dachową z odkrytym solarium, zadaszonym salonem i jacuzzi.',
  'Brosjyren nevner en skypool og en lounge på taket, og planen for toppleilighet 12 legger til et eget takplan med en åpen solterrasse, en overbygd stue og et boblebad.',
  'Broschyren nämner en skypool och en lounge på taket, och planritningen för takvåning 12 lägger till ett eget takplan med en öppen solterrass, ett övertäckt vardagsrum och ett jacuzzi.')

# ---- residences -------------------------------------------------------------------------------------
p('.residences.headlineHtml', 'Seis viviendas, <em>tres tipos</em>', 'Six logements, <em>trois types</em>', 'Sechs Wohnungen, <em>drei Typen</em>',
  'Шесть квартир, <em>три типа</em>', 'ستة مساكن، <em>ثلاثة أنواع</em>', 'Zes woningen, <em>drie soorten</em>', 'Sześć lokali, <em>trzy rodzaje</em>',
  'Seks boliger, <em>tre typer</em>', 'Sex bostäder, <em>tre typer</em>')
p('.residences.copy',
  'Las seis viviendas disponibles son cinco viviendas en la primera planta y un ático. Las superficies construidas son las de la lista de precios, que los planos repiten; las superficies útiles proceden de los planos.',
  'Les six logements disponibles sont cinq logements au premier étage et un penthouse. Les surfaces construites sont celles de la liste de prix, que les plans reprennent ; les surfaces utiles proviennent des plans.',
  'Die sechs verfügbaren Wohnungen sind fünf Wohnungen im ersten Obergeschoss und ein Penthouse. Die bebauten Flächen stammen aus der Preisliste, die die Pläne wiederholen; die Nutzflächen stammen aus den Plänen.',
  'Шесть доступных объектов — это пять квартир на втором этаже и один пентхаус. Площади застройки взяты из прайс-листа, и планы их повторяют; полезные площади — из планов.',
  'المساكن الستة المتاحة هي خمسة مساكن في الطابق الأول وبنتهاوس واحد. المساحات المبنية هي الواردة في قائمة الأسعار وتكررها المخططات، أما المساحات الصافية فمن المخططات.',
  'De zes beschikbare woningen zijn vijf woningen op de eerste verdieping en één penthouse. De bebouwde oppervlakten zijn die van de prijslijst, die de plattegronden herhalen; de gebruiksoppervlakten komen uit de plattegronden.',
  'Sześć dostępnych lokali to pięć lokali na pierwszym piętrze i jeden penthouse. Powierzchnie zabudowy pochodzą z cennika, a rzuty je powtarzają; powierzchnie użytkowe pochodzą z rzutów.',
  'De seks ledige boligene er fem boliger i andre etasje og én toppleilighet. De bebygde arealene er de fra prislisten, som plantegningene gjentar; bruksarealene er fra plantegningene.',
  'De sex lediga bostäderna är fem bostäder på första våningen och en takvåning. Byggytorna är de i prislistan, som planritningarna upprepar; nyttoytorna kommer från planritningarna.')
p('.residences.items[0].name', 'La vivienda de cuatro dormitorios', 'Le logement de quatre chambres', 'Die Wohnung mit vier Schlafzimmern', 'Квартира с четырьмя спальнями',
  'المسكن بأربع غرف نوم', 'De woning met vier slaapkamers', 'Lokal z czterema sypialniami', 'Boligen med fire soverom', 'Bostaden med fyra sovrum')
p('.residences.items[0].points[0]',
  'La vivienda 1 está en la primera planta, con cuatro dormitorios, cuatro baños y un aseo de cortesía: {N230.07} {U} construidos y {N208.06} {U} útiles en el interior, con terrazas cubiertas de {N133.27} {U} construidos, que son {N114.96} {U} útiles en dos terrazas de {N63.53} y {N51.43} {U}.',
  'Le logement 1 est au premier étage, avec quatre chambres, quatre salles de bains et des toilettes d’invités : {N230.07} {U} construits et {N208.06} {U} utiles à l’intérieur, avec des terrasses couvertes de {N133.27} {U} construits, soit {N114.96} {U} utiles en deux terrasses de {N63.53} et {N51.43} {U}.',
  'Wohnung 1 liegt im ersten Obergeschoss, mit vier Schlafzimmern, vier Bädern und einem Gäste-WC: {N230.07} {U} bebaut und {N208.06} {U} Nutzfläche innen, mit überdachten Terrassen von {N133.27} {U} bebaut, das sind {N114.96} {U} Nutzfläche in zwei Terrassen von {N63.53} und {N51.43} {U}.',
  'Квартира 1 находится на втором этаже: четыре спальни, четыре ванные комнаты и гостевой санузел; {N230.07} {U} застроенной площади и {N208.06} {U} полезной площади внутри, крытые террасы {N133.27} {U} застройки, что составляет {N114.96} {U} полезной площади в двух террасах по {N63.53} и {N51.43} {U}.',
  'المسكن 1 في الطابق الأول، بأربع غرف نوم وأربعة حمامات ودورة مياه للضيوف: {N230.07} {U} مبنية و{N208.06} {U} مساحة صافية في الداخل، مع تراسات مغطاة بمساحة {N133.27} {U} مبنية، أي {N114.96} {U} صافية في تراسين مساحتهما {N63.53} و{N51.43} {U}.',
  'Woning 1 ligt op de eerste verdieping, met vier slaapkamers, vier badkamers en een gastentoilet: {N230.07} {U} bebouwd en {N208.06} {U} gebruiksoppervlak binnen, met overdekte terrassen van {N133.27} {U} bebouwd, wat {N114.96} {U} gebruiksoppervlak is in twee terrassen van {N63.53} en {N51.43} {U}.',
  'Lokal 1 znajduje się na pierwszym piętrze i ma cztery sypialnie, cztery łazienki oraz toaletę dla gości: {N230.07} {U} zabudowy i {N208.06} {U} powierzchni użytkowej wewnątrz, z zadaszonymi tarasami o powierzchni zabudowy {N133.27} {U}, co daje {N114.96} {U} powierzchni użytkowej w dwóch tarasach o powierzchni {N63.53} i {N51.43} {U}.',
  'Bolig 1 ligger i andre etasje, med fire soverom, fire bad og et gjestetoalett: {N230.07} {U} bebygd og {N208.06} {U} bruksareal innvendig, med overbygde terrasser på {N133.27} {U} bebygd, som er {N114.96} {U} bruksareal fordelt på to terrasser på {N63.53} og {N51.43} {U}.',
  'Bostad 1 ligger på första våningen, med fyra sovrum, fyra badrum och en gästtoalett: {N230.07} {U} byggyta och {N208.06} {U} nyttoyta inomhus, med övertäckta terrasser på {N133.27} {U} byggyta, vilket är {N114.96} {U} nyttoyta fördelad på två terrasser på {N63.53} och {N51.43} {U}.')
p('.residences.items[0].points[1]',
  'La zona de salón, cocina y comedor mide {N85.76} {U}, el dormitorio principal {N30.89} {U} y los demás dormitorios {N22.34}, {N19.52} y {N19.50} {U}. La lista de precios asigna a la vivienda dos plazas de garaje.',
  'L’espace séjour, cuisine et salle à manger mesure {N85.76} {U}, la chambre principale {N30.89} {U} et les autres chambres {N22.34}, {N19.52} et {N19.50} {U}. La liste de prix attribue deux places de garage au logement.',
  'Der Wohn-, Koch- und Essbereich misst {N85.76} {U}, das Hauptschlafzimmer {N30.89} {U} und die übrigen Schlafzimmer {N22.34}, {N19.52} und {N19.50} {U}. Die Preisliste weist der Wohnung zwei Garagenstellplätze zu.',
  'Зона гостиной, кухни и столовой — {N85.76} {U}, главная спальня — {N30.89} {U}, остальные спальни — {N22.34}, {N19.52} и {N19.50} {U}. По прайс-листу к квартире относятся два места в гараже.',
  'تبلغ مساحة منطقة المعيشة والمطبخ والطعام {N85.76} {U}، وغرفة النوم الرئيسية {N30.89} {U}، وغرف النوم الأخرى {N22.34} و{N19.52} و{N19.50} {U}. وتمنح قائمة الأسعار المسكن موقفين في المرآب.',
  'De woon-, keuken- en eetruimte meet {N85.76} {U}, de hoofdslaapkamer {N30.89} {U} en de andere slaapkamers {N22.34}, {N19.52} en {N19.50} {U}. De prijslijst kent de woning twee garageplaatsen toe.',
  'Strefa salonu, kuchni i jadalni ma {N85.76} {U}, sypialnia główna {N30.89} {U}, a pozostałe sypialnie {N22.34}, {N19.52} i {N19.50} {U}. Cennik przypisuje lokalowi dwa miejsca garażowe.',
  'Området for stue, kjøkken og spisestue er {N85.76} {U}, hovedsoverommet {N30.89} {U} og de andre soverommene {N22.34}, {N19.52} og {N19.50} {U}. Prislisten gir boligen to garasjeplasser.',
  'Ytan för vardagsrum, kök och matplats är {N85.76} {U}, huvudsovrummet {N30.89} {U} och de andra sovrummen {N22.34}, {N19.52} och {N19.50} {U}. Prislistan ger bostaden två garageplatser.')
p('.residences.items[0].points[2]', 'El precio es de {E3700000}.', 'Le prix est de {E3700000}.', 'Der Preis beträgt {E3700000}.', 'Цена — {E3700000}.', 'السعر {E3700000}.',
  'De prijs is {E3700000}.', 'Cena wynosi {E3700000}.', 'Prisen er {E3700000}.', 'Priset är {E3700000}.')
p('.residences.items[1].name', 'Viviendas de tres dormitorios en la primera planta', 'Logements de trois chambres au premier étage', 'Wohnungen mit drei Schlafzimmern im ersten Obergeschoss',
  'Квартиры с тремя спальнями на втором этаже', 'مساكن بثلاث غرف نوم في الطابق الأول', 'Woningen met drie slaapkamers op de eerste verdieping', 'Lokale z trzema sypialniami na pierwszym piętrze',
  'Boliger med tre soverom i andre etasje', 'Bostäder med tre sovrum på första våningen')
p('.residences.items[1].points[0]',
  'Cuatro viviendas de la primera planta con tres dormitorios, tres baños y un aseo de cortesía: las viviendas 5, 9, 13 y 17, de {N194.17}, {N186.32}, {N186.32} y {N200.40} {U} construidos y {N176.02}, {N168.44}, {N168.44} y {N182.26} {U} útiles.',
  'Quatre logements du premier étage avec trois chambres, trois salles de bains et des toilettes d’invités : les logements 5, 9, 13 et 17, de {N194.17}, {N186.32}, {N186.32} et {N200.40} {U} construits et {N176.02}, {N168.44}, {N168.44} et {N182.26} {U} utiles.',
  'Vier Wohnungen im ersten Obergeschoss mit drei Schlafzimmern, drei Bädern und einem Gäste-WC: die Wohnungen 5, 9, 13 und 17 mit {N194.17}, {N186.32}, {N186.32} und {N200.40} {U} bebaut und {N176.02}, {N168.44}, {N168.44} und {N182.26} {U} Nutzfläche.',
  'Четыре квартиры на втором этаже с тремя спальнями, тремя ванными комнатами и гостевым санузлом: квартиры 5, 9, 13 и 17 площадью {N194.17}, {N186.32}, {N186.32} и {N200.40} {U} застройки и {N176.02}, {N168.44}, {N168.44} и {N182.26} {U} полезной площади.',
  'أربعة مساكن في الطابق الأول بثلاث غرف نوم وثلاثة حمامات ودورة مياه للضيوف: المساكن 5 و9 و13 و17، بمساحات مبنية {N194.17} و{N186.32} و{N186.32} و{N200.40} {U} ومساحات صافية {N176.02} و{N168.44} و{N168.44} و{N182.26} {U}.',
  'Vier woningen op de eerste verdieping met drie slaapkamers, drie badkamers en een gastentoilet: de woningen 5, 9, 13 en 17, van {N194.17}, {N186.32}, {N186.32} en {N200.40} {U} bebouwd en {N176.02}, {N168.44}, {N168.44} en {N182.26} {U} gebruiksoppervlak.',
  'Cztery lokale na pierwszym piętrze z trzema sypialniami, trzema łazienkami i toaletą dla gości: lokale 5, 9, 13 i 17, o powierzchni zabudowy {N194.17}, {N186.32}, {N186.32} i {N200.40} {U} oraz powierzchni użytkowej {N176.02}, {N168.44}, {N168.44} i {N182.26} {U}.',
  'Fire boliger i andre etasje med tre soverom, tre bad og et gjestetoalett: bolig 5, 9, 13 og 17, på {N194.17}, {N186.32}, {N186.32} og {N200.40} {U} bebygd og {N176.02}, {N168.44}, {N168.44} og {N182.26} {U} bruksareal.',
  'Fyra bostäder på första våningen med tre sovrum, tre badrum och en gästtoalett: bostad 5, 9, 13 och 17, på {N194.17}, {N186.32}, {N186.32} och {N200.40} {U} byggyta och {N176.02}, {N168.44}, {N168.44} och {N182.26} {U} nyttoyta.')
p('.residences.items[1].points[1]',
  'Terrazas cubiertas de {N71.40}, {N67.46}, {N67.46} y {N76.39} {U} construidos, y zonas de salón, cocina y comedor de {N72.99}, {N69.41}, {N69.41} y {N77.87} {U}. Las viviendas 5, 9 y 13 tienen dos plazas de garaje y la vivienda 17 tiene tres.',
  'Des terrasses couvertes de {N71.40}, {N67.46}, {N67.46} et {N76.39} {U} construits, et des espaces séjour, cuisine et salle à manger de {N72.99}, {N69.41}, {N69.41} et {N77.87} {U}. Les logements 5, 9 et 13 ont deux places de garage et le logement 17 en a trois.',
  'Überdachte Terrassen von {N71.40}, {N67.46}, {N67.46} und {N76.39} {U} bebaut sowie Wohn-, Koch- und Essbereiche von {N72.99}, {N69.41}, {N69.41} und {N77.87} {U}. Die Wohnungen 5, 9 und 13 haben zwei Garagenstellplätze, die Wohnung 17 hat drei.',
  'Крытые террасы {N71.40}, {N67.46}, {N67.46} и {N76.39} {U} застройки и зоны гостиной, кухни и столовой {N72.99}, {N69.41}, {N69.41} и {N77.87} {U}. У квартир 5, 9 и 13 по два места в гараже, у квартиры 17 — три.',
  'تراسات مغطاة بمساحات مبنية {N71.40} و{N67.46} و{N67.46} و{N76.39} {U}، ومناطق معيشة ومطبخ وطعام بمساحات {N72.99} و{N69.41} و{N69.41} و{N77.87} {U}. للمساكن 5 و9 و13 موقفان في المرآب وللمسكن 17 ثلاثة مواقف.',
  'Overdekte terrassen van {N71.40}, {N67.46}, {N67.46} en {N76.39} {U} bebouwd, en woon-, keuken- en eetruimtes van {N72.99}, {N69.41}, {N69.41} en {N77.87} {U}. De woningen 5, 9 en 13 hebben twee garageplaatsen en woning 17 heeft er drie.',
  'Zadaszone tarasy o powierzchni zabudowy {N71.40}, {N67.46}, {N67.46} i {N76.39} {U} oraz strefy salonu, kuchni i jadalni o powierzchni {N72.99}, {N69.41}, {N69.41} i {N77.87} {U}. Lokale 5, 9 i 13 mają po dwa miejsca garażowe, a lokal 17 ma trzy.',
  'Overbygde terrasser på {N71.40}, {N67.46}, {N67.46} og {N76.39} {U} bebygd, og områder for stue, kjøkken og spisestue på {N72.99}, {N69.41}, {N69.41} og {N77.87} {U}. Bolig 5, 9 og 13 har to garasjeplasser og bolig 17 har tre.',
  'Övertäckta terrasser på {N71.40}, {N67.46}, {N67.46} och {N76.39} {U} byggyta, och ytor för vardagsrum, kök och matplats på {N72.99}, {N69.41}, {N69.41} och {N77.87} {U}. Bostad 5, 9 och 13 har två garageplatser och bostad 17 har tre.')
p('.residences.items[1].points[2]',
  'Los precios son {E2700000} para la vivienda 5, {E2500000} para las viviendas 9 y 13, y {E2900000} para la vivienda 17.',
  'Les prix sont de {E2700000} pour le logement 5, de {E2500000} pour les logements 9 et 13, et de {E2900000} pour le logement 17.',
  'Die Preise betragen {E2700000} für Wohnung 5, {E2500000} für die Wohnungen 9 und 13 und {E2900000} für Wohnung 17.',
  'Цены: {E2700000} за квартиру 5, {E2500000} за квартиры 9 и 13 и {E2900000} за квартиру 17.',
  'الأسعار {E2700000} للمسكن 5، و{E2500000} للمسكنين 9 و13، و{E2900000} للمسكن 17.',
  'De prijzen zijn {E2700000} voor woning 5, {E2500000} voor de woningen 9 en 13 en {E2900000} voor woning 17.',
  'Ceny wynoszą {E2700000} za lokal 5, {E2500000} za lokale 9 i 13 oraz {E2900000} za lokal 17.',
  'Prisene er {E2700000} for bolig 5, {E2500000} for bolig 9 og 13 og {E2900000} for bolig 17.',
  'Priserna är {E2700000} för bostad 5, {E2500000} för bostad 9 och 13 och {E2900000} för bostad 17.')
p('.residences.items[2].name', 'El ático', 'Le penthouse', 'Das Penthouse', 'Пентхаус', 'البنتهاوس', 'Het penthouse', 'Penthouse', 'Toppleiligheten', 'Takvåningen')
p('.residences.items[2].points[0]',
  'El ático 12 tiene tres dormitorios, tres baños y dos aseos de cortesía, repartidos en una planta principal y una planta de azotea: {N191.16} {U} construidos y {N167.92} {U} útiles en el interior, una terraza cubierta de {N67.46} {U} construidos y {N157.77} {U} construidos de solárium en la azotea, cubierto y descubierto.',
  'Le penthouse 12 compte trois chambres, trois salles de bains et deux toilettes d’invités, répartis sur un niveau principal et un niveau de toit : {N191.16} {U} construits et {N167.92} {U} utiles à l’intérieur, une terrasse couverte de {N67.46} {U} construits et {N157.77} {U} construits de solarium sur le toit, couvert et découvert.',
  'Penthouse 12 hat drei Schlafzimmer, drei Bäder und zwei Gäste-WCs, verteilt auf ein Hauptgeschoss und ein Dachgeschoss: {N191.16} {U} bebaut und {N167.92} {U} Nutzfläche innen, eine überdachte Terrasse von {N67.46} {U} bebaut und {N157.77} {U} bebaut Dachsolarium, überdacht und unüberdacht.',
  'В пентхаусе 12 три спальни, три ванные комнаты и два гостевых санузла на основном уровне и уровне крыши: {N191.16} {U} застроенной площади и {N167.92} {U} полезной площади внутри, крытая терраса {N67.46} {U} застройки и {N157.77} {U} застройки солярия на крыше, крытого и открытого.',
  'للبنتهاوس 12 ثلاث غرف نوم وثلاثة حمامات ودورتا مياه للضيوف، موزعة على طابق رئيسي وطابق سطح: {N191.16} {U} مبنية و{N167.92} {U} مساحة صافية في الداخل، وتراس مغطى بمساحة {N67.46} {U} مبنية، و{N157.77} {U} مبنية من سولاريوم السطح، مغطى ومكشوف.',
  'Penthouse 12 heeft drie slaapkamers, drie badkamers en twee gastentoiletten, verdeeld over een hoofdverdieping en een dakverdieping: {N191.16} {U} bebouwd en {N167.92} {U} gebruiksoppervlak binnen, een overdekt terras van {N67.46} {U} bebouwd en {N157.77} {U} bebouwd daksolarium, overdekt en onoverdekt.',
  'Penthouse 12 ma trzy sypialnie, trzy łazienki i dwie toalety dla gości na kondygnacji głównej i kondygnacji dachowej: {N191.16} {U} zabudowy i {N167.92} {U} powierzchni użytkowej wewnątrz, zadaszony taras o powierzchni zabudowy {N67.46} {U} oraz {N157.77} {U} zabudowy solarium na dachu, zadaszonego i odkrytego.',
  'Toppleilighet 12 har tre soverom, tre bad og to gjestetoaletter, fordelt på et hovedplan og et takplan: {N191.16} {U} bebygd og {N167.92} {U} bruksareal innvendig, en overbygd terrasse på {N67.46} {U} bebygd og {N157.77} {U} bebygd solterrasse på taket, overbygd og åpen.',
  'Takvåning 12 har tre sovrum, tre badrum och två gästtoaletter, fördelade på ett huvudplan och ett takplan: {N191.16} {U} byggyta och {N167.92} {U} nyttoyta inomhus, en övertäckt terrass på {N67.46} {U} byggyta och {N157.77} {U} byggyta solterrass på taket, övertäckt och öppen.')
p('.residences.items[2].points[1]',
  'En el plano, la planta de azotea tiene un solárium descubierto de {N73.92} {U}, un salón cubierto de {N67.80} {U} y un jacuzzi. La lista de precios asigna al ático cuatro plazas de garaje.',
  'Sur le plan, le niveau de toit comprend un solarium découvert de {N73.92} {U}, un séjour couvert de {N67.80} {U} et un jacuzzi. La liste de prix attribue quatre places de garage au penthouse.',
  'Im Plan hat die Dachebene ein unüberdachtes Solarium von {N73.92} {U}, einen überdachten Wohnbereich von {N67.80} {U} und einen Whirlpool. Die Preisliste weist dem Penthouse vier Garagenstellplätze zu.',
  'На плане уровень крыши включает открытый солярий {N73.92} {U}, крытую гостиную {N67.80} {U} и джакузи. По прайс-листу к пентхаусу относятся четыре места в гараже.',
  'في المخطط يضم طابق السطح سولاريوم مكشوفاً بمساحة {N73.92} {U} وصالة معيشة مغطاة بمساحة {N67.80} {U} وجاكوزي. وتمنح قائمة الأسعار البنتهاوس أربعة مواقف في المرآب.',
  'Op de plattegrond heeft de dakverdieping een onoverdekt solarium van {N73.92} {U}, een overdekte woonkamer van {N67.80} {U} en een jacuzzi. De prijslijst kent het penthouse vier garageplaatsen toe.',
  'Na rzucie kondygnacja dachowa ma odkryte solarium o powierzchni {N73.92} {U}, zadaszony salon o powierzchni {N67.80} {U} i jacuzzi. Cennik przypisuje penthouse’owi cztery miejsca garażowe.',
  'På planen har takplanet en åpen solterrasse på {N73.92} {U}, en overbygd stue på {N67.80} {U} og et boblebad. Prislisten gir toppleiligheten fire garasjeplasser.',
  'På planritningen har takplanet en öppen solterrass på {N73.92} {U}, ett övertäckt vardagsrum på {N67.80} {U} och ett jacuzzi. Prislistan ger takvåningen fyra garageplatser.')
p('.residences.items[2].points[2]', 'El precio es de {E4800000}.', 'Le prix est de {E4800000}.', 'Der Preis beträgt {E4800000}.', 'Цена — {E4800000}.', 'السعر {E4800000}.',
  'De prijs is {E4800000}.', 'Cena wynosi {E4800000}.', 'Prisen er {E4800000}.', 'Priset är {E4800000}.')

# ---- lifestyle ---------------------------------------------------------------------------------------
p('.lifestyle.headlineHtml', 'Un spa, <em>dos piscinas</em> y una azotea', 'Un spa, <em>deux piscines</em> et un toit', 'Ein Spa, <em>zwei Pools</em> und ein Dach',
  'Спа, <em>два бассейна</em> и крыша', 'سبا، <em>ومسبحان</em> وسطح', 'Een spa, <em>twee zwembaden</em> en een dak', 'Spa, <em>dwa baseny</em> i dach',
  'Et spa, <em>to basseng</em> og et tak', 'Ett spa, <em>två pooler</em> och ett tak')
p('.lifestyle.copy',
  'El folleto presenta el edificio como un lugar con su propia oferta de bienestar y un club de propietarios.',
  'La brochure présente l’immeuble comme un lieu doté de sa propre offre de bien-être et d’un club des propriétaires.',
  'Die Broschüre stellt das Gebäude als einen Ort mit eigenem Wellnessangebot und einem Eigentümerclub dar.',
  'В брошюре здание представлено как место с собственным велнес-предложением и клубом владельцев.',
  'يقدّم الكتيّب المبنى مكاناً له عرضه الخاص من خدمات العافية ونادٍ للملاك.',
  'De brochure presenteert het gebouw als een plek met een eigen wellnessaanbod en een eigenarenclub.',
  'Broszura przedstawia budynek jako miejsce z własną ofertą wellness i klubem właścicieli.',
  'Brosjyren presenterer bygningen som et sted med sitt eget velværetilbud og en eierklubb.',
  'Broschyren presenterar byggnaden som en plats med ett eget wellnessutbud och en ägarklubb.')
p('.lifestyle.panels[0][1]',
  'Un spa con piscina interior climatizada, salas de masajes y de belleza, y una sauna y hammam.',
  'Un spa avec piscine intérieure chauffée, des salles de massage et de beauté, ainsi qu’un sauna et un hammam.',
  'Ein Spa mit beheiztem Innenpool, Massage- und Beautyräumen sowie Sauna und Hammam.',
  'Спа с подогреваемым крытым бассейном, массажными и косметическими кабинетами, сауной и хаммамом.',
  'سبا بمسبح داخلي مدفأ وغرف للمساج والتجميل وساونا وحمّام.',
  'Een spa met verwarmd binnenzwembad, massage- en schoonheidsruimtes en een sauna en hammam.',
  'Spa z podgrzewanym basenem wewnętrznym, gabinetami masażu i kosmetycznymi oraz sauną i hammamem.',
  'Et spa med oppvarmet innendørsbasseng, masasje- og skjønnhetsrom og en badstue og hammam.',
  'Ett spa med uppvärmd inomhuspool, massage- och skönhetsrum samt bastu och hammam.')
p('.lifestyle.panels[1][0]', 'La skypool', 'La skypool', 'Der Skypool', 'Скайпул', 'مسبح السكاي', 'De skypool', 'Skypool', 'Skypoolen', 'Skypoolen')
p('.lifestyle.panels[1][1]',
  'Una skypool y un salón en la azotea y, según la ficha del promotor, una azotea con una zona de yoga.',
  'Une skypool et un salon sur le toit et, selon la fiche du promoteur, un toit avec un espace de yoga.',
  'Ein Skypool und eine Dachlounge sowie, laut Datenblatt des Bauträgers, ein Dach mit Yogabereich.',
  'Скайпул и лаунж на крыше, а по справке застройщика — ещё и крыша с зоной для йоги.',
  'مسبح سكاي وصالة على السطح، وبحسب ورقة المطوّر سطح فيه منطقة لليوغا.',
  'Een skypool en een lounge op het dak en, volgens het informatieblad van de ontwikkelaar, een dak met een yogaruimte.',
  'Skypool i lounge na dachu oraz, według arkusza dewelopera, dach ze strefą jogi.',
  'En skypool og en lounge på taket og, ifølge utbyggerens ark, et tak med et yogaområde.',
  'En skypool och en lounge på taket och, enligt exploatörens blad, ett tak med en yogayta.')
p('.lifestyle.panels[2][0]', 'El club de propietarios', 'Le club des propriétaires', 'Der Eigentümerclub', 'Клуб владельцев', 'نادي الملاك', 'De eigenarenclub', 'Klub właścicieli', 'Eierklubben', 'Ägarklubben')
p('.lifestyle.panels[2][1]',
  'Una comunidad para propietarios, con un salón y bar de propietarios, una sala de reuniones, un gimnasio y una sala polivalente, y acceso a marcas seleccionadas de bienestar, gastronomía y ocio.',
  'Une communauté pour les propriétaires, avec un salon et un bar réservés aux propriétaires, une salle de réunion, une salle de sport et une salle polyvalente, et un accès à des marques sélectionnées de bien-être, de gastronomie et de loisirs.',
  'Eine Gemeinschaft für Eigentümer mit einer Eigentümerlounge samt Bar, einem Besprechungsraum, einem Fitnessraum mit Mehrzweckfläche und Zugang zu ausgewählten Marken aus Wellness, Gastronomie und Freizeit.',
  'Сообщество для владельцев: лаунж с баром для владельцев, переговорная, тренажёрный зал с многофункциональным залом и доступ к избранным брендам в сфере велнеса, гастрономии и досуга.',
  'مجتمع للملاك، مع صالة وبار للملاك وقاعة اجتماعات وصالة رياضية وقاعة متعددة الاستخدامات، ووصول إلى علامات مختارة في العافية والطعام والترفيه.',
  'Een gemeenschap voor eigenaren, met een lounge met bar voor de eigenaren, een vergaderruimte, een fitnessruimte met flexruimte en toegang tot geselecteerde merken op het gebied van wellness, gastronomie en vrije tijd.',
  'Wspólnota dla właścicieli, z salonem i barem dla właścicieli, salą spotkań, siłownią z salą wielofunkcyjną oraz dostępem do wybranych marek z dziedziny wellness, gastronomii i wypoczynku.',
  'Et fellesskap for eiere, med en eierlounge med bar, et møterom, et treningsrom med fleksirom og tilgang til utvalgte merker innen velvære, gastronomi og fritid.',
  'En gemenskap för ägare, med en ägarlounge med bar, ett mötesrum, ett gym med flexyta och tillgång till utvalda varumärken inom wellness, gastronomi och fritid.')
p('.lifestyle.panels[3][1]',
  'El folleto enumera un administrador residencial, seguridad 24/7, un entrenador personal, instructores de yoga y fitness, masajistas y fisioterapeutas, tratamientos de belleza y servicios domésticos. Preguntamos cuáles están incluidos y cuáles se cobran aparte.',
  'La brochure énumère un gestionnaire résidentiel, une sécurité 24 h/24 et 7 j/7, un coach personnel, des instructeurs de yoga et de fitness, des masseurs et kinésithérapeutes, des soins de beauté et des services à domicile. Nous demandons lesquels sont inclus et lesquels sont facturés.',
  'Die Broschüre führt einen Residenzmanager, rund um die Uhr Sicherheitsdienst, einen Personal Trainer, Yoga- und Fitnesstrainer, Masseure und Physiotherapeuten, Schönheitsbehandlungen und Haushaltsdienste auf. Wir fragen nach, welche inbegriffen sind und welche berechnet werden.',
  'В брошюре перечислены управляющий комплексом, круглосуточная охрана, персональный тренер, инструкторы по йоге и фитнесу, массажисты и физиотерапевты, косметические процедуры и бытовые услуги. Мы уточняем, какие из них включены, а какие оплачиваются отдельно.',
  'يذكر الكتيّب مدير إقامة وأمناً على مدار الساعة ومدرباً شخصياً ومدرّبي يوغا ولياقة وأخصائيي مساج وعلاج طبيعي وعلاجات تجميل وخدمات منزلية. نسأل عن الخدمات المشمولة وتلك التي تُحتسب بمقابل.',
  'De brochure noemt een residentiemanager, 24/7 beveiliging, een personal trainer, yoga- en fitnessinstructeurs, masseurs en fysiotherapeuten, schoonheidsbehandelingen en huishoudelijke diensten. Wij vragen welke inbegrepen zijn en welke worden doorberekend.',
  'Broszura wymienia zarządcę rezydencji, całodobową ochronę, trenera personalnego, instruktorów jogi i fitnessu, masażystów i fizjoterapeutów, zabiegi kosmetyczne oraz usługi domowe. Pytamy, które są wliczone, a które płatne dodatkowo.',
  'Brosjyren nevner en boligforvalter, døgnvakt, en personlig trener, yoga- og treningsinstruktører, massører og fysioterapeuter, skjønnhetsbehandlinger og husholdningstjenester. Vi spør hvilke som er inkludert og hvilke som betales ekstra.',
  'Broschyren nämner en bostadsansvarig, säkerhet dygnet runt, en personlig tränare, yoga- och fitnessinstruktörer, massörer och fysioterapeuter, skönhetsbehandlingar och hushållstjänster. Vi frågar vilka som ingår och vilka som debiteras.')

# ---- location ------------------------------------------------------------------------------------------
p('.location.headlineHtml', 'Estepona, <em>en la Costa del Sol</em>', 'Estepona, <em>sur la Costa del Sol</em>', 'Estepona, <em>an der Costa del Sol</em>',
  'Эстепона, <em>на Коста-дель-Соль</em>', 'إستيبونا، <em>على كوستا ديل سول</em>', 'Estepona, <em>aan de Costa del Sol</em>', 'Estepona, <em>na Costa del Sol</em>',
  'Estepona, <em>på Costa del Sol</em>', 'Estepona, <em>på Costa del Sol</em>')
p('.location.copy',
  'El promotor sitúa el edificio en Estepona. Su mapa marca la parcela entre el centro de Estepona y Marbella, y su plano de situación muestra la parcela frente a una carretera costera, con el mar al otro lado. El folleto da tiempos de viaje aproximados desde la parcela, sin decir con qué medio, y describe paseos junto al mar, campos de golf, paseos a caballo, rutas y salidas en barco.',
  'Le promoteur situe l’immeuble à Estepona. Sa carte place le site entre le centre d’Estepona et Marbella, et son plan de situation montre la parcelle face à une route côtière, avec la mer au-delà. La brochure donne des temps de trajet approximatifs depuis le site, sans préciser le moyen de transport, et décrit des promenades en bord de mer, des parcours de golf, des balades à cheval, des sentiers et des sorties en bateau.',
  'Der Bauträger verortet das Gebäude in Estepona. Seine Karte markiert das Grundstück zwischen dem Zentrum von Estepona und Marbella, und sein Lageplan zeigt das Grundstück an einer Küstenstraße, dahinter das Meer. Die Broschüre nennt ungefähre Fahrzeiten ab dem Grundstück, ohne das Verkehrsmittel anzugeben, und beschreibt Spaziergänge am Meer, Golfplätze, Reiten, Wanderwege und Bootsausflüge.',
  'Застройщик помещает здание в Эстепоне. На его карте участок отмечен между центром Эстепоны и Марбельей, а на плане участка он обращён к прибрежной дороге, за которой море. В брошюре указано примерное время в пути от участка, без уточнения способа передвижения, и описаны прогулки у моря, поля для гольфа, верховая езда, тропы и морские прогулки.',
  'يضع المطوّر المبنى في إستيبونا. وتحدد خريطته الموقع بين مركز إستيبونا وماربيا، ويُظهر مخطط الموقع الأرض مقابل طريق ساحلي والبحر خلفه. ويذكر الكتيّب أزمنة سفر تقريبية من الموقع دون بيان وسيلة التنقل، ويصف التنزه قرب البحر وملاعب الغولف وركوب الخيل والمسارات والرحلات بالقارب.',
  'De ontwikkelaar plaatst het gebouw in Estepona. Zijn kaart markeert de locatie tussen het centrum van Estepona en Marbella, en zijn situatieplattegrond toont het perceel tegenover een kustweg, met de zee daarachter. De brochure geeft geschatte reistijden vanaf de locatie, zonder het vervoermiddel te noemen, en beschrijft wandelingen langs de zee, golfbanen, paardrijden, wandelpaden en boottochten.',
  'Deweloper umieszcza budynek w Esteponie. Jego mapa oznacza miejsce między centrum Estepony a Marbellą, a plan sytuacyjny pokazuje działkę przy drodze nadmorskiej, za którą jest morze. Broszura podaje przybliżone czasy dojazdu z tego miejsca, bez wskazania środka transportu, i opisuje spacery nad morzem, pola golfowe, jazdę konną, szlaki oraz rejsy łodzią.',
  'Utbyggeren plasserer bygningen i Estepona. Kartet dets markerer stedet mellom sentrum av Estepona og Marbella, og situasjonsplanen viser tomten ved en kystvei, med havet bak. Brosjyren oppgir omtrentlige reisetider fra stedet, uten å si hvilket transportmiddel, og beskriver turer langs havet, golfbaner, ridning, stier og båtturer.',
  'Exploatören placerar byggnaden i Estepona. Dess karta markerar platsen mellan centrala Estepona och Marbella, och dess situationsplan visar tomten vid en kustväg, med havet bortom. Broschyren anger ungefärliga restider från platsen, utan att säga med vilket färdmedel, och beskriver promenader vid havet, golfbanor, ridning, stigar och båtutflykter.')

# ---- investment, checks, availability ------------------------------------------------------------------
p('.investment.copy',
  'Confirmamos por escrito los precios actuales, la disponibilidad y las condiciones de compra antes de que usted reserve.',
  'Nous confirmons par écrit les prix actuels, la disponibilité et les conditions d’achat avant que vous ne réserviez.',
  'Wir bestätigen die aktuellen Preise, die Verfügbarkeit und die Kaufbedingungen schriftlich, bevor Sie reservieren.',
  'Мы письменно подтверждаем актуальные цены, наличие и условия покупки до того, как вы забронируете.',
  'نؤكد كتابةً الأسعار الحالية والتوفر وشروط الشراء قبل أن تحجزوا.',
  'Wij bevestigen de actuele prijzen, de beschikbaarheid en de aankoopvoorwaarden schriftelijk voordat u reserveert.',
  'Aktualne ceny, dostępność i warunki zakupu potwierdzamy na piśmie, zanim Pan lub Pani dokona rezerwacji.',
  'Vi bekrefter gjeldende priser, tilgjengelighet og kjøpsvilkår skriftlig før De reserverer.',
  'Vi bekräftar aktuella priser, tillgänglighet och köpvillkor skriftligen innan ni bokar.')
p('.investment.cards[0][1]',
  'La lista de precios indica que sus precios son netos y no incluyen el IVA. No da el tipo, por lo que confirmamos por escrito el tipo y los demás gastos de compra.',
  'La liste de prix indique que ses prix sont nets et n’incluent pas la TVA. Elle n’en donne pas le taux ; nous confirmons donc par écrit le taux et les autres frais d’achat.',
  'Laut Preisliste sind die Preise netto und enthalten keine MwSt. Sie nennt den Satz nicht, daher bestätigen wir den Satz und die übrigen Kaufnebenkosten schriftlich.',
  'В прайс-листе сказано, что цены указаны нетто и не включают НДС. Ставка не названа, поэтому мы письменно подтверждаем ставку и остальные расходы на покупку.',
  'تذكر قائمة الأسعار أن أسعارها صافية ولا تشمل ضريبة القيمة المضافة. ولا تذكر النسبة، لذلك نؤكد كتابةً النسبة وباقي مصاريف الشراء.',
  'De prijslijst vermeldt dat de prijzen netto zijn en geen btw bevatten. Ze geeft het tarief niet, dus bevestigen wij het tarief en de overige aankoopkosten schriftelijk.',
  'Cennik wskazuje, że jego ceny są cenami netto i nie zawierają VAT. Nie podaje stawki, dlatego potwierdzamy na piśmie stawkę i pozostałe koszty zakupu.',
  'Prislisten oppgir at prisene er netto og ikke inkluderer mva. Den oppgir ikke satsen, så vi bekrefter satsen og de øvrige kjøpskostnadene skriftlig.',
  'Prislistan anger att priserna är nettopriser och inte inkluderar IVA (spansk moms). Den anger inte satsen, så vi bekräftar satsen och de övriga köpkostnaderna skriftligen.')
p('.investment.cards[1][0]', 'Lo que muestra la lista de precios', 'Ce que montre la liste de prix', 'Was die Preisliste zeigt', 'Что показывает прайс-лист', 'ما تعرضه قائمة الأسعار',
  'Wat de prijslijst toont', 'Co pokazuje cennik', 'Hva prislisten viser', 'Vad prislistan visar')
p('.investment.cards[1][1]',
  'Cada vivienda incluye plazas de garaje: dos para las viviendas 1, 5, 9 y 13, tres para la vivienda 17 y cuatro para el ático 12.',
  'Chaque logement comprend des places de garage : deux pour les logements 1, 5, 9 et 13, trois pour le logement 17 et quatre pour le penthouse 12.',
  'Jede Wohnung hat Garagenstellplätze: zwei bei den Wohnungen 1, 5, 9 und 13, drei bei Wohnung 17 und vier beim Penthouse 12.',
  'К каждому объекту относятся места в гараже: два у квартир 1, 5, 9 и 13, три у квартиры 17 и четыре у пентхауса 12.',
  'يأتي كل مسكن مع مواقف في المرآب: موقفان للمساكن 1 و5 و9 و13، وثلاثة للمسكن 17، وأربعة للبنتهاوس 12.',
  'Elke woning heeft garageplaatsen: twee bij de woningen 1, 5, 9 en 13, drie bij woning 17 en vier bij penthouse 12.',
  'Każdy lokal ma miejsca garażowe: dwa w lokalach 1, 5, 9 i 13, trzy w lokalu 17 i cztery w penthouse’ie 12.',
  'Hver bolig har garasjeplasser: to for bolig 1, 5, 9 og 13, tre for bolig 17 og fire for toppleilighet 12.',
  'Varje bostad har garageplatser: två för bostad 1, 5, 9 och 13, tre för bostad 17 och fyra för takvåning 12.')
p('.investment.cards[2][1]',
  'La lista de precios lleva fecha del 6 de mayo de 2026 y marca 12 de las 20 viviendas como reservadas. Nuestra lista del 29 de octubre de 2026 muestra seis viviendas disponibles, a los mismos precios.',
  'La liste de prix est datée du 6 mai 2026 et marque 12 des 20 logements comme réservés. Notre liste du 29 octobre 2026 montre six logements disponibles, aux mêmes prix.',
  'Die Preisliste trägt das Datum 6. Mai 2026 und kennzeichnet 12 der 20 Wohnungen als reserviert. Unsere Liste vom 29. Oktober 2026 zeigt sechs verfügbare Wohnungen zu denselben Preisen.',
  'Прайс-лист датирован 6 мая 2026 года и отмечает 12 из 20 квартир как забронированные. В нашем списке от 29 октября 2026 года шесть доступных объектов по тем же ценам.',
  'تحمل قائمة الأسعار تاريخ 6 مايو 2026 وتضع 12 من المساكن العشرين في خانة المحجوزة. وتُظهر قائمتنا بتاريخ 29 أكتوبر 2026 ستة مساكن متاحة بالأسعار نفسها.',
  'De prijslijst is gedateerd op 6 mei 2026 en markeert 12 van de 20 woningen als gereserveerd. Onze lijst van 29 oktober 2026 toont zes beschikbare woningen, tegen dezelfde prijzen.',
  'Cennik nosi datę 6 maja 2026 r. i oznacza 12 z 20 lokali jako zarezerwowane. Nasza lista z 29 października 2026 r. pokazuje sześć dostępnych lokali po tych samych cenach.',
  'Prislisten er datert 6. mai 2026 og markerer 12 av de 20 boligene som reservert. Vår liste fra 29. oktober 2026 viser seks ledige boliger, til de samme prisene.',
  'Prislistan är daterad den 6 maj 2026 och markerar 12 av de 20 bostäderna som reserverade. Vår lista från den 29 oktober 2026 visar sex lediga bostäder, till samma priser.')
p('.investment.cards[3][0]', 'Lo que no está incluido', 'Ce qui n’est pas inclus', 'Was nicht enthalten ist', 'Что не входит в цену', 'ما هو غير مشمول',
  'Wat niet inbegrepen is', 'Czego nie obejmuje cena', 'Hva som ikke er inkludert', 'Vad som inte ingår')
p('.investment.cards[3][1]',
  'El mobiliario, los textiles y la decoración que se ven en las imágenes no están incluidos en el precio, como indica el folleto.',
  'Le mobilier, les textiles et la décoration que l’on voit sur les images ne sont pas inclus dans le prix, comme l’indique la brochure.',
  'Möbel, Textilien und Dekoration auf den Bildern sind im Preis nicht enthalten, wie die Broschüre festhält.',
  'Мебель, текстиль и декор, показанные на изображениях, не входят в цену, как указано в брошюре.',
  'الأثاث والمنسوجات والديكور الظاهرة في الصور غير مشمولة في السعر، كما يذكر الكتيّب.',
  'Het meubilair, de textiel en de decoratie die op de beelden te zien zijn, zijn niet bij de prijs inbegrepen, zoals de brochure vermeldt.',
  'Meble, tekstylia i dekoracje widoczne na wizualizacjach nie są wliczone w cenę, jak wskazuje broszura.',
  'Møblene, tekstilene og dekoren som vises på bildene er ikke inkludert i prisen, slik brosjyren oppgir.',
  'Möblerna, textilierna och inredningen som visas på bilderna ingår inte i priset, som broschyren anger.')

p('.trustDossier.cards[0][0]', 'Licencias y obras', 'Permis et travaux', 'Genehmigungen und Bauarbeiten', 'Разрешения и работы', 'الرخص والأعمال',
  'Vergunningen en werken', 'Pozwolenia i prace', 'Tillatelser og arbeider', 'Tillstånd och arbeten')
p('.trustDossier.cards[0][1]',
  'La ficha del promotor marca como pendientes la licencia de obras, la licencia de primera ocupación y la empresa constructora. Preguntamos por el estado de cada una y ponemos las respuestas por escrito.',
  'La fiche du promoteur indique que le permis de construire, la licence de première occupation et l’entreprise de construction sont en attente. Nous demandons l’état de chacun et mettons les réponses par écrit.',
  'Das Datenblatt des Bauträgers kennzeichnet die Baugenehmigung, die Erstbezugsgenehmigung und das Bauunternehmen als ausstehend. Wir fragen den Stand jedes Punktes ab und halten die Antworten schriftlich fest.',
  'В справке застройщика разрешение на строительство, лицензия на первое заселение и строительная компания отмечены как ожидаемые. Мы выясняем статус каждого пункта и фиксируем ответы письменно.',
  'تضع ورقة المطوّر رخصة البناء ورخصة الإشغال الأول وشركة المقاولات في خانة قيد الانتظار. نسأل عن حالة كل منها ونثبّت الإجابات كتابةً.',
  'Het informatieblad van de ontwikkelaar markeert de bouwvergunning, de vergunning voor eerste ingebruikname en het bouwbedrijf als in afwachting. Wij vragen naar de stand van elk en leggen de antwoorden schriftelijk vast.',
  'Arkusz dewelopera oznacza pozwolenie na budowę, pozwolenie na pierwsze zasiedlenie i firmę budowlaną jako oczekujące. Pytamy o stan każdego z nich i spisujemy odpowiedzi na piśmie.',
  'Utbyggerens ark markerer byggetillatelsen, brukstillatelsen og byggefirmaet som ikke på plass. Vi spør om status for hver av dem og setter svarene skriftlig.',
  'Exploatörens blad markerar bygglovet, tillståndet för första ibruktagande och byggföretaget som ännu inte på plats. Vi frågar om status för vart och ett och sätter svaren skriftligen.')
p('.trustDossier.cards[1][1]',
  'La ficha da el inicio y el fin de la construcción como por confirmar y ningún documento que tenemos da una fecha de finalización, por lo que pedimos la fecha contractual de la vivienda que usted elija.',
  'La fiche indique le début et la fin des travaux comme restant à confirmer et aucun document en notre possession ne donne de date d’achèvement ; nous demandons donc la date contractuelle pour le logement que vous choisirez.',
  'Das Datenblatt gibt Baubeginn und Bauende als noch zu bestätigen an, und kein Dokument, das uns vorliegt, nennt einen Fertigstellungstermin; deshalb fragen wir den vertraglichen Termin für die von Ihnen gewählte Wohnung ab.',
  'В справке начало и окончание строительства указаны как подлежащие уточнению, и ни в одном имеющемся у нас документе нет срока завершения, поэтому мы запрашиваем договорный срок для выбранной вами квартиры.',
  'تذكر الورقة أن بدء البناء وانتهاءه سيُؤكَّدان لاحقاً، ولا يذكر أي مستند لدينا موعداً للإنجاز، لذلك نطلب الموعد التعاقدي للمسكن الذي تختارونه.',
  'Het informatieblad geeft de start en het einde van de bouw aan als nog te bevestigen en geen enkel document dat wij hebben noemt een opleverdatum, dus vragen wij de contractuele datum voor de woning die u kiest.',
  'Arkusz podaje rozpoczęcie i zakończenie budowy jako do potwierdzenia, a żaden posiadany przez nas dokument nie podaje terminu ukończenia, dlatego pytamy o termin umowny dla wybranego przez Pana lub Panią lokalu.',
  'Arket oppgir start og slutt for byggingen som skal bekreftes, og ingen dokumenter vi har oppgir en ferdigstillelsesdato, så vi ber om den kontraktsfestede datoen for boligen De velger.',
  'Bladet anger byggstart och byggslut som att bekräfta, och inget dokument vi har anger ett färdigställandedatum, så vi begär det avtalade datumet för den bostad ni väljer.')
p('.trustDossier.cards[2][1]',
  'La lista de precios y los planos dan las mismas superficies construidas y terrazas cubiertas para las seis viviendas. Los planos dan además superficies útiles menores y, para cada vivienda, un total «según el Decreto 218/2005», por ejemplo {N228.87} {U} para la vivienda 1. Confirmamos qué cifras usa el contrato.',
  'La liste de prix et les plans donnent les mêmes surfaces construites et terrasses couvertes pour les six logements. Les plans donnent en outre des surfaces utiles plus petites et, pour chaque logement, un total « selon le décret 218/2005 », par exemple {N228.87} {U} pour le logement 1. Nous confirmons quels chiffres retient le contrat.',
  'Preisliste und Pläne nennen für die sechs Wohnungen dieselben bebauten Flächen und überdachten Terrassen. Die Pläne geben zusätzlich kleinere Nutzflächen und für jede Wohnung eine Summe „gemäß Dekret 218/2005“, zum Beispiel {N228.87} {U} bei Wohnung 1. Wir bestätigen, welche Zahlen der Vertrag verwendet.',
  'В прайс-листе и на планах для шести объектов указаны одинаковые площади застройки и крытых террас. На планах есть и меньшие полезные площади, а для каждой квартиры — итог «согласно декрету 218/2005», например {N228.87} {U} для квартиры 1. Мы уточняем, какие цифры берёт за основу договор.',
  'تعطي قائمة الأسعار والمخططات المساحات المبنية والتراسات المغطاة نفسها للمساكن الستة. وتعطي المخططات أيضاً مساحات صافية أصغر، ولكل مسكن إجمالياً «وفق المرسوم 218/2005»، مثل {N228.87} {U} للمسكن 1. نؤكد أي الأرقام يعتمدها العقد.',
  'De prijslijst en de plattegronden geven voor de zes woningen dezelfde bebouwde oppervlakten en overdekte terrassen. De plattegronden geven daarnaast kleinere gebruiksoppervlakten en voor elke woning een totaal “volgens Decreet 218/2005”, bijvoorbeeld {N228.87} {U} voor woning 1. Wij bevestigen welke cijfers het contract hanteert.',
  'Cennik i rzuty podają dla sześciu lokali te same powierzchnie zabudowy i zadaszonych tarasów. Rzuty podają ponadto mniejsze powierzchnie użytkowe oraz dla każdego lokalu sumę „zgodnie z dekretem 218/2005”, na przykład {N228.87} {U} dla lokalu 1. Potwierdzamy, jakie liczby przyjmuje umowa.',
  'Prislisten og plantegningene oppgir de samme bebygde arealene og overbygde terrassene for de seks boligene. Plantegningene oppgir i tillegg mindre bruksarealer og, for hver bolig, en sum «i henhold til dekret 218/2005», for eksempel {N228.87} {U} for bolig 1. Vi bekrefter hvilke tall kontrakten bruker.',
  'Prislistan och planritningarna anger samma byggytor och övertäckta terrasser för de sex bostäderna. Planritningarna anger dessutom mindre nyttoytor och, för varje bostad, en summa ”enligt dekret 218/2005”, till exempel {N228.87} {U} för bostad 1. Vi bekräftar vilka siffror avtalet använder.')
p('.trustDossier.cards[3][0]', 'Las viviendas 10 y 15', 'Les logements 10 et 15', 'Die Wohnungen 10 und 15', 'Квартиры 10 и 15', 'المسكنان 10 و15',
  'De woningen 10 en 15', 'Lokale 10 i 15', 'Bolig 10 og 15', 'Bostad 10 och 15')
p('.trustDossier.cards[3][1]',
  'Las viviendas 10 y 15 mostraban un precio en la lista de precios del 6 de mayo de 2026 y no figuran en nuestra lista de disponibilidad del 29 de octubre de 2026, por lo que no se muestran aquí. Confirmamos lo que está disponible antes de que usted decida.',
  'Les logements 10 et 15 affichaient un prix dans la liste de prix du 6 mai 2026 et ne figurent pas dans notre liste de disponibilité du 29 octobre 2026 ; ils ne sont donc pas présentés ici. Nous confirmons ce qui est disponible avant que vous ne décidiez.',
  'Die Wohnungen 10 und 15 hatten in der Preisliste vom 6. Mai 2026 einen Preis und stehen nicht auf unserer Verfügbarkeitsliste vom 29. Oktober 2026; deshalb werden sie hier nicht gezeigt. Wir bestätigen, was verfügbar ist, bevor Sie sich entscheiden.',
  'У квартир 10 и 15 в прайс-листе от 6 мая 2026 года была указана цена, а в нашем списке наличия от 29 октября 2026 года их нет, поэтому здесь они не показаны. Мы подтверждаем, что доступно, прежде чем вы примете решение.',
  'كان للمسكنين 10 و15 سعر في قائمة الأسعار بتاريخ 6 مايو 2026 وهما غير واردين في قائمة التوفر لدينا بتاريخ 29 أكتوبر 2026، لذلك لا يُعرضان هنا. نؤكد المتاح قبل أن تقرروا.',
  'De woningen 10 en 15 hadden een prijs in de prijslijst van 6 mei 2026 en staan niet op onze beschikbaarheidslijst van 29 oktober 2026, dus worden ze hier niet getoond. Wij bevestigen wat beschikbaar is voordat u beslist.',
  'Lokale 10 i 15 miały cenę w cenniku z 6 maja 2026 r. i nie ma ich na naszej liście dostępności z 29 października 2026 r., dlatego nie są tu pokazane. Potwierdzamy, co jest dostępne, zanim Pan lub Pani podejmie decyzję.',
  'Bolig 10 og 15 hadde en pris i prislisten fra 6. mai 2026 og står ikke på vår tilgjengelighetsliste fra 29. oktober 2026, så de vises ikke her. Vi bekrefter hva som er ledig før De bestemmer Dem.',
  'Bostad 10 och 15 hade ett pris i prislistan från den 6 maj 2026 och finns inte i vår tillgänglighetslista från den 29 oktober 2026, så de visas inte här. Vi bekräftar vad som är ledigt innan ni bestämmer er.')

p('.availability.headlineHtml', '6 de 20 viviendas <em>disponibles ahora</em>', '6 logements sur 20 <em>actuellement disponibles</em>', '6 von 20 Wohnungen <em>derzeit verfügbar</em>',
  '6 из 20 квартир <em>доступны сейчас</em>', '6 من 20 مسكناً <em>متاحة حالياً</em>', '6 van de 20 woningen <em>nu beschikbaar</em>', '6 z 20 lokali <em>aktualnie dostępnych</em>',
  '6 av 20 boliger <em>ledige nå</em>', '6 av 20 bostäder <em>lediga nu</em>')
p('.availability.copy',
  'Hay seis viviendas disponibles: cinco apartamentos en la primera planta y un ático. La disponibilidad y los precios son los listados el 29 de octubre de 2026 y se confirman antes de cualquier reserva. Los precios no incluyen IVA.',
  'Six logements sont disponibles : cinq appartements au premier étage et un penthouse. La disponibilité et les prix sont ceux listés le 29 octobre 2026 et sont confirmés avant toute réservation. Les prix s’entendent hors TVA.',
  'Sechs Wohnungen sind verfügbar: fünf Wohnungen im ersten Obergeschoss und ein Penthouse. Verfügbarkeit und Preise entsprechen der Liste vom 29. Oktober 2026 und werden vor jeder Reservierung bestätigt. Die Preise verstehen sich zuzüglich MwSt.',
  'Доступны шесть объектов: пять апартаментов на втором этаже и один пентхаус. Наличие и цены — по списку от 29 октября 2026 года; они подтверждаются до любого бронирования. Цены указаны без НДС.',
  'هناك ستة مساكن متاحة: خمس شقق في الطابق الأول وبنتهاوس واحد. التوفر والأسعار وفق القائمة بتاريخ 29 أكتوبر 2026 وتؤكَّد قبل أي حجز. الأسعار لا تشمل ضريبة القيمة المضافة.',
  'Zes woningen zijn beschikbaar: vijf appartementen op de eerste verdieping en een penthouse. De beschikbaarheid en de prijzen zijn die van de lijst van 29 oktober 2026 en worden vóór elke reservering bevestigd. De prijzen zijn exclusief btw.',
  'Dostępnych jest sześć lokali: pięć apartamentów na pierwszym piętrze i jeden penthouse. Dostępność i ceny są zgodne z listą z 29 października 2026 r. i są potwierdzane przed każdą rezerwacją. Ceny nie zawierają VAT.',
  'Seks boliger er ledige: fem leiligheter i andre etasje og én toppleilighet. Tilgjengelighet og priser er som oppført 29. oktober 2026 og bekreftes før enhver reservasjon. Prisene er eksklusive mva.',
  'Sex bostäder är lediga: fem lägenheter på första våningen och en takvåning. Tillgänglighet och priser är de som listades den 29 oktober 2026 och bekräftas före varje bokning. Priserna är exklusive IVA.')
p('.availability.sourceNote',
  'Los precios, dormitorios, superficies construidas, terrazas y plazas de garaje se transcriben de la lista de precios del promotor con fecha del 6 de mayo de 2026, y las seis viviendas mostradas son las de nuestra lista de disponibilidad del 29 de octubre de 2026, que da los mismos precios. La lista de precios marca 12 de las 20 viviendas como reservadas y mostraba precio para otras dos, las viviendas 10 y 15, que la lista posterior no muestra como disponibles. La lista indica que los precios son netos y no incluyen IVA, sin dar el tipo. La superficie construida es la superficie construida interior y la terraza es la terraza cubierta sobre base construida, como en los planos; los planos dan además superficies útiles. En el ático 12 el solárium reúne las zonas cubierta y descubierta de la azotea. Los planos son los del promotor, versión del 14 de abril de 2026.',
  'Les prix, chambres, surfaces construites, terrasses et places de garage sont transcrits de la liste de prix du promoteur datée du 6 mai 2026, et les six logements présentés sont ceux de notre liste de disponibilité du 29 octobre 2026, qui donne les mêmes prix. La liste de prix marque 12 des 20 logements comme réservés et affichait un prix pour deux autres, les logements 10 et 15, que la liste plus récente ne présente pas comme disponibles. La liste indique que les prix sont nets et n’incluent pas la TVA, sans en donner le taux. La surface construite est la surface construite intérieure et la terrasse est la terrasse couverte sur base construite, comme sur les plans ; les plans donnent en outre des surfaces utiles. Pour le penthouse 12, le solarium réunit les zones couverte et découverte du toit. Les plans sont ceux du promoteur, version du 14 avril 2026.',
  'Preise, Schlafzimmer, bebaute Flächen, Terrassen und Garagenstellplätze sind aus der Preisliste des Bauträgers vom 6. Mai 2026 übernommen, und die sechs gezeigten Wohnungen sind die auf unserer Verfügbarkeitsliste vom 29. Oktober 2026, die dieselben Preise nennt. Die Preisliste kennzeichnet 12 der 20 Wohnungen als reserviert und zeigte Preise für zwei weitere, die Wohnungen 10 und 15, die die spätere Liste nicht als verfügbar ausweist. Die Liste gibt an, dass die Preise netto sind und keine MwSt. enthalten, ohne den Satz zu nennen. Die bebaute Fläche ist die bebaute Innenfläche, und die Terrasse ist die überdachte Terrasse auf bebauter Basis, wie in den Plänen; die Pläne nennen zusätzlich Nutzflächen. Beim Penthouse 12 umfasst das Solarium die überdachten und die unüberdachten Dachflächen zusammen. Die Pläne sind die des Bauträgers, Stand 14. April 2026.',
  'Цены, спальни, площади застройки, террасы и места в гараже перенесены из прайс-листа застройщика от 6 мая 2026 года, а показанные шесть объектов — те, что значатся в нашем списке наличия от 29 октября 2026 года, где цены те же. В прайс-листе 12 из 20 квартир отмечены как забронированные и были указаны цены ещё для двух — квартир 10 и 15, которых в более позднем списке нет среди доступных. В списке сказано, что цены указаны нетто и не включают НДС, ставка не названа. Площадь застройки — это застроенная площадь внутри, а терраса — крытая терраса в застроенных площадях, как на планах; на планах есть и полезные площади. У пентхауса 12 солярий — это крытая и открытая зоны крыши вместе. Планы — застройщика, версия от 14 апреля 2026 года.',
  'الأسعار وغرف النوم والمساحات المبنية والتراسات ومواقف المرآب منقولة من قائمة أسعار المطوّر المؤرخة في 6 مايو 2026، والمساكن الستة المعروضة هي الواردة في قائمة التوفر لدينا بتاريخ 29 أكتوبر 2026 التي تعطي الأسعار نفسها. تضع قائمة الأسعار 12 من المساكن العشرين في خانة المحجوزة وكانت تعرض سعراً لمسكنين آخرين هما 10 و15 لا تعرضهما القائمة الأحدث متاحين. وتذكر القائمة أن الأسعار صافية ولا تشمل ضريبة القيمة المضافة دون ذكر النسبة. المساحة المبنية هي المساحة الداخلية المبنية، والتراس هو التراس المغطى على أساس المساحة المبنية، كما في المخططات؛ وتعطي المخططات أيضاً مساحات صافية. وفي البنتهاوس 12 يجمع السولاريوم منطقتي السطح المغطاة والمكشوفة معاً. المخططات هي مخططات المطوّر، إصدار 14 أبريل 2026.',
  'De prijzen, slaapkamers, bebouwde oppervlakten, terrassen en garageplaatsen zijn overgenomen uit de prijslijst van de ontwikkelaar van 6 mei 2026, en de zes getoonde woningen zijn die van onze beschikbaarheidslijst van 29 oktober 2026, die dezelfde prijzen geeft. De prijslijst markeert 12 van de 20 woningen als gereserveerd en toonde prijzen voor twee andere, de woningen 10 en 15, die de latere lijst niet als beschikbaar toont. De lijst vermeldt dat de prijzen netto zijn en geen btw bevatten, zonder het tarief te noemen. De bebouwde oppervlakte is de bebouwde binnenoppervlakte en het terras is het overdekte terras op bebouwde basis, zoals op de plattegronden; de plattegronden geven daarnaast gebruiksoppervlakten. Bij penthouse 12 omvat het solarium de overdekte en de onoverdekte dakzones samen. De plattegronden zijn die van de ontwikkelaar, versie van 14 april 2026.',
  'Ceny, sypialnie, powierzchnie zabudowy, tarasy i miejsca garażowe zostały przepisane z cennika dewelopera z datą 6 maja 2026 r., a pokazane sześć lokali to te z naszej listy dostępności z 29 października 2026 r., która podaje te same ceny. Cennik oznacza 12 z 20 lokali jako zarezerwowane i pokazywał ceny dla dwóch kolejnych, lokali 10 i 15, których późniejsza lista nie wskazuje jako dostępnych. Cennik podaje, że ceny są cenami netto i nie zawierają VAT, bez podania stawki. Powierzchnia zabudowy to zabudowana powierzchnia wewnętrzna, a taras to taras zadaszony w ujęciu powierzchni zabudowy, jak na rzutach; rzuty podają ponadto powierzchnie użytkowe. W penthouse’ie 12 solarium obejmuje razem zadaszone i odkryte części dachu. Rzuty są rzutami dewelopera, wersja z 14 kwietnia 2026 r.',
  'Prisene, soverommene, de bebygde arealene, terrassene og garasjeplassene er overført fra utbyggerens prisliste datert 6. mai 2026, og de seks viste boligene er de på vår tilgjengelighetsliste fra 29. oktober 2026, som oppgir de samme prisene. Prislisten markerer 12 av de 20 boligene som reservert og viste pris for to til, bolig 10 og 15, som den senere listen ikke viser som ledige. Listen oppgir at prisene er netto og ikke inkluderer mva., uten å oppgi satsen. Det bebygde arealet er det bebygde innvendige arealet, og terrassen er den overbygde terrassen på bebygd grunnlag, som på plantegningene; plantegningene oppgir i tillegg bruksarealer. For toppleilighet 12 omfatter solterrassen de overbygde og åpne takarealene til sammen. Plantegningene er utbyggerens, versjon av 14. april 2026.',
  'Priserna, sovrummen, byggytorna, terrasserna och garageplatserna är hämtade från exploatörens prislista daterad den 6 maj 2026, och de sex visade bostäderna är de i vår tillgänglighetslista från den 29 oktober 2026, som anger samma priser. Prislistan markerar 12 av de 20 bostäderna som reserverade och visade pris för ytterligare två, bostad 10 och 15, som den senare listan inte visar som lediga. Listan anger att priserna är nettopriser och inte inkluderar IVA, utan att ange satsen. Byggytan är den byggda inomhusytan och terrassen är den övertäckta terrassen på byggytebasis, som på planritningarna; planritningarna anger dessutom nyttoytor. För takvåning 12 omfattar solterrassen de övertäckta och öppna takytorna tillsammans. Planritningarna är exploatörens, version av den 14 april 2026.')

# ---- timeline, viewing, enquiry, FAQ ----------------------------------------------------------------------
p('.timeline.items[2][2]',
  'Vea la parcela y la zona con nosotros, y los planos frente al estado de las licencias.',
  'Voyez la parcelle et le quartier avec nous, et les plans au regard de l’état des permis.',
  'Sehen Sie sich mit uns das Grundstück und die Umgebung an, dazu die Pläne im Verhältnis zum Stand der Genehmigungen.',
  'Посмотрите участок и окрестности вместе с нами, а планировки — с учётом статуса разрешений.',
  'شاهدوا معنا الأرض والمنطقة، والمخططات مقابل حالة الرخص.',
  'Bekijk met ons het perceel en de omgeving, en de plattegronden naast de stand van de vergunningen.',
  'Proszę obejrzeć z nami działkę i okolicę oraz rzuty w zestawieniu ze stanem pozwoleń.',
  'Se tomten og området sammen med oss, og plantegningene opp mot status for tillatelsene.',
  'Se tomten och området tillsammans med oss, och planritningarna mot status för tillstånden.')
p('.timeline.items[3][2]',
  'Confirmamos por escrito el precio, el estado de las licencias y la fecha de finalización antes de cualquier reserva.',
  'Nous confirmons par écrit le prix, l’état des permis et la date d’achèvement avant toute réservation.',
  'Wir bestätigen Preis, Stand der Genehmigungen und Fertigstellungstermin schriftlich vor jeder Reservierung.',
  'Мы письменно подтверждаем цену, статус разрешений и срок завершения до любого бронирования.',
  'نؤكد كتابةً السعر وحالة الرخص وموعد الإنجاز قبل أي حجز.',
  'Wij bevestigen de prijs, de stand van de vergunningen en de opleverdatum schriftelijk vóór elke reservering.',
  'Przed każdą rezerwacją potwierdzamy na piśmie cenę, stan pozwoleń i termin ukończenia.',
  'Vi bekrefter prisen, status for tillatelsene og ferdigstillelsesdatoen skriftlig før enhver reservasjon.',
  'Vi bekräftar priset, status för tillstånden och färdigställandedatumet skriftligen före varje bokning.')
p('.privateViewing.copy',
  'El edificio aún no está construido, así que una visita trata de la ubicación, los planos y el estado de las licencias.',
  'L’immeuble n’est pas encore construit ; une visite porte donc sur l’emplacement, les plans et l’état des permis.',
  'Das Gebäude ist noch nicht gebaut, daher geht es bei einem Besuch um die Lage, die Pläne und den Stand der Genehmigungen.',
  'Здание ещё не построено, поэтому визит посвящён расположению, планировкам и статусу разрешений.',
  'المبنى لم يُبنَ بعد، لذلك تدور الزيارة حول الموقع والمخططات وحالة الرخص.',
  'Het gebouw is nog niet gebouwd, dus een bezoek gaat over de ligging, de plattegronden en de stand van de vergunningen.',
  'Budynek jeszcze nie powstał, więc wizyta dotyczy lokalizacji, rzutów i stanu pozwoleń.',
  'Bygningen er ikke bygget ennå, så et besøk handler om beliggenheten, plantegningene og status for tillatelsene.',
  'Byggnaden är inte byggd ännu, så ett besök handlar om läget, planritningarna och status för tillstånden.')
p('.privateViewing.insights[0][1]',
  'Vea la parcela frente a la carretera costera y dónde está la playa.',
  'Voyez la parcelle face à la route côtière et où se trouve la plage.',
  'Sehen Sie das Grundstück an der Küstenstraße und wo der Strand liegt.',
  'Увидьте участок напротив прибрежной дороги и где находится пляж.',
  'شاهدوا الأرض المقابلة للطريق الساحلي وموقع الشاطئ.',
  'Zie het perceel tegenover de kustweg en waar het strand ligt.',
  'Proszę zobaczyć działkę przy drodze nadmorskiej i gdzie leży plaża.',
  'Se tomten ved kystveien og hvor stranden ligger.',
  'Se tomten vid kustvägen och var stranden ligger.')
p('.privateViewing.insights[1][1]',
  'Conducimos con usted hasta el centro de Estepona y hasta Marbella y cronometramos el trayecto.',
  'Nous vous conduisons jusqu’au centre d’Estepona et à Marbella et chronométrons le trajet.',
  'Wir fahren mit Ihnen ins Zentrum von Estepona und nach Marbella und stoppen die Fahrzeit.',
  'Мы проезжаем с вами до центра Эстепоны и до Марбельи и засекаем время в пути.',
  'نقود معكم إلى مركز إستيبونا وإلى ماربيا ونحتسب زمن الرحلة.',
  'Wij rijden met u naar het centrum van Estepona en naar Marbella en meten de reistijd.',
  'Jedziemy z Panem lub Panią do centrum Estepony i do Marbelli i mierzymy czas przejazdu.',
  'Vi kjører med Dem til sentrum av Estepona og til Marbella og tar tiden.',
  'Vi kör med er till centrala Estepona och till Marbella och tar tiden.')
p('.privateViewing.insights[2][1]',
  'Licencias, fecha de finalización y contrato, antes de firmar nada.',
  'Permis, date d’achèvement et contrat, avant toute signature.',
  'Genehmigungen, Fertigstellungstermin und Vertrag, bevor etwas unterzeichnet wird.',
  'Разрешения, срок завершения и договор — до того, как что-либо подписано.',
  'الرخص وموعد الإنجاز والعقد، قبل توقيع أي شيء.',
  'Vergunningen, opleverdatum en contract, voordat er iets wordt ondertekend.',
  'Pozwolenia, termin ukończenia i umowa — zanim cokolwiek zostanie podpisane.',
  'Tillatelser, ferdigstillelsesdato og kontrakt, før noe signeres.',
  'Tillstånd, färdigställandedatum och avtal, innan något skrivs under.')
p('.enquiry.headlineHtml', 'Pregunte por <em>Nacare</em>', 'Renseignez-vous sur <em>Nacare</em>', 'Fragen Sie nach <em>Nacare</em>', 'Узнайте о <em>Nacare</em>',
  'اسألوا عن <em>Nacare</em>', 'Vraag naar <em>Nacare</em>', 'Zapytaj o <em>Nacare</em>', 'Spør om <em>Nacare</em>', 'Fråga om <em>Nacare</em>')
p('.enquiry.message',
  'Hola Nueva Living, me gustaría recibir información sobre Nacare.',
  'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Nacare.',
  'Hallo Nueva Living, ich hätte gern Informationen zu Nacare.',
  'Здравствуйте, Nueva Living! Я хотел бы получить информацию о Nacare.',
  'مرحباً Nueva Living، أودّ الحصول على معلومات عن Nacare.',
  'Hallo Nueva Living, ik zou graag informatie ontvangen over Nacare.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Nacare.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Nacare.',
  'Hej Nueva Living, jag skulle vilja ha information om Nacare.')
p('.faq[0][1]',
  'El edificio tiene 20 viviendas y seis están disponibles ahora: una de cuatro dormitorios y cinco de tres, de {E2500000} a {E4800000} más IVA.',
  'L’immeuble compte 20 logements et six sont actuellement disponibles : un de quatre chambres et cinq de trois chambres, de {E2500000} à {E4800000} hors TVA.',
  'Das Gebäude hat 20 Wohnungen, und sechs sind derzeit verfügbar: eine mit vier und fünf mit drei Schlafzimmern, von {E2500000} bis {E4800000} zuzüglich MwSt.',
  'В здании 20 квартир, сейчас доступны шесть: одна с четырьмя спальнями и пять с тремя, от {E2500000} до {E4800000} без НДС.',
  'يضم المبنى 20 مسكناً، وستة منها متاحة حالياً: مسكن واحد بأربع غرف نوم وخمسة بثلاث غرف نوم، من {E2500000} إلى {E4800000} دون ضريبة القيمة المضافة.',
  'Het gebouw heeft 20 woningen en zes zijn nu beschikbaar: één met vier slaapkamers en vijf met drie, van {E2500000} tot {E4800000} excl. btw.',
  'Budynek ma 20 lokali, a sześć jest obecnie dostępnych: jeden z czterema sypialniami i pięć z trzema, od {E2500000} do {E4800000} plus VAT.',
  'Bygningen har 20 boliger, og seks er ledige nå: én med fire soverom og fem med tre, fra {E2500000} til {E4800000} pluss mva.',
  'Byggnaden har 20 bostäder och sex är lediga nu: en med fyra sovrum och fem med tre, från {E2500000} till {E4800000} plus IVA.')
p('.faq[1][1]',
  'No. La lista de precios indica que los precios son netos y no incluyen el IVA, y no da el tipo. Confirmamos por escrito el tipo y los demás gastos de compra.',
  'Non. La liste de prix indique que les prix sont nets et n’incluent pas la TVA, et elle n’en donne pas le taux. Nous confirmons par écrit le taux et les autres frais d’achat.',
  'Nein. Laut Preisliste sind die Preise netto und enthalten keine MwSt., und sie nennt den Satz nicht. Wir bestätigen den Satz und die übrigen Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе сказано, что цены указаны нетто и не включают НДС, а ставка не названа. Мы письменно подтверждаем ставку и остальные расходы на покупку.',
  'لا. تذكر قائمة الأسعار أن الأسعار صافية ولا تشمل ضريبة القيمة المضافة، ولا تذكر النسبة. نؤكد كتابةً النسبة وباقي مصاريف الشراء.',
  'Nee. De prijslijst vermeldt dat de prijzen netto zijn en geen btw bevatten, en ze geeft het tarief niet. Wij bevestigen het tarief en de overige aankoopkosten schriftelijk.',
  'Nie. Cennik wskazuje, że ceny są cenami netto i nie zawierają VAT, i nie podaje stawki. Potwierdzamy na piśmie stawkę i pozostałe koszty zakupu.',
  'Nei. Prislisten oppgir at prisene er netto og ikke inkluderer mva., og den oppgir ikke satsen. Vi bekrefter satsen og de øvrige kjøpskostnadene skriftlig.',
  'Nej. Prislistan anger att priserna är nettopriser och inte inkluderar IVA (spansk moms), och den anger inte satsen. Vi bekräftar satsen och de övriga köpkostnaderna skriftligen.')
p('.faq[2][1]',
  'Sí. La lista de precios asigna a cada vivienda plazas de garaje: dos para las viviendas 1, 5, 9 y 13, tres para la vivienda 17 y cuatro para el ático 12.',
  'Oui. La liste de prix attribue à chaque logement des places de garage : deux pour les logements 1, 5, 9 et 13, trois pour le logement 17 et quatre pour le penthouse 12.',
  'Ja. Die Preisliste weist jeder Wohnung Garagenstellplätze zu: zwei bei den Wohnungen 1, 5, 9 und 13, drei bei Wohnung 17 und vier beim Penthouse 12.',
  'Да. По прайс-листу к каждому объекту относятся места в гараже: два у квартир 1, 5, 9 и 13, три у квартиры 17 и четыре у пентхауса 12.',
  'نعم. تمنح قائمة الأسعار كل مسكن مواقف في المرآب: موقفين للمساكن 1 و5 و9 و13، وثلاثة للمسكن 17، وأربعة للبنتهاوس 12.',
  'Ja. De prijslijst kent elke woning garageplaatsen toe: twee bij de woningen 1, 5, 9 en 13, drie bij woning 17 en vier bij penthouse 12.',
  'Tak. Cennik przypisuje każdemu lokalowi miejsca garażowe: dwa w lokalach 1, 5, 9 i 13, trzy w lokalu 17 i cztery w penthouse’ie 12.',
  'Ja. Prislisten gir hver bolig garasjeplasser: to for bolig 1, 5, 9 og 13, tre for bolig 17 og fire for toppleilighet 12.',
  'Ja. Prislistan ger varje bostad garageplatser: två för bostad 1, 5, 9 och 13, tre för bostad 17 och fyra för takvåning 12.')
p('.faq[3][1]',
  'Ningún documento que tenemos da una fecha. La ficha del promotor marca la licencia de obras y la licencia de primera ocupación como pendientes y el inicio y el fin de la construcción como por confirmar. Pedimos la fecha contractual y la ponemos por escrito.',
  'Aucun document en notre possession ne donne de date. La fiche du promoteur indique que le permis de construire et la licence de première occupation sont en attente et que le début et la fin des travaux restent à confirmer. Nous demandons la date contractuelle et la mettons par écrit.',
  'Kein Dokument, das uns vorliegt, nennt ein Datum. Das Datenblatt des Bauträgers kennzeichnet die Baugenehmigung und die Erstbezugsgenehmigung als ausstehend und Baubeginn und Bauende als noch zu bestätigen. Wir fragen den vertraglichen Termin ab und halten ihn schriftlich fest.',
  'Ни в одном имеющемся у нас документе даты нет. В справке застройщика разрешение на строительство и лицензия на первое заселение отмечены как ожидаемые, а начало и окончание строительства — как подлежащие уточнению. Мы запрашиваем договорный срок и фиксируем его письменно.',
  'لا يذكر أي مستند لدينا موعداً. تضع ورقة المطوّر رخصة البناء ورخصة الإشغال الأول في خانة قيد الانتظار، وبدء البناء وانتهاءه في خانة سيُؤكَّدان لاحقاً. نطلب الموعد التعاقدي ونثبّته كتابةً.',
  'Geen enkel document dat wij hebben noemt een datum. Het informatieblad van de ontwikkelaar markeert de bouwvergunning en de vergunning voor eerste ingebruikname als in afwachting en de start en het einde van de bouw als nog te bevestigen. Wij vragen de contractuele datum en leggen die schriftelijk vast.',
  'Żaden posiadany przez nas dokument nie podaje daty. Arkusz dewelopera oznacza pozwolenie na budowę i pozwolenie na pierwsze zasiedlenie jako oczekujące, a rozpoczęcie i zakończenie budowy jako do potwierdzenia. Pytamy o termin umowny i spisujemy go na piśmie.',
  'Ingen dokumenter vi har oppgir en dato. Utbyggerens ark markerer byggetillatelsen og brukstillatelsen som ikke på plass og start og slutt for byggingen som skal bekreftes. Vi ber om den kontraktsfestede datoen og setter den skriftlig.',
  'Inget dokument vi har anger ett datum. Exploatörens blad markerar bygglovet och tillståndet för första ibruktagande som ännu inte på plats och byggstart och byggslut som att bekräfta. Vi begär det avtalade datumet och sätter det skriftligen.')
p('.faq[4][0]', '¿Qué ofrece el edificio?', 'Qu’offre l’immeuble ?', 'Was bietet das Gebäude?', 'Что предлагает здание?', 'ماذا يقدّم المبنى؟',
  'Wat biedt het gebouw?', 'Co oferuje budynek?', 'Hva tilbyr bygningen?', 'Vad erbjuder byggnaden?')
p('.faq[4][1]',
  'El folleto enumera un spa, una piscina interior climatizada, salas de masajes y de belleza, un gimnasio y una sala polivalente, un salón y bar para propietarios, una sala de reuniones, una skypool y un salón en la azotea, y jardines paisajísticos. Preguntamos qué servicios están incluidos y cuáles se cobran aparte.',
  'La brochure énumère un spa, une piscine intérieure chauffée, des salles de massage et de beauté, une salle de sport et une salle polyvalente, un salon et un bar pour les propriétaires, une salle de réunion, une skypool et un salon sur le toit, ainsi que des jardins paysagers. Nous demandons quels services sont inclus et lesquels sont facturés.',
  'Die Broschüre führt ein Spa, einen beheizten Innenpool, Massage- und Beautyräume, einen Fitnessraum mit Mehrzweckfläche, eine Eigentümerlounge mit Bar, einen Besprechungsraum, einen Skypool und eine Dachlounge sowie angelegte Gärten auf. Wir fragen nach, welche Leistungen inbegriffen sind und welche berechnet werden.',
  'В брошюре перечислены спа, подогреваемый крытый бассейн, массажные и косметические кабинеты, тренажёрный зал с многофункциональным залом, лаунж с баром для владельцев, переговорная, скайпул и лаунж на крыше, а также ландшафтные сады. Мы уточняем, какие услуги включены, а какие оплачиваются отдельно.',
  'يذكر الكتيّب سباً ومسبحاً داخلياً مدفأً وغرف مساج وتجميل وصالة رياضية وقاعة متعددة الاستخدامات وصالة وبار للملاك وقاعة اجتماعات ومسبح سكاي وصالة على السطح وحدائق منسّقة. نسأل عن الخدمات المشمولة وتلك التي تُحتسب بمقابل.',
  'De brochure noemt een spa, een verwarmd binnenzwembad, massage- en schoonheidsruimtes, een fitnessruimte met flexruimte, een lounge met bar voor de eigenaren, een vergaderruimte, een skypool en een lounge op het dak, en aangelegde tuinen. Wij vragen welke diensten inbegrepen zijn en welke worden doorberekend.',
  'Broszura wymienia spa, podgrzewany basen wewnętrzny, gabinety masażu i kosmetyczne, siłownię z salą wielofunkcyjną, salon z barem dla właścicieli, salę spotkań, skypool i lounge na dachu oraz ogrody krajobrazowe. Pytamy, które usługi są wliczone, a które płatne dodatkowo.',
  'Brosjyren nevner et spa, et oppvarmet innendørsbasseng, masasje- og skjønnhetsrom, et treningsrom med fleksirom, en eierlounge med bar, et møterom, en skypool og en lounge på taket, og opparbeidede hager. Vi spør hvilke tjenester som er inkludert og hvilke som betales ekstra.',
  'Broschyren nämner ett spa, en uppvärmd inomhuspool, massage- och skönhetsrum, ett gym med flexyta, en ägarlounge med bar, ett mötesrum, en skypool och en lounge på taket, och anlagda trädgårdar. Vi frågar vilka tjänster som ingår och vilka som debiteras.')

# ---- SEO --------------------------------------------------------------------------------------------------
p('.seo.title',
  'Nacare - Apartamentos y áticos nuevos en Estepona', 'Nacare - Appartements et penthouses neufs à Estepona', 'Nacare - Neubauwohnungen und Penthäuser in Estepona',
  'Nacare - новые апартаменты и пентхаусы в Эстепоне', 'Nacare - شقق وبنتهاوس جديدة في إستيبونا', 'Nacare - Nieuwbouwappartementen en penthouses in Estepona',
  'Nacare - Nowe apartamenty i penthouse’y w Esteponie', 'Nacare - Nye leiligheter og toppleiligheter i Estepona', 'Nacare - Nya lägenheter och takvåningar i Estepona')
p('.seo.h1',
  'Nacare: apartamentos y áticos amplios con vistas al mar en Estepona', 'Nacare : grands appartements et penthouses avec vue sur la mer à Estepona',
  'Nacare: große Wohnungen und Penthäuser mit Meerblick in Estepona', 'Nacare: просторные апартаменты и пентхаусы с видом на море в Эстепоне',
  'Nacare: شقق وبنتهاوس واسعة بإطلالة على البحر في إستيبونا', 'Nacare: ruime appartementen en penthouses met zeezicht in Estepona',
  'Nacare: duże apartamenty i penthouse’y z widokiem na morze w Esteponie', 'Nacare: store leiligheter og toppleiligheter med utsikt over havet i Estepona',
  'Nacare: stora lägenheter och takvåningar med havsutsikt i Estepona')
p('.seo.h1Context',
  'Apartamentos y áticos amplios con vistas al mar en Estepona', 'Grands appartements et penthouses avec vue sur la mer à Estepona',
  'Große Wohnungen und Penthäuser mit Meerblick in Estepona', 'Просторные апартаменты и пентхаусы с видом на море в Эстепоне',
  'شقق وبنتهاوس واسعة بإطلالة على البحر في إستيبونا', 'Ruime appartementen en penthouses met zeezicht in Estepona',
  'Duże apartamenty i penthouse’y z widokiem na morze w Esteponie', 'Store leiligheter og toppleiligheter med utsikt over havet i Estepona',
  'Stora lägenheter och takvåningar med havsutsikt i Estepona')

# ---- unit sizes and plan alts/captions, from templates -----------------------------------------------------
proj = json.load(open('content/liora-projects/nacare/project.json'))
SIZE = {
    'es': ('{b} {U} construidos', '{t} {U} de terraza', '{s} {U} de solárium'),
    'fr': ('{b} {U} construits', '{t} {U} de terrasse', '{s} {U} de solarium'),
    'de': ('{b} {U} bebaut', '{t} {U} Terrasse', '{s} {U} Solarium'),
    'ru': ('{b} {U} застроенной площади', 'терраса {t} {U}', 'солярий {s} {U}'),
    'ar': ('{b} {U} مبنية', '{t} {U} تراس', '{s} {U} سولاريوم'),
    'nl': ('{b} {U} bebouwd', '{t} {U} terras', '{s} {U} solarium'),
    'pl': ('{b} {U} zabudowy', '{t} {U} tarasu', '{s} {U} solarium'),
    'no': ('{b} {U} bebygd', '{t} {U} terrasse', '{s} {U} solterrasse'),
    'sv': ('{b} {U} byggyta', '{t} {U} terrass', '{s} {U} solterrass'),
}
for u in proj['availability']['units']:
    if u['reference'] not in T:
        T[u['reference']] = {l: u['reference'] for l in LOCS}
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm solarium)?', u['size'])
    assert m, u['size']
    b, t, s = m.groups()
    out = []
    for l in LOCS:
        parts = [SIZE[l][0].format(b='{N%s}' % b, U='{U}'), SIZE[l][1].format(t='{N%s}' % t, U='{U}')]
        if s:
            parts.append(SIZE[l][2].format(s='{N%s}' % s, U='{U}'))
        out.append(expand(('، ' if l == 'ar' else ', ').join(parts), l))
    T[u['size']] = dict(zip(LOCS, out))

HOME = {'es': 'Vivienda', 'fr': 'Logement', 'de': 'Wohnung', 'ru': 'Квартира', 'ar': 'المسكن', 'nl': 'Woning', 'pl': 'Lokal', 'no': 'Bolig', 'sv': 'Bostad'}
PLAN = {'es': 'Plano de la vivienda', 'fr': 'Plan du logement', 'de': 'Grundriss der Wohnung', 'ru': 'Планировка квартиры', 'ar': 'مخطط المسكن',
        'nl': 'Plattegrond van woning', 'pl': 'Rzut lokalu', 'no': 'Plantegning av bolig', 'sv': 'Planritning för bostad'}
for it in proj['media']['items']:
    if it.get('category') != 'Floorplans':
        continue
    m = re.fullmatch(r'Home (\d+)', it['caption'])
    ref = m.group(1)
    T[it['caption']] = {l: f'{HOME[l]} {ref}' for l in LOCS}
    T[it['alt']] = {l: f'{PLAN[l]} {ref}' for l in LOCS}

if SKIPPED:
    print('SKIPPED (already in the translation memory):', SKIPPED)
if BAD:
    print('WRONG ARG COUNT', BAD)
# ---- two shared strings whose translation-memory wording was written for houses ---------------------------------
T['The plans of the homes that interest you and the price list.'] = dict(zip(LOCS, [
    'Los planos de las viviendas que le interesen y la lista de precios.',
    'Les plans des logements qui vous intéressent et la liste de prix.',
    'Die Pläne der Wohnungen, die Sie interessieren, und die Preisliste.',
    'Планировки интересующих вас квартир и прайс-лист.',
    'مخططات المساكن التي تهمكم وقائمة الأسعار.',
    'De plattegronden van de woningen die u interesseren en de prijslijst.',
    'Rzuty interesujących Państwa lokali i cennik.',
    'Plantegningene av boligene som interesserer Dem, og prislisten.',
    'Planritningarna för de bostäder som intresserar er och prislistan.']))
T['The penthouse'] = dict(zip(LOCS, ['El ático', 'Le penthouse', 'Das Penthouse', 'Пентхаус', 'البنتهاوس', 'Het penthouse', 'Penthouse', 'Toppleiligheten', 'Takvåningen']))

missing = [path for path in BY_PATH if path not in USED and BY_PATH[path] not in T]
if missing:
    print('NOT COVERED', len(missing))
    for path in missing:
        print('  ', path, '|', BY_PATH[path][:90])
json.dump(T, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
