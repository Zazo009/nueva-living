# -*- coding: utf-8 -*-
"""Estepona Fairway Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_f.json keyed by the English string, as assemble.py expects. Tokens: {E325000}
money, {N75.06} decimal number, {U} the area unit.
    python3 tools/import/k_estepona_fairway_residences.py <scratch dir>   (writes <dir>/tr_f.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/estepona-fairway-residences/project.json'))


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


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


# render prefix per locale: the description that follows carries its own connector (de, d’, van, av ...)
CGP = {'es': 'Vista generada por ordenador ', 'fr': 'Vue générée par ordinateur ', 'de': 'Computergenerierte Ansicht ',
       'ru': 'Компьютерная визуализация ', 'ar': 'منظر مولَّد بالحاسوب ', 'nl': 'Computergegenereerd beeld ',
       'pl': 'Wygenerowany komputerowo widok ', 'no': 'Datagenerert bilde ', 'sv': 'Datorgenererad vy '}


def cg(path, *tr):
    assert len(tr) == 9, path
    en = get(path)
    assert en.startswith('Computer-generated view of '), en
    put(en, [CGP[l] + t for l, t in zip(LOCS, tr)])


same(get('.name')); same(get('.shortName')); same(get('.titleHtml'))

# ---- description, SEO, hero, card -------------------------------------------------------------

a('.description',
  '8 de las 43 viviendas de la lista de precios del promotor del 3 de noviembre de 2026 están disponibles en Estepona Golf, Estepona: cuatro apartamentos de dos dormitorios y cuatro de tres dormitorios, con terrazas, desde {E325000} hasta {E730000}, más IVA. No se indica fecha de entrega.',
  '8 des 43 logements de la liste de prix du promoteur du 3 novembre 2026 sont disponibles à Estepona Golf, Estepona : quatre appartements de deux chambres et quatre de trois chambres, avec terrasses, de {E325000} à {E730000}, hors TVA. Aucune date de livraison n’est indiquée.',
  '8 der 43 Immobilien auf der Preisliste des Bauträgers vom 3. November 2026 sind in Estepona Golf, Estepona, verfügbar: vier Wohnungen mit zwei und vier mit drei Schlafzimmern, mit Terrassen, von {E325000} bis {E730000}, zuzüglich MwSt. Ein Fertigstellungstermin ist nicht angegeben.',
  '8 из 43 объектов в прайс-листе застройщика от 3 ноября 2026 года доступны в Estepona Golf, Эстепона: четыре квартиры с двумя спальнями и четыре с тремя, с террасами, от {E325000} до {E730000} без НДС. Срок сдачи не указан.',
  '8 من أصل 43 مسكنًا في قائمة أسعار المطوّر بتاريخ 3 نوفمبر 2026 متاحة في Estepona Golf، إستيبونا: أربع شقق بغرفتي نوم وأربع شقق بثلاث غرف نوم، مع تراسات، من {E325000} إلى {E730000}، دون ضريبة القيمة المضافة. لم يُذكر موعد إنجاز.',
  '8 van de 43 woningen op de prijslijst van de ontwikkelaar van 3 november 2026 zijn beschikbaar in Estepona Golf, Estepona: vier appartementen met twee en vier met drie slaapkamers, met terrassen, van {E325000} tot {E730000}, excl. btw. Er wordt geen opleveringsdatum genoemd.',
  '8 z 43 lokali na cenniku dewelopera z 3 listopada 2026 jest dostępnych w Estepona Golf, Estepona: cztery mieszkania z dwiema sypialniami i cztery z trzema, z tarasami, od {E325000} do {E730000} plus VAT. Termin ukończenia nie jest podany.',
  '8 av de 43 boligene på utbyggerens prisliste fra 3. november 2026 er tilgjengelige i Estepona Golf, Estepona: fire leiligheter med to soverom og fire med tre soverom, med terrasser, fra {E325000} til {E730000}, pluss mva. Ingen ferdigstillelsesdato er oppgitt.',
  '8 av de 43 bostäderna på exploatörens prislista från den 3 november 2026 är tillgängliga i Estepona Golf, Estepona: fyra lägenheter med två sovrum och fyra med tre sovrum, med terrasser, från {E325000} till {E730000}, plus IVA. Inget färdigställandedatum anges.')
a('.seoDescription',
  '8 de 43 apartamentos de la lista en Estepona Golf, Estepona: viviendas de dos y tres dormitorios con terrazas, desde {E325000} hasta {E730000}, más IVA.',
  '8 appartements sur 43 listés à Estepona Golf, Estepona : logements de deux et trois chambres avec terrasses, de {E325000} à {E730000}, hors TVA.',
  '8 von 43 aufgeführten Wohnungen in Estepona Golf, Estepona: Immobilien mit zwei und drei Schlafzimmern und Terrassen, von {E325000} bis {E730000}, zuzüglich MwSt.',
  '8 из 43 квартир из списка в Estepona Golf, Эстепона: жильё с двумя и тремя спальнями и террасами, от {E325000} до {E730000} без НДС.',
  '8 من أصل 43 شقة مدرجة في Estepona Golf، إستيبونا: مساكن بغرفتي نوم وثلاث غرف نوم مع تراسات، من {E325000} إلى {E730000}، دون ضريبة القيمة المضافة.',
  '8 van de 43 vermelde appartementen in Estepona Golf, Estepona: woningen met twee en drie slaapkamers en terrassen, van {E325000} tot {E730000}, excl. btw.',
  '8 z 43 wymienionych mieszkań w Estepona Golf, Estepona: lokale z dwiema i trzema sypialniami oraz tarasami, od {E325000} do {E730000} plus VAT.',
  '8 av 43 oppførte leiligheter i Estepona Golf, Estepona: boliger med to og tre soverom og terrasser, fra {E325000} til {E730000}, pluss mva.',
  '8 av 43 listade lägenheter i Estepona Golf, Estepona: bostäder med två och tre sovrum och terrasser, från {E325000} till {E730000}, plus IVA.')
a('.twitterDescription',
  'Apartamentos de dos y tres dormitorios en Estepona Golf, Estepona, desde {E325000} más IVA.',
  'Appartements de deux et trois chambres à Estepona Golf, Estepona, à partir de {E325000} hors TVA.',
  'Wohnungen mit zwei und drei Schlafzimmern in Estepona Golf, Estepona, ab {E325000} zuzüglich MwSt.',
  'Квартиры с двумя и тремя спальнями в Estepona Golf, Эстепона, от {E325000} без НДС.',
  'شقق بغرفتي نوم وثلاث غرف نوم في Estepona Golf، إستيبونا، ابتداءً من {E325000} دون ضريبة القيمة المضافة.',
  'Appartementen met twee en drie slaapkamers in Estepona Golf, Estepona, vanaf {E325000} excl. btw.',
  'Mieszkania z dwiema i trzema sypialniami w Estepona Golf, Estepona, od {E325000} plus VAT.',
  'Leiligheter med to og tre soverom i Estepona Golf, Estepona, fra {E325000} pluss mva.',
  'Lägenheter med två och tre sovrum i Estepona Golf, Estepona, från {E325000} plus IVA.')
a('.hero.eyebrow',
  '8 de 43 viviendas de la lista disponibles', '8 logements sur 43 listés disponibles', '8 von 43 aufgeführten Immobilien verfügbar',
  '8 из 43 объектов списка доступны', '8 من أصل 43 مسكنًا مدرجًا متاحة', '8 van de 43 vermelde woningen beschikbaar',
  '8 z 43 wymienionych lokali dostępnych', '8 av 43 oppførte boliger tilgjengelige', '8 av 43 listade bostäder tillgängliga')
a('.hero.startingPrice',
  'Desde {E325000} + IVA', 'À partir de {E325000} + TVA', 'Ab {E325000} + MwSt.', 'От {E325000} + НДС',
  'ابتداءً من {E325000} + ضريبة القيمة المضافة', 'Vanaf {E325000} + btw', 'Od {E325000} + VAT', 'Fra {E325000} + mva.', 'Från {E325000} + IVA')
a('.card.description',
  '8 de 43 apartamentos de dos y tres dormitorios con terrazas en Estepona Golf, con piscina en la cubierta, gimnasio y club social, desde {E325000} + IVA.',
  '8 appartements de deux et trois chambres avec terrasses sur 43 listés à Estepona Golf, avec piscine sur le toit, salle de sport et club social, à partir de {E325000} + TVA.',
  '8 von 43 aufgeführten Wohnungen mit zwei und drei Schlafzimmern und Terrassen in Estepona Golf, mit Dachpool, Fitnessraum und Social Club, ab {E325000} + MwSt.',
  '8 из 43 квартир с двумя и тремя спальнями и террасами в Estepona Golf, с бассейном на крыше, тренажёрным залом и общественным клубом, от {E325000} + НДС.',
  '8 من أصل 43 شقة مدرجة بغرفتي نوم وثلاث غرف نوم مع تراسات في Estepona Golf، مع مسبح على السطح ونادٍ رياضي ونادٍ اجتماعي، ابتداءً من {E325000} + ضريبة القيمة المضافة.',
  '8 van de 43 vermelde appartementen met twee en drie slaapkamers en terrassen in Estepona Golf, met een dakzwembad, een sportschool en een sociale club, vanaf {E325000} + btw.',
  '8 z 43 wymienionych mieszkań z dwiema i trzema sypialniami oraz tarasami w Estepona Golf, z basenem na dachu, siłownią i klubem towarzyskim, od {E325000} + VAT.',
  '8 av 43 oppførte leiligheter med to og tre soverom og terrasser i Estepona Golf, med takbasseng, treningsrom og sosial klubb, fra {E325000} + mva.',
  '8 av 43 listade lägenheter med två och tre sovrum och terrasser i Estepona Golf, med takpool, gym och social klubb, från {E325000} + IVA.')
a('.card.meta[0][1]',
  '{E325000} + IVA', '{E325000} + TVA', '{E325000} + MwSt.', '{E325000} + НДС', '{E325000} + ضريبة القيمة المضافة',
  '{E325000} + btw', '{E325000} + VAT', '{E325000} + mva.', '{E325000} + IVA')
a('.availability.priceRange',
  '{E325000} - {E730000} + IVA', '{E325000} - {E730000} + TVA', '{E325000} - {E730000} + MwSt.', '{E325000} - {E730000} + НДС',
  '{E325000} - {E730000} + ضريبة القيمة المضافة', '{E325000} - {E730000} + btw', '{E325000} - {E730000} + VAT',
  '{E325000} - {E730000} + mva.', '{E325000} - {E730000} + IVA')

# ---- images and media ---------------------------------------------------------------------------

cg('.images.hero.alt',
   'del edificio visto desde el talud de césped inferior, con terrazas curvas, barandillas de vidrio y un buggy de golf',
   'du bâtiment vu depuis le talus de pelouse en contrebas, avec des terrasses courbes, des garde-corps en verre et une voiturette de golf',
   'des Gebäudes vom Grashang darunter aus gesehen, mit geschwungenen Terrassen, Glasbrüstungen und einem Golfbuggy',
   'здания, увиденного с травяного склона внизу, с изогнутыми террасами, стеклянными ограждениями и гольф-каром',
   'للمبنى من المنحدر العشبي أسفله، مع تراسات منحنية وحواجز زجاجية وعربة غولف',
   'van het gebouw gezien vanaf de grashelling eronder, met gebogen terrassen, glazen balustrades en een golfbuggy',
   'budynku widzianego z trawiastej skarpy poniżej, z zakrzywionymi tarasami, szklanymi balustradami i melexem golfowym',
   'av bygningen sett fra gressskråningen nedenfor, med buede terrasser, glassrekkverk og en golfbil',
   'av byggnaden sedd från gräsluttningen nedanför, med böjda terrasser, glasräcken och en golfbil')
cg('.images.architecture.alt',
   'de dos bloques con terrazas curvas en tonos de piedra clara y madera, con palmeras delante y buggies de golf aparcados al pie',
   'de deux immeubles aux terrasses courbes dans des tons de pierre claire et de bois, avec des palmiers devant et des voiturettes de golf garées au pied',
   'von zwei Blöcken mit geschwungenen Terrassen in hellen Stein- und Holztönen, mit Palmen davor und Golfbuggys, die am Fuß geparkt sind',
   'двух корпусов с изогнутыми террасами в тонах светлого камня и дерева, с пальмами впереди и гольф-карами, припаркованными у основания',
   'لمبنيين بتراسات منحنية بدرجات الحجر الفاتح والخشب، مع نخيل في المقدمة وعربات غولف متوقفة عند الأسفل',
   'van twee blokken met gebogen terrassen in tinten van lichte steen en hout, met palmen ervoor en geparkeerde golfbuggy’s aan de voet',
   'dwóch budynków z zakrzywionymi tarasami w tonacji jasnego kamienia i drewna, z palmami z przodu i melexami golfowymi zaparkowanymi u podstawy',
   'av to blokker med buede terrasser i toner av lys stein og tre, med palmer foran og golfbiler parkert ved foten',
   'av två hus med böjda terrasser i toner av ljus sten och trä, med palmer framför och golfbilar parkerade vid foten')
cg('.images.lifestyle.alt',
   'de una piscina con tumbonas y pantallas vegetales, con el campo de golf y casas blancas al fondo',
   'd’une piscine avec des transats et des écrans de végétation, avec le parcours de golf et des maisons blanches au fond',
   'eines Pools mit Liegen und bepflanzten Sichtschutzelementen, dahinter der Golfplatz und weiße Häuser',
   'бассейна с шезлонгами и зелёными ширмами, с полем для гольфа и белыми домами позади',
   'لمسبح مع كراسٍ للاستلقاء وحواجز نباتية، وخلفه ملعب الغولف ومنازل بيضاء',
   'van een zwembad met ligbedden en beplante schermen, met de golfbaan en witte huizen erachter',
   'basenu z leżakami i osłonami z roślin, z polem golfowym i białymi domami w tle',
   'av et basseng med solsenger og beplantede skjermer, med golfbanen og hvite hus bak',
   'av en pool med solstolar och planterade skärmar, med golfbanan och vita hus bakom')
cg('.images.privateViewing.alt',
   'de una cocina abierta con isla y taburetes y un salón con sofá rinconero',
   'd’une cuisine ouverte avec îlot et tabourets et d’un séjour avec canapé d’angle',
   'einer offenen Küche mit Kochinsel und Hockern und eines Wohnzimmers mit Ecksofa',
   'открытой кухни с островом и барными стульями и гостиной с угловым диваном',
   'لمطبخ مفتوح مع جزيرة ومقاعد مرتفعة وغرفة جلوس مع أريكة زاوية',
   'van een open keuken met eiland en krukken en een woonkamer met hoekbank',
   'otwartej kuchni z wyspą i stołkami oraz salonu z narożną sofą',
   'av et åpent kjøkken med øy og krakker og en stue med hjørnesofa',
   'av ett öppet kök med köksö och barstolar och ett vardagsrum med hörnsoffa')

a('.media.headlineHtml',
  'El conjunto <em>en imágenes</em>', 'L’ensemble <em>en images</em>', 'Die Anlage <em>in Bildern</em>',
  'Комплекс <em>в изображениях</em>', 'المشروع <em>في صور</em>', 'Het complex <em>in beelden</em>',
  'Zespół <em>na obrazach</em>', 'Anlegget <em>i bilder</em>', 'Området <em>i bilder</em>')
a('.media.copy',
  'Vistas generadas por ordenador del edificio, las terrazas, la piscina y los interiores, del dossier del promotor.',
  'Vues générées par ordinateur du bâtiment, des terrasses, de la piscine et des intérieurs, tirées du dossier du promoteur.',
  'Computergenerierte Ansichten des Gebäudes, der Terrassen, des Pools und der Innenräume aus der Dokumentation des Bauträgers.',
  'Компьютерные визуализации здания, террас, бассейна и интерьеров из досье застройщика.',
  'مناظر مولَّدة بالحاسوب للمبنى والتراسات والمسبح والتصاميم الداخلية، من ملف المطوّر.',
  'Computergegenereerde beelden van het gebouw, de terrassen, het zwembad en de interieurs, uit het dossier van de ontwikkelaar.',
  'Wygenerowane komputerowo widoki budynku, tarasów, basenu i wnętrz z dossier dewelopera.',
  'Datagenererte bilder av bygningen, terrassene, bassenget og interiørene, fra utbyggerens dossier.',
  'Datorgenererade vyer av byggnaden, terrasserna, poolen och interiörerna, från exploatörens dossier.')
a('.media.note',
  'Las imágenes son ilustraciones generadas por ordenador, no fotografías del edificio terminado. El dossier dice que se basan en un proyecto inicial y son solo orientativas, y que el mobiliario, la decoración y la vegetación que aparecen no forman parte de la oferta. Los planos de la tabla son los planos comerciales del promotor: los nombres de las estancias están en español y el mobiliario es decorativo.',
  'Les images sont des illustrations générées par ordinateur, et non des photographies du bâtiment achevé. Le dossier précise qu’elles s’appuient sur un projet initial et ne sont qu’indicatives, et que le mobilier, la décoration et la végétation qui y figurent ne font pas partie de l’offre. Les plans du tableau sont les plans commerciaux du promoteur : les noms des pièces y sont en espagnol et le mobilier y est décoratif.',
  'Die Bilder sind computergenerierte Illustrationen und keine Fotos des fertigen Gebäudes. Laut Dokumentation beruhen sie auf einem ersten Projekt und sind nur eine Orientierung; Möbel, Dekoration und Bepflanzung darauf gehören nicht zum Angebot. Die Grundrisse in der Tabelle sind die Verkaufspläne des Bauträgers: Die Raumbezeichnungen sind auf Spanisch, und die Möbel darauf sind dekorativ.',
  'Изображения — компьютерные иллюстрации, а не фотографии готового здания. В досье сказано, что они основаны на первоначальном проекте и носят лишь ориентировочный характер, а мебель, декор и озеленение на них не входят в предложение. Планировки в таблице — коммерческие планы застройщика: названия помещений на них даны по-испански, а мебель декоративная.',
  'الصور رسوم توضيحية مولَّدة بالحاسوب وليست صورًا فوتوغرافية للمبنى المنجز. ويذكر الملف أنها مبنية على مشروع أولي وأنها للاسترشاد فقط، وأن الأثاث والديكور والنباتات الظاهرة فيها ليست جزءًا من العرض. أما المخططات في الجدول فهي المخططات التجارية للمطوّر: أسماء الغرف فيها بالإسبانية والأثاث فيها للزينة.',
  'De beelden zijn computergegenereerde illustraties en geen foto’s van het afgewerkte gebouw. Volgens het dossier zijn ze gebaseerd op een eerste project en slechts een richtlijn, en maken het meubilair, de inrichting en de beplanting erop geen deel uit van het aanbod. De plattegronden in de tabel zijn de commerciële plattegronden van de ontwikkelaar: de namen van de ruimtes erop zijn in het Spaans en het meubilair is decoratief.',
  'Obrazy są wygenerowanymi komputerowo ilustracjami, a nie zdjęciami ukończonego budynku. Według dossier opierają się na wstępnym projekcie i mają charakter wyłącznie poglądowy, a meble, wystrój i roślinność na nich nie wchodzą w zakres oferty. Rzuty w tabeli to plany sprzedażowe dewelopera: nazwy pomieszczeń są po hiszpańsku, a meble mają charakter dekoracyjny.',
  'Bildene er datagenererte illustrasjoner og ikke fotografier av den ferdige bygningen. Dossieret sier at de bygger på et innledende prosjekt og bare er veiledende, og at møblene, innredningen og beplantningen på dem ikke er en del av tilbudet. Plantegningene i tabellen er utbyggerens salgstegninger: romnavnene på dem er på spansk, og møblene er dekorative.',
  'Bilderna är datorgenererade illustrationer och inte fotografier av den färdiga byggnaden. Dossiern uppger att de bygger på ett inledande projekt och bara är vägledande, och att möblerna, inredningen och växtligheten på dem inte ingår i erbjudandet. Planritningarna i tabellen är exploatörens försäljningsritningar: rumsnamnen på dem är på spanska och möblerna är dekorativa.')

a('.media.items[0].caption', 'El edificio desde el talud inferior', 'Le bâtiment vu depuis le talus en contrebas', 'Das Gebäude vom Hang darunter aus',
  'Здание со склона внизу', 'المبنى من المنحدر السفلي', 'Het gebouw vanaf de helling eronder',
  'Budynek widziany ze skarpy poniżej', 'Bygningen fra skråningen nedenfor', 'Byggnaden från luttningen nedanför')
a('.media.items[1].caption', 'Terrazas curvas y palmeras', 'Terrasses courbes et palmiers', 'Geschwungene Terrassen und Palmen',
  'Изогнутые террасы и пальмы', 'تراسات منحنية ونخيل', 'Gebogen terrassen en palmen',
  'Zakrzywione tarasy i palmy', 'Buede terrasser og palmer', 'Böjda terrasser och palmer')
cg('.media.items[2].alt',
   'de un edificio blanco con largas terrazas acristaladas sobre una carretera curva, con un seto y lavanda en primer plano',
   'd’un bâtiment blanc aux longues terrasses vitrées au-dessus d’une route sinueuse, avec une haie et de la lavande au premier plan',
   'eines weißen Gebäudes mit langen verglasten Terrassen über einer geschwungenen Straße, mit einer Hecke und Lavendel im Vordergrund',
   'белого здания с длинными остеклёнными террасами над изогнутой дорогой, с живой изгородью и лавандой на переднем плане',
   'لمبنى أبيض بتراسات زجاجية طويلة فوق طريق منحنٍ، مع سياج نباتي ولافندر في المقدمة',
   'van een wit gebouw met lange beglaasde terrassen boven een kronkelende weg, met een haag en lavendel op de voorgrond',
   'białego budynku z długimi przeszklonymi tarasami nad łukiem drogi, z żywopłotem i lawendą na pierwszym planie',
   'av en hvit bygning med lange glassede terrasser over en buet vei, med hekk og lavendel i forgrunnen',
   'av en vit byggnad med långa inglasade terrasser ovanför en kurvig väg, med en häck och lavendel i förgrunden')
a('.media.items[2].caption', 'El edificio sobre la carretera', 'Le bâtiment au-dessus de la route', 'Das Gebäude über der Straße',
  'Здание над дорогой', 'المبنى فوق الطريق', 'Het gebouw boven de weg',
  'Budynek nad drogą', 'Bygningen over veien', 'Byggnaden ovanför vägen')
cg('.media.items[3].alt',
   'de una fachada curva con una palmera y el borde de una piscina en primer plano',
   'd’une façade courbe avec un palmier et le bord d’une piscine au premier plan',
   'einer geschwungenen Fassade mit einer Palme und dem Beckenrand eines Pools im Vordergrund',
   'изогнутого фасада с пальмой и краем бассейна на переднем плане',
   'لواجهة منحنية مع نخلة وحافة مسبح في المقدمة',
   'van een gebogen gevel met een palmboom en de rand van een zwembad op de voorgrond',
   'zakrzywionej fasady z palmą i krawędzią basenu na pierwszym planie',
   'av en buet fasade med en palme og kanten av et basseng i forgrunnen',
   'av en böjd fasad med en palm och kanten av en pool i förgrunden')
a('.media.items[3].caption', 'Una fachada curva sobre la piscina', 'Une façade courbe au-dessus de la piscine', 'Eine geschwungene Fassade über dem Pool',
  'Изогнутый фасад над бассейном', 'واجهة منحنية فوق المسبح', 'Een gebogen gevel boven het zwembad',
  'Zakrzywiona fasada nad basenem', 'En buet fasade over bassenget', 'En böjd fasad ovanför poolen')
cg('.media.items[4].alt',
   'de una terraza cubierta con sofás, un puf redondo y una alfombra, con el campo y el mar al fondo',
   'd’une terrasse couverte avec des canapés, un pouf rond et un tapis, avec la campagne et la mer au loin',
   'einer überdachten Terrasse mit Sofas, einem runden Pouf und einem Teppich, dahinter Landschaft und Meer',
   'крытой террасы с диванами, круглым пуфом и ковром, с видом на окрестности и море',
   'لتراس مسقوف مع أرائك ومقعد دائري وسجادة، وخلفه الريف والبحر',
   'van een overdekt terras met banken, een ronde poef en een tapijt, met het platteland en de zee erachter',
   'tarasu zadaszonego z sofami, okrągłym pufem i dywanem, z widokiem na okolicę i morze',
   'av en overbygd terrasse med sofaer, en rund puff og et teppe, med landskapet og havet bak',
   'av en övertäckt terrass med soffor, en rund puff och en matta, med landskapet och havet bakom')
a('.media.items[4].caption', 'Una terraza con el mar al fondo', 'Une terrasse avec la mer au loin', 'Eine Terrasse mit Meerblick im Hintergrund',
  'Терраса с видом на море', 'تراس يطل عليه البحر من بعيد', 'Een terras met de zee erachter',
  'Taras z widokiem na morze', 'En terrasse med havet bak', 'En terrass med havet bakom')
cg('.media.items[5].alt',
   'de una terraza con zona de estar y mesa de comedor, con el campo y el mar a lo lejos',
   'd’une terrasse avec un coin salon et une table à manger, avec la campagne et la mer au loin',
   'einer Terrasse mit Loungebereich und Esstisch, in der Ferne Landschaft und Meer',
   'террасы с зоной отдыха и обеденным столом, с видом на окрестности и море вдали',
   'لتراس مع منطقة جلوس وطاولة طعام، وفي البعيد الريف والبحر',
   'van een terras met een loungehoek en een eettafel, met het platteland en de zee in de verte',
   'tarasu ze strefą wypoczynkową i stołem jadalnianym, z widokiem na okolicę i morze w oddali',
   'av en terrasse med loungeområde og spisebord, med landskapet og havet i det fjerne',
   'av en terrass med loungehörna och matbord, med landskapet och havet i fjärran')
a('.media.items[5].caption', 'Una terraza con zona de estar y mesa de comedor', 'Une terrasse avec un coin salon et une table à manger', 'Eine Terrasse mit Loungebereich und Esstisch',
  'Терраса с зоной отдыха и обеденным столом', 'تراس مع منطقة جلوس وطاولة طعام', 'Een terras met een loungehoek en een eettafel',
  'Taras ze strefą wypoczynkową i stołem jadalnianym', 'En terrasse med loungeområde og spisebord', 'En terrass med loungehörna och matbord')
cg('.media.items[6].alt',
   'del borde de una piscina con tumbonas y una mesa auxiliar, con el mar y un cabo a lo lejos',
   'du bord d’une piscine avec des transats et une table d’appoint, avec la mer et un cap au loin',
   'des Beckenrands eines Pools mit Liegen und einem Beistelltisch, in der Ferne Meer und eine Landzunge',
   'края бассейна с шезлонгами и приставным столиком, с морем и мысом вдали',
   'لحافة مسبح مع كراسٍ للاستلقاء وطاولة جانبية، وفي البعيد البحر ورأس بحري',
   'van de rand van een zwembad met ligbedden en een bijzettafel, met de zee en een landtong in de verte',
   'krawędzi basenu z leżakami i stolikiem pomocniczym, z morzem i przylądkiem w oddali',
   'av kanten av et basseng med solsenger og et sidebord, med havet og et nes i det fjerne',
   'av kanten av en pool med solstolar och ett sidobord, med havet och en udde i fjärran')
a('.media.items[6].caption', 'Una terraza con piscina y tumbonas', 'Une terrasse avec piscine et transats', 'Eine Poolterrasse mit Liegen',
  'Терраса у бассейна с шезлонгами', 'تراس مسبح مع كراسٍ للاستلقاء', 'Een zwembadterras met ligbedden',
  'Taras przy basenie z leżakami', 'En bassengterrasse med solsenger', 'En poolterrass med solstolar')
a('.media.items[7].caption', 'Una piscina con el campo de golf al fondo', 'Une piscine avec le parcours de golf au loin', 'Ein Pool mit dem Golfplatz dahinter',
  'Бассейн с полем для гольфа вдали', 'مسبح يطل عليه ملعب الغولف من بعيد', 'Een zwembad met de golfbaan erachter',
  'Basen z polem golfowym w oddali', 'Et basseng med golfbanen bak', 'En pool med golfbanan bakom')
cg('.media.items[8].alt',
   'de un salón comedor con sofá rinconero, mesa de comedor y puertas correderas de vidrio hacia la terraza',
   'd’un séjour-salle à manger avec canapé d’angle, table à manger et portes vitrées coulissantes vers la terrasse',
   'eines Wohn- und Essbereichs mit Ecksofa, Esstisch und gläsernen Schiebetüren zur Terrasse',
   'гостиной-столовой с угловым диваном, обеденным столом и стеклянными раздвижными дверями на террасу',
   'لغرفة جلوس وطعام مع أريكة زاوية وطاولة طعام وأبواب زجاجية منزلقة إلى التراس',
   'van een woon- en eetkamer met hoekbank, eettafel en glazen schuifdeuren naar het terras',
   'salonu z jadalnią, narożną sofą, stołem jadalnianym i przesuwnymi szklanymi drzwiami na taras',
   'av en stue og spisestue med hjørnesofa, spisebord og skyvedører i glass til terrassen',
   'av ett vardagsrum och matrum med hörnsoffa, matbord och skjutdörrar i glas ut mot terrassen')
a('.media.items[8].caption', 'Un salón que se abre a la terraza', 'Un séjour qui s’ouvre sur la terrasse', 'Ein Wohnzimmer, das sich zur Terrasse öffnet',
  'Гостиная с выходом на террасу', 'غرفة جلوس تنفتح على التراس', 'Een woonkamer die uitkomt op het terras',
  'Salon otwarty na taras', 'En stue som åpner seg mot terrassen', 'Ett vardagsrum som öppnar sig mot terrassen')
a('.media.items[9].caption', 'Una cocina abierta y un salón', 'Une cuisine ouverte et un séjour', 'Eine offene Küche und ein Wohnzimmer',
  'Открытая кухня и гостиная', 'مطبخ مفتوح وغرفة جلوس', 'Een open keuken en een woonkamer',
  'Otwarta kuchnia i salon', 'Et åpent kjøkken og en stue', 'Ett öppet kök och ett vardagsrum')
cg('.media.items[10].alt',
   'de un dormitorio doble con una pared de cabecero de paneles, dos lámparas de mesilla y una cama tapizada',
   'd’une chambre double avec un mur de tête de lit en panneaux, deux lampes de chevet et un lit capitonné',
   'eines Doppelschlafzimmers mit einer paneelierten Kopfteilwand, zwei Nachttischlampen und einem gepolsterten Bett',
   'двухместной спальни со стеновыми панелями у изголовья, двумя прикроватными лампами и мягкой кроватью',
   'لغرفة نوم مزدوجة بجدار رأس سرير مكسو بألواح ومصباحين جانبيين وسرير منجَّد',
   'van een tweepersoonsslaapkamer met een gepaneelde hoofdeindwand, twee nachtlampjes en een gestoffeerd bed',
   'sypialni dwuosobowej ze ścianą z panelami przy wezgłowiu, dwiema lampkami nocnymi i tapicerowanym łóżkiem',
   'av et dobbeltsoverom med en panelvegg bak sengen, to nattbordlamper og en polstret seng',
   'av ett dubbelrum med en panelad vägg bakom sängen, två sänglampor och en stoppad säng')
a('.media.items[10].caption', 'Un dormitorio con cabecero de paneles', 'Une chambre avec tête de lit en panneaux', 'Ein Schlafzimmer mit paneelierter Kopfteilwand',
  'Спальня со стеновыми панелями у изголовья', 'غرفة نوم بجدار رأس سرير مكسو بألواح', 'Een slaapkamer met gepaneelde hoofdeindwand',
  'Sypialnia z panelami przy wezgłowiu', 'Et soverom med panelvegg bak sengen', 'Ett sovrum med panelad vägg bakom sängen')
cg('.media.items[11].alt',
   'de un baño con inodoro suspendido, mueble de lavabo de madera y ducha a ras de suelo',
   'd’une salle de bains avec WC suspendu, meuble vasque en bois et douche à l’italienne',
   'eines Badezimmers mit Wand-WC, Waschtischunterschrank aus Holz und bodengleicher Dusche',
   'ванной комнаты с подвесным унитазом, деревянной тумбой под раковину и душем без поддона',
   'لحمّام مع مرحاض معلّق ووحدة مغسلة خشبية ودش بمستوى الأرضية',
   'van een badkamer met een hangend toilet, een houten wastafelmeubel en een inloopdouche',
   'łazienki z podwieszaną toaletą, drewnianą szafką pod umywalkę i prysznicem bez brodzika',
   'av et bad med veggmontert toalett, en vaskeskap i tre og en åpen dusj',
   'av ett badrum med väggmonterad toalett, en tvättställsskåp i trä och en duschplats utan kant')
a('.media.items[11].caption', 'Un baño con mueble de lavabo y ducha', 'Une salle de bains avec meuble vasque et douche', 'Ein Bad mit Waschtischunterschrank und Dusche',
  'Ванная с тумбой под раковину и душем', 'حمّام مع وحدة مغسلة ودش', 'Een badkamer met wastafelmeubel en douche',
  'Łazienka z szafką pod umywalkę i prysznicem', 'Et bad med vaskeskap og dusj', 'Ett badrum med tvättställsskåp och dusch')

# ---- overview, why, architecture ----------------------------------------------------------------

a('.overview.headlineHtml',
  '8 viviendas <em>disponibles</em> en Estepona Golf', '8 logements <em>disponibles</em> à Estepona Golf', '8 <em>verfügbare</em> Immobilien in Estepona Golf',
  '8 <em>доступных</em> объектов в Estepona Golf', '8 مساكن <em>متاحة</em> في Estepona Golf', '8 <em>beschikbare</em> woningen in Estepona Golf',
  '8 <em>dostępnych</em> lokali w Estepona Golf', '8 <em>tilgjengelige</em> boliger i Estepona Golf', '8 <em>tillgängliga</em> bostäder i Estepona Golf')
a('.overview.copy[0]',
  'El dossier del promotor describe viviendas de uno, dos y tres dormitorios dentro del campo de golf de Estepona Golf, con vistas abiertas al green, privacidad y luz natural durante todo el día. Las define como modernas y conectadas con el paisaje.',
  'Le dossier du promoteur décrit des logements d’une, deux et trois chambres situés au sein du parcours de Estepona Golf, avec des vues dégagées sur le green, de l’intimité et la lumière naturelle toute la journée. Il les qualifie de modernes et en lien avec le paysage.',
  'Die Dokumentation des Bauträgers beschreibt Immobilien mit einem, zwei und drei Schlafzimmern innerhalb des Golfplatzes von Estepona Golf, mit offenem Blick auf das Grün, Privatsphäre und natürlichem Licht den ganzen Tag. Sie nennt sie modern und mit der Landschaft verbunden.',
  'В досье застройщика описаны жилые единицы с одной, двумя и тремя спальнями на территории гольф-поля Estepona Golf, с открытым видом на грин, уединённостью и естественным светом в течение всего дня. Там их называют современными и связанными с ландшафтом.',
  'يصف ملف المطوّر مساكن بغرفة وغرفتي وثلاث غرف نوم داخل ملعب الغولف في Estepona Golf، مع إطلالات مفتوحة على المساحة الخضراء وخصوصية وضوء طبيعي طوال النهار. ويصفها بأنها عصرية ومتصلة بالمناظر الطبيعية.',
  'Het dossier van de ontwikkelaar beschrijft woningen met een, twee en drie slaapkamers binnen de golfbaan van Estepona Golf, met open uitzicht over de green, privacy en natuurlijk licht gedurende de hele dag. Het noemt ze modern en verbonden met het landschap.',
  'Dossier dewelopera opisuje lokale z jedną, dwiema i trzema sypialniami położone na terenie pola golfowego Estepona Golf, z otwartym widokiem na green, prywatnością i naturalnym światłem przez cały dzień. Określa je jako nowoczesne i związane z krajobrazem.',
  'Utbyggerens dossier beskriver boliger med ett, to og tre soverom innenfor golfbanen i Estepona Golf, med åpen utsikt over greenen, privatliv og naturlig lys hele dagen. Det kaller dem moderne og knyttet til landskapet.',
  'Exploatörens dossier beskriver bostäder med ett, två och tre sovrum inom golfbanan i Estepona Golf, med öppen utsikt över greenen, avskildhet och naturligt ljus hela dagen. Den kallar dem moderna och förbundna med landskapet.')
a('.overview.copy[1]',
  'La lista de precios del 3 de noviembre de 2026 nombra 43 viviendas en dos bloques. Muestra 8 con precio y marca las otras 35 como reservadas. Las viviendas con precio tienen dos o tres dormitorios y cada una incluye una plaza de aparcamiento y un trastero. Ningún documento que tengamos da una fecha de entrega, una fecha de licencia o el estado de las obras.',
  'La liste de prix du 3 novembre 2026 nomme 43 logements répartis en deux immeubles. Elle en montre 8 avec un prix et marque les 35 autres comme réservés. Les logements avec un prix ont deux ou trois chambres et chacun comprend une place de parking et un débarras. Aucun document en notre possession ne donne de date de livraison, de date de licence ni l’état d’avancement des travaux.',
  'Die Preisliste vom 3. November 2026 nennt 43 Immobilien in zwei Blöcken. Sie zeigt 8 mit Preis und kennzeichnet die übrigen 35 als reserviert. Die Immobilien mit Preis haben zwei oder drei Schlafzimmer, und zu jeder gehören ein Stellplatz und ein Abstellraum. Kein Dokument, das uns vorliegt, nennt einen Fertigstellungstermin, ein Datum der Baugenehmigung oder den Baustand.',
  'В прайс-листе от 3 ноября 2026 года названы 43 объекта в двух корпусах. У 8 указана цена, остальные 35 отмечены как зарезервированные. У объектов с ценой две или три спальни, и к каждому прилагаются одно машиноместо и одна кладовая. Ни один из имеющихся у нас документов не называет срок сдачи, дату получения лицензии или стадию строительства.',
  'تذكر قائمة الأسعار بتاريخ 3 نوفمبر 2026 ما مجموعه 43 مسكنًا في مبنيين. وتُظهر 8 منها بسعر وتضع على الـ35 الأخرى علامة «محجوزة». والمساكن ذات السعر بغرفتي نوم أو ثلاث غرف نوم، ويتضمن كل منها موقف سيارة واحدًا ومخزنًا واحدًا. ولا يذكر أي مستند لدينا موعد إنجاز أو تاريخ ترخيص أو مرحلة الأعمال.',
  'De prijslijst van 3 november 2026 noemt 43 woningen in twee blokken. Ze toont er 8 met een prijs en markeert de andere 35 als gereserveerd. De woningen met een prijs hebben twee of drie slaapkamers en bij elk hoort één parkeerplaats en één berging. Geen enkel document dat wij hebben geeft een opleveringsdatum, een vergunningsdatum of de bouwfase.',
  'Cennik z 3 listopada 2026 wymienia 43 lokale w dwóch budynkach. Przy 8 podaje cenę, a pozostałe 35 oznacza jako zarezerwowane. Lokale z ceną mają dwie lub trzy sypialnie, a do każdego należą jedno miejsce postojowe i jedna komórka lokatorska. Żaden dokument, którym dysponujemy, nie podaje terminu ukończenia, daty pozwolenia ani etapu robót.',
  'Prislisten fra 3. november 2026 nevner 43 boliger i to blokker. Den viser 8 med pris og markerer de øvrige 35 som reservert. Boligene med pris har to eller tre soverom, og hver av dem hører med én parkeringsplass og ett bod. Ingen dokumenter vi har oppgir en ferdigstillelsesdato, en dato for byggetillatelse eller byggetrinnet.',
  'Prislistan från den 3 november 2026 nämner 43 bostäder i två hus. Den visar 8 med pris och markerar de övriga 35 som reserverade. Bostäderna med pris har två eller tre sovrum, och till varje hör en parkeringsplats och ett förråd. Inget dokument vi har anger ett färdigställandedatum, ett licensdatum eller byggstadiet.')
a('.why.copy',
  'Apartamentos de dos y tres dormitorios con grandes terrazas en Estepona Golf, con piscina, gimnasio y club social, y el 60% del precio solo se paga en la escritura.',
  'Appartements de deux et trois chambres avec de grandes terrasses à Estepona Golf, avec piscine, salle de sport et club social, et 60 % du prix seulement dû à l’acte.',
  'Wohnungen mit zwei und drei Schlafzimmern und großen Terrassen in Estepona Golf, mit Pool, Fitnessraum und Social Club; 60 % des Preises werden erst bei der Beurkundung fällig.',
  'Квартиры с двумя и тремя спальнями и большими террасами в Estepona Golf, с бассейном, тренажёрным залом и общественным клубом; 60 % цены оплачивается только при оформлении акта.',
  'شقق بغرفتي نوم وثلاث غرف نوم مع تراسات واسعة في Estepona Golf، مع مسبح ونادٍ رياضي ونادٍ اجتماعي، ولا يُدفع 60% من السعر إلا عند توقيع سند الملكية.',
  'Appartementen met twee en drie slaapkamers en grote terrassen in Estepona Golf, met een zwembad, een sportschool en een sociale club, waarbij 60% van de prijs pas bij de akte verschuldigd is.',
  'Mieszkania z dwiema i trzema sypialniami oraz dużymi tarasami w Estepona Golf, z basenem, siłownią i klubem towarzyskim, a 60% ceny płatne dopiero przy akcie notarialnym.',
  'Leiligheter med to og tre soverom og store terrasser i Estepona Golf, med basseng, treningsrom og sosial klubb, der 60 % av prisen forfaller først ved skjøtet.',
  'Lägenheter med två och tre sovrum och stora terrasser i Estepona Golf, med pool, gym och social klubb, där 60 % av priset förfaller först vid lagfarten.')
a('.why.points[0][1]',
  'Compradores que buscan un apartamento nuevo de dos o tres dormitorios en Estepona Golf, con terraza o jardín, plaza de aparcamiento y trastero, para vivir o como segunda residencia.',
  'Acheteurs qui recherchent un appartement neuf de deux ou trois chambres à Estepona Golf, avec terrasse ou jardin, place de parking et débarras, pour y vivre ou comme résidence secondaire.',
  'Käufer, die eine neue Wohnung mit zwei oder drei Schlafzimmern in Estepona Golf suchen, mit Terrasse oder Garten, Stellplatz und Abstellraum, zum Wohnen oder als Zweitwohnsitz.',
  'Покупатели, которые ищут новую квартиру с двумя или тремя спальнями в Estepona Golf, с террасой или садом, машиноместом и кладовой, для проживания или как второй дом.',
  'المشترون الباحثون عن شقة جديدة بغرفتي نوم أو ثلاث غرف نوم في Estepona Golf، مع تراس أو حديقة وموقف سيارة ومخزن، للسكن أو كمسكن ثانٍ.',
  'Kopers die een nieuw appartement met twee of drie slaapkamers in Estepona Golf zoeken, met een terras of een tuin, een parkeerplaats en een berging, om in te wonen of als tweede woning.',
  'Kupujący szukający nowego mieszkania z dwiema lub trzema sypialniami w Estepona Golf, z tarasem lub ogrodem, miejscem postojowym i komórką lokatorską, do zamieszkania lub jako druga nieruchomość.',
  'Kjøpere som søker en ny leilighet med to eller tre soverom i Estepona Golf, med terrasse eller hage, parkeringsplass og bod, til å bo i eller som feriebolig.',
  'Köpare som söker en ny lägenhet med två eller tre sovrum i Estepona Golf, med terrass eller trädgård, parkeringsplats och förråd, för att bo i eller som andrabostad.')
a('.why.points[1][1]',
  'El dossier sitúa las viviendas dentro del campo de golf de Estepona Golf, con vistas abiertas al green, y las zonas comunes incluyen aparcamiento para buggies de golf a nivel del campo. Las terrazas de las viviendas con precio van de 22,25 m² (24F, cubierta) a 88,71 m² (25A, descubierta).',
  'Le dossier situe les logements au sein du parcours de Estepona Golf, avec des vues dégagées sur le green, et les parties communes comprennent un parking pour voiturettes de golf au niveau du parcours. Les terrasses des logements avec un prix vont de 22,25 m² (24F, couverte) à 88,71 m² (25A, découverte).',
  'Die Dokumentation verortet die Immobilien innerhalb des Golfplatzes von Estepona Golf, mit offenem Blick auf das Grün; zu den Gemeinschaftsflächen gehören Parkplätze für Golfbuggys auf Höhe des Platzes. Die Terrassen der Immobilien mit Preis reichen von 22,25 m² (24F, überdacht) bis 88,71 m² (25A, offen).',
  'В досье жильё расположено на территории гольф-поля Estepona Golf, с открытым видом на грин, а в общих зонах предусмотрена парковка для гольф-каров на уровне поля. Террасы объектов с ценой — от 22,25 м² (24F, крытая) до 88,71 м² (25A, открытая).',
  'يضع الملف المساكن داخل ملعب الغولف في Estepona Golf، مع إطلالات مفتوحة على المساحة الخضراء، وتشمل المناطق المشتركة موقفًا لعربات الغولف على مستوى الملعب. وتتراوح مساحات تراسات المساكن ذات السعر بين 22.25 م² (24F، مسقوف) و88.71 م² (25A، مكشوف).',
  'Het dossier plaatst de woningen binnen de golfbaan van Estepona Golf, met open uitzicht over de green, en de gemeenschappelijke ruimtes omvatten een parkeerplaats voor golfbuggy’s op baanniveau. De terrassen van de woningen met een prijs lopen van 22,25 m² (24F, overdekt) tot 88,71 m² (25A, open).',
  'Dossier umieszcza lokale na terenie pola golfowego Estepona Golf, z otwartym widokiem na green, a części wspólne obejmują parking dla melexów golfowych na poziomie pola. Tarasy lokali z ceną mają od 22,25 m² (24F, zadaszony) do 88,71 m² (25A, odkryty).',
  'Dossieret plasserer boligene innenfor golfbanen i Estepona Golf, med åpen utsikt over greenen, og fellesarealene omfatter parkering for golfbiler på banenivå. Terrassene til boligene med pris varierer fra 22,25 m² (24F, overbygd) til 88,71 m² (25A, åpen).',
  'Dossiern placerar bostäderna inom golfbanan i Estepona Golf, med öppen utsikt över greenen, och de gemensamma ytorna omfattar parkering för golfbilar på banans nivå. Terrasserna för bostäderna med pris går från 22,25 m² (24F, övertäckt) till 88,71 m² (25A, öppen).')
a('.why.points[2][1]',
  'La reserva es de {E12000} + IVA y el 20% + IVA vence con el contrato privado. El 60% + IVA vence solo en la escritura, a la finalización y entrega de llaves.',
  'La réservation est de {E12000} + TVA et 20 % + TVA sont dus au contrat privé. 60 % + TVA ne sont dus qu’à l’acte, à l’achèvement et à la remise des clés.',
  'Die Reservierung beträgt {E12000} + MwSt., und 20 % + MwSt. sind beim privaten Kaufvertrag fällig. 60 % + MwSt. werden erst bei der Beurkundung fällig, bei Fertigstellung und Schlüsselübergabe.',
  'Бронирование стоит {E12000} + НДС, а 20 % + НДС подлежат оплате при подписании частного договора. 60 % + НДС оплачиваются только при оформлении акта, по завершении строительства и передаче ключей.',
  'يبلغ الحجز {E12000} + ضريبة القيمة المضافة، وتُستحق نسبة 20% + ضريبة القيمة المضافة عند توقيع العقد الخاص. ولا تُستحق نسبة 60% + ضريبة القيمة المضافة إلا عند توقيع سند الملكية، عند الإنجاز وتسليم المفاتيح.',
  'De reservering bedraagt {E12000} + btw en 20% + btw is verschuldigd bij het privécontract. 60% + btw is pas verschuldigd bij de akte, bij oplevering en overhandiging van de sleutels.',
  'Rezerwacja kosztuje {E12000} + VAT, a 20% + VAT płatne jest przy umowie prywatnej. 60% + VAT płatne jest dopiero przy akcie notarialnym, po ukończeniu i wydaniu kluczy.',
  'Reservasjonen er {E12000} + mva., og 20 % + mva. forfaller ved den private kontrakten. 60 % + mva. forfaller først ved skjøtet, ved ferdigstillelse og nøkkeloverlevering.',
  'Bokningen är {E12000} + IVA, och 20 % + IVA förfaller vid det privata avtalet. 60 % + IVA förfaller först vid lagfarten, vid färdigställande och nyckelöverlämning.')
a('.why.points[3][1]',
  'Hay 35 de las 43 viviendas de la lista marcadas como reservadas, y la lista dice que sus precios son válidos durante dos días desde su descarga. Confirmamos precio y disponibilidad antes de cualquier reserva.',
  '35 des 43 logements de la liste sont marqués comme réservés, et la liste indique que ses prix sont valables deux jours après son téléchargement. Nous confirmons le prix et la disponibilité avant toute réservation.',
  '35 der 43 Immobilien auf der Liste sind als reserviert gekennzeichnet, und die Liste gibt an, dass ihre Preise zwei Tage nach dem Herunterladen gültig sind. Wir bestätigen Preis und Verfügbarkeit vor jeder Reservierung.',
  '35 из 43 объектов списка отмечены как зарезервированные, а в списке сказано, что его цены действительны два дня после загрузки. Мы подтверждаем цену и наличие перед любым бронированием.',
  'يوجد 35 من أصل 43 مسكنًا في القائمة موسومة بأنها محجوزة، وتذكر القائمة أن أسعارها سارية لمدة يومين بعد تنزيلها. ونؤكد السعر والتوافر قبل أي حجز.',
  '35 van de 43 woningen op de lijst zijn gemarkeerd als gereserveerd, en de lijst zegt dat de prijzen twee dagen na het downloaden geldig zijn. Wij bevestigen prijs en beschikbaarheid vóór elke reservering.',
  '35 z 43 lokali na liście jest oznaczonych jako zarezerwowane, a lista podaje, że jej ceny obowiązują przez dwa dni od pobrania. Cenę i dostępność potwierdzamy przed każdą rezerwacją.',
  '35 av de 43 boligene på listen er markert som reservert, og listen sier at prisene gjelder i to dager etter at den er lastet ned. Vi bekrefter pris og tilgjengelighet før enhver reservasjon.',
  '35 av de 43 bostäderna på listan är markerade som reserverade, och listan anger att priserna gäller i två dagar efter nedladdning. Vi bekräftar pris och tillgänglighet före varje bokning.')

a('.architecture.headlineHtml',
  'Terrazas curvas, <em>vidrio y vegetación</em>', 'Terrasses courbes, <em>verre et végétation</em>', 'Geschwungene Terrassen, <em>Glas und Grün</em>',
  'Изогнутые террасы, <em>стекло и зелень</em>', 'تراسات منحنية، <em>زجاج ونباتات</em>', 'Gebogen terrassen, <em>glas en groen</em>',
  'Zakrzywione tarasy, <em>szkło i zieleń</em>', 'Buede terrasser, <em>glass og grønt</em>', 'Böjda terrasser, <em>glas och grönska</em>')
a('.architecture.copy[0]',
  'En las imágenes generadas por ordenador del promotor, el edificio tiene largas losas de terraza curvas en un tono de piedra clara y otro de madera, con barandillas de vidrio, palmeras y bordes plantados, y se alza sobre un talud de césped por encima del campo. La lista de precios y los planos nombran dos bloques.',
  'Dans les images générées par ordinateur du promoteur, le bâtiment présente de longues dalles de terrasse courbes dans une teinte de pierre claire et une teinte bois, avec des garde-corps en verre, des palmiers et des bordures plantées, et se dresse sur un talus de pelouse au-dessus du parcours. La liste de prix et les plans nomment deux immeubles.',
  'In den computergenerierten Bildern des Bauträgers hat das Gebäude lange, geschwungene Terrassenplatten in hellem Steinton und Holzton, mit Glasbrüstungen, Palmen und bepflanzten Rändern, und steht auf einem Grashang über dem Platz. Die Preisliste und die Pläne nennen zwei Blöcke.',
  'На компьютерных изображениях застройщика здание имеет длинные изогнутые плиты террас в тонах светлого камня и дерева, со стеклянными ограждениями, пальмами и озеленёнными краями и стоит на травяном склоне над полем. В прайс-листе и на планах названы два корпуса.',
  'في صور المطوّر المولَّدة بالحاسوب، للمبنى بلاطات تراسات طويلة منحنية بلون الحجر الفاتح ولون الخشب، مع حواجز زجاجية ونخيل وحواف مزروعة، ويقوم على منحدر عشبي فوق الملعب. وتذكر قائمة الأسعار والمخططات مبنيين.',
  'In de computergegenereerde beelden van de ontwikkelaar heeft het gebouw lange, gebogen terrasplaten in een lichte steentint en een houttint, met glazen balustrades, palmen en beplante randen, en staat het op een grashelling boven de baan. De prijslijst en de plattegronden noemen twee blokken.',
  'Na wygenerowanych komputerowo obrazach dewelopera budynek ma długie, zakrzywione płyty tarasów w tonacji jasnego kamienia i drewna, ze szklanymi balustradami, palmami i obsadzonymi krawędziami, i stoi na trawiastej skarpie nad polem. Cennik i plany wymieniają dwa budynki.',
  'På utbyggerens datagenererte bilder har bygningen lange, buede terrasseplater i en lys steinfarge og en trefarge, med glassrekkverk, palmer og beplantede kanter, og står på en gressskråning over banen. Prislisten og tegningene nevner to blokker.',
  'På exploatörens datorgenererade bilder har byggnaden långa, böjda terrassplattor i en ljus stenton och en trätton, med glasräcken, palmer och planterade kanter, och står på en gräsluttning ovanför banan. Prislistan och ritningarna nämner två hus.')
a('.architecture.copy[1]',
  'El informe de calidades describe una fachada de doble hoja de ladrillo perforado con revoco, cubiertas planas con doble impermeabilización y albañilería acústica entre viviendas, con agua caliente aerotérmica y paneles fotovoltaicos en las cubiertas.',
  'Le rapport de qualité décrit une façade à double paroi en brique perforée avec enduit, des toitures planes à double étanchéité et une maçonnerie acoustique entre les logements, avec eau chaude aérothermique et panneaux photovoltaïques en toiture.',
  'Der Qualitätsbericht beschreibt eine zweischalige Fassade aus Lochziegeln mit Putz, Flachdächer mit doppelter Abdichtung und schalldämmendes Mauerwerk zwischen den Wohnungen, mit aerothermischer Warmwasserbereitung und Photovoltaikmodulen auf den Dächern.',
  'В отчёте о качестве описаны фасад с воздушной прослойкой из пустотелого кирпича с штукатуркой, плоские кровли с двойной гидроизоляцией и звукоизоляционная кладка между жилыми единицами, а также аэротермальное горячее водоснабжение и фотоэлектрические панели на крышах.',
  'يصف تقرير الجودة واجهة بجدار مزدوج من الطوب المثقّب مع طلاء، وأسطحًا مستوية بعزل مائي مزدوج، وبناءً عازلًا للصوت بين المساكن، مع ماء ساخن بالطاقة الهوائية الحرارية وألواح كهروضوئية على الأسطح.',
  'Het kwaliteitsrapport beschrijft een spouwgevel van geperforeerde baksteen met pleisterwerk, platte daken met dubbele waterdichting en akoestisch metselwerk tussen de woningen, met aerothermisch warm water en zonnepanelen op de daken.',
  'Raport jakości opisuje fasadę dwuwarstwową z cegły dziurawki z tynkiem, dachy płaskie z podwójną hydroizolacją oraz akustyczny mur między lokalami, z aerotermalną ciepłą wodą i panelami fotowoltaicznymi na dachach.',
  'Kvalitetsrapporten beskriver en hulromsfasade av hullmurstein med puss, flate tak med dobbel tetting og lydisolerende murverk mellom boligene, med aerotermisk varmtvann og solcellepaneler på takene.',
  'Kvalitetsrapporten beskriver en luftspaltsfasad av hålsten med puts, platta tak med dubbel fuktisolering och ljudisolerande murverk mellan bostäderna, med aerotermiskt varmvatten och solcellspaneler på taken.')
a('.architecture.highlights[0][1]',
  'Un muro de doble hoja de ladrillo perforado con revoco exterior, aislamiento de poliuretano proyectado, cámara de aire y trasdosado interior de lana mineral y yeso laminado.',
  'Un mur à double paroi en brique perforée avec enduit extérieur, isolation en polyuréthane projeté, lame d’air et doublage intérieur en laine minérale et plaques de plâtre.',
  'Eine zweischalige Wand aus Lochziegeln mit Außenputz, Dämmung aus Spritzpolyurethan, Luftschicht und Innenverkleidung aus Mineralwolle und Gipskarton.',
  'Стена с воздушной прослойкой из пустотелого кирпича с наружной штукатуркой, напылённой полиуретановой теплоизоляцией, воздушным зазором и внутренней обшивкой из минеральной ваты и гипсокартона.',
  'جدار مزدوج من الطوب المثقّب مع طلاء خارجي وعزل بالبولي يوريثان المرشوش وفراغ هوائي وتبطين داخلي من الصوف المعدني والجبس.',
  'Een spouwmuur van geperforeerde baksteen met buitenpleister, gespoten polyurethaanisolatie, een luchtspouw en een binnenbekleding van mineraalwol en gipsplaat.',
  'Mur dwuwarstwowy z cegły dziurawki z tynkiem zewnętrznym, izolacją z natryskowego poliuretanu, pustką powietrzną i wewnętrzną okładziną z wełny mineralnej i płyty gipsowo-kartonowej.',
  'En hulmur av hullmurstein med utvendig puss, sprøytet polyuretanisolasjon, luftspalte og innvendig kledning av mineralull og gips.',
  'En luftspaltsvägg av hålsten med utvändig puts, sprutad polyuretanisolering, luftspalt och invändig beklädnad av mineralull och gips.')
a('.architecture.highlights[1][0]',
  'Entre viviendas', 'Entre les logements', 'Zwischen den Wohnungen', 'Между жилыми единицами', 'بين المساكن', 'Tussen de woningen', 'Między lokalami', 'Mellom boligene', 'Mellan bostäderna')
a('.architecture.highlights[1][1]',
  'Albañilería acústica con yeso laminado en ambas caras sobre perfilería de acero galvanizado y aislamiento de lana mineral.',
  'Maçonnerie acoustique avec plaques de plâtre sur les deux faces, sur ossature en acier galvanisé et isolation en laine minérale.',
  'Schalldämmendes Mauerwerk mit Gipskarton auf beiden Seiten über Ständerwerk aus verzinktem Stahl und Mineralwolledämmung.',
  'Звукоизоляционная кладка с гипсокартоном с обеих сторон по каркасу из оцинкованной стали и изоляцией из минеральной ваты.',
  'بناء عازل للصوت مع ألواح جبس على الوجهين فوق هيكل من الفولاذ المجلفن وعزل من الصوف المعدني.',
  'Akoestisch metselwerk met gipsplaat aan beide zijden over een frame van verzinkt staal en isolatie van mineraalwol.',
  'Akustyczny mur z płytą gipsowo-kartonową po obu stronach na stelażu ze stali ocynkowanej z izolacją z wełny mineralnej.',
  'Lydisolerende murverk med gips på begge sider over stålstendere i galvanisert stål og mineralullisolasjon.',
  'Ljudisolerande murverk med gips på båda sidor över galvaniserade stålreglar och mineralullsisolering.')
a('.architecture.highlights[2][1]',
  'Carpintería de PVC o aluminio, oscilobatiente o corredera, con doble acristalamiento tipo Climalit, vidrio laminado de seguridad en las puertas de terraza y persianas de aluminio aislado en los dormitorios.',
  'Menuiseries en PVC ou en aluminium, oscillo-battantes ou coulissantes, avec double vitrage de type Climalit, verre feuilleté de sécurité aux portes de terrasse et volets roulants en aluminium isolé dans les chambres.',
  'Rahmen aus PVC oder Aluminium, Dreh-Kipp oder Schiebe, mit Doppelverglasung vom Typ Climalit, Sicherheitsverbundglas an den Terrassentüren und gedämmten Aluminium-Rollläden in den Schlafzimmern.',
  'Рамы из ПВХ или алюминия, поворотно-откидные или раздвижные, с двойным остеклением типа Climalit, безопасным многослойным стеклом на дверях террас и изолированными алюминиевыми рольставнями в спальнях.',
  'إطارات من PVC أو الألمنيوم، قلّابة أو منزلقة، بزجاج مزدوج من نوع Climalit، وزجاج رقائقي للسلامة في أبواب التراسات وستائر ألمنيوم معزولة في غرف النوم.',
  'Kozijnen van pvc of aluminium, draai-kiep of schuif, met dubbele beglazing van het type Climalit, veiligheidslaminaatglas in de terrasdeuren en geïsoleerde aluminium rolluiken in de slaapkamers.',
  'Ramy z PCV lub aluminium, rozwierno-uchylne lub przesuwne, z podwójnym szkleniem typu Climalit, bezpiecznym szkłem laminowanym w drzwiach tarasowych i izolowanymi aluminiowymi roletami w sypialniach.',
  'Rammer av PVC eller aluminium, sving-tilt eller skyv, med dobbelt glass av typen Climalit, sikkerhetslaminert glass i terrassedørene og isolerte aluminiumsrullegardiner i soverommene.',
  'Karmar av PVC eller aluminium, vrid-tipp eller skjut, med dubbelglas av typen Climalit, säkerhetslaminerat glas i terrassdörrarna och isolerade aluminiumrullgardiner i sovrummen.')
a('.architecture.highlights[3][1]',
  'Agua caliente aerotérmica, paneles fotovoltaicos en las cubiertas como exige el Código Técnico de la Edificación y aire acondicionado por conductos de frío y calor.',
  'Eau chaude aérothermique, panneaux photovoltaïques en toiture comme l’exige le Code technique du bâtiment espagnol et climatisation réversible par gaines.',
  'Aerothermische Warmwasserbereitung, Photovoltaikmodule auf den Dächern, wie sie der spanische Bautechnische Kodex verlangt, und Warm- und Kaltluft-Klimatisierung über Kanäle.',
  'Аэротермальное горячее водоснабжение, фотоэлектрические панели на крышах, как того требует испанский Строительный кодекс, и канальное кондиционирование на тепло и холод.',
  'ماء ساخن بالطاقة الهوائية الحرارية وألواح كهروضوئية على الأسطح كما يشترط قانون البناء الإسباني وتكييف هواء ساخن وبارد عبر مجارٍ.',
  'Aerothermisch warm water, zonnepanelen op de daken zoals de Spaanse bouwcode voorschrijft en kanaalairconditioning voor warme en koude lucht.',
  'Aerotermalna ciepła woda, panele fotowoltaiczne na dachach, jak wymaga hiszpański Kodeks Techniczny Budownictwa, oraz kanałowa klimatyzacja ciepłego i zimnego powietrza.',
  'Aerotermisk varmtvann, solcellepaneler på takene slik den spanske byggeforskriften krever, og kanalbasert klimaanlegg for varm og kald luft.',
  'Aerotermiskt varmvatten, solcellspaneler på taken enligt spanska byggnormen och kanalansluten luftkonditionering för varm och kall luft.')

# ---- quality specification ----------------------------------------------------------------------

a('.qualitySpecs.copy',
  'El informe de calidades del propio promotor, resumido por partes de la vivienda.',
  'Le rapport de qualité du promoteur lui-même, résumé par partie du logement.',
  'Der Qualitätsbericht des Bauträgers selbst, nach Bereichen der Immobilie zusammengefasst.',
  'Отчёт о качестве от самого застройщика, сгруппированный по частям жилья.',
  'تقرير الجودة الصادر عن المطوّر نفسه، مُلخَّصًا حسب أجزاء المسكن.',
  'Het kwaliteitsrapport van de ontwikkelaar zelf, samengevat per deel van de woning.',
  'Raport jakości samego dewelopera, podsumowany według części lokalu.',
  'Utbyggerens egen kvalitetsrapport, oppsummert etter del av boligen.',
  'Exploatörens egen kvalitetsrapport, sammanfattad efter del av bostaden.')
a('.qualitySpecs.sourceNote',
  'Fuente: el informe de calidades del 14 de abril de 2026 (revisión 01) y el dossier de calidades, ambos a nombre del promotor. Los dos dicen que la dirección facultativa puede modificar las especificaciones y sustituir partidas por otras similares sin reducir la calidad prevista. El dossier añade que sus imágenes son solo orientativas y que el mobiliario, la decoración y la vegetación que aparecen no forman parte de la oferta. La piedra natural y la madera varían de tono y color.',
  'Source : le rapport de qualité du 14 avril 2026 (révision 01) et le dossier de qualité, tous deux au nom du promoteur. Les deux indiquent que la direction de projet peut modifier les spécifications et remplacer des éléments par d’autres similaires sans réduire la qualité prévue. Le dossier ajoute que ses images ne sont qu’indicatives et que le mobilier, la décoration et la végétation qui y figurent ne font pas partie de l’offre. La pierre naturelle et le bois varient de teinte et de couleur.',
  'Quelle: der Qualitätsbericht vom 14. April 2026 (Revision 01) und das Qualitätsdossier, beide im Namen des Bauträgers. Beide besagen, dass die Projektleitung die Spezifikation ändern und Positionen durch ähnliche ersetzen darf, ohne die geplante Qualität zu mindern. Das Dossier ergänzt, dass seine Bilder nur eine Orientierung sind und dass die gezeigten Möbel, die Dekoration und die Bepflanzung nicht zum Angebot gehören. Naturstein und Holz variieren in Ton und Farbe.',
  'Источник: отчёт о качестве от 14 апреля 2026 года (редакция 01) и досье качества, оба от имени застройщика. В обоих сказано, что руководство проекта может изменять спецификацию и заменять позиции аналогичными без снижения запланированного качества. В досье добавлено, что его изображения носят лишь ориентировочный характер, а показанные мебель, декор и озеленение не входят в предложение. Натуральный камень и дерево различаются по тону и цвету.',
  'المصدر: تقرير الجودة بتاريخ 14 أبريل 2026 (المراجعة 01) وملف الجودة، وكلاهما باسم المطوّر. ويذكر الاثنان أن إدارة المشروع يجوز لها تعديل المواصفات واستبدال بنود ببنود مماثلة دون خفض الجودة المخططة. ويضيف الملف أن صوره للاسترشاد فقط وأن الأثاث والديكور والنباتات الظاهرة فيها ليست جزءًا من العرض. ويختلف الحجر الطبيعي والخشب في الدرجة واللون.',
  'Bron: het kwaliteitsrapport van 14 april 2026 (herziening 01) en het kwaliteitsdossier, beide op naam van de ontwikkelaar. Beide zeggen dat de projectleiding de specificatie mag wijzigen en onderdelen door soortgelijke mag vervangen zonder de geplande kwaliteit te verlagen. Het dossier voegt eraan toe dat de beelden slechts een richtlijn zijn en dat het getoonde meubilair, de inrichting en de beplanting geen deel uitmaken van het aanbod. Natuursteen en hout variëren in tint en kleur.',
  'Źródło: raport jakości z 14 kwietnia 2026 (rewizja 01) i dossier jakości, oba w imieniu dewelopera. Oba dokumenty mówią, że kierownictwo projektu może zmieniać specyfikację i zastępować pozycje podobnymi bez obniżania planowanej jakości. Dossier dodaje, że jego obrazy mają charakter wyłącznie poglądowy, a pokazane meble, wystrój i roślinność nie wchodzą w zakres oferty. Kamień naturalny i drewno różnią się odcieniem i kolorem.',
  'Kilde: kvalitetsrapporten fra 14. april 2026 (revisjon 01) og kvalitetsdossieret, begge i utbyggerens navn. Begge sier at prosjektledelsen kan endre spesifikasjonen og erstatte poster med tilsvarende uten å redusere den planlagte kvaliteten. Dossieret legger til at bildene bare er veiledende, og at møblene, innredningen og beplantningen som vises ikke er en del av tilbudet. Naturstein og tre varierer i tone og farge.',
  'Källa: kvalitetsrapporten från den 14 april 2026 (revision 01) och kvalitetsdossiern, båda i exploatörens namn. Båda anger att projektledningen får ändra specifikationen och ersätta poster med liknande utan att sänka den planerade kvaliteten. Dossiern tillägger att dess bilder bara är vägledande och att de visade möblerna, inredningen och växtligheten inte ingår i erbjudandet. Natursten och trä varierar i ton och färg.')
a('.qualitySpecs.groups[0].items[0]',
  'Baldosas de gres cerámico de 60 x 60 cm en toda la vivienda y revestimiento de 30 x 90 cm en la zona de ducha y en la pared tras el lavabo.',
  'Carreaux de grès cérame de 60 x 60 cm dans tout le logement et revêtement mural de 30 x 90 cm dans la zone de douche et sur le mur derrière le lavabo.',
  'Bodenfliesen aus Keramik-Steinzeug im Format 60 x 60 cm in der gesamten Immobilie und Wandfliesen im Format 30 x 90 cm im Duschbereich und an der Wand hinter dem Waschbecken.',
  'Керамогранитная плитка для пола 60 x 60 см во всём жилье и настенная плитка 30 x 90 см в зоне душа и на стене за раковиной.',
  'بلاط أرضيات من الجرانيت الخزفي بقياس 60 × 60 سم في كامل المسكن وبلاط جدران بقياس 30 × 90 سم في منطقة الدش وعلى الجدار خلف المغسلة.',
  'Keramische steengoed vloertegels van 60 x 60 cm in de hele woning en wandtegels van 30 x 90 cm in de douchezone en op de wand achter de wastafel.',
  'Gresowe płytki podłogowe 60 x 60 cm w całym lokalu oraz płytki ścienne 30 x 90 cm w strefie prysznica i na ścianie za umywalką.',
  'Gulvfliser i keramisk steingods på 60 x 60 cm i hele boligen og veggfliser på 30 x 90 cm i dusjområdet og på veggen bak vasken.',
  'Golvplattor av keramiskt stengods på 60 x 60 cm i hela bostaden och kakel på 30 x 90 cm i duschzonen och på väggen bakom handfatet.')
a('.qualitySpecs.groups[0].items[1]',
  'Baldosas exteriores antideslizantes y resistentes a las heladas en terrazas y patios. El dossier muestra un tono base de suelo y revestimiento y dos tonos más como opción sin coste adicional.',
  'Carreaux extérieurs antidérapants et résistants au gel sur les terrasses et les patios. Le dossier montre une teinte de base pour le sol et le revêtement mural et deux autres teintes en option sans supplément.',
  'Rutschhemmende, frostbeständige Außenfliesen auf Terrassen und Patios. Das Dossier zeigt einen Grundton für Boden- und Wandfliesen und zwei weitere Töne als Option ohne Aufpreis.',
  'Нескользящая морозостойкая плитка для улицы на террасах и патио. В досье показан базовый тон плитки для пола и стен и ещё два тона на выбор без доплаты.',
  'بلاط خارجي مانع للانزلاق ومقاوم للصقيع في التراسات والأفنية. ويعرض الملف درجة أساسية لبلاط الأرضيات والجدران ودرجتين أخريين كخيار دون تكلفة إضافية.',
  'Antislip, vorstbestendige buitentegels op de terrassen en patio’s. Het dossier toont een basistint voor vloer- en wandtegels en twee andere tinten als optie zonder meerprijs.',
  'Antypoślizgowe, mrozoodporne płytki zewnętrzne na tarasach i patio. Dossier pokazuje bazowy odcień płytek podłogowych i ściennych oraz dwa dalsze odcienie do wyboru bez dopłaty.',
  'Sklisikre, frostbestandige utendørsfliser på terrasser og uteplasser. Dossieret viser en grunntone for gulv- og veggfliser og to andre toner som valg uten tillegg.',
  'Halkfria, frostbeständiga utomhusplattor på terrasser och uteplatser. Dossiern visar en grundton för golv- och väggplattor och ytterligare två toner som tillval utan extra kostnad.')
a('.qualitySpecs.groups[1].items[0]',
  'Cocina equipada con armarios altos y bajos de tablero laminado a presión y frigorífico panelado a juego con los armarios.',
  'Cuisine équipée avec meubles hauts et bas en panneaux stratifiés haute pression et réfrigérateur intégré, habillé comme les meubles.',
  'Einbauküche mit Hoch- und Unterschränken aus Schichtstoffplatten und einem Kühlschrank mit Front passend zu den Schränken.',
  'Кухня с верхними и нижними шкафами из ламинированной плиты высокого давления и встроенным холодильником с фасадом под цвет шкафов.',
  'مطبخ مجهّز بخزائن علوية وسفلية من ألواح مغلّفة بالضغط وثلاجة مكسوّة بألواح تتناسق مع الخزائن.',
  'Een ingerichte keuken met hoge en lage kasten van onder druk gelamineerd plaatmateriaal en een gepaneelde koelkast die bij de kasten past.',
  'Wyposażona kuchnia z szafkami górnymi i dolnymi z płyty laminowanej wysokociśnieniowo oraz lodówką z frontem pasującym do szafek.',
  'Innredet kjøkken med høye og lave skap i trykklaminert plate og et panelt kjøleskap som matcher skapene.',
  'Ett utrustat kök med höga och låga skåp av högtryckslaminerad skiva och ett panelklätt kylskåp som matchar skåpen.')
a('.qualitySpecs.groups[1].items[1]',
  'Placa de cocción cerámica, horno microondas, campana extractora, frigorífico, lavavajillas y lavadora, Bosch o similar. El informe de calidades indica una encimera tipo Silestone y el dossier una de tipo porcelánico, en ambos casos según el diseño del proyecto.',
  'Plaque de cuisson vitrocéramique, four micro-ondes, hotte, réfrigérateur, lave-vaisselle et lave-linge, Bosch ou équivalent. Le rapport de qualité indique un plan de travail de type Silestone et le dossier un plan de type porcelaine, dans les deux cas selon le projet.',
  'Keramikkochfeld, Mikrowellenbackofen, Dunstabzugshaube, Kühlschrank, Geschirrspüler und Waschmaschine, Bosch oder gleichwertig. Der Qualitätsbericht nennt eine Arbeitsplatte vom Typ Silestone und das Dossier eine vom Typ Porzellan, in beiden Fällen nach Projektentwurf.',
  'Керамическая варочная панель, духовой шкаф с микроволновой функцией, вытяжка, холодильник, посудомоечная и стиральная машины, Bosch или аналогичные. В отчёте о качестве указана столешница типа Silestone, а в досье — типа керамогранит, в обоих случаях по дизайну проекта.',
  'موقد سيراميك وفرن مع ميكروويف ومروحة شفط وثلاجة وغسالة أطباق وغسالة ملابس، من Bosch أو ما يماثلها. ويذكر تقرير الجودة سطح عمل من نوع Silestone ويذكر الملف سطحًا من نوع البورسلين، وفي الحالتين بحسب تصميم المشروع.',
  'Een keramische kookplaat, een combimagnetron, een afzuigkap, een koelkast, een vaatwasser en een wasmachine, Bosch of gelijkwaardig. Het kwaliteitsrapport noemt een werkblad van het type Silestone en het dossier een van het type porselein, in beide gevallen volgens het ontwerp van het project.',
  'Płyta ceramiczna, piekarnik z mikrofalą, okap, lodówka, zmywarka i pralka, Bosch lub równoważne. Raport jakości podaje blat typu Silestone, a dossier blat typu porcelana, w obu przypadkach zgodnie z projektem.',
  'Keramisk kokeplate, ovn med mikrobølge, ventilator, kjøleskap, oppvaskmaskin og vaskemaskin, Bosch eller tilsvarende. Kvalitetsrapporten oppgir en benkeplate av typen Silestone og dossieret en av typen porselen, i begge tilfeller etter prosjektets utforming.',
  'Keramikhäll, ugn med mikrovågsfunktion, fläkt, kylskåp, diskmaskin och tvättmaskin, Bosch eller likvärdigt. Kvalitetsrapporten anger en bänkskiva av typen Silestone och dossiern en av typen porslin, i båda fallen enligt projektets utformning.')
a('.qualitySpecs.groups[2].items[0]',
  'Sanitarios de porcelana vitrificada blanca, plato de ducha de resina en el baño principal y bañera de acero esmaltado en el segundo.',
  'Appareils sanitaires en porcelaine vitrifiée blanche, receveur de douche en résine dans la salle de bains principale et baignoire en acier émaillé dans la seconde.',
  'Sanitärkeramik aus weißem Porzellan, Duschwanne aus Kunstharz im Hauptbad und emaillierte Stahlbadewanne im zweiten Bad.',
  'Сантехника из белого глазурованного фарфора, душевой поддон из смолы в главной ванной и эмалированная стальная ванна во второй.',
  'أدوات صحية من البورسلين الأبيض المزجّج، وحوض دش من الراتنج في الحمّام الرئيسي وحوض استحمام من الفولاذ المطلي بالمينا في الحمّام الثاني.',
  'Sanitair van wit verglaasd porselein, een douchebak van hars in de hoofdbadkamer en een geëmailleerd stalen bad in de tweede.',
  'Armatura sanitarna z białej porcelany witryfikowanej, brodzik żywiczny w głównej łazience i wanna ze stali emaliowanej w drugiej.',
  'Sanitærutstyr i hvitt glasert porselen, dusjkar av harpiks på hovedbadet og emaljert stålbadekar på det andre.',
  'Vitt glaserat sanitetsporslin, duschkar av harts i huvudbadrummet och emaljerat stålbadkar i det andra.')
a('.qualitySpecs.groups[2].items[1]',
  'Columna de ducha con grifo monomando, Grohe o similar, y en el baño principal un mueble de lavabo y una mampara de ducha.',
  'Colonne de douche avec mitigeur monocommande, Grohe ou équivalent, et dans la salle de bains principale un meuble vasque et un pare-douche.',
  'Duschsäule mit Einhebelmischer, Grohe oder gleichwertig, und im Hauptbad ein Waschtischunterschrank und eine Duschabtrennung.',
  'Душевая колонна с однорычажным смесителем, Grohe или аналогичная, а в главной ванной — тумба под раковину и душевая перегородка.',
  'عمود دش بخلاط بذراع واحدة، من Grohe أو ما يماثله، وفي الحمّام الرئيسي وحدة مغسلة وحاجز دش.',
  'Een doucheset met eengreepsmengkraan, Grohe of gelijkwaardig, en in de hoofdbadkamer een wastafelmeubel en een douchescherm.',
  'Kolumna prysznicowa z baterią jednouchwytową, Grohe lub równoważna, a w głównej łazience szafka pod umywalkę i kabina prysznicowa.',
  'Dusjsøyle med énhåndsblander, Grohe eller tilsvarende, og på hovedbadet et vaskeskap og en dusjvegg.',
  'Duschpelare med enhandsblandare, Grohe eller likvärdig, och i huvudbadrummet ett tvättställsskåp och en duschvägg.')
a('.qualitySpecs.groups[3].items[0]',
  'Carpintería de PVC o aluminio con doble acristalamiento tipo Climalit, vidrio laminado de seguridad en las puertas de terraza y persianas de aluminio aislado en los dormitorios.',
  'Menuiseries en PVC ou en aluminium avec double vitrage de type Climalit, verre feuilleté de sécurité aux portes de terrasse et volets roulants en aluminium isolé dans les chambres.',
  'Rahmen aus PVC oder Aluminium mit Doppelverglasung vom Typ Climalit, Sicherheitsverbundglas an den Terrassentüren und gedämmten Aluminium-Rollläden in den Schlafzimmern.',
  'Рамы из ПВХ или алюминия с двойным остеклением типа Climalit, безопасным многослойным стеклом на дверях террас и изолированными алюминиевыми рольставнями в спальнях.',
  'إطارات من PVC أو الألمنيوم بزجاج مزدوج من نوع Climalit، وزجاج رقائقي للسلامة في أبواب التراسات وستائر ألمنيوم معزولة في غرف النوم.',
  'Kozijnen van pvc of aluminium met dubbele beglazing van het type Climalit, veiligheidslaminaatglas in de terrasdeuren en geïsoleerde aluminium rolluiken in de slaapkamers.',
  'Ramy z PCV lub aluminium z podwójnym szkleniem typu Climalit, bezpiecznym szkłem laminowanym w drzwiach tarasowych i izolowanymi aluminiowymi roletami w sypialniach.',
  'Rammer av PVC eller aluminium med dobbelt glass av typen Climalit, sikkerhetslaminert glass i terrassedørene og isolerte aluminiumsrullegardiner i soverommene.',
  'Karmar av PVC eller aluminium med dubbelglas av typen Climalit, säkerhetslaminerat glas i terrassdörrarna och isolerade aluminiumrullgardiner i sovrummen.')
a('.qualitySpecs.groups[3].items[1]',
  'Puertas interiores lacadas en blanco con manillas cromadas o sistemas correderos, y armarios modulares empotrados con puertas a juego.',
  'Portes intérieures laquées blanc avec poignées chromées ou systèmes coulissants, et placards modulaires encastrés avec portes assorties.',
  'Weiß lackierte Innentüren mit verchromten Griffen oder Schiebesystemen und eingebaute modulare Schränke mit passenden Türen.',
  'Белые лакированные межкомнатные двери с хромированными ручками или раздвижные системы и встроенные модульные шкафы с дверями в тон.',
  'أبواب داخلية مطلية باللاكر الأبيض بمقابض مطلية بالكروم أو أنظمة منزلقة، وخزائن مدمجة مجزأة بأبواب مماثلة.',
  'Wit gelakte binnendeuren met verchroomde deurkrukken of schuifsystemen, en ingebouwde modulaire kasten met bijpassende deuren.',
  'Białe lakierowane drzwi wewnętrzne z chromowanymi klamkami lub systemy przesuwne oraz zabudowane szafy modułowe z pasującymi drzwiami.',
  'Hvitlakkerte innerdører med forkrommede håndtak eller skyvesystemer, og innebygde modulgarderober med dører som matcher.',
  'Vitlackerade innerdörrar med förkromade handtag eller skjutsystem och inbyggda modulgarderober med matchande dörrar.')
a('.qualitySpecs.groups[4].items[0]',
  'Agua caliente aerotérmica, aire acondicionado por conductos de frío y calor en el salón y los dormitorios con toma de aire en la cocina, y ventilación mecánica individual en baños y cocinas.',
  'Eau chaude aérothermique, climatisation réversible par gaines dans le séjour et les chambres avec une prise d’air dans la cuisine, et ventilation mécanique individuelle dans les salles de bains et les cuisines.',
  'Aerothermische Warmwasserbereitung, Warm- und Kaltluft-Klimatisierung über Kanäle im Wohnzimmer und in den Schlafzimmern mit einer Luftzufuhr in der Küche sowie individuelle mechanische Lüftung in Bädern und Küchen.',
  'Аэротермальное горячее водоснабжение, канальное кондиционирование на тепло и холод в гостиной и спальнях с подачей воздуха на кухне и индивидуальная механическая вентиляция в ванных комнатах и на кухнях.',
  'ماء ساخن بالطاقة الهوائية الحرارية وتكييف هواء ساخن وبارد عبر مجارٍ في غرفة الجلوس وغرف النوم مع مدخل هواء في المطبخ، وتهوية ميكانيكية فردية في الحمّامات والمطابخ.',
  'Aerothermisch warm water, kanaalairconditioning voor warme en koude lucht in de woonkamer en de slaapkamers met een luchttoevoer in de keuken, en individuele mechanische ventilatie in de badkamers en keukens.',
  'Aerotermalna ciepła woda, kanałowa klimatyzacja ciepłego i zimnego powietrza w salonie i sypialniach z nawiewem w kuchni oraz indywidualna wentylacja mechaniczna w łazienkach i kuchniach.',
  'Aerotermisk varmtvann, kanalbasert klimaanlegg for varm og kald luft i stuen og soverommene med lufttilførsel i kjøkkenet, og individuell mekanisk ventilasjon på bad og kjøkken.',
  'Aerotermiskt varmvatten, kanalansluten luftkonditionering för varm och kall luft i vardagsrummet och sovrummen med lufttillförsel i köket, och individuell mekanisk ventilation i badrum och kök.')
a('.qualitySpecs.groups[4].items[1]',
  'Paneles fotovoltaicos en las cubiertas, como exige el Código Técnico de la Edificación.',
  'Panneaux photovoltaïques en toiture, comme l’exige le Code technique du bâtiment espagnol.',
  'Photovoltaikmodule auf den Dächern, wie sie der spanische Bautechnische Kodex verlangt.',
  'Фотоэлектрические панели на крышах, как того требует испанский Строительный кодекс.',
  'ألواح كهروضوئية على الأسطح كما يشترط قانون البناء الإسباني.',
  'Zonnepanelen op de daken, zoals de Spaanse bouwcode voorschrijft.',
  'Panele fotowoltaiczne na dachach, jak wymaga hiszpański Kodeks Techniczny Budownictwa.',
  'Solcellepaneler på takene, slik den spanske byggeforskriften krever.',
  'Solcellspaneler på taken enligt spanska byggnormen.')
a('.qualitySpecs.groups[5].name',
  'Tecnología y seguridad', 'Technologie et sécurité', 'Technik und Sicherheit', 'Технологии и безопасность', 'التقنية والأمان', 'Technologie en veiligheid', 'Technologia i bezpieczeństwo', 'Teknologi og sikkerhet', 'Teknik och säkerhet')
a('.qualitySpecs.groups[5].items[0]',
  'Tomas de TV y ethernet en el salón, la cocina y los dormitorios, iluminación exterior en terrazas y patios, un grifo de agua en las terrazas y un punto de carga preinstalado para un vehículo eléctrico.',
  'Prises TV et ethernet dans le séjour, la cuisine et les chambres, éclairage extérieur sur les terrasses et les patios, un robinet d’eau sur les terrasses et un point de recharge préinstallé pour véhicule électrique.',
  'TV- und Ethernet-Anschlüsse im Wohnzimmer, in der Küche und in den Schlafzimmern, Außenbeleuchtung auf Terrassen und Patios, ein Wasseranschluss auf den Terrassen und eine vorinstallierte Ladestelle für ein Elektrofahrzeug.',
  'Розетки для ТВ и сети Ethernet в гостиной, на кухне и в спальнях, наружное освещение на террасах и патио, водопроводный кран на террасах и заранее подготовленная точка зарядки электромобиля.',
  'مآخذ تلفاز وإيثرنت في غرفة الجلوس والمطبخ وغرف النوم، وإضاءة خارجية في التراسات والأفنية، وصنبور مياه في التراسات، ونقطة شحن مجهّزة مسبقًا لسيارة كهربائية.',
  'Tv- en ethernetaansluitingen in de woonkamer, de keuken en de slaapkamers, buitenverlichting op de terrassen en patio’s, een watertap op de terrassen en een voorbereid laadpunt voor een elektrisch voertuig.',
  'Gniazda TV i ethernet w salonie, kuchni i sypialniach, oświetlenie zewnętrzne na tarasach i patio, kran z wodą na tarasach oraz fabrycznie przygotowany punkt ładowania pojazdu elektrycznego.',
  'TV- og ethernet-uttak i stuen, kjøkkenet og soverommene, utebelysning på terrasser og uteplasser, en vannkran på terrassene og et forhåndsinstallert ladepunkt for elbil.',
  'TV- och ethernetuttag i vardagsrummet, köket och sovrummen, utomhusbelysning på terrasser och uteplatser, en vattenkran på terrasserna och en förberedd laddpunkt för elbil.')
a('.qualitySpecs.groups[5].items[1]',
  'Puerta de entrada blindada, sistema de llave maestra, videoportero en el acceso y en el edificio, ascensores con puertas automáticas y acceso para personas con discapacidad, y un complejo cerrado con acceso privado.',
  'Porte d’entrée blindée, système de passe général, interphone vidéo à l’entrée et à l’immeuble, ascenseurs à portes automatiques et accès pour personnes handicapées, et ensemble fermé à accès privé.',
  'Gepanzerte Wohnungseingangstür, Generalschlüsselsystem, Videosprechanlage am Eingang und am Gebäude, Aufzüge mit automatischen Türen und behindertengerechtem Zugang sowie eine abgeschlossene Anlage mit privatem Zugang.',
  'Бронированная входная дверь, система мастер-ключа, видеодомофон на входе и в здании, лифты с автоматическими дверями и доступом для маломобильных людей, закрытый комплекс с частным въездом.',
  'باب دخول مصفّح، ونظام مفتاح رئيسي، وجهاز اتصال مرئي عند المدخل وفي المبنى، ومصاعد بأبواب أوتوماتيكية ومدخل لذوي الإعاقة، ومجمّع مسوَّر بمدخل خاص.',
  'Een gepantserde voordeur, een mastersleutelsysteem, een videofoon bij de ingang en bij het gebouw, liften met automatische deuren en toegang voor mindervaliden, en een afgesloten complex met privétoegang.',
  'Drzwi wejściowe antywłamaniowe, system klucza generalnego, wideodomofon przy wejściu i w budynku, windy z automatycznymi drzwiami i dostępem dla osób niepełnosprawnych oraz zamknięty kompleks z prywatnym wjazdem.',
  'Pansret inngangsdør, hovednøkkelsystem, videointerkom ved inngangen og i bygningen, heiser med automatiske dører og tilgang for funksjonshemmede, og et lukket anlegg med privat adkomst.',
  'Pansardörr i entrén, huvudnyckelsystem, videodörrtelefon vid entrén och i byggnaden, hissar med automatiska dörrar och tillgänglighet för funktionshindrade, och ett inhägnat område med privat tillfart.')

# ---- residences ---------------------------------------------------------------------------------

a('.residences.headlineHtml',
  'Apartamentos de dos y tres <em>dormitorios</em>', 'Appartements de deux et trois <em>chambres</em>', 'Wohnungen mit zwei und drei <em>Schlafzimmern</em>',
  'Квартиры с двумя и тремя <em>спальнями</em>', 'شقق بغرفتي نوم وثلاث <em>غرف نوم</em>', 'Appartementen met twee en drie <em>slaapkamers</em>',
  'Mieszkania z dwiema i trzema <em>sypialniami</em>', 'Leiligheter med to og tre <em>soverom</em>', 'Lägenheter med två och tre <em>sovrum</em>')
a('.residences.copy',
  'Las 8 viviendas con precio se enumeran a continuación con su superficie construida, sus terrazas y, cuando la hay, su jardín. Los documentos no dan otro nombre a un tipo de vivienda.',
  'Les 8 logements avec un prix sont listés ci-dessous avec leur surface construite, leurs terrasses et, le cas échéant, leur jardin. Les documents ne donnent aucun autre nom à un type de logement.',
  'Die 8 Immobilien mit Preis sind unten mit ihrer bebauten Fläche, ihren Terrassen und, falls vorhanden, ihrem Garten aufgeführt. Die Dokumente geben keinem Wohnungstyp einen anderen Namen.',
  'Ниже перечислены 8 объектов с ценой с указанием площади застройки, террас и, если он есть, сада. В документах нет других названий типов жилья.',
  'المساكن الثمانية ذات السعر مدرجة أدناه مع مساحتها المبنية وتراساتها وحديقتها إن وُجدت. ولا تعطي المستندات اسمًا آخر لأي نوع من المساكن.',
  'De 8 woningen met een prijs staan hieronder met hun bebouwde oppervlakte, hun terrassen en, indien aanwezig, hun tuin. De documenten geven geen andere naam aan een type woning.',
  'Poniżej wymieniono 8 lokali z ceną wraz z powierzchnią zabudowy, tarasami i, jeśli jest, ogrodem. Dokumenty nie podają innej nazwy dla żadnego typu lokalu.',
  'De 8 boligene med pris er oppført nedenfor med bebygd areal, terrasser og, der det finnes, hage. Dokumentene gir ingen annen betegnelse på en boligtype.',
  'De 8 bostäderna med pris är listade nedan med byggyta, terrasser och, där sådan finns, trädgård. Dokumenten ger inget annat namn åt någon bostadstyp.')
a('.residences.items[0].points[0]',
  '4 de las 8 tienen dos dormitorios: 13H, 23C, 24C y 24F, con 70,79 a 76,35 m² construidos, desde {E325000} hasta {E490000}.',
  '4 des 8 ont deux chambres : 13H, 23C, 24C et 24F, de 70,79 à 76,35 m² construits, de {E325000} à {E490000}.',
  '4 der 8 haben zwei Schlafzimmer: 13H, 23C, 24C und 24F, mit 70,79 bis 76,35 m² bebauter Fläche, von {E325000} bis {E490000}.',
  '4 из 8 имеют две спальни: 13H, 23C, 24C и 24F, с площадью застройки от {N70.79} до {N76.35} {U}, от {E325000} до {E490000}.',
  '4 من أصل 8 بغرفتي نوم: 13H و23C و24C و24F، بمساحة مبنية من {N70.79} إلى {N76.35} {U}، من {E325000} إلى {E490000}.',
  '4 van de 8 hebben twee slaapkamers: 13H, 23C, 24C en 24F, met 70,79 tot 76,35 m² bebouwd, van {E325000} tot {E490000}.',
  '4 z 8 mają dwie sypialnie: 13H, 23C, 24C i 24F, o powierzchni zabudowy od 70,79 do 76,35 m², od {E325000} do {E490000}.',
  '4 av de 8 har to soverom: 13H, 23C, 24C og 24F, med 70,79 til 76,35 m² bebygd areal, fra {E325000} til {E490000}.',
  '4 av de 8 har två sovrum: 13H, 23C, 24C och 24F, med 70,79 till 76,35 m² byggyta, från {E325000} till {E490000}.')
a('.residences.items[0].points[1]',
  '13H está en la planta baja, con un jardín de 34,00 m² y una terraza cubierta de 25,11 m². 23C tiene una terraza cubierta de 45,22 m² y una descubierta de 51,98 m². 24C y 24F tienen terrazas cubiertas de 36,04 y 22,25 m².',
  '13H est au rez-de-chaussée, avec un jardin de 34,00 m² et une terrasse couverte de 25,11 m². 23C a une terrasse couverte de 45,22 m² et une terrasse découverte de 51,98 m². 24C et 24F ont des terrasses couvertes de 36,04 et 22,25 m².',
  '13H liegt im Erdgeschoss, mit einem Garten von 34,00 m² und einer überdachten Terrasse von 25,11 m². 23C hat eine überdachte Terrasse von 45,22 m² und eine offene von 51,98 m². 24C und 24F haben überdachte Terrassen von 36,04 und 22,25 m².',
  '13H находится на первом этаже, с садом {N34.00} {U} и крытой террасой {N25.11} {U}. У 23C крытая терраса {N45.22} {U} и открытая {N51.98} {U}. У 24C и 24F крытые террасы {N36.04} и {N22.25} {U}.',
  '13H في الطابق الأرضي، مع حديقة مساحتها {N34.00} {U} وتراس مسقوف مساحته {N25.11} {U}. وفي 23C تراس مسقوف مساحته {N45.22} {U} وآخر مكشوف مساحته {N51.98} {U}. وفي 24C و24F تراسان مسقوفان مساحتاهما {N36.04} و{N22.25} {U}.',
  '13H ligt op de begane grond, met een tuin van 34,00 m² en een overdekt terras van 25,11 m². 23C heeft een overdekt terras van 45,22 m² en een open terras van 51,98 m². 24C en 24F hebben overdekte terrassen van 36,04 en 22,25 m².',
  '13H znajduje się na parterze, z ogrodem o powierzchni 34,00 m² i tarasem zadaszonym o powierzchni 25,11 m². 23C ma taras zadaszony o powierzchni 45,22 m² i odkryty o powierzchni 51,98 m². 24C i 24F mają tarasy zadaszone o powierzchni 36,04 i 22,25 m².',
  '13H ligger i første etasje, med en hage på 34,00 m² og en overbygd terrasse på 25,11 m². 23C har en overbygd terrasse på 45,22 m² og en åpen på 51,98 m². 24C og 24F har overbygde terrasser på 36,04 og 22,25 m².',
  '13H ligger på bottenplan, med en trädgård på 34,00 m² och en övertäckt terrass på 25,11 m². 23C har en övertäckt terrass på 45,22 m² och en öppen på 51,98 m². 24C och 24F har övertäckta terrasser på 36,04 och 22,25 m².')
a('.residences.items[1].points[0]',
  '4 de las 8 tienen tres dormitorios: 14C, 15A, 25A y 25D, con 96,60 a 115,56 m² construidos, desde {E470000} hasta {E730000}.',
  '4 des 8 ont trois chambres : 14C, 15A, 25A et 25D, de 96,60 à 115,56 m² construits, de {E470000} à {E730000}.',
  '4 der 8 haben drei Schlafzimmer: 14C, 15A, 25A und 25D, mit 96,60 bis 115,56 m² bebauter Fläche, von {E470000} bis {E730000}.',
  '4 из 8 имеют три спальни: 14C, 15A, 25A и 25D, с площадью застройки от {N96.60} до {N115.56} {U}, от {E470000} до {E730000}.',
  '4 من أصل 8 بثلاث غرف نوم: 14C و15A و25A و25D، بمساحة مبنية من {N96.60} إلى {N115.56} {U}، من {E470000} إلى {E730000}.',
  '4 van de 8 hebben drie slaapkamers: 14C, 15A, 25A en 25D, met 96,60 tot 115,56 m² bebouwd, van {E470000} tot {E730000}.',
  '4 z 8 mają trzy sypialnie: 14C, 15A, 25A i 25D, o powierzchni zabudowy od 96,60 do 115,56 m², od {E470000} do {E730000}.',
  '4 av de 8 har tre soverom: 14C, 15A, 25A og 25D, med 96,60 til 115,56 m² bebygd areal, fra {E470000} til {E730000}.',
  '4 av de 8 har tre sovrum: 14C, 15A, 25A och 25D, med 96,60 till 115,56 m² byggyta, från {E470000} till {E730000}.')
a('.residences.items[1].points[1]',
  '14C tiene una terraza cubierta de 52,70 m². 15A y 25A, en la quinta planta, tienen terrazas descubiertas de 55,61 y 88,71 m², y la segunda es la mayor terraza de la lista. 25D tiene una terraza cubierta de 28,41 m² y una descubierta de 3,35 m².',
  '14C a une terrasse couverte de 52,70 m². 15A et 25A, au cinquième étage, ont des terrasses découvertes de 55,61 et 88,71 m², et la seconde est la plus grande terrasse de la liste. 25D a une terrasse couverte de 28,41 m² et une terrasse découverte de 3,35 m².',
  '14C hat eine überdachte Terrasse von 52,70 m². 15A und 25A im fünften Obergeschoss haben offene Terrassen von 55,61 und 88,71 m², und die zweite ist die größte Terrasse auf der Liste. 25D hat eine überdachte Terrasse von 28,41 m² und eine offene von 3,35 m².',
  'У 14C крытая терраса {N52.70} {U}. У 15A и 25A, на шестом этаже, открытые террасы {N55.61} и {N88.71} {U}, причём вторая — самая большая терраса в списке. У 25D крытая терраса {N28.41} {U} и открытая {N3.35} {U}.',
  'في 14C تراس مسقوف مساحته {N52.70} {U}. وفي 15A و25A، في الطابق الخامس، تراسان مكشوفان مساحتاهما {N55.61} و{N88.71} {U}، والثاني هو أكبر تراس في القائمة. وفي 25D تراس مسقوف مساحته {N28.41} {U} وآخر مكشوف مساحته {N3.35} {U}.',
  '14C heeft een overdekt terras van 52,70 m². 15A en 25A, op de vijfde verdieping, hebben open terrassen van 55,61 en 88,71 m², en het tweede is het grootste terras op de lijst. 25D heeft een overdekt terras van 28,41 m² en een open terras van 3,35 m².',
  '14C ma taras zadaszony o powierzchni 52,70 m². 15A i 25A, na piątym piętrze, mają tarasy odkryte o powierzchni 55,61 i 88,71 m², a drugi jest największym tarasem na liście. 25D ma taras zadaszony o powierzchni 28,41 m² i odkryty o powierzchni 3,35 m².',
  '14C har en overbygd terrasse på 52,70 m². 15A og 25A, i sjette etasje, har åpne terrasser på 55,61 og 88,71 m², og den andre er den største terrassen på listen. 25D har en overbygd terrasse på 28,41 m² og en åpen på 3,35 m².',
  '14C har en övertäckt terrass på 52,70 m². 15A och 25A, på femte våningen, har öppna terrasser på 55,61 och 88,71 m², och den andra är den största terrassen på listan. 25D har en övertäckt terrass på 28,41 m² och en öppen på 3,35 m².')
a('.residences.items[2].name',
  'Con cada vivienda', 'Avec chaque logement', 'Zu jeder Immobilie', 'К каждому объекту', 'مع كل مسكن', 'Bij elke woning', 'Z każdym lokalem', 'Til hver bolig', 'Till varje bostad')
a('.residences.items[2].points[0]',
  'Una plaza de aparcamiento y un trastero, como indica la lista de precios.',
  'Une place de parking et un débarras, comme l’indique la liste de prix.',
  'Ein Stellplatz und ein Abstellraum, wie die Preisliste angibt.',
  'Одно машиноместо и одна кладовая, как указано в прайс-листе.',
  'موقف سيارة واحد ومخزن واحد، كما تذكر قائمة الأسعار.',
  'Eén parkeerplaats en één berging, zoals de prijslijst vermeldt.',
  'Jedno miejsce postojowe i jedna komórka lokatorska, jak podaje cennik.',
  'Én parkeringsplass og ett bod, slik prislisten oppgir.',
  'En parkeringsplats och ett förråd, som prislistan anger.')
a('.residences.items[2].points[1]',
  'Una cocina equipada con electrodomésticos Bosch o similares y aire acondicionado por conductos de frío y calor, como indica el informe de calidades.',
  'Une cuisine équipée d’appareils Bosch ou équivalents et une climatisation réversible par gaines, comme l’indique le rapport de qualité.',
  'Eine Einbauküche mit Bosch-Geräten oder gleichwertigen und eine Warm- und Kaltluft-Klimatisierung über Kanäle, wie der Qualitätsbericht aufführt.',
  'Кухня с техникой Bosch или аналогичной и канальное кондиционирование на тепло и холод, как указано в отчёте о качестве.',
  'مطبخ مجهّز بأجهزة Bosch أو ما يماثلها وتكييف هواء ساخن وبارد عبر مجارٍ، كما يذكر تقرير الجودة.',
  'Een ingerichte keuken met Bosch-apparaten of gelijkwaardig en kanaalairconditioning voor warme en koude lucht, zoals het kwaliteitsrapport vermeldt.',
  'Wyposażona kuchnia ze sprzętem Bosch lub równoważnym oraz kanałowa klimatyzacja ciepłego i zimnego powietrza, jak wymienia raport jakości.',
  'Et innredet kjøkken med Bosch-apparater eller tilsvarende og kanalbasert klimaanlegg for varm og kald luft, slik kvalitetsrapporten oppgir.',
  'Ett utrustat kök med Bosch-apparater eller likvärdiga och kanalansluten luftkonditionering för varm och kall luft, som kvalitetsrapporten anger.')

# ---- lifestyle and location ---------------------------------------------------------------------

a('.lifestyle.headlineHtml',
  'Una piscina, <em>un gimnasio</em> y aparcamiento para buggies', 'Une piscine, <em>une salle de sport</em> et un parking pour voiturettes', 'Ein Pool, <em>ein Fitnessraum</em> und Parkplätze für Golfbuggys',
  'Бассейн, <em>тренажёрный зал</em> и парковка для гольф-каров', 'مسبح <em>ونادٍ رياضي</em> وموقف لعربات الغولف', 'Een zwembad, <em>een sportschool</em> en parkeerplaats voor golfbuggy’s',
  'Basen, <em>siłownia</em> i parking dla melexów golfowych', 'Et basseng, <em>et treningsrom</em> og parkering for golfbiler', 'En pool, <em>ett gym</em> och parkering för golfbilar')
a('.lifestyle.copy',
  'El informe de calidades y el dossier enumeran las zonas comunes sin superficies, de modo que confirmamos lo que está construido y abierto antes de cualquier reserva.',
  'Le rapport de qualité et le dossier énumèrent les parties communes sans surfaces ; nous confirmons donc ce qui est construit et ouvert avant toute réservation.',
  'Der Qualitätsbericht und das Dossier führen die Gemeinschaftsflächen ohne Größenangaben auf, daher bestätigen wir vor jeder Reservierung, was gebaut und geöffnet ist.',
  'В отчёте о качестве и в досье общие зоны перечислены без площадей, поэтому перед любым бронированием мы подтверждаем, что построено и открыто.',
  'يذكر تقرير الجودة والملف المناطق المشتركة دون مساحات، لذلك نؤكد ما هو مبني ومفتوح قبل أي حجز.',
  'Het kwaliteitsrapport en het dossier noemen de gemeenschappelijke ruimtes zonder oppervlaktes, dus wij bevestigen wat gebouwd en geopend is vóór elke reservering.',
  'Raport jakości i dossier wymieniają części wspólne bez podania powierzchni, dlatego przed każdą rezerwacją potwierdzamy, co jest zbudowane i otwarte.',
  'Kvalitetsrapporten og dossieret oppgir fellesarealene uten størrelser, så vi bekrefter hva som er bygget og åpent før enhver reservasjon.',
  'Kvalitetsrapporten och dossiern anger de gemensamma ytorna utan storlekar, så vi bekräftar vad som är byggt och öppet före varje bokning.')
a('.lifestyle.panels[0][1]',
  'Los documentos enumeran piscinas para adultos con cloración salina en las zonas comunes exteriores y en la cubierta, y el resumen del dossier añade una piscina en una zona de solárium. En las imágenes del promotor, la terraza de la piscina tiene tumbonas y vegetación, con el campo de golf al fondo.',
  'Les documents mentionnent des piscines pour adultes à traitement au sel dans les parties communes extérieures et sur le toit, et le résumé du dossier ajoute une piscine dans un espace solarium. Dans les images du promoteur, la terrasse de la piscine a des transats et de la végétation, avec le parcours de golf au loin.',
  'Die Dokumente führen Salzwasser-Pools für Erwachsene in den Außenbereichen der Gemeinschaftsflächen und auf dem Dach auf, und die Zusammenfassung des Dossiers ergänzt einen Pool in einem Sonnenterrassenbereich. In den Bildern des Bauträgers hat die Poolterrasse Liegen und Bepflanzung, dahinter der Golfplatz.',
  'В документах перечислены бассейны для взрослых с соляной хлоринацией в общих зонах на улице и на крыше, а в сводке досье добавлен бассейн в зоне солярия. На изображениях застройщика на террасе у бассейна стоят шезлонги и посажены растения, а за ней виднеется поле для гольфа.',
  'تذكر المستندات مسابح للبالغين بالتعقيم الملحي في المناطق المشتركة الخارجية وعلى السطح، ويضيف ملخص الملف مسبحًا في منطقة تراس للتشمس. وفي صور المطوّر يضم تراس المسبح كراسيَ للاستلقاء ونباتات، ويظهر خلفه ملعب الغولف.',
  'De documenten noemen zwembaden voor volwassenen met zoutchlorering in de buitenste gemeenschappelijke ruimtes en op het dak, en de samenvatting van het dossier voegt een zwembad in een zonneterrasgedeelte toe. Op de beelden van de ontwikkelaar heeft het zwembadterras ligbedden en beplanting, met de golfbaan erachter.',
  'Dokumenty wymieniają baseny dla dorosłych z chlorowaniem solą w zewnętrznych częściach wspólnych i na dachu, a streszczenie dossier dodaje basen w strefie tarasu słonecznego. Na obrazach dewelopera taras przy basenie ma leżaki i roślinność, a za nim widać pole golfowe.',
  'Dokumentene oppgir saltklorerte bassenger for voksne i de utvendige fellesarealene og på taket, og dossierets sammendrag legger til et basseng i et solterrasseområde. På utbyggerens bilder har bassengterrassen solsenger og beplantning, med golfbanen bak.',
  'Dokumenten anger saltklorerade pooler för vuxna i de utvändiga gemensamma ytorna och på taket, och dossierns sammanfattning lägger till en pool i ett solterrassområde. På exploatörens bilder har poolterrassen solstolar och växtlighet, med golfbanan bakom.')
a('.lifestyle.panels[1][0]',
  'El gimnasio y el club social', 'La salle de sport et le club social', 'Der Fitnessraum und der Social Club', 'Тренажёрный зал и общественный клуб', 'النادي الرياضي والنادي الاجتماعي',
  'De sportschool en de sociale club', 'Siłownia i klub towarzyski', 'Treningsrommet og den sosiale klubben', 'Gymmet och den sociala klubben')
a('.lifestyle.panels[1][1]',
  'Un gimnasio totalmente equipado y un club social que, según el dossier, tiene una zona de coworking. Los documentos no dan superficie ni lista de equipamiento.',
  'Une salle de sport entièrement équipée et un club social qui, selon le dossier, comprend un espace de coworking. Les documents ne donnent ni surface ni liste d’équipements.',
  'Ein voll ausgestatteter Fitnessraum und ein Social Club, der laut Dossier einen Coworking-Bereich hat. Die Dokumente nennen weder eine Größe noch eine Ausstattungsliste.',
  'Полностью оборудованный тренажёрный зал и общественный клуб, в котором, как сказано в досье, есть зона коворкинга. В документах нет ни площади, ни перечня оборудования.',
  'نادٍ رياضي مجهّز بالكامل ونادٍ اجتماعي يضم، بحسب الملف، منطقة عمل مشترك. ولا تذكر المستندات مساحة ولا قائمة بالتجهيزات.',
  'Een volledig uitgeruste sportschool en een sociale club die volgens het dossier een coworkingruimte heeft. De documenten geven geen oppervlakte en geen lijst met apparatuur.',
  'W pełni wyposażona siłownia i klub towarzyski, który według dossier ma strefę coworkingową. Dokumenty nie podają ani powierzchni, ani listy wyposażenia.',
  'Et fullt utstyrt treningsrom og en sosial klubb som ifølge dossieret har et coworking-område. Dokumentene oppgir verken størrelse eller utstyrsliste.',
  'Ett fullt utrustat gym och en social klubb som enligt dossiern har ett coworkingområde. Dokumenten anger varken storlek eller utrustningslista.')
a('.lifestyle.panels[2][1]',
  'Jardines comunes paisajísticos con iluminación y riego automático, como establece el proyecto de urbanización.',
  'Jardins communs paysagers avec éclairage et arrosage automatique, comme le prévoit le projet d’aménagement.',
  'Gestaltete Gemeinschaftsgärten mit Beleuchtung und automatischer Bewässerung, wie es das Erschließungsprojekt vorsieht.',
  'Благоустроенные общие сады с освещением и автоматическим поливом, как предусмотрено проектом благоустройства территории.',
  'حدائق مشتركة منسّقة بإضاءة وري آلي، كما ينص مشروع التهيئة العمرانية.',
  'Aangelegde gemeenschappelijke tuinen met verlichting en automatische bewatering, zoals het urbanisatieproject bepaalt.',
  'Zagospodarowane ogrody wspólne z oświetleniem i automatycznym nawadnianiem, jak przewiduje projekt zagospodarowania terenu.',
  'Opparbeidede fellesbager med belysning og automatisk vanning, slik urbaniseringsprosjektet fastsetter.',
  'Planterade gemensamma trädgårdar med belysning och automatisk bevattning, enligt exploateringsprojektet.')
a('.lifestyle.panels[3][0]',
  'Golf y seguridad', 'Golf et sécurité', 'Golf und Sicherheit', 'Гольф и безопасность', 'الغولف والأمان', 'Golf en veiligheid', 'Golf i bezpieczeństwo', 'Golf og sikkerhet', 'Golf och säkerhet')
a('.lifestyle.panels[3][1]',
  'Aparcamiento para buggies de golf a nivel del campo y, según el dossier, vistas abiertas al green. El complejo es cerrado, con acceso privado, y cada vivienda tiene un trastero con punto de luz.',
  'Parking pour voiturettes de golf au niveau du parcours et, selon le dossier, des vues dégagées sur le green. L’ensemble est fermé, à accès privé, et chaque logement a un débarras avec point lumineux.',
  'Parkplätze für Golfbuggys auf Höhe des Platzes und, laut Dossier, offener Blick auf das Grün. Die Anlage ist abgeschlossen mit privatem Zugang, und jede Immobilie hat einen Abstellraum mit Lichtpunkt.',
  'Парковка для гольф-каров на уровне поля и, как сказано в досье, открытый вид на грин. Комплекс закрытый, с частным въездом, а у каждого объекта есть кладовая со светильником.',
  'موقف لعربات الغولف على مستوى الملعب، وبحسب الملف إطلالات مفتوحة على المساحة الخضراء. والمجمّع مسوَّر بمدخل خاص، ولكل مسكن مخزن بنقطة إضاءة.',
  'Parkeerplaats voor golfbuggy’s op baanniveau en, in de woorden van het dossier, open uitzicht over de green. Het complex is afgesloten met privétoegang en elke woning heeft een berging met lichtpunt.',
  'Parking dla melexów golfowych na poziomie pola i, jak ujmuje to dossier, otwarty widok na green. Kompleks jest zamknięty, z prywatnym wjazdem, a każdy lokal ma komórkę lokatorską z punktem świetlnym.',
  'Parkering for golfbiler på banenivå og, med dossierets ord, åpen utsikt over greenen. Anlegget er lukket med privat adkomst, og hver bolig har et bod med lyspunkt.',
  'Parkering för golfbilar på banans nivå och, med dossiern ord, öppen utsikt över greenen. Området är inhägnat med privat tillfart, och varje bostad har ett förråd med ljuspunkt.')
a('.location.copy',
  'El dossier sitúa el desarrollo dentro del campo de golf de Estepona Golf, en Estepona, con vistas abiertas al green. Los documentos no dan dirección, coordenadas ni distancias, de modo que el mapa muestra la zona de Estepona Golf y aquí no indicamos distancias.',
  'Le dossier situe le programme au sein du parcours de Estepona Golf, à Estepona, avec des vues dégagées sur le green. Les documents ne donnent ni adresse, ni coordonnées, ni distances ; la carte montre donc le secteur de Estepona Golf et nous n’indiquons ici aucune distance.',
  'Das Dossier verortet die Entwicklung innerhalb des Golfplatzes von Estepona Golf in Estepona, mit offenem Blick auf das Grün. Die Dokumente nennen weder Adresse noch Koordinaten noch Entfernungen, daher zeigt die Karte das Gebiet Estepona Golf, und wir geben hier keine Entfernungen an.',
  'В досье проект расположен на территории гольф-поля Estepona Golf в Эстепоне, с открытым видом на грин. В документах нет ни адреса, ни координат, ни расстояний, поэтому на карте показан район Estepona Golf, а расстояния мы здесь не указываем.',
  'يضع الملف المشروع داخل ملعب الغولف في Estepona Golf في إستيبونا، مع إطلالات مفتوحة على المساحة الخضراء. ولا تذكر المستندات عنوانًا ولا إحداثيات ولا مسافات، لذلك تعرض الخريطة منطقة Estepona Golf ولا نذكر هنا أي مسافات.',
  'Het dossier plaatst de ontwikkeling binnen de golfbaan van Estepona Golf, in Estepona, met open uitzicht over de green. De documenten geven geen adres, geen coördinaten en geen afstanden, dus de kaart toont het gebied Estepona Golf en wij vermelden hier geen afstanden.',
  'Dossier umieszcza inwestycję na terenie pola golfowego Estepona Golf w Estepona, z otwartym widokiem na green. Dokumenty nie podają adresu, współrzędnych ani odległości, więc mapa pokazuje okolicę Estepona Golf, a my nie podajemy tu żadnych odległości.',
  'Dossieret plasserer prosjektet innenfor golfbanen i Estepona Golf, i Estepona, med åpen utsikt over greenen. Dokumentene oppgir verken adresse, koordinater eller avstander, så kartet viser området Estepona Golf, og vi oppgir ingen avstander her.',
  'Dossiern placerar projektet inom golfbanan i Estepona Golf, i Estepona, med öppen utsikt över greenen. Dokumenten anger varken adress, koordinater eller avstånd, så kartan visar området Estepona Golf, och vi anger inga avstånd här.')

# ---- investment and trust -----------------------------------------------------------------------

a('.investment.cards[0][1]',
  '8 de las 43 viviendas de la lista tienen precio: cuatro apartamentos de dos dormitorios desde {E325000} hasta {E490000} y cuatro de tres dormitorios desde {E470000} hasta {E730000}, más IVA. Las otras 35 figuran como reservadas.',
  '8 des 43 logements de la liste ont un prix : quatre appartements de deux chambres de {E325000} à {E490000} et quatre de trois chambres de {E470000} à {E730000}, hors TVA. Les 35 autres sont marqués comme réservés.',
  '8 der 43 Immobilien auf der Liste haben einen Preis: vier Wohnungen mit zwei Schlafzimmern von {E325000} bis {E490000} und vier mit drei Schlafzimmern von {E470000} bis {E730000}, zuzüglich MwSt. Die übrigen 35 sind als reserviert gekennzeichnet.',
  'У 8 из 43 объектов списка указана цена: четыре квартиры с двумя спальнями от {E325000} до {E490000} и четыре с тремя спальнями от {E470000} до {E730000} без НДС. Остальные 35 отмечены как зарезервированные.',
  'لدى 8 من أصل 43 مسكنًا في القائمة سعر: أربع شقق بغرفتي نوم من {E325000} إلى {E490000} وأربع شقق بثلاث غرف نوم من {E470000} إلى {E730000}، دون ضريبة القيمة المضافة. أما الـ35 الأخرى فموسومة بأنها محجوزة.',
  '8 van de 43 woningen op de lijst hebben een prijs: vier appartementen met twee slaapkamers van {E325000} tot {E490000} en vier met drie slaapkamers van {E470000} tot {E730000}, excl. btw. De andere 35 zijn gemarkeerd als gereserveerd.',
  '8 z 43 lokali na liście ma cenę: cztery mieszkania z dwiema sypialniami od {E325000} do {E490000} i cztery z trzema sypialniami od {E470000} do {E730000} plus VAT. Pozostałe 35 jest oznaczonych jako zarezerwowane.',
  '8 av de 43 boligene på listen har pris: fire leiligheter med to soverom fra {E325000} til {E490000} og fire med tre soverom fra {E470000} til {E730000}, pluss mva. De øvrige 35 er markert som reservert.',
  '8 av de 43 bostäderna på listan har pris: fyra lägenheter med två sovrum från {E325000} till {E490000} och fyra med tre sovrum från {E470000} till {E730000}, plus IVA. De övriga 35 är markerade som reserverade.')
a('.investment.cards[1][1]',
  'La lista dice que el IVA no está incluido. Con el IVA al 10 por ciento y el impuesto de actos jurídicos documentados al 1,20 por ciento, {E325000} pasan a ser unos {E361000} y {E730000} unos {E812000}, antes de los gastos de notaría y registro.',
  'La liste indique que la TVA n’est pas comprise. Avec la TVA à 10 pour cent et le droit de timbre à 1,20 pour cent, {E325000} deviennent environ {E361000} et {E730000} environ {E812000}, avant les frais de notaire et d’enregistrement.',
  'Die Liste gibt an, dass die MwSt. nicht enthalten ist. Mit 10 Prozent MwSt. und 1,20 Prozent Stempelsteuer werden aus {E325000} etwa {E361000} und aus {E730000} etwa {E812000}, vor Notar- und Grundbuchkosten.',
  'В списке сказано, что НДС не включён. При НДС 10 процентов и гербовом сборе 1,20 процента {E325000} превращаются примерно в {E361000}, а {E730000} — примерно в {E812000}, до расходов на нотариуса и регистрацию.',
  'تذكر القائمة أن ضريبة القيمة المضافة غير مشمولة. وبضريبة قيمة مضافة قدرها 10 بالمئة ورسم دمغة قدره 1.20 بالمئة، يصبح مبلغ {E325000} نحو {E361000} ويصبح {E730000} نحو {E812000}، قبل أتعاب التوثيق والتسجيل.',
  'De lijst geeft aan dat de btw niet is inbegrepen. Met 10 procent btw en 1,20 procent overdrachtsbelasting wordt {E325000} ongeveer {E361000} en {E730000} ongeveer {E812000}, vóór notaris- en kadasterkosten.',
  'Cennik podaje, że VAT nie jest wliczony. Przy VAT 10 procent i podatku od czynności cywilnoprawnych 1,20 procent kwota {E325000} wzrasta do około {E361000}, a {E730000} do około {E812000}, przed opłatami notarialnymi i wpisem do księgi wieczystej.',
  'Listen oppgir at merverdiavgiften ikke er inkludert. Med merverdiavgift på 10 prosent og dokumentavgift på 1,20 prosent blir {E325000} til rundt {E361000} og {E730000} til rundt {E812000}, før notar- og tinglysingsgebyrer.',
  'Listan anger att IVA (spansk moms) inte ingår. Med IVA på 10 procent och stämpelskatt på 1,20 procent blir {E325000} omkring {E361000} och {E730000} omkring {E812000}, före notarie- och registreringsavgifter.')
a('.investment.cards[2][0]',
  'Los pagos siguen a la licencia', 'Les paiements suivent la licence', 'Die Zahlungen folgen der Baugenehmigung', 'Платежи следуют за лицензией', 'الدفعات تتبع الترخيص',
  'De betalingen volgen de vergunning', 'Płatności następują po pozwoleniu', 'Betalingene følger tillatelsen', 'Betalningarna följer licensen')
a('.investment.cards[2][1]',
  'El contrato privado, el 20% + IVA menos la reserva, vence cuando se obtiene la licencia de obras, y siguen dos plazos del 10% + IVA a los 6 y a los 12 meses. Ningún documento da una fecha de licencia, de modo que no podemos decir cuándo vence el primero.',
  'Le contrat privé, 20 % + TVA moins la réservation, est dû à l’obtention du permis de construire, et deux échéances de 10 % + TVA suivent 6 et 12 mois après. Aucun document ne donne de date de permis ; nous ne pouvons donc pas dire quand la première échéance tombe.',
  'Der private Vertrag, 20 % + MwSt. abzüglich der Reservierung, wird fällig, wenn die Baugenehmigung erteilt wird, und zwei Raten von je 10 % + MwSt. folgen 6 und 12 Monate danach. Kein Dokument nennt ein Datum der Genehmigung, daher können wir nicht sagen, wann die erste davon fällig wird.',
  'Частный договор, 20 % + НДС за вычетом бронирования, оплачивается при получении строительной лицензии, а затем через 6 и 12 месяцев следуют два платежа по 10 % + НДС. Ни в одном документе нет даты лицензии, поэтому мы не можем сказать, когда наступит срок первого из них.',
  'يُستحق العقد الخاص، بنسبة 20% + ضريبة القيمة المضافة مطروحًا منها الحجز، عند الحصول على رخصة البناء، وتتبعه دفعتان بنسبة 10% + ضريبة القيمة المضافة بعد 6 أشهر و12 شهرًا منها. ولا يذكر أي مستند تاريخ الرخصة، لذلك لا نستطيع القول متى تُستحق أولاهما.',
  'Het privécontract, 20% + btw min de reservering, is verschuldigd wanneer de bouwvergunning wordt verkregen, en twee termijnen van 10% + btw volgen 6 en 12 maanden daarna. Geen enkel document geeft een vergunningsdatum, dus wij kunnen niet zeggen wanneer de eerste verschuldigd is.',
  'Umowa prywatna, 20% + VAT pomniejszone o rezerwację, jest płatna po uzyskaniu pozwolenia na budowę, a dwie raty po 10% + VAT następują po 6 i 12 miesiącach. Żaden dokument nie podaje daty pozwolenia, więc nie możemy powiedzieć, kiedy upływa termin pierwszej z nich.',
  'Den private kontrakten, 20 % + mva. minus reservasjonen, forfaller når byggetillatelsen er innvilget, og to avdrag på 10 % + mva. følger 6 og 12 måneder etter. Ingen dokumenter oppgir en dato for tillatelsen, så vi kan ikke si når det første forfaller.',
  'Det privata avtalet, 20 % + IVA minus bokningen, förfaller när bygglovet erhålls, och två delbetalningar på 10 % + IVA följer 6 och 12 månader efter det. Inget dokument anger ett datum för bygglovet, så vi kan inte säga när den första förfaller.')
a('.investment.cards[3][1]',
  'La lista dice que sus precios son válidos durante dos días desde su descarga. Reconfirmamos la cifra con el vendedor antes de que usted reserve, y puede haber cambiado para entonces.',
  'La liste indique que ses prix sont valables deux jours après son téléchargement. Nous reconfirmons le chiffre auprès du vendeur avant que vous ne réserviez, et il peut avoir changé d’ici là.',
  'Die Liste gibt an, dass ihre Preise zwei Tage nach dem Herunterladen gültig sind. Wir bestätigen den Betrag beim Verkäufer erneut, bevor Sie reservieren, und er kann sich bis dahin geändert haben.',
  'В списке сказано, что его цены действительны два дня после загрузки. Мы заново подтверждаем сумму у продавца до того, как вы забронируете, и к тому времени она может измениться.',
  'تذكر القائمة أن أسعارها سارية لمدة يومين بعد تنزيلها. نعيد تأكيد المبلغ مع البائع قبل أن تحجز، وقد يكون تغيّر بحلول ذلك الوقت.',
  'De lijst zegt dat de prijzen twee dagen na het downloaden geldig zijn. Wij bevestigen het bedrag opnieuw bij de verkoper voordat u reserveert, en het kan dan veranderd zijn.',
  'Cennik podaje, że jego ceny obowiązują przez dwa dni od pobrania. Kwotę potwierdzamy ponownie ze sprzedawcą przed rezerwacją i do tego czasu może się ona zmienić.',
  'Listen sier at prisene gjelder i to dager etter at den er lastet ned. Vi bekrefter beløpet på nytt med selgeren før reservasjon, og det kan ha endret seg innen da.',
  'Listan anger att priserna gäller i två dagar efter nedladdning. Vi bekräftar beloppet på nytt med säljaren före bokning, och det kan ha ändrats till dess.')

a('.trustDossier.headlineHtml',
  'Lo que <em>comprobamos</em> antes de comprometerse', 'Ce que nous <em>vérifions</em> avant tout engagement', 'Was wir <em>prüfen</em>, bevor Sie sich festlegen',
  'Что мы <em>проверяем</em> до принятия решения', 'ما <em>نتحقق</em> منه قبل أن تلتزم', 'Wat wij <em>controleren</em> voordat u zich vastlegt',
  'Co <em>sprawdzamy</em> przed podjęciem decyzji', 'Hva vi <em>kontrollerer</em> før en forplikter seg', 'Vad vi <em>kontrollerar</em> innan man binder sig')
a('.trustDossier.cards[0][0]',
  'La licencia y las obras', 'Le permis et les travaux', 'Die Baugenehmigung und die Bauarbeiten', 'Лицензия и строительство', 'الترخيص والأعمال',
  'De vergunning en de werken', 'Pozwolenie i roboty budowlane', 'Tillatelsen og byggearbeidene', 'Bygglovet och byggarbetena')
a('.trustDossier.cards[0][1]',
  'Ninguno de los documentos da una fecha de licencia, un estado de las obras o una fecha de entrega, y las condiciones de pago hacen que el contrato privado venza al obtener la licencia de obras. Pedimos por escrito la licencia, el estado de las obras y la fecha de entrega contractual.',
  'Aucun des documents ne donne de date de permis, d’état d’avancement des travaux ni de date de livraison, et les conditions de paiement font tomber le contrat privé à l’obtention du permis de construire. Nous demandons par écrit le permis, l’état des travaux et la date de livraison contractuelle.',
  'Keines der Dokumente nennt ein Datum der Baugenehmigung, einen Baustand oder einen Fertigstellungstermin, und nach den Zahlungsbedingungen wird der private Vertrag mit Erteilung der Baugenehmigung fällig. Wir fordern die Baugenehmigung, den Baustand und den vertraglichen Fertigstellungstermin schriftlich an.',
  'Ни один из документов не называет дату лицензии, стадию строительства или срок сдачи, а по условиям оплаты частный договор оплачивается при получении строительной лицензии. Мы запрашиваем в письменной форме лицензию, стадию строительства и договорной срок сдачи.',
  'لا يذكر أي من المستندات تاريخ ترخيص أو مرحلة الأعمال أو موعد إنجاز، وبحسب شروط الدفع يُستحق العقد الخاص عند الحصول على رخصة البناء. ونطلب كتابةً الرخصة ومرحلة الأعمال وموعد الإنجاز التعاقدي.',
  'Geen van de documenten geeft een vergunningsdatum, een bouwfase of een opleveringsdatum, en volgens de betalingsvoorwaarden is het privécontract verschuldigd bij het verkrijgen van de bouwvergunning. Wij vragen de vergunning, de bouwfase en de contractuele opleveringsdatum schriftelijk op.',
  'Żaden z dokumentów nie podaje daty pozwolenia, etapu robót ani terminu ukończenia, a zgodnie z warunkami płatności umowa prywatna staje się płatna po uzyskaniu pozwolenia na budowę. Pisemnie prosimy o pozwolenie, etap robót i umowny termin ukończenia.',
  'Ingen av dokumentene oppgir en dato for tillatelsen, et byggetrinn eller en ferdigstillelsesdato, og etter betalingsvilkårene forfaller den private kontrakten når byggetillatelsen er innvilget. Vi ber skriftlig om tillatelsen, byggetrinnet og den kontraktsfestede ferdigstillelsesdatoen.',
  'Inget av dokumenten anger ett datum för bygglovet, ett byggstadium eller ett färdigställandedatum, och enligt betalningsvillkoren förfaller det privata avtalet när bygglovet erhålls. Vi begär bygglovet, byggstadiet och det avtalade färdigställandedatumet skriftligen.')
a('.trustDossier.cards[1][1]',
  'La lista de precios y los planos dan superficies distintas para cinco de las ocho viviendas, de modo que la tabla usa las cifras de la lista y la nota que hay debajo da ambas. Preguntamos al vendedor qué cifras van al contrato.',
  'La liste de prix et les plans donnent des surfaces différentes pour cinq des huit logements ; le tableau reprend donc les chiffres de la liste et la note placée dessous donne les deux. Nous demandons au vendeur quels chiffres figureront au contrat.',
  'Die Preisliste und die Pläne nennen für fünf der acht Immobilien unterschiedliche Flächen, daher verwendet die Tabelle die Zahlen der Liste, und die Anmerkung darunter nennt beide. Wir fragen den Verkäufer, welche Zahlen in den Vertrag kommen.',
  'Прайс-лист и планы дают разные площади для пяти из восьми объектов, поэтому в таблице использованы цифры из списка, а в примечании под ней приведены обе. Мы спрашиваем у продавца, какие цифры войдут в договор.',
  'تعطي قائمة الأسعار والمخططات مساحات مختلفة لخمسة من المساكن الثمانية، لذلك يستخدم الجدول أرقام القائمة وتذكر الملاحظة تحته الأرقام الاثنتين. ونسأل البائع عن الأرقام التي ستدخل في العقد.',
  'De prijslijst en de plattegronden geven voor vijf van de acht woningen verschillende oppervlaktes, dus de tabel gebruikt de cijfers van de lijst en de noot eronder geeft beide. Wij vragen de verkoper welke cijfers in het contract komen.',
  'Cennik i plany podają różne powierzchnie dla pięciu z ośmiu lokali, więc tabela używa liczb z cennika, a przypis pod nią podaje obie. Pytamy sprzedawcę, które liczby trafią do umowy.',
  'Prislisten og tegningene oppgir ulike arealer for fem av de åtte boligene, så tabellen bruker listens tall, og merknaden under oppgir begge. Vi spør selgeren hvilke tall som går inn i kontrakten.',
  'Prislistan och ritningarna anger olika ytor för fem av de åtta bostäderna, så tabellen använder listans siffror och anmärkningen under anger båda. Vi frågar säljaren vilka siffror som går in i avtalet.')
a('.trustDossier.cards[2][1]',
  'La lista de precios es del 3 de noviembre de 2026 y el informe de calidades del 14 de abril de 2026. Los planos comerciales llevan la fecha 18 de diciembre de 2025 en sus hojas, aunque su nombre de archivo dice 190826. Usamos la lista para precios y disponibilidad y los demás documentos para describir las viviendas.',
  'La liste de prix date du 3 novembre 2026 et le rapport de qualité du 14 avril 2026. Les plans commerciaux portent la date du 18 décembre 2025 sur leurs feuilles, bien que leur nom de fichier indique 190826. Nous utilisons la liste pour les prix et la disponibilité et les autres documents pour décrire les logements.',
  'Die Preisliste ist vom 3. November 2026 datiert und der Qualitätsbericht vom 14. April 2026. Die Verkaufspläne tragen auf ihren Blättern das Datum 18. Dezember 2025, obwohl ihr Dateiname 190826 lautet. Wir verwenden die Liste für Preise und Verfügbarkeit und die übrigen Dokumente für die Beschreibung der Immobilien.',
  'Прайс-лист датирован 3 ноября 2026 года, а отчёт о качестве — 14 апреля 2026 года. На листах коммерческих планов стоит дата 18 декабря 2025 года, хотя в названии файла указано 190826. Мы используем список для цен и наличия, а остальные документы — для описания жилья.',
  'قائمة الأسعار مؤرخة في 3 نوفمبر 2026 وتقرير الجودة في 14 أبريل 2026. وتحمل المخططات التجارية على أوراقها تاريخ 18 ديسمبر 2025، مع أن اسم ملفها يقول 190826. ونستخدم القائمة للأسعار والتوافر والمستندات الأخرى لوصف المساكن.',
  'De prijslijst is gedateerd 3 november 2026 en het kwaliteitsrapport 14 april 2026. De commerciële plattegronden dragen op hun bladen de datum 18 december 2025, hoewel hun bestandsnaam 190826 luidt. Wij gebruiken de lijst voor prijzen en beschikbaarheid en de andere documenten om de woningen te beschrijven.',
  'Cennik jest datowany na 3 listopada 2026, a raport jakości na 14 kwietnia 2026. Plany sprzedażowe mają na arkuszach datę 18 grudnia 2025, chociaż ich nazwa pliku brzmi 190826. Cennik wykorzystujemy do cen i dostępności, a pozostałe dokumenty do opisu lokali.',
  'Prislisten er datert 3. november 2026 og kvalitetsrapporten 14. april 2026. Salgstegningene har datoen 18. desember 2025 på arkene, selv om filnavnet er 190826. Vi bruker listen til priser og tilgjengelighet og de andre dokumentene til å beskrive boligene.',
  'Prislistan är daterad den 3 november 2026 och kvalitetsrapporten den 14 april 2026. Försäljningsritningarna har datumet 18 december 2025 på sina blad, även om deras filnamn lyder 190826. Vi använder listan för priser och tillgänglighet och de övriga dokumenten för att beskriva bostäderna.')
a('.trustDossier.cards[3][0]',
  'La encimera de la cocina', 'Le plan de travail de la cuisine', 'Die Küchenarbeitsplatte', 'Столешница на кухне', 'سطح عمل المطبخ',
  'Het keukenwerkblad', 'Blat kuchenny', 'Kjøkkenbenkeplaten', 'Köksbänkskivan')
a('.trustDossier.cards[3][1]',
  'El informe de calidades indica una encimera tipo Silestone y el dossier una de tipo porcelánico, ambas según el diseño del proyecto. Preguntamos cuál se instala.',
  'Le rapport de qualité indique un plan de travail de type Silestone et le dossier un plan de type porcelaine, tous deux selon le projet. Nous demandons lequel est posé.',
  'Der Qualitätsbericht nennt eine Arbeitsplatte vom Typ Silestone und das Dossier eine vom Typ Porzellan, beide nach Projektentwurf. Wir fragen, welche eingebaut wird.',
  'В отчёте о качестве указана столешница типа Silestone, а в досье — типа керамогранит, обе по дизайну проекта. Мы спрашиваем, какая устанавливается.',
  'يذكر تقرير الجودة سطح عمل من نوع Silestone ويذكر الملف سطحًا من نوع البورسلين، وكلاهما بحسب تصميم المشروع. ونسأل عن النوع الذي يُركَّب.',
  'Het kwaliteitsrapport noemt een werkblad van het type Silestone en het dossier een van het type porselein, beide volgens het ontwerp van het project. Wij vragen welk wordt geïnstalleerd.',
  'Raport jakości podaje blat typu Silestone, a dossier blat typu porcelana, oba zgodnie z projektem. Pytamy, który zostanie zamontowany.',
  'Kvalitetsrapporten oppgir en benkeplate av typen Silestone og dossieret en av typen porselen, begge etter prosjektets utforming. Vi spør hvilken som monteres.',
  'Kvalitetsrapporten anger en bänkskiva av typen Silestone och dossiern en av typen porslin, båda enligt projektets utformning. Vi frågar vilken som monteras.')
a('.trustDossier.cards[4][1]',
  'El dossier habla de viviendas de uno, dos y tres dormitorios, mientras que las de la lista de precios tienen dos o tres. La lista nombra 43 viviendas y no dice cuántas tiene el desarrollo en total.',
  'Le dossier parle de logements d’une, deux et trois chambres, alors que ceux de la liste de prix ont deux ou trois chambres. La liste nomme 43 logements et ne dit pas combien compte le programme au total.',
  'Das Dossier spricht von Immobilien mit einem, zwei und drei Schlafzimmern, während die auf der Preisliste zwei oder drei haben. Die Liste nennt 43 Immobilien und sagt nicht, wie viele die Entwicklung insgesamt hat.',
  'В досье речь идёт об объектах с одной, двумя и тремя спальнями, тогда как в прайс-листе у них две или три. В списке названы 43 объекта, и не сказано, сколько их в проекте всего.',
  'يتحدث الملف عن مساكن بغرفة وغرفتي وثلاث غرف نوم، بينما لدى مساكن قائمة الأسعار غرفتان أو ثلاث. وتذكر القائمة 43 مسكنًا ولا تقول كم عددها في المشروع كله.',
  'Het dossier spreekt van woningen met een, twee en drie slaapkamers, terwijl die op de prijslijst er twee of drie hebben. De lijst noemt 43 woningen en zegt niet hoeveel de ontwikkeling er in totaal heeft.',
  'Dossier mówi o lokalach z jedną, dwiema i trzema sypialniami, podczas gdy lokale z cennika mają dwie lub trzy. Cennik wymienia 43 lokale i nie podaje, ile ich jest w całej inwestycji.',
  'Dossieret taler om boliger med ett, to og tre soverom, mens boligene på prislisten har to eller tre. Listen nevner 43 boliger og sier ikke hvor mange prosjektet har til sammen.',
  'Dossiern talar om bostäder med ett, två och tre sovrum, medan de på prislistan har två eller tre. Listan nämner 43 bostäder och anger inte hur många projektet har sammanlagt.')

# ---- availability and payment terms -------------------------------------------------------------

a('.availability.headlineHtml',
  '8 de las 43 viviendas listadas <em>disponibles</em>', '8 des 43 logements listés <em>disponibles</em>', '8 der 43 aufgeführten Immobilien <em>verfügbar</em>',
  '8 из 43 объектов списка <em>доступны</em>', '8 من أصل 43 مسكنًا مدرجًا <em>متاحة</em>', '8 van de 43 vermelde woningen <em>beschikbaar</em>',
  '8 z 43 wymienionych lokali <em>dostępnych</em>', '8 av de 43 oppførte boligene <em>tilgjengelige</em>', '8 av de 43 listade bostäderna <em>tillgängliga</em>')
a('.availability.copy',
  'La lista de precios del promotor del 3 de noviembre de 2026 nombra 43 viviendas. Ocho tienen precio y están disponibles, cuatro con dos dormitorios y cuatro con tres; las otras 35 figuran como reservadas. La lista dice que sus precios son válidos durante dos días desde su descarga, de modo que Nueva Living confirma precio y disponibilidad antes de cualquier visita o reserva.',
  'La liste de prix du promoteur du 3 novembre 2026 nomme 43 logements. Huit ont un prix et sont disponibles, quatre de deux chambres et quatre de trois ; les 35 autres sont marqués comme réservés. La liste indique que ses prix sont valables deux jours après son téléchargement ; Nueva Living confirme donc le prix et la disponibilité avant toute visite ou réservation.',
  'Die Preisliste des Bauträgers vom 3. November 2026 nennt 43 Immobilien. Acht haben einen Preis und sind verfügbar, vier mit zwei und vier mit drei Schlafzimmern; die übrigen 35 sind als reserviert gekennzeichnet. Die Liste gibt an, dass ihre Preise zwei Tage nach dem Herunterladen gültig sind, daher bestätigt Nueva Living Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung.',
  'В прайс-листе застройщика от 3 ноября 2026 года названы 43 объекта. У восьми указана цена, и они доступны: четыре с двумя спальнями и четыре с тремя; остальные 35 отмечены как зарезервированные. В списке сказано, что его цены действительны два дня после загрузки, поэтому Nueva Living подтверждает цену и наличие перед любым просмотром или бронированием.',
  'تذكر قائمة أسعار المطوّر بتاريخ 3 نوفمبر 2026 ما مجموعه 43 مسكنًا. لثمانية منها سعر وهي متاحة، أربعة بغرفتي نوم وأربعة بثلاث غرف نوم؛ أما الـ35 الأخرى فموسومة بأنها محجوزة. وتذكر القائمة أن أسعارها سارية لمدة يومين بعد تنزيلها، لذلك تؤكد Nueva Living السعر والتوافر قبل أي معاينة أو حجز.',
  'De prijslijst van de ontwikkelaar van 3 november 2026 noemt 43 woningen. Acht hebben een prijs en zijn beschikbaar, vier met twee en vier met drie slaapkamers; de andere 35 zijn gemarkeerd als gereserveerd. De lijst zegt dat de prijzen twee dagen na het downloaden geldig zijn, dus Nueva Living bevestigt prijs en beschikbaarheid vóór elke bezichtiging of reservering.',
  'Cennik dewelopera z 3 listopada 2026 wymienia 43 lokale. Osiem ma cenę i jest dostępnych, cztery z dwiema i cztery z trzema sypialniami; pozostałe 35 jest oznaczonych jako zarezerwowane. Cennik podaje, że jego ceny obowiązują przez dwa dni od pobrania, więc Nueva Living potwierdza cenę i dostępność przed każdym oglądaniem lub rezerwacją.',
  'Utbyggerens prisliste fra 3. november 2026 nevner 43 boliger. Åtte har pris og er tilgjengelige, fire med to og fire med tre soverom; de øvrige 35 er markert som reservert. Listen sier at prisene gjelder i to dager etter at den er lastet ned, så Nueva Living bekrefter pris og tilgjengelighet før enhver visning eller reservasjon.',
  'Exploatörens prislista från den 3 november 2026 nämner 43 bostäder. Åtta har pris och är tillgängliga, fyra med två och fyra med tre sovrum; de övriga 35 är markerade som reserverade. Listan anger att priserna gäller i två dagar efter nedladdning, så Nueva Living bekräftar pris och tillgänglighet före varje visning eller bokning.')
a('.availability.sourceNote',
  'Los precios, los dormitorios y las superficies están transcritos de la lista de precios del promotor del 3 de noviembre de 2026, que tiene 43 filas: 8 con precio y 35 marcadas como reservadas. Los precios no incluyen IVA y la lista dice que cada vivienda tiene una plaza de aparcamiento y un trastero. La lista da la superficie interior construida, la terraza cubierta, la terraza descubierta y el jardín; la tabla usa sus cifras. Los planos comerciales del promotor, con fecha 18 de diciembre de 2025 en sus hojas, dan otras superficies para cinco de las ocho viviendas. 13H: {N76.35} {U} construidos, {N25.11} {U} de terraza cubierta y {N34.00} {U} de jardín en la lista, {N76.48}, {N24.19} y {N29.96} en el plano. 23C: {N70.96}, {N45.22} y {N51.98} {U} de terraza descubierta en la lista, {N70.82}, {N44.08} y {N47.38} en el plano. 24F: {N75.06} y {N22.25} en la lista, {N75.10} y {N23.25} en el plano. 25A: {N103.11} y {N88.71} en la lista, {N103.13} y {N83.81} en el plano. 25D: {N96.60} en ambos, con {N28.41} de terraza cubierta y {N3.35} de descubierta en la lista, {N3.25} cubierta y {N25.97} descubierta en el plano. 14C y 15A coinciden, y no hay plano de 24C. La planta es la de la columna de plantas de la lista; las hojas de los planos nombran 13H, 24F y 25D con otros números de nivel (P03, P04 y P05). Con el IVA al 10 por ciento y el impuesto de actos jurídicos documentados al 1,20 por ciento, la vivienda de {E325000} cuesta unos {E361000} y la de {E730000} unos {E812000}, antes de los gastos de notaría y registro.',
  'Les prix, les chambres et les surfaces sont transcrits de la liste de prix du promoteur du 3 novembre 2026, qui compte 43 lignes : 8 avec un prix et 35 marquées comme réservées. Les prix excluent la TVA et la liste indique que chaque logement a une place de parking et un débarras. La liste donne la surface intérieure construite, la terrasse couverte, la terrasse découverte et le jardin ; le tableau reprend ses chiffres. Les plans commerciaux du promoteur, datés du 18 décembre 2025 sur leurs feuilles, donnent d’autres surfaces pour cinq des huit logements. 13H : {N76.35} {U} construits, {N25.11} {U} de terrasse couverte et {N34.00} {U} de jardin sur la liste, {N76.48}, {N24.19} et {N29.96} sur le plan. 23C : {N70.96}, {N45.22} et {N51.98} {U} de terrasse découverte sur la liste, {N70.82}, {N44.08} et {N47.38} sur le plan. 24F : {N75.06} et {N22.25} sur la liste, {N75.10} et {N23.25} sur le plan. 25A : {N103.11} et {N88.71} sur la liste, {N103.13} et {N83.81} sur le plan. 25D : {N96.60} sur les deux, avec {N28.41} de terrasse couverte et {N3.35} de découverte sur la liste, {N3.25} couverte et {N25.97} découverte sur le plan. 14C et 15A concordent, et il n’y a pas de plan pour 24C. L’étage est celui de la colonne d’étages de la liste ; les feuilles de plans désignent 13H, 24F et 25D avec d’autres numéros de niveau (P03, P04 et P05). Avec la TVA à 10 pour cent et le droit de timbre à 1,20 pour cent, le logement à {E325000} revient à environ {E361000} et celui à {E730000} à environ {E812000}, avant les frais de notaire et d’enregistrement.',
  'Preise, Schlafzimmer und Flächen sind der Preisliste des Bauträgers vom 3. November 2026 entnommen, die 43 Zeilen hat: 8 mit Preis und 35 als reserviert gekennzeichnet. Die Preise verstehen sich ohne MwSt., und die Liste gibt an, dass zu jeder Immobilie ein Stellplatz und ein Abstellraum gehören. Die Liste nennt die bebaute Innenfläche, die überdachte Terrasse, die offene Terrasse und den Garten; die Tabelle verwendet ihre Zahlen. Die Verkaufspläne des Bauträgers, auf ihren Blättern auf den 18. Dezember 2025 datiert, nennen für fünf der acht Immobilien andere Flächen. 13H: {N76.35} {U} bebaut, {N25.11} {U} überdachte Terrasse und {N34.00} {U} Garten laut Liste, {N76.48}, {N24.19} und {N29.96} laut Plan. 23C: {N70.96}, {N45.22} und {N51.98} {U} offene Terrasse laut Liste, {N70.82}, {N44.08} und {N47.38} laut Plan. 24F: {N75.06} und {N22.25} laut Liste, {N75.10} und {N23.25} laut Plan. 25A: {N103.11} und {N88.71} laut Liste, {N103.13} und {N83.81} laut Plan. 25D: {N96.60} in beiden, mit {N28.41} überdachter und {N3.35} offener Terrasse laut Liste, {N3.25} überdacht und {N25.97} offen laut Plan. 14C und 15A stimmen überein, und für 24C gibt es keinen Plan. Das Geschoss ist das der Geschossspalte der Liste; die Planblätter bezeichnen 13H, 24F und 25D mit anderen Ebenennummern (P03, P04 und P05). Mit 10 Prozent MwSt. und 1,20 Prozent Stempelsteuer kostet die Immobilie zu {E325000} etwa {E361000} und die zu {E730000} etwa {E812000}, vor Notar- und Grundbuchkosten.',
  'Цены, число спален и площади перенесены из прайс-листа застройщика от 3 ноября 2026 года, в котором 43 строки: у 8 указана цена, 35 отмечены как зарезервированные. Цены указаны без НДС, а в списке сказано, что к каждому объекту относятся одно машиноместо и одна кладовая. В списке даны внутренняя застроенная площадь, крытая терраса, открытая терраса и сад; в таблице использованы его цифры. Коммерческие планы застройщика, на листах которых стоит дата 18 декабря 2025 года, дают другие площади для пяти из восьми объектов. 13H: {N76.35} {U} застроенной площади, {N25.11} {U} крытой террасы и {N34.00} {U} сада по списку, {N76.48}, {N24.19} и {N29.96} по плану. 23C: {N70.96}, {N45.22} и {N51.98} {U} открытой террасы по списку, {N70.82}, {N44.08} и {N47.38} по плану. 24F: {N75.06} и {N22.25} по списку, {N75.10} и {N23.25} по плану. 25A: {N103.11} и {N88.71} по списку, {N103.13} и {N83.81} по плану. 25D: {N96.60} в обоих, с {N28.41} крытой и {N3.35} открытой террасы по списку, {N3.25} крытой и {N25.97} открытой по плану. 14C и 15A совпадают, плана для 24C нет. Этаж взят из столбца этажей списка; на листах планов 13H, 24F и 25D обозначены другими номерами уровней (P03, P04 и P05). При НДС 10 процентов и гербовом сборе 1,20 процента объект за {E325000} обходится примерно в {E361000}, а за {E730000} — примерно в {E812000}, до расходов на нотариуса и регистрацию.',
  'الأسعار وعدد غرف النوم والمساحات منقولة من قائمة أسعار المطوّر بتاريخ 3 نوفمبر 2026، وهي تضم 43 صفًا: 8 بسعر و35 موسومة بأنها محجوزة. الأسعار لا تشمل ضريبة القيمة المضافة، وتذكر القائمة أن لكل مسكن موقف سيارة واحدًا ومخزنًا واحدًا. وتعطي القائمة المساحة الداخلية المبنية والتراس المسقوف والتراس المكشوف والحديقة، ويستخدم الجدول أرقامها. أما المخططات التجارية للمطوّر، وعلى أوراقها تاريخ 18 ديسمبر 2025، فتعطي مساحات أخرى لخمسة من المساكن الثمانية. 13H: {N76.35} {U} مبنية و{N25.11} {U} تراس مسقوف و{N34.00} {U} حديقة بحسب القائمة، و{N76.48} و{N24.19} و{N29.96} بحسب المخطط. 23C: {N70.96} و{N45.22} و{N51.98} {U} تراس مكشوف بحسب القائمة، و{N70.82} و{N44.08} و{N47.38} بحسب المخطط. 24F: {N75.06} و{N22.25} بحسب القائمة، و{N75.10} و{N23.25} بحسب المخطط. 25A: {N103.11} و{N88.71} بحسب القائمة، و{N103.13} و{N83.81} بحسب المخطط. 25D: {N96.60} في الاثنين، مع {N28.41} تراس مسقوف و{N3.35} مكشوف بحسب القائمة، و{N3.25} مسقوف و{N25.97} مكشوف بحسب المخطط. 14C و15A متطابقان، ولا يوجد مخطط لـ24C. والطابق هو الوارد في عمود الطوابق في القائمة؛ وتسمّي أوراق المخططات 13H و24F و25D بأرقام مستويات أخرى (P03 وP04 وP05). وبضريبة قيمة مضافة قدرها 10 بالمئة ورسم دمغة قدره 1.20 بالمئة، يكلّف المسكن بسعر {E325000} نحو {E361000} والمسكن بسعر {E730000} نحو {E812000}، قبل أتعاب التوثيق والتسجيل.',
  'De prijzen, slaapkamers en oppervlaktes zijn overgenomen uit de prijslijst van de ontwikkelaar van 3 november 2026, die 43 rijen heeft: 8 met een prijs en 35 gemarkeerd als gereserveerd. De prijzen zijn exclusief btw en de lijst zegt dat bij elke woning één parkeerplaats en één berging horen. De lijst geeft de bebouwde binnenoppervlakte, het overdekte terras, het open terras en de tuin; de tabel gebruikt haar cijfers. De commerciële plattegronden van de ontwikkelaar, op hun bladen gedateerd 18 december 2025, geven voor vijf van de acht woningen andere oppervlaktes. 13H: {N76.35} {U} bebouwd, {N25.11} {U} overdekt terras en {N34.00} {U} tuin volgens de lijst, {N76.48}, {N24.19} en {N29.96} volgens de plattegrond. 23C: {N70.96}, {N45.22} en {N51.98} {U} open terras volgens de lijst, {N70.82}, {N44.08} en {N47.38} volgens de plattegrond. 24F: {N75.06} en {N22.25} volgens de lijst, {N75.10} en {N23.25} volgens de plattegrond. 25A: {N103.11} en {N88.71} volgens de lijst, {N103.13} en {N83.81} volgens de plattegrond. 25D: {N96.60} in beide, met {N28.41} overdekt en {N3.35} open terras volgens de lijst, {N3.25} overdekt en {N25.97} open volgens de plattegrond. 14C en 15A komen overeen, en voor 24C is er geen plattegrond. De verdieping is die uit de verdiepingskolom van de lijst; de plattegrondbladen noemen 13H, 24F en 25D met andere niveaunummers (P03, P04 en P05). Met 10 procent btw en 1,20 procent overdrachtsbelasting kost de woning van {E325000} ongeveer {E361000} en die van {E730000} ongeveer {E812000}, vóór notaris- en kadasterkosten.',
  'Ceny, liczba sypialni i powierzchnie zostały przepisane z cennika dewelopera z 3 listopada 2026, który ma 43 wiersze: 8 z ceną i 35 oznaczonych jako zarezerwowane. Ceny nie zawierają VAT, a cennik podaje, że do każdego lokalu należą jedno miejsce postojowe i jedna komórka lokatorska. Cennik podaje powierzchnię zabudowy wnętrza, taras zadaszony, taras odkryty i ogród; tabela używa jego liczb. Plany sprzedażowe dewelopera, z datą 18 grudnia 2025 na arkuszach, podają inne powierzchnie dla pięciu z ośmiu lokali. 13H: {N76.35} {U} zabudowy, {N25.11} {U} tarasu zadaszonego i {N34.00} {U} ogrodu według cennika, {N76.48}, {N24.19} i {N29.96} według planu. 23C: {N70.96}, {N45.22} i {N51.98} {U} tarasu odkrytego według cennika, {N70.82}, {N44.08} i {N47.38} według planu. 24F: {N75.06} i {N22.25} według cennika, {N75.10} i {N23.25} według planu. 25A: {N103.11} i {N88.71} według cennika, {N103.13} i {N83.81} według planu. 25D: {N96.60} w obu, z {N28.41} tarasu zadaszonego i {N3.35} odkrytego według cennika, {N3.25} zadaszonego i {N25.97} odkrytego według planu. 14C i 15A zgadzają się, a dla 24C nie ma planu. Piętro pochodzi z kolumny pięter w cenniku; arkusze planów oznaczają 13H, 24F i 25D innymi numerami poziomów (P03, P04 i P05). Przy VAT 10 procent i podatku od czynności cywilnoprawnych 1,20 procent lokal za {E325000} kosztuje około {E361000}, a lokal za {E730000} około {E812000}, przed opłatami notarialnymi i wpisem do księgi wieczystej.',
  'Priser, soverom og arealer er hentet fra utbyggerens prisliste fra 3. november 2026, som har 43 rader: 8 med pris og 35 markert som reservert. Prisene er uten mva., og listen sier at hver bolig hører med én parkeringsplass og ett bod. Listen oppgir bebygd innvendig areal, overbygd terrasse, åpen terrasse og hage; tabellen bruker tallene fra den. Utbyggerens salgstegninger, datert 18. desember 2025 på arkene, oppgir andre arealer for fem av de åtte boligene. 13H: {N76.35} {U} bebygd, {N25.11} {U} overbygd terrasse og {N34.00} {U} hage ifølge listen, {N76.48}, {N24.19} og {N29.96} ifølge tegningen. 23C: {N70.96}, {N45.22} og {N51.98} {U} åpen terrasse ifølge listen, {N70.82}, {N44.08} og {N47.38} ifølge tegningen. 24F: {N75.06} og {N22.25} ifølge listen, {N75.10} og {N23.25} ifølge tegningen. 25A: {N103.11} og {N88.71} ifølge listen, {N103.13} og {N83.81} ifølge tegningen. 25D: {N96.60} i begge, med {N28.41} overbygd og {N3.35} åpen terrasse ifølge listen, {N3.25} overbygd og {N25.97} åpen ifølge tegningen. 14C og 15A stemmer overens, og det finnes ingen tegning for 24C. Etasjen er den fra etasjekolonnen i listen; tegningsarkene betegner 13H, 24F og 25D med andre nivånumre (P03, P04 og P05). Med mva. på 10 prosent og dokumentavgift på 1,20 prosent koster boligen til {E325000} rundt {E361000} og den til {E730000} rundt {E812000}, før notar- og tinglysingsgebyrer.',
  'Priser, sovrum och ytor är hämtade från exploatörens prislista från den 3 november 2026, som har 43 rader: 8 med pris och 35 markerade som reserverade. Priserna är exklusive IVA (spansk moms), och listan anger att varje bostad hör till en parkeringsplats och ett förråd. Listan anger den invändiga byggytan, den övertäckta terrassen, den öppna terrassen och trädgården; tabellen använder dess siffror. Exploatörens försäljningsritningar, daterade den 18 december 2025 på bladen, anger andra ytor för fem av de åtta bostäderna. 13H: {N76.35} {U} byggyta, {N25.11} {U} övertäckt terrass och {N34.00} {U} trädgård enligt listan, {N76.48}, {N24.19} och {N29.96} enligt ritningen. 23C: {N70.96}, {N45.22} och {N51.98} {U} öppen terrass enligt listan, {N70.82}, {N44.08} och {N47.38} enligt ritningen. 24F: {N75.06} och {N22.25} enligt listan, {N75.10} och {N23.25} enligt ritningen. 25A: {N103.11} och {N88.71} enligt listan, {N103.13} och {N83.81} enligt ritningen. 25D: {N96.60} i båda, med {N28.41} övertäckt och {N3.35} öppen terrass enligt listan, {N3.25} övertäckt och {N25.97} öppen enligt ritningen. 14C och 15A stämmer överens, och det finns ingen ritning för 24C. Våningen är den i listans våningskolumn; ritningsbladen betecknar 13H, 24F och 25D med andra nivånummer (P03, P04 och P05). Med IVA på 10 procent och stämpelskatt på 1,20 procent kostar bostaden för {E325000} omkring {E361000} och den för {E730000} omkring {E812000}, före notarie- och registreringsavgifter.')

a('.constructionTimeline.points[0].label',
  '{E12000} + IVA', '{E12000} + TVA', '{E12000} + MwSt.', '{E12000} + НДС', '{E12000} + ضريبة القيمة المضافة', '{E12000} + btw', '{E12000} + VAT', '{E12000} + mva.', '{E12000} + IVA')
a('.constructionTimeline.points[3].year',
  '+12 meses', '+12 mois', '+12 Monate', '+12 месяцев', '+12 شهرًا', '+12 maanden', '+12 miesięcy', '+12 måneder', '+12 månader')
a('.constructionTimeline.points[4].year',
  'Escritura', 'Acte notarié', 'Notarielle Urkunde', 'Нотариальный акт', 'سند الملكية', 'Notariële akte', 'Akt notarialny', 'Skjøte', 'Lagfart')
a('.constructionTimeline.paymentTerms[0][2]',
  '{E13200} con IVA', '{E13200} TVA comprise', '{E13200} inkl. MwSt.', '{E13200} с НДС', '{E13200} شاملة ضريبة القيمة المضافة', '{E13200} incl. btw', '{E13200} z VAT', '{E13200} inkl. mva.', '{E13200} inkl. IVA')
a('.constructionTimeline.paymentTerms[1][2]',
  'Vence al obtener la licencia de obras, menos la reserva', 'Dû à l’obtention du permis de construire, moins la réservation', 'Fällig bei Erteilung der Baugenehmigung, abzüglich der Reservierung',
  'Подлежит оплате при получении строительной лицензии, за вычетом бронирования', 'يُستحق عند الحصول على رخصة البناء، مطروحًا منه الحجز', 'Verschuldigd bij het verkrijgen van de bouwvergunning, min de reservering',
  'Płatne po uzyskaniu pozwolenia na budowę, pomniejszone o rezerwację', 'Forfaller når byggetillatelsen er innvilget, minus reservasjonen', 'Förfaller när bygglovet erhålls, minus bokningen')
a('.constructionTimeline.paymentTerms[2][0]',
  'A los 6 meses', 'Après 6 mois', 'Nach 6 Monaten', 'Через 6 месяцев', 'بعد 6 أشهر', 'Na 6 maanden', 'Po 6 miesiącach', 'Etter 6 måneder', 'Efter 6 månader')
a('.constructionTimeline.paymentTerms[3][0]',
  'A los 12 meses', 'Après 12 mois', 'Nach 12 Monaten', 'Через 12 месяцев', 'بعد 12 شهرًا', 'Na 12 maanden', 'Po 12 miesiącach', 'Etter 12 måneder', 'Efter 12 månader')
a('.constructionTimeline.paymentTerms[3][2]',
  'Doce meses después del contrato privado', 'Douze mois après le contrat privé', 'Zwölf Monate nach dem privaten Vertrag', 'Через двенадцать месяцев после частного договора',
  'بعد اثني عشر شهرًا من العقد الخاص', 'Twaalf maanden na het privécontract', 'Dwanaście miesięcy po umowie prywatnej', 'Tolv måneder etter den private kontrakten', 'Tolv månader efter det privata avtalet')
a('.constructionTimeline.paymentTerms[4][2]',
  'Escritura, a la finalización y entrega de llaves', 'Acte notarié, à l’achèvement et à la remise des clés', 'Notarielle Urkunde, bei Fertigstellung und Schlüsselübergabe',
  'Нотариальный акт, по завершении строительства и передаче ключей', 'سند الملكية، عند الإنجاز وتسليم المفاتيح', 'Notariële akte, bij oplevering en overhandiging van de sleutels',
  'Akt notarialny, po ukończeniu i wydaniu kluczy', 'Skjøte, ved ferdigstillelse og nøkkeloverlevering', 'Lagfart, vid färdigställande och nyckelöverlämning')
a('.constructionTimeline.paymentTermsNote',
  'El contrato privado vence al obtener la licencia de obras, no en una fecha fija, y los dos plazos aplazados corren desde la fecha de ese contrato. La hoja de pagos del promotor no lleva fecha y no dice nada de un aval bancario para los pagos a cuenta, de modo que Nueva Living pide por escrito la fecha de la licencia, el aval y las fechas del contrato antes de cualquier reserva.',
  'Le contrat privé est dû à l’obtention du permis de construire, et non à une date fixe, et les deux échéances différées courent à partir de la date de ce contrat. La fiche de paiement du promoteur n’est pas datée et ne dit rien d’une garantie bancaire pour les paiements d’acompte ; Nueva Living demande donc par écrit la date du permis, la garantie et les dates du contrat avant toute réservation.',
  'Der private Vertrag wird mit Erteilung der Baugenehmigung fällig, nicht zu einem festen Datum, und die beiden aufgeschobenen Raten laufen ab dem Datum dieses Vertrags. Das Zahlungsblatt des Bauträgers ist undatiert und sagt nichts über eine Bankgarantie für Anzahlungen, daher fragt Nueva Living vor jeder Reservierung schriftlich nach dem Datum der Genehmigung, der Garantie und den Vertragsdaten.',
  'Частный договор оплачивается при получении строительной лицензии, а не в фиксированную дату, и два отсроченных платежа отсчитываются от даты этого договора. Платёжный лист застройщика не датирован и ничего не говорит о банковской гарантии для авансовых платежей, поэтому Nueva Living до любого бронирования запрашивает в письменной форме дату лицензии, гарантию и даты договора.',
  'يُستحق العقد الخاص عند الحصول على رخصة البناء لا في تاريخ ثابت، وتسري الدفعتان المؤجلتان من تاريخ ذلك العقد. وورقة الدفع الخاصة بالمطوّر غير مؤرخة ولا تقول شيئًا عن ضمان مصرفي للدفعات المقدمة، لذلك تطلب Nueva Living كتابةً تاريخ الرخصة والضمان وتواريخ العقد قبل أي حجز.',
  'Het privécontract is verschuldigd bij het verkrijgen van de bouwvergunning, niet op een vaste datum, en de twee uitgestelde termijnen lopen vanaf de datum van dat contract. Het betalingsblad van de ontwikkelaar is ongedateerd en zegt niets over een bankgarantie voor vooruitbetalingen, dus Nueva Living vraagt vóór elke reservering schriftelijk om de vergunningsdatum, de garantie en de contractdata.',
  'Umowa prywatna staje się płatna po uzyskaniu pozwolenia na budowę, a nie w stałym terminie, a dwie odroczone raty liczone są od daty tej umowy. Arkusz płatności dewelopera nie ma daty i nie wspomina o gwarancji bankowej dla wpłat na poczet ceny, dlatego Nueva Living przed każdą rezerwacją prosi pisemnie o datę pozwolenia, gwarancję i daty umów.',
  'Den private kontrakten forfaller når byggetillatelsen er innvilget, ikke på en fast dato, og de to utsatte avdragene løper fra datoen for den kontrakten. Utbyggerens betalingsark er udatert og sier ingenting om en bankgaranti for forskuddsbetalinger, så Nueva Living ber skriftlig om datoen for tillatelsen, garantien og kontraktsdatoene før enhver reservasjon.',
  'Det privata avtalet förfaller när bygglovet erhålls, inte på ett fast datum, och de två uppskjutna delbetalningarna löper från datumet för det avtalet. Exploatörens betalningsblad är odaterat och säger ingenting om en bankgaranti för förskottsbetalningar, så Nueva Living begär skriftligen datumet för bygglovet, garantin och avtalsdatumen före varje bokning.')

# ---- enquiry, FAQ, SEO --------------------------------------------------------------------------

a('.enquiry.headlineHtml',
  'Pregunte por <em>Estepona Fairway Residences</em>', 'Renseignez-vous sur <em>Estepona Fairway Residences</em>', 'Fragen Sie nach <em>Estepona Fairway Residences</em>', 'Узнайте о <em>Estepona Fairway Residences</em>',
  'استفسر عن <em>Estepona Fairway Residences</em>', 'Vraag naar <em>Estepona Fairway Residences</em>', 'Zapytanie o <em>Estepona Fairway Residences</em>', 'Spør om <em>Estepona Fairway Residences</em>', 'Fråga om <em>Estepona Fairway Residences</em>')
a('.enquiry.message',
  'Hola, Nueva Living, me gustaría recibir información sobre Estepona Fairway Residences.',
  'Bonjour Nueva Living, je souhaiterais des informations sur Estepona Fairway Residences.',
  'Guten Tag Nueva Living, ich möchte Informationen zu Estepona Fairway Residences erhalten.',
  'Здравствуйте, Nueva Living! Хочу получить информацию о Estepona Fairway Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Estepona Fairway Residences.',
  'Goedendag Nueva Living, ik wil graag informatie over Estepona Fairway Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje o Estepona Fairway Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Estepona Fairway Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Estepona Fairway Residences.')
a('.faq[0][1]',
  '8 de las 43 de la lista de precios del promotor del 3 de noviembre de 2026: cuatro apartamentos de dos dormitorios desde {E325000} hasta {E490000} y cuatro apartamentos de tres dormitorios desde {E470000} hasta {E730000}, más IVA. Las otras 35 figuran como reservadas.',
  '8 des 43 de la liste de prix du promoteur du 3 novembre 2026 : quatre appartements de deux chambres de {E325000} à {E490000} et quatre appartements de trois chambres de {E470000} à {E730000}, hors TVA. Les 35 autres sont marqués comme réservés.',
  '8 der 43 auf der Preisliste des Bauträgers vom 3. November 2026: vier Wohnungen mit zwei Schlafzimmern von {E325000} bis {E490000} und vier Wohnungen mit drei Schlafzimmern von {E470000} bis {E730000}, zuzüglich MwSt. Die übrigen 35 sind als reserviert gekennzeichnet.',
  '8 из 43 в прайс-листе застройщика от 3 ноября 2026 года: четыре квартиры с двумя спальнями от {E325000} до {E490000} и четыре квартиры с тремя спальнями от {E470000} до {E730000} без НДС. Остальные 35 отмечены как зарезервированные.',
  '8 من أصل 43 في قائمة أسعار المطوّر بتاريخ 3 نوفمبر 2026: أربع شقق بغرفتي نوم من {E325000} إلى {E490000} وأربع شقق بثلاث غرف نوم من {E470000} إلى {E730000}، دون ضريبة القيمة المضافة. أما الـ35 الأخرى فموسومة بأنها محجوزة.',
  '8 van de 43 op de prijslijst van de ontwikkelaar van 3 november 2026: vier appartementen met twee slaapkamers van {E325000} tot {E490000} en vier appartementen met drie slaapkamers van {E470000} tot {E730000}, excl. btw. De andere 35 zijn gemarkeerd als gereserveerd.',
  '8 z 43 na cenniku dewelopera z 3 listopada 2026: cztery mieszkania z dwiema sypialniami od {E325000} do {E490000} i cztery mieszkania z trzema sypialniami od {E470000} do {E730000} plus VAT. Pozostałe 35 jest oznaczonych jako zarezerwowane.',
  '8 av de 43 på utbyggerens prisliste fra 3. november 2026: fire leiligheter med to soverom fra {E325000} til {E490000} og fire leiligheter med tre soverom fra {E470000} til {E730000}, pluss mva. De øvrige 35 er markert som reservert.',
  '8 av de 43 på exploatörens prislista från den 3 november 2026: fyra lägenheter med två sovrum från {E325000} till {E490000} och fyra lägenheter med tre sovrum från {E470000} till {E730000}, plus IVA. De övriga 35 är markerade som reserverade.')
a('.faq[1][1]',
  'No. La lista dice que el IVA no está incluido. El IVA es del 10 por ciento y el impuesto de actos jurídicos documentados del 1,20 por ciento, y los gastos de notaría y registro se suman. Confirmamos por escrito los impuestos y los costes de la compra.',
  'Non. La liste indique que la TVA n’est pas comprise. La TVA est de 10 pour cent et le droit de timbre de 1,20 pour cent, et les frais de notaire et d’enregistrement s’y ajoutent. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Die Liste gibt an, dass die MwSt. nicht enthalten ist. Die MwSt. beträgt 10 Prozent und die Stempelsteuer 1,20 Prozent, hinzu kommen Notar- und Grundbuchkosten. Wir bestätigen die Steuern und die Kaufnebenkosten schriftlich.',
  'Нет. В списке сказано, что НДС не включён. НДС составляет 10 процентов, гербовый сбор — 1,20 процента, а расходы на нотариуса и регистрацию добавляются сверху. Мы подтверждаем налоги и расходы на покупку в письменной форме.',
  'لا. تذكر القائمة أن ضريبة القيمة المضافة غير مشمولة. وضريبة القيمة المضافة 10 بالمئة ورسم الدمغة 1.20 بالمئة، وتُضاف إليها أتعاب التوثيق والتسجيل. ونؤكد الضرائب وتكاليف الشراء كتابةً.',
  'Nee. De lijst zegt dat de btw niet is inbegrepen. De btw bedraagt 10 procent en de overdrachtsbelasting 1,20 procent, en notaris- en kadasterkosten komen daar bovenop. Wij bevestigen de belastingen en de aankoopkosten schriftelijk.',
  'Nie. Cennik podaje, że VAT nie jest wliczony. VAT wynosi 10 procent, a podatek od czynności cywilnoprawnych 1,20 procent, do tego dochodzą opłaty notarialne i wpis do księgi wieczystej. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Listen oppgir at merverdiavgiften ikke er inkludert. Merverdiavgiften er 10 prosent og dokumentavgiften 1,20 prosent, og notar- og tinglysingsgebyrer kommer i tillegg. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Nej. Listan anger att IVA (spansk moms) inte ingår. IVA är 10 procent och stämpelskatten 1,20 procent, och notarie- och registreringsavgifter tillkommer. Vi bekräftar skatter och köpkostnader skriftligen.')
a('.faq[2][1]',
  'La lista de precios dice que cada vivienda tiene una plaza de aparcamiento y un trastero. No los numera, de modo que confirmamos por escrito que están incluidos en el precio.',
  'La liste de prix indique que chaque logement a une place de parking et un débarras. Elle ne les numérote pas ; nous confirmons donc par écrit qu’ils sont compris dans le prix.',
  'Die Preisliste gibt an, dass zu jeder Immobilie ein Stellplatz und ein Abstellraum gehören. Sie nummeriert sie nicht, daher bestätigen wir schriftlich, dass sie im Preis enthalten sind.',
  'В прайс-листе сказано, что к каждому объекту относятся одно машиноместо и одна кладовая. Они в нём не пронумерованы, поэтому мы письменно подтверждаем, что они включены в цену.',
  'تذكر قائمة الأسعار أن لكل مسكن موقف سيارة واحدًا ومخزنًا واحدًا. ولا ترقّمهما، لذلك نؤكد كتابةً أنهما مشمولان في السعر.',
  'De prijslijst zegt dat bij elke woning één parkeerplaats en één berging horen. Ze nummert ze niet, dus wij bevestigen schriftelijk dat ze in de prijs zijn inbegrepen.',
  'Cennik podaje, że do każdego lokalu należą jedno miejsce postojowe i jedna komórka lokatorska. Nie numeruje ich, więc na piśmie potwierdzamy, że są wliczone w cenę.',
  'Prislisten sier at hver bolig hører med én parkeringsplass og ett bod. Den nummererer dem ikke, så vi bekrefter skriftlig at de er inkludert i prisen.',
  'Prislistan anger att varje bostad hör till en parkeringsplats och ett förråd. Den numrerar dem inte, så vi bekräftar skriftligen att de ingår i priset.')
a('.faq[3][1]',
  '{E12000} + IVA en la reserva ({E13200} con IVA), luego el 20% + IVA en el contrato privado, menos la reserva, el 10% + IVA seis meses después del contrato, el 10% + IVA doce meses después, y el 60% + IVA en la escritura, a la finalización y entrega de llaves. El contrato privado vence al obtener la licencia de obras.',
  '{E12000} + TVA à la réservation ({E13200} TVA comprise), puis 20 % + TVA au contrat privé, moins la réservation, 10 % + TVA six mois après le contrat, 10 % + TVA douze mois après, et 60 % + TVA à l’acte, à l’achèvement et à la remise des clés. Le contrat privé est dû à l’obtention du permis de construire.',
  '{E12000} + MwSt. bei der Reservierung ({E13200} inkl. MwSt.), dann 20 % + MwSt. beim privaten Vertrag, abzüglich der Reservierung, 10 % + MwSt. sechs Monate nach dem Vertrag, 10 % + MwSt. zwölf Monate danach und 60 % + MwSt. bei der Beurkundung, bei Fertigstellung und Schlüsselübergabe. Der private Vertrag wird mit Erteilung der Baugenehmigung fällig.',
  '{E12000} + НДС при бронировании ({E13200} с НДС), затем 20 % + НДС при частном договоре за вычетом бронирования, 10 % + НДС через шесть месяцев после договора, 10 % + НДС через двенадцать месяцев после него и 60 % + НДС при оформлении нотариального акта, по завершении строительства и передаче ключей. Частный договор оплачивается при получении строительной лицензии.',
  '{E12000} + ضريبة القيمة المضافة عند الحجز ({E13200} شاملة ضريبة القيمة المضافة)، ثم 20% + ضريبة القيمة المضافة عند العقد الخاص مطروحًا منها الحجز، و10% + ضريبة القيمة المضافة بعد ستة أشهر من العقد، و10% + ضريبة القيمة المضافة بعد اثني عشر شهرًا منه، و60% + ضريبة القيمة المضافة عند سند الملكية، عند الإنجاز وتسليم المفاتيح. ويُستحق العقد الخاص عند الحصول على رخصة البناء.',
  '{E12000} + btw bij de reservering ({E13200} incl. btw), daarna 20% + btw bij het privécontract, min de reservering, 10% + btw zes maanden na het contract, 10% + btw twaalf maanden erna, en 60% + btw bij de akte, bij oplevering en overhandiging van de sleutels. Het privécontract is verschuldigd bij het verkrijgen van de bouwvergunning.',
  '{E12000} + VAT przy rezerwacji ({E13200} z VAT), potem 20% + VAT przy umowie prywatnej, pomniejszone o rezerwację, 10% + VAT sześć miesięcy po umowie, 10% + VAT dwanaście miesięcy po niej i 60% + VAT przy akcie notarialnym, po ukończeniu i wydaniu kluczy. Umowa prywatna staje się płatna po uzyskaniu pozwolenia na budowę.',
  '{E12000} + mva. ved reservasjon ({E13200} inkl. mva.), deretter 20 % + mva. ved den private kontrakten, minus reservasjonen, 10 % + mva. seks måneder etter kontrakten, 10 % + mva. tolv måneder etter den, og 60 % + mva. ved skjøtet, ved ferdigstillelse og nøkkeloverlevering. Den private kontrakten forfaller når byggetillatelsen er innvilget.',
  '{E12000} + IVA vid bokning ({E13200} inkl. IVA), därefter 20 % + IVA vid det privata avtalet, minus bokningen, 10 % + IVA sex månader efter avtalet, 10 % + IVA tolv månader efter det, och 60 % + IVA vid lagfarten, vid färdigställande och nyckelöverlämning. Det privata avtalet förfaller när bygglovet erhålls.')
a('.faq[4][1]',
  'Ningún documento da una fecha de entrega, una fecha de licencia o el estado de las obras, de modo que esta página dice solo que la finalización está por confirmar. Pedimos la fecha contractual por escrito antes de cualquier reserva.',
  'Aucun document ne donne de date de livraison, de date de permis ni l’état d’avancement des travaux ; cette page dit donc seulement que l’achèvement reste à confirmer. Nous demandons la date contractuelle par écrit avant toute réservation.',
  'Kein Dokument nennt einen Fertigstellungstermin, ein Datum der Baugenehmigung oder den Baustand, daher sagt diese Seite nur, dass die Fertigstellung noch zu bestätigen ist. Wir fordern den vertraglichen Termin vor jeder Reservierung schriftlich an.',
  'Ни один документ не называет срок сдачи, дату лицензии или стадию строительства, поэтому на этой странице сказано лишь, что срок завершения уточняется. Договорной срок мы запрашиваем в письменной форме до любого бронирования.',
  'لا يذكر أي مستند موعد إنجاز أو تاريخ ترخيص أو مرحلة الأعمال، لذلك تقول هذه الصفحة فقط إن الإنجاز قيد التأكيد. ونطلب الموعد التعاقدي كتابةً قبل أي حجز.',
  'Geen enkel document geeft een opleveringsdatum, een vergunningsdatum of de bouwfase, dus deze pagina zegt alleen dat de oplevering nog bevestigd moet worden. Wij vragen de contractuele datum vóór elke reservering schriftelijk op.',
  'Żaden dokument nie podaje terminu ukończenia, daty pozwolenia ani etapu robót, więc ta strona mówi tylko, że ukończenie wymaga potwierdzenia. Umowny termin prosimy podać na piśmie przed każdą rezerwacją.',
  'Ingen dokumenter oppgir en ferdigstillelsesdato, en dato for tillatelsen eller byggetrinnet, så denne siden sier bare at ferdigstillelsen skal bekreftes. Vi ber skriftlig om den kontraktsfestede datoen før enhver reservasjon.',
  'Inget dokument anger ett färdigställandedatum, ett datum för bygglovet eller byggstadiet, så den här sidan säger bara att färdigställandet ska bekräftas. Vi begär det avtalade datumet skriftligen före varje bokning.')
a('.faq[5][0]',
  '¿Dan los planos y la lista de precios las mismas superficies?', 'Les plans et la liste de prix donnent-ils les mêmes surfaces ?', 'Nennen die Pläne und die Preisliste dieselben Flächen?',
  'Совпадают ли площади на планах и в прайс-листе?', 'هل تعطي المخططات وقائمة الأسعار المساحات نفسها؟', 'Geven de plattegronden en de prijslijst dezelfde oppervlaktes?',
  'Czy plany i cennik podają te same powierzchnie?', 'Oppgir tegningene og prislisten de samme arealene?', 'Anger ritningarna och prislistan samma ytor?')
a('.faq[5][1]',
  'No en cinco de las ocho viviendas. La tabla usa las superficies de la lista de precios y la nota que hay debajo da ambos conjuntos. No hay plano de 24C.',
  'Pas pour cinq des huit logements. Le tableau reprend les surfaces de la liste de prix et la note placée dessous donne les deux séries. Il n’y a pas de plan pour 24C.',
  'Nicht bei fünf der acht Immobilien. Die Tabelle verwendet die Flächen der Preisliste, und die Anmerkung darunter nennt beide Angaben. Für 24C gibt es keinen Plan.',
  'Не у пяти из восьми объектов. В таблице использованы площади из прайс-листа, а в примечании под ней приведены оба набора. Плана для 24C нет.',
  'ليس في خمسة من المساكن الثمانية. يستخدم الجدول مساحات قائمة الأسعار وتذكر الملاحظة تحته المجموعتين. ولا يوجد مخطط لـ24C.',
  'Niet bij vijf van de acht woningen. De tabel gebruikt de oppervlaktes van de prijslijst en de noot eronder geeft beide reeksen. Voor 24C is er geen plattegrond.',
  'Nie w przypadku pięciu z ośmiu lokali. Tabela używa powierzchni z cennika, a przypis pod nią podaje oba zestawy. Dla 24C nie ma planu.',
  'Ikke for fem av de åtte boligene. Tabellen bruker arealene fra prislisten, og merknaden under oppgir begge sett. Det finnes ingen tegning for 24C.',
  'Inte för fem av de åtta bostäderna. Tabellen använder ytorna från prislistan och anmärkningen under anger båda uppsättningarna. Det finns ingen ritning för 24C.')
a('.faq[6][1]',
  'No. El mobiliario, la decoración y la vegetación de las imágenes y de los planos no forman parte de la oferta. Las cocinas llevan los electrodomésticos que enumera el informe de calidades.',
  'Non. Le mobilier, la décoration et la végétation des images et des plans ne font pas partie de l’offre. Les cuisines sont livrées avec les appareils que liste le rapport de qualité.',
  'Nein. Möbel, Dekoration und Bepflanzung auf den Bildern und Plänen gehören nicht zum Angebot. Die Küchen werden mit den im Qualitätsbericht aufgeführten Geräten geliefert.',
  'Нет. Мебель, декор и озеленение на изображениях и планах не входят в предложение. Кухни поставляются с техникой, перечисленной в отчёте о качестве.',
  'لا. الأثاث والديكور والنباتات في الصور والمخططات ليست جزءًا من العرض. وتأتي المطابخ مع الأجهزة المذكورة في تقرير الجودة.',
  'Nee. Het meubilair, de inrichting en de beplanting op de beelden en de plattegronden maken geen deel uit van het aanbod. De keukens worden geleverd met de apparatuur uit het kwaliteitsrapport.',
  'Nie. Meble, wystrój i roślinność na obrazach i planach nie wchodzą w zakres oferty. Kuchnie są wyposażone w sprzęt wymieniony w raporcie jakości.',
  'Nei. Møblene, innredningen og beplantningen på bildene og tegningene er ikke en del av tilbudet. Kjøkkenene leveres med apparatene som kvalitetsrapporten oppgir.',
  'Nej. Möblerna, inredningen och växtligheten på bilderna och ritningarna ingår inte i erbjudandet. Köken levereras med de apparater som kvalitetsrapporten anger.')
a('.faq[7][1]',
  'Sí. La lista dice que sus precios son válidos durante dos días desde su descarga. Reconfirmamos el precio antes de que usted reserve.',
  'Oui. La liste indique que ses prix sont valables deux jours après son téléchargement. Nous reconfirmons le prix avant que vous ne réserviez.',
  'Ja. Die Liste gibt an, dass ihre Preise zwei Tage nach dem Herunterladen gültig sind. Wir bestätigen den Preis erneut, bevor Sie reservieren.',
  'Да. В списке сказано, что его цены действительны два дня после загрузки. Мы заново подтверждаем цену до того, как вы забронируете.',
  'نعم. تذكر القائمة أن أسعارها سارية لمدة يومين بعد تنزيلها. نعيد تأكيد السعر قبل أن تحجز.',
  'Ja. De lijst zegt dat de prijzen twee dagen na het downloaden geldig zijn. Wij bevestigen de prijs opnieuw voordat u reserveert.',
  'Tak. Cennik podaje, że jego ceny obowiązują przez dwa dni od pobrania. Cenę potwierdzamy ponownie przed rezerwacją.',
  'Ja. Listen sier at prisene gjelder i to dager etter at den er lastet ned. Vi bekrefter prisen på nytt før reservasjon.',
  'Ja. Listan anger att priserna gäller i två dagar efter nedladdning. Vi bekräftar priset på nytt före bokning.')
a('.seo.title',
  'Estepona Fairway Residences - Apartamentos en Estepona Golf', 'Estepona Fairway Residences - Appartements à Estepona Golf', 'Estepona Fairway Residences - Wohnungen in Estepona Golf',
  'Estepona Fairway Residences - квартиры в Estepona Golf', 'Estepona Fairway Residences - شقق في Estepona Golf', 'Estepona Fairway Residences - Appartementen in Estepona Golf',
  'Estepona Fairway Residences - mieszkania w Estepona Golf', 'Estepona Fairway Residences - leiligheter i Estepona Golf', 'Estepona Fairway Residences - lägenheter i Estepona Golf')
a('.seo.h1',
  'Estepona Fairway Residences: apartamentos en Estepona Golf, Estepona', 'Estepona Fairway Residences : appartements à Estepona Golf, Estepona',
  'Estepona Fairway Residences: Wohnungen in Estepona Golf, Estepona', 'Estepona Fairway Residences: квартиры в Estepona Golf, Эстепона',
  'Estepona Fairway Residences: شقق في Estepona Golf، إستيبونا', 'Estepona Fairway Residences: appartementen in Estepona Golf, Estepona',
  'Estepona Fairway Residences: mieszkania w Estepona Golf, Estepona', 'Estepona Fairway Residences: leiligheter i Estepona Golf, Estepona',
  'Estepona Fairway Residences: lägenheter i Estepona Golf, Estepona')
a('.seo.h1Context',
  'Apartamentos en Estepona Golf, Estepona', 'Appartements à Estepona Golf, Estepona', 'Wohnungen in Estepona Golf, Estepona', 'Квартиры в Estepona Golf, Эстепона',
  'شقق في Estepona Golf، إستيبونا', 'Appartementen in Estepona Golf, Estepona', 'Mieszkania w Estepona Golf, Estepona', 'Leiligheter i Estepona Golf, Estepona', 'Lägenheter i Estepona Golf, Estepona')

# ---- unit sizes (every size line is built from the same parts) -------------------------------------

PARTS = {  # built, covered terrace, open terrace, garden
    'es': ('{v} {U} construidos', '{v} {U} de terraza cubierta', '{v} {U} de terraza descubierta', '{v} {U} de jardín'),
    'fr': ('{v} {U} construits', '{v} {U} de terrasse couverte', '{v} {U} de terrasse découverte', '{v} {U} de jardin'),
    'de': ('{v} {U} bebaut', '{v} {U} überdachte Terrasse', '{v} {U} offene Terrasse', '{v} {U} Garten'),
    'ru': ('{v} {U} застроенной площади', 'крытая терраса {v} {U}', 'открытая терраса {v} {U}', 'сад {v} {U}'),
    'ar': ('{v} {U} مبنية', '{v} {U} تراس مسقوف', '{v} {U} تراس مكشوف', '{v} {U} حديقة'),
    'nl': ('{v} {U} bebouwd', '{v} {U} overdekt terras', '{v} {U} open terras', '{v} {U} tuin'),
    'pl': ('{v} {U} zabudowy', '{v} {U} tarasu zadaszonego', '{v} {U} tarasu odkrytego', '{v} {U} ogrodu'),
    'no': ('{v} {U} bebygd', '{v} {U} overbygd terrasse', '{v} {U} åpen terrasse', '{v} {U} hage'),
    'sv': ('{v} {U} byggyta', '{v} {U} övertäckt terrass', '{v} {U} öppen terrass', '{v} {U} trädgård'),
}
KEYS = ['built', 'covered terrace', 'open terrace', 'garden']
n_size = 0
for u in proj['availability']['units']:
    pieces = [p.strip() for p in u['size'].split(', ')]
    vals = []
    for p in pieces:
        m = re.fullmatch(r'([\d.]+) sqm (built|covered terrace|open terrace|garden)', p)
        assert m, (u['reference'], p)
        vals.append((m.group(2), m.group(1)))
    out = {}
    for l in LOCS:
        sep = '، ' if l == 'ar' else ', '
        out[l] = sep.join(PARTS[l][KEYS.index(k)].replace('{v}', num(v, l)).replace('{U}', UNIT[l]) for k, v in vals)
    assert u['size'] not in T or T[u['size']] == out
    T[u['size']] = out
    n_size += 1
print('sizes', n_size)

json.dump(T, open(f'{SP}/tr_f.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings to', f'{SP}/tr_f.json')
