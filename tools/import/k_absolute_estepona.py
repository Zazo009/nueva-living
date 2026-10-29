# -*- coding: utf-8 -*-
# Absolute Estepona (Estepona), human translations in one pass.
# p(path, es, fr, de, ru, ar, nl, pl, no, sv)
#
# The English string is looked up from the path scaffold.py printed in todo.json, so it is never
# copied here and cannot drift from project.json.
#
# Tokens expanded per locale, so a figure is written once and takes its locale's own format:
# €599000 -> "599.000 €" (nl "€ 599.000", fr/ru/pl/no/sv "599 000 €", ar "599,000 €"),
# #57.16 -> "57,16" (ar "57.16"), [m2] is the area unit (m², ru "м²", ar "م²"), and {D} is
# 29 October 2026 in the locale's own date form (the form scripts/lib/dates.mjs produces).
#
# The unit rows (size strings) and the floorplan alts and captions are built by function from the same
# numbers the English was built from, with the same words the-privilege and zenith-estepona use.
# Floor labels ("Portal 1, Second floor & solarium") are built by assemble.py from FLOOR_PARTS.
#
#   python3 tools/import/k_absolute_estepona.py <workdir>/tr_z.json <workdir>/todo.json
import json, re, sys

LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}
UNIT['ru'] = 'м²'
UNIT['ar'] = 'م²'
DATE = {'es': '29 de octubre de 2026', 'fr': '29 octobre 2026', 'de': '29. Oktober 2026', 'ru': '29 октября 2026 года',
        'ar': '29 أكتوبر 2026', 'nl': '29 oktober 2026', 'pl': '29 października 2026', 'no': '29. oktober 2026',
        'sv': '29 oktober 2026'}


def money(n, loc):
    body = f'{n:,}'.replace(',', GROUP[loc])
    return f'€ {body}' if loc == 'nl' else f'{body} €'


def expand(s, loc):
    s = re.sub(r'€(\d+)', lambda m: money(int(m.group(1)), loc), s)
    s = re.sub(r'#(\d+)\.(\d+)', lambda m: m.group(1) + ('.' if loc == 'ar' else ',') + m.group(2), s)
    return s.replace('[m2]', UNIT[loc]).replace('{D}', DATE[loc])


T = {}
TODO = json.load(open(sys.argv[2]))
BY_PATH = {paths[0]: en for en, paths in TODO.items()}
USED = set()


def p(path, *tr):
    assert len(tr) == 9, path
    en = BY_PATH[path]
    USED.add(path)
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---- identifiers that read the same in every language ---------------------------------------
for path, en in BY_PATH.items():
    if en in ('Absolute Estepona', 'Absolute <em>Estepona</em>') or re.fullmatch(r'[12]\.(?:0\d|S01)\.[A-D]', en):
        T[en] = {l: en for l in LOCS}
        USED.add(path)
    if path.endswith('.phase') and en == '':
        T[en] = {l: '' for l in LOCS}
        USED.add(path)
    # "Portal 1, Second floor & solarium": built from FLOOR_PARTS by assemble.py, not here.
    if re.fullmatch(r'\.availability\.units\[\d\]\.floor', path):
        USED.add(path)

# ---- the unit rows ---------------------------------------------------------------------------
WORDS = {
    'es': dict(built='m² construidos', interior='m² interiores', terrace='m² de terraza', garden='m² de jardín', solarium='m² de solárium'),
    'fr': dict(built='m² construits', interior='m² intérieurs', terrace='m² de terrasse', garden='m² de jardin', solarium='m² de solarium'),
    'de': dict(built='m² bebaut', interior='m² Innenfläche', terrace='m² Terrasse', garden='m² Garten', solarium='m² Solarium'),
    'nl': dict(built='m² bebouwd', interior='m² binnen', terrace='m² terras', garden='m² tuin', solarium='m² solarium'),
    'pl': dict(built='m² zabudowy', interior='m² wnętrza', terrace='m² tarasu', garden='m² ogrodu', solarium='m² solarium'),
    'no': dict(built='m² bebygd areal', interior='m² innvendig', terrace='m² terrasse', garden='m² hage', solarium='m² solterrasse'),
    'sv': dict(built='m² byggyta', interior='m² inomhus', terrace='m² terrass', garden='m² trädgård', solarium='m² solterrass'),
}


def size_row(en, loc):
    segs = [s.strip() for s in re.split(r',\s+', en)]
    out = []
    for seg in segs:
        m = re.fullmatch(r'([\d.]+) sqm (built|interior|terrace|garden|solarium)', seg)
        assert m, seg
        num = m.group(1).replace('.', '.' if loc == 'ar' else ',')
        kind = m.group(2)
        if loc == 'ru':
            out.append({'built': f'{num} м² застроенной площади', 'interior': f'{num} м² внутри',
                        'terrace': f'терраса {num} м²', 'garden': f'сад {num} м²', 'solarium': f'солярий {num} м²'}[kind])
        elif loc == 'ar':
            out.append({'built': f'{num} م² مبنية', 'interior': f'{num} م² داخلية', 'terrace': f'{num} م² تراس',
                        'garden': f'{num} م² حديقة', 'solarium': f'{num} م² سولاريوم'}[kind])
        else:
            out.append(f'{num} {WORDS[loc][kind]}')
    return ('، ' if loc == 'ar' else ', ').join(out)


for path, en in BY_PATH.items():
    if path.startswith('.availability.units[') and path.endswith('.size'):
        T[en] = {l: size_row(en, l) for l in LOCS}
        USED.add(path)

FP_ALT = dict(es='Plano de la vivienda {}', fr='Plan du logement {}', de='Grundriss der Wohnung {}', ru='Планировка квартиры {}',
              ar='مخطط المسكن {}', nl='Plattegrond van woning {}', pl='Rzut mieszkania {}', no='Plantegning av bolig {}',
              sv='Planritning för bostad {}')
FP_CAP = dict(es='Vivienda {}', fr='Logement {}', de='Wohnung {}', ru='Квартира {}', ar='المسكن {}', nl='Woning {}',
              pl='Mieszkanie {}', no='Bolig {}', sv='Bostad {}')
for path, en in BY_PATH.items():
    m = re.fullmatch(r'Floorplan of home (.+)', en)
    if m:
        T[en] = {l: FP_ALT[l].format(m.group(1)) for l in LOCS}
        USED.add(path)
    m = re.fullmatch(r'Home (.+)', en)
    if m and path.startswith('.media.items['):
        T[en] = {l: FP_CAP[l].format(m.group(1)) for l in LOCS}
        USED.add(path)

# ================================ translated prose ==============================================
# description
p('.description',
  '5 de 24 apartamentos y áticos de dos y tres dormitorios en una promoción cerrada de estilo boutique en Estepona, con piscina exterior, gimnasio, vistas al mar y, en los áticos, un solárium con jacuzzi. En construcción desde el tercer trimestre de 2024, con el fin de obra estimado para el primer trimestre de 2027. Desde €599000 más IVA.',
  '5 appartements et penthouses sur 24, de deux et trois chambres, dans un programme fermé de type boutique à Estepona, avec piscine extérieure, salle de sport, vue sur la mer et, pour les penthouses, un solarium avec jacuzzi. En construction depuis le troisième trimestre 2024, avec une fin de travaux estimée au premier trimestre 2027. À partir de €599000 plus TVA.',
  '5 von 24 Wohnungen und Penthäusern mit zwei und drei Schlafzimmern in einer kleinen geschlossenen Anlage in Estepona, mit Außenpool, Fitnessraum, Meerblick und bei den Penthäusern einem Solarium mit Whirlpool. Im Bau seit dem dritten Quartal 2024, Bauende geschätzt für das erste Quartal 2027. Ab €599000 plus MwSt.',
  '5 из 24 апартаментов и пентхаусов с двумя и тремя спальнями в небольшом закрытом комплексе в Эстепоне: открытый бассейн, тренажёрный зал, вид на море, а у пентхаусов — солярий с джакузи. Строится с третьего квартала 2024 года, окончание строительства ориентировочно в первом квартале 2027 года. От €599000 плюс НДС.',
  '5 من 24 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم في مشروع مغلق صغير في إستيبونا، مع مسبح خارجي وصالة رياضية وإطلالات على البحر، وسولاريوم مع جاكوزي في البنتهاوس. قيد الإنشاء منذ الربع الثالث من 2024، ويُقدَّر انتهاء البناء في الربع الأول من 2027. ابتداءً من €599000 زائد ضريبة القيمة المضافة.',
  '5 van de 24 appartementen en penthouses met twee en drie slaapkamers in een kleinschalig besloten project in Estepona, met een buitenzwembad, een fitnessruimte, zeezicht en bij de penthouses een solarium met jacuzzi. In aanbouw sinds het derde kwartaal van 2024, met een geschat einde van de bouw in het eerste kwartaal van 2027. Vanaf €599000 plus btw.',
  '5 z 24 apartamentów i penthouse’ów z dwiema i trzema sypialniami w niewielkiej zamkniętej inwestycji w Esteponie, z basenem zewnętrznym, siłownią, widokiem na morze oraz, w penthouse’ach, solarium z jacuzzi. W budowie od trzeciego kwartału 2024 r., z szacowanym zakończeniem budowy w pierwszym kwartale 2027 r. Od €599000 plus VAT.',
  '5 av 24 leiligheter og toppleiligheter med to og tre soverom i et lite bevoktet anlegg i Estepona, med utendørsbasseng, treningsrom, sjøutsikt og, i toppleilighetene, en solterrasse med jacuzzi. Under bygging siden tredje kvartal 2024, med byggeslutt anslått til første kvartal 2027. Fra €599000 pluss mva.',
  '5 av 24 lägenheter och takvåningar med två och tre sovrum i en liten bevakad anläggning i Estepona, med utomhuspool, gym, havsutsikt och, i takvåningarna, en solterrass med jacuzzi. Under uppförande sedan tredje kvartalet 2024, med byggslut beräknat till första kvartalet 2027. Från €599000 plus IVA.')
p('.seoDescription',
  '5 de 24 apartamentos y áticos de dos y tres dormitorios en una promoción cerrada de Estepona, con vistas al mar, piscina y gimnasio, fin de obra estimado para el T1 2027, desde €599000 más IVA.',
  '5 appartements et penthouses sur 24, de deux et trois chambres, dans un programme fermé à Estepona, avec vue sur la mer, piscine et salle de sport, fin des travaux estimée au T1 2027, à partir de €599000 plus TVA.',
  '5 von 24 Wohnungen und Penthäusern mit zwei und drei Schlafzimmern in einer geschlossenen Anlage in Estepona, mit Meerblick, Pool und Fitnessraum, Bauende geschätzt für Q1 2027, ab €599000 plus MwSt.',
  '5 из 24 апартаментов и пентхаусов с двумя и тремя спальнями в закрытом комплексе в Эстепоне: вид на море, бассейн и тренажёрный зал, окончание строительства ориентировочно в 1 кв. 2027 года, от €599000 плюс НДС.',
  '5 من 24 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم في مشروع مغلق في إستيبونا، مع إطلالات على البحر ومسبح وصالة رياضية، ويُقدَّر انتهاء البناء في الربع الأول 2027، ابتداءً من €599000 زائد ضريبة القيمة المضافة.',
  '5 van de 24 appartementen en penthouses met twee en drie slaapkamers in een besloten project in Estepona, met zeezicht, een zwembad en een fitnessruimte, geschat einde van de bouw in K1 2027, vanaf €599000 plus btw.',
  '5 z 24 apartamentów i penthouse’ów z dwiema i trzema sypialniami w zamkniętej inwestycji w Esteponie, z widokiem na morze, basenem i siłownią, szacowane zakończenie budowy w I kw. 2027 r., od €599000 plus VAT.',
  '5 av 24 leiligheter og toppleiligheter med to og tre soverom i et bevoktet anlegg i Estepona, med sjøutsikt, basseng og treningsrom, byggeslutt anslått til K1 2027, fra €599000 pluss mva.',
  '5 av 24 lägenheter och takvåningar med två och tre sovrum i en bevakad anläggning i Estepona, med havsutsikt, pool och gym, byggslut beräknat till K1 2027, från €599000 plus IVA.')
p('.twitterDescription',
  'Apartamentos y áticos de dos y tres dormitorios en Estepona con vistas al mar, piscina y gimnasio, desde €599000 más IVA.',
  'Appartements et penthouses de deux et trois chambres à Estepona avec vue sur la mer, piscine et salle de sport, à partir de €599000 plus TVA.',
  'Wohnungen und Penthäuser mit zwei und drei Schlafzimmern in Estepona mit Meerblick, Pool und Fitnessraum, ab €599000 plus MwSt.',
  'Апартаменты и пентхаусы с двумя и тремя спальнями в Эстепоне: вид на море, бассейн и тренажёрный зал, от €599000 плюс НДС.',
  'شقق وبنتهاوس بغرفتي نوم وثلاث غرف نوم في إستيبونا مع إطلالات على البحر ومسبح وصالة رياضية، ابتداءً من €599000 زائد ضريبة القيمة المضافة.',
  'Appartementen en penthouses met twee en drie slaapkamers in Estepona met zeezicht, een zwembad en een fitnessruimte, vanaf €599000 plus btw.',
  'Apartamenty i penthouse’y z dwiema i trzema sypialniami w Esteponie z widokiem na morze, basenem i siłownią, od €599000 plus VAT.',
  'Leiligheter og toppleiligheter med to og tre soverom i Estepona med sjøutsikt, basseng og treningsrom, fra €599000 pluss mva.',
  'Lägenheter och takvåningar med två och tre sovrum i Estepona med havsutsikt, pool och gym, från €599000 plus IVA.')

p('.hero.startingPrice', 'Desde €599000 + IVA', 'À partir de €599000 + TVA', 'Ab €599000 + MwSt.', 'От €599000 + НДС',
  'ابتداءً من €599000 + ضريبة القيمة المضافة', 'Vanaf €599000 + btw', 'Od €599000 + VAT', 'Fra €599000 + mva.', 'Från €599000 + IVA')
p('.hero.delivery', 'Estimada T1 2027', 'Estimée T1 2027', 'Voraussichtlich Q1 2027', 'Ориентировочно 1 кв. 2027',
  'المتوقع الربع الأول 2027', 'Verwacht K1 2027', 'Szacowany I kw. 2027', 'Forventet K1 2027', 'Beräknat K1 2027')
p('.card.description',
  '5 de 24 apartamentos y áticos de dos y tres dormitorios en una promoción cerrada de Estepona, con vistas al mar, piscina exterior y gimnasio.',
  '5 appartements et penthouses sur 24, de deux et trois chambres, dans un programme fermé à Estepona, avec vue sur la mer, piscine extérieure et salle de sport.',
  '5 von 24 Wohnungen und Penthäusern mit zwei und drei Schlafzimmern in einer geschlossenen Anlage in Estepona, mit Meerblick, Außenpool und Fitnessraum.',
  '5 из 24 апартаментов и пентхаусов с двумя и тремя спальнями в закрытом комплексе в Эстепоне: вид на море, открытый бассейн и тренажёрный зал.',
  '5 من 24 شقة وبنتهاوس بغرفتي نوم وثلاث غرف نوم في مشروع مغلق في إستيبونا، مع إطلالات على البحر ومسبح خارجي وصالة رياضية.',
  '5 van de 24 appartementen en penthouses met twee en drie slaapkamers in een besloten project in Estepona, met zeezicht, een buitenzwembad en een fitnessruimte.',
  '5 z 24 apartamentów i penthouse’ów z dwiema i trzema sypialniami w zamkniętej inwestycji w Esteponie, z widokiem na morze, basenem zewnętrznym i siłownią.',
  '5 av 24 leiligheter og toppleiligheter med to og tre soverom i et bevoktet anlegg i Estepona, med sjøutsikt, utendørsbasseng og treningsrom.',
  '5 av 24 lägenheter och takvåningar med två och tre sovrum i en bevakad anläggning i Estepona, med havsutsikt, utomhuspool och gym.')
p('.card.meta[0][1]', '€599000 + IVA', '€599000 + TVA', '€599000 + MwSt.', '€599000 + НДС', '€599000 + ضريبة القيمة المضافة',
  '€599000 + btw', '€599000 + VAT', '€599000 + mva.', '€599000 + IVA')

# image alts
p('.images.hero.alt',
  'Vista generada por ordenador de dos bloques blancos con terrazas escalonadas sobre un césped y una piscina, con el mar al fondo',
  'Vue de synthèse de deux bâtiments blancs aux terrasses en gradins au-dessus d’une pelouse et d’une piscine, avec la mer au fond',
  'Computergenerierte Ansicht von zwei weißen Gebäuden mit gestaffelten Terrassen über einem Rasen und einem Pool, dahinter das Meer',
  'Компьютерная визуализация двух белых корпусов со ступенчатыми террасами над газоном и бассейном, вдали море',
  'منظر مُولَّد بالحاسوب لمبنيين أبيضين بتراسات متدرجة فوق مرج ومسبح، والبحر في الخلفية',
  'Computergegenereerd beeld van twee witte blokken met getrapte terrassen boven een gazon en een zwembad, met de zee op de achtergrond',
  'Komputerowa wizualizacja dwóch białych budynków z tarasami schodzącymi tarasowo nad trawnikiem i basenem, w tle morze',
  'Datagenerert bilde av to hvite bygg med trappetrinnsformede terrasser over en plen og et basseng, med havet i bakgrunnen',
  'Datorgenererad bild av två vita byggnader med trappstegsformade terrasser ovanför en gräsmatta och en pool, med havet i bakgrunden')
p('.images.architecture.alt',
  'Vista generada por ordenador de las largas terrazas blancas de los bloques desde la piscina, con tumbonas y palmeras',
  'Vue de synthèse des longues terrasses blanches des bâtiments depuis la piscine, avec des bains de soleil et des palmiers',
  'Computergenerierte Ansicht der langen weißen Terrassen der Gebäude vom Pool aus, mit Sonnenliegen und Palmen',
  'Компьютерная визуализация длинных белых террас корпусов со стороны бассейна, с шезлонгами и пальмами',
  'منظر مُولَّد بالحاسوب للتراسات البيضاء الطويلة للمبنيين من المسبح، مع كراسي استلقاء ونخيل',
  'Computergegenereerd beeld van de lange witte terrassen van de blokken vanaf het zwembad, met ligbedden en palmbomen',
  'Komputerowa wizualizacja długich białych tarasów budynków od strony basenu, z leżakami i palmami',
  'Datagenerert bilde av byggenes lange hvite terrasser sett fra bassenget, med solsenger og palmer',
  'Datorgenererad bild av byggnadernas långa vita terrasser sedd från poolen, med solstolar och palmer')
p('.images.lifestyle.alt',
  'Terraza generada por ordenador bajo una losa blanca, con sillones y una mesa de comedor, mirando al mar por encima de una barandilla de cristal',
  'Terrasse de synthèse sous une dalle blanche, avec des fauteuils et une table à manger, donnant sur la mer par-dessus un garde-corps en verre',
  'Computergenerierte Terrasse unter einer weißen Deckenplatte, mit Loungemöbeln und einem Esstisch, mit Blick über eine Glasbrüstung zum Meer',
  'Компьютерная визуализация террасы под белой плитой с мягкой мебелью и обеденным столом, вид на море поверх стеклянного ограждения',
  'تراس مُولَّد بالحاسوب تحت بلاطة بيضاء مع مقاعد وطاولة طعام، يطل على البحر فوق حاجز زجاجي',
  'Computergegenereerd terras onder een witte plaat met loungemeubels en een eettafel, met uitzicht op zee over een glazen balustrade',
  'Komputerowa wizualizacja tarasu pod białą płytą z wypoczynkiem i stołem jadalnym, z widokiem na morze ponad szklaną balustradą',
  'Datagenerert terrasse under en hvit takplate med loungemøbler og et spisebord, med utsikt mot havet over et glassrekkverk',
  'Datorgenererad terrass under en vit platta med loungemöbler och ett matbord, med utsikt mot havet över ett glasräcke')
p('.images.privateViewing.alt',
  'Dormitorio principal generado por ordenador con una cama doble, un espejo redondo y puertas de cristal a un balcón con vistas al mar',
  'Chambre principale de synthèse avec un lit double, un miroir rond et des portes vitrées donnant sur un balcon avec vue sur la mer',
  'Computergeneriertes Hauptschlafzimmer mit einem Doppelbett, einem runden Spiegel und Glastüren zu einem Balkon mit Meerblick',
  'Компьютерная визуализация главной спальни с двуспальной кроватью, круглым зеркалом и стеклянными дверями на балкон с видом на море',
  'غرفة نوم رئيسية مُولَّدة بالحاسوب بسرير مزدوج ومرآة مستديرة وأبواب زجاجية إلى شرفة تطل على البحر',
  'Computergegenereerde hoofdslaapkamer met een tweepersoonsbed, een ronde spiegel en glazen deuren naar een balkon met uitzicht op zee',
  'Komputerowa wizualizacja głównej sypialni z podwójnym łóżkiem, okrągłym lustrem i szklanymi drzwiami na balkon z widokiem na morze',
  'Datagenerert hovedsoverom med en dobbeltseng, et rundt speil og glassdører til en balkong med utsikt mot havet',
  'Datorgenererat huvudsovrum med en dubbelsäng, en rund spegel och glasdörrar till en balkong med havsutsikt')

# media
p('.media.copy',
  'Vistas generadas por ordenador de los bloques, la piscina y los interiores, y los planos de las cinco viviendas a la venta.',
  'Vues de synthèse des bâtiments, de la piscine et des intérieurs, et plans des cinq logements annoncés.',
  'Computergenerierte Ansichten der Gebäude, des Pools und der Innenräume sowie die Grundrisse der fünf gelisteten Wohnungen.',
  'Компьютерные визуализации корпусов, бассейна и интерьеров и планировки пяти квартир из списка.',
  'مناظر مُولَّدة بالحاسوب للمبنيين والمسبح والمساحات الداخلية، ومخططات المساكن الخمسة المدرجة.',
  'Computergegenereerde beelden van de blokken, het zwembad en de interieurs, en de plattegronden van de vijf woningen op de lijst.',
  'Komputerowe wizualizacje budynków, basenu i wnętrz oraz rzuty pięciu mieszkań z listy.',
  'Datagenererte bilder av byggene, bassenget og interiørene, og plantegningene til de fem oppførte boligene.',
  'Datorgenererade bilder av byggnaderna, poolen och interiörerna samt planritningarna för de fem listade bostäderna.')
p('.media.note',
  'Todas las vistas están generadas por ordenador, salvo la vista aérea, que sitúa los bloques generados por ordenador en una fotografía, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los planos comerciales del promotor: no son contractuales, los nombres de las estancias figuran en español y indican que las superficies son aproximadas.',
  'Toutes les vues sont des images de synthèse, sauf la vue aérienne, qui place les bâtiments de synthèse dans une photographie ; le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont les plans commerciaux du promoteur : ils ne sont pas contractuels, les noms des pièces y sont en espagnol et ils indiquent que les surfaces sont approximatives.',
  'Alle Ansichten sind computergeneriert, mit Ausnahme der Luftansicht, die die computergenerierten Gebäude in ein Foto setzt; die darin gezeigten Möbel und die Dekoration sind illustrativ und nicht enthalten. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen sind auf Spanisch, und sie weisen darauf hin, dass die Flächen ungefähre Angaben sind.',
  'Все изображения — компьютерные визуализации, кроме вида с воздуха, где визуализированные корпуса помещены на фотографию; мебель и декор на них носят иллюстративный характер и не входят в стоимость. Планировки — коммерческие планы застройщика: они не имеют договорной силы, названия помещений на них даны по-испански, а площади, как указано на них, приблизительные.',
  'جميع المناظر مُولَّدة بالحاسوب، باستثناء المنظر الجوي الذي يضع المبنيين المُولَّدين بالحاسوب في صورة فوتوغرافية، والأثاث والديكور فيها توضيحيان وغير مشمولين. المخططات هي مخططات المطوّر التسويقية: ليست تعاقدية، وأسماء الغرف عليها بالإسبانية، وهي تنص على أن المساحات تقريبية.',
  'Alle beelden zijn computergegenereerd, behalve het luchtbeeld, dat de computergegenereerde blokken in een foto plaatst, en het meubilair en de inrichting daarin zijn illustratief en niet inbegrepen. De plattegronden zijn de verkoopplattegronden van de ontwikkelaar: ze zijn niet contractueel, de ruimtenamen staan in het Spaans en ze vermelden dat de oppervlakten bij benadering zijn.',
  'Wszystkie widoki są wygenerowane komputerowo, z wyjątkiem widoku z lotu ptaka, który umieszcza wygenerowane komputerowo budynki na fotografii; meble i dekoracje na nich mają charakter poglądowy i nie są wliczone. Rzuty to rzuty sprzedażowe dewelopera: nie mają mocy umownej, nazwy pomieszczeń są po hiszpańsku, a powierzchnie, jak zaznaczono, są przybliżone.',
  'Alle bildene er datagenererte, bortsett fra flyfotoet, som plasserer de datagenererte byggene i et fotografi, og møblene og dekorasjonen i dem er illustrative og ikke inkludert. Plantegningene er utbyggerens salgstegninger: de er ikke kontraktsfestet, romnavnene er på spansk, og de oppgir at arealene er omtrentlige.',
  'Alla bilder är datorgenererade, förutom flygbilden, som placerar de datorgenererade byggnaderna i ett fotografi, och möblerna och inredningen i dem är illustrativa och ingår inte. Planritningarna är exploatörens försäljningsritningar: de är inte avtalsbindande, rumsnamnen är på spanska och de anger att ytorna är ungefärliga.')
p('.media.items[0].caption', 'Los bloques escalonados sobre la piscina', 'Les bâtiments en gradins au-dessus de la piscine',
  'Die gestaffelten Gebäude über dem Pool', 'Ступенчатые корпуса над бассейном', 'المبنيان المتدرجان فوق المسبح',
  'De getrapte blokken boven het zwembad', 'Tarasowe budynki nad basenem', 'De trappetrinnsformede byggene over bassenget',
  'De trappstegsformade byggnaderna ovanför poolen')
p('.media.items[1].caption', 'La fachada desde la piscina', 'La façade vue de la piscine', 'Die Fassade vom Pool aus',
  'Фасад со стороны бассейна', 'الواجهة من المسبح', 'De gevel vanaf het zwembad', 'Elewacja od strony basenu',
  'Fasaden sett fra bassenget', 'Fasaden sedd från poolen')
p('.media.items[2].alt',
  'Vista generada por ordenador al atardecer de los bloques escalonados con ventanas iluminadas sobre una piscina iluminada y otra más pequeña',
  'Vue de synthèse au crépuscule des bâtiments en gradins aux fenêtres éclairées au-dessus d’une piscine éclairée et d’une plus petite',
  'Computergenerierte Ansicht der gestaffelten Gebäude in der Dämmerung mit erleuchteten Fenstern über einem beleuchteten Pool und einem kleineren Pool',
  'Компьютерная визуализация ступенчатых корпусов в сумерках с освещёнными окнами над освещённым бассейном и вторым, меньшим бассейном',
  'منظر مُولَّد بالحاسوب عند الغروب للمبنيين المتدرجين بنوافذ مضاءة فوق مسبح مضاء ومسبح آخر أصغر',
  'Computergegenereerd beeld bij schemering van de getrapte blokken met verlichte ramen boven een verlicht zwembad en een kleiner zwembad',
  'Komputerowa wizualizacja o zmierzchu tarasowych budynków z podświetlonymi oknami nad podświetlonym basenem i drugim, mniejszym basenem',
  'Datagenerert bilde i skumringen av de trappetrinnsformede byggene med opplyste vinduer over et opplyst basseng og et mindre basseng',
  'Datorgenererad bild i skymningen av de trappstegsformade byggnaderna med upplysta fönster ovanför en upplyst pool och en mindre pool')
p('.media.items[2].caption', 'Los bloques y la piscina al atardecer', 'Les bâtiments et la piscine au crépuscule',
  'Die Gebäude und der Pool in der Dämmerung', 'Корпуса и бассейн в сумерках', 'المبنيان والمسبح عند الغروب',
  'De blokken en het zwembad in de schemering', 'Budynki i basen o zmierzchu', 'Byggene og bassenget i skumringen',
  'Byggnaderna och poolen i skymningen')
p('.media.items[3].alt',
  'Fotografía aérea de una parcela en ladera con los bloques generados por ordenador colocados sobre ella, una piscina delante y colinas detrás',
  'Photographie aérienne d’une parcelle en pente sur laquelle sont placés les bâtiments de synthèse, avec une piscine devant et des collines derrière',
  'Luftaufnahme eines Hanggrundstücks, auf dem die computergenerierten Gebäude platziert sind, mit einem Pool davor und Hügeln dahinter',
  'Аэрофотоснимок участка на склоне с помещёнными на него визуализированными корпусами, бассейном впереди и холмами позади',
  'صورة جوية لقطعة أرض على سفح تلة وُضع عليها المبنيان المُولَّدان بالحاسوب، مع مسبح في المقدمة وتلال في الخلفية',
  'Luchtfoto van een perceel op een helling met de computergegenereerde blokken erop geplaatst, een zwembad ervoor en heuvels erachter',
  'Zdjęcie lotnicze działki na zboczu z umieszczonymi na niej wygenerowanymi komputerowo budynkami, basenem z przodu i wzgórzami w tle',
  'Flyfoto av en tomt i en skråning med de datagenererte byggene plassert på den, et basseng foran og åser bak',
  'Flygfoto av en tomt i en sluttning med de datorgenererade byggnaderna placerade på den, en pool framför och kullar bakom')
p('.media.items[3].caption', 'Los dos bloques en la parcela, vistos desde arriba', 'Les deux bâtiments sur la parcelle, vus d’en haut',
  'Die beiden Gebäude auf dem Grundstück von oben', 'Два корпуса на участке, вид сверху', 'المبنيان على القطعة، منظر من الأعلى',
  'De twee blokken op het perceel, van bovenaf gezien', 'Dwa budynki na działce, widok z góry', 'De to byggene på tomten, sett ovenfra',
  'De två byggnaderna på tomten, sedda uppifrån')
p('.media.items[5].alt',
  'Terraza en la cubierta generada por ordenador con tumbonas, una mesa de comedor y una zona de estar, con vistas al mar',
  'Terrasse sur le toit de synthèse avec bains de soleil, table à manger et coin salon, avec vue sur la mer',
  'Computergenerierte Dachterrasse mit Sonnenliegen, einem Esstisch und einer Sitzgruppe, mit Blick aufs Meer',
  'Компьютерная визуализация террасы на крыше с шезлонгами, обеденным столом и зоной отдыха, вид на море',
  'تراس على السطح مُولَّد بالحاسوب مع كراسي استلقاء وطاولة طعام ومنطقة جلوس، يطل على البحر',
  'Computergegenereerd dakterras met ligbedden, een eettafel en een zithoek, met uitzicht over zee',
  'Komputerowa wizualizacja tarasu na dachu z leżakami, stołem jadalnym i strefą wypoczynkową, z widokiem na morze',
  'Datagenerert takterrasse med solsenger, et spisebord og en sittegruppe, med utsikt over havet',
  'Datorgenererad takterrass med solstolar, ett matbord och en sittgrupp, med utsikt över havet')
p('.media.items[6].alt',
  'Terraza de planta baja generada por ordenador con una mesa de comedor y una zona de estar, abierta a un césped con setos y palmeras',
  'Terrasse de rez-de-chaussée de synthèse avec une table à manger et un coin salon, ouverte sur une pelouse bordée de haies et de palmiers',
  'Computergenerierte Erdgeschossterrasse mit einem Esstisch und einer Sitzgruppe, die sich zu einem Rasen mit Hecken und Palmen öffnet',
  'Компьютерная визуализация террасы на первом этаже с обеденным столом и зоной отдыха, выходящей на газон с живой изгородью и пальмами',
  'تراس في الطابق الأرضي مُولَّد بالحاسوب مع طاولة طعام ومنطقة جلوس، يفتح على مرج به أسيجة ونخيل',
  'Computergegenereerd terras op de begane grond met een eettafel en een zithoek, dat uitkomt op een gazon met hagen en palmbomen',
  'Komputerowa wizualizacja tarasu na parterze ze stołem jadalnym i strefą wypoczynkową, otwartego na trawnik z żywopłotami i palmami',
  'Datagenerert terrasse i første etasje med et spisebord og en sittegruppe, åpen mot en plen med hekker og palmer',
  'Datorgenererad terrass på bottenvåningen med ett matbord och en sittgrupp, öppen mot en gräsmatta med häckar och palmer')
p('.media.items[7].alt',
  'Cocina abierta generada por ordenador con una isla y una mesa de comedor, con una zona de estar y el mar al otro lado de una pared acristalada corredera',
  'Cuisine ouverte de synthèse avec un îlot et une table à manger, avec un coin salon et la mer au-delà d’une baie vitrée coulissante',
  'Computergenerierte offene Küche mit einer Kochinsel und einem Esstisch, mit Wohnbereich und dem Meer hinter einer verglasten Schiebewand',
  'Компьютерная визуализация открытой кухни с островом и обеденным столом, зоной гостиной и морем за стеклянной раздвижной стеной',
  'مطبخ مفتوح مُولَّد بالحاسوب مع جزيرة وطاولة طعام ومنطقة معيشة، والبحر خلف جدار زجاجي منزلق',
  'Computergegenereerde open keuken met een eiland en een eettafel, met een woonruimte en de zee achter een glazen schuifwand',
  'Komputerowa wizualizacja otwartej kuchni z wyspą i stołem jadalnym, ze strefą dzienną i morzem za przeszkloną ścianą przesuwną',
  'Datagenerert åpent kjøkken med en øy og et spisebord, med en stueavdeling og havet bak en glassvegg som kan skyves',
  'Datorgenererat öppet kök med en köksö och ett matbord, med en vardagsrumsdel och havet bakom en glasvägg som går att skjuta')
p('.media.items[8].alt',
  'Salón generado por ordenador con una mesa de comedor de mármol, una pared de lamas de madera tras el televisor y puertas correderas de cristal a una terraza y al mar',
  'Séjour de synthèse avec une table à manger en marbre, un mur de lamelles de bois derrière le téléviseur et des portes vitrées coulissantes vers une terrasse et la mer',
  'Computergeneriertes Wohnzimmer mit einem Marmoresstisch, einer Lamellenwand aus Holz hinter dem Fernseher und gläsernen Schiebetüren zu einer Terrasse und zum Meer',
  'Компьютерная визуализация гостиной с мраморным обеденным столом, стеной из деревянных реек за телевизором и стеклянными раздвижными дверями на террасу и к морю',
  'غرفة معيشة مُولَّدة بالحاسوب مع طاولة طعام رخامية وجدار من الشرائح الخشبية خلف التلفزيون وأبواب زجاجية منزلقة إلى تراس والبحر',
  'Computergegenereerde woonkamer met een marmeren eettafel, een lamellenwand van hout achter de televisie en glazen schuifdeuren naar een terras en de zee',
  'Komputerowa wizualizacja salonu z marmurowym stołem jadalnym, ścianą z drewnianych lameli za telewizorem i szklanymi drzwiami przesuwnymi na taras i w stronę morza',
  'Datagenerert stue med et marmorspisebord, en lamellvegg i tre bak TV-en og skyvedører i glass til en terrasse og havet',
  'Datorgenererat vardagsrum med ett marmormatbord, en lamellvägg i trä bakom tv:n och skjutdörrar i glas till en terrass och havet')

# overview
p('.overview.headlineHtml', 'Veinticuatro viviendas, <em>cinco a la venta</em>', 'Vingt-quatre logements, <em>cinq annoncés</em>',
  'Vierundzwanzig Wohnungen, <em>fünf gelistet</em>', 'Двадцать четыре квартиры, <em>пять в списке</em>',
  'أربع وعشرون شقة، <em>خمس منها مدرجة</em>', 'Vierentwintig woningen, <em>vijf op de lijst</em>',
  'Dwadzieścia cztery mieszkania, <em>pięć na liście</em>', 'Tjuefire boliger, <em>fem oppført</em>',
  'Tjugofyra bostäder, <em>fem listade</em>')
p('.overview.copy[0]',
  'Absolute Estepona es una promoción cerrada de estilo boutique de 24 apartamentos de dos y tres dormitorios en Estepona. La ficha informativa del promotor la sitúa a 500 metros de la playa y de los servicios locales, con vistas panorámicas al mar. Las imágenes muestran dos bloques de terrazas blancas escalonadas en una ladera hacia una piscina, y los planos numeran las entradas como portales 1 y 2. Cinco viviendas figuran con precio: dos áticos de tres dormitorios con solárium y jacuzzi, y tres viviendas de dos dormitorios, una con jardín, una a nivel de jardín con una terraza muy grande y una en la primera planta.',
  'Absolute Estepona est un programme fermé de type boutique de 24 appartements de deux et trois chambres à Estepona. La fiche d’information du promoteur le situe à 500 mètres de la plage et des commerces locaux, avec une vue panoramique sur la mer. Les images montrent deux bâtiments aux terrasses blanches en gradins sur une pente, face à une piscine, et les plans numérotent les entrées en cages 1 et 2. Cinq logements sont annoncés avec un prix : deux penthouses de trois chambres avec solarium et jacuzzi, et trois logements de deux chambres, l’un avec jardin, l’un de plain-pied avec le jardin et une très grande terrasse, et l’un au premier étage.',
  'Absolute Estepona ist eine kleine geschlossene Anlage mit 24 Wohnungen mit zwei und drei Schlafzimmern in Estepona. Das Infoblatt des Bauträgers nennt sie 500 Meter vom Strand und von den örtlichen Einrichtungen entfernt, mit Panorama-Meerblick. Die Bilder zeigen zwei Gebäude mit weißen, gestaffelten Terrassen an einem Hang oberhalb eines Pools, und die Pläne nummerieren die Eingänge als Aufgang 1 und 2. Fünf Wohnungen sind mit Preis gelistet: zwei Penthäuser mit drei Schlafzimmern, Solarium und Whirlpool sowie drei Wohnungen mit zwei Schlafzimmern, eine mit Garten, eine auf Gartenebene mit einer sehr großen Terrasse und eine im ersten Obergeschoss.',
  'Absolute Estepona — небольшой закрытый комплекс из 24 апартаментов с двумя и тремя спальнями в Эстепоне. В информационном листе застройщика он расположен в 500 метрах от пляжа и местной инфраструктуры, с панорамным видом на море. На изображениях два корпуса с белыми ступенчатыми террасами на склоне над бассейном, а на планах входы пронумерованы как подъезды 1 и 2. С ценой указаны пять квартир: два трёхспальных пентхауса с солярием и джакузи и три двухспальные квартиры — одна с садом, одна на уровне сада с очень большой террасой и одна на втором этаже.',
  'Absolute Estepona مشروع مغلق صغير من 24 شقة بغرفتي نوم وثلاث غرف نوم في إستيبونا. تضعه نشرة المطوّر التعريفية على بعد 500 متر من الشاطئ والمرافق المحلية، مع إطلالات بانورامية على البحر. وتُظهر الصور مبنيين بتراسات بيضاء متدرجة على سفح تلة فوق مسبح، وترقّم المخططات المداخل كمدخل 1 ومدخل 2. تُدرج خمسة مساكن بأسعارها: بنتهاوسان بثلاث غرف نوم مع سولاريوم وجاكوزي، وثلاثة مساكن بغرفتي نوم، أحدها بحديقة، وآخر في مستوى الحديقة بتراس كبير جداً، وثالث في الطابق الأول.',
  'Absolute Estepona is een kleinschalig besloten project van 24 appartementen met twee en drie slaapkamers in Estepona. Het infoblad van de ontwikkelaar plaatst het op 500 meter van het strand en de lokale voorzieningen, met panoramisch zeezicht. De beelden tonen twee blokken met witte, getrapte terrassen op een helling boven een zwembad, en de plattegronden nummeren de ingangen als portiek 1 en 2. Vijf woningen staan met prijs op de lijst: twee penthouses met drie slaapkamers met solarium en jacuzzi, en drie woningen met twee slaapkamers, één met tuin, één op tuinniveau met een heel groot terras en één op de eerste verdieping.',
  'Absolute Estepona to niewielka zamknięta inwestycja z 24 apartamentami z dwiema i trzema sypialniami w Esteponie. Karta informacyjna dewelopera umieszcza ją 500 metrów od plaży i lokalnych usług, z panoramicznym widokiem na morze. Wizualizacje pokazują dwa budynki z białymi tarasami schodzącymi po zboczu w stronę basenu, a rzuty numerują wejścia jako klatki 1 i 2. Z ceną wymieniono pięć lokali: dwa trzysypialniowe penthouse’y z solarium i jacuzzi oraz trzy mieszkania z dwiema sypialniami — jedno z ogrodem, jedno na poziomie ogrodu z bardzo dużym tarasem i jedno na pierwszym piętrze.',
  'Absolute Estepona er et lite bevoktet anlegg med 24 leiligheter med to og tre soverom i Estepona. Utbyggerens infoark plasserer det 500 meter fra stranden og de lokale tilbudene, med panoramautsikt over havet. Bildene viser to bygg med hvite terrasser i trinn nedover en skråning mot et basseng, og plantegningene nummererer inngangene som oppgang 1 og 2. Fem boliger er oppført med pris: to toppleiligheter med tre soverom, solterrasse og jacuzzi, og tre boliger med to soverom, én med hage, én på hagenivå med en veldig stor terrasse og én i andre etasje.',
  'Absolute Estepona är en liten bevakad anläggning med 24 lägenheter med två och tre sovrum i Estepona. Exploatörens infoblad placerar den 500 meter från stranden och den lokala servicen, med panoramautsikt över havet. Bilderna visar två byggnader med vita terrasser i trappsteg nedför en sluttning mot en pool, och planritningarna numrerar ingångarna som uppgång 1 och 2. Fem bostäder är listade med pris: två takvåningar med tre sovrum, solterrass och jacuzzi samt tre bostäder med två sovrum, en med trädgård, en på trädgårdsplan med en mycket stor terrass och en på första våningen.')
p('.overview.copy[1]',
  'La ficha informativa da la licencia de obras con fecha 18 de septiembre de 2024 y el estado como en construcción, con inicio en el tercer trimestre de 2024 y fin de obra estimado para el primer trimestre de 2027. Deja en blanco la licencia de primera ocupación y no lleva fecha, por lo que preguntamos en qué punto está la obra.',
  'La fiche d’information indique un permis de construire daté du 18 septembre 2024 et le statut en construction, commencée au troisième trimestre 2024, avec une fin de travaux estimée au premier trimestre 2027. Elle laisse vide le permis de première occupation et ne porte aucune date ; nous demandons donc où en est le chantier.',
  'Das Infoblatt nennt die Baugenehmigung mit Datum vom 18. September 2024 und den Stand als im Bau, begonnen im dritten Quartal 2024, mit geschätztem Bauende im ersten Quartal 2027. Die Erstbezugsgenehmigung lässt es leer, und es trägt kein Datum, daher fragen wir, wie weit der Bau ist.',
  'В информационном листе разрешение на строительство указано с датой 18 сентября 2024 года, статус — строится: работы начались в третьем квартале 2024 года, окончание ориентировочно в первом квартале 2027 года. Разрешение на первое заселение не указано, лист не датирован, поэтому мы уточняем, на какой стадии стройка.',
  'تذكر النشرة التعريفية رخصة بناء مؤرخة في 18 سبتمبر 2024 وأن المشروع قيد الإنشاء، وقد بدأ البناء في الربع الثالث من 2024 ويُقدَّر انتهاؤه في الربع الأول من 2027. وتترك رخصة أول إشغال فارغة ولا تحمل تاريخاً، لذلك نسأل أين وصل البناء.',
  'Het infoblad vermeldt een bouwvergunning van 18 september 2024 en de status als in aanbouw, gestart in het derde kwartaal van 2024, met een geschat einde van de bouw in het eerste kwartaal van 2027. De vergunning voor eerste ingebruikname laat het leeg en het draagt geen datum, dus we vragen hoe ver de bouw is.',
  'Karta informacyjna podaje pozwolenie na budowę z datą 18 września 2024 r. i status w budowie, rozpoczętej w trzecim kwartale 2024 r., z szacowanym zakończeniem w pierwszym kwartale 2027 r. Pozostawia puste pozwolenie na użytkowanie i nie nosi daty, dlatego pytamy, na jakim etapie jest budowa.',
  'Infoarket oppgir en byggetillatelse datert 18. september 2024 og at prosjektet er under bygging, startet i tredje kvartal 2024, med byggeslutt anslått til første kvartal 2027. Det lar ferdigattesten stå tom og har ingen dato, så vi spør hvor langt byggingen er kommet.',
  'Infobladet anger ett bygglov daterat den 18 september 2024 och att projektet är under uppförande, påbörjat under tredje kvartalet 2024, med byggslut beräknat till första kvartalet 2027. Det lämnar slutbeviset tomt och saknar datum, så vi frågar hur långt bygget har kommit.')
p('.overview.metrics[0][1]', '24 viviendas', '24 logements', '24 Wohnungen', '24 квартиры', '24 مسكناً', '24 woningen', '24 mieszkania', '24 boliger', '24 bostäder')
p('.overview.metrics[3][1]', '€599000 - €1090000 + IVA', '€599000 - €1090000 + TVA', '€599000 - €1090000 + MwSt.', '€599000 - €1090000 + НДС',
  '€599000 - €1090000 + ضريبة القيمة المضافة', '€599000 - €1090000 + btw', '€599000 - €1090000 + VAT', '€599000 - €1090000 + mva.', '€599000 - €1090000 + IVA')

# why
p('.why.copy',
  'Viviendas de dos y tres dormitorios con grandes terrazas y vistas al mar en una promoción cerrada de estilo boutique en Estepona, desde €599000 más IVA.',
  'Des logements de deux et trois chambres avec de grandes terrasses et une vue sur la mer dans un programme fermé de type boutique à Estepona, à partir de €599000 plus TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern, großen Terrassen und Meerblick in einer kleinen geschlossenen Anlage in Estepona, ab €599000 plus MwSt.',
  'Квартиры с двумя и тремя спальнями, большими террасами и видом на море в небольшом закрытом комплексе в Эстепоне, от €599000 плюс НДС.',
  'مساكن بغرفتي نوم وثلاث غرف نوم مع تراسات كبيرة وإطلالات على البحر في مشروع مغلق صغير في إستيبونا، ابتداءً من €599000 زائد ضريبة القيمة المضافة.',
  'Woningen met twee en drie slaapkamers, grote terrassen en zeezicht in een kleinschalig besloten project in Estepona, vanaf €599000 plus btw.',
  'Mieszkania z dwiema i trzema sypialniami, dużymi tarasami i widokiem na morze w niewielkiej zamkniętej inwestycji w Esteponie, od €599000 plus VAT.',
  'Boliger med to og tre soverom, store terrasser og sjøutsikt i et lite bevoktet anlegg i Estepona, fra €599000 pluss mva.',
  'Bostäder med två och tre sovrum, stora terrasser och havsutsikt i en liten bevakad anläggning i Estepona, från €599000 plus IVA.')
p('.why.points[0][1]',
  'Compradores que quieren una vivienda nueva de dos o tres dormitorios con una gran terraza en una promoción cerrada pequeña de Estepona, para vivir o como segunda residencia, desde un apartamento en la primera planta hasta un ático con jacuzzi en la cubierta.',
  'Des acheteurs qui veulent un logement neuf de deux ou trois chambres avec une grande terrasse dans un petit programme fermé à Estepona, pour y vivre ou comme résidence secondaire, de l’appartement au premier étage au penthouse avec jacuzzi sur le toit.',
  'Käufer, die eine neue Wohnung mit zwei oder drei Schlafzimmern und einer großen Terrasse in einer kleinen geschlossenen Anlage in Estepona suchen, zum Selbstbewohnen oder als Zweitwohnsitz, von der Wohnung im ersten Obergeschoss bis zum Penthouse mit Whirlpool auf dem Dach.',
  'Покупатели, которым нужна новая квартира с двумя или тремя спальнями и большой террасой в небольшом закрытом комплексе в Эстепоне — для жизни или как вторая недвижимость: от квартиры на втором этаже до пентхауса с джакузи на крыше.',
  'مشترون يريدون مسكناً جديداً بغرفتي نوم أو ثلاث غرف نوم مع تراس كبير في مشروع مغلق صغير في إستيبونا، للسكن أو كمسكن ثانٍ، من شقة في الطابق الأول إلى بنتهاوس بجاكوزي على السطح.',
  'Kopers die een nieuwe woning met twee of drie slaapkamers en een groot terras zoeken in een kleinschalig besloten project in Estepona, om in te wonen of als tweede woning, van een appartement op de eerste verdieping tot een penthouse met jacuzzi op het dak.',
  'Kupujący, którzy szukają nowego mieszkania z dwiema lub trzema sypialniami i dużym tarasem w niewielkiej zamkniętej inwestycji w Esteponie, do zamieszkania lub jako drugi dom, od apartamentu na pierwszym piętrze po penthouse z jacuzzi na dachu.',
  'Kjøpere som vil ha en ny bolig med to eller tre soverom og en stor terrasse i et lite bevoktet anlegg i Estepona, til å bo i eller som feriebolig, fra en leilighet i andre etasje til en toppleilighet med jacuzzi på taket.',
  'Köpare som vill ha en ny bostad med två eller tre sovrum och en stor terrass i en liten bevakad anläggning i Estepona, att bo i eller som andrabostad, från en lägenhet på första våningen till en takvåning med jacuzzi på taket.')
p('.why.points[1][1]',
  'Las cinco viviendas a la venta tienen terrazas de #57.16 a #227.06 [m2] según los planos, y cada ático añade un solárium de #100.97 [m2] con jacuzzi.',
  'Les cinq logements annoncés ont des terrasses de #57.16 à #227.06 [m2] selon les plans, et chaque penthouse ajoute un solarium de #100.97 [m2] avec jacuzzi.',
  'Die fünf gelisteten Wohnungen haben laut Plänen Terrassen von #57.16 bis #227.06 [m2], und jedes Penthouse hat zusätzlich ein Solarium von #100.97 [m2] mit Whirlpool.',
  'У пяти квартир из списка по планам террасы от #57.16 до #227.06 [m2], а каждый пентхаус дополнительно имеет солярий #100.97 [m2] с джакузи.',
  'للمساكن الخمسة المدرجة تراسات تتراوح بين #57.16 و#227.06 [m2] بحسب المخططات، ويضيف كل بنتهاوس سولاريوم بمساحة #100.97 [m2] مع جاكوزي.',
  'De vijf woningen op de lijst hebben volgens de plattegronden terrassen van #57.16 tot #227.06 [m2], en elk penthouse heeft daarbovenop een solarium van #100.97 [m2] met jacuzzi.',
  'Pięć lokali z listy ma według rzutów tarasy od #57.16 do #227.06 [m2], a każdy penthouse ma dodatkowo solarium o powierzchni #100.97 [m2] z jacuzzi.',
  'De fem oppførte boligene har ifølge plantegningene terrasser på #57.16 til #227.06 [m2], og hver toppleilighet har i tillegg en solterrasse på #100.97 [m2] med jacuzzi.',
  'De fem listade bostäderna har enligt planritningarna terrasser på #57.16 till #227.06 [m2], och varje takvåning har dessutom en solterrass på #100.97 [m2] med jacuzzi.')
p('.why.points[2][1]',
  'La ficha informativa sitúa la promoción a 500 metros de la playa y de los servicios locales y da vistas panorámicas al mar. No da otras distancias.',
  'La fiche d’information situe le programme à 500 mètres de la plage et des commerces locaux et mentionne une vue panoramique sur la mer. Elle ne donne aucune autre distance.',
  'Das Infoblatt nennt die Anlage 500 Meter vom Strand und von den örtlichen Einrichtungen entfernt und führt Panorama-Meerblick auf. Weitere Entfernungen gibt es nicht.',
  'В информационном листе комплекс расположен в 500 метрах от пляжа и местной инфраструктуры, указан панорамный вид на море. Других расстояний он не даёт.',
  'تضع النشرة التعريفية المشروع على بعد 500 متر من الشاطئ والمرافق المحلية وتذكر إطلالات بانورامية على البحر. ولا تذكر مسافات أخرى.',
  'Het infoblad plaatst het project op 500 meter van het strand en de lokale voorzieningen en vermeldt panoramisch zeezicht. Andere afstanden geeft het niet.',
  'Karta informacyjna umieszcza inwestycję 500 metrów od plaży i lokalnych usług i podaje panoramiczny widok na morze. Nie podaje innych odległości.',
  'Infoarket plasserer anlegget 500 meter fra stranden og de lokale tilbudene og oppgir panoramautsikt over havet. Det oppgir ingen andre avstander.',
  'Infobladet placerar anläggningen 500 meter från stranden och den lokala servicen och anger panoramautsikt över havet. Det anger inga andra avstånd.')
p('.why.points[3][1]',
  'La lista de disponibilidad y los planos no coinciden en la superficie construida de dos viviendas, los planos dan dos direcciones y el fin de obra es solo una estimación, por lo que lo confirmamos con el promotor antes de cualquier reserva.',
  'La liste de disponibilité et les plans ne concordent pas sur la surface construite de deux logements, les plans donnent deux adresses et la fin des travaux n’est qu’une estimation ; nous le confirmons donc avec le promoteur avant toute réservation.',
  'Die Verfügbarkeitsliste und die Pläne weichen bei der bebauten Fläche von zwei Wohnungen voneinander ab, die Pläne nennen zwei Straßenadressen, und das Bauende ist nur eine Schätzung, daher bestätigen wir dies vor jeder Reservierung mit dem Bauträger.',
  'Список наличия и планы расходятся по застроенной площади двух квартир, на планах указаны два адреса, а окончание строительства — лишь оценка, поэтому до любого бронирования мы подтверждаем это у застройщика.',
  'تختلف قائمة التوفر والمخططات في المساحة المبنية لمسكنين، وتذكر المخططات عنوانين للشارع، ويبقى انتهاء البناء تقديراً فقط، لذلك نؤكد ذلك مع المطوّر قبل أي حجز.',
  'De beschikbaarheidslijst en de plattegronden verschillen in de bebouwde oppervlakte van twee woningen, de plattegronden geven twee straatadressen en het einde van de bouw is slechts een schatting, dus bevestigen wij dit vóór elke reservering bij de ontwikkelaar.',
  'Lista dostępności i rzuty różnią się co do powierzchni zabudowy dwóch lokali, rzuty podają dwa adresy ulic, a zakończenie budowy jest tylko szacunkiem, dlatego potwierdzamy to z deweloperem przed jakąkolwiek rezerwacją.',
  'Tilgjengelighetslisten og plantegningene er uenige om bebygd areal for to boliger, plantegningene oppgir to gateadresser, og byggeslutt er bare et anslag, så vi bekrefter dette med utbyggeren før enhver reservasjon.',
  'Tillgänglighetslistan och planritningarna skiljer sig åt i byggyta för två bostäder, planritningarna anger två gatuadresser och byggslut är bara en uppskattning, så vi bekräftar detta med exploatören före varje reservation.')

# architecture
p('.architecture.copy[0]',
  'En las imágenes, los dos bloques tienen largas losas de terraza blancas en cada nivel, con barandillas de cristal, pérgolas y bordes ajardinados, que descienden por la ladera hacia una piscina y un césped, con el mar al fondo.',
  'Sur les images, les deux bâtiments ont de longues dalles de terrasse blanches à chaque niveau, avec des garde-corps en verre, des pergolas et des bords plantés, qui descendent la pente vers une piscine et une pelouse, avec la mer au fond.',
  'Auf den Bildern haben die beiden Gebäude auf jeder Ebene lange weiße Terrassenplatten mit Glasbrüstungen, Pergolen und bepflanzten Rändern, die den Hang hinunter zu einem Pool und einem Rasen führen, dahinter das Meer.',
  'На изображениях у двух корпусов на каждом уровне длинные белые плиты террас со стеклянными ограждениями, пергола и озеленёнными краями, спускающиеся по склону к бассейну и газону, вдали море.',
  'في الصور، للمبنيين بلاطات تراس بيضاء طويلة في كل مستوى، مع حواجز زجاجية وبرجولات وحواف مزروعة، تنحدر على السفح نحو مسبح ومرج، والبحر في الخلفية.',
  'Op de beelden hebben de twee blokken op elk niveau lange witte terrasplaten met glazen balustrades, pergola’s en beplante randen, die langs de helling afdalen naar een zwembad en een gazon, met de zee op de achtergrond.',
  'Na wizualizacjach oba budynki mają na każdym poziomie długie białe płyty tarasów ze szklanymi balustradami, pergolami i obsadzonymi roślinnością krawędziami, schodzące po zboczu w stronę basenu i trawnika, a w tle widać morze.',
  'På bildene har de to byggene lange hvite terrasseplater på hvert nivå, med glassrekkverk, pergolaer og beplantede kanter, som går nedover skråningen mot et basseng og en plen, med havet i bakgrunnen.',
  'På bilderna har de två byggnaderna långa vita terrassplattor på varje plan, med glasräcken, pergolor och planterade kanter, som löper nedför sluttningen mot en pool och en gräsmatta, med havet i bakgrunden.')
p('.architecture.copy[1]',
  'La memoria de calidades describe una ambiciosa fachada vanguardista con materiales innovadores para una mayor eficiencia energética, con distribuciones interiores estudiadas y detalles de calidad en el portal y las zonas comunes.',
  'Le descriptif de qualité décrit une façade d’avant-garde ambitieuse, en matériaux innovants pour une meilleure efficacité énergétique, avec des distributions intérieures étudiées et des détails de qualité dans l’entrée et les parties communes.',
  'Die Bau- und Ausstattungsbeschreibung nennt eine ambitionierte avantgardistische Fassade aus innovativen Materialien für höhere Energieeffizienz, mit durchdachten Grundrissen und hochwertigen Details im Eingangsbereich und in den Gemeinschaftsbereichen.',
  'В спецификации качества описан амбициозный авангардный фасад из инновационных материалов для повышения энергоэффективности, с продуманными планировками и качественными деталями в входной группе и местах общего пользования.',
  'تصف مواصفات الجودة واجهة طموحة طليعية بمواد مبتكرة لرفع كفاءة الطاقة، مع توزيعات داخلية مدروسة وتفاصيل عالية الجودة في المدخل والمناطق المشتركة.',
  'De kwaliteitsspecificatie beschrijft een ambitieuze avant-gardistische gevel in innovatieve materialen voor een hogere energie-efficiëntie, met doordachte indelingen en kwalitatieve details in de entree en de gemeenschappelijke delen.',
  'Specyfikacja jakości opisuje ambitną awangardową elewację z innowacyjnych materiałów, zapewniającą wyższą efektywność energetyczną, z przemyślanymi układami wnętrz i wysokiej jakości detalami w wejściu i częściach wspólnych.',
  'Kvalitetsspesifikasjonen beskriver en ambisiøs avantgardistisk fasade i innovative materialer for høyere energieffektivitet, med gjennomtenkte planløsninger og kvalitetsdetaljer i inngangen og fellesarealene.',
  'Kvalitetsspecifikationen beskriver en ambitiös avantgardistisk fasad i innovativa material för högre energieffektivitet, med genomtänkta planlösningar och kvalitetsdetaljer i entrén och de gemensamma utrymmena.')
p('.architecture.highlights[0][0]', 'Altura libre', 'Hauteur sous plafond', 'Raumhöhe', 'Высота потолков', 'ارتفاع السقف', 'Plafondhoogte', 'Wysokość pomieszczeń', 'Takhøyde', 'Takhöjd')
p('.architecture.highlights[0][1]', '#2.70 m, según la ficha informativa.', '#2.70 m, selon la fiche d’information.', '#2.70 m laut Infoblatt.',
  '#2.70 м по информационному листу.', '#2.70 م بحسب النشرة التعريفية.', '#2.70 m volgens het infoblad.', '#2.70 m według karty informacyjnej.',
  '#2.70 m ifølge infoarket.', '#2.70 m enligt infobladet.')
p('.architecture.highlights[1][1]',
  'Solería continua de gres porcelánico rectificado de gran formato en toda la vivienda; la ficha informativa nombra porcelánico Porcelanosa en formato 1 x 1 m.',
  'Sol continu en grès cérame rectifié grand format dans tout le logement ; la fiche d’information cite du grès cérame Porcelanosa au format 1 x 1 m.',
  'Durchgehender Bodenbelag aus großformatigem, rektifiziertem Feinsteinzeug in der ganzen Wohnung; das Infoblatt nennt Porcelanosa-Feinsteinzeug im Format 1 x 1 m.',
  'Сплошное покрытие пола из крупноформатного ректифицированного керамогранита во всей квартире; в информационном листе указан керамогранит Porcelanosa формата 1 x 1 м.',
  'أرضيات متصلة من الجرانيت الخزفي المقطوع بدقة بحجم كبير في كامل المسكن؛ وتذكر النشرة التعريفية خزف Porcelanosa بقياس 1 × 1 م.',
  'Doorlopende vloer van grootformaat gerectificeerd porseleinen steengoed in de hele woning; het infoblad noemt Porcelanosa-porselein in het formaat 1 x 1 m.',
  'Ciągła podłoga z wielkoformatowego gresu rektyfikowanego w całym mieszkaniu; karta informacyjna wymienia gres Porcelanosa w formacie 1 x 1 m.',
  'Sammenhengende gulv i storformat rektifisert porselensfliser i hele boligen; infoarket nevner Porcelanosa-fliser i formatet 1 x 1 m.',
  'Sammanhängande golv i storformat rektifierat porslinsgods i hela bostaden; infobladet nämner Porcelanosa-klinker i formatet 1 x 1 m.')
p('.architecture.highlights[2][1]',
  'Perfiles de aluminio beige con doble acristalamiento para el aislamiento térmico y acústico y el ahorro de energía, y persianas motorizadas en los dormitorios.',
  'Profilés en aluminium beige avec double vitrage pour l’isolation thermique et acoustique et les économies d’énergie, et volets motorisés dans les chambres.',
  'Beige Aluminiumprofile mit Doppelverglasung für Wärme- und Schallschutz und Energieeinsparung sowie motorisierte Rollläden in den Schlafzimmern.',
  'Профили из алюминия бежевого цвета с двойным остеклением для тепло- и звукоизоляции и экономии энергии, моторизованные жалюзи в спальнях.',
  'إطارات من الألمنيوم بلون بيج مع زجاج مزدوج للعزل الحراري والصوتي وتوفير الطاقة، وستائر معدنية بمحركات في غرف النوم.',
  'Beige aluminium profielen met dubbele beglazing voor thermische en akoestische isolatie en energiebesparing, en gemotoriseerde rolluiken in de slaapkamers.',
  'Beżowe profile aluminiowe z podwójnymi szybami zapewniającymi izolację termiczną i akustyczną oraz oszczędność energii, a w sypialniach zmotoryzowane rolety.',
  'Beige aluminiumsprofiler med dobbeltvindu for varme- og lydisolasjon og energisparing, og motoriserte persienner i soverommene.',
  'Beiga aluminiumprofiler med dubbelglas för värme- och ljudisolering och energibesparing, samt motoriserade persienner i sovrummen.')
p('.architecture.highlights[3][1]',
  'Agua caliente, calefacción y refrigeración con un sistema de aerotermia individual en cada vivienda, con aire acondicionado por conductos.',
  'Eau chaude, chauffage et rafraîchissement par un système aérothermique individuel dans chaque logement, avec climatisation par gaines.',
  'Warmwasser, Heizung und Kühlung über eine individuelle Luft-Wasser-Wärmepumpe in jeder Wohnung, mit Kanalklimaanlage.',
  'Горячая вода, отопление и охлаждение от индивидуальной аэротермальной системы в каждой квартире, с канальным кондиционированием.',
  'مياه ساخنة وتدفئة وتبريد من نظام حراري هوائي فردي في كل مسكن، مع تكييف هواء عبر مجارٍ.',
  'Warm water, verwarming en koeling via een individuele lucht-waterwarmtepomp in elke woning, met kanaalairco.',
  'Ciepła woda, ogrzewanie i chłodzenie z indywidualnego systemu aerotermalnego w każdym mieszkaniu, z klimatyzacją kanałową.',
  'Varmtvann, oppvarming og kjøling fra et individuelt luft-til-vann-varmepumpesystem i hver bolig, med kanalklimaanlegg.',
  'Varmvatten, värme och kyla från ett individuellt luft-vattenvärmepumpssystem i varje bostad, med kanalluftkonditionering.')

# quality specs
p('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades de los documentos del promotor, que no lleva fecha. Indica que se encuentra en fase de desarrollo y que sus referencias pueden cambiar por razones técnicas sin reducir la calidad ni el diseño del resultado, y que el mobiliario de cocina que aparece es una muestra esquemática que puede variar.',
  'Source : le descriptif de qualité figurant dans les documents du promoteur, qui n’est pas daté. Il indique qu’il est à un stade de développement et que ses références peuvent changer pour des raisons techniques sans réduire la qualité ni le design du résultat, et que le mobilier de cuisine représenté est un échantillon schématique qui peut varier.',
  'Quelle: die Bau- und Ausstattungsbeschreibung in den Unterlagen des Bauträgers, die kein Datum trägt. Sie besagt, dass sie sich im Entwicklungsstadium befindet und ihre Angaben aus technischen Gründen geändert werden können, ohne Qualität oder Design des Ergebnisses zu mindern, und dass die gezeigten Küchenmöbel ein schematisches Muster sind, das abweichen kann.',
  'Источник: спецификация качества в документах застройщика, не имеющая даты. В ней сказано, что она находится на стадии разработки и что её позиции могут меняться по техническим причинам без снижения качества и дизайна результата, а показанная кухонная мебель — схематический образец, который может отличаться.',
  'المصدر: مواصفات الجودة في وثائق المطوّر، وهي غير مؤرخة. وتنص على أنها في مرحلة التطوير وأن مراجعها قد تتغير لأسباب فنية دون خفض جودة النتيجة أو تصميمها، وأن أثاث المطبخ المعروض عينة تخطيطية قد تتغير.',
  'Bron: de kwaliteitsspecificatie in de documenten van de ontwikkelaar, die geen datum draagt. Ze vermeldt dat ze zich in de ontwikkelingsfase bevindt en dat de referenties om technische redenen kunnen wijzigen zonder de kwaliteit of het ontwerp van het resultaat te verminderen, en dat het getoonde keukenmeubilair een schematisch voorbeeld is dat kan afwijken.',
  'Źródło: specyfikacja jakości w dokumentach dewelopera, która nie nosi daty. Podaje, że jest na etapie opracowania i że jej pozycje mogą się zmienić z przyczyn technicznych bez obniżenia jakości i projektu efektu końcowego, a pokazane meble kuchenne to schematyczny przykład, który może się różnić.',
  'Kilde: kvalitetsspesifikasjonen i utbyggerens dokumenter, som ikke har dato. Den sier at den er på utviklingsstadiet og at henvisningene kan endres av tekniske grunner uten at kvaliteten eller designet på resultatet reduseres, og at kjøkkenmøblene som vises er en skjematisk prøve som kan variere.',
  'Källa: kvalitetsspecifikationen i exploatörens dokument, som saknar datum. Den anger att den är på utvecklingsstadiet och att dess referenser kan ändras av tekniska skäl utan att kvaliteten eller designen på resultatet minskar, och att köksmöblerna som visas är ett schematiskt exempel som kan variera.')
p('.qualitySpecs.groups[0].items[0]',
  'Solería continua de gres porcelánico rectificado de gran formato en toda la vivienda.',
  'Sol continu en grès cérame rectifié grand format dans tout le logement.',
  'Durchgehender Bodenbelag aus großformatigem, rektifiziertem Feinsteinzeug in der ganzen Wohnung.',
  'Сплошное покрытие пола из крупноформатного ректифицированного керамогранита во всей квартире.',
  'أرضيات متصلة من الجرانيت الخزفي المقطوع بدقة بحجم كبير في كامل المسكن.',
  'Doorlopende vloer van grootformaat gerectificeerd porseleinen steengoed in de hele woning.',
  'Ciągła podłoga z wielkoformatowego gresu rektyfikowanego w całym mieszkaniu.',
  'Sammenhengende gulv i storformat rektifisert porselensfliser i hele boligen.',
  'Sammanhängande golv i storformat rektifierat porslinsgods i hela bostaden.')
p('.qualitySpecs.groups[0].items[1]',
  'El baño principal se reviste con gres de gran formato con efecto mármol blanco, y el segundo baño con una combinación de PORCELANOSA o similar.',
  'La salle de bains principale est revêtue de grès grand format effet marbre blanc, et la seconde salle de bains d’une combinaison de PORCELANOSA ou équivalent.',
  'Das Hauptbad ist mit großformatigem Feinsteinzeug in weißer Marmoroptik gefliest, das zweite Bad mit einer Kombination von PORCELANOSA oder Ähnlichem.',
  'Главная ванная облицована крупноформатным керамогранитом с эффектом белого мрамора, вторая ванная — комбинацией PORCELANOSA или аналогичной.',
  'يُكسى الحمام الرئيسي بخزف كبير الحجم بتأثير الرخام الأبيض، ويُكسى الحمام الثاني بتشكيلة من PORCELANOSA أو ما يماثلها.',
  'De hoofdbadkamer is betegeld met grootformaat steengoed met een witte marmerlook, en de tweede badkamer met een combinatie van PORCELANOSA of vergelijkbaar.',
  'Główna łazienka jest wyłożona wielkoformatowym gresem o wyglądzie białego marmuru, a druga łazienka kombinacją płytek PORCELANOSA lub podobnych.',
  'Hovedbadet er flislagt med storformat fliser med hvit marmoreffekt, og det andre badet med en kombinasjon fra PORCELANOSA eller tilsvarende.',
  'Huvudbadrummet är klätt med storformatsplattor med vit marmoreffekt och det andra badrummet med en kombination från PORCELANOSA eller liknande.')
p('.qualitySpecs.groups[1].items[0]',
  'Un mueble de lavabo suspendido con dos cajones y espejo, una mampara de ducha de cristal transparente y, en el baño principal, un inodoro suspendido y un espejo iluminado antivaho.',
  'Un meuble-vasque suspendu à deux tiroirs avec miroir, une paroi de douche en verre transparent et, dans la salle de bains principale, des WC suspendus et un miroir éclairé anti-buée.',
  'Ein wandhängender Waschtischunterschrank mit zwei Schubladen und Spiegel, eine Duschabtrennung aus Klarglas und im Hauptbad ein wandhängendes WC sowie ein beleuchteter Spiegel mit Antibeschlagfunktion.',
  'Подвесная тумба с раковиной на два ящика и зеркало, прозрачная стеклянная душевая перегородка, а в главной ванной — подвесной унитаз и зеркало с подсветкой и защитой от запотевания.',
  'خزانة مغسلة معلقة بدرجين ومرآة، وحاجز دش من الزجاج الشفاف، وفي الحمام الرئيسي مرحاض معلق ومرآة مضاءة مضادة للضباب.',
  'Een hangend wastafelmeubel met twee laden en spiegel, een douchewand van helder glas en in de hoofdbadkamer een hangend toilet en een verlichte spiegel met antidampfunctie.',
  'Wisząca szafka umywalkowa z dwiema szufladami i lustrem, przezroczysta szklana kabina prysznicowa, a w głównej łazience wiszący sedes i podświetlane lustro z funkcją antyparową.',
  'Et veggmontert servantskap med to skuffer og speil, en dusjvegg i klart glass og, på hovedbadet, et veggmontert toalett og et opplyst speil som motvirker dugg.',
  'Ett väggmonterat tvättskåp med två lådor och spegel, en duschvägg i klarglas och, i huvudbadrummet, en väggmonterad toalett och en upplyst spegel som motverkar imma.')
p('.qualitySpecs.groups[1].items[1]',
  'Grifería negro mate y una ducha termostática en el baño principal, con rociador tipo lluvia, sistema antical, botón de seguridad a 40 °C y ángulo de ducha fija ajustable.',
  'Robinetterie noir mat et douche thermostatique dans la salle de bains principale, avec pomme de pluie, système anticalcaire, bouton de sécurité à 40 °C et angle de douche fixe réglable.',
  'Mattschwarze Armaturen und eine Thermostatdusche im Hauptbad, mit Regenbrause, Kalkschutzsystem, Sicherheitstaste bei 40 °C und verstellbarem Winkel der festen Brause.',
  'Матовые чёрные смесители и термостатический душ в главной ванной: тропический душ, система против накипи, кнопка безопасности на 40 °C и регулируемый угол фиксированной лейки.',
  'حنفيات سوداء مطفأة ودش ثرموستاتي في الحمام الرئيسي، برأس مطري ونظام مضاد للكلس وزر أمان عند 40 °م وزاوية قابلة للضبط للدش الثابت.',
  'Mat zwarte kranen en een thermostatische douche in de hoofdbadkamer, met regendouche, antikalksysteem, veiligheidsknop op 40 °C en een verstelbare hoek van de vaste douchekop.',
  'Matowe czarne baterie i prysznic termostatyczny w głównej łazience, z deszczownicą, systemem przeciw osadzaniu się kamienia, przyciskiem bezpieczeństwa na 40 °C i regulowanym kątem stałej głowicy.',
  'Matt svarte kraner og en termostatisk dusj på hovedbadet, med regndusj, kalkbeskyttelse, sikkerhetsknapp ved 40 °C og justerbar vinkel på den faste dusjhodet.',
  'Mattsvarta kranar och en termostatisk dusch i huvudbadrummet, med regnduschhuvud, kalkskydd, säkerhetsknapp vid 40 °C och justerbar vinkel på det fasta duschhuvudet.')
p('.qualitySpecs.groups[2].items[0]',
  'Puertas interiores lacadas en blanco con herrajes cromados, y armarios tipo block forrados interiormente con balda intermedia, barra para colgar y una cajonera.',
  'Portes intérieures laquées blanc avec quincaillerie chromée, et placards de type bloc doublés à l’intérieur avec tablette intermédiaire, barre de penderie et un bloc tiroirs.',
  'Weiß lackierte Innentüren mit verchromten Beschlägen und innen ausgekleidete Blockschränke mit Zwischenboden, Kleiderstange und einem Schubladenelement.',
  'Межкомнатные двери, окрашенные в белый, с хромированной фурнитурой и шкафы блочного типа с внутренней отделкой, промежуточной полкой, штангой для одежды и блоком ящиков.',
  'أبواب داخلية مطلية باللون الأبيض بإكسسوارات كروم، وخزائن ملابس مبطنة من الداخل برف وسطي وعمود تعليق ووحدة أدراج.',
  'Wit gelakte binnendeuren met verchroomd beslag, en inwendig bekleedde blokkasten met een tussenplank, een kledingstang en een ladeblok.',
  'Drzwi wewnętrzne lakierowane na biało z chromowanymi okuciami oraz szafy blokowe wyłożone wewnątrz, z półką pośrednią, drążkiem na ubrania i blokiem szuflad.',
  'Hvitlakkerte innerdører med forkrommede beslag, og innvendig kledde blokkskap med mellomhylle, kleshenger og en skuffeseksjon.',
  'Vitlackerade innerdörrar med kromade beslag och invändigt klädda blockgarderober med mellanhylla, klädstång och en lådenhet.')
p('.qualitySpecs.groups[2].items[1]',
  'Carpintería exterior de aluminio beige con doble acristalamiento para el aislamiento térmico y acústico y el ahorro de energía, y persianas motorizadas con pulsador en los dormitorios.',
  'Menuiseries extérieures en aluminium beige avec double vitrage pour l’isolation thermique et acoustique et les économies d’énergie, et volets motorisés avec bouton-poussoir dans les chambres.',
  'Beige Aluminium-Außenrahmen mit Doppelverglasung für Wärme- und Schallschutz und Energieeinsparung sowie motorisierte Rollläden mit Taster in den Schlafzimmern.',
  'Наружные рамы из алюминия бежевого цвета с двойным остеклением для тепло- и звукоизоляции и экономии энергии, моторизованные жалюзи с кнопкой в спальнях.',
  'إطارات خارجية من الألمنيوم بلون بيج مع زجاج مزدوج للعزل الحراري والصوتي وتوفير الطاقة، وستائر معدنية بمحركات وزر تحكم في غرف النوم.',
  'Beige aluminium buitenkozijnen met dubbele beglazing voor thermische en akoestische isolatie en energiebesparing, en gemotoriseerde rolluiken met drukknop in de slaapkamers.',
  'Stolarka zewnętrzna z beżowego aluminium z podwójnymi szybami zapewniającymi izolację termiczną i akustyczną oraz oszczędność energii, a w sypialniach zmotoryzowane rolety z przyciskiem.',
  'Utvendige rammer i beige aluminium med dobbeltvindu for varme- og lydisolasjon og energisparing, og motoriserte persienner med trykknapp i soverommene.',
  'Yttre karmar i beige aluminium med dubbelglas för värme- och ljudisolering och energibesparing, samt motoriserade persienner med knapp i sovrummen.')
p('.qualitySpecs.groups[3].items[0]',
  'Placa de inducción, microondas, horno, campana extractora, frigorífico, lavavajillas, y fregadero y grifo.',
  'Plaque à induction, micro-ondes, four, hotte aspirante, réfrigérateur, lave-vaisselle, évier et robinet.',
  'Induktionskochfeld, Mikrowelle, Backofen, Dunstabzugshaube, Kühlschrank, Geschirrspüler sowie Spüle und Armatur.',
  'Индукционная варочная панель, микроволновая печь, духовой шкаф, вытяжка, холодильник, посудомоечная машина, мойка и смеситель.',
  'سطح طهي بالحث ومايكروويف وفرن وشفاط وثلاجة وغسالة أطباق وحوض وحنفية.',
  'Een inductiekookplaat, een magnetron, een oven, een afzuigkap, een koelkast, een vaatwasser, en een spoelbak met kraan.',
  'Płyta indukcyjna, mikrofalówka, piekarnik, okap, lodówka, zmywarka oraz zlewozmywak z baterią.',
  'Induksjonstopp, mikrobølgeovn, ovn, ventilator, kjøleskap, oppvaskmaskin, og vask og kran.',
  'Induktionshäll, mikrovågsugn, ugn, köksfläkt, kylskåp, diskmaskin samt diskho och kran.')
p('.qualitySpecs.groups[3].items[1]',
  'Iluminación con tira de led bajo el mobiliario para iluminar la zona de trabajo.',
  'Éclairage par bandeau LED sous les meubles pour éclairer le plan de travail.',
  'LED-Streifenbeleuchtung unter den Schränken zur Beleuchtung des Arbeitsbereichs.',
  'Светодиодная подсветка под шкафами для освещения рабочей зоны.',
  'إضاءة بشريط LED تحت الوحدات لإضاءة منطقة العمل.',
  'LED-stripverlichting onder de kasten om het werkvlak te verlichten.',
  'Oświetlenie taśmą LED pod szafkami, oświetlające strefę roboczą.',
  'LED-stripebelysning under skapene for å lyse opp arbeidsområdet.',
  'LED-slingor under skåpen som lyser upp arbetsytan.')
p('.qualitySpecs.groups[4].name', 'Clima, energía y aislamientos', 'Climatisation, énergie et isolation', 'Klima, Energie und Dämmung',
  'Климат, энергия и изоляция', 'المناخ والطاقة والعزل', 'Klimaat, energie en isolatie', 'Klimat, energia i izolacje', 'Klima, energi og isolasjon', 'Klimat, energi och isolering')
p('.qualitySpecs.groups[4].items[0]',
  'Agua caliente, calefacción y refrigeración con un sistema de aerotermia individual en cada vivienda, que según la memoria ahorra gastos de comunidad porque solo se usa cuando hace falta, con aire acondicionado por conductos cuyas máquinas van en el falso techo de los baños.',
  'Eau chaude, chauffage et rafraîchissement par un système aérothermique individuel dans chaque logement, qui, selon le descriptif, réduit les charges de copropriété car il n’est utilisé qu’en cas de besoin, avec une climatisation par gaines dont les machines sont placées dans le faux plafond des salles de bains.',
  'Warmwasser, Heizung und Kühlung über eine individuelle Luft-Wasser-Wärmepumpe in jeder Wohnung, die laut Beschreibung Gemeinschaftskosten spart, weil sie nur bei Bedarf läuft, mit Kanalklimaanlage, deren Geräte in der Abhangdecke der Bäder sitzen.',
  'Горячая вода, отопление и охлаждение от индивидуальной аэротермальной системы в каждой квартире, которая, как сказано в спецификации, снижает расходы на содержание дома, поскольку работает только по необходимости, с канальным кондиционированием, агрегаты которого размещены в подвесных потолках ванных комнат.',
  'مياه ساخنة وتدفئة وتبريد من نظام حراري هوائي فردي في كل مسكن، وتقول المواصفات إنه يوفر مصاريف المجمع لأنه يُستخدم عند الحاجة فقط، مع تكييف هواء عبر مجارٍ تقع آلاته في السقف المستعار للحمامات.',
  'Warm water, verwarming en koeling via een individuele lucht-waterwarmtepomp in elke woning, die volgens de specificatie kosten van de gemeenschap bespaart omdat ze alleen wordt gebruikt wanneer dat nodig is, met kanaalairco waarvan de units in het verlaagde plafond van de badkamers zitten.',
  'Ciepła woda, ogrzewanie i chłodzenie z indywidualnego systemu aerotermalnego w każdym mieszkaniu, który według specyfikacji obniża koszty wspólnoty, bo działa tylko w razie potrzeby, z klimatyzacją kanałową, której urządzenia znajdują się w podwieszanych sufitach łazienek.',
  'Varmtvann, oppvarming og kjøling fra et individuelt luft-til-vann-varmepumpesystem i hver bolig, som ifølge spesifikasjonen sparer fellesutgifter fordi det bare brukes ved behov, med kanalklimaanlegg der enhetene sitter i det nedsenkede taket på badene.',
  'Varmvatten, värme och kyla från ett individuellt luft-vattenvärmepumpssystem i varje bostad, som enligt specifikationen sparar gemensamma kostnader eftersom det bara används vid behov, med kanalluftkonditionering vars enheter sitter i undertaket i badrummen.')
p('.qualitySpecs.groups[4].items[1]',
  'Aislamiento acústico antiimpacto en todas las viviendas, aislamiento termoacústico en los cerramientos exteriores y entre viviendas, y un sistema de bajantes insonorizado de tres capas.',
  'Isolation acoustique anti-bruit d’impact dans tous les logements, isolation thermique et acoustique des murs extérieurs et entre les logements, et un système de descentes insonorisé à trois couches.',
  'Trittschalldämmung in allen Wohnungen, Wärme- und Schalldämmung der Außenwände und zwischen den Wohnungen sowie ein dreischichtiges schallgedämmtes Fallrohrsystem.',
  'Противоударная звукоизоляция во всех квартирах, тепло- и звукоизоляция наружных стен и стен между квартирами и трёхслойная шумоизолированная система стояков.',
  'عزل صوتي مضاد للصدمات في جميع المساكن، وعزل حراري وصوتي للجدران الخارجية وبين المساكن، ونظام أنابيب تصريف عازل للصوت من ثلاث طبقات.',
  'Contactgeluidisolatie in alle woningen, thermische en akoestische isolatie van de buitenmuren en tussen de woningen, en een driedelig geluiddicht afvoersysteem.',
  'Izolacja akustyczna od dźwięków uderzeniowych we wszystkich mieszkaniach, izolacja termiczna i akustyczna ścian zewnętrznych i między mieszkaniami oraz trójwarstwowy wyciszony system pionów.',
  'Trinnlydisolasjon i alle boligene, varme- og lydisolasjon i yttervegger og mellom boligene, og et lydisolert nedløpssystem i tre lag.',
  'Stegljudsisolering i alla bostäder, värme- och ljudisolering i ytterväggar och mellan bostäder samt ett tredelat ljudisolerat stamsystem.')
p('.qualitySpecs.groups[5].name', 'Instalación eléctrica, telecomunicaciones y zonas comunes', 'Électricité, télécommunications et parties communes',
  'Elektrik, Telekommunikation und Gemeinschaftsbereiche', 'Электрика, связь и места общего пользования',
  'الكهرباء والاتصالات والمناطق المشتركة', 'Elektra, telecom en gemeenschappelijke delen', 'Instalacja elektryczna, telekomunikacja i części wspólne',
  'Elektrisk, telekom og fellesarealer', 'El, telekom och gemensamma utrymmen')
p('.qualitySpecs.groups[5].items[0]',
  'Mecanismos eléctricos serie Simon 100, iluminación led en baños y cocina, videoportero en el acceso y fibra óptica en el edificio con tomas en el salón y los dormitorios.',
  'Appareillage électrique de la série Simon 100, éclairage LED dans les salles de bains et la cuisine, interphone vidéo à l’entrée et fibre optique dans l’immeuble avec prises dans le séjour et les chambres.',
  'Schalter und Steckdosen der Serie Simon 100, LED-Beleuchtung in Bädern und Küche, Videosprechanlage am Eingang und Glasfaser im Gebäude mit Anschlüssen im Wohnzimmer und in den Schlafzimmern.',
  'Электроустановочные изделия серии Simon 100, светодиодное освещение в ванных и на кухне, видеодомофон у входа и оптоволокно в здании с розетками в гостиной и спальнях.',
  'مفاتيح ومقابس من سلسلة Simon 100، وإضاءة LED في الحمامات والمطبخ، وجرس مرئي عند المدخل، وألياف ضوئية في المبنى مع مخارج في غرفة المعيشة وغرف النوم.',
  'Schakelmateriaal uit de Simon 100-serie, ledverlichting in de badkamers en keuken, een videofoon bij de ingang en glasvezel in het gebouw met aansluitingen in de woonkamer en slaapkamers.',
  'Osprzęt elektryczny serii Simon 100, oświetlenie LED w łazienkach i kuchni, wideodomofon przy wejściu oraz światłowód w budynku z gniazdami w salonie i sypialniach.',
  'Brytere og stikkontakter fra Simon 100-serien, LED-belysning på bad og kjøkken, videoporttelefon ved inngangen og fiber i bygget med uttak i stuen og soverommene.',
  'Strömbrytare och eluttag i serien Simon 100, led-belysning i badrum och kök, en videodörrtelefon vid entrén och fiber i byggnaden med uttag i vardagsrummet och sovrummen.')
p('.qualitySpecs.groups[5].items[1]',
  'Puerta de garaje motorizada con mando a distancia y ascensor hasta el nivel de aparcamiento que sirve a todas las plantas, con ventilación mecánica controlada de las viviendas y presión de agua constante gracias a un aljibe y un grupo de bombeo.',
  'Porte de garage motorisée avec télécommande et ascenseur jusqu’au niveau du parking desservant tous les étages, avec ventilation mécanique contrôlée des logements et pression d’eau constante grâce à une cuve de stockage et un groupe de pompage.',
  'Motorisiertes Garagentor mit Fernbedienung und ein Aufzug bis zur Parkebene, der alle Etagen bedient, mit kontrollierter mechanischer Wohnraumlüftung und konstantem Wasserdruck durch einen Speichertank und eine Pumpenanlage.',
  'Моторизованные гаражные ворота с пультом и лифт до уровня парковки, обслуживающий все этажи, контролируемая механическая вентиляция квартир и постоянное давление воды благодаря накопительной ёмкости и насосной станции.',
  'باب مرآب بمحرك مع جهاز تحكم عن بعد ومصعد حتى مستوى المواقف يخدم جميع الطوابق، مع تهوية ميكانيكية متحكم بها للمساكن وضغط ماء ثابت بفضل خزان ومجموعة ضخ.',
  'Een gemotoriseerde garagedeur met afstandsbediening en een lift tot op het parkeerniveau die alle verdiepingen bedient, met gecontroleerde mechanische ventilatie van de woningen en constante waterdruk dankzij een opslagtank en een pompgroep.',
  'Zmotoryzowana brama garażowa z pilotem i winda do poziomu parkingu obsługująca wszystkie piętra, z kontrolowaną wentylacją mechaniczną mieszkań i stałym ciśnieniem wody dzięki zbiornikowi i zespołowi pompowemu.',
  'Motorisert garasjeport med fjernkontroll og en heis til parkeringsnivået som betjener alle etasjer, med kontrollert mekanisk ventilasjon av boligene og jevnt vanntrykk takket være en lagringstank og et pumpeaggregat.',
  'En motoriserad garageport med fjärrkontroll och en hiss till parkeringsplanet som betjänar alla våningar, med kontrollerad mekanisk ventilation av bostäderna och jämnt vattentryck tack vare en lagringstank och ett pumpaggregat.')

# residences
p('.residences.headlineHtml', 'Cinco viviendas, <em>cuatro tipos</em>', 'Cinq logements, <em>quatre types</em>', 'Fünf Wohnungen, <em>vier Arten</em>',
  'Пять квартир, <em>четыре типа</em>', 'خمسة مساكن، <em>أربعة أنواع</em>', 'Vijf woningen, <em>vier soorten</em>',
  'Pięć mieszkań, <em>cztery rodzaje</em>', 'Fem boliger, <em>fire typer</em>', 'Fem bostäder, <em>fyra slag</em>')
p('.residences.copy',
  'Las cinco viviendas a la venta se dividen en cuatro grupos según la planta y el espacio exterior. La tabla siguiente enumera cada una con su precio.',
  'Les cinq logements annoncés se répartissent en quatre groupes selon l’étage et l’espace extérieur. Le tableau ci-dessous les présente un par un avec leur prix.',
  'Die fünf gelisteten Wohnungen gliedern sich nach Etage und Außenbereich in vier Gruppen. Die Tabelle unten führt jede mit ihrem Preis auf.',
  'Пять квартир из списка делятся на четыре группы по этажу и наружному пространству. В таблице ниже каждая указана с ценой.',
  'تنقسم المساكن الخمسة المدرجة إلى أربع مجموعات بحسب الطابق والمساحة الخارجية. ويعرض الجدول أدناه كلاً منها مع سعره.',
  'De vijf woningen op de lijst vallen naar verdieping en buitenruimte in vier groepen uiteen. De tabel hieronder toont elke woning met haar prijs.',
  'Pięć lokali z listy dzieli się na cztery grupy według piętra i przestrzeni zewnętrznej. Tabela poniżej wymienia każdy z ceną.',
  'De fem oppførte boligene deler seg i fire grupper etter etasje og utearealer. Tabellen under viser hver enkelt med pris.',
  'De fem listade bostäderna delar sig i fyra grupper efter våning och uteyta. Tabellen nedan visar var och en med pris.')
p('.residences.items[0].name', 'Áticos con solárium y jacuzzi', 'Penthouses avec solarium et jacuzzi', 'Penthäuser mit Solarium und Whirlpool',
  'Пентхаусы с солярием и джакузи', 'بنتهاوس مع سولاريوم وجاكوزي', 'Penthouses met solarium en jacuzzi', 'Penthouse’y z solarium i jacuzzi',
  'Toppleiligheter med solterrasse og jacuzzi', 'Takvåningar med solterrass och jacuzzi')
p('.residences.items[0].points[0]',
  'Dos viviendas de tres dormitorios, 1.02.A y 1.02.B, en el portal 1, cada una con #153.50 [m2] construidos, #98.13 [m2] interiores, una terraza de #69.78 [m2] y un solárium de #100.97 [m2] con jacuzzi.',
  'Deux logements de trois chambres, 1.02.A et 1.02.B, dans la cage 1, chacun avec #153.50 [m2] construits, #98.13 [m2] intérieurs, une terrasse de #69.78 [m2] et un solarium de #100.97 [m2] avec jacuzzi.',
  'Zwei Wohnungen mit drei Schlafzimmern, 1.02.A und 1.02.B, in Aufgang 1, jede mit #153.50 [m2] bebauter Fläche, #98.13 [m2] Innenfläche, einer Terrasse von #69.78 [m2] und einem Solarium von #100.97 [m2] mit Whirlpool.',
  'Две квартиры с тремя спальнями, 1.02.A и 1.02.B, в подъезде 1, каждая с застроенной площадью #153.50 [m2], внутренней площадью #98.13 [m2], террасой #69.78 [m2] и солярием #100.97 [m2] с джакузи.',
  'مسكنان بثلاث غرف نوم، 1.02.A و1.02.B، في المدخل 1، لكل منهما #153.50 [m2] مبنية و#98.13 [m2] داخلية وتراس بمساحة #69.78 [m2] وسولاريوم بمساحة #100.97 [m2] مع جاكوزي.',
  'Twee woningen met drie slaapkamers, 1.02.A en 1.02.B, in portiek 1, elk met #153.50 [m2] bebouwd, #98.13 [m2] binnen, een terras van #69.78 [m2] en een solarium van #100.97 [m2] met jacuzzi.',
  'Dwa mieszkania z trzema sypialniami, 1.02.A i 1.02.B, w klatce 1, każde z powierzchnią zabudowy #153.50 [m2], powierzchnią wnętrza #98.13 [m2], tarasem #69.78 [m2] i solarium #100.97 [m2] z jacuzzi.',
  'To boliger med tre soverom, 1.02.A og 1.02.B, i oppgang 1, hver med #153.50 [m2] bebygd areal, #98.13 [m2] innvendig, en terrasse på #69.78 [m2] og en solterrasse på #100.97 [m2] med jacuzzi.',
  'Två bostäder med tre sovrum, 1.02.A och 1.02.B, i uppgång 1, var och en med #153.50 [m2] byggyta, #98.13 [m2] inomhus, en terrass på #69.78 [m2] och en solterrass på #100.97 [m2] med jacuzzi.')
p('.residences.items[0].points[1]',
  'Los dos planos muestran las mismas estancias y superficies, en espejo. Los precios son €995000 para 1.02.B y €1090000 para 1.02.A.',
  'Les deux plans montrent les mêmes pièces et les mêmes surfaces, en miroir. Les prix sont de €1090000 pour 1.02.A et de €995000 pour 1.02.B.',
  'Die beiden Pläne zeigen dieselben Räume und Flächen, spiegelverkehrt. Die Preise betragen €1090000 für 1.02.A und €995000 für 1.02.B.',
  'На двух планах одни и те же помещения и площади в зеркальном отражении. Цены: €1090000 за 1.02.A и €995000 за 1.02.B.',
  'يُظهر المخططان الغرف والمساحات نفسها بشكل معكوس. الأسعار €1090000 للمسكن 1.02.A و€995000 للمسكن 1.02.B.',
  'De twee plattegronden tonen dezelfde ruimtes en oppervlakten, gespiegeld. De prijzen zijn €1090000 voor 1.02.A en €995000 voor 1.02.B.',
  'Oba rzuty pokazują te same pomieszczenia i powierzchnie w odbiciu lustrzanym. Ceny to €1090000 za 1.02.A i €995000 za 1.02.B.',
  'De to plantegningene viser de samme rommene og arealene, speilvendt. Prisene er €1090000 for 1.02.A og €995000 for 1.02.B.',
  'De två planritningarna visar samma rum och ytor, spegelvända. Priserna är €1090000 för 1.02.A och €995000 för 1.02.B.')
p('.residences.items[1].name', 'Una vivienda de planta baja con jardín', 'Un logement de rez-de-chaussée avec jardin', 'Eine Erdgeschosswohnung mit Garten',
  'Квартира на первом этаже с садом', 'مسكن أرضي بحديقة', 'Een woning op de begane grond met tuin', 'Mieszkanie na parterze z ogrodem',
  'En bolig i første etasje med hage', 'En bostad på bottenvåningen med trädgård')
p('.residences.items[1].points[0]',
  'La vivienda 2.00.D, en el portal 2, tiene dos dormitorios, una terraza cubierta de #57.16 [m2] y un jardín de #13.75 [m2], con #113.46 [m2] interiores y #160.07 [m2] construidos según el plano. El precio es €645000.',
  'Le logement 2.00.D, dans la cage 2, compte deux chambres, une terrasse couverte de #57.16 [m2] et un jardin de #13.75 [m2], avec #113.46 [m2] intérieurs et #160.07 [m2] construits selon le plan. Le prix est de €645000.',
  'Die Wohnung 2.00.D in Aufgang 2 hat zwei Schlafzimmer, eine überdachte Terrasse von #57.16 [m2] und einen Garten von #13.75 [m2], mit laut Plan #113.46 [m2] Innenfläche und #160.07 [m2] bebauter Fläche. Der Preis beträgt €645000.',
  'Квартира 2.00.D в подъезде 2 имеет две спальни, крытую террасу #57.16 [m2] и сад #13.75 [m2], по плану внутренняя площадь #113.46 [m2], застроенная #160.07 [m2]. Цена — €645000.',
  'للمسكن 2.00.D في المدخل 2 غرفتا نوم وتراس مغطى بمساحة #57.16 [m2] وحديقة بمساحة #13.75 [m2]، مع #113.46 [m2] داخلية و#160.07 [m2] مبنية بحسب المخطط. السعر €645000.',
  'Woning 2.00.D in portiek 2 heeft twee slaapkamers, een overdekt terras van #57.16 [m2] en een tuin van #13.75 [m2], met volgens de plattegrond #113.46 [m2] binnen en #160.07 [m2] bebouwd. De prijs is €645000.',
  'Mieszkanie 2.00.D w klatce 2 ma dwie sypialnie, zadaszony taras #57.16 [m2] i ogród #13.75 [m2], a według rzutu powierzchnia wnętrza to #113.46 [m2], a zabudowy #160.07 [m2]. Cena wynosi €645000.',
  'Bolig 2.00.D i oppgang 2 har to soverom, en overbygd terrasse på #57.16 [m2] og en hage på #13.75 [m2], med ifølge plantegningen #113.46 [m2] innvendig og #160.07 [m2] bebygd areal. Prisen er €645000.',
  'Bostad 2.00.D i uppgång 2 har två sovrum, en täckt terrass på #57.16 [m2] och en trädgård på #13.75 [m2], med enligt planritningen #113.46 [m2] inomhus och #160.07 [m2] byggyta. Priset är €645000.')
p('.residences.items[1].points[1]',
  'El plano muestra un trastero de #30.21 [m2] y un baño de #4.66 [m2] en la planta jardín inferior, y la superficie interior los cuenta: las estancias de la planta de vida suman #78.59 [m2].',
  'Le plan montre une cave de #30.21 [m2] et une salle de bains de #4.66 [m2] au niveau jardin inférieur, et la surface intérieure les comptabilise : les pièces du niveau de vie totalisent #78.59 [m2].',
  'Der Plan zeigt einen Abstellraum von #30.21 [m2] und ein Bad von #4.66 [m2] auf der darunterliegenden Gartenebene, und die Innenfläche rechnet sie mit: Die Räume der Wohnebene ergeben zusammen #78.59 [m2].',
  'На плане показаны кладовая #30.21 [m2] и санузел #4.66 [m2] на нижнем садовом уровне, и внутренняя площадь их включает: помещения жилого уровня в сумме дают #78.59 [m2].',
  'يُظهر المخطط غرفة تخزين بمساحة #30.21 [m2] وحماماً بمساحة #4.66 [m2] في مستوى الحديقة السفلي، وتحتسبهما المساحة الداخلية: تبلغ مجموع غرف مستوى المعيشة #78.59 [m2].',
  'De plattegrond toont een berging van #30.21 [m2] en een badkamer van #4.66 [m2] op het lagere tuinniveau, en de binnenoppervlakte telt ze mee: de ruimtes op het woonniveau tellen op tot #78.59 [m2].',
  'Rzut pokazuje komórkę lokatorską o powierzchni #30.21 [m2] i łazienkę #4.66 [m2] na niższym poziomie ogrodowym, a powierzchnia wnętrza je wlicza: pomieszczenia poziomu mieszkalnego dają razem #78.59 [m2].',
  'Plantegningen viser en bod på #30.21 [m2] og et bad på #4.66 [m2] på det nedre hagenivået, og det innvendige arealet teller dem med: rommene på oppholdsnivået utgjør til sammen #78.59 [m2].',
  'Planritningen visar ett förråd på #30.21 [m2] och ett badrum på #4.66 [m2] på det nedre trädgårdsplanet, och den invändiga ytan räknar med dem: rummen på bostadsplanet blir tillsammans #78.59 [m2].')
p('.residences.items[1].points[2]',
  'La lista de disponibilidad da #114.18 [m2] construidos para esta vivienda, cifra que no coincide con ninguna del plano.',
  'La liste de disponibilité donne #114.18 [m2] construits pour ce logement, un chiffre qui ne correspond à aucun de ceux du plan.',
  'Die Verfügbarkeitsliste nennt für diese Wohnung #114.18 [m2] bebaute Fläche, eine Zahl, die mit keiner Angabe im Plan übereinstimmt.',
  'В списке наличия для этой квартиры указана застроенная площадь #114.18 [m2], которая не совпадает ни с одной цифрой на плане.',
  'تذكر قائمة التوفر #114.18 [m2] مبنية لهذا المسكن، وهو رقم لا يطابق أياً من أرقام المخطط.',
  'De beschikbaarheidslijst geeft #114.18 [m2] bebouwd voor deze woning, wat met geen van beide cijfers op de plattegrond overeenkomt.',
  'Lista dostępności podaje dla tego mieszkania powierzchnię zabudowy #114.18 [m2], która nie zgadza się z żadną wartością na rzucie.',
  'Tilgjengelighetslisten oppgir #114.18 [m2] bebygd areal for denne boligen, noe som ikke stemmer med noen av tallene på plantegningen.',
  'Tillgänglighetslistan anger #114.18 [m2] byggyta för denna bostad, vilket inte stämmer med någon av siffrorna på planritningen.')
p('.residences.items[2].name', 'Una vivienda a nivel de jardín con una terraza muy grande', 'Un logement de plain-pied avec le jardin et une très grande terrasse',
  'Eine Wohnung auf Gartenebene mit einer sehr großen Terrasse', 'Квартира на уровне сада с очень большой террасой',
  'مسكن في مستوى الحديقة بتراس كبير جداً', 'Een woning op tuinniveau met een heel groot terras', 'Mieszkanie na poziomie ogrodu z bardzo dużym tarasem',
  'En bolig på hagenivå med en veldig stor terrasse', 'En bostad på trädgårdsplan med en mycket stor terrass')
p('.residences.items[2].points[0]',
  'La vivienda 1.S01.A, en el portal 1, tiene dos dormitorios, terrazas de #227.06 [m2] (#173.83 descubiertas, #36.20 bajo una pérgola y #17.03 cubiertas) y un jardín de #29.66 [m2], por €750000.',
  'Le logement 1.S01.A, dans la cage 1, compte deux chambres, des terrasses de #227.06 [m2] (#173.83 découvertes, #36.20 sous une pergola et #17.03 couvertes) et un jardin de #29.66 [m2], au prix de €750000.',
  'Die Wohnung 1.S01.A in Aufgang 1 hat zwei Schlafzimmer, Terrassen von #227.06 [m2] (#173.83 unüberdacht, #36.20 unter einer Pergola und #17.03 überdacht) und einen Garten von #29.66 [m2], zum Preis von €750000.',
  'Квартира 1.S01.A в подъезде 1 имеет две спальни, террасы #227.06 [m2] (#173.83 открытых, #36.20 под перголой и #17.03 крытых) и сад #29.66 [m2], цена — €750000.',
  'للمسكن 1.S01.A في المدخل 1 غرفتا نوم وتراسات بمساحة #227.06 [m2] (#173.83 مكشوفة و#36.20 تحت برجولة و#17.03 مغطاة) وحديقة بمساحة #29.66 [m2]، بسعر €750000.',
  'Woning 1.S01.A in portiek 1 heeft twee slaapkamers, terrassen van #227.06 [m2] (#173.83 open, #36.20 onder een pergola en #17.03 overdekt) en een tuin van #29.66 [m2], voor €750000.',
  'Mieszkanie 1.S01.A w klatce 1 ma dwie sypialnie, tarasy o łącznej powierzchni #227.06 [m2] (#173.83 odkrytych, #36.20 pod pergolą i #17.03 zadaszonych) oraz ogród #29.66 [m2], za €750000.',
  'Bolig 1.S01.A i oppgang 1 har to soverom, terrasser på #227.06 [m2] (#173.83 åpne, #36.20 under en pergola og #17.03 overbygde) og en hage på #29.66 [m2], til €750000.',
  'Bostad 1.S01.A i uppgång 1 har två sovrum, terrasser på #227.06 [m2] (#173.83 öppna, #36.20 under en pergola och #17.03 täckta) och en trädgård på #29.66 [m2], för €750000.')
p('.residences.items[2].points[1]',
  'El plano muestra un trastero de #33.00 [m2] con un baño de #3.29 [m2] en el sótano, y la cifra interior de #115.51 [m2] los cuenta: las estancias de la planta jardín suman #79.22 [m2]. El plano da #161.34 [m2] construidos.',
  'Le plan montre une cave de #33.00 [m2] avec une salle de bains de #3.29 [m2] au sous-sol, et la surface intérieure de #115.51 [m2] les comptabilise : les pièces du niveau jardin totalisent #79.22 [m2]. Le plan donne #161.34 [m2] construits.',
  'Der Plan zeigt im Untergeschoss einen Abstellraum von #33.00 [m2] mit einem Bad von #3.29 [m2], und die Innenfläche von #115.51 [m2] rechnet sie mit: Die Räume der Gartenebene ergeben zusammen #79.22 [m2]. Der Plan nennt #161.34 [m2] bebaute Fläche.',
  'На плане в подвале показаны кладовая #33.00 [m2] и санузел #3.29 [m2], и внутренняя площадь #115.51 [m2] их включает: помещения садового уровня в сумме дают #79.22 [m2]. По плану застроенная площадь — #161.34 [m2].',
  'يُظهر المخطط غرفة تخزين بمساحة #33.00 [m2] مع حمام بمساحة #3.29 [m2] في الطابق السفلي، وتحتسبهما المساحة الداخلية البالغة #115.51 [m2]: تبلغ مجموع غرف مستوى الحديقة #79.22 [m2]. ويذكر المخطط #161.34 [m2] مبنية.',
  'De plattegrond toont in de kelder een berging van #33.00 [m2] met een badkamer van #3.29 [m2], en de binnenoppervlakte van #115.51 [m2] telt ze mee: de ruimtes op tuinniveau tellen op tot #79.22 [m2]. De plattegrond geeft #161.34 [m2] bebouwd.',
  'Rzut pokazuje w piwnicy komórkę lokatorską #33.00 [m2] z łazienką #3.29 [m2], a powierzchnia wnętrza #115.51 [m2] je wlicza: pomieszczenia na poziomie ogrodu dają razem #79.22 [m2]. Rzut podaje powierzchnię zabudowy #161.34 [m2].',
  'Plantegningen viser en bod på #33.00 [m2] med et bad på #3.29 [m2] i kjelleren, og det innvendige arealet på #115.51 [m2] teller dem med: rommene på hagenivået utgjør til sammen #79.22 [m2]. Plantegningen oppgir #161.34 [m2] bebygd areal.',
  'Planritningen visar ett förråd på #33.00 [m2] med ett badrum på #3.29 [m2] i källaren, och den invändiga ytan på #115.51 [m2] räknar med dem: rummen på trädgårdsplanet blir tillsammans #79.22 [m2]. Planritningen anger #161.34 [m2] byggyta.')
p('.residences.items[2].points[2]',
  'La lista de disponibilidad da #115.27 [m2] construidos para esta vivienda, cifra que no coincide con ninguna del plano.',
  'La liste de disponibilité donne #115.27 [m2] construits pour ce logement, un chiffre qui ne correspond à aucun de ceux du plan.',
  'Die Verfügbarkeitsliste nennt für diese Wohnung #115.27 [m2] bebaute Fläche, eine Zahl, die mit keiner Angabe im Plan übereinstimmt.',
  'В списке наличия для этой квартиры указана застроенная площадь #115.27 [m2], которая не совпадает ни с одной цифрой на плане.',
  'تذكر قائمة التوفر #115.27 [m2] مبنية لهذا المسكن، وهو رقم لا يطابق أياً من أرقام المخطط.',
  'De beschikbaarheidslijst geeft #115.27 [m2] bebouwd voor deze woning, wat met geen van beide cijfers op de plattegrond overeenkomt.',
  'Lista dostępności podaje dla tego mieszkania powierzchnię zabudowy #115.27 [m2], która nie zgadza się z żadną wartością na rzucie.',
  'Tilgjengelighetslisten oppgir #115.27 [m2] bebygd areal for denne boligen, noe som ikke stemmer med noen av tallene på plantegningen.',
  'Tillgänglighetslistan anger #115.27 [m2] byggyta för denna bostad, vilket inte stämmer med någon av siffrorna på planritningen.')
p('.residences.items[3].name', 'Una vivienda de primera planta con terraza', 'Un logement au premier étage avec terrasse', 'Eine Wohnung im ersten Obergeschoss mit Terrasse',
  'Квартира на втором этаже с террасой', 'مسكن في الطابق الأول بتراس', 'Een woning op de eerste verdieping met terras',
  'Mieszkanie na pierwszym piętrze z tarasem', 'En bolig i andre etasje med terrasse', 'En bostad på första våningen med terrass')
p('.residences.items[3].points[0]',
  'La vivienda 2.01.A, en el portal 2, tiene dos dormitorios, #81.45 [m2] interiores, #114.96 [m2] construidos y una terraza de #61.97 [m2], de los cuales #27.73 [m2] cubiertos, por €599000.',
  'Le logement 2.01.A, dans la cage 2, compte deux chambres, #81.45 [m2] intérieurs, #114.96 [m2] construits et une terrasse de #61.97 [m2], dont #27.73 [m2] couverts, au prix de €599000.',
  'Die Wohnung 2.01.A in Aufgang 2 hat zwei Schlafzimmer, #81.45 [m2] Innenfläche, #114.96 [m2] bebaute Fläche und eine Terrasse von #61.97 [m2], davon #27.73 [m2] überdacht, zum Preis von €599000.',
  'Квартира 2.01.A в подъезде 2 имеет две спальни, внутреннюю площадь #81.45 [m2], застроенную #114.96 [m2] и террасу #61.97 [m2], из которых #27.73 [m2] крытые, цена — €599000.',
  'للمسكن 2.01.A في المدخل 2 غرفتا نوم و#81.45 [m2] داخلية و#114.96 [m2] مبنية وتراس بمساحة #61.97 [m2] منها #27.73 [m2] مغطاة، بسعر €599000.',
  'Woning 2.01.A in portiek 2 heeft twee slaapkamers, #81.45 [m2] binnen, #114.96 [m2] bebouwd en een terras van #61.97 [m2], waarvan #27.73 [m2] overdekt, voor €599000.',
  'Mieszkanie 2.01.A w klatce 2 ma dwie sypialnie, powierzchnię wnętrza #81.45 [m2], powierzchnię zabudowy #114.96 [m2] i taras #61.97 [m2], z czego #27.73 [m2] zadaszone, za €599000.',
  'Bolig 2.01.A i oppgang 2 har to soverom, #81.45 [m2] innvendig, #114.96 [m2] bebygd areal og en terrasse på #61.97 [m2], hvorav #27.73 [m2] overbygd, til €599000.',
  'Bostad 2.01.A i uppgång 2 har två sovrum, #81.45 [m2] inomhus, #114.96 [m2] byggyta och en terrass på #61.97 [m2], varav #27.73 [m2] täckt, för €599000.')
p('.residences.items[3].points[1]',
  'El plano muestra un lavadero. La lista de disponibilidad y el plano coinciden en la superficie construida.',
  'Le plan montre une buanderie. La liste de disponibilité et le plan concordent sur la surface construite.',
  'Der Plan zeigt einen Hauswirtschaftsraum. Die Verfügbarkeitsliste und der Plan stimmen bei der bebauten Fläche überein.',
  'На плане показана постирочная. Список наличия и план совпадают по застроенной площади.',
  'يُظهر المخطط غرفة غسيل. وتتفق قائمة التوفر والمخطط في المساحة المبنية.',
  'De plattegrond toont een washok. De beschikbaarheidslijst en de plattegrond komen overeen in de bebouwde oppervlakte.',
  'Rzut pokazuje pomieszczenie gospodarcze z pralnią. Lista dostępności i rzut zgadzają się co do powierzchni zabudowy.',
  'Plantegningen viser et vaskerom. Tilgjengelighetslisten og plantegningen stemmer overens om bebygd areal.',
  'Planritningen visar ett tvättrum. Tillgänglighetslistan och planritningen stämmer överens om byggytan.')

# lifestyle
p('.lifestyle.headlineHtml', 'Una piscina, <em>un gimnasio</em> y vistas al mar', 'Une piscine, <em>une salle de sport</em> et la vue sur la mer',
  'Ein Pool, <em>ein Fitnessraum</em> und Meerblick', 'Бассейн, <em>тренажёрный зал</em> и вид на море',
  'مسبح <em>وصالة رياضية</em> وإطلالات على البحر', 'Een zwembad, <em>een fitnessruimte</em> en zeezicht',
  'Basen, <em>siłownia</em> i widok na morze', 'Et basseng, <em>et treningsrom</em> og sjøutsikt', 'En pool, <em>ett gym</em> och havsutsikt')
p('.lifestyle.copy',
  'La ficha informativa enumera una piscina exterior, un gimnasio y vistas panorámicas al mar; las imágenes y los planos muestran más.',
  'La fiche d’information mentionne une piscine extérieure, une salle de sport et une vue panoramique sur la mer ; les images et les plans en montrent davantage.',
  'Das Infoblatt führt einen Außenpool, einen Fitnessraum und Panorama-Meerblick auf; die Bilder und die Pläne zeigen mehr.',
  'В информационном листе указаны открытый бассейн, тренажёрный зал и панорамный вид на море; изображения и планы показывают больше.',
  'تذكر النشرة التعريفية مسبحاً خارجياً وصالة رياضية وإطلالات بانورامية على البحر؛ وتُظهر الصور والمخططات أكثر من ذلك.',
  'Het infoblad noemt een buitenzwembad, een fitnessruimte en panoramisch zeezicht; de beelden en de plattegronden tonen meer.',
  'Karta informacyjna wymienia basen zewnętrzny, siłownię i panoramiczny widok na morze; wizualizacje i rzuty pokazują więcej.',
  'Infoarket nevner et utendørsbasseng, et treningsrom og panoramautsikt over havet; bildene og plantegningene viser mer.',
  'Infobladet nämner en utomhuspool, ett gym och panoramautsikt över havet; bilderna och planritningarna visar mer.')
p('.lifestyle.panels[0][1]',
  'Una piscina exterior, como la enumera la ficha informativa. En las imágenes es una piscina alargada con tumbonas junto a un césped, con otra más pequeña a su lado y un pequeño pabellón con la cubierta ajardinada.',
  'Une piscine extérieure, comme la cite la fiche d’information. Sur les images, c’est un long bassin avec des bains de soleil à côté d’une pelouse, une plus petite piscine à ses côtés et un petit pavillon à toit végétalisé.',
  'Ein Außenpool, wie ihn das Infoblatt aufführt. Auf den Bildern ist es ein langer Pool mit Sonnenliegen neben einem Rasen, daneben ein kleinerer Pool und ein kleiner Pavillon mit bepflanztem Dach.',
  'Открытый бассейн, как он указан в информационном листе. На изображениях это длинный бассейн с шезлонгами рядом с газоном, рядом с ним второй, меньший бассейн и небольшой павильон с озеленённой крышей.',
  'مسبح خارجي، كما تذكره النشرة التعريفية. وفي الصور هو مسبح طويل مع كراسي استلقاء بجانب مرج، وبجواره مسبح أصغر وجناح صغير بسقف مزروع.',
  'Een buitenzwembad, zoals het infoblad het vermeldt. Op de beelden is het een lang zwembad met ligbedden naast een gazon, met een kleiner zwembad ernaast en een klein paviljoen met een beplant dak.',
  'Basen zewnętrzny, jak podaje karta informacyjna. Na wizualizacjach jest to długi basen z leżakami obok trawnika, z mniejszym basenem obok i niewielkim pawilonem z obsadzonym roślinnością dachem.',
  'Et utendørsbasseng, slik infoarket oppgir det. På bildene er det et langt basseng med solsenger ved siden av en plen, med et mindre basseng ved siden av og en liten paviljong med beplantet tak.',
  'En utomhuspool, som infobladet anger den. På bilderna är det en lång pool med solstolar bredvid en gräsmatta, med en mindre pool intill och en liten paviljong med planterat tak.')
p('.lifestyle.panels[1][1]',
  'Un gimnasio, como lo enumera la ficha informativa. Los documentos no dan su tamaño ni su equipamiento, y las imágenes no lo muestran.',
  'Une salle de sport, comme la cite la fiche d’information. Les documents n’en donnent ni la taille ni l’équipement, et les images ne la montrent pas.',
  'Ein Fitnessraum, wie ihn das Infoblatt aufführt. Die Unterlagen nennen weder Größe noch Ausstattung, und die Bilder zeigen ihn nicht.',
  'Тренажёрный зал, как он указан в информационном листе. В документах нет ни его размера, ни оснащения, и на изображениях его нет.',
  'صالة رياضية، كما تذكرها النشرة التعريفية. لا تذكر الوثائق حجمها ولا تجهيزاتها، ولا تُظهرها الصور.',
  'Een fitnessruimte, zoals het infoblad die vermeldt. De documenten geven geen grootte of uitrusting, en de beelden tonen haar niet.',
  'Siłownia, jak podaje karta informacyjna. Dokumenty nie podają jej wielkości ani wyposażenia, a wizualizacje jej nie pokazują.',
  'Et treningsrom, slik infoarket oppgir det. Dokumentene oppgir verken størrelse eller utstyr, og bildene viser det ikke.',
  'Ett gym, som infobladet anger det. Dokumenten anger varken storlek eller utrustning, och bilderna visar det inte.')
p('.lifestyle.panels[2][1]',
  'En las imágenes, cada nivel tiene una terraza profunda con barandilla de cristal y vistas hacia el mar. En los planos, las terrazas de las cinco viviendas a la venta van de #57.16 a #227.06 [m2].',
  'Sur les images, chaque niveau a une terrasse profonde avec un garde-corps en verre et une vue vers la mer. Sur les plans, les terrasses des cinq logements annoncés vont de #57.16 à #227.06 [m2].',
  'Auf den Bildern hat jede Ebene eine tiefe Terrasse mit Glasbrüstung und Blick Richtung Meer. Auf den Plänen reichen die Terrassen der fünf gelisteten Wohnungen von #57.16 bis #227.06 [m2].',
  'На изображениях на каждом уровне глубокая терраса со стеклянным ограждением и видом в сторону моря. По планам террасы пяти квартир из списка — от #57.16 до #227.06 [m2].',
  'في الصور، لكل مستوى تراس عميق بحاجز زجاجي وإطلالة نحو البحر. وفي المخططات تتراوح تراسات المساكن الخمسة المدرجة بين #57.16 و#227.06 [m2].',
  'Op de beelden heeft elk niveau een diep terras met een glazen balustrade en uitzicht richting zee. Op de plattegronden lopen de terrassen van de vijf woningen op de lijst van #57.16 tot #227.06 [m2].',
  'Na wizualizacjach każdy poziom ma głęboki taras ze szklaną balustradą i widokiem w stronę morza. Według rzutów tarasy pięciu lokali z listy mają od #57.16 do #227.06 [m2].',
  'På bildene har hvert nivå en dyp terrasse med glassrekkverk og utsikt mot havet. På plantegningene varierer terrassene til de fem oppførte boligene fra #57.16 til #227.06 [m2].',
  'På bilderna har varje plan en djup terrass med glasräcke och utsikt mot havet. På planritningarna varierar terrasserna för de fem listade bostäderna från #57.16 till #227.06 [m2].')
p('.lifestyle.panels[3][0]', 'El solárium de los áticos', 'Le solarium des penthouses', 'Das Solarium der Penthäuser', 'Солярий пентхаусов',
  'سولاريوم البنتهاوس', 'Het solarium van de penthouses', 'Solarium penthouse’ów', 'Solterrassen i toppleilighetene', 'Takvåningarnas solterrass')
p('.lifestyle.panels[3][1]',
  'Cada uno de los dos áticos a la venta tiene un solárium de #100.97 [m2] sobre la vivienda, con un jacuzzi, una zona de pérgola de #13.91 [m2] y una terraza descubierta de #87.06 [m2], a la que se sube por la escalera que muestra el plano.',
  'Chacun des deux penthouses annoncés a un solarium de #100.97 [m2] au-dessus du logement, avec un jacuzzi, une zone de pergola de #13.91 [m2] et une terrasse découverte de #87.06 [m2], desservi par l’escalier que montre le plan.',
  'Jedes der beiden gelisteten Penthäuser hat über der Wohnung ein Solarium von #100.97 [m2] mit einem Whirlpool, einem Pergolabereich von #13.91 [m2] und einer offenen Terrasse von #87.06 [m2], erreichbar über die im Plan gezeigte Treppe.',
  'У каждого из двух пентхаусов из списка над квартирой есть солярий #100.97 [m2] с джакузи, зоной перголы #13.91 [m2] и открытой террасой #87.06 [m2], на который ведёт лестница, показанная на плане.',
  'لكل من البنتهاوسين المدرجين سولاريوم بمساحة #100.97 [m2] فوق المسكن، مع جاكوزي ومنطقة برجولة بمساحة #13.91 [m2] وتراس مكشوف بمساحة #87.06 [m2]، يُصعد إليه بالدرج المبين في المخطط.',
  'Elk van de twee penthouses op de lijst heeft boven de woning een solarium van #100.97 [m2], met een jacuzzi, een pergolagedeelte van #13.91 [m2] en een open terras van #87.06 [m2], bereikbaar via de trap die op de plattegrond staat.',
  'Każdy z dwóch penthouse’ów z listy ma nad mieszkaniem solarium o powierzchni #100.97 [m2], z jacuzzi, strefą pod pergolą #13.91 [m2] i odkrytym tarasem #87.06 [m2], na które prowadzą schody pokazane na rzucie.',
  'Hver av de to oppførte toppleilighetene har en solterrasse på #100.97 [m2] over boligen, med en jacuzzi, et pergolaområde på #13.91 [m2] og en åpen terrasse på #87.06 [m2], nådd via trappen som plantegningen viser.',
  'Var och en av de två listade takvåningarna har en solterrass på #100.97 [m2] ovanför bostaden, med en jacuzzi, en pergolayta på #13.91 [m2] och en öppen terrass på #87.06 [m2], som nås via trappan som planritningen visar.')

# location
p('.location.headlineHtml', 'Estepona, <em>cerca de la playa</em>', 'Estepona, <em>près de la plage</em>', 'Estepona, <em>in Strandnähe</em>',
  'Эстепона, <em>рядом с пляжем</em>', 'إستيبونا، <em>بالقرب من الشاطئ</em>', 'Estepona, <em>dicht bij het strand</em>',
  'Estepona, <em>blisko plaży</em>', 'Estepona, <em>nær stranden</em>', 'Estepona, <em>nära stranden</em>')
p('.location.copy',
  'La promoción está en Estepona. La ficha informativa del promotor la sitúa a 500 metros de la playa y de los servicios locales, y da vistas panorámicas al mar. Los planos dan dos direcciones y ningún documento da una coordenada que se indique como la de la parcela, por lo que el mapa muestra la zona de Estepona. La ficha no da otras distancias.',
  'Le programme se trouve à Estepona. La fiche d’information du promoteur le situe à 500 mètres de la plage et des commerces locaux et mentionne une vue panoramique sur la mer. Les plans donnent deux adresses et aucun document ne donne de coordonnée présentée comme celle de la parcelle ; la carte montre donc la zone d’Estepona. La fiche ne donne aucune autre distance.',
  'Die Anlage liegt in Estepona. Das Infoblatt des Bauträgers nennt sie 500 Meter vom Strand und von den örtlichen Einrichtungen entfernt und führt Panorama-Meerblick auf. Die Pläne geben zwei Straßenadressen an, und keine Unterlage nennt eine Koordinate, die als die des Grundstücks bezeichnet wird, daher zeigt die Karte die Gegend von Estepona. Weitere Entfernungen nennt das Infoblatt nicht.',
  'Комплекс находится в Эстепоне. В информационном листе застройщика он расположен в 500 метрах от пляжа и местной инфраструктуры, указан панорамный вид на море. На планах два адреса, а ни в одном документе нет координат, которые названы координатами участка, поэтому на карте показан район Эстепоны. Других расстояний лист не даёт.',
  'يقع المشروع في إستيبونا. تضعه نشرة المطوّر التعريفية على بعد 500 متر من الشاطئ والمرافق المحلية وتذكر إطلالات بانورامية على البحر. وتذكر المخططات عنوانين للشارع، ولا تذكر أي وثيقة إحداثياً يُنص على أنه إحداثي القطعة، لذلك تعرض الخريطة منطقة إستيبونا. ولا تذكر النشرة مسافات أخرى.',
  'Het project ligt in Estepona. Het infoblad van de ontwikkelaar plaatst het op 500 meter van het strand en de lokale voorzieningen en vermeldt panoramisch zeezicht. De plattegronden geven twee straatadressen en geen enkel document geeft een coördinaat dat als dat van het perceel wordt aangeduid, dus toont de kaart de omgeving van Estepona. Andere afstanden geeft het infoblad niet.',
  'Inwestycja znajduje się w Esteponie. Karta informacyjna dewelopera umieszcza ją 500 metrów od plaży i lokalnych usług i podaje panoramiczny widok na morze. Rzuty podają dwa adresy ulic i żaden dokument nie podaje współrzędnej wskazanej jako współrzędna działki, dlatego mapa pokazuje okolice Estepony. Karta nie podaje innych odległości.',
  'Anlegget ligger i Estepona. Utbyggerens infoark plasserer det 500 meter fra stranden og de lokale tilbudene og oppgir panoramautsikt over havet. Plantegningene oppgir to gateadresser, og ingen dokumenter oppgir en koordinat som er angitt som tomtens, så kartet viser Estepona-området. Infoarket oppgir ingen andre avstander.',
  'Anläggningen ligger i Estepona. Exploatörens infoblad placerar den 500 meter från stranden och den lokala servicen och anger panoramautsikt över havet. Planritningarna anger två gatuadresser och inget dokument anger en koordinat som uppges vara tomtens, så kartan visar Estepona-området. Infobladet anger inga andra avstånd.')
p('.location.distances[0][0]', 'Playa y servicios locales', 'Plage et commerces locaux', 'Strand und örtliche Einrichtungen', 'Пляж и местная инфраструктура',
  'الشاطئ والمرافق المحلية', 'Strand en lokale voorzieningen', 'Plaża i lokalne usługi', 'Stranden og lokale tilbud', 'Stranden och den lokala servicen')
p('.location.distances[0][1]', 'Aprox. 500 metros', 'Env. 500 mètres', 'Ca. 500 Meter', 'Около 500 метров', 'نحو 500 متر', 'Ca. 500 meter',
  'Ok. 500 metrów', 'Ca. 500 meter', 'Ca 500 meter')

# investment
p('.investment.cards[0][0]', 'Reserva y calendario de pagos', 'Réservation et échéancier de paiement', 'Reservierung und Zahlungsplan',
  'Бронирование и график платежей', 'الحجز وجدول الدفعات', 'Reservering en betalingsschema', 'Rezerwacja i harmonogram płatności',
  'Reservasjon og betalingsplan', 'Reservation och betalningsplan')
p('.investment.cards[0][1]',
  'El promotor fija en su ficha informativa una reserva y un plan de pagos escalonado. Le enviamos por escrito los importes y las fechas vigentes antes de que reserve.',
  'Le promoteur fixe dans sa fiche d’information une réservation et un plan de paiement échelonné. Nous vous envoyons par écrit les montants et les dates en vigueur avant que vous ne réserviez.',
  'Der Bauträger legt in seinem Infoblatt eine Reservierung und einen gestaffelten Zahlungsplan fest. Wir senden Ihnen die aktuellen Beträge und Termine schriftlich zu, bevor Sie reservieren.',
  'Застройщик устанавливает в информационном листе бронирование и поэтапный план платежей. Перед бронированием мы письменно направим вам действующие суммы и сроки.',
  'يحدد المطوّر في نشرته التعريفية مبلغ حجز وخطة دفعات مرحلية. نرسل لكم كتابةً المبالغ والتواريخ السارية قبل أن تحجزوا.',
  'De ontwikkelaar legt in zijn infoblad een reservering en een gefaseerd betalingsplan vast. Wij sturen u de actuele bedragen en data schriftelijk toe voordat u reserveert.',
  'Deweloper określa w karcie informacyjnej rezerwację i etapowy plan płatności. Przed rezerwacją przesyłamy Państwu na piśmie aktualne kwoty i terminy.',
  'Utbyggeren fastsetter i infoarket en reservasjon og en trinnvis betalingsplan. Vi sender dere de gjeldende beløpene og datoene skriftlig før dere reserverer.',
  'Exploatören fastställer i infobladet en reservation och en stegvis betalningsplan. Vi skickar er de gällande beloppen och datumen skriftligen innan ni reserverar.')
p('.investment.cards[1][1]',
  'La lista de disponibilidad da los precios netos del promotor y la ficha informativa añade el IVA a cada pago, por lo que entendemos que los precios no incluyen IVA. No se indica el tipo, así que lo confirmamos por escrito, junto con los demás gastos de compra.',
  'La liste de disponibilité donne les prix nets du promoteur et la fiche d’information ajoute la TVA à chaque versement ; nous lisons donc les prix hors TVA. Le taux n’est pas indiqué, et nous le confirmons par écrit, ainsi que les autres frais d’achat.',
  'Die Verfügbarkeitsliste nennt die Nettopreise des Bauträgers, und das Infoblatt schlägt die MwSt. auf jede Rate auf, daher verstehen wir die Preise zuzüglich MwSt. Der Satz ist nicht angegeben, deshalb bestätigen wir ihn und die übrigen Kaufnebenkosten schriftlich.',
  'В списке наличия указаны чистые цены застройщика, а в информационном листе НДС добавляется к каждому платежу, поэтому мы считаем цены не включающими НДС. Ставка не указана, и мы письменно подтверждаем её и остальные расходы на покупку.',
  'تذكر قائمة التوفر الأسعار الصافية للمطوّر وتضيف النشرة التعريفية ضريبة القيمة المضافة إلى كل دفعة، لذلك نفهم أن الأسعار لا تشملها. ولا تُذكر النسبة، فنؤكدها كتابةً مع باقي مصاريف الشراء.',
  'De beschikbaarheidslijst geeft de nettoprijzen van de ontwikkelaar en het infoblad telt btw bij elke termijn op, dus lezen wij de prijzen als exclusief btw. Het tarief is niet vermeld, dus bevestigen wij dat en de overige aankoopkosten schriftelijk.',
  'Lista dostępności podaje ceny netto dewelopera, a karta informacyjna dodaje VAT do każdej raty, dlatego odczytujemy ceny jako niezawierające VAT. Stawka nie jest podana, więc potwierdzamy ją i pozostałe koszty zakupu na piśmie.',
  'Tilgjengelighetslisten oppgir utbyggerens nettopriser, og infoarket legger mva. til hver delbetaling, så vi leser prisene som eksklusive mva. Satsen er ikke oppgitt, så vi bekrefter den og de øvrige kjøpskostnadene skriftlig.',
  'Tillgänglighetslistan anger exploatörens nettopriser och infobladet lägger IVA på varje delbetalning, så vi läser priserna som exklusive IVA. Satsen anges inte, så vi bekräftar den och de övriga köpkostnaderna skriftligen.')
p('.investment.cards[2][1]',
  'Los planos de 1.S01.A y 2.00.D muestran un trastero en la planta inferior, y la memoria de calidades da una cocina equipada con electrodomésticos. Ningún documento dice si cada vivienda incluye una plaza de garaje, ni que el mobiliario de las imágenes esté incluido.',
  'Les plans de 1.S01.A et 2.00.D montrent une cave au niveau inférieur, et le descriptif de qualité donne une cuisine équipée avec électroménager. Aucun document ne dit si une place de garage est incluse avec chaque logement, ni que le mobilier des images est inclus.',
  'Die Pläne von 1.S01.A und 2.00.D zeigen einen Abstellraum auf der darunterliegenden Ebene, und die Bau- und Ausstattungsbeschreibung nennt eine Küche mit Geräten. Keine Unterlage sagt, ob zu jeder Wohnung ein Garagenstellplatz gehört oder ob die Möbel auf den Bildern enthalten sind.',
  'На планах 1.S01.A и 2.00.D показана кладовая на нижнем уровне, а в спецификации качества указана кухня с бытовой техникой. Ни в одном документе не сказано, входит ли в каждую квартиру место в гараже и включена ли мебель с изображений.',
  'يُظهر مخططا 1.S01.A و2.00.D غرفة تخزين في المستوى السفلي، وتذكر مواصفات الجودة مطبخاً مجهزاً بالأجهزة. ولا تقول أي وثيقة إن كان لكل مسكن موقف في المرآب، أو إن كان أثاث الصور مشمولاً.',
  'De plattegronden van 1.S01.A en 2.00.D tonen een berging op het lagere niveau, en de kwaliteitsspecificatie geeft een keuken met apparatuur. Geen enkel document zegt of bij elke woning een garageplaats hoort, of dat het meubilair op de beelden is inbegrepen.',
  'Rzuty 1.S01.A i 2.00.D pokazują komórkę lokatorską na niższym poziomie, a specyfikacja jakości podaje kuchnię ze sprzętem. Żaden dokument nie mówi, czy do każdego mieszkania należy miejsce garażowe ani czy meble z wizualizacji są wliczone.',
  'Plantegningene til 1.S01.A og 2.00.D viser en bod på nivået under, og kvalitetsspesifikasjonen oppgir et kjøkken med hvitevarer. Ingen dokumenter sier om en garasjeplass følger med hver bolig, eller om møblene på bildene er inkludert.',
  'Planritningarna för 1.S01.A och 2.00.D visar ett förråd på planet under, och kvalitetsspecifikationen anger ett kök med vitvaror. Inget dokument säger om en garageplats ingår i varje bostad eller om möblerna på bilderna ingår.')
p('.investment.cards[3][1]',
  'La memoria de calidades se encuentra en fase de desarrollo y puede cambiar por razones técnicas sin reducir la calidad ni el diseño del resultado. Pedimos la memoria definitiva.',
  'Le descriptif de qualité est à un stade de développement et peut changer pour des raisons techniques sans réduire la qualité ni le design du résultat. Nous demandons le descriptif définitif.',
  'Die Bau- und Ausstattungsbeschreibung befindet sich im Entwicklungsstadium und kann sich aus technischen Gründen ändern, ohne Qualität oder Design des Ergebnisses zu mindern. Wir fordern die endgültige Beschreibung an.',
  'Спецификация качества находится на стадии разработки и может меняться по техническим причинам без снижения качества и дизайна результата. Мы запрашиваем окончательную спецификацию.',
  'مواصفات الجودة في مرحلة التطوير وقد تتغير لأسباب فنية دون خفض جودة النتيجة أو تصميمها. نطلب المواصفات النهائية.',
  'De kwaliteitsspecificatie bevindt zich in de ontwikkelingsfase en kan om technische redenen wijzigen zonder de kwaliteit of het ontwerp van het resultaat te verminderen. Wij vragen de definitieve specificatie op.',
  'Specyfikacja jakości jest na etapie opracowania i może się zmienić z przyczyn technicznych bez obniżenia jakości i projektu efektu końcowego. Prosimy o ostateczną specyfikację.',
  'Kvalitetsspesifikasjonen er på utviklingsstadiet og kan endres av tekniske grunner uten at kvaliteten eller designet på resultatet reduseres. Vi ber om den endelige spesifikasjonen.',
  'Kvalitetsspecifikationen är på utvecklingsstadiet och kan ändras av tekniska skäl utan att kvaliteten eller designen på resultatet minskar. Vi ber om den slutliga specifikationen.')

# trust dossier
p('.trustDossier.cards[0][1]',
  'La ficha informativa da una licencia de obras con fecha 18 de septiembre de 2024, obras iniciadas en el tercer trimestre de 2024 y la licencia de primera ocupación en blanco. Pedimos la licencia y el aval bancario que cubre las cantidades entregadas a cuenta.',
  'La fiche d’information donne un permis de construire daté du 18 septembre 2024, des travaux commencés au troisième trimestre 2024 et le permis de première occupation laissé vide. Nous demandons le permis et la garantie bancaire qui couvre les sommes versées en acompte.',
  'Das Infoblatt nennt eine Baugenehmigung vom 18. September 2024, Baubeginn im dritten Quartal 2024 und die Erstbezugsgenehmigung leer. Wir fordern die Genehmigung und die Bankgarantie an, die geleistete Anzahlungen absichert.',
  'В информационном листе указаны разрешение на строительство от 18 сентября 2024 года, начало работ в третьем квартале 2024 года и незаполненное разрешение на первое заселение. Мы запрашиваем разрешение и банковскую гарантию, покрывающую суммы, внесённые в качестве аванса.',
  'تذكر النشرة التعريفية رخصة بناء مؤرخة في 18 سبتمبر 2024 وبدء الأعمال في الربع الثالث من 2024 وتترك رخصة أول إشغال فارغة. نطلب الرخصة والضمان المصرفي الذي يغطي المبالغ المدفوعة على الحساب.',
  'Het infoblad geeft een bouwvergunning van 18 september 2024, werken gestart in het derde kwartaal van 2024 en de vergunning voor eerste ingebruikname leeg. We vragen om de vergunning en om de bankgarantie die de vooruitbetaalde bedragen dekt.',
  'Karta informacyjna podaje pozwolenie na budowę z 18 września 2024 r., rozpoczęcie prac w trzecim kwartale 2024 r. i puste pozwolenie na użytkowanie. Prosimy o pozwolenie i gwarancję bankową, która zabezpiecza wpłacone zaliczki.',
  'Infoarket oppgir en byggetillatelse datert 18. september 2024, byggestart i tredje kvartal 2024 og en tom ferdigattest. Vi ber om tillatelsen og om bankgarantien som dekker beløp betalt på forhånd.',
  'Infobladet anger ett bygglov daterat den 18 september 2024, byggstart under tredje kvartalet 2024 och ett tomt slutbevis. Vi ber om bygglovet och om bankgarantin som täcker belopp som betalats i förskott.')
p('.trustDossier.cards[1][1]',
  'La ficha informativa estima el fin de obra para el primer trimestre de 2027 y no lleva fecha. Preguntamos hasta dónde ha llegado la obra y por la fecha contractual, y ponemos ambas por escrito.',
  'La fiche d’information estime la fin des travaux au premier trimestre 2027 et ne porte aucune date. Nous demandons où en est le chantier et la date contractuelle, et nous mettons les deux par écrit.',
  'Das Infoblatt schätzt das Bauende auf das erste Quartal 2027 und trägt kein Datum. Wir fragen, wie weit der Bau ist und nach dem vertraglichen Termin, und halten beides schriftlich fest.',
  'В информационном листе окончание строительства оценено на первый квартал 2027 года, дата на листе не указана. Мы уточняем, как далеко продвинулось строительство, и договорную дату и фиксируем оба ответа письменно.',
  'تقدّر النشرة التعريفية انتهاء البناء في الربع الأول من 2027 ولا تحمل تاريخاً. نسأل أين وصل البناء وعن التاريخ التعاقدي ونثبّت الجوابين كتابةً.',
  'Het infoblad schat het einde van de bouw op het eerste kwartaal van 2027 en draagt geen datum. We vragen hoe ver de bouw is en naar de contractuele datum, en leggen beide schriftelijk vast.',
  'Karta informacyjna szacuje zakończenie budowy na pierwszy kwartał 2027 r. i nie nosi daty. Pytamy, jak daleko jest budowa, i o termin umowny, a obie odpowiedzi potwierdzamy na piśmie.',
  'Infoarket anslår byggeslutt til første kvartal 2027 og har ingen dato. Vi spør hvor langt byggingen er kommet og om den kontraktsfestede datoen, og får begge deler skriftlig.',
  'Infobladet beräknar byggslut till första kvartalet 2027 och saknar datum. Vi frågar hur långt bygget har kommit och om det avtalade datumet och får båda skriftligen.')
p('.trustDossier.cards[2][1]',
  'La lista de disponibilidad y los planos coinciden en la superficie construida de 1.02.A, 1.02.B y 2.01.A, pero no en la de 1.S01.A, que figura con #115.27 [m2] frente a #161.34 [m2] construidos y #115.51 [m2] interiores en el plano, ni en la de 2.00.D, con #114.18 [m2] frente a #160.07 [m2] construidos y #113.46 [m2] interiores. Los planos dan además superficies útiles según el Decreto 218/2005, por ejemplo #107.94 [m2] para 1.02.A y 1.02.B frente a #98.13 [m2]. Confirmamos qué cifras usa el contrato.',
  'La liste de disponibilité et les plans concordent sur la surface construite de 1.02.A, 1.02.B et 2.01.A, mais pas sur celle de 1.S01.A, annoncée à #115.27 [m2] contre #161.34 [m2] construits et #115.51 [m2] intérieurs sur le plan, ni sur celle de 2.00.D, à #114.18 [m2] contre #160.07 [m2] construits et #113.46 [m2] intérieurs. Les plans donnent aussi des surfaces utiles selon le décret 218/2005, par exemple #107.94 [m2] pour 1.02.A et 1.02.B contre #98.13 [m2]. Nous confirmons quels chiffres le contrat retient.',
  'Die Verfügbarkeitsliste und die Pläne stimmen bei der bebauten Fläche von 1.02.A, 1.02.B und 2.01.A überein, nicht aber bei 1.S01.A, die mit #115.27 [m2] gelistet ist gegenüber #161.34 [m2] bebauter Fläche und #115.51 [m2] Innenfläche im Plan, und nicht bei 2.00.D, mit #114.18 [m2] gegenüber #160.07 [m2] bebauter Fläche und #113.46 [m2] Innenfläche. Die Pläne geben außerdem Nutzflächen nach dem Dekret 218/2005 an, zum Beispiel #107.94 [m2] für 1.02.A und 1.02.B gegenüber #98.13 [m2]. Wir bestätigen, welche Zahlen der Vertrag verwendet.',
  'Список наличия и планы совпадают по застроенной площади 1.02.A, 1.02.B и 2.01.A, но не по 1.S01.A, указанной как #115.27 [m2] против #161.34 [m2] застроенной и #115.51 [m2] внутренней площади на плане, и не по 2.00.D: #114.18 [m2] против #160.07 [m2] застроенной и #113.46 [m2] внутренней. Кроме того, планы дают полезные площади по декрету 218/2005, например #107.94 [m2] для 1.02.A и 1.02.B против #98.13 [m2]. Мы уточняем, какие цифры использует договор.',
  'تتفق قائمة التوفر والمخططات في المساحة المبنية للمساكن 1.02.A و1.02.B و2.01.A، لكنها تختلف في 1.S01.A المدرج بمساحة #115.27 [m2] مقابل #161.34 [m2] مبنية و#115.51 [m2] داخلية في المخطط، وفي 2.00.D بمساحة #114.18 [m2] مقابل #160.07 [m2] مبنية و#113.46 [m2] داخلية. وتذكر المخططات أيضاً مساحات مفيدة بحسب المرسوم 218/2005، مثل #107.94 [m2] للمسكنين 1.02.A و1.02.B مقابل #98.13 [m2]. نؤكد أي الأرقام يعتمدها العقد.',
  'De beschikbaarheidslijst en de plattegronden komen overeen in de bebouwde oppervlakte van 1.02.A, 1.02.B en 2.01.A, maar niet bij 1.S01.A, vermeld met #115.27 [m2] tegenover #161.34 [m2] bebouwd en #115.51 [m2] binnen op de plattegrond, noch bij 2.00.D, met #114.18 [m2] tegenover #160.07 [m2] bebouwd en #113.46 [m2] binnen. De plattegronden geven ook nuttige oppervlakten volgens decreet 218/2005, bijvoorbeeld #107.94 [m2] voor 1.02.A en 1.02.B tegenover #98.13 [m2]. Wij bevestigen welke cijfers het contract hanteert.',
  'Lista dostępności i rzuty zgadzają się co do powierzchni zabudowy 1.02.A, 1.02.B i 2.01.A, ale nie w przypadku 1.S01.A, podanego jako #115.27 [m2] wobec #161.34 [m2] zabudowy i #115.51 [m2] wnętrza na rzucie, ani 2.00.D: #114.18 [m2] wobec #160.07 [m2] zabudowy i #113.46 [m2] wnętrza. Rzuty podają też powierzchnie użytkowe według dekretu 218/2005, na przykład #107.94 [m2] dla 1.02.A i 1.02.B wobec #98.13 [m2]. Potwierdzamy, jakich wartości używa umowa.',
  'Tilgjengelighetslisten og plantegningene stemmer overens om bebygd areal for 1.02.A, 1.02.B og 2.01.A, men ikke for 1.S01.A, oppført med #115.27 [m2] mot #161.34 [m2] bebygd og #115.51 [m2] innvendig på plantegningen, eller for 2.00.D, med #114.18 [m2] mot #160.07 [m2] bebygd og #113.46 [m2] innvendig. Plantegningene oppgir også bruksarealer etter dekret 218/2005, for eksempel #107.94 [m2] for 1.02.A og 1.02.B mot #98.13 [m2]. Vi bekrefter hvilke tall kontrakten bruker.',
  'Tillgänglighetslistan och planritningarna stämmer överens om byggytan för 1.02.A, 1.02.B och 2.01.A, men inte för 1.S01.A, som anges med #115.27 [m2] mot #161.34 [m2] byggyta och #115.51 [m2] inomhus på planritningen, eller för 2.00.D, med #114.18 [m2] mot #160.07 [m2] byggyta och #113.46 [m2] inomhus. Planritningarna anger även nyttjandeytor enligt dekret 218/2005, till exempel #107.94 [m2] för 1.02.A och 1.02.B mot #98.13 [m2]. Vi bekräftar vilka siffror avtalet använder.')
p('.trustDossier.cards[3][0]', 'Dirección y precios', 'Adresse et prix', 'Adresse und Preise', 'Адрес и цены', 'العنوان والأسعار', 'Adres en prijzen', 'Adres i ceny',
  'Adresse og priser', 'Adress och priser')
p('.trustDossier.cards[3][1]',
  'Los planos dan una dirección para los áticos y las viviendas del portal 2 y otra para 1.S01.A, aunque los áticos y 1.S01.A están ambos en el portal 1. Los dos planos de ático muestran las mismas superficies, pero la lista los precia con €95000 de diferencia. Preguntamos qué dirección es la registrada y qué explica la diferencia.',
  'Les plans donnent une adresse pour les penthouses et les logements de la cage 2 et une autre pour 1.S01.A, alors que les penthouses et 1.S01.A sont tous dans la cage 1. Les deux plans de penthouse montrent les mêmes surfaces, mais la liste les affiche à €95000 d’écart. Nous demandons quelle adresse est la bonne et ce qui explique l’écart.',
  'Die Pläne geben eine Adresse für die Penthäuser und die Wohnungen in Aufgang 2 und eine andere für 1.S01.A an, obwohl die Penthäuser und 1.S01.A beide in Aufgang 1 liegen. Die beiden Penthouse-Pläne zeigen dieselben Flächen, doch die Liste preist sie um €95000 verschieden. Wir fragen, welche Adresse die eingetragene ist und was den Unterschied erklärt.',
  'На планах указан один адрес для пентхаусов и квартир подъезда 2 и другой для 1.S01.A, хотя пентхаусы и 1.S01.A находятся в подъезде 1. Два плана пентхаусов показывают одинаковые площади, но в списке их цены различаются на €95000. Мы уточняем, какой адрес зарегистрирован и чем объясняется разница.',
  'تذكر المخططات عنواناً للبنتهاوس ومساكن المدخل 2 وعنواناً آخر للمسكن 1.S01.A، مع أن البنتهاوس و1.S01.A كليهما في المدخل 1. ويُظهر مخططا البنتهاوس المساحات نفسها، لكن القائمة تسعّرهما بفارق €95000. نسأل أي العنوانين هو المسجّل وما الذي يفسر الفارق.',
  'De plattegronden geven één adres voor de penthouses en de woningen in portiek 2 en een ander voor 1.S01.A, hoewel de penthouses en 1.S01.A allebei in portiek 1 liggen. De twee penthouse-plattegronden tonen dezelfde oppervlakten, maar de lijst prijst ze €95000 uit elkaar. We vragen welk adres is geregistreerd en wat het verschil verklaart.',
  'Rzuty podają jeden adres dla penthouse’ów i mieszkań w klatce 2 i inny dla 1.S01.A, choć penthouse’y i 1.S01.A są obie w klatce 1. Dwa rzuty penthouse’ów pokazują te same powierzchnie, ale lista wycenia je z różnicą €95000. Pytamy, który adres jest zarejestrowany i co wyjaśnia różnicę.',
  'Plantegningene oppgir én adresse for toppleilighetene og boligene i oppgang 2 og en annen for 1.S01.A, selv om toppleilighetene og 1.S01.A begge ligger i oppgang 1. De to plantegningene av toppleilighetene viser de samme arealene, men listen priser dem €95000 fra hverandre. Vi spør hvilken adresse som er den registrerte og hva som forklarer forskjellen.',
  'Planritningarna anger en adress för takvåningarna och bostäderna i uppgång 2 och en annan för 1.S01.A, trots att takvåningarna och 1.S01.A båda ligger i uppgång 1. De två planritningarna för takvåningarna visar samma ytor, men listan prissätter dem €95000 från varandra. Vi frågar vilken adress som är den registrerade och vad som förklarar skillnaden.')

# availability
p('.availability.headlineHtml', '5 de 24 viviendas <em>disponibles ahora</em>', '5 logements sur 24 <em>disponibles actuellement</em>',
  '5 von 24 Wohnungen <em>derzeit verfügbar</em>', '5 из 24 квартир <em>доступны сейчас</em>', '5 من 24 مسكناً <em>متاحة حالياً</em>',
  '5 van de 24 woningen <em>nu beschikbaar</em>', '5 z 24 mieszkań <em>dostępnych obecnie</em>', '5 av 24 boliger <em>ledige nå</em>',
  '5 av 24 bostäder <em>lediga just nu</em>')
p('.availability.copy',
  'Cinco viviendas figuran a la venta: dos áticos de tres dormitorios con solárium y jacuzzi, una vivienda de planta baja con jardín, una vivienda a nivel de jardín con una terraza muy grande y una vivienda de primera planta. La lista no dice nada de las otras 19. La disponibilidad y los precios son los de la lista del {D} y se confirman antes de cualquier reserva.',
  'Cinq logements sont annoncés : deux penthouses de trois chambres avec solarium et jacuzzi, un logement de rez-de-chaussée avec jardin, un logement de plain-pied avec le jardin et une très grande terrasse, et un logement au premier étage. La liste ne dit rien des 19 autres. La disponibilité et les prix sont ceux de la liste du {D} et sont confirmés avant toute réservation.',
  'Fünf Wohnungen sind gelistet: zwei Penthäuser mit drei Schlafzimmern, Solarium und Whirlpool, eine Erdgeschosswohnung mit Garten, eine Wohnung auf Gartenebene mit einer sehr großen Terrasse und eine Wohnung im ersten Obergeschoss. Zu den übrigen 19 sagt die Liste nichts. Verfügbarkeit und Preise entsprechen der Liste vom {D} und werden vor jeder Reservierung bestätigt.',
  'В списке пять квартир: два трёхспальных пентхауса с солярием и джакузи, квартира на первом этаже с садом, квартира на уровне сада с очень большой террасой и квартира на втором этаже. О других 19 список ничего не говорит. Наличие и цены — по списку от {D}, они подтверждаются перед любым бронированием.',
  'خمسة مساكن مدرجة: بنتهاوسان بثلاث غرف نوم مع سولاريوم وجاكوزي، ومسكن في الطابق الأرضي بحديقة، ومسكن في مستوى الحديقة بتراس كبير جداً، ومسكن في الطابق الأول. ولا تقول القائمة شيئاً عن المساكن التسعة عشر الأخرى. التوفر والأسعار هما ما في قائمة {D} ويُؤكَّدان قبل أي حجز.',
  'Vijf woningen staan op de lijst: twee penthouses met drie slaapkamers met solarium en jacuzzi, een woning op de begane grond met tuin, een woning op tuinniveau met een heel groot terras en een woning op de eerste verdieping. Over de andere 19 zegt de lijst niets. Beschikbaarheid en prijzen zijn die van de lijst van {D} en worden vóór elke reservering bevestigd.',
  'Na liście jest pięć lokali: dwa trzysypialniowe penthouse’y z solarium i jacuzzi, mieszkanie na parterze z ogrodem, mieszkanie na poziomie ogrodu z bardzo dużym tarasem i mieszkanie na pierwszym piętrze. O pozostałych 19 lista nic nie mówi. Dostępność i ceny pochodzą z listy z {D} i są potwierdzane przed jakąkolwiek rezerwacją.',
  'Fem boliger er oppført: to toppleiligheter med tre soverom, solterrasse og jacuzzi, en bolig i første etasje med hage, en bolig på hagenivå med en veldig stor terrasse og en bolig i andre etasje. Listen sier ingenting om de øvrige 19. Tilgjengelighet og priser er de fra listen av {D} og bekreftes før enhver reservasjon.',
  'Fem bostäder är listade: två takvåningar med tre sovrum, solterrass och jacuzzi, en bostad på bottenvåningen med trädgård, en bostad på trädgårdsplan med en mycket stor terrass och en bostad på första våningen. Listan säger ingenting om de övriga 19. Tillgänglighet och priser är de från listan den {D} och bekräftas före varje reservation.')
p('.availability.sourceNote',
  'Las referencias, los dormitorios y los precios están transcritos de la lista de disponibilidad que se nos facilitó, tal como figuraba el {D}, que muestra cinco de las 24 viviendas y no dice nada del resto. Las superficies interiores, las terrazas, los jardines y los solariums proceden de los planos del promotor, y la superficie construida es la cifra de los planos, que la encabezan como «vivienda + ZCC» sin explicar la abreviatura. Los precios son las cifras netas del promotor y la ficha informativa añade el IVA a sus pagos, por lo que entendemos que no incluyen IVA. Donde la lista difiere de los planos, en la superficie construida de 1.S01.A y 2.00.D, la tabla sigue los planos y ambas cifras se dan arriba.',
  'Les références, les chambres et les prix sont transcrits de la liste de disponibilité qui nous a été remise, telle qu’elle figurait le {D}, qui présente cinq des 24 logements et ne dit rien des autres. Les surfaces intérieures, terrasses, jardins et solariums proviennent des plans du promoteur, et la surface construite est le chiffre des plans, qui l’intitulent « vivienda + ZCC » sans expliquer l’abréviation. Les prix sont les chiffres nets du promoteur et la fiche d’information ajoute la TVA à ses versements ; nous les lisons donc hors TVA. Là où la liste diffère des plans, pour la surface construite de 1.S01.A et 2.00.D, le tableau suit les plans et les deux chiffres sont donnés plus haut.',
  'Referenzen, Schlafzimmer und Preise sind aus der uns vorliegenden Verfügbarkeitsliste übernommen, wie sie am {D} lautete; sie zeigt fünf der 24 Wohnungen und sagt nichts zu den übrigen. Die Innenflächen, Terrassen, Gärten und Solarien stammen aus den Plänen des Bauträgers, und die bebaute Fläche ist der Wert der Pläne, die ihn mit „vivienda + ZCC“ überschreiben, ohne die Abkürzung zu erklären. Die Preise sind die Nettowerte des Bauträgers, und das Infoblatt schlägt die MwSt. auf seine Raten auf, daher verstehen wir sie zuzüglich MwSt. Wo die Liste von den Plänen abweicht, bei der bebauten Fläche von 1.S01.A und 2.00.D, folgt die Tabelle den Plänen, und beide Werte sind oben angegeben.',
  'Референсы, спальни и цены перенесены из предоставленного нам списка наличия в том виде, как он был {D}: в нём пять из 24 квартир, об остальных он ничего не говорит. Внутренние площади, террасы, сады и солярии взяты из планов застройщика, а застроенная площадь — это цифра планов, которые озаглавливают её «vivienda + ZCC», не поясняя аббревиатуру. Цены — чистые цифры застройщика, а в информационном листе НДС добавляется к его платежам, поэтому мы считаем цены не включающими НДС. Там, где список расходится с планами, — по застроенной площади 1.S01.A и 2.00.D, — таблица следует планам, а обе цифры приведены выше.',
  'المراجع وغرف النوم والأسعار منقولة من قائمة التوفر التي وصلتنا كما كانت في {D}، وهي تعرض خمسة من 24 مسكناً ولا تقول شيئاً عن الباقي. المساحات الداخلية والتراسات والحدائق والسولاريوم مأخوذة من مخططات المطوّر، والمساحة المبنية هي رقم المخططات التي تعنونه «vivienda + ZCC» دون شرح الاختصار. الأسعار هي الأرقام الصافية للمطوّر وتضيف النشرة التعريفية ضريبة القيمة المضافة إلى دفعاتها، لذلك نفهم أنها لا تشملها. وحيث تختلف القائمة عن المخططات، في المساحة المبنية للمسكنين 1.S01.A و2.00.D، يتبع الجدول المخططات وتُذكر الرقمان أعلاه.',
  'De referenties, slaapkamers en prijzen zijn overgenomen uit de beschikbaarheidslijst die we hebben gekregen, zoals die op {D} luidde, met vijf van de 24 woningen en zonder iets over de rest. De binnenoppervlakten, terrassen, tuinen en solariums komen uit de plattegronden van de ontwikkelaar, en de bebouwde oppervlakte is het cijfer van de plattegronden, die het “vivienda + ZCC” noemen zonder de afkorting uit te leggen. De prijzen zijn de nettocijfers van de ontwikkelaar en het infoblad telt btw bij zijn termijnen op, dus lezen wij ze als exclusief btw. Waar de lijst afwijkt van de plattegronden, bij de bebouwde oppervlakte van 1.S01.A en 2.00.D, volgt de tabel de plattegronden en zijn beide cijfers hierboven vermeld.',
  'Odniesienia, sypialnie i ceny przepisano z otrzymanej przez nas listy dostępności w brzmieniu z {D}, która pokazuje pięć z 24 mieszkań i nic nie mówi o pozostałych. Powierzchnie wnętrz, tarasów, ogrodów i solariów pochodzą z rzutów dewelopera, a powierzchnia zabudowy to wartość z rzutów, które opisują ją jako „vivienda + ZCC”, nie wyjaśniając skrótu. Ceny to kwoty netto dewelopera, a karta informacyjna dodaje VAT do jego rat, dlatego odczytujemy je jako niezawierające VAT. Tam, gdzie lista różni się od rzutów, w powierzchni zabudowy 1.S01.A i 2.00.D, tabela podąża za rzutami, a obie wartości podano wyżej.',
  'Referansene, soverommene og prisene er hentet fra tilgjengelighetslisten vi fikk, slik den lød {D}, som viser fem av de 24 boligene og ikke sier noe om resten. De innvendige arealene, terrassene, hagene og solterrassene er hentet fra utbyggerens plantegninger, og bebygd areal er plantegningenes tall, som overskriver det «vivienda + ZCC» uten å forklare forkortelsen. Prisene er utbyggerens nettotall, og infoarket legger mva. til delbetalingene, så vi leser dem som eksklusive mva. Der listen avviker fra plantegningene, i bebygd areal for 1.S01.A og 2.00.D, følger tabellen plantegningene, og begge tallene er oppgitt over.',
  'Referenserna, sovrummen och priserna är hämtade från tillgänglighetslistan vi fick, som den löd den {D}, och som visar fem av de 24 bostäderna och inte säger något om resten. De invändiga ytorna, terrasserna, trädgårdarna och solterrasserna är hämtade från exploatörens planritningar, och byggytan är planritningarnas siffra, som rubricerar den «vivienda + ZCC» utan att förklara förkortningen. Priserna är exploatörens nettosiffror och infobladet lägger IVA på dess delbetalningar, så vi läser dem som exklusive IVA. Där listan avviker från planritningarna, i byggytan för 1.S01.A och 2.00.D, följer tabellen planritningarna och båda siffrorna anges ovan.')

# private viewing, enquiry
p('.privateViewing.insights[1][1]',
  'Caminamos con usted hasta la playa y las tiendas más cercanas y medimos el tiempo.',
  'Nous allons à pied avec vous jusqu’à la plage et aux commerces les plus proches et chronométrons le trajet.',
  'Wir gehen mit Ihnen zum Strand und zu den nächsten Geschäften und stoppen die Zeit.',
  'Мы идём с вами пешком до пляжа и ближайших магазинов и засекаем время.',
  'نمشي معكم إلى الشاطئ وأقرب المتاجر ونحسب الوقت.',
  'We lopen met u naar het strand en de dichtstbijzijnde winkels en meten de tijd.',
  'Idziemy z Państwem pieszo na plażę i do najbliższych sklepów i mierzymy czas.',
  'Vi går med dere til stranden og de nærmeste butikkene og tar tiden.',
  'Vi går med er till stranden och de närmaste butikerna och tar tiden.')
p('.enquiry.headlineHtml', 'Pregunte por <em>Absolute Estepona</em>', 'Renseignez-vous sur <em>Absolute Estepona</em>', 'Fragen Sie nach <em>Absolute Estepona</em>',
  'Спросите об <em>Absolute Estepona</em>', 'اسأل عن <em>Absolute Estepona</em>', 'Vraag naar <em>Absolute Estepona</em>', 'Zapytaj o <em>Absolute Estepona</em>',
  'Spør om <em>Absolute Estepona</em>', 'Fråga om <em>Absolute Estepona</em>')
p('.enquiry.message', 'Hola Nueva Living, quisiera información sobre Absolute Estepona.', 'Bonjour Nueva Living, je souhaiterais des informations sur Absolute Estepona.',
  'Hallo Nueva Living, ich hätte gern Informationen zu Absolute Estepona.', 'Здравствуйте, Nueva Living, прошу прислать информацию о Absolute Estepona.',
  'مرحباً Nueva Living، أودّ الحصول على معلومات عن Absolute Estepona.', 'Hallo Nueva Living, ik wil graag informatie over Absolute Estepona.',
  'Dzień dobry, Nueva Living, proszę o informacje o Absolute Estepona.', 'Hei Nueva Living, jeg vil gjerne ha informasjon om Absolute Estepona.',
  'Hej Nueva Living, jag vill gärna ha information om Absolute Estepona.')

# faq
p('.faq[0][1]',
  'La promoción tiene 24 viviendas y cinco figuran con precio: tres de dos dormitorios y dos áticos de tres dormitorios, de €599000 a €1090000 más IVA.',
  'Le programme compte 24 logements et cinq sont annoncés avec un prix : trois de deux chambres et deux penthouses de trois chambres, de €599000 à €1090000 plus TVA.',
  'Die Anlage hat 24 Wohnungen, und fünf sind mit Preis gelistet: drei mit zwei Schlafzimmern und zwei Penthäuser mit drei Schlafzimmern, von €599000 bis €1090000 plus MwSt.',
  'В комплексе 24 квартиры, пять указаны с ценой: три двухспальные и два трёхспальных пентхауса, от €599000 до €1090000 плюс НДС.',
  'يضم المشروع 24 مسكناً وخمسة منها مدرجة بأسعارها: ثلاثة بغرفتي نوم وبنتهاوسان بثلاث غرف نوم، من €599000 إلى €1090000 زائد ضريبة القيمة المضافة.',
  'Het project heeft 24 woningen en vijf staan met prijs op de lijst: drie met twee slaapkamers en twee penthouses met drie slaapkamers, van €599000 tot €1090000 plus btw.',
  'Inwestycja ma 24 mieszkania, a pięć jest podanych z ceną: trzy z dwiema sypialniami i dwa trzysypialniowe penthouse’y, od €599000 do €1090000 plus VAT.',
  'Anlegget har 24 boliger, og fem er oppført med pris: tre med to soverom og to toppleiligheter med tre soverom, fra €599000 til €1090000 pluss mva.',
  'Anläggningen har 24 bostäder och fem är listade med pris: tre med två sovrum och två takvåningar med tre sovrum, från €599000 till €1090000 plus IVA.')
p('.faq[1][1]',
  'No. La lista da los precios netos del promotor y la ficha informativa añade el IVA a cada pago. No se indica el tipo, así que lo confirmamos por escrito, junto con los demás gastos de compra.',
  'Non. La liste donne les prix nets du promoteur et la fiche d’information ajoute la TVA à chaque versement. Le taux n’est pas indiqué ; nous le confirmons donc par écrit, ainsi que les autres frais d’achat.',
  'Nein. Die Liste nennt die Nettopreise des Bauträgers, und das Infoblatt schlägt die MwSt. auf jede Rate auf. Der Satz ist nicht angegeben, daher bestätigen wir ihn und die übrigen Kaufnebenkosten schriftlich.',
  'Нет. В списке указаны чистые цены застройщика, а в информационном листе НДС добавляется к каждому платежу. Ставка не указана, поэтому мы письменно подтверждаем её и остальные расходы на покупку.',
  'لا. تذكر القائمة الأسعار الصافية للمطوّر وتضيف النشرة التعريفية ضريبة القيمة المضافة إلى كل دفعة. ولا تُذكر النسبة، لذلك نؤكدها كتابةً مع باقي مصاريف الشراء.',
  'Nee. De lijst geeft de nettoprijzen van de ontwikkelaar en het infoblad telt btw bij elke termijn op. Het tarief is niet vermeld, dus bevestigen wij dat en de overige aankoopkosten schriftelijk.',
  'Nie. Lista podaje ceny netto dewelopera, a karta informacyjna dodaje VAT do każdej raty. Stawka nie jest podana, dlatego potwierdzamy ją i pozostałe koszty zakupu na piśmie.',
  'Nei. Listen oppgir utbyggerens nettopriser, og infoarket legger mva. til hver delbetaling. Satsen er ikke oppgitt, så vi bekrefter den og de øvrige kjøpskostnadene skriftlig.',
  'Nej. Listan anger exploatörens nettopriser och infobladet lägger IVA på varje delbetalning. Satsen anges inte, så vi bekräftar den och de övriga köpkostnaderna skriftligen.')
p('.faq[2][1]',
  'Los planos de 1.S01.A y 2.00.D muestran un trastero en la planta inferior. Ningún documento dice si cada vivienda incluye una plaza de garaje, y lo confirmamos.',
  'Les plans de 1.S01.A et 2.00.D montrent une cave au niveau inférieur. Aucun document ne dit si une place de garage est incluse avec chaque logement, et nous le confirmons.',
  'Die Pläne von 1.S01.A und 2.00.D zeigen einen Abstellraum auf der darunterliegenden Ebene. Keine Unterlage sagt, ob zu jeder Wohnung ein Garagenstellplatz gehört, und wir bestätigen das.',
  'На планах 1.S01.A и 2.00.D показана кладовая на нижнем уровне. Ни в одном документе не сказано, входит ли в каждую квартиру место в гараже, — мы это подтверждаем.',
  'يُظهر مخططا 1.S01.A و2.00.D غرفة تخزين في المستوى السفلي. ولا تقول أي وثيقة إن كان لكل مسكن موقف في المرآب، ونحن نؤكد ذلك.',
  'De plattegronden van 1.S01.A en 2.00.D tonen een berging op het lagere niveau. Geen enkel document zegt of bij elke woning een garageplaats hoort, en dat bevestigen wij.',
  'Rzuty 1.S01.A i 2.00.D pokazują komórkę lokatorską na niższym poziomie. Żaden dokument nie mówi, czy do każdego mieszkania należy miejsce garażowe, i to potwierdzamy.',
  'Plantegningene til 1.S01.A og 2.00.D viser en bod på nivået under. Ingen dokumenter sier om en garasjeplass følger med hver bolig, og vi bekrefter det.',
  'Planritningarna för 1.S01.A och 2.00.D visar ett förråd på planet under. Inget dokument säger om en garageplats ingår i varje bostad, och vi bekräftar det.')
p('.faq[3][1]',
  'La ficha informativa da las obras como iniciadas en el tercer trimestre de 2024 y el fin de obra estimado para el primer trimestre de 2027. No lleva fecha, por lo que preguntamos hasta dónde ha llegado la obra y por la fecha contractual.',
  'La fiche d’information donne les travaux comme commencés au troisième trimestre 2024 et la fin des travaux estimée au premier trimestre 2027. Elle ne porte aucune date ; nous demandons donc où en est le chantier et la date contractuelle.',
  'Das Infoblatt nennt den Baubeginn im dritten Quartal 2024 und das Bauende, geschätzt für das erste Quartal 2027. Es trägt kein Datum, daher fragen wir, wie weit der Bau ist, und nach dem vertraglichen Termin.',
  'В информационном листе работы указаны как начавшиеся в третьем квартале 2024 года, окончание строительства — ориентировочно в первом квартале 2027 года. Дата на листе не указана, поэтому мы уточняем, как далеко продвинулось строительство, и договорную дату.',
  'تذكر النشرة التعريفية أن الأعمال بدأت في الربع الثالث من 2024 ويُقدَّر انتهاء البناء في الربع الأول من 2027. وهي لا تحمل تاريخاً، لذلك نسأل أين وصل البناء وعن التاريخ التعاقدي.',
  'Het infoblad geeft de werken als gestart in het derde kwartaal van 2024 en het einde van de bouw geschat op het eerste kwartaal van 2027. Het draagt geen datum, dus vragen we hoe ver de bouw is en naar de contractuele datum.',
  'Karta informacyjna podaje prace jako rozpoczęte w trzecim kwartale 2024 r. i zakończenie budowy szacowane na pierwszy kwartał 2027 r. Nie nosi daty, dlatego pytamy, jak daleko jest budowa, i o termin umowny.',
  'Infoarket oppgir at arbeidene startet i tredje kvartal 2024 og byggeslutt anslått til første kvartal 2027. Det har ingen dato, så vi spør hvor langt byggingen er kommet og om den kontraktsfestede datoen.',
  'Infobladet anger att arbetena påbörjades under tredje kvartalet 2024 och byggslut beräknat till första kvartalet 2027. Det saknar datum, så vi frågar hur långt bygget har kommit och om det avtalade datumet.')
p('.faq[4][1]',
  'El promotor fija una reserva y un plan de pagos escalonado. Le enviamos por escrito los importes y las fechas vigentes antes de que reserve.',
  'Le promoteur fixe une réservation et un plan de paiement échelonné. Nous vous envoyons par écrit les montants et les dates en vigueur avant que vous ne réserviez.',
  'Der Bauträger legt eine Reservierung und einen gestaffelten Zahlungsplan fest. Wir senden Ihnen die aktuellen Beträge und Termine schriftlich zu, bevor Sie reservieren.',
  'Застройщик устанавливает бронирование и поэтапный план платежей. Перед бронированием мы письменно направим вам действующие суммы и сроки.',
  'يحدد المطوّر مبلغ حجز وخطة دفعات مرحلية. نرسل لكم كتابةً المبالغ والتواريخ السارية قبل أن تحجزوا.',
  'De ontwikkelaar legt een reservering en een gefaseerd betalingsplan vast. Wij sturen u de actuele bedragen en data schriftelijk toe voordat u reserveert.',
  'Deweloper określa rezerwację i etapowy plan płatności. Przed rezerwacją przesyłamy Państwu na piśmie aktualne kwoty i terminy.',
  'Utbyggeren fastsetter en reservasjon og en trinnvis betalingsplan. Vi sender dere de gjeldende beløpene og datoene skriftlig før dere reserverer.',
  'Exploatören fastställer en reservation och en stegvis betalningsplan. Vi skickar er de gällande beloppen och datumen skriftligen innan ni reserverar.')

# seo
p('.seo.title',
  'Absolute Estepona - Apartamentos y áticos en Estepona', 'Absolute Estepona - Appartements et penthouses à Estepona',
  'Absolute Estepona - Wohnungen & Penthäuser in Estepona', 'Absolute Estepona - апартаменты и пентхаусы в Эстепоне',
  'Absolute Estepona - شقق وبنتهاوس في إستيبونا', 'Absolute Estepona - Appartementen & penthouses in Estepona',
  'Absolute Estepona - Apartamenty i penthouse’y w Esteponie', 'Absolute Estepona - Leiligheter og toppleiligheter i Estepona',
  'Absolute Estepona - Lägenheter och takvåningar i Estepona')
p('.seo.h1',
  'Absolute Estepona: apartamentos y áticos con vistas al mar en Estepona', 'Absolute Estepona : appartements et penthouses avec vue sur la mer à Estepona',
  'Absolute Estepona: Wohnungen & Penthäuser mit Meerblick in Estepona', 'Absolute Estepona: апартаменты и пентхаусы с видом на море в Эстепоне',
  'Absolute Estepona: شقق وبنتهاوس بإطلالات على البحر في إستيبونا', 'Absolute Estepona: appartementen & penthouses met zeezicht in Estepona',
  'Absolute Estepona: apartamenty i penthouse’y z widokiem na morze w Esteponie', 'Absolute Estepona: leiligheter og toppleiligheter med sjøutsikt i Estepona',
  'Absolute Estepona: lägenheter och takvåningar med havsutsikt i Estepona')
p('.seo.h1Context',
  'Apartamentos y áticos con vistas al mar en Estepona', 'Appartements et penthouses avec vue sur la mer à Estepona',
  'Wohnungen & Penthäuser mit Meerblick in Estepona', 'Апартаменты и пентхаусы с видом на море в Эстепоне',
  'شقق وبنتهاوس بإطلالات على البحر في إستيبونا', 'Appartementen & penthouses met zeezicht in Estepona',
  'Apartamenty i penthouse’y z widokiem na morze w Esteponie', 'Leiligheter og toppleiligheter med sjøutsikt i Estepona',
  'Lägenheter och takvåningar med havsutsikt i Estepona')

# ---- finish ---------------------------------------------------------------------------------
missing = [pth for pth in BY_PATH if pth not in USED]
if missing:
    for pth in missing:
        print('NOT COVERED', pth, '|', BY_PATH[pth][:90])
json.dump(T, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries,', len(missing), 'paths not covered')
