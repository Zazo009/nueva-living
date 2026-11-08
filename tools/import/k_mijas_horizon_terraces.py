# -*- coding: utf-8 -*-
"""Mijas Horizon Terraces: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E492000}
money, {N88.4} decimal number, {U} the area unit, {D5.3.2027} a date, {T} the local tax word.
    python3 tools/import/k_mijas_horizon_terraces.py <scratch dir>   (writes <dir>/tr_a.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
# The tax word in running text. Swedish glosses it once, in the first sentence that names it.
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة', 'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
# ... and after a price, where Norwegian carries the full stop (as the Arosa overlay does).
TAXP = dict(TAXW); TAXP['no'] = 'mva.'
FROM = {'es': 'Desde {}', 'fr': 'À partir de {}', 'de': 'Ab {}', 'ru': 'От {}', 'ar': 'ابتداءً من {}',
        'nl': 'Vanaf {}', 'pl': 'Od {}', 'no': 'Fra {}', 'sv': 'Från {}'}
MONTHS = {
    3: dict(es='marzo', fr='mars', de='März', ru='марта', ar='مارس', nl='maart', pl='marca', no='mars', sv='mars'),
    4: dict(es='abril', fr='avril', de='April', ru='апреля', ar='أبريل', nl='april', pl='kwietnia', no='april', sv='april'),
    9: dict(es='septiembre', fr='septembre', de='September', ru='сентября', ar='سبتمبر', nl='september', pl='września', no='september', sv='september'),
    10: dict(es='octubre', fr='octobre', de='Oktober', ru='октября', ar='أكتوبر', nl='oktober', pl='października', no='oktober', sv='oktober'),
}
T = {}
proj = json.load(open('content/liora-projects/mijas-horizon-terraces/project.json'))
tm = json.load(open(f'{SP}/tm.json'))


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def date(d, m, y, l):
    mo = MONTHS[m][l]
    return {'es': f'{d} de {mo} de {y}', 'fr': f'{d} {mo} {y}', 'de': f'{d}. {mo} {y}', 'ru': f'{d} {mo} {y} года',
            'ar': f'{d} {mo} {y}', 'nl': f'{d} {mo} {y}', 'pl': f'{d} {mo} {y} roku', 'no': f'{d}. {mo} {y}',
            'sv': f'{d} {mo} {y}'}[l]


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    text = re.sub(r'\{D(\d+)\.(\d+)\.(\d+)\}', lambda m: date(m.group(1), int(m.group(2)), m.group(3), l), text)
    text = re.sub(r'\{P(\d+)\}', lambda m: money(int(m.group(1)), l) + ' + ' + TAXP[l], text)
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


# Names and the developer's own unit codes read the same in every language.
same('Mijas Horizon Terraces'); same('Mijas Horizon <em>Terraces</em>')
for u in proj['availability']['units']:
    same(u['reference'])

# ---- description, SEO, card ------------------------------------------------------------------

a('.description',
  'Seis de las 19 viviendas de la lista de precios de Mijas Horizon Terraces, una promoción de 142 apartamentos y áticos de dos y tres dormitorios en Mijas Costa, están disponibles, desde {E320000} más IVA. Las condiciones de pago sitúan la escritura en el primer trimestre de 2029.',
  'Six des 19 logements de la liste de prix de Mijas Horizon Terraces, un programme de 142 appartements et penthouses de deux et trois chambres à Mijas Costa, sont disponibles, à partir de {E320000} hors TVA. Les conditions de paiement placent l’acte authentique au premier trimestre 2029.',
  'Sechs der 19 Wohnungen auf der Preisliste von Mijas Horizon Terraces, einer Anlage mit 142 Wohnungen und Penthäusern mit zwei und drei Schlafzimmern in Mijas Costa, sind verfügbar, ab {E320000} zuzüglich MwSt. Die Zahlungsbedingungen setzen die Beurkundung auf das erste Quartal 2029.',
  'Шесть из 19 квартир в прайс-листе Mijas Horizon Terraces — комплекса из 142 квартир и пентхаусов с двумя и тремя спальнями в Михас-Коста — доступны, от {E320000} плюс НДС. По условиям оплаты оформление права собственности у нотариуса намечено на первый квартал 2029 года.',
  'ست من 19 مسكنًا في قائمة أسعار Mijas Horizon Terraces، وهو مشروع من 142 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم في ميخاس كوستا، متاحة، ابتداءً من {E320000} زائد ضريبة القيمة المضافة. وتحدد شروط الدفع موعد سند الملكية في الربع الأول من 2029.',
  'Zes van de 19 woningen op de prijslijst van Mijas Horizon Terraces, een ontwikkeling van 142 appartementen en penthouses met twee en drie slaapkamers in Mijas Costa, zijn beschikbaar, vanaf {E320000} plus btw. De betalingsvoorwaarden plaatsen de notariële akte in het eerste kwartaal van 2029.',
  'Sześć z 19 lokali z cennika Mijas Horizon Terraces, inwestycji obejmującej 142 apartamenty i penthouse’y z dwiema i trzema sypialniami w Mijas Costa, jest dostępnych, od {E320000} plus VAT. Warunki płatności wskazują akt notarialny w pierwszym kwartale 2029 roku.',
  'Seks av de 19 boligene på prislisten for Mijas Horizon Terraces, et prosjekt med 142 leiligheter og toppleiligheter med to og tre soverom i Mijas Costa, er tilgjengelige, fra {E320000} pluss mva. Betalingsvilkårene legger skjøtet til første kvartal 2029.',
  'Sex av de 19 bostäderna på prislistan för Mijas Horizon Terraces, ett projekt med 142 lägenheter och takvåningar med två och tre sovrum i Mijas Costa, är tillgängliga, från {E320000} plus IVA. Betalningsvillkoren lägger köpebrevet till första kvartalet 2029.')
a('.seoDescription',
  'Apartamentos y áticos de dos y tres dormitorios con terrazas en Mijas Costa, con piscina, spa, gimnasio y espacio de coworking, desde {E320000} más IVA.',
  'Appartements et penthouses de deux et trois chambres avec terrasses à Mijas Costa, avec piscine, spa, salle de sport et espace de coworking, à partir de {E320000} hors TVA.',
  'Wohnungen und Penthäuser mit zwei und drei Schlafzimmern und Terrassen in Mijas Costa, mit Pool, Spa, Fitnessraum und Coworking-Bereich, ab {E320000} zuzüglich MwSt.',
  'Апартаменты и пентхаусы с двумя и тремя спальнями и террасами в Михас-Коста, с бассейном, спа, тренажёрным залом и коворкингом, от {E320000} плюс НДС.',
  'شقق وبنتهاوس بغرفتي نوم وثلاث غرف نوم مع تراسات في ميخاس كوستا، مع مسبح وسبا ونادٍ رياضي ومساحة عمل مشتركة، ابتداءً من {E320000} زائد ضريبة القيمة المضافة.',
  'Appartementen en penthouses met twee en drie slaapkamers en terrassen in Mijas Costa, met zwembad, spa, sportruimte en coworkingruimte, vanaf {E320000} plus btw.',
  'Apartamenty i penthouse’y z dwiema i trzema sypialniami oraz tarasami w Mijas Costa, z basenem, spa, siłownią i przestrzenią coworkingową, od {E320000} plus VAT.',
  'Leiligheter og toppleiligheter med to og tre soverom og terrasser i Mijas Costa, med basseng, spa, treningsrom og coworking-område, fra {E320000} pluss mva.',
  'Lägenheter och takvåningar med två och tre sovrum och terrasser i Mijas Costa, med pool, spa, gym och coworking-yta, från {E320000} plus IVA.')
a('.twitterDescription',
  'Viviendas de dos y tres dormitorios con terrazas en Mijas Costa, desde {E320000} más IVA.',
  'Logements de deux et trois chambres avec terrasses à Mijas Costa, à partir de {E320000} hors TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Mijas Costa, ab {E320000} zuzüglich MwSt.',
  'Квартиры с двумя и тремя спальнями и террасами в Михас-Коста, от {E320000} плюс НДС.',
  'مساكن بغرفتي نوم وثلاث غرف نوم مع تراسات في ميخاس كوستا، ابتداءً من {E320000} زائد ضريبة القيمة المضافة.',
  'Woningen met twee en drie slaapkamers en terrassen in Mijas Costa, vanaf {E320000} plus btw.',
  'Lokale z dwiema i trzema sypialniami oraz tarasami w Mijas Costa, od {E320000} plus VAT.',
  'Boliger med to og tre soverom og terrasser i Mijas Costa, fra {E320000} pluss mva.',
  'Bostäder med två och tre sovrum och terrasser i Mijas Costa, från {E320000} plus IVA.')
a('.hero.eyebrow',
  '6 de 19 viviendas de la lista disponibles', '6 des 19 logements de la liste disponibles', '6 von 19 gelisteten Wohnungen verfügbar',
  '6 из 19 квартир из списка доступны', '6 من 19 مسكنًا مدرجًا متاحة', '6 van de 19 vermelde woningen beschikbaar',
  '6 z 19 lokali z listy dostępnych', '6 av de 19 oppførte boligene tilgjengelige', '6 av de 19 listade bostäderna tillgängliga')
T['From EUR 320,000 + VAT'] = {l: expand(FROM[l].format('{P320000}'), l) for l in LOCS}
T['EUR 320,000 + VAT'] = {l: expand('{P320000}', l) for l in LOCS}
T['EUR 320,000 - EUR 480,000 + VAT'] = {l: f'{money(320000, l)} - {money(480000, l)} + {TAXP[l]}' for l in LOCS}
a('.card.description',
  'Apartamentos y áticos de dos y tres dormitorios con terrazas en una promoción de 142 viviendas en Mijas Costa, con piscina, spa, gimnasio y espacio de coworking.',
  'Appartements et penthouses de deux et trois chambres avec terrasses dans un programme de 142 logements à Mijas Costa, avec piscine, spa, salle de sport et espace de coworking.',
  'Wohnungen und Penthäuser mit zwei und drei Schlafzimmern und Terrassen in einer Anlage mit 142 Wohnungen in Mijas Costa, mit Pool, Spa, Fitnessraum und Coworking-Bereich.',
  'Апартаменты и пентхаусы с двумя и тремя спальнями и террасами в комплексе из 142 квартир в Михас-Коста, с бассейном, спа, тренажёрным залом и коворкингом.',
  'شقق وبنتهاوس بغرفتي نوم وثلاث غرف نوم مع تراسات في مشروع من 142 مسكنًا في ميخاس كوستا، مع مسبح وسبا ونادٍ رياضي ومساحة عمل مشتركة.',
  'Appartementen en penthouses met twee en drie slaapkamers en terrassen in een ontwikkeling van 142 woningen in Mijas Costa, met zwembad, spa, sportruimte en coworkingruimte.',
  'Apartamenty i penthouse’y z dwiema i trzema sypialniami oraz tarasami w inwestycji obejmującej 142 lokale w Mijas Costa, z basenem, spa, siłownią i przestrzenią coworkingową.',
  'Leiligheter og toppleiligheter med to og tre soverom og terrasser i et prosjekt med 142 boliger i Mijas Costa, med basseng, spa, treningsrom og coworking-område.',
  'Lägenheter och takvåningar med två och tre sovrum och terrasser i ett projekt med 142 bostäder i Mijas Costa, med pool, spa, gym och coworking-yta.')
a('.quickFacts[4][1]',
  '142 apartamentos y áticos', '142 appartements et penthouses', '142 Wohnungen und Penthäuser', '142 апартаментов и пентхаусов',
  '142 شقة وبنتهاوس', '142 appartementen en penthouses', '142 apartamenty i penthouse’y', '142 leiligheter og toppleiligheter', '142 lägenheter och takvåningar')

# ---- image alts and captions ----------------------------------------------------------------------

ALTS = [
 ('Vista generada por ordenador de dos bloques con terrazas escalonadas alrededor de la piscina comunitaria, con palmeras y tumbonas',
  'Vue générée par ordinateur de deux bâtiments à terrasses en gradins autour de la piscine commune, avec des palmiers et des transats',
  'Computergenerierte Ansicht von zwei Gebäuden mit gestaffelten Terrassen rund um den Gemeinschaftspool, mit Palmen und Sonnenliegen',
  'Компьютерная визуализация: вид на два корпуса со ступенчатыми террасами вокруг общего бассейна, с пальмами и шезлонгами',
  'منظر مولَّد بالحاسوب لمبنيين بتراسات متدرجة حول المسبح المشترك، مع أشجار نخيل ومقاعد تشمّس',
  'Computergegenereerd beeld van twee blokken met trapsgewijze terrassen rond het gemeenschappelijke zwembad, met palmbomen en ligstoelen',
  'Wygenerowany komputerowo widok dwóch budynków z tarasami schodkowymi wokół wspólnego basenu, z palmami i leżakami',
  'Datagenerert bilde av to blokker med trappede terrasser rundt fellesbassenget, med palmer og solsenger',
  'Datorgenererad vy över två hus med trappstegsformade terrasser runt den gemensamma poolen, med palmer och solstolar'),
 ('Vista generada por ordenador a través de la piscina hacia un bloque con terrazas, barandillas de cristal y una palmera',
  'Vue générée par ordinateur à travers la piscine vers un bâtiment à terrasses avec garde-corps en verre et un palmier',
  'Computergenerierte Ansicht über den Pool hinweg auf ein Gebäude mit Terrassen, Glasbrüstungen und einer Palme',
  'Компьютерная визуализация: вид через бассейн на корпус с террасами, стеклянными ограждениями и пальмой',
  'منظر مولَّد بالحاسوب عبر المسبح نحو مبنى بتراسات وحواجز زجاجية ونخلة',
  'Computergegenereerd beeld over het zwembad naar een blok met terrassen, glazen balustrades en een palmboom',
  'Wygenerowany komputerowo widok przez basen na budynek z tarasami, szklanymi balustradami i palmą',
  'Datagenerert bilde over bassenget mot en blokk med terrasser, glassrekkverk og en palme',
  'Datorgenererad vy över poolen mot ett hus med terrasser, glasräcken och en palm'),
 ('Vista generada por ordenador de un bloque largo con terrazas detrás de la piscina, con tumbonas y palmeras',
  'Vue générée par ordinateur d’un long bâtiment à terrasses derrière la piscine, avec des transats et des palmiers',
  'Computergenerierte Ansicht eines langen Gebäudes mit Terrassen hinter dem Pool, mit Sonnenliegen und Palmen',
  'Компьютерная визуализация: вид на длинный корпус с террасами за бассейном, с шезлонгами и пальмами',
  'منظر مولَّد بالحاسوب لمبنى طويل بتراسات خلف المسبح، مع مقاعد تشمّس ونخيل',
  'Computergegenereerd beeld van een lang blok met terrassen achter het zwembad, met ligstoelen en palmbomen',
  'Wygenerowany komputerowo widok długiego budynku z tarasami za basenem, z leżakami i palmami',
  'Datagenerert bilde av en lang blokk med terrasser bak bassenget, med solsenger og palmer',
  'Datorgenererad vy över ett långt hus med terrasser bakom poolen, med solstolar och palmer'),
 ('Vista generada por ordenador de la terraza de la piscina con sillones de descanso y el mar en el horizonte',
  'Vue générée par ordinateur de la terrasse de la piscine avec des fauteuils de détente et la mer à l’horizon',
  'Computergenerierte Ansicht der Poolterrasse mit Loungesesseln und dem Meer am Horizont',
  'Компьютерная визуализация: вид на террасу у бассейна с лаунж-креслами; на горизонте море',
  'منظر مولَّد بالحاسوب لتراس المسبح مع كراسي استرخاء والبحر في الأفق',
  'Computergegenereerd beeld van het zwembadterras met loungestoelen en de zee aan de horizon',
  'Wygenerowany komputerowo widok tarasu przy basenie z fotelami wypoczynkowymi i morzem na horyzoncie',
  'Datagenerert bilde av bassengterrassen med loungestoler og havet i horisonten',
  'Datorgenererad vy över pooltrassen med loungestolar och havet i horisonten'),
 ('Vista generada por ordenador desde una terraza con un sofá y una mesa de comedor, por encima de los tejados hasta el mar',
  'Vue générée par ordinateur depuis une terrasse avec un canapé et une table à manger, par-dessus les toits jusqu’à la mer',
  'Computergenerierte Ansicht von einer Terrasse mit Sofa und Esstisch, über die Dächer hinweg zum Meer',
  'Компьютерная визуализация: вид с террасы с диваном и обеденным столом поверх крыш к морю',
  'منظر مولَّد بالحاسوب من تراس فيه أريكة وطاولة طعام، فوق الأسطح نحو البحر',
  'Computergegenereerd beeld vanaf een terras met een bank en een eettafel, over de daken naar de zee',
  'Wygenerowany komputerowo widok z tarasu z sofą i stołem jadalnianym, ponad dachami w stronę morza',
  'Datagenerert bilde fra en terrasse med en sofa og et spisebord, over takene mot havet',
  'Datorgenererad vy från en terrass med en soffa och ett matbord, över hustaken mot havet'),
 ('Salón generado por ordenador con dos sillones y un sofá, y una puerta corredera de cristal a una terraza con el mar al fondo',
  'Séjour généré par ordinateur avec deux fauteuils et un canapé, et une porte coulissante vitrée donnant sur une terrasse avec la mer au loin',
  'Computergeneriertes Wohnzimmer mit zwei Sesseln und einem Sofa sowie einer gläsernen Schiebetür zu einer Terrasse mit Meerblick',
  'Компьютерная визуализация гостиной с двумя креслами и диваном и стеклянной раздвижной дверью на террасу с видом на море',
  'غرفة معيشة مولَّدة بالحاسوب بكرسيين وأريكة وباب زجاجي منزلق يؤدي إلى تراس يطل على البحر',
  'Computergegenereerde woonkamer met twee fauteuils en een bank, en een glazen schuifdeur naar een terras met de zee erachter',
  'Wygenerowany komputerowo salon z dwoma fotelami i sofą oraz przesuwnymi szklanymi drzwiami na taras z morzem w tle',
  'Datagenerert stue med to lenestoler og en sofa og en skyvedør i glass mot en terrasse med havet bak',
  'Datorgenererat vardagsrum med två fåtöljer och en soffa och en skjutdörr i glas mot en terrass med havet bortom'),
 ('Cocina blanca generada por ordenador con una campana extractora, y una mesa de comedor ovalada con sillas',
  'Cuisine blanche générée par ordinateur avec une hotte aspirante, et une table à manger ovale avec des chaises',
  'Computergenerierte weiße Küche mit Dunstabzugshaube und einem ovalen Esstisch mit Stühlen',
  'Компьютерная визуализация белой кухни с вытяжкой и овальным обеденным столом со стульями',
  'مطبخ أبيض مولَّد بالحاسوب بمروحة شفط وطاولة طعام بيضاوية مع كراسٍ',
  'Computergegenereerde witte keuken met een afzuigkap en een ovale eettafel met stoelen',
  'Wygenerowana komputerowo biała kuchnia z okapem i owalnym stołem jadalnianym z krzesłami',
  'Datagenerert hvitt kjøkken med en ventilator og et ovalt spisebord med stoler',
  'Datorgenererat vitt kök med en köksfläkt och ett ovalt matbord med stolar'),
 ('Dormitorio generado por ordenador con una cama doble, un panel de cabecero tejido y una puerta de cristal a una terraza',
  'Chambre générée par ordinateur avec un lit double, un panneau de tête de lit tressé et une porte vitrée donnant sur une terrasse',
  'Computergeneriertes Schlafzimmer mit Doppelbett, einer geflochtenen Kopfteilverkleidung und einer Glastür zur Terrasse',
  'Компьютерная визуализация спальни с двуспальной кроватью, плетёной панелью изголовья и стеклянной дверью на террасу',
  'غرفة نوم مولَّدة بالحاسوب بسرير مزدوج ولوح منسوج خلف السرير وباب زجاجي يؤدي إلى تراس',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een gevlochten hoofdbordpaneel en een glazen deur naar een terras',
  'Wygenerowana komputerowo sypialnia z łóżkiem dwuosobowym, plecionym panelem za wezgłowiem i szklanymi drzwiami na taras',
  'Datagenerert soverom med en dobbeltseng, et flettet panel bak sengen og en glassdør mot en terrasse',
  'Datorgenererat sovrum med en dubbelsäng, en flätad panel bakom sängen och en glasdörr mot en terrass'),
 ('Baño generado por ordenador con una ducha a ras de suelo, un espejo redondo y un mueble suspendido con lavabo',
  'Salle de bain générée par ordinateur avec une douche à l’italienne, un miroir rond et un meuble suspendu avec vasque',
  'Computergeneriertes Bad mit begehbarer Dusche, rundem Spiegel und einem wandhängenden Waschtisch mit Waschbecken',
  'Компьютерная визуализация ванной комнаты с душем без поддона, круглым зеркалом и подвесной тумбой с раковиной',
  'حمام مولَّد بالحاسوب بدشّ واسع مفتوح ومرآة دائرية ووحدة معلقة بالجدار مع مغسلة',
  'Computergegenereerde badkamer met een inloopdouche, een ronde spiegel en een hangend badkamermeubel met wastafel',
  'Wygenerowana komputerowo łazienka z prysznicem bez brodzika, okrągłym lustrem i wiszącą szafką z umywalką',
  'Datagenerert bad med en åpen dusj, et rundt speil og et veggmontert baderomsmøbel med servant',
  'Datorgenererat badrum med en duschhörna utan kar, en rund spegel och ett väggmonterat badrumsskåp med handfat'),
 ('Zona de spa generada por ordenador con una piscina, un muro vegetal y una cama de descanso',
  'Espace spa généré par ordinateur avec un bassin, un mur végétal et un lit de repos',
  'Computergenerierter Spa-Bereich mit Becken, einer grünen Pflanzenwand und einer Liege',
  'Компьютерная визуализация спа-зоны с бассейном, зелёной стеной из растений и кушеткой',
  'منطقة سبا مولَّدة بالحاسوب بمسبح وجدار نباتي أخضر وسرير استرخاء',
  'Computergegenereerde spa-ruimte met een bad, een groene plantenwand en een ligbed',
  'Wygenerowana komputerowo strefa spa z basenem, zieloną ścianą roślin i leżanką',
  'Datagenerert spa-område med et basseng, en grønn plantevegg og en dagseng',
  'Datorgenererat spaområde med en bassäng, en grön växtvägg och en dagbädd'),
 ('Gimnasio generado por ordenador con cintas de correr, elípticas, pesas y una zona de estiramientos',
  'Salle de sport générée par ordinateur avec des tapis de course, des vélos elliptiques, des poids et une zone d’étirements',
  'Computergenerierter Fitnessraum mit Laufbändern, Crosstrainern, Gewichten und einem Dehnbereich',
  'Компьютерная визуализация тренажёрного зала с беговыми дорожками, эллиптическими тренажёрами, весами и зоной для растяжки',
  'نادٍ رياضي مولَّد بالحاسوب بأجهزة مشي وأجهزة إهليلجية وأوزان ومنطقة لتمارين الإطالة',
  'Computergegenereerde sportruimte met loopbanden, crosstrainers, gewichten en een stretchzone',
  'Wygenerowana komputerowo siłownia z bieżniami, orbitrekami, ciężarami i strefą do rozciągania',
  'Datagenerert treningsrom med tredemøller, ellipsemaskiner, vekter og et tøyningsområde',
  'Datorgenererat gym med löpband, crosstrainers, vikter och en stretchyta'),
 ('Sala de coworking generada por ordenador con escritorios, sillas, una estantería y una barra con taburetes',
  'Salle de coworking générée par ordinateur avec des bureaux, des chaises, une bibliothèque et un comptoir avec des tabourets',
  'Computergenerierter Coworking-Raum mit Schreibtischen, Stühlen, einem Bücherregal und einer Theke mit Hockern',
  'Компьютерная визуализация коворкинга со столами, стульями, книжным шкафом и стойкой с барными стульями',
  'غرفة عمل مشتركة مولَّدة بالحاسوب بمكاتب وكراسٍ ومكتبة وبار بمقاعد مرتفعة',
  'Computergegenereerde coworkingruimte met bureaus, stoelen, een boekenkast en een toonbank met krukken',
  'Wygenerowana komputerowo sala coworkingowa z biurkami, krzesłami, regałem i ladą z hokerami',
  'Datagenerert coworking-rom med skrivebord, stoler, en bokhylle og en benk med barkrakker',
  'Datorgenererat coworking-rum med skrivbord, stolar, en bokhylla och en bardisk med pallar'),
 ('Salón del club social generado por ordenador con asientos, mesas de comedor y puertas correderas a la terraza',
  'Salon du club social généré par ordinateur avec des assises, des tables à manger et des portes coulissantes sur la terrasse',
  'Computergenerierte Lounge des Social Clubs mit Sitzgelegenheiten, Esstischen und Schiebetüren zur Terrasse',
  'Компьютерная визуализация лаунджа соушл-клуба с сиденьями, обеденными столами и раздвижными дверями на террасу',
  'صالة النادي الاجتماعي مولَّدة بالحاسوب بمقاعد وطاولات طعام وأبواب منزلقة إلى التراس',
  'Computergegenereerde lounge van de sociale club met zitplaatsen, eettafels en schuifdeuren naar het terras',
  'Wygenerowana komputerowo sala klubu społecznego z miejscami do siedzenia, stołami jadalnianymi i przesuwnymi drzwiami na taras',
  'Datagenerert lounge i sosialklubben med sitteplasser, spiseborder og skyvedører mot terrassen',
  'Datorgenererad lounge i socialklubben med sittplatser, matbord och skjutdörrar mot terrassen'),
]
for i, tr in enumerate(ALTS):
    put(get(f'.media.items[{i}].alt'), tr)
for key, i in (('hero', 0), ('architecture', 1), ('lifestyle', 3), ('privateViewing', 4)):
    put(get(f'.images.{key}.alt'), ALTS[i])
put(proj['availability']['image']['alt'], ALTS[0])

CAPS = {0: ('Los dos bloques y la piscina comunitaria', 'Les deux bâtiments et la piscine commune', 'Die beiden Gebäude und der Gemeinschaftspool', 'Два корпуса и общий бассейн', 'المبنيان والمسبح المشترك', 'De twee blokken en het gemeenschappelijke zwembad', 'Dwa budynki i wspólny basen', 'De to blokkene og fellesbassenget', 'De två husen och den gemensamma poolen'),
        1: ('El bloque al otro lado de la piscina', 'Le bâtiment de l’autre côté de la piscine', 'Das Gebäude auf der anderen Poolseite', 'Корпус на другой стороне бассейна', 'المبنى على الجانب الآخر من المسبح', 'Het blok aan de overkant van het zwembad', 'Budynek po drugiej stronie basenu', 'Blokken på andre siden av bassenget', 'Huset på andra sidan poolen'),
        2: ('Un bloque largo detrás de la piscina', 'Un long bâtiment derrière la piscine', 'Ein langes Gebäude hinter dem Pool', 'Длинный корпус за бассейном', 'مبنى طويل خلف المسبح', 'Een lang blok achter het zwembad', 'Długi budynek za basenem', 'En lang blokk bak bassenget', 'Ett långt hus bakom poolen'),
        3: ('La terraza de la piscina y el mar', 'La terrasse de la piscine et la mer', 'Die Poolterrasse und das Meer', 'Терраса у бассейна и море', 'تراس المسبح والبحر', 'Het zwembadterras en de zee', 'Taras przy basenie i morze', 'Bassengterrassen og havet', 'Pooltrassen och havet'),
        9: ('La zona de spa', 'L’espace spa', 'Der Spa-Bereich', 'Спа-зона', 'منطقة السبا', 'De spa-ruimte', 'Strefa spa', 'Spa-området', 'Spaområdet')}
for i, tr in CAPS.items():
    put(get(f'.media.items[{i}].caption'), tr)

a('.media.copy',
  'Vistas generadas por ordenador de los bloques, la piscina, los espacios comunes y los interiores, y los planos de las seis viviendas de la lista de precios.',
  'Vues générées par ordinateur des bâtiments, de la piscine, des espaces communs et des intérieurs, et plans des six logements de la liste de prix.',
  'Computergenerierte Ansichten der Gebäude, des Pools, der Gemeinschaftsflächen und der Innenräume sowie die Grundrisse der sechs Wohnungen auf der Preisliste.',
  'Компьютерные визуализации корпусов, бассейна, общих пространств и интерьеров, а также планировки шести квартир из прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمباني والمسبح والمساحات المشتركة والتصاميم الداخلية، ومخططات المساكن الستة الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van de blokken, het zwembad, de gemeenschappelijke ruimtes en de interieurs, en de plattegronden van de zes woningen op de prijslijst.',
  'Wizualizacje komputerowe budynków, basenu, części wspólnych i wnętrz oraz rzuty sześciu lokali z cennika.',
  'Datagenererte bilder av blokkene, bassenget, fellesarealene og interiørene, og plantegningene av de seks boligene på prislisten.',
  'Datorgenererade vyer över husen, poolen, de gemensamma ytorna och interiörerna, samt planritningarna för de sex bostäderna på prislistan.')
a('.media.note',
  'Todas las imágenes son generadas por ordenador y tienen carácter meramente orientativo: el folleto indica que se basan en un proyecto inicial que puede cambiar durante las obras, y que el mobiliario, la decoración y la vegetación que se muestran no forman parte de la oferta. Los planos son los del promotor de las seis viviendas de la lista de precios; indican que pueden modificarse durante las obras por exigencias técnicas o jurídicas, y los nombres de las estancias están en inglés.',
  'Toutes les images sont générées par ordinateur et ne sont données qu’à titre indicatif : la brochure indique qu’elles reposent sur un projet initial susceptible d’évoluer pendant les travaux, et que le mobilier, la décoration et la végétation montrés ne font pas partie de l’offre. Les plans sont ceux du promoteur pour les six logements de la liste de prix ; ils précisent qu’ils peuvent être modifiés pendant les travaux pour des raisons techniques ou juridiques, et les noms des pièces y sont en anglais.',
  'Alle Bilder sind computergenerierte Darstellungen und dienen nur zur Orientierung: Die Broschüre gibt an, dass sie auf einem ursprünglichen Projekt beruhen, das sich während der Bauarbeiten ändern kann, und dass die gezeigten Möbel, die Dekoration und die Bepflanzung nicht zum Angebot gehören. Die Grundrisse sind die Pläne des Bauträgers für die sechs Wohnungen auf der Preisliste; sie weisen darauf hin, dass sie während der Bauarbeiten aus technischen oder rechtlichen Gründen geändert werden können, und die Raumbezeichnungen darauf sind englisch.',
  'Все изображения — компьютерные визуализации, они носят ориентировочный характер: в брошюре сказано, что они основаны на первоначальном проекте, который может измениться в ходе строительства, а показанные мебель, декор и озеленение в предложение не входят. Планировки — это планы застройщика для шести квартир из прайс-листа; в них указано, что они могут быть изменены в ходе строительства по техническим или юридическим причинам, а названия помещений на них даны по-английски.',
  'جميع الصور مولَّدة بالحاسوب وهي للاسترشاد فقط: يذكر الكتيّب أنها مبنية على مشروع أولي قد يتغير أثناء الأعمال، وأن الأثاث والديكور والنباتات الظاهرة ليست جزءًا من العرض. المخططات هي مخططات المطوّر للمساكن الستة الواردة في قائمة الأسعار؛ وهي تذكر أنه قد يجري تعديلها أثناء الأعمال لأسباب فنية أو قانونية، وأسماء الغرف عليها بالإنجليزية.',
  'Alle beelden zijn computergegenereerd en uitsluitend ter oriëntatie: de brochure vermeldt dat ze gebaseerd zijn op een oorspronkelijk project dat tijdens de werken kan veranderen, en dat het getoonde meubilair, de inrichting en de beplanting geen deel van het aanbod uitmaken. De plattegronden zijn de plannen van de ontwikkelaar voor de zes woningen op de prijslijst; ze vermelden dat ze tijdens de werken om technische of juridische redenen kunnen worden gewijzigd, en de kamernamen erop zijn in het Engels.',
  'Wszystkie zdjęcia są wizualizacjami komputerowymi i mają charakter poglądowy: broszura wskazuje, że opierają się na pierwotnym projekcie, który może się zmienić w trakcie prac, oraz że pokazane meble, dekoracje i zieleń nie wchodzą w skład oferty. Rzuty to plany dewelopera sześciu lokali z cennika; zaznaczono na nich, że mogą zostać zmienione w trakcie prac z przyczyn technicznych lub prawnych, a nazwy pomieszczeń na nich są po angielsku.',
  'Alle bildene er datagenererte og kun veiledende: brosjyren oppgir at de bygger på et opprinnelig prosjekt som kan endres under byggearbeidene, og at møblene, dekorasjonen og beplantningen som vises ikke er en del av tilbudet. Plantegningene er utbyggerens egne for de seks boligene på prislisten; de angir at de kan endres under arbeidene av tekniske eller juridiske grunner, og romnavnene på dem er på engelsk.',
  'Alla bilder är datorgenererade och endast vägledande: broschyren anger att de bygger på ett ursprungligt projekt som kan ändras under arbetena och att de möbler, den inredning och den växtlighet som visas inte ingår i erbjudandet. Planritningarna är exploatörens egna för de sex bostäderna på prislistan; de anger att de kan ändras under arbetena av tekniska eller juridiska skäl, och rumsnamnen på dem är på engelska.')

PLAN_ALT = {'es': 'Plano de la vivienda {}', 'fr': 'Plan du logement {}', 'de': 'Grundriss der Wohnung {}',
            'ru': 'Планировка квартиры {}', 'ar': 'مخطط المسكن {}', 'nl': 'Plattegrond van woning {}',
            'pl': 'Rzut lokalu {}', 'no': 'Plantegning av bolig {}', 'sv': 'Planritning för bostad {}'}
PLAN_CAP = {'es': 'Vivienda {}', 'fr': 'Logement {}', 'de': 'Wohnung {}', 'ru': 'Квартира {}',
            'ar': 'المسكن {}', 'nl': 'Woning {}', 'pl': 'Lokal {}', 'no': 'Bolig {}', 'sv': 'Bostad {}'}
n_plan = 0
for it in proj['media']['items']:
    for key, tpl, rx in (('alt', PLAN_ALT, r'Floorplan of home ([A-Z0-9-]+)'), ('caption', PLAN_CAP, r'Home ([A-Z0-9-]+)')):
        m = re.fullmatch(rx, it.get(key, ''))
        if m:
            T[it[key]] = {l: tpl[l].format(m.group(1)) for l in LOCS}
            n_plan += 1
assert n_plan == 12, n_plan

# ---- unit rows: built from the same numbers the English was built from ------------------------------

INNER = {'es': 'm² interiores', 'fr': 'm² intérieurs', 'de': 'm² Innenfläche', 'ru': 'м² внутри',
         'ar': 'م² داخلية', 'nl': 'm² binnen', 'pl': 'm² wnętrza', 'no': 'm² innvendig', 'sv': 'm² inomhus'}
TERR = {'es': 'm² de terraza', 'fr': 'm² de terrasse', 'de': 'm² Terrasse', 'ru': 'терраса {} м²',
        'ar': 'م² تراس', 'nl': 'm² terras', 'pl': 'm² tarasu', 'no': 'm² terrasse', 'sv': 'm² terrass'}
GARD = {'es': 'm² de jardín', 'fr': 'm² de jardin', 'de': 'm² Garten', 'ru': 'сад {} м²',
        'ar': 'م² حديقة', 'nl': 'm² tuin', 'pl': 'm² ogrodu', 'no': 'm² hage', 'sv': 'm² trädgård'}
SEP = {l: ', ' for l in LOCS}; SEP['ar'] = '، '


def dec(x, loc):
    return f'{x:.2f}'.replace('.', '.' if loc == 'ar' else ',')


def size(inner, terr, garden, loc):
    parts = [f'{dec(inner, loc)} {INNER[loc]}']
    for x, tpl in ((terr, TERR), (garden, GARD)):
        if x is None:
            continue
        t = tpl[loc]
        parts.append(t.format(dec(x, loc)) if '{}' in t else f'{dec(x, loc)} {t}')
    return SEP[loc].join(parts)


for u in proj['availability']['units']:
    m = re.fullmatch(r'([\d.]+) sqm interior, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm garden)?', u['size'])
    assert m, u['size']
    T[u['size']] = {l: size(float(m.group(1)), float(m.group(2)), float(m.group(3)) if m.group(3) else None, l) for l in LOCS}

# ---- overview, why, architecture ------------------------------------------------------------------

a('.overview.headlineHtml',
  '142 viviendas, <em>seis disponibles actualmente</em>', '142 logements, <em>six disponibles actuellement</em>',
  '142 Wohnungen, <em>sechs derzeit verfügbar</em>', '142 квартиры, <em>шесть доступны сейчас</em>',
  '142 مسكنًا، <em>ستة منها متاحة حاليًا</em>', '142 woningen, <em>zes momenteel beschikbaar</em>',
  '142 lokale, <em>sześć obecnie dostępnych</em>', '142 boliger, <em>seks tilgjengelige nå</em>',
  '142 bostäder, <em>sex tillgängliga just nu</em>')
a('.overview.copy[0]',
  'Mijas Horizon Terraces es una promoción de 142 apartamentos y áticos de dos y tres dormitorios en Mijas Costa. El folleto describe vistas al mar incluso desde las plantas bajas, una piscina central con zona chill-out, un gimnasio, una zona de spa, un club social y un espacio de coworking, en jardines paisajísticos.',
  'Mijas Horizon Terraces est un programme de 142 appartements et penthouses de deux et trois chambres à Mijas Costa. La brochure décrit des vues sur la mer jusque depuis les rez-de-chaussée, une piscine centrale avec un espace de détente, une salle de sport, un espace spa, un club social et un espace de coworking, au milieu de jardins paysagers.',
  'Mijas Horizon Terraces ist eine Anlage mit 142 Wohnungen und Penthäusern mit zwei und drei Schlafzimmern in Mijas Costa. Die Broschüre beschreibt Meerblick sogar aus den Erdgeschossen, einen zentralen Pool mit Chill-out-Bereich, einen Fitnessraum, einen Spa-Bereich, einen Social Club und einen Coworking-Bereich in gepflegten Gartenanlagen.',
  'Mijas Horizon Terraces — комплекс из 142 апартаментов и пентхаусов с двумя и тремя спальнями в Михас-Коста. В брошюре описаны вид на море даже с первых этажей, центральный бассейн с зоной отдыха, тренажёрный зал, спа-зона, соушл-клуб и коворкинг среди ландшафтных садов.',
  'Mijas Horizon Terraces مشروع من 142 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم في ميخاس كوستا. يصف الكتيّب إطلالات على البحر حتى من الطوابق الأرضية، ومسبحًا مركزيًا مع منطقة استرخاء، ونادياً رياضياً، ومنطقة سبا، ونادياً اجتماعياً، ومساحة عمل مشتركة، وسط حدائق مُنسَّقة.',
  'Mijas Horizon Terraces is een ontwikkeling van 142 appartementen en penthouses met twee en drie slaapkamers in Mijas Costa. De brochure beschrijft zeezicht tot op de begane grond, een centraal zwembad met een chill-outzone, een sportruimte, een spa-ruimte, een sociale club en een coworkingruimte, in aangelegde tuinen.',
  'Mijas Horizon Terraces to inwestycja obejmująca 142 apartamenty i penthouse’y z dwiema i trzema sypialniami w Mijas Costa. Broszura opisuje widok na morze nawet z parteru, centralny basen ze strefą relaksu, siłownię, strefę spa, klub społeczny i przestrzeń coworkingową, w zagospodarowanych ogrodach.',
  'Mijas Horizon Terraces er et prosjekt med 142 leiligheter og toppleiligheter med to og tre soverom i Mijas Costa. Brosjyren beskriver havutsikt selv fra første etasje, et sentralt basseng med en chill-out-sone, et treningsrom, et spa-område, en sosial klubb og et coworking-område, i opparbeidede hager.',
  'Mijas Horizon Terraces är ett projekt med 142 lägenheter och takvåningar med två och tre sovrum i Mijas Costa. Broschyren beskriver havsutsikt även från bottenvåningarna, en central pool med chill-out-yta, ett gym, ett spaområde, en socialklubb och en coworking-yta, i anlagda trädgårdar.')
a('.overview.copy[1]',
  'La lista de precios nombra 19 de las 142 viviendas. Seis tienen precio y están disponibles, desde una vivienda de dos dormitorios por {E320000} hasta un ático de dos dormitorios por {E480000}, todo antes de IVA, y las otras 13 figuran como reservadas. Las condiciones de pago sitúan la escritura en el primer trimestre de 2029.',
  'La liste de prix nomme 19 des 142 logements. Six ont un prix et sont disponibles, d’un logement de deux chambres à {E320000} à un penthouse de deux chambres à {E480000}, le tout hors TVA, et les 13 autres sont marqués comme réservés. Les conditions de paiement placent l’acte authentique au premier trimestre 2029.',
  'Die Preisliste nennt 19 der 142 Wohnungen. Sechs haben einen Preis und sind verfügbar, von einer Wohnung mit zwei Schlafzimmern für {E320000} bis zu einem Penthouse mit zwei Schlafzimmern für {E480000}, alles vor MwSt.; die übrigen 13 sind als reserviert gekennzeichnet. Die Zahlungsbedingungen setzen die Beurkundung auf das erste Quartal 2029.',
  'В прайс-листе названы 19 из 142 квартир. У шести указана цена, и они доступны: от квартиры с двумя спальнями за {E320000} до пентхауса с двумя спальнями за {E480000}, всё без НДС; остальные 13 отмечены как зарезервированные. По условиям оплаты оформление права собственности у нотариуса намечено на первый квартал 2029 года.',
  'تسمّي قائمة الأسعار 19 مسكنًا من أصل 142. ستة منها لها سعر ومتاحة، من مسكن بغرفتي نوم بسعر {E320000} إلى بنتهاوس بغرفتي نوم بسعر {E480000}، كلها قبل ضريبة القيمة المضافة، أما الـ13 الأخرى فمعلَّمة محجوزة. وتحدد شروط الدفع موعد سند الملكية في الربع الأول من 2029.',
  'De prijslijst noemt 19 van de 142 woningen. Zes hebben een prijs en zijn beschikbaar, van een woning met twee slaapkamers voor {E320000} tot een penthouse met twee slaapkamers voor {E480000}, alles vóór btw, en de overige 13 staan als gereserveerd aangemerkt. De betalingsvoorwaarden plaatsen de notariële akte in het eerste kwartaal van 2029.',
  'Cennik wymienia 19 ze 142 lokali. Sześć ma cenę i jest dostępnych, od lokalu z dwiema sypialniami za {E320000} do penthouse’u z dwiema sypialniami za {E480000}, wszystko przed VAT, a pozostałe 13 jest oznaczonych jako zarezerwowane. Warunki płatności wskazują akt notarialny w pierwszym kwartale 2029 roku.',
  'Prislisten nevner 19 av de 142 boligene. Seks har pris og er tilgjengelige, fra en bolig med to soverom til {E320000} til en toppleilighet med to soverom til {E480000}, alt før mva, og de øvrige 13 er merket som reservert. Betalingsvilkårene legger skjøtet til første kvartal 2029.',
  'Prislistan nämner 19 av de 142 bostäderna. Sex har pris och är tillgängliga, från en bostad med två sovrum för {E320000} till en takvåning med två sovrum för {E480000}, allt före IVA (spansk moms), och de övriga 13 är markerade som reserverade. Betalningsvillkoren lägger köpebrevet till första kvartalet 2029.')
a('.overview.metrics[0][1]', '142 viviendas', '142 logements', '142 Wohnungen', '142 квартиры', '142 مسكنًا', '142 woningen', '142 lokale', '142 boliger', '142 bostäder')
a('.overview.metrics[1][1]', '19 viviendas', '19 logements', '19 Wohnungen', '19 квартир', '19 مسكنًا', '19 woningen', '19 lokali', '19 boliger', '19 bostäder')

a('.why.copy',
  'Viviendas nuevas de dos y tres dormitorios con terraza o jardín y el mar a la vista, en una promoción con piscina, spa, gimnasio y espacio de coworking, y el 70 por ciento del precio reservado para la escritura.',
  'Des logements neufs de deux et trois chambres avec terrasse ou jardin et vue sur la mer, dans un programme avec piscine, spa, salle de sport et espace de coworking, et 70 pour cent du prix réservé à l’acte authentique.',
  'Neue Wohnungen mit zwei und drei Schlafzimmern, Terrasse oder Garten und Blick aufs Meer, in einer Anlage mit Pool, Spa, Fitnessraum und Coworking-Bereich, und 70 Prozent des Preises erst bei der Beurkundung fällig.',
  'Новые квартиры с двумя и тремя спальнями, террасой или садом и видом на море в комплексе с бассейном, спа, тренажёрным залом и коворкингом; 70 процентов цены оплачивается при оформлении сделки у нотариуса.',
  'مساكن جديدة بغرفتي نوم وثلاث غرف نوم مع تراس أو حديقة وإطلالة على البحر، في مشروع يضم مسبحًا وسبا ونادياً رياضياً ومساحة عمل مشتركة، مع تأجيل 70 بالمئة من السعر إلى سند الملكية.',
  'Nieuwe woningen met twee en drie slaapkamers, een terras of een tuin en zicht op zee, in een ontwikkeling met zwembad, spa, sportruimte en coworkingruimte, waarbij 70 procent van de prijs pas bij de akte verschuldigd is.',
  'Nowe lokale z dwiema i trzema sypialniami, tarasem lub ogrodem i widokiem na morze, w inwestycji z basenem, spa, siłownią i przestrzenią coworkingową, z 70 procentami ceny płatnymi dopiero przy akcie notarialnym.',
  'Nye boliger med to og tre soverom, terrasse eller hage og utsikt mot havet, i et prosjekt med basseng, spa, treningsrom og coworking-område, der 70 prosent av prisen forfaller først ved skjøtet.',
  'Nya bostäder med två och tre sovrum, terrass eller trädgård och utsikt mot havet, i ett projekt med pool, spa, gym och coworking-yta, där 70 procent av priset förfaller först vid köpebrevet.')
a('.why.points[0][1]',
  'Compradores que quieren un apartamento o ático nuevo de dos o tres dormitorios en Mijas Costa con terraza o jardín, para vivir o como segunda residencia.',
  'Acheteurs qui veulent un appartement ou un penthouse neuf de deux ou trois chambres à Mijas Costa, avec terrasse ou jardin, pour y vivre ou comme résidence secondaire.',
  'Käufer, die in Mijas Costa eine neue Wohnung oder ein neues Penthouse mit zwei oder drei Schlafzimmern und Terrasse oder Garten suchen, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которым нужны новые апартаменты или пентхаус с двумя или тремя спальнями, террасой или садом в Михас-Коста — для жизни или как вторая недвижимость.',
  'مشترون يريدون شقة أو بنتهاوس جديدًا بغرفتي نوم أو ثلاث غرف نوم في ميخاس كوستا مع تراس أو حديقة، للسكن أو كمسكن ثانٍ.',
  'Kopers die in Mijas Costa een nieuw appartement of penthouse met twee of drie slaapkamers en een terras of tuin zoeken, om er te wonen of als tweede woning.',
  'Kupujący, którzy szukają nowego apartamentu lub penthouse’u z dwiema lub trzema sypialniami oraz tarasem lub ogrodem w Mijas Costa, do zamieszkania lub jako druga nieruchomość.',
  'Kjøpere som vil ha en ny leilighet eller toppleilighet med to eller tre soverom og terrasse eller hage i Mijas Costa, til å bo i eller som feriebolig.',
  'Köpare som vill ha en ny lägenhet eller takvåning med två eller tre sovrum och terrass eller trädgård i Mijas Costa, att bo i eller som andrabostad.')
a('.why.points[1][1]',
  'Las seis viviendas de la lista son dos en planta baja, tres apartamentos en las plantas primera y segunda y un ático. Una de las viviendas de planta baja tiene un jardín delantero de {N49.54} {U}, y el ático, una terraza descubierta de {N36.96} {U}. Cada una figura con una plaza de garaje y un trastero.',
  'Les six logements de la liste sont deux logements en rez-de-chaussée, trois appartements au premier et au deuxième étage et un penthouse. Un des logements du rez-de-chaussée a un jardin sur le devant de {N49.54} {U}, et le penthouse une terrasse découverte de {N36.96} {U}. Chacun est indiqué avec une place de garage et une cave.',
  'Die sechs Wohnungen auf der Liste sind zwei Erdgeschosswohnungen, drei Wohnungen im ersten und zweiten Obergeschoss und ein Penthouse. Eine der Erdgeschosswohnungen hat einen Vorgarten von {N49.54} {U}, das Penthouse eine unüberdachte Terrasse von {N36.96} {U}. Jede ist mit einem Garagenstellplatz und einem Abstellraum aufgeführt.',
  'Шесть квартир из списка — это две квартиры на первом этаже, три апартамента на втором и третьем этажах и один пентхаус. У одной квартиры на первом этаже есть палисадник площадью {N49.54} {U}, а у пентхауса — открытая терраса {N36.96} {U}. У каждой в списке указаны место в гараже и кладовая.',
  'المساكن الستة في القائمة هي مسكنان في الطابق الأرضي وثلاث شقق في الطابقين الأول والثاني وبنتهاوس واحد. لأحد مسكني الطابق الأرضي حديقة أمامية مساحتها {N49.54} {U}، وللبنتهاوس تراس مكشوف مساحته {N36.96} {U}. ويُدرج لكل منها موقف في المرآب ومخزن.',
  'De zes woningen op de lijst zijn twee woningen op de begane grond, drie appartementen op de eerste en tweede verdieping en één penthouse. Een van de woningen op de begane grond heeft een voortuin van {N49.54} {U}, en het penthouse een open terras van {N36.96} {U}. Elk is vermeld met een garageplaats en een berging.',
  'Sześć lokali z listy to dwa lokale na parterze, trzy apartamenty na pierwszym i drugim piętrze oraz jeden penthouse. Jeden z lokali na parterze ma ogródek przed domem o powierzchni {N49.54} {U}, a penthouse niezadaszony taras o powierzchni {N36.96} {U}. Każdy jest podany z miejscem w garażu i komórką lokatorską.',
  'De seks boligene på listen er to boliger i første etasje, tre leiligheter i andre og tredje etasje og én toppleilighet. Den ene boligen i første etasje har en forhage på {N49.54} {U}, og toppleiligheten har en uoverbygd terrasse på {N36.96} {U}. Hver er oppført med en garasjeplass og en bod.',
  'De sex bostäderna på listan är två bostäder i bottenvåningen, tre lägenheter på första och andra våningen och en takvåning. En av bostäderna i bottenvåningen har en trädgård framför på {N49.54} {U}, och takvåningen har en öppen terrass på {N36.96} {U}. Var och en är listad med en garageplats och ett förråd.')
a('.why.points[2][1]',
  'El folleto sitúa la promoción en Mijas Costa, a 40 km de Marbella y a 41 km de Málaga, y señala que a 800 m se está construyendo un gran parque con un lago navegable, un carril bici y un anfiteatro al aire libre.',
  'La brochure situe le programme à Mijas Costa, à 40 km de Marbella et à 41 km de Málaga, et indique qu’un grand parc avec un lac navigable, une piste cyclable et un amphithéâtre en plein air est en construction à 800 m.',
  'Die Broschüre verortet die Anlage in Mijas Costa, 40 km von Marbella und 41 km von Málaga entfernt, und nennt einen großen Park mit schiffbarem See, Radweg und Freilichtamphitheater, der 800 m entfernt gebaut wird.',
  'В брошюре комплекс расположен в Михас-Коста, в 40 км от Марбельи и в 41 км от Малаги; там же сказано, что в 800 м строится большой парк с судоходным озером, велодорожкой и амфитеатром под открытым небом.',
  'يضع الكتيّب المشروع في ميخاس كوستا، على بعد 40 كم من ماربيا و41 كم من مالقة، ويذكر أن حديقة كبيرة بها بحيرة صالحة للإبحار ومسار للدراجات ومدرج في الهواء الطلق قيد الإنشاء على بعد 800 م.',
  'De brochure plaatst de ontwikkeling in Mijas Costa, 40 km van Marbella en 41 km van Málaga, en meldt dat op 800 m een groot park met een bevaarbaar meer, een fietspad en een openluchtamfitheater wordt aangelegd.',
  'Broszura umieszcza inwestycję w Mijas Costa, 40 km od Marbelli i 41 km od Málagi, i podaje, że 800 m dalej powstaje duży park z żeglownym jeziorem, ścieżką rowerową i amfiteatrem na wolnym powietrzu.',
  'Brosjyren plasserer prosjektet i Mijas Costa, 40 km fra Marbella og 41 km fra Málaga, og opplyser at en stor park med en seilbar innsjø, en sykkelsti og et utendørs amfiteater bygges 800 m unna.',
  'Broschyren placerar projektet i Mijas Costa, 40 km från Marbella och 41 km från Málaga, och anger att en stor park med en farbar sjö, en cykelväg och en utomhusamfiteater byggs 800 m bort.')
a('.why.points[3][1]',
  'La lista de precios nombra 19 de las 142 viviendas, los precios son antes de IVA, y las condiciones de pago vinculan el contrato privado a la obtención de la licencia, cuyo estado no consta en ningún documento. Confirmamos la licencia, la fecha de entrega y la lista vigente antes de cualquier reserva.',
  'La liste de prix nomme 19 des 142 logements, les prix s’entendent hors TVA, et les conditions de paiement lient le contrat privé à l’obtention du permis, dont aucun document ne donne le statut. Nous confirmons le permis, la date de livraison et la liste en vigueur avant toute réservation.',
  'Die Preisliste nennt 19 der 142 Wohnungen, die Preise verstehen sich vor MwSt., und die Zahlungsbedingungen knüpfen den privaten Kaufvertrag an die Erteilung der Baugenehmigung, deren Stand kein Dokument nennt. Wir bestätigen Genehmigung, Fertigstellungstermin und aktuelle Liste vor jeder Reservierung.',
  'В прайс-листе названы 19 из 142 квартир, цены указаны без НДС, а условия оплаты привязывают частный договор к получению лицензии на строительство, статус которой ни один документ не называет. Лицензию, срок сдачи и актуальный список мы подтверждаем до любого бронирования.',
  'تسمّي قائمة الأسعار 19 مسكنًا من أصل 142، والأسعار قبل ضريبة القيمة المضافة، وتربط شروط الدفع العقد الخاص بالحصول على الرخصة، ولا تذكر أي وثيقة وضعها. نؤكد الرخصة وموعد التسليم والقائمة الحالية قبل أي حجز.',
  'De prijslijst noemt 19 van de 142 woningen, de prijzen zijn vóór btw, en de betalingsvoorwaarden koppelen het onderhandse contract aan het verkrijgen van de vergunning, waarvan geen enkel document de stand vermeldt. We bevestigen de vergunning, de opleveringsdatum en de actuele lijst vóór een reservering.',
  'Cennik wymienia 19 ze 142 lokali, ceny są przed VAT, a warunki płatności wiążą umowę przedwstępną z uzyskaniem pozwolenia, którego status nie wynika z żadnego dokumentu. Pozwolenie, termin oddania i aktualną listę potwierdzamy przed jakąkolwiek rezerwacją.',
  'Prislisten nevner 19 av de 142 boligene, prisene er før mva, og betalingsvilkårene knytter den private kontrakten til at tillatelsen innvilges, men ingen dokumenter oppgir status for den. Vi bekrefter tillatelsen, overleveringsdatoen og den gjeldende listen før enhver reservasjon.',
  'Prislistan nämner 19 av de 142 bostäderna, priserna är före IVA, och betalningsvillkoren knyter det privata avtalet till att bygglovet beviljas, men inget dokument anger dess status. Vi bekräftar bygglovet, tillträdesdatumet och den aktuella listan före varje reservation.')

a('.architecture.headlineHtml',
  'Bloques con terrazas, <em>terrazas abiertas a las vistas</em>', 'Bâtiments à terrasses, <em>terrasses ouvertes sur la vue</em>',
  'Terrassierte Gebäude, <em>Terrassen zur Aussicht</em>', 'Корпуса с террасами, <em>террасы с открытым видом</em>',
  'مبانٍ ذات تراسات، <em>تراسات مفتوحة على المنظر</em>', 'Blokken met terrassen, <em>terrassen open naar het uitzicht</em>',
  'Budynki z tarasami, <em>tarasy otwarte na widok</em>', 'Blokker med terrasser, <em>terrasser åpne mot utsikten</em>',
  'Hus med terrasser, <em>terrasser öppna mot utsikten</em>')
a('.architecture.copy[0]',
  'En las imágenes, los bloques son largos y bajos, con una terraza profunda en cada planta, barandillas de cristal y muros de color arena sobre la piscina comunitaria. El folleto promete vistas al mar incluso desde las plantas bajas y dice que todas las viviendas están orientadas al sur o al suroeste.',
  'Sur les images, les bâtiments sont longs et bas, avec une terrasse profonde à chaque étage, des garde-corps en verre et des murs couleur sable au-dessus de la piscine commune. La brochure promet des vues sur la mer jusque depuis les rez-de-chaussée et indique que tous les logements sont orientés au sud ou au sud-ouest.',
  'In den Bildern sind die Gebäude lang und niedrig, mit einer tiefen Terrasse auf jeder Etage, Glasbrüstungen und sandfarbenen Wänden über dem Gemeinschaftspool. Die Broschüre verspricht Meerblick sogar aus den Erdgeschossen und gibt an, dass alle Wohnungen nach Süden oder Südwesten ausgerichtet sind.',
  'На визуализациях корпуса длинные и невысокие, с глубокой террасой на каждом этаже, стеклянными ограждениями и стенами песочного цвета над общим бассейном. В брошюре обещан вид на море даже с первых этажей и сказано, что все квартиры ориентированы на юг или юго-запад.',
  'في الصور تبدو المباني طويلة ومنخفضة، بتراس عميق في كل طابق وحواجز زجاجية وجدران بلون الرمل فوق المسبح المشترك. يعد الكتيّب بإطلالات على البحر حتى من الطوابق الأرضية، ويذكر أن جميع المساكن تتجه نحو الجنوب أو الجنوب الغربي.',
  'Op de beelden zijn de blokken lang en laag, met op elke verdieping een diep terras, glazen balustrades en zandkleurige muren boven het gemeenschappelijke zwembad. De brochure belooft zeezicht tot op de begane grond en zegt dat alle woningen op het zuiden of zuidwesten liggen.',
  'Na wizualizacjach budynki są długie i niskie, z głębokim tarasem na każdym piętrze, szklanymi balustradami i piaskowymi ścianami nad wspólnym basenem. Broszura obiecuje widok na morze nawet z parteru i podaje, że wszystkie lokale są skierowane na południe lub południowy zachód.',
  'På bildene er blokkene lange og lave, med en dyp terrasse i hver etasje, glassrekkverk og sandfargede vegger over fellesbassenget. Brosjyren lover havutsikt selv fra første etasje og sier at alle boligene vender mot sør eller sørvest.',
  'På bilderna är husen långa och låga, med en djup terrass på varje våning, glasräcken och sandfärgade väggar ovanför den gemensamma poolen. Broschyren lovar havsutsikt även från bottenvåningarna och anger att alla bostäder har söderläge eller sydvästläge.')
a('.architecture.copy[1]',
  'Los planos muestran las viviendas de planta baja abiertas a una terraza o a un jardín delantero, y el ático con una única terraza descubierta a lo largo de todo el ancho de la vivienda.',
  'Les plans montrent les logements du rez-de-chaussée ouverts sur une terrasse ou un jardin à l’avant, et le penthouse avec une seule terrasse découverte sur toute la largeur du logement.',
  'Die Pläne zeigen die Erdgeschosswohnungen mit Zugang zu einer Terrasse oder einem Vorgarten und das Penthouse mit einer einzigen unüberdachten Terrasse über die gesamte Breite der Wohnung.',
  'На планах квартиры первого этажа выходят на террасу или в палисадник, а пентхаус имеет одну открытую террасу на всю ширину квартиры.',
  'تُظهر المخططات مساكن الطابق الأرضي مفتوحة على تراس أو حديقة أمامية، والبنتهاوس بتراس مكشوف واحد على امتداد عرض المسكن كله.',
  'De plattegronden tonen de woningen op de begane grond met uitgang naar een terras of een voortuin, en het penthouse met één open terras over de volle breedte van de woning.',
  'Rzuty pokazują lokale na parterze z wyjściem na taras lub do ogródka przed domem oraz penthouse z jednym niezadaszonym tarasem na całej szerokości lokalu.',
  'Plantegningene viser boligene i første etasje med utgang til en terrasse eller en forhage, og toppleiligheten med én uoverbygd terrasse over hele boligens bredde.',
  'Planritningarna visar bostäderna i bottenvåningen med utgång till en terrass eller en trädgård framför, och takvåningen med en enda öppen terrass över hela bostadens bredd.')
a('.architecture.highlights[0][1]',
  'Cimentación de hormigón armado, según el estudio geotécnico del terreno, y estructura de hormigón armado encima.',
  'Fondations en béton armé, selon l’étude géotechnique du terrain, et structure en béton armé au-dessus.',
  'Eine Stahlbetonfundierung nach dem geotechnischen Gutachten des Grundstücks und darüber eine Stahlbetonkonstruktion.',
  'Железобетонный фундамент по геотехническому исследованию участка и железобетонный каркас выше.',
  'أساس من الخرسانة المسلحة وفق الدراسة الجيوتقنية للأرض، وهيكل من الخرسانة المسلحة فوقه.',
  'Een fundering van gewapend beton volgens het geotechnisch onderzoek van het terrein, met daarboven een constructie van gewapend beton.',
  'Fundament z żelbetu zgodny z badaniem geotechnicznym gruntu oraz żelbetowa konstrukcja nad nim.',
  'Et fundament av armert betong etter den geotekniske undersøkelsen av tomten, og en bærekonstruksjon av armert betong over det.',
  'En grund av armerad betong enligt markens geotekniska undersökning och en stomme av armerad betong ovanpå.')
a('.architecture.highlights[1][1]',
  'Ladrillo perforado, aislamiento de poliuretano proyectado, cámara de aire y trasdosado de placa de yeso laminado con lana mineral.',
  'Brique perforée, isolation en polyuréthane projeté, lame d’air et doublage en plaques de plâtre avec laine minérale.',
  'Lochziegel, gespritzte Polyurethandämmung, ein Luftraum und eine Gipskartonverkleidung mit Mineralwolle.',
  'Пустотелый кирпич, напылённая полиуретановая теплоизоляция, воздушная прослойка и облицовка гипсокартоном с минеральной ватой.',
  'طوب مثقّب وعزل حراري من البولي يوريثان المرشوش وفراغ هوائي وتكسية من ألواح الجبس مع صوف معدني.',
  'Geperforeerde baksteen, gespoten polyurethaanisolatie, een luchtspouw en een gipsplaatbekleding met minerale wol.',
  'Cegła dziurawka, natryskowa izolacja poliuretanowa, szczelina powietrzna i okładzina z płyt gipsowo-kartonowych z wełną mineralną.',
  'Hulltegl, sprøytet polyuretanisolasjon, et luftrom og en gipsplatekledning med mineralull.',
  'Håltegel, sprutad polyuretanisolering, en luftspalt och en gipsskiva med mineralull.')
a('.architecture.highlights[2][1]',
  'Ventanas de PVC con doble acristalamiento y cámara aislante, vidrio laminado de seguridad en las puertas de la terraza y persianas enrollables manuales con aislamiento térmico en los dormitorios.',
  'Fenêtres en PVC avec double vitrage et lame isolante, verre feuilleté de sécurité aux portes des terrasses et volets roulants manuels à isolation thermique dans les chambres.',
  'PVC-Fenster mit Doppelverglasung und Dämmkammer, Verbundsicherheitsglas an den Terrassentüren und manuelle Rollläden mit Wärmedämmung in den Schlafzimmern.',
  'Окна из ПВХ с двойным остеклением и изолирующей камерой, безопасное многослойное стекло в дверях на террасы и ручные рольставни с теплоизоляцией в спальнях.',
  'نوافذ من البي في سي بزجاج مزدوج وغرفة عزل، وزجاج مُصفَّح للسلامة في أبواب التراسات، وستائر لفّ يدوية معزولة حراريًا في غرف النوم.',
  'PVC-ramen met dubbele beglazing en isolerende spouw, gelaagd veiligheidsglas in de terrasdeuren en handbediende rolluiken met thermische isolatie in de slaapkamers.',
  'Okna z PCV z podwójnym szkleniem i komorą izolacyjną, bezpieczne szkło warstwowe w drzwiach tarasowych oraz ręczne rolety z izolacją termiczną w sypialniach.',
  'PVC-vinduer med dobbeltglass og isolerende kammer, laminert sikkerhetsglass i terrassedørene og manuelle rullegardiner med varmeisolasjon i soverommene.',
  'PVC-fönster med dubbelglas och isolerande kammare, laminerat säkerhetsglas i terrassdörrarna och manuella rullgardiner med värmeisolering i sovrummen.')
a('.architecture.highlights[3][1]',
  'Suelos de baldosas antideslizantes y resistentes a las heladas, con grifo, conexión de TV, tomas eléctricas e iluminación en la terraza.',
  'Sols en carreaux antidérapants et résistants au gel, avec un robinet, une prise TV, des prises électriques et un éclairage sur la terrasse.',
  'Rutschfeste, frostbeständige Fliesen auf den Böden, mit Wasserhahn, TV-Anschluss, Steckdosen und Beleuchtung auf der Terrasse.',
  'Нескользящая морозостойкая плитка на полу, кран, телевизионная розетка, электрические розетки и освещение на террасе.',
  'بلاط مانع للانزلاق ومقاوم للصقيع على الأرضيات، مع صنبور ووصلة تلفزيون ومآخذ كهربائية وإضاءة في التراس.',
  'Antislip, vorstbestendige tegels op de vloeren, met een kraan, een tv-aansluiting, stopcontacten en verlichting op het terras.',
  'Antypoślizgowe, mrozoodporne płytki na podłogach, z kranem, przyłączem TV, gniazdami elektrycznymi i oświetleniem na tarasie.',
  'Sklisikre, frostbestandige fliser på gulvene, med en kran, TV-tilkobling, stikkontakter og belysning på terrassen.',
  'Halksäkra, frostbeständiga plattor på golven, med en kran, tv-uttag, eluttag och belysning på terrassen.')

# ---- qualitySpecs ----------------------------------------------------------------------------------

a('.qualitySpecs.sourceNote',
  'Fuente: la descripción de materiales del promotor, revisión 02, de fecha {D8.4.2026}. Indica que los materiales pueden modificarse a criterio de la dirección facultativa y sustituirse por otros de calidad similar o superior.',
  'Source : la description des matériaux du promoteur, révision 02, datée du {D8.4.2026}. Elle indique que les matériaux peuvent être modifiés à la discrétion de la maîtrise d’œuvre et remplacés par d’autres de qualité similaire ou supérieure.',
  'Quelle: die Materialbeschreibung des Bauträgers, Revision 02, vom {D8.4.2026}. Sie besagt, dass die Materialien nach Ermessen der Bauleitung geändert und durch andere von gleichwertiger oder höherer Qualität ersetzt werden können.',
  'Источник: описание материалов от застройщика, редакция 02, от {D8.4.2026}. В нём сказано, что материалы могут быть изменены по усмотрению руководства проекта и заменены другими, равного или более высокого качества.',
  'المصدر: وصف المواد الصادر عن المطوّر، المراجعة 02، بتاريخ {D8.4.2026}. وينص على أنه يجوز تعديل المواد بتقدير إدارة المشروع واستبدالها بمواد أخرى بجودة مماثلة أو أعلى.',
  'Bron: de materiaalbeschrijving van de ontwikkelaar, revisie 02, van {D8.4.2026}. Daarin staat dat de materialen naar goeddunken van de projectleiding mogen worden gewijzigd en vervangen door andere van gelijke of hogere kwaliteit.',
  'Źródło: opis materiałów dewelopera, rewizja 02, z dnia {D8.4.2026}. Wynika z niego, że materiały mogą zostać zmienione według uznania kierownictwa projektu i zastąpione innymi, o podobnej lub wyższej jakości.',
  'Kilde: utbyggerens materialbeskrivelse, revisjon 02, datert {D8.4.2026}. Den sier at materialene kan endres etter prosjektledelsens skjønn og erstattes av andre av tilsvarende eller høyere kvalitet.',
  'Källa: exploatörens materialbeskrivning, revision 02, daterad {D8.4.2026}. Den anger att materialen kan ändras efter projektledningens gottfinnande och ersättas med andra av likvärdig eller högre kvalitet.')
a('.qualitySpecs.groups[0].items[0]',
  'Suelo laminado en el salón, los dormitorios, la cocina, los pasillos y los vestíbulos, con rodapiés blancos, y baldosas cerámicas en el suelo de los baños.',
  'Parquet stratifié dans le séjour, les chambres, la cuisine, les couloirs et les entrées, avec des plinthes blanches, et carrelage en céramique au sol des salles de bains.',
  'Laminatboden in Wohnzimmer, Schlafzimmern, Küche, Fluren und Dielen mit weißen Sockelleisten sowie Keramikfliesen auf den Badezimmerböden.',
  'Ламинат в гостиной, спальнях, кухне, коридорах и холлах с белыми плинтусами и керамическая плитка на полу в ванных комнатах.',
  'أرضيات لامينيت في غرفة المعيشة وغرف النوم والمطبخ والممرات والمداخل، مع وزرات بيضاء، وبلاط سيراميك على أرضيات الحمامات.',
  'Laminaatvloer in de woonkamer, slaapkamers, keuken, gangen en hallen, met witte plinten, en keramische tegels op de badkamervloeren.',
  'Panele laminowane w salonie, sypialniach, kuchni, korytarzach i przedpokojach, z białymi listwami przypodłogowymi, oraz płytki ceramiczne na podłogach łazienek.',
  'Laminatgulv i stue, soverom, kjøkken, ganger og entreer, med hvite gulvlister, og keramiske fliser på baderomsgulvene.',
  'Laminatgolv i vardagsrum, sovrum, kök, korridorer och hallar, med vita golvlister, och keramiska plattor på badrumsgolven.')
a('.qualitySpecs.groups[0].items[1]',
  'Baldosas cerámicas solo en las paredes de la zona de ducha, y pintura plástica lisa en el resto de paredes y en los techos de yeso laminado.',
  'Carrelage en céramique uniquement sur les murs de la zone de douche, et peinture plastique lisse sur les autres murs et sur les plafonds en plaques de plâtre.',
  'Keramikfliesen nur an den Wänden des Duschbereichs und glatte Kunststoffdispersionsfarbe an den übrigen Wänden und an den Gipskartondecken.',
  'Керамическая плитка только на стенах душевой зоны и гладкая пластиковая краска на остальных стенах и гипсокартонных потолках.',
  'بلاط سيراميك على جدران منطقة الاستحمام فقط، ودهان بلاستيكي أملس على بقية الجدران وعلى الأسقف الجبسية.',
  'Keramische tegels alleen op de wanden van de douchezone, en gladde kunststofverf op de overige wanden en op de gipsplaatplafonds.',
  'Płytki ceramiczne wyłącznie na ścianach strefy prysznica oraz gładka farba plastyczna na pozostałych ścianach i sufitach z płyt gipsowo-kartonowych.',
  'Keramiske fliser kun på veggene i dusjområdet, og glatt plastmaling på de andre veggene og på himlingene av gipsplater.',
  'Keramiska plattor enbart på väggarna i duschområdet, och slät plastfärg på övriga väggar och på gipsskivetaken.')
a('.qualitySpecs.groups[1].items[0]',
  'Puertas interiores de madera lacada en blanco con manillas cromadas, y armarios modulares con balda superior y barra de colgar, con puertas del mismo color que las puertas interiores.',
  'Portes intérieures en bois laqué blanc avec poignées chromées, et placards modulaires avec une étagère haute et une barre de penderie, aux portes de la même couleur que les portes intérieures.',
  'Innentüren aus weiß lackiertem Holz mit verchromten Griffen sowie modulare Einbauschränke mit oberem Fachboden und Kleiderstange, deren Türen dieselbe Farbe wie die Innentüren haben.',
  'Межкомнатные двери из дерева, покрытого белым лаком, с хромированными ручками и модульные шкафы с верхней полкой и штангой для одежды, двери которых того же цвета, что и межкомнатные.',
  'أبواب داخلية من الخشب المطلي باللاكيه الأبيض بمقابض مطلية بالكروم، وخزائن ملابس مركّبة بوحدات مع رف علوي وعمود تعليق، بأبواب بنفس لون الأبواب الداخلية.',
  'Binnendeuren van wit gelakt hout met verchroomde klinken, en modulaire kasten met een bovenplank en een kledingroede, met deuren in dezelfde kleur als de binnendeuren.',
  'Drzwi wewnętrzne z drewna lakierowanego na biało z chromowanymi klamkami oraz modułowe szafy z górną półką i drążkiem na ubrania, z drzwiami w tym samym kolorze co drzwi wewnętrzne.',
  'Innerdører i hvitlakkert tre med forkrommede håndtak, og modulgarderober med en øvre hylle og en kleshenger, med dører i samme farge som innerdørene.',
  'Innerdörrar i vitlackerat trä med förkromade handtag, och modulgarderober med en övre hylla och en klädstång, med dörrar i samma färg som innerdörrarna.')
a('.qualitySpecs.groups[2].items[0]',
  'Muebles altos y bajos de laminado de alta presión, encimera de Silestone o similar y fregadero según el diseño del proyecto.',
  'Meubles hauts et bas en stratifié haute pression, plan de travail en Silestone ou similaire et évier selon la conception du projet.',
  'Hänge- und Unterschränke aus Hochdrucklaminat, eine Arbeitsplatte aus Silestone oder gleichwertig und eine Spüle nach dem Entwurf des Projekts.',
  'Навесные и напольные шкафы из ламината высокого давления, столешница из Silestone или аналогичная и мойка по дизайну проекта.',
  'خزائن علوية وسفلية من اللامينيت عالي الضغط، وسطح عمل من السيلستون أو ما يماثله، وحوض بحسب تصميم المشروع.',
  'Boven- en onderkasten van hogedruklaminaat, een werkblad van Silestone of gelijkwaardig en een spoelbak volgens het ontwerp van het project.',
  'Szafki wiszące i stojące z laminatu wysokociśnieniowego, blat z Silestone lub podobny oraz zlewozmywak według projektu.',
  'Over- og underskap i høytrykkslaminat, en benkeplate i Silestone eller tilsvarende og en vask etter prosjektets utforming.',
  'Över- och underskåp i högtryckslaminat, en bänkskiva i Silestone eller liknande och en diskho enligt projektets utformning.')
a('.qualitySpecs.groups[2].items[1]',
  'Frigorífico, lavadora, lavavajillas, placa de inducción, horno, microondas y campana extractora.',
  'Réfrigérateur, lave-linge, lave-vaisselle, plaque à induction, four, micro-ondes et hotte aspirante.',
  'Kühlschrank, Waschmaschine, Geschirrspüler, Induktionskochfeld, Backofen, Mikrowelle und Dunstabzugshaube mit Abluft.',
  'Холодильник, стиральная машина, посудомоечная машина, индукционная варочная панель, духовой шкаф, микроволновая печь и вытяжка.',
  'ثلاجة وغسالة وغسالة صحون وموقد حثّي وفرن وميكروويف وشفّاط مطبخ.',
  'Een koelkast, een wasmachine, een vaatwasser, een inductiekookplaat, een oven, een magnetron en een afzuigkap met afzuigventilator.',
  'Lodówka, pralka, zmywarka, płyta indukcyjna, piekarnik, kuchenka mikrofalowa i okap z wentylatorem wyciągowym.',
  'Et kjøleskap, en vaskemaskin, en oppvaskmaskin, en induksjonstopp, en stekeovn, en mikrobølgeovn og en kjøkkenvifte med avtrekk.',
  'Ett kylskåp, en tvättmaskin, en diskmaskin, en induktionshäll, en ugn, en mikrovågsugn och en köksfläkt med utsug.')
a('.qualitySpecs.groups[3].items[0]',
  'Sanitarios de porcelana vitrificada blanca, platos de ducha de resina en los dos baños y grifería monomando.',
  'Sanitaires en porcelaine vitrifiée blanche, receveurs de douche en résine dans les deux salles de bains et robinetterie mitigeur.',
  'Sanitärkeramik aus weißem Sanitärporzellan, Duschwannen aus Kunstharz in beiden Bädern und Einhebelarmaturen.',
  'Сантехника из белого глазурованного фарфора, поддоны душа из смолы в обеих ванных комнатах и однорычажные смесители.',
  'أدوات صحية من الخزف الأبيض المزجّج، وأحواض استحمام من الراتنج في الحمامين، وخلاطات بذراع واحد.',
  'Wit sanitair van verglaasd porselein, douchebakken van hars in beide badkamers en eenhendelkranen.',
  'Biała ceramika sanitarna z porcelany witryfikowanej, brodziki z żywicy w obu łazienkach oraz baterie jednouchwytowe.',
  'Hvitt sanitærutstyr i forglasset porselen, dusjbunner i harpiks i begge baderom og énhåndsblandebatterier.',
  'Vita sanitetsartiklar i förglasat porslin, duschbottnar i harts i båda badrummen och enhandsblandare.')
a('.qualitySpecs.groups[3].items[1]',
  'El lavabo va integrado en el mueble en el baño principal y suspendido de la pared en el segundo baño.',
  'Le lavabo est encastré dans le meuble vasque dans la salle de bains principale et suspendu au mur dans la seconde.',
  'Das Waschbecken ist im Hauptbad in den Waschtischunterschrank eingebaut und im zweiten Bad wandhängend.',
  'Раковина встроена в тумбу в главной ванной комнате и подвесная во второй.',
  'الحوض مدمج في وحدة الحمام في الحمام الرئيسي ومعلّق على الجدار في الحمام الثاني.',
  'De wastafel is in de hoofdbadkamer in het badkamermeubel ingebouwd en in de tweede badkamer aan de wand gehangen.',
  'Umywalka jest wbudowana w szafkę w łazience głównej i wisząca w drugiej łazience.',
  'Servanten er bygget inn i baderomsinnredningen på hovedbadet og veggmontert på det andre badet.',
  'Handfatet är inbyggt i badrumsskåpet i huvudbadrummet och väggmonterat i det andra badrummet.')
a('.qualitySpecs.groups[4].items[0]',
  'Aire frío y caliente por conductos hacia el salón, los dormitorios y la cocina, con un sistema de bomba de calor solo en la cocina.',
  'Air chaud et froid par gaines vers le séjour, les chambres et la cuisine, avec un système de pompe à chaleur dans la cuisine seulement.',
  'Warme und kühle Luft über Kanäle ins Wohnzimmer, in die Schlafzimmer und in die Küche, mit einem Wärmepumpensystem allein in der Küche.',
  'Горячий и холодный воздух по воздуховодам в гостиную, спальни и кухню, с системой теплового насоса только на кухне.',
  'هواء ساخن وبارد عبر مجاري التهوية إلى غرفة المعيشة وغرف النوم والمطبخ، مع نظام مضخة حرارية في المطبخ وحده.',
  'Warme en koude lucht via kanalen naar de woonkamer, de slaapkamers en de keuken, met een warmtepompsysteem alleen in de keuken.',
  'Ciepłe i zimne powietrze kanałami do salonu, sypialni i kuchni, z układem pompy ciepła wyłącznie w kuchni.',
  'Varm og kald luft gjennom kanaler til stue, soverom og kjøkken, med et varmepumpesystem bare på kjøkkenet.',
  'Varm och kall luft genom kanaler till vardagsrum, sovrum och kök, med ett värmepumpssystem enbart i köket.')
a('.qualitySpecs.groups[4].items[1]',
  'Agua caliente mediante un sistema de aerotermia y ventilación mecánica individual en las cocinas y los baños.',
  'Eau chaude par un système aérothermique et ventilation mécanique individuelle dans les cuisines et les salles de bains.',
  'Warmwasser über ein aerothermisches System und individuelle mechanische Lüftung in Küchen und Bädern.',
  'Горячая вода от аэротермальной системы и индивидуальная механическая вентиляция на кухнях и в ванных комнатах.',
  'ماء ساخن من نظام الطاقة الهوائية الحرارية (إيروثيرميا)، وتهوية ميكانيكية فردية في المطابخ والحمامات.',
  'Warm water van een aerothermisch systeem en individuele mechanische ventilatie in de keukens en badkamers.',
  'Ciepła woda z systemu aerotermalnego i indywidualna wentylacja mechaniczna w kuchniach i łazienkach.',
  'Varmtvann fra et aerotermisk system og individuell mekanisk ventilasjon på kjøkkenene og baderomene.',
  'Varmvatten från ett aerotermiskt system och individuell mekanisk ventilation i köken och badrummen.')
a('.qualitySpecs.groups[5].items[0]',
  'Tomas de TV y de red ethernet según la norma de telecomunicaciones ICT 2 en el salón, la cocina y los dormitorios.',
  'Prises TV et Ethernet selon la norme de télécommunications ICT 2 dans le séjour, la cuisine et les chambres.',
  'TV- und Ethernet-Anschlüsse nach dem Telekommunikationsstandard ICT 2 im Wohnzimmer, in der Küche und in den Schlafzimmern.',
  'Телевизионные и Ethernet-розетки по стандарту телекоммуникаций ICT 2 в гостиной, на кухне и в спальнях.',
  'وصلات تلفزيون وإيثرنت وفق معيار الاتصالات ICT 2 في غرفة المعيشة والمطبخ وغرف النوم.',
  'Tv- en ethernetaansluitingen volgens de telecommunicatienorm ICT 2 in de woonkamer, de keuken en de slaapkamers.',
  'Przyłącza TV i Ethernet zgodne ze standardem telekomunikacyjnym ICT 2 w salonie, kuchni i sypialniach.',
  'TV- og ethernet-tilkoblinger etter telekommunikasjonsstandarden ICT 2 i stue, kjøkken og soverom.',
  'Tv- och ethernetuttag enligt telekommunikationsstandarden ICT 2 i vardagsrum, kök och sovrum.')
a('.qualitySpecs.groups[6].name',
  'Seguridad', 'Sécurité', 'Sicherheit', 'Безопасность', 'الأمان', 'Veiligheid', 'Bezpieczeństwo', 'Sikkerhet', 'Säkerhet')
a('.qualitySpecs.groups[6].items[0]',
  'Puerta de entrada de seguridad con mirilla y cerradura de seguridad, y cristales y herrajes de seguridad en las ventanas y puertas de las viviendas de planta baja.',
  'Porte d’entrée de sécurité avec judas et serrure de sécurité, et vitrages et quincaillerie de sécurité aux fenêtres et aux portes des logements du rez-de-chaussée.',
  'Eine Sicherheitseingangstür mit Spion und Sicherheitsschloss sowie Sicherheitsglas und -beschläge an den Fenstern und Türen der Erdgeschosswohnungen.',
  'Входная бронированная дверь с глазком и замком повышенной безопасности, а также безопасное стекло и фурнитура на окнах и дверях квартир на первом этаже.',
  'باب مدخل أمان مزوّد بعين سحرية وقفل أمان، وزجاج وإكسسوارات أمان على نوافذ وأبواب مساكن الطابق الأرضي.',
  'Een veiligheidsvoordeur met kijkgaatje en veiligheidsslot, en veiligheidsglas en -beslag op de ramen en deuren van de woningen op de begane grond.',
  'Drzwi wejściowe antywłamaniowe z wizjerem i zamkiem bezpieczeństwa oraz szkło i okucia bezpieczne w oknach i drzwiach lokali na parterze.',
  'En sikkerhetsinngangsdør med dørspion og sikkerhetslås, og sikkerhetsglass og -beslag på vinduene og dørene i boligene i første etasje.',
  'En säkerhetsingångsdörr med titthål och säkerhetslås, och säkerhetsglas och -beslag på fönstren och dörrarna i bostäderna i bottenvåningen.')
a('.qualitySpecs.groups[6].items[1]',
  'Un complejo cerrado de acceso privado, llaves maestras para la urbanización, el portal del bloque, las viviendas y el garaje, y un videoportero automático en la entrada de la urbanización y en el portal del bloque.',
  'Une résidence fermée à accès privé, un passe général pour la résidence, le hall de l’immeuble, les logements et le garage, et un système de vidéophone automatique à l’entrée de la résidence et dans le hall de l’immeuble.',
  'Eine geschlossene Anlage mit ausschließlich privatem Zugang, Generalschlüssel für die Anlage, den Hausflur, die Wohnungen und die Garage sowie eine automatische Videosprechanlage am Eingang der Anlage und im Hausflur.',
  'Закрытая территория с частным доступом, мастер-ключи от территории, подъезда, квартир и гаража, а также автоматическая система видеодомофона у входа на территорию и в подъезде.',
  'مجمع مغلق بمدخل خاص فقط، ومفاتيح رئيسية للمجمع ومدخل المبنى والمساكن والمرآب، ونظام اتصال مرئي تلقائي عند مدخل المجمع وفي مدخل المبنى.',
  'Een afgesloten complex met uitsluitend privétoegang, hoofdsleutels voor het complex, de hal van het blok, de woningen en de garage, en een automatisch videofoonsysteem bij de ingang van het complex en in de hal van het blok.',
  'Zamknięty kompleks z wyłącznie prywatnym dostępem, klucze uniwersalne do osiedla, klatki schodowej, lokali i garażu oraz automatyczny system wideodomofonowy przy wejściu na osiedle i na klatce schodowej.',
  'Et lukket anlegg med kun privat adkomst, hovednøkler til anlegget, blokkens inngangsparti, boligene og garasjen, og et automatisk videoporttelefonsystem ved inngangen til anlegget og i blokkens inngangsparti.',
  'Ett slutet område med enbart privat tillträde, huvudnycklar till området, husets entré, bostäderna och garaget, och ett automatiskt videoporttelefonsystem vid områdets ingång och i husets entré.')
a('.qualitySpecs.groups[7].items[0]',
  'Piscinas de chapoteo con cloración salina, un gimnasio totalmente equipado, una sauna y una zona de spa, una sala de coworking y una sala de club social.',
  'Pataugeoires au chlore salin, une salle de sport entièrement équipée, un sauna et un espace spa, une salle de coworking et une salle de club social.',
  'Planschbecken mit Salzwasserchlorierung, ein voll ausgestatteter Fitnessraum, eine Sauna und ein Spa-Bereich, ein Coworking-Raum und ein Social-Club-Raum.',
  'Мелкие бассейны с солевой хлорацией, полностью оборудованный тренажёрный зал, сауна и спа-зона, комната коворкинга и комната соушл-клуба.',
  'مسابح ضحلة بالكلور الملحي، ونادٍ رياضي مجهز بالكامل، وساونا ومنطقة سبا، وغرفة عمل مشتركة وغرفة نادٍ اجتماعي.',
  'Pierenbadjes met zoutchlorering, een volledig uitgeruste sportruimte, een sauna en een spa-ruimte, een coworkingruimte en een ruimte voor de sociale club.',
  'Brodziki z chlorowaniem solą, w pełni wyposażona siłownia, sauna i strefa spa, sala coworkingowa i sala klubu społecznego.',
  'Plaskebasseng med saltklorering, et fullt utstyrt treningsrom, en badstue og et spa-område, et coworking-rom og et rom for sosial klubb.',
  'Plaskpooler med saltklorering, ett fullt utrustat gym, en bastu och ett spaområde, ett coworking-rum och ett rum för socialklubben.')
a('.qualitySpecs.groups[7].items[1]',
  'Jardines con iluminación y riego automático, y un desfibrilador portátil en las zonas comunes.',
  'Jardins avec éclairage et arrosage automatique, et un défibrillateur portable dans les parties communes.',
  'Gärten mit Beleuchtung und automatischer Bewässerung sowie ein tragbarer Defibrillator in den Gemeinschaftsbereichen.',
  'Сады с освещением и автоматическим поливом и портативный дефибриллятор в общих зонах.',
  'حدائق بإضاءة وري تلقائي، وجهاز إزالة رجفان محمول في المناطق المشتركة.',
  'Tuinen met verlichting en automatische bevloeiing, en een draagbare defibrillator in de gemeenschappelijke ruimten.',
  'Ogrody z oświetleniem i automatycznym nawadnianiem oraz przenośny defibrylator w częściach wspólnych.',
  'Hager med belysning og automatisk vanning, og en bærbar hjertestarter i fellesarealene.',
  'Trädgårdar med belysning och automatisk bevattning, och en bärbar hjärtstartare i de gemensamma utrymmena.')
a('.qualitySpecs.groups[8].items[0]',
  'Un garaje con puerta de acceso automática y apertura a distancia, un punto de recarga para vehículos eléctricos preinstalado y ascensores adaptados para el acceso, con puertas automáticas.',
  'Un garage avec porte d’accès automatique et ouverture à distance, une borne de recharge pour véhicules électriques préinstallée et des ascenseurs adaptés à l’accès, à portes automatiques.',
  'Eine Garage mit automatischem Zufahrtstor und Fernbedienung, eine vorinstallierte Ladestation für Elektrofahrzeuge und barrierefreie Aufzüge mit automatischen Türen.',
  'Гараж с автоматическими въездными воротами и дистанционным открыванием, предустановленная зарядная станция для электромобилей и лифты, адаптированные для доступа, с автоматическими дверями.',
  'مرآب بباب دخول أوتوماتيكي وفتح عن بُعد، ومحطة شحن للمركبات الكهربائية مُجهَّزة مسبقًا، ومصاعد مهيأة لسهولة الوصول بأبواب أوتوماتيكية.',
  'Een garage met een automatische toegangsdeur en afstandsbediening, een voorgeïnstalleerd laadstation voor elektrische voertuigen en liften die toegankelijk zijn aangepast, met automatische deuren.',
  'Garaż z automatycznymi drzwiami wjazdowymi i zdalnym otwieraniem, fabrycznie przygotowana stacja ładowania pojazdów elektrycznych oraz windy dostosowane do dostępności, z automatycznymi drzwiami.',
  'En garasje med automatisk adkomstdør og fjernåpning, en forhåndsinstallert ladestasjon for elbiler og heiser tilrettelagt for tilgjengelighet, med automatiske dører.',
  'Ett garage med automatisk infartsdörr och fjärröppning, en förinstallerad laddstation för elfordon och hissar anpassade för tillgänglighet, med automatiska dörrar.')

# ---- residences ------------------------------------------------------------------------------------

a('.residences.headlineHtml',
  'Seis viviendas, <em>cada una con terraza o jardín</em>', 'Six logements, <em>chacun avec une terrasse ou un jardin</em>',
  'Sechs Wohnungen, <em>jede mit Terrasse oder Garten</em>', 'Шесть квартир, <em>у каждой терраса или сад</em>',
  'ست مساكن، <em>لكل منها تراس أو حديقة</em>', 'Zes woningen, <em>elk met een terras of een tuin</em>',
  'Sześć lokali, <em>każdy z tarasem lub ogrodem</em>', 'Seks boliger, <em>hver med en terrasse eller en hage</em>',
  'Sex bostäder, <em>var och en med en terrass eller en trädgård</em>')
a('.residences.copy',
  'La lista de precios da las seis viviendas disponibles por bloque, portal y planta. La tabla de abajo recoge cada una con su precio.',
  'La liste de prix donne les six logements disponibles par bloc, entrée et étage. Le tableau ci-dessous les liste chacun avec son prix.',
  'Die Preisliste führt die sechs verfügbaren Wohnungen nach Block, Portal und Stockwerk auf. Die Tabelle unten nennt jede mit ihrem Preis.',
  'В прайс-листе шесть доступных квартир указаны по блоку, подъезду и этажу. В таблице ниже каждая приведена с ценой.',
  'تذكر قائمة الأسعار المساكن الستة المتاحة بحسب المبنى والمدخل والطابق. ويورد الجدول أدناه كلًا منها مع سعره.',
  'De prijslijst geeft de zes beschikbare woningen per blok, portaal en verdieping. De tabel hieronder vermeldt elk met zijn prijs.',
  'Cennik podaje sześć dostępnych lokali według bloku, klatki i piętra. Poniższa tabela wymienia każdy z nich wraz z ceną.',
  'Prislisten oppgir de seks tilgjengelige boligene etter blokk, oppgang og etasje. Tabellen under viser hver av dem med pris.',
  'Prislistan anger de sex tillgängliga bostäderna efter block, uppgång och våning. Tabellen nedan listar var och en med sitt pris.')
a('.residences.items[0].name',
  'Las viviendas de dos dormitorios', 'Les logements de deux chambres', 'Die Wohnungen mit zwei Schlafzimmern', 'Квартиры с двумя спальнями',
  'المساكن بغرفتي نوم', 'De woningen met twee slaapkamers', 'Lokale z dwiema sypialniami', 'Boligene med to soverom', 'Bostäderna med två sovrum')
a('.residences.items[1].name',
  'Las viviendas de tres dormitorios', 'Les logements de trois chambres', 'Die Wohnungen mit drei Schlafzimmern', 'Квартиры с тремя спальнями',
  'المساكن بثلاث غرف نوم', 'De woningen met drie slaapkamers', 'Lokale z trzema sypialniami', 'Boligene med tre soverom', 'Bostäderna med tre sovrum')
a('.residences.items[0].points[0]',
  'B4-P8-1D en la primera planta, B4-P8-0B en la planta baja y el ático B4-P8-PH-B: dos dormitorios y dos baños cada una.',
  'B4-P8-1D au premier étage, B4-P8-0B au rez-de-chaussée et le penthouse B4-P8-PH-B : deux chambres et deux salles de bains chacun.',
  'B4-P8-1D im ersten Obergeschoss, B4-P8-0B im Erdgeschoss und das Penthouse B4-P8-PH-B: jeweils zwei Schlafzimmer und zwei Bäder.',
  'B4-P8-1D на втором этаже, B4-P8-0B на первом этаже и пентхаус B4-P8-PH-B: в каждой по две спальни и две ванные комнаты.',
  'B4-P8-1D في الطابق الأول، وB4-P8-0B في الطابق الأرضي، والبنتهاوس B4-P8-PH-B: غرفتا نوم وحمامان في كل منها.',
  'B4-P8-1D op de eerste verdieping, B4-P8-0B op de begane grond en het penthouse B4-P8-PH-B: elk met twee slaapkamers en twee badkamers.',
  'B4-P8-1D na pierwszym piętrze, B4-P8-0B na parterze i penthouse B4-P8-PH-B: po dwie sypialnie i dwie łazienki w każdym.',
  'B4-P8-1D i andre etasje, B4-P8-0B i første etasje og toppleiligheten B4-P8-PH-B: to soverom og to bad i hver.',
  'B4-P8-1D på första våningen, B4-P8-0B i bottenvåningen och takvåningen B4-P8-PH-B: två sovrum och två badrum i var och en.')
a('.residences.items[0].points[1]',
  'Superficies interiores de {N67.61}, {N65.79} y {N77.05} {U}, con terrazas de {N11.06}, {N27.97} y {N36.96} {U}.',
  'Surfaces intérieures de {N67.61}, {N65.79} et {N77.05} {U}, avec des terrasses de {N11.06}, {N27.97} et {N36.96} {U}.',
  'Innenflächen von {N67.61}, {N65.79} und {N77.05} {U}, mit Terrassen von {N11.06}, {N27.97} und {N36.96} {U}.',
  'Внутренняя площадь {N67.61}, {N65.79} и {N77.05} {U}, террасы {N11.06}, {N27.97} и {N36.96} {U}.',
  'مساحات داخلية تبلغ {N67.61} و{N65.79} و{N77.05} {U}، مع تراسات مساحتها {N11.06} و{N27.97} و{N36.96} {U}.',
  'Binnenoppervlakten van {N67.61}, {N65.79} en {N77.05} {U}, met terrassen van {N11.06}, {N27.97} en {N36.96} {U}.',
  'Powierzchnie wewnętrzne {N67.61}, {N65.79} i {N77.05} {U}, z tarasami o powierzchni {N11.06}, {N27.97} i {N36.96} {U}.',
  'Innvendige arealer på {N67.61}, {N65.79} og {N77.05} {U}, med terrasser på {N11.06}, {N27.97} og {N36.96} {U}.',
  'Inomhusytor på {N67.61}, {N65.79} och {N77.05} {U}, med terrasser på {N11.06}, {N27.97} och {N36.96} {U}.')
a('.residences.items[0].points[2]',
  'Una plaza de garaje y un trastero cada una, por {E320000}, {E345000} y {E480000}.',
  'Une place de garage et une cave chacun, pour {E320000}, {E345000} et {E480000}.',
  'Jeweils ein Garagenstellplatz und ein Abstellraum, für {E320000}, {E345000} und {E480000}.',
  'В каждой место в гараже и кладовая, за {E320000}, {E345000} и {E480000}.',
  'موقف في المرآب ومخزن لكل منها، بسعر {E320000} و{E345000} و{E480000}.',
  'Elk met een garageplaats en een berging, voor {E320000}, {E345000} en {E480000}.',
  'W każdym miejsce w garażu i komórka lokatorska, za {E320000}, {E345000} i {E480000}.',
  'En garasjeplass og en bod hver, for {E320000}, {E345000} og {E480000}.',
  'En garageplats och ett förråd var, för {E320000}, {E345000} och {E480000}.')
a('.residences.items[1].points[0]',
  'B4-P7-1D en la primera planta, B4-P8-2A en la segunda planta y B6-P11-0A en la planta baja: tres dormitorios y dos baños cada una.',
  'B4-P7-1D au premier étage, B4-P8-2A au deuxième étage et B6-P11-0A au rez-de-chaussée : trois chambres et deux salles de bains chacun.',
  'B4-P7-1D im ersten Obergeschoss, B4-P8-2A im zweiten Obergeschoss und B6-P11-0A im Erdgeschoss: jeweils drei Schlafzimmer und zwei Bäder.',
  'B4-P7-1D на втором этаже, B4-P8-2A на третьем этаже и B6-P11-0A на первом этаже: в каждой по три спальни и две ванные комнаты.',
  'B4-P7-1D في الطابق الأول، وB4-P8-2A في الطابق الثاني، وB6-P11-0A في الطابق الأرضي: ثلاث غرف نوم وحمامان في كل منها.',
  'B4-P7-1D op de eerste verdieping, B4-P8-2A op de tweede verdieping en B6-P11-0A op de begane grond: elk met drie slaapkamers en twee badkamers.',
  'B4-P7-1D na pierwszym piętrze, B4-P8-2A na drugim piętrze i B6-P11-0A na parterze: po trzy sypialnie i dwie łazienki w każdym.',
  'B4-P7-1D i andre etasje, B4-P8-2A i tredje etasje og B6-P11-0A i første etasje: tre soverom og to bad i hver.',
  'B4-P7-1D på första våningen, B4-P8-2A på andra våningen och B6-P11-0A i bottenvåningen: tre sovrum och två badrum i var och en.')
a('.residences.items[1].points[1]',
  'Todas tienen {N83.78} {U} de superficie interior. Las dos viviendas de las plantas altas tienen terrazas de {N21.92} y {N24.71} {U}, y la de planta baja una terraza cubierta de {N17.91} {U} y un jardín delantero de {N49.54} {U}.',
  'Chacun a {N83.78} {U} de surface intérieure. Les deux logements des étages ont des terrasses de {N21.92} et {N24.71} {U}, et celui du rez-de-chaussée une terrasse couverte de {N17.91} {U} et un jardin sur le devant de {N49.54} {U}.',
  'Jede hat {N83.78} {U} Innenfläche. Die beiden oberen Wohnungen haben Terrassen von {N21.92} und {N24.71} {U}, die Erdgeschosswohnung eine überdachte Terrasse von {N17.91} {U} und einen Vorgarten von {N49.54} {U}.',
  'У каждой {N83.78} {U} внутренней площади. У двух квартир на верхних этажах террасы {N21.92} и {N24.71} {U}, у квартиры на первом этаже — крытая терраса {N17.91} {U} и палисадник {N49.54} {U}.',
  'لكل منها {N83.78} {U} من المساحة الداخلية. وللمسكنين العلويين تراسان مساحتهما {N21.92} و{N24.71} {U}، ولمسكن الطابق الأرضي تراس مغطى مساحته {N17.91} {U} وحديقة أمامية مساحتها {N49.54} {U}.',
  'Elk heeft {N83.78} {U} binnenoppervlak. De twee bovenste woningen hebben terrassen van {N21.92} en {N24.71} {U}, en de woning op de begane grond een overdekt terras van {N17.91} {U} en een voortuin van {N49.54} {U}.',
  'Każdy ma {N83.78} {U} powierzchni wewnętrznej. Dwa lokale na wyższych piętrach mają tarasy o powierzchni {N21.92} i {N24.71} {U}, a lokal na parterze zadaszony taras o powierzchni {N17.91} {U} i ogródek przed domem o powierzchni {N49.54} {U}.',
  'Hver har {N83.78} {U} innvendig areal. De to øvre boligene har terrasser på {N21.92} og {N24.71} {U}, og boligen i første etasje en overbygd terrasse på {N17.91} {U} og en forhage på {N49.54} {U}.',
  'Var och en har {N83.78} {U} inomhusyta. De två övre bostäderna har terrasser på {N21.92} och {N24.71} {U}, och bostaden i bottenvåningen en överbyggd terrass på {N17.91} {U} och en trädgård framför på {N49.54} {U}.')
a('.residences.items[1].points[2]',
  'Una plaza de garaje y un trastero cada una, por {E425000}, {E430000} y {E440000}.',
  'Une place de garage et une cave chacun, pour {E425000}, {E430000} et {E440000}.',
  'Jeweils ein Garagenstellplatz und ein Abstellraum, für {E425000}, {E430000} und {E440000}.',
  'В каждой место в гараже и кладовая, за {E425000}, {E430000} и {E440000}.',
  'موقف في المرآب ومخزن لكل منها، بسعر {E425000} و{E430000} و{E440000}.',
  'Elk met een garageplaats en een berging, voor {E425000}, {E430000} en {E440000}.',
  'W każdym miejsce w garażu i komórka lokatorska, za {E425000}, {E430000} i {E440000}.',
  'En garasjeplass og en bod hver, for {E425000}, {E430000} og {E440000}.',
  'En garageplats och ett förråd var, för {E425000}, {E430000} och {E440000}.')

# ---- lifestyle -------------------------------------------------------------------------------------

a('.lifestyle.headlineHtml',
  'Terrazas, <em>una piscina</em> y un spa', 'Des terrasses, <em>une piscine</em> et un spa', 'Terrassen, <em>ein Pool</em> und ein Spa',
  'Террасы, <em>бассейн</em> и спа', 'تراسات، <em>ومسبح</em> وسبا', 'Terrassen, <em>een zwembad</em> en een spa',
  'Tarasy, <em>basen</em> i spa', 'Terrasser, <em>et basseng</em> og et spa', 'Terrasser, <em>en pool</em> och ett spa')
a('.lifestyle.copy',
  'La vida aquí es al aire libre y compartida: la terraza o el jardín de la vivienda, la piscina central con su zona chill-out, y el spa, el gimnasio, el club social y el espacio de coworking.',
  'La vie ici se passe dehors et en partage : la terrasse ou le jardin du logement, la piscine centrale avec son espace de détente, et le spa, la salle de sport, le club social et l’espace de coworking.',
  'Das Leben hier spielt sich draußen und gemeinsam ab: die Terrasse oder der Garten der Wohnung, der zentrale Pool mit Chill-out-Bereich sowie Spa, Fitnessraum, Social Club und Coworking-Bereich.',
  'Жизнь здесь проходит на открытом воздухе и вместе с соседями: терраса или сад квартиры, центральный бассейн с зоной отдыха, а также спа, тренажёрный зал, соушл-клуб и коворкинг.',
  'الحياة هنا في الهواء الطلق ومشتركة: تراس المسكن أو حديقته، والمسبح المركزي بمنطقة الاسترخاء، والسبا والنادي الرياضي والنادي الاجتماعي ومساحة العمل المشتركة.',
  'Het leven hier speelt zich buiten en samen af: het terras of de tuin van de woning, het centrale zwembad met chill-outzone, en de spa, de sportruimte, de sociale club en de coworkingruimte.',
  'Życie tutaj toczy się na zewnątrz i wspólnie: taras lub ogród lokalu, centralny basen ze strefą relaksu oraz spa, siłownia, klub społeczny i przestrzeń coworkingowa.',
  'Livet her foregår ute og sammen: boligens terrasse eller hage, det sentrale bassenget med chill-out-sonen, og spaet, treningsrommet, den sosiale klubben og coworking-området.',
  'Livet här levs utomhus och tillsammans: bostadens terrass eller trädgård, den centrala poolen med chill-out-ytan, och spat, gymmet, socialklubben och coworking-ytan.')
a('.lifestyle.panels[0][1]',
  'Una piscina central con zona chill-out, en jardines paisajísticos con riego automático, tal como lo describe el folleto. La memoria de calidades menciona piscinas de chapoteo con cloración salina.',
  'Une piscine centrale avec un espace de détente, dans des jardins paysagers à arrosage automatique, comme la brochure la décrit. Le descriptif des matériaux mentionne des pataugeoires au chlore salin.',
  'Ein zentraler Pool mit Chill-out-Bereich in gepflegten Gärten mit automatischer Bewässerung, so beschreibt es die Broschüre. Die Bau- und Ausstattungsbeschreibung nennt Planschbecken mit Salzwasserchlorierung.',
  'Центральный бассейн с зоной отдыха в ландшафтных садах с автоматическим поливом, как его описывает брошюра. В спецификации материалов указаны мелкие бассейны с солевой хлорацией.',
  'مسبح مركزي بمنطقة استرخاء، في حدائق مُنسَّقة بري تلقائي، كما يصفه الكتيّب. وتذكر مواصفات المواد مسابح ضحلة بالكلور الملحي.',
  'Een centraal zwembad met chill-outzone, in aangelegde tuinen met automatische bevloeiing, zoals de brochure het beschrijft. De specificatie noemt pierenbadjes met zoutchlorering.',
  'Centralny basen ze strefą relaksu w zagospodarowanych ogrodach z automatycznym nawadnianiem, tak jak opisuje go broszura. Specyfikacja wymienia brodziki z chlorowaniem solą.',
  'Et sentralt basseng med en chill-out-sone, i opparbeidede hager med automatisk vanning, slik brosjyren beskriver det. Spesifikasjonen nevner plaskebasseng med saltklorering.',
  'En central pool med en chill-out-yta, i anlagda trädgårdar med automatisk bevattning, så som broschyren beskriver den. Specifikationen nämner plaskpooler med saltklorering.')
a('.lifestyle.panels[1][0]',
  'Bienestar', 'Bien-être', 'Wellness', 'Здоровье и отдых', 'العناية بالنفس', 'Welzijn', 'Dobre samopoczucie', 'Velvære', 'Välmående')
a('.lifestyle.panels[1][1]',
  'Una zona de spa con sauna, y un gimnasio con equipos para cardio, fuerza y estiramientos.',
  'Un espace spa avec sauna, et une salle de sport équipée pour le cardio, la musculation et les étirements.',
  'Ein Spa-Bereich mit Sauna und ein Fitnessraum mit Geräten für Cardio, Kraft und Dehnung.',
  'Спа-зона с сауной и тренажёрный зал с оборудованием для кардио, силовых тренировок и растяжки.',
  'منطقة سبا مع ساونا، ونادٍ رياضي بمعدات للكارديو والقوة والإطالة.',
  'Een spa-ruimte met sauna en een sportruimte met toestellen voor cardio, kracht en rekken.',
  'Strefa spa z sauną oraz siłownia ze sprzętem do cardio, treningu siłowego i rozciągania.',
  'Et spa-område med badstue og et treningsrom med utstyr for kondisjon, styrke og tøyning.',
  'Ett spaområde med bastu och ett gym med utrustning för kondition, styrka och stretching.')
a('.lifestyle.panels[2][0]',
  'Trabajar y reunirse', 'Travailler et se retrouver', 'Arbeiten und sich treffen', 'Работа и встречи', 'العمل واللقاء', 'Werken en ontmoeten', 'Praca i spotkania', 'Jobbe og møtes', 'Arbeta och mötas')
a('.lifestyle.panels[2][1]',
  'Un espacio de coworking con zonas luminosas y bien iluminadas, y una sala de club social para encontrarse con los vecinos y los amigos.',
  'Un espace de coworking avec des zones claires et bien éclairées, et une salle de club social pour retrouver ses voisins et ses amis.',
  'Ein Coworking-Bereich mit hellen, gut beleuchteten Zonen und ein Social-Club-Raum, um Nachbarn und Freunde zu treffen.',
  'Коворкинг со светлыми, хорошо освещёнными зонами и комната соушл-клуба, где можно встретиться с соседями и друзьями.',
  'مساحة عمل مشتركة بمناطق مشرقة وجيدة الإضاءة، وغرفة نادٍ اجتماعي للقاء الجيران والأصدقاء.',
  'Een coworkingruimte met lichte, goed verlichte zones en een ruimte voor de sociale club om buren en vrienden te ontmoeten.',
  'Przestrzeń coworkingowa z jasnymi, dobrze oświetlonymi strefami oraz sala klubu społecznego do spotkań z sąsiadami i przyjaciółmi.',
  'Et coworking-område med lyse, godt belyste soner og et rom for sosial klubb der man kan møte naboer og venner.',
  'En coworking-yta med ljusa, väl belysta zoner och ett rum för socialklubben där man kan träffa grannar och vänner.')
a('.lifestyle.panels[3][0]',
  'El parque', 'Le parc', 'Der Park', 'Парк', 'الحديقة العامة', 'Het park', 'Park', 'Parken', 'Parken')
a('.lifestyle.panels[3][1]',
  'El folleto dice que a 800 m de la promoción se está construyendo uno de los mayores parques de Andalucía, con un lago navegable, rocódromos, un carril bici y un anfiteatro al aire libre.',
  'La brochure indique que l’un des plus grands parcs d’Andalousie est en construction à 800 m du programme, avec un lac navigable, des murs d’escalade, une piste cyclable et un amphithéâtre en plein air.',
  'Die Broschüre sagt, dass 800 m von der Anlage entfernt einer der größten Parks Andalusiens gebaut wird, mit einem schiffbaren See, Kletterwänden, einem Radweg und einem Freilichtamphitheater.',
  'В брошюре сказано, что в 800 м от комплекса строится один из крупнейших парков Андалусии с судоходным озером, скалодромами, велодорожкой и амфитеатром под открытым небом.',
  'يقول الكتيّب إن أحد أكبر المتنزهات في الأندلس يُبنى على بعد 800 م من المشروع، وفيه بحيرة صالحة للإبحار وجدران تسلق ومسار للدراجات ومدرج في الهواء الطلق.',
  'De brochure zegt dat op 800 m van de ontwikkeling een van de grootste parken van Andalusië wordt aangelegd, met een bevaarbaar meer, klimwanden, een fietspad en een openluchtamfitheater.',
  'Broszura podaje, że 800 m od inwestycji powstaje jeden z największych parków w Andaluzji, z żeglownym jeziorem, ściankami wspinaczkowymi, ścieżką rowerową i amfiteatrem na wolnym powietrzu.',
  'Brosjyren sier at en av de største parkene i Andalusia bygges 800 m fra prosjektet, med en seilbar innsjø, klatrevegger, en sykkelsti og et utendørs amfiteater.',
  'Broschyren säger att en av Andalusiens största parker byggs 800 m från projektet, med en farbar sjö, klättringsväggar, en cykelväg och en utomhusamfiteater.')

# ---- location --------------------------------------------------------------------------------------

a('.location.headlineHtml',
  'Mijas Costa, <em>entre Marbella y Málaga</em>', 'Mijas Costa, <em>entre Marbella et Málaga</em>', 'Mijas Costa, <em>zwischen Marbella und Málaga</em>',
  'Михас-Коста, <em>между Марбельей и Малагой</em>', 'ميخاس كوستا، <em>بين ماربيا ومالقة</em>', 'Mijas Costa, <em>tussen Marbella en Málaga</em>',
  'Mijas Costa, <em>między Marbellą a Málagą</em>', 'Mijas Costa, <em>mellom Marbella og Málaga</em>', 'Mijas Costa, <em>mellan Marbella och Málaga</em>')
a('.location.copy',
  'La promoción está en Mijas Costa. El mapa del folleto señala el centro comercial y parque comercial Miramar, un hipódromo, un club de pádel y dos campos de golf a pocos kilómetros, con Fuengirola y La Cala de Mijas en la costa, y da 40 km hasta Marbella y 41 km hasta Málaga. Los documentos no dan dirección ni coordenadas de la parcela, así que el mapa muestra la zona de Mijas Costa.',
  'Le programme est à Mijas Costa. La carte de la brochure signale le centre commercial et parc d’activités commerciales Miramar, un hippodrome, un club de padel et deux golfs à quelques kilomètres, avec Fuengirola et La Cala de Mijas sur la côte, et donne 40 km jusqu’à Marbella et 41 km jusqu’à Málaga. Les documents ne donnent ni adresse ni coordonnées de la parcelle ; la carte montre donc la zone de Mijas Costa.',
  'Die Anlage liegt in Mijas Costa. Die Karte der Broschüre zeigt das Einkaufszentrum und den Fachmarkt Miramar, eine Pferderennbahn, einen Padelclub und zwei Golfplätze in wenigen Kilometern Entfernung, mit Fuengirola und La Cala de Mijas an der Küste, und nennt 40 km bis Marbella und 41 km bis Málaga. Die Unterlagen nennen weder Adresse noch Koordinaten des Grundstücks, daher zeigt die Karte das Gebiet Mijas Costa.',
  'Комплекс находится в Михас-Коста. На карте в брошюре отмечены торговый центр и торговый парк Miramar, ипподром, падел-клуб и два поля для гольфа в нескольких километрах, а на побережье — Фуэнхирола и Ла-Кала-де-Михас; указано 40 км до Марбельи и 41 км до Малаги. Адрес и координаты участка в документах не указаны, поэтому на карте показан район Михас-Коста.',
  'يقع المشروع في ميخاس كوستا. تُظهر خريطة الكتيّب مركز ميرامار التجاري ومجمع المتاجر وحلبة سباق خيل ونادي بادل وملعبي غولف على بعد بضعة كيلومترات، مع فوينخيرولا ولا كالا دي ميخاس على الساحل، وتذكر 40 كم إلى ماربيا و41 كم إلى مالقة. لا تذكر الوثائق عنوان القطعة ولا إحداثياتها، ولذلك تعرض الخريطة منطقة ميخاس كوستا.',
  'De ontwikkeling ligt in Mijas Costa. De kaart in de brochure toont het winkelcentrum en de retailpark Miramar, een renbaan, een padelclub en twee golfbanen op enkele kilometers afstand, met Fuengirola en La Cala de Mijas aan de kust, en geeft 40 km naar Marbella en 41 km naar Málaga. De documenten geven geen adres of coördinaat van het perceel, dus de kaart toont het gebied Mijas Costa.',
  'Inwestycja znajduje się w Mijas Costa. Mapa w broszurze zaznacza centrum handlowe i park handlowy Miramar, hipodrom, klub padla i dwa pola golfowe w odległości kilku kilometrów, a na wybrzeżu Fuengirolę i La Cala de Mijas, oraz podaje 40 km do Marbelli i 41 km do Málagi. Dokumenty nie podają adresu ani współrzędnych działki, dlatego mapa pokazuje obszar Mijas Costa.',
  'Prosjektet ligger i Mijas Costa. Kartet i brosjyren markerer kjøpesenteret og handelsparken Miramar, en travbane, en padelklubb og to golfbaner innen noen få kilometer, med Fuengirola og La Cala de Mijas ved kysten, og oppgir 40 km til Marbella og 41 km til Málaga. Dokumentene oppgir verken adresse eller koordinater for tomten, så kartet viser området Mijas Costa.',
  'Projektet ligger i Mijas Costa. Kartan i broschyren markerar köpcentret och handelsparken Miramar, en travbana, en padelklubb och två golfbanor inom några kilometer, med Fuengirola och La Cala de Mijas vid kusten, och anger 40 km till Marbella och 41 km till Málaga. Dokumenten anger varken adress eller koordinater för tomten, så kartan visar området Mijas Costa.')
a('.location.distances[0][1]', '40 km', '40 km', '40 km', '40 км', '40 كم', '40 km', '40 km', '40 km', '40 km')
a('.location.distances[1][1]', '41 km', '41 km', '41 km', '41 км', '41 كم', '41 km', '41 km', '41 km', '41 km')
a('.location.distances[2][0]',
  'Gran parque (en construcción)', 'Grand parc (en construction)', 'Großer Park (im Bau)', 'Большой парк (строится)', 'حديقة عامة كبيرة (قيد الإنشاء)',
  'Groot park (in aanleg)', 'Duży park (w budowie)', 'Stor park (under bygging)', 'Stor park (under byggnad)')
a('.location.distances[2][1]', '800 m', '800 m', '800 m', '800 м', '800 م', '800 m', '800 m', '800 m', '800 m')

# ---- investment ------------------------------------------------------------------------------------

a('.investment.copy',
  'La lista de precios da un precio para cada una de las seis viviendas, antes de IVA, y las condiciones de pago fijan la reserva, el contrato privado, tres plazos y la escritura.',
  'La liste de prix donne un prix pour chacun des six logements, hors TVA, et les conditions de paiement fixent la réservation, le contrat privé, trois versements et l’acte authentique.',
  'Die Preisliste nennt für jede der sechs Wohnungen einen Preis vor MwSt., und die Zahlungsbedingungen regeln die Reservierung, den privaten Vertrag, drei Raten und die Beurkundung.',
  'В прайс-листе у каждой из шести квартир указана цена без НДС, а условия оплаты определяют бронирование, частный договор, три платежа и оформление права собственности.',
  'تذكر قائمة الأسعار سعرًا لكل مسكن من المساكن الستة قبل ضريبة القيمة المضافة، وتحدد شروط الدفع الحجز والعقد الخاص وثلاث دفعات وسند الملكية.',
  'De prijslijst geeft voor elk van de zes woningen een prijs vóór btw, en de betalingsvoorwaarden leggen de reservering, het privécontract, drie termijnen en de akte vast.',
  'Cennik podaje cenę każdego z sześciu lokali przed VAT, a warunki płatności określają rezerwację, umowę prywatną, trzy raty i akt notarialny.',
  'Prislisten oppgir en pris for hver av de seks boligene, før mva, og betalingsvilkårene fastsetter reservasjonen, den private kontrakten, tre avdrag og skjøtet.',
  'Prislistan anger ett pris för var och en av de sex bostäderna, före IVA (spansk moms), och betalningsvillkoren fastställer bokningen, det privata kontraktet, tre delbetalningar och köpebrevet.')
a('.investment.cards[0][1]',
  'La lista de precios dice que el IVA no está incluido, y la reserva figura como {E6000} más IVA. Con un IVA del 10 por ciento y un impuesto de actos jurídicos documentados del {N1.20} por ciento, la vivienda de {E320000} cuesta unos {E356000} y el ático de {E480000} unos {E534000}, antes de notaría y registro de la propiedad.',
  'La liste de prix indique que la TVA n’est pas comprise, et la réservation est donnée à {E6000} hors TVA. Avec une TVA de 10 pour cent et un droit de timbre de {N1.20} pour cent, le logement à {E320000} coûte environ {E356000} et le penthouse à {E480000} environ {E534000}, avant frais de notaire et de registre foncier.',
  'Die Preisliste besagt, dass die MwSt. nicht enthalten ist, und die Reservierung ist mit {E6000} zuzüglich MwSt. angegeben. Bei 10 Prozent MwSt. und {N1.20} Prozent Stempelsteuer kostet die Wohnung für {E320000} rund {E356000} und das Penthouse für {E480000} rund {E534000}, vor Notar- und Grundbuchkosten.',
  'В прайс-листе сказано, что НДС не включён, а бронирование указано как {E6000} плюс НДС. При НДС 10 процентов и гербовом сборе {N1.20} процента квартира за {E320000} обойдётся примерно в {E356000}, а пентхаус за {E480000} — примерно в {E534000}, до расходов на нотариуса и регистрацию.',
  'تذكر قائمة الأسعار أن ضريبة القيمة المضافة غير مشمولة، وأن الحجز مذكور بمبلغ {E6000} زائد ضريبة القيمة المضافة. وبضريبة قيمة مضافة قدرها 10 بالمئة ورسم دمغة قدره {N1.20} بالمئة، يكلّف المسكن البالغ سعره {E320000} نحو {E356000}، والبنتهاوس البالغ سعره {E480000} نحو {E534000}، قبل أتعاب التوثيق والتسجيل العقاري.',
  'De prijslijst zegt dat btw niet is inbegrepen, en de reservering staat vermeld als {E6000} plus btw. Bij 10 procent btw en {N1.20} procent overdrachtsbelasting kost de woning van {E320000} ongeveer {E356000} en het penthouse van {E480000} ongeveer {E534000}, vóór notaris- en kadasterkosten.',
  'Cennik podaje, że VAT nie jest wliczony, a rezerwacja jest wskazana jako {E6000} plus VAT. Przy VAT w wysokości 10 procent i podatku od czynności cywilnoprawnych w wysokości {N1.20} procent lokal za {E320000} kosztuje około {E356000}, a penthouse za {E480000} około {E534000}, przed opłatami notarialnymi i wieczystoksięgowymi.',
  'Prislisten sier at mva ikke er inkludert, og reservasjonen er oppgitt som {E6000} pluss mva. Med 10 prosent mva og {N1.20} prosent dokumentavgift koster boligen til {E320000} omtrent {E356000} og toppleiligheten til {E480000} omtrent {E534000}, før notar- og tinglysingsgebyrer.',
  'Prislistan anger att IVA (spansk moms) inte ingår, och reservationen anges som {E6000} plus IVA. Med 10 procent IVA och {N1.20} procent stämpelskatt kostar bostaden för {E320000} cirka {E356000} och takvåningen för {E480000} cirka {E534000}, före notarie- och registreringsavgifter.')
a('.investment.cards[1][1]',
  '{E6000} más {T} en la reserva; el 15 por ciento más {T} en el contrato privado, menos la reserva; el 15 por ciento más {T} en tres pagos el {D5.3.2027}, el {D5.9.2027} y el {D5.3.2028}; y el 70 por ciento más {T} en la escritura.',
  '{E6000} hors {T} à la réservation ; 15 pour cent hors {T} au contrat privé, moins la réservation ; 15 pour cent hors {T} en trois versements, le {D5.3.2027}, le {D5.9.2027} et le {D5.3.2028} ; et 70 pour cent hors {T} à l’acte authentique.',
  '{E6000} zuzüglich {T} bei der Reservierung; 15 Prozent zuzüglich {T} beim privaten Vertrag, abzüglich der Reservierung; 15 Prozent zuzüglich {T} in drei Raten am {D5.3.2027}, am {D5.9.2027} und am {D5.3.2028}; und 70 Prozent zuzüglich {T} bei der Beurkundung.',
  '{E6000} плюс {T} при бронировании; 15 процентов плюс {T} при частном договоре за вычетом бронирования; 15 процентов плюс {T} тремя платежами: {D5.3.2027}, {D5.9.2027} и {D5.3.2028}; и 70 процентов плюс {T} при оформлении права собственности.',
  '{E6000} زائد {T} عند الحجز؛ و15 بالمئة زائد {T} عند العقد الخاص، مخصومًا منها الحجز؛ و15 بالمئة زائد {T} على ثلاث دفعات في {D5.3.2027} و{D5.9.2027} و{D5.3.2028}؛ و70 بالمئة زائد {T} عند سند الملكية.',
  '{E6000} plus {T} bij reservering; 15 procent plus {T} bij het privécontract, min de reservering; 15 procent plus {T} in drie termijnen op {D5.3.2027}, {D5.9.2027} en {D5.3.2028}; en 70 procent plus {T} bij de akte.',
  '{E6000} plus {T} przy rezerwacji; 15 procent plus {T} przy umowie prywatnej, pomniejszone o rezerwację; 15 procent plus {T} w trzech ratach w dniach {D5.3.2027}, {D5.9.2027} i {D5.3.2028}; oraz 70 procent plus {T} przy akcie notarialnym.',
  '{E6000} pluss {T} ved reservasjon; 15 prosent pluss {T} ved den private kontrakten, minus reservasjonen; 15 prosent pluss {T} i tre betalinger {D5.3.2027}, {D5.9.2027} og {D5.3.2028}; og 70 prosent pluss {T} ved skjøtet.',
  '{E6000} plus {T} vid bokning; 15 procent plus {T} vid det privata kontraktet, minus bokningen; 15 procent plus {T} i tre betalningar den {D5.3.2027}, {D5.9.2027} och {D5.3.2028}; och 70 procent plus {T} vid köpebrevet.')
a('.investment.cards[2][1]',
  'La lista de precios da una plaza de garaje y un trastero, con su número, para cada vivienda, y el folleto habla de aparcamiento y trastero. Confirmamos que ambos están incluidos en el precio.',
  'La liste de prix donne pour chaque logement une place de garage et une cave, avec leur numéro, et la brochure parle de stationnement et d’une cave. Nous confirmons que les deux sont compris dans le prix.',
  'Die Preisliste nennt für jede Wohnung einen Garagenstellplatz und einen Abstellraum mit Nummer, und die Broschüre spricht von Parkplatz und Abstellraum. Wir bestätigen, dass beides im Preis enthalten ist.',
  'В прайс-листе для каждой квартиры указаны место в гараже и кладовая с номерами, а в брошюре говорится о парковке и кладовой. Мы подтверждаем, что и то и другое входит в цену.',
  'تذكر قائمة الأسعار لكل مسكن موقفًا في المرآب ومخزنًا بأرقامهما، ويتحدث الكتيّب عن موقف سيارات ومخزن. نؤكد أن كليهما مشمول في السعر.',
  'De prijslijst geeft voor elke woning een garageplaats en een berging met nummer, en de brochure spreekt van parkeren en een berging. We bevestigen dat beide in de prijs zijn inbegrepen.',
  'Cennik podaje dla każdego lokalu numer miejsca w garażu i komórki lokatorskiej, a broszura wspomina o parkingu i komórce lokatorskiej. Potwierdzamy, że oba są wliczone w cenę.',
  'Prislisten oppgir en garasjeplass og en bod med nummer for hver bolig, og brosjyren omtaler parkering og en bod. Vi bekrefter at begge er inkludert i prisen.',
  'Prislistan anger en garageplats och ett förråd med nummer för varje bostad, och broschyren nämner parkering och ett förråd. Vi bekräftar att båda ingår i priset.')
a('.investment.cards[3][0]',
  'Plazos con fecha', 'Versements datés', 'Raten mit festen Terminen', 'Платежи с фиксированными датами', 'دفعات بتواريخ محددة',
  'Termijnen met vaste data', 'Raty z ustalonymi terminami', 'Avdrag med faste datoer', 'Delbetalningar med fasta datum')
a('.investment.cards[3][1]',
  'Los tres plazos del 15 por ciento tienen fechas fijas, y el contrato privado que los precede se firma al obtenerse la licencia. Preguntamos qué ocurre con las fechas si la licencia se retrasa y cómo se garantiza el dinero entregado antes de la finalización.',
  'Les trois versements de 15 pour cent ont des dates fixes, et le contrat privé qui les précède est dû à l’obtention du permis. Nous demandons ce qu’il advient des dates si le permis est en retard et comment l’argent versé avant l’achèvement est garanti.',
  'Die drei Raten von je 15 Prozent haben feste Termine, und der private Vertrag davor wird mit der Erteilung der Baugenehmigung fällig. Wir fragen nach, was mit den Terminen geschieht, wenn die Genehmigung sich verzögert, und wie das vor der Fertigstellung gezahlte Geld abgesichert ist.',
  'Три платежа по 15 процентов привязаны к фиксированным датам, а предшествующий им частный договор наступает при получении лицензии на строительство. Мы выясняем, что будет с датами, если лицензия задержится, и как гарантируются деньги, выплаченные до завершения строительства.',
  'للدفعات الثلاث البالغة 15 بالمئة تواريخ ثابتة، ويستحق العقد الخاص الذي يسبقها عند الحصول على الرخصة. نسأل عمّا يحدث للتواريخ إذا تأخرت الرخصة، وكيف تُضمن الأموال المدفوعة قبل الإنجاز.',
  'De drie termijnen van 15 procent hebben vaste data, en het privécontract daarvoor is verschuldigd bij het verkrijgen van de vergunning. We vragen wat er met de data gebeurt als de vergunning te laat komt, en hoe het geld dat vóór de oplevering is betaald wordt gewaarborgd.',
  'Trzy raty po 15 procent mają ustalone terminy, a poprzedzająca je umowa prywatna jest wymagalna po uzyskaniu pozwolenia. Pytamy, co dzieje się z terminami, jeśli pozwolenie się opóźni, i jak zabezpieczone są pieniądze wpłacone przed ukończeniem.',
  'De tre avdragene på 15 prosent har faste datoer, og den private kontrakten før dem forfaller når tillatelsen innvilges. Vi spør hva som skjer med datoene hvis tillatelsen blir forsinket, og hvordan penger betalt før ferdigstillelsen er sikret.',
  'De tre delbetalningarna på 15 procent har fasta datum, och det privata kontraktet före dem förfaller när bygglovet beviljas. Vi frågar vad som händer med datumen om bygglovet försenas, och hur pengar som betalats före färdigställandet är säkrade.')

# ---- trustDossier ----------------------------------------------------------------------------------

a('.trustDossier.cards[0][1]',
  'La lista de precios nombra 19 de las 142 viviendas: seis con precio y 13 marcadas como reservadas. No dice nada de las otras 123 y no lleva fecha impresa; la fecha de esta página es la registrada en el archivo. Pedimos la lista completa y el estado de cada vivienda.',
  'La liste de prix nomme 19 des 142 logements : six avec un prix et 13 marqués comme réservés. Elle ne dit rien des 123 autres et ne porte aucune date imprimée ; la date de cette page est celle enregistrée dans le fichier. Nous demandons la liste complète et le statut de chaque logement.',
  'Die Preisliste nennt 19 der 142 Wohnungen: sechs mit Preis und 13 als reserviert gekennzeichnet. Zu den übrigen 123 sagt sie nichts, und sie trägt kein gedrucktes Datum; das Datum auf dieser Seite ist das in der Datei vermerkte. Wir fordern die vollständige Liste und den Status jeder Wohnung an.',
  'В прайс-листе названы 19 из 142 квартир: шесть с ценой и 13 с пометкой «зарезервировано». Об остальных 123 в нём ничего не сказано, и даты в нём не напечатано; дата на этой странице — та, что записана в файле. Мы запрашиваем полный список и статус каждой квартиры.',
  'تسمّي قائمة الأسعار 19 مسكنًا من أصل 142: ستة بسعر و13 معلَّمة محجوزة. ولا تقول شيئًا عن الـ123 الأخرى، ولا تحمل تاريخًا مطبوعًا؛ والتاريخ في هذه الصفحة هو المسجَّل في الملف. نطلب القائمة الكاملة وحالة كل مسكن.',
  'De prijslijst noemt 19 van de 142 woningen: zes met een prijs en 13 als gereserveerd aangemerkt. Over de overige 123 zegt ze niets, en ze draagt geen gedrukte datum; de datum op deze pagina is die uit het bestand. We vragen de volledige lijst en de status van elke woning op.',
  'Cennik wymienia 19 ze 142 lokali: sześć z ceną i 13 oznaczonych jako zarezerwowane. O pozostałych 123 nic nie mówi i nie ma wydrukowanej daty; data na tej stronie to ta zapisana w pliku. Prosimy o pełną listę i status każdego lokalu.',
  'Prislisten nevner 19 av de 142 boligene: seks med pris og 13 merket som reservert. Den sier ingenting om de øvrige 123, og den har ingen trykt dato; datoen på denne siden er den som er registrert i filen. Vi ber om den fullstendige listen og statusen for hver bolig.',
  'Prislistan nämner 19 av de 142 bostäderna: sex med pris och 13 markerade som reserverade. Den säger ingenting om de övriga 123, och den har inget tryckt datum; datumet på den här sidan är det som är registrerat i filen. Vi ber om den fullständiga listan och status för varje bostad.')
a('.trustDossier.cards[1][0]',
  'La licencia y la fecha de entrega', 'Le permis et la date de livraison', 'Die Baugenehmigung und der Fertigstellungstermin', 'Лицензия и срок сдачи',
  'الرخصة وموعد التسليم', 'De vergunning en de opleveringsdatum', 'Pozwolenie i termin oddania', 'Tillatelsen og overleveringsdatoen', 'Bygglovet och tillträdesdatumet')
a('.trustDossier.cards[1][1]',
  'Las condiciones de pago sitúan el contrato privado en el momento de concederse la licencia y la escritura en el primer trimestre de 2029. Ningún documento indica el estado de la licencia ni el inicio de las obras. Pedimos la licencia, el inicio de las obras y la fecha de entrega contractual.',
  'Les conditions de paiement placent le contrat privé à l’octroi du permis et l’acte authentique au premier trimestre 2029. Aucun document n’indique le statut du permis ni le début des travaux. Nous demandons le permis, le début des travaux et la date de livraison contractuelle.',
  'Die Zahlungsbedingungen legen den privaten Vertrag auf die Erteilung der Baugenehmigung und die Beurkundung auf das erste Quartal 2029. Kein Dokument nennt den Stand der Genehmigung oder einen Baubeginn. Wir fordern die Genehmigung, den Baubeginn und den vertraglichen Übergabetermin an.',
  'По условиям оплаты частный договор заключается при выдаче лицензии, а оформление права собственности у нотариуса — в первом квартале 2029 года. Ни один документ не называет статус лицензии или начало работ. Мы запрашиваем лицензию, дату начала работ и договорный срок сдачи.',
  'تضع شروط الدفع العقد الخاص عند منح الرخصة وسند الملكية في الربع الأول من 2029. ولا تذكر أي وثيقة وضع الرخصة أو بدء الأشغال. نطلب الرخصة وموعد بدء الأشغال وموعد التسليم التعاقدي.',
  'De betalingsvoorwaarden plaatsen het privécontract bij de verlening van de vergunning en de akte in het eerste kwartaal van 2029. Geen enkel document vermeldt de stand van de vergunning of een start van de werken. We vragen de vergunning, de start van de werken en de contractuele opleveringsdatum op.',
  'Warunki płatności wiążą umowę prywatną z udzieleniem pozwolenia, a akt notarialny z pierwszym kwartałem 2029 roku. Żaden dokument nie podaje statusu pozwolenia ani rozpoczęcia prac. Prosimy o pozwolenie, termin rozpoczęcia prac i umowny termin oddania.',
  'Betalingsvilkårene legger den private kontrakten til innvilgelsen av tillatelsen og skjøtet til første kvartal 2029. Ingen dokumenter oppgir status for tillatelsen eller byggestart. Vi ber om tillatelsen, byggestarten og den avtalte overleveringsdatoen.',
  'Betalningsvillkoren lägger det privata kontraktet vid beviljandet av bygglovet och köpebrevet till första kvartalet 2029. Inget dokument anger bygglovets status eller byggstart. Vi ber om bygglovet, byggstarten och det avtalade tillträdesdatumet.')
a('.trustDossier.cards[2][1]',
  'El folleto dice que todas las viviendas están orientadas al sur o al suroeste. La lista de precios da oeste para 13 de las 19 viviendas, incluidas las seis disponibles, y sureste para las otras seis. Confirmamos la orientación de la vivienda elegida con el plano y sobre el terreno.',
  'La brochure dit que tous les logements sont orientés au sud ou au sud-ouest. La liste de prix donne l’ouest pour 13 des 19 logements, dont les six disponibles, et le sud-est pour les six autres. Nous confirmons l’orientation du logement choisi d’après le plan et sur place.',
  'Die Broschüre sagt, dass alle Wohnungen nach Süden oder Südwesten ausgerichtet sind. Die Preisliste nennt Westen für 13 der 19 Wohnungen, darunter alle sechs verfügbaren, und Südosten für die anderen sechs. Wir bestätigen die Ausrichtung der gewählten Wohnung anhand des Plans und vor Ort.',
  'В брошюре сказано, что все квартиры ориентированы на юг или юго-запад. В прайс-листе указан запад для 13 из 19 квартир, включая все шесть доступных, и юго-восток для остальных шести. Ориентацию выбранной квартиры мы подтверждаем по плану и на месте.',
  'يقول الكتيّب إن جميع المساكن تتجه نحو الجنوب أو الجنوب الغربي. وتذكر قائمة الأسعار الغرب لـ13 مسكنًا من أصل 19، منها المساكن الستة المتاحة جميعها، والجنوب الشرقي للمساكن الستة الأخرى. نؤكد اتجاه المسكن المختار من المخطط وفي الموقع.',
  'De brochure zegt dat alle woningen op het zuiden of zuidwesten liggen. De prijslijst geeft west voor 13 van de 19 woningen, waaronder alle zes beschikbare, en zuidoost voor de andere zes. We bevestigen de oriëntatie van de gekozen woning aan de hand van de plattegrond en ter plaatse.',
  'Broszura podaje, że wszystkie lokale są skierowane na południe lub południowy zachód. Cennik podaje zachód dla 13 z 19 lokali, w tym dla wszystkich sześciu dostępnych, i południowy wschód dla pozostałych sześciu. Orientację wybranego lokalu potwierdzamy na podstawie rzutu i na miejscu.',
  'Brosjyren sier at alle boligene vender mot sør eller sørvest. Prislisten oppgir vest for 13 av de 19 boligene, blant dem alle de seks tilgjengelige, og sørøst for de andre seks. Vi bekrefter orienteringen til den valgte boligen ut fra plantegningen og på stedet.',
  'Broschyren säger att alla bostäder har söderläge eller sydvästläge. Prislistan anger väster för 13 av de 19 bostäderna, däribland alla sex tillgängliga, och sydost för de andra sex. Vi bekräftar den valda bostadens väderstreck utifrån planritningen och på plats.')
a('.trustDossier.cards[3][1]',
  'La lista de precios da la superficie útil interior de cada vivienda y una superficie construida interior mayor, {N83.78} y {N99.26} {U} para la misma vivienda. Los planos añaden una superficie bruta que incluye una parte de las zonas comunes y las superficies según el decreto andaluz 218/2005. La tabla muestra la superficie útil interior, en la que coinciden la lista y los planos, y confirmamos qué cifra usa el contrato.',
  'La liste de prix donne la surface utile intérieure de chaque logement et une surface construite intérieure plus grande, {N83.78} et {N99.26} {U} pour le même logement. Les plans ajoutent une surface brute incluant une quote-part des parties communes et les surfaces selon le décret andalou 218/2005. Le tableau montre la surface utile intérieure, sur laquelle la liste et les plans concordent, et nous confirmons quel chiffre le contrat retient.',
  'Die Preisliste nennt für jede Wohnung die Nutzfläche innen und eine größere bebaute Innenfläche, {N83.78} und {N99.26} {U} für dieselbe Wohnung. Die Pläne fügen eine Bruttofläche mit einem Anteil an den Gemeinschaftsflächen und die Flächen nach dem andalusischen Dekret 218/2005 hinzu. Die Tabelle zeigt die Nutzfläche innen, in der Liste und Pläne übereinstimmen, und wir bestätigen, welche Zahl der Vertrag verwendet.',
  'В прайс-листе для каждой квартиры указаны внутренняя полезная площадь и бо́льшая внутренняя застроенная площадь — {N83.78} и {N99.26} {U} для одной и той же квартиры. На планах добавлена общая площадь с долей общих зон и площади по андалусскому декрету 218/2005. В таблице приведена полезная внутренняя площадь, по которой прайс-лист и планы совпадают; какую цифру использует договор, мы подтверждаем.',
  'تذكر قائمة الأسعار لكل مسكن المساحة الداخلية الصالحة للاستخدام ومساحة داخلية مبنية أكبر، {N83.78} و{N99.26} {U} للمسكن نفسه. وتضيف المخططات مساحة إجمالية تشمل حصة من المناطق المشتركة والمساحات وفق المرسوم الأندلسي 218/2005. يعرض الجدول المساحة الداخلية الصالحة للاستخدام التي تتفق عليها القائمة والمخططات، ونؤكد أي رقم يستخدمه العقد.',
  'De prijslijst geeft per woning de bruikbare binnenoppervlakte en een grotere bebouwde binnenoppervlakte, {N83.78} en {N99.26} {U} voor dezelfde woning. De plattegronden voegen een bruto-oppervlakte toe met een aandeel in de gemeenschappelijke ruimten en de oppervlakten volgens het Andalusische decreet 218/2005. De tabel toont de bruikbare binnenoppervlakte, waarover de lijst en de plattegronden het eens zijn, en we bevestigen welk cijfer het contract hanteert.',
  'Cennik podaje dla każdego lokalu powierzchnię użytkową wewnętrzną oraz większą wewnętrzną powierzchnię zabudowy, {N83.78} i {N99.26} {U} dla tego samego lokalu. Rzuty dodają powierzchnię brutto z udziałem w częściach wspólnych oraz powierzchnie według andaluzyjskiego dekretu 218/2005. Tabela pokazuje powierzchnię użytkową wewnętrzną, co do której cennik i rzuty są zgodne, a którą wartość stosuje umowa, potwierdzamy.',
  'Prislisten oppgir hver boligs innvendige bruksareal og et større innvendig bebygd areal, {N83.78} og {N99.26} {U} for samme bolig. Plantegningene legger til et bruttoareal med en andel av fellesarealene og arealene etter det andalusiske dekretet 218/2005. Tabellen viser det innvendige bruksarealet, som listen og plantegningene er enige om, og vi bekrefter hvilket tall kontrakten bruker.',
  'Prislistan anger varje bostads invändiga boyta och en större invändig byggd yta, {N83.78} och {N99.26} {U} för samma bostad. Planritningarna lägger till en bruttoyta med en andel av de gemensamma ytorna och ytorna enligt det andalusiska dekretet 218/2005. Tabellen visar den invändiga boytan, som listan och planritningarna är överens om, och vi bekräftar vilken siffra avtalet använder.')
a('.trustDossier.cards[4][1]',
  'El folleto describe una piscina central con zona chill-out, y la memoria de calidades menciona piscinas de chapoteo con cloración salina. Preguntamos el número, el tamaño y el tipo de las piscinas.',
  'La brochure décrit une piscine centrale avec un espace de détente, et le descriptif des matériaux mentionne des pataugeoires au chlore salin. Nous demandons le nombre, la taille et le type des piscines.',
  'Die Broschüre beschreibt einen zentralen Pool mit Chill-out-Bereich, und die Ausstattungsbeschreibung nennt Planschbecken mit Salzwasserchlorierung. Wir fragen nach Anzahl, Größe und Art der Pools.',
  'В брошюре описан центральный бассейн с зоной отдыха, а в спецификации материалов указаны мелкие бассейны с солевой хлорацией. Мы запрашиваем количество, размеры и тип бассейнов.',
  'يصف الكتيّب مسبحًا مركزيًا بمنطقة استرخاء، وتذكر مواصفات المواد مسابح ضحلة بالكلور الملحي. نسأل عن عدد المسابح وحجمها ونوعها.',
  'De brochure beschrijft een centraal zwembad met chill-outzone, en de specificatie noemt pierenbadjes met zoutchlorering. We vragen naar het aantal, de afmetingen en het type van de zwembaden.',
  'Broszura opisuje centralny basen ze strefą relaksu, a specyfikacja wymienia brodziki z chlorowaniem solą. Pytamy o liczbę, rozmiar i typ basenów.',
  'Brosjyren beskriver et sentralt basseng med en chill-out-sone, og spesifikasjonen nevner plaskebasseng med saltklorering. Vi spør om antall, størrelse og type basseng.',
  'Broschyren beskriver en central pool med en chill-out-yta, och specifikationen nämner plaskpooler med saltklorering. Vi frågar efter antal, storlek och typ av pooler.')
a('.trustDossier.cards[5][1]',
  'Las imágenes están generadas por ordenador y, según el folleto, se basan en un proyecto inicial que puede cambiar durante las obras. Los planos dicen lo mismo. El mobiliario, la decoración y la vegetación que se muestran no forman parte de la oferta.',
  'Les images sont générées par ordinateur et, selon la brochure, reposent sur un projet initial qui peut évoluer pendant les travaux. Les plans disent la même chose. Le mobilier, la décoration et la végétation représentés ne font pas partie de l’offre.',
  'Die Bilder sind computergeneriert und beruhen laut Broschüre auf einem ersten Projekt, das sich während der Bauarbeiten ändern kann. Die Pläne sagen dasselbe. Die gezeigten Möbel, die Dekoration und die Bepflanzung sind nicht Teil des Angebots.',
  'Изображения созданы на компьютере и, как сказано в брошюре, основаны на первоначальном проекте, который может измениться в ходе строительства. На планах сказано то же самое. Показанная мебель, декор и озеленение не входят в предложение.',
  'الصور مولَّدة بالكمبيوتر وهي، بحسب الكتيّب، مبنية على مشروع أولي قد يتغير أثناء الأشغال. وتقول المخططات الشيء نفسه. والأثاث والديكور والنباتات الظاهرة ليست جزءًا من العرض.',
  'De beelden zijn computergegenereerd en zijn, zo zegt de brochure, gebaseerd op een eerste project dat tijdens de werken kan veranderen. De plattegronden zeggen hetzelfde. Het getoonde meubilair, de inrichting en de beplanting maken geen deel uit van het aanbod.',
  'Wizualizacje są wygenerowane komputerowo i, jak podaje broszura, opierają się na pierwotnym projekcie, który może się zmienić w trakcie prac. Rzuty mówią to samo. Pokazane meble, dekoracje i nasadzenia nie są częścią oferty.',
  'Bildene er datagenererte og bygger, ifølge brosjyren, på et første prosjekt som kan endres under arbeidene. Plantegningene sier det samme. Møblene, dekorasjonen og beplantningen som vises er ikke en del av tilbudet.',
  'Bilderna är datorgenererade och bygger, enligt broschyren, på ett första projekt som kan ändras under byggarbetena. Planritningarna säger detsamma. Möblerna, dekorationen och planteringen som visas ingår inte i erbjudandet.')

# ---- availability ----------------------------------------------------------------------------------

a('.availability.headlineHtml',
  '6 viviendas <em>disponibles actualmente</em>', '6 logements <em>actuellement disponibles</em>', '6 Wohnungen <em>derzeit verfügbar</em>',
  '6 квартир <em>доступны сейчас</em>', '6 مساكن <em>متاحة حاليًا</em>', '6 woningen <em>momenteel beschikbaar</em>',
  '6 lokali <em>obecnie dostępnych</em>', '6 boliger <em>tilgjengelige nå</em>', '6 bostäder <em>tillgängliga just nu</em>')
a('.availability.copy',
  'Los precios son los de la lista de precios del promotor, cuyo archivo registra el {D23.10.2026}, y confirmamos precios y disponibilidad antes de cualquier reserva. La lista nombra 19 de las 142 viviendas: seis tienen precio y están disponibles y 13 figuran como reservadas. Los precios son antes de IVA.',
  'Les prix sont ceux de la liste de prix du promoteur, dont le fichier porte la date du {D23.10.2026}, et nous confirmons prix et disponibilité avant toute réservation. La liste nomme 19 des 142 logements : six ont un prix et sont disponibles et 13 sont marqués comme réservés. Les prix s’entendent hors TVA.',
  'Die Preise stammen aus der Preisliste des Bauträgers, deren Datei den {D23.10.2026} vermerkt, und wir bestätigen Preise und Verfügbarkeit vor jeder Reservierung. Die Liste nennt 19 der 142 Wohnungen: sechs haben einen Preis und sind verfügbar, 13 sind als reserviert gekennzeichnet. Die Preise verstehen sich vor MwSt.',
  'Цены взяты из прайс-листа застройщика, в файле которого записано {D23.10.2026}; цены и наличие мы подтверждаем до любого бронирования. В списке названы 19 из 142 квартир: шесть с ценой и доступны, 13 отмечены как зарезервированные. Цены указаны без НДС.',
  'الأسعار هي أسعار قائمة المطوّر، التي يسجّل ملفها تاريخ {D23.10.2026}، ونؤكد الأسعار والتوافر قبل أي حجز. تسمّي القائمة 19 مسكنًا من أصل 142: ستة لها سعر ومتاحة و13 معلَّمة محجوزة. الأسعار قبل ضريبة القيمة المضافة.',
  'De prijzen zijn die van de prijslijst van de ontwikkelaar, waarvan het bestand {D23.10.2026} vermeldt, en we bevestigen prijzen en beschikbaarheid vóór een reservering. De lijst noemt 19 van de 142 woningen: zes hebben een prijs en zijn beschikbaar en 13 zijn als gereserveerd aangemerkt. De prijzen zijn vóór btw.',
  'Ceny pochodzą z cennika dewelopera, którego plik odnotowuje datę {D23.10.2026}, a ceny i dostępność potwierdzamy przed jakąkolwiek rezerwacją. Lista wymienia 19 ze 142 lokali: sześć ma cenę i jest dostępnych, a 13 jest oznaczonych jako zarezerwowane. Ceny są przed VAT.',
  'Prisene er fra utbyggerens prisliste, hvis fil oppgir {D23.10.2026}, og vi bekrefter priser og tilgjengelighet før enhver reservasjon. Listen nevner 19 av de 142 boligene: seks har pris og er tilgjengelige, og 13 er merket som reservert. Prisene er før mva.',
  'Priserna är de i exploatörens prislista, vars fil anger {D23.10.2026}, och vi bekräftar priser och tillgänglighet före varje reservation. Listan nämner 19 av de 142 bostäderna: sex har pris och är tillgängliga, och 13 är markerade som reserverade. Priserna är före IVA.')
a('.availability.sourceNote',
  'Los precios y las superficies están transcritos de la lista de precios del promotor, que no lleva fecha impresa; su archivo registra el {D23.10.2026}. La lista nombra 19 viviendas y muestra 13 de ellas como reservadas, que no se incluyen aquí. Los precios de las otras seis son antes de IVA, y se añaden el IVA del 10 por ciento y el impuesto de actos jurídicos documentados del {N1.20} por ciento, de modo que la vivienda de {E320000} cuesta unos {E356000} y el ático de {E480000} unos {E534000}, antes de notaría y registro de la propiedad. Interior es la superficie útil interior de la lista, y terraza es el conjunto de las terrazas cubiertas y descubiertas; la vivienda de planta baja B6-P11-0A tiene un jardín delantero de {N49.54} {U} en lugar de una terraza descubierta. Las superficies construidas interiores de la lista, que son mayores, no figuran en la tabla. Cada vivienda aparece con una plaza de garaje y un trastero, con su número; la lista no dice que estén incluidos en el precio.',
  'Les prix et les surfaces sont repris de la liste de prix du promoteur, qui ne porte aucune date imprimée ; son fichier indique le {D23.10.2026}. La liste nomme 19 logements et en montre 13 comme réservés, qui ne figurent pas ici. Les prix des six autres s’entendent hors TVA, et s’y ajoutent la TVA à 10 pour cent et le droit de timbre à {N1.20} pour cent, si bien que le logement à {E320000} coûte environ {E356000} et le penthouse à {E480000} environ {E534000}, avant frais de notaire et de registre foncier. Intérieur est la surface utile intérieure de la liste, et terrasse l’ensemble des terrasses couvertes et découvertes ; le logement du rez-de-chaussée B6-P11-0A a un jardin sur le devant de {N49.54} {U} à la place d’une terrasse découverte. Les surfaces construites intérieures de la liste, plus grandes, ne figurent pas dans le tableau. Chaque logement est indiqué avec une place de garage et une cave, avec leur numéro ; la liste ne dit pas qu’elles sont comprises dans le prix.',
  'Preise und Flächen sind der Preisliste des Bauträgers entnommen, die kein gedrucktes Datum trägt; ihre Datei vermerkt den {D23.10.2026}. Die Liste nennt 19 Wohnungen und zeigt 13 davon als reserviert, die hier nicht aufgeführt sind. Die Preise der übrigen sechs verstehen sich vor MwSt.; hinzu kommen 10 Prozent MwSt. und {N1.20} Prozent Stempelsteuer, sodass die Wohnung für {E320000} rund {E356000} und das Penthouse für {E480000} rund {E534000} kostet, vor Notar- und Grundbuchkosten. Innen ist die Nutzfläche innen der Liste, und Terrasse sind die überdachten und unüberdachten Terrassen zusammen; die Erdgeschosswohnung B6-P11-0A hat statt einer unüberdachten Terrasse einen Vorgarten von {N49.54} {U}. Die größeren bebauten Innenflächen der Liste fehlen in der Tabelle. Jede Wohnung ist mit einem Garagenstellplatz und einem Abstellraum mit Nummer aufgeführt; die Liste sagt nicht, dass sie im Preis enthalten sind.',
  'Цены и площади перенесены из прайс-листа застройщика, в котором не напечатана дата; в его файле записано {D23.10.2026}. В списке названы 19 квартир, 13 из них показаны как зарезервированные и здесь не приведены. Цены остальных шести указаны без НДС, к ним добавляются НДС 10 процентов и гербовый сбор {N1.20} процента, так что квартира за {E320000} обойдётся примерно в {E356000}, а пентхаус за {E480000} — примерно в {E534000}, до расходов на нотариуса и регистрацию. «Внутри» — это внутренняя полезная площадь из списка, а «терраса» — крытые и открытые террасы вместе; у квартиры на первом этаже B6-P11-0A вместо открытой террасы есть палисадник {N49.54} {U}. Бо́льшие внутренние застроенные площади из списка в таблицу не включены. Каждая квартира указана с местом в гараже и кладовой с номерами; в списке не сказано, что они входят в цену.',
  'الأسعار والمساحات منقولة من قائمة أسعار المطوّر، التي لا تحمل تاريخًا مطبوعًا؛ ويسجّل ملفها تاريخ {D23.10.2026}. تسمّي القائمة 19 مسكنًا وتُظهر 13 منها محجوزة، وهي غير مدرجة هنا. أسعار المساكن الستة الأخرى قبل ضريبة القيمة المضافة، وتُضاف ضريبة القيمة المضافة بنسبة 10 بالمئة ورسم الدمغة بنسبة {N1.20} بالمئة، فيكلّف المسكن البالغ سعره {E320000} نحو {E356000} والبنتهاوس البالغ سعره {E480000} نحو {E534000}، قبل أتعاب التوثيق والتسجيل العقاري. الداخلي هو المساحة الداخلية الصالحة للاستخدام في القائمة، والتراس هو التراسات المغطاة والمكشوفة معًا؛ ولمسكن الطابق الأرضي B6-P11-0A حديقة أمامية مساحتها {N49.54} {U} بدل تراس مكشوف. أما المساحات الداخلية المبنية في القائمة، وهي أكبر، فلم تُدرج في الجدول. يُدرج كل مسكن مع موقف في المرآب ومخزن بأرقامهما؛ ولا تذكر القائمة أنهما مشمولان في السعر.',
  'Prijzen en oppervlakten zijn overgenomen uit de prijslijst van de ontwikkelaar, die geen gedrukte datum draagt; het bestand vermeldt {D23.10.2026}. De lijst noemt 19 woningen en toont er 13 als gereserveerd, die hier niet zijn opgenomen. De prijzen van de overige zes zijn vóór btw, en daar komen 10 procent btw en {N1.20} procent overdrachtsbelasting bij, zodat de woning van {E320000} ongeveer {E356000} kost en het penthouse van {E480000} ongeveer {E534000}, vóór notaris- en kadasterkosten. Binnen is de bruikbare binnenoppervlakte uit de lijst, en terras zijn de overdekte en open terrassen samen; de woning op de begane grond B6-P11-0A heeft in plaats van een open terras een voortuin van {N49.54} {U}. De grotere bebouwde binnenoppervlakten uit de lijst zijn niet in de tabel opgenomen. Elke woning staat vermeld met een garageplaats en een berging met nummer; de lijst zegt niet dat ze in de prijs zijn inbegrepen.',
  'Ceny i powierzchnie przepisano z cennika dewelopera, który nie ma wydrukowanej daty; jego plik odnotowuje {D23.10.2026}. Lista wymienia 19 lokali i pokazuje 13 z nich jako zarezerwowane, których tu nie ujęto. Ceny pozostałych sześciu są przed VAT, a doliczany jest VAT w wysokości 10 procent i podatek od czynności cywilnoprawnych w wysokości {N1.20} procent, tak że lokal za {E320000} kosztuje około {E356000}, a penthouse za {E480000} około {E534000}, przed opłatami notarialnymi i wieczystoksięgowymi. Wnętrze to powierzchnia użytkowa wewnętrzna z listy, a taras to tarasy zadaszone i niezadaszone razem; lokal na parterze B6-P11-0A ma zamiast niezadaszonego tarasu ogródek przed domem o powierzchni {N49.54} {U}. Większe wewnętrzne powierzchnie zabudowy z listy pominięto w tabeli. Każdy lokal jest podany z miejscem w garażu i komórką lokatorską z numerami; lista nie mówi, że są wliczone w cenę.',
  'Prisene og arealene er hentet fra utbyggerens prisliste, som ikke har trykt dato; filen oppgir {D23.10.2026}. Listen nevner 19 boliger og viser 13 av dem som reservert, og de er ikke tatt med her. Prisene på de øvrige seks er før mva, og 10 prosent mva og {N1.20} prosent dokumentavgift kommer i tillegg, slik at boligen til {E320000} koster omtrent {E356000} og toppleiligheten til {E480000} omtrent {E534000}, før notar- og tinglysingsgebyrer. Innvendig er det innvendige bruksarealet fra listen, og terrasse er de overbygde og uoverbygde terrassene sammen; boligen i første etasje B6-P11-0A har en forhage på {N49.54} {U} i stedet for en uoverbygd terrasse. De større innvendige bebygde arealene fra listen er utelatt fra tabellen. Hver bolig er oppført med en garasjeplass og en bod med nummer; listen sier ikke at de er inkludert i prisen.',
  'Priser och ytor är hämtade från exploatörens prislista, som inte har något tryckt datum; filen anger {D23.10.2026}. Listan nämner 19 bostäder och visar 13 av dem som reserverade, vilka inte är med här. Priserna för de övriga sex är före IVA (spansk moms), och 10 procent IVA och {N1.20} procent stämpelskatt tillkommer, så att bostaden för {E320000} kostar cirka {E356000} och takvåningen för {E480000} cirka {E534000}, före notarie- och registreringsavgifter. Inomhus är den invändiga boytan från listan, och terrass är de överbyggda och öppna terrasserna tillsammans; bostaden i bottenvåningen B6-P11-0A har en trädgård framför på {N49.54} {U} i stället för en öppen terrass. De större invändiga byggda ytorna från listan har lämnats utanför tabellen. Varje bostad är listad med en garageplats och ett förråd med nummer; listan säger inte att de ingår i priset.')

# ---- constructionTimeline ----------------------------------------------------------------------------

a('.constructionTimeline.copy',
  'Una reserva, un contrato privado al concederse la licencia, tres plazos con fecha y la escritura en el primer trimestre de 2029, todo más {T}. Nueva Living confirma el calendario y la fecha de entrega antes de cualquier reserva.',
  'Une réservation, un contrat privé à l’octroi du permis, trois versements datés et l’acte authentique au premier trimestre 2029, le tout hors {T}. Nueva Living confirme le calendrier et la date de livraison avant toute réservation.',
  'Eine Reservierung, ein privater Vertrag bei Erteilung der Baugenehmigung, drei Raten mit festen Terminen und die Beurkundung im ersten Quartal 2029, alles zuzüglich {T}. Nueva Living bestätigt den Zeitplan und den Übergabetermin vor jeder Reservierung.',
  'Бронирование, частный договор при выдаче лицензии, три платежа с фиксированными датами и оформление права собственности в первом квартале 2029 года, всё плюс {T}. Nueva Living подтверждает график и срок сдачи до любого бронирования.',
  'حجز، وعقد خاص عند منح الرخصة، وثلاث دفعات بتواريخ محددة، وسند الملكية في الربع الأول من 2029، كل ذلك زائد {T}. تؤكد Nueva Living الجدول وموعد التسليم قبل أي حجز.',
  'Een reservering, een privécontract bij de verlening van de vergunning, drie termijnen met vaste data en de akte in het eerste kwartaal van 2029, alles plus {T}. Nueva Living bevestigt het schema en de opleveringsdatum vóór een reservering.',
  'Rezerwacja, umowa prywatna przy udzieleniu pozwolenia, trzy raty z ustalonymi terminami i akt notarialny w pierwszym kwartale 2029 roku, wszystko plus {T}. Nueva Living potwierdza harmonogram i termin oddania przed jakąkolwiek rezerwacją.',
  'En reservasjon, en privat kontrakt når tillatelsen innvilges, tre avdrag med faste datoer og skjøtet i første kvartal 2029, alt pluss {T}. Nueva Living bekrefter planen og overleveringsdatoen før enhver reservasjon.',
  'En bokning, ett privat kontrakt när bygglovet beviljas, tre delbetalningar med fasta datum och köpebrevet under första kvartalet 2029, allt plus {T}. Nueva Living bekräftar tidsplanen och tillträdesdatumet före varje reservation.')
a('.constructionTimeline.paymentTerms[0][1]',
  *[expand('{P6000}', l) for l in LOCS])
INCL = {'es': '{E6600} con IVA incluido', 'fr': '{E6600} TVA comprise', 'de': '{E6600} inkl. MwSt.', 'ru': '{E6600} с НДС',
        'ar': '{E6600} شاملة ضريبة القيمة المضافة', 'nl': '{E6600} inclusief btw', 'pl': '{E6600} z VAT', 'no': '{E6600} inkl. mva', 'sv': '{E6600} inklusive IVA'}
a('.constructionTimeline.paymentTerms[0][2]', *[INCL[l] for l in LOCS])
a('.constructionTimeline.paymentTerms[1][2]',
  'Al obtenerse la licencia, menos la reserva', 'À l’obtention du permis, moins la réservation', 'Bei Erteilung der Baugenehmigung, abzüglich der Reservierung',
  'При получении лицензии за вычетом бронирования', 'عند الحصول على الرخصة، مخصومًا منها الحجز', 'Bij het verkrijgen van de vergunning, min de reservering',
  'Po uzyskaniu pozwolenia, pomniejszone o rezerwację', 'Når tillatelsen innvilges, minus reservasjonen', 'När bygglovet beviljas, minus bokningen')
a('.constructionTimeline.paymentTerms[2][0]',
  'Tras el contrato privado', 'Après le contrat privé', 'Nach dem privaten Vertrag', 'После частного договора', 'بعد العقد الخاص',
  'Na het privécontract', 'Po umowie prywatnej', 'Etter den private kontrakten', 'Efter det privata kontraktet')
a('.constructionTimeline.paymentTerms[2][2]',
  'Tres pagos el {D5.3.2027}, el {D5.9.2027} y el {D5.3.2028}', 'Trois versements : le {D5.3.2027}, le {D5.9.2027} et le {D5.3.2028}',
  'Drei Zahlungen am {D5.3.2027}, am {D5.9.2027} und am {D5.3.2028}', 'Три платежа: {D5.3.2027}, {D5.9.2027} и {D5.3.2028}',
  'ثلاث دفعات في {D5.3.2027} و{D5.9.2027} و{D5.3.2028}', 'Drie betalingen op {D5.3.2027}, {D5.9.2027} en {D5.3.2028}',
  'Trzy wpłaty w dniach {D5.3.2027}, {D5.9.2027} i {D5.3.2028}', 'Tre betalinger {D5.3.2027}, {D5.9.2027} og {D5.3.2028}',
  'Tre betalningar den {D5.3.2027}, {D5.9.2027} och {D5.3.2028}')
a('.constructionTimeline.paymentTerms[3][0]',
  'En la escritura', 'À l’acte authentique', 'Bei der Beurkundung', 'При оформлении права собственности', 'عند سند الملكية',
  'Bij de akte', 'Przy akcie notarialnym', 'Ved skjøtet', 'Vid köpebrevet')
a('.constructionTimeline.paymentTerms[3][2]',
  'Primer trimestre de 2029, a la finalización y entrega de llaves', 'Premier trimestre 2029, à l’achèvement et à la remise des clés',
  'Erstes Quartal 2029, bei Fertigstellung und Schlüsselübergabe', 'Первый квартал 2029 года, при завершении строительства и передаче ключей',
  'الربع الأول من 2029، عند الإنجاز وتسليم المفاتيح', 'Eerste kwartaal 2029, bij oplevering en overhandiging van de sleutels',
  'Pierwszy kwartał 2029 roku, przy ukończeniu i wydaniu kluczy', 'Første kvartal 2029, ved ferdigstillelse og overlevering av nøklene',
  'Första kvartalet 2029, vid färdigställande och överlämnande av nycklarna')
a('.constructionTimeline.paymentTermsNote',
  'Calendario de pagos según las condiciones de pago del promotor, que no llevan fecha impresa. Ningún documento que tenemos dice cómo se garantiza el dinero entregado antes de la finalización. Nueva Living confirma con usted directamente las condiciones exactas antes de cualquier reserva.',
  'Échéancier de paiement selon les conditions de paiement du promoteur, qui ne portent aucune date imprimée. Aucun document en notre possession n’indique comment l’argent versé avant l’achèvement est garanti. Nueva Living confirme directement avec vous les conditions exactes avant toute réservation.',
  'Zahlungsplan nach den Zahlungsbedingungen des Bauträgers, die kein gedrucktes Datum tragen. Kein Dokument, das uns vorliegt, sagt, wie das vor der Fertigstellung gezahlte Geld abgesichert ist. Nueva Living bestätigt die genauen Bedingungen direkt mit Ihnen vor jeder Reservierung.',
  'График платежей по условиям оплаты от застройщика, на которых не напечатана дата. Ни в одном имеющемся у нас документе не сказано, как гарантируются деньги, выплаченные до завершения строительства. Nueva Living подтверждает точные условия с вами напрямую до любого бронирования.',
  'جدول الدفع وفق شروط الدفع الصادرة عن المطوّر، التي لا تحمل تاريخًا مطبوعًا. لا تذكر أي وثيقة لدينا كيف تُضمن الأموال المدفوعة قبل الإنجاز. تؤكد Nueva Living الشروط الدقيقة معكم مباشرة قبل أي حجز.',
  'Betaalschema volgens de betalingsvoorwaarden van de ontwikkelaar, die geen gedrukte datum dragen. Geen enkel document dat wij hebben, zegt hoe het geld dat vóór de oplevering is betaald wordt gewaarborgd. Nueva Living bevestigt de exacte voorwaarden rechtstreeks met u vóór een reservering.',
  'Harmonogram płatności zgodnie z warunkami płatności dewelopera, które nie mają wydrukowanej daty. Żaden posiadany przez nas dokument nie mówi, jak zabezpieczone są pieniądze wpłacone przed ukończeniem. Nueva Living potwierdza dokładne warunki bezpośrednio z Państwem przed jakąkolwiek rezerwacją.',
  'Betalingsplan etter utbyggerens betalingsvilkår, som ikke har trykt dato. Ingen dokumenter vi har, sier hvordan penger betalt før ferdigstillelsen er sikret. Nueva Living bekrefter de nøyaktige vilkårene direkte med deg før enhver reservasjon.',
  'Betalningsplan enligt exploatörens betalningsvillkor, som inte har något tryckt datum. Inget dokument vi har säger hur pengar som betalats före färdigställandet är säkrade. Nueva Living bekräftar de exakta villkoren direkt med dig före varje reservation.')
a('.timeline.items[2][2]',
  'Recorremos la zona y repasamos los planos juntos.', 'Nous visitons la zone avec vous et passons les plans en revue ensemble.',
  'Wir sehen uns mit Ihnen die Gegend an und gehen die Pläne gemeinsam durch.', 'Мы вместе осматриваем район и разбираем планы.',
  'نزور المنطقة معكم ونراجع المخططات معًا.', 'We bekijken samen met u de omgeving en gaan de plattegronden samen door.',
  'Razem oglądamy okolicę i omawiamy rzuty.', 'Vi ser på området sammen og går gjennom plantegningene sammen.',
  'Vi tittar på området tillsammans och går igenom planritningarna tillsammans.')
a('.privateViewing.insights[0][1]',
  'Ver la zona y dónde están el mar, los campos de golf y las tiendas.', 'Voir la zone et où se trouvent la mer, les golfs et les commerces.',
  'Die Gegend sehen und wo Meer, Golfplätze und Geschäfte liegen.', 'Увидеть район и где находятся море, поля для гольфа и магазины.',
  'رؤية المنطقة وأين يقع البحر وملاعب الغولف والمتاجر.', 'De omgeving zien en waar de zee, de golfbanen en de winkels liggen.',
  'Zobaczyć okolicę i gdzie leżą morze, pola golfowe i sklepy.', 'Se området og hvor havet, golfbanene og butikkene ligger.',
  'Se området och var havet, golfbanorna och butikerna ligger.')
a('.privateViewing.insights[1][1]',
  'Vamos en coche a Fuengirola, Marbella y Málaga y cronometramos el trayecto.', 'Nous allons en voiture à Fuengirola, Marbella et Málaga avec vous et chronométrons le trajet.',
  'Wir fahren mit Ihnen nach Fuengirola, Marbella und Málaga und stoppen die Zeit.', 'Мы вместе с вами едем в Фуэнхиролу, Марбелью и Малагу и засекаем время.',
  'نقود معكم إلى فوينخيرولا وماربيا ومالقة ونحتسب مدة الرحلة.', 'We rijden met u naar Fuengirola, Marbella en Málaga en nemen de tijd op.',
  'Jedziemy razem samochodem do Fuengiroli, Marbelli i Málagi i mierzymy czas przejazdu.', 'Vi kjører til Fuengirola, Marbella og Málaga sammen og tar tiden.',
  'Vi åker bil till Fuengirola, Marbella och Málaga tillsammans och tar tid på resan.')

# ---- enquiry: the same wording as the other projects, with this project's name -------------------------

_ref = json.load(open('content/liora-projects/aire-estepona/project.json'))
for _k in ('headlineHtml', 'message'):
    put(proj['enquiry'][_k], [_ref['i18n'][l]['enquiry'][_k].replace('Aire Estepona', 'Mijas Horizon Terraces') for l in LOCS])

# ---- faq -------------------------------------------------------------------------------------------

a('.faq[0][1]',
  'El folleto describe 142 apartamentos y áticos de dos y tres dormitorios. La lista de precios nombra 19 de ellos: seis están disponibles, de {E320000} a {E480000} antes de IVA, y 13 figuran como reservados.',
  'La brochure décrit 142 appartements et penthouses de deux et trois chambres. La liste de prix en nomme 19 : six sont disponibles, de {E320000} à {E480000} hors TVA, et 13 sont marqués comme réservés.',
  'Die Broschüre beschreibt 142 Wohnungen und Penthäuser mit zwei und drei Schlafzimmern. Die Preisliste nennt 19 davon: sechs sind verfügbar, von {E320000} bis {E480000} vor MwSt., und 13 sind als reserviert gekennzeichnet.',
  'В брошюре описаны 142 апартамента и пентхауса с двумя и тремя спальнями. В прайс-листе названы 19 из них: шесть доступны, от {E320000} до {E480000} без НДС, а 13 отмечены как зарезервированные.',
  'يصف الكتيّب 142 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم. وتسمّي قائمة الأسعار 19 منها: ستة متاحة، من {E320000} إلى {E480000} قبل ضريبة القيمة المضافة، و13 معلَّمة محجوزة.',
  'De brochure beschrijft 142 appartementen en penthouses met twee en drie slaapkamers. De prijslijst noemt er 19: zes zijn beschikbaar, van {E320000} tot {E480000} vóór btw, en 13 zijn als gereserveerd aangemerkt.',
  'Broszura opisuje 142 apartamenty i penthouse’y z dwiema i trzema sypialniami. Cennik wymienia 19 z nich: sześć jest dostępnych, od {E320000} do {E480000} przed VAT, a 13 jest oznaczonych jako zarezerwowane.',
  'Brosjyren beskriver 142 leiligheter og toppleiligheter med to og tre soverom. Prislisten nevner 19 av dem: seks er tilgjengelige, fra {E320000} til {E480000} før mva, og 13 er merket som reservert.',
  'Broschyren beskriver 142 lägenheter och takvåningar med två och tre sovrum. Prislistan nämner 19 av dem: sex är tillgängliga, från {E320000} till {E480000} före IVA (spansk moms), och 13 är markerade som reserverade.')
a('.faq[1][1]',
  'No. La lista de precios dice que el IVA no está incluido. Se añaden el IVA del 10 por ciento y el impuesto de actos jurídicos documentados del {N1.20} por ciento, además de los gastos de notaría y de registro de la propiedad.',
  'Non. La liste de prix indique que la TVA n’est pas comprise. S’y ajoutent la TVA à 10 pour cent et le droit de timbre à {N1.20} pour cent, ainsi que les frais de notaire et de registre foncier.',
  'Nein. Die Preisliste besagt, dass die MwSt. nicht enthalten ist. Hinzu kommen 10 Prozent MwSt. und {N1.20} Prozent Stempelsteuer sowie die Notar- und Grundbuchkosten.',
  'Нет. В прайс-листе сказано, что НДС не включён. Добавляются НДС 10 процентов и гербовый сбор {N1.20} процента, а также расходы на нотариуса и регистрацию.',
  'لا. تذكر قائمة الأسعار أن ضريبة القيمة المضافة غير مشمولة. وتُضاف ضريبة القيمة المضافة بنسبة 10 بالمئة ورسم الدمغة بنسبة {N1.20} بالمئة، إضافة إلى أتعاب التوثيق والتسجيل العقاري.',
  'Nee. De prijslijst zegt dat btw niet is inbegrepen. Er komen 10 procent btw en {N1.20} procent overdrachtsbelasting bij, samen met de notaris- en kadasterkosten.',
  'Nie. Cennik podaje, że VAT nie jest wliczony. Doliczany jest VAT w wysokości 10 procent i podatek od czynności cywilnoprawnych w wysokości {N1.20} procent, a także opłaty notarialne i wieczystoksięgowe.',
  'Nei. Prislisten sier at mva ikke er inkludert. 10 prosent mva og {N1.20} prosent dokumentavgift kommer i tillegg, sammen med notar- og tinglysingsgebyrer.',
  'Nej. Prislistan anger att IVA inte ingår. 10 procent IVA och {N1.20} procent stämpelskatt tillkommer, tillsammans med notarie- och registreringsavgifter.')
a('.faq[2][1]',
  'La lista de precios da una plaza de garaje y un trastero, con su número, para cada vivienda, y el folleto habla de aparcamiento y trastero. No dice que estén incluidos en el precio, así que lo confirmamos.',
  'La liste de prix donne pour chaque logement une place de garage et une cave, avec leur numéro, et la brochure parle de stationnement et d’une cave. Elle ne dit pas qu’elles sont comprises dans le prix ; nous le confirmons donc.',
  'Die Preisliste nennt für jede Wohnung einen Garagenstellplatz und einen Abstellraum mit Nummer, und die Broschüre spricht von Parkplatz und Abstellraum. Sie sagt nicht, dass beides im Preis enthalten ist, daher bestätigen wir das.',
  'В прайс-листе для каждой квартиры указаны место в гараже и кладовая с номерами, а в брошюре говорится о парковке и кладовой. Там не сказано, что они входят в цену, поэтому мы это подтверждаем.',
  'تذكر قائمة الأسعار لكل مسكن موقفًا في المرآب ومخزنًا بأرقامهما، ويتحدث الكتيّب عن موقف سيارات ومخزن. ولا تذكر أنهما مشمولان في السعر، ولذلك نؤكد ذلك.',
  'De prijslijst geeft voor elke woning een garageplaats en een berging met nummer, en de brochure spreekt van parkeren en een berging. Ze zegt niet dat ze in de prijs zijn inbegrepen, dus dat bevestigen we.',
  'Cennik podaje dla każdego lokalu numer miejsca w garażu i komórki lokatorskiej, a broszura wspomina o parkingu i komórce lokatorskiej. Nie mówi, że są wliczone w cenę, dlatego to potwierdzamy.',
  'Prislisten oppgir en garasjeplass og en bod med nummer for hver bolig, og brosjyren omtaler parkering og en bod. Den sier ikke at de er inkludert i prisen, så det bekrefter vi.',
  'Prislistan anger en garageplats och ett förråd med nummer för varje bostad, och broschyren nämner parkering och ett förråd. Den säger inte att de ingår i priset, så det bekräftar vi.')
a('.faq[3][1]',
  'Las condiciones de pago sitúan la escritura, con la finalización y la entrega de llaves, en el primer trimestre de 2029. Ningún documento indica el estado de la licencia ni el inicio de las obras, así que pedimos la licencia y la fecha contractual.',
  'Les conditions de paiement placent l’acte authentique, avec l’achèvement et la remise des clés, au premier trimestre 2029. Aucun document n’indique le statut du permis ni le début des travaux ; nous demandons donc le permis et la date contractuelle.',
  'Die Zahlungsbedingungen legen die Beurkundung mit Fertigstellung und Schlüsselübergabe auf das erste Quartal 2029. Kein Dokument nennt den Stand der Genehmigung oder einen Baubeginn, daher fordern wir die Genehmigung und den vertraglichen Termin an.',
  'По условиям оплаты оформление права собственности вместе с завершением строительства и передачей ключей намечено на первый квартал 2029 года. Ни один документ не называет статус лицензии или начало работ, поэтому мы запрашиваем лицензию и договорный срок.',
  'تضع شروط الدفع سند الملكية، مع الإنجاز وتسليم المفاتيح، في الربع الأول من 2029. ولا تذكر أي وثيقة وضع الرخصة أو بدء الأشغال، ولذلك نطلب الرخصة والموعد التعاقدي.',
  'De betalingsvoorwaarden plaatsen de akte, met oplevering en overhandiging van de sleutels, in het eerste kwartaal van 2029. Geen enkel document vermeldt de stand van de vergunning of een start van de werken, dus we vragen de vergunning en de contractuele datum op.',
  'Warunki płatności wskazują akt notarialny, wraz z ukończeniem i wydaniem kluczy, w pierwszym kwartale 2029 roku. Żaden dokument nie podaje statusu pozwolenia ani rozpoczęcia prac, dlatego prosimy o pozwolenie i umowny termin.',
  'Betalingsvilkårene legger skjøtet, med ferdigstillelse og overlevering av nøklene, til første kvartal 2029. Ingen dokumenter oppgir status for tillatelsen eller byggestart, så vi ber om tillatelsen og den avtalte datoen.',
  'Betalningsvillkoren lägger köpebrevet, med färdigställande och överlämnande av nycklarna, till första kvartalet 2029. Inget dokument anger bygglovets status eller byggstart, så vi ber om bygglovet och det avtalade datumet.')
a('.faq[4][1]',
  '{E6000} más {T} en la reserva; el 15 por ciento más {T} en el contrato privado, a pagar al obtenerse la licencia, menos la reserva; el 15 por ciento más {T} en tres pagos el {D5.3.2027}, el {D5.9.2027} y el {D5.3.2028}; y el 70 por ciento más {T} en la escritura.',
  '{E6000} hors {T} à la réservation ; 15 pour cent hors {T} au contrat privé, dû à l’obtention du permis, moins la réservation ; 15 pour cent hors {T} en trois versements, le {D5.3.2027}, le {D5.9.2027} et le {D5.3.2028} ; et 70 pour cent hors {T} à l’acte authentique.',
  '{E6000} zuzüglich {T} bei der Reservierung; 15 Prozent zuzüglich {T} beim privaten Vertrag, fällig bei Erteilung der Baugenehmigung, abzüglich der Reservierung; 15 Prozent zuzüglich {T} in drei Raten am {D5.3.2027}, am {D5.9.2027} und am {D5.3.2028}; und 70 Prozent zuzüglich {T} bei der Beurkundung.',
  '{E6000} плюс {T} при бронировании; 15 процентов плюс {T} при частном договоре, подлежащие оплате при получении лицензии, за вычетом бронирования; 15 процентов плюс {T} тремя платежами: {D5.3.2027}, {D5.9.2027} и {D5.3.2028}; и 70 процентов плюс {T} при оформлении права собственности.',
  '{E6000} زائد {T} عند الحجز؛ و15 بالمئة زائد {T} عند العقد الخاص، تُستحق عند الحصول على الرخصة، مخصومًا منها الحجز؛ و15 بالمئة زائد {T} على ثلاث دفعات في {D5.3.2027} و{D5.9.2027} و{D5.3.2028}؛ و70 بالمئة زائد {T} عند سند الملكية.',
  '{E6000} plus {T} bij reservering; 15 procent plus {T} bij het privécontract, verschuldigd bij het verkrijgen van de vergunning, min de reservering; 15 procent plus {T} in drie termijnen op {D5.3.2027}, {D5.9.2027} en {D5.3.2028}; en 70 procent plus {T} bij de akte.',
  '{E6000} plus {T} przy rezerwacji; 15 procent plus {T} przy umowie prywatnej, płatne po uzyskaniu pozwolenia, pomniejszone o rezerwację; 15 procent plus {T} w trzech ratach w dniach {D5.3.2027}, {D5.9.2027} i {D5.3.2028}; oraz 70 procent plus {T} przy akcie notarialnym.',
  '{E6000} pluss {T} ved reservasjon; 15 prosent pluss {T} ved den private kontrakten, forfaller når tillatelsen innvilges, minus reservasjonen; 15 prosent pluss {T} i tre betalinger {D5.3.2027}, {D5.9.2027} og {D5.3.2028}; og 70 prosent pluss {T} ved skjøtet.',
  '{E6000} plus {T} vid bokning; 15 procent plus {T} vid det privata kontraktet, förfaller när bygglovet beviljas, minus bokningen; 15 procent plus {T} i tre betalningar den {D5.3.2027}, {D5.9.2027} och {D5.3.2028}; och 70 procent plus {T} vid köpebrevet.')
a('.faq[5][1]',
  'Una piscina central con zona chill-out, un gimnasio, una zona de spa con sauna, un club social y un espacio de coworking, en jardines paisajísticos, tal como los describen el folleto y la memoria de calidades.',
  'Une piscine centrale avec un espace de détente, une salle de sport, un espace spa avec sauna, un club social et un espace de coworking, dans des jardins paysagers, comme les décrivent la brochure et le descriptif des matériaux.',
  'Ein zentraler Pool mit Chill-out-Bereich, ein Fitnessraum, ein Spa-Bereich mit Sauna, ein Social Club und ein Coworking-Bereich in gepflegten Gärten, so wie Broschüre und Ausstattungsbeschreibung sie darstellen.',
  'Центральный бассейн с зоной отдыха, тренажёрный зал, спа-зона с сауной, соушл-клуб и коворкинг в ландшафтных садах, как они описаны в брошюре и спецификации материалов.',
  'مسبح مركزي بمنطقة استرخاء، ونادٍ رياضي، ومنطقة سبا مع ساونا، ونادٍ اجتماعي، ومساحة عمل مشتركة، في حدائق مُنسَّقة، كما يصفها الكتيّب ومواصفات المواد.',
  'Een centraal zwembad met chill-outzone, een sportruimte, een spa-ruimte met sauna, een sociale club en een coworkingruimte, in aangelegde tuinen, zoals de brochure en de specificatie ze beschrijven.',
  'Centralny basen ze strefą relaksu, siłownia, strefa spa z sauną, klub społeczny i przestrzeń coworkingowa w zagospodarowanych ogrodach, tak jak opisują je broszura i specyfikacja materiałów.',
  'Et sentralt basseng med en chill-out-sone, et treningsrom, et spa-område med badstue, en sosial klubb og et coworking-område, i opparbeidede hager, slik brosjyren og materialbeskrivelsen beskriver dem.',
  'En central pool med en chill-out-yta, ett gym, ett spaområde med bastu, en socialklubb och en coworking-yta, i anlagda trädgårdar, så som broschyren och materialbeskrivningen beskriver dem.')
a('.faq[6][0]',
  '¿Hacia dónde están orientadas las viviendas?', 'Comment sont orientés les logements ?', 'Wie sind die Wohnungen ausgerichtet?',
  'Как ориентированы квартиры?', 'ما اتجاه المساكن؟', 'Hoe liggen de woningen georiënteerd?',
  'Jak zorientowane są lokale?', 'Hvilken retning vender boligene?', 'Åt vilket håll vetter bostäderna?')
a('.faq[6][1]',
  'El folleto dice sur o suroeste. La lista de precios dice oeste para las seis viviendas disponibles. Confirmamos la orientación de la vivienda elegida.',
  'La brochure dit sud ou sud-ouest. La liste de prix dit ouest pour les six logements disponibles. Nous confirmons l’orientation du logement choisi.',
  'Die Broschüre sagt Süden oder Südwesten. Die Preisliste sagt Westen für die sechs verfügbaren Wohnungen. Wir bestätigen die Ausrichtung der gewählten Wohnung.',
  'В брошюре сказано: юг или юго-запад. В прайс-листе для шести доступных квартир указан запад. Ориентацию выбранной квартиры мы подтверждаем.',
  'يقول الكتيّب جنوب أو جنوب غرب. وتقول قائمة الأسعار غرب للمساكن الستة المتاحة. نؤكد اتجاه المسكن المختار.',
  'De brochure zegt zuiden of zuidwesten. De prijslijst zegt west voor de zes beschikbare woningen. We bevestigen de oriëntatie van de gekozen woning.',
  'Broszura podaje południe lub południowy zachód. Cennik podaje zachód dla sześciu dostępnych lokali. Orientację wybranego lokalu potwierdzamy.',
  'Brosjyren sier sør eller sørvest. Prislisten sier vest for de seks tilgjengelige boligene. Vi bekrefter orienteringen til den valgte boligen.',
  'Broschyren säger söder eller sydväst. Prislistan säger väster för de sex tillgängliga bostäderna. Vi bekräftar den valda bostadens väderstreck.')

# ---- seo -------------------------------------------------------------------------------------------

a('.seo.title',
  'Mijas Horizon Terraces - Apartamentos en Mijas Costa', 'Mijas Horizon Terraces - Appartements à Mijas Costa', 'Mijas Horizon Terraces - Wohnungen in Mijas Costa',
  'Mijas Horizon Terraces - Апартаменты в Михас-Коста', 'Mijas Horizon Terraces - شقق في ميخاس كوستا', 'Mijas Horizon Terraces - Appartementen in Mijas Costa',
  'Mijas Horizon Terraces - Apartamenty w Mijas Costa', 'Mijas Horizon Terraces - Leiligheter i Mijas Costa', 'Mijas Horizon Terraces - Lägenheter i Mijas Costa')
_ctx = ['Apartamentos y áticos con terrazas en Mijas Costa', 'Appartements et penthouses avec terrasses à Mijas Costa',
        'Wohnungen und Penthäuser mit Terrassen in Mijas Costa', 'Апартаменты и пентхаусы с террасами в Михас-Коста',
        'شقق وبنتهاوس مع تراسات في ميخاس كوستا', 'Appartementen en penthouses met terrassen in Mijas Costa',
        'Apartamenty i penthouse’y z tarasami w Mijas Costa', 'Leiligheter og toppleiligheter med terrasser i Mijas Costa',
        'Lägenheter och takvåningar med terrasser i Mijas Costa']
a('.seo.h1Context', *_ctx)
a('.seo.h1', *['Mijas Horizon Terraces: ' + c for c in _ctx])

# assemble.py's pattern for "N% + VAT" gives Swedish "moms", which the audit forbids: set them here.
for _pc in ('15', '70'):
    T[f'{_pc}% + VAT'] = {l: f'{_pc}% + {TAXW[l]}' for l in LOCS}

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings')
