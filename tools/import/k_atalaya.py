# -*- coding: utf-8 -*-
"""Atalaya Pool Villas: the 179 strings the translation memory did not have.

Floorplan and caption strings are built from one template per language; the prose is
written by hand. Money, areas and metres are written as tokens and expanded per language
so the separators are the ones the site already uses:  {E1530000}  {N46.31}  {U}  {M}  {KM}
and {DIM10x4}.  Run:  python3 tools/import/k_atalaya.py <scratch dir>
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/import/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {'es': 'm²', 'fr': 'm²', 'de': 'm²', 'ru': 'м²', 'ar': 'م²', 'nl': 'm²', 'pl': 'm²', 'no': 'm²', 'sv': 'm²'}
METRE = {'ru': 'м', 'ar': 'م'}
KM = {'ru': 'км', 'ar': 'كم'}
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    text = re.sub(r'\{DIM(\d+)x(\d+)\}',
                  lambda m: f"{m.group(1)} {'×' if l in ('ru', 'ar') else 'x'} {m.group(2)} {METRE.get(l, 'm')}", text)
    return (text.replace('{U}', UNIT[l]).replace('{M}', METRE.get(l, 'm')).replace('{KM}', KM.get(l, 'km')))


def a(i, hint, *tr):
    en = todo[i]
    assert en.startswith(hint), (i, hint, en[:40])
    assert len(tr) == 9, (i, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---------------------------------------------------------------- templates
LEVEL = {   # ground, first, solarium, basement
    'es': ('planta baja', 'primera planta', 'solárium', 'sótano'),
    'fr': ('rez-de-chaussée', 'premier étage', 'solarium', 'sous-sol'),
    'de': ('Erdgeschoss', 'erstes Obergeschoss', 'Solarium', 'Untergeschoss'),
    'ru': ('первый этаж', 'второй этаж', 'солярий', 'цокольный этаж'),
    'ar': ('الطابق الأرضي', 'الطابق الأول', 'السولاريوم', 'الطابق السفلي'),
    'nl': ('begane grond', 'eerste verdieping', 'solarium', 'kelder'),
    'pl': ('parter', 'pierwsze piętro', 'solarium', 'piwnica'),
    'no': ('første etasje', 'andre etasje', 'solterrasse', 'kjeller'),
    'sv': ('bottenvåning', 'första våningen', 'solterrass', 'källare'),
}
KEYS = ('ground floor', 'first floor', 'solarium', 'basement')
PLAN = {    # alt, caption: format with villa number and level
    'es': ('Plano de la Villa {v}, {lv}', 'Villa {v}, {lv}', 'Plano de la parcela de la Villa {v}', 'Villa {v}, plano de la parcela'),
    'fr': ('Plan de la Villa {v}, {lv}', 'Villa {v}, {lv}', 'Plan de la parcelle de la Villa {v}', 'Villa {v}, plan de la parcelle'),
    'de': ('Grundriss Villa {v}, {lv}', 'Villa {v}, {lv}', 'Grundstücksplan Villa {v}', 'Villa {v}, Grundstücksplan'),
    'ru': ('Планировка Villa {v}, {lv}', 'Villa {v}, {lv}', 'План участка Villa {v}', 'Villa {v}, план участка'),
    'ar': ('مخطط Villa {v}، {lv}', 'Villa {v}، {lv}', 'مخطط قطعة أرض Villa {v}', 'Villa {v}، مخطط قطعة الأرض'),
    'nl': ('Plattegrond van Villa {v}, {lv}', 'Villa {v}, {lv}', 'Plattegrond van het perceel van Villa {v}', 'Villa {v}, plattegrond van het perceel'),
    'pl': ('Rzut Willi {v}, {lv}', 'Willa {v}, {lv}', 'Plan działki Willi {v}', 'Willa {v}, plan działki'),
    'no': ('Plantegning Villa {v}, {lv}', 'Villa {v}, {lv}', 'Tomteplan for Villa {v}', 'Villa {v}, tomteplan'),
    'sv': ('Planritning Villa {v}, {lv}', 'Villa {v}, {lv}', 'Tomtplan för Villa {v}', 'Villa {v}, tomtplan'),
}
for en in todo:
    m = re.fullmatch(r'Floorplan of Villa (\d\d), (ground floor|first floor|solarium|basement)', en)
    c = re.fullmatch(r'Villa (\d\d), (ground floor|first floor|solarium|basement)', en)
    p1 = re.fullmatch(r'Plot plan of Villa (\d\d)', en)
    p2 = re.fullmatch(r'Villa (\d\d), plot plan', en)
    if m:
        T[en] = {l: PLAN[l][0].format(v=m.group(1), lv=LEVEL[l][KEYS.index(m.group(2))]) for l in LOCS}
    elif c:
        T[en] = {l: PLAN[l][1].format(v=c.group(1), lv=LEVEL[l][KEYS.index(c.group(2))]) for l in LOCS}
    elif p1:
        T[en] = {l: PLAN[l][2].format(v=p1.group(1)) for l in LOCS}
    elif p2:
        T[en] = {l: PLAN[l][3].format(v=p2.group(1)) for l in LOCS}

# unit sizes: "<built> sqm built / <plot> sqm plot", in the pattern each language already uses
SIZE = {'es': '{b} m² construidos / {p} m² de parcela', 'fr': '{b} m² construits / {p} m² de parcelle',
        'de': '{b} m² bebaut / {p} m² Grundstück', 'ru': '{b} м² застройки / {p} м² участок',
        'ar': '{b} م² مبنية / {p} م² أرض', 'nl': '{b} m² bebouwd / {p} m² perceel',
        'pl': '{b} m² zabudowy / {p} m² działki', 'no': '{b} m² bygget / {p} m² tomt',
        'sv': '{b} m² byggyta / {p} m² tomt'}
for en in todo:
    m = re.fullmatch(r'(\d+) sqm built / (\d+) sqm plot', en)
    if m:
        T[en] = {l: SIZE[l].format(b=m.group(1), p=m.group(2)) for l in LOCS}

# ---------------------------------------------------------------- names
same = lambda *k: tuple(k)
a(0, 'Atalaya Pool Villas', *(['Atalaya Pool Villas'] * 9))
a(1, 'Atalaya Pool<br>', *(['Atalaya Pool<br><em>Villas</em>'] * 9))

# ---------------------------------------------------------------- card, meta
a(2, 'Seven detached villas in Atalaya, Estepona, each with three',
  "Siete villas independientes en Atalaya, Estepona, de tres o cuatro dormitorios, con piscina infinity privada, jardín y solárium en la azotea. Cinco están disponibles, desde {E1530000}.",
  "Sept villas individuelles à Atalaya, Estepona, de trois ou quatre chambres, avec piscine à débordement privée, jardin et solarium sur le toit. Cinq sont disponibles, à partir de {E1530000}.",
  "Sieben freistehende Villen in Atalaya, Estepona, mit drei oder vier Schlafzimmern, privatem Infinity-Pool, Garten und Dach-Solarium. Fünf sind derzeit verfügbar, ab {E1530000}.",
  "Семь отдельно стоящих вилл в Аталайе, Эстепона, с тремя или четырьмя спальнями, собственным бассейном-инфинити, садом и солярием на крыше. Сейчас доступны пять, от {E1530000}.",
  "سبع فلل مستقلة في أتالايا بإستيبونا، من ثلاث أو أربع غرف نوم، لكل منها مسبح لا نهائي خاص وحديقة وسولاريوم على السطح. خمس منها متاحة حاليًا، ابتداءً من {E1530000}.",
  "Zeven vrijstaande villa's in Atalaya, Estepona, met drie of vier slaapkamers, een eigen infinity pool, een tuin en een solarium op het dak. Vijf zijn momenteel beschikbaar, vanaf {E1530000}.",
  "Siedem wolnostojących willi w Atalayi, Estepona, z trzema lub czterema sypialniami, prywatnym basenem infinity, ogrodem i solarium na dachu. Pięć jest obecnie dostępnych, od {E1530000}.",
  "Sju frittliggende villaer i Atalaya, Estepona, med tre eller fire soverom, eget infinitybasseng, hage og solterrasse på taket. Fem er for øyeblikket tilgjengelige, fra {E1530000}.",
  "Sju fristående villor i Atalaya, Estepona, med tre eller fyra sovrum, egen infinitypool, trädgård och solterrass på taket. Fem är just nu tillgängliga, från {E1530000}.")
a(3, 'Detached 3-4 bedroom villas in Atalaya, Estepona, with a private infinity pool, garden and rooftop solarium. Five',
  "Villas independientes de 3-4 dormitorios en Atalaya, Estepona, con piscina infinity privada, jardín y solárium en la azotea. Cinco disponibles desde {E1530000}, entrega T4 2027 / T1 2028.",
  "Villas individuelles de 3-4 chambres à Atalaya, Estepona, avec piscine à débordement privée, jardin et solarium sur le toit. Cinq disponibles à partir de {E1530000}, livraison T4 2027 / T1 2028.",
  "Freistehende Villen mit 3-4 Schlafzimmern in Atalaya, Estepona, mit privatem Infinity-Pool, Garten und Dach-Solarium. Fünf verfügbar ab {E1530000}, Übergabe Q4 2027 / Q1 2028.",
  "Отдельно стоящие виллы с 3-4 спальнями в Аталайе, Эстепона, с собственным бассейном-инфинити, садом и солярием на крыше. Пять доступны от {E1530000}, сдача 4 кв. 2027 / 1 кв. 2028.",
  "فلل مستقلة من 3 إلى 4 غرف نوم في أتالايا بإستيبونا، بمسبح لا نهائي خاص وحديقة وسولاريوم على السطح. خمس فلل متاحة ابتداءً من {E1530000}، والتسليم الربع الرابع 2027 / الربع الأول 2028.",
  "Vrijstaande villa's met 3-4 slaapkamers in Atalaya, Estepona, met eigen infinity pool, tuin en solarium op het dak. Vijf beschikbaar vanaf {E1530000}, oplevering K4 2027 / K1 2028.",
  "Wolnostojące wille z 3-4 sypialniami w Atalayi, Estepona, z prywatnym basenem infinity, ogrodem i solarium na dachu. Pięć dostępnych od {E1530000}, odbiór IV kw. 2027 / I kw. 2028.",
  "Frittliggende villaer med 3-4 soverom i Atalaya, Estepona, med eget infinitybasseng, hage og solterrasse på taket. Fem tilgjengelige fra {E1530000}, overlevering K4 2027 / K1 2028.",
  "Fristående villor med 3-4 sovrum i Atalaya, Estepona, med egen infinitypool, trädgård och solterrass på taket. Fem tillgängliga från {E1530000}, leverans K4 2027 / K1 2028.")
a(4, 'Detached 3-4 bedroom villas in Atalaya, Estepona, with a private infinity pool. From',
  "Villas independientes de 3-4 dormitorios en Atalaya, Estepona, con piscina infinity privada. Desde {E1530000}.",
  "Villas individuelles de 3-4 chambres à Atalaya, Estepona, avec piscine à débordement privée. À partir de {E1530000}.",
  "Freistehende Villen mit 3-4 Schlafzimmern in Atalaya, Estepona, mit privatem Infinity-Pool. Ab {E1530000}.",
  "Отдельно стоящие виллы с 3-4 спальнями в Аталайе, Эстепона, с собственным бассейном-инфинити. От {E1530000}.",
  "فلل مستقلة من 3 إلى 4 غرف نوم في أتالايا بإستيبونا، بمسبح لا نهائي خاص. ابتداءً من {E1530000}.",
  "Vrijstaande villa's met 3-4 slaapkamers in Atalaya, Estepona, met eigen infinity pool. Vanaf {E1530000}.",
  "Wolnostojące wille z 3-4 sypialniami w Atalayi, Estepona, z prywatnym basenem infinity. Od {E1530000}.",
  "Frittliggende villaer med 3-4 soverom i Atalaya, Estepona, med eget infinitybasseng. Fra {E1530000}.",
  "Fristående villor med 3-4 sovrum i Atalaya, Estepona, med egen infinitypool. Från {E1530000}.")
a(5, 'Q4 2027 / Q1 2028', "T4 2027 / T1 2028", "T4 2027 / T1 2028", "Q4 2027 / Q1 2028", "4 кв. 2027 / 1 кв. 2028",
  "الربع الرابع 2027 / الربع الأول 2028", "K4 2027 / K1 2028", "IV kw. 2027 / I kw. 2028", "K4 2027 / K1 2028", "K4 2027 / K1 2028")
a(6, 'Atalaya', 'Atalaya', 'Atalaya', 'Atalaya', 'Аталайя', 'أتالايا', 'Atalaya', 'Atalaya', 'Atalaya', 'Atalaya')
a(7, 'Seven detached villas in Atalaya, five currently available',
  "Siete villas independientes en Atalaya, cinco disponibles ahora, cada una con piscina infinity privada, jardín y solárium en la azotea.",
  "Sept villas individuelles à Atalaya, cinq actuellement disponibles, chacune avec piscine à débordement privée, jardin et solarium sur le toit.",
  "Sieben freistehende Villen in Atalaya, fünf davon derzeit verfügbar, jeweils mit privatem Infinity-Pool, Garten und Dach-Solarium.",
  "Семь отдельно стоящих вилл в Аталайе, пять из них сейчас доступны; у каждой свой бассейн-инфинити, сад и солярий на крыше.",
  "سبع فلل مستقلة في أتالايا، خمس منها متاحة حاليًا، ولكل منها مسبح لا نهائي خاص وحديقة وسولاريوم على السطح.",
  "Zeven vrijstaande villa's in Atalaya, waarvan er vijf beschikbaar zijn, elk met een eigen infinity pool, tuin en solarium op het dak.",
  "Siedem wolnostojących willi w Atalayi, z których pięć jest obecnie dostępnych; każda ma prywatny basen infinity, ogród i solarium na dachu.",
  "Sju frittliggende villaer i Atalaya, fem er tilgjengelige nå, hver med eget infinitybasseng, hage og solterrasse på taket.",
  "Sju fristående villor i Atalaya, fem är just nu tillgängliga, var och en med egen infinitypool, trädgård och solterrass på taket.")

# ---------------------------------------------------------------- image alt text and captions
a(8, 'Detached villa with infinity pool and garden in Atalaya',
  "Villa independiente con piscina infinity y jardín en Atalaya, Estepona", "Villa individuelle avec piscine à débordement et jardin à Atalaya, Estepona",
  "Freistehende Villa mit Infinity-Pool und Garten in Atalaya, Estepona", "Отдельно стоящая вилла с бассейном-инфинити и садом в Аталайе, Эстепона",
  "فيلا مستقلة بمسبح لا نهائي وحديقة في أتالايا بإستيبونا", "Vrijstaande villa met infinity pool en tuin in Atalaya, Estepona",
  "Wolnostojąca willa z basenem infinity i ogrodem w Atalayi, Estepona", "Frittliggende villa med infinitybasseng og hage i Atalaya, Estepona",
  "Fristående villa med infinitypool och trädgård i Atalaya, Estepona")
a(9, 'Villa facade with covered porch',
  "Fachada de la villa con porche cubierto y piscina infinity", "Façade de la villa avec porche couvert et piscine à débordement",
  "Villenfassade mit überdachtem Vorbau und Infinity-Pool", "Фасад виллы с крытым портиком и бассейном-инфинити",
  "واجهة الفيلا مع رواق مغطى ومسبح لا نهائي", "Gevel van de villa met overdekte veranda en infinity pool",
  "Elewacja willi z zadaszonym gankiem i basenem infinity", "Villaens fasade med overbygd veranda og infinitybasseng",
  "Villans fasad med övertäckt veranda och infinitypool")
a(10, 'Rooftop solarium with lounge, dining table and hot tub',
  "Solárium en la azotea con zona de estar, mesa de comedor y jacuzzi", "Solarium sur le toit avec salon, table à manger et spa",
  "Dach-Solarium mit Lounge, Esstisch und Whirlpool", "Солярий на крыше с зоной отдыха, обеденным столом и джакузи",
  "سولاريوم على السطح مع منطقة جلوس وطاولة طعام وجاكوزي", "Solarium op het dak met loungehoek, eettafel en bubbelbad",
  "Solarium na dachu ze strefą wypoczynku, stołem jadalnianym i jacuzzi", "Solterrasse på taket med loungeområde, spisebord og boblebad",
  "Solterrass på taket med loungeyta, matbord och bubbelpool")
a(11, 'Villa and pool terrace at dusk',
  "La villa y la terraza de la piscina al anochecer", "La villa et la terrasse de la piscine au crépuscule",
  "Villa und Poolterrasse in der Abenddämmerung", "Вилла и терраса у бассейна в сумерках",
  "الفيلا وتراس المسبح عند الغسق", "De villa en het zwembadterras in de schemering",
  "Willa i taras przy basenie o zmierzchu", "Villaen og bassengterrassen i skumringen",
  "Villan och poolterrassen i skymningen")
a(12, 'Renders of the pool terraces',
  "Recreaciones de las terrazas de la piscina, el solárium de la azotea y los interiores, dos vistas aéreas y los planos de todas las plantas de las cinco villas disponibles, con un plano de la parcela de cada una.",
  "Images de synthèse des terrasses de piscine, du solarium sur le toit et des intérieurs, deux vues aériennes et les plans de tous les niveaux des cinq villas disponibles, avec un plan de la parcelle pour chacune.",
  "Visualisierungen der Poolterrassen, des Dach-Solariums und der Innenräume, zwei Luftaufnahmen sowie die Grundrisse aller Ebenen der fünf verfügbaren Villen, jeweils mit einem Grundstücksplan.",
  "Визуализации террас у бассейнов, солярия на крыше и интерьеров, два вида с воздуха и планировки всех уровней пяти доступных вилл, с планом участка для каждой.",
  "تصاميم ثلاثية الأبعاد لتراسات المسابح والسولاريوم على السطح والمساحات الداخلية، ومنظران جويان، ومخططات جميع طوابق الفلل الخمس المتاحة، مع مخطط قطعة الأرض لكل فيلا.",
  "Renders van de zwembadterrassen, het solarium op het dak en de interieurs, twee luchtopnamen en de plattegronden van alle verdiepingen van de vijf beschikbare villa's, elk met een plattegrond van het perceel.",
  "Wizualizacje tarasów przy basenach, solarium na dachu i wnętrz, dwa widoki z lotu ptaka oraz rzuty wszystkich kondygnacji pięciu dostępnych willi, każdy z planem działki.",
  "Visualiseringer av bassengterrassene, solterrassen på taket og interiørene, to flyfoto og plantegninger av alle etasjer i de fem tilgjengelige villaene, hver med en tomteplan.",
  "Visualiseringar av poolterrasserna, solterrassen på taket och interiörerna, två flygvyer och planritningar över alla våningar i de fem tillgängliga villorna, var och en med en tomtplan.")
a(13, 'Furniture, hot tubs and landscaping',
  "El mobiliario, los jacuzzis y el paisajismo que muestran las recreaciones son ilustrativos y no contractuales; las estancias amuebladas muestran un paquete de mobiliario opcional. Las imágenes aéreas muestran las villas insertadas en una fotografía del terreno. Los planos son los de la promotora y las superficies que indican son aproximadas.",
  "Le mobilier, les spas et l'aménagement paysager des images de synthèse sont illustratifs et non contractuels ; les pièces meublées montrent un pack de mobilier en option. Les vues aériennes montrent les villas insérées dans une photographie du terrain. Les plans sont ceux du promoteur et les surfaces qui y figurent sont approximatives.",
  "Möbel, Whirlpools und Landschaftsgestaltung in den Visualisierungen sind illustrativ und nicht vertraglich bindend; die möblierten Räume zeigen ein optionales Möblierungspaket. Die Luftaufnahmen zeigen die Villen in eine Fotografie des Geländes einmontiert. Die Grundrisse stammen vom Bauträger, und die darauf angegebenen Flächen sind ungefähr.",
  "Мебель, джакузи и озеленение на визуализациях носят иллюстративный характер и не являются договорными; в обставленных комнатах показан дополнительный пакет мебели. На снимках с воздуха виллы вмонтированы в фотографию участка. Планировки предоставлены застройщиком, а указанные на них площади приблизительны.",
  "الأثاث والجاكوزي وتنسيق الحدائق الظاهرة في التصاميم ثلاثية الأبعاد توضيحية وغير تعاقدية؛ وتُظهر الغرف المفروشة حزمة أثاث اختيارية. وتُظهر الصور الجوية الفلل مدمجة في صورة فوتوغرافية للموقع. المخططات من إعداد المطور، والمساحات المبينة عليها تقريبية.",
  "Meubilair, bubbelbaden en landschapsinrichting op de renders zijn illustratief en niet contractueel; de gemeubileerde ruimtes tonen een optioneel meubelpakket. De luchtopnamen tonen de villa's in een foto van het terrein geplaatst. De plattegronden zijn die van de ontwikkelaar en de daarop vermelde oppervlaktes zijn bij benadering.",
  "Meble, jacuzzi i zagospodarowanie terenu widoczne na wizualizacjach mają charakter poglądowy i nie są wiążące umownie; umeblowane pomieszczenia pokazują opcjonalny pakiet wyposażenia. Zdjęcia z lotu ptaka przedstawiają wille wmontowane w fotografię terenu. Rzuty pochodzą od dewelopera, a podane na nich powierzchnie są przybliżone.",
  "Møbler, boblebad og landskapsutforming på visualiseringene er illustrative og ikke avtalefestet; de møblerte rommene viser en valgfri møbelpakke. Flyfotoene viser villaene montert inn i et fotografi av området. Plantegningene er utviklerens, og arealene på dem er omtrentlige.",
  "Möbler, bubbelpooler och landskapsutformning i visualiseringarna är illustrativa och inte avtalsenliga; de möblerade rummen visar ett valfritt möbelpaket. Flygbilderna visar villorna inmonterade i ett fotografi av platsen. Planritningarna är byggherrens, och ytorna på dem är ungefärliga.")
a(14, 'The pool terrace in daylight',
  "La terraza de la piscina de día", "La terrasse de la piscine en plein jour", "Die Poolterrasse bei Tageslicht", "Терраса у бассейна днём",
  "تراس المسبح في ضوء النهار", "Het zwembadterras overdag", "Taras przy basenie za dnia", "Bassengterrassen på dagtid", "Poolterrassen i dagsljus")
a(15, 'Facade, porch and pool',
  "Fachada, porche y piscina", "Façade, porche et piscine", "Fassade, Vorbau und Pool", "Фасад, портик и бассейн",
  "الواجهة والرواق والمسبح", "Gevel, veranda en zwembad", "Elewacja, ganek i basen", "Fasade, veranda og basseng", "Fasad, veranda och pool")
a(16, 'Aerial view of the seven villas, with the coast beyond',
  "Vista aérea de las siete villas, con la costa al fondo", "Vue aérienne des sept villas, avec la côte au loin",
  "Luftaufnahme der sieben Villen, dahinter die Küste", "Вид с воздуха на семь вилл, вдали видно побережье",
  "منظر جوي للفلل السبع، والساحل في الخلفية", "Luchtopname van de zeven villa's, met de kust erachter",
  "Widok z lotu ptaka na siedem willi, w tle wybrzeże", "Flyfoto av de sju villaene, med kysten bak", "Flygvy över de sju villorna, med kusten bortom")
a(17, 'The seven villas and the coast',
  "Las siete villas y la costa", "Les sept villas et la côte", "Die sieben Villen und die Küste", "Семь вилл и побережье",
  "الفلل السبع والساحل", "De zeven villa's en de kust", "Siedem willi i wybrzeże", "De sju villaene og kysten", "De sju villorna och kusten")
a(18, 'Aerial view of the seven villas, with the hills behind',
  "Vista aérea de las siete villas, con las colinas detrás", "Vue aérienne des sept villas, avec les collines derrière",
  "Luftaufnahme der sieben Villen, dahinter die Hügel", "Вид с воздуха на семь вилл, позади видны холмы",
  "منظر جوي للفلل السبع، والتلال خلفها", "Luchtopname van de zeven villa's, met de heuvels erachter",
  "Widok z lotu ptaka na siedem willi, w tle wzgórza", "Flyfoto av de sju villaene, med åsene bak", "Flygvy över de sju villorna, med kullarna bakom")
a(19, 'The seven villas and the hills behind',
  "Las siete villas y las colinas detrás", "Les sept villas et les collines derrière", "Die sieben Villen und die Hügel dahinter", "Семь вилл и холмы позади",
  "الفلل السبع والتلال خلفها", "De zeven villa's en de heuvels erachter", "Siedem willi i wzgórza za nimi", "De sju villaene og åsene bak", "De sju villorna och kullarna bakom")
a(20, 'The rooftop solarium',
  "El solárium de la azotea", "Le solarium sur le toit", "Das Dach-Solarium", "Солярий на крыше", "السولاريوم على السطح",
  "Het solarium op het dak", "Solarium na dachu", "Solterrassen på taket", "Solterrassen på taket")
a(21, 'Living and dining room opening onto the pool terrace',
  "Salón comedor que se abre a la terraza de la piscina", "Séjour et salle à manger ouvrant sur la terrasse de la piscine",
  "Wohn- und Essbereich mit Zugang zur Poolterrasse", "Гостиная и столовая с выходом на террасу у бассейна",
  "غرفة المعيشة والطعام تفتح على تراس المسبح", "Woon- en eetkamer die uitkomt op het zwembadterras",
  "Salon z jadalnią otwierający się na taras przy basenie", "Stue og spisestue som åpner seg mot bassengterrassen",
  "Vardagsrum och matplats som öppnar sig mot poolterrassen")
a(22, 'Bedroom with a sliding door to a terrace',
  "Dormitorio con puerta corredera a una terraza", "Chambre avec porte coulissante donnant sur une terrasse",
  "Schlafzimmer mit Schiebetür zu einer Terrasse", "Спальня с раздвижной дверью на террасу",
  "غرفة نوم بباب منزلق يفتح على تراس", "Slaapkamer met een schuifdeur naar een terras",
  "Sypialnia z drzwiami przesuwnymi na taras", "Soverom med skyvedør til en terrasse", "Sovrum med skjutdörr till en terrass")
a(23, 'Bedroom with terrace',
  "Dormitorio con terraza", "Chambre avec terrasse", "Schlafzimmer mit Terrasse", "Спальня с террасой", "غرفة نوم مع تراس",
  "Slaapkamer met terras", "Sypialnia z tarasem", "Soverom med terrasse", "Sovrum med terrass")
a(24, 'Living room with the optional furniture package',
  "Salón con el paquete de mobiliario opcional", "Séjour avec le pack de mobilier en option", "Wohnzimmer mit dem optionalen Möblierungspaket",
  "Гостиная с дополнительным пакетом мебели", "غرفة المعيشة مع حزمة الأثاث الاختيارية", "Woonkamer met het optionele meubelpakket",
  "Salon z opcjonalnym pakietem wyposażenia", "Stue med den valgfrie møbelpakken", "Vardagsrum med det valfria möbelpaketet")
a(25, 'Living room, furnished',
  "Salón amueblado", "Séjour meublé", "Wohnzimmer, möbliert", "Гостиная с мебелью", "غرفة المعيشة مفروشة",
  "Woonkamer, gemeubileerd", "Salon, umeblowany", "Stue, møblert", "Vardagsrum, möblerat")
a(26, 'Dining room and kitchen with the optional furniture package',
  "Comedor y cocina con el paquete de mobiliario opcional", "Salle à manger et cuisine avec le pack de mobilier en option",
  "Esszimmer und Küche mit dem optionalen Möblierungspaket", "Столовая и кухня с дополнительным пакетом мебели",
  "غرفة الطعام والمطبخ مع حزمة الأثاث الاختيارية", "Eetkamer en keuken met het optionele meubelpakket",
  "Jadalnia i kuchnia z opcjonalnym pakietem wyposażenia", "Spisestue og kjøkken med den valgfrie møbelpakken",
  "Matplats och kök med det valfria möbelpaketet")
a(27, 'Dining room, furnished',
  "Comedor amueblado", "Salle à manger meublée", "Esszimmer, möbliert", "Столовая с мебелью", "غرفة الطعام مفروشة",
  "Eetkamer, gemeubileerd", "Jadalnia, umeblowana", "Spisestue, møblert", "Matplats, möblerad")
a(28, 'Main bedroom with the optional furniture package',
  "Dormitorio principal con el paquete de mobiliario opcional", "Chambre principale avec le pack de mobilier en option",
  "Hauptschlafzimmer mit dem optionalen Möblierungspaket", "Главная спальня с дополнительным пакетом мебели",
  "غرفة النوم الرئيسية مع حزمة الأثاث الاختيارية", "Hoofdslaapkamer met het optionele meubelpakket",
  "Główna sypialnia z opcjonalnym pakietem wyposażenia", "Hovedsoverom med den valgfrie møbelpakken", "Huvudsovrum med det valfria möbelpaketet")
a(29, 'Main bedroom, furnished',
  "Dormitorio principal amueblado", "Chambre principale meublée", "Hauptschlafzimmer, möbliert", "Главная спальня с мебелью", "غرفة النوم الرئيسية مفروشة",
  "Hoofdslaapkamer, gemeubileerd", "Główna sypialnia, umeblowana", "Hovedsoverom, møblert", "Huvudsovrum, möblerat")

# ---------------------------------------------------------------- overview, why, architecture
a(74, 'Seven villas, <em>each on its own plot</em>',
  "Siete villas, <em>cada una en su propia parcela</em>", "Sept villas, <em>chacune sur sa propre parcelle</em>",
  "Sieben Villen, <em>jede auf ihrem eigenen Grundstück</em>", "Семь вилл, <em>каждая на собственном участке</em>",
  "سبع فلل، <em>كل واحدة على قطعة أرضها</em>", "Zeven villa's, <em>elk op een eigen perceel</em>",
  "Siedem willi, <em>każda na własnej działce</em>", "Sju villaer, <em>hver på sin egen tomt</em>", "Sju villor, <em>var och en på sin egen tomt</em>")
a(75, 'Atalaya Pool Villas is a development of seven',
  "Atalaya Pool Villas es una promoción de siete villas independientes en Atalaya, Estepona, en el tramo de la Costa del Sol entre Estepona y Marbella. Cada villa se levanta en su propia parcela vallada de entre {N536} y {N795} {U}, con jardín privado, piscina infinity y solárium en la azotea, y cada una tiene una distribución propia.",
  "Atalaya Pool Villas est un programme de sept villas individuelles à Atalaya, Estepona, sur le tronçon de la Costa del Sol compris entre Estepona et Marbella. Chaque villa se dresse sur sa propre parcelle close, de {N536} à {N795} {U}, avec jardin privé, piscine à débordement et solarium sur le toit, et chacune a sa propre distribution.",
  "Atalaya Pool Villas ist ein Projekt mit sieben freistehenden Villen in Atalaya, Estepona, an dem Abschnitt der Costa del Sol zwischen Estepona und Marbella. Jede Villa steht auf einem eigenen, ummauerten Grundstück von {N536} bis {N795} {U} mit privatem Garten, Infinity-Pool und Dach-Solarium, und jede hat einen eigenen Grundriss.",
  "Atalaya Pool Villas — комплекс из семи отдельно стоящих вилл в Аталайе, Эстепона, на участке побережья Коста-дель-Соль между Эстепоной и Марбельей. Каждая вилла стоит на собственном огороженном участке площадью от {N536} до {N795} {U}, с частным садом, бассейном-инфинити и солярием на крыше, и у каждой своя планировка.",
  "Atalaya Pool Villas مشروع من سبع فلل مستقلة في أتالايا بإستيبونا، على امتداد كوستا ديل سول بين إستيبونا وماربيا. تقوم كل فيلا على قطعة أرض مسوّرة خاصة بها تتراوح مساحتها بين {N536} و{N795} {U}، مع حديقة خاصة ومسبح لا نهائي وسولاريوم على السطح، ولكل فيلا تصميمها الخاص.",
  "Atalaya Pool Villas is een project van zeven vrijstaande villa's in Atalaya, Estepona, aan het stuk van de Costa del Sol tussen Estepona en Marbella. Elke villa staat op een eigen ommuurd perceel van {N536} tot {N795} {U}, met een privétuin, een infinity pool en een solarium op het dak, en elke villa heeft een eigen indeling.",
  "Atalaya Pool Villas to inwestycja obejmująca siedem wolnostojących willi w Atalayi, Estepona, na odcinku Costa del Sol między Esteponą a Marbellą. Każda willa stoi na własnej ogrodzonej działce o powierzchni od {N536} do {N795} {U}, z prywatnym ogrodem, basenem infinity i solarium na dachu, a każda ma własny układ pomieszczeń.",
  "Atalaya Pool Villas er et prosjekt med sju frittliggende villaer i Atalaya, Estepona, på strekningen av Costa del Sol mellom Estepona og Marbella. Hver villa står på sin egen inngjerdede tomt på {N536} til {N795} {U}, med privat hage, infinitybasseng og solterrasse på taket, og hver har sin egen planløsning.",
  "Atalaya Pool Villas är ett projekt med sju fristående villor i Atalaya, Estepona, på den del av Costa del Sol som ligger mellan Estepona och Marbella. Varje villa står på sin egen inhägnade tomt på {N536} till {N795} {U}, med privat trädgård, infinitypool och solterrass på taket, och varje villa har sin egen planlösning.")
a(76, 'Every villa is arranged over a basement',
  "Todas las villas se distribuyen en sótano, planta baja, primera planta y un solárium al que se sube por una escalera cubierta. En la planta baja, el salón comedor, con una zona a doble altura, se abre a un porche cubierto y a la piscina, y hay un dormitorio con acceso a la terraza. Cinco de las siete villas están disponibles ahora: cuatro de tres dormitorios y una de cuatro.",
  "Chaque villa est répartie sur un sous-sol, un rez-de-chaussée, un premier étage et un solarium accessible par un escalier couvert. Au rez-de-chaussée, le séjour-salle à manger, qui comporte une partie en double hauteur, s'ouvre sur un porche couvert et sur la piscine, et une chambre donne accès à la terrasse. Cinq des sept villas sont actuellement disponibles : quatre de trois chambres et une de quatre.",
  "Jede Villa verteilt sich auf Untergeschoss, Erdgeschoss, erstes Obergeschoss und ein Solarium, das über eine überdachte Treppe erreicht wird. Im Erdgeschoss öffnet sich der Wohn- und Essbereich, der einen Teil mit doppelter Raumhöhe hat, zu einem überdachten Vorbau und zum Pool, und es gibt ein Schlafzimmer mit Zugang zur Terrasse. Fünf der sieben Villen sind derzeit verfügbar: vier mit drei Schlafzimmern und eine mit vier.",
  "Каждая вилла состоит из цокольного этажа, первого и второго этажей и солярия, на который ведёт крытая лестница. На первом этаже гостиная-столовая, часть которой имеет двойную высоту, открывается на крытый портик и к бассейну; здесь же спальня с выходом на террасу. Сейчас доступны пять из семи вилл: четыре с тремя спальнями и одна с четырьмя.",
  "تتوزع كل فيلا على قبو وطابق أرضي وطابق أول وسولاريوم يُصعد إليه بدرج مغطى. في الطابق الأرضي تنفتح غرفة المعيشة والطعام، التي يتمتع جزء منها بارتفاع مزدوج، على رواق مغطى وعلى المسبح، وتوجد غرفة نوم تطل على التراس. خمس من الفلل السبع متاحة حاليًا: أربع بثلاث غرف نوم وواحدة بأربع.",
  "Elke villa is verdeeld over een kelder, een begane grond, een eerste verdieping en een solarium dat via een overdekte trap wordt bereikt. Op de begane grond komt de woon- en eetkamer, die deels dubbel hoog is, uit op een overdekte veranda en op het zwembad, en is er een slaapkamer met toegang tot het terras. Vijf van de zeven villa's zijn momenteel beschikbaar: vier met drie slaapkamers en één met vier.",
  "Każda willa jest rozplanowana na piwnicę, parter, pierwsze piętro i solarium, na które prowadzą zadaszone schody. Na parterze salon z jadalnią, w części o podwójnej wysokości, otwiera się na zadaszony ganek i basen, a do tarasu prowadzi z niego wejście z sypialni. Pięć z siedmiu willi jest obecnie dostępnych: cztery z trzema sypialniami i jedna z czterema.",
  "Hver villa er fordelt på kjeller, første etasje, andre etasje og en solterrasse som nås via en overbygd trapp. I første etasje åpner stuen og spisestuen, som delvis har dobbel takhøyde, seg mot en overbygd veranda og bassenget, og det er et soverom med tilgang til terrassen. Fem av de sju villaene er tilgjengelige nå: fire med tre soverom og én med fire.",
  "Varje villa är fördelad på källare, bottenvåning, första våningen och en solterrass som nås via en övertäckt trappa. På bottenvåningen öppnar sig vardagsrummet och matplatsen, som delvis har dubbel takhöjd, mot en övertäckt veranda och poolen, och där finns ett sovrum med tillgång till terrassen. Fem av de sju villorna är just nu tillgängliga: fyra med tre sovrum och en med fyra.")
a(77, '7 detached villas',
  "7 villas independientes", "7 villas individuelles", "7 freistehende Villen", "7 отдельно стоящих вилл", "7 فلل مستقلة",
  "7 vrijstaande villa's", "7 wolnostojących willi", "7 frittliggende villaer", "7 fristående villor")
a(78, 'Private infinity pool, garden and rooftop solarium',
  "Piscina infinity privada, jardín y solárium en la azotea", "Piscine à débordement privée, jardin et solarium sur le toit",
  "Privater Infinity-Pool, Garten und Dach-Solarium", "Собственный бассейн-инфинити, сад и солярий на крыше",
  "مسبح لا نهائي خاص وحديقة وسولاريوم على السطح", "Eigen infinity pool, tuin en solarium op het dak",
  "Prywatny basen infinity, ogród i solarium na dachu", "Eget infinitybasseng, hage og solterrasse på taket",
  "Egen infinitypool, trädgård och solterrass på taket")
a(79, 'Detached villas with a private pool, a garden of their own',
  "Villas independientes con piscina privada, jardín propio y solárium en la azotea, en una zona de golf a pocos minutos de Puerto Banús.",
  "Villas individuelles avec piscine privée, jardin et solarium sur le toit, dans un secteur de golf à quelques minutes de Puerto Banús.",
  "Freistehende Villen mit privatem Pool, eigenem Garten und Dach-Solarium in einer Golfgegend, wenige Minuten von Puerto Banús entfernt.",
  "Отдельно стоящие виллы с частным бассейном, собственным садом и солярием на крыше, в районе гольф-полей в нескольких минутах от Пуэрто-Бануса.",
  "فلل مستقلة بمسبح خاص وحديقة خاصة وسولاريوم على السطح، في منطقة غولف على بُعد دقائق من بويرتو بانوس.",
  "Vrijstaande villa's met een eigen zwembad, een eigen tuin en een solarium op het dak, in een golfomgeving op enkele minuten van Puerto Banús.",
  "Wolnostojące wille z prywatnym basenem, własnym ogrodem i solarium na dachu, w okolicy pól golfowych kilka minut od Puerto Banús.",
  "Frittliggende villaer med eget basseng, egen hage og solterrasse på taket, i et golfområde noen få minutter fra Puerto Banús.",
  "Fristående villor med egen pool, egen trädgård och solterrass på taket, i ett golfområde några minuter från Puerto Banús.")
a(80, 'Buyers who want a detached villa with its own pool',
  "Compradores que quieren una villa independiente con piscina y jardín propios, en una parcela suya, y no una vivienda dentro de un conjunto mayor.",
  "Acheteurs qui veulent une villa individuelle avec sa propre piscine et son jardin, sur une parcelle à elle, plutôt qu'un logement au sein d'un ensemble plus vaste.",
  "Käufer, die eine freistehende Villa mit eigenem Pool und Garten auf einem eigenen Grundstück suchen und keine Wohnung in einer größeren Anlage.",
  "Покупатели, которым нужна отдельно стоящая вилла с собственным бассейном и садом на собственном участке, а не дом в более крупном комплексе.",
  "المشترون الذين يريدون فيلا مستقلة بمسبحها وحديقتها على قطعة أرض خاصة بها، لا مسكنًا ضمن مجمع أكبر.",
  "Kopers die een vrijstaande villa met eigen zwembad en tuin op een eigen perceel zoeken, in plaats van een woning in een groter complex.",
  "Kupujący, którzy chcą wolnostojącej willi z własnym basenem i ogrodem na własnej działce, a nie domu w większym kompleksie.",
  "Kjøpere som ønsker en frittliggende villa med eget basseng og egen hage på en egen tomt, i stedet for en bolig i et større anlegg.",
  "Köpare som vill ha en fristående villa med egen pool och trädgård på en egen tomt, snarare än en bostad i ett större område.")
a(81, 'Seven villas, each different from the others',
  "Siete villas, cada una distinta de las demás y con acceso propio, en una zona residencial consolidada y no dentro de un gran resort.",
  "Sept villas, chacune différente des autres et dotée de son propre accès, dans un quartier résidentiel établi plutôt qu'au sein d'un grand resort.",
  "Sieben Villen, jede anders als die anderen und mit eigener Zufahrt, in einem gewachsenen Wohngebiet statt in einer großen Resortanlage.",
  "Семь вилл, каждая не похожа на остальные и имеет собственный въезд, в сложившемся жилом районе, а не внутри крупного курортного комплекса.",
  "سبع فلل، كل واحدة تختلف عن الأخريات ولها مدخلها الخاص، في منطقة سكنية راسخة لا داخل منتجع كبير.",
  "Zeven villa's, elk anders dan de rest en elk met een eigen toegang, in een gevestigde woonwijk in plaats van binnen een groot resort.",
  "Siedem willi, każda inna od pozostałych i z własnym wjazdem, w ugruntowanej dzielnicy mieszkalnej, a nie w dużym kompleksie wypoczynkowym.",
  "Sju villaer, hver forskjellig fra de andre og med egen adkomst, i et etablert boligområde i stedet for inne i et stort resort.",
  "Sju villor, var och en olik de andra och med egen tillfart, i ett etablerat bostadsområde snarare än inne i ett stort resort.")
a(82, 'Atalaya Golf is 600 m away, Puerto Ban',
  "Atalaya Golf queda a {N600} {M}, Puerto Banús y San Pedro de Alcántara están a unos ocho minutos en coche y la playa a {N1.9} {KM} a pie.",
  "Atalaya Golf se trouve à {N600} {M}, Puerto Banús et San Pedro de Alcántara sont à environ huit minutes en voiture et la plage à {N1.9} {KM} à pied.",
  "Atalaya Golf liegt {N600} {M} entfernt, Puerto Banús und San Pedro de Alcántara sind mit dem Auto in etwa acht Minuten erreichbar, der Strand zu Fuß in {N1.9} {KM}.",
  "Atalaya Golf находится в {N600} {M}, до Пуэрто-Бануса и Сан-Педро-де-Алькантара около восьми минут на машине, до пляжа {N1.9} {KM} пешком.",
  "يبعد Atalaya Golf مسافة {N600} {M}، ويبعد بويرتو بانوس وسان بيدرو دي ألكانتارا نحو ثماني دقائق بالسيارة، والشاطئ {N1.9} {KM} سيرًا على الأقدام.",
  "Atalaya Golf ligt op {N600} {M}, Puerto Banús en San Pedro de Alcántara zijn ongeveer acht minuten met de auto en het strand ligt op {N1.9} {KM} lopen.",
  "Atalaya Golf jest oddalone o {N600} {M}, Puerto Banús i San Pedro de Alcántara o około osiem minut samochodem, a plaża o {N1.9} {KM} pieszo.",
  "Atalaya Golf ligger {N600} {M} unna, Puerto Banús og San Pedro de Alcántara er omtrent åtte minutter unna med bil, og stranden er {N1.9} {KM} til fots.",
  "Atalaya Golf ligger {N600} {M} bort, Puerto Banús och San Pedro de Alcántara är ungefär åtta minuter med bil och stranden ligger {N1.9} {KM} till fots.")
a(83, 'Five of the seven villas are currently listed',
  "Cinco de las siete villas figuran ahora como disponibles. Nueva Living vuelve a confirmar con la promotora el precio, el mes de entrega y el aparcamiento antes de cualquier visita.",
  "Cinq des sept villas figurent actuellement comme disponibles. Nueva Living reconfirme auprès du promoteur le prix, le mois de livraison et le stationnement avant toute visite.",
  "Fünf der sieben Villen sind derzeit als verfügbar gelistet. Nueva Living bestätigt Preis, Übergabemonat und Stellplatz vor jeder Besichtigung erneut beim Bauträger.",
  "Сейчас в продаже пять из семи вилл. Nueva Living повторно подтверждает у застройщика цену, месяц сдачи и парковку до любого просмотра.",
  "خمس من الفلل السبع معروضة حاليًا كمتاحة. تعيد Nueva Living تأكيد السعر وشهر التسليم والمواقف مع المطور قبل أي معاينة.",
  "Vijf van de zeven villa's staan momenteel als beschikbaar vermeld. Nueva Living bevestigt prijs, opleveringsmaand en parkeerplaats opnieuw bij de ontwikkelaar vóór elke bezichtiging.",
  "Pięć z siedmiu willi figuruje obecnie jako dostępne. Nueva Living ponownie potwierdza u dewelopera cenę, miesiąc odbioru i miejsca parkingowe przed każdym oglądaniem.",
  "Fem av de sju villaene er for tiden oppført som tilgjengelige. Nueva Living bekrefter pris, overleveringsmåned og parkering på nytt med utvikleren før enhver visning.",
  "Fem av de sju villorna är just nu angivna som tillgängliga. Nueva Living bekräftar pris, leveransmånad och parkering på nytt med byggherren före varje visning.")
a(84, 'Contemporary lines, <em>Mediterranean materials</em>',
  "Líneas contemporáneas, <em>materiales mediterráneos</em>", "Lignes contemporaines, <em>matériaux méditerranéens</em>",
  "Zeitgenössische Linien, <em>mediterrane Materialien</em>", "Современные линии, <em>средиземноморские материалы</em>",
  "خطوط معاصرة، <em>ومواد متوسطية</em>", "Eigentijdse lijnen, <em>mediterrane materialen</em>",
  "Współczesne linie, <em>śródziemnomorskie materiały</em>", "Moderne linjer, <em>middelhavsmaterialer</em>", "Samtida linjer, <em>medelhavsmaterial</em>")
a(85, 'The facades combine white cement render',
  "Las fachadas combinan enfoscado de cemento blanco con paneles de revestimiento y celosías de acabado imitación madera, y unas pérgolas con vigas imitación madera dan sombra a las terrazas. Grandes puertas correderas y ventanas en el salón y los dormitorios aportan luz y ventilación cruzada, y las barandillas de obra y de cristal conservan desde el interior la vista a la piscina y al jardín.",
  "Les façades associent un enduit de ciment blanc à des panneaux de bardage et des claustras à finition aspect bois, et des pergolas à poutres aspect bois ombragent les terrasses. De grandes baies coulissantes et des fenêtres dans le séjour et les chambres apportent la lumière et une ventilation traversante, et les garde-corps en maçonnerie et en verre préservent depuis l'intérieur la vue sur la piscine et le jardin.",
  "Die Fassaden verbinden weißen Zementputz mit Verkleidungspaneelen und Sichtschutzelementen in Holzoptik, und Pergolen mit Balken in Holzoptik beschatten die Terrassen. Große Schiebetüren und Fenster in Wohnzimmer und Schlafzimmern bringen Licht und sorgen für Querlüftung, und Brüstungen aus Mauerwerk und Glas erhalten vom Hausinneren aus den Blick auf Pool und Garten.",
  "Фасады сочетают белую цементную штукатурку с облицовочными панелями и экранами с отделкой под дерево, а террасы затеняют пергол с балками под дерево. Большие раздвижные двери и окна в гостиной и спальнях пропускают свет и обеспечивают сквозное проветривание, а ограждения из кладки и стекла сохраняют из дома вид на бассейн и сад.",
  "تجمع الواجهات بين لياسة الإسمنت الأبيض وألواح كسوة وستائر مشبّكة بتشطيب يحاكي الخشب، وتظلّل البرغولات ذات العوارض المحاكية للخشب التراسات. وتُدخل الأبواب المنزلقة الكبيرة والنوافذ في غرفة المعيشة وغرف النوم الضوء وتؤمّن تهوية متقاطعة، وتحافظ الدرابزينات من البناء والزجاج على الإطلالة على المسبح والحديقة من داخل المنزل.",
  "De gevels combineren witte cementstuc met gevelpanelen en schermen met een houtlook-afwerking, en pergola's met balken in houtlook geven schaduw op de terrassen. Grote schuifpuien en ramen in de woonkamer en de slaapkamers laten licht binnen en zorgen voor kruisventilatie, en balustrades van metselwerk en glas houden het uitzicht op het zwembad en de tuin vanuit het huis intact.",
  "Elewacje łączą biały tynk cementowy z panelami okładzinowymi i ekranami w wykończeniu imitującym drewno, a pergole z belkami imitującymi drewno zacieniają tarasy. Duże drzwi przesuwne i okna w salonie i sypialniach wpuszczają światło i zapewniają przewietrzanie, a balustrady murowane i szklane zachowują widok z wnętrza na basen i ogród.",
  "Fasadene kombinerer hvit sementpuss med kledningspaneler og skjermer i tre-effekt, og pergolaer med bjelker i tre-effekt gir skygge over terrassene. Store skyvedører og vinduer i stuen og soverommene slipper inn lys og gir gjennomlufting, og rekkverk i murverk og glass beholder utsikten mot bassenget og hagen fra innsiden av huset.",
  "Fasaderna kombinerar vit cementputs med fasadpaneler och skärmar i trälook, och pergolor med bjälkar i trälook ger skugga åt terrasserna. Stora skjutdörrar och fönster i vardagsrummet och sovrummen släpper in ljus och ger genomluftning, och räcken av murverk och glas bevarar utsikten mot poolen och trädgården inifrån huset.")
a(86, 'The developer’s own specification',
  "La memoria de calidades de la propia promotora, resumida por partes de la vivienda.",
  "Le descriptif de la qualité du promoteur lui-même, résumé par partie du logement.",
  "Die eigene Bau- und Ausstattungsbeschreibung des Bauträgers, nach Bereichen des Hauses zusammengefasst.",
  "Собственная спецификация застройщика, сгруппированная по частям дома.",
  "مواصفات المطور نفسه، ملخّصة بحسب أجزاء المسكن.",
  "De eigen specificatie van de ontwikkelaar, samengevat per onderdeel van de woning.",
  "Własna specyfikacja dewelopera, podsumowana według części domu.",
  "Utviklerens egen spesifikasjon, oppsummert etter deler av boligen.",
  "Byggherrens egen specifikation, sammanfattad efter bostadens delar.")
a(87, 'Source: the developer’s circular for these villas',
  "Fuente: la circular informativa de la promotora sobre estas villas, de mayo de 2024. La memoria de calidades definitiva es el documento de calidades de la promotora, que pedimos por escrito antes de cualquier reserva. Las imágenes, el mobiliario y el paisajismo de las recreaciones son ilustrativos.",
  "Source : la circulaire d'information du promoteur sur ces villas, datée de mai 2024. Le descriptif définitif est le mémoire de qualité du promoteur, que nous demandons par écrit avant toute réservation. Les images, le mobilier et l'aménagement paysager des images de synthèse sont illustratifs.",
  "Quelle: das Informationsschreiben des Bauträgers zu diesen Villen vom Mai 2024. Maßgeblich für die endgültige Ausstattung ist die Qualitätsbeschreibung des Bauträgers, die wir vor jeder Reservierung schriftlich anfordern. Bilder, Möbel und Landschaftsgestaltung in den Visualisierungen sind illustrativ.",
  "Источник: информационное письмо застройщика по этим виллам от мая 2024 года. Окончательной спецификацией является описание качества и оснащения от застройщика, которое мы запрашиваем в письменном виде до любого бронирования. Изображения, мебель и озеленение на визуализациях носят иллюстративный характер.",
  "المصدر: التعميم الصادر عن المطور بشأن هذه الفلل والمؤرخ في مايو 2024. المواصفات النهائية هي مذكرة الجودة الخاصة بالمطور، ونطلبها كتابةً قبل أي حجز. الصور والأثاث وتنسيق الحدائق في التصاميم ثلاثية الأبعاد توضيحية.",
  "Bron: de informatiebrief van de ontwikkelaar over deze villa's, van mei 2024. De definitieve specificatie is de kwaliteitsomschrijving van de ontwikkelaar, die wij vóór elke reservering schriftelijk opvragen. Beelden, meubilair en landschapsinrichting op de renders zijn illustratief.",
  "Źródło: pismo informacyjne dewelopera dotyczące tych willi z maja 2024 roku. Ostateczną specyfikacją jest opis jakości wykonania dewelopera, o który prosimy na piśmie przed jakąkolwiek rezerwacją. Obrazy, meble i zagospodarowanie terenu na wizualizacjach mają charakter poglądowy.",
  "Kilde: utviklerens informasjonsskriv om disse villaene, datert mai 2024. Den endelige spesifikasjonen er utviklerens kvalitetsbeskrivelse, som vi ber om skriftlig før enhver reservasjon. Bilder, møbler og landskapsutforming på visualiseringene er illustrative.",
  "Källa: byggherrens informationsbrev om dessa villor, daterat maj 2024. Den slutliga specifikationen är byggherrens kvalitetsbeskrivning, som vi begär skriftligt före varje reservation. Bilder, möbler och landskapsutformning i visualiseringarna är illustrativa.")

# ---------------------------------------------------------------- quality specification
a(88, 'Floors and interior',
  "Suelos e interior", "Sols et intérieur", "Böden und Innenausbau", "Полы и интерьер", "الأرضيات والمساحات الداخلية",
  "Vloeren en interieur", "Podłogi i wnętrza", "Gulv og interiør", "Golv och interiör")
a(89, 'Large-format porcelain floors',
  "Suelos de gres porcelánico de gran formato y alicatado cerámico de gran formato en las paredes.",
  "Sols en grès cérame grand format et faïence murale céramique grand format.",
  "Bodenbeläge aus großformatigem Feinsteinzeug und großformatige Keramikfliesen an den Wänden.",
  "Полы из крупноформатного керамогранита и крупноформатная керамическая плитка на стенах.",
  "أرضيات من البورسلين كبير القياس وكسوة جدران بالسيراميك كبير القياس.",
  "Vloeren van groot formaat porseleintegels en wandtegels van groot formaat keramiek.",
  "Podłogi z wielkoformatowego gresu porcelanowego i wielkoformatowa glazura ceramiczna na ścianach.",
  "Gulv i storformat porselensfliser og storformat keramiske veggfliser.",
  "Golv av storformatigt porslinsgolv och storformatigt keramiskt kakel på väggarna.")
a(90, 'Interior doors 2.20 m high.',
  "Puertas interiores de {N2.20} {M} de altura.", "Portes intérieures de {N2.20} {M} de hauteur.", "Innentüren mit {N2.20} {M} Höhe.",
  "Межкомнатные двери высотой {N2.20} {M}.", "أبواب داخلية بارتفاع {N2.20} {M}.", "Binnendeuren van {N2.20} {M} hoog.",
  "Drzwi wewnętrzne o wysokości {N2.20} {M}.", "Innerdører med høyde på {N2.20} {M}.", "Innerdörrar med en höjd på {N2.20} {M}.")
a(91, 'Air conditioning and hot water by aerothermal energy',
  "Climatización y agua caliente mediante aerotermia, con control independiente por estancias.",
  "Climatisation et eau chaude par aérothermie, avec régulation pièce par pièce.",
  "Klimatisierung und Warmwasser über eine Luft-Wasser-Wärmepumpe, mit raumweiser Regelung.",
  "Кондиционирование и горячая вода от аэротермальной системы с раздельным управлением по комнатам.",
  "تكييف الهواء والماء الساخن بالطاقة الحرارية الهوائية، مع تحكم مستقل في كل غرفة.",
  "Airconditioning en warm water via een lucht-waterwarmtepomp, met regeling per ruimte.",
  "Klimatyzacja i ciepła woda z systemu aerotermicznego, ze sterowaniem w każdym pomieszczeniu osobno.",
  "Klimaanlegg og varmtvann fra et luft-vann-varmepumpeanlegg, med styring rom for rom.",
  "Luftkonditionering och varmvatten från en luft-vattenvärmepump, med styrning rum för rum.")
a(92, 'Underfloor heating throughout the house except the basement',
  "Suelo radiante en toda la casa salvo en el sótano, y suelo radiante eléctrico en los baños.",
  "Plancher chauffant dans toute la maison sauf au sous-sol, et plancher chauffant électrique dans les salles de bains.",
  "Fußbodenheizung im ganzen Haus mit Ausnahme des Untergeschosses sowie elektrische Fußbodenheizung in den Bädern.",
  "Тёплый пол во всём доме, кроме цокольного этажа, и электрический тёплый пол в ванных комнатах.",
  "تدفئة أرضية في المنزل كله باستثناء القبو، وتدفئة أرضية كهربائية في الحمامات.",
  "Vloerverwarming in het hele huis behalve in de kelder, en elektrische vloerverwarming in de badkamers.",
  "Ogrzewanie podłogowe w całym domu poza piwnicą oraz elektryczne ogrzewanie podłogowe w łazienkach.",
  "Gulvvarme i hele huset unntatt kjelleren, og elektrisk gulvvarme på badene.",
  "Golvvärme i hela huset utom källaren, och elektrisk golvvärme i badrummen.")
a(93, 'An electrical installation of 11.50 kW.',
  "Instalación eléctrica de {N11.50} kW.", "Installation électrique de {N11.50} kW.", "Elektroinstallation mit {N11.50} kW.",
  "Электроустановка мощностью {N11.50} кВт.", "تركيب كهربائي بقدرة {N11.50} كيلوواط.", "Een elektrische installatie van {N11.50} kW.",
  "Instalacja elektryczna o mocy {N11.50} kW.", "Elektrisk anlegg på {N11.50} kW.", "Elinstallation på {N11.50} kW.")
a(94, 'Kitchen and laundry',
  "Cocina y lavandería", "Cuisine et buanderie", "Küche und Waschküche", "Кухня и прачечная", "المطبخ وغرفة الغسيل",
  "Keuken en wasruimte", "Kuchnia i pralnia", "Kjøkken og vaskerom", "Kök och tvättstuga")
a(95, 'Designer kitchen with Siemens appliances included.',
  "Cocina de diseño con electrodomésticos Siemens incluidos.", "Cuisine design avec électroménager Siemens inclus.",
  "Designerküche mit Siemens-Geräten inklusive.", "Дизайнерская кухня с техникой Siemens в комплекте.",
  "مطبخ بتصميم راقٍ مع أجهزة Siemens مشمولة.", "Designkeuken met Siemens-apparatuur inbegrepen.",
  "Kuchnia projektowana na wymiar ze sprzętem Siemens w cenie.", "Designkjøkken med Siemens-hvitevarer inkludert.",
  "Designkök med Siemens-apparater inkluderade.")
a(96, 'Basement laundry room with washer and dryer included.',
  "Lavandería en el sótano con lavadora y secadora incluidas.", "Buanderie au sous-sol avec lave-linge et sèche-linge inclus.",
  "Waschküche im Untergeschoss mit Waschmaschine und Trockner inklusive.", "Прачечная в цоколе со стиральной машиной и сушилкой в комплекте.",
  "غرفة غسيل في القبو مع غسالة ومجفف مشمولتين.", "Wasruimte in de kelder met wasmachine en droger inbegrepen.",
  "Pralnia w piwnicy z pralką i suszarką w cenie.", "Vaskerom i kjelleren med vaskemaskin og tørketrommel inkludert.",
  "Tvättstuga i källaren med tvättmaskin och torktumlare inkluderade.")
a(97, 'Wall-hung vanity units with recessed LED lighting',
  "Muebles de lavabo suspendidos con iluminación LED empotrada y espejo, retroiluminado y antivaho en el baño principal.",
  "Meubles de salle de bains suspendus avec éclairage LED encastré et miroir, rétroéclairé et antibuée dans la salle de bains principale.",
  "Wandhängende Waschtischunterschränke mit eingelassener LED-Beleuchtung und Spiegel, im Hauptbad hinterleuchtet und beschlagfrei.",
  "Подвесные тумбы под раковину со встроенной светодиодной подсветкой и зеркалом; в главной ванной комнате зеркало с подсветкой и защитой от запотевания.",
  "وحدات مغاسل معلقة على الجدار بإضاءة LED مدمجة ومرآة، وتكون المرآة مضاءة من الخلف ومانعة للبخار في الحمام الرئيسي.",
  "Hangende wastafelmeubels met inbouw-ledverlichting en een spiegel, in de hoofdbadkamer met achtergrondverlichting en antibeslag.",
  "Podwieszane szafki umywalkowe z wpuszczanym oświetleniem LED i lustrem, w głównej łazience podświetlanym i niezaparowującym.",
  "Vegghengte servantskap med innfelt LED-belysning og speil, i hovedbadet med bakbelysning og antidugg.",
  "Väggmonterade tvättställsskåp med infälld LED-belysning och spegel, i huvudbadrummet med bakgrundsbelysning och imfri.")
a(98, 'Wall-hung toilets with concealed cisterns',
  "Inodoros suspendidos con cisterna empotrada. El baño principal tiene ducha y bañera de obra, salvo en las villas 06 y 07, donde solo tiene ducha.",
  "Toilettes suspendues à réservoir encastré. La salle de bains principale a une douche et une baignoire encastrée, sauf dans les villas 06 et 07, où elle n'a qu'une douche.",
  "Wandhängende WCs mit Unterputzspülkasten. Das Hauptbad hat Dusche und eingebaute Badewanne, außer in den Villen 06 und 07, wo es nur eine Dusche gibt.",
  "Подвесные унитазы со скрытыми бачками. В главной ванной комнате есть душ и встроенная ванна, кроме вилл 06 и 07, где только душ.",
  "مراحيض معلقة بخزانات مخفية. يضم الحمام الرئيسي دشًا وحوض استحمام مدمجًا، باستثناء الفيلتين 06 و07 اللتين تضمان دشًا فقط.",
  "Hangende toiletten met inbouwreservoir. De hoofdbadkamer heeft een douche en een ingebouwd bad, behalve in villa 06 en 07, waar alleen een douche is.",
  "Podwieszane toalety z ukrytymi spłuczkami. Główna łazienka ma prysznic i wbudowaną wannę, z wyjątkiem willi 06 i 07, gdzie jest tylko prysznic.",
  "Vegghengte toaletter med skjult sisterne. Hovedbadet har dusj og innebygd badekar, unntatt i villa 06 og 07, der det bare har dusj.",
  "Väggmonterade toaletter med dold cistern. Huvudbadrummet har dusch och inbyggt badkar, utom i villa 06 och 07, där det bara har dusch.")
a(99, 'Windows, doors and security',
  "Ventanas, puertas y seguridad", "Fenêtres, portes et sécurité", "Fenster, Türen und Sicherheit", "Окна, двери и безопасность", "النوافذ والأبواب والأمان",
  "Ramen, deuren en beveiliging", "Okna, drzwi i bezpieczeństwo", "Vinduer, dører og sikkerhet", "Fönster, dörrar och säkerhet")
a(100, 'Large lifting sliding doors in the living room',
  "Grandes puertas correderas elevables en el salón, con persiana motorizada opaca, y persianas motorizadas en el resto de las ventanas y puertas.",
  "Grandes baies coulissantes à levage dans le séjour, avec store enrouleur occultant motorisé, et volets motorisés sur les autres fenêtres et portes.",
  "Große Hebe-Schiebetüren im Wohnzimmer mit motorisiertem Verdunkelungsrollo sowie motorisierte Rollläden an den übrigen Fenstern und Türen.",
  "Большие подъёмно-раздвижные двери в гостиной с электрической затемняющей шторой-рулоном и электрические жалюзи на остальных окнах и дверях.",
  "أبواب منزلقة رافعة كبيرة في غرفة المعيشة مع ستارة معتمة بمحرك، وستائر بمحرك على النوافذ والأبواب الأخرى.",
  "Grote hef-schuifpuien in de woonkamer met een gemotoriseerd verduisterend rolgordijn, en gemotoriseerde rolluiken op de overige ramen en deuren.",
  "Duże drzwi przesuwne podnoszone w salonie z zasłoną zaciemniającą na napędzie elektrycznym oraz rolety elektryczne na pozostałych oknach i drzwiach.",
  "Store løfte-skyvedører i stuen med motorisert mørklegging, og motoriserte persienner på de øvrige vinduene og dørene.",
  "Stora lyft-skjutdörrar i vardagsrummet med motoriserad mörkläggningsrullgardin, och motoriserade rullgardiner på övriga fönster och dörrar.")
a(101, 'A video entry phone, and an alarm',
  "Videoportero e instalación de alarma conectada a una central receptora.",
  "Visiophone et installation d'alarme reliée à un centre de télésurveillance.",
  "Video-Gegensprechanlage und eine Alarmanlage mit Anschluss an eine Überwachungszentrale.",
  "Видеодомофон и охранная сигнализация с подключением к пульту наблюдения.",
  "جهاز اتصال داخلي بالفيديو ونظام إنذار موصول بمركز مراقبة.",
  "Een video-intercom en een alarminstallatie die op een meldkamer is aangesloten.",
  "Wideodomofon i instalacja alarmowa połączona z centrum monitoringu.",
  "Porttelefon med video og et alarmanlegg koblet til en overvåkingssentral.",
  "Porttelefon med video och ett larm anslutet till en larmcentral.")
a(102, 'Garden, pool and solarium',
  "Jardín, piscina y solárium", "Jardin, piscine et solarium", "Garten, Pool und Solarium", "Сад, бассейн и солярий", "الحديقة والمسبح والسولاريوم",
  "Tuin, zwembad en solarium", "Ogród, basen i solarium", "Hage, basseng og solterrasse", "Trädgård, pool och solterrass")
a(103, 'A private garden with natural lawn',
  "Jardín privado con césped natural, plantaciones, iluminación y riego automático.",
  "Jardin privé avec pelouse naturelle, plantations, éclairage et arrosage automatique.",
  "Privater Garten mit Naturrasen, Bepflanzung, Beleuchtung und automatischer Bewässerung.",
  "Частный сад с натуральным газоном, посадками, освещением и автоматическим поливом.",
  "حديقة خاصة بعشب طبيعي ونباتات وإضاءة وري تلقائي.",
  "Een privétuin met natuurlijk gazon, beplanting, verlichting en automatische bewatering.",
  "Prywatny ogród z naturalnym trawnikiem, nasadzeniami, oświetleniem i automatycznym nawadnianiem.",
  "Privat hage med naturlig gress, beplantning, belysning og automatisk vanning.",
  "Privat trädgård med naturlig gräsmatta, planteringar, belysning och automatisk bevattning.")
a(104, 'An infinity pool with interior lighting',
  "Piscina infinity con iluminación interior y preinstalación para climatización: de {DIM10x4} en la villa de cuatro dormitorios y de {DIM8x4} en las demás.",
  "Piscine à débordement avec éclairage intérieur et pré-équipement pour le chauffage : {DIM10x4} sur la villa de quatre chambres et {DIM8x4} sur les autres.",
  "Infinity-Pool mit Innenbeleuchtung und Vorinstallation für eine Beheizung: {DIM10x4} bei der Villa mit vier Schlafzimmern und {DIM8x4} bei den übrigen.",
  "Бассейн-инфинити с подсветкой и подготовкой под подогрев: {DIM10x4} на вилле с четырьмя спальнями и {DIM8x4} на остальных.",
  "مسبح لا نهائي بإضاءة داخلية وتجهيز مسبق للتسخين: {DIM10x4} في الفيلا ذات الأربع غرف نوم و{DIM8x4} في الباقي.",
  "Infinity pool met binnenverlichting en voorbereiding voor verwarming: {DIM10x4} bij de villa met vier slaapkamers en {DIM8x4} bij de overige.",
  "Basen infinity z oświetleniem wewnętrznym i instalacją pod podgrzewanie: {DIM10x4} przy willi z czterema sypialniami i {DIM8x4} przy pozostałych.",
  "Infinitybasseng med innvendig belysning og forberedelse for oppvarming: {DIM10x4} ved villaen med fire soverom og {DIM8x4} ved de andre.",
  "Infinitypool med belysning i poolen och förberedelse för uppvärmning: {DIM10x4} vid villan med fyra sovrum och {DIM8x4} vid de övriga.")
a(105, 'An integrated gas barbecue on the porch.',
  "Barbacoa de gas integrada en el porche.", "Barbecue à gaz intégré sur le porche.", "Integrierter Gasgrill auf dem Vorbau.",
  "Встроенный газовый гриль на портике.", "شواية غاز مدمجة في الرواق.", "Ingebouwde gasbarbecue op de veranda.",
  "Wbudowany grill gazowy na ganku.", "Innebygd gassgrill på verandaen.", "Inbyggd gasolgrill på verandan.")
a(106, 'A solarium reached by a covered staircase',
  "Solárium al que se sube por una escalera cubierta con techo motorizado, con ducha, armario trastero empotrado, tomas de TV y de corriente y preinstalación para un jacuzzi.",
  "Solarium accessible par un escalier couvert à toit motorisé, avec douche, placard de rangement intégré, prises TV et électriques et pré-équipement pour un spa.",
  "Solarium, das über eine überdachte Treppe mit motorisiertem Dach erreicht wird, mit Dusche, Einbauschrank, TV- und Stromanschlüssen und Vorinstallation für einen Whirlpool.",
  "Солярий, на который ведёт крытая лестница с электрической крышей, с душем, встроенным шкафом для хранения, розетками для ТВ и электропитания и подготовкой под джакузи.",
  "سولاريوم يُصعد إليه بدرج مغطى بسقف بمحرك، مع دش وخزانة تخزين مدمجة ومنافذ تلفزيون وكهرباء وتجهيز مسبق لجاكوزي.",
  "Solarium dat via een overdekte trap met gemotoriseerd dak wordt bereikt, met douche, een ingebouwde bergkast, tv- en stroomaansluitingen en voorbereiding voor een bubbelbad.",
  "Solarium, na które prowadzą zadaszone schody z dachem na napędzie elektrycznym, z prysznicem, wbudowaną szafą gospodarczą, gniazdami TV i zasilania oraz instalacją pod jacuzzi.",
  "Solterrasse som nås via en overbygd trapp med motorisert tak, med dusj, innebygd oppbevaringsskap, TV- og strømuttak og forberedelse for boblebad.",
  "Solterrass som nås via en övertäckt trappa med motoriserat tak, med dusch, ett inbyggt förvaringsskåp, TV- och eluttag och förberedelse för bubbelpool.")
a(107, 'Home automation linked to climate',
  "Domótica vinculada a climatización, multimedia, alarma, agua, iluminación y persianas, con coste adicional.",
  "Domotique reliée à la climatisation, au multimédia, à l'alarme, à l'eau, à l'éclairage et aux stores, disponible en option payante.",
  "Hausautomation für Klima, Multimedia, Alarm, Wasser, Beleuchtung und Jalousien gegen Aufpreis erhältlich.",
  "Система «умный дом», объединяющая климат, мультимедиа, сигнализацию, воду, освещение и жалюзи, доступна за дополнительную плату.",
  "أتمتة المنزل المرتبطة بالمناخ والوسائط المتعددة والإنذار والمياه والإضاءة والستائر متاحة مقابل تكلفة إضافية.",
  "Domotica voor klimaat, multimedia, alarm, water, verlichting en zonwering is tegen meerprijs verkrijgbaar.",
  "Automatyka domowa obejmująca klimatyzację, multimedia, alarm, wodę, oświetlenie i rolety jest dostępna za dodatkową opłatą.",
  "Hjemmeautomatisering knyttet til klima, multimedia, alarm, vann, belysning og persienner er tilgjengelig mot tillegg.",
  "Hemautomation kopplad till klimat, multimedia, larm, vatten, belysning och persienner finns mot tillägg.")
a(108, 'The structure is pre-installed for a lift',
  "La estructura tiene preinstalación para un ascensor que para en todas las plantas salvo en el solárium; el ascensor en sí no está incluido.",
  "La structure est pré-équipée pour un ascenseur desservant tous les niveaux sauf le solarium ; l'ascenseur lui-même n'est pas inclus.",
  "Die Struktur ist für einen Aufzug vorbereitet, der auf allen Ebenen außer dem Solarium hält; der Aufzug selbst ist nicht enthalten.",
  "Конструкция подготовлена под лифт, останавливающийся на всех уровнях, кроме солярия; сам лифт в стоимость не входит.",
  "البنية مجهزة مسبقًا لمصعد يتوقف في كل الطوابق باستثناء السولاريوم؛ والمصعد نفسه غير مشمول.",
  "De constructie is voorbereid op een lift die op elke verdieping stopt behalve bij het solarium; de lift zelf is niet inbegrepen.",
  "Konstrukcja jest przygotowana pod windę zatrzymującą się na każdej kondygnacji z wyjątkiem solarium; sama winda nie jest w cenie.",
  "Konstruksjonen er forberedt for en heis som stopper i alle etasjer unntatt ved solterrassen; selve heisen er ikke inkludert.",
  "Konstruktionen är förberedd för en hiss som stannar på alla plan utom vid solterrassen; själva hissen ingår inte.")
a(109, 'Customisation of materials',
  "La personalización de materiales, con y sin coste adicional, es posible a través del catálogo de la promotora dentro de los plazos fijados. Los paquetes de mobiliario se valoran aparte.",
  "La personnalisation des matériaux, avec ou sans supplément, est possible par le catalogue du promoteur dans des délais fixés. Les packs de mobilier sont chiffrés séparément.",
  "Eine individuelle Auswahl der Materialien, mit und ohne Aufpreis, ist innerhalb festgelegter Fristen über den Katalog des Bauträgers möglich. Möblierungspakete werden gesondert berechnet.",
  "Индивидуальный выбор материалов, с доплатой и без неё, возможен по каталогу застройщика в установленные сроки. Пакеты мебели оцениваются отдельно.",
  "يمكن تخصيص المواد، بتكلفة إضافية أو بدونها، من خلال كتالوج المطور وضمن مهل محددة. وتُسعَّر حزم الأثاث بشكل منفصل.",
  "Het aanpassen van materialen, met en zonder meerprijs, is mogelijk via de catalogus van de ontwikkelaar binnen vastgestelde termijnen. Meubelpakketten worden apart geprijsd.",
  "Personalizacja materiałów, z dopłatą i bez niej, jest możliwa z katalogu dewelopera w ustalonych terminach. Pakiety wyposażenia wyceniane są osobno.",
  "Tilpasning av materialer, med og uten tillegg, er mulig gjennom utviklerens katalog innenfor fastsatte frister. Møbelpakker prises separat.",
  "Anpassning av material, med och utan tillägg, är möjlig via byggherrens katalog inom fastställda tidsfrister. Möbelpaket prissätts separat.")

# ---------------------------------------------------------------- residences
a(110, 'Three or four bedrooms, <em>over four levels</em>',
  "Tres o cuatro dormitorios, <em>en cuatro niveles</em>", "Trois ou quatre chambres, <em>sur quatre niveaux</em>",
  "Drei oder vier Schlafzimmer, <em>auf vier Ebenen</em>", "Три или четыре спальни, <em>на четырёх уровнях</em>",
  "ثلاث أو أربع غرف نوم، <em>على أربعة مستويات</em>", "Drie of vier slaapkamers, <em>over vier niveaus</em>",
  "Trzy lub cztery sypialnie, <em>na czterech poziomach</em>", "Tre eller fire soverom, <em>over fire nivåer</em>",
  "Tre eller fyra sovrum, <em>på fyra nivåer</em>")
a(111, 'The five available villas are Villa 02',
  "Las cinco villas disponibles son la Villa 02, de cuatro dormitorios, y las Villas 03, 05, 06 y 07, de tres. Todas tienen sótano, planta baja, primera planta y solárium en la azotea.",
  "Les cinq villas disponibles sont la Villa 02, de quatre chambres, et les Villas 03, 05, 06 et 07, de trois. Chacune comprend un sous-sol, un rez-de-chaussée, un premier étage et un solarium sur le toit.",
  "Die fünf verfügbaren Villen sind Villa 02 mit vier Schlafzimmern sowie die Villen 03, 05, 06 und 07 mit drei. Jede hat Untergeschoss, Erdgeschoss, erstes Obergeschoss und ein Dach-Solarium.",
  "Пять доступных вилл — Villa 02 с четырьмя спальнями и Villa 03, 05, 06 и 07 с тремя. В каждой есть цокольный этаж, первый и второй этажи и солярий на крыше.",
  "الفلل الخمس المتاحة هي Villa 02 بأربع غرف نوم، وVilla 03 وVilla 05 وVilla 06 وVilla 07 بثلاث غرف نوم. لكل فيلا قبو وطابق أرضي وطابق أول وسولاريوم على السطح.",
  "De vijf beschikbare villa's zijn Villa 02 met vier slaapkamers en Villa 03, 05, 06 en 07 met drie. Elke villa heeft een kelder, een begane grond, een eerste verdieping en een solarium op het dak.",
  "Pięć dostępnych willi to Willa 02 z czterema sypialniami oraz Wille 03, 05, 06 i 07 z trzema. Każda ma piwnicę, parter, pierwsze piętro i solarium na dachu.",
  "De fem tilgjengelige villaene er Villa 02 med fire soverom og Villa 03, 05, 06 og 07 med tre. Hver har kjeller, første etasje, andre etasje og solterrasse på taket.",
  "De fem tillgängliga villorna är Villa 02 med fyra sovrum och Villa 03, 05, 06 och 07 med tre. Var och en har källare, bottenvåning, första våning och solterrass på taket.")
a(112, 'Ground floor: living and dining room of 46.31 sqm',
  "Planta baja: salón comedor de {N46.31} {U} con una zona a doble altura, cocina de {N8.80} {U}, un dormitorio de {N14.36} {U} con baño propio y un porche cubierto que se abre al jardín y a la piscina.",
  "Rez-de-chaussée : séjour-salle à manger de {N46.31} {U} avec une partie en double hauteur, cuisine de {N8.80} {U}, une chambre de {N14.36} {U} avec salle de bains privative et un porche couvert ouvrant sur le jardin et la piscine.",
  "Erdgeschoss: Wohn- und Essbereich von {N46.31} {U} mit einem Teil in doppelter Raumhöhe, Küche mit {N8.80} {U}, ein Schlafzimmer von {N14.36} {U} mit eigenem Bad und ein überdachter Vorbau zu Garten und Pool.",
  "Первый этаж: гостиная-столовая {N46.31} {U} с частью двойной высоты, кухня {N8.80} {U}, спальня {N14.36} {U} с собственной ванной комнатой и крытый портик с выходом в сад и к бассейну.",
  "الطابق الأرضي: غرفة معيشة وطعام بمساحة {N46.31} {U} بجزء مزدوج الارتفاع، ومطبخ بمساحة {N8.80} {U}، وغرفة نوم بمساحة {N14.36} {U} بحمام خاص، ورواق مغطى يفتح على الحديقة والمسبح.",
  "Begane grond: woon- en eetkamer van {N46.31} {U} met een dubbel hoog deel, keuken van {N8.80} {U}, een slaapkamer van {N14.36} {U} met eigen badkamer en een overdekte veranda die uitkomt op de tuin en het zwembad.",
  "Parter: salon z jadalnią o powierzchni {N46.31} {U} z częścią o podwójnej wysokości, kuchnia {N8.80} {U}, sypialnia {N14.36} {U} z własną łazienką oraz zadaszony ganek otwierający się na ogród i basen.",
  "Første etasje: stue og spisestue på {N46.31} {U} med en del i dobbel takhøyde, kjøkken på {N8.80} {U}, et soverom på {N14.36} {U} med eget bad og en overbygd veranda mot hagen og bassenget.",
  "Bottenvåning: vardagsrum och matplats på {N46.31} {U} med en del i dubbel takhöjd, kök på {N8.80} {U}, ett sovrum på {N14.36} {U} med eget badrum och en övertäckt veranda mot trädgården och poolen.")
a(113, 'First floor: three bedrooms of 19.13',
  "Primera planta: tres dormitorios de {N19.13}, {N16.04} y {N14.84} {U}, cada uno con baño propio, y un vestidor de {N6.98} {U} para el dormitorio principal.",
  "Premier étage : trois chambres de {N19.13}, {N16.04} et {N14.84} {U}, chacune avec salle de bains privative, et un dressing de {N6.98} {U} pour la chambre principale.",
  "Erstes Obergeschoss: drei Schlafzimmer mit {N19.13}, {N16.04} und {N14.84} {U}, jeweils mit eigenem Bad, sowie ein Ankleidezimmer von {N6.98} {U} für das Hauptschlafzimmer.",
  "Второй этаж: три спальни площадью {N19.13}, {N16.04} и {N14.84} {U}, каждая с собственной ванной комнатой, и гардеробная {N6.98} {U} при главной спальне.",
  "الطابق الأول: ثلاث غرف نوم بمساحات {N19.13} و{N16.04} و{N14.84} {U}، لكل منها حمام خاص، وغرفة ملابس بمساحة {N6.98} {U} لغرفة النوم الرئيسية.",
  "Eerste verdieping: drie slaapkamers van {N19.13}, {N16.04} en {N14.84} {U}, elk met eigen badkamer, en een kleedkamer van {N6.98} {U} bij de hoofdslaapkamer.",
  "Pierwsze piętro: trzy sypialnie o powierzchni {N19.13}, {N16.04} i {N14.84} {U}, każda z własną łazienką, oraz garderoba {N6.98} {U} przy głównej sypialni.",
  "Andre etasje: tre soverom på {N19.13}, {N16.04} og {N14.84} {U}, hvert med eget bad, og en garderobe på {N6.98} {U} til hovedsoverommet.",
  "Första våningen: tre sovrum på {N19.13}, {N16.04} och {N14.84} {U}, vart och ett med eget badrum, och en klädkammare på {N6.98} {U} till huvudsovrummet.")
a(114, 'Basement: a private garage of 41.90 sqm',
  "Sótano: garaje privado de {N41.90} {U} para dos coches, sala polivalente de {N33.10} {U}, lavandería de {N5.46} {U} y trasteros.",
  "Sous-sol : garage privé de {N41.90} {U} pour deux voitures, salle polyvalente de {N33.10} {U}, buanderie de {N5.46} {U} et débarras.",
  "Untergeschoss: private Garage von {N41.90} {U} für zwei Autos, Multifunktionsraum von {N33.10} {U}, Waschküche von {N5.46} {U} und Abstellräume.",
  "Цокольный этаж: частный гараж {N41.90} {U} на две машины, многофункциональное помещение {N33.10} {U}, прачечная {N5.46} {U} и кладовые.",
  "القبو: مرآب خاص بمساحة {N41.90} {U} لسيارتين، وغرفة متعددة الاستخدامات بمساحة {N33.10} {U}، وغرفة غسيل بمساحة {N5.46} {U}، ومخازن.",
  "Kelder: een eigen garage van {N41.90} {U} voor twee auto's, een multifunctionele ruimte van {N33.10} {U}, een wasruimte van {N5.46} {U} en bergingen.",
  "Piwnica: prywatny garaż o powierzchni {N41.90} {U} na dwa samochody, pomieszczenie wielofunkcyjne {N33.10} {U}, pralnia {N5.46} {U} i komórki.",
  "Kjeller: privat garasje på {N41.90} {U} for to biler, flerbruksrom på {N33.10} {U}, vaskerom på {N5.46} {U} og boder.",
  "Källare: privat garage på {N41.90} {U} för två bilar, allrum på {N33.10} {U}, tvättstuga på {N5.46} {U} och förråd.")
a(115, 'Outdoors: a 95 sqm solarium, a 513 sqm garden',
  "Exterior: solárium de {N95} {U}, jardín de {N513} {U} y piscina infinity de {DIM10x4}.",
  "Extérieur : solarium de {N95} {U}, jardin de {N513} {U} et piscine à débordement de {DIM10x4}.",
  "Außenbereich: Solarium mit {N95} {U}, Garten mit {N513} {U} und Infinity-Pool von {DIM10x4}.",
  "На улице: солярий {N95} {U}, сад {N513} {U} и бассейн-инфинити {DIM10x4}.",
  "المساحات الخارجية: سولاريوم بمساحة {N95} {U}، وحديقة بمساحة {N513} {U}، ومسبح لا نهائي بقياس {DIM10x4}.",
  "Buiten: een solarium van {N95} {U}, een tuin van {N513} {U} en een infinity pool van {DIM10x4}.",
  "Na zewnątrz: solarium o powierzchni {N95} {U}, ogród {N513} {U} i basen infinity {DIM10x4}.",
  "Utendørs: solterrasse på {N95} {U}, hage på {N513} {U} og infinitybasseng på {DIM10x4}.",
  "Utomhus: solterrass på {N95} {U}, trädgård på {N513} {U} och infinitypool på {DIM10x4}.")
a(116, 'Ground floor: living and dining room under a double-height',
  "Planta baja: salón comedor con una zona a doble altura, cocina, un dormitorio con acceso a la terraza y baño, y un porche cubierto con barbacoa de gas integrada.",
  "Rez-de-chaussée : séjour-salle à manger avec une partie en double hauteur, cuisine, une chambre donnant accès à la terrasse et une salle de bains, et un porche couvert avec barbecue à gaz intégré.",
  "Erdgeschoss: Wohn- und Essbereich mit einem Teil in doppelter Raumhöhe, Küche, ein Schlafzimmer mit Zugang zur Terrasse, ein Bad und ein überdachter Vorbau mit eingebautem Gasgrill.",
  "Первый этаж: гостиная-столовая с частью двойной высоты, кухня, спальня с выходом на террасу, ванная комната и крытый портик со встроенным газовым грилем.",
  "الطابق الأرضي: غرفة معيشة وطعام بجزء مزدوج الارتفاع، ومطبخ، وغرفة نوم تطل على التراس، وحمام، ورواق مغطى بشواية غاز مدمجة.",
  "Begane grond: woon- en eetkamer met een dubbel hoog deel, keuken, een slaapkamer met toegang tot het terras, een badkamer en een overdekte veranda met ingebouwde gasbarbecue.",
  "Parter: salon z jadalnią w części o podwójnej wysokości, kuchnia, sypialnia z wyjściem na taras, łazienka oraz zadaszony ganek z wbudowanym grillem gazowym.",
  "Første etasje: stue og spisestue med en del i dobbel takhøyde, kjøkken, et soverom med tilgang til terrassen, et bad og en overbygd veranda med innebygd gassgrill.",
  "Bottenvåning: vardagsrum och matplats med en del i dubbel takhöjd, kök, ett sovrum med tillgång till terrassen, ett badrum och en övertäckt veranda med inbyggd gasolgrill.")
a(117, 'First floor: two bedrooms, each with its own bathroom',
  "Primera planta: dos dormitorios, cada uno con baño propio, y el principal con vestidor.",
  "Premier étage : deux chambres, chacune avec salle de bains privative, la principale avec dressing.",
  "Erstes Obergeschoss: zwei Schlafzimmer mit jeweils eigenem Bad, das Hauptschlafzimmer mit Ankleidezimmer.",
  "Второй этаж: две спальни, каждая с собственной ванной комнатой; при главной спальне есть гардеробная.",
  "الطابق الأول: غرفتا نوم، لكل منهما حمام خاص، وتضم الرئيسية غرفة ملابس.",
  "Eerste verdieping: twee slaapkamers, elk met eigen badkamer, de hoofdslaapkamer met kleedkamer.",
  "Pierwsze piętro: dwie sypialnie, każda z własną łazienką, główna z garderobą.",
  "Andre etasje: to soverom, hvert med eget bad, hovedsoverommet med garderobe.",
  "Första våningen: två sovrum, vart och ett med eget badrum, huvudsovrummet med klädkammare.")
a(118, 'Basement: a private garage for two cars, a multipurpose room',
  "Sótano: garaje privado para dos coches, sala polivalente, lavandería y trasteros.",
  "Sous-sol : garage privé pour deux voitures, salle polyvalente, buanderie et débarras.",
  "Untergeschoss: private Garage für zwei Autos, Multifunktionsraum, Waschküche und Abstellräume.",
  "Цокольный этаж: частный гараж на две машины, многофункциональное помещение, прачечная и кладовые.",
  "القبو: مرآب خاص لسيارتين، وغرفة متعددة الاستخدامات، وغرفة غسيل، ومخازن.",
  "Kelder: een eigen garage voor twee auto's, een multifunctionele ruimte, een wasruimte en bergingen.",
  "Piwnica: prywatny garaż na dwa samochody, pomieszczenie wielofunkcyjne, pralnia i komórki.",
  "Kjeller: privat garasje for to biler, flerbruksrom, vaskerom og boder.",
  "Källare: privat garage för två bilar, allrum, tvättstuga och förråd.")
a(119, 'Outdoors: a 49 sqm solarium, a 374 sqm garden',
  "Exterior: solárium de {N49} {U}, jardín de {N374} {U} y piscina infinity de {DIM8x4}.",
  "Extérieur : solarium de {N49} {U}, jardin de {N374} {U} et piscine à débordement de {DIM8x4}.",
  "Außenbereich: Solarium mit {N49} {U}, Garten mit {N374} {U} und Infinity-Pool von {DIM8x4}.",
  "На улице: солярий {N49} {U}, сад {N374} {U} и бассейн-инфинити {DIM8x4}.",
  "المساحات الخارجية: سولاريوم بمساحة {N49} {U}، وحديقة بمساحة {N374} {U}، ومسبح لا نهائي بقياس {DIM8x4}.",
  "Buiten: een solarium van {N49} {U}, een tuin van {N374} {U} en een infinity pool van {DIM8x4}.",
  "Na zewnątrz: solarium o powierzchni {N49} {U}, ogród {N374} {U} i basen infinity {DIM8x4}.",
  "Utendørs: solterrasse på {N49} {U}, hage på {N374} {U} og infinitybasseng på {DIM8x4}.",
  "Utomhus: solterrass på {N49} {U}, trädgård på {N374} {U} och infinitypool på {DIM8x4}.")
a(120, 'Outdoors: a 49 sqm solarium, a 380 sqm garden',
  "Exterior: solárium de {N49} {U}, jardín de {N380} {U} y piscina infinity de {DIM8x4}.",
  "Extérieur : solarium de {N49} {U}, jardin de {N380} {U} et piscine à débordement de {DIM8x4}.",
  "Außenbereich: Solarium mit {N49} {U}, Garten mit {N380} {U} und Infinity-Pool von {DIM8x4}.",
  "На улице: солярий {N49} {U}, сад {N380} {U} и бассейн-инфинити {DIM8x4}.",
  "المساحات الخارجية: سولاريوم بمساحة {N49} {U}، وحديقة بمساحة {N380} {U}، ومسبح لا نهائي بقياس {DIM8x4}.",
  "Buiten: een solarium van {N49} {U}, een tuin van {N380} {U} en een infinity pool van {DIM8x4}.",
  "Na zewnątrz: solarium o powierzchni {N49} {U}, ogród {N380} {U} i basen infinity {DIM8x4}.",
  "Utendørs: solterrasse på {N49} {U}, hage på {N380} {U} og infinitybasseng på {DIM8x4}.",
  "Utomhus: solterrass på {N49} {U}, trädgård på {N380} {U} och infinitypool på {DIM8x4}.")
a(121, 'Basement: a private garage for two cars, a laundry room and storerooms, with no multipurpose',
  "Sótano: garaje privado para dos coches, lavandería y trasteros, sin sala polivalente.",
  "Sous-sol : garage privé pour deux voitures, buanderie et débarras, sans salle polyvalente.",
  "Untergeschoss: private Garage für zwei Autos, Waschküche und Abstellräume, ohne Multifunktionsraum.",
  "Цокольный этаж: частный гараж на две машины, прачечная и кладовые, без многофункционального помещения.",
  "القبو: مرآب خاص لسيارتين، وغرفة غسيل، ومخازن، دون غرفة متعددة الاستخدامات.",
  "Kelder: een eigen garage voor twee auto's, een wasruimte en bergingen, zonder multifunctionele ruimte.",
  "Piwnica: prywatny garaż na dwa samochody, pralnia i komórki, bez pomieszczenia wielofunkcyjnego.",
  "Kjeller: privat garasje for to biler, vaskerom og boder, uten flerbruksrom.",
  "Källare: privat garage för två bilar, tvättstuga och förråd, utan allrum.")
a(122, 'Outdoors: a 56 sqm solarium, a 317 sqm garden',
  "Exterior: solárium de {N56} {U}, jardín de {N317} {U} y piscina infinity de {DIM8x4}.",
  "Extérieur : solarium de {N56} {U}, jardin de {N317} {U} et piscine à débordement de {DIM8x4}.",
  "Außenbereich: Solarium mit {N56} {U}, Garten mit {N317} {U} und Infinity-Pool von {DIM8x4}.",
  "На улице: солярий {N56} {U}, сад {N317} {U} и бассейн-инфинити {DIM8x4}.",
  "المساحات الخارجية: سولاريوم بمساحة {N56} {U}، وحديقة بمساحة {N317} {U}، ومسبح لا نهائي بقياس {DIM8x4}.",
  "Buiten: een solarium van {N56} {U}, een tuin van {N317} {U} en een infinity pool van {DIM8x4}.",
  "Na zewnątrz: solarium o powierzchni {N56} {U}, ogród {N317} {U} i basen infinity {DIM8x4}.",
  "Utendørs: solterrasse på {N56} {U}, hage på {N317} {U} og infinitybasseng på {DIM8x4}.",
  "Utomhus: solterrass på {N56} {U}, trädgård på {N317} {U} och infinitypool på {DIM8x4}.")
a(123, 'Parking: two spaces on the surface under a pergola',
  "Aparcamiento: dos plazas en superficie bajo una pérgola, según muestran los planos y la circular informativa de la promotora; esta villa no tiene garaje en el sótano.",
  "Stationnement : deux places en surface sous une pergola, comme le montrent les plans et la circulaire d'information du promoteur ; cette villa n'a pas de garage en sous-sol.",
  "Stellplätze: zwei Plätze oberirdisch unter einer Pergola, wie die Pläne und das Informationsschreiben des Bauträgers zeigen; diese Villa hat keine Garage im Untergeschoss.",
  "Парковка: два места на поверхности под перголой, как показывают планировки и информационное письмо застройщика; гаража в цоколе у этой виллы нет.",
  "المواقف: موقفان على السطح تحت برغولا، كما تُظهر المخططات والتعميم الصادر عن المطور؛ ولا يوجد في هذه الفيلا مرآب في القبو.",
  "Parkeren: twee plaatsen op het maaiveld onder een pergola, zoals de plattegronden en de informatiebrief van de ontwikkelaar laten zien; deze villa heeft geen garage in de kelder.",
  "Parkowanie: dwa miejsca na powierzchni pod pergolą, jak pokazują rzuty i pismo informacyjne dewelopera; ta willa nie ma garażu w piwnicy.",
  "Parkering: to plasser på bakkeplan under en pergola, slik plantegningene og utviklerens informasjonsskriv viser; denne villaen har ingen garasje i kjelleren.",
  "Parkering: två platser på marknivå under en pergola, som planritningarna och byggherrens informationsbrev visar; den här villan har inget garage i källaren.")
a(124, 'Basement: a multipurpose room, a laundry room and storerooms.',
  "Sótano: sala polivalente, lavandería y trasteros.", "Sous-sol : salle polyvalente, buanderie et débarras.",
  "Untergeschoss: Multifunktionsraum, Waschküche und Abstellräume.", "Цокольный этаж: многофункциональное помещение, прачечная и кладовые.",
  "القبو: غرفة متعددة الاستخدامات، وغرفة غسيل، ومخازن.", "Kelder: een multifunctionele ruimte, een wasruimte en bergingen.",
  "Piwnica: pomieszczenie wielofunkcyjne, pralnia i komórki.", "Kjeller: flerbruksrom, vaskerom og boder.", "Källare: allrum, tvättstuga och förråd.")
a(125, 'Outdoors: a 56 sqm solarium, a 330 sqm garden',
  "Exterior: solárium de {N56} {U}, jardín de {N330} {U} y piscina infinity de {DIM8x4}.",
  "Extérieur : solarium de {N56} {U}, jardin de {N330} {U} et piscine à débordement de {DIM8x4}.",
  "Außenbereich: Solarium mit {N56} {U}, Garten mit {N330} {U} und Infinity-Pool von {DIM8x4}.",
  "На улице: солярий {N56} {U}, сад {N330} {U} и бассейн-инфинити {DIM8x4}.",
  "المساحات الخارجية: سولاريوم بمساحة {N56} {U}، وحديقة بمساحة {N330} {U}، ومسبح لا نهائي بقياس {DIM8x4}.",
  "Buiten: een solarium van {N56} {U}, een tuin van {N330} {U} en een infinity pool van {DIM8x4}.",
  "Na zewnątrz: solarium o powierzchni {N56} {U}, ogród {N330} {U} i basen infinity {DIM8x4}.",
  "Utendørs: solterrasse på {N56} {U}, hage på {N330} {U} og infinitybasseng på {DIM8x4}.",
  "Utomhus: solterrass på {N56} {U}, trädgård på {N330} {U} och infinitypool på {DIM8x4}.")

# ---------------------------------------------------------------- lifestyle, location
a(126, 'Each villa is arranged around its own pool',
  "Cada villa se organiza en torno a su propia piscina, su jardín y su porche cubierto, con un solárium en la azotea.",
  "Chaque villa s'organise autour de sa propre piscine, de son jardin et de son porche couvert, avec un solarium sur le toit.",
  "Jede Villa ist um ihren eigenen Pool, Garten und überdachten Vorbau angelegt, mit einem Solarium auf dem Dach.",
  "Каждая вилла организована вокруг собственного бассейна, сада и крытого портика, а на крыше расположен солярий.",
  "تتنظم كل فيلا حول مسبحها وحديقتها ورواقها المغطى، مع سولاريوم على السطح.",
  "Elke villa is opgezet rond een eigen zwembad, tuin en overdekte veranda, met een solarium op het dak.",
  "Każda willa jest zaplanowana wokół własnego basenu, ogrodu i zadaszonego ganku, z solarium na dachu.",
  "Hver villa er lagt opp rundt sitt eget basseng, sin egen hage og sin overbygde veranda, med solterrasse på taket.",
  "Varje villa är planerad kring sin egen pool, sin trädgård och sin övertäckta veranda, med en solterrass på taket.")
a(127, 'Pool and garden',
  "Piscina y jardín", "Piscine et jardin", "Pool und Garten", "Бассейн и сад", "المسبح والحديقة", "Zwembad en tuin", "Basen i ogród", "Basseng og hage", "Pool och trädgård")
a(128, 'An infinity pool in a private garden of natural lawn',
  "Una piscina infinity en un jardín privado de césped natural, con iluminación, riego automático y preinstalación para climatización.",
  "Une piscine à débordement dans un jardin privé de pelouse naturelle, avec éclairage, arrosage automatique et pré-équipement pour le chauffage.",
  "Ein Infinity-Pool in einem privaten Garten mit Naturrasen, mit Beleuchtung, automatischer Bewässerung und Vorinstallation für eine Beheizung.",
  "Бассейн-инфинити в частном саду с натуральным газоном, с освещением, автоматическим поливом и подготовкой под подогрев.",
  "مسبح لا نهائي في حديقة خاصة بعشب طبيعي، مع إضاءة وري تلقائي وتجهيز مسبق للتسخين.",
  "Een infinity pool in een privétuin met natuurlijk gazon, met verlichting, automatische bewatering en voorbereiding voor verwarming.",
  "Basen infinity w prywatnym ogrodzie z naturalnym trawnikiem, z oświetleniem, automatycznym nawadnianiem i instalacją pod podgrzewanie.",
  "Et infinitybasseng i en privat hage med naturlig gress, med belysning, automatisk vanning og forberedelse for oppvarming.",
  "En infinitypool i en privat trädgård med naturlig gräsmatta, med belysning, automatisk bevattning och förberedelse för uppvärmning.")
a(129, 'Porch and barbecue',
  "Porche y barbacoa", "Porche et barbecue", "Vorbau und Grill", "Портик и гриль", "الرواق والشواء", "Veranda en barbecue", "Ganek i grill", "Veranda og grill", "Veranda och grill")
a(130, 'A covered porch off the living room',
  "Un porche cubierto junto al salón, con barbacoa de gas integrada frente al jardín y la piscina.",
  "Un porche couvert attenant au séjour, avec barbecue à gaz intégré face au jardin et à la piscine.",
  "Ein überdachter Vorbau am Wohnzimmer, mit eingebautem Gasgrill zu Garten und Pool hin.",
  "Крытый портик рядом с гостиной со встроенным газовым грилем, обращённым к саду и бассейну.",
  "رواق مغطى بجوار غرفة المعيشة، مع شواية غاز مدمجة مقابل الحديقة والمسبح.",
  "Een overdekte veranda aan de woonkamer, met een ingebouwde gasbarbecue die op de tuin en het zwembad uitkijkt.",
  "Zadaszony ganek przy salonie z wbudowanym grillem gazowym, zwróconym w stronę ogrodu i basenu.",
  "En overbygd veranda ved stuen, med innebygd gassgrill vendt mot hagen og bassenget.",
  "En övertäckt veranda vid vardagsrummet, med inbyggd gasolgrill vänd mot trädgården och poolen.")
a(131, 'Reached by a covered staircase',
  "Se sube por una escalera cubierta con techo motorizado, y tiene ducha, armario trastero y preinstalación para un jacuzzi.",
  "On y accède par un escalier couvert à toit motorisé ; elle comprend une douche, un placard de rangement et un pré-équipement pour un spa.",
  "Erreichbar über eine überdachte Treppe mit motorisiertem Dach, mit Dusche, Schrank und Vorinstallation für einen Whirlpool.",
  "На солярий ведёт крытая лестница с электрической крышей; там есть душ, шкаф для хранения и подготовка под джакузи.",
  "يُصعد إليه بدرج مغطى بسقف بمحرك، ويضم دشًا وخزانة تخزين وتجهيزًا مسبقًا لجاكوزي.",
  "Bereikbaar via een overdekte trap met gemotoriseerd dak, met douche, bergkast en voorbereiding voor een bubbelbad.",
  "Prowadzą na nie zadaszone schody z dachem na napędzie elektrycznym; w solarium jest prysznic, szafa gospodarcza i instalacja pod jacuzzi.",
  "Nås via en overbygd trapp med motorisert tak, med dusj, oppbevaringsskap og forberedelse for boblebad.",
  "Nås via en övertäckt trappa med motoriserat tak, med dusch, förvaringsskåp och förberedelse för bubbelpool.")
a(132, 'Golf and beach',
  "Golf y playa", "Golf et plage", "Golf und Strand", "Гольф и пляж", "الغولف والشاطئ", "Golf en strand", "Golf i plaża", "Golf og strand", "Golf och strand")
a(133, 'Atalaya Golf is 600 m away, and the beach at Saladillo',
  "Atalaya Golf queda a {N600} {M}, y la playa de Saladillo a {N1.9} {KM} a pie, cruzando la A-7 por una pasarela.",
  "Atalaya Golf se trouve à {N600} {M}, et la plage de Saladillo à {N1.9} {KM} à pied, en franchissant l'A-7 par une passerelle.",
  "Atalaya Golf liegt {N600} {M} entfernt, der Strand von Saladillo {N1.9} {KM} zu Fuß, mit Überquerung der A-7 über eine Fußgängerbrücke.",
  "Atalaya Golf находится в {N600} {M}, а до пляжа Саладильо {N1.9} {KM} пешком, через A-7 по пешеходному мосту.",
  "يبعد Atalaya Golf مسافة {N600} {M}، وشاطئ سالاديو {N1.9} {KM} سيرًا على الأقدام مع عبور الطريق A-7 عبر جسر للمشاة.",
  "Atalaya Golf ligt op {N600} {M}, en het strand van Saladillo op {N1.9} {KM} lopen, met een oversteek van de A-7 via een voetgangersbrug.",
  "Atalaya Golf jest oddalone o {N600} {M}, a plaża Saladillo o {N1.9} {KM} pieszo, z przejściem nad A-7 kładką dla pieszych.",
  "Atalaya Golf ligger {N600} {M} unna, og stranden ved Saladillo er {N1.9} {KM} til fots, med kryssing av A-7 via en gangbro.",
  "Atalaya Golf ligger {N600} {M} bort, och stranden vid Saladillo är {N1.9} {KM} till fots, med korsning av A-7 via en gångbro.")
a(134, 'Atalaya, <em>between Estepona and Marbella</em>',
  "Atalaya, <em>entre Estepona y Marbella</em>", "Atalaya, <em>entre Estepona et Marbella</em>", "Atalaya, <em>zwischen Estepona und Marbella</em>",
  "Аталайя, <em>между Эстепоной и Марбельей</em>", "أتالايا، <em>بين إستيبونا وماربيا</em>", "Atalaya, <em>tussen Estepona en Marbella</em>",
  "Atalaya, <em>między Esteponą a Marbellą</em>", "Atalaya, <em>mellom Estepona og Marbella</em>", "Atalaya, <em>mellan Estepona och Marbella</em>")
a(135, 'Atalaya is an established residential area of golf',
  "Atalaya es una zona residencial consolidada de golf y grandes parcelas, en el tramo de la Costa del Sol entre Estepona, Marbella y Benahavís. La carretera de Benahavís queda a {N500} {M}, la A-7 a {N1} {KM} y la AP-7 a {N8} {KM}, y el aeropuerto de Málaga a unos 40 minutos en coche.",
  "Atalaya est un secteur résidentiel établi de golfs et de grandes parcelles, sur le tronçon de la Costa del Sol entre Estepona, Marbella et Benahavís. La route de Benahavís est à {N500} {M}, l'A-7 à {N1} {KM} et l'AP-7 à {N8} {KM}, et l'aéroport de Malaga à environ 40 minutes en voiture.",
  "Atalaya ist ein gewachsenes Wohngebiet mit Golf und großen Grundstücken an dem Abschnitt der Costa del Sol zwischen Estepona, Marbella und Benahavís. Die Straße nach Benahavís ist {N500} {M} entfernt, die A-7 {N1} {KM} und die AP-7 {N8} {KM}; der Flughafen Málaga ist mit dem Auto in etwa 40 Minuten erreichbar.",
  "Аталайя — сложившийся жилой район с гольфом и крупными участками на отрезке Коста-дель-Соль между Эстепоной, Марбельей и Бенаависом. Дорога на Бенаавис находится в {N500} {M}, трасса A-7 — в {N1} {KM}, AP-7 — в {N8} {KM}, а до аэропорта Малаги около 40 минут на машине.",
  "أتالايا منطقة سكنية راسخة للغولف والقطع الكبيرة، على امتداد كوستا ديل سول بين إستيبونا وماربيا وبيناهافيس. يبعد طريق بيناهافيس {N500} {M}، والطريق A-7 {N1} {KM}، والطريق AP-7 {N8} {KM}، ومطار مالقة نحو 40 دقيقة بالسيارة.",
  "Atalaya is een gevestigd woongebied met golf en grote percelen, aan het stuk van de Costa del Sol tussen Estepona, Marbella en Benahavís. De weg naar Benahavís ligt op {N500} {M}, de A-7 op {N1} {KM} en de AP-7 op {N8} {KM}, en de luchthaven van Málaga is ongeveer 40 minuten met de auto.",
  "Atalaya to ugruntowana dzielnica mieszkalna z polami golfowymi i dużymi działkami, na odcinku Costa del Sol między Esteponą, Marbellą i Benahavís. Droga do Benahavís jest oddalona o {N500} {M}, A-7 o {N1} {KM}, a AP-7 o {N8} {KM}, a lotnisko w Maladze o około 40 minut jazdy samochodem.",
  "Atalaya er et etablert boligområde med golf og store tomter, på strekningen av Costa del Sol mellom Estepona, Marbella og Benahavís. Veien til Benahavís ligger {N500} {M} unna, A-7 {N1} {KM} og AP-7 {N8} {KM}, og Málaga lufthavn er omtrent 40 minutter unna med bil.",
  "Atalaya är ett etablerat bostadsområde med golf och stora tomter, på den del av Costa del Sol som ligger mellan Estepona, Marbella och Benahavís. Vägen till Benahavís ligger {N500} {M} bort, A-7 {N1} {KM} och AP-7 {N8} {KM}, och Málagas flygplats är ungefär 40 minuter bort med bil.")
a(136, 'Saladillo beach',
  "Playa de Saladillo", "Plage de Saladillo", "Strand von Saladillo", "Пляж Саладильо", "شاطئ سالاديو", "Strand van Saladillo", "Plaża Saladillo", "Saladillo-stranden", "Saladillostranden")
a(137, '1.9 km on foot',
  "{N1.9} {KM} a pie", "{N1.9} {KM} à pied", "{N1.9} {KM} zu Fuß", "{N1.9} {KM} пешком", "{N1.9} {KM} سيرًا", "{N1.9} {KM} lopen",
  "{N1.9} {KM} pieszo", "{N1.9} {KM} til fots", "{N1.9} {KM} till fots")
a(138, 'Malaga airport',
  "Aeropuerto de Málaga", "Aéroport de Malaga", "Flughafen Malaga", "Аэропорт Малаги", "مطار مالقة", "Luchthaven Málaga", "Lotnisko w Maladze", "Málaga lufthavn", "Málagas flygplats")

# ---------------------------------------------------------------- investment, trust, availability
a(139, 'The payment stages are set out in the developer’s sales contract',
  "Las fases de pago figuran en el contrato de compraventa de la promotora. Confirmamos por escrito los importes y las fechas vigentes antes de que reserve.",
  "Les étapes de paiement figurent dans le contrat de vente du promoteur. Nous confirmons par écrit les montants et les dates en vigueur avant que vous ne réserviez.",
  "Die Zahlungsstufen sind im Kaufvertrag des Bauträgers festgelegt. Wir bestätigen die aktuellen Beträge und Termine schriftlich, bevor Sie reservieren.",
  "Этапы оплаты изложены в договоре купли-продажи застройщика. Мы письменно подтверждаем действующие суммы и сроки до того, как вы забронируете.",
  "مراحل الدفع مبينة في عقد البيع الخاص بالمطور. نؤكد لك كتابةً المبالغ والتواريخ الحالية قبل أن تحجز.",
  "De betalingsfasen staan in de koopovereenkomst van de ontwikkelaar. Wij bevestigen de actuele bedragen en data schriftelijk voordat u reserveert.",
  "Etapy płatności określa umowa sprzedaży dewelopera. Aktualne kwoty i terminy potwierdzamy Państwu na piśmie przed rezerwacją.",
  "Betalingstrinnene er fastsatt i utviklerens kjøpekontrakt. Vi bekrefter gjeldende beløp og datoer skriftlig før du reserverer.",
  "Betalningsstegen framgår av byggherrens köpeavtal. Vi bekräftar gällande belopp och datum skriftligt innan ni reserverar.")
a(140, 'Reservation and contract',
  "Reserva y contrato", "Réservation et contrat", "Reservierung und Vertrag", "Бронирование и договор", "الحجز والعقد", "Reservering en contract", "Rezerwacja i umowa", "Reservasjon og kontrakt", "Reservation och avtal")
a(141, 'The developer’s May 2024 circular set the reservation deposit',
  "La circular informativa de la promotora de mayo de 2024 fijaba la señal de reserva en {E50000}, y los pagos por fases se recogían después en el contrato de compraventa.",
  "La circulaire d'information du promoteur de mai 2024 fixait le dépôt de réservation à {E50000}, les paiements échelonnés suivant dans le contrat d'achat.",
  "Das Informationsschreiben des Bauträgers vom Mai 2024 setzte die Reservierungsanzahlung auf {E50000} fest; die Ratenzahlungen folgen dann im Kaufvertrag.",
  "Информационное письмо застройщика от мая 2024 года устанавливало депозит при бронировании в размере {E50000}; поэтапные платежи затем следуют по договору купли-продажи.",
  "حدد التعميم الصادر عن المطور في مايو 2024 دفعة الحجز بمبلغ {E50000}، على أن تأتي الدفعات المرحلية لاحقًا في عقد الشراء.",
  "De informatiebrief van de ontwikkelaar van mei 2024 stelde de aanbetaling bij reservering vast op {E50000}, waarna de gefaseerde betalingen in de koopovereenkomst volgen.",
  "Pismo informacyjne dewelopera z maja 2024 roku ustalało zadatek rezerwacyjny na {E50000}, a kolejne płatności etapowe następowały w umowie kupna.",
  "Utviklerens informasjonsskriv fra mai 2024 fastsatte reservasjonsdepositumet til {E50000}, med de trinnvise betalingene i kjøpekontrakten etterpå.",
  "Byggherrens informationsbrev från maj 2024 fastställde handpenningen vid bokning till {E50000}, och de stegvisa betalningarna följer sedan i köpeavtalet.")
a(142, 'Guaranteed payments',
  "Pagos avalados", "Paiements garantis", "Abgesicherte Zahlungen", "Гарантированные платежи", "دفعات مضمونة", "Gegarandeerde betalingen", "Gwarantowane płatności", "Garanterte innbetalinger", "Garanterade betalningar")
a(143, 'The developer undertakes to guarantee the amounts paid on account',
  "La promotora se compromete a avalar mediante un banco las cantidades entregadas a cuenta, conforme a la ley de edificación española, en un plazo de 20 días desde cada pago.",
  "Le promoteur s'engage à garantir par une banque les sommes versées à valoir sur le prix, conformément à la loi espagnole sur la construction, dans les 20 jours suivant chaque paiement.",
  "Der Bauträger verpflichtet sich, die geleisteten Anzahlungen nach dem spanischen Baurecht innerhalb von 20 Tagen nach jeder Zahlung durch eine Bank abzusichern.",
  "Застройщик обязуется обеспечить банковской гарантией суммы, внесённые в счёт цены, в соответствии с испанским законодательством о строительстве, в течение 20 дней после каждого платежа.",
  "يلتزم المطور بضمان المبالغ المدفوعة على الحساب عبر بنك، بموجب قانون البناء الإسباني، في غضون 20 يومًا من كل دفعة.",
  "De ontwikkelaar verbindt zich ertoe de vooruitbetaalde bedragen via een bank te garanderen, volgens de Spaanse bouwwet, binnen 20 dagen na elke betaling.",
  "Deweloper zobowiązuje się zagwarantować przez bank kwoty wpłacone na poczet ceny, zgodnie z hiszpańskim prawem budowlanym, w ciągu 20 dni od każdej wpłaty.",
  "Utvikleren forplikter seg til å garantere beløpene som er betalt på forskudd gjennom en bank, i henhold til spansk byggelovgivning, innen 20 dager etter hver betaling.",
  "Byggherren förbinder sig att garantera de belopp som betalats på förskott genom en bank, enligt spansk byggnadslag, inom 20 dagar efter varje betalning.")
a(144, 'Costs on top of the price',
  "Gastos adicionales al precio", "Frais en sus du prix", "Kosten zusätzlich zum Preis", "Расходы сверх цены", "تكاليف إضافية على السعر",
  "Kosten bovenop de prijs", "Koszty poza ceną", "Kostnader utover prisen", "Kostnader utöver priset")
a(145, 'The buyer pays the notary, the property registry',
  "El comprador paga la notaría, el Registro de la Propiedad y los impuestos de la compra. El vendedor paga el impuesto de plusvalía y la inscripción de la obra nueva y de su división en unidades.",
  "L'acheteur règle le notaire, le registre de la propriété et les taxes liées à l'achat. Le vendeur règle la taxe de plus-value (plusvalía) et l'inscription de la construction neuve et de sa division en lots.",
  "Der Käufer trägt Notar, Grundbuch und die Erwerbssteuern. Der Verkäufer trägt die Plusvalía-Steuer sowie die Eintragung des Neubaus und seiner Aufteilung in Einheiten.",
  "Покупатель оплачивает нотариуса, реестр недвижимости и налоги при покупке. Продавец оплачивает налог на прирост стоимости (плусвалия) и регистрацию нового строения и его раздела на объекты.",
  "يدفع المشتري أتعاب كاتب العدل والسجل العقاري وضرائب الشراء. ويدفع البائع ضريبة الزيادة في قيمة الأرض (بلوسبايا) وتسجيل المبنى الجديد وتقسيمه إلى وحدات.",
  "De koper betaalt de notaris, het kadaster en de belastingen bij de aankoop. De verkoper betaalt de plusvalía-belasting en de inschrijving van de nieuwbouw en de verdeling ervan in eenheden.",
  "Kupujący płaci notariusza, rejestr nieruchomości i podatki od zakupu. Sprzedający płaci podatek plusvalía oraz wpis nowego budynku i jego podziału na lokale.",
  "Kjøperen betaler notar, eiendomsregisteret og kjøpsavgiftene. Selgeren betaler plusvalía-skatten og registreringen av nybygget og delingen av det i enheter.",
  "Köparen betalar notarie, fastighetsregister och köpskatter. Säljaren betalar plusvalía-skatten och registreringen av nybygget och dess uppdelning i enheter.")
a(146, 'Annual fees',
  "Cuotas anuales", "Charges annuelles", "Jährliche Gebühren", "Ежегодные взносы", "الرسوم السنوية", "Jaarlijkse kosten", "Opłaty roczne", "Årlige avgifter", "Årliga avgifter")
a(147, 'The seven plots belong to the area’s urbanisation maintenance body',
  "Las siete parcelas pertenecen a la entidad de conservación de la urbanización de la zona, con una cuota anual de entre {E183} y {E272} por parcela aproximadamente, según la circular informativa de la promotora de 2024.",
  "Les sept parcelles relèvent de l'association de gestion de la résidence du secteur, avec une cotisation annuelle d'environ {E183} à {E272} par parcelle, selon la circulaire d'information du promoteur de 2024.",
  "Die sieben Grundstücke gehören zur Erhaltungsgemeinschaft der Wohnanlage des Gebiets, mit einer Jahresgebühr von etwa {E183} bis {E272} je Grundstück laut Informationsschreiben des Bauträgers von 2024.",
  "Семь участков входят в организацию по содержанию жилого массива района, с годовым взносом примерно от {E183} до {E272} за участок по информационному письму застройщика 2024 года.",
  "تنتمي القطع السبع إلى هيئة صيانة المجمع السكني في المنطقة، برسوم سنوية تتراوح تقريبًا بين {E183} و{E272} للقطعة بحسب تعميم المطور لعام 2024.",
  "De zeven percelen behoren tot de onderhoudsvereniging van de urbanisatie in het gebied, met een jaarlijkse bijdrage van ongeveer {E183} tot {E272} per perceel, volgens de informatiebrief van de ontwikkelaar uit 2024.",
  "Siedem działek należy do organizacji utrzymującej osiedle w tej okolicy, z roczną opłatą rzędu od {E183} do {E272} za działkę, według pisma informacyjnego dewelopera z 2024 roku.",
  "De sju tomtene tilhører områdets vedlikeholdsforening for boligområdet, med en årlig avgift på omtrent {E183} til {E272} per tomt, ifølge utviklerens informasjonsskriv fra 2024.",
  "De sju tomterna tillhör områdets samfällighet för underhåll av bostadsområdet, med en årlig avgift på ungefär {E183} till {E272} per tomt, enligt byggherrens informationsbrev från 2024.")
a(148, 'The building licence, the current construction stage',
  "La licencia de obra, la fase de construcción actual y el mes de entrega de la villa que elija.",
  "Le permis de construire, l'état d'avancement du chantier et le mois de livraison de la villa que vous choisissez.",
  "Die Baugenehmigung, den aktuellen Baustand und den Übergabemonat der Villa, die Sie wählen.",
  "Разрешение на строительство, текущий этап строительства и месяц сдачи выбранной вами виллы.",
  "رخصة البناء ومرحلة البناء الحالية وشهر تسليم الفيلا التي تختارها.",
  "De bouwvergunning, de huidige bouwfase en de opleveringsmaand van de villa die u kiest.",
  "Pozwolenie na budowę, aktualny etap budowy i miesiąc odbioru wybranej przez Państwa willi.",
  "Byggetillatelsen, nåværende byggetrinn og overleveringsmåneden for villaen du velger.",
  "Bygglovet, det aktuella byggskedet och leveransmånaden för den villa ni väljer.")
a(149, 'The guarantee covering your staged payments',
  "El aval que cubre sus pagos por fases, con nombre y fecha, en un plazo de 20 días desde cada pago.",
  "La garantie couvrant vos paiements échelonnés, nommée et datée, dans les 20 jours suivant chaque paiement.",
  "Die Bankgarantie für Ihre Ratenzahlungen, mit Namen und Datum, innerhalb von 20 Tagen nach jeder Zahlung.",
  "Гарантия, покрывающая ваши поэтапные платежи, с названием банка и датой, в течение 20 дней после каждого платежа.",
  "الضمان الذي يغطي دفعاتكم المرحلية، باسم الضامن وتاريخه، في غضون 20 يومًا من كل دفعة.",
  "De garantie die uw gefaseerde betalingen dekt, met naam en datum, binnen 20 dagen na elke betaling.",
  "Gwarancja obejmująca Państwa płatności etapowe, z nazwą gwaranta i datą, w ciągu 20 dni od każdej wpłaty.",
  "Garantien som dekker de trinnvise innbetalingene dine, navngitt og datert, innen 20 dager etter hver betaling.",
  "Garantin som täcker era stegvisa betalningar, namngiven och daterad, inom 20 dagar efter varje betalning.")
a(150, 'Parking on Villa 07',
  "El aparcamiento de la Villa 07", "Le stationnement de la Villa 07", "Der Stellplatz bei Villa 07", "Парковка на Villa 07", "مواقف الفيلا 07",
  "Het parkeren bij Villa 07", "Parkowanie przy Willi 07", "Parkeringen på Villa 07", "Parkeringen på Villa 07")
a(151, 'Whether its two spaces are on the surface under a pergola',
  "Si sus dos plazas están en superficie bajo una pérgola, como muestran los planos y la circular informativa de la promotora, o si una está en el sótano, como sugiere el folleto de abril de 2026 de la promotora.",
  "Si ses deux places sont en surface sous une pergola, comme le montrent les plans et la circulaire d'information du promoteur, ou si l'une est en sous-sol, comme le suggère la brochure d'avril 2026 du promoteur.",
  "Ob die beiden Stellplätze oberirdisch unter einer Pergola liegen, wie die Pläne und das Informationsschreiben des Bauträgers zeigen, oder ob einer im Untergeschoss liegt, wie die Broschüre des Bauträgers vom April 2026 nahelegt.",
  "Находятся ли два места на поверхности под перголой, как показывают планировки и информационное письмо застройщика, или одно из них в цоколе, как предполагает брошюра застройщика от апреля 2026 года.",
  "هل موقفاها على السطح تحت برغولا، كما تُظهر المخططات وتعميم المطور، أم أن أحدهما في القبو، كما يوحي كتيّب المطور الصادر في أبريل 2026.",
  "Of de twee plaatsen op het maaiveld onder een pergola liggen, zoals de plattegronden en de informatiebrief van de ontwikkelaar laten zien, of dat er één in de kelder ligt, zoals de brochure van de ontwikkelaar van april 2026 doet vermoeden.",
  "Czy oba miejsca znajdują się na powierzchni pod pergolą, jak pokazują rzuty i pismo informacyjne dewelopera, czy jedno z nich jest w piwnicy, jak sugeruje broszura dewelopera z kwietnia 2026 roku.",
  "Om de to plassene ligger på bakkeplan under en pergola, slik plantegningene og utviklerens informasjonsskriv viser, eller om den ene ligger i kjelleren, slik utviklerens brosjyre fra april 2026 antyder.",
  "Om de två platserna ligger på marknivå under en pergola, som planritningarna och byggherrens informationsbrev visar, eller om den ena ligger i källaren, som byggherrens broschyr från april 2026 antyder.")

a(152, 'The price list',
  "La lista de precios", "La liste de prix", "Die Preisliste", "Прайс-лист", "قائمة الأسعار", "De prijslijst", "Lista cen", "Prislisten", "Prislistan")
a(153, 'Whether the quoted price includes VAT',
  "Si el precio indicado incluye el IVA y qué contiene la cifra de equipamiento aparte que figura en la lista de precios de la promotora.",
  "Si le prix indiqué inclut la TVA et ce que comprend le montant d'équipement distinct figurant sur la liste de prix du promoteur.",
  "Ob der genannte Preis die Mehrwertsteuer enthält und was der gesondert ausgewiesene Ausstattungsbetrag in der Preisliste des Bauträgers umfasst.",
  "Включает ли указанная цена НДС и что входит в отдельную сумму за оснащение в прайс-листе застройщика.",
  "هل يشمل السعر المذكور ضريبة القيمة المضافة، وما الذي يتضمنه رقم التجهيز المنفصل في قائمة أسعار المطور.",
  "Of de genoemde prijs btw bevat en wat het apart vermelde uitrustingsbedrag op de prijslijst van de ontwikkelaar omvat.",
  "Czy podana cena zawiera VAT i co obejmuje odrębna kwota za wyposażenie na liście cen dewelopera.",
  "Om den oppgitte prisen inkluderer mva., og hva det separate utstyrsbeløpet på utviklerens prisliste omfatter.",
  "Om det angivna priset inkluderar moms och vad det separata utrustningsbeloppet i byggherrens prislista omfattar.")
a(154, 'Five villas <em>currently available</em>',
  "Cinco villas <em>disponibles ahora</em>", "Cinq villas <em>actuellement disponibles</em>", "Fünf Villen <em>derzeit verfügbar</em>",
  "Пять вилл <em>сейчас в продаже</em>", "خمس فلل <em>متاحة حاليًا</em>", "Vijf villa's <em>momenteel beschikbaar</em>",
  "Pięć willi <em>obecnie dostępnych</em>", "Fem villaer <em>tilgjengelige nå</em>", "Fem villor <em>tillgängliga just nu</em>")
a(155, 'Villas 02, 03, 05, 06 and 07 are the available villas',
  "Las villas 02, 03, 05, 06 y 07 son las disponibles. Las villas 01 y 04 ya no figuran en la lista. Los precios son los de la lista de precios de la promotora, sin su cifra de equipamiento aparte.",
  "Les villas 02, 03, 05, 06 et 07 sont les villas disponibles. Les villas 01 et 04 ne figurent plus sur la liste. Les prix sont ceux de la liste de prix du promoteur, hors son montant d'équipement distinct.",
  "Die Villen 02, 03, 05, 06 und 07 sind verfügbar. Die Villen 01 und 04 sind nicht mehr gelistet. Die Preise stammen aus der Preisliste des Bauträgers, ohne den dort gesondert ausgewiesenen Ausstattungsbetrag.",
  "В продаже виллы 02, 03, 05, 06 и 07. Виллы 01 и 04 из списка исключены. Цены взяты из прайс-листа застройщика без указанной в нём отдельной суммы за оснащение.",
  "الفلل المتاحة هي 02 و03 و05 و06 و07. أما الفيلتان 01 و04 فلم تعودا مدرجتين. الأسعار هي أسعار قائمة المطور، دون رقم التجهيز المنفصل الوارد فيها.",
  "Villa 02, 03, 05, 06 en 07 zijn de beschikbare villa's. Villa 01 en 04 staan niet meer in de lijst. De prijzen zijn die van de prijslijst van de ontwikkelaar, zonder het daarin apart vermelde uitrustingsbedrag.",
  "Dostępne są wille 02, 03, 05, 06 i 07. Wille 01 i 04 nie figurują już na liście. Ceny pochodzą z listy cen dewelopera, bez odrębnej kwoty za wyposażenie, którą ta lista podaje.",
  "Villa 02, 03, 05, 06 og 07 er de tilgjengelige villaene. Villa 01 og 04 er ikke lenger oppført. Prisene er fra utviklerens prisliste, uten det separate utstyrsbeløpet den oppgir.",
  "Villa 02, 03, 05, 06 och 07 är de tillgängliga villorna. Villa 01 och 04 är inte längre listade. Priserna är de i byggherrens prislista, utan det separata utrustningsbelopp den anger.")
a(156, 'Prices and delivery months are transcribed from the developer’s price list of 8 October 2026',
  "Los precios y los meses de entrega están transcritos de la lista de precios de la promotora del 8 de octubre de 2026 para las cinco villas que figuran como disponibles. La lista no indica si el IVA y los gastos de compra están incluidos, y Nueva Living lo confirma antes de cualquier reserva. También muestra una cifra de equipamiento aparte para cada villa ({E56500}, y {E72400} para la Villa 02), que aquí no está incluida. La superficie construida es el total de la promotora: interior, terrazas, porches y solárium. La circular informativa de la promotora de mayo de 2024 daba como fecha de entrega marzo de 2026, que la lista de precios actual sustituye.",
  "Les prix et les mois de livraison sont transcrits de la liste de prix du promoteur du 8 octobre 2026 pour les cinq villas indiquées comme disponibles. La liste ne précise pas si la TVA et les frais d'achat sont inclus, et Nueva Living le confirme avant toute réservation. Elle indique aussi un montant d'équipement distinct pour chaque villa ({E56500}, et {E72400} pour la Villa 02), qui n'est pas inclus ici. La surface construite est le total du promoteur : intérieur, terrasses, porches et solarium. La circulaire d'information du promoteur de mai 2024 donnait une date de livraison de mars 2026, que la liste de prix actuelle remplace.",
  "Preise und Übergabemonate sind der Preisliste des Bauträgers vom 8. Oktober 2026 für die fünf als verfügbar gelisteten Villen entnommen. Die Liste sagt nicht, ob Mehrwertsteuer und Erwerbsnebenkosten enthalten sind, und Nueva Living bestätigt dies vor jeder Reservierung. Sie nennt außerdem für jede Villa einen gesonderten Ausstattungsbetrag ({E56500}, bei Villa 02 {E72400}), der hier nicht enthalten ist. Die bebaute Fläche ist die Gesamtangabe des Bauträgers: Innenräume, Terrassen, Vorbauten und Solarium. Das Informationsschreiben des Bauträgers vom Mai 2024 nannte als Übergabetermin März 2026, den die aktuelle Preisliste ersetzt.",
  "Цены и месяцы сдачи перенесены из прайс-листа застройщика от 8 октября 2026 года по пяти виллам, указанным как доступные. В списке не сказано, включены ли НДС и расходы на покупку, и Nueva Living подтверждает это до любого бронирования. Там же указана отдельная сумма за оснащение для каждой виллы ({E56500}, а для Villa 02 — {E72400}), здесь она не включена. Застроенная площадь — общая цифра застройщика: внутренние помещения, террасы, портики и солярий. Информационное письмо застройщика от мая 2024 года называло сроком сдачи март 2026 года; его заменяет действующий прайс-лист.",
  "الأسعار وأشهر التسليم منقولة من قائمة أسعار المطور المؤرخة في 8 أكتوبر 2026 للفلل الخمس المدرجة كمتاحة. لا تذكر القائمة ما إذا كانت ضريبة القيمة المضافة وتكاليف الشراء مشمولة، وتؤكد Nueva Living ذلك قبل أي حجز. وتُظهر القائمة أيضًا رقم تجهيز منفصلًا لكل فيلا ({E56500}، و{E72400} للفيلا 02)، وهو غير مشمول هنا. المساحة المبنية هي الإجمالي الذي يذكره المطور: المساحات الداخلية والتراسات والأروقة والسولاريوم. وكان تعميم المطور الصادر في مايو 2024 يذكر موعد تسليم هو مارس 2026، وتحل محله قائمة الأسعار الحالية.",
  "Prijzen en opleveringsmaanden zijn overgenomen uit de prijslijst van de ontwikkelaar van 8 oktober 2026 voor de vijf villa's die als beschikbaar zijn vermeld. De lijst vermeldt niet of btw en aankoopkosten zijn inbegrepen, en Nueva Living bevestigt dit vóór elke reservering. Ze toont ook voor elke villa een apart uitrustingsbedrag ({E56500}, en {E72400} voor Villa 02), dat hier niet is inbegrepen. De bebouwde oppervlakte is het totaal van de ontwikkelaar: binnenruimtes, terrassen, veranda's en solarium. De informatiebrief van de ontwikkelaar van mei 2024 gaf als opleverdatum maart 2026, die de huidige prijslijst vervangt.",
  "Ceny i miesiące odbioru przepisano z listy cen dewelopera z 8 października 2026 roku dla pięciu willi wskazanych jako dostępne. Lista nie podaje, czy VAT i koszty zakupu są wliczone, a Nueva Living potwierdza to przed jakąkolwiek rezerwacją. Podaje też odrębną kwotę za wyposażenie każdej willi ({E56500}, a dla Willi 02 {E72400}), której tu nie uwzględniono. Powierzchnia zabudowy to łączna liczba dewelopera: wnętrza, tarasy, ganki i solarium. Pismo informacyjne dewelopera z maja 2024 roku podawało termin odbioru marzec 2026, który zastępuje obecna lista cen.",
  "Prisene og overleveringsmånedene er hentet fra utviklerens prisliste av 8. oktober 2026 for de fem villaene som er oppført som tilgjengelige. Listen oppgir ikke om mva. og kjøpskostnader er inkludert, og Nueva Living bekrefter dette før enhver reservasjon. Den viser også et separat utstyrsbeløp for hver villa ({E56500}, og {E72400} for Villa 02), som ikke er med her. Bygget areal er utviklerens totaltall: innvendige rom, terrasser, verandaer og solterrasse. Utviklerens informasjonsskriv fra mai 2024 oppga overlevering i mars 2026, som den gjeldende prislisten erstatter.",
  "Priserna och leveransmånaderna är avskrivna från byggherrens prislista av den 8 oktober 2026 för de fem villor som anges som tillgängliga. Listan anger inte om moms och köpkostnader ingår, och Nueva Living bekräftar det före varje reservation. Den visar också ett separat utrustningsbelopp för varje villa ({E56500}, och {E72400} för Villa 02), som inte ingår här. Byggd yta är byggherrens totalsiffra: invändiga ytor, terrasser, verandor och solterrass. Byggherrens informationsbrev från maj 2024 angav leverans i mars 2026, vilket den nuvarande prislistan ersätter.")
a(162, 'Aerial view of the seven villas and their plots',
  "Vista aérea de las siete villas y sus parcelas", "Vue aérienne des sept villas et de leurs parcelles", "Luftaufnahme der sieben Villen und ihrer Grundstücke",
  "Вид с воздуха на семь вилл и их участки", "منظر جوي للفلل السبع وقطع أراضيها", "Luchtopname van de zeven villa's en hun percelen",
  "Widok z lotu ptaka na siedem willi i ich działki", "Flyfoto av de sju villaene og tomtene deres", "Flygvy över de sju villorna och deras tomter")

# ---------------------------------------------------------------- timeline, viewing, enquiry
a(163, 'Floorplans for all five available villas',
  "Planos de las cinco villas disponibles, la memoria de calidades y el calendario de pagos.",
  "Plans des cinq villas disponibles, descriptif de la qualité et échéancier de paiement.",
  "Grundrisse aller fünf verfügbaren Villen, die Ausstattungsbeschreibung und der Zahlungsplan.",
  "Планировки всех пяти доступных вилл, спецификация и график платежей.",
  "مخططات الفلل الخمس المتاحة، والمواصفات، وجدول الدفعات.",
  "Plattegronden van alle vijf beschikbare villa's, de specificatie en het betalingsschema.",
  "Rzuty wszystkich pięciu dostępnych willi, specyfikacja i harmonogram płatności.",
  "Plantegninger for alle fem tilgjengelige villaer, spesifikasjonen og betalingsplanen.",
  "Planritningar för alla fem tillgängliga villor, specifikationen och betalningsplanen.")
a(164, 'See this alongside the other Estepona and Marbella villa projects',
  "Véalo junto a los demás proyectos de villas en Estepona y Marbella que representamos.",
  "Découvrez ce programme aux côtés des autres projets de villas à Estepona et Marbella que nous représentons.",
  "Sehen Sie dieses Projekt neben den anderen Villenprojekten in Estepona und Marbella, die wir vertreten.",
  "Посмотрите этот проект рядом с другими проектами вилл в Эстепоне и Марбелье, которые мы представляем.",
  "شاهد هذا المشروع إلى جانب مشاريع الفلل الأخرى في إستيبونا وماربيا التي نمثّلها.",
  "Bekijk dit project naast de andere villaprojecten in Estepona en Marbella die wij vertegenwoordigen.",
  "Zobacz tę inwestycję obok innych projektów willi w Esteponie i Marbelli, które reprezentujemy.",
  "Se dette sammen med de andre villaprosjektene i Estepona og Marbella som vi representerer.",
  "Se detta tillsammans med de andra villaprojekten i Estepona och Marbella som vi representerar.")
a(165, 'Reservation deposit, then the purchase contract',
  "Señal de reserva y después el contrato de compraventa, con los pagos avalados por un banco.",
  "Dépôt de réservation, puis contrat d'achat, avec paiements garantis par une banque.",
  "Reservierungsanzahlung, dann der Kaufvertrag, mit durch eine Bank abgesicherten Zahlungen.",
  "Депозит при бронировании, затем договор купли-продажи, с платежами, защищёнными банковской гарантией.",
  "دفعة الحجز ثم عقد الشراء، مع دفعات مضمونة من بنك.",
  "Aanbetaling bij reservering, daarna de koopovereenkomst, met betalingen die door een bank worden gegarandeerd.",
  "Zadatek rezerwacyjny, następnie umowa kupna, a płatności gwarantowane przez bank.",
  "Reservasjonsdepositum, deretter kjøpekontrakten, med innbetalinger garantert av en bank.",
  "Handpenning vid bokning, därefter köpeavtalet, med betalningar garanterade av en bank.")
a(166, 'We walk the route to the golf club and to the beach with you.',
  "Recorremos con usted el camino al club de golf y a la playa.",
  "Nous parcourons avec vous le trajet jusqu'au club de golf et à la plage.",
  "Wir gehen mit Ihnen den Weg zum Golfclub und zum Strand ab.",
  "Мы вместе с вами пройдём маршрут до гольф-клуба и до пляжа.",
  "نسير معك المسار إلى نادي الغولف وإلى الشاطئ.",
  "Wij lopen de route naar de golfclub en naar het strand samen met u.",
  "Przechodzimy razem z Państwem trasę do klubu golfowego i na plażę.",
  "Vi går veien til golfklubben og til stranden sammen med deg.",
  "Vi går vägen till golfklubben och till stranden tillsammans med er.")
a(167, 'Licence, bank guarantee and payment schedule',
  "La licencia, el aval bancario y el calendario de pagos, antes de firmar nada.",
  "Le permis, la garantie bancaire et l'échéancier de paiement, avant toute signature.",
  "Baugenehmigung, Bankgarantie und Zahlungsplan, bevor etwas unterschrieben wird.",
  "Разрешение на строительство, банковская гарантия и график платежей — до подписания чего-либо.",
  "الرخصة والضمان المصرفي وجدول الدفعات، قبل توقيع أي شيء.",
  "Vergunning, bankgarantie en betalingsschema, vóór er iets wordt ondertekend.",
  "Pozwolenie, gwarancja bankowa i harmonogram płatności — zanim cokolwiek zostanie podpisane.",
  "Tillatelse, bankgaranti og betalingsplan, før noe signeres.",
  "Bygglov, bankgaranti och betalningsplan, innan något skrivs under.")
a(168, 'Ask about <em>Atalaya Pool Villas</em>',
  "Pregunte por <em>Atalaya Pool Villas</em>", "Renseignez-vous sur <em>Atalaya Pool Villas</em>", "Fragen Sie nach <em>Atalaya Pool Villas</em>",
  "Узнайте больше об <em>Atalaya Pool Villas</em>", "استفسر عن <em>Atalaya Pool Villas</em>", "Vraag naar <em>Atalaya Pool Villas</em>",
  "Zapytaj o <em>Atalaya Pool Villas</em>", "Spør om <em>Atalaya Pool Villas</em>", "Fråga om <em>Atalaya Pool Villas</em>")
a(169, 'Hello Nueva Living, I would like information about Atalaya Pool Villas.',
  "Hola Nueva Living, me gustaría recibir información sobre Atalaya Pool Villas.",
  "Bonjour Nueva Living, je souhaite recevoir des informations sur Atalaya Pool Villas.",
  "Hallo Nueva Living, ich interessiere mich für Informationen zu Atalaya Pool Villas.",
  "Здравствуйте, Nueva Living! Я хотел бы получить информацию об Atalaya Pool Villas.",
  "مرحبًا Nueva Living، أرغب في الحصول على معلومات عن Atalaya Pool Villas.",
  "Hallo Nueva Living, ik ontvang graag informatie over Atalaya Pool Villas.",
  "Witam Nueva Living, chciałbym/chciałabym otrzymać informacje o Atalaya Pool Villas.",
  "Hei Nueva Living, jeg ønsker informasjon om Atalaya Pool Villas.",
  "Hej Nueva Living, jag vill gärna få information om Atalaya Pool Villas.")

# ---------------------------------------------------------------- questions and answers
a(170, 'Seven villas make up the development',
  "La promoción se compone de siete villas y cinco figuran ahora como disponibles: la Villa 02, de cuatro dormitorios, y las Villas 03, 05, 06 y 07, de tres, desde {E1530000} hasta {E2220000}. Las villas 01 y 04 ya no figuran en la lista.",
  "Le programme compte sept villas et cinq figurent actuellement comme disponibles : la Villa 02, de quatre chambres, et les Villas 03, 05, 06 et 07, de trois, de {E1530000} à {E2220000}. Les villas 01 et 04 ne figurent plus sur la liste.",
  "Das Projekt besteht aus sieben Villen, von denen fünf derzeit als verfügbar gelistet sind: Villa 02 mit vier Schlafzimmern sowie die Villen 03, 05, 06 und 07 mit drei, von {E1530000} bis {E2220000}. Die Villen 01 und 04 sind nicht mehr gelistet.",
  "В комплексе семь вилл, и пять из них сейчас в продаже: Villa 02 с четырьмя спальнями и Villa 03, 05, 06 и 07 с тремя, по ценам от {E1530000} до {E2220000}. Виллы 01 и 04 из списка исключены.",
  "يتألف المشروع من سبع فلل، وخمس منها مدرجة حاليًا كمتاحة: Villa 02 بأربع غرف نوم، وVilla 03 وVilla 05 وVilla 06 وVilla 07 بثلاث غرف نوم، بأسعار من {E1530000} إلى {E2220000}. أما الفيلتان 01 و04 فلم تعودا مدرجتين.",
  "Het project bestaat uit zeven villa's, waarvan er vijf momenteel als beschikbaar zijn vermeld: Villa 02 met vier slaapkamers en Villa 03, 05, 06 en 07 met drie, van {E1530000} tot {E2220000}. Villa 01 en 04 staan niet meer in de lijst.",
  "Inwestycja obejmuje siedem willi, z których pięć figuruje obecnie jako dostępne: Willa 02 z czterema sypialniami oraz Wille 03, 05, 06 i 07 z trzema, w cenach od {E1530000} do {E2220000}. Wille 01 i 04 nie figurują już na liście.",
  "Prosjektet består av sju villaer, og fem er for øyeblikket oppført som tilgjengelige: Villa 02 med fire soverom og Villa 03, 05, 06 og 07 med tre, fra {E1530000} til {E2220000}. Villa 01 og 04 er ikke lenger oppført.",
  "Projektet består av sju villor och fem är just nu angivna som tillgängliga: Villa 02 med fyra sovrum och Villa 03, 05, 06 och 07 med tre, från {E1530000} till {E2220000}. Villa 01 och 04 är inte längre listade.")
a(171, 'When will the villas be ready?',
  "¿Cuándo estarán listas las villas?", "Quand les villas seront-elles prêtes ?", "Wann sind die Villen fertig?", "Когда виллы будут готовы?",
  "متى ستكون الفلل جاهزة؟", "Wanneer zijn de villa's klaar?", "Kiedy wille będą gotowe?", "Når er villaene ferdige?", "När är villorna klara?")
a(172, 'The developer’s current price list gives a delivery month',
  "La lista de precios actual de la promotora indica un mes de entrega para cada villa: octubre de 2027 para la Villa 05, noviembre de 2027 para la Villa 03, enero de 2028 para la Villa 07 y febrero de 2028 para las Villas 02 y 06. Material anterior de la promotora indicaba marzo de 2026, que la lista actual sustituye.",
  "La liste de prix actuelle du promoteur indique un mois de livraison pour chaque villa : octobre 2027 pour la Villa 05, novembre 2027 pour la Villa 03, janvier 2028 pour la Villa 07 et février 2028 pour les Villas 02 et 06. Des documents antérieurs du promoteur indiquaient mars 2026, que la liste actuelle remplace.",
  "Die aktuelle Preisliste des Bauträgers nennt für jede Villa einen Übergabemonat: Oktober 2027 für Villa 05, November 2027 für Villa 03, Januar 2028 für Villa 07 und Februar 2028 für die Villen 02 und 06. Frühere Unterlagen des Bauträgers nannten März 2026, was die aktuelle Liste ersetzt.",
  "В действующем прайс-листе застройщика для каждой виллы указан месяц сдачи: октябрь 2027 года для Villa 05, ноябрь 2027 года для Villa 03, январь 2028 года для Villa 07 и февраль 2028 года для вилл 02 и 06. В более ранних материалах застройщика значился март 2026 года; его заменяет действующий список.",
  "تذكر قائمة أسعار المطور الحالية شهر تسليم لكل فيلا: أكتوبر 2027 للفيلا 05، ونوفمبر 2027 للفيلا 03، ويناير 2028 للفيلا 07، وفبراير 2028 للفيلتين 02 و06. وكانت مواد سابقة للمطور تذكر مارس 2026، وتحل محله القائمة الحالية.",
  "De huidige prijslijst van de ontwikkelaar geeft voor elke villa een opleveringsmaand: oktober 2027 voor Villa 05, november 2027 voor Villa 03, januari 2028 voor Villa 07 en februari 2028 voor Villa 02 en 06. Eerder materiaal van de ontwikkelaar gaf maart 2026, dat de huidige lijst vervangt.",
  "Obecna lista cen dewelopera podaje miesiąc odbioru każdej willi: październik 2027 roku dla Willi 05, listopad 2027 roku dla Willi 03, styczeń 2028 roku dla Willi 07 i luty 2028 roku dla Willi 02 i 06. Wcześniejsze materiały dewelopera podawały marzec 2026 roku, który zastępuje obecna lista.",
  "Utviklerens gjeldende prisliste oppgir en overleveringsmåned for hver villa: oktober 2027 for Villa 05, november 2027 for Villa 03, januar 2028 for Villa 07 og februar 2028 for Villa 02 og 06. Tidligere materiale fra utvikleren oppga mars 2026, som den gjeldende listen erstatter.",
  "Byggherrens nuvarande prislista anger en leveransmånad för varje villa: oktober 2027 för Villa 05, november 2027 för Villa 03, januari 2028 för Villa 07 och februari 2028 för Villa 02 och 06. Tidigare material från byggherren angav mars 2026, vilket den nuvarande listan ersätter.")
a(173, 'Is the solarium included?',
  "¿Está incluido el solárium?", "Le solarium est-il inclus ?", "Ist das Solarium inbegriffen?", "Входит ли солярий в стоимость?",
  "هل السولاريوم مشمول؟", "Is het solarium inbegrepen?", "Czy solarium jest w cenie?", "Er solterrassen inkludert?", "Ingår solterrassen?")
a(174, 'Yes. Each villa has a rooftop solarium of 49 to 95 sqm',
  "Sí. Cada villa tiene un solárium en la azotea de entre {N49} y {N95} {U}, al que se sube por una escalera cubierta, con ducha, armario trastero y preinstalación para un jacuzzi. El jacuzzi en sí no está incluido.",
  "Oui. Chaque villa dispose d'un solarium sur le toit de {N49} à {N95} {U}, accessible par un escalier couvert, avec douche, placard de rangement et pré-équipement pour un spa. Le spa lui-même n'est pas inclus.",
  "Ja. Jede Villa hat ein Dach-Solarium von {N49} bis {N95} {U}, erreichbar über eine überdachte Treppe, mit Dusche, Schrank und Vorinstallation für einen Whirlpool. Der Whirlpool selbst ist nicht enthalten.",
  "Да. У каждой виллы есть солярий на крыше площадью от {N49} до {N95} {U}, на который ведёт крытая лестница; там есть душ, шкаф для хранения и подготовка под джакузи. Само джакузи в стоимость не входит.",
  "نعم. لكل فيلا سولاريوم على السطح تتراوح مساحته بين {N49} و{N95} {U}، يُصعد إليه بدرج مغطى، ويضم دشًا وخزانة تخزين وتجهيزًا مسبقًا لجاكوزي. والجاكوزي نفسه غير مشمول.",
  "Ja. Elke villa heeft een solarium op het dak van {N49} tot {N95} {U}, bereikbaar via een overdekte trap, met douche, bergkast en voorbereiding voor een bubbelbad. Het bubbelbad zelf is niet inbegrepen.",
  "Tak. Każda willa ma solarium na dachu o powierzchni od {N49} do {N95} {U}, na które prowadzą zadaszone schody; jest w nim prysznic, szafa gospodarcza i instalacja pod jacuzzi. Samo jacuzzi nie jest w cenie.",
  "Ja. Hver villa har en solterrasse på taket på {N49} til {N95} {U}, som nås via en overbygd trapp, med dusj, oppbevaringsskap og forberedelse for boblebad. Selve boblebadet er ikke inkludert.",
  "Ja. Varje villa har en solterrass på taket på {N49} till {N95} {U}, som nås via en övertäckt trappa, med dusch, förvaringsskåp och förberedelse för bubbelpool. Själva bubbelpoolen ingår inte.")
a(175, 'Where is the parking?',
  "¿Dónde está el aparcamiento?", "Où se trouve le stationnement ?", "Wo sind die Stellplätze?", "Где находится парковка?",
  "أين المواقف؟", "Waar is het parkeren?", "Gdzie jest parking?", "Hvor er parkeringen?", "Var finns parkeringen?")
a(176, 'Villas 02, 03, 05 and 06 have a basement garage',
  "Las villas 02, 03, 05 y 06 tienen un garaje en el sótano para dos coches. La Villa 07 tiene dos plazas en superficie bajo una pérgola, según los planos y la circular informativa de la promotora, mientras que el folleto de la promotora describe una villa con una plaza en el sótano y otra fuera. Confirmamos la Villa 07 por escrito.",
  "Les villas 02, 03, 05 et 06 ont un garage au sous-sol pour deux voitures. La Villa 07 a deux places en surface sous une pergola, d'après les plans et la circulaire d'information du promoteur, tandis que la brochure du promoteur décrit une villa avec une place au sous-sol et une à l'extérieur. Nous confirmons la Villa 07 par écrit.",
  "Die Villen 02, 03, 05 und 06 haben eine Garage im Untergeschoss für zwei Autos. Villa 07 hat laut Plänen und Informationsschreiben des Bauträgers zwei oberirdische Stellplätze unter einer Pergola, während die Broschüre des Bauträgers eine Villa mit einem Stellplatz im Untergeschoss und einem draußen beschreibt. Wir bestätigen Villa 07 schriftlich.",
  "У вилл 02, 03, 05 и 06 есть гараж в цоколе на две машины. У Villa 07, согласно планировкам и информационному письму застройщика, два места на поверхности под перголой, тогда как в брошюре застройщика описана вилла с одним местом в цоколе и одним снаружи. Мы подтверждаем Villa 07 в письменном виде.",
  "للفلل 02 و03 و05 و06 مرآب في القبو يتسع لسيارتين. أما الفيلا 07 فلها موقفان على السطح تحت برغولا بحسب المخططات وتعميم المطور، بينما يصف كتيّب المطور فيلا بموقف واحد في القبو وآخر في الخارج. ونؤكد وضع الفيلا 07 كتابةً.",
  "Villa 02, 03, 05 en 06 hebben een garage in de kelder voor twee auto's. Villa 07 heeft volgens de plattegronden en de informatiebrief van de ontwikkelaar twee plaatsen op het maaiveld onder een pergola, terwijl de brochure van de ontwikkelaar een villa beschrijft met één plaats in de kelder en één buiten. Wij bevestigen Villa 07 schriftelijk.",
  "Wille 02, 03, 05 i 06 mają garaż w piwnicy na dwa samochody. Willa 07 ma według rzutów i pisma informacyjnego dewelopera dwa miejsca na powierzchni pod pergolą, podczas gdy broszura dewelopera opisuje willę z jednym miejscem w piwnicy i jednym na zewnątrz. Willę 07 potwierdzamy na piśmie.",
  "Villa 02, 03, 05 og 06 har garasje i kjelleren for to biler. Villa 07 har ifølge plantegningene og utviklerens informasjonsskriv to plasser på bakkeplan under en pergola, mens utviklerens brosjyre beskriver en villa med én plass i kjelleren og én utenfor. Vi bekrefter Villa 07 skriftlig.",
  "Villa 02, 03, 05 och 06 har garage i källaren för två bilar. Villa 07 har enligt planritningarna och byggherrens informationsbrev två platser på marknivå under en pergola, medan byggherrens broschyr beskriver en villa med en plats i källaren och en utanför. Vi bekräftar Villa 07 skriftligt.")
a(177, 'Is each plot private?',
  "¿Es privada cada parcela?", "Chaque parcelle est-elle privée ?", "Ist jedes Grundstück privat?", "Является ли каждый участок частным?",
  "هل كل قطعة أرض خاصة؟", "Is elk perceel privé?", "Czy każda działka jest prywatna?", "Er hver tomt privat?", "Är varje tomt privat?")
a(178, 'Each villa stands on its own walled plot',
  "Cada villa se levanta en su propia parcela vallada, con jardín privado y acceso propio. Las parcelas comparten muros medianeros con las vecinas y pertenecen a la entidad de conservación de la urbanización de la zona.",
  "Chaque villa se dresse sur sa propre parcelle close, avec jardin privé et accès propre. Les parcelles partagent des murs mitoyens avec leurs voisines et relèvent de l'association de gestion de la résidence du secteur.",
  "Jede Villa steht auf einem eigenen, ummauerten Grundstück mit privatem Garten und eigener Zufahrt. Die Grundstücke haben Grenzmauern mit den Nachbarn gemeinsam und gehören zur Erhaltungsgemeinschaft der Wohnanlage des Gebiets.",
  "Каждая вилла стоит на собственном огороженном участке с частным садом и отдельным въездом. Участки имеют общие стены с соседними и входят в организацию по содержанию жилого массива района.",
  "تقوم كل فيلا على قطعة أرض مسوّرة خاصة بها، مع حديقة خاصة ومدخل مستقل. تشترك القطع في جدران فاصلة مع جاراتها وتنتمي إلى هيئة صيانة المجمع السكني في المنطقة.",
  "Elke villa staat op een eigen ommuurd perceel met een privétuin en een eigen toegang. De percelen delen scheidingsmuren met hun buren en behoren tot de onderhoudsvereniging van de urbanisatie in het gebied.",
  "Każda willa stoi na własnej ogrodzonej działce z prywatnym ogrodem i własnym wjazdem. Działki mają wspólne mury z sąsiednimi i należą do organizacji utrzymującej osiedle w tej okolicy.",
  "Hver villa står på sin egen inngjerdede tomt med privat hage og egen adkomst. Tomtene deler skillemurer med naboene og tilhører områdets vedlikeholdsforening for boligområdet.",
  "Varje villa står på sin egen inhägnade tomt med privat trädgård och egen tillfart. Tomterna delar skiljemurar med grannarna och tillhör områdets samfällighet för underhåll av bostadsområdet.")

# ---------------------------------------------------------------- write
missing = [i for i, en in enumerate(todo) if en not in T]
assert not missing, f'not translated: {missing}'
json.dump(T, open(f'{SP}/import/tr_z.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')

# ---------------------------------------------------------------- architecture.highlights
# overlay_shape has no `highlights` key, so scaffold/assemble leave these in English;
# they are translated here and written straight into the overlays after assemble.py.
H = {
 'Facades': ("Fachadas", "Façades", "Fassaden", "Фасады", "الواجهات", "Gevels", "Elewacje", "Fasader", "Fasader"),
 'White cement render and paint, with cladding panels and exterior screens in a timber-effect finish.':
  ("Enfoscado y pintura de cemento blanco, con paneles de revestimiento y celosías exteriores de acabado imitación madera.",
   "Enduit et peinture de ciment blanc, avec panneaux de bardage et claustras extérieurs à finition aspect bois.",
   "Weißer Zementputz und Anstrich, mit Verkleidungspaneelen und Sichtschutzelementen außen in Holzoptik.",
   "Белая цементная штукатурка и покраска, облицовочные панели и наружные экраны с отделкой под дерево.",
   "لياسة إسمنت أبيض ودهان، مع ألواح كسوة وستائر مشبّكة خارجية بتشطيب يحاكي الخشب.",
   "Witte cementstuc en verf, met gevelpanelen en buitenschermen in houtlook-afwerking.",
   "Biały tynk cementowy i malowanie, z panelami okładzinowymi i ekranami zewnętrznymi w wykończeniu imitującym drewno.",
   "Hvit sementpuss og maling, med kledningspaneler og utvendige skjermer i tre-effekt.",
   "Vit cementputs och färg, med fasadpaneler och yttre skärmar i trälook."),
 'Pergolas with timber-effect beams, and masonry and glass balustrades facing the pool and garden.':
  ("Pérgolas con vigas imitación madera, y barandillas de obra y de cristal hacia la piscina y el jardín.",
   "Pergolas à poutres aspect bois, et garde-corps en maçonnerie et en verre face à la piscine et au jardin.",
   "Pergolen mit Balken in Holzoptik sowie Brüstungen aus Mauerwerk und Glas zu Pool und Garten hin.",
   "Перголы с балками под дерево и ограждения из кладки и стекла, обращённые к бассейну и саду.",
   "برغولات بعوارض محاكية للخشب، ودرابزينات من البناء والزجاج تطل على المسبح والحديقة.",
   "Pergola's met balken in houtlook, en balustrades van metselwerk en glas richting het zwembad en de tuin.",
   "Pergole z belkami imitującymi drewno oraz murowane i szklane balustrady zwrócone w stronę basenu i ogrodu.",
   "Pergolaer med bjelker i tre-effekt, og rekkverk i murverk og glass mot bassenget og hagen.",
   "Pergolor med bjälkar i trälook, och räcken av murverk och glas mot poolen och trädgården."),
 'Light and air': ("Luz y aire", "Lumière et air", "Licht und Luft", "Свет и воздух", "الضوء والهواء", "Licht en lucht", "Światło i powietrze", "Lys og luft", "Ljus och luft"),
 'Large openings in the living room and bedrooms, and cross ventilation through the house.':
  ("Grandes aberturas en el salón y los dormitorios, y ventilación cruzada por toda la casa.",
   "De grandes ouvertures dans le séjour et les chambres, et une ventilation traversante dans toute la maison.",
   "Große Öffnungen in Wohnzimmer und Schlafzimmern und Querlüftung durch das ganze Haus.",
   "Большие проёмы в гостиной и спальнях и сквозное проветривание по всему дому.",
   "فتحات كبيرة في غرفة المعيشة وغرف النوم، وتهوية متقاطعة في أرجاء المنزل.",
   "Grote openingen in de woonkamer en de slaapkamers, en kruisventilatie door het hele huis.",
   "Duże otwory w salonie i sypialniach oraz przewietrzanie przez cały dom.",
   "Store åpninger i stuen og soverommene, og gjennomlufting i hele huset.",
   "Stora öppningar i vardagsrummet och sovrummen, och genomluftning i hela huset."),
 'Every villa faces south, with the main rooms looking onto the garden.':
  ("Todas las villas miran al sur, con las estancias principales orientadas al jardín.",
   "Toutes les villas sont orientées au sud, avec les pièces principales donnant sur le jardin.",
   "Alle Villen sind nach Süden ausgerichtet, die Haupträume öffnen sich zum Garten.",
   "Все виллы ориентированы на юг, основные комнаты выходят в сад.",
   "تتجه جميع الفلل نحو الجنوب، وتطل الغرف الرئيسية على الحديقة.",
   "Alle villa's liggen op het zuiden, met de hoofdvertrekken gericht op de tuin.",
   "Wszystkie wille są zwrócone na południe, a główne pomieszczenia wychodzą na ogród.",
   "Alle villaene vender mot sør, med hovedrommene mot hagen.",
   "Alla villor vetter mot söder, med huvudrummen mot trädgården."),
}
tm_words = json.load(open(f'{SP}/import/tm.json'))
P = 'content/liora-projects/atalaya-pool-villas/project.json'
proj = json.load(open(P))
for l_i, l in enumerate(LOCS):
    hl = proj['i18n'][l]['architecture']['highlights']
    for row, src in zip(hl, proj['architecture']['highlights']):
        for col in (0, 1):
            tr = H.get(src[col])
            if tr is not None:
                row[col] = tr[l_i]
            elif src[col] in tm_words:     # 'Terraces', 'Orientation': already translated elsewhere
                row[col] = tm_words[src[col]][l]
# Unit references stay English in every overlay (localizedUnitFloor() translates them at
# render time); assemble.py's Villa NN rule would otherwise rewrite them for ru, ar, pl.
for l in LOCS:
    ov = proj['i18n'][l]
    for row, src in zip(ov['residences']['items'], proj['residences']['items']):
        row['name'] = src['name']
    for row, src in zip(ov['availability']['units'], proj['availability']['units']):
        row['reference'] = src['reference']
json.dump(proj, open(P, 'w'), ensure_ascii=False, indent=2)
open(P, 'a').write('\n')
print('highlights written')
