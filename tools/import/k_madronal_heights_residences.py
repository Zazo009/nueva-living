# -*- coding: utf-8 -*-
"""Madroñal Heights Residences: the strings the translation memory did not have.

Same shape as k_selwo_garden_residences.py: keyed by the path of the English string in
project.json (looked up here, never retyped) and written to tr_m.json keyed by the English string,
as assemble.py expects. Unit sizes are built from one template per locale, the words Selwo Garden
Residences already publishes plus the solarium (sv "solterrass", no "solterrasse").
Floor labels ("Phase III, Block 4, Ground Floor") are left to assemble.py: it builds them from
floor_parts.json, which needs the "phase" prefix that scripts/lib/unit_floor_parts.mjs carries.
Tokens: {E999000} money, {N218.79} decimal number, {U} the area unit, {T} the tax word.
    python3 tools/import/k_madronal_heights_residences.py <scratch dir>   (writes <dir>/tr_m.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة',
        'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
T = {}
SLUG = 'madronal-heights-residences'
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


same(get('.name')); same(get('.shortName')); same(get('.titleHtml'))

# ---- units: the reference is the developer's own numbering; sizes from one template --------------
SIZE = {  # built, usable, terrace, garden, solarium
    'es': ('construido', 'superficie útil', 'terraza', 'jardín', 'solárium'),
    'fr': ('construit', 'surface utile', 'terrasse', 'jardin', 'solarium'),
    'de': ('bebaut', 'Wohnfläche', 'Terrasse', 'Garten', 'Solarium'),
    'ru': ('застройка', 'полезная площадь', 'терраса', 'сад', 'солярий'),
    'ar': ('مبنية', 'مساحة صافية', 'تراس', 'حديقة', 'سولاريوم'),
    'nl': ('bebouwd', 'nuttige oppervlakte', 'terras', 'tuin', 'solarium'),
    'pl': ('powierzchnia zabudowy', 'powierzchnia użytkowa', 'taras', 'ogród', 'solarium'),
    'no': ('bebygd areal', 'bruksareal', 'terrasse', 'hage', 'solterrasse'),
    'sv': ('byggyta', 'nyttoyta', 'terrass', 'trädgård', 'solterrass'),
}
KIND = ['built', 'usable', 'terrace', 'garden', 'solarium']
for u in proj['availability']['units']:
    same(u['reference'])
    parts = []
    for seg in u['size'].split(', '):
        m = re.fullmatch(r'([\d.]+) sqm (built|usable|terrace|garden|solarium)', seg)
        assert m, u['size']
        parts.append((m.group(1), KIND.index(m.group(2))))
    T[u['size']] = {l: ('، ' if l == 'ar' else ', ').join(f'{num(v, l)} {UNIT[l]} {SIZE[l][k]}' for v, k in parts)
                    for l in LOCS}

# ---- everything else, in the order of project.json ------------------------------------------------

a('.description',
  'Veinte apartamentos y áticos disponibles en una ladera de Benahavís, sobre Golf Valley, en un conjunto de tres fases: cuatro viviendas llave en mano en la primera fase, ya terminada, dos de ellas en su edificio circular, y dieciséis en las dos fases posteriores, en construcción, de dos a cuatro dormitorios, desde {E999000} + {T}.',
  'Vingt appartements et attiques disponibles sur un coteau de Benahavís, au-dessus de Golf Valley, dans une résidence en trois phases : quatre logements clés en main dans la première phase, achevée, dont deux dans son bâtiment circulaire, et seize dans les deux phases suivantes, en construction, de deux à quatre chambres, à partir de {E999000} + {T}.',
  'Zwanzig verfügbare Wohnungen und Penthäuser an einem Hang in Benahavís oberhalb von Golf Valley, in einer Anlage mit drei Bauabschnitten: vier schlüsselfertige Wohnungen in der fertiggestellten ersten Phase, zwei davon im runden Gebäude, und sechzehn in den beiden späteren Phasen im Bau, mit zwei bis vier Schlafzimmern, ab {E999000} + {T}.',
  'Двадцать свободных апартаментов и пентхаусов на склоне холма в Бенаависе над Гольф-долиной, в комплексе из трёх очередей: четыре квартиры, готовые к заселению, в завершённой первой очереди, в том числе две в её круглом здании, и шестнадцать в двух строящихся очередях, с двумя–четырьмя спальнями, от {E999000} + {T}.',
  'عشرون شقة وبنتهاوس متاحة على سفح تلّ في بيناهافيس فوق وادي الغولف، ضمن مجمع من ثلاث مراحل: أربعة مساكن جاهزة للتسليم في المرحلة الأولى المكتملة، منها اثنان في مبناها الدائري، وستة عشر مسكنًا في المرحلتين اللاحقتين قيد الإنشاء، من غرفتي نوم إلى أربع غرف، ابتداءً من {E999000} + {T}.',
  'Twintig beschikbare appartementen en penthouses op een heuvel in Benahavís boven Golf Valley, in een project van drie fasen: vier sleutelklare woningen in de voltooide eerste fase, waarvan twee in het ronde gebouw, en zestien in de twee latere fasen die in aanbouw zijn, met twee tot vier slaapkamers, vanaf {E999000} + {T}.',
  "Dwadzieścia dostępnych apartamentów i penthouse'ów na zboczu wzgórza w Benahavís nad Golf Valley, w inwestycji realizowanej w trzech etapach: cztery mieszkania gotowe do odbioru w ukończonym pierwszym etapie, w tym dwa w jego okrągłym budynku, oraz szesnaście w dwóch kolejnych etapach w budowie, z dwiema do czterech sypialni, od {E999000} + {T}.",
  'Tjue ledige leiligheter og toppleiligheter i en åsside i Benahavís over Golf Valley, i et prosjekt i tre byggetrinn: fire innflyttingsklare boliger i det ferdige første byggetrinnet, hvorav to i den runde bygningen, og seksten i de to senere byggetrinnene, som er under bygging, med to til fire soverom, fra {E999000} + {T}.',
  'Tjugo lediga lägenheter och takvåningar på en sluttning i Benahavís ovanför Golf Valley, i ett projekt i tre etapper: fyra inflyttningsklara bostäder i den färdiga första etappen, varav två i den runda byggnaden, och sexton i de två senare etapperna som är under uppförande, med två till fyra sovrum, från {E999000} + {T} (spansk moms).')

a('.seoDescription',
  'Veinte apartamentos y áticos sobre Golf Valley, Benahavís: cuatro llave en mano, dieciséis en construcción, de 2 a 4 dormitorios, piscinas y health club.',
  'Vingt appartements et attiques au-dessus de Golf Valley, Benahavís : quatre clés en main, seize en construction, 2 à 4 chambres, piscines et club de santé.',
  'Zwanzig Wohnungen und Penthäuser über Golf Valley, Benahavís: vier schlüsselfertig, sechzehn im Bau, 2 bis 4 Schlafzimmer, Pools und Health Club.',
  'Двадцать апартаментов и пентхаусов над Гольф-долиной, Бенаавис: четыре готовы к заселению, шестнадцать строятся, 2–4 спальни, бассейны и оздоровительный клуб.',
  'عشرون شقة وبنتهاوس فوق وادي الغولف، بيناهافيس: أربعة جاهزة للتسليم وستة عشر قيد الإنشاء، من 2 إلى 4 غرف نوم، مع مسابح ونادٍ صحي.',
  'Twintig appartementen en penthouses boven Golf Valley, Benahavís: vier sleutelklaar, zestien in aanbouw, 2 tot 4 slaapkamers, zwembaden en een health club.',
  "Dwadzieścia apartamentów i penthouse'ów nad Golf Valley, Benahavís: cztery gotowe do odbioru, szesnaście w budowie, 2–4 sypialnie, baseny i klub zdrowia.",
  'Tjue leiligheter og toppleiligheter over Golf Valley, Benahavís: fire innflyttingsklare, seksten under bygging, 2 til 4 soverom, bassenger og helseklubb.',
  'Tjugo lägenheter och takvåningar ovanför Golf Valley, Benahavís: fyra inflyttningsklara, sexton under uppförande, 2 till 4 sovrum, pooler och hälsoklubb.')

a('.twitterDescription',
  'Apartamentos y áticos sobre Golf Valley, en Benahavís: una primera fase terminada con viviendas llave en mano y dos fases posteriores en construcción. Desde {E999000} + {T}.',
  'Appartements et attiques au-dessus de Golf Valley, à Benahavís : une première phase achevée avec des logements clés en main et deux phases suivantes en construction. À partir de {E999000} + {T}.',
  'Wohnungen und Penthäuser oberhalb von Golf Valley in Benahavís: eine fertiggestellte erste Phase mit schlüsselfertigen Wohnungen und zwei spätere Phasen im Bau. Ab {E999000} + {T}.',
  'Апартаменты и пентхаусы над Гольф-долиной в Бенаависе: завершённая первая очередь с квартирами, готовыми к заселению, и две строящиеся очереди. От {E999000} + {T}.',
  'شقق وبنتهاوس فوق وادي الغولف في بيناهافيس: مرحلة أولى مكتملة بمساكن جاهزة للتسليم، ومرحلتان لاحقتان قيد الإنشاء. ابتداءً من {E999000} + {T}.',
  'Appartementen en penthouses boven Golf Valley in Benahavís: een voltooide eerste fase met sleutelklare woningen en twee latere fasen in aanbouw. Vanaf {E999000} + {T}.',
  "Apartamenty i penthouse'y nad Golf Valley w Benahavís: ukończony pierwszy etap z mieszkaniami gotowymi do odbioru i dwa kolejne etapy w budowie. Od {E999000} + {T}.",
  'Leiligheter og toppleiligheter over Golf Valley i Benahavís: et ferdig første byggetrinn med innflyttingsklare boliger og to senere byggetrinn under bygging. Fra {E999000} + {T}.',
  'Lägenheter och takvåningar ovanför Golf Valley i Benahavís: en färdig första etapp med inflyttningsklara bostäder och två senare etapper under uppförande. Från {E999000} + {T}.')

a('.hero.eyebrow',
  'Veinte viviendas disponibles / tres fases',
  'Vingt logements disponibles / trois phases',
  'Zwanzig Wohnungen verfügbar / drei Phasen',
  'Двадцать квартир в продаже / три очереди',
  'عشرون مسكنًا متاحًا / ثلاث مراحل',
  'Twintig woningen beschikbaar / drie fasen',
  'Dwadzieścia dostępnych mieszkań / trzy etapy',
  'Tjue boliger ledige / tre byggetrinn',
  'Tjugo bostäder lediga / tre etapper')

a('.hero.location',
  'Sobre Golf Valley, Benahavís',
  'Au-dessus de Golf Valley, Benahavís',
  'Oberhalb von Golf Valley, Benahavís',
  'Над Гольф-долиной, Бенаавис',
  'فوق وادي الغولف، بيناهافيس',
  'Boven Golf Valley, Benahavís',
  'Nad Golf Valley, Benahavís',
  'Over Golf Valley, Benahavís',
  'Ovanför Golf Valley, Benahavís')

a('.hero.startingPrice',
  'Desde {E999000} + {T}',
  'À partir de {E999000} + {T}',
  'Ab {E999000} + {T}',
  'От {E999000} + {T}',
  'ابتداءً من {E999000} + {T}',
  'Vanaf {E999000} + {T}',
  'Od {E999000} + {T}',
  'Fra {E999000} + {T}',
  'Från {E999000} + {T}')

a('.hero.delivery',
  'Fase I llave en mano',
  'Phase I clés en main',
  'Phase I schlüsselfertig',
  'Очередь I готова к заселению',
  'المرحلة I جاهزة للتسليم',
  'Fase I sleutelklaar',
  'Etap I gotowy do odbioru',
  'Byggetrinn I innflyttingsklart',
  'Etapp I inflyttningsklar')

a('.card.description',
  'Veinte apartamentos y áticos sobre Golf Valley, en Benahavís, cuatro de ellos llave en mano en una primera fase terminada con piscinas y health club, y dieciséis en dos fases en construcción, desde {E999000} + {T}.',
  'Vingt appartements et attiques au-dessus de Golf Valley, à Benahavís, dont quatre clés en main dans une première phase achevée avec piscines et club de santé, et seize dans deux phases en construction, à partir de {E999000} + {T}.',
  'Zwanzig Wohnungen und Penthäuser oberhalb von Golf Valley in Benahavís, vier davon schlüsselfertig in einer fertiggestellten ersten Phase mit Pools und Health Club, sechzehn in zwei Phasen im Bau, ab {E999000} + {T}.',
  'Двадцать апартаментов и пентхаусов над Гольф-долиной в Бенаависе: четыре готовы к заселению в завершённой первой очереди с бассейнами и оздоровительным клубом, шестнадцать — в двух строящихся очередях, от {E999000} + {T}.',
  'عشرون شقة وبنتهاوس فوق وادي الغولف في بيناهافيس، أربعة منها جاهزة للتسليم في مرحلة أولى مكتملة تضم مسابح ونادياً صحياً، وستة عشر في مرحلتين قيد الإنشاء، ابتداءً من {E999000} + {T}.',
  'Twintig appartementen en penthouses boven Golf Valley in Benahavís, waarvan vier sleutelklaar in een voltooide eerste fase met zwembaden en een health club, en zestien in twee fasen in aanbouw, vanaf {E999000} + {T}.',
  "Dwadzieścia apartamentów i penthouse'ów nad Golf Valley w Benahavís: cztery gotowe do odbioru w ukończonym pierwszym etapie z basenami i klubem zdrowia, szesnaście w dwóch etapach w budowie, od {E999000} + {T}.",
  'Tjue leiligheter og toppleiligheter over Golf Valley i Benahavís, fire av dem innflyttingsklare i et ferdig første byggetrinn med bassenger og helseklubb, seksten i to byggetrinn under bygging, fra {E999000} + {T}.',
  'Tjugo lägenheter och takvåningar ovanför Golf Valley i Benahavís, fyra av dem inflyttningsklara i en färdig första etapp med pooler och hälsoklubb, sexton i två etapper under uppförande, från {E999000} + {T}.')

a('.card.meta[0][1]',
  '{E999000} + {T}',
  '{E999000} + {T}',
  '{E999000} + {T}',
  '{E999000} + {T}',
  '{E999000} + {T}',
  '{E999000} + {T}',
  '{E999000} + {T}',
  '{E999000} + {T}',
  '{E999000} + {T}')

a('.quickFacts[6][1]',
  'Fase I llave en mano; fases II y III en construcción',
  'Phase I clés en main ; phases II et III en construction',
  'Phase I schlüsselfertig; Phasen II und III im Bau',
  'Очередь I готова к заселению; очереди II и III строятся',
  'المرحلة I جاهزة للتسليم، والمرحلتان II وIII قيد الإنشاء',
  'Fase I sleutelklaar; Fase II en III in aanbouw',
  'Etap I gotowy do odbioru; etapy II i III w budowie',
  'Byggetrinn I innflyttingsklart; byggetrinn II og III under bygging',
  'Etapp I inflyttningsklar; etapp II och III under uppförande')

a('.images.hero.alt',
  'Fotografía de la primera fase terminada: bloques blancos con terrazas curvas escalonados en la ladera, con las montañas detrás',
  'Photographie de la première phase achevée : des immeubles blancs aux terrasses courbes étagés sur le coteau, les montagnes en arrière-plan',
  'Foto der fertiggestellten ersten Phase: weiße Gebäude mit geschwungenen Terrassen, am Hang gestaffelt, dahinter die Berge',
  'Фотография завершённой первой очереди: белые корпуса с изогнутыми террасами уступами поднимаются по склону, позади горы',
  'صورة فوتوغرافية للمرحلة الأولى المكتملة: مبانٍ بيضاء بتراسات منحنية متدرجة على سفح التل، والجبال خلفها',
  'Foto van de voltooide eerste fase: witte blokken met gebogen terrassen die trapsgewijs tegen de heuvel oplopen, met de bergen erachter',
  'Zdjęcie ukończonego pierwszego etapu: białe budynki z zaokrąglonymi tarasami tarasowo wspinające się po zboczu, w tle góry',
  'Foto av det ferdige første byggetrinnet: hvite bygg med buede terrasser trappet oppover åssiden, med fjellene bak',
  'Foto av den färdiga första etappen: vita hus med svängda terrasser i trappsteg uppför sluttningen, med bergen bakom')

a('.images.architecture.alt',
  'Fotografía de un bloque terminado de la primera fase, con amplias terrazas curvas sobre la ladera ajardinada',
  'Photographie d’un immeuble achevé de la première phase, avec de profondes terrasses courbes au-dessus du talus planté',
  'Foto eines fertiggestellten Gebäudes der ersten Phase mit tiefen, geschwungenen Terrassen über dem bepflanzten Hang',
  'Фотография готового корпуса первой очереди с глубокими изогнутыми террасами над озеленённым склоном',
  'صورة فوتوغرافية لمبنى مكتمل من المرحلة الأولى بتراسات منحنية عميقة فوق المنحدر المزروع',
  'Foto van een voltooid blok uit de eerste fase met diepe, gebogen terrassen boven de beplante helling',
  'Zdjęcie ukończonego budynku pierwszego etapu z głębokimi zaokrąglonymi tarasami nad zazielenionym zboczem',
  'Foto av et ferdig bygg i første byggetrinn med dype, buede terrasser over den beplantede skråningen',
  'Foto av ett färdigt hus i första etappen med djupa, svängda terrasser ovanför den planterade slänten')

a('.images.lifestyle.alt',
  'Fotografía de la terraza de un ático de la primera fase con sofás de exterior y la costa al fondo',
  'Photographie de la terrasse d’un attique de la première phase avec des canapés d’extérieur, la côte au loin',
  'Foto der Terrasse eines Penthouses der ersten Phase mit Outdoor-Sofas, dahinter die Küste',
  'Фотография террасы пентхауса первой очереди с уличными диванами, вдали побережье',
  'صورة فوتوغرافية لتراس بنتهاوس في المرحلة الأولى مع أرائك خارجية، والساحل في الأفق',
  'Foto van een penthouseterras uit de eerste fase met loungebanken, met de kust in de verte',
  "Zdjęcie tarasu penthouse'u z pierwszego etapu z sofami ogrodowymi, w oddali wybrzeże",
  'Foto av en takterrasse i første byggetrinn med utesofaer, med kysten i bakgrunnen',
  'Foto av en takvåningsterrass i första etappen med utesoffor, med kusten i fjärran')

a('.images.privateViewing.alt',
  'Fotografía de una mesa de comedor redonda en la terraza del ático V1-312, con vistas sobre el valle hasta el mar',
  'Photographie d’une table ronde sur la terrasse de l’attique V1-312, avec vue sur la vallée jusqu’à la mer',
  'Foto eines runden Esstischs auf der Terrasse des Penthouses V1-312 mit Blick über das Tal bis zum Meer',
  'Фотография круглого обеденного стола на террасе пентхауса V1-312 с видом на долину и море',
  'صورة فوتوغرافية لطاولة طعام مستديرة على تراس البنتهاوس V1-312، مطلّة على الوادي والبحر',
  'Foto van een ronde eettafel op het terras van penthouse V1-312, met uitzicht over het dal naar zee',
  "Zdjęcie okrągłego stołu jadalnego na tarasie penthouse'u V1-312 z widokiem na dolinę i morze",
  'Foto av et rundt spisebord på terrassen til toppleilighet V1-312, med utsikt over dalen mot havet',
  'Foto av ett runt matbord på terrassen till takvåning V1-312, med utsikt över dalen mot havet')

a('.media.headlineHtml',
  'Tres fases en <em>imágenes</em>',
  'Trois phases en <em>images</em>',
  'Drei Phasen in <em>Bildern</em>',
  'Три очереди <em>в фотографиях</em>',
  'ثلاث مراحل <em>بالصور</em>',
  'Drie fasen in <em>beeld</em>',
  'Trzy etapy <em>na zdjęciach</em>',
  'Tre byggetrinn i <em>bilder</em>',
  'Tre etapper i <em>bilder</em>')

a('.media.copy',
  'Fotografías de la primera fase terminada, de su edificio circular, de sus piscinas y su health club y de viviendas amuebladas, y los renders de la promotora de las dos fases en construcción.',
  'Photographies de la première phase achevée, de son bâtiment circulaire, de ses piscines, de son club de santé et de logements meublés, ainsi que les images de synthèse du promoteur pour les deux phases en construction.',
  'Fotos der fertiggestellten ersten Phase, ihres runden Gebäudes, ihrer Pools, ihres Health Clubs und möblierter Wohnungen sowie die Visualisierungen des Bauträgers für die beiden Phasen im Bau.',
  'Фотографии завершённой первой очереди, её круглого здания, бассейнов, оздоровительного клуба и меблированных квартир, а также визуализации застройщика для двух строящихся очередей.',
  'صور فوتوغرافية للمرحلة الأولى المكتملة ومبناها الدائري ومسابحها وناديها الصحي ومساكنها المفروشة، وتصورات المطوّر للمرحلتين قيد الإنشاء.',
  'Foto’s van de voltooide eerste fase, het ronde gebouw, de zwembaden, de health club en ingerichte woningen, en renders van de ontwikkelaar van de twee fasen in aanbouw.',
  'Zdjęcia ukończonego pierwszego etapu, jego okrągłego budynku, basenów, klubu zdrowia i umeblowanych mieszkań oraz wizualizacje dewelopera dla dwóch etapów w budowie.',
  'Foto av det ferdige første byggetrinnet, den runde bygningen, bassengene, helseklubben og møblerte boliger, og utbyggerens illustrasjoner av de to byggetrinnene under bygging.',
  'Foton av den färdiga första etappen, den runda byggnaden, poolerna, hälsoklubben och möblerade bostäder, samt exploatörens illustrationer av de två etapperna under uppförande.')

a('.media.note',
  'Cada imagen está identificada. Las fotografías muestran la primera fase terminada; varias de sus viviendas se amueblaron y decoraron para las fotos, y el mobiliario solo se incluye cuando la lista de precios lo indica. Los renders muestran las fases II y III, que aún están en construcción, y no son los edificios terminados. Los planos son las fichas de la propia promotora para cada vivienda, sin el logotipo, el nombre del proyecto, el plano de situación ni la tabla de viviendas vecinas; no son contractuales.',
  'Chaque image est légendée. Les photographies montrent la première phase achevée ; plusieurs de ses logements ont été meublés et décorés pour les prises de vue, et le mobilier n’est inclus que lorsque la liste de prix l’indique. Les images de synthèse montrent les phases II et III, encore en construction, et ne représentent pas les bâtiments achevés. Les plans sont les fiches du promoteur pour chaque logement, sans le logo, le nom du projet, le plan de situation ni le tableau des logements voisins ; ils ne sont pas contractuels.',
  'Jedes Bild ist gekennzeichnet. Die Fotos zeigen die fertiggestellte erste Phase; mehrere ihrer Wohnungen wurden für die Aufnahmen möbliert und dekoriert, und Möbel sind nur dann enthalten, wenn die Preisliste es angibt. Die Visualisierungen zeigen die Phasen II und III, die noch gebaut werden, und nicht die fertigen Gebäude. Die Grundrisse sind die eigenen Blätter des Bauträgers für jede Wohnung, ohne Logo, Projektnamen, Lageplan und die Tabelle der Nachbarwohnungen; sie sind nicht vertragsrelevant.',
  'Каждое изображение подписано. Фотографии показывают завершённую первую очередь; часть её квартир была обставлена и оформлена для съёмки, а мебель входит в цену только там, где это указано в прайс-листе. Визуализации показывают очереди II и III, которые ещё строятся, и не являются готовыми зданиями. Планировки — это собственные листы застройщика для каждой квартиры, с которых удалены логотип, название проекта, генплан и таблица соседних квартир; они не имеют договорной силы.',
  'كل صورة معنونة. تُظهر الصور الفوتوغرافية المرحلة الأولى المكتملة، وقد فُرش عدد من مساكنها ونُسّق خصيصًا للتصوير، ولا يُشمل الأثاث إلا حيث تنص قائمة الأسعار على ذلك. أما التصورات فتُظهر المرحلتين II وIII اللتين لا تزالان قيد البناء، وهي ليست المباني المنجزة. والمخططات هي أوراق المطوّر الخاصة بكل مسكن، بعد إزالة الشعار واسم المشروع والمخطط العام وجدول المساكن المجاورة، وهي غير ملزمة تعاقدياً.',
  'Elk beeld is gelabeld. De foto’s tonen de voltooide eerste fase; verschillende woningen zijn voor de foto’s ingericht en gestyled, en meubilair is alleen inbegrepen waar de prijslijst dat vermeldt. De renders tonen Fase II en III, die nog worden gebouwd, en zijn niet de afgewerkte gebouwen. De plattegronden zijn de eigen bladen van de ontwikkelaar per woning, zonder logo, projectnaam, situatietekening en tabel met naburige woningen; ze zijn niet contractueel.',
  'Każde zdjęcie jest podpisane. Zdjęcia pokazują ukończony pierwszy etap; kilka jego mieszkań zostało umeblowanych i zaaranżowanych na potrzeby sesji, a meble są wliczone tylko tam, gdzie mówi o tym cennik. Wizualizacje przedstawiają etapy II i III, które wciąż są w budowie, i nie są gotowymi budynkami. Rzuty to własne arkusze dewelopera dla każdego mieszkania, z usuniętym logo, nazwą projektu, planem sytuacyjnym i tabelą sąsiednich mieszkań; nie mają mocy umownej.',
  'Hvert bilde er merket. Fotografiene viser det ferdige første byggetrinnet; flere av boligene ble møblert og innredet for fotograferingen, og møbler følger bare med der prislisten sier det. Illustrasjonene viser byggetrinn II og III, som fortsatt bygges, og er ikke de ferdige byggene. Plantegningene er utbyggerens egne ark for hver bolig, med logo, prosjektnavn, situasjonsplan og tabellen over nabo-boligene fjernet; de er ikke kontraktsmessige.',
  'Varje bild är märkt. Fotona visar den färdiga första etappen; flera av bostäderna möblerades och stylades för fotograferingen, och möbler ingår bara där prislistan säger det. Illustrationerna visar etapp II och III, som fortfarande byggs, och är inte de färdiga husen. Planritningarna är exploatörens egna blad för varje bostad, utan logotyp, projektnamn, situationsplan och tabellen över grannbostäderna; de är inte kontraktsbindande.')

a('.media.video.title',
  'La primera fase, terminada',
  'La première phase, achevée',
  'Die erste Phase, fertiggestellt',
  'Первая очередь, завершённая',
  'المرحلة الأولى مكتملة',
  'De eerste fase, voltooid',
  'Pierwszy etap, ukończony',
  'Første byggetrinn, ferdig',
  'Första etappen, färdig')

a('.media.video.caption',
  'Imágenes de dron y a pie de la primera fase terminada, rodadas para la promotora: los bloques curvos, la piscina de 25 metros, las piscinas redondas, los jardines y las terrazas. Imágenes reales, sin sonido.',
  'Images de drone et au sol de la première phase achevée, tournées pour le promoteur : les immeubles courbes, la piscine de 25 mètres, les piscines rondes, les jardins et les terrasses. Images réelles, présentées sans le son.',
  'Drohnen- und Bodenaufnahmen der fertiggestellten ersten Phase, gedreht für den Bauträger: die geschwungenen Gebäude, der 25-Meter-Pool, die runden Pools, die Gärten und die Terrassen. Echte Aufnahmen, ohne Ton gezeigt.',
  'Съёмка с дрона и с земли завершённой первой очереди, снятая для застройщика: изогнутые корпуса, 25-метровый бассейн, круглые бассейны, сады и террасы. Реальная съёмка, показана без звука.',
  'لقطات جوية وأرضية للمرحلة الأولى المكتملة، صُوّرت لصالح المطوّر: المباني المنحنية، والمسبح بطول 25 متراً، والمسابح الدائرية، والحدائق والتراسات. لقطات حقيقية تُعرض دون صوت.',
  'Drone- en grondbeelden van de voltooide eerste fase, gefilmd voor de ontwikkelaar: de gebogen blokken, het zwembad van 25 meter, de ronde zwembaden, de tuinen en de terrassen. Echte beelden, getoond zonder geluid.',
  'Nagrania z drona i z ziemi ukończonego pierwszego etapu, wykonane dla dewelopera: zaokrąglone budynki, 25-metrowy basen, okrągłe baseny, ogrody i tarasy. Prawdziwe ujęcia, pokazane bez dźwięku.',
  'Drone- og bakkeopptak av det ferdige første byggetrinnet, filmet for utbyggeren: de buede byggene, det 25 meter lange bassenget, de runde bassengene, hagene og terrassene. Ekte opptak, vist uten lyd.',
  'Drönar- och markbilder av den färdiga första etappen, filmade för exploatören: de svängda husen, den 25 meter långa poolen, de runda poolerna, trädgårdarna och terrasserna. Verkliga bilder, visade utan ljud.')

a('.media.video.alt',
  'Vídeo de la primera fase terminada, desde el aire y a pie de calle',
  'Film de la première phase achevée, vue du ciel et depuis le sol',
  'Film der fertiggestellten ersten Phase aus der Luft und vom Boden',
  'Фильм о завершённой первой очереди с воздуха и с земли',
  'فيلم عن المرحلة الأولى المكتملة من الجو وعلى الأرض',
  'Film van de voltooide eerste fase vanuit de lucht en op de grond',
  'Film o ukończonym pierwszym etapie z powietrza i z ziemi',
  'Film av det ferdige første byggetrinnet fra luften og på bakken',
  'Film av den färdiga första etappen från luften och på marken')

a('.media.items[0].caption',
  'La primera fase, construida',
  'La première phase, construite',
  'Die erste Phase, gebaut',
  'Первая очередь, построенная',
  'المرحلة الأولى بعد إنجازها',
  'De eerste fase, gebouwd',
  'Pierwszy etap, zbudowany',
  'Første byggetrinn, bygget',
  'Första etappen, byggd')

a('.media.items[1].caption',
  'Terrazas curvas',
  'Terrasses courbes',
  'Geschwungene Terrassen',
  'Изогнутые террасы',
  'تراسات منحنية',
  'Gebogen terrassen',
  'Zaokrąglone tarasy',
  'Buede terrasser',
  'Svängda terrasser')

a('.media.items[2].alt',
  'Fotografía del edificio circular desde la terraza y el jardín de su vivienda en planta baja',
  'Photographie du bâtiment circulaire depuis la terrasse et le jardin de son logement en rez-de-chaussée',
  'Foto des runden Gebäudes von der Terrasse und dem Garten seiner Erdgeschosswohnung aus',
  'Фотография круглого здания с террасы и сада его квартиры на первом этаже',
  'صورة فوتوغرافية للمبنى الدائري من تراس وحديقة مسكنه في الطابق الأرضي',
  'Foto van het ronde gebouw vanaf het terras en de tuin van de woning op de begane grond',
  'Zdjęcie okrągłego budynku z tarasu i ogrodu mieszkania na parterze',
  'Foto av den runde bygningen fra terrassen og hagen til boligen i første etasje',
  'Foto av den runda byggnaden från terrassen och trädgården till bostaden på bottenvåningen')

a('.media.items[2].caption',
  'El edificio circular',
  'Le bâtiment circulaire',
  'Das runde Gebäude',
  'Круглое здание',
  'المبنى الدائري',
  'Het ronde gebouw',
  'Okrągły budynek',
  'Den runde bygningen',
  'Den runda byggnaden')

a('.media.items[3].alt',
  'Fotografía de dron de la terraza en cubierta del edificio circular durante una jornada de puertas abiertas, con su piscina y su pérgola',
  'Photographie de drone du toit-terrasse du bâtiment circulaire lors d’une journée portes ouvertes, avec sa piscine et sa pergola',
  'Drohnenfoto der Dachterrasse des runden Gebäudes während eines Tags der offenen Tür, mit Pool und Pergola',
  'Фотография с дрона: кровельная терраса круглого здания в день открытых дверей, с бассейном и перголой',
  'صورة جوية بطائرة مسيّرة لتراس سطح المبنى الدائري خلال يوم مفتوح، مع مسبحه وعريشته',
  'Dronefoto van het dakterras van het ronde gebouw tijdens een open dag, met het zwembad en de pergola',
  'Zdjęcie z drona: taras na dachu okrągłego budynku podczas dnia otwartego, z basenem i pergolą',
  'Dronefoto av takterrassen på den runde bygningen under en visningsdag, med basseng og pergola',
  'Drönarfoto av takterrassen på den runda byggnaden under en visningsdag, med pool och pergola')

a('.media.items[3].caption',
  'La terraza en cubierta del edificio circular',
  'Le toit-terrasse du bâtiment circulaire',
  'Die Dachterrasse des runden Gebäudes',
  'Кровельная терраса круглого здания',
  'تراس سطح المبنى الدائري',
  'Het dakterras van het ronde gebouw',
  'Taras na dachu okrągłego budynku',
  'Takterrassen på den runde bygningen',
  'Takterrassen på den runda byggnaden')

a('.media.items[4].alt',
  'Fotografía de dron tomada en vertical sobre la piscina curva y la tarima de la terraza en cubierta del edificio circular',
  'Photographie de drone prise à la verticale de la piscine courbe et du deck du toit-terrasse du bâtiment circulaire',
  'Drohnenfoto senkrecht von oben auf den geschwungenen Pool und das Deck der Dachterrasse des runden Gebäudes',
  'Фотография с дрона строго сверху: изогнутый бассейн и настил кровельной террасы круглого здания',
  'صورة جوية بطائرة مسيّرة من الأعلى مباشرةً للمسبح المنحني والأرضية الخشبية لتراس سطح المبنى الدائري',
  'Dronefoto recht van boven op het gebogen zwembad en het dek van het dakterras van het ronde gebouw',
  'Zdjęcie z drona prosto z góry: zaokrąglony basen i deck tarasu na dachu okrągłego budynku',
  'Dronefoto rett ovenfra av det buede bassenget og dekket på takterrassen til den runde bygningen',
  'Drönarfoto rakt ovanifrån av den svängda poolen och däcket på den runda byggnadens takterrass')

a('.media.items[4].caption',
  'La piscina de la cubierta, desde arriba',
  'La piscine du toit, vue d’en haut',
  'Der Dachpool von oben',
  'Бассейн на крыше сверху',
  'مسبح السطح من الأعلى',
  'Het dakzwembad van bovenaf',
  'Basen na dachu z góry',
  'Takbassenget ovenfra',
  'Takpoolen ovanifrån')

a('.media.items[5].alt',
  'Fotografía de una piscina comunitaria redonda en los jardines de la primera fase, con los bloques al fondo',
  'Photographie d’une piscine commune ronde dans les jardins de la première phase, avec les immeubles en arrière-plan',
  'Foto eines runden Gemeinschaftspools in den Gärten der ersten Phase, dahinter die Gebäude',
  'Фотография круглого общего бассейна в садах первой очереди, за ним корпуса',
  'صورة فوتوغرافية لمسبح مشترك دائري في حدائق المرحلة الأولى، والمباني خلفه',
  'Foto van een rond gemeenschappelijk zwembad in de tuinen van de eerste fase, met de blokken erachter',
  'Zdjęcie okrągłego wspólnego basenu w ogrodach pierwszego etapu, w tle budynki',
  'Foto av et rundt felles basseng i hagene i første byggetrinn, med byggene bak',
  'Foto av en rund gemensam pool i trädgårdarna i första etappen, med husen bakom')

a('.media.items[6].alt',
  'Fotografía del interior del health club: una piscina alicatada con pasamanos y, al fondo, la piscina cubierta',
  'Photographie de l’intérieur du club de santé : un bassin carrelé avec une main courante, la piscine intérieure au fond',
  'Foto im Health Club: ein gefliestes Becken mit Handlauf, dahinter das Innenbecken',
  'Фотография внутри оздоровительного клуба: бассейн, отделанный плиткой, с поручнем, дальше крытый бассейн',
  'صورة فوتوغرافية داخل النادي الصحي: حوض مكسو بالبلاط مع درابزين، والمسبح الداخلي خلفه',
  'Foto in de health club: een betegeld bad met een leuning, met het binnenzwembad erachter',
  'Zdjęcie wnętrza klubu zdrowia: wyłożony płytkami basen z poręczą, dalej basen kryty',
  'Foto inne i helseklubben: et flislagt basseng med rekkverk, med innebassenget bak',
  'Foto inne i hälsoklubben: en kaklad bassäng med ledstång, med inomhuspoolen bakom')

a('.media.items[6].caption',
  'El health club',
  'Le club de santé',
  'Der Health Club',
  'Оздоровительный клуб',
  'النادي الصحي',
  'De health club',
  'Klub zdrowia',
  'Helseklubben',
  'Hälsoklubben')

a('.media.items[7].alt',
  'Fotografía del gimnasio de la primera fase con cintas de correr y elípticas',
  'Photographie de la salle de sport de la première phase avec des tapis de course et des vélos elliptiques',
  'Foto des Fitnessraums der ersten Phase mit Laufbändern und Crosstrainern',
  'Фотография тренажёрного зала первой очереди с беговыми дорожками и эллиптическими тренажёрами',
  'صورة فوتوغرافية للصالة الرياضية في المرحلة الأولى، مع أجهزة المشي وأجهزة التمارين البيضاوية',
  'Foto van de fitnessruimte van de eerste fase met loopbanden en crosstrainers',
  'Zdjęcie siłowni pierwszego etapu z bieżniami i orbitrekami',
  'Foto av treningsrommet i første byggetrinn med tredemøller og crosstrainere',
  'Foto av gymmet i första etappen med löpband och crosstrainers')

a('.media.items[8].alt',
  'Fotografía de una terraza en planta baja de la primera fase con una sombrilla y dos tumbonas junto al césped',
  'Photographie d’une terrasse en rez-de-chaussée de la première phase avec un parasol et deux transats au bord de la pelouse',
  'Foto einer Erdgeschossterrasse der ersten Phase mit Sonnenschirm und zwei Liegen am Rasen',
  'Фотография террасы квартиры на первом этаже в первой очереди: зонт и два шезлонга рядом с газоном',
  'صورة فوتوغرافية لتراس مسكن في الطابق الأرضي من المرحلة الأولى، مع مظلة وكرسيين للتشمس بجانب العشب',
  'Foto van een terras op de begane grond in de eerste fase met een parasol en twee ligstoelen naast het gazon',
  'Zdjęcie tarasu mieszkania na parterze w pierwszym etapie z parasolem i dwoma leżakami przy trawniku',
  'Foto av en terrasse i første etasje i første byggetrinn med parasoll og to solsenger ved plenen',
  'Foto av en terrass på bottenvåningen i första etappen med parasoll och två solsängar vid gräsmattan')

a('.media.items[10].caption',
  'La terraza del ático V1-312',
  'La terrasse de l’attique V1-312',
  'Die Terrasse des Penthouses V1-312',
  'Терраса пентхауса V1-312',
  'تراس البنتهاوس V1-312',
  'Het terras van penthouse V1-312',
  "Taras penthouse'u V1-312",
  'Terrassen til toppleilighet V1-312',
  'Terrassen till takvåning V1-312')

a('.media.items[11].alt',
  'Fotografía de la isla de cocina y la zona de estar del ático V1-312, con ventanales en dos lados',
  'Photographie de l’îlot de cuisine et du séjour de l’attique V1-312, avec des baies vitrées sur deux côtés',
  'Foto der Kücheninsel und des Wohnbereichs im Penthouse V1-312 mit Fenstern auf zwei Seiten',
  'Фотография кухонного острова и гостиной пентхауса V1-312 с окнами на две стороны',
  'صورة فوتوغرافية لجزيرة المطبخ وصالة المعيشة في البنتهاوس V1-312، بنوافذ على جانبين',
  'Foto van het kookeiland en de woonruimte van penthouse V1-312, met ramen aan twee zijden',
  "Zdjęcie wyspy kuchennej i salonu penthouse'u V1-312 z oknami na dwie strony",
  'Foto av kjøkkenøya og stuen i toppleilighet V1-312, med vinduer på to sider',
  'Foto av köksön och vardagsrummet i takvåning V1-312, med fönster åt två håll')

a('.media.items[11].caption',
  'Ático V1-312, cocina y salón',
  'Attique V1-312, cuisine et séjour',
  'Penthouse V1-312, Küche und Wohnzimmer',
  'Пентхаус V1-312: кухня и гостиная',
  'البنتهاوس V1-312: المطبخ وصالة المعيشة',
  'Penthouse V1-312, keuken en woonkamer',
  'Penthouse V1-312, kuchnia i salon',
  'Toppleilighet V1-312, kjøkken og stue',
  'Takvåning V1-312, kök och vardagsrum')

a('.media.items[12].alt',
  'Fotografía de la mesa de comedor del ático V1-312, rodeada de cristal de suelo a techo',
  'Photographie de la table à manger de l’attique V1-312, entourée de baies vitrées du sol au plafond',
  'Foto des Esstischs im Penthouse V1-312 hinter raumhohen Glasflächen',
  'Фотография обеденного стола пентхауса V1-312 в окружении остекления от пола до потолка',
  'صورة فوتوغرافية لطاولة الطعام في البنتهاوس V1-312 تحيط بها واجهات زجاجية من الأرض حتى السقف',
  'Foto van de eettafel van penthouse V1-312 achter glas van vloer tot plafond',
  "Zdjęcie stołu jadalnego penthouse'u V1-312 otoczonego przeszkleniem od podłogi do sufitu",
  'Foto av spisebordet i toppleilighet V1-312 innenfor glass fra gulv til tak',
  'Foto av matbordet i takvåning V1-312 innanför glas från golv till tak')

a('.media.items[12].caption',
  'Ático V1-312, comedor',
  'Attique V1-312, coin repas',
  'Penthouse V1-312, Essbereich',
  'Пентхаус V1-312: обеденная зона',
  'البنتهاوس V1-312: منطقة الطعام',
  'Penthouse V1-312, eethoek',
  'Penthouse V1-312, jadalnia',
  'Toppleilighet V1-312, spiseplass',
  'Takvåning V1-312, matplats')

a('.media.items[13].alt',
  'Fotografía del piso piloto amueblado del edificio circular: un salón curvo con el mar al fondo',
  'Photographie de l’appartement témoin meublé du bâtiment circulaire : un séjour courbe avec la mer au loin',
  'Foto der möblierten Musterwohnung im runden Gebäude: ein geschwungenes Wohnzimmer, dahinter das Meer',
  'Фотография меблированной шоу-квартиры в круглом здании: изогнутая гостиная с видом на море',
  'صورة فوتوغرافية للشقة النموذجية المفروشة في المبنى الدائري: صالة معيشة منحنية والبحر في الأفق',
  'Foto van het ingerichte modelappartement in het ronde gebouw: een gebogen woonkamer met de zee in de verte',
  'Zdjęcie umeblowanego mieszkania pokazowego w okrągłym budynku: zaokrąglony salon z widokiem na morze',
  'Foto av den møblerte visningsleiligheten i den runde bygningen: en buet stue med havet i bakgrunnen',
  'Foto av den möblerade visningslägenheten i den runda byggnaden: ett svängt vardagsrum med havet i fjärran')

a('.media.items[13].caption',
  'El piso piloto circular',
  'L’appartement témoin circulaire',
  'Die runde Musterwohnung',
  'Шоу-квартира в круглом здании',
  'الشقة النموذجية في المبنى الدائري',
  'Het ronde modelappartement',
  'Mieszkanie pokazowe w okrągłym budynku',
  'Den runde visningsleiligheten',
  'Den runda visningslägenheten')

a('.media.items[14].alt',
  'Fotografía de un dormitorio del piso piloto del edificio circular, con un espejo redondo y una alfombra curva',
  'Photographie d’une chambre de l’appartement témoin du bâtiment circulaire, avec un miroir rond et un tapis courbe',
  'Foto eines Schlafzimmers der Musterwohnung im runden Gebäude mit rundem Spiegel und geschwungenem Teppich',
  'Фотография спальни в шоу-квартире круглого здания с круглым зеркалом и изогнутым ковром',
  'صورة فوتوغرافية لغرفة نوم في الشقة النموذجية بالمبنى الدائري، مع مرآة مستديرة وسجادة منحنية',
  'Foto van een slaapkamer in het modelappartement van het ronde gebouw, met een ronde spiegel en een gebogen vloerkleed',
  'Zdjęcie sypialni w mieszkaniu pokazowym okrągłego budynku z okrągłym lustrem i zaokrąglonym dywanem',
  'Foto av et soverom i visningsleiligheten i den runde bygningen, med et rundt speil og et buet teppe',
  'Foto av ett sovrum i den runda byggnadens visningslägenhet, med en rund spegel och en svängd matta')

a('.media.items[14].caption',
  'Un dormitorio del edificio circular',
  'Une chambre du bâtiment circulaire',
  'Ein Schlafzimmer im runden Gebäude',
  'Спальня в круглом здании',
  'غرفة نوم في المبنى الدائري',
  'Een slaapkamer in het ronde gebouw',
  'Sypialnia w okrągłym budynku',
  'Et soverom i den runde bygningen',
  'Ett sovrum i den runda byggnaden')

a('.media.items[15].alt',
  'Fotografía de un piso piloto amueblado de la primera fase: salón comedor abierto a la terraza',
  'Photographie d’un appartement témoin meublé de la première phase : séjour et salle à manger ouverts sur la terrasse',
  'Foto einer möblierten Musterwohnung der ersten Phase: Wohn- und Essbereich mit Zugang zur Terrasse',
  'Фотография меблированной шоу-квартиры первой очереди: гостиная со столовой с выходом на террасу',
  'صورة فوتوغرافية لشقة نموذجية مفروشة في المرحلة الأولى: صالة معيشة وطعام تنفتح على التراس',
  'Foto van een ingericht modelappartement uit de eerste fase: woon- en eetkamer die uitkomen op het terras',
  'Zdjęcie umeblowanego mieszkania pokazowego pierwszego etapu: salon z jadalnią otwarty na taras',
  'Foto av en møblert visningsleilighet i første byggetrinn: stue og spisestue som åpner seg mot terrassen',
  'Foto av en möblerad visningslägenhet i första etappen: vardags- och matrum som öppnar sig mot terrassen')

a('.media.items[15].caption',
  'Un piso piloto de la primera fase',
  'Un appartement témoin de la première phase',
  'Eine Musterwohnung der ersten Phase',
  'Шоу-квартира первой очереди',
  'شقة نموذجية في المرحلة الأولى',
  'Een modelappartement uit de eerste fase',
  'Mieszkanie pokazowe pierwszego etapu',
  'En visningsleilighet i første byggetrinn',
  'En visningslägenhet i första etappen')

a('.media.items[16].alt',
  'Fotografía de la terraza cubierta de un piso piloto de la primera fase, con un sofá de exterior bajo la pérgola',
  'Photographie de la terrasse couverte d’un appartement témoin de la première phase, avec un canapé d’extérieur sous la pergola',
  'Foto der überdachten Terrasse einer Musterwohnung der ersten Phase mit Outdoor-Sofa unter der Pergola',
  'Фотография крытой террасы шоу-квартиры первой очереди с уличным диваном под перголой',
  'صورة فوتوغرافية للتراس المسقوف في شقة نموذجية من المرحلة الأولى، مع أريكة خارجية تحت العريشة',
  'Foto van het overdekte terras van een modelappartement uit de eerste fase, met een loungebank onder de pergola',
  'Zdjęcie zadaszonego tarasu mieszkania pokazowego pierwszego etapu z sofą ogrodową pod pergolą',
  'Foto av den overdekkede terrassen i en visningsleilighet i første byggetrinn, med en utesofa under pergolaen',
  'Foto av den täckta terrassen i en visningslägenhet i första etappen, med en utesoffa under pergolan')

a('.media.items[17].alt',
  'Fotografía de un dormitorio de un piso piloto de la primera fase, con una pared revestida de madera y un escritorio',
  'Photographie d’une chambre d’un appartement témoin de la première phase, avec un mur habillé de bois et un bureau',
  'Foto eines Schlafzimmers einer Musterwohnung der ersten Phase mit holzverkleideter Wand und Schreibtisch',
  'Фотография спальни в шоу-квартире первой очереди со стеной, облицованной деревом, и письменным столом',
  'صورة فوتوغرافية لغرفة نوم في شقة نموذجية من المرحلة الأولى، بجدار مكسو بالخشب ومكتب',
  'Foto van een slaapkamer in een modelappartement uit de eerste fase, met een houten wandbekleding en een bureau',
  'Zdjęcie sypialni w mieszkaniu pokazowym pierwszego etapu ze ścianą wyłożoną drewnem i biurkiem',
  'Foto av et soverom i en visningsleilighet i første byggetrinn, med trepanel på veggen og et skrivebord',
  'Foto av ett sovrum i en visningslägenhet i första etappen, med träpanel på väggen och ett skrivbord')

a('.media.items[17].caption',
  'Un dormitorio del piso piloto',
  'Une chambre de l’appartement témoin',
  'Ein Schlafzimmer der Musterwohnung',
  'Спальня в шоу-квартире',
  'غرفة نوم في الشقة النموذجية',
  'Een slaapkamer in het modelappartement',
  'Sypialnia w mieszkaniu pokazowym',
  'Et soverom i visningsleiligheten',
  'Ett sovrum i visningslägenheten')

a('.media.items[18].alt',
  'Imagen aérea del juego de planos generales de la promotora: los bloques blancos y curvos en la ladera, con movimientos de tierra y grúas en la parte alta',
  'Image aérienne tirée du plan de masse du promoteur : les immeubles blancs et courbes sur le coteau, avec des terrassements et des grues sur les terrains plus hauts',
  'Luftbild aus den Masterplan-Unterlagen des Bauträgers: die geschwungenen weißen Gebäude am Hang, mit Erdarbeiten und Kränen auf dem höher gelegenen Gelände',
  'Аэроснимок из материалов генплана застройщика: изогнутые белые корпуса на склоне, выше — земляные работы и краны',
  'صورة جوية من مجموعة المخطط العام للمطوّر: المباني البيضاء المنحنية على المنحدر، مع أعمال الحفر والرافعات على الأرض الأعلى',
  'Luchtbeeld uit de masterplanset van de ontwikkelaar: de gebogen witte blokken op de helling, met grondwerken en kranen op het hoger gelegen terrein',
  'Zdjęcie lotnicze z materiałów planu zagospodarowania dewelopera: zaokrąglone białe budynki na zboczu, wyżej roboty ziemne i dźwigi',
  'Luftbilde fra utbyggerens reguleringsplanmateriale: de buede hvite byggene i skråningen, med gravearbeider og kraner på terrenget ovenfor',
  'Flygbild ur exploatörens översiktsplanmaterial: de svängda vita husen i slänten, med markarbeten och kranar på marken ovanför')

a('.media.items[18].caption',
  'La ladera, según el plan general de la promotora',
  'Le coteau, d’après le plan de masse du promoteur',
  'Der Hang, aus dem Masterplan des Bauträgers',
  'Склон, из генплана застройщика',
  'سفح التل، من المخطط العام للمطوّر',
  'De heuvel, uit het masterplan van de ontwikkelaar',
  'Zbocze, z planu zagospodarowania dewelopera',
  'Åssiden, fra utbyggerens reguleringsplan',
  'Sluttningen, ur exploatörens översiktsplan')

a('.media.items[19].alt',
  'Imagen generada por ordenador de la piscina de agua salada prevista para las fases II y III, con tumbonas y la costa al fondo',
  'Image de synthèse de la piscine d’eau salée prévue pour les phases II et III, avec des transats, la côte au loin',
  'Computergenerierte Ansicht des für die Phasen II und III geplanten Salzwasserpools mit Liegen, dahinter die Küste',
  'Компьютерная визуализация бассейна с морской водой, запланированного для очередей II и III, с шезлонгами и видом на побережье',
  'صورة مولّدة بالحاسوب لمسبح المياه المالحة المخطط للمرحلتين II وIII، مع كراسي التشمس والساحل في الأفق',
  'Computergegenereerd beeld van het zoutwaterzwembad dat voor Fase II en III is gepland, met ligstoelen en de kust in de verte',
  'Wizualizacja komputerowa basenu ze słoną wodą planowanego dla etapów II i III, z leżakami i wybrzeżem w tle',
  'Datagenerert bilde av saltvannsbassenget som er planlagt for byggetrinn II og III, med solsenger og kysten i bakgrunnen',
  'Datorgenererad vy av saltvattenpoolen som planeras för etapp II och III, med solsängar och kusten i fjärran')

a('.media.items[19].caption',
  'La piscina de agua salada (render)',
  'La piscine d’eau salée (image de synthèse)',
  'Der Salzwasserpool (Visualisierung)',
  'Бассейн с морской водой (визуализация)',
  'مسبح المياه المالحة (تصور)',
  'Het zoutwaterzwembad (render)',
  'Basen ze słoną wodą (wizualizacja)',
  'Saltvannsbassenget (illustrasjon)',
  'Saltvattenpoolen (illustration)')

a('.media.items[20].alt',
  'Imagen generada por ordenador del sports lounge previsto, con simulador de golf y mesa de billar',
  'Image de synthèse du salon sportif prévu, avec un simulateur de golf et un billard',
  'Computergenerierte Ansicht der geplanten Sport-Lounge mit Golfsimulator und Billardtisch',
  'Компьютерная визуализация запланированного спортивного лаунжа с гольф-симулятором и бильярдным столом',
  'صورة مولّدة بالحاسوب لصالة الرياضة الترفيهية المخططة، مع جهاز محاكاة الغولف وطاولة بلياردو',
  'Computergegenereerd beeld van de geplande sportlounge met een golfsimulator en een biljarttafel',
  'Wizualizacja komputerowa planowanego salonu sportowego z symulatorem golfa i stołem bilardowym',
  'Datagenerert bilde av den planlagte sportsloungen med golfsimulator og biljardbord',
  'Datorgenererad vy av den planerade sportloungen med golfsimulator och biljardbord')

a('.media.items[20].caption',
  'El sports lounge (render)',
  'Le salon sportif (image de synthèse)',
  'Die Sport-Lounge (Visualisierung)',
  'Спортивный лаунж (визуализация)',
  'الصالة الرياضية الترفيهية (تصور)',
  'De sportlounge (render)',
  'Salon sportowy (wizualizacja)',
  'Sportsloungen (illustrasjon)',
  'Sportloungen (illustration)')

a('.media.items[21].alt',
  'Imagen generada por ordenador de un jardín en planta baja de las fases II y III, con piscina propia y el mar al fondo',
  'Image de synthèse d’un jardin en rez-de-chaussée des phases II et III, avec sa propre piscine et la mer au loin',
  'Computergenerierte Ansicht eines Erdgeschossgartens der Phasen II und III mit eigenem Pool, dahinter das Meer',
  'Компьютерная визуализация сада квартиры на первом этаже в очередях II и III с собственным бассейном и видом на море',
  'صورة مولّدة بالحاسوب لحديقة مسكن في الطابق الأرضي من المرحلتين II وIII، بمسبح خاص والبحر في الأفق',
  'Computergegenereerd beeld van een tuin bij een benedenwoning in Fase II en III, met een eigen zwembad en de zee in de verte',
  'Wizualizacja komputerowa ogrodu mieszkania na parterze w etapach II i III z własnym basenem i widokiem na morze',
  'Datagenerert bilde av en hage til en bolig i første etasje i byggetrinn II og III, med eget basseng og havet i bakgrunnen',
  'Datorgenererad vy av en trädgård till en bottenvåning i etapp II och III, med egen pool och havet i fjärran')

a('.media.items[21].caption',
  'Un jardín con piscina privada (render)',
  'Un jardin avec piscine privée (image de synthèse)',
  'Ein Garten mit privatem Pool (Visualisierung)',
  'Сад с собственным бассейном (визуализация)',
  'حديقة بمسبح خاص (تصور)',
  'Een tuin met privézwembad (render)',
  'Ogród z prywatnym basenem (wizualizacja)',
  'En hage med privat basseng (illustrasjon)',
  'En trädgård med egen pool (illustration)')

a('.media.items[22].alt',
  'Imagen nocturna generada por ordenador de un jardín en planta baja con piscina privada y un banco hundido junto a un fuego',
  'Image de synthèse nocturne d’un jardin en rez-de-chaussée avec piscine privée et un salon encastré autour d’un brasero',
  'Computergenerierte Nachtansicht eines Erdgeschossgartens mit privatem Pool und abgesenkter Sitzecke an einer Feuerstelle',
  'Компьютерная визуализация ночного сада квартиры на первом этаже с собственным бассейном и утопленной зоной у очага',
  'صورة ليلية مولّدة بالحاسوب لحديقة مسكن في الطابق الأرضي، بمسبح خاص ومقعد غائر حول موقد نار',
  'Computergegenereerd avondbeeld van een tuin bij een benedenwoning met een privézwembad en een verzonken zitplek bij een vuurplaats',
  'Nocna wizualizacja komputerowa ogrodu mieszkania na parterze z prywatnym basenem i zagłębionym siedziskiem przy palenisku',
  'Datagenerert kveldsbilde av en hage til en bolig i første etasje med privat basseng og en nedsenket sittegruppe ved et bålsted',
  'Datorgenererad kvällsvy av en trädgård till en bottenvåning med egen pool och en nedsänkt sittplats vid en eldstad')

a('.media.items[22].caption',
  'Un jardín de noche (render)',
  'Un jardin la nuit (image de synthèse)',
  'Ein Garten bei Nacht (Visualisierung)',
  'Сад ночью (визуализация)',
  'حديقة في الليل (تصور)',
  'Een tuin bij avond (render)',
  'Ogród nocą (wizualizacja)',
  'En hage om kvelden (illustrasjon)',
  'En trädgård på kvällen (illustration)')

a('.media.items[23].alt',
  'Imagen generada por ordenador de la terraza en cubierta de un ático con piscina alicatada, tumbonas y un brasero',
  'Image de synthèse du toit-terrasse d’un attique avec une piscine carrelée, des transats et un brasero',
  'Computergenerierte Ansicht der Dachterrasse eines Penthouses mit gefliestem Pool, Liegen und Feuerstelle',
  'Компьютерная визуализация кровельной террасы пентхауса с бассейном, отделанным плиткой, шезлонгами и очагом',
  'صورة مولّدة بالحاسوب لتراس سطح بنتهاوس بمسبح مكسو بالبلاط وكراسي تشمس وموقد نار',
  'Computergegenereerd beeld van een dakterras van een penthouse met een betegeld zwembad, ligstoelen en een vuurplaats',
  "Wizualizacja komputerowa tarasu na dachu penthouse'u z basenem wyłożonym płytkami, leżakami i paleniskiem",
  'Datagenerert bilde av en takterrasse til en toppleilighet med flislagt basseng, solsenger og et bålsted',
  'Datorgenererad vy av en takterrass till en takvåning med kaklad pool, solsängar och en eldstad')

a('.media.items[23].caption',
  'La terraza en cubierta de un ático (render)',
  'Le toit-terrasse d’un attique (image de synthèse)',
  'Die Dachterrasse eines Penthouses (Visualisierung)',
  'Кровельная терраса пентхауса (визуализация)',
  'تراس سطح بنتهاوس (تصور)',
  'Een dakterras van een penthouse (render)',
  "Taras na dachu penthouse'u (wizualizacja)",
  'En takterrasse på en toppleilighet (illustrasjon)',
  'En takterrass på en takvåning (illustration)')

a('.media.items[24].alt',
  'Imagen generada por ordenador de una mesa de comedor en una terraza en cubierta junto a un muro vegetal, con las montañas y la costa detrás',
  'Image de synthèse d’une table à manger sur un toit-terrasse, à côté d’un mur végétal, les montagnes et la côte en arrière-plan',
  'Computergenerierte Ansicht eines Esstischs auf einer Dachterrasse neben einer begrünten Wand, dahinter die Berge und die Küste',
  'Компьютерная визуализация обеденного стола на кровельной террасе у зелёной стены, позади горы и побережье',
  'صورة مولّدة بالحاسوب لطاولة طعام على تراس السطح بجانب جدار مزروع، والجبال والساحل خلفها',
  'Computergegenereerd beeld van een eettafel op een dakterras naast een begroeide wand, met de bergen en de kust erachter',
  'Wizualizacja komputerowa stołu jadalnego na tarasie dachowym przy zielonej ścianie, w tle góry i wybrzeże',
  'Datagenerert bilde av et spisebord på en takterrasse ved en beplantet vegg, med fjellene og kysten bak',
  'Datorgenererad vy av ett matbord på en takterrass vid en planterad vägg, med bergen och kusten bakom')

a('.media.items[24].caption',
  'Un jardín en la cubierta (render)',
  'Un jardin sur le toit (image de synthèse)',
  'Ein Dachgarten (Visualisierung)',
  'Сад на крыше (визуализация)',
  'حديقة على السطح (تصور)',
  'Een daktuin (render)',
  'Ogród na dachu (wizualizacja)',
  'En takhage (illustrasjon)',
  'En takträdgård (illustration)')

a('.media.items[25].alt',
  'Imagen generada por ordenador del salón de un ático de las fases II y III, abierto a una terraza curva',
  'Image de synthèse du séjour d’un attique des phases II et III, ouvert sur une terrasse courbe',
  'Computergenerierte Ansicht des Wohnzimmers eines Penthouses der Phasen II und III mit Zugang zu einer geschwungenen Terrasse',
  'Компьютерная визуализация гостиной пентхауса в очередях II и III с выходом на изогнутую террасу',
  'صورة مولّدة بالحاسوب لصالة معيشة بنتهاوس في المرحلتين II وIII تنفتح على تراس منحنٍ',
  'Computergegenereerd beeld van een woonkamer van een penthouse in Fase II en III die uitkomt op een gebogen terras',
  "Wizualizacja komputerowa salonu penthouse'u w etapach II i III z wyjściem na zaokrąglony taras",
  'Datagenerert bilde av en stue i en toppleilighet i byggetrinn II og III som åpner seg mot en buet terrasse',
  'Datorgenererad vy av ett vardagsrum i en takvåning i etapp II och III som öppnar sig mot en svängd terrass')

a('.media.items[25].caption',
  'El salón de un ático (render)',
  'Le séjour d’un attique (image de synthèse)',
  'Das Wohnzimmer eines Penthouses (Visualisierung)',
  'Гостиная пентхауса (визуализация)',
  'صالة معيشة بنتهاوس (تصور)',
  'Een woonkamer van een penthouse (render)',
  "Salon penthouse'u (wizualizacja)",
  'En stue i en toppleilighet (illustrasjon)',
  'Ett vardagsrum i en takvåning (illustration)')

a('.media.items[26].alt',
  'Imagen generada por ordenador de la cocina de un ático con isla de piedra y tres taburetes',
  'Image de synthèse de la cuisine d’un attique avec un îlot en pierre et trois tabourets de bar',
  'Computergenerierte Ansicht der Küche eines Penthouses mit Steininsel und drei Barhockern',
  'Компьютерная визуализация кухни пентхауса с каменным островом и тремя барными стульями',
  'صورة مولّدة بالحاسوب لمطبخ بنتهاوس بجزيرة حجرية وثلاثة مقاعد مرتفعة',
  'Computergegenereerd beeld van een penthousekeuken met een stenen kookeiland en drie barkrukken',
  "Wizualizacja komputerowa kuchni penthouse'u z kamienną wyspą i trzema hokerami",
  'Datagenerert bilde av et kjøkken i en toppleilighet med kjøkkenøy i stein og tre barkrakker',
  'Datorgenererad vy av ett kök i en takvåning med köksö i sten och tre barstolar')

a('.media.items[26].caption',
  'La cocina de un ático (render)',
  'La cuisine d’un attique (image de synthèse)',
  'Die Küche eines Penthouses (Visualisierung)',
  'Кухня пентхауса (визуализация)',
  'مطبخ بنتهاوس (تصور)',
  'Een penthousekeuken (render)',
  "Kuchnia penthouse'u (wizualizacja)",
  'Et kjøkken i en toppleilighet (illustrasjon)',
  'Ett kök i en takvåning (illustration)')

a('.overview.headlineHtml',
  'Una ladera, <em>tres fases</em>',
  'Un coteau, <em>trois phases</em>',
  'Ein Hang, <em>drei Phasen</em>',
  'Один склон, <em>три очереди</em>',
  'سفح واحد، <em>ثلاث مراحل</em>',
  'Eén heuvel, <em>drie fasen</em>',
  'Jedno zbocze, <em>trzy etapy</em>',
  'Én åsside, <em>tre byggetrinn</em>',
  'En sluttning, <em>tre etapper</em>')

a('.overview.copy[0]',
  'Madroñal Heights Residences es el nombre que damos a un conjunto de 107 apartamentos y áticos en una ladera de Benahavís, sobre Golf Valley, con El Madroñal detrás. Se construye en tres fases. La primera, 49 viviendas en siete bloques, está terminada; la segunda y la tercera, 58 viviendas entre ambas, están en construcción, y sus propietarios comparten el health club, las piscinas y el club infantil de la primera fase.',
  'Madroñal Heights Residences est le nom que nous donnons à une résidence de 107 appartements et attiques sur un coteau de Benahavís, au-dessus de Golf Valley, avec El Madroñal en arrière-plan. Elle se construit en trois phases. La première, 49 logements en sept immeubles, est achevée ; la deuxième et la troisième, 58 logements à elles deux, sont en construction, et leurs propriétaires partagent le club de santé, les piscines et le club enfants de la première phase.',
  'Madroñal Heights Residences ist der Name, den wir einer Anlage mit 107 Wohnungen und Penthäusern an einem Hang in Benahavís oberhalb von Golf Valley geben, mit El Madroñal im Rücken. Sie entsteht in drei Phasen. Die erste mit 49 Wohnungen in sieben Gebäuden ist fertiggestellt; die zweite und dritte, zusammen 58 Wohnungen, sind im Bau, und ihre Eigentümer teilen sich Health Club, Pools und Kinderclub der ersten Phase.',
  'Madroñal Heights Residences — так мы называем комплекс из 107 апартаментов и пентхаусов на склоне холма в Бенаависе, над Гольф-долиной, за которым поднимается Эль-Мадроньяль. Он строится в три очереди. Первая — 49 квартир в семи корпусах — завершена; вторая и третья, вместе 58 квартир, строятся, а их владельцы пользуются оздоровительным клубом, бассейнами и детским клубом первой очереди.',
  'Madroñal Heights Residences هو الاسم الذي نطلقه على مجمع من 107 شقق وبنتهاوس على سفح تلّ في بيناهافيس، فوق وادي الغولف، ويقع إل مادرونيال خلفه. ويُبنى المجمع على ثلاث مراحل: الأولى، 49 مسكنًا في سبعة مبانٍ، مكتملة؛ والثانية والثالثة، 58 مسكنًا بينهما، قيد الإنشاء، ويتشارك ملّاكهما النادي الصحي والمسابح ونادي الأطفال في المرحلة الأولى.',
  'Madroñal Heights Residences is de naam die wij geven aan een project van 107 appartementen en penthouses op een heuvel in Benahavís, boven Golf Valley, met El Madroñal erachter. Het wordt in drie fasen gebouwd. De eerste, 49 woningen in zeven blokken, is voltooid; de tweede en derde, samen 58 woningen, zijn in aanbouw, en hun eigenaren delen de health club, de zwembaden en de kinderclub van de eerste fase.',
  "Madroñal Heights Residences to nazwa, którą nadajemy inwestycji obejmującej 107 apartamentów i penthouse'ów na zboczu wzgórza w Benahavís, nad Golf Valley, z El Madroñal za plecami. Powstaje w trzech etapach. Pierwszy, 49 mieszkań w siedmiu budynkach, jest ukończony; drugi i trzeci, łącznie 58 mieszkań, są w budowie, a ich właściciele korzystają z klubu zdrowia, basenów i klubu dziecięcego pierwszego etapu.",
  'Madroñal Heights Residences er navnet vi gir et prosjekt med 107 leiligheter og toppleiligheter i en åsside i Benahavís, over Golf Valley, med El Madroñal bak. Det bygges i tre byggetrinn. Det første, 49 boliger i sju bygg, er ferdig; det andre og tredje, 58 boliger til sammen, er under bygging, og eierne der deler helseklubben, bassengene og barneklubben i første byggetrinn.',
  'Madroñal Heights Residences är namnet vi ger ett projekt med 107 lägenheter och takvåningar på en sluttning i Benahavís, ovanför Golf Valley, med El Madroñal bakom. Det byggs i tre etapper. Den första, 49 bostäder i sju hus, är färdig; den andra och tredje, 58 bostäder tillsammans, är under uppförande, och deras ägare delar den första etappens hälsoklubb, pooler och barnklubb.')

a('.overview.copy[1]',
  'En las listas de precios de la promotora hay veinte viviendas disponibles. Cuatro están en la primera fase, listas para entregar llaves: dos áticos de cuatro dormitorios y dos viviendas de tres dormitorios en la planta baja y la primera planta del edificio circular. Una está en la segunda fase y quince en la tercera, desde apartamentos de dos dormitorios hasta áticos de cuatro.',
  'Vingt logements sont disponibles sur les listes de prix du promoteur. Quatre sont dans la première phase et prêts à la remise des clés : deux attiques de quatre chambres et deux logements de trois chambres au rez-de-chaussée et au premier étage du bâtiment circulaire. Un se trouve dans la deuxième phase et quinze dans la troisième, des appartements de deux chambres aux attiques de quatre chambres.',
  'Auf den Preislisten des Bauträgers sind zwanzig Wohnungen verfügbar. Vier liegen in der ersten Phase und sind schlüsselfertig: zwei Penthäuser mit vier Schlafzimmern und zwei Wohnungen mit drei Schlafzimmern im Erdgeschoss und im ersten Obergeschoss des runden Gebäudes. Eine liegt in der zweiten Phase und fünfzehn in der dritten, von Wohnungen mit zwei Schlafzimmern bis zu Penthäusern mit vier.',
  'В прайс-листах застройщика свободны двадцать квартир. Четыре — в первой очереди и готовы к заселению: два пентхауса с четырьмя спальнями и две квартиры с тремя спальнями на первом и втором этажах круглого здания. Одна — во второй очереди и пятнадцать — в третьей, от квартир с двумя спальнями до пентхаусов с четырьмя.',
  'تتاح عشرون وحدة في قوائم أسعار المطوّر. أربع منها في المرحلة الأولى وجاهزة للتسليم: بنتهاوسان بأربع غرف نوم، ومسكنان بثلاث غرف نوم في الطابقين الأرضي والأول من المبنى الدائري. وواحدة في المرحلة الثانية، وخمس عشرة في الثالثة، من شقق بغرفتي نوم إلى بنتهاوس بأربع غرف.',
  'Twintig woningen staan als beschikbaar op de prijslijsten van de ontwikkelaar. Vier liggen in de eerste fase en zijn sleutelklaar: twee penthouses met vier slaapkamers en twee woningen met drie slaapkamers op de begane grond en de eerste verdieping van het ronde gebouw. Eén ligt in de tweede fase en vijftien in de derde, van appartementen met twee slaapkamers tot penthouses met vier.',
  "W cennikach dewelopera dostępnych jest dwadzieścia mieszkań. Cztery są w pierwszym etapie i gotowe do odbioru: dwa penthouse'y z czterema sypialniami i dwa mieszkania z trzema sypialniami na parterze i pierwszym piętrze okrągłego budynku. Jedno jest w drugim etapie, a piętnaście w trzecim, od mieszkań z dwiema sypialniami po penthouse'y z czterema.",
  'Tjue boliger er ledige på utbyggerens prislister. Fire er i første byggetrinn og klare for innflytting: to toppleiligheter med fire soverom og to boliger med tre soverom i første og andre etasje i den runde bygningen. Én er i andre byggetrinn og femten i det tredje, fra leiligheter med to soverom til toppleiligheter med fire.',
  'Tjugo bostäder är lediga på exploatörens prislistor. Fyra ligger i första etappen och är klara för inflyttning: två takvåningar med fyra sovrum och två bostäder med tre sovrum på bottenvåningen och första våningen i den runda byggnaden. En ligger i andra etappen och femton i den tredje, från lägenheter med två sovrum till takvåningar med fyra.')

a('.overview.copy[2]',
  'Las viviendas en planta baja de las fases posteriores tienen jardín con piscina privada, y los áticos una terraza en cubierta, con piscina en todos los planos de las fases posteriores. Todos los precios son la cifra neta de la promotora; se añade el {T}, actualmente del 10 por ciento.',
  'Les logements en rez-de-chaussée des phases suivantes ont un jardin avec piscine privée, et les attiques un toit-terrasse, avec une piscine sur tous les plans des phases suivantes. Chaque prix est le montant net du promoteur ; la {T}, actuellement de 10 pour cent, s’y ajoute.',
  'Die Erdgeschosswohnungen der späteren Phasen haben einen Garten mit privatem Pool, die Penthäuser eine Dachterrasse, auf jedem Grundriss der späteren Phasen mit Pool. Jeder Preis ist der Nettobetrag des Bauträgers; die {T} von derzeit 10 Prozent kommt hinzu.',
  'У квартир на первом этаже в последующих очередях есть сад с собственным бассейном, у пентхаусов — кровельная терраса, на всех планировках последующих очередей с бассейном. Все цены — нетто-суммы застройщика; сверху добавляется НДС по действующей ставке 10%.',
  'تتمتع مساكن الطابق الأرضي في المرحلتين اللاحقتين بحديقة ومسبح خاص، ولكل بنتهاوس تراس على السطح، مع مسبح في كل مخطط من مخططات المرحلتين اللاحقتين. وكل سعر هو الرقم الصافي للمطوّر، وتُضاف إليه ضريبة القيمة المضافة بنسبتها الحالية البالغة 10%.',
  'Benedenwoningen in de latere fasen hebben een tuin met een privézwembad, en penthouses hebben een dakterras, met een zwembad op elke plattegrond van de latere fasen. Elke prijs is het nettobedrag van de ontwikkelaar; daarbovenop komt btw van momenteel 10 procent.',
  "Mieszkania na parterze w kolejnych etapach mają ogród z prywatnym basenem, a penthouse'y taras na dachu, na każdym rzucie kolejnych etapów z basenem. Każda cena to kwota netto dewelopera; do niej doliczany jest VAT według obecnej stawki 10%.",
  'Boligene i første etasje i de senere byggetrinnene har hage med privat basseng, og toppleilighetene har takterrasse, med basseng på hver plantegning i de senere byggetrinnene. Alle priser er utbyggerens nettopris; i tillegg kommer mva., i dag 10 prosent.',
  'Bottenvåningarna i de senare etapperna har en trädgård med egen pool, och takvåningarna har en takterrass, med pool på varje planritning i de senare etapperna. Varje pris är exploatörens nettopris; därtill kommer IVA, för närvarande 10 procent.')

a('.overview.metrics[3][0]',
  'Fases',
  'Phases',
  'Phasen',
  'Очереди',
  'المراحل',
  'Fasen',
  'Etapy',
  'Byggetrinn',
  'Etapper')

a('.overview.metrics[3][1]',
  '3, una terminada',
  '3, dont une achevée',
  '3, eine fertiggestellt',
  '3, одна завершена',
  '3، واحدة مكتملة',
  '3, één voltooid',
  '3, jeden ukończony',
  '3, ett ferdig',
  '3, en färdig')

a('.residences.headlineHtml',
  'Llave en mano o <em>en construcción</em>',
  'Clés en main ou <em>en construction</em>',
  'Schlüsselfertig oder <em>im Bau</em>',
  'Готово к заселению или <em>строится</em>',
  'جاهز للتسليم أو <em>قيد الإنشاء</em>',
  'Sleutelklaar of <em>in aanbouw</em>',
  'Gotowe do odbioru lub <em>w budowie</em>',
  'Innflyttingsklar eller <em>under bygging</em>',
  'Inflyttningsklar eller <em>under uppförande</em>')

a('.residences.copy',
  'A qué fase pertenece cada vivienda disponible y en qué punto está esa fase. La referencia lo indica: V1 es la primera fase, ya terminada; V2-101 está en la segunda fase, y de V2-322 a V2-622 en la tercera.',
  'La phase à laquelle appartient chaque logement disponible, et où en est cette phase. La référence l’indique : V1 correspond à la première phase, achevée, V2-101 à la deuxième phase, et V2-322 à V2-622 à la troisième.',
  'Zu welcher Phase jede verfügbare Wohnung gehört und wo diese Phase steht. Die Referenz verrät es: V1 ist die fertiggestellte erste Phase, V2-101 liegt in der zweiten Phase und V2-322 bis V2-622 in der dritten.',
  'К какой очереди относится каждая свободная квартира и на какой стадии эта очередь. Подсказка — в номере: V1 — завершённая первая очередь, V2-101 — вторая, V2-322–V2-622 — третья.',
  'إلى أي مرحلة ينتمي كل مسكن متاح، وأين وصلت تلك المرحلة. والمرجع يدلّك: V1 هي المرحلة الأولى المكتملة، وV2-101 في المرحلة الثانية، ومن V2-322 إلى V2-622 في الثالثة.',
  'Bij welke fase elke beschikbare woning hoort, en hoe ver die fase is. De referentie zegt het u: V1 is de voltooide eerste fase, V2-101 ligt in de tweede fase en V2-322 tot en met V2-622 liggen in de derde.',
  'Do którego etapu należy każde dostępne mieszkanie i na jakim jest on etapie prac. Podpowiada to numer: V1 to ukończony pierwszy etap, V2-101 należy do drugiego, a V2-322 do V2-622 do trzeciego.',
  'Hvilket byggetrinn hver ledig bolig hører til, og hvor langt det byggetrinnet har kommet. Referansen forteller deg det: V1 er det ferdige første byggetrinnet, V2-101 er i andre byggetrinn og V2-322 til V2-622 er i det tredje.',
  'Vilken etapp varje ledig bostad hör till, och hur långt den etappen har kommit. Referensen visar det: V1 är den färdiga första etappen, V2-101 ligger i andra etappen och V2-322 till V2-622 ligger i den tredje.')

a('.residences.items[0].name',
  'Fase I, terminada',
  'Phase I, achevée',
  'Phase I, fertiggestellt',
  'Очередь I, завершена',
  'المرحلة I، مكتملة',
  'Fase I, voltooid',
  'Etap I, ukończony',
  'Byggetrinn I, ferdig',
  'Etapp I, färdig')

a('.residences.items[0].points[0]',
  'Dos áticos de cuatro dormitorios en el bloque 3, V1-311 y V1-312, cada uno con {N218.79} {U} construidos, una terraza de {N103.98} {U} y un solárium de {N127.58} {U} en la planta superior, dos plazas de garaje y un trastero.',
  'Deux attiques de quatre chambres dans l’immeuble 3, V1-311 et V1-312, chacun avec {N218.79} {U} construits, une terrasse de {N103.98} {U} et un solarium de {N127.58} {U} au-dessus, deux places de parking et un cellier.',
  'Zwei Penthäuser mit vier Schlafzimmern in Block 3, V1-311 und V1-312, jeweils mit {N218.79} {U} bebauter Fläche, einer Terrasse von {N103.98} {U} und einem Solarium von {N127.58} {U} darüber, zwei Stellplätzen und einem Abstellraum.',
  'Два пентхауса с четырьмя спальнями в корпусе 3, V1-311 и V1-312, у каждого {N218.79} {U} площади застройки, терраса {N103.98} {U} и солярий {N127.58} {U} над ней, два машиноместа и кладовая.',
  'بنتهاوسان بأربع غرف نوم في المبنى 3، هما V1-311 وV1-312، لكل منهما مساحة مبنية قدرها {N218.79} {U}، وتراس بمساحة {N103.98} {U}، وسولاريوم بمساحة {N127.58} {U} فوقه، وموقفان للسيارات ومخزن.',
  'Twee penthouses met vier slaapkamers in Blok 3, V1-311 en V1-312, elk met {N218.79} {U} bebouwd, een terras van {N103.98} {U} en daarboven een solarium van {N127.58} {U}, twee parkeerplaatsen en een berging.',
  "Dwa penthouse'y z czterema sypialniami w budynku 3, V1-311 i V1-312, każdy z {N218.79} {U} powierzchni zabudowy, tarasem {N103.98} {U} i solarium {N127.58} {U} piętro wyżej, dwoma miejscami postojowymi i komórką lokatorską.",
  'To toppleiligheter med fire soverom i Hus 3, V1-311 og V1-312, hver med {N218.79} {U} bebygd areal, en terrasse på {N103.98} {U} og en solterrasse på {N127.58} {U} over, to parkeringsplasser og en bod.',
  'Två takvåningar med fyra sovrum i Hus 3, V1-311 och V1-312, var och en med {N218.79} {U} byggyta, en terrass på {N103.98} {U} och en solterrass på {N127.58} {U} ovanpå, två parkeringsplatser och ett förråd.')

a('.residences.items[0].points[1]',
  'Dos viviendas en el edificio circular, el bloque 7: V1-701 en planta baja, con una terraza de {N232.39} {U} y un jardín de {N191.75} {U}, y V1-711 en la primera planta, con una terraza de unos 130 {U}. Ambas tienen tres dormitorios, cada uno con su propio baño, tres plazas de garaje y un trastero.',
  'Deux logements dans le bâtiment circulaire, l’immeuble 7 : V1-701 au rez-de-chaussée, avec une terrasse de {N232.39} {U} et un jardin de {N191.75} {U}, et V1-711 au premier étage, avec une terrasse d’environ 130 {U}. Tous deux ont trois chambres, chacune avec sa salle de bains, trois places de parking et un cellier.',
  'Zwei Wohnungen im runden Gebäude, Block 7: V1-701 im Erdgeschoss mit einer Terrasse von {N232.39} {U} und einem Garten von {N191.75} {U}, und V1-711 im ersten Obergeschoss mit einer Terrasse von rund 130 {U}. Beide haben drei Schlafzimmer, jedes mit eigenem Bad, drei Stellplätze und einen Abstellraum.',
  'Две квартиры в круглом здании, корпус 7: V1-701 на первом этаже с террасой {N232.39} {U} и садом {N191.75} {U} и V1-711 на втором этаже с террасой около 130 {U}. В обеих по три спальни, у каждой своя ванная, три машиноместа и кладовая.',
  'مسكنان في المبنى الدائري، المبنى 7: V1-701 في الطابق الأرضي بتراس مساحته {N232.39} {U} وحديقة مساحتها {N191.75} {U}، وV1-711 في الطابق الأول بتراس مساحته نحو 130 {U}. ولكل منهما ثلاث غرف نوم، لكل غرفة حمّامها، وثلاثة مواقف للسيارات ومخزن.',
  'Twee woningen in het ronde gebouw, Blok 7: V1-701 op de begane grond met een terras van {N232.39} {U} en een tuin van {N191.75} {U}, en V1-711 op de eerste verdieping met een terras van ongeveer 130 {U}. Beide hebben drie slaapkamers, elk met een eigen badkamer, drie parkeerplaatsen en een berging.',
  'Dwa mieszkania w okrągłym budynku, budynek 7: V1-701 na parterze z tarasem {N232.39} {U} i ogrodem {N191.75} {U} oraz V1-711 na pierwszym piętrze z tarasem około 130 {U}. Oba mają trzy sypialnie, każdą z własną łazienką, trzy miejsca postojowe i komórkę lokatorską.',
  'To boliger i den runde bygningen, Hus 7: V1-701 i første etasje med en terrasse på {N232.39} {U} og en hage på {N191.75} {U}, og V1-711 i andre etasje med en terrasse på omtrent 130 {U}. Begge har tre soverom, hvert med eget bad, tre parkeringsplasser og en bod.',
  'Två bostäder i den runda byggnaden, Hus 7: V1-701 på bottenvåningen med en terrass på {N232.39} {U} och en trädgård på {N191.75} {U}, och V1-711 på första våningen med en terrass på omkring 130 {U}. Båda har tre sovrum, vart och ett med eget badrum, tre parkeringsplatser och ett förråd.')

a('.residences.items[0].points[2]',
  'El jardín de V1-701 figura en su plano como zona común de uso privativo de la vivienda, no como terreno que se vende con ella.',
  'Le jardin de V1-701 figure sur son plan comme partie commune à usage privatif du logement, et non comme un terrain vendu avec lui.',
  'Der Garten von V1-701 ist auf seinem Grundriss als Gemeinschaftsfläche zur privaten Nutzung der Wohnung ausgewiesen, nicht als mitverkauftes Grundstück.',
  'Сад V1-701 обозначен на его планировке как общая территория в частном пользовании квартиры, а не земля, продаваемая вместе с ней.',
  'حديقة V1-701 مُعلَّمة في مخططها كأرض مشتركة مخصصة للاستخدام الخاص للمسكن، لا كأرض تُباع معه.',
  'De tuin van V1-701 staat op de plattegrond aangegeven als gemeenschappelijke grond voor privégebruik door de woning, niet als grond die erbij wordt verkocht.',
  'Ogród V1-701 jest oznaczony na rzucie jako teren wspólny w prywatnym użytkowaniu mieszkania, a nie grunt sprzedawany wraz z nim.',
  'Hagen til V1-701 er på plantegningen markert som fellesareal til privat bruk for boligen, ikke som grunn som selges med den.',
  'Trädgården till V1-701 är på planritningen markerad som gemensam mark för bostadens privata bruk, inte som mark som säljs med den.')

a('.residences.items[0].points[3]',
  'La lista de la fase I de la promotora muestra V1-311 rebajado de {E2590000} a {E2290000} con el mobiliario del salón incluido, y V1-312 rebajado de {E2690000} a {E2390000}.',
  'La liste de la phase I du promoteur indique V1-311 ramené de {E2590000} à {E2290000}, mobilier du salon inclus, et V1-312 ramené de {E2690000} à {E2390000}.',
  'Die Preisliste des Bauträgers für Phase I führt V1-311 reduziert von {E2590000} auf {E2290000}, einschließlich der Wohnzimmermöbel, und V1-312 reduziert von {E2690000} auf {E2390000}.',
  'В прайс-листе застройщика по очереди I цена V1-311 снижена с {E2590000} до {E2290000} с мебелью для гостиной, а V1-312 — с {E2690000} до {E2390000}.',
  'تُظهر قائمة المطوّر للمرحلة I خفض سعر V1-311 من {E2590000} إلى {E2290000} مع أثاث صالة الجلوس، وخفض سعر V1-312 من {E2690000} إلى {E2390000}.',
  'De lijst van de ontwikkelaar voor Fase I toont V1-311 verlaagd van {E2590000} naar {E2290000}, inclusief het loungemeubilair, en V1-312 verlaagd van {E2690000} naar {E2390000}.',
  'Cennik dewelopera dla etapu I pokazuje obniżkę V1-311 z {E2590000} do {E2290000} z meblami do salonu w cenie oraz V1-312 z {E2690000} do {E2390000}.',
  'Utbyggerens liste for byggetrinn I viser V1-311 satt ned fra {E2590000} til {E2290000} med loungemøblene inkludert, og V1-312 satt ned fra {E2690000} til {E2390000}.',
  'Exploatörens lista för etapp I visar V1-311 sänkt från {E2590000} till {E2290000} med loungemöblerna inkluderade, och V1-312 sänkt från {E2690000} till {E2390000}.')

a('.residences.items[1].name',
  'Fase II, en construcción',
  'Phase II, en construction',
  'Phase II, im Bau',
  'Очередь II, строится',
  'المرحلة II، قيد الإنشاء',
  'Fase II, in aanbouw',
  'Etap II, w budowie',
  'Byggetrinn II, under bygging',
  'Etapp II, under uppförande')

a('.residences.items[1].points[0]',
  'Una vivienda disponible, V2-101: una vivienda de tres dormitorios en planta baja en el bloque 1, con {N176.39} {U} construidos, una terraza de {N147.68} {U} y un jardín de {N107.36} {U}, por {E1895000}.',
  'Un logement disponible, V2-101 : un logement de trois chambres en rez-de-chaussée dans l’immeuble 1, avec {N176.39} {U} construits, une terrasse de {N147.68} {U} et un jardin de {N107.36} {U}, à {E1895000}.',
  'Eine Wohnung verfügbar, V2-101: eine Erdgeschosswohnung mit drei Schlafzimmern in Block 1 mit {N176.39} {U} bebauter Fläche, einer Terrasse von {N147.68} {U} und einem Garten von {N107.36} {U}, für {E1895000}.',
  'Свободна одна квартира, V2-101: квартира с тремя спальнями на первом этаже корпуса 1, площадь застройки {N176.39} {U}, терраса {N147.68} {U} и сад {N107.36} {U}, за {E1895000}.',
  'مسكن واحد متاح، V2-101: مسكن بثلاث غرف نوم في الطابق الأرضي من المبنى 1، بمساحة مبنية قدرها {N176.39} {U}، وتراس بمساحة {N147.68} {U}، وحديقة بمساحة {N107.36} {U}، بسعر {E1895000}.',
  'Eén woning beschikbaar, V2-101: een benedenwoning met drie slaapkamers in Blok 1 met {N176.39} {U} bebouwd, een terras van {N147.68} {U} en een tuin van {N107.36} {U}, voor {E1895000}.',
  'Dostępne jest jedno mieszkanie, V2-101: mieszkanie z trzema sypialniami na parterze budynku 1, z {N176.39} {U} powierzchni zabudowy, tarasem {N147.68} {U} i ogrodem {N107.36} {U}, za {E1895000}.',
  'Én bolig ledig, V2-101: en bolig med tre soverom i første etasje i Hus 1 med {N176.39} {U} bebygd areal, en terrasse på {N147.68} {U} og en hage på {N107.36} {U}, til {E1895000}.',
  'En bostad ledig, V2-101: en bottenvåning med tre sovrum i Hus 1 med {N176.39} {U} byggyta, en terrass på {N147.68} {U} och en trädgård på {N107.36} {U}, för {E1895000}.')

a('.residences.items[1].points[1]',
  'No disponemos de un plano individual de V2-101, solo del plano de la promotora para su tipología, por lo que no se indica su superficie útil.',
  'Nous ne disposons pas de plan individuel pour V2-101, seulement du plan du promoteur pour sa typologie ; sa surface utile n’est donc pas indiquée.',
  'Für V2-101 liegt uns kein eigener Grundriss vor, nur der Grundriss des Bauträgers für den Wohnungstyp; die Nutzfläche wird daher nicht angegeben.',
  'Индивидуальной планировки V2-101 у нас нет, только типовая планировка застройщика, поэтому полезная площадь не указана.',
  'لا نملك مخططاً فردياً للوحدة V2-101، بل مخطط المطوّر لنوعها فقط، لذا لا تُعرض مساحتها الصافية.',
  'Wij hebben voor V2-101 geen eigen plattegrond, alleen de plattegrond van de ontwikkelaar voor het type, dus de bruikbare oppervlakte wordt niet getoond.',
  'Nie mamy indywidualnego rzutu V2-101, tylko rzut dewelopera dla jego typu, dlatego powierzchnia użytkowa nie jest podana.',
  'Vi har ingen egen plantegning for V2-101, bare utbyggerens tegning av boligtypen, så boarealet vises ikke.',
  'Vi har ingen egen planritning för V2-101, bara exploatörens ritning av bostadstypen, så boytan visas inte.')

a('.residences.items[1].points[2]',
  'El documento informativo abreviado (DIA) de la primera parte de esta fase, 22 viviendas en dos bloques, fija la entrega en el cuarto trimestre de 2026; los vídeos de 2026 de la promotora sobre sus últimas viviendas hablan del tercer trimestre de 2027.',
  'Le document d’information abrégé de la première partie de cette phase, 22 logements en deux immeubles, prévoit la livraison au quatrième trimestre 2026 ; les films 2026 du promoteur sur ses derniers logements parlent du troisième trimestre 2027.',
  'Das Kurzinformationsblatt (DIA) für den ersten Teil dieser Phase, 22 Wohnungen in zwei Gebäuden, nennt die Übergabe im vierten Quartal 2026; die Filme des Bauträgers von 2026 über die letzten Wohnungen nennen das dritte Quartal 2027.',
  'Краткий информационный документ (DIA) для первой части этой очереди, 22 квартиры в двух корпусах, указывает сдачу в четвёртом квартале 2026 года; в фильмах застройщика 2026 года о последних квартирах очереди назван третий квартал 2027 года.',
  'تحدد الوثيقة الإعلامية المختصرة (DIA) للجزء الأول من هذه المرحلة، 22 مسكنًا في مبنيين، التسليم في الربع الرابع من عام 2026، بينما تذكر أفلام المطوّر لعام 2026 عن آخر مساكنها الربع الثالث من عام 2027.',
  'Het beknopt informatiedocument (DIA) voor het eerste deel van deze fase, 22 woningen in twee blokken, noemt oplevering in het vierde kwartaal van 2026; de films van de ontwikkelaar uit 2026 over de laatste woningen noemen het derde kwartaal van 2027.',
  'Skrócony dokument informacyjny (DIA) dla pierwszej części tego etapu, 22 mieszkania w dwóch budynkach, podaje odbiór w czwartym kwartale 2026 r.; filmy dewelopera z 2026 r. o ostatnich mieszkaniach mówią o trzecim kwartale 2027 r.',
  'Det kortfattede informasjonsdokumentet (DIA) for den første delen av dette byggetrinnet, 22 boliger i to bygg, oppgir overlevering i fjerde kvartal 2026; utbyggerens filmer fra 2026 om de siste boligene sier tredje kvartal 2027.',
  'Det kortfattade informationsdokumentet (DIA) för den första delen av denna etapp, 22 bostäder i två hus, anger tillträde under fjärde kvartalet 2026; exploatörens filmer från 2026 om de sista bostäderna säger tredje kvartalet 2027.')

a('.residences.items[2].name',
  'Fase III, en construcción',
  'Phase III, en construction',
  'Phase III, im Bau',
  'Очередь III, строится',
  'المرحلة III، قيد الإنشاء',
  'Fase III, in aanbouw',
  'Etap III, w budowie',
  'Byggetrinn III, under bygging',
  'Etapp III, under uppförande')

a('.residences.items[2].points[0]',
  'Quince viviendas en los bloques 3 a 6: apartamentos de dos dormitorios desde {E999000}, apartamentos de tres dormitorios desde {E1495000}, y áticos de tres y cuatro dormitorios de {E2490000} a {E2750000}.',
  'Quinze logements dans les immeubles 3 à 6 : appartements de deux chambres à partir de {E999000}, appartements de trois chambres à partir de {E1495000}, et attiques de trois et quatre chambres de {E2490000} à {E2750000}.',
  'Fünfzehn Wohnungen in den Blöcken 3 bis 6: Wohnungen mit zwei Schlafzimmern ab {E999000}, Wohnungen mit drei Schlafzimmern ab {E1495000} und Penthäuser mit drei und vier Schlafzimmern von {E2490000} bis {E2750000}.',
  'Пятнадцать квартир в корпусах 3–6: квартиры с двумя спальнями от {E999000}, с тремя спальнями от {E1495000} и пентхаусы с тремя и четырьмя спальнями от {E2490000} до {E2750000}.',
  'خمس عشرة وحدة في المباني من 3 إلى 6: شقق بغرفتي نوم ابتداءً من {E999000}، وشقق بثلاث غرف نوم ابتداءً من {E1495000}، وبنتهاوس بثلاث وأربع غرف نوم من {E2490000} إلى {E2750000}.',
  'Vijftien woningen in Blok 3 tot en met 6: appartementen met twee slaapkamers vanaf {E999000}, appartementen met drie slaapkamers vanaf {E1495000}, en penthouses met drie en vier slaapkamers van {E2490000} tot {E2750000}.',
  "Piętnaście mieszkań w budynkach 3–6: mieszkania z dwiema sypialniami od {E999000}, z trzema sypialniami od {E1495000} oraz penthouse'y z trzema i czterema sypialniami od {E2490000} do {E2750000}.",
  'Femten boliger i Hus 3 til 6: leiligheter med to soverom fra {E999000}, leiligheter med tre soverom fra {E1495000}, og toppleiligheter med tre og fire soverom fra {E2490000} til {E2750000}.',
  'Femton bostäder i Hus 3 till 6: lägenheter med två sovrum från {E999000}, lägenheter med tre sovrum från {E1495000}, och takvåningar med tre och fyra sovrum från {E2490000} till {E2750000}.')

a('.residences.items[2].points[1]',
  'Las viviendas en planta baja tienen terraza y jardín con piscina privada; en los planos de las viviendas de dos dormitorios y de tres dormitorios tipo B del bloque 6 se añade una zona de fuego. Los planos señalan el jardín y la piscina como zona común de uso privativo de la vivienda.',
  'Les logements en rez-de-chaussée ont une terrasse et un jardin avec piscine privée ; sur les plans des logements de deux chambres et de trois chambres de type B de l’immeuble 6 s’ajoute un coin brasero. Les plans désignent le jardin et la piscine comme partie commune à usage privatif du logement.',
  'Die Erdgeschosswohnungen haben eine Terrasse und einen Garten mit privatem Pool; auf den Grundrissen der Wohnungen mit zwei Schlafzimmern und mit drei Schlafzimmern Typ B in Block 6 kommt ein Bereich mit Feuerstelle hinzu. Die Grundrisse weisen Garten und Pool als Gemeinschaftsfläche zur privaten Nutzung der Wohnung aus.',
  'У квартир на первом этаже есть терраса и сад с собственным бассейном; на планировках квартир с двумя спальнями и квартир с тремя спальнями типа B в корпусе 6 добавлена зона с очагом. На планировках сад и бассейн обозначены как общая территория в частном пользовании квартиры.',
  'لمساكن الطابق الأرضي تراس وحديقة بمسبح خاص؛ وفي مخططات المساكن بغرفتي نوم والمساكن بثلاث غرف من النوع B في المبنى 6 تُضاف منطقة لموقد النار. وتصنّف المخططات الحديقة والمسبح كأرض مشتركة مخصصة للاستخدام الخاص للمسكن.',
  'Benedenwoningen hebben een terras en een tuin met een privézwembad; op de plattegronden van de woningen met twee slaapkamers en het type B met drie slaapkamers in Blok 6 komt daar een zone met vuurplaats bij. De plattegronden geven tuin en zwembad aan als gemeenschappelijke grond voor privégebruik door de woning.',
  'Mieszkania na parterze mają taras i ogród z prywatnym basenem; na rzutach mieszkań z dwiema sypialniami i mieszkań z trzema sypialniami typu B w budynku 6 dochodzi strefa z paleniskiem. Rzuty oznaczają ogród i basen jako teren wspólny w prywatnym użytkowaniu mieszkania.',
  'Boligene i første etasje har terrasse og hage med privat basseng; på plantegningene til boligene med to soverom og type B med tre soverom i Hus 6 kommer et område med bålsted i tillegg. Plantegningene markerer hage og basseng som fellesareal til privat bruk for boligen.',
  'Bottenvåningarna har en terrass och en trädgård med egen pool; på planritningarna för bostäderna med två sovrum och typ B med tre sovrum i Hus 6 tillkommer en yta med eldstad. Planritningarna markerar trädgård och pool som gemensam mark för bostadens privata bruk.')

a('.residences.items[2].points[2]',
  'Los áticos tienen un solárium de {N123.50} a {N155.86} {U} al que se sube por una escalera privada, con piscina en su plano.',
  'Les attiques disposent d’un solarium de {N123.50} à {N155.86} {U}, accessible par un escalier privé, avec une piscine sur leur plan.',
  'Die Penthäuser haben ein Solarium von {N123.50} bis {N155.86} {U}, erreichbar über eine private Treppe, auf dem Grundriss mit Pool.',
  'У пентхаусов есть солярий площадью от {N123.50} до {N155.86} {U}, на который ведёт собственная лестница, на планировке — с бассейном.',
  'للبنتهاوس سولاريوم بمساحة من {N123.50} إلى {N155.86} {U} يُصعد إليه بدرج خاص، ويظهر عليه مسبح في المخطط.',
  'Penthouses hebben een solarium van {N123.50} tot {N155.86} {U}, bereikbaar via een eigen trap, met een zwembad op de plattegrond.',
  "Penthouse'y mają solarium o powierzchni od {N123.50} do {N155.86} {U}, na które prowadzą prywatne schody, z basenem na rzucie.",
  'Toppleilighetene har en solterrasse på {N123.50} til {N155.86} {U}, med egen trapp opp, og basseng på plantegningen.',
  'Takvåningarna har en solterrass på {N123.50} till {N155.86} {U}, nåbar via en egen trappa, med pool på planritningen.')

a('.residences.items[2].points[3]',
  'Ningún documento da fecha de entrega para esta fase. El vídeo de obra de la promotora de febrero de 2026 muestra cómo se ejecutan sus cimientos.',
  'Aucun document ne donne de date de livraison pour cette phase. Le film de chantier du promoteur de février 2026 montre la pose de ses fondations.',
  'Für diese Phase nennt kein Dokument einen Übergabetermin. Der Baustellenfilm des Bauträgers vom Februar 2026 zeigt, wie ihre Fundamente gelegt werden.',
  'Ни один документ не указывает срок сдачи этой очереди. В строительном фильме застройщика за февраль 2026 года видно, как закладывается её фундамент.',
  'لا تذكر أي وثيقة موعد تسليم لهذه المرحلة. ويُظهر فيلم البناء الذي أعدّه المطوّر في فبراير 2026 أعمال صبّ أساساتها.',
  'Geen enkel document noemt een opleverdatum voor deze fase. De bouwfilm van de ontwikkelaar van februari 2026 toont hoe de fundering wordt gelegd.',
  'Żaden dokument nie podaje terminu odbioru tego etapu. Film budowy dewelopera z lutego 2026 r. pokazuje wylewanie jego fundamentów.',
  'Ingen dokumenter oppgir en overleveringsdato for dette byggetrinnet. Utbyggerens byggefilm fra februar 2026 viser at fundamentene legges.',
  'Inget dokument anger något tillträdesdatum för denna etapp. Exploatörens byggfilm från februari 2026 visar hur grunden läggs.')

a('.residences.items[3].name',
  'En todas las viviendas',
  'Dans chaque logement',
  'In jeder Wohnung',
  'В каждой квартире',
  'في كل مسكن',
  'In elke woning',
  'W każdym mieszkaniu',
  'I alle boliger',
  'I varje bostad')

a('.residences.items[3].points[0]',
  'Cocina abierta al salón, aseo de cortesía, lavadero o cuarto técnico y un baño por dormitorio; el dormitorio principal tiene vestidor.',
  'Cuisine ouverte sur le séjour, WC invités, buanderie ou local technique et une salle de bains par chambre ; la chambre principale dispose d’un dressing.',
  'Offene Küche mit Wohnzimmer, Gäste-WC, Waschküche oder Technikraum und ein Bad zu jedem Schlafzimmer; das Hauptschlafzimmer hat einen Ankleideraum.',
  'Кухня открытой планировки, совмещённая с гостиной, гостевой туалет, постирочная или техническое помещение и ванная при каждой спальне; в главной спальне есть гардеробная.',
  'مطبخ مفتوح على صالة المعيشة، ومرحاض للضيوف، وغرفة غسيل أو غرفة فنية، وحمّام لكل غرفة نوم؛ ولغرفة النوم الرئيسية غرفة ملابس.',
  'Open keuken en woonkamer, een gastentoilet, een was- of technische ruimte, en bij elke slaapkamer een badkamer; de hoofdslaapkamer heeft een kleedkamer.',
  'Kuchnia otwarta na salon, toaleta dla gości, pralnia lub pomieszczenie techniczne oraz łazienka przy każdej sypialni; główna sypialnia ma garderobę.',
  'Åpen kjøkken- og stueløsning, gjestetoalett, vaskerom eller teknisk rom, og eget bad til hvert soverom; hovedsoverommet har garderoberom.',
  'Öppen planlösning med kök och vardagsrum, gästtoalett, tvättstuga eller teknikrum, och ett badrum till varje sovrum; huvudsovrummet har ett klädrum.')

a('.residences.items[3].points[1]',
  'De una a tres plazas de garaje y un trastero en las listas de precios; una plaza adicional cuesta {E50000}, con disponibilidad limitada.',
  'Une à trois places de parking et un cellier sur les listes de prix ; une place supplémentaire coûte {E50000}, dans la limite des disponibilités.',
  'Ein bis drei Stellplätze und ein Abstellraum laut Preislisten; ein zusätzlicher Stellplatz kostet {E50000}, nur begrenzt verfügbar.',
  'По прайс-листам — от одного до трёх машиномест и кладовая; дополнительное место стоит {E50000}, их количество ограничено.',
  'تتضمن قوائم الأسعار من موقف إلى ثلاثة مواقف للسيارات ومخزناً؛ ويكلّف الموقف الإضافي {E50000}، والعدد محدود.',
  'Eén tot drie parkeerplaatsen en een berging volgens de prijslijsten; een extra plaats kost {E50000}, met beperkte beschikbaarheid.',
  'Według cenników od jednego do trzech miejsc postojowych i komórka lokatorska; dodatkowe miejsce kosztuje {E50000}, liczba jest ograniczona.',
  'Én til tre parkeringsplasser og en bod ifølge prislistene; en ekstra plass koster {E50000}, og det er begrenset tilgang.',
  'En till tre parkeringsplatser och ett förråd enligt prislistorna; en extra plats kostar {E50000}, med begränsad tillgång.')

a('.qualitySpecs.copy',
  'La memoria de calidades de la promotora para la primera fase, resumida por partes de la vivienda. Donde el edificio circular difiere, se indica.',
  'Le descriptif des prestations du promoteur pour la première phase, résumé par partie du logement. Lorsque le bâtiment circulaire diffère, c’est précisé.',
  'Die Baubeschreibung des Bauträgers für die erste Phase, zusammengefasst nach Bereichen der Wohnung. Wo das runde Gebäude abweicht, ist es vermerkt.',
  'Спецификация застройщика для первой очереди, кратко по частям квартиры. Где круглое здание отличается, это указано.',
  'مواصفات المطوّر للمرحلة الأولى، ملخّصة حسب أجزاء المسكن. وحيث يختلف المبنى الدائري، يُشار إلى ذلك.',
  'De specificatie van de ontwikkelaar voor de eerste fase, samengevat per onderdeel van de woning. Waar het ronde gebouw afwijkt, staat dat erbij.',
  'Specyfikacja dewelopera dla pierwszego etapu, w skrócie według części mieszkania. Tam, gdzie okrągły budynek się różni, jest to zaznaczone.',
  'Utbyggerens spesifikasjon for første byggetrinn, oppsummert etter deler av boligen. Der den runde bygningen skiller seg ut, er det nevnt.',
  'Exploatörens specifikation för första etappen, sammanfattad efter delar av bostaden. Där den runda byggnaden avviker anges det.')

a('.qualitySpecs.sourceNote',
  'Fuente: las memorias de calidades de la promotora para los bloques 1 a 6 y para el bloque 7, el edificio circular, de la primera fase. No llevan fecha, indican que las calidades pueden cambiar por motivos técnicos y añaden que la promotora ofrece un plan de personalización con precio aparte. No disponemos de memoria de calidades de las fases II y III y la solicitamos antes de la reserva.',
  'Source : les descriptifs des prestations du promoteur pour les immeubles 1 à 6 et pour l’immeuble 7, le bâtiment circulaire, de la première phase. Ils ne sont pas datés, précisent que les prestations peuvent changer pour des raisons techniques et ajoutent que le promoteur propose un plan de personnalisation facturé à part. Nous n’avons pas de descriptif pour les phases II et III et le demandons avant la réservation.',
  'Quelle: die Baubeschreibungen des Bauträgers für die Blöcke 1 bis 6 und für Block 7, das runde Gebäude, der ersten Phase. Sie tragen kein Datum, sagen, dass sich die Ausstattung aus technischen Gründen ändern kann, und fügen hinzu, dass der Bauträger ein gesondert berechnetes Individualisierungsprogramm anbietet. Für die Phasen II und III liegt uns keine Baubeschreibung vor; wir fordern sie vor der Reservierung an.',
  'Источник: спецификации качества застройщика для корпусов 1–6 и для корпуса 7, круглого здания, первой очереди. Они не датированы, указывают, что спецификации могут меняться по техническим причинам, и добавляют, что застройщик предлагает план индивидуализации за отдельную плату. Спецификации для очередей II и III у нас нет; мы запрашиваем её до бронирования.',
  'المصدر: مواصفات الجودة الصادرة عن المطوّر للمباني من 1 إلى 6 وللمبنى 7، المبنى الدائري، في المرحلة الأولى. وهي غير مؤرخة، وتنص على أن المواصفات قد تتغير لأسباب فنية، وتضيف أن المطوّر يقدّم خطة تخصيص بسعر منفصل. ولا نملك مواصفات للمرحلتين II وIII، ونطلبها قبل الحجز.',
  'Bron: de kwaliteitsspecificaties van de ontwikkelaar voor Blok 1 tot en met 6 en voor Blok 7, het ronde gebouw, van de eerste fase. Ze zijn niet gedateerd, vermelden dat de specificaties om technische redenen kunnen wijzigen en voegen eraan toe dat de ontwikkelaar een apart geprijsd personalisatieplan aanbiedt. Voor Fase II en III hebben wij geen specificatie; wij vragen die op vóór de reservering.',
  'Źródło: specyfikacje jakości dewelopera dla budynków 1–6 oraz dla budynku 7, okrągłego, pierwszego etapu. Nie mają daty, zastrzegają, że specyfikacja może się zmienić z przyczyn technicznych, i dodają, że deweloper oferuje odpłatny plan personalizacji. Nie mamy specyfikacji dla etapów II i III i prosimy o nią przed rezerwacją.',
  'Kilde: utbyggerens kvalitetsspesifikasjoner for Hus 1 til 6 og for Hus 7, den runde bygningen, i første byggetrinn. De er udaterte, sier at spesifikasjonene kan endres av tekniske årsaker, og legger til at utbyggeren tilbyr en tilpasningsplan som prises separat. Vi har ingen spesifikasjon for byggetrinn II og III og ber om den før reservasjon.',
  'Källa: exploatörens kvalitetsspecifikationer för Hus 1 till 6 och för Hus 7, den runda byggnaden, i första etappen. De saknar datum, anger att specifikationerna kan ändras av tekniska skäl och tillägger att exploatören erbjuder en separat prissatt anpassningsplan. Vi har ingen specifikation för etapp II och III och begär den före bokning.')

a('.qualitySpecs.groups[0].name',
  'Estructura y aislamiento',
  'Structure et isolation',
  'Tragwerk und Dämmung',
  'Конструкция и изоляция',
  'الهيكل والعزل',
  'Constructie en isolatie',
  'Konstrukcja i izolacja',
  'Konstruksjon og isolasjon',
  'Stomme och isolering')

a('.qualitySpecs.groups[0].items[0]',
  'Cimentación y estructura de hormigón armado, con muros exteriores de hormigón armado aislados: 8 cm de aislamiento por fuera y 4 cm por dentro.',
  'Fondations et structure en béton armé, avec des murs extérieurs en béton armé isolés : 8 cm d’isolant à l’extérieur et 4 cm à l’intérieur.',
  'Fundamente und Tragwerk aus Stahlbeton, mit gedämmten Außenwänden aus Stahlbeton: 8 cm Dämmung außen und 4 cm innen.',
  'Фундамент и каркас из железобетона, наружные стены из утеплённого железобетона: 8 см изоляции снаружи и 4 см изнутри.',
  'أساسات وهيكل من الخرسانة المسلحة، وجدران خارجية من الخرسانة المسلحة المعزولة: 8 سم من العزل من الخارج و4 سم من الداخل.',
  'Fundering en draagconstructie van gewapend beton, met geïsoleerde buitenmuren van gewapend beton: 8 cm isolatie aan de buitenzijde en 4 cm aan de binnenzijde.',
  'Fundamenty i szkielet z żelbetu, ocieplone ściany zewnętrzne z żelbetu: 8 cm izolacji od zewnątrz i 4 cm od wewnątrz.',
  'Fundamenter og bærekonstruksjon i armert betong, med isolerte yttervegger i armert betong: 8 cm isolasjon utvendig og 4 cm innvendig.',
  'Grund och stomme i armerad betong, med isolerade ytterväggar i armerad betong: 8 cm isolering utvändigt och 4 cm invändigt.')

a('.qualitySpecs.groups[0].items[1]',
  'Cubiertas planas invertidas con aislamiento continuo y doble lámina asfáltica impermeabilizante; tabiques de placa de yeso aislados con lana de roca.',
  'Toitures plates inversées avec isolation continue et double membrane d’étanchéité bitumineuse ; cloisons en plaques de plâtre isolées à la laine de roche.',
  'Flache Umkehrdächer mit durchgehender Dämmung und doppelter Bitumenabdichtung; gedämmte Gipskartonwände mit Steinwolle.',
  'Плоские инверсионные кровли со сплошной теплоизоляцией и двойной битумной гидроизоляцией; перегородки из гипсокартона с утеплителем из минеральной ваты.',
  'أسطح مستوية معكوسة بعزل متواصل وطبقة مزدوجة من الأغشية الإسفلتية المانعة لتسرب الماء؛ وقواطع من ألواح الجبس المعزولة بالصوف الصخري.',
  'Platte omgekeerde daken met doorlopende isolatie en een dubbele bitumineuze dakbaan; geïsoleerde scheidingswanden van gipsplaat met steenwol.',
  'Płaskie dachy odwrócone z ciągłą izolacją i podwójną hydroizolacją z papy asfaltowej; ścianki działowe z płyt gipsowo-kartonowych z wełną mineralną.',
  'Flate, omvendte tak med sammenhengende isolasjon og dobbelt lag asfaltpapp som tetting; isolerte skillevegger i gipsplater med steinull.',
  'Platta omvända tak med obruten isolering och dubbel asfaltsmatta som tätskikt; isolerade innerväggar av gipsskivor med stenull.')

a('.qualitySpecs.groups[1].name',
  'Suelos y carpintería exterior',
  'Sols et menuiseries',
  'Böden und Verglasung',
  'Полы и остекление',
  'الأرضيات والزجاج',
  'Vloeren en beglazing',
  'Podłogi i przeszklenia',
  'Gulv og glass',
  'Golv och glas')

a('.qualitySpecs.groups[1].items[0]',
  'Suelos interiores de porcelánico de gran formato, de 100 por 100 cm, y la misma colección, antideslizante, en las terrazas; en el edificio circular, porcelánico con acabado madera.',
  'Sols intérieurs en grès cérame grand format, 100 par 100 cm, et la même collection, antidérapante, sur les terrasses ; dans le bâtiment circulaire, grès cérame aspect bois.',
  'Großformatige Feinsteinzeugböden innen, 100 mal 100 cm, und dieselbe Kollektion rutschfest auf den Terrassen; im runden Gebäude Feinsteinzeug in Holzoptik.',
  'Крупноформатный керамогранит в интерьере, 100 на 100 см, и та же коллекция с противоскользящей поверхностью на террасах; в круглом здании — керамогранит под дерево.',
  'أرضيات داخلية من البورسلين كبير الحجم، 100 في 100 سم، والمجموعة نفسها بسطح مانع للانزلاق على التراسات؛ وفي المبنى الدائري بورسلين بلمسة خشبية.',
  'Binnen porseleinen vloeren in groot formaat, 100 bij 100 cm, en dezelfde collectie, antislip, op de terrassen; in het ronde gebouw porselein met een houtlook.',
  'Wielkoformatowe płyty gresowe we wnętrzach, 100 na 100 cm, i ta sama kolekcja w wersji antypoślizgowej na tarasach; w okrągłym budynku gres imitujący drewno.',
  'Storformat porselensfliser innendørs, 100 ganger 100 cm, og samme kolleksjon, sklisikker, på terrassene; i den runde bygningen porselen med trefinish.',
  'Storformatigt porslinsgolv inomhus, 100 gånger 100 cm, och samma kollektion, halkfri, på terrasserna; i den runda byggnaden porslin med träfinish.')

a('.qualitySpecs.groups[1].items[1]',
  'Carpintería de aluminio lacado con doble acristalamiento y control solar, y barandillas de vidrio de 110 cm de altura.',
  'Menuiseries en aluminium laqué avec double vitrage et protection solaire, et garde-corps en verre de 110 cm de haut.',
  'Lackierte Aluminiumrahmen mit Doppelverglasung und Sonnenschutz sowie Glasbrüstungen von 110 cm Höhe.',
  'Лакированные алюминиевые рамы с двойным остеклением и солнцезащитой, стеклянные ограждения высотой 110 см.',
  'إطارات من الألومنيوم المطلي بزجاج مزدوج وحماية من الشمس، ودرابزينات زجاجية بارتفاع 110 سم.',
  'Gelakte aluminium kozijnen met dubbele beglazing en zonwering, en glazen balustrades van 110 cm hoog.',
  'Lakierowane ramy aluminiowe z podwójnym szkleniem i ochroną przeciwsłoneczną oraz szklane balustrady o wysokości 110 cm.',
  'Lakkerte aluminiumsrammer med doble glass og solbeskyttelse, og glassrekkverk 110 cm høye.',
  'Lackerade aluminiumkarmar med tvåglasfönster och solskydd, samt glasräcken 110 cm höga.')

a('.qualitySpecs.groups[2].items[0]',
  'Muebles de cocina de suelo a techo con isla central y frontal de porcelánico, con electrodomésticos Miele o similares; Gaggenau o similares en el edificio circular.',
  'Meubles de cuisine du sol au plafond avec îlot central et crédence en grès cérame, électroménager Miele ou équivalent ; Gaggenau ou équivalent dans le bâtiment circulaire.',
  'Raumhohe Küchenmöbel mit Kochinsel und Rückwand aus Feinsteinzeug, mit Geräten von Miele oder gleichwertig; im runden Gebäude Gaggenau oder gleichwertig.',
  'Кухонная мебель от пола до потолка с центральным островом и фартуком из керамогранита, техника Miele или аналог; в круглом здании — Gaggenau или аналог.',
  'وحدات مطبخ من الأرض حتى السقف مع جزيرة مركزية وواجهة خلفية من البورسلين، وأجهزة Miele أو ما يماثلها؛ وGaggenau أو ما يماثلها في المبنى الدائري.',
  'Keukenkasten van vloer tot plafond met een kookeiland en een spatwand van porselein, met apparatuur van Miele of gelijkwaardig; in het ronde gebouw Gaggenau of gelijkwaardig.',
  'Zabudowa kuchenna od podłogi do sufitu z wyspą centralną i ścianą z gresu, ze sprzętem Miele lub podobnym; w okrągłym budynku Gaggenau lub podobny.',
  'Kjøkkenskap fra gulv til tak med kjøkkenøy og sprutvegg i porselen, med hvitevarer fra Miele eller tilsvarende; Gaggenau eller tilsvarende i den runde bygningen.',
  'Köksskåp från golv till tak med köksö och stänkskydd i porslin, med vitvaror från Miele eller likvärdigt; Gaggenau eller likvärdigt i den runda byggnaden.')

a('.qualitySpecs.groups[2].items[1]',
  'Un lavadero independiente con lavadora y secadora.',
  'Une buanderie séparée avec lave-linge et sèche-linge.',
  'Ein separater Hauswirtschaftsraum mit Waschmaschine und Trockner.',
  'Отдельная постирочная со стиральной и сушильной машинами.',
  'غرفة غسيل مستقلة مع غسالة ومجففة ملابس.',
  'Een aparte wasruimte met wasmachine en droger.',
  'Osobna pralnia z pralką i suszarką.',
  'Et eget vaskerom med vaskemaskin og tørketrommel.',
  'En separat tvättstuga med tvättmaskin och torktumlare.')

a('.qualitySpecs.groups[3].items[0]',
  'Porcelánico de suelo a techo en las duchas, inodoros suspendidos y muebles de lavabo volados.',
  'Grès cérame du sol au plafond dans les douches, WC suspendus et meubles vasques suspendus.',
  'Feinsteinzeug raumhoch in den Duschen, wandhängende WCs und Waschtischunterschränke.',
  'Керамогранит от пола до потолка в душевых, подвесные унитазы и подвесные тумбы под раковину.',
  'تكسية بالبورسلين من الأرض حتى السقف في أماكن الاستحمام، ومراحيض معلّقة، ووحدات مغاسل معلّقة على الجدار.',
  'Porseleinen tegels van vloer tot plafond in de douches, hangende toiletten en zwevende wastafelmeubels.',
  'Gres od podłogi do sufitu w prysznicach, podwieszane miski WC i wiszące szafki umywalkowe.',
  'Porselensfliser fra gulv til tak i dusjene, vegghengte toaletter og vegghengte servantskap.',
  'Porslinsplattor från golv till tak i duscharna, vägghängda toaletter och vägghängda kommodskåp.')

a('.qualitySpecs.groups[3].items[1]',
  'Bañera exenta y ducha de lluvia en el techo en el baño principal.',
  'Une baignoire îlot et une douche de pluie au plafond dans la salle de bains principale.',
  'Eine freistehende Badewanne und eine Regendusche an der Decke im Hauptbad.',
  'Отдельно стоящая ванна и потолочный тропический душ в главной ванной.',
  'حوض استحمام قائم بذاته ودشّ مطري سقفي في الحمّام الرئيسي.',
  'Een vrijstaand bad en een plafondregendouche in de hoofdbadkamer.',
  'Wolnostojąca wanna i sufitowa deszczownica w głównej łazience.',
  'Et frittstående badekar og en regndusj i taket på hovedbadet.',
  'Ett fristående badkar och en takmonterad regndusch i huvudbadrummet.')

a('.qualitySpecs.groups[4].items[0]',
  'Aire acondicionado por conductos, frío y calor, con termostato en el salón y en cada dormitorio.',
  'Climatisation gainable chaud et froid avec thermostat dans le séjour et dans chaque chambre.',
  'Kanal-Klimaanlage für Kühlen und Heizen mit Thermostat im Wohnzimmer und in jedem Schlafzimmer.',
  'Канальное кондиционирование на тепло и холод с термостатом в гостиной и каждой спальне.',
  'تكييف هواء بقنوات للتدفئة والتبريد مع منظم حرارة في صالة المعيشة وكل غرفة نوم.',
  'Kanaalgebonden airconditioning voor warmte en koeling, met een thermostaat in de woonkamer en in elke slaapkamer.',
  'Kanałowa klimatyzacja grzewczo-chłodząca z termostatem w salonie i każdej sypialni.',
  'Kanalbasert klimaanlegg for varme og kjøling, med termostat i stuen og hvert soverom.',
  'Kanalbaserad luftkonditionering för värme och kyla, med termostat i vardagsrummet och varje sovrum.')

a('.qualitySpecs.groups[4].items[1]',
  'Suelo radiante por agua en el salón y los dormitorios, suelo radiante eléctrico en los baños y agua caliente con depósito acumulador.',
  'Plancher chauffant hydraulique dans le séjour et les chambres, plancher chauffant électrique dans les salles de bains et eau chaude par ballon d’accumulation.',
  'Wasserführende Fußbodenheizung im Wohnzimmer und in den Schlafzimmern, elektrische Fußbodenheizung in den Bädern und Warmwasser aus einem Speicher.',
  'Водяной тёплый пол в гостиной и спальнях, электрический тёплый пол в ванных, горячая вода из бака-накопителя.',
  'تدفئة أرضية مائية في صالة المعيشة وغرف النوم، وتدفئة أرضية كهربائية في الحمّامات، ومياه ساخنة من خزان تجميع.',
  'Watergedragen vloerverwarming in de woonkamer en slaapkamers, elektrische vloerverwarming in de badkamers, en warm water uit een boilervat.',
  'Wodne ogrzewanie podłogowe w salonie i sypialniach, elektryczne ogrzewanie podłogowe w łazienkach i ciepła woda z zasobnika.',
  'Vannbåren gulvvarme i stuen og soverommene, elektrisk gulvvarme på badene, og varmtvann fra en akkumulatortank.',
  'Vattenburen golvvärme i vardagsrummet och sovrummen, elektrisk golvvärme i badrummen, och varmvatten från en ackumulatortank.')

a('.qualitySpecs.groups[5].name',
  'Puertas y tecnología',
  'Portes et technologie',
  'Türen und Technik',
  'Двери и технологии',
  'الأبواب والتقنيات',
  'Deuren en techniek',
  'Drzwi i technologia',
  'Dører og teknologi',
  'Dörrar och teknik')

a('.qualitySpecs.groups[5].items[0]',
  'Puerta de entrada de roble de 265 cm de altura con cerrojos de seguridad, y puertas interiores lacadas en blanco de 240 cm de altura.',
  'Porte d’entrée en chêne de 265 cm de haut avec verrous de sécurité, et portes intérieures laquées blanc de 240 cm de haut.',
  'Eine Eingangstür aus Eiche, 265 cm hoch, mit Sicherheitsverriegelung, und weiß lackierte Innentüren von 240 cm Höhe.',
  'Входная дубовая дверь высотой 265 см с защитными ригелями и белые лакированные межкомнатные двери высотой 240 см.',
  'باب أمامي من خشب البلوط بارتفاع 265 سم مع مزاليج أمان، وأبواب داخلية مطلية بالأبيض بارتفاع 240 سم.',
  'Een eikenhouten voordeur van 265 cm hoog met veiligheidsgrendels, en wit gelakte binnendeuren van 240 cm hoog.',
  'Dębowe drzwi wejściowe o wysokości 265 cm z ryglami antywłamaniowymi i białe lakierowane drzwi wewnętrzne o wysokości 240 cm.',
  'En inngangsdør i eik, 265 cm høy, med sikkerhetslåser, og hvitlakkerte innerdører 240 cm høye.',
  'En ytterdörr i ek, 265 cm hög, med säkerhetsregel, och vitlackerade innerdörrar 240 cm höga.')

a('.qualitySpecs.groups[5].items[1]',
  'Domótica compatible con Android e iOS, videoportero, preinstalación de alarma y preinstalación de fibra.',
  'Domotique compatible Android et iOS, visiophone, pré-installation d’alarme et pré-installation de la fibre.',
  'Hausautomation für Android und iOS, Video-Gegensprechanlage, Vorinstallation für Alarmanlage und Glasfaser.',
  'Система «умный дом», работающая с Android и iOS, видеодомофон, подготовка под сигнализацию и под оптоволокно.',
  'نظام منزل ذكي يعمل مع Android وiOS، وجهاز اتصال داخلي بالفيديو، وتمديدات مسبقة لنظام الإنذار ولشبكة الألياف الضوئية.',
  'Domotica die werkt met Android en iOS, een video-intercom, voorbereiding voor een alarm en voorbereiding voor glasvezel.',
  'Automatyka domowa współpracująca z Androidem i iOS, wideodomofon oraz przygotowanie pod alarm i światłowód.',
  'Hjemmeautomasjon som fungerer med Android og iOS, videocalling ved inngangen, forberedelse for alarm og forberedelse for fiber.',
  'Hemautomation som fungerar med Android och iOS, porttelefon med video, förberedelse för larm och förberedelse för fiber.')

a('.qualitySpecs.groups[6].name',
  'Garaje y comunidad',
  'Garage et copropriété',
  'Garage und Gemeinschaft',
  'Гараж и комплекс',
  'المرآب والمجمع',
  'Garage en gemeenschap',
  'Garaż i osiedle',
  'Garasje og fellesskap',
  'Garage och förening')

a('.qualitySpecs.groups[6].items[0]',
  'Dos plazas de garaje y un trastero con cada vivienda, una de cada en algunas viviendas de dos dormitorios, y preinstalación para la carga de coches eléctricos en plazas seleccionadas.',
  'Deux places de garage et un cellier avec chaque logement, une de chaque pour certains logements de deux chambres, et pré-installation pour la recharge de voitures électriques sur certaines places.',
  'Zwei Garagenstellplätze und ein Abstellraum zu jeder Wohnung, bei bestimmten Wohnungen mit zwei Schlafzimmern je einer, und Vorinstallation für das Laden von Elektroautos an ausgewählten Stellplätzen.',
  'Два машиноместа в гараже и кладовая при каждой квартире, по одному для некоторых квартир с двумя спальнями, и подготовка под зарядку электромобилей на отдельных местах.',
  'موقفان في المرآب ومخزن لكل مسكن، وواحد من كل منهما لبعض المساكن بغرفتي نوم، وتمديدات مسبقة لشحن السيارات الكهربائية في مواقف مختارة.',
  'Twee garageplaatsen en een berging bij elke woning, één van elk voor bepaalde woningen met twee slaapkamers, en voorbereiding voor het laden van elektrische auto’s op geselecteerde plaatsen.',
  'Dwa miejsca w garażu i komórka lokatorska przy każdym mieszkaniu, po jednym dla niektórych mieszkań z dwiema sypialniami, oraz przygotowanie do ładowania samochodów elektrycznych na wybranych miejscach.',
  'To garasjeplasser og en bod til hver bolig, én av hver for enkelte boliger med to soverom, og forberedelse for elbillading på utvalgte plasser.',
  'Två garageplatser och ett förråd till varje bostad, en av varje för vissa bostäder med två sovrum, och förberedelse för elbilsladdning på utvalda platser.')

a('.qualitySpecs.groups[6].items[1]',
  'Parcela cerrada con caseta de seguridad en la entrada principal que vigila el perímetro con cámaras, y una oficina de conserjería en el health club.',
  'Une parcelle fermée avec un poste de sécurité à l’entrée principale surveillant le périmètre par caméra, et un bureau de conciergerie au club de santé.',
  'Ein umzäuntes Grundstück mit Sicherheitsposten am Haupteingang, der das Gelände per Kamera überwacht, und einem Concierge-Büro im Health Club.',
  'Огороженная территория с постом охраны у главного въезда, следящим за периметром по камерам, и офис консьержа в оздоровительном клубе.',
  'أرض مسوّرة مع نقطة حراسة عند المدخل الرئيسي تراقب المحيط بالكاميرات، ومكتب للكونسيرج في النادي الصحي.',
  'Een afgesloten terrein met een beveiligingspost bij de hoofdingang die de omtrek met camera’s bewaakt, en een conciërgekantoor bij de health club.',
  'Ogrodzona działka z posterunkiem ochrony przy głównym wjeździe, monitorującym obwód kamerami, oraz biuro concierge w klubie zdrowia.',
  'En inngjerdet tomt med vaktpost ved hovedinngangen som overvåker omkretsen med kamera, og et concierge-kontor ved helseklubben.',
  'En inhägnad tomt med vaktpost vid huvudentrén som bevakar området med kameror, och ett conciergekontor vid hälsoklubben.')

a('.availability.headlineHtml',
  '20 viviendas <em>disponibles</em>',
  '20 logements <em>disponibles</em>',
  '20 Wohnungen <em>verfügbar</em>',
  'Свободно <em>20 квартир</em>',
  '20 مسكنًا <em>متاحًا</em>',
  '20 woningen <em>beschikbaar</em>',
  '20 mieszkań <em>dostępnych</em>',
  '20 boliger <em>ledige</em>',
  '20 bostäder <em>lediga</em>')

a('.availability.copy',
  'Disponibilidad y precios según tres listas de precios de la promotora: la de la fase I del 23 de septiembre de 2026, la del edificio circular del 5 de noviembre de 2026 y la de las fases II y III del 10 de noviembre de 2026. Las viviendas marcadas como reservadas o en espera se omiten. Volvemos a confirmar cada dato antes de la reserva.',
  'Disponibilités et prix issus de trois listes de prix du promoteur : la phase I au 23 septembre 2026, le bâtiment circulaire au 5 novembre 2026 et les phases II et III au 10 novembre 2026. Les logements marqués réservés ou en attente sont exclus. Nous reconfirmons chaque chiffre avant la réservation.',
  'Verfügbarkeit und Preise aus drei Preislisten des Bauträgers: Phase I vom 23. September 2026, das runde Gebäude vom 5. November 2026 und die Phasen II und III vom 10. November 2026. Als reserviert oder zurückgehalten markierte Wohnungen sind nicht aufgeführt. Wir bestätigen jede Angabe vor der Reservierung erneut.',
  'Наличие и цены по трём прайс-листам застройщика: очередь I от 23 сентября 2026 года, круглое здание от 5 ноября 2026 года и очереди II и III от 10 ноября 2026 года. Квартиры с пометкой «забронировано» или «на удержании» не включены. Мы повторно подтверждаем все данные перед бронированием.',
  'التوفر والأسعار من ثلاث قوائم أسعار للمطوّر: المرحلة I بتاريخ 23 سبتمبر 2026، والمبنى الدائري بتاريخ 5 نوفمبر 2026، والمرحلتان II وIII بتاريخ 10 نوفمبر 2026. وقد استُبعدت المساكن المحجوزة أو الموقوفة. ونعيد تأكيد كل رقم قبل الحجز.',
  'Beschikbaarheid en prijzen uit drie prijslijsten van de ontwikkelaar: Fase I van 23 september 2026, het ronde gebouw van 5 november 2026, en Fase II en III van 10 november 2026. Woningen die als gereserveerd of in optie staan, zijn weggelaten. Wij bevestigen elk cijfer opnieuw vóór de reservering.',
  'Dostępność i ceny z trzech cenników dewelopera: etap I z 23 września 2026 r., okrągły budynek z 5 listopada 2026 r. oraz etapy II i III z 10 listopada 2026 r. Mieszkania oznaczone jako zarezerwowane lub wstrzymane zostały pominięte. Każdą liczbę potwierdzamy ponownie przed rezerwacją.',
  'Tilgjengelighet og priser fra tre prislister fra utbyggeren: byggetrinn I av 23. september 2026, den runde bygningen av 5. november 2026, og byggetrinn II og III av 10. november 2026. Boliger som er merket reservert eller holdt av, er utelatt. Vi bekrefter hvert tall på nytt før reservasjon.',
  'Tillgänglighet och priser från tre av exploatörens prislistor: etapp I av den 23 september 2026, den runda byggnaden av den 5 november 2026, och etapp II och III av den 10 november 2026. Bostäder som är markerade som reserverade eller vilande är utelämnade. Vi bekräftar varje uppgift på nytt före bokning.')

a('.availability.priceRange',
  '{E999000} - {E2789500} + {T}',
  '{E999000} - {E2789500} + {T}',
  '{E999000} - {E2789500} + {T}',
  '{E999000} - {E2789500} + {T}',
  '{E999000} - {E2789500} + {T}',
  '{E999000} - {E2789500} + {T}',
  '{E999000} – {E2789500} + {T}',
  '{E999000} - {E2789500} + {T}',
  '{E999000} - {E2789500} + {T}')

a('.availability.sourceNote',
  'Precios, plantas y dormitorios se transcriben de las listas de precios de la promotora del 23 de septiembre de 2026 (fase I), del 5 de noviembre de 2026 (el edificio circular, bloque 7) y del 10 de noviembre de 2026 (fases II y III). Cada una indica que los precios están sujetos a {T}, actualmente del 10 por ciento, y que la lista es informativa y no forma parte de ningún contrato. Los precios mostrados son las cifras netas de la promotora y no incluyen el {T} ni los gastos de compra. V1-311 y V1-312 figuran con el precio de oferta especial de la lista de la fase I, que también recoge las cifras anteriores, {E2590000} y {E2690000}; la lista indica que el mobiliario del salón se incluye con V1-311. La superficie construida, la terraza, el jardín y el solárium son las cifras de las listas de precios; la superficie útil procede del plano de la promotora de cada vivienda. La cifra de jardín de las listas incluye la piscina privada y, cuando la hay, la zona de fuego. Las cifras difieren en cuatro casos, y damos ambas: la lista del edificio circular indica {N260.61} {U} interiores para V1-701 y V1-711, mientras que sus planos de 2026 indican {N238.61} {U} construidos (la misma lista da {N238.61} para el ático reservado de encima), por lo que la tabla no muestra superficie construida para esas dos; V1-711 tiene una terraza de {N129.59} {U} en la lista y de {N129.92} en su plano; V2-402, {N76.61} en la lista y {N75.51} en su plano; V2-403, {N160.63} en la lista y {N150.63} en su plano. Los planos de las fases posteriores llevan en todos los casos el título Fase II, mientras que la lista de precios las divide entre la fase II (bloque 1) y la fase III (bloques 3 a 6); la tabla sigue la lista de precios. No disponemos de un plano individual de V2-101. Nueva Living vuelve a confirmar precio, estado y condiciones antes de cualquier reserva.',
  'Prix, étages et chambres sont repris des listes de prix du promoteur du 23 septembre 2026 (phase I), du 5 novembre 2026 (le bâtiment circulaire, immeuble 7) et du 10 novembre 2026 (phases II et III). Chacune précise que les prix sont soumis à la {T}, actuellement de 10 pour cent, et que la liste est informative et ne fait partie d’aucun contrat. Les prix affichés sont les montants nets du promoteur, hors {T} et frais d’acquisition. V1-311 et V1-312 figurent au prix d’offre spéciale de la liste de la phase I, qui donne aussi les montants précédents, {E2590000} et {E2690000} ; la liste précise que le mobilier du salon est inclus avec V1-311. Surface construite, terrasse, jardin et solarium sont les chiffres des listes de prix ; la surface utile provient du plan du promoteur pour chaque logement. Le chiffre du jardin sur les listes inclut la piscine privée et, le cas échéant, le coin brasero. Les chiffres divergent à quatre endroits, et nous donnons les deux : la liste du bâtiment circulaire indique {N260.61} {U} intérieurs pour V1-701 et V1-711, alors que leurs plans de 2026 indiquent {N238.61} {U} construits (la même liste donne {N238.61} pour l’attique réservé au-dessus), si bien que le tableau n’affiche pas de surface construite pour ces deux logements ; V1-711 a une terrasse de {N129.59} {U} sur la liste et de {N129.92} sur son plan ; V2-402, {N76.61} sur la liste et {N75.51} sur son plan ; V2-403, {N160.63} sur la liste et {N150.63} sur son plan. Les plans des phases suivantes portent tous l’intitulé Phase II, alors que la liste de prix les répartit entre la phase II (immeuble 1) et la phase III (immeubles 3 à 6) ; le tableau suit la liste de prix. Nous ne disposons pas de plan individuel pour V2-101. Nueva Living reconfirme prix, statut et conditions avant toute réservation.',
  'Preise, Etagen und Schlafzimmer sind aus den Preislisten des Bauträgers vom 23. September 2026 (Phase I), vom 5. November 2026 (das runde Gebäude, Block 7) und vom 10. November 2026 (Phasen II und III) übernommen. Jede besagt, dass die Preise der {T} von derzeit 10 Prozent unterliegen und dass die Liste unverbindlich ist und keinen Vertragsbestandteil bildet. Die angezeigten Preise sind die Nettobeträge des Bauträgers ohne {T} und Kaufnebenkosten. V1-311 und V1-312 sind zum Sonderangebotspreis der Liste für Phase I aufgeführt, die auch die früheren Beträge nennt, {E2590000} und {E2690000}; laut Liste sind bei V1-311 die Wohnzimmermöbel inbegriffen. Bebaute Fläche, Terrasse, Garten und Solarium sind die Angaben der Preislisten; die Nutzfläche stammt aus dem Grundriss des Bauträgers für die jeweilige Wohnung. Die Gartenfläche der Listen umfasst den privaten Pool und, wo vorhanden, den Bereich mit Feuerstelle. An vier Stellen weichen die Zahlen voneinander ab, und wir nennen beide: Die Liste für das runde Gebäude gibt für V1-701 und V1-711 {N260.61} {U} Innenfläche an, ihre Grundrisse von 2026 dagegen {N238.61} {U} bebaute Fläche (dieselbe Liste nennt {N238.61} für das reservierte Penthouse darüber), daher zeigt die Tabelle für diese beiden keine bebaute Fläche; V1-711 hat laut Liste eine Terrasse von {N129.59} {U}, laut Grundriss {N129.92}; V2-402 laut Liste {N76.61}, laut Grundriss {N75.51}; V2-403 laut Liste {N160.63}, laut Grundriss {N150.63}. Die Grundrisse der späteren Phasen tragen durchgehend die Überschrift Phase II, während die Preisliste sie auf Phase II (Block 1) und Phase III (Blöcke 3 bis 6) aufteilt; die Tabelle folgt der Preisliste. Für V2-101 liegt uns kein eigener Grundriss vor. Nueva Living bestätigt Preis, Status und Konditionen vor jeder Reservierung erneut.',
  'Цены, этажи и число спален перенесены из прайс-листов застройщика от 23 сентября 2026 года (очередь I), 5 ноября 2026 года (круглое здание, корпус 7) и 10 ноября 2026 года (очереди II и III). В каждом указано, что цены облагаются НДС, сейчас 10%, и что прайс-лист носит информационный характер и не является частью договора. Показанные цены — нетто-суммы застройщика без НДС и расходов на покупку. V1-311 и V1-312 указаны по цене специального предложения из прайс-листа очереди I, где также приведены прежние суммы, {E2590000} и {E2690000}; по прайс-листу мебель для гостиной входит в цену V1-311. Площадь застройки, терраса, сад и солярий — данные прайс-листов; полезная площадь взята из планировки застройщика для каждой квартиры. Площадь сада в прайс-листах включает собственный бассейн и, где она есть, зону с очагом. Данные расходятся в четырёх местах, и мы приводим оба значения: прайс-лист круглого здания даёт {N260.61} {U} внутренней площади для V1-701 и V1-711, тогда как их планировки 2026 года дают {N238.61} {U} площади застройки (тот же прайс-лист даёт {N238.61} для забронированного пентхауса выше), поэтому для этих двух квартир площадь застройки в таблице не указана; у V1-711 терраса {N129.59} {U} по прайс-листу и {N129.92} по планировке; у V2-402 — {N76.61} по прайс-листу и {N75.51} по планировке; у V2-403 — {N160.63} по прайс-листу и {N150.63} по планировке. Планировки последующих очередей везде озаглавлены «Phase II», тогда как прайс-лист делит их на очередь II (корпус 1) и очередь III (корпуса 3–6); таблица следует прайс-листу. Индивидуальной планировки V2-101 у нас нет. Nueva Living повторно подтверждает цену, статус и условия перед любым бронированием.',
  'نُقلت الأسعار والطوابق وعدد غرف النوم من قوائم أسعار المطوّر بتاريخ 23 سبتمبر 2026 (المرحلة I)، و5 نوفمبر 2026 (المبنى الدائري، المبنى 7)، و10 نوفمبر 2026 (المرحلتان II وIII). وتنص كل قائمة على أن الأسعار تخضع لضريبة القيمة المضافة، وهي حالياً 10%، وأن القائمة إعلامية ولا تشكّل جزءاً من أي عقد. والأسعار المعروضة هي الأرقام الصافية للمطوّر ولا تشمل ضريبة القيمة المضافة ولا تكاليف الشراء. ويظهر V1-311 وV1-312 بسعر العرض الخاص الوارد في قائمة المرحلة I، التي تذكر أيضاً الرقمين السابقين، {E2590000} و{E2690000}؛ وتنص القائمة على أن أثاث صالة الجلوس مشمول مع V1-311. والمساحة المبنية والتراس والحديقة والسولاريوم هي أرقام قوائم الأسعار؛ أما المساحة الصافية فمأخوذة من مخطط المطوّر لكل مسكن. ويشمل رقم الحديقة في القوائم المسبح الخاص، ومنطقة موقد النار حيث وُجدت. وتختلف الأرقام في أربعة مواضع، ونذكر الرقمين معاً: تعطي قائمة المبنى الدائري {N260.61} {U} مساحةً داخلية للوحدتين V1-701 وV1-711، بينما تعطي مخططاتهما لعام 2026 مساحة مبنية قدرها {N238.61} {U} (وتعطي القائمة نفسها {N238.61} للبنتهاوس المحجوز فوقهما)، لذا لا يعرض الجدول مساحة مبنية لهاتين الوحدتين؛ وللوحدة V1-711 تراس بمساحة {N129.59} {U} في القائمة و{N129.92} في مخططها؛ وللوحدة V2-402 {N76.61} في القائمة و{N75.51} في مخططها؛ وللوحدة V2-403 {N160.63} في القائمة و{N150.63} في مخططها. وتحمل مخططات المرحلتين اللاحقتين عنوان «Phase II» في جميعها، بينما تقسّمها قائمة الأسعار بين المرحلة II (المبنى 1) والمرحلة III (المباني من 3 إلى 6)؛ ويتبع الجدول قائمة الأسعار. ولا نملك مخططاً فردياً للوحدة V2-101. وتعيد Nueva Living تأكيد السعر والحالة والشروط قبل أي حجز.',
  'Prijzen, verdiepingen en slaapkamers zijn overgenomen uit de prijslijsten van de ontwikkelaar van 23 september 2026 (Fase I), 5 november 2026 (het ronde gebouw, Blok 7) en 10 november 2026 (Fase II en III). Elke lijst vermeldt dat de prijzen exclusief btw zijn, momenteel 10 procent, en dat de lijst informatief is en geen deel uitmaakt van een contract. De getoonde prijzen zijn de nettobedragen van de ontwikkelaar, exclusief btw en aankoopkosten. V1-311 en V1-312 staan vermeld tegen de actieprijs op de lijst van Fase I, die ook de eerdere bedragen noemt, {E2590000} en {E2690000}; volgens de lijst is het loungemeubilair bij V1-311 inbegrepen. Bebouwde oppervlakte, terras, tuin en solarium zijn de cijfers van de prijslijsten; de bruikbare oppervlakte komt van de plattegrond van de ontwikkelaar per woning. Het tuincijfer op de lijsten omvat het privézwembad en, waar aanwezig, de zone met vuurplaats. Op vier punten verschillen de cijfers, en wij geven beide: de lijst van het ronde gebouw noemt {N260.61} {U} binnen voor V1-701 en V1-711, waar hun plattegronden van 2026 {N238.61} {U} bebouwd noemen (dezelfde lijst noemt {N238.61} voor het gereserveerde penthouse erboven), daarom toont de tabel voor die twee geen bebouwde oppervlakte; V1-711 heeft een terras van {N129.59} {U} op de lijst en {N129.92} op de plattegrond; V2-402 heeft {N76.61} op de lijst en {N75.51} op de plattegrond; V2-403 heeft {N160.63} op de lijst en {N150.63} op de plattegrond. De plattegronden van de latere fasen dragen overal de kop Fase II, terwijl de prijslijst ze verdeelt over Fase II (Blok 1) en Fase III (Blok 3 tot en met 6); de tabel volgt de prijslijst. Voor V2-101 hebben wij geen eigen plattegrond. Nueva Living bevestigt prijs, status en voorwaarden opnieuw vóór elke reservering.',
  "Ceny, piętra i liczba sypialni zostały przepisane z cenników dewelopera z 23 września 2026 r. (etap I), 5 listopada 2026 r. (okrągły budynek, budynek 7) i 10 listopada 2026 r. (etapy II i III). Każdy z nich podaje, że ceny podlegają VAT, obecnie 10%, oraz że cennik ma charakter informacyjny i nie stanowi części umowy. Podane ceny to kwoty netto dewelopera, bez VAT i kosztów zakupu. V1-311 i V1-312 są podane w cenie oferty specjalnej z cennika etapu I, który podaje też wcześniejsze kwoty, {E2590000} i {E2690000}; według cennika meble do salonu są wliczone w cenę V1-311. Powierzchnia zabudowy, taras, ogród i solarium to dane z cenników; powierzchnia użytkowa pochodzi z rzutu dewelopera dla każdego mieszkania. Powierzchnia ogrodu w cennikach obejmuje prywatny basen oraz, jeśli jest, strefę z paleniskiem. Dane różnią się w czterech miejscach i podajemy obie wartości: cennik okrągłego budynku podaje {N260.61} {U} powierzchni wewnętrznej dla V1-701 i V1-711, podczas gdy ich rzuty z 2026 r. podają {N238.61} {U} powierzchni zabudowy (ten sam cennik podaje {N238.61} dla zarezerwowanego penthouse'u powyżej), dlatego tabela nie podaje dla tych dwóch powierzchni zabudowy; V1-711 ma taras {N129.59} {U} w cenniku i {N129.92} na rzucie; V2-402 ma {N76.61} w cenniku i {N75.51} na rzucie; V2-403 ma {N160.63} w cenniku i {N150.63} na rzucie. Rzuty kolejnych etapów mają wszędzie nagłówek „Phase II”, podczas gdy cennik dzieli je na etap II (budynek 1) i etap III (budynki 3–6); tabela trzyma się cennika. Nie mamy indywidualnego rzutu V2-101. Nueva Living ponownie potwierdza cenę, status i warunki przed każdą rezerwacją.",
  'Priser, etasjer og soverom er hentet fra utbyggerens prislister av 23. september 2026 (byggetrinn I), 5. november 2026 (den runde bygningen, Hus 7) og 10. november 2026 (byggetrinn II og III). Hver av dem sier at prisene er eksklusive mva., i dag 10 prosent, og at listen er veiledende og ikke inngår i noen kontrakt. Prisene som vises, er utbyggerens nettopriser og er eksklusive mva. og kjøpskostnader. V1-311 og V1-312 vises til tilbudsprisen på listen for byggetrinn I, som også oppgir de tidligere prisene, {E2590000} og {E2690000}; ifølge listen følger loungemøblene med V1-311. Bebygd areal, terrasse, hage og solterrasse er prislistenes tall; boarealet er hentet fra utbyggerens plantegning for hver bolig. Hagetallet på listene omfatter det private bassenget og, der det finnes, området med bålsted. Tallene spriker på fire punkter, og vi oppgir begge: listen for den runde bygningen oppgir {N260.61} {U} innvendig for V1-701 og V1-711, der plantegningene deres fra 2026 oppgir {N238.61} {U} bebygd areal (samme liste oppgir {N238.61} for den reserverte toppleiligheten over), så tabellen viser ikke bebygd areal for disse to; V1-711 har en terrasse på {N129.59} {U} på listen og {N129.92} på plantegningen; V2-402 har {N76.61} på listen og {N75.51} på plantegningen; V2-403 har {N160.63} på listen og {N150.63} på plantegningen. Plantegningene for de senere byggetrinnene har overskriften Byggetrinn II hele veien, mens prislisten deler dem mellom byggetrinn II (Hus 1) og byggetrinn III (Hus 3 til 6); tabellen følger prislisten. Vi har ingen egen plantegning for V2-101. Nueva Living bekrefter pris, status og vilkår på nytt før enhver reservasjon.',
  'Priser, våningar och sovrum är hämtade från exploatörens prislistor av den 23 september 2026 (etapp I), den 5 november 2026 (den runda byggnaden, Hus 7) och den 10 november 2026 (etapp II och III). Var och en anger att priserna är exklusive IVA, för närvarande 10 procent, och att listan är informativ och inte ingår i något avtal. De priser som visas är exploatörens nettopriser och exkluderar IVA och köpkostnader. V1-311 och V1-312 visas till kampanjpriset på listan för etapp I, som också anger de tidigare beloppen, {E2590000} och {E2690000}; enligt listan ingår loungemöblerna i V1-311. Byggyta, terrass, trädgård och solterrass är prislistornas siffror; boytan kommer från exploatörens planritning för varje bostad. Trädgårdssiffran på listorna inkluderar den egna poolen och, där den finns, ytan med eldstad. Siffrorna skiljer sig på fyra punkter, och vi anger båda: listan för den runda byggnaden anger {N260.61} {U} inomhus för V1-701 och V1-711, där deras planritningar från 2026 anger {N238.61} {U} byggyta (samma lista anger {N238.61} för den reserverade takvåningen ovanför), så tabellen visar ingen byggyta för de två; V1-711 har en terrass på {N129.59} {U} på listan och {N129.92} på planritningen; V2-402 har {N76.61} på listan och {N75.51} på planritningen; V2-403 har {N160.63} på listan och {N150.63} på planritningen. Planritningarna för de senare etapperna har rubriken Etapp II rakt igenom, medan prislistan delar upp dem på etapp II (Hus 1) och etapp III (Hus 3 till 6); tabellen följer prislistan. Vi har ingen egen planritning för V2-101. Nueva Living bekräftar pris, status och villkor på nytt före varje bokning.')

a('.constructionTimeline.headlineHtml',
  'En qué punto está <em>cada fase</em>',
  'Où en est <em>chaque phase</em>',
  'Wo jede Phase <em>steht</em>',
  'На какой стадии <em>каждая очередь</em>',
  'أين وصلت <em>كل مرحلة</em>',
  'Hoe ver elke fase <em>is</em>',
  'Na jakim etapie jest <em>każda faza</em>',
  'Hvor hvert byggetrinn <em>står</em>',
  'Hur långt varje etapp <em>har kommit</em>')

a('.constructionTimeline.paymentTermsLabel',
  'Forma de pago, fases posteriores',
  'Modalités de paiement, phases suivantes',
  'Zahlungsbedingungen, spätere Phasen',
  'Условия оплаты, последующие очереди',
  'شروط الدفع، المرحلتان اللاحقتان',
  'Betalingsvoorwaarden, latere fasen',
  'Warunki płatności, kolejne etapy',
  'Betalingsvilkår, senere byggetrinn',
  'Betalningsvillkor, senare etapper')

a('.constructionTimeline.points[0].year',
  'Fase I',
  'Phase I',
  'Phase I',
  'Очередь I',
  'المرحلة I',
  'Fase I',
  'Etap I',
  'Byggetrinn I',
  'Etapp I')

a('.constructionTimeline.points[0].label',
  'Terminada, llave en mano',
  'Achevée, clés en main',
  'Fertiggestellt, schlüsselfertig',
  'Завершена, готова к заселению',
  'مكتملة، جاهزة للتسليم',
  'Voltooid, sleutelklaar',
  'Ukończony, gotowy do odbioru',
  'Ferdig, innflyttingsklart',
  'Färdig, inflyttningsklar')

a('.constructionTimeline.points[1].year',
  'Fase II',
  'Phase II',
  'Phase II',
  'Очередь II',
  'المرحلة II',
  'Fase II',
  'Etap II',
  'Byggetrinn II',
  'Etapp II')

a('.constructionTimeline.points[2].year',
  'Fase III',
  'Phase III',
  'Phase III',
  'Очередь III',
  'المرحلة III',
  'Fase III',
  'Etap III',
  'Byggetrinn III',
  'Etapp III')

a('.constructionTimeline.note',
  'La fase I se construyó con una licencia de obra de Benahavís de 2018; su documento informativo abreviado (DIA) fijaba la entrega el 30 de junio de 2023, y las dos listas de precios de la fase I del otoño de 2026 califican sus viviendas de llave en mano. La primera parte de la fase II cuenta con una licencia de Benahavís de 2024. El DIA de sus primeras 22 viviendas fija la entrega en el cuarto trimestre de 2026, mientras que los vídeos de 2026 de la promotora sobre las últimas viviendas de la fase II hablan del tercer trimestre de 2027; citamos ambas fechas y pedimos la fecha por escrito. Ningún documento da licencia ni fecha para la fase III; los vídeos de obra de la promotora de enero y febrero de 2026 muestran la estructura de un bloque de la fase II a nivel de cubierta y los cimientos de los bloques posteriores.',
  'La phase I a été construite sous un permis de construire de Benahavís de 2018 ; son document d’information abrégé prévoyait la livraison au 30 juin 2023, et les deux listes de prix de la phase I de l’automne 2026 qualifient ses logements de clés en main. La première partie de la phase II dispose d’un permis de Benahavís de 2024. Le document d’information abrégé de ses 22 premiers logements prévoit la livraison au quatrième trimestre 2026, tandis que les films 2026 du promoteur sur les derniers logements de la phase II parlent du troisième trimestre 2027 ; nous citons les deux et demandons la date par écrit. Aucun document ne donne de permis ni de date pour la phase III ; les films de chantier du promoteur de janvier et février 2026 montrent la structure d’un immeuble de la phase II arrivée au niveau du toit et les fondations des immeubles suivants.',
  'Phase I wurde mit einer Baugenehmigung von Benahavís aus dem Jahr 2018 errichtet; ihr Kurzinformationsblatt (DIA) nannte den 30. Juni 2023 als Übergabetermin, und beide Preislisten für Phase I vom Herbst 2026 bezeichnen ihre Wohnungen als schlüsselfertig. Der erste Teil von Phase II hat eine Genehmigung von Benahavís aus dem Jahr 2024. Das DIA für seine ersten 22 Wohnungen nennt das vierte Quartal 2026 für die Übergabe, während die Filme des Bauträgers von 2026 über die letzten Wohnungen der Phase II das dritte Quartal 2027 nennen; wir nennen beide und verlangen den Termin schriftlich. Für Phase III nennt kein Dokument eine Genehmigung oder einen Termin; die Baustellenfilme des Bauträgers von Januar und Februar 2026 zeigen den Rohbau eines Gebäudes der Phase II auf Dachhöhe und die Fundamente der späteren Gebäude.',
  'Очередь I построена по разрешению на строительство, выданному в Бенаависе в 2018 году; её краткий информационный документ (DIA) указывал сдачу 30 июня 2023 года, а оба прайс-листа очереди I осени 2026 года называют её квартиры готовыми к заселению. Первая часть очереди II имеет разрешение Бенаависа 2024 года. Краткий информационный документ (DIA) для её первых 22 квартир указывает сдачу в четвёртом квартале 2026 года, тогда как фильмы застройщика 2026 года о последних квартирах очереди II называют третий квартал 2027 года; мы приводим обе даты и запрашиваем срок письменно. Ни один документ не указывает разрешение или срок для очереди III; строительные фильмы застройщика за январь и февраль 2026 года показывают каркас одного корпуса очереди II на уровне кровли и фундаменты последующих корпусов.',
  'بُنيت المرحلة I بموجب رخصة بناء صادرة في بيناهافيس عام 2018؛ وقد حددت وثيقتها الإعلامية المختصرة (DIA) تاريخ 30 يونيو 2023 للتسليم، وتصف قائمتا أسعار المرحلة I في خريف 2026 مساكنها بأنها جاهزة للتسليم. ويحمل الجزء الأول من المرحلة II رخصة من بيناهافيس صادرة عام 2024. وتحدد الوثيقة الإعلامية المختصرة (DIA) لمساكنه الـ22 الأولى التسليم في الربع الرابع من عام 2026، بينما تذكر أفلام المطوّر لعام 2026 عن آخر مساكن المرحلة II الربع الثالث من عام 2027؛ ونذكر التاريخين ونطلب الموعد كتابياً. ولا تذكر أي وثيقة رخصة أو موعداً للمرحلة III؛ وتُظهر أفلام البناء التي أعدّها المطوّر في يناير وفبراير 2026 هيكل أحد مباني المرحلة II وقد بلغ مستوى السطح، وأساسات المباني اللاحقة.',
  'Fase I is gebouwd onder een bouwvergunning van Benahavís uit 2018; het beknopt informatiedocument (DIA) noemde 30 juni 2023 voor de oplevering, en beide prijslijsten van Fase I uit het najaar van 2026 noemen de woningen sleutelklaar. Het eerste deel van Fase II heeft een vergunning van Benahavís uit 2024. Het beknopt informatiedocument (DIA) voor de eerste 22 woningen noemt het vierde kwartaal van 2026 voor de oplevering, terwijl de films van de ontwikkelaar uit 2026 over de laatste woningen van Fase II het derde kwartaal van 2027 noemen; wij noemen beide en vragen de datum schriftelijk op. Geen enkel document noemt een vergunning of een datum voor Fase III; de bouwfilms van de ontwikkelaar van januari en februari 2026 tonen het casco van één blok van Fase II op dakhoogte en de funderingen van de latere blokken.',
  'Etap I zbudowano na podstawie pozwolenia na budowę wydanego w Benahavís w 2018 r.; jego skrócony dokument informacyjny (DIA) podawał odbiór 30 czerwca 2023 r., a oba cenniki etapu I z jesieni 2026 r. określają jego mieszkania jako gotowe do odbioru. Pierwsza część etapu II ma pozwolenie z Benahavís z 2024 r. Skrócony dokument informacyjny (DIA) dla jej pierwszych 22 mieszkań podaje odbiór w czwartym kwartale 2026 r., natomiast filmy dewelopera z 2026 r. o ostatnich mieszkaniach etapu II mówią o trzecim kwartale 2027 r.; podajemy oba terminy i prosimy o termin na piśmie. Żaden dokument nie podaje pozwolenia ani terminu dla etapu III; filmy z budowy dewelopera ze stycznia i lutego 2026 r. pokazują konstrukcję jednego budynku etapu II na wysokości dachu i fundamenty kolejnych budynków.',
  'Byggetrinn I ble oppført med en byggetillatelse fra Benahavís fra 2018; det kortfattede informasjonsdokumentet (DIA) oppga 30. juni 2023 for overlevering, og begge prislistene for byggetrinn I fra høsten 2026 kaller boligene innflyttingsklare. Den første delen av byggetrinn II har en tillatelse fra Benahavís fra 2024. Det kortfattede informasjonsdokumentet (DIA) for de første 22 boligene oppgir fjerde kvartal 2026 for overlevering, mens utbyggerens filmer fra 2026 om de siste boligene i byggetrinn II oppgir tredje kvartal 2027; vi nevner begge og ber om datoen skriftlig. Ingen dokumenter oppgir en tillatelse eller en dato for byggetrinn III; utbyggerens byggefilmer fra januar og februar 2026 viser råbygget til ett bygg i byggetrinn II i takhøyde og fundamentene til de senere byggene.',
  'Etapp I byggdes med ett bygglov från Benahavís från 2018; det kortfattade informationsdokumentet (DIA) angav den 30 juni 2023 för tillträde, och båda prislistorna för etapp I från hösten 2026 kallar bostäderna inflyttningsklara. Den första delen av etapp II har ett bygglov från Benahavís från 2024. Det kortfattade informationsdokumentet (DIA) för de första 22 bostäderna anger fjärde kvartalet 2026 för tillträde, medan exploatörens filmer från 2026 om de sista bostäderna i etapp II anger tredje kvartalet 2027; vi nämner båda och begär datumet skriftligt. Inget dokument anger något bygglov eller datum för etapp III; exploatörens byggfilmer från januari och februari 2026 visar stommen till ett hus i etapp II i höjd med taket och grunderna till de senare husen.')

a('.constructionTimeline.paymentTerms[0][2]',
  'Señal de reserva',
  'Dépôt de réservation',
  'Reservierungsanzahlung',
  'Задаток за бронирование',
  'عربون الحجز',
  'Reserveringsaanbetaling',
  'Zadatek rezerwacyjny',
  'Reservasjonsdepositum',
  'Bokningsavgift')

a('.constructionTimeline.paymentTerms[2][2]',
  'Contados desde el contrato privado',
  'À compter du contrat privé',
  'Ab dem privaten Kaufvertrag gerechnet',
  'Отсчитывается от частного договора',
  'تُحتسب من تاريخ العقد الخاص',
  'Gerekend vanaf het onderhandse contract',
  'Liczone od umowy prywatnej',
  'Regnet fra den private kontrakten',
  'Räknat från det privata avtalet')

a('.constructionTimeline.paymentTerms[3][0]',
  'Nueve meses después',
  'Neuf mois plus tard',
  'Neun Monate später',
  'Через девять месяцев',
  'بعد تسعة أشهر',
  'Negen maanden later',
  'Dziewięć miesięcy później',
  'Ni måneder senere',
  'Nio månader senare')

a('.constructionTimeline.paymentTerms[4][2]',
  'El resto',
  'Le solde',
  'Der Restbetrag',
  'Остаток',
  'الرصيد المتبقي',
  'Het restant',
  'Pozostała kwota',
  'Restbeløpet',
  'Resterande belopp')

a('.constructionTimeline.paymentTermsNote',
  'Según el calendario de pagos de la promotora titulado Fase 2; confirmamos que se aplica a la vivienda de la fase III que usted elija antes de la reserva. A cada pago se le suma el {T}, actualmente del 10 por ciento. Los dos pagos intermedios vencen en fechas contadas desde el contrato privado, no según el avance de la obra. Los documentos informativos indican que los pagos a cuenta están garantizados según la ley española de edificación; pedimos la garantía de sus propios pagos antes de que se mueva el dinero. Para las viviendas de la fase I, llave en mano, no se publica calendario; las condiciones llegan con el contrato de compraventa.',
  'D’après l’échéancier du promoteur intitulé Phase 2 ; nous vérifions qu’il s’applique au logement de la phase III que vous choisissez avant la réservation. La {T}, actuellement de 10 pour cent, s’ajoute à chaque échéance. Les deux paiements intermédiaires tombent à des dates comptées à partir du contrat privé, et non selon l’avancement des travaux. Les documents d’information indiquent que les acomptes sont garantis selon la loi espagnole sur la construction ; nous demandons la garantie couvrant vos propres paiements avant tout versement. Pour les logements clés en main de la phase I, aucun échéancier n’est publié ; les conditions accompagnent le contrat de vente.',
  'Aus dem Zahlungsplan des Bauträgers mit der Überschrift Phase 2; wir klären vor der Reservierung, ob er für die von Ihnen gewählte Wohnung der Phase III gilt. Auf jede Rate kommt die {T} von derzeit 10 Prozent. Die beiden mittleren Zahlungen werden zu Terminen fällig, die ab dem privaten Kaufvertrag gerechnet werden, nicht nach Baufortschritt. Laut den Kurzinformationsblättern sind Anzahlungen nach spanischem Baurecht abgesichert; wir verlangen die Bürgschaft für Ihre eigenen Zahlungen, bevor Geld fließt. Für die schlüsselfertigen Wohnungen der Phase I ist kein Zahlungsplan veröffentlicht; die Bedingungen ergeben sich aus dem Kaufvertrag.',
  'По графику платежей застройщика с заголовком «Phase 2»; мы подтверждаем, что он применяется к выбранной вами квартире очереди III, до бронирования. К каждому этапу добавляется НДС по действующей ставке 10%. Два промежуточных платежа привязаны к датам, отсчитываемым от частного договора, а не к стадиям работ. Краткие информационные документы (DIA) указывают, что авансовые платежи гарантированы согласно испанскому закону о строительстве; мы запрашиваем гарантию на ваши платежи до того, как будут переведены деньги. Для квартир очереди I, готовых к заселению, график не опубликован; условия определяются договором купли-продажи.',
  'وفق جدول دفعات المطوّر المعنون «Phase 2»؛ ونؤكد قبل الحجز أنه ينطبق على مسكن المرحلة III الذي تختارونه. وتُضاف ضريبة القيمة المضافة بنسبتها الحالية البالغة 10% إلى كل دفعة. وتستحق الدفعتان الوسطيتان في مواعيد تُحتسب من العقد الخاص، لا بحسب مراحل الأعمال. وتنص الوثائق الإعلامية المختصرة (DIA) على أن الدفعات المسبقة مضمونة بموجب قانون البناء الإسباني؛ ونطلب الضمان الخاص بدفعاتكم قبل تحويل أي مبلغ. أما مساكن المرحلة I الجاهزة للتسليم فلا يُنشر لها جدول دفعات، وتُحدَّد الشروط في عقد الشراء.',
  'Uit het betalingsschema van de ontwikkelaar met de kop Fase 2; wij bevestigen vóór de reservering dat het geldt voor de woning in Fase III die u kiest. Over elke termijn komt btw van momenteel 10 procent. De twee middelste betalingen vervallen op data gerekend vanaf het onderhandse contract, niet bij bouwfasen. De beknopte informatiedocumenten (DIA) vermelden dat betalingen vooraf gegarandeerd zijn volgens de Spaanse bouwwet; wij vragen de garantie voor uw eigen betalingen op voordat er geld wordt overgemaakt. Voor de sleutelklare woningen van Fase I is geen schema gepubliceerd; de voorwaarden volgen met de koopovereenkomst.',
  'Na podstawie harmonogramu płatności dewelopera z nagłówkiem „Phase 2”; przed rezerwacją potwierdzamy, że ma on zastosowanie do wybranego przez Państwa mieszkania w etapie III. Do każdej raty doliczany jest VAT według obecnej stawki 10%. Dwie środkowe płatności przypadają w terminach liczonych od umowy prywatnej, a nie od etapów prac. Skrócone dokumenty informacyjne (DIA) podają, że zaliczki są gwarantowane zgodnie z hiszpańskim prawem budowlanym; prosimy o gwarancję dla Państwa płatności, zanim zostaną przekazane jakiekolwiek pieniądze. Dla gotowych do odbioru mieszkań etapu I harmonogram nie jest publikowany; warunki określa umowa kupna.',
  'Fra utbyggerens betalingsplan med overskriften Fase 2; vi bekrefter før reservasjon at den gjelder boligen du velger i byggetrinn III. Mva., i dag 10 prosent, kommer i tillegg på hver termin. De to midterste betalingene forfaller på datoer regnet fra den private kontrakten, ikke etter byggets fremdrift. De kortfattede informasjonsdokumentene (DIA) sier at forskuddsbetalinger er garantert etter spansk byggelov; vi ber om garantien for dine egne betalinger før noen penger overføres. For de innflyttingsklare boligene i byggetrinn I er det ikke publisert noen plan; vilkårene følger kjøpekontrakten.',
  'Ur exploatörens betalningsplan med rubriken Fase 2; vi bekräftar före bokning att den gäller den bostad i etapp III som ni väljer. IVA, för närvarande 10 procent, tillkommer på varje delbetalning. De två mittersta betalningarna förfaller på datum räknade från det privata avtalet, inte efter byggets framsteg. De kortfattade informationsdokumenten (DIA) anger att förskottsbetalningar är garanterade enligt spansk bygglag; vi begär garantin för era egna betalningar innan några pengar förs över. För de inflyttningsklara bostäderna i etapp I finns ingen publicerad plan; villkoren följer med köpeavtalet.')

a('.why.points[0][1]',
  'Veinte apartamentos y áticos disponibles en un conjunto de tres fases sobre Golf Valley, cuatro de ellos terminados y dieciséis en construcción.',
  'Vingt appartements et attiques disponibles dans une résidence en trois phases au-dessus de Golf Valley, dont quatre achevés et seize en construction.',
  'Zwanzig verfügbare Wohnungen und Penthäuser in einer Anlage mit drei Phasen oberhalb von Golf Valley, vier davon fertiggestellt und sechzehn im Bau.',
  'Двадцать свободных апартаментов и пентхаусов в комплексе из трёх очередей над Гольф-долиной, четыре из них готовы и шестнадцать строятся.',
  'عشرون شقة وبنتهاوس متاحة في مجمع من ثلاث مراحل فوق وادي الغولف، أربعة منها مكتملة وستة عشر قيد الإنشاء.',
  'Twintig beschikbare appartementen en penthouses in een project van drie fasen boven Golf Valley, waarvan vier voltooid en zestien in aanbouw.',
  "Dwadzieścia dostępnych apartamentów i penthouse'ów w trzyetapowej inwestycji nad Golf Valley, cztery ukończone i szesnaście w budowie.",
  'Tjue ledige leiligheter og toppleiligheter i et prosjekt i tre byggetrinn over Golf Valley, fire av dem ferdige og seksten under bygging.',
  'Tjugo lediga lägenheter och takvåningar i ett projekt i tre etapper ovanför Golf Valley, fyra av dem färdiga och sexton under uppförande.')

a('.why.points[1][1]',
  'Compradores que quieren entrar ya en una vivienda terminada, y compradores que prefieren comprar sobre plano en una fase posterior con piscina en el jardín o terraza en cubierta.',
  'Les acheteurs qui veulent emménager dès maintenant dans un logement achevé, et ceux qui préfèrent acheter sur plan dans une phase ultérieure, avec une piscine au jardin ou un toit-terrasse.',
  'Käufer, die jetzt in eine fertige Wohnung einziehen möchten, und Käufer, die lieber in einer späteren Phase vom Plan kaufen, mit Gartenpool oder Dachterrasse.',
  'Покупателям, которые хотят въехать в готовую квартиру уже сейчас, и тем, кто предпочитает купить на этапе строительства в последующей очереди квартиру с бассейном в саду или кровельной террасой.',
  'للمشترين الراغبين في الانتقال إلى مسكن مكتمل الآن، وللمشترين الذين يفضّلون الشراء على المخطط في مرحلة لاحقة مع مسبح في الحديقة أو تراس على السطح.',
  'Kopers die nu een afgewerkte woning willen betrekken, en kopers die liever op plan kopen in een latere fase, met een tuinzwembad of een dakterras.',
  'Dla kupujących, którzy chcą wprowadzić się do gotowego mieszkania już teraz, oraz dla tych, którzy wolą kupić z planu w kolejnym etapie mieszkanie z basenem w ogrodzie lub tarasem na dachu.',
  'Kjøpere som vil flytte inn i en ferdig bolig nå, og kjøpere som heller vil kjøpe på tegning i et senere byggetrinn, med hagebasseng eller takterrasse.',
  'Köpare som vill flytta in i en färdig bostad nu, och köpare som hellre köper på ritning i en senare etapp, med trädgårdspool eller takterrass.')

a('.why.points[2][1]',
  'Los servicios de la primera fase están construidos y en uso: un health club con piscina cubierta de 25 metros, una piscina exterior de 25 metros y piscinas redondas en los jardines. Además, un bloque es circular, con una vivienda por planta.',
  'Les équipements de la première phase sont construits et ouverts : un club de santé avec piscine intérieure de 25 mètres, une piscine extérieure de 25 mètres et des piscines rondes dans les jardins. Et un immeuble est circulaire, avec un logement par étage.',
  'Die Einrichtungen der ersten Phase sind gebaut und in Betrieb: ein Health Club mit 25-Meter-Innenpool, ein 25-Meter-Außenpool und runde Pools in den Gärten. Und ein Gebäude ist rund, mit einer Wohnung pro Etage.',
  'Инфраструктура первой очереди построена и работает: оздоровительный клуб с 25-метровым крытым бассейном, 25-метровый открытый бассейн и круглые бассейны в садах. А один из корпусов круглый, с одной квартирой на каждом этаже.',
  'مرافق المرحلة الأولى مبنية وتعمل: نادٍ صحي بمسبح داخلي بطول 25 متراً، ومسبح خارجي بطول 25 متراً، ومسابح دائرية في الحدائق. وأحد المباني دائري، بمسكن واحد في كل طابق.',
  'De voorzieningen van de eerste fase zijn gebouwd en open: een health club met een binnenzwembad van 25 meter, een buitenzwembad van 25 meter en ronde zwembaden in de tuinen. En één blok is rond, met één woning per verdieping.',
  'Udogodnienia pierwszego etapu są zbudowane i działają: klub zdrowia z 25-metrowym basenem krytym, 25-metrowy basen odkryty i okrągłe baseny w ogrodach. Do tego jeden z budynków jest okrągły, z jednym mieszkaniem na każdym piętrze.',
  'Fellesfasilitetene i første byggetrinn er bygget og i bruk: en helseklubb med 25 meter innebasseng, et 25 meter utebasseng og runde bassenger i hagene. Og ett av byggene er rundt, med én bolig i hver etasje.',
  'Den första etappens gemensamma anläggningar är byggda och öppna: en hälsoklubb med en 25 meter lång inomhuspool, en 25 meter lång utomhuspool och runda pooler i trädgårdarna. Och ett av husen är runt, med en bostad på varje våning.')

a('.why.points[3][1]',
  'La ladera mira sobre Golf Valley hacia la costa, con las montañas detrás, y la promotora indica unos ocho minutos en coche hasta Puerto Banús.',
  'Le coteau domine Golf Valley jusqu’à la côte, avec les montagnes derrière, et le promoteur indique environ huit minutes en voiture jusqu’à Puerto Banús.',
  'Der Hang blickt über Golf Valley zur Küste, mit den Bergen im Rücken, und der Bauträger nennt rund acht Autominuten bis Puerto Banús.',
  'Со склона открывается вид на Гольф-долину и побережье, позади горы, а по данным застройщика до Пуэрто-Бануса около восьми минут на машине.',
  'يطل السفح على وادي الغولف حتى الساحل، والجبال خلفه، ويذكر المطوّر أن بويرتو بانوس على بعد نحو ثماني دقائق بالسيارة.',
  'De heuvel kijkt uit over Golf Valley naar de kust, met de bergen erachter, en de ontwikkelaar noemt ongeveer acht minuten met de auto naar Puerto Banús.',
  'Ze zbocza widać Golf Valley aż po wybrzeże, z górami za plecami, a według dewelopera do Puerto Banús jest około ośmiu minut samochodem.',
  'Åssiden har utsikt over Golf Valley mot kysten, med fjellene bak, og utbyggeren oppgir omtrent åtte minutter med bil til Puerto Banús.',
  'Sluttningen har utsikt över Golf Valley mot kusten, med bergen bakom, och exploatören anger omkring åtta minuter med bil till Puerto Banús.')

a('.investment.cards[0][0]',
  'Terminada o sobre plano',
  'Achevé ou sur plan',
  'Fertig oder vom Plan',
  'Готовое или на этапе строительства',
  'مكتمل أو على المخطط',
  'Afgewerkt of op plan',
  'Gotowe czy z planu',
  'Ferdig eller på tegning',
  'Färdig eller på ritning')

a('.investment.cards[0][1]',
  'Las cuatro viviendas de la fase I pueden visitarse y comprarse tal como están. Las dieciséis de las fases posteriores se compran sobre planos y renders, y usted paga la mayor parte del precio antes de recibir las llaves.',
  'Les quatre logements de la phase I peuvent être visités et achetés en l’état. Les seize des phases suivantes s’achètent sur plans et images de synthèse, et vous réglez l’essentiel du prix avant la remise des clés.',
  'Die vier Wohnungen der Phase I können so, wie sie sind, besichtigt und gekauft werden. Die sechzehn in den späteren Phasen werden nach Plänen und Visualisierungen gekauft, und Sie zahlen den Großteil des Preises vor der Schlüsselübergabe.',
  'Четыре квартиры очереди I можно осмотреть и купить в нынешнем виде. Шестнадцать квартир в последующих очередях покупаются по планировкам и визуализациям, и большую часть цены вы платите до получения ключей.',
  'يمكن معاينة مساكن المرحلة I الأربعة وشراؤها كما هي. أما الستة عشر في المرحلتين اللاحقتين فتُشترى بناءً على المخططات والتصورات، وتدفعون معظم الثمن قبل استلام المفاتيح.',
  'De vier woningen van Fase I kunt u bekijken en kopen zoals ze zijn. De zestien in de latere fasen koopt u op basis van plattegronden en renders, en u betaalt het grootste deel van de prijs vóór de sleuteloverdracht.',
  'Cztery mieszkania etapu I można obejrzeć i kupić w obecnym stanie. Szesnaście w kolejnych etapach kupuje się na podstawie rzutów i wizualizacji, a większość ceny płacą Państwo przed odbiorem kluczy.',
  'De fire boligene i byggetrinn I kan du se og kjøpe slik de står. De seksten i de senere byggetrinnene kjøpes ut fra tegninger og illustrasjoner, og du betaler det meste av prisen før du får nøklene.',
  'De fyra bostäderna i etapp I kan ni se och köpa som de står. De sexton i de senare etapperna köps utifrån ritningar och illustrationer, och ni betalar större delen av priset före nyckelöverlämningen.')

a('.investment.cards[1][0]',
  'Dos fechas para la fase II',
  'Deux dates pour la phase II',
  'Zwei Termine für Phase II',
  'Две даты для очереди II',
  'موعدان للمرحلة II',
  'Twee data voor Fase II',
  'Dwa terminy dla etapu II',
  'To datoer for byggetrinn II',
  'Två datum för etapp II')

a('.investment.cards[1][1]',
  'El DIA dice el cuarto trimestre de 2026; los vídeos de 2026 de la promotora, el tercer trimestre de 2027. La fase III no tiene fecha. Incluimos la fecha en el contrato.',
  'Le document d’information abrégé indique le quatrième trimestre 2026, les films 2026 du promoteur le troisième trimestre 2027. La phase III n’a aucune date. Nous faisons inscrire la date dans le contrat.',
  'Das Kurzinformationsblatt nennt das vierte Quartal 2026, die Filme des Bauträgers von 2026 das dritte Quartal 2027. Für Phase III gibt es gar keinen Termin. Wir lassen den Termin in den Vertrag aufnehmen.',
  'Краткий информационный документ (DIA) называет четвёртый квартал 2026 года, фильмы застройщика 2026 года — третий квартал 2027 года. У очереди III даты нет вовсе. Мы вносим срок в договор.',
  'تذكر الوثيقة الإعلامية المختصرة (DIA) الربع الرابع من عام 2026، وأفلام المطوّر لعام 2026 الربع الثالث من عام 2027. ولا موعد إطلاقاً للمرحلة III. ونُدرج الموعد في العقد.',
  'Het beknopt informatiedocument (DIA) noemt het vierde kwartaal van 2026, de films van de ontwikkelaar uit 2026 het derde kwartaal van 2027. Fase III heeft helemaal geen datum. Wij nemen de datum op in het contract.',
  'Skrócony dokument informacyjny (DIA) podaje czwarty kwartał 2026 r., filmy dewelopera z 2026 r. trzeci kwartał 2027 r. Etap III nie ma żadnego terminu. Termin wpisujemy do umowy.',
  'Det kortfattede informasjonsdokumentet (DIA) sier fjerde kvartal 2026, utbyggerens filmer fra 2026 tredje kvartal 2027. Byggetrinn III har ingen dato i det hele tatt. Vi skriver datoen inn i kontrakten.',
  'Det kortfattade informationsdokumentet (DIA) säger fjärde kvartalet 2026, exploatörens filmer från 2026 tredje kvartalet 2027. Etapp III har inget datum alls. Vi skriver in datumet i avtalet.')

a('.investment.cards[2][0]',
  'Impuestos aparte',
  'Taxes en sus',
  'Steuern kommen hinzu',
  'Налог сверху',
  'الضريبة فوق السعر',
  'Belasting komt erbij',
  'Podatek na wierzch',
  'Avgift kommer i tillegg',
  'Skatt tillkommer')

a('.investment.cards[2][1]',
  'Todos los precios son netos: se añade el {T} del 10 por ciento, de modo que el apartamento de {E999000} queda en {E1098900} antes del impuesto de actos jurídicos documentados y de los gastos de notaría y registro.',
  'Tous les prix sont nets : la {T} de 10 pour cent s’ajoute, si bien que l’appartement à {E999000} revient à {E1098900} avant droits d’enregistrement, frais de notaire et de registre.',
  'Jeder Preis ist netto: Die {T} von 10 Prozent kommt hinzu, sodass die Wohnung zu {E999000} auf {E1098900} kommt, vor Stempelsteuer, Notar- und Grundbuchkosten.',
  'Все цены указаны нетто: добавляется НДС 10%, так что квартира за {E999000} обойдётся в {E1098900} до гербового сбора, нотариальных и регистрационных расходов.',
  'كل الأسعار صافية: تُضاف ضريبة القيمة المضافة بنسبة 10%، فتبلغ الشقة التي سعرها {E999000} مبلغ {E1098900} قبل رسم الدمغة وأتعاب الكاتب العدل ورسوم التسجيل.',
  'Elke prijs is netto: er komt 10 procent btw bij, zodat het appartement van {E999000} uitkomt op {E1098900}, vóór overdrachtsbelasting, notaris- en kadasterkosten.',
  'Każda cena jest netto: doliczany jest VAT 10%, więc mieszkanie za {E999000} kosztuje {E1098900} przed podatkiem od czynności, opłatami notarialnymi i rejestrowymi.',
  'Alle priser er netto: 10 prosent mva. kommer i tillegg, så leiligheten til {E999000} koster {E1098900} før dokumentavgift, notar- og tinglysingsgebyrer.',
  'Varje pris är netto: 10 procent IVA tillkommer, så lägenheten för {E999000} kostar {E1098900} före stämpelskatt, notarie- och registreringsavgifter.')

a('.investment.cards[3][1]',
  'Las listas asignan a cada vivienda de una a tres plazas de garaje y un trastero; una plaza adicional cuesta {E50000} y hay pocas.',
  'Les listes attribuent à chaque logement une à trois places de parking et un cellier ; une place supplémentaire coûte {E50000} et elles sont rares.',
  'Laut den Listen gehören zu jeder Wohnung ein bis drei Stellplätze und ein Abstellraum; ein zusätzlicher Stellplatz kostet {E50000} und ist knapp.',
  'По прайс-листам к каждой квартире относится от одного до трёх машиномест и кладовая; дополнительное место стоит {E50000}, и их мало.',
  'تمنح القوائم كل مسكن من موقف إلى ثلاثة مواقف للسيارات ومخزناً؛ ويبلغ سعر الموقف الإضافي {E50000} والمعروض منه قليل.',
  'De lijsten geven elke woning één tot drie parkeerplaatsen en een berging; een extra plaats kost {E50000} en is schaars.',
  'Cenniki przypisują każdemu mieszkaniu od jednego do trzech miejsc postojowych i komórkę lokatorską; dodatkowe miejsce kosztuje {E50000} i jest ich niewiele.',
  'Listene gir hver bolig én til tre parkeringsplasser og en bod; en ekstra plass koster {E50000}, og det er få av dem.',
  'Listorna ger varje bostad en till tre parkeringsplatser och ett förråd; en extra plats kostar {E50000} och de är få.')

a('.trustDossier.cards[0][1]',
  'La licencia de la fase II y la de la fase III, y la licencia de primera ocupación de la primera fase, ya terminada.',
  'Le permis de la phase II et celui de la phase III, ainsi que le permis de première occupation de la première phase achevée.',
  'Die Genehmigung für Phase II und die für Phase III sowie die Erstbezugsgenehmigung der fertiggestellten ersten Phase.',
  'Разрешение на очередь II и разрешение на очередь III, а также разрешение на первое заселение завершённой первой очереди.',
  'رخصة المرحلة II ورخصة المرحلة III، ورخصة الإشغال الأول للمرحلة الأولى المكتملة.',
  'De vergunning van Fase II en die voor Fase III, en de vergunning van eerste bewoning van de voltooide eerste fase.',
  'Pozwolenie dla etapu II i pozwolenie dla etapu III oraz pozwolenie na pierwsze zasiedlenie ukończonego pierwszego etapu.',
  'Tillatelsen for byggetrinn II og den for byggetrinn III, og brukstillatelsen for det ferdige første byggetrinnet.',
  'Bygglovet för etapp II och det för etapp III, samt slutbeskedet för inflyttning i den färdiga första etappen.')

a('.trustDossier.cards[1][1]',
  'La entrega de las fases posteriores, por escrito, dado que los propios documentos de la promotora no coinciden.',
  'La livraison des phases suivantes, par écrit, puisque les propres documents du promoteur se contredisent.',
  'Die Übergabe der späteren Phasen, schriftlich, da sich die eigenen Unterlagen des Bauträgers widersprechen.',
  'Срок сдачи последующих очередей — письменно, поскольку собственные документы застройщика расходятся.',
  'موعد تسليم المرحلتين اللاحقتين كتابياً، إذ إن وثائق المطوّر نفسه متعارضة.',
  'De oplevering van de latere fasen, schriftelijk, nu de eigen documenten van de ontwikkelaar elkaar tegenspreken.',
  'Termin odbioru kolejnych etapów na piśmie, skoro własne dokumenty dewelopera są ze sobą sprzeczne.',
  'Overleveringen av de senere byggetrinnene, skriftlig, siden utbyggerens egne dokumenter er uenige.',
  'Tillträdet i de senare etapperna, skriftligt, eftersom exploatörens egna dokument inte stämmer överens.')

a('.trustDossier.cards[2][1]',
  'Las superficies en las que la lista de precios y el plano no coinciden, y el plano de V2-101, del que aún no disponemos.',
  'Les surfaces pour lesquelles la liste de prix et le plan divergent, et le plan de V2-101, que nous n’avons pas encore.',
  'Die Flächen, bei denen Preisliste und Grundriss voneinander abweichen, und den Grundriss für V2-101, der uns noch nicht vorliegt.',
  'Площади, по которым прайс-лист и планировка расходятся, и планировку V2-101, которой у нас пока нет.',
  'المساحات التي تختلف فيها قائمة الأسعار عن المخطط، ومخطط V2-101 الذي لا نملكه بعد.',
  'De oppervlakten waar prijslijst en plattegrond van elkaar verschillen, en de plattegrond van V2-101, die wij nog niet hebben.',
  'Powierzchnie, co do których cennik i rzut się różnią, oraz rzut V2-101, którego jeszcze nie mamy.',
  'Arealene der prislisten og plantegningen spriker, og plantegningen for V2-101, som vi ennå ikke har.',
  'Ytorna där prislistan och planritningen skiljer sig åt, och planritningen för V2-101, som vi ännu inte har.')

a('.trustDossier.cards[3][0]',
  'Jardines y piscinas',
  'Jardins et piscines',
  'Gärten und Pools',
  'Сады и бассейны',
  'الحدائق والمسابح',
  'Tuinen en zwembaden',
  'Ogrody i baseny',
  'Hager og bassenger',
  'Trädgårdar och pooler')

a('.trustDossier.cards[3][1]',
  'Qué significa el uso privativo del jardín y la piscina comunes en las escrituras y en los estatutos de la comunidad.',
  'Ce que signifie l’usage privatif du jardin et de la piscine communs dans l’acte de vente et dans le règlement de copropriété.',
  'Was die private Nutzung von gemeinschaftlichem Garten und Pool in der Urkunde und in der Gemeinschaftsordnung bedeutet.',
  'Что означает частное пользование общим садом и бассейном в документах о собственности и в правилах сообщества.',
  'ما يعنيه الاستخدام الخاص للحديقة والمسبح المشتركين في سندات الملكية وفي أنظمة المجمع.',
  'Wat het privégebruik van de gemeenschappelijke tuin en het zwembad betekent in de akten en in het reglement van de gemeenschap.',
  'Co oznacza prywatne użytkowanie wspólnego ogrodu i basenu w akcie własności i w regulaminie wspólnoty.',
  'Hva privat bruk av fellesarealets hage og basseng betyr i skjøtet og i sameiets vedtekter.',
  'Vad den privata nyttjanderätten till den gemensamma trädgården och poolen innebär i lagfarten och i föreningens stadgar.')

a('.trustDossier.cards[4][1]',
  'El calendario de pagos de su fase y el aval bancario de las cantidades entregadas a cuenta, antes de la reserva.',
  'L’échéancier de votre phase et la garantie bancaire des acomptes, avant la réservation.',
  'Den Zahlungsplan Ihrer Phase und die Bankbürgschaft für Anzahlungen, vor der Reservierung.',
  'График платежей для вашей очереди и банковскую гарантию на авансовые платежи — до бронирования.',
  'جدول الدفعات الخاص بمرحلتكم والضمان المصرفي للدفعات المسبقة، قبل الحجز.',
  'Het schema voor uw fase en de bankgarantie voor betalingen vooraf, vóór de reservering.',
  'Harmonogram płatności dla Państwa etapu i gwarancję bankową dla zaliczek, przed rezerwacją.',
  'Betalingsplanen for ditt byggetrinn og bankgarantien for forskuddsbetalinger, før reservasjon.',
  'Betalningsplanen för er etapp och bankgarantin för förskottsbetalningar, före bokning.')

a('.architecture.headlineHtml',
  'Terrazas curvas, <em>un bloque circular</em>',
  'Terrasses courbes, <em>un immeuble circulaire</em>',
  'Geschwungene Terrassen, <em>ein runder Block</em>',
  'Изогнутые террасы, <em>круглый корпус</em>',
  'تراسات منحنية، <em>ومبنى دائري</em>',
  'Gebogen terrassen, <em>een rond blok</em>',
  'Zaokrąglone tarasy, <em>okrągły budynek</em>',
  'Buede terrasser, <em>et rundt bygg</em>',
  'Svängda terrasser, <em>ett runt hus</em>')

a('.architecture.copy[0]',
  'La primera fase está construida: bloques blancos con largas terrazas curvas y barandillas de vidrio, escalonados en la pendiente para que los edificios queden más bajos a medida que desciende el terreno, en torno a jardines en terrazas plantados con olivos.',
  'La première phase est construite : des immeubles blancs aux longues terrasses courbes et aux garde-corps en verre, étagés sur la pente pour que les bâtiments s’abaissent à mesure que le terrain descend, autour de jardins en terrasses plantés d’oliviers.',
  'Die erste Phase steht: weiße Gebäude mit langen, geschwungenen Terrassen und Glasbrüstungen, am Hang so gestaffelt, dass sie mit dem abfallenden Gelände niedriger werden, um terrassierte Gärten mit Olivenbäumen.',
  'Первая очередь построена: белые корпуса с длинными изогнутыми террасами и стеклянными ограждениями, уступами спускающиеся по склону, так что здания становятся ниже вслед за рельефом, среди террасных садов с оливковыми деревьями.',
  'المرحلة الأولى مبنية: مبانٍ بيضاء بتراسات منحنية طويلة ودرابزينات زجاجية، متدرجة نزولاً مع المنحدر بحيث تنخفض المباني كلما انحدرت الأرض، وسط حدائق مدرّجة مزروعة بأشجار الزيتون.',
  'De eerste fase is gebouwd: witte blokken met lange, gebogen terrassen en glazen balustrades, trapsgewijs langs de helling zodat de gebouwen lager liggen naarmate het terrein daalt, rond terrastuinen beplant met olijfbomen.',
  'Pierwszy etap jest zbudowany: białe budynki z długimi zaokrąglonymi tarasami i szklanymi balustradami, schodzące kaskadowo po zboczu tak, że obniżają się wraz z terenem, wśród tarasowych ogrodów z drzewami oliwnymi.',
  'Første byggetrinn er bygget: hvite bygg med lange, buede terrasser og glassrekkverk, trappet nedover skråningen slik at byggene ligger lavere der terrenget faller, rundt terrasserte hager beplantet med oliventrær.',
  'Den första etappen är byggd: vita hus med långa, svängda terrasser och glasräcken, i trappsteg nedför slänten så att husen ligger lägre där marken sluttar, runt terrasserade trädgårdar planterade med olivträd.')

a('.architecture.copy[1]',
  'El bloque 7 es circular, con una vivienda en cada una de sus tres plantas en torno a un atrio central redondo que aporta luz, y una terraza en cubierta con piscina para el ático. Las fases posteriores mantienen las terrazas curvas y añaden jardines con piscinas privadas y piscinas en las terrazas en cubierta.',
  'L’immeuble 7 est circulaire, avec un logement à chacun de ses trois niveaux autour d’un atrium central rond qui apporte la lumière, et un toit-terrasse avec piscine pour l’attique. Les phases suivantes conservent les terrasses courbes et ajoutent des jardins avec piscine privée et des piscines sur les toits-terrasses.',
  'Block 7 ist rund, mit einer Wohnung auf jeder seiner drei Etagen um ein rundes zentrales Atrium, das Licht hereinbringt, und einer Dachterrasse mit Pool für das Penthouse. Die späteren Phasen behalten die geschwungenen Terrassen bei und ergänzen Gärten mit privaten Pools sowie Pools auf den Dachterrassen.',
  'Корпус 7 круглый: по одной квартире на каждом из трёх этажей вокруг круглого центрального атриума, который пропускает свет, и кровельная терраса с бассейном у пентхауса. Последующие очереди сохраняют изогнутые террасы и добавляют сады с собственными бассейнами и бассейны на кровельных террасах.',
  'المبنى 7 دائري، بمسكن واحد في كل طابق من طوابقه الثلاثة حول ردهة مركزية مستديرة تُدخل الضوء، وتراس على السطح بمسبح للبنتهاوس. وتحافظ المرحلتان اللاحقتان على التراسات المنحنية وتضيفان حدائق بمسابح خاصة ومسابح على تراسات الأسطح.',
  'Blok 7 is rond, met één woning op elk van de drie verdiepingen rond een rond centraal atrium dat licht binnenbrengt, en een dakterras met zwembad voor het penthouse. De latere fasen houden de gebogen terrassen aan en voegen tuinen met privézwembaden en zwembaden op de dakterrassen toe.',
  "Budynek 7 jest okrągły: po jednym mieszkaniu na każdym z trzech pięter wokół okrągłego centralnego atrium, które wpuszcza światło, oraz taras na dachu z basenem dla penthouse'u. Kolejne etapy zachowują zaokrąglone tarasy i dodają ogrody z prywatnymi basenami oraz baseny na tarasach dachowych.",
  'Hus 7 er rundt, med én bolig i hver av de tre etasjene rundt et rundt atrium i midten som slipper inn lys, og en takterrasse med basseng til toppleiligheten. De senere byggetrinnene beholder de buede terrassene og legger til hager med private bassenger og bassenger på takterrassene.',
  'Hus 7 är runt, med en bostad på var och en av de tre våningarna runt ett runt atrium i mitten som släpper in ljus, och en takterrass med pool till takvåningen. De senare etapperna behåller de svängda terrasserna och lägger till trädgårdar med egna pooler och pooler på takterrasserna.')

a('.architecture.highlights[0][0]',
  'La primera fase',
  'La première phase',
  'Die erste Phase',
  'Первая очередь',
  'المرحلة الأولى',
  'De eerste fase',
  'Pierwszy etap',
  'Første byggetrinn',
  'Första etappen')

a('.architecture.highlights[0][1]',
  'Cuarenta y nueve viviendas en siete bloques, terminadas y en uso.',
  'Quarante-neuf logements en sept immeubles, achevés et habités.',
  'Neunundvierzig Wohnungen in sieben Gebäuden, fertiggestellt und bezogen.',
  'Сорок девять квартир в семи корпусах, построены и работают.',
  'تسعة وأربعون مسكنًا في سبعة مبانٍ، مكتملة ومفتوحة.',
  'Negenenveertig woningen in zeven blokken, voltooid en in gebruik.',
  'Czterdzieści dziewięć mieszkań w siedmiu budynkach, ukończonych i zamieszkanych.',
  'Førtini boliger i sju bygg, ferdige og i bruk.',
  'Fyrtionio bostäder i sju hus, färdiga och i bruk.')

a('.architecture.highlights[1][1]',
  'Tres viviendas, una por planta, en torno a un atrio central de 22 {U}.',
  'Trois logements, un par étage, autour d’un atrium central de 22 {U}.',
  'Drei Wohnungen, eine pro Etage, um ein zentrales Atrium von 22 {U}.',
  'Три квартиры, по одной на этаж, вокруг центрального атриума площадью 22 {U}.',
  'ثلاثة مساكن، واحد في كل طابق، حول ردهة مركزية مساحتها 22 {U}.',
  'Drie woningen, één per verdieping, rond een centraal atrium van 22 {U}.',
  'Trzy mieszkania, po jednym na piętrze, wokół centralnego atrium o powierzchni 22 {U}.',
  'Tre boliger, én per etasje, rundt et atrium i midten på 22 {U}.',
  'Tre bostäder, en per våning, runt ett atrium i mitten på 22 {U}.')

a('.architecture.highlights[2][0]',
  'Las fases posteriores',
  'Les phases suivantes',
  'Die späteren Phasen',
  'Последующие очереди',
  'المرحلتان اللاحقتان',
  'De latere fasen',
  'Kolejne etapy',
  'De senere byggetrinnene',
  'De senare etapperna')

a('.architecture.highlights[2][1]',
  'Cincuenta y ocho viviendas en nuevos bloques, en construcción.',
  'Cinquante-huit logements dans de nouveaux immeubles, en construction.',
  'Achtundfünfzig Wohnungen in weiteren Gebäuden, im Bau.',
  'Пятьдесят восемь квартир в новых корпусах, строятся.',
  'ثمانية وخمسون مسكنًا في مبانٍ إضافية، قيد الإنشاء.',
  'Achtenvijftig woningen in verdere blokken, in aanbouw.',
  'Pięćdziesiąt osiem mieszkań w kolejnych budynkach, w budowie.',
  'Femtiåtte boliger i nye bygg, under bygging.',
  'Femtioåtta bostäder i ytterligare hus, under uppförande.')

a('.architecture.highlights[3][1]',
  'De {N37.99} a {N232.39} {U} en las viviendas disponibles.',
  'De {N37.99} à {N232.39} {U} sur les logements disponibles.',
  'Von {N37.99} bis {N232.39} {U} bei den verfügbaren Wohnungen.',
  'От {N37.99} до {N232.39} {U} у свободных квартир.',
  'من {N37.99} إلى {N232.39} {U} في المساكن المتاحة.',
  'Van {N37.99} tot {N232.39} {U} bij de beschikbare woningen.',
  'Od {N37.99} do {N232.39} {U} w dostępnych mieszkaniach.',
  'Fra {N37.99} til {N232.39} {U} på de ledige boligene.',
  'Från {N37.99} till {N232.39} {U} på de lediga bostäderna.')

a('.architecture.highlights[4][1]',
  'Jardines de uso privativo con piscina en las plantas bajas de las fases posteriores.',
  'Jardins à usage privatif avec piscine aux rez-de-chaussée des phases suivantes.',
  'Gärten zur privaten Nutzung mit Pool in den Erdgeschossen der späteren Phasen.',
  'Сады в частном пользовании с бассейнами у квартир на первом этаже последующих очередей.',
  'حدائق للاستخدام الخاص بمسابح في الطوابق الأرضية للمرحلتين اللاحقتين.',
  'Tuinen voor privégebruik met zwembaden bij de benedenwoningen van de latere fasen.',
  'Ogrody w prywatnym użytkowaniu z basenami na parterach kolejnych etapów.',
  'Hager til privat bruk med bassenger i første etasje i de senere byggetrinnene.',
  'Trädgårdar med privat nyttjanderätt och pooler på bottenvåningarna i de senare etapperna.')

a('.architecture.highlights[5][0]',
  'Terrazas en cubierta',
  'Toits-terrasses',
  'Dachterrassen',
  'Кровельные террасы',
  'تراسات الأسطح',
  'Dakterrassen',
  'Tarasy na dachu',
  'Takterrasser',
  'Takterrasser')

a('.architecture.highlights[5][1]',
  'Soláriums de {N123.50} a {N155.86} {U} en los áticos.',
  'Solariums de {N123.50} à {N155.86} {U} sur les attiques.',
  'Solarien von {N123.50} bis {N155.86} {U} auf den Penthäusern.',
  'Солярии от {N123.50} до {N155.86} {U} у пентхаусов.',
  'سولاريوم من {N123.50} إلى {N155.86} {U} في البنتهاوس.',
  'Solariums van {N123.50} tot {N155.86} {U} bij de penthouses.',
  "Solaria od {N123.50} do {N155.86} {U} w penthouse'ach.",
  'Solterrasser på {N123.50} til {N155.86} {U} på toppleilighetene.',
  'Solterrasser på {N123.50} till {N155.86} {U} på takvåningarna.')

a('.lifestyle.headlineHtml',
  'Construido y <em>por llegar</em>',
  'Construit et <em>à venir</em>',
  'Gebaut und <em>noch geplant</em>',
  'Построено и <em>ещё впереди</em>',
  'ما بُني <em>وما سيأتي</em>',
  'Gebouwd en <em>nog in aantocht</em>',
  'Zbudowane i <em>jeszcze przed nami</em>',
  'Bygget og <em>fortsatt på vei</em>',
  'Byggt och <em>på väg</em>')

a('.lifestyle.copy',
  'Lo que ya tiene la primera fase y lo que la promotora prevé para las fases posteriores, cuyos propietarios comparten ambos.',
  'Ce que la première phase offre déjà et ce que le promoteur prévoit pour les phases suivantes, dont les propriétaires partagent l’ensemble.',
  'Was die erste Phase bereits bietet und was der Bauträger für die späteren Phasen plant, deren Eigentümer beides gemeinsam nutzen.',
  'Что уже есть в первой очереди и что застройщик планирует для последующих, владельцы которых пользуются и тем и другим.',
  'ما تضمّه المرحلة الأولى بالفعل، وما يخطط له المطوّر للمرحلتين اللاحقتين، اللتين يتشارك ملّاكهما الأمرين معاً.',
  'Wat de eerste fase al heeft, en wat de ontwikkelaar plant voor de latere fasen, waarvan de eigenaren beide delen.',
  'Co pierwszy etap już ma i co deweloper planuje dla kolejnych etapów, których właściciele korzystają z obu.',
  'Hva første byggetrinn allerede har, og hva utbyggeren planlegger for de senere byggetrinnene, der eierne deler begge deler.',
  'Vad den första etappen redan har, och vad exploatören planerar för de senare etapperna, vars ägare delar båda.')

a('.lifestyle.panels[0][1]',
  'Construido en la primera fase: una piscina cubierta climatizada de 25 metros, sauna, baño de vapor, jacuzzi, baño de hielo y gimnasio, con un club infantil al lado.',
  'Construit dans la première phase : une piscine intérieure chauffée de 25 mètres, un sauna, un hammam, un jacuzzi, un bain de glace et une salle de sport, avec un club enfants attenant.',
  'In der ersten Phase gebaut: ein beheizter 25-Meter-Innenpool, Sauna, Dampfbad, Whirlpool, Eisbad und Fitnessraum, daneben ein Kinderclub.',
  'Построено в первой очереди: 25-метровый крытый бассейн с подогревом, сауна, паровая баня, джакузи, ледяная купель и тренажёрный зал, рядом детский клуб.',
  'مبني في المرحلة الأولى: مسبح داخلي مدفأ بطول 25 متراً، وساونا، وغرفة بخار، وجاكوزي، وحوض ماء مثلج، وصالة رياضية، وبجانبها نادٍ للأطفال.',
  'Gebouwd in de eerste fase: een verwarmd binnenzwembad van 25 meter, een sauna, een stoombad, een jacuzzi, een ijsbad en een fitnessruimte, met een kinderclub ernaast.',
  'Zbudowane w pierwszym etapie: 25-metrowy podgrzewany basen kryty, sauna, łaźnia parowa, jacuzzi, balia z lodowatą wodą i siłownia, a obok klub dziecięcy.',
  'Bygget i første byggetrinn: et oppvarmet 25 meter innebasseng, badstue, dampbad, boblebad, isbad og treningsrom, med en barneklubb ved siden av.',
  'Byggt i första etappen: en uppvärmd 25 meter lång inomhuspool, bastu, ångbad, bubbelpool, isbad och gym, med en barnklubb intill.')

a('.lifestyle.panels[1][0]',
  'Piscinas y jardines',
  'Piscines et jardins',
  'Pools und Gärten',
  'Бассейны и сады',
  'المسابح والحدائق',
  'Zwembaden en tuinen',
  'Baseny i ogrody',
  'Bassenger og hager',
  'Pooler och trädgårdar')

a('.lifestyle.panels[1][1]',
  'Construido: una piscina exterior de 25 metros para nadar y piscinas redondas para adultos y niños en jardines paisajísticos. Previsto: una piscina de agua salada con jacuzzi exterior.',
  'Construit : une piscine extérieure de nage de 25 mètres et des piscines rondes pour adultes et enfants dans des jardins paysagers. Prévu : une piscine d’eau salée avec jacuzzi extérieur.',
  'Gebaut: ein 25-Meter-Außenpool zum Bahnenschwimmen und runde Pools für Erwachsene und Kinder in angelegten Gärten. Geplant: ein Salzwasserpool mit Außen-Whirlpool.',
  'Построено: 25-метровый открытый бассейн для плавания и круглые бассейны для взрослых и детей в ландшафтных садах. Запланировано: бассейн с морской водой и открытым джакузи.',
  'مبني: مسبح خارجي للسباحة بطول 25 متراً ومسابح دائرية للكبار والأطفال في حدائق منسّقة. مخطط: مسبح بالمياه المالحة مع جاكوزي خارجي.',
  'Gebouwd: een buitenbaan van 25 meter en ronde zwembaden voor volwassenen en kinderen in aangelegde tuinen. Gepland: een zoutwaterzwembad met een buitenjacuzzi.',
  'Zbudowane: 25-metrowy odkryty basen pływacki i okrągłe baseny dla dorosłych i dzieci w urządzonych ogrodach. Planowane: basen ze słoną wodą z jacuzzi na zewnątrz.',
  'Bygget: et 25 meter langt svømmebasseng ute og runde bassenger for voksne og barn i anlagte hager. Planlagt: et saltvannsbasseng med boblebad ute.',
  'Byggt: en 25 meter lång motionspool utomhus och runda pooler för vuxna och barn i anlagda trädgårdar. Planerat: en saltvattenpool med bubbelpool utomhus.')

a('.lifestyle.panels[2][0]',
  'Previsto para las fases posteriores',
  'Prévu pour les phases suivantes',
  'Geplant für die späteren Phasen',
  'Запланировано для последующих очередей',
  'مخطط للمرحلتين اللاحقتين',
  'Gepland voor de latere fasen',
  'Planowane w kolejnych etapach',
  'Planlagt for de senere byggetrinnene',
  'Planerat för de senare etapperna')

a('.lifestyle.panels[2][1]',
  'Un gimnasio exterior, un jardín de yoga y meditación, un parque infantil, una zona de petanca, un mirador y un business centre con sports lounge.',
  'Une salle de sport en plein air, un jardin de yoga et de méditation, une aire de jeux, un terrain de pétanque, un belvédère et un centre d’affaires avec un salon sportif.',
  'Ein Outdoor-Fitnessbereich, ein Yoga- und Meditationsgarten, ein Spielplatz, eine Boule-Bahn, ein Aussichtspunkt und ein Business Center mit Sport-Lounge.',
  'Уличный тренажёрный зал, сад для йоги и медитации, детская площадка, площадка для петанка, смотровая площадка, а также бизнес-центр со спортивным лаунжем.',
  'صالة رياضية خارجية، وحديقة لليوغا والتأمل، وملعب للأطفال، ومساحة للعبة البيتانك، ومنصة مطلّة، ومركز أعمال مع صالة رياضية ترفيهية.',
  'Een buitenfitness, een yoga- en meditatietuin, een speeltuin, een jeu-de-boulesbaan, een uitkijkpunt, en een businesscentrum met een sportlounge.',
  'Siłownia na świeżym powietrzu, ogród do jogi i medytacji, plac zabaw, boisko do pétanque, punkt widokowy oraz centrum biznesowe z salonem sportowym.',
  'Et utendørs treningsområde, en hage for yoga og meditasjon, en lekeplass, en boulebane, et utsiktspunkt, og et forretningssenter med sportslounge.',
  'Ett utomhusgym, en trädgård för yoga och meditation, en lekplats, en boulebana, en utsiktsplats, och ett affärscenter med sportlounge.')

a('.privateViewing.copy',
  'La primera fase está terminada, así que las viviendas, las piscinas y el health club pueden verse tal como son, y las fases posteriores desde la obra.',
  'La première phase est achevée : les logements, les piscines et le club de santé se visitent tels qu’ils sont, et les phases suivantes depuis le chantier.',
  'Die erste Phase ist fertiggestellt, Wohnungen, Pools und Health Club lassen sich also so besichtigen, wie sie sind, und die späteren Phasen von der Baustelle aus.',
  'Первая очередь завершена, поэтому квартиры, бассейны и оздоровительный клуб можно увидеть такими, какие они есть, а последующие очереди — на стройплощадке.',
  'المرحلة الأولى مكتملة، لذا يمكن رؤية المساكن والمسابح والنادي الصحي كما هي، والمرحلتين اللاحقتين من الموقع.',
  'De eerste fase is voltooid, dus de woningen, de zwembaden en de health club kunt u bekijken zoals ze zijn, en de latere fasen vanaf het terrein.',
  'Pierwszy etap jest ukończony, więc mieszkania, baseny i klub zdrowia można zobaczyć w obecnym stanie, a kolejne etapy na placu budowy.',
  'Første byggetrinn er ferdig, så boligene, bassengene og helseklubben kan du se slik de er, og de senere byggetrinnene fra tomten.',
  'Den första etappen är färdig, så bostäderna, poolerna och hälsoklubben kan ni se som de är, och de senare etapperna från området.')

a('.privateViewing.insights[0][0]',
  'Las viviendas llave en mano',
  'Les logements clés en main',
  'Die schlüsselfertigen Wohnungen',
  'Квартиры, готовые к заселению',
  'المساكن الجاهزة للتسليم',
  'De sleutelklare woningen',
  'Mieszkania gotowe do odbioru',
  'De innflyttingsklare boligene',
  'De inflyttningsklara bostäderna')

a('.privateViewing.insights[0][1]',
  'Recorra los áticos y el edificio circular.',
  'Visitez les attiques et le bâtiment circulaire.',
  'Besichtigen Sie die Penthäuser und das runde Gebäude.',
  'Пройдите по пентхаусам и круглому зданию.',
  'تجوّلوا في البنتهاوس والمبنى الدائري.',
  'Loop door de penthouses en het ronde gebouw.',
  "Prosimy obejrzeć penthouse'y i okrągły budynek.",
  'Gå gjennom toppleilighetene og den runde bygningen.',
  'Gå igenom takvåningarna och den runda byggnaden.')

a('.privateViewing.insights[1][1]',
  'Vea el health club, las piscinas y los jardines.',
  'Découvrez le club de santé, les piscines et les jardins.',
  'Sehen Sie sich Health Club, Pools und Gärten an.',
  'Посмотрите оздоровительный клуб, бассейны и сады.',
  'شاهدوا النادي الصحي والمسابح والحدائق.',
  'Bekijk de health club, de zwembaden en de tuinen.',
  'Prosimy zobaczyć klub zdrowia, baseny i ogrody.',
  'Se helseklubben, bassengene og hagene.',
  'Se hälsoklubben, poolerna och trädgårdarna.')

a('.privateViewing.insights[2][1]',
  'Vea las obras y dónde se levantará su bloque.',
  'Voyez le chantier et l’emplacement de votre immeuble.',
  'Sehen Sie die Baustelle und wo Ihr Gebäude stehen wird.',
  'Посмотрите на ход работ и место, где будет стоять ваш корпус.',
  'اطّلعوا على سير الأعمال وعلى موقع مبناكم.',
  'Bekijk de werken en waar uw blok komt te staan.',
  'Prosimy przyjrzeć się pracom i miejscu, w którym stanie Państwa budynek.',
  'Se byggearbeidene og hvor ditt bygg skal stå.',
  'Se bygget och var ert hus kommer att stå.')

a('.location.headlineHtml',
  'Sobre Golf Valley, <em>Benahavís</em>',
  'Au-dessus de Golf Valley, <em>Benahavís</em>',
  'Oberhalb von Golf Valley, <em>Benahavís</em>',
  'Над Гольф-долиной, <em>Бенаавис</em>',
  'فوق وادي الغولف، <em>بيناهافيس</em>',
  'Boven Golf Valley, <em>Benahavís</em>',
  'Nad Golf Valley, <em>Benahavís</em>',
  'Over Golf Valley, <em>Benahavís</em>',
  'Ovanför Golf Valley, <em>Benahavís</em>')

a('.location.copy',
  'Los documentos informativos sitúan el conjunto en el término municipal de Benahavís. La promotora describe la ladera como situada entre Marbella y Benahavís, sobre Golf Valley, con El Madroñal detrás y acceso por la carretera que atraviesa La Quinta o por la carretera de Ronda. Ningún documento da la posición exacta, por lo que el mapa sitúa la parcela de forma aproximada; confirmamos los tiempos de trayecto en una visita.',
  'Les documents d’information situent la résidence sur la commune de Benahavís. Le promoteur décrit le coteau comme situé entre Marbella et Benahavís, au-dessus de Golf Valley, avec El Madroñal en arrière-plan et un accès par la route qui traverse La Quinta ou par la route de Ronda. Aucun document ne donne la position exacte : la carte situe donc le terrain de façon approximative ; nous confirmons les temps de trajet lors d’une visite.',
  'Die Kurzinformationsblätter verorten die Anlage im Gemeindegebiet von Benahavís. Der Bauträger beschreibt den Hang als zwischen Marbella und Benahavís gelegen, oberhalb von Golf Valley, mit El Madroñal im Rücken und Zufahrt über die Straße durch La Quinta oder die Straße nach Ronda. Kein Dokument nennt die genaue Lage, daher zeigt die Karte das Grundstück nur ungefähr; die Fahrzeiten bestätigen wir bei einem Besuch.',
  'Краткие информационные документы (DIA) относят комплекс к муниципалитету Бенаавис. Застройщик описывает склон как расположенный между Марбельей и Бенаависом, над Гольф-долиной, с Эль-Мадроньялем позади, с подъездом по дороге через Ла-Кинту или по дороге на Ронду. Точное положение не указано ни в одном документе, поэтому карта показывает участок приблизительно; время в пути мы уточняем во время визита.',
  'تحدد الوثائق الإعلامية المختصرة (DIA) موقع المجمع في بلدية بيناهافيس. ويصف المطوّر السفح بأنه يقع بين ماربيا وبيناهافيس، فوق وادي الغولف، وخلفه إل مادرونيال، ويُوصَل إليه عبر الطريق المار بلا كوينتا أو طريق روندا. ولا تذكر أي وثيقة الموقع الدقيق، لذا تُظهر الخريطة الموقع على وجه التقريب؛ ونؤكد أوقات القيادة خلال الزيارة.',
  'De beknopte informatiedocumenten (DIA) situeren het project in de gemeente Benahavís. De ontwikkelaar beschrijft de heuvel als gelegen tussen Marbella en Benahavís, boven Golf Valley, met El Madroñal erachter en bereikbaar via de weg door La Quinta of de weg naar Ronda. Geen enkel document geeft de precieze ligging, dus de kaart plaatst het terrein bij benadering; wij bevestigen de rijtijden tijdens een bezoek.',
  'Skrócone dokumenty informacyjne (DIA) lokalizują inwestycję w gminie Benahavís. Deweloper opisuje zbocze jako położone między Marbellą a Benahavís, nad Golf Valley, z El Madroñal za plecami, z dojazdem drogą przez La Quinta lub drogą do Rondy. Żaden dokument nie podaje dokładnego położenia, dlatego mapa pokazuje działkę w przybliżeniu; czasy dojazdu potwierdzamy podczas wizyty.',
  'De kortfattede informasjonsdokumentene (DIA) plasserer prosjektet i Benahavís kommune. Utbyggeren beskriver åssiden som liggende mellom Marbella og Benahavís, over Golf Valley, med El Madroñal bak og atkomst via veien gjennom La Quinta eller veien til Ronda. Ingen dokumenter oppgir den nøyaktige plasseringen, så kartet viser tomten omtrentlig; vi bekrefter kjøretidene ved en visning.',
  'De kortfattade informationsdokumenten (DIA) placerar projektet i Benahavís kommun. Exploatören beskriver sluttningen som belägen mellan Marbella och Benahavís, ovanför Golf Valley, med El Madroñal bakom och tillfart via vägen genom La Quinta eller vägen mot Ronda. Inget dokument anger det exakta läget, så kartan placerar området ungefärligt; vi bekräftar körtiderna vid ett besök.')

a('.location.distances[0][1]',
  'Unos 8 minutos en coche',
  'Environ 8 minutes en voiture',
  'Rund 8 Minuten mit dem Auto',
  'Около 8 минут на машине',
  'نحو 8 دقائق بالسيارة',
  'Ongeveer 8 minuten met de auto',
  'Około 8 minut samochodem',
  'Omtrent 8 minutter med bil',
  'Omkring 8 minuter med bil')

a('.faq[0][1]',
  'De {E999000} a {E2789500} por la vivienda, más el {T} del 10 por ciento y los gastos de compra, según las listas de precios de la promotora del 23 de septiembre, el 5 de noviembre y el 10 de noviembre de 2026.',
  'De {E999000} à {E2789500} pour le logement, plus la {T} de 10 pour cent et les frais d’acquisition, selon les listes de prix du promoteur des 23 septembre, 5 novembre et 10 novembre 2026.',
  'Von {E999000} bis {E2789500} für die Wohnung, zuzüglich {T} von 10 Prozent und Kaufnebenkosten, laut den Preislisten des Bauträgers vom 23. September, 5. November und 10. November 2026.',
  'От {E999000} до {E2789500} за квартиру плюс НДС 10% и расходы на покупку, согласно прайс-листам застройщика от 23 сентября, 5 ноября и 10 ноября 2026 года.',
  'من {E999000} إلى {E2789500} للمسكن، تُضاف إليها ضريبة القيمة المضافة بنسبة 10% وتكاليف الشراء، وفق قوائم أسعار المطوّر بتاريخ 23 سبتمبر و5 نوفمبر و10 نوفمبر 2026.',
  'Van {E999000} tot {E2789500} voor de woning, plus 10 procent btw en aankoopkosten, volgens de prijslijsten van de ontwikkelaar van 23 september, 5 november en 10 november 2026.',
  'Od {E999000} do {E2789500} za mieszkanie, plus VAT 10% i koszty zakupu, według cenników dewelopera z 23 września, 5 listopada i 10 listopada 2026 r.',
  'Fra {E999000} til {E2789500} for boligen, pluss 10 prosent mva. og kjøpskostnader, ifølge utbyggerens prislister av 23. september, 5. november og 10. november 2026.',
  'Från {E999000} till {E2789500} för bostaden, plus 10 procent IVA och köpkostnader, enligt exploatörens prislistor av den 23 september, 5 november och 10 november 2026.')

a('.faq[1][1]',
  'Veinte: cuatro viviendas llave en mano en la primera fase, una en la segunda y quince en la tercera.',
  'Vingt : quatre logements clés en main dans la première phase, un dans la deuxième et quinze dans la troisième.',
  'Zwanzig: vier schlüsselfertige Wohnungen in der ersten Phase, eine in der zweiten und fünfzehn in der dritten.',
  'Двадцать: четыре готовые к заселению квартиры в первой очереди, одна во второй и пятнадцать в третьей.',
  'عشرون: أربعة مساكن جاهزة للتسليم في المرحلة الأولى، وواحد في الثانية، وخمسة عشر في الثالثة.',
  'Twintig: vier sleutelklare woningen in de eerste fase, één in de tweede en vijftien in de derde.',
  'Dwadzieścia: cztery mieszkania gotowe do odbioru w pierwszym etapie, jedno w drugim i piętnaście w trzecim.',
  'Tjue: fire innflyttingsklare boliger i første byggetrinn, én i det andre og femten i det tredje.',
  'Tjugo: fyra inflyttningsklara bostäder i första etappen, en i den andra och femton i den tredje.')

a('.faq[2][0]',
  '¿Puedo mudarme ya?',
  'Puis-je emménager dès maintenant ?',
  'Kann ich sofort einziehen?',
  'Можно ли въехать сейчас?',
  'هل يمكنني الانتقال الآن؟',
  'Kan ik er nu intrekken?',
  'Czy mogę wprowadzić się już teraz?',
  'Kan jeg flytte inn nå?',
  'Kan jag flytta in nu?')

a('.faq[2][1]',
  'A una vivienda de la fase I, sí: las listas de la promotora califican las cuatro de llave en mano. Las fases posteriores están en construcción.',
  'Dans un logement de la phase I, oui : les listes du promoteur les qualifient toutes les quatre de clés en main. Les phases suivantes sont en construction.',
  'In eine Wohnung der Phase I, ja: Die Listen des Bauträgers bezeichnen alle vier als schlüsselfertig. Die späteren Phasen sind im Bau.',
  'В квартиру очереди I — да: в прайс-листах застройщика все четыре названы готовыми к заселению. Последующие очереди строятся.',
  'إلى مسكن في المرحلة I، نعم: تصف قوائم المطوّر المساكن الأربعة كلها بأنها جاهزة للتسليم. أما المرحلتان اللاحقتان فقيد الإنشاء.',
  'In een woning van Fase I, ja: volgens de lijsten van de ontwikkelaar zijn alle vier sleutelklaar. De latere fasen zijn in aanbouw.',
  'Do mieszkania w etapie I tak: cenniki dewelopera określają wszystkie cztery jako gotowe do odbioru. Kolejne etapy są w budowie.',
  'I en bolig i byggetrinn I, ja: utbyggerens lister kaller alle fire innflyttingsklare. De senere byggetrinnene er under bygging.',
  'I en bostad i etapp I, ja: exploatörens listor kallar alla fyra inflyttningsklara. De senare etapperna är under uppförande.')

a('.faq[3][0]',
  '¿Cuándo se entregan las fases posteriores?',
  'Quand les phases suivantes seront-elles livrées ?',
  'Wann werden die späteren Phasen übergeben?',
  'Когда сдаются последующие очереди?',
  'متى تُسلَّم المرحلتان اللاحقتان؟',
  'Wanneer worden de latere fasen opgeleverd?',
  'Kiedy zostaną oddane kolejne etapy?',
  'Når overleveres de senere byggetrinnene?',
  'När är tillträdet i de senare etapperna?')

a('.faq[3][1]',
  'Para la primera parte de la fase II, el DIA indica el cuarto trimestre de 2026 y los vídeos de 2026 de la promotora el tercer trimestre de 2027. Ningún documento da fecha para la fase III. La pedimos por escrito.',
  'Pour la première partie de la phase II, le document d’information abrégé indique le quatrième trimestre 2026 et les films 2026 du promoteur le troisième trimestre 2027. Aucun document ne donne de date pour la phase III. Nous la demandons par écrit.',
  'Für den ersten Teil von Phase II nennt das Kurzinformationsblatt das vierte Quartal 2026 und die Filme des Bauträgers von 2026 das dritte Quartal 2027. Für Phase III nennt kein Dokument einen Termin. Wir verlangen ihn schriftlich.',
  'Для первой части очереди II краткий информационный документ (DIA) указывает четвёртый квартал 2026 года, а фильмы застройщика 2026 года — третий квартал 2027 года. Для очереди III ни один документ дату не указывает. Мы запрашиваем её письменно.',
  'بالنسبة للجزء الأول من المرحلة II، تذكر الوثيقة الإعلامية المختصرة (DIA) الربع الرابع من عام 2026، وأفلام المطوّر لعام 2026 الربع الثالث من عام 2027. ولا تذكر أي وثيقة موعداً للمرحلة III. ونطلبه كتابياً.',
  'Voor het eerste deel van Fase II noemt het beknopt informatiedocument (DIA) het vierde kwartaal van 2026 en noemen de films van de ontwikkelaar uit 2026 het derde kwartaal van 2027. Geen enkel document noemt een datum voor Fase III. Wij vragen die schriftelijk op.',
  'Dla pierwszej części etapu II skrócony dokument informacyjny (DIA) podaje czwarty kwartał 2026 r., a filmy dewelopera z 2026 r. trzeci kwartał 2027 r. Żaden dokument nie podaje terminu dla etapu III. Prosimy o niego na piśmie.',
  'For den første delen av byggetrinn II oppgir det kortfattede informasjonsdokumentet (DIA) fjerde kvartal 2026 og utbyggerens filmer fra 2026 tredje kvartal 2027. Ingen dokumenter oppgir en dato for byggetrinn III. Vi ber om den skriftlig.',
  'För den första delen av etapp II anger det kortfattade informationsdokumentet (DIA) fjärde kvartalet 2026 och exploatörens filmer från 2026 tredje kvartalet 2027. Inget dokument anger något datum för etapp III. Vi begär det skriftligt.')

a('.faq[4][0]',
  '¿Comparto los servicios comunes?',
  'Les équipements sont-ils partagés ?',
  'Teile ich die Gemeinschaftseinrichtungen?',
  'Буду ли я пользоваться общей инфраструктурой?',
  'هل أتشارك المرافق؟',
  'Deel ik de voorzieningen?',
  'Czy będę korzystać z udogodnień?',
  'Deler jeg fellesfasilitetene?',
  'Delar jag de gemensamma anläggningarna?')

a('.faq[4][1]',
  'Sí. El DIA de la fase II y la web de la promotora indican que los propietarios de las fases posteriores comparten el health club, las piscinas y el club infantil de la primera fase, y que las nuevas zonas comunes también se comparten.',
  'Oui. Le document d’information abrégé de la phase II et le site du promoteur indiquent que les propriétaires des phases suivantes partagent le club de santé, les piscines et le club enfants de la première phase, et que les nouvelles parties communes sont elles aussi partagées.',
  'Ja. Das Kurzinformationsblatt für Phase II und die Website des Bauträgers sagen, dass die Eigentümer der späteren Phasen Health Club, Pools und Kinderclub der ersten Phase mitnutzen und dass auch die neuen Gemeinschaftsbereiche geteilt werden.',
  'Да. Краткий информационный документ (DIA) для очереди II и сайт застройщика указывают, что владельцы последующих очередей пользуются оздоровительным клубом, бассейнами и детским клубом первой очереди, а новые общие зоны также будут общими.',
  'نعم. تنص الوثيقة الإعلامية المختصرة (DIA) للمرحلة II وموقع المطوّر على أن ملّاك المرحلتين اللاحقتين يتشاركون النادي الصحي والمسابح ونادي الأطفال في المرحلة الأولى، وأن المساحات المشتركة الجديدة مشتركة كذلك.',
  'Ja. Het beknopt informatiedocument (DIA) voor Fase II en de website van de ontwikkelaar vermelden dat eigenaren in de latere fasen de health club, de zwembaden en de kinderclub van de eerste fase delen, en ook de nieuwe gemeenschappelijke ruimten worden gedeeld.',
  'Tak. Skrócony dokument informacyjny (DIA) dla etapu II i strona dewelopera podają, że właściciele kolejnych etapów korzystają z klubu zdrowia, basenów i klubu dziecięcego pierwszego etapu, a nowe części wspólne również będą wspólne.',
  'Ja. Det kortfattede informasjonsdokumentet (DIA) for byggetrinn II og utbyggerens nettside sier at eierne i de senere byggetrinnene deler helseklubben, bassengene og barneklubben i første byggetrinn, og de nye fellesarealene deles også.',
  'Ja. Det kortfattade informationsdokumentet (DIA) för etapp II och exploatörens webbplats anger att ägarna i de senare etapperna delar den första etappens hälsoklubb, pooler och barnklubb, och de nya gemensamma ytorna delas också.')

a('.faq[5][1]',
  'Las listas de precios asignan a cada vivienda de una a tres plazas de garaje y un trastero. Una plaza adicional cuesta {E50000}, con disponibilidad limitada.',
  'Les listes de prix attribuent à chaque logement une à trois places de parking et un cellier. Une place supplémentaire coûte {E50000}, dans la limite des disponibilités.',
  'Laut den Preislisten gehören zu jeder Wohnung ein bis drei Stellplätze und ein Abstellraum. Ein zusätzlicher Stellplatz kostet {E50000}, nur begrenzt verfügbar.',
  'По прайс-листам к каждой квартире относится от одного до трёх машиномест и кладовая. Дополнительное место стоит {E50000}, их количество ограничено.',
  'تمنح قوائم الأسعار كل مسكن من موقف إلى ثلاثة مواقف للسيارات ومخزناً. ويكلّف الموقف الإضافي {E50000}، والعدد محدود.',
  'De prijslijsten geven elke woning één tot drie parkeerplaatsen en een berging. Een extra plaats kost {E50000}, met beperkte beschikbaarheid.',
  'Cenniki przypisują każdemu mieszkaniu od jednego do trzech miejsc postojowych i komórkę lokatorską. Dodatkowe miejsce kosztuje {E50000}, liczba jest ograniczona.',
  'Prislistene gir hver bolig én til tre parkeringsplasser og en bod. En ekstra plass koster {E50000}, og det er begrenset tilgang.',
  'Prislistorna ger varje bostad en till tre parkeringsplatser och ett förråd. En extra plats kostar {E50000}, med begränsad tillgång.')

a('.faq[6][1]',
  'Para las fases posteriores: {E20000} para reservar, el 30% al firmar el contrato privado menos la señal, el 20% seis meses después, el 10% nueve meses después y el 40% a la entrega, cada pago más {T}.',
  'Pour les phases suivantes : {E20000} à la réservation, 30% au contrat privé moins le dépôt, 20% six mois plus tard, 10% neuf mois plus tard et 40% à la livraison, chaque échéance plus {T}.',
  'Für die späteren Phasen: {E20000} zur Reservierung, 30% beim privaten Kaufvertrag abzüglich der Anzahlung, 20% sechs Monate später, 10% neun Monate später und 40% bei Fertigstellung, jeweils zuzüglich {T}.',
  'Для последующих очередей: {E20000} при бронировании, 30% при подписании частного договора за вычетом задатка, 20% через шесть месяцев, 10% через девять месяцев и 40% при сдаче, к каждому платежу добавляется НДС.',
  'للمرحلتين اللاحقتين: {E20000} للحجز، و30% عند توقيع العقد الخاص مخصوماً منها العربون، و20% بعد ستة أشهر، و10% بعد تسعة أشهر، و40% عند الإنجاز، تُضاف إلى كل منها ضريبة القيمة المضافة.',
  'Voor de latere fasen: {E20000} bij reservering, 30% bij het onderhandse contract minus de aanbetaling, 20% zes maanden later, 10% negen maanden later en 40% bij oplevering, telkens plus btw.',
  'Dla kolejnych etapów: {E20000} przy rezerwacji, 30% przy umowie prywatnej pomniejszone o zadatek, 20% sześć miesięcy później, 10% dziewięć miesięcy później i 40% przy odbiorze, do każdej raty doliczany jest VAT.',
  'For de senere byggetrinnene: {E20000} ved reservasjon, 30% ved den private kontrakten fratrukket depositumet, 20% seks måneder senere, 10% ni måneder senere og 40% ved overtakelse, hver gang pluss mva.',
  'För de senare etapperna: {E20000} vid bokning, 30% vid det privata avtalet minus bokningsavgiften, 20% sex månader senare, 10% nio månader senare och 40% vid tillträde, varje gång plus IVA.')

a('.timeline.items[0][2]',
  'Las listas de precios, los planos de las viviendas que le interesan y la memoria de calidades.',
  'Les listes de prix, les plans des logements qui vous intéressent et le descriptif des prestations.',
  'Die Preislisten, die Grundrisse der Wohnungen, die Sie interessieren, und die Baubeschreibung.',
  'Прайс-листы, планировки интересующих вас квартир и спецификация.',
  'قوائم الأسعار، ومخططات المساكن التي تهمّكم، والمواصفات.',
  'De prijslijsten, de plattegronden van de woningen die u interesseren en de specificatie.',
  'Cenniki, rzuty interesujących Państwa mieszkań i specyfikacja.',
  'Prislistene, plantegningene for boligene du er interessert i, og spesifikasjonen.',
  'Prislistorna, planritningarna för de bostäder som intresserar er och specifikationen.')

a('.timeline.items[1][2]',
  'Organizamos la visita a las viviendas terminadas y a las fases posteriores.',
  'Nous organisons la visite des logements achevés et des phases suivantes.',
  'Wir organisieren die Besichtigung der fertigen Wohnungen und der späteren Phasen.',
  'Мы организуем осмотр готовых квартир и последующих очередей.',
  'ننظّم زيارة المساكن المكتملة والمرحلتين اللاحقتين.',
  'Wij regelen het bezoek aan de afgewerkte woningen en de latere fasen.',
  'Organizujemy wizytę w gotowych mieszkaniach i na kolejnych etapach.',
  'Vi ordner visningen av de ferdige boligene og de senere byggetrinnene.',
  'Vi ordnar besöket i de färdiga bostäderna och de senare etapperna.')

a('.timeline.items[2][2]',
  'Reserva, contrato, fecha de entrega y aval revisados antes de firmar.',
  'Réservation, contrat, date de livraison et garantie vérifiés avant la signature.',
  'Reservierung, Vertrag, Übergabetermin und Bürgschaft geprüft, bevor Sie unterschreiben.',
  'Бронирование, договор, срок сдачи и гарантия проверяются до подписания.',
  'مراجعة الحجز والعقد وموعد التسليم والضمان قبل التوقيع.',
  'Reservering, contract, opleverdatum en garantie beoordeeld voordat u tekent.',
  'Rezerwacja, umowa, termin odbioru i gwarancja sprawdzone przed podpisaniem.',
  'Reservasjon, kontrakt, overleveringsdato og garanti gjennomgått før du signerer.',
  'Bokning, avtal, tillträdesdatum och garanti granskade innan ni skriver under.')

a('.enquiry.message',
  'Me gustaría recibir la información más reciente del proyecto Madroñal Heights Residences.',
  'Je souhaite recevoir les dernières informations sur le projet Madroñal Heights Residences.',
  'Ich möchte die neuesten Projektinformationen zu Madroñal Heights Residences erhalten.',
  'Я хотел(а) бы получить актуальную информацию о проекте Madroñal Heights Residences.',
  'أرغب في الحصول على أحدث المعلومات عن مشروع Madroñal Heights Residences.',
  'Ik ontvang graag de meest recente projectinformatie over Madroñal Heights Residences.',
  'Chciałbym/Chciałabym otrzymać najnowsze informacje o projekcie Madroñal Heights Residences.',
  'Jeg ønsker å motta den nyeste prosjektinformasjonen om Madroñal Heights Residences.',
  'Jag vill gärna få den senaste projektinformationen om Madroñal Heights Residences.')

a('.enquiry.note',
  'Contexto del proyecto: Madroñal Heights Residences.',
  'Contexte du projet : Madroñal Heights Residences.',
  'Projektkontext: Madroñal Heights Residences.',
  'Контекст проекта: Madroñal Heights Residences.',
  'سياق المشروع: Madroñal Heights Residences.',
  'Projectcontext: Madroñal Heights Residences.',
  'Kontekst projektu: Madroñal Heights Residences.',
  'Prosjektkontekst: Madroñal Heights Residences.',
  'Projektsammanhang: Madroñal Heights Residences.')

a('.seo.title',
  'Madroñal Heights Residences - Benahavís',
  'Madroñal Heights Residences - Benahavís',
  'Madroñal Heights Residences - Benahavís',
  'Madroñal Heights Residences - Бенаавис',
  'Madroñal Heights Residences - بيناهافيس',
  'Madroñal Heights Residences - Benahavís',
  'Madroñal Heights Residences - Benahavís',
  'Madroñal Heights Residences - Benahavís',
  'Madroñal Heights Residences - Benahavís')

a('.seo.h1',
  'Madroñal Heights Residences: veinte viviendas, Benahavís',
  'Madroñal Heights Residences : vingt logements, Benahavís',
  'Madroñal Heights Residences: zwanzig Wohnungen, Benahavís',
  'Madroñal Heights Residences: двадцать квартир, Бенаавис',
  'Madroñal Heights Residences: عشرون مسكنًا، بيناهافيس',
  'Madroñal Heights Residences: twintig woningen, Benahavís',
  'Madroñal Heights Residences: dwadzieścia mieszkań, Benahavís',
  'Madroñal Heights Residences: tjue boliger, Benahavís',
  'Madroñal Heights Residences: tjugo bostäder, Benahavís')

a('.seo.h1Context',
  'Veinte viviendas, Benahavís',
  'Vingt logements, Benahavís',
  'Zwanzig Wohnungen, Benahavís',
  'Двадцать квартир, Бенаавис',
  'عشرون مسكنًا، بيناهافيس',
  'Twintig woningen, Benahavís',
  'Dwadzieścia mieszkań, Benahavís',
  'Tjue boliger, Benahavís',
  'Tjugo bostäder, Benahavís')


json.dump(T, open(f'{SP}/tr_m.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'strings to', f'{SP}/tr_m.json')
