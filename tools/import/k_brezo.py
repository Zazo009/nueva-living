# -*- coding: utf-8 -*-
"""Brezo Residences, part 1 of 2: names, descriptions, images, overview, why, architecture, quality specification.

Same shape as k_brisamar.py. Entries are keyed by the first words of the English string, so they do not move when
the scaffold list changes order. Unit sizes, floorplan captions and the "+ VAT" price lines are templates. Tokens:
{E483500} = money, {N74.10} = a number in the locale's decimal mark, {U} = m2.
Run:  python3 tools/import/k_brezo.py <scratch dir>     (writes <scratch dir>/tr_a.json)
Part 2 is k_brezo_2.py and writes tr_b.json.
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {'es': 'm²', 'fr': 'm²', 'de': 'm²', 'ru': 'м²', 'ar': 'م²', 'nl': 'm²', 'pl': 'm²', 'no': 'm²', 'sv': 'm²'}
TAX = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة', 'nl': 'btw', 'pl': 'VAT', 'no': 'mva.', 'sv': 'moms'}
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


def find(hint):
    hits = [s for s in todo if s == hint] or [s for s in todo if s.startswith(hint)]
    assert len(hits) == 1, (hint, len(hits))
    return hits[0]


def a(hint, *tr):
    en = find(hint)
    assert len(tr) == 9, (hint, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---------------------------------------------------------------- templates
HOME = {'es': 'Vivienda', 'fr': 'Logement', 'de': 'Wohnung', 'ru': 'Квартира', 'ar': 'المسكن', 'nl': 'Woning',
        'pl': 'Lokal', 'no': 'Bolig', 'sv': 'Bostad'}
PLANOF = {'es': 'Plano de la vivienda', 'fr': 'Plan du logement', 'de': 'Grundriss der Wohnung', 'ru': 'Планировка квартиры',
          'ar': 'مخطط المسكن', 'nl': 'Plattegrond van woning', 'pl': 'Rzut lokalu', 'no': 'Plantegning av bolig',
          'sv': 'Planritning för bostad'}
COMMA = {l: (', ' if l != 'ar' else '، ') for l in LOCS}
LV = {
    'ground floor': ['planta baja', 'rez-de-chaussée', 'Erdgeschoss', 'первый этаж', 'الطابق الأرضي', 'begane grond', 'parter', 'første etasje', 'bottenvåning'],
    'second floor': ['segunda planta', 'deuxième étage', 'zweites Obergeschoss', 'третий этаж', 'الطابق الثاني', 'tweede verdieping', 'drugie piętro', 'tredje etasje', 'andra våningen'],
    'penthouse': ['ático', 'penthouse', 'Penthouse', 'пентхаус', 'بنتهاوس', 'penthouse', 'penthouse', 'toppleilighet', 'takvåning'],
}
FROM = {'es': 'Desde', 'fr': 'À partir de', 'de': 'Ab', 'ru': 'От', 'ar': 'ابتداءً من', 'nl': 'Vanaf', 'pl': 'Od', 'no': 'Fra', 'sv': 'Från'}
DASH = {l: ' - ' for l in LOCS}
DASH['pl'] = ' – '
# built, interior, terrace, garden: the wording the other apartment and villa projects use
SIZE = {
    'es': ('{b} {U} construidos', '{i} {U} interiores', '{t} {U} de terraza', '{x} {U} de jardín'),
    'fr': ('{b} {U} construits', '{i} {U} intérieurs', '{t} {U} de terrasse', '{x} {U} de jardin'),
    'de': ('{b} {U} bebaut', '{i} {U} Innenfläche', '{t} {U} Terrasse', '{x} {U} Garten'),
    'ru': ('{b} {U} застроенной площади', '{i} {U} внутри', 'терраса {t} {U}', 'сад {x} {U}'),
    'ar': ('{b} {U} مبنية', '{i} {U} داخلية', '{t} {U} تراس', '{x} {U} حديقة'),
    'nl': ('{b} {U} bebouwd', '{i} {U} binnen', '{t} {U} terras', '{x} {U} tuin'),
    'pl': ('{b} {U} zabudowy', '{i} {U} wnętrza', '{t} {U} tarasu', '{x} {U} ogrodu'),
    'no': ('{b} {U} bygd', '{i} {U} innvendig', '{t} {U} terrasse', '{x} {U} hage'),
    'sv': ('{b} {U} byggyta', '{i} {U} inomhus', '{t} {U} terrass', '{x} {U} trädgård'),
}
HOMES72 = {'es': '72 viviendas', 'fr': '72 logements', 'de': '72 Wohnungen', 'ru': '72 квартиры', 'ar': '72 مسكنًا',
           'nl': '72 woningen', 'pl': '72 lokale', 'no': '72 boliger', 'sv': '72 bostäder'}
for en in todo:
    m = re.fullmatch(r'From EUR ([\d,]+) \+ VAT', en)
    if m:
        T[en] = {l: f"{FROM[l]} {money(int(m.group(1).replace(',', '')), l)} + {TAX[l]}" for l in LOCS}
        continue
    m = re.fullmatch(r'EUR ([\d,]+) \+ VAT', en)
    if m:
        T[en] = {l: f"{money(int(m.group(1).replace(',', '')), l)} + {TAX[l]}" for l in LOCS}
        continue
    m = re.fullmatch(r'EUR ([\d,]+) - EUR ([\d,]+) \+ VAT', en)
    if m:
        T[en] = {l: f"{money(int(m.group(1).replace(',', '')), l)}{DASH[l]}{money(int(m.group(2).replace(',', '')), l)} + {TAX[l]}" for l in LOCS}
        continue
    if en == '72 homes':
        T[en] = dict(zip(LOCS, [HOMES72[l] for l in LOCS]))
        continue
    m = re.fullmatch(r'Floorplan of home (\d+), (ground floor|second floor|penthouse)', en)
    if m:
        T[en] = {l: f'{PLANOF[l]} {m.group(1)}{COMMA[l]}{LV[m.group(2)][i]}' for i, l in enumerate(LOCS)}
        continue
    m = re.fullmatch(r'Home (\d+), (ground floor|second floor|penthouse)', en)
    if m:
        T[en] = {l: f'{HOME[l]} {m.group(1)}{COMMA[l]}{LV[m.group(2)][i]}' for i, l in enumerate(LOCS)}
        continue
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm interior, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm garden)?', en)
    if m:
        out = {}
        for l in LOCS:
            b, i_, t, x = SIZE[l]
            parts = [b.format(b='{N%s}' % m.group(1), U='{U}'), i_.format(i='{N%s}' % m.group(2), U='{U}'),
                     t.format(t='{N%s}' % m.group(3), U='{U}')]
            if m.group(4):
                parts.append(x.format(x='{N%s}' % m.group(4), U='{U}'))
            out[l] = expand(COMMA[l].join(parts), l)
        T[en] = out

# ---------------------------------------------------------------- names, descriptions, card
for en in todo:
    if en in ('Brezo Residences', 'Brezo', 'Brezo <em>Residences</em>'):
        T[en] = {l: en for l in LOCS}
a('A gated complex of 72 homes with two',
  'Un conjunto cerrado de 72 viviendas de dos, tres o cuatro dormitorios en Cala de Mijas, a dos minutos a pie de la playa según el promotor, con piscina comunitaria, gimnasio y sala social. Cinco viviendas de dos y tres dormitorios figuran con precio, desde {E483500} más IVA.',
  'Un ensemble fermé de 72 logements de deux, trois ou quatre chambres à Cala de Mijas, à deux minutes à pied de la plage selon le promoteur, avec piscine commune, salle de sport et salle commune. Cinq logements de deux et trois chambres sont listés, à partir de {E483500} hors TVA.',
  'Eine geschlossene Anlage mit 72 Wohnungen mit zwei, drei oder vier Schlafzimmern in Cala de Mijas, nach Angabe des Bauträgers zwei Gehminuten vom Strand entfernt, mit Gemeinschaftspool, Fitnessraum und Gemeinschaftsraum. Fünf Wohnungen mit zwei und drei Schlafzimmern sind aufgeführt, ab {E483500} zuzüglich MwSt.',
  'Закрытый комплекс из 72 квартир с двумя, тремя или четырьмя спальнями в Кала-де-Михас, по данным застройщика, в двух минутах ходьбы от пляжа, с общим бассейном, тренажёрным залом и общей гостиной. В списке пять квартир с двумя и тремя спальнями, от {E483500} плюс НДС.',
  'مجمّع مغلق من 72 مسكنًا بغرفتي نوم أو ثلاث أو أربع غرف نوم في كالا دي ميهاس، على بُعد دقيقتين سيرًا من الشاطئ بحسب المطوّر، مع مسبح مشترك وصالة رياضية وقاعة اجتماعية. خمسة مساكن بغرفتي نوم وثلاث غرف نوم مدرجة بالأسعار، ابتداءً من {E483500} زائد ضريبة القيمة المضافة.',
  'Een besloten complex van 72 woningen met twee, drie of vier slaapkamers in Cala de Mijas, volgens de ontwikkelaar op twee minuten lopen van het strand, met gemeenschappelijk zwembad, fitnessruimte en gemeenschappelijke ruimte. Vijf woningen met twee en drie slaapkamers staan op de lijst, vanaf {E483500} plus btw.',
  'Zamknięty kompleks 72 lokali z dwiema, trzema lub czterema sypialniami w Cala de Mijas, według dewelopera dwie minuty spacerem od plaży, ze wspólnym basenem, siłownią i salą wspólną. Pięć lokali z dwiema i trzema sypialniami jest na liście, od {E483500} plus VAT.',
  'Et lukket anlegg med 72 boliger med to, tre eller fire soverom i Cala de Mijas, to minutter å gå fra stranden ifølge utbyggeren, med felles basseng, treningsrom og fellesrom. Fem boliger med to og tre soverom er oppført, fra {E483500} pluss mva.',
  'En bevakad anläggning med 72 bostäder med två, tre eller fyra sovrum i Cala de Mijas, enligt exploatören två minuters promenad från stranden, med gemensam pool, gym och gemensamhetsrum. Fem bostäder med två och tre sovrum är listade, från {E483500} plus moms.')
a('Five of 72 two- and three-bedroom homes listed',
  'Cinco de 72 viviendas de dos y tres dormitorios en Cala de Mijas, desde {E483500} más IVA: jardines en planta baja, terraza en el ático, piscina comunitaria, gimnasio, y aparcamiento y trastero incluidos.',
  'Cinq logements de deux et trois chambres sur 72 à Cala de Mijas, à partir de {E483500} hors TVA : jardins au rez-de-chaussée, terrasse sur le penthouse, piscine commune, salle de sport, stationnement et cave inclus.',
  'Fünf von 72 Wohnungen mit zwei und drei Schlafzimmern in Cala de Mijas ab {E483500} zuzüglich MwSt.: Gärten im Erdgeschoss, eine Penthouse-Terrasse, Gemeinschaftspool, Fitnessraum, Stellplatz und Abstellraum inklusive.',
  'Пять из 72 квартир с двумя и тремя спальнями в Кала-де-Михас, от {E483500} плюс НДС: сады на первом этаже, терраса пентхауса, общий бассейн, тренажёрный зал, парковка и кладовая включены.',
  'خمسة من 72 مسكنًا بغرفتي نوم وثلاث غرف نوم في كالا دي ميهاس، ابتداءً من {E483500} زائد ضريبة القيمة المضافة: حدائق في الطابق الأرضي، وتراس البنتهاوس، ومسبح مشترك، وصالة رياضية، والموقف والمخزن مشمولان.',
  'Vijf van de 72 woningen met twee en drie slaapkamers in Cala de Mijas, vanaf {E483500} plus btw: tuinen op de begane grond, een penthouseterras, gemeenschappelijk zwembad, fitnessruimte, parkeerplaats en berging inbegrepen.',
  'Pięć z 72 lokali z dwiema i trzema sypialniami w Cala de Mijas, od {E483500} plus VAT: ogrody na parterze, taras penthouse’u, wspólny basen, siłownia, miejsce postojowe i komórka w cenie.',
  'Fem av 72 boliger med to og tre soverom i Cala de Mijas, fra {E483500} pluss mva.: hager i første etasje, en toppleilighetsterrasse, felles basseng, treningsrom, parkeringsplass og bod inkludert.',
  'Fem av 72 bostäder med två och tre sovrum i Cala de Mijas, från {E483500} plus moms: trädgårdar på bottenvåningen, en takterrass, gemensam pool, gym, parkeringsplats och förråd ingår.')
a('Two- and three-bedroom apartments and a penthouse',
  'Apartamentos de dos y tres dormitorios y un ático en Cala de Mijas, cerca de la playa, desde {E483500} más IVA.',
  'Appartements de deux et trois chambres et un penthouse à Cala de Mijas, près de la plage, à partir de {E483500} hors TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern und ein Penthouse in Cala de Mijas, nahe am Strand, ab {E483500} zuzüglich MwSt.',
  'Апартаменты с двумя и тремя спальнями и пентхаус в Кала-де-Михас, недалеко от пляжа, от {E483500} плюс НДС.',
  'شقق بغرفتي نوم وثلاث غرف نوم وبنتهاوس في كالا دي ميهاس، قرب الشاطئ، ابتداءً من {E483500} زائد ضريبة القيمة المضافة.',
  'Appartementen met twee en drie slaapkamers en een penthouse in Cala de Mijas, dicht bij het strand, vanaf {E483500} plus btw.',
  'Apartamenty z dwiema i trzema sypialniami oraz penthouse w Cala de Mijas, blisko plaży, od {E483500} plus VAT.',
  'Leiligheter med to og tre soverom og en toppleilighet i Cala de Mijas, nær stranden, fra {E483500} pluss mva.',
  'Lägenheter med två och tre sovrum och en takvåning i Cala de Mijas, nära stranden, från {E483500} plus moms.')
a('A gated complex of 72 homes at Cala de Mijas',
  'Un conjunto cerrado de 72 viviendas en Cala de Mijas con piscina comunitaria, gimnasio y sala social; cinco viviendas de dos y tres dormitorios figuran con precio, con jardín o terraza.',
  'Un ensemble fermé de 72 logements à Cala de Mijas avec piscine commune, salle de sport et salle commune ; cinq logements de deux et trois chambres sont listés, avec jardin ou terrasse.',
  'Eine geschlossene Anlage mit 72 Wohnungen in Cala de Mijas mit Gemeinschaftspool, Fitnessraum und Gemeinschaftsraum; fünf Wohnungen mit zwei und drei Schlafzimmern sind aufgeführt, mit Garten oder Terrasse.',
  'Закрытый комплекс из 72 квартир в Кала-де-Михас с общим бассейном, тренажёрным залом и общей гостиной; в списке пять квартир с двумя и тремя спальнями, с садом или террасой.',
  'مجمّع مغلق من 72 مسكنًا في كالا دي ميهاس مع مسبح مشترك وصالة رياضية وقاعة اجتماعية؛ خمسة مساكن بغرفتي نوم وثلاث غرف نوم مدرجة بالأسعار، بحديقة أو تراس.',
  'Een besloten complex van 72 woningen in Cala de Mijas met gemeenschappelijk zwembad, fitnessruimte en gemeenschappelijke ruimte; vijf woningen met twee en drie slaapkamers staan op de lijst, met tuin of terras.',
  'Zamknięty kompleks 72 lokali w Cala de Mijas ze wspólnym basenem, siłownią i salą wspólną; pięć lokali z dwiema i trzema sypialniami jest na liście, z ogrodem lub tarasem.',
  'Et lukket anlegg med 72 boliger i Cala de Mijas med felles basseng, treningsrom og fellesrom; fem boliger med to og tre soverom er oppført, med hage eller terrasse.',
  'En bevakad anläggning med 72 bostäder i Cala de Mijas med gemensam pool, gym och gemensamhetsrum; fem bostäder med två och tre sovrum är listade, med trädgård eller terrass.')

# ---------------------------------------------------------------- image alts and captions
a('Computer-generated view of a white apartment block with stepped terraces',
  'Vista generada por ordenador de un bloque de apartamentos blanco con terrazas escalonadas detrás de una piscina comunitaria, tumbonas y una palmera',
  'Vue générée par ordinateur d’un immeuble blanc à terrasses en gradins derrière une piscine commune, des transats et un palmier',
  'Computergenerierte Ansicht eines weißen Wohnblocks mit gestaffelten Terrassen hinter einem Gemeinschaftspool, Sonnenliegen und einer Palme',
  'Компьютерная визуализация белого жилого корпуса с террасами-уступами за общим бассейном, шезлонгами и пальмой',
  'منظر مولَّد بالحاسوب لمبنى سكني أبيض بتراسات متدرجة خلف مسبح مشترك ومقاعد تشمّس ونخلة',
  'Computergegenereerd beeld van een wit appartementengebouw met getrapte terrassen achter een gemeenschappelijk zwembad, ligbedden en een palmboom',
  'Wygenerowany komputerowo widok białego budynku z tarasami schodkowymi za wspólnym basenem, leżakami i palmą',
  'Datagenerert bilde av en hvit leilighetsblokk med trappede terrasser bak et felles basseng, solsenger og en palme',
  'Datorgenererad vy av ett vitt flerbostadshus med trappstegsformade terrasser bakom en gemensam pool, solstolar och en palm')
a('Computer-generated aerial view of the white blocks on a wooded slope',
  'Vista aérea generada por ordenador de los bloques blancos en una ladera arbolada sobre la costa, con el mar al fondo',
  'Vue aérienne générée par ordinateur des immeubles blancs sur un versant boisé au-dessus de la côte, avec la mer en arrière-plan',
  'Computergenerierte Luftansicht der weißen Blöcke an einem bewaldeten Hang über der Küste, dahinter das Meer',
  'Компьютерная визуализация белых корпусов на лесистом склоне над побережьем с высоты птичьего полёта; позади море',
  'منظر جوي مولَّد بالحاسوب للمباني البيضاء على منحدر مشجَّر فوق الساحل، وخلفها البحر',
  'Computergegenereerd luchtbeeld van de witte blokken op een beboomde helling boven de kust, met de zee erachter',
  'Wygenerowany komputerowo widok z lotu ptaka na białe budynki na zalesionym zboczu nad wybrzeżem, a za nimi morze',
  'Datagenerert flyfoto av de hvite blokkene i en skogkledd skråning over kysten, med havet bak',
  'Datorgenererad flygvy av de vita husen i en skogsbeklädd sluttning ovanför kusten, med havet bakom')
a('Computer-generated living room with a corner sofa',
  'Salón generado por ordenador con un sofá rinconero, una mesa de centro redonda y una puerta corredera de cristal a la terraza',
  'Séjour généré par ordinateur avec un canapé d’angle, une table basse ronde et une porte vitrée coulissante sur la terrasse',
  'Computergeneriertes Wohnzimmer mit einem Ecksofa, einem runden Couchtisch und einer gläsernen Schiebetür zur Terrasse',
  'Компьютерная визуализация гостиной с угловым диваном, круглым журнальным столиком и стеклянной раздвижной дверью на террасу',
  'غرفة معيشة مولَّدة بالحاسوب فيها أريكة زاوية وطاولة قهوة مستديرة وباب زجاجي منزلق إلى التراس',
  'Computergegenereerde woonkamer met een hoekbank, een ronde salontafel en een glazen schuifdeur naar het terras',
  'Wygenerowany komputerowo salon z sofą narożną, okrągłym stolikiem kawowym i przesuwnymi szklanymi drzwiami na taras',
  'Datagenerert stue med hjørnesofa, et rundt salongbord og en skyvedør i glass til terrassen',
  'Datorgenererat vardagsrum med hörnsoffa, ett runt soffbord och en glasskjutdörr till terrassen')
a('Computer-generated bedroom with a double bed, a built-in wardrobe',
  'Dormitorio generado por ordenador con cama de matrimonio, armario empotrado y una ventana',
  'Chambre générée par ordinateur avec lit double, placard intégré et une fenêtre',
  'Computergeneriertes Schlafzimmer mit Doppelbett, Einbauschrank und einem Fenster',
  'Компьютерная визуализация спальни с двуспальной кроватью, встроенным шкафом и окном',
  'غرفة نوم مولَّدة بالحاسوب فيها سرير مزدوج وخزانة مدمجة ونافذة',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een inbouwkast en een raam',
  'Wygenerowana komputerowo sypialnia z łóżkiem dwuosobowym, szafą wnękową i oknem',
  'Datagenerert soverom med dobbeltseng, innebygd garderobeskap og et vindu',
  'Datorgenererat sovrum med dubbelsäng, inbyggd garderob och ett fönster')
a('Computer-generated views of the building, the shared areas',
  'Vistas del edificio, de las zonas comunes y de los interiores generadas por ordenador, y planos de las cinco viviendas de la lista.',
  'Vues générées par ordinateur de l’immeuble, des espaces communs et des intérieurs, et plans des cinq logements de la liste.',
  'Computergenerierte Ansichten des Gebäudes, der Gemeinschaftsbereiche und der Innenräume sowie die Grundrisse der fünf aufgeführten Wohnungen.',
  'Компьютерные визуализации здания, общих зон и интерьеров и планировки пяти квартир из списка.',
  'مناظر مولَّدة بالحاسوب للمبنى والمناطق المشتركة والداخل، ومخططات المساكن الخمسة المدرجة.',
  'Computergegenereerde beelden van het gebouw, de gemeenschappelijke ruimten en de interieurs, en de plattegronden van de vijf woningen op de lijst.',
  'Wygenerowane komputerowo widoki budynku, części wspólnych i wnętrz oraz rzuty pięciu lokali z listy.',
  'Datagenererte bilder av bygningen, fellesarealene og interiørene, og plantegninger av de fem boligene på listen.',
  'Datorgenererade vyer av byggnaden, de gemensamma ytorna och interiörerna, och planritningar över de fem bostäderna på listan.')
a('All the images are computer-generated illustrations',
  'Todas las imágenes son ilustraciones generadas por ordenador y no fotografías del edificio terminado, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. El promotor indica que sus dibujos de las zonas comunes no muestran los detalles definitivos. Los planos son los del promotor, en fase de proyecto, y las superficies que figuran en ellos son aproximadas y están sujetas al proyecto definitivo. Los nombres de las estancias en los planos están en español.',
  'Toutes les images sont des illustrations générées par ordinateur et non des photographies du bâtiment achevé ; le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Le promoteur précise que ses dessins des espaces communs ne montrent pas les détails définitifs. Les plans sont ceux du promoteur au stade du projet, et les surfaces qui y figurent sont approximatives et soumises au projet définitif. Les noms des pièces sur les plans sont en espagnol.',
  'Alle Bilder sind computergenerierte Illustrationen und keine Fotos des fertigen Gebäudes; Möblierung und Dekoration darauf sind illustrativ und nicht enthalten. Der Bauträger weist darauf hin, dass seine Zeichnungen der Gemeinschaftsbereiche nicht die endgültigen Details zeigen. Die Grundrisse sind die Pläne des Bauträgers im Projektstadium, die darin angegebenen Flächen sind ungefähre Werte und vorbehaltlich des endgültigen Projekts. Die Raumbezeichnungen in den Plänen sind auf Spanisch.',
  'Все изображения — компьютерные иллюстрации, а не фотографии готового здания; мебель и декор на них носят иллюстративный характер и не входят в комплектацию. Застройщик отмечает, что его рисунки общих зон не показывают окончательных деталей. Планировки — проектные чертежи застройщика, площади на них приблизительные и зависят от окончательного проекта. Названия помещений на планах даны на испанском языке.',
  'جميع الصور رسوم توضيحية مولَّدة بالحاسوب وليست صورًا فوتوغرافية للمبنى بعد اكتماله، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. ويشير المطوّر إلى أن رسومه للمناطق المشتركة لا تُظهر التفاصيل النهائية. المخططات هي مخططات المطوّر في مرحلة المشروع، والمساحات المبيّنة عليها تقريبية وخاضعة للمشروع النهائي. وأسماء الغرف على المخططات بالإسبانية.',
  'Alle beelden zijn computergegenereerde illustraties en geen foto’s van het voltooide gebouw, en het meubilair en de inrichting erop zijn illustratief en niet inbegrepen. De ontwikkelaar geeft aan dat zijn tekeningen van de gemeenschappelijke ruimten niet de definitieve details tonen. De plattegronden zijn de plannen van de ontwikkelaar in projectfase en de oppervlakten erop zijn bij benadering en onder voorbehoud van het definitieve project. De namen van de ruimten op de plattegronden zijn in het Spaans.',
  'Wszystkie obrazy to ilustracje wygenerowane komputerowo, a nie zdjęcia ukończonego budynku, a meble i wystrój na nich są poglądowe i nie wchodzą w cenę. Deweloper zaznacza, że jego rysunki części wspólnych nie pokazują ostatecznych szczegółów. Rzuty są planami dewelopera z etapu projektu, a podane na nich powierzchnie są przybliżone i zależą od ostatecznego projektu. Nazwy pomieszczeń na rzutach są po hiszpańsku.',
  'Alle bildene er datagenererte illustrasjoner og ikke fotografier av den ferdige bygningen, og møblene og innredningen på dem er illustrative og ikke inkludert. Utbyggeren oppgir at tegningene av fellesarealene ikke viser de endelige detaljene. Plantegningene er utbyggerens planer i prosjektfasen, og arealene på dem er omtrentlige og avhengige av det endelige prosjektet. Romnavnene på plantegningene er på spansk.',
  'Alla bilder är datagenererade illustrationer och inte fotografier av den färdiga byggnaden, och möblerna och inredningen på dem är illustrativa och ingår inte. Exploatören anger att dess ritningar av de gemensamma ytorna inte visar de slutliga detaljerna. Planritningarna är exploatörens projektplaner, och ytorna på dem är ungefärliga och beroende av det slutliga projektet. Rumsnamnen på planritningarna är på spanska.')
a('The communal pool and the building',
  'La piscina comunitaria y el edificio', 'La piscine commune et l’immeuble', 'Der Gemeinschaftspool und das Gebäude',
  'Общий бассейн и здание', 'المسبح المشترك والمبنى', 'Het gemeenschappelijk zwembad en het gebouw', 'Wspólny basen i budynek',
  'Det felles bassenget og bygningen', 'Den gemensamma poolen och byggnaden')
a('Computer-generated view of two white apartment blocks',
  'Vista generada por ordenador de dos bloques de apartamentos blancos con largas terrazas y pérgolas sobre un césped ajardinado',
  'Vue générée par ordinateur de deux immeubles blancs aux longues terrasses et pergolas au-dessus d’une pelouse paysagée',
  'Computergenerierte Ansicht zweier weißer Wohnblöcke mit langen Terrassen und Pergolen über einer angelegten Rasenfläche',
  'Компьютерная визуализация двух белых жилых корпусов с длинными террасами и перголами над ухоженным газоном',
  'منظر مولَّد بالحاسوب لمبنيين سكنيين أبيضين بتراسات طويلة وبرجولات فوق مرج منسّق',
  'Computergegenereerd beeld van twee witte appartementengebouwen met lange terrassen en pergola’s boven een aangelegd grasveld',
  'Wygenerowany komputerowo widok dwóch białych budynków z długimi tarasami i pergolami nad zagospodarowanym trawnikiem',
  'Datagenerert bilde av to hvite leilighetsblokker med lange terrasser og pergolaer over en opparbeidet plen',
  'Datorgenererad vy av två vita flerbostadshus med långa terrasser och pergolor ovanför en anlagd gräsmatta')
a('Computer-generated aerial view of the white blocks with the communal pool',
  'Vista aérea generada por ordenador de los bloques blancos con la piscina comunitaria delante y la costa que se extiende al fondo',
  'Vue aérienne générée par ordinateur des immeubles blancs avec la piscine commune au premier plan et la côte qui s’étire au loin',
  'Computergenerierte Luftansicht der weißen Blöcke mit dem Gemeinschaftspool davor und der sich in der Ferne erstreckenden Küste',
  'Компьютерная визуализация белых корпусов с высоты птичьего полёта: впереди общий бассейн, вдали тянется побережье',
  'منظر جوي مولَّد بالحاسوب للمباني البيضاء والمسبح المشترك أمامها والساحل الممتد في البعيد',
  'Computergegenereerd luchtbeeld van de witte blokken met het gemeenschappelijk zwembad ervoor en de zich uitstrekkende kustlijn',
  'Wygenerowany komputerowo widok z lotu ptaka na białe budynki ze wspólnym basenem z przodu i rozciągającym się wybrzeżem',
  'Datagenerert flyfoto av de hvite blokkene med det felles bassenget foran og kystlinjen som strekker seg bortover',
  'Datorgenererad flygvy av de vita husen med den gemensamma poolen framför och kustlinjen som sträcker sig bort')
a('The blocks and the pool from the air',
  'Los bloques y la piscina desde el aire', 'Les immeubles et la piscine vus du ciel', 'Die Blöcke und der Pool aus der Luft',
  'Корпуса и бассейн с высоты птичьего полёта', 'المباني والمسبح من الجو', 'De blokken en het zwembad vanuit de lucht',
  'Budynki i basen z lotu ptaka', 'Blokkene og bassenget fra luften', 'Husen och poolen från luften')
a('Computer-generated view of a covered terrace with wicker chairs',
  'Vista generada por ordenador de una terraza cubierta con sillas de mimbre y una mesa redonda, con palmeras y el mar al fondo',
  'Vue générée par ordinateur d’une terrasse couverte avec des chaises en rotin et une table ronde, donnant sur les palmiers et la mer',
  'Computergenerierte Ansicht einer überdachten Terrasse mit Korbstühlen und einem runden Tisch, mit Blick über Palmen aufs Meer',
  'Компьютерная визуализация крытой террасы с плетёными стульями и круглым столом; вдали пальмы и море',
  'منظر مولَّد بالحاسوب لتراس مغطى بكراسي من الخيزران وطاولة مستديرة، تطل على النخيل والبحر',
  'Computergegenereerd beeld van een overdekt terras met rieten stoelen en een ronde tafel, met uitzicht over palmbomen op de zee',
  'Wygenerowany komputerowo widok zadaszonego tarasu z wiklinowymi krzesłami i okrągłym stołem, z widokiem na palmy i morze',
  'Datagenerert bilde av en overbygd terrasse med flettestoler og et rundt bord, med utsikt over palmer til havet',
  'Datorgenererad vy av en övertäckt terrass med korgstolar och ett runt bord, med utsikt över palmer mot havet')
a('Computer-generated open kitchen with white units',
  'Cocina abierta generada por ordenador con muebles blancos y encimera de madera, y una mesa de comedor con sillas',
  'Cuisine ouverte générée par ordinateur avec des meubles blancs et un plan de travail en bois, et une table à manger avec des chaises',
  'Computergenerierte offene Küche mit weißen Schränken und einer Holzarbeitsplatte sowie einem Esstisch mit Stühlen',
  'Компьютерная визуализация открытой кухни с белыми шкафами и деревянной столешницей и обеденным столом со стульями',
  'مطبخ مفتوح مولَّد بالحاسوب بخزائن بيضاء وسطح عمل خشبي، وطاولة طعام مع كراسٍ',
  'Computergegenereerde open keuken met witte kastjes en een houten werkblad, en een eettafel met stoelen',
  'Wygenerowana komputerowo otwarta kuchnia z białymi szafkami i drewnianym blatem oraz stołem jadalnianym z krzesłami',
  'Datagenerert åpent kjøkken med hvite skap og en benkeplate i tre, og et spisebord med stoler',
  'Datorgenererat öppet kök med vita skåp och en bänkskiva i trä, samt ett matbord med stolar')
a('Computer-generated bedroom with two single beds',
  'Dormitorio generado por ordenador con dos camas individuales y una pared estampada, con una ventana al jardín',
  'Chambre générée par ordinateur avec deux lits simples et un mur à motifs, avec une fenêtre sur le jardin',
  'Computergeneriertes Schlafzimmer mit zwei Einzelbetten und einer gemusterten Wand, mit einem Fenster zum Garten',
  'Компьютерная визуализация спальни с двумя односпальными кроватями и стеной с узором; окно выходит в сад',
  'غرفة نوم مولَّدة بالحاسوب فيها سريران مفردان وجدار منقوش، ونافذة تطل على الحديقة',
  'Computergegenereerde slaapkamer met twee eenpersoonsbedden en een gedessineerde wand, met een raam naar de tuin',
  'Wygenerowana komputerowo sypialnia z dwoma łóżkami pojedynczymi i ścianą we wzory, z oknem na ogród',
  'Datagenerert soverom med to enkeltsenger og en mønstret vegg, med et vindu mot hagen',
  'Datorgenererat sovrum med två enkelsängar och en mönstrad vägg, med ett fönster mot trädgården')
a('Computer-generated bathroom with a walk-in shower',
  'Baño generado por ordenador con ducha a ras de suelo, inodoro y mueble de lavabo con espejo',
  'Salle de bains générée par ordinateur avec douche à l’italienne, WC et meuble vasque avec miroir',
  'Computergeneriertes Bad mit bodengleicher Dusche, Toilette und Waschtischunterschrank mit Spiegel',
  'Компьютерная визуализация ванной комнаты с душевой зоной без поддона, унитазом и тумбой с раковиной и зеркалом',
  'حمام مولَّد بالحاسوب فيه مكان استحمام مفتوح ومرحاض ووحدة مغسلة مع مرآة',
  'Computergegenereerde badkamer met een inloopdouche, een toilet en een wastafelmeubel met spiegel',
  'Wygenerowana komputerowo łazienka z prysznicem bez brodzika, toaletą i szafką umywalkową z lustrem',
  'Datagenerert bad med åpen dusj, toalett og servantskap med speil',
  'Datorgenererat badrum med inloppsdusch, toalett och tvättställsskåp med spegel')
a('Bathroom with a shower', 'Baño con ducha', 'Salle de bains avec douche', 'Bad mit Dusche', 'Ванная комната с душем',
  'حمام مع دوش', 'Badkamer met douche', 'Łazienka z prysznicem', 'Bad med dusj', 'Badrum med dusch')
a('Computer-generated bathroom with a bath and shower',
  'Baño generado por ordenador con bañera y ducha, inodoro y lavabo suspendido',
  'Salle de bains générée par ordinateur avec baignoire et douche, WC et vasque suspendue',
  'Computergeneriertes Bad mit Badewanne und Dusche, Toilette und wandhängendem Waschbecken',
  'Компьютерная визуализация ванной комнаты с ванной и душем, унитазом и подвесной раковиной',
  'حمام مولَّد بالحاسوب فيه حوض استحمام ودوش ومرحاض ومغسلة معلّقة',
  'Computergegenereerde badkamer met een bad en douche, een toilet en een hangende wastafel',
  'Wygenerowana komputerowo łazienka z wanną i prysznicem, toaletą i podwieszaną umywalką',
  'Datagenerert bad med badekar og dusj, toalett og veggmontert servant',
  'Datorgenererat badrum med badkar och dusch, toalett och väggmonterat tvättställ')
a('Computer-generated view of the residents’ gym',
  'Vista generada por ordenador del gimnasio de los residentes, con bicicletas estáticas, una cinta de correr, espalderas y paredes de cristal al jardín',
  'Vue générée par ordinateur de la salle de sport des résidents, avec vélos d’appartement, tapis de course, espaliers et parois vitrées sur le jardin',
  'Computergenerierte Ansicht des Fitnessraums der Bewohner mit Standrädern, einem Laufband, Sprossenwänden und Glaswänden zum Garten',
  'Компьютерная визуализация тренажёрного зала для жильцов с велотренажёрами, беговой дорожкой, шведской стенкой и стеклянными стенами в сад',
  'منظر مولَّد بالحاسوب لصالة السكان الرياضية فيها دراجات ثابتة وجهاز مشي وسلالم سويدية وجدران زجاجية تطل على الحديقة',
  'Computergegenereerd beeld van de fitnessruimte voor bewoners met hometrainers, een loopband, een rekstok en glazen wanden naar de tuin',
  'Wygenerowany komputerowo widok siłowni dla mieszkańców z rowerami stacjonarnymi, bieżnią, drabinkami i szklanymi ścianami na ogród',
  'Datagenerert bilde av beboernes treningsrom med mosjonssykler, en tredemølle, ribbevegger og glassvegger mot hagen',
  'Datorgenererad vy av de boendes gym med motionscyklar, ett löpband, ribbstolar och glasväggar mot trädgården')
a('The gym', 'El gimnasio', 'La salle de sport', 'Der Fitnessraum', 'Тренажёрный зал', 'الصالة الرياضية', 'De fitnessruimte',
  'Siłownia', 'Treningsrommet', 'Gymmet')
a('Computer-generated view of the social room with a lounge area',
  'Vista generada por ordenador de la sala social con una zona de estar y mesas de comedor junto a paredes de cristal que dan a la piscina',
  'Vue générée par ordinateur de la salle commune avec un coin salon et des tables à manger le long de parois vitrées donnant sur la piscine',
  'Computergenerierte Ansicht des Gemeinschaftsraums mit einer Sitzecke und Esstischen neben Glaswänden zum Pool',
  'Компьютерная визуализация общей гостиной с зоной отдыха и обеденными столами у стеклянных стен, выходящих на бассейн',
  'منظر مولَّد بالحاسوب للقاعة الاجتماعية فيها ركن جلوس وطاولات طعام بجانب جدران زجاجية تطل على المسبح',
  'Computergegenereerd beeld van de gemeenschappelijke ruimte met een zithoek en eettafels naast glazen wanden naar het zwembad',
  'Wygenerowany komputerowo widok sali wspólnej ze strefą wypoczynkową i stołami jadalnianymi przy szklanych ścianach wychodzących na basen',
  'Datagenerert bilde av fellesrommet med en sofagruppe og spisebord ved glassvegger mot bassenget',
  'Datorgenererad vy av gemensamhetsrummet med en sittgrupp och matbord intill glasväggar mot poolen')
a('The social room', 'La sala social', 'La salle commune', 'Der Gemeinschaftsraum', 'Общая гостиная', 'القاعة الاجتماعية',
  'De gemeenschappelijke ruimte', 'Sala wspólna', 'Fellesrommet', 'Gemensamhetsrummet')
a('Computer-generated view of a paved terrace under a pergola',
  'Vista generada por ordenador de una terraza pavimentada bajo una pérgola junto a la sala social, con asientos y la piscina al fondo',
  'Vue générée par ordinateur d’une terrasse dallée sous une pergola à côté de la salle commune, avec des sièges et la piscine au loin',
  'Computergenerierte Ansicht einer gepflasterten Terrasse unter einer Pergola neben dem Gemeinschaftsraum, mit Sitzmöbeln und dem Pool dahinter',
  'Компьютерная визуализация мощёной террасы под перголой рядом с общей гостиной, с зоной отдыха; за ней виден бассейн',
  'منظر مولَّد بالحاسوب لتراس مرصوف تحت برجولة بجانب القاعة الاجتماعية، مع مقاعد وجلسات والمسبح في البعيد',
  'Computergegenereerd beeld van een bestraat terras onder een pergola naast de gemeenschappelijke ruimte, met zitmeubilair en het zwembad erachter',
  'Wygenerowany komputerowo widok brukowanego tarasu pod pergolą obok sali wspólnej, z meblami wypoczynkowymi i basenem w tle',
  'Datagenerert bilde av en brolagt terrasse under en pergola ved siden av fellesrommet, med sittemøbler og bassenget bak',
  'Datorgenererad vy av en stensatt terrass under en pergola bredvid gemensamhetsrummet, med sittmöbler och poolen bakom')
a('The social room terrace', 'La terraza de la sala social', 'La terrasse de la salle commune', 'Die Terrasse am Gemeinschaftsraum',
  'Терраса общей гостиной', 'تراس القاعة الاجتماعية', 'Het terras bij de gemeenschappelijke ruimte', 'Taras przy sali wspólnej',
  'Terrassen ved fellesrommet', 'Terrassen vid gemensamhetsrummet')

# ---------------------------------------------------------------- overview, why, architecture
a('Seventy-two homes,',
  'Setenta y dos viviendas, <em>cinco a la venta</em>', 'Soixante-douze logements, <em>cinq annoncés</em>',
  'Zweiundsiebzig Wohnungen, <em>fünf aufgeführt</em>', 'Семьдесят две квартиры, <em>пять в списке</em>',
  'اثنان وسبعون مسكنًا، <em>خمسة منها مدرجة</em>', 'Tweeënzeventig woningen, <em>vijf op de lijst</em>',
  'Siedemdziesiąt dwa lokale, <em>pięć na liście</em>', 'Syttito boliger, <em>fem oppført</em>', 'Sjuttiotvå bostäder, <em>fem listade</em>')
a('This is a gated residential complex of 72 homes',
  'Es un conjunto residencial cerrado de 72 viviendas de dos, tres y cuatro dormitorios, en planta baja, primera y segunda y en áticos, en Cala de Mijas, entre Fuengirola y La Cala. El promotor indica que todas las viviendas están orientadas al sur o suroeste y que muchas tienen vistas al mar. Las viviendas de planta baja tienen jardín y los áticos amplias terrazas.',
  'Il s’agit d’un ensemble résidentiel fermé de 72 logements de deux, trois et quatre chambres, au rez-de-chaussée, aux premier et deuxième étages et en penthouse, à Cala de Mijas, entre Fuengirola et La Cala. Le promoteur indique que tous les logements sont orientés au sud ou au sud-ouest et que beaucoup ont vue sur la mer. Les logements du rez-de-chaussée ont un jardin et les penthouses de vastes terrasses.',
  'Dies ist eine geschlossene Wohnanlage mit 72 Wohnungen mit zwei, drei und vier Schlafzimmern, im Erdgeschoss, im ersten und zweiten Obergeschoss und als Penthäuser, in Cala de Mijas zwischen Fuengirola und La Cala. Nach Angabe des Bauträgers sind alle Wohnungen nach Süden oder Südwesten ausgerichtet und viele haben Meerblick. Die Erdgeschosswohnungen haben einen Garten, die Penthäuser große Terrassen.',
  'Это закрытый жилой комплекс из 72 квартир с двумя, тремя и четырьмя спальнями — на первом, втором и третьем этажах и в виде пентхаусов — в Кала-де-Михас, между Фуэнхиролой и Ла-Калой. Застройщик сообщает, что все квартиры обращены на юг или юго-запад, а из многих открывается вид на море. У квартир на первом этаже есть сад, у пентхаусов — просторные террасы.',
  'هذا مجمّع سكني مغلق من 72 مسكنًا بغرفتي نوم وثلاث وأربع غرف نوم، في الطابق الأرضي والأول والثاني وفي شقق بنتهاوس، في كالا دي ميهاس بين فوينخيرولا ولا كالا. ويذكر المطوّر أن جميع المساكن تتجه جنوبًا أو جنوبًا غربيًا وأن كثيرًا منها يطل على البحر. ولمساكن الطابق الأرضي حديقة، وللبنتهاوس تراسات واسعة.',
  'Dit is een besloten woongebouwencomplex van 72 woningen met twee, drie en vier slaapkamers, op de begane grond, de eerste en tweede verdieping en als penthouses, in Cala de Mijas tussen Fuengirola en La Cala. Volgens de ontwikkelaar liggen alle woningen op het zuiden of zuidwesten en hebben veel ervan zeezicht. De woningen op de begane grond hebben een tuin en de penthouses ruime terrassen.',
  'To zamknięty kompleks mieszkaniowy z 72 lokalami z dwiema, trzema i czterema sypialniami, na parterze, pierwszym i drugim piętrze oraz jako penthouse’y, w Cala de Mijas, między Fuengirolą a La Calą. Deweloper podaje, że wszystkie lokale są zwrócone na południe lub południowy zachód, a wiele z nich ma widok na morze. Lokale na parterze mają ogród, a penthouse’y duże tarasy.',
  'Dette er et lukket boligkompleks med 72 boliger med to, tre og fire soverom, i første, andre og tredje etasje og som toppleiligheter, i Cala de Mijas mellom Fuengirola og La Cala. Utbyggeren oppgir at alle boligene vender mot sør eller sørvest og at mange har sjøutsikt. Boligene i første etasje har hage og toppleilighetene store terrasser.',
  'Detta är ett bevakat bostadskomplex med 72 bostäder med två, tre och fyra sovrum, på bottenvåningen, första och andra våningen och som takvåningar, i Cala de Mijas mellan Fuengirola och La Cala. Exploatören anger att alla bostäder vetter mot söder eller sydväst och att många har havsutsikt. Bostäderna på bottenvåningen har trädgård och takvåningarna stora terrasser.')
a('Residents share a pool, a gym and a social room',
  'Los residentes comparten una piscina, un gimnasio y una sala social con cocina, y cada vivienda tiene al menos una plaza de aparcamiento y un trastero. Cinco viviendas figuran con precio, y los documentos del promotor no dan una fecha de finalización.',
  'Les résidents partagent une piscine, une salle de sport et une salle commune avec cuisine, et chaque logement dispose d’au moins une place de stationnement et d’une cave. Cinq logements sont listés avec un prix, et les documents du promoteur ne donnent pas de date d’achèvement.',
  'Die Bewohner teilen sich einen Pool, einen Fitnessraum und einen Gemeinschaftsraum mit Küche, und jede Wohnung hat mindestens einen Stellplatz und einen Abstellraum. Fünf Wohnungen sind mit Preis aufgeführt, und die Unterlagen des Bauträgers nennen kein Fertigstellungsdatum.',
  'Жильцы пользуются общим бассейном, тренажёрным залом и общей гостиной с кухней, а у каждой квартиры есть как минимум одно парковочное место и кладовая. Пять квартир указаны с ценой; в документах застройщика нет даты завершения строительства.',
  'يتشارك السكان مسبحًا وصالة رياضية وقاعة اجتماعية بمطبخ، ولكل مسكن موقف سيارات واحد على الأقل وغرفة تخزين. خمسة مساكن مدرجة بالأسعار، ولا تذكر وثائق المطوّر موعد إنجاز.',
  'De bewoners delen een zwembad, een fitnessruimte en een gemeenschappelijke ruimte met keuken, en elke woning heeft minstens één parkeerplaats en een berging. Vijf woningen staan met een prijs op de lijst en de documenten van de ontwikkelaar geven geen opleverdatum.',
  'Mieszkańcy korzystają ze wspólnego basenu, siłowni i sali wspólnej z kuchnią, a każdy lokal ma co najmniej jedno miejsce postojowe i komórkę. Pięć lokali jest na liście z ceną, a dokumenty dewelopera nie podają terminu ukończenia.',
  'Beboerne deler et basseng, et treningsrom og et fellesrom med kjøkken, og hver bolig har minst én parkeringsplass og en bod. Fem boliger er oppført med pris, og utbyggerens dokumenter oppgir ingen ferdigstillelsesdato.',
  'De boende delar en pool, ett gym och ett gemensamhetsrum med kök, och varje bostad har minst en parkeringsplats och ett förråd. Fem bostäder är listade med pris, och exploatörens dokument anger inget slutdatum.')
a('New two- and three-bedroom homes close to the beach',
  'Viviendas nuevas de dos y tres dormitorios cerca de la playa en Cala de Mijas, cada una con una plaza de aparcamiento y un trastero.',
  'Logements neufs de deux et trois chambres près de la plage à Cala de Mijas, chacun avec une place de stationnement et une cave.',
  'Neue Wohnungen mit zwei und drei Schlafzimmern nahe dem Strand in Cala de Mijas, jeweils mit Stellplatz und Abstellraum.',
  'Новые квартиры с двумя и тремя спальнями недалеко от пляжа в Кала-де-Михас, у каждой — парковочное место и кладовая.',
  'مساكن جديدة بغرفتي نوم وثلاث غرف نوم قرب الشاطئ في كالا دي ميهاس، لكل منها موقف سيارات وغرفة تخزين.',
  'Nieuwe woningen met twee en drie slaapkamers dicht bij het strand in Cala de Mijas, elk met een parkeerplaats en een berging.',
  'Nowe lokale z dwiema i trzema sypialniami blisko plaży w Cala de Mijas, każdy z miejscem postojowym i komórką.',
  'Nye boliger med to og tre soverom nær stranden i Cala de Mijas, hver med en parkeringsplass og en bod.',
  'Nya bostäder med två och tre sovrum nära stranden i Cala de Mijas, var och en med en parkeringsplats och ett förråd.')
a('Buyers who want a new home a short walk from the beach',
  'Compradores que buscan una vivienda nueva a poca distancia a pie de la playa, desde una planta baja con jardín hasta un ático con una gran terraza.',
  'Acheteurs qui cherchent un logement neuf à quelques pas de la plage, d’un rez-de-chaussée avec jardin à un penthouse avec une grande terrasse.',
  'Käufer, die eine neue Wohnung in kurzer Gehentfernung zum Strand suchen, von der Erdgeschosswohnung mit Garten bis zum Penthouse mit großer Terrasse.',
  'Покупатели, которым нужна новая квартира в нескольких минутах ходьбы от пляжа — от квартиры на первом этаже с садом до пентхауса с большой террасой.',
  'مشترون يريدون مسكنًا جديدًا على مسافة قصيرة سيرًا من الشاطئ، من مسكن في الطابق الأرضي بحديقة إلى بنتهاوس بتراس كبير.',
  'Kopers die een nieuwe woning zoeken op korte loopafstand van het strand, van een woning op de begane grond met tuin tot een penthouse met een groot terras.',
  'Kupujący, którzy szukają nowego lokalu w krótkiej odległości spacerem od plaży, od mieszkania na parterze z ogrodem po penthouse z dużym tarasem.',
  'Kjøpere som vil ha en ny bolig i kort gangavstand fra stranden, fra en bolig i første etasje med hage til en toppleilighet med stor terrasse.',
  'Köpare som vill ha en ny bostad på kort promenadavstånd från stranden, från en bostad på bottenvåningen med trädgård till en takvåning med stor terrass.')
a('Gardens on the ground floor, a penthouse terrace',
  'Jardines en planta baja, una terraza de ático de casi 100 {U}, piscina comunitaria, gimnasio y sala social con cocina, y una plaza de aparcamiento y un trastero con cada vivienda.',
  'Des jardins au rez-de-chaussée, une terrasse de penthouse de presque 100 {U}, une piscine commune, une salle de sport et une salle commune avec cuisine, et une place de stationnement et une cave avec chaque logement.',
  'Gärten im Erdgeschoss, eine Penthouse-Terrasse von fast 100 {U}, Gemeinschaftspool, Fitnessraum und Gemeinschaftsraum mit Küche sowie ein Stellplatz und ein Abstellraum bei jeder Wohnung.',
  'Сады на первом этаже, терраса пентхауса почти в 100 {U}, общий бассейн, тренажёрный зал и общая гостиная с кухней, а также парковочное место и кладовая у каждой квартиры.',
  'حدائق في الطابق الأرضي، وتراس بنتهاوس يقارب 100 {U}، ومسبح مشترك وصالة رياضية وقاعة اجتماعية بمطبخ، وموقف سيارات وغرفة تخزين مع كل مسكن.',
  'Tuinen op de begane grond, een penthouseterras van bijna 100 {U}, een gemeenschappelijk zwembad, een fitnessruimte en een gemeenschappelijke ruimte met keuken, en bij elke woning een parkeerplaats en een berging.',
  'Ogrody na parterze, taras penthouse’u o powierzchni prawie 100 {U}, wspólny basen, siłownia i sala wspólna z kuchnią oraz miejsce postojowe i komórka przy każdym lokalu.',
  'Hager i første etasje, en toppleilighetsterrasse på nesten 100 {U}, felles basseng, treningsrom og fellesrom med kjøkken, og en parkeringsplass og en bod til hver bolig.',
  'Trädgårdar på bottenvåningen, en takterrass på nästan 100 {U}, gemensam pool, gym och gemensamhetsrum med kök, samt en parkeringsplats och ett förråd till varje bostad.')
a('The developer puts the beach two minutes away on foot',
  'El promotor sitúa la playa a dos minutos a pie y la promoción junto a la A-7 y la AP-7, con Fuengirola a unos diez minutos en coche y el aeropuerto de Málaga a menos de 25 minutos.',
  'Le promoteur place la plage à deux minutes à pied et le programme à côté de l’A-7 et de l’AP-7, avec Fuengirola à environ dix minutes en voiture et l’aéroport de Malaga à moins de 25 minutes.',
  'Der Bauträger gibt den Strand zwei Gehminuten entfernt an und die Anlage direkt an der A-7 und der AP-7, mit Fuengirola etwa zehn Autominuten und dem Flughafen Malaga unter 25 Minuten entfernt.',
  'Застройщик указывает, что до пляжа две минуты пешком, а комплекс расположен рядом с трассами A-7 и AP-7; до Фуэнхиролы около десяти минут на машине, до аэропорта Малаги — менее 25 минут.',
  'يذكر المطوّر أن الشاطئ على بُعد دقيقتين سيرًا وأن المشروع بجوار الطريقين A-7 وAP-7، وأن فوينخيرولا على بُعد نحو عشر دقائق بالسيارة ومطار مالقة على بُعد أقل من 25 دقيقة.',
  'De ontwikkelaar plaatst het strand op twee minuten lopen en het complex naast de A-7 en de AP-7, met Fuengirola op ongeveer tien minuten rijden en de luchthaven van Málaga op minder dan 25 minuten.',
  'Deweloper podaje, że plaża jest dwie minuty spacerem, a kompleks leży przy A-7 i AP-7, z Fuengirolą około dziesięć minut samochodem i lotniskiem w Maladze w mniej niż 25 minut.',
  'Utbyggeren oppgir stranden to minutter å gå unna og anlegget ved siden av A-7 og AP-7, med Fuengirola omtrent ti minutter unna med bil og Málaga lufthavn på under 25 minutter.',
  'Exploatören anger stranden två minuters promenad bort och anläggningen intill A-7 och AP-7, med Fuengirola ungefär tio minuter bort med bil och Málagas flygplats på under 25 minuter.')
a('The documents give no completion date and the specification is provisional',
  'Los documentos no dan fecha de finalización y la memoria de calidades es provisional, así que confirmamos la licencia, el estado de las obras y la fecha antes de cualquier reserva.',
  'Les documents ne donnent pas de date d’achèvement et le descriptif est provisoire ; nous confirmons donc le permis, l’état des travaux et la date avant toute réservation.',
  'Die Unterlagen nennen kein Fertigstellungsdatum und die Ausstattungsbeschreibung ist vorläufig; deshalb klären wir Genehmigung, Baustand und Termin vor jeder Reservierung.',
  'В документах нет даты завершения строительства, а спецификация предварительная, поэтому до любого бронирования мы уточняем разрешение, стадию работ и дату.',
  'لا تذكر الوثائق موعد إنجاز، والمواصفات مؤقتة، لذلك نؤكد الرخصة ومرحلة الأعمال والتاريخ قبل أي حجز.',
  'De documenten geven geen opleverdatum en de specificatie is voorlopig, dus we bevestigen de vergunning, de stand van de werken en de datum vóór elke reservering.',
  'Dokumenty nie podają terminu ukończenia, a specyfikacja jest wstępna, dlatego przed każdą rezerwacją potwierdzamy pozwolenie, etap prac i termin.',
  'Dokumentene oppgir ingen ferdigstillelsesdato, og spesifikasjonen er foreløpig, så vi bekrefter tillatelsen, byggestadiet og datoen før enhver reservasjon.',
  'Dokumenten anger inget slutdatum och specifikationen är preliminär, så vi bekräftar bygglovet, byggstadiet och datumet före varje reservation.')
a('White blocks, <em>terraces',
  'Bloques blancos, <em>terrazas orientadas al sur</em>', 'Immeubles blancs, <em>terrasses plein sud</em>',
  'Weiße Blöcke, <em>Terrassen nach Süden</em>', 'Белые корпуса, <em>террасы на юг</em>',
  'مبانٍ بيضاء، <em>وتراسات تتجه جنوبًا</em>', 'Witte blokken, <em>terrassen op het zuiden</em>',
  'Białe budynki, <em>tarasy na południe</em>', 'Hvite blokker, <em>terrasser mot sør</em>', 'Vita hus, <em>terrasser mot söder</em>')
a('In the developer’s computer-generated images the homes are in white blocks',
  'En las imágenes generadas por ordenador del promotor, las viviendas están en bloques blancos de hasta cuatro niveles, con largas terrazas y pérgolas, sobre una ladera ajardinada sobre la costa. El promotor indica que todas las viviendas están orientadas al sur o suroeste.',
  'Dans les images générées par ordinateur du promoteur, les logements sont dans des immeubles blancs de quatre niveaux au plus, avec de longues terrasses et des pergolas, sur un versant paysagé au-dessus de la côte. Le promoteur indique que tous les logements sont orientés au sud ou au sud-ouest.',
  'In den computergenerierten Bildern des Bauträgers liegen die Wohnungen in weißen Blöcken mit bis zu vier Ebenen, mit langen Terrassen und Pergolen, an einem angelegten Hang über der Küste. Der Bauträger gibt an, dass alle Wohnungen nach Süden oder Südwesten ausgerichtet sind.',
  'На компьютерных визуализациях застройщика квартиры находятся в белых корпусах высотой до четырёх уровней, с длинными террасами и перголами, на благоустроенном склоне над побережьем. Застройщик сообщает, что все квартиры обращены на юг или юго-запад.',
  'في الصور المولَّدة بالحاسوب من المطوّر، تقع المساكن في مبانٍ بيضاء من أربعة طوابق على الأكثر، بتراسات طويلة وبرجولات، على منحدر منسّق فوق الساحل. ويذكر المطوّر أن جميع المساكن تتجه جنوبًا أو جنوبًا غربيًا.',
  'In de computergegenereerde beelden van de ontwikkelaar liggen de woningen in witte blokken van maximaal vier lagen, met lange terrassen en pergola’s, op een aangelegde helling boven de kust. De ontwikkelaar geeft aan dat alle woningen op het zuiden of zuidwesten liggen.',
  'Na wygenerowanych komputerowo obrazach dewelopera lokale znajdują się w białych budynkach o maksymalnie czterech kondygnacjach, z długimi tarasami i pergolami, na zagospodarowanym zboczu nad wybrzeżem. Deweloper podaje, że wszystkie lokale są zwrócone na południe lub południowy zachód.',
  'På utbyggerens datagenererte bilder ligger boligene i hvite blokker på opptil fire nivåer, med lange terrasser og pergolaer, i en opparbeidet skråning over kysten. Utbyggeren oppgir at alle boligene vender mot sør eller sørvest.',
  'På exploatörens datorgenererade bilder ligger bostäderna i vita hus på upp till fyra nivåer, med långa terrasser och pergolor, i en anlagd sluttning ovanför kusten. Exploatören anger att alla bostäder vetter mot söder eller sydväst.')
a('The ground-floor homes open onto a garden and the penthouses onto large terraces',
  'Las viviendas de planta baja se abren a un jardín y los áticos a grandes terrazas, y cada vivienda de la lista tiene una terraza en su plano.',
  'Les logements du rez-de-chaussée s’ouvrent sur un jardin et les penthouses sur de grandes terrasses, et chaque logement listé a une terrasse sur son plan.',
  'Die Erdgeschosswohnungen öffnen sich zu einem Garten und die Penthäuser zu großen Terrassen, und jede aufgeführte Wohnung hat in ihrem Grundriss eine Terrasse.',
  'Квартиры на первом этаже выходят в сад, а пентхаусы — на большие террасы; у каждой квартиры из списка на плане есть терраса.',
  'تنفتح مساكن الطابق الأرضي على حديقة والبنتهاوس على تراسات كبيرة، ولكل مسكن مدرج تراس في مخططه.',
  'De woningen op de begane grond openen naar een tuin en de penthouses naar grote terrassen, en elke woning op de lijst heeft een terras op de plattegrond.',
  'Lokale na parterze otwierają się na ogród, a penthouse’y na duże tarasy, a każdy lokal z listy ma na rzucie taras.',
  'Boligene i første etasje åpner seg mot en hage og toppleilighetene mot store terrasser, og hver oppført bolig har en terrasse på plantegningen.',
  'Bostäderna på bottenvåningen öppnar sig mot en trädgård och takvåningarna mot stora terrasser, och varje listad bostad har en terrass på sin planritning.')
a('Reinforced concrete, with two-way slabs',
  'Hormigón armado, con forjados bidireccionales o losas según el cálculo estructural.',
  'Béton armé, avec des planchers bidirectionnels ou des dalles pleines selon le calcul de structure.',
  'Stahlbeton, mit zweiachsig gespannten Decken oder Vollplatten nach der statischen Berechnung.',
  'Монолитный железобетон с плитами перекрытия, работающими в двух направлениях, или сплошными плитами — по расчёту конструкций.',
  'خرسانة مسلحة مع بلاطات ثنائية الاتجاه أو بلاطات مصمتة بحسب الحساب الإنشائي.',
  'Gewapend beton, met tweewegplaten of massieve platen volgens de constructieberekening.',
  'Żelbet ze stropami krzyżowo-zbrojonymi lub płytami pełnymi, zgodnie z obliczeniami konstrukcyjnymi.',
  'Armert betong, med toveis dekker eller massive plater etter den statiske beregningen.',
  'Armerad betong, med tvåvägsbjälklag eller massiva plattor enligt konstruktionsberäkningen.')
a('Brickwork clad on the outside as defined in the project',
  'Fábrica de ladrillo revestida al exterior según lo definido en el proyecto, con aislamiento térmico interior, cámara de aire y trasdosado de yeso laminado.',
  'Maçonnerie de brique revêtue à l’extérieur selon le projet, avec isolation thermique intérieure, lame d’air et doublage en plaques de plâtre.',
  'Ziegelmauerwerk, außen nach den Vorgaben des Projekts verkleidet, mit Innendämmung, Luftschicht und Gipskartonvorsatzschale.',
  'Кирпичная кладка с наружной отделкой по проекту, внутренней теплоизоляцией, воздушной прослойкой и облицовкой гипсокартоном.',
  'بناء من الطوب مكسوّ من الخارج وفق المشروع، مع عزل حراري داخلي وفجوة هوائية وبطانة من ألواح الجبس.',
  'Metselwerk van baksteen, aan de buitenzijde afgewerkt zoals in het project bepaald, met thermische isolatie aan de binnenzijde, een luchtspouw en een voorzetwand van gipsplaat.',
  'Mur z cegły z okładziną zewnętrzną określoną w projekcie, z izolacją termiczną od wewnątrz, pustką powietrzną i obudową z płyt gipsowo-kartonowych.',
  'Murverk i tegl, kledd utvendig som definert i prosjektet, med innvendig varmeisolasjon, luftspalte og innvendig kledning i gipsplater.',
  'Tegelmurverk, klätt utvändigt enligt projektet, med invändig värmeisolering, luftspalt och innerbeklädnad av gipsskivor.')
a('PVC frames with double glazing',
  'Carpintería de PVC con doble acristalamiento y persianas en todas las ventanas de dormitorios y salones, del color de la carpintería.',
  'Menuiseries en PVC avec double vitrage, et volets roulants à toutes les fenêtres des chambres et des séjours, de la couleur des menuiseries.',
  'PVC-Rahmen mit Doppelverglasung und Rollläden an allen Schlafzimmer- und Wohnzimmerfenstern in der Farbe der Rahmen.',
  'Рамы из ПВХ с двойным остеклением и жалюзи на всех окнах спален и гостиных в цвет рам.',
  'إطارات من PVC بزجاج مزدوج وستائر دوّارة على جميع نوافذ غرف النوم والمعيشة بلون الإطارات.',
  'PVC-kozijnen met dubbele beglazing en rolluiken op alle slaapkamer- en woonkamerramen in de kleur van de kozijnen.',
  'Ramy z PVC z podwójnym szkleniem oraz rolety na wszystkich oknach sypialni i salonów w kolorze ram.',
  'PVC-rammer med dobbeltglass og rullegardiner på alle soverom- og stuevinduer i samme farge som rammene.',
  'PVC-karmar med dubbelglas och rullgardiner på alla sovrums- och vardagsrumsfönster i karmarnas färg.')
a('Terrace parapets of masonry or railings',
  'Petos de fábrica o barandillas en las terrazas, según el diseño de la fachada.',
  'Garde-corps des terrasses en maçonnerie ou en métal, selon le dessin de la façade.',
  'Terrassenbrüstungen aus Mauerwerk oder Geländer, je nach Fassadengestaltung.',
  'Ограждения террас из кладки или металлические перила — в зависимости от дизайна фасада.',
  'حواجز التراسات من البناء أو من درابزين بحسب تصميم الواجهة.',
  'Terrasborstweringen van metselwerk of hekwerk, naargelang het gevelontwerp.',
  'Balustrady tarasów murowane lub w formie barierek, zgodnie z projektem elewacji.',
  'Terrasserekkverk av murverk eller metallrekkverk, i tråd med fasadedesignet.',
  'Terrassräcken av murverk eller metallräcken, enligt fasadens utformning.')

# ---------------------------------------------------------------- quality specification
a('Source: the developer’s quality specification, edition 00',
  'Fuente: la memoria de calidades del promotor, edición 00. Es provisional y puede cambiar por exigencias de la licencia o a criterio de la dirección del proyecto, sin menoscabo de la calidad.',
  'Source : le descriptif de qualité du promoteur, édition 00. Il est provisoire et peut changer selon les exigences du permis ou à la discrétion de la direction du projet, sans nuire à la qualité.',
  'Quelle: die Ausstattungsbeschreibung des Bauträgers, Ausgabe 00. Sie ist vorläufig und kann sich aufgrund von Genehmigungsauflagen oder nach Ermessen der Projektleitung ändern, ohne die Qualität zu mindern.',
  'Источник: спецификация качества застройщика, редакция 00. Она предварительная и может меняться по требованиям разрешения или по решению руководства проекта без снижения качества.',
  'المصدر: مواصفات الجودة الصادرة عن المطوّر، الإصدار 00. وهي مؤقتة وقد تتغير بحسب متطلبات الرخصة أو بتقدير إدارة المشروع، دون الإخلال بالجودة.',
  'Bron: de kwaliteitsspecificatie van de ontwikkelaar, editie 00. Ze is voorlopig en kan wijzigen door vergunningseisen of naar goeddunken van de projectleiding, zonder de kwaliteit te verminderen.',
  'Źródło: specyfikacja jakości dewelopera, edycja 00. Jest wstępna i może ulec zmianie z powodu wymogów pozwolenia lub decyzji kierownictwa projektu, bez obniżenia jakości.',
  'Kilde: utbyggerens kvalitetsspesifikasjon, utgave 00. Den er foreløpig og kan endres på grunn av krav i tillatelsen eller etter prosjektledelsens skjønn, uten at kvaliteten reduseres.',
  'Källa: exploatörens kvalitetsspecifikation, utgåva 00. Den är preliminär och kan ändras på grund av krav i bygglovet eller efter projektledningens bedömning, utan att kvaliteten försämras.')
a('A reinforced-concrete structure, and a facade of brickwork',
  'Estructura de hormigón armado y fachada de fábrica de ladrillo revestida al exterior, con aislamiento térmico interior, cámara de aire y trasdosado de yeso laminado fijado con perfiles metálicos.',
  'Une structure en béton armé et une façade en maçonnerie de brique revêtue à l’extérieur, avec isolation thermique intérieure, lame d’air et doublage en plaques de plâtre fixé sur profilés métalliques.',
  'Eine Stahlbetonkonstruktion und eine außen verkleidete Ziegelfassade mit Innendämmung, Luftschicht und Gipskartonvorsatzschale auf Metallprofilen.',
  'Железобетонный каркас и фасад из кирпичной кладки с наружной отделкой, внутренней теплоизоляцией, воздушной прослойкой и облицовкой гипсокартоном на металлических профилях.',
  'هيكل من الخرسانة المسلحة وواجهة من الطوب مكسوّة من الخارج، مع عزل حراري داخلي وفجوة هوائية وبطانة من ألواح الجبس مثبتة على أعمدة معدنية.',
  'Een constructie van gewapend beton en een gevel van baksteen, aan de buitenzijde afgewerkt, met thermische isolatie aan de binnenzijde, een luchtspouw en een voorzetwand van gipsplaat op metalen profielen.',
  'Konstrukcja żelbetowa i elewacja z cegły z okładziną zewnętrzną, z izolacją termiczną od wewnątrz, pustką powietrzną i obudową z płyt gipsowo-kartonowych na profilach metalowych.',
  'En konstruksjon av armert betong og en fasade av tegl med utvendig kledning, innvendig varmeisolasjon, luftspalte og innvendig kledning i gipsplater på metallprofiler.',
  'En stomme av armerad betong och en fasad av tegel med utvändig beklädnad, invändig värmeisolering, luftspalt och innerbeklädnad av gipsskivor på metallprofiler.')
a('Flat roofs finished in gravel',
  'Cubiertas planas acabadas en grava donde no hay acceso, y solado de gres antideslizante en las cubiertas transitables.',
  'Toitures plates en gravier là où il n’y a pas d’accès, et dallage en grès cérame antidérapant sur les toitures accessibles.',
  'Flachdächer mit Kiesauflage, wo sie nicht begehbar sind, und rutschfester Feinsteinzeugbelag auf den begehbaren Dächern.',
  'Плоские кровли с гравийной отсыпкой там, где нет доступа, и противоскользящее покрытие из керамогранита на эксплуатируемых кровлях.',
  'أسطح مستوية مكسوّة بالحصى حيث لا يوجد وصول، وتغطية بحجر خزفي مانع للانزلاق على الأسطح التي يمكن السير عليها.',
  'Platte daken afgewerkt met grind waar ze niet toegankelijk zijn, en antislip keramische vloertegels op de betreedbare daken.',
  'Dachy płaskie wykończone żwirem tam, gdzie nie ma dostępu, oraz antypoślizgowa posadzka gresowa na dachach użytkowych.',
  'Flate tak med grusbelegg der det ikke er tilgang, og sklisikker steingods på takene som kan brukes.',
  'Platta tak med grustäckning där det saknas tillträde och halkfritt stengods på de tak som går att beträda.')
a('Partitions and windows', 'Tabiquería y ventanas', 'Cloisons et fenêtres', 'Trennwände und Fenster',
  'Перегородки и окна', 'القواطع والنوافذ', 'Scheidingswanden en ramen', 'Przegrody i okna', 'Skillevegger og vinduer', 'Mellanväggar och fönster')
a('Plasterboard partitions on a metal frame',
  'Tabiquería interior de yeso laminado sobre estructura metálica con aislamiento térmico y acústico, y muros de fábrica de ladrillo trasdosados con yeso laminado y aislamiento entre viviendas y entre una vivienda y las zonas comunes.',
  'Cloisons intérieures en plaques de plâtre sur ossature métallique avec isolation thermique et acoustique, et murs en brique doublés de plaques de plâtre et d’isolant entre les logements et entre un logement et les parties communes.',
  'Trennwände aus Gipskarton auf Metallständern mit Wärme- und Schalldämmung im Inneren der Wohnung sowie Ziegelwände mit Gipskartonvorsatzschale und Dämmung zwischen den Wohnungen und zwischen Wohnung und Gemeinschaftsbereichen.',
  'Внутренние перегородки из гипсокартона на металлическом каркасе с тепло- и звукоизоляцией, а между квартирами и между квартирой и общими зонами — кирпичные стены с облицовкой гипсокартоном и изоляцией.',
  'قواطع داخلية من ألواح الجبس على هيكل معدني مع عزل حراري وصوتي داخل المسكن، وجدران من الطوب مبطّنة بألواح الجبس والعزل بين المساكن وبين المسكن والمناطق المشتركة.',
  'Scheidingswanden van gipsplaat op een metalen frame met thermische en akoestische isolatie binnen de woning, en bakstenen muren met een voorzetwand van gipsplaat en isolatie tussen woningen en tussen een woning en de gemeenschappelijke ruimten.',
  'Przegrody wewnętrzne z płyt gipsowo-kartonowych na stelażu metalowym z izolacją termiczną i akustyczną oraz ściany z cegły z obudową z płyt gipsowo-kartonowych i izolacją między lokalami oraz między lokalem a częściami wspólnymi.',
  'Skillevegger i gipsplater på stålskjelett med varme- og lydisolasjon inne i boligen, og murvegger i tegl med innvendig kledning i gipsplater og isolasjon mellom boligene og mellom en bolig og fellesarealene.',
  'Mellanväggar av gipsskivor på metallstomme med värme- och ljudisolering inne i bostaden, samt tegelväggar med innerbeklädnad av gipsskivor och isolering mellan bostäderna och mellan en bostad och de gemensamma ytorna.')
a('PVC window frames with double glazing and an air chamber',
  'Carpintería de PVC con doble acristalamiento y cámara de aire, que reduce el intercambio de calor y el ruido exterior, y persianas del color de la carpintería en todas las ventanas de dormitorios y salones.',
  'Menuiseries PVC avec double vitrage et lame d’air, qui réduit les échanges de chaleur et le bruit extérieur, et volets roulants de la couleur des menuiseries à toutes les fenêtres des chambres et des séjours.',
  'PVC-Fensterrahmen mit Doppelverglasung und Luftkammer, die den Wärmeaustausch und den Außenlärm verringern, und Rollläden in der Farbe der Rahmen an allen Schlafzimmer- und Wohnzimmerfenstern.',
  'Оконные рамы из ПВХ с двойным остеклением и воздушной камерой, снижающие теплообмен и уличный шум, и жалюзи в цвет рам на всех окнах спален и гостиных.',
  'إطارات نوافذ من PVC بزجاج مزدوج وحجرة هواء تقلل تبادل الحرارة والضجيج الخارجي، وستائر دوّارة بلون الإطارات على جميع نوافذ غرف النوم والمعيشة.',
  'PVC-kozijnen met dubbele beglazing en een luchtkamer, die warmteuitwisseling en lawaai van buiten beperken, en rolluiken in de kleur van de kozijnen op alle slaapkamer- en woonkamerramen.',
  'Ramy okienne z PVC z podwójnym szkleniem i komorą powietrzną, które ograniczają wymianę ciepła i hałas z zewnątrz, oraz rolety w kolorze ram na wszystkich oknach sypialni i salonów.',
  'PVC-vindusrammer med dobbeltglass og luftkammer, som reduserer varmeutveksling og støy utenfra, og rullegardiner i samme farge som rammene på alle soverom- og stuevinduer.',
  'PVC-fönsterkarmar med dubbelglas och luftkammare, som minskar värmeutbyte och buller utifrån, och rullgardiner i karmarnas färg på alla sovrums- och vardagsrumsfönster.')
a('A white-lacquered armoured front door',
  'Puerta de entrada blindada lacada en blanco con herrajes de seguridad, tirador exterior y mirilla, puertas interiores lisas blancas, y armarios modulares abatibles o correderas a juego, con interior de melamina, maletero y barra para colgar.',
  'Porte d’entrée blindée laquée blanc avec quincaillerie de sécurité, poignée extérieure et judas, portes intérieures planes blanches, et placards modulaires battants ou coulissants assortis, avec intérieur en mélaminé, étagère à valises et barre de penderie.',
  'Eine weiß lackierte gepanzerte Wohnungseingangstür mit Sicherheitsbeschlägen, Außengriff und Spion, glatte weiße Innentüren sowie dazu passende modulare Einbauschränke mit Dreh- oder Schiebetüren, innen melaminbeschichtet, mit Koffer-Ablagefach und Kleiderstange.',
  'Бронированная входная дверь, окрашенная в белый цвет, с защитной фурнитурой, наружной ручкой и глазком, гладкие белые межкомнатные двери и подходящие по стилю модульные шкафы с распашными или раздвижными дверцами, внутри с меламиновой отделкой, полкой для чемоданов и штангой.',
  'باب دخول مصفّح مطلي بالأبيض بتجهيزات أمان ومقبض خارجي وعين سحرية، وأبواب داخلية بيضاء مسطحة، وخزائن مدمجة بأبواب مفصلية أو منزلقة بنفس اللون، بداخل من الميلامين ورف للحقائب وعمود تعليق.',
  'Een wit gelakte gepantserde voordeur met beveiligingsbeslag, buitengreep en kijkgaatje, vlakke witte binnendeuren en bijpassende modulaire kasten met draai- of schuifdeuren, binnenin van melamine, met een koffervak en een kledingstang.',
  'Pancerne drzwi wejściowe lakierowane na biało z okuciami zabezpieczającymi, klamką zewnętrzną i wizjerem, gładkie białe drzwi wewnętrzne oraz pasujące do nich modułowe szafy z drzwiami skrzydłowymi lub przesuwnymi, wewnątrz z melaminy, z półką na walizki i drążkiem.',
  'En hvitlakkert pansret inngangsdør med sikkerhetsbeslag, utvendig håndtak og kikkhull, flate hvite innerdører og tilhørende modulgarderober med slag- eller skyvedører, med melamin innvendig, bagasjehylle og kleshengerstang.',
  'En vitlackerad pansardörr med säkerhetsbeslag, utvändigt handtag och titthål, släta vita innerdörrar och matchande moduluppbyggda garderober med slag- eller skjutdörrar, med melamin invändigt, resväskhylla och klädstång.')
a('Stoneware flooring in the living room',
  'Pavimento de gres en el salón, los dormitorios, el vestíbulo, el pasillo y los baños, y gres cerámico antideslizante en las terrazas.',
  'Sols en grès cérame dans le séjour, les chambres, l’entrée, le couloir et les salles de bains, et grès cérame antidérapant sur les terrasses.',
  'Feinsteinzeugboden in Wohnzimmer, Schlafzimmern, Flur, Gang und Bädern sowie rutschfestes keramisches Feinsteinzeug auf den Terrassen.',
  'Керамогранитные полы в гостиной, спальнях, прихожей, коридоре и ванных комнатах и противоскользящий керамогранит на террасах.',
  'أرضيات من الحجر الخزفي في غرفة المعيشة وغرف النوم والمدخل والممر والحمامات، وحجر خزفي مانع للانزلاق على التراسات.',
  'Een vloer van keramische tegels in de woonkamer, de slaapkamers, de hal, de gang en de badkamers, en antislip keramische tegels op de terrassen.',
  'Posadzka gresowa w salonie, sypialniach, przedpokoju, korytarzu i łazienkach oraz antypoślizgowy gres na tarasach.',
  'Steingodsgulv i stuen, soverommene, entreen, gangen og badene, og sklisikkert keramisk steingods på terrassene.',
  'Stengodsgolv i vardagsrummet, sovrummen, hallen, korridoren och badrummen samt halkfritt keramiskt stengods på terrasserna.')
a('Smooth plastic paint in a soft colour',
  'Pintura plástica lisa de color suave en las paredes y blanca en los techos, con pintura o plaqueta cerámica en las zonas húmedas de la cocina y los baños, y un falso techo registrable en el baño que aloja los equipos de climatización.',
  'Peinture plastique lisse de teinte douce sur les murs et blanche aux plafonds, avec peinture ou carrelage céramique sur les parois humides de la cuisine et des salles de bains, et un faux plafond démontable dans la salle de bains qui abrite les équipements de climatisation.',
  'Glatte Kunststoffdispersionsfarbe in einem sanften Farbton an den Wänden und in Weiß an den Decken, mit Farbe oder Keramikfliesen an den Nassbereichswänden von Küche und Bädern und einer zugänglichen Abhangdecke im Bad, die die Klimatechnik aufnimmt.',
  'Гладкая водоэмульсионная краска мягкого оттенка на стенах и белая на потолках, краска или керамическая плитка на мокрых стенах кухни и ванных комнат и съёмный подвесной потолок в ванной, где размещено климатическое оборудование.',
  'دهان بلاستيكي أملس بلون هادئ على الجدران وبالأبيض على الأسقف، مع دهان أو بلاط خزفي على الجدران الرطبة في المطبخ والحمامات، وسقف مستعار قابل للفتح في الحمام يضم معدات التكييف.',
  'Gladde muurverf in een zachte kleur op de wanden en in wit op de plafonds, met verf of keramische tegels op de natte wanden van keuken en badkamers, en een toegankelijk verlaagd plafond in de badkamer waarin de klimaatapparatuur zit.',
  'Gładka farba emulsyjna w stonowanym kolorze na ścianach i biała na sufitach, z farbą lub płytkami ceramicznymi na mokrych ścianach kuchni i łazienek oraz rewizyjnym sufitem podwieszanym w łazience, w którym mieści się sprzęt klimatyzacyjny.',
  'Glatt plastmaling i en dempet farge på veggene og hvit i taket, med maling eller keramiske fliser på de våte veggene i kjøkken og bad, og et tilgjengelig nedsenket tak på badet som rommer klimautstyret.',
  'Slät plastfärg i en dämpad kulör på väggarna och vit i taken, med färg eller keramiska plattor på de våta väggarna i kök och badrum, samt ett åtkomligt undertak i badrummet som rymmer klimatutrustningen.')
a('A furnished kitchen with base and wall units',
  'Cocina amueblada con muebles bajos y altos, encimera postformada en la zona de trabajo, fregadero de acero inoxidable y grifo monomando.',
  'Cuisine équipée de meubles bas et hauts, plan de travail postformé dans la zone de travail, évier en inox et mitigeur monocommande.',
  'Eine möblierte Küche mit Unter- und Oberschränken, einer Arbeitsplatte aus Postforming im Arbeitsbereich, einer Edelstahlspüle und einer Einhebelarmatur.',
  'Меблированная кухня с нижними и верхними шкафами, столешницей из постформинга в рабочей зоне, мойкой из нержавеющей стали и однорычажным смесителем.',
  'مطبخ مفروش بخزائن سفلية وعلوية وسطح عمل من مادة البوستفورمينغ في منطقة العمل وحوض من الفولاذ المقاوم للصدأ وخلاط بمقبض واحد.',
  'Een gemeubileerde keuken met onder- en bovenkasten, een werkblad van postforming in de werkzone, een roestvrijstalen spoelbak en een eengreepskraan.',
  'Umeblowana kuchnia z szafkami dolnymi i górnymi, blatem z postformingu w strefie roboczej, zlewozmywakiem ze stali nierdzewnej i baterią jednouchwytową.',
  'Et møblert kjøkken med over- og underskap, benkeplate i postforming i arbeidssonen, en vask i rustfritt stål og et enhåndsbatteri.',
  'Ett möblerat kök med över- och underskåp, en bänkskiva i postforming i arbetszonen, en diskho i rostfritt stål och en enhandsblandare.')
a('Appliances: an electric oven',
  'Electrodomésticos: horno eléctrico, placa vitrocerámica, campana extractora, frigorífico, lavadora y lavavajillas.',
  'Électroménager : four électrique, plaque vitrocéramique, hotte aspirante, réfrigérateur, lave-linge et lave-vaisselle.',
  'Geräte: ein Elektrobackofen, ein Glaskeramik-Kochfeld, eine Dunstabzugshaube, ein Kühlschrank, eine Waschmaschine und ein Geschirrspüler.',
  'Бытовая техника: электрическая духовка, стеклокерамическая варочная панель, вытяжка, холодильник, стиральная и посудомоечная машины.',
  'الأجهزة: فرن كهربائي وموقد زجاجي خزفي وشفاط وثلاجة وغسالة وغسالة صحون.',
  'Apparaten: een elektrische oven, een keramische kookplaat, een afzuigkap, een koelkast, een wasmachine en een vaatwasser.',
  'Sprzęt: piekarnik elektryczny, płyta ceramiczna, okap, lodówka, pralka i zmywarka.',
  'Hvitevarer: en elektrisk ovn, en keramisk koketopp, en ventilator, et kjøleskap, en vaskemaskin og en oppvaskmaskin.',
  'Vitvaror: en elugn, en keramisk spishäll, en köksfläkt, ett kylskåp, en tvättmaskin och en diskmaskin.')
a('White sanitaryware, a washbasin built into a vanity unit',
  'Aparatos sanitarios blancos, lavabo integrado en mueble en el baño principal y lavabo suspendido en el segundo, espejo en ambos, grifería cromada, monomandos en la bañera y los lavabos y grifería termostática en las duchas.',
  'Sanitaires blancs, vasque intégrée dans un meuble dans la salle de bains principale et vasque suspendue dans la seconde, miroir dans les deux, robinetterie chromée, mitigeurs monocommande sur la baignoire et les vasques et mitigeurs thermostatiques sur les douches.',
  'Weiße Sanitärobjekte, ein in einen Waschtischunterschrank integriertes Waschbecken im Hauptbad und ein wandhängendes Waschbecken im zweiten Bad, in beiden ein Spiegel, verchromte Armaturen, Einhebelmischer an Badewanne und Waschbecken und Thermostatarmaturen an den Duschen.',
  'Белая сантехника, раковина, встроенная в тумбу, в главной ванной и подвесная раковина во второй, зеркала в обеих, хромированная арматура, однорычажные смесители на ванне и раковинах и термостатические смесители в душевых.',
  'أدوات صحية بيضاء، ومغسلة مدمجة في وحدة تخزين في الحمام الرئيسي ومغسلة معلّقة في الحمام الثاني، ومرآة في كليهما، وخلاطات مطلية بالكروم، وخلاطات بمقبض واحد على حوض الاستحمام والمغاسل وخلاطات حرارية في الدوش.',
  'Wit sanitair, een in een meubel geïntegreerde wastafel in de hoofdbadkamer en een hangende wastafel in de tweede, in beide een spiegel, verchroomde kranen, eengreepsmengkranen op het bad en de wastafels en thermostatische kranen op de douches.',
  'Biała ceramika sanitarna, umywalka wbudowana w szafkę w głównej łazience i podwieszana w drugiej, lustro w obu, baterie chromowane, baterie jednouchwytowe przy wannie i umywalkach oraz termostatyczne przy prysznicach.',
  'Hvit sanitærporselen, en servant integrert i et skap på hovedbadet og en veggmontert servant på det andre, speil i begge, kromarmaturer, enhåndsbatterier på badekar og servanter og termostatblandebatterier på dusjene.',
  'Vit sanitetsporslin, ett tvättställ integrerat i ett skåp i huvudbadrummet och ett väggmonterat tvättställ i det andra, spegel i båda, kromade blandare, enhandsblandare på badkar och tvättställ och termostatblandare i duscharna.')
a('Hot water from an aerothermal system in every home',
  'Agua caliente por aerotermia en todas las viviendas, calefacción y refrigeración con bomba de calor por conductos, y un sistema individual de ventilación mecánica.',
  'Eau chaude par système aérothermique dans chaque logement, chauffage et climatisation par pompe à chaleur gainable, et un système individuel de ventilation mécanique.',
  'Warmwasser über ein Luft-Wasser-Wärmepumpensystem in jeder Wohnung, Heizen und Kühlen über eine Kanal-Wärmepumpe und eine individuelle mechanische Lüftung.',
  'Горячая вода от аэротермальной системы в каждой квартире, отопление и охлаждение канальным тепловым насосом и индивидуальная система механической вентиляции.',
  'ماء ساخن من نظام حراري هوائي في كل مسكن، وتدفئة وتبريد بمضخة حرارية عبر المجاري، ونظام تهوية ميكانيكية فردي.',
  'Warm water via een aerothermisch systeem in elke woning, verwarming en koeling met een kanaalwarmtepomp en een individueel mechanisch ventilatiesysteem.',
  'Ciepła woda z systemu aerotermalnego w każdym lokalu, ogrzewanie i chłodzenie kanałową pompą ciepła oraz indywidualny system wentylacji mechanicznej.',
  'Varmtvann fra et aerotermisk system i hver bolig, oppvarming og kjøling med en kanalvarmepumpe og et individuelt mekanisk ventilasjonsanlegg.',
  'Varmvatten från ett aerotermiskt system i varje bostad, uppvärmning och kylning med en kanalvärmepump och ett individuellt mekaniskt ventilationssystem.')
a('The building is listed with an energy rating of B',
  'El edificio figura con calificación energética B, lograda con una envolvente térmica mejorada, acristalamientos eficientes e instalaciones de alta eficiencia. El promotor estima el ahorro respecto a una vivienda con calificación F.',
  'L’immeuble est classé en performance énergétique B, obtenue grâce à une enveloppe thermique améliorée, des vitrages performants et des installations à haut rendement. Le promoteur estime l’économie par rapport à un logement classé F.',
  'Das Gebäude ist mit der Energieeffizienzklasse B aufgeführt, erreicht durch eine verbesserte Gebäudehülle, effiziente Verglasung und hocheffiziente Anlagentechnik. Der Bauträger schätzt die Einsparung gegenüber einer Wohnung der Klasse F.',
  'Здание заявлено с классом энергоэффективности B, достигнутым за счёт улучшенной теплоизоляционной оболочки, эффективного остекления и высокоэффективных инженерных систем. Застройщик оценивает экономию по сравнению с квартирой класса F.',
  'يُدرج المبنى بتصنيف طاقة B، تحقق بغلاف حراري محسّن وزجاج عالي الكفاءة وتجهيزات عالية الكفاءة. ويقدّر المطوّر التوفير مقارنةً بمسكن مصنّف F.',
  'Het gebouw staat vermeld met energielabel B, bereikt met een verbeterde thermische schil, efficiënte beglazing en zeer efficiënte installaties. De ontwikkelaar raamt de besparing ten opzichte van een woning met label F.',
  'Budynek ma klasę energetyczną B, uzyskaną dzięki ulepszonej obudowie cieplnej, efektywnym oknom i wysokosprawnym instalacjom. Deweloper szacuje oszczędność w porównaniu z lokalem klasy F.',
  'Bygningen er oppført med energimerke B, oppnådd med et forbedret klimaskall, effektive vinduer og høyeffektive installasjoner. Utbyggeren anslår besparelsen sammenlignet med en bolig med merke F.',
  'Byggnaden är listad med energiklass B, som uppnås med ett förbättrat klimatskal, effektiva fönster och högeffektiva installationer. Exploatören uppskattar besparingen jämfört med en bostad med klass F.')
a('An electrical installation to the low-voltage regulations',
  'Instalación eléctrica conforme al reglamento de baja tensión, tomas de telecomunicaciones en el salón, los dormitorios y la cocina, preinstalación de antena parabólica, videoportero en los accesos a la urbanización y a los portales, y un aplique, una toma eléctrica y una toma de antena de TV en la terraza del salón.',
  'Installation électrique conforme à la réglementation basse tension, prises de télécommunications dans le séjour, les chambres et la cuisine, pré-installation d’antenne parabolique, visiophone aux entrées de la résidence et des immeubles, et un luminaire, une prise électrique et une prise d’antenne TV sur la terrasse du séjour.',
  'Eine Elektroinstallation nach den Niederspannungsvorschriften, Telekommunikationsanschlüsse in Wohnzimmer, Schlafzimmern und Küche, eine Vorinstallation für eine Satellitenschüssel, eine Videosprechanlage an den Zugängen zur Anlage und zu den Hauseingängen sowie eine Leuchte, eine Steckdose und eine TV-Antennendose auf der Wohnzimmerterrasse.',
  'Электропроводка по правилам для низкого напряжения, телекоммуникационные розетки в гостиной, спальнях и на кухне, подготовка под спутниковую антенну, видеодомофон у входов в комплекс и в подъезды, а также светильник, розетка и антенная розетка ТВ на террасе гостиной.',
  'تمديد كهربائي وفق لائحة الجهد المنخفض، ومآخذ اتصالات في غرفة المعيشة وغرف النوم والمطبخ، وتجهيز مسبق لطبق استقبال فضائي، وجهاز اتصال مرئي عند مداخل المجمّع والمباني، ومصباح ومأخذ كهرباء ومأخذ هوائي تلفاز على تراس غرفة المعيشة.',
  'Een elektrische installatie volgens de laagspanningsvoorschriften, telecomaansluitingen in de woonkamer, de slaapkamers en de keuken, een voorbereiding voor een satellietschotel, een videofoon bij de ingangen van het complex en de blokken, en een lamp, een stopcontact en een tv-antenne-aansluiting op het terras van de woonkamer.',
  'Instalacja elektryczna zgodna z przepisami niskiego napięcia, gniazda telekomunikacyjne w salonie, sypialniach i kuchni, przygotowanie pod antenę satelitarną, wideodomofon przy wejściach na osiedle i do budynków oraz oprawa, gniazdo elektryczne i gniazdo antenowe TV na tarasie salonu.',
  'En elektrisk installasjon etter lavspenningsforskriftene, telekomuttak i stuen, soverommene og kjøkkenet, forberedelse for parabolantenne, videoporttelefon ved inngangene til anlegget og blokkene, og en lampe, en stikkontakt og et TV-antenneuttak på stueterrassen.',
  'En elinstallation enligt lågspänningsföreskrifterna, teleuttag i vardagsrummet, sovrummen och köket, förberedelse för parabolantenn, porttelefon med video vid ingångarna till anläggningen och husen, samt en armatur, ett eluttag och ett tv-antennuttag på vardagsrumsterrassen.')
a('A fully enclosed and fenced complex',
  'Conjunto totalmente cerrado y vallado, con iluminación de bajo consumo en accesos, viales interiores y jardines, detectores de movimiento en portales, vestíbulos de planta y garaje, y jardines con riego y xerojardinería con arbustos y árboles de la zona.',
  'Ensemble entièrement clos et clôturé, avec éclairage basse consommation sur les accès, les voies intérieures et les jardins, détecteurs de mouvement dans les halls, les paliers et le garage, et jardins avec arrosage et xérojardinage d’arbustes et d’arbres locaux.',
  'Eine vollständig umschlossene und eingezäunte Anlage mit Energiesparbeleuchtung an Zugängen, Wegen und Gärten, Bewegungsmeldern in Hauseingängen, Etagenfluren und Garage sowie Gärten mit Bewässerung und trockenheitsverträglicher Bepflanzung mit heimischen Sträuchern und Bäumen.',
  'Полностью огороженный и закрытый комплекс с энергосберегающим освещением входов, внутренних проездов и садов, датчиками движения в подъездах, на этажных площадках и в гараже, садами с поливом и ксерофитным озеленением местными кустарниками и деревьями.',
  'مجمّع مغلق ومسوّر بالكامل، بإضاءة منخفضة الاستهلاك عند المداخل والطرق الداخلية والحدائق، وكاشفات حركة في مداخل المباني وبهو الطوابق والمرآب، وحدائق بنظام ري وزراعة مقاومة للجفاف بشجيرات وأشجار من المنطقة.',
  'Een volledig omsloten en omheind complex met zuinige verlichting bij de toegangen, de interne wegen en de tuinen, bewegingsmelders in de portieken, de verdiepingshallen en de garage, en tuinen met bewatering en droogtebestendige beplanting met inheemse struiken en bomen.',
  'W pełni ogrodzony i zamknięty kompleks z energooszczędnym oświetleniem wejść, dróg wewnętrznych i ogrodów, czujnikami ruchu w klatkach schodowych, na korytarzach pięter i w garażu oraz ogrodami z nawadnianiem i roślinnością odporną na suszę z miejscowych krzewów i drzew.',
  'Et helt avgrenset og inngjerdet anlegg med lavenergibelysning ved adkomstene, de interne veiene og hagene, bevegelsessensorer i oppgangene, etasjegangene og garasjen, og hager med vanning og tørketålende beplantning med stedegne busker og trær.',
  'En helt avgränsad och inhägnad anläggning med lågenergibelysning vid tillfarterna, de interna vägarna och trädgårdarna, rörelsedetektorer i trapphus, våningsplan och garage, samt trädgårdar med bevattning och torktålig planering av inhemska buskar och träd.')
a('A sunny communal outdoor pool for adults with salt chlorination',
  'Una amplia y soleada piscina comunitaria exterior para adultos con cloración salina e iluminación nocturna, un gimnasio equipado, una sala social con cocina, aseos y wifi, y un espacio con un desfibrilador externo.',
  'Une vaste piscine extérieure commune ensoleillée pour adultes, à électrolyse au sel et éclairage nocturne, une salle de sport équipée, une salle commune avec cuisine, sanitaires et wifi, et un espace doté d’un défibrillateur externe.',
  'Ein sonniger Gemeinschaftspool im Freien für Erwachsene mit Salzelektrolyse und Nachtbeleuchtung, ein ausgestatteter Fitnessraum, ein Gemeinschaftsraum mit Küche, Toiletten und WLAN sowie ein Bereich mit einem externen Defibrillator.',
  'Просторный солнечный общий открытый бассейн для взрослых с солевым хлорированием и ночной подсветкой, оборудованный тренажёрный зал, общая гостиная с кухней, санузлами и Wi-Fi и зона с внешним дефибриллятором.',
  'مسبح خارجي مشترك واسع ومشمس للبالغين بمعالجة بالكلور الملحي وإضاءة ليلية، وصالة رياضية مجهزة، وقاعة اجتماعية بمطبخ ودورات مياه وواي فاي، ومساحة مزودة بجهاز إزالة رجفان خارجي.',
  'Een zonnig gemeenschappelijk buitenzwembad voor volwassenen met zoutelektrolyse en nachtverlichting, een uitgeruste fitnessruimte, een gemeenschappelijke ruimte met keuken, toiletten en wifi, en een ruimte met een externe defibrillator.',
  'Duży, nasłoneczniony wspólny basen zewnętrzny dla dorosłych z chlorowaniem solnym i oświetleniem nocnym, wyposażona siłownia, sala wspólna z kuchnią, toaletami i Wi-Fi oraz strefa z zewnętrznym defibrylatorem.',
  'Et stort, solrikt felles utendørsbasseng for voksne med saltklorering og nattbelysning, et utstyrt treningsrom, et fellesrom med kjøkken, toaletter og wifi, og et område med en ekstern hjertestarter.',
  'En stor, solig gemensam utomhuspool för vuxna med saltklorering och nattbelysning, ett utrustat gym, ett gemensamhetsrum med kök, toaletter och wifi samt ett utrymme med en extern hjärtstartare.')
a('A garage with forced ventilation',
  'Garaje con ventilación forzada, detección de monóxido de carbono, protección contra incendios e iluminación de emergencia, y preinstalación para la recarga de vehículos eléctricos según la normativa.',
  'Un garage avec ventilation forcée, détection de monoxyde de carbone, protection incendie et éclairage de secours, et une pré-installation pour la recharge de véhicules électriques conformément à la réglementation.',
  'Eine Garage mit Zwangsbelüftung, Kohlenmonoxid-Erkennung, Brandschutz und Notbeleuchtung sowie einer Vorinstallation für das Laden von Elektrofahrzeugen, wie es die Vorschriften verlangen.',
  'Гараж с принудительной вентиляцией, детекцией угарного газа, противопожарной защитой и аварийным освещением, а также подготовка под зарядку электромобилей по нормативам.',
  'مرآب بتهوية قسرية وكشف عن أول أكسيد الكربون وحماية من الحريق وإضاءة طوارئ، وتجهيز مسبق لشحن المركبات الكهربائية وفق اللوائح.',
  'Een garage met geforceerde ventilatie, koolmonoxidedetectie, brandbeveiliging en noodverlichting, en een voorbereiding voor het laden van elektrische voertuigen zoals de regelgeving voorschrijft.',
  'Garaż z wentylacją wymuszoną, wykrywaniem tlenku węgla, ochroną przeciwpożarową i oświetleniem awaryjnym oraz przygotowaniem pod ładowanie pojazdów elektrycznych zgodnie z przepisami.',
  'En garasje med tvungen ventilasjon, deteksjon av karbonmonoksid, brannvern og nødbelysning, og forberedelse for lading av elbiler slik forskriftene krever.',
  'Ett garage med forcerad ventilation, kolmonoxiddetektering, brandskydd och nödbelysning samt förberedelse för laddning av elfordon enligt föreskrifterna.')

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
print('tr_a entries', len(T))
