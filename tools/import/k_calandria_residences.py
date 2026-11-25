# -*- coding: utf-8 -*-
"""Calandria Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E378000}
money, {N55.38} decimal number, {U} the area unit, {T} the tax word.
Argument order in a(): es fr de ru ar nl pl no sv.
    python3 tools/import/k_calandria_residences.py <scratch dir>   (writes <dir>/tr_a.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة',
        'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
T = {}
SLUG = 'calandria-residences'
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


same('Calandria Residences'); same('Calandria'); same('Calandria <em>Residences</em>')
for u in proj['availability']['units']:
    same(u['reference'])

# ---- description, SEO, card ------------------------------------------------------------------

a('.description',
  'Apartamentos de uno a cuatro dormitorios con terraza en Torremolinos, a cinco minutos a pie de la playa de La Carihuela, en un conjunto de 353 viviendas con piscinas exteriores, piscina interior climatizada, gimnasio y espacio de coworking. Cuatro viviendas figuran en la lista de precios del promotor de noviembre de 2026, desde {E378000}.',
  'Appartements d’une à quatre chambres avec terrasse à Torremolinos, à cinq minutes à pied de la plage de La Carihuela, dans un ensemble de 353 logements avec piscines extérieures, piscine intérieure chauffée, salle de sport et espace de coworking. Quatre logements figurent sur la liste de prix du promoteur de novembre 2026, à partir de {E378000}.',
  'Wohnungen mit einem bis vier Schlafzimmern und Terrasse in Torremolinos, fünf Gehminuten vom Strand La Carihuela, in einer Anlage mit 353 Wohnungen, Außenpools, beheiztem Innenpool, Fitnessraum und Coworking-Bereich. Vier Wohnungen stehen auf der Preisliste des Bauträgers vom November 2026, ab {E378000}.',
  'Квартиры с одной–четырьмя спальнями и террасами в Торремолиносе, в пяти минутах ходьбы от пляжа Ла-Каригуэла, в комплексе из 353 квартир с открытыми бассейнами, крытым бассейном с подогревом, тренажёрным залом и коворкингом. В прайс-листе застройщика за ноябрь 2026 года четыре квартиры, от {E378000}.',
  'شقق بغرفة إلى أربع غرف نوم مع تراسات في توريمولينوس، على بُعد خمس دقائق سيرًا من شاطئ لا كاريويلا، ضمن مجمّع من 353 مسكنًا يضم مسابح خارجية ومسبحًا داخليًا مدفأً وصالة رياضية ومساحة للعمل المشترك. تضم قائمة أسعار المطوّر لشهر نوفمبر 2026 أربعة مساكن، ابتداءً من {E378000}.',
  'Appartementen met één tot vier slaapkamers en een terras in Torremolinos, op vijf minuten lopen van het strand van La Carihuela, in een complex van 353 woningen met buitenzwembaden, een verwarmd binnenbad, een fitnessruimte en een coworkingruimte. Vier woningen staan op de prijslijst van de ontwikkelaar van november 2026, vanaf {E378000}.',
  'Mieszkania z jedną do czterech sypialni i tarasem w Torremolinos, pięć minut pieszo od plaży La Carihuela, w zespole 353 lokali z basenami zewnętrznymi, ogrzewanym basenem wewnętrznym, siłownią i strefą coworkingu. W cenniku dewelopera z listopada 2026 roku figurują cztery lokale, od {E378000}.',
  'Leiligheter med ett til fire soverom og terrasse i Torremolinos, fem minutters gange fra stranden La Carihuela, i et anlegg med 353 boliger, utendørs bassenger, oppvarmet innendørsbasseng, treningsrom og coworking-område. Fire boliger står på utbyggerens prisliste fra november 2026, fra {E378000}.',
  'Lägenheter med ett till fyra sovrum och terrass i Torremolinos, fem minuters promenad från stranden La Carihuela, i ett område med 353 bostäder, utomhuspooler, uppvärmd inomhuspool, gym och coworkingyta. Fyra bostäder finns på exploatörens prislista från november 2026, från {E378000}.')
a('.seoDescription',
  'Apartamentos nuevos de uno a cuatro dormitorios en Torremolinos, a cinco minutos a pie de la playa de La Carihuela, con piscinas, gimnasio y coworking. Cuatro en la lista desde {E378000}.',
  'Appartements neufs d’une à quatre chambres à Torremolinos, à cinq minutes à pied de la plage de La Carihuela, avec piscines, salle de sport et coworking. Quatre sur la liste à partir de {E378000}.',
  'Neue Wohnungen mit einem bis vier Schlafzimmern in Torremolinos, fünf Gehminuten vom Strand La Carihuela, mit Pools, Fitnessraum und Coworking. Vier gelistet ab {E378000}.',
  'Новые квартиры с одной–четырьмя спальнями в Торремолиносе, в пяти минутах ходьбы от пляжа Ла-Каригуэла, с бассейнами, тренажёрным залом и коворкингом. Четыре в списке, от {E378000}.',
  'شقق جديدة بغرفة إلى أربع غرف نوم في توريمولينوس، على بُعد خمس دقائق سيرًا من شاطئ لا كاريويلا، مع مسابح وصالة رياضية ومساحة عمل مشترك. أربعة مدرجة ابتداءً من {E378000}.',
  'Nieuwe appartementen met één tot vier slaapkamers in Torremolinos, op vijf minuten lopen van het strand van La Carihuela, met zwembaden, een fitnessruimte en coworking. Vier op de lijst vanaf {E378000}.',
  'Nowe mieszkania z jedną do czterech sypialni w Torremolinos, pięć minut pieszo od plaży La Carihuela, z basenami, siłownią i coworkingiem. Cztery w cenniku od {E378000}.',
  'Nye leiligheter med ett til fire soverom i Torremolinos, fem minutters gange fra stranden La Carihuela, med bassenger, treningsrom og coworking. Fire oppført fra {E378000}.',
  'Nya lägenheter med ett till fyra sovrum i Torremolinos, fem minuters promenad från stranden La Carihuela, med pooler, gym och coworking. Fyra listade från {E378000}.')
a('.twitterDescription',
  'Apartamentos de uno a cuatro dormitorios con terraza cerca de la playa de La Carihuela, Torremolinos, desde {E378000}.',
  'Appartements d’une à quatre chambres avec terrasse près de la plage de La Carihuela, Torremolinos, à partir de {E378000}.',
  'Wohnungen mit einem bis vier Schlafzimmern und Terrasse nahe dem Strand La Carihuela, Torremolinos, ab {E378000}.',
  'Квартиры с одной–четырьмя спальнями и террасами у пляжа Ла-Каригуэла, Торремолинос, от {E378000}.',
  'شقق بغرفة إلى أربع غرف نوم مع تراسات قرب شاطئ لا كاريويلا، توريمولينوس، ابتداءً من {E378000}.',
  'Appartementen met één tot vier slaapkamers en een terras bij het strand van La Carihuela, Torremolinos, vanaf {E378000}.',
  'Mieszkania z jedną do czterech sypialni i tarasem przy plaży La Carihuela, Torremolinos, od {E378000}.',
  'Leiligheter med ett til fire soverom og terrasse nær stranden La Carihuela, Torremolinos, fra {E378000}.',
  'Lägenheter med ett till fyra sovrum och terrass nära stranden La Carihuela, Torremolinos, från {E378000}.')
a('.hero.eyebrow',
  '4 viviendas en la lista de precios', '4 logements sur la liste de prix', '4 Wohnungen auf der Preisliste',
  '4 квартиры в прайс-листе', '4 مساكن في قائمة الأسعار', '4 woningen op de prijslijst',
  '4 lokale w cenniku', '4 boliger på prislisten', '4 bostäder i prislistan')
a('.card.description',
  'Cuatro apartamentos en lista, de uno a cuatro dormitorios y con terraza, en Torremolinos, a cinco minutos a pie de la playa de La Carihuela, con piscinas, gimnasio y coworking, desde {E378000}.',
  'Quatre appartements sur la liste, d’une à quatre chambres avec terrasse, à Torremolinos, à cinq minutes à pied de la plage de La Carihuela, avec piscines, salle de sport et coworking, à partir de {E378000}.',
  'Vier gelistete Wohnungen mit einem bis vier Schlafzimmern und Terrasse in Torremolinos, fünf Gehminuten vom Strand La Carihuela, mit Pools, Fitnessraum und Coworking, ab {E378000}.',
  'Четыре квартиры в списке, с одной–четырьмя спальнями и террасами, в Торремолиносе, в пяти минутах ходьбы от пляжа Ла-Каригуэла, с бассейнами, тренажёрным залом и коворкингом, от {E378000}.',
  'أربع شقق مدرجة بغرفة إلى أربع غرف نوم مع تراسات في توريمولينوس، على بُعد خمس دقائق سيرًا من شاطئ لا كاريويلا، مع مسابح وصالة رياضية ومساحة عمل مشترك، ابتداءً من {E378000}.',
  'Vier appartementen op de lijst met één tot vier slaapkamers en een terras in Torremolinos, op vijf minuten lopen van het strand van La Carihuela, met zwembaden, een fitnessruimte en coworking, vanaf {E378000}.',
  'Cztery mieszkania w cenniku, z jedną do czterech sypialni i tarasem, w Torremolinos, pięć minut pieszo od plaży La Carihuela, z basenami, siłownią i coworkingiem, od {E378000}.',
  'Fire oppførte leiligheter med ett til fire soverom og terrasse i Torremolinos, fem minutters gange fra stranden La Carihuela, med bassenger, treningsrom og coworking, fra {E378000}.',
  'Fyra listade lägenheter med ett till fyra sovrum och terrass i Torremolinos, fem minuters promenad från stranden La Carihuela, med pooler, gym och coworking, från {E378000}.')

# ---- images ----------------------------------------------------------------------------------

a('.images.hero.alt',
  'Vista generada por ordenador del patio al atardecer, con una piscina, tumbonas y sombrillas sobre el césped, palmeras y terrazas ajardinadas que se escalonan en los bloques curvos que lo rodean',
  'Vue de synthèse de la cour au crépuscule, avec une piscine, des transats et des parasols sur la pelouse, des palmiers et des terrasses plantées qui s’étagent sur les bâtiments courbes qui l’entourent',
  'Computergenerierte Ansicht des Innenhofs in der Abenddämmerung, mit Pool, Liegen und Sonnenschirmen auf dem Rasen, Palmen und bepflanzten Terrassen, die an den geschwungenen Gebäuden ringsum ansteigen',
  'Компьютерная визуализация внутреннего двора в сумерках: бассейн, шезлонги и зонтики на газоне, пальмы и озеленённые террасы, уступами поднимающиеся по изогнутым корпусам вокруг',
  'منظر مُنشأ بالحاسوب للفناء عند الغسق، مع مسبح وكراسي استلقاء ومظلات على العشب، ونخيل وتراسات مزروعة تتدرّج على المباني المنحنية المحيطة به',
  'Computergegenereerd beeld van de binnenplaats bij schemering, met een zwembad, ligbedden en parasols op het gazon, palmbomen en beplante terrassen die oplopen langs de gebogen gebouwen eromheen',
  'Wizualizacja komputerowa dziedzińca o zmierzchu: basen, leżaki i parasole na trawniku, palmy i obsadzone zielenią tarasy schodzące kaskadą po otaczających go zaokrąglonych budynkach',
  'Datagenerert bilde av gårdsrommet i skumringen, med basseng, solsenger og parasoller på plenen, palmer og beplantede terrasser som trappes opp på de buede byggene rundt',
  'Datorgenererad bild av innergården i skymningen, med pool, solstolar och parasoller på gräsmattan, palmer och planterade terrasser som trappas upp på de böjda husen runt omkring')
a('.images.architecture.alt',
  'Vista generada por ordenador de una esquina del edificio, con terrazas curvas, barandillas blancas, paneles verticales acanalados y vegetación a lo largo de la cubierta',
  'Vue de synthèse d’un angle du bâtiment, avec des terrasses courbes, des garde-corps blancs, des panneaux verticaux cannelés et de la végétation le long du toit',
  'Computergenerierte Ansicht einer Gebäudeecke mit geschwungenen Terrassen, weißen Geländern, gerippten senkrechten Paneelen und Bepflanzung entlang des Daches',
  'Компьютерная визуализация угла здания: изогнутые террасы, белые ограждения, рифлёные вертикальные панели и зелень вдоль крыши',
  'منظر مُنشأ بالحاسوب لزاوية من المبنى، مع تراسات منحنية ودرابزينات بيضاء وألواح عمودية مضلّعة ونباتات على امتداد السطح',
  'Computergegenereerd beeld van een hoek van het gebouw, met gebogen terrassen, witte balustrades, geribde verticale panelen en beplanting langs het dak',
  'Wizualizacja komputerowa narożnika budynku z zaokrąglonymi tarasami, białymi balustradami, żebrowanymi pionowymi panelami i zielenią wzdłuż dachu',
  'Datagenerert bilde av et hjørne av bygget, med buede terrasser, hvite rekkverk, riflede vertikale paneler og beplantning langs taket',
  'Datorgenererad bild av ett hörn av huset, med böjda terrasser, vita räcken, räfflade vertikala paneler och växtlighet längs taket')
a('.images.lifestyle.alt',
  'Vista generada por ordenador de la piscina interior climatizada, con bancos de piedra con cojines a un lado y una pared acristalada hacia un jardín tropical',
  'Vue de synthèse de la piscine intérieure chauffée, avec des banquettes en pierre garnies de coussins d’un côté et une paroi vitrée sur un jardin tropical',
  'Computergenerierte Ansicht des beheizten Innenpools, mit gepolsterten Steinbänken an einer Seite und einer Glaswand zu einem tropischen Garten',
  'Компьютерная визуализация крытого бассейна с подогревом: каменные скамьи с подушками вдоль одной стороны и стеклянная стена в тропический сад',
  'منظر مُنشأ بالحاسوب للمسبح الداخلي المدفأ، مع مقاعد حجرية مبطّنة بالوسائد على أحد جانبيه وجدار زجاجي يطلّ على حديقة استوائية',
  'Computergegenereerd beeld van het verwarmde binnenbad, met stenen banken met kussens aan één kant en een glazen wand naar een tropische tuin',
  'Wizualizacja komputerowa ogrzewanego basenu wewnętrznego z kamiennymi ławami z poduszkami wzdłuż jednego boku i przeszkloną ścianą od strony tropikalnego ogrodu',
  'Datagenerert bilde av det oppvarmede innendørsbassenget, med steinbenker med puter langs den ene siden og en glassvegg mot en tropisk hage',
  'Datorgenererad bild av den uppvärmda inomhuspoolen, med stenbänkar med dynor längs ena sidan och en glasvägg mot en tropisk trädgård')
a('.images.privateViewing.alt',
  'Vista generada por ordenador de una amplia terraza con un sofá curvo, una mesa baja y una mesa de comedor, con vistas al mar al atardecer',
  'Vue de synthèse d’une grande terrasse avec un canapé courbe, une table basse et une table à manger, face à la mer au coucher du soleil',
  'Computergenerierte Ansicht einer großen Terrasse mit geschwungenem Sofa, Couchtisch und Esstisch, mit Blick auf das Meer bei Sonnenuntergang',
  'Компьютерная визуализация большой террасы с изогнутым диваном, журнальным и обеденным столами, с видом на море на закате',
  'منظر مُنشأ بالحاسوب لتراس واسع مع أريكة منحنية وطاولة منخفضة وطاولة طعام، يطلّ على البحر عند الغروب',
  'Computergegenereerd beeld van een groot terras met een gebogen bank, een salontafel en een eettafel, met uitzicht op zee bij zonsondergang',
  'Wizualizacja komputerowa dużego tarasu z zaokrągloną sofą, niskim stolikiem i stołem jadalnym, z widokiem na morze o zachodzie słońca',
  'Datagenerert bilde av en stor terrasse med en buet sofa, et lavt bord og et spisebord, med utsikt over havet i solnedgang',
  'Datorgenererad bild av en stor terrass med en böjd soffa, ett soffbord och ett matbord, med utsikt över havet i solnedgången')

# ---- media -----------------------------------------------------------------------------------

a('.media.copy',
  'Vistas generadas por ordenador del edificio, las piscinas, el gimnasio y los interiores, del dosier de imágenes del promotor, y los planos de las cuatro viviendas de la lista de precios.',
  'Vues de synthèse du bâtiment, des piscines, de la salle de sport et des intérieurs, issues des images du promoteur, et les plans des quatre logements de la liste de prix.',
  'Computergenerierte Ansichten des Gebäudes, der Pools, des Fitnessraums und der Innenräume aus dem Bildmaterial des Bauträgers sowie die Grundrisse der vier Wohnungen auf der Preisliste.',
  'Компьютерные визуализации здания, бассейнов, тренажёрного зала и интерьеров из материалов застройщика, а также планировки четырёх квартир из прайс-листа.',
  'مناظر مُنشأة بالحاسوب للمبنى والمسابح والصالة الرياضية والتصميمات الداخلية من مجموعة صور المطوّر، ومخططات المساكن الأربعة المدرجة في قائمة الأسعار.',
  'Computergegenereerde beelden van het gebouw, de zwembaden, de fitnessruimte en de interieurs uit het beeldmateriaal van de ontwikkelaar, en de plattegronden van de vier woningen op de prijslijst.',
  'Wizualizacje komputerowe budynku, basenów, siłowni i wnętrz z materiałów dewelopera oraz rzuty czterech lokali z cennika.',
  'Datagenererte bilder av bygget, bassengene, treningsrommet og interiørene fra utbyggerens bildemateriale, og plantegningene til de fire boligene på prislisten.',
  'Datorgenererade bilder av huset, poolerna, gymmet och interiörerna ur exploatörens bildmaterial, och planritningarna till de fyra bostäderna i prislistan.')
a('.media.note',
  'Las imágenes son ilustraciones generadas por ordenador, no fotografías del edificio terminado; la vista aérea inserta la promoción en una fotografía real. El folleto indica que sus imágenes son orientativas e incluyen opciones, mobiliario, decoración y paisajismo no incluidos en el precio. Los planos son los del promotor, recortados de sus láminas para que no quede ningún logotipo ni nombre del proyecto; los nombres de las estancias están en español, y los planos indican que son informativos y no contractuales, que sus superficies son aproximadas y pueden variar por razones técnicas, legales o de ejecución, y que el mobiliario no forma parte de la venta.',
  'Les visuels sont des illustrations de synthèse, pas des photographies du bâtiment achevé ; la vue aérienne insère le projet dans une photographie réelle. La brochure précise que ses images sont indicatives et montrent des options, du mobilier, de la décoration et des aménagements paysagers non compris dans le prix. Les plans sont ceux du promoteur, découpés de leurs planches pour qu’il n’y reste aucun logo ni nom de projet ; les pièces sont nommées en espagnol, et les plans indiquent qu’ils sont informatifs et non contractuels, que leurs surfaces sont approximatives et peuvent varier pour des raisons techniques, juridiques ou d’exécution, et que le mobilier ne fait pas partie de la vente.',
  'Die Bilder sind computergenerierte Illustrationen, keine Fotos des fertigen Gebäudes; die Luftansicht setzt das Projekt in ein echtes Foto. Laut Broschüre dienen die Bilder nur zur Orientierung und zeigen Optionen, Möbel, Dekoration und Bepflanzung, die nicht im Preis enthalten sind. Die Grundrisse sind die des Bauträgers, aus ihren Blättern ausgeschnitten, sodass kein Logo und kein Projektname bleibt; die Räume sind auf Spanisch beschriftet, und die Pläne sind laut eigener Angabe unverbindlich und nicht Vertragsbestandteil, ihre Flächen sind ungefähr und können sich aus technischen, rechtlichen oder baulichen Gründen ändern, und die Möblierung ist nicht Teil des Verkaufs.',
  'Изображения — компьютерные иллюстрации, а не фотографии готового здания; на аэроснимке проект вписан в реальную фотографию. В буклете сказано, что изображения носят ориентировочный характер и показывают опции, мебель, декор и озеленение, не входящие в цену. Планировки — застройщика, вырезанные из листов так, чтобы не осталось ни логотипа, ни названия проекта; помещения подписаны по-испански, а сами планы указывают, что носят информационный, а не договорный характер, что площади приблизительны и могут меняться по техническим, юридическим или строительным причинам и что мебель не входит в продажу.',
  'الصور رسوم توضيحية مُنشأة بالحاسوب وليست صورًا للمبنى المكتمل؛ ويضع المنظر الجوي المشروع داخل صورة حقيقية. ويذكر الكتيّب أن صوره إرشادية وتُظهر خيارات وأثاثًا وديكورًا وتنسيقًا للحدائق غير مشمولة في السعر. أما المخططات فهي مخططات المطوّر، مقتطعة من لوحاتها بحيث لا يبقى أي شعار أو اسم للمشروع؛ وأسماء الغرف بالإسبانية، وتذكر المخططات أنها إعلامية وغير تعاقدية، وأن مساحاتها تقريبية وقد تتغيّر لأسباب فنية أو قانونية أو تنفيذية، وأن الأثاث ليس جزءًا من البيع.',
  'De beelden zijn computergegenereerde illustraties, geen foto’s van het afgewerkte gebouw; het luchtbeeld plaatst het project in een echte foto. Volgens de brochure zijn de beelden indicatief en tonen ze opties, meubilair, decoratie en beplanting die niet in de prijs zijn inbegrepen. De plattegronden zijn die van de ontwikkelaar, uit hun bladen geknipt zodat er geen logo of projectnaam overblijft; de ruimten staan er in het Spaans op, en volgens de plannen zelf zijn ze informatief en niet contractueel, zijn de oppervlakten bij benadering en kunnen ze om technische, juridische of uitvoeringsredenen wijzigen, en hoort het meubilair niet bij de verkoop.',
  'Wizualizacje są ilustracjami komputerowymi, a nie zdjęciami gotowego budynku; widok z lotu ptaka osadza inwestycję w prawdziwej fotografii. Broszura zaznacza, że jej obrazy mają charakter orientacyjny i pokazują opcje, meble, dekoracje oraz zieleń nieujęte w cenie. Rzuty pochodzą od dewelopera i zostały wycięte z arkuszy tak, by nie pozostało żadne logo ani nazwa projektu; pomieszczenia opisano po hiszpańsku, a same rzuty zastrzegają, że mają charakter informacyjny, a nie umowny, że ich powierzchnie są przybliżone i mogą się zmienić z przyczyn technicznych, prawnych lub wykonawczych oraz że meble nie są przedmiotem sprzedaży.',
  'Bildene er datagenererte illustrasjoner, ikke fotografier av det ferdige bygget; flybildet setter prosjektet inn i et ekte fotografi. Brosjyren sier at bildene er veiledende og viser tilvalg, møbler, dekor og beplantning som ikke er inkludert i prisen. Plantegningene er utbyggerens, klippet ut av arkene slik at ingen logo eller prosjektnavn står igjen; rommene er navngitt på spansk, og tegningene sier selv at de er informative og ikke kontraktsmessige, at arealene er omtrentlige og kan endres av tekniske, juridiske eller byggetekniske grunner, og at møblene ikke inngår i salget.',
  'Bilderna är datorgenererade illustrationer, inte fotografier av det färdiga huset; flygbilden placerar projektet i ett verkligt fotografi. Enligt broschyren är bilderna vägledande och visar tillval, möbler, dekor och plantering som inte ingår i priset. Planritningarna är exploatörens, utklippta ur sina blad så att ingen logotyp eller projektnamn finns kvar; rummen är namngivna på spanska, och ritningarna anger själva att de är informativa och inte avtalsgrundande, att ytorna är ungefärliga och kan ändras av tekniska, juridiska eller byggtekniska skäl, och att möblerna inte ingår i försäljningen.')
a('.media.items[1].alt',
  'Imagen generada por ordenador de la promoción insertada en una fotografía aérea al anochecer: un edificio largo y curvo con una piscina en su patio junto a una avenida principal, las calles de Torremolinos alrededor y, al fondo, el puerto deportivo y el mar',
  'Image de synthèse du projet insérée dans une photographie aérienne au crépuscule : un long bâtiment courbe avec une piscine dans sa cour, au bord d’une grande avenue, les rues de Torremolinos autour et, au loin, la marina et la mer',
  'Computergeneriertes Bild des Projekts in einem Luftfoto in der Abenddämmerung: ein langes, geschwungenes Gebäude mit Pool im Innenhof an einer Hauptstraße, ringsum die Straßen von Torremolinos, dahinter der Jachthafen und das Meer',
  'Компьютерное изображение проекта, вписанное в аэрофотоснимок в сумерках: длинное изогнутое здание с бассейном во дворе у главной улицы, вокруг улицы Торремолиноса, вдали марина и море',
  'صورة مُنشأة بالحاسوب للمشروع داخل صورة جوية عند الغسق: مبنى طويل منحنٍ مع مسبح في فنائه بجوار طريق رئيسي، وشوارع توريمولينوس من حوله، وفي الأفق المرسى والبحر',
  'Computergegenereerd beeld van het project in een luchtfoto bij schemering: een lang, gebogen gebouw met een zwembad op de binnenplaats aan een hoofdweg, de straten van Torremolinos eromheen en daarachter de jachthaven en de zee',
  'Komputerowy obraz inwestycji wpisany w zdjęcie lotnicze o zmierzchu: długi, zaokrąglony budynek z basenem na dziedzińcu przy głównej ulicy, wokół ulice Torremolinos, w oddali przystań jachtowa i morze',
  'Datagenerert bilde av prosjektet satt inn i et flyfoto i skumringen: et langt, buet bygg med basseng i gårdsrommet ved en hovedvei, gatene i Torremolinos rundt og marinaen og havet i bakgrunnen',
  'Datorgenererad bild av projektet infogad i ett flygfoto i skymningen: ett långt, böjt hus med pool på innergården vid en huvudgata, Torremolinos gator runt omkring och marinan och havet i bakgrunden')
a('.media.items[1].caption',
  'La parcela, hacia el puerto deportivo', 'Le site, vers la marina', 'Das Grundstück, Blick zum Jachthafen',
  'Участок, вид в сторону марины', 'الموقع باتجاه المرسى', 'Het terrein, richting de jachthaven',
  'Działka, widok w stronę przystani', 'Tomten, mot marinaen', 'Tomten, mot marinan')
a('.media.items[2].caption',
  'El edificio desde la esquina', 'Le bâtiment vu de l’angle de la rue', 'Das Gebäude von der Straßenecke',
  'Здание с угла улицы', 'المبنى من زاوية الشارع', 'Het gebouw vanaf de straathoek',
  'Budynek od strony narożnika ulicy', 'Bygget sett fra gatehjørnet', 'Huset från gathörnet')
a('.media.items[3].alt',
  'Vista generada por ordenador del edificio a lo largo de una avenida con palmeras, con seis plantas de terrazas curvas y ventanas iluminadas',
  'Vue de synthèse du bâtiment le long d’une avenue bordée de palmiers, avec six niveaux de terrasses courbes et des fenêtres éclairées',
  'Computergenerierte Ansicht des Gebäudes entlang einer Palmenallee, mit sechs Geschossen geschwungener Terrassen und beleuchteten Fenstern',
  'Компьютерная визуализация здания вдоль пальмовой аллеи: шесть этажей изогнутых террас и освещённые окна',
  'منظر مُنشأ بالحاسوب للمبنى على امتداد جادة تصطف فيها أشجار النخيل، بستة طوابق من التراسات المنحنية ونوافذ مضاءة',
  'Computergegenereerd beeld van het gebouw langs een laan met palmbomen, met zes verdiepingen gebogen terrassen en verlichte ramen',
  'Wizualizacja komputerowa budynku wzdłuż alei z palmami, z sześcioma kondygnacjami zaokrąglonych tarasów i oświetlonymi oknami',
  'Datagenerert bilde av bygget langs en palmeallé, med seks etasjer med buede terrasser og opplyste vinduer',
  'Datorgenererad bild av huset längs en palmkantad aveny, med sex våningar böjda terrasser och upplysta fönster')
a('.media.items[3].caption',
  'El edificio a lo largo de la avenida', 'Le bâtiment le long de l’avenue', 'Das Gebäude entlang der Allee',
  'Здание вдоль проспекта', 'المبنى على امتداد الجادة', 'Het gebouw langs de laan',
  'Budynek wzdłuż alei', 'Bygget langs avenyen', 'Huset längs avenyn')
a('.media.items[4].alt',
  'Vista generada por ordenador de una piscina sobre una tarima de madera con tumbonas y sombrillas, con vistas al mar y a la costa tras una barandilla de vidrio',
  'Vue de synthèse d’une piscine sur un deck en bois avec transats et parasols, face à la mer et à la côte derrière un garde-corps vitré',
  'Computergenerierte Ansicht eines Pools auf einem Holzdeck mit Liegen und Sonnenschirmen, mit Blick über ein Glasgeländer auf das Meer und die Küste',
  'Компьютерная визуализация бассейна на деревянном настиле с шезлонгами и зонтиками, с видом на море и побережье за стеклянным ограждением',
  'منظر مُنشأ بالحاسوب لمسبح على سطح خشبي مع كراسي استلقاء ومظلات، يطلّ على البحر والساحل من وراء درابزين زجاجي',
  'Computergegenereerd beeld van een zwembad op een houten vlonder met ligbedden en parasols, met uitzicht over een glazen balustrade op de zee en de kust',
  'Wizualizacja komputerowa basenu na drewnianym tarasie z leżakami i parasolami, z widokiem przez szklaną balustradę na morze i wybrzeże',
  'Datagenerert bilde av et basseng på et tredekk med solsenger og parasoller, med utsikt over et glassrekkverk mot havet og kysten',
  'Datorgenererad bild av en pool på ett trädäck med solstolar och parasoller, med utsikt över ett glasräcke mot havet och kusten')
a('.media.items[4].caption',
  'Una tarima con piscina frente al mar', 'Un deck avec piscine face à la mer', 'Ein Pooldeck mit Meerblick',
  'Площадка с бассейном и видом на море', 'سطح مسبح يطلّ على البحر', 'Een zwembadterras met zicht op zee',
  'Taras z basenem z widokiem na morze', 'Et bassengdekk med utsikt mot havet', 'Ett pooldäck med utsikt mot havet')
a('.media.items[6].alt',
  'Salón diáfano generado por ordenador con cocina blanca e isla efecto mármol, un sofá, una mesa de comedor y una ventana al mar',
  'Séjour ouvert en image de synthèse avec une cuisine blanche et un îlot effet marbre, un canapé, une table à manger et une fenêtre sur la mer',
  'Computergenerierter offener Wohnbereich mit weißer Küche und Kochinsel in Marmoroptik, Sofa, Esstisch und Fenster zum Meer',
  'Компьютерная визуализация открытой гостиной с белой кухней и островом под мрамор, диваном, обеденным столом и окном на море',
  'غرفة معيشة مفتوحة مُنشأة بالحاسوب مع مطبخ أبيض وجزيرة بمظهر الرخام وأريكة وطاولة طعام ونافذة تطلّ على البحر',
  'Computergegenereerde open woonkamer met een witte keuken en een kookeiland in marmerlook, een bank, een eettafel en een raam naar zee',
  'Wizualizacja komputerowa otwartego salonu z białą kuchnią i wyspą imitującą marmur, sofą, stołem jadalnym i oknem na morze',
  'Datagenerert åpen stue med hvitt kjøkken og kjøkkenøy i marmorlook, sofa, spisebord og et vindu mot havet',
  'Datorgenererat öppet vardagsrum med vitt kök och köksö i marmorlook, soffa, matbord och ett fönster mot havet')
a('.media.items[7].alt',
  'Salón generado por ordenador con un sofá curvo, mesas de centro redondas, una pared de cocina en madera y una puerta de vidrio a una terraza con las montañas al fondo',
  'Séjour en image de synthèse avec un canapé courbe, des tables basses rondes, un mur de cuisine en bois et une porte vitrée sur une terrasse avec les collines au loin',
  'Computergenerierter Wohnraum mit geschwungenem Sofa, runden Couchtischen, einer Küchenwand in Holz und einer Glastür zu einer Terrasse mit Blick auf die Hügel',
  'Компьютерная визуализация гостиной с изогнутым диваном, круглыми журнальными столиками, деревянной кухонной стеной и стеклянной дверью на террасу с видом на холмы',
  'غرفة معيشة مُنشأة بالحاسوب مع أريكة منحنية وطاولات قهوة مستديرة وجدار مطبخ خشبي وباب زجاجي يفضي إلى تراس تظهر خلفه التلال',
  'Computergegenereerde woonkamer met een gebogen bank, ronde salontafels, een houten keukenwand en een glazen deur naar een terras met de heuvels erachter',
  'Wizualizacja komputerowa salonu z zaokrągloną sofą, okrągłymi stolikami, drewnianą ścianą kuchenną i szklanymi drzwiami na taras z widokiem na wzgórza',
  'Datagenerert stue med buet sofa, runde salongbord, en kjøkkenvegg i tre og en glassdør til en terrasse med åsene i bakgrunnen',
  'Datorgenererat vardagsrum med böjd soffa, runda soffbord, en köksvägg i trä och en glasdörr till en terrass med kullarna i bakgrunden')
a('.media.items[8].alt',
  'Salón comedor generado por ordenador con una mesa redonda efecto mármol, un sofá curvo y una puerta de vidrio a una terraza frente a las montañas',
  'Séjour et espace repas en image de synthèse avec une table ronde effet marbre, un canapé courbe et une porte vitrée sur une terrasse face aux collines',
  'Computergenerierter Wohn- und Essbereich mit rundem Tisch in Marmoroptik, geschwungenem Sofa und einer Glastür zu einer Terrasse mit Blick auf die Hügel',
  'Компьютерная визуализация гостиной-столовой с круглым столом под мрамор, изогнутым диваном и стеклянной дверью на террасу с видом на холмы',
  'غرفة معيشة وطعام مُنشأة بالحاسوب مع طاولة مستديرة بمظهر الرخام وأريكة منحنية وباب زجاجي يفضي إلى تراس يطلّ على التلال',
  'Computergegenereerde woon-eetkamer met een ronde tafel in marmerlook, een gebogen bank en een glazen deur naar een terras met zicht op de heuvels',
  'Wizualizacja komputerowa salonu z jadalnią: okrągły stół imitujący marmur, zaokrąglona sofa i szklane drzwi na taras z widokiem na wzgórza',
  'Datagenerert stue og spiseplass med rundt bord i marmorlook, buet sofa og en glassdør til en terrasse mot åsene',
  'Datorgenererat vardagsrum med matplats, ett runt bord i marmorlook, en böjd soffa och en glasdörr till en terrass mot kullarna')
a('.media.items[9].alt',
  'Dormitorio principal generado por ordenador con cama doble, una pared de armarios y un lavabo de piedra abierto al dormitorio, junto a una puerta de vidrio a una terraza',
  'Chambre principale en image de synthèse avec un lit double, un mur de placards et une vasque en pierre ouverte sur la chambre, à côté d’une porte vitrée sur une terrasse',
  'Computergeneriertes Hauptschlafzimmer mit Doppelbett, einer Schrankwand und einem zum Raum offenen Waschtisch mit Steinbecken, neben einer Glastür zu einer Terrasse',
  'Компьютерная визуализация главной спальни с двуспальной кроватью, стеной шкафов и открытой в комнату раковиной из камня рядом со стеклянной дверью на террасу',
  'غرفة نوم رئيسية مُنشأة بالحاسوب مع سرير مزدوج وجدار من الخزائن ومغسلة حجرية مفتوحة على الغرفة، بجانب باب زجاجي يفضي إلى تراس',
  'Computergegenereerde hoofdslaapkamer met een tweepersoonsbed, een kastenwand en een wastafel met stenen bak die open is naar de kamer, naast een glazen deur naar een terras',
  'Wizualizacja komputerowa sypialni głównej z podwójnym łóżkiem, ścianą szaf i otwartą na pokój umywalką z kamienną misą, obok szklanych drzwi na taras',
  'Datagenerert hovedsoverom med dobbeltseng, en vegg med garderobeskap og en servant med steinvask åpen mot rommet, ved en glassdør til en terrasse',
  'Datorgenererat huvudsovrum med dubbelsäng, en garderobsvägg och ett tvättställ med stenhandfat öppet mot rummet, vid en glasdörr till en terrass')
a('.media.items[10].alt',
  'Dormitorio generado por ordenador con cama doble sobre una tarima de madera, una pared de madera y una puerta de vidrio a un balcón con las montañas al fondo',
  'Chambre en image de synthèse avec un lit double sur une estrade en bois, un mur en bois et une porte vitrée sur un balcon avec les collines au loin',
  'Computergeneriertes Schlafzimmer mit Doppelbett auf einem Holzpodest, einer Holzwand und einer Glastür zu einem Balkon mit Blick auf die Hügel',
  'Компьютерная визуализация спальни с двуспальной кроватью на деревянном подиуме, деревянной стеной и стеклянной дверью на балкон с видом на холмы',
  'غرفة نوم مُنشأة بالحاسوب مع سرير مزدوج على منصة خشبية وجدار خشبي وباب زجاجي يفضي إلى شرفة تظهر خلفها التلال',
  'Computergegenereerde slaapkamer met een tweepersoonsbed op een houten podium, een houten wand en een glazen deur naar een balkon met de heuvels erachter',
  'Wizualizacja komputerowa sypialni z podwójnym łóżkiem na drewnianym podeście, drewnianą ścianą i szklanymi drzwiami na balkon z widokiem na wzgórza',
  'Datagenerert soverom med dobbeltseng på et tregulv i opphøyd nivå, en trevegg og en glassdør til en balkong med åsene i bakgrunnen',
  'Datorgenererat sovrum med dubbelsäng på en träpodest, en trävägg och en glasdörr till en balkong med kullarna i bakgrunden')
a('.media.items[11].alt',
  'Dormitorio generado por ordenador con dos camas individuales, una alfombra redonda y una puerta de vidrio a una terraza',
  'Chambre en image de synthèse avec deux lits simples, un tapis rond et une porte vitrée sur une terrasse',
  'Computergeneriertes Schlafzimmer mit zwei Einzelbetten, einem runden Teppich und einer Glastür zu einer Terrasse',
  'Компьютерная визуализация спальни с двумя односпальными кроватями, круглым ковром и стеклянной дверью на террасу',
  'غرفة نوم مُنشأة بالحاسوب مع سريرين مفردين وسجادة مستديرة وباب زجاجي يفضي إلى تراس',
  'Computergegenereerde slaapkamer met twee eenpersoonsbedden, een rond vloerkleed en een glazen deur naar een terras',
  'Wizualizacja komputerowa sypialni z dwoma pojedynczymi łóżkami, okrągłym dywanem i szklanymi drzwiami na taras',
  'Datagenerert soverom med to enkeltsenger, et rundt teppe og en glassdør til en terrasse',
  'Datorgenererat sovrum med två enkelsängar, en rund matta och en glasdörr till en terrass')
a('.media.items[12].alt',
  'Dormitorio generado por ordenador con una cama individual, un escritorio y una puerta de vidrio a un balcón con las montañas al fondo',
  'Chambre en image de synthèse avec un lit simple, un bureau et une porte vitrée sur un balcon avec les collines au loin',
  'Computergeneriertes Schlafzimmer mit Einzelbett, Schreibtisch und einer Glastür zu einem Balkon mit Blick auf die Hügel',
  'Компьютерная визуализация спальни с односпальной кроватью, письменным столом и стеклянной дверью на балкон с видом на холмы',
  'غرفة نوم مُنشأة بالحاسوب مع سرير مفرد ومكتب وباب زجاجي يفضي إلى شرفة تظهر خلفها التلال',
  'Computergegenereerde slaapkamer met een eenpersoonsbed, een bureau en een glazen deur naar een balkon met de heuvels erachter',
  'Wizualizacja komputerowa sypialni z pojedynczym łóżkiem, biurkiem i szklanymi drzwiami na balkon z widokiem na wzgórza',
  'Datagenerert soverom med enkeltseng, skrivebord og en glassdør til en balkong med åsene i bakgrunnen',
  'Datorgenererat sovrum med enkelsäng, skrivbord och en glasdörr till en balkong med kullarna i bakgrunden')
a('.media.items[12].caption',
  'Dormitorio con escritorio', 'Chambre avec bureau', 'Schlafzimmer mit Schreibtisch', 'Спальня с письменным столом',
  'غرفة نوم مع مكتب', 'Slaapkamer met bureau', 'Sypialnia z biurkiem', 'Soverom med skrivebord', 'Sovrum med skrivbord')
a('.media.items[14].alt',
  'Vista generada por ordenador del gimnasio, con máquinas de musculación, cintas de correr, una zona de pesas libres y esterillas, y ventanas al jardín',
  'Vue de synthèse de la salle de sport, avec des appareils de musculation, des tapis de course, un espace de poids libres et des tapis de sol, et des fenêtres sur le jardin',
  'Computergenerierte Ansicht des Fitnessraums mit Kraftgeräten, Laufbändern, einem Freihantelbereich und Matten sowie Fenstern zum Garten',
  'Компьютерная визуализация тренажёрного зала: силовые тренажёры, беговые дорожки, зона свободных весов, коврики и окна в сад',
  'منظر مُنشأ بالحاسوب للصالة الرياضية، مع أجهزة لتمارين القوة وأجهزة مشي ومنطقة للأوزان الحرة وحصائر، ونوافذ تطلّ على الحديقة',
  'Computergegenereerd beeld van de fitnessruimte, met krachttoestellen, loopbanden, een zone voor losse gewichten en matten, en ramen naar de tuin',
  'Wizualizacja komputerowa siłowni z maszynami do ćwiczeń siłowych, bieżniami, strefą wolnych ciężarów i matami oraz oknami na ogród',
  'Datagenerert bilde av treningsrommet, med styrkeapparater, tredemøller, et område for frivekter og matter, og vinduer mot hagen',
  'Datorgenererad bild av gymmet, med styrkemaskiner, löpband, en yta för fria vikter och mattor, och fönster mot trädgården')
a('.media.items[15].alt',
  'Vista generada por ordenador de un portal con una pared de buzones revestida de madera, paredes de piedra y una pared acristalada hacia el jardín',
  'Vue de synthèse d’un hall d’entrée avec un mur de boîtes aux lettres habillé de bois, des murs en pierre et une paroi vitrée sur le jardin',
  'Computergenerierte Ansicht einer Eingangshalle mit holzverkleideter Briefkastenwand, Steinwänden und einer Glaswand zum Garten',
  'Компьютерная визуализация входного холла: стена почтовых ящиков с деревянной облицовкой, каменные стены и стеклянная стена в сад',
  'منظر مُنشأ بالحاسوب لبهو مدخل مع جدار صناديق بريد مكسو بالخشب وجدران حجرية وجدار زجاجي يطلّ على الحديقة',
  'Computergegenereerd beeld van een inkomhal met een met hout beklede wand met brievenbussen, stenen muren en een glazen wand naar de tuin',
  'Wizualizacja komputerowa holu wejściowego ze ścianą skrzynek pocztowych obłożoną drewnem, kamiennymi ścianami i przeszkloną ścianą od strony ogrodu',
  'Datagenerert bilde av en inngangshall med en trekledd vegg med postkasser, steinvegger og en glassvegg mot hagen',
  'Datorgenererad bild av en entréhall med en träklädd vägg med brevlådor, stenväggar och en glasvägg mot trädgården')
a('.media.items[15].caption',
  'Un portal', 'Un hall d’entrée', 'Eine Eingangshalle', 'Входной холл', 'بهو مدخل', 'Een inkomhal', 'Hol wejściowy',
  'En inngangshall', 'En entréhall')
for i, u in zip(range(16, 20), proj['availability']['units']):
    r = u['reference']
    a(f'.media.items[{i}].alt', f'Plano de la vivienda {r}', f'Plan du logement {r}', f'Grundriss der Wohnung {r}',
      f'Планировка квартиры {r}', f'مخطط المسكن {r}', f'Plattegrond van woning {r}', f'Rzut lokalu {r}',
      f'Plantegning av bolig {r}', f'Planritning för bostad {r}')
    a(f'.media.items[{i}].caption', f'Vivienda {r}', f'Logement {r}', f'Wohnung {r}', f'Квартира {r}',
      f'المسكن {r}', f'Woning {r}', f'Lokal {r}', f'Bolig {r}', f'Bostad {r}')

# ---- overview, why ---------------------------------------------------------------------------

a('.overview.headlineHtml',
  '4 viviendas en la <em>lista de precios</em>', '4 logements sur la <em>liste de prix</em>', '4 Wohnungen auf der <em>Preisliste</em>',
  '4 квартиры в <em>прайс-листе</em>', '4 مساكن في <em>قائمة الأسعار</em>', '4 woningen op de <em>prijslijst</em>',
  '4 lokale w <em>cenniku</em>', '4 boliger på <em>prislisten</em>', '4 bostäder i <em>prislistan</em>')
a('.overview.copy[0]',
  'El folleto del promotor presenta un conjunto contemporáneo de apartamentos con grandes ventanales y amplias terrazas en Torremolinos, a unos cinco minutos a pie de la playa de La Carihuela y, según sus datos, a menos de diez minutos en coche del aeropuerto de Málaga. La página del portal habla de 353 viviendas en total, de uno a cuatro dormitorios.',
  'La brochure du promoteur présente un ensemble contemporain d’appartements aux grandes baies vitrées et aux terrasses généreuses à Torremolinos, à environ cinq minutes à pied de la plage de La Carihuela et, selon elle, à moins de dix minutes en voiture de l’aéroport de Malaga. La page du portail annonce 353 logements au total, d’une à quatre chambres.',
  'Die Broschüre des Bauträgers zeigt eine zeitgemäße Wohnanlage mit großen Fenstern und großzügigen Terrassen in Torremolinos, etwa fünf Gehminuten vom Strand La Carihuela und nach ihren Angaben weniger als zehn Autominuten vom Flughafen Malaga. Die Portalseite nennt insgesamt 353 Wohnungen mit einem bis vier Schlafzimmern.',
  'Буклет застройщика представляет современный комплекс квартир с большими окнами и просторными террасами в Торремолиносе, примерно в пяти минутах ходьбы от пляжа Ла-Каригуэла и, по его данным, менее чем в десяти минутах езды от аэропорта Малаги. На странице портала указано 353 квартиры в общей сложности, с одной–четырьмя спальнями.',
  'يقدّم كتيّب المطوّر مجمّعًا معاصرًا من الشقق بنوافذ كبيرة وتراسات واسعة في توريمولينوس، على بُعد نحو خمس دقائق سيرًا من شاطئ لا كاريويلا، وبحسب أرقامه على أقل من عشر دقائق بالسيارة من مطار مالقة. وتذكر صفحة البوابة 353 مسكنًا في المجموع، بغرفة إلى أربع غرف نوم.',
  'De brochure van de ontwikkelaar toont een eigentijds complex van appartementen met grote ramen en ruime terrassen in Torremolinos, op ongeveer vijf minuten lopen van het strand van La Carihuela en, volgens de brochure, op minder dan tien minuten rijden van de luchthaven van Málaga. De portaalpagina noemt in totaal 353 woningen, met één tot vier slaapkamers.',
  'Broszura dewelopera przedstawia współczesny zespół mieszkań z dużymi oknami i obszernymi tarasami w Torremolinos, około pięciu minut pieszo od plaży La Carihuela i, według niej, niecałe dziesięć minut samochodem od lotniska w Maladze. Strona portalu podaje łącznie 353 lokale, z jedną do czterech sypialni.',
  'Utbyggerens brosjyre presenterer et moderne anlegg med leiligheter med store vinduer og romslige terrasser i Torremolinos, rundt fem minutters gange fra stranden La Carihuela og, ifølge brosjyren, under ti minutter med bil fra Málaga lufthavn. Portalsiden oppgir 353 boliger i alt, med ett til fire soverom.',
  'Exploatörens broschyr presenterar ett modernt område med lägenheter med stora fönster och rymliga terrasser i Torremolinos, omkring fem minuters promenad från stranden La Carihuela och enligt broschyren under tio minuter med bil från Málagas flygplats. Portalsidan anger 353 bostäder totalt, med ett till fyra sovrum.')
a('.overview.copy[1]',
  'La lista de precios que tenemos, de noviembre de 2026, recoge cuatro viviendas: un apartamento de un dormitorio y otro de dos en el nivel que los planos llaman -2, uno de tres dormitorios en la primera planta y uno de cuatro en la quinta. Ningún documento indica una licencia, el estado de las obras ni una fecha de entrega.',
  'La liste de prix dont nous disposons, de novembre 2026, compte quatre logements : un appartement d’une chambre et un de deux chambres au niveau que les plans appellent -2, un de trois chambres au premier étage et un de quatre chambres au cinquième. Aucun document n’indique de permis, d’état d’avancement des travaux ni de date de livraison.',
  'Die uns vorliegende Preisliste vom November 2026 nennt vier Wohnungen: eine mit einem und eine mit zwei Schlafzimmern auf der Ebene, die die Pläne -2 nennen, eine mit drei Schlafzimmern im ersten und eine mit vier im fünften Obergeschoss. Kein Dokument nennt eine Baugenehmigung, den Baufortschritt oder einen Fertigstellungstermin.',
  'В имеющемся у нас прайс-листе за ноябрь 2026 года четыре квартиры: с одной и с двумя спальнями на уровне, который на планах обозначен как -2, с тремя спальнями на втором этаже и с четырьмя на шестом. Ни один документ не указывает разрешение на строительство, стадию работ или срок сдачи.',
  'تضم قائمة الأسعار التي بحوزتنا، لشهر نوفمبر 2026، أربعة مساكن: شقة بغرفة نوم واحدة وأخرى بغرفتين في المستوى الذي تسميه المخططات -2، وشقة بثلاث غرف نوم في الطابق الأول وأخرى بأربع غرف في الطابق الخامس. ولا تذكر أي وثيقة ترخيصًا أو مرحلة الأعمال أو موعدًا للإنجاز.',
  'De prijslijst die wij hebben, van november 2026, noemt vier woningen: een appartement met één en een met twee slaapkamers op het niveau dat de plannen -2 noemen, een met drie slaapkamers op de eerste verdieping en een met vier op de vijfde. Geen enkel document vermeldt een vergunning, de stand van de werken of een opleverdatum.',
  'Cennik, którym dysponujemy, z listopada 2026 roku, obejmuje cztery lokale: mieszkanie z jedną i z dwiema sypialniami na poziomie, który rzuty oznaczają jako -2, mieszkanie z trzema sypialniami na pierwszym piętrze i z czterema na piątym. Żaden dokument nie podaje pozwolenia na budowę, etapu prac ani terminu oddania.',
  'Prislisten vi har, fra november 2026, har fire boliger: en leilighet med ett og en med to soverom på nivået tegningene kaller -2, en med tre soverom i andre etasje og en med fire i sjette. Ingen dokumenter oppgir byggetillatelse, byggefase eller ferdigstillelsesdato.',
  'Prislistan vi har, från november 2026, tar upp fyra bostäder: en lägenhet med ett och en med två sovrum på det plan som ritningarna kallar -2, en med tre sovrum på första våningen och en med fyra på femte. Inget dokument anger bygglov, byggskede eller färdigställandedatum.')
a('.why.copy',
  'Apartamentos nuevos con terraza a un corto paseo de la playa de La Carihuela, en Torremolinos, cerca del aeropuerto de Málaga, en un conjunto con piscinas exteriores, piscina interior climatizada, gimnasio y espacio de coworking.',
  'Des appartements neufs avec terrasse à quelques pas de la plage de La Carihuela, à Torremolinos, près de l’aéroport de Malaga, dans un ensemble avec piscines extérieures, piscine intérieure chauffée, salle de sport et espace de coworking.',
  'Neue Wohnungen mit Terrasse, nur einen kurzen Spaziergang vom Strand La Carihuela in Torremolinos und nahe dem Flughafen Malaga, in einer Anlage mit Außenpools, beheiztem Innenpool, Fitnessraum und Coworking-Bereich.',
  'Новые квартиры с террасами недалеко от пляжа Ла-Каригуэла в Торремолиносе, рядом с аэропортом Малаги, в комплексе с открытыми бассейнами, крытым бассейном с подогревом, тренажёрным залом и коворкингом.',
  'شقق جديدة مع تراسات على مسافة قصيرة سيرًا من شاطئ لا كاريويلا في توريمولينوس، قرب مطار مالقة، ضمن مجمّع يضم مسابح خارجية ومسبحًا داخليًا مدفأً وصالة رياضية ومساحة للعمل المشترك.',
  'Nieuwe appartementen met een terras op korte loopafstand van het strand van La Carihuela in Torremolinos, dicht bij de luchthaven van Málaga, in een complex met buitenzwembaden, een verwarmd binnenbad, een fitnessruimte en een coworkingruimte.',
  'Nowe mieszkania z tarasem kilka minut spacerem od plaży La Carihuela w Torremolinos, blisko lotniska w Maladze, w zespole z basenami zewnętrznymi, ogrzewanym basenem wewnętrznym, siłownią i strefą coworkingu.',
  'Nye leiligheter med terrasse en kort spasertur fra stranden La Carihuela i Torremolinos, nær Málaga lufthavn, i et anlegg med utendørs bassenger, oppvarmet innendørsbasseng, treningsrom og coworking-område.',
  'Nya lägenheter med terrass en kort promenad från stranden La Carihuela i Torremolinos, nära Málagas flygplats, i ett område med utomhuspooler, uppvärmd inomhuspool, gym och coworkingyta.')
a('.why.points[0][1]',
  'Compradores que buscan un apartamento nuevo cerca de la playa y del aeropuerto, para vivir o como segunda residencia, con piscinas y gimnasio compartidos en lugar de un jardín privado.',
  'Les acheteurs qui recherchent un appartement neuf près de la plage et de l’aéroport, comme résidence principale ou secondaire, avec piscines et salle de sport partagées plutôt qu’un jardin privé.',
  'Käufer, die eine neue Wohnung nahe Strand und Flughafen suchen, als Hauptwohnsitz oder Zweitwohnung, mit gemeinsamen Pools und Fitnessraum statt eines eigenen Gartens.',
  'Покупателям, которым нужна новая квартира рядом с пляжем и аэропортом, для жизни или как второй дом, с общими бассейнами и тренажёрным залом вместо собственного сада.',
  'المشترون الذين يبحثون عن شقة جديدة قرب الشاطئ والمطار، للسكن الدائم أو كمسكن ثانٍ، مع مسابح وصالة رياضية مشتركة بدلًا من حديقة خاصة.',
  'Kopers die een nieuw appartement zoeken dicht bij het strand en de luchthaven, om er te wonen of als tweede woning, met gedeelde zwembaden en een fitnessruimte in plaats van een eigen tuin.',
  'Dla kupujących, którzy szukają nowego mieszkania blisko plaży i lotniska, na stałe lub jako drugiego domu, ze wspólnymi basenami i siłownią zamiast prywatnego ogrodu.',
  'Kjøpere som ønsker en ny leilighet nær stranden og flyplassen, som fast bolig eller fritidsbolig, med felles bassenger og treningsrom i stedet for egen hage.',
  'Köpare som vill ha en ny lägenhet nära stranden och flygplatsen, att bo i eller som fritidsbostad, med gemensamma pooler och gym i stället för en egen trädgård.')
a('.why.points[1][1]',
  'Su tamaño y su ubicación: un conjunto de 353 viviendas en una avenida principal de Torremolinos, con las zonas comunes en el interior de la manzana, a cinco minutos a pie de La Carihuela según el mapa del promotor.',
  'Sa taille et son emplacement : un ensemble de 353 logements sur une grande avenue de Torremolinos, avec les espaces communs à l’intérieur de l’îlot, à cinq minutes à pied de La Carihuela selon le plan du promoteur.',
  'Größe und Lage: eine Anlage mit 353 Wohnungen an einer Hauptstraße von Torremolinos, mit den Gemeinschaftsbereichen im Inneren des Blocks, laut Karte des Bauträgers fünf Gehminuten von La Carihuela.',
  'Масштаб и расположение: комплекс из 353 квартир на одном из главных проспектов Торремолиноса, с общими зонами внутри квартала, в пяти минутах ходьбы от Ла-Каригуэлы по карте застройщика.',
  'حجمه وموقعه: مجمّع من 353 مسكنًا على جادة رئيسية في توريمولينوس، مع المرافق المشتركة داخل المربّع السكني، على بُعد خمس دقائق سيرًا من لا كاريويلا بحسب خريطة المطوّر.',
  'De omvang en de ligging: een complex van 353 woningen aan een hoofdlaan van Torremolinos, met de gemeenschappelijke ruimten binnen het bouwblok, op vijf minuten lopen van La Carihuela volgens de kaart van de ontwikkelaar.',
  'Skala i położenie: zespół 353 lokali przy jednej z głównych alei Torremolinos, z częściami wspólnymi wewnątrz kwartału, pięć minut pieszo od La Carihueli według mapy dewelopera.',
  'Størrelsen og beliggenheten: et anlegg med 353 boliger ved en hovedgate i Torremolinos, med fellesarealene inne i kvartalet, fem minutters gange fra La Carihuela på utbyggerens kart.',
  'Storleken och läget: ett område med 353 bostäder vid en huvudgata i Torremolinos, med de gemensamma ytorna inne i kvarteret, fem minuters promenad från La Carihuela enligt exploatörens karta.')
a('.why.points[2][1]',
  '35C, en la quinta planta, tiene cuatro dormitorios, dos baños y un aseo, {N121.94} {U} construidos y dos terrazas cubiertas, una en cada extremo, que suman {N30.79} {U}, por {E1040000}.',
  '35C, au cinquième étage, compte quatre chambres, deux salles de bains et un WC indépendant, {N121.94} {U} construits et deux terrasses couvertes, une à chaque extrémité, totalisant {N30.79} {U}, pour {E1040000}.',
  '35C im fünften Obergeschoss hat vier Schlafzimmer, zwei Bäder und ein Gäste-WC, {N121.94} {U} bebaute Fläche und zwei überdachte Terrassen, je eine an jedem Ende, zusammen {N30.79} {U}, für {E1040000}.',
  '35C на шестом этаже: четыре спальни, две ванные комнаты и гостевой санузел, {N121.94} {U} площади застройки и две крытые террасы, по одной с каждого конца, в сумме {N30.79} {U}, за {E1040000}.',
  'يضم 35C، في الطابق الخامس، أربع غرف نوم وحمّامين ودورة مياه للضيوف، و{N121.94} {U} مساحة مبنية وتراسين مسقوفين، واحد في كل طرف، مجموعهما {N30.79} {U}، بسعر {E1040000}.',
  '35C, op de vijfde verdieping, heeft vier slaapkamers, twee badkamers en een gastentoilet, {N121.94} {U} bebouwd en twee overdekte terrassen, aan elk uiteinde één, samen {N30.79} {U}, voor {E1040000}.',
  '35C na piątym piętrze ma cztery sypialnie, dwie łazienki i toaletę dla gości, {N121.94} {U} powierzchni zabudowy oraz dwa zadaszone tarasy, po jednym na każdym końcu, łącznie {N30.79} {U}, za {E1040000}.',
  '35C, i sjette etasje, har fire soverom, to bad og et gjestetoalett, {N121.94} {U} bygd areal og to overdekkede terrasser, én i hver ende, til sammen {N30.79} {U}, for {E1040000}.',
  '35C, på femte våningen, har fyra sovrum, två badrum och en gästtoalett, {N121.94} {U} byggyta och två överbyggda terrasser, en i vardera änden, sammanlagt {N30.79} {U}, för {E1040000}.')
a('.why.points[3][1]',
  'Las cuatro viviendas son las que el portal de agentes del promotor mostraba el 25 de noviembre de 2026, de un total de 353. Confirmamos precio y disponibilidad, y preguntamos qué más sale a la venta, antes de cualquier reserva.',
  'Les quatre logements sont ceux que le portail agents du promoteur affichait le 25 novembre 2026, sur 353. Nous confirmons le prix et la disponibilité, et demandons ce qui est mis en vente par ailleurs, avant toute réservation.',
  'Die vier Wohnungen sind die, die das Maklerportal des Bauträgers am 25. November 2026 auswies, von insgesamt 353. Wir bestätigen Preis und Verfügbarkeit und fragen nach, was sonst freigegeben ist, bevor Sie reservieren.',
  'Эти четыре квартиры — то, что агентский портал застройщика показывал 25 ноября 2026 года, из 353. Мы подтверждаем цену и наличие и уточняем, что ещё выставлено в продажу, до любого бронирования.',
  'المساكن الأربعة هي ما عرضته بوابة الوكلاء لدى المطوّر في 25 نوفمبر 2026، من أصل 353. ونؤكد السعر والتوفر ونستفسر عمّا طُرح غيرها للبيع قبل أي حجز.',
  'De vier woningen zijn wat het makelaarsportaal van de ontwikkelaar op 25 november 2026 toonde, van de 353. Wij bevestigen prijs en beschikbaarheid, en vragen wat er verder in verkoop is, vóór elke reservering.',
  'Te cztery lokale to te, które portal dla agentów dewelopera pokazywał 25 listopada 2026 roku, spośród 353. Przed rezerwacją potwierdzamy cenę i dostępność oraz pytamy, co jeszcze jest w sprzedaży.',
  'De fire boligene er det utbyggerens meglerportal viste 25. november 2026, av 353. Vi bekrefter pris og tilgjengelighet, og spør hva mer som er lagt ut for salg, før en eventuell reservasjon.',
  'De fyra bostäderna är vad exploatörens mäklarportal visade den 25 november 2026, av 353. Vi bekräftar pris och tillgänglighet, och frågar vad mer som släppts till försäljning, före en eventuell bokning.')

# ---- architecture ----------------------------------------------------------------------------

a('.architecture.headlineHtml',
  'Terrazas curvas, <em>un patio de jardines</em>', 'Des terrasses courbes, <em>une cour de jardins</em>', 'Geschwungene Terrassen, <em>ein Gartenhof</em>',
  'Изогнутые террасы, <em>двор с садами</em>', 'تراسات منحنية، <em>وفناء من الحدائق</em>', 'Gebogen terrassen, <em>een binnenhof met tuinen</em>',
  'Zaokrąglone tarasy, <em>dziedziniec z ogrodami</em>', 'Buede terrasser, <em>et gårdsrom med hager</em>', 'Böjda terrasser, <em>en innergård med trädgårdar</em>')
a('.architecture.copy[0]',
  'El folleto habla de líneas limpias, espacios abiertos y viviendas pensadas para aprovechar la luz natural, con grandes ventanales y terrazas que prolongan el salón hacia el exterior. Menciona carpinterías de altas prestaciones, climatización eficiente con aerotermia y materiales duraderos, sin dar una memoria de calidades.',
  'La brochure évoque des lignes épurées, des espaces ouverts et des logements conçus pour la lumière naturelle, avec de grandes baies et des terrasses qui prolongent le séjour vers l’extérieur. Elle cite des menuiseries performantes, une climatisation efficace par aérothermie et des matériaux durables, sans fournir de descriptif technique.',
  'Die Broschüre spricht von klaren Linien, offenen Räumen und Wohnungen, die auf Tageslicht ausgelegt sind, mit großen Fenstern und Terrassen, die den Wohnraum nach draußen verlängern. Sie nennt leistungsstarke Fensterrahmen, effiziente Klimatisierung mit Aerothermie und langlebige Materialien, ohne eine Baubeschreibung zu liefern.',
  'Буклет говорит о чистых линиях, открытых пространствах и квартирах, спланированных под естественный свет, с большими окнами и террасами, продолжающими гостиную наружу. В нём упомянуты высокоэффективные оконные рамы, экономичный климат-контроль с аэротермией и долговечные материалы, но спецификации нет.',
  'يتحدث الكتيّب عن خطوط نقية ومساحات مفتوحة ومساكن مصمّمة للاستفادة من الضوء الطبيعي، مع نوافذ كبيرة وتراسات تمدّ غرفة المعيشة إلى الخارج. ويذكر نوافذ عالية الأداء وتكييفًا فعّالًا بتقنية الطاقة الهوائية الحرارية ومواد متينة، دون تقديم مواصفات بناء.',
  'De brochure spreekt van strakke lijnen, open ruimten en woningen die op daglicht zijn ontworpen, met grote ramen en terrassen die de woonkamer naar buiten verlengen. Ze noemt hoogwaardig schrijnwerk, efficiënte klimaatregeling met een luchtwarmtepomp en duurzame materialen, zonder een lastenboek te geven.',
  'Broszura mówi o czystych liniach, otwartych przestrzeniach i mieszkaniach zaprojektowanych z myślą o świetle dziennym, z dużymi oknami i tarasami przedłużającymi salon na zewnątrz. Wymienia wysokiej klasy stolarkę okienną, wydajną klimatyzację z aerotermią i trwałe materiały, nie podając specyfikacji technicznej.',
  'Brosjyren beskriver rene linjer, åpne rom og boliger utformet for dagslys, med store vinduer og terrasser som forlenger stuen utendørs. Den nevner vinduer med høy ytelse, effektiv klimastyring med luft-til-vann-varmepumpe og slitesterke materialer, uten å gi en byggebeskrivelse.',
  'Broschyren talar om rena linjer, öppna ytor och bostäder utformade för dagsljus, med stora fönster och terrasser som förlänger vardagsrummet utomhus. Den nämner högpresterande fönsterpartier, effektiv klimatanläggning med luft-vattenvärmepump och tåliga material, utan att ge någon byggbeskrivning.')
a('.architecture.copy[1]',
  'En las imágenes generadas por ordenador del promotor, el edificio rodea una manzana con largas losas de terraza curvas, barandillas blancas, paneles verticales acanalados y vegetación en las cubiertas, alrededor de un patio con jardines y piscina. Sus planos numeran las viviendas por portal, del 1 al menos al 17, y por planta, desde el nivel -2 hacia arriba.',
  'Dans les images de synthèse du promoteur, le bâtiment entoure un îlot de longues dalles de terrasse courbes, de garde-corps blancs, de panneaux verticaux cannelés et de végétation sur les toits, autour d’une cour plantée avec piscine. Ses plans numérotent les logements par cage d’escalier, de 1 à 17 au moins, et par niveau, à partir du niveau -2.',
  'In den computergenerierten Bildern des Bauträgers umschließt das Gebäude einen Block mit langen, geschwungenen Terrassenplatten, weißen Geländern, gerippten senkrechten Paneelen und begrünten Dächern, um einen Gartenhof mit Pool. Die Pläne nummerieren die Wohnungen nach Aufgang, von 1 bis mindestens 17, und nach Geschoss, ab Ebene -2 aufwärts.',
  'На компьютерных визуализациях застройщика здание охватывает квартал длинными изогнутыми плитами террас с белыми ограждениями, рифлёными вертикальными панелями и озеленёнными крышами, вокруг двора с садами и бассейном. Планы нумеруют квартиры по подъездам, от 1 как минимум до 17, и по этажам, начиная с уровня -2.',
  'في صور المطوّر المُنشأة بالحاسوب يلتفّ المبنى حول مربّع سكني بألواح تراسات طويلة منحنية ودرابزينات بيضاء وألواح عمودية مضلّعة ونباتات على الأسطح، حول فناء من الحدائق ومسبح. وترقّم المخططات المساكن حسب المدخل، من 1 إلى 17 على الأقل، وحسب الطابق، من المستوى -2 صعودًا.',
  'Op de computergegenereerde beelden van de ontwikkelaar omsluit het gebouw een bouwblok met lange, gebogen terrasplaten, witte balustrades, geribde verticale panelen en beplante daken, rond een binnenhof met tuinen en een zwembad. De plannen nummeren de woningen per portiek, van 1 tot minstens 17, en per verdieping, vanaf niveau -2.',
  'Na wizualizacjach dewelopera budynek otacza kwartał długimi, zaokrąglonymi płytami tarasów z białymi balustradami, żebrowanymi pionowymi panelami i zielenią na dachach, wokół dziedzińca z ogrodami i basenem. Rzuty numerują lokale według klatek, od 1 do co najmniej 17, i według kondygnacji, od poziomu -2 w górę.',
  'I utbyggerens datagenererte bilder omslutter bygget et kvartal med lange, buede terrasseplater, hvite rekkverk, riflede vertikale paneler og beplantede tak, rundt et gårdsrom med hager og basseng. Tegningene nummererer boligene etter oppgang, fra 1 til minst 17, og etter etasje, fra nivå -2 og oppover.',
  'I exploatörens datorgenererade bilder omsluter huset ett kvarter med långa, böjda terrassplattor, vita räcken, räfflade vertikala paneler och planterade tak, runt en innergård med trädgårdar och pool. Ritningarna numrerar bostäderna efter uppgång, från 1 till minst 17, och efter våning, från plan -2 och uppåt.')
a('.architecture.highlights[0][1]',
  'Todas las viviendas de la lista tienen terraza: desde {N8.33} {U} en 11B hasta {N30.79} {U} en dos partes en 35C, según los planos del promotor.',
  'Tous les logements de la liste ont une terrasse : de {N8.33} {U} pour 11B à {N30.79} {U} en deux parties pour 35C, d’après les plans du promoteur.',
  'Jede gelistete Wohnung hat eine Terrasse: von {N8.33} {U} bei 11B bis {N30.79} {U} in zwei Teilen bei 35C, laut den Plänen des Bauträgers.',
  'У каждой квартиры из списка есть терраса: от {N8.33} {U} у 11B до {N30.79} {U} в двух частях у 35C, по планам застройщика.',
  'لكل مسكن مدرج تراس: من {N8.33} {U} في 11B إلى {N30.79} {U} على جزأين في 35C، بحسب مخططات المطوّر.',
  'Elke woning op de lijst heeft een terras: van {N8.33} {U} bij 11B tot {N30.79} {U} in twee delen bij 35C, volgens de plannen van de ontwikkelaar.',
  'Każdy lokal z cennika ma taras: od {N8.33} {U} w 11B do {N30.79} {U} w dwóch częściach w 35C, według rzutów dewelopera.',
  'Alle boligene på listen har terrasse: fra {N8.33} {U} i 11B til {N30.79} {U} fordelt på to i 35C, ifølge utbyggerens tegninger.',
  'Varje bostad på listan har terrass: från {N8.33} {U} i 11B till {N30.79} {U} i två delar i 35C, enligt exploatörens ritningar.')
a('.architecture.highlights[1][0]',
  'Luz', 'Lumière', 'Licht', 'Свет', 'الضوء', 'Licht', 'Światło', 'Lys', 'Ljus')
a('.architecture.highlights[1][1]',
  'Grandes ventanales y amplias terrazas, que el folleto presenta como una prolongación del espacio de día.',
  'De grandes baies et des terrasses généreuses, que la brochure présente comme le prolongement des pièces de vie.',
  'Große Fenster und großzügige Terrassen, die die Broschüre als Verlängerung des Wohnraums darstellt.',
  'Большие окна и просторные террасы, которые буклет подаёт как продолжение жилого пространства.',
  'نوافذ كبيرة وتراسات واسعة يقدّمها الكتيّب امتدادًا لمساحة المعيشة.',
  'Grote ramen en ruime terrassen, die de brochure voorstelt als verlengstuk van de leefruimte.',
  'Duże okna i obszerne tarasy, które broszura przedstawia jako przedłużenie strefy dziennej.',
  'Store vinduer og romslige terrasser, som brosjyren presenterer som en forlengelse av oppholdsrommene.',
  'Stora fönster och rymliga terrasser, som broschyren beskriver som en förlängning av vardagsrummen.')
a('.architecture.highlights[2][1]',
  'Aerotermia y climatización eficiente, tal como las nombra el folleto; no hemos podido obtener la memoria de calidades.',
  'Aérothermie et climatisation efficace, telles que la brochure les nomme ; nous n’avons pas pu obtenir le descriptif technique.',
  'Aerothermie und effiziente Klimatisierung, wie die Broschüre sie nennt; die Baubeschreibung lag uns nicht vor.',
  'Аэротермия и экономичный климат-контроль, как их называет буклет; спецификацию получить не удалось.',
  'تقنية الطاقة الهوائية الحرارية وتكييف فعّال، كما يذكرهما الكتيّب؛ ولم نتمكّن من الحصول على مواصفات البناء.',
  'Een luchtwarmtepomp en efficiënte klimaatregeling, zoals de brochure ze noemt; het lastenboek konden wij niet krijgen.',
  'Aerotermia i wydajna klimatyzacja, tak jak wymienia je broszura; specyfikacji technicznej nie udało się uzyskać.',
  'Luft-til-vann-varmepumpe og effektiv klimastyring, slik brosjyren nevner dem; byggebeskrivelsen har vi ikke fått tak i.',
  'Luft-vattenvärmepump och effektiv klimatanläggning, så som broschyren nämner dem; byggbeskrivningen har vi inte kunnat få.')
a('.architecture.highlights[3][0]',
  'Distribución', 'Agencement', 'Raumaufteilung', 'Планировка', 'التوزيع الداخلي', 'Indeling', 'Układ', 'Planløsning', 'Planlösning')
a('.architecture.highlights[3][1]',
  'Salones diáfanos con la cocina integrada y dormitorios en torno a un distribuidor independiente, en los cuatro planos.',
  'Des séjours ouverts avec la cuisine et des chambres desservies par un dégagement séparé, sur les quatre plans.',
  'Offene Wohnbereiche mit Küche und Schlafzimmer an einem separaten Flur, auf allen vier Grundrissen.',
  'Открытые гостиные с кухней и спальни, выходящие в отдельный коридор, на всех четырёх планах.',
  'غرف معيشة مفتوحة مع المطبخ وغرف نوم على ممر منفصل، في المخططات الأربعة كلها.',
  'Open woonkamers met de keuken en slaapkamers aan een aparte gang, op alle vier de plattegronden.',
  'Otwarte salony z kuchnią i sypialnie przy osobnym korytarzu, na wszystkich czterech rzutach.',
  'Åpne stuer med kjøkken og soverom langs en egen gang, på alle fire tegningene.',
  'Öppna vardagsrum med kök och sovrum längs en separat hall, på alla fyra ritningarna.')

# ---- residences ------------------------------------------------------------------------------

a('.residences.headlineHtml',
  'Apartamentos de uno a <em>cuatro dormitorios</em>', 'Appartements d’une à <em>quatre chambres</em>', 'Wohnungen mit einem bis <em>vier Schlafzimmern</em>',
  'Квартиры с одной–<em>четырьмя спальнями</em>', 'شقق بغرفة إلى <em>أربع غرف نوم</em>', 'Appartementen met één tot <em>vier slaapkamers</em>',
  'Mieszkania z jedną do <em>czterech sypialni</em>', 'Leiligheter med ett til <em>fire soverom</em>', 'Lägenheter med ett till <em>fyra sovrum</em>')
a('.residences.copy',
  'Las cuatro viviendas de la lista de precios, con la superficie construida y la terraza de los planos del promotor. La página del portal describe además el conjunto: viviendas en plantas intermedias con amplias terrazas con vistas a Torremolinos y a los jardines, y áticos con terrazas privadas con piscina y jacuzzi. En la lista que tenemos no figura ningún ático.',
  'Les quatre logements de la liste de prix, avec la surface construite et la terrasse issues des plans du promoteur. La page du portail décrit aussi l’ensemble : des logements aux étages intermédiaires avec de grandes terrasses donnant sur Torremolinos et les jardins, et des penthouses avec des terrasses privées équipées d’une piscine et d’un jacuzzi. Aucun penthouse ne figure sur la liste dont nous disposons.',
  'Die vier Wohnungen der Preisliste, mit bebauter Fläche und Terrasse aus den Plänen des Bauträgers. Die Portalseite beschreibt auch die übrige Anlage: Wohnungen in den mittleren Geschossen mit großen Terrassen und Blick über Torremolinos und die Gärten, und Penthäuser mit privaten Terrassen samt Pool und Whirlpool. Auf der uns vorliegenden Liste steht kein Penthouse.',
  'Четыре квартиры из прайс-листа, с площадью застройки и террасой по планам застройщика. Страница портала описывает и весь комплекс: квартиры на средних этажах с большими террасами и видом на Торремолинос и сады, а также пентхаусы с собственными террасами, где есть бассейн и джакузи. Пентхаусов в имеющемся у нас списке нет.',
  'المساكن الأربعة المدرجة في قائمة الأسعار، مع المساحة المبنية والتراس من مخططات المطوّر. وتصف صفحة البوابة المجمّع أيضًا: مساكن في الطوابق الوسطى بتراسات واسعة تطلّ على توريمولينوس والحدائق، وبنتهاوس بتراسات خاصة تضم مسبحًا وجاكوزي. ولا يرد أي بنتهاوس في القائمة التي بحوزتنا.',
  'De vier woningen van de prijslijst, met de bebouwde oppervlakte en het terras uit de plannen van de ontwikkelaar. De portaalpagina beschrijft ook de rest van het complex: woningen op de middelste verdiepingen met ruime terrassen met uitzicht op Torremolinos en de tuinen, en penthouses met privéterrassen met een zwembad en een jacuzzi. Op de lijst die wij hebben staat geen penthouse.',
  'Cztery lokale z cennika, z powierzchnią zabudowy i tarasem według rzutów dewelopera. Strona portalu opisuje też resztę zespołu: mieszkania na środkowych piętrach z dużymi tarasami z widokiem na Torremolinos i ogrody oraz penthouse’y z prywatnymi tarasami z basenem i jacuzzi. Na liście, którą mamy, nie ma żadnego penthouse’u.',
  'De fire boligene på prislisten, med bygd areal og terrasse fra utbyggerens tegninger. Portalsiden beskriver også resten av anlegget: boliger i midtetasjene med store terrasser med utsikt over Torremolinos og hagene, og toppleiligheter med private terrasser med basseng og boblebad. Ingen toppleilighet står på listen vi har.',
  'De fyra bostäderna i prislistan, med byggyta och terrass enligt exploatörens ritningar. Portalsidan beskriver även resten av området: bostäder på mellanvåningarna med stora terrasser med utsikt över Torremolinos och trädgårdarna, och takvåningar med privata terrasser med pool och jacuzzi. Ingen takvåning finns på listan vi har.')
a('.residences.items[0].name',
  'En el nivel -2', 'Au niveau -2', 'Auf Ebene -2', 'На уровне -2', 'في المستوى -2', 'Op niveau -2', 'Na poziomie -2', 'På nivå -2', 'På plan -2')
a('.residences.items[0].points[0]',
  '16-2D tiene un dormitorio y un baño, {N55.38} {U} construidos y una terraza de {N13.28} {U}, en parte cubierta y bordeada de vegetación en su plano, por {E378000}.',
  '16-2D compte une chambre et une salle de bains, {N55.38} {U} construits et une terrasse de {N13.28} {U}, en partie couverte et bordée de végétation sur son plan, pour {E378000}.',
  '16-2D hat ein Schlafzimmer und ein Bad, {N55.38} {U} bebaute Fläche und eine Terrasse von {N13.28} {U}, teils überdacht und laut Plan von Bepflanzung gesäumt, für {E378000}.',
  '16-2D: одна спальня и одна ванная, {N55.38} {U} площади застройки и терраса {N13.28} {U}, частично крытая и окаймлённая зеленью на плане, за {E378000}.',
  'يضم 16-2D غرفة نوم وحمّامًا واحدًا، و{N55.38} {U} مساحة مبنية وتراسًا مساحته {N13.28} {U}، مسقوفًا جزئيًا وتحيط به النباتات في مخططه، بسعر {E378000}.',
  '16-2D heeft één slaapkamer en één badkamer, {N55.38} {U} bebouwd en een terras van {N13.28} {U}, deels overdekt en op de plattegrond omzoomd door beplanting, voor {E378000}.',
  '16-2D ma jedną sypialnię i jedną łazienkę, {N55.38} {U} powierzchni zabudowy i taras o powierzchni {N13.28} {U}, częściowo zadaszony i obsadzony zielenią na rzucie, za {E378000}.',
  '16-2D har ett soverom og ett bad, {N55.38} {U} bygd areal og en terrasse på {N13.28} {U}, delvis overdekket og omkranset av beplantning på tegningen, for {E378000}.',
  '16-2D har ett sovrum och ett badrum, {N55.38} {U} byggyta och en terrass på {N13.28} {U}, delvis överbyggd och kantad av växtlighet på ritningen, för {E378000}.')
a('.residences.items[0].points[1]',
  '13-2B tiene dos dormitorios y dos baños, {N71.40} {U} construidos y una terraza cubierta de {N12.97} {U} a lo largo de sus tres estancias principales, por {E472000}. Los documentos no indican si el nivel -2 da a la calle o al jardín; lo comprobamos en una visita.',
  '13-2B compte deux chambres et deux salles de bains, {N71.40} {U} construits et une terrasse couverte de {N12.97} {U} le long de ses trois pièces principales, pour {E472000}. Les documents ne disent pas si le niveau -2 donne sur la rue ou sur le jardin ; nous le vérifions lors d’une visite.',
  '13-2B hat zwei Schlafzimmer und zwei Bäder, {N71.40} {U} bebaute Fläche und eine überdachte Terrasse von {N12.97} {U} entlang der drei Haupträume, für {E472000}. Die Unterlagen sagen nicht, ob Ebene -2 zur Straße oder zum Garten liegt; wir prüfen es bei einem Besuch.',
  '13-2B: две спальни и две ванные, {N71.40} {U} площади застройки и крытая терраса {N12.97} {U} вдоль трёх основных комнат, за {E472000}. Документы не уточняют, выходит ли уровень -2 на улицу или в сад; мы проверяем это при осмотре.',
  'يضم 13-2B غرفتي نوم وحمّامين، و{N71.40} {U} مساحة مبنية وتراسًا مسقوفًا مساحته {N12.97} {U} على امتداد غرفه الرئيسية الثلاث، بسعر {E472000}. ولا تذكر الوثائق ما إذا كان المستوى -2 يطلّ على الشارع أم على الحديقة؛ ونتحقق من ذلك خلال الزيارة.',
  '13-2B heeft twee slaapkamers en twee badkamers, {N71.40} {U} bebouwd en een overdekt terras van {N12.97} {U} langs de drie hoofdruimten, voor {E472000}. De documenten zeggen niet of niveau -2 op de straat of op de tuin uitkomt; dat controleren wij bij een bezoek.',
  '13-2B ma dwie sypialnie i dwie łazienki, {N71.40} {U} powierzchni zabudowy i zadaszony taras o powierzchni {N12.97} {U} wzdłuż trzech głównych pomieszczeń, za {E472000}. Dokumenty nie mówią, czy poziom -2 wychodzi na ulicę, czy na ogród; sprawdzamy to podczas wizyty.',
  '13-2B har to soverom og to bad, {N71.40} {U} bygd areal og en overdekket terrasse på {N12.97} {U} langs de tre hovedrommene, for {E472000}. Dokumentene sier ikke om nivå -2 vender mot gaten eller hagen; det sjekker vi ved en visning.',
  '13-2B har två sovrum och två badrum, {N71.40} {U} byggyta och en överbyggd terrass på {N12.97} {U} längs de tre huvudrummen, för {E472000}. Handlingarna säger inte om plan -2 vetter mot gatan eller trädgården; det kontrollerar vi vid ett besök.')
a('.residences.items[1].name',
  'En las plantas superiores', 'Aux étages supérieurs', 'In den oberen Geschossen', 'На верхних этажах', 'في الطوابق العليا',
  'Op de bovenverdiepingen', 'Na wyższych piętrach', 'I de øvre etasjene', 'På de övre våningarna')
a('.residences.items[1].points[0]',
  '11B, en la primera planta, tiene tres dormitorios y dos baños, {N104.73} {U} construidos y una terraza cubierta de {N8.33} {U} junto al salón, por {E597000}.',
  '11B, au premier étage, compte trois chambres et deux salles de bains, {N104.73} {U} construits et une terrasse couverte de {N8.33} {U} attenante au séjour, pour {E597000}.',
  '11B im ersten Obergeschoss hat drei Schlafzimmer und zwei Bäder, {N104.73} {U} bebaute Fläche und eine überdachte Terrasse von {N8.33} {U} am Wohnraum, für {E597000}.',
  '11B на втором этаже: три спальни и две ванные, {N104.73} {U} площади застройки и крытая терраса {N8.33} {U} у гостиной, за {E597000}.',
  'يضم 11B، في الطابق الأول، ثلاث غرف نوم وحمّامين، و{N104.73} {U} مساحة مبنية وتراسًا مسقوفًا مساحته {N8.33} {U} ملاصقًا لغرفة المعيشة، بسعر {E597000}.',
  '11B, op de eerste verdieping, heeft drie slaapkamers en twee badkamers, {N104.73} {U} bebouwd en een overdekt terras van {N8.33} {U} aan de woonkamer, voor {E597000}.',
  '11B na pierwszym piętrze ma trzy sypialnie i dwie łazienki, {N104.73} {U} powierzchni zabudowy i zadaszony taras o powierzchni {N8.33} {U} przy salonie, za {E597000}.',
  '11B, i andre etasje, har tre soverom og to bad, {N104.73} {U} bygd areal og en overdekket terrasse på {N8.33} {U} ut fra stuen, for {E597000}.',
  '11B, på första våningen, har tre sovrum och två badrum, {N104.73} {U} byggyta och en överbyggd terrass på {N8.33} {U} i anslutning till vardagsrummet, för {E597000}.')
a('.residences.items[1].points[1]',
  '35C, en la quinta planta, tiene cuatro dormitorios, dos baños y un aseo, {N121.94} {U} construidos y {N30.79} {U} de terraza cubierta en dos partes, por {E1040000}.',
  '35C, au cinquième étage, compte quatre chambres, deux salles de bains et un WC indépendant, {N121.94} {U} construits et {N30.79} {U} de terrasse couverte en deux parties, pour {E1040000}.',
  '35C im fünften Obergeschoss hat vier Schlafzimmer, zwei Bäder und ein Gäste-WC, {N121.94} {U} bebaute Fläche und {N30.79} {U} überdachte Terrasse in zwei Teilen, für {E1040000}.',
  '35C на шестом этаже: четыре спальни, две ванные и гостевой санузел, {N121.94} {U} площади застройки и {N30.79} {U} крытой террасы в двух частях, за {E1040000}.',
  'يضم 35C، في الطابق الخامس، أربع غرف نوم وحمّامين ودورة مياه للضيوف، و{N121.94} {U} مساحة مبنية و{N30.79} {U} من التراس المسقوف على جزأين، بسعر {E1040000}.',
  '35C, op de vijfde verdieping, heeft vier slaapkamers, twee badkamers en een gastentoilet, {N121.94} {U} bebouwd en {N30.79} {U} overdekt terras in twee delen, voor {E1040000}.',
  '35C na piątym piętrze ma cztery sypialnie, dwie łazienki i toaletę dla gości, {N121.94} {U} powierzchni zabudowy i {N30.79} {U} zadaszonego tarasu w dwóch częściach, za {E1040000}.',
  '35C, i sjette etasje, har fire soverom, to bad og et gjestetoalett, {N121.94} {U} bygd areal og {N30.79} {U} overdekket terrasse fordelt på to, for {E1040000}.',
  '35C, på femte våningen, har fyra sovrum, två badrum och en gästtoalett, {N121.94} {U} byggyta och {N30.79} {U} överbyggd terrass i två delar, för {E1040000}.')
a('.residences.items[2].name',
  'En todos los planos', 'Sur tous les plans', 'Auf allen Plänen', 'На всех планах', 'في كل المخططات', 'Op alle plattegronden',
  'Na wszystkich rzutach', 'På alle tegningene', 'På alla ritningar')
a('.residences.items[2].points[0]',
  'Un salón-comedor-cocina diáfano, con los dormitorios y los baños en torno a un distribuidor.',
  'Une pièce ouverte séjour-salle à manger-cuisine, avec les chambres et les salles de bains autour d’un dégagement.',
  'Ein offener Wohn-, Ess- und Kochbereich, mit Schlafzimmern und Bädern an einem Flur.',
  'Открытая гостиная-столовая с кухней; спальни и ванные выходят в коридор.',
  'غرفة مفتوحة للمعيشة والطعام والمطبخ، مع غرف النوم والحمّامات على ممر.',
  'Een open woon-eetkamer met keuken, met de slaapkamers en badkamers aan een gang.',
  'Otwarty salon z jadalnią i kuchnią, a sypialnie i łazienki przy korytarzu.',
  'Et åpent rom med stue, spiseplass og kjøkken, med soverom og bad langs en gang.',
  'Ett öppet rum med vardagsrum, matplats och kök, med sovrum och badrum längs en hall.')
a('.residences.items[2].points[1]',
  'Los planos dan también una superficie construida que incluye una parte de las zonas comunes; aquí no se muestra.',
  'Les plans donnent aussi une surface construite incluant une quote-part des parties communes ; elle n’est pas reprise ici.',
  'Die Pläne nennen außerdem eine bebaute Fläche mit Anteil an den Gemeinschaftsflächen; sie wird hier nicht gezeigt.',
  'На планах указана и площадь застройки с долей мест общего пользования; здесь она не приводится.',
  'وتذكر المخططات أيضًا مساحة مبنية تشمل حصة من المناطق المشتركة؛ ولا تُعرض هنا.',
  'De plannen geven ook een bebouwde oppervlakte inclusief een aandeel in de gemeenschappelijke delen; die wordt hier niet getoond.',
  'Rzuty podają też powierzchnię zabudowy z udziałem w częściach wspólnych; nie jest tu pokazywana.',
  'Tegningene oppgir også et bygd areal som inkluderer en andel av fellesarealene; det vises ikke her.',
  'Ritningarna anger också en byggyta som inkluderar en andel av de gemensamma ytorna; den visas inte här.')

# ---- lifestyle -------------------------------------------------------------------------------

a('.lifestyle.headlineHtml',
  'Piscinas, gimnasio <em>y espacio de coworking</em>', 'Piscines, salle de sport <em>et espace de coworking</em>', 'Pools, Fitnessraum <em>und Coworking-Bereich</em>',
  'Бассейны, тренажёрный зал <em>и коворкинг</em>', 'مسابح وصالة رياضية <em>ومساحة للعمل المشترك</em>', 'Zwembaden, een fitnessruimte <em>en een coworkingruimte</em>',
  'Baseny, siłownia <em>i strefa coworkingu</em>', 'Bassenger, treningsrom <em>og coworking-område</em>', 'Pooler, gym <em>och coworkingyta</em>')
a('.lifestyle.copy',
  'El folleto enumera las zonas comunes sin medidas ni horarios, así que confirmamos qué se construye y qué está en uso antes de cualquier reserva.',
  'La brochure énumère les espaces communs sans dimensions ni horaires ; nous confirmons donc ce qui est construit et ouvert avant toute réservation.',
  'Die Broschüre zählt die Gemeinschaftsbereiche ohne Größen oder Öffnungszeiten auf; wir bestätigen daher vor jeder Reservierung, was gebaut wird und nutzbar ist.',
  'Буклет перечисляет общие зоны без размеров и режима работы, поэтому до бронирования мы уточняем, что будет построено и открыто.',
  'يعدّد الكتيّب المرافق المشتركة دون مقاسات أو مواعيد عمل، لذا نؤكد ما سيُبنى وما سيكون مفتوحًا قبل أي حجز.',
  'De brochure somt de gemeenschappelijke ruimten op zonder afmetingen of openingstijden, dus wij bevestigen vóór elke reservering wat er gebouwd wordt en open is.',
  'Broszura wymienia części wspólne bez wymiarów i godzin otwarcia, dlatego przed rezerwacją potwierdzamy, co zostanie zbudowane i będzie dostępne.',
  'Brosjyren lister opp fellesarealene uten mål eller åpningstider, så vi bekrefter hva som bygges og er åpent før en eventuell reservasjon.',
  'Broschyren räknar upp de gemensamma ytorna utan mått eller öppettider, så vi bekräftar vad som byggs och är öppet före en eventuell bokning.')
a('.lifestyle.panels[0][1]',
  'El folleto menciona piscinas exteriores y una piscina interior climatizada. Las imágenes del promotor muestran una piscina en un patio ajardinado y otra sobre una tarima frente al mar.',
  'La brochure cite des piscines extérieures et une piscine intérieure chauffée. Les images du promoteur montrent une piscine dans une cour plantée et une autre sur un deck face à la mer.',
  'Die Broschüre nennt Außenpools und einen beheizten Innenpool. Die Bilder des Bauträgers zeigen einen Pool in einem Gartenhof und einen auf einem Deck mit Blick aufs Meer.',
  'В буклете названы открытые бассейны и крытый бассейн с подогревом. На изображениях застройщика — бассейн в саду во дворе и ещё один на настиле с видом на море.',
  'يذكر الكتيّب مسابح خارجية ومسبحًا داخليًا مدفأً. وتُظهر صور المطوّر مسبحًا في فناء مزروع وآخر على سطح خشبي يطلّ على البحر.',
  'De brochure noemt buitenzwembaden en een verwarmd binnenbad. De beelden van de ontwikkelaar tonen een zwembad op een binnenhof met tuin en een op een vlonder met uitzicht op zee.',
  'Broszura wymienia baseny zewnętrzne i ogrzewany basen wewnętrzny. Wizualizacje dewelopera pokazują basen na dziedzińcu z ogrodem i drugi na tarasie z widokiem na morze.',
  'Brosjyren nevner utendørs bassenger og et oppvarmet innendørsbasseng. Utbyggerens bilder viser et basseng i et hagegårdsrom og et på et dekk med utsikt mot havet.',
  'Broschyren nämner utomhuspooler och en uppvärmd inomhuspool. Exploatörens bilder visar en pool på en trädgårdsgård och en på ett däck med utsikt mot havet.')
a('.lifestyle.panels[1][1]',
  'Un gimnasio equipado y espacios deportivos al aire libre, tal como los enumera el folleto, sin medidas ni equipamiento.',
  'Une salle de sport équipée et des espaces sportifs en plein air, tels que la brochure les énumère, sans dimensions ni équipements.',
  'Ein ausgestatteter Fitnessraum und Sportbereiche im Freien, wie die Broschüre sie aufzählt, ohne Größen oder Ausstattung.',
  'Оборудованный тренажёрный зал и спортивные площадки под открытым небом, как их перечисляет буклет, без размеров и списка оборудования.',
  'صالة رياضية مجهّزة ومساحات رياضية في الهواء الطلق، كما يعدّدها الكتيّب، دون مقاسات أو تجهيزات.',
  'Een uitgeruste fitnessruimte en sportruimten in de open lucht, zoals de brochure ze opsomt, zonder afmetingen of uitrusting.',
  'Wyposażona siłownia i strefy sportowe na świeżym powietrzu, tak jak wymienia je broszura, bez wymiarów i wyposażenia.',
  'Et utstyrt treningsrom og utendørs idrettsområder, slik brosjyren lister dem opp, uten mål eller utstyr.',
  'Ett utrustat gym och idrottsytor utomhus, så som broschyren räknar upp dem, utan mått eller utrustning.')
a('.lifestyle.panels[2][0]',
  'Coworking y gastroteca', 'Coworking et gastroteca', 'Coworking und Gastroteca', 'Коворкинг и гастротека',
  'العمل المشترك والغاستروتيكا', 'Coworking en gastroteca', 'Coworking i gastroteka', 'Coworking og gastroteca', 'Coworking och gastroteca')
a('.lifestyle.panels[2][1]',
  'Un espacio de coworking y una gastroteca, un espacio compartido para comer y beber, ambos citados en el folleto.',
  'Un espace de coworking et une gastroteca, un espace partagé pour manger et boire, tous deux cités dans la brochure.',
  'Ein Coworking-Bereich und eine Gastroteca, ein gemeinsamer Raum zum Essen und Trinken, beide in der Broschüre genannt.',
  'Коворкинг и гастротека — общее пространство для еды и напитков; оба упомянуты в буклете.',
  'مساحة للعمل المشترك وغاستروتيكا، وهي مساحة مشتركة للطعام والشراب، وكلتاهما مذكورتان في الكتيّب.',
  'Een coworkingruimte en een gastroteca, een gedeelde ruimte om te eten en te drinken, beide genoemd in de brochure.',
  'Strefa coworkingu i gastroteka, wspólna przestrzeń do jedzenia i picia, obie wymienione w broszurze.',
  'Et coworking-område og en gastroteca, et felles rom for mat og drikke, begge nevnt i brosjyren.',
  'En coworkingyta och en gastroteca, ett gemensamt utrymme för mat och dryck, båda nämnda i broschyren.')
a('.lifestyle.panels[3][1]',
  'La playa de La Carihuela, a unos cinco minutos a pie según el mapa del promotor, con el Puerto Marina de Benalmádena a lo largo de la costa.',
  'La plage de La Carihuela, à environ cinq minutes à pied selon le plan du promoteur, avec la marina de Benalmádena le long de la côte.',
  'Der Strand La Carihuela, laut Karte des Bauträgers etwa fünf Gehminuten entfernt, mit dem Jachthafen von Benalmádena weiter an der Küste.',
  'Пляж Ла-Каригуэла — примерно в пяти минутах ходьбы по карте застройщика, а дальше по побережью марина Бенальмадены.',
  'شاطئ لا كاريويلا، على بُعد نحو خمس دقائق سيرًا بحسب خريطة المطوّر، ومرسى بينالمادينا على امتداد الساحل.',
  'Het strand van La Carihuela, op ongeveer vijf minuten lopen volgens de kaart van de ontwikkelaar, met de jachthaven van Benalmádena verderop langs de kust.',
  'Plaża La Carihuela, około pięciu minut pieszo według mapy dewelopera, a dalej wzdłuż wybrzeża przystań jachtowa Benalmádeny.',
  'Stranden La Carihuela, rundt fem minutters gange ifølge utbyggerens kart, med marinaen i Benalmádena lenger langs kysten.',
  'Stranden La Carihuela, omkring fem minuters promenad enligt exploatörens karta, med marinan i Benalmádena längre längs kusten.')

# ---- location --------------------------------------------------------------------------------

a('.location.headlineHtml',
  'Torremolinos, <em>cerca de La Carihuela</em>', 'Torremolinos, <em>près de La Carihuela</em>', 'Torremolinos, <em>nahe La Carihuela</em>',
  'Торремолинос, <em>рядом с Ла-Каригуэлой</em>', 'توريمولينوس، <em>قرب لا كاريويلا</em>', 'Torremolinos, <em>bij La Carihuela</em>',
  'Torremolinos, <em>blisko La Carihueli</em>', 'Torremolinos, <em>nær La Carihuela</em>', 'Torremolinos, <em>nära La Carihuela</em>')
a('.location.mapLabelPlain',
  'Torremolinos, cerca de La Carihuela', 'Torremolinos, près de La Carihuela', 'Torremolinos, nahe La Carihuela',
  'Торремолинос, рядом с Ла-Каригуэлой', 'توريمولينوس، قرب لا كاريويلا', 'Torremolinos, bij La Carihuela',
  'Torremolinos, blisko La Carihueli', 'Torremolinos, nær La Carihuela', 'Torremolinos, nära La Carihuela')
a('.location.copy',
  'Los planos del promotor dan como dirección Av. Carlota Alessandri 109, en Torremolinos, en una manzana entre esa avenida, la calle Nerja, la calle Puerto Real y la Av. de España; el punto del mapa está dentro de ella y es aproximado. El folleto indica unos cinco minutos a pie hasta la playa de La Carihuela, menos de diez minutos en coche hasta el aeropuerto de Málaga y unos quince hasta el centro de Málaga. Confirmamos los tiempos a pie y en coche en una visita.',
  'Les plans du promoteur donnent pour adresse Av. Carlota Alessandri 109, à Torremolinos, sur un îlot entre cette avenue, la calle Nerja, la calle Puerto Real et l’Av. de España ; le repère sur la carte est placé à l’intérieur et reste approximatif. La brochure indique environ cinq minutes à pied jusqu’à la plage de La Carihuela, moins de dix minutes en voiture jusqu’à l’aéroport de Malaga et une quinzaine jusqu’au centre de Malaga. Nous confirmons les temps à pied et en voiture lors d’une visite.',
  'Die Pläne des Bauträgers nennen als Adresse Av. Carlota Alessandri 109 in Torremolinos, auf einem Block zwischen dieser Allee, der Calle Nerja, der Calle Puerto Real und der Av. de España; die Kartenmarkierung liegt darin und ist ungefähr. Die Broschüre nennt etwa fünf Gehminuten zum Strand La Carihuela, weniger als zehn Autominuten zum Flughafen Malaga und etwa fünfzehn ins Zentrum von Malaga. Geh- und Fahrzeiten bestätigen wir bei einem Besuch.',
  'На планах застройщика указан адрес Av. Carlota Alessandri 109 в Торремолиносе — квартал между этим проспектом, улицами Calle Nerja и Calle Puerto Real и Av. de España; метка на карте стоит внутри него и приблизительна. Буклет указывает около пяти минут пешком до пляжа Ла-Каригуэла, менее десяти минут на машине до аэропорта Малаги и около пятнадцати до центра Малаги. Время в пути пешком и на машине мы уточняем при осмотре.',
  'تذكر مخططات المطوّر العنوان Av. Carlota Alessandri 109 في توريمولينوس، في مربّع سكني بين هذه الجادة وشارع Calle Nerja وشارع Calle Puerto Real وجادة Av. de España؛ وعلامة الخريطة موضوعة داخله وهي تقريبية. ويذكر الكتيّب نحو خمس دقائق سيرًا إلى شاطئ لا كاريويلا، وأقل من عشر دقائق بالسيارة إلى مطار مالقة، ونحو خمس عشرة دقيقة إلى وسط مالقة. ونؤكد أوقات المشي والقيادة خلال الزيارة.',
  'De plannen van de ontwikkelaar geven als adres Av. Carlota Alessandri 109 in Torremolinos, op een bouwblok tussen die laan, de Calle Nerja, de Calle Puerto Real en de Av. de España; de markering op de kaart staat daarbinnen en is bij benadering. De brochure noemt ongeveer vijf minuten lopen naar het strand van La Carihuela, minder dan tien minuten rijden naar de luchthaven van Málaga en ongeveer vijftien naar het centrum van Málaga. Loop- en rijtijden bevestigen wij bij een bezoek.',
  'Rzuty dewelopera podają adres Av. Carlota Alessandri 109 w Torremolinos, w kwartale między tą aleją, Calle Nerja, Calle Puerto Real i Av. de España; znacznik na mapie stoi wewnątrz niego i jest przybliżony. Broszura podaje około pięciu minut pieszo do plaży La Carihuela, niecałe dziesięć minut samochodem do lotniska w Maladze i około piętnastu do centrum Malagi. Czasy dojścia i dojazdu potwierdzamy podczas wizyty.',
  'Utbyggerens tegninger oppgir adressen Av. Carlota Alessandri 109 i Torremolinos, i et kvartal mellom denne avenyen, Calle Nerja, Calle Puerto Real og Av. de España; kartmarkøren står inne i kvartalet og er omtrentlig. Brosjyren oppgir rundt fem minutters gange til stranden La Carihuela, under ti minutter med bil til Málaga lufthavn og rundt femten til Málaga sentrum. Gang- og kjøretider bekrefter vi ved en visning.',
  'Exploatörens ritningar anger adressen Av. Carlota Alessandri 109 i Torremolinos, i ett kvarter mellan den avenyn, Calle Nerja, Calle Puerto Real och Av. de España; kartmarkeringen står inne i kvarteret och är ungefärlig. Broschyren anger omkring fem minuters promenad till stranden La Carihuela, under tio minuter med bil till Málagas flygplats och omkring femton till Málaga centrum. Gång- och körtider bekräftar vi vid ett besök.')
a('.location.distances[0][0]',
  'Playa de La Carihuela', 'Plage de La Carihuela', 'Strand La Carihuela', 'Пляж Ла-Каригуэла', 'شاطئ لا كاريويلا',
  'Strand van La Carihuela', 'Plaża La Carihuela', 'Stranden La Carihuela', 'Stranden La Carihuela')
a('.location.distances[0][1]',
  'Unos 5 minutos a pie', 'Environ 5 minutes à pied', 'Etwa 5 Minuten zu Fuß', 'Около 5 минут пешком', 'نحو 5 دقائق سيرًا',
  'Ongeveer 5 minuten lopen', 'Około 5 minut pieszo', 'Rundt 5 minutters gange', 'Omkring 5 minuters promenad')
a('.location.distances[1][1]',
  'Menos de 10 minutos en coche', 'Moins de 10 minutes en voiture', 'Unter 10 Minuten mit dem Auto', 'Менее 10 минут на машине',
  'أقل من 10 دقائق بالسيارة', 'Minder dan 10 minuten met de auto', 'Poniżej 10 minut samochodem', 'Under 10 minutter med bil',
  'Under 10 minuter med bil')
a('.location.distances[2][1]',
  'Unos 15 minutos en coche', 'Environ 15 minutes en voiture', 'Etwa 15 Minuten mit dem Auto', 'Около 15 минут на машине',
  'نحو 15 دقيقة بالسيارة', 'Ongeveer 15 minuten met de auto', 'Około 15 minut samochodem', 'Rundt 15 minutter med bil',
  'Omkring 15 minuter med bil')

# ---- investment, trust -----------------------------------------------------------------------

a('.investment.cards[0][1]',
  'Cuatro viviendas figuran en la lista, de 353: un dormitorio a {E378000}, dos dormitorios a {E472000}, tres dormitorios a {E597000} y cuatro dormitorios a {E1040000}.',
  'Quatre logements figurent sur la liste, sur 353 : une chambre à {E378000}, deux chambres à {E472000}, trois chambres à {E597000} et quatre chambres à {E1040000}.',
  'Vier Wohnungen stehen auf der Liste, von 353: ein Schlafzimmer für {E378000}, zwei Schlafzimmer für {E472000}, drei Schlafzimmer für {E597000} und vier Schlafzimmer für {E1040000}.',
  'В списке четыре квартиры из 353: с одной спальней за {E378000}, с двумя за {E472000}, с тремя за {E597000} и с четырьмя за {E1040000}.',
  'أربعة مساكن مدرجة في القائمة من أصل 353: غرفة نوم واحدة بسعر {E378000}، وغرفتا نوم بسعر {E472000}، وثلاث غرف نوم بسعر {E597000}، وأربع غرف نوم بسعر {E1040000}.',
  'Vier woningen staan op de lijst, van de 353: één slaapkamer voor {E378000}, twee slaapkamers voor {E472000}, drie slaapkamers voor {E597000} en vier slaapkamers voor {E1040000}.',
  'W cenniku są cztery lokale z 353: z jedną sypialnią za {E378000}, z dwiema za {E472000}, z trzema za {E597000} i z czterema za {E1040000}.',
  'Fire boliger står på listen, av 353: ett soverom til {E378000}, to soverom til {E472000}, tre soverom til {E597000} og fire soverom til {E1040000}.',
  'Fyra bostäder finns på listan, av 353: ett sovrum för {E378000}, två sovrum för {E472000}, tre sovrum för {E597000} och fyra sovrum för {E1040000}.')
a('.investment.cards[1][1]',
  'La lista de precios no indica si el {T} está incluido ni menciona plaza de garaje o trastero. Con el {T} al 10% y el AJD al 1,20%, un precio de {E378000} sin {T} pasaría a unos {E420000}, antes de notaría y registro. Confirmamos ambos puntos por escrito.',
  'La liste de prix ne précise pas si la {T} est incluse et ne mentionne ni parking ni cave. Avec une {T} de 10% et un droit de timbre de 1,20%, un prix de {E378000} hors {T} passerait à environ {E420000}, avant les frais de notaire et d’enregistrement. Nous confirmons ces deux points par écrit.',
  'Die Preisliste sagt nicht, ob die {T} enthalten ist, und erwähnt weder Stellplatz noch Abstellraum. Mit 10% {T} und 1,20% Stempelsteuer würde ein Preis von {E378000} vor {T} zu etwa {E420000}, vor Notar- und Grundbuchkosten. Beide Punkte bestätigen wir schriftlich.',
  'В прайс-листе не сказано, включён ли {T}, и не упомянуты ни парковочное место, ни кладовая. При {T} 10% и гербовом сборе 1,20% цена {E378000} без {T} составила бы около {E420000}, без учёта нотариальных и регистрационных расходов. Оба вопроса мы подтверждаем письменно.',
  'لا تذكر قائمة الأسعار ما إذا كانت {T} مشمولة، ولا تشير إلى موقف سيارة أو مخزن. ومع {T} بنسبة 10% ورسم دمغة بنسبة 1.20%، يصبح سعر {E378000} قبل {T} نحو {E420000}، قبل رسوم الكاتب العدل والسجل العقاري. ونؤكد النقطتين كتابيًا.',
  'De prijslijst vermeldt niet of de {T} is inbegrepen en noemt geen parkeerplaats of berging. Met 10% {T} en 1,20% zegelbelasting wordt een prijs van {E378000} exclusief {T} ongeveer {E420000}, vóór notaris- en kadasterkosten. Beide punten bevestigen wij schriftelijk.',
  'Cennik nie podaje, czy {T} jest wliczony, ani nie wspomina o miejscu parkingowym czy komórce lokatorskiej. Przy {T} 10% i opłacie skarbowej 1,20% cena {E378000} bez {T} wyniosłaby około {E420000}, przed opłatami notarialnymi i wieczystoksięgowymi. Oba punkty potwierdzamy na piśmie.',
  'Prislisten sier ikke om {T} er inkludert, og nevner verken parkeringsplass eller bod. Med 10 % {T} og 1,20 % dokumentavgift blir en pris på {E378000} før {T} omtrent {E420000}, før notar- og tinglysingsgebyrer. Begge punktene bekrefter vi skriftlig.',
  'Prislistan anger inte om {T} (spansk moms) ingår, och nämner varken parkeringsplats eller förråd. Med 10 % {T} och 1,20 % stämpelskatt blir ett pris på {E378000} före {T} omkring {E420000}, före notarie- och inskrivningsavgifter. Båda punkterna bekräftar vi skriftligt.')
a('.investment.cards[2][1]',
  'Ningún documento indica una licencia, el estado de las obras ni una fecha de entrega.',
  'Aucun document n’indique de permis, d’état d’avancement des travaux ni de date de livraison.',
  'Kein Dokument nennt eine Baugenehmigung, den Baufortschritt oder einen Fertigstellungstermin.',
  'Ни один документ не указывает разрешение, стадию работ или срок сдачи.',
  'لا تذكر أي وثيقة ترخيصًا أو مرحلة الأعمال أو موعدًا للإنجاز.',
  'Geen enkel document vermeldt een vergunning, de stand van de werken of een opleverdatum.',
  'Żaden dokument nie podaje pozwolenia, etapu prac ani terminu oddania.',
  'Ingen dokumenter oppgir tillatelse, byggefase eller ferdigstillelsesdato.',
  'Inget dokument anger bygglov, byggskede eller färdigställandedatum.')
a('.investment.cards[3][1]',
  'La tabla es una copia del portal del promotor del 25 de noviembre de 2026. Reconfirmamos la cifra con el vendedor antes de que usted reserve.',
  'Le tableau est une copie du portail du promoteur au 25 novembre 2026. Nous reconfirmons le montant auprès du vendeur avant que vous ne réserviez.',
  'Die Tabelle ist eine Kopie des Portals des Bauträgers vom 25. November 2026. Wir bestätigen den Betrag beim Verkäufer erneut, bevor Sie reservieren.',
  'Таблица — копия портала застройщика на 25 ноября 2026 года. Мы повторно подтверждаем сумму у продавца до того, как вы забронируете.',
  'الجدول نسخة من بوابة المطوّر بتاريخ 25 نوفمبر 2026. ونعيد تأكيد المبلغ مع البائع قبل أن تحجزوا.',
  'De tabel is een kopie van het portaal van de ontwikkelaar op 25 november 2026. Wij bevestigen het bedrag opnieuw bij de verkoper voordat u reserveert.',
  'Tabela jest kopią portalu dewelopera z 25 listopada 2026 roku. Przed Państwa rezerwacją ponownie potwierdzamy kwotę u sprzedającego.',
  'Tabellen er en kopi av utbyggerens portal per 25. november 2026. Vi bekrefter beløpet på nytt med selgeren før De reserverer.',
  'Tabellen är en kopia av exploatörens portal den 25 november 2026. Vi bekräftar beloppet på nytt med säljaren innan ni bokar.')
a('.trustDossier.cards[0][0]',
  '{T}, garaje y trastero', '{T}, parking et cave', '{T}, Stellplatz und Abstellraum', '{T}, парковка и кладовая',
  '{T} والموقف والمخزن', '{T}, parkeerplaats en berging', '{T}, miejsce parkingowe i komórka', '{T}, parkering og bod',
  '{T}, parkering och förråd')
a('.trustDossier.cards[0][1]',
  'La lista de precios no indica si sus precios incluyen el {T}, ni si la vivienda lleva plaza de garaje o trastero. Las imágenes del promotor muestran un garaje subterráneo. Pedimos los tres puntos por escrito.',
  'La liste de prix ne précise pas si ses prix incluent la {T}, ni si un parking ou une cave accompagne le logement. Les images du promoteur montrent un parking souterrain. Nous demandons les trois points par écrit.',
  'Die Preisliste sagt nicht, ob ihre Preise die {T} enthalten, und nicht, ob ein Stellplatz oder ein Abstellraum zur Wohnung gehört. Die Bilder des Bauträgers zeigen eine Tiefgarage. Wir lassen uns alle drei Punkte schriftlich bestätigen.',
  'В прайс-листе не сказано, включён ли в цены {T} и прилагаются ли к квартире парковочное место или кладовая. На изображениях застройщика есть подземный гараж. Все три пункта мы запрашиваем письменно.',
  'لا تذكر قائمة الأسعار ما إذا كانت أسعارها تشمل {T}، ولا ما إذا كان المسكن يأتي مع موقف سيارة أو مخزن. وتُظهر صور المطوّر مرأبًا تحت الأرض. ونطلب النقاط الثلاث كتابيًا.',
  'De prijslijst vermeldt niet of de prijzen {T} bevatten, en ook niet of er een parkeerplaats of berging bij de woning hoort. De beelden van de ontwikkelaar tonen een ondergrondse garage. Wij vragen alle drie de punten schriftelijk op.',
  'Cennik nie podaje, czy ceny zawierają {T}, ani czy do lokalu należy miejsce parkingowe lub komórka lokatorska. Wizualizacje dewelopera pokazują garaż podziemny. O wszystkie trzy punkty prosimy na piśmie.',
  'Prislisten sier ikke om prisene inkluderer {T}, eller om det følger parkeringsplass eller bod med boligen. Utbyggerens bilder viser en parkeringskjeller. Vi ber om alle tre punktene skriftlig.',
  'Prislistan anger inte om priserna inkluderar {T}, eller om parkeringsplats eller förråd ingår i bostaden. Exploatörens bilder visar ett underjordiskt garage. Vi begär alla tre punkterna skriftligt.')
a('.trustDossier.cards[1][1]',
  'Ningún documento indica una licencia de obra, el estado de las obras ni una fecha de entrega. Pedimos la licencia, el calendario de obra y la fecha de entrega contractual.',
  'Aucun document n’indique de permis de construire, d’état d’avancement des travaux ni de date de livraison. Nous demandons le permis, le calendrier des travaux et la date de livraison contractuelle.',
  'Kein Dokument nennt eine Baugenehmigung, den Baufortschritt oder einen Fertigstellungstermin. Wir fordern die Genehmigung, den Bauzeitenplan und den vertraglichen Fertigstellungstermin an.',
  'Ни один документ не указывает разрешение на строительство, стадию работ или срок сдачи. Мы запрашиваем разрешение, график работ и договорной срок сдачи.',
  'لا تذكر أي وثيقة رخصة بناء أو مرحلة الأعمال أو موعدًا للإنجاز. ونطلب الرخصة والجدول الزمني للأعمال وموعد الإنجاز التعاقدي.',
  'Geen enkel document vermeldt een bouwvergunning, de stand van de werken of een opleverdatum. Wij vragen de vergunning, de bouwplanning en de contractuele opleverdatum op.',
  'Żaden dokument nie podaje pozwolenia na budowę, etapu prac ani terminu oddania. Prosimy o pozwolenie, harmonogram prac i umowny termin oddania.',
  'Ingen dokumenter oppgir byggetillatelse, byggefase eller ferdigstillelsesdato. Vi ber om tillatelsen, fremdriftsplanen og den kontraktsfestede ferdigstillelsesdatoen.',
  'Inget dokument anger bygglov, byggskede eller färdigställandedatum. Vi begär bygglovet, tidplanen och det avtalade färdigställandedatumet.')
a('.trustDossier.cards[2][1]',
  'En 11B y 35C la superficie construida de la lista es la superficie construida de la vivienda en el plano. En 16-2D y 13-2B la lista da {N66.00} y {N87.00} {U}, cerca de las cifras de los planos con zonas comunes ({N66.30} y {N87.07} {U}), mientras que los planos dan {N55.38} y {N71.40} {U} para la vivienda en sí; la lista redondea sus terrazas a {N13.00} {U}, los planos dan {N13.28} y {N12.97} {U}. Esta página toma ambas cifras de los planos.',
  'Pour 11B et 35C, la surface construite de la liste est celle du logement sur le plan. Pour 16-2D et 13-2B, la liste donne {N66.00} et {N87.00} {U}, proches des chiffres des plans parties communes comprises ({N66.30} et {N87.07} {U}), alors que les plans donnent {N55.38} et {N71.40} {U} pour le logement lui-même ; la liste arrondit leurs terrasses à {N13.00} {U}, les plans donnent {N13.28} et {N12.97} {U}. Cette page reprend les deux chiffres des plans.',
  'Bei 11B und 35C entspricht die bebaute Fläche der Liste der bebauten Fläche der Wohnung laut Plan. Bei 16-2D und 13-2B nennt die Liste {N66.00} und {N87.00} {U}, nahe an den Planwerten inklusive Gemeinschaftsflächen ({N66.30} und {N87.07} {U}), während die Pläne für die Wohnung selbst {N55.38} und {N71.40} {U} angeben; die Liste rundet ihre Terrassen auf {N13.00} {U}, die Pläne nennen {N13.28} und {N12.97} {U}. Diese Seite übernimmt beide Werte aus den Plänen.',
  'У 11B и 35C площадь застройки в списке совпадает с площадью квартиры на плане. У 16-2D и 13-2B список указывает {N66.00} и {N87.00} {U} — близко к цифрам планов с учётом мест общего пользования ({N66.30} и {N87.07} {U}), тогда как для самих квартир планы дают {N55.38} и {N71.40} {U}; террасы список округляет до {N13.00} {U}, а планы дают {N13.28} и {N12.97} {U}. На этой странице обе цифры взяты из планов.',
  'في 11B و35C تطابق المساحة المبنية في القائمة المساحة المبنية للمسكن في المخطط. أما في 16-2D و13-2B فتذكر القائمة {N66.00} و{N87.00} {U}، وهي قريبة من أرقام المخططات شاملة المناطق المشتركة ({N66.30} و{N87.07} {U})، بينما تذكر المخططات {N55.38} و{N71.40} {U} للمسكن نفسه؛ وتقرّب القائمة تراساتهما إلى {N13.00} {U}، في حين تذكر المخططات {N13.28} و{N12.97} {U}. وتأخذ هذه الصفحة الرقمين من المخططات.',
  'Bij 11B en 35C is de bebouwde oppervlakte op de lijst die van de woning op de plattegrond. Bij 16-2D en 13-2B geeft de lijst {N66.00} en {N87.00} {U}, dicht bij de cijfers van de plannen inclusief gemeenschappelijke delen ({N66.30} en {N87.07} {U}), terwijl de plannen {N55.38} en {N71.40} {U} geven voor de woning zelf; de lijst rondt hun terrassen af op {N13.00} {U}, de plannen geven {N13.28} en {N12.97} {U}. Deze pagina neemt beide cijfers uit de plannen.',
  'W 11B i 35C powierzchnia zabudowy z cennika to powierzchnia lokalu z rzutu. W 16-2D i 13-2B cennik podaje {N66.00} i {N87.00} {U}, blisko wartości z rzutów wraz z częściami wspólnymi ({N66.30} i {N87.07} {U}), podczas gdy rzuty podają {N55.38} i {N71.40} {U} dla samego lokalu; tarasy cennik zaokrągla do {N13.00} {U}, rzuty podają {N13.28} i {N12.97} {U}. Ta strona przyjmuje obie wartości z rzutów.',
  'For 11B og 35C er listens bygde areal boligens bygde areal på tegningen. For 16-2D og 13-2B oppgir listen {N66.00} og {N87.00} {U}, nær tegningenes tall inkludert fellesarealer ({N66.30} og {N87.07} {U}), mens tegningene oppgir {N55.38} og {N71.40} {U} for selve boligen; listen runder terrassene av til {N13.00} {U}, tegningene oppgir {N13.28} og {N12.97} {U}. Denne siden henter begge tallene fra tegningene.',
  'För 11B och 35C är listans byggyta bostadens byggyta på ritningen. För 16-2D och 13-2B anger listan {N66.00} och {N87.00} {U}, nära ritningarnas siffror inklusive gemensamma ytor ({N66.30} och {N87.07} {U}), medan ritningarna anger {N55.38} och {N71.40} {U} för själva bostaden; listan avrundar terrasserna till {N13.00} {U}, ritningarna anger {N13.28} och {N12.97} {U}. Den här sidan tar båda siffrorna från ritningarna.')
a('.trustDossier.cards[3][0]',
  'Nivel -2', 'Niveau -2', 'Ebene -2', 'Уровень -2', 'المستوى -2', 'Niveau -2', 'Poziom -2', 'Nivå -2', 'Plan -2')
a('.trustDossier.cards[3][1]',
  'Las dos viviendas más económicas están en el nivel que los planos llaman -2. Sus planos muestran terrazas bordeadas de vegetación, pero ningún documento dice hacia dónde dan ni cuánta luz reciben. Lo vemos sobre el terreno.',
  'Les deux logements les moins chers sont au niveau que les plans appellent -2. Leurs plans montrent des terrasses bordées de végétation, mais aucun document ne dit sur quoi elles donnent ni quelle lumière elles reçoivent. Nous le vérifions sur place.',
  'Die beiden günstigsten Wohnungen liegen auf der Ebene, die die Pläne -2 nennen. Ihre Pläne zeigen von Bepflanzung gesäumte Terrassen, aber kein Dokument sagt, wohin sie ausgerichtet sind oder wie viel Tageslicht sie bekommen. Das sehen wir uns vor Ort an.',
  'Две самые доступные квартиры находятся на уровне, который на планах обозначен как -2. Планы показывают террасы, окаймлённые зеленью, но ни один документ не говорит, куда они выходят и сколько у них дневного света. Мы смотрим это на месте.',
  'يقع المسكنان الأقل سعرًا في المستوى الذي تسميه المخططات -2. وتُظهر مخططاتهما تراسات تحيط بها النباتات، لكن لا تذكر أي وثيقة إلى أين تطلّ ولا مقدار الضوء الذي تتلقاه. ونعاين ذلك في الموقع.',
  'De twee goedkoopste woningen liggen op het niveau dat de plannen -2 noemen. Hun plattegronden tonen terrassen omzoomd door beplanting, maar geen enkel document zegt waar ze op uitkijken of hoeveel daglicht ze krijgen. Dat bekijken wij ter plaatse.',
  'Dwa najtańsze lokale znajdują się na poziomie, który rzuty oznaczają jako -2. Ich rzuty pokazują tarasy obsadzone zielenią, ale żaden dokument nie mówi, na co wychodzą ani ile mają światła dziennego. Sprawdzamy to na miejscu.',
  'De to rimeligste boligene ligger på nivået tegningene kaller -2. Tegningene viser terrasser omkranset av beplantning, men ingen dokumenter sier hva de vender mot eller hvor mye dagslys de får. Det ser vi på stedet.',
  'De två billigaste bostäderna ligger på det plan som ritningarna kallar -2. Ritningarna visar terrasser kantade av växtlighet, men inget dokument säger vad de vetter mot eller hur mycket dagsljus de får. Det ser vi på plats.')
a('.trustDossier.cards[4][1]',
  'No se ha podido obtener la memoria de calidades, por lo que esta página no indica acabados, equipamiento ni electrodomésticos. La pedimos antes de cualquier reserva.',
  'Le descriptif technique n’a pas pu être obtenu ; cette page n’indique donc ni finitions, ni équipements, ni électroménager. Nous le demandons avant toute réservation.',
  'Die Baubeschreibung war nicht erhältlich, daher nennt diese Seite keine Ausstattung, Armaturen oder Geräte. Wir fordern sie vor jeder Reservierung an.',
  'Спецификацию получить не удалось, поэтому на этой странице нет отделки, оснащения и бытовой техники. Мы запрашиваем её до любого бронирования.',
  'تعذّر الحصول على مواصفات البناء، لذا لا تذكر هذه الصفحة التشطيبات أو التجهيزات أو الأجهزة. ونطلبها قبل أي حجز.',
  'Het lastenboek was niet te krijgen, dus deze pagina noemt geen afwerking, uitrusting of apparaten. Wij vragen het op vóór elke reservering.',
  'Nie udało się uzyskać specyfikacji technicznej, dlatego ta strona nie podaje wykończeń, wyposażenia ani sprzętu AGD. Prosimy o nią przed każdą rezerwacją.',
  'Byggebeskrivelsen har ikke vært mulig å skaffe, så denne siden oppgir ingen overflater, utstyr eller hvitevarer. Vi ber om den før en eventuell reservasjon.',
  'Byggbeskrivningen har inte gått att få fram, så den här sidan anger inga ytskikt, inredning eller vitvaror. Vi begär den före en eventuell bokning.')

# ---- availability ----------------------------------------------------------------------------

a('.availability.copy',
  'La lista de precios del promotor, a noviembre de 2026, recoge cuatro viviendas, de uno, dos, tres y cuatro dormitorios. La disponibilidad y los precios proceden de la lista del promotor a noviembre de 2026 y se confirman antes de la reserva.',
  'La liste de prix du promoteur, à novembre 2026, compte quatre logements, d’une, deux, trois et quatre chambres. Disponibilité et prix proviennent de la liste du promoteur à novembre 2026 et sont confirmés avant réservation.',
  'Die Preisliste des Bauträgers mit Stand November 2026 nennt vier Wohnungen mit einem, zwei, drei und vier Schlafzimmern. Verfügbarkeit und Preise stammen aus der Liste des Bauträgers mit Stand November 2026 und werden vor der Reservierung bestätigt.',
  'В прайс-листе застройщика на ноябрь 2026 года четыре квартиры: с одной, двумя, тремя и четырьмя спальнями. Наличие и цены — по списку застройщика на ноябрь 2026 года, они подтверждаются до бронирования.',
  'تضم قائمة أسعار المطوّر، حتى نوفمبر 2026، أربعة مساكن بغرفة وغرفتين وثلاث وأربع غرف نوم. والتوفر والأسعار مأخوذة من قائمة المطوّر حتى نوفمبر 2026، ويتم تأكيدها قبل الحجز.',
  'De prijslijst van de ontwikkelaar, per november 2026, noemt vier woningen, met één, twee, drie en vier slaapkamers. Beschikbaarheid en prijzen komen uit de lijst van de ontwikkelaar per november 2026 en worden vóór reservering bevestigd.',
  'Cennik dewelopera, według stanu na listopad 2026 roku, obejmuje cztery lokale z jedną, dwiema, trzema i czterema sypialniami. Dostępność i ceny pochodzą z cennika dewelopera według stanu na listopad 2026 roku i są potwierdzane przed rezerwacją.',
  'Utbyggerens prisliste per november 2026 har fire boliger, med ett, to, tre og fire soverom. Tilgjengelighet og priser er fra utbyggerens liste per november 2026 og bekreftes før reservasjon.',
  'Exploatörens prislista per november 2026 tar upp fyra bostäder, med ett, två, tre och fyra sovrum. Tillgänglighet och priser är hämtade ur exploatörens lista per november 2026 och bekräftas före bokning.')
a('.availability.sourceNote',
  'Precios, plantas, dormitorios y baños transcritos de la tabla de precios del portal de agentes del promotor, copiada el 25 de noviembre de 2026, que marca las cuatro viviendas como disponibles. La lista no indica si el {T} está incluido, ni si lo están el garaje o el trastero; confirmamos ambos puntos por escrito. Las superficies construidas y las terrazas proceden de los planos del promotor: la lista da {N66.00} y {N87.00} {U} construidos y {N13.00} {U} de terraza para 16-2D y 13-2B, cifras que incluyen una parte de las zonas comunes, frente a {N55.38} y {N71.40} {U} construidos y {N13.28} y {N12.97} {U} de terraza en sus planos.',
  'Prix, étages, chambres et salles de bains transcrits du tableau de prix du portail agents du promoteur, copié le 25 novembre 2026, qui indique les quatre logements comme disponibles. La liste ne précise pas si la {T} est incluse, ni si le parking ou la cave le sont ; nous confirmons ces deux points par écrit. Les surfaces construites et les terrasses proviennent des plans du promoteur : la liste donne {N66.00} et {N87.00} {U} construits et {N13.00} {U} de terrasse pour 16-2D et 13-2B, chiffres qui incluent une quote-part des parties communes, contre {N55.38} et {N71.40} {U} construits et {N13.28} et {N12.97} {U} de terrasse sur leurs plans.',
  'Preise, Geschosse, Schlafzimmer und Bäder sind aus der Preistabelle des Maklerportals des Bauträgers übernommen, kopiert am 25. November 2026, die alle vier Wohnungen als verfügbar ausweist. Die Liste sagt nicht, ob die {T} enthalten ist und ob Stellplatz oder Abstellraum dazugehören; beides bestätigen wir schriftlich. Bebaute Flächen und Terrassen stammen aus den Plänen des Bauträgers: Die Liste nennt für 16-2D und 13-2B {N66.00} und {N87.00} {U} bebaute Fläche und {N13.00} {U} Terrasse, Werte mit Anteil an den Gemeinschaftsflächen, gegenüber {N55.38} und {N71.40} {U} bebauter Fläche und {N13.28} und {N12.97} {U} Terrasse auf ihren Plänen.',
  'Цены, этажи, спальни и ванные взяты из таблицы цен агентского портала застройщика, скопированной 25 ноября 2026 года, где все четыре квартиры отмечены как свободные. В списке не сказано, включён ли {T}, а также парковка и кладовая; оба вопроса мы подтверждаем письменно. Площади застройки и террас взяты из планов застройщика: для 16-2D и 13-2B список даёт {N66.00} и {N87.00} {U} площади застройки и {N13.00} {U} террасы — цифры с долей мест общего пользования — против {N55.38} и {N71.40} {U} площади застройки и {N13.28} и {N12.97} {U} террасы на их планах.',
  'الأسعار والطوابق وغرف النوم والحمّامات منقولة من جدول أسعار بوابة الوكلاء لدى المطوّر، المنسوخ في 25 نوفمبر 2026، والذي يبيّن أن المساكن الأربعة متاحة. ولا تذكر القائمة ما إذا كانت {T} مشمولة، ولا ما إذا كان الموقف أو المخزن مشمولين؛ ونؤكد النقطتين كتابيًا. والمساحات المبنية والتراسات مأخوذة من مخططات المطوّر: إذ تذكر القائمة لـ16-2D و13-2B مساحة مبنية قدرها {N66.00} و{N87.00} {U} وتراسًا قدره {N13.00} {U}، وهي أرقام تشمل حصة من المناطق المشتركة، مقابل {N55.38} و{N71.40} {U} مساحة مبنية و{N13.28} و{N12.97} {U} تراسًا في مخططاتهما.',
  'Prijzen, verdiepingen, slaapkamers en badkamers zijn overgenomen uit de prijstabel van het makelaarsportaal van de ontwikkelaar, gekopieerd op 25 november 2026, die alle vier de woningen als beschikbaar aanduidt. De lijst vermeldt niet of de {T} is inbegrepen, en ook niet of een parkeerplaats of berging dat is; beide bevestigen wij schriftelijk. Bebouwde oppervlakten en terrassen komen uit de plannen van de ontwikkelaar: de lijst geeft voor 16-2D en 13-2B {N66.00} en {N87.00} {U} bebouwd en {N13.00} {U} terras, cijfers met een aandeel in de gemeenschappelijke delen, tegenover {N55.38} en {N71.40} {U} bebouwd en {N13.28} en {N12.97} {U} terras op hun plattegronden.',
  'Ceny, piętra, sypialnie i łazienki przepisano z tabeli cen portalu dla agentów dewelopera, skopiowanej 25 listopada 2026 roku, która oznacza wszystkie cztery lokale jako dostępne. Cennik nie podaje, czy {T} jest wliczony, ani czy wliczone są miejsce parkingowe lub komórka; oba punkty potwierdzamy na piśmie. Powierzchnie zabudowy i tarasy pochodzą z rzutów dewelopera: dla 16-2D i 13-2B cennik podaje {N66.00} i {N87.00} {U} powierzchni zabudowy i {N13.00} {U} tarasu, wartości z udziałem w częściach wspólnych, wobec {N55.38} i {N71.40} {U} powierzchni zabudowy oraz {N13.28} i {N12.97} {U} tarasu na ich rzutach.',
  'Priser, etasjer, soverom og bad er hentet fra pristabellen på utbyggerens meglerportal, kopiert 25. november 2026, som merker alle fire boligene som ledige. Listen sier ikke om {T} er inkludert, eller om parkering eller bod er det; begge deler bekrefter vi skriftlig. Bebygd areal og terrasser er fra utbyggerens tegninger: listen oppgir {N66.00} og {N87.00} {U} bygd areal og {N13.00} {U} terrasse for 16-2D og 13-2B, tall som inkluderer en andel av fellesarealene, mot {N55.38} og {N71.40} {U} bygd areal og {N13.28} og {N12.97} {U} terrasse på tegningene.',
  'Priser, våningar, sovrum och badrum är hämtade ur pristabellen på exploatörens mäklarportal, kopierad den 25 november 2026, som anger alla fyra bostäderna som lediga. Listan anger inte om {T} (spansk moms) ingår, eller om parkering eller förråd gör det; båda punkterna bekräftar vi skriftligt. Byggytor och terrasser är hämtade ur exploatörens ritningar: listan anger {N66.00} och {N87.00} {U} byggyta och {N13.00} {U} terrass för 16-2D och 13-2B, siffror som inkluderar en andel av de gemensamma ytorna, mot {N55.38} och {N71.40} {U} byggyta och {N13.28} och {N12.97} {U} terrass på deras ritningar.')
SIZE = {'es': '{b} {U} construidos, {t} {U} de terraza', 'fr': '{b} {U} construits, {t} {U} de terrasse',
        'de': '{b} {U} bebaute Fläche, {t} {U} Terrasse', 'ru': '{b} {U} площадь застройки, терраса {t} {U}',
        'ar': '{b} {U} مساحة مبنية، {t} {U} تراس', 'nl': '{b} {U} bebouwd, {t} {U} terras',
        'pl': '{b} {U} powierzchni zabudowy, {t} {U} tarasu', 'no': '{b} {U} bygd areal, {t} {U} terrasse',
        'sv': '{b} {U} byggyta, {t} {U} terrass'}
for u in proj['availability']['units']:
    b, t = re.match(r'([\d.]+) sqm built, ([\d.]+) sqm terrace', u['size']).groups()
    put(u['size'], [SIZE[l].replace('{b}', f'{{N{b}}}').replace('{t}', f'{{N{t}}}') for l in LOCS])

# ---- built-area range (house shape "sqm built"; Norwegian takes the settled "bygd areal") ------

for path in ('.quickFacts[4][1]', '.overview.metrics[2][1]'):
    a(path, '{N55.38} - {N121.94} {U} construidos', '{N55.38} - {N121.94} {U} construits', '{N55.38} - {N121.94} {U} bebaute Fläche',
      '{N55.38} - {N121.94} {U} площадь застройки', '{N55.38} - {N121.94} {U} مساحة مبنية', '{N55.38} - {N121.94} {U} bebouwd',
      '{N55.38} - {N121.94} {U} powierzchni zabudowy', '{N55.38} - {N121.94} {U} bygd areal', '{N55.38} - {N121.94} {U} byggyta')
for path in ('.quickFacts[4][0]', '.overview.metrics[2][0]'):
    a(path, 'Superficie construida', 'Surface construite', 'Bebaute Fläche', 'Площадь застройки', 'المساحة المبنية',
      'Bebouwde oppervlakte', 'Powierzchnia zabudowy', 'Bebygd areal', 'Byggyta')

# ---- timeline, enquiry, FAQ ------------------------------------------------------------------

a('.timeline.items[0][2]',
  'Los planos de las viviendas que le interesen, el folleto y la lista de precios.',
  'Les plans des logements qui vous intéressent, la brochure et la liste de prix.',
  'Die Grundrisse der Wohnungen, die Sie interessieren, die Broschüre und die Preisliste.',
  'Планировки интересующих вас квартир, буклет и прайс-лист.',
  'مخططات المساكن التي تهمّكم، والكتيّب، وقائمة الأسعار.',
  'De plattegronden van de woningen die u interesseren, de brochure en de prijslijst.',
  'Rzuty lokali, które Państwa interesują, broszura i cennik.',
  'Plantegningene av boligene De er interessert i, brosjyren og prislisten.',
  'Planritningarna för de bostäder som intresserar er, broschyren och prislistan.')
a('.enquiry.headlineHtml',
  'Pregunte por <em>Calandria Residences</em>', 'Renseignez-vous sur <em>Calandria Residences</em>', 'Anfrage zu <em>Calandria Residences</em>',
  'Узнать о <em>Calandria Residences</em>', 'استفسروا عن <em>Calandria Residences</em>', 'Vraag naar <em>Calandria Residences</em>',
  'Zapytaj o <em>Calandria Residences</em>', 'Spør om <em>Calandria Residences</em>', 'Fråga om <em>Calandria Residences</em>')
a('.enquiry.message',
  'Hola Nueva Living, me gustaría recibir información sobre Calandria Residences.',
  'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Calandria Residences.',
  'Hallo Nueva Living, ich hätte gern Informationen zu Calandria Residences.',
  'Здравствуйте, Nueva Living! Я хотел(а) бы получить информацию о Calandria Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Calandria Residences.',
  'Hallo Nueva Living, ik wil graag informatie over Calandria Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje na temat Calandria Residences.',
  'Hei Nueva Living, jeg ønsker informasjon om Calandria Residences.',
  'Hej Nueva Living, jag skulle vilja ha information om Calandria Residences.')
a('.faq[0][1]',
  'Cuatro figuran en la lista de precios del promotor a noviembre de 2026, de las 353 del conjunto: un apartamento de un dormitorio a {E378000}, uno de dos a {E472000}, uno de tres a {E597000} y uno de cuatro a {E1040000}. Preguntamos qué más sale a la venta.',
  'Quatre figurent sur la liste de prix du promoteur à novembre 2026, sur les 353 de l’ensemble : un appartement d’une chambre à {E378000}, un de deux chambres à {E472000}, un de trois à {E597000} et un de quatre à {E1040000}. Nous demandons ce qui est mis en vente par ailleurs.',
  'Vier stehen auf der Preisliste des Bauträgers mit Stand November 2026, von den 353 der Anlage: eine Wohnung mit einem Schlafzimmer für {E378000}, eine mit zwei für {E472000}, eine mit drei für {E597000} und eine mit vier für {E1040000}. Wir fragen nach, was sonst freigegeben ist.',
  'В прайс-листе застройщика на ноябрь 2026 года четыре квартиры из 353 в комплексе: с одной спальней за {E378000}, с двумя за {E472000}, с тремя за {E597000} и с четырьмя за {E1040000}. Мы уточняем, что ещё выставлено в продажу.',
  'أربعة مساكن مدرجة في قائمة أسعار المطوّر حتى نوفمبر 2026، من أصل 353 في المجمّع: شقة بغرفة نوم واحدة بسعر {E378000}، وأخرى بغرفتين بسعر {E472000}، وثالثة بثلاث غرف بسعر {E597000}، ورابعة بأربع غرف بسعر {E1040000}. ونستفسر عمّا طُرح غيرها للبيع.',
  'Vier staan op de prijslijst van de ontwikkelaar per november 2026, van de 353 in het complex: een appartement met één slaapkamer voor {E378000}, een met twee voor {E472000}, een met drie voor {E597000} en een met vier voor {E1040000}. Wij vragen wat er verder in verkoop is.',
  'W cenniku dewelopera według stanu na listopad 2026 roku są cztery lokale z 353 w zespole: mieszkanie z jedną sypialnią za {E378000}, z dwiema za {E472000}, z trzema za {E597000} i z czterema za {E1040000}. Pytamy, co jeszcze jest w sprzedaży.',
  'Fire står på utbyggerens prisliste per november 2026, av de 353 i anlegget: en leilighet med ett soverom til {E378000}, en med to til {E472000}, en med tre til {E597000} og en med fire til {E1040000}. Vi spør hva mer som er lagt ut for salg.',
  'Fyra finns på exploatörens prislista per november 2026, av områdets 353: en lägenhet med ett sovrum för {E378000}, en med två för {E472000}, en med tre för {E597000} och en med fyra för {E1040000}. Vi frågar vad mer som släppts till försäljning.')
a('.faq[1][1]',
  'La lista de precios no lo indica. El {T} de una vivienda nueva es del 10% y el AJD del 1,20%, y a ello se suman la notaría y el registro. Confirmamos por escrito si los precios incluyen el {T}, y los gastos de compra.',
  'La liste de prix ne le précise pas. La {T} sur un logement neuf est de 10% et le droit de timbre de 1,20%, auxquels s’ajoutent les frais de notaire et d’enregistrement. Nous confirmons par écrit si les prix incluent la {T}, ainsi que les frais d’acquisition.',
  'Die Preisliste sagt es nicht. Die {T} auf eine Neubauwohnung beträgt 10% und die Stempelsteuer 1,20%, hinzu kommen Notar- und Grundbuchkosten. Wir bestätigen schriftlich, ob die Preise die {T} enthalten, und die Erwerbsnebenkosten.',
  'В прайс-листе об этом не сказано. {T} на новое жильё составляет 10%, гербовый сбор 1,20%, а нотариальные и регистрационные расходы оплачиваются отдельно. Мы письменно подтверждаем, включён ли {T} в цены, и расходы на покупку.',
  'لا تذكر قائمة الأسعار ذلك. وتبلغ {T} على المسكن الجديد 10% ورسم الدمغة 1.20%، وتُضاف إليهما رسوم الكاتب العدل والسجل العقاري. ونؤكد كتابيًا ما إذا كانت الأسعار تشمل {T}، وكذلك تكاليف الشراء.',
  'De prijslijst zegt het niet. De {T} op een nieuwbouwwoning is 10% en de zegelbelasting 1,20%, en daar komen notaris- en kadasterkosten bij. Wij bevestigen schriftelijk of de prijzen {T} bevatten, en de aankoopkosten.',
  'Cennik tego nie podaje. {T} od nowego mieszkania wynosi 10%, opłata skarbowa 1,20%, a do tego dochodzą opłaty notarialne i za wpis do księgi wieczystej. Potwierdzamy na piśmie, czy ceny zawierają {T}, oraz koszty zakupu.',
  'Prislisten sier det ikke. {T} på en ny bolig er 10 % og dokumentavgiften 1,20 %, og notar- og tinglysingsgebyrer kommer i tillegg. Vi bekrefter skriftlig om prisene inkluderer {T}, og kjøpskostnadene.',
  'Prislistan anger det inte. {T} (spansk moms) på en nyproducerad bostad är 10 % och stämpelskatten 1,20 %, och till det kommer notarie- och inskrivningsavgifter. Vi bekräftar skriftligt om priserna inkluderar {T}, och köpkostnaderna.')
a('.faq[2][1]',
  'La lista de precios no los menciona. Las imágenes del promotor muestran un garaje subterráneo; confirmamos por escrito qué incluye la vivienda que usted elija.',
  'La liste de prix ne les mentionne pas. Les images du promoteur montrent un parking souterrain ; nous confirmons par écrit ce qui accompagne le logement que vous choisissez.',
  'Die Preisliste erwähnt sie nicht. Die Bilder des Bauträgers zeigen eine Tiefgarage; wir bestätigen schriftlich, was zu der von Ihnen gewählten Wohnung gehört.',
  'В прайс-листе они не упомянуты. На изображениях застройщика есть подземный гараж; мы письменно подтверждаем, что входит в выбранную вами квартиру.',
  'لا تذكرهما قائمة الأسعار. وتُظهر صور المطوّر مرأبًا تحت الأرض؛ ونؤكد كتابيًا ما يشمله المسكن الذي تختارونه.',
  'De prijslijst noemt ze niet. De beelden van de ontwikkelaar tonen een ondergrondse garage; wij bevestigen schriftelijk wat er bij de door u gekozen woning hoort.',
  'Cennik o nich nie wspomina. Wizualizacje dewelopera pokazują garaż podziemny; potwierdzamy na piśmie, co obejmuje wybrany przez Państwa lokal.',
  'Prislisten nevner dem ikke. Utbyggerens bilder viser en parkeringskjeller; vi bekrefter skriftlig hva som følger med boligen De velger.',
  'Prislistan nämner dem inte. Exploatörens bilder visar ett underjordiskt garage; vi bekräftar skriftligt vad som ingår i den bostad ni väljer.')
a('.faq[4][0]',
  '¿A qué distancia está la playa?', 'À quelle distance se trouve la plage ?', 'Wie weit ist es zum Strand?',
  'Как далеко до пляжа?', 'كم يبعد الشاطئ؟', 'Hoe ver is het strand?', 'Jak daleko jest do plaży?',
  'Hvor langt er det til stranden?', 'Hur långt är det till stranden?')
a('.faq[4][1]',
  'El folleto indica unos cinco minutos a pie hasta la playa de La Carihuela. Hacemos el recorrido con usted en una visita.',
  'La brochure indique environ cinq minutes à pied jusqu’à la plage de La Carihuela. Nous faisons le trajet avec vous lors d’une visite.',
  'Die Broschüre nennt etwa fünf Gehminuten zum Strand La Carihuela. Bei einem Besuch gehen wir den Weg mit Ihnen ab.',
  'В буклете указано около пяти минут пешком до пляжа Ла-Каригуэла. Во время осмотра мы пройдём этот путь вместе с вами.',
  'يذكر الكتيّب نحو خمس دقائق سيرًا إلى شاطئ لا كاريويلا. ونقطع الطريق معكم خلال الزيارة.',
  'De brochure noemt ongeveer vijf minuten lopen naar het strand van La Carihuela. Bij een bezoek lopen wij het met u.',
  'Broszura podaje około pięciu minut pieszo do plaży La Carihuela. Podczas wizyty przejdziemy tę trasę razem z Państwem.',
  'Brosjyren oppgir rundt fem minutters gange til stranden La Carihuela. Ved en visning går vi strekningen sammen med Dem.',
  'Broschyren anger omkring fem minuters promenad till stranden La Carihuela. Vid ett besök går vi sträckan tillsammans med er.')
a('.faq[5][1]',
  'No. El folleto indica que sus imágenes muestran mobiliario, decoración, paisajismo y opciones no incluidos en el precio, y los planos indican que el mobiliario dibujado no forma parte de la venta.',
  'Non. La brochure précise que ses images montrent du mobilier, de la décoration, des aménagements paysagers et des options non compris dans le prix, et les plans indiquent que le mobilier dessiné ne fait pas partie de la vente.',
  'Nein. Laut Broschüre zeigen die Bilder Möbel, Dekoration, Bepflanzung und Optionen, die nicht im Preis enthalten sind, und die Pläne sagen, dass die eingezeichneten Möbel nicht Teil des Verkaufs sind.',
  'Нет. В буклете сказано, что на изображениях показаны мебель, декор, озеленение и опции, не входящие в цену, а на планах указано, что изображённая мебель не входит в продажу.',
  'لا. يذكر الكتيّب أن صوره تُظهر أثاثًا وديكورًا وتنسيقًا للحدائق وخيارات غير مشمولة في السعر، وتذكر المخططات أن الأثاث المرسوم عليها ليس جزءًا من البيع.',
  'Nee. Volgens de brochure tonen de beelden meubilair, decoratie, beplanting en opties die niet in de prijs zijn inbegrepen, en de plannen zeggen dat het getekende meubilair niet bij de verkoop hoort.',
  'Nie. Broszura zaznacza, że jej obrazy pokazują meble, dekoracje, zieleń i opcje nieujęte w cenie, a rzuty podają, że narysowane meble nie są przedmiotem sprzedaży.',
  'Nei. Brosjyren sier at bildene viser møbler, dekor, beplantning og tilvalg som ikke er inkludert i prisen, og tegningene sier at møblene som er tegnet inn, ikke inngår i salget.',
  'Nej. Enligt broschyren visar bilderna möbler, dekor, plantering och tillval som inte ingår i priset, och ritningarna anger att de inritade möblerna inte ingår i försäljningen.')
a('.faq[6][1]',
  'Sí. La lista es una copia del portal del promotor del 25 de noviembre de 2026. Reconfirmamos el precio antes de que usted reserve.',
  'Oui. La liste est une copie du portail du promoteur au 25 novembre 2026. Nous reconfirmons le prix avant que vous ne réserviez.',
  'Ja. Die Liste ist eine Kopie des Portals des Bauträgers vom 25. November 2026. Wir bestätigen den Preis erneut, bevor Sie reservieren.',
  'Да. Список — копия портала застройщика на 25 ноября 2026 года. Мы повторно подтверждаем цену до того, как вы забронируете.',
  'نعم. القائمة نسخة من بوابة المطوّر بتاريخ 25 نوفمبر 2026. ونعيد تأكيد السعر قبل أن تحجزوا.',
  'Ja. De lijst is een kopie van het portaal van de ontwikkelaar op 25 november 2026. Wij bevestigen de prijs opnieuw voordat u reserveert.',
  'Tak. Cennik jest kopią portalu dewelopera z 25 listopada 2026 roku. Przed Państwa rezerwacją ponownie potwierdzamy cenę.',
  'Ja. Listen er en kopi av utbyggerens portal per 25. november 2026. Vi bekrefter prisen på nytt før De reserverer.',
  'Ja. Listan är en kopia av exploatörens portal den 25 november 2026. Vi bekräftar priset på nytt innan ni bokar.')

# ---- SEO -------------------------------------------------------------------------------------

a('.seo.title',
  'Calandria Residences - Apartamentos en Torremolinos', 'Calandria Residences - Appartements à Torremolinos',
  'Calandria Residences - Wohnungen in Torremolinos', 'Calandria Residences - квартиры в Торремолиносе',
  'Calandria Residences - شقق في توريمولينوس', 'Calandria Residences - Appartementen in Torremolinos',
  'Calandria Residences - Mieszkania w Torremolinos', 'Calandria Residences - Leiligheter i Torremolinos',
  'Calandria Residences - Lägenheter i Torremolinos')
a('.seo.h1',
  'Calandria Residences: apartamentos en Torremolinos', 'Calandria Residences : appartements à Torremolinos',
  'Calandria Residences: Wohnungen in Torremolinos', 'Calandria Residences: квартиры в Торремолиносе',
  'Calandria Residences: شقق في توريمولينوس', 'Calandria Residences: appartementen in Torremolinos',
  'Calandria Residences: mieszkania w Torremolinos', 'Calandria Residences: leiligheter i Torremolinos',
  'Calandria Residences: lägenheter i Torremolinos')

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings')
