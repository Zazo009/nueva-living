# -*- coding: utf-8 -*-
# The Privilege (Estepona), human translations in one pass.
# p(path, es, fr, de, ru, ar, nl, pl, no, sv)
#
# The English string is looked up from the path scaffold.py printed in todo.json, so it is never
# copied here and cannot drift from project.json.
#
# Tokens expanded per locale, so a figure is written once and takes its locale's own format:
# €775500 -> "775.500 €" (nl "€ 775.500", fr/ru/pl/no/sv "775 500 €", ar "775,500 €"),
# #134.62 -> "134,62" (ar "134.62"), and [m2] is the area unit: m² everywhere but ru "м²" and ar "م²".
#
# The 17 unit rows (size strings) and the floorplan alts and captions are built by function below from
# the same numbers the English was built from, with the same words zenith-estepona uses.
#
#   python3 tools/import/k_the_privilege.py <workdir>/tr_z.json <workdir>/todo.json
import json, re, sys

LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}
UNIT['ru'] = 'м²'
UNIT['ar'] = 'م²'


def money(n, loc):
    body = f'{n:,}'.replace(',', GROUP[loc])
    return f'€ {body}' if loc == 'nl' else f'{body} €'


def expand(s, loc):
    s = re.sub(r'€(\d+)', lambda m: money(int(m.group(1)), loc), s)
    s = re.sub(r'#(\d+)\.(\d+)', lambda m: m.group(1) + ('.' if loc == 'ar' else ',') + m.group(2), s)
    return s.replace('[m2]', UNIT[loc])


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
    if en in ('The Privilege', 'The Privilege <em>Estepona</em>') or re.fullmatch(r'Ground [AB]|[1-4][A-H]', en):
        T[en] = {l: en for l in LOCS}
        USED.add(path)
    if path.endswith('.phase') and en == '':
        T[en] = {l: '' for l in LOCS}
        USED.add(path)

# ---- the 17 unit rows --------------------------------------------------------------------------
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
# 2 description
p('.description',
  '17 de 32 viviendas de dos y tres dormitorios en un edificio junto al casco antiguo de Estepona, con piscinas privadas, solariums en la cubierta, piscina comunitaria, gimnasio, spa, club social y espacio de coworking, y con dos plazas de garaje y un trastero en cada vivienda a la venta. No se indica fecha de entrega. Desde €775500 más IVA.',
  '17 logements sur 32, de deux et trois chambres, dans un immeuble à côté de la vieille ville d’Estepona, avec piscines privées, solariums sur le toit, piscine commune, salle de sport, spa, club social et espace de coworking, et deux places de garage et une cave pour chaque logement annoncé. Aucune date de livraison n’est indiquée. À partir de €775500 plus TVA.',
  '17 von 32 Wohnungen mit zwei und drei Schlafzimmern in einem Gebäude neben der Altstadt von Estepona, mit privaten Pools, Dachsolarien, Gemeinschaftspool, Fitnessraum, Spa, Social Club und Coworking-Bereich sowie zwei Garagenstellplätzen und einem Abstellraum bei jeder gelisteten Wohnung. Ein Übergabetermin wird nicht genannt. Ab €775500 plus MwSt.',
  '17 из 32 квартир с двумя и тремя спальнями в здании рядом со старым городом Эстепоны: частные бассейны, солярии на крыше, общий бассейн, тренажёрный зал, спа, клуб для жителей и коворкинг, а к каждой квартире в списке — два места в гараже и кладовая. Срок сдачи не указан. От €775500 плюс НДС.',
  '17 من 32 مسكناً بغرفتي نوم وثلاث غرف نوم في مبنى بجوار البلدة القديمة في إستيبونا، مع مسابح خاصة وسولاريوم على السطح ومسبح مشترك وصالة رياضية وسبا ونادٍ اجتماعي ومساحة عمل مشتركة، وموقفين في المرآب وغرفة تخزين لكل مسكن مدرج. لم يُذكر موعد التسليم. ابتداءً من €775500 زائد ضريبة القيمة المضافة.',
  '17 van de 32 woningen met twee en drie slaapkamers in een gebouw naast de oude binnenstad van Estepona, met privézwembaden, daksolariums, een gemeenschappelijk zwembad, een fitnessruimte, een spa, een sociale club en een coworkingruimte, en twee garageplaatsen en een berging bij elke aangeboden woning. Er wordt geen opleveringsdatum genoemd. Vanaf €775500 plus btw.',
  '17 z 32 mieszkań z dwiema i trzema sypialniami w budynku obok starówki Estepony, z prywatnymi basenami, solariami na dachu, wspólnym basenem, siłownią, spa, klubem dla mieszkańców i przestrzenią coworkingową oraz z dwoma miejscami garażowymi i komórką lokatorską przy każdym oferowanym mieszkaniu. Termin oddania nie jest podany. Od €775500 plus VAT.',
  '17 av 32 boliger med to og tre soverom i en bygning ved siden av gamlebyen i Estepona, med private basseng, solterrasser på taket, felles basseng, treningsrom, spa, sosial klubb og coworking-areal, og to garasjeplasser og en bod til hver oppførte bolig. Ingen overleveringsdato er oppgitt. Fra €775500 pluss mva.',
  '17 av 32 bostäder med två och tre sovrum i en byggnad intill gamla stan i Estepona, med privata pooler, solterrasser på taket, gemensam pool, gym, spa, social klubb och coworkingyta samt två garageplatser och ett förråd till varje listad bostad. Inget tillträdesdatum anges. Från €775500 plus IVA.')

# 3 seoDescription
p('.seoDescription',
  '17 de 32 viviendas de dos y tres dormitorios junto al casco antiguo de Estepona, con piscinas privadas, solariums en la cubierta, gimnasio y spa, desde €775500 más IVA.',
  '17 logements sur 32, de deux et trois chambres, à côté de la vieille ville d’Estepona, avec piscines privées, solariums sur le toit, salle de sport et spa, à partir de €775500 plus TVA.',
  '17 von 32 Wohnungen mit zwei und drei Schlafzimmern neben der Altstadt von Estepona, mit privaten Pools, Dachsolarien, Fitnessraum und Spa, ab €775500 plus MwSt.',
  '17 из 32 квартир с двумя и тремя спальнями рядом со старым городом Эстепоны: частные бассейны, солярии на крыше, тренажёрный зал и спа, от €775500 плюс НДС.',
  '17 من 32 مسكناً بغرفتي نوم وثلاث غرف نوم بجوار البلدة القديمة في إستيبونا، مع مسابح خاصة وسولاريوم على السطح وصالة رياضية وسبا، ابتداءً من €775500 زائد ضريبة القيمة المضافة.',
  '17 van de 32 woningen met twee en drie slaapkamers naast de oude binnenstad van Estepona, met privézwembaden, daksolariums, een fitnessruimte en een spa, vanaf €775500 plus btw.',
  '17 z 32 mieszkań z dwiema i trzema sypialniami obok starówki Estepony, z prywatnymi basenami, solariami na dachu, siłownią i spa, od €775500 plus VAT.',
  '17 av 32 boliger med to og tre soverom ved siden av gamlebyen i Estepona, med private basseng, solterrasser på taket, treningsrom og spa, fra €775500 pluss mva.',
  '17 av 32 bostäder med två och tre sovrum intill gamla stan i Estepona, med privata pooler, solterrasser på taket, gym och spa, från €775500 plus IVA.')

# 4 twitterDescription
p('.twitterDescription',
  'Viviendas de dos y tres dormitorios en Estepona con piscinas privadas, solariums en la cubierta, gimnasio y spa, desde €775500 más IVA.',
  'Logements de deux et trois chambres à Estepona avec piscines privées, solariums sur le toit, salle de sport et spa, à partir de €775500 plus TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern in Estepona mit privaten Pools, Dachsolarien, Fitnessraum und Spa, ab €775500 plus MwSt.',
  'Квартиры с двумя и тремя спальнями в Эстепоне: частные бассейны, солярии на крыше, тренажёрный зал и спа, от €775500 плюс НДС.',
  'مساكن بغرفتي نوم وثلاث غرف نوم في إستيبونا مع مسابح خاصة وسولاريوم على السطح وصالة رياضية وسبا، ابتداءً من €775500 زائد ضريبة القيمة المضافة.',
  'Woningen met twee en drie slaapkamers in Estepona met privézwembaden, daksolariums, een fitnessruimte en een spa, vanaf €775500 plus btw.',
  'Mieszkania z dwiema i trzema sypialniami w Estepona z prywatnymi basenami, solariami na dachu, siłownią i spa, od €775500 plus VAT.',
  'Boliger med to og tre soverom i Estepona med private basseng, solterrasser på taket, treningsrom og spa, fra €775500 pluss mva.',
  'Bostäder med två och tre sovrum i Estepona med privata pooler, solterrasser på taket, gym och spa, från €775500 plus IVA.')

# 5 hero.startingPrice, 7 card.meta[0][1]
p('.hero.startingPrice', 'Desde €775500 + IVA', 'À partir de €775500 + TVA', 'Ab €775500 + MwSt.', 'От €775500 + НДС',
  'ابتداءً من €775500 + ضريبة القيمة المضافة', 'Vanaf €775500 + btw', 'Od €775500 + VAT', 'Fra €775500 + mva.', 'Från €775500 + IVA')
p('.card.meta[0][1]', '€775500 + IVA', '€775500 + TVA', '€775500 + MwSt.', '€775500 + НДС', '€775500 + ضريبة القيمة المضافة',
  '€775500 + btw', '€775500 + VAT', '€775500 + mva.', '€775500 + IVA')

# 6 card.description
p('.card.description',
  '17 de 32 viviendas de dos y tres dormitorios en un edificio junto al casco antiguo de Estepona, con piscinas privadas, solariums en la cubierta y gimnasio y spa comunitarios.',
  '17 logements sur 32, de deux et trois chambres, dans un immeuble à côté de la vieille ville d’Estepona, avec piscines privées, solariums sur le toit, salle de sport et spa communs.',
  '17 von 32 Wohnungen mit zwei und drei Schlafzimmern in einem Gebäude neben der Altstadt von Estepona, mit privaten Pools, Dachsolarien sowie Gemeinschafts-Fitnessraum und Spa.',
  '17 из 32 квартир с двумя и тремя спальнями в здании рядом со старым городом Эстепоны: частные бассейны, солярии на крыше, общий тренажёрный зал и спа.',
  '17 من 32 مسكناً بغرفتي نوم وثلاث غرف نوم في مبنى بجوار البلدة القديمة في إستيبونا، مع مسابح خاصة وسولاريوم على السطح وصالة رياضية وسبا مشتركين.',
  '17 van de 32 woningen met twee en drie slaapkamers in een gebouw naast de oude binnenstad van Estepona, met privézwembaden, daksolariums en een gemeenschappelijke fitnessruimte en spa.',
  '17 z 32 mieszkań z dwiema i trzema sypialniami w budynku obok starówki Estepony, z prywatnymi basenami, solariami na dachu oraz wspólną siłownią i spa.',
  '17 av 32 boliger med to og tre soverom i en bygning ved siden av gamlebyen i Estepona, med private basseng, solterrasser på taket og felles treningsrom og spa.',
  '17 av 32 bostäder med två och tre sovrum i en byggnad intill gamla stan i Estepona, med privata pooler, solterrasser på taket samt gemensamt gym och spa.')

# 8-11 image alts (hero, architecture, lifestyle, privateViewing)
p('.images.hero.alt',
  'Vista generada por ordenador del edificio desde el jardín, con terrazas ajardinadas en cada planta, césped y una piscina delante',
  'Vue de synthèse de l’immeuble depuis le jardin, avec des terrasses plantées à chaque étage, une pelouse et une piscine au premier plan',
  'Computergenerierte Ansicht des Gebäudes vom Garten aus, mit bepflanzten Terrassen auf jedem Geschoss, einem Rasen und einem Pool davor',
  'Компьютерная визуализация здания со стороны сада: озеленённые террасы на каждом этаже, газон и бассейн на переднем плане',
  'منظر مُولَّد بالحاسوب للمبنى من الحديقة، مع تراسات مزروعة في كل طابق ومرج ومسبح في المقدمة',
  'Computergegenereerd beeld van het gebouw vanuit de tuin, met beplante terrassen op elke verdieping, een gazon en een zwembad ervoor',
  'Komputerowa wizualizacja budynku od strony ogrodu, z obsadzonymi roślinnością tarasami na każdym piętrze, trawnikiem i basenem z przodu',
  'Datagenerert bilde av bygningen fra hagen, med beplantede terrasser i hver etasje, en plen og et basseng foran',
  'Datorgenererad bild av byggnaden från trädgården, med planterade terrasser på varje våning, en gräsmatta och en pool framför')
p('.images.architecture.alt',
  'Vista generada por ordenador del edificio desde la calle, con marcos angulares de tono bronce alrededor de las terrazas y palmeras a lo largo de la acera',
  'Vue de synthèse de l’immeuble depuis la rue, avec des cadres anguleux de ton bronze autour des terrasses et des palmiers le long du trottoir',
  'Computergenerierte Ansicht des Gebäudes von der Straße aus, mit kantigen bronzefarbenen Rahmen um die Terrassen und Palmen entlang des Gehwegs',
  'Компьютерная визуализация здания со стороны улицы: угловатые рамы бронзового тона вокруг террас и пальмы вдоль тротуара',
  'منظر مُولَّد بالحاسوب للمبنى من الشارع، مع إطارات زاوية بلون البرونز حول التراسات ونخيل على طول الرصيف',
  'Computergegenereerd beeld van het gebouw vanaf de straat, met hoekige bronskleurige kaders rond de terrassen en palmbomen langs het trottoir',
  'Komputerowa wizualizacja budynku od strony ulicy, z kanciastymi ramami w kolorze brązu wokół tarasów i palmami wzdłuż chodnika',
  'Datagenerert bilde av bygningen fra gaten, med kantete bronsefargede rammer rundt terrassene og palmer langs fortauet',
  'Datorgenererad bild av byggnaden från gatan, med kantiga bronsfärgade ramar runt terrasserna och palmer längs trottoaren')
p('.images.lifestyle.alt',
  'Terraza generada por ordenador con tumbonas, sillones y una piscina, con vistas a colinas y montañas',
  'Terrasse de synthèse avec bains de soleil, fauteuils et une piscine, avec vue sur les collines et les montagnes',
  'Computergenerierte Terrasse mit Sonnenliegen, Sesseln und einem Pool, mit Blick auf Hügel und Berge',
  'Компьютерная визуализация террасы с шезлонгами, креслами и бассейном и видом на холмы и горы',
  'تراس مُولَّد بالحاسوب مع كراسي استلقاء ومقاعد ومسبح، وإطلالة على التلال والجبال',
  'Computergegenereerd terras met ligbedden, fauteuils en een zwembad, met uitzicht op heuvels en bergen',
  'Komputerowa wizualizacja tarasu z leżakami, fotelami i basenem oraz widokiem na wzgórza i góry',
  'Datagenerert terrasse med solsenger, lenestoler og et basseng, med utsikt over åser og fjell',
  'Datorgenererad terrass med solstolar, fåtöljer och en pool, med utsikt över kullar och berg')
p('.images.privateViewing.alt',
  'Dormitorio principal generado por ordenador con una cama doble, un cabecero panelado y puertas de cristal a un balcón con vistas a las colinas',
  'Chambre principale de synthèse avec un lit double, un mur de tête panneauté et des portes vitrées donnant sur un balcon avec vue sur les collines',
  'Computergeneriertes Hauptschlafzimmer mit einem Doppelbett, einer paneelierten Kopfwand und Glastüren zu einem Balkon mit Blick auf die Hügel',
  'Компьютерная визуализация главной спальни с двуспальной кроватью, панелями за изголовьем и стеклянными дверями на балкон с видом на холмы',
  'غرفة نوم رئيسية مُولَّدة بالحاسوب بسرير مزدوج وجدار رأس مكسو بالألواح وأبواب زجاجية إلى شرفة تطل على التلال',
  'Computergegenereerde hoofdslaapkamer met een tweepersoonsbed, een gepaneelde hoofdwand en glazen deuren naar een balkon met uitzicht op de heuvels',
  'Komputerowa wizualizacja głównej sypialni z łóżkiem małżeńskim, panelowaną ścianą za wezgłowiem i szklanymi drzwiami na balkon z widokiem na wzgórza',
  'Datagenerert hovedsoverom med en dobbeltseng, en panelt hodegavlvegg og glassdører til en balkong med utsikt over åsene',
  'Datorgenererat huvudsovrum med en dubbelsäng, en panelklädd väggparti bakom sängen och glasdörrar till en balkong med utsikt över kullarna')

# 12-13 media copy and note
p('.media.copy',
  'Vistas generadas por ordenador del edificio, las zonas comunes y los interiores, y los planos de las 17 viviendas a la venta.',
  'Vues de synthèse de l’immeuble, des espaces communs et des intérieurs, et plans des 17 logements annoncés.',
  'Computergenerierte Ansichten des Gebäudes, der Gemeinschaftsbereiche und der Innenräume sowie die Grundrisse der 17 gelisteten Wohnungen.',
  'Компьютерные визуализации здания, общих зон и интерьеров, а также планировки 17 квартир, находящихся в продаже.',
  'مناظر مُولَّدة بالحاسوب للمبنى والمرافق المشتركة والمساحات الداخلية، ومخططات المساكن السبعة عشر المعروضة.',
  'Computergegenereerde beelden van het gebouw, de gemeenschappelijke ruimten en de interieurs, en de plattegronden van de 17 aangeboden woningen.',
  'Komputerowe wizualizacje budynku, części wspólnych i wnętrz oraz rzuty 17 oferowanych mieszkań.',
  'Datagenererte bilder av bygningen, fellesarealene og interiørene, og plantegningene til de 17 annonserte boligene.',
  'Datorgenererade bilder av byggnaden, de gemensamma ytorna och interiörerna samt planritningarna för de 17 listade bostäderna.')
p('.media.note',
  'Todas las vistas están generadas por ordenador, salvo la vista aérea, que sitúa el edificio generado por ordenador en una fotografía, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los planos de venta del promotor: no tienen carácter contractual, los nombres de las estancias están en inglés y las superficies que figuran difieren en algunos casos de la lista de precios.',
  'Toutes les vues sont des images de synthèse, à l’exception de la vue aérienne, qui place le bâtiment de synthèse dans une photographie, et le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont les plans de vente du promoteur : ils n’ont pas valeur contractuelle, le nom des pièces y est en anglais et les surfaces indiquées diffèrent par endroits de la liste de prix.',
  'Alle Ansichten sind computergeneriert, mit Ausnahme der Luftaufnahme, die das computergenerierte Gebäude in ein Foto setzt; die darin gezeigten Möbel und die Dekoration dienen der Veranschaulichung und sind nicht enthalten. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen sind auf Englisch, und die darin angegebenen Flächen weichen stellenweise von der Preisliste ab.',
  'Все изображения созданы на компьютере, за исключением аэрофотоснимка, на котором компьютерная визуализация здания помещена в фотографию; мебель и декор на них приведены для иллюстрации и в стоимость не входят. Планировки — это продажные планы застройщика: они не имеют договорной силы, названия помещений на них даны по-английски, а указанные площади местами отличаются от прайс-листа.',
  'جميع المناظر مُولَّدة بالحاسوب، باستثناء المنظر الجوي الذي يضع المبنى المُولَّد بالحاسوب داخل صورة فوتوغرافية، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. المخططات هي مخططات البيع الخاصة بالمطوّر: وهي غير ملزمة تعاقديًا، وأسماء الغرف عليها بالإنجليزية، والمساحات المذكورة فيها تختلف في بعض المواضع عن قائمة الأسعار.',
  'Alle beelden zijn computergegenereerd, met uitzondering van de luchtfoto, die het computergegenereerde gebouw in een foto plaatst; de meubels en de inrichting erop zijn illustratief en niet inbegrepen. De plattegronden zijn de verkoopplattegronden van de ontwikkelaar: ze zijn niet contractueel, de ruimtenamen erop zijn in het Engels en de vermelde oppervlakten wijken op sommige punten af van de prijslijst.',
  'Wszystkie wizualizacje są wygenerowane komputerowo, z wyjątkiem zdjęcia lotniczego, które umieszcza komputerowy model budynku na fotografii; widoczne na nich meble i wystrój mają charakter poglądowy i nie są wliczone w cenę. Rzuty to plany sprzedażowe dewelopera: nie mają charakteru umownego, nazwy pomieszczeń są po angielsku, a podane na nich powierzchnie miejscami różnią się od cennika.',
  'Alle bildene er datagenererte, bortsett fra flyfotoet, som plasserer den datagenererte bygningen i et fotografi, og møblene og innredningen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens salgstegninger: de er ikke kontraktsfestet, romnavnene på dem er på engelsk, og arealene på dem avviker noen steder fra prislisten.',
  'Alla bilder är datorgenererade, förutom flygfotot, som placerar den datorgenererade byggnaden i ett fotografi, och möblerna och inredningen i dem är illustrativa och ingår inte. Planritningarna är exploatörens säljplaner: de är inte avtalsgrundande, rummens namn på dem är på engelska och ytorna på dem avviker på sina håll från prislistan.')

# 14-41 media alts and captions (items 2.. in the gallery)
p('.media.items[2].alt',
  'Vista generada por ordenador de una esquina de calle con el edificio sobre un rótulo en la entrada, palmeras y un coche aparcado',
  'Vue de synthèse d’un angle de rue avec l’immeuble au-dessus d’une enseigne à l’entrée, des palmiers et une voiture garée',
  'Computergenerierte Ansicht einer Straßenecke mit dem Gebäude über einem Schild am Eingang, Palmen und einem geparkten Auto',
  'Компьютерная визуализация угла улицы: здание над вывеской у входа, пальмы и припаркованный автомобиль',
  'منظر مُولَّد بالحاسوب لزاوية شارع يظهر فيها المبنى فوق لافتة عند المدخل مع نخيل وسيارة متوقفة',
  'Computergegenereerd beeld van een straathoek met het gebouw boven een bord bij de ingang, palmbomen en een geparkeerde auto',
  'Komputerowa wizualizacja narożnika ulicy z budynkiem nad szyldem przy wejściu, palmami i zaparkowanym samochodem',
  'Datagenerert bilde av et gatehjørne med bygningen over et skilt ved inngangen, palmer og en parkert bil',
  'Datorgenererad bild av ett gathörn med byggnaden ovanför en skylt vid entrén, palmer och en parkerad bil')
p('.media.items[2].caption', 'La esquina y la entrada', 'L’angle et l’entrée', 'Die Ecke und der Eingang', 'Угол здания и вход',
  'الزاوية والمدخل', 'De hoek en de ingang', 'Narożnik i wejście', 'Hjørnet og inngangen', 'Hörnet och entrén')
p('.media.items[3].alt',
  'Vista generada por ordenador del edificio desde un cruce, con un marco de cubierta de tono bronce, un rótulo en el muro de la entrada y un coche en la calzada',
  'Vue de synthèse de l’immeuble depuis un carrefour, avec un cadre de toiture de ton bronze, une enseigne sur le mur d’entrée et une voiture sur la chaussée',
  'Computergenerierte Ansicht des Gebäudes von einer Kreuzung aus, mit einem bronzefarbenen Dachrahmen, einem Schild an der Eingangsmauer und einem Auto auf der Straße',
  'Компьютерная визуализация здания со стороны перекрёстка: рама крыши бронзового тона, вывеска на стене у входа и автомобиль на дороге',
  'منظر مُولَّد بالحاسوب للمبنى من تقاطع طرق، مع إطار سقف بلون البرونز ولافتة على جدار المدخل وسيارة على الطريق',
  'Computergegenereerd beeld van het gebouw vanaf een kruispunt, met een bronskleurig daklijst, een bord op de ingangsmuur en een auto op de weg',
  'Komputerowa wizualizacja budynku od strony skrzyżowania, z ramą dachu w kolorze brązu, szyldem na murze przy wejściu i samochodem na jezdni',
  'Datagenerert bilde av bygningen fra et veikryss, med en bronsefarget takramme, et skilt på inngangsmuren og en bil på veien',
  'Datorgenererad bild av byggnaden från en korsning, med en bronsfärgad takram, en skylt på entrémuren och en bil på vägen')
p('.media.items[3].caption', 'El edificio desde el cruce', 'L’immeuble depuis le carrefour', 'Das Gebäude von der Kreuzung aus',
  'Здание со стороны перекрёстка', 'المبنى من التقاطع', 'Het gebouw vanaf het kruispunt', 'Budynek od strony skrzyżowania',
  'Bygningen fra veikrysset', 'Byggnaden från korsningen')
p('.media.items[4].alt',
  'Vista generada por ordenador del edificio al otro lado de una larga piscina comunitaria con tumbonas y sombrillas blancas',
  'Vue de synthèse de l’immeuble de l’autre côté d’une longue piscine commune avec bains de soleil et parasols blancs',
  'Computergenerierte Ansicht des Gebäudes auf der anderen Seite eines langen Gemeinschaftspools mit Sonnenliegen und weißen Sonnenschirmen',
  'Компьютерная визуализация здания за длинным общим бассейном с шезлонгами и белыми зонтами',
  'منظر مُولَّد بالحاسوب للمبنى على الجانب الآخر من مسبح مشترك طويل مع كراسي استلقاء ومظلات بيضاء',
  'Computergegenereerd beeld van het gebouw aan de overkant van een lang gemeenschappelijk zwembad met ligbedden en witte parasols',
  'Komputerowa wizualizacja budynku po drugiej stronie długiego wspólnego basenu z leżakami i białymi parasolami',
  'Datagenerert bilde av bygningen på den andre siden av et langt felles basseng med solsenger og hvite parasoller',
  'Datorgenererad bild av byggnaden på andra sidan en lång gemensam pool med solstolar och vita parasoller')
p('.media.items[4].caption', 'El edificio al otro lado de la piscina comunitaria', 'L’immeuble de l’autre côté de la piscine commune',
  'Das Gebäude hinter dem Gemeinschaftspool', 'Здание за общим бассейном', 'المبنى على الجانب الآخر من المسبح المشترك',
  'Het gebouw aan de overkant van het gemeenschappelijke zwembad', 'Budynek po drugiej stronie wspólnego basenu',
  'Bygningen på den andre siden av fellesbassenget', 'Byggnaden på andra sidan den gemensamma poolen')
p('.media.items[5].alt',
  'Vista generada por ordenador del edificio al anochecer, con ventanas iluminadas, terrazas ajardinadas y una piscina y césped delante',
  'Vue de synthèse de l’immeuble au crépuscule, avec des fenêtres éclairées, des terrasses plantées et une piscine et une pelouse au premier plan',
  'Computergenerierte Ansicht des Gebäudes in der Abenddämmerung, mit beleuchteten Fenstern, bepflanzten Terrassen und einem Pool und Rasen davor',
  'Компьютерная визуализация здания в сумерках: освещённые окна, озеленённые террасы, бассейн и газон на переднем плане',
  'منظر مُولَّد بالحاسوب للمبنى عند الغسق، مع نوافذ مضاءة وتراسات مزروعة ومسبح ومرج في المقدمة',
  'Computergegenereerd beeld van het gebouw in de schemering, met verlichte ramen, beplante terrassen en een zwembad en gazon ervoor',
  'Komputerowa wizualizacja budynku o zmierzchu, z oświetlonymi oknami, obsadzonymi roślinnością tarasami oraz basenem i trawnikiem z przodu',
  'Datagenerert bilde av bygningen i skumringen, med opplyste vinduer, beplantede terrasser og et basseng og en plen foran',
  'Datorgenererad bild av byggnaden i skymningen, med upplysta fönster, planterade terrasser och en pool och gräsmatta framför')
p('.media.items[6].alt',
  'Fotografía aérea de la parcela en Estepona con el edificio generado por ordenador colocado sobre ella, entre la calle y un espacio verde abierto',
  'Photographie aérienne de la parcelle à Estepona avec l’immeuble de synthèse placé dessus, entre la rue et un espace vert ouvert',
  'Luftaufnahme des Grundstücks in Estepona mit dem darauf platzierten computergenerierten Gebäude, zwischen der Straße und einer offenen Grünfläche',
  'Аэрофотоснимок участка в Эстепоне с размещённой на нём компьютерной визуализацией здания между улицей и открытым зелёным пространством',
  'صورة جوية للقطعة في إستيبونا مع المبنى المُولَّد بالحاسوب موضوعاً عليها، بين الشارع ومساحة خضراء مفتوحة',
  'Luchtfoto van het perceel in Estepona met het computergegenereerde gebouw erop geplaatst, tussen de straat en een open groene ruimte',
  'Zdjęcie lotnicze działki w Esteponie z umieszczonym na niej komputerowym modelem budynku, między ulicą a otwartą przestrzenią zieleni',
  'Flyfoto av tomten i Estepona med den datagenererte bygningen plassert på den, mellom gaten og et åpent grøntareal',
  'Flygfoto av tomten i Estepona med den datorgenererade byggnaden placerad på den, mellan gatan och en öppen grönyta')
p('.media.items[6].caption', 'La parcela desde el aire', 'La parcelle vue du ciel', 'Das Grundstück aus der Luft', 'Участок с высоты птичьего полёта',
  'القطعة من الجو', 'Het perceel vanuit de lucht', 'Działka z lotu ptaka', 'Tomten fra lufta', 'Tomten från luften')
p('.media.items[7].alt',
  'Piscina comunitaria generada por ordenador con tumbonas blancas junto a un pabellón de hormigón y madera, con colinas al fondo',
  'Piscine commune de synthèse avec des bains de soleil blancs à côté d’un pavillon en béton et en bois, avec des collines au loin',
  'Computergenerierter Gemeinschaftspool mit weißen Liegen neben einem Pavillon aus Beton und Holz, mit Hügeln im Hintergrund',
  'Компьютерная визуализация общего бассейна с белыми шезлонгами у павильона из бетона и дерева, на фоне холмов',
  'مسبح مشترك مُولَّد بالحاسوب مع كراسي استلقاء بيضاء بجوار جناح من الخرسانة والخشب وتلال في الخلفية',
  'Computergegenereerd gemeenschappelijk zwembad met witte ligbedden naast een paviljoen van beton en hout, met heuvels op de achtergrond',
  'Komputerowa wizualizacja wspólnego basenu z białymi leżakami przy pawilonie z betonu i drewna, ze wzgórzami w tle',
  'Datagenerert felles basseng med hvite solsenger ved siden av en paviljong i betong og tre, med åser i bakgrunnen',
  'Datorgenererad gemensam pool med vita solstolar intill en paviljong i betong och trä, med kullar i bakgrunden')
p('.media.items[7].caption', 'La piscina comunitaria y un pabellón', 'La piscine commune et un pavillon', 'Der Gemeinschaftspool und ein Pavillon',
  'Общий бассейн и павильон', 'المسبح المشترك وجناح', 'Het gemeenschappelijke zwembad en een paviljoen', 'Wspólny basen i pawilon',
  'Fellesbassenget og en paviljong', 'Den gemensamma poolen och en paviljong')
p('.media.items[8].alt',
  'Espacio de coworking generado por ordenador con una mesa larga, sillas de cuero marrón, lámparas colgantes y una pared de paneles de madera',
  'Espace de coworking de synthèse avec une longue table, des chaises en cuir marron, des suspensions et un mur en panneaux de bois',
  'Computergenerierter Coworking-Bereich mit einem langen Tisch, braunen Ledersesseln, Pendelleuchten und einer Wand aus Holzpaneelen',
  'Компьютерная визуализация коворкинга с длинным столом, коричневыми кожаными стульями, подвесными светильниками и стеной из деревянных панелей',
  'مساحة عمل مشتركة مُولَّدة بالحاسوب بطاولة طويلة وكراسٍ من الجلد البني ومصابيح معلقة وجدار من الألواح الخشبية',
  'Computergegenereerde coworkingruimte met een lange tafel, bruinleren stoelen, hanglampen en een wand van houten panelen',
  'Komputerowa wizualizacja przestrzeni coworkingowej z długim stołem, brązowymi skórzanymi krzesłami, lampami wiszącymi i ścianą z drewnianych paneli',
  'Datagenerert coworking-areal med et langt bord, brune lærstoler, pendellamper og en vegg av trepaneler',
  'Datorgenererad coworkingyta med ett långt bord, bruna läderstolar, hängande lampor och en vägg av träpaneler')
p('.media.items[8].caption', 'El espacio de coworking', 'L’espace de coworking', 'Der Coworking-Bereich', 'Коворкинг', 'مساحة العمل المشتركة',
  'De coworkingruimte', 'Przestrzeń coworkingowa', 'Coworking-arealet', 'Coworkingytan')
p('.media.items[9].alt',
  'Gimnasio generado por ordenador con bicicletas estáticas, esterillas de yoga y un saco de boxeo tras una pared de vidrio con motivos',
  'Salle de sport de synthèse avec des vélos d’exercice, des tapis de yoga et un sac de frappe derrière une paroi de verre à motifs',
  'Computergenerierter Fitnessraum mit Heimtrainern, Yogamatten und einem Boxsack hinter einer gemusterten Glaswand',
  'Компьютерная визуализация тренажёрного зала с велотренажёрами, ковриками для йоги и боксёрской грушей за стеклянной стеной с рисунком',
  'صالة رياضية مُولَّدة بالحاسوب بدراجات تمرين وحصائر يوغا وكيس ملاكمة خلف جدار زجاجي بنقوش',
  'Computergegenereerde fitnessruimte met hometrainers, yogamatten en een bokszak achter een glazen wand met patroon',
  'Komputerowa wizualizacja siłowni z rowerami treningowymi, matami do jogi i workiem bokserskim za wzorzystą szklaną ścianą',
  'Datagenerert treningsrom med spinningsykler, yogamatter og en boksesekk bak en mønstret glassvegg',
  'Datorgenererat gym med motionscyklar, yogamattor och en boxningssäck bakom en mönstrad glasvägg')
p('.media.items[10].alt',
  'Spa generado por ordenador con una piscina interior, una zona de sofás bajos y una celosía con plantas',
  'Spa de synthèse avec une piscine intérieure, un salon de canapés bas et un claustra avec des plantes',
  'Computergeneriertes Spa mit einem Innenpool, einem Loungebereich mit niedrigen Sofas und einem Gitterschirm mit Pflanzen',
  'Компьютерная визуализация спа с крытым бассейном, зоной отдыха с низкими диванами и решётчатой перегородкой с растениями',
  'سبا مُولَّد بالحاسوب بمسبح داخلي ومنطقة جلوس بأرائك منخفضة وحاجز شبكي مع نباتات',
  'Computergegenereerde spa met een binnenzwembad, een loungehoek met lage banken en een latwerkscherm met planten',
  'Komputerowa wizualizacja spa z basenem wewnętrznym, strefą wypoczynkową z niskimi sofami i ażurowym parawanem z roślinami',
  'Datagenerert spa med et innendørs basseng, en loungekrok med lave sofaer og en gitterskjerm med planter',
  'Datorgenererat spa med en inomhuspool, en loungeyta med låga soffor och en gallerskärm med växter')
p('.media.items[11].alt',
  'Terraza cubierta generada por ordenador con una mesa de comedor, una piscina larga y estrecha y un césped con asientos blancos redondos, y montañas al fondo',
  'Terrasse couverte de synthèse avec une table à manger, une piscine longue et étroite et une pelouse avec des sièges blancs ronds, et des montagnes au loin',
  'Computergenerierte überdachte Terrasse mit einem Esstisch, einem langen schmalen Pool und einem Rasen mit runden weißen Sitzen, mit Bergen im Hintergrund',
  'Компьютерная визуализация крытой террасы с обеденным столом, длинным узким бассейном и газоном с круглыми белыми сиденьями, на фоне гор',
  'تراس مسقوف مُولَّد بالحاسوب بطاولة طعام ومسبح طويل وضيق ومرج مع مقاعد بيضاء مستديرة، وجبال في الخلفية',
  'Computergegenereerd overdekt terras met een eettafel, een lang smal zwembad en een gazon met ronde witte zitelementen, met bergen op de achtergrond',
  'Komputerowa wizualizacja zadaszonego tarasu ze stołem jadalnianym, długim wąskim basenem i trawnikiem z okrągłymi białymi siedziskami, z górami w tle',
  'Datagenerert overdekket terrasse med et spisebord, et langt og smalt basseng og en plen med runde hvite sitteelementer, med fjell i bakgrunnen',
  'Datorgenererad övertäckt terrass med ett matbord, en lång smal pool och en gräsmatta med runda vita sittelement, med berg i bakgrunden')
p('.media.items[11].caption', 'Una terraza con piscina y césped', 'Une terrasse avec piscine et pelouse', 'Eine Terrasse mit Pool und Rasen',
  'Терраса с бассейном и газоном', 'تراس مع مسبح ومرج', 'Een terras met zwembad en gazon', 'Taras z basenem i trawnikiem',
  'En terrasse med basseng og plen', 'En terrass med pool och gräsmatta')
p('.media.items[12].caption', 'Una terraza con piscina y vistas a las montañas', 'Une terrasse avec piscine et vue sur les montagnes',
  'Eine Terrasse mit Pool und Blick auf die Berge', 'Терраса с бассейном и видом на горы', 'تراس مع مسبح وإطلالة على الجبال',
  'Een terras met zwembad en uitzicht op de bergen', 'Taras z basenem i widokiem na góry', 'En terrasse med basseng og utsikt over fjellene',
  'En terrass med pool och utsikt över bergen')
p('.media.items[13].alt',
  'Terraza pavimentada generada por ordenador con dos tumbonas y una piscina pequeña con escalones, bajo un techo de lamas',
  'Terrasse dallée de synthèse avec deux bains de soleil et une petite piscine à marches, sous un plafond à lames',
  'Computergenerierte gepflasterte Terrasse mit zwei Sonnenliegen und einem kleinen Pool mit Stufen unter einer Lamellendecke',
  'Компьютерная визуализация мощёной террасы с двумя шезлонгами и небольшим бассейном со ступенями под потолком из реек',
  'تراس مرصوف مُولَّد بالحاسوب بكرسيي استلقاء ومسبح صغير بدرجات تحت سقف من الشرائح',
  'Computergegenereerd bestraat terras met twee ligbedden en een klein zwembad met trappen, onder een lamellenplafond',
  'Komputerowa wizualizacja wybrukowanego tarasu z dwoma leżakami i małym basenem ze schodkami, pod sufitem z lameli',
  'Datagenerert brolagt terrasse med to solsenger og et lite basseng med trinn, under et tak av lameller',
  'Datorgenererad belagd terrass med två solstolar och en liten pool med trappsteg, under ett tak av lameller')
p('.media.items[13].caption', 'Una terraza con una piscina pequeña', 'Une terrasse avec une petite piscine', 'Eine Terrasse mit einem kleinen Pool',
  'Терраса с небольшим бассейном', 'تراس مع مسبح صغير', 'Een terras met een klein zwembad', 'Taras z małym basenem',
  'En terrasse med et lite basseng', 'En terrass med en liten pool')
p('.media.items[14].alt',
  'Terraza generada por ordenador con asientos y una mesa de comedor bajo una cubierta de lamas, frente a un salón acristalado, con colinas al fondo',
  'Terrasse de synthèse avec un salon de jardin et une table à manger sous un toit à lames, devant un séjour vitré, avec des collines au loin',
  'Computergenerierte Terrasse mit Sitzgruppe und Esstisch unter einem Lamellendach, vor einem verglasten Wohnzimmer, mit Hügeln im Hintergrund',
  'Компьютерная визуализация террасы с мягкой мебелью и обеденным столом под крышей из реек перед остеклённой гостиной, на фоне холмов',
  'تراس مُولَّد بالحاسوب بمقاعد وطاولة طعام تحت سقف من الشرائح أمام غرفة معيشة زجاجية، وتلال في الخلفية',
  'Computergegenereerd terras met zitgroep en eettafel onder een lamellendak, voor een beglaasde woonkamer, met heuvels op de achtergrond',
  'Komputerowa wizualizacja tarasu z zestawem wypoczynkowym i stołem jadalnianym pod dachem z lameli, przed przeszklonym salonem, ze wzgórzami w tle',
  'Datagenerert terrasse med sittegruppe og spisebord under et lamelltak, foran en glassfasade-stue, med åser i bakgrunnen',
  'Datorgenererad terrass med sittgrupp och matbord under ett lamelltak, framför ett inglasat vardagsrum, med kullar i bakgrunden')
p('.media.items[14].caption', 'Una terraza y el salón al fondo', 'Une terrasse et le séjour derrière', 'Eine Terrasse und das Wohnzimmer dahinter',
  'Терраса и гостиная за ней', 'تراس وغرفة المعيشة خلفه', 'Een terras en de woonkamer erachter', 'Taras i salon za nim',
  'En terrasse og stuen bak', 'En terrass och vardagsrummet bakom')
p('.media.items[15].alt',
  'Vista generada por ordenador de una terraza amueblada situada dentro de un marco angular de tono bronce en la fachada, con plantas trepadoras',
  'Vue de synthèse d’une terrasse meublée placée dans un cadre anguleux de ton bronze de la façade, avec des plantes grimpantes',
  'Computergenerierte Ansicht einer möblierten Terrasse in einem kantigen bronzefarbenen Fassadenrahmen, mit Kletterpflanzen',
  'Компьютерная визуализация меблированной террасы внутри угловатой рамы бронзового тона на фасаде, с вьющимися растениями',
  'منظر مُولَّد بالحاسوب لتراس مفروش داخل إطار زاوي بلون البرونز في الواجهة، مع نباتات متسلقة',
  'Computergegenereerd beeld van een gemeubileerd terras in een hoekig bronskleurig kader in de gevel, met klimplanten',
  'Komputerowa wizualizacja umeblowanego tarasu w kanciastej ramie w kolorze brązu w elewacji, z pnączami',
  'Datagenerert bilde av en møblert terrasse inne i en kantet bronsefarget ramme i fasaden, med klatreplanter',
  'Datorgenererad bild av en möblerad terrass inuti en kantig bronsfärgad ram i fasaden, med klätterväxter')
p('.media.items[15].caption', 'Una terraza dentro del marco de la fachada', 'Une terrasse dans le cadre de la façade',
  'Eine Terrasse im Fassadenrahmen', 'Терраса внутри рамы фасада', 'تراس داخل إطار الواجهة', 'Een terras in het gevelkader',
  'Taras w ramie elewacji', 'En terrasse inne i fasaderammen', 'En terrass i fasadens ram')
p('.media.items[16].alt',
  'Salón-comedor abierto generado por ordenador con un sofá curvo, una mesa de comedor de mármol y puertas de cristal a la terraza',
  'Séjour-salle à manger ouvert de synthèse avec un canapé arrondi, une table à manger en marbre et des portes vitrées donnant sur la terrasse',
  'Computergenerierter offener Wohn- und Essbereich mit einem geschwungenen Sofa, einem Esstisch aus Marmor und Glastüren zur Terrasse',
  'Компьютерная визуализация открытой гостиной-столовой с изогнутым диваном, мраморным обеденным столом и стеклянными дверями на террасу',
  'غرفة معيشة وطعام مفتوحة مُولَّدة بالحاسوب بأريكة منحنية وطاولة طعام من الرخام وأبواب زجاجية إلى التراس',
  'Computergegenereerde open woon- en eetkamer met een gebogen bank, een marmeren eettafel en glazen deuren naar het terras',
  'Komputerowa wizualizacja otwartego salonu z jadalnią z zaokrągloną sofą, marmurowym stołem jadalnianym i szklanymi drzwiami na taras',
  'Datagenerert åpen stue og spisestue med en buet sofa, et spisebord i marmor og glassdører til terrassen',
  'Datorgenererat öppet vardagsrum med matplats med en böjd soffa, ett matbord i marmor och glasdörrar till terrassen')
p('.media.items[17].alt',
  'Cocina generada por ordenador con una isla de mármol y taburetes, un frente de armarios de madera y una terraza con mesa de comedor',
  'Cuisine de synthèse avec un îlot en marbre et des tabourets, un mur de meubles en bois et une terrasse avec une table à manger',
  'Computergenerierte Küche mit einer Marmorinsel und Barhockern, einer Wand aus Holzschränken und einer Terrasse mit Esstisch',
  'Компьютерная визуализация кухни с мраморным островом и барными стульями, стеной деревянных шкафов и террасой с обеденным столом',
  'مطبخ مُولَّد بالحاسوب بجزيرة من الرخام ومقاعد مرتفعة وجدار من الخزائن الخشبية وتراس بطاولة طعام',
  'Computergegenereerde keuken met een marmeren eiland en barkrukken, een wand van houten kasten en een terras met eettafel',
  'Komputerowa wizualizacja kuchni z marmurową wyspą i stołkami barowymi, ścianą drewnianych szafek i tarasem ze stołem jadalnianym',
  'Datagenerert kjøkken med en marmorøy og barstoler, en vegg av tre-skap og en terrasse med spisebord',
  'Datorgenererat kök med en marmorö och barstolar, en vägg av trämöbler och en terrass med matbord')
p('.media.items[17].caption', 'Cocina y terraza', 'Cuisine et terrasse', 'Küche und Terrasse', 'Кухня и терраса', 'المطبخ والتراس', 'Keuken en terras',
  'Kuchnia i taras', 'Kjøkken og terrasse', 'Kök och terrass')
p('.media.items[19].alt',
  'Baño generado por ordenador con un lavabo suspendido de piedra con dos senos, un espejo largo y una ducha a ras de suelo junto a una pared de cristal',
  'Salle de bain de synthèse avec un meuble-vasque suspendu en pierre à deux vasques, un long miroir et une douche à l’italienne près d’une paroi de verre',
  'Computergeneriertes Badezimmer mit einem wandhängenden Steinwaschtisch mit zwei Becken, einem langen Spiegel und einer bodengleichen Dusche neben einer Glaswand',
  'Компьютерная визуализация ванной комнаты с подвесной каменной тумбой с двумя раковинами, длинным зеркалом и душем без поддона рядом со стеклянной стеной',
  'حمام مُولَّد بالحاسوب بمغسلة حجرية معلقة بحوضين ومرآة طويلة ودش بمستوى الأرض بجانب جدار زجاجي',
  'Computergegenereerde badkamer met een hangend stenen wastafelmeubel met twee kommen, een lange spiegel en een inloopdouche naast een glazen wand',
  'Komputerowa wizualizacja łazienki z wiszącą kamienną szafką z dwiema umywalkami, długim lustrem i prysznicem bez brodzika obok szklanej ściany',
  'Datagenerert bad med en vegghengt servant i stein med to kummer, et langt speil og en åpen dusj ved siden av en glassvegg',
  'Datorgenererat badrum med ett väggmonterat tvättställ i sten med två handfat, en lång spegel och en duschplats utan kant bredvid en glasvägg')

# 76-85 overview, why
p('.overview.headlineHtml', 'Treinta y dos viviendas, <em>diecisiete a la venta</em>', 'Trente-deux logements, <em>dix-sept annoncés</em>',
  'Zweiunddreißig Wohnungen, <em>siebzehn gelistet</em>', 'Тридцать две квартиры, <em>семнадцать в списке</em>',
  'اثنان وثلاثون مسكناً، <em>سبعة عشر منها مدرجة</em>', 'Tweeëndertig woningen, <em>zeventien op de lijst</em>',
  'Trzydzieści dwa mieszkania, <em>siedemnaście na liście</em>', 'Trettito boliger, <em>sytten oppført</em>',
  'Trettiotvå bostäder, <em>sjutton listade</em>')
p('.overview.copy[0]',
  'The Privilege es un edificio residencial de 32 viviendas de dos y tres dormitorios junto al casco antiguo de Estepona. Tiene planta baja, cuatro plantas superiores y una cubierta-solárium, con dos sótanos para garaje y trasteros. Las viviendas de planta baja tienen jardín privado y piscina privada, y los áticos tienen terraza y un solárium privado con piscina en la cubierta.',
  'The Privilege est un immeuble résidentiel de 32 logements de deux et trois chambres à côté de la vieille ville d’Estepona. Il compte un rez-de-chaussée, quatre étages et un niveau de solarium sur le toit, avec deux niveaux de sous-sol pour les parkings et les caves. Les logements du rez-de-chaussée ont un jardin privé et une piscine privée, et les penthouses ont une terrasse et un solarium privé avec piscine sur le toit.',
  'The Privilege ist ein Wohngebäude mit 32 Wohnungen mit zwei und drei Schlafzimmern neben der Altstadt von Estepona. Es hat ein Erdgeschoss, vier Obergeschosse und eine Dachsolarium-Ebene sowie zwei Untergeschosse für Stellplätze und Abstellräume. Die Erdgeschosswohnungen haben einen privaten Garten und einen privaten Pool, die Penthäuser eine Terrasse und ein privates Solarium mit Pool auf dem Dach.',
  'The Privilege — жилой дом на 32 квартиры с двумя и тремя спальнями рядом со старым городом Эстепоны. В нём первый этаж, четыре верхних этажа и уровень солярия на крыше, а также два подземных уровня под парковку и кладовые. У квартир на первом этаже есть частный сад и частный бассейн, а у пентхаусов — терраса и частный солярий с бассейном на крыше.',
  'The Privilege مبنى سكني من 32 مسكناً بغرفتي نوم وثلاث غرف نوم بجوار البلدة القديمة في إستيبونا. فيه طابق أرضي وأربعة طوابق علوية ومستوى سولاريوم على السطح، وطابقان سفليان للمواقف والمخازن. للمساكن الأرضية حديقة خاصة ومسبح خاص، وللبنتهاوس تراس وسولاريوم خاص بمسبح على السطح.',
  'The Privilege is een woongebouw met 32 woningen met twee en drie slaapkamers naast de oude binnenstad van Estepona. Het heeft een begane grond, vier bovenverdiepingen en een solariumniveau op het dak, en twee kelderverdiepingen voor parkeerplaatsen en bergingen. De woningen op de begane grond hebben een privétuin en een privézwembad, en de penthouses hebben een terras en een privésolarium met zwembad op het dak.',
  'The Privilege to budynek mieszkalny z 32 mieszkaniami z dwiema i trzema sypialniami obok starówki Estepony. Ma parter, cztery piętra i poziom solarium na dachu oraz dwa poziomy podziemne z miejscami parkingowymi i komórkami. Mieszkania na parterze mają prywatny ogród i prywatny basen, a penthouse’y mają taras oraz prywatne solarium z basenem na dachu.',
  'The Privilege er en boligbygning med 32 boliger med to og tre soverom ved siden av gamlebyen i Estepona. Den har første etasje, fire etasjer over og et solterrassenivå på taket, med to kjelleretasjer for parkering og boder. Boligene i første etasje har privat hage og privat basseng, og toppleilighetene har terrasse og en privat solterrasse med basseng på taket.',
  'The Privilege är en bostadsbyggnad med 32 bostäder med två och tre sovrum intill gamla stan i Estepona. Den har bottenvåning, fyra våningar ovanför och en solterrassnivå på taket, med två källarplan för parkering och förråd. Bostäderna på bottenvåningen har privat trädgård och privat pool, och takvåningarna har terrass och en privat solterrass med pool på taket.')
p('.overview.copy[1]',
  'Diecisiete viviendas figuran con precio y las otras 15 aparecen como reservadas en la lista de precios del promotor con fecha de septiembre de 2026. Las zonas comunes son una piscina comunitaria con iluminación nocturna, un gimnasio, un spa con sauna, un club social y un espacio de coworking. Los documentos del promotor no dan fecha de entrega.',
  'Dix-sept logements sont annoncés avec un prix et les 15 autres figurent comme réservés sur la liste de prix du promoteur datée de septembre 2026. Les espaces communs comprennent une piscine commune avec éclairage nocturne, une salle de sport, un spa avec sauna, un club social et un espace de coworking. Les documents du promoteur ne donnent pas de date de livraison.',
  'Siebzehn Wohnungen sind mit Preis gelistet, die übrigen 15 sind in der Preisliste des Bauträgers mit Stand September 2026 als reserviert gekennzeichnet. Die Gemeinschaftsbereiche sind ein Gemeinschaftspool mit Nachtbeleuchtung, ein Fitnessraum, ein Spa mit Sauna, ein Social Club und ein Coworking-Bereich. Die Unterlagen des Bauträgers nennen keinen Übergabetermin.',
  'Семнадцать квартир указаны с ценой, остальные 15 помечены как зарезервированные в прайс-листе застройщика за сентябрь 2026 года. Общие зоны — общий бассейн с ночной подсветкой, тренажёрный зал, спа с сауной, клуб для жителей и коворкинг. В документах застройщика срок сдачи не указан.',
  'تظهر سبعة عشر مسكناً بأسعارها، وتظهر المساكن الخمسة عشر الأخرى محجوزة في قائمة أسعار المطوّر المؤرخة سبتمبر 2026. والمرافق المشتركة هي مسبح مشترك بإضاءة ليلية وصالة رياضية وسبا بساونا ونادٍ اجتماعي ومساحة عمل مشتركة. ولا تذكر وثائق المطوّر موعد التسليم.',
  'Zeventien woningen staan met een prijs op de lijst en de andere 15 staan als gereserveerd op de prijslijst van de ontwikkelaar van september 2026. De gemeenschappelijke ruimten zijn een gemeenschappelijk zwembad met nachtverlichting, een fitnessruimte, een spa met sauna, een sociale club en een coworkingruimte. De documenten van de ontwikkelaar noemen geen opleveringsdatum.',
  'Siedemnaście mieszkań ma podaną cenę, a pozostałe 15 jest oznaczonych jako zarezerwowane w cenniku dewelopera z września 2026 roku. Części wspólne to wspólny basen z oświetleniem nocnym, siłownia, spa z sauną, klub dla mieszkańców i przestrzeń coworkingowa. Dokumenty dewelopera nie podają terminu oddania.',
  'Sytten boliger er oppført med pris, og de øvrige 15 er markert som reservert i utbyggerens prisliste fra september 2026. Fellesarealene er et felles basseng med nattbelysning, et treningsrom, et spa med badstue, en sosial klubb og et coworking-areal. Utbyggerens dokumenter oppgir ingen overleveringsdato.',
  'Sjutton bostäder är listade med pris och de övriga 15 är markerade som reserverade i exploatörens prislista från september 2026. De gemensamma ytorna är en gemensam pool med kvällsbelysning, ett gym, ett spa med bastu, en social klubb och en coworkingyta. Exploatörens dokument anger inget tillträdesdatum.')
p('.overview.metrics[0][1]', '32 viviendas', '32 logements', '32 Wohnungen', '32 квартиры', '32 مسكناً', '32 woningen', '32 mieszkania', '32 boliger', '32 bostäder')
p('.overview.metrics[3][1]', '€775500 - €2084500 + IVA', '€775500 - €2084500 + TVA', '€775500 - €2084500 + MwSt.', '€775500 - €2084500 + НДС',
  '€775500 - €2084500 + ضريبة القيمة المضافة', '€775500 - €2084500 + btw', '€775500 - €2084500 + VAT', '€775500 - €2084500 + mva.', '€775500 - €2084500 + IVA')
p('.why.copy',
  'Viviendas de dos y tres dormitorios junto al casco antiguo de Estepona, cada una con dos plazas de garaje y un trastero, y gimnasio, spa y coworking comunitarios.',
  'Des logements de deux et trois chambres à côté de la vieille ville d’Estepona, chacun avec deux places de garage et une cave, et une salle de sport, un spa et un espace de coworking communs.',
  'Wohnungen mit zwei und drei Schlafzimmern neben der Altstadt von Estepona, jede mit zwei Garagenstellplätzen und einem Abstellraum, sowie Gemeinschafts-Fitnessraum, Spa und Coworking.',
  'Квартиры с двумя и тремя спальнями рядом со старым городом Эстепоны, к каждой — два места в гараже и кладовая, а для жителей — общие тренажёрный зал, спа и коворкинг.',
  'مساكن بغرفتي نوم وثلاث غرف نوم بجوار البلدة القديمة في إستيبونا، لكل منها موقفان في المرآب وغرفة تخزين، مع صالة رياضية وسبا ومساحة عمل مشتركة.',
  'Woningen met twee en drie slaapkamers naast de oude binnenstad van Estepona, elk met twee garageplaatsen en een berging, en een gemeenschappelijke fitnessruimte, spa en coworkingruimte.',
  'Mieszkania z dwiema i trzema sypialniami obok starówki Estepony, każde z dwoma miejscami garażowymi i komórką lokatorską, oraz wspólna siłownia, spa i przestrzeń coworkingowa.',
  'Boliger med to og tre soverom ved siden av gamlebyen i Estepona, hver med to garasjeplasser og en bod, og felles treningsrom, spa og coworking.',
  'Bostäder med två och tre sovrum intill gamla stan i Estepona, var och en med två garageplatser och ett förråd, samt gemensamt gym, spa och coworking.')
p('.why.points[0][1]',
  'Compradores que quieren una vivienda nueva de dos o tres dormitorios junto al casco antiguo de Estepona, para vivir o como segunda residencia, desde una vivienda de planta baja con jardín hasta un ático con piscina en la cubierta.',
  'Des acheteurs qui veulent un logement neuf de deux ou trois chambres à côté de la vieille ville d’Estepona, pour y vivre ou comme résidence secondaire, du logement de rez-de-chaussée avec jardin au penthouse avec piscine sur le toit.',
  'Käufer, die eine neue Wohnung mit zwei oder drei Schlafzimmern neben der Altstadt von Estepona suchen, zum Selbstbewohnen oder als Zweitwohnsitz, von der Erdgeschosswohnung mit Garten bis zum Penthouse mit Pool auf dem Dach.',
  'Покупатели, которым нужна новая квартира с двумя или тремя спальнями рядом со старым городом Эстепоны — для жизни или как вторая недвижимость: от квартиры на первом этаже с садом до пентхауса с бассейном на крыше.',
  'مشترون يريدون مسكناً جديداً بغرفتي نوم أو ثلاث غرف نوم بجوار البلدة القديمة في إستيبونا، للسكن أو كمسكن ثانٍ، من مسكن أرضي بحديقة إلى بنتهاوس بمسبح على السطح.',
  'Kopers die een nieuwe woning met twee of drie slaapkamers naast de oude binnenstad van Estepona zoeken, om in te wonen of als tweede woning, van een woning op de begane grond met tuin tot een penthouse met zwembad op het dak.',
  'Kupujący, którzy szukają nowego mieszkania z dwiema lub trzema sypialniami obok starówki Estepony, do zamieszkania lub jako drugi dom, od mieszkania na parterze z ogrodem po penthouse z basenem na dachu.',
  'Kjøpere som vil ha en ny bolig med to eller tre soverom ved siden av gamlebyen i Estepona, til å bo i eller som feriebolig, fra en bolig i første etasje med hage til en toppleilighet med basseng på taket.',
  'Köpare som vill ha en ny bostad med två eller tre sovrum intill gamla stan i Estepona, att bo i eller som andrabostad, från en bostad på bottenvåningen med trädgård till en takvåning med pool på taket.')
p('.why.points[1][1]',
  'Un edificio de 32 viviendas con jardín y piscina privados en planta baja, un solárium y una piscina privados en la cubierta de cada ático, y gimnasio, spa, club social y coworking para los residentes.',
  'Un immeuble de 32 logements avec jardin et piscine privés au rez-de-chaussée, un solarium et une piscine privés sur le toit de chaque penthouse, et une salle de sport, un spa, un club social et un espace de coworking pour les résidents.',
  'Ein Gebäude mit 32 Wohnungen, mit privatem Garten und Pool im Erdgeschoss, einem privaten Dachsolarium mit Pool für jedes Penthouse sowie Fitnessraum, Spa, Social Club und Coworking für die Bewohner.',
  'Дом на 32 квартиры с частным садом и бассейном на первом этаже, частным солярием и бассейном на крыше у каждого пентхауса, а для жителей — тренажёрный зал, спа, клуб и коворкинг.',
  'مبنى من 32 مسكناً بحديقة ومسبح خاصين في الطابق الأرضي، وسولاريوم ومسبح خاصين على سطح كل بنتهاوس، وصالة رياضية وسبا ونادٍ اجتماعي ومساحة عمل مشتركة للسكان.',
  'Een gebouw met 32 woningen, met een privétuin en privézwembad op de begane grond, een privésolarium en zwembad op het dak bij elk penthouse, en een fitnessruimte, spa, sociale club en coworkingruimte voor de bewoners.',
  'Budynek z 32 mieszkaniami, z prywatnym ogrodem i basenem na parterze, prywatnym solarium i basenem na dachu przy każdym penthousie oraz siłownią, spa, klubem i przestrzenią coworkingową dla mieszkańców.',
  'En bygning med 32 boliger, med privat hage og basseng i første etasje, en privat solterrasse og et basseng på taket til hver toppleilighet, og treningsrom, spa, sosial klubb og coworking for beboerne.',
  'En byggnad med 32 bostäder, med privat trädgård och pool på bottenvåningen, en privat solterrass och pool på taket till varje takvåning samt gym, spa, social klubb och coworking för de boende.')
p('.why.points[2][1]',
  'El folleto del promotor sitúa el puerto deportivo, Playa Beach y la playa de La Rada a menos de diez minutos, junto al casco antiguo, con la A-7 y la AP-7 cerca.',
  'La brochure du promoteur situe le port de plaisance, Playa Beach et la plage de La Rada à moins de dix minutes, à côté de la vieille ville, avec l’A-7 et l’AP-7 à proximité.',
  'Laut Prospekt des Bauträgers sind der Yachthafen, der Strand Playa Beach und der Strand La Rada weniger als zehn Minuten entfernt, neben der Altstadt, mit der A-7 und der AP-7 in der Nähe.',
  'В брошюре застройщика яхтенная гавань, пляж Playa Beach и пляж Ла-Рада указаны менее чем в десяти минутах, рядом со старым городом, а автострады A-7 и AP-7 находятся поблизости.',
  'يضع كتيّب المطوّر المرفأ وشاطئ بلايا بيتش وشاطئ لا رادا على بعد أقل من عشر دقائق، بجوار البلدة القديمة، مع الطريقين A-7 وAP-7 القريبين.',
  'In de brochure van de ontwikkelaar liggen de jachthaven, het strand Playa Beach en het strand La Rada op minder dan tien minuten, naast de oude binnenstad, met de A-7 en de AP-7 in de buurt.',
  'Według broszury dewelopera port jachtowy, plaża Playa Beach i plaża La Rada są oddalone o mniej niż dziesięć minut, obok starówki, a autostrady A-7 i AP-7 są w pobliżu.',
  'Utbyggerens brosjyre oppgir at småbåthavnen, stranden Playa Beach og stranden La Rada ligger under ti minutter unna, ved siden av gamlebyen, med A-7 og AP-7 i nærheten.',
  'Exploatörens broschyr anger att småbåtshamnen, stranden Playa Beach och stranden La Rada ligger under tio minuter bort, intill gamla stan, med A-7 och AP-7 i närheten.')
p('.why.points[3][1]',
  'Los documentos no dan fecha de entrega ni calendario de pagos, y el folleto y los planos del sótano no coinciden en el número de plazas de garaje, por lo que lo confirmamos con el promotor antes de cualquier reserva.',
  'Les documents ne donnent ni date de livraison ni échéancier de paiement, et la brochure et les plans des sous-sols ne s’accordent pas sur le nombre de places de parking ; nous le confirmons donc avec le promoteur avant toute réservation.',
  'Die Unterlagen nennen weder einen Übergabetermin noch einen Zahlungsplan, und Prospekt und Untergeschosspläne weichen bei der Zahl der Stellplätze voneinander ab; deshalb klären wir das vor jeder Reservierung mit dem Bauträger.',
  'В документах нет ни срока сдачи, ни графика платежей, а брошюра и планы подземных уровней расходятся в числе парковочных мест, поэтому мы уточняем это у застройщика до любого бронирования.',
  'لا تذكر الوثائق موعد التسليم ولا جدول الدفعات، ويختلف الكتيّب ومخططات الطابقين السفليين في عدد مواقف السيارات، لذلك نؤكد ذلك مع المطوّر قبل أي حجز.',
  'De documenten geven geen opleveringsdatum of betalingsschema, en de brochure en de plattegronden van de kelders zijn het niet eens over het aantal parkeerplaatsen, dus bevestigen wij dit bij de ontwikkelaar vóór elke reservering.',
  'Dokumenty nie podają terminu oddania ani harmonogramu płatności, a broszura i rzuty poziomów podziemnych różnią się liczbą miejsc parkingowych, dlatego potwierdzamy to z deweloperem przed każdą rezerwacją.',
  'Dokumentene oppgir verken overleveringsdato eller betalingsplan, og brosjyren og kjelleretegningene er uenige om antall parkeringsplasser, så vi bekrefter dette med utbyggeren før enhver reservasjon.',
  'Dokumenten anger varken tillträdesdatum eller betalningsplan, och broschyren och källarplanritningarna är oeniga om antalet parkeringsplatser, så vi bekräftar detta med exploatören före varje reservation.')

# 86-92 architecture
p('.architecture.headlineHtml', 'Marcos de tono bronce, <em>terrazas ajardinadas</em>', 'Des cadres de ton bronze, <em>des terrasses plantées</em>',
  'Bronzefarbene Rahmen, <em>bepflanzte Terrassen</em>', 'Рамы бронзового тона, <em>озеленённые террасы</em>',
  'إطارات بلون البرونز، <em>وتراسات مزروعة</em>', 'Bronskleurige kaders, <em>beplante terrassen</em>',
  'Ramy w kolorze brązu, <em>obsadzone tarasy</em>', 'Bronsefargede rammer, <em>beplantede terrasser</em>',
  'Bronsfärgade ramar, <em>planterade terrasser</em>')
p('.architecture.copy[0]',
  'El folleto del promotor describe el diseño como innovador y vanguardista, y eminentemente contemporáneo. En sus imágenes generadas por ordenador, el edificio tiene marcos angulares de tono bronce alrededor de las terrazas de cada planta, antepechos ajardinados y un gran marco alrededor de la cubierta.',
  'La brochure du promoteur décrit le design comme innovant et avant-gardiste, et résolument contemporain. Dans ses images de synthèse, l’immeuble présente des cadres anguleux de ton bronze autour des terrasses de chaque étage, des garde-corps plantés et un grand cadre autour du toit.',
  'Der Prospekt des Bauträgers beschreibt das Design als innovativ und avantgardistisch und ausgesprochen zeitgenössisch. In seinen computergenerierten Bildern hat das Gebäude kantige bronzefarbene Rahmen um die Terrassen auf jedem Geschoss, bepflanzte Brüstungen und einen großen Rahmen um das Dach.',
  'В брошюре застройщика дизайн назван новаторским и авангардным, в высшей степени современным. На его компьютерных визуализациях у здания угловатые рамы бронзового тона вокруг террас на каждом этаже, озеленённые ограждения и большая рама вокруг крыши.',
  'يصف كتيّب المطوّر التصميم بأنه مبتكر ورائد، ومعاصر بامتياز. وفي صوره المُولَّدة بالحاسوب يظهر المبنى بإطارات زاوية بلون البرونز حول التراسات في كل طابق، وأسوار مزروعة، وإطار كبير حول السطح.',
  'De brochure van de ontwikkelaar noemt het ontwerp innovatief en avant-gardistisch, en uitgesproken hedendaags. In de computergegenereerde beelden heeft het gebouw hoekige bronskleurige kaders rond de terrassen op elke verdieping, beplante balustrades en een groot kader rond het dak.',
  'Broszura dewelopera opisuje projekt jako innowacyjny i awangardowy, wyraźnie współczesny. Na jej wizualizacjach komputerowych budynek ma kanciaste ramy w kolorze brązu wokół tarasów na każdym piętrze, obsadzone roślinnością balustrady i dużą ramę wokół dachu.',
  'Utbyggerens brosjyre beskriver designet som nyskapende og avantgardistisk, og utpreget moderne. I de datagenererte bildene har bygningen kantete bronsefargede rammer rundt terrassene i hver etasje, beplantede rekkverk og en stor ramme rundt taket.',
  'Exploatörens broschyr beskriver designen som nyskapande och avantgardistisk, och uttalat modern. I de datorgenererade bilderna har byggnaden kantiga bronsfärgade ramar runt terrasserna på varje våning, planterade räcken och en stor ram runt taket.')
p('.architecture.copy[1]',
  'La memoria de calidades describe una fachada de muro cortina con paños deslizantes y practicables donde el salón y la cocina dan a la terraza, con los perfiles ocultos en el suelo, de modo que la estancia se prolonga hacia el exterior.',
  'Le descriptif de qualité décrit une façade en mur-rideau avec des panneaux coulissants et ouvrants là où le séjour et la cuisine s’ouvrent sur la terrasse, les profilés étant dissimulés dans le sol, si bien que la pièce se prolonge vers l’extérieur.',
  'Die Baubeschreibung nennt eine Vorhangfassade mit Schiebe- und Öffnungselementen dort, wo Wohnzimmer und Küche an die Terrasse grenzen, mit im Boden verborgenen Schienen, sodass der Raum in den Außenbereich übergeht.',
  'В спецификации описан фасад из навесной стеклянной стены с раздвижными и открывающимися панелями там, где гостиная и кухня выходят на террасу; направляющие скрыты в полу, и комнату как будто продолжает пространство снаружи.',
  'تصف المواصفات واجهة جدارية ستارية بألواح منزلقة وقابلة للفتح حيث تلتقي غرفة المعيشة والمطبخ بالتراس، مع إخفاء المجاري في الأرضية، بحيث تمتد الغرفة نحو الخارج.',
  'De specificatie beschrijft een vliesgevel met schuif- en openslaande delen waar de woonkamer en de keuken aan het terras grenzen, met in de vloer verborgen profielen, zodat de ruimte doorloopt naar buiten.',
  'Specyfikacja opisuje elewację kurtynową z przesuwnymi i otwieranymi skrzydłami tam, gdzie salon i kuchnia łączą się z tarasem, z prowadnicami ukrytymi w podłodze, dzięki czemu pomieszczenie przechodzi płynnie na zewnątrz.',
  'Spesifikasjonen beskriver en glassfasade med skyve- og åpningselementer der stuen og kjøkkenet møter terrassen, med skinnene skjult i gulvet, slik at rommet går over i uterommet.',
  'Specifikationen beskriver en glasfasad med skjut- och öppningsbara partier där vardagsrummet och köket möter terrassen, med skenorna dolda i golvet, så att rummet går över i utemiljön.')
p('.architecture.highlights[0][1]',
  'Hormigón armado conforme a la normativa vigente y al Código Técnico de la Edificación, sobre una cimentación diseñada según el estudio geotécnico.',
  'Béton armé conforme à la réglementation en vigueur et au Code technique du bâtiment, sur des fondations conçues d’après l’étude géotechnique.',
  'Stahlbeton nach den geltenden Vorschriften und dem spanischen Bautechnikkodex, auf einem nach dem geotechnischen Gutachten ausgelegten Fundament.',
  'Железобетон в соответствии с действующими нормами и Техническим строительным кодексом, на фундаменте, рассчитанном по геотехническому исследованию.',
  'خرسانة مسلحة وفق الأنظمة السارية والكود الفني للبناء، على أساسات مصممة بحسب الدراسة الجيوتقنية.',
  'Gewapend beton volgens de geldende regelgeving en de Spaanse bouwtechnische code, op een fundering die is ontworpen op basis van het geotechnisch onderzoek.',
  'Żelbet zgodny z obowiązującymi przepisami i Technicznym Kodeksem Budowlanym, na fundamentach zaprojektowanych na podstawie badania geotechnicznego.',
  'Armert betong etter gjeldende regler og den tekniske byggekoden, på et fundament utformet etter den geotekniske undersøkelsen.',
  'Armerad betong enligt gällande regler och den tekniska byggkoden, på en grund som utformats efter den geotekniska undersökningen.')
p('.architecture.highlights[1][1]',
  'Multicapa: muro exterior de ladrillo, aislamiento interior, cámara de aire y trasdosado de placa de yeso laminado, con acabado en vidrio y revestimientos como paneles de aluminio lacado o de GRC, a determinar por la dirección facultativa.',
  'Multicouche : mur extérieur en brique, isolation intérieure, lame d’air et doublage en plaques de plâtre, avec une finition en verre et des revêtements tels que des panneaux d’aluminium laqué ou de GRC, à fixer par la direction de projet.',
  'Mehrschichtig: Außenwand aus Ziegel, Innendämmung, Luftschicht und Gipskartonvorsatzschale, abgeschlossen mit Glas und Verkleidungen wie lackierten Aluminium- oder GRC-Paneelen, die von der Bauleitung festgelegt werden.',
  'Многослойный: наружная кирпичная стена, внутренняя теплоизоляция, воздушная прослойка и гипсокартонная облицовка; отделка стеклом и облицовкой, например панелями из окрашенного алюминия или GRC, которые определит руководство проекта.',
  'متعددة الطبقات: جدار خارجي من الطوب وعزل داخلي وفراغ هوائي وبطانة من ألواح الجبس، بتشطيب من الزجاج وكسوات مثل ألواح الألمنيوم المطلي أو GRC، تحددها إدارة المشروع.',
  'Meerlagig: een buitenmuur van baksteen, isolatie aan de binnenzijde, een luchtspouw en een voorzetwand van gipsplaat, afgewerkt met glas en bekleding zoals gelakte aluminium of GRC-panelen, te bepalen door de bouwleiding.',
  'Wielowarstwowa: zewnętrzna ściana z cegły, ocieplenie od wewnątrz, pustka powietrzna i okładzina z płyt gipsowo-kartonowych, z wykończeniem ze szkła i okładzin, takich jak panele z lakierowanego aluminium lub GRC, do ustalenia przez kierownictwo projektu.',
  'Flerlags: en yttervegg av murstein, innvendig isolasjon, et luftrom og en gipsforkledning, ferdigstilt med glass og kledning som lakkerte aluminiums- eller GRC-paneler, som fastsettes av prosjektledelsen.',
  'Flerskikts: en yttervägg av tegel, invändig isolering, ett luftrum och en gipsbeklädnad, med ytskikt av glas och beklädnad som lackerade aluminium- eller GRC-paneler, som projektledningen bestämmer.')
p('.architecture.highlights[2][1]',
  'Perfiles de aluminio lacado con rotura de puente térmico y doble acristalamiento con tratamiento bajo emisivo y de control solar, y estores motorizados de oscurecimiento en los dormitorios y salones.',
  'Profilés en aluminium laqué à rupture de pont thermique et double vitrage avec traitement à faible émissivité et de contrôle solaire, et stores motorisés occultants dans les chambres et les séjours.',
  'Lackierte Aluminiumprofile mit thermischer Trennung und Doppelverglasung mit Wärmeschutz- und Sonnenschutzbeschichtung sowie motorisierte Verdunkelungsrollos in den Schlafzimmern und Wohnzimmern.',
  'Профили из окрашенного алюминия с терморазрывом и двойное остекление с низкоэмиссионным и солнцезащитным покрытием, а в спальнях и гостиных — моторизованные затемняющие шторы.',
  'إطارات من الألمنيوم المطلي بفاصل حراري وزجاج مزدوج بمعالجة منخفضة الانبعاثية ومعالجة للتحكم في الشمس، وستائر معتمة بمحركات في غرف النوم وغرف المعيشة.',
  'Gelakte aluminium profielen met thermische onderbreking en dubbele beglazing met low-e- en zonwerende coating, en gemotoriseerde verduisterende rolgordijnen in de slaapkamers en woonkamers.',
  'Profile z lakierowanego aluminium z przerwą termiczną i podwójne szyby z powłoką niskoemisyjną i przeciwsłoneczną oraz zmotoryzowane rolety zaciemniające w sypialniach i salonach.',
  'Lakkerte aluminiumsprofiler med termisk brudd og dobbeltvindu med lavemisjons- og solkontrollbehandling, og motoriserte mørkleggingsgardiner i soverom og stuer.',
  'Lackerade aluminiumprofiler med termisk brytning och dubbelglas med lågemissions- och solskyddsbehandling, samt motoriserade mörkläggningsrullgardiner i sovrum och vardagsrum.')
p('.architecture.highlights[3][1]',
  'Cubiertas planas invertidas, impermeabilizadas y aisladas, con grava en las zonas no transitables y solado cerámico antideslizante en las transitables.',
  'Toitures-terrasses inversées, étanchées et isolées, avec du gravier dans les zones non accessibles et un carrelage antidérapant dans les zones accessibles.',
  'Umkehrdächer als Flachdächer, abgedichtet und gedämmt, mit Kies in den nicht begehbaren Bereichen und rutschhemmendem Keramikbelag in den begehbaren.',
  'Инверсионные плоские кровли с гидроизоляцией и утеплением: гравий на неэксплуатируемых участках и нескользящая керамическая плитка на эксплуатируемых.',
  'أسقف مسطحة مقلوبة معزولة مائيًا وحراريًا، بالحصى في المناطق غير المخصصة للمشي وببلاط سيراميك مانع للانزلاق في المناطق المخصصة للمشي.',
  'Omgekeerde platte daken, waterdicht en geïsoleerd, met grind op de niet-begaanbare delen en antislip keramische vloeren op de begaanbare delen.',
  'Odwrócone dachy płaskie, hydroizolowane i ocieplone, ze żwirem w strefach niedostępnych i antypoślizgową płytką ceramiczną w strefach dostępnych.',
  'Omvendte flate tak, vanntettet og isolert, med grus i områdene der ingen går og sklisikre keramiske fliser der de er tilgjengelige.',
  'Omvända platta tak, tätade och isolerade, med grus på de ytor där ingen går och halkfria keramikplattor där de är beträdbara.')

# 93 qualitySpecs.sourceNote and the group names / items
p('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades de los documentos del promotor, que no lleva fecha. Indica que los materiales pueden ser modificados por la dirección facultativa siempre que no se reduzca su calidad, que no tiene carácter contractual y que el mobiliario mostrado en las imágenes no está incluido. Las marcas se citan en ella «o similar».',
  'Source : le descriptif de qualité des documents du promoteur, qui n’est pas daté. Il précise que les matériaux peuvent être modifiés par la direction de projet tant que leur qualité n’est pas réduite, qu’il n’a pas valeur contractuelle et que le mobilier présenté sur les images n’est pas inclus. Les marques y sont citées « ou équivalent ».',
  'Quelle: die Baubeschreibung in den Unterlagen des Bauträgers, die kein Datum trägt. Sie weist darauf hin, dass die Materialien von der Bauleitung geändert werden können, solange ihre Qualität nicht gemindert wird, dass sie nicht vertraglich bindend ist und dass die auf den Bildern gezeigten Möbel nicht enthalten sind. Marken werden darin mit „oder gleichwertig“ genannt.',
  'Источник: спецификация качества в документах застройщика, которая не датирована. В ней сказано, что материалы может изменить руководство проекта, если их качество не снижается, что она не имеет договорной силы и что мебель, показанная на изображениях, не входит в стоимость. Марки названы в ней с оговоркой «или аналог».',
  'المصدر: مواصفات الجودة في وثائق المطوّر، وهي غير مؤرخة. وتذكر أن إدارة المشروع قد تغيّر المواد ما دامت جودتها لا تنخفض، وأنها غير ملزمة تعاقديًا، وأن الأثاث الظاهر في الصور غير مشمول. وتُذكر العلامات التجارية فيها مع عبارة «أو ما يعادلها».',
  'Bron: de kwaliteitsspecificatie in de documenten van de ontwikkelaar, die niet is gedateerd. Daarin staat dat de materialen door de bouwleiding mogen worden gewijzigd zolang hun kwaliteit niet daalt, dat ze niet contractueel is en dat de op de beelden getoonde meubels niet zijn inbegrepen. Merken worden erin genoemd met „of gelijkwaardig”.',
  'Źródło: specyfikacja jakości w dokumentach dewelopera, która nie jest datowana. Podano w niej, że kierownictwo projektu może zmieniać materiały, o ile nie obniża to ich jakości, że nie ma ona charakteru umownego i że meble pokazane na wizualizacjach nie są wliczone w cenę. Marki są w niej podane z dopiskiem „lub równoważne”.',
  'Kilde: kvalitetsspesifikasjonen i utbyggerens dokumenter, som ikke er datert. Den sier at materialene kan endres av prosjektledelsen så lenge kvaliteten ikke reduseres, at den ikke er kontraktsfestet, og at møblene som vises på bildene ikke er inkludert. Merker er nevnt i den med «eller tilsvarende».',
  'Källa: kvalitetsbeskrivningen i exploatörens dokument, som inte är daterad. Den anger att materialen kan ändras av projektledningen så länge kvaliteten inte sänks, att den inte är avtalsgrundande och att de möbler som visas på bilderna inte ingår. Märken nämns i den med ”eller likvärdigt”.')
p('.qualitySpecs.groups[0].name', 'Fachada y acristalamiento', 'Façade et vitrage', 'Fassade und Verglasung', 'Фасад и остекление', 'الواجهة والزجاج',
  'Gevel en beglazing', 'Elewacja i przeszklenia', 'Fasade og vinduer', 'Fasad och glas')
p('.qualitySpecs.groups[0].items[0]',
  'Fachada multicapa de muro exterior de ladrillo, aislamiento interior, cámara de aire y trasdosado de placa de yeso laminado, con acabado en vidrio y revestimientos como paneles de aluminio lacado o de GRC.',
  'Façade multicouche composée d’un mur extérieur en brique, d’une isolation intérieure, d’une lame d’air et d’un doublage en plaques de plâtre, avec une finition en verre et des revêtements tels que des panneaux d’aluminium laqué ou de GRC.',
  'Mehrschichtige Fassade aus Außenwand aus Ziegel, Innendämmung, Luftschicht und Gipskartonvorsatzschale, abgeschlossen mit Glas und Verkleidungen wie lackierten Aluminium- oder GRC-Paneelen.',
  'Многослойный фасад: наружная кирпичная стена, внутренняя теплоизоляция, воздушная прослойка и гипсокартонная облицовка; отделка стеклом и облицовкой, например панелями из окрашенного алюминия или GRC.',
  'واجهة متعددة الطبقات من جدار خارجي من الطوب وعزل داخلي وفراغ هوائي وبطانة من ألواح الجبس، بتشطيب من الزجاج وكسوات مثل ألواح الألمنيوم المطلي أو GRC.',
  'Een meerlaagse gevel van een buitenmuur van baksteen, isolatie aan de binnenzijde, een luchtspouw en een voorzetwand van gipsplaat, afgewerkt met glas en bekleding zoals gelakte aluminium of GRC-panelen.',
  'Wielowarstwowa elewacja: zewnętrzna ściana z cegły, ocieplenie od wewnątrz, pustka powietrzna i okładzina z płyt gipsowo-kartonowych, z wykończeniem ze szkła i okładzin, takich jak panele z lakierowanego aluminium lub GRC.',
  'En flerlags fasade med yttervegg av murstein, innvendig isolasjon, et luftrom og en gipsforkledning, ferdigstilt med glass og kledning som lakkerte aluminiums- eller GRC-paneler.',
  'En flerskiktsfasad med yttervägg av tegel, invändig isolering, ett luftrum och en gipsbeklädnad, med ytskikt av glas och beklädnad som lackerade aluminium- eller GRC-paneler.')
p('.qualitySpecs.groups[0].items[1]',
  'Muro cortina de aluminio lacado con rotura de puente térmico y doble acristalamiento tipo Climalit con tratamiento bajo emisivo y de control solar, con paños deslizantes y practicables hacia las terrazas y estores motorizados de oscurecimiento en dormitorios y salones.',
  'Mur-rideau en aluminium laqué à rupture de pont thermique et double vitrage de type Climalit avec traitement à faible émissivité et de contrôle solaire, avec des panneaux coulissants et ouvrants vers les terrasses et des stores motorisés occultants dans les chambres et les séjours.',
  'Vorhangfassade aus lackiertem Aluminium mit thermischer Trennung und Doppelverglasung nach Art von Climalit mit Wärmeschutz- und Sonnenschutzbeschichtung, mit Schiebe- und Öffnungselementen zu den Terrassen und motorisierten Verdunkelungsrollos in den Schlafzimmern und Wohnzimmern.',
  'Навесная стена из окрашенного алюминия с терморазрывом и двойное остекление типа Climalit с низкоэмиссионным и солнцезащитным покрытием, с раздвижными и открывающимися панелями к террасам и моторизованными затемняющими шторами в спальнях и гостиных.',
  'جدار ستاري من الألمنيوم المطلي بفاصل حراري وزجاج مزدوج من نوع Climalit بمعالجة منخفضة الانبعاثية ومعالجة للتحكم في الشمس، مع ألواح منزلقة وقابلة للفتح نحو التراسات وستائر معتمة بمحركات في غرف النوم وغرف المعيشة.',
  'Een vliesgevel van gelakt aluminium met thermische onderbreking en dubbele beglazing van het type Climalit met low-e- en zonwerende coating, met schuif- en openslaande delen naar de terrassen en gemotoriseerde verduisterende rolgordijnen in de slaapkamers en woonkamers.',
  'Elewacja kurtynowa z lakierowanego aluminium z przerwą termiczną i podwójne szyby typu Climalit z powłoką niskoemisyjną i przeciwsłoneczną, z przesuwnymi i otwieranymi skrzydłami do tarasów oraz zmotoryzowanymi roletami zaciemniającymi w sypialniach i salonach.',
  'Glassfasade i lakkert aluminium med termisk brudd og dobbeltvindu av typen Climalit med lavemisjons- og solkontrollbehandling, med skyve- og åpningselementer mot terrassene og motoriserte mørkleggingsgardiner i soverom og stuer.',
  'Glasfasad i lackerat aluminium med termisk brytning och dubbelglas av typen Climalit med lågemissions- och solskyddsbehandling, med skjut- och öppningsbara partier mot terrasserna och motoriserade mörkläggningsrullgardiner i sovrum och vardagsrum.')
p('.qualitySpecs.groups[1].items[0]',
  'Tabiquería interior de la vivienda de placas de yeso laminado sobre perfilería metálica con aislamiento de lana mineral, y placas de yeso laminado hidrófugas en las zonas húmedas.',
  'Cloisons intérieures du logement en plaques de plâtre sur ossature métallique avec isolation en laine minérale, et plaques de plâtre hydrofuges dans les pièces humides.',
  'Trennwände innerhalb der Wohnung aus Gipskarton auf Metallprofilen mit Mineralwolldämmung sowie wasserabweisende Gipskartonplatten in den Feuchträumen.',
  'Внутренние перегородки в квартире из гипсокартона на металлическом каркасе с минераловатной изоляцией, а во влажных помещениях — влагостойкий гипсокартон.',
  'قواطع داخلية في المسكن من ألواح الجبس على هيكل معدني مع عزل بالصوف المعدني، وألواح جبس مقاومة للماء في المناطق الرطبة.',
  'Binnenwanden in de woning van gipsplaat op een metalen frame met isolatie van minerale wol, en waterafstotende gipsplaat in de natte ruimten.',
  'Przegrody wewnętrzne w mieszkaniu z płyt gipsowo-kartonowych na stelażu metalowym z izolacją z wełny mineralnej oraz wodoodporne płyty gipsowo-kartonowe w pomieszczeniach mokrych.',
  'Skillevegger inne i boligen av gipsplater på metallprofiler med mineralullisolasjon, og vannavvisende gipsplater i våtrommene.',
  'Mellanväggar inne i bostaden av gipsskivor på metallreglar med mineralullsisolering, och fuktbeständiga gipsskivor i de våta utrymmena.')
p('.qualitySpecs.groups[1].items[1]',
  'Entre las viviendas y las zonas comunes, una hoja de ladrillo perforado con trasdosado autoportante de placa de yeso laminado y aislamiento térmico y acústico con lámina antiimpacto.',
  'Entre les logements et les parties communes, une paroi en brique perforée avec un doublage autoportant en plaques de plâtre et une isolation thermique et acoustique avec une membrane anti-impact.',
  'Zwischen den Wohnungen und den Gemeinschaftsbereichen eine Lage perforierter Ziegel mit selbsttragender Gipskartonvorsatzschale sowie Wärme- und Schalldämmung mit Trittschallschutzlage.',
  'Между квартирами и общими зонами — слой перфорированного кирпича с самонесущей гипсокартонной облицовкой, тепло- и звукоизоляцией и противоударной мембраной.',
  'بين المساكن والمرافق المشتركة طبقة من الطوب المثقب مع بطانة ذاتية الحمل من ألواح الجبس وعزل حراري وصوتي بطبقة مضادة للصدمات.',
  'Tussen de woningen en de gemeenschappelijke ruimten een laag geperforeerde baksteen met een zelfdragende voorzetwand van gipsplaat en thermische en akoestische isolatie met een anti-impactlaag.',
  'Między mieszkaniami a częściami wspólnymi warstwa cegły dziurawki z samonośną okładziną z płyt gipsowo-kartonowych oraz izolacją termiczną i akustyczną z membraną przeciwuderzeniową.',
  'Mellom boligene og fellesarealene et lag perforert murstein med selvbærende gipsforkledning og termisk og akustisk isolasjon med et slagdempende lag.',
  'Mellan bostäderna och de gemensamma ytorna ett skikt av hålstegel med självbärande gipsbeklädnad och termisk och akustisk isolering med ett stegljudsskikt.')
p('.qualitySpecs.groups[2].items[0]',
  'Suelos de gres porcelánico rectificado de formato 120 x 120 cm de PORCELANOSA o similar en las estancias, los baños y, con acabado antideslizante, en las terrazas, con rodapié de madera a juego con las puertas.',
  'Sols en grès cérame rectifié au format 120 x 120 cm de PORCELANOSA ou équivalent dans les pièces, les salles de bain et, avec une finition antidérapante, sur les terrasses, avec des plinthes en bois assorties aux portes.',
  'Böden aus rektifiziertem Feinsteinzeug im Format 120 x 120 cm von PORCELANOSA oder gleichwertig in den Räumen, den Bädern und, mit rutschhemmender Oberfläche, auf den Terrassen, mit Holzsockelleisten passend zu den Türen.',
  'Полы из ректифицированного керамогранита форматом 120 x 120 см от PORCELANOSA или аналогичного бренда в комнатах, ванных и, с нескользящей поверхностью, на террасах, с деревянными плинтусами в тон дверям.',
  'أرضيات من البورسلين المصقول بقياس 120 × 120 سم من PORCELANOSA أو ما يعادلها في الغرف والحمامات، وبتشطيب مانع للانزلاق على التراسات، مع وزرات خشبية تناسب الأبواب.',
  'Vloeren van gerectificeerd porseleinen steengoed in het formaat 120 x 120 cm van PORCELANOSA of gelijkwaardig in de vertrekken, de badkamers en, met een antislipafwerking, op de terrassen, met houten plinten passend bij de deuren.',
  'Podłogi z gresu porcelanowego szlifowanego o formacie 120 x 120 cm marki PORCELANOSA lub równoważnej w pomieszczeniach, łazienkach i, w wykończeniu antypoślizgowym, na tarasach, z drewnianymi listwami przypodłogowymi dopasowanymi do drzwi.',
  'Gulv av rektifisert porselensfliser i formatet 120 x 120 cm fra PORCELANOSA eller tilsvarende i rommene, badene og, med sklisikker overflate, på terrassene, med tregulvlister som matcher dørene.',
  'Golv av rektifierat porslinsgods i formatet 120 x 120 cm från PORCELANOSA eller likvärdigt i rummen, badrummen och, med halkfri yta, på terrasserna, med golvlister i trä som matchar dörrarna.')
p('.qualitySpecs.groups[2].items[1]',
  'Puerta de entrada blindada con cerradura de tres puntos y cerradura inteligente, puertas interiores de suelo a techo lacadas y sin tapetas, y armarios empotrados lacados con balda maletero y barra de colgar. Algunas paredes se revisten de panelado de madera con varios acabados a elegir.',
  'Porte d’entrée blindée avec serrure trois points et serrure connectée, portes intérieures laquées sur toute la hauteur et sans chambranles, et placards intégrés laqués avec tablette et barre de penderie. Certains murs sont habillés de panneaux de bois avec un choix de finitions.',
  'Gepanzerte Wohnungstür mit Dreipunktverriegelung und Smart-Lock, raumhohe lackierte Innentüren ohne Zargen und eingebaute lackierte Schränke mit Hutablage und Kleiderstange. Einige Wände sind mit Holzpaneelen in verschiedenen Ausführungen verkleidet.',
  'Бронированная входная дверь с трёхточечным замком и умным замком, окрашенные межкомнатные двери в полный рост без наличников и встроенные окрашенные шкафы с полкой для чемоданов и штангой. Некоторые стены облицованы деревянными панелями на выбор.',
  'باب دخول مصفح بقفل ثلاثي النقاط وقفل ذكي، وأبواب داخلية مطلية بارتفاع كامل بلا إطارات، وخزائن مدمجة مطلية برف للحقائب وعمود تعليق. وتُكسى بعض الجدران بألواح خشبية بتشطيبات متعددة للاختيار.',
  'Een pantserdeur met driepuntssluiting en een slim slot, volledig hoge gelakte binnendeuren zonder kozijnbekleding en ingebouwde gelakte kasten met een koffertablet en een kledingstang. Sommige wanden zijn bekleed met houten panelen in verschillende afwerkingen.',
  'Drzwi wejściowe antywłamaniowe z zamkiem trzypunktowym i zamkiem inteligentnym, lakierowane drzwi wewnętrzne na całą wysokość bez obudowy oraz zabudowane szafy lakierowane z półką na walizki i drążkiem. Niektóre ściany są wykończone drewnianymi panelami do wyboru.',
  'En pansret inngangsdør med trepunktslås og smartlås, høye lakkerte innerdører uten karmer og innebygde lakkerte skap med kofferthylle og kleshengerstang. Noen vegger er kledd med treplater i flere utførelser.',
  'En pansrad ytterdörr med trepunktslås och smart lås, hela lackerade innerdörrar utan foder och inbyggda lackerade garderober med resväskshylla och klädstång. Vissa väggar är klädda med träpaneler i flera utföranden.')
p('.qualitySpecs.groups[3].items[0]',
  'Cocina entregada totalmente amueblada, con muebles de laminado de alta presión, encimera y frente en cuarzo compacto SILESTONE o porcelánico, isla central con encimera de porcelánico o CORIAN y grifo extraíble GROHE o similar.',
  'Cuisine livrée entièrement meublée, avec des meubles en stratifié haute pression, un plan de travail et une crédence en quartz compact SILESTONE ou en grès cérame, un îlot central avec un plan en grès cérame ou en CORIAN et un robinet extractible GROHE ou équivalent.',
  'Vollständig möblierte Küche mit Hochdrucklaminat-Schränken, Arbeitsplatte und Rückwand aus Kompaktquarz von SILESTONE oder Feinsteinzeug, einer Kücheninsel mit Platte aus Feinsteinzeug oder CORIAN und ausziehbarer Armatur von GROHE oder gleichwertig.',
  'Полностью меблированная кухня: шкафы из ламината высокого давления, столешница и фартук из компактного кварца SILESTONE или керамогранита, центральный остров со столешницей из керамогранита или CORIAN и выдвижной смеситель GROHE или аналогичный.',
  'مطبخ يُسلَّم مؤثثاً بالكامل، بخزائن من اللامينيت عالي الضغط، وسطح عمل وواجهة من الكوارتز المضغوط SILESTONE أو البورسلين، وجزيرة مركزية بسطح من البورسلين أو CORIAN وخلاط سحب من GROHE أو ما يعادله.',
  'Een volledig gemeubileerde keuken met kasten van hogedruklaminaat, een werkblad en achterwand van compact kwarts van SILESTONE of porseleinen steengoed, een centraal eiland met een blad van porselein of CORIAN en een uittrekbare kraan van GROHE of gelijkwaardig.',
  'W pełni umeblowana kuchnia z szafkami z laminatu wysokociśnieniowego, blatem i panelem ściennym z kwarcu kompaktowego SILESTONE lub gresu, centralną wyspą z blatem z gresu lub CORIAN oraz wyciąganą baterią GROHE lub równoważną.',
  'Et fullt møblert kjøkken med skap i høytrykkslaminat, benkeplate og sprutsone i kompaktkvarts fra SILESTONE eller porselensfliser, en sentral øy med topp i porselen eller CORIAN og en uttrekkbar kran fra GROHE eller tilsvarende.',
  'Ett helt möblerat kök med skåp i högtryckslaminat, bänkskiva och stänkskydd i kompaktkvarts från SILESTONE eller porslinsgods, en central ö med skiva i porslin eller CORIAN och en utdragbar kran från GROHE eller likvärdig.')
p('.qualitySpecs.groups[3].items[1]',
  'Electrodomésticos GAGGENAU o similares: horno, placa de inducción con campana integrada, lavavajillas, frigorífico y vinoteca, y una zona de lavandería con lavadora, secadora y centro de planchado.',
  'Électroménager GAGGENAU ou équivalent : four, plaque à induction avec hotte intégrée, lave-vaisselle, réfrigérateur et cave à vin, ainsi qu’un coin buanderie avec lave-linge, sèche-linge et centre de repassage.',
  'Geräte von GAGGENAU oder gleichwertig: Backofen, Induktionskochfeld mit integriertem Dunstabzug, Geschirrspüler, Kühlschrank und Weinkühlschrank sowie ein Hauswirtschaftsbereich mit Waschmaschine, Wäschetrockner und Bügelstation.',
  'Техника GAGGENAU или аналогичная: духовой шкаф, индукционная варочная панель со встроенной вытяжкой, посудомоечная машина, холодильник и винный шкаф, а также зона прачечной со стиральной и сушильной машинами и гладильным центром.',
  'أجهزة GAGGENAU أو ما يعادلها: فرن وموقد حثي بشفاط مدمج وغسالة أطباق وثلاجة وثلاجة نبيذ، ومنطقة غسيل بغسالة ونشافة ومركز كي.',
  'Apparatuur van GAGGENAU of gelijkwaardig: een oven, een inductiekookplaat met geïntegreerde afzuigkap, een vaatwasser, een koelkast en een wijnklimaatkast, en een wasruimte met een wasmachine, een droger en een strijkcentrum.',
  'Sprzęt GAGGENAU lub równoważny: piekarnik, płyta indukcyjna z wbudowanym okapem, zmywarka, lodówka i chłodziarka do wina oraz pralnia z pralką, suszarką i centrum prasowania.',
  'Hvitevarer fra GAGGENAU eller tilsvarende: en ovn, en induksjonstopp med integrert ventilator, en oppvaskmaskin, et kjøleskap og et vinskap, og et vaskeområde med vaskemaskin, tørketrommel og strykestasjon.',
  'Vitvaror från GAGGENAU eller likvärdiga: en ugn, en induktionshäll med integrerad fläkt, en diskmaskin, ett kylskåp och ett vinskåp, samt en tvättyta med tvättmaskin, torktumlare och strykstation.')
p('.qualitySpecs.groups[4].items[0]',
  'Suelo radiante eléctrico en el baño principal y en el segundo baño, lavabo continuo de cuarzo compacto, porcelánico o Corian con mueble suspendido, y platos de ducha de perfil bajo con mamparas de cristal.',
  'Plancher chauffant électrique dans la salle de bain principale et la seconde salle de bain, vasque continue en quartz compact, en grès cérame ou en Corian avec meuble suspendu, et receveurs de douche extra-plats avec parois de verre.',
  'Elektrische Fußbodenheizung im Hauptbad und im zweiten Bad, durchgehender Waschtisch aus Kompaktquarz, Feinsteinzeug oder Corian mit wandhängendem Unterschrank sowie flache Duschwannen mit Glaswänden.',
  'Электрический тёплый пол в главной и во второй ванной, сплошная столешница с раковиной из компактного кварца, керамогранита или Corian с подвесной тумбой и плоские душевые поддоны со стеклянными ограждениями.',
  'تدفئة كهربائية تحت الأرضية في الحمام الرئيسي والحمام الثاني، ومغسلة متصلة من الكوارتز المضغوط أو البورسلين أو Corian مع وحدة معلقة، وأحواض دش منخفضة بحواجز زجاجية.',
  'Elektrische vloerverwarming in de hoofdbadkamer en de tweede badkamer, een doorlopende wastafel van compact kwarts, porselein of Corian met een hangend meubel, en lage douchebakken met glazen wanden.',
  'Elektryczne ogrzewanie podłogowe w łazience głównej i drugiej, ciągła umywalka z kwarcu kompaktowego, gresu lub Corianu z wiszącą szafką oraz niskie brodziki z szklanymi parawanami.',
  'Elektrisk gulvvarme på hovedbadet og det andre badet, en gjennomgående servant i kompaktkvarts, porselen eller Corian med veggmontert underskap, og lave dusjkar med glassvegger.',
  'Elektrisk golvvärme i huvudbadrummet och det andra badrummet, ett genomgående tvättställ i kompaktkvarts, porslin eller Corian med väggmonterat underskåp samt låga duschkar med glasväggar.')
p('.qualitySpecs.groups[4].items[1]',
  'Grifería de ducha termostática empotrada GROHE o similar con barra deslizante y rociador de mano, revestimientos de gran formato rectificados de PORCELANOSA o similar combinados con microcemento, y techos de acabado moteado.',
  'Robinetterie de douche thermostatique encastrée GROHE ou équivalente avec barre coulissante et douchette, revêtements muraux grand format rectifiés de PORCELANOSA ou équivalent associés à du microciment, et plafonds à finition texturée.',
  'Wandmontierte thermostatische Duscharmaturen von GROHE oder gleichwertig mit Gleitstange und Handbrause, großformatige rektifizierte Wandfliesen von PORCELANOSA oder gleichwertig in Kombination mit Mikrozement sowie Decken mit strukturierter Oberfläche.',
  'Встроенная термостатическая душевая арматура GROHE или аналогичная со скользящей штангой и ручной лейкой, крупноформатная ректифицированная настенная плитка PORCELANOSA или аналогичная в сочетании с микроцементом и потолки с фактурной отделкой.',
  'خلاطات دش حرارية مدمجة من GROHE أو ما يعادلها بعمود منزلق ورشاش يدوي، وبلاط جدران كبير الحجم مصقول من PORCELANOSA أو ما يعادله مع الأسمنت الدقيق، وأسقف بتشطيب منقوش.',
  'Thermostatische inbouwdouchekranen van GROHE of gelijkwaardig met een glijstang en een handdouche, groot formaat gerectificeerde wandtegels van PORCELANOSA of gelijkwaardig gecombineerd met microcement, en plafonds met een gestructureerde afwerking.',
  'Podtynkowe baterie prysznicowe termostatyczne GROHE lub równoważne z drążkiem przesuwnym i słuchawką ręczną, wielkoformatowe szlifowane płytki ścienne PORCELANOSA lub równoważne w połączeniu z mikrocementem oraz sufity o fakturowanym wykończeniu.',
  'Termostatiske innfelte dusjarmaturer fra GROHE eller tilsvarende med glidestang og hånddusj, storformat rektifiserte veggfliser fra PORCELANOSA eller tilsvarende kombinert med mikrosement, og tak med strukturert overflate.',
  'Termostatiska inbyggda duschblandare från GROHE eller likvärdiga med glidstång och handdusch, storformatiga rektifierade väggplattor från PORCELANOSA eller likvärdiga i kombination med mikrocement samt tak med strukturerad yta.')
p('.qualitySpecs.groups[5].items[0]',
  'Agua caliente sanitaria mediante bomba de calor aerotérmica en cada vivienda.',
  'Eau chaude sanitaire par pompe à chaleur aérothermique dans chaque logement.',
  'Warmwasser über eine aerothermische Wärmepumpe in jeder Wohnung.',
  'Горячая вода от аэротермального теплового насоса в каждой квартире.',
  'ماء ساخن في كل مسكن من مضخة حرارية هوائية.',
  'Warm water via een aerothermische warmtepomp in elke woning.',
  'Ciepła woda użytkowa z aerotermalnej pompy ciepła w każdym mieszkaniu.',
  'Varmtvann fra en aerotermisk varmepumpe i hver bolig.',
  'Varmvatten från en aerotermisk värmepump i varje bostad.')
p('.qualitySpecs.groups[5].items[1]',
  'Aire acondicionado y calefacción mediante bomba de calor por expansión directa, con conductos en el falso techo y rejillas en el salón, la cocina y los dormitorios, y un termostato en el salón y en cada dormitorio con zonificación Airzone.',
  'Climatisation et chauffage par pompe à chaleur à détente directe, avec des gaines dans le faux plafond et des grilles dans le séjour, la cuisine et les chambres, et un thermostat dans le séjour et dans chaque chambre avec zonage Airzone.',
  'Klimatisierung und Heizung über eine Direktexpansions-Wärmepumpe, mit Kanälen in der Zwischendecke und Gittern im Wohnzimmer, in der Küche und in den Schlafzimmern sowie einem Thermostat im Wohnzimmer und in jedem Schlafzimmer mit Airzone-Zonensteuerung.',
  'Кондиционирование и отопление тепловым насосом прямого расширения: воздуховоды в подвесном потолке и решётки в гостиной, кухне и спальнях, термостат в гостиной и в каждой спальне с зонированием Airzone.',
  'تكييف وتدفئة بمضخة حرارية بالتمدد المباشر، عبر مجارٍ في السقف المستعار وشبكات في غرفة المعيشة والمطبخ وغرف النوم، مع ثرموستات في غرفة المعيشة وفي كل غرفة نوم بنظام تقسيم Airzone.',
  'Airconditioning en verwarming met een directe-expansiewarmtepomp, via kanalen in het verlaagde plafond met roosters in de woonkamer, de keuken en de slaapkamers, en een thermostaat in de woonkamer en in elke slaapkamer met Airzone-zonering.',
  'Klimatyzacja i ogrzewanie pompą ciepła z bezpośrednim odparowaniem, z kanałami w suficie podwieszanym i kratkami w salonie, kuchni i sypialniach oraz termostatem w salonie i w każdej sypialni ze strefowaniem Airzone.',
  'Klimaanlegg og oppvarming med en varmepumpe med direkte ekspansjon, gjennom kanaler i det nedsenkede taket med ventiler i stuen, på kjøkkenet og i soverommene, og en termostat i stuen og i hvert soverom med Airzone-soner.',
  'Luftkonditionering och uppvärmning med en värmepump med direktexpansion, genom kanaler i det nedsänkta taket med galler i vardagsrummet, köket och sovrummen, och en termostat i vardagsrummet och i varje sovrum med Airzone-zonindelning.')
p('.qualitySpecs.groups[6].items[0]',
  'Un grado de electrificación elevado, tomas de TV, radio y teléfono en los salones, las cocinas y los dormitorios, videoportero automático a color y luminarias LED empotradas en cocinas, pasillos y baños.',
  'Un niveau d’électrification élevé, des prises TV, radio et téléphone dans les séjours, les cuisines et les chambres, un visiophone couleur automatique et des spots LED encastrés dans les cuisines, les couloirs et les salles de bain.',
  'Eine hohe Elektroausstattung, TV-, Radio- und Telefonanschlüsse in den Wohnzimmern, Küchen und Schlafzimmern, eine automatische Farb-Videosprechanlage sowie LED-Einbauleuchten in den Küchen, Fluren und Bädern.',
  'Повышенная электрификация, розетки для ТВ, радио и телефона в гостиных, кухнях и спальнях, цветной видеодомофон и встроенные светодиодные светильники на кухнях, в коридорах и ванных.',
  'تجهيز كهربائي مرتفع، ومآخذ للتلفزيون والراديو والهاتف في غرف المعيشة والمطابخ وغرف النوم، وجهاز اتصال مرئي ملوّن، وإضاءة LED غائرة في المطابخ والممرات والحمامات.',
  'Een hoge elektrische uitrusting, tv-, radio- en telefoonaansluitingen in de woonkamers, keukens en slaapkamers, een kleurenvideofoon en ingebouwde led-spots in de keukens, gangen en badkamers.',
  'Podwyższony standard instalacji elektrycznej, gniazda TV, radiowe i telefoniczne w salonach, kuchniach i sypialniach, kolorowy wideodomofon oraz wpuszczane oprawy LED w kuchniach, korytarzach i łazienkach.',
  'Høy elektrisk standard, TV-, radio- og telefonuttak i stuene, på kjøkkenene og i soverommene, en automatisk fargevideotelefon og innfelte LED-lys på kjøkken, i ganger og på bad.',
  'Hög elstandard, TV-, radio- och telefonuttag i vardagsrummen, köken och sovrummen, en automatisk färgvideotelefon och infällda LED-spotlights i kök, korridorer och badrum.')
p('.qualitySpecs.groups[6].items[1]',
  'Iluminación LED, un enchufe y una toma de agua en las terrazas, los solariums de la cubierta y los jardines de planta baja.',
  'Éclairage LED, une prise électrique et un point d’eau sur les terrasses, les solariums en toiture et les jardins du rez-de-chaussée.',
  'LED-Beleuchtung, eine Steckdose und ein Wasseranschluss auf den Terrassen, den Dachsolarien und den Gärten im Erdgeschoss.',
  'Светодиодное освещение, розетка и точка подачи воды на террасах, в солярии на крыше и в садах на первом этаже.',
  'إضاءة LED ومأخذ كهرباء ومأخذ ماء في التراسات وسولاريوم السطح وحدائق الطابق الأرضي.',
  'Ledverlichting, een stopcontact en een wateraansluiting op de terrassen, de daksolariums en de tuinen op de begane grond.',
  'Oświetlenie LED, gniazdo elektryczne i punkt poboru wody na tarasach, solariach na dachu i w ogrodach na parterze.',
  'LED-belysning, en stikkontakt og et vannuttak på terrassene, solterrassene på taket og hagene i første etasje.',
  'LED-belysning, ett eluttag och ett vattenuttag på terrasserna, solterrasserna på taket och trädgårdarna på bottenvåningen.')
p('.qualitySpecs.groups[7].name', 'Terrazas, jardines y solariums', 'Terrasses, jardins et solariums', 'Terrassen, Gärten und Solarien',
  'Террасы, сады и солярии', 'التراسات والحدائق والسولاريوم', 'Terrassen, tuinen en solariums', 'Tarasy, ogrody i solaria',
  'Terrasser, hager og solterrasser', 'Terrasser, trädgårdar och solterrasser')
p('.qualitySpecs.groups[7].items[0]',
  'Piscinas privadas de obra en algunas terrazas, revestidas de piedra natural, con iluminación LED exterior y características propias de cada vivienda, y duchas exteriores en los jardines y los solariums.',
  'Piscines privées maçonnées sur certaines terrasses, revêtues de pierre naturelle, avec éclairage LED extérieur et des caractéristiques propres à chaque logement, et douches extérieures dans les jardins et les solariums.',
  'Private gemauerte Pools auf einigen Terrassen, mit Naturstein verkleidet, mit LED-Außenbeleuchtung und je nach Wohnung eigenen Merkmalen, sowie Außenduschen in den Gärten und Solarien.',
  'Частные бассейны на некоторых террасах, облицованные натуральным камнем, с наружной светодиодной подсветкой и индивидуальными особенностями для каждой квартиры, а также уличные души в садах и солярии.',
  'مسابح خاصة مبنية في بعض التراسات، مكسوة بالحجر الطبيعي بإضاءة LED خارجية وخصائص تخص كل مسكن، ودشّات خارجية في الحدائق والسولاريوم.',
  'Privézwembaden van metselwerk op sommige terrassen, bekleed met natuursteen, met led-buitenverlichting en eigen kenmerken per woning, en buitendouches in de tuinen en solariums.',
  'Prywatne baseny murowane na niektórych tarasach, wyłożone kamieniem naturalnym, z zewnętrznym oświetleniem LED i cechami indywidualnymi dla każdego mieszkania, oraz prysznice zewnętrzne w ogrodach i solariach.',
  'Private bassenger av mur på noen terrasser, kledd med naturstein, med LED-belysning utendørs og egne kjennetegn for hver bolig, og utendørsdusjer i hagene og på solterrassene.',
  'Privata murade pooler på vissa terrasser, klädda med natursten, med LED-belysning utomhus och egna kännetecken för varje bostad, och utomhusduschar i trädgårdarna och på solterrasserna.')
p('.qualitySpecs.groups[7].items[1]',
  'Jardines y terrazas pavimentados con gres porcelánico exterior y plantados con césped natural y sistema de riego integrado.',
  'Jardins et terrasses dallés en grès cérame d’extérieur et plantés de gazon naturel avec un système d’arrosage intégré.',
  'Gärten und Terrassen mit Außen-Feinsteinzeug gepflastert und mit Naturrasen und integrierter Bewässerungsanlage bepflanzt.',
  'Сады и террасы с покрытием из уличного керамогранита и натуральным газоном со встроенной системой полива.',
  'حدائق وتراسات مرصوفة ببورسلين خارجي ومزروعة بعشب طبيعي مع نظام ري مدمج.',
  'Tuinen en terrassen bestraat met buitenporselein en beplant met natuurlijk gras en een geïntegreerd bewateringssysteem.',
  'Ogrody i tarasy wyłożone gresem zewnętrznym i obsiane naturalną trawą z wbudowanym systemem nawadniania.',
  'Hager og terrasser belagt med utendørs porselensfliser og beplantet med naturlig gress og et integrert vanningssystem.',
  'Trädgårdar och terrasser belagda med utomhusporslinsgods och planterade med naturlig gräsmatta och ett integrerat bevattningssystem.')
p('.qualitySpecs.groups[8].name', 'Zonas comunes, garaje y ascensores', 'Parties communes, garage et ascenseurs', 'Gemeinschaftsbereiche, Garage und Aufzüge',
  'Общие зоны, гараж и лифты', 'المرافق المشتركة والمرآب والمصاعد', 'Gemeenschappelijke ruimten, garage en liften',
  'Części wspólne, garaż i windy', 'Fellesarealer, garasje og heiser', 'Gemensamma ytor, garage och hissar')
p('.qualitySpecs.groups[8].items[0]',
  'Piscina comunitaria con iluminación nocturna, zonas ajardinadas con vegetación autóctona de bajo consumo de agua y riego por goteo automático, un solárium, un gimnasio totalmente equipado, un spa con sauna, un club social y un espacio de coworking.',
  'Piscine commune avec éclairage nocturne, espaces paysagers avec une végétation locale peu gourmande en eau et un arrosage goutte à goutte automatique, un solarium, une salle de sport entièrement équipée, un spa avec sauna, un club social et un espace de coworking.',
  'Gemeinschaftspool mit Nachtbeleuchtung, Grünflächen mit heimischer, wassersparender Bepflanzung und automatischer Tropfbewässerung, ein Solarium, ein voll ausgestatteter Fitnessraum, ein Spa mit Sauna, ein Social Club und ein Coworking-Bereich.',
  'Общий бассейн с ночной подсветкой, озеленённые территории с местными растениями, не требующими много воды, и автоматическим капельным поливом, солярий, полностью оборудованный тренажёрный зал, спа с сауной, клуб для жителей и коворкинг.',
  'مسبح مشترك بإضاءة ليلية، ومساحات خضراء بنباتات محلية قليلة استهلاك المياه وري بالتنقيط الآلي، وسولاريوم، وصالة رياضية مجهزة بالكامل، وسبا بساونا، ونادٍ اجتماعي، ومساحة عمل مشتركة.',
  'Een gemeenschappelijk zwembad met nachtverlichting, groene zones met inheemse, waterzuinige beplanting en automatische druppelirrigatie, een solarium, een volledig uitgeruste fitnessruimte, een spa met sauna, een sociale club en een coworkingruimte.',
  'Wspólny basen z oświetleniem nocnym, tereny zieleni z rodzimą roślinnością o niskim zużyciu wody i automatycznym nawadnianiem kroplowym, solarium, w pełni wyposażona siłownia, spa z sauną, klub dla mieszkańców i przestrzeń coworkingowa.',
  'Et felles basseng med nattbelysning, grøntområder med stedegen, vannsparende beplantning og automatisk dryppvanning, en solterrasse, et fullt utstyrt treningsrom, et spa med badstue, en sosial klubb og et coworking-areal.',
  'En gemensam pool med kvällsbelysning, grönområden med inhemsk, vattensnål planterad växtlighet och automatisk droppbevattning, en solterrass, ett fullt utrustat gym, ett spa med bastu, en social klubb och en coworkingyta.')
p('.qualitySpecs.groups[8].items[1]',
  'Portales con suelos de piedra, cerámica o piedra artificial de gran formato y detectores de presencia con temporizador en la iluminación de portales, escaleras y vestíbulos de planta.',
  'Halls d’entrée avec sols en pierre, en céramique ou en pierre artificielle grand format et détecteurs de présence avec minuterie sur l’éclairage des halls, des escaliers et des paliers.',
  'Eingangshallen mit Böden aus Stein, Keramik oder großformatigem Kunststein und Präsenzmeldern mit Zeitschaltung für die Beleuchtung von Eingangshallen, Treppen und Fluren.',
  'Входные холлы с полами из камня, керамики или крупноформатного искусственного камня и датчики присутствия с таймером в освещении холлов, лестниц и площадок.',
  'مداخل بأرضيات من الحجر أو السيراميك أو الحجر الاصطناعي كبير الحجم، وكاشفات حضور بمؤقت في إضاءة المداخل والسلالم وردهات الطوابق.',
  'Entreehallen met vloeren van natuursteen, keramiek of grootformaat kunststeen en aanwezigheidsmelders met timer op de verlichting van hallen, trappen en overlopen.',
  'Holy wejściowe z podłogami z kamienia, ceramiki lub wielkoformatowego kamienia sztucznego oraz czujniki obecności z timerem w oświetleniu holi, klatek schodowych i korytarzy.',
  'Inngangspartier med gulv av stein, keramikk eller storformat kunststein og tilstedeværelsessensorer med timer på belysningen i inngangspartier, trapper og repos.',
  'Entréer med golv av sten, keramik eller storformatig konststen och närvarodetektorer med timer på belysningen i entréer, trapphus och våningsplan.')
p('.qualitySpecs.groups[8].items[2]',
  'Garaje con puerta mecanizada con mando a distancia, suelo de hormigón pulido al cuarzo con membrana epoxi, protección contra incendios y preinstalación para la carga de vehículos eléctricos, y ascensores que llegan a todas las plantas y a las plantas de garaje, con puertas automáticas, detección de sobrecarga y conexión telefónica.',
  'Garage avec porte motorisée à télécommande, sol en béton poli au quartz avec revêtement époxy, protection incendie et pré-équipement pour la recharge de véhicules électriques, et ascenseurs desservant tous les étages et directement les niveaux de garage, avec portes automatiques, détection de surcharge et liaison téléphonique.',
  'Garage mit ferngesteuertem Tor, poliertem Quarzbetonboden mit Epoxidbeschichtung, Brandschutz und Vorinstallation für das Laden von Elektrofahrzeugen sowie Aufzüge, die alle Geschosse und die Garagenebenen direkt erreichen, mit automatischen Türen, Überlastungserkennung und Telefonverbindung.',
  'Гараж с автоматическими воротами с дистанционным управлением, полом из полированного кварцевого бетона с эпоксидным покрытием, противопожарной защитой и подготовкой к зарядке электромобилей, а также лифты, которые доходят до всех этажей и напрямую до уровней гаража, с автоматическими дверями, датчиком перегрузки и телефонной связью.',
  'مرآب ببوابة آلية بجهاز تحكم عن بُعد، وأرضية من الخرسانة المصقولة بالكوارتز بطبقة إيبوكسي، وحماية من الحريق وتجهيز مسبق لشحن السيارات الكهربائية، ومصاعد تصل إلى جميع الطوابق ومباشرة إلى طابقي المرآب، بأبواب أوتوماتيكية وكشف للحمولة الزائدة واتصال هاتفي.',
  'Een garage met een afstandsbediende poort, een gepolijste kwartsbetonvloer met epoxycoating, brandbeveiliging en voorbereiding voor het opladen van elektrische auto’s, en liften die alle verdiepingen en rechtstreeks de garageverdiepingen bereiken, met automatische deuren, overbelastingsdetectie en een telefoonverbinding.',
  'Garaż z bramą sterowaną pilotem, podłogą z polerowanego betonu kwarcowego z powłoką epoksydową, ochroną przeciwpożarową i przygotowaniem do ładowania pojazdów elektrycznych oraz windy docierające na wszystkie piętra i bezpośrednio na poziomy garażowe, z drzwiami automatycznymi, wykrywaniem przeciążenia i łącznością telefoniczną.',
  'Garasje med fjernstyrt port, gulv av pusset kvartsbetong med epoksybelegg, brannsikring og forberedelse for lading av elbiler, og heiser som når alle etasjer og garasjeplanene direkte, med automatiske dører, overlastdeteksjon og telefonforbindelse.',
  'Garage med fjärrstyrd port, golv av polerad kvartsbetong med epoxibeläggning, brandskydd och förberedelse för laddning av elbilar, samt hissar som når alla våningar och garageplanen direkt, med automatiska dörrar, överlastdetektering och telefonanslutning.')

# 116-136 residences
p('.residences.headlineHtml', 'Diecisiete viviendas, <em>cuatro tipos</em>', 'Dix-sept logements, <em>quatre types</em>',
  'Siebzehn Wohnungen, <em>vier Arten</em>', 'Семнадцать квартир, <em>четыре типа</em>', 'سبعة عشر مسكناً، <em>أربعة أنواع</em>',
  'Zeventien woningen, <em>vier soorten</em>', 'Siedemnaście mieszkań, <em>cztery rodzaje</em>', 'Sytten boliger, <em>fire typer</em>',
  'Sjutton bostäder, <em>fyra slag</em>')
p('.residences.copy',
  'Las 17 viviendas a la venta se dividen en cuatro grupos según la planta y el espacio exterior. La tabla de abajo recoge cada una con su precio.',
  'Les 17 logements annoncés se répartissent en quatre groupes selon l’étage et l’espace extérieur. Le tableau ci-dessous les présente un par un avec leur prix.',
  'Die 17 gelisteten Wohnungen gliedern sich nach Geschoss und Außenbereich in vier Gruppen. Die Tabelle unten führt jede einzelne mit ihrem Preis auf.',
  'Семнадцать квартир, находящихся в продаже, делятся на четыре группы по этажу и наружным пространствам. В таблице ниже перечислены все они с ценами.',
  'تنقسم المساكن السبعة عشر المعروضة إلى أربع مجموعات بحسب الطابق والمساحة الخارجية. ويعرض الجدول أدناه كل مسكن مع سعره.',
  'De 17 aangeboden woningen vallen naar verdieping en buitenruimte uiteen in vier groepen. De tabel hieronder somt elke woning op met haar prijs.',
  '17 oferowanych mieszkań dzieli się na cztery grupy według piętra i przestrzeni zewnętrznej. W tabeli poniżej wymieniono każde z nich wraz z ceną.',
  'De 17 annonserte boligene deles i fire grupper etter etasje og uteareal. Tabellen nedenfor viser hver enkelt med pris.',
  'De 17 listade bostäderna delas in i fyra grupper efter våning och utomhusyta. Tabellen nedan listar var och en med pris.')
p('.residences.items[0].name', 'Viviendas de planta baja con jardín y piscina', 'Logements de rez-de-chaussée avec jardin et piscine',
  'Erdgeschosswohnungen mit Garten und Pool', 'Квартиры на первом этаже с садом и бассейном', 'مساكن أرضية بحديقة ومسبح',
  'Woningen op de begane grond met tuin en zwembad', 'Mieszkania na parterze z ogrodem i basenem', 'Boliger i første etasje med hage og basseng',
  'Bostäder på bottenvåningen med trädgård och pool')
p('.residences.items[0].points[0]',
  'Dos viviendas de tres dormitorios a nivel de calle, cada una con terraza, jardín privado y piscina privada: Ground A, con #134.62 [m2] construidos, una terraza de #102.25 [m2] y un jardín de #177.69 [m2], y Ground B, con #104.61 [m2] construidos, una terraza de #78.28 [m2] y un jardín de #45.47 [m2].',
  'Deux logements de trois chambres au niveau du sol, chacun avec une terrasse, un jardin privé et une piscine privée : Ground A, avec #134.62 [m2] construits, une terrasse de #102.25 [m2] et un jardin de #177.69 [m2], et Ground B, avec #104.61 [m2] construits, une terrasse de #78.28 [m2] et un jardin de #45.47 [m2].',
  'Zwei Wohnungen mit drei Schlafzimmern auf Erdgeschossniveau, jeweils mit Terrasse, privatem Garten und privatem Pool: Ground A mit #134.62 [m2] bebauter Fläche, einer Terrasse von #102.25 [m2] und einem Garten von #177.69 [m2] sowie Ground B mit #104.61 [m2] bebauter Fläche, einer Terrasse von #78.28 [m2] und einem Garten von #45.47 [m2].',
  'Две квартиры с тремя спальнями на уровне земли, у каждой есть терраса, частный сад и частный бассейн: Ground A — #134.62 [m2] застроенной площади, терраса #102.25 [m2] и сад #177.69 [m2]; Ground B — #104.61 [m2] застроенной площади, терраса #78.28 [m2] и сад #45.47 [m2].',
  'مسكنان بثلاث غرف نوم على مستوى الأرض، لكل منهما تراس وحديقة خاصة ومسبح خاص: Ground A بمساحة مبنية #134.62 [m2] وتراس #102.25 [m2] وحديقة #177.69 [m2]، وGround B بمساحة مبنية #104.61 [m2] وتراس #78.28 [m2] وحديقة #45.47 [m2].',
  'Twee woningen met drie slaapkamers op begane-grondniveau, elk met een terras, een privétuin en een privézwembad: Ground A met #134.62 [m2] bebouwd, een terras van #102.25 [m2] en een tuin van #177.69 [m2], en Ground B met #104.61 [m2] bebouwd, een terras van #78.28 [m2] en een tuin van #45.47 [m2].',
  'Dwa mieszkania z trzema sypialniami na poziomie parteru, każde z tarasem, prywatnym ogrodem i prywatnym basenem: Ground A z #134.62 [m2] powierzchni zabudowy, tarasem o powierzchni #102.25 [m2] i ogrodem o powierzchni #177.69 [m2] oraz Ground B z #104.61 [m2] powierzchni zabudowy, tarasem o powierzchni #78.28 [m2] i ogrodem o powierzchni #45.47 [m2].',
  'To boliger med tre soverom i bakkeplan, hver med terrasse, privat hage og privat basseng: Ground A med #134.62 [m2] bebygd areal, en terrasse på #102.25 [m2] og en hage på #177.69 [m2], og Ground B med #104.61 [m2] bebygd areal, en terrasse på #78.28 [m2] og en hage på #45.47 [m2].',
  'Två bostäder med tre sovrum i marknivå, var och en med terrass, privat trädgård och privat pool: Ground A med #134.62 [m2] byggyta, en terrass på #102.25 [m2] och en trädgård på #177.69 [m2], och Ground B med #104.61 [m2] byggyta, en terrass på #78.28 [m2] och en trädgård på #45.47 [m2].')
p('.residences.items[0].points[1]',
  'Los planos dan las piscinas como de #99.33 [m2] para Ground A y de #23.76 [m2] para Ground B. Cada vivienda tiene dos plazas de garaje y un trastero.',
  'Les plans donnent des piscines de #99.33 [m2] pour Ground A et de #23.76 [m2] pour Ground B. Chaque logement a deux places de garage et une cave.',
  'Die Pläne geben die Pools mit #99.33 [m2] für Ground A und #23.76 [m2] für Ground B an. Jede Wohnung hat zwei Garagenstellplätze und einen Abstellraum.',
  'По планам бассейны имеют площадь #99.33 [m2] у Ground A и #23.76 [m2] у Ground B. К каждой квартире прилагаются два места в гараже и кладовая.',
  'تعطي المخططات مساحة المسبحين #99.33 [m2] لـ Ground A و#23.76 [m2] لـ Ground B. ولكل مسكن موقفان في المرآب وغرفة تخزين.',
  'De plattegronden geven de zwembaden op #99.33 [m2] voor Ground A en #23.76 [m2] voor Ground B. Elke woning heeft twee garageplaatsen en een berging.',
  'Według rzutów baseny mają #99.33 [m2] w Ground A i #23.76 [m2] w Ground B. Każde mieszkanie ma dwa miejsca garażowe i komórkę lokatorską.',
  'Tegningene oppgir bassengene til #99.33 [m2] for Ground A og #23.76 [m2] for Ground B. Hver bolig har to garasjeplasser og en bod.',
  'Ritningarna anger poolerna till #99.33 [m2] för Ground A och #23.76 [m2] för Ground B. Varje bostad har två garageplatser och ett förråd.')
p('.residences.items[0].points[2]', 'Los precios son €2084500 y €1408000.', 'Les prix sont de €2084500 et €1408000.', 'Die Preise betragen €2084500 und €1408000.',
  'Цены — €2084500 и €1408000.', 'السعران هما €2084500 و€1408000.', 'De prijzen zijn €2084500 en €1408000.', 'Ceny wynoszą €2084500 i €1408000.',
  'Prisene er €2084500 og €1408000.', 'Priserna är €2084500 och €1408000.')
p('.residences.items[0].points[3]',
  'Los planos dan terrazas de #102.73 y #84.24 [m2] frente a #102.25 y #78.28 [m2] en la lista de precios.',
  'Les plans donnent des terrasses de #102.73 et #84.24 [m2] contre #102.25 et #78.28 [m2] sur la liste de prix.',
  'Die Pläne geben Terrassen von #102.73 und #84.24 [m2] an, die Preisliste #102.25 und #78.28 [m2].',
  'По планам террасы имеют площадь #102.73 и #84.24 [m2], а в прайс-листе — #102.25 и #78.28 [m2].',
  'تعطي المخططات تراسين بمساحة #102.73 و#84.24 [m2] مقابل #102.25 و#78.28 [m2] في قائمة الأسعار.',
  'De plattegronden geven terrassen van #102.73 en #84.24 [m2], tegenover #102.25 en #78.28 [m2] op de prijslijst.',
  'Według rzutów tarasy mają #102.73 i #84.24 [m2], a w cenniku #102.25 i #78.28 [m2].',
  'Tegningene oppgir terrasser på #102.73 og #84.24 [m2], mot #102.25 og #78.28 [m2] i prislisten.',
  'Ritningarna anger terrasser på #102.73 och #84.24 [m2], mot #102.25 och #78.28 [m2] i prislistan.')
p('.residences.items[1].name', 'Viviendas con terraza, de la primera a la tercera planta', 'Logements avec terrasse, du premier au troisième étage',
  'Wohnungen mit Terrasse im ersten bis dritten Obergeschoss', 'Квартиры с террасой на втором–четвёртом этажах', 'مساكن بتراس من الطابق الأول إلى الثالث',
  'Woningen met terras op de eerste tot en met de derde verdieping', 'Mieszkania z tarasem na pierwszym–trzecim piętrze',
  'Boliger med terrasse i andre til fjerde etasje', 'Bostäder med terrass på första till tredje våningen')
p('.residences.items[1].points[0]',
  'Siete viviendas sin piscina privada: seis de tres dormitorios (1D, 1G, 2D, 2G, 3D y 3G) y una de dos dormitorios (2E).',
  'Sept logements sans piscine privée : six de trois chambres (1D, 1G, 2D, 2G, 3D et 3G) et un de deux chambres (2E).',
  'Sieben Wohnungen ohne privaten Pool: sechs mit drei Schlafzimmern (1D, 1G, 2D, 2G, 3D und 3G) und eine mit zwei Schlafzimmern (2E).',
  'Семь квартир без частного бассейна: шесть с тремя спальнями (1D, 1G, 2D, 2G, 3D и 3G) и одна с двумя спальнями (2E).',
  'سبعة مساكن بلا مسبح خاص: ستة بثلاث غرف نوم (1D وَ1G وَ2D وَ2G وَ3D وَ3G) وواحد بغرفتي نوم (2E).',
  'Zeven woningen zonder privézwembad: zes met drie slaapkamers (1D, 1G, 2D, 2G, 3D en 3G) en één met twee slaapkamers (2E).',
  'Siedem mieszkań bez prywatnego basenu: sześć z trzema sypialniami (1D, 1G, 2D, 2G, 3D i 3G) i jedno z dwiema sypialniami (2E).',
  'Sju boliger uten privat basseng: seks med tre soverom (1D, 1G, 2D, 2G, 3D og 3G) og én med to soverom (2E).',
  'Sju bostäder utan privat pool: sex med tre sovrum (1D, 1G, 2D, 2G, 3D och 3G) och en med två sovrum (2E).')
p('.residences.items[1].points[1]',
  'Las viviendas de tres dormitorios tienen #103.26 o #103.49 [m2] construidos y terrazas de #19.51 a #101.21 [m2], las mayores en 1G, 2G y 3G, con #101.21, #92.13 y #77.58 [m2]; 2E tiene #79.48 [m2] construidos y una terraza de #14.92 [m2]. Cada una tiene dos plazas de garaje y un trastero.',
  'Les logements de trois chambres ont #103.26 ou #103.49 [m2] construits et des terrasses de #19.51 à #101.21 [m2], les plus grandes étant celles de 1G, 2G et 3G avec #101.21, #92.13 et #77.58 [m2] ; le 2E a #79.48 [m2] construits et une terrasse de #14.92 [m2]. Chacun a deux places de garage et une cave.',
  'Die Wohnungen mit drei Schlafzimmern haben #103.26 oder #103.49 [m2] bebaute Fläche und Terrassen von #19.51 bis #101.21 [m2]; die größten haben 1G, 2G und 3G mit #101.21, #92.13 und #77.58 [m2]; 2E hat #79.48 [m2] bebaute Fläche und eine Terrasse von #14.92 [m2]. Jede hat zwei Garagenstellplätze und einen Abstellraum.',
  'У квартир с тремя спальнями #103.26 или #103.49 [m2] застроенной площади и террасы от #19.51 до #101.21 [m2]; самые большие — у 1G, 2G и 3G: #101.21, #92.13 и #77.58 [m2]; у 2E — #79.48 [m2] застроенной площади и терраса #14.92 [m2]. К каждой прилагаются два места в гараже и кладовая.',
  'للمساكن ذات الغرف الثلاث مساحة مبنية #103.26 أو #103.49 [m2] وتراسات من #19.51 إلى #101.21 [m2]، وأكبرها في 1G وَ2G وَ3G بمساحة #101.21 وَ#92.13 وَ#77.58 [m2]؛ أما 2E فمساحته المبنية #79.48 [m2] وتراسه #14.92 [m2]. ولكل منها موقفان في المرآب وغرفة تخزين.',
  'De woningen met drie slaapkamers hebben #103.26 of #103.49 [m2] bebouwd en terrassen van #19.51 tot #101.21 [m2], de grootste bij 1G, 2G en 3G met #101.21, #92.13 en #77.58 [m2]; 2E heeft #79.48 [m2] bebouwd en een terras van #14.92 [m2]. Elke woning heeft twee garageplaatsen en een berging.',
  'Mieszkania z trzema sypialniami mają #103.26 lub #103.49 [m2] powierzchni zabudowy i tarasy od #19.51 do #101.21 [m2], największe przy 1G, 2G i 3G: #101.21, #92.13 i #77.58 [m2]; 2E ma #79.48 [m2] powierzchni zabudowy i taras o powierzchni #14.92 [m2]. Każde ma dwa miejsca garażowe i komórkę lokatorską.',
  'Boligene med tre soverom har #103.26 eller #103.49 [m2] bebygd areal og terrasser på #19.51 til #101.21 [m2], de største ved 1G, 2G og 3G med #101.21, #92.13 og #77.58 [m2]; 2E har #79.48 [m2] bebygd areal og en terrasse på #14.92 [m2]. Hver har to garasjeplasser og en bod.',
  'Bostäderna med tre sovrum har #103.26 eller #103.49 [m2] byggyta och terrasser på #19.51 till #101.21 [m2], de största hos 1G, 2G och 3G med #101.21, #92.13 och #77.58 [m2]; 2E har #79.48 [m2] byggyta och en terrass på #14.92 [m2]. Varje bostad har två garageplatser och ett förråd.')
p('.residences.items[1].points[2]',
  'La vivienda 2E cuesta €775500 y las de tres dormitorios van de €1097250 a €1249500.',
  'Le logement 2E coûte €775500 et les logements de trois chambres vont de €1097250 à €1249500.',
  'Die Wohnung 2E kostet €775500 und die Wohnungen mit drei Schlafzimmern reichen von €1097250 bis €1249500.',
  'Квартира 2E стоит €775500, а квартиры с тремя спальнями — от €1097250 до €1249500.',
  'يبلغ سعر المسكن 2E ‏€775500 وتتراوح أسعار المساكن ذات الغرف الثلاث من €1097250 إلى €1249500.',
  'Woning 2E kost €775500 en de woningen met drie slaapkamers lopen van €1097250 tot €1249500.',
  'Mieszkanie 2E kosztuje €775500, a mieszkania z trzema sypialniami od €1097250 do €1249500.',
  'Bolig 2E koster €775500, og boligene med tre soverom går fra €1097250 til €1249500.',
  'Bostad 2E kostar €775500 och bostäderna med tre sovrum går från €1097250 till €1249500.')
p('.residences.items[1].points[3]',
  'La lista de precios da #103.26 [m2] construidos para 2D y 3D, donde los planos dan #103.49 [m2].',
  'La liste de prix donne #103.26 [m2] construits pour 2D et 3D, là où les plans donnent #103.49 [m2].',
  'Die Preisliste gibt für 2D und 3D #103.26 [m2] bebaute Fläche an, die Pläne dagegen #103.49 [m2].',
  'В прайс-листе у 2D и 3D указано #103.26 [m2] застроенной площади, а на планах — #103.49 [m2].',
  'تذكر قائمة الأسعار #103.26 [m2] مساحة مبنية للمسكنين 2D وَ3D، بينما تذكر المخططات #103.49 [m2].',
  'De prijslijst geeft voor 2D en 3D #103.26 [m2] bebouwd, waar de plattegronden #103.49 [m2] geven.',
  'Cennik podaje dla 2D i 3D #103.26 [m2] powierzchni zabudowy, a rzuty #103.49 [m2].',
  'Prislisten oppgir #103.26 [m2] bebygd areal for 2D og 3D, der tegningene oppgir #103.49 [m2].',
  'Prislistan anger #103.26 [m2] byggyta för 2D och 3D, där ritningarna anger #103.49 [m2].')
p('.residences.items[2].name', 'Viviendas de tercera planta con piscina privada', 'Logements du troisième étage avec piscine privée',
  'Wohnungen im dritten Obergeschoss mit privatem Pool', 'Квартиры на четвёртом этаже с частным бассейном', 'مساكن الطابق الثالث بمسبح خاص',
  'Woningen op de derde verdieping met privézwembad', 'Mieszkania na trzecim piętrze z prywatnym basenem',
  'Boliger i fjerde etasje med privat basseng', 'Bostäder på tredje våningen med privat pool')
p('.residences.items[2].points[0]',
  'Las viviendas 3A y 3B tienen tres dormitorios, una terraza y una piscina privada de #4.73 [m2] según los planos: 3A tiene #134.62 [m2] construidos y una terraza de #42.99 [m2], y 3B tiene #104.61 [m2] construidos y una terraza de #33.13 [m2].',
  'Les logements 3A et 3B ont trois chambres, une terrasse et une piscine privée de #4.73 [m2] d’après les plans : le 3A a #134.62 [m2] construits et une terrasse de #42.99 [m2], et le 3B a #104.61 [m2] construits et une terrasse de #33.13 [m2].',
  'Die Wohnungen 3A und 3B haben drei Schlafzimmer, eine Terrasse und laut Plänen einen privaten Pool von #4.73 [m2]: 3A hat #134.62 [m2] bebaute Fläche und eine Terrasse von #42.99 [m2], 3B hat #104.61 [m2] bebaute Fläche und eine Terrasse von #33.13 [m2].',
  'У квартир 3A и 3B три спальни, терраса и, согласно планам, частный бассейн площадью #4.73 [m2]: у 3A — #134.62 [m2] застроенной площади и терраса #42.99 [m2], у 3B — #104.61 [m2] застроенной площади и терраса #33.13 [m2].',
  'للمسكنين 3A وَ3B ثلاث غرف نوم وتراس ومسبح خاص مساحته #4.73 [m2] بحسب المخططات: مساحة 3A المبنية #134.62 [m2] وتراسه #42.99 [m2]، ومساحة 3B المبنية #104.61 [m2] وتراسه #33.13 [m2].',
  'De woningen 3A en 3B hebben drie slaapkamers, een terras en volgens de plattegronden een privézwembad van #4.73 [m2]: 3A heeft #134.62 [m2] bebouwd en een terras van #42.99 [m2], en 3B heeft #104.61 [m2] bebouwd en een terras van #33.13 [m2].',
  'Mieszkania 3A i 3B mają trzy sypialnie, taras i według rzutów prywatny basen o powierzchni #4.73 [m2]: 3A ma #134.62 [m2] powierzchni zabudowy i taras o powierzchni #42.99 [m2], a 3B ma #104.61 [m2] powierzchni zabudowy i taras o powierzchni #33.13 [m2].',
  'Boligene 3A og 3B har tre soverom, en terrasse og ifølge tegningene et privat basseng på #4.73 [m2]: 3A har #134.62 [m2] bebygd areal og en terrasse på #42.99 [m2], og 3B har #104.61 [m2] bebygd areal og en terrasse på #33.13 [m2].',
  'Bostäderna 3A och 3B har tre sovrum, en terrass och enligt ritningarna en privat pool på #4.73 [m2]: 3A har #134.62 [m2] byggyta och en terrass på #42.99 [m2], och 3B har #104.61 [m2] byggyta och en terrass på #33.13 [m2].')
p('.residences.items[2].points[1]',
  'Cada una tiene dos plazas de garaje y un trastero. Los precios son €1420650 y €1193500.',
  'Chacun a deux places de garage et une cave. Les prix sont de €1420650 et €1193500.',
  'Jede hat zwei Garagenstellplätze und einen Abstellraum. Die Preise betragen €1420650 und €1193500.',
  'К каждой прилагаются два места в гараже и кладовая. Цены — €1420650 и €1193500.',
  'ولكل منهما موقفان في المرآب وغرفة تخزين. والسعران هما €1420650 و€1193500.',
  'Elke woning heeft twee garageplaatsen en een berging. De prijzen zijn €1420650 en €1193500.',
  'Każde ma dwa miejsca garażowe i komórkę lokatorską. Ceny wynoszą €1420650 i €1193500.',
  'Hver har to garasjeplasser og en bod. Prisene er €1420650 og €1193500.',
  'Varje bostad har två garageplatser och ett förråd. Priserna är €1420650 och €1193500.')
p('.residences.items[2].points[2]',
  'El plano de 3A da una terraza de #47.72 [m2] frente a #42.99 [m2] en la lista de precios.',
  'Le plan du 3A donne une terrasse de #47.72 [m2] contre #42.99 [m2] sur la liste de prix.',
  'Der Plan von 3A gibt eine Terrasse von #47.72 [m2] an, die Preisliste #42.99 [m2].',
  'На плане 3A терраса имеет площадь #47.72 [m2], а в прайс-листе — #42.99 [m2].',
  'يعطي مخطط 3A تراساً بمساحة #47.72 [m2] مقابل #42.99 [m2] في قائمة الأسعار.',
  'De plattegrond van 3A geeft een terras van #47.72 [m2], tegenover #42.99 [m2] op de prijslijst.',
  'Rzut 3A podaje taras o powierzchni #47.72 [m2], a cennik #42.99 [m2].',
  'Tegningen av 3A oppgir en terrasse på #47.72 [m2], mot #42.99 [m2] i prislisten.',
  'Ritningen för 3A anger en terrass på #47.72 [m2], mot #42.99 [m2] i prislistan.')
p('.residences.items[3].name', 'Áticos con solárium en la cubierta y piscina', 'Penthouses avec solarium sur le toit et piscine',
  'Penthäuser mit Dachsolarium und Pool', 'Пентхаусы с солярием на крыше и бассейном', 'بنتهاوس بسولاريوم على السطح ومسبح',
  'Penthouses met daksolarium en zwembad', 'Penthouse’y z solarium na dachu i basenem', 'Toppleiligheter med solterrasse på taket og basseng',
  'Takvåningar med solterrass på taket och pool')
p('.residences.items[3].points[0]',
  'Seis viviendas en la cuarta planta, cada una con una terraza y un solárium privado con piscina en la cubierta, en el nivel superior: 4B, 4C, 4F y 4G con dos dormitorios y #79.48 [m2] construidos, y 4E y 4H con tres dormitorios y #103.49 [m2] construidos.',
  'Six logements au quatrième étage, chacun avec une terrasse et un solarium privé avec piscine sur le toit, au niveau supérieur : 4B, 4C, 4F et 4G avec deux chambres et #79.48 [m2] construits, et 4E et 4H avec trois chambres et #103.49 [m2] construits.',
  'Sechs Wohnungen im vierten Obergeschoss, jeweils mit einer Terrasse und einem privaten Solarium mit Pool auf der darüberliegenden Dachebene: 4B, 4C, 4F und 4G mit zwei Schlafzimmern und #79.48 [m2] bebauter Fläche sowie 4E und 4H mit drei Schlafzimmern und #103.49 [m2] bebauter Fläche.',
  'Шесть квартир на пятом этаже, у каждой терраса и частный солярий с бассейном на крыше, на уровне выше: 4B, 4C, 4F и 4G с двумя спальнями и #79.48 [m2] застроенной площади, а также 4E и 4H с тремя спальнями и #103.49 [m2] застроенной площади.',
  'ستة مساكن في الطابق الرابع، لكل منها تراس وسولاريوم خاص بمسبح على السطح في المستوى الأعلى: 4B وَ4C وَ4F وَ4G بغرفتي نوم ومساحة مبنية #79.48 [m2]، و4E وَ4H بثلاث غرف نوم ومساحة مبنية #103.49 [m2].',
  'Zes woningen op de vierde verdieping, elk met een terras en een privésolarium met zwembad op het dak op het niveau erboven: 4B, 4C, 4F en 4G met twee slaapkamers en #79.48 [m2] bebouwd, en 4E en 4H met drie slaapkamers en #103.49 [m2] bebouwd.',
  'Sześć mieszkań na czwartym piętrze, każde z tarasem i prywatnym solarium z basenem na dachu, na poziomie wyżej: 4B, 4C, 4F i 4G z dwiema sypialniami i #79.48 [m2] powierzchni zabudowy oraz 4E i 4H z trzema sypialniami i #103.49 [m2] powierzchni zabudowy.',
  'Seks boliger i femte etasje, hver med en terrasse og en privat solterrasse med basseng på taket på nivået over: 4B, 4C, 4F og 4G med to soverom og #79.48 [m2] bebygd areal, og 4E og 4H med tre soverom og #103.49 [m2] bebygd areal.',
  'Sex bostäder på fjärde våningen, var och en med en terrass och en privat solterrass med pool på taket på nivån ovanför: 4B, 4C, 4F och 4G med två sovrum och #79.48 [m2] byggyta, och 4E och 4H med tre sovrum och #103.49 [m2] byggyta.')
p('.residences.items[3].points[1]',
  'Terrazas de #22.31 [m2] (4B y 4C), #16.67 [m2] (4F y 4G), #29.18 [m2] (4E) y #76.07 [m2] (4H), y solariums de #27.33 [m2] en las viviendas de dos dormitorios y de #36.32 [m2] en las otras dos. Los planos dan las piscinas de #9.99 [m2] en las de dos dormitorios y de #13.28 y #13.27 [m2] en 4E y 4H.',
  'Terrasses de #22.31 [m2] (4B et 4C), #16.67 [m2] (4F et 4G), #29.18 [m2] (4E) et #76.07 [m2] (4H), et solariums de #27.33 [m2] pour les logements de deux chambres et de #36.32 [m2] pour les deux autres. Les plans donnent des piscines de #9.99 [m2] pour les logements de deux chambres et de #13.28 et #13.27 [m2] pour 4E et 4H.',
  'Terrassen von #22.31 [m2] (4B und 4C), #16.67 [m2] (4F und 4G), #29.18 [m2] (4E) und #76.07 [m2] (4H) sowie Solarien von #27.33 [m2] bei den Wohnungen mit zwei Schlafzimmern und #36.32 [m2] bei den beiden anderen. Die Pläne geben die Pools mit #9.99 [m2] bei den Wohnungen mit zwei Schlafzimmern und mit #13.28 und #13.27 [m2] bei 4E und 4H an.',
  'Террасы #22.31 [m2] (4B и 4C), #16.67 [m2] (4F и 4G), #29.18 [m2] (4E) и #76.07 [m2] (4H), солярии #27.33 [m2] у квартир с двумя спальнями и #36.32 [m2] у двух остальных. По планам бассейны имеют площадь #9.99 [m2] у квартир с двумя спальнями и #13.28 и #13.27 [m2] у 4E и 4H.',
  'تراسات بمساحة #22.31 [m2] (4B وَ4C) و#16.67 [m2] (4F وَ4G) و#29.18 [m2] (4E) و#76.07 [m2] (4H)، وسولاريوم بمساحة #27.33 [m2] في المساكن ذات الغرفتين و#36.32 [m2] في المسكنين الآخرين. وتعطي المخططات مساحة المسابح #9.99 [m2] في المساكن ذات الغرفتين و#13.28 وَ#13.27 [m2] في 4E وَ4H.',
  'Terrassen van #22.31 [m2] (4B en 4C), #16.67 [m2] (4F en 4G), #29.18 [m2] (4E) en #76.07 [m2] (4H), en solariums van #27.33 [m2] bij de woningen met twee slaapkamers en #36.32 [m2] bij de andere twee. De plattegronden geven de zwembaden op #9.99 [m2] bij de woningen met twee slaapkamers en op #13.28 en #13.27 [m2] bij 4E en 4H.',
  'Tarasy o powierzchni #22.31 [m2] (4B i 4C), #16.67 [m2] (4F i 4G), #29.18 [m2] (4E) i #76.07 [m2] (4H) oraz solaria o powierzchni #27.33 [m2] przy mieszkaniach z dwiema sypialniami i #36.32 [m2] przy pozostałych dwóch. Według rzutów baseny mają #9.99 [m2] przy mieszkaniach z dwiema sypialniami oraz #13.28 i #13.27 [m2] przy 4E i 4H.',
  'Terrasser på #22.31 [m2] (4B og 4C), #16.67 [m2] (4F og 4G), #29.18 [m2] (4E) og #76.07 [m2] (4H), og solterrasser på #27.33 [m2] ved boligene med to soverom og #36.32 [m2] ved de to andre. Tegningene oppgir bassengene til #9.99 [m2] ved boligene med to soverom og til #13.28 og #13.27 [m2] ved 4E og 4H.',
  'Terrasser på #22.31 [m2] (4B och 4C), #16.67 [m2] (4F och 4G), #29.18 [m2] (4E) och #76.07 [m2] (4H), och solterrasser på #27.33 [m2] vid bostäderna med två sovrum och #36.32 [m2] vid de två andra. Ritningarna anger poolerna till #9.99 [m2] vid bostäderna med två sovrum och till #13.28 och #13.27 [m2] vid 4E och 4H.')
p('.residences.items[3].points[2]',
  'Las viviendas de dos dormitorios cuestan €1230000 o €1290800, y las de tres dormitorios, €1721500 y €1908500.',
  'Les logements de deux chambres coûtent €1230000 ou €1290800, et ceux de trois chambres €1721500 et €1908500.',
  'Die Wohnungen mit zwei Schlafzimmern kosten €1230000 oder €1290800, die mit drei Schlafzimmern €1721500 und €1908500.',
  'Квартиры с двумя спальнями стоят €1230000 или €1290800, а с тремя спальнями — €1721500 и €1908500.',
  'تبلغ أسعار المساكن ذات الغرفتين €1230000 أو €1290800، وأسعار المساكن ذات الغرف الثلاث €1721500 و€1908500.',
  'De woningen met twee slaapkamers kosten €1230000 of €1290800 en die met drie slaapkamers €1721500 en €1908500.',
  'Mieszkania z dwiema sypialniami kosztują €1230000 lub €1290800, a z trzema sypialniami €1721500 i €1908500.',
  'Boligene med to soverom koster €1230000 eller €1290800, og boligene med tre soverom €1721500 og €1908500.',
  'Bostäderna med två sovrum kostar €1230000 eller €1290800, och bostäderna med tre sovrum €1721500 och €1908500.')
p('.residences.items[3].points[3]',
  'El plano de 4E da una terraza de #21.80 [m2] frente a #29.18 [m2] en la lista de precios.',
  'Le plan du 4E donne une terrasse de #21.80 [m2] contre #29.18 [m2] sur la liste de prix.',
  'Der Plan von 4E gibt eine Terrasse von #21.80 [m2] an, die Preisliste #29.18 [m2].',
  'На плане 4E терраса имеет площадь #21.80 [m2], а в прайс-листе — #29.18 [m2].',
  'يعطي مخطط 4E تراساً بمساحة #21.80 [m2] مقابل #29.18 [m2] في قائمة الأسعار.',
  'De plattegrond van 4E geeft een terras van #21.80 [m2], tegenover #29.18 [m2] op de prijslijst.',
  'Rzut 4E podaje taras o powierzchni #21.80 [m2], a cennik #29.18 [m2].',
  'Tegningen av 4E oppgir en terrasse på #21.80 [m2], mot #29.18 [m2] i prislisten.',
  'Ritningen för 4E anger en terrass på #21.80 [m2], mot #29.18 [m2] i prislistan.')

# 137-144 lifestyle
p('.lifestyle.headlineHtml', 'Una piscina, un spa <em>y espacio para trabajar</em>', 'Une piscine, un spa <em>et de la place pour travailler</em>',
  'Ein Pool, ein Spa <em>und Raum zum Arbeiten</em>', 'Бассейн, спа <em>и место для работы</em>', 'مسبح وسبا <em>ومساحة للعمل</em>',
  'Een zwembad, een spa <em>en ruimte om te werken</em>', 'Basen, spa <em>i miejsce do pracy</em>', 'Et basseng, et spa <em>og plass til å jobbe</em>',
  'En pool, ett spa <em>och plats att arbeta</em>')
p('.lifestyle.copy',
  'Las zonas comunes giran en torno a una piscina comunitaria, un gimnasio, un spa con sauna, un club social y un espacio de coworking.',
  'Les espaces communs s’organisent autour d’une piscine commune, d’une salle de sport, d’un spa avec sauna, d’un club social et d’un espace de coworking.',
  'Die Gemeinschaftsbereiche sind um einen Gemeinschaftspool, einen Fitnessraum, ein Spa mit Sauna, einen Social Club und einen Coworking-Bereich angelegt.',
  'Общие зоны построены вокруг общего бассейна, тренажёрного зала, спа с сауной, клуба для жителей и коворкинга.',
  'تدور المرافق المشتركة حول مسبح مشترك وصالة رياضية وسبا بساونا ونادٍ اجتماعي ومساحة عمل مشتركة.',
  'De gemeenschappelijke ruimten zijn gepland rond een gemeenschappelijk zwembad, een fitnessruimte, een spa met sauna, een sociale club en een coworkingruimte.',
  'Części wspólne zaplanowano wokół wspólnego basenu, siłowni, spa z sauną, klubu dla mieszkańców i przestrzeni coworkingowej.',
  'Fellesarealene er lagt opp rundt et felles basseng, et treningsrom, et spa med badstue, en sosial klubb og et coworking-areal.',
  'De gemensamma ytorna är planerade kring en gemensam pool, ett gym, ett spa med bastu, en social klubb och en coworkingyta.')
p('.lifestyle.panels[0][1]',
  'Una piscina comunitaria con iluminación nocturna, con zonas ajardinadas y un solárium para tomar el sol.',
  'Une piscine commune avec éclairage nocturne, des espaces paysagers et un solarium pour bronzer.',
  'Ein Gemeinschaftspool mit Nachtbeleuchtung, mit Grünflächen und einem Solarium zum Sonnenbaden.',
  'Общий бассейн с ночной подсветкой, озеленёнными территориями и солярием для загара.',
  'مسبح مشترك بإضاءة ليلية، مع مساحات خضراء وسولاريوم للتشمّس.',
  'Een gemeenschappelijk zwembad met nachtverlichting, met groene zones en een solarium om te zonnebaden.',
  'Wspólny basen z oświetleniem nocnym, terenami zieleni i solarium do opalania.',
  'Et felles basseng med nattbelysning, med grøntområder og en solterrasse for soling.',
  'En gemensam pool med kvällsbelysning, med grönområden och en solterrass för solbad.')
p('.lifestyle.panels[1][0]', 'El gimnasio y el spa', 'La salle de sport et le spa', 'Der Fitnessraum und das Spa', 'Спортзал и спа', 'الصالة الرياضية والسبا',
  'De fitnessruimte en de spa', 'Siłownia i spa', 'Treningsrommet og spaet', 'Gymmet och spaet')
p('.lifestyle.panels[1][1]',
  'Un gimnasio totalmente equipado y un spa con sauna para los residentes.',
  'Une salle de sport entièrement équipée et un spa avec sauna pour les résidents.',
  'Ein voll ausgestatteter Fitnessraum und ein Spa mit Sauna für die Bewohner.',
  'Полностью оборудованный тренажёрный зал и спа с сауной для жителей.',
  'صالة رياضية مجهزة بالكامل وسبا بساونا للسكان.',
  'Een volledig uitgeruste fitnessruimte en een spa met sauna voor de bewoners.',
  'W pełni wyposażona siłownia i spa z sauną dla mieszkańców.',
  'Et fullt utstyrt treningsrom og et spa med badstue for beboerne.',
  'Ett fullt utrustat gym och ett spa med bastu för de boende.')
p('.lifestyle.panels[2][0]', 'El club social y el coworking', 'Le club social et le coworking', 'Der Social Club und das Coworking', 'Клуб и коворкинг',
  'النادي الاجتماعي ومساحة العمل المشتركة', 'De sociale club en de coworkingruimte', 'Klub dla mieszkańców i coworking', 'Den sosiale klubben og coworking-arealet',
  'Den sociala klubben och coworkingytan')
p('.lifestyle.panels[2][1]',
  'Un club social para los residentes y un espacio de coworking, que el folleto y la memoria de calidades incluyen entre las zonas comunes.',
  'Un club social pour les résidents et un espace de coworking, que la brochure et le descriptif de qualité comptent parmi les espaces communs.',
  'Ein Social Club für die Bewohner und ein Coworking-Bereich, die Prospekt und Baubeschreibung zu den Gemeinschaftsbereichen zählen.',
  'Клуб для жителей и коворкинг, которые брошюра и спецификация качества относят к общим зонам.',
  'نادٍ اجتماعي للسكان ومساحة عمل مشتركة، يدرجهما الكتيّب ومواصفات الجودة ضمن المرافق المشتركة.',
  'Een sociale club voor de bewoners en een coworkingruimte, die de brochure en de kwaliteitsspecificatie onder de gemeenschappelijke ruimten rekenen.',
  'Klub dla mieszkańców i przestrzeń coworkingowa, które broszura i specyfikacja jakości zaliczają do części wspólnych.',
  'En sosial klubb for beboerne og et coworking-areal, som brosjyren og kvalitetsspesifikasjonen regner blant fellesarealene.',
  'En social klubb för de boende och en coworkingyta, som broschyren och kvalitetsbeskrivningen räknar bland de gemensamma ytorna.')
p('.lifestyle.panels[3][1]',
  'Cada vivienda a la venta incluye dos plazas de garaje y un trastero en los dos sótanos, a los que se llega en ascensor, con preinstalación para la carga de coches eléctricos.',
  'Chaque logement annoncé comprend deux places de garage et une cave sur les deux niveaux de sous-sol, desservis par ascenseur, avec pré-équipement pour la recharge de voitures électriques.',
  'Jede gelistete Wohnung hat zwei Garagenstellplätze und einen Abstellraum auf den beiden Untergeschossen, die per Aufzug erreichbar sind, mit Vorinstallation für das Laden von Elektroautos.',
  'К каждой квартире в списке прилагаются два места в гараже и кладовая на двух подземных уровнях, куда можно спуститься на лифте, с подготовкой к зарядке электромобилей.',
  'يشمل كل مسكن مدرج موقفين في المرآب وغرفة تخزين في الطابقين السفليين، ويُصل إليهما بالمصعد، مع تجهيز مسبق لشحن السيارات الكهربائية.',
  'Elke aangeboden woning omvat twee garageplaatsen en een berging op de twee kelderniveaus, bereikbaar met de lift, met voorbereiding voor het opladen van elektrische auto’s.',
  'Każde oferowane mieszkanie obejmuje dwa miejsca garażowe i komórkę lokatorską na dwóch poziomach podziemnych, dostępne windą, z przygotowaniem do ładowania samochodów elektrycznych.',
  'Hver oppførte bolig inkluderer to garasjeplasser og en bod i de to kjelleretasjene, nådd med heis, med forberedelse for lading av elbiler.',
  'Varje listad bostad inkluderar två garageplatser och ett förråd på de två källarplanen, nåbara med hiss, med förberedelse för laddning av elbilar.')

# 145-149 location
p('.location.headlineHtml', 'Estepona, <em>junto al casco antiguo</em>', 'Estepona, <em>à côté de la vieille ville</em>',
  'Estepona, <em>neben der Altstadt</em>', 'Эстепона, <em>рядом со старым городом</em>', 'إستيبونا، <em>بجوار البلدة القديمة</em>',
  'Estepona, <em>naast de oude binnenstad</em>', 'Estepona, <em>obok starówki</em>', 'Estepona, <em>ved siden av gamlebyen</em>',
  'Estepona, <em>intill gamla stan</em>')
p('.location.copy',
  'El edificio está en una de las zonas residenciales de Estepona, junto al casco antiguo y en pleno corazón de la Costa del Sol, cerca de la A-7 y la AP-7. El folleto del promotor sitúa el puerto deportivo, Playa Beach y la playa de La Rada a menos de diez minutos, con comercios, supermercados, colegios e instalaciones deportivas cerca y un acceso rápido a Málaga y su aeropuerto. Su plano de situación añade tiempos de 4 minutos hasta el puerto deportivo de Estepona, 6 hasta la playa de Punta Plata y 8 hasta la playa del Padrón, sin indicar cómo se recorren.',
  'L’immeuble se trouve dans l’un des quartiers résidentiels d’Estepona, à côté de la vieille ville et en plein cœur de la Costa del Sol, près de l’A-7 et de l’AP-7. La brochure du promoteur situe le port de plaisance, Playa Beach et la plage de La Rada à moins de dix minutes, avec des commerces, des supermarchés, des écoles et des équipements sportifs à proximité et un accès rapide à Málaga et à son aéroport. Sa carte de situation ajoute des temps de 4 minutes jusqu’au port de plaisance d’Estepona, de 6 jusqu’à la plage de Punta Plata et de 8 jusqu’à la plage du Padrón, sans préciser comment le trajet s’effectue.',
  'Das Gebäude liegt in einem der Wohnviertel von Estepona, neben der Altstadt und mitten an der Costa del Sol, nahe der A-7 und der AP-7. Laut Prospekt des Bauträgers sind der Yachthafen, Playa Beach und der Strand La Rada weniger als zehn Minuten entfernt, mit Geschäften, Supermärkten, Schulen und Sportanlagen in der Nähe und schneller Anbindung an Málaga und seinen Flughafen. Die Lagekarte nennt zusätzlich 4 Minuten bis zum Yachthafen von Estepona, 6 bis zum Strand Punta Plata und 8 bis zum Strand Padrón, ohne anzugeben, wie diese Strecken zurückgelegt werden.',
  'Здание находится в одном из жилых районов Эстепоны, рядом со старым городом и в самом сердце Коста-дель-Соль, недалеко от автострад A-7 и AP-7. В брошюре застройщика яхтенная гавань, Playa Beach и пляж Ла-Рада указаны менее чем в десяти минутах; рядом магазины, супермаркеты, школы и спортивные объекты, а до Малаги и её аэропорта быстро добраться. На карте расположения добавлено время: 4 минуты до яхтенной гавани Эстепоны, 6 до пляжа Пунта-Плата и 8 до пляжа Падрон, без указания, как именно проходится этот путь.',
  'يقع المبنى في إحدى المناطق السكنية في إستيبونا، بجوار البلدة القديمة وفي قلب كوستا ديل سول، قرب الطريقين A-7 وAP-7. ويضع كتيّب المطوّر المرفأ وPlaya Beach وشاطئ لا رادا على بعد أقل من عشر دقائق، مع متاجر وأسواق ومدارس ومرافق رياضية قريبة ووصول سريع إلى مالقة ومطارها. وتضيف خريطة الموقع فيه أزمنة قدرها 4 دقائق إلى مرفأ إستيبونا و6 إلى شاطئ بونتا بلاتا و8 إلى شاطئ بادرون، دون بيان وسيلة قطعها.',
  'Het gebouw staat in een van de woonwijken van Estepona, naast de oude binnenstad en midden aan de Costa del Sol, vlak bij de A-7 en de AP-7. De brochure van de ontwikkelaar noemt de jachthaven, Playa Beach en het strand La Rada op minder dan tien minuten, met winkels, supermarkten, scholen en sportvoorzieningen in de buurt en een snelle verbinding met Málaga en de luchthaven. De locatiekaart voegt daar tijden aan toe van 4 minuten naar de jachthaven van Estepona, 6 naar het strand Punta Plata en 8 naar het strand Padrón, zonder te zeggen hoe die worden afgelegd.',
  'Budynek stoi w jednej z dzielnic mieszkalnych Estepony, obok starówki i w samym sercu Costa del Sol, blisko autostrad A-7 i AP-7. Broszura dewelopera podaje, że port jachtowy, Playa Beach i plaża La Rada są oddalone o mniej niż dziesięć minut, a w pobliżu są sklepy, supermarkety, szkoły i obiekty sportowe oraz szybki dojazd do Malagi i jej lotniska. Mapa lokalizacji dodaje czasy: 4 minuty do portu jachtowego Estepony, 6 do plaży Punta Plata i 8 do plaży Padrón, bez wskazania, w jaki sposób je pokonać.',
  'Bygningen ligger i et av boligområdene i Estepona, ved siden av gamlebyen og midt på Costa del Sol, nær A-7 og AP-7. Utbyggerens brosjyre oppgir at småbåthavnen, Playa Beach og stranden La Rada ligger under ti minutter unna, med butikker, supermarkeder, skoler og idrettsanlegg i nærheten og rask tilgang til Málaga og flyplassen. Lokaliseringskartet legger til tider på 4 minutter til småbåthavnen i Estepona, 6 til stranden Punta Plata og 8 til stranden Padrón, uten å si hvordan de tilbakelegges.',
  'Byggnaden ligger i ett av Esteponas bostadsområden, intill gamla stan och mitt på Costa del Sol, nära A-7 och AP-7. Exploatörens broschyr anger att småbåtshamnen, Playa Beach och stranden La Rada ligger under tio minuter bort, med butiker, stormarknader, skolor och idrottsanläggningar i närheten och snabb åtkomst till Málaga och dess flygplats. Lägeskartan lägger till tider på 4 minuter till Esteponas småbåtshamn, 6 till stranden Punta Plata och 8 till stranden Padrón, utan att ange hur sträckorna tillryggaläggs.')
p('.location.mapLabelPlain', 'Estepona, junto al casco antiguo', 'Estepona, à côté de la vieille ville', 'Estepona, neben der Altstadt',
  'Эстепона, рядом со старым городом', 'إستيبونا، بجوار البلدة القديمة', 'Estepona, naast de oude binnenstad', 'Estepona, obok starówki',
  'Estepona, ved siden av gamlebyen', 'Estepona, intill gamla stan')
p('.location.distances[1][0]', 'Playa de Punta Plata', 'Plage de Punta Plata', 'Strand Punta Plata', 'Пляж Пунта-Плата', 'شاطئ بونتا بلاتا',
  'Strand Punta Plata', 'Plaża Punta Plata', 'Stranden Punta Plata', 'Stranden Punta Plata')
p('.location.distances[2][0]', 'Playa del Padrón', 'Plage du Padrón', 'Strand Padrón', 'Пляж Падрон', 'شاطئ بادرون', 'Strand Padrón', 'Plaża Padrón',
  'Stranden Padrón', 'Stranden Padrón')

# 150-154 investment and trust
p('.investment.cards[1][1]',
  'La lista de precios indica que sus precios no incluyen el 10% de IVA, el tipo aplicable a la vivienda nueva. Confirmamos por escrito el impuesto y los demás gastos de la compra.',
  'La liste de prix indique que ses prix s’entendent hors TVA de 10 %, le taux applicable aux logements neufs. Nous confirmons par écrit la taxe et les autres frais d’achat.',
  'Die Preisliste gibt an, dass ihre Preise die 10 % MwSt., den Satz für Neubauwohnungen, nicht enthalten. Wir bestätigen die Steuer und die übrigen Kaufnebenkosten schriftlich.',
  'В прайс-листе указано, что его цены не включают НДС 10% — ставку для новых квартир. Мы письменно подтверждаем налог и другие расходы на покупку.',
  'تذكر قائمة الأسعار أن أسعارها لا تشمل ضريبة القيمة المضافة البالغة 10%، وهي النسبة المطبقة على المساكن الجديدة. نؤكد الضريبة وسائر تكاليف الشراء كتابةً.',
  'De prijslijst vermeldt dat de prijzen exclusief 10% btw zijn, het tarief voor nieuwbouwwoningen. Wij bevestigen de belasting en de overige aankoopkosten schriftelijk.',
  'Cennik podaje, że jego ceny nie obejmują 10% VAT, czyli stawki dla nowych mieszkań. Podatek i pozostałe koszty zakupu potwierdzamy na piśmie.',
  'Prislisten oppgir at prisene ikke inkluderer 10 % mva, satsen for nye boliger. Vi bekrefter skatten og de øvrige kjøpskostnadene skriftlig.',
  'Prislistan anger att priserna inte inkluderar 10 % IVA, satsen för nybyggda bostäder. Vi bekräftar skatten och de övriga köpkostnaderna skriftligen.')
p('.investment.cards[2][1]',
  'La lista de precios asigna a cada vivienda a la venta dos plazas de garaje y un trastero, por número. Confirmamos las plazas y el trastero de la vivienda que usted elija.',
  'La liste de prix attribue à chaque logement annoncé deux places de garage et une cave, par numéro. Nous confirmons les places et la cave du logement que vous choisissez.',
  'Die Preisliste ordnet jeder gelisteten Wohnung zwei Garagenstellplätze und einen Abstellraum nach Nummer zu. Wir bestätigen die Stellplätze und den Abstellraum der von Ihnen gewählten Wohnung.',
  'В прайс-листе за каждой квартирой в списке закреплены два места в гараже и кладовая — по номерам. Мы подтверждаем места и кладовую той квартиры, которую вы выберете.',
  'تخصص قائمة الأسعار لكل مسكن مدرج موقفين في المرآب وغرفة تخزين، بالأرقام. نؤكد المواقف وغرفة التخزين الخاصة بالمسكن الذي تختارونه.',
  'De prijslijst kent elke aangeboden woning twee garageplaatsen en een berging toe, met nummer. Wij bevestigen de plaatsen en de berging van de woning die u kiest.',
  'Cennik przypisuje każdemu oferowanemu mieszkaniu dwa miejsca garażowe i komórkę lokatorską, według numerów. Miejsca i komórkę wybranego przez Państwa mieszkania potwierdzamy.',
  'Prislisten gir hver oppførte bolig to garasjeplasser og en bod, med nummer. Vi bekrefter plassene og boden til boligen dere velger.',
  'Prislistan ger varje listad bostad två garageplatser och ett förråd, med nummer. Vi bekräftar platserna och förrådet för den bostad ni väljer.')
p('.investment.cards[3][1]',
  'La memoria de calidades indica que los materiales pueden ser modificados por la dirección facultativa siempre que no se reduzca su calidad, y que no tiene carácter contractual. Pedimos la memoria definitiva.',
  'Le descriptif de qualité indique que les matériaux peuvent être modifiés par la direction de projet tant que leur qualité n’est pas réduite, et qu’il n’a pas valeur contractuelle. Nous demandons le descriptif définitif.',
  'Die Baubeschreibung weist darauf hin, dass die Materialien von der Bauleitung geändert werden können, solange ihre Qualität nicht gemindert wird, und dass sie nicht vertraglich bindend ist. Wir fordern die endgültige Baubeschreibung an.',
  'В спецификации качества сказано, что материалы может изменить руководство проекта, если их качество не снижается, и что она не имеет договорной силы. Мы запрашиваем окончательную спецификацию.',
  'تذكر مواصفات الجودة أن إدارة المشروع قد تغيّر المواد ما دامت جودتها لا تنخفض، وأنها غير ملزمة تعاقديًا. نطلب المواصفات النهائية.',
  'De kwaliteitsspecificatie vermeldt dat de materialen door de bouwleiding mogen worden gewijzigd zolang hun kwaliteit niet daalt, en dat ze niet contractueel is. Wij vragen de definitieve specificatie op.',
  'Specyfikacja jakości podaje, że kierownictwo projektu może zmieniać materiały, o ile nie obniża to ich jakości, oraz że nie ma ona charakteru umownego. Prosimy o ostateczną specyfikację.',
  'Kvalitetsspesifikasjonen oppgir at materialene kan endres av prosjektledelsen så lenge kvaliteten ikke reduseres, og at den ikke er kontraktsfestet. Vi ber om den endelige spesifikasjonen.',
  'Kvalitetsbeskrivningen anger att materialen kan ändras av projektledningen så länge kvaliteten inte sänks, och att den inte är avtalsgrundande. Vi ber om den slutliga beskrivningen.')
p('.trustDossier.cards[2][1]',
  'La lista de precios y los planos difieren en algunas cifras: la terraza de Ground A, Ground B, 3A y 4E, y la superficie construida de 2D y 3D, que es de #103.26 [m2] en la lista y de #103.49 [m2] en los planos. Los planos dan además superficies útiles y construidas según el Decreto 218/2005, por ejemplo #147.11 [m2] construidos para Ground A frente a #134.62 [m2] en la lista. Confirmamos qué cifras utiliza el contrato.',
  'La liste de prix et les plans diffèrent sur quelques chiffres : la terrasse de Ground A, Ground B, 3A et 4E, et la surface construite de 2D et 3D, qui est de #103.26 [m2] sur la liste et de #103.49 [m2] sur les plans. Les plans donnent aussi des surfaces utiles et construites selon le décret 218/2005, par exemple #147.11 [m2] construits pour Ground A contre #134.62 [m2] sur la liste. Nous confirmons quels chiffres le contrat retient.',
  'Die Preisliste und die Pläne weichen bei einigen Zahlen voneinander ab: bei der Terrasse von Ground A, Ground B, 3A und 4E und bei der bebauten Fläche von 2D und 3D, die in der Liste #103.26 [m2] und in den Plänen #103.49 [m2] beträgt. Die Pläne geben außerdem Nutz- und bebaute Flächen nach dem Dekret 218/2005 an, zum Beispiel #147.11 [m2] bebaute Fläche für Ground A gegenüber #134.62 [m2] in der Liste. Wir klären, welche Zahlen der Vertrag verwendet.',
  'Прайс-лист и планы расходятся в нескольких цифрах: терраса у Ground A, Ground B, 3A и 4E, а также застроенная площадь у 2D и 3D — #103.26 [m2] в прайс-листе и #103.49 [m2] на планах. Кроме того, на планах приведены полезные и застроенные площади по декрету 218/2005, например #147.11 [m2] застроенной площади для Ground A против #134.62 [m2] в прайс-листе. Мы уточняем, какие цифры берёт за основу договор.',
  'تختلف قائمة الأسعار والمخططات في بعض الأرقام: تراس Ground A وGround B و3A و4E، والمساحة المبنية للمسكنين 2D وَ3D التي تبلغ #103.26 [m2] في القائمة و#103.49 [m2] في المخططات. وتعطي المخططات أيضاً مساحات صالحة للاستخدام ومبنية بحسب المرسوم 218/2005، مثل #147.11 [m2] مساحة مبنية لـ Ground A مقابل #134.62 [m2] في القائمة. نؤكد الأرقام التي يعتمدها العقد.',
  'De prijslijst en de plattegronden wijken op enkele cijfers af: het terras van Ground A, Ground B, 3A en 4E, en de bebouwde oppervlakte van 2D en 3D, die op de lijst #103.26 [m2] bedraagt en op de plattegronden #103.49 [m2]. De plattegronden geven bovendien gebruiksoppervlakten en bebouwde oppervlakten volgens decreet 218/2005, bijvoorbeeld #147.11 [m2] bebouwd voor Ground A tegenover #134.62 [m2] op de lijst. Wij bevestigen welke cijfers het contract hanteert.',
  'Cennik i rzuty różnią się w kilku liczbach: taras w Ground A, Ground B, 3A i 4E oraz powierzchnia zabudowy w 2D i 3D, która w cenniku wynosi #103.26 [m2], a na rzutach #103.49 [m2]. Rzuty podają też powierzchnie użytkowe i zabudowy według dekretu 218/2005, na przykład #147.11 [m2] powierzchni zabudowy dla Ground A wobec #134.62 [m2] w cenniku. Potwierdzamy, które liczby przyjmuje umowa.',
  'Prislisten og tegningene avviker på noen tall: terrassen til Ground A, Ground B, 3A og 4E, og bebygd areal for 2D og 3D, som er #103.26 [m2] i listen og #103.49 [m2] på tegningene. Tegningene oppgir også bruksareal og bebygd areal etter dekret 218/2005, for eksempel #147.11 [m2] bebygd areal for Ground A mot #134.62 [m2] i listen. Vi bekrefter hvilke tall kontrakten bruker.',
  'Prislistan och ritningarna avviker på några siffror: terrassen hos Ground A, Ground B, 3A och 4E, och byggytan hos 2D och 3D, som är #103.26 [m2] i listan och #103.49 [m2] på ritningarna. Ritningarna anger också användbara ytor och byggytor enligt dekret 218/2005, till exempel #147.11 [m2] byggyta för Ground A mot #134.62 [m2] i listan. Vi bekräftar vilka siffror kontraktet använder.')
p('.trustDossier.cards[3][1]',
  'El folleto cuenta 76 plazas de aparcamiento y 35 trasteros, mientras que los planos de los sótanos numeran 86 plazas y 37 trasteros y la lista de precios usa números de plaza hasta el 84 y de trastero hasta el 37. Cada vivienda a la venta tiene dos plazas y un trastero. Preguntamos qué recuento es el correcto.',
  'La brochure compte 76 places de parking et 35 caves, alors que les plans des sous-sols numérotent 86 places et 37 caves et que la liste de prix utilise des numéros de place jusqu’à 84 et de cave jusqu’à 37. Chaque logement annoncé a deux places et une cave. Nous demandons quel décompte est le bon.',
  'Der Prospekt zählt 76 Stellplätze und 35 Abstellräume, während die Untergeschosspläne 86 Stellplätze und 37 Abstellräume nummerieren und die Preisliste Stellplatznummern bis 84 und Abstellraumnummern bis 37 verwendet. Jede gelistete Wohnung hat zwei Stellplätze und einen Abstellraum. Wir fragen nach, welche Zählung stimmt.',
  'В брошюре указано 76 парковочных мест и 35 кладовых, тогда как на планах подземных уровней пронумеровано 86 мест и 37 кладовых, а в прайс-листе номера мест доходят до 84, а кладовых — до 37. У каждой квартиры в списке два места и кладовая. Мы выясняем, какой подсчёт верен.',
  'يذكر الكتيّب 76 موقف سيارة و35 غرفة تخزين، بينما ترقّم مخططات الطابقين السفليين 86 موقفاً و37 غرفة تخزين، وتستخدم قائمة الأسعار أرقام مواقف حتى 84 وأرقام غرف تخزين حتى 37. ولكل مسكن مدرج موقفان وغرفة تخزين. نسأل أي العددين صحيح.',
  'De brochure telt 76 parkeerplaatsen en 35 bergingen, terwijl de plattegronden van de kelders 86 plaatsen en 37 bergingen nummeren en de prijslijst plaatsnummers tot 84 en bergingnummers tot 37 gebruikt. Elke aangeboden woning heeft twee plaatsen en een berging. Wij vragen na welke telling klopt.',
  'Broszura podaje 76 miejsc parkingowych i 35 komórek, podczas gdy rzuty poziomów podziemnych numerują 86 miejsc i 37 komórek, a cennik używa numerów miejsc do 84 i komórek do 37. Każde oferowane mieszkanie ma dwa miejsca i komórkę. Pytamy, które zestawienie jest właściwe.',
  'Brosjyren teller 76 parkeringsplasser og 35 boder, mens kjelleretegningene nummererer 86 plasser og 37 boder og prislisten bruker plassnumre til 84 og bodnumre til 37. Hver oppførte bolig har to plasser og en bod. Vi spør hvilken telling som er riktig.',
  'Broschyren räknar 76 parkeringsplatser och 35 förråd, medan källarplanritningarna numrerar 86 platser och 37 förråd och prislistan använder platsnummer upp till 84 och förrådsnummer upp till 37. Varje listad bostad har två platser och ett förråd. Vi frågar vilken räkning som stämmer.')

# 156-158 availability
p('.availability.headlineHtml', '17 de 32 viviendas <em>disponibles ahora</em>', '17 logements sur 32 <em>disponibles actuellement</em>',
  '17 von 32 Wohnungen <em>derzeit verfügbar</em>', '17 из 32 квартир <em>доступны сейчас</em>', '17 من 32 مسكناً <em>متاحة حالياً</em>',
  '17 van de 32 woningen <em>nu beschikbaar</em>', '17 z 32 mieszkań <em>dostępnych obecnie</em>', '17 av 32 boliger <em>ledige nå</em>',
  '17 av 32 bostäder <em>lediga just nu</em>')
p('.availability.copy',
  'Diecisiete viviendas figuran con precio: dos en planta baja con jardín y piscina, siete con terraza entre la primera y la tercera planta, dos en la tercera planta con piscina privada y seis áticos con solárium en la cubierta y piscina. Las otras 15 figuran como RESERVADO, reservadas, en la lista de precios del promotor con fecha de septiembre de 2026. Los precios no incluyen el 10% de IVA y se confirman antes de cualquier reserva.',
  'Dix-sept logements sont annoncés avec un prix : deux au rez-de-chaussée avec jardin et piscine, sept avec terrasse du premier au troisième étage, deux au troisième étage avec piscine privée et six penthouses avec solarium sur le toit et piscine. Les 15 autres sont indiqués RESERVADO, réservés, sur la liste de prix du promoteur datée de septembre 2026. Les prix s’entendent hors TVA de 10 % et sont confirmés avant toute réservation.',
  'Siebzehn Wohnungen sind mit Preis gelistet: zwei im Erdgeschoss mit Garten und Pool, sieben mit Terrasse im ersten bis dritten Obergeschoss, zwei im dritten Obergeschoss mit privatem Pool und sechs Penthäuser mit Dachsolarium und Pool. Die übrigen 15 sind in der Preisliste des Bauträgers mit Stand September 2026 als RESERVADO, reserviert, gekennzeichnet. Die Preise verstehen sich zuzüglich 10 % MwSt. und werden vor jeder Reservierung bestätigt.',
  'Семнадцать квартир указаны с ценой: две на первом этаже с садом и бассейном, семь с террасой на втором–четвёртом этажах, две на четвёртом этаже с частным бассейном и шесть пентхаусов с солярием на крыше и бассейном. Остальные 15 помечены RESERVADO, то есть зарезервированы, в прайс-листе застройщика за сентябрь 2026 года. Цены указаны без учёта 10% НДС и подтверждаются перед любым бронированием.',
  'تظهر سبعة عشر مسكناً بأسعارها: اثنان في الطابق الأرضي بحديقة ومسبح، وسبعة بتراس بين الطابق الأول والثالث، واثنان في الطابق الثالث بمسبح خاص، وستة بنتهاوس بسولاريوم على السطح ومسبح. أما الخمسة عشر الأخرى فمكتوب عليها RESERVADO أي محجوزة في قائمة أسعار المطوّر المؤرخة سبتمبر 2026. والأسعار لا تشمل ضريبة القيمة المضافة البالغة 10% ويُؤكَّد التوفر قبل أي حجز.',
  'Zeventien woningen staan met een prijs op de lijst: twee op de begane grond met tuin en zwembad, zeven met terras op de eerste tot en met de derde verdieping, twee op de derde verdieping met privézwembad en zes penthouses met daksolarium en zwembad. De andere 15 staan als RESERVADO, gereserveerd, op de prijslijst van de ontwikkelaar van september 2026. De prijzen zijn exclusief 10% btw en worden bevestigd vóór elke reservering.',
  'Siedemnaście mieszkań ma podaną cenę: dwa na parterze z ogrodem i basenem, siedem z tarasem na pierwszym–trzecim piętrze, dwa na trzecim piętrze z prywatnym basenem i sześć penthouse’ów z solarium na dachu i basenem. Pozostałe 15 jest oznaczonych RESERVADO, czyli zarezerwowane, w cenniku dewelopera z września 2026 roku. Ceny nie obejmują 10% VAT i są potwierdzane przed każdą rezerwacją.',
  'Sytten boliger er oppført med pris: to i første etasje med hage og basseng, sju med terrasse i andre til fjerde etasje, to i fjerde etasje med privat basseng og seks toppleiligheter med solterrasse på taket og basseng. De øvrige 15 er markert RESERVADO, reservert, i utbyggerens prisliste fra september 2026. Prisene er eksklusive 10 % mva og bekreftes før enhver reservasjon.',
  'Sjutton bostäder är listade med pris: två på bottenvåningen med trädgård och pool, sju med terrass på första till tredje våningen, två på tredje våningen med privat pool och sex takvåningar med solterrass på taket och pool. De övriga 15 är markerade RESERVADO, reserverade, i exploatörens prislista från september 2026. Priserna är exklusive 10 % IVA (spansk moms) och bekräftas före varje reservation.')
p('.availability.sourceNote',
  'Los precios, los dormitorios, las superficies construidas, las terrazas, los solariums y los jardines están transcritos de la lista de precios del promotor con fecha de septiembre de 2026, que da precio a 17 de las 32 viviendas y marca las otras 15 como reservadas. La lista indica que los precios no incluyen el 10% de IVA. Llama Bajo A y Bajo B a las dos viviendas de planta baja e indica la escalera de cada vivienda, 1 o 2. Las superficies interiores y las piscinas proceden de los planos del promotor, ya que la lista no las da. La superficie construida es la superficie construida total de los planos, sin parte proporcional de zonas comunes. Cuando los planos o el folleto difieren de la lista, en la tabla se sigue la lista y arriba se dan ambas cifras.',
  'Les prix, les chambres, les surfaces construites, les terrasses, les solariums et les jardins sont transcrits de la liste de prix du promoteur datée de septembre 2026, qui donne un prix à 17 des 32 logements et indique les 15 autres comme réservés. La liste précise que les prix s’entendent hors TVA de 10 %. Elle appelle Bajo A et Bajo B les deux logements du rez-de-chaussée et indique l’escalier de chaque logement, 1 ou 2. Les surfaces intérieures et les piscines proviennent des plans du promoteur, la liste ne les donnant pas. La surface construite est la surface construite totale des plans, sans quote-part des parties communes. Lorsque les plans ou la brochure diffèrent de la liste, le tableau suit la liste et les deux chiffres sont donnés ci-dessus.',
  'Preise, Schlafzimmer, bebaute Flächen, Terrassen, Solarien und Gärten sind der Preisliste des Bauträgers mit Stand September 2026 entnommen, die 17 der 32 Wohnungen einen Preis zuweist und die übrigen 15 als reserviert kennzeichnet. Die Liste gibt an, dass die Preise 10 % MwSt. nicht enthalten. Sie nennt die beiden Erdgeschosswohnungen Bajo A und Bajo B und gibt das Treppenhaus jeder Wohnung an, 1 oder 2. Die Innenflächen und die Pools stammen aus den Plänen des Bauträgers, da die Liste sie nicht angibt. Die bebaute Fläche ist die gesamte bebaute Fläche der Pläne, ohne Anteil an den Gemeinschaftsflächen. Wo die Pläne oder der Prospekt von der Liste abweichen, folgt die Tabelle der Liste, und oben werden beide Zahlen genannt.',
  'Цены, спальни, застроенные площади, террасы, солярии и сады приведены по прайс-листу застройщика за сентябрь 2026 года, в котором 17 из 32 квартир указаны с ценой, а остальные 15 помечены как зарезервированные. В прайс-листе сказано, что цены не включают НДС 10%. Две квартиры на первом этаже в нём названы Bajo A и Bajo B, и для каждой квартиры указана лестница — 1 или 2. Внутренние площади и бассейны взяты из планов застройщика, так как в прайс-листе их нет. Застроенная площадь — это общая застроенная площадь по планам, без доли общих зон. Там, где планы или брошюра расходятся с прайс-листом, таблица следует прайс-листу, а выше приведены обе цифры.',
  'الأسعار وغرف النوم والمساحات المبنية والتراسات والسولاريوم والحدائق منقولة من قائمة أسعار المطوّر المؤرخة سبتمبر 2026، التي تضع سعراً لـ 17 من 32 مسكناً وتعلّم الخمسة عشر الأخرى محجوزة. وتذكر القائمة أن الأسعار لا تشمل ضريبة القيمة المضافة البالغة 10%. وهي تسمي المسكنين الأرضيين Bajo A وBajo B وتذكر درج كل مسكن، 1 أو 2. أما المساحات الداخلية والمسابح فمأخوذة من مخططات المطوّر لأن القائمة لا تذكرها. والمساحة المبنية هي إجمالي المساحة المبنية في المخططات دون حصة من المرافق المشتركة. وحيث تختلف المخططات أو الكتيّب عن القائمة، يتبع الجدول القائمة وتُذكر الرقمان أعلاه.',
  'Prijzen, slaapkamers, bebouwde oppervlakten, terrassen, solariums en tuinen zijn overgenomen uit de prijslijst van de ontwikkelaar van september 2026, die 17 van de 32 woningen een prijs geeft en de andere 15 als gereserveerd aanmerkt. De lijst vermeldt dat de prijzen exclusief 10% btw zijn. Ze noemt de twee woningen op de begane grond Bajo A en Bajo B en geeft het trappenhuis van elke woning aan, 1 of 2. De binnenoppervlakten en de zwembaden komen uit de plattegronden van de ontwikkelaar, omdat de lijst ze niet geeft. De bebouwde oppervlakte is de totale bebouwde oppervlakte uit de plattegronden, zonder aandeel in de gemeenschappelijke ruimten. Waar de plattegronden of de brochure van de lijst afwijken, volgt de tabel de lijst en worden hierboven beide cijfers genoemd.',
  'Ceny, sypialnie, powierzchnie zabudowy, tarasy, solaria i ogrody przepisano z cennika dewelopera z września 2026 roku, który podaje cenę 17 z 32 mieszkań, a pozostałe 15 oznacza jako zarezerwowane. Cennik podaje, że ceny nie obejmują 10% VAT. Dwa mieszkania na parterze nazywa Bajo A i Bajo B i wskazuje klatkę schodową każdego mieszkania, 1 lub 2. Powierzchnie wewnętrzne i baseny pochodzą z planów dewelopera, ponieważ cennik ich nie podaje. Powierzchnia zabudowy to całkowita powierzchnia zabudowy z rzutów, bez udziału w częściach wspólnych. Tam, gdzie rzuty lub broszura różnią się od cennika, tabela podąża za cennikiem, a powyżej podano obie liczby.',
  'Priser, soverom, bebygd areal, terrasser, solterrasser og hager er hentet fra utbyggerens prisliste fra september 2026, som gir 17 av de 32 boligene en pris og markerer de øvrige 15 som reservert. Listen oppgir at prisene ikke inkluderer 10 % mva. Den kaller de to boligene i første etasje Bajo A og Bajo B og oppgir trappeoppgangen til hver bolig, 1 eller 2. De innvendige arealene og bassengene er hentet fra utbyggerens tegninger, siden listen ikke oppgir dem. Bebygd areal er det totale bebygde arealet fra tegningene, uten andel av fellesarealene. Der tegningene eller brosjyren avviker fra listen, følger tabellen listen, og begge tallene oppgis ovenfor.',
  'Priser, sovrum, byggytor, terrasser, solterrasser och trädgårdar är hämtade från exploatörens prislista från september 2026, som ger 17 av de 32 bostäderna ett pris och markerar de övriga 15 som reserverade. Listan anger att priserna inte inkluderar 10 % IVA. Den kallar de två bostäderna på bottenvåningen Bajo A och Bajo B och anger varje bostads trapphus, 1 eller 2. De invändiga ytorna och poolerna är hämtade från exploatörens ritningar, eftersom listan inte anger dem. Byggytan är den totala byggytan på ritningarna, utan andel av de gemensamma ytorna. Där ritningarna eller broschyren avviker från listan följer tabellen listan, och båda siffrorna anges ovan.')

# 196-204 enquiry, faq, seo
p('.enquiry.headlineHtml', 'Pregunte por <em>The Privilege</em>', 'Renseignez-vous sur <em>The Privilege</em>', 'Fragen Sie nach <em>The Privilege</em>',
  'Спросите о <em>The Privilege</em>', 'استفسروا عن <em>The Privilege</em>', 'Vraag naar <em>The Privilege</em>', 'Zapytaj o <em>The Privilege</em>',
  'Spør om <em>The Privilege</em>', 'Fråga om <em>The Privilege</em>')
p('.enquiry.message',
  'Hola Nueva Living, quisiera información sobre The Privilege.', 'Bonjour Nueva Living, je souhaiterais des informations sur The Privilege.',
  'Hallo Nueva Living, ich hätte gern Informationen zu The Privilege.', 'Здравствуйте, Nueva Living, прошу прислать информацию о The Privilege.',
  'مرحباً Nueva Living، أودّ الحصول على معلومات عن The Privilege.', 'Hallo Nueva Living, ik wil graag informatie over The Privilege.',
  'Dzień dobry, Nueva Living, proszę o informacje o The Privilege.', 'Hei Nueva Living, jeg vil gjerne ha informasjon om The Privilege.',
  'Hej Nueva Living, jag vill gärna ha information om The Privilege.')
p('.faq[0][1]',
  'El edificio tiene 32 viviendas y 17 figuran con precio: cinco de dos dormitorios y doce de tres, de €775500 a €2084500 más IVA. Las otras 15 figuran como reservadas en la lista del promotor.',
  'L’immeuble compte 32 logements et 17 sont annoncés avec un prix : cinq de deux chambres et douze de trois, de €775500 à €2084500 plus TVA. Les 15 autres sont indiqués comme réservés sur la liste du promoteur.',
  'Das Gebäude hat 32 Wohnungen, 17 davon sind mit Preis gelistet: fünf mit zwei und zwölf mit drei Schlafzimmern, von €775500 bis €2084500 plus MwSt. Die übrigen 15 sind in der Liste des Bauträgers als reserviert gekennzeichnet.',
  'В доме 32 квартиры, 17 из них указаны с ценой: пять с двумя спальнями и двенадцать с тремя, от €775500 до €2084500 плюс НДС. Остальные 15 помечены в списке застройщика как зарезервированные.',
  'يضم المبنى 32 مسكناً، منها 17 بأسعارها: خمسة بغرفتي نوم واثنا عشر بثلاث غرف نوم، من €775500 إلى €2084500 زائد ضريبة القيمة المضافة. أما الخمسة عشر الأخرى فمعلَّمة محجوزة في قائمة المطوّر.',
  'Het gebouw heeft 32 woningen en 17 staan met een prijs op de lijst: vijf met twee en twaalf met drie slaapkamers, van €775500 tot €2084500 plus btw. De andere 15 staan als gereserveerd op de lijst van de ontwikkelaar.',
  'Budynek ma 32 mieszkania, a 17 z nich ma podaną cenę: pięć z dwiema i dwanaście z trzema sypialniami, od €775500 do €2084500 plus VAT. Pozostałe 15 jest oznaczonych w liście dewelopera jako zarezerwowane.',
  'Bygningen har 32 boliger, og 17 er oppført med pris: fem med to og tolv med tre soverom, fra €775500 til €2084500 pluss mva. De øvrige 15 er markert som reservert i utbyggerens liste.',
  'Byggnaden har 32 bostäder och 17 är listade med pris: fem med två och tolv med tre sovrum, från €775500 till €2084500 plus IVA. De övriga 15 är markerade som reserverade i exploatörens lista.')
p('.faq[1][1]',
  'No. La lista de precios indica que sus precios no incluyen el 10% de IVA. Confirmamos por escrito el impuesto y los demás gastos de la compra.',
  'Non. La liste de prix indique que ses prix s’entendent hors TVA de 10 %. Nous confirmons par écrit la taxe et les autres frais d’achat.',
  'Nein. Die Preisliste gibt an, dass ihre Preise die 10 % MwSt. nicht enthalten. Wir bestätigen die Steuer und die übrigen Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе указано, что его цены не включают НДС 10%. Мы письменно подтверждаем налог и другие расходы на покупку.',
  'لا. تذكر قائمة الأسعار أن أسعارها لا تشمل ضريبة القيمة المضافة البالغة 10%. نؤكد الضريبة وسائر تكاليف الشراء كتابةً.',
  'Nee. De prijslijst vermeldt dat de prijzen exclusief 10% btw zijn. Wij bevestigen de belasting en de overige aankoopkosten schriftelijk.',
  'Nie. Cennik podaje, że jego ceny nie obejmują 10% VAT. Podatek i pozostałe koszty zakupu potwierdzamy na piśmie.',
  'Nei. Prislisten oppgir at prisene ikke inkluderer 10 % mva. Vi bekrefter skatten og de øvrige kjøpskostnadene skriftlig.',
  'Nej. Prislistan anger att priserna inte inkluderar 10 % IVA. Vi bekräftar skatten och de övriga köpkostnaderna skriftligen.')
p('.faq[2][1]',
  'Sí. La lista de precios asigna a cada una de las 17 viviendas dos plazas de garaje y un trastero, y la memoria de calidades incluye la preinstalación de carga para coche eléctrico en el garaje.',
  'Oui. La liste de prix attribue à chacun des 17 logements deux places de garage et une cave, et le descriptif prévoit le pré-équipement pour la recharge de véhicules électriques dans le garage.',
  'Ja. Laut Preisliste gehören zu jeder der 17 Wohnungen zwei Garagenstellplätze und ein Abstellraum, und die Baubeschreibung umfasst die Vorinstallation für das Laden von Elektrofahrzeugen in der Garage.',
  'Да. Согласно прайс-листу, к каждой из 17 квартир прилагаются два места в гараже и кладовая, а спецификация включает подготовку к зарядке электромобилей в гараже.',
  'نعم. تخصص قائمة الأسعار لكل مسكن من المساكن السبعة عشر موقفين في المرآب وغرفة تخزين، وتشمل المواصفات تجهيزًا مسبقًا لشحن السيارات الكهربائية في المرآب.',
  'Ja. De prijslijst kent elk van de 17 woningen twee garageplaatsen en een berging toe, en de specificatie omvat de voorbereiding voor het opladen van elektrische auto’s in de garage.',
  'Tak. Zgodnie z cennikiem każde ze 17 mieszkań ma dwa miejsca garażowe i komórkę lokatorską, a specyfikacja obejmuje przygotowanie do ładowania pojazdów elektrycznych w garażu.',
  'Ja. Prislisten gir hver av de 17 boligene to garasjeplasser og en bod, og spesifikasjonen inkluderer forberedelse for lading av elbil i garasjen.',
  'Ja. Prislistan ger var och en av de 17 bostäderna två garageplatser och ett förråd, och specifikationen inkluderar förberedelse för laddning av elbil i garaget.')
p('.faq[3][1]',
  'Ninguno de los documentos del promotor da una fecha de entrega. Pedimos la fecha contractual y el estado de las obras y los ponemos por escrito.',
  'Aucun des documents du promoteur ne donne de date de livraison. Nous demandons la date contractuelle et l’état d’avancement des travaux et les mettons par écrit.',
  'Keines der Dokumente des Bauträgers nennt einen Übergabetermin. Wir fragen das vertragliche Datum und den Stand der Bauarbeiten an und halten beides schriftlich fest.',
  'Ни в одном из документов застройщика не указан срок сдачи. Мы запрашиваем договорную дату и стадию работ и фиксируем их письменно.',
  'لا تذكر أي من وثائق المطوّر موعد تسليم. نطلب التاريخ التعاقدي ومرحلة الأعمال ونثبّتهما كتابةً.',
  'Geen van de documenten van de ontwikkelaar noemt een opleveringsdatum. Wij vragen de contractuele datum en de voortgang van de werken op en leggen beide schriftelijk vast.',
  'Żaden z dokumentów dewelopera nie podaje terminu oddania. Prosimy o termin umowny i etap prac i potwierdzamy je na piśmie.',
  'Ingen av utbyggerens dokumenter oppgir en overleveringsdato. Vi ber om den kontraktsfestede datoen og hvor langt byggearbeidene har kommet, og får begge deler skriftlig.',
  'Inget av exploatörens dokument anger ett tillträdesdatum. Vi ber om det avtalade datumet och hur långt byggarbetena har kommit och får båda skriftligen.')
p('.seo.title',
  'The Privilege - Obra nueva con piscina privada en Estepona', 'The Privilege - Logements neufs avec piscine privée à Estepona',
  'The Privilege - Neubau mit privatem Pool in Estepona', 'The Privilege - новостройка с частным бассейном в Эстепоне',
  'The Privilege - مساكن جديدة بمسبح خاص في إستيبونا', 'The Privilege - Nieuwbouw met privézwembad in Estepona',
  'The Privilege - Mieszkania z prywatnym basenem w Esteponie', 'The Privilege - Nybygg med privat basseng i Estepona',
  'The Privilege - Nybyggt med privat pool i Estepona')
p('.seo.h1',
  'The Privilege: obra nueva con piscina privada junto al casco antiguo de Estepona', 'The Privilege : logements neufs avec piscine privée à côté de la vieille ville d’Estepona',
  'The Privilege: Neubau mit privatem Pool neben der Altstadt von Estepona', 'The Privilege: новостройка с частным бассейном рядом со старым городом Эстепоны',
  'The Privilege: مساكن جديدة بمسبح خاص بجوار البلدة القديمة في إستيبونا', 'The Privilege: nieuwbouw met privézwembad naast de oude binnenstad van Estepona',
  'The Privilege: nowe mieszkania z prywatnym basenem obok starówki Estepony', 'The Privilege: nybygg med privat basseng ved siden av gamlebyen i Estepona',
  'The Privilege: nybyggt med privat pool intill gamla stan i Estepona')
p('.seo.h1Context',
  'Obra nueva con piscina privada junto al casco antiguo de Estepona', 'Logements neufs avec piscine privée à côté de la vieille ville d’Estepona',
  'Neubau mit privatem Pool neben der Altstadt von Estepona', 'Новостройка с частным бассейном рядом со старым городом Эстепоны',
  'مساكن جديدة بمسبح خاص بجوار البلدة القديمة في إستيبونا', 'Nieuwbouw met privézwembad naast de oude binnenstad van Estepona',
  'Nowe mieszkania z prywatnym basenem obok starówki Estepony', 'Nybygg med privat basseng ved siden av gamlebyen i Estepona',
  'Nybyggt med privat pool intill gamla stan i Estepona')

# ---- finish ---------------------------------------------------------------------------------
missing = [pth for pth in BY_PATH if pth not in USED]
if missing:
    for pth in missing:
        print('NOT COVERED', pth, '|', BY_PATH[pth][:90])
json.dump(T, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries,', len(missing), 'paths not covered')
