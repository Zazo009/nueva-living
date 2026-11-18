# -*- coding: utf-8 -*-
"""Lentisco Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E363000}
money, {N70.89} decimal number, {U} the area unit, {D5.11.2026} a date, {P363000} a price plus
the local tax word, {T} the local tax word.
    python3 tools/import/k_lentisco_residences.py <scratch dir>   (writes <dir>/tr_a.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة', 'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
TAXP = dict(TAXW); TAXP['no'] = 'mva.'
FROM = {'es': 'Desde {}', 'fr': 'À partir de {}', 'de': 'Ab {}', 'ru': 'От {}', 'ar': 'ابتداءً من {}',
        'nl': 'Vanaf {}', 'pl': 'Od {}', 'no': 'Fra {}', 'sv': 'Från {}'}
MONTHS = {
    11: dict(es='noviembre', fr='novembre', de='November', ru='ноября', ar='نوفمبر', nl='november', pl='listopada', no='november', sv='november'),
}
T = {}
proj = json.load(open('content/liora-projects/lentisco-residences/project.json'))


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def date(d, m, y, l):
    mo = MONTHS[m][l]
    return {'es': f'{d} de {mo} de {y}', 'fr': f'{d} {mo} {y}', 'de': f'{d}. {mo} {y}', 'ru': f'{d} {mo} {y} года',
            'ar': f'{d} {mo} {y}', 'nl': f'{d} {mo} {y}', 'pl': f'{d} {mo} {y} roku', 'no': f'{d}. {mo} {y}',
            'sv': f'{d} {mo} {y}'}[l]


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    text = re.sub(r'\{D(\d+)\.(\d+)\.(\d+)\}', lambda m: date(m.group(1), int(m.group(2)), m.group(3), l), text)
    text = re.sub(r'\{P(\d+)\}', lambda m: money(int(m.group(1)), l) + ' + ' + TAXP[l], text)
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


same('Lentisco Residences'); same('Lentisco'); same('Lentisco <em>Residences</em>'); same('')
# Unit references are identifiers: the page localises them at render time.
for u in proj['availability']['units']:
    same(u['reference'])

# ---- description, SEO, hero, card ------------------------------------------------------------

a('.description',
  'Tres áticos de dos dormitorios disponibles en un edificio nuevo de 15 viviendas en Los Pacos, Fuengirola, segunda fase de un residencial consolidado cuya piscina, gimnasio, sauna y lavandería ya están en funcionamiento: dos con solárium privado en la cubierta y uno con una terraza cubierta de {N46.65} {U}, desde {E363000} más IVA. La entrega está prevista para septiembre de 2027.',
  'Trois penthouses de deux chambres disponibles dans un immeuble neuf de 15 logements à Los Pacos, Fuengirola, deuxième phase d’une résidence établie dont la piscine, la salle de sport, le sauna et la laverie sont déjà en service : deux avec un solarium privé sur le toit et un avec une terrasse couverte de {N46.65} {U}, à partir de {E363000} hors TVA. La livraison est prévue pour septembre 2027.',
  'Drei Penthäuser mit zwei Schlafzimmern verfügbar, in einem neuen Gebäude mit 15 Wohnungen in Los Pacos, Fuengirola, dem zweiten Bauabschnitt einer bestehenden Anlage, deren Pool, Fitnessraum, Sauna und Waschküche bereits in Betrieb sind: zwei mit privatem Dachsolarium und eines mit einer überdachten Terrasse von {N46.65} {U}, ab {E363000} zuzüglich MwSt. Die Fertigstellung ist für September 2027 geplant.',
  'Три пентхауса с двумя спальнями в продаже в новом доме на 15 квартир в Лос-Пакос, Фуэнхирола, — второй очереди уже сложившегося комплекса, где бассейн, тренажёрный зал, сауна и прачечная уже работают: два с собственным солярием на крыше и один с крытой террасой {N46.65} {U}, от {E363000} плюс НДС. Сдача запланирована на сентябрь 2027 года.',
  'ثلاثة بنتهاوس بغرفتي نوم متاحة في مبنى جديد من 15 مسكنًا في لوس باكوس، فوينخيرولا، وهو المرحلة الثانية من مجمع قائم يعمل فيه المسبح والصالة الرياضية والساونا والمغسلة بالفعل: اثنان مع سولاريوم خاص على السطح وواحد مع تراس مسقوف مساحته {N46.65} {U}، ابتداءً من {E363000} زائد ضريبة القيمة المضافة. ومن المقرر الإنجاز في سبتمبر 2027.',
  'Drie penthouses met twee slaapkamers beschikbaar in een nieuw gebouw met 15 woningen in Los Pacos, Fuengirola, de tweede fase van een bestaand complex waarvan het zwembad, de fitnessruimte, de sauna en de wasruimte al in gebruik zijn: twee met een eigen solarium op het dak en één met een overdekt terras van {N46.65} {U}, vanaf {E363000} plus btw. De oplevering is gepland voor september 2027.',
  'Trzy penthouse’y z dwiema sypialniami dostępne w nowym budynku z 15 mieszkaniami w Los Pacos w Fuengiroli, drugim etapie istniejącego osiedla, którego basen, siłownia, sauna i pralnia już działają: dwa z prywatnym solarium na dachu i jeden z zadaszonym tarasem o powierzchni {N46.65} {U}, od {E363000} plus VAT. Zakończenie budowy zaplanowano na wrzesień 2027 roku.',
  'Tre toppleiligheter med to soverom tilgjengelige i et nytt bygg med 15 boliger i Los Pacos, Fuengirola, andre byggetrinn i et etablert anlegg der bassenget, treningsrommet, badstuen og vaskerommet allerede er i bruk: to med egen solterrasse på taket og én med en overbygd terrasse på {N46.65} {U}, fra {E363000} pluss mva. Ferdigstillelse er planlagt til september 2027.',
  'Tre takvåningar med två sovrum tillgängliga i en ny byggnad med 15 bostäder i Los Pacos, Fuengirola, andra etappen i ett etablerat område där poolen, gymmet, bastun och tvättstugan redan är i bruk: två med egen solterrass på taket och en med en överbyggd terrass på {N46.65} {U}, från {E363000} plus IVA (spansk moms). Färdigställandet är planerat till september 2027.')
a('.seoDescription',
  'Tres áticos de dos dormitorios en Los Pacos, Fuengirola, dos con solárium en la cubierta, en una nueva fase de un residencial consolidado con piscina y gimnasio, desde {E363000} más IVA.',
  'Trois penthouses de deux chambres à Los Pacos, Fuengirola, dont deux avec un solarium sur le toit, dans une nouvelle phase d’une résidence établie avec piscine et salle de sport, à partir de {E363000} hors TVA.',
  'Drei Penthäuser mit zwei Schlafzimmern in Los Pacos, Fuengirola, zwei mit Dachsolarium, in einem neuen Bauabschnitt einer bestehenden Anlage mit Pool und Fitnessraum, ab {E363000} zuzüglich MwSt.',
  'Три пентхауса с двумя спальнями в Лос-Пакос, Фуэнхирола, два с солярием на крыше, в новой очереди сложившегося комплекса с бассейном и тренажёрным залом, от {E363000} плюс НДС.',
  'ثلاثة بنتهاوس بغرفتي نوم في لوس باكوس، فوينخيرولا، اثنان منها مع سولاريوم على السطح، في مرحلة جديدة من مجمع قائم مع مسبح وصالة رياضية، ابتداءً من {E363000} زائد ضريبة القيمة المضافة.',
  'Drie penthouses met twee slaapkamers in Los Pacos, Fuengirola, twee met een solarium op het dak, in een nieuwe fase van een bestaand complex met zwembad en fitnessruimte, vanaf {E363000} plus btw.',
  'Trzy penthouse’y z dwiema sypialniami w Los Pacos w Fuengiroli, dwa z solarium na dachu, w nowym etapie istniejącego osiedla z basenem i siłownią, od {E363000} plus VAT.',
  'Tre toppleiligheter med to soverom i Los Pacos, Fuengirola, to med solterrasse på taket, i et nytt byggetrinn i et etablert anlegg med basseng og treningsrom, fra {E363000} pluss mva.',
  'Tre takvåningar med två sovrum i Los Pacos, Fuengirola, två med solterrass på taket, i en ny etapp av ett etablerat område med pool och gym, från {E363000} plus IVA.')
a('.twitterDescription',
  'Tres áticos de dos dormitorios en Los Pacos, Fuengirola, desde {E363000} más IVA.',
  'Trois penthouses de deux chambres à Los Pacos, Fuengirola, à partir de {E363000} hors TVA.',
  'Drei Penthäuser mit zwei Schlafzimmern in Los Pacos, Fuengirola, ab {E363000} zuzüglich MwSt.',
  'Три пентхауса с двумя спальнями в Лос-Пакос, Фуэнхирола, от {E363000} плюс НДС.',
  'ثلاثة بنتهاوس بغرفتي نوم في لوس باكوس، فوينخيرولا، ابتداءً من {E363000} زائد ضريبة القيمة المضافة.',
  'Drie penthouses met twee slaapkamers in Los Pacos, Fuengirola, vanaf {E363000} plus btw.',
  'Trzy penthouse’y z dwiema sypialniami w Los Pacos w Fuengiroli, od {E363000} plus VAT.',
  'Tre toppleiligheter med to soverom i Los Pacos, Fuengirola, fra {E363000} pluss mva.',
  'Tre takvåningar med två sovrum i Los Pacos, Fuengirola, från {E363000} plus IVA.')
a('.hero.location', 'Los Pacos, Fuengirola', 'Los Pacos, Fuengirola', 'Los Pacos, Fuengirola', 'Лос-Пакос, Фуэнхирола',
  'لوس باكوس، فوينخيرولا', 'Los Pacos, Fuengirola', 'Los Pacos, Fuengirola', 'Los Pacos, Fuengirola', 'Los Pacos, Fuengirola')
a('.hero.delivery', 'Entrega septiembre 2027', 'Livraison septembre 2027', 'Fertigstellung September 2027', 'Сдача в сентябре 2027',
  'الإنجاز سبتمبر 2027', 'Oplevering september 2027', 'Odbiór we wrześniu 2027', 'Ferdigstillelse september 2027',
  'Färdigställande september 2027')
a('.card.description',
  'Tres áticos de dos dormitorios en un edificio nuevo de 15 viviendas en Los Pacos, Fuengirola, dos con solárium privado en la cubierta, junto a un residencial consolidado con piscina, gimnasio y sauna.',
  'Trois penthouses de deux chambres dans un immeuble neuf de 15 logements à Los Pacos, Fuengirola, dont deux avec un solarium privé sur le toit, à côté d’une résidence établie avec piscine, salle de sport et sauna.',
  'Drei Penthäuser mit zwei Schlafzimmern in einem neuen Gebäude mit 15 Wohnungen in Los Pacos, Fuengirola, zwei mit privatem Dachsolarium, neben einer bestehenden Anlage mit Pool, Fitnessraum und Sauna.',
  'Три пентхауса с двумя спальнями в новом доме на 15 квартир в Лос-Пакос, Фуэнхирола, два с собственным солярием на крыше, рядом со сложившимся комплексом с бассейном, тренажёрным залом и сауной.',
  'ثلاثة بنتهاوس بغرفتي نوم في مبنى جديد من 15 مسكنًا في لوس باكوس، فوينخيرولا، اثنان منها مع سولاريوم خاص على السطح، بجوار مجمع قائم فيه مسبح وصالة رياضية وساونا.',
  'Drie penthouses met twee slaapkamers in een nieuw gebouw met 15 woningen in Los Pacos, Fuengirola, twee met een eigen solarium op het dak, naast een bestaand complex met zwembad, fitnessruimte en sauna.',
  'Trzy penthouse’y z dwiema sypialniami w nowym budynku z 15 mieszkaniami w Los Pacos w Fuengiroli, dwa z prywatnym solarium na dachu, obok istniejącego osiedla z basenem, siłownią i sauną.',
  'Tre toppleiligheter med to soverom i et nytt bygg med 15 boliger i Los Pacos, Fuengirola, to med egen solterrasse på taket, ved siden av et etablert anlegg med basseng, treningsrom og badstue.',
  'Tre takvåningar med två sovrum i en ny byggnad med 15 bostäder i Los Pacos, Fuengirola, två med egen solterrass på taket, intill ett etablerat område med pool, gym och bastu.')
a('.quickFacts[4][1]', '15 viviendas en esta fase', '15 logements dans cette phase', '15 Wohnungen in diesem Bauabschnitt',
  '15 квартир в этой очереди', '15 مسكنًا في هذه المرحلة', '15 woningen in deze fase', '15 mieszkań w tym etapie',
  '15 boliger i dette byggetrinnet', '15 bostäder i denna etapp')

# ---- images -------------------------------------------------------------------------------------

a('.images.hero.alt',
  'Vista generada por ordenador del edificio de cinco plantas con balcones curvos blancos y paredes terracota, sobre un muro de contención ajardinado',
  'Vue de synthèse de l’immeuble de cinq niveaux aux balcons courbes blancs et aux murs couleur terre cuite, au-dessus d’un mur de soutènement planté',
  'Computergenerierte Ansicht des fünfgeschossigen Gebäudes mit weißen geschwungenen Balkonen und terrakottafarbenen Wänden über einer bepflanzten Stützmauer',
  'Компьютерная визуализация пятиэтажного дома с белыми изогнутыми балконами и терракотовыми стенами над озеленённой подпорной стеной',
  'منظر مُنشأ بالحاسوب للمبنى ذي الطوابق الخمسة بشرفاته البيضاء المنحنية وجدرانه بلون التيراكوتا، فوق جدار استنادي مزروع',
  'Computergegenereerd beeld van het gebouw van vijf verdiepingen met witte gebogen balkons en terracottakleurige muren, boven een beplante keermuur',
  'Wizualizacja komputerowa pięciokondygnacyjnego budynku z białymi, zaokrąglonymi balkonami i ścianami w kolorze terakoty, nad obsadzonym zielenią murem oporowym',
  'Datagenerert bilde av bygget i fem etasjer med hvite, buede balkonger og terrakottafargede vegger, over en beplantet støttemur',
  'Datorgenererad bild av den fem våningar höga byggnaden med vita, svängda balkonger och terrakottafärgade väggar, ovanför en planterad stödmur')
a('.images.architecture.alt',
  'Vista generada por ordenador del edificio desde la calle inferior, con los jardines escalonados de las viviendas de planta baja y la planta de áticos bajo una amplia cubierta blanca',
  'Vue de synthèse de l’immeuble depuis la rue en contrebas, avec les jardins en terrasses des logements du rez-de-chaussée et le niveau des penthouses sous un large toit blanc',
  'Computergenerierte Ansicht des Gebäudes von der Straße unterhalb, mit den Gartenterrassen der Erdgeschosswohnungen und der Penthouse-Ebene unter einem tiefen weißen Dach',
  'Компьютерная визуализация дома с нижней улицы: садовые террасы квартир первого этажа и уровень пентхаусов под широким белым козырьком крыши',
  'منظر مُنشأ بالحاسوب للمبنى من الطريق في الأسفل، مع حدائق مساكن الطابق الأرضي المتدرجة ومستوى البنتهاوس تحت سقف أبيض عريض',
  'Computergegenereerd beeld van het gebouw vanaf de weg eronder, met de tuinterrassen van de benedenwoningen en de penthouseverdieping onder een diep wit dak',
  'Wizualizacja komputerowa budynku od strony niższej ulicy, z ogrodami tarasowymi mieszkań na parterze i poziomem penthouse’ów pod głębokim białym dachem',
  'Datagenerert bilde av bygget sett fra veien nedenfor, med hageterrassene til boligene på bakkeplan og toppleilighetsetasjen under et dypt, hvitt tak',
  'Datorgenererad bild av byggnaden från vägen nedanför, med trädgårdsterrasserna till bostäderna i markplan och takvåningsplanet under ett djupt, vitt tak')
a('.images.lifestyle.alt',
  'Salón comedor generado por ordenador con mesa de cristal, pared de listones de madera y puerta corredera a una terraza',
  'Séjour et espace repas en image de synthèse, avec une table en verre, un mur à lames de bois et une porte coulissante sur une terrasse',
  'Computergenerierter Wohn- und Essbereich mit Glastisch, Holzlamellenwand und Schiebetür zur Terrasse',
  'Компьютерная визуализация гостиной-столовой со стеклянным столом, стеной из деревянных реек и раздвижной дверью на террасу',
  'غرفة معيشة وطعام مُنشأة بالحاسوب مع طاولة زجاجية وجدار من الشرائح الخشبية وباب منزلق إلى تراس',
  'Computergegenereerde woon-eetkamer met een glazen tafel, een wand van houten latten en een schuifpui naar een terras',
  'Wizualizacja komputerowa salonu z jadalnią: szklany stół, ściana z drewnianych lameli i przesuwne drzwi na taras',
  'Datagenerert stue og spiseplass med glassbord, en vegg med trespiler og skyvedør ut til en terrasse',
  'Datorgenererat vardagsrum med matplats, glasbord, en vägg med träribbor och skjutdörr ut mot en terrass')
a('.images.privateViewing.alt',
  'Dormitorio generado por ordenador con cama doble, dos dibujos de línea enmarcados y una ventana con vistas a la ladera',
  'Chambre en image de synthèse avec un lit double, deux dessins au trait encadrés et une fenêtre ouvrant sur la colline',
  'Computergeneriertes Schlafzimmer mit Doppelbett, zwei gerahmten Strichzeichnungen und einem Fenster zum Hang',
  'Компьютерная визуализация спальни с двуспальной кроватью, двумя графическими рисунками в рамах и окном с видом на склон',
  'غرفة نوم مُنشأة بالحاسوب مع سرير مزدوج ورسمتين خطيتين مؤطرتين ونافذة تطل على التلة',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, twee ingelijste lijntekeningen en een raam met uitzicht op de heuvel',
  'Wizualizacja komputerowa sypialni z podwójnym łóżkiem, dwoma oprawionymi rysunkami i oknem z widokiem na zbocze',
  'Datagenerert soverom med dobbeltseng, to innrammede strektegninger og et vindu mot åssiden',
  'Datorgenererat sovrum med dubbelsäng, två inramade linjeteckningar och ett fönster mot sluttningen')

# ---- media ----------------------------------------------------------------------------------------

a('.media.copy',
  'Vistas generadas por ordenador del edificio nuevo y de los interiores, fotografías de la piscina y del gimnasio, y los planos de los tres áticos disponibles.',
  'Vues de synthèse de l’immeuble neuf et des intérieurs, photographies de la piscine et de la salle de sport, et plans des trois penthouses disponibles.',
  'Computergenerierte Ansichten des neuen Gebäudes und der Innenräume, Fotos des Pools und des Fitnessraums sowie die Grundrisse der drei verfügbaren Penthäuser.',
  'Компьютерные визуализации нового дома и интерьеров, фотографии бассейна и тренажёрного зала, а также планировки трёх доступных пентхаусов.',
  'مناظر مُنشأة بالحاسوب للمبنى الجديد وللتصاميم الداخلية، وصور فوتوغرافية للمسبح والصالة الرياضية، ومخططات البنتهاوس الثلاثة المتاحة.',
  'Computergegenereerde beelden van het nieuwe gebouw en de interieurs, foto’s van het zwembad en de fitnessruimte, en de plattegronden van de drie beschikbare penthouses.',
  'Wizualizacje komputerowe nowego budynku i wnętrz, zdjęcia basenu i siłowni oraz rzuty trzech dostępnych penthouse’ów.',
  'Datagenererte bilder av det nye bygget og interiørene, fotografier av bassenget og treningsrommet, og plantegningene til de tre tilgjengelige toppleilighetene.',
  'Datorgenererade bilder av den nya byggnaden och interiörerna, fotografier av poolen och gymmet samt planritningarna för de tre tillgängliga takvåningarna.')
a('.media.note',
  'Las vistas del edificio y de las estancias están generadas por ordenador: el folleto indica que son meramente informativas, que el mobiliario no está incluido y que los acabados, colores, sanitarios y muebles de cocina son aproximados. La piscina y el gimnasio son fotografías de instalaciones comunes ya existentes, que el folleto presenta como preexistentes para esta fase. Los planos son los del propio promotor para los tres áticos, sin los logotipos, la tabla de superficies ni el plano de situación; indican que superficies y distribuciones son previstas y pueden cambiar por exigencias técnicas, jurídicas o comerciales.',
  'Les vues de l’immeuble et des pièces sont des images de synthèse : la brochure précise qu’elles sont purement indicatives, que le mobilier n’est pas inclus et que les finitions, couleurs, sanitaires et meubles de cuisine sont approximatifs. La piscine et la salle de sport sont des photographies d’équipements communs existants, que la brochure présente comme déjà en place pour cette phase. Les plans sont ceux du promoteur pour les trois penthouses, sans les logos, le tableau des surfaces ni le plan de situation ; ils indiquent que surfaces et agencements sont prévisionnels et peuvent changer pour des raisons techniques, juridiques ou commerciales, et les noms des pièces y sont en espagnol.',
  'Die Ansichten des Gebäudes und der Räume sind computergeneriert: Die Broschüre bezeichnet sie als rein informativ, Möbel sind nicht enthalten, und Oberflächen, Farben, Sanitärobjekte und Küchenmöbel sind nur annähernd dargestellt. Pool und Fitnessraum sind Fotos bereits bestehender Gemeinschaftseinrichtungen, die die Broschüre für diesen Bauabschnitt als vorhanden aufführt. Die Grundrisse sind die eigenen Pläne des Bauträgers für die drei Penthäuser, ohne Logos, Flächentabelle und Lageplan; sie weisen darauf hin, dass Flächen und Aufteilung vorläufig sind und sich aus technischen, rechtlichen oder kaufmännischen Gründen ändern können, und die Raumbezeichnungen sind auf Spanisch.',
  'Виды дома и помещений — компьютерные визуализации: в буклете сказано, что они носят исключительно информационный характер, мебель не входит в стоимость, а отделка, цвета, сантехника и кухонная мебель показаны приблизительно. Бассейн и тренажёрный зал — фотографии уже существующих общих объектов, которые буклет указывает как имеющиеся для этой очереди. Планировки — собственные планы застройщика для трёх пентхаусов, без логотипов, таблицы площадей и схемы расположения; в них указано, что площади и планировки предварительные и могут измениться по техническим, юридическим или коммерческим причинам, а названия помещений даны на испанском.',
  'مناظر المبنى والغرف مُنشأة بالحاسوب: يذكر الكتيّب أنها لأغراض إعلامية فقط، وأن الأثاث غير مشمول، وأن التشطيبات والألوان والأدوات الصحية وخزائن المطبخ تقريبية. أما المسبح والصالة الرياضية فهي صور فوتوغرافية لمرافق مشتركة قائمة، يذكرها الكتيّب على أنها موجودة مسبقًا لهذه المرحلة. والمخططات هي مخططات المطوّر نفسه للبنتهاوس الثلاثة، بعد إزالة الشعارات وجدول المساحات ومخطط الموقع؛ وهي تنص على أن المساحات والتوزيع مبدئية وقد تتغير لأسباب فنية أو قانونية أو تجارية، وأسماء الغرف عليها بالإسبانية.',
  'De beelden van het gebouw en de kamers zijn computergegenereerd: volgens de brochure zijn ze uitsluitend informatief, is het meubilair niet inbegrepen en zijn afwerking, kleuren, sanitair en keukenmeubelen bij benadering. Het zwembad en de fitnessruimte zijn foto’s van bestaande gemeenschappelijke voorzieningen, die de brochure voor deze fase als al aanwezig vermeldt. De plattegronden zijn de eigen tekeningen van de ontwikkelaar voor de drie penthouses, zonder logo’s, oppervlaktetabel en situatieschets; ze vermelden dat oppervlakten en indeling voorlopig zijn en om technische, juridische of commerciële redenen kunnen wijzigen, en de ruimtenamen staan er in het Spaans op.',
  'Widoki budynku i pomieszczeń to wizualizacje komputerowe: broszura podaje, że mają charakter wyłącznie informacyjny, meble nie są wliczone, a wykończenia, kolory, armatura sanitarna i meble kuchenne są przybliżone. Basen i siłownia to zdjęcia istniejących już części wspólnych, które broszura wymienia jako dostępne dla tego etapu. Rzuty to własne plany dewelopera dla trzech penthouse’ów, bez logotypów, tabeli powierzchni i planu sytuacyjnego; zaznaczono na nich, że powierzchnie i układ są wstępne i mogą się zmienić z przyczyn technicznych, prawnych lub handlowych, a nazwy pomieszczeń są po hiszpańsku.',
  'Bildene av bygget og rommene er datagenererte: brosjyren sier at de kun er veiledende, at møblene ikke er inkludert og at overflater, farger, sanitærutstyr og kjøkkeninnredning er omtrentlige. Bassenget og treningsrommet er fotografier av eksisterende fellesanlegg, som brosjyren oppgir som allerede på plass for dette byggetrinnet. Plantegningene er utbyggerens egne tegninger av de tre toppleilighetene, uten logoer, arealtabell og situasjonskart; de sier at arealer og planløsning er foreløpige og kan endres av tekniske, juridiske eller kommersielle grunner, og romnavnene på dem er på spansk.',
  'Bilderna av byggnaden och rummen är datorgenererade: broschyren anger att de endast är vägledande, att möblerna inte ingår och att ytskikt, färger, sanitetsporslin och köksinredning är ungefärliga. Poolen och gymmet är fotografier av befintliga gemensamma anläggningar, som broschyren anger som redan på plats för denna etapp. Planritningarna är exploatörens egna ritningar av de tre takvåningarna, utan logotyper, ytuppställning och situationsplan; de anger att ytor och planlösning är preliminära och kan ändras av tekniska, juridiska eller kommersiella skäl, och rumsnamnen på dem är på spanska.')
# Spanish: the plans are already in Spanish, so the sentence about their language is dropped there.
a('.media.items[0].caption', 'El edificio nuevo', 'Le nouvel immeuble', 'Das neue Gebäude', 'Новый дом', 'المبنى الجديد',
  'Het nieuwe gebouw', 'Nowy budynek', 'Det nye bygget', 'Den nya byggnaden')
a('.media.items[3].alt',
  'Cocina en L generada por ordenador, en gris brillo, con frigorífico alto, placa de inducción y mesa de comedor de cristal',
  'Cuisine en L en image de synthèse, gris brillant, avec un grand réfrigérateur, une plaque à induction et une table en verre',
  'Computergenerierte L-Küche in Hochglanzgrau mit hohem Kühlschrank, Induktionskochfeld und gläsernem Esstisch',
  'Компьютерная визуализация Г-образной кухни в сером глянце с высоким холодильником, индукционной варочной панелью и стеклянным обеденным столом',
  'مطبخ على شكل حرف L مُنشأ بالحاسوب باللون الرمادي اللامع، مع ثلاجة طويلة وموقد حثّي وطاولة طعام زجاجية',
  'Computergegenereerde L-vormige keuken in hoogglans grijs met een hoge koelkast, een inductiekookplaat en een glazen eettafel',
  'Wizualizacja komputerowa kuchni w kształcie litery L w szarym połysku, z wysoką lodówką, płytą indukcyjną i szklanym stołem',
  'Datagenerert L-formet kjøkken i grå høyglans med høyt kjøleskap, induksjonstopp og spisebord i glass',
  'Datorgenererat L-format kök i grå högglans med högt kylskåp, induktionshäll och matbord i glas')
a('.media.items[3].caption', 'La cocina en L', 'La cuisine en L', 'Die L-Küche', 'Г-образная кухня', 'المطبخ على شكل حرف L',
  'De L-vormige keuken', 'Kuchnia w kształcie litery L', 'Det L-formede kjøkkenet', 'Det L-formade köket')
a('.media.items[5].alt',
  'Baño generado por ordenador con paredes efecto mármol, ducha a ras de suelo con mampara de cristal y mueble de lavabo en madera',
  'Salle de bains en image de synthèse aux murs effet marbre, avec une douche à l’italienne derrière une paroi vitrée et un meuble vasque en bois',
  'Computergeneriertes Bad mit Wänden in Marmoroptik, bodengleicher Dusche hinter Glaswand und Waschtischunterschrank mit Holzfront',
  'Компьютерная визуализация ванной со стенами под мрамор, душем без поддона за стеклянной перегородкой и тумбой с деревянными фасадами',
  'حمّام مُنشأ بالحاسوب بجدران بتأثير الرخام، ودُش مفتوح خلف حاجز زجاجي، وخزانة مغسلة بواجهة خشبية',
  'Computergegenereerde badkamer met wanden in marmerlook, een inloopdouche achter een glazen wand en een badmeubel met houten front',
  'Wizualizacja komputerowa łazienki ze ścianami imitującymi marmur, prysznicem typu walk-in za szklaną ścianką i szafką pod umywalkę z drewnianym frontem',
  'Datagenerert bad med vegger i marmoreffekt, walk-in-dusj bak en glassvegg og et servantskap med trefront',
  'Datorgenererat badrum med väggar i marmoreffekt, en walk-in-dusch bakom en glasvägg och ett tvättställsskåp med träfront')
a('.media.items[6].alt',
  'Baño generado por ordenador con una pared revestida efecto madera, mueble de lavabo blanco y ducha a ras de suelo',
  'Salle de bains en image de synthèse avec un mur en carrelage effet bois, un meuble vasque blanc et une douche à l’italienne',
  'Computergeneriertes Bad mit einer Wand in Holzoptik-Fliesen, weißem Waschtischunterschrank und bodengleicher Dusche',
  'Компьютерная визуализация ванной со стеной в плитке под дерево, белой тумбой под раковину и душем без поддона',
  'حمّام مُنشأ بالحاسوب بجدار مكسو ببلاط بتأثير الخشب، وخزانة مغسلة بيضاء، ودُش مفتوح',
  'Computergegenereerde badkamer met een wand van tegels in houtlook, een wit badmeubel en een inloopdouche',
  'Wizualizacja komputerowa łazienki ze ścianą wyłożoną płytkami imitującymi drewno, białą szafką pod umywalkę i prysznicem typu walk-in',
  'Datagenerert bad med en vegg i fliser med treeffekt, hvitt servantskap og walk-in-dusj',
  'Datorgenererat badrum med en vägg i kakel med träeffekt, ett vitt tvättställsskåp och en walk-in-dusch')
a('.media.items[7].alt',
  'Fotografía de la piscina comunitaria existente, con palmeras, tumbonas y los edificios de la fase anterior al fondo',
  'Photographie de la piscine commune existante, avec des palmiers, des transats et les immeubles de la phase précédente en arrière-plan',
  'Foto des bestehenden Gemeinschaftspools mit Palmen, Sonnenliegen und den Wohngebäuden des früheren Bauabschnitts dahinter',
  'Фотография существующего общего бассейна с пальмами, шезлонгами и домами предыдущей очереди на заднем плане',
  'صورة فوتوغرافية للمسبح المشترك القائم، مع أشجار النخيل وكراسي التشمس ومباني المرحلة السابقة في الخلفية',
  'Foto van het bestaande gemeenschappelijke zwembad, met palmbomen, ligbedden en de appartementsgebouwen van de eerdere fase erachter',
  'Zdjęcie istniejącego wspólnego basenu z palmami, leżakami i budynkami wcześniejszego etapu w tle',
  'Fotografi av det eksisterende fellesbassenget, med palmer, solsenger og boligbyggene fra det tidligere byggetrinnet bak',
  'Fotografi av den befintliga gemensamma poolen, med palmer, solstolar och bostadshusen från den tidigare etappen i bakgrunden')
a('.media.items[7].caption', 'La piscina comunitaria existente', 'La piscine commune existante', 'Der bestehende Gemeinschaftspool',
  'Существующий общий бассейн', 'المسبح المشترك القائم', 'Het bestaande gemeenschappelijke zwembad', 'Istniejący wspólny basen',
  'Det eksisterende fellesbassenget', 'Den befintliga gemensamma poolen')
a('.media.items[8].alt',
  'Fotografía de un gimnasio con máquina de musculación, bicicletas estáticas, espalderas y paredes de espejo',
  'Photographie d’une salle de sport avec un appareil de musculation, des vélos d’appartement, un espalier et des murs en miroir',
  'Foto eines Fitnessraums mit Kraftstation, Heimtrainern, Sprossenwand und Spiegelwänden',
  'Фотография тренажёрного зала с силовым тренажёром, велотренажёрами, шведской стенкой и зеркальными стенами',
  'صورة فوتوغرافية لصالة رياضية فيها جهاز لتمارين القوة ودراجات ثابتة وعارضة حائط وجدران مرايا',
  'Foto van een fitnessruimte met een krachtstation, hometrainers, een wandrek en spiegelwanden',
  'Zdjęcie siłowni z atlasem, rowerkami stacjonarnymi, drabinką gimnastyczną i lustrzanymi ścianami',
  'Fotografi av et treningsrom med styrkeapparat, trimsykler, ribbevegg og speilvegger',
  'Fotografi av ett gym med styrkemaskin, motionscyklar, ribbstol och speglade väggar')
for _u, _es, _ru, _ar, _sv, _no in (('C', 'Ático C', 'Пентхаус C', 'بنتهاوس C', 'Takvåning C', 'Toppleilighet C'),
                                     ('F', 'Ático F', 'Пентхаус F', 'بنتهاوس F', 'Takvåning F', 'Toppleilighet F')):
    i = 9 if _u == 'C' else 10
    a(f'.media.items[{i}].alt',
      f'Plano del {_es}, con la vivienda y su terraza cubierta a la izquierda y el solárium de la cubierta a la derecha',
      f'Plan du penthouse {_u}, avec le logement et sa terrasse couverte à gauche et le solarium sur le toit à droite',
      f'Grundriss von Penthouse {_u}, links die Wohnung mit überdachter Terrasse, rechts das Dachsolarium',
      f'Планировка пентхауса {_u}: слева квартира с крытой террасой, справа солярий на крыше',
      f'مخطط {_ar}، مع المسكن وتراسه المسقوف على اليسار والسولاريوم على السطح على اليمين',
      f'Plattegrond van penthouse {_u}, met de woning en het overdekte terras links en het solarium op het dak rechts',
      f'Rzut penthouse’u {_u}: po lewej mieszkanie z zadaszonym tarasem, po prawej solarium na dachu',
      f'Plantegning av {_no.lower()}, med boligen og den overbygde terrassen til venstre og solterrassen på taket til høyre',
      f'Planritning av {_sv.lower()}, med bostaden och den överbyggda terrassen till vänster och solterrassen på taket till höger')
    a(f'.media.items[{i}].caption', f'Plano del {_es}', f'Plan du penthouse {_u}', f'Grundriss Penthouse {_u}', f'Планировка пентхауса {_u}',
      f'مخطط {_ar}', f'Plattegrond penthouse {_u}', f'Rzut penthouse’u {_u}', f'Plantegning, {_no.lower()}', f'Planritning, {_sv.lower()}')
a('.media.items[11].alt',
  'Plano del Ático G, con una gran terraza cubierta que rodea el salón',
  'Plan du penthouse G, avec une grande terrasse couverte autour du séjour',
  'Grundriss von Penthouse G mit großer überdachter Terrasse rund um den Wohnbereich',
  'Планировка пентхауса G с большой крытой террасой вокруг гостиной',
  'مخطط بنتهاوس G، مع تراس مسقوف كبير يحيط بغرفة المعيشة',
  'Plattegrond van penthouse G, met een groot overdekt terras rond de woonkamer',
  'Rzut penthouse’u G z dużym zadaszonym tarasem wokół salonu',
  'Plantegning av toppleilighet G, med en stor overbygd terrasse rundt stuen',
  'Planritning av takvåning G, med en stor överbyggd terrass runt vardagsrummet')
a('.media.items[11].caption', 'Plano del Ático G', 'Plan du penthouse G', 'Grundriss Penthouse G', 'Планировка пентхауса G',
  'مخطط بنتهاوس G', 'Plattegrond penthouse G', 'Rzut penthouse’u G', 'Plantegning, toppleilighet G', 'Planritning, takvåning G')

# ---- overview, why ---------------------------------------------------------------------------------

a('.overview.headlineHtml', 'Quince viviendas, <em>tres áticos disponibles</em>', 'Quinze logements, <em>trois penthouses disponibles</em>',
  'Fünfzehn Wohnungen, <em>drei Penthäuser verfügbar</em>', 'Пятнадцать квартир, <em>три пентхауса в продаже</em>',
  'خمسة عشر مسكنًا، <em>ثلاثة بنتهاوس متاحة</em>', 'Vijftien woningen, <em>drie penthouses beschikbaar</em>',
  'Piętnaście mieszkań, <em>trzy penthouse’y dostępne</em>', 'Femten boliger, <em>tre toppleiligheter tilgjengelige</em>',
  'Femton bostäder, <em>tre takvåningar tillgängliga</em>')
a('.overview.copy[0]',
  'Lentisco Residences es un edificio nuevo de 15 viviendas de dos dormitorios y dos baños en Los Pacos, Fuengirola, construido como segunda fase de un residencial consolidado. Según el folleto, la piscina, el gimnasio, la sauna, la lavandería y el garaje de la fase anterior ya existen, y todas las viviendas del edificio nuevo tienen terraza.',
  'Lentisco Residences est un immeuble neuf de 15 logements de deux chambres et deux salles de bains à Los Pacos, Fuengirola, construit comme deuxième phase d’une résidence établie. Selon la brochure, la piscine, la salle de sport, le sauna, la laverie et le garage de la phase précédente existent déjà, et tous les logements du nouvel immeuble ont une terrasse.',
  'Lentisco Residences ist ein neues Gebäude mit 15 Wohnungen mit zwei Schlafzimmern und zwei Bädern in Los Pacos, Fuengirola, errichtet als zweiter Bauabschnitt einer bestehenden Anlage. Laut Broschüre sind Pool, Fitnessraum, Sauna, Waschküche und Garage des früheren Abschnitts bereits vorhanden, und jede Wohnung im neuen Gebäude hat eine Terrasse.',
  'Lentisco Residences — новый дом на 15 квартир с двумя спальнями и двумя ванными комнатами в Лос-Пакос, Фуэнхирола, построенный как вторая очередь сложившегося комплекса. По данным буклета, бассейн, тренажёрный зал, сауна, прачечная и гараж предыдущей очереди уже существуют, а у каждой квартиры нового дома есть терраса.',
  'Lentisco Residences مبنى جديد من 15 مسكنًا بغرفتي نوم وحمّامين في لوس باكوس، فوينخيرولا، يُشيَّد كمرحلة ثانية من مجمع قائم. ووفقًا للكتيّب، فإن المسبح والصالة الرياضية والساونا والمغسلة والمرآب التابعة للمرحلة السابقة موجودة بالفعل، ولكل مسكن في المبنى الجديد تراس.',
  'Lentisco Residences is een nieuw gebouw met 15 woningen met twee slaapkamers en twee badkamers in Los Pacos, Fuengirola, gebouwd als tweede fase van een bestaand complex. Volgens de brochure zijn het zwembad, de fitnessruimte, de sauna, de wasruimte en de garage van de eerdere fase er al, en heeft elke woning in het nieuwe gebouw een terras.',
  'Lentisco Residences to nowy budynek z 15 mieszkaniami z dwiema sypialniami i dwiema łazienkami w Los Pacos w Fuengiroli, wznoszony jako drugi etap istniejącego osiedla. Według broszury basen, siłownia, sauna, pralnia i garaż wcześniejszego etapu już istnieją, a każde mieszkanie w nowym budynku ma taras.',
  'Lentisco Residences er et nytt bygg med 15 boliger med to soverom og to bad i Los Pacos, Fuengirola, oppført som andre byggetrinn i et etablert anlegg. Ifølge brosjyren finnes bassenget, treningsrommet, badstuen, vaskerommet og garasjen fra det tidligere byggetrinnet allerede, og alle boligene i det nye bygget har terrasse.',
  'Lentisco Residences är en ny byggnad med 15 bostäder med två sovrum och två badrum i Los Pacos, Fuengirola, uppförd som andra etappen i ett etablerat område. Enligt broschyren finns poolen, gymmet, bastun, tvättstugan och garaget från den tidigare etappen redan, och alla bostäder i den nya byggnaden har terrass.')
a('.overview.copy[1]',
  'La lista de precios del {D5.11.2026} muestra 11 de las 15 viviendas como vendidas y una como reservada. Las tres que quedan son los áticos de la última planta: los Áticos C y F, con solárium privado en la cubierta de {N96.72} y {N104.96} {U}, y el Ático G, con una terraza cubierta de {N46.65} {U}, de {E363000} a {E460000} antes de IVA.',
  'La liste de prix du {D5.11.2026} indique 11 des 15 logements comme vendus et un comme réservé. Les trois restants sont les penthouses du dernier étage : les penthouses C et F, avec un solarium privé sur le toit de {N96.72} et {N104.96} {U}, et le penthouse G, avec une terrasse couverte de {N46.65} {U}, de {E363000} à {E460000} hors TVA.',
  'Die Preisliste vom {D5.11.2026} weist 11 der 15 Wohnungen als verkauft und eine als reserviert aus. Die drei verbleibenden sind die Penthäuser im obersten Geschoss: Penthouse C und F mit privatem Dachsolarium von {N96.72} und {N104.96} {U} und Penthouse G mit einer überdachten Terrasse von {N46.65} {U}, von {E363000} bis {E460000} zuzüglich MwSt.',
  'В прайс-листе от {D5.11.2026} 11 из 15 квартир отмечены как проданные и одна как забронированная. Оставшиеся три — пентхаусы на верхнем этаже: пентхаусы C и F с собственным солярием на крыше {N96.72} и {N104.96} {U} и пентхаус G с крытой террасой {N46.65} {U}, от {E363000} до {E460000} без учёта НДС.',
  'تُظهر قائمة الأسعار المؤرخة {D5.11.2026} أن 11 من المساكن الخمسة عشر مبيعة وواحدًا محجوز. والثلاثة المتبقية هي البنتهاوس في الطابق الأخير: البنتهاوس C وF مع سولاريوم خاص على السطح مساحته {N96.72} و{N104.96} {U}، والبنتهاوس G مع تراس مسقوف مساحته {N46.65} {U}، من {E363000} إلى {E460000} قبل ضريبة القيمة المضافة.',
  'De prijslijst van {D5.11.2026} toont 11 van de 15 woningen als verkocht en één als gereserveerd. De drie die overblijven zijn de penthouses op de bovenste verdieping: penthouse C en F met een eigen solarium op het dak van {N96.72} en {N104.96} {U}, en penthouse G met een overdekt terras van {N46.65} {U}, van {E363000} tot {E460000} exclusief btw.',
  'Cennik z {D5.11.2026} pokazuje 11 z 15 mieszkań jako sprzedane i jedno jako zarezerwowane. Pozostałe trzy to penthouse’y na najwyższym piętrze: penthouse’y C i F z prywatnym solarium na dachu o powierzchni {N96.72} i {N104.96} {U} oraz penthouse G z zadaszonym tarasem o powierzchni {N46.65} {U}, od {E363000} do {E460000} bez VAT.',
  'Prislisten datert {D5.11.2026} viser 11 av de 15 boligene som solgt og én som reservert. De tre som gjenstår, er toppleilighetene i øverste etasje: toppleilighet C og F med egen solterrasse på taket på {N96.72} og {N104.96} {U}, og toppleilighet G med en overbygd terrasse på {N46.65} {U}, fra {E363000} til {E460000} før mva.',
  'Prislistan daterad {D5.11.2026} visar 11 av de 15 bostäderna som sålda och en som reserverad. De tre som återstår är takvåningarna på översta planet: takvåning C och F med egen solterrass på taket på {N96.72} och {N104.96} {U}, och takvåning G med en överbyggd terrass på {N46.65} {U}, från {E363000} till {E460000} före IVA (spansk moms).')
a('.overview.metrics[0][0]', 'Esta fase', 'Cette phase', 'Dieser Bauabschnitt', 'Эта очередь', 'هذه المرحلة', 'Deze fase', 'Ten etap',
  'Dette byggetrinnet', 'Denna etapp')
a('.overview.metrics[1][1]', '3 áticos', '3 penthouses', '3 Penthäuser', '3 пентхауса', '3 بنتهاوس', '3 penthouses', '3 penthouse’y',
  '3 toppleiligheter', '3 takvåningar')
a('.overview.metrics[3][1]', 'Septiembre 2027', 'Septembre 2027', 'September 2027', 'Сентябрь 2027', 'سبتمبر 2027', 'September 2027',
  'Wrzesień 2027', 'September 2027', 'September 2027')
a('.why.copy',
  'Áticos nuevos con mucho espacio exterior en una zona residencial de Fuengirola, a 2 km del mar, con las instalaciones comunes ya construidas.',
  'Des penthouses neufs avec beaucoup d’espace extérieur dans un quartier résidentiel de Fuengirola, à 2 km de la mer, avec des équipements communs déjà construits.',
  'Neue Penthäuser mit viel Außenfläche in einem Wohnviertel von Fuengirola, 2 km vom Meer, mit bereits gebauten Gemeinschaftseinrichtungen.',
  'Новые пентхаусы с большим открытым пространством в жилом районе Фуэнхиролы, в 2 км от моря, с уже построенной общей инфраструктурой.',
  'بنتهاوس جديدة بمساحات خارجية واسعة في حي سكني من فوينخيرولا، على بُعد 2 كم من البحر، مع مرافق مشتركة مبنية بالفعل.',
  'Nieuwe penthouses met veel buitenruimte in een woonwijk van Fuengirola, op 2 km van zee, met de gemeenschappelijke voorzieningen al gebouwd.',
  'Nowe penthouse’y z dużą przestrzenią na zewnątrz w dzielnicy mieszkaniowej Fuengiroli, 2 km od morza, z już zbudowanymi częściami wspólnymi.',
  'Nye toppleiligheter med mye uteareal i et boligområde i Fuengirola, 2 km fra sjøen, med fellesanleggene allerede bygget.',
  'Nya takvåningar med mycket utomhusyta i ett bostadsområde i Fuengirola, 2 km från havet, med de gemensamma anläggningarna redan byggda.')
a('.why.points[0][1]',
  'Compradores que buscan una vivienda nueva de dos dormitorios en la última planta en Fuengirola, con solárium en la cubierta o una gran terraza cubierta, para vivir o como segunda residencia.',
  'Les acheteurs qui souhaitent un logement neuf de deux chambres au dernier étage à Fuengirola, avec un solarium sur le toit ou une grande terrasse couverte, pour y vivre ou comme résidence secondaire.',
  'Käufer, die in Fuengirola eine neue Wohnung mit zwei Schlafzimmern im obersten Geschoss suchen, mit Dachsolarium oder großer überdachter Terrasse, zum Wohnen oder als Zweitwohnsitz.',
  'Покупателям, которым нужна новая квартира с двумя спальнями на верхнем этаже в Фуэнхироле, с солярием на крыше или большой крытой террасой, для жизни или как второй дом.',
  'المشترون الذين يريدون مسكنًا جديدًا بغرفتي نوم في الطابق الأخير في فوينخيرولا، مع سولاريوم على السطح أو تراس مسقوف كبير، للسكن أو كمنزل ثانٍ.',
  'Kopers die in Fuengirola een nieuwe woning met twee slaapkamers op de bovenste verdieping zoeken, met een solarium op het dak of een groot overdekt terras, om er te wonen of als tweede woning.',
  'Dla kupujących, którzy szukają w Fuengiroli nowego mieszkania z dwiema sypialniami na najwyższym piętrze, z solarium na dachu lub dużym zadaszonym tarasem, do zamieszkania lub jako drugi dom.',
  'Kjøpere som ønsker en ny bolig med to soverom i øverste etasje i Fuengirola, med solterrasse på taket eller en stor overbygd terrasse, til å bo i eller som feriebolig.',
  'Köpare som vill ha en ny bostad med två sovrum högst upp i Fuengirola, med solterrass på taket eller en stor överbyggd terrass, att bo i eller som fritidsbostad.')
a('.why.points[1][1]',
  'Los soláriums de los Áticos C y F son mayores que las viviendas que tienen debajo, y el Ático G tiene una terraza cubierta de {N46.65} {U}. La piscina, el gimnasio y la sauna pertenecen a la fase anterior y ya están en uso.',
  'Les solariums des penthouses C et F sont plus grands que les logements situés en dessous, et le penthouse G dispose d’une terrasse couverte de {N46.65} {U}. La piscine, la salle de sport et le sauna appartiennent à la phase précédente et sont déjà en service.',
  'Die Dachsolarien von Penthouse C und F sind größer als die Wohnungen darunter, und Penthouse G hat eine überdachte Terrasse von {N46.65} {U}. Pool, Fitnessraum und Sauna gehören zum früheren Bauabschnitt und sind bereits in Betrieb.',
  'Солярии пентхаусов C и F больше самих квартир под ними, а у пентхауса G крытая терраса {N46.65} {U}. Бассейн, тренажёрный зал и сауна относятся к предыдущей очереди и уже работают.',
  'سولاريوم البنتهاوس C وF أكبر من المسكن الذي تحته، وللبنتهاوس G تراس مسقوف مساحته {N46.65} {U}. أما المسبح والصالة الرياضية والساونا فتتبع المرحلة السابقة وهي قيد الاستخدام بالفعل.',
  'De dakterrassen van penthouse C en F zijn groter dan de woningen eronder, en penthouse G heeft een overdekt terras van {N46.65} {U}. Het zwembad, de fitnessruimte en de sauna horen bij de eerdere fase en zijn al in gebruik.',
  'Solaria penthouse’ów C i F są większe niż mieszkania pod nimi, a penthouse G ma zadaszony taras o powierzchni {N46.65} {U}. Basen, siłownia i sauna należą do wcześniejszego etapu i już działają.',
  'Solterrassene til toppleilighet C og F er større enn boligene under dem, og toppleilighet G har en overbygd terrasse på {N46.65} {U}. Bassenget, treningsrommet og badstuen hører til det tidligere byggetrinnet og er allerede i bruk.',
  'Solterrasserna till takvåning C och F är större än bostäderna under dem, och takvåning G har en överbyggd terrass på {N46.65} {U}. Poolen, gymmet och bastun hör till den tidigare etappen och används redan.')
a('.why.points[2][1]',
  'El folleto sitúa el edificio a 2 km del mar, unos ocho minutos en coche, y a cinco minutos a pie del centro de Los Pacos, con colegios, comercios, parques, instalaciones deportivas y una parada de autobús cerca.',
  'La brochure situe l’immeuble à 2 km de la mer, à environ huit minutes en voiture, et à cinq minutes à pied du centre de Los Pacos, avec des écoles, des commerces, des parcs, des équipements sportifs et un arrêt de bus à proximité.',
  'Laut Broschüre liegt das Gebäude 2 km vom Meer, etwa acht Autominuten, und fünf Gehminuten vom Zentrum von Los Pacos, mit Schulen, Geschäften, Parks, Sportanlagen und einer Bushaltestelle in der Nähe.',
  'По данным буклета, дом находится в 2 км от моря, примерно в восьми минутах на машине, и в пяти минутах пешком от центра Лос-Пакоса; рядом школы, магазины, парки, спортивные объекты и автобусная остановка.',
  'يضع الكتيّب المبنى على بُعد 2 كم من البحر، أي نحو ثماني دقائق بالسيارة، وعلى بُعد خمس دقائق سيرًا من وسط لوس باكوس، مع مدارس ومتاجر وحدائق ومرافق رياضية وموقف حافلات في الجوار.',
  'Volgens de brochure ligt het gebouw op 2 km van zee, ongeveer acht minuten met de auto, en op vijf minuten lopen van het centrum van Los Pacos, met scholen, winkels, parken, sportvoorzieningen en een bushalte in de buurt.',
  'Według broszury budynek leży 2 km od morza, około ośmiu minut samochodem, i pięć minut pieszo od centrum Los Pacos, w pobliżu szkół, sklepów, parków, obiektów sportowych i przystanku autobusowego.',
  'Brosjyren plasserer bygget 2 km fra sjøen, rundt åtte minutter med bil, og fem minutters gange fra sentrum av Los Pacos, med skoler, butikker, parker, idrettsanlegg og en bussholdeplass i nærheten.',
  'Broschyren placerar byggnaden 2 km från havet, cirka åtta minuter med bil, och fem minuters promenad från centrum av Los Pacos, med skolor, butiker, parker, idrottsanläggningar och en busshållplats i närheten.')
a('.why.points[3][1]',
  'Solo quedan los tres áticos de las 15 viviendas de esta fase. Los precios son antes de IVA, y confirmamos la lista vigente, la licencia y la fecha de entrega antes de cualquier reserva.',
  'Il ne reste que les trois penthouses sur les 15 logements de cette phase. Les prix sont hors TVA, et nous confirmons la liste en vigueur, le permis et la date de livraison avant toute réservation.',
  'Von den 15 Wohnungen dieses Bauabschnitts sind nur noch die drei Penthäuser frei. Die Preise verstehen sich zuzüglich MwSt., und wir bestätigen die aktuelle Liste, die Baugenehmigung und den Übergabetermin vor jeder Reservierung.',
  'Из 15 квартир этой очереди остались только три пентхауса. Цены указаны без НДС; мы подтверждаем актуальный список, разрешение на строительство и дату сдачи до любого бронирования.',
  'لم يتبقَّ من مساكن هذه المرحلة الخمسة عشر سوى البنتهاوس الثلاثة. والأسعار قبل ضريبة القيمة المضافة، ونؤكد القائمة الحالية والترخيص وموعد التسليم قبل أي حجز.',
  'Van de 15 woningen in deze fase zijn alleen de drie penthouses nog over. De prijzen zijn exclusief btw, en wij bevestigen de actuele lijst, de vergunning en de opleverdatum vóór elke reservering.',
  'Z 15 mieszkań tego etapu zostały tylko trzy penthouse’y. Ceny są podane bez VAT, a przed każdą rezerwacją potwierdzamy aktualny cennik, pozwolenie na budowę i termin oddania.',
  'Bare de tre toppleilighetene gjenstår av de 15 boligene i dette byggetrinnet. Prisene er før mva, og vi bekrefter gjeldende liste, byggetillatelsen og overleveringsdatoen før enhver reservasjon.',
  'Endast de tre takvåningarna återstår av de 15 bostäderna i denna etapp. Priserna är före IVA, och vi bekräftar den aktuella listan, bygglovet och tillträdesdagen före varje bokning.')

# ---- architecture, quality specification -----------------------------------------------------------

a('.architecture.headlineHtml', 'Balcones curvos, <em>una amplia cubierta blanca</em>', 'Balcons courbes, <em>un large toit blanc</em>',
  'Geschwungene Balkone, <em>ein tiefes weißes Dach</em>', 'Изогнутые балконы, <em>широкая белая крыша</em>',
  'شرفات منحنية، <em>وسقف أبيض عريض</em>', 'Gebogen balkons, <em>een diep wit dak</em>', 'Zaokrąglone balkony, <em>głęboki biały dach</em>',
  'Buede balkonger, <em>et dypt, hvitt tak</em>', 'Svängda balkonger, <em>ett djupt, vitt tak</em>')
a('.architecture.copy[0]',
  'En las imágenes, el edificio se eleva cinco plantas sobre la calle en una parcela en pendiente, con paredes terracota, balcones curvos blancos en todas las plantas y una amplia cubierta blanca sobre la planta de áticos. Las viviendas de planta baja se abren a jardines escalonados sobre un muro de contención ajardinado.',
  'Sur les images, l’immeuble s’élève sur cinq niveaux au-dessus de la rue, sur un terrain en pente, avec des murs couleur terre cuite, des balcons courbes blancs à chaque étage et un large toit blanc au-dessus du niveau des penthouses. Les logements du rez-de-chaussée s’ouvrent sur des jardins en terrasses au-dessus d’un mur de soutènement planté.',
  'In den Visualisierungen erhebt sich das Gebäude auf einem Hanggrundstück fünf Geschosse über der Straße, mit terrakottafarbenen Wänden, weißen geschwungenen Balkonen auf jeder Etage und einem tiefen weißen Dach über der Penthouse-Ebene. Die Erdgeschosswohnungen öffnen sich zu gestuften Gärten über einer bepflanzten Stützmauer.',
  'На визуализациях дом поднимается на пять этажей над улицей на участке со склоном: терракотовые стены, белые изогнутые балконы на каждом этаже и широкая белая крыша над уровнем пентхаусов. Квартиры первого этажа выходят в ступенчатые сады над озеленённой подпорной стеной.',
  'في الصور يرتفع المبنى خمسة طوابق فوق الشارع على قطعة أرض منحدرة، بجدران بلون التيراكوتا وشرفات بيضاء منحنية في كل طابق وسقف أبيض عريض فوق مستوى البنتهاوس. وتنفتح مساكن الطابق الأرضي على حدائق متدرجة فوق جدار استنادي مزروع.',
  'Op de beelden rijst het gebouw vijf verdiepingen boven de straat op een hellend perceel, met terracottakleurige muren, witte gebogen balkons op elke verdieping en een diep wit dak boven de penthouseverdieping. De benedenwoningen komen uit op getrapte tuinen boven een beplante keermuur.',
  'Na wizualizacjach budynek wznosi się na pięć kondygnacji nad ulicą na nachylonej działce, ze ścianami w kolorze terakoty, białymi zaokrąglonymi balkonami na każdym piętrze i głębokim białym dachem nad poziomem penthouse’ów. Mieszkania na parterze wychodzą na tarasowe ogrody nad obsadzonym zielenią murem oporowym.',
  'På bildene reiser bygget seg fem etasjer over gaten på en skrånende tomt, med terrakottafargede vegger, hvite, buede balkonger i hver etasje og et dypt, hvitt tak over toppleilighetsetasjen. Boligene på bakkeplan åpner seg mot terrasserte hager over en beplantet støttemur.',
  'På bilderna reser sig byggnaden fem våningar över gatan på en sluttande tomt, med terrakottafärgade väggar, vita, svängda balkonger på varje våning och ett djupt, vitt tak över takvåningsplanet. Bostäderna i markplan öppnar sig mot terrasserade trädgårdar ovanför en planterad stödmur.')
a('.architecture.copy[1]',
  'Los planos muestran cada ático con salón, comedor y cocina abiertos a una terraza cubierta. El Ático C accede a su solárium por una escalera de caracol desde la terraza, y el Ático F por una escalera junto a la entrada.',
  'Les plans montrent chaque penthouse avec un séjour, un espace repas et une cuisine ouverts sur une terrasse couverte. Le penthouse C accède à son solarium par un escalier en colimaçon depuis la terrasse, et le penthouse F par un escalier près de l’entrée.',
  'Die Grundrisse zeigen jedes Penthouse mit offenem Wohn-, Ess- und Küchenbereich zur überdachten Terrasse. Penthouse C erreicht sein Dachsolarium über eine Wendeltreppe von der Terrasse aus, Penthouse F über eine Treppe neben dem Eingang.',
  'На планах у каждого пентхауса гостиная, столовая и кухня открыты на крытую террасу. В пентхаусе C на солярий ведёт винтовая лестница с террасы, в пентхаусе F — лестница у входа.',
  'تُظهر المخططات كل بنتهاوس بغرفة معيشة ومنطقة طعام ومطبخ مفتوحة على تراس مسقوف. ويُصعَد إلى سولاريوم البنتهاوس C بدرج حلزوني من التراس، وإلى سولاريوم البنتهاوس F بدرج بجوار المدخل.',
  'De plattegronden tonen elk penthouse met een open woonkamer, eethoek en keuken aan een overdekt terras. Penthouse C bereikt zijn solarium via een wenteltrap vanaf het terras, penthouse F via een trap naast de entree.',
  'Rzuty pokazują każdy penthouse z otwartym salonem, jadalnią i kuchnią wychodzącymi na zadaszony taras. Do solarium penthouse’u C prowadzą kręcone schody z tarasu, a penthouse’u F schody przy wejściu.',
  'Plantegningene viser hver toppleilighet med åpen stue, spiseplass og kjøkken ut mot en overbygd terrasse. Toppleilighet C når solterrassen via en vindeltrapp fra terrassen, og toppleilighet F via en trapp ved inngangen.',
  'Planritningarna visar varje takvåning med öppet vardagsrum, matplats och kök ut mot en överbyggd terrass. Takvåning C når solterrassen via en spiraltrappa från terrassen, och takvåning F via en trappa vid entrén.')
a('.architecture.highlights[0][0]', 'Envolvente', 'Enveloppe', 'Gebäudehülle', 'Ограждающие конструкции', 'الغلاف الخارجي',
  'Gebouwschil', 'Przegrody zewnętrzne', 'Klimaskall', 'Klimatskal')
a('.architecture.highlights[0][1]',
  'Aislamiento térmico en la fachada y mejor impermeabilización de cubierta y suelos, para reducir las pérdidas de calor y el ruido.',
  'Isolation thermique de la façade et étanchéité renforcée du toit et des sols, pour limiter les pertes de chaleur et le bruit.',
  'Wärmedämmung der Fassade und verbesserte Abdichtung von Dach und Böden, um Wärmeverluste und Lärm zu verringern.',
  'Теплоизоляция фасада и улучшенная гидроизоляция кровли и полов для снижения теплопотерь и шума.',
  'عزل حراري في الواجهة وعزل محسّن للسقف والأرضيات ضد المياه، للحد من فقدان الحرارة والضوضاء.',
  'Thermische isolatie in de gevel en betere waterdichting van dak en vloeren, om warmteverlies en geluid te beperken.',
  'Izolacja termiczna elewacji oraz lepsza hydroizolacja dachu i podłóg, ograniczające straty ciepła i hałas.',
  'Varmeisolering i fasaden og forbedret tetting av tak og gulv, for å redusere varmetap og støy.',
  'Värmeisolering i fasaden och förbättrad tätning av tak och bjälklag, för att minska värmeförluster och buller.')
a('.architecture.highlights[1][1]',
  'Carpintería exterior con rotura de puente térmico y doble acristalamiento con cámara de aire deshidratado.',
  'Menuiseries extérieures à rupture de pont thermique et double vitrage avec lame d’air déshydraté.',
  'Außenfenster mit thermischer Trennung und Doppelverglasung mit entfeuchtetem Luftzwischenraum.',
  'Наружные оконные и дверные блоки с терморазрывом и двойным остеклением с камерой осушенного воздуха.',
  'نجارة خارجية بفاصل حراري وزجاج مزدوج مع حجرة هواء مجفف.',
  'Buitenschrijnwerk met thermische onderbreking en dubbele beglazing met een gedroogde luchtspouw.',
  'Stolarka zewnętrzna z przekładką termiczną i podwójnymi szybami z komorą osuszonego powietrza.',
  'Utvendige vinduer og dører med kuldebrobryter og doble glass med tørket luftspalte.',
  'Fönster och dörrar med köldbryggsbrytning och dubbla glas med torkad luftspalt.')
a('.architecture.highlights[2][0]', 'Ventilación', 'Ventilation', 'Lüftung', 'Вентиляция', 'التهوية', 'Ventilatie', 'Wentylacja',
  'Ventilasjon', 'Ventilation')
a('.architecture.highlights[2][1]',
  'Un sistema de ventilación de simple flujo que introduce aire fresco y extrae el aire viciado de forma continua.',
  'Une ventilation simple flux qui fait entrer l’air frais et évacue l’air vicié en continu.',
  'Eine Abluftanlage, die kontinuierlich Frischluft zuführt und verbrauchte Luft abführt.',
  'Однопоточная система вентиляции, которая непрерывно подаёт свежий воздух и удаляет отработанный.',
  'نظام تهوية أحادي التدفق يُدخل الهواء النقي ويُخرج الهواء الفاسد بشكل متواصل.',
  'Een enkelvoudig ventilatiesysteem dat continu verse lucht aanvoert en gebruikte lucht afvoert.',
  'Jednostrumieniowy system wentylacji, który stale doprowadza świeże powietrze i odprowadza zużyte.',
  'Et enkelt ventilasjonsanlegg som kontinuerlig tilfører frisk luft og trekker ut brukt luft.',
  'Ett frånluftssystem som kontinuerligt tar in frisk luft och för ut förbrukad luft.')
a('.architecture.highlights[3][1]',
  'Paneles fotovoltaicos en la cubierta para las zonas comunes, iluminación LED en las zonas comunes y agua caliente mediante bomba de calor por aerotermia.',
  'Panneaux photovoltaïques sur le toit pour les parties communes, éclairage LED dans les parties communes et eau chaude produite par une pompe à chaleur aérothermique.',
  'Photovoltaikmodule auf dem Dach für die Gemeinschaftsbereiche, LED-Beleuchtung in den Gemeinschaftsflächen und Warmwasser über eine Luft-Wasser-Wärmepumpe.',
  'Солнечные панели на крыше для мест общего пользования, светодиодное освещение в общих зонах и горячая вода от аэротермального теплового насоса.',
  'ألواح كهروضوئية على السطح للمناطق المشتركة، وإنارة LED في الأجزاء المشتركة، وماء ساخن بمضخة حرارية تعمل بالطاقة الهوائية.',
  'Zonnepanelen op het dak voor de gemeenschappelijke delen, ledverlichting in de gemeenschappelijke ruimtes en warm water via een lucht-waterwarmtepomp.',
  'Panele fotowoltaiczne na dachu dla części wspólnych, oświetlenie LED w częściach wspólnych i ciepła woda z powietrznej pompy ciepła.',
  'Solcellepaneler på taket for fellesarealene, LED-belysning i fellesarealene og varmtvann fra en luft-til-vann-varmepumpe.',
  'Solpaneler på taket för de gemensamma utrymmena, LED-belysning i allmänna utrymmen och varmvatten från en luft-vattenvärmepump.')
a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor, en español y en inglés, y el folleto. La memoria indica que los acabados pueden modificarse o sustituirse por otros de igual o superior calidad por decisiones técnicas, cambios de modelos de fabricación o de normativa. Para el segundo baño, la memoria en español y el folleto indican porcelánico efecto madera combinado con paredes en blanco, mientras que la versión inglesa repite el efecto mármol brillo del baño principal; mostramos la versión española y la confirmamos antes de la reserva.',
  'Source : le descriptif des prestations du promoteur, en espagnol et en anglais, et la brochure. Le descriptif précise que les finitions peuvent être modifiées ou remplacées par d’autres de qualité égale ou supérieure pour des raisons techniques, des changements de modèles des fabricants ou de réglementation. Pour la deuxième salle de bains, la version espagnole et la brochure indiquent un grès cérame effet bois associé à des murs blancs, tandis que la version anglaise reprend l’effet marbre brillant de la salle de bains principale ; nous présentons la version espagnole et la confirmons avant la réservation.',
  'Quelle: die Baubeschreibung des Bauträgers auf Spanisch und Englisch sowie die Broschüre. Laut Baubeschreibung können Ausstattungen aus technischen Gründen, wegen geänderter Herstellermodelle oder neuer Vorschriften geändert oder durch gleich- oder höherwertige ersetzt werden. Für das zweite Bad nennen die spanische Fassung und die Broschüre Feinsteinzeug in Holzoptik mit weißen Wänden, die englische Fassung dagegen die glänzende Marmoroptik des Hauptbads; wir zeigen die spanische Fassung und bestätigen sie vor der Reservierung.',
  'Источник: спецификация отделки застройщика на испанском и английском языках и буклет. В спецификации сказано, что отделка может быть изменена или заменена на равноценную или более качественную по техническим причинам, из-за смены моделей производителей или норм. Для второй ванной испанская версия и буклет указывают керамогранит под дерево в сочетании с белыми стенами, а английская версия повторяет глянцевый мрамор главной ванной; мы приводим испанскую версию и подтверждаем её до бронирования.',
  'المصدر: مواصفات الجودة الخاصة بالمطوّر باللغتين الإسبانية والإنجليزية، والكتيّب. وتنص المواصفات على أن التشطيبات قد تُعدَّل أو تُستبدل بأخرى مماثلة أو أعلى جودة لأسباب فنية أو بسبب تغيّر طرازات المصنّعين أو الأنظمة. وبالنسبة إلى الحمّام الثاني، تذكر النسخة الإسبانية والكتيّب بورسلان بتأثير الخشب مع جدران بيضاء، بينما تكرر النسخة الإنجليزية تأثير الرخام اللامع للحمّام الرئيسي؛ ونعرض النسخة الإسبانية ونؤكدها قبل الحجز.',
  'Bron: de kwaliteitsomschrijving van de ontwikkelaar, in het Spaans en het Engels, en de brochure. Daarin staat dat afwerkingen gewijzigd of vervangen kunnen worden door gelijkwaardige of betere om technische redenen, door gewijzigde modellen van fabrikanten of nieuwe regelgeving. Voor de tweede badkamer noemen de Spaanse versie en de brochure keramiek in houtlook met witte wanden, terwijl de Engelse versie de glanzende marmerlook van de hoofdbadkamer herhaalt; wij tonen de Spaanse versie en bevestigen die vóór de reservering.',
  'Źródło: specyfikacja wykończenia dewelopera w wersji hiszpańskiej i angielskiej oraz broszura. Według specyfikacji wykończenia mogą zostać zmienione lub zastąpione innymi o tej samej lub wyższej jakości z przyczyn technicznych, ze względu na zmianę modeli producentów lub przepisów. Dla drugiej łazienki wersja hiszpańska i broszura podają gres imitujący drewno w połączeniu z białymi ścianami, a wersja angielska powtarza połyskujący efekt marmuru z łazienki głównej; podajemy wersję hiszpańską i potwierdzamy ją przed rezerwacją.',
  'Kilde: utbyggerens kvalitetsbeskrivelse, på spansk og engelsk, og brosjyren. Beskrivelsen sier at overflater kan endres eller erstattes av andre av samme eller bedre kvalitet av tekniske grunner, ved endrede produsentmodeller eller nye forskrifter. For det andre badet oppgir den spanske versjonen og brosjyren porselensfliser med treeffekt kombinert med hvite vegger, mens den engelske versjonen gjentar hovedbadets blanke marmoreffekt; vi viser den spanske versjonen og bekrefter den før reservasjon.',
  'Källa: exploatörens kvalitetsbeskrivning, på spanska och engelska, samt broschyren. Beskrivningen anger att ytskikt kan ändras eller ersättas med andra av samma eller högre kvalitet av tekniska skäl, vid ändrade tillverkarmodeller eller nya regler. För det andra badrummet anger den spanska versionen och broschyren porslinskakel med träeffekt kombinerat med vita väggar, medan den engelska versionen upprepar huvudbadrummets blanka marmoreffekt; vi visar den spanska versionen och bekräftar den före bokning.')
a('.qualitySpecs.groups[0].items[0]',
  'Pavimento porcelánico en tono crema o gris a elegir, con acabado antideslizante en las terrazas.',
  'Sol en grès cérame au choix crème ou gris, avec une finition antidérapante sur les terrasses.',
  'Feinsteinzeugböden wahlweise in Creme oder Grau, mit rutschfester Oberfläche auf den Terrassen.',
  'Напольный керамогранит на выбор кремового или серого цвета, с противоскользящей отделкой на террасах.',
  'أرضيات من البورسلان باللون الكريمي أو الرمادي حسب الاختيار، مع تشطيب مانع للانزلاق على التراسات.',
  'Vloeren in keramische tegels naar keuze in crème of grijs, met een antislipafwerking op de terrassen.',
  'Podłogi z gresu porcelanowego w kolorze kremowym lub szarym do wyboru, z wykończeniem antypoślizgowym na tarasach.',
  'Gulv i porselensfliser i krem eller grått etter valg, med sklisikker finish på terrassene.',
  'Golv av porslinsklinker i kräm eller grått efter val, med halkfri yta på terrasserna.')
a('.qualitySpecs.groups[0].items[1]',
  'Porcelánico efecto mármol brillo en las paredes del baño principal, y porcelánico efecto madera combinado con paredes en blanco en el segundo baño.',
  'Grès cérame effet marbre brillant sur les murs de la salle de bains principale, et grès cérame effet bois associé à des murs blancs dans la deuxième salle de bains.',
  'Feinsteinzeug in glänzender Marmoroptik an den Wänden des Hauptbads und Feinsteinzeug in Holzoptik mit weißen Wänden im zweiten Bad.',
  'Глянцевый керамогранит под мрамор на стенах главной ванной и керамогранит под дерево в сочетании с белыми стенами во второй ванной.',
  'بورسلان بتأثير الرخام اللامع على جدران الحمّام الرئيسي، وبورسلان بتأثير الخشب مع جدران بيضاء في الحمّام الثاني.',
  'Keramiek in glanzende marmerlook op de wanden van de hoofdbadkamer, en keramiek in houtlook met witte wanden in de tweede badkamer.',
  'Gres z połyskującym efektem marmuru na ścianach łazienki głównej oraz gres imitujący drewno w połączeniu z białymi ścianami w drugiej łazience.',
  'Porselensfliser med blank marmoreffekt på veggene på hovedbadet, og porselensfliser med treeffekt kombinert med hvite vegger på det andre badet.',
  'Porslinskakel med blank marmoreffekt på väggarna i huvudbadrummet, och porslinskakel med träeffekt kombinerat med vita väggar i det andra badrummet.')
a('.qualitySpecs.groups[1].items[0]',
  'Muebles altos y bajos con acabado lacado, encimera y frontal entre muebles en material tipo cuarzo tecnológico, y fregadero de acero inoxidable bajo encimera.',
  'Meubles hauts et bas à finition laquée, plan de travail et crédence en matériau de type quartz reconstitué, et évier en inox sous plan.',
  'Ober- und Unterschränke mit Lackoberfläche, Arbeitsplatte und Rückwand aus quarzartigem Werkstoff und ein unterbautes Edelstahlspülbecken.',
  'Верхние и нижние шкафы с лакированными фасадами, столешница и фартук из материала типа инженерного кварца и мойка из нержавеющей стали под столешницей.',
  'خزائن علوية وسفلية بتشطيب مطلي بالورنيش، وسطح عمل وكسوة بين الخزائن من مادة شبيهة بالكوارتز الصناعي، وحوض من الفولاذ المقاوم للصدأ مثبت أسفل سطح العمل.',
  'Boven- en onderkasten met een gelakte afwerking, een werkblad en achterwand in een kwartsachtig composiet en een roestvrijstalen spoelbak onder het werkblad.',
  'Szafki górne i dolne z lakierowanym wykończeniem, blat i panel między szafkami z materiału typu konglomerat kwarcowy oraz zlewozmywak ze stali nierdzewnej montowany pod blatem.',
  'Over- og underskap med lakkert finish, benkeplate og vegg mellom skapene i et kvartslignende materiale, og en kum i rustfritt stål montert under benkeplaten.',
  'Över- och underskåp med lackad yta, bänkskiva och stänkskydd i ett kvartsliknande material samt en diskho i rostfritt stål monterad under bänkskivan.')
a('.qualitySpecs.groups[1].items[1]',
  'Placa de inducción, horno, microondas, lavavajillas y frigorífico, de primera marca nacional.',
  'Plaque à induction, four, micro-ondes, lave-vaisselle et réfrigérateur, d’une grande marque nationale.',
  'Induktionskochfeld, Backofen, Mikrowelle, Geschirrspüler und Kühlschrank einer führenden spanischen Marke.',
  'Индукционная варочная панель, духовой шкаф, микроволновая печь, посудомоечная машина и холодильник ведущей испанской марки.',
  'موقد حثّي وفرن وميكروويف وغسالة صحون وثلاجة من علامة تجارية إسبانية رائدة.',
  'Een inductiekookplaat, een oven, een magnetron, een vaatwasser en een koelkast van een toonaangevend Spaans merk.',
  'Płyta indukcyjna, piekarnik, mikrofalówka, zmywarka i lodówka czołowej hiszpańskiej marki.',
  'Induksjonstopp, stekeovn, mikrobølgeovn, oppvaskmaskin og kjøleskap fra et ledende spansk merke.',
  'Induktionshäll, ugn, mikrovågsugn, diskmaskin och kylskåp från ett ledande spanskt märke.')
a('.qualitySpecs.groups[2].items[0]',
  'Sanitarios de porcelana blanca de primera marca, platos de ducha de resina con textura natural y grifería monomando con sistema de ahorro de agua.',
  'Sanitaires en porcelaine blanche de grande marque, receveurs de douche en résine à texture naturelle et robinetterie mitigeur avec système d’économie d’eau.',
  'Sanitärobjekte aus weißem Porzellan einer Markenfirma, Duschtassen aus Mineralguss mit natürlicher Struktur und Einhebelmischer mit Wasserspartechnik.',
  'Сантехника из белого фарфора ведущей марки, душевые поддоны из смолы с натуральной текстурой и однорычажные смесители с водосберегающей системой.',
  'أدوات صحية من البورسلان الأبيض من علامة رائدة، وأحواض دُش من الراتنج بملمس طبيعي، وخلاطات أحادية الذراع بنظام لتوفير المياه.',
  'Sanitair in wit porselein van een topmerk, douchebakken van kunsthars met een natuurlijke textuur en eengreepsmengkranen met een waterbesparend systeem.',
  'Ceramika sanitarna z białej porcelany renomowanej marki, brodziki z żywicy o naturalnej fakturze i baterie jednouchwytowe z systemem oszczędzania wody.',
  'Sanitærutstyr i hvitt porselen fra et ledende merke, dusjkar i resin med naturlig struktur og ettgrepsbatterier med vannsparesystem.',
  'Sanitetsporslin i vitt porslin från ett ledande märke, duschgolv i resin med naturlig struktur och engreppsblandare med vattenbesparande system.')
a('.qualitySpecs.groups[2].items[1]',
  'Muebles de baño con cajones y lavabo integrado en blanco.',
  'Meubles de salle de bains à tiroirs avec vasque intégrée blanche.',
  'Badmöbel mit Schubladen und integriertem weißem Waschbecken.',
  'Мебель для ванной с ящиками и встроенной белой раковиной.',
  'خزائن حمّام بأدراج ومغسلة بيضاء مدمجة.',
  'Badmeubels met laden en een geïntegreerde witte wastafel.',
  'Meble łazienkowe z szufladami i zintegrowaną białą umywalką.',
  'Baderomsmøbler med skuffer og integrert hvit servant.',
  'Badrumsmöbler med lådor och integrerat vitt tvättställ.')
a('.qualitySpecs.groups[3].items[0]',
  'Climatización frío/calor por conductos con calificación energética A+.',
  'Climatisation chaud/froid par gaines avec un classement énergétique A+.',
  'Kanalgebundene Heizung und Kühlung mit Energieeffizienzklasse A+.',
  'Канальная система отопления и кондиционирования с энергетическим классом A+.',
  'تدفئة وتبريد عبر مجاري هواء بتصنيف طاقة A+.',
  'Verwarming en koeling via kanalen met energielabel A+.',
  'Kanałowe ogrzewanie i chłodzenie o klasie energetycznej A+.',
  'Kanalbasert varme og kjøling med energiklasse A+.',
  'Kanalburen värme och kyla med energiklass A+.')
a('.qualitySpecs.groups[3].items[1]',
  'Agua caliente sanitaria mediante bomba de calor por aerotermia con depósito acumulador.',
  'Eau chaude sanitaire par pompe à chaleur aérothermique avec ballon de stockage.',
  'Warmwasserbereitung über eine Luft-Wasser-Wärmepumpe mit Speicher.',
  'Горячее водоснабжение от аэротермального теплового насоса с накопительным баком.',
  'ماء ساخن صحي بمضخة حرارية تعمل بالطاقة الهوائية مع خزان تخزين.',
  'Warm tapwater via een lucht-waterwarmtepomp met boilervat.',
  'Ciepła woda użytkowa z powietrznej pompy ciepła z zasobnikiem.',
  'Varmtvann fra en luft-til-vann-varmepumpe med bereder.',
  'Varmvatten från en luft-vattenvärmepump med ackumulatortank.')
a('.qualitySpecs.groups[4].items[0]',
  'Preinstalación para cualquier tipo de instalación de televisión, por cable, satélite o digital, y mecanismos eléctricos en blanco.',
  'Préinstallation pour tout type de réception télévisée, par câble, satellite ou numérique, et appareillage électrique blanc.',
  'Vorbereitung für jede Art von Fernsehempfang über Kabel, Satellit oder digital sowie weiße Schalter und Steckdosen.',
  'Подготовка для любого вида телевидения — кабельного, спутникового или цифрового — и белые выключатели и розетки.',
  'تمديدات مسبقة لأي نوع من البث التلفزيوني، عبر الكابل أو الأقمار الصناعية أو الرقمي، ومفاتيح ومقابس كهربائية بيضاء.',
  'Voorbereiding voor elk type televisie-ontvangst, via kabel, satelliet of digitaal, en witte schakelaars en stopcontacten.',
  'Przygotowanie pod każdy rodzaj odbioru telewizji, kablowej, satelitarnej lub cyfrowej, oraz białe włączniki i gniazdka.',
  'Klargjort for alle typer TV-mottak, via kabel, satellitt eller digitalt, og hvite brytere og stikkontakter.',
  'Förberett för alla typer av tv-mottagning, via kabel, satellit eller digitalt, och vita strömbrytare och uttag.')

# ---- residences ------------------------------------------------------------------------------------

a('.residences.headlineHtml', 'Tres áticos, <em>dos dormitorios cada uno</em>', 'Trois penthouses, <em>deux chambres chacun</em>',
  'Drei Penthäuser, <em>je zwei Schlafzimmer</em>', 'Три пентхауса, <em>по две спальни</em>', 'ثلاثة بنتهاوس، <em>بغرفتي نوم لكل منها</em>',
  'Drie penthouses, <em>elk twee slaapkamers</em>', 'Trzy penthouse’y, <em>każdy z dwiema sypialniami</em>',
  'Tre toppleiligheter, <em>to soverom hver</em>', 'Tre takvåningar, <em>två sovrum vardera</em>')
a('.residences.copy',
  'Cada ático tiene dos dormitorios, dos baños, salón y cocina abiertos, lavadero y una terraza cubierta, y la lista de precios asigna a cada uno una plaza de garaje numerada.',
  'Chaque penthouse comprend deux chambres, deux salles de bains, un séjour avec cuisine ouverte, une buanderie et une terrasse couverte, et la liste de prix attribue à chacun une place de garage numérotée.',
  'Jedes Penthouse hat zwei Schlafzimmer, zwei Bäder, einen offenen Wohnbereich mit Küche, einen Hauswirtschaftsbereich und eine überdachte Terrasse, und die Preisliste weist jedem einen nummerierten Garagenstellplatz zu.',
  'В каждом пентхаусе две спальни, две ванные комнаты, гостиная, объединённая с кухней, постирочная и крытая терраса, а прайс-лист закрепляет за каждым пронумерованное место в гараже.',
  'لكل بنتهاوس غرفتا نوم وحمّامان وغرفة معيشة مفتوحة على المطبخ وركن للغسيل وتراس مسقوف، وتخصص قائمة الأسعار لكل منها موقفًا مرقّمًا في المرآب.',
  'Elk penthouse heeft twee slaapkamers, twee badkamers, een open woonkamer met keuken, een wasruimte en een overdekt terras, en de prijslijst wijst elk penthouse een genummerde garageplaats toe.',
  'Każdy penthouse ma dwie sypialnie, dwie łazienki, otwarty salon z kuchnią, pralnię i zadaszony taras, a cennik przypisuje każdemu ponumerowane miejsce w garażu.',
  'Hver toppleilighet har to soverom, to bad, åpen stue og kjøkken, vaskerom og en overbygd terrasse, og prislisten gir hver av dem en nummerert garasjeplass.',
  'Varje takvåning har två sovrum, två badrum, öppet vardagsrum och kök, tvättutrymme och en överbyggd terrass, och prislistan ger var och en en numrerad garageplats.')
a('.residences.items[0].name', 'Áticos C y F, con solárium en la cubierta', 'Penthouses C et F, avec solarium sur le toit',
  'Penthouse C und F, mit Dachsolarium', 'Пентхаусы C и F с солярием на крыше', 'البنتهاوس C وF، مع سولاريوم على السطح',
  'Penthouse C en F, met solarium op het dak', 'Penthouse’y C i F, z solarium na dachu', 'Toppleilighet C og F, med solterrasse på taket',
  'Takvåning C och F, med solterrass på taket')
a('.residences.items[0].points[0]',
  'Ático C: {N70.89} {U} construidos interiores y una terraza cubierta de {N12.68} {U}, con un solárium privado en la cubierta de {N96.72} {U} al que se sube por una escalera de caracol. Superficies útiles: salón y cocina {N26.35} {U}, dormitorios de {N12.72} y {N10.02} {U}, baños de {N4.06} y {N3.80} {U}.',
  'Penthouse C : {N70.89} {U} construits à l’intérieur et une terrasse couverte de {N12.68} {U}, avec un solarium privé sur le toit de {N96.72} {U} accessible par un escalier en colimaçon. Surfaces utiles : séjour et cuisine {N26.35} {U}, chambres de {N12.72} et {N10.02} {U}, salles de bains de {N4.06} et {N3.80} {U}.',
  'Penthouse C: {N70.89} {U} bebaute Innenfläche und eine überdachte Terrasse von {N12.68} {U}, dazu ein privates Dachsolarium von {N96.72} {U}, das über eine Wendeltreppe erreicht wird. Nutzflächen: Wohnbereich mit Küche {N26.35} {U}, Schlafzimmer mit {N12.72} und {N10.02} {U}, Bäder mit {N4.06} und {N3.80} {U}.',
  'Пентхаус C: {N70.89} {U} внутренней площади застройки и крытая терраса {N12.68} {U}, а также собственный солярий на крыше {N96.72} {U}, куда ведёт винтовая лестница. Полезная площадь: гостиная с кухней {N26.35} {U}, спальни {N12.72} и {N10.02} {U}, ванные {N4.06} и {N3.80} {U}.',
  'البنتهاوس C: {N70.89} {U} مساحة مبنية داخلية وتراس مسقوف مساحته {N12.68} {U}، مع سولاريوم خاص على السطح مساحته {N96.72} {U} يُصعد إليه بدرج حلزوني. المساحات الصافية: غرفة المعيشة والمطبخ {N26.35} {U}، وغرفتا نوم {N12.72} و{N10.02} {U}، وحمّامان {N4.06} و{N3.80} {U}.',
  'Penthouse C: {N70.89} {U} bebouwd binnen en een overdekt terras van {N12.68} {U}, met een eigen solarium op het dak van {N96.72} {U}, bereikbaar via een wenteltrap. Nuttige oppervlakten: woonkamer en keuken {N26.35} {U}, slaapkamers van {N12.72} en {N10.02} {U}, badkamers van {N4.06} en {N3.80} {U}.',
  'Penthouse C: {N70.89} {U} powierzchni zabudowy wewnątrz i zadaszony taras o powierzchni {N12.68} {U}, a do tego prywatne solarium na dachu o powierzchni {N96.72} {U}, na które prowadzą kręcone schody. Powierzchnie użytkowe: salon z kuchnią {N26.35} {U}, sypialnie {N12.72} i {N10.02} {U}, łazienki {N4.06} i {N3.80} {U}.',
  'Toppleilighet C: {N70.89} {U} bebygd innvendig areal og en overbygd terrasse på {N12.68} {U}, med egen solterrasse på taket på {N96.72} {U}, som nås via en vindeltrapp. Bruksarealer: stue og kjøkken {N26.35} {U}, soverom på {N12.72} og {N10.02} {U}, bad på {N4.06} og {N3.80} {U}.',
  'Takvåning C: {N70.89} {U} invändig byggyta och en överbyggd terrass på {N12.68} {U}, med egen solterrass på taket på {N96.72} {U}, som nås via en spiraltrappa. Nyttoytor: vardagsrum och kök {N26.35} {U}, sovrum på {N12.72} och {N10.02} {U}, badrum på {N4.06} och {N3.80} {U}.')
a('.residences.items[0].points[1]',
  'Ático F: {N85.89} {U} construidos interiores, una terraza cubierta de {N10.09} {U} y una descubierta de {N4.09} {U}, con un solárium privado en la cubierta de {N104.96} {U}. Superficies útiles: salón y cocina {N30.93} {U}, dormitorios de {N15.56} y {N11.22} {U}, baños de {N4.57} y {N3.80} {U}.',
  'Penthouse F : {N85.89} {U} construits à l’intérieur, une terrasse couverte de {N10.09} {U} et une terrasse découverte de {N4.09} {U}, avec un solarium privé sur le toit de {N104.96} {U}. Surfaces utiles : séjour et cuisine {N30.93} {U}, chambres de {N15.56} et {N11.22} {U}, salles de bains de {N4.57} et {N3.80} {U}.',
  'Penthouse F: {N85.89} {U} bebaute Innenfläche, eine überdachte Terrasse von {N10.09} {U} und eine offene von {N4.09} {U}, dazu ein privates Dachsolarium von {N104.96} {U}. Nutzflächen: Wohnbereich mit Küche {N30.93} {U}, Schlafzimmer mit {N15.56} und {N11.22} {U}, Bäder mit {N4.57} und {N3.80} {U}.',
  'Пентхаус F: {N85.89} {U} внутренней площади застройки, крытая терраса {N10.09} {U} и открытая {N4.09} {U}, а также собственный солярий на крыше {N104.96} {U}. Полезная площадь: гостиная с кухней {N30.93} {U}, спальни {N15.56} и {N11.22} {U}, ванные {N4.57} и {N3.80} {U}.',
  'البنتهاوس F: {N85.89} {U} مساحة مبنية داخلية، وتراس مسقوف مساحته {N10.09} {U} وتراس مكشوف مساحته {N4.09} {U}، مع سولاريوم خاص على السطح مساحته {N104.96} {U}. المساحات الصافية: غرفة المعيشة والمطبخ {N30.93} {U}، وغرفتا نوم {N15.56} و{N11.22} {U}، وحمّامان {N4.57} و{N3.80} {U}.',
  'Penthouse F: {N85.89} {U} bebouwd binnen, een overdekt terras van {N10.09} {U} en een onoverdekt terras van {N4.09} {U}, met een eigen solarium op het dak van {N104.96} {U}. Nuttige oppervlakten: woonkamer en keuken {N30.93} {U}, slaapkamers van {N15.56} en {N11.22} {U}, badkamers van {N4.57} en {N3.80} {U}.',
  'Penthouse F: {N85.89} {U} powierzchni zabudowy wewnątrz, zadaszony taras o powierzchni {N10.09} {U} i odkryty o powierzchni {N4.09} {U}, a do tego prywatne solarium na dachu o powierzchni {N104.96} {U}. Powierzchnie użytkowe: salon z kuchnią {N30.93} {U}, sypialnie {N15.56} i {N11.22} {U}, łazienki {N4.57} i {N3.80} {U}.',
  'Toppleilighet F: {N85.89} {U} bebygd innvendig areal, en overbygd terrasse på {N10.09} {U} og en åpen terrasse på {N4.09} {U}, med egen solterrasse på taket på {N104.96} {U}. Bruksarealer: stue og kjøkken {N30.93} {U}, soverom på {N15.56} og {N11.22} {U}, bad på {N4.57} og {N3.80} {U}.',
  'Takvåning F: {N85.89} {U} invändig byggyta, en överbyggd terrass på {N10.09} {U} och en öppen terrass på {N4.09} {U}, med egen solterrass på taket på {N104.96} {U}. Nyttoytor: vardagsrum och kök {N30.93} {U}, sovrum på {N15.56} och {N11.22} {U}, badrum på {N4.57} och {N3.80} {U}.')
a('.residences.items[0].points[2]',
  '{E363000} el Ático C y {E423000} el Ático F, antes de IVA.',
  '{E363000} pour le penthouse C et {E423000} pour le penthouse F, hors TVA.',
  '{E363000} für Penthouse C und {E423000} für Penthouse F, zuzüglich MwSt.',
  '{E363000} за пентхаус C и {E423000} за пентхаус F, без учёта НДС.',
  '{E363000} للبنتهاوس C و{E423000} للبنتهاوس F، قبل ضريبة القيمة المضافة.',
  '{E363000} voor penthouse C en {E423000} voor penthouse F, exclusief btw.',
  '{E363000} za penthouse C i {E423000} za penthouse F, bez VAT.',
  '{E363000} for toppleilighet C og {E423000} for toppleilighet F, før mva.',
  '{E363000} för takvåning C och {E423000} för takvåning F, före IVA.')
a('.residences.items[1].name', 'Ático G, con una gran terraza cubierta', 'Penthouse G, avec une grande terrasse couverte',
  'Penthouse G, mit großer überdachter Terrasse', 'Пентхаус G с большой крытой террасой', 'البنتهاوس G، مع تراس مسقوف كبير',
  'Penthouse G, met een groot overdekt terras', 'Penthouse G, z dużym zadaszonym tarasem', 'Toppleilighet G, med stor overbygd terrasse',
  'Takvåning G, med stor överbyggd terrass')
a('.residences.items[1].points[0]',
  '{N79.92} {U} construidos interiores, con una terraza cubierta de {N46.65} {U} y una descubierta de {N4.14} {U} a lo largo de dos lados del salón. No tiene solárium en la cubierta.',
  '{N79.92} {U} construits à l’intérieur, avec une terrasse couverte de {N46.65} {U} et une terrasse découverte de {N4.14} {U} sur deux côtés du séjour. Il n’a pas de solarium sur le toit.',
  '{N79.92} {U} bebaute Innenfläche, mit einer überdachten Terrasse von {N46.65} {U} und einer offenen von {N4.14} {U} an zwei Seiten des Wohnbereichs. Ein Dachsolarium gibt es nicht.',
  '{N79.92} {U} внутренней площади застройки, крытая терраса {N46.65} {U} и открытая {N4.14} {U} вдоль двух сторон гостиной. Солярия на крыше нет.',
  '{N79.92} {U} مساحة مبنية داخلية، مع تراس مسقوف مساحته {N46.65} {U} وتراس مكشوف مساحته {N4.14} {U} على امتداد جانبين من غرفة المعيشة. ولا يوجد سولاريوم على السطح.',
  '{N79.92} {U} bebouwd binnen, met een overdekt terras van {N46.65} {U} en een onoverdekt terras van {N4.14} {U} langs twee zijden van de woonkamer. Er is geen solarium op het dak.',
  '{N79.92} {U} powierzchni zabudowy wewnątrz, z zadaszonym tarasem o powierzchni {N46.65} {U} i odkrytym o powierzchni {N4.14} {U} wzdłuż dwóch boków salonu. Nie ma solarium na dachu.',
  '{N79.92} {U} bebygd innvendig areal, med en overbygd terrasse på {N46.65} {U} og en åpen terrasse på {N4.14} {U} langs to sider av stuen. Den har ingen solterrasse på taket.',
  '{N79.92} {U} invändig byggyta, med en överbyggd terrass på {N46.65} {U} och en öppen terrass på {N4.14} {U} längs två sidor av vardagsrummet. Den har ingen solterrass på taket.')
a('.residences.items[1].points[1]',
  'Superficies útiles: salón y cocina {N33.95} {U}, dormitorios de {N12.72} y {N10.15} {U}, baños de {N4.60} y {N3.80} {U}.',
  'Surfaces utiles : séjour et cuisine {N33.95} {U}, chambres de {N12.72} et {N10.15} {U}, salles de bains de {N4.60} et {N3.80} {U}.',
  'Nutzflächen: Wohnbereich mit Küche {N33.95} {U}, Schlafzimmer mit {N12.72} und {N10.15} {U}, Bäder mit {N4.60} und {N3.80} {U}.',
  'Полезная площадь: гостиная с кухней {N33.95} {U}, спальни {N12.72} и {N10.15} {U}, ванные {N4.60} и {N3.80} {U}.',
  'المساحات الصافية: غرفة المعيشة والمطبخ {N33.95} {U}، وغرفتا نوم {N12.72} و{N10.15} {U}، وحمّامان {N4.60} و{N3.80} {U}.',
  'Nuttige oppervlakten: woonkamer en keuken {N33.95} {U}, slaapkamers van {N12.72} en {N10.15} {U}, badkamers van {N4.60} en {N3.80} {U}.',
  'Powierzchnie użytkowe: salon z kuchnią {N33.95} {U}, sypialnie {N12.72} i {N10.15} {U}, łazienki {N4.60} i {N3.80} {U}.',
  'Bruksarealer: stue og kjøkken {N33.95} {U}, soverom på {N12.72} og {N10.15} {U}, bad på {N4.60} og {N3.80} {U}.',
  'Nyttoytor: vardagsrum och kök {N33.95} {U}, sovrum på {N12.72} och {N10.15} {U}, badrum på {N4.60} och {N3.80} {U}.')
a('.residences.items[1].points[2]',
  '{E460000}, antes de IVA.', '{E460000}, hors TVA.', '{E460000}, zuzüglich MwSt.', '{E460000}, без учёта НДС.',
  '{E460000}، قبل ضريبة القيمة المضافة.', '{E460000}, exclusief btw.', '{E460000}, bez VAT.', '{E460000}, før mva.', '{E460000}, före IVA.')

# ---- lifestyle, location ---------------------------------------------------------------------------

a('.lifestyle.headlineHtml', 'Una última planta, <em>con las instalaciones ya abiertas</em>', 'Un dernier étage, <em>avec des équipements déjà ouverts</em>',
  'Ganz oben, <em>mit bereits geöffneten Einrichtungen</em>', 'Верхний этаж — <em>и инфраструктура уже работает</em>',
  'طابق أخير، <em>مع مرافق مفتوحة بالفعل</em>', 'De bovenste verdieping, <em>met de voorzieningen al open</em>',
  'Ostatnie piętro, <em>a części wspólne już działają</em>', 'Øverste etasje, <em>med fellesanleggene allerede åpne</em>',
  'Högst upp, <em>med anläggningarna redan öppna</em>')
a('.lifestyle.copy',
  'El edificio nuevo se suma a un residencial consolidado, así que las instalaciones comunes están en uso antes de que se terminen los áticos.',
  'Le nouvel immeuble rejoint une résidence établie : les équipements communs sont donc en service avant l’achèvement des penthouses.',
  'Das neue Gebäude ergänzt eine bestehende Anlage, sodass die Gemeinschaftseinrichtungen schon vor Fertigstellung der Penthäuser genutzt werden.',
  'Новый дом присоединяется к сложившемуся комплексу, поэтому общая инфраструктура работает ещё до завершения пентхаусов.',
  'ينضم المبنى الجديد إلى مجمع قائم، لذا فإن المرافق المشتركة قيد الاستخدام قبل اكتمال البنتهاوس.',
  'Het nieuwe gebouw sluit aan bij een bestaand complex, dus de gemeenschappelijke voorzieningen zijn al in gebruik voordat de penthouses klaar zijn.',
  'Nowy budynek dołącza do istniejącego osiedla, więc części wspólne działają, zanim penthouse’y zostaną ukończone.',
  'Det nye bygget slutter seg til et etablert anlegg, så fellesanleggene er i bruk før toppleilighetene står ferdige.',
  'Den nya byggnaden ansluter till ett etablerat område, så de gemensamma anläggningarna används redan innan takvåningarna är klara.')
a('.lifestyle.panels[0][1]',
  'La piscina comunitaria de la fase anterior, en sus jardines con palmeras y tumbonas, tal como la muestra el folleto.',
  'La piscine commune de la phase précédente, dans ses jardins avec palmiers et transats, telle que la brochure la présente.',
  'Der Gemeinschaftspool des früheren Bauabschnitts in seinen Gärten mit Palmen und Sonnenliegen, wie ihn die Broschüre zeigt.',
  'Общий бассейн предыдущей очереди в саду с пальмами и шезлонгами — таким его показывает буклет.',
  'المسبح المشترك للمرحلة السابقة، في حدائقه بأشجار النخيل وكراسي التشمس، كما يعرضه الكتيّب.',
  'Het gemeenschappelijke zwembad van de eerdere fase, in de tuinen met palmbomen en ligbedden, zoals de brochure het toont.',
  'Wspólny basen wcześniejszego etapu, w ogrodach z palmami i leżakami, tak jak pokazuje go broszura.',
  'Fellesbassenget fra det tidligere byggetrinnet, i hagene med palmer og solsenger, slik brosjyren viser det.',
  'Den gemensamma poolen från den tidigare etappen, i trädgården med palmer och solstolar, så som broschyren visar den.')
a('.lifestyle.panels[1][1]',
  'Un gimnasio y una sauna en el residencial existente, con lavandería y garaje comunes.',
  'Une salle de sport et un sauna dans la résidence existante, avec une laverie et un garage communs.',
  'Ein Fitnessraum und eine Sauna in der bestehenden Anlage, dazu eine gemeinsame Waschküche und eine Garage.',
  'Тренажёрный зал и сауна в существующем комплексе, а также общая прачечная и гараж.',
  'صالة رياضية وساونا في المجمع القائم، مع مغسلة مشتركة ومرآب.',
  'Een fitnessruimte en een sauna in het bestaande complex, met een gemeenschappelijke wasruimte en een garage.',
  'Siłownia i sauna w istniejącym osiedlu oraz wspólna pralnia i garaż.',
  'Et treningsrom og en badstue i det eksisterende anlegget, med felles vaskerom og garasje.',
  'Ett gym och en bastu i det befintliga området, med gemensam tvättstuga och garage.')
a('.lifestyle.panels[2][1]',
  'Los Áticos C y F tienen cada uno un solárium privado en la cubierta de unos 100 {U}, mayor que la vivienda que tiene debajo.',
  'Les penthouses C et F disposent chacun d’un solarium privé sur le toit d’environ 100 {U}, plus grand que le logement situé en dessous.',
  'Penthouse C und F haben jeweils ein privates Dachsolarium von rund 100 {U}, größer als die Wohnung darunter.',
  'У пентхаусов C и F есть собственный солярий на крыше площадью около 100 {U} — больше самой квартиры под ним.',
  'لكل من البنتهاوس C وF سولاريوم خاص على السطح مساحته نحو 100 {U}، أكبر من المسكن الذي تحته.',
  'Penthouse C en F hebben elk een eigen solarium op het dak van ongeveer 100 {U}, groter dan de woning eronder.',
  'Penthouse’y C i F mają po prywatnym solarium na dachu o powierzchni około 100 {U}, większym niż mieszkanie pod nim.',
  'Toppleilighet C og F har hver sin egen solterrasse på taket på rundt 100 {U}, større enn boligen under.',
  'Takvåning C och F har var sin egen solterrass på taket på cirka 100 {U}, större än bostaden under.')
a('.lifestyle.panels[3][1]',
  'El folleto señala colegios, supermercados, parques e instalaciones deportivas alrededor del residencial, y una parada de la línea 4 de autobús.',
  'La brochure signale des écoles, des supermarchés, des parcs et des équipements sportifs autour de la résidence, ainsi qu’un arrêt de la ligne de bus 4.',
  'Die Broschüre verzeichnet Schulen, Supermärkte, Parks und Sportanlagen rund um die Anlage sowie eine Haltestelle der Buslinie 4.',
  'Буклет отмечает вокруг комплекса школы, супермаркеты, парки и спортивные объекты, а также остановку автобуса № 4.',
  'يحدد الكتيّب مدارس ومتاجر كبرى وحدائق ومرافق رياضية حول المجمع، وموقفًا لخط الحافلات رقم 4.',
  'De brochure toont scholen, supermarkten, parken en sportvoorzieningen rond het complex, en een halte van buslijn 4.',
  'Broszura wskazuje wokół osiedla szkoły, supermarkety, parki i obiekty sportowe oraz przystanek autobusu linii 4.',
  'Brosjyren viser skoler, dagligvarebutikker, parker og idrettsanlegg rundt anlegget, og en holdeplass for buss linje 4.',
  'Broschyren visar skolor, livsmedelsbutiker, parker och idrottsanläggningar runt området, och en hållplats för busslinje 4.')
a('.location.headlineHtml', 'Los Pacos, <em>Fuengirola</em>', 'Los Pacos, <em>Fuengirola</em>', 'Los Pacos, <em>Fuengirola</em>',
  'Лос-Пакос, <em>Фуэнхирола</em>', 'لوس باكوس، <em>فوينخيرولا</em>', 'Los Pacos, <em>Fuengirola</em>', 'Los Pacos, <em>Fuengirola</em>',
  'Los Pacos, <em>Fuengirola</em>', 'Los Pacos, <em>Fuengirola</em>')
a('.location.copy',
  'El edificio está en la calle María de las Mercedes, en la zona residencial de Los Pacos, en la ladera sobre Fuengirola. El folleto indica 2 km hasta el mar, unos ocho minutos en coche, y cinco minutos a pie hasta el centro de Los Pacos, y señala en su mapa colegios, un parque, pistas de pádel y la estación de Cercanías de Los Boliches. Indica 30 km hasta Marbella y 23 km hasta el aeropuerto de Málaga. El punto del mapa se ha situado a partir del plano de situación del folleto y es aproximado.',
  'L’immeuble se trouve calle María de las Mercedes, dans le quartier résidentiel de Los Pacos, sur la colline au-dessus de Fuengirola. La brochure indique 2 km jusqu’à la mer, environ huit minutes en voiture, et cinq minutes à pied jusqu’au centre de Los Pacos, et signale sur sa carte des écoles, un parc, des courts de padel et la gare de banlieue de Los Boliches. Elle indique 30 km jusqu’à Marbella et 23 km jusqu’à l’aéroport de Malaga. Le repère sur la carte est placé d’après le plan de situation de la brochure et reste approximatif.',
  'Das Gebäude liegt an der Calle María de las Mercedes im Wohngebiet Los Pacos am Hang oberhalb von Fuengirola. Die Broschüre nennt 2 km bis zum Meer, etwa acht Autominuten, und fünf Gehminuten bis ins Zentrum von Los Pacos und verzeichnet auf ihrer Karte Schulen, einen Park, Padelplätze und den Vorortbahnhof Los Boliches. Sie nennt 30 km bis Marbella und 23 km bis zum Flughafen Málaga. Die Markierung auf der Karte folgt dem Lageplan der Broschüre und ist ungefähr.',
  'Дом стоит на улице Мария-де-лас-Мерседес, в жилом районе Лос-Пакос на склоне над Фуэнхиролой. Буклет указывает 2 км до моря, примерно восемь минут на машине, и пять минут пешком до центра Лос-Пакоса, а на карте отмечает школы, парк, корты для падела и пригородную станцию Лос-Боличес. До Марбельи, по буклету, 30 км, до аэропорта Малаги — 23 км. Метка на карте поставлена по схеме расположения из буклета и приблизительна.',
  'يقع المبنى في شارع ماريا دي لاس ميرسيديس، في الحي السكني لوس باكوس على التلة المطلة على فوينخيرولا. ويذكر الكتيّب مسافة 2 كم إلى البحر، أي نحو ثماني دقائق بالسيارة، وخمس دقائق سيرًا إلى وسط لوس باكوس، ويحدد على خريطته مدارس وحديقة وملاعب بادل ومحطة قطار الضواحي في لوس بوليتشيس. ويذكر 30 كم إلى ماربيا و23 كم إلى مطار مالقة. وقد وُضعت العلامة على الخريطة استنادًا إلى مخطط الموقع في الكتيّب وهي تقريبية.',
  'Het gebouw staat aan de Calle María de las Mercedes, in de woonwijk Los Pacos op de heuvel boven Fuengirola. De brochure noemt 2 km tot de zee, ongeveer acht minuten met de auto, en vijf minuten lopen tot het centrum van Los Pacos, en toont op de kaart scholen, een park, padelbanen en het voorstadstation Los Boliches. Ze noemt 30 km tot Marbella en 23 km tot de luchthaven van Málaga. De markering op de kaart is geplaatst aan de hand van de situatieschets in de brochure en is bij benadering.',
  'Budynek stoi przy Calle María de las Mercedes, w dzielnicy mieszkaniowej Los Pacos na zboczu nad Fuengirolą. Broszura podaje 2 km do morza, około ośmiu minut samochodem, i pięć minut pieszo do centrum Los Pacos, a na mapie zaznacza szkoły, park, korty do padla i stację kolei podmiejskiej Los Boliches. Podaje 30 km do Marbelli i 23 km do lotniska w Maladze. Znacznik na mapie umieszczono według planu sytuacyjnego z broszury i jest przybliżony.',
  'Bygget ligger i Calle María de las Mercedes, i boligområdet Los Pacos i åssiden over Fuengirola. Brosjyren oppgir 2 km til sjøen, rundt åtte minutter med bil, og fem minutters gange til sentrum av Los Pacos, og viser på kartet skoler, en park, padelbaner og lokaltogstasjonen Los Boliches. Den oppgir 30 km til Marbella og 23 km til Málaga lufthavn. Kartnålen er plassert etter situasjonskartet i brosjyren og er omtrentlig.',
  'Byggnaden ligger på Calle María de las Mercedes, i bostadsområdet Los Pacos i sluttningen ovanför Fuengirola. Broschyren anger 2 km till havet, cirka åtta minuter med bil, och fem minuters promenad till centrum av Los Pacos, och visar på kartan skolor, en park, padelbanor och pendeltågsstationen Los Boliches. Den anger 30 km till Marbella och 23 km till Málagas flygplats. Kartnålen är placerad efter situationsplanen i broschyren och är ungefärlig.')
a('.location.distances[0][0]', 'El mar', 'La mer', 'Das Meer', 'Море', 'البحر', 'De zee', 'Morze', 'Sjøen', 'Havet')
a('.location.distances[1][1]', '23 km', '23 km', '23 km', '23 км', '23 كم', '23 km', '23 km', '23 km', '23 km')
a('.location.distances[2][1]', '30 km', '30 km', '30 km', '30 км', '30 كم', '30 km', '30 km', '30 km', '30 km')

# ---- investment, trust dossier ----------------------------------------------------------------------

a('.investment.copy',
  'La lista de precios da un precio para cada uno de los tres áticos, antes de IVA, y el calendario de pagos fija una reserva, un pago al contrato privado y el resto en la escritura.',
  'La liste de prix indique un prix pour chacun des trois penthouses, hors TVA, et l’échéancier prévoit une réservation, un paiement au contrat privé et le solde à l’acte authentique.',
  'Die Preisliste nennt für jedes der drei Penthäuser einen Preis zuzüglich MwSt., und der Zahlungsplan sieht eine Reservierung, eine Zahlung beim privaten Kaufvertrag und den Rest bei der Beurkundung vor.',
  'В прайс-листе указана цена каждого из трёх пентхаусов без НДС, а график платежей предусматривает бронирование, платёж при подписании предварительного договора и остаток при оформлении права собственности.',
  'تعطي قائمة الأسعار سعرًا لكل من البنتهاوس الثلاثة قبل ضريبة القيمة المضافة، ويحدد جدول الدفعات حجزًا ودفعة عند العقد الخاص والباقي عند سند الملكية.',
  'De prijslijst geeft een prijs voor elk van de drie penthouses, exclusief btw, en het betalingsschema voorziet in een reservering, een betaling bij de onderhandse overeenkomst en het restant bij de akte.',
  'Cennik podaje cenę każdego z trzech penthouse’ów bez VAT, a harmonogram płatności przewiduje rezerwację, wpłatę przy umowie przedwstępnej i resztę przy akcie notarialnym.',
  'Prislisten gir en pris for hver av de tre toppleilighetene, før mva, og betalingsplanen fastsetter en reservasjon, en innbetaling ved den private kontrakten og resten ved skjøtet.',
  'Prislistan anger ett pris för var och en av de tre takvåningarna, före IVA, och betalningsplanen fastställer en bokning, en betalning vid det privata avtalet och resten vid köpebrevet.')
a('.investment.cards[0][1]',
  'La lista de precios indica que los precios son netos y no incluyen IVA, impuesto de transmisiones ni otros cargos. Con el IVA actual del 10 por ciento para vivienda nueva, el ático de {E363000} queda en {E399300} y el de {E460000} en {E506000}, antes de actos jurídicos documentados, notaría y registro.',
  'La liste de prix précise que les prix sont nets et n’incluent ni la TVA, ni les droits de mutation, ni d’autres frais. Avec la TVA actuelle de 10 pour cent sur le logement neuf, le penthouse à {E363000} revient à {E399300} et celui à {E460000} à {E506000}, avant droits d’enregistrement, frais de notaire et de registre foncier.',
  'Laut Preisliste sind die Preise netto, ohne MwSt., Grunderwerbsteuer oder sonstige Abgaben. Mit der derzeitigen MwSt. von 10 Prozent auf Neubauwohnungen kostet das Penthouse für {E363000} dann {E399300} und das für {E460000} dann {E506000}, vor Stempelsteuer, Notar- und Grundbuchkosten.',
  'В прайс-листе указано, что цены нетто и не включают НДС, налог на передачу имущества и прочие сборы. С учётом действующего НДС 10 процентов на новое жильё пентхаус за {E363000} обойдётся в {E399300}, а за {E460000} — в {E506000}, без гербового сбора, нотариуса и регистрации.',
  'تنص قائمة الأسعار على أن الأسعار صافية ولا تشمل ضريبة القيمة المضافة ولا ضريبة نقل الملكية ولا رسومًا أخرى. ومع ضريبة القيمة المضافة الحالية البالغة 10 بالمئة على المساكن الجديدة، يصبح البنتهاوس بسعر {E363000} بمبلغ {E399300} والبنتهاوس بسعر {E460000} بمبلغ {E506000}، قبل رسم الدمغة ورسوم كاتب العدل والسجل العقاري.',
  'De prijslijst vermeldt dat de prijzen netto zijn, zonder btw, overdrachtsbelasting of andere kosten. Met de huidige btw van 10 procent op nieuwbouw komt het penthouse van {E363000} op {E399300} en dat van {E460000} op {E506000}, vóór zegelrecht, notaris- en kadasterkosten.',
  'Cennik podaje, że ceny są netto i nie obejmują VAT, podatku od przeniesienia własności ani innych opłat. Przy obecnym VAT w wysokości 10 procent na nowe mieszkania penthouse za {E363000} kosztuje {E399300}, a za {E460000} – {E506000}, przed opłatą skarbową, kosztami notariusza i rejestru.',
  'Prislisten sier at prisene er netto og ikke inkluderer mva, overdragelsesskatt eller andre kostnader. Med dagens mva på 10 prosent på nye boliger koster toppleiligheten til {E363000} {E399300} og den til {E460000} {E506000}, før dokumentavgift, notar- og tinglysingsgebyrer.',
  'Prislistan anger att priserna är netto och inte inkluderar IVA (spansk moms), överlåtelseskatt eller andra avgifter. Med dagens IVA på 10 procent på nybyggda bostäder kostar takvåningen för {E363000} {E399300} och den för {E460000} {E506000}, före stämpelskatt, notarie- och inskrivningsavgifter.')
a('.investment.cards[1][1]',
  '{E10000} para reservar; el 30 por ciento al contrato privado, que el calendario vincula a la licencia de obra; y el 70 por ciento en la escritura, con la licencia de primera ocupación. El calendario indica que a estas cantidades se añade el IVA.',
  '{E10000} pour réserver ; 30 pour cent au contrat privé, que l’échéancier lie au permis de construire ; et 70 pour cent à l’acte authentique, avec le certificat de première occupation. L’échéancier précise que la TVA s’ajoute à ces montants.',
  '{E10000} zur Reservierung; 30 Prozent beim privaten Kaufvertrag, den der Zahlungsplan an die Baugenehmigung knüpft; und 70 Prozent bei der Beurkundung, mit der Bezugsgenehmigung. Laut Zahlungsplan kommt zu diesen Beträgen die MwSt. hinzu.',
  '{E10000} при бронировании; 30 процентов при подписании предварительного договора, который график связывает с разрешением на строительство; и 70 процентов при оформлении права собственности, после получения разрешения на заселение. В графике сказано, что к этим суммам добавляется НДС.',
  '{E10000} للحجز؛ و30 بالمئة عند العقد الخاص الذي يربطه الجدول برخصة البناء؛ و70 بالمئة عند سند الملكية، مع رخصة الإشغال الأولى. ويذكر الجدول أن ضريبة القيمة المضافة تُضاف إلى هذه المبالغ.',
  '{E10000} om te reserveren; 30 procent bij de onderhandse overeenkomst, die het schema koppelt aan de bouwvergunning; en 70 procent bij de akte, met de bewoningsvergunning. Volgens het schema komt de btw bovenop deze bedragen.',
  '{E10000} przy rezerwacji; 30 procent przy umowie przedwstępnej, którą harmonogram wiąże z pozwoleniem na budowę; i 70 procent przy akcie notarialnym, po uzyskaniu pozwolenia na użytkowanie. Harmonogram podaje, że do tych kwot dolicza się VAT.',
  '{E10000} ved reservasjon; 30 prosent ved den private kontrakten, som planen knytter til byggetillatelsen; og 70 prosent ved skjøtet, med brukstillatelsen. Planen sier at mva kommer i tillegg til disse beløpene.',
  '{E10000} vid bokning; 30 procent vid det privata avtalet, som planen kopplar till bygglovet; och 70 procent vid köpebrevet, med inflyttningstillståndet. Planen anger att IVA tillkommer på dessa belopp.')
a('.investment.cards[2][0]', 'Plaza de garaje', 'Place de garage', 'Garagenstellplatz', 'Место в гараже', 'موقف في المرآب',
  'Garageplaats', 'Miejsce w garażu', 'Garasjeplass', 'Garageplats')
a('.investment.cards[2][1]',
  'La lista de precios asigna a cada ático una plaza de garaje numerada, y el folleto incluye aparcamiento con cada vivienda. Confirmamos que la plaza está incluida en el precio.',
  'La liste de prix attribue à chaque penthouse une place de garage numérotée, et la brochure mentionne un stationnement avec chaque logement. Nous confirmons que la place est comprise dans le prix.',
  'Die Preisliste weist jedem Penthouse einen nummerierten Garagenstellplatz zu, und die Broschüre nennt einen Parkplatz zu jeder Wohnung. Wir bestätigen, dass der Stellplatz im Preis enthalten ist.',
  'Прайс-лист закрепляет за каждым пентхаусом пронумерованное место в гараже, а буклет указывает парковку при каждой квартире. Мы подтверждаем, что место входит в цену.',
  'تخصص قائمة الأسعار لكل بنتهاوس موقفًا مرقّمًا في المرآب، ويذكر الكتيّب موقفًا مع كل مسكن. ونؤكد أن الموقف مشمول في السعر.',
  'De prijslijst wijst elk penthouse een genummerde garageplaats toe, en de brochure vermeldt parkeren bij elke woning. Wij bevestigen dat de plaats in de prijs is inbegrepen.',
  'Cennik przypisuje każdemu penthouse’owi ponumerowane miejsce w garażu, a broszura wymienia miejsce parkingowe przy każdym mieszkaniu. Potwierdzamy, że miejsce jest wliczone w cenę.',
  'Prislisten gir hver toppleilighet en nummerert garasjeplass, og brosjyren oppgir parkering til hver bolig. Vi bekrefter at plassen er inkludert i prisen.',
  'Prislistan ger varje takvåning en numrerad garageplats, och broschyren anger parkering till varje bostad. Vi bekräftar att platsen ingår i priset.')
a('.investment.cards[3][0]', 'Pagos antes de la entrega', 'Les paiements avant la livraison', 'Zahlungen vor der Fertigstellung',
  'Платежи до сдачи', 'الدفعات قبل التسليم', 'Betalingen vóór oplevering', 'Wpłaty przed oddaniem', 'Innbetalinger før ferdigstillelse',
  'Betalningar före tillträdet')
a('.investment.cards[3][1]',
  'El 30 por ciento se paga mucho antes de recibir las llaves. Ningún documento que tenemos indica cómo se garantizan los pagos anteriores a la entrega, por lo que pedimos el aval bancario o el seguro antes de que se mueva dinero.',
  'Trente pour cent sont versés bien avant la remise des clés. Aucun document en notre possession ne précise comment les paiements avant livraison sont garantis ; nous demandons donc la garantie bancaire ou l’assurance avant tout versement.',
  'Dreißig Prozent werden lange vor der Schlüsselübergabe gezahlt. Keines der uns vorliegenden Dokumente sagt, wie Zahlungen vor der Fertigstellung abgesichert sind; deshalb verlangen wir die Bankbürgschaft oder Versicherung, bevor Geld fließt.',
  'Тридцать процентов оплачиваются задолго до передачи ключей. Ни один из имеющихся у нас документов не говорит, как гарантируются платежи до сдачи, поэтому мы запрашиваем банковскую гарантию или страховку до перевода денег.',
  'تُدفع ثلاثون بالمئة قبل تسليم المفاتيح بوقت طويل. ولا تذكر أي وثيقة لدينا كيف تُضمن الدفعات السابقة للتسليم، لذا نطلب الضمان المصرفي أو التأمين قبل تحويل أي مبلغ.',
  'Dertig procent wordt betaald lang vóór de sleuteloverdracht. Geen enkel document dat wij hebben, zegt hoe betalingen vóór oplevering worden gegarandeerd, dus vragen wij de bankgarantie of verzekering voordat er geld wordt overgemaakt.',
  'Trzydzieści procent płaci się długo przed odbiorem kluczy. Żaden z posiadanych przez nas dokumentów nie mówi, jak zabezpieczone są wpłaty przed oddaniem budynku, dlatego przed jakimkolwiek przelewem prosimy o gwarancję bankową lub ubezpieczenie.',
  'Tretti prosent betales lenge før nøkkeloverleveringen. Ingen av dokumentene vi har, sier hvordan innbetalinger før ferdigstillelse er sikret, så vi ber om bankgaranti eller forsikring før penger overføres.',
  'Trettio procent betalas långt före nyckelöverlämningen. Inget av de dokument vi har anger hur betalningar före tillträdet är säkrade, så vi begär bankgaranti eller försäkring innan pengar förs över.')
a('.trustDossier.cards[0][0]', 'Licencia y fechas', 'Permis et dates', 'Genehmigung und Termine', 'Разрешение и сроки',
  'الترخيص والمواعيد', 'Vergunning en data', 'Pozwolenie i terminy', 'Tillatelse og datoer', 'Bygglov och datum')
a('.trustDossier.cards[0][1]',
  'El portal del promotor indica que la licencia de obra está concedida, que la construcción empezó en octubre de 2025 y que la entrega está prevista para septiembre de 2027. Pedimos la licencia y la fecha de entrega que figurará en el contrato.',
  'Le portail du promoteur indique que le permis de construire est accordé, que la construction a commencé en octobre 2025 et que la livraison est prévue pour septembre 2027. Nous demandons le permis et la date de livraison qui figurera au contrat.',
  'Das Portal des Bauträgers gibt an, dass die Baugenehmigung erteilt ist, der Bau im Oktober 2025 begonnen hat und die Fertigstellung für September 2027 geplant ist. Wir verlangen die Genehmigung und den Übergabetermin, der in den Vertrag kommt.',
  'На портале застройщика сказано, что разрешение на строительство получено, строительство началось в октябре 2025 года, а сдача запланирована на сентябрь 2027 года. Мы запрашиваем разрешение и дату сдачи, которая войдёт в договор.',
  'تذكر بوابة المطوّر أن رخصة البناء ممنوحة، وأن البناء بدأ في أكتوبر 2025، وأن الإنجاز مقرر في سبتمبر 2027. ونطلب الرخصة وموعد التسليم الذي سيُدرج في العقد.',
  'Het portaal van de ontwikkelaar vermeldt dat de bouwvergunning is verleend, dat de bouw in oktober 2025 is begonnen en dat de oplevering gepland is voor september 2027. Wij vragen de vergunning en de opleverdatum die in het contract komt.',
  'Portal dewelopera podaje, że pozwolenie na budowę zostało wydane, budowa ruszyła w październiku 2025 roku, a zakończenie zaplanowano na wrzesień 2027 roku. Prosimy o pozwolenie i termin oddania, który trafi do umowy.',
  'Utbyggerens portal oppgir at byggetillatelsen er gitt, at byggingen startet i oktober 2025 og at ferdigstillelse er planlagt til september 2027. Vi ber om tillatelsen og overleveringsdatoen som skal stå i kontrakten.',
  'Exploatörens portal anger att bygglovet är beviljat, att bygget startade i oktober 2025 och att färdigställandet är planerat till september 2027. Vi begär bygglovet och den tillträdesdag som skrivs in i avtalet.')
a('.trustDossier.cards[1][1]',
  'La lista de precios da superficies construidas y los planos añaden las útiles: {N60.90}, {N72.79} y {N68.58} {U} interiores para los Áticos C, F y G. En el plano del Ático C las superficies de las estancias suman {N60.36} {U}, no los {N60.90} {U} impresos como total. Los soláriums solo figuran en la lista de precios. Confirmamos qué cifras utiliza el contrato.',
  'La liste de prix donne les surfaces construites, et les plans ajoutent les surfaces utiles : {N60.90}, {N72.79} et {N68.58} {U} à l’intérieur pour les penthouses C, F et G. Sur le plan du penthouse C, les surfaces des pièces totalisent {N60.36} {U}, et non les {N60.90} {U} imprimés comme total. Les solariums ne figurent que sur la liste de prix. Nous confirmons les chiffres retenus par le contrat.',
  'Die Preisliste nennt bebaute Flächen, die Grundrisse ergänzen die Nutzflächen: {N60.90}, {N72.79} und {N68.58} {U} innen für Penthouse C, F und G. Auf dem Grundriss von Penthouse C ergeben die Raumflächen zusammen {N60.36} {U}, nicht die als Summe gedruckten {N60.90} {U}. Die Dachsolarien stehen nur in der Preisliste. Wir bestätigen, welche Zahlen der Vertrag verwendet.',
  'В прайс-листе даны площади застройки, а планы добавляют полезные площади: {N60.90}, {N72.79} и {N68.58} {U} внутри для пентхаусов C, F и G. На плане пентхауса C площади помещений в сумме дают {N60.36} {U}, а не напечатанные как итог {N60.90} {U}. Солярии указаны только в прайс-листе. Мы подтверждаем, какие цифры используются в договоре.',
  'تعطي قائمة الأسعار المساحات المبنية، وتضيف المخططات المساحات الصافية: {N60.90} و{N72.79} و{N68.58} {U} داخلية للبنتهاوس C وF وG. وعلى مخطط البنتهاوس C يبلغ مجموع مساحات الغرف {N60.36} {U}، لا {N60.90} {U} المطبوعة كمجموع. ولا يرد السولاريوم إلا في قائمة الأسعار. ونؤكد الأرقام التي يعتمدها العقد.',
  'De prijslijst geeft bebouwde oppervlakten en de plattegronden voegen de nuttige oppervlakten toe: {N60.90}, {N72.79} en {N68.58} {U} binnen voor penthouse C, F en G. Op de plattegrond van penthouse C tellen de ruimten op tot {N60.36} {U}, niet de {N60.90} {U} die als totaal is gedrukt. De solariums staan alleen op de prijslijst. Wij bevestigen welke cijfers het contract hanteert.',
  'Cennik podaje powierzchnie zabudowy, a rzuty dodają powierzchnie użytkowe: {N60.90}, {N72.79} i {N68.58} {U} wewnątrz dla penthouse’ów C, F i G. Na rzucie penthouse’u C powierzchnie pomieszczeń sumują się do {N60.36} {U}, a nie do {N60.90} {U} wydrukowanych jako suma. Solaria podaje tylko cennik. Potwierdzamy, które liczby przyjmuje umowa.',
  'Prislisten oppgir bebygd areal, og plantegningene legger til bruksarealene: {N60.90}, {N72.79} og {N68.58} {U} innvendig for toppleilighet C, F og G. På plantegningen for toppleilighet C blir romarealene til sammen {N60.36} {U}, ikke de {N60.90} {U} som er trykt som sum. Solterrassene står bare på prislisten. Vi bekrefter hvilke tall kontrakten bruker.',
  'Prislistan anger byggyta, och planritningarna lägger till nyttoytorna: {N60.90}, {N72.79} och {N68.58} {U} invändigt för takvåning C, F och G. På planritningen för takvåning C blir rumsytorna sammanlagt {N60.36} {U}, inte de {N60.90} {U} som är tryckta som summa. Solterrasserna finns bara i prislistan. Vi bekräftar vilka siffror avtalet använder.')
a('.trustDossier.cards[2][0]', 'Las instalaciones comunes', 'Les équipements communs', 'Die Gemeinschaftseinrichtungen',
  'Общая инфраструктура', 'المرافق المشتركة', 'De gemeenschappelijke voorzieningen', 'Części wspólne', 'Fellesanleggene',
  'De gemensamma anläggningarna')
a('.trustDossier.cards[2][1]',
  'La piscina, el gimnasio, la sauna, la lavandería y el garaje pertenecen a la fase anterior. Pedimos los estatutos y las cuotas de la comunidad, y cómo participa en ellas el edificio nuevo.',
  'La piscine, la salle de sport, le sauna, la laverie et le garage appartiennent à la phase précédente. Nous demandons le règlement et les charges de la copropriété, et la façon dont le nouvel immeuble les partage.',
  'Pool, Fitnessraum, Sauna, Waschküche und Garage gehören zum früheren Bauabschnitt. Wir verlangen die Gemeinschaftsordnung und die Hausgeldhöhe und klären, wie das neue Gebäude daran beteiligt ist.',
  'Бассейн, тренажёрный зал, сауна, прачечная и гараж относятся к предыдущей очереди. Мы запрашиваем устав и взносы сообщества собственников и выясняем, как новый дом участвует в их использовании.',
  'المسبح والصالة الرياضية والساونا والمغسلة والمرآب تتبع المرحلة السابقة. ونطلب نظام الملاك ورسومه، وكيف يتشارك المبنى الجديد هذه المرافق.',
  'Het zwembad, de fitnessruimte, de sauna, de wasruimte en de garage horen bij de eerdere fase. Wij vragen het reglement en de bijdragen van de vereniging van eigenaren op, en hoe het nieuwe gebouw daarin deelt.',
  'Basen, siłownia, sauna, pralnia i garaż należą do wcześniejszego etapu. Prosimy o regulamin i opłaty wspólnoty oraz o to, jak nowy budynek z nich korzysta.',
  'Bassenget, treningsrommet, badstuen, vaskerommet og garasjen hører til det tidligere byggetrinnet. Vi ber om sameiets vedtekter og felleskostnader, og hvordan det nye bygget deler dem.',
  'Poolen, gymmet, bastun, tvättstugan och garaget hör till den tidigare etappen. Vi begär föreningens stadgar och avgifter, och hur den nya byggnaden delar dem.')
a('.trustDossier.cards[3][1]',
  'Las vistas del edificio y de las estancias están generadas por ordenador y son aproximadas, y el mobiliario no está incluido. La piscina y el gimnasio son fotografías de las instalaciones existentes.',
  'Les vues de l’immeuble et des pièces sont des images de synthèse approximatives, et le mobilier n’est pas inclus. La piscine et la salle de sport sont des photographies des équipements existants.',
  'Die Ansichten des Gebäudes und der Räume sind computergeneriert und nur annähernd, Möbel sind nicht enthalten. Pool und Fitnessraum sind Fotos der bestehenden Einrichtungen.',
  'Виды дома и помещений — приблизительные компьютерные визуализации, мебель в стоимость не входит. Бассейн и тренажёрный зал — фотографии существующих объектов.',
  'مناظر المبنى والغرف مُنشأة بالحاسوب وتقريبية، والأثاث غير مشمول. أما المسبح والصالة الرياضية فهي صور فوتوغرافية للمرافق القائمة.',
  'De beelden van het gebouw en de kamers zijn computergegenereerd en bij benadering, en het meubilair is niet inbegrepen. Het zwembad en de fitnessruimte zijn foto’s van de bestaande voorzieningen.',
  'Widoki budynku i pomieszczeń to przybliżone wizualizacje komputerowe, a meble nie są wliczone. Basen i siłownia to zdjęcia istniejących obiektów.',
  'Bildene av bygget og rommene er datagenererte og omtrentlige, og møblene er ikke inkludert. Bassenget og treningsrommet er fotografier av de eksisterende anleggene.',
  'Bilderna av byggnaden och rummen är datorgenererade och ungefärliga, och möblerna ingår inte. Poolen och gymmet är fotografier av de befintliga anläggningarna.')

# ---- availability ------------------------------------------------------------------------------------

a('.availability.headlineHtml', '3 áticos <em>disponibles actualmente</em>', '3 penthouses <em>actuellement disponibles</em>',
  '3 Penthäuser <em>derzeit verfügbar</em>', '3 пентхауса <em>сейчас в продаже</em>', '3 بنتهاوس <em>متاحة حاليًا</em>',
  '3 penthouses <em>momenteel beschikbaar</em>', '3 penthouse’y <em>obecnie dostępne</em>', '3 toppleiligheter <em>tilgjengelige nå</em>',
  '3 takvåningar <em>tillgängliga nu</em>')
a('.availability.copy',
  'Disponibilidad y precios según la lista del {D5.11.2026}, confirmados antes de la reserva. La lista muestra 11 de las 15 viviendas como vendidas y una como reservada; los tres áticos siguientes están disponibles. Los precios son antes de IVA.',
  'Disponibilité et prix selon la liste du {D5.11.2026}, confirmés avant la réservation. La liste indique 11 des 15 logements comme vendus et un comme réservé ; les trois penthouses ci-dessous sont disponibles. Les prix sont hors TVA.',
  'Verfügbarkeit und Preise laut Liste vom {D5.11.2026}, vor der Reservierung bestätigt. Die Liste weist 11 der 15 Wohnungen als verkauft und eine als reserviert aus; die drei folgenden Penthäuser sind verfügbar. Die Preise verstehen sich zuzüglich MwSt.',
  'Наличие и цены по списку от {D5.11.2026}, подтверждаются перед бронированием. В списке 11 из 15 квартир отмечены как проданные и одна как забронированная; три пентхауса ниже доступны. Цены указаны без НДС.',
  'التوفر والأسعار وفق القائمة المؤرخة {D5.11.2026}، وتُؤكَّد قبل الحجز. تُظهر القائمة أن 11 من المساكن الخمسة عشر مبيعة وواحدًا محجوز؛ والبنتهاوس الثلاثة أدناه متاحة. والأسعار قبل ضريبة القيمة المضافة.',
  'Beschikbaarheid en prijzen volgens de lijst van {D5.11.2026}, bevestigd vóór reservering. De lijst toont 11 van de 15 woningen als verkocht en één als gereserveerd; de drie penthouses hieronder zijn beschikbaar. De prijzen zijn exclusief btw.',
  'Dostępność i ceny według cennika z {D5.11.2026}, potwierdzane przed rezerwacją. Cennik pokazuje 11 z 15 mieszkań jako sprzedane i jedno jako zarezerwowane; trzy poniższe penthouse’y są dostępne. Ceny są podane bez VAT.',
  'Tilgjengelighet og priser ifølge listen datert {D5.11.2026}, bekreftet før reservasjon. Listen viser 11 av de 15 boligene som solgt og én som reservert; de tre toppleilighetene nedenfor er tilgjengelige. Prisene er før mva.',
  'Tillgänglighet och priser enligt listan daterad {D5.11.2026}, bekräftade före bokning. Listan visar 11 av de 15 bostäderna som sålda och en som reserverad; de tre takvåningarna nedan är tillgängliga. Priserna är före IVA (spansk moms).')
a('.availability.sourceNote',
  'Los precios, las superficies construidas, las terrazas, los soláriums y las plazas de garaje están transcritos de la lista de precios del promotor del {D5.11.2026}. Recoge las 15 viviendas de esta fase: 11 vendidas, una reservada y tres disponibles. Indica que los precios son netos y no incluyen IVA, impuesto de transmisiones ni otros cargos, y que la lista es solo informativa y no forma parte de ningún contrato. Las superficies de la tabla son la superficie construida interior, las terrazas cubiertas y descubiertas juntas y, en C y F, el solárium de la cubierta. Las superficies útiles y de las estancias proceden del plano del promotor de cada ático. Cada ático figura con una plaza de garaje numerada; la lista no dice si está incluida en el precio.',
  'Les prix, surfaces construites, terrasses, solariums et places de garage sont repris de la liste de prix du promoteur du {D5.11.2026}. Elle recense les 15 logements de cette phase : 11 vendus, un réservé et trois disponibles. Elle précise que les prix sont nets et n’incluent ni la TVA, ni les droits de mutation, ni d’autres frais, et que la liste est purement informative et ne fait partie d’aucun contrat. Les surfaces du tableau sont la surface construite intérieure, les terrasses couvertes et découvertes réunies et, pour C et F, le solarium sur le toit. Les surfaces utiles et celles des pièces proviennent du plan du promoteur pour chaque penthouse. Chaque penthouse figure avec une place de garage numérotée ; la liste ne dit pas si elle est comprise dans le prix.',
  'Preise, bebaute Flächen, Terrassen, Dachsolarien und Garagenstellplätze sind der Preisliste des Bauträgers vom {D5.11.2026} entnommen. Sie führt alle 15 Wohnungen dieses Bauabschnitts auf: 11 verkauft, eine reserviert und drei verfügbar. Laut Liste sind die Preise netto, ohne MwSt., Grunderwerbsteuer oder sonstige Abgaben, und die Liste dient nur der Information und ist nicht Vertragsbestandteil. Die Flächen in der Tabelle sind die bebaute Innenfläche, die überdachten und offenen Terrassen zusammen und bei C und F das Dachsolarium. Nutz- und Raumflächen stammen aus dem Grundriss des Bauträgers für jedes Penthouse. Jedes Penthouse ist mit einem nummerierten Garagenstellplatz aufgeführt; ob er im Preis enthalten ist, sagt die Liste nicht.',
  'Цены, площади застройки, террасы, солярии и места в гараже взяты из прайс-листа застройщика от {D5.11.2026}. В нём перечислены все 15 квартир этой очереди: 11 проданы, одна забронирована и три доступны. В нём указано, что цены нетто и не включают НДС, налог на передачу имущества и прочие сборы, а сам список носит информационный характер и не является частью договора. Площади в таблице — внутренняя площадь застройки, крытые и открытые террасы вместе и, для C и F, солярий на крыше. Полезная площадь и площади помещений взяты из плана застройщика для каждого пентхауса. Каждый пентхаус указан с пронумерованным местом в гараже; входит ли оно в цену, в списке не сказано.',
  'الأسعار والمساحات المبنية والتراسات والسولاريوم ومواقف المرآب منقولة من قائمة أسعار المطوّر المؤرخة {D5.11.2026}. وهي تشمل المساكن الخمسة عشر لهذه المرحلة: 11 مبيعة وواحد محجوز وثلاثة متاحة. وتنص على أن الأسعار صافية ولا تشمل ضريبة القيمة المضافة ولا ضريبة نقل الملكية ولا رسومًا أخرى، وأن القائمة لأغراض إعلامية فقط ولا تشكل جزءًا من أي عقد. والمساحات في الجدول هي المساحة المبنية الداخلية، والتراسات المسقوفة والمكشوفة معًا، والسولاريوم على السطح للبنتهاوس C وF. أما المساحات الصافية ومساحات الغرف فمأخوذة من مخطط المطوّر لكل بنتهاوس. ويرد كل بنتهاوس مع موقف مرقّم في المرآب؛ ولا تذكر القائمة ما إذا كان مشمولًا في السعر.',
  'Prijzen, bebouwde oppervlakten, terrassen, solariums en garageplaatsen zijn overgenomen uit de prijslijst van de ontwikkelaar van {D5.11.2026}. Die vermeldt alle 15 woningen van deze fase: 11 verkocht, één gereserveerd en drie beschikbaar. Volgens de lijst zijn de prijzen netto, zonder btw, overdrachtsbelasting of andere kosten, en is de lijst alleen informatief en geen onderdeel van een contract. De oppervlakten in de tabel zijn de bebouwde binnenoppervlakte, de overdekte en onoverdekte terrassen samen en, bij C en F, het solarium op het dak. De nuttige oppervlakten en die van de ruimten komen uit de plattegrond van de ontwikkelaar voor elk penthouse. Elk penthouse staat vermeld met een genummerde garageplaats; de lijst zegt niet of die in de prijs is inbegrepen.',
  'Ceny, powierzchnie zabudowy, tarasy, solaria i miejsca w garażu przepisano z cennika dewelopera z {D5.11.2026}. Obejmuje on wszystkie 15 mieszkań tego etapu: 11 sprzedanych, jedno zarezerwowane i trzy dostępne. Cennik podaje, że ceny są netto i nie obejmują VAT, podatku od przeniesienia własności ani innych opłat oraz że ma on charakter wyłącznie informacyjny i nie stanowi części umowy. Powierzchnie w tabeli to powierzchnia zabudowy wewnątrz, tarasy zadaszone i odkryte łącznie oraz, w przypadku C i F, solarium na dachu. Powierzchnie użytkowe i powierzchnie pomieszczeń pochodzą z rzutu dewelopera dla każdego penthouse’u. Każdy penthouse ma przypisane ponumerowane miejsce w garażu; cennik nie mówi, czy jest ono wliczone w cenę.',
  'Priser, bebygde arealer, terrasser, solterrasser og garasjeplasser er hentet fra utbyggerens prisliste datert {D5.11.2026}. Den omfatter alle de 15 boligene i dette byggetrinnet: 11 solgt, én reservert og tre tilgjengelige. Den sier at prisene er netto og ikke inkluderer mva, overdragelsesskatt eller andre kostnader, og at listen kun er veiledende og ikke er del av noen kontrakt. Arealene i tabellen er bebygd innvendig areal, de overbygde og åpne terrassene samlet og, for C og F, solterrassen på taket. Bruksarealer og romarealer er hentet fra utbyggerens plantegning for hver toppleilighet. Hver toppleilighet står oppført med en nummerert garasjeplass; listen sier ikke om den er inkludert i prisen.',
  'Priser, byggytor, terrasser, solterrasser och garageplatser är hämtade från exploatörens prislista daterad {D5.11.2026}. Den omfattar alla 15 bostäder i denna etapp: 11 sålda, en reserverad och tre tillgängliga. Den anger att priserna är netto och inte inkluderar IVA (spansk moms), överlåtelseskatt eller andra avgifter, och att listan endast är vägledande och inte ingår i något avtal. Ytorna i tabellen är den invändiga byggytan, de överbyggda och öppna terrasserna tillsammans och, för C och F, solterrassen på taket. Nyttoytor och rumsytor kommer från exploatörens planritning för varje takvåning. Varje takvåning står med en numrerad garageplats; listan säger inte om den ingår i priset.')
_SIZE = {
    0: ('70.89', '12.68', '96.72'),
    1: ('85.89', '14.18', '104.96'),
    2: ('79.92', '50.79', None),
}
_W = {  # built, terrace, solarium
    'es': ('{} {U} construidos', '{} {U} de terraza', '{} {U} de solárium'),
    'fr': ('{} {U} construits', '{} {U} de terrasse', '{} {U} de solarium'),
    'de': ('{} {U} bebaut', '{} {U} Terrasse', '{} {U} Dachsolarium'),
    'ru': ('{} {U} площадь застройки', '{} {U} терраса', '{} {U} солярий'),
    'ar': ('{} {U} مبنية', '{} {U} تراس', '{} {U} سولاريوم'),
    'nl': ('{} {U} bebouwd', '{} {U} terras', '{} {U} solarium'),
    'pl': ('{} {U} powierzchni zabudowy', '{} {U} tarasu', '{} {U} solarium'),
    'no': ('{} {U} bebygd areal', '{} {U} terrasse', '{} {U} solterrasse'),
    'sv': ('{} {U} byggyta', '{} {U} terrass', '{} {U} solterrass'),
}
for _i, (_b, _t, _s) in _SIZE.items():
    out = []
    for l in LOCS:
        sep = '، ' if l == 'ar' else ', '
        parts = [_W[l][0].replace('{}', '{N' + _b + '}'), _W[l][1].replace('{}', '{N' + _t + '}')]
        if _s:
            parts.append(_W[l][2].replace('{}', '{N' + _s + '}'))
        out.append(sep.join(parts))
    a(f'.availability.units[{_i}].size', *out)

# ---- construction timeline, payment terms ------------------------------------------------------------

a('.constructionTimeline.points[0].year', 'Octubre 2025', 'Octobre 2025', 'Oktober 2025', 'Октябрь 2025', 'أكتوبر 2025',
  'Oktober 2025', 'Październik 2025', 'Oktober 2025', 'Oktober 2025')
a('.constructionTimeline.points[0].label', 'Inicio de obra', 'Début des travaux', 'Baubeginn', 'Начало строительства', 'بدء البناء',
  'Start van de bouw', 'Rozpoczęcie budowy', 'Byggestart', 'Byggstart')
a('.constructionTimeline.points[2].year', 'Septiembre 2027', 'Septembre 2027', 'September 2027', 'Сентябрь 2027', 'سبتمبر 2027',
  'September 2027', 'Wrzesień 2027', 'September 2027', 'September 2027')
a('.constructionTimeline.points[2].label', 'Entrega prevista', 'Livraison prévue', 'Geplante Fertigstellung', 'Плановая сдача',
  'الإنجاز المقرر', 'Geplande oplevering', 'Planowane zakończenie', 'Planlagt ferdigstillelse', 'Planerat färdigställande')
a('.constructionTimeline.note',
  'El portal del promotor indica que la licencia de obra está concedida, que la construcción empezó en octubre de 2025 y que la entrega está prevista para septiembre de 2027. Ningún documento que tenemos fija una fecha de entrega contractual, por lo que Nueva Living la pide por escrito y que se incluya en el contrato.',
  'Le portail du promoteur indique que le permis de construire est accordé, que la construction a commencé en octobre 2025 et que la livraison est prévue pour septembre 2027. Aucun document en notre possession ne fixe de date de livraison contractuelle ; Nueva Living la demande donc par écrit et veille à ce qu’elle figure au contrat.',
  'Das Portal des Bauträgers gibt an, dass die Baugenehmigung erteilt ist, der Bau im Oktober 2025 begonnen hat und die Fertigstellung für September 2027 geplant ist. Keines der uns vorliegenden Dokumente nennt einen vertraglichen Übergabetermin; Nueva Living fordert ihn daher schriftlich an und lässt ihn in den Vertrag aufnehmen.',
  'На портале застройщика сказано, что разрешение на строительство получено, строительство началось в октябре 2025 года, а сдача запланирована на сентябрь 2027 года. Ни один из имеющихся у нас документов не фиксирует договорную дату сдачи, поэтому Nueva Living запрашивает её письменно и добивается её включения в договор.',
  'تذكر بوابة المطوّر أن رخصة البناء ممنوحة، وأن البناء بدأ في أكتوبر 2025، وأن الإنجاز مقرر في سبتمبر 2027. ولا تحدد أي وثيقة لدينا موعد تسليم تعاقديًا، لذا تطلبه Nueva Living كتابيًا وتحرص على إدراجه في العقد.',
  'Het portaal van de ontwikkelaar vermeldt dat de bouwvergunning is verleend, dat de bouw in oktober 2025 is begonnen en dat de oplevering gepland is voor september 2027. Geen enkel document dat wij hebben, legt een contractuele opleverdatum vast; Nueva Living vraagt die daarom schriftelijk op en laat die in het contract opnemen.',
  'Portal dewelopera podaje, że pozwolenie na budowę zostało wydane, budowa ruszyła w październiku 2025 roku, a zakończenie zaplanowano na wrzesień 2027 roku. Żaden z posiadanych przez nas dokumentów nie określa umownego terminu oddania, dlatego Nueva Living prosi o niego na piśmie i o wpisanie go do umowy.',
  'Utbyggerens portal oppgir at byggetillatelsen er gitt, at byggingen startet i oktober 2025 og at ferdigstillelse er planlagt til september 2027. Ingen av dokumentene vi har, fastsetter en kontraktsfestet overleveringsdato, så Nueva Living ber om den skriftlig og om at den tas inn i kontrakten.',
  'Exploatörens portal anger att bygglovet är beviljat, att bygget startade i oktober 2025 och att färdigställandet är planerat till september 2027. Inget av de dokument vi har anger ett avtalat tillträdesdatum, så Nueva Living begär det skriftligt och att det skrivs in i avtalet.')
a('.constructionTimeline.paymentTerms[0][1]', '{E10000} + IVA', '{E10000} + TVA', '{E10000} + MwSt.', '{E10000} + НДС',
  '{E10000} + ضريبة القيمة المضافة', '{E10000} + btw', '{E10000} + VAT', '{E10000} + mva', '{E10000} + IVA')
a('.constructionTimeline.paymentTerms[0][2]', 'Para reservar el ático', 'Pour réserver le penthouse', 'Zur Reservierung des Penthouses',
  'Для бронирования пентхауса', 'لحجز البنتهاوس', 'Om het penthouse te reserveren', 'Na rezerwację penthouse’u',
  'For å reservere toppleiligheten', 'För att boka takvåningen')
a('.constructionTimeline.paymentTerms[1][2]',
  'A la firma del contrato privado, que el calendario vincula a la licencia de obra',
  'À la signature du contrat privé, que l’échéancier lie au permis de construire',
  'Bei Unterzeichnung des privaten Kaufvertrags, den der Zahlungsplan an die Baugenehmigung knüpft',
  'При подписании предварительного договора, который график связывает с разрешением на строительство',
  'عند توقيع العقد الخاص الذي يربطه الجدول برخصة البناء',
  'Bij ondertekening van de onderhandse overeenkomst, die het schema koppelt aan de bouwvergunning',
  'Przy podpisaniu umowy przedwstępnej, którą harmonogram wiąże z pozwoleniem na budowę',
  'Ved signering av den private kontrakten, som planen knytter til byggetillatelsen',
  'Vid undertecknandet av det privata avtalet, som planen kopplar till bygglovet')
a('.constructionTimeline.paymentTerms[2][2]',
  'Con la licencia de primera ocupación y la firma de la escritura',
  'À l’obtention du certificat de première occupation et à la signature de l’acte authentique',
  'Mit der Bezugsgenehmigung und der Beurkundung',
  'После получения разрешения на заселение и подписания нотариального акта',
  'عند صدور رخصة الإشغال الأولى وتوقيع سند الملكية',
  'Bij de bewoningsvergunning en de ondertekening van de akte',
  'Po uzyskaniu pozwolenia na użytkowanie i podpisaniu aktu notarialnego',
  'Ved brukstillatelsen og signering av skjøtet',
  'Vid inflyttningstillståndet och undertecknandet av köpebrevet')
a('.constructionTimeline.paymentTermsNote',
  'Según el calendario de pagos del promotor, que indica que a todas las cantidades se añade el IVA. No dice si la reserva se descuenta del 30 por ciento ni cómo se garantizan los pagos anteriores a la entrega. Nueva Living confirma con usted las condiciones exactas antes de cualquier reserva.',
  'D’après l’échéancier du promoteur, qui précise que la TVA s’ajoute à tous les montants. Il ne dit pas si la réservation est déduite des 30 pour cent, ni comment les paiements avant livraison sont garantis. Nueva Living confirme avec vous les conditions exactes avant toute réservation.',
  'Nach dem Zahlungsplan des Bauträgers, laut dem zu allen Beträgen die MwSt. hinzukommt. Er sagt nicht, ob die Reservierung auf die 30 Prozent angerechnet wird oder wie Zahlungen vor der Fertigstellung abgesichert sind. Nueva Living bestätigt Ihnen die genauen Bedingungen vor jeder Reservierung.',
  'По графику платежей застройщика, где сказано, что ко всем суммам добавляется НДС. В нём не указано, засчитывается ли бронирование в 30 процентов и как гарантируются платежи до сдачи. Nueva Living подтверждает с вами точные условия до любого бронирования.',
  'وفق جدول دفعات المطوّر، الذي يذكر أن ضريبة القيمة المضافة تُضاف إلى جميع المبالغ. ولا يذكر ما إذا كان مبلغ الحجز يُخصم من نسبة 30 بالمئة، ولا كيف تُضمن الدفعات السابقة للتسليم. وتؤكد Nueva Living معكم الشروط الدقيقة قبل أي حجز.',
  'Volgens het betalingsschema van de ontwikkelaar, dat vermeldt dat de btw bij alle bedragen komt. Het zegt niet of de reservering van de 30 procent wordt afgetrokken, of hoe betalingen vóór oplevering worden gegarandeerd. Nueva Living bevestigt de exacte voorwaarden met u vóór elke reservering.',
  'Według harmonogramu płatności dewelopera, który podaje, że do wszystkich kwot dolicza się VAT. Nie mówi on, czy rezerwacja jest odliczana od 30 procent ani jak zabezpieczone są wpłaty przed oddaniem budynku. Nueva Living potwierdza z Państwem dokładne warunki przed każdą rezerwacją.',
  'Etter utbyggerens betalingsplan, som sier at mva kommer i tillegg til alle beløp. Den sier ikke om reservasjonen trekkes fra de 30 prosentene, eller hvordan innbetalinger før ferdigstillelse er sikret. Nueva Living bekrefter de nøyaktige vilkårene med deg før enhver reservasjon.',
  'Enligt exploatörens betalningsplan, som anger att IVA tillkommer på alla belopp. Den säger inte om bokningsavgiften dras av från de 30 procenten eller hur betalningar före tillträdet är säkrade. Nueva Living bekräftar de exakta villkoren med er före varje bokning.')

# ---- next steps, viewing, enquiry, FAQ, SEO ----------------------------------------------------------

a('.timeline.items[0][2]',
  'Los planos de los tres áticos, la memoria de calidades y la lista de precios.',
  'Les plans des trois penthouses, le descriptif des prestations et la liste de prix.',
  'Die Grundrisse der drei Penthäuser, die Baubeschreibung und die Preisliste.',
  'Планировки трёх пентхаусов, спецификация отделки и прайс-лист.',
  'مخططات البنتهاوس الثلاثة ومواصفات الجودة وقائمة الأسعار.',
  'De plattegronden van de drie penthouses, de kwaliteitsomschrijving en de prijslijst.',
  'Rzuty trzech penthouse’ów, specyfikacja wykończenia i cennik.',
  'Plantegningene til de tre toppleilighetene, kvalitetsbeskrivelsen og prislisten.',
  'Planritningarna för de tre takvåningarna, kvalitetsbeskrivningen och prislistan.')
a('.timeline.items[2][2]',
  'Vea con nosotros la parcela, la piscina y el gimnasio del residencial existente, y repasemos juntos los planos.',
  'Découvrez avec nous le terrain, la piscine et la salle de sport de la résidence existante, et parcourons ensemble les plans.',
  'Besichtigen Sie mit uns das Grundstück, den Pool und den Fitnessraum der bestehenden Anlage, und wir gehen die Grundrisse gemeinsam durch.',
  'Осмотрите вместе с нами участок, бассейн и тренажёрный зал существующего комплекса, и мы вместе разберём планировки.',
  'شاهدوا معنا الموقع والمسبح والصالة الرياضية في المجمع القائم، ونراجع المخططات معًا.',
  'Bekijk met ons het perceel, het zwembad en de fitnessruimte van het bestaande complex, en we nemen samen de plattegronden door.',
  'Zobaczą Państwo z nami działkę, basen i siłownię istniejącego osiedla, a rzuty omówimy wspólnie.',
  'Se tomten, bassenget og treningsrommet i det eksisterende anlegget sammen med oss, og gå gjennom plantegningene.',
  'Se tomten, poolen och gymmet i det befintliga området tillsammans med oss, och gå igenom planritningarna.')
a('.timeline.items[3][2]',
  'Una reserva de {E10000} más IVA y, después, el contrato privado de compraventa.',
  'Une réservation de {E10000} plus TVA, puis le contrat de vente privé.',
  'Eine Reservierung von {E10000} zuzüglich MwSt., danach der private Kaufvertrag.',
  'Бронирование за {E10000} плюс НДС, затем предварительный договор купли-продажи.',
  'حجز بمبلغ {E10000} زائد ضريبة القيمة المضافة، ثم عقد الشراء الخاص.',
  'Een reservering van {E10000} plus btw, daarna de onderhandse koopovereenkomst.',
  'Rezerwacja w wysokości {E10000} plus VAT, a następnie umowa przedwstępna.',
  'En reservasjon på {E10000} pluss mva, deretter den private kjøpekontrakten.',
  'En bokning på {E10000} plus IVA, därefter det privata köpeavtalet.')
a('.privateViewing.headlineHtml', 'Vea <em>la parcela y las instalaciones</em>', 'Découvrez <em>le terrain et les équipements</em>',
  'Sehen Sie <em>Grundstück und Einrichtungen</em>', 'Осмотрите <em>участок и инфраструктуру</em>', 'شاهدوا <em>الموقع والمرافق</em>',
  'Bekijk <em>het perceel en de voorzieningen</em>', 'Zobaczą Państwo <em>działkę i części wspólne</em>', 'Se <em>tomten og fellesanleggene</em>',
  'Se <em>tomten och anläggningarna</em>')
a('.privateViewing.copy',
  'El edificio está en construcción, pero la piscina, el gimnasio y la zona ya se pueden ver.',
  'L’immeuble est en construction, mais la piscine, la salle de sport et le quartier se visitent dès maintenant.',
  'Das Gebäude ist im Bau, aber Pool, Fitnessraum und Umgebung lassen sich schon jetzt besichtigen.',
  'Дом строится, но бассейн, тренажёрный зал и район можно посмотреть уже сейчас.',
  'المبنى قيد الإنشاء، لكن يمكن مشاهدة المسبح والصالة الرياضية والمنطقة الآن.',
  'Het gebouw is in aanbouw, maar het zwembad, de fitnessruimte en de omgeving zijn nu al te bekijken.',
  'Budynek jest w budowie, ale basen, siłownię i okolicę można zobaczyć już teraz.',
  'Bygget er under oppføring, men bassenget, treningsrommet og området kan ses allerede nå.',
  'Byggnaden är under uppförande, men poolen, gymmet och området kan ses redan nu.')
a('.privateViewing.insights[0][1]',
  'Vea la parcela, las vistas desde la ladera y las instalaciones comunes de la fase anterior.',
  'Découvrez le terrain, la vue depuis la colline et les équipements communs de la phase précédente.',
  'Sehen Sie das Grundstück, den Blick vom Hang und die Gemeinschaftseinrichtungen des früheren Bauabschnitts.',
  'Посмотрите участок, вид со склона и общую инфраструктуру предыдущей очереди.',
  'شاهدوا الموقع والإطلالة من التلة والمرافق المشتركة للمرحلة السابقة.',
  'Bekijk het perceel, het uitzicht vanaf de heuvel en de gemeenschappelijke voorzieningen van de eerdere fase.',
  'Działka, widok ze zbocza i części wspólne wcześniejszego etapu.',
  'Se tomten, utsikten fra åssiden og fellesanleggene fra det tidligere byggetrinnet.',
  'Se tomten, utsikten från sluttningen och de gemensamma anläggningarna från den tidigare etappen.')
a('.privateViewing.insights[1][1]',
  'Recorremos con usted el trayecto a la playa, al centro de Fuengirola y al aeropuerto, y lo cronometramos.',
  'Nous faisons avec vous le trajet jusqu’à la plage, au centre de Fuengirola et à l’aéroport, chronomètre en main.',
  'Wir fahren mit Ihnen zum Strand, ins Zentrum von Fuengirola und zum Flughafen und stoppen die Zeit.',
  'Мы вместе с вами проедем до пляжа, центра Фуэнхиролы и аэропорта и засечём время.',
  'نقود معكم إلى الشاطئ ووسط فوينخيرولا والمطار ونقيس الوقت.',
  'We rijden met u naar het strand, het centrum van Fuengirola en de luchthaven en klokken de tijd.',
  'Przejedziemy z Państwem na plażę, do centrum Fuengiroli i na lotnisko, mierząc czas.',
  'Vi kjører med deg til stranden, sentrum av Fuengirola og flyplassen og tar tiden.',
  'Vi kör med er till stranden, centrum av Fuengirola och flygplatsen och tar tid.')
a('.privateViewing.insights[2][1]',
  'Licencia, fecha de entrega, garantías y contrato, antes de firmar nada.',
  'Permis, date de livraison, garanties et contrat, avant toute signature.',
  'Genehmigung, Übergabetermin, Sicherheiten und Vertrag, bevor etwas unterschrieben wird.',
  'Разрешение, дата сдачи, гарантии и договор — до подписания чего-либо.',
  'الترخيص وموعد التسليم والضمانات والعقد، قبل توقيع أي شيء.',
  'Vergunning, opleverdatum, garanties en het contract, voordat er iets wordt getekend.',
  'Pozwolenie, termin oddania, gwarancje i umowa, zanim cokolwiek zostanie podpisane.',
  'Tillatelse, overleveringsdato, garantier og kontrakten, før noe signeres.',
  'Bygglov, tillträdesdag, garantier och avtalet, innan något skrivs under.')
a('.enquiry.headlineHtml', 'Pregunte por <em>Lentisco Residences</em>', 'Renseignez-vous sur <em>Lentisco Residences</em>',
  'Fragen Sie nach <em>Lentisco Residences</em>', 'Узнайте о <em>Lentisco Residences</em>', 'استفسر عن <em>Lentisco Residences</em>',
  'Vraag naar <em>Lentisco Residences</em>', 'Zapytanie o <em>Lentisco Residences</em>', 'Spør om <em>Lentisco Residences</em>',
  'Fråga om <em>Lentisco Residences</em>')
a('.enquiry.message',
  'Hola, Nueva Living, me gustaría recibir información sobre Lentisco Residences.',
  'Bonjour Nueva Living, je souhaiterais des informations sur Lentisco Residences.',
  'Guten Tag Nueva Living, ich möchte Informationen zu Lentisco Residences erhalten.',
  'Здравствуйте, Nueva Living! Хочу получить информацию о Lentisco Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Lentisco Residences.',
  'Goedendag Nueva Living, ik wil graag informatie over Lentisco Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje o Lentisco Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Lentisco Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Lentisco Residences.')
a('.faq[0][1]',
  'Tres de las 15 viviendas de esta fase, todas áticos de dos dormitorios: el C por {E363000}, el F por {E423000} y el G por {E460000}, antes de IVA. La lista de precios del {D5.11.2026} muestra 11 viviendas vendidas y una reservada.',
  'Trois des 15 logements de cette phase, tous des penthouses de deux chambres : le C à {E363000}, le F à {E423000} et le G à {E460000}, hors TVA. La liste de prix du {D5.11.2026} indique 11 logements vendus et un réservé.',
  'Drei der 15 Wohnungen dieses Bauabschnitts, alle Penthäuser mit zwei Schlafzimmern: C für {E363000}, F für {E423000} und G für {E460000}, zuzüglich MwSt. Die Preisliste vom {D5.11.2026} weist 11 Wohnungen als verkauft und eine als reserviert aus.',
  'Три из 15 квартир этой очереди, все — пентхаусы с двумя спальнями: C за {E363000}, F за {E423000} и G за {E460000}, без учёта НДС. В прайс-листе от {D5.11.2026} 11 квартир отмечены как проданные и одна как забронированная.',
  'ثلاثة من المساكن الخمسة عشر في هذه المرحلة، وكلها بنتهاوس بغرفتي نوم: C بسعر {E363000} وF بسعر {E423000} وG بسعر {E460000}، قبل ضريبة القيمة المضافة. وتُظهر قائمة الأسعار المؤرخة {D5.11.2026} أن 11 مسكنًا مبيعة وواحدًا محجوز.',
  'Drie van de 15 woningen in deze fase, allemaal penthouses met twee slaapkamers: C voor {E363000}, F voor {E423000} en G voor {E460000}, exclusief btw. De prijslijst van {D5.11.2026} toont 11 woningen als verkocht en één als gereserveerd.',
  'Trzy z 15 mieszkań tego etapu, wszystkie to penthouse’y z dwiema sypialniami: C za {E363000}, F za {E423000} i G za {E460000}, bez VAT. Cennik z {D5.11.2026} pokazuje 11 mieszkań jako sprzedane i jedno jako zarezerwowane.',
  'Tre av de 15 boligene i dette byggetrinnet, alle toppleiligheter med to soverom: C til {E363000}, F til {E423000} og G til {E460000}, før mva. Prislisten datert {D5.11.2026} viser 11 boliger som solgt og én som reservert.',
  'Tre av de 15 bostäderna i denna etapp, alla takvåningar med två sovrum: C för {E363000}, F för {E423000} och G för {E460000}, före IVA. Prislistan daterad {D5.11.2026} visar 11 bostäder som sålda och en som reserverad.')
a('.faq[1][1]',
  'No. La lista de precios indica que los precios son netos y no incluyen IVA, impuesto de transmisiones ni otros cargos. El IVA de la vivienda nueva es actualmente del 10 por ciento, y se añaden actos jurídicos documentados, notaría y registro.',
  'Non. La liste de prix précise que les prix sont nets et n’incluent ni la TVA, ni les droits de mutation, ni d’autres frais. La TVA sur le logement neuf est actuellement de 10 pour cent, à laquelle s’ajoutent les droits d’enregistrement et les frais de notaire et de registre foncier.',
  'Nein. Laut Preisliste sind die Preise netto, ohne MwSt., Grunderwerbsteuer oder sonstige Abgaben. Die MwSt. auf Neubauwohnungen beträgt derzeit 10 Prozent; hinzu kommen Stempelsteuer sowie Notar- und Grundbuchkosten.',
  'Нет. В прайс-листе указано, что цены нетто и не включают НДС, налог на передачу имущества и прочие сборы. НДС на новое жильё сейчас составляет 10 процентов; к нему добавляются гербовый сбор, услуги нотариуса и регистрация.',
  'لا. تنص قائمة الأسعار على أن الأسعار صافية ولا تشمل ضريبة القيمة المضافة ولا ضريبة نقل الملكية ولا رسومًا أخرى. وتبلغ ضريبة القيمة المضافة على المساكن الجديدة حاليًا 10 بالمئة، ويُضاف إليها رسم الدمغة ورسوم كاتب العدل والسجل العقاري.',
  'Nee. De prijslijst vermeldt dat de prijzen netto zijn, zonder btw, overdrachtsbelasting of andere kosten. De btw op nieuwbouw is momenteel 10 procent, en daar komen zegelrecht, notaris- en kadasterkosten bij.',
  'Nie. Cennik podaje, że ceny są netto i nie obejmują VAT, podatku od przeniesienia własności ani innych opłat. VAT na nowe mieszkania wynosi obecnie 10 procent, a do tego dochodzą opłata skarbowa oraz koszty notariusza i rejestru.',
  'Nei. Prislisten sier at prisene er netto og ikke inkluderer mva, overdragelsesskatt eller andre kostnader. Mva på nye boliger er i dag 10 prosent, og i tillegg kommer dokumentavgift, notar- og tinglysingsgebyrer.',
  'Nej. Prislistan anger att priserna är netto och inte inkluderar IVA (spansk moms), överlåtelseskatt eller andra avgifter. IVA på nybyggda bostäder är i dag 10 procent, och till det kommer stämpelskatt, notarie- och inskrivningsavgifter.')
a('.faq[2][1]',
  'El portal del promotor indica que la construcción empezó en octubre de 2025 y que la entrega está prevista para septiembre de 2027. Pedimos la fecha que figurará en el contrato.',
  'Le portail du promoteur indique que la construction a commencé en octobre 2025 et que la livraison est prévue pour septembre 2027. Nous demandons la date qui figurera au contrat.',
  'Das Portal des Bauträgers gibt an, dass der Bau im Oktober 2025 begonnen hat und die Fertigstellung für September 2027 geplant ist. Wir verlangen den Termin, der in den Vertrag kommt.',
  'На портале застройщика сказано, что строительство началось в октябре 2025 года, а сдача запланирована на сентябрь 2027 года. Мы запрашиваем дату, которая войдёт в договор.',
  'تذكر بوابة المطوّر أن البناء بدأ في أكتوبر 2025 وأن الإنجاز مقرر في سبتمبر 2027. ونطلب الموعد الذي سيُدرج في العقد.',
  'Het portaal van de ontwikkelaar vermeldt dat de bouw in oktober 2025 is begonnen en dat de oplevering gepland is voor september 2027. Wij vragen de datum die in het contract komt.',
  'Portal dewelopera podaje, że budowa ruszyła w październiku 2025 roku, a zakończenie zaplanowano na wrzesień 2027 roku. Prosimy o termin, który trafi do umowy.',
  'Utbyggerens portal oppgir at byggingen startet i oktober 2025 og at ferdigstillelse er planlagt til september 2027. Vi ber om datoen som skal stå i kontrakten.',
  'Exploatörens portal anger att bygget startade i oktober 2025 och att färdigställandet är planerat till september 2027. Vi begär det datum som skrivs in i avtalet.')
a('.faq[3][1]',
  '{E10000} para reservar, el 30 por ciento al contrato privado y el 70 por ciento en la escritura, con la licencia de primera ocupación, más el IVA de cada cantidad.',
  '{E10000} pour réserver, 30 pour cent au contrat privé et 70 pour cent à l’acte authentique, avec le certificat de première occupation, la TVA s’ajoutant à chaque montant.',
  '{E10000} zur Reservierung, 30 Prozent beim privaten Kaufvertrag und 70 Prozent bei der Beurkundung, mit der Bezugsgenehmigung, jeweils zuzüglich MwSt.',
  '{E10000} при бронировании, 30 процентов при подписании предварительного договора и 70 процентов при оформлении права собственности после получения разрешения на заселение, к каждой сумме добавляется НДС.',
  '{E10000} للحجز، و30 بالمئة عند العقد الخاص، و70 بالمئة عند سند الملكية مع رخصة الإشغال الأولى، وتُضاف ضريبة القيمة المضافة إلى كل مبلغ.',
  '{E10000} om te reserveren, 30 procent bij de onderhandse overeenkomst en 70 procent bij de akte, met de bewoningsvergunning, telkens plus btw.',
  '{E10000} przy rezerwacji, 30 procent przy umowie przedwstępnej i 70 procent przy akcie notarialnym, po uzyskaniu pozwolenia na użytkowanie, do każdej kwoty dolicza się VAT.',
  '{E10000} ved reservasjon, 30 prosent ved den private kontrakten og 70 prosent ved skjøtet, med brukstillatelsen, med mva i tillegg til hvert beløp.',
  '{E10000} vid bokning, 30 procent vid det privata avtalet och 70 procent vid köpebrevet, med inflyttningstillståndet, med IVA ovanpå varje belopp.')
a('.faq[4][0]', '¿Qué áticos tienen solárium?', 'Quels penthouses ont un solarium ?', 'Welche Penthäuser haben ein Dachsolarium?',
  'У каких пентхаусов есть солярий?', 'أي البنتهاوس لديها سولاريوم؟', 'Welke penthouses hebben een solarium?',
  'Które penthouse’y mają solarium?', 'Hvilke toppleiligheter har solterrasse?', 'Vilka takvåningar har solterrass?')
a('.faq[4][1]',
  'Los Áticos C y F, con soláriums privados en la cubierta de {N96.72} y {N104.96} {U}. El Ático G no tiene solárium, pero sí una terraza cubierta de {N46.65} {U} y una descubierta de {N4.14} {U}.',
  'Les penthouses C et F, avec des solariums privés sur le toit de {N96.72} et {N104.96} {U}. Le penthouse G n’a pas de solarium, mais une terrasse couverte de {N46.65} {U} et une terrasse découverte de {N4.14} {U}.',
  'Penthouse C und F, mit privaten Dachsolarien von {N96.72} und {N104.96} {U}. Penthouse G hat kein Solarium, dafür eine überdachte Terrasse von {N46.65} {U} und eine offene von {N4.14} {U}.',
  'Пентхаусы C и F — с собственными соляриями на крыше {N96.72} и {N104.96} {U}. У пентхауса G солярия нет, зато есть крытая терраса {N46.65} {U} и открытая {N4.14} {U}.',
  'البنتهاوس C وF، مع سولاريوم خاص على السطح مساحته {N96.72} و{N104.96} {U}. أما البنتهاوس G فلا سولاريوم له، لكن لديه تراس مسقوف مساحته {N46.65} {U} وتراس مكشوف مساحته {N4.14} {U}.',
  'Penthouse C en F, met een eigen solarium op het dak van {N96.72} en {N104.96} {U}. Penthouse G heeft geen solarium, maar wel een overdekt terras van {N46.65} {U} en een onoverdekt terras van {N4.14} {U}.',
  'Penthouse’y C i F, z prywatnymi solariami na dachu o powierzchni {N96.72} i {N104.96} {U}. Penthouse G nie ma solarium, ale ma zadaszony taras o powierzchni {N46.65} {U} i odkryty o powierzchni {N4.14} {U}.',
  'Toppleilighet C og F, med egne solterrasser på taket på {N96.72} og {N104.96} {U}. Toppleilighet G har ingen solterrasse, men en overbygd terrasse på {N46.65} {U} og en åpen terrasse på {N4.14} {U}.',
  'Takvåning C och F, med egna solterrasser på taket på {N96.72} och {N104.96} {U}. Takvåning G har ingen solterrass, men en överbyggd terrass på {N46.65} {U} och en öppen terrass på {N4.14} {U}.')
a('.faq[5][1]',
  'La piscina, el gimnasio, la sauna, la lavandería y el garaje de la fase anterior, que según el folleto ya existen.',
  'La piscine, la salle de sport, le sauna, la laverie et le garage de la phase précédente, qui existent déjà selon la brochure.',
  'Pool, Fitnessraum, Sauna, Waschküche und Garage des früheren Bauabschnitts, die laut Broschüre bereits vorhanden sind.',
  'Бассейн, тренажёрный зал, сауна, прачечная и гараж предыдущей очереди, которые, по данным буклета, уже существуют.',
  'المسبح والصالة الرياضية والساونا والمغسلة والمرآب التابعة للمرحلة السابقة، وهي موجودة بالفعل وفق الكتيّب.',
  'Het zwembad, de fitnessruimte, de sauna, de wasruimte en de garage van de eerdere fase, die er volgens de brochure al zijn.',
  'Basen, siłownia, sauna, pralnia i garaż wcześniejszego etapu, które według broszury już istnieją.',
  'Bassenget, treningsrommet, badstuen, vaskerommet og garasjen fra det tidligere byggetrinnet, som ifølge brosjyren allerede finnes.',
  'Poolen, gymmet, bastun, tvättstugan och garaget från den tidigare etappen, som enligt broschyren redan finns.')
a('.seo.title',
  'Lentisco Residences - Áticos en Los Pacos, Fuengirola', 'Lentisco Residences - Penthouses à Los Pacos, Fuengirola',
  'Lentisco Residences - Penthäuser in Los Pacos, Fuengirola', 'Lentisco Residences - Пентхаусы в Лос-Пакос, Фуэнхирола',
  'Lentisco Residences - بنتهاوس في لوس باكوس، فوينخيرولا', 'Lentisco Residences - Penthouses in Los Pacos, Fuengirola',
  'Lentisco Residences - Penthouse’y w Los Pacos, Fuengirola', 'Lentisco Residences - Toppleiligheter i Los Pacos',
  'Lentisco Residences - Takvåningar i Los Pacos, Fuengirola')
a('.seo.description',
  'Tres áticos de dos dormitorios en Los Pacos, Fuengirola, dos con solárium en la cubierta, en una nueva fase de un residencial consolidado, desde {E363000} más IVA, entrega en septiembre de 2027.',
  'Trois penthouses de deux chambres à Los Pacos, Fuengirola, dont deux avec un solarium sur le toit, dans une nouvelle phase d’une résidence établie, à partir de {E363000} hors TVA, livraison en septembre 2027.',
  'Drei Penthäuser mit zwei Schlafzimmern in Los Pacos, Fuengirola, zwei mit Dachsolarium, in einem neuen Bauabschnitt einer bestehenden Anlage, ab {E363000} zuzüglich MwSt., Fertigstellung September 2027.',
  'Три пентхауса с двумя спальнями в Лос-Пакос, Фуэнхирола, два с солярием на крыше, в новой очереди сложившегося комплекса, от {E363000} плюс НДС, сдача в сентябре 2027 года.',
  'ثلاثة بنتهاوس بغرفتي نوم في لوس باكوس، فوينخيرولا، اثنان منها مع سولاريوم على السطح، في مرحلة جديدة من مجمع قائم، ابتداءً من {E363000} زائد ضريبة القيمة المضافة، والإنجاز في سبتمبر 2027.',
  'Drie penthouses met twee slaapkamers in Los Pacos, Fuengirola, twee met een solarium op het dak, in een nieuwe fase van een bestaand complex, vanaf {E363000} plus btw, oplevering september 2027.',
  'Trzy penthouse’y z dwiema sypialniami w Los Pacos w Fuengiroli, dwa z solarium na dachu, w nowym etapie istniejącego osiedla, od {E363000} plus VAT, zakończenie we wrześniu 2027 roku.',
  'Tre toppleiligheter med to soverom i Los Pacos, Fuengirola, to med solterrasse på taket, i et nytt byggetrinn i et etablert anlegg, fra {E363000} pluss mva, ferdigstillelse september 2027.',
  'Tre takvåningar med två sovrum i Los Pacos, Fuengirola, två med solterrass på taket, i en ny etapp av ett etablerat område, från {E363000} plus IVA, färdigställande september 2027.')
_ctx = ['Áticos con solárium en Los Pacos, Fuengirola', 'Penthouses avec solarium sur le toit à Los Pacos, Fuengirola',
        'Penthäuser mit Dachsolarium in Los Pacos, Fuengirola', 'Пентхаусы с солярием на крыше в Лос-Пакос, Фуэнхирола',
        'بنتهاوس مع سولاريوم على السطح في لوس باكوس، فوينخيرولا', 'Penthouses met solarium op het dak in Los Pacos, Fuengirola',
        'Penthouse’y z solarium na dachu w Los Pacos, Fuengirola', 'Toppleiligheter med solterrasse på taket i Los Pacos, Fuengirola',
        'Takvåningar med solterrass på taket i Los Pacos, Fuengirola']
a('.seo.h1Context', *_ctx)
a('.seo.h1', *['Lentisco Residences: ' + c for c in _ctx])

T['EUR 363,000 - EUR 460,000 + VAT'] = {l: expand('{E363000} - {P460000}', l) for l in LOCS}

# assemble.py's pattern for "N% + VAT" gives Swedish "moms", which the audit forbids: set them here.
for _pc in ('30', '70'):
    T[f'{_pc}% + VAT'] = {l: f'{_pc}% + {TAXW[l]}' for l in LOCS}

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings')
