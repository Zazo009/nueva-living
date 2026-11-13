# -*- coding: utf-8 -*-
"""Torrevigía Residences: the strings the translation memory did not have.

Same shape as k_selwo.py: one a() per string, positionally a(index, hint, es, fr, de, ru, ar, nl, pl, no, sv),
where `index` is the string's position in todo.json and `hint` the start of its English, asserted so a reordered
todo cannot shift a translation onto the wrong string. Unit references stay as printed; unit sizes are a template;
floor labels are left to assemble.py (floor_parts.json). Tokens: {E638000} money, {N131.05} number, {U} m2.

    python3 tools/import/k_torrevigia_residences.py <workdir>     # writes <workdir>/tr_t.json
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {'es': 'm²', 'fr': 'm²', 'de': 'm²', 'ru': 'м²', 'ar': 'م²', 'nl': 'm²', 'pl': 'm²', 'no': 'm²', 'sv': 'm²'}
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


def a(i, hint, *tr):
    en = todo[i]
    assert en.startswith(hint), (i, hint, en[:60])
    assert len(tr) == 9, (i, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---------------------------------------------------------------- templates
SIZE = {
    'es': ('{b} m² construido, {u} m² superficie útil', ', {t} m² terraza'),
    'fr': ('{b} m² construit, {u} m² surface utile', ', {t} m² terrasse'),
    'de': ('{b} m² bebaut, {u} m² Wohnfläche', ', {t} m² Terrasse'),
    'ru': ('{b} м² застройка, {u} м² полезная площадь', ', {t} м² терраса'),
    'ar': ('{b} م² مبنية, {u} م² مساحة صافية', ', {t} م² تراس'),
    'nl': ('{b} m² bebouwd, {u} m² nuttige oppervlakte', ', {t} m² terras'),
    'pl': ('{b} m² powierzchnia zabudowy, {u} m² powierzchnia użytkowa', ', {t} m² taras'),
    'no': ('{b} m² bygget, {u} m² nyttbart areal', ', {t} m² terrasse'),
    'sv': ('{b} m² byggyta, {u} m² nyttoyta', ', {t} m² terrass'),
}
for en in todo:
    if re.fullmatch(r'\d-\d+-\d+-[A-Z]', en):          # a unit reference, kept as printed
        T[en] = {l: en for l in LOCS}
        continue
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm usable(?:, ([\d.]+) sqm terrace)?', en)
    if m:
        b, u, t = m.groups()
        T[en] = {l: SIZE[l][0].format(b=num(b, l), u=num(u, l)) + (SIZE[l][1].format(t=num(t, l)) if t else '')
                 for l in LOCS}
for en in ('Torrevigía Residences', 'Torrevigía', 'Torrevigía <em>Residences</em>', 'Torrevigía, Estepona'):
    if en in todo:
        T[en] = {l: en for l in LOCS}

# ---------------------------------------------------------------- prose
a(3, 'Nineteen finished apartments listed',
  'Diecinueve apartamentos terminados y listos para entrar a vivir, en dos fases de un mismo conjunto en la ladera de Torrevigía, Estepona, junto a Selwo Aventura: de dos a cuatro dormitorios, de {N131.05} a {N196.08} {U} construidos, terrazas cubiertas de 33 a 50 {U}, piscina comunitaria y acceso a un club de residentes con piscina interior climatizada, gimnasio y saunas.',
  'Dix-neuf appartements achevés et prêts à habiter, répartis sur deux phases d’un même ensemble à flanc de colline à Torrevigía, Estepona, à côté de Selwo Aventura : de deux à quatre chambres, de {N131.05} à {N196.08} {U} construits, des terrasses couvertes de 33 à 50 {U}, une piscine commune et l’accès à un club des résidents avec piscine intérieure chauffée, salle de sport et saunas.',
  'Neunzehn fertiggestellte, bezugsfertige Wohnungen in zwei Bauabschnitten einer Anlage am Hang von Torrevigía, Estepona, neben Selwo Aventura: zwei bis vier Schlafzimmer, {N131.05} bis {N196.08} {U} bebaute Fläche, überdachte Terrassen von 33 bis 50 {U}, ein Gemeinschaftspool und Zugang zu einem Bewohnerclub mit beheiztem Hallenbad, Fitnessraum und Saunen.',
  'Девятнадцать готовых квартир, доступных к заселению, в двух очередях одного комплекса на склоне в Торревихии, Эстепона, рядом с Selwo Aventura: от двух до четырёх спален, от {N131.05} до {N196.08} {U} площади застройки, крытые террасы от 33 до 50 {U}, общий бассейн и доступ в клуб для жителей с крытым подогреваемым бассейном, тренажёрным залом и саунами.',
  'تسع عشرة شقة مكتملة وجاهزة للسكن، في مرحلتين من مجمّع واحد على سفح التل في توريفيخيا، إستيبونا، بجوار Selwo Aventura: من غرفتي نوم إلى أربع غرف، ومن {N131.05} إلى {N196.08} {U} مبنية، وتراسات مسقوفة من 33 إلى 50 {U}، ومسبح مشترك، وإمكانية دخول نادي السكان بمسبح داخلي مدفأ وصالة رياضية وساونا.',
  'Negentien opgeleverde appartementen, klaar om in te trekken, in twee fasen van één complex op de heuvel in Torrevigía, Estepona, naast Selwo Aventura: twee tot vier slaapkamers, {N131.05} tot {N196.08} {U} bebouwd, overdekte terrassen van 33 tot 50 {U}, een gemeenschappelijk zwembad en toegang tot een bewonersclub met verwarmd binnenzwembad, fitnessruimte en sauna’s.',
  'Dziewiętnaście ukończonych mieszkań gotowych do zamieszkania, w dwóch etapach jednego osiedla na zboczu w Torrevigía, Estepona, obok Selwo Aventura: od dwóch do czterech sypialni, od {N131.05} do {N196.08} {U} powierzchni zabudowy, zadaszone tarasy od 33 do 50 {U}, wspólny basen i dostęp do klubu mieszkańców z krytym podgrzewanym basenem, siłownią i saunami.',
  'Nitten ferdigstilte leiligheter, klare til innflytting, i to byggetrinn av ett anlegg i åssiden i Torrevigía, Estepona, ved Selwo Aventura: to til fire soverom, {N131.05} til {N196.08} {U} bygget, overbygde terrasser på 33 til 50 {U}, et felles basseng og tilgang til en beboerklubb med oppvarmet innendørsbasseng, treningsrom og badstuer.',
  'Nitton färdiga lägenheter, inflyttningsklara, i två etapper av ett och samma område i sluttningen i Torrevigía, Estepona, intill Selwo Aventura: två till fyra sovrum, {N131.05} till {N196.08} {U} byggyta, övertäckta terrasser på 33 till 50 {U}, en gemensam pool och tillgång till en klubb för de boende med uppvärmd inomhuspool, gym och bastur.')

a(4, 'Nineteen ready apartments at',
  'Diecinueve apartamentos listos para entrar a vivir en Torrevigía, Estepona: de dos a cuatro dormitorios, de 131 a 196 {U} construidos, terrazas cubiertas, piscina comunitaria y club de residentes con piscina interior.',
  'Dix-neuf appartements prêts à habiter à Torrevigía, Estepona : deux à quatre chambres, 131 à 196 {U} construits, terrasses couvertes, piscine commune et club des résidents avec piscine intérieure.',
  'Neunzehn bezugsfertige Wohnungen in Torrevigía, Estepona: zwei bis vier Schlafzimmer, 131 bis 196 {U} bebaut, überdachte Terrassen, Gemeinschaftspool und Bewohnerclub mit Hallenbad.',
  'Девятнадцать готовых квартир в Торревихии, Эстепона: от двух до четырёх спален, от 131 до 196 {U} застройки, крытые террасы, общий бассейн и клуб для жителей с крытым бассейном.',
  'تسع عشرة شقة جاهزة للسكن في توريفيخيا، إستيبونا: من غرفتي نوم إلى أربع، ومن 131 إلى 196 {U} مبنية، وتراسات مسقوفة، ومسبح مشترك، ونادٍ للسكان بمسبح داخلي.',
  'Negentien appartementen, klaar om in te trekken, in Torrevigía, Estepona: twee tot vier slaapkamers, 131 tot 196 {U} bebouwd, overdekte terrassen, een gemeenschappelijk zwembad en een bewonersclub met binnenzwembad.',
  'Dziewiętnaście mieszkań gotowych do zamieszkania w Torrevigía, Estepona: od dwóch do czterech sypialni, od 131 do 196 {U} zabudowy, zadaszone tarasy, wspólny basen i klub mieszkańców z krytym basenem.',
  'Nitten innflyttingsklare leiligheter i Torrevigía, Estepona: to til fire soverom, 131 til 196 {U} bygget, overbygde terrasser, felles basseng og beboerklubb med innendørsbasseng.',
  'Nitton inflyttningsklara lägenheter i Torrevigía, Estepona: två till fyra sovrum, 131 till 196 {U} byggyta, övertäckta terrasser, gemensam pool och en klubb för de boende med inomhuspool.')
a(5, 'Finished apartments on the hillside',
  'Apartamentos terminados en la ladera de Torrevigía, Estepona, con terrazas cubiertas, piscina comunitaria y club de residentes. Desde {E638000}.',
  'Appartements achevés à flanc de colline à Torrevigía, Estepona, avec terrasses couvertes, piscine commune et club des résidents. À partir de {E638000}.',
  'Fertiggestellte Wohnungen am Hang von Torrevigía, Estepona, mit überdachten Terrassen, Gemeinschaftspool und Bewohnerclub. Ab {E638000}.',
  'Готовые квартиры на склоне в Торревихии, Эстепона, с крытыми террасами, общим бассейном и клубом для жителей. От {E638000}.',
  'شقق مكتملة على سفح التل في توريفيخيا، إستيبونا، بتراسات مسقوفة ومسبح مشترك ونادٍ للسكان. ابتداءً من {E638000}.',
  'Opgeleverde appartementen op de heuvel in Torrevigía, Estepona, met overdekte terrassen, een gemeenschappelijk zwembad en een bewonersclub. Vanaf {E638000}.',
  'Ukończone mieszkania na zboczu w Torrevigía, Estepona, z zadaszonymi tarasami, wspólnym basenem i klubem mieszkańców. Od {E638000}.',
  'Ferdigstilte leiligheter i åssiden i Torrevigía, Estepona, med overbygde terrasser, felles basseng og beboerklubb. Fra {E638000}.',
  'Färdiga lägenheter i sluttningen i Torrevigía, Estepona, med övertäckta terrasser, gemensam pool och en klubb för de boende. Från {E638000}.')
a(6, 'Nineteen homes available',
  'Diecinueve viviendas disponibles / listas para entrar a vivir',
  'Dix-neuf logements disponibles / prêts à habiter',
  'Neunzehn Wohnungen verfügbar / bezugsfertig',
  'Девятнадцать квартир в продаже / готовы к заселению',
  'تسعة عشر مسكناً متاحاً / جاهزة للسكن',
  'Negentien woningen beschikbaar / klaar om in te trekken',
  'Dziewiętnaście mieszkań dostępnych / gotowe do zamieszkania',
  'Nitten boliger tilgjengelige / klare til innflytting',
  'Nitton bostäder tillgängliga / inflyttningsklara')
a(8, 'Nineteen finished apartments on the hillside',
  'Diecinueve apartamentos terminados en la ladera de Torrevigía, Estepona, con terrazas cubiertas, piscina comunitaria y un club de residentes con piscina interior.',
  'Dix-neuf appartements achevés à flanc de colline à Torrevigía, Estepona, avec terrasses couvertes, piscine commune et un club des résidents doté d’une piscine intérieure.',
  'Neunzehn fertiggestellte Wohnungen am Hang von Torrevigía, Estepona, mit überdachten Terrassen, Gemeinschaftspool und einem Bewohnerclub mit Hallenbad.',
  'Девятнадцать готовых квартир на склоне в Торревихии, Эстепона, с крытыми террасами, общим бассейном и клубом для жителей с крытым бассейном.',
  'تسع عشرة شقة مكتملة على سفح التل في توريفيخيا، إستيبونا، بتراسات مسقوفة ومسبح مشترك ونادٍ للسكان بمسبح داخلي.',
  'Negentien opgeleverde appartementen op de heuvel in Torrevigía, Estepona, met overdekte terrassen, een gemeenschappelijk zwembad en een bewonersclub met binnenzwembad.',
  'Dziewiętnaście ukończonych mieszkań na zboczu w Torrevigía, Estepona, z zadaszonymi tarasami, wspólnym basenem i klubem mieszkańców z krytym basenem.',
  'Nitten ferdigstilte leiligheter i åssiden i Torrevigía, Estepona, med overbygde terrasser, felles basseng og en beboerklubb med innendørsbasseng.',
  'Nitton färdiga lägenheter i sluttningen i Torrevigía, Estepona, med övertäckta terrasser, gemensam pool och en klubb för de boende med inomhuspool.')

# ---- image alts and captions. "Computer-generated view of" follows the memory's wording per locale.
CG = {'es': 'Vista generada por ordenador de ', 'fr': 'Vue de synthèse ', 'de': 'Computergenerierte Ansicht ',
      'ru': 'Компьютерная визуализация: ', 'ar': 'منظر مُولَّد بالحاسوب ', 'nl': 'Computergegenereerd beeld van ',
      'pl': 'Komputerowa wizualizacja: ', 'no': 'Datagenerert bilde av ', 'sv': 'Datorgenererad bild av '}


def cg(i, hint, *rest):
    a(i, hint, *[(CG[l] + r).replace('ordenador de el ', 'ordenador del ') for l, r in zip(LOCS, rest)])


cg(9, 'Computer-generated view of the blocks on the hillside, with the coast',
   'los bloques en la ladera, con la costa y el mar al fondo', 'des blocs à flanc de colline, avec la côte et la mer au loin',
   'der Blöcke am Hang, dahinter die Küste und das Meer', 'корпуса на склоне, вдали побережье и море',
   'للمباني على سفح التل، ويظهر الساحل والبحر في الخلفية', 'de blokken op de heuvel, met de kust en de zee op de achtergrond',
   'bloki na zboczu, w tle wybrzeże i morze', 'blokkene i åssiden, med kysten og havet i bakgrunnen', 'husen i sluttningen, med kusten och havet i bakgrunden')
cg(10, 'Computer-generated view of the blocks stepping down',
   'los bloques escalonados en la pendiente, con terrazas ajardinadas en cada planta', 'des blocs en gradins sur la pente, avec des terrasses plantées à chaque étage',
   'der Blöcke, die sich den Hang hinab staffeln, mit bepflanzten Terrassen auf jeder Etage', 'корпуса уступами на склоне, с озеленёнными террасами на каждом этаже',
   'للمباني المتدرجة على المنحدر، مع تراسات مزروعة في كل طابق', 'de blokken die trapsgewijs de helling af lopen, met beplante terrassen op elke verdieping',
   'bloki schodzące tarasowo po zboczu, z obsadzonymi zielenią tarasami na każdym piętrze', 'blokkene som trapper seg nedover skråningen, med beplantede terrasser i hver etasje',
   'husen som trappar ner för sluttningen, med planterade terrasser på varje våning')
cg(11, 'Computer-generated view of a covered terrace with a sofa',
   'una terraza cubierta con sofá y mesa de comedor, con las montañas al fondo', 'd’une terrasse couverte avec canapé et table à manger, les montagnes au loin',
   'einer überdachten Terrasse mit Sofa und Esstisch, dahinter die Berge', 'крытая терраса с диваном и обеденным столом, вдали горы',
   'لتراس مسقوف مع أريكة وطاولة طعام، والجبال في الخلفية', 'een overdekt terras met een bank en eettafel, met de bergen op de achtergrond',
   'zadaszony taras z sofą i stołem jadalnym, w tle góry', 'en overbygd terrasse med sofa og spisebord, med fjellene i bakgrunnen',
   'en övertäckt terrass med soffa och matbord, med bergen i bakgrunden')
a(12, 'Computer-generated images from the developer',
  'Imágenes generadas por ordenador del folleto del promotor, realizadas antes de terminar los edificios: muestran las viviendas, las terrazas, las zonas comunes y el club de residentes tal como se proyectaron, no tal como se construyeron. El mobiliario y la decoración son orientativos y no están incluidos en la venta.',
  'Images de synthèse issues de la brochure du promoteur, réalisées avant l’achèvement des bâtiments : elles montrent les logements, les terrasses, les parties communes et le club des résidents tels qu’ils ont été conçus, et non tels qu’ils ont été construits. Le mobilier et la décoration sont indicatifs et ne sont pas compris dans la vente.',
  'Computergenerierte Bilder aus der Broschüre des Bauträgers, entstanden vor der Fertigstellung der Gebäude: Sie zeigen die Wohnungen, die Terrassen, die Gemeinschaftsbereiche und den Bewohnerclub wie geplant, nicht wie gebaut. Möbel und Dekoration sind beispielhaft und nicht im Kaufpreis enthalten.',
  'Компьютерные визуализации из брошюры застройщика, созданные до завершения строительства: они показывают квартиры, террасы, общие зоны и клуб для жителей такими, какими они были задуманы, а не построены. Мебель и декор приведены для примера и в продажу не входят.',
  'صور مُولَّدة بالحاسوب من كتيّب المطوّر، أُعدّت قبل اكتمال المباني: تُظهر المساكن والتراسات والمناطق المشتركة ونادي السكان كما صُمّمت، لا كما بُنيت. الأثاث والديكور للإيضاح فقط وليسا مشمولين في البيع.',
  'Computergegenereerde beelden uit de brochure van de ontwikkelaar, gemaakt voordat de gebouwen klaar waren: ze tonen de woningen, de terrassen, de gemeenschappelijke ruimten en de bewonersclub zoals ontworpen, niet zoals gebouwd. Meubilair en inrichting zijn indicatief en niet bij de koop inbegrepen.',
  'Wizualizacje komputerowe z broszury dewelopera, wykonane przed ukończeniem budynków: pokazują mieszkania, tarasy, części wspólne i klub mieszkańców tak, jak je zaprojektowano, a nie jak je zbudowano. Meble i wystrój są poglądowe i nie wchodzą w zakres sprzedaży.',
  'Datagenererte bilder fra utbyggerens brosjyre, laget før byggene var ferdige: de viser boligene, terrassene, fellesområdene og beboerklubben slik de ble prosjektert, ikke slik de ble bygget. Møbler og innredning er veiledende og inngår ikke i salget.',
  'Datorgenererade bilder ur exploatörens broschyr, gjorda innan husen stod klara: de visar bostäderna, terrasserna, de gemensamma ytorna och de boendes klubb så som de projekterades, inte så som de byggdes. Möbler och inredning är vägledande och ingår inte i köpet.')
cg(13, 'Computer-generated view of the blocks and the pool among pines',
   'los bloques y la piscina entre pinos, con las montañas detrás', 'des blocs et de la piscine parmi les pins, avec les montagnes derrière',
   'der Blöcke und des Pools zwischen Pinien, dahinter die Berge', 'корпуса и бассейн среди сосен, позади горы',
   'للمباني والمسبح بين أشجار الصنوبر، والجبال من خلفها', 'de blokken en het zwembad tussen de pijnbomen, met de bergen erachter',
   'bloki i basen wśród sosen, w tle góry', 'blokkene og bassenget blant furutrær, med fjellene bak', 'husen och poolen bland tallar, med bergen bakom')
cg(14, 'Computer-generated view of two blocks on the wooded hillside',
   'dos bloques en la ladera arbolada, con el mar a lo lejos', 'de deux blocs sur la colline boisée, avec la mer au loin',
   'zweier Blöcke am bewaldeten Hang, in der Ferne das Meer', 'два корпуса на лесистом склоне, вдали море',
   'لمبنيين على سفح التل المشجّر، والبحر في البعيد', 'twee blokken op de beboste heuvel, met de zee in de verte',
   'dwa bloki na zalesionym zboczu, w oddali morze', 'to blokker i den skogkledde åssiden, med havet i det fjerne', 'två hus i den skogklädda sluttningen, med havet i fjärran')
a(15, 'On the hillside', 'En la ladera', 'À flanc de colline', 'Am Hang', 'На склоне', 'على سفح التل', 'Op de heuvel', 'Na zboczu', 'I åssiden', 'I sluttningen')
cg(16, 'Computer-generated view of the terraced blocks above',
   'los bloques escalonados sobre la piscina comunitaria y los jardines', 'des blocs en gradins au-dessus de la piscine commune et des jardins',
   'der terrassierten Blöcke über dem Gemeinschaftspool und den Gärten', 'корпуса уступами над общим бассейном и садами',
   'للمباني المتدرجة فوق المسبح المشترك والحدائق', 'de getrapte blokken boven het gemeenschappelijke zwembad en de tuinen',
   'tarasowe bloki nad wspólnym basenem i ogrodami', 'de terrasserte blokkene over fellesbassenget og hagene', 'de terrasserade husen ovanför den gemensamma poolen och trädgårdarna')
cg(17, 'Computer-generated view of curved terraces at dusk',
   'terrazas curvas al atardecer sobre un césped con muebles de exterior', 'de terrasses courbes au crépuscule au-dessus d’une pelouse avec du mobilier d’extérieur',
   'geschwungener Terrassen in der Abenddämmerung über einem Rasen mit Gartenmöbeln', 'изогнутые террасы в сумерках над газоном с уличной мебелью',
   'لتراسات منحنية عند الغسق فوق عشب عليه أثاث خارجي', 'gebogen terrassen in de schemering boven een gazon met tuinmeubilair',
   'zaokrąglone tarasy o zmierzchu nad trawnikiem z meblami ogrodowymi', 'buede terrasser i skumringen over en plen med utemøbler', 'svängda terrasser i skymningen ovanför en gräsmatta med utemöbler')
a(18, 'Terraces at dusk', 'Terrazas al atardecer', 'Terrasses au crépuscule', 'Terrassen in der Dämmerung', 'Террасы в сумерках', 'التراسات عند الغسق',
  'Terrassen in de schemering', 'Tarasy o zmierzchu', 'Terrasser i skumringen', 'Terrasser i skymningen')
cg(19, 'Computer-generated view of a long pool beside a glazed',
   'una piscina alargada junto a un edificio común acristalado, con los bloques encima', 'd’une longue piscine à côté d’un bâtiment commun vitré, avec les blocs au-dessus',
   'eines langen Pools neben einem verglasten Gemeinschaftsgebäude, darüber die Blöcke', 'длинный бассейн рядом с остеклённым общим зданием, выше корпуса',
   'لمسبح طويل بجوار مبنى مشترك زجاجي، والمباني فوقه', 'een langgerekt zwembad naast een glazen gemeenschappelijk gebouw, met de blokken erboven',
   'długi basen obok przeszklonego budynku wspólnego, powyżej bloki', 'et langt basseng ved et glassfasadert fellesbygg, med blokkene over', 'en lång pool intill en glasad gemensam byggnad, med husen ovanför')
cg(20, 'Computer-generated view of sun loungers and parasols',
   'tumbonas y sombrillas en el césped junto a la piscina comunitaria', 'de transats et de parasols sur la pelouse au bord de la piscine commune',
   'von Sonnenliegen und Schirmen auf dem Rasen neben dem Gemeinschaftspool', 'шезлонги и зонты на газоне у общего бассейна',
   'لكراسي استلقاء ومظلات على العشب بجانب المسبح المشترك', 'ligbedden en parasols op het gazon naast het gemeenschappelijke zwembad',
   'leżaki i parasole na trawniku przy wspólnym basenie', 'solsenger og parasoller på plenen ved fellesbassenget', 'solsängar och parasoller på gräsmattan vid den gemensamma poolen')
a(21, 'By the pool', 'Junto a la piscina', 'Au bord de la piscine', 'Am Pool', 'У бассейна', 'بجانب المسبح', 'Bij het zwembad', 'Przy basenie', 'Ved bassenget', 'Vid poolen')
cg(22, 'Computer-generated view of upper-floor terraces over',
   'terrazas de las plantas altas sobre un valle arbolado, con el mar al fondo', 'des terrasses des étages supérieurs au-dessus d’une vallée boisée, avec la mer au loin',
   'der Terrassen der oberen Etagen über einem bewaldeten Tal, dahinter das Meer', 'террасы верхних этажей над лесистой долиной, вдали море',
   'لتراسات الطوابق العليا فوق وادٍ مشجّر، والبحر في الخلفية', 'terrassen op de bovenverdiepingen boven een beboste vallei, met de zee op de achtergrond',
   'tarasy wyższych pięter nad zalesioną doliną, w tle morze', 'terrasser i de øvre etasjene over en skogkledd dal, med havet i bakgrunnen', 'terrasser på de övre våningarna ovanför en skogklädd dal, med havet i bakgrunden')
a(23, 'Upper terraces', 'Terrazas superiores', 'Terrasses supérieures', 'Obere Terrassen', 'Верхние террасы', 'التراسات العليا', 'Bovenste terrassen', 'Górne tarasy', 'Øvre terrasser', 'Övre terrasser')
cg(24, 'Computer-generated view of a terrace under a pergola',
   'una terraza bajo una pérgola, con sofás y el mar al fondo', 'd’une terrasse sous une pergola, avec des canapés et la mer au loin',
   'einer Terrasse unter einer Pergola, mit Sofas und dem Meer im Hintergrund', 'терраса под перголой, с диванами и видом на море',
   'لتراس تحت برغولة، مع أرائك والبحر في الخلفية', 'een terras onder een pergola, met banken en de zee op de achtergrond',
   'taras pod pergolą, z sofami i morzem w tle', 'en terrasse under en pergola, med sofaer og havet i bakgrunnen', 'en terrass under en pergola, med soffor och havet i bakgrunden')
cg(25, 'Computer-generated view of the communal lawn',
   'el césped comunitario con tumbonas, árboles y el mar en el horizonte', 'de la pelouse commune avec des transats, des arbres et la mer à l’horizon',
   'des Gemeinschaftsrasens mit Liegen, Bäumen und dem Meer am Horizont', 'общий газон с шезлонгами, деревьями и морем на горизонте',
   'للعشب المشترك مع كراسي استلقاء وأشجار والبحر في الأفق', 'het gemeenschappelijke gazon met ligbedden, bomen en de zee aan de horizon',
   'wspólny trawnik z leżakami, drzewami i morzem na horyzoncie', 'fellesplenen med solsenger, trær og havet i horisonten', 'den gemensamma gräsmattan med solsängar, träd och havet vid horisonten')
cg(26, 'Computer-generated view of the living room with the open kitchen',
   'el salón con la cocina abierta y el comedor detrás', 'du séjour avec la cuisine ouverte et le coin repas derrière',
   'des Wohnzimmers mit der offenen Küche und dem Essbereich dahinter', 'гостиная с открытой кухней и обеденной зоной позади',
   'لغرفة المعيشة مع المطبخ المفتوح ومنطقة الطعام خلفها', 'de woonkamer met de open keuken en de eethoek erachter',
   'salon z otwartą kuchnią i jadalnią w głębi', 'stuen med det åpne kjøkkenet og spisestuen bak', 'vardagsrummet med det öppna köket och matplatsen bakom')
cg(27, 'Computer-generated view of the kitchen with an island',
   'la cocina con isla, muebles altos de frente de madera y columna de horno', 'de la cuisine avec îlot, meubles hauts à façade bois et colonne four',
   'der Küche mit Kochinsel, Oberschränken mit Holzfronten und Backofen-Hochschrank', 'кухня с островом, навесными шкафами с деревянными фасадами и колонной с духовкой',
   'للمطبخ مع جزيرة وخزائن علوية بواجهات خشبية وعمود للفرن', 'de keuken met een kookeiland, bovenkasten met houten fronten en een ovenkolom',
   'kuchnia z wyspą, górnymi szafkami z drewnianymi frontami i słupkiem z piekarnikiem', 'kjøkkenet med kjøkkenøy, overskap med trefronter og en ovnskolonne',
   'köket med köksö, överskåp med träfronter och ett ugnsskåp')
cg(28, 'Computer-generated view of the living room with a corner sofa',
   'el salón con un sofá rinconero y una mesa baja de madera', 'du séjour avec un canapé d’angle et une table basse en bois',
   'des Wohnzimmers mit Ecksofa und niedrigem Holztisch', 'гостиная с угловым диваном и низким деревянным столиком',
   'لغرفة المعيشة مع أريكة زاوية وطاولة خشبية منخفضة', 'de woonkamer met een hoekbank en een lage houten tafel',
   'salon z narożną sofą i niskim drewnianym stolikiem', 'stuen med en hjørnesofa og et lavt bord i tre', 'vardagsrummet med en hörnsoffa och ett lågt träbord')
cg(29, 'Computer-generated view of the living room opening',
   'el salón abierto a la terraza a través de puertas correderas de cristal', 'du séjour ouvert sur la terrasse par des baies coulissantes vitrées',
   'des Wohnzimmers, das sich über gläserne Schiebetüren zur Terrasse öffnet', 'гостиная, выходящая на террасу через раздвижные стеклянные двери',
   'لغرفة المعيشة المفتوحة على التراس عبر أبواب زجاجية منزلقة', 'de woonkamer die via glazen schuifdeuren uitkomt op het terras',
   'salon otwierający się na taras przez przesuwne drzwi szklane', 'stuen som åpner seg mot terrassen gjennom skyvedører i glass', 'vardagsrummet som öppnar sig mot terrassen genom skjutdörrar i glas')
cg(30, 'Computer-generated view of the main bedroom',
   'el dormitorio principal con un espejo alto y una ventana al mar', 'de la chambre principale avec un grand miroir et une fenêtre sur la mer',
   'des Hauptschlafzimmers mit hohem Spiegel und Fenster zum Meer', 'главная спальня с высоким зеркалом и окном на море',
   'لغرفة النوم الرئيسية مع مرآة طويلة ونافذة على البحر', 'de hoofdslaapkamer met een hoge spiegel en een raam naar zee',
   'główna sypialnia z wysokim lustrem i oknem z widokiem na morze', 'hovedsoverommet med et høyt speil og et vindu mot havet', 'huvudsovrummet med en hög spegel och ett fönster mot havet')
cg(31, 'Computer-generated view of the main bathroom',
   'el baño principal con lavabo doble y ducha a ras de suelo', 'de la salle de bains principale avec double vasque et douche à l’italienne',
   'des Hauptbads mit Doppelwaschtisch und bodengleicher Dusche', 'главная ванная с двойной раковиной и душем без поддона',
   'للحمّام الرئيسي مع مغسلة مزدوجة ودش مفتوح', 'de hoofdbadkamer met een dubbele wastafel en een inloopdouche',
   'łazienka główna z podwójną umywalką i prysznicem typu walk-in', 'hovedbadet med dobbel servant og walk-in-dusj', 'huvudbadrummet med dubbel tvättställ och walk in-dusch')
cg(32, 'Computer-generated view of the second bathroom',
   'el segundo baño con ducha, mueble de lavabo suspendido y espejo iluminado', 'de la deuxième salle de bains avec douche, meuble vasque suspendu et miroir éclairé',
   'des zweiten Bads mit Dusche, wandhängendem Waschtisch und beleuchtetem Spiegel', 'вторая ванная с душем, подвесной тумбой и зеркалом с подсветкой',
   'للحمّام الثاني مع دش وخزانة مغسلة معلّقة ومرآة مضاءة', 'de tweede badkamer met een douche, een zwevend wastafelmeubel en een verlichte spiegel',
   'druga łazienka z prysznicem, wiszącą szafką umywalkową i podświetlanym lustrem', 'det andre badet med dusj, vegghengt servantskap og opplyst speil',
   'det andra badrummet med dusch, vägghängt tvättställsskåp och belyst spegel')
cg(33, "Computer-generated view of the residents' club heated",
   'la piscina interior climatizada del club de residentes, con ventanales a una terraza', 'de la piscine intérieure chauffée du club des résidents, avec des baies donnant sur une terrasse',
   'des beheizten Hallenbads im Bewohnerclub, mit Fenstern zu einer Terrasse', 'крытый подогреваемый бассейн клуба для жителей, с окнами на террасу',
   'للمسبح الداخلي المدفأ في نادي السكان، بنوافذ تطل على تراس', 'het verwarmde binnenzwembad van de bewonersclub, met ramen op een terras',
   'kryty podgrzewany basen klubu mieszkańców, z oknami na taras', 'det oppvarmede innendørsbassenget i beboerklubben, med vinduer mot en terrasse',
   'den uppvärmda inomhuspoolen i de boendes klubb, med fönster mot en terrass')
cg(34, "Computer-generated view of the residents' club gym",
   'el gimnasio del club de residentes, con máquinas de cardio junto a una pared acristalada', 'de la salle de sport du club des résidents, avec des machines de cardio le long d’une paroi vitrée',
   'des Fitnessraums im Bewohnerclub, mit Cardiogeräten an einer Glasfront', 'тренажёрный зал клуба для жителей, с кардиотренажёрами вдоль остеклённой стены',
   'لصالة نادي السكان الرياضية، بأجهزة كارديو على امتداد جدار زجاجي', 'de fitnessruimte van de bewonersclub, met cardioapparatuur langs een glazen wand',
   'siłownia klubu mieszkańców, ze sprzętem cardio wzdłuż przeszklonej ściany', 'treningsrommet i beboerklubben, med kondisjonsapparater langs en glassvegg',
   'gymmet i de boendes klubb, med konditionsmaskiner längs en glasvägg')
cg(35, "Computer-generated view of the residents' club dining",
   'el comedor del club de residentes, con lámparas colgantes de mimbre', 'de la salle à manger du club des résidents, avec des suspensions en osier',
   'des Speisesaals im Bewohnerclub, mit Hängeleuchten aus Korbgeflecht', 'обеденный зал клуба для жителей с плетёными подвесными светильниками',
   'لصالة الطعام في نادي السكان، مع مصابيح معلّقة من الخيزران', 'de eetzaal van de bewonersclub, met hanglampen van riet',
   'jadalnia klubu mieszkańców z wiklinowymi lampami wiszącymi', 'spisesalen i beboerklubben, med taklamper i flettverk', 'matsalen i de boendes klubb, med taklampor i flätverk')
a(36, 'The club dining room', 'El comedor del club', 'La salle à manger du club', 'Der Speisesaal des Clubs', 'Обеденный зал клуба', 'صالة الطعام في النادي',
  'De eetzaal van de club', 'Jadalnia klubu', 'Spisesalen i klubben', 'Klubbens matsal')
cg(37, "Computer-generated view of the residents' club building",
   'el edificio del club de residentes sobre su césped y sus tumbonas', 'du bâtiment du club des résidents au-dessus de sa pelouse et de ses transats',
   'des Bewohnerclubs über seinem Rasen mit Liegen', 'здание клуба для жителей над газоном с шезлонгами',
   'لمبنى نادي السكان فوق العشب وكراسي الاستلقاء', 'het gebouw van de bewonersclub boven het gazon en de ligbedden',
   'budynek klubu mieszkańców nad trawnikiem z leżakami', 'beboerklubbens bygg over plenen og solsengene', 'klubbhuset för de boende ovanför gräsmattan och solsängarna')
cg(38, "Computer-generated view of the residents' club at dusk",
   'el club de residentes al atardecer, al otro lado de un amplio césped', 'du club des résidents au crépuscule, au-delà d’une vaste pelouse',
   'des Bewohnerclubs in der Abenddämmerung, jenseits einer weiten Rasenfläche', 'клуб для жителей в сумерках за широким газоном',
   'لنادي السكان عند الغسق عبر مرجة واسعة', 'de bewonersclub in de schemering, aan de overkant van een breed gazon',
   'klub mieszkańców o zmierzchu, za rozległym trawnikiem', 'beboerklubben i skumringen, på andre siden av en stor plen', 'de boendes klubb i skymningen, på andra sidan en stor gräsmatta')
a(39, 'The club at dusk', 'El club al atardecer', 'Le club au crépuscule', 'Der Club in der Dämmerung', 'Клуб в сумерках', 'النادي عند الغسق',
  'De club in de schemering', 'Klub o zmierzchu', 'Klubben i skumringen', 'Klubben i skymningen')

# ---- overview and residences
a(40, 'Nineteen homes, <em>two phases</em>',
  'Diecinueve viviendas, <em>dos fases</em>', 'Dix-neuf logements, <em>deux phases</em>', 'Neunzehn Wohnungen, <em>zwei Bauabschnitte</em>',
  'Девятнадцать квартир, <em>две очереди</em>', 'تسعة عشر مسكناً، <em>مرحلتان</em>', 'Negentien woningen, <em>twee fasen</em>',
  'Dziewiętnaście mieszkań, <em>dwa etapy</em>', 'Nitten boliger, <em>to byggetrinn</em>', 'Nitton bostäder, <em>två etapper</em>')
a(41, 'Torrevigía Residences is a gated scheme',
  'Torrevigía Residences es un conjunto cerrado de bloques de apartamentos en la ladera de Torrevigía, Estepona, junto a Selwo Aventura, construido en dos fases. El portal de agentes del promotor ofrece diecinueve viviendas, ocho en la primera fase y once en la segunda, todas llave en mano y de entrega inmediata.',
  'Torrevigía Residences est un ensemble fermé de blocs d’appartements à flanc de colline à Torrevigía, Estepona, à côté de Selwo Aventura, construit en deux phases. Le portail agents du promoteur propose dix-neuf logements, huit dans la première phase et onze dans la seconde, tous clés en main et livrables immédiatement.',
  'Torrevigía Residences ist eine geschlossene Wohnanlage aus Apartmentblöcken am Hang von Torrevigía, Estepona, neben Selwo Aventura, errichtet in zwei Bauabschnitten. Das Maklerportal des Bauträgers bietet neunzehn Wohnungen an, acht im ersten und elf im zweiten Bauabschnitt, alle schlüsselfertig und sofort übergabebereit.',
  'Torrevigía Residences — закрытый комплекс жилых корпусов на склоне в Торревихии, Эстепона, рядом с Selwo Aventura, построенный в две очереди. На портале застройщика для агентов в продаже девятнадцать квартир: восемь в первой очереди и одиннадцать во второй, все под ключ и с немедленной передачей.',
  'Torrevigía Residences مجمّع مسوَّر من مبانٍ سكنية على سفح التل في توريفيخيا، إستيبونا، بجوار Selwo Aventura، شُيّد على مرحلتين. تعرض بوابة الوكلاء لدى المطوّر تسعة عشر مسكناً للبيع، ثمانية في المرحلة الأولى وأحد عشر في الثانية، وكلها جاهزة بالكامل للتسليم الفوري.',
  'Torrevigía Residences is een afgesloten complex van appartementsblokken op de heuvel in Torrevigía, Estepona, naast Selwo Aventura, gebouwd in twee fasen. Het agentenportaal van de ontwikkelaar biedt negentien woningen aan, acht in de eerste fase en elf in de tweede, allemaal sleutelklaar en direct beschikbaar.',
  'Torrevigía Residences to zamknięte osiedle bloków mieszkalnych na zboczu w Torrevigía, Estepona, obok Selwo Aventura, zbudowane w dwóch etapach. Portal dewelopera dla agentów oferuje dziewiętnaście mieszkań, osiem w pierwszym etapie i jedenaście w drugim, wszystkie pod klucz i do natychmiastowego odbioru.',
  'Torrevigía Residences er et inngjerdet anlegg av leilighetsblokker i åssiden i Torrevigía, Estepona, ved Selwo Aventura, bygget i to byggetrinn. Utbyggerens meglerportal tilbyr nitten boliger, åtte i første byggetrinn og elleve i det andre, alle nøkkelferdige med umiddelbar overtakelse.',
  'Torrevigía Residences är ett inhägnat område med flerbostadshus i sluttningen i Torrevigía, Estepona, intill Selwo Aventura, byggt i två etapper. Exploatörens mäklarportal erbjuder nitton bostäder, åtta i den första etappen och elva i den andra, alla nyckelfärdiga med omedelbart tillträde.')
a(42, 'The available homes have two, three or four',
  'Las viviendas disponibles tienen dos, tres o cuatro dormitorios y dos o tres baños, y van de {N131.05} a {N196.08} {U} construidos, con un interior útil de {N103.73} a {N155.32} {U}. Todas las viviendas con plano tienen terraza, de {N33.10} a {N50.45} {U}, cubierta en planta baja y primera planta y en parte cubierta en la segunda.',
  'Les logements disponibles comptent deux, trois ou quatre chambres et deux ou trois salles de bains, et vont de {N131.05} à {N196.08} {U} construits, avec {N103.73} à {N155.32} {U} de surface utile intérieure. Chaque logement doté d’un plan a une terrasse, de {N33.10} à {N50.45} {U}, couverte au rez-de-chaussée et au premier étage et en partie couverte au deuxième.',
  'Die verfügbaren Wohnungen haben zwei, drei oder vier Schlafzimmer und zwei oder drei Bäder, bei {N131.05} bis {N196.08} {U} bebauter Fläche und {N103.73} bis {N155.32} {U} Wohnfläche. Jede Wohnung mit Grundriss hat eine Terrasse von {N33.10} bis {N50.45} {U}, im Erdgeschoss und im ersten Obergeschoss überdacht, im zweiten teilweise überdacht.',
  'В доступных квартирах две, три или четыре спальни и две или три ванные; площадь застройки от {N131.05} до {N196.08} {U}, полезная внутренняя площадь от {N103.73} до {N155.32} {U}. У каждой квартиры с планом есть терраса площадью от {N33.10} до {N50.45} {U}: на первом и втором этажах крытая, на третьем частично крытая.',
  'تضم المساكن المتاحة غرفتي نوم أو ثلاثاً أو أربعاً وحمّامين أو ثلاثة، وتتراوح مساحتها المبنية بين {N131.05} و{N196.08} {U} ومساحتها الداخلية الصافية بين {N103.73} و{N155.32} {U}. ولكل مسكن له مخطط تراس من {N33.10} إلى {N50.45} {U}، مسقوف في الطابقين الأرضي والأول ومسقوف جزئياً في الثاني.',
  'De beschikbare woningen hebben twee, drie of vier slaapkamers en twee of drie badkamers, en meten {N131.05} tot {N196.08} {U} bebouwd met {N103.73} tot {N155.32} {U} nuttige binnenoppervlakte. Elke woning met een plattegrond heeft een terras van {N33.10} tot {N50.45} {U}, overdekt op de begane grond en de eerste verdieping en deels overdekt op de tweede.',
  'Dostępne mieszkania mają dwie, trzy lub cztery sypialnie oraz dwie lub trzy łazienki, a ich powierzchnia zabudowy wynosi od {N131.05} do {N196.08} {U}, przy powierzchni użytkowej wnętrza od {N103.73} do {N155.32} {U}. Każde mieszkanie z rzutem ma taras od {N33.10} do {N50.45} {U}, zadaszony na parterze i pierwszym piętrze, a na drugim częściowo zadaszony.',
  'De tilgjengelige boligene har to, tre eller fire soverom og to eller tre bad, og måler {N131.05} til {N196.08} {U} bygget med {N103.73} til {N155.32} {U} nyttbart innvendig areal. Hver bolig med plantegning har en terrasse på {N33.10} til {N50.45} {U}, overbygd i første og andre etasje og delvis overbygd i tredje.',
  'De tillgängliga bostäderna har två, tre eller fyra sovrum och två eller tre badrum, och mäter {N131.05} till {N196.08} {U} byggyta med {N103.73} till {N155.32} {U} invändig nyttoyta. Varje bostad med planritning har en terrass på {N33.10} till {N50.45} {U}, övertäckt på bottenvåningen och första våningen och delvis övertäckt på andra.')
a(43, 'Within the scheme the brochure lists',
  'Dentro del conjunto, el folleto enumera una piscina, un espacio de coworking, jardines paisajísticos, aparcamiento para bicicletas, una entrada cerrada y videovigilancia perimetral. Los compradores también tienen acceso al club de residentes de la urbanización, con piscina interior climatizada, gimnasio, saunas y comedor.',
  'Au sein de l’ensemble, la brochure mentionne une piscine, un espace de coworking, des jardins paysagers, un local à vélos, une entrée fermée et une vidéosurveillance périmétrique. Les acquéreurs ont aussi accès au club des résidents du domaine, avec piscine intérieure chauffée, salle de sport, saunas et salle à manger.',
  'Innerhalb der Anlage nennt die Broschüre einen Pool, einen Coworking-Bereich, angelegte Gärten, Fahrradstellplätze, einen geschlossenen Zugang und Videoüberwachung entlang der Grundstücksgrenze. Käufer haben zudem Zugang zum Bewohnerclub des Gesamtareals mit beheiztem Hallenbad, Fitnessraum, Saunen und Speisesaal.',
  'На территории комплекса, по данным брошюры, есть бассейн, коворкинг, ландшафтные сады, велосипедная стоянка, въезд с воротами и видеонаблюдение по периметру. Покупатели также получают доступ в клуб для жителей всего жилого района с крытым подогреваемым бассейном, тренажёрным залом, саунами и обеденным залом.',
  'يذكر الكتيّب داخل المجمّع مسبحاً، ومساحة عمل مشتركة، وحدائق منسّقة، ومكاناً للدراجات، ومدخلاً مسوّراً، ومراقبة بالفيديو على المحيط. ويحق للمشترين أيضاً دخول نادي السكان في المنطقة السكنية الأوسع، بمسبح داخلي مدفأ وصالة رياضية وساونا وصالة طعام.',
  'Binnen het complex noemt de brochure een zwembad, een coworkingruimte, aangelegde tuinen, een fietsenstalling, een afgesloten toegang en camerabewaking langs de omheining. Kopers hebben daarnaast toegang tot de bewonersclub van het grotere domein, met een verwarmd binnenzwembad, een fitnessruimte, sauna’s en een eetzaal.',
  'Na terenie osiedla broszura wymienia basen, przestrzeń coworkingową, zagospodarowane ogrody, miejsce na rowery, ogrodzony wjazd i monitoring obwodowy. Kupujący mają też dostęp do klubu mieszkańców całego kompleksu, z krytym podgrzewanym basenem, siłownią, saunami i jadalnią.',
  'Innenfor anlegget nevner brosjyren et basseng, et coworking-område, opparbeidede hager, sykkelparkering, en inngjerdet inngang og videoovervåking langs gjerdet. Kjøperne har også tilgang til beboerklubben i det større området, med oppvarmet innendørsbasseng, treningsrom, badstuer og spisesal.',
  'Inom området nämner broschyren en pool, ett coworkingutrymme, anlagda trädgårdar, cykelförråd, en grindförsedd entré och kameraövervakning längs områdesgränsen. Köparna har också tillgång till de boendes klubb i det större området, med uppvärmd inomhuspool, gym, bastur och matsal.')
a(44, 'Fourteen of the nineteen homes',
  'Catorce de las diecinueve viviendas tienen tres dormitorios, una de ellas en la tercera planta; tres tienen cuatro dormitorios, y las dos de la segunda planta tienen dos. La tabla sigue la lista del promotor del 13 de noviembre de 2026.',
  'Quatorze des dix-neuf logements ont trois chambres, dont un au troisième étage ; trois en ont quatre, et les deux du deuxième étage en ont deux. Le tableau suit la liste du promoteur du 13 novembre 2026.',
  'Vierzehn der neunzehn Wohnungen haben drei Schlafzimmer, eine davon im dritten Obergeschoss; drei haben vier Schlafzimmer, und die beiden im zweiten Obergeschoss haben zwei. Die Tabelle folgt der Liste des Bauträgers vom 13. November 2026.',
  'В четырнадцати из девятнадцати квартир три спальни, одна из них на четвёртом этаже; в трёх — четыре спальни, а в двух квартирах на третьем этаже — две. Таблица ниже следует списку застройщика от 13 ноября 2026 года.',
  'أربعة عشر من المساكن التسعة عشر بثلاث غرف نوم، أحدها في الطابق الثالث؛ وثلاثة بأربع غرف، والمسكنان في الطابق الثاني بغرفتين. يتبع الجدول أدناه قائمة المطوّر الصادرة في 13 نوفمبر 2026.',
  'Veertien van de negentien woningen hebben drie slaapkamers, waarvan één op de derde verdieping; drie hebben er vier, en de twee op de tweede verdieping hebben er twee. De tabel hieronder volgt de lijst van de ontwikkelaar van 13 november 2026.',
  'Czternaście z dziewiętnastu mieszkań ma trzy sypialnie, w tym jedno na trzecim piętrze; trzy mają cztery sypialnie, a dwa na drugim piętrze mają dwie. Tabela poniżej odpowiada liście dewelopera z 13 listopada 2026 r.',
  'Fjorten av de nitten boligene har tre soverom, én av dem i fjerde etasje; tre har fire soverom, og de to i tredje etasje har to. Tabellen nedenfor følger utbyggerens liste av 13. november 2026.',
  'Fjorton av de nitton bostäderna har tre sovrum, varav en på tredje våningen; tre har fyra sovrum, och de två på andra våningen har två. Tabellen nedan följer exploatörens lista från den 13 november 2026.')
a(45, 'Three bedrooms', 'Tres dormitorios', 'Trois chambres', 'Drei Schlafzimmer', 'Три спальни', 'ثلاث غرف نوم', 'Drie slaapkamers', 'Trzy sypialnie', 'Tre soverom', 'Tre sovrum')
a(46, 'Fourteen homes of 153.46',
  'Catorce viviendas de {N153.46} a {N167.72} {U} construidos, con dos baños, el principal en suite.',
  'Quatorze logements de {N153.46} à {N167.72} {U} construits, avec deux salles de bains, dont la principale attenante à la chambre.',
  'Vierzehn Wohnungen mit {N153.46} bis {N167.72} {U} bebauter Fläche und zwei Bädern, das Hauptbad en suite.',
  'Четырнадцать квартир площадью застройки от {N153.46} до {N167.72} {U}, с двумя ванными, главная при спальне.',
  'أربعة عشر مسكناً من {N153.46} إلى {N167.72} {U} مبنية، بحمّامين، الرئيسي منهما ملحق بغرفة النوم.',
  'Veertien woningen van {N153.46} tot {N167.72} {U} bebouwd, met twee badkamers, de hoofdbadkamer en suite.',
  'Czternaście mieszkań o powierzchni zabudowy od {N153.46} do {N167.72} {U}, z dwiema łazienkami, główna przy sypialni.',
  'Fjorten boliger på {N153.46} til {N167.72} {U} bygget, med to bad, hovedbadet med eget soverom.',
  'Fjorton bostäder på {N153.46} till {N167.72} {U} byggyta, med två badrum, huvudbadrummet i anslutning till sovrummet.')
a(47, 'An open living room, dining area and kitchen of about 52',
  'Salón, comedor y cocina abiertos de unos 52 {U} en los planos, con salida a la terraza.',
  'Un séjour, un coin repas et une cuisine ouverts d’environ 52 {U} sur les plans, donnant sur la terrasse.',
  'Ein offener Wohn-, Ess- und Kochbereich von etwa 52 {U} laut Grundriss, mit Zugang zur Terrasse.',
  'Открытая гостиная, столовая и кухня площадью около 52 {U} по планам, с выходом на террасу.',
  'غرفة معيشة وطعام ومطبخ مفتوحة بمساحة نحو 52 {U} في المخططات، تنفتح على التراس.',
  'Een open woonkamer, eethoek en keuken van ongeveer 52 {U} op de plattegronden, met toegang tot het terras.',
  'Otwarty salon z jadalnią i kuchnią o powierzchni około 52 {U} według rzutów, z wyjściem na taras.',
  'Åpen stue, spisestue og kjøkken på omkring 52 {U} på plantegningene, med utgang til terrassen.',
  'Öppet vardagsrum, matplats och kök på omkring 52 {U} enligt planritningarna, med utgång till terrassen.')
a(48, 'On the ground and first floors, a covered terrace',
  'En planta baja y primera planta, una terraza cubierta de {N33.10} a {N37.45} {U} a lo largo de la fachada de la vivienda.',
  'Au rez-de-chaussée et au premier étage, une terrasse couverte de {N33.10} à {N37.45} {U} sur toute la façade du logement.',
  'Im Erdgeschoss und im ersten Obergeschoss eine überdachte Terrasse von {N33.10} bis {N37.45} {U} über die ganze Vorderseite der Wohnung.',
  'На первом и втором этажах — крытая терраса от {N33.10} до {N37.45} {U} вдоль всего фасада квартиры.',
  'في الطابقين الأرضي والأول، تراس مسقوف من {N33.10} إلى {N37.45} {U} على امتداد واجهة المسكن.',
  'Op de begane grond en de eerste verdieping een overdekt terras van {N33.10} tot {N37.45} {U} over de hele voorgevel van de woning.',
  'Na parterze i pierwszym piętrze zadaszony taras od {N33.10} do {N37.45} {U} wzdłuż całego frontu mieszkania.',
  'I første og andre etasje en overbygd terrasse på {N33.10} til {N37.45} {U} langs hele fronten av boligen.',
  'På bottenvåningen och första våningen en övertäckt terrass på {N33.10} till {N37.45} {U} längs hela bostadens framsida.')
a(49, 'Prices from EUR 638,000 to EUR 777,000',
  'Precios de {E638000} a {E777000}, y {E1762000} la única vivienda de la tercera planta.',
  'Prix de {E638000} à {E777000}, et {E1762000} pour l’unique logement du troisième étage.',
  'Preise von {E638000} bis {E777000}, und {E1762000} für die einzige Wohnung im dritten Obergeschoss.',
  'Цены от {E638000} до {E777000}, и {E1762000} за единственную квартиру на четвёртом этаже.',
  'الأسعار من {E638000} إلى {E777000}، و{E1762000} للمسكن الوحيد في الطابق الثالث.',
  'Prijzen van {E638000} tot {E777000}, en {E1762000} voor de enige woning op de derde verdieping.',
  'Ceny od {E638000} do {E777000} oraz {E1762000} za jedyne mieszkanie na trzecim piętrze.',
  'Priser fra {E638000} til {E777000}, og {E1762000} for den eneste boligen i fjerde etasje.',
  'Priser från {E638000} till {E777000}, och {E1762000} för den enda bostaden på tredje våningen.')
a(50, 'Four bedrooms', 'Cuatro dormitorios', 'Quatre chambres', 'Vier Schlafzimmer', 'Четыре спальни', 'أربع غرف نوم', 'Vier slaapkamers', 'Cztery sypialnie', 'Fire soverom', 'Fyra sovrum')
a(51, 'Three ground-floor homes of 196.08',
  'Tres viviendas en planta baja de {N196.08} {U} construidos y {N155.32} {U} útiles, con tres baños.',
  'Trois logements en rez-de-chaussée de {N196.08} {U} construits et {N155.32} {U} utiles, avec trois salles de bains.',
  'Drei Erdgeschosswohnungen mit {N196.08} {U} bebauter Fläche und {N155.32} {U} Wohnfläche, mit drei Bädern.',
  'Три квартиры на первом этаже: {N196.08} {U} застройки и {N155.32} {U} полезной площади, с тремя ванными.',
  'ثلاثة مساكن في الطابق الأرضي بمساحة {N196.08} {U} مبنية و{N155.32} {U} صافية، بثلاثة حمّامات.',
  'Drie woningen op de begane grond van {N196.08} {U} bebouwd en {N155.32} {U} nuttig, met drie badkamers.',
  'Trzy mieszkania na parterze o powierzchni zabudowy {N196.08} {U} i użytkowej {N155.32} {U}, z trzema łazienkami.',
  'Tre boliger i første etasje på {N196.08} {U} bygget og {N155.32} {U} nyttbart, med tre bad.',
  'Tre bostäder på bottenvåningen på {N196.08} {U} byggyta och {N155.32} {U} nyttoyta, med tre badrum.')
a(52, 'A living room, dining area and kitchen of 57.45',
  'Salón, comedor y cocina de {N57.45} {U} en los planos, y una terraza cubierta de {N45.35} {U}.',
  'Un séjour, un coin repas et une cuisine de {N57.45} {U} sur les plans, et une terrasse couverte de {N45.35} {U}.',
  'Ein Wohn-, Ess- und Kochbereich von {N57.45} {U} laut Grundriss und eine überdachte Terrasse von {N45.35} {U}.',
  'Гостиная, столовая и кухня площадью {N57.45} {U} по планам и крытая терраса {N45.35} {U}.',
  'غرفة معيشة وطعام ومطبخ بمساحة {N57.45} {U} في المخططات، وتراس مسقوف بمساحة {N45.35} {U}.',
  'Een woonkamer, eethoek en keuken van {N57.45} {U} op de plattegronden, en een overdekt terras van {N45.35} {U}.',
  'Salon z jadalnią i kuchnią o powierzchni {N57.45} {U} według rzutów oraz zadaszony taras {N45.35} {U}.',
  'Stue, spisestue og kjøkken på {N57.45} {U} på plantegningene, og en overbygd terrasse på {N45.35} {U}.',
  'Vardagsrum, matplats och kök på {N57.45} {U} enligt planritningarna, och en övertäckt terrass på {N45.35} {U}.')
a(53, 'Each comes with two parking spaces',
  'Cada una se vende con dos plazas de garaje y un trastero según la lista del promotor.',
  'Chacun est vendu avec deux places de parking et un cellier selon la liste du promoteur.',
  'Zu jeder gehören laut Liste des Bauträgers zwei Stellplätze und ein Abstellraum.',
  'По списку застройщика к каждой прилагаются два машино-места и кладовая.',
  'يُباع مع كل منها موقفان للسيارات ومخزن بحسب قائمة المطوّر.',
  'Bij elke woning horen volgens de lijst van de ontwikkelaar twee parkeerplaatsen en een berging.',
  'Do każdego według listy dewelopera należą dwa miejsca parkingowe i komórka lokatorska.',
  'Hver selges med to parkeringsplasser og en bod ifølge utbyggerens liste.',
  'Till varje bostad hör enligt exploatörens lista två parkeringsplatser och ett förråd.')
a(54, 'Prices from EUR 898,000 to EUR 900,000',
  'Precios de {E898000} a {E900000}.', 'Prix de {E898000} à {E900000}.', 'Preise von {E898000} bis {E900000}.', 'Цены от {E898000} до {E900000}.',
  'الأسعار من {E898000} إلى {E900000}.', 'Prijzen van {E898000} tot {E900000}.', 'Ceny od {E898000} do {E900000}.', 'Priser fra {E898000} til {E900000}.', 'Priser från {E898000} till {E900000}.')
a(55, 'Two second-floor homes of 131.05',
  'Dos viviendas en segunda planta de {N131.05} y {N137.21} {U} construidos, con dos baños.',
  'Deux logements au deuxième étage de {N131.05} et {N137.21} {U} construits, avec deux salles de bains.',
  'Zwei Wohnungen im zweiten Obergeschoss mit {N131.05} und {N137.21} {U} bebauter Fläche und zwei Bädern.',
  'Две квартиры на третьем этаже площадью застройки {N131.05} и {N137.21} {U}, с двумя ванными.',
  'مسكنان في الطابق الثاني بمساحة {N131.05} و{N137.21} {U} مبنية، بحمّامين.',
  'Twee woningen op de tweede verdieping van {N131.05} en {N137.21} {U} bebouwd, met twee badkamers.',
  'Dwa mieszkania na drugim piętrze o powierzchni zabudowy {N131.05} i {N137.21} {U}, z dwiema łazienkami.',
  'To boliger i tredje etasje på {N131.05} og {N137.21} {U} bygget, med to bad.',
  'Två bostäder på andra våningen på {N131.05} och {N137.21} {U} byggyta, med två badrum.')
a(56, 'A terrace of 49.15 and 50.45',
  'Una terraza de {N49.15} y {N50.45} {U} en los planos, en parte cubierta y en parte descubierta.',
  'Une terrasse de {N49.15} et {N50.45} {U} sur les plans, en partie couverte et en partie ouverte.',
  'Eine Terrasse von {N49.15} bzw. {N50.45} {U} laut Grundriss, teils überdacht und teils offen.',
  'Терраса {N49.15} и {N50.45} {U} по планам, частично крытая и частично открытая.',
  'تراس بمساحة {N49.15} و{N50.45} {U} في المخططات، جزء منه مسقوف وجزء مكشوف.',
  'Een terras van {N49.15} en {N50.45} {U} op de plattegronden, deels overdekt en deels open.',
  'Taras o powierzchni {N49.15} i {N50.45} {U} według rzutów, częściowo zadaszony i częściowo otwarty.',
  'En terrasse på {N49.15} og {N50.45} {U} på plantegningene, delvis overbygd og delvis åpen.',
  'En terrass på {N49.15} och {N50.45} {U} enligt planritningarna, delvis övertäckt och delvis öppen.')
a(57, 'Prices of EUR 761,000 and EUR 745,000',
  'Precios de {E761000} y {E745000}.', 'Prix de {E761000} et {E745000}.', 'Preise von {E761000} und {E745000}.', 'Цены {E761000} и {E745000}.',
  'السعران {E761000} و{E745000}.', 'Prijzen van {E761000} en {E745000}.', 'Ceny {E761000} i {E745000}.', 'Priser på {E761000} og {E745000}.', 'Priser på {E761000} och {E745000}.')

# ---- availability
a(58, '19 homes <em>available</em>',
  '19 viviendas <em>disponibles</em>', '19 logements <em>disponibles</em>', '19 Wohnungen <em>verfügbar</em>', '19 квартир <em>в продаже</em>',
  '19 مسكناً <em>متاحاً</em>', '19 woningen <em>beschikbaar</em>', '19 mieszkań <em>dostępnych</em>', '19 boliger <em>tilgjengelige</em>', '19 bostäder <em>tillgängliga</em>')
a(59, 'Eight homes in the first phase and eleven',
  'Ocho viviendas de la primera fase y once de la segunda figuran como disponibles, todas listas para entrar a vivir. Disponibilidad y precios según el portal de agentes del promotor a 13 de noviembre de 2026, que se reconfirman antes de la reserva.',
  'Huit logements de la première phase et onze de la seconde sont indiqués comme disponibles, tous prêts à habiter. Disponibilités et prix tels qu’affichés sur le portail agents du promoteur au 13 novembre 2026, reconfirmés avant toute réservation.',
  'Acht Wohnungen im ersten und elf im zweiten Bauabschnitt sind als verfügbar gelistet, alle bezugsfertig. Verfügbarkeit und Preise laut Maklerportal des Bauträgers vom 13. November 2026, vor der Reservierung erneut bestätigt.',
  'Восемь квартир первой очереди и одиннадцать второй указаны как доступные, все готовы к заселению. Наличие и цены — по данным портала застройщика для агентов на 13 ноября 2026 года, с повторным подтверждением перед бронированием.',
  'ثمانية مساكن من المرحلة الأولى وأحد عشر من الثانية مدرجة على أنها متاحة، وكلها جاهزة للسكن. التوفر والأسعار كما وردت في بوابة الوكلاء لدى المطوّر في 13 نوفمبر 2026، ويُعاد تأكيدها قبل الحجز.',
  'Acht woningen in de eerste fase en elf in de tweede staan als beschikbaar vermeld, allemaal klaar om in te trekken. Beschikbaarheid en prijzen volgens het agentenportaal van de ontwikkelaar op 13 november 2026, opnieuw bevestigd vóór reservering.',
  'Osiem mieszkań z pierwszego etapu i jedenaście z drugiego figuruje jako dostępne, wszystkie gotowe do zamieszkania. Dostępność i ceny według portalu dewelopera dla agentów z 13 listopada 2026 r., ponownie potwierdzane przed rezerwacją.',
  'Åtte boliger i første byggetrinn og elleve i det andre er oppført som tilgjengelige, alle klare til innflytting. Tilgjengelighet og priser slik de står i utbyggerens meglerportal 13. november 2026, bekreftet på nytt før reservasjon.',
  'Åtta bostäder i den första etappen och elva i den andra står som tillgängliga, alla inflyttningsklara. Tillgänglighet och priser enligt exploatörens mäklarportal den 13 november 2026, bekräftade på nytt före bokning.')
a(60, 'Prices, bedrooms, bathrooms and built and usable areas',
  'Los precios, dormitorios, baños y superficies construidas y útiles se han transcrito de la lista del portal de agentes del promotor del 13 de noviembre de 2026; las terrazas se leen en los planos de las viviendas del promotor (V1, junio de 2023), porque la lista no da ninguna para las viviendas de planta baja y segunda planta y da {N33.08} {U} donde el plano indica {N33.10} {U}. Los planos expresan las superficies de otro modo que la lista: para la vivienda de tres dormitorios más habitual, la lista da {N153.46} {U} construidos y {N122.14} {U} útiles, mientras que el plano da {N121.95} {U} útiles interiores, {N167.20} {U} construidos según el Decreto 218/2005 y {N191.36} {U} construidos con la parte proporcional de zonas comunes. La vivienda 6-9-03-A de la tercera planta, de {E1762000}, no tiene plano en los documentos de que disponemos y su terraza no consta; pedimos su plano antes de cualquier visita. Cada precio corresponde solo a la vivienda: la lista vende una plaza de garaje y un trastero con la mayoría de las viviendas, que suman {E22000}, y dos plazas y un trastero con 3-4-0-B, 3-5-02-B, 6-9-03-A, 6-10-0-B y 7-12-0-B, que suman {E38000}. Los precios no incluyen el IVA ni los gastos de compra. El portal advierte que su lista es meramente informativa y que precios y viviendas están sujetos a disponibilidad; Nueva Living reconfirma precio, estado y condiciones antes de cualquier reserva.',
  'Les prix, chambres, salles de bains et surfaces construites et utiles sont transcrits de la liste du portail agents du promoteur du 13 novembre 2026 ; les terrasses sont lues sur les plans des logements du promoteur (V1, juin 2023), car la liste n’en donne aucune pour les logements du rez-de-chaussée et du deuxième étage et indique {N33.08} {U} là où le plan porte {N33.10} {U}. Les plans expriment les surfaces autrement que la liste : pour le logement de trois chambres le plus courant, la liste donne {N153.46} {U} construits et {N122.14} {U} utiles, tandis que le plan donne {N121.95} {U} de surface utile intérieure, {N167.20} {U} construits au sens du décret 218/2005 et {N191.36} {U} construits avec la quote-part des parties communes. Le logement 6-9-03-A du troisième étage, à {E1762000}, n’a pas de plan dans les documents dont nous disposons et sa terrasse n’est pas indiquée ; nous demandons son plan avant toute visite. Chaque prix s’entend pour le logement seul : la liste vend une place de parking et un cellier avec la plupart des logements, pour {E22000} de plus, et deux places et un cellier avec 3-4-0-B, 3-5-02-B, 6-9-03-A, 6-10-0-B et 7-12-0-B, pour {E38000} de plus. Les prix s’entendent hors TVA et hors frais d’acquisition. Le portail précise que sa liste est purement informative et que les prix et les logements sont soumis à disponibilité ; Nueva Living reconfirme le prix, le statut et les conditions avant toute réservation.',
  'Preise, Schlafzimmer, Bäder sowie bebaute Fläche und Wohnfläche sind der Liste im Maklerportal des Bauträgers vom 13. November 2026 entnommen; die Terrassen stammen aus den Wohnungsgrundrissen des Bauträgers (V1, Juni 2023), weil die Liste für die Wohnungen im Erdgeschoss und im zweiten Obergeschoss keine angibt und {N33.08} {U} nennt, wo der Grundriss {N33.10} {U} zeigt. Die Grundrisse weisen die Flächen anders aus als die Liste: Für die häufigste Dreizimmerwohnung nennt die Liste {N153.46} {U} bebaut und {N122.14} {U} Wohnfläche, der Grundriss dagegen {N121.95} {U} Innenwohnfläche, {N167.20} {U} bebaut nach Dekret 218/2005 und {N191.36} {U} bebaut einschließlich des Anteils an den Gemeinschaftsflächen. Für die Wohnung 6-9-03-A im dritten Obergeschoss zu {E1762000} liegt uns kein Grundriss vor, und ihre Terrasse ist nicht angegeben; wir fordern den Grundriss vor jeder Besichtigung an. Jeder Preis gilt für die Wohnung allein: Die Liste verkauft mit den meisten Wohnungen einen Stellplatz und einen Abstellraum für zusätzlich {E22000}, mit 3-4-0-B, 3-5-02-B, 6-9-03-A, 6-10-0-B und 7-12-0-B zwei Stellplätze und einen Abstellraum für zusätzlich {E38000}. Die Preise verstehen sich zuzüglich MwSt. und Erwerbsnebenkosten. Das Portal weist darauf hin, dass seine Liste nur der Information dient und Preise und Wohnungen der Verfügbarkeit unterliegen; Nueva Living bestätigt Preis, Status und Konditionen erneut vor jeder Reservierung.',
  'Цены, количество спален и ванных, площади застройки и полезные площади взяты из списка на портале застройщика для агентов от 13 ноября 2026 года; террасы указаны по планам квартир застройщика (V1, июнь 2023 года), так как список не приводит их для квартир первого и третьего этажей и даёт {N33.08} {U} там, где на плане {N33.10} {U}. Планы указывают площади иначе, чем список: для самой распространённой квартиры с тремя спальнями список даёт {N153.46} {U} застройки и {N122.14} {U} полезной площади, а план — {N121.95} {U} полезной внутренней площади, {N167.20} {U} застройки по декрету 218/2005 и {N191.36} {U} застройки с долей общих зон. Для квартиры 6-9-03-A на четвёртом этаже стоимостью {E1762000} в имеющихся у нас документах нет плана, а её терраса не указана; мы запрашиваем план до любого просмотра. Каждая цена — только за квартиру: по списку с большинством квартир продаются машино-место и кладовая за дополнительные {E22000}, а с 3-4-0-B, 3-5-02-B, 6-9-03-A, 6-10-0-B и 7-12-0-B — два машино-места и кладовая за дополнительные {E38000}. Цены указаны без НДС и расходов на оформление. Портал оговаривает, что его список носит лишь информационный характер, а цены и квартиры зависят от наличия; Nueva Living заново подтверждает цену, статус и условия перед любым бронированием.',
  'الأسعار وعدد غرف النوم والحمّامات والمساحات المبنية والصافية منقولة من قائمة بوابة الوكلاء لدى المطوّر بتاريخ 13 نوفمبر 2026؛ أما التراسات فمأخوذة من مخططات المساكن لدى المطوّر (V1، يونيو 2023)، لأن القائمة لا تذكر أي تراس لمساكن الطابقين الأرضي والثاني، وتذكر {N33.08} {U} حيث يذكر المخطط {N33.10} {U}. تعرض المخططات المساحات بطريقة تختلف عن القائمة: ففي المسكن الأكثر شيوعاً بثلاث غرف نوم تذكر القائمة {N153.46} {U} مبنية و{N122.14} {U} صافية، بينما يذكر المخطط {N121.95} {U} مساحة داخلية صافية، و{N167.20} {U} مبنية وفق المرسوم 218/2005، و{N191.36} {U} مبنية مع حصة المناطق المشتركة. لا يوجد مخطط للمسكن 6-9-03-A في الطابق الثالث، بسعر {E1762000}، ضمن المستندات التي لدينا، ولا تُذكر مساحة تراسه؛ ونطلب مخططه قبل أي معاينة. كل سعر للمسكن وحده: تبيع القائمة مع معظم المساكن موقف سيارة ومخزناً بإضافة {E22000}، ومع 3-4-0-B و3-5-02-B و6-9-03-A و6-10-0-B و7-12-0-B موقفين ومخزناً بإضافة {E38000}. الأسعار لا تشمل ضريبة القيمة المضافة ولا مصاريف الشراء. وتنبّه البوابة إلى أن قائمتها للعلم فقط وأن الأسعار والمساكن رهن التوفر؛ وتعيد Nueva Living تأكيد السعر والحالة والشروط قبل أي حجز.',
  'Prijzen, slaapkamers, badkamers en bebouwde en nuttige oppervlaktes zijn overgenomen uit de lijst op het agentenportaal van de ontwikkelaar van 13 november 2026; de terrassen komen van de woningplattegronden van de ontwikkelaar (V1, juni 2023), omdat de lijst er geen geeft voor de woningen op de begane grond en de tweede verdieping en {N33.08} {U} noemt waar de plattegrond {N33.10} {U} aangeeft. De plattegronden geven de oppervlaktes anders weer dan de lijst: voor de meest voorkomende driekamerwoning noemt de lijst {N153.46} {U} bebouwd en {N122.14} {U} nuttig, terwijl de plattegrond {N121.95} {U} nuttige binnenoppervlakte geeft, {N167.20} {U} bebouwd volgens decreet 218/2005 en {N191.36} {U} bebouwd inclusief het aandeel in de gemeenschappelijke ruimten. Woning 6-9-03-A op de derde verdieping, van {E1762000}, heeft geen plattegrond in de documenten die wij hebben en het terras ervan is niet vermeld; wij vragen de plattegrond op vóór elke bezichtiging. Elke prijs geldt voor de woning alleen: de lijst verkoopt bij de meeste woningen een parkeerplaats en een berging voor {E22000} extra, en bij 3-4-0-B, 3-5-02-B, 6-9-03-A, 6-10-0-B en 7-12-0-B twee parkeerplaatsen en een berging voor {E38000} extra. De prijzen zijn exclusief btw en aankoopkosten. Het portaal vermeldt dat de lijst alleen ter informatie dient en dat prijzen en woningen onder voorbehoud van beschikbaarheid zijn; Nueva Living bevestigt prijs, status en voorwaarden opnieuw vóór elke reservering.',
  'Ceny, liczba sypialni i łazienek oraz powierzchnie zabudowy i użytkowe zostały przepisane z listy na portalu dewelopera dla agentów z 13 listopada 2026 r.; tarasy odczytano z rzutów mieszkań dewelopera (V1, czerwiec 2023 r.), ponieważ lista nie podaje ich dla mieszkań na parterze i drugim piętrze, a tam, gdzie rzut wskazuje {N33.10} {U}, podaje {N33.08} {U}. Rzuty podają powierzchnie inaczej niż lista: dla najczęstszego mieszkania z trzema sypialniami lista podaje {N153.46} {U} zabudowy i {N122.14} {U} użytkowej, a rzut {N121.95} {U} powierzchni użytkowej wnętrza, {N167.20} {U} zabudowy według dekretu 218/2005 i {N191.36} {U} zabudowy z udziałem w częściach wspólnych. Dla mieszkania 6-9-03-A na trzecim piętrze, za {E1762000}, nie ma rzutu w posiadanych przez nas dokumentach, a jego taras nie jest podany; prosimy o rzut przed każdą wizytą. Każda cena dotyczy samego mieszkania: lista sprzedaje z większością mieszkań miejsce parkingowe i komórkę lokatorską za dodatkowe {E22000}, a z 3-4-0-B, 3-5-02-B, 6-9-03-A, 6-10-0-B i 7-12-0-B dwa miejsca i komórkę za dodatkowe {E38000}. Ceny nie zawierają podatku VAT ani kosztów nabycia. Portal zastrzega, że jego lista ma charakter wyłącznie informacyjny, a ceny i mieszkania zależą od dostępności; Nueva Living ponownie potwierdza cenę, status i warunki przed każdą rezerwacją.',
  'Priser, soverom, bad og bygget og nyttbart areal er hentet fra listen i utbyggerens meglerportal av 13. november 2026; terrassene er lest av utbyggerens plantegninger av boligene (V1, juni 2023), fordi listen ikke oppgir noen for boligene i første og tredje etasje og oppgir {N33.08} {U} der plantegningen viser {N33.10} {U}. Plantegningene oppgir arealene annerledes enn listen: for den vanligste treromsboligen gir listen {N153.46} {U} bygget og {N122.14} {U} nyttbart, mens plantegningen gir {N121.95} {U} nyttbart innvendig areal, {N167.20} {U} bygget etter dekret 218/2005 og {N191.36} {U} bygget inkludert andel av fellesarealene. Bolig 6-9-03-A i fjerde etasje, til {E1762000}, har ingen plantegning i dokumentene vi har, og terrassen er ikke oppgitt; vi ber om plantegningen før enhver visning. Hver pris gjelder boligen alene: listen selger en parkeringsplass og en bod med de fleste boligene for {E22000} ekstra, og to plasser og en bod med 3-4-0-B, 3-5-02-B, 6-9-03-A, 6-10-0-B og 7-12-0-B for {E38000} ekstra. Prisene er eksklusive mva og kjøpsomkostninger. Portalen opplyser at listen kun er til informasjon, og at priser og boliger er avhengige av tilgjengelighet; Nueva Living bekrefter pris, status og vilkår på nytt før enhver reservasjon.',
  'Priser, sovrum, badrum samt byggyta och nyttoyta är hämtade ur listan i exploatörens mäklarportal från den 13 november 2026; terrasserna är avlästa på exploatörens planritningar av bostäderna (V1, juni 2023), eftersom listan inte anger någon för bostäderna på bottenvåningen och andra våningen och anger {N33.08} {U} där planritningen visar {N33.10} {U}. Planritningarna redovisar ytorna på ett annat sätt än listan: för den vanligaste bostaden med tre sovrum anger listan {N153.46} {U} byggyta och {N122.14} {U} nyttoyta, medan planritningen anger {N121.95} {U} invändig nyttoyta, {N167.20} {U} byggyta enligt dekret 218/2005 och {N191.36} {U} byggyta inklusive andel av de gemensamma ytorna. Bostad 6-9-03-A på tredje våningen, för {E1762000}, har ingen planritning i de handlingar vi har och dess terrass anges inte; vi begär planritningen före varje visning. Varje pris gäller bostaden ensam: listan säljer en parkeringsplats och ett förråd med de flesta bostäderna för {E22000} extra, och två platser och ett förråd med 3-4-0-B, 3-5-02-B, 6-9-03-A, 6-10-0-B och 7-12-0-B för {E38000} extra. Priserna är exklusive IVA (spansk moms) och köpkostnader. Portalen anger att listan endast är informativ och att priser och bostäder gäller i mån av tillgång; Nueva Living bekräftar pris, status och villkor på nytt före varje bokning.')

# ---- quality specification
a(97, 'The developer’s own specification, from its brochure',
  'La memoria de calidades del propio promotor, tomada de su folleto y resumida por partes de la vivienda.',
  'Le descriptif du promoteur lui-même, tiré de sa brochure et résumé par partie du logement.',
  'Die eigene Baubeschreibung des Bauträgers aus seiner Broschüre, nach Bereichen der Wohnung zusammengefasst.',
  'Собственная спецификация застройщика из его брошюры, кратко по частям квартиры.',
  'مواصفات المطوّر نفسه من كتيّبه، ملخّصة حسب أجزاء المسكن.',
  'De eigen technische omschrijving van de ontwikkelaar uit zijn brochure, samengevat per onderdeel van de woning.',
  'Własna specyfikacja dewelopera z jego broszury, streszczona według części mieszkania.',
  'Utbyggerens egen beskrivelse fra brosjyren, oppsummert etter del av boligen.',
  'Exploatörens egen byggbeskrivning ur broschyren, sammanfattad efter del av bostaden.')
a(98, 'Source: the building specifications in the developer',
  'Fuente: la memoria de calidades del folleto del promotor, redactada antes de terminar la obra. Nueva Living confirma lo instalado en la vivienda que usted elija antes de cualquier reserva.',
  'Source : le descriptif de construction figurant dans la brochure du promoteur, rédigé avant l’achèvement. Nueva Living confirme ce qui a été installé dans le logement que vous choisissez avant toute réservation.',
  'Quelle: die Baubeschreibung in der Broschüre des Bauträgers, verfasst vor der Fertigstellung. Nueva Living bestätigt vor jeder Reservierung, was in der von Ihnen gewählten Wohnung tatsächlich verbaut wurde.',
  'Источник: строительная спецификация в брошюре застройщика, составленная до завершения строительства. Nueva Living подтверждает, что именно установлено в выбранной вами квартире, перед любым бронированием.',
  'المصدر: مواصفات البناء في كتيّب المطوّر، المكتوبة قبل اكتمال البناء. تؤكد Nueva Living ما رُكّب فعلاً في المسكن الذي تختارونه قبل أي حجز.',
  'Bron: de bouwomschrijving in de brochure van de ontwikkelaar, opgesteld vóór de oplevering. Nueva Living bevestigt vóór elke reservering wat er in de woning van uw keuze is aangebracht.',
  'Źródło: specyfikacja budowlana w broszurze dewelopera, sporządzona przed ukończeniem budowy. Nueva Living przed każdą rezerwacją potwierdza, co zostało zamontowane w wybranym przez Państwa mieszkaniu.',
  'Kilde: byggebeskrivelsen i utbyggerens brosjyre, skrevet før ferdigstillelse. Nueva Living bekrefter hva som er installert i den boligen De velger, før enhver reservasjon.',
  'Källa: byggbeskrivningen i exploatörens broschyr, skriven före färdigställandet. Nueva Living bekräftar vad som har installerats i den bostad ni väljer före varje bokning.')
a(99, 'Porcelain stoneware floors in the hall',
  'Suelos de gres porcelánico en vestíbulo, salón, dormitorios y cocina, con rodapié blanco.',
  'Sols en grès cérame dans l’entrée, le séjour, les chambres et la cuisine, avec plinthes blanches.',
  'Feinsteinzeugböden in Diele, Wohnzimmer, Schlafzimmern und Küche, mit weißen Sockelleisten.',
  'Полы из керамогранита в прихожей, гостиной, спальнях и на кухне, с белыми плинтусами.',
  'أرضيات من البورسلين في المدخل وغرفة المعيشة وغرف النوم والمطبخ، مع وزرات بيضاء.',
  'Vloeren van keramisch graniet in de hal, de woonkamer, de slaapkamers en de keuken, met witte plinten.',
  'Podłogi z gresu porcelanowego w przedpokoju, salonie, sypialniach i kuchni, z białymi listwami przypodłogowymi.',
  'Gulv av porselensfliser i entré, stue, soverom og kjøkken, med hvite gulvlister.',
  'Golv av porslinsklinker i hall, vardagsrum, sovrum och kök, med vita golvlister.')
a(100, 'Suspended ceilings throughout',
  'Falsos techos en toda la vivienda, acabados en pintura plástica.', 'Faux plafonds dans tout le logement, finis en peinture mate.',
  'Abgehängte Decken in der ganzen Wohnung, mit Dispersionsfarbe gestrichen.', 'Подвесные потолки по всей квартире, окрашенные водоэмульсионной краской.',
  'أسقف معلّقة في كامل المسكن، مطلية بطلاء مستحلب.', 'Verlaagde plafonds in de hele woning, afgewerkt met latexverf.',
  'Sufity podwieszane w całym mieszkaniu, wykończone farbą emulsyjną.', 'Nedsenkede himlinger i hele boligen, malt med plastmaling.', 'Undertak i hela bostaden, målade med plastfärg.')
a(101, 'Hot-water underfloor heating',
  'Suelo radiante por agua caliente, eléctrico en los baños, con termostato en las estancias principales.',
  'Plancher chauffant à eau chaude, électrique dans les salles de bains, avec thermostat dans les pièces principales.',
  'Warmwasser-Fußbodenheizung, in den Bädern elektrisch, mit Thermostat in den Haupträumen.',
  'Водяной тёплый пол, в ванных электрический, с термостатом в основных комнатах.',
  'تدفئة أرضية بالماء الساخن، كهربائية في الحمّامات، مع منظّم حرارة في الغرف الرئيسية.',
  'Vloerverwarming op warm water, elektrisch in de badkamers, met een thermostaat in de hoofdvertrekken.',
  'Wodne ogrzewanie podłogowe, w łazienkach elektryczne, z termostatem w głównych pomieszczeniach.',
  'Vannbåren gulvvarme, elektrisk på badene, med termostat i hovedrommene.',
  'Vattenburen golvvärme, elektrisk i badrummen, med termostat i huvudrummen.')
a(102, 'Ducted cooling to the living room',
  'Refrigeración por conductos en salón y dormitorios, y bomba de calor aerotérmica para el agua caliente.',
  'Rafraîchissement gainable dans le séjour et les chambres, et pompe à chaleur aérothermique pour l’eau chaude.',
  'Kanalgeführte Kühlung in Wohnzimmer und Schlafzimmern sowie eine Luft-Wasser-Wärmepumpe für das Warmwasser.',
  'Канальное охлаждение в гостиной и спальнях и аэротермальный тепловой насос для горячей воды.',
  'تبريد عبر مجارٍ في غرفة المعيشة وغرف النوم، ومضخة حرارية هوائية لتسخين المياه.',
  'Koeling via kanalen in de woonkamer en de slaapkamers, en een luchtwarmtepomp voor warm water.',
  'Chłodzenie kanałowe w salonie i sypialniach oraz aerotermiczna pompa ciepła do ciepłej wody.',
  'Kanalbasert kjøling i stue og soverom, og en luft-til-vann-varmepumpe for varmtvann.',
  'Kanaliserad kyla i vardagsrum och sovrum, och en luft-vattenvärmepump för varmvatten.')
a(103, 'Fitted wall and base units',
  'Muebles altos y bajos, con placa vitrocerámica en isla o península y campana extractora de techo.',
  'Meubles hauts et bas, avec plaque vitrocéramique sur îlot ou péninsule et hotte de plafond.',
  'Ober- und Unterschränke, mit Glaskeramik-Kochfeld auf Insel oder Halbinsel und Deckenabzugshaube.',
  'Навесные и напольные шкафы, стеклокерамическая варочная панель на острове или полуострове и потолочная вытяжка.',
  'خزائن علوية وسفلية، مع موقد زجاجي خزفي على جزيرة أو شبه جزيرة وشفاط سقفي.',
  'Boven- en onderkasten, met een keramische kookplaat op een eiland of schiereiland en een plafondafzuigkap.',
  'Szafki górne i dolne, z płytą ceramiczną na wyspie lub półwyspie i okapem sufitowym.',
  'Over- og underskap, med keramisk koketopp på øy eller halvøy og takmontert ventilator.',
  'Över- och underskåp, med glaskeramikhäll på köksö eller halvö och takmonterad köksfläkt.')
a(104, 'An oven and microwave column',
  'Columna de horno y microondas, lavavajillas y frigorífico panelados, y lavadora-secadora.',
  'Une colonne four et micro-ondes, un lave-vaisselle et un réfrigérateur habillés, et un lave-linge séchant.',
  'Ein Hochschrank mit Backofen und Mikrowelle, integrierter Geschirrspüler und Kühlschrank sowie ein Waschtrockner.',
  'Колонна с духовкой и микроволновой печью, встроенные посудомоечная машина и холодильник, стирально-сушильная машина.',
  'عمود للفرن والميكروويف، وغسّالة صحون وثلاجة مدمجتان بواجهات، وغسّالة مجفّفة.',
  'Een ovenkolom met magnetron, een ingebouwde vaatwasser en koelkast, en een was-droogcombinatie.',
  'Słupek z piekarnikiem i mikrofalówką, zabudowane zmywarka i lodówka oraz pralko-suszarka.',
  'En ovnskolonne med mikrobølgeovn, integrert oppvaskmaskin og kjøleskap, og en kombinert vaske- og tørkemaskin.',
  'Ett ugnsskåp med mikrovågsugn, integrerad diskmaskin och kylskåp samt en kombinerad tvättmaskin och torktumlare.')
a(105, 'Ceramic wall tiles, porcelain floors',
  'Revestimiento cerámico en paredes, suelos porcelánicos, platos de ducha de resina y mamparas.',
  'Faïence murale, sols en grès cérame, receveurs de douche en résine et parois de douche.',
  'Keramische Wandfliesen, Feinsteinzeugböden, Duschwannen aus Mineralguss und Duschabtrennungen.',
  'Керамическая плитка на стенах, полы из керамогранита, душевые поддоны из смолы и душевые перегородки.',
  'جدران مكسوّة بالسيراميك، وأرضيات من البورسلين، وقواعد دش من الراتنج، وحواجز دش.',
  'Keramische wandtegels, vloeren van keramisch graniet, douchebakken van kunsthars en douchewanden.',
  'Ceramiczne płytki ścienne, podłogi z gresu porcelanowego, brodziki z żywicy i kabiny prysznicowe.',
  'Keramiske veggfliser, gulv av porselensfliser, dusjkar i støpemarmor og dusjvegger.',
  'Keramiska väggplattor, golv av porslinsklinker, duschkar av gjutmarmor och duschväggar.')
a(106, 'In the main bathroom a thermostatic shower',
  'En el baño principal, ducha termostática, mueble de lavabo con encimera de cuarzo compacto e inodoro suspendido.',
  'Dans la salle de bains principale, une douche thermostatique, un meuble vasque avec plan en quartz compact et un WC suspendu.',
  'Im Hauptbad eine Thermostatdusche, ein Waschtischunterschrank mit Quarzkompositplatte und ein wandhängendes WC.',
  'В главной ванной — термостатический душ, тумба с раковиной и столешницей из кварцевого композита и подвесной унитаз.',
  'في الحمّام الرئيسي: دش بمنظّم حرارة، وخزانة مغسلة بسطح من الكوارتز المضغوط، ومرحاض معلّق.',
  'In de hoofdbadkamer een thermostatische douche, een wastafelmeubel met een blad van composietkwarts en een hangtoilet.',
  'W łazience głównej prysznic z termostatem, szafka umywalkowa z blatem z kompaktowego kwarcu i podwieszana toaleta.',
  'På hovedbadet en termostatstyrt dusj, et servantskap med benkeplate i kompakt kvarts og et vegghengt toalett.',
  'I huvudbadrummet en termostatstyrd dusch, ett tvättställsskåp med skiva i kompakt kvarts och en vägghängd toalett.')
a(107, 'Thermally broken aluminium windows',
  'Carpintería de aluminio con rotura de puente térmico y doble acristalamiento, y persianas motorizadas aisladas en los dormitorios.',
  'Menuiseries en aluminium à rupture de pont thermique avec double vitrage, et volets roulants motorisés isolés dans les chambres.',
  'Aluminiumfenster mit thermischer Trennung und Doppelverglasung sowie motorisierte, gedämmte Rollläden in den Schlafzimmern.',
  'Алюминиевые окна с терморазрывом и двойным остеклением, моторизованные утеплённые рольставни в спальнях.',
  'نوافذ ألومنيوم بعازل حراري وزجاج مزدوج، وستائر دوّارة آلية معزولة في غرف النوم.',
  'Aluminium ramen met thermische onderbreking en dubbele beglazing, en gemotoriseerde geïsoleerde rolluiken in de slaapkamers.',
  'Okna aluminiowe z przekładką termiczną i podwójnymi szybami oraz zmotoryzowane, ocieplane rolety w sypialniach.',
  'Aluminiumsvinduer med kuldebrobryter og doble glass, og motoriserte, isolerte rullegardiner på soverommene.',
  'Aluminiumfönster med köldbryggsbrytning och tvåglas, och motoriserade isolerade rullgardiner i sovrummen.')
a(108, 'An armoured front door',
  'Puerta de entrada blindada, puertas interiores lacadas en blanco de 220 cm de altura y armarios empotrados.',
  'Une porte d’entrée blindée, des portes intérieures laquées blanc de 220 cm de haut et des placards intégrés.',
  'Eine Sicherheitseingangstür, weiß lackierte Innentüren von 220 cm Höhe und Einbauschränke.',
  'Бронированная входная дверь, белые лакированные межкомнатные двери высотой 220 см и встроенные шкафы.',
  'باب مدخل مصفّح، وأبواب داخلية مطلية بالأبيض بارتفاع 220 سم، وخزائن مدمجة.',
  'Een gepantserde voordeur, wit gelakte binnendeuren van 220 cm hoog en inbouwkasten.',
  'Antywłamaniowe drzwi wejściowe, białe lakierowane drzwi wewnętrzne o wysokości 220 cm i szafy wnękowe.',
  'Sikkerhetsdør i inngangen, hvitlakkerte innerdører på 220 cm og innebygde garderobeskap.',
  'Säkerhetsdörr vid entrén, vitlackerade innerdörrar på 220 cm och inbyggda garderober.')
a(109, 'Non-slip stoneware paving',
  'Pavimento de gres antideslizante, con toma de agua, desagüe, iluminación, enchufe y toma de televisión en todas las terrazas.',
  'Revêtement en grès antidérapant, avec point d’eau, évacuation, éclairage, prise électrique et prise TV sur chaque terrasse.',
  'Rutschfester Steinzeugbelag, mit Wasseranschluss, Ablauf, Beleuchtung, Steckdose und TV-Anschluss auf jeder Terrasse.',
  'Нескользящее покрытие из керамики, на каждой террасе — водоразборный кран, водосток, освещение, розетка и ТВ-розетка.',
  'أرضية من الخزف المقاوم للانزلاق، مع نقطة مياه وتصريف وإنارة ومقبس كهربائي ومقبس تلفاز في كل تراس.',
  'Antislip tegelvloer, met een waterpunt, afvoer, verlichting, een stopcontact en een tv-aansluiting op elk terras.',
  'Antypoślizgowa okładzina z gresu, z punktem poboru wody, odpływem, oświetleniem, gniazdkiem i gniazdem TV na każdym tarasie.',
  'Sklisikre fliser, med vannuttak, avløp, belysning, stikkontakt og TV-uttak på hver terrasse.',
  'Halksäkra klinkers, med vattenutkastare, avlopp, belysning, eluttag och tv-uttag på varje terrass.')

# ---- why, investment, trust
a(110, 'Nineteen finished apartments in two phases',
  'Diecinueve apartamentos terminados en dos fases de un mismo conjunto cerrado, listos para entrar a vivir.',
  'Dix-neuf appartements achevés dans deux phases d’un même ensemble fermé, prêts à habiter.',
  'Neunzehn fertiggestellte Wohnungen in zwei Bauabschnitten einer geschlossenen Anlage, bezugsfertig gelistet.',
  'Девятнадцать готовых квартир в двух очередях одного закрытого комплекса, готовых к заселению.',
  'تسع عشرة شقة مكتملة في مرحلتين من مجمّع مسوَّر واحد، مدرجة على أنها جاهزة للسكن.',
  'Negentien opgeleverde appartementen in twee fasen van één afgesloten complex, klaar om in te trekken.',
  'Dziewiętnaście ukończonych mieszkań w dwóch etapach jednego zamkniętego osiedla, gotowych do zamieszkania.',
  'Nitten ferdigstilte leiligheter i to byggetrinn av ett inngjerdet anlegg, klare til innflytting.',
  'Nitton färdiga lägenheter i två etapper av ett inhägnat område, inflyttningsklara.')
a(111, 'Buyers who want a large home',
  'Compradores que quieren una vivienda amplia con terraza cubierta ya, sin esperar a una obra.',
  'Les acquéreurs qui veulent un grand logement avec terrasse couverte dès maintenant, sans attendre un chantier.',
  'Käufer, die jetzt eine großzügige Wohnung mit überdachter Terrasse möchten, statt auf einen Neubau zu warten.',
  'Покупателям, которым нужна просторная квартира с крытой террасой сейчас, а не после стройки.',
  'للمشترين الذين يريدون مسكناً واسعاً بتراس مسقوف الآن، بدلاً من انتظار البناء.',
  'Kopers die nu een ruime woning met een overdekt terras willen, in plaats van op een bouw te wachten.',
  'Kupujący, którzy chcą przestronnego mieszkania z zadaszonym tarasem od razu, zamiast czekać na budowę.',
  'Kjøpere som vil ha en romslig bolig med overbygd terrasse nå, i stedet for å vente på et byggeprosjekt.',
  'Köpare som vill ha en rymlig bostad med övertäckt terrass nu, i stället för att vänta på ett bygge.')
a(112, 'Most homes have three bedrooms and more than 150',
  'La mayoría de las viviendas tienen tres dormitorios y más de 150 {U} construidos, y los compradores tienen acceso a un club de residentes con piscina interior climatizada y gimnasio.',
  'La plupart des logements ont trois chambres et plus de 150 {U} construits, et les acquéreurs ont accès à un club des résidents avec piscine intérieure chauffée et salle de sport.',
  'Die meisten Wohnungen haben drei Schlafzimmer und mehr als 150 {U} bebaute Fläche, und Käufer haben Zugang zu einem Bewohnerclub mit beheiztem Hallenbad und Fitnessraum.',
  'В большинстве квартир три спальни и более 150 {U} площади застройки, а покупатели получают доступ в клуб для жителей с крытым подогреваемым бассейном и тренажёрным залом.',
  'معظم المساكن بثلاث غرف نوم وبمساحة مبنية تزيد على 150 {U}، ويحق للمشترين دخول نادٍ للسكان بمسبح داخلي مدفأ وصالة رياضية.',
  'De meeste woningen hebben drie slaapkamers en meer dan 150 {U} bebouwd, en kopers hebben toegang tot een bewonersclub met een verwarmd binnenzwembad en een fitnessruimte.',
  'Większość mieszkań ma trzy sypialnie i ponad 150 {U} zabudowy, a kupujący mają dostęp do klubu mieszkańców z krytym podgrzewanym basenem i siłownią.',
  'De fleste boligene har tre soverom og over 150 {U} bygget, og kjøperne har tilgang til en beboerklubb med oppvarmet innendørsbasseng og treningsrom.',
  'De flesta bostäderna har tre sovrum och över 150 {U} byggyta, och köparna har tillgång till en klubb för de boende med uppvärmd inomhuspool och gym.')
a(113, 'The scheme sits on the hillside beside Selwo',
  'El conjunto está en la ladera junto a Selwo Aventura, a poca distancia en coche del centro de Estepona y de la playa, con vistas al mar.',
  'L’ensemble se trouve à flanc de colline à côté de Selwo Aventura, à quelques minutes en voiture du centre d’Estepona et de la plage, avec vue sur la mer.',
  'Die Anlage liegt am Hang neben Selwo Aventura, eine kurze Autofahrt vom Zentrum Esteponas und vom Strand entfernt, mit Blick aufs Meer.',
  'Комплекс расположен на склоне рядом с Selwo Aventura, в нескольких минутах езды от центра Эстепоны и пляжа, с видом на море.',
  'يقع المجمّع على سفح التل بجوار Selwo Aventura، على مسافة قصيرة بالسيارة من وسط إستيبونا والشاطئ، مع إطلالة على البحر.',
  'Het complex ligt op de heuvel naast Selwo Aventura, op korte rijafstand van het centrum van Estepona en het strand, met uitzicht op zee.',
  'Osiedle leży na zboczu obok Selwo Aventura, niedaleko samochodem od centrum Estepony i plaży, z widokiem na morze.',
  'Anlegget ligger i åssiden ved Selwo Aventura, en kort kjøretur fra sentrum av Estepona og stranden, med utsikt mot havet.',
  'Området ligger i sluttningen intill Selwo Aventura, en kort bilresa från Esteponas centrum och stranden, med utsikt mot havet.')
a(114, 'A finished home <em>in Estepona</em>',
  'Una vivienda terminada <em>en Estepona</em>', 'Un logement achevé <em>à Estepona</em>', 'Eine fertige Wohnung <em>in Estepona</em>',
  'Готовая квартира <em>в Эстепоне</em>', 'مسكن مكتمل <em>في إستيبونا</em>', 'Een opgeleverde woning <em>in Estepona</em>',
  'Ukończone mieszkanie <em>w Esteponie</em>', 'En ferdig bolig <em>i Estepona</em>', 'En färdig bostad <em>i Estepona</em>')
a(115, 'Ready now', 'Lista ya', 'Prêt dès maintenant', 'Sofort bereit', 'Готово сейчас', 'جاهز الآن', 'Nu klaar', 'Gotowe od razu', 'Klar nå', 'Klar nu')
a(116, 'The portal lists every home as turnkey',
  'El portal presenta todas las viviendas como llave en mano y de entrega inmediata, de modo que no hay plazo de obra que esperar.',
  'Le portail présente chaque logement comme clés en main et livrable immédiatement : il n’y a donc pas de chantier à attendre.',
  'Das Portal führt jede Wohnung als schlüsselfertig mit sofortiger Übergabe, es gibt also keine Bauzeit abzuwarten.',
  'Портал указывает все квартиры как готовые под ключ с немедленной передачей, поэтому ждать окончания стройки не нужно.',
  'تعرض البوابة كل المساكن على أنها جاهزة بالكامل للتسليم الفوري، فلا توجد فترة بناء للانتظار.',
  'Het portaal vermeldt elke woning als sleutelklaar met directe oplevering, dus er is geen bouwperiode om op te wachten.',
  'Portal podaje wszystkie mieszkania jako gotowe pod klucz do natychmiastowego odbioru, więc nie trzeba czekać na zakończenie budowy.',
  'Portalen oppgir alle boligene som nøkkelferdige med umiddelbar overtakelse, så det er ingen byggeperiode å vente på.',
  'Portalen anger varje bostad som nyckelfärdig med omedelbart tillträde, så det finns ingen byggtid att vänta ut.')
a(117, 'The Torrevigía sector lies close to Estepona',
  'El sector de Torrevigía está cerca del centro de Estepona, con La Resina Golf y la playa a poca distancia.',
  'Le secteur de Torrevigía est proche du centre d’Estepona, avec La Resina Golf et la plage à courte distance.',
  'Der Sektor Torrevigía liegt nahe dem Zentrum Esteponas, mit La Resina Golf und dem Strand in kurzer Entfernung.',
  'Сектор Торревихия находится недалеко от центра Эстепоны, а La Resina Golf и пляж — совсем рядом.',
  'يقع قطاع توريفيخيا قرب وسط إستيبونا، ويبعد عنه نادي La Resina Golf والشاطئ مسافة قصيرة.',
  'De sector Torrevigía ligt dicht bij het centrum van Estepona, met La Resina Golf en het strand op korte afstand.',
  'Sektor Torrevigía leży blisko centrum Estepony, a La Resina Golf i plaża są niedaleko.',
  'Torrevigía-området ligger nær sentrum av Estepona, med La Resina Golf og stranden et lite stykke unna.',
  'Torrevigía-området ligger nära Esteponas centrum, med La Resina Golf och stranden en kort bit bort.')
a(118, 'Suits a main or second home',
  'Adecuada como vivienda habitual o segunda residencia, o para alquilar con sujeción a las normas de la comunidad y a la licencia local, que comprobamos.',
  'Convient comme résidence principale ou secondaire, ou à la location sous réserve du règlement de copropriété et de la licence locale, que nous vérifions.',
  'Geeignet als Haupt- oder Zweitwohnsitz oder zur Vermietung, vorbehaltlich der Gemeinschaftsordnung und der örtlichen Lizenz, die wir beide prüfen.',
  'Подходит как основное или второе жильё либо для сдачи в аренду с учётом правил сообщества и местной лицензии — мы проверяем и то, и другое.',
  'يناسب السكن الرئيسي أو الثاني، أو التأجير وفق أنظمة المجمّع والترخيص المحلي، ونتحقق من كليهما.',
  'Geschikt als hoofdverblijf of tweede woning, of voor verhuur onder voorbehoud van het reglement van de vereniging van eigenaars en de lokale vergunning, die wij allebei controleren.',
  'Nadaje się na główne lub drugie mieszkanie albo na wynajem, z zastrzeżeniem regulaminu wspólnoty i lokalnej licencji, które sprawdzamy.',
  'Passer som helårsbolig eller fritidsbolig, eller for utleie med forbehold om sameiets vedtekter og den lokale lisensen, som vi sjekker begge.',
  'Passar som permanentbostad eller fritidsbostad, eller för uthyrning med förbehåll för föreningens regler och den lokala licensen, som vi kontrollerar båda.')
a(119, 'The first-occupation licence and the final energy',
  'La licencia de primera ocupación y el certificado energético definitivo de la vivienda que elija; los planos indican la calificación como provisional.',
  'La licence de première occupation et le certificat énergétique définitif du logement que vous choisissez ; les plans indiquent un classement provisoire.',
  'Die Erstbezugsgenehmigung und den endgültigen Energieausweis der von Ihnen gewählten Wohnung; die Grundrisse weisen die Einstufung als vorläufig aus.',
  'Лицензию на первое заселение и окончательный энергетический сертификат выбранной вами квартиры; на планах класс указан как предварительный.',
  'رخصة الإشغال الأول وشهادة الطاقة النهائية للمسكن الذي تختارونه؛ إذ تشير المخططات إلى أن التصنيف مؤقت.',
  'De vergunning voor eerste bewoning en het definitieve energiecertificaat van de woning van uw keuze; de plattegronden vermelden het label als voorlopig.',
  'Pozwolenie na pierwsze zasiedlenie i ostateczne świadectwo energetyczne wybranego mieszkania; na rzutach klasa jest oznaczona jako tymczasowa.',
  'Brukstillatelsen og det endelige energisertifikatet for boligen De velger; plantegningene oppgir karakteren som foreløpig.',
  'Inflyttningstillståndet och den slutliga energideklarationen för den bostad ni väljer; planritningarna anger klassningen som preliminär.')
a(120, 'That the home, its terrace, and the parking',
  'Que la vivienda, su terraza y la plaza o plazas de garaje y el trastero que se venden con ella estén inscritos tal como se describen.',
  'Que le logement, sa terrasse, et la ou les places de parking et le cellier vendus avec lui sont inscrits tels que décrits.',
  'Dass die Wohnung, ihre Terrasse sowie der oder die mitverkauften Stellplätze und der Abstellraum wie beschrieben eingetragen sind.',
  'Что квартира, её терраса, а также продаваемые вместе с ней машино-место или места и кладовая зарегистрированы так, как описано.',
  'أن المسكن وتراسه وموقف السيارة أو المواقف والمخزن المبيعة معه مسجّلة كما هو موصوف.',
  'Dat de woning, het terras en de meeverkochte parkeerplaats of -plaatsen en berging zijn ingeschreven zoals beschreven.',
  'Że mieszkanie, jego taras oraz sprzedawane z nim miejsce lub miejsca parkingowe i komórka lokatorska są wpisane do rejestru zgodnie z opisem.',
  'At boligen, terrassen og parkeringsplassen eller -plassene og boden som selges med den, er registrert slik de er beskrevet.',
  'Att bostaden, terrassen samt den eller de parkeringsplatser och det förråd som säljs med den är registrerade så som de beskrivs.')
a(121, 'The list and the drawings state the areas',
  'La lista y los planos expresan las superficies de forma distinta; confirmamos las cifras registrales de la vivienda que elija.',
  'La liste et les plans expriment les surfaces différemment ; nous confirmons les chiffres inscrits pour le logement que vous choisissez.',
  'Liste und Grundrisse weisen die Flächen unterschiedlich aus; wir bestätigen die eingetragenen Werte der von Ihnen gewählten Wohnung.',
  'Список и планы указывают площади по-разному; мы подтверждаем зарегистрированные значения для выбранной вами квартиры.',
  'تعرض القائمة والمخططات المساحات بطريقتين مختلفتين؛ ونؤكد الأرقام المسجّلة للمسكن الذي تختارونه.',
  'De lijst en de plattegronden geven de oppervlaktes verschillend weer; wij bevestigen de ingeschreven cijfers van de woning van uw keuze.',
  'Lista i rzuty podają powierzchnie w różny sposób; potwierdzamy wartości wpisane do rejestru dla wybranego przez Państwa mieszkania.',
  'Listen og plantegningene oppgir arealene ulikt; vi bekrefter de registrerte tallene for boligen De velger.',
  'Listan och planritningarna redovisar ytorna olika; vi bekräftar de registrerade siffrorna för den bostad ni väljer.')
a(122, 'The third-floor home', 'La vivienda de la tercera planta', 'Le logement du troisième étage', 'Die Wohnung im dritten Obergeschoss',
  'Квартира на четвёртом этаже', 'مسكن الطابق الثالث', 'De woning op de derde verdieping', 'Mieszkanie na trzecim piętrze', 'Boligen i fjerde etasje', 'Bostaden på tredje våningen')
a(123, 'Its drawing is not in the documents',
  'Su plano no figura en los documentos de que disponemos y su precio queda muy por encima del resto; pedimos ambos por escrito.',
  'Son plan ne figure pas dans les documents dont nous disposons et son prix est nettement supérieur aux autres ; nous demandons l’un et l’autre par écrit.',
  'Ihr Grundriss liegt uns nicht vor, und ihr Preis liegt deutlich über dem der übrigen; wir fordern beides schriftlich an.',
  'Её плана нет в имеющихся у нас документах, а цена значительно выше остальных; мы запрашиваем и то, и другое в письменном виде.',
  'لا يوجد مخططه ضمن المستندات التي لدينا، وسعره أعلى بكثير من البقية؛ ونطلب الأمرين كتابياً.',
  'De plattegrond zit niet in de documenten die wij hebben en de prijs ligt ver boven die van de rest; wij vragen beide schriftelijk op.',
  'Jego rzutu nie ma w posiadanych przez nas dokumentach, a cena znacznie przewyższa pozostałe; prosimy o jedno i drugie na piśmie.',
  'Plantegningen finnes ikke i dokumentene vi har, og prisen ligger godt over de andre; vi ber om begge deler skriftlig.',
  'Dess planritning finns inte i de handlingar vi har och priset ligger långt över de övriga; vi begär båda delarna skriftligen.')

# ---- architecture, lifestyle, viewing, location
a(124, 'Blocks that <em>step down the slope</em>',
  'Bloques que <em>bajan por la ladera</em>', 'Des blocs <em>en gradins sur la pente</em>', 'Blöcke, die sich <em>den Hang hinab staffeln</em>',
  'Корпуса, <em>спускающиеся по склону</em>', 'مبانٍ <em>تتدرّج مع المنحدر</em>', 'Blokken die <em>de helling af trappen</em>',
  'Bloki <em>schodzące po zboczu</em>', 'Blokker som <em>trapper seg ned skråningen</em>', 'Hus som <em>trappar ner för sluttningen</em>')
a(125, 'The blocks are tiered over the slope',
  'Los bloques se escalonan sobre la pendiente para que las viviendas miren al mar, con esquinas redondeadas, fachadas de piedra, hormigón blanco y vidrio, y cubiertas y terrazas ajardinadas.',
  'Les blocs s’étagent sur la pente pour que les logements regardent la mer, avec des angles arrondis, des façades en pierre, béton blanc et verre, et des toits et terrasses plantés.',
  'Die Blöcke staffeln sich über den Hang, damit die Wohnungen zum Meer blicken, mit abgerundeten Ecken, Fassaden aus Naturstein, weißem Beton und Glas sowie begrünten Dächern und Terrassen.',
  'Корпуса расположены уступами на склоне, чтобы квартиры смотрели на море; у них скруглённые углы, фасады из камня, белого бетона и стекла, озеленённые крыши и террасы.',
  'تتدرّج المباني على المنحدر لتطل المساكن على البحر، بزوايا مستديرة وواجهات من الحجر والخرسانة البيضاء والزجاج، وأسطح وتراسات مزروعة.',
  'De blokken zijn trapsgewijs over de helling gebouwd zodat de woningen op zee uitkijken, met afgeronde hoeken, gevels van natuursteen, wit beton en glas, en beplante daken en terrassen.',
  'Bloki ustawiono tarasowo na zboczu, tak by mieszkania patrzyły na morze; mają zaokrąglone narożniki, elewacje z kamienia, białego betonu i szkła oraz zazielenione dachy i tarasy.',
  'Blokkene er trappet over skråningen slik at boligene ser mot havet, med avrundede hjørner, fasader i stein, hvit betong og glass, og beplantede tak og terrasser.',
  'Husen är terrasserade över sluttningen så att bostäderna vetter mot havet, med rundade hörn, fasader av sten, vit betong och glas samt planterade tak och terrasser.')
a(126, 'Several low blocks on the hillside',
  'Varios bloques bajos en la ladera, cada uno con sus portales, ascensores y garaje comunitario.',
  'Plusieurs blocs bas à flanc de colline, chacun avec ses entrées, ses ascenseurs et un garage commun.',
  'Mehrere niedrige Blöcke am Hang, jeder mit eigenen Aufgängen, Aufzügen und einer Gemeinschaftsgarage.',
  'Несколько невысоких корпусов на склоне, у каждого свои подъезды, лифты и общий гараж.',
  'عدة مبانٍ منخفضة على سفح التل، لكل منها مداخله ومصاعده ومرأب مشترك.',
  'Enkele lage blokken op de heuvel, elk met eigen portieken, liften en een gemeenschappelijke garage.',
  'Kilka niskich bloków na zboczu, każdy z własnymi klatkami, windami i wspólnym garażem.',
  'Flere lave blokker i åssiden, hver med egne oppganger, heiser og en felles garasje.',
  'Flera låga hus i sluttningen, vart och ett med egna uppgångar, hissar och ett gemensamt garage.')
a(127, 'Covered terraces of 33.10 to 45.35',
  'Terrazas cubiertas de {N33.10} a {N45.35} {U} en planta baja y primera planta, y de unos 50 {U}, en parte descubiertas, en la segunda.',
  'Des terrasses couvertes de {N33.10} à {N45.35} {U} au rez-de-chaussée et au premier étage, et d’environ 50 {U}, en partie ouvertes, au deuxième.',
  'Überdachte Terrassen von {N33.10} bis {N45.35} {U} im Erdgeschoss und ersten Obergeschoss und von etwa 50 {U}, teils offen, im zweiten.',
  'Крытые террасы от {N33.10} до {N45.35} {U} на первом и втором этажах и около 50 {U}, частично открытые, на третьем.',
  'تراسات مسقوفة من {N33.10} إلى {N45.35} {U} في الطابقين الأرضي والأول، وتراسات بنحو 50 {U}، مكشوفة جزئياً، في الثاني.',
  'Overdekte terrassen van {N33.10} tot {N45.35} {U} op de begane grond en de eerste verdieping, en van ongeveer 50 {U}, deels open, op de tweede.',
  'Zadaszone tarasy od {N33.10} do {N45.35} {U} na parterze i pierwszym piętrze oraz około 50 {U}, częściowo otwarte, na drugim.',
  'Overbygde terrasser på {N33.10} til {N45.35} {U} i første og andre etasje, og på omkring 50 {U}, delvis åpne, i tredje.',
  'Övertäckta terrasser på {N33.10} till {N45.35} {U} på bottenvåningen och första våningen, och på omkring 50 {U}, delvis öppna, på andra.')
a(128, 'Porcelain stoneware floors, suspended ceilings',
  'Suelos de gres porcelánico, falsos techos, cocina amueblada y equipada y baño principal en suite.',
  'Sols en grès cérame, faux plafonds, cuisine aménagée et équipée et salle de bains principale attenante à la chambre.',
  'Feinsteinzeugböden, abgehängte Decken, eine eingebaute und ausgestattete Küche und ein Hauptbad en suite.',
  'Полы из керамогранита, подвесные потолки, встроенная оборудованная кухня и главная ванная при спальне.',
  'أرضيات من البورسلين، وأسقف معلّقة، ومطبخ مجهّز بالكامل، وحمّام رئيسي ملحق بغرفة النوم.',
  'Vloeren van keramisch graniet, verlaagde plafonds, een ingerichte en uitgeruste keuken en een hoofdbadkamer en suite.',
  'Podłogi z gresu porcelanowego, sufity podwieszane, umeblowana i wyposażona kuchnia oraz łazienka główna przy sypialni.',
  'Gulv av porselensfliser, nedsenkede himlinger, innredet og utstyrt kjøkken og hovedbad med eget soverom.',
  'Golv av porslinsklinker, undertak, inrett och utrustat kök och huvudbadrum i anslutning till sovrummet.')
a(129, 'Hot-water underfloor heating, ducted cooling',
  'Suelo radiante por agua caliente, refrigeración por conductos, bomba de calor aerotérmica para el agua caliente y doble acristalamiento; los planos indican una calificación A provisional.',
  'Plancher chauffant à eau chaude, rafraîchissement gainable, pompe à chaleur aérothermique pour l’eau chaude et double vitrage ; les plans portent un classement A provisoire.',
  'Warmwasser-Fußbodenheizung, kanalgeführte Kühlung, eine Luft-Wasser-Wärmepumpe für das Warmwasser und Doppelverglasung; die Grundrisse weisen eine vorläufige Einstufung A aus.',
  'Водяной тёплый пол, канальное охлаждение, аэротермальный тепловой насос для горячей воды и двойное остекление; на планах указан предварительный класс A.',
  'تدفئة أرضية بالماء الساخن، وتبريد عبر مجارٍ، ومضخة حرارية هوائية لتسخين المياه، وزجاج مزدوج؛ وتحمل المخططات تصنيف A مؤقتاً.',
  'Vloerverwarming op warm water, koeling via kanalen, een luchtwarmtepomp voor warm water en dubbele beglazing; de plattegronden vermelden een voorlopig A-label.',
  'Wodne ogrzewanie podłogowe, chłodzenie kanałowe, aerotermiczna pompa ciepła do ciepłej wody i podwójne szyby; na rzutach widnieje tymczasowa klasa A.',
  'Vannbåren gulvvarme, kanalbasert kjøling, luft-til-vann-varmepumpe for varmtvann og doble glass; plantegningene oppgir en foreløpig A-karakter.',
  'Vattenburen golvvärme, kanaliserad kyla, en luft-vattenvärmepump för varmvatten och tvåglas; planritningarna anger en preliminär A-klassning.')
a(130, 'Torrevigía, <em>above Estepona</em>',
  'Torrevigía, <em>sobre Estepona</em>', 'Torrevigía, <em>au-dessus d’Estepona</em>', 'Torrevigía, <em>über Estepona</em>', 'Торревихия, <em>над Эстепоной</em>',
  'توريفيخيا، <em>فوق إستيبونا</em>', 'Torrevigía, <em>boven Estepona</em>', 'Torrevigía, <em>nad Esteponą</em>', 'Torrevigía, <em>over Estepona</em>', 'Torrevigía, <em>ovanför Estepona</em>')
a(131, 'A natural setting on the hillside',
  'Un entorno natural en la ladera junto a Selwo Aventura, con La Resina Golf cerca y la costa a sus pies.',
  'Un cadre naturel à flanc de colline à côté de Selwo Aventura, avec La Resina Golf tout près et la côte en contrebas.',
  'Eine natürliche Umgebung am Hang neben Selwo Aventura, mit La Resina Golf in der Nähe und der Küste unterhalb.',
  'Природное окружение на склоне рядом с Selwo Aventura, неподалёку La Resina Golf, внизу побережье.',
  'بيئة طبيعية على سفح التل بجوار Selwo Aventura، مع نادي La Resina Golf على مقربة والساحل في الأسفل.',
  'Een natuurlijke omgeving op de heuvel naast Selwo Aventura, met La Resina Golf dichtbij en de kust beneden.',
  'Naturalne otoczenie na zboczu obok Selwo Aventura, z pobliskim La Resina Golf i wybrzeżem poniżej.',
  'Naturlige omgivelser i åssiden ved Selwo Aventura, med La Resina Golf like i nærheten og kysten nedenfor.',
  'En naturnära miljö i sluttningen intill Selwo Aventura, med La Resina Golf i närheten och kusten nedanför.')
a(132, 'Access to the residents’ club of the wider estate',
  'Acceso al club de residentes de la urbanización, con piscina interior climatizada, gimnasio, saunas, comedor y jardines.',
  'L’accès au club des résidents du domaine, avec piscine intérieure chauffée, salle de sport, saunas, salle à manger et jardins.',
  'Zugang zum Bewohnerclub des Gesamtareals mit beheiztem Hallenbad, Fitnessraum, Saunen, Speisesaal und Gärten.',
  'Доступ в клуб для жителей всего жилого района с крытым подогреваемым бассейном, тренажёрным залом, саунами, обеденным залом и садами.',
  'إمكانية دخول نادي السكان في المنطقة السكنية الأوسع، بمسبح داخلي مدفأ وصالة رياضية وساونا وصالة طعام وحدائق.',
  'Toegang tot de bewonersclub van het grotere domein, met een verwarmd binnenzwembad, een fitnessruimte, sauna’s, een eetzaal en tuinen.',
  'Dostęp do klubu mieszkańców całego kompleksu, z krytym podgrzewanym basenem, siłownią, saunami, jadalnią i ogrodami.',
  'Tilgang til beboerklubben i det større området, med oppvarmet innendørsbasseng, treningsrom, badstuer, spisesal og hager.',
  'Tillgång till de boendes klubb i det större området, med uppvärmd inomhuspool, gym, bastur, matsal och trädgårdar.')
a(133, 'In the scheme', 'En el conjunto', 'Dans l’ensemble', 'In der Anlage', 'В комплексе', 'داخل المجمّع', 'In het complex', 'Na osiedlu', 'I anlegget', 'Inom området')
a(134, 'A swimming pool, a co-working space',
  'Una piscina, un espacio de coworking, jardines con vegetación autóctona de bajo consumo de agua y aparcamiento para bicicletas.',
  'Une piscine, un espace de coworking, des jardins plantés d’espèces locales peu gourmandes en eau et un local à vélos.',
  'Ein Pool, ein Coworking-Bereich, Gärten mit heimischer, wassersparender Bepflanzung und Fahrradstellplätze.',
  'Бассейн, коворкинг, сады с местными засухоустойчивыми растениями и велосипедная стоянка.',
  'مسبح، ومساحة عمل مشتركة، وحدائق بنباتات محلية قليلة الاستهلاك للمياه، ومكان للدراجات.',
  'Een zwembad, een coworkingruimte, tuinen met inheemse, waterzuinige beplanting en een fietsenstalling.',
  'Basen, przestrzeń coworkingowa, ogrody z rodzimą, oszczędzającą wodę roślinnością i miejsce na rowery.',
  'Et basseng, et coworking-område, hager med stedegne, vannsparende planter og sykkelparkering.',
  'En pool, ett coworkingutrymme, trädgårdar med inhemska, vattensnåla växter och cykelförråd.')
a(135, 'The A-7 is close; the brochure puts',
  'La A-7 está cerca; el folleto sitúa Puerto Banús a unos veinte minutos y Gibraltar a una hora aproximadamente.',
  'L’A-7 est proche ; la brochure place Puerto Banús à une vingtaine de minutes et Gibraltar à environ une heure.',
  'Die A-7 ist nah; laut Broschüre liegt Puerto Banús etwa zwanzig Minuten und Gibraltar etwa eine Stunde entfernt.',
  'Трасса A-7 рядом; по данным брошюры, до Пуэрто-Бануса около двадцати минут, до Гибралтара около часа.',
  'الطريق A-7 قريب؛ ويذكر الكتيّب أن بويرتو بانوس على بعد نحو عشرين دقيقة وجبل طارق على بعد نحو ساعة.',
  'De A-7 ligt dichtbij; volgens de brochure ligt Puerto Banús op zo’n twintig minuten en Gibraltar op ongeveer een uur.',
  'A-7 jest blisko; według broszury do Puerto Banús jest około dwudziestu minut, a do Gibraltaru około godziny.',
  'A-7 er like ved; ifølge brosjyren ligger Puerto Banús omkring tjue minutter unna og Gibraltar omkring en time.',
  'A-7 ligger nära; enligt broschyren ligger Puerto Banús omkring tjugo minuter bort och Gibraltar omkring en timme.')
a(136, 'Walk the blocks and the portal',
  'Recorra los bloques y el portal que le interese, la piscina comunitaria y los jardines.',
  'Parcourez les blocs et l’entrée qui vous intéresse, la piscine commune et les jardins.',
  'Gehen Sie durch die Blöcke und den Aufgang, der Sie interessiert, sowie den Gemeinschaftspool und die Gärten.',
  'Пройдите по корпусам и интересующему вас подъезду, к общему бассейну и садам.',
  'تجوّلوا في المباني والمدخل الذي يهمّكم، وفي المسبح المشترك والحدائق.',
  'Loop door de blokken en het portiek dat u overweegt, en langs het gemeenschappelijke zwembad en de tuinen.',
  'Proszę obejrzeć bloki i interesującą Państwa klatkę, a także wspólny basen i ogrody.',
  'Gå gjennom blokkene og oppgangen De vurderer, og fellesbassenget og hagene.',
  'Gå igenom husen och den uppgång ni överväger, samt den gemensamma poolen och trädgårdarna.')
a(137, 'Compare what each floor and orientation',
  'Compare qué ve cada planta y orientación, hacia el mar o hacia las colinas.',
  'Comparez ce que voit chaque étage et chaque orientation, vers la mer ou vers les collines.',
  'Vergleichen Sie, worauf jede Etage und Ausrichtung blickt, aufs Meer oder auf die Hügel.',
  'Сравните, что видно с каждого этажа и при каждой ориентации — море или холмы.',
  'قارنوا ما يطل عليه كل طابق وكل اتجاه، نحو البحر أو التلال.',
  'Vergelijk waar elke verdieping en oriëntatie op uitkijkt, naar zee of naar de heuvels.',
  'Proszę porównać, na co wychodzi każde piętro i orientacja, na morze czy na wzgórza.',
  'Sammenlign hva hver etasje og retning ser mot, havet eller åsene.',
  'Jämför vad varje våning och väderstreck vetter mot, havet eller kullarna.')
a(138, 'See the residents’ club with its indoor pool',
  'Conozca el club de residentes con su piscina interior y su gimnasio.',
  'Découvrez le club des résidents, avec sa piscine intérieure et sa salle de sport.',
  'Besichtigen Sie den Bewohnerclub mit Hallenbad und Fitnessraum.',
  'Осмотрите клуб для жителей с крытым бассейном и тренажёрным залом.',
  'شاهدوا نادي السكان بمسبحه الداخلي وصالته الرياضية.',
  'Bekijk de bewonersclub met het binnenzwembad en de fitnessruimte.',
  'Proszę zobaczyć klub mieszkańców z krytym basenem i siłownią.',
  'Se beboerklubben med innendørsbasseng og treningsrom.',
  'Se de boendes klubb med inomhuspool och gym.')
a(139, 'Torrevigía, <em>Estepona</em>',
  'Torrevigía, <em>Estepona</em>', 'Torrevigía, <em>Estepona</em>', 'Torrevigía, <em>Estepona</em>', 'Торревихия, <em>Эстепона</em>', 'توريفيخيا، <em>إستيبونا</em>',
  'Torrevigía, <em>Estepona</em>', 'Torrevigía, <em>Estepona</em>', 'Torrevigía, <em>Estepona</em>', 'Torrevigía, <em>Estepona</em>')
a(140, 'A gated scheme in the Torrevigía sector',
  'Un conjunto cerrado en el sector de Torrevigía, en la ladera sobre Estepona, junto a Selwo Aventura, con La Resina Golf cerca y la costa abajo.',
  'Un ensemble fermé dans le secteur de Torrevigía, à flanc de colline au-dessus d’Estepona, à côté de Selwo Aventura, avec La Resina Golf tout près et la côte en contrebas.',
  'Eine geschlossene Anlage im Sektor Torrevigía am Hang über Estepona, neben Selwo Aventura, mit La Resina Golf in der Nähe und der Küste unterhalb.',
  'Закрытый комплекс в секторе Торревихия на склоне над Эстепоной, рядом с Selwo Aventura, неподалёку La Resina Golf, внизу побережье.',
  'مجمّع مسوَّر في قطاع توريفيخيا على سفح التل فوق إستيبونا، بجوار Selwo Aventura، مع نادي La Resina Golf على مقربة والساحل في الأسفل.',
  'Een afgesloten complex in de sector Torrevigía op de heuvel boven Estepona, naast Selwo Aventura, met La Resina Golf dichtbij en de kust beneden.',
  'Zamknięte osiedle w sektorze Torrevigía na zboczu nad Esteponą, obok Selwo Aventura, z pobliskim La Resina Golf i wybrzeżem poniżej.',
  'Et inngjerdet anlegg i Torrevigía-området i åssiden over Estepona, ved Selwo Aventura, med La Resina Golf i nærheten og kysten nedenfor.',
  'Ett inhägnat område i Torrevigía i sluttningen ovanför Estepona, intill Selwo Aventura, med La Resina Golf i närheten och kusten nedanför.')
a(141, 'Approx. 1 hour 10 minutes',
  'Aprox. 1 hora y 10 minutos', 'Env. 1 heure 10 minutes', 'Ca. 1 Stunde 10 Minuten', 'Ок. 1 часа 10 минут', 'حوالي ساعة و10 دقائق',
  'Ca. 1 uur en 10 minuten', 'Ok. 1 godzina 10 minut', 'Ca. 1 time og 10 minutter', 'Ca 1 timme och 10 minuter')

# ---- faq, timeline, enquiry, seo
a(142, 'From EUR 638,000 to EUR 900,000, and EUR 1,762,000',
  'De {E638000} a {E900000}, y {E1762000} la única vivienda de la tercera planta, sin IVA ni gastos de compra.',
  'De {E638000} à {E900000}, et {E1762000} pour l’unique logement du troisième étage, hors TVA et frais d’acquisition.',
  'Von {E638000} bis {E900000} und {E1762000} für die einzige Wohnung im dritten Obergeschoss, zuzüglich MwSt. und Erwerbsnebenkosten.',
  'От {E638000} до {E900000} и {E1762000} за единственную квартиру на четвёртом этаже, без НДС и расходов на оформление.',
  'من {E638000} إلى {E900000}، و{E1762000} للمسكن الوحيد في الطابق الثالث، دون ضريبة القيمة المضافة ومصاريف الشراء.',
  'Van {E638000} tot {E900000}, en {E1762000} voor de enige woning op de derde verdieping, exclusief btw en aankoopkosten.',
  'Od {E638000} do {E900000} oraz {E1762000} za jedyne mieszkanie na trzecim piętrze, bez podatku VAT i kosztów nabycia.',
  'Fra {E638000} til {E900000}, og {E1762000} for den eneste boligen i fjerde etasje, eksklusive mva og kjøpsomkostninger.',
  'Från {E638000} till {E900000}, och {E1762000} för den enda bostaden på tredje våningen, exklusive IVA (spansk moms) och köpkostnader.')
a(143, 'Nineteen: eight in the first phase',
  'Diecinueve: ocho en la primera fase y once en la segunda.', 'Dix-neuf : huit dans la première phase et onze dans la seconde.',
  'Neunzehn: acht im ersten und elf im zweiten Bauabschnitt.', 'Девятнадцать: восемь в первой очереди и одиннадцать во второй.',
  'تسعة عشر: ثمانية في المرحلة الأولى وأحد عشر في الثانية.', 'Negentien: acht in de eerste fase en elf in de tweede.',
  'Dziewiętnaście: osiem w pierwszym etapie i jedenaście w drugim.', 'Nitten: åtte i første byggetrinn og elleve i det andre.',
  'Nitton: åtta i den första etappen och elva i den andra.')
a(144, 'Are the homes finished?', '¿Están terminadas las viviendas?', 'Les logements sont-ils achevés ?', 'Sind die Wohnungen fertiggestellt?',
  'Квартиры уже построены?', 'هل المساكن مكتملة؟', 'Zijn de woningen opgeleverd?', 'Czy mieszkania są ukończone?', 'Er boligene ferdige?', 'Är bostäderna färdiga?')
a(145, 'The developer’s portal lists both phases',
  'El portal del promotor presenta ambas fases como llave en mano y de entrega inmediata. Solicitamos la licencia de primera ocupación y el certificado energético de la vivienda que elija.',
  'Le portail du promoteur présente les deux phases comme clés en main et livrables immédiatement. Nous demandons la licence de première occupation et le certificat énergétique du logement que vous choisissez.',
  'Das Portal des Bauträgers führt beide Bauabschnitte als schlüsselfertig mit sofortiger Übergabe. Wir fragen die Erstbezugsgenehmigung und den Energieausweis der von Ihnen gewählten Wohnung an.',
  'Портал застройщика указывает обе очереди как готовые под ключ с немедленной передачей. Мы запрашиваем лицензию на первое заселение и энергетический сертификат выбранной вами квартиры.',
  'تعرض بوابة المطوّر المرحلتين على أنهما جاهزتان بالكامل للتسليم الفوري. ونطلب رخصة الإشغال الأول وشهادة الطاقة للمسكن الذي تختارونه.',
  'Het portaal van de ontwikkelaar vermeldt beide fasen als sleutelklaar met directe oplevering. Wij vragen de vergunning voor eerste bewoning en het energiecertificaat van de woning van uw keuze op.',
  'Portal dewelopera podaje oba etapy jako gotowe pod klucz do natychmiastowego odbioru. Prosimy o pozwolenie na pierwsze zasiedlenie i świadectwo energetyczne wybranego przez Państwa mieszkania.',
  'Utbyggerens portal oppgir begge byggetrinnene som nøkkelferdige med umiddelbar overtakelse. Vi ber om brukstillatelsen og energisertifikatet for boligen De velger.',
  'Exploatörens portal anger båda etapperna som nyckelfärdiga med omedelbart tillträde. Vi begär inflyttningstillståndet och energideklarationen för den bostad ni väljer.')
a(146, 'From 131.05 to 196.08 sqm built',
  'De {N131.05} a {N196.08} {U} construidos, con un interior útil de {N103.73} a {N155.32} {U} y terrazas de {N33.10} a {N50.45} {U} según los planos.',
  'De {N131.05} à {N196.08} {U} construits, avec {N103.73} à {N155.32} {U} de surface utile intérieure et des terrasses de {N33.10} à {N50.45} {U} selon les plans.',
  'Von {N131.05} bis {N196.08} {U} bebaut, mit {N103.73} bis {N155.32} {U} Wohnfläche und Terrassen von {N33.10} bis {N50.45} {U} laut Grundriss.',
  'От {N131.05} до {N196.08} {U} застройки, полезная внутренняя площадь от {N103.73} до {N155.32} {U}, террасы от {N33.10} до {N50.45} {U} по планам.',
  'من {N131.05} إلى {N196.08} {U} مبنية، بمساحة داخلية صافية من {N103.73} إلى {N155.32} {U} وتراسات من {N33.10} إلى {N50.45} {U} وفق المخططات.',
  'Van {N131.05} tot {N196.08} {U} bebouwd, met {N103.73} tot {N155.32} {U} nuttige binnenoppervlakte en terrassen van {N33.10} tot {N50.45} {U} volgens de plattegronden.',
  'Od {N131.05} do {N196.08} {U} zabudowy, z powierzchnią użytkową wnętrza od {N103.73} do {N155.32} {U} i tarasami od {N33.10} do {N50.45} {U} według rzutów.',
  'Fra {N131.05} til {N196.08} {U} bygget, med {N103.73} til {N155.32} {U} nyttbart innvendig areal og terrasser på {N33.10} til {N50.45} {U} ifølge plantegningene.',
  'Från {N131.05} till {N196.08} {U} byggyta, med {N103.73} till {N155.32} {U} invändig nyttoyta och terrasser på {N33.10} till {N50.45} {U} enligt planritningarna.')
a(147, 'The price shown is for the home alone',
  'El precio indicado es solo el de la vivienda. La lista del promotor vende una plaza de garaje y un trastero con la mayoría de las viviendas por {E22000}, y dos plazas y un trastero con cinco viviendas por {E38000}.',
  'Le prix indiqué concerne le logement seul. La liste du promoteur vend une place de parking et un cellier avec la plupart des logements pour {E22000}, et deux places et un cellier avec cinq logements pour {E38000}.',
  'Der angegebene Preis gilt für die Wohnung allein. Die Liste des Bauträgers verkauft mit den meisten Wohnungen einen Stellplatz und einen Abstellraum für {E22000}, mit fünf Wohnungen zwei Stellplätze und einen Abstellraum für {E38000}.',
  'Указанная цена — только за квартиру. По списку застройщика с большинством квартир продаются машино-место и кладовая за {E22000}, а с пятью квартирами — два машино-места и кладовая за {E38000}.',
  'السعر المذكور للمسكن وحده. تبيع قائمة المطوّر مع معظم المساكن موقف سيارة ومخزناً مقابل {E22000}، ومع خمسة مساكن موقفين ومخزناً مقابل {E38000}.',
  'De vermelde prijs geldt voor de woning alleen. De lijst van de ontwikkelaar verkoopt bij de meeste woningen een parkeerplaats en een berging voor {E22000}, en bij vijf woningen twee parkeerplaatsen en een berging voor {E38000}.',
  'Podana cena dotyczy samego mieszkania. Lista dewelopera sprzedaje z większością mieszkań miejsce parkingowe i komórkę lokatorską za {E22000}, a z pięcioma mieszkaniami dwa miejsca i komórkę za {E38000}.',
  'Prisen som vises gjelder boligen alene. Utbyggerens liste selger en parkeringsplass og en bod med de fleste boligene for {E22000}, og to plasser og en bod med fem boliger for {E38000}.',
  'Det angivna priset gäller bostaden ensam. Exploatörens lista säljer en parkeringsplats och ett förråd med de flesta bostäderna för {E22000}, och två platser och ett förråd med fem bostäder för {E38000}.')
a(148, 'What does the residents’ club offer?',
  '¿Qué ofrece el club de residentes?', 'Que propose le club des résidents ?', 'Was bietet der Bewohnerclub?', 'Что предлагает клуб для жителей?',
  'ماذا يقدّم نادي السكان؟', 'Wat biedt de bewonersclub?', 'Co oferuje klub mieszkańców?', 'Hva tilbyr beboerklubben?', 'Vad erbjuder de boendes klubb?')
a(149, 'The brochure lists a heated indoor pool',
  'El folleto enumera piscina interior climatizada, gimnasio, saunas, comedor y jardines, abiertos a los residentes del conjunto.',
  'La brochure mentionne une piscine intérieure chauffée, une salle de sport, des saunas, une salle à manger et des jardins, ouverts aux résidents de l’ensemble.',
  'Die Broschüre nennt ein beheiztes Hallenbad, einen Fitnessraum, Saunen, einen Speisesaal und Gärten, offen für die Bewohner der Anlage.',
  'В брошюре перечислены крытый подогреваемый бассейн, тренажёрный зал, сауны, обеденный зал и сады, открытые для жителей комплекса.',
  'يذكر الكتيّب مسبحاً داخلياً مدفأً وصالة رياضية وساونا وصالة طعام وحدائق، متاحة لسكان المجمّع.',
  'De brochure noemt een verwarmd binnenzwembad, een fitnessruimte, sauna’s, een eetzaal en tuinen, open voor de bewoners van het complex.',
  'Broszura wymienia kryty podgrzewany basen, siłownię, sauny, jadalnię i ogrody, dostępne dla mieszkańców osiedla.',
  'Brosjyren nevner oppvarmet innendørsbasseng, treningsrom, badstuer, spisesal og hager, åpne for beboerne i anlegget.',
  'Broschyren nämner uppvärmd inomhuspool, gym, bastur, matsal och trädgårdar, öppna för de boende i området.')
a(150, 'The price list, the drawings of the homes',
  'La lista de precios, los planos de las viviendas que elija y la memoria de calidades.',
  'La liste de prix, les plans des logements que vous choisissez et le descriptif.',
  'Die Preisliste, die Grundrisse der von Ihnen gewählten Wohnungen und die Baubeschreibung.',
  'Прайс-лист, планы выбранных вами квартир и спецификация.',
  'قائمة الأسعار، ومخططات المساكن التي تختارونها، والمواصفات.',
  'De prijslijst, de plattegronden van de woningen van uw keuze en de technische omschrijving.',
  'Cennik, rzuty wybranych przez Państwa mieszkań i specyfikacja.',
  'Prislisten, plantegningene for boligene De velger, og byggebeskrivelsen.',
  'Prislistan, planritningarna för de bostäder ni väljer och byggbeskrivningen.')
a(151, 'See the homes', 'Ver las viviendas', 'Voir les logements', 'Die Wohnungen besichtigen', 'Осмотреть квартиры', 'معاينة المساكن',
  'De woningen bekijken', 'Obejrzeć mieszkania', 'Se boligene', 'Se bostäderna')
a(152, 'We arrange the visit and walk the blocks',
  'Organizamos la visita y recorremos con usted los bloques, los jardines y el club.',
  'Nous organisons la visite et parcourons avec vous les blocs, les jardins et le club.',
  'Wir organisieren die Besichtigung und gehen mit Ihnen durch die Blöcke, die Gärten und den Club.',
  'Мы организуем визит и вместе с вами осмотрим корпуса, сады и клуб.',
  'نرتّب الزيارة ونتجوّل معكم في المباني والحدائق والنادي.',
  'Wij regelen het bezoek en lopen met u door de blokken, de tuinen en de club.',
  'Organizujemy wizytę i oprowadzamy Państwa po blokach, ogrodach i klubie.',
  'Vi ordner visningen og går gjennom blokkene, hagene og klubben sammen med Dem.',
  'Vi ordnar visningen och går igenom husen, trädgårdarna och klubben tillsammans med er.')
a(153, 'Reservation, contract and licences reviewed',
  'Reserva, contrato y licencias revisados antes de que usted firme.', 'Réservation, contrat et licences vérifiés avant votre signature.',
  'Reservierung, Vertrag und Genehmigungen geprüft, bevor Sie unterschreiben.', 'Бронирование, договор и лицензии проверяются до подписания.',
  'مراجعة الحجز والعقد والتراخيص قبل التوقيع.', 'Reservering, contract en vergunningen gecontroleerd voordat u tekent.',
  'Rezerwacja, umowa i pozwolenia sprawdzone przed podpisaniem.', 'Reservasjon, kontrakt og tillatelser gjennomgått før De signerer.',
  'Bokning, kontrakt och tillstånd granskade innan ni skriver under.')
a(154, 'I would like to receive the latest project information',
  'Me gustaría recibir la información más reciente sobre Torrevigía Residences.',
  'Je souhaite recevoir les dernières informations sur Torrevigía Residences.',
  'Ich möchte die aktuellen Projektinformationen zu Torrevigía Residences erhalten.',
  'Я хотел бы получить актуальную информацию о проекте Torrevigía Residences.',
  'أرغب في تلقّي أحدث المعلومات عن مشروع Torrevigía Residences.',
  'Ik ontvang graag de meest recente projectinformatie over Torrevigía Residences.',
  'Chciałbym otrzymać najnowsze informacje o projekcie Torrevigía Residences.',
  'Jeg ønsker å motta oppdatert prosjektinformasjon om Torrevigía Residences.',
  'Jag vill gärna få den senaste projektinformationen om Torrevigía Residences.')
a(155, 'Project context: Torrevigía Residences.',
  'Contexto del proyecto: Torrevigía Residences.', 'Contexte du projet : Torrevigía Residences.', 'Projektkontext: Torrevigía Residences.',
  'Контекст проекта: Torrevigía Residences.', 'سياق المشروع: Torrevigía Residences.', 'Projectcontext: Torrevigía Residences.',
  'Kontekst projektu: Torrevigía Residences.', 'Prosjektkontekst: Torrevigía Residences.', 'Projektkontext: Torrevigía Residences.')
a(156, 'Torrevigía Residences - Ready Apartments, Estepona',
  'Torrevigía Residences - Apartamentos listos, Estepona', 'Torrevigía Residences - Appartements prêts, Estepona',
  'Torrevigía Residences - Bezugsfertige Wohnungen, Estepona', 'Torrevigía Residences - готовые квартиры, Эстепона',
  'Torrevigía Residences - شقق جاهزة، إستيبونا', 'Torrevigía Residences - Instapklare appartementen, Estepona',
  'Torrevigía Residences - Gotowe mieszkania, Estepona', 'Torrevigía Residences - Innflyttingsklare boliger, Estepona',
  'Torrevigía Residences - Inflyttningsklara lägenheter, Estepona')
a(157, 'Torrevigía Residences: Ready Apartments, Estepona',
  'Torrevigía Residences: apartamentos listos para entrar a vivir, Estepona', 'Torrevigía Residences : appartements prêts à habiter, Estepona',
  'Torrevigía Residences: bezugsfertige Wohnungen, Estepona', 'Torrevigía Residences: готовые квартиры, Эстепона',
  'Torrevigía Residences: شقق جاهزة للسكن، إستيبونا', 'Torrevigía Residences: instapklare appartementen, Estepona',
  'Torrevigía Residences: gotowe mieszkania, Estepona', 'Torrevigía Residences: innflyttingsklare leiligheter, Estepona',
  'Torrevigía Residences: inflyttningsklara lägenheter, Estepona')
a(158, 'Ready Apartments, Estepona',
  'Apartamentos listos para entrar a vivir, Estepona', 'Appartements prêts à habiter, Estepona', 'Bezugsfertige Wohnungen, Estepona',
  'Готовые квартиры, Эстепона', 'شقق جاهزة للسكن، إستيبونا', 'Instapklare appartementen, Estepona', 'Gotowe mieszkania, Estepona',
  'Innflyttingsklare leiligheter, Estepona', 'Inflyttningsklara lägenheter, Estepona')

# ---- Norwegian formal address (De) where the memory's most common wording uses "du"; other locales keep the memory.
TM = json.load(open(f'{SP}/tm.json'))
NO_FORMAL = {
    'What Nueva Living verifies before you commit.': 'Hva Nueva Living kontrollerer før De binder Dem.',
    'The homes are listed as ready, so a visit shows the finished building and the view from the floor you are considering.':
        'Boligene er oppført som ferdige, så en visning viser det ferdige bygget og utsikten fra etasjen De vurderer.',
    'Share your details and we will send you the current project information.':
        'Del Deres opplysninger, så sender vi Dem den gjeldende prosjektinformasjonen.',
    'Thank you. We have received your enquiry and will be in touch.': 'Takk. Vi har mottatt Deres henvendelse og tar kontakt med Dem.',
}
for en, no in NO_FORMAL.items():
    T[en] = {**{l: TM[en][l] for l in LOCS if l != 'no'}, 'no': no}

# The Gibraltar figure was dropped from this panel: the measured route on the location map (47 minutes) and the
# brochure ("1 hr") disagree, and the page should not print both. Keyed by text, so it does not depend on todo order.
T['The A-7 is close; the brochure puts Puerto Banús about twenty minutes away.'] = {
    'es': 'La A-7 está cerca; el folleto sitúa Puerto Banús a unos veinte minutos.',
    'fr': 'L’A-7 est proche ; la brochure place Puerto Banús à une vingtaine de minutes.',
    'de': 'Die A-7 ist nah; laut Broschüre liegt Puerto Banús etwa zwanzig Minuten entfernt.',
    'ru': 'Трасса A-7 рядом; по данным брошюры, до Пуэрто-Бануса около двадцати минут.',
    'ar': 'الطريق A-7 قريب؛ ويذكر الكتيّب أن بويرتو بانوس على بعد نحو عشرين دقيقة.',
    'nl': 'De A-7 ligt dichtbij; volgens de brochure ligt Puerto Banús op zo’n twintig minuten.',
    'pl': 'A-7 jest blisko; według broszury do Puerto Banús jest około dwudziestu minut.',
    'no': 'A-7 er like ved; ifølge brosjyren ligger Puerto Banús omkring tjue minutter unna.',
    'sv': 'A-7 ligger nära; enligt broschyren ligger Puerto Banús omkring tjugo minuter bort.',
}

# ---- 6-9-03-A held back (coordinator, 13 Nov 2026): 18 homes, top price EUR 900,000. The new English is derived
# from the strings above by exact substring edits per locale, each asserted, so nothing is re-guessed.
N19 = {'es': ('Diecinueve', 'Dieciocho'), 'fr': ('Dix-neuf', 'Dix-huit'), 'de': ('Neunzehn', 'Achtzehn'),
       'ru': ('Девятнадцать', 'Восемнадцать'), 'nl': ('Negentien', 'Achttien'), 'pl': ('Dziewiętnaście', 'Osiemnaście'),
       'no': ('Nitten', 'Atten'), 'sv': ('Nitton', 'Arton')}
AR_SHE = ('تسع عشرة', 'ثماني عشرة')      # feminine noun (شقة)
AR_HE = ('تسعة عشر', 'ثمانية عشر')       # masculine noun (مسكن)


def derive(old, new, edits):
    src = T[old]
    out = {}
    for l in LOCS:
        v = src[l]
        for a_, b_ in edits.get(l, []):
            assert a_ in v, (new[:40], l, a_)
            v = v.replace(a_, b_)
        out[l] = v
    T[new] = out


def nineteen(old, new, ar, extra=None):
    e = {l: [N19[l]] for l in N19}
    e['ar'] = [ar]
    for l, more in (extra or {}).items():
        e[l] = e.get(l, []) + more
    derive(old, new, e)


def by_start(prefix):
    return [k for k in T if k.startswith(prefix)][0]



def d(o, n): return (by_start(o), n)

o, n = d('Nineteen finished apartments listed', 'Eighteen finished apartments listed as ready to move in, in two phases of one scheme on the hillside at Torrevigía, Estepona, beside Selwo Aventura: two to four bedrooms, 131.05 to 196.08 sqm built, covered terraces of 33 to 50 sqm, a communal pool and access to a residents’ club with a heated indoor pool, gym and saunas.')
nineteen(o, n, AR_SHE)
o, n = d('Nineteen ready apartments at', 'Eighteen ready apartments at Torrevigía, Estepona: two to four bedrooms, 131 to 196 sqm built, covered terraces, a communal pool and a residents’ club with indoor pool.')
nineteen(o, n, AR_SHE)
nineteen('Nineteen homes available / ready to move in', 'Eighteen homes available / ready to move in', AR_HE)
o, n = d('Nineteen finished apartments on the hillside', 'Eighteen finished apartments on the hillside at Torrevigía, Estepona, with covered terraces, a communal pool and a residents’ club with an indoor pool.')
nineteen(o, n, AR_SHE)
nineteen('Nineteen homes, <em>two phases</em>', 'Eighteen homes, <em>two phases</em>', AR_HE)
nineteen('Nineteen finished apartments in two phases of one gated scheme, listed as ready to move in.',
         'Eighteen finished apartments in two phases of one gated scheme, listed as ready to move in.', AR_SHE)
derive('Nineteen: eight in the first phase and eleven in the second.', 'Eighteen: seven in the first phase and eleven in the second.', {
    'es': [('Diecinueve: ocho', 'Dieciocho: siete')], 'fr': [('Dix-neuf : huit', 'Dix-huit : sept')],
    'de': [('Neunzehn: acht', 'Achtzehn: sieben')], 'ru': [('Девятнадцать: восемь', 'Восемнадцать: семь')],
    'ar': [('تسعة عشر: ثمانية', 'ثمانية عشر: سبعة')], 'nl': [('Negentien: acht', 'Achttien: zeven')],
    'pl': [('Dziewiętnaście: osiem', 'Osiemnaście: siedem')], 'no': [('Nitten: åtte', 'Atten: sju')],
    'sv': [('Nitton: åtta', 'Arton: sju')]})
o, n = d('Torrevigía Residences is a gated scheme', 'Torrevigía Residences is a gated scheme of apartment blocks on the hillside at Torrevigía, Estepona, beside Selwo Aventura, built in two phases. The developer’s agent portal lists eighteen homes for sale, seven in the first phase and eleven in the second, all turnkey with immediate delivery.')
derive(o, n, {
    'es': [('diecinueve viviendas, ocho', 'dieciocho viviendas, siete')], 'fr': [('dix-neuf logements, huit', 'dix-huit logements, sept')],
    'de': [('neunzehn Wohnungen an, acht', 'achtzehn Wohnungen an, sieben')], 'ru': [('девятнадцать квартир: восемь', 'восемнадцать квартир: семь')],
    'ar': [('تسعة عشر مسكناً للبيع، ثمانية', 'ثمانية عشر مسكناً للبيع، سبعة')], 'nl': [('negentien woningen aan, acht', 'achttien woningen aan, zeven')],
    'pl': [('dziewiętnaście mieszkań, osiem', 'osiemnaście mieszkań, siedem')], 'no': [('nitten boliger, åtte', 'atten boliger, sju')],
    'sv': [('nitton bostäder, åtta', 'arton bostäder, sju')]})
o, n = d('Fourteen of the nineteen homes', 'Thirteen of the eighteen homes have three bedrooms; three have four bedrooms, and the two on the second floor have two. The table below follows the developer’s list of 13 November 2026.')
derive(o, n, {
    'es': [('Catorce de las diecinueve viviendas tienen tres dormitorios, una de ellas en la tercera planta;', 'Trece de las dieciocho viviendas tienen tres dormitorios;')],
    'fr': [('Quatorze des dix-neuf logements ont trois chambres, dont un au troisième étage ;', 'Treize des dix-huit logements ont trois chambres ;')],
    'de': [('Vierzehn der neunzehn Wohnungen haben drei Schlafzimmer, eine davon im dritten Obergeschoss;', 'Dreizehn der achtzehn Wohnungen haben drei Schlafzimmer;')],
    'ru': [('В четырнадцати из девятнадцати квартир три спальни, одна из них на четвёртом этаже;', 'В тринадцати из восемнадцати квартир три спальни;')],
    'ar': [('أربعة عشر من المساكن التسعة عشر بثلاث غرف نوم، أحدها في الطابق الثالث؛', 'ثلاثة عشر من المساكن الثمانية عشر بثلاث غرف نوم؛')],
    'nl': [('Veertien van de negentien woningen hebben drie slaapkamers, waarvan één op de derde verdieping;', 'Dertien van de achttien woningen hebben drie slaapkamers;')],
    'pl': [('Czternaście z dziewiętnastu mieszkań ma trzy sypialnie, w tym jedno na trzecim piętrze;', 'Trzynaście z osiemnastu mieszkań ma trzy sypialnie;')],
    'no': [('Fjorten av de nitten boligene har tre soverom, én av dem i fjerde etasje;', 'Tretten av de atten boligene har tre soverom;')],
    'sv': [('Fjorton av de nitton bostäderna har tre sovrum, varav en på tredje våningen;', 'Tretton av de arton bostäderna har tre sovrum;')]})
o, n = d('Fourteen homes of 153.46', 'Thirteen homes of 153.46 to 159.85 sqm built, with two bathrooms, the main one en suite.')
derive(o, n, {
    'es': [('Catorce', 'Trece'), ('167,72', '159,85')], 'fr': [('Quatorze', 'Treize'), ('167,72', '159,85')],
    'de': [('Vierzehn', 'Dreizehn'), ('167,72', '159,85')], 'ru': [('Четырнадцать', 'Тринадцать'), ('167,72', '159,85')],
    'ar': [('أربعة عشر', 'ثلاثة عشر'), ('167.72', '159.85')], 'nl': [('Veertien', 'Dertien'), ('167,72', '159,85')],
    'pl': [('Czternaście', 'Trzynaście'), ('167,72', '159,85')], 'no': [('Fjorten', 'Tretten'), ('167,72', '159,85')],
    'sv': [('Fjorton', 'Tretton'), ('167,72', '159,85')]})
o, n = d('Prices from EUR 638,000 to EUR 777,000', 'Prices from EUR 638,000 to EUR 777,000.')
derive(o, n, {
    'es': [(', y 1.762.000 € la única vivienda de la tercera planta.', '.')],
    'fr': [(', et 1 762 000 € pour l’unique logement du troisième étage.', '.')],
    'de': [(', und 1.762.000 € für die einzige Wohnung im dritten Obergeschoss.', '.')],
    'ru': [(', и 1 762 000 € за единственную квартиру на четвёртом этаже.', '.')],
    'ar': [('، و1,762,000 € للمسكن الوحيد في الطابق الثالث.', '.')],
    'nl': [(', en € 1.762.000 voor de enige woning op de derde verdieping.', '.')],
    'pl': [(' oraz 1 762 000 € za jedyne mieszkanie na trzecim piętrze.', '.')],
    'no': [(', og 1 762 000 € for den eneste boligen i fjerde etasje.', '.')],
    'sv': [(', och 1 762 000 € för den enda bostaden på tredje våningen.', '.')]})
o, n = d('From EUR 638,000 to EUR 900,000, and EUR 1,762,000', 'From EUR 638,000 to EUR 900,000, excluding IVA and purchase costs.')
derive(o, n, {
    'es': [(', y 1.762.000 € la única vivienda de la tercera planta,', ',')],
    'fr': [(', et 1 762 000 € pour l’unique logement du troisième étage,', ',')],
    'de': [(' und 1.762.000 € für die einzige Wohnung im dritten Obergeschoss,', ',')],
    'ru': [(' и 1 762 000 € за единственную квартиру на четвёртом этаже,', ',')],
    'ar': [('، و1,762,000 € للمسكن الوحيد في الطابق الثالث،', '،')],
    'nl': [(', en € 1.762.000 voor de enige woning op de derde verdieping,', ',')],
    'pl': [(' oraz 1 762 000 € za jedyne mieszkanie na trzecim piętrze,', ',')],
    'no': [(', og 1 762 000 € for den eneste boligen i fjerde etasje,', ',')],
    'sv': [(', och 1 762 000 € för den enda bostaden på tredje våningen,', ',')]})
derive('19 homes <em>available</em>', '18 homes <em>available</em>', {l: [('19', '18')] for l in LOCS})
o, n = d('Eight homes in the first phase and eleven', 'Seven homes in the first phase and eleven in the second are listed as available, all ready to move in. Availability and prices as listed in the developer’s agent portal on 13 November 2026, reconfirmed before reservation.')
derive(o, n, {
    'es': [('Ocho viviendas', 'Siete viviendas')], 'fr': [('Huit logements', 'Sept logements')],
    'de': [('Acht Wohnungen', 'Sieben Wohnungen')], 'ru': [('Восемь квартир', 'Семь квартир')],
    'ar': [('ثمانية مساكن', 'سبعة مساكن')], 'nl': [('Acht woningen', 'Zeven woningen')],
    'pl': [('Osiem mieszkań', 'Siedem mieszkań')], 'no': [('Åtte boliger', 'Sju boliger')],
    'sv': [('Åtta bostäder', 'Sju bostäder')]})
o, n = d('The price shown is for the home alone', 'The price shown is for the home alone. The developer’s list sells a parking space and a storeroom with most homes for EUR 22,000, and two spaces and a storeroom with four homes for EUR 38,000.')
derive(o, n, {
    'es': [('con cinco viviendas', 'con cuatro viviendas')], 'fr': [('avec cinq logements', 'avec quatre logements')],
    'de': [('mit fünf Wohnungen', 'mit vier Wohnungen')], 'ru': [('с пятью квартирами', 'с четырьмя квартирами')],
    'ar': [('ومع خمسة مساكن', 'ومع أربعة مساكن')], 'nl': [('bij vijf woningen', 'bij vier woningen')],
    'pl': [('z pięcioma mieszkaniami', 'z czterema mieszkaniami')], 'no': [('med fem boliger', 'med fire boliger')],
    'sv': [('med fem bostäder', 'med fyra bostäder')]})
o = by_start('Prices, bedrooms, bathrooms and built and usable areas')
n = 'Prices, bedrooms, bathrooms and built and usable areas are transcribed from the developer’s agent portal list of 13 November 2026; terraces are read from the developer’s unit drawings (V1, June 2023), because the list gives none for the ground-floor and second-floor homes and gives 33.08 sqm where the drawing prints 33.10 sqm. The drawings state areas differently from the list: for the most common three-bedroom home the list gives 153.46 sqm built and 122.14 sqm usable, while the drawing gives 121.95 sqm usable interior, 167.20 sqm built under Decree 218/2005 and 191.36 sqm built including a share of the communal areas. Each price is for the home alone: the list sells one parking space and a storeroom with most homes, adding EUR 22,000, and two spaces and a storeroom with 3-4-0-B, 3-5-02-B, 6-10-0-B and 7-12-0-B, adding EUR 38,000. Prices exclude IVA and purchase costs. The portal says its list is for information only and that prices and units are subject to availability; Nueva Living reconfirms price, status and terms before any reservation.'
END = {'es': 'visita.', 'fr': 'visite.', 'de': 'Besichtigung an.', 'ru': 'просмотра.', 'ar': 'معاينة.', 'nl': 'bezichtiging.',
       'pl': 'wizytą.', 'no': 'visning.', 'sv': 'visning.'}
out = {}
for l in LOCS:
    v = T[o][l]
    i = v.index('6-9-03-A')
    start = max(v.rfind('. ', 0, i), v.rfind('. ', 0, i)) + 2
    end = v.index(END[l], i) + len(END[l]) + 1
    v = v[:start] + v[end:]
    v = v.replace('6-9-03-A, ', '').replace('و6-9-03-A ', '')
    assert '6-9-03-A' not in v and '762' not in v, (l, v[:80])
    out[l] = v
T[n] = out
a_ = 'The drawings'
T[a_] = {'es': 'Los planos', 'fr': 'Les plans', 'de': 'Die Grundrisse', 'ru': 'Планы', 'ar': 'المخططات', 'nl': 'De plattegronden',
         'pl': 'Rzuty', 'no': 'Plantegningene', 'sv': 'Planritningarna'}
T['The drawings we hold are the developer’s project-stage plans of June 2023; we ask for the as-built plan of the home you choose.'] = {
    'es': 'Los planos de que disponemos son los del proyecto del promotor, de junio de 2023; pedimos el plano final de obra de la vivienda que elija.',
    'fr': 'Les plans dont nous disposons sont ceux du projet du promoteur, de juin 2023 ; nous demandons le plan de récolement du logement que vous choisissez.',
    'de': 'Die uns vorliegenden Grundrisse sind die Projektpläne des Bauträgers vom Juni 2023; wir fordern den Bestandsplan der von Ihnen gewählten Wohnung an.',
    'ru': 'Имеющиеся у нас планы — проектные планы застройщика от июня 2023 года; мы запрашиваем исполнительный план выбранной вами квартиры.',
    'ar': 'المخططات التي لدينا هي مخططات المشروع لدى المطوّر بتاريخ يونيو 2023؛ ونطلب المخطط النهائي كما نُفّذ للمسكن الذي تختارونه.',
    'nl': 'De plattegronden die wij hebben zijn de projectplannen van de ontwikkelaar van juni 2023; wij vragen de revisietekening van de woning van uw keuze op.',
    'pl': 'Posiadane przez nas rzuty to projektowe plany dewelopera z czerwca 2023 r.; prosimy o rzut powykonawczy wybranego przez Państwa mieszkania.',
    'no': 'Plantegningene vi har, er utbyggerens prosjekttegninger fra juni 2023; vi ber om som-bygget-tegningen for boligen De velger.',
    'sv': 'Planritningarna vi har är exploatörens projektritningar från juni 2023; vi begär relationsritningen för den bostad ni väljer.'}

missing = [s for s in todo if s not in T and not re.fullmatch(r'(Ground|First|Second|Third) Floor, Block \d+, Portal \d+', s)]
print('translated', len(T), 'still missing', len(missing))
for s in missing:
    print('  ', s[:90])
json.dump(T, open(f'{SP}/tr_t.json', 'w'), ensure_ascii=False, indent=1)
