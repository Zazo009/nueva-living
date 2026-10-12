# -*- coding: utf-8 -*-
"""Olmo Residences: the strings the translation memory did not have.

Same shape as k_selwo.py, but keyed by the English string instead of by index, so a change to the
English copy cannot silently shift a translation onto the wrong sentence. Tokens: {E789000} money,
{N30.33} decimal number, {U} the area unit. Unit sizes are built from a per-locale template.
    python3 tools/import/k_olmo.py <scratch dir>      (writes <dir>/tr_o.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


def a(en, *tr):
    assert len(tr) == 9, (en[:50], len(tr))
    assert en not in T, en[:50]
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    T[en] = {l: en for l in LOCS}


# identifiers: the invented name and the developer's own home codes read the same everywhere
for s in ['Olmo Residences', 'Olmo', 'Olmo <em>Residences</em>']:
    same(s)

a('18 of 25 contemporary townhouses with three or four bedrooms at El Higuerón, Fuengirola, each with a private pool and its own outdoor space, and a shared gym, pool and multi-purpose space. The developer’s documents give no completion date. From EUR 789,000.',
  '18 de 25 adosados contemporáneos de tres o cuatro dormitorios en El Higuerón, Fuengirola, cada uno con piscina privada y espacio exterior propio, y gimnasio, piscina y espacio polivalente compartidos. Los documentos del promotor no indican fecha de entrega. Desde {E789000}.',
  '18 des 25 maisons mitoyennes contemporaines de trois ou quatre chambres à El Higuerón, Fuengirola, chacune avec piscine privée et espace extérieur propre, ainsi qu’une salle de sport, une piscine et un espace polyvalent communs. Les documents du promoteur ne donnent aucune date de livraison. À partir de {E789000}.',
  '18 von 25 zeitgenössischen Reihenhäusern mit drei oder vier Schlafzimmern in El Higuerón, Fuengirola, jeweils mit privatem Pool und eigenem Außenbereich sowie gemeinsamem Fitnessraum, Pool und Mehrzweckraum. Die Unterlagen des Bauträgers nennen keinen Fertigstellungstermin. Ab {E789000}.',
  '18 из 25 современных таунхаусов с тремя или четырьмя спальнями в Эль-Игероне, Фуэнхирола: у каждого частный бассейн и собственное открытое пространство, а для всех жителей есть тренажёрный зал, бассейн и многофункциональное помещение. В документах застройщика нет срока завершения. От {E789000}.',
  '18 من أصل 25 منزلًا متلاصقًا معاصرًا بثلاث أو أربع غرف نوم في إل إيغيرون، فوينخيرولا، لكل منزل مسبح خاص ومساحة خارجية خاصة، مع صالة رياضية ومسبح وقاعة متعددة الاستخدامات مشتركة. لا تذكر وثائق المطوّر موعد الإنجاز. ابتداءً من {E789000}.',
  '18 van de 25 eigentijdse rijwoningen met drie of vier slaapkamers in El Higuerón, Fuengirola, elk met een privézwembad en een eigen buitenruimte, plus een gedeelde fitnessruimte, een zwembad en een multifunctionele ruimte. De documenten van de ontwikkelaar noemen geen opleveringsdatum. Vanaf {E789000}.',
  '18 z 25 nowoczesnych domów szeregowych z trzema lub czterema sypialniami w El Higuerón, Fuengirola, każdy z prywatnym basenem i własną przestrzenią zewnętrzną, a także wspólną siłownią, basenem i salą wielofunkcyjną. Dokumenty dewelopera nie podają terminu ukończenia. Od {E789000}.',
  '18 av 25 moderne rekkehus med tre eller fire soverom i El Higuerón, Fuengirola, hvert med privat basseng og egen utendørs plass, samt felles treningsrom, basseng og flerbruksrom. Utbyggerens dokumenter oppgir ingen ferdigstillelsesdato. Fra {E789000}.',
  '18 av 25 moderna radhus med tre eller fyra sovrum i El Higuerón, Fuengirola, vart och ett med privat pool och egen utomhusyta, samt gemensamt gym, gemensam pool och ett flexibelt rum. Exploatörens dokument anger inget färdigställandedatum. Från {E789000}.')

a('18 of 25 three- and four-bedroom townhouses at El Higuerón, Fuengirola, each with a private pool and terraces, with a communal gym and pool, from EUR 789,000.',
  '18 de 25 adosados de tres y cuatro dormitorios en El Higuerón, Fuengirola, cada uno con piscina privada y terrazas, con gimnasio y piscina comunitarios, desde {E789000}.',
  '18 des 25 maisons mitoyennes de trois et quatre chambres à El Higuerón, Fuengirola, chacune avec piscine privée et terrasses, avec salle de sport et piscine communes, à partir de {E789000}.',
  '18 von 25 Reihenhäusern mit drei und vier Schlafzimmern in El Higuerón, Fuengirola, jeweils mit privatem Pool und Terrassen, mit gemeinsamem Fitnessraum und Pool, ab {E789000}.',
  '18 из 25 таунхаусов с тремя и четырьмя спальнями в Эль-Игероне, Фуэнхирола, у каждого частный бассейн и террасы, есть общий тренажёрный зал и бассейн, от {E789000}.',
  '18 من أصل 25 منزلًا متلاصقًا بثلاث وأربع غرف نوم في إل إيغيرون، فوينخيرولا، لكل منزل مسبح خاص وتراسات، مع صالة رياضية ومسبح مشتركين، ابتداءً من {E789000}.',
  '18 van de 25 rijwoningen met drie en vier slaapkamers in El Higuerón, Fuengirola, elk met een privézwembad en terrassen, met een gemeenschappelijke fitnessruimte en een zwembad, vanaf {E789000}.',
  '18 z 25 domów szeregowych z trzema i czterema sypialniami w El Higuerón, Fuengirola, każdy z prywatnym basenem i tarasami, ze wspólną siłownią i basenem, od {E789000}.',
  '18 av 25 rekkehus med tre og fire soverom i El Higuerón, Fuengirola, hvert med privat basseng og terrasser, med felles treningsrom og basseng, fra {E789000}.',
  '18 av 25 radhus med tre och fyra sovrum i El Higuerón, Fuengirola, vart och ett med privat pool och terrasser, med gemensamt gym och gemensam pool, från {E789000}.')

a('Three- and four-bedroom townhouses with private pools at El Higuerón, Fuengirola, from EUR 789,000.',
  'Adosados de tres y cuatro dormitorios con piscina privada en El Higuerón, Fuengirola, desde {E789000}.',
  'Maisons mitoyennes de trois et quatre chambres avec piscine privée à El Higuerón, Fuengirola, à partir de {E789000}.',
  'Reihenhäuser mit drei und vier Schlafzimmern und privatem Pool in El Higuerón, Fuengirola, ab {E789000}.',
  'Таунхаусы с тремя и четырьмя спальнями и частным бассейном в Эль-Игероне, Фуэнхирола, от {E789000}.',
  'منازل متلاصقة بثلاث وأربع غرف نوم مع مسبح خاص في إل إيغيرون، فوينخيرولا، ابتداءً من {E789000}.',
  'Rijwoningen met drie en vier slaapkamers en een privézwembad in El Higuerón, Fuengirola, vanaf {E789000}.',
  'Domy szeregowe z trzema i czterema sypialniami oraz prywatnym basenem w El Higuerón, Fuengirola, od {E789000}.',
  'Rekkehus med tre og fire soverom og privat basseng i El Higuerón, Fuengirola, fra {E789000}.',
  'Radhus med tre och fyra sovrum och privat pool i El Higuerón, Fuengirola, från {E789000}.')

a('18 of 25 three- and four-bedroom townhouses at El Higuerón, Fuengirola, each with a private pool, in five groups stepped down the hillside.',
  '18 de 25 adosados de tres y cuatro dormitorios en El Higuerón, Fuengirola, cada uno con piscina privada, en cinco conjuntos escalonados por la ladera.',
  '18 des 25 maisons mitoyennes de trois et quatre chambres à El Higuerón, Fuengirola, chacune avec piscine privée, en cinq ensembles étagés sur le versant.',
  '18 von 25 Reihenhäusern mit drei und vier Schlafzimmern in El Higuerón, Fuengirola, jeweils mit privatem Pool, in fünf Gruppen, die sich den Hang hinunterstufen.',
  '18 из 25 таунхаусов с тремя и четырьмя спальнями в Эль-Игероне, Фуэнхирола, у каждого частный бассейн; пять групп домов спускаются уступами по склону.',
  '18 من أصل 25 منزلًا متلاصقًا بثلاث وأربع غرف نوم في إل إيغيرون، فوينخيرولا، لكل منزل مسبح خاص، في خمس مجموعات تتدرج على سفح التل.',
  '18 van de 25 rijwoningen met drie en vier slaapkamers in El Higuerón, Fuengirola, elk met een privézwembad, in vijf groepen die langs de heuvel afdalen.',
  '18 z 25 domów szeregowych z trzema i czterema sypialniami w El Higuerón, Fuengirola, każdy z prywatnym basenem, w pięciu grupach schodzących tarasowo po zboczu.',
  '18 av 25 rekkehus med tre og fire soverom i El Higuerón, Fuengirola, hvert med privat basseng, i fem grupper som trapper seg nedover åssiden.',
  '18 av 25 radhus med tre och fyra sovrum i El Higuerón, Fuengirola, vart och ett med privat pool, i fem grupper som trappar ner längs sluttningen.')

# --- image alts and captions
a('Computer-generated view of curved terraced facades stepping down a hillside towards the sea',
  'Imagen generada por ordenador de fachadas curvas con terrazas que descienden por una ladera hacia el mar',
  'Image de synthèse de façades courbes à terrasses qui descendent un versant vers la mer',
  'Computergenerierte Ansicht geschwungener Terrassenfassaden, die einen Hang zum Meer hin hinabsteigen',
  'Компьютерная визуализация изогнутых фасадов с террасами, спускающихся по склону к морю',
  'منظر مُنشأ بالحاسوب لواجهات منحنية ذات تراسات تنحدر على سفح التل باتجاه البحر',
  'Computergegenereerd beeld van gebogen gevels met terrassen die langs een heuvel naar de zee aflopen',
  'Wizualizacja komputerowa zakrzywionych elewacji z tarasami, schodzących po zboczu w stronę morza',
  'Datagenerert bilde av buede fasader med terrasser som trapper seg nedover en åsside mot havet',
  'Datorgenererad bild av böjda fasader med terrasser som trappar ner längs en sluttning mot havet')
a('The terraced facades above the sea',
  'Las fachadas con terrazas sobre el mar', 'Les façades à terrasses au-dessus de la mer', 'Die Terrassenfassaden über dem Meer',
  'Фасады с террасами над морем', 'الواجهات المدرجة فوق البحر', 'De gevels met terrassen boven de zee', 'Elewacje z tarasami nad morzem',
  'Terrassefasadene over havet', 'Terrassfasaderna ovanför havet')
a('Computer-generated view of the rows of homes on the hillside, with the pool terrace and the mountains behind',
  'Imagen generada por ordenador de las hileras de viviendas en la ladera, con la terraza de la piscina y las montañas al fondo',
  'Image de synthèse des rangées de maisons sur le versant, avec la terrasse de la piscine et les montagnes en arrière-plan',
  'Computergenerierte Ansicht der Häuserreihen am Hang, mit der Poolterrasse und den Bergen im Hintergrund',
  'Компьютерная визуализация рядов домов на склоне с террасой у бассейна и горами на заднем плане',
  'منظر مُنشأ بالحاسوب لصفوف المنازل على سفح التل، مع تراس المسبح والجبال في الخلفية',
  'Computergegenereerd beeld van de rijen woningen op de heuvel, met het zwembadterras en de bergen erachter',
  'Wizualizacja komputerowa rzędów domów na zboczu, z tarasem przy basenie i górami w tle',
  'Datagenerert bilde av husradene i åssiden, med bassengterrassen og fjellene bak',
  'Datorgenererad bild av husraderna i sluttningen, med poolterrassen och bergen bakom')
a('The homes on the hillside',
  'Las viviendas en la ladera', 'Les maisons sur le versant', 'Die Häuser am Hang', 'Дома на склоне', 'المنازل على سفح التل',
  'De woningen op de heuvel', 'Domy na zboczu', 'Boligene i åssiden', 'Bostäderna i sluttningen')
a('Computer-generated view of a living room opening to a terrace with seating and a private pool, with the sea beyond',
  'Imagen generada por ordenador de un salón que se abre a una terraza con asientos y piscina privada, con el mar al fondo',
  'Image de synthèse d’un séjour ouvert sur une terrasse avec salon d’extérieur et piscine privée, la mer au loin',
  'Computergenerierte Ansicht eines Wohnzimmers, das sich zu einer Terrasse mit Sitzgelegenheiten und privatem Pool öffnet, dahinter das Meer',
  'Компьютерная визуализация гостиной с выходом на террасу с зоной отдыха и частным бассейном, вдали море',
  'منظر مُنشأ بالحاسوب لغرفة معيشة تُفتح على تراس فيه مقاعد ومسبح خاص، والبحر في الأفق',
  'Computergegenereerd beeld van een woonkamer die uitkomt op een terras met zitgedeelte en een privézwembad, met de zee op de achtergrond',
  'Wizualizacja komputerowa salonu otwierającego się na taras z miejscem do siedzenia i prywatnym basenem, w tle morze',
  'Datagenerert bilde av en stue som åpner seg mot en terrasse med sittegruppe og privat basseng, med havet bak',
  'Datorgenererad bild av ett vardagsrum som öppnar sig mot en terrass med sittgrupp och privat pool, med havet bortom')
a('Computer-generated view of a bedroom with a double bed and a sliding glass door to the terrace',
  'Imagen generada por ordenador de un dormitorio con cama doble y puerta corredera de vidrio a la terraza',
  'Image de synthèse d’une chambre avec un lit double et une porte coulissante vitrée donnant sur la terrasse',
  'Computergenerierte Ansicht eines Schlafzimmers mit Doppelbett und einer Glasschiebetür zur Terrasse',
  'Компьютерная визуализация спальни с двуспальной кроватью и раздвижной стеклянной дверью на террасу',
  'منظر مُنشأ بالحاسوب لغرفة نوم بسرير مزدوج وباب زجاجي منزلق إلى التراس',
  'Computergegenereerd beeld van een slaapkamer met een tweepersoonsbed en een glazen schuifdeur naar het terras',
  'Wizualizacja komputerowa sypialni z podwójnym łóżkiem i przesuwnymi szklanymi drzwiami na taras',
  'Datagenerert bilde av et soverom med dobbeltseng og skyvedør i glass til terrassen',
  'Datorgenererad bild av ett sovrum med dubbelsäng och en glasskjutdörr till terrassen')
a('Computer-generated views of the homes, their interiors and the shared areas, and the floorplans of two home types.',
  'Imágenes generadas por ordenador de las viviendas, sus interiores y las zonas comunes, y los planos de dos tipos de vivienda.',
  'Images de synthèse des maisons, de leurs intérieurs et des parties communes, et plans de deux types de maison.',
  'Computergenerierte Ansichten der Häuser, ihrer Innenräume und der Gemeinschaftsbereiche sowie die Grundrisse von zwei Haustypen.',
  'Компьютерные визуализации домов, их интерьеров и общих зон, а также планировки двух типов домов.',
  'مناظر مُنشأة بالحاسوب للمنازل وفضاءاتها الداخلية والمناطق المشتركة، ومخططات نوعين من المنازل.',
  'Computergegenereerde beelden van de woningen, hun interieurs en de gedeelde ruimten, en de plattegronden van twee woningtypes.',
  'Wizualizacje komputerowe domów, ich wnętrz i części wspólnych oraz rzuty dwóch typów domów.',
  'Datagenererte bilder av boligene, interiørene og fellesområdene, og plantegninger av to boligtyper.',
  'Datorgenererade bilder av bostäderna, deras interiörer och de gemensamma ytorna samt planritningar av två bostadstyper.')
a('All the images are computer-generated, and the furniture, decoration and planting in them are illustrative and not included in the price. The floorplans are the developer’s project-stage plans and the areas on them are approximate and subject to the final project. The room names on the plans are in Spanish.',
  'Todas las imágenes están generadas por ordenador, y el mobiliario, la decoración y la vegetación que aparecen son ilustrativos y no están incluidos en el precio. Los planos son los de proyecto del promotor y las superficies que figuran en ellos son aproximadas y están sujetas al proyecto definitivo. Los nombres de las estancias en los planos están en español.',
  'Toutes les images sont de synthèse, et le mobilier, la décoration et la végétation qui y figurent sont illustratifs et non compris dans le prix. Les plans sont les plans de projet du promoteur et les surfaces qui y figurent sont approximatives et soumises au projet définitif. Les noms des pièces sur les plans sont en espagnol.',
  'Alle Bilder sind computergeneriert; Möblierung, Dekoration und Bepflanzung darin sind illustrativ und nicht im Preis enthalten. Die Grundrisse sind die Projektpläne des Bauträgers, und die darin angegebenen Flächen sind ungefähr und vorbehaltlich des endgültigen Projekts. Die Raumbezeichnungen in den Plänen sind auf Spanisch.',
  'Все изображения созданы на компьютере; мебель, отделка и озеленение на них носят иллюстративный характер и в стоимость не входят. Планировки — это проектные планы застройщика, указанные на них площади приблизительны и зависят от окончательного проекта. Названия помещений на планах даны на испанском языке.',
  'جميع الصور مُنشأة بالحاسوب، والأثاث والديكور والنباتات الظاهرة فيها للتوضيح فقط وغير مشمولة في السعر. المخططات هي مخططات مرحلة المشروع لدى المطوّر، والمساحات المبينة عليها تقريبية وخاضعة للمشروع النهائي. أسماء الغرف على المخططات باللغة الإسبانية.',
  'Alle beelden zijn computergegenereerd en het meubilair, de inrichting en de beplanting daarop zijn illustratief en niet in de prijs inbegrepen. De plattegronden zijn de projectplannen van de ontwikkelaar en de oppervlakten erop zijn bij benadering en onder voorbehoud van het definitieve project. De namen van de ruimten op de plattegronden zijn in het Spaans.',
  'Wszystkie obrazy są wygenerowane komputerowo, a meble, wystrój i zieleń na nich mają charakter poglądowy i nie są wliczone w cenę. Rzuty to projektowe plany dewelopera, a podane na nich powierzchnie są przybliżone i zależą od ostatecznego projektu. Nazwy pomieszczeń na rzutach są po hiszpańsku.',
  'Alle bildene er datagenererte, og møbler, innredning og beplantning på dem er illustrasjoner og ikke inkludert i prisen. Plantegningene er utbyggerens prosjektplaner, og arealene på dem er omtrentlige og med forbehold om det endelige prosjektet. Romnavnene på tegningene er på spansk.',
  'Alla bilder är datorgenererade, och möbler, inredning och växtlighet på dem är illustrationer och ingår inte i priset. Planritningarna är exploatörens projektritningar, och ytorna på dem är ungefärliga och med förbehåll för det slutliga projektet. Rumsnamnen på ritningarna är på spanska.')
a('Computer-generated aerial view at dusk of the curved terraces with the communal pool lit below',
  'Vista aérea generada por ordenador al anochecer de las terrazas curvas con la piscina comunitaria iluminada debajo',
  'Vue aérienne de synthèse au crépuscule des terrasses courbes avec la piscine commune éclairée en contrebas',
  'Computergenerierte Luftansicht in der Abenddämmerung der geschwungenen Terrassen mit dem beleuchteten Gemeinschaftspool darunter',
  'Компьютерная визуализация с высоты в сумерках: изогнутые террасы и освещённый общий бассейн внизу',
  'منظر جوي مُنشأ بالحاسوب عند الغسق للتراسات المنحنية مع المسبح المشترك المضاء في الأسفل',
  'Computergegenereerd luchtbeeld bij schemering van de gebogen terrassen met daaronder het verlichte gemeenschappelijke zwembad',
  'Wizualizacja komputerowa z lotu ptaka o zmierzchu: zakrzywione tarasy i oświetlony wspólny basen poniżej',
  'Datagenerert flyfoto i skumringen av de buede terrassene med det opplyste fellesbassenget under',
  'Datorgenererad flygbild i skymningen av de böjda terrasserna med den upplysta gemensamma poolen nedanför')
a('The terraces and the pool at dusk',
  'Las terrazas y la piscina al anochecer', 'Les terrasses et la piscine au crépuscule', 'Die Terrassen und der Pool in der Abenddämmerung',
  'Террасы и бассейн в сумерках', 'التراسات والمسبح عند الغسق', 'De terrassen en het zwembad bij schemering', 'Tarasy i basen o zmierzchu',
  'Terrassene og bassenget i skumringen', 'Terrasserna och poolen i skymningen')
a('Computer-generated view at dusk of the stone-walled entrance, the garage opening and the curved terraces above',
  'Imagen generada por ordenador al anochecer de la entrada con muro de piedra, la boca del garaje y las terrazas curvas por encima',
  'Image de synthèse au crépuscule de l’entrée à mur de pierre, de l’accès au garage et des terrasses courbes au-dessus',
  'Computergenerierte Ansicht in der Abenddämmerung des Eingangs mit Natursteinmauer, der Garagenzufahrt und der geschwungenen Terrassen darüber',
  'Компьютерная визуализация в сумерках: въезд с каменной стеной, проём гаража и изогнутые террасы выше',
  'منظر مُنشأ بالحاسوب عند الغسق للمدخل ذي الجدار الحجري وفتحة المرآب والتراسات المنحنية فوقه',
  'Computergegenereerd beeld bij schemering van de ingang met stenen muur, de garage-opening en de gebogen terrassen erboven',
  'Wizualizacja komputerowa o zmierzchu: wjazd z kamiennym murem, wjazd do garażu i zakrzywione tarasy powyżej',
  'Datagenerert bilde i skumringen av inngangen med steinmur, garasjeåpningen og de buede terrassene over',
  'Datorgenererad bild i skymningen av ingången med stenmur, garageinfarten och de böjda terrasserna ovanför')
a('The entrance and terraces at dusk',
  'La entrada y las terrazas al anochecer', 'L’entrée et les terrasses au crépuscule', 'Der Eingang und die Terrassen in der Abenddämmerung',
  'Въезд и террасы в сумерках', 'المدخل والتراسات عند الغسق', 'De ingang en de terrassen bij schemering', 'Wjazd i tarasy o zmierzchu',
  'Inngangen og terrassene i skumringen', 'Ingången och terrasserna i skymningen')
a('Computer-generated view of the communal outdoor pool with sun loungers on a timber deck and the sea beyond',
  'Imagen generada por ordenador de la piscina exterior comunitaria con tumbonas sobre una tarima de madera y el mar al fondo',
  'Image de synthèse de la piscine extérieure commune avec transats sur un deck en bois et la mer au loin',
  'Computergenerierte Ansicht des gemeinschaftlichen Außenpools mit Sonnenliegen auf einem Holzdeck und dem Meer dahinter',
  'Компьютерная визуализация общего открытого бассейна с шезлонгами на деревянном настиле, вдали море',
  'منظر مُنشأ بالحاسوب للمسبح الخارجي المشترك مع كراسي استلقاء على أرضية خشبية والبحر في الأفق',
  'Computergegenereerd beeld van het gemeenschappelijke buitenzwembad met ligbedden op een houten dek en de zee erachter',
  'Wizualizacja komputerowa wspólnego basenu zewnętrznego z leżakami na drewnianym podeście, w tle morze',
  'Datagenerert bilde av det felles utendørsbassenget med solsenger på et tredekk og havet bak',
  'Datorgenererad bild av den gemensamma utomhuspoolen med solstolar på ett trädäck och havet bortom')
a('The communal pool and the sea',
  'La piscina comunitaria y el mar', 'La piscine commune et la mer', 'Der Gemeinschaftspool und das Meer', 'Общий бассейн и море',
  'المسبح المشترك والبحر', 'Het gemeenschappelijke zwembad en de zee', 'Wspólny basen i morze', 'Fellesbassenget og havet', 'Den gemensamma poolen och havet')
a('Computer-generated view of a timber walkway with two people doing yoga above the pool terrace',
  'Imagen generada por ordenador de un paseo de madera con dos personas haciendo yoga sobre la terraza de la piscina',
  'Image de synthèse d’une promenade en bois où deux personnes font du yoga au-dessus de la terrasse de la piscine',
  'Computergenerierte Ansicht eines Holzwegs, auf dem zwei Personen oberhalb der Poolterrasse Yoga machen',
  'Компьютерная визуализация деревянной дорожки, где двое занимаются йогой над террасой у бассейна',
  'منظر مُنشأ بالحاسوب لممر خشبي يمارس فيه شخصان اليوغا فوق تراس المسبح',
  'Computergegenereerd beeld van een houten wandelpad waar twee mensen yoga doen boven het zwembadterras',
  'Wizualizacja komputerowa drewnianej ścieżki, na której dwie osoby ćwiczą jogę nad tarasem przy basenie',
  'Datagenerert bilde av en tregang der to personer gjør yoga over bassengterrassen',
  'Datorgenererad bild av en träpromenad där två personer gör yoga ovanför poolterrassen')
a('The walkway above the pool',
  'El paseo sobre la piscina', 'La promenade au-dessus de la piscine', 'Der Weg oberhalb des Pools', 'Дорожка над бассейном',
  'الممر فوق المسبح', 'Het wandelpad boven het zwembad', 'Ścieżka nad basenem', 'Gangen over bassenget', 'Promenaden ovanför poolen')
a('Computer-generated view of the residents’ gym with weights, cardio machines and a glazed wall facing the landscape',
  'Imagen generada por ordenador del gimnasio de los residentes con pesas, máquinas de cardio y una pared acristalada hacia el paisaje',
  'Image de synthèse de la salle de sport des résidents avec poids, appareils de cardio et une paroi vitrée donnant sur le paysage',
  'Computergenerierte Ansicht des Fitnessraums der Bewohner mit Gewichten, Cardiogeräten und einer verglasten Wand zur Landschaft',
  'Компьютерная визуализация тренажёрного зала для жителей с гантелями, кардиотренажёрами и стеклянной стеной с видом на ландшафт',
  'منظر مُنشأ بالحاسوب لصالة السكان الرياضية بأوزانها وأجهزة الكارديو وجدار زجاجي يطل على المشهد الطبيعي',
  'Computergegenereerd beeld van de fitnessruimte voor bewoners met gewichten, cardioapparaten en een glazen wand met uitzicht op het landschap',
  'Wizualizacja komputerowa siłowni dla mieszkańców z obciążnikami, sprzętem cardio i przeszkloną ścianą z widokiem na krajobraz',
  'Datagenerert bilde av beboernes treningsrom med vekter, kardioapparater og en glassvegg mot landskapet',
  'Datorgenererad bild av de boendes gym med vikter, konditionsmaskiner och en glasvägg mot landskapet')
a('The residents’ gym',
  'El gimnasio de los residentes', 'La salle de sport des résidents', 'Der Fitnessraum der Bewohner', 'Тренажёрный зал для жителей',
  'صالة السكان الرياضية', 'De fitnessruimte voor bewoners', 'Siłownia dla mieszkańców', 'Beboernes treningsrom', 'De boendes gym')
a('Computer-generated view of a terrace at sunset with seating, a private pool and the sea on the horizon',
  'Imagen generada por ordenador de una terraza al atardecer con asientos, una piscina privada y el mar en el horizonte',
  'Image de synthèse d’une terrasse au coucher du soleil avec salon d’extérieur, piscine privée et la mer à l’horizon',
  'Computergenerierte Ansicht einer Terrasse bei Sonnenuntergang mit Sitzgelegenheiten, privatem Pool und dem Meer am Horizont',
  'Компьютерная визуализация террасы на закате с зоной отдыха, частным бассейном и морем на горизонте',
  'منظر مُنشأ بالحاسوب لتراس عند الغروب فيه مقاعد ومسبح خاص والبحر عند الأفق',
  'Computergegenereerd beeld van een terras bij zonsondergang met zitgedeelte, een privézwembad en de zee aan de horizon',
  'Wizualizacja komputerowa tarasu o zachodzie słońca z miejscem do siedzenia, prywatnym basenem i morzem na horyzoncie',
  'Datagenerert bilde av en terrasse ved solnedgang med sittegruppe, privat basseng og havet i horisonten',
  'Datorgenererad bild av en terrass i solnedgången med sittgrupp, privat pool och havet vid horisonten')
a('A private pool terrace at sunset',
  'Una terraza con piscina privada al atardecer', 'Une terrasse avec piscine privée au coucher du soleil', 'Eine Terrasse mit privatem Pool bei Sonnenuntergang',
  'Терраса с частным бассейном на закате', 'تراس بمسبح خاص عند الغروب', 'Een terras met privézwembad bij zonsondergang', 'Taras z prywatnym basenem o zachodzie słońca',
  'En terrasse med privat basseng ved solnedgang', 'En terrass med privat pool i solnedgången')
a('Living room, terrace and private pool',
  'Salón, terraza y piscina privada', 'Séjour, terrasse et piscine privée', 'Wohnzimmer, Terrasse und privater Pool', 'Гостиная, терраса и частный бассейн',
  'غرفة المعيشة والتراس والمسبح الخاص', 'Woonkamer, terras en privézwembad', 'Salon, taras i prywatny basen', 'Stue, terrasse og privat basseng', 'Vardagsrum, terrass och privat pool')
a('Computer-generated view of a lawned terrace with armchairs and a glass balustrade above the pool and the sea',
  'Imagen generada por ordenador de una terraza con césped, butacas y barandilla de vidrio sobre la piscina y el mar',
  'Image de synthèse d’une terrasse engazonnée avec fauteuils et garde-corps en verre au-dessus de la piscine et de la mer',
  'Computergenerierte Ansicht einer Rasenterrasse mit Sesseln und einer Glasbrüstung oberhalb von Pool und Meer',
  'Компьютерная визуализация террасы с газоном, креслами и стеклянным ограждением над бассейном и морем',
  'منظر مُنشأ بالحاسوب لتراس مكسو بالعشب فيه كراسٍ وحاجز زجاجي فوق المسبح والبحر',
  'Computergegenereerd beeld van een terras met gazon, fauteuils en een glazen balustrade boven het zwembad en de zee',
  'Wizualizacja komputerowa tarasu z trawnikiem, fotelami i szklaną balustradą nad basenem i morzem',
  'Datagenerert bilde av en terrasse med gressplen, lenestoler og glassrekkverk over bassenget og havet',
  'Datorgenererad bild av en terrass med gräsmatta, fåtöljer och glasräcke ovanför poolen och havet')
a('A lawned terrace above the sea',
  'Una terraza con césped sobre el mar', 'Une terrasse engazonnée au-dessus de la mer', 'Eine Rasenterrasse über dem Meer', 'Терраса с газоном над морем',
  'تراس معشوشب فوق البحر', 'Een terras met gazon boven de zee', 'Taras z trawnikiem nad morzem', 'En terrasse med plen over havet', 'En terrass med gräsmatta ovanför havet')
a('Computer-generated view of a living and dining room with a marble table and a sliding glass wall to the terrace and the sea',
  'Imagen generada por ordenador de un salón-comedor con mesa de mármol y una pared de vidrio corredera hacia la terraza y el mar',
  'Image de synthèse d’un séjour-salle à manger avec table en marbre et paroi vitrée coulissante donnant sur la terrasse et la mer',
  'Computergenerierte Ansicht eines Wohn- und Essbereichs mit Marmortisch und einer gläsernen Schiebewand zur Terrasse und zum Meer',
  'Компьютерная визуализация гостиной со столовой, мраморным столом и раздвижной стеклянной стеной на террасу и море',
  'منظر مُنشأ بالحاسوب لغرفة معيشة وطعام بطاولة رخامية وجدار زجاجي منزلق نحو التراس والبحر',
  'Computergegenereerd beeld van een woon- en eetkamer met een marmeren tafel en een glazen schuifwand naar het terras en de zee',
  'Wizualizacja komputerowa salonu z jadalnią, marmurowym stołem i przesuwną szklaną ścianą na taras i morze',
  'Datagenerert bilde av en stue og spisestue med marmorbord og en glassskyvevegg mot terrassen og havet',
  'Datorgenererad bild av ett vardagsrum med matplats, marmorbord och en glasskjutvägg mot terrassen och havet')
a('Computer-generated view of an open-plan living room and kitchen with a marble island and sea views',
  'Imagen generada por ordenador de un salón y una cocina abiertos con isla de mármol y vistas al mar',
  'Image de synthèse d’un séjour et d’une cuisine ouverts avec îlot en marbre et vue sur la mer',
  'Computergenerierte Ansicht eines offenen Wohnbereichs mit Küche, Marmorinsel und Meerblick',
  'Компьютерная визуализация гостиной, совмещённой с кухней, с мраморным островом и видом на море',
  'منظر مُنشأ بالحاسوب لغرفة معيشة ومطبخ مفتوحين بجزيرة رخامية وإطلالة على البحر',
  'Computergegenereerd beeld van een open woonkamer met keuken, een marmeren eiland en zeezicht',
  'Wizualizacja komputerowa otwartego salonu z kuchnią, marmurową wyspą i widokiem na morze',
  'Datagenerert bilde av en åpen stue med kjøkken, marmoröy og havutsikt',
  'Datorgenererad bild av ett öppet vardagsrum med kök, marmorö och havsutsikt')
a('Living room and kitchen island',
  'Salón e isla de cocina', 'Séjour et îlot de cuisine', 'Wohnzimmer und Kücheninsel', 'Гостиная и кухонный остров',
  'غرفة المعيشة وجزيرة المطبخ', 'Woonkamer en keukeneiland', 'Salon i wyspa kuchenna', 'Stue og kjøkkenøy', 'Vardagsrum och köksö')
a('Computer-generated view of an open-plan kitchen and living room with a long sofa and a large glazed door to the terrace',
  'Imagen generada por ordenador de una cocina y un salón abiertos con un sofá largo y una gran puerta acristalada a la terraza',
  'Image de synthèse d’une cuisine et d’un séjour ouverts avec un long canapé et une grande porte vitrée sur la terrasse',
  'Computergenerierte Ansicht einer offenen Küche mit Wohnbereich, einem langen Sofa und einer großen verglasten Tür zur Terrasse',
  'Компьютерная визуализация кухни-гостиной с длинным диваном и большой стеклянной дверью на террасу',
  'منظر مُنشأ بالحاسوب لمطبخ وغرفة معيشة مفتوحين بأريكة طويلة وباب زجاجي كبير إلى التراس',
  'Computergegenereerd beeld van een open keuken met woonkamer, een lange bank en een grote glazen deur naar het terras',
  'Wizualizacja komputerowa otwartej kuchni z salonem, długą sofą i dużymi przeszklonymi drzwiami na taras',
  'Datagenerert bilde av et åpent kjøkken og en stue med en lang sofa og en stor glassdør til terrassen',
  'Datorgenererad bild av ett öppet kök med vardagsrum, en lång soffa och en stor glasdörr till terrassen')
a('Open-plan kitchen and living room',
  'Cocina y salón abiertos', 'Cuisine et séjour ouverts', 'Offene Küche mit Wohnzimmer', 'Кухня-гостиная', 'مطبخ وغرفة معيشة مفتوحان',
  'Open keuken en woonkamer', 'Otwarta kuchnia z salonem', 'Åpent kjøkken og stue', 'Öppet kök och vardagsrum')
a('Computer-generated view of a kitchen and dining area with a spiral staircase to the upper level',
  'Imagen generada por ordenador de una cocina y un comedor con una escalera de caracol a la planta superior',
  'Image de synthèse d’une cuisine et d’un coin repas avec un escalier en colimaçon vers l’étage',
  'Computergenerierte Ansicht einer Küche mit Essbereich und einer Wendeltreppe zum Obergeschoss',
  'Компьютерная визуализация кухни со столовой зоной и винтовой лестницей на верхний уровень',
  'منظر مُنشأ بالحاسوب لمطبخ ومنطقة طعام مع سلم حلزوني إلى الطابق العلوي',
  'Computergegenereerd beeld van een keuken met eethoek en een wenteltrap naar de verdieping',
  'Wizualizacja komputerowa kuchni z jadalnią i spiralnymi schodami na wyższy poziom',
  'Datagenerert bilde av et kjøkken med spiseplass og en spiraltrapp til øvre plan',
  'Datorgenererad bild av ett kök med matplats och en spiraltrappa till övre planet')
a('Kitchen and spiral staircase',
  'Cocina y escalera de caracol', 'Cuisine et escalier en colimaçon', 'Küche und Wendeltreppe', 'Кухня и винтовая лестница',
  'المطبخ والسلم الحلزوني', 'Keuken en wenteltrap', 'Kuchnia i spiralne schody', 'Kjøkken og spiraltrapp', 'Kök och spiraltrappa')
a('Computer-generated view of a main bedroom with a glazed screen to the bathroom and a dressing area',
  'Imagen generada por ordenador de un dormitorio principal con un cerramiento acristalado al baño y un vestidor',
  'Image de synthèse d’une chambre principale avec une cloison vitrée vers la salle de bains et un dressing',
  'Computergenerierte Ansicht eines Hauptschlafzimmers mit Glaswand zum Bad und einem Ankleidebereich',
  'Компьютерная визуализация главной спальни со стеклянной перегородкой в ванную и гардеробной зоной',
  'منظر مُنشأ بالحاسوب لغرفة نوم رئيسية بحاجز زجاجي نحو الحمام ومنطقة لتبديل الملابس',
  'Computergegenereerd beeld van een hoofdslaapkamer met een glazen wand naar de badkamer en een kleedruimte',
  'Wizualizacja komputerowa głównej sypialni ze szklaną ścianą do łazienki i garderobą',
  'Datagenerert bilde av et hovedsoverom med glassvegg mot badet og en garderobe',
  'Datorgenererad bild av ett huvudsovrum med glasvägg mot badrummet och en klädavdelning')
a('Main bedroom, bathroom and dressing area',
  'Dormitorio principal, baño y vestidor', 'Chambre principale, salle de bains et dressing', 'Hauptschlafzimmer, Bad und Ankleidebereich',
  'Главная спальня, ванная и гардеробная', 'غرفة النوم الرئيسية والحمام ومنطقة الملابس', 'Hoofdslaapkamer, badkamer en kleedruimte',
  'Główna sypialnia, łazienka i garderoba', 'Hovedsoverom, bad og garderobe', 'Huvudsovrum, badrum och klädavdelning')
a('Computer-generated view of a bathroom with a double vanity, a walk-in shower and a freestanding bath',
  'Imagen generada por ordenador de un baño con doble lavabo, ducha de obra y bañera exenta',
  'Image de synthèse d’une salle de bains avec double vasque, douche à l’italienne et baignoire îlot',
  'Computergenerierte Ansicht eines Badezimmers mit Doppelwaschtisch, ebenerdiger Dusche und freistehender Badewanne',
  'Компьютерная визуализация ванной комнаты с двумя раковинами, душевой без поддона и отдельно стоящей ванной',
  'منظر مُنشأ بالحاسوب لحمام بحوضين ودش مفتوح وحوض استحمام قائم بذاته',
  'Computergegenereerd beeld van een badkamer met dubbele wastafel, inloopdouche en vrijstaand bad',
  'Wizualizacja komputerowa łazienki z podwójną umywalką, prysznicem bez brodzika i wolnostojącą wanną',
  'Datagenerert bilde av et bad med dobbel servant, åpen dusj og frittstående badekar',
  'Datorgenererad bild av ett badrum med dubbel tvättställ, öppen dusch och fristående badkar')
for ref in ['A.04', 'C.02']:
    pass

LV = {'living level': ('planta salón', 'niveau séjour', 'Wohnebene', 'жилой уровень', 'مستوى المعيشة', 'woonniveau', 'poziom dzienny', 'stueplan', 'vardagsplan'),
      'bedroom level': ('planta dormitorios', 'niveau chambres', 'Schlafebene', 'спальный уровень', 'مستوى غرف النوم', 'slaapniveau', 'poziom sypialni', 'soveplan', 'sovplan'),
      'solarium': ('solárium', 'solarium', 'Solarium', 'солярий', 'السولاريوم', 'solarium', 'solarium', 'solterrasse', 'solterrass')}
for ref in ['A.04', 'C.02']:
    for lv, w in LV.items():
        if ref == 'A.04' and lv == 'solarium':
            continue
        cap = f'Home {ref}, {lv}'
        alt = f'Floorplan of home {ref}, {lv}'
        a(alt, f'Plano de la vivienda {ref}, {w[0]}', f'Plan de la maison {ref}, {w[1]}', f'Grundriss von Haus {ref}, {w[2]}',
          f'Планировка дома {ref}, {w[3]}', f'مخطط المنزل {ref}، {w[4]}', f'Plattegrond van woning {ref}, {w[5]}', f'Rzut domu {ref}, {w[6]}',
          f'Plantegning av bolig {ref}, {w[7]}', f'Planritning av bostad {ref}, {w[8]}')
        a(cap, f'Vivienda {ref}, {w[0]}', f'Maison {ref}, {w[1]}', f'Haus {ref}, {w[2]}', f'Дом {ref}, {w[3]}', f'المنزل {ref}، {w[4]}',
          f'Woning {ref}, {w[5]}', f'Dom {ref}, {w[6]}', f'Bolig {ref}, {w[7]}', f'Bostad {ref}, {w[8]}')

# --- overview, why, architecture
a('Twenty-five homes, <em>eighteen listed</em>',
  'Veinticinco viviendas, <em>dieciocho en lista</em>', 'Vingt-cinq maisons, <em>dix-huit listées</em>', 'Fünfundzwanzig Häuser, <em>achtzehn gelistet</em>',
  'Двадцать пять домов, <em>восемнадцать в списке</em>', 'خمسة وعشرون منزلًا، <em>ثمانية عشر منها مدرجة</em>', 'Vijfentwintig woningen, <em>achttien vermeld</em>',
  'Dwadzieścia pięć domów, <em>osiemnaście na liście</em>', 'Tjuefem boliger, <em>atten oppført</em>', 'Tjugofem bostäder, <em>arton listade</em>')
a('Contemporary townhouses on a hillside at El Higuerón, Fuengirola, in five groups of homes at different levels, so that the architecture steps down the slope. The developer’s brochure describes just 25 homes, with large windows, terraces that are part of daily life and open views of the Mediterranean.',
  'Adosados contemporáneos en una ladera de El Higuerón, Fuengirola, en cinco conjuntos de viviendas a distintos niveles, de modo que la arquitectura desciende escalonada por la pendiente. El folleto del promotor habla de solo 25 viviendas, con grandes ventanales, terrazas que forman parte del día a día y vistas abiertas al Mediterráneo.',
  'Maisons mitoyennes contemporaines sur un versant d’El Higuerón, à Fuengirola, en cinq ensembles de maisons à différents niveaux, de sorte que l’architecture descend en gradins le long de la pente. La brochure du promoteur présente seulement 25 maisons, avec de grandes baies vitrées, des terrasses qui font partie du quotidien et des vues dégagées sur la Méditerranée.',
  'Zeitgenössische Reihenhäuser an einem Hang in El Higuerón, Fuengirola, in fünf Gruppen auf verschiedenen Ebenen, sodass sich die Architektur stufenweise den Hang hinabzieht. Die Broschüre des Bauträgers beschreibt nur 25 Häuser mit großen Fenstern, Terrassen, die zum Alltag gehören, und offenem Blick auf das Mittelmeer.',
  'Современные таунхаусы на склоне в Эль-Игероне, Фуэнхирола: пять групп домов на разных уровнях, так что архитектура спускается уступами по склону. В брошюре застройщика говорится всего о 25 домах с большими окнами, террасами, которые становятся частью повседневной жизни, и открытым видом на Средиземное море.',
  'منازل متلاصقة معاصرة على سفح تل في إل إيغيرون، فوينخيرولا، في خمس مجموعات على مستويات مختلفة، فتتدرج العمارة على المنحدر. تصف نشرة المطوّر 25 منزلًا فقط، بنوافذ كبيرة وتراسات هي جزء من الحياة اليومية وإطلالات مفتوحة على البحر المتوسط.',
  'Eigentijdse rijwoningen op een heuvel in El Higuerón, Fuengirola, in vijf groepen woningen op verschillende niveaus, zodat de architectuur trapsgewijs langs de helling daalt. De brochure van de ontwikkelaar beschrijft slechts 25 woningen, met grote ramen, terrassen die deel uitmaken van het dagelijks leven en open uitzicht op de Middellandse Zee.',
  'Nowoczesne domy szeregowe na zboczu w El Higuerón, Fuengirola, w pięciu grupach na różnych poziomach, tak że architektura schodzi tarasowo po stoku. Broszura dewelopera opisuje zaledwie 25 domów z dużymi oknami, tarasami będącymi częścią codziennego życia i otwartym widokiem na Morze Śródziemne.',
  'Moderne rekkehus i en åsside i El Higuerón, Fuengirola, i fem grupper på ulike nivåer, slik at arkitekturen trapper seg nedover skråningen. Utbyggerens brosjyre beskriver bare 25 boliger, med store vinduer, terrasser som er en del av hverdagen og åpen utsikt mot Middelhavet.',
  'Moderna radhus i en sluttning i El Higuerón, Fuengirola, i fem grupper på olika nivåer, så att arkitekturen trappar ner längs sluttningen. Exploatörens broschyr beskriver bara 25 bostäder, med stora fönster, terrasser som är en del av vardagen och öppen utsikt över Medelhavet.')
a('Each home has its own outdoor space and private pool. Residents share a gym, an outdoor pool with a sunbathing area and a multi-purpose space for working or studying. The developer’s documents give no completion date, so none is quoted here.',
  'Cada vivienda tiene su propio espacio exterior y piscina privada. Los residentes comparten un gimnasio, una piscina exterior con zona de solárium y un espacio polivalente para trabajar o estudiar. Los documentos del promotor no indican fecha de entrega, por lo que aquí no se cita ninguna.',
  'Chaque maison dispose de son propre espace extérieur et d’une piscine privée. Les résidents partagent une salle de sport, une piscine extérieure avec un espace solarium et un espace polyvalent pour travailler ou étudier. Les documents du promoteur ne donnent aucune date de livraison ; aucune n’est donc indiquée ici.',
  'Jedes Haus hat einen eigenen Außenbereich und einen privaten Pool. Die Bewohner teilen sich einen Fitnessraum, einen Außenpool mit Liegefläche und einen Mehrzweckraum zum Arbeiten oder Lernen. Die Unterlagen des Bauträgers nennen keinen Fertigstellungstermin, daher wird hier keiner angegeben.',
  'У каждого дома есть собственное открытое пространство и частный бассейн. Жители пользуются общим тренажёрным залом, открытым бассейном с зоной для загара и многофункциональным помещением для работы или учёбы. В документах застройщика нет срока завершения, поэтому здесь он не указан.',
  'لكل منزل مساحة خارجية خاصة ومسبح خاص. ويتشارك السكان صالة رياضية ومسبحًا خارجيًا بمنطقة للتشمس وقاعة متعددة الاستخدامات للعمل أو الدراسة. لا تذكر وثائق المطوّر موعد الإنجاز، لذلك لا نورد موعدًا هنا.',
  'Elke woning heeft een eigen buitenruimte en een privézwembad. De bewoners delen een fitnessruimte, een buitenzwembad met zonneterras en een multifunctionele ruimte om te werken of te studeren. De documenten van de ontwikkelaar noemen geen opleveringsdatum, dus er wordt hier geen genoemd.',
  'Każdy dom ma własną przestrzeń zewnętrzną i prywatny basen. Mieszkańcy korzystają ze wspólnej siłowni, basenu zewnętrznego ze strefą do opalania oraz sali wielofunkcyjnej do pracy lub nauki. Dokumenty dewelopera nie podają terminu ukończenia, dlatego nie jest tu wskazany żaden.',
  'Hver bolig har egen utendørs plass og privat basseng. Beboerne deler et treningsrom, et utendørsbasseng med solplass og et flerbruksrom for arbeid eller studier. Utbyggerens dokumenter oppgir ingen ferdigstillelsesdato, så ingen er oppgitt her.',
  'Varje bostad har egen utomhusyta och privat pool. De boende delar ett gym, en utomhuspool med solplats och ett flexibelt rum för arbete eller studier. Exploatörens dokument anger inget färdigställandedatum, så inget anges här.')
a('25 homes', '25 viviendas', '25 maisons', '25 Häuser', '25 домов', '25 منزلًا', '25 woningen', '25 domów', '25 boliger', '25 bostäder')
a('Townhouses with a private pool and large terraces, in a development of only 25 homes.',
  'Adosados con piscina privada y grandes terrazas, en una promoción de solo 25 viviendas.',
  'Maisons mitoyennes avec piscine privée et grandes terrasses, dans un programme de seulement 25 maisons.',
  'Reihenhäuser mit privatem Pool und großen Terrassen in einem Projekt mit nur 25 Häusern.',
  'Таунхаусы с частным бассейном и большими террасами в комплексе всего из 25 домов.',
  'منازل متلاصقة بمسبح خاص وتراسات واسعة، في مشروع من 25 منزلًا فقط.',
  'Rijwoningen met een privézwembad en grote terrassen, in een project van slechts 25 woningen.',
  'Domy szeregowe z prywatnym basenem i dużymi tarasami, w inwestycji liczącej tylko 25 domów.',
  'Rekkehus med privat basseng og store terrasser, i et prosjekt med bare 25 boliger.',
  'Radhus med privat pool och stora terrasser, i ett projekt med bara 25 bostäder.')
a('Buyers who want a house rather than an apartment, with a private pool, large terraces and a gym and pool to share, at El Higuerón in Fuengirola.',
  'Compradores que prefieren una casa a un apartamento, con piscina privada, grandes terrazas y un gimnasio y una piscina compartidos, en El Higuerón, Fuengirola.',
  'Acheteurs qui préfèrent une maison à un appartement, avec piscine privée, grandes terrasses et salle de sport et piscine communes, à El Higuerón, Fuengirola.',
  'Käufer, die ein Haus statt einer Wohnung suchen, mit privatem Pool, großen Terrassen sowie gemeinsamem Fitnessraum und Pool, in El Higuerón, Fuengirola.',
  'Покупателям, которым нужен дом, а не квартира: с частным бассейном, большими террасами, общим тренажёрным залом и бассейном, в Эль-Игероне, Фуэнхирола.',
  'للمشترين الذين يفضلون منزلًا على شقة، بمسبح خاص وتراسات واسعة وصالة رياضية ومسبح مشتركين، في إل إيغيرون بفوينخيرولا.',
  'Kopers die een huis verkiezen boven een appartement, met een privézwembad, grote terrassen en een gedeelde fitnessruimte en zwembad, in El Higuerón, Fuengirola.',
  'Dla kupujących, którzy wolą dom od mieszkania: z prywatnym basenem, dużymi tarasami oraz wspólną siłownią i basenem, w El Higuerón w Fuengiroli.',
  'Kjøpere som vil ha et hus fremfor en leilighet, med privat basseng, store terrasser og felles treningsrom og basseng, i El Higuerón i Fuengirola.',
  'Köpare som vill ha ett hus snarare än en lägenhet, med privat pool, stora terrasser samt gemensamt gym och gemensam pool, i El Higuerón i Fuengirola.')
a('A small scale of 25 homes, a private pool in every home, underfloor heating throughout and homes of 140 to 229 sqm built.',
  'Una escala reducida de 25 viviendas, piscina privada en cada una, suelo radiante en toda la vivienda y casas de 140 a 229 {U} construidos.',
  'Une échelle réduite de 25 maisons, une piscine privée dans chacune, un plancher chauffant dans toute la maison et des maisons de 140 à 229 {U} construits.',
  'Eine kleine Anlage mit 25 Häusern, privatem Pool in jedem Haus, Fußbodenheizung im ganzen Haus und Häusern mit 140 bis 229 {U} bebauter Fläche.',
  'Небольшой комплекс из 25 домов, частный бассейн у каждого, тёплые полы во всём доме и дома площадью застройки от 140 до 229 {U}.',
  'مشروع صغير من 25 منزلًا، لكل منزل مسبح خاص، وتدفئة أرضية في المنزل كله، ومنازل مساحتها المبنية من 140 إلى 229 {U}.',
  'Een kleinschalig project van 25 woningen, een privézwembad bij elke woning, vloerverwarming door het hele huis en woningen van 140 tot 229 {U} bebouwd.',
  'Niewielka skala 25 domów, prywatny basen przy każdym, ogrzewanie podłogowe w całym domu i domy o powierzchni zabudowy od 140 do 229 {U}.',
  'Liten skala med 25 boliger, privat basseng ved hver bolig, gulvvarme i hele boligen og boliger på 140 til 229 {U} bygd areal.',
  'Liten skala med 25 bostäder, privat pool vid varje bostad, golvvärme i hela bostaden och bostäder på 140 till 229 {U} byggyta.')
a('The brochure describes El Higuerón as elevated, with open views of the Mediterranean. Its map marks the A-7 and AP-7 roads, the beaches of Carvajal, Torreblanca, Fuengirola and Torremuelle and several golf courses, and gives no distances.',
  'El folleto describe El Higuerón como un lugar elevado, con vistas abiertas al Mediterráneo. Su mapa marca las carreteras A-7 y AP-7, las playas de Carvajal, Torreblanca, Fuengirola y Torremuelle y varios campos de golf, y no da distancias.',
  'La brochure décrit El Higuerón comme un site en hauteur, avec des vues dégagées sur la Méditerranée. Sa carte indique les routes A-7 et AP-7, les plages de Carvajal, Torreblanca, Fuengirola et Torremuelle et plusieurs golfs, sans donner de distances.',
  'Die Broschüre beschreibt El Higuerón als erhöhte Lage mit offenem Blick auf das Mittelmeer. Ihre Karte zeigt die Straßen A-7 und AP-7, die Strände von Carvajal, Torreblanca, Fuengirola und Torremuelle sowie mehrere Golfplätze und nennt keine Entfernungen.',
  'В брошюре Эль-Игерон описан как возвышенное место с открытым видом на Средиземное море. На её карте отмечены дороги A-7 и AP-7, пляжи Карвахаль, Торреблянка, Фуэнхирола и Торремуэлье и несколько полей для гольфа; расстояния не указаны.',
  'تصف النشرة إل إيغيرون بأنه موقع مرتفع بإطلالات مفتوحة على البحر المتوسط. وتُظهر خريطتها طريقي A-7 وAP-7 وشواطئ كارفاخال وتوريبلانكا وفوينخيرولا وتوريمويِّه وعدة ملاعب غولف، ولا تذكر مسافات.',
  'De brochure beschrijft El Higuerón als een verhoogde plek met open uitzicht op de Middellandse Zee. De kaart toont de wegen A-7 en AP-7, de stranden van Carvajal, Torreblanca, Fuengirola en Torremuelle en meerdere golfbanen, zonder afstanden te geven.',
  'Broszura opisuje El Higuerón jako miejsce położone wysoko, z otwartym widokiem na Morze Śródziemne. Jej mapa wskazuje drogi A-7 i AP-7, plaże Carvajal, Torreblanca, Fuengirola i Torremuelle oraz kilka pól golfowych, ale nie podaje odległości.',
  'Brosjyren beskriver El Higuerón som et høyt beliggende sted med åpen utsikt mot Middelhavet. Kartet viser veiene A-7 og AP-7, strendene Carvajal, Torreblanca, Fuengirola og Torremuelle og flere golfbaner, men oppgir ingen avstander.',
  'Broschyren beskriver El Higuerón som ett högt beläget område med öppen utsikt över Medelhavet. Kartan visar vägarna A-7 och AP-7, stränderna Carvajal, Torreblanca, Fuengirola och Torremuelle och flera golfbanor, men anger inga avstånd.')
a('Why check the delivery',
  'Por qué comprobar la entrega', 'Pourquoi vérifier la livraison', 'Warum wir den Fertigstellungstermin prüfen', 'Почему стоит проверить срок сдачи',
  'لماذا نتحقق من موعد التسليم', 'Waarom de oplevering controleren', 'Dlaczego warto sprawdzić termin odbioru', 'Hvorfor sjekke overleveringen', 'Varför kontrollera tillträdet')
a('None of the developer’s documents gives a completion date or a building status, so we ask for the date, the licence and the start of the works in writing before any reservation.',
  'Ninguno de los documentos del promotor indica una fecha de entrega ni el estado de la obra, por lo que pedimos por escrito la fecha, la licencia y el inicio de las obras antes de cualquier reserva.',
  'Aucun document du promoteur ne donne de date de livraison ni d’état d’avancement ; nous demandons donc par écrit la date, le permis et le début des travaux avant toute réservation.',
  'Keine der Unterlagen des Bauträgers nennt einen Fertigstellungstermin oder den Baustand, daher fragen wir vor jeder Reservierung schriftlich den Termin, die Genehmigung und den Baubeginn an.',
  'Ни в одном документе застройщика нет срока завершения или статуса строительства, поэтому перед любым бронированием мы письменно запрашиваем дату, разрешение и начало работ.',
  'لا تذكر أي من وثائق المطوّر موعد الإنجاز أو حالة البناء، لذلك نطلب كتابةً الموعد والرخصة وبدء الأعمال قبل أي حجز.',
  'Geen van de documenten van de ontwikkelaar noemt een opleveringsdatum of een bouwstatus, dus we vragen vóór elke reservering schriftelijk naar de datum, de vergunning en de start van de werken.',
  'Żaden z dokumentów dewelopera nie podaje terminu ukończenia ani stanu budowy, dlatego przed każdą rezerwacją prosimy na piśmie o termin, pozwolenie i datę rozpoczęcia prac.',
  'Ingen av utbyggerens dokumenter oppgir en ferdigstillelsesdato eller byggestatus, så vi ber skriftlig om datoen, tillatelsen og oppstarten av arbeidene før enhver reservasjon.',
  'Inget av exploatörens dokument anger ett färdigställandedatum eller byggstatus, så vi ber skriftligen om datum, bygglov och byggstart före varje bokning.')
a('Five groups of homes, <em>stepping down the hill</em>',
  'Cinco conjuntos, <em>escalonados por la ladera</em>', 'Cinq ensembles, <em>en gradins sur la colline</em>', 'Fünf Gruppen, <em>stufenweise den Hang hinab</em>',
  'Пять групп домов, <em>спускающихся по склону уступами</em>', 'خمس مجموعات من المنازل، <em>تتدرج على سفح التل</em>', 'Vijf groepen woningen, <em>trapsgewijs langs de heuvel</em>',
  'Pięć grup domów, <em>schodzących tarasowo po zboczu</em>', 'Fem grupper boliger, <em>som trapper seg nedover åssiden</em>', 'Fem grupper av bostäder, <em>som trappar ner längs sluttningen</em>')
a('The development is five groups of homes on different levels of the slope, which the brochure calls a staggered architecture that follows the terrain. The homes are townhouses with a living level and a bedroom level and, in types C, D and E, a third level with a solarium and the private pool.',
  'La promoción son cinco conjuntos de viviendas a distintos niveles de la pendiente, lo que el folleto llama una arquitectura escalonada que sigue el terreno. Las viviendas son adosados con una planta de salón y una planta de dormitorios y, en los tipos C, D y E, una tercera planta con solárium y la piscina privada.',
  'Le programme compte cinq ensembles de maisons à différents niveaux de la pente, ce que la brochure appelle une architecture en gradins qui suit le terrain. Ce sont des maisons mitoyennes avec un niveau séjour et un niveau chambres et, pour les types C, D et E, un troisième niveau avec solarium et la piscine privée.',
  'Das Projekt besteht aus fünf Gruppen von Häusern auf verschiedenen Ebenen des Hangs, was die Broschüre als gestaffelte Architektur bezeichnet, die dem Gelände folgt. Die Häuser sind Reihenhäuser mit einer Wohnebene und einer Schlafebene und bei den Typen C, D und E mit einer dritten Ebene mit Solarium und dem privaten Pool.',
  'Комплекс состоит из пяти групп домов на разных уровнях склона; брошюра называет это ступенчатой архитектурой, следующей рельефу. Дома — таунхаусы с жилым и спальным уровнями, а в типах C, D и E есть третий уровень с солярием и частным бассейном.',
  'يتألف المشروع من خمس مجموعات من المنازل على مستويات مختلفة من المنحدر، وتصفه النشرة بعمارة متدرجة تتبع التضاريس. والمنازل متلاصقة بمستوى للمعيشة ومستوى لغرف النوم، وفي الأنواع C وD وE مستوى ثالث فيه سولاريوم والمسبح الخاص.',
  'Het project bestaat uit vijf groepen woningen op verschillende niveaus van de helling, wat de brochure een getrapte architectuur noemt die het terrein volgt. De woningen zijn rijwoningen met een woonniveau en een slaapniveau en, bij de types C, D en E, een derde niveau met een solarium en het privézwembad.',
  'Inwestycję tworzy pięć grup domów na różnych poziomach zbocza, co broszura nazywa architekturą tarasową podążającą za terenem. Domy szeregowe mają poziom dzienny i poziom sypialni, a w typach C, D i E trzeci poziom z solarium i prywatnym basenem.',
  'Prosjektet er fem grupper boliger på ulike nivåer i skråningen, noe brosjyren kaller en trappet arkitektur som følger terrenget. Boligene er rekkehus med et stueplan og et soveplan og, i type C, D og E, et tredje plan med solterrasse og det private bassenget.',
  'Projektet är fem grupper av bostäder på olika nivåer i sluttningen, vilket broschyren kallar en trappad arkitektur som följer terrängen. Bostäderna är radhus med ett vardagsplan och ett sovplan och, i typerna C, D och E, ett tredje plan med solterrass och den privata poolen.')
a('The brochure describes clean lines, continuous materials, neutral tones and interiors that open to the landscape. The images are illustrations of that intention.',
  'El folleto habla de líneas limpias, materiales continuos, tonos neutros e interiores que se abren al paisaje. Las imágenes son ilustraciones de esa intención.',
  'La brochure parle de lignes épurées, de matériaux continus, de tons neutres et d’intérieurs ouverts sur le paysage. Les images illustrent cette intention.',
  'Die Broschüre beschreibt klare Linien, durchgehende Materialien, neutrale Töne und Innenräume, die sich zur Landschaft öffnen. Die Bilder sind Illustrationen dieser Absicht.',
  'В брошюре говорится о чистых линиях, непрерывных материалах, нейтральных тонах и интерьерах, открытых ландшафту. Изображения лишь иллюстрируют этот замысел.',
  'تصف النشرة خطوطًا نظيفة ومواد متصلة وألوانًا محايدة وفضاءات داخلية تنفتح على المشهد الطبيعي. والصور توضيحات لهذه الفكرة.',
  'De brochure beschrijft zuivere lijnen, doorlopende materialen, neutrale tinten en interieurs die zich naar het landschap openen. De beelden zijn illustraties van dat uitgangspunt.',
  'Broszura opisuje czyste linie, ciągłe materiały, neutralne kolory i wnętrza otwarte na krajobraz. Obrazy są ilustracją tego zamysłu.',
  'Brosjyren beskriver rene linjer, sammenhengende materialer, nøytrale toner og interiører som åpner seg mot landskapet. Bildene er illustrasjoner av denne intensjonen.',
  'Broschyren beskriver rena linjer, sammanhängande material, neutrala toner och interiörer som öppnar sig mot landskapet. Bilderna är illustrationer av den tanken.')
a('Reinforced concrete foundations and structure to the Technical Building Code, with independent quality control and a ten-year building warranty insurance.',
  'Cimentación y estructura de hormigón armado conforme al Código Técnico de la Edificación, con control de calidad independiente y seguro decenal de la edificación.',
  'Fondations et structure en béton armé conformes au Code technique du bâtiment, avec contrôle de qualité indépendant et assurance décennale de la construction.',
  'Fundamente und Tragwerk aus Stahlbeton nach dem spanischen Technischen Baukodex, mit unabhängiger Qualitätskontrolle und einer zehnjährigen Bauwerksversicherung.',
  'Железобетонные фундамент и каркас по Техническому строительному кодексу Испании, с независимым контролем качества и десятилетней страховкой на строительство.',
  'أساسات وهيكل من الخرسانة المسلحة وفق الكود الفني للبناء، مع رقابة جودة مستقلة وتأمين ضمان البناء لعشر سنوات.',
  'Fundering en constructie van gewapend beton volgens de Spaanse technische bouwcode, met onafhankelijke kwaliteitscontrole en een tienjarige bouwgarantieverzekering.',
  'Fundamenty i konstrukcja żelbetowa zgodnie z hiszpańskim Kodeksem Technicznym Budownictwa, z niezależną kontrolą jakości i dziesięcioletnim ubezpieczeniem gwarancyjnym budynku.',
  'Fundamenter og konstruksjon i armert betong etter den spanske tekniske byggekoden, med uavhengig kvalitetskontroll og en tiårig byggeforsikring.',
  'Grund och stomme i armerad betong enligt den spanska tekniska byggkoden, med oberoende kvalitetskontroll och en tioårig byggförsäkring.')
a('Flat, waterproofed and insulated roofs, accessible only for maintenance except on usable terraces.',
  'Cubiertas planas, impermeabilizadas y aisladas, accesibles solo para mantenimiento salvo en las terrazas de uso.',
  'Toitures plates, étanchéifiées et isolées, accessibles uniquement pour l’entretien sauf sur les terrasses d’usage.',
  'Flachdächer, abgedichtet und gedämmt, nur zu Wartungszwecken zugänglich, außer auf nutzbaren Terrassen.',
  'Плоские гидроизолированные и утеплённые кровли, доступные только для обслуживания, за исключением эксплуатируемых террас.',
  'أسقف مسطحة معزولة مائيًا وحراريًا، لا يُسمح بالصعود إليها إلا للصيانة باستثناء التراسات المخصصة للاستخدام.',
  'Platte daken, waterdicht en geïsoleerd, alleen toegankelijk voor onderhoud behalve op de gebruiksterrassen.',
  'Dachy płaskie, hydroizolowane i ocieplone, dostępne tylko w celach konserwacyjnych, z wyjątkiem tarasów użytkowych.',
  'Flate, tettede og isolerte tak, kun tilgjengelige for vedlikehold unntatt på terrassene som brukes.',
  'Platta, tätade och isolerade tak, endast åtkomliga för underhåll utom på terrasser som används.')
a('A selection of materials and finishes for durability and energy efficiency. The specification does not name them.',
  'Una selección de materiales y acabados por su durabilidad y eficiencia energética. La memoria de calidades no los nombra.',
  'Une sélection de matériaux et de finitions pour la durabilité et l’efficacité énergétique. Le descriptif ne les nomme pas.',
  'Eine Auswahl an Materialien und Oberflächen für Langlebigkeit und Energieeffizienz. Die Baubeschreibung nennt sie nicht.',
  'Подбор материалов и отделки с расчётом на долговечность и энергоэффективность. Спецификация их не называет.',
  'مجموعة منتقاة من المواد والتشطيبات من أجل المتانة وكفاءة الطاقة. ولا تسمّيها المواصفات.',
  'Een selectie van materialen en afwerkingen voor duurzaamheid en energie-efficiëntie. Het lastenboek noemt ze niet.',
  'Dobór materiałów i wykończeń zapewniający trwałość i efektywność energetyczną. Specyfikacja ich nie wymienia.',
  'Et utvalg materialer og overflater for holdbarhet og energieffektivitet. Spesifikasjonen nevner dem ikke.',
  'Ett urval av material och ytskikt för hållbarhet och energieffektivitet. Specifikationen namnger dem inte.')
a('Thermally broken aluminium or PVC joinery with double glazing, motorised blinds in the bedrooms and motorised exterior blinds in the living room.',
  'Carpintería de aluminio con rotura de puente térmico o de PVC con doble acristalamiento, persianas motorizadas en los dormitorios y estores exteriores motorizados en el salón.',
  'Menuiseries en aluminium à rupture de pont thermique ou en PVC avec double vitrage, volets motorisés dans les chambres et stores extérieurs motorisés dans le séjour.',
  'Fenster aus Aluminium mit thermischer Trennung oder aus PVC mit Doppelverglasung, motorisierte Rollläden in den Schlafzimmern und motorisierte Außenstores im Wohnzimmer.',
  'Алюминиевые профили с терморазрывом или ПВХ с двойным остеклением, мотоприводные жалюзи в спальнях и мотоприводные наружные шторы в гостиной.',
  'نجارة من الألمنيوم بكاسر حراري أو من PVC مع زجاج مزدوج، وستائر مزودة بمحرك في غرف النوم وستائر خارجية بمحرك في غرفة المعيشة.',
  'Aluminium kozijnen met thermische onderbreking of pvc met dubbele beglazing, gemotoriseerde rolluiken in de slaapkamers en gemotoriseerde buitenzonwering in de woonkamer.',
  'Stolarka aluminiowa z przerwą termiczną lub z PVC z podwójnym szkleniem, zmotoryzowane rolety w sypialniach i zmotoryzowane żaluzje zewnętrzne w salonie.',
  'Aluminiumsvinduer med termisk brudd eller PVC med dobbeltglass, motoriserte persienner i soverommene og motorisert utvendig solskjerming i stuen.',
  'Aluminiumfönster med termisk brytning eller PVC med dubbelglas, motoriserade rullgardiner i sovrummen och motoriserad utvändig solavskärmning i vardagsrummet.')

# --- quality specs
a('Source: the developer’s quality specification, supplied in English and Spanish and dated 17 April 2026 in its file name. It says that the specification may be amended at the discretion of the project management during the works, with the changes documented.',
  'Fuente: la memoria de calidades del promotor, facilitada en inglés y español y fechada el 17 de abril de 2026 en el nombre de su archivo. Indica que puede modificarse a criterio de la dirección facultativa durante las obras, documentándose los cambios.',
  'Source : le descriptif du promoteur, fourni en anglais et en espagnol et daté du 17 avril 2026 dans le nom de son fichier. Il indique qu’il peut être modifié à la discrétion de la direction de projet pendant les travaux, les changements étant documentés.',
  'Quelle: die Bau- und Ausstattungsbeschreibung des Bauträgers, auf Englisch und Spanisch geliefert und im Dateinamen auf den 17. April 2026 datiert. Sie weist darauf hin, dass sie nach Ermessen der Projektleitung während der Bauarbeiten geändert werden kann, wobei die Änderungen dokumentiert werden.',
  'Источник: строительная спецификация застройщика на английском и испанском языках; в названии файла указана дата 17 апреля 2026 года. В ней сказано, что в ходе работ она может быть изменена по усмотрению руководства проекта с документированием изменений.',
  'المصدر: مواصفات البناء الخاصة بالمطوّر، المقدمة بالإنجليزية والإسبانية والمؤرخة في 17 أبريل 2026 في اسم ملفها. وتنص على أنها قد تُعدَّل بتقدير إدارة المشروع أثناء الأعمال مع توثيق التغييرات.',
  'Bron: de bouwspecificatie van de ontwikkelaar, geleverd in het Engels en Spaans en in de bestandsnaam gedateerd 17 april 2026. Daarin staat dat zij tijdens de werken naar goeddunken van de projectleiding kan worden gewijzigd, waarbij de wijzigingen worden gedocumenteerd.',
  'Źródło: specyfikacja budowlana dewelopera, dostarczona po angielsku i hiszpańsku, z datą 17 kwietnia 2026 r. w nazwie pliku. Zastrzega ona, że w trakcie prac może zostać zmieniona według uznania kierownictwa projektu, z udokumentowaniem zmian.',
  'Kilde: utbyggerens byggespesifikasjon, levert på engelsk og spansk og datert 17. april 2026 i filnavnet. Den sier at den kan endres etter prosjektledelsens skjønn under arbeidene, med dokumenterte endringer.',
  'Källa: exploatörens byggspecifikation, levererad på engelska och spanska och daterad 17 april 2026 i filnamnet. Den anger att den kan ändras efter projektledningens bedömning under arbetena, med dokumenterade ändringar.')
a('Large-format porcelain flooring throughout, including the bathrooms and kitchen, anti-slip ceramic flooring on the terraces, ceramic tiles in the bathrooms and smooth white paint on the other walls and ceilings.',
  'Pavimento continuo de gres porcelánico de gran formato en toda la vivienda, incluidos baños y cocina, pavimento cerámico antideslizante en las terrazas, alicatado cerámico en los baños y pintura lisa blanca en el resto de paredes y techos.',
  'Sol en grès cérame grand format dans toute la maison, salles de bains et cuisine comprises, carrelage antidérapant sur les terrasses, faïence dans les salles de bains et peinture blanche lisse sur les autres murs et plafonds.',
  'Großformatige Feinsteinzeugböden im gesamten Haus, einschließlich Bädern und Küche, rutschhemmende Keramikböden auf den Terrassen, Keramikfliesen in den Bädern und glatter weißer Anstrich an den übrigen Wänden und Decken.',
  'Крупноформатный керамогранит по всему дому, включая ванные и кухню, нескользящая керамика на террасах, керамическая плитка в ванных и гладкая белая краска на остальных стенах и потолках.',
  'أرضيات بورسلان كبيرة المقاس في المنزل كله، بما في ذلك الحمامات والمطبخ، وأرضيات سيراميك مانعة للانزلاق على التراسات، وبلاط سيراميك في الحمامات، ودهان أبيض أملس على بقية الجدران والأسقف.',
  'Grootformaat porseleinen vloeren in het hele huis, ook in de badkamers en de keuken, antislipkeramiek op de terrassen, keramische tegels in de badkamers en gladde witte verf op de overige wanden en plafonds.',
  'Wielkoformatowe płytki gresowe w całym domu, także w łazienkach i kuchni, antypoślizgowa ceramika na tarasach, płytki ceramiczne w łazienkach i gładka biała farba na pozostałych ścianach i sufitach.',
  'Storformat porselensfliser i hele boligen, også på bad og kjøkken, sklisikre keramiske fliser på terrassene, keramiske fliser på badene og glatt hvit maling på øvrige vegger og tak.',
  'Storformat klinker i hela bostaden, även i badrum och kök, halksäkert keramikgolv på terrasserna, keramiska plattor i badrummen och slät vit färg på övriga väggar och tak.')
a('A reinforced security door with satin chrome handles, white lacquered sliding or hinged interior doors with concealed hinges, and modular wardrobes lined in textile-finish melamine with a top shelf, a hanging rail and drawers.',
  'Puerta de entrada acorazada con manivelas cromadas satinadas, puertas interiores correderas o abatibles lacadas en blanco con bisagras ocultas, y armarios empotrados modulares forrados en melamina con acabado textil, con balda superior, barra de colgar y cajonera.',
  'Porte d’entrée blindée avec poignées chrome satiné, portes intérieures coulissantes ou battantes laquées blanc à charnières cachées, et placards modulaires doublés de mélaminé à finition textile avec tablette haute, barre de penderie et tiroirs.',
  'Eine Sicherheitseingangstür mit satinierten Chromgriffen, weiß lackierte Innentüren als Schiebe- oder Drehtüren mit verdeckten Scharnieren und modulare Einbauschränke, innen mit Melamin in Textiloptik ausgekleidet, mit oberer Ablage, Kleiderstange und Schubladen.',
  'Бронированная входная дверь с хромированными сатинированными ручками, белые лакированные раздвижные или распашные межкомнатные двери со скрытыми петлями и модульные шкафы с внутренней отделкой из меламина с текстильной фактурой, с верхней полкой, штангой и ящиками.',
  'باب دخول مصفّح بمقابض كروم ساتان، وأبواب داخلية منزلقة أو مفصلية مطلية باللاكيه الأبيض بمفصلات مخفية، وخزائن مدمجة معيارية مبطنة بالميلامين بلمسة نسيجية مع رف علوي وعمود تعليق وأدراج.',
  'Een pantserdeur met satijnchromen kruk, wit gelakte schuif- of draaideuren met verborgen scharnieren en modulaire inbouwkasten bekleed met melamine in textieloptiek, met een bovenplank, een hangstang en laden.',
  'Drzwi wejściowe antywłamaniowe z satynowymi chromowanymi klamkami, białe lakierowane drzwi wewnętrzne przesuwne lub skrzydłowe z ukrytymi zawiasami oraz modułowe szafy wnękowe wyłożone melaminą o fakturze tkaniny, z półką górną, drążkiem i szufladami.',
  'Sikkerhetsdør med satinert krom på håndtakene, hvitlakkerte skyve- eller svingdører med skjulte hengsler og modulære innebygde skap kledd med melamin med tekstilfinish, med toppheller, kleshenger og skuffer.',
  'Säkerhetsdörr med satinkromade handtag, vitlackerade skjut- eller svängdörrar med dolda gångjärn och modulära garderober klädda med melamin med textilyta, med överhylla, klädstång och lådor.')
a('Delivered fitted with cabinetry, depending on the home type, and with appliances. The specification does not list the appliances.',
  'Se entrega equipada con mobiliario, según la tipología de la vivienda, y con electrodomésticos. La memoria de calidades no enumera los electrodomésticos.',
  'Livrée équipée de meubles, selon le type de maison, et d’électroménager. Le descriptif ne détaille pas l’électroménager.',
  'Wird je nach Haustyp mit Küchenmöbeln und Geräten ausgestattet übergeben. Die Baubeschreibung listet die Geräte nicht auf.',
  'Кухня передаётся с мебелью (в зависимости от типа дома) и техникой. Перечня техники в спецификации нет.',
  'يُسلَّم المطبخ مجهزًا بالخزائن، بحسب نوع المنزل، وبالأجهزة. ولا تذكر المواصفات قائمة الأجهزة.',
  'Wordt geleverd met keukenmeubilair, afhankelijk van het woningtype, en met apparatuur. Het lastenboek somt de apparaten niet op.',
  'Kuchnia jest przekazywana z zabudową, zależnie od typu domu, oraz ze sprzętem. Specyfikacja nie wymienia tego sprzętu.',
  'Leveres med innredning, avhengig av boligtype, og med hvitevarer. Spesifikasjonen lister ikke opp apparatene.',
  'Levereras utrustat med skåp, beroende på bostadstyp, och med vitvaror. Specifikationen listar inte vitvarorna.')
a('White sanitaryware, a wall-hung toilet with a concealed cistern and soft-close seat, chrome single-lever taps, a vanity unit with a washbasin and a backlit anti-fog mirror, and a shower tray built in the same finish as the floor with a sliding glass screen.',
  'Sanitarios blancos, inodoro suspendido con cisterna encastrada y cierre amortiguado, grifería monomando cromada, mueble con lavabo y espejo antivaho retroiluminado, y plato de ducha de obra con el mismo acabado que el suelo y mampara de vidrio corredera.',
  'Sanitaires blancs, WC suspendu avec réservoir encastré et abattant à fermeture douce, robinetterie mitigeur chromée, meuble vasque avec miroir antibuée rétroéclairé, et receveur de douche réalisé dans la même finition que le sol, avec paroi vitrée coulissante.',
  'Weiße Sanitärobjekte, ein Wand-WC mit Unterputzspülkasten und Absenkautomatik, verchromte Einhebelmischer, ein Waschtischunterschrank mit Waschbecken und einem hinterleuchteten Antibeschlag-Spiegel sowie eine Duschfläche im gleichen Finish wie der Boden mit gläserner Schiebetür.',
  'Белая сантехника, подвесной унитаз со скрытым бачком и плавно опускающимся сиденьем, хромированные однорычажные смесители, тумба с раковиной и подсвеченное зеркало с защитой от запотевания, а также душевой поддон, выполненный в той же отделке, что и пол, со стеклянной раздвижной перегородкой.',
  'أدوات صحية بيضاء، ومرحاض معلّق بخزان مخفي ومقعد بإغلاق هادئ، وخلاطات كروم بذراع واحدة، ووحدة حوض مع مرآة مضيئة مضادة للبخار، وقاعدة دش منفذة بنفس تشطيب الأرضية مع حاجز زجاجي منزلق.',
  'Wit sanitair, een wandcloset met inbouwreservoir en soft-closezitting, verchroomde eengreepsmengkranen, een wastafelmeubel met een verlichte antibeslagspiegel en een douchebak in dezelfde afwerking als de vloer met een glazen schuifwand.',
  'Biała ceramika sanitarna, podwieszana toaleta z ukrytym spłuczkiem i deską wolnoopadającą, chromowane baterie jednouchwytowe, szafka z umywalką i podświetlane lustro przeciwparowe oraz brodzik wykonany w tym samym wykończeniu co podłoga, ze szklaną przesuwną kabiną.',
  'Hvit sanitær, et vegghengt toalett med skjult sisterne og mykt lukkende sete, kromblandebatterier med én spak, en servantskap med lyst antidugg-speil og en dusjbunn i samme finish som gulvet med glassskyvedør.',
  'Vit sanitetsporslin, en väggmonterad toalett med dold spolcistern och mjukstängande sits, kromade enhandsblandare, ett tvättställsskåp med bakgrundsbelyst antimist-spegel och en duschplatta i samma utförande som golvet med glasskjutdörr.')
a('Hot water by an aerothermal system and underfloor heating throughout the home, with a climate system as the regulations require.',
  'Agua caliente mediante aerotermia y suelo radiante en toda la vivienda, con un sistema de climatización conforme a la normativa.',
  'Eau chaude par un système aérothermique et plancher chauffant dans toute la maison, avec un système de climatisation conforme à la réglementation.',
  'Warmwasser über ein Luft-Wasser-Wärmepumpensystem und Fußbodenheizung im ganzen Haus, mit einem Klimasystem nach den geltenden Vorschriften.',
  'Горячая вода от аэротермальной системы и тёплые полы во всём доме, а также климатическая система в соответствии с нормами.',
  'ماء ساخن بنظام الطاقة الهوائية الحرارية (أيروثيرميا) وتدفئة أرضية في المنزل كله، مع نظام مناخي وفق اللوائح.',
  'Warm water via een aerothermisch systeem en vloerverwarming door het hele huis, met een klimaatsysteem zoals de regelgeving vereist.',
  'Ciepła woda z systemu aerotermalnego i ogrzewanie podłogowe w całym domu, z systemem klimatyzacji zgodnym z przepisami.',
  'Varmtvann fra et aerotermisk system og gulvvarme i hele boligen, med et klimaanlegg slik regelverket krever.',
  'Varmvatten från ett aerotermiskt system och golvvärme i hela bostaden, med ett klimatsystem enligt föreskrifterna.')
a('The development is to have an energy performance certificate rated A, which is a project-stage rating.',
  'La promoción contará con un certificado de eficiencia energética de calificación A, que es una calificación en fase de proyecto.',
  'Le programme doit obtenir un certificat de performance énergétique de classe A, qui est une note au stade du projet.',
  'Das Projekt soll einen Energieausweis der Klasse A erhalten; dies ist eine Bewertung im Projektstadium.',
  'Комплекс должен получить сертификат энергоэффективности класса A; это оценка на стадии проекта.',
  'سيحصل المشروع على شهادة أداء طاقي بتصنيف A، وهو تصنيف في مرحلة المشروع.',
  'Het project krijgt een energieprestatiecertificaat met label A, een beoordeling in de projectfase.',
  'Inwestycja ma uzyskać świadectwo charakterystyki energetycznej klasy A, czyli ocenę na etapie projektu.',
  'Prosjektet skal få energisertifikat med karakter A, som er en vurdering på prosjektstadiet.',
  'Projektet ska få ett energicertifikat med klass A, vilket är en bedömning på projektstadiet.')
a('A protected electrical installation, television, telephone and fibre-optic points, an automatic video entry phone and a home-automation hub with general on and off lighting control.',
  'Instalación eléctrica protegida, tomas de televisión, telefonía y fibra óptica, videoportero automático y una central domótica con control general de encendido y apagado de la iluminación.',
  'Installation électrique protégée, prises télévision, téléphone et fibre optique, visiophone automatique et centrale domotique avec commande générale marche/arrêt de l’éclairage.',
  'Eine abgesicherte Elektroinstallation, Anschlüsse für Fernsehen, Telefon und Glasfaser, eine automatische Videosprechanlage und eine Hausautomations-Zentrale mit allgemeiner Ein- und Ausschaltung der Beleuchtung.',
  'Защищённая электропроводка, розетки для телевидения, телефона и оптоволокна, автоматический видеодомофон и блок домашней автоматизации с общим включением и выключением освещения.',
  'تمديدات كهربائية محمية، ونقاط للتلفزيون والهاتف والألياف الضوئية، وهاتف مرئي آلي للمدخل، ووحدة أتمتة منزلية مع تحكم عام بتشغيل الإضاءة وإطفائها.',
  'Een beveiligde elektrische installatie, aansluitingen voor tv, telefoon en glasvezel, een automatische videofoon en een domoticacentrale met algemene aan-uitbediening van de verlichting.',
  'Zabezpieczona instalacja elektryczna, gniazda telewizyjne, telefoniczne i światłowodowe, automatyczny wideodomofon oraz centrala automatyki domowej z ogólnym włączaniem i wyłączaniem oświetlenia.',
  'En beskyttet elektrisk installasjon, tilkoblinger for tv, telefon og fiber, automatisk videoporttelefon og en smarthjemsentral med generell av og på-styring av belysningen.',
  'En skyddad elinstallation, uttag för tv, telefon och fiber, automatisk videodörrtelefon och en hemautomationscentral med allmän tänd- och släckstyrning av belysningen.')
a('Private pool and communal areas',
  'Piscina privada y zonas comunes', 'Piscine privée et parties communes', 'Privater Pool und Gemeinschaftsbereiche', 'Частный бассейн и общие зоны',
  'المسبح الخاص والمناطق المشتركة', 'Privézwembad en gemeenschappelijke ruimten', 'Prywatny basen i części wspólne', 'Privat basseng og fellesområder', 'Privat pool och gemensamma ytor')
a('A private swimming pool in each home, built with high-end materials and fitted with a filtration system.',
  'Una piscina privada en cada vivienda, ejecutada con materiales de alta gama y equipada con un sistema de depuración.',
  'Une piscine privée dans chaque maison, réalisée avec des matériaux haut de gamme et équipée d’un système de filtration.',
  'Ein privater Swimmingpool in jedem Haus, aus hochwertigen Materialien gebaut und mit einer Filteranlage ausgestattet.',
  'Частный бассейн в каждом доме, построенный из материалов высокого класса и оснащённый системой фильтрации.',
  'مسبح خاص في كل منزل، منفذ بمواد عالية الجودة ومجهز بنظام ترشيح.',
  'Een privézwembad bij elke woning, gebouwd met hoogwaardige materialen en voorzien van een filtersysteem.',
  'Prywatny basen przy każdym domu, wykonany z wysokiej klasy materiałów i wyposażony w system filtracji.',
  'Et privat svømmebasseng i hver bolig, bygget med høyverdige materialer og utstyrt med filtreringsanlegg.',
  'En privat pool vid varje bostad, byggd med högklassiga material och utrustad med ett filtreringssystem.')
a('Paved and landscaped communal grounds, preferably with native, low-water planting, with LED lighting, a fully equipped gym, an outdoor pool with salt chlorination and a sunbathing area, and a multi-purpose space.',
  'Zonas comunes pavimentadas y ajardinadas, preferentemente con especies autóctonas de bajo consumo de agua, con iluminación LED, un gimnasio totalmente equipado, una piscina exterior con cloración salina y zona de solárium, y un espacio polivalente.',
  'Parties communes pavées et paysagées, de préférence avec des espèces locales peu gourmandes en eau, éclairage LED, une salle de sport entièrement équipée, une piscine extérieure au sel avec un espace solarium, et un espace polyvalent.',
  'Gepflasterte und begrünte Gemeinschaftsflächen, vorzugsweise mit heimischer, wassersparender Bepflanzung, mit LED-Beleuchtung, einem voll ausgestatteten Fitnessraum, einem Außenpool mit Salzchlorierung und Liegefläche sowie einem Mehrzweckraum.',
  'Вымощенная и озеленённая общая территория, преимущественно местными растениями с низким водопотреблением, светодиодное освещение, полностью оборудованный тренажёрный зал, открытый бассейн с солевым хлорированием и зоной для загара, а также многофункциональное помещение.',
  'مناطق مشتركة مرصوفة ومشجّرة، يفضّل بنباتات محلية قليلة استهلاك المياه، مع إضاءة LED وصالة رياضية مجهزة بالكامل ومسبح خارجي بتعقيم بالملح ومنطقة للتشمس وقاعة متعددة الاستخدامات.',
  'Bestrate en beplante gemeenschappelijke buitenruimten, bij voorkeur met inheemse, waterzuinige beplanting, met ledverlichting, een volledig uitgeruste fitnessruimte, een buitenzwembad met zoutchlorering en een zonneterras, en een multifunctionele ruimte.',
  'Utwardzone i obsadzone tereny wspólne, najchętniej rodzimymi roślinami o niskim zapotrzebowaniu na wodę, z oświetleniem LED, w pełni wyposażoną siłownią, basenem zewnętrznym z elektrolizą soli i strefą do opalania oraz salą wielofunkcyjną.',
  'Brulagte og beplantede fellesområder, helst med stedegne, vannsparende arter, med LED-belysning, et fullt utstyrt treningsrom, et utendørsbasseng med saltklorering og solplass, og et flerbruksrom.',
  'Stensatta och planterade gemensamma ytor, helst med inhemska, vattensnåla växter, med LED-belysning, ett fullt utrustat gym, en utomhuspool med saltklorering och solplats samt ett flexibelt rum.')
a('Garage and lifts',
  'Garaje y ascensores', 'Garage et ascenseurs', 'Garage und Aufzüge', 'Гараж и лифты', 'المرآب والمصاعد', 'Garage en liften', 'Garaż i windy', 'Garasje og heiser', 'Garage och hissar')
a('A garage with vehicle access, a polished concrete floor and a fire-fighting system, electric lifts, and a pre-installation for electric-vehicle charging through an accessible conduit to each parking space.',
  'Un garaje con acceso de vehículos, suelo de hormigón pulido e instalación contraincendios, ascensores eléctricos y una preinstalación de recarga de vehículos eléctricos mediante canalización accesible hasta cada plaza.',
  'Un garage avec accès pour véhicules, sol en béton poli et installation de protection incendie, des ascenseurs électriques et une pré-installation de recharge pour véhicules électriques par conduit accessible jusqu’à chaque place.',
  'Eine Garage mit Fahrzeugzufahrt, poliertem Betonboden und Brandschutzanlage, elektrische Aufzüge und eine Vorinstallation für das Laden von Elektrofahrzeugen über einen zugänglichen Leerrohrweg zu jedem Stellplatz.',
  'Гараж с въездом для автомобилей, полированным бетонным полом и противопожарной системой, электрические лифты и подготовка под зарядку электромобилей через доступный кабель-канал к каждому парковочному месту.',
  'مرآب بمدخل للسيارات وأرضية خرسانية مصقولة ونظام مكافحة حريق، ومصاعد كهربائية، وتجهيز مسبق لشحن السيارات الكهربائية عبر قناة يسهل الوصول إليها عند كل موقف.',
  'Een garage met toegang voor voertuigen, een gepolijste betonvloer en een brandbeveiligingsinstallatie, elektrische liften en een voorbereiding voor het laden van elektrische auto’s via een toegankelijke leiding naar elke parkeerplaats.',
  'Garaż z wjazdem dla pojazdów, polerowaną posadzką betonową i instalacją przeciwpożarową, windy elektryczne oraz przygotowanie do ładowania pojazdów elektrycznych przez dostępny kanał przy każdym miejscu parkingowym.',
  'En garasje med kjøretøyadkomst, polert betonggulv og brannsikringsanlegg, elektriske heiser og forberedelse for lading av elbil gjennom tilgjengelig føringsrør til hver parkeringsplass.',
  'Ett garage med infart för fordon, polerat betonggolv och brandskyddsanläggning, elhissar och förberedelse för laddning av elbil genom ett åtkomligt kabelrör till varje parkeringsplats.')

# --- residences
a('Three groups of plans, <em>one development</em>',
  'Tres grupos de planos, <em>una sola promoción</em>', 'Trois groupes de plans, <em>un seul programme</em>', 'Drei Plangruppen, <em>ein Projekt</em>',
  'Три группы планировок, <em>один комплекс</em>', 'ثلاث مجموعات من المخططات، <em>مشروع واحد</em>', 'Drie groepen plattegronden, <em>één project</em>',
  'Trzy grupy rzutów, <em>jedna inwestycja</em>', 'Tre grupper planer, <em>ett prosjekt</em>', 'Tre grupper av planritningar, <em>ett projekt</em>')
a('The plans are drawn home by home and the homes are lettered A to E. The table below lists the 18 homes with a price.',
  'Los planos están dibujados vivienda por vivienda y las viviendas se designan con letras de la A a la E. La tabla siguiente recoge las 18 viviendas con precio.',
  'Les plans sont dessinés maison par maison et les maisons sont désignées par les lettres A à E. Le tableau ci-dessous présente les 18 maisons avec un prix.',
  'Die Pläne sind für jedes Haus einzeln gezeichnet, und die Häuser sind mit den Buchstaben A bis E bezeichnet. Die folgende Tabelle listet die 18 Häuser mit Preis auf.',
  'Планировки выполнены для каждого дома отдельно, дома обозначены буквами от A до E. В таблице ниже перечислены 18 домов с ценой.',
  'المخططات مرسومة لكل منزل على حدة، والمنازل مصنفة بالحروف من A إلى E. يعرض الجدول أدناه المنازل الثمانية عشر التي لها سعر.',
  'De plattegronden zijn per woning getekend en de woningen zijn met de letters A tot en met E aangeduid. De tabel hieronder toont de 18 woningen met een prijs.',
  'Rzuty są rysowane dla każdego domu osobno, a domy oznaczono literami od A do E. Poniższa tabela zawiera 18 domów z ceną.',
  'Planene er tegnet bolig for bolig, og boligene er merket med bokstavene A til E. Tabellen nedenfor viser de 18 boligene med pris.',
  'Planritningarna är ritade bostad för bostad och bostäderna betecknas med bokstäverna A till E. Tabellen nedan visar de 18 bostäderna med pris.')
a('Homes A and B', 'Viviendas A y B', 'Maisons A et B', 'Häuser A und B', 'Дома A и B', 'المنازل A وB', 'Woningen A en B', 'Domy A i B', 'Bolig A og B', 'Bostäderna A och B')
a('5 homes listed, all with three bedrooms and three bathrooms, of 140.00 to 189.99 sqm built, on two levels: a living level and a bedroom level.',
  '5 viviendas en lista, todas de tres dormitorios y tres baños, de {N140.00} a {N189.99} {U} construidos, en dos plantas: una planta de salón y una de dormitorios.',
  '5 maisons listées, toutes de trois chambres et trois salles de bains, de {N140.00} à {N189.99} {U} construits, sur deux niveaux : un niveau séjour et un niveau chambres.',
  '5 gelistete Häuser, alle mit drei Schlafzimmern und drei Bädern, mit {N140.00} bis {N189.99} {U} bebauter Fläche, auf zwei Ebenen: einer Wohnebene und einer Schlafebene.',
  '5 домов в списке, все с тремя спальнями и тремя ванными, площадью застройки от {N140.00} до {N189.99} {U}, на двух уровнях: жилом и спальном.',
  '5 منازل مدرجة، جميعها بثلاث غرف نوم وثلاثة حمامات، بمساحة مبنية من {N140.00} إلى {N189.99} {U}، على مستويين: مستوى للمعيشة ومستوى لغرف النوم.',
  '5 vermelde woningen, allemaal met drie slaapkamers en drie badkamers, van {N140.00} tot {N189.99} {U} bebouwd, op twee niveaus: een woonniveau en een slaapniveau.',
  '5 domów na liście, wszystkie z trzema sypialniami i trzema łazienkami, o powierzchni zabudowy od {N140.00} do {N189.99} {U}, na dwóch poziomach: dziennym i sypialni.',
  '5 oppførte boliger, alle med tre soverom og tre bad, på {N140.00} til {N189.99} {U} bygd areal, på to plan: et stueplan og et soveplan.',
  '5 listade bostäder, alla med tre sovrum och tre badrum, på {N140.00} till {N189.99} {U} byggyta, på två plan: ett vardagsplan och ett sovplan.')
a('On the plans the private pool sits in the garden beside the living level. Gardens are 30.73 to 47.70 sqm and terraces 30.33 to 64.00 sqm.',
  'En los planos la piscina privada está en el jardín, junto a la planta de salón. Los jardines miden de {N30.73} a {N47.70} {U} y las terrazas de {N30.33} a {N64.00} {U}.',
  'Sur les plans, la piscine privée se trouve dans le jardin, à côté du niveau séjour. Les jardins font de {N30.73} à {N47.70} {U} et les terrasses de {N30.33} à {N64.00} {U}.',
  'Auf den Plänen liegt der private Pool im Garten neben der Wohnebene. Die Gärten messen {N30.73} bis {N47.70} {U} und die Terrassen {N30.33} bis {N64.00} {U}.',
  'На планах частный бассейн расположен в саду рядом с жилым уровнем. Сады — от {N30.73} до {N47.70} {U}, террасы — от {N30.33} до {N64.00} {U}.',
  'في المخططات يقع المسبح الخاص في الحديقة بجانب مستوى المعيشة. مساحة الحدائق من {N30.73} إلى {N47.70} {U} والتراسات من {N30.33} إلى {N64.00} {U}.',
  'Op de plattegronden ligt het privézwembad in de tuin naast het woonniveau. De tuinen meten {N30.73} tot {N47.70} {U} en de terrassen {N30.33} tot {N64.00} {U}.',
  'Na rzutach prywatny basen znajduje się w ogrodzie obok poziomu dziennego. Ogrody mają od {N30.73} do {N47.70} {U}, a tarasy od {N30.33} do {N64.00} {U}.',
  'På tegningene ligger det private bassenget i hagen ved stueplanet. Hagene er på {N30.73} til {N47.70} {U} og terrassene på {N30.33} til {N64.00} {U}.',
  'På ritningarna ligger den privata poolen i trädgården bredvid vardagsplanet. Trädgårdarna är på {N30.73} till {N47.70} {U} och terrasserna på {N30.33} till {N64.00} {U}.')
a('Prices run from EUR 789,000 to EUR 913,000.',
  'Los precios van de {E789000} a {E913000}.', 'Les prix vont de {E789000} à {E913000}.', 'Die Preise reichen von {E789000} bis {E913000}.',
  'Цены — от {E789000} до {E913000}.', 'تتراوح الأسعار من {E789000} إلى {E913000}.', 'De prijzen lopen van {E789000} tot {E913000}.',
  'Ceny wahają się od {E789000} do {E913000}.', 'Prisene går fra {E789000} til {E913000}.', 'Priserna går från {E789000} till {E913000}.')
a('Homes C and D', 'Viviendas C y D', 'Maisons C et D', 'Häuser C und D', 'Дома C и D', 'المنازل C وD', 'Woningen C en D', 'Domy C i D', 'Bolig C og D', 'Bostäderna C och D')
a('9 homes listed, 6 with three bedrooms and 3 with four, all with three bathrooms, of 158.61 to 227.19 sqm built, on three levels: living, bedroom and solarium, where the private pool sits.',
  '9 viviendas en lista, 6 de tres dormitorios y 3 de cuatro, todas con tres baños, de {N158.61} a {N227.19} {U} construidos, en tres plantas: salón, dormitorios y solárium, donde está la piscina privada.',
  '9 maisons listées, 6 de trois chambres et 3 de quatre, toutes avec trois salles de bains, de {N158.61} à {N227.19} {U} construits, sur trois niveaux : séjour, chambres et solarium, où se trouve la piscine privée.',
  '9 gelistete Häuser, 6 mit drei und 3 mit vier Schlafzimmern, alle mit drei Bädern, mit {N158.61} bis {N227.19} {U} bebauter Fläche, auf drei Ebenen: Wohnen, Schlafen und Solarium, wo der private Pool liegt.',
  '9 домов в списке, 6 с тремя спальнями и 3 с четырьмя, все с тремя ванными, площадью застройки от {N158.61} до {N227.19} {U}, на трёх уровнях: жилом, спальном и солярии, где находится частный бассейн.',
  '9 منازل مدرجة، 6 منها بثلاث غرف نوم و3 بأربع، وجميعها بثلاثة حمامات، بمساحة مبنية من {N158.61} إلى {N227.19} {U}، على ثلاثة مستويات: المعيشة وغرف النوم والسولاريوم حيث يقع المسبح الخاص.',
  '9 vermelde woningen, 6 met drie en 3 met vier slaapkamers, allemaal met drie badkamers, van {N158.61} tot {N227.19} {U} bebouwd, op drie niveaus: wonen, slapen en solarium, waar het privézwembad ligt.',
  '9 domów na liście, 6 z trzema i 3 z czterema sypialniami, wszystkie z trzema łazienkami, o powierzchni zabudowy od {N158.61} do {N227.19} {U}, na trzech poziomach: dziennym, sypialni i solarium, gdzie znajduje się prywatny basen.',
  '9 oppførte boliger, 6 med tre og 3 med fire soverom, alle med tre bad, på {N158.61} til {N227.19} {U} bygd areal, på tre plan: stue, soverom og solterrasse, der det private bassenget ligger.',
  '9 listade bostäder, 6 med tre och 3 med fyra sovrum, alla med tre badrum, på {N158.61} till {N227.19} {U} byggyta, på tre plan: vardag, sovrum och solterrass, där den privata poolen ligger.')
a('Terraces of 62.47 to 108.50 sqm. The list shows a garden for only two of them: 86.02 sqm for C.01 and 32.72 sqm for D.02.',
  'Terrazas de {N62.47} a {N108.50} {U}. La lista muestra jardín solo en dos de ellas: {N86.02} {U} en la C.01 y {N32.72} {U} en la D.02.',
  'Terrasses de {N62.47} à {N108.50} {U}. La liste n’indique un jardin que pour deux d’entre elles : {N86.02} {U} pour la C.01 et {N32.72} {U} pour la D.02.',
  'Terrassen von {N62.47} bis {N108.50} {U}. Die Liste weist nur bei zwei Häusern einen Garten aus: {N86.02} {U} bei C.01 und {N32.72} {U} bei D.02.',
  'Террасы — от {N62.47} до {N108.50} {U}. Сад в списке указан только у двух домов: {N86.02} {U} у C.01 и {N32.72} {U} у D.02.',
  'التراسات من {N62.47} إلى {N108.50} {U}. تُظهر القائمة حديقة لمنزلين فقط: {N86.02} {U} للمنزل C.01 و{N32.72} {U} للمنزل D.02.',
  'Terrassen van {N62.47} tot {N108.50} {U}. De lijst vermeldt slechts bij twee woningen een tuin: {N86.02} {U} bij C.01 en {N32.72} {U} bij D.02.',
  'Tarasy od {N62.47} do {N108.50} {U}. Lista podaje ogród tylko przy dwóch z nich: {N86.02} {U} przy C.01 i {N32.72} {U} przy D.02.',
  'Terrasser på {N62.47} til {N108.50} {U}. Listen viser hage for bare to av dem: {N86.02} {U} for C.01 og {N32.72} {U} for D.02.',
  'Terrasser på {N62.47} till {N108.50} {U}. Listan visar trädgård för bara två av dem: {N86.02} {U} för C.01 och {N32.72} {U} för D.02.')
a('Prices run from EUR 1,085,000 to EUR 1,275,000.',
  'Los precios van de {E1085000} a {E1275000}.', 'Les prix vont de {E1085000} à {E1275000}.', 'Die Preise reichen von {E1085000} bis {E1275000}.',
  'Цены — от {E1085000} до {E1275000}.', 'تتراوح الأسعار من {E1085000} إلى {E1275000}.', 'De prijzen lopen van {E1085000} tot {E1275000}.',
  'Ceny wahają się od {E1085000} do {E1275000}.', 'Prisene går fra {E1085000} til {E1275000}.', 'Priserna går från {E1085000} till {E1275000}.')
a('Homes E', 'Viviendas E', 'Maisons E', 'Häuser E', 'Дома E', 'المنازل E', 'Woningen E', 'Domy E', 'Bolig E', 'Bostäderna E')
a('4 homes listed, all with four bedrooms and three bathrooms, of 185.42 to 228.89 sqm built, on the same three levels.',
  '4 viviendas en lista, todas de cuatro dormitorios y tres baños, de {N185.42} a {N228.89} {U} construidos, en las mismas tres plantas.',
  '4 maisons listées, toutes de quatre chambres et trois salles de bains, de {N185.42} à {N228.89} {U} construits, sur les trois mêmes niveaux.',
  '4 gelistete Häuser, alle mit vier Schlafzimmern und drei Bädern, mit {N185.42} bis {N228.89} {U} bebauter Fläche, auf denselben drei Ebenen.',
  '4 дома в списке, все с четырьмя спальнями и тремя ванными, площадью застройки от {N185.42} до {N228.89} {U}, на тех же трёх уровнях.',
  '4 منازل مدرجة، جميعها بأربع غرف نوم وثلاثة حمامات، بمساحة مبنية من {N185.42} إلى {N228.89} {U}، على المستويات الثلاثة نفسها.',
  '4 vermelde woningen, allemaal met vier slaapkamers en drie badkamers, van {N185.42} tot {N228.89} {U} bebouwd, op dezelfde drie niveaus.',
  '4 domy na liście, wszystkie z czterema sypialniami i trzema łazienkami, o powierzchni zabudowy od {N185.42} do {N228.89} {U}, na tych samych trzech poziomach.',
  '4 oppførte boliger, alle med fire soverom og tre bad, på {N185.42} til {N228.89} {U} bygd areal, på de samme tre planene.',
  '4 listade bostäder, alla med fyra sovrum och tre badrum, på {N185.42} till {N228.89} {U} byggyta, på samma tre plan.')
a('Terraces of 110.65 to 120.10 sqm. The list shows a garden of 33.96 and 32.77 sqm for E.03 and E.04 only.',
  'Terrazas de {N110.65} a {N120.10} {U}. La lista muestra jardín solo en la E.03 y la E.04, de {N33.96} y {N32.77} {U}.',
  'Terrasses de {N110.65} à {N120.10} {U}. La liste n’indique un jardin que pour la E.03 et la E.04, de {N33.96} et {N32.77} {U}.',
  'Terrassen von {N110.65} bis {N120.10} {U}. Die Liste weist nur bei E.03 und E.04 einen Garten aus, mit {N33.96} und {N32.77} {U}.',
  'Террасы — от {N110.65} до {N120.10} {U}. Сад в списке указан только у E.03 и E.04: {N33.96} и {N32.77} {U}.',
  'التراسات من {N110.65} إلى {N120.10} {U}. تُظهر القائمة حديقة للمنزلين E.03 وE.04 فقط، بمساحة {N33.96} و{N32.77} {U}.',
  'Terrassen van {N110.65} tot {N120.10} {U}. De lijst vermeldt alleen bij E.03 en E.04 een tuin, van {N33.96} en {N32.77} {U}.',
  'Tarasy od {N110.65} do {N120.10} {U}. Lista podaje ogród tylko przy E.03 i E.04: {N33.96} i {N32.77} {U}.',
  'Terrasser på {N110.65} til {N120.10} {U}. Listen viser bare hage for E.03 og E.04, på {N33.96} og {N32.77} {U}.',
  'Terrasser på {N110.65} till {N120.10} {U}. Listan visar bara trädgård för E.03 och E.04, på {N33.96} och {N32.77} {U}.')
a('Prices run from EUR 1,226,000 to EUR 1,327,000.',
  'Los precios van de {E1226000} a {E1327000}.', 'Les prix vont de {E1226000} à {E1327000}.', 'Die Preise reichen von {E1226000} bis {E1327000}.',
  'Цены — от {E1226000} до {E1327000}.', 'تتراوح الأسعار من {E1226000} إلى {E1327000}.', 'De prijzen lopen van {E1226000} tot {E1327000}.',
  'Ceny wahają się od {E1226000} do {E1327000}.', 'Prisene går fra {E1226000} til {E1327000}.', 'Priserna går från {E1226000} till {E1327000}.')

# --- lifestyle
a('A private pool, <em>a gym</em> and the sea in view',
  'Piscina privada, <em>gimnasio</em> y el mar a la vista', 'Piscine privée, <em>salle de sport</em> et vue sur la mer', 'Privater Pool, <em>Fitnessraum</em> und Meerblick',
  'Частный бассейн, <em>тренажёрный зал</em> и море перед глазами', 'مسبح خاص، <em>وصالة رياضية</em> والبحر في الأفق', 'Privézwembad, <em>fitnessruimte</em> en zicht op zee',
  'Prywatny basen, <em>siłownia</em> i widok na morze', 'Privat basseng, <em>treningsrom</em> og havet i sikte', 'Privat pool, <em>gym</em> och havet i sikte')
a('Each home has its own pool and outdoor space, and residents share a gym, a pool and a work space.',
  'Cada vivienda tiene su propia piscina y espacio exterior, y los residentes comparten un gimnasio, una piscina y un espacio de trabajo.',
  'Chaque maison a sa propre piscine et son espace extérieur, et les résidents partagent une salle de sport, une piscine et un espace de travail.',
  'Jedes Haus hat seinen eigenen Pool und Außenbereich, und die Bewohner teilen sich einen Fitnessraum, einen Pool und einen Arbeitsraum.',
  'У каждого дома есть собственный бассейн и открытое пространство, а жители пользуются общим тренажёрным залом, бассейном и рабочим помещением.',
  'لكل منزل مسبحه الخاص ومساحته الخارجية، ويتشارك السكان صالة رياضية ومسبحًا وفضاءً للعمل.',
  'Elke woning heeft een eigen zwembad en buitenruimte, en de bewoners delen een fitnessruimte, een zwembad en een werkruimte.',
  'Każdy dom ma własny basen i przestrzeń zewnętrzną, a mieszkańcy korzystają ze wspólnej siłowni, basenu i przestrzeni do pracy.',
  'Hver bolig har eget basseng og egen utendørs plass, og beboerne deler et treningsrom, et basseng og et arbeidsrom.',
  'Varje bostad har egen pool och egen utomhusyta, och de boende delar ett gym, en pool och ett arbetsrum.')
a('Your own pool', 'Su propia piscina', 'Votre propre piscine', 'Ihr eigener Pool', 'Ваш собственный бассейн', 'مسبحكم الخاص', 'Uw eigen zwembad', 'Własny basen', 'Ditt eget basseng', 'Er egen pool')
a('Each home has a private swimming pool, built with high-end materials and fitted with a filtration system, and its own outdoor space.',
  'Cada vivienda tiene una piscina privada, ejecutada con materiales de alta gama y equipada con un sistema de depuración, y su propio espacio exterior.',
  'Chaque maison a une piscine privée, réalisée avec des matériaux haut de gamme et équipée d’un système de filtration, ainsi que son propre espace extérieur.',
  'Jedes Haus hat einen privaten Swimmingpool aus hochwertigen Materialien mit Filteranlage sowie einen eigenen Außenbereich.',
  'У каждого дома есть частный бассейн из материалов высокого класса с системой фильтрации и собственное открытое пространство.',
  'لكل منزل مسبح خاص منفذ بمواد عالية الجودة ومجهز بنظام ترشيح، ومساحة خارجية خاصة به.',
  'Elke woning heeft een privézwembad, gebouwd met hoogwaardige materialen en voorzien van een filtersysteem, en een eigen buitenruimte.',
  'Każdy dom ma prywatny basen z wysokiej klasy materiałów, wyposażony w system filtracji, oraz własną przestrzeń zewnętrzną.',
  'Hver bolig har et privat svømmebasseng, bygget med høyverdige materialer og utstyrt med filtreringsanlegg, og egen utendørs plass.',
  'Varje bostad har en privat pool, byggd med högklassiga material och utrustad med ett filtreringssystem, och egen utomhusyta.')
a('Pool and solarium', 'Piscina y solárium', 'Piscine et solarium', 'Pool und Liegefläche', 'Бассейн и солярий', 'المسبح ومنطقة التشمس', 'Zwembad en zonneterras', 'Basen i solarium', 'Basseng og solplass', 'Pool och solplats')
a('A shared outdoor pool with salt chlorination and a sunbathing area.',
  'Una piscina exterior compartida con cloración salina y zona de solárium.', 'Une piscine extérieure commune au sel avec un espace solarium.',
  'Ein gemeinsamer Außenpool mit Salzchlorierung und Liegefläche.', 'Общий открытый бассейн с солевым хлорированием и зоной для загара.',
  'مسبح خارجي مشترك بتعقيم بالملح ومنطقة للتشمس.', 'Een gedeeld buitenzwembad met zoutchlorering en een zonneterras.',
  'Wspólny basen zewnętrzny z elektrolizą soli i strefą do opalania.', 'Et felles utendørsbasseng med saltklorering og solplass.', 'En gemensam utomhuspool med saltklorering och solplats.')
a('Work and study', 'Trabajo y estudio', 'Travail et études', 'Arbeiten und Lernen', 'Работа и учёба', 'العمل والدراسة', 'Werken en studeren', 'Praca i nauka', 'Arbeid og studier', 'Arbete och studier')
a('A multi-purpose space for working, studying or meeting, which the brochure calls coworking.',
  'Un espacio polivalente para trabajar, estudiar o reunirse, que el folleto llama coworking.', 'Un espace polyvalent pour travailler, étudier ou se réunir, que la brochure appelle coworking.',
  'Ein Mehrzweckraum zum Arbeiten, Lernen oder für Treffen, den die Broschüre Coworking nennt.', 'Многофункциональное помещение для работы, учёбы или встреч; в брошюре оно названо коворкингом.',
  'قاعة متعددة الاستخدامات للعمل أو الدراسة أو الاجتماعات، تسميها النشرة مساحة عمل مشتركة (كوورکينغ).',
  'Een multifunctionele ruimte om te werken, te studeren of af te spreken, die de brochure coworking noemt.',
  'Sala wielofunkcyjna do pracy, nauki lub spotkań, którą broszura nazywa coworkingiem.', 'Et flerbruksrom for arbeid, studier eller møter, som brosjyren kaller coworking.',
  'Ett flexibelt rum för arbete, studier eller möten, som broschyren kallar coworking.')

# --- location, investment, trust
a('El Higuerón is in Fuengirola, on the Costa del Sol. The developer’s brochure says it combines elevation, open views of the Mediterranean and a direct connection to everything that matters. Its map marks the A-7 and AP-7 roads, the beaches of Carvajal, Torreblanca, Fuengirola and Torremuelle and the golf courses of Chaparral, Mijas, Alhaurín, La Noria and Calanova. It gives no distances; the ones shown here are measured by road from the site.',
  'El Higuerón está en Fuengirola, en la Costa del Sol. El folleto del promotor dice que combina altura, vistas abiertas al Mediterráneo y una conexión directa con todo lo que importa. Su mapa marca las carreteras A-7 y AP-7, las playas de Carvajal, Torreblanca, Fuengirola y Torremuelle y los campos de golf de Chaparral, Mijas, Alhaurín, La Noria y Calanova. No da distancias; las que se muestran aquí se miden por carretera desde la parcela.',
  'El Higuerón se trouve à Fuengirola, sur la Costa del Sol. La brochure du promoteur dit qu’il allie hauteur, vues dégagées sur la Méditerranée et liaison directe avec tout ce qui compte. Sa carte indique les routes A-7 et AP-7, les plages de Carvajal, Torreblanca, Fuengirola et Torremuelle et les golfs de Chaparral, Mijas, Alhaurín, La Noria et Calanova. Elle ne donne aucune distance ; celles présentées ici sont mesurées par la route depuis la parcelle.',
  'El Higuerón liegt in Fuengirola an der Costa del Sol. Laut Broschüre des Bauträgers verbindet es erhöhte Lage, offenen Blick auf das Mittelmeer und eine direkte Anbindung an alles Wichtige. Die Karte zeigt die Straßen A-7 und AP-7, die Strände von Carvajal, Torreblanca, Fuengirola und Torremuelle sowie die Golfplätze Chaparral, Mijas, Alhaurín, La Noria und Calanova. Entfernungen nennt sie nicht; die hier gezeigten sind ab dem Grundstück auf der Straße gemessen.',
  'Эль-Игерон находится в Фуэнхироле на Коста-дель-Соль. В брошюре застройщика сказано, что здесь сочетаются возвышенное положение, открытый вид на Средиземное море и прямая связь со всем необходимым. На её карте отмечены дороги A-7 и AP-7, пляжи Карвахаль, Торреблянка, Фуэнхирола и Торремуэлье и поля для гольфа Чапарраль, Михас, Алаурин, Ла-Нория и Каланова. Расстояния она не указывает; приведённые здесь измерены по дороге от участка.',
  'يقع إل إيغيرون في فوينخيرولا على كوستا ديل سول. تقول نشرة المطوّر إنه يجمع بين الارتفاع وإطلالات مفتوحة على البحر المتوسط واتصال مباشر بكل ما يهم. وتُظهر خريطتها طريقي A-7 وAP-7 وشواطئ كارفاخال وتوريبلانكا وفوينخيرولا وتوريمويِّه وملاعب الغولف شابارال وميخاس وألاورين ولا نوريا وكالانوفا. ولا تذكر مسافات؛ والمسافات المعروضة هنا مقيسة بالطريق من موقع المشروع.',
  'El Higuerón ligt in Fuengirola, aan de Costa del Sol. Volgens de brochure van de ontwikkelaar combineert het hoogte, open uitzicht op de Middellandse Zee en een directe verbinding met alles wat telt. De kaart toont de wegen A-7 en AP-7, de stranden van Carvajal, Torreblanca, Fuengirola en Torremuelle en de golfbanen van Chaparral, Mijas, Alhaurín, La Noria en Calanova. Afstanden geeft ze niet; de hier getoonde zijn over de weg vanaf het perceel gemeten.',
  'El Higuerón leży w Fuengiroli, na Costa del Sol. Według broszury dewelopera łączy wysokie położenie, otwarty widok na Morze Śródziemne i bezpośrednie połączenie ze wszystkim, co ważne. Jej mapa wskazuje drogi A-7 i AP-7, plaże Carvajal, Torreblanca, Fuengirola i Torremuelle oraz pola golfowe Chaparral, Mijas, Alhaurín, La Noria i Calanova. Nie podaje odległości; te pokazane tutaj zmierzono drogą od działki.',
  'El Higuerón ligger i Fuengirola på Costa del Sol. Utbyggerens brosjyre sier at stedet kombinerer høyde, åpen utsikt mot Middelhavet og direkte forbindelse til alt som betyr noe. Kartet viser veiene A-7 og AP-7, strendene Carvajal, Torreblanca, Fuengirola og Torremuelle og golfbanene Chaparral, Mijas, Alhaurín, La Noria og Calanova. Det oppgir ingen avstander; de som vises her er målt langs vei fra tomten.',
  'El Higuerón ligger i Fuengirola på Costa del Sol. Exploatörens broschyr säger att platsen förenar höjd, öppen utsikt över Medelhavet och direkt förbindelse med allt som är viktigt. Kartan visar vägarna A-7 och AP-7, stränderna Carvajal, Torreblanca, Fuengirola och Torremuelle och golfbanorna Chaparral, Mijas, Alhaurín, La Noria och Calanova. Den anger inga avstånd; de som visas här är uppmätta längs väg från tomten.')
a('The developer’s documents give no payment terms. We confirm the current amounts and dates in writing before you reserve.',
  'Los documentos del promotor no indican condiciones de pago. Confirmamos por escrito los importes y las fechas vigentes antes de que usted reserve.',
  'Les documents du promoteur ne donnent aucune condition de paiement. Nous confirmons par écrit les montants et les dates en vigueur avant que vous ne réserviez.',
  'Die Unterlagen des Bauträgers nennen keine Zahlungsbedingungen. Wir bestätigen die aktuellen Beträge und Termine schriftlich, bevor Sie reservieren.',
  'В документах застройщика нет условий оплаты. Мы письменно подтверждаем актуальные суммы и сроки до того, как вы забронируете.',
  'لا تذكر وثائق المطوّر شروط الدفع. نؤكد كتابةً المبالغ والمواعيد الحالية قبل أن تحجزوا.',
  'De documenten van de ontwikkelaar noemen geen betalingsvoorwaarden. We bevestigen de actuele bedragen en data schriftelijk voordat u reserveert.',
  'Dokumenty dewelopera nie podają warunków płatności. Aktualne kwoty i terminy potwierdzamy na piśmie, zanim Państwo dokonają rezerwacji.',
  'Utbyggerens dokumenter oppgir ingen betalingsvilkår. Vi bekrefter gjeldende beløp og datoer skriftlig før De reserverer.',
  'Exploatörens dokument anger inga betalningsvillkor. Vi bekräftar aktuella belopp och datum skriftligen innan ni bokar.')
a('None of the documents gives a reservation amount, so we ask for it and for how it is deducted from the price.',
  'Ninguno de los documentos indica el importe de la reserva, por lo que lo pedimos, junto con la forma en que se descuenta del precio.',
  'Aucun document ne donne le montant de la réservation ; nous le demandons, ainsi que la manière dont il est déduit du prix.',
  'Kein Dokument nennt einen Reservierungsbetrag, daher fragen wir ihn an, ebenso wie die Art, in der er auf den Preis angerechnet wird.',
  'Ни в одном документе нет суммы бронирования, поэтому мы запрашиваем её и порядок зачёта в стоимость.',
  'لا تذكر أي وثيقة مبلغ الحجز، لذلك نطلبه ونطلب طريقة خصمه من السعر.',
  'Geen enkel document noemt een reserveringsbedrag, dus we vragen ernaar en naar de manier waarop het op de prijs in mindering wordt gebracht.',
  'Żaden dokument nie podaje kwoty rezerwacji, dlatego prosimy o nią oraz o sposób jej odliczenia od ceny.',
  'Ingen av dokumentene oppgir et reservasjonsbeløp, så vi ber om det og om hvordan det trekkes fra prisen.',
  'Inget dokument anger något bokningsbelopp, så vi ber om det och om hur det dras av från priset.')
a('No payment schedule is given. We ask for the instalments and their dates before you reserve.',
  'No se indica un calendario de pagos. Pedimos los plazos y sus fechas antes de que usted reserve.',
  'Aucun échéancier de paiement n’est donné. Nous demandons les échéances et leurs dates avant que vous ne réserviez.',
  'Ein Zahlungsplan wird nicht genannt. Wir fragen die Raten und ihre Termine an, bevor Sie reservieren.',
  'График платежей не приведён. Мы запрашиваем платежи и их сроки до того, как вы забронируете.',
  'لا يُذكر جدول للدفعات. نطلب الدفعات ومواعيدها قبل أن تحجزوا.',
  'Er wordt geen betalingsschema genoemd. We vragen de termijnen en hun data op voordat u reserveert.',
  'Nie podano harmonogramu płatności. Prosimy o raty i ich terminy, zanim Państwo dokonają rezerwacji.',
  'Ingen betalingsplan er oppgitt. Vi ber om delbetalingene og datoene før De reserverer.',
  'Ingen betalningsplan anges. Vi ber om delbetalningarna och deras datum innan ni bokar.')
a('The price list does not say whether prices include VAT. Nueva Living confirms the taxes and purchase costs in writing.',
  'La lista de precios no indica si los precios incluyen el IVA. Nueva Living confirma por escrito los impuestos y los gastos de compra.',
  'La liste de prix n’indique pas si les prix incluent la TVA. Nueva Living confirme par écrit les taxes et les frais d’achat.',
  'Die Preisliste sagt nicht, ob die Preise die MwSt. enthalten. Nueva Living bestätigt Steuern und Kaufnebenkosten schriftlich.',
  'В прайс-листе не сказано, включён ли НДС в цены. Nueva Living письменно подтверждает налоги и расходы на покупку.',
  'لا توضح قائمة الأسعار ما إذا كانت الأسعار تشمل ضريبة القيمة المضافة. وتؤكد Nueva Living الضرائب ومصاريف الشراء كتابةً.',
  'De prijslijst vermeldt niet of de prijzen inclusief btw zijn. Nueva Living bevestigt de belastingen en aankoopkosten schriftelijk.',
  'Cennik nie wskazuje, czy ceny zawierają VAT. Nueva Living potwierdza na piśmie podatki i koszty zakupu.',
  'Prislisten oppgir ikke om prisene inkluderer mva. Nueva Living bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan anger inte om priserna inkluderar moms. Nueva Living bekräftar skatter och köpkostnader skriftligen.')
a('The specification says a ten-year building warranty insurance will be in place. It does not describe a guarantee on sums paid in advance, so we ask for the policy before any payment.',
  'La memoria de calidades indica que habrá un seguro decenal de la edificación. No describe ninguna garantía sobre las cantidades entregadas a cuenta, por lo que pedimos la póliza antes de cualquier pago.',
  'Le descriptif indique qu’une assurance décennale de la construction sera en place. Il ne décrit aucune garantie sur les sommes versées à l’avance ; nous demandons donc la police avant tout paiement.',
  'Die Baubeschreibung sagt, dass eine zehnjährige Bauwerksversicherung bestehen wird. Eine Absicherung für im Voraus gezahlte Beträge beschreibt sie nicht, daher fragen wir die Police vor jeder Zahlung an.',
  'В спецификации сказано, что будет действовать десятилетняя страховка на строительство. Гарантии на суммы, уплаченные заранее, она не описывает, поэтому мы запрашиваем полис до любого платежа.',
  'تذكر المواصفات أنه سيكون هناك تأمين ضمان للبناء لعشر سنوات. ولا تصف ضمانًا للمبالغ المدفوعة مقدمًا، لذلك نطلب البوليصة قبل أي دفعة.',
  'Het lastenboek zegt dat er een tienjarige bouwgarantieverzekering zal zijn. Een waarborg voor vooruitbetaalde bedragen beschrijft het niet, dus we vragen de polis op vóór elke betaling.',
  'Specyfikacja stwierdza, że będzie obowiązywać dziesięcioletnie ubezpieczenie gwarancyjne budynku. Nie opisuje gwarancji dla kwot wpłacanych z góry, dlatego przed jakąkolwiek płatnością prosimy o polisę.',
  'Spesifikasjonen sier at det vil være en tiårig byggeforsikring. Den beskriver ingen garanti for beløp betalt på forhånd, så vi ber om polisen før noen betaling.',
  'Specifikationen anger att en tioårig byggförsäkring kommer att finnas. Den beskriver ingen garanti för belopp som betalas i förskott, så vi ber om försäkringsbrevet före varje betalning.')
a('The documents do not say whether the building licence has been granted or whether the works have started. We ask for the licence, its status and the start date of the works.',
  'Los documentos no indican si la licencia de obras se ha concedido ni si las obras han comenzado. Pedimos la licencia, su estado y la fecha de inicio de las obras.',
  'Les documents n’indiquent pas si le permis de construire a été accordé ni si les travaux ont commencé. Nous demandons le permis, son état et la date de début des travaux.',
  'Die Unterlagen sagen nicht, ob die Baugenehmigung erteilt wurde oder ob die Arbeiten begonnen haben. Wir fragen die Genehmigung, ihren Stand und den Baubeginn an.',
  'В документах не сказано, получено ли разрешение на строительство и начались ли работы. Мы запрашиваем разрешение, его статус и дату начала работ.',
  'لا توضح الوثائق ما إذا كانت رخصة البناء قد مُنحت أو ما إذا كانت الأعمال قد بدأت. نطلب الرخصة وحالتها وتاريخ بدء الأعمال.',
  'De documenten vermelden niet of de bouwvergunning is verleend of dat de werken zijn begonnen. We vragen de vergunning, de status ervan en de startdatum van de werken op.',
  'Dokumenty nie wskazują, czy pozwolenie na budowę zostało wydane ani czy prace się rozpoczęły. Prosimy o pozwolenie, jego status i datę rozpoczęcia prac.',
  'Dokumentene oppgir ikke om byggetillatelsen er gitt eller om arbeidene har startet. Vi ber om tillatelsen, statusen og startdatoen for arbeidene.',
  'Dokumenten anger inte om bygglovet har beviljats eller om arbetena har påbörjats. Vi ber om bygglovet, dess status och startdatum för arbetena.')
a('The documents give no completion date, so we ask for the contractual date in writing.',
  'Los documentos no indican fecha de entrega, por lo que pedimos la fecha contractual por escrito.',
  'Les documents ne donnent aucune date de livraison ; nous demandons donc la date contractuelle par écrit.',
  'Die Unterlagen nennen keinen Fertigstellungstermin, daher fragen wir das vertragliche Datum schriftlich an.',
  'В документах нет срока завершения, поэтому мы письменно запрашиваем договорную дату.',
  'لا تذكر الوثائق موعد الإنجاز، لذلك نطلب التاريخ التعاقدي كتابةً.',
  'De documenten noemen geen opleveringsdatum, dus we vragen de contractuele datum schriftelijk op.',
  'Dokumenty nie podają terminu ukończenia, dlatego prosimy na piśmie o termin wskazany w umowie.',
  'Dokumentene oppgir ingen ferdigstillelsesdato, så vi ber skriftlig om den kontraktsfestede datoen.',
  'Dokumenten anger inget färdigställandedatum, så vi ber skriftligen om det avtalade datumet.')
a('The price list gives one built area, while the plan sheets give an interior area and an area that includes a share of the communal zones. They do not always agree, so we confirm which figure the contract uses.',
  'La lista de precios da una única superficie construida, mientras que los planos dan una superficie interior y otra que incluye la parte proporcional de las zonas comunes. No siempre coinciden, por lo que confirmamos qué cifra utiliza el contrato.',
  'La liste de prix donne une seule surface construite, tandis que les plans donnent une surface intérieure et une surface incluant une quote-part des parties communes. Elles ne concordent pas toujours ; nous confirmons donc quel chiffre retient le contrat.',
  'Die Preisliste nennt eine bebaute Fläche, während die Pläne eine Innenfläche und eine Fläche samt Anteil an den Gemeinschaftsbereichen angeben. Sie stimmen nicht immer überein, daher bestätigen wir, welche Zahl der Vertrag verwendet.',
  'В прайс-листе указана одна площадь застройки, а на планах — внутренняя площадь и площадь с долей общих зон. Они не всегда совпадают, поэтому мы уточняем, какая цифра используется в договоре.',
  'تذكر قائمة الأسعار مساحة مبنية واحدة، بينما تذكر المخططات مساحة داخلية ومساحة تشمل حصة من المناطق المشتركة. وهما لا تتطابقان دائمًا، لذلك نؤكد أي رقم يعتمده العقد.',
  'De prijslijst geeft één bebouwde oppervlakte, terwijl de plattegronden een binnenoppervlakte geven en een oppervlakte inclusief een aandeel in de gemeenschappelijke ruimten. Ze komen niet altijd overeen, dus we bevestigen welk cijfer het contract hanteert.',
  'Cennik podaje jedną powierzchnię zabudowy, a rzuty podają powierzchnię wewnętrzną oraz powierzchnię z udziałem w częściach wspólnych. Nie zawsze są one zgodne, dlatego potwierdzamy, której wartości używa umowa.',
  'Prislisten oppgir ett bygd areal, mens tegningene oppgir et innvendig areal og et areal som inkluderer en andel av fellesområdene. De stemmer ikke alltid overens, så vi bekrefter hvilket tall kontrakten bruker.',
  'Prislistan anger en byggyta, medan ritningarna anger en inomhusyta och en yta som inkluderar en andel av de gemensamma ytorna. De stämmer inte alltid överens, så vi bekräftar vilken siffra avtalet använder.')
a('The other seven homes', 'Las otras siete viviendas', 'Les sept autres maisons', 'Die übrigen sieben Häuser', 'Остальные семь домов', 'المنازل السبعة الأخرى',
  'De andere zeven woningen', 'Pozostałe siedem domów', 'De sju andre boligene', 'De övriga sju bostäderna')
a('The developer’s list shows 18 of the 25 homes. We ask for the status and prices of the other seven.',
  'La lista del promotor muestra 18 de las 25 viviendas. Pedimos el estado y los precios de las otras siete.',
  'La liste du promoteur présente 18 des 25 maisons. Nous demandons le statut et les prix des sept autres.',
  'Die Liste des Bauträgers zeigt 18 der 25 Häuser. Wir fragen Stand und Preise der übrigen sieben an.',
  'В списке застройщика указаны 18 из 25 домов. Мы запрашиваем статус и цены остальных семи.',
  'تعرض قائمة المطوّر 18 منزلًا من أصل 25. نطلب حالة المنازل السبعة الأخرى وأسعارها.',
  'De lijst van de ontwikkelaar toont 18 van de 25 woningen. We vragen de status en prijzen van de andere zeven op.',
  'Lista dewelopera zawiera 18 z 25 domów. Prosimy o status i ceny pozostałych siedmiu.',
  'Utbyggerens liste viser 18 av de 25 boligene. Vi ber om status og priser for de sju andre.',
  'Exploatörens lista visar 18 av de 25 bostäderna. Vi ber om status och priser för de övriga sju.')

# --- availability
a('18 of 25 homes <em>listed with a price</em>',
  '18 de 25 viviendas <em>en lista con precio</em>', '18 maisons sur 25 <em>listées avec un prix</em>', '18 von 25 Häusern <em>mit Preis gelistet</em>',
  '18 из 25 домов <em>в списке с ценой</em>', '18 من أصل 25 منزلًا <em>مدرجة بسعر</em>', '18 van de 25 woningen <em>met prijs vermeld</em>',
  '18 z 25 domów <em>na liście z ceną</em>', '18 av 25 boliger <em>oppført med pris</em>', '18 av 25 bostäder <em>listade med pris</em>')
a('Prices are those of the developer’s price list as of October 2026 and are confirmed before any reservation. The 18 homes are townhouses with three or four bedrooms and three bathrooms.',
  'Los precios son los de la lista de precios del promotor a octubre de 2026 y se confirman antes de cualquier reserva. Las 18 viviendas son adosados de tres o cuatro dormitorios y tres baños.',
  'Les prix sont ceux de la liste de prix du promoteur à octobre 2026 et sont confirmés avant toute réservation. Les 18 maisons sont des maisons mitoyennes de trois ou quatre chambres et trois salles de bains.',
  'Die Preise stammen aus der Preisliste des Bauträgers, Stand Oktober 2026, und werden vor jeder Reservierung bestätigt. Die 18 Häuser sind Reihenhäuser mit drei oder vier Schlafzimmern und drei Bädern.',
  'Цены взяты из прайс-листа застройщика по состоянию на октябрь 2026 года и подтверждаются перед любым бронированием. 18 домов — таунхаусы с тремя или четырьмя спальнями и тремя ванными.',
  'الأسعار هي أسعار قائمة المطوّر في أكتوبر 2026 وتُؤكَّد قبل أي حجز. والمنازل الثمانية عشر منازل متلاصقة بثلاث أو أربع غرف نوم وثلاثة حمامات.',
  'De prijzen zijn die van de prijslijst van de ontwikkelaar per oktober 2026 en worden vóór elke reservering bevestigd. De 18 woningen zijn rijwoningen met drie of vier slaapkamers en drie badkamers.',
  'Ceny pochodzą z cennika dewelopera według stanu na październik 2026 r. i są potwierdzane przed każdą rezerwacją. 18 domów to domy szeregowe z trzema lub czterema sypialniami i trzema łazienkami.',
  'Prisene er de i utbyggerens prisliste per oktober 2026 og bekreftes før enhver reservasjon. De 18 boligene er rekkehus med tre eller fire soverom og tre bad.',
  'Priserna är de i exploatörens prislista per oktober 2026 och bekräftas före varje bokning. De 18 bostäderna är radhus med tre eller fyra sovrum och tre badrum.')
a('Prices and areas are transcribed from the developer’s online price list, copied on 12 October 2026, which lists 18 of the 25 homes, all marked available. The list does not say whether prices include VAT. The built area, terrace and garden columns are shown as printed, and a dash means that no garden is listed. They do not always agree with the plan sheets. For C.01 to C.05, D.01, D.03, D.04, E.01 and E.02 the listed built area is the plan sheet’s interior built area, while for D.02, E.03 and E.04 it is the sheet’s figure including a share of the communal zones, which is why those three look larger. For A.02, A.05, B.02 and B.03 it is within 2.5 sqm of that figure, and A.04 is listed at 140.00 sqm against 142.60 sqm interior on its sheet. The listed terrace is lower than the terraces plus solarium on the sheets (C.02: 84.82 sqm against 97.40 sqm), and C.02 has no listed garden although its living-level sheet gives 30.52 sqm. For A.02 the listed terrace and garden, 40.73 and 37.37 sqm, are those on the sheet for A1, while the sheet for A2 gives 37.60 and 40.23 sqm. We confirm which figures the contract uses.',
  'Los precios y las superficies están transcritos de la lista de precios en línea del promotor, copiada el 12 de octubre de 2026, que recoge 18 de las 25 viviendas, todas marcadas como disponibles. La lista no indica si los precios incluyen IVA. Las columnas de superficie construida, terraza y jardín se muestran tal como figuran, y un guion significa que no se indica jardín. No siempre coinciden con los planos. En C.01 a C.05, D.01, D.03, D.04, E.01 y E.02 la superficie construida de la lista es la superficie construida interior del plano, mientras que en D.02, E.03 y E.04 es la cifra del plano que incluye la parte proporcional de las zonas comunes, por lo que esas tres parecen mayores. En A.02, A.05, B.02 y B.03 está a menos de {N2.5} {U} de esa cifra, y la A.04 figura con {N140.00} {U} frente a {N142.60} {U} interiores en su plano. La terraza de la lista es menor que las terrazas más el solárium de los planos (C.02: {N84.82} {U} frente a {N97.40} {U}), y la C.02 no tiene jardín en la lista aunque su plano de la planta de salón indica {N30.52} {U}. En la A.02, la terraza y el jardín de la lista, {N40.73} y {N37.37} {U}, son los del plano de la A1, mientras que el plano de la A2 indica {N37.60} y {N40.23} {U}. Confirmamos qué cifras utiliza el contrato.',
  'Les prix et les surfaces sont repris de la liste de prix en ligne du promoteur, copiée le 12 octobre 2026, qui présente 18 des 25 maisons, toutes indiquées comme disponibles. La liste n’indique pas si les prix incluent la TVA. Les colonnes surface construite, terrasse et jardin sont reproduites telles quelles, et un tiret signifie qu’aucun jardin n’est indiqué. Elles ne concordent pas toujours avec les plans. Pour C.01 à C.05, D.01, D.03, D.04, E.01 et E.02, la surface construite de la liste est la surface construite intérieure du plan, tandis que pour D.02, E.03 et E.04 c’est le chiffre du plan incluant une quote-part des parties communes, ce qui explique que ces trois maisons paraissent plus grandes. Pour A.02, A.05, B.02 et B.03, l’écart avec ce chiffre est inférieur à {N2.5} {U}, et la A.04 est indiquée à {N140.00} {U} contre {N142.60} {U} intérieurs sur son plan. La terrasse de la liste est inférieure aux terrasses plus le solarium des plans (C.02 : {N84.82} {U} contre {N97.40} {U}), et la C.02 n’a pas de jardin dans la liste alors que son plan du niveau séjour indique {N30.52} {U}. Pour la A.02, la terrasse et le jardin de la liste, {N40.73} et {N37.37} {U}, sont ceux du plan de la A1, alors que le plan de la A2 indique {N37.60} et {N40.23} {U}. Nous confirmons quels chiffres retient le contrat.',
  'Preise und Flächen sind der Online-Preisliste des Bauträgers entnommen, kopiert am 12. Oktober 2026, die 18 der 25 Häuser auflistet, alle als verfügbar gekennzeichnet. Die Liste sagt nicht, ob die Preise die MwSt. enthalten. Die Spalten für bebaute Fläche, Terrasse und Garten sind wie gedruckt wiedergegeben, ein Strich bedeutet, dass kein Garten aufgeführt ist. Sie stimmen nicht immer mit den Plänen überein. Bei C.01 bis C.05, D.01, D.03, D.04, E.01 und E.02 ist die gelistete bebaute Fläche die bebaute Innenfläche laut Plan, bei D.02, E.03 und E.04 dagegen der Planwert samt Anteil an den Gemeinschaftsbereichen, weshalb diese drei größer wirken. Bei A.02, A.05, B.02 und B.03 liegt sie höchstens {N2.5} {U} von diesem Wert entfernt, und A.04 ist mit {N140.00} {U} gelistet gegenüber {N142.60} {U} Innenfläche auf ihrem Plan. Die gelistete Terrasse ist kleiner als Terrassen plus Solarium auf den Plänen (C.02: {N84.82} {U} gegenüber {N97.40} {U}), und für C.02 ist kein Garten gelistet, obwohl der Plan der Wohnebene {N30.52} {U} nennt. Bei A.02 stammen die gelistete Terrasse und der Garten, {N40.73} und {N37.37} {U}, aus dem Plan von A1, während der Plan von A2 {N37.60} und {N40.23} {U} nennt. Wir bestätigen, welche Werte der Vertrag verwendet.',
  'Цены и площади перенесены из онлайн-прайс-листа застройщика, скопированного 12 октября 2026 года; в нём указаны 18 из 25 домов, все отмечены как доступные. В прайс-листе не сказано, включён ли НДС. Столбцы площади застройки, террасы и сада приведены как напечатано, прочерк означает, что сад не указан. Они не всегда совпадают с планами. У C.01–C.05, D.01, D.03, D.04, E.01 и E.02 указанная площадь застройки равна внутренней площади застройки по плану, а у D.02, E.03 и E.04 это цифра по плану с долей общих зон, поэтому эти три дома выглядят больше. У A.02, A.05, B.02 и B.03 расхождение с этой цифрой не более {N2.5} {U}, а A.04 указан как {N140.00} {U} против {N142.60} {U} внутренней площади на плане. Указанная терраса меньше террас плюс солярий на планах (C.02: {N84.82} {U} против {N97.40} {U}), а у C.02 сад не указан, хотя план жилого уровня даёт {N30.52} {U}. У A.02 указанные терраса и сад, {N40.73} и {N37.37} {U}, взяты с плана A1, тогда как план A2 даёт {N37.60} и {N40.23} {U}. Мы уточняем, какие цифры использует договор.',
  'الأسعار والمساحات منقولة من قائمة أسعار المطوّر على الإنترنت، المنسوخة في 12 أكتوبر 2026، وتضم 18 منزلًا من أصل 25 جميعها معلّمة بأنها متاحة. ولا توضح القائمة ما إذا كانت الأسعار تشمل ضريبة القيمة المضافة. أعمدة المساحة المبنية والتراس والحديقة معروضة كما وردت، وتعني الشرطة أنه لا توجد حديقة مدرجة. وهي لا تتفق دائمًا مع المخططات. ففي C.01 إلى C.05 وD.01 وD.03 وD.04 وE.01 وE.02 تساوي المساحة المبنية المدرجة المساحة المبنية الداخلية في المخطط، أما في D.02 وE.03 وE.04 فهي رقم المخطط شاملًا حصة من المناطق المشتركة، ولذلك تبدو هذه الثلاثة أكبر. وفي A.02 وA.05 وB.02 وB.03 تقع ضمن {N2.5} {U} من ذلك الرقم، والمنزل A.04 مدرج بمساحة {N140.00} {U} مقابل {N142.60} {U} داخلية في مخططه. والتراس المدرج أصغر من التراسات مع السولاريوم في المخططات (C.02: {N84.82} {U} مقابل {N97.40} {U})، ولا توجد حديقة مدرجة للمنزل C.02 مع أن مخطط مستوى المعيشة يذكر {N30.52} {U}. وفي A.02 التراس والحديقة المدرجان، {N40.73} و{N37.37} {U}، هما رقما مخطط A1، بينما يذكر مخطط A2 الرقمين {N37.60} و{N40.23} {U}. نؤكد الأرقام التي يعتمدها العقد.',
  'Prijzen en oppervlakten zijn overgenomen uit de online prijslijst van de ontwikkelaar, gekopieerd op 12 oktober 2026, waarin 18 van de 25 woningen staan, allemaal als beschikbaar aangeduid. De lijst vermeldt niet of de prijzen inclusief btw zijn. De kolommen bebouwde oppervlakte, terras en tuin zijn weergegeven zoals gedrukt, en een streepje betekent dat er geen tuin is vermeld. Ze komen niet altijd overeen met de plattegronden. Bij C.01 tot en met C.05, D.01, D.03, D.04, E.01 en E.02 is de vermelde bebouwde oppervlakte de bebouwde binnenoppervlakte op de plattegrond, terwijl het bij D.02, E.03 en E.04 het cijfer op de plattegrond is inclusief een aandeel in de gemeenschappelijke ruimten, waardoor die drie groter lijken. Bij A.02, A.05, B.02 en B.03 ligt ze binnen {N2.5} {U} van dat cijfer, en A.04 staat vermeld met {N140.00} {U} tegenover {N142.60} {U} binnen op de plattegrond. Het vermelde terras is kleiner dan de terrassen plus solarium op de plattegronden (C.02: {N84.82} {U} tegenover {N97.40} {U}), en voor C.02 is geen tuin vermeld, terwijl de plattegrond van het woonniveau {N30.52} {U} geeft. Bij A.02 zijn het vermelde terras en de tuin, {N40.73} en {N37.37} {U}, die van de plattegrond van A1, terwijl de plattegrond van A2 {N37.60} en {N40.23} {U} geeft. We bevestigen welke cijfers het contract hanteert.',
  'Ceny i powierzchnie przepisano z internetowego cennika dewelopera, skopiowanego 12 października 2026 r., który obejmuje 18 z 25 domów, wszystkie oznaczone jako dostępne. Cennik nie wskazuje, czy ceny zawierają VAT. Kolumny powierzchni zabudowy, tarasu i ogrodu pokazano tak, jak je wydrukowano, a kreska oznacza, że nie podano ogrodu. Nie zawsze są zgodne z rzutami. W C.01–C.05, D.01, D.03, D.04, E.01 i E.02 podana powierzchnia zabudowy to powierzchnia zabudowy wewnętrznej z rzutu, a w D.02, E.03 i E.04 to wartość z rzutu wraz z udziałem w częściach wspólnych, dlatego te trzy domy wyglądają na większe. W A.02, A.05, B.02 i B.03 różni się ona od tej wartości o mniej niż {N2.5} {U}, a A.04 jest podany jako {N140.00} {U} wobec {N142.60} {U} wewnętrznych na jego rzucie. Podany taras jest mniejszy niż tarasy plus solarium na rzutach (C.02: {N84.82} {U} wobec {N97.40} {U}), a dla C.02 nie podano ogrodu, choć rzut poziomu dziennego wskazuje {N30.52} {U}. W A.02 podany taras i ogród, {N40.73} i {N37.37} {U}, pochodzą z rzutu A1, a rzut A2 podaje {N37.60} i {N40.23} {U}. Potwierdzamy, jakich wartości używa umowa.',
  'Priser og arealer er hentet fra utbyggerens nettbaserte prisliste, kopiert 12. oktober 2026, som viser 18 av de 25 boligene, alle merket som tilgjengelige. Listen oppgir ikke om prisene inkluderer mva. Kolonnene for bygd areal, terrasse og hage er gjengitt slik de er trykt, og en strek betyr at ingen hage er oppført. De stemmer ikke alltid med tegningene. For C.01 til C.05, D.01, D.03, D.04, E.01 og E.02 er det oppførte bygde arealet det innvendige bygde arealet på tegningen, mens det for D.02, E.03 og E.04 er tallet på tegningen inkludert en andel av fellesområdene, og derfor ser disse tre større ut. For A.02, A.05, B.02 og B.03 ligger det innenfor {N2.5} {U} av dette tallet, og A.04 er oppført med {N140.00} {U} mot {N142.60} {U} innvendig på tegningen. Den oppførte terrassen er mindre enn terrassene pluss solterrassen på tegningene (C.02: {N84.82} {U} mot {N97.40} {U}), og C.02 har ingen oppført hage selv om tegningen av stueplanet viser {N30.52} {U}. For A.02 er den oppførte terrassen og hagen, {N40.73} og {N37.37} {U}, de på tegningen av A1, mens tegningen av A2 viser {N37.60} og {N40.23} {U}. Vi bekrefter hvilke tall kontrakten bruker.',
  'Priser och ytor är hämtade från exploatörens onlineprislista, kopierad den 12 oktober 2026, som listar 18 av de 25 bostäderna, alla markerade som tillgängliga. Listan anger inte om priserna inkluderar moms. Kolumnerna för byggyta, terrass och trädgård återges som de är tryckta, och ett streck betyder att ingen trädgård är angiven. De stämmer inte alltid med ritningarna. För C.01 till C.05, D.01, D.03, D.04, E.01 och E.02 är den angivna byggytan ritningens invändiga byggyta, medan den för D.02, E.03 och E.04 är ritningens siffra inklusive en andel av de gemensamma ytorna, och därför ser dessa tre större ut. För A.02, A.05, B.02 och B.03 ligger den inom {N2.5} {U} från den siffran, och A.04 är angiven med {N140.00} {U} mot {N142.60} {U} invändigt på sin ritning. Den angivna terrassen är mindre än terrasserna plus solterrassen på ritningarna (C.02: {N84.82} {U} mot {N97.40} {U}), och C.02 har ingen angiven trädgård trots att ritningen av vardagsplanet anger {N30.52} {U}. För A.02 är den angivna terrassen och trädgården, {N40.73} och {N37.37} {U}, de på ritningen av A1, medan ritningen av A2 anger {N37.60} och {N40.23} {U}. Vi bekräftar vilka siffror avtalet använder.')

# --- timeline, viewing, enquiry, faq
a('See this alongside the other projects in Mijas and Fuengirola we hold.',
  'Véalo junto a los demás proyectos de Mijas y Fuengirola que tenemos.', 'Découvrez-le aux côtés des autres projets de Mijas et Fuengirola que nous suivons.',
  'Sehen Sie es neben den anderen Projekten in Mijas und Fuengirola, die wir betreuen.', 'Сравните его с другими проектами в Михасе и Фуэнхироле, которые мы ведём.',
  'اطّلع عليه إلى جانب المشاريع الأخرى في ميخاس وفوينخيرولا التي نتابعها.', 'Bekijk het naast de andere projecten in Mijas en Fuengirola die wij begeleiden.',
  'Zobaczcie go Państwo obok innych projektów w Mijas i Fuengiroli, które prowadzimy.', 'Se det ved siden av de andre prosjektene i Mijas og Fuengirola vi har.',
  'Se det vid sidan av de andra projekten i Mijas och Fuengirola som vi har.')
a('We agree the reservation, the payment schedule and the completion date with the developer in writing before you sign.',
  'Acordamos por escrito con el promotor la reserva, el calendario de pagos y la fecha de entrega antes de que usted firme.',
  'Nous convenons par écrit avec le promoteur de la réservation, de l’échéancier de paiement et de la date de livraison avant que vous ne signiez.',
  'Wir vereinbaren mit dem Bauträger schriftlich die Reservierung, den Zahlungsplan und den Fertigstellungstermin, bevor Sie unterschreiben.',
  'Мы письменно согласуем с застройщиком бронирование, график платежей и срок завершения до того, как вы подпишете договор.',
  'نتفق كتابةً مع المطوّر على الحجز وجدول الدفعات وموعد الإنجاز قبل أن توقّعوا.',
  'We leggen met de ontwikkelaar schriftelijk de reservering, het betalingsschema en de opleveringsdatum vast voordat u tekent.',
  'Ustalamy z deweloperem na piśmie rezerwację, harmonogram płatności i termin ukończenia, zanim Państwo podpiszą umowę.',
  'Vi avtaler skriftlig med utbyggeren reservasjonen, betalingsplanen og ferdigstillelsesdatoen før De signerer.',
  'Vi kommer skriftligen överens med exploatören om bokningen, betalningsplanen och färdigställandedatumet innan ni skriver under.')
a('A visit is about the location, the plans and the state of the works, and we confirm beforehand what can be seen on site.',
  'Una visita trata de la ubicación, los planos y el estado de las obras, y confirmamos de antemano lo que se puede ver sobre el terreno.',
  'Une visite porte sur l’emplacement, les plans et l’état des travaux, et nous confirmons à l’avance ce qui peut être vu sur place.',
  'Bei einem Besuch geht es um die Lage, die Pläne und den Stand der Arbeiten, und wir bestätigen vorab, was vor Ort zu sehen ist.',
  'Визит посвящён расположению, планировкам и ходу работ, а заранее мы уточняем, что можно увидеть на месте.',
  'تتناول الزيارة الموقع والمخططات وحالة الأعمال، ونؤكد مسبقًا ما يمكن رؤيته في الموقع.',
  'Een bezoek gaat over de ligging, de plattegronden en de stand van de werken, en we bevestigen vooraf wat ter plaatse te zien is.',
  'Wizyta dotyczy lokalizacji, rzutów i stanu prac, a wcześniej potwierdzamy, co można zobaczyć na miejscu.',
  'Et besøk handler om beliggenheten, planene og arbeidenes status, og vi bekrefter på forhånd hva som kan ses på stedet.',
  'Ett besök handlar om läget, planritningarna och arbetenas status, och vi bekräftar i förväg vad som går att se på plats.')
a('Walk the hillside and see where each group of homes sits.',
  'Recorra la ladera y vea dónde se sitúa cada conjunto de viviendas.', 'Parcourez le versant et voyez où se situe chaque ensemble de maisons.',
  'Gehen Sie den Hang ab und sehen Sie, wo jede Hausgruppe liegt.', 'Пройдитесь по склону и посмотрите, где расположена каждая группа домов.',
  'تجوّل على سفح التل وانظر أين تقع كل مجموعة من المنازل.', 'Loop over de helling en zie waar elke groep woningen ligt.',
  'Spacer po zboczu i sprawdzenie, gdzie leży każda grupa domów.', 'Gå rundt i åssiden og se hvor hver gruppe boliger ligger.', 'Gå runt i sluttningen och se var varje grupp av bostäder ligger.')
a('We drive to the beach and the centre of Fuengirola with you and time it.',
  'Vamos en coche con usted a la playa y al centro de Fuengirola y cronometramos el trayecto.', 'Nous roulons avec vous jusqu’à la plage et au centre de Fuengirola et chronométrons le trajet.',
  'Wir fahren mit Ihnen zum Strand und ins Zentrum von Fuengirola und messen die Zeit.', 'Мы едем вместе с вами к пляжу и в центр Фуэнхиролы и засекаем время.',
  'نقود معكم إلى الشاطئ ووسط فوينخيرولا ونحتسب الوقت.', 'We rijden met u naar het strand en het centrum van Fuengirola en timen de rit.',
  'Jedziemy z Państwem na plażę i do centrum Fuengiroli i mierzymy czas przejazdu.', 'Vi kjører med Dem til stranden og sentrum av Fuengirola og tar tiden.',
  'Vi kör med er till stranden och centrala Fuengirola och tar tiden.')
a('Licence, completion date and the contract, before anything is signed.',
  'La licencia, la fecha de entrega y el contrato, antes de firmar nada.', 'Le permis, la date de livraison et le contrat, avant toute signature.',
  'Genehmigung, Fertigstellungstermin und Vertrag, bevor etwas unterschrieben wird.', 'Разрешение, срок завершения и договор — до подписания чего-либо.',
  'الرخصة وموعد الإنجاز والعقد، قبل توقيع أي شيء.', 'De vergunning, de opleveringsdatum en het contract, voordat er iets wordt getekend.',
  'Pozwolenie, termin ukończenia i umowa — zanim cokolwiek zostanie podpisane.', 'Tillatelsen, ferdigstillelsesdatoen og kontrakten, før noe signeres.',
  'Bygglov, färdigställandedatum och avtal, innan något skrivs under.')
a('Ask about <em>Olmo Residences</em>',
  'Pregunte por <em>Olmo Residences</em>', 'Renseignez-vous sur <em>Olmo Residences</em>', 'Fragen Sie nach <em>Olmo Residences</em>', 'Узнайте об <em>Olmo Residences</em>',
  'استفسر عن <em>Olmo Residences</em>', 'Informeer naar <em>Olmo Residences</em>', 'Zapytaj o <em>Olmo Residences</em>', 'Spør om <em>Olmo Residences</em>', 'Fråga om <em>Olmo Residences</em>')
a('Hello Nueva Living, I would like information about Olmo Residences.',
  'Hola Nueva Living, me gustaría recibir información sobre Olmo Residences.', 'Bonjour Nueva Living, je souhaiterais des informations sur Olmo Residences.',
  'Hallo Nueva Living, ich hätte gern Informationen zu Olmo Residences.', 'Здравствуйте, Nueva Living! Мне хотелось бы получить информацию об Olmo Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Olmo Residences.', 'Hallo Nueva Living, ik wil graag informatie over Olmo Residences.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Olmo Residences.', 'Hei Nueva Living, jeg ønsker informasjon om Olmo Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Olmo Residences.')
a('The development has 25 homes. The developer lists 18 of them with a price: 11 with three bedrooms and 7 with four, from EUR 789,000 to EUR 1,327,000.',
  'La promoción tiene 25 viviendas. El promotor lista 18 con precio: 11 de tres dormitorios y 7 de cuatro, de {E789000} a {E1327000}.',
  'Le programme compte 25 maisons. Le promoteur en liste 18 avec un prix : 11 de trois chambres et 7 de quatre, de {E789000} à {E1327000}.',
  'Das Projekt hat 25 Häuser. Der Bauträger listet 18 davon mit Preis: 11 mit drei und 7 mit vier Schlafzimmern, von {E789000} bis {E1327000}.',
  'В комплексе 25 домов. Застройщик указывает цену у 18 из них: 11 с тремя спальнями и 7 с четырьмя, от {E789000} до {E1327000}.',
  'يضم المشروع 25 منزلًا. ويدرج المطوّر 18 منها بسعر: 11 بثلاث غرف نوم و7 بأربع، من {E789000} إلى {E1327000}.',
  'Het project telt 25 woningen. De ontwikkelaar vermeldt er 18 met een prijs: 11 met drie en 7 met vier slaapkamers, van {E789000} tot {E1327000}.',
  'Inwestycja liczy 25 domów. Deweloper podaje ceny 18 z nich: 11 z trzema i 7 z czterema sypialniami, od {E789000} do {E1327000}.',
  'Prosjektet har 25 boliger. Utbyggeren oppfører 18 av dem med pris: 11 med tre og 7 med fire soverom, fra {E789000} til {E1327000}.',
  'Projektet har 25 bostäder. Exploatören listar 18 av dem med pris: 11 med tre och 7 med fyra sovrum, från {E789000} till {E1327000}.')
a('Does every home have a pool?', '¿Tiene piscina cada vivienda?', 'Chaque maison a-t-elle une piscine ?', 'Hat jedes Haus einen Pool?', 'Есть ли бассейн у каждого дома?',
  'هل لكل منزل مسبح؟', 'Heeft elke woning een zwembad?', 'Czy każdy dom ma basen?', 'Har hver bolig basseng?', 'Har varje bostad en pool?')
a('Yes. The developer’s documents say that each home has its own outdoor space and a private swimming pool.',
  'Sí. Los documentos del promotor dicen que cada vivienda tiene su propio espacio exterior y una piscina privada.',
  'Oui. Les documents du promoteur indiquent que chaque maison dispose de son propre espace extérieur et d’une piscine privée.',
  'Ja. Laut den Unterlagen des Bauträgers hat jedes Haus einen eigenen Außenbereich und einen privaten Swimmingpool.',
  'Да. В документах застройщика сказано, что у каждого дома есть собственное открытое пространство и частный бассейн.',
  'نعم. تذكر وثائق المطوّر أن لكل منزل مساحة خارجية خاصة ومسبحًا خاصًا.',
  'Ja. In de documenten van de ontwikkelaar staat dat elke woning een eigen buitenruimte en een privézwembad heeft.',
  'Tak. Dokumenty dewelopera mówią, że każdy dom ma własną przestrzeń zewnętrzną i prywatny basen.',
  'Ja. Utbyggerens dokumenter sier at hver bolig har egen utendørs plass og et privat svømmebasseng.',
  'Ja. Exploatörens dokument anger att varje bostad har egen utomhusyta och en privat pool.')
a('The price list does not say. We confirm the taxes and purchase costs in writing.',
  'La lista de precios no lo indica. Confirmamos por escrito los impuestos y los gastos de compra.', 'La liste de prix ne le dit pas. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Die Preisliste sagt es nicht. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.', 'В прайс-листе об этом не сказано. Мы письменно подтверждаем налоги и расходы на покупку.',
  'لا توضح قائمة الأسعار ذلك. نؤكد الضرائب ومصاريف الشراء كتابةً.', 'De prijslijst vermeldt het niet. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Cennik tego nie wskazuje. Podatki i koszty zakupu potwierdzamy na piśmie.', 'Prislisten oppgir det ikke. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan anger det inte. Vi bekräftar skatter och köpkostnader skriftligen.')
a('The specification describes a garage with vehicle access and a pre-installation for electric-vehicle charging at each parking space. The price list does not say whether a space is included, so we ask.',
  'La memoria de calidades describe un garaje con acceso de vehículos y una preinstalación de recarga de vehículos eléctricos en cada plaza. La lista de precios no indica si se incluye una plaza, por lo que lo preguntamos.',
  'Le descriptif décrit un garage avec accès pour véhicules et une pré-installation de recharge pour véhicules électriques à chaque place. La liste de prix n’indique pas si une place est incluse ; nous posons donc la question.',
  'Die Baubeschreibung nennt eine Garage mit Fahrzeugzufahrt und eine Vorinstallation für das Laden von Elektrofahrzeugen an jedem Stellplatz. Die Preisliste sagt nicht, ob ein Stellplatz enthalten ist, daher fragen wir nach.',
  'В спецификации описан гараж с въездом для автомобилей и подготовка под зарядку электромобилей у каждого парковочного места. В прайс-листе не сказано, входит ли место в цену, поэтому мы уточняем это.',
  'تصف المواصفات مرآبًا بمدخل للسيارات وتجهيزًا مسبقًا لشحن السيارات الكهربائية عند كل موقف. ولا توضح قائمة الأسعار ما إذا كان الموقف مشمولًا، لذلك نستفسر عن ذلك.',
  'Het lastenboek beschrijft een garage met toegang voor voertuigen en een voorbereiding voor het laden van elektrische auto’s bij elke parkeerplaats. De prijslijst vermeldt niet of een plaats is inbegrepen, dus we vragen ernaar.',
  'Specyfikacja opisuje garaż z wjazdem dla pojazdów i przygotowanie do ładowania pojazdów elektrycznych przy każdym miejscu parkingowym. Cennik nie wskazuje, czy miejsce jest wliczone, dlatego o to pytamy.',
  'Spesifikasjonen beskriver en garasje med kjøretøyadkomst og forberedelse for lading av elbil ved hver parkeringsplass. Prislisten oppgir ikke om en plass er inkludert, så vi spør om det.',
  'Specifikationen beskriver ett garage med infart för fordon och förberedelse för laddning av elbil vid varje parkeringsplats. Prislistan anger inte om en plats ingår, så vi frågar om det.')
a('None of the developer’s documents gives a completion date. Nueva Living asks for it in writing before any reservation.',
  'Ninguno de los documentos del promotor indica una fecha de entrega. Nueva Living la pide por escrito antes de cualquier reserva.',
  'Aucun document du promoteur ne donne de date de livraison. Nueva Living la demande par écrit avant toute réservation.',
  'Keine der Unterlagen des Bauträgers nennt einen Fertigstellungstermin. Nueva Living fragt ihn vor jeder Reservierung schriftlich an.',
  'Ни в одном документе застройщика нет срока завершения. Nueva Living письменно запрашивает его перед любым бронированием.',
  'لا تذكر أي من وثائق المطوّر موعد الإنجاز. وتطلبه Nueva Living كتابةً قبل أي حجز.',
  'Geen van de documenten van de ontwikkelaar noemt een opleveringsdatum. Nueva Living vraagt er vóór elke reservering schriftelijk naar.',
  'Żaden z dokumentów dewelopera nie podaje terminu ukończenia. Nueva Living prosi o niego na piśmie przed każdą rezerwacją.',
  'Ingen av utbyggerens dokumenter oppgir en ferdigstillelsesdato. Nueva Living ber om den skriftlig før enhver reservasjon.',
  'Inget av exploatörens dokument anger ett färdigställandedatum. Nueva Living ber om det skriftligen före varje bokning.')
a('What is shared?', '¿Qué se comparte?', 'Qu’est-ce qui est partagé ?', 'Was wird gemeinsam genutzt?', 'Что используется совместно?', 'ما الذي يُشترك فيه؟',
  'Wat wordt gedeeld?', 'Co jest wspólne?', 'Hva deles?', 'Vad delas?')
a('A fully equipped gym, an outdoor pool with salt chlorination and a sunbathing area, and a multi-purpose space for working, studying or meeting, in landscaped communal grounds.',
  'Un gimnasio totalmente equipado, una piscina exterior con cloración salina y zona de solárium, y un espacio polivalente para trabajar, estudiar o reunirse, en zonas comunes ajardinadas.',
  'Une salle de sport entièrement équipée, une piscine extérieure au sel avec un espace solarium, et un espace polyvalent pour travailler, étudier ou se réunir, dans des parties communes paysagées.',
  'Ein voll ausgestatteter Fitnessraum, ein Außenpool mit Salzchlorierung und Liegefläche sowie ein Mehrzweckraum zum Arbeiten, Lernen oder für Treffen, in begrünten Gemeinschaftsflächen.',
  'Полностью оборудованный тренажёрный зал, открытый бассейн с солевым хлорированием и зоной для загара, а также многофункциональное помещение для работы, учёбы или встреч — на озеленённой общей территории.',
  'صالة رياضية مجهزة بالكامل، ومسبح خارجي بتعقيم بالملح ومنطقة للتشمس، وقاعة متعددة الاستخدامات للعمل أو الدراسة أو الاجتماعات، في مناطق مشتركة مشجّرة.',
  'Een volledig uitgeruste fitnessruimte, een buitenzwembad met zoutchlorering en een zonneterras, en een multifunctionele ruimte om te werken, te studeren of af te spreken, in beplante gemeenschappelijke buitenruimten.',
  'W pełni wyposażona siłownia, basen zewnętrzny z elektrolizą soli i strefą do opalania oraz sala wielofunkcyjna do pracy, nauki lub spotkań, na zagospodarowanym terenie wspólnym.',
  'Et fullt utstyrt treningsrom, et utendørsbasseng med saltklorering og solplass, og et flerbruksrom for arbeid, studier eller møter, i beplantede fellesområder.',
  'Ett fullt utrustat gym, en utomhuspool med saltklorering och solplats samt ett flexibelt rum för arbete, studier eller möten, på planterade gemensamma ytor.')

# unit sizes: built per-locale template; references stay as printed
SIZE = {
 'es': ('{b} {U} construidos', '{t} {U} de terraza', '{g} {U} de jardín'),
 'fr': ('{b} {U} construits', '{t} {U} de terrasse', '{g} {U} de jardin'),
 'de': ('{b} {U} bebaut', '{t} {U} Terrasse', '{g} {U} Garten'),
 'ru': ('{b} {U} застроенной площади', 'терраса {t} {U}', 'сад {g} {U}'),
 'ar': ('{b} {U} مبنية', '{t} {U} تراس', '{g} {U} حديقة'),
 'nl': ('{b} {U} bebouwd', '{t} {U} terras', '{g} {U} tuin'),
 'pl': ('{b} {U} zabudowy', '{t} {U} tarasu', '{g} {U} ogrodu'),
 'no': ('{b} {U} bygd', '{t} {U} terrasse', '{g} {U} hage'),
 'sv': ('{b} {U} byggyta', '{t} {U} terrass', '{g} {U} trädgård'),
}
proj = json.load(open('content/liora-projects/olmo-residences/project.json'))
for u in proj['availability']['units']:
    same(u['reference'])
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm garden)?', u['size'])
    assert m, u['size']
    b, t, g = m.groups()
    out = []
    for l in LOCS:
        parts = [SIZE[l][0].format(b='{N%s}' % b, U='{U}'), SIZE[l][1].format(t='{N%s}' % t, U='{U}')]
        if g:
            parts.append(SIZE[l][2].format(g='{N%s}' % g, U='{U}'))
        out.append(('، ' if l == 'ar' else ', ').join(parts))
    a(u['size'], *out)

json.dump(T, open(f'{SP}/tr_o.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
