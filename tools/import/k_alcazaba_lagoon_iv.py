# -*- coding: utf-8 -*-
# Alcazaba Lagoon IV (Casares), human translations in one pass.
# p(path, es, fr, de, ru, ar, nl, pl, no, sv)
#
# The English string is looked up from the path scaffold.py printed in todo.json, so it is never
# copied here and cannot drift from project.json.
#
# Tokens expanded per locale, so a figure is written once and takes its locale's own format:
# EUR amounts written as euro-sign + digits (615000) become "615.000 €" (nl "€ 615.000", fr/ru/pl/no/sv
# "615 000 €", ar "615,000 €"); every two-decimal area (107.57) takes the locale's decimal mark
# (a comma, but a point in Arabic); and [m2] is the area unit: m² everywhere but ru "м²" and ar "م²".
# Spanish IVA is "IVA" in es and sv, "TVA" in fr, "MwSt." in de, "НДС" in ru, "ضريبة القيمة المضافة" in ar,
# "btw" in nl, "VAT" in pl and "mva." in no, as in the sibling projects; the first Swedish mention
# is glossed "(spansk moms)".
#
#   python3 tools/import/k_alcazaba_lagoon_iv.py <workdir>/tr_z.json <workdir>/todo.json
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
    if loc != 'ar':
        s = re.sub(r'(?<![\d.])(\d+)\.(\d{2})(?!\d)', r'\1,\2', s)
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
    if en in ('Alcazaba Lagoon IV', 'Alcazaba Lagoon <em>IV</em>', 'AL4-1924') or path.endswith('.phase') and en == '':
        T[en] = {l: en for l in LOCS}
        USED.add(path)

# ---- the unit row and the floorplan labels, built from the same numbers the English was -------
WORDS = {
    'es': dict(built='m² construidos', terraces='m² de terrazas', solarium='m² de solárium'),
    'fr': dict(built='m² construits', terraces='m² de terrasses', solarium='m² de solarium'),
    'de': dict(built='m² bebaut', terraces='m² Terrassen', solarium='m² Solarium'),
    'nl': dict(built='m² bebouwd', terraces='m² terrassen', solarium='m² solarium'),
    'pl': dict(built='m² zabudowy', terraces='m² tarasów', solarium='m² solarium'),
    'no': dict(built='m² bebygd', terraces='m² terrasser', solarium='m² solterrasse'),
    'sv': dict(built='m² byggyta', terraces='m² terrasser', solarium='m² solterrass'),
}


def size_row(en, loc):
    out = []
    for seg in [s.strip() for s in re.split(r',\s+', en)]:
        m = re.fullmatch(r'([\d.]+) sqm (built|terraces|solarium)', seg)
        assert m, seg
        num = m.group(1).replace('.', '.' if loc == 'ar' else ',')
        kind = m.group(2)
        if loc == 'ru':
            out.append({'built': f'{num} м² застроенной площади', 'terraces': f'террасы {num} м²', 'solarium': f'солярий {num} м²'}[kind])
        elif loc == 'ar':
            out.append({'built': f'{num} م² مبنية', 'terraces': f'{num} م² تراسات', 'solarium': f'{num} م² سولاريوم'}[kind])
        else:
            out.append(f'{num} {WORDS[loc][kind]}')
    return ('، ' if loc == 'ar' else ', ').join(out)


for path, en in BY_PATH.items():
    if path.startswith('.availability.units[') and path.endswith('.size'):
        T[en] = {l: size_row(en, l) for l in LOCS}
        USED.add(path)

FP_ALT2 = dict(es='Plano de la vivienda {}, segunda planta del bloque 19', fr='Plan du logement {}, deuxième étage du bloc 19',
               de='Grundriss der Wohnung {}, zweites Obergeschoss von Block 19', ru='Планировка квартиры {}, третий этаж блока 19',
               ar='مخطط المسكن {}، الطابق الثاني من المبنى 19', nl='Plattegrond van woning {}, tweede verdieping van blok 19',
               pl='Rzut mieszkania {}, drugie piętro bloku 19', no='Plantegning av bolig {}, andre etasje i hus 19',
               sv='Planritning för bostad {}, andra våningen i hus 19')
FP_ALT_SOL = dict(es='Plano del solárium de la vivienda {}', fr='Plan du solarium du logement {}', de='Grundriss des Solariums der Wohnung {}',
                  ru='Планировка солярия квартиры {}', ar='مخطط سولاريوم المسكن {}', nl='Plattegrond van het solarium van woning {}',
                  pl='Rzut solarium mieszkania {}', no='Plantegning av solterrassen til bolig {}', sv='Planritning för solterrassen till bostad {}')
FP_CAP2 = dict(es='Vivienda {}, segunda planta', fr='Logement {}, deuxième étage', de='Wohnung {}, zweites Obergeschoss',
               ru='Квартира {}, третий этаж', ar='المسكن {}، الطابق الثاني', nl='Woning {}, tweede verdieping',
               pl='Mieszkanie {}, drugie piętro', no='Bolig {}, andre etasje', sv='Bostad {}, andra våningen')
FP_CAP_SOL = dict(es='Vivienda {}, solárium', fr='Logement {}, solarium', de='Wohnung {}, Solarium', ru='Квартира {}, солярий',
                  ar='المسكن {}، السولاريوم', nl='Woning {}, solarium', pl='Mieszkanie {}, solarium', no='Bolig {}, solterrasse',
                  sv='Bostad {}, solterrass')
HOME_NAME = dict(es='Vivienda {}', fr='Logement {}', de='Wohnung {}', ru='Квартира {}', ar='المسكن {}', nl='Woning {}',
                 pl='Mieszkanie {}', no='Bolig {}', sv='Bostad {}')
for path, en in BY_PATH.items():
    m = re.fullmatch(r'Floorplan of home (\S+), second floor of block 19', en)
    if m: T[en] = {l: FP_ALT2[l].format(m.group(1)) for l in LOCS}; USED.add(path)
    m = re.fullmatch(r'Floorplan of the solarium of home (\S+)', en)
    if m: T[en] = {l: FP_ALT_SOL[l].format(m.group(1)) for l in LOCS}; USED.add(path)
    m = re.fullmatch(r'Home (\S+), second floor', en)
    if m: T[en] = {l: FP_CAP2[l].format(m.group(1)) for l in LOCS}; USED.add(path)
    m = re.fullmatch(r'Home (\S+), solarium', en)
    if m: T[en] = {l: FP_CAP_SOL[l].format(m.group(1)) for l in LOCS}; USED.add(path)
    m = re.fullmatch(r'Home (AL4-\d+)', en)
    if m and path.startswith('.residences.items['):
        T[en] = {l: HOME_NAME[l].format(m.group(1)) for l in LOCS}; USED.add(path)

# ---- the enquiry block, from the sibling that already carries the shared wording -----------------
VERDEMAR = json.load(open('content/liora-projects/verdemar-residences/project.json'))['i18n']
for path, getter in (('.enquiry.headlineHtml', lambda o: o['enquiry']['headlineHtml']),
                     ('.enquiry.message', lambda o: o['enquiry']['message'])):
    en = BY_PATH[path]
    T[en] = {l: getter(VERDEMAR[l]).replace('Verdemar Residences', 'Alcazaba Lagoon IV') for l in LOCS}
    assert all('Verdemar' not in v for v in T[en].values()), path
    USED.add(path)

# ================================ translated prose ==============================================
# 2 description
p('.description',
  'Un apartamento terminado de dos dormitorios a la venta en la Fase IV de Alcazaba Lagoon, en Casares, con 55.52 [m2] de terrazas y un solárium de 109.60 [m2], en una urbanización con piscina, jardines tropicales y zona de juegos infantil. €615000 más IVA.',
  'Un appartement achevé de deux chambres à vendre dans la phase IV d’Alcazaba Lagoon, à Casares, avec 55.52 [m2] de terrasses et un solarium de 109.60 [m2], dans un ensemble avec piscine, jardins tropicaux et aire de jeux pour enfants. €615000 plus TVA.',
  'Eine fertiggestellte Wohnung mit zwei Schlafzimmern zum Verkauf in Phase IV von Alcazaba Lagoon in Casares, mit 55.52 [m2] Terrassen und einem Solarium von 109.60 [m2], in einer Anlage mit Pool, tropischen Gärten und Kinderspielplatz. €615000 plus MwSt.',
  'Одна готовая квартира с двумя спальнями в IV очереди Alcazaba Lagoon в Касаресе: террасы 55.52 [m2] и солярий 109.60 [m2], в комплексе с бассейном, тропическими садами и детской площадкой. €615000 плюс НДС.',
  'شقة واحدة جاهزة بغرفتي نوم معروضة للبيع في المرحلة الرابعة من Alcazaba Lagoon في كاساريس، مع تراسات بمساحة 55.52 [m2] وسولاريوم بمساحة 109.60 [m2]، في مجمّع فيه مسبح وحدائق استوائية ومنطقة ألعاب للأطفال. €615000 زائد ضريبة القيمة المضافة.',
  'Eén afgewerkt appartement met twee slaapkamers te koop in fase IV van Alcazaba Lagoon in Casares, met 55.52 [m2] terrassen en een solarium van 109.60 [m2], in een complex met zwembad, tropische tuinen en een speeltuin. €615000 plus btw.',
  'Jedno ukończone mieszkanie z dwiema sypialniami w sprzedaży w etapie IV Alcazaba Lagoon w Casares, z tarasami o powierzchni 55.52 [m2] i solarium o powierzchni 109.60 [m2], na osiedlu z basenem, tropikalnymi ogrodami i placem zabaw. €615000 plus VAT.',
  'Én ferdigstilt leilighet med to soverom til salgs i fase IV av Alcazaba Lagoon i Casares, med 55.52 [m2] terrasser og en solterrasse på 109.60 [m2], i et anlegg med basseng, tropiske hager og lekeplass. €615000 pluss mva.',
  'En färdigställd lägenhet med två sovrum till salu i etapp IV av Alcazaba Lagoon i Casares, med terrasser på 55.52 [m2] och en solterrass på 109.60 [m2], i ett område med pool, tropiska trädgårdar och lekplats. €615000 plus IVA (spansk moms).')

# 3 seoDescription
p('.seoDescription',
  'Un apartamento terminado de dos dormitorios en la Fase IV de Alcazaba Lagoon, Casares: 107.57 [m2] construidos, 55.52 [m2] de terrazas y un solárium de 109.60 [m2], €615000 más IVA.',
  'Un appartement achevé de deux chambres dans la phase IV d’Alcazaba Lagoon, à Casares : 107.57 [m2] construits, 55.52 [m2] de terrasses et un solarium de 109.60 [m2], €615000 plus TVA.',
  'Eine fertiggestellte Wohnung mit zwei Schlafzimmern in Phase IV von Alcazaba Lagoon, Casares: 107.57 [m2] bebaut, 55.52 [m2] Terrassen und ein Solarium von 109.60 [m2], €615000 plus MwSt.',
  'Одна готовая квартира с двумя спальнями в IV очереди Alcazaba Lagoon, Касарес: 107.57 [m2] застроенной площади, террасы 55.52 [m2] и солярий 109.60 [m2], €615000 плюс НДС.',
  'شقة واحدة جاهزة بغرفتي نوم في المرحلة الرابعة من Alcazaba Lagoon في كاساريس: 107.57 [m2] مبنية و55.52 [m2] تراسات وسولاريوم بمساحة 109.60 [m2]، €615000 زائد ضريبة القيمة المضافة.',
  'Eén afgewerkt appartement met twee slaapkamers in fase IV van Alcazaba Lagoon, Casares: 107.57 [m2] bebouwd, 55.52 [m2] terrassen en een solarium van 109.60 [m2], €615000 plus btw.',
  'Jedno ukończone mieszkanie z dwiema sypialniami w etapie IV Alcazaba Lagoon, Casares: 107.57 [m2] zabudowy, tarasy 55.52 [m2] i solarium 109.60 [m2], €615000 plus VAT.',
  'Én ferdigstilt leilighet med to soverom i fase IV av Alcazaba Lagoon, Casares: 107.57 [m2] bebygd, 55.52 [m2] terrasser og en solterrasse på 109.60 [m2], €615000 pluss mva.',
  'En färdigställd lägenhet med två sovrum i etapp IV av Alcazaba Lagoon, Casares: 107.57 [m2] byggyta, terrasser på 55.52 [m2] och en solterrass på 109.60 [m2], €615000 plus IVA.')

# 4 twitterDescription
p('.twitterDescription',
  'Un apartamento terminado de dos dormitorios con solárium en Casares, €615000 más IVA.',
  'Un appartement achevé de deux chambres avec solarium à Casares, €615000 plus TVA.',
  'Eine fertiggestellte Wohnung mit zwei Schlafzimmern und Solarium in Casares, €615000 plus MwSt.',
  'Одна готовая квартира с двумя спальнями и солярием в Касаресе, €615000 плюс НДС.',
  'شقة واحدة جاهزة بغرفتي نوم وسولاريوم في كاساريس، €615000 زائد ضريبة القيمة المضافة.',
  'Eén afgewerkt appartement met twee slaapkamers en een solarium in Casares, €615000 plus btw.',
  'Jedno ukończone mieszkanie z dwiema sypialniami i solarium w Casares, €615000 plus VAT.',
  'Én ferdigstilt leilighet med to soverom og solterrasse i Casares, €615000 pluss mva.',
  'En färdigställd lägenhet med två sovrum och solterrass i Casares, €615000 plus IVA.')

# 5 hero.startingPrice, 7 card.meta
p('.hero.startingPrice',
  'Desde €615000 + IVA', 'À partir de €615000 + TVA', 'Ab €615000 + MwSt.', 'От €615000 + НДС', 'ابتداءً من €615000 + ضريبة القيمة المضافة',
  'Vanaf €615000 + btw', 'Od €615000 + VAT', 'Fra €615000 + mva.', 'Från €615000 + IVA')
p('.card.meta[0][1]',
  '€615000 + IVA', '€615000 + TVA', '€615000 + MwSt.', '€615000 + НДС', '€615000 + ضريبة القيمة المضافة',
  '€615000 + btw', '€615000 + VAT', '€615000 + mva.', '€615000 + IVA')

# 6 card.description
p('.card.description',
  'Un apartamento terminado de dos dormitorios en la Fase IV de Alcazaba Lagoon, Casares, con 55.52 [m2] de terrazas y un solárium de 109.60 [m2], desde €615000 + IVA.',
  'Un appartement achevé de deux chambres dans la phase IV d’Alcazaba Lagoon, à Casares, avec 55.52 [m2] de terrasses et un solarium de 109.60 [m2], à partir de €615000 + TVA.',
  'Eine fertiggestellte Wohnung mit zwei Schlafzimmern in Phase IV von Alcazaba Lagoon, Casares, mit 55.52 [m2] Terrassen und einem Solarium von 109.60 [m2], ab €615000 + MwSt.',
  'Одна готовая квартира с двумя спальнями в IV очереди Alcazaba Lagoon, Касарес: террасы 55.52 [m2] и солярий 109.60 [m2], от €615000 + НДС.',
  'شقة واحدة جاهزة بغرفتي نوم في المرحلة الرابعة من Alcazaba Lagoon في كاساريس، مع تراسات بمساحة 55.52 [m2] وسولاريوم بمساحة 109.60 [m2]، ابتداءً من €615000 + ضريبة القيمة المضافة.',
  'Eén afgewerkt appartement met twee slaapkamers in fase IV van Alcazaba Lagoon, Casares, met 55.52 [m2] terrassen en een solarium van 109.60 [m2], vanaf €615000 + btw.',
  'Jedno ukończone mieszkanie z dwiema sypialniami w etapie IV Alcazaba Lagoon w Casares, z tarasami 55.52 [m2] i solarium 109.60 [m2], od €615000 + VAT.',
  'Én ferdigstilt leilighet med to soverom i fase IV av Alcazaba Lagoon i Casares, med 55.52 [m2] terrasser og en solterrasse på 109.60 [m2], fra €615000 + mva.',
  'En färdigställd lägenhet med två sovrum i etapp IV av Alcazaba Lagoon i Casares, med terrasser på 55.52 [m2] och en solterrass på 109.60 [m2], från €615000 + IVA.')

# 8-11 section image alts
p('.images.hero.alt',
  'Fotografía de un bloque blanco de apartamentos con terrazas junto a un césped y el borde de la piscina',
  'Photographie d’un immeuble blanc avec terrasses, à côté d’une pelouse et du bord de la piscine',
  'Foto eines weißen Apartmentblocks mit Terrassen neben einer Rasenfläche und dem Beckenrand des Pools',
  'Фотография белого жилого блока с террасами рядом с газоном и краем бассейна',
  'صورة فوتوغرافية لمبنى سكني أبيض بتراسات بجوار مرج وحافة المسبح',
  'Foto van een wit appartementengebouw met terrassen naast een grasveld en de rand van het zwembad',
  'Zdjęcie białego bloku z tarasami obok trawnika i krawędzi basenu',
  'Fotografi av en hvit leilighetsblokk med terrasser ved siden av en plen og kanten av bassenget',
  'Fotografi av ett vitt lägenhetshus med terrasser intill en gräsmatta och poolkanten')
p('.images.architecture.alt',
  'Fotografía de un bloque blanco de tres plantas sobre un muro de jardín de piedra, con un camino pavimentado y escalones entre el césped',
  'Photographie d’un immeuble blanc de trois étages au-dessus d’un mur de jardin en pierre, avec un chemin dallé et des marches dans la pelouse',
  'Foto eines weißen dreigeschossigen Blocks über einer Gartenmauer aus Naturstein, mit einem gepflasterten Weg und Stufen durch den Rasen',
  'Фотография белого трёхэтажного блока над каменной садовой подпорной стенкой, с мощёной дорожкой и ступенями на газоне',
  'صورة فوتوغرافية لمبنى أبيض من ثلاثة طوابق فوق جدار حديقة حجري، مع ممر مرصوف ودرجات عبر المرج',
  'Foto van een wit gebouw van drie verdiepingen boven een tuinmuur van natuursteen, met een bestraat pad en trappen door het gras',
  'Zdjęcie białego trzykondygnacyjnego bloku nad kamiennym murem ogrodowym, z brukowaną ścieżką i schodami przez trawnik',
  'Fotografi av en hvit blokk i tre etasjer over en hagemur av stein, med en brolagt sti og trapper gjennom plenen',
  'Fotografi av ett vitt trevåningshus ovanför en trädgårdsmur av sten, med en stenlagd gång och trappsteg genom gräsmattan')
p('.images.lifestyle.alt',
  'Fotografía de la piscina comunitaria con tumbonas, palmeras y un bloque blanco al fondo',
  'Photographie de la piscine commune avec des bains de soleil, des palmiers et un immeuble blanc au fond',
  'Foto des Gemeinschaftspools mit Sonnenliegen, Palmen und einem weißen Block dahinter',
  'Фотография общего бассейна с шезлонгами, пальмами и белым блоком вдалеке',
  'صورة فوتوغرافية للمسبح المشترك مع كراسي استلقاء ونخيل ومبنى أبيض في الخلفية',
  'Foto van het gemeenschappelijke zwembad met ligbedden, palmbomen en een wit gebouw erachter',
  'Zdjęcie wspólnego basenu z leżakami, palmami i białym blokiem w tle',
  'Fotografi av fellesbassenget med solsenger, palmer og en hvit blokk bak',
  'Fotografi av den gemensamma poolen med solstolar, palmer och ett vitt hus bakom')
p('.images.privateViewing.alt',
  'Fotografía de una zona de salón y comedor amueblada con la cocina y una barra de desayuno al fondo',
  'Photographie d’un séjour et d’un coin repas meublés, avec la cuisine et un bar de petit-déjeuner au fond',
  'Foto eines möblierten Wohn- und Essbereichs mit der Küche und einer Frühstücksbar dahinter',
  'Фотография обставленной гостиной со столовой, за которой видны кухня и барная стойка',
  'صورة فوتوغرافية لمنطقة جلوس وطعام مفروشة يظهر خلفها المطبخ وبار للفطور',
  'Foto van een gemeubileerd woon- en eetgedeelte met daarachter de keuken en een ontbijtbar',
  'Zdjęcie umeblowanej części dziennej z jadalnią, a za nią kuchnia i bar śniadaniowy',
  'Fotografi av et møblert oppholds- og spiseområde med kjøkkenet og en frokostbar bak',
  'Fotografi av en möblerad vardagsrums- och matplats med köket och en frukostbar bakom')

# 12-13 media
p('.media.copy',
  'Fotografías de la urbanización y de un interior amueblado, y los planos del apartamento disponible.',
  'Photographies de l’ensemble et d’un intérieur meublé, et les plans de l’appartement disponible.',
  'Fotos der Anlage und eines möblierten Innenraums sowie die Grundrisse der verfügbaren Wohnung.',
  'Фотографии комплекса и обставленного интерьера, а также планировки доступной квартиры.',
  'صور فوتوغرافية للمجمّع ولمساحة داخلية مفروشة، ومخططات الشقة المتاحة.',
  'Foto’s van het complex en van een gemeubileerd interieur, en de plattegronden van het beschikbare appartement.',
  'Zdjęcia osiedla i umeblowanego wnętrza oraz rzuty dostępnego mieszkania.',
  'Fotografier av anlegget og av et møblert interiør, og plantegningene av den tilgjengelige leiligheten.',
  'Fotografier av området och av en möblerad interiör, samt planritningarna för den tillgängliga lägenheten.')
p('.media.note',
  'Son fotografías de la urbanización terminada. Las fotografías de interior muestran una vivienda amueblada; el mobiliario y la decoración no están incluidos, y los documentos no indican qué vivienda aparece. Los planos son el plano del promotor de la vivienda AL4-1924, y las superficies que figuran en ellos son aproximadas. Los nombres de las estancias en los planos están en español.',
  'Ce sont des photographies de l’ensemble achevé. Les photographies d’intérieur montrent un logement meublé ; le mobilier et la décoration ne sont pas inclus, et les documents n’indiquent pas de quel logement il s’agit. Les plans sont le plan du promoteur du logement AL4-1924, et les surfaces qui y figurent sont approximatives. Les noms des pièces sur les plans sont en espagnol.',
  'Dies sind Fotos der fertiggestellten Anlage. Die Innenaufnahmen zeigen eine möblierte Wohnung; Möbel und Dekoration sind nicht enthalten, und die Unterlagen geben nicht an, welche Wohnung gezeigt wird. Die Grundrisse sind der Plan des Bauträgers für die Wohnung AL4-1924, und die darauf angegebenen Flächen sind ungefähre Werte. Die Raumbezeichnungen auf den Plänen sind spanisch.',
  'Это фотографии построенного комплекса. На фотографиях интерьера показана обставленная квартира; мебель и декор не входят в стоимость, а в документах не указано, какая именно квартира показана. Планировки — это план застройщика для квартиры AL4-1924, а указанные на них площади приблизительные. Названия помещений на планах даны по-испански.',
  'هذه صور فوتوغرافية للمجمّع بعد اكتماله. تُظهر صور الداخل مسكناً مفروشاً؛ والأثاث والديكور غير مشمولين، ولا تذكر الوثائق أي مسكن هو المعروض. المخططات هي مخطط المطوّر للمسكن AL4-1924، والمساحات الواردة فيها تقريبية. وأسماء الغرف في المخططات بالإسبانية.',
  'Dit zijn foto’s van het opgeleverde complex. De interieurfoto’s tonen een gemeubileerde woning; het meubilair en de aankleding zijn niet inbegrepen, en de documenten vermelden niet welke woning te zien is. De plattegronden zijn het plan van de ontwikkelaar voor woning AL4-1924, en de oppervlakten erop zijn bij benadering. De namen van de ruimtes op de plattegronden zijn in het Spaans.',
  'To zdjęcia ukończonego osiedla. Zdjęcia wnętrz przedstawiają umeblowane mieszkanie; meble i wystrój nie są w cenie, a dokumenty nie wskazują, które mieszkanie jest pokazane. Rzuty to plan dewelopera mieszkania AL4-1924, a podane na nich powierzchnie są przybliżone. Nazwy pomieszczeń na rzutach są po hiszpańsku.',
  'Dette er fotografier av det ferdige anlegget. Interiørbildene viser en møblert bolig; møbler og dekor er ikke inkludert, og dokumentene oppgir ikke hvilken bolig som vises. Plantegningene er utbyggerens plan for bolig AL4-1924, og arealene på dem er omtrentlige. Romnavnene på plantegningene er på spansk.',
  'Detta är fotografier av det färdiga området. Interiörbilderna visar en möblerad bostad; möbler och inredning ingår inte, och handlingarna anger inte vilken bostad som visas. Planritningarna är exploatörens ritning för bostad AL4-1924, och ytorna på dem är ungefärliga. Rumsnamnen på ritningarna är på spanska.')

# 14-33 media items
p('.media.items[0].caption',
  'El bloque junto al césped de la piscina', 'L’immeuble à côté de la pelouse de la piscine', 'Der Block neben der Poolwiese', 'Блок рядом с газоном у бассейна',
  'المبنى بجوار مرج المسبح', 'Het gebouw naast het gazon bij het zwembad', 'Blok obok trawnika przy basenie', 'Blokken ved plenen rundt bassenget', 'Huset intill poolgräsmattan')
p('.media.items[1].caption',
  'Camino y escalones bajo el bloque', 'Chemin et marches au pied de l’immeuble', 'Weg und Stufen unterhalb des Blocks', 'Дорожка и ступени под блоком',
  'ممر ودرجات أسفل المبنى', 'Pad en trappen onder het gebouw', 'Ścieżka i schody pod blokiem', 'Sti og trapper under blokken', 'Gång och trappsteg nedanför huset')
p('.media.items[2].alt',
  'Fotografía de un bloque blanco con una pérgola y una escalera de caracol hasta la cubierta, visto desde el jardín entre flores moradas',
  'Photographie d’un immeuble blanc avec une pergola et un escalier en colimaçon jusqu’au toit, vu du jardin à travers des fleurs violettes',
  'Foto eines weißen Blocks mit einer Pergola und einer Wendeltreppe zum Dach, vom Garten aus durch violette Blumen gesehen',
  'Фотография белого блока с перголой и винтовой лестницей на крышу, вид из сада сквозь фиолетовые цветы',
  'صورة فوتوغرافية لمبنى أبيض بمظلة بيرغولا ودرج حلزوني إلى السطح، من الحديقة عبر زهور بنفسجية',
  'Foto van een wit gebouw met een pergola en een wenteltrap naar het dak, gezien vanuit de tuin door paarse bloemen',
  'Zdjęcie białego bloku z pergolą i spiralnymi schodami na dach, widok z ogrodu przez fioletowe kwiaty',
  'Fotografi av en hvit blokk med en pergola og en spiraltrapp til taket, sett fra hagen gjennom lilla blomster',
  'Fotografi av ett vitt hus med en pergola och en spiraltrappa till taket, sett från trädgården genom lila blommor')
p('.media.items[2].caption',
  'El bloque sobre el jardín', 'L’immeuble au-dessus du jardin', 'Der Block über dem Garten', 'Блок над садом',
  'المبنى فوق الحديقة', 'Het gebouw boven de tuin', 'Blok nad ogrodem', 'Blokken over hagen', 'Huset ovanför trädgården')
p('.media.items[3].alt',
  'Fotografía de un bloque blanco con terrazas sobre una ladera de césped y un muro de piedra',
  'Photographie d’un immeuble blanc à terrasses au-dessus d’un talus engazonné et d’un mur en pierre',
  'Foto eines weißen Terrassenblocks über einem Rasenhang mit einer Natursteinmauer',
  'Фотография белого террасного блока над травянистым склоном с каменной стенкой',
  'صورة فوتوغرافية لمبنى أبيض مدرّج التراسات فوق منحدر عشبي وجدار حجري',
  'Foto van een wit terrassengebouw boven een grashelling met een natuurstenen muur',
  'Zdjęcie białego tarasowego bloku nad trawiastą skarpą z kamiennym murem',
  'Fotografi av en hvit terrasseblokk over en gresskledd skråning med en steinmur',
  'Fotografi av ett vitt terrasshus ovanför en gräsbevuxen slänt med en stenmur')
p('.media.items[3].caption',
  'El bloque desde la pendiente', 'L’immeuble vu du talus', 'Der Block vom Hang aus', 'Блок со стороны склона',
  'المبنى من المنحدر', 'Het gebouw vanaf de helling', 'Blok widziany ze skarpy', 'Blokken sett fra skråningen', 'Huset sett från slänten')
p('.media.items[5].alt',
  'Fotografía de una piscina pequeña sobre el césped, con una palmera y un bloque de apartamentos blanco detrás',
  'Photographie d’une petite piscine sur une pelouse, avec un palmier et un immeuble blanc derrière',
  'Foto eines kleinen Pools auf einer Rasenfläche, mit einer Palme und einem weißen Apartmentblock dahinter',
  'Фотография небольшого бассейна на газоне с пальмой и белым жилым блоком позади',
  'صورة فوتوغرافية لمسبح صغير على المرج مع نخلة ومبنى سكني أبيض خلفه',
  'Foto van een klein zwembad op een grasveld, met een palmboom en een wit appartementengebouw erachter',
  'Zdjęcie małego basenu na trawniku z palmą i białym blokiem w tle',
  'Fotografi av et lite basseng på en plen, med en palme og en hvit leilighetsblokk bak',
  'Fotografi av en liten pool på en gräsmatta, med en palm och ett vitt lägenhetshus bakom')
p('.media.items[5].caption',
  'Una piscina pequeña en el césped', 'Une petite piscine sur la pelouse', 'Ein kleiner Pool auf der Rasenfläche', 'Небольшой бассейн на газоне',
  'مسبح صغير على المرج', 'Een klein zwembad op het gazon', 'Mały basen na trawniku', 'Et lite basseng på plenen', 'En liten pool på gräsmattan')
p('.media.items[6].alt',
  'Fotografía de un salón abierto amueblado con una isla de cocina y puertas correderas de cristal al jardín',
  'Photographie d’un séjour ouvert meublé avec un îlot de cuisine et des portes coulissantes vitrées donnant sur le jardin',
  'Foto eines möblierten offenen Wohnbereichs mit einer Kücheninsel und gläsernen Schiebetüren zum Garten',
  'Фотография обставленной открытой гостиной с кухонным островом и стеклянными раздвижными дверями в сад',
  'صورة فوتوغرافية لصالة مفتوحة مفروشة مع جزيرة مطبخ وأبواب زجاجية منزلقة نحو الحديقة',
  'Foto van een gemeubileerde open woonkamer met een keukeneiland en glazen schuifdeuren naar de tuin',
  'Zdjęcie umeblowanego otwartego salonu z wyspą kuchenną i przesuwnymi szklanymi drzwiami do ogrodu',
  'Fotografi av en møblert åpen stue med en kjøkkenøy og skyvedører i glass ut mot hagen',
  'Fotografi av ett möblerat öppet vardagsrum med en köksö och skjutdörrar i glas mot trädgården')
p('.media.items[8].alt',
  'Fotografía de una mesa de comedor redonda junto a puertas correderas de cristal, con una pared de madera iluminada desde arriba',
  'Photographie d’une table à manger ronde près de portes coulissantes vitrées, avec un mur en bois éclairé par le haut',
  'Foto eines runden Esstisches an gläsernen Schiebetüren, mit einer von oben beleuchteten Holzwand',
  'Фотография круглого обеденного стола у стеклянных раздвижных дверей, со стеной из дерева с подсветкой сверху',
  'صورة فوتوغرافية لطاولة طعام دائرية قرب أبواب زجاجية منزلقة، مع جدار خشبي مضاء من الأعلى',
  'Foto van een ronde eettafel bij glazen schuifdeuren, met een houten wand die van bovenaf wordt verlicht',
  'Zdjęcie okrągłego stołu jadalnianego przy przesuwnych szklanych drzwiach, z drewnianą ścianą oświetloną od góry',
  'Fotografi av et rundt spisebord ved skyvedører i glass, med en trevegg som er belyst ovenfra',
  'Fotografi av ett runt matbord vid skjutdörrar i glas, med en träpanelvägg som är belyst uppifrån')
p('.media.items[9].alt',
  'Fotografía de una cocina blanca con encimera oscura, mirando hacia el recibidor y la puerta de entrada',
  'Photographie d’une cuisine blanche avec un plan de travail sombre, avec vue sur l’entrée et la porte d’entrée',
  'Foto einer weißen Einbauküche mit dunkler Arbeitsplatte, mit Blick zum Flur und zur Wohnungstür',
  'Фотография белой кухни с тёмной столешницей, вид в сторону прихожей и входной двери',
  'صورة فوتوغرافية لمطبخ أبيض بسطح عمل داكن، بإطلالة نحو المدخل وباب الشقة',
  'Foto van een witte keuken met een donker werkblad, met zicht op de hal en de voordeur',
  'Zdjęcie białej kuchni z ciemnym blatem, z widokiem na przedpokój i drzwi wejściowe',
  'Fotografi av et hvitt kjøkken med mørk benkeplate, sett mot gangen og inngangsdøren',
  'Fotografi av ett vitt kök med mörk bänkskiva, med utsikt mot hallen och ytterdörren')
p('.media.items[9].caption',
  'Cocina y recibidor', 'Cuisine et entrée', 'Küche und Flur', 'Кухня и прихожая', 'المطبخ والمدخل', 'Keuken en hal', 'Kuchnia i przedpokój', 'Kjøkken og gang', 'Kök och hall')
p('.media.items[10].alt',
  'Fotografía de la zona de estar abierta con una barra de desayuno, tres taburetes y una pared de madera',
  'Photographie du séjour ouvert avec un bar de petit-déjeuner, trois tabourets et un mur en bois',
  'Foto des offenen Wohnbereichs mit einer Frühstücksbar, drei Hockern und einer Holzwand',
  'Фотография открытой гостиной с барной стойкой, тремя стульями и стеной из дерева',
  'صورة فوتوغرافية لمنطقة الجلوس المفتوحة مع بار للفطور وثلاثة كراسٍ عالية وجدار خشبي',
  'Foto van het open woongedeelte met een ontbijtbar, drie krukken en een houten wand',
  'Zdjęcie otwartej części dziennej z barem śniadaniowym, trzema stołkami i drewnianą ścianą',
  'Fotografi av det åpne oppholdsområdet med en frokostbar, tre krakker og en trevegg',
  'Fotografi av den öppna vardagsytan med en frukostbar, tre barstolar och en träpanelvägg')
p('.media.items[10].caption',
  'Salón abierto y barra de desayuno', 'Séjour ouvert et bar de petit-déjeuner', 'Offener Wohnbereich und Frühstücksbar', 'Открытая гостиная и барная стойка',
  'صالة مفتوحة وبار للفطور', 'Open woonkamer en ontbijtbar', 'Otwarty salon i bar śniadaniowy', 'Åpen stue og frokostbar', 'Öppet vardagsrum och frukostbar')
p('.media.items[11].alt',
  'Fotografía de un dormitorio amueblado con una cama doble y una puerta corredera de cristal al exterior',
  'Photographie d’une chambre meublée avec un lit double et une porte coulissante vitrée donnant sur l’extérieur',
  'Foto eines möblierten Schlafzimmers mit einem Doppelbett und einer gläsernen Schiebetür nach draußen',
  'Фотография обставленной спальни с двуспальной кроватью и стеклянной раздвижной дверью наружу',
  'صورة فوتوغرافية لغرفة نوم مفروشة بسرير مزدوج وباب زجاجي منزلق نحو الخارج',
  'Foto van een gemeubileerde slaapkamer met een tweepersoonsbed en een glazen schuifdeur naar buiten',
  'Zdjęcie umeblowanej sypialni z łóżkiem dwuosobowym i przesuwnymi szklanymi drzwiami na zewnątrz',
  'Fotografi av et møblert soverom med en dobbeltseng og en skyvedør i glass ut',
  'Fotografi av ett möblerat sovrum med en dubbelsäng och en skjutdörr i glas ut')
p('.media.items[12].alt',
  'Fotografía de un dormitorio amueblado con una cama tapizada en azul y dos mesitas de noche',
  'Photographie d’une chambre meublée avec un lit capitonné bleu et deux tables de chevet',
  'Foto eines möblierten Schlafzimmers mit einem blau gepolsterten Bett und zwei Nachttischen',
  'Фотография обставленной спальни с кроватью с синей обивкой и двумя прикроватными тумбами',
  'صورة فوتوغرافية لغرفة نوم مفروشة بسرير مكسو بالأزرق وطاولتي سرير جانبيتين',
  'Foto van een gemeubileerde slaapkamer met een blauw gestoffeerd bed en twee nachtkastjes',
  'Zdjęcie umeblowanej sypialni z łóżkiem tapicerowanym na niebiesko i dwiema szafkami nocnymi',
  'Fotografi av et møblert soverom med en blå polstret seng og to nattbord',
  'Fotografi av ett möblerat sovrum med en blåklädd säng och två sängbord')

# 34-39 overview
p('.overview.headlineHtml',
  'Fase IV, <em>una vivienda disponible</em>', 'Phase IV, <em>un logement disponible</em>', 'Phase IV, <em>eine Wohnung verfügbar</em>',
  'IV очередь, <em>одна доступная квартира</em>', 'المرحلة الرابعة، <em>مسكن واحد متاح</em>', 'Fase IV, <em>één woning beschikbaar</em>',
  'Etap IV, <em>jedno dostępne mieszkanie</em>', 'Fase IV, <em>én bolig tilgjengelig</em>', 'Etapp IV, <em>en bostad tillgänglig</em>')
p('.overview.copy[0]',
  'Alcazaba Lagoon IV es la Fase IV de Alcazaba Lagoon, en Casares, en la Costa del Sol. La ficha informativa del promotor describe 59 apartamentos de uno, dos y tres dormitorios, y los planos de la fase muestran los bloques 19, 20 y 21. Hay una vivienda anunciada como disponible: la AL4-1924, un apartamento de dos dormitorios y dos baños en la segunda planta del Bloque 19, con terrazas de 55.52 [m2] y un solárium de 109.60 [m2].',
  'Alcazaba Lagoon IV est la phase IV d’Alcazaba Lagoon, à Casares, sur la Costa del Sol. La fiche d’information du promoteur décrit 59 appartements de une, deux et trois chambres, et les plans de la phase montrent les blocs 19, 20 et 21. Un logement est actuellement annoncé comme disponible : le AL4-1924, un appartement de deux chambres et deux salles de bains au deuxième étage du bloc 19, avec des terrasses de 55.52 [m2] et un solarium de 109.60 [m2].',
  'Alcazaba Lagoon IV ist Phase IV von Alcazaba Lagoon in Casares an der Costa del Sol. Das Infoblatt des Bauträgers beschreibt 59 Apartments mit einem, zwei und drei Schlafzimmern, und die Pläne der Phase zeigen die Blöcke 19, 20 und 21. Eine Wohnung ist derzeit als verfügbar gelistet: AL4-1924, eine Wohnung mit zwei Schlafzimmern und zwei Bädern im zweiten Obergeschoss von Block 19, mit Terrassen von 55.52 [m2] und einem Solarium von 109.60 [m2].',
  'Alcazaba Lagoon IV — это IV очередь Alcazaba Lagoon в Касаресе на Коста-дель-Соль. В информационном листе застройщика описаны 59 квартир с одной, двумя и тремя спальнями, а на планах очереди показаны блоки 19, 20 и 21. Сейчас в списке доступных числится одна квартира: AL4-1924, с двумя спальнями и двумя ванными комнатами на третьем этаже блока 19, с террасами 55.52 [m2] и солярием 109.60 [m2].',
  'Alcazaba Lagoon IV هو المرحلة الرابعة من Alcazaba Lagoon في كاساريس على كوستا ديل سول. تصف نشرة معلومات المطوّر 59 شقة بغرفة نوم واحدة وغرفتين وثلاث غرف، وتُظهر مخططات المرحلة المباني 19 و20 و21. مسكن واحد مدرج حالياً على أنه متاح: AL4-1924، وهو شقة بغرفتي نوم وحمامين في الطابق الثاني من المبنى 19، مع تراسات بمساحة 55.52 [m2] وسولاريوم بمساحة 109.60 [m2].',
  'Alcazaba Lagoon IV is fase IV van Alcazaba Lagoon, in Casares aan de Costa del Sol. Het infoblad van de ontwikkelaar beschrijft 59 appartementen met een, twee en drie slaapkamers, en de plannen van de fase tonen de blokken 19, 20 en 21. Eén woning staat momenteel als beschikbaar vermeld: AL4-1924, een appartement met twee slaapkamers en twee badkamers op de tweede verdieping van blok 19, met terrassen van 55.52 [m2] en een solarium van 109.60 [m2].',
  'Alcazaba Lagoon IV to etap IV Alcazaba Lagoon w Casares na Costa del Sol. Karta informacyjna dewelopera opisuje 59 apartamentów z jedną, dwiema i trzema sypialniami, a plany etapu pokazują bloki 19, 20 i 21. Obecnie jako dostępne wymienione jest jedno mieszkanie: AL4-1924, z dwiema sypialniami i dwiema łazienkami na drugim piętrze bloku 19, z tarasami o powierzchni 55.52 [m2] i solarium o powierzchni 109.60 [m2].',
  'Alcazaba Lagoon IV er fase IV av Alcazaba Lagoon i Casares på Costa del Sol. Utbyggerens informasjonsark beskriver 59 leiligheter med ett, to og tre soverom, og planene for fasen viser hus 19, 20 og 21. Én bolig er for tiden oppført som tilgjengelig: AL4-1924, en leilighet med to soverom og to bad i andre etasje i hus 19, med terrasser på 55.52 [m2] og en solterrasse på 109.60 [m2].',
  'Alcazaba Lagoon IV är etapp IV av Alcazaba Lagoon, i Casares på Costa del Sol. Exploatörens informationsblad beskriver 59 lägenheter med ett, två och tre sovrum, och planritningarna för etappen visar husen 19, 20 och 21. En bostad är för närvarande listad som tillgänglig: AL4-1924, en lägenhet med två sovrum och två badrum på andra våningen i hus 19, med terrasser på 55.52 [m2] och en solterrass på 109.60 [m2].')
p('.overview.copy[1]',
  'La ficha informativa de 2024 enumera una piscina de diseño moderno, jardines tropicales, una zona de juegos infantil y lo que llama uso exclusivo de una laguna de aguas cristalinas, junto con grandes ventanas de doble acristalamiento, un sistema de aerotermia y una plaza de garaje y un trastero con cada vivienda. La lista de disponibilidad indica que la urbanización está terminada.',
  'La fiche d’information de 2024 énumère une piscine au design moderne, des jardins tropicaux, une aire de jeux pour enfants et ce qu’elle appelle l’usage exclusif d’un lagon aux eaux cristallines, ainsi que de grandes fenêtres à double vitrage, un système aérothermique, et une place de parking et une cave avec chaque logement. La liste de disponibilité indique que l’ensemble est achevé.',
  'Das Infoblatt von 2024 nennt einen Pool in modernem Design, tropische Gärten, einen Kinderspielplatz und das, was es die exklusive Nutzung einer kristallklaren Lagune nennt, dazu große doppelt verglaste Fenster, ein aerothermisches System sowie einen Stellplatz und einen Abstellraum bei jeder Wohnung. Die Verfügbarkeitsliste gibt die Anlage als fertiggestellt an.',
  'В информационном листе 2024 года указаны бассейн современного дизайна, тропические сады, детская площадка и то, что он называет эксклюзивным пользованием кристально чистой лагуной, а также большие окна с двойным остеклением, аэротермальная система и по одному месту в гараже и одной кладовой при каждой квартире. Список доступных объектов указывает, что комплекс построен.',
  'تذكر نشرة المعلومات لعام 2024 مسبحاً بتصميم عصري وحدائق استوائية ومنطقة ألعاب للأطفال وما تسميه الاستخدام الحصري لبحيرة لاغون صافية الماء، إلى جانب نوافذ واسعة بزجاج مزدوج ونظام حراري هوائي وموقف سيارة واحد وغرفة تخزين واحدة مع كل مسكن. وتذكر قائمة التوفر أن المجمّع مكتمل.',
  'Het infoblad van 2024 vermeldt een zwembad met modern ontwerp, tropische tuinen, een speeltuin en wat het exclusief gebruik van een kristalheldere lagune noemt, samen met grote ramen met dubbele beglazing, een aerothermisch systeem en bij elke woning één parkeerplaats en één berging. De beschikbaarheidslijst geeft het complex als opgeleverd aan.',
  'Karta informacyjna z 2024 r. wymienia basen o nowoczesnym designie, tropikalne ogrody, plac zabaw oraz to, co nazywa wyłącznym korzystaniem z krystalicznie czystej laguny, a także duże okna z podwójnymi szybami, system aerotermiczny oraz jedno miejsce postojowe i jedną komórkę lokatorską przy każdym mieszkaniu. Lista dostępności podaje, że osiedle jest ukończone.',
  'Informasjonsarket fra 2024 oppgir et basseng med moderne design, tropiske hager, en lekeplass og det det kaller eksklusiv bruk av en krystallklar lagune, sammen med store vinduer med dobbeltglass, et aerotermisk system og én parkeringsplass og én bod til hver bolig. Tilgjengelighetslisten oppgir at anlegget er ferdigstilt.',
  'Informationsbladet från 2024 anger en pool med modern design, tropiska trädgårdar, en lekplats och det som det kallar exklusiv användning av en kristallklar lagun, tillsammans med stora fönster med dubbelglas, ett aerotermiskt system samt en parkeringsplats och ett förråd till varje bostad. Tillgänglighetslistan anger att området är färdigställt.')
p('.overview.metrics[0][0]',
  'Fase', 'Phase', 'Phase', 'Очередь', 'المرحلة', 'Fase', 'Etap', 'Fase', 'Etapp')
p('.overview.metrics[0][1]',
  'IV, 59 apartamentos', 'IV, 59 appartements', 'IV, 59 Apartments', 'IV, 59 квартир', 'الرابعة، 59 شقة', 'IV, 59 appartementen', 'IV, 59 apartamentów', 'IV, 59 leiligheter', 'IV, 59 lägenheter')
p('.overview.metrics[3][1]',
  'Terrazas y un solárium de 109.60 [m2]', 'Terrasses et un solarium de 109.60 [m2]', 'Terrassen und ein Solarium von 109.60 [m2]',
  'Террасы и солярий 109.60 [m2]', 'تراسات وسولاريوم بمساحة 109.60 [m2]', 'Terrassen en een solarium van 109.60 [m2]',
  'Tarasy i solarium o powierzchni 109.60 [m2]', 'Terrasser og en solterrasse på 109.60 [m2]', 'Terrasser och en solterrass på 109.60 [m2]')

# 40-44 why
p('.why.copy',
  'Una vivienda terminada de dos dormitorios con más espacio exterior que interior, en una urbanización de bloques blancos en terrazas alrededor de una piscina y jardines tropicales.',
  'Un logement achevé de deux chambres avec plus d’espace extérieur qu’intérieur, dans un ensemble d’immeubles blancs à terrasses autour d’une piscine et de jardins tropicaux.',
  'Eine fertiggestellte Wohnung mit zwei Schlafzimmern und mehr Außen- als Innenfläche, in einer Anlage aus weißen Terrassenblöcken rund um einen Pool und tropische Gärten.',
  'Готовая квартира с двумя спальнями, где открытых пространств больше, чем жилых, в комплексе из белых террасных блоков вокруг бассейна и тропических садов.',
  'مسكن جاهز بغرفتي نوم تفوق مساحاته الخارجية مساحاته الداخلية، في مجمّع من مبانٍ بيضاء مدرّجة التراسات حول مسبح وحدائق استوائية.',
  'Een afgewerkte woning met twee slaapkamers en meer buiten- dan binnenruimte, in een complex van witte terrasgebouwen rond een zwembad en tropische tuinen.',
  'Ukończone mieszkanie z dwiema sypialniami, z większą powierzchnią zewnętrzną niż wewnętrzną, na osiedlu białych tarasowych bloków wokół basenu i tropikalnych ogrodów.',
  'En ferdigstilt bolig med to soverom og mer uteareal enn innearealer, i et anlegg med hvite terrasseblokker rundt et basseng og tropiske hager.',
  'En färdigställd bostad med två sovrum och mer ytor utomhus än inomhus, i ett område med vita terrasshus kring en pool och tropiska trädgårdar.')
p('.why.points[0][1]',
  'Compradores que quieren una vivienda terminada de dos dormitorios con un gran solárium, en una urbanización que pueden recorrer antes de comprar.',
  'Acheteurs qui veulent un logement achevé de deux chambres avec un grand solarium, dans un ensemble qu’ils peuvent parcourir avant d’acheter.',
  'Käufer, die eine fertiggestellte Wohnung mit zwei Schlafzimmern und einem großen Solarium suchen, in einer Anlage, die sie vor dem Kauf besichtigen können.',
  'Покупатели, которым нужна готовая квартира с двумя спальнями и большим солярием в комплексе, который можно обойти до покупки.',
  'المشترون الذين يريدون مسكناً جاهزاً بغرفتي نوم وسولاريوم كبير، في مجمّع يمكنهم التجول فيه قبل الشراء.',
  'Kopers die een afgewerkte woning met twee slaapkamers en een groot solarium zoeken, in een complex dat ze voor de aankoop kunnen bezoeken.',
  'Kupujący, którzy szukają ukończonego mieszkania z dwiema sypialniami i dużym solarium na osiedlu, które mogą obejść przed zakupem.',
  'Kjøpere som vil ha en ferdigstilt bolig med to soverom og en stor solterrasse, i et anlegg de kan gå gjennom før kjøpet.',
  'Köpare som vill ha en färdigställd bostad med två sovrum och en stor solterrass, i ett område som de kan gå igenom före köpet.')
p('.why.points[1][1]',
  'La vivienda tiene 55.52 [m2] de terrazas y un solárium de 109.60 [m2], mayor que sus 107.57 [m2] construidos de interior. El plano dibuja una escalera de caracol hasta el solárium.',
  'Le logement compte 55.52 [m2] de terrasses et un solarium de 109.60 [m2], plus grand que ses 107.57 [m2] construits à l’intérieur. Le plan dessine un escalier en colimaçon jusqu’au solarium.',
  'Die Wohnung hat 55.52 [m2] Terrassen und ein Solarium von 109.60 [m2], größer als die 107.57 [m2] bebaute Innenfläche. Der Plan zeichnet eine Wendeltreppe hinauf zum Solarium.',
  'У квартиры 55.52 [m2] террас и солярий 109.60 [m2], больше её 107.57 [m2] застроенной внутренней площади. На плане нарисована винтовая лестница на солярий.',
  'يضم المسكن تراسات بمساحة 55.52 [m2] وسولاريوم بمساحة 109.60 [m2]، أكبر من مساحته الداخلية المبنية البالغة 107.57 [m2]. ويرسم المخطط درجاً حلزونياً يصعد إلى السولاريوم.',
  'De woning heeft 55.52 [m2] terrassen en een solarium van 109.60 [m2], groter dan de 107.57 [m2] bebouwd binnenoppervlak. Op het plan staat een wenteltrap naar het solarium.',
  'Mieszkanie ma tarasy o powierzchni 55.52 [m2] i solarium o powierzchni 109.60 [m2], większe niż jego 107.57 [m2] zabudowy wnętrza. Na rzucie narysowano spiralne schody na solarium.',
  'Boligen har 55.52 [m2] terrasser og en solterrasse på 109.60 [m2], større enn de 107.57 [m2] bebygde innvendige arealet. Planen viser en spiraltrapp opp til solterrassen.',
  'Bostaden har 55.52 [m2] terrasser och en solterrass på 109.60 [m2], större än dess 107.57 [m2] byggyta inomhus. På ritningen finns en spiraltrappa upp till solterrassen.')
p('.why.points[2][1]',
  'La urbanización está en Casares, en la Costa del Sol, y el mapa de la ficha informativa la sitúa al oeste del puerto deportivo de Estepona.',
  'L’ensemble se trouve à Casares, sur la Costa del Sol, et la carte de la fiche d’information le place à l’ouest du port de plaisance d’Estepona.',
  'Die Anlage liegt in Casares an der Costa del Sol, und die Karte im Infoblatt verortet sie westlich des Sporthafens von Estepona.',
  'Комплекс находится в Касаресе на Коста-дель-Соль, а на карте из информационного листа он обозначен к западу от спортивной гавани Эстепоны.',
  'يقع المجمّع في كاساريس على كوستا ديل سول، وتضعه خريطة نشرة المعلومات إلى الغرب من الميناء الرياضي في إستيبونا.',
  'Het complex ligt in Casares aan de Costa del Sol, en de kaart in het infoblad plaatst het ten westen van de jachthaven van Estepona.',
  'Osiedle leży w Casares na Costa del Sol, a mapa w karcie informacyjnej umieszcza je na zachód od portu sportowego w Esteponie.',
  'Anlegget ligger i Casares på Costa del Sol, og kartet i informasjonsarket plasserer det vest for sportshavnen i Estepona.',
  'Området ligger i Casares på Costa del Sol, och kartan i informationsbladet placerar det väster om sporthamnen i Estepona.')
p('.why.points[3][1]',
  'Hay una vivienda anunciada como disponible. La lista de precios del promotor de julio de 2025 la mostraba como reservada, por lo que Nueva Living vuelve a confirmar la disponibilidad y el precio antes de cualquier visita.',
  'Un logement est actuellement annoncé comme disponible. La liste de prix du promoteur de juillet 2025 le montrait comme réservé, c’est pourquoi Nueva Living reconfirme la disponibilité et le prix avant toute visite.',
  'Eine Wohnung ist derzeit als verfügbar gelistet. Die Preisliste des Bauträgers vom Juli 2025 wies sie als reserviert aus, daher bestätigt Nueva Living Verfügbarkeit und Preis vor jeder Besichtigung erneut.',
  'Сейчас в списке доступных числится одна квартира. В прайс-листе застройщика за июль 2025 года она значилась как зарезервированная, поэтому Nueva Living повторно подтверждает наличие и цену до любого просмотра.',
  'مسكن واحد مدرج حالياً على أنه متاح. وكانت قائمة أسعار المطوّر الصادرة في يوليو 2025 تُظهره محجوزاً، لذا تعيد Nueva Living تأكيد التوفر والسعر قبل أي معاينة.',
  'Eén woning staat momenteel als beschikbaar vermeld. De prijslijst van de ontwikkelaar van juli 2025 toonde haar als gereserveerd, daarom bevestigt Nueva Living de beschikbaarheid en de prijs opnieuw vóór elke bezichtiging.',
  'Obecnie jako dostępne wymienione jest jedno mieszkanie. Cennik dewelopera z lipca 2025 r. pokazywał je jako zarezerwowane, dlatego Nueva Living ponownie potwierdza dostępność i cenę przed każdą wizytą.',
  'Én bolig er for tiden oppført som tilgjengelig. Utbyggerens prisliste fra juli 2025 viste den som reservert, så Nueva Living bekrefter tilgjengelighet og pris på nytt før enhver visning.',
  'En bostad är för närvarande listad som tillgänglig. Exploatörens prislista från juli 2025 visade den som reserverad, så Nueva Living bekräftar tillgänglighet och pris på nytt före varje visning.')

# 45-52 architecture
p('.architecture.headlineHtml',
  'Bloques blancos, <em>terrazas y pérgolas</em>', 'Immeubles blancs, <em>terrasses et pergolas</em>', 'Weiße Blöcke, <em>Terrassen und Pergolen</em>',
  'Белые блоки, <em>террасы и пергол</em>', 'مبانٍ بيضاء، <em>تراسات وبيرغولات</em>', 'Witte gebouwen, <em>terrassen en pergola’s</em>',
  'Białe bloki, <em>tarasy i pergole</em>', 'Hvite blokker, <em>terrasser og pergolaer</em>', 'Vita hus, <em>terrasser och pergolor</em>')
p('.architecture.copy[0]',
  'En las fotografías, los bloques son blancos y escalonados, con terrazas, barandillas de cristal, pérgolas en las plantas altas y escaleras de caracol hasta las cubiertas, sobre muros de jardín de piedra.',
  'Sur les photographies, les immeubles sont blancs et en retrait progressif, avec des terrasses, des garde-corps en verre, des pergolas aux étages supérieurs et des escaliers en colimaçon jusqu’aux toits, au-dessus de murs de jardin en pierre.',
  'Auf den Fotos sind die Blöcke weiß und gestaffelt, mit Terrassen, Glasbrüstungen, Pergolen in den oberen Geschossen und Wendeltreppen zu den Dächern, über Gartenmauern aus Naturstein.',
  'На фотографиях блоки белые, с уступами, с террасами, стеклянными ограждениями, перголами на верхних уровнях и винтовыми лестницами на крыши, над каменными садовыми стенками.',
  'في الصور تبدو المباني بيضاء متدرجة، بتراسات وحواجز زجاجية وبيرغولات في الطوابق العليا ودرج حلزوني يصعد إلى الأسطح، فوق جدران حدائق حجرية.',
  'Op de foto’s zijn de gebouwen wit en terugspringend, met terrassen, glazen balustrades, pergola’s op de bovenste niveaus en wenteltrappen naar de daken, boven tuinmuren van natuursteen.',
  'Na zdjęciach bloki są białe i schodkowe, z tarasami, szklanymi balustradami, pergolami na wyższych poziomach i spiralnymi schodami na dachy, nad kamiennymi murami ogrodowymi.',
  'På fotografiene er blokkene hvite og trappet tilbake, med terrasser, glassrekkverk, pergolaer i de øvre etasjene og spiraltrapper opp til takene, over hagemurer av stein.',
  'På fotografierna är husen vita och trappade, med terrasser, glasräcken, pergolor på de övre nivåerna och spiraltrappor upp till taken, ovanför trädgårdsmurar av sten.')
p('.architecture.copy[1]',
  'Los planos de la fase muestran los bloques 19, 20 y 21, cada uno con sótano y plantas baja, primera y segunda. La vivienda AL4-1924 está en la segunda planta, con su propio nivel de solárium encima.',
  'Les plans de la phase montrent les blocs 19, 20 et 21, chacun avec un sous-sol et un rez-de-chaussée, un premier et un deuxième étage. Le logement AL4-1924 se trouve au deuxième étage, avec son propre niveau de solarium au-dessus.',
  'Die Pläne der Phase zeigen die Blöcke 19, 20 und 21, jeweils mit Untergeschoss sowie Erd-, erstem und zweitem Obergeschoss. Die Wohnung AL4-1924 liegt im zweiten Obergeschoss, mit einer eigenen Solariumebene darüber.',
  'На планах очереди показаны блоки 19, 20 и 21, в каждом — подвал, первый, второй и третий этажи. Квартира AL4-1924 находится на третьем этаже, выше у неё собственный уровень солярия.',
  'تُظهر مخططات المرحلة المباني 19 و20 و21، وفي كل منها طابق سفلي وطوابق أرضي وأول وثانٍ. والمسكن AL4-1924 في الطابق الثاني، وفوقه مستوى السولاريوم الخاص به.',
  'De plannen van de fase tonen de blokken 19, 20 en 21, elk met een kelder en een begane grond, een eerste en een tweede verdieping. Woning AL4-1924 ligt op de tweede verdieping, met een eigen solariumniveau erboven.',
  'Plany etapu pokazują bloki 19, 20 i 21, każdy z piwnicą oraz parterem, pierwszym i drugim piętrem. Mieszkanie AL4-1924 znajduje się na drugim piętrze, a nad nim ma własny poziom solarium.',
  'Planene for fasen viser hus 19, 20 og 21, hvert med kjeller samt første, andre og tredje etasje. Bolig AL4-1924 ligger i andre etasje, med sitt eget solterrassenivå over.',
  'Planritningarna för etappen visar husen 19, 20 och 21, vart och ett med källare samt bottenvåning, första och andra våningen. Bostad AL4-1924 ligger på andra våningen, med en egen solterrassnivå ovanpå.')
p('.architecture.highlights[0][1]',
  'Cimentación de zapatas o losa, muros de sótano y forjados bidireccionales de hormigón armado, con muros exteriores de ladrillo macizo enfoscados por fuera y trasdosados con aislamiento proyectado.',
  'Fondations sur semelles ou radier, murs de sous-sol et planchers à double sens en béton armé, avec des murs extérieurs en brique pleine enduits à l’extérieur et doublés d’une isolation projetée.',
  'Fundament aus Einzelfundamenten oder Bodenplatte, Kellerwände und zweiachsig gespannte Decken aus Stahlbeton, mit Außenwänden aus Vollziegeln, außen verputzt und innen mit Spritzdämmung verkleidet.',
  'Фундамент на лентах или плита, стены подвала и перекрытия с армированием в двух направлениях из железобетона, наружные стены из полнотелого кирпича, оштукатуренные снаружи и утеплённые изнутри напылением.',
  'أساسات منفصلة أو لوح أساس، وجدران قبو وأسقف باتجاهين من الخرسانة المسلحة، مع جدران خارجية من الطوب المصمت مكسوة بالملاط من الخارج ومبطّنة بعزل مرشوش من الداخل.',
  'Fundering op poeren of een plaat, kelderwanden en tweezijdig gewapende vloeren van gewapend beton, met buitenmuren van massieve baksteen die buiten gepleisterd zijn en binnen bekleed met gespoten isolatie.',
  'Fundamenty stopowe lub płyta, ściany piwnic i stropy zbrojone dwukierunkowo z betonu zbrojonego, ze ścianami zewnętrznymi z cegły pełnej, tynkowanymi z zewnątrz i obłożonymi od wewnątrz natryskową izolacją.',
  'Fundament på punktfundamenter eller plate, kjellervegger og toveis dekker i armert betong, med yttervegger av massiv murstein som er pusset utvendig og kledd innvendig med sprøytet isolasjon.',
  'Grund på plintar eller platta, källarväggar och tvåvägsarmerade bjälklag av armerad betong, med ytterväggar av massivt tegel som är putsade utvändigt och invändigt klädda med sprutisolering.')
p('.architecture.highlights[1][1]',
  'Ventanas correderas o abatibles con doble acristalamiento y cámara de aire, y barandillas de cristal en las terrazas.',
  'Fenêtres coulissantes ou battantes à double vitrage avec lame d’air, et garde-corps en verre sur les terrasses.',
  'Schiebe- oder Drehkippfenster mit Doppelverglasung und Luftschicht sowie Glasbrüstungen auf den Terrassen.',
  'Раздвижные или распашные окна с двойным остеклением и воздушной прослойкой и стеклянные ограждения на террасах.',
  'نوافذ منزلقة أو مفصلية بزجاج مزدوج وطبقة هواء، وحواجز زجاجية على التراسات.',
  'Schuif- of draairamen met dubbele beglazing en een luchtspouw, en glazen balustrades op de terrassen.',
  'Okna przesuwne lub uchylne z podwójnymi szybami i komorą powietrzną oraz szklane balustrady na tarasach.',
  'Skyve- eller sidehengslede vinduer med dobbeltglass og luftspalte, og glassrekkverk på terrassene.',
  'Skjut- eller sidohängda fönster med dubbelglas och luftspalt samt glasräcken på terrasserna.')
p('.architecture.highlights[2][0]',
  'Aislamiento acústico', 'Isolation acoustique', 'Schallschutz', 'Звукоизоляция', 'العزل الصوتي', 'Geluidsisolatie', 'Izolacja akustyczna', 'Lydisolasjon', 'Ljudisolering')
p('.architecture.highlights[2][1]',
  'Entre viviendas, una doble hoja de ladrillo perforado acústico con lana mineral.',
  'Entre les logements, une double paroi de brique perforée acoustique avec de la laine minérale.',
  'Zwischen den Wohnungen eine doppelte Schale aus akustischen Lochziegeln mit Mineralwolle.',
  'Между квартирами — двойная стена из акустического дырчатого кирпича с минеральной ватой.',
  'بين المساكن جدار مزدوج من الطوب المثقّب العازل للصوت مع صوف معدني.',
  'Tussen de woningen een dubbele wand van akoestische geperforeerde baksteen met mineraalwol.',
  'Między mieszkaniami podwójna ściana z akustycznej cegły dziurawki z wełną mineralną.',
  'Mellom boligene en dobbel vegg av akustisk hulmurstein med mineralull.',
  'Mellan bostäderna en dubbel vägg av akustiskt håltegel med mineralull.')
p('.architecture.highlights[3][1]',
  'Cubiertas transitables y terrazas de cubierta con solería porcelánica, sobre una base con pendiente y una capa de mortero de protección.',
  'Toitures accessibles et toits-terrasses avec revêtement en grès cérame, sur un support en pente et une couche de mortier de protection.',
  'Begehbare Dächer und Dachterrassen mit Feinsteinzeugbelag, auf einem Gefällunterbau mit einer schützenden Mörtelschicht.',
  'Эксплуатируемые кровли и крышные террасы с покрытием из керамогранита, на основании с уклоном и защитным слоем раствора.',
  'أسطح قابلة للسير عليها وتراسات سطحية مكسوة بالبورسلين، فوق قاعدة مائلة وطبقة ملاط واقية.',
  'Begaanbare daken en dakterrassen met een porseleinen vloer, op een hellende onderlaag met een beschermende mortellaag.',
  'Dachy użytkowe i tarasy dachowe z posadzką porcelanową, na podkładzie ze spadkiem i z ochronną warstwą zaprawy.',
  'Gangbare tak og takterrasser med porselensbelegg, over en skrå underlagsflate og et beskyttende mørtellag.',
  'Gångbara tak och takterrasser med porslinsbeläggning, på ett lutande underlag med ett skyddande murbrukslager.')

# 53-69 qualitySpecs
p('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor para la Fase IV. Está en fase de desarrollo, y el promotor puede modificarla por razones técnicas sin reducir la calidad ni el diseño del resultado. En el original, la mayoría de las partidas llevan «o similar».',
  'Source : le descriptif du promoteur pour la phase IV. Il est en cours d’élaboration, et le promoteur peut le modifier pour des raisons techniques sans réduire la qualité ni le design du résultat. Dans l’original, la plupart des postes sont suivis de « ou similaire ».',
  'Quelle: die Baubeschreibung des Bauträgers für Phase IV. Sie befindet sich im Entwicklungsstadium, und der Bauträger kann sie aus technischen Gründen ändern, ohne Qualität oder Design des Ergebnisses zu mindern. Im Original steht bei den meisten Positionen „oder ähnlich“.',
  'Источник: спецификация застройщика для IV очереди. Она находится на стадии разработки, и застройщик может изменить её по техническим причинам, не снижая качества и дизайна результата. В оригинале большинство позиций снабжено оговоркой «или аналогичное».',
  'المصدر: مواصفات المطوّر للمرحلة الرابعة. وهي في مرحلة التطوير، ويجوز للمطوّر تعديلها لأسباب فنية دون خفض جودة النتيجة أو تصميمها. وفي النص الأصلي ترد عبارة «أو ما يماثله» في معظم البنود.',
  'Bron: de specificatie van de ontwikkelaar voor fase IV. Ze bevindt zich in het ontwikkelstadium, en de ontwikkelaar kan haar om technische redenen wijzigen zonder de kwaliteit of het ontwerp van het resultaat te verminderen. In het origineel staat bij de meeste posten „of gelijkwaardig”.',
  'Źródło: specyfikacja dewelopera dla etapu IV. Jest na etapie opracowania, a deweloper może ją zmienić z przyczyn technicznych bez obniżania jakości i projektu efektu końcowego. W oryginale większość pozycji ma dopisek „lub podobne”.',
  'Kilde: utbyggerens spesifikasjon for fase IV. Den er i utviklingsfasen, og utbyggeren kan endre den av tekniske grunner uten å redusere kvaliteten eller designet på resultatet. I originalen står «eller tilsvarende» ved de fleste postene.',
  'Källa: exploatörens specifikation för etapp IV. Den är i utvecklingsskedet, och exploatören kan ändra den av tekniska skäl utan att sänka kvaliteten eller designen på resultatet. I originalet står ”eller liknande” vid de flesta posterna.')
p('.qualitySpecs.groups[0].name',
  'Estructura y muros', 'Structure et murs', 'Tragwerk und Wände', 'Конструкция и стены', 'الهيكل والجدران', 'Constructie en muren', 'Konstrukcja i ściany', 'Konstruksjon og vegger', 'Stomme och väggar')
p('.qualitySpecs.groups[0].items[0]',
  'Zapatas o losa, muros de sótano y forjados bidireccionales de hormigón armado, con lámina anti-impacto.',
  'Semelles ou radier, murs de sous-sol et planchers à double sens en béton armé, avec une couche anti-impact.',
  'Einzelfundamente oder Bodenplatte, Kellerwände und zweiachsig gespannte Decken aus Stahlbeton, mit einer Trittschalldämmschicht.',
  'Ленты или плита, стены подвала и перекрытия из железобетона с армированием в двух направлениях, с ударопоглощающим слоем.',
  'أساسات منفصلة أو لوح أساس وجدران قبو وأسقف باتجاهين من الخرسانة المسلحة، مع طبقة مضادة للصدمات.',
  'Poeren of een plaat, kelderwanden en tweezijdig gewapende vloeren van gewapend beton, met een anti-impactlaag.',
  'Fundamenty stopowe lub płyta, ściany piwnic i stropy zbrojone dwukierunkowo z betonu zbrojonego, z warstwą przeciwuderzeniową.',
  'Punktfundamenter eller plate, kjellervegger og toveis dekker i armert betong, med et støtdempende lag.',
  'Plintar eller platta, källarväggar och tvåvägsarmerade bjälklag av armerad betong, med ett stötdämpande lager.')
p('.qualitySpecs.groups[0].items[1]',
  'Muros exteriores de ladrillo macizo, enfoscados por fuera con mortero de cemento y trasdosados por dentro con aislamiento térmico y acústico de poliuretano proyectado, una cámara de aire y un tabicón de ladrillo hueco.',
  'Murs extérieurs en brique pleine, enduits à l’extérieur au mortier de ciment et doublés à l’intérieur d’une isolation thermique et acoustique en polyuréthane projeté, d’une lame d’air et d’une cloison en brique creuse.',
  'Außenwände aus Vollziegeln, außen mit Zementmörtel verputzt und innen mit einer Wärme- und Schalldämmung aus Polyurethan-Spritzschaum, einer Luftschicht und einer Hohlziegelwand verkleidet.',
  'Наружные стены из полнотелого кирпича, оштукатуренные снаружи цементным раствором и облицованные изнутри теплозвукоизоляцией из напылённого полиуретана, воздушной прослойкой и перегородкой из пустотелого кирпича.',
  'جدران خارجية من الطوب المصمت مكسوة من الخارج بملاط الإسمنت ومبطّنة من الداخل بعزل حراري وصوتي من البولي يوريثان المرشوش وطبقة هواء وجدار من الطوب المفرّغ.',
  'Buitenmuren van massieve baksteen, buiten gepleisterd met cementmortel en binnen bekleed met thermische en akoestische isolatie van gespoten polyurethaan, een luchtspouw en een wand van holle baksteen.',
  'Ściany zewnętrzne z cegły pełnej, tynkowane z zewnątrz zaprawą cementową, a od wewnątrz obłożone izolacją termiczną i akustyczną z natryskowego poliuretanu, komorą powietrzną i ścianką z cegły dziurawki.',
  'Yttervegger av massiv murstein, pusset utvendig med sementmørtel og kledd innvendig med varme- og lydisolasjon av sprøytet polyuretan, en luftspalte og en vegg av hulmurstein.',
  'Ytterväggar av massivt tegel, putsade utvändigt med cementbruk och invändigt klädda med värme- och ljudisolering av sprutad polyuretan, en luftspalt och en vägg av hålblock.')
p('.qualitySpecs.groups[1].name',
  'Sonido y tabiquería', 'Isolation phonique et cloisons', 'Schallschutz und Trennwände', 'Звукоизоляция и перегородки', 'العزل الصوتي والقواطع', 'Geluid en scheidingswanden', 'Dźwięk i ścianki działowe', 'Lyd og skillevegger', 'Ljud och mellanväggar')
p('.qualitySpecs.groups[1].items[0]',
  'Entre viviendas, una doble hoja de ladrillo perforado acústico con lana mineral, y dentro de cada vivienda un tabicón doble de ladrillo hueco.',
  'Entre les logements, une double paroi de brique perforée acoustique avec de la laine minérale, et à l’intérieur de chaque logement une épaisse cloison double en brique creuse.',
  'Zwischen den Wohnungen eine doppelte Schale aus akustischen Lochziegeln mit Mineralwolle, innerhalb jeder Wohnung eine dicke doppelte Hohlziegelwand.',
  'Между квартирами — двойная стена из акустического дырчатого кирпича с минеральной ватой, а внутри каждой квартиры — толстая двойная перегородка из пустотелого кирпича.',
  'بين المساكن جدار مزدوج من الطوب المثقّب العازل للصوت مع صوف معدني، وداخل كل مسكن قاطع سميك مزدوج من الطوب المفرّغ.',
  'Tussen de woningen een dubbele wand van akoestische geperforeerde baksteen met mineraalwol, en binnen elke woning een dikke dubbele wand van holle baksteen.',
  'Między mieszkaniami podwójna ściana z akustycznej cegły dziurawki z wełną mineralną, a wewnątrz każdego mieszkania gruba podwójna ścianka z cegły dziurawki.',
  'Mellom boligene en dobbel vegg av akustisk hulmurstein med mineralull, og inne i hver bolig en tykk dobbel skillevegg av hulmurstein.',
  'Mellan bostäderna en dubbel vägg av akustiskt håltegel med mineralull, och inne i varje bostad en tjock dubbel mellanvägg av hålblock.')
p('.qualitySpecs.groups[1].items[1]',
  'Revestimiento de yeso en paredes y techos, con falsos techos de escayola en zonas húmedas y por donde pasan las instalaciones, y falsos techos registrables donde están las máquinas de aire acondicionado.',
  'Enduit de plâtre sur les murs et les plafonds, avec des faux plafonds en plâtre dans les pièces humides et là où passent les installations, et des faux plafonds démontables là où se trouvent les unités de climatisation.',
  'Gipsputz an Wänden und Decken, mit Gipsabhangdecken in Feuchträumen und dort, wo Leitungen verlaufen, sowie abnehmbaren Abhangdecken dort, wo die Klimageräte sitzen.',
  'Гипсовая штукатурка стен и потолков, подвесные гипсовые потолки во влажных зонах и там, где проходят коммуникации, и съёмные подвесные потолки там, где расположены кондиционеры.',
  'كسوة من الجبس على الجدران والأسقف، مع أسقف مستعارة من الجص في المناطق الرطبة وأماكن مرور التمديدات، وأسقف مستعارة قابلة للفتح حيث توجد أجهزة التكييف.',
  'Gipspleister op wanden en plafonds, met gipsen verlaagde plafonds in natte ruimtes en waar leidingen lopen, en afneembare verlaagde plafonds waar de airconditioningunits zitten.',
  'Tynk gipsowy na ścianach i sufitach, z podwieszanymi sufitami gipsowymi w strefach mokrych i tam, gdzie biegną instalacje, oraz z demontowalnymi sufitami podwieszanymi w miejscach klimatyzatorów.',
  'Gipspuss på vegger og tak, med nedsenkede himlinger av gips i våtrom og der installasjonene går, og nedtakbare himlinger der klimaanleggene sitter.',
  'Gipsputs på väggar och tak, med undertak av gips i våtrum och där installationerna går, och avtagbara undertak där luftkonditioneringsenheterna sitter.')
p('.qualitySpecs.groups[2].items[0]',
  'Suelos interiores de gres porcelánico en lama de 20 x 120 cm con aspecto de madera, y suelos exteriores antideslizantes de gres porcelánico de 60 x 60 cm.',
  'Sols intérieurs en grès cérame en lames de 20 x 120 cm d’aspect bois, et sols extérieurs antidérapants en grès cérame de 60 x 60 cm.',
  'Innen Feinsteinzeugböden als Dielen in Holzoptik, 20 x 120 cm, und außen rutschhemmendes Feinsteinzeug, 60 x 60 cm.',
  'Полы внутри из керамогранита в виде досок 20 x 120 см с эффектом дерева, снаружи — противоскользящий керамогранит 60 x 60 см.',
  'أرضيات داخلية من البورسلين على هيئة ألواح بمظهر الخشب بقياس 20 × 120 سم، وأرضيات خارجية من البورسلين المانع للانزلاق بقياس 60 × 60 سم.',
  'Binnen vloeren van porseleinen steengoed als planken van 20 x 120 cm in houtlook, en buiten antislip porseleinen steengoed van 60 x 60 cm.',
  'Wewnątrz podłogi z gresu porcelanowego w formie desek o wymiarach 20 x 120 cm z efektem drewna, na zewnątrz antypoślizgowy gres porcelanowy 60 x 60 cm.',
  'Innvendig gulv av porselensflis som planker på 20 x 120 cm i trelook, og utvendig sklisikker porselensflis på 60 x 60 cm.',
  'Invändigt golv av klinker som plankor på 20 x 120 cm i träutseende, och utvändigt halkfri klinker på 60 x 60 cm.')
p('.qualitySpecs.groups[2].items[1]',
  'Baños y aseos alicatados con gres porcelánico, con pintura plástica lisa.',
  'Salles de bains et toilettes carrelées en grès cérame, avec une peinture plastique lisse.',
  'Bäder und Gäste-WCs mit Feinsteinzeug gefliest, dazu glatte Dispersionsfarbe.',
  'Ванные комнаты и санузлы облицованы керамогранитом, остальные поверхности окрашены гладкой краской.',
  'الحمامات ودورات المياه مكسوة بالبورسلين، مع طلاء بلاستيكي أملس.',
  'Badkamers en toiletten betegeld met porseleinen steengoed, met gladde muurverf.',
  'Łazienki i toalety wyłożone gresem porcelanowym, z gładką farbą plastyczną.',
  'Bad og toaletter flislagt med porselensflis, med glatt plastmaling.',
  'Badrum och toaletter kaklade med klinker, med slät plastfärg.')
p('.qualitySpecs.groups[3].items[0]',
  'Inodoros de suelo con asiento de cierre amortiguado y cisterna empotrada, mueble de lavabo con cajón, mampara de baño y espejo.',
  'Toilettes sur pied avec abattant à fermeture amortie et réservoir encastré, meuble-vasque avec tiroir, pare-baignoire et miroir.',
  'Stand-WCs mit Absenkautomatik und Unterputzspülkasten, Waschtischunterschrank mit Schublade, Badewannenabtrennung und Spiegel.',
  'Напольные унитазы с сиденьем плавного закрытия и скрытым бачком, тумба под раковину с ящиком, ванная перегородка и зеркало.',
  'مراحيض أرضية بمقعد إغلاق هادئ وخزان مخفي، ووحدة مغسلة بدرج، وحاجز للحمام ومرآة.',
  'Staande toiletten met soft-close zitting en inbouwreservoir, een wastafelmeubel met lade, een badscherm en een spiegel.',
  'Toalety stojące z deską wolnoopadającą i spłuczką podtynkową, szafka umywalkowa z szufladą, parawan nawannowy i lustro.',
  'Gulvstående toaletter med mykt lukkende sete og innebygd cisterne, servantskap med skuff, badekarvegg og speil.',
  'Golvstående toaletter med mjukstängande sits och inbyggd spolcistern, tvättskåp med låda, badkarsskärm och spegel.')
p('.qualitySpecs.groups[3].items[1]',
  'El baño principal tiene un monomando de dos salidas, un rociador mural y una teleducha; el baño secundario tiene una ducha fija, una teleducha, un termostato, un flexo y una barra deslizante.',
  'La salle de bains principale a un mitigeur à deux sorties, une pomme de douche de pluie murale et une douchette ; la salle de bains secondaire a une douche fixe, une douchette, un thermostat, un flexible et une barre coulissante.',
  'Das Hauptbad hat eine Einhebelmischbatterie mit zwei Abgängen, einen Wandregenbrausekopf und eine Handbrause; das zweite Bad hat eine Kopfbrause, eine Handbrause, einen Thermostat, einen Schlauch und eine Gleitstange.',
  'В главной ванной — однорычажный смеситель с двумя выходами, настенная тропическая лейка и ручной душ; во второй ванной — верхний душ, ручной душ, термостат, шланг и скользящий держатель.',
  'في الحمام الرئيسي خلاط بمقبض واحد بمخرجين ورشاش مطري جداري ودش يدوي؛ وفي الحمام الثانوي دش علوي ودش يدوي وثرموستات وخرطوم وشريط منزلق.',
  'De hoofdbadkamer heeft een eengreepsmengkraan met twee uitgangen, een wandregendouche en een handdouche; de tweede badkamer heeft een hoofddouche, een handdouche, een thermostaat, een slang en een glijstang.',
  'Łazienka główna ma baterię jednouchwytową z dwoma wyjściami, ścienną deszczownicę i słuchawkę prysznicową; druga łazienka ma deszczownicę, słuchawkę, termostat, wąż i drążek przesuwny.',
  'Hovedbadet har en énhåndsblander med to uttak, et veggmontert regnhode og en håndtusj; det andre badet har et takhode, en håndtusj, en termostat, en slange og en glidestang.',
  'Huvudbadrummet har en enhandsblandare med två utlopp, ett väggmonterat regnduschhuvud och en handdusch; det andra badrummet har ett takduschhuvud, en handdusch, en termostat, en slang och en glidstång.')
p('.qualitySpecs.groups[4].name',
  'Puertas y ventanas', 'Portes et fenêtres', 'Türen und Fenster', 'Двери и окна', 'الأبواب والنوافذ', 'Deuren en ramen', 'Drzwi i okna', 'Dører og vinduer', 'Dörrar och fönster')
p('.qualitySpecs.groups[4].items[0]',
  'Puerta de entrada blindada con chapa de acero, cerradura de seguridad y mirilla, y puertas de paso lacadas en blanco mate, abatibles o correderas según el proyecto.',
  'Porte d’entrée blindée en tôle d’acier avec serrure de sécurité et judas, et portes intérieures laquées blanc mat, battantes ou coulissantes selon le projet.',
  'Gepanzerte Wohnungstür mit Stahlblech, Sicherheitsschloss und Spion sowie matt weiß lackierte Innentüren, je nach Planung als Dreh- oder Schiebetüren.',
  'Бронированная входная дверь со стальным листом, замком безопасности и глазком, межкомнатные двери, окрашенные в матовый белый цвет, распашные или раздвижные в зависимости от проекта.',
  'باب دخول مصفّح بصفيحة فولاذية وقفل أمان وعين سحرية، وأبواب داخلية مطلية بالأبيض غير اللامع، مفصلية أو منزلقة بحسب المشروع.',
  'Een gepantserde voordeur met stalen plaat, een veiligheidsslot en een spion, en matwit gelakte binnendeuren, draaiend of schuivend afhankelijk van het plan.',
  'Drzwi wejściowe antywłamaniowe z blachą stalową, zamkiem bezpieczeństwa i wizjerem oraz drzwi wewnętrzne lakierowane na biały mat, otwierane lub przesuwne, zależnie od projektu.',
  'Pansret inngangsdør med stålplate, sikkerhetslås og dørspion, og innerdører lakkert i matt hvitt, hengslede eller skyvedører avhengig av prosjektet.',
  'Pansrad ytterdörr med ståldörrblad, säkerhetslås och dörrkikare, och innerdörrar lackade i matt vitt, vanliga eller skjutdörrar beroende på projektet.')
p('.qualitySpecs.groups[5].items[0]',
  'Cocinas amuebladas y totalmente equipadas con lavadora, lavavajillas, frigorífico, placa, horno eléctrico, fregadero y campana extractora.',
  'Cuisines meublées et entièrement équipées avec lave-linge, lave-vaisselle, réfrigérateur, plaque de cuisson, four électrique, évier et hotte aspirante.',
  'Möblierte und voll ausgestattete Küchen mit Waschmaschine, Geschirrspüler, Kühlschrank, Kochfeld, Elektrobackofen, Spüle und Dunstabzugshaube.',
  'Меблированные и полностью оснащённые кухни со стиральной машиной, посудомоечной машиной, холодильником, варочной панелью, электрической духовкой, мойкой и вытяжкой.',
  'مطابخ مجهزة بالأثاث ومزودة بالكامل بغسالة وغسالة صحون وثلاجة وموقد وفرن كهربائي ومغسلة وشفاط.',
  'Ingerichte en volledig uitgeruste keukens met een wasmachine, een vaatwasser, een koelkast, een kookplaat, een elektrische oven, een spoelbak en een afzuigkap.',
  'Umeblowane i w pełni wyposażone kuchnie z pralką, zmywarką, lodówką, płytą grzewczą, piekarnikiem elektrycznym, zlewem i okapem.',
  'Møblerte og fullt utstyrte kjøkken med vaskemaskin, oppvaskmaskin, kjøleskap, platetopp, elektrisk ovn, vask og kjøkkenvifte.',
  'Möblerade och fullt utrustade kök med tvättmaskin, diskmaskin, kylskåp, häll, elugn, diskho och köksfläkt.')
p('.qualitySpecs.groups[6].items[0]',
  'Agua caliente con un sistema Altherma de alta eficiencia, y aire acondicionado por bomba de calor mediante conductos en todas las estancias.',
  'Eau chaude par un système Altherma à haute efficacité, et climatisation par pompe à chaleur avec gaines dans toutes les pièces.',
  'Warmwasser über ein hocheffizientes Altherma-System und Klimaanlage per Wärmepumpe über Kanäle in allen Räumen.',
  'Горячая вода от высокоэффективной системы Altherma и кондиционирование тепловым насосом с воздуховодами во всех помещениях.',
  'مياه ساخنة من نظام Altherma عالي الكفاءة، وتكييف بمضخة حرارية عبر مجاري الهواء في جميع الغرف.',
  'Warm water via een zeer efficiënt Altherma-systeem en airconditioning met warmtepomp via kanalen in alle kamers.',
  'Ciepła woda z wysokosprawnego systemu Altherma oraz klimatyzacja z pompą ciepła w kanałach we wszystkich pomieszczeniach.',
  'Varmtvann fra et høyeffektivt Altherma-system og klimaanlegg med varmepumpe gjennom kanaler i alle rom.',
  'Varmvatten från ett högeffektivt Altherma-system och luftkonditionering med värmepump genom kanaler i alla rum.')
p('.qualitySpecs.groups[6].items[1]',
  'Ventilación mecánica en cocinas, baños y aseos, tomas de televisión, teléfono e internet, portero electrónico y preinstalación de un sistema básico de domótica.',
  'Ventilation mécanique dans les cuisines, salles de bains et toilettes, prises de télévision, de téléphone et d’internet, interphone électronique et pré-équipement pour un système domotique de base.',
  'Mechanische Lüftung in Küchen, Bädern und Gäste-WCs, TV-, Telefon- und Internetanschlüsse, eine elektronische Türsprechanlage und eine Vorinstallation für ein einfaches Hausautomationssystem.',
  'Механическая вентиляция на кухнях и в санузлах, розетки для телевидения, телефона и интернета, электронный домофон и подготовка под базовую систему «умный дом».',
  'تهوية ميكانيكية في المطابخ والحمامات ودورات المياه، ومآخذ للتلفاز والهاتف والإنترنت، ونظام اتصال داخلي إلكتروني، وتجهيز مسبق لنظام أتمتة منزلية أساسي.',
  'Mechanische ventilatie in keukens, badkamers en toiletten, aansluitingen voor tv, telefoon en internet, een elektronische deurintercom en een voorbereiding voor een eenvoudig domoticasysteem.',
  'Wentylacja mechaniczna w kuchniach, łazienkach i toaletach, gniazda telewizyjne, telefoniczne i internetowe, elektroniczny domofon oraz przygotowanie pod podstawowy system automatyki domowej.',
  'Mekanisk ventilasjon i kjøkken, bad og toaletter, uttak for TV, telefon og internett, elektronisk dørtelefon og forberedelse for et enkelt hjemmeautomasjonssystem.',
  'Mekanisk ventilation i kök, badrum och toaletter, uttag för tv, telefon och internet, elektronisk porttelefon och förberedelse för ett enkelt hemautomationssystem.')
p('.qualitySpecs.groups[7].items[0]',
  'Piscinas y jardines plantados con especies subtropicales y autóctonas, con sistema de riego e iluminación de todo el conjunto, iluminación exterior y una puerta metálica de garaje con célula fotoeléctrica y receptor de mandos.',
  'Piscines et jardins plantés d’espèces subtropicales et locales, avec un système d’arrosage et d’éclairage pour tout l’ensemble, éclairage extérieur et une porte de garage métallique avec cellule photoélectrique et récepteur de télécommande.',
  'Pools und Gärten mit subtropischen und heimischen Pflanzen, mit Bewässerung und Beleuchtung für die gesamte Anlage, Außenbeleuchtung und ein Garagentor aus Metall mit Lichtschranke und Funkempfänger.',
  'Бассейны и сады с субтропическими и местными растениями, система полива и освещения для всего комплекса, наружное освещение и металлические гаражные ворота с фотоэлементом и приёмником пультов.',
  'مسابح وحدائق مزروعة بأنواع شبه استوائية ومحلية، مع نظام ري وإنارة للمجمّع كله، وإنارة خارجية وباب مرآب معدني بخلية كهروضوئية ومستقبل للتحكم عن بُعد.',
  'Zwembaden en tuinen beplant met subtropische en inheemse soorten, met irrigatie en verlichting voor het hele complex, buitenverlichting en een metalen garagedeur met fotocel en afstandsbedieningsontvanger.',
  'Baseny i ogrody obsadzone roślinami subtropikalnymi i rodzimymi, z systemem nawadniania i oświetlenia dla całego osiedla, oświetlenie zewnętrzne oraz metalowa brama garażowa z fotokomórką i odbiornikiem pilotów.',
  'Basseng og hager beplantet med subtropiske og stedegne arter, med vanning og belysning for hele anlegget, utebelysning og en garasjeport av metall med fotocelle og mottaker for fjernkontroll.',
  'Pooler och trädgårdar planterade med subtropiska och inhemska arter, med bevattning och belysning för hela området, utomhusbelysning och en metallgarageport med fotocell och mottagare för fjärrkontroll.')

# 70-74 residences
p('.residences.headlineHtml',
  'Una vivienda, <em>con un gran solárium</em>', 'Un logement, <em>avec un grand solarium</em>', 'Eine Wohnung, <em>mit großem Solarium</em>',
  'Одна квартира, <em>с большим солярием</em>', 'مسكن واحد، <em>بسولاريوم كبير</em>', 'Eén woning, <em>met een groot solarium</em>',
  'Jedno mieszkanie, <em>z dużym solarium</em>', 'Én bolig, <em>med stor solterrasse</em>', 'En bostad, <em>med en stor solterrass</em>')
p('.residences.copy',
  'Un apartamento de dos dormitorios y dos baños en la segunda planta del Bloque 19, con tres terrazas y un nivel de solárium.',
  'Un appartement de deux chambres et deux salles de bains au deuxième étage du bloc 19, avec trois terrasses et un niveau de solarium.',
  'Eine Wohnung mit zwei Schlafzimmern und zwei Bädern im zweiten Obergeschoss von Block 19, mit drei Terrassen und einer Solariumebene.',
  'Квартира с двумя спальнями и двумя ванными комнатами на третьем этаже блока 19, с тремя террасами и уровнем солярия.',
  'شقة بغرفتي نوم وحمامين في الطابق الثاني من المبنى 19، مع ثلاثة تراسات ومستوى سولاريوم.',
  'Een appartement met twee slaapkamers en twee badkamers op de tweede verdieping van blok 19, met drie terrassen en een solariumniveau.',
  'Mieszkanie z dwiema sypialniami i dwiema łazienkami na drugim piętrze bloku 19, z trzema tarasami i poziomem solarium.',
  'En leilighet med to soverom og to bad i andre etasje i hus 19, med tre terrasser og et solterrassenivå.',
  'En lägenhet med två sovrum och två badrum på andra våningen i hus 19, med tre terrasser och en solterrassnivå.')
p('.residences.items[0].features[0]',
  'Segunda planta, Bloque 19. Salón-comedor de 26.10 [m2], cocina de 14.28 [m2], dos dormitorios de 20.86 y 13.70 [m2], dos baños de 4.33 y 3.72 [m2], un hall de 3.30 [m2] y un pasillo de 3.02 [m2], que suman los 89.31 [m2] de superficie útil interior del plano.',
  'Deuxième étage, bloc 19. Séjour-salle à manger de 26.10 [m2], cuisine de 14.28 [m2], deux chambres de 20.86 et 13.70 [m2], deux salles de bains de 4.33 et 3.72 [m2], une entrée de 3.30 [m2] et un couloir de 3.02 [m2], soit les 89.31 [m2] de surface utile intérieure du plan.',
  'Zweites Obergeschoss, Block 19. Wohn- und Esszimmer von 26.10 [m2], Küche von 14.28 [m2], zwei Schlafzimmer von 20.86 und 13.70 [m2], zwei Bäder von 4.33 und 3.72 [m2], ein Eingangsbereich von 3.30 [m2] und ein Flur von 3.02 [m2], zusammen die 89.31 [m2] Nutzfläche im Inneren laut Plan.',
  'Третий этаж, блок 19. Гостиная-столовая 26.10 [m2], кухня 14.28 [m2], две спальни 20.86 и 13.70 [m2], две ванные комнаты 4.33 и 3.72 [m2], холл 3.30 [m2] и коридор 3.02 [m2], что вместе составляет 89.31 [m2] полезной внутренней площади по плану.',
  'الطابق الثاني، المبنى 19. صالة جلوس وطعام بمساحة 26.10 [m2]، ومطبخ بمساحة 14.28 [m2]، وغرفتا نوم بمساحة 20.86 و13.70 [m2]، وحمامان بمساحة 4.33 و3.72 [m2]، ومدخل بمساحة 3.30 [m2] وممر بمساحة 3.02 [m2]، وهي مجتمعة 89.31 [m2] من المساحة الداخلية المفيدة في المخطط.',
  'Tweede verdieping, blok 19. Woon-eetkamer van 26.10 [m2], keuken van 14.28 [m2], twee slaapkamers van 20.86 en 13.70 [m2], twee badkamers van 4.33 en 3.72 [m2], een hal van 3.30 [m2] en een gang van 3.02 [m2], samen de 89.31 [m2] bruikbaar binnenoppervlak op het plan.',
  'Drugie piętro, blok 19. Salon z jadalnią 26.10 [m2], kuchnia 14.28 [m2], dwie sypialnie 20.86 i 13.70 [m2], dwie łazienki 4.33 i 3.72 [m2], hol 3.30 [m2] i korytarz 3.02 [m2], co razem daje 89.31 [m2] użytkowej powierzchni wnętrza według rzutu.',
  'Andre etasje, hus 19. Stue og spisestue på 26.10 [m2], kjøkken på 14.28 [m2], to soverom på 20.86 og 13.70 [m2], to bad på 4.33 og 3.72 [m2], en entré på 3.30 [m2] og en gang på 3.02 [m2], til sammen de 89.31 [m2] bruksareal innvendig på planen.',
  'Andra våningen, hus 19. Vardagsrum och matplats på 26.10 [m2], kök på 14.28 [m2], två sovrum på 20.86 och 13.70 [m2], två badrum på 4.33 och 3.72 [m2], en hall på 3.30 [m2] och en korridor på 3.02 [m2], tillsammans de 89.31 [m2] nyttoarea inomhus på ritningen.')
p('.residences.items[0].features[1]',
  'Terrazas de 28.85, 21.44 y 5.23 [m2], la última cubierta, que suman 55.52 [m2] construidos y 40.10 [m2] útiles. Un solárium de 109.60 [m2] construidos y 96.43 [m2] útiles, al que se llega por una escalera de caracol dibujada en el plano.',
  'Terrasses de 28.85, 21.44 et 5.23 [m2], la dernière couverte, soit 55.52 [m2] construits et 40.10 [m2] utiles. Un solarium de 109.60 [m2] construits et 96.43 [m2] utiles, auquel on accède par un escalier en colimaçon dessiné sur le plan.',
  'Terrassen von 28.85, 21.44 und 5.23 [m2], die letzte überdacht, zusammen 55.52 [m2] bebaut und 40.10 [m2] nutzbar. Ein Solarium von 109.60 [m2] bebaut und 96.43 [m2] nutzbar, das über eine im Plan eingezeichnete Wendeltreppe erreicht wird.',
  'Террасы 28.85, 21.44 и 5.23 [m2], последняя крытая, что вместе составляет 55.52 [m2] застроенной и 40.10 [m2] полезной площади. Солярий 109.60 [m2] застроенной и 96.43 [m2] полезной площади, на который ведёт винтовая лестница, нарисованная на плане.',
  'تراسات بمساحة 28.85 و21.44 و5.23 [m2]، الأخيرة مسقوفة، وهي مجتمعة 55.52 [m2] مبنية و40.10 [m2] مفيدة. وسولاريوم بمساحة 109.60 [m2] مبنية و96.43 [m2] مفيدة، يُصعد إليه بدرج حلزوني مرسوم في المخطط.',
  'Terrassen van 28.85, 21.44 en 5.23 [m2], de laatste overdekt, samen 55.52 [m2] bebouwd en 40.10 [m2] bruikbaar. Een solarium van 109.60 [m2] bebouwd en 96.43 [m2] bruikbaar, bereikbaar via een op het plan getekende wenteltrap.',
  'Tarasy 28.85, 21.44 i 5.23 [m2], ostatni zadaszony, co razem daje 55.52 [m2] zabudowy i 40.10 [m2] powierzchni użytkowej. Solarium 109.60 [m2] zabudowy i 96.43 [m2] powierzchni użytkowej, na które prowadzą spiralne schody narysowane na rzucie.',
  'Terrasser på 28.85, 21.44 og 5.23 [m2], den siste overbygd, til sammen 55.52 [m2] bebygd og 40.10 [m2] bruksareal. En solterrasse på 109.60 [m2] bebygd og 96.43 [m2] bruksareal, som nås med en spiraltrapp tegnet på planen.',
  'Terrasser på 28.85, 21.44 och 5.23 [m2], den sista övertäckt, tillsammans 55.52 [m2] byggyta och 40.10 [m2] nyttoarea. En solterrass på 109.60 [m2] byggyta och 96.43 [m2] nyttoarea, som nås med en spiraltrappa som är ritad på ritningen.')

# 75-82 lifestyle
p('.lifestyle.headlineHtml',
  'Piscina, jardines <em>y una laguna</em>', 'Piscine, jardins <em>et un lagon</em>', 'Pool, Gärten <em>und eine Lagune</em>',
  'Бассейн, сады <em>и лагуна</em>', 'مسبح وحدائق <em>وبحيرة لاغون</em>', 'Zwembad, tuinen <em>en een lagune</em>',
  'Basen, ogrody <em>i laguna</em>', 'Basseng, hager <em>og en lagune</em>', 'Pool, trädgårdar <em>och en lagun</em>')
p('.lifestyle.copy',
  'Las zonas comunes que enumera la ficha informativa de 2024, y lo que muestran las fotografías.',
  'Les espaces communs que cite la fiche d’information de 2024, et ce que montrent les photographies.',
  'Die Gemeinschaftsbereiche, die das Infoblatt von 2024 nennt, und was die Fotos zeigen.',
  'Общие зоны, которые перечислены в информационном листе 2024 года, и то, что показано на фотографиях.',
  'المرافق المشتركة التي تذكرها نشرة المعلومات لعام 2024، وما تُظهره الصور.',
  'De gemeenschappelijke voorzieningen die het infoblad van 2024 noemt, en wat de foto’s tonen.',
  'Części wspólne wymienione w karcie informacyjnej z 2024 r. oraz to, co pokazują zdjęcia.',
  'Fellesarealene som informasjonsarket fra 2024 oppgir, og det fotografiene viser.',
  'De gemensamma ytorna som informationsbladet från 2024 anger, och det som fotografierna visar.')
p('.lifestyle.panels[0][1]',
  'Una piscina de diseño moderno, según la ficha informativa. Las fotografías muestran una piscina grande con tumbonas y palmeras, y una piscina más pequeña sobre el césped.',
  'Une piscine au design moderne, selon la fiche d’information. Les photographies montrent une grande piscine avec des bains de soleil et des palmiers, et une piscine plus petite sur la pelouse.',
  'Ein Pool in modernem Design, laut Infoblatt. Die Fotos zeigen einen großen Pool mit Sonnenliegen und Palmen sowie einen kleineren Pool auf einer Rasenfläche.',
  'Бассейн современного дизайна, согласно информационному листу. На фотографиях виден большой бассейн с шезлонгами и пальмами и небольшой бассейн на газоне.',
  'مسبح بتصميم عصري بحسب نشرة المعلومات. وتُظهر الصور مسبحاً كبيراً مع كراسي استلقاء ونخيل، ومسبحاً أصغر على المرج.',
  'Een zwembad met modern ontwerp, volgens het infoblad. De foto’s tonen een groot zwembad met ligbedden en palmbomen en een kleiner zwembad op een grasveld.',
  'Basen o nowoczesnym designie, według karty informacyjnej. Zdjęcia pokazują duży basen z leżakami i palmami oraz mniejszy basen na trawniku.',
  'Et basseng med moderne design, ifølge informasjonsarket. Fotografiene viser et stort basseng med solsenger og palmer og et mindre basseng på en plen.',
  'En pool med modern design, enligt informationsbladet. Fotografierna visar en stor pool med solstolar och palmer och en mindre pool på en gräsmatta.')
p('.lifestyle.panels[1][0]',
  'La laguna', 'Le lagon', 'Die Lagune', 'Лагуна', 'بحيرة اللاغون', 'De lagune', 'Laguna', 'Lagunen', 'Lagunen')
p('.lifestyle.panels[1][1]',
  'La ficha informativa enumera el uso exclusivo de una laguna de aguas cristalinas. Preguntamos al promotor cómo la usan los residentes antes de cualquier reserva.',
  'La fiche d’information cite l’usage exclusif d’un lagon aux eaux cristallines. Nous demandons au promoteur comment les résidents l’utilisent avant toute réservation.',
  'Das Infoblatt nennt die exklusive Nutzung einer kristallklaren Lagune. Wir fragen den Bauträger vor jeder Reservierung, wie die Bewohner sie nutzen.',
  'В информационном листе указано эксклюзивное пользование кристально чистой лагуной. Мы спрашиваем у застройщика, как ею пользуются жители, до любого бронирования.',
  'تذكر نشرة المعلومات الاستخدام الحصري لبحيرة لاغون صافية الماء. نسأل المطوّر عن كيفية استخدام السكان لها قبل أي حجز.',
  'Het infoblad vermeldt het exclusieve gebruik van een kristalheldere lagune. We vragen de ontwikkelaar vóór elke reservering hoe de bewoners haar gebruiken.',
  'Karta informacyjna wymienia wyłączne korzystanie z krystalicznie czystej laguny. Przed każdą rezerwacją pytamy dewelopera, jak mieszkańcy z niej korzystają.',
  'Informasjonsarket oppgir eksklusiv bruk av en krystallklar lagune. Vi spør utbyggeren hvordan beboerne bruker den før enhver reservasjon.',
  'Informationsbladet anger exklusiv användning av en kristallklar lagun. Vi frågar exploatören hur de boende använder den före varje reservation.')
p('.lifestyle.panels[2][0]',
  'Jardines y juegos', 'Jardins et jeux', 'Gärten und Spielen', 'Сады и игры', 'الحدائق واللعب', 'Tuinen en spelen', 'Ogrody i zabawa', 'Hager og lek', 'Trädgårdar och lek')
p('.lifestyle.panels[2][1]',
  'Jardines tropicales modernos y una zona de juegos infantil, según la ficha informativa, con riego e iluminación de todo el conjunto en la memoria de calidades.',
  'Des jardins tropicaux modernes et une aire de jeux pour enfants, selon la fiche d’information, avec arrosage et éclairage de tout l’ensemble dans le descriptif.',
  'Moderne tropische Gärten und ein Kinderspielplatz, laut Infoblatt, mit Bewässerung und Beleuchtung für die gesamte Anlage in der Baubeschreibung.',
  'Современные тропические сады и детская площадка, согласно информационному листу, а в спецификации — полив и освещение всего комплекса.',
  'حدائق استوائية عصرية ومنطقة ألعاب للأطفال بحسب نشرة المعلومات، مع ري وإنارة للمجمّع كله في المواصفات.',
  'Moderne tropische tuinen en een speeltuin, volgens het infoblad, met in de specificatie irrigatie en verlichting voor het hele complex.',
  'Nowoczesne tropikalne ogrody i plac zabaw, według karty informacyjnej, a w specyfikacji nawadnianie i oświetlenie całego osiedla.',
  'Moderne tropiske hager og en lekeplass, ifølge informasjonsarket, med vanning og belysning for hele anlegget i spesifikasjonen.',
  'Moderna tropiska trädgårdar och en lekplats, enligt informationsbladet, med bevattning och belysning för hela området i specifikationen.')
p('.lifestyle.panels[3][1]',
  'Una plaza de garaje y un trastero con cada vivienda, según la ficha informativa.',
  'Une place de parking et une cave avec chaque logement, selon la fiche d’information.',
  'Ein Stellplatz und ein Abstellraum bei jeder Wohnung, laut Infoblatt.',
  'По одному месту в гараже и одной кладовой при каждой квартире, согласно информационному листу.',
  'موقف سيارة واحد وغرفة تخزين واحدة مع كل مسكن، بحسب نشرة المعلومات.',
  'Eén parkeerplaats en één berging bij elke woning, volgens het infoblad.',
  'Jedno miejsce postojowe i jedna komórka lokatorska przy każdym mieszkaniu, według karty informacyjnej.',
  'Én parkeringsplass og én bod til hver bolig, ifølge informasjonsarket.',
  'En parkeringsplats och ett förråd till varje bostad, enligt informationsbladet.')

# 83-84 location
p('.location.headlineHtml',
  'Casares, <em>Costa del Sol</em>', 'Casares, <em>Costa del Sol</em>', 'Casares, <em>Costa del Sol</em>', 'Касарес, <em>Коста-дель-Соль</em>',
  'كاساريس، <em>كوستا ديل سول</em>', 'Casares, <em>Costa del Sol</em>', 'Casares, <em>Costa del Sol</em>', 'Casares, <em>Costa del Sol</em>', 'Casares, <em>Costa del Sol</em>')
p('.location.copy',
  'Alcazaba Lagoon IV está en Casares, en la Costa del Sol, tal como la nombran los planos y la memoria de calidades del promotor. El mapa de la ficha informativa la sitúa al oeste del puerto deportivo de Estepona.',
  'Alcazaba Lagoon IV se trouve à Casares, sur la Costa del Sol, comme le nomment les plans et le descriptif du promoteur. La carte de la fiche d’information le place à l’ouest du port de plaisance d’Estepona.',
  'Alcazaba Lagoon IV liegt in Casares an der Costa del Sol, wie es die Pläne und die Baubeschreibung des Bauträgers benennen. Die Karte im Infoblatt verortet es westlich des Sporthafens von Estepona.',
  'Alcazaba Lagoon IV находится в Касаресе на Коста-дель-Соль — так его называют планы и спецификация застройщика. На карте из информационного листа он обозначен к западу от спортивной гавани Эстепоны.',
  'يقع Alcazaba Lagoon IV في كاساريس على كوستا ديل سول، كما تسميه مخططات المطوّر ومواصفاته. وتضعه خريطة نشرة المعلومات إلى الغرب من الميناء الرياضي في إستيبونا.',
  'Alcazaba Lagoon IV ligt in Casares aan de Costa del Sol, zoals de plannen en de specificatie van de ontwikkelaar het noemen. De kaart in het infoblad plaatst het ten westen van de jachthaven van Estepona.',
  'Alcazaba Lagoon IV leży w Casares na Costa del Sol, tak jak nazywają to plany i specyfikacja dewelopera. Mapa w karcie informacyjnej umieszcza go na zachód od portu sportowego w Esteponie.',
  'Alcazaba Lagoon IV ligger i Casares på Costa del Sol, slik utbyggerens planer og spesifikasjon navngir det. Kartet i informasjonsarket plasserer det vest for sportshavnen i Estepona.',
  'Alcazaba Lagoon IV ligger i Casares på Costa del Sol, så som exploatörens planritningar och specifikation anger det. Kartan i informationsbladet placerar det väster om sporthamnen i Estepona.')

# 85-92 investment, trust
p('.investment.copy',
  'Confirmamos con el promotor los importes, las fechas y las condiciones vigentes, y se los damos por escrito antes de que reserve.',
  'Nous confirmons avec le promoteur les montants, les dates et les conditions en vigueur, et nous vous les remettons par écrit avant que vous ne réserviez.',
  'Wir bestätigen mit dem Bauträger die aktuellen Beträge, Termine und Bedingungen und halten sie schriftlich fest, bevor Sie reservieren.',
  'Мы подтверждаем у застройщика актуальные суммы, сроки и условия и фиксируем их письменно до того, как вы забронируете.',
  'نؤكد مع المطوّر المبالغ والمواعيد والشروط الحالية، ونقدّمها لكم كتابةً قبل أن تحجزوا.',
  'We bevestigen bij de ontwikkelaar de actuele bedragen, data en voorwaarden en leggen ze schriftelijk vast voordat u reserveert.',
  'Aktualne kwoty, terminy i warunki potwierdzamy u dewelopera i przekazujemy Państwu na piśmie przed rezerwacją.',
  'Vi bekrefter gjeldende beløp, datoer og vilkår med utbyggeren og får dem skriftlig før reservasjonen.',
  'Vi bekräftar aktuella belopp, datum och villkor med exploatören och ger er dem skriftligen innan ni reserverar.')
p('.investment.cards[2][1]',
  'La lista de precios del promotor indica que los precios son netos y no incluyen el IVA, el impuesto sobre el valor añadido español. Confirmamos por escrito los impuestos y los gastos de compra.',
  'La liste de prix du promoteur indique que les prix s’entendent nets, hors TVA (IVA), la taxe espagnole sur la valeur ajoutée. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Die Preisliste des Bauträgers gibt an, dass die Preise netto sind und die spanische MwSt. (IVA) nicht enthalten. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'В прайс-листе застройщика указано, что цены нетто и не включают испанский НДС (IVA). Налоги и расходы на покупку мы подтверждаем письменно.',
  'تذكر قائمة أسعار المطوّر أن الأسعار صافية ولا تشمل ضريبة القيمة المضافة (IVA) الإسبانية. ونؤكد الضرائب وتكاليف الشراء كتابةً.',
  'De prijslijst van de ontwikkelaar vermeldt dat de prijzen netto zijn en de Spaanse btw (IVA) niet omvatten. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Cennik dewelopera podaje, że ceny są netto i nie obejmują hiszpańskiego VAT (IVA). Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Utbyggerens prisliste oppgir at prisene er netto og ikke inkluderer den spanske mva (IVA). Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Exploatörens prislista anger att priserna är netto och inte inkluderar IVA, den spanska skatten på mervärde (spansk moms). Vi bekräftar skatter och köpkostnader skriftligen.')
p('.investment.cards[3][1]',
  'La ficha informativa de 2024 dice que se incluyen una plaza de garaje y un trastero. La lista de precios de julio de 2025 nombra la plaza Ext-5 y el trastero 15 para AL4-1924. Confirmamos ambos por escrito.',
  'La fiche d’information de 2024 indique qu’une place de parking et une cave sont incluses. La liste de prix de juillet 2025 nomme la place Ext-5 et la cave 15 pour AL4-1924. Nous confirmons les deux par écrit.',
  'Das Infoblatt von 2024 nennt einen Stellplatz und einen Abstellraum als enthalten. Die Preisliste vom Juli 2025 benennt für AL4-1924 den Stellplatz Ext-5 und den Abstellraum 15. Wir bestätigen beides schriftlich.',
  'В информационном листе 2024 года сказано, что включены одно место в гараже и одна кладовая. В прайс-листе за июль 2025 года для AL4-1924 названы место Ext-5 и кладовая 15. Мы подтверждаем и то и другое письменно.',
  'تقول نشرة المعلومات لعام 2024 إن موقف سيارة وغرفة تخزين مشمولان. وتذكر قائمة أسعار يوليو 2025 الموقف Ext-5 وغرفة التخزين 15 للمسكن AL4-1924. ونؤكد كليهما كتابةً.',
  'Het infoblad van 2024 zegt dat een parkeerplaats en een berging zijn inbegrepen. De prijslijst van juli 2025 noemt voor AL4-1924 plaats Ext-5 en berging 15. We bevestigen beide schriftelijk.',
  'Karta informacyjna z 2024 r. podaje, że w cenie jest jedno miejsce postojowe i jedna komórka lokatorska. Cennik z lipca 2025 r. wskazuje dla AL4-1924 miejsce Ext-5 i komórkę 15. Oba potwierdzamy na piśmie.',
  'Informasjonsarket fra 2024 sier at en parkeringsplass og en bod er inkludert. Prislisten fra juli 2025 oppgir plass Ext-5 og bod 15 for AL4-1924. Vi bekrefter begge skriftlig.',
  'Informationsbladet från 2024 anger att en parkeringsplats och ett förråd ingår. Prislistan från juli 2025 anger plats Ext-5 och förråd 15 för AL4-1924. Vi bekräftar båda skriftligen.')
p('.trustDossier.cards[0][1]',
  'La lista de disponibilidad indica que la urbanización está terminada, y la ficha informativa de 2024 dice que está lista para entrar con la licencia de obras en vigor. Pedimos la licencia de primera ocupación y el certificado final de obra.',
  'La liste de disponibilité indique que l’ensemble est achevé, et la fiche d’information de 2024 dit qu’il est prêt à emménager, avec le permis de construire en vigueur. Nous demandons la licence de première occupation et le certificat de fin de travaux.',
  'Die Verfügbarkeitsliste gibt die Anlage als fertiggestellt an, und das Infoblatt von 2024 sagt bezugsfertig, mit vorliegender Baugenehmigung. Wir fordern die Erstbezugsgenehmigung und die Fertigstellungsbescheinigung an.',
  'Список доступных объектов указывает, что комплекс построен, а в информационном листе 2024 года сказано, что он готов к заселению и разрешение на строительство действует. Мы запрашиваем лицензию на первое заселение и акт о завершении строительства.',
  'تذكر قائمة التوفر أن المجمّع مكتمل، وتقول نشرة المعلومات لعام 2024 إنه جاهز للسكن مع رخصة بناء سارية. ونطلب رخصة السكن الأول وشهادة إتمام البناء.',
  'De beschikbaarheidslijst geeft het complex als opgeleverd aan, en het infoblad van 2024 zegt sleutelklaar, met een geldige bouwvergunning. We vragen de eerste-bewoningsvergunning en het opleveringscertificaat op.',
  'Lista dostępności podaje, że osiedle jest ukończone, a karta informacyjna z 2024 r. mówi, że jest gotowe do zamieszkania, a pozwolenie na budowę jest w mocy. Prosimy o licencję pierwszego zamieszkania i zaświadczenie o zakończeniu budowy.',
  'Tilgjengelighetslisten oppgir at anlegget er ferdigstilt, og informasjonsarket fra 2024 sier innflyttingsklart, med byggetillatelsen på plass. Vi ber om førstegangsbruksbevillingen og ferdigattesten.',
  'Tillgänglighetslistan anger att området är färdigställt, och informationsbladet från 2024 säger nyckelfärdigt, med bygglovet på plats. Vi begär bruksgodkännandet och slutbeviset.')
p('.trustDossier.cards[1][1]',
  'El plano da 107.57 [m2] construidos y 89.31 [m2] útiles para la vivienda, 55.52 y 40.10 [m2] para las terrazas, y 109.60 y 96.43 [m2] para el solárium. Dice que las superficies son aproximadas y pueden cambiar por razones técnicas, y confirmamos las superficies de la escritura.',
  'Le plan donne 107.57 [m2] construits et 89.31 [m2] utiles pour le logement, 55.52 et 40.10 [m2] pour les terrasses, et 109.60 et 96.43 [m2] pour le solarium. Il indique que les surfaces sont approximatives et peuvent changer pour des raisons techniques, et nous confirmons les surfaces de l’acte.',
  'Der Plan gibt für die Wohnung 107.57 [m2] bebaut und 89.31 [m2] nutzbar an, für die Terrassen 55.52 und 40.10 [m2] und für das Solarium 109.60 und 96.43 [m2]. Er weist darauf hin, dass die Flächen ungefähr sind und sich aus technischen Gründen ändern können; wir bestätigen die Flächen in der Urkunde.',
  'На плане для квартиры указано 107.57 [m2] застроенной и 89.31 [m2] полезной площади, для террас — 55.52 и 40.10 [m2], для солярия — 109.60 и 96.43 [m2]. В нём сказано, что площади приблизительные и могут измениться по техническим причинам; мы подтверждаем площади по договору.',
  'يعطي المخطط للمسكن 107.57 [m2] مبنية و89.31 [m2] مفيدة، وللتراسات 55.52 و40.10 [m2]، وللسولاريوم 109.60 و96.43 [m2]. ويقول إن المساحات تقريبية وقد تتغير لأسباب فنية، ونؤكد المساحات الواردة في سند الملكية.',
  'Het plan geeft voor de woning 107.57 [m2] bebouwd en 89.31 [m2] bruikbaar, voor de terrassen 55.52 en 40.10 [m2] en voor het solarium 109.60 en 96.43 [m2]. Het zegt dat de oppervlakten bij benadering zijn en om technische redenen kunnen veranderen, en we bevestigen de oppervlakten in de akte.',
  'Rzut podaje dla mieszkania 107.57 [m2] zabudowy i 89.31 [m2] powierzchni użytkowej, dla tarasów 55.52 i 40.10 [m2], a dla solarium 109.60 i 96.43 [m2]. Zastrzega, że powierzchnie są przybliżone i mogą się zmienić z przyczyn technicznych, a my potwierdzamy powierzchnie w akcie.',
  'Planen oppgir 107.57 [m2] bebygd og 89.31 [m2] bruksareal for boligen, 55.52 og 40.10 [m2] for terrassene og 109.60 og 96.43 [m2] for solterrassen. Den sier at arealene er omtrentlige og kan endres av tekniske grunner, og vi bekrefter arealene i skjøtet.',
  'Ritningen anger 107.57 [m2] byggyta och 89.31 [m2] nyttoarea för bostaden, 55.52 och 40.10 [m2] för terrasserna och 109.60 och 96.43 [m2] för solterrassen. Den säger att ytorna är ungefärliga och kan ändras av tekniska skäl, och vi bekräftar ytorna i köpebrevet.')
p('.trustDossier.cards[2][0]',
  'Las dos listas', 'Les deux listes', 'Die zwei Listen', 'Два списка', 'القائمتان', 'De twee lijsten', 'Dwie listy', 'De to listene', 'De två listorna')
p('.trustDossier.cards[2][1]',
  'La lista de precios del 17 de julio de 2025 muestra AL4-1924 como reservada, mientras que la lista de disponibilidad del 29 de octubre de 2026 la muestra como disponible a €615000. Confirmamos que está libre antes de cualquier visita.',
  'La liste de prix du 17 juillet 2025 montre AL4-1924 comme réservé, alors que la liste de disponibilité du 29 octobre 2026 le montre comme disponible à €615000. Nous confirmons qu’il est libre avant toute visite.',
  'Die Preisliste vom 17. Juli 2025 weist AL4-1924 als reserviert aus, während die Verfügbarkeitsliste vom 29. Oktober 2026 sie als verfügbar zu €615000 ausweist. Wir bestätigen, dass sie frei ist, bevor eine Besichtigung stattfindet.',
  'В прайс-листе от 17 июля 2025 года AL4-1924 значится как зарезервированная, а в списке доступных объектов от 29 октября 2026 года — как доступная за €615000. Мы подтверждаем, что она свободна, до любого просмотра.',
  'تُظهر قائمة الأسعار بتاريخ 17 يوليو 2025 المسكن AL4-1924 محجوزاً، بينما تُظهره قائمة التوفر بتاريخ 29 أكتوبر 2026 متاحاً بسعر €615000. ونؤكد أنه شاغر قبل أي معاينة.',
  'De prijslijst van 17 juli 2025 toont AL4-1924 als gereserveerd, terwijl de beschikbaarheidslijst van 29 oktober 2026 haar als beschikbaar toont voor €615000. We bevestigen dat ze vrij is vóór elke bezichtiging.',
  'Cennik z 17 lipca 2025 r. pokazuje AL4-1924 jako zarezerwowane, a lista dostępności z 29 października 2026 r. jako dostępne za €615000. Przed każdą wizytą potwierdzamy, że mieszkanie jest wolne.',
  'Prislisten fra 17. juli 2025 viser AL4-1924 som reservert, mens tilgjengelighetslisten fra 29. oktober 2026 viser den som tilgjengelig til €615000. Vi bekrefter at den er ledig før enhver visning.',
  'Prislistan från den 17 juli 2025 visar AL4-1924 som reserverad, medan tillgänglighetslistan från den 29 oktober 2026 visar den som tillgänglig för €615000. Vi bekräftar att den är ledig före varje visning.')
p('.trustDossier.cards[3][1]',
  'La lista de precios nombra la plaza Ext-5 y el trastero 15 para esta vivienda, y la ficha informativa dice que se incluyen una plaza de garaje y un trastero. Confirmamos cuáles pertenecen a la vivienda y dónde están.',
  'La liste de prix nomme la place Ext-5 et la cave 15 pour ce logement, et la fiche d’information dit qu’une place de parking et une cave sont incluses. Nous confirmons lesquelles appartiennent au logement et où elles se trouvent.',
  'Die Preisliste benennt für diese Wohnung den Stellplatz Ext-5 und den Abstellraum 15, und das Infoblatt nennt einen Stellplatz und einen Abstellraum als enthalten. Wir bestätigen, welche zur Wohnung gehören und wo sie liegen.',
  'В прайс-листе для этой квартиры названы место Ext-5 и кладовая 15, а в информационном листе сказано, что включены одно место в гараже и одна кладовая. Мы подтверждаем, какие из них относятся к квартире и где они расположены.',
  'تذكر قائمة الأسعار الموقف Ext-5 وغرفة التخزين 15 لهذا المسكن، وتقول نشرة المعلومات إن موقف سيارة وغرفة تخزين مشمولان. ونؤكد أيهما يتبع المسكن وأين يقعان.',
  'De prijslijst noemt voor deze woning plaats Ext-5 en berging 15, en het infoblad zegt dat een parkeerplaats en een berging zijn inbegrepen. We bevestigen welke bij de woning horen en waar ze liggen.',
  'Cennik wskazuje dla tego mieszkania miejsce Ext-5 i komórkę 15, a karta informacyjna mówi, że w cenie jest jedno miejsce postojowe i jedna komórka lokatorska. Potwierdzamy, które należą do mieszkania i gdzie się znajdują.',
  'Prislisten oppgir plass Ext-5 og bod 15 for denne boligen, og informasjonsarket sier at en parkeringsplass og en bod er inkludert. Vi bekrefter hvilke som hører til boligen, og hvor de ligger.',
  'Prislistan anger plats Ext-5 och förråd 15 för den här bostaden, och informationsbladet säger att en parkeringsplats och ett förråd ingår. Vi bekräftar vilka som hör till bostaden och var de ligger.')

# 94-95 availability
p('.availability.copy',
  'La vivienda AL4-1924 es un apartamento de dos dormitorios y dos baños en la segunda planta del Bloque 19, con tres terrazas y un solárium. La disponibilidad y el precio son los listados el 29 de octubre de 2026 y no incluyen el IVA. Los confirmamos antes de cualquier reserva.',
  'Le logement AL4-1924 est un appartement de deux chambres et deux salles de bains au deuxième étage du bloc 19, avec trois terrasses et un solarium. La disponibilité et le prix sont ceux de la liste du 29 octobre 2026 et s’entendent hors TVA. Nous les confirmons avant toute réservation.',
  'Die Wohnung AL4-1924 ist eine Wohnung mit zwei Schlafzimmern und zwei Bädern im zweiten Obergeschoss von Block 19, mit drei Terrassen und einem Solarium. Verfügbarkeit und Preis entsprechen der Liste vom 29. Oktober 2026 und verstehen sich ohne MwSt. Wir bestätigen sie vor jeder Reservierung.',
  'Квартира AL4-1924 — это квартира с двумя спальнями и двумя ванными комнатами на третьем этаже блока 19, с тремя террасами и солярием. Наличие и цена указаны по списку от 29 октября 2026 года и даны без НДС. Мы подтверждаем их до любого бронирования.',
  'المسكن AL4-1924 شقة بغرفتي نوم وحمامين في الطابق الثاني من المبنى 19، مع ثلاثة تراسات وسولاريوم. التوفر والسعر هما المدرجان في 29 أكتوبر 2026 ولا يشملان ضريبة القيمة المضافة. ونؤكدهما قبل أي حجز.',
  'Woning AL4-1924 is een appartement met twee slaapkamers en twee badkamers op de tweede verdieping van blok 19, met drie terrassen en een solarium. Beschikbaarheid en prijs zijn die van de lijst van 29 oktober 2026 en zijn exclusief btw. We bevestigen ze vóór elke reservering.',
  'Mieszkanie AL4-1924 to apartament z dwiema sypialniami i dwiema łazienkami na drugim piętrze bloku 19, z trzema tarasami i solarium. Dostępność i cena są zgodne z listą z 29 października 2026 r. i nie zawierają VAT. Potwierdzamy je przed każdą rezerwacją.',
  'Bolig AL4-1924 er en leilighet med to soverom og to bad i andre etasje i hus 19, med tre terrasser og en solterrasse. Tilgjengelighet og pris er slik de er oppført 29. oktober 2026, og er eksklusive mva. Vi bekrefter dem før enhver reservasjon.',
  'Bostad AL4-1924 är en lägenhet med två sovrum och två badrum på andra våningen i hus 19, med tre terrasser och en solterrass. Tillgänglighet och pris är som de listades den 29 oktober 2026 och är exklusive IVA. Vi bekräftar dem före varje reservation.')
p('.availability.sourceNote',
  'La referencia, los dormitorios, la superficie construida, el precio y la fase de obra proceden de la lista de disponibilidad a 29 de octubre de 2026, que incluye una vivienda como disponible. La planta, los tamaños de las estancias, las superficies útiles, el garaje y el trastero proceden del plano del promotor de la vivienda y de su lista de precios del 17 de julio de 2025. Esa lista anterior muestra AL4-1924 como reservada; usamos la lista posterior para la disponibilidad y el precio, y la confirmamos antes de cualquier reserva. La lista de precios indica que los precios son netos y no incluyen el IVA. Los 59 apartamentos y sus uno, dos y tres dormitorios proceden de la ficha informativa de 2024 y del título de los planos de la fase. Las superficies del plano son aproximadas y los nombres de sus estancias están en español.',
  'La référence, les chambres, la surface construite, le prix et l’état d’avancement proviennent de la liste de disponibilité au 29 octobre 2026, qui indique un logement comme disponible. L’étage, la taille des pièces, les surfaces utiles, le parking et la cave proviennent du plan du promoteur pour ce logement et de sa liste de prix du 17 juillet 2025. Cette liste antérieure montre AL4-1924 comme réservé ; nous utilisons la liste postérieure pour la disponibilité et le prix, et nous la confirmons avant toute réservation. La liste de prix indique que les prix s’entendent nets, hors TVA (IVA). Les 59 appartements et leurs une, deux et trois chambres proviennent de la fiche d’information de 2024 et du titre des plans de la phase. Les surfaces du plan sont approximatives et les noms des pièces y sont en espagnol.',
  'Referenz, Schlafzimmer, bebaute Fläche, Preis und Baustand stammen aus der Verfügbarkeitsliste vom 29. Oktober 2026, die eine Wohnung als verfügbar führt. Stockwerk, Raumgrößen, Nutzflächen, Stellplatz und Abstellraum stammen aus dem Plan des Bauträgers für die Wohnung und aus seiner Preisliste vom 17. Juli 2025. Diese frühere Liste weist AL4-1924 als reserviert aus; für Verfügbarkeit und Preis verwenden wir die spätere Liste und bestätigen sie vor jeder Reservierung. Die Preisliste gibt an, dass die Preise netto sind und die MwSt. (IVA) nicht enthalten. Die 59 Apartments und ihre ein, zwei und drei Schlafzimmer stammen aus dem Infoblatt von 2024 und dem Titel der Pläne der Phase. Die Flächen im Plan sind ungefähre Werte, und seine Raumbezeichnungen sind spanisch.',
  'Номер, число спален, застроенная площадь, цена и стадия готовности взяты из списка доступных объектов на 29 октября 2026 года, в котором числится одна доступная квартира. Этаж, размеры помещений, полезные площади, место в гараже и кладовая взяты из плана застройщика для этой квартиры и его прайс-листа от 17 июля 2025 года. Этот более ранний список показывает AL4-1924 как зарезервированную; для наличия и цены мы используем более поздний список и подтверждаем их до любого бронирования. В прайс-листе указано, что цены нетто и не включают НДС (IVA). Сведения о 59 квартирах с одной, двумя и тремя спальнями взяты из информационного листа 2024 года и из заголовка планов очереди. Площади на плане приблизительные, а названия помещений даны по-испански.',
  'المرجع وغرف النوم والمساحة المبنية والسعر ومرحلة الإنجاز مأخوذة من قائمة التوفر بتاريخ 29 أكتوبر 2026، وهي تدرج مسكناً واحداً على أنه متاح. أما الطابق وقياسات الغرف والمساحات المفيدة والموقف وغرفة التخزين فمأخوذة من مخطط المطوّر للمسكن ومن قائمة أسعاره بتاريخ 17 يوليو 2025. وتُظهر تلك القائمة الأقدم المسكن AL4-1924 محجوزاً؛ ونعتمد القائمة الأحدث للتوفر والسعر ونؤكدها قبل أي حجز. وتذكر قائمة الأسعار أن الأسعار صافية ولا تشمل ضريبة القيمة المضافة (IVA). أما الشقق التسع والخمسون بغرفها الواحدة والاثنتين والثلاث فمأخوذة من نشرة المعلومات لعام 2024 ومن عنوان مخططات المرحلة. والمساحات في المخطط تقريبية، وأسماء غرفه بالإسبانية.',
  'Referentie, slaapkamers, bebouwde oppervlakte, prijs en bouwstand komen uit de beschikbaarheidslijst van 29 oktober 2026, die één woning als beschikbaar vermeldt. Verdieping, kamerafmetingen, bruikbare oppervlakten, parkeerplaats en berging komen uit het plan van de ontwikkelaar voor de woning en uit zijn prijslijst van 17 juli 2025. Die eerdere lijst toont AL4-1924 als gereserveerd; voor beschikbaarheid en prijs gebruiken we de latere lijst en bevestigen we die vóór elke reservering. De prijslijst vermeldt dat de prijzen netto zijn en de btw (IVA) niet omvatten. De 59 appartementen en hun een, twee en drie slaapkamers komen uit het infoblad van 2024 en uit de titel van de plannen van de fase. De oppervlakten op het plan zijn bij benadering en de ruimtenamen erop zijn in het Spaans.',
  'Numer, liczba sypialni, powierzchnia zabudowy, cena i stan zaawansowania pochodzą z listy dostępności na dzień 29 października 2026 r., która wymienia jedno mieszkanie jako dostępne. Piętro, wymiary pomieszczeń, powierzchnie użytkowe, miejsce postojowe i komórka pochodzą z planu dewelopera dla tego mieszkania i z jego cennika z 17 lipca 2025 r. Ten wcześniejszy cennik pokazuje AL4-1924 jako zarezerwowane; dla dostępności i ceny przyjmujemy późniejszą listę i potwierdzamy ją przed każdą rezerwacją. Cennik podaje, że ceny są netto i nie obejmują VAT (IVA). Informacje o 59 apartamentach z jedną, dwiema i trzema sypialniami pochodzą z karty informacyjnej z 2024 r. i z tytułu planów etapu. Powierzchnie na rzucie są przybliżone, a nazwy pomieszczeń na nim są po hiszpańsku.',
  'Referanse, soverom, bebygd areal, pris og byggetrinn er hentet fra tilgjengelighetslisten per 29. oktober 2026, som oppfører én bolig som tilgjengelig. Etasje, romstørrelser, bruksarealer, parkeringsplass og bod er hentet fra utbyggerens plan for boligen og dens prisliste fra 17. juli 2025. Den tidligere listen viser AL4-1924 som reservert; vi bruker den senere listen for tilgjengelighet og pris, og bekrefter den før enhver reservasjon. Prislisten oppgir at prisene er netto og ikke inkluderer mva (IVA). De 59 leilighetene og deres ett, to og tre soverom er hentet fra informasjonsarket fra 2024 og fra tittelen på planene for fasen. Arealene på planen er omtrentlige, og romnavnene på den er på spansk.',
  'Referens, sovrum, byggyta, pris och byggstadium kommer från tillgänglighetslistan per den 29 oktober 2026, som listar en bostad som tillgänglig. Våning, rumsstorlekar, nyttoytor, parkeringsplats och förråd kommer från exploatörens ritning för bostaden och dess prislista från den 17 juli 2025. Den tidigare listan visar AL4-1924 som reserverad; vi använder den senare listan för tillgänglighet och pris och bekräftar den före varje reservation. Prislistan anger att priserna är netto och inte inkluderar IVA. De 59 lägenheterna och deras ett, två och tre sovrum kommer från informationsbladet från 2024 och från rubriken på planritningarna för etappen. Ytorna på ritningen är ungefärliga, och rumsnamnen på den är på spanska.')

# 99-102 timeline
p('.timeline.items[0][2]',
  'El plano de la vivienda disponible, la memoria de calidades y la lista de precios.', 'Le plan du logement disponible, le descriptif et la liste de prix.',
  'Der Grundriss der verfügbaren Wohnung, die Baubeschreibung und die Preisliste.', 'Планировка доступной квартиры, спецификация и прайс-лист.',
  'مخطط المسكن المتاح والمواصفات وقائمة الأسعار.', 'De plattegrond van de beschikbare woning, de specificatie en de prijslijst.',
  'Rzut dostępnego mieszkania, specyfikacja i cennik.', 'Plantegningen av den tilgjengelige boligen, spesifikasjonen og prislisten.',
  'Planritningen för den tillgängliga bostaden, specifikationen och prislistan.')
p('.timeline.items[1][2]',
  'Véalo junto a los demás proyectos de Casares y Estepona que representamos.', 'Découvrez ce programme aux côtés des autres projets de Casares et d’Estepona que nous représentons.',
  'Sehen Sie dieses Projekt neben den anderen Projekten in Casares und Estepona, die wir vertreten.', 'Посмотрите этот проект рядом с другими проектами в Касаресе и Эстепоне, которые мы представляем.',
  'شاهد هذا المشروع إلى جانب مشاريع كاساريس وإستيبونا الأخرى التي نمثّلها.', 'Bekijk dit project naast de andere projecten in Casares en Estepona die wij vertegenwoordigen.',
  'Zobacz tę inwestycję obok innych projektów w Casares i Esteponie, które reprezentujemy.', 'Se dette sammen med de andre prosjektene i Casares og Estepona som vi representerer.',
  'Se detta tillsammans med de andra projekten i Casares och Estepona som vi representerar.')
p('.timeline.items[2][2]',
  'Recorra con nosotros los jardines, la piscina y la vivienda.', 'Parcourez avec nous les jardins, la piscine et le logement.',
  'Gehen Sie mit uns durch die Gärten, am Pool entlang und durch die Wohnung.', 'Пройдите с нами по садам, у бассейна и по квартире.',
  'تجولوا معنا في الحدائق وبجوار المسبح وفي المسكن.', 'Loop met ons door de tuinen, langs het zwembad en door de woning.',
  'Przejdź z nami po ogrodach, wzdłuż basenu i po mieszkaniu.', 'Gå gjennom hagene, langs bassenget og gjennom boligen sammen med oss.',
  'Gå med oss genom trädgårdarna, längs poolen och genom bostaden.')
p('.timeline.items[3][2]',
  'Confirmamos por escrito las condiciones de reserva y el calendario de pagos antes de que se comprometa.', 'Nous confirmons par écrit les conditions de réservation et l’échéancier de paiement avant que vous vous engagiez.',
  'Wir bestätigen die Reservierungsbedingungen und den Zahlungsplan schriftlich, bevor Sie sich binden.', 'Мы письменно подтверждаем условия бронирования и график платежей до того, как вы примете решение.',
  'نؤكد كتابةً شروط الحجز وجدول الدفعات قبل أن تلتزموا.', 'We bevestigen de reserveringsvoorwaarden en het betalingsschema schriftelijk voordat u zich bindt.',
  'Warunki rezerwacji i harmonogram płatności potwierdzamy na piśmie, zanim Państwo podejmą decyzję.', 'Vi bekrefter reservasjonsvilkårene og betalingsplanen skriftlig før det foretas noen forpliktelse.',
  'Vi bekräftar reservationsvillkoren och betalningsplanen skriftligen innan ni binder er.')

# 103-107 privateViewing
p('.privateViewing.headlineHtml',
  'Véala <em>terminada</em>', 'Voyez-le <em>achevé</em>', 'Sehen Sie es <em>fertiggestellt</em>', 'Посмотрите на <em>готовый комплекс</em>',
  'شاهدوه <em>مكتملاً</em>', 'Zie het <em>opgeleverd</em>', 'Zobacz je <em>ukończone</em>', 'Se det <em>ferdigstilt</em>', 'Se det <em>färdigställt</em>')
p('.privateViewing.copy',
  'La urbanización está terminada, así que la visita trata de la vivienda en sí: las terrazas, el solárium y los acabados.',
  'L’ensemble est achevé, la visite porte donc sur le logement lui-même : les terrasses, le solarium et les finitions.',
  'Die Anlage ist fertiggestellt, bei einem Besuch geht es also um die Wohnung selbst: die Terrassen, das Solarium und die Ausführung.',
  'Комплекс построен, поэтому просмотр посвящён самой квартире: террасам, солярию и отделке.',
  'المجمّع مكتمل، لذا تدور المعاينة حول المسكن نفسه: التراسات والسولاريوم والتشطيبات.',
  'Het complex is opgeleverd, dus een bezoek gaat over de woning zelf: de terrassen, het solarium en de afwerking.',
  'Osiedle jest ukończone, więc wizyta dotyczy samego mieszkania: tarasów, solarium i wykończenia.',
  'Anlegget er ferdigstilt, så en visning handler om selve boligen: terrassene, solterrassen og finishen.',
  'Området är färdigställt, så ett besök handlar om själva bostaden: terrasserna, solterrassen och finishen.')
p('.privateViewing.insights[0][1]',
  'Recorra los jardines, la piscina y la vivienda, y vea las terrazas y el solárium.', 'Parcourez les jardins, la piscine et le logement, et voyez les terrasses et le solarium.',
  'Gehen Sie durch die Gärten, am Pool entlang und durch die Wohnung und sehen Sie sich die Terrassen und das Solarium an.', 'Пройдите по садам, у бассейна и по квартире и осмотрите террасы и солярий.',
  'تجولوا في الحدائق وبجوار المسبح وفي المسكن، وشاهدوا التراسات والسولاريوم.', 'Loop door de tuinen, langs het zwembad en door de woning, en bekijk de terrassen en het solarium.',
  'Przejdź po ogrodach, wzdłuż basenu i po mieszkaniu oraz obejrzyj tarasy i solarium.', 'Gå gjennom hagene, langs bassenget og gjennom boligen, og se terrassene og solterrassen.',
  'Gå genom trädgårdarna, längs poolen och genom bostaden, och se terrasserna och solterrassen.')
p('.privateViewing.insights[1][1]',
  'Hacemos con usted los trayectos que le importan y los cronometramos.', 'Nous faisons avec vous les trajets qui comptent pour vous et nous les chronométrons.',
  'Wir fahren mit Ihnen die Strecken, die Ihnen wichtig sind, und stoppen die Zeit.', 'Мы проезжаем с вами маршруты, которые важны для вас, и засекаем время.',
  'نقطع معكم المسارات التي تهمكم ونحتسب الوقت.', 'We rijden met u de routes die voor u belangrijk zijn en nemen de tijd op.',
  'Przejeżdżamy z Państwem trasy, na których Państwu zależy, i mierzymy czas.', 'Vi kjører de rutene som betyr noe, og tar tiden.',
  'Vi kör de sträckor som är viktiga för er tillsammans med er och tar tid.')
p('.privateViewing.insights[2][1]',
  'Licencia de primera ocupación, certificado final de obra y aval bancario, antes de firmar nada.', 'Licence de première occupation, certificat de fin de travaux et garantie bancaire, avant toute signature.',
  'Erstbezugsgenehmigung, Fertigstellungsbescheinigung und Bankgarantie, bevor etwas unterschrieben wird.', 'Лицензия на первое заселение, акт о завершении строительства и банковская гарантия — до подписания чего-либо.',
  'رخصة السكن الأول وشهادة إتمام البناء والضمان المصرفي، قبل توقيع أي شيء.', 'Eerste-bewoningsvergunning, opleveringscertificaat en bankgarantie, vóór er iets wordt ondertekend.',
  'Licencja pierwszego zamieszkania, zaświadczenie o zakończeniu budowy i gwarancja bankowa — zanim cokolwiek zostanie podpisane.', 'Førstegangsbruksbevilling, ferdigattest og bankgaranti, før noe signeres.',
  'Bruksgodkännande, slutbevis och bankgaranti, innan något skrivs under.')

# 110-116 faq
p('.faq[0][1]',
  'La fase tiene 59 apartamentos, según la ficha informativa, y hay uno anunciado como disponible: AL4-1924, un apartamento de dos dormitorios y dos baños en la segunda planta del Bloque 19, por €615000 más IVA.',
  'La phase compte 59 appartements, selon la fiche d’information, et un est actuellement annoncé comme disponible : AL4-1924, un appartement de deux chambres et deux salles de bains au deuxième étage du bloc 19, à €615000 plus TVA.',
  'Die Phase hat laut Infoblatt 59 Apartments, und eines ist derzeit als verfügbar gelistet: AL4-1924, eine Wohnung mit zwei Schlafzimmern und zwei Bädern im zweiten Obergeschoss von Block 19, zu €615000 plus MwSt.',
  'В очереди 59 квартир, согласно информационному листу, и одна сейчас числится доступной: AL4-1924, квартира с двумя спальнями и двумя ванными комнатами на третьем этаже блока 19, за €615000 плюс НДС.',
  'تضم المرحلة 59 شقة بحسب نشرة المعلومات، وشقة واحدة مدرجة حالياً على أنها متاحة: AL4-1924، وهي شقة بغرفتي نوم وحمامين في الطابق الثاني من المبنى 19، بسعر €615000 زائد ضريبة القيمة المضافة.',
  'De fase telt 59 appartementen, volgens het infoblad, en één staat momenteel als beschikbaar vermeld: AL4-1924, een appartement met twee slaapkamers en twee badkamers op de tweede verdieping van blok 19, voor €615000 plus btw.',
  'Etap liczy 59 apartamentów, według karty informacyjnej, a jeden jest obecnie wymieniony jako dostępny: AL4-1924, apartament z dwiema sypialniami i dwiema łazienkami na drugim piętrze bloku 19, za €615000 plus VAT.',
  'Fasen har 59 leiligheter, ifølge informasjonsarket, og én er for tiden oppført som tilgjengelig: AL4-1924, en leilighet med to soverom og to bad i andre etasje i hus 19, til €615000 pluss mva.',
  'Etappen har 59 lägenheter, enligt informationsbladet, och en är för närvarande listad som tillgänglig: AL4-1924, en lägenhet med två sovrum och två badrum på andra våningen i hus 19, för €615000 plus IVA.')
p('.faq[1][1]',
  'No. El precio es la cifra neta del promotor, y su lista de precios indica que los precios no incluyen el IVA, el impuesto sobre el valor añadido español. Confirmamos por escrito los impuestos y los gastos de compra.',
  'Non. Le prix est le chiffre net du promoteur, et sa liste de prix indique que les prix s’entendent hors TVA (IVA), la taxe espagnole sur la valeur ajoutée. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Der Preis ist der Nettobetrag des Bauträgers, und seine Preisliste gibt an, dass die Preise die spanische MwSt. (IVA) nicht enthalten. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'Нет. Цена — это сумма нетто застройщика, а в его прайс-листе указано, что цены не включают испанский НДС (IVA). Налоги и расходы на покупку мы подтверждаем письменно.',
  'لا. السعر هو الرقم الصافي للمطوّر، وتذكر قائمة أسعاره أن الأسعار لا تشمل ضريبة القيمة المضافة (IVA) الإسبانية. ونؤكد الضرائب وتكاليف الشراء كتابةً.',
  'Nee. De prijs is het nettobedrag van de ontwikkelaar, en zijn prijslijst vermeldt dat de prijzen de Spaanse btw (IVA) niet omvatten. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Nie. Cena to kwota netto dewelopera, a jego cennik podaje, że ceny nie obejmują hiszpańskiego VAT (IVA). Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Prisen er utbyggerens nettobeløp, og prislisten oppgir at prisene ikke inkluderer den spanske mva (IVA). Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Nej. Priset är exploatörens nettobelopp, och dess prislista anger att priserna inte inkluderar IVA, den spanska skatten på mervärde (spansk moms). Vi bekräftar skatter och köpkostnader skriftligen.')
p('.faq[2][0]',
  '¿Está terminada?', 'Est-il achevé ?', 'Ist es fertiggestellt?', 'Построен ли комплекс?', 'هل هو مكتمل؟', 'Is het opgeleverd?', 'Czy jest ukończone?', 'Er det ferdigstilt?', 'Är det färdigställt?')
p('.faq[2][1]',
  'La lista de disponibilidad indica que la urbanización está terminada, y la ficha informativa de 2024 dice que está lista para entrar con la licencia de obras en vigor. Pedimos la licencia de primera ocupación y el certificado final de obra antes de que reserve.',
  'La liste de disponibilité indique que l’ensemble est achevé, et la fiche d’information de 2024 dit qu’il est prêt à emménager, avec le permis de construire en vigueur. Nous demandons la licence de première occupation et le certificat de fin de travaux avant que vous réserviez.',
  'Die Verfügbarkeitsliste gibt die Anlage als fertiggestellt an, und das Infoblatt von 2024 sagt bezugsfertig, mit vorliegender Baugenehmigung. Wir fordern die Erstbezugsgenehmigung und die Fertigstellungsbescheinigung an, bevor Sie reservieren.',
  'Список доступных объектов указывает, что комплекс построен, а в информационном листе 2024 года сказано, что он готов к заселению и разрешение на строительство действует. Мы запрашиваем лицензию на первое заселение и акт о завершении строительства до того, как вы забронируете.',
  'تذكر قائمة التوفر أن المجمّع مكتمل، وتقول نشرة المعلومات لعام 2024 إنه جاهز للسكن مع رخصة بناء سارية. ونطلب رخصة السكن الأول وشهادة إتمام البناء قبل أن تحجزوا.',
  'De beschikbaarheidslijst geeft het complex als opgeleverd aan, en het infoblad van 2024 zegt sleutelklaar, met een geldige bouwvergunning. We vragen de eerste-bewoningsvergunning en het opleveringscertificaat op voordat u reserveert.',
  'Lista dostępności podaje, że osiedle jest ukończone, a karta informacyjna z 2024 r. mówi, że jest gotowe do zamieszkania, a pozwolenie na budowę jest w mocy. Przed rezerwacją prosimy o licencję pierwszego zamieszkania i zaświadczenie o zakończeniu budowy.',
  'Tilgjengelighetslisten oppgir at anlegget er ferdigstilt, og informasjonsarket fra 2024 sier innflyttingsklart, med byggetillatelsen på plass. Vi ber om førstegangsbruksbevillingen og ferdigattesten før reservasjon.',
  'Tillgänglighetslistan anger att området är färdigställt, och informationsbladet från 2024 säger nyckelfärdigt, med bygglovet på plats. Vi begär bruksgodkännandet och slutbeviset innan ni reserverar.')
p('.faq[3][0]',
  '¿Por qué una lista anterior la mostraba como reservada?', 'Pourquoi une liste antérieure le montrait-elle comme réservé ?', 'Warum wies eine frühere Liste sie als reserviert aus?',
  'Почему в более раннем списке она значилась как зарезервированная?', 'لماذا أظهرته قائمة سابقة محجوزاً؟', 'Waarom toonde een eerdere lijst haar als gereserveerd?',
  'Dlaczego wcześniejsza lista pokazywała je jako zarezerwowane?', 'Hvorfor viste en tidligere liste den som reservert?', 'Varför visade en tidigare lista den som reserverad?')
p('.faq[3][1]',
  'La lista de precios del promotor del 17 de julio de 2025 marca AL4-1924 como reservada, y la lista de disponibilidad del 29 de octubre de 2026 la anuncia como disponible. Usamos la lista posterior y confirmamos con el promotor que la vivienda está libre antes de cualquier visita.',
  'La liste de prix du promoteur du 17 juillet 2025 marque AL4-1924 comme réservé, et la liste de disponibilité du 29 octobre 2026 l’annonce comme disponible. Nous utilisons la liste postérieure et confirmons avec le promoteur que le logement est libre avant toute visite.',
  'Die Preisliste des Bauträgers vom 17. Juli 2025 kennzeichnet AL4-1924 als reserviert, und die Verfügbarkeitsliste vom 29. Oktober 2026 führt sie als verfügbar. Wir verwenden die spätere Liste und bestätigen beim Bauträger, dass die Wohnung frei ist, bevor eine Besichtigung stattfindet.',
  'В прайс-листе застройщика от 17 июля 2025 года AL4-1924 помечена как зарезервированная, а в списке доступных объектов от 29 октября 2026 года она числится доступной. Мы используем более поздний список и подтверждаем у застройщика, что квартира свободна, до любого просмотра.',
  'تضع قائمة أسعار المطوّر بتاريخ 17 يوليو 2025 علامة «محجوز» على AL4-1924، وتدرجه قائمة التوفر بتاريخ 29 أكتوبر 2026 متاحاً. ونعتمد القائمة الأحدث ونتأكد من المطوّر أن المسكن شاغر قبل أي معاينة.',
  'De prijslijst van de ontwikkelaar van 17 juli 2025 markeert AL4-1924 als gereserveerd, en de beschikbaarheidslijst van 29 oktober 2026 vermeldt haar als beschikbaar. We gebruiken de latere lijst en bevestigen bij de ontwikkelaar dat de woning vrij is vóór elke bezichtiging.',
  'Cennik dewelopera z 17 lipca 2025 r. oznacza AL4-1924 jako zarezerwowane, a lista dostępności z 29 października 2026 r. wymienia je jako dostępne. Przyjmujemy późniejszą listę i przed każdą wizytą potwierdzamy u dewelopera, że mieszkanie jest wolne.',
  'Utbyggerens prisliste fra 17. juli 2025 markerer AL4-1924 som reservert, og tilgjengelighetslisten fra 29. oktober 2026 oppfører den som tilgjengelig. Vi bruker den senere listen og bekrefter med utbyggeren at boligen er ledig før enhver visning.',
  'Exploatörens prislista från den 17 juli 2025 markerar AL4-1924 som reserverad, och tillgänglighetslistan från den 29 oktober 2026 listar den som tillgänglig. Vi använder den senare listan och bekräftar med exploatören att bostaden är ledig före varje visning.')
p('.faq[4][1]',
  'La ficha informativa dice que se incluyen una plaza de garaje y un trastero, y la lista de precios de 2025 nombra la plaza Ext-5 y el trastero 15 para esta vivienda. Confirmamos qué cubren los €615000.',
  'La fiche d’information dit qu’une place de parking et une cave sont incluses, et la liste de prix de 2025 nomme la place Ext-5 et la cave 15 pour ce logement. Nous confirmons ce que couvrent les €615000.',
  'Das Infoblatt nennt einen Stellplatz und einen Abstellraum als enthalten, und die Preisliste von 2025 benennt für diese Wohnung den Stellplatz Ext-5 und den Abstellraum 15. Wir bestätigen, was die €615000 abdecken.',
  'В информационном листе сказано, что включены одно место в гараже и одна кладовая, а в прайс-листе 2025 года для этой квартиры названы место Ext-5 и кладовая 15. Мы подтверждаем, что покрывают €615000.',
  'تقول نشرة المعلومات إن موقف سيارة وغرفة تخزين مشمولان، وتذكر قائمة أسعار 2025 الموقف Ext-5 وغرفة التخزين 15 لهذا المسكن. ونؤكد ما يغطيه مبلغ €615000.',
  'Het infoblad zegt dat een parkeerplaats en een berging zijn inbegrepen, en de prijslijst van 2025 noemt voor deze woning plaats Ext-5 en berging 15. We bevestigen wat de €615000 omvat.',
  'Karta informacyjna mówi, że w cenie jest jedno miejsce postojowe i jedna komórka lokatorska, a cennik z 2025 r. wskazuje dla tego mieszkania miejsce Ext-5 i komórkę 15. Potwierdzamy, co obejmuje €615000.',
  'Informasjonsarket sier at en parkeringsplass og en bod er inkludert, og prislisten fra 2025 oppgir plass Ext-5 og bod 15 for denne boligen. Vi bekrefter hva €615000 dekker.',
  'Informationsbladet säger att en parkeringsplats och ett förråd ingår, och prislistan från 2025 anger plats Ext-5 och förråd 15 för den här bostaden. Vi bekräftar vad €615000 täcker.')

# 117-119 seo
p('.seo.title',
  'Alcazaba Lagoon IV - Apartamento terminado en Casares', 'Alcazaba Lagoon IV - Appartement achevé à Casares',
  'Alcazaba Lagoon IV - Fertige Wohnung in Casares', 'Alcazaba Lagoon IV - готовая квартира в Касаресе',
  'Alcazaba Lagoon IV - شقة جاهزة في كاساريس', 'Alcazaba Lagoon IV - Opgeleverd appartement in Casares',
  'Alcazaba Lagoon IV - Ukończone mieszkanie w Casares', 'Alcazaba Lagoon IV - Ferdigstilt leilighet i Casares',
  'Alcazaba Lagoon IV - Färdigställd lägenhet i Casares')
p('.seo.h1',
  'Alcazaba Lagoon IV: apartamento terminado de dos dormitorios con solárium en Casares', 'Alcazaba Lagoon IV : appartement achevé de deux chambres avec solarium à Casares',
  'Alcazaba Lagoon IV: fertiggestellte Wohnung mit zwei Schlafzimmern und Solarium in Casares', 'Alcazaba Lagoon IV: готовая квартира с двумя спальнями и солярием в Касаресе',
  'Alcazaba Lagoon IV: شقة جاهزة بغرفتي نوم وسولاريوم في كاساريس', 'Alcazaba Lagoon IV: opgeleverd appartement met twee slaapkamers en solarium in Casares',
  'Alcazaba Lagoon IV: ukończone mieszkanie z dwiema sypialniami i solarium w Casares', 'Alcazaba Lagoon IV: ferdigstilt leilighet med to soverom og solterrasse i Casares',
  'Alcazaba Lagoon IV: färdigställd lägenhet med två sovrum och solterrass i Casares')
p('.seo.h1Context',
  'Apartamento terminado de dos dormitorios con solárium en Casares', 'Appartement achevé de deux chambres avec solarium à Casares',
  'Fertiggestellte Wohnung mit zwei Schlafzimmern und Solarium in Casares', 'Готовая квартира с двумя спальнями и солярием в Касаресе',
  'شقة جاهزة بغرفتي نوم وسولاريوم في كاساريس', 'Opgeleverd appartement met twee slaapkamers en solarium in Casares',
  'Ukończone mieszkanie z dwiema sypialniami i solarium w Casares', 'Ferdigstilt leilighet med to soverom og solterrasse i Casares',
  'Färdigställd lägenhet med två sovrum och solterrass i Casares')

# ---- the one drive time the translation memory does not hold yet ------------------------------
p('.location.distances[4][1]',
  'Aprox. 48 minutos', 'Env. 48 minutes', 'Ca. 48 Minuten', 'Около 48 минут', 'حوالي 48 دقيقة',
  'Ca. 48 minuten', 'Ok. 48 minut', 'Ca. 48 minutter', 'Ca 48 minuter')

# ---- finish ---------------------------------------------------------------------------------
missing = [pth for pth in BY_PATH if pth not in USED]
if missing:
    for pth in missing:
        print('NOT COVERED', pth, '|', BY_PATH[pth][:90])
json.dump(T, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries,', len(missing), 'paths not covered')
