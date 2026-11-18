# -*- coding: utf-8 -*-
"""Arrebol Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E740000}
money, {N138.95} decimal number, {U} the area unit.
    python3 tools/import/k_arrebol_residences.py <scratch dir>   (writes <dir>/tr_a.json, then run assemble.py)

Wording follows what the siblings already say: Benalmádena as proa-residences and
benalmadena-village-residences spell it (Бенальмадена, بينالمادينا), the tax word the audit wants
(IVA, TVA, MwSt., НДС, ضريبة القيمة المضافة, btw, VAT, mva, IVA with the first Swedish mention glossed
as spansk moms), the unit-size wording of madronal-heights-residences, formal address throughout
(usted, vous, Sie, вы, u, Państwo, ni; du in Norwegian) and a price only ever as an {E...} token
so that it takes the locale's own shape.
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
proj = json.load(open('content/liora-projects/arrebol-residences/project.json'))


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


TAX = ['IVA', 'TVA', 'MwSt.', 'НДС', 'ضريبة القيمة المضافة', 'btw', 'VAT', 'mva', 'IVA']

# ---- name ---------------------------------------------------------------------------------------
same('Arrebol Residences'); same('Arrebol'); same('Arrebol <em>Residences</em>')
same('Arrebol Residences - Benalmádena Costa')

# ---- description, SEO, hero, card ---------------------------------------------------------------
a('.description',
  'Un edificio boutique de dieciséis viviendas de tres y cuatro dormitorios en una ladera de la costa de Benalmádena, a unos 300 metros de la playa de Malibú, con terrazas orientadas al sur, piscina, gimnasio y sauna. Trece están reservadas; quedan tres, desde {E740000} + IVA.',
  'Un immeuble de standing de seize logements de trois et quatre chambres, à flanc de colline sur la côte de Benalmádena, à environ 300 mètres de la plage de Malibú, avec des terrasses orientées au sud, une piscine, une salle de sport et un sauna. Treize sont réservés ; il en reste trois, à partir de {E740000} + TVA.',
  'Ein kleines Wohngebäude mit sechzehn Wohnungen mit drei und vier Schlafzimmern an einem Hang an der Küste von Benalmádena, rund 300 Meter vom Strand von Malibú, mit Südterrassen, Pool, Fitnessraum und Sauna. Dreizehn sind reserviert; drei sind noch frei, ab {E740000} + MwSt.',
  'Камерный дом из шестнадцати квартир с тремя и четырьмя спальнями на склоне холма на побережье Бенальмадены, примерно в 300 метрах от пляжа Малибу, с террасами на юг, бассейном, тренажёрным залом и сауной. Тринадцать забронированы; осталось три, от {E740000} + НДС.',
  'مبنى صغير راقٍ من ستة عشر مسكناً بثلاث وأربع غرف نوم على سفح تلة في ساحل بينالمادينا، على بعد نحو 300 متر من شاطئ ماليبو، مع تراسات جنوبية ومسبح وصالة رياضية وساونا. ثلاثة عشر منها محجوزة؛ وتبقى ثلاثة، ابتداءً من {E740000} + ضريبة القيمة المضافة.',
  'Een kleinschalig gebouw met zestien woningen met drie en vier slaapkamers op een heuvel aan de kust van Benalmádena, op zo’n 300 meter van het strand van Malibú, met terrassen op het zuiden, een zwembad, een fitnessruimte en een sauna. Dertien zijn gereserveerd; er zijn er nog drie, vanaf {E740000} + btw.',
  'Kameralny budynek z szesnastoma mieszkaniami z trzema i czterema sypialniami na zboczu wzgórza na wybrzeżu Benalmádeny, około 300 metrów od plaży Malibú, z tarasami od południa, basenem, siłownią i sauną. Trzynaście jest zarezerwowanych; zostały trzy, od {E740000} + VAT.',
  'Et lite boligbygg med seksten boliger med tre og fire soverom i en åsside ved kysten av Benalmádena, omkring 300 meter fra Malibú-stranden, med sørvendte terrasser, basseng, treningsrom og badstue. Tretten er reservert; tre gjenstår, fra {E740000} + mva.',
  'Ett litet bostadshus med sexton bostäder med tre och fyra sovrum i en sluttning vid kusten i Benalmádena, omkring 300 meter från Malibústranden, med söderterrasser, pool, gym och bastu. Tretton är reserverade; tre återstår, från {E740000} + IVA (spansk moms).')
a('.seoDescription',
  'Dieciséis viviendas en la costa de Benalmádena, a 300 m de la playa: quedan tres, un dúplex y dos áticos, de 3 o 4 dormitorios, desde {E740000} + IVA.',
  'Seize logements sur la côte de Benalmádena, à 300 m de la plage : il en reste trois, un duplex et deux penthouses, 3 ou 4 chambres, dès {E740000} + TVA.',
  'Sechzehn Wohnungen an der Küste von Benalmádena, 300 m vom Strand: drei frei, eine Maisonette und zwei Penthäuser, 3 oder 4 Schlafzimmer, ab {E740000} + MwSt.',
  'Шестнадцать квартир на побережье Бенальмадены, в 300 м от пляжа: осталось три — дуплекс и два пентхауса, 3 или 4 спальни, от {E740000} + НДС.',
  'ستة عشر مسكناً في ساحل بينالمادينا على بعد 300 م من الشاطئ: تبقى ثلاثة، دوبلكس وبنتهاوسان، بثلاث أو أربع غرف نوم، ابتداءً من {E740000} + ضريبة القيمة المضافة.',
  'Zestien woningen aan de kust van Benalmádena, 300 m van het strand: nog drie, een duplex en twee penthouses, 3 of 4 slaapkamers, vanaf {E740000} + btw.',
  'Szesnaście mieszkań na wybrzeżu Benalmádeny, 300 m od plaży: zostały trzy, dwupoziomowe i dwa penthouse’y, 3 lub 4 sypialnie, od {E740000} + VAT.',
  'Seksten boliger ved kysten av Benalmádena, 300 m fra stranden: tre igjen, en toetasjes og to toppleiligheter, 3 eller 4 soverom, fra {E740000} + mva.',
  'Sexton bostäder vid kusten i Benalmádena, 300 m från stranden: tre kvar, en etagelägenhet och två takvåningar, 3 eller 4 sovrum, från {E740000} + IVA.')
a('.twitterDescription',
  'Un edificio boutique en una ladera de la costa de Benalmádena, a unos 300 metros de la playa. Quedan tres viviendas, desde {E740000} + IVA.',
  'Un petit immeuble à flanc de colline sur la côte de Benalmádena, à environ 300 mètres de la plage. Il reste trois logements, à partir de {E740000} + TVA.',
  'Ein kleines Wohngebäude am Hang an der Küste von Benalmádena, rund 300 Meter vom Strand. Noch drei Wohnungen frei, ab {E740000} + MwSt.',
  'Камерный дом на склоне на побережье Бенальмадены, примерно в 300 метрах от пляжа. Осталось три квартиры, от {E740000} + НДС.',
  'مبنى صغير راقٍ على سفح تلة في ساحل بينالمادينا، على بعد نحو 300 متر من الشاطئ. تبقى ثلاثة مساكن، ابتداءً من {E740000} + ضريبة القيمة المضافة.',
  'Een kleinschalig gebouw op een heuvel aan de kust van Benalmádena, op zo’n 300 meter van het strand. Nog drie woningen, vanaf {E740000} + btw.',
  'Kameralny budynek na zboczu na wybrzeżu Benalmádeny, około 300 metrów od plaży. Zostały trzy mieszkania, od {E740000} + VAT.',
  'Et lite boligbygg i en åsside ved kysten av Benalmádena, omkring 300 meter fra stranden. Tre boliger igjen, fra {E740000} + mva.',
  'Ett litet bostadshus i en sluttning vid kusten i Benalmádena, omkring 300 meter från stranden. Tre bostäder kvar, från {E740000} + IVA.')
a('.hero.location', 'Benalmádena Costa', 'Benalmádena Costa', 'Benalmádena Costa', 'Бенальмадена-Коста',
  'بينالمادينا كوستا', 'Benalmádena Costa', 'Benalmádena Costa', 'Benalmádena Costa', 'Benalmádena Costa')
a('.hero.startingPrice', 'Desde {E740000} + IVA', 'À partir de {E740000} + TVA', 'Ab {E740000} + MwSt.', 'От {E740000} + НДС',
  'ابتداءً من {E740000} + ضريبة القيمة المضافة', 'Vanaf {E740000} + btw', 'Od {E740000} + VAT', 'Fra {E740000} + mva', 'Från {E740000} + IVA')
a('.card.meta[0][1]', *[f'{{E740000}} + {t}' for t in TAX])
a('.availability.priceRange', *[f'{{E740000}} - {{E1145000}} + {t}' for t in TAX])
a('.card.description',
  'Un edificio boutique de dieciséis viviendas en una ladera de la costa de Benalmádena, a unos 300 metros de la playa, con piscina, gimnasio y sauna. Quedan tres viviendas.',
  'Un petit immeuble de seize logements à flanc de colline sur la côte de Benalmádena, à environ 300 mètres de la plage, avec piscine, salle de sport et sauna. Il reste trois logements.',
  'Ein kleines Wohngebäude mit sechzehn Wohnungen am Hang an der Küste von Benalmádena, rund 300 Meter vom Strand, mit Pool, Fitnessraum und Sauna. Drei Wohnungen sind noch frei.',
  'Камерный дом из шестнадцати квартир на склоне на побережье Бенальмадены, примерно в 300 метрах от пляжа, с бассейном, тренажёрным залом и сауной. Осталось три квартиры.',
  'مبنى صغير راقٍ من ستة عشر مسكناً على سفح تلة في ساحل بينالمادينا، على بعد نحو 300 متر من الشاطئ، مع مسبح وصالة رياضية وساونا. تبقى ثلاثة مساكن.',
  'Een kleinschalig gebouw met zestien woningen op een heuvel aan de kust van Benalmádena, op zo’n 300 meter van het strand, met zwembad, fitnessruimte en sauna. Er zijn nog drie woningen.',
  'Kameralny budynek z szesnastoma mieszkaniami na zboczu na wybrzeżu Benalmádeny, około 300 metrów od plaży, z basenem, siłownią i sauną. Zostały trzy mieszkania.',
  'Et lite boligbygg med seksten boliger i en åsside ved kysten av Benalmádena, omkring 300 meter fra stranden, med basseng, treningsrom og badstue. Tre boliger gjenstår.',
  'Ett litet bostadshus med sexton bostäder i en sluttning vid kusten i Benalmádena, omkring 300 meter från stranden, med pool, gym och bastu. Tre bostäder återstår.')

# ---- images and media ---------------------------------------------------------------------------
a('.images.hero.alt',
  'El edificio blanco escalonado descendiendo por una ladera arbolada, con el mar al fondo, imagen generada por ordenador',
  'L’immeuble blanc en gradins qui descend une colline boisée, avec la mer au loin, image générée par ordinateur',
  'Das weiße, terrassierte Gebäude an einem bewaldeten Hang, dahinter das Meer, eine computergenerierte Darstellung',
  'Белое террасное здание, спускающееся по лесистому склону, вдали море, компьютерная визуализация',
  'المبنى الأبيض المتدرّج على سفح تلة مشجّرة، والبحر في الأفق، صورة مولَّدة بالحاسوب',
  'Het witte, terrasvormige gebouw op een beboste helling, met de zee erachter, een computergegenereerd beeld',
  'Biały, tarasowy budynek schodzący po zalesionym zboczu, w tle morze, wizualizacja komputerowa',
  'Den hvite, terrasserte bygningen nedover en skogkledd åsside, med havet bak, et datagenerert bilde',
  'Den vita, terrasserade byggnaden nedför en skogsklädd sluttning, med havet bortom, en datorgenererad bild')
a('.images.architecture.alt',
  'Terrazas ajardinadas de planta baja bajo los amplios balcones de las plantas superiores, con el mar al fondo, imagen generada por ordenador',
  'Terrasses plantées du rez-de-chaussée sous les profonds balcons des étages, avec la mer au bout, image générée par ordinateur',
  'Bepflanzte Terrassen im Erdgeschoss unter den tiefen Balkonen der oberen Etagen, am Ende das Meer, eine computergenerierte Darstellung',
  'Озеленённые террасы нижнего этажа под глубокими балконами верхних этажей, вдали море, компьютерная визуализация',
  'تراسات مزروعة في الطابق الأرضي تحت الشرفات العميقة للطوابق العليا، والبحر في نهايتها، صورة مولَّدة بالحاسوب',
  'Beplante terrassen op de begane grond onder de diepe balkons van de bovenverdiepingen, met de zee aan het eind, een computergegenereerd beeld',
  'Obsadzone zielenią tarasy parteru pod głębokimi balkonami wyższych pięter, na końcu morze, wizualizacja komputerowa',
  'Beplantede terrasser i første etasje under de dype balkongene i etasjene over, med havet i enden, et datagenerert bilde',
  'Planterade terrasser på bottenvåningen under de djupa balkongerna på våningarna ovanför, med havet längst bort, en datorgenererad bild')
a('.images.lifestyle.alt',
  'La piscina iluminada al anochecer, con tumbonas dentro del agua y camas balinesas con dosel delante del edificio, imagen generada por ordenador',
  'La piscine éclairée au crépuscule, avec des transats dans l’eau et des lits de repos à baldaquin devant l’immeuble, image générée par ordinateur',
  'Der beleuchtete Pool in der Abenddämmerung, mit Liegen im Wasser und Liegen mit Baldachin vor dem Gebäude, eine computergenerierte Darstellung',
  'Бассейн с подсветкой в сумерках, шезлонги прямо в воде и кровати под балдахином перед зданием, компьютерная визуализация',
  'المسبح مضاءً عند الغسق، مع كراسي استلقاء داخل الماء وأسرّة بمظلات أمام المبنى، صورة مولَّدة بالحاسوب',
  'Het verlichte zwembad bij schemering, met ligstoelen in het water en ligbedden met luifel voor het gebouw, een computergegenereerd beeld',
  'Podświetlony basen o zmierzchu, z leżakami w wodzie i łożami z baldachimem przed budynkiem, wizualizacja komputerowa',
  'Det opplyste bassenget i skumringen, med solsenger i vannet og daybeds med baldakin foran bygningen, et datagenerert bilde',
  'Den upplysta poolen i skymningen, med solstolar i vattnet och dagbäddar med baldakin framför byggnaden, en datorgenererad bild')
a('.images.privateViewing.alt',
  'Un salón de ático que se abre a una terraza con barandilla de vidrio sobre la costa arbolada y el mar, imagen generada por ordenador',
  'Un séjour de penthouse ouvert sur une terrasse à garde-corps vitré, au-dessus de la côte boisée et de la mer, image générée par ordinateur',
  'Ein Penthouse-Wohnzimmer, das sich zu einer Terrasse mit Glasbrüstung über der bewaldeten Küste und dem Meer öffnet, eine computergenerierte Darstellung',
  'Гостиная пентхауса с выходом на террасу со стеклянным ограждением над лесистым побережьем и морем, компьютерная визуализация',
  'صالة بنتهاوس تنفتح على تراس بدرابزين زجاجي يطل على الساحل المشجّر والبحر، صورة مولَّدة بالحاسوب',
  'Een woonkamer van een penthouse die uitkomt op een terras met glazen balustrade boven de beboste kust en de zee, een computergegenereerd beeld',
  'Salon penthouse’u otwarty na taras ze szklaną balustradą nad zalesionym wybrzeżem i morzem, wizualizacja komputerowa',
  'En stue i en toppleilighet som åpner seg mot en terrasse med glassrekkverk over den skogkledde kysten og havet, et datagenerert bilde',
  'Ett vardagsrum i en takvåning som öppnar sig mot en terrass med glasräcke över den skogsklädda kusten och havet, en datorgenererad bild')
a('.media.copy',
  'Vistas generadas por ordenador del edificio, la piscina y los interiores, los planos de las tres viviendas aún disponibles y el plano de la parcela.',
  'Vues générées par ordinateur de l’immeuble, de la piscine et des intérieurs, plans des trois logements encore disponibles et plan de masse.',
  'Computergenerierte Ansichten des Gebäudes, des Pools und der Innenräume, die Grundrisse der drei noch freien Wohnungen und der Lageplan.',
  'Компьютерные визуализации здания, бассейна и интерьеров, планировки трёх оставшихся квартир и генплан участка.',
  'صور مولَّدة بالحاسوب للمبنى والمسبح والتصاميم الداخلية، ومخططات المساكن الثلاثة التي لا تزال متاحة، ومخطط الموقع.',
  'Computergegenereerde beelden van het gebouw, het zwembad en de interieurs, de plattegronden van de drie nog beschikbare woningen en de situatietekening.',
  'Wizualizacje komputerowe budynku, basenu i wnętrz, rzuty trzech wciąż dostępnych mieszkań oraz plan działki.',
  'Datagenererte bilder av bygningen, bassenget og interiørene, plantegningene for de tre boligene som fortsatt er ledige, og situasjonsplanen.',
  'Datorgenererade bilder av byggnaden, poolen och interiörerna, planritningarna för de tre bostäder som fortfarande är lediga och situationsplanen.')
a('.media.note',
  'Todas las imágenes están generadas por ordenador e ilustran el diseño; no son el edificio terminado, y el mobiliario, la decoración y la vegetación que aparecen no forman parte de la oferta. Los planos son los planos comerciales del promotor: el promotor indica que las superficies, medidas y distribución son previstas y pueden cambiar por exigencias técnicas, jurídicas o comerciales, y los nombres de las estancias figuran en español.',
  'Toutes les images sont générées par ordinateur et illustrent le projet ; elles ne montrent pas l’immeuble achevé, et le mobilier, la décoration et la végétation ne font pas partie de l’offre. Les plans sont les plans commerciaux du promoteur : il précise que les surfaces, les cotes et la distribution sont prévisionnelles et peuvent changer pour des raisons techniques, juridiques ou commerciales, et les pièces y sont nommées en espagnol.',
  'Alle Bilder sind computergeneriert und veranschaulichen den Entwurf; sie zeigen nicht das fertige Gebäude, und Möbel, Dekoration und Bepflanzung gehören nicht zum Angebot. Die Grundrisse sind die Verkaufspläne des Bauträgers: Er weist darauf hin, dass Flächen, Maße und Aufteilung vorläufig sind und sich aus technischen, rechtlichen oder kaufmännischen Gründen ändern können; die Räume sind darin auf Spanisch bezeichnet.',
  'Все изображения созданы на компьютере и иллюстрируют проект; это не готовое здание, а мебель, декор и озеленение не входят в предложение. Планировки — это коммерческие планы застройщика: застройщик указывает, что площади, размеры и планировка являются предварительными и могут измениться по техническим, юридическим или коммерческим причинам; помещения на них подписаны по-испански.',
  'جميع الصور مولَّدة بالحاسوب وتوضّح التصميم، وهي ليست المبنى بعد إنجازه، والأثاث والديكور والنباتات الظاهرة فيها ليست جزءاً من العرض. والمخططات هي مخططات البيع الخاصة بالمطوّر، ويذكر المطوّر أن المساحات والمقاسات والتوزيع تقديرية وقد تتغير لأسباب فنية أو قانونية أو تجارية، وأسماء الغرف فيها بالإسبانية.',
  'Alle beelden zijn computergegenereerd en illustreren het ontwerp; ze tonen niet het afgewerkte gebouw, en meubilair, decoratie en beplanting maken geen deel uit van het aanbod. De plattegronden zijn de verkooptekeningen van de ontwikkelaar: volgens de ontwikkelaar zijn oppervlakten, maten en indeling voorlopig en kunnen ze om technische, juridische of commerciële redenen wijzigen, en de ruimten zijn erop in het Spaans benoemd.',
  'Wszystkie obrazy są wizualizacjami komputerowymi i ilustrują projekt; nie przedstawiają gotowego budynku, a meble, wystrój i roślinność nie są częścią oferty. Rzuty to plany sprzedażowe dewelopera: deweloper zaznacza, że powierzchnie, wymiary i układ są wstępne i mogą się zmienić z przyczyn technicznych, prawnych lub handlowych, a nazwy pomieszczeń są na nich po hiszpańsku.',
  'Alle bildene er datagenererte og illustrerer prosjektet; de viser ikke den ferdige bygningen, og møbler, dekor og beplantning er ikke en del av tilbudet. Plantegningene er utbyggerens salgstegninger: utbyggeren oppgir at arealer, mål og planløsning er foreløpige og kan endres av tekniske, juridiske eller kommersielle grunner, og rommene er navngitt på spansk.',
  'Alla bilder är datorgenererade och illustrerar projektet; de visar inte den färdiga byggnaden, och möbler, inredning och växter ingår inte i erbjudandet. Planritningarna är exploatörens försäljningsritningar: exploatören anger att ytor, mått och planlösning är preliminära och kan ändras av tekniska, juridiska eller kommersiella skäl, och rummen är namngivna på spanska.')
a('.media.items[0].caption', 'El edificio en la ladera', 'L’immeuble à flanc de colline', 'Das Gebäude am Hang', 'Здание на склоне',
  'المبنى على سفح التلة', 'Het gebouw op de helling', 'Budynek na zboczu', 'Bygningen i åssiden', 'Byggnaden i sluttningen')
a('.media.items[2].alt',
  'La piscina comunitaria con tumbonas dentro del agua y camas balinesas con dosel, el edificio detrás, imagen generada por ordenador',
  'La piscine commune avec des transats dans l’eau et des lits de repos à baldaquin, l’immeuble derrière, image générée par ordinateur',
  'Der Gemeinschaftspool mit Liegen im Wasser und Liegen mit Baldachin, dahinter das Gebäude, eine computergenerierte Darstellung',
  'Общий бассейн с шезлонгами в воде и кроватями под балдахином, за ним здание, компьютерная визуализация',
  'المسبح المشترك مع كراسي استلقاء داخل الماء وأسرّة بمظلات، والمبنى خلفه، صورة مولَّدة بالحاسوب',
  'Het gemeenschappelijke zwembad met ligstoelen in het water en ligbedden met luifel, het gebouw erachter, een computergegenereerd beeld',
  'Wspólny basen z leżakami w wodzie i łożami z baldachimem, za nim budynek, wizualizacja komputerowa',
  'Fellesbassenget med solsenger i vannet og daybeds med baldakin, bygningen bak, et datagenerert bilde',
  'Den gemensamma poolen med solstolar i vattnet och dagbäddar med baldakin, byggnaden bakom, en datorgenererad bild')
a('.media.items[4].alt',
  'La piscina comunitaria con barandilla de vidrio, camas balinesas con dosel y palmeras, imagen generada por ordenador',
  'La piscine commune avec garde-corps vitré, lits de repos à baldaquin et palmiers, image générée par ordinateur',
  'Der Gemeinschaftspool mit Glasbrüstung, Liegen mit Baldachin und Palmen, eine computergenerierte Darstellung',
  'Общий бассейн со стеклянным ограждением, кроватями под балдахином и пальмами, компьютерная визуализация',
  'المسبح المشترك بدرابزين زجاجي وأسرّة بمظلات ونخيل، صورة مولَّدة بالحاسوب',
  'Het gemeenschappelijke zwembad met glazen balustrade, ligbedden met luifel en palmen, een computergegenereerd beeld',
  'Wspólny basen ze szklaną balustradą, łożami z baldachimem i palmami, wizualizacja komputerowa',
  'Fellesbassenget med glassrekkverk, daybeds med baldakin og palmer, et datagenerert bilde',
  'Den gemensamma poolen med glasräcke, dagbäddar med baldakin och palmer, en datorgenererad bild')
a('.media.items[5].alt',
  'Una cocina exterior con barra y taburetes, y una zona de descanso bajo un toldo vela, imagen generada por ordenador',
  'Une cuisine d’extérieur avec comptoir et tabourets, et un salon sous une voile d’ombrage, image générée par ordinateur',
  'Eine Außenküche mit Bartresen und Hockern und eine Lounge unter einem Sonnensegel, eine computergenerierte Darstellung',
  'Летняя кухня с барной стойкой и табуретами и зона отдыха под тентом-парусом, компьютерная визуализация',
  'مطبخ خارجي بطاولة بار ومقاعد عالية، وجلسة استرخاء تحت مظلة شراعية، صورة مولَّدة بالحاسوب',
  'Een buitenkeuken met bar en krukken, en een lounge onder een schaduwdoek, een computergegenereerd beeld',
  'Kuchnia plenerowa z barem i hokerami oraz strefa wypoczynku pod żaglem przeciwsłonecznym, wizualizacja komputerowa',
  'Et utekjøkken med bardisk og barkrakker, og en loungeplass under et solseil, et datagenerert bilde',
  'Ett utekök med bardisk och barstolar, och en loungeplats under ett solsegel, en datorgenererad bild')
a('.media.items[5].caption', 'La cocina exterior y la zona chill-out', 'La cuisine d’extérieur et l’espace détente',
  'Die Außenküche und die Chill-out-Zone', 'Летняя кухня и зона отдыха', 'المطبخ الخارجي ومنطقة الاسترخاء',
  'De buitenkeuken en de chill-outzone', 'Kuchnia plenerowa i strefa chill-out', 'Utekjøkkenet og chill-out-området',
  'Uteköket och chill-out-ytan')
a('.media.items[6].alt',
  'El gimnasio de los residentes con suelo de madera, máquinas de cardio, pesas y esterillas de yoga, imagen generada por ordenador',
  'La salle de sport des résidents, parquet, appareils de cardio, poids et tapis de yoga, image générée par ordinateur',
  'Der Fitnessraum der Bewohner mit Holzboden, Cardiogeräten, Gewichten und Yogamatten, eine computergenerierte Darstellung',
  'Тренажёрный зал для жильцов с деревянным полом, кардиотренажёрами, весами и ковриками для йоги, компьютерная визуализация',
  'صالة رياضية للسكان بأرضية خشبية وأجهزة كارديو وأوزان وحُصُر يوغا، صورة مولَّدة بالحاسوب',
  'De fitnessruimte voor bewoners met houten vloer, cardiotoestellen, gewichten en yogamatten, een computergegenereerd beeld',
  'Siłownia dla mieszkańców z drewnianą podłogą, sprzętem cardio, ciężarami i matami do jogi, wizualizacja komputerowa',
  'Beboernes treningsrom med tregulv, kondisjonsmaskiner, vekter og yogamatter, et datagenerert bilde',
  'De boendes gym med trägolv, konditionsmaskiner, vikter och yogamattor, en datorgenererad bild')
a('.media.items[7].alt',
  'Una terraza cubierta en esquina con sofás bajos y una mesa de comedor, con vistas sobre jardines hacia el mar, imagen generada por ordenador',
  'Une terrasse couverte d’angle avec des canapés bas et une table à manger, donnant sur des jardins et la mer, image générée par ordinateur',
  'Eine überdachte Eckterrasse mit niedrigen Sofas und einem Esstisch, mit Blick über Gärten zum Meer, eine computergenerierte Darstellung',
  'Угловая крытая терраса с низкими диванами и обеденным столом, с видом на сады и море, компьютерная визуализация',
  'تراس مسقوف في زاوية المبنى بأرائك منخفضة وطاولة طعام، يطل على الحدائق والبحر، صورة مولَّدة بالحاسوب',
  'Een overdekt hoekterras met lage banken en een eettafel, met uitzicht over tuinen naar de zee, een computergegenereerd beeld',
  'Narożny zadaszony taras z niskimi sofami i stołem jadalnianym, z widokiem na ogrody i morze, wizualizacja komputerowa',
  'En overbygd hjørneterrasse med lave sofaer og et spisebord, med utsikt over hager mot havet, et datagenerert bilde',
  'En överbyggd hörnterrass med låga soffor och ett matbord, med utsikt över trädgårdar mot havet, en datorgenererad bild')
a('.media.items[9].alt',
  'Un salón-comedor diáfano con isla de cocina y ventanales al mar, imagen generada por ordenador',
  'Un séjour-salle à manger ouvert avec îlot de cuisine et baies sur la mer, image générée par ordinateur',
  'Ein offener Wohn- und Essbereich mit Kücheninsel und Fenstern zum Meer, eine computergenerierte Darstellung',
  'Открытая гостиная-столовая с кухонным островом и окнами на море, компьютерная визуализация',
  'صالة جلوس وطعام مفتوحة مع جزيرة مطبخ ونوافذ على البحر، صورة مولَّدة بالحاسوب',
  'Een open woon- en eetkamer met kookeiland en ramen op de zee, een computergegenereerd beeld',
  'Otwarty salon z jadalnią, wyspą kuchenną i oknami na morze, wizualizacja komputerowa',
  'En åpen stue og spisestue med kjøkkenøy og vinduer mot havet, et datagenerert bilde',
  'Ett öppet vardagsrum och matrum med köksö och fönster mot havet, en datorgenererad bild')
a('.media.items[10].alt',
  'Una cocina blanca con columnas de madera y una isla, abierta al salón, imagen generada por ordenador',
  'Une cuisine blanche avec colonnes en bois et îlot, ouverte sur le séjour, image générée par ordinateur',
  'Eine weiße Küche mit Hochschränken in Holz und einer Insel, offen zum Wohnzimmer, eine computergenerierte Darstellung',
  'Белая кухня с деревянными колоннами-шкафами и островом, открытая в гостиную, компьютерная визуализация',
  'مطبخ أبيض بخزائن طويلة خشبية وجزيرة، مفتوح على الصالة، صورة مولَّدة بالحاسوب',
  'Een witte keuken met houten hoge kasten en een eiland, open naar de woonkamer, een computergegenereerd beeld',
  'Biała kuchnia z wysokimi drewnianymi zabudowami i wyspą, otwarta na salon, wizualizacja komputerowa',
  'Et hvitt kjøkken med høyskap i tre og en øy, åpent mot stuen, et datagenerert bilde',
  'Ett vitt kök med högskåp i trä och en köksö, öppet mot vardagsrummet, en datorgenererad bild')
a('.media.items[11].alt',
  'Un dormitorio principal con zona de vestidor y un ventanal corredero a una terraza sobre el mar, imagen generada por ordenador',
  'Une chambre principale avec dressing et une baie coulissante sur une terrasse au-dessus de la mer, image générée par ordinateur',
  'Ein Hauptschlafzimmer mit Ankleidebereich und einer Schiebeglaswand zu einer Terrasse über dem Meer, eine computergenerierte Darstellung',
  'Главная спальня с гардеробной зоной и раздвижной стеклянной стеной на террасу над морем, компьютерная визуализация',
  'غرفة نوم رئيسية مع منطقة ملابس وجدار زجاجي منزلق يفتح على تراس يطل على البحر، صورة مولَّدة بالحاسوب',
  'Een grote slaapkamer met inloopgedeelte en een glazen schuifwand naar een terras boven de zee, een computergegenereerd beeld',
  'Główna sypialnia z garderobą i przesuwną szklaną ścianą na taras nad morzem, wizualizacja komputerowa',
  'Et hovedsoverom med garderobedel og en skyvbar glassvegg ut til en terrasse over havet, et datagenerert bilde',
  'Ett huvudsovrum med klädavdelning och en skjutbar glasvägg ut mot en terrass över havet, en datorgenererad bild')
a('.media.items[12].alt',
  'Un dormitorio de dos camas bajo un techo inclinado, con un escritorio bajo una ventana al mar, imagen generada por ordenador',
  'Une chambre à deux lits sous un plafond mansardé, avec un bureau sous une fenêtre sur la mer, image générée par ordinateur',
  'Ein Zweibettzimmer unter einer Dachschräge, mit einem Schreibtisch unter einem Fenster zum Meer, eine computergenerierte Darstellung',
  'Спальня с двумя кроватями под скатным потолком, письменный стол у окна с видом на море, компьютерная визуализация',
  'غرفة نوم بسريرين تحت سقف مائل، مع مكتب أسفل نافذة تطل على البحر، صورة مولَّدة بالحاسوب',
  'Een slaapkamer met twee bedden onder een schuin plafond, met een bureau onder een raam op de zee, een computergegenereerd beeld',
  'Sypialnia z dwoma łóżkami pod skośnym sufitem, z biurkiem pod oknem z widokiem na morze, wizualizacja komputerowa',
  'Et soverom med to senger under skråtak, med et skrivebord under et vindu mot havet, et datagenerert bilde',
  'Ett sovrum med två sängar under snedtak, med ett skrivbord under ett fönster mot havet, en datorgenererad bild')
a('.media.items[12].caption', 'Un dormitorio bajo cubierta', 'Une chambre sous les toits', 'Ein Schlafzimmer unter dem Dach',
  'Спальня под крышей', 'غرفة نوم تحت السقف', 'Een slaapkamer onder het dak', 'Sypialnia pod dachem',
  'Et soverom under taket', 'Ett sovrum under taket')
a('.media.items[13].alt',
  'Un baño en acabado efecto mármol con bañera exenta, ducha a ras de suelo y mueble suspendido, imagen generada por ordenador',
  'Une salle de bains effet marbre avec baignoire îlot, douche à l’italienne et meuble suspendu, image générée par ordinateur',
  'Ein Bad in Marmoroptik mit freistehender Wanne, bodengleicher Dusche und wandhängendem Waschtisch, eine computergenerierte Darstellung',
  'Ванная комната под мрамор с отдельно стоящей ванной, душем без поддона и подвесной тумбой, компьютерная визуализация',
  'حمّام بتشطيب يحاكي الرخام مع حوض استحمام قائم ودُش مفتوح ووحدة مغسلة معلّقة، صورة مولَّدة بالحاسوب',
  'Een badkamer in marmerlook met vrijstaand bad, inloopdouche en zwevend badmeubel, een computergegenereerd beeld',
  'Łazienka w stylu marmuru z wolnostojącą wanną, prysznicem typu walk-in i podwieszaną szafką, wizualizacja komputerowa',
  'Et bad i marmorlook med frittstående badekar, walk-in-dusj og vegghengt servantskap, et datagenerert bilde',
  'Ett badrum i marmorlook med fristående badkar, walk-in-dusch och vägghängd kommod, en datorgenererad bild')
a('.media.items[14].alt', 'Plano de la vivienda 3, niveles 0 y 1', 'Plan du logement 3, niveaux 0 et 1', 'Grundriss der Wohnung 3, Ebenen 0 und 1',
  'Планировка квартиры 3, уровни 0 и 1', 'مخطط المسكن 3، المستويان 0 و1', 'Plattegrond van woning 3, niveaus 0 en 1',
  'Rzut mieszkania 3, poziomy 0 i 1', 'Plantegning av bolig 3, plan 0 og 1', 'Planritning för bostad 3, plan 0 och 1')
a('.media.items[15].alt', 'Plano de la vivienda 13, un ático', 'Plan du logement 13, un penthouse', 'Grundriss der Wohnung 13, ein Penthouse',
  'Планировка квартиры 13, пентхаус', 'مخطط المسكن 13، بنتهاوس', 'Plattegrond van woning 13, een penthouse',
  'Rzut mieszkania 13, penthouse', 'Plantegning av bolig 13, en toppleilighet', 'Planritning för bostad 13, en takvåning')
a('.media.items[16].alt', 'Plano de la vivienda 15, un ático dúplex en dos niveles', 'Plan du logement 15, un penthouse duplex sur deux niveaux',
  'Grundriss der Wohnung 15, ein Maisonette-Penthaus auf zwei Ebenen', 'Планировка квартиры 15, двухуровневый пентхаус',
  'مخطط المسكن 15، بنتهاوس دوبلكس على مستويين', 'Plattegrond van woning 15, een duplex penthouse op twee niveaus',
  'Rzut mieszkania 15, dwupoziomowy penthouse', 'Plantegning av bolig 15, en toppleilighet over to plan',
  'Planritning för bostad 15, en takvåning i två plan')
# Captions for the three plans: the memory holds "Home 3" untranslated from an earlier project.
for n in ('3', '13', '15'):
    put(f'Home {n}', [f'Vivienda {n}', f'Logement {n}', f'Wohnung {n}', f'Квартира {n}', f'المسكن {n}',
                      f'Woning {n}', f'Mieszkanie {n}', f'Bolig {n}', f'Bostad {n}'])
a('.media.items[17].alt',
  'Plano de la parcela con el edificio, la piscina y el edificio wellness en la pendiente',
  'Plan de masse de la parcelle avec l’immeuble, la piscine et le bâtiment bien-être sur la pente',
  'Lageplan des Grundstücks mit dem Gebäude, dem Pool und dem Wellnessgebäude am Hang',
  'Генплан участка со зданием, бассейном и велнес-корпусом на склоне',
  'مخطط قطعة الأرض مع المبنى والمسبح ومبنى العافية على المنحدر',
  'Situatietekening van het perceel met het gebouw, het zwembad en het wellnessgebouw op de helling',
  'Plan działki z budynkiem, basenem i budynkiem wellness na zboczu',
  'Situasjonsplan for tomten med bygningen, bassenget og velværebygget i skråningen',
  'Situationsplan över tomten med byggnaden, poolen och wellnessbyggnaden i sluttningen')
a('.media.items[17].caption', 'Plano de la parcela', 'Plan de masse', 'Lageplan', 'Генплан участка', 'مخطط الموقع',
  'Situatietekening', 'Plan działki', 'Situasjonsplan', 'Situationsplan')

# ---- overview -----------------------------------------------------------------------------------
a('.overview.headlineHtml', 'Dieciséis viviendas, <em>tres aún disponibles</em>', 'Seize logements, <em>trois encore disponibles</em>',
  'Sechzehn Wohnungen, <em>drei noch frei</em>', 'Шестнадцать квартир, <em>три ещё свободны</em>',
  'ستة عشر مسكناً، <em>ثلاثة لا تزال متاحة</em>', 'Zestien woningen, <em>drie nog beschikbaar</em>',
  'Szesnaście mieszkań, <em>trzy wciąż dostępne</em>', 'Seksten boliger, <em>tre fortsatt ledige</em>',
  'Sexton bostäder, <em>tre fortfarande lediga</em>')
a('.overview.copy[0]',
  'Un único edificio escalonado de dieciséis viviendas de tres o cuatro dormitorios en una ladera de la costa de Benalmádena. El folleto del promotor lo sitúa a unos 300 metros de la playa de Malibú y describe amplias terrazas orientadas al sur, y su plano de situación marca la parcela por encima de la carretera de la costa N-340.',
  'Un seul immeuble en gradins de seize logements de trois ou quatre chambres, à flanc de colline sur la côte de Benalmádena. La brochure du promoteur le situe à environ 300 mètres de la plage de Malibú et décrit de grandes terrasses orientées au sud ; son plan de situation place la parcelle au-dessus de la route côtière N-340.',
  'Ein einziges terrassiertes Gebäude mit sechzehn Wohnungen mit drei oder vier Schlafzimmern an einem Hang an der Küste von Benalmádena. Die Broschüre des Bauträgers verortet es rund 300 Meter vom Strand von Malibú und beschreibt große, nach Süden ausgerichtete Terrassen; sein Lageplan zeigt das Grundstück oberhalb der Küstenstraße N-340.',
  'Одно террасное здание из шестнадцати квартир с тремя или четырьмя спальнями на склоне холма на побережье Бенальмадены. В буклете застройщика указано, что оно находится примерно в 300 метрах от пляжа Малибу, и описаны большие террасы на юг; ситуационный план показывает участок выше прибрежной дороги N-340.',
  'مبنى واحد متدرّج من ستة عشر مسكناً بثلاث أو أربع غرف نوم على سفح تلة في ساحل بينالمادينا. ويحدّد كتيّب المطوّر موقعه على بعد نحو 300 متر من شاطئ ماليبو ويصف تراسات واسعة متجهة جنوباً، ويُظهر مخطط الموقع الخاص به قطعة الأرض فوق الطريق الساحلي N-340.',
  'Eén terrasvormig gebouw met zestien woningen met drie of vier slaapkamers op een heuvel aan de kust van Benalmádena. De brochure van de ontwikkelaar situeert het op zo’n 300 meter van het strand van Malibú en beschrijft grote terrassen op het zuiden; de situatiekaart toont het perceel boven de kustweg N-340.',
  'Jeden tarasowy budynek z szesnastoma mieszkaniami z trzema lub czterema sypialniami na zboczu wzgórza na wybrzeżu Benalmádeny. Broszura dewelopera lokalizuje go około 300 metrów od plaży Malibú i opisuje duże tarasy od południa, a plan sytuacyjny pokazuje działkę powyżej nadmorskiej drogi N-340.',
  'Én terrassert bygning med seksten boliger med tre eller fire soverom i en åsside ved kysten av Benalmádena. Utbyggerens brosjyre plasserer den omkring 300 meter fra Malibú-stranden og beskriver store, sørvendte terrasser, og situasjonskartet viser tomten ovenfor kystveien N-340.',
  'En enda terrasserad byggnad med sexton bostäder med tre eller fyra sovrum i en sluttning vid kusten i Benalmádena. Exploatörens broschyr placerar den omkring 300 meter från Malibústranden och beskriver stora, söderläge terrasser, och lägesplanen visar tomten ovanför kustvägen N-340.')
a('.overview.copy[1]',
  'La lista de precios del 27 de octubre de 2026 muestra trece de las dieciséis viviendas reservadas. Quedan tres: una vivienda de tres dormitorios en dos niveles por {E740000}, un ático de tres dormitorios por {E1040000} y un ático dúplex de cuatro dormitorios por {E1145000}, todos más IVA, cada uno con dos plazas de garaje y un trastero.',
  'La liste de prix du 27 octobre 2026 indique treize des seize logements réservés. Il en reste trois : un logement de trois chambres sur deux niveaux à {E740000}, un penthouse de trois chambres à {E1040000} et un penthouse duplex de quatre chambres à {E1145000}, tous hors TVA, chacun avec deux places de parking et une cave.',
  'Die Preisliste vom 27. Oktober 2026 weist dreizehn der sechzehn Wohnungen als reserviert aus. Drei sind noch frei: eine Wohnung mit drei Schlafzimmern auf zwei Ebenen für {E740000}, ein Penthouse mit drei Schlafzimmern für {E1040000} und ein Maisonette-Penthaus mit vier Schlafzimmern für {E1145000}, jeweils zuzüglich MwSt., jede mit zwei Stellplätzen und einem Abstellraum.',
  'В прайс-листе от 27 октября 2026 года тринадцать из шестнадцати квартир отмечены как забронированные. Осталось три: квартира с тремя спальнями на двух уровнях за {E740000}, пентхаус с тремя спальнями за {E1040000} и двухуровневый пентхаус с четырьмя спальнями за {E1145000}, все без НДС, каждая с двумя машино-местами и кладовой.',
  'تُظهر قائمة الأسعار المؤرخة 27 أكتوبر 2026 أن ثلاثة عشر من المساكن الستة عشر محجوزة. وتبقى ثلاثة: مسكن بثلاث غرف نوم على مستويين بسعر {E740000}، وبنتهاوس بثلاث غرف نوم بسعر {E1040000}، وبنتهاوس دوبلكس بأربع غرف نوم بسعر {E1145000}، وكلها دون ضريبة القيمة المضافة، ولكل منها موقفا سيارات ومخزن.',
  'De prijslijst van 27 oktober 2026 toont dertien van de zestien woningen als gereserveerd. Er zijn er nog drie: een woning met drie slaapkamers op twee niveaus voor {E740000}, een penthouse met drie slaapkamers voor {E1040000} en een duplex penthouse met vier slaapkamers voor {E1145000}, alle excl. btw, elk met twee parkeerplaatsen en een berging.',
  'Cennik z 27 października 2026 r. pokazuje trzynaście z szesnastu mieszkań jako zarezerwowane. Zostały trzy: mieszkanie z trzema sypialniami na dwóch poziomach za {E740000}, penthouse z trzema sypialniami za {E1040000} i dwupoziomowy penthouse z czterema sypialniami za {E1145000}, wszystkie plus VAT, każde z dwoma miejscami parkingowymi i komórką lokatorską.',
  'Prislisten datert 27. oktober 2026 viser tretten av de seksten boligene som reservert. Tre gjenstår: en bolig med tre soverom over to plan til {E740000}, en toppleilighet med tre soverom til {E1040000} og en toppleilighet over to plan med fire soverom til {E1145000}, alle pluss mva, hver med to parkeringsplasser og en bod.',
  'Prislistan daterad 27 oktober 2026 visar tretton av de sexton bostäderna som reserverade. Tre återstår: en bostad med tre sovrum i två plan för {E740000}, en takvåning med tre sovrum för {E1040000} och en takvåning i två plan med fyra sovrum för {E1145000}, samtliga plus IVA, var och en med två parkeringsplatser och ett förråd.')
a('.overview.copy[2]',
  'Los residentes comparten una piscina de cloración salina con pared de vidrio, una cocina exterior con barbacoa y zona chill-out, un gimnasio y una sauna finlandesa con vestuario. El portal del promotor indica la licencia de obra como concedida, el inicio de las obras en junio de 2025 y la entrega en el tercer trimestre de 2027.',
  'Les résidents partagent une piscine à électrolyse au sel avec paroi vitrée, une cuisine d’extérieur avec barbecue et espace détente, une salle de sport et un sauna finlandais avec vestiaire. Le portail du promoteur indique le permis de construire comme accordé, le début des travaux en juin 2025 et la livraison au troisième trimestre 2027.',
  'Die Bewohner teilen sich einen Salzwasserpool mit Glaswand, eine Außenküche mit Grill und Chill-out-Zone, einen Fitnessraum und eine finnische Sauna mit Umkleide. Das Portal des Bauträgers nennt die Baugenehmigung als erteilt, den Baubeginn im Juni 2025 und die Fertigstellung im dritten Quartal 2027.',
  'Жильцы пользуются бассейном с солевой системой очистки и стеклянной стенкой, летней кухней с барбекю и зоной отдыха, тренажёрным залом и финской сауной с раздевалкой. На портале застройщика указано, что разрешение на строительство получено, работы начались в июне 2025 года, а завершение запланировано на третий квартал 2027 года.',
  'يتشارك السكان مسبحاً يعمل بالتعقيم الملحي بجدار زجاجي، ومطبخاً خارجياً مع شواء ومنطقة استرخاء، وصالة رياضية، وساونا فنلندية مع غرفة تبديل ملابس. ويذكر بوابة المطوّر أن رخصة البناء ممنوحة، وأن الأعمال بدأت في يونيو 2025، وأن الإنجاز في الربع الثالث من عام 2027.',
  'Bewoners delen een zoutwaterzwembad met glazen wand, een buitenkeuken met barbecue en chill-outzone, een fitnessruimte en een Finse sauna met kleedruimte. Het portaal van de ontwikkelaar vermeldt de bouwvergunning als verleend, de start van de bouw in juni 2025 en de oplevering in het derde kwartaal van 2027.',
  'Mieszkańcy dzielą basen z chlorowaniem solnym i szklaną ścianą, kuchnię plenerową z grillem i strefą chill-out, siłownię oraz fińską saunę z przebieralnią. Portal dewelopera podaje, że pozwolenie na budowę zostało wydane, budowa ruszyła w czerwcu 2025 r., a zakończenie planowane jest na trzeci kwartał 2027 r.',
  'Beboerne deler et saltvannsbasseng med glassvegg, et utekjøkken med grill og chill-out-område, et treningsrom og en finsk badstue med garderobe. Utbyggerens portal oppgir byggetillatelsen som gitt, byggestart i juni 2025 og ferdigstillelse i tredje kvartal 2027.',
  'De boende delar en saltvattenpool med glasvägg, ett utekök med grill och chill-out-yta, ett gym och en finsk bastu med omklädningsrum. Exploatörens portal anger bygglovet som beviljat, byggstarten i juni 2025 och färdigställandet till tredje kvartalet 2027.')
a('.overview.metrics[3][1]', *[f'{{E740000}} - {{E1145000}} + {t}' for t in TAX])

# ---- residences ---------------------------------------------------------------------------------
a('.residences.headlineHtml', 'Un dúplex <em>y dos áticos</em>', 'Un duplex <em>et deux penthouses</em>',
  'Eine Maisonette <em>und zwei Penthäuser</em>', 'Дуплекс <em>и два пентхауса</em>', 'دوبلكس <em>وبنتهاوسان</em>',
  'Een duplex <em>en twee penthouses</em>', 'Mieszkanie dwupoziomowe <em>i dwa penthouse’y</em>',
  'En toetasjes bolig <em>og to toppleiligheter</em>', 'En etagebostad <em>och två takvåningar</em>')
a('.residences.copy',
  'Las tres viviendas aún disponibles difieren en distribución y nivel. Cada una figura en la lista de precios con dos plazas de garaje y un trastero.',
  'Les trois logements encore disponibles diffèrent par leur plan et leur niveau. Chacun figure sur la liste de prix avec deux places de parking et une cave.',
  'Die drei noch freien Wohnungen unterscheiden sich in Grundriss und Ebene. Jede ist in der Preisliste mit zwei Stellplätzen und einem Abstellraum aufgeführt.',
  'Три оставшиеся квартиры различаются планировкой и уровнем. Каждая указана в прайс-листе с двумя машино-местами и кладовой.',
  'تختلف المساكن الثلاثة التي لا تزال متاحة في التوزيع والمستوى. ويرد كل منها في قائمة الأسعار مع موقفَي سيارات ومخزن.',
  'De drie nog beschikbare woningen verschillen in indeling en niveau. Elk staat op de prijslijst met twee parkeerplaatsen en een berging.',
  'Trzy wciąż dostępne mieszkania różnią się układem i poziomem. Każde figuruje w cenniku z dwoma miejscami parkingowymi i komórką lokatorską.',
  'Hver av de tre boligene som fortsatt er ledige, har sin egen planløsning og etasje. Hver står på prislisten med to parkeringsplasser og en bod.',
  'De tre bostäder som fortfarande är lediga skiljer sig åt i planlösning och plan. Var och en står i prislistan med två parkeringsplatser och ett förråd.')
a('.residences.items[0].name', 'Vivienda 3, en dos niveles', 'Logement 3, sur deux niveaux', 'Wohnung 3, auf zwei Ebenen',
  'Квартира 3, на двух уровнях', 'المسكن 3، على مستويين', 'Woning 3, op twee niveaus', 'Mieszkanie 3, na dwóch poziomach',
  'Bolig 3, over to plan', 'Bostad 3, i två plan')
a('.residences.items[0].points[0]',
  'Salón, comedor y cocina en una sola estancia de {N40.00} {U} en el nivel 1, con un dormitorio, un baño y una terraza cubierta junto a otra descubierta; debajo, en el nivel 0, una sala de estar, un dormitorio, un despacho, dos baños, un lavadero y una terraza con jardinera.',
  'Séjour, salle à manger et cuisine en une seule pièce de {N40.00} {U} au niveau 1, avec une chambre, une salle de bains et une terrasse couverte à côté d’une terrasse découverte ; en dessous, au niveau 0, un salon, une chambre, un bureau, deux salles de bains, une buanderie et une terrasse avec jardinière.',
  'Wohnzimmer, Essbereich und Küche als ein Raum von {N40.00} {U} auf Ebene 1, mit einem Schlafzimmer, einem Bad und einer überdachten neben einer offenen Terrasse; darunter, auf Ebene 0, ein Wohnraum, ein Schlafzimmer, ein Arbeitszimmer, zwei Bäder, ein Hauswirtschaftsraum und eine Terrasse mit Pflanzbeet.',
  'Гостиная, столовая и кухня в одном помещении площадью {N40.00} {U} на уровне 1, со спальней, ванной и крытой террасой рядом с открытой; ниже, на уровне 0, — гостиная, спальня, кабинет, две ванные, постирочная и терраса с клумбой.',
  'الصالة وغرفة الطعام والمطبخ في غرفة واحدة مساحتها {N40.00} {U} في المستوى 1، مع غرفة نوم وحمّام وتراس مسقوف بجوار آخر مكشوف؛ وفي الأسفل، في المستوى 0، غرفة جلوس وغرفة نوم ومكتب وحمّامان وغرفة غسيل وتراس مع حوض زراعة.',
  'Woonkamer, eethoek en keuken als één ruimte van {N40.00} {U} op niveau 1, met een slaapkamer, een badkamer en een overdekt terras naast een open terras; daaronder, op niveau 0, een zitkamer, een slaapkamer, een werkkamer, twee badkamers, een wasruimte en een terras met plantenbak.',
  'Salon, jadalnia i kuchnia w jednym pomieszczeniu o powierzchni {N40.00} {U} na poziomie 1, z sypialnią, łazienką i zadaszonym tarasem obok otwartego; niżej, na poziomie 0, pokój dzienny, sypialnia, gabinet, dwie łazienki, pralnia i taras z donicą.',
  'Stue, spiseplass og kjøkken i ett rom på {N40.00} {U} på plan 1, med et soverom, et bad og en overbygd terrasse ved siden av en åpen; under, på plan 0, en stue, et soverom, et kontor, to bad, en vaskerom og en terrasse med plantekasse.',
  'Vardagsrum, matplats och kök i ett rum på {N40.00} {U} på plan 1, med ett sovrum, ett badrum och en överbyggd terrass bredvid en öppen; nedanför, på plan 0, ett allrum, ett sovrum, ett arbetsrum, två badrum, en tvättstuga och en terrass med planteringslåda.')
a('.residences.items[0].points[1]',
  '{N138.95} {U} construidos interiores y {N72.03} {U} de terrazas, {N210.98} {U} en total; {N121.70} {U} útiles y {N67.48} {U} de terraza útil según el plano.',
  '{N138.95} {U} construits à l’intérieur et {N72.03} {U} de terrasses, {N210.98} {U} au total ; {N121.70} {U} utiles et {N67.48} {U} de terrasse utile sur le plan.',
  '{N138.95} {U} bebaute Innenfläche und {N72.03} {U} Terrassen, insgesamt {N210.98} {U}; laut Plan {N121.70} {U} Wohnfläche und {N67.48} {U} nutzbare Terrasse.',
  '{N138.95} {U} внутренней площади застройки и {N72.03} {U} террас, всего {N210.98} {U}; по плану {N121.70} {U} полезной площади и {N67.48} {U} полезной площади террас.',
  '{N138.95} {U} مساحة داخلية مبنية و{N72.03} {U} تراسات، بإجمالي {N210.98} {U}؛ و{N121.70} {U} مساحة صافية و{N67.48} {U} تراسات صافية بحسب المخطط.',
  '{N138.95} {U} bebouwd binnen en {N72.03} {U} terrassen, {N210.98} {U} in totaal; {N121.70} {U} nuttige oppervlakte en {N67.48} {U} nuttig terras volgens de plattegrond.',
  '{N138.95} {U} powierzchni zabudowy wewnątrz i {N72.03} {U} tarasów, łącznie {N210.98} {U}; według rzutu {N121.70} {U} powierzchni użytkowej i {N67.48} {U} użytkowej powierzchni tarasów.',
  '{N138.95} {U} bebygd innvendig og {N72.03} {U} terrasser, {N210.98} {U} til sammen; {N121.70} {U} bruksareal og {N67.48} {U} terrasse i bruksareal ifølge plantegningen.',
  '{N138.95} {U} byggyta inomhus och {N72.03} {U} terrasser, {N210.98} {U} totalt; {N121.70} {U} nyttoyta och {N67.48} {U} terrass i nyttoyta enligt planritningen.')
a('.residences.items[0].points[2]',
  'La lista de precios indica tres dormitorios y tres baños. El plano del promotor dibuja dos dormitorios, un despacho de {N10.50} {U} y tres baños; mencionamos ambos datos y confirmamos cuál es el correcto antes de la reserva.',
  'La liste de prix indique trois chambres et trois salles de bains. Le plan du promoteur dessine deux chambres, un bureau de {N10.50} {U} et trois salles de bains ; nous citons les deux et confirmons laquelle prévaut avant la réservation.',
  'Die Preisliste nennt drei Schlafzimmer und drei Bäder. Der Plan des Bauträgers zeigt zwei Schlafzimmer, ein Arbeitszimmer von {N10.50} {U} und drei Bäder; wir nennen beide Angaben und klären vor der Reservierung, welche gilt.',
  'В прайс-листе указаны три спальни и три ванные. На плане застройщика — две спальни, кабинет площадью {N10.50} {U} и три ванные; мы приводим оба варианта и уточняем, какой верен, до бронирования.',
  'تذكر قائمة الأسعار ثلاث غرف نوم وثلاثة حمّامات. أما مخطط المطوّر فيُظهر غرفتي نوم ومكتباً مساحته {N10.50} {U} وثلاثة حمّامات؛ نذكر الرقمين ونؤكد الصحيح منهما قبل الحجز.',
  'De prijslijst vermeldt drie slaapkamers en drie badkamers. De plattegrond van de ontwikkelaar tekent twee slaapkamers, een werkkamer van {N10.50} {U} en drie badkamers; wij noemen beide en bevestigen vóór de reservering welke klopt.',
  'Cennik podaje trzy sypialnie i trzy łazienki. Rzut dewelopera pokazuje dwie sypialnie, gabinet o powierzchni {N10.50} {U} i trzy łazienki; podajemy oba warianty i przed rezerwacją potwierdzamy, który jest właściwy.',
  'Prislisten oppgir tre soverom og tre bad. Utbyggerens plantegning viser to soverom, et kontor på {N10.50} {U} og tre bad; vi oppgir begge og bekrefter hva som gjelder før reservasjon.',
  'Prislistan anger tre sovrum och tre badrum. Exploatörens planritning visar två sovrum, ett arbetsrum på {N10.50} {U} och tre badrum; vi anger båda och bekräftar vilket som gäller före reservationen.')
a('.residences.items[0].points[3]', *[f'{{E740000}} + {t}.' for t in TAX])
a('.residences.items[1].name', 'Vivienda 13, un ático', 'Logement 13, un penthouse', 'Wohnung 13, ein Penthouse',
  'Квартира 13, пентхаус', 'المسكن 13، بنتهاوس', 'Woning 13, een penthouse', 'Mieszkanie 13, penthouse',
  'Bolig 13, en toppleilighet', 'Bostad 13, en takvåning')
a('.residences.items[1].points[0]',
  'En una sola planta: tres dormitorios, dos baños, un vestidor, una cocina y un salón-comedor de {N41.90} {U}.',
  'Sur un seul niveau : trois chambres, deux salles de bains, un dressing, une cuisine et un séjour-salle à manger de {N41.90} {U}.',
  'Auf einer Ebene: drei Schlafzimmer, zwei Bäder, ein Ankleidezimmer, eine Küche und ein Wohn- und Essbereich von {N41.90} {U}.',
  'На одном уровне: три спальни, две ванные, гардеробная, кухня и гостиная-столовая площадью {N41.90} {U}.',
  'على مستوى واحد: ثلاث غرف نوم وحمّامان وغرفة ملابس ومطبخ وصالة جلوس وطعام مساحتها {N41.90} {U}.',
  'Op één niveau: drie slaapkamers, twee badkamers, een inloopkast, een keuken en een woon- en eetkamer van {N41.90} {U}.',
  'Na jednym poziomie: trzy sypialnie, dwie łazienki, garderoba, kuchnia oraz salon z jadalnią o powierzchni {N41.90} {U}.',
  'På ett plan: tre soverom, to bad, et garderoberom, et kjøkken og en stue med spisestue på {N41.90} {U}.',
  'På ett plan: tre sovrum, två badrum, ett klädrum, ett kök och ett vardagsrum med matplats på {N41.90} {U}.')
a('.residences.items[1].points[1]',
  '{N136.28} {U} construidos interiores y {N44.21} {U} de terrazas, {N180.49} {U} en total; {N117.99} {U} útiles y {N43.28} {U} de terraza útil, la mayor parte en una terraza descubierta de {N33.50} {U} junto a los dormitorios.',
  '{N136.28} {U} construits à l’intérieur et {N44.21} {U} de terrasses, {N180.49} {U} au total ; {N117.99} {U} utiles et {N43.28} {U} de terrasse utile, dont l’essentiel en une terrasse découverte de {N33.50} {U} devant les chambres.',
  '{N136.28} {U} bebaute Innenfläche und {N44.21} {U} Terrassen, insgesamt {N180.49} {U}; {N117.99} {U} Wohnfläche und {N43.28} {U} nutzbare Terrasse, das meiste davon eine offene Terrasse von {N33.50} {U} vor den Schlafzimmern.',
  '{N136.28} {U} внутренней площади застройки и {N44.21} {U} террас, всего {N180.49} {U}; {N117.99} {U} полезной площади и {N43.28} {U} полезной площади террас, большая часть — открытая терраса {N33.50} {U} у спален.',
  '{N136.28} {U} مساحة داخلية مبنية و{N44.21} {U} تراسات، بإجمالي {N180.49} {U}؛ و{N117.99} {U} مساحة صافية و{N43.28} {U} تراسات صافية، معظمها تراس مكشوف مساحته {N33.50} {U} بجوار غرف النوم.',
  '{N136.28} {U} bebouwd binnen en {N44.21} {U} terrassen, {N180.49} {U} in totaal; {N117.99} {U} nuttige oppervlakte en {N43.28} {U} nuttig terras, grotendeels een open terras van {N33.50} {U} aan de slaapkamers.',
  '{N136.28} {U} powierzchni zabudowy wewnątrz i {N44.21} {U} tarasów, łącznie {N180.49} {U}; {N117.99} {U} powierzchni użytkowej i {N43.28} {U} użytkowej powierzchni tarasów, w większości otwarty taras o powierzchni {N33.50} {U} przy sypialniach.',
  '{N136.28} {U} bebygd innvendig og {N44.21} {U} terrasser, {N180.49} {U} til sammen; {N117.99} {U} bruksareal og {N43.28} {U} terrasse i bruksareal, det meste en åpen terrasse på {N33.50} {U} utenfor soverommene.',
  '{N136.28} {U} byggyta inomhus och {N44.21} {U} terrasser, {N180.49} {U} totalt; {N117.99} {U} nyttoyta och {N43.28} {U} terrass i nyttoyta, det mesta en öppen terrass på {N33.50} {U} utanför sovrummen.')
a('.residences.items[1].points[2]', *[f'{{E1040000}} + {t}.' for t in TAX])
a('.residences.items[2].name', 'Vivienda 15, un ático dúplex', 'Logement 15, un penthouse duplex', 'Wohnung 15, ein Maisonette-Penthaus',
  'Квартира 15, двухуровневый пентхаус', 'المسكن 15، بنتهاوس دوبلكس', 'Woning 15, een duplex penthouse',
  'Mieszkanie 15, dwupoziomowy penthouse', 'Bolig 15, en toppleilighet over to plan', 'Bostad 15, en takvåning i två plan')
a('.residences.items[2].points[0]',
  'La cocina, un salón-comedor de {N40.00} {U} y un aseo en el nivel 3, con una terraza cubierta y otra descubierta; cuatro dormitorios, dos baños y un vestidor en el nivel 4, con una segunda terraza.',
  'La cuisine, un séjour-salle à manger de {N40.00} {U} et des toilettes d’invités au niveau 3, avec une terrasse couverte et une terrasse découverte ; quatre chambres, deux salles de bains et un dressing au niveau 4, avec une seconde terrasse.',
  'Die Küche, ein Wohn- und Essbereich von {N40.00} {U} und ein Gäste-WC auf Ebene 3, mit einer überdachten und einer offenen Terrasse; vier Schlafzimmer, zwei Bäder und ein Ankleidezimmer auf Ebene 4, mit einer zweiten Terrasse.',
  'Кухня, гостиная-столовая площадью {N40.00} {U} и гостевой туалет на уровне 3, с крытой и открытой террасами; четыре спальни, две ванные и гардеробная на уровне 4, со второй террасой.',
  'المطبخ وصالة جلوس وطعام مساحتها {N40.00} {U} ودورة مياه للضيوف في المستوى 3، مع تراس مسقوف وآخر مكشوف؛ وأربع غرف نوم وحمّامان وغرفة ملابس في المستوى 4، مع تراس ثانٍ.',
  'De keuken, een woon- en eetkamer van {N40.00} {U} en een gastentoilet op niveau 3, met een overdekt en een open terras; vier slaapkamers, twee badkamers en een inloopkast op niveau 4, met een tweede terras.',
  'Kuchnia, salon z jadalnią o powierzchni {N40.00} {U} i toaleta dla gości na poziomie 3, z tarasem zadaszonym i otwartym; cztery sypialnie, dwie łazienki i garderoba na poziomie 4, z drugim tarasem.',
  'Kjøkkenet, en stue med spisestue på {N40.00} {U} og et gjestetoalett på plan 3, med en overbygd og en åpen terrasse; fire soverom, to bad og et garderoberom på plan 4, med en terrasse til.',
  'Köket, ett vardagsrum med matplats på {N40.00} {U} och en gästtoalett på plan 3, med en överbyggd och en öppen terrass; fyra sovrum, två badrum och ett klädrum på plan 4, med ytterligare en terrass.')
a('.residences.items[2].points[1]',
  '{N165.85} {U} construidos interiores y {N38.99} {U} de terrazas, {N204.84} {U} en total; {N136.95} {U} útiles y {N33.72} {U} de terraza útil.',
  '{N165.85} {U} construits à l’intérieur et {N38.99} {U} de terrasses, {N204.84} {U} au total ; {N136.95} {U} utiles et {N33.72} {U} de terrasse utile.',
  '{N165.85} {U} bebaute Innenfläche und {N38.99} {U} Terrassen, insgesamt {N204.84} {U}; {N136.95} {U} Wohnfläche und {N33.72} {U} nutzbare Terrasse.',
  '{N165.85} {U} внутренней площади застройки и {N38.99} {U} террас, всего {N204.84} {U}; {N136.95} {U} полезной площади и {N33.72} {U} полезной площади террас.',
  '{N165.85} {U} مساحة داخلية مبنية و{N38.99} {U} تراسات، بإجمالي {N204.84} {U}؛ و{N136.95} {U} مساحة صافية و{N33.72} {U} تراسات صافية.',
  '{N165.85} {U} bebouwd binnen en {N38.99} {U} terrassen, {N204.84} {U} in totaal; {N136.95} {U} nuttige oppervlakte en {N33.72} {U} nuttig terras.',
  '{N165.85} {U} powierzchni zabudowy wewnątrz i {N38.99} {U} tarasów, łącznie {N204.84} {U}; {N136.95} {U} powierzchni użytkowej i {N33.72} {U} użytkowej powierzchni tarasów.',
  '{N165.85} {U} bebygd innvendig og {N38.99} {U} terrasser, {N204.84} {U} til sammen; {N136.95} {U} bruksareal og {N33.72} {U} terrasse i bruksareal.',
  '{N165.85} {U} byggyta inomhus och {N38.99} {U} terrasser, {N204.84} {U} totalt; {N136.95} {U} nyttoyta och {N33.72} {U} terrass i nyttoyta.')
a('.residences.items[2].points[2]', *[f'{{E1145000}} + {t}.' for t in TAX])

# ---- quality specification ----------------------------------------------------------------------
a('.qualitySpecs.copy',
  'La memoria de calidades del propio promotor, resumida por partes de la vivienda.',
  'Le descriptif technique du promoteur, résumé par partie du logement.',
  'Die Baubeschreibung des Bauträgers, nach Bereichen der Wohnung zusammengefasst.',
  'Спецификация застройщика, кратко по частям квартиры.',
  'مواصفات البناء الخاصة بالمطوّر، ملخّصة بحسب أجزاء المسكن.',
  'De eigen bouwbeschrijving van de ontwikkelaar, samengevat per onderdeel van de woning.',
  'Specyfikacja techniczna dewelopera, w skrócie według części mieszkania.',
  'Utbyggerens egen byggebeskrivelse, oppsummert etter del av boligen.',
  'Exploatörens egen byggbeskrivning, sammanfattad per del av bostaden.')
a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor, en inglés y en español, de julio de 2025. Indica que los acabados pueden modificarse o sustituirse por otros de igual o superior calidad por decisiones técnicas, cambios en los modelos de fabricación o cambios normativos. Las dos versiones difieren en un punto: la inglesa sitúa las placas fotovoltaicas en la cubierta de los garajes, y la española y el folleto en la cubierta del edificio wellness.',
  'Source : le descriptif technique du promoteur, en anglais et en espagnol, de juillet 2025. Il précise que les finitions peuvent être modifiées ou remplacées par d’autres de qualité égale ou supérieure pour des raisons techniques, des changements de modèles des fabricants ou de nouvelles réglementations. Les deux versions diffèrent sur un point : l’anglaise place les panneaux photovoltaïques sur le toit des parkings, l’espagnole et la brochure sur le toit du bâtiment bien-être.',
  'Quelle: die Baubeschreibung des Bauträgers auf Englisch und Spanisch vom Juli 2025. Sie hält fest, dass Ausstattungen aus technischen Gründen, wegen geänderter Herstellermodelle oder neuer Vorschriften geändert oder durch gleich- oder höherwertige ersetzt werden können. Die beiden Fassungen weichen in einem Punkt ab: Die englische verortet die Photovoltaikanlage auf dem Dach der Garagen, die spanische und die Broschüre auf dem Dach des Wellnessgebäudes.',
  'Источник: спецификация застройщика на английском и испанском языках от июля 2025 года. В ней указано, что отделка может быть изменена или заменена на равноценную или более качественную по техническим причинам, из-за смены моделей производителей или новых норм. Версии расходятся в одном: в английской солнечные панели размещены на крыше парковки, в испанской и в буклете — на крыше велнес-корпуса.',
  'المصدر: مواصفات البناء الخاصة بالمطوّر، بالإنجليزية والإسبانية، المؤرخة يوليو 2025. وتذكر أن التشطيبات قد تُعدَّل أو تُستبدل بأخرى مماثلة الجودة أو أعلى لأسباب فنية أو لتغيّر طرازات الشركات المصنّعة أو لتغيّر اللوائح. وتختلف النسختان في نقطة واحدة: فالإنجليزية تضع الألواح الكهروضوئية على سطح مواقف السيارات، أما الإسبانية والكتيّب فعلى سطح مبنى العافية.',
  'Bron: de bouwbeschrijving van de ontwikkelaar, in het Engels en het Spaans, van juli 2025. Daarin staat dat afwerkingen om technische redenen, door gewijzigde fabrieksmodellen of nieuwe regelgeving kunnen worden gewijzigd of vervangen door gelijkwaardige of betere. De twee versies verschillen op één punt: de Engelse plaatst de zonnepanelen op het dak van de garages, de Spaanse en de brochure op het dak van het wellnessgebouw.',
  'Źródło: specyfikacja techniczna dewelopera, po angielsku i po hiszpańsku, z lipca 2025 r. Zaznacza ona, że wykończenia mogą zostać zmienione lub zastąpione innymi o równej lub wyższej jakości z przyczyn technicznych, wskutek zmian modeli producentów lub nowych przepisów. Obie wersje różnią się w jednym punkcie: angielska umieszcza panele fotowoltaiczne na dachu garaży, hiszpańska i broszura — na dachu budynku wellness.',
  'Kilde: utbyggerens byggebeskrivelse, på engelsk og spansk, fra juli 2025. Den sier at utførelsen kan endres eller erstattes med tilsvarende eller bedre kvalitet av tekniske grunner, endrede produsentmodeller eller nye forskrifter. Versjonene er uenige på ett punkt: den engelske plasserer solcellepanelene på taket av parkeringsanlegget, den spanske og brosjyren på taket av velværebygget.',
  'Källa: exploatörens byggbeskrivning, på engelska och spanska, från juli 2025. Den anger att utförandet kan ändras eller ersättas med likvärdigt eller bättre av tekniska skäl, ändrade tillverkarmodeller eller nya föreskrifter. De två versionerna skiljer sig på en punkt: den engelska placerar solpanelerna på garagens tak, den spanska och broschyren på wellnessbyggnadens tak.')
a('.qualitySpecs.groups[0].items[0]',
  'Cimentación y estructura de hormigón armado, conforme al Código Técnico de la Edificación.',
  'Fondations et structure en béton armé, conformes au Code technique de la construction espagnol.',
  'Fundamente und Tragwerk aus Stahlbeton nach der spanischen Bauordnung (Código Técnico de la Edificación).',
  'Фундамент и каркас из железобетона в соответствии с Техническим строительным кодексом Испании.',
  'أساسات وهيكل من الخرسانة المسلّحة وفق قانون البناء الفني الإسباني.',
  'Fundering en draagstructuur van gewapend beton, volgens de Spaanse technische bouwcode.',
  'Fundamenty i konstrukcja z żelbetu, zgodnie z hiszpańskim Technicznym Kodeksem Budowlanym.',
  'Fundamenter og bærekonstruksjon i armert betong, etter den spanske tekniske byggeforskriften.',
  'Grundläggning och stomme i armerad betong, enligt den spanska tekniska byggnormen.')
a('.qualitySpecs.groups[0].items[1]',
  'Fachada de doble hoja de ladrillo perforado con mortero hidrófugo y pintura acrílica, aislamiento de poliuretano proyectado, cámara de aire y hoja interior de placa de yeso con lana mineral.',
  'Façade à double paroi en brique perforée avec enduit hydrofuge et peinture acrylique, isolation en polyuréthane projeté, lame d’air et paroi intérieure en plaques de plâtre avec laine minérale.',
  'Zweischalige Fassade aus Lochziegeln mit wasserabweisendem Putz und Acrylfarbe, Spritzschaum-Dämmung aus Polyurethan, Luftschicht und innerer Schale aus Gipskarton mit Mineralwolle.',
  'Двухслойный фасад из пустотелого кирпича с гидрофобной штукатуркой и акриловой краской, напыляемым пенополиуретановым утеплителем, воздушной прослойкой и внутренним слоем из гипсокартона с минеральной ватой.',
  'واجهة مزدوجة الطبقة من الطوب المثقّب مع لياسة طاردة للماء وطلاء أكريليكي، وعزل من البولي يوريثان المرشوش، وفجوة هوائية، وطبقة داخلية من ألواح الجبس مع الصوف المعدني.',
  'Een dubbelwandige gevel van geperforeerde baksteen met waterafstotende pleister en acrylverf, gespoten polyurethaanisolatie, een spouw en een binnenblad van gipsplaat met minerale wol.',
  'Dwuwarstwowa elewacja z cegły perforowanej z hydrofobowym tynkiem i farbą akrylową, natryskową izolacją z poliuretanu, pustką powietrzną i wewnętrzną warstwą z płyt gipsowo-kartonowych z wełną mineralną.',
  'En totrinns fasade i hulltegl med vannavstøtende puss og akrylmaling, sprøytet polyuretanisolasjon, luftspalte og et indre sjikt av gipsplater med mineralull.',
  'En tvåskalig fasad av håltegel med vattenavvisande puts och akrylfärg, sprutad polyuretanisolering, luftspalt och ett inre skikt av gipsskivor med mineralull.')
a('.qualitySpecs.groups[0].items[2]',
  'Cubiertas transitables en terraza, de tipo invertido, impermeabilizadas y aisladas, acabadas en gres porcelánico antideslizante.',
  'Toitures-terrasses accessibles de type inversé, étanchées et isolées, finies en grès cérame antidérapant.',
  'Begehbare Dachterrassen als Umkehrdach, abgedichtet und gedämmt, mit rutschfestem Feinsteinzeug belegt.',
  'Эксплуатируемые кровли-террасы инверсионного типа с гидро- и теплоизоляцией, с нескользящим керамогранитом.',
  'أسطح تراسات قابلة للمشي من النوع المعكوس، معزولة ضد الماء والحرارة، ومكسوّة بالبورسلين المانع للانزلاق.',
  'Beloopbare dakterrassen als omgekeerd dak, waterdicht gemaakt en geïsoleerd, afgewerkt met antislip keramische tegels.',
  'Użytkowe dachy tarasowe w układzie odwróconym, zaizolowane przeciwwodnie i termicznie, wykończone antypoślizgowym gresem porcelanowym.',
  'Gangbare takterrasser bygget som omvendt tak, tettet og isolert, med sklisikre porselensfliser.',
  'Gångbara takterrasser byggda som omvänt tak, tätade och isolerade, med halksäkra porslinsplattor.')
a('.qualitySpecs.groups[1].name', 'Paredes y suelos', 'Murs et sols', 'Wände und Böden', 'Стены и полы', 'الجدران والأرضيات',
  'Wanden en vloeren', 'Ściany i podłogi', 'Vegger og gulv', 'Väggar och golv')
a('.qualitySpecs.groups[1].items[0]',
  'Triple tabique entre viviendas, de ladrillo hueco doble con membrana acústica, trasdosado con placa de yeso por ambas caras y aislado con lana mineral.',
  'Une triple cloison entre logements, en brique creuse double avec membrane acoustique, doublée de plaques de plâtre des deux côtés et isolée à la laine minérale.',
  'Eine dreifache Trennwand zwischen den Wohnungen aus doppeltem Hohlziegel mit Akustikmembran, beidseitig mit Gipskarton beplankt und mit Mineralwolle gedämmt.',
  'Тройная перегородка между квартирами из двойного пустотелого кирпича с акустической мембраной, облицованная гипсокартоном с обеих сторон и утеплённая минеральной ватой.',
  'جدار ثلاثي بين المساكن من الطوب المجوّف المزدوج مع غشاء صوتي، مكسوّ بألواح الجبس من الجهتين ومعزول بالصوف المعدني.',
  'Een driedubbele wand tussen de woningen, van dubbele holle baksteen met akoestisch membraan, aan beide zijden bekleed met gipsplaat en geïsoleerd met minerale wol.',
  'Potrójna ściana między mieszkaniami z podwójnej cegły dziurawki z membraną akustyczną, obłożona z obu stron płytami gipsowo-kartonowymi i izolowana wełną mineralną.',
  'En trippel skillevegg mellom boligene, av dobbel hulltegl med lydmembran, kledd med gipsplater på begge sider og isolert med mineralull.',
  'En trippel vägg mellan bostäderna, av dubbelt håltegel med ljudmembran, klädd med gipsskivor på båda sidor och isolerad med mineralull.')
a('.qualitySpecs.groups[1].items[1]',
  'Tabiquería interior de placa de yeso por ambas caras con lana mineral, con placas hidrófugas en los cuartos húmedos.',
  'Cloisons intérieures en plaques de plâtre des deux côtés avec laine minérale, et plaques hydrofuges dans les pièces humides.',
  'Innenwände aus beidseitigem Gipskarton mit Mineralwolle, mit wasserabweisenden Platten in den Nassräumen.',
  'Внутренние перегородки из гипсокартона с обеих сторон с минеральной ватой, во влажных помещениях — влагостойкие листы.',
  'قواطع داخلية من ألواح الجبس من الجهتين مع الصوف المعدني، وألواح مقاومة للماء في الغرف الرطبة.',
  'Binnenwanden van gipsplaat aan beide zijden met minerale wol, met waterwerende platen in de natte ruimten.',
  'Ścianki działowe z płyt gipsowo-kartonowych po obu stronach z wełną mineralną, w pomieszczeniach mokrych z płyt wodoodpornych.',
  'Innervegger av gipsplater på begge sider med mineralull, med vannavstøtende plater i våtrommene.',
  'Innerväggar av gipsskivor på båda sidor med mineralull, med vattenavvisande skivor i våtrummen.')
a('.qualitySpecs.groups[1].items[2]',
  'Gres porcelánico de gran formato en toda la vivienda, el mismo en las terrazas, y porcelánico rectificado de gran formato en las paredes de los baños.',
  'Grès cérame grand format dans tout le logement, le même sur les terrasses, et céramique rectifiée grand format aux murs des salles de bains.',
  'Großformatiges Feinsteinzeug in der ganzen Wohnung, dasselbe auf den Terrassen, und großformatige rektifizierte Feinsteinzeugfliesen an den Badwänden.',
  'Крупноформатный керамогранит во всей квартире, тот же на террасах, и крупноформатная ректифицированная плитка на стенах ванных.',
  'بورسلين كبير الحجم في كامل المسكن، والنوع نفسه على التراسات، وبورسلين مُعايَر كبير الحجم على جدران الحمّامات.',
  'Groot formaat keramische tegels in de hele woning, dezelfde op de terrassen, en gerectificeerde tegels van groot formaat op de badkamerwanden.',
  'Wielkoformatowy gres porcelanowy w całym mieszkaniu, ten sam na tarasach, oraz wielkoformatowe rektyfikowane płytki na ścianach łazienek.',
  'Storformat porselensfliser i hele boligen, de samme på terrassene, og storformat kalibrerte fliser på baderomsveggene.',
  'Storformatiga porslinsplattor i hela bostaden, samma på terrasserna, och storformatiga kalibrerade plattor på badrumsväggarna.')
a('.qualitySpecs.groups[2].items[0]',
  'Carpintería de aluminio lacado con rotura de puente térmico y doble acristalamiento, con vidrio bajo emisivo en los salones.',
  'Menuiseries en aluminium laqué à rupture de pont thermique et double vitrage, avec verre à faible émissivité dans les séjours.',
  'Fenster aus lackiertem Aluminium mit thermischer Trennung und Doppelverglasung, in den Wohnzimmern mit Low-E-Glas.',
  'Окна из окрашенного алюминия с терморазрывом и двойным остеклением, в гостиных — низкоэмиссионное стекло.',
  'نوافذ من الألمنيوم المطلي مع قاطع حراري وزجاج مزدوج، وزجاج منخفض الانبعاث في الصالات.',
  'Gelakt aluminium schrijnwerk met thermische onderbreking en dubbele beglazing, met laag-emissieglas in de woonkamers.',
  'Stolarka z lakierowanego aluminium z przekładką termiczną i podwójnymi szybami, w salonach szkło niskoemisyjne.',
  'Vinduer i lakkert aluminium med kuldebrobryter og dobbelt glass, med lavemisjonsglass i stuene.',
  'Fönster i lackerad aluminium med köldbryggsbrytning och dubbla glas, med lågemissionsglas i vardagsrummen.')
a('.qualitySpecs.groups[2].items[1]',
  'Persianas enrollables de lamas de aluminio en los dormitorios, motorizadas en los principales y de cinta en el resto.',
  'Volets roulants à lames d’aluminium dans les chambres, motorisés dans les chambres principales et à sangle dans les autres.',
  'Aluminium-Rollläden in den Schlafzimmern, in den Hauptschlafzimmern motorisiert, in den übrigen mit Gurt.',
  'Алюминиевые рольставни в спальнях: в главных — с электроприводом, в остальных — с ручным ремнём.',
  'مصاريع ألمنيوم ملفوفة في غرف النوم، تعمل بمحرّك في الغرف الرئيسية وبحزام يدوي في الباقي.',
  'Aluminium rolluiken in de slaapkamers, gemotoriseerd in de grote slaapkamers en met band in de andere.',
  'Aluminiowe rolety zewnętrzne w sypialniach, z napędem w głównych i na taśmę w pozostałych.',
  'Rullegardiner i aluminium på soverommene, motoriserte på hovedsoverommene og med reim på de andre.',
  'Rullgardiner i aluminium i sovrummen, motoriserade i huvudsovrummen och med band i de övriga.')
a('.qualitySpecs.groups[2].items[2]',
  'Puerta de entrada de seguridad con cerradura de tres puntos, puertas interiores lacadas en blanco y armarios empotrados con puertas correderas o abatibles, balda y barra de colgar.',
  'Porte d’entrée de sécurité avec serrure trois points, portes intérieures laquées blanc et placards intégrés à portes coulissantes ou battantes, avec étagère et penderie.',
  'Sicherheitseingangstür mit Dreifachverriegelung, weiß lackierte Innentüren und Einbauschränke mit Schiebe- oder Falttüren, Ablage und Kleiderstange.',
  'Входная бронированная дверь с трёхточечным замком, белые лакированные межкомнатные двери и встроенные шкафы с раздвижными или распашными дверцами, полкой и штангой.',
  'باب دخول أمني بقفل ثلاثي النقاط، وأبواب داخلية مطلية بالأبيض، وخزائن مدمجة بأبواب منزلقة أو قابلة للطي مع رفّ وقضيب تعليق.',
  'Een veiligheidsvoordeur met driepuntsslot, wit gelakte binnendeuren en inbouwkasten met schuif- of vouwdeuren, een legplank en een kledingstang.',
  'Antywłamaniowe drzwi wejściowe z zamkiem trzypunktowym, białe lakierowane drzwi wewnętrzne i szafy wnękowe z drzwiami przesuwnymi lub składanymi, półką i drążkiem.',
  'Sikkerhetsdør med trepunktslås, hvitlakkerte innerdører og innebygde garderobeskap med skyve- eller foldedører, hylle og kleshengerstang.',
  'Säkerhetsdörr med trepunktslås, vitlackerade innerdörrar och inbyggda garderober med skjut- eller vikdörrar, hylla och klädstång.')
a('.qualitySpecs.groups[3].items[0]',
  'Muebles altos y bajos a elegir entre dos colores, con encimera y frente entre muebles de Silestone, Compac o similar.',
  'Meubles hauts et bas au choix en deux coloris, avec plan de travail et crédence en Silestone, Compac ou similaire.',
  'Ober- und Unterschränke in zwei Farben zur Wahl, mit Arbeitsplatte und Rückwand aus Silestone, Compac oder Gleichwertigem.',
  'Верхние и нижние шкафы на выбор в двух цветах, со столешницей и фартуком из Silestone, Compac или аналога.',
  'خزائن علوية وسفلية بلونين للاختيار، مع سطح عمل وواجهة خلفية من Silestone أو Compac أو ما يماثلهما.',
  'Boven- en onderkasten in een keuze uit twee kleuren, met werkblad en achterwand van Silestone, Compac of gelijkwaardig.',
  'Szafki górne i dolne do wyboru w dwóch kolorach, z blatem i ścianą między szafkami z Silestone, Compac lub podobnego materiału.',
  'Over- og underskap i valgfri av to farger, med benkeplate og vegg mellom skapene i Silestone, Compac eller tilsvarende.',
  'Över- och underskåp i två färger att välja mellan, med bänkskiva och stänkskydd i Silestone, Compac eller likvärdigt.')
a('.qualitySpecs.groups[3].items[1]',
  'Electrodomésticos Bosch, Teka o similar: campana extractora, placa de inducción, horno eléctrico, microondas, lavavajillas, frigorífico y fregadero de acero.',
  'Électroménager Bosch, Teka ou similaire : hotte, plaque à induction, four électrique, micro-ondes, lave-vaisselle, réfrigérateur et évier en inox.',
  'Geräte von Bosch, Teka oder gleichwertig: Dunstabzugshaube, Induktionskochfeld, Elektrobackofen, Mikrowelle, Geschirrspüler, Kühlschrank und Edelstahlspüle.',
  'Техника Bosch, Teka или аналог: вытяжка, индукционная варочная панель, электрическая духовка, микроволновая печь, посудомоечная машина, холодильник и стальная мойка.',
  'أجهزة Bosch أو Teka أو ما يماثلها: شفاط، وموقد حثّي، وفرن كهربائي، وميكروويف، وغسالة صحون، وثلاجة، ومغسلة من الفولاذ.',
  'Apparatuur van Bosch, Teka of gelijkwaardig: afzuigkap, inductiekookplaat, elektrische oven, magnetron, vaatwasser, koelkast en stalen spoelbak.',
  'Sprzęt Bosch, Teka lub podobny: okap, płyta indukcyjna, piekarnik elektryczny, mikrofalówka, zmywarka, lodówka i stalowy zlew.',
  'Hvitevarer fra Bosch, Teka eller tilsvarende: kjøkkenvifte, induksjonstopp, elektrisk stekeovn, mikrobølgeovn, oppvaskmaskin, kjøleskap og stålvask.',
  'Vitvaror från Bosch, Teka eller likvärdigt: köksfläkt, induktionshäll, elektrisk ugn, mikrovågsugn, diskmaskin, kylskåp och diskho i stål.')
a('.qualitySpecs.groups[4].items[0]',
  'Mueble con lavabo integrado, inodoros suspendidos con cisterna empotrada en el baño principal y platos de ducha de resina de bajo perfil.',
  'Meuble avec vasque intégrée, WC suspendus à réservoir encastré dans la salle de bains principale et receveurs de douche extra-plats en résine.',
  'Waschtischunterschrank mit integriertem Becken, wandhängende WCs mit Unterputzspülkasten im Hauptbad und flache Duschwannen aus Mineralguss.',
  'Тумба с интегрированной раковиной, подвесные унитазы со скрытым бачком в главной ванной и низкие душевые поддоны из искусственного камня.',
  'وحدة مغسلة مدمجة، ومراحيض معلّقة بخزان مخفي في الحمّام الرئيسي، وقواعد دُش منخفضة من الراتنج.',
  'Een badmeubel met geïntegreerde wastafel, hangtoiletten met inbouwreservoir in de hoofdbadkamer en lage douchebakken van kunsthars.',
  'Szafka z wbudowaną umywalką, podwieszane toalety ze stelażem w głównej łazience i niskie brodziki z żywicy.',
  'Servantskap med integrert vask, vegghengte toaletter med innebygd sisterne på hovedbadet og lave dusjkar i kunstharpiks.',
  'Kommod med integrerat tvättställ, vägghängda toaletter med inbyggd cistern i huvudbadrummet och låga duschkar i kompositmaterial.')
a('.qualitySpecs.groups[4].items[1]',
  'Grifería monomando cromada con economizadores de agua, y grifería empotrada en las duchas.',
  'Robinetterie mitigeur chromée avec économiseurs d’eau, et robinetterie encastrée dans les douches.',
  'Verchromte Einhebelarmaturen mit Wassersparern und Unterputzarmaturen in den Duschen.',
  'Хромированные однорычажные смесители с водосберегающими насадками и встроенные смесители в душевых.',
  'خلّاطات كرومية بذراع واحدة مع موفّرات للمياه، وخلّاطات مدمجة في الجدار في أماكن الدُش.',
  'Verchroomde eenhendelkranen met waterbesparing, en inbouwkranen in de douches.',
  'Chromowane baterie jednouchwytowe z perlatorami oszczędzającymi wodę oraz baterie podtynkowe w prysznicach.',
  'Forkrommede ettgrepsbatterier med vannsparer, og innebygde batterier i dusjene.',
  'Förkromade engreppsblandare med vattensparare, och infällda blandare i duscharna.')
a('.qualitySpecs.groups[4].items[2]',
  'Suelo radiante eléctrico en los baños.', 'Plancher chauffant électrique dans les salles de bains.',
  'Elektrische Fußbodenheizung in den Bädern.', 'Электрический тёплый пол в ванных комнатах.',
  'تدفئة أرضية كهربائية في الحمّامات.', 'Elektrische vloerverwarming in de badkamers.',
  'Elektryczne ogrzewanie podłogowe w łazienkach.', 'Elektrisk gulvvarme på badene.', 'Elektrisk golvvärme i badrummen.')
a('.qualitySpecs.groups[5].items[0]',
  'Climatización por conductos con bomba de calor, frío y calor, con control de temperatura por estancia mediante rejillas motorizadas, o equipos split en cada estancia, según la vivienda.',
  'Climatisation gainable par pompe à chaleur, chaud et froid, avec réglage de la température pièce par pièce par grilles motorisées, ou splits dans chaque pièce, selon le logement.',
  'Kanal-Klimaanlage mit Wärmepumpe für Wärme und Kühlung, mit raumweiser Temperaturregelung über motorisierte Gitter, oder Split-Geräte in jedem Raum, je nach Wohnung.',
  'Канальное кондиционирование с тепловым насосом на тепло и холод, с регулировкой температуры в каждой комнате через моторизованные решётки, или сплит-системы в каждой комнате — в зависимости от квартиры.',
  'تكييف بمجاري الهواء بمضخة حرارية للتدفئة والتبريد، مع تحكم في درجة حرارة كل غرفة عبر فتحات آلية، أو وحدات سبليت في كل غرفة، بحسب المسكن.',
  'Kanaalgebonden airconditioning met warmtepomp, voor warmte en koeling, met temperatuurregeling per kamer via gemotoriseerde roosters, of splitunits in elke kamer, afhankelijk van de woning.',
  'Klimatyzacja kanałowa z pompą ciepła, grzanie i chłodzenie, z regulacją temperatury w każdym pomieszczeniu przez zmotoryzowane kratki, lub klimatyzatory split w każdym pomieszczeniu, zależnie od mieszkania.',
  'Kanalbasert klimaanlegg med varmepumpe, varme og kjøling, med temperaturstyring rom for rom via motoriserte rister, eller splitenheter i hvert rom, avhengig av boligen.',
  'Kanalbaserad luftkonditionering med värmepump, värme och kyla, med temperaturstyrning rum för rum via motoriserade galler, eller splitaggregat i varje rum, beroende på bostaden.')
a('.qualitySpecs.groups[5].items[1]',
  'Agua caliente mediante aerotermia en cada vivienda y un sistema de ventilación de simple flujo que renueva el aire de forma continua.',
  'Eau chaude par pompe à chaleur aérothermique dans chaque logement, et une VMC simple flux qui renouvelle l’air en continu.',
  'Warmwasser über eine Luftwärmepumpe in jeder Wohnung und eine Abluftanlage, die laufend frische Luft zuführt.',
  'Горячая вода от аэротермального теплового насоса в каждой квартире и приточно-вытяжная вентиляция простого потока, непрерывно обновляющая воздух.',
  'مياه ساخنة من مضخة حرارية هوائية في كل مسكن، ونظام تهوية أحادي التدفق يجدد الهواء باستمرار.',
  'Warm water via een luchtwarmtepomp in elke woning, en een enkelvoudig ventilatiesysteem dat continu verse lucht aanvoert.',
  'Ciepła woda z pompy ciepła typu powietrze-woda w każdym mieszkaniu i jednostrumieniowa wentylacja, która stale doprowadza świeże powietrze.',
  'Varmtvann fra en luft-til-vann-varmepumpe i hver bolig, og et enkelt ventilasjonsanlegg som tilfører frisk luft kontinuerlig.',
  'Varmvatten från en luftvärmepump i varje bostad, och ett frånluftssystem som kontinuerligt tillför frisk luft.')
a('.qualitySpecs.groups[5].items[2]',
  'Placas fotovoltaicas para el autoconsumo de la comunidad, que además cubren parte de la demanda del sistema de aerotermia.',
  'Panneaux photovoltaïques pour l’autoconsommation de la copropriété, qui couvrent aussi une partie des besoins du système aérothermique.',
  'Photovoltaikanlage für den Eigenverbrauch der Gemeinschaft, die auch einen Teil des Bedarfs der Luftwärmepumpen deckt.',
  'Солнечные панели для собственного потребления комплекса, покрывающие также часть потребностей аэротермальной системы.',
  'ألواح كهروضوئية للاستهلاك الذاتي للمجمع، تغطي أيضاً جزءاً من احتياجات نظام المضخات الحرارية الهوائية.',
  'Zonnepanelen voor eigen verbruik van de gemeenschap, die ook een deel van de behoefte van het luchtwarmtepompsysteem dekken.',
  'Panele fotowoltaiczne na własne potrzeby wspólnoty, pokrywające także część zapotrzebowania systemu pomp ciepła.',
  'Solcellepaneler til fellesskapets eget forbruk, som også dekker en del av behovet til luft-til-vann-anlegget.',
  'Solpaneler för gemensamhetens egen förbrukning, som också täcker en del av luftvärmepumparnas behov.')
a('.qualitySpecs.groups[6].items[0]',
  'Piscina con pared de vidrio, cloración salina e iluminación subacuática, zona chill-out con barbacoa junto a ella, sauna finlandesa con vestuario y ducha, y gimnasio con grandes ventanales.',
  'Une piscine à paroi vitrée, électrolyse au sel et éclairage subaquatique, un espace détente avec barbecue à côté, un sauna finlandais avec vestiaire et douche, et une salle de sport aux grandes baies.',
  'Ein Pool mit Glaswand, Salzelektrolyse und Unterwasserbeleuchtung, eine Chill-out-Zone mit Grill daneben, eine finnische Sauna mit Umkleide und Dusche und ein Fitnessraum mit großen Fenstern.',
  'Бассейн со стеклянной стенкой, солевой очисткой и подводной подсветкой, зона отдыха с барбекю рядом, финская сауна с раздевалкой и душем и тренажёрный зал с большими окнами.',
  'مسبح بجدار زجاجي وتعقيم ملحي وإضاءة تحت الماء، ومنطقة استرخاء مع شواء بجواره، وساونا فنلندية مع غرفة تبديل ملابس ودُش، وصالة رياضية بنوافذ كبيرة.',
  'Een zwembad met glazen wand, zoutelektrolyse en onderwaterverlichting, een chill-outzone met barbecue ernaast, een Finse sauna met kleedruimte en douche, en een fitnessruimte met grote ramen.',
  'Basen ze szklaną ścianą, chlorowaniem solnym i podwodnym oświetleniem, obok strefa chill-out z grillem, fińska sauna z przebieralnią i prysznicem oraz siłownia z dużymi oknami.',
  'Et basseng med glassvegg, saltklorering og undervannsbelysning, et chill-out-område med grill ved siden av, en finsk badstue med garderobe og dusj, og et treningsrom med store vinduer.',
  'En pool med glasvägg, saltklorering och undervattensbelysning, en chill-out-yta med grill bredvid, en finsk bastu med omklädningsrum och dusch, och ett gym med stora fönster.')
a('.qualitySpecs.groups[6].items[1]',
  'Recinto completamente cerrado y vallado, con control de acceso peatonal y de vehículos mediante circuito cerrado de televisión, y ascensores para ocho personas que comunican todas las plantas.',
  'Un ensemble entièrement clos, avec contrôle d’accès des piétons et des véhicules par vidéosurveillance, et des ascenseurs pour huit personnes desservant tous les étages.',
  'Eine vollständig umzäunte Anlage mit Zugangskontrolle für Fußgänger und Fahrzeuge per Videoüberwachung und Aufzügen für acht Personen zu allen Etagen.',
  'Полностью огороженный комплекс с контролем доступа для пешеходов и автомобилей через систему видеонаблюдения и лифтами на восемь человек на все этажи.',
  'مجمع مسوّر بالكامل مع مراقبة دخول المشاة والمركبات عبر دائرة تلفزيونية مغلقة، ومصاعد تتسع لثمانية أشخاص تخدم جميع الطوابق.',
  'Een volledig omheind complex met toegangscontrole voor voetgangers en voertuigen via camerabewaking, en liften voor acht personen naar alle verdiepingen.',
  'Całkowicie ogrodzony kompleks z kontrolą dostępu pieszych i pojazdów przez monitoring, oraz windy dla ośmiu osób obsługujące wszystkie piętra.',
  'Et helt inngjerdet anlegg med adgangskontroll for gående og kjøretøy via videoovervåking, og heiser for åtte personer til alle etasjer.',
  'Ett helt inhägnat område med tillträdeskontroll för gående och fordon via kameraövervakning, och hissar för åtta personer till alla våningar.')
a('.qualitySpecs.groups[6].items[2]',
  'Garaje con puerta automática, solería de hormigón pulido y preinstalación para la carga de vehículo eléctrico desde el contador de la propia vivienda.',
  'Un garage à porte automatique, sol en béton poli et pré-installation pour la recharge d’une voiture électrique depuis le compteur du logement.',
  'Eine Garage mit automatischem Tor, poliertem Betonboden und Vorinstallation zum Laden eines Elektroautos über den Zähler der eigenen Wohnung.',
  'Гараж с автоматическими воротами, полированным бетонным полом и подготовкой для зарядки электромобиля от счётчика квартиры.',
  'مرآب ببوابة آلية وأرضية خرسانية مصقولة، وتمديدات مسبقة لشحن السيارة الكهربائية من عدّاد المسكن نفسه.',
  'Een garage met automatische poort, gepolijste betonvloer en voorbereiding voor het laden van een elektrische auto via de eigen meter van de woning.',
  'Garaż z automatyczną bramą, polerowaną posadzką betonową i przygotowaniem do ładowania samochodu elektrycznego z licznika mieszkania.',
  'En garasje med automatisk port, polert betonggulv og forberedt for lading av elbil fra boligens egen måler.',
  'Ett garage med automatisk port, polerat betonggolv och förberett för laddning av elbil från bostadens egen mätare.')

# ---- availability -------------------------------------------------------------------------------
a('.availability.copy',
  'La lista de precios del promotor del 27 de octubre de 2026 muestra trece de las dieciséis viviendas reservadas y tres disponibles. Los precios son netos y no incluyen el IVA; confirmamos precio y disponibilidad antes de cualquier reserva.',
  'La liste de prix du promoteur du 27 octobre 2026 indique treize des seize logements réservés et trois disponibles. Les prix sont nets, hors TVA ; nous confirmons prix et disponibilité avant toute réservation.',
  'Die Preisliste des Bauträgers vom 27. Oktober 2026 weist dreizehn der sechzehn Wohnungen als reserviert und drei als frei aus. Die Preise sind Nettopreise ohne MwSt.; wir bestätigen Preis und Verfügbarkeit vor jeder Reservierung.',
  'В прайс-листе застройщика от 27 октября 2026 года тринадцать из шестнадцати квартир забронированы, три свободны. Цены указаны нетто, без НДС; мы подтверждаем цену и наличие перед любым бронированием.',
  'تُظهر قائمة أسعار المطوّر المؤرخة 27 أكتوبر 2026 أن ثلاثة عشر من المساكن الستة عشر محجوزة وثلاثة متاحة. والأسعار صافية ولا تشمل ضريبة القيمة المضافة؛ ونؤكد السعر والتوافر قبل أي حجز.',
  'De prijslijst van de ontwikkelaar van 27 oktober 2026 toont dertien van de zestien woningen als gereserveerd en drie als beschikbaar. De prijzen zijn netto, excl. btw; wij bevestigen prijs en beschikbaarheid vóór elke reservering.',
  'Cennik dewelopera z 27 października 2026 r. pokazuje trzynaście z szesnastu mieszkań jako zarezerwowane i trzy jako dostępne. Ceny są netto, bez VAT; potwierdzamy cenę i dostępność przed każdą rezerwacją.',
  'Utbyggerens prisliste datert 27. oktober 2026 viser tretten av de seksten boligene som reservert og tre som ledige. Prisene er netto og uten mva; vi bekrefter pris og tilgjengelighet før enhver reservasjon.',
  'Exploatörens prislista daterad 27 oktober 2026 visar tretton av de sexton bostäderna som reserverade och tre som lediga. Priserna är netto och exklusive IVA; vi bekräftar pris och tillgänglighet före varje reservation.')
a('.availability.startingPrice', *[f'{{E740000}} + {t}' for t in TAX])
a('.availability.checkedDate', '27 de octubre de 2026', '27 octobre 2026', '27. Oktober 2026', '27 октября 2026 года',
  '27 أكتوبر 2026', '27 oktober 2026', '27 października 2026 r.', '27. oktober 2026', '27 oktober 2026')
a('.availability.sourceNote',
  'Disponibilidad y precios según la lista del 27 de octubre de 2026, confirmados antes de la reserva. Dormitorios, baños, niveles y superficies construidas proceden de la lista de precios del promotor de esa fecha, que indica que los precios son netos y no incluyen el IVA, el Impuesto sobre Transmisiones Patrimoniales ni otros cargos, que es meramente informativa y no forma parte de ningún contrato, y que el vendedor puede modificarla mientras no se haya recibido el depósito inicial. La superficie construida mostrada es la cifra interior de la lista; la de terrazas suma sus terrazas cubiertas y descubiertas. Las superficies útiles proceden del plano del promotor de cada vivienda, calculadas conforme al Decreto andaluz 218/2005. La lista asigna a cada vivienda dos plazas de garaje y un trastero. Las cifras coinciden, con una diferencia que señalamos: la lista da a la vivienda 3 tres dormitorios, mientras que su plano dibuja dos dormitorios y un despacho. Nueva Living vuelve a confirmar precio, estado y condiciones antes de cualquier reserva.',
  'Disponibilité et prix selon la liste du 27 octobre 2026, confirmés avant la réservation. Chambres, salles de bains, niveaux et surfaces construites proviennent de la liste de prix du promoteur à cette date, qui précise que les prix sont nets et n’incluent ni la TVA, ni les droits de mutation, ni d’autres frais, qu’elle est purement indicative et ne fait partie d’aucun contrat, et que le vendeur peut la modifier tant que le dépôt initial n’a pas été reçu. La surface construite indiquée est le chiffre intérieur de la liste ; celle des terrasses additionne ses terrasses couvertes et découvertes. Les surfaces utiles viennent du plan du promoteur pour chaque logement, calculées selon le décret andalou 218/2005. La liste attribue à chaque logement deux places de parking et une cave. Les chiffres concordent, à une différence près que nous signalons : la liste donne trois chambres au logement 3, alors que son plan dessine deux chambres et un bureau. Nueva Living reconfirme prix, statut et conditions avant toute réservation.',
  'Verfügbarkeit und Preise laut Liste vom 27. Oktober 2026, vor der Reservierung bestätigt. Schlafzimmer, Bäder, Ebenen und bebaute Flächen stammen aus der Preisliste des Bauträgers von diesem Datum; sie hält fest, dass die Preise netto sind und weder MwSt. noch Grunderwerbsteuer oder sonstige Kosten enthalten, dass sie nur zur Information dient und nicht Vertragsbestandteil ist und dass der Verkäufer sie ändern kann, solange die erste Anzahlung nicht eingegangen ist. Die angegebene bebaute Fläche ist die Innenfläche der Liste; die Terrassenfläche addiert ihre überdachten und offenen Terrassen. Die Wohnflächen stammen aus dem Plan des Bauträgers für jede Wohnung, berechnet nach dem andalusischen Dekret 218/2005. Die Liste ordnet jeder Wohnung zwei Stellplätze und einen Abstellraum zu. Die Angaben stimmen überein, bis auf einen Unterschied, den wir nennen: Die Liste gibt Wohnung 3 drei Schlafzimmer, ihr Plan zeigt zwei Schlafzimmer und ein Arbeitszimmer. Nueva Living bestätigt Preis, Status und Bedingungen vor jeder Reservierung erneut.',
  'Наличие и цены по списку от 27 октября 2026 года, подтверждаются перед бронированием. Спальни, ванные, уровни и площади застройки взяты из прайс-листа застройщика на эту дату; в нём указано, что цены нетто и не включают НДС, налог на передачу имущества и другие сборы, что список носит информационный характер и не является частью договора и что продавец может изменить его до получения первоначального задатка. Указанная площадь застройки — внутренняя площадь из списка; площадь террас складывается из крытых и открытых террас. Полезные площади взяты из плана застройщика для каждой квартиры и рассчитаны по андалусскому декрету 218/2005. По списку каждой квартире полагаются два машино-места и кладовая. Данные совпадают, за одним отмеченным нами исключением: в списке у квартиры 3 три спальни, а на её плане — две спальни и кабинет. Nueva Living повторно подтверждает цену, статус и условия перед любым бронированием.',
  'التوافر والأسعار وفق القائمة المؤرخة 27 أكتوبر 2026، وتُؤكَّد قبل الحجز. وأعداد غرف النوم والحمّامات والمستويات والمساحات المبنية منقولة من قائمة أسعار المطوّر بذلك التاريخ، والتي تذكر أن الأسعار صافية ولا تشمل ضريبة القيمة المضافة ولا ضريبة نقل الملكية ولا رسوماً أخرى، وأنها لأغراض إعلامية فقط ولا تشكّل جزءاً من أي عقد، وأن للبائع تعديلها ما لم يُستلم العربون الأول. والمساحة المبنية المعروضة هي الرقم الداخلي في القائمة، ورقم التراسات يجمع تراساتها المسقوفة والمكشوفة. والمساحات الصافية مأخوذة من مخطط المطوّر لكل مسكن، ومحسوبة وفق المرسوم الأندلسي 218/2005. وتمنح القائمة كل مسكن موقفَي سيارات ومخزناً. والأرقام متطابقة باستثناء فرق واحد نذكره: تذكر القائمة ثلاث غرف نوم للمسكن 3، بينما يُظهر مخططه غرفتي نوم ومكتباً. وتعيد Nueva Living تأكيد السعر والحالة والشروط قبل أي حجز.',
  'Beschikbaarheid en prijzen volgens de lijst van 27 oktober 2026, bevestigd vóór reservering. Slaapkamers, badkamers, niveaus en bebouwde oppervlakten komen uit de prijslijst van de ontwikkelaar van die datum, die vermeldt dat de prijzen netto zijn en geen btw, overdrachtsbelasting of andere kosten bevatten, dat de lijst alleen ter informatie dient en geen deel uitmaakt van een contract, en dat de verkoper haar mag wijzigen zolang de eerste aanbetaling niet is ontvangen. De getoonde bebouwde oppervlakte is het binnencijfer van de lijst; het terrascijfer telt de overdekte en open terrassen op. De nuttige oppervlakten komen uit de plattegrond van de ontwikkelaar per woning, berekend volgens het Andalusische decreet 218/2005. De lijst kent elke woning twee parkeerplaatsen en een berging toe. De cijfers kloppen, op één verschil na dat wij noemen: de lijst geeft woning 3 drie slaapkamers, terwijl de plattegrond twee slaapkamers en een werkkamer tekent. Nueva Living bevestigt prijs, status en voorwaarden opnieuw vóór elke reservering.',
  'Dostępność i ceny według cennika z 27 października 2026 r., potwierdzane przed rezerwacją. Sypialnie, łazienki, poziomy i powierzchnie zabudowy przepisano z cennika dewelopera z tej daty, który podaje, że ceny są netto i nie obejmują VAT, podatku od przeniesienia własności ani innych opłat, że ma charakter wyłącznie informacyjny i nie stanowi części żadnej umowy oraz że sprzedawca może go zmienić, dopóki nie otrzyma pierwszej wpłaty. Podana powierzchnia zabudowy to wartość wewnętrzna z cennika; powierzchnia tarasów sumuje jego tarasy zadaszone i otwarte. Powierzchnie użytkowe pochodzą z rzutu dewelopera dla każdego mieszkania, obliczone zgodnie z andaluzyjskim dekretem 218/2005. Cennik przypisuje każdemu mieszkaniu dwa miejsca parkingowe i komórkę lokatorską. Dane są zgodne, z jedną różnicą, którą wskazujemy: cennik podaje dla mieszkania 3 trzy sypialnie, a jego rzut pokazuje dwie sypialnie i gabinet. Nueva Living ponownie potwierdza cenę, status i warunki przed każdą rezerwacją.',
  'Tilgjengelighet og priser etter listen datert 27. oktober 2026, bekreftet før reservasjon. Soverom, bad, plan og bebygde arealer er hentet fra utbyggerens prisliste fra den datoen, som sier at prisene er netto og ikke inkluderer mva, dokumentavgift eller andre kostnader, at den kun er til informasjon og ikke er del av noen kontrakt, og at selgeren kan endre den så lenge det første depositumet ikke er mottatt. Bebygd areal som vises, er listens innvendige tall; terrassetallet legger sammen de overbygde og åpne terrassene. Bruksarealene er hentet fra utbyggerens plantegning for hver bolig, beregnet etter det andalusiske dekretet 218/2005. Listen gir hver bolig to parkeringsplasser og en bod. Tallene stemmer, med én forskjell vi nevner: listen gir bolig 3 tre soverom, mens plantegningen viser to soverom og et kontor. Nueva Living bekrefter pris, status og vilkår på nytt før enhver reservasjon.',
  'Tillgänglighet och priser enligt listan daterad 27 oktober 2026, bekräftade före reservation. Sovrum, badrum, plan och byggytor är hämtade från exploatörens prislista från det datumet, som anger att priserna är netto och inte inkluderar IVA, överlåtelseskatt eller andra avgifter, att den endast är informativ och inte ingår i något avtal, och att säljaren får ändra den så länge den första handpenningen inte har mottagits. Den byggyta som visas är listans inomhussiffra; terrassiffran lägger ihop de överbyggda och öppna terrasserna. Nyttoytorna kommer från exploatörens planritning för varje bostad, beräknade enligt det andalusiska dekretet 218/2005. Listan ger varje bostad två parkeringsplatser och ett förråd. Siffrorna stämmer, med en skillnad som vi anger: listan ger bostad 3 tre sovrum, medan planritningen visar två sovrum och ett arbetsrum. Nueva Living bekräftar pris, status och villkor på nytt före varje reservation.')

SIZES = {
    'es': '{N%s} {U} construido, {N%s} {U} superficie útil, {N%s} {U} terrazas',
    'fr': '{N%s} {U} construit, {N%s} {U} surface utile, {N%s} {U} terrasses',
    'de': '{N%s} {U} bebaut, {N%s} {U} Wohnfläche, {N%s} {U} Terrassen',
    'ru': '{N%s} {U} застройка, {N%s} {U} полезная площадь, {N%s} {U} террасы',
    'ar': '{N%s} {U} مبنية، {N%s} {U} مساحة صافية، {N%s} {U} تراسات',
    'nl': '{N%s} {U} bebouwd, {N%s} {U} nuttige oppervlakte, {N%s} {U} terrassen',
    'pl': '{N%s} {U} powierzchnia zabudowy, {N%s} {U} powierzchnia użytkowa, {N%s} {U} tarasy',
    'no': '{N%s} {U} bebygd areal, {N%s} {U} bruksareal, {N%s} {U} terrasser',
    'sv': '{N%s} {U} byggyta, {N%s} {U} nyttoyta, {N%s} {U} terrasser',
}
for i, trio in enumerate((('138.95', '121.70', '72.03'), ('136.28', '117.99', '44.21'), ('165.85', '136.95', '38.99'))):
    a(f'.availability.units[{i}].size', *[SIZES[l] % trio for l in LOCS])

# ---- construction and payment -------------------------------------------------------------------
a('.constructionTimeline.headlineHtml', 'Dónde está <em>el edificio</em>', 'Où en est <em>l’immeuble</em>',
  'Wo das Gebäude <em>steht</em>', 'На каком этапе <em>здание</em>', 'أين وصل <em>المبنى</em>',
  'Waar het gebouw <em>staat</em>', 'Na jakim etapie <em>jest budynek</em>', 'Hvor bygget <em>står</em>', 'Var byggnaden <em>står</em>')
a('.constructionTimeline.points[0].year', 'Licencia', 'Permis', 'Genehmigung', 'Разрешение', 'الرخصة', 'Vergunning',
  'Pozwolenie', 'Tillatelse', 'Bygglov')
a('.constructionTimeline.points[0].label', 'Licencia de obra concedida', 'Permis de construire accordé', 'Baugenehmigung erteilt',
  'Разрешение на строительство получено', 'رخصة البناء ممنوحة', 'Bouwvergunning verleend', 'Pozwolenie na budowę wydane',
  'Byggetillatelse gitt', 'Bygglov beviljat')
a('.constructionTimeline.points[1].year', 'Junio de 2025', 'Juin 2025', 'Juni 2025', 'Июнь 2025', 'يونيو 2025', 'Juni 2025',
  'Czerwiec 2025', 'Juni 2025', 'Juni 2025')
a('.constructionTimeline.points[1].label', 'Inicio de las obras', 'Début des travaux', 'Baubeginn', 'Начало строительства',
  'بدء الأعمال', 'Start van de bouw', 'Rozpoczęcie budowy', 'Byggestart', 'Byggstart')
a('.constructionTimeline.points[2].year', 'T3 2027', 'T3 2027', 'Q3 2027', '3 кв. 2027', 'الربع الثالث 2027', 'K3 2027',
  'III kw. 2027', 'K3 2027', 'K3 2027')
a('.constructionTimeline.note',
  'El portal del promotor indica la licencia de obra como concedida, el inicio de las obras en junio de 2025 y la entrega en el tercer trimestre de 2027. Nueva Living solicita por escrito la licencia y la fecha contractual de entrega antes de cualquier pago, y que el contrato diga qué ocurre si la fecha se retrasa.',
  'Le portail du promoteur indique le permis de construire comme accordé, le début des travaux en juin 2025 et la livraison au troisième trimestre 2027. Nueva Living demande le permis et la date contractuelle de livraison par écrit avant tout versement, et que le contrat prévoie ce qui se passe en cas de retard.',
  'Das Portal des Bauträgers nennt die Baugenehmigung als erteilt, den Baubeginn im Juni 2025 und die Fertigstellung im dritten Quartal 2027. Nueva Living verlangt die Genehmigung und den vertraglichen Fertigstellungstermin schriftlich, bevor Geld fließt, und dass der Vertrag regelt, was bei einer Verzögerung gilt.',
  'На портале застройщика указано, что разрешение на строительство получено, работы начались в июне 2025 года, а завершение — в третьем квартале 2027 года. Nueva Living запрашивает разрешение и договорную дату сдачи в письменном виде до любых платежей, а также чтобы договор оговаривал последствия задержки.',
  'تذكر بوابة المطوّر أن رخصة البناء ممنوحة، وأن الأعمال بدأت في يونيو 2025، وأن الإنجاز في الربع الثالث من عام 2027. وتطلب Nueva Living الرخصة وتاريخ التسليم التعاقدي كتابةً قبل دفع أي مبلغ، وأن ينص العقد على ما يحدث إذا تأخر الموعد.',
  'Het portaal van de ontwikkelaar vermeldt de bouwvergunning als verleend, de start van de bouw in juni 2025 en de oplevering in het derde kwartaal van 2027. Nueva Living vraagt de vergunning en de contractuele opleverdatum schriftelijk op voordat er geld wordt betaald, en dat het contract regelt wat er gebeurt als de datum uitloopt.',
  'Portal dewelopera podaje, że pozwolenie na budowę zostało wydane, budowa ruszyła w czerwcu 2025 r., a zakończenie przewidziano na trzeci kwartał 2027 r. Nueva Living prosi o pozwolenie i umowny termin oddania na piśmie przed jakąkolwiek płatnością oraz o zapis w umowie na wypadek opóźnienia.',
  'Utbyggerens portal oppgir byggetillatelsen som gitt, byggestart i juni 2025 og ferdigstillelse i tredje kvartal 2027. Nueva Living ber om tillatelsen og den avtalte ferdigdatoen skriftlig før noen penger betales, og om at kontrakten sier hva som skjer om datoen glipper.',
  'Exploatörens portal anger bygglovet som beviljat, byggstarten i juni 2025 och färdigställandet till tredje kvartalet 2027. Nueva Living begär bygglovet och det avtalade färdigställandedatumet skriftligen innan några pengar betalas, och att avtalet anger vad som händer om datumet skjuts upp.')
a('.constructionTimeline.paymentTerms[0][1]', *[f'{{E10000}} + {t}' for t in TAX])
for i, pct in ((1, '30%'), (2, '20%'), (3, '50%')):
    a(f'.constructionTimeline.paymentTerms[{i}][1]', *[f'{pct} + {t}' for t in TAX])
a('.constructionTimeline.paymentTerms[0][2]', 'Reserva de la vivienda', 'Réservation du logement', 'Reserviert die Wohnung',
  'Бронирует квартиру', 'لحجز المسكن', 'Reserveert de woning', 'Rezerwuje mieszkanie', 'Reserverer boligen', 'Reserverar bostaden')
a('.constructionTimeline.paymentTerms[1][2]', 'A la firma, con la licencia de obra concedida', 'À la signature, le permis de construire étant accordé',
  'Bei Unterzeichnung, mit erteilter Baugenehmigung', 'При подписании, после получения разрешения на строительство',
  'عند التوقيع، بعد منح رخصة البناء', 'Bij ondertekening, met verleende bouwvergunning', 'Przy podpisaniu, po wydaniu pozwolenia na budowę',
  'Ved signering, med byggetillatelsen gitt', 'Vid undertecknandet, med bygglovet beviljat')
a('.constructionTimeline.paymentTerms[3][2]', 'Con la licencia de primera ocupación y la escritura', 'À l’obtention du certificat de conformité et à l’acte authentique',
  'Bei Erteilung der Bezugsgenehmigung und der notariellen Beurkundung', 'При получении лицензии на первое заселение и подписании купчей',
  'عند صدور رخصة الإشغال الأول وتوقيع سند الملكية', 'Bij de eerste bewoningsvergunning en de notariële akte',
  'Przy pozwoleniu na pierwsze użytkowanie i akcie notarialnym', 'Ved brukstillatelse og skjøte', 'Vid slutbesked och köpebrev')
a('.constructionTimeline.paymentTermsNote',
  'Según el calendario de pagos del promotor, que indica que a cada importe se añade el IVA. No dice si la reserva se descuenta del 30 %, ni cómo se garantizan las cantidades entregadas a cuenta, por lo que Nueva Living pide ambas cosas por escrito antes de que usted reserve.',
  'D’après l’échéancier du promoteur, qui précise que la TVA s’ajoute à chaque montant. Il ne dit pas si la réservation est déduite des 30 %, ni comment les sommes versées sont garanties ; Nueva Living demande donc les deux par écrit avant que vous ne réserviez.',
  'Nach dem Zahlungsplan des Bauträgers, der festhält, dass auf jeden Betrag die MwSt. aufgeschlagen wird. Er sagt nicht, ob die Reservierung auf die 30 % angerechnet wird oder wie Anzahlungen abgesichert sind; Nueva Living verlangt beides schriftlich, bevor Sie reservieren.',
  'По графику платежей застройщика, где указано, что к каждой сумме добавляется НДС. В нём не сказано, засчитывается ли бронь в 30 % и как гарантируются авансовые платежи, поэтому Nueva Living запрашивает и то и другое письменно до того, как вы забронируете квартиру.',
  'وفق جدول الدفعات الخاص بالمطوّر، الذي يذكر أن ضريبة القيمة المضافة تُضاف إلى كل مبلغ. ولا يذكر ما إذا كان مبلغ الحجز يُخصم من الـ30%، ولا كيف تُضمن الدفعات المقدّمة، لذا تطلب Nueva Living الأمرين كتابةً قبل أن تحجزوا.',
  'Volgens het betalingsschema van de ontwikkelaar, dat vermeldt dat op elk bedrag btw komt. Het zegt niet of de reservering van de 30% wordt afgetrokken, noch hoe vooruitbetalingen zijn gegarandeerd; Nueva Living vraagt beide schriftelijk op voordat u reserveert.',
  'Według harmonogramu płatności dewelopera, który podaje, że do każdej kwoty dolicza się VAT. Nie mówi on, czy opłata rezerwacyjna jest odliczana od 30%, ani jak zabezpieczone są wpłaty zaliczkowe, dlatego Nueva Living prosi o jedno i drugie na piśmie, zanim Państwo dokonają rezerwacji.',
  'Etter utbyggerens betalingsplan, som sier at mva kommer i tillegg til hvert beløp. Den sier ikke om reservasjonen trekkes fra de 30 %, eller hvordan forskuddsbetalinger er sikret, så Nueva Living ber om begge deler skriftlig før du reserverer.',
  'Enligt exploatörens betalningsplan, som anger att IVA läggs på varje belopp. Den anger inte om reservationen dras av från de 30 %, eller hur förskottsbetalningar är säkrade, så Nueva Living begär båda skriftligen innan ni reserverar.')

# ---- why ----------------------------------------------------------------------------------------
a('.why.copy',
  'Un edificio pequeño cerca de la playa en Benalmádena, con terrazas amplias y una zona wellness compartida por dieciséis viviendas.',
  'Un petit immeuble près de la plage à Benalmádena, avec de grandes terrasses et un espace bien-être partagé par seize logements.',
  'Ein kleines Gebäude nahe dem Strand in Benalmádena, mit großen Terrassen und einem Wellnessbereich für sechzehn Wohnungen.',
  'Небольшое здание у пляжа в Бенальмадене, с большими террасами и велнес-зоной на шестнадцать квартир.',
  'مبنى صغير قرب الشاطئ في بينالمادينا، بتراسات واسعة ومنطقة عافية يتشاركها ستة عشر مسكناً.',
  'Een klein gebouw bij het strand in Benalmádena, met ruime terrassen en een wellnessruimte voor zestien woningen.',
  'Niewielki budynek blisko plaży w Benalmádenie, z dużymi tarasami i strefą wellness dla szesnastu mieszkań.',
  'Et lite bygg nær stranden i Benalmádena, med store terrasser og et velværeområde som deles av seksten boliger.',
  'Ett litet hus nära stranden i Benalmádena, med stora terrasser och en wellnessavdelning som delas av sexton bostäder.')
a('.why.points[0][1]',
  'Compradores que buscan tres o cuatro dormitorios con una terraza amplia cerca de la playa en Benalmádena, como vivienda habitual o segunda residencia.',
  'Les acheteurs qui cherchent trois ou quatre chambres avec une grande terrasse près de la plage à Benalmádena, en résidence principale ou secondaire.',
  'Käufer, die drei oder vier Schlafzimmer mit großer Terrasse nahe dem Strand in Benalmádena suchen, als Hauptwohnsitz oder Zweitwohnung.',
  'Покупатели, которым нужны три или четыре спальни с большой террасой у пляжа в Бенальмадене — для постоянной жизни или как второй дом.',
  'المشترون الذين يبحثون عن ثلاث أو أربع غرف نوم مع تراس واسع قرب الشاطئ في بينالمادينا، للسكن الدائم أو كمنزل ثانٍ.',
  'Kopers die drie of vier slaapkamers met een groot terras bij het strand in Benalmádena zoeken, om er te wonen of als tweede woning.',
  'Kupujący, którzy szukają trzech lub czterech sypialni z dużym tarasem blisko plaży w Benalmádenie, do zamieszkania lub jako drugi dom.',
  'Kjøpere som ønsker tre eller fire soverom med stor terrasse nær stranden i Benalmádena, som fast bolig eller fritidsbolig.',
  'Köpare som söker tre eller fyra sovrum med stor terrass nära stranden i Benalmádena, som permanentbostad eller fritidsbostad.')
a('.why.points[1][1]',
  'Solo dieciséis viviendas comparten la piscina, el gimnasio, la sauna y la cocina exterior, y cada vivienda tiene dos plazas de garaje y un trastero.',
  'Seuls seize logements se partagent la piscine, la salle de sport, le sauna et la cuisine d’extérieur, et chaque logement a deux places de parking et une cave.',
  'Nur sechzehn Wohnungen teilen sich Pool, Fitnessraum, Sauna und Außenküche, und jede Wohnung hat zwei Stellplätze und einen Abstellraum.',
  'Бассейн, тренажёрный зал, сауну и летнюю кухню делят всего шестнадцать квартир, и у каждой два машино-места и кладовая.',
  'ستة عشر مسكناً فقط تتشارك المسبح والصالة الرياضية والساونا والمطبخ الخارجي، ولكل مسكن موقفا سيارات ومخزن.',
  'Slechts zestien woningen delen het zwembad, de fitnessruimte, de sauna en de buitenkeuken, en elke woning heeft twee parkeerplaatsen en een berging.',
  'Tylko szesnaście mieszkań dzieli basen, siłownię, saunę i kuchnię plenerową, a każde ma dwa miejsca parkingowe i komórkę lokatorską.',
  'Bare seksten boliger deler bassenget, treningsrommet, badstuen og utekjøkkenet, og hver bolig har to parkeringsplasser og en bod.',
  'Endast sexton bostäder delar poolen, gymmet, bastun och uteköket, och varje bostad har två parkeringsplatser och ett förråd.')
a('.why.points[2][1]',
  'El promotor sitúa el edificio a unos 300 metros de la playa de Malibú, en una de las últimas parcelas de la costa de Benalmádena.',
  'Le promoteur situe l’immeuble à environ 300 mètres de la plage de Malibú, sur l’une des dernières parcelles de la côte de Benalmádena.',
  'Der Bauträger verortet das Gebäude rund 300 Meter vom Strand von Malibú, auf einem der letzten Grundstücke an der Küste von Benalmádena.',
  'Застройщик указывает, что здание стоит примерно в 300 метрах от пляжа Малибу, на одном из последних участков на побережье Бенальмадены.',
  'يحدّد المطوّر موقع المبنى على بعد نحو 300 متر من شاطئ ماليبو، على إحدى آخر قطع الأرض في ساحل بينالمادينا.',
  'De ontwikkelaar situeert het gebouw op zo’n 300 meter van het strand van Malibú, op een van de laatste percelen aan de kust van Benalmádena.',
  'Deweloper lokalizuje budynek około 300 metrów od plaży Malibú, na jednej z ostatnich działek na wybrzeżu Benalmádeny.',
  'Utbyggeren plasserer bygget omkring 300 meter fra Malibú-stranden, på en av de siste tomtene ved kysten av Benalmádena.',
  'Exploatören placerar huset omkring 300 meter från Malibústranden, på en av de sista tomterna vid kusten i Benalmádena.')
a('.why.points[3][1]',
  'Trece de las dieciséis viviendas están reservadas en la lista de octubre de 2026, así que la elección está entre las tres que quedan.',
  'Treize des seize logements sont réservés sur la liste d’octobre 2026 ; le choix se fait donc entre les trois restants.',
  'Dreizehn der sechzehn Wohnungen sind auf der Liste vom Oktober 2026 reserviert, die Wahl besteht also zwischen den drei übrigen.',
  'В списке за октябрь 2026 года тринадцать из шестнадцати квартир забронированы, так что выбор — из трёх оставшихся.',
  'ثلاثة عشر من المساكن الستة عشر محجوزة في قائمة أكتوبر 2026، فالاختيار بين الثلاثة المتبقية.',
  'Dertien van de zestien woningen zijn gereserveerd op de lijst van oktober 2026, dus de keuze is tussen de drie die overblijven.',
  'Trzynaście z szesnastu mieszkań jest zarezerwowanych w cenniku z października 2026 r., więc wybór ogranicza się do trzech pozostałych.',
  'Tretten av de seksten boligene er reservert på listen fra oktober 2026, så valget står mellom de tre som gjenstår.',
  'Tretton av de sexton bostäderna är reserverade i listan från oktober 2026, så valet står mellan de tre som återstår.')

# ---- investment ---------------------------------------------------------------------------------
a('.investment.headlineHtml', 'Cómo <em>valorarlo</em>', 'Comment <em>l’envisager</em>', 'Wie man es <em>einordnet</em>',
  'Как это <em>оценить</em>', 'كيف <em>تقيّمونه</em>', 'Hoe u het <em>kunt bekijken</em>', 'Jak to <em>ocenić</em>',
  'Slik kan du <em>vurdere det</em>', 'Så kan ni <em>se på det</em>')
a('.investment.copy',
  'Puntos que conviene sopesar antes de reservar, sin ninguna promesa de rentabilidad futura.',
  'Des points à peser avant de réserver, sans aucune promesse de rendement futur.',
  'Punkte, die Sie vor der Reservierung abwägen sollten, ohne jedes Renditeversprechen.',
  'Что стоит взвесить перед бронированием — без каких-либо обещаний будущей доходности.',
  'نقاط تستحق الموازنة قبل الحجز، دون أي وعد بعوائد مستقبلية.',
  'Punten om af te wegen voordat u reserveert, zonder enige belofte van toekomstig rendement.',
  'Kwestie warte rozważenia przed rezerwacją, bez żadnych obietnic przyszłych zysków.',
  'Punkter verdt å vurdere før du reserverer, uten noe løfte om fremtidig avkastning.',
  'Punkter värda att väga in innan ni reserverar, utan några löften om framtida avkastning.')
a('.investment.cards[0][0]', 'Los impuestos no están incluidos', 'Les taxes ne sont pas comprises', 'Steuern sind nicht enthalten',
  'Налоги не включены', 'الضرائب غير مشمولة', 'Belastingen zijn niet inbegrepen', 'Podatki nie są wliczone',
  'Avgifter er ikke inkludert', 'Skatten ingår inte')
a('.investment.cards[0][1]',
  'Los precios de la lista son netos. Se suman el IVA, hoy del 10 % en vivienda nueva, y el impuesto de actos jurídicos documentados, además de los gastos de notaría y registro.',
  'Les prix de la liste sont nets. S’y ajoutent la TVA, actuellement de 10 % sur le neuf, et le droit de timbre, plus les frais de notaire et d’enregistrement.',
  'Die Listenpreise sind Nettopreise. Hinzu kommen die MwSt., derzeit 10 % auf Neubauten, und die Stempelsteuer sowie Notar- und Registerkosten.',
  'Цены в списке указаны нетто. К ним добавляются НДС, сейчас 10 % на новое жильё, и гербовый сбор, а также расходы на нотариуса и регистрацию.',
  'أسعار القائمة صافية. وتُضاف إليها ضريبة القيمة المضافة، وهي حالياً 10% على المساكن الجديدة، وضريبة الدمغة، إضافة إلى رسوم الموثّق والتسجيل.',
  'De lijstprijzen zijn netto. Daar komen btw bij, momenteel 10% op nieuwbouw, en zegelrecht, plus notaris- en registratiekosten.',
  'Ceny w cenniku są netto. Doliczany jest VAT, obecnie 10% na nowe mieszkania, oraz opłata skarbowa, a także koszty notariusza i rejestru.',
  'Listeprisene er netto. Mva, i dag 10 % på nye boliger, og dokumentavgift kommer i tillegg, pluss notar- og tinglysingsgebyrer.',
  'Listpriserna är netto. IVA, i dag 10 % på nyproduktion, och stämpelskatt tillkommer, plus notarie- och lagfartsavgifter.')
a('.investment.cards[1][0]', 'Tres viviendas, tres distribuciones', 'Trois logements, trois plans', 'Drei Wohnungen, drei Grundrisse',
  'Три квартиры, три планировки', 'ثلاثة مساكن، ثلاثة توزيعات', 'Drie woningen, drie indelingen', 'Trzy mieszkania, trzy układy',
  'Tre boliger, tre planløsninger', 'Tre bostäder, tre planlösningar')
a('.investment.cards[1][1]',
  'Una vivienda en dos niveles con terrazas en ambos, un ático en una planta y un ático dúplex: cada una es la última de su tipo en la lista.',
  'Un logement sur deux niveaux avec des terrasses à chacun, un penthouse de plain-pied et un penthouse duplex : chacun est le dernier de son type sur la liste.',
  'Eine Wohnung auf zwei Ebenen mit Terrassen auf beiden, ein Penthouse auf einer Ebene und ein Maisonette-Penthaus: Jede ist die letzte ihrer Art auf der Liste.',
  'Квартира на двух уровнях с террасами на обоих, одноуровневый пентхаус и двухуровневый пентхаус: каждая — последняя своего типа в списке.',
  'مسكن على مستويين بتراسات في كليهما، وبنتهاوس على مستوى واحد، وبنتهاوس دوبلكس: كل منها الأخير من نوعه في القائمة.',
  'Een woning op twee niveaus met terrassen op beide, een penthouse op één niveau en een duplex penthouse: elk is de laatste van zijn soort op de lijst.',
  'Mieszkanie na dwóch poziomach z tarasami na obu, jednopoziomowy penthouse i dwupoziomowy penthouse: każde jest ostatnim tego typu w cenniku.',
  'En bolig over to plan med terrasser på begge, en toppleilighet på ett plan og en toppleilighet over to plan: hver er den siste av sitt slag på listen.',
  'En bostad i två plan med terrasser på båda, en takvåning i ett plan och en takvåning i två plan: var och en är den sista av sitt slag i listan.')
a('.investment.cards[2][0]', 'La mitad en la escritura', 'La moitié à l’acte', 'Die Hälfte bei der Beurkundung', 'Половина — при купчей',
  'النصف عند سند الملكية', 'De helft bij de akte', 'Połowa przy akcie notarialnym', 'Halvparten ved skjøtet', 'Hälften vid tillträdet')
a('.investment.cards[2][1]',
  'La mitad del precio se paga con la licencia de primera ocupación y la escritura, tras la terminación, que el portal sitúa en el tercer trimestre de 2027.',
  'La moitié du prix est due au certificat de conformité et à l’acte authentique, après l’achèvement, que le portail situe au troisième trimestre 2027.',
  'Die Hälfte des Preises wird mit der Bezugsgenehmigung und der Beurkundung fällig, nach der Fertigstellung, die das Portal für das dritte Quartal 2027 angibt.',
  'Половина цены оплачивается при получении лицензии на первое заселение и подписании купчей, после завершения строительства, которое портал относит к третьему кварталу 2027 года.',
  'يُستحق نصف السعر عند صدور رخصة الإشغال الأول وتوقيع سند الملكية، بعد الإنجاز الذي تحدده البوابة في الربع الثالث من عام 2027.',
  'De helft van de prijs is verschuldigd bij de eerste bewoningsvergunning en de notariële akte, na de oplevering, die het portaal in het derde kwartaal van 2027 plaatst.',
  'Połowa ceny jest płatna przy pozwoleniu na pierwsze użytkowanie i akcie notarialnym, po zakończeniu budowy, które portal przewiduje na trzeci kwartał 2027 r.',
  'Halvparten av prisen forfaller ved brukstillatelse og skjøte, etter ferdigstillelsen, som portalen angir til tredje kvartal 2027.',
  'Hälften av priset förfaller vid slutbesked och köpebrev, efter färdigställandet, som portalen anger till tredje kvartalet 2027.')
a('.investment.cards[3][1]',
  'Adecuada como vivienda habitual o segunda residencia. El alquiler depende de las normas de la comunidad y de la licencia local, que comprobamos.',
  'Convient en résidence principale ou secondaire. La location dépend du règlement de copropriété et de la licence locale, que nous vérifions.',
  'Geeignet als Haupt- oder Zweitwohnsitz. Vermietung hängt von der Gemeinschaftsordnung und der örtlichen Lizenz ab, die wir prüfen.',
  'Подходит для постоянного проживания или как второй дом. Сдача в аренду зависит от правил сообщества и местной лицензии, которые мы проверяем.',
  'مناسب للسكن الدائم أو كمنزل ثانٍ. ويعتمد التأجير على قواعد الجمعية والترخيص المحلي، وهو ما نتحقق منه.',
  'Geschikt als vaste of tweede woning. Verhuur hangt af van het reglement van de VvE en de lokale vergunning, die wij controleren.',
  'Nadaje się do zamieszkania lub jako drugi dom. Wynajem zależy od regulaminu wspólnoty i lokalnej licencji, które sprawdzamy.',
  'Passer som fast bolig eller fritidsbolig. Utleie avhenger av sameiets regler og den lokale lisensen, som vi sjekker.',
  'Passar som permanentbostad eller fritidsbostad. Uthyrning beror på samfällighetens regler och den lokala licensen, som vi kontrollerar.')

# ---- trust dossier ------------------------------------------------------------------------------
a('.trustDossier.cards[0][0]', 'La licencia y la fecha', 'Le permis et la date', 'Genehmigung und Termin', 'Разрешение и сроки',
  'الرخصة والموعد', 'De vergunning en de datum', 'Pozwolenie i termin', 'Tillatelsen og datoen', 'Bygglovet och datumet')
a('.trustDossier.cards[0][1]',
  'El portal indica la licencia como concedida y la entrega en el tercer trimestre de 2027. Pedimos por escrito la propia licencia y la fecha contractual.',
  'Le portail indique le permis comme accordé et la livraison au troisième trimestre 2027. Nous demandons par écrit le permis lui-même et la date contractuelle.',
  'Das Portal nennt die Genehmigung als erteilt und die Fertigstellung im dritten Quartal 2027. Wir verlangen die Genehmigung selbst und den vertraglichen Termin schriftlich.',
  'Портал указывает, что разрешение получено, а сдача — в третьем квартале 2027 года. Мы запрашиваем само разрешение и договорную дату в письменном виде.',
  'تذكر البوابة أن الرخصة ممنوحة وأن التسليم في الربع الثالث من عام 2027. ونطلب الرخصة نفسها والموعد التعاقدي كتابةً.',
  'Het portaal vermeldt de vergunning als verleend en de oplevering in het derde kwartaal van 2027. Wij vragen de vergunning zelf en de contractuele datum schriftelijk op.',
  'Portal podaje, że pozwolenie zostało wydane, a oddanie nastąpi w trzecim kwartale 2027 r. Prosimy na piśmie o samo pozwolenie i umowny termin.',
  'Portalen oppgir tillatelsen som gitt og ferdigstillelse i tredje kvartal 2027. Vi ber om selve tillatelsen og den avtalte datoen skriftlig.',
  'Portalen anger bygglovet som beviljat och färdigställandet till tredje kvartalet 2027. Vi begär själva bygglovet och det avtalade datumet skriftligen.')
a('.trustDossier.cards[1][0]', 'Dormitorios de la vivienda 3', 'Les chambres du logement 3', 'Schlafzimmer in Wohnung 3',
  'Спальни в квартире 3', 'غرف النوم في المسكن 3', 'Slaapkamers in woning 3', 'Sypialnie w mieszkaniu 3',
  'Soverom i bolig 3', 'Sovrum i bostad 3')
a('.trustDossier.cards[1][1]',
  'La lista de precios cuenta tres dormitorios en la vivienda 3; su plano dibuja dos dormitorios y un despacho. Confirmamos cuál es el correcto antes de la reserva.',
  'La liste de prix compte trois chambres dans le logement 3 ; son plan dessine deux chambres et un bureau. Nous confirmons laquelle prévaut avant la réservation.',
  'Die Preisliste zählt drei Schlafzimmer in Wohnung 3; ihr Plan zeigt zwei Schlafzimmer und ein Arbeitszimmer. Wir klären vor der Reservierung, was gilt.',
  'В прайс-листе у квартиры 3 три спальни; на её плане — две спальни и кабинет. Мы уточняем, что верно, до бронирования.',
  'تذكر قائمة الأسعار ثلاث غرف نوم في المسكن 3، بينما يُظهر مخططه غرفتي نوم ومكتباً. ونؤكد الصحيح قبل الحجز.',
  'De prijslijst telt drie slaapkamers in woning 3; de plattegrond tekent twee slaapkamers en een werkkamer. Wij bevestigen vóór de reservering wat klopt.',
  'Cennik podaje trzy sypialnie w mieszkaniu 3; jego rzut pokazuje dwie sypialnie i gabinet. Przed rezerwacją potwierdzamy, co jest właściwe.',
  'Prislisten oppgir tre soverom i bolig 3; plantegningen viser to soverom og et kontor. Vi bekrefter hva som gjelder før reservasjon.',
  'Prislistan anger tre sovrum i bostad 3; planritningen visar två sovrum och ett arbetsrum. Vi bekräftar vad som gäller före reservationen.')
a('.trustDossier.cards[2][1]',
  'El calendario de pagos no dice cómo se garantizan las cantidades entregadas a cuenta. Pedimos ver la garantía antes de cualquier pago.',
  'L’échéancier ne dit pas comment les sommes versées sont garanties. Nous demandons à voir la garantie avant tout versement.',
  'Der Zahlungsplan sagt nicht, wie Anzahlungen abgesichert sind. Wir verlangen, die Bürgschaft vor jeder Zahlung zu sehen.',
  'В графике платежей не сказано, как гарантируются авансовые платежи. Мы просим показать гарантию до любого платежа.',
  'لا يذكر جدول الدفعات كيف تُضمن الدفعات المقدّمة. ونطلب الاطلاع على الضمان قبل أي دفعة.',
  'Het betalingsschema zegt niet hoe vooruitbetalingen zijn gegarandeerd. Wij vragen de garantie te zien vóór elke betaling.',
  'Harmonogram płatności nie mówi, jak zabezpieczone są wpłaty zaliczkowe. Prosimy o wgląd w gwarancję przed każdą płatnością.',
  'Betalingsplanen sier ikke hvordan forskuddsbetalinger er sikret. Vi ber om å se garantien før enhver betaling.',
  'Betalningsplanen anger inte hur förskottsbetalningar är säkrade. Vi begär att få se garantin före varje betalning.')
a('.trustDossier.cards[3][1]',
  'Las imágenes están generadas por ordenador e ilustran el diseño. Los planos son planos comerciales que, según el promotor, pueden cambiar.',
  'Les images sont générées par ordinateur et illustrent le projet. Les plans sont des plans commerciaux que le promoteur dit susceptibles de changer.',
  'Die Bilder sind computergeneriert und veranschaulichen den Entwurf. Die Pläne sind Verkaufspläne, die sich laut Bauträger ändern können.',
  'Изображения созданы на компьютере и иллюстрируют проект. Планы — коммерческие, и, по словам застройщика, могут измениться.',
  'الصور مولَّدة بالحاسوب وتوضّح التصميم. والمخططات مخططات بيع يقول المطوّر إنها قد تتغير.',
  'De beelden zijn computergegenereerd en illustreren het ontwerp. De plattegronden zijn verkooptekeningen die volgens de ontwikkelaar kunnen wijzigen.',
  'Obrazy są wizualizacjami komputerowymi i ilustrują projekt. Rzuty to plany sprzedażowe, które według dewelopera mogą się zmienić.',
  'Bildene er datagenererte og illustrerer prosjektet. Plantegningene er salgstegninger som utbyggeren sier kan endres.',
  'Bilderna är datorgenererade och illustrerar projektet. Planritningarna är försäljningsritningar som exploatören säger kan ändras.')

# ---- architecture -------------------------------------------------------------------------------
a('.architecture.headlineHtml', 'Terrazas <em>ladera abajo</em>', 'Des terrasses <em>en descendant la colline</em>',
  'Terrassen <em>den Hang hinab</em>', 'Террасы <em>вниз по склону</em>', 'تراسات <em>على امتداد المنحدر</em>',
  'Terrassen <em>langs de helling</em>', 'Tarasy <em>w dół zbocza</em>', 'Terrasser <em>nedover åssiden</em>',
  'Terrasser <em>nedför sluttningen</em>')
a('.architecture.copy[0]',
  'El edificio desciende por la pendiente en largas terrazas bajo cubiertas inclinadas de poca pendiente, de modo que la mayoría de las viviendas se abren a una terraza profunda orientada al mar. El folleto describe grandes ventanales que difuminan el límite entre interior y exterior.',
  'L’immeuble descend la pente en longues terrasses sous des toits à faible pente, si bien que la plupart des logements ouvrent sur une terrasse profonde face à la mer. La brochure décrit de grandes baies qui effacent la limite entre intérieur et extérieur.',
  'Das Gebäude stuft sich in langen Terrassen unter flach geneigten Dächern den Hang hinab, sodass sich die meisten Wohnungen zu einer tiefen Terrasse zum Meer öffnen. Die Broschüre beschreibt große Fenster, die die Grenze zwischen innen und außen aufheben.',
  'Здание спускается по склону длинными террасами под пологими скатными крышами, поэтому большинство квартир выходят на глубокую террасу с видом на море. В буклете описаны большие окна, стирающие границу между домом и улицей.',
  'ينحدر المبنى مع المنحدر في تراسات طويلة تحت أسقف مائلة قليلاً، فتنفتح معظم المساكن على تراس عميق مواجه للبحر. ويصف الكتيّب نوافذ كبيرة تُذيب الحد بين الداخل والخارج.',
  'Het gebouw daalt in lange terrassen langs de helling af onder flauw hellende daken, zodat de meeste woningen uitkomen op een diep terras richting zee. De brochure beschrijft grote ramen die de grens tussen binnen en buiten laten vervagen.',
  'Budynek schodzi po zboczu długimi tarasami pod łagodnie nachylonymi dachami, dzięki czemu większość mieszkań otwiera się na głęboki taras z widokiem na morze. Broszura opisuje duże okna zacierające granicę między wnętrzem a zewnętrzem.',
  'Bygningen trappes ned skråningen i lange terrasser under slake saltak, slik at de fleste boligene åpner seg mot en dyp terrasse mot havet. Brosjyren beskriver store vinduer som visker ut grensen mellom ute og inne.',
  'Byggnaden trappas ned längs sluttningen i långa terrasser under flacka sadeltak, så att de flesta bostäderna öppnar sig mot en djup terrass mot havet. Broschyren beskriver stora fönster som suddar ut gränsen mellan ute och inne.')
a('.architecture.copy[1]',
  'Junto a la piscina, un edificio wellness independiente alberga el gimnasio y la sauna, con la cocina exterior y la zona chill-out delante, como muestran el plano de la parcela y el folleto.',
  'À côté de la piscine, un bâtiment bien-être séparé abrite la salle de sport et le sauna, avec la cuisine d’extérieur et l’espace détente devant, comme le montrent le plan de masse et la brochure.',
  'Neben dem Pool beherbergt ein eigenes Wellnessgebäude den Fitnessraum und die Sauna, davor die Außenküche und die Chill-out-Zone, wie Lageplan und Broschüre zeigen.',
  'Рядом с бассейном отдельный велнес-корпус с тренажёрным залом и сауной, перед ним летняя кухня и зона отдыха — так показано на генплане и в буклете.',
  'بجوار المسبح، يضم مبنى عافية منفصل الصالة الرياضية والساونا، وأمامه المطبخ الخارجي ومنطقة الاسترخاء، كما يُظهر مخطط الموقع والكتيّب.',
  'Naast het zwembad herbergt een apart wellnessgebouw de fitnessruimte en de sauna, met de buitenkeuken en de chill-outzone ervoor, zoals de situatietekening en de brochure laten zien.',
  'Obok basenu osobny budynek wellness mieści siłownię i saunę, a przed nim kuchnię plenerową i strefę chill-out, jak pokazują plan działki i broszura.',
  'Ved siden av bassenget rommer et eget velværebygg treningsrommet og badstuen, med utekjøkkenet og chill-out-området foran, slik situasjonsplanen og brosjyren viser.',
  'Bredvid poolen rymmer en separat wellnessbyggnad gymmet och bastun, med uteköket och chill-out-ytan framför, så som situationsplanen och broschyren visar.')
a('.architecture.highlights[0]',
  'Dieciséis viviendas en un solo edificio: viviendas en dos niveles en la parte baja de la pendiente, apartamentos encima y áticos bajo la cubierta.',
  'Seize logements dans un seul immeuble : des logements sur deux niveaux en bas de la pente, des appartements au-dessus et des penthouses sous le toit.',
  'Sechzehn Wohnungen in einem Gebäude: Wohnungen auf zwei Ebenen am Fuß des Hangs, darüber Etagenwohnungen und unter dem Dach Penthäuser.',
  'Шестнадцать квартир в одном здании: двухуровневые квартиры в нижней части склона, над ними квартиры и под крышей пентхаусы.',
  'ستة عشر مسكناً في مبنى واحد: مساكن على مستويين في أسفل المنحدر، وشقق فوقها، وبنتهاوسات تحت السقف.',
  'Zestien woningen in één gebouw: woningen op twee niveaus onderaan de helling, appartementen erboven en penthouses onder het dak.',
  'Szesnaście mieszkań w jednym budynku: dwupoziomowe u dołu zbocza, mieszkania nad nimi i penthouse’y pod dachem.',
  'Seksten boliger i ett bygg: boliger over to plan nederst i skråningen, leiligheter over dem og toppleiligheter under taket.',
  'Sexton bostäder i en byggnad: bostäder i två plan längst ned i sluttningen, lägenheter ovanför och takvåningar under taket.')
a('.architecture.highlights[1]',
  'Terrazas de {N38.99} a {N72.03} {U} en las tres viviendas disponibles, con el mismo porcelánico que los suelos interiores.',
  'Des terrasses de {N38.99} à {N72.03} {U} sur les trois logements disponibles, dans le même grès cérame que les sols intérieurs.',
  'Terrassen von {N38.99} bis {N72.03} {U} bei den drei freien Wohnungen, mit demselben Feinsteinzeug wie die Böden innen.',
  'Террасы от {N38.99} до {N72.03} {U} у трёх свободных квартир, с тем же керамогранитом, что и полы внутри.',
  'تراسات من {N38.99} إلى {N72.03} {U} في المساكن الثلاثة المتاحة، مكسوّة بالبورسلين نفسه المستخدم في الأرضيات الداخلية.',
  'Terrassen van {N38.99} tot {N72.03} {U} bij de drie beschikbare woningen, met dezelfde keramische tegels als de vloeren binnen.',
  'Tarasy od {N38.99} do {N72.03} {U} w trzech dostępnych mieszkaniach, wyłożone tym samym gresem co podłogi wewnątrz.',
  'Terrasser på {N38.99} til {N72.03} {U} på de tre ledige boligene, med de samme porselensflisene som gulvene inne.',
  'Terrasser på {N38.99} till {N72.03} {U} i de tre lediga bostäderna, med samma porslinsplattor som golven inomhus.')
a('.architecture.highlights[2]',
  'Dos plazas de garaje y un trastero con cada vivienda, y preinstalación para cargar un coche eléctrico.',
  'Deux places de parking et une cave avec chaque logement, et une pré-installation pour recharger une voiture électrique.',
  'Zwei Stellplätze und ein Abstellraum zu jeder Wohnung sowie eine Vorinstallation zum Laden eines Elektroautos.',
  'Два машино-места и кладовая с каждой квартирой и подготовка для зарядки электромобиля.',
  'موقفا سيارات ومخزن مع كل مسكن، وتمديدات مسبقة لشحن السيارة الكهربائية.',
  'Twee parkeerplaatsen en een berging bij elke woning, en voorbereiding voor het laden van een elektrische auto.',
  'Dwa miejsca parkingowe i komórka lokatorska przy każdym mieszkaniu oraz przygotowanie do ładowania samochodu elektrycznego.',
  'To parkeringsplasser og en bod med hver bolig, og forberedt for lading av elbil.',
  'Två parkeringsplatser och ett förråd till varje bostad, och förberett för laddning av elbil.')
a('.architecture.highlights[3]',
  'Recinto completamente cerrado con control de acceso peatonal y de vehículos, y ascensores a todas las plantas.',
  'Un ensemble entièrement clos avec contrôle d’accès des piétons et des véhicules, et des ascenseurs à tous les étages.',
  'Eine vollständig umzäunte Anlage mit Zugangskontrolle für Fußgänger und Fahrzeuge und Aufzügen zu allen Etagen.',
  'Полностью огороженный комплекс с контролем доступа для пешеходов и автомобилей и лифтами на все этажи.',
  'مجمع مسوّر بالكامل مع مراقبة دخول المشاة والمركبات، ومصاعد إلى جميع الطوابق.',
  'Een volledig omheind complex met toegangscontrole voor voetgangers en voertuigen, en liften naar alle verdiepingen.',
  'Całkowicie ogrodzony kompleks z kontrolą dostępu pieszych i pojazdów oraz windami na wszystkie piętra.',
  'Et helt inngjerdet anlegg med adgangskontroll for gående og kjøretøy, og heiser til alle etasjer.',
  'Ett helt inhägnat område med tillträdeskontroll för gående och fordon, och hissar till alla våningar.')

# ---- lifestyle ----------------------------------------------------------------------------------
a('.lifestyle.headlineHtml', 'Piscina, gimnasio <em>y sauna</em>', 'Piscine, salle de sport <em>et sauna</em>',
  'Pool, Fitnessraum <em>und Sauna</em>', 'Бассейн, тренажёрный зал <em>и сауна</em>', 'مسبح وصالة رياضية <em>وساونا</em>',
  'Zwembad, fitnessruimte <em>en sauna</em>', 'Basen, siłownia <em>i sauna</em>', 'Basseng, treningsrom <em>og badstue</em>',
  'Pool, gym <em>och bastu</em>')
a('.lifestyle.copy',
  'Zonas comunes compartidas por dieciséis viviendas, en una ladera a un corto paseo por encima de la playa.',
  'Des espaces communs partagés par seize logements, à flanc de colline, à quelques pas au-dessus de la plage.',
  'Gemeinschaftsbereiche für sechzehn Wohnungen, an einem Hang nur einen kurzen Spaziergang oberhalb des Strandes.',
  'Общие зоны на шестнадцать квартир, на склоне в нескольких минутах ходьбы над пляжем.',
  'مرافق مشتركة يتشاركها ستة عشر مسكناً، على سفح تلة على مسافة قصيرة سيراً فوق الشاطئ.',
  'Gemeenschappelijke ruimten voor zestien woningen, op een helling op korte loopafstand boven het strand.',
  'Części wspólne dla szesnastu mieszkań, na zboczu, kilka minut spacerem nad plażą.',
  'Fellesområder for seksten boliger, i en åsside en kort spasertur ovenfor stranden.',
  'Gemensamma ytor för sexton bostäder, i en sluttning en kort promenad ovanför stranden.')
a('.lifestyle.panels[0][1]',
  'Una piscina de cloración salina con pared de vidrio e iluminación subacuática, y una cocina exterior con barbacoa y zona chill-out junto a ella.',
  'Une piscine à électrolyse au sel avec paroi vitrée et éclairage subaquatique, et une cuisine d’extérieur avec barbecue et espace détente à côté.',
  'Ein Salzwasserpool mit Glaswand und Unterwasserbeleuchtung und daneben eine Außenküche mit Grill und Chill-out-Zone.',
  'Бассейн с солевой очисткой, стеклянной стенкой и подводной подсветкой, а рядом летняя кухня с барбекю и зоной отдыха.',
  'مسبح بالتعقيم الملحي بجدار زجاجي وإضاءة تحت الماء، وبجواره مطبخ خارجي مع شواء ومنطقة استرخاء.',
  'Een zoutwaterzwembad met glazen wand en onderwaterverlichting, met ernaast een buitenkeuken met barbecue en chill-outzone.',
  'Basen z chlorowaniem solnym, szklaną ścianą i podwodnym oświetleniem, a obok kuchnia plenerowa z grillem i strefą chill-out.',
  'Et saltvannsbasseng med glassvegg og undervannsbelysning, og ved siden av et utekjøkken med grill og chill-out-område.',
  'En saltvattenpool med glasvägg och undervattensbelysning, och bredvid ett utekök med grill och chill-out-yta.')
a('.lifestyle.panels[1][1]',
  'Un gimnasio con grandes ventanales y la maquinaria más reciente, una sauna finlandesa con vestuario y ducha, y una zona de relajación.',
  'Une salle de sport aux grandes baies avec des appareils récents, un sauna finlandais avec vestiaire et douche, et un espace de détente.',
  'Ein Fitnessraum mit großen Fenstern und neuesten Geräten, eine finnische Sauna mit Umkleide und Dusche und ein Ruhebereich.',
  'Тренажёрный зал с большими окнами и новейшими тренажёрами, финская сауна с раздевалкой и душем и зона релаксации.',
  'صالة رياضية بنوافذ كبيرة وأحدث الأجهزة، وساونا فنلندية مع غرفة تبديل ملابس ودُش، ومنطقة استرخاء.',
  'Een fitnessruimte met grote ramen en de nieuwste toestellen, een Finse sauna met kleedruimte en douche, en een relaxruimte.',
  'Siłownia z dużymi oknami i najnowszym sprzętem, fińska sauna z przebieralnią i prysznicem oraz strefa relaksu.',
  'Et treningsrom med store vinduer og det nyeste utstyret, en finsk badstue med garderobe og dusj, og et hvileområde.',
  'Ett gym med stora fönster och den senaste utrustningen, en finsk bastu med omklädningsrum och dusch, och en avslappningsyta.')
a('.lifestyle.panels[2][1]',
  'El promotor sitúa el edificio a unos 300 metros de la playa de Malibú, en la costa de Benalmádena, con servicios y buenas conexiones cerca.',
  'Le promoteur situe l’immeuble à environ 300 mètres de la plage de Malibú, sur la côte de Benalmádena, avec commerces, services et bonnes liaisons à proximité.',
  'Der Bauträger verortet das Gebäude rund 300 Meter vom Strand von Malibú an der Küste von Benalmádena, mit Versorgung und guten Verbindungen in der Nähe.',
  'Застройщик указывает, что здание находится примерно в 300 метрах от пляжа Малибу на побережье Бенальмадены, рядом с инфраструктурой и хорошим транспортным сообщением.',
  'يحدّد المطوّر موقع المبنى على بعد نحو 300 متر من شاطئ ماليبو في ساحل بينالمادينا، وبالقرب منه خدمات ومواصلات جيدة.',
  'De ontwikkelaar situeert het gebouw op zo’n 300 meter van het strand van Malibú aan de kust van Benalmádena, met voorzieningen en goede verbindingen dichtbij.',
  'Deweloper lokalizuje budynek około 300 metrów od plaży Malibú na wybrzeżu Benalmádeny, z usługami i dobrą komunikacją w pobliżu.',
  'Utbyggeren plasserer bygget omkring 300 meter fra Malibú-stranden ved kysten av Benalmádena, med servicetilbud og gode forbindelser i nærheten.',
  'Exploatören placerar huset omkring 300 meter från Malibústranden vid kusten i Benalmádena, med service och goda förbindelser i närheten.')

# ---- private viewing ----------------------------------------------------------------------------
a('.privateViewing.headlineHtml', 'Vea <em>la parcela y las vistas</em>', 'Voyez <em>la parcelle et la vue</em>',
  'Sehen Sie <em>Grundstück und Aussicht</em>', 'Посмотрите <em>участок и виды</em>', 'شاهدوا <em>قطعة الأرض والإطلالات</em>',
  'Bekijk <em>het perceel en het uitzicht</em>', 'Zobaczą Państwo <em>działkę i widoki</em>', 'Se <em>tomten og utsikten</em>',
  'Se <em>tomten och utsikten</em>')
a('.privateViewing.copy',
  'El edificio está en construcción, así que la visita trata de la parcela, de las vistas desde cada nivel y del paseo hasta la playa.',
  'L’immeuble est en construction ; la visite porte donc sur la parcelle, la vue depuis chaque niveau et la marche jusqu’à la plage.',
  'Das Gebäude ist im Bau, bei einer Besichtigung geht es also um das Grundstück, die Aussicht von jeder Ebene und den Weg zum Strand.',
  'Здание строится, поэтому визит — это участок, виды с каждого уровня и прогулка до пляжа.',
  'المبنى قيد الإنشاء، لذا تتعلق الزيارة بقطعة الأرض والإطلالة من كل مستوى والطريق سيراً إلى الشاطئ.',
  'Het gebouw is in aanbouw, dus een bezoek gaat over het perceel, het uitzicht vanaf elk niveau en de wandeling naar het strand.',
  'Budynek jest w budowie, więc wizyta dotyczy działki, widoku z każdego poziomu i spaceru na plażę.',
  'Bygget er under oppføring, så en visning handler om tomten, utsikten fra hvert plan og gåturen til stranden.',
  'Huset är under uppförande, så en visning handlar om tomten, utsikten från varje plan och promenaden till stranden.')
a('.privateViewing.insights[0][1]',
  'Vea cómo se asienta el edificio en la pendiente y qué ve cada una de las tres viviendas.',
  'Voyez comment l’immeuble s’inscrit dans la pente et ce que voit chacun des trois logements.',
  'Sehen Sie, wie das Gebäude am Hang liegt und wohin jede der drei Wohnungen blickt.',
  'Посмотрите, как здание стоит на склоне и какой вид открывается из каждой из трёх квартир.',
  'شاهدوا كيف يستقر المبنى على المنحدر وما الذي يطل عليه كل من المساكن الثلاثة.',
  'Zie hoe het gebouw op de helling ligt en waar elk van de drie woningen op uitkijkt.',
  'Zobaczą Państwo, jak budynek leży na zboczu i na co wychodzi każde z trzech mieszkań.',
  'Se hvordan bygget ligger i skråningen og hva hver av de tre boligene ser ut mot.',
  'Se hur huset ligger i sluttningen och vad var och en av de tre bostäderna ser ut mot.')
a('.privateViewing.insights[1][1]',
  'Baje andando hasta la playa de Malibú y cronometre el paseo.',
  'Descendez à pied jusqu’à la plage de Malibú et chronométrez le trajet.',
  'Gehen Sie zu Fuß zum Strand von Malibú hinunter und stoppen Sie die Zeit.',
  'Спуститесь пешком к пляжу Малибу и засеките время.',
  'انزلوا سيراً إلى شاطئ ماليبو واحسبوا الوقت.',
  'Loop naar het strand van Malibú en neem de tijd op.',
  'Proszę zejść pieszo na plażę Malibú i zmierzyć czas.',
  'Gå ned til Malibú-stranden og ta tiden.',
  'Gå ned till Malibústranden och ta tid.')
a('.privateViewing.insights[2][1]',
  'La licencia, el calendario de pagos y el contrato, antes de firmar nada.',
  'Le permis, l’échéancier et le contrat, avant toute signature.',
  'Genehmigung, Zahlungsplan und Vertrag, bevor etwas unterschrieben wird.',
  'Разрешение, график платежей и договор — до того, как что-либо подписано.',
  'الرخصة وجدول الدفعات والعقد، قبل توقيع أي شيء.',
  'De vergunning, het betalingsschema en het contract, voordat er iets wordt getekend.',
  'Pozwolenie, harmonogram płatności i umowa, zanim cokolwiek zostanie podpisane.',
  'Tillatelsen, betalingsplanen og kontrakten, før noe signeres.',
  'Bygglovet, betalningsplanen och avtalet, innan något skrivs under.')

# ---- location -----------------------------------------------------------------------------------
a('.location.headlineHtml', 'Benalmádena, <em>sobre la playa</em>', 'Benalmádena, <em>au-dessus de la plage</em>',
  'Benalmádena, <em>über dem Strand</em>', 'Бенальмадена, <em>над пляжем</em>', 'بينالمادينا، <em>فوق الشاطئ</em>',
  'Benalmádena, <em>boven het strand</em>', 'Benalmádena, <em>nad plażą</em>', 'Benalmádena, <em>over stranden</em>',
  'Benalmádena, <em>ovanför stranden</em>')
a('.location.copy',
  'En la costa de Benalmádena, en una ladera por encima de la carretera de la costa N-340. El folleto del promotor indica unos 300 metros hasta la playa de Malibú. Los documentos no dan dirección, así que el mapa muestra la posición marcada en el plano de situación del promotor, no una parcela topografiada.',
  'Sur la côte de Benalmádena, à flanc de colline au-dessus de la route côtière N-340. La brochure du promoteur indique environ 300 mètres jusqu’à la plage de Malibú. Les documents ne donnent pas d’adresse ; la carte montre donc la position marquée sur le plan de situation du promoteur, et non une parcelle relevée.',
  'An der Küste von Benalmádena, an einem Hang oberhalb der Küstenstraße N-340. Die Broschüre des Bauträgers nennt rund 300 Meter bis zum Strand von Malibú. Die Unterlagen nennen keine Adresse, die Karte zeigt daher die im Lageplan des Bauträgers markierte Position, kein vermessenes Grundstück.',
  'На побережье Бенальмадены, на склоне над прибрежной дорогой N-340. В буклете застройщика указано около 300 метров до пляжа Малибу. Адреса в документах нет, поэтому на карте показано место, отмеченное на ситуационном плане застройщика, а не геодезически привязанный участок.',
  'في ساحل بينالمادينا، على سفح تلة فوق الطريق الساحلي N-340. ويذكر كتيّب المطوّر نحو 300 متر إلى شاطئ ماليبو. ولا تذكر الوثائق عنواناً، لذا تُظهر الخريطة الموقع المحدد في مخطط الموقع الخاص بالمطوّر، لا قطعة أرض مسّاحة.',
  'Aan de kust van Benalmádena, op een helling boven de kustweg N-340. De brochure van de ontwikkelaar noemt zo’n 300 meter tot het strand van Malibú. De documenten geven geen adres, dus de kaart toont de positie die op de situatiekaart van de ontwikkelaar is aangegeven, geen ingemeten perceel.',
  'Na wybrzeżu Benalmádeny, na zboczu nad nadmorską drogą N-340. Broszura dewelopera podaje około 300 metrów do plaży Malibú. Dokumenty nie podają adresu, więc mapa pokazuje miejsce zaznaczone na planie sytuacyjnym dewelopera, a nie wymierzoną działkę.',
  'Ved kysten av Benalmádena, i en åsside ovenfor kystveien N-340. Utbyggerens brosjyre oppgir omkring 300 meter til Malibú-stranden. Dokumentene gir ingen adresse, så kartet viser posisjonen som er markert på utbyggerens situasjonskart, ikke en oppmålt tomt.',
  'Vid kusten i Benalmádena, i en sluttning ovanför kustvägen N-340. Exploatörens broschyr anger omkring 300 meter till Malibústranden. Dokumenten ger ingen adress, så kartan visar läget som är markerat på exploatörens lägesplan, inte en uppmätt tomt.')
a('.location.mapLabelHtml', 'Benalmádena, <em>Costa del Sol</em>', 'Benalmádena, <em>Costa del Sol</em>', 'Benalmádena, <em>Costa del Sol</em>',
  'Бенальмадена, <em>Коста-дель-Соль</em>', 'بينالمادينا، <em>كوستا ديل سول</em>', 'Benalmádena, <em>Costa del Sol</em>',
  'Benalmádena, <em>Costa del Sol</em>', 'Benalmádena, <em>Costa del Sol</em>', 'Benalmádena, <em>Costa del Sol</em>')
a('.location.mapLabelPlain', 'Benalmádena, Costa del Sol', 'Benalmádena, Costa del Sol', 'Benalmádena, Costa del Sol',
  'Бенальмадена, Коста-дель-Соль', 'بينالمادينا، كوستا ديل سول', 'Benalmádena, Costa del Sol', 'Benalmádena, Costa del Sol',
  'Benalmádena, Costa del Sol', 'Benalmádena, Costa del Sol')
a('.location.distances[0][0]', 'Playa de Malibú', 'Plage de Malibú', 'Strand von Malibú', 'Пляж Малибу', 'شاطئ ماليبو',
  'Strand van Malibú', 'Plaża Malibú', 'Malibú-stranden', 'Malibústranden')
a('.location.distances[0][1]', 'Aprox. 300 m', 'Env. 300 m', 'Ca. 300 m', 'Около 300 м', 'نحو 300 م', 'Ca. 300 m',
  'Ok. 300 m', 'Ca. 300 m', 'Ca 300 m')

# ---- faq ----------------------------------------------------------------------------------------
a('.faq[0][1]',
  'Tres de dieciséis. La lista de precios del 27 de octubre de 2026 muestra las otras trece reservadas.',
  'Trois sur seize. La liste de prix du 27 octobre 2026 indique les treize autres comme réservés.',
  'Drei von sechzehn. Die Preisliste vom 27. Oktober 2026 weist die übrigen dreizehn als reserviert aus.',
  'Три из шестнадцати. В прайс-листе от 27 октября 2026 года остальные тринадцать забронированы.',
  'ثلاثة من ستة عشر. وتُظهر قائمة الأسعار المؤرخة 27 أكتوبر 2026 أن الثلاثة عشر الأخرى محجوزة.',
  'Drie van de zestien. De prijslijst van 27 oktober 2026 toont de andere dertien als gereserveerd.',
  'Trzy z szesnastu. Cennik z 27 października 2026 r. pokazuje pozostałe trzynaście jako zarezerwowane.',
  'Tre av seksten. Prislisten datert 27. oktober 2026 viser de andre tretten som reservert.',
  'Tre av sexton. Prislistan daterad 27 oktober 2026 visar de övriga tretton som reserverade.')
a('.faq[1][1]',
  '{E740000} la vivienda 3, {E1040000} el ático y {E1145000} el ático dúplex, más IVA y gastos de compra.',
  '{E740000} pour le logement 3, {E1040000} pour le penthouse et {E1145000} pour le penthouse duplex, hors TVA et frais d’achat.',
  '{E740000} für Wohnung 3, {E1040000} für das Penthouse und {E1145000} für das Maisonette-Penthaus, zuzüglich MwSt. und Kaufnebenkosten.',
  '{E740000} за квартиру 3, {E1040000} за пентхаус и {E1145000} за двухуровневый пентхаус, плюс НДС и расходы на покупку.',
  '{E740000} للمسكن 3، و{E1040000} للبنتهاوس، و{E1145000} للبنتهاوس الدوبلكس، تُضاف إليها ضريبة القيمة المضافة وتكاليف الشراء.',
  '{E740000} voor woning 3, {E1040000} voor het penthouse en {E1145000} voor de duplex penthouse, plus btw en aankoopkosten.',
  '{E740000} za mieszkanie 3, {E1040000} za penthouse i {E1145000} za dwupoziomowy penthouse, plus VAT i koszty zakupu.',
  '{E740000} for bolig 3, {E1040000} for toppleiligheten og {E1145000} for toppleiligheten over to plan, pluss mva og kjøpskostnader.',
  '{E740000} för bostad 3, {E1040000} för takvåningen och {E1145000} för takvåningen i två plan, plus IVA och köpkostnader.')
a('.faq[2][1]',
  'No. La lista de precios indica que sus precios son netos y no incluyen el IVA, el Impuesto sobre Transmisiones Patrimoniales ni otros cargos.',
  'Non. La liste de prix précise que ses prix sont nets et n’incluent ni la TVA, ni les droits de mutation, ni d’autres frais.',
  'Nein. Die Preisliste hält fest, dass ihre Preise netto sind und weder MwSt. noch Grunderwerbsteuer oder sonstige Kosten enthalten.',
  'Нет. В прайс-листе указано, что цены нетто и не включают НДС, налог на передачу имущества и другие сборы.',
  'لا. تذكر قائمة الأسعار أن أسعارها صافية ولا تشمل ضريبة القيمة المضافة ولا ضريبة نقل الملكية ولا رسوماً أخرى.',
  'Nee. De prijslijst vermeldt dat de prijzen netto zijn en geen btw, overdrachtsbelasting of andere kosten bevatten.',
  'Nie. Cennik podaje, że ceny są netto i nie obejmują VAT, podatku od przeniesienia własności ani innych opłat.',
  'Nei. Prislisten sier at prisene er netto og ikke inkluderer mva, dokumentavgift eller andre kostnader.',
  'Nej. Prislistan anger att priserna är netto och inte inkluderar IVA, överlåtelseskatt eller andra avgifter.')
a('.faq[3][1]',
  'El portal del promotor indica el tercer trimestre de 2027, con la licencia de obra concedida y las obras iniciadas en junio de 2025.',
  'Le portail du promoteur indique le troisième trimestre 2027, avec le permis de construire accordé et les travaux commencés en juin 2025.',
  'Das Portal des Bauträgers nennt das dritte Quartal 2027, mit erteilter Baugenehmigung und Baubeginn im Juni 2025.',
  'Портал застройщика указывает третий квартал 2027 года; разрешение на строительство получено, работы начались в июне 2025 года.',
  'تذكر بوابة المطوّر الربع الثالث من عام 2027، مع منح رخصة البناء وبدء الأعمال في يونيو 2025.',
  'Het portaal van de ontwikkelaar noemt het derde kwartaal van 2027, met verleende bouwvergunning en de bouw gestart in juni 2025.',
  'Portal dewelopera podaje trzeci kwartał 2027 r.; pozwolenie na budowę wydano, a budowa ruszyła w czerwcu 2025 r.',
  'Utbyggerens portal oppgir tredje kvartal 2027, med byggetillatelse gitt og byggestart i juni 2025.',
  'Exploatörens portal anger tredje kvartalet 2027, med bygglov beviljat och byggstart i juni 2025.')
a('.faq[4][1]',
  '{E10000} para reservar, el 30 % en el contrato privado, el 20 % seis meses después y el 50 % con la licencia de primera ocupación y la escritura, cada importe más IVA.',
  '{E10000} pour réserver, 30 % au contrat privé, 20 % six mois plus tard et 50 % au certificat de conformité et à l’acte authentique, chaque montant hors TVA.',
  '{E10000} zur Reservierung, 30 % beim privaten Kaufvertrag, 20 % sechs Monate später und 50 % bei Bezugsgenehmigung und Beurkundung, jeweils zuzüglich MwSt.',
  '{E10000} за бронирование, 30 % при подписании частного договора, 20 % через шесть месяцев и 50 % при получении лицензии на первое заселение и подписании купчей, каждый платёж плюс НДС.',
  '{E10000} للحجز، و30% عند العقد الخاص، و20% بعد ستة أشهر، و50% عند صدور رخصة الإشغال الأول وتوقيع سند الملكية، ويُضاف إلى كل مبلغ ضريبة القيمة المضافة.',
  '{E10000} om te reserveren, 30% bij het onderhandse contract, 20% zes maanden later en 50% bij de eerste bewoningsvergunning en de notariële akte, telkens plus btw.',
  '{E10000} przy rezerwacji, 30% przy umowie prywatnej, 20% sześć miesięcy później i 50% przy pozwoleniu na pierwsze użytkowanie i akcie notarialnym, każda kwota plus VAT.',
  '{E10000} for å reservere, 30 % ved privat kontrakt, 20 % seks måneder senere og 50 % ved brukstillatelse og skjøte, hvert beløp pluss mva.',
  '{E10000} för att reservera, 30 % vid det privata avtalet, 20 % sex månader senare och 50 % vid slutbesked och köpebrev, varje belopp plus IVA.')
a('.faq[5][1]',
  'La lista de precios asigna a cada vivienda dos plazas de garaje y un trastero.',
  'La liste de prix attribue à chaque logement deux places de parking et une cave.',
  'Die Preisliste ordnet jeder Wohnung zwei Stellplätze und einen Abstellraum zu.',
  'По прайс-листу каждой квартире полагаются два машино-места и кладовая.',
  'تمنح قائمة الأسعار كل مسكن موقفَي سيارات ومخزناً.',
  'De prijslijst kent elke woning twee parkeerplaatsen en een berging toe.',
  'Cennik przypisuje każdemu mieszkaniu dwa miejsca parkingowe i komórkę lokatorską.',
  'Prislisten gir hver bolig to parkeringsplasser og en bod.',
  'Prislistan ger varje bostad två parkeringsplatser och ett förråd.')
a('.faq[6][1]',
  'Una piscina, una cocina exterior con barbacoa y zona chill-out, un gimnasio y una sauna finlandesa, en un recinto cerrado con acceso controlado.',
  'Une piscine, une cuisine d’extérieur avec barbecue et espace détente, une salle de sport et un sauna finlandais, dans un ensemble clos à accès contrôlé.',
  'Ein Pool, eine Außenküche mit Grill und Chill-out-Zone, ein Fitnessraum und eine finnische Sauna, in einer umzäunten Anlage mit Zugangskontrolle.',
  'Бассейн, летняя кухня с барбекю и зоной отдыха, тренажёрный зал и финская сауна на огороженной территории с контролем доступа.',
  'مسبح، ومطبخ خارجي مع شواء ومنطقة استرخاء، وصالة رياضية، وساونا فنلندية، داخل مجمع مسوّر بدخول مراقَب.',
  'Een zwembad, een buitenkeuken met barbecue en chill-outzone, een fitnessruimte en een Finse sauna, in een omheind complex met toegangscontrole.',
  'Basen, kuchnia plenerowa z grillem i strefą chill-out, siłownia i fińska sauna, w ogrodzonym kompleksie z kontrolą dostępu.',
  'Et basseng, et utekjøkken med grill og chill-out-område, et treningsrom og en finsk badstue, i et inngjerdet anlegg med adgangskontroll.',
  'En pool, ett utekök med grill och chill-out-yta, ett gym och en finsk bastu, i ett inhägnat område med tillträdeskontroll.')

# ---- timeline, enquiry, seo ---------------------------------------------------------------------
a('.timeline.items[0][2]',
  'La lista actual, los planos de las tres viviendas y el calendario de pagos.',
  'La liste actuelle, les plans des trois logements et l’échéancier.',
  'Die aktuelle Liste, die Grundrisse der drei Wohnungen und der Zahlungsplan.',
  'Актуальный список, планировки трёх квартир и график платежей.',
  'القائمة الحالية، ومخططات المساكن الثلاثة، وجدول الدفعات.',
  'De actuele lijst, de plattegronden van de drie woningen en het betalingsschema.',
  'Aktualny cennik, rzuty trzech mieszkań i harmonogram płatności.',
  'Den gjeldende listen, plantegningene for de tre boligene og betalingsplanen.',
  'Den aktuella listan, planritningarna för de tre bostäderna och betalningsplanen.')
a('.timeline.items[1][2]',
  'Recorremos con usted la parcela y el camino a la playa.',
  'Nous parcourons avec vous la parcelle et le chemin de la plage.',
  'Wir gehen mit Ihnen über das Grundstück und den Weg zum Strand.',
  'Мы пройдём с вами по участку и дорогой до пляжа.',
  'نتجوّل معكم في قطعة الأرض وعلى الطريق إلى الشاطئ.',
  'Wij lopen met u over het perceel en de weg naar het strand.',
  'Przejdziemy z Państwem po działce i drogą na plażę.',
  'Vi går over tomten og veien til stranden sammen med deg.',
  'Vi går igenom tomten och vägen till stranden tillsammans med er.')
a('.timeline.items[2][2]',
  'Licencia, garantía y fecha de entrega comprobadas antes de que usted firme.',
  'Permis, garantie et date de livraison vérifiés avant que vous ne signiez.',
  'Genehmigung, Bürgschaft und Fertigstellungstermin geprüft, bevor Sie unterschreiben.',
  'Разрешение, гарантия и дата сдачи проверены до того, как вы подпишете.',
  'التحقق من الرخصة والضمان وموعد التسليم قبل أن توقّعوا.',
  'Vergunning, garantie en opleverdatum gecontroleerd voordat u tekent.',
  'Pozwolenie, gwarancja i termin oddania sprawdzone, zanim Państwo podpiszą.',
  'Tillatelse, garanti og ferdigdato sjekket før du signerer.',
  'Bygglov, garanti och färdigställandedatum kontrollerade innan ni skriver under.')
a('.enquiry.headlineHtml', 'Pregunte por <em>las tres viviendas</em>', 'Renseignez-vous sur <em>les trois logements</em>',
  'Fragen Sie nach <em>den drei Wohnungen</em>', 'Узнайте о <em>трёх квартирах</em>', 'استفسروا عن <em>المساكن الثلاثة</em>',
  'Vraag naar <em>de drie woningen</em>', 'Zapytanie o <em>trzy mieszkania</em>',
  'Spør om <em>de tre boligene</em>', 'Fråga om <em>de tre bostäderna</em>')
a('.enquiry.copy',
  'Díganos qué vivienda le interesa y le enviaremos la lista actual y los planos.',
  'Dites-nous quel logement vous intéresse et nous vous enverrons la liste actuelle et les plans.',
  'Sagen Sie uns, welche Wohnung Sie interessiert, und wir senden Ihnen die aktuelle Liste und die Grundrisse.',
  'Сообщите, какая квартира вас интересует, и мы пришлём актуальный список и планировки.',
  'أخبرونا أي مسكن يهمّكم وسنرسل إليكم القائمة الحالية والمخططات.',
  'Laat ons weten welke woning u interesseert en wij sturen u de actuele lijst en de plattegronden.',
  'Prosimy dać nam znać, które mieszkanie Państwa interesuje, a prześlemy aktualny cennik i rzuty.',
  'Fortell oss hvilken bolig du er interessert i, så sender vi den gjeldende listen og plantegningene.',
  'Berätta vilken bostad ni är intresserade av, så skickar vi den aktuella listan och planritningarna.')
a('.enquiry.message',
  'Me gustaría conocer la disponibilidad y los precios actuales de Arrebol Residences.',
  'Je souhaiterais connaître la disponibilité et les prix actuels d’Arrebol Residences.',
  'Ich hätte gern die aktuelle Verfügbarkeit und die Preise für Arrebol Residences.',
  'Хочу узнать актуальное наличие и цены в Arrebol Residences.',
  'أودّ معرفة التوافر والأسعار الحالية لمشروع Arrebol Residences.',
  'Ik wil graag de actuele beschikbaarheid en prijzen van Arrebol Residences weten.',
  'Proszę o informacje o aktualnej dostępności i cenach Arrebol Residences.',
  'Jeg vil gjerne vite gjeldende tilgjengelighet og priser for Arrebol Residences.',
  'Jag vill gärna få veta aktuell tillgänglighet och aktuella priser för Arrebol Residences.')
a('.enquiry.note', 'Contexto del proyecto: Arrebol Residences.', 'Contexte du projet : Arrebol Residences.',
  'Projektkontext: Arrebol Residences.', 'Контекст проекта: Arrebol Residences.', 'سياق المشروع: Arrebol Residences.',
  'Projectcontext: Arrebol Residences.', 'Kontekst projektu: Arrebol Residences.', 'Prosjektkontekst: Arrebol Residences.',
  'Projektkontext: Arrebol Residences.')
CTX = ['Tres viviendas cerca de la playa, Benalmádena', 'Trois logements près de la plage, Benalmádena',
       'Drei Wohnungen nahe dem Strand, Benalmádena', 'Три квартиры у пляжа, Бенальмадена',
       'ثلاثة مساكن قرب الشاطئ، بينالمادينا', 'Drie woningen bij het strand, Benalmádena',
       'Trzy mieszkania blisko plaży, Benalmádena', 'Tre boliger nær stranden, Benalmádena',
       'Tre bostäder nära stranden, Benalmádena']
a('.seo.h1Context', *CTX)
a('.seo.h1', *[f'Arrebol Residences: {c}' for c in CTX])

# ---- write --------------------------------------------------------------------------------------
json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries to', f'{SP}/tr_a.json')
