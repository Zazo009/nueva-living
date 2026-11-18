# -*- coding: utf-8 -*-
"""Retama Residences: the strings the translation memory did not have.

Keyed by the path of the English string in project.json (looked up here, never retyped, so a
change to the English copy cannot leave a translation attached to the wrong sentence) and
written to tr_a.json keyed by the English string, as assemble.py expects. Tokens: {E341000}
money, {N46.78} decimal number, {N31,000} grouped number, {U} the area unit, {T} the tax word.
Argument order in a(): es fr de ru ar nl pl no sv.
    python3 tools/import/k_retama_residences.py <scratch dir>   (writes <dir>/tr_a.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
TAXW = {'es': 'IVA', 'fr': 'TVA', 'de': 'MwSt.', 'ru': 'НДС', 'ar': 'ضريبة القيمة المضافة',
        'nl': 'btw', 'pl': 'VAT', 'no': 'mva', 'sv': 'IVA'}
T = {}
SLUG = 'retama-residences'
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


same('Retama Residences'); same('Retama'); same('Retama <em>Residences</em>')
for g in ['Cerrado del Águila Golf', 'Chaparral Golf', 'La Cala Golf Resort']:
    same(g)
for u in proj['availability']['units']:
    same(u['reference'])

# ---- description, SEO, card ------------------------------------------------------------------

a('.description',
  'Una promoción cerrada de 120 apartamentos y áticos en construcción en una ladera de Mijas Costa, con dos piscinas exteriores, spa, gimnasio y un salón de coworking. Diez viviendas de uno a tres dormitorios figuran en la lista de precios del promotor, desde {E341000} antes de {T}.',
  'Une résidence fermée de 120 appartements et penthouses en construction sur un coteau de Mijas Costa, avec deux piscines extérieures, un spa, une salle de sport et un espace de coworking. Dix logements d’une à trois chambres figurent sur la liste de prix du promoteur, à partir de {E341000} hors {T}.',
  'Eine geschlossene Anlage mit 120 Wohnungen und Penthouses im Bau an einem Hang in Mijas Costa, mit zwei Außenpools, Spa, Fitnessraum und Coworking-Lounge. Zehn Wohnungen mit einem bis drei Schlafzimmern stehen auf der Preisliste des Bauträgers, ab {E341000} vor {T}.',
  'Закрытый комплекс из 120 апартаментов и пентхаусов, который строится на склоне холма в Михас-Коста: два открытых бассейна, спа, тренажёрный зал и коворкинг. В прайс-листе застройщика десять квартир с одной–тремя спальнями, от {E341000} без {T}.',
  'مجمّع مغلق من 120 شقة وبنتهاوس قيد الإنشاء على سفح تلّ في ميخاس كوستا، مع مسبحين خارجيين وسبا وصالة رياضية وصالة للعمل المشترك. عشرة مساكن بغرفة إلى ثلاث غرف نوم مدرجة في قائمة أسعار المطوّر، ابتداءً من {E341000} قبل {T}.',
  'Een afgesloten complex van 120 appartementen en penthouses in aanbouw op een helling in Mijas Costa, met twee buitenzwembaden, een spa, een fitnessruimte en een coworkinglounge. Tien woningen met één tot drie slaapkamers staan op de prijslijst van de ontwikkelaar, vanaf {E341000} vóór {T}.',
  'Zamknięte osiedle 120 apartamentów i penthouse’ów w budowie na zboczu wzgórza w Mijas Costa, z dwoma basenami zewnętrznymi, spa, siłownią i strefą coworkingu. W cenniku dewelopera figuruje dziesięć lokali z jedną do trzech sypialni, od {E341000} przed {T}.',
  'Et inngjerdet anlegg med 120 leiligheter og toppleiligheter under bygging i en åsside i Mijas Costa, med to utendørs bassenger, spa, treningsrom og en coworking-lounge. Ti boliger med ett til tre soverom står på utbyggerens prisliste, fra {E341000} før {T}.',
  'Ett inhägnat område med 120 lägenheter och takvåningar under uppförande i en sluttning i Mijas Costa, med två utomhuspooler, spa, gym och en coworkinglounge. Tio bostäder med ett till tre sovrum finns på exploatörens prislista, från {E341000} före {T} (spansk moms).')
a('.seoDescription',
  'Apartamentos y áticos nuevos de uno a tres dormitorios en construcción en Mijas Costa, con dos piscinas, spa y gimnasio. Diez en la lista desde {E341000} más {T}.',
  'Appartements et penthouses neufs d’une à trois chambres en construction à Mijas Costa, avec deux piscines, un spa et une salle de sport. Dix sur la liste à partir de {E341000} hors {T}.',
  'Neue Wohnungen und Penthouses mit einem bis drei Schlafzimmern im Bau in Mijas Costa, mit zwei Pools, Spa und Fitnessraum. Zehn gelistet ab {E341000} zuzüglich {T}.',
  'Новые апартаменты и пентхаусы с одной–тремя спальнями, строящиеся в Михас-Коста: два бассейна, спа и тренажёрный зал. Десять в списке, от {E341000} плюс {T}.',
  'شقق وبنتهاوس جديدة بغرفة إلى ثلاث غرف نوم قيد الإنشاء في ميخاس كوستا، مع مسبحين وسبا وصالة رياضية. عشرة مدرجة ابتداءً من {E341000} زائد {T}.',
  'Nieuwe appartementen en penthouses met één tot drie slaapkamers in aanbouw in Mijas Costa, met twee zwembaden, een spa en een fitnessruimte. Tien op de lijst vanaf {E341000} plus {T}.',
  'Nowe apartamenty i penthouse’y z jedną do trzech sypialni w budowie w Mijas Costa, z dwoma basenami, spa i siłownią. Dziesięć w cenniku od {E341000} plus {T}.',
  'Nye leiligheter og toppleiligheter med ett til tre soverom under bygging i Mijas Costa, med to bassenger, spa og treningsrom. Ti oppført fra {E341000} pluss {T}.',
  'Nya lägenheter och takvåningar med ett till tre sovrum under uppförande i Mijas Costa, med två pooler, spa och gym. Tio listade från {E341000} plus {T}.')
a('.twitterDescription',
  'Apartamentos y áticos en construcción en Mijas Costa, con dos piscinas, spa y gimnasio, desde {E341000} más {T}.',
  'Appartements et penthouses en construction à Mijas Costa, avec deux piscines, un spa et une salle de sport, à partir de {E341000} hors {T}.',
  'Wohnungen und Penthouses im Bau in Mijas Costa, mit zwei Pools, Spa und Fitnessraum, ab {E341000} zuzüglich {T}.',
  'Строящиеся апартаменты и пентхаусы в Михас-Коста с двумя бассейнами, спа и тренажёрным залом, от {E341000} плюс {T}.',
  'شقق وبنتهاوس قيد الإنشاء في ميخاس كوستا، مع مسبحين وسبا وصالة رياضية، ابتداءً من {E341000} زائد {T}.',
  'Appartementen en penthouses in aanbouw in Mijas Costa, met twee zwembaden, een spa en een fitnessruimte, vanaf {E341000} plus {T}.',
  'Apartamenty i penthouse’y w budowie w Mijas Costa, z dwoma basenami, spa i siłownią, od {E341000} plus {T}.',
  'Leiligheter og toppleiligheter under bygging i Mijas Costa, med to bassenger, spa og treningsrom, fra {E341000} pluss {T}.',
  'Lägenheter och takvåningar under uppförande i Mijas Costa, med två pooler, spa och gym, från {E341000} plus {T}.')
a('.hero.delivery',
  'Entrega septiembre de 2028', 'Livraison septembre 2028', 'Fertigstellung September 2028', 'Сдача в сентябре 2028',
  'الإنجاز سبتمبر 2028', 'Oplevering september 2028', 'Odbiór wrzesień 2028', 'Ferdigstillelse september 2028',
  'Färdigställande september 2028')
a('.card.meta[2][1]',
  'Septiembre de 2028', 'Septembre 2028', 'September 2028', 'Сентябрь 2028', 'سبتمبر 2028', 'September 2028',
  'Wrzesień 2028', 'September 2028', 'September 2028')
a('.card.description',
  'Apartamentos y áticos de uno a tres dormitorios en una promoción cerrada de 120 viviendas en una ladera de Mijas Costa, con dos piscinas, spa y gimnasio.',
  'Appartements et penthouses d’une à trois chambres dans une résidence fermée de 120 logements sur un coteau de Mijas Costa, avec deux piscines, un spa et une salle de sport.',
  'Wohnungen und Penthouses mit einem bis drei Schlafzimmern in einer geschlossenen Hanganlage mit 120 Wohnungen in Mijas Costa, mit zwei Pools, Spa und Fitnessraum.',
  'Апартаменты и пентхаусы с одной–тремя спальнями в закрытом комплексе из 120 квартир на склоне в Михас-Коста, с двумя бассейнами, спа и тренажёрным залом.',
  'شقق وبنتهاوس بغرفة إلى ثلاث غرف نوم في مجمّع مغلق من 120 مسكناً على سفح تلّ في ميخاس كوستا، مع مسبحين وسبا وصالة رياضية.',
  'Appartementen en penthouses met één tot drie slaapkamers in een afgesloten complex van 120 woningen op een helling in Mijas Costa, met twee zwembaden, een spa en een fitnessruimte.',
  'Apartamenty i penthouse’y z jedną do trzech sypialni na zamkniętym osiedlu 120 lokali na zboczu w Mijas Costa, z dwoma basenami, spa i siłownią.',
  'Leiligheter og toppleiligheter med ett til tre soverom i et inngjerdet anlegg med 120 boliger i en åsside i Mijas Costa, med to bassenger, spa og treningsrom.',
  'Lägenheter och takvåningar med ett till tre sovrum i ett inhägnat område med 120 bostäder i en sluttning i Mijas Costa, med två pooler, spa och gym.')

# ---- images ----------------------------------------------------------------------------------

a('.images.hero.alt',
  'Vista generada por ordenador de dos piscinas comunitarias con tumbonas y sombrillas delante de un largo bloque de apartamentos con terrazas, con el mar en el horizonte',
  'Vue de synthèse de deux piscines communes avec transats et parasols devant un long bâtiment d’appartements à terrasses, avec la mer à l’horizon',
  'Computergenerierte Ansicht zweier Gemeinschaftspools mit Sonnenliegen und Schirmen vor einem langen Gebäude mit Terrassenwohnungen, das Meer am Horizont',
  'Компьютерная визуализация: два общих бассейна с шезлонгами и зонтиками перед длинным корпусом квартир с террасами, на горизонте море',
  'منظر مُنشأ بالحاسوب لمسبحين مشتركين مع كراسي استلقاء ومظلات أمام مبنى طويل من الشقق ذات التراسات، والبحر في الأفق',
  'Computergegenereerd beeld van twee gemeenschappelijke zwembaden met ligbedden en parasols voor een lang blok appartementen met terrassen, met de zee aan de horizon',
  'Wizualizacja komputerowa dwóch wspólnych basenów z leżakami i parasolami przed długim budynkiem apartamentów z tarasami, z morzem na horyzoncie',
  'Datagenerert bilde av to felles bassenger med solsenger og parasoller foran en lang blokk med terrasseleiligheter, med havet i horisonten',
  'Datorgenererad bild av två gemensamma pooler med solstolar och parasoller framför ett långt hus med terrasslägenheter, med havet vid horisonten')
a('.images.architecture.alt',
  'Vista generada por ordenador de un patio de entrada pavimentado con plantas y olivos delante de bloques blancos y color piedra',
  'Vue de synthèse d’une cour d’entrée pavée, plantée d’arbustes et d’oliviers, devant des bâtiments blancs et couleur pierre',
  'Computergenerierte Ansicht eines gepflasterten Eingangshofs mit Bepflanzung und Olivenbäumen vor weißen und steinfarbenen Gebäuden',
  'Компьютерная визуализация мощёного въездного двора с зеленью и оливами перед белыми и песочными корпусами',
  'منظر مُنشأ بالحاسوب لساحة مدخل مرصوفة بالنباتات وأشجار الزيتون أمام مبانٍ بيضاء وبلون الحجر',
  'Computergegenereerd beeld van een geplaveide entreehof met beplanting en olijfbomen voor witte en steenkleurige blokken',
  'Wizualizacja komputerowa brukowanego dziedzińca wejściowego z zielenią i drzewami oliwnymi przed białymi i kamiennymi budynkami',
  'Datagenerert bilde av en brolagt inngangsgård med beplantning og oliventrær foran hvite og steinfargede blokker',
  'Datorgenererad bild av en stenlagd entrégård med planteringar och olivträd framför vita och stenfärgade hus')
a('.images.lifestyle.alt',
  'Salón exterior generado por ordenador al anochecer, con sofás curvos alrededor de un fuego bajo una pérgola de madera cubierta de plantas y mesas de comedor detrás',
  'Salon extérieur de synthèse au crépuscule, avec des canapés courbes autour d’un brasero sous une pergola en bois végétalisée et des tables à manger derrière',
  'Computergenerierte Außenlounge in der Abenddämmerung mit geschwungenen Sofas um eine Feuerstelle unter einer bewachsenen Holzpergola, dahinter Esstische',
  'Компьютерная визуализация уличной лаунж-зоны в сумерках: изогнутые диваны вокруг очага под деревянной перголой с растениями, позади обеденные столы',
  'صالة خارجية مُنشأة بالحاسوب عند الغسق، بأرائك منحنية حول موقد نار تحت عريشة خشبية مكسوّة بالنباتات، وخلفها طاولات طعام',
  'Computergegenereerde buitenlounge bij schemering met gebogen banken rond een vuurplaats onder een begroeide houten pergola, met eettafels erachter',
  'Wizualizacja komputerowa zewnętrznego salonu o zmierzchu z łukowymi sofami wokół paleniska pod porośniętą drewnianą pergolą i stołami jadalnymi w tle',
  'Datagenerert utendørs lounge i skumringen med buede sofaer rundt et bålsted under en tilgrodd trepergola, med spisebord bak',
  'Datorgenererad utomhuslounge i skymningen med svängda soffor kring en eldstad under en grönskande träpergola, med matbord bakom')
a('.images.privateViewing.alt',
  'Terraza cubierta generada por ordenador con una mesa de comedor bajo una pérgola de lamas, el salón tras puertas correderas de cristal y colinas arboladas que bajan hasta el mar',
  'Terrasse couverte de synthèse avec une table à manger sous une pergola à lames, le séjour derrière des baies coulissantes et des collines boisées descendant vers la mer',
  'Computergenerierte überdachte Terrasse mit Esstisch unter einer Lamellenpergola, dahinter das Wohnzimmer hinter Glasschiebetüren und bewaldete Hügel bis zum Meer',
  'Компьютерная визуализация крытой террасы с обеденным столом под ламельной перголой; за раздвижными стеклянными дверями гостиная, лесистые холмы спускаются к морю',
  'تراس مسقوف مُنشأ بالحاسوب مع طاولة طعام تحت عريشة من الشرائح، وغرفة المعيشة خلف أبواب زجاجية منزلقة، وتلال مشجّرة تنحدر نحو البحر',
  'Computergegenereerd overdekt terras met een eettafel onder een lamellenpergola, de woonkamer achter glazen schuifdeuren en beboste heuvels die aflopen naar de zee',
  'Wizualizacja komputerowa zadaszonego tarasu ze stołem pod pergolą lamelową, salonem za przesuwnymi szklanymi drzwiami i zalesionymi wzgórzami opadającymi ku morzu',
  'Datagenerert overbygd terrasse med spisebord under en lamellpergola, stuen bak skyvedører i glass og skogkledde åser ned mot havet',
  'Datorgenererad täckt terrass med matbord under en lamellpergola, vardagsrummet bakom glasade skjutdörrar och skogklädda kullar ned mot havet')

a('.media.headlineHtml',
  'La promoción en <em>imágenes</em>', 'La résidence en <em>images</em>', 'Die Anlage in <em>Bildern</em>',
  'Комплекс в <em>изображениях</em>', 'المشروع <em>بالصور</em>', 'Het complex in <em>beeld</em>',
  'Osiedle na <em>zdjęciach</em>', 'Anlegget i <em>bilder</em>', 'Området i <em>bilder</em>')
a('.media.copy',
  'Vistas generadas por ordenador de los bloques, las piscinas, las terrazas, los interiores y las zonas comunes, una vista aérea del solar y los planos de las diez viviendas de la lista de precios.',
  'Vues de synthèse des bâtiments, des piscines, des terrasses, des intérieurs et des espaces communs, une vue aérienne du terrain et les plans des dix logements de la liste de prix.',
  'Computergenerierte Ansichten der Gebäude, der Pools, der Terrassen, der Innenräume und der Gemeinschaftsbereiche, eine Luftaufnahme des Grundstücks und die Grundrisse der zehn Wohnungen der Preisliste.',
  'Компьютерные визуализации корпусов, бассейнов, террас, интерьеров и общих зон, вид участка с воздуха и планировки десяти квартир из прайс-листа.',
  'مناظر مُنشأة بالحاسوب للمباني والمسابح والتراسات والتصاميم الداخلية والمرافق المشتركة، ومنظر جوي للموقع، ومخططات المساكن العشرة الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van de blokken, de zwembaden, de terrassen, de interieurs en de gemeenschappelijke ruimtes, een luchtfoto van het terrein en de plattegronden van de tien woningen op de prijslijst.',
  'Wizualizacje komputerowe budynków, basenów, tarasów, wnętrz i części wspólnych, widok działki z lotu ptaka oraz rzuty dziesięciu lokali z cennika.',
  'Datagenererte bilder av blokkene, bassengene, terrassene, interiørene og fellesområdene, et flyfoto av tomten og planløsningene for de ti boligene på prislisten.',
  'Datorgenererade bilder av husen, poolerna, terrasserna, interiörerna och de gemensamma ytorna, en flygbild av tomten och planritningarna för de tio bostäderna på prislistan.')
a('.media.note',
  'Las imágenes están generadas por ordenador, salvo la vista aérea, en la que los edificios previstos se insertan en una fotografía del entorno. El mobiliario, la decoración y la vegetación que muestran son ilustrativos y no están incluidos. Los planos son los del promotor, elaborados a partir del proyecto básico del edificio, sin los logotipos del promotor ni el nombre del proyecto; el promotor indica que son orientativos y no definitivos y que las superficies son aproximadas, y los nombres de las estancias figuran en español.',
  'Les images sont des vues de synthèse, sauf la vue aérienne, dans laquelle les bâtiments prévus sont insérés dans une photographie des environs. Le mobilier, la décoration et la végétation qu’elles montrent sont illustratifs et non inclus. Les plans sont ceux du promoteur, établis à partir du projet de base du bâtiment, sans les logos du promoteur ni le nom du projet ; le promoteur précise qu’ils sont indicatifs et non définitifs et que les surfaces sont approximatives, et les noms des pièces y figurent en espagnol.',
  'Die Bilder sind computergeneriert, mit Ausnahme der Luftaufnahme, in die die geplanten Gebäude in ein Foto der Umgebung eingesetzt sind. Möbel, Dekoration und Bepflanzung sind illustrativ und nicht enthalten. Die Grundrisse sind die des Bauträgers, erstellt nach dem Grundprojekt des Gebäudes, ohne die Logos des Bauträgers und den Projektnamen; der Bauträger bezeichnet sie als Orientierung und nicht endgültig, die Flächen als ungefähr, und die Raumbezeichnungen sind auf Spanisch.',
  'Изображения созданы на компьютере, кроме вида с воздуха, где запланированные здания вставлены в фотографию окрестностей. Мебель, декор и растения на них показаны для иллюстрации и не входят в предложение. Планировки — застройщика, составлены по базовому проекту здания, без логотипов застройщика и названия проекта; застройщик указывает, что они ориентировочные и не окончательные, а площади приблизительные. Названия помещений на них на испанском языке.',
  'الصور مُنشأة بالحاسوب، باستثناء المنظر الجوي الذي أُدرجت فيه المباني المخطط لها في صورة فوتوغرافية للمحيط. الأثاث والديكور والنباتات الظاهرة فيها للتوضيح فقط وليست مشمولة. المخططات هي مخططات المطوّر، مُعدّة انطلاقاً من المشروع الأساسي للمبنى، بعد إزالة شعارات المطوّر واسم المشروع؛ ويذكر المطوّر أنها إرشادية وغير نهائية وأن المساحات تقريبية، وأسماء الغرف فيها بالإسبانية.',
  'De beelden zijn computergegenereerd, behalve de luchtfoto, waarin de geplande gebouwen in een foto van de omgeving zijn geplaatst. Het meubilair, de decoratie en de beplanting zijn illustratief en niet inbegrepen. De plattegronden zijn die van de ontwikkelaar, opgesteld op basis van het basisproject van het gebouw, zonder de logo’s van de ontwikkelaar en de projectnaam; de ontwikkelaar noemt ze indicatief en niet definitief en de oppervlaktes bij benadering, en de namen van de vertrekken staan er in het Spaans op.',
  'Obrazy są wizualizacjami komputerowymi, z wyjątkiem widoku z lotu ptaka, w którym planowane budynki wstawiono w fotografię okolicy. Meble, dekoracje i roślinność mają charakter poglądowy i nie są wliczone. Rzuty pochodzą od dewelopera i zostały opracowane na podstawie projektu podstawowego budynku, bez logotypów dewelopera i nazwy projektu; deweloper zaznacza, że są orientacyjne i nieostateczne, a powierzchnie przybliżone. Nazwy pomieszczeń są na nich po hiszpańsku.',
  'Bildene er datagenererte, unntatt flyfotoet, der de planlagte bygningene er satt inn i et fotografi av omgivelsene. Møbler, dekor og beplantning er illustrasjoner og ikke inkludert. Planløsningene er utbyggerens, laget ut fra byggets forprosjekt, uten utbyggerens logoer og prosjektnavnet; utbyggeren skriver at de er veiledende og ikke endelige, at arealene er omtrentlige, og romnavnene står på spansk.',
  'Bilderna är datorgenererade, utom flygbilden, där de planerade husen har infogats i ett fotografi av omgivningen. Möbler, inredning och växter är illustrationer och ingår inte. Planritningarna är exploatörens, gjorda utifrån byggnadens grundprojekt, utan exploatörens logotyper och projektnamnet; exploatören anger att de är vägledande och inte slutgiltiga och att ytorna är ungefärliga, och rumsnamnen står på spanska.')

a('.media.items[0].caption',
  'Las dos piscinas y un bloque', 'Les deux piscines et un bâtiment', 'Die beiden Pools und ein Gebäude', 'Два бассейна и корпус',
  'المسبحان وأحد المباني', 'De twee zwembaden en een blok', 'Dwa baseny i budynek', 'De to bassengene og en blokk', 'De två poolerna och ett hus')
a('.media.items[1].alt',
  'Vista generada por ordenador al anochecer a través de la piscina comunitaria hacia bloques con terrazas profundas y barandillas de cristal, con tumbonas a lo largo del agua',
  'Vue de synthèse au crépuscule à travers la piscine commune vers des bâtiments aux terrasses profondes et garde-corps en verre, avec des transats le long de l’eau',
  'Computergenerierte Ansicht in der Abenddämmerung über den Gemeinschaftspool zu Gebäuden mit tiefen Terrassen und Glasbrüstungen, mit Sonnenliegen am Wasser',
  'Компьютерная визуализация в сумерках: вид через общий бассейн на корпуса с глубокими террасами и стеклянными ограждениями, вдоль воды шезлонги',
  'منظر مُنشأ بالحاسوب عند الغسق عبر المسبح المشترك نحو مبانٍ ذات تراسات عميقة ودرابزين زجاجي، مع كراسي استلقاء على امتداد الماء',
  'Computergegenereerd beeld bij schemering over het gemeenschappelijke zwembad naar blokken met diepe terrassen en glazen balustrades, met ligbedden langs het water',
  'Wizualizacja komputerowa o zmierzchu: widok przez wspólny basen na budynki z głębokimi tarasami i szklanymi balustradami, z leżakami wzdłuż wody',
  'Datagenerert bilde i skumringen over fellesbassenget mot blokker med dype terrasser og glassrekkverk, med solsenger langs vannet',
  'Datorgenererad bild i skymningen över den gemensamma poolen mot hus med djupa terrasser och glasräcken, med solstolar längs vattnet')
a('.media.items[1].caption',
  'Las piscinas al anochecer', 'Les piscines au crépuscule', 'Die Pools in der Abenddämmerung', 'Бассейны в сумерках',
  'المسابح عند الغسق', 'De zwembaden bij schemering', 'Baseny o zmierzchu', 'Bassengene i skumringen', 'Poolerna i skymningen')
a('.media.items[2].alt',
  'Vista aérea de los bloques previstos alrededor de su piscina en una ladera de monte bajo y pinos, con casas, calles de golf y el mar al fondo',
  'Vue aérienne des bâtiments prévus autour de leur piscine sur un coteau de garrigue et de pins, avec des maisons, des fairways de golf et la mer au loin',
  'Luftaufnahme der geplanten Gebäude um ihren Pool an einem Hang mit Buschland und Pinien, dahinter Häuser, Golfbahnen und das Meer',
  'Вид с воздуха на запланированные корпуса вокруг бассейна на склоне с кустарником и соснами; дальше дома, поля для гольфа и море',
  'منظر جوي للمباني المخطط لها حول مسبحها على سفح تكسوه الشجيرات والصنوبر، وخلفها منازل وملاعب غولف والبحر',
  'Luchtfoto van de geplande blokken rond hun zwembad op een helling met struikgewas en pijnbomen, met huizen, golfbanen en de zee op de achtergrond',
  'Widok z lotu ptaka na planowane budynki wokół basenu na zboczu porośniętym zaroślami i sosnami, z domami, polami golfowymi i morzem w tle',
  'Flyfoto av de planlagte blokkene rundt bassenget i en åsside med kratt og furu, med hus, golfbaner og havet i bakgrunnen',
  'Flygbild av de planerade husen kring sin pool i en sluttning med buskmark och tallar, med hus, golfbanor och havet i bakgrunden')
a('.media.items[3].alt',
  'Vista generada por ordenador de los bloques bajos escalonados en una ladera verde alrededor de la piscina, con paneles solares sobre el aparcamiento en primer plano',
  'Vue de synthèse des bâtiments bas étagés sur un coteau verdoyant autour de la piscine, avec des panneaux solaires au-dessus du parking au premier plan',
  'Computergenerierte Ansicht der niedrigen Gebäude, gestaffelt an einem grünen Hang um den Pool, mit Solarmodulen über dem Parkplatz im Vordergrund',
  'Компьютерная визуализация: невысокие корпуса уступами на зелёном склоне вокруг бассейна, на переднем плане солнечные панели над парковкой',
  'منظر مُنشأ بالحاسوب للمباني المنخفضة المتدرّجة على سفح أخضر حول المسبح، مع ألواح شمسية فوق موقف السيارات في المقدمة',
  'Computergegenereerd beeld van de lage blokken die trapsgewijs over een groene helling rond het zwembad lopen, met zonnepanelen boven het parkeerterrein op de voorgrond',
  'Wizualizacja komputerowa niskich budynków tarasowo rozmieszczonych na zielonym zboczu wokół basenu, z panelami słonecznymi nad parkingiem na pierwszym planie',
  'Datagenerert bilde av de lave blokkene trappet over en grønn åsside rundt bassenget, med solcellepaneler over parkeringen i forgrunnen',
  'Datorgenererad bild av de låga husen i terrasser på en grön sluttning kring poolen, med solpaneler över parkeringen i förgrunden')
a('.media.items[5].alt',
  'Vista generada por ordenador de un camino pavimentado que cruza un estanque de nenúfares hacia la terraza de la piscina, con tumbonas, olivos y el mar a lo lejos',
  'Vue de synthèse d’une allée pavée traversant un bassin de nénuphars vers la plage de la piscine, avec transats, oliviers et la mer au loin',
  'Computergenerierte Ansicht eines gepflasterten Wegs über einen Seerosenteich zur Poolterrasse, mit Sonnenliegen, Olivenbäumen und dem Meer in der Ferne',
  'Компьютерная визуализация мощёной дорожки через пруд с кувшинками к террасе бассейна, с шезлонгами, оливами и морем вдали',
  'منظر مُنشأ بالحاسوب لممر مرصوف يعبر بركة زنابق نحو تراس المسبح، مع كراسي استلقاء وأشجار زيتون والبحر في البعيد',
  'Computergegenereerd beeld van een geplaveid pad over een vijver met waterlelies naar het zwembadterras, met ligbedden, olijfbomen en de zee in de verte',
  'Wizualizacja komputerowa brukowanej ścieżki przecinającej staw z liliami wodnymi w stronę tarasu basenu, z leżakami, drzewami oliwnymi i morzem w oddali',
  'Datagenerert bilde av en brolagt sti over en dam med vannliljer mot bassengterrassen, med solsenger, oliventrær og havet i det fjerne',
  'Datorgenererad bild av en stenlagd gång över en damm med näckrosor mot poolterrassen, med solstolar, olivträd och havet i fjärran')
a('.media.items[5].caption',
  'El camino a la piscina', 'L’allée vers la piscine', 'Der Weg zum Pool', 'Дорожка к бассейну', 'الممر إلى المسبح',
  'Het pad naar het zwembad', 'Ścieżka do basenu', 'Stien til bassenget', 'Gången till poolen')
a('.media.items[6].alt',
  'Terraza de planta baja generada por ordenador con una mesa de comedor larga y un sofá de exterior sobre césped, bajo balcones con ventiladores de techo y con el mar a lo lejos',
  'Terrasse de rez-de-chaussée de synthèse avec une longue table à manger et un canapé d’extérieur sur la pelouse, sous des balcons à ventilateurs de plafond, avec la mer au loin',
  'Computergenerierte Erdgeschossterrasse mit langem Esstisch und Outdoor-Sofa auf dem Rasen, unter Balkonen mit Deckenventilatoren, das Meer in der Ferne',
  'Компьютерная визуализация террасы первого этажа с длинным обеденным столом и уличным диваном на газоне, под балконами с потолочными вентиляторами, вдали море',
  'تراس في الطابق الأرضي مُنشأ بالحاسوب مع طاولة طعام طويلة وأريكة خارجية على العشب، تحت شرفات بمراوح سقف، والبحر في البعيد',
  'Computergegenereerd terras op de begane grond met een lange eettafel en een buitenbank op het gazon, onder balkons met plafondventilatoren, met de zee in de verte',
  'Wizualizacja komputerowa tarasu na parterze z długim stołem i sofą ogrodową na trawniku, pod balkonami z wentylatorami sufitowymi, z morzem w oddali',
  'Datagenerert terrasse i første etasje med et langt spisebord og en utesofa på plenen, under balkonger med takvifter, med havet i det fjerne',
  'Datorgenererad terrass på bottenvåningen med ett långt matbord och en utomhussoffa på gräsmattan, under balkonger med takfläktar, med havet i fjärran')
a('.media.items[6].caption',
  'Una terraza y jardín en planta baja', 'Une terrasse et un jardin en rez-de-chaussée', 'Terrasse und Garten im Erdgeschoss',
  'Терраса и сад на первом этаже', 'تراس وحديقة في الطابق الأرضي', 'Een terras en tuin op de begane grond',
  'Taras i ogród na parterze', 'En terrasse og hage i første etasje', 'En terrass och trädgård på bottenvåningen')
a('.media.items[8].alt',
  'Terraza de ático generada por ordenador con una mesa de comedor redonda, una encimera de cocina exterior bajo un voladizo de vigas de madera y el mar tras una barandilla de cristal',
  'Terrasse de penthouse de synthèse avec une table ronde, un plan de cuisine extérieure sous un auvent à poutres de bois et la mer au-delà d’un garde-corps en verre',
  'Computergenerierte Penthouse-Terrasse mit rundem Esstisch, einer Außenküchenzeile unter einem Holzbalkenvordach und dem Meer hinter einer Glasbrüstung',
  'Компьютерная визуализация террасы пентхауса с круглым обеденным столом, уличной кухонной стойкой под навесом из деревянных балок и морем за стеклянным ограждением',
  'تراس بنتهاوس مُنشأ بالحاسوب مع طاولة طعام مستديرة ومطبخ خارجي تحت بروز بعوارض خشبية، والبحر خلف درابزين زجاجي',
  'Computergegenereerd penthouseterras met een ronde eettafel, een buitenkeuken onder een overstek met houten balken en de zee achter een glazen balustrade',
  'Wizualizacja komputerowa tarasu penthouse’u z okrągłym stołem, blatem kuchni zewnętrznej pod okapem z drewnianych belek i morzem za szklaną balustradą',
  'Datagenerert terrasse på en toppleilighet med rundt spisebord, et utekjøkken under et overheng med trebjelker og havet bak et glassrekkverk',
  'Datorgenererad terrass på en takvåning med runt matbord, en utomhusköksbänk under ett utsprång med träbjälkar och havet bakom ett glasräcke')
a('.media.items[8].caption',
  'Una terraza de ático', 'Une terrasse de penthouse', 'Eine Penthouse-Terrasse', 'Терраса пентхауса', 'تراس بنتهاوس',
  'Een penthouseterras', 'Taras penthouse’u', 'En terrasse på en toppleilighet', 'En terrass på en takvåning')
a('.media.items[9].alt',
  'Salón abierto generado por ordenador con sofá, mesa de comedor y una cocina con isla de aspecto mármol, abierto a una terraza mediante puertas correderas de cristal',
  'Séjour ouvert de synthèse avec canapé, table à manger et cuisine à îlot aspect marbre, ouvert sur une terrasse par des baies coulissantes',
  'Computergenerierter offener Wohnbereich mit Sofa, Esstisch und Küche mit Kochinsel in Marmoroptik, über Glasschiebetüren zur Terrasse geöffnet',
  'Компьютерная визуализация открытой гостиной с диваном, обеденным столом и кухней с островом под мрамор, раздвижные стеклянные двери ведут на террасу',
  'غرفة معيشة مفتوحة مُنشأة بالحاسوب مع أريكة وطاولة طعام ومطبخ بجزيرة بمظهر الرخام، تنفتح على تراس عبر أبواب زجاجية منزلقة',
  'Computergegenereerde open woonkamer met een bank, een eettafel en een keuken met een kookeiland in marmerlook, via glazen schuifdeuren open naar een terras',
  'Wizualizacja komputerowa otwartego salonu z sofą, stołem i kuchnią z wyspą imitującą marmur, otwartego na taras przesuwnymi szklanymi drzwiami',
  'Datagenerert åpen stue med sofa, spisebord og kjøkken med marmorlignende kjøkkenøy, åpen mot en terrasse gjennom skyvedører i glass',
  'Datorgenererat öppet vardagsrum med soffa, matbord och kök med köksö i marmorlook, öppet mot en terrass genom glasade skjutdörrar')
a('.media.items[10].alt',
  'Dormitorio generado por ordenador con una cama doble contra una pared de listones de madera y una puerta corredera de cristal a una terraza con vistas al mar',
  'Chambre de synthèse avec un lit double contre un mur à tasseaux de bois et une baie coulissante ouvrant sur une terrasse avec vue sur la mer',
  'Computergeneriertes Schlafzimmer mit Doppelbett vor einer gerippten Holzwand und einer Glasschiebetür zu einer Terrasse mit Meerblick',
  'Компьютерная визуализация спальни с двуспальной кроватью у стены из деревянных реек и раздвижной стеклянной дверью на террасу с видом на море',
  'غرفة نوم مُنشأة بالحاسوب مع سرير مزدوج أمام جدار من الألواح الخشبية المضلّعة وباب زجاجي منزلق إلى تراس بإطلالة على البحر',
  'Computergegenereerde slaapkamer met een tweepersoonsbed tegen een geribde houten wand en een glazen schuifdeur naar een terras met zeezicht',
  'Wizualizacja komputerowa sypialni z podwójnym łóżkiem przy ścianie z drewnianych listew i przesuwnymi szklanymi drzwiami na taras z widokiem na morze',
  'Datagenerert soverom med dobbeltseng mot en ribbet trevegg og en skyvedør i glass til en terrasse med havutsikt',
  'Datorgenererat sovrum med dubbelsäng mot en räfflad trävägg och en glasad skjutdörr till en terrass med havsutsikt')
a('.media.items[11].alt',
  'Baño generado por ordenador con revestimiento de aspecto mármol, ducha a ras de suelo con mampara de cristal y un mueble de lavabo suspendido',
  'Salle de bains de synthèse aux carreaux aspect marbre, avec douche à l’italienne derrière une paroi vitrée et un meuble vasque suspendu',
  'Computergeneriertes Bad mit Fliesen in Marmoroptik, bodengleicher Dusche mit Glaswand und wandhängendem Waschtisch',
  'Компьютерная визуализация ванной с плиткой под мрамор, душем без поддона за стеклянной перегородкой и подвесной тумбой с раковиной',
  'حمام مُنشأ بالحاسوب ببلاط بمظهر الرخام ودُش مفتوح بحاجز زجاجي ووحدة مغسلة معلّقة',
  'Computergegenereerde badkamer met tegels in marmerlook, een inloopdouche met glazen wand en een zwevend wastafelmeubel',
  'Wizualizacja komputerowa łazienki z płytkami imitującymi marmur, prysznicem typu walk-in za szklaną ścianką i podwieszaną szafką z umywalką',
  'Datagenerert bad med marmorlignende fliser, en walk-in-dusj med glassvegg og et vegghengt servantskap',
  'Datorgenererat badrum med kakel i marmorlook, en walk-in-dusch med glasvägg och ett vägghängt tvättställ')
a('.media.items[12].alt',
  'Spa generado por ordenador con una piscina interior climatizada, tumbonas sobre suelo de piedra y una sauna con frente de cristal',
  'Spa de synthèse avec une piscine intérieure chauffée, des transats sur un sol en pierre et un sauna à façade vitrée',
  'Computergeneriertes Spa mit beheiztem Innenpool, Liegen auf Steinboden und einer Sauna mit Glasfront',
  'Компьютерная визуализация спа с крытым подогреваемым бассейном, лежаками на каменном полу и сауной со стеклянным фасадом',
  'سبا مُنشأ بالحاسوب مع مسبح داخلي مُدفّأ وكراسي استلقاء على أرضية حجرية وساونا بواجهة زجاجية',
  'Computergegenereerde spa met een verwarmd binnenzwembad, ligbedden op een stenen vloer en een sauna met glazen pui',
  'Wizualizacja komputerowa spa z podgrzewanym basenem wewnętrznym, leżankami na kamiennej posadzce i sauną z przeszkloną ścianą',
  'Datagenerert spa med oppvarmet innendørsbasseng, solsenger på steingulv og en badstue med glassfront',
  'Datorgenererat spa med en uppvärmd inomhuspool, vilstolar på stengolv och en bastu med glasfront')
a('.media.items[13].alt',
  'Gimnasio generado por ordenador con techo de lamas de madera, máquinas de musculación, cintas de correr y puertas acristaladas al jardín',
  'Salle de sport de synthèse avec un plafond à lames de bois, des appareils de musculation, des tapis de course et des portes vitrées sur le jardin',
  'Computergenerierter Fitnessraum mit Holzlamellendecke, Kraftgeräten, Laufbändern und Glastüren zum Garten',
  'Компьютерная визуализация тренажёрного зала с потолком из деревянных ламелей, силовыми тренажёрами, беговыми дорожками и стеклянными дверями в сад',
  'صالة رياضية مُنشأة بالحاسوب بسقف من الشرائح الخشبية وأجهزة قوة وأجهزة جري وأبواب زجاجية إلى الحديقة',
  'Computergegenereerde fitnessruimte met een plafond van houten lamellen, krachtapparaten, loopbanden en glazen deuren naar de tuin',
  'Wizualizacja komputerowa siłowni z sufitem z drewnianych lameli, maszynami do ćwiczeń siłowych, bieżniami i przeszklonymi drzwiami do ogrodu',
  'Datagenerert treningsrom med tak av trelameller, styrkeapparater, tredemøller og glassdører ut mot hagen',
  'Datorgenererat gym med tak av träribbor, styrkemaskiner, löpband och glasdörrar mot trädgården')
a('.media.items[14].alt',
  'Vista generada por ordenador del edificio de una planta del gimnasio, con esterillas de yoga sobre una tarima de madera delante, cubierta vegetal y un bloque de apartamentos encima',
  'Vue de synthèse du bâtiment de plain-pied de la salle de sport, avec des tapis de yoga sur un platelage en bois devant, un toit végétalisé et un bâtiment d’appartements au-dessus',
  'Computergenerierte Ansicht des eingeschossigen Fitnessgebäudes mit Yogamatten auf einem Holzdeck davor, begrüntem Dach und einem Wohngebäude darüber',
  'Компьютерная визуализация одноэтажного здания тренажёрного зала: коврики для йоги на деревянном настиле перед ним, зелёная кровля и жилой корпус выше',
  'منظر مُنشأ بالحاسوب لمبنى الصالة الرياضية ذي الطابق الواحد، مع حُصر يوغا على منصة خشبية أمامه وسطح مزروع ومبنى شقق فوقه',
  'Computergegenereerd beeld van het gelijkvloerse gebouw van de fitnessruimte, met yogamatten op een houten vlonder ervoor, een groen dak en een blok appartementen erboven',
  'Wizualizacja komputerowa parterowego budynku siłowni z matami do jogi na drewnianym podeście przed nim, zielonym dachem i budynkiem apartamentów powyżej',
  'Datagenerert bilde av treningsbygget i én etasje, med yogamatter på et treplatting foran, grønt tak og en leilighetsblokk over',
  'Datorgenererad bild av gymmets byggnad i ett plan, med yogamattor på ett trädäck framför, sedumtak och ett lägenhetshus ovanför')
a('.media.items[14].caption',
  'El gimnasio y la terraza de yoga', 'La salle de sport et la terrasse de yoga', 'Der Fitnessraum und die Yogaterrasse',
  'Тренажёрный зал и терраса для йоги', 'الصالة الرياضية وتراس اليوغا', 'De fitnessruimte en het yogaterras',
  'Siłownia i taras do jogi', 'Treningsrommet og yogaterrassen', 'Gymmet och yogaterrassen')
a('.media.items[15].alt',
  'Salón social generado por ordenador con largas mesas de trabajo compartidas, pufs y un sofá, abierto a una terraza',
  'Salon commun de synthèse avec de longs bureaux partagés, des poufs et un canapé, ouvert sur une terrasse',
  'Computergenerierte Gemeinschaftslounge mit langen gemeinsamen Arbeitstischen, Sitzsäcken und einem Sofa, zur Terrasse geöffnet',
  'Компьютерная визуализация общей гостиной с длинными общими рабочими столами, креслами-мешками и диваном, с выходом на террасу',
  'صالة اجتماعية مُنشأة بالحاسوب مع مكاتب عمل طويلة مشتركة ووسائد جلوس وأريكة، تنفتح على تراس',
  'Computergegenereerde sociale lounge met lange gedeelde werktafels, zitzakken en een bank, open naar een terras',
  'Wizualizacja komputerowa salonu wspólnego z długimi wspólnymi biurkami, pufami i sofą, otwartego na taras',
  'Datagenerert fellesstue med lange delte arbeidsbord, saccosekker og en sofa, åpen mot en terrasse',
  'Datorgenererad sällskapslounge med långa delade arbetsbord, sittsäckar och en soffa, öppen mot en terrass')
a('.media.items[15].caption',
  'El salón social y el coworking', 'Le salon commun et le coworking', 'Die Gemeinschaftslounge und der Coworking-Raum',
  'Общая гостиная и коворкинг', 'الصالة الاجتماعية ومساحة العمل المشترك', 'De sociale lounge en de coworkingruimte',
  'Salon wspólny i coworking', 'Fellesstuen og coworking-rommet', 'Sällskapsloungen och coworkingrummet')
a('.media.items[17].alt',
  'Green de putting generado por ordenador junto a un bloque de apartamentos, con dos jugadores, banderas, una hilera de cipreses y el mar a lo lejos',
  'Green d’entraînement au putting de synthèse le long d’un bâtiment d’appartements, avec deux joueurs, des drapeaux, une rangée de cyprès et la mer au loin',
  'Computergeneriertes Putting-Green entlang eines Wohngebäudes, mit zwei Spielern, Fahnen, einer Reihe Zypressen und dem Meer in der Ferne',
  'Компьютерная визуализация паттинг-грина вдоль жилого корпуса: два игрока, флажки, ряд кипарисов и море вдали',
  'ملعب تدريب على الضربات القصيرة مُنشأ بالحاسوب بمحاذاة مبنى شقق، مع لاعبَين وأعلام وصف من أشجار السرو والبحر في البعيد',
  'Computergegenereerde puttinggreen langs een blok appartementen, met twee spelers, vlaggen, een rij cipressen en de zee in de verte',
  'Wizualizacja komputerowa putting greenu wzdłuż budynku apartamentów, z dwoma graczami, flagami, rzędem cyprysów i morzem w oddali',
  'Datagenerert puttinggreen langs en leilighetsblokk, med to spillere, flagg, en rekke sypresser og havet i det fjerne',
  'Datorgenererad puttinggreen längs ett lägenhetshus, med två spelare, flaggor, en rad cypresser och havet i fjärran')
a('.media.items[17].caption',
  'El green de putting', 'Le green de putting', 'Das Putting-Green', 'Паттинг-грин', 'ملعب الضربات القصيرة',
  'De puttinggreen', 'Putting green', 'Puttinggreenen', 'Puttinggreenen')
a('.media.items[18].alt',
  'Mirador generado por ordenador bajo una pérgola cubierta de flores moradas, con una mesa y taburetes de madera y vistas sobre un campo de golf hacia las montañas',
  'Belvédère de synthèse sous une pergola couverte de fleurs violettes, avec une table et des tabourets en bois et une vue sur un golf vers les montagnes',
  'Computergenerierter Aussichtspunkt unter einer mit violetten Blüten bewachsenen Pergola, mit Holztisch und Hockern und Blick über einen Golfplatz auf die Berge',
  'Компьютерная визуализация смотровой площадки под перголой, увитой фиолетовыми цветами, с деревянным столом и табуретами и видом на гольф-поле и горы',
  'نقطة إطلالة مُنشأة بالحاسوب تحت عريشة مكسوّة بأزهار بنفسجية، مع طاولة ومقاعد خشبية وإطلالة على ملعب غولف باتجاه الجبال',
  'Computergegenereerd uitkijkpunt onder een pergola vol paarse bloemen, met een houten tafel en krukken en uitzicht over een golfbaan naar de bergen',
  'Wizualizacja komputerowa punktu widokowego pod pergolą porośniętą fioletowymi kwiatami, z drewnianym stołem i taboretami oraz widokiem na pole golfowe i góry',
  'Datagenerert utsiktspunkt under en pergola dekket av lilla blomster, med trebord og krakker og utsikt over en golfbane mot fjellene',
  'Datorgenererad utsiktsplats under en pergola täckt av lila blommor, med träbord och pallar och utsikt över en golfbana mot bergen')
a('.media.items[18].caption',
  'El mirador', 'Le belvédère', 'Der Aussichtspunkt', 'Смотровая площадка', 'نقطة الإطلالة', 'Het uitkijkpunt',
  'Punkt widokowy', 'Utsiktspunktet', 'Utsiktsplatsen')
a('.media.items[19].alt',
  'Garaje generado por ordenador con plazas numeradas, puertas de trasteros y un rótulo que indica la entrada a un portal',
  'Garage de synthèse avec des places numérotées, des portes de caves et un panneau indiquant l’entrée d’une cage d’escalier',
  'Computergenerierte Garage mit nummerierten Stellplätzen, Abstellraumtüren und einem Schild zum Eingang eines Aufgangs',
  'Компьютерная визуализация гаража с пронумерованными местами, дверями кладовых и указателем ко входу в подъезд',
  'مرآب مُنشأ بالحاسوب بمواقف مرقّمة وأبواب مخازن ولافتة تشير إلى مدخل أحد المباني',
  'Computergegenereerde garage met genummerde parkeerplaatsen, bergingsdeuren en een bord naar de ingang van een portiek',
  'Wizualizacja komputerowa garażu z numerowanymi miejscami, drzwiami komórek lokatorskich i oznaczeniem wejścia do klatki',
  'Datagenerert garasje med nummererte plasser, boddører og et skilt mot inngangen til en oppgang',
  'Datorgenererat garage med numrerade platser, förrådsdörrar och en skylt mot entrén till en uppgång')

# floorplan alts and captions
FP = {'es': ('Plano de la vivienda {}', 'Vivienda {}', ', con su solárium al lado', ' y su solárium'),
      'fr': ('Plan du logement {}', 'Logement {}', ', avec son solarium à côté', ' et son solarium'),
      'de': ('Grundriss der Wohnung {}', 'Wohnung {}', ', daneben ihr Solarium', ' und ihr Solarium'),
      'ru': ('Планировка квартиры {}', 'Квартира {}', ', рядом её солярий', ' и её солярий'),
      'ar': ('مخطط المسكن {}', 'المسكن {}', '، مع السولاريوم الخاص به بجانبه', ' والسولاريوم الخاص به'),
      'nl': ('Plattegrond van woning {}', 'Woning {}', ', met het solarium ernaast', ' en het solarium'),
      'pl': ('Rzut lokalu {}', 'Lokal {}', ', obok jego solarium', ' i jego solarium'),
      'no': ('Planløsning for bolig {}', 'Bolig {}', ', med solterrassen ved siden av', ' og solterrassen'),
      'sv': ('Planritning för bostad {}', 'Bostad {}', ', med solterrassen bredvid', ' och solterrassen')}
for it in proj['media']['items']:
    if it['category'] != 'Floorplans':
        continue
    ref = re.search(r'home (\d+)', it['alt']).group(1)
    sol = 'solarium' in it['alt']
    T[it['alt']] = {l: FP[l][0].format(ref) + (FP[l][2] if sol else '') for l in LOCS}
    T[it['caption']] = {l: FP[l][1].format(ref) + (FP[l][3] if sol else '') for l in LOCS}

# ---- overview, why ---------------------------------------------------------------------------

a('.overview.headlineHtml',
  'Una ladera de 120 viviendas, <em>diez en la lista</em>', 'Un coteau de 120 logements, <em>dix sur la liste</em>',
  'Ein Hang mit 120 Wohnungen, <em>zehn auf der Liste</em>', 'Склон со 120 квартирами, <em>десять в списке</em>',
  'سفح من 120 مسكناً، <em>عشرة منها في القائمة</em>', 'Een helling met 120 woningen, <em>tien op de lijst</em>',
  'Zbocze ze 120 lokalami, <em>dziesięć w cenniku</em>', 'En åsside med 120 boliger, <em>ti på listen</em>',
  'En sluttning med 120 bostäder, <em>tio på listan</em>')
a('.overview.copy[0]',
  'Retama Residences es una promoción cerrada de 120 viviendas en bloques bajos sobre una parcela de {N31,000} {U} en Mijas Costa, entre los campos de golf de Cerrado del Águila y Chaparral. El folleto dispone los edificios alrededor de un gran jardín, con caminos que los unen con las zonas comunes y con un mirador, y deja parte de la parcela como terreno natural.',
  'Retama Residences est une résidence fermée de 120 logements en bâtiments bas sur un terrain de {N31,000} {U} à Mijas Costa, entre les golfs de Cerrado del Águila et de Chaparral. La brochure dispose les bâtiments autour d’un grand jardin, avec des allées qui les relient aux espaces communs et à un belvédère, et laisse une partie du terrain à l’état naturel.',
  'Retama Residences ist eine geschlossene Anlage mit 120 Wohnungen in niedrigen Gebäuden auf einem Grundstück von {N31,000} {U} in Mijas Costa, zwischen den Golfplätzen Cerrado del Águila und Chaparral. Die Broschüre ordnet die Gebäude um einen großen Garten an, mit Wegen zu den Gemeinschaftsbereichen und zu einem Aussichtspunkt, und lässt einen Teil des Grundstücks als Naturfläche.',
  'Retama Residences — закрытый комплекс из 120 квартир в невысоких корпусах на участке площадью {N31,000} {U} в Михас-Коста, между гольф-полями Cerrado del Águila и Chaparral. По буклету здания расположены вокруг большого сада, дорожки ведут от них к общим зонам и к смотровой площадке, а часть участка остаётся природной территорией.',
  'Retama Residences مجمّع مغلق من 120 مسكناً في مبانٍ منخفضة على قطعة أرض مساحتها {N31,000} {U} في ميخاس كوستا، بين ملعبي غولف Cerrado del Águila وChaparral. ويرتّب الكتيّب المباني حول حديقة كبيرة، تربطها ممرات بالمرافق المشتركة وبنقطة إطلالة، ويترك جزءاً من الأرض منطقة طبيعية.',
  'Retama Residences is een afgesloten complex van 120 woningen in lage blokken op een perceel van {N31,000} {U} in Mijas Costa, tussen de golfbanen van Cerrado del Águila en Chaparral. De brochure groepeert de gebouwen rond een grote tuin, met paden naar de gemeenschappelijke ruimtes en naar een uitkijkpunt, en laat een deel van het perceel als natuurterrein.',
  'Retama Residences to zamknięte osiedle 120 lokali w niskich budynkach na działce o powierzchni {N31,000} {U} w Mijas Costa, między polami golfowymi Cerrado del Águila i Chaparral. Według broszury budynki otaczają duży ogród, ścieżki łączą je z częściami wspólnymi i z punktem widokowym, a część działki pozostaje terenem naturalnym.',
  'Retama Residences er et inngjerdet anlegg med 120 boliger i lave blokker på en tomt på {N31,000} {U} i Mijas Costa, mellom golfbanene Cerrado del Águila og Chaparral. Brosjyren plasserer bygningene rundt en stor hage, med stier til fellesområdene og et utsiktspunkt, og lar en del av tomten være naturområde.',
  'Retama Residences är ett inhägnat område med 120 bostäder i låga hus på en tomt om {N31,000} {U} i Mijas Costa, mellan golfbanorna Cerrado del Águila och Chaparral. Broschyren placerar husen kring en stor trädgård, med gångar till de gemensamma ytorna och en utsiktsplats, och låter en del av tomten vara naturmark.')
a('.overview.copy[1]',
  'La lista de precios del promotor del 14 de septiembre de 2026 muestra diez viviendas, todas disponibles: apartamentos de uno a tres dormitorios en planta baja, primera y segunda desde {E341000}, y tres áticos con grandes terrazas de {E780000} a {E885000}, todo antes de {T}. El portal del promotor indica la licencia de obra como concedida, el inicio de las obras el 11 de noviembre de 2025 y la entrega en septiembre de 2028.',
  'La liste de prix du promoteur du 14 septembre 2026 présente dix logements, tous disponibles : des appartements d’une à trois chambres au rez-de-chaussée, au premier et au deuxième étage à partir de {E341000}, et trois penthouses avec de grandes terrasses de {E780000} à {E885000}, le tout hors {T}. Le portail du promoteur indique le permis de construire comme accordé, le début des travaux le 11 novembre 2025 et la livraison en septembre 2028.',
  'Die Preisliste des Bauträgers vom 14. September 2026 zeigt zehn Wohnungen, alle verfügbar: Wohnungen mit einem bis drei Schlafzimmern im Erdgeschoss, im ersten und im zweiten Obergeschoss ab {E341000} und drei Penthouses mit großen Terrassen von {E780000} bis {E885000}, alles vor {T}. Das Portal des Bauträgers nennt die Baugenehmigung als erteilt, den Baubeginn am 11. November 2025 und die Fertigstellung im September 2028.',
  'В прайс-листе застройщика от 14 сентября 2026 года десять квартир, все доступны: квартиры с одной–тремя спальнями на первом, втором и третьем этажах от {E341000} и три пентхауса с большими террасами от {E780000} до {E885000}, всё без {T}. На портале застройщика указано, что разрешение на строительство получено, работы начались 11 ноября 2025 года, а сдача — в сентябре 2028 года.',
  'تعرض قائمة أسعار المطوّر بتاريخ 14 سبتمبر 2026 عشرة مساكن، كلها متاحة: شقق بغرفة إلى ثلاث غرف نوم في الطابق الأرضي والأول والثاني ابتداءً من {E341000}، وثلاث شقق بنتهاوس بتراسات كبيرة من {E780000} إلى {E885000}، وكلها قبل {T}. وتذكر بوابة المطوّر أن رخصة البناء ممنوحة، وأن الأعمال بدأت في 11 نوفمبر 2025، وأن الإنجاز في سبتمبر 2028.',
  'De prijslijst van de ontwikkelaar van 14 september 2026 toont tien woningen, alle beschikbaar: appartementen met één tot drie slaapkamers op de begane grond, de eerste en de tweede verdieping vanaf {E341000}, en drie penthouses met grote terrassen van {E780000} tot {E885000}, alles vóór {T}. Het portaal van de ontwikkelaar vermeldt de bouwvergunning als verleend, de start van de werken op 11 november 2025 en de oplevering in september 2028.',
  'Cennik dewelopera z 14 września 2026 r. obejmuje dziesięć lokali, wszystkie dostępne: mieszkania z jedną do trzech sypialni na parterze, pierwszym i drugim piętrze od {E341000} oraz trzy penthouse’y z dużymi tarasami od {E780000} do {E885000}, wszystko przed {T}. Portal dewelopera podaje, że pozwolenie na budowę zostało wydane, prace ruszyły 11 listopada 2025 r., a odbiór przewidziano na wrzesień 2028 r.',
  'Utbyggerens prisliste av 14. september 2026 viser ti boliger, alle ledige: leiligheter med ett til tre soverom i første, andre og tredje etasje fra {E341000}, og tre toppleiligheter med store terrasser fra {E780000} til {E885000}, alt før {T}. Utbyggerens portal oppgir byggetillatelsen som gitt, byggestart 11. november 2025 og ferdigstillelse i september 2028.',
  'Exploatörens prislista av den 14 september 2026 visar tio bostäder, alla lediga: lägenheter med ett till tre sovrum på bottenvåningen, första och andra våningen från {E341000}, och tre takvåningar med stora terrasser från {E780000} till {E885000}, allt före {T}. Exploatörens portal anger bygglovet som beviljat, byggstarten den 11 november 2025 och färdigställandet i september 2028.')
a('.overview.metrics[0][1]',
  '120 viviendas', '120 logements', '120 Wohnungen', '120 квартир', '120 مسكناً', '120 woningen', '120 lokali', '120 boliger', '120 bostäder')

a('.why.copy',
  'Viviendas nuevas ya en construcción, spa, gimnasio y dos piscinas en la propia promoción, una plaza de garaje y un trastero numerados junto a cada precio, y el 60 % del precio para la escritura.',
  'Des logements neufs déjà en construction, un spa, une salle de sport et deux piscines sur place, une place de parking et une cave numérotées à côté de chaque prix, et 60 % du prix à l’acte.',
  'Neue Wohnungen, die bereits gebaut werden, Spa, Fitnessraum und zwei Pools in der Anlage, ein Stellplatz und ein Abstellraum mit Nummer neben jedem Preis, und 60 % des Preises erst bei der Beurkundung.',
  'Новые квартиры, которые уже строятся, спа, тренажёрный зал и два бассейна на территории, машино-место и кладовая с номерами рядом с каждой ценой и 60 % цены при подписании купчей.',
  'مساكن جديدة قيد الإنشاء فعلاً، وسبا وصالة رياضية ومسبحان داخل المجمّع، وموقف سيارة ومخزن مرقّمان بجانب كل سعر، و60% من السعر عند توقيع سند الملكية.',
  'Nieuwe woningen die al in aanbouw zijn, een spa, een fitnessruimte en twee zwembaden op het terrein, een genummerde parkeerplaats en berging naast elke prijs, en 60 % van de prijs bij de akte.',
  'Nowe lokale już w budowie, spa, siłownia i dwa baseny na terenie osiedla, numerowane miejsce w garażu i komórka przy każdej cenie oraz 60% ceny przy akcie notarialnym.',
  'Nye boliger som allerede er under bygging, spa, treningsrom og to bassenger i anlegget, en nummerert garasjeplass og bod ved hver pris, og 60 % av prisen ved skjøtet.',
  'Nya bostäder som redan byggs, spa, gym och två pooler i området, en numrerad garageplats och ett förråd vid varje pris, och 60 % av priset vid köpebrevet.')
a('.why.points[0][1]',
  'Compradores que buscan un apartamento o ático nuevo en Mijas Costa como vivienda habitual o segunda residencia, con los servicios de un resort dentro de una promoción cerrada.',
  'Les acquéreurs qui cherchent un appartement ou un penthouse neuf à Mijas Costa comme résidence principale ou secondaire, avec les services d’un resort dans une résidence fermée.',
  'Käufer, die eine neue Wohnung oder ein Penthouse in Mijas Costa als Hauptwohnsitz oder Zweitwohnung suchen, mit den Einrichtungen eines Resorts in einer geschlossenen Anlage.',
  'Покупатели, которым нужна новая квартира или пентхаус в Михас-Коста для постоянной жизни или как второй дом, с инфраструктурой курорта в закрытом комплексе.',
  'المشترون الذين يبحثون عن شقة أو بنتهاوس جديد في ميخاس كوستا للسكن الدائم أو كمنزل ثانٍ، مع مرافق منتجع داخل مجمّع مغلق.',
  'Kopers die een nieuw appartement of penthouse in Mijas Costa zoeken om er te wonen of als tweede woning, met de voorzieningen van een resort binnen een afgesloten complex.',
  'Kupujący, którzy szukają nowego mieszkania lub penthouse’u w Mijas Costa do stałego zamieszkania lub jako drugiego domu, z udogodnieniami resortu na zamkniętym osiedlu.',
  'Kjøpere som ønsker en ny leilighet eller toppleilighet i Mijas Costa å bo i eller som feriebolig, med fasilitetene til et feriested i et inngjerdet anlegg.',
  'Köpare som söker en ny lägenhet eller takvåning i Mijas Costa att bo i eller som fritidsbostad, med en resorts faciliteter i ett inhägnat område.')
a('.why.points[1][0]',
  'Las obras ya han empezado', 'Les travaux ont commencé', 'Der Bau hat begonnen', 'Строительство уже началось', 'بدأ البناء',
  'De bouw is begonnen', 'Budowa już trwa', 'Byggingen er i gang', 'Bygget har börjat')
a('.why.points[1][1]',
  'El portal del promotor indica la licencia de obra como concedida y las obras como iniciadas el 11 de noviembre de 2025, con entrega en septiembre de 2028.',
  'Le portail du promoteur indique le permis de construire comme accordé et les travaux comme commencés le 11 novembre 2025, avec une livraison en septembre 2028.',
  'Das Portal des Bauträgers nennt die Baugenehmigung als erteilt und den Baubeginn am 11. November 2025, mit Fertigstellung im September 2028.',
  'На портале застройщика указано, что разрешение на строительство получено, а работы начались 11 ноября 2025 года; сдача — в сентябре 2028 года.',
  'تذكر بوابة المطوّر أن رخصة البناء ممنوحة وأن الأعمال بدأت في 11 نوفمبر 2025، مع الإنجاز في سبتمبر 2028.',
  'Het portaal van de ontwikkelaar vermeldt de bouwvergunning als verleend en de werken als gestart op 11 november 2025, met oplevering in september 2028.',
  'Portal dewelopera podaje, że pozwolenie na budowę zostało wydane, a prace ruszyły 11 listopada 2025 r.; odbiór we wrześniu 2028 r.',
  'Utbyggerens portal oppgir byggetillatelsen som gitt og byggestart 11. november 2025, med ferdigstillelse i september 2028.',
  'Exploatörens portal anger bygglovet som beviljat och byggstarten den 11 november 2025, med färdigställande i september 2028.')
a('.why.points[2][0]',
  'Más que una piscina', 'Plus qu’une piscine', 'Mehr als ein Pool', 'Больше, чем бассейн', 'أكثر من مسبح',
  'Meer dan een zwembad', 'Więcej niż basen', 'Mer enn et basseng', 'Mer än en pool')
a('.why.points[2][1]',
  'Un spa con piscina climatizada y sauna, gimnasio, salón de coworking, green de putting y una pista de arena para vóley playa y pádel playa, tal como los recogen los documentos del promotor.',
  'Un spa avec piscine chauffée et sauna, une salle de sport, un espace de coworking, un green de putting et un terrain de sable pour le beach-volley et le beach-tennis, tels que les documents du promoteur les énumèrent.',
  'Ein Spa mit beheiztem Pool und Sauna, ein Fitnessraum, eine Coworking-Lounge, ein Putting-Green und ein Sandplatz für Beachvolleyball und Beach-Paddle, wie die Unterlagen des Bauträgers sie aufführen.',
  'Спа с подогреваемым бассейном и сауной, тренажёрный зал, коворкинг, паттинг-грин и песчаная площадка для пляжного волейбола и пляжного падела — так их перечисляют документы застройщика.',
  'سبا بمسبح مُدفّأ وساونا، وصالة رياضية، وصالة للعمل المشترك، وملعب للضربات القصيرة، وملعب رملي للكرة الطائرة الشاطئية والبادل الشاطئي، كما تذكرها وثائق المطوّر.',
  'Een spa met verwarmd zwembad en sauna, een fitnessruimte, een coworkinglounge, een puttinggreen en een zandveld voor beachvolleybal en beachpaddle, zoals de documenten van de ontwikkelaar ze opsommen.',
  'Spa z podgrzewanym basenem i sauną, siłownia, strefa coworkingu, putting green i piaszczyste boisko do siatkówki plażowej i plażowego padla — tak wymieniają je dokumenty dewelopera.',
  'Et spa med oppvarmet basseng og badstue, treningsrom, en coworking-lounge, en puttinggreen og en sandbane for sandvolleyball og strandpadel, slik utbyggerens dokumenter lister dem opp.',
  'Ett spa med uppvärmd pool och bastu, gym, en coworkinglounge, en puttinggreen och en sandplan för beachvolley och beachpaddel, så som exploatörens handlingar räknar upp dem.')
a('.why.points[3][1]',
  'Tras una reserva de {E10000}, el 30 % se paga en el contrato privado y el 10 % seis meses después; el 60 % restante se abona con la licencia de primera ocupación y la escritura. A cada pago se le suma el {T}.',
  'Après une réservation de {E10000}, 30 % sont dus au contrat privé et 10 % six mois plus tard ; les 60 % restants sont dus à la licence de première occupation et à l’acte. La {T} s’ajoute à chaque paiement.',
  'Nach einer Reservierung von {E10000} sind 30 % beim privaten Kaufvertrag und 10 % sechs Monate später fällig; die übrigen 60 % bei der Erstbezugsgenehmigung und der Beurkundung. Auf jede Zahlung kommt die {T}.',
  'После брони в {E10000} 30 % платятся при частном договоре и 10 % через шесть месяцев; остальные 60 % — при получении лицензии на первое заселение и подписании купчей. К каждому платежу добавляется {T}.',
  'بعد حجز بقيمة {E10000}، تُدفع 30% عند العقد الخاص و10% بعد ستة أشهر، وتُستحق الـ60% المتبقية عند رخصة الإشغال الأول وتوقيع سند الملكية. وتُضاف {T} إلى كل دفعة.',
  'Na een reservering van {E10000} valt 30 % bij het koopcontract en 10 % zes maanden later; de resterende 60 % is verschuldigd bij de vergunning voor eerste bewoning en de akte. Op elke betaling komt {T}.',
  'Po rezerwacji w wysokości {E10000} 30% płaci się przy umowie prywatnej, a 10% sześć miesięcy później; pozostałe 60% przy pozwoleniu na pierwsze użytkowanie i akcie notarialnym. Do każdej płatności dolicza się {T}.',
  'Etter en reservasjon på {E10000} betales 30 % ved den private kontrakten og 10 % seks måneder senere; de resterende 60 % forfaller ved brukstillatelsen og skjøtet. Det kommer {T} på hver betaling.',
  'Efter en reservation på {E10000} betalas 30 % vid det privata köpekontraktet och 10 % sex månader senare; resterande 60 % förfaller vid inflyttningslicensen och köpebrevet. {T} tillkommer på varje betalning.')

# ---- architecture ----------------------------------------------------------------------------

a('.architecture.headlineHtml',
  'Bloques bajos <em>alrededor de un jardín</em>', 'Des bâtiments bas <em>autour d’un jardin</em>', 'Niedrige Gebäude <em>um einen Garten</em>',
  'Невысокие корпуса <em>вокруг сада</em>', 'مبانٍ منخفضة <em>حول حديقة</em>', 'Lage blokken <em>rond een tuin</em>',
  'Niskie budynki <em>wokół ogrodu</em>', 'Lave blokker <em>rundt en hage</em>', 'Låga hus <em>kring en trädgård</em>')
a('.architecture.copy[0]',
  'El folleto describe edificios de poco volumen dispuestos alrededor de un gran espacio verde, con el jardín como protagonista y caminos que lo atraviesan hacia las zonas comunes y un mirador. En las imágenes, los bloques tienen terrazas profundas con barandillas de cristal, pérgolas de lamas y muros color piedra, entre olivos, lavanda y gramíneas.',
  'La brochure décrit des bâtiments de faible volume disposés autour d’un grand espace vert, le jardin étant l’élément principal, traversé d’allées vers les espaces communs et un belvédère. Sur les visuels, les bâtiments ont des terrasses profondes avec garde-corps en verre, des pergolas à lames et des murs couleur pierre, parmi les oliviers, la lavande et les graminées.',
  'Die Broschüre beschreibt Gebäude mit geringem Volumen um eine große Grünfläche, mit dem Garten als Hauptelement und Wegen durch ihn zu den Gemeinschaftsbereichen und einem Aussichtspunkt. In den Visualisierungen haben die Gebäude tiefe Terrassen mit Glasbrüstungen, Lamellenpergolen und steinfarbene Wände, zwischen Olivenbäumen, Lavendel und Gräsern.',
  'Буклет описывает невысокие здания вокруг большого зелёного пространства: главную роль играет сад, через который дорожки ведут к общим зонам и смотровой площадке. На визуализациях у корпусов глубокие террасы со стеклянными ограждениями, ламельные перголы и стены песочного цвета среди олив, лаванды и злаков.',
  'يصف الكتيّب مباني قليلة الارتفاع موزّعة حول مساحة خضراء كبيرة، تكون فيها الحديقة العنصر الرئيسي وتعبرها ممرات نحو المرافق المشتركة ونقطة إطلالة. وفي الصور تظهر المباني بتراسات عميقة ودرابزين زجاجي وعرائش من الشرائح وجدران بلون الحجر، بين أشجار الزيتون والخزامى والأعشاب.',
  'De brochure beschrijft gebouwen met een klein volume rond een grote groene ruimte, met de tuin als middelpunt en paden erdoorheen naar de gemeenschappelijke ruimtes en een uitkijkpunt. Op de beelden hebben de blokken diepe terrassen met glazen balustrades, lamellenpergola’s en steenkleurige muren, tussen olijfbomen, lavendel en siergrassen.',
  'Broszura opisuje niewielkie bryły rozmieszczone wokół dużej przestrzeni zielonej, z ogrodem jako głównym elementem i ścieżkami prowadzącymi przez niego do części wspólnych i punktu widokowego. Na wizualizacjach budynki mają głębokie tarasy ze szklanymi balustradami, pergole lamelowe i ściany w kolorze kamienia, wśród drzew oliwnych, lawendy i traw.',
  'Brosjyren beskriver bygninger med lite volum rundt et stort grøntområde, med hagen som hovedelement og stier gjennom den til fellesområdene og et utsiktspunkt. På bildene har blokkene dype terrasser med glassrekkverk, lamellpergolaer og steinfargede vegger, blant oliventrær, lavendel og gress.',
  'Broschyren beskriver byggnader med liten volym kring en stor grönyta, med trädgården som huvudsak och gångar genom den till de gemensamma ytorna och en utsiktsplats. På bilderna har husen djupa terrasser med glasräcken, lamellpergolor och stenfärgade väggar, bland olivträd, lavendel och gräs.')
a('.architecture.copy[1]',
  'El plano de conjunto numera nueve portales, y la lista de precios nombra cuatro niveles: planta baja, primera planta, segunda planta y ático. Dos de los áticos de la lista suman un solárium sobre la vivienda, al que en los planos se sube por una escalera de caracol.',
  'Le plan de masse numérote neuf cages d’escalier, et la liste de prix nomme quatre niveaux : rez-de-chaussée, premier étage, deuxième étage et penthouse. Deux des penthouses de la liste ajoutent un solarium au-dessus du logement, accessible sur les plans par un escalier en colimaçon.',
  'Der Lageplan nummeriert neun Aufgänge, und die Preisliste nennt vier Ebenen: Erdgeschoss, erstes Obergeschoss, zweites Obergeschoss und Penthouse. Zwei der gelisteten Penthouses haben zusätzlich ein Solarium über der Wohnung, das auf den Plänen über eine Wendeltreppe erreicht wird.',
  'На генплане пронумерованы девять подъездов, а в прайс-листе названы четыре уровня: первый, второй и третий этажи и пентхаус. У двух пентхаусов из списка над квартирой есть ещё солярий, на планах на него ведёт винтовая лестница.',
  'يرقّم المخطط العام تسعة مداخل، وتذكر قائمة الأسعار أربعة مستويات: الطابق الأرضي والأول والثاني والبنتهاوس. ويضيف اثنان من البنتهاوس المدرجين سولاريوم فوق المسكن، يُصعد إليه في المخططات عبر درج حلزوني.',
  'De situatietekening nummert negen portieken, en de prijslijst noemt vier niveaus: begane grond, eerste verdieping, tweede verdieping en penthouse. Twee van de penthouses op de lijst hebben daarbovenop een solarium, op de plattegronden bereikbaar via een wenteltrap.',
  'Plan zagospodarowania numeruje dziewięć klatek, a cennik wymienia cztery poziomy: parter, pierwsze piętro, drugie piętro i penthouse. Dwa penthouse’y z cennika mają dodatkowo solarium nad mieszkaniem, na które według rzutów prowadzą kręcone schody.',
  'Situasjonsplanen nummererer ni oppganger, og prislisten nevner fire nivåer: første etasje, andre etasje, tredje etasje og toppleilighet. To av toppleilighetene på listen har i tillegg en solterrasse over boligen, som tegningene viser med en vindeltrapp opp.',
  'Situationsplanen numrerar nio uppgångar, och prislistan nämner fyra plan: bottenvåning, första våningen, andra våningen och takvåning. Två av takvåningarna på listan har dessutom en solterrass ovanför bostaden, som ritningarna visar nås via en spiraltrappa.')
a('.architecture.highlights[0]',
  'Un recinto vallado y cerrado, con control de acceso para peatones y vehículos y circuito cerrado de televisión.',
  'Un ensemble clos et clôturé, avec contrôle d’accès pour piétons et véhicules et vidéosurveillance.',
  'Ein eingezäunter, geschlossener Komplex mit Zugangskontrolle für Fußgänger und Fahrzeuge und Videoüberwachung.',
  'Огороженная закрытая территория с контролем доступа для пешеходов и автомобилей и видеонаблюдением.',
  'مجمّع مسوّر ومغلق، مع نظام تحكم في دخول المشاة والمركبات ودائرة تلفزيونية مغلقة.',
  'Een omheind en afgesloten complex met toegangscontrole voor voetgangers en voertuigen en camerabewaking.',
  'Ogrodzony i zamknięty teren z kontrolą dostępu dla pieszych i pojazdów oraz monitoringiem.',
  'Et inngjerdet og lukket anlegg med adgangskontroll for gående og kjøretøy og videoovervåking.',
  'Ett inhägnat och slutet område med passerkontroll för gående och fordon och kameraövervakning.')
a('.architecture.highlights[1]',
  'Ascensores eléctricos para ocho personas a todas las plantas, con puertas automáticas de acero inoxidable y aptos para personas con movilidad reducida.',
  'Des ascenseurs électriques pour huit personnes desservant tous les étages, avec portes automatiques en inox, adaptés aux personnes à mobilité réduite.',
  'Elektrische Aufzüge für acht Personen in alle Geschosse, mit automatischen Edelstahltüren und geeignet für Menschen mit eingeschränkter Mobilität.',
  'Электрические лифты на восемь человек на все этажи, с автоматическими дверями из нержавеющей стали, приспособленные для людей с ограниченной подвижностью.',
  'مصاعد كهربائية لثمانية أشخاص إلى جميع الطوابق، بأبواب أوتوماتيكية من الفولاذ المقاوم للصدأ، ومناسبة لذوي الحركة المحدودة.',
  'Elektrische liften voor acht personen naar alle verdiepingen, met automatische roestvrijstalen deuren, geschikt voor mensen met beperkte mobiliteit.',
  'Elektryczne windy dla ośmiu osób na wszystkie piętra, z automatycznymi drzwiami ze stali nierdzewnej, przystosowane dla osób o ograniczonej mobilności.',
  'Elektriske heiser for åtte personer til alle etasjer, med automatiske dører i rustfritt stål, tilpasset personer med nedsatt bevegelighet.',
  'Elektriska hissar för åtta personer till alla våningar, med automatiska dörrar i rostfritt stål, anpassade för personer med nedsatt rörlighet.')
a('.architecture.highlights[2]',
  'Puerta de garaje automática con mando a distancia y preinstalación para cargar un vehículo eléctrico desde el contador de la propia vivienda.',
  'Une porte de garage automatique avec télécommande et une pré-installation pour recharger un véhicule électrique depuis le compteur du logement.',
  'Ein automatisches Garagentor mit Fernbedienung und eine Vorinstallation zum Laden eines Elektroautos über den Zähler der eigenen Wohnung.',
  'Автоматические ворота гаража с пультом и подготовка для зарядки электромобиля от собственного счётчика квартиры.',
  'باب مرآب آلي بجهاز تحكم عن بُعد، وتمديدات مسبقة لشحن سيارة كهربائية من عدّاد المسكن نفسه.',
  'Een automatische garagedeur met afstandsbediening en een voorbereiding om een elektrische auto te laden via de eigen meter van de woning.',
  'Automatyczna brama garażowa z pilotem i przygotowanie do ładowania samochodu elektrycznego z licznika własnego lokalu.',
  'Automatisk garasjeport med fjernkontroll og forberedelse for lading av elbil fra boligens egen måler.',
  'En automatisk garageport med fjärrkontroll och förberedelse för laddning av elbil från bostadens egen elmätare.')
a('.architecture.highlights[3]',
  'Ventanas de aluminio con rotura de puente térmico y vidrio bajo emisivo, y paneles fotovoltaicos en las cubiertas del aparcamiento para las zonas comunes.',
  'Des fenêtres en aluminium à rupture de pont thermique et vitrage à faible émissivité, et des panneaux photovoltaïques sur les toits du parking pour les espaces communs.',
  'Aluminiumfenster mit thermischer Trennung und Low-E-Verglasung sowie Photovoltaikmodule auf den Dächern des Parkplatzes für die Gemeinschaftsbereiche.',
  'Алюминиевые окна с терморазрывом и низкоэмиссионным остеклением, а также солнечные панели на крышах парковки для общих зон.',
  'نوافذ ألومنيوم بعازل حراري وزجاج منخفض الانبعاث، وألواح كهروضوئية على أسطح موقف السيارات لتغذية المرافق المشتركة.',
  'Aluminium ramen met thermische onderbreking en laagemissieglas, en zonnepanelen op de daken van het parkeerterrein voor de gemeenschappelijke ruimtes.',
  'Aluminiowe okna z przekładką termiczną i szybami niskoemisyjnymi oraz panele fotowoltaiczne na dachach parkingu zasilające części wspólne.',
  'Aluminiumsvinduer med kuldebrudd og lavemisjonsglass, og solcellepaneler på takene over parkeringen til fellesområdene.',
  'Aluminiumfönster med köldbrygga och lågemissionsglas, och solceller på parkeringens tak för de gemensamma ytorna.')

# ---- quality specs ---------------------------------------------------------------------------

a('.qualitySpecs.sourceNote',
  'Fuente: la memoria de calidades del promotor, en inglés y en español, sin fecha impresa. Indica que los acabados pueden modificarse o sustituirse por elementos de igual o superior calidad, y que el mobiliario, la decoración y la vegetación de las imágenes no forman parte de la oferta.',
  'Source : le descriptif des prestations du promoteur, en anglais et en espagnol, sans date imprimée. Il précise que les finitions peuvent être modifiées ou remplacées par des éléments de qualité égale ou supérieure, et que le mobilier, la décoration et la végétation des visuels ne font pas partie de l’offre.',
  'Quelle: die Baubeschreibung des Bauträgers, auf Englisch und Spanisch, ohne aufgedrucktes Datum. Sie hält fest, dass die Ausstattung geändert oder durch gleich- oder höherwertige Elemente ersetzt werden kann und dass Möbel, Dekoration und Bepflanzung auf den Bildern nicht zum Angebot gehören.',
  'Источник: спецификация застройщика на английском и испанском языках без указанной даты. В ней сказано, что отделка может быть изменена или заменена элементами равного или более высокого качества, а мебель, декор и растения на изображениях не входят в предложение.',
  'المصدر: مواصفات البناء الصادرة عن المطوّر، بالإنجليزية والإسبانية، دون تاريخ مطبوع. وتذكر أن التشطيبات قد تُعدَّل أو تُستبدل بعناصر مماثلة الجودة أو أعلى، وأن الأثاث والديكور والنباتات في الصور ليست جزءاً من العرض.',
  'Bron: de technische beschrijving van de ontwikkelaar, in het Engels en het Spaans, zonder gedrukte datum. Daarin staat dat de afwerking kan worden gewijzigd of vervangen door elementen van gelijke of hogere kwaliteit, en dat het meubilair, de decoratie en de beplanting op de beelden niet bij het aanbod horen.',
  'Źródło: specyfikacja techniczna dewelopera, po angielsku i hiszpańsku, bez wydrukowanej daty. Zaznacza ona, że wykończenia mogą zostać zmienione lub zastąpione elementami o tej samej lub wyższej jakości, a meble, dekoracje i roślinność z wizualizacji nie są częścią oferty.',
  'Kilde: utbyggerens byggebeskrivelse, på engelsk og spansk, uten trykt dato. Den sier at utførelsen kan endres eller erstattes med elementer av samme eller høyere kvalitet, og at møbler, dekor og beplantning på bildene ikke er en del av tilbudet.',
  'Källa: exploatörens byggbeskrivning, på engelska och spanska, utan tryckt datum. Den anger att utförandet kan ändras eller ersättas med element av samma eller högre kvalitet, och att möbler, inredning och växter på bilderna inte ingår i erbjudandet.')
a('.qualitySpecs.groups[0].name',
  'Fachada y estructura', 'Façade et structure', 'Fassade und Tragwerk', 'Фасад и конструкция', 'الواجهة والهيكل',
  'Gevel en draagstructuur', 'Elewacja i konstrukcja', 'Fasade og konstruksjon', 'Fasad och stomme')
a('.qualitySpecs.groups[0].items[0]',
  'Estructura de hormigón armado y fachada de doble hoja de ladrillo perforado enfoscado, con aislamiento de poliuretano proyectado, trasdosada por dentro con placa de yeso laminado y lana mineral.',
  'Une structure en béton armé et une façade à double paroi en brique perforée enduite, isolée au polyuréthane projeté, doublée à l’intérieur de plaques de plâtre et de laine minérale.',
  'Ein Tragwerk aus Stahlbeton und eine zweischalige Fassade aus verputztem Lochziegel mit Spritzschaum-Polyurethan-Dämmung, innen mit Gipskarton und Mineralwolle verkleidet.',
  'Каркас из монолитного железобетона и двухслойный фасад из оштукатуренного пустотелого кирпича с напылённым пенополиуретаном, изнутри облицованный гипсокартоном с минеральной ватой.',
  'هيكل من الخرسانة المسلحة وواجهة مزدوجة من الطوب المثقوب المكسو بالملاط مع عزل من البولي يوريثان المرشوش، ومبطّنة من الداخل بألواح الجبس والصوف المعدني.',
  'Een draagstructuur van gewapend beton en een dubbelwandige gevel van bepleisterde geperforeerde baksteen met gespoten polyurethaanisolatie, binnen afgewerkt met gipsplaat en minerale wol.',
  'Konstrukcja żelbetowa i dwuwarstwowa elewacja z tynkowanej cegły dziurawki z natryskową izolacją poliuretanową, od wewnątrz okładzina z płyt gipsowo-kartonowych i wełny mineralnej.',
  'Bærekonstruksjon i armert betong og en todelt fasade av pusset hulltegl med sprøytet polyuretanisolasjon, kledd innvendig med gipsplater og mineralull.',
  'En stomme av armerad betong och en dubbelväggig fasad av putsat håltegel med sprutad polyuretanisolering, invändigt klädd med gipsskivor och mineralull.')
a('.qualitySpecs.groups[0].items[1]',
  'Triple tabique entre viviendas, con membrana acústica, y tabiques de placa de yeso laminado con aislamiento de lana mineral dentro de cada vivienda.',
  'Des cloisons triples entre logements, avec membrane acoustique, et des cloisons en plaques de plâtre isolées à la laine minérale à l’intérieur de chaque logement.',
  'Dreifache Trennwände zwischen den Wohnungen mit Schallschutzmembran und Gipskarton-Trennwände mit Mineralwolldämmung innerhalb jeder Wohnung.',
  'Тройные стены между квартирами с акустической мембраной и перегородки из гипсокартона с минеральной ватой внутри каждой квартиры.',
  'جدران فاصلة ثلاثية بين المساكن مع غشاء صوتي، وقواطع من ألواح الجبس معزولة بالصوف المعدني داخل كل مسكن.',
  'Drievoudige scheidingswanden tussen de woningen met een akoestisch membraan, en binnenwanden van gipsplaat met isolatie van minerale wol in elke woning.',
  'Potrójne ściany między lokalami z membraną akustyczną oraz ścianki działowe z płyt gipsowo-kartonowych z wełną mineralną wewnątrz każdego lokalu.',
  'Tredobbelte skillevegger mellom boligene med akustisk membran, og innervegger av gipsplater med mineralullisolasjon i hver bolig.',
  'Tredubbla skiljeväggar mellan bostäderna med akustiskt membran, och innerväggar av gipsskivor med mineralullsisolering i varje bostad.')
a('.qualitySpecs.groups[1].items[0]',
  'Suelos de gres porcelánico de gran formato en toda la vivienda, con rodapié lacado en blanco, y gres antideslizante del mismo modelo en las terrazas.',
  'Des sols en grès cérame grand format dans tout le logement, avec plinthes laquées blanc, et du grès antidérapant du même modèle sur les terrasses.',
  'Großformatige Feinsteinzeugböden in der gesamten Wohnung mit weiß lackierten Sockelleisten und rutschfestes Feinsteinzeug desselben Modells auf den Terrassen.',
  'Крупноформатный керамогранит на полу во всей квартире с белыми лакированными плинтусами и нескользящий керамогранит той же модели на террасах.',
  'أرضيات من البورسلين بقياس كبير في كامل المسكن مع وزرات مطلية بالأبيض، وبورسلين مانع للانزلاق من الطراز نفسه على التراسات.',
  'Vloeren van grootformaat keramische tegels in de hele woning met wit gelakte plinten, en antislip tegels van hetzelfde model op de terrassen.',
  'Wielkoformatowe płytki gresowe na podłogach w całym lokalu z białymi lakierowanymi listwami oraz antypoślizgowy gres tego samego modelu na tarasach.',
  'Storformat porselensfliser på gulvene i hele boligen med hvitlakkerte gulvlister, og sklisikre fliser av samme modell på terrassene.',
  'Storformatigt klinker på golven i hela bostaden med vitlackade golvlister, och halksäkert klinker av samma modell på terrasserna.')
a('.qualitySpecs.groups[1].items[1]',
  'Porcelánico rectificado de gran formato en las paredes de los baños, y falsos techos en el recibidor, el pasillo, la cocina y los baños.',
  'Du grès cérame rectifié grand format aux murs des salles de bains, et des faux plafonds dans l’entrée, le couloir, la cuisine et les salles de bains.',
  'Rektifiziertes großformatiges Feinsteinzeug an den Badwänden und abgehängte Decken in Diele, Flur, Küche und Bädern.',
  'Ректифицированный крупноформатный керамогранит на стенах ванных и подвесные потолки в прихожей, коридоре, на кухне и в ванных.',
  'بورسلين مشطوف الحواف بقياس كبير على جدران الحمامات، وأسقف مستعارة في المدخل والممر والمطبخ والحمامات.',
  'Gerectificeerde grootformaat tegels op de badkamerwanden, en verlaagde plafonds in de hal, de gang, de keuken en de badkamers.',
  'Rektyfikowany wielkoformatowy gres na ścianach łazienek oraz sufity podwieszane w przedpokoju, korytarzu, kuchni i łazienkach.',
  'Rettkantede storformat porselensfliser på badeveggene, og nedforede tak i entré, gang, kjøkken og bad.',
  'Rektifierat storformatigt kakel på badrumsväggarna, och undertak i hall, korridor, kök och badrum.')
a('.qualitySpecs.groups[2].items[0]',
  'Muebles altos y bajos en dos colores a elegir, con encimera y frente entre muebles de Silestone, Compac o similar.',
  'Des meubles hauts et bas au choix en deux couleurs, avec plan de travail et crédence en Silestone, Compac ou équivalent.',
  'Ober- und Unterschränke in zwei Farben zur Wahl, mit Arbeitsplatte und Rückwand aus Silestone, Compac oder gleichwertig.',
  'Верхние и нижние шкафы на выбор в двух цветах, со столешницей и фартуком из Silestone, Compac или аналога.',
  'خزائن علوية وسفلية بلونين للاختيار، مع سطح عمل وواجهة خلفية من Silestone أو Compac أو ما يماثلهما.',
  'Hoge en lage kasten in twee kleuren naar keuze, met een werkblad en achterwand van Silestone, Compac of gelijkwaardig.',
  'Szafki górne i dolne w dwóch kolorach do wyboru, z blatem i ścianą między szafkami z Silestone, Compac lub podobnego materiału.',
  'Over- og underskap i to farger å velge mellom, med benkeplate og vegg mellom skapene i Silestone, Compac eller tilsvarende.',
  'Över- och underskåp i två färger att välja mellan, med bänkskiva och stänkskydd i Silestone, Compac eller likvärdigt.')
a('.qualitySpecs.groups[2].items[1]',
  'Electrodomésticos Bosch, Teka o similares: campana extractora, placa de inducción, horno eléctrico, microondas, lavavajillas, frigorífico y fregadero de acero integrado.',
  'Électroménager Bosch, Teka ou équivalent : hotte aspirante, plaque à induction, four électrique, micro-ondes, lave-vaisselle, réfrigérateur et évier en inox encastré.',
  'Geräte von Bosch, Teka oder gleichwertig: Dunstabzugshaube, Induktionskochfeld, Elektrobackofen, Mikrowelle, Geschirrspüler, Kühlschrank und eingebaute Edelstahlspüle.',
  'Техника Bosch, Teka или аналог: вытяжка, индукционная варочная панель, электрическая духовка, микроволновая печь, посудомоечная машина, холодильник и встроенная стальная мойка.',
  'أجهزة Bosch أو Teka أو ما يماثلها: شفاط، وموقد بالحث، وفرن كهربائي، وميكروويف، وغسالة صحون، وثلاجة، وحوض فولاذي مدمج.',
  'Apparatuur van Bosch, Teka of gelijkwaardig: afzuigkap, inductiekookplaat, elektrische oven, magnetron, vaatwasser, koelkast en een ingebouwde stalen spoelbak.',
  'Sprzęt Bosch, Teka lub podobny: okap, płyta indukcyjna, piekarnik elektryczny, mikrofalówka, zmywarka, lodówka i wbudowany stalowy zlew.',
  'Hvitevarer fra Bosch, Teka eller tilsvarende: kjøkkenvifte, induksjonstopp, elektrisk stekeovn, mikrobølgeovn, oppvaskmaskin, kjøleskap og innfelt stålvask.',
  'Vitvaror från Bosch, Teka eller likvärdigt: köksfläkt, induktionshäll, elektrisk ugn, mikrovågsugn, diskmaskin, kylskåp och infälld diskho i stål.')
a('.qualitySpecs.groups[3].items[0]',
  'Mueble de cajones con lavabo integrado, aparatos sanitarios de porcelana vitrificada blanca y plato de ducha de resina de bajo perfil.',
  'Un meuble à tiroirs avec vasque intégrée, des sanitaires en porcelaine vitrifiée blanche et un receveur de douche extra-plat en résine.',
  'Ein Schubladenunterschrank mit integriertem Waschbecken, Sanitärkeramik aus weißem Porzellan und eine flache Duschwanne aus Mineralguss.',
  'Тумба с ящиками и встроенной раковиной, сантехника из белого фаянса и низкий душевой поддон из искусственного камня.',
  'وحدة أدراج بمغسلة مدمجة، وأدوات صحية من البورسلين الأبيض المزجج، وقاعدة دُش منخفضة من الراتنج.',
  'Een ladekast met geïntegreerde wastafel, sanitair van wit verglaasd porselein en een lage douchebak van kunsthars.',
  'Szafka z szufladami i zintegrowaną umywalką, ceramika sanitarna z białej porcelany oraz niski brodzik z żywicy.',
  'Et skuffeskap med integrert servant, sanitærutstyr i hvitt porselen og et lavt dusjkar i kompositt.',
  'Ett lådskåp med integrerat handfat, sanitetsporslin i vitt och ett lågt duschtråg i komposit.')
a('.qualitySpecs.groups[3].items[1]',
  'Grifería monomando cromada con economizadores de agua y un sistema que reduce el consumo de agua caliente, y grifería empotrada en las duchas.',
  'Une robinetterie mitigeur chromée avec économiseurs d’eau et un système qui réduit la consommation d’eau chaude, et une robinetterie encastrée dans les douches.',
  'Verchromte Einhebelarmaturen mit Wassersparern und einem System, das den Warmwasserverbrauch senkt, sowie Unterputzarmaturen in den Duschen.',
  'Хромированные однорычажные смесители с экономайзерами и системой, снижающей расход горячей воды, и встроенные смесители в душевых.',
  'خلاطات كرومية بذراع واحدة مع موفّرات للمياه ونظام يقلّل استهلاك الماء الساخن، وخلاطات مدمجة في جدران الدُش.',
  'Verchroomde eenhendelkranen met waterbesparers en een systeem dat het warmwaterverbruik verlaagt, en inbouwkranen in de douches.',
  'Chromowane baterie jednouchwytowe z perlatorami oszczędzającymi wodę i systemem ograniczającym zużycie ciepłej wody oraz baterie podtynkowe pod prysznicami.',
  'Forkrommede ettgrepsbatterier med vannsparere og et system som reduserer forbruket av varmtvann, og innebygde dusjbatterier.',
  'Förkromade engreppsblandare med vattensparare och ett system som minskar varmvattenförbrukningen, och inbyggda duschblandare.')
a('.qualitySpecs.groups[4].items[0]',
  'Puerta de entrada de seguridad con tres puntos de anclaje y puertas interiores lisas lacadas en blanco con manillas en color cromo.',
  'Une porte d’entrée de sécurité à trois points d’ancrage et des portes intérieures lisses laquées blanc avec poignées couleur chrome.',
  'Eine Sicherheitseingangstür mit Dreifachverriegelung und glatte, weiß lackierte Innentüren mit verchromten Griffen.',
  'Защитная входная дверь с трёхточечным замком и гладкие межкомнатные двери, покрытые белым лаком, с ручками цвета хрома.',
  'باب دخول أمني بثلاث نقاط تثبيت، وأبواب داخلية ملساء مطلية بالأبيض بمقابض بلون الكروم.',
  'Een veiligheidsvoordeur met driepuntssluiting en gladde, wit gelakte binnendeuren met chroomkleurige klinken.',
  'Antywłamaniowe drzwi wejściowe z trzypunktowym ryglowaniem oraz gładkie, białe lakierowane drzwi wewnętrzne z klamkami w kolorze chromu.',
  'Sikkerhetsdør med trepunktslås og glatte, hvitlakkerte innerdører med kromfargede håndtak.',
  'En säkerhetsdörr med trepunktslås och släta, vitlackerade innerdörrar med kromfärgade handtag.')
a('.qualitySpecs.groups[4].items[1]',
  'Armarios empotrados de madera lacada en blanco con puertas correderas o abatibles, balda y barra de colgar, y persianas de aluminio lacado en los dormitorios.',
  'Des placards intégrés en bois laqué blanc à portes coulissantes ou battantes, avec étagère et penderie, et des volets roulants en aluminium laqué dans les chambres.',
  'Einbauschränke aus weiß lackiertem Holz mit Schiebe- oder Falttüren, Fachboden und Kleiderstange, und lackierte Aluminiumrollläden in den Schlafzimmern.',
  'Встроенные шкафы из дерева, покрытого белым лаком, с раздвижными или распашными дверцами, полкой и штангой и рольставни из окрашенного алюминия в спальнях.',
  'خزائن حائط مدمجة من الخشب المطلي بالأبيض بأبواب منزلقة أو قابلة للطي، مع رف وقضيب تعليق، ومصاريع ألومنيوم مطلية في غرف النوم.',
  'Inbouwkasten van wit gelakt hout met schuif- of vouwdeuren, een legplank en een kledingroede, en gelakte aluminium rolluiken in de slaapkamers.',
  'Szafy wnękowe z białego lakierowanego drewna z drzwiami przesuwnymi lub składanymi, półką i drążkiem oraz lakierowane aluminiowe rolety w sypialniach.',
  'Innebygde garderobeskap i hvitlakkert tre med skyve- eller foldedører, hylle og klesstang, og lakkerte aluminiumsrullegardiner på soverommene.',
  'Inbyggda garderober i vitlackerat trä med skjut- eller vikdörrar, hylla och klädstång, och lackerade aluminiumrullgardiner i sovrummen.')
a('.qualitySpecs.groups[5].items[0]',
  'Aire acondicionado por conductos, frío y calor, con bomba de calor, rejillas en todas las estancias y un único termostato en el salón.',
  'Une climatisation gainable, chaud et froid, par pompe à chaleur, avec des grilles dans chaque pièce et un seul thermostat dans le séjour.',
  'Kanalklimaanlage für Kühlen und Heizen mit Wärmepumpe, Gittern in jedem Raum und einem Thermostat im Wohnzimmer.',
  'Канальное кондиционирование на тепло и холод с тепловым насосом, решётками в каждой комнате и одним термостатом в гостиной.',
  'تكييف هواء بالقنوات، تبريد وتدفئة، بمضخة حرارية، مع فتحات في كل غرفة ومنظّم حرارة واحد في غرفة المعيشة.',
  'Kanaalairconditioning voor koelen en verwarmen met een warmtepomp, roosters in elke kamer en één thermostaat in de woonkamer.',
  'Kanałowa klimatyzacja z pompą ciepła, chłodzenie i ogrzewanie, z kratkami w każdym pomieszczeniu i jednym termostatem w salonie.',
  'Kanalbasert klimaanlegg for varme og kjøling med varmepumpe, rister i hvert rom og én termostat i stuen.',
  'Kanalbaserad luftkonditionering för värme och kyla med värmepump, galler i varje rum och en termostat i vardagsrummet.')
a('.qualitySpecs.groups[5].items[1]',
  'Agua caliente mediante un equipo de aerotermia en cada vivienda, y un sistema de ventilación de simple flujo que introduce aire fresco y extrae el aire viciado.',
  'L’eau chaude par une unité aérothermique propre à chaque logement, et une ventilation simple flux qui fait entrer l’air frais et extrait l’air vicié.',
  'Warmwasser über eine Luftwärmepumpe je Wohnung und eine einfache Abluftanlage, die Frischluft zuführt und verbrauchte Luft abführt.',
  'Горячая вода от собственного воздушного теплового насоса в каждой квартире и однопоточная вентиляция, подающая свежий воздух и удаляющая отработанный.',
  'الماء الساخن من وحدة طاقة هوائية حرارية لكل مسكن، ونظام تهوية أحادي التدفق يُدخل الهواء النقي ويطرد الهواء الفاسد.',
  'Warm water via een eigen luchtwarmtepomp per woning, en een enkelvoudig ventilatiesysteem dat verse lucht aanvoert en gebruikte lucht afvoert.',
  'Ciepła woda z indywidualnej pompy ciepła typu powietrze-woda w każdym lokalu oraz wentylacja jednostrumieniowa, która doprowadza świeże powietrze i usuwa zużyte.',
  'Varmtvann fra en luft-til-vann-varmepumpe i hver bolig, og et ventilasjonsanlegg med ett luftstrømsystem som tar inn frisk luft og trekker ut brukt luft.',
  'Varmvatten från en luft-vattenvärmepump i varje bostad, och ett frånluftssystem som tar in frisk luft och för ut förbrukad luft.')
a('.qualitySpecs.groups[6].items[0]',
  'Un spa con piscina climatizada por aerotermia, sauna finlandesa, duchas y vestuarios, y dos piscinas exteriores con cloración salina e iluminación subacuática.',
  'Un spa avec une piscine chauffée par aérothermie, un sauna finlandais, des douches et des vestiaires, et deux piscines extérieures à électrolyse au sel avec éclairage subaquatique.',
  'Ein Spa mit einem per Luftwärmepumpe beheizten Pool, finnischer Sauna, Duschen und Umkleiden, und zwei Außenpools mit Salzelektrolyse und Unterwasserbeleuchtung.',
  'Спа с бассейном, подогреваемым воздушным тепловым насосом, финской сауной, душевыми и раздевалками, и два открытых бассейна с солевым хлорированием и подводной подсветкой.',
  'سبا بمسبح مُدفّأ بالطاقة الهوائية الحرارية وساونا فنلندية ودُشات وغرف تبديل، ومسبحان خارجيان بالكلورة الملحية وإضاءة تحت الماء.',
  'Een spa met een zwembad dat met een luchtwarmtepomp wordt verwarmd, een Finse sauna, douches en kleedruimtes, en twee buitenzwembaden met zoutelektrolyse en onderwaterverlichting.',
  'Spa z basenem podgrzewanym pompą ciepła, sauną fińską, prysznicami i przebieralniami oraz dwa baseny zewnętrzne z chlorowaniem solnym i podwodnym oświetleniem.',
  'Et spa med basseng oppvarmet av luft-til-vann-varmepumpe, finsk badstue, dusjer og garderober, og to utendørs bassenger med saltklorering og undervannsbelysning.',
  'Ett spa med en pool som värms av luft-vattenvärmepump, finsk bastu, duschar och omklädningsrum, och två utomhuspooler med saltklorering och undervattensbelysning.')
a('.qualitySpecs.groups[6].items[1]',
  'Una zona chill-out con barbacoa, jardines de especies autóctonas que necesitan menos agua, recogida de pluviales para el riego y una zona de conserjería para los servicios del edificio.',
  'Un espace chill-out avec barbecue, des jardins d’espèces locales peu gourmandes en eau, la récupération des eaux de pluie pour l’arrosage et une conciergerie pour les services de l’immeuble.',
  'Ein Chill-out-Bereich mit Grill, Gärten mit heimischen Pflanzen, die weniger Wasser brauchen, Regenwassersammlung für die Bewässerung und ein Concierge-Bereich für die Gebäudedienste.',
  'Чилаут-зона с барбекю, сады из местных растений, которым нужно меньше воды, сбор дождевой воды для полива и консьерж-зона для обслуживания здания.',
  'منطقة استرخاء مع شواء، وحدائق من نباتات محلية تحتاج إلى مياه أقل، وتجميع مياه الأمطار للري، ومنطقة كونسيرج لخدمات المبنى.',
  'Een chill-outzone met barbecue, tuinen met inheemse soorten die minder water nodig hebben, opvang van regenwater voor de irrigatie en een conciërgeruimte voor de gebouwdiensten.',
  'Strefa chill-out z grillem, ogrody z rodzimych gatunków potrzebujących mniej wody, zbieranie deszczówki do nawadniania i strefa recepcji dla obsługi budynku.',
  'Et chill-out-område med grill, hager med stedegne arter som trenger mindre vann, oppsamling av regnvann til vanning og et resepsjonsområde for byggets tjenester.',
  'En chill-out-yta med grill, trädgårdar med inhemska arter som behöver mindre vatten, uppsamling av regnvatten för bevattning och en conciergeyta för byggnadens tjänster.')

# ---- residences ------------------------------------------------------------------------------

a('.residences.headlineHtml',
  'Diez viviendas, <em>cuatro niveles</em>', 'Dix logements, <em>quatre niveaux</em>', 'Zehn Wohnungen, <em>vier Ebenen</em>',
  'Десять квартир, <em>четыре уровня</em>', 'عشرة مساكن، <em>أربعة مستويات</em>', 'Tien woningen, <em>vier niveaus</em>',
  'Dziesięć lokali, <em>cztery poziomy</em>', 'Ti boliger, <em>fire nivåer</em>', 'Tio bostäder, <em>fyra plan</em>')
a('.residences.copy',
  'Las diez viviendas de la lista van desde un apartamento de un dormitorio en primera planta hasta áticos de tres dormitorios. Cada línea de la lista numera también una plaza de garaje y un trastero. La tabla de abajo recoge cada vivienda con su precio.',
  'Les dix logements de la liste vont d’un appartement d’une chambre au premier étage à des penthouses de trois chambres. Chaque ligne de la liste numérote aussi une place de parking et une cave. Le tableau ci-dessous présente chaque logement avec son prix.',
  'Die zehn Wohnungen der Liste reichen von einer Wohnung mit einem Schlafzimmer im ersten Obergeschoss bis zu Penthouses mit drei Schlafzimmern. Jede Zeile der Liste nennt außerdem die Nummer eines Stellplatzes und eines Abstellraums. Die Tabelle unten zeigt jede Wohnung mit ihrem Preis.',
  'Десять квартир из списка — от квартиры с одной спальней на втором этаже до пентхаусов с тремя спальнями. В каждой строке списка также указаны номера машино-места и кладовой. В таблице ниже — каждая квартира с ценой.',
  'تتراوح المساكن العشرة في القائمة بين شقة بغرفة نوم واحدة في الطابق الأول وشقق بنتهاوس بثلاث غرف نوم. ويرقّم كل سطر في القائمة أيضاً موقف سيارة ومخزناً. ويعرض الجدول أدناه كل مسكن مع سعره.',
  'De tien woningen op de lijst lopen van een appartement met één slaapkamer op de eerste verdieping tot penthouses met drie slaapkamers. Elke regel van de lijst nummert ook een parkeerplaats en een berging. De tabel hieronder toont elke woning met haar prijs.',
  'Dziesięć lokali z cennika to od mieszkania z jedną sypialnią na pierwszym piętrze po penthouse’y z trzema sypialniami. Każdy wiersz cennika podaje też numer miejsca w garażu i komórki. Tabela poniżej zawiera każdy lokal z ceną.',
  'De ti boligene på listen spenner fra en leilighet med ett soverom i andre etasje til toppleiligheter med tre soverom. Hver linje på listen nummererer også en garasjeplass og en bod. Tabellen nedenfor viser hver bolig med pris.',
  'De tio bostäderna på listan sträcker sig från en lägenhet med ett sovrum på första våningen till takvåningar med tre sovrum. Varje rad på listan numrerar också en garageplats och ett förråd. Tabellen nedan visar varje bostad med pris.')
a('.residences.items[0].name',
  'Una vivienda de un dormitorio', 'Un logement d’une chambre', 'Eine Wohnung mit einem Schlafzimmer', 'Квартира с одной спальней',
  'مسكن بغرفة نوم واحدة', 'Een woning met één slaapkamer', 'Lokal z jedną sypialnią', 'En bolig med ett soverom', 'En bostad med ett sovrum')
a('.residences.items[0].points[0]',
  'Vivienda 912, en el portal 9, primera planta: un dormitorio y un baño, con {N46.78} {U} construidos.',
  'Logement 912, cage 9, au premier étage : une chambre et une salle de bains, avec {N46.78} {U} construits.',
  'Wohnung 912, Aufgang 9, erstes Obergeschoss: ein Schlafzimmer und ein Bad, mit {N46.78} {U} bebauter Fläche.',
  'Квартира 912, подъезд 9, второй этаж: одна спальня и одна ванная, {N46.78} {U} застроенной площади.',
  'المسكن 912، المدخل 9، الطابق الأول: غرفة نوم واحدة وحمام واحد، بمساحة مبنية {N46.78} {U}.',
  'Woning 912, portiek 9, eerste verdieping: één slaapkamer en één badkamer, met {N46.78} {U} bebouwd.',
  'Lokal 912, klatka 9, pierwsze piętro: jedna sypialnia i jedna łazienka, {N46.78} {U} powierzchni zabudowy.',
  'Bolig 912, oppgang 9, andre etasje: ett soverom og ett bad, med {N46.78} {U} bygget.',
  'Bostad 912, uppgång 9, första våningen: ett sovrum och ett badrum, med {N46.78} {U} byggyta.')
a('.residences.items[0].points[1]',
  'Una terraza de {N14.30} {U}, en parte cubierta y en parte descubierta, por {E341000} antes de {T}.',
  'Une terrasse de {N14.30} {U}, en partie couverte et en partie ouverte, pour {E341000} hors {T}.',
  'Eine Terrasse von {N14.30} {U}, teils überdacht und teils offen, für {E341000} vor {T}.',
  'Терраса {N14.30} {U}, частично крытая и частично открытая, за {E341000} без {T}.',
  'تراس بمساحة {N14.30} {U}، جزء منه مسقوف وجزء مكشوف، بسعر {E341000} قبل {T}.',
  'Een terras van {N14.30} {U}, deels overdekt en deels open, voor {E341000} vóór {T}.',
  'Taras o powierzchni {N14.30} {U}, częściowo zadaszony i częściowo otwarty, za {E341000} przed {T}.',
  'En terrasse på {N14.30} {U}, delvis overbygd og delvis åpen, for {E341000} før {T}.',
  'En terrass på {N14.30} {U}, delvis täckt och delvis öppen, för {E341000} före {T}.')
a('.residences.items[1].name',
  'Viviendas de dos dormitorios', 'Logements de deux chambres', 'Wohnungen mit zwei Schlafzimmern', 'Квартиры с двумя спальнями',
  'مساكن بغرفتي نوم', 'Woningen met twee slaapkamers', 'Lokale z dwiema sypialniami', 'Boliger med to soverom', 'Bostäder med två sovrum')
a('.residences.items[1].points[0]',
  'Cuatro viviendas de dos dormitorios y dos baños, de {N72.28} a {N80.26} {U} construidos, de {E451000} a {E490000} antes de {T}.',
  'Quatre logements de deux chambres et deux salles de bains, de {N72.28} à {N80.26} {U} construits, de {E451000} à {E490000} hors {T}.',
  'Vier Wohnungen mit zwei Schlafzimmern und zwei Bädern, mit {N72.28} bis {N80.26} {U} bebauter Fläche, von {E451000} bis {E490000} vor {T}.',
  'Четыре квартиры с двумя спальнями и двумя ванными, от {N72.28} до {N80.26} {U} застроенной площади, от {E451000} до {E490000} без {T}.',
  'أربعة مساكن بغرفتي نوم وحمامين، بمساحة مبنية من {N72.28} إلى {N80.26} {U}، من {E451000} إلى {E490000} قبل {T}.',
  'Vier woningen met twee slaapkamers en twee badkamers, van {N72.28} tot {N80.26} {U} bebouwd, van {E451000} tot {E490000} vóór {T}.',
  'Cztery lokale z dwiema sypialniami i dwiema łazienkami, od {N72.28} do {N80.26} {U} powierzchni zabudowy, od {E451000} do {E490000} przed {T}.',
  'Fire boliger med to soverom og to bad, fra {N72.28} til {N80.26} {U} bygget, fra {E451000} til {E490000} før {T}.',
  'Fyra bostäder med två sovrum och två badrum, från {N72.28} till {N80.26} {U} byggyta, från {E451000} till {E490000} före {T}.')
a('.residences.items[1].points[1]',
  'La vivienda 403, en planta baja en el portal 4, tiene una terraza de {N41.85} {U} y un jardín de {N59.91} {U}; la vivienda 303, también en planta baja, tiene una terraza de {N45.59} {U}.',
  'Le logement 403, au rez-de-chaussée de la cage 4, a une terrasse de {N41.85} {U} et un jardin de {N59.91} {U} ; le logement 303, également au rez-de-chaussée, a une terrasse de {N45.59} {U}.',
  'Wohnung 403 im Erdgeschoss von Aufgang 4 hat eine Terrasse von {N41.85} {U} und einen Garten von {N59.91} {U}; Wohnung 303, ebenfalls im Erdgeschoss, hat eine Terrasse von {N45.59} {U}.',
  'У квартиры 403 на первом этаже в подъезде 4 терраса {N41.85} {U} и сад {N59.91} {U}; у квартиры 303, тоже на первом этаже, терраса {N45.59} {U}.',
  'للمسكن 403 في الطابق الأرضي عند المدخل 4 تراس بمساحة {N41.85} {U} وحديقة بمساحة {N59.91} {U}؛ وللمسكن 303، في الطابق الأرضي أيضاً، تراس بمساحة {N45.59} {U}.',
  'Woning 403 op de begane grond van portiek 4 heeft een terras van {N41.85} {U} en een tuin van {N59.91} {U}; woning 303, ook op de begane grond, heeft een terras van {N45.59} {U}.',
  'Lokal 403 na parterze w klatce 4 ma taras o powierzchni {N41.85} {U} i ogród o powierzchni {N59.91} {U}; lokal 303, również na parterze, ma taras o powierzchni {N45.59} {U}.',
  'Bolig 403 i første etasje i oppgang 4 har en terrasse på {N41.85} {U} og en hage på {N59.91} {U}; bolig 303, også i første etasje, har en terrasse på {N45.59} {U}.',
  'Bostad 403 på bottenvåningen i uppgång 4 har en terrass på {N41.85} {U} och en trädgård på {N59.91} {U}; bostad 303, också på bottenvåningen, har en terrass på {N45.59} {U}.')
a('.residences.items[1].points[2]',
  'Las viviendas 222 y 624 están en segundas plantas, con terrazas de {N21.65} y {N26.71} {U}.',
  'Les logements 222 et 624 sont au deuxième étage, avec des terrasses de {N21.65} et {N26.71} {U}.',
  'Die Wohnungen 222 und 624 liegen im zweiten Obergeschoss, mit Terrassen von {N21.65} und {N26.71} {U}.',
  'Квартиры 222 и 624 находятся на третьих этажах, с террасами {N21.65} и {N26.71} {U}.',
  'يقع المسكنان 222 و624 في الطابق الثاني، بتراسين مساحتهما {N21.65} و{N26.71} {U}.',
  'De woningen 222 en 624 liggen op de tweede verdieping, met terrassen van {N21.65} en {N26.71} {U}.',
  'Lokale 222 i 624 znajdują się na drugich piętrach, z tarasami o powierzchni {N21.65} i {N26.71} {U}.',
  'Bolig 222 og 624 ligger i tredje etasje, med terrasser på {N21.65} og {N26.71} {U}.',
  'Bostäderna 222 och 624 ligger på andra våningen, med terrasser på {N21.65} och {N26.71} {U}.')
a('.residences.items[2].name',
  'Viviendas de tres dormitorios', 'Logements de trois chambres', 'Wohnungen mit drei Schlafzimmern', 'Квартиры с тремя спальнями',
  'مساكن بثلاث غرف نوم', 'Woningen met drie slaapkamers', 'Lokale z trzema sypialniami', 'Boliger med tre soverom', 'Bostäder med tre sovrum')
a('.residences.items[2].points[0]',
  'Vivienda 101, en planta baja en el portal 1, con {N96.76} {U} construidos incluido un lavadero y una terraza de {N64.78} {U}, por {E595000} antes de {T}.',
  'Logement 101, au rez-de-chaussée de la cage 1, avec {N96.76} {U} construits buanderie comprise et une terrasse de {N64.78} {U}, pour {E595000} hors {T}.',
  'Wohnung 101 im Erdgeschoss von Aufgang 1, mit {N96.76} {U} bebauter Fläche einschließlich eines Hauswirtschaftsraums und einer Terrasse von {N64.78} {U}, für {E595000} vor {T}.',
  'Квартира 101 на первом этаже в подъезде 1: {N96.76} {U} застроенной площади с постирочной и терраса {N64.78} {U}, за {E595000} без {T}.',
  'المسكن 101 في الطابق الأرضي عند المدخل 1، بمساحة مبنية {N96.76} {U} تشمل غرفة غسيل، وتراس بمساحة {N64.78} {U}، بسعر {E595000} قبل {T}.',
  'Woning 101 op de begane grond van portiek 1, met {N96.76} {U} bebouwd inclusief een wasruimte en een terras van {N64.78} {U}, voor {E595000} vóór {T}.',
  'Lokal 101 na parterze w klatce 1, {N96.76} {U} powierzchni zabudowy łącznie z pralnią i taras o powierzchni {N64.78} {U}, za {E595000} przed {T}.',
  'Bolig 101 i første etasje i oppgang 1, med {N96.76} {U} bygget inkludert vaskerom og en terrasse på {N64.78} {U}, for {E595000} før {T}.',
  'Bostad 101 på bottenvåningen i uppgång 1, med {N96.76} {U} byggyta inklusive tvättstuga och en terrass på {N64.78} {U}, för {E595000} före {T}.')
a('.residences.items[2].points[1]',
  'Vivienda 914, en primera planta en el portal 9, con {N101.62} {U} construidos incluido un lavadero y una terraza de {N16.50} {U}, por {E581000} antes de {T}.',
  'Logement 914, au premier étage de la cage 9, avec {N101.62} {U} construits buanderie comprise et une terrasse de {N16.50} {U}, pour {E581000} hors {T}.',
  'Wohnung 914 im ersten Obergeschoss von Aufgang 9, mit {N101.62} {U} bebauter Fläche einschließlich eines Hauswirtschaftsraums und einer Terrasse von {N16.50} {U}, für {E581000} vor {T}.',
  'Квартира 914 на втором этаже в подъезде 9: {N101.62} {U} застроенной площади с постирочной и терраса {N16.50} {U}, за {E581000} без {T}.',
  'المسكن 914 في الطابق الأول عند المدخل 9، بمساحة مبنية {N101.62} {U} تشمل غرفة غسيل، وتراس بمساحة {N16.50} {U}، بسعر {E581000} قبل {T}.',
  'Woning 914 op de eerste verdieping van portiek 9, met {N101.62} {U} bebouwd inclusief een wasruimte en een terras van {N16.50} {U}, voor {E581000} vóór {T}.',
  'Lokal 914 na pierwszym piętrze w klatce 9, {N101.62} {U} powierzchni zabudowy łącznie z pralnią i taras o powierzchni {N16.50} {U}, za {E581000} przed {T}.',
  'Bolig 914 i andre etasje i oppgang 9, med {N101.62} {U} bygget inkludert vaskerom og en terrasse på {N16.50} {U}, for {E581000} før {T}.',
  'Bostad 914 på första våningen i uppgång 9, med {N101.62} {U} byggyta inklusive tvättstuga och en terrass på {N16.50} {U}, för {E581000} före {T}.')
a('.residences.items[3].name',
  'Áticos', 'Penthouses', 'Penthouses', 'Пентхаусы', 'شقق البنتهاوس', 'Penthouses', 'Penthouse’y', 'Toppleiligheter', 'Takvåningar')
a('.residences.items[3].points[0]',
  'Tres áticos con terrazas de unos {N100} {U}: la vivienda 531, de tres dormitorios y {N99.51} {U} construidos, por {E795000}, y las viviendas 231 y 232 en el portal 2.',
  'Trois penthouses avec des terrasses d’environ {N100} {U} : le logement 531, de trois chambres et {N99.51} {U} construits, pour {E795000}, et les logements 231 et 232 dans la cage 2.',
  'Drei Penthouses mit Terrassen von etwa {N100} {U}: Wohnung 531 mit drei Schlafzimmern und {N99.51} {U} bebauter Fläche für {E795000} sowie die Wohnungen 231 und 232 in Aufgang 2.',
  'Три пентхауса с террасами около {N100} {U}: квартира 531 с тремя спальнями и {N99.51} {U} застроенной площади за {E795000} и квартиры 231 и 232 в подъезде 2.',
  'ثلاث شقق بنتهاوس بتراسات تبلغ نحو {N100} {U}: المسكن 531 بثلاث غرف نوم ومساحة مبنية {N99.51} {U} بسعر {E795000}، والمسكنان 231 و232 عند المدخل 2.',
  'Drie penthouses met terrassen van ongeveer {N100} {U}: woning 531 met drie slaapkamers en {N99.51} {U} bebouwd voor {E795000}, en de woningen 231 en 232 in portiek 2.',
  'Trzy penthouse’y z tarasami o powierzchni około {N100} {U}: lokal 531 z trzema sypialniami i {N99.51} {U} powierzchni zabudowy za {E795000} oraz lokale 231 i 232 w klatce 2.',
  'Tre toppleiligheter med terrasser på rundt {N100} {U}: bolig 531 med tre soverom og {N99.51} {U} bygget for {E795000}, og bolig 231 og 232 i oppgang 2.',
  'Tre takvåningar med terrasser på omkring {N100} {U}: bostad 531 med tre sovrum och {N99.51} {U} byggyta för {E795000}, och bostäderna 231 och 232 i uppgång 2.')
a('.residences.items[3].points[1]',
  'La vivienda 231, de tres dormitorios, suma un solárium de {N87.42} {U}, por {E885000}; la vivienda 232, de dos dormitorios, suma un solárium de {N65.85} {U}, por {E780000}, ambas antes de {T}.',
  'Le logement 231, de trois chambres, ajoute un solarium de {N87.42} {U}, pour {E885000} ; le logement 232, de deux chambres, ajoute un solarium de {N65.85} {U}, pour {E780000}, tous deux hors {T}.',
  'Wohnung 231 mit drei Schlafzimmern hat zusätzlich ein Solarium von {N87.42} {U}, für {E885000}; Wohnung 232 mit zwei Schlafzimmern hat ein Solarium von {N65.85} {U}, für {E780000}, beide vor {T}.',
  'У квартиры 231 с тремя спальнями есть ещё солярий {N87.42} {U}, за {E885000}; у квартиры 232 с двумя спальнями — солярий {N65.85} {U}, за {E780000}, обе цены без {T}.',
  'يضيف المسكن 231، بثلاث غرف نوم، سولاريوم بمساحة {N87.42} {U}، بسعر {E885000}؛ ويضيف المسكن 232، بغرفتي نوم، سولاريوم بمساحة {N65.85} {U}، بسعر {E780000}، وكلاهما قبل {T}.',
  'Woning 231, met drie slaapkamers, heeft daarbij een solarium van {N87.42} {U}, voor {E885000}; woning 232, met twee slaapkamers, een solarium van {N65.85} {U}, voor {E780000}, beide vóór {T}.',
  'Lokal 231 z trzema sypialniami ma dodatkowo solarium o powierzchni {N87.42} {U}, za {E885000}; lokal 232 z dwiema sypialniami ma solarium o powierzchni {N65.85} {U}, za {E780000}, oba przed {T}.',
  'Bolig 231, med tre soverom, har i tillegg en solterrasse på {N87.42} {U}, for {E885000}; bolig 232, med to soverom, en solterrasse på {N65.85} {U}, for {E780000}, begge før {T}.',
  'Bostad 231, med tre sovrum, har dessutom en solterrass på {N87.42} {U}, för {E885000}; bostad 232, med två sovrum, en solterrass på {N65.85} {U}, för {E780000}, båda före {T}.')

# ---- lifestyle, location ---------------------------------------------------------------------

a('.lifestyle.headlineHtml',
  'Dos piscinas, un spa <em>y un mirador</em>', 'Deux piscines, un spa <em>et un belvédère</em>', 'Zwei Pools, ein Spa <em>und ein Aussichtspunkt</em>',
  'Два бассейна, спа <em>и смотровая площадка</em>', 'مسبحان وسبا <em>ونقطة إطلالة</em>', 'Twee zwembaden, een spa <em>en een uitkijkpunt</em>',
  'Dwa baseny, spa <em>i punkt widokowy</em>', 'To bassenger, et spa <em>og et utsiktspunkt</em>', 'Två pooler, ett spa <em>och en utsiktsplats</em>')
a('.lifestyle.copy',
  'Las zonas comunes están en el jardín entre los bloques: dos piscinas exteriores, un spa, un gimnasio, un salón social con coworking, zonas de juego y un camino hasta un mirador.',
  'Les espaces communs se trouvent dans le jardin entre les bâtiments : deux piscines extérieures, un spa, une salle de sport, un salon commun avec coworking, des espaces de jeu et une allée jusqu’à un belvédère.',
  'Die Gemeinschaftsbereiche liegen im Garten zwischen den Gebäuden: zwei Außenpools, ein Spa, ein Fitnessraum, eine Gemeinschaftslounge mit Coworking, Spielbereiche und ein Weg zu einem Aussichtspunkt.',
  'Общие зоны расположены в саду между корпусами: два открытых бассейна, спа, тренажёрный зал, общая гостиная с коворкингом, игровые зоны и дорожка к смотровой площадке.',
  'تقع المرافق المشتركة في الحديقة بين المباني: مسبحان خارجيان وسبا وصالة رياضية وصالة اجتماعية مع مساحة عمل مشترك ومناطق للعب وممر إلى نقطة إطلالة.',
  'De gemeenschappelijke ruimtes liggen in de tuin tussen de blokken: twee buitenzwembaden, een spa, een fitnessruimte, een sociale lounge met coworking, speelplekken en een pad naar een uitkijkpunt.',
  'Części wspólne znajdują się w ogrodzie między budynkami: dwa baseny zewnętrzne, spa, siłownia, salon wspólny z coworkingiem, miejsca do zabawy i ścieżka do punktu widokowego.',
  'Fellesområdene ligger i hagen mellom blokkene: to utendørs bassenger, et spa, et treningsrom, en fellesstue med coworking, lekeområder og en sti til et utsiktspunkt.',
  'De gemensamma ytorna ligger i trädgården mellan husen: två utomhuspooler, ett spa, ett gym, en sällskapslounge med coworking, lekytor och en gång till en utsiktsplats.')
a('.lifestyle.panels[0][1]',
  'Dos piscinas exteriores con solárium, una de ellas con calle de nado y borde de tipo infinito, ambas con cloración salina, a las que se llega por un camino que cruza un estanque.',
  'Deux piscines extérieures avec solarium, l’une avec un couloir de nage et un bord de type débordement, toutes deux à électrolyse au sel, auxquelles on accède par une allée qui traverse un bassin.',
  'Zwei Außenpools mit Sonnenterrasse, einer davon mit Schwimmbahn und Infinity-Kante, beide mit Salzelektrolyse, erreichbar über einen Weg, der einen Teich quert.',
  'Два открытых бассейна с солнечной террасой, один из них с дорожкой для плавания и бортом типа «инфинити», оба с солевым хлорированием; к ним ведёт дорожка через пруд.',
  'مسبحان خارجيان مع تراس للتشمس، أحدهما بممر سباحة وحافة من نوع اللانهائي، وكلاهما بالكلورة الملحية، ويُصل إليهما عبر ممر يعبر بركة.',
  'Twee buitenzwembaden met zonneterras, een ervan met een zwembaan en een infinityrand, beide met zoutelektrolyse, bereikbaar via een pad over een vijver.',
  'Dwa baseny zewnętrzne z tarasem słonecznym, jeden z torem do pływania i krawędzią typu infinity, oba z chlorowaniem solnym, do których prowadzi ścieżka przez staw.',
  'To utendørs bassenger med soldekk, det ene med svømmebane og infinitykant, begge med saltklorering, og en sti over en dam fører dit.',
  'Två utomhuspooler med soldäck, den ena med simbana och infinitykant, båda med saltklorering, och en gång över en damm leder dit.')
a('.lifestyle.panels[1][0]',
  'El spa y el gimnasio', 'Le spa et la salle de sport', 'Spa und Fitnessraum', 'Спа и тренажёрный зал', 'السبا والصالة الرياضية',
  'De spa en de fitnessruimte', 'Spa i siłownia', 'Spaet og treningsrommet', 'Spaet och gymmet')
a('.lifestyle.panels[1][1]',
  'Un spa con piscina climatizada, sauna, vestuarios y zona de relajación, junto a un gimnasio con una terraza de yoga delante.',
  'Un spa avec piscine chauffée, sauna, vestiaires et espace détente, à côté d’une salle de sport précédée d’une terrasse de yoga.',
  'Ein Spa mit beheiztem Pool, Sauna, Umkleiden und Ruhebereich, neben einem Fitnessraum mit einer Yogaterrasse davor.',
  'Спа с подогреваемым бассейном, сауной, раздевалками и зоной отдыха, рядом тренажёрный зал с террасой для йоги перед ним.',
  'سبا بمسبح مُدفّأ وساونا وغرف تبديل ومنطقة استرخاء، بجانب صالة رياضية أمامها تراس لليوغا.',
  'Een spa met verwarmd zwembad, sauna, kleedruimtes en een relaxruimte, naast een fitnessruimte met een yogaterras ervoor.',
  'Spa z podgrzewanym basenem, sauną, przebieralniami i strefą relaksu, obok siłowni z tarasem do jogi przed wejściem.',
  'Et spa med oppvarmet basseng, badstue, garderober og hvileområde, ved siden av et treningsrom med en yogaterrasse foran.',
  'Ett spa med uppvärmd pool, bastu, omklädningsrum och vilrum, bredvid ett gym med en yogaterrass framför.')
a('.lifestyle.panels[2][0]',
  'El salón social', 'Le salon commun', 'Die Gemeinschaftslounge', 'Общая гостиная', 'الصالة الاجتماعية', 'De sociale lounge',
  'Salon wspólny', 'Fellesstuen', 'Sällskapsloungen')
a('.lifestyle.panels[2][1]',
  'Un salón y sala de coworking con mesas compartidas y terraza, y un salón exterior con barbacoa para reuniones.',
  'Un salon et un espace de coworking avec bureaux partagés et terrasse, et un salon extérieur avec barbecue pour se retrouver.',
  'Eine Lounge mit Coworking-Raum, gemeinsamen Arbeitstischen und Terrasse, und eine Außenlounge mit Grill für Zusammenkünfte.',
  'Гостиная и коворкинг с общими столами и террасой, а также уличная лаунж-зона с барбекю для встреч.',
  'صالة ومساحة عمل مشترك بمكاتب مشتركة وتراس، وصالة خارجية مع شواء للتجمعات.',
  'Een lounge en coworkingruimte met gedeelde werktafels en een terras, en een buitenlounge met barbecue om samen te komen.',
  'Salon i sala coworkingowa ze wspólnymi stołami i tarasem oraz zewnętrzny salon z grillem na spotkania.',
  'En salong og et coworking-rom med delte arbeidsbord og terrasse, og en utendørs lounge med grill til sammenkomster.',
  'En lounge och ett coworkingrum med delade arbetsbord och terrass, och en utomhuslounge med grill för samvaro.')
a('.lifestyle.panels[3][0]',
  'Juegos en el jardín', 'Jeux dans le jardin', 'Spiel im Garten', 'Игры в саду', 'الألعاب في الحديقة', 'Spel in de tuin',
  'Gry w ogrodzie', 'Lek i hagen', 'Lek i trädgården')
a('.lifestyle.panels[3][1]',
  'Un green de putting, una pista de arena para vóley playa y pádel playa, una zona infantil y huertos ecológicos.',
  'Un green de putting, un terrain de sable pour le beach-volley et le beach-tennis, un espace enfants et des potagers biologiques.',
  'Ein Putting-Green, ein Sandplatz für Beachvolleyball und Beach-Paddle, ein Kinderbereich und Bio-Gemüsegärten.',
  'Паттинг-грин, песчаная площадка для пляжного волейбола и пляжного падела, детская зона и органические огороды.',
  'ملعب للضربات القصيرة، وملعب رملي للكرة الطائرة الشاطئية والبادل الشاطئي، ومنطقة للأطفال، وحدائق خضراوات عضوية.',
  'Een puttinggreen, een zandveld voor beachvolleybal en beachpaddle, een kinderhoek en biologische moestuinen.',
  'Putting green, piaszczyste boisko do siatkówki plażowej i plażowego padla, strefa dla dzieci i ekologiczne ogródki warzywne.',
  'En puttinggreen, en sandbane for sandvolleyball og strandpadel, et barneområde og økologiske kjøkkenhager.',
  'En puttinggreen, en sandplan för beachvolley och beachpaddel, en lekyta för barn och ekologiska köksträdgårdar.')
a('.lifestyle.panels[4][0]',
  'El mirador', 'Le belvédère', 'Der Aussichtspunkt', 'Смотровая площадка', 'نقطة الإطلالة', 'Het uitkijkpunt',
  'Punkt widokowy', 'Utsiktspunktet', 'Utsiktsplatsen')
a('.lifestyle.panels[4][1]',
  'Un sendero por el jardín lleva a un mirador con zona de lectura, que el folleto presenta como un lugar para ver la puesta de sol.',
  'Un sentier à travers le jardin mène à un belvédère avec un coin lecture, que la brochure présente comme un endroit d’où regarder le coucher du soleil.',
  'Ein Fußweg durch den Garten führt zu einem Aussichtspunkt mit Leseecke, den die Broschüre als Ort für den Sonnenuntergang beschreibt.',
  'Тропинка через сад ведёт к смотровой площадке с зоной для чтения, которую буклет представляет как место, откуда можно наблюдать закат.',
  'يقود ممر عبر الحديقة إلى نقطة إطلالة مع منطقة للقراءة، يقدّمها الكتيّب مكاناً لمشاهدة غروب الشمس.',
  'Een voetpad door de tuin leidt naar een uitkijkpunt met een leeshoek, dat de brochure voorstelt als een plek om de zonsondergang te zien.',
  'Ścieżka przez ogród prowadzi do punktu widokowego z kącikiem do czytania, który broszura przedstawia jako miejsce do oglądania zachodów słońca.',
  'En gangsti gjennom hagen fører til et utsiktspunkt med lesekrok, som brosjyren presenterer som et sted å se solnedgangen fra.',
  'En gångstig genom trädgården leder till en utsiktsplats med läshörna, som broschyren presenterar som en plats att se solnedgången från.')
a('.lifestyle.panels[5][0]',
  'La conserjería', 'La conciergerie', 'Der Concierge', 'Консьерж', 'خدمة الكونسيرج', 'De conciërge', 'Recepcja', 'Resepsjonen', 'Conciergen')
a('.lifestyle.panels[5][1]',
  'El folleto describe una zona de conserjería desde la que gestionar la lavandería, la limpieza de apartamentos, pequeñas reparaciones y el mantenimiento de las zonas comunes.',
  'La brochure décrit une conciergerie depuis laquelle gérer la blanchisserie, le ménage des appartements, les petites réparations et l’entretien des espaces communs.',
  'Die Broschüre beschreibt einen Concierge-Bereich, über den Wäscheservice, Wohnungsreinigung, kleine Reparaturen und die Pflege der Gemeinschaftsbereiche organisiert werden können.',
  'Буклет описывает консьерж-зону, через которую можно заказать прачечную, уборку квартиры, мелкий ремонт и обслуживание общих зон.',
  'يصف الكتيّب منطقة كونسيرج يمكن من خلالها ترتيب خدمات الغسيل وتنظيف الشقق والإصلاحات الصغيرة وصيانة المرافق المشتركة.',
  'De brochure beschrijft een conciërgeruimte van waaruit wasservice, schoonmaak van appartementen, kleine reparaties en het onderhoud van de gemeenschappelijke ruimtes geregeld kunnen worden.',
  'Broszura opisuje strefę recepcji, przez którą można zamówić pralnię, sprzątanie mieszkań, drobne naprawy i utrzymanie części wspólnych.',
  'Brosjyren beskriver et resepsjonsområde der vasketjeneste, rengjøring av leiligheter, småreparasjoner og vedlikehold av fellesområdene kan ordnes.',
  'Broschyren beskriver en conciergeyta där tvätt, städning av lägenheter, mindre reparationer och skötseln av de gemensamma ytorna kan ordnas.')

a('.location.headlineHtml',
  'Mijas Costa, <em>entre campos de golf</em>', 'Mijas Costa, <em>parmi les golfs</em>', 'Mijas Costa, <em>zwischen Golfplätzen</em>',
  'Михас-Коста, <em>среди гольф-полей</em>', 'ميخاس كوستا، <em>بين ملاعب الغولف</em>', 'Mijas Costa, <em>tussen de golfbanen</em>',
  'Mijas Costa, <em>wśród pól golfowych</em>', 'Mijas Costa, <em>blant golfbanene</em>', 'Mijas Costa, <em>bland golfbanorna</em>')
a('.location.copy',
  'El folleto sitúa la promoción entre Fuengirola y La Cala de Mijas, en un entorno natural entre campos de golf. Su mapa marca Cerrado del Águila Golf a 2 km y Chaparral Golf a 3 km, y el plano urbanístico del promotor muestra la parcela al oeste del Hipódromo Costa del Sol. Los documentos no dan una dirección, así que la ubicación de nuestro mapa es aproximada.',
  'La brochure situe la résidence entre Fuengirola et La Cala de Mijas, dans un cadre naturel entre des golfs. Sa carte place Cerrado del Águila Golf à 2 km et Chaparral Golf à 3 km, et le plan d’urbanisme du promoteur montre le terrain à l’ouest de l’hippodrome de la Costa del Sol. Les documents ne donnent pas d’adresse, la position sur notre carte est donc approximative.',
  'Die Broschüre verortet die Anlage zwischen Fuengirola und La Cala de Mijas, in natürlicher Umgebung zwischen Golfplätzen. Ihre Karte zeigt Cerrado del Águila Golf in 2 km und Chaparral Golf in 3 km Entfernung, und der Bebauungsplan des Bauträgers zeigt das Grundstück westlich der Pferderennbahn der Costa del Sol. Die Unterlagen nennen keine Adresse, daher ist die Markierung auf unserer Karte ungefähr.',
  'Буклет располагает комплекс между Фуэнхиролой и Ла-Кала-де-Михас, в природном окружении среди гольф-полей. На его карте Cerrado del Águila Golf отмечен в 2 км, а Chaparral Golf — в 3 км, а градостроительный план застройщика показывает участок к западу от ипподрома Коста-дель-Соль. Адреса в документах нет, поэтому точка на нашей карте приблизительная.',
  'يضع الكتيّب المشروع بين فوينخيرولا ولا كالا دي ميخاس، في بيئة طبيعية بين ملاعب الغولف. وتحدّد خريطته Cerrado del Águila Golf على بُعد 2 كم وChaparral Golf على بُعد 3 كم، ويُظهر المخطط العمراني للمطوّر قطعة الأرض غرب ميدان سباق الخيل في كوستا ديل سول. ولا تذكر الوثائق عنواناً، لذا فإن الموقع على خريطتنا تقريبي.',
  'De brochure situeert het complex tussen Fuengirola en La Cala de Mijas, in een natuurlijke omgeving tussen golfbanen. De kaart plaatst Cerrado del Águila Golf op 2 km en Chaparral Golf op 3 km, en het bestemmingsplan van de ontwikkelaar toont het perceel ten westen van de renbaan van de Costa del Sol. De documenten geven geen adres, dus de positie op onze kaart is bij benadering.',
  'Broszura lokalizuje osiedle między Fuengirolą a La Cala de Mijas, w naturalnym otoczeniu wśród pól golfowych. Jej mapa podaje Cerrado del Águila Golf w odległości 2 km i Chaparral Golf w odległości 3 km, a plan zagospodarowania dewelopera pokazuje działkę na zachód od toru wyścigów konnych Costa del Sol. Dokumenty nie podają adresu, więc położenie na naszej mapie jest przybliżone.',
  'Brosjyren plasserer anlegget mellom Fuengirola og La Cala de Mijas, i naturlige omgivelser mellom golfbaner. Kartet viser Cerrado del Águila Golf 2 km unna og Chaparral Golf 3 km unna, og utbyggerens reguleringsplan viser tomten vest for galoppbanen på Costa del Sol. Dokumentene oppgir ingen adresse, så plasseringen på kartet vårt er omtrentlig.',
  'Broschyren placerar området mellan Fuengirola och La Cala de Mijas, i en naturlig miljö bland golfbanor. Kartan anger Cerrado del Águila Golf på 2 km och Chaparral Golf på 3 km, och exploatörens detaljplan visar tomten väster om Costa del Sols galoppbana. Handlingarna anger ingen adress, så platsen på vår karta är ungefärlig.')
a('.location.distances[0][1]',
  '2 km en el mapa del promotor', '2 km sur la carte du promoteur', '2 km laut Karte des Bauträgers', '2 км по карте застройщика',
  '2 كم على خريطة المطوّر', '2 km op de kaart van de ontwikkelaar', '2 km na mapie dewelopera', '2 km på utbyggerens kart', '2 km på exploatörens karta')
a('.location.distances[1][1]',
  '3 km en el mapa del promotor', '3 km sur la carte du promoteur', '3 km laut Karte des Bauträgers', '3 км по карте застройщика',
  '3 كم على خريطة المطوّر', '3 km op de kaart van de ontwikkelaar', '3 km na mapie dewelopera', '3 km på utbyggerens kart', '3 km på exploatörens karta')
a('.location.distances[2][1]',
  '5 km en el mapa del promotor', '5 km sur la carte du promoteur', '5 km laut Karte des Bauträgers', '5 км по карте застройщика',
  '5 كم على خريطة المطوّر', '5 km op de kaart van de ontwikkelaar', '5 km na mapie dewelopera', '5 km på utbyggerens kart', '5 km på exploatörens karta')
a('.location.distances[3][1]',
  '13 km en el mapa del promotor', '13 km sur la carte du promoteur', '13 km laut Karte des Bauträgers', '13 км по карте застройщика',
  '13 كم على خريطة المطوّر', '13 km op de kaart van de ontwikkelaar', '13 km na mapie dewelopera', '13 km på utbyggerens kart', '13 km på exploatörens karta')
a('.location.distances[4][1]',
  '37 km en el mapa del promotor', '37 km sur la carte du promoteur', '37 km laut Karte des Bauträgers', '37 км по карте застройщика',
  '37 كم على خريطة المطوّر', '37 km op de kaart van de ontwikkelaar', '37 km na mapie dewelopera', '37 km på utbyggerens kart', '37 km på exploatörens karta')

# ---- investment, trust -----------------------------------------------------------------------

a('.investment.cards[0][1]',
  'La lista de precios indica que sus precios son netos y no incluyen el {T} ni el impuesto de transmisiones. El {T} del 10 % y el AJD del 1,20 % suman unos {E38000} a la vivienda más económica y unos {E99000} al ático más caro, antes de notaría y registro.',
  'La liste de prix indique que ses prix sont nets et n’incluent ni la {T} ni les droits de mutation. La {T} de 10 % et le droit de timbre de 1,20 % ajoutent environ {E38000} au logement le moins cher et environ {E99000} au penthouse le plus cher, avant les frais de notaire et d’enregistrement.',
  'Die Preisliste gibt ihre Preise als Nettopreise ohne {T} und Grunderwerbsteuer an. 10 % {T} und 1,20 % Stempelsteuer (AJD) kommen beim günstigsten Objekt auf etwa {E38000} und beim teuersten Penthouse auf etwa {E99000}, vor Notar- und Grundbuchkosten.',
  'В прайс-листе сказано, что цены указаны нетто, без {T} и налога на передачу имущества. {T} 10 % и гербовый сбор 1,20 % добавляют около {E38000} к самой доступной квартире и около {E99000} к самому дорогому пентхаусу, без учёта нотариуса и регистрации.',
  'تذكر قائمة الأسعار أن أسعارها صافية ولا تشمل {T} ولا ضريبة نقل الملكية. وتضيف {T} بنسبة 10% ورسم الدمغة بنسبة 1.20% نحو {E38000} إلى أرخص مسكن ونحو {E99000} إلى أغلى بنتهاوس، قبل رسوم الكاتب العدل والسجل العقاري.',
  'De prijslijst vermeldt dat de prijzen netto zijn, exclusief {T} en overdrachtsbelasting. {T} van 10 % en zegelrecht van 1,20 % tellen ongeveer {E38000} op bij de goedkoopste woning en ongeveer {E99000} bij de duurste penthouse, vóór notaris- en registratiekosten.',
  'Cennik podaje, że ceny są netto i nie obejmują {T} ani podatku od przeniesienia własności. {T} 10% i opłata skarbowa 1,20% dodają około {E38000} do najtańszego lokalu i około {E99000} do najdroższego penthouse’u, przed kosztami notariusza i rejestru.',
  'Prislisten oppgir at prisene er netto og ikke inkluderer {T} eller dokumentavgift. {T} på 10 % og stempelavgift på 1,20 % legger til omkring {E38000} på den rimeligste boligen og omkring {E99000} på den dyreste toppleiligheten, før notar- og tinglysingskostnader.',
  'Prislistan anger att priserna är nettopriser utan {T} (spansk moms) och överlåtelseskatt. {T} på 10 % och stämpelskatt på 1,20 % lägger till omkring {E38000} på den billigaste bostaden och omkring {E99000} på den dyraste takvåningen, före notarie- och inskrivningskostnader.')
a('.investment.cards[1][0]',
  'Las fechas vienen del portal', 'Les dates viennent du portail', 'Die Termine stammen aus dem Portal', 'Даты взяты с портала',
  'التواريخ مصدرها البوابة', 'De data komen uit het portaal', 'Daty pochodzą z portalu', 'Datoene kommer fra portalen', 'Datumen kommer från portalen')
a('.investment.cards[1][1]',
  'El inicio de las obras el 11 de noviembre de 2025, la licencia de obra y la entrega en septiembre de 2028 figuran en el portal del promotor, no en el folleto ni en la lista de precios, así que los pedimos en el contrato, con lo que ocurre si la fecha se retrasa.',
  'Le début des travaux le 11 novembre 2025, le permis de construire et la livraison en septembre 2028 figurent sur le portail du promoteur, et non dans la brochure ni sur la liste de prix ; nous les demandons donc dans le contrat, avec ce qui se passe si la date glisse.',
  'Der Baubeginn am 11. November 2025, die Baugenehmigung und die Fertigstellung im September 2028 stehen im Portal des Bauträgers, nicht in der Broschüre oder der Preisliste. Deshalb verlangen wir sie im Vertrag, zusammen mit den Folgen einer Verzögerung.',
  'Начало работ 11 ноября 2025 года, разрешение на строительство и сдача в сентябре 2028 года указаны на портале застройщика, а не в буклете и не в прайс-листе, поэтому мы требуем зафиксировать их в договоре вместе с последствиями задержки.',
  'إن بدء الأعمال في 11 نوفمبر 2025 ورخصة البناء والإنجاز في سبتمبر 2028 مذكورة على بوابة المطوّر، لا في الكتيّب ولا في قائمة الأسعار، لذا نطلب إدراجها في العقد مع ما يترتب على تأخر الموعد.',
  'De start van de werken op 11 november 2025, de bouwvergunning en de oplevering in september 2028 staan in het portaal van de ontwikkelaar, niet in de brochure of de prijslijst. Daarom vragen wij ze in het contract op te nemen, met wat er gebeurt als de datum uitloopt.',
  'Rozpoczęcie prac 11 listopada 2025 r., pozwolenie na budowę i odbiór we wrześniu 2028 r. podaje portal dewelopera, a nie broszura ani cennik, dlatego wymagamy ich wpisania do umowy wraz z tym, co się dzieje w razie opóźnienia.',
  'Byggestart 11. november 2025, byggetillatelsen og ferdigstillelse i september 2028 står på utbyggerens portal, ikke i brosjyren eller prislisten. Derfor ber vi om dem i kontrakten, sammen med hva som skjer hvis datoen glipper.',
  'Byggstarten den 11 november 2025, bygglovet och färdigställandet i september 2028 står på exploatörens portal, inte i broschyren eller prislistan. Därför begär vi dem i kontraktet, tillsammans med vad som gäller om datumet skjuts upp.')
a('.investment.cards[2][0]',
  'Diez de 120 viviendas en la lista', 'Dix logements sur 120 dans la liste', 'Zehn von 120 Wohnungen gelistet', 'В списке десять из 120 квартир',
  'عشرة من 120 مسكناً في القائمة', 'Tien van de 120 woningen op de lijst', 'Dziesięć ze 120 lokali w cenniku', 'Ti av 120 boliger på listen', 'Tio av 120 bostäder på listan')
a('.investment.cards[2][1]',
  'La lista de precios solo muestra las diez viviendas que marca como disponibles. No dice cuántas de las otras 110 están vendidas o reservadas, y el promotor puede revisar los precios antes de una reserva.',
  'La liste de prix ne montre que les dix logements qu’elle indique comme disponibles. Elle ne dit pas combien des 110 autres sont vendus ou réservés, et le promoteur peut réviser les prix avant une réservation.',
  'Die Preisliste zeigt nur die zehn Wohnungen, die sie als verfügbar führt. Sie sagt nicht, wie viele der übrigen 110 verkauft oder reserviert sind, und der Bauträger kann die Preise vor einer Reservierung ändern.',
  'Прайс-лист показывает только десять квартир, отмеченных как доступные. В нём не сказано, сколько из остальных 110 продано или забронировано, а застройщик может изменить цены до бронирования.',
  'لا تعرض قائمة الأسعار سوى المساكن العشرة التي تصنّفها متاحة. ولا تذكر كم من المساكن الـ110 الأخرى بيع أو حُجز، ويمكن للمطوّر تعديل الأسعار قبل الحجز.',
  'De prijslijst toont alleen de tien woningen die zij als beschikbaar aanmerkt. Zij zegt niet hoeveel van de andere 110 verkocht of gereserveerd zijn, en de ontwikkelaar kan de prijzen vóór een reservering aanpassen.',
  'Cennik pokazuje tylko dziesięć lokali oznaczonych jako dostępne. Nie podaje, ile z pozostałych 110 jest sprzedanych lub zarezerwowanych, a deweloper może zmienić ceny przed rezerwacją.',
  'Prislisten viser bare de ti boligene den merker som ledige. Den sier ikke hvor mange av de andre 110 som er solgt eller reservert, og utbyggeren kan endre prisene før en reservasjon.',
  'Prislistan visar bara de tio bostäder den anger som lediga. Den säger inte hur många av de övriga 110 som är sålda eller reserverade, och exploatören kan ändra priserna före en reservation.')
a('.investment.cards[3][0]',
  'Una lista de precios de septiembre', 'Une liste de prix de septembre', 'Eine Preisliste vom September', 'Прайс-лист от сентября',
  'قائمة أسعار من سبتمبر', 'Een prijslijst van september', 'Cennik z września', 'En prisliste fra september', 'En prislista från september')
a('.investment.cards[3][1]',
  'La lista tiene fecha del 14 de septiembre de 2026. Confirmamos cada precio y su disponibilidad con el promotor antes de que usted reserve.',
  'La liste est datée du 14 septembre 2026. Nous confirmons chaque prix et sa disponibilité auprès du promoteur avant que vous ne réserviez.',
  'Die Liste ist auf den 14. September 2026 datiert. Wir bestätigen jeden Preis und seine Verfügbarkeit beim Bauträger, bevor Sie reservieren.',
  'Список датирован 14 сентября 2026 года. Мы подтверждаем каждую цену и наличие у застройщика, прежде чем вы забронируете.',
  'القائمة مؤرخة في 14 سبتمبر 2026. ونؤكد كل سعر وتوفّره مع المطوّر قبل أن تحجزوا.',
  'De lijst is gedateerd 14 september 2026. Wij bevestigen elke prijs en de beschikbaarheid bij de ontwikkelaar voordat u reserveert.',
  'Cennik nosi datę 14 września 2026 r. Każdą cenę i dostępność potwierdzamy u dewelopera, zanim Państwo dokonają rezerwacji.',
  'Listen er datert 14. september 2026. Vi bekrefter hver pris og om boligen er ledig hos utbyggeren før du reserverer.',
  'Listan är daterad den 14 september 2026. Vi bekräftar varje pris och tillgängligheten hos exploatören innan ni reserverar.')
a('.trustDossier.cards[0][1]',
  'El portal indica la licencia de obra como concedida y las obras como iniciadas. Pedimos la propia licencia y el programa de obra.',
  'Le portail indique le permis de construire comme accordé et les travaux comme commencés. Nous demandons le permis lui-même et le calendrier des travaux.',
  'Das Portal nennt die Baugenehmigung als erteilt und den Bau als begonnen. Wir verlangen die Genehmigung selbst und den Bauzeitenplan.',
  'На портале указано, что разрешение на строительство получено и работы начаты. Мы запрашиваем само разрешение и график работ.',
  'تذكر البوابة أن رخصة البناء ممنوحة وأن الأعمال بدأت. ونطلب الرخصة نفسها وبرنامج الأعمال.',
  'Het portaal vermeldt de bouwvergunning als verleend en de werken als gestart. Wij vragen de vergunning zelf en de bouwplanning op.',
  'Portal podaje, że pozwolenie na budowę zostało wydane, a prace ruszyły. Prosimy o samo pozwolenie i harmonogram prac.',
  'Portalen oppgir byggetillatelsen som gitt og byggingen som startet. Vi ber om selve tillatelsen og fremdriftsplanen.',
  'Portalen anger bygglovet som beviljat och bygget som påbörjat. Vi begär själva bygglovet och tidplanen för bygget.')
a('.trustDossier.cards[2][1]',
  'Los precios y las superficies se transcriben de la lista de precios del 14 de septiembre de 2026. Sus superficies son construidas; los planos dan además superficies útiles menores, que no publicamos.',
  'Les prix et les surfaces sont repris de la liste de prix du 14 septembre 2026. Ses surfaces sont construites ; les plans donnent aussi des surfaces utiles plus petites, que nous ne publions pas.',
  'Preise und Flächen sind aus der Preisliste vom 14. September 2026 übernommen. Ihre Flächen sind bebaute Flächen; die Pläne nennen außerdem kleinere Nutzflächen, die wir nicht veröffentlichen.',
  'Цены и площади перенесены из прайс-листа от 14 сентября 2026 года. Его площади — застроенные; на планах также указаны меньшие полезные площади, которые мы не публикуем.',
  'الأسعار والمساحات منقولة من قائمة الأسعار المؤرخة في 14 سبتمبر 2026. ومساحاتها مساحات مبنية، وتذكر المخططات أيضاً مساحات صافية أصغر لا ننشرها.',
  'Prijzen en oppervlaktes zijn overgenomen uit de prijslijst van 14 september 2026. De oppervlaktes zijn bebouwde oppervlaktes; de plattegronden geven ook kleinere netto-oppervlaktes, die wij niet publiceren.',
  'Ceny i powierzchnie przepisano z cennika z 14 września 2026 r. Są to powierzchnie zabudowy; rzuty podają też mniejsze powierzchnie netto, których nie publikujemy.',
  'Priser og arealer er hentet fra prislisten av 14. september 2026. Arealene er bygde arealer; tegningene oppgir også mindre nettoarealer, som vi ikke publiserer.',
  'Priser och ytor är hämtade från prislistan av den 14 september 2026. Ytorna är byggytor; ritningarna anger även mindre nettoytor, som vi inte publicerar.')
a('.trustDossier.cards[4][1]',
  'Las imágenes están generadas por ordenador, los planos están hechos a partir del proyecto básico y no son definitivos, y el mobiliario que se muestra no está incluido.',
  'Les images sont des vues de synthèse, les plans sont établis à partir du projet de base et ne sont pas définitifs, et le mobilier montré n’est pas inclus.',
  'Die Bilder sind computergeneriert, die Pläne beruhen auf dem Grundprojekt und sind nicht endgültig, und die gezeigten Möbel sind nicht enthalten.',
  'Изображения созданы на компьютере, планировки составлены по базовому проекту и не окончательны, а показанная мебель не входит в предложение.',
  'الصور مُنشأة بالحاسوب، والمخططات مُعدّة انطلاقاً من المشروع الأساسي وليست نهائية، والأثاث المعروض غير مشمول.',
  'De beelden zijn computergegenereerd, de plattegronden zijn gebaseerd op het basisproject en niet definitief, en het getoonde meubilair is niet inbegrepen.',
  'Obrazy są wizualizacjami komputerowymi, rzuty opracowano na podstawie projektu podstawowego i nie są ostateczne, a pokazane meble nie są wliczone.',
  'Bildene er datagenererte, tegningene er laget ut fra forprosjektet og er ikke endelige, og møblene som vises er ikke inkludert.',
  'Bilderna är datorgenererade, ritningarna bygger på grundprojektet och är inte slutgiltiga, och möblerna som visas ingår inte.')

# ---- availability ----------------------------------------------------------------------------

a('.availability.copy',
  'Los precios proceden de la lista de precios del promotor con fecha 14 de septiembre de 2026, que muestra 10 viviendas, todas disponibles, de una promoción de 120. Confirmamos precios y disponibilidad antes de cualquier reserva. Los precios no incluyen el {T}.',
  'Les prix proviennent de la liste de prix du promoteur datée du 14 septembre 2026, qui présente 10 logements, tous disponibles, sur une résidence de 120. Nous confirmons les prix et la disponibilité avant toute réservation. Les prix s’entendent hors {T}.',
  'Die Preise stammen aus der Preisliste des Bauträgers vom 14. September 2026, die 10 Wohnungen zeigt, alle verfügbar, in einer Anlage mit 120 Wohnungen. Wir bestätigen Preise und Verfügbarkeit vor jeder Reservierung. Die Preise verstehen sich vor {T}.',
  'Цены взяты из прайс-листа застройщика от 14 сентября 2026 года, в котором 10 квартир, все доступны, из 120 в комплексе. Мы подтверждаем цены и наличие перед любым бронированием. Цены указаны без {T}.',
  'الأسعار مأخوذة من قائمة أسعار المطوّر المؤرخة في 14 سبتمبر 2026، التي تعرض 10 مساكن، كلها متاحة، من مشروع يضم 120 مسكناً. ونؤكد الأسعار والتوفّر قبل أي حجز. والأسعار قبل {T}.',
  'De prijzen komen uit de prijslijst van de ontwikkelaar van 14 september 2026, die 10 woningen toont, alle beschikbaar, in een complex van 120. Wij bevestigen prijzen en beschikbaarheid vóór elke reservering. De prijzen zijn exclusief {T}.',
  'Ceny pochodzą z cennika dewelopera z 14 września 2026 r., który obejmuje 10 lokali, wszystkie dostępne, z osiedla liczącego 120. Ceny i dostępność potwierdzamy przed każdą rezerwacją. Ceny nie obejmują {T}.',
  'Prisene er hentet fra utbyggerens prisliste datert 14. september 2026, som viser 10 boliger, alle ledige, i et anlegg med 120. Vi bekrefter priser og tilgjengelighet før enhver reservasjon. Prisene er før {T}.',
  'Priserna kommer från exploatörens prislista daterad den 14 september 2026, som visar 10 bostäder, alla lediga, i ett område med 120. Vi bekräftar priser och tillgänglighet före varje reservation. Priserna är före {T}.')
a('.availability.sourceNote',
  'Todas las cifras se transcriben de la lista de precios del promotor, con fecha 14 de septiembre de 2026. Muestra diez viviendas, todas marcadas como disponibles, e indica que sus precios son netos, sin {T}, impuesto de transmisiones ni otros cargos, y que puede modificarse mientras no se haya recibido el depósito inicial. En Andalucía se aplican un {T} del 10 % y un AJD del 1,20 %, de modo que el apartamento de {E341000} cuesta unos {E379000} y el ático de {E885000} unos {E984000}, antes de notaría y registro. La superficie construida indicada es la superficie construida interior de la lista, incluido el lavadero cuando lo hay; la terraza suma las terrazas cubiertas y descubiertas de la lista, con el solárium y el jardín por separado. Cada vivienda de la lista tiene una plaza de garaje y un trastero numerados en la misma línea que su precio; los documentos no dicen expresamente que ambos estén incluidos.',
  'Tous les chiffres sont repris de la liste de prix du promoteur, datée du 14 septembre 2026. Elle présente dix logements, tous indiqués comme disponibles, et précise que ses prix sont nets, hors {T}, droits de mutation et autres frais, et qu’elle peut être modifiée tant que l’acompte initial n’a pas été reçu. En Andalousie s’appliquent une {T} de 10 % et un droit de timbre de 1,20 %, si bien que l’appartement à {E341000} revient à environ {E379000} et le penthouse à {E885000} à environ {E984000}, avant frais de notaire et d’enregistrement. La surface construite indiquée est la surface construite intérieure de la liste, buanderie comprise le cas échéant ; la terrasse additionne les terrasses couvertes et ouvertes de la liste, le solarium et le jardin étant donnés à part. Chaque logement de la liste a une place de parking et une cave numérotées sur la même ligne que son prix ; les documents ne disent pas expressément que les deux sont inclus.',
  'Alle Zahlen sind aus der Preisliste des Bauträgers vom 14. September 2026 übernommen. Sie zeigt zehn Wohnungen, alle als verfügbar markiert, und gibt an, dass die Preise netto sind, ohne {T}, Grunderwerbsteuer und sonstige Abgaben, und dass sie geändert werden kann, solange die erste Anzahlung nicht eingegangen ist. In Andalusien fallen 10 % {T} und 1,20 % Stempelsteuer an, sodass die Wohnung zu {E341000} etwa {E379000} und das Penthouse zu {E885000} etwa {E984000} kostet, vor Notar- und Grundbuchkosten. Die angegebene bebaute Fläche ist die bebaute Innenfläche der Liste, einschließlich des Hauswirtschaftsraums, wo es einen gibt; die Terrasse fasst die überdachten und offenen Terrassen der Liste zusammen, Solarium und Garten sind getrennt angegeben. Jede gelistete Wohnung hat einen nummerierten Stellplatz und Abstellraum in derselben Zeile wie ihr Preis; die Unterlagen sagen nicht ausdrücklich, dass beide inbegriffen sind.',
  'Все цифры перенесены из прайс-листа застройщика от 14 сентября 2026 года. В нём десять квартир, все отмечены как доступные; там сказано, что цены указаны нетто, без {T}, налога на передачу имущества и других сборов, и что список может меняться, пока не получен первоначальный депозит. В Андалусии взимаются {T} 10 % и гербовый сбор 1,20 %, так что квартира за {E341000} обойдётся примерно в {E379000}, а пентхаус за {E885000} — примерно в {E984000}, без учёта нотариуса и регистрации. Указанная застроенная площадь — это внутренняя застроенная площадь из списка, включая постирочную, если она есть; терраса — сумма крытых и открытых террас из списка, солярий и сад указаны отдельно. У каждой квартиры из списка в той же строке, что и цена, указаны номера машино-места и кладовой; прямо о том, что они входят в цену, в документах не сказано.',
  'كل الأرقام منقولة من قائمة أسعار المطوّر المؤرخة في 14 سبتمبر 2026. وتعرض عشرة مساكن، كلها مصنّفة متاحة، وتذكر أن أسعارها صافية دون {T} وضريبة نقل الملكية والرسوم الأخرى، وأنه يمكن تعديلها ما دامت الدفعة الأولى لم تُستلم. وتُطبّق في الأندلس {T} بنسبة 10% ورسم دمغة بنسبة 1.20%، فتبلغ كلفة الشقة بسعر {E341000} نحو {E379000} والبنتهاوس بسعر {E885000} نحو {E984000}، قبل رسوم الكاتب العدل والسجل العقاري. والمساحة المبنية المذكورة هي المساحة الداخلية المبنية في القائمة، بما فيها غرفة الغسيل حيث توجد؛ ويجمع التراس التراسات المسقوفة والمكشوفة في القائمة، مع ذكر السولاريوم والحديقة على حدة. ولكل مسكن في القائمة موقف سيارة ومخزن مرقّمان في السطر نفسه مع سعره، ولا تذكر الوثائق صراحةً أنهما مشمولان.',
  'Alle cijfers zijn overgenomen uit de prijslijst van de ontwikkelaar van 14 september 2026. Die toont tien woningen, alle als beschikbaar aangemerkt, en vermeldt dat de prijzen netto zijn, exclusief {T}, overdrachtsbelasting en andere kosten, en dat de lijst kan worden gewijzigd zolang de eerste aanbetaling niet is ontvangen. In Andalusië gelden {T} van 10 % en zegelrecht van 1,20 %, zodat het appartement van {E341000} ongeveer {E379000} kost en de penthouse van {E885000} ongeveer {E984000}, vóór notaris- en registratiekosten. De vermelde bebouwde oppervlakte is de bebouwde binnenoppervlakte van de lijst, inclusief de wasruimte waar die er is; het terras telt de overdekte en open terrassen van de lijst op, met het solarium en de tuin apart. Elke woning op de lijst heeft een genummerde parkeerplaats en berging op dezelfde regel als haar prijs; de documenten zeggen niet uitdrukkelijk dat beide zijn inbegrepen.',
  'Wszystkie liczby przepisano z cennika dewelopera z 14 września 2026 r. Obejmuje on dziesięć lokali, wszystkie oznaczone jako dostępne, i podaje, że ceny są netto, bez {T}, podatku od przeniesienia własności i innych opłat, oraz że cennik może się zmienić, dopóki nie wpłynie pierwsza zaliczka. W Andaluzji obowiązują {T} 10% i opłata skarbowa 1,20%, więc mieszkanie za {E341000} kosztuje około {E379000}, a penthouse za {E885000} około {E984000}, przed kosztami notariusza i rejestru. Podana powierzchnia zabudowy to wewnętrzna powierzchnia zabudowy z cennika, łącznie z pralnią, jeśli jest; taras to suma tarasów zadaszonych i otwartych z cennika, a solarium i ogród podano osobno. Każdy lokal z cennika ma numerowane miejsce w garażu i komórkę w tym samym wierszu co cena; dokumenty nie mówią wprost, że oba są wliczone.',
  'Alle tall er hentet fra utbyggerens prisliste datert 14. september 2026. Den viser ti boliger, alle merket som ledige, og oppgir at prisene er netto, uten {T}, dokumentavgift og andre kostnader, og at listen kan endres så lenge det første depositumet ikke er mottatt. I Andalucía gjelder {T} på 10 % og stempelavgift på 1,20 %, slik at leiligheten til {E341000} koster omkring {E379000} og toppleiligheten til {E885000} omkring {E984000}, før notar- og tinglysingskostnader. Bygget areal er listens innvendige bygde areal, inkludert vaskerom der det finnes; terrassen er summen av listens overbygde og åpne terrasser, med solterrassen og hagen oppgitt for seg. Hver bolig på listen har en nummerert garasjeplass og bod på samme linje som prisen; dokumentene sier ikke uttrykkelig at begge er inkludert.',
  'Alla siffror är hämtade från exploatörens prislista daterad den 14 september 2026. Den visar tio bostäder, alla markerade som lediga, och anger att priserna är nettopriser utan {T}, överlåtelseskatt och andra avgifter, och att listan kan ändras så länge den första handpenningen inte har mottagits. I Andalusien tas {T} på 10 % och stämpelskatt på 1,20 % ut, så lägenheten för {E341000} kostar omkring {E379000} och takvåningen för {E885000} omkring {E984000}, före notarie- och inskrivningskostnader. Den angivna byggytan är listans invändiga byggyta, inklusive tvättstuga där sådan finns; terrassen är summan av listans täckta och öppna terrasser, med solterrassen och trädgården angivna separat. Varje bostad på listan har en numrerad garageplats och ett förråd på samma rad som priset; handlingarna säger inte uttryckligen att båda ingår.')

# unit sizes, in each locale's established wording (agora-residences, alborada-residences, brisamar-residences)
BUILT = {'es': '{} m² construidos', 'fr': '{} m² construits', 'de': '{} m² bebaut', 'ru': '{} м² застроенной площади',
         'ar': '{} م² مبنية', 'nl': '{} m² bebouwd', 'pl': '{} m² zabudowy', 'no': '{} m² bygget', 'sv': '{} m² byggyta'}
PART = {'terrace': {'es': '{} m² de terraza', 'fr': '{} m² de terrasse', 'de': '{} m² Terrasse', 'ru': 'терраса {} м²',
                    'ar': '{} م² تراس', 'nl': '{} m² terras', 'pl': '{} m² tarasu', 'no': '{} m² terrasse', 'sv': '{} m² terrass'},
        'solarium': {'es': '{} m² de solárium', 'fr': '{} m² de solarium', 'de': '{} m² Solarium', 'ru': 'солярий {} м²',
                     'ar': '{} م² سولاريوم', 'nl': '{} m² solarium', 'pl': '{} m² solarium', 'no': '{} m² solterrasse', 'sv': '{} m² solterrass'},
        'garden': {'es': '{} m² de jardín', 'fr': '{} m² de jardin', 'de': '{} m² Garten', 'ru': 'сад {} м²',
                   'ar': '{} م² حديقة', 'nl': '{} m² tuin', 'pl': '{} m² ogrodu', 'no': '{} m² hage', 'sv': '{} m² trädgård'}}
for u in proj['availability']['units']:
    segs = u['size'].split(', ')
    out = {}
    for l in LOCS:
        parts = []
        for i, s in enumerate(segs):
            n, kind = re.fullmatch(r'([\d.]+) sqm (\w+)', s).groups()
            v = num(n, l)
            parts.append(BUILT[l].format(v) if kind == 'built' else PART[kind][l].format(v))
        out[l] = ('، ' if l == 'ar' else ', ').join(parts)
    T[u['size']] = out
for u in proj['availability']['units']:
    if u['bedrooms'] == '1 bedroom':
        T['1 bedroom'] = {'es': '1 dormitorio', 'fr': '1 chambre', 'de': '1 Schlafzimmer', 'ru': '1 спальня', 'ar': 'غرفة نوم واحدة',
                          'nl': '1 slaapkamer', 'pl': '1 sypialnia', 'no': '1 soverom', 'sv': '1 sovrum'}

# ---- construction timeline and payments ------------------------------------------------------

a('.constructionTimeline.headlineHtml',
  'Del inicio de las obras <em>a las llaves</em>', 'Du début des travaux <em>à la remise des clés</em>', 'Vom Baubeginn <em>bis zur Schlüsselübergabe</em>',
  'От начала строительства <em>до ключей</em>', 'من بدء الأعمال <em>حتى تسليم المفاتيح</em>', 'Van de start van de bouw <em>tot de sleutels</em>',
  'Od rozpoczęcia budowy <em>do kluczy</em>', 'Fra byggestart <em>til nøklene</em>', 'Från byggstart <em>till nycklarna</em>')
a('.constructionTimeline.points[0].year',
  'Noviembre de 2025', 'Novembre 2025', 'November 2025', 'Ноябрь 2025', 'نوفمبر 2025', 'November 2025', 'Listopad 2025', 'November 2025', 'November 2025')
a('.constructionTimeline.points[1].year',
  'Septiembre de 2028', 'Septembre 2028', 'September 2028', 'Сентябрь 2028', 'سبتمبر 2028', 'September 2028', 'Wrzesień 2028', 'September 2028', 'September 2028')
a('.constructionTimeline.points[0].label',
  'Inicio de las obras', 'Début des travaux', 'Baubeginn', 'Начало строительства', 'بدء الأعمال', 'Start van de bouw',
  'Rozpoczęcie budowy', 'Byggestart', 'Byggstart')
a('.constructionTimeline.note',
  'El portal del promotor indica la licencia de obra como concedida, el inicio de las obras el 11 de noviembre de 2025 y la entrega en septiembre de 2028. El calendario de pagos vincula el último 60 % a la licencia de primera ocupación y a la escritura. Nueva Living pide por escrito la licencia, el programa de obra y la fecha de entrega, e incorpora la fecha al contrato.',
  'Le portail du promoteur indique le permis de construire comme accordé, le début des travaux le 11 novembre 2025 et la livraison en septembre 2028. L’échéancier lie les derniers 60 % à la licence de première occupation et à l’acte. Nueva Living demande par écrit le permis, le calendrier des travaux et la date de livraison, et inscrit la date dans le contrat.',
  'Das Portal des Bauträgers nennt die Baugenehmigung als erteilt, den Baubeginn am 11. November 2025 und die Fertigstellung im September 2028. Der Zahlungsplan knüpft die letzten 60 % an die Erstbezugsgenehmigung und die Beurkundung. Nueva Living verlangt die Genehmigung, den Bauzeitenplan und den Übergabetermin schriftlich und nimmt den Termin in den Vertrag auf.',
  'На портале застройщика указано, что разрешение на строительство получено, работы начались 11 ноября 2025 года, а сдача — в сентябре 2028 года. График платежей привязывает последние 60 % к лицензии на первое заселение и подписанию купчей. Nueva Living запрашивает разрешение, график работ и дату сдачи в письменном виде и вносит дату в договор.',
  'تذكر بوابة المطوّر أن رخصة البناء ممنوحة، وأن الأعمال بدأت في 11 نوفمبر 2025، وأن الإنجاز في سبتمبر 2028. ويربط جدول الدفعات الـ60% الأخيرة برخصة الإشغال الأول وتوقيع سند الملكية. وتطلب Nueva Living الرخصة وبرنامج الأعمال وموعد التسليم كتابةً، وتُدرج الموعد في العقد.',
  'Het portaal van de ontwikkelaar vermeldt de bouwvergunning als verleend, de start van de werken op 11 november 2025 en de oplevering in september 2028. Het betalingsschema koppelt de laatste 60 % aan de vergunning voor eerste bewoning en de akte. Nueva Living vraagt de vergunning, de bouwplanning en de opleverdatum schriftelijk op en neemt de datum op in het contract.',
  'Portal dewelopera podaje, że pozwolenie na budowę zostało wydane, prace ruszyły 11 listopada 2025 r., a odbiór nastąpi we wrześniu 2028 r. Harmonogram płatności wiąże ostatnie 60% z pozwoleniem na pierwsze użytkowanie i aktem notarialnym. Nueva Living prosi na piśmie o pozwolenie, harmonogram prac i termin odbioru oraz wpisuje termin do umowy.',
  'Utbyggerens portal oppgir byggetillatelsen som gitt, byggestart 11. november 2025 og ferdigstillelse i september 2028. Betalingsplanen knytter de siste 60 % til brukstillatelsen og skjøtet. Nueva Living ber om tillatelsen, fremdriftsplanen og overtakelsesdatoen skriftlig og tar datoen inn i kontrakten.',
  'Exploatörens portal anger bygglovet som beviljat, byggstarten den 11 november 2025 och färdigställandet i september 2028. Betalningsplanen knyter de sista 60 % till inflyttningslicensen och köpebrevet. Nueva Living begär bygglovet, tidplanen och tillträdesdatumet skriftligt och för in datumet i kontraktet.')
a('.constructionTimeline.paymentTerms[0][2]',
  'Al reservar la vivienda', 'À la réservation du logement', 'Bei der Reservierung der Wohnung', 'При бронировании квартиры',
  'عند حجز المسكن', 'Bij de reservering van de woning', 'Przy rezerwacji lokalu', 'Ved reservasjon av boligen', 'Vid reservation av bostaden')
a('.constructionTimeline.paymentTerms[1][2]',
  'En el contrato privado, que el calendario vincula a la licencia de obra',
  'Au contrat privé, que l’échéancier lie au permis de construire',
  'Beim privaten Kaufvertrag, den der Zahlungsplan an die Baugenehmigung knüpft',
  'При подписании частного договора, который график привязывает к разрешению на строительство',
  'عند العقد الخاص، الذي يربطه الجدول برخصة البناء',
  'Bij het koopcontract, dat het schema koppelt aan de bouwvergunning',
  'Przy umowie prywatnej, którą harmonogram wiąże z pozwoleniem na budowę',
  'Ved den private kontrakten, som planen knytter til byggetillatelsen',
  'Vid det privata köpekontraktet, som planen knyter till bygglovet')
a('.constructionTimeline.paymentTerms[2][2]',
  'Seis meses después del contrato privado', 'Six mois après le contrat privé', 'Sechs Monate nach dem privaten Kaufvertrag',
  'Через шесть месяцев после частного договора', 'بعد ستة أشهر من العقد الخاص', 'Zes maanden na het koopcontract',
  'Sześć miesięcy po umowie prywatnej', 'Seks måneder etter den private kontrakten', 'Sex månader efter det privata köpekontraktet')
a('.constructionTimeline.paymentTerms[3][2]',
  'Con la licencia de primera ocupación y la firma de la escritura', 'À la licence de première occupation et à la signature de l’acte',
  'Bei der Erstbezugsgenehmigung und der Beurkundung', 'При получении лицензии на первое заселение и подписании купчей',
  'عند رخصة الإشغال الأول وتوقيع سند الملكية', 'Bij de vergunning voor eerste bewoning en de ondertekening van de akte',
  'Przy pozwoleniu na pierwsze użytkowanie i podpisaniu aktu notarialnego', 'Ved brukstillatelsen og signering av skjøtet',
  'Vid inflyttningslicensen och undertecknandet av köpebrevet')
a('.constructionTimeline.paymentTermsNote',
  'El calendario indica que a cada importe se le suma el {T}. No dice si la reserva se descuenta del 30 %, si las cantidades entregadas a cuenta están avaladas ni a cuánto ascienden los gastos de compra además del precio. Nueva Living pide cada punto por escrito antes de que usted reserve.',
  'L’échéancier précise que la {T} s’ajoute à chaque montant. Il ne dit pas si la réservation est déduite des 30 %, si les sommes versées d’avance sont garanties, ni à combien s’élèvent les frais d’achat en plus du prix. Nueva Living demande chaque point par écrit avant que vous ne réserviez.',
  'Der Zahlungsplan sagt, dass auf jeden Betrag die {T} kommt. Er sagt nicht, ob die Reservierung von den 30 % abgezogen wird, ob Anzahlungen abgesichert sind oder wie hoch die Kaufnebenkosten sind. Nueva Living lässt sich jeden Punkt schriftlich bestätigen, bevor Sie reservieren.',
  'В графике сказано, что к каждой сумме добавляется {T}. В нём не сказано, вычитается ли бронь из 30 %, гарантированы ли авансовые платежи и каковы расходы на покупку сверх цены. Nueva Living запрашивает каждый пункт письменно, прежде чем вы забронируете.',
  'يذكر الجدول أن {T} تُضاف إلى كل مبلغ. ولا يذكر ما إذا كان مبلغ الحجز يُخصم من الـ30%، ولا ما إذا كانت الدفعات المقدمة مضمونة، ولا مقدار تكاليف الشراء الإضافية على السعر. وتطلب Nueva Living كل نقطة كتابةً قبل أن تحجزوا.',
  'Het schema vermeldt dat op elk bedrag {T} komt. Het zegt niet of de reservering van de 30 % wordt afgetrokken, of vooruitbetalingen zijn gegarandeerd, en hoeveel de aankoopkosten bovenop de prijs bedragen. Nueva Living vraagt elk punt schriftelijk op voordat u reserveert.',
  'Harmonogram podaje, że do każdej kwoty dolicza się {T}. Nie mówi, czy rezerwacja jest odliczana od 30%, czy wpłaty zaliczkowe są zabezpieczone ani ile wynoszą koszty zakupu ponad cenę. Nueva Living prosi o każdy z tych punktów na piśmie, zanim Państwo dokonają rezerwacji.',
  'Planen sier at det kommer {T} på hvert beløp. Den sier ikke om reservasjonen trekkes fra de 30 %, om forskuddsbetalinger er sikret, eller hva kjøpskostnadene utover prisen utgjør. Nueva Living ber om hvert punkt skriftlig før du reserverer.',
  'Planen anger att {T} tillkommer på varje belopp. Den säger inte om reservationen dras av från de 30 %, om förskottsbetalningar är säkrade eller vad köpkostnaderna utöver priset uppgår till. Nueva Living begär varje punkt skriftligt innan ni reserverar.')

# ---- next steps, viewing, enquiry ------------------------------------------------------------

a('.timeline.items[0][2]',
  'El número de dormitorios, la planta y si busca un jardín, una gran terraza o un solárium.',
  'Le nombre de chambres, l’étage et si vous cherchez un jardin, une grande terrasse ou un solarium.',
  'Die Zahl der Schlafzimmer, das Geschoss und ob Sie einen Garten, eine große Terrasse oder ein Solarium suchen.',
  'Число спален, этаж и что вам нужно: сад, большая терраса или солярий.',
  'عدد غرف النوم، والطابق، وما إذا كنتم تبحثون عن حديقة أو تراس كبير أو سولاريوم.',
  'Het aantal slaapkamers, de verdieping en of u een tuin, een groot terras of een solarium zoekt.',
  'Liczba sypialni, piętro i to, czy szukają Państwo ogrodu, dużego tarasu czy solarium.',
  'Antall soverom, etasjen og om du ønsker hage, en stor terrasse eller en solterrasse.',
  'Antal sovrum, våningen och om ni vill ha trädgård, en stor terrass eller en solterrass.')
a('.timeline.items[2][2]',
  'Recorremos con usted la obra y la zona, y trasladamos al promotor las preguntas sobre la licencia, el aval y la fecha.',
  'Nous parcourons avec vous le chantier et le quartier, et posons au promoteur les questions sur le permis, la garantie et la date.',
  'Wir besichtigen mit Ihnen die Baustelle und die Umgebung und stellen dem Bauträger die Fragen zu Genehmigung, Bürgschaft und Termin.',
  'Мы вместе с вами осматриваем стройку и район и задаём застройщику вопросы о разрешении, гарантии и сроке.',
  'نتجوّل معكم في موقع البناء والمنطقة، ونطرح على المطوّر الأسئلة المتعلقة بالرخصة والضمان والموعد.',
  'Wij lopen met u over de bouwplaats en door de omgeving, en leggen de vragen over de vergunning, de garantie en de datum voor aan de ontwikkelaar.',
  'Razem z Państwem oglądamy budowę i okolicę oraz zadajemy deweloperowi pytania o pozwolenie, gwarancję i termin.',
  'Vi går over byggeplassen og området sammen med deg, og stiller utbyggeren spørsmålene om tillatelsen, garantien og datoen.',
  'Vi går runt på byggplatsen och i området tillsammans med er, och ställer frågorna om bygglovet, garantin och datumet till exploatören.')
a('.privateViewing.copy',
  'Las viviendas están en construcción, así que una visita se centra en la ubicación, los planos y el calendario.',
  'Les logements sont en construction, une visite porte donc sur l’emplacement, les plans et le calendrier.',
  'Die Wohnungen sind im Bau, daher geht es bei einem Besuch um die Lage, die Pläne und den Zeitplan.',
  'Квартиры строятся, поэтому визит посвящён расположению, планировкам и графику.',
  'المساكن قيد الإنشاء، لذا تتمحور الزيارة حول الموقع والمخططات والجدول الزمني.',
  'De woningen zijn in aanbouw, dus een bezoek draait om de ligging, de plattegronden en de planning.',
  'Lokale są w budowie, więc wizyta dotyczy lokalizacji, rzutów i harmonogramu.',
  'Boligene er under bygging, så et besøk handler om beliggenheten, tegningene og fremdriften.',
  'Bostäderna är under uppförande, så ett besök handlar om läget, ritningarna och tidplanen.')
a('.privateViewing.insights[0][1]',
  'Vea la obra y la ladera, y cómo se orientarán los bloques hacia el jardín y el mar.',
  'Voyez le chantier et le coteau, et comment les bâtiments s’orienteront vers le jardin et la mer.',
  'Sehen Sie die Baustelle und den Hang und wie die Gebäude zum Garten und zum Meer ausgerichtet sein werden.',
  'Посмотрите на стройку и склон и на то, как корпуса будут обращены к саду и морю.',
  'شاهدوا موقع البناء والسفح، وكيف ستتجه المباني نحو الحديقة والبحر.',
  'Bekijk de bouwplaats en de helling, en hoe de blokken op de tuin en de zee gericht zullen zijn.',
  'Proszę zobaczyć budowę i zbocze oraz to, jak budynki będą zwrócone ku ogrodowi i morzu.',
  'Se byggeplassen og åssiden, og hvordan blokkene vil vende mot hagen og havet.',
  'Se byggplatsen och sluttningen, och hur husen kommer att vända sig mot trädgården och havet.')
a('.privateViewing.insights[1][1]',
  'Recorremos con usted las carreteras hasta la autopista, los campos de golf y la costa, y cronometramos los trayectos.',
  'Nous parcourons avec vous les routes vers l’autoroute, les golfs et la côte, en chronométrant les trajets.',
  'Wir fahren mit Ihnen die Strecken zur Autobahn, zu den Golfplätzen und zur Küste und messen die Fahrzeiten.',
  'Мы проезжаем с вами дороги до автомагистрали, гольф-полей и побережья и засекаем время.',
  'نقود معكم على الطرق المؤدية إلى الطريق السريع وملاعب الغولف والساحل ونقيس الوقت.',
  'Wij rijden met u de wegen naar de snelweg, de golfbanen en de kust en klokken de tijden.',
  'Przejeżdżamy z Państwem drogi do autostrady, na pola golfowe i nad morze, mierząc czas przejazdu.',
  'Vi kjører veiene til motorveien, golfbanene og kysten sammen med deg og tar tiden.',
  'Vi kör vägarna till motorvägen, golfbanorna och kusten tillsammans med er och tar tid.')
a('.enquiry.message',
  'Me gustaría conocer la disponibilidad y los precios actuales de Retama Residences.',
  'Je souhaiterais connaître les disponibilités et les prix actuels de Retama Residences.',
  'Ich hätte gern die aktuelle Verfügbarkeit und die Preise von Retama Residences.',
  'Хочу узнать актуальное наличие и цены на Retama Residences.',
  'أرغب في معرفة التوفّر والأسعار الحالية في Retama Residences.',
  'Ik ontvang graag de actuele beschikbaarheid en prijzen van Retama Residences.',
  'Chciałbym poznać aktualną dostępność i ceny w Retama Residences.',
  'Jeg vil gjerne ha oppdatert tilgjengelighet og priser for Retama Residences.',
  'Jag vill gärna ha aktuell tillgänglighet och aktuella priser för Retama Residences.')
a('.enquiry.headlineHtml',
  'Pregunte por <em>Retama Residences</em>', 'Renseignez-vous sur <em>Retama Residences</em>', 'Fragen Sie nach <em>Retama Residences</em>',
  'Узнайте о <em>Retama Residences</em>', 'استفسروا عن <em>Retama Residences</em>', 'Vraag naar <em>Retama Residences</em>',
  'Zapytaj o <em>Retama Residences</em>', 'Spør om <em>Retama Residences</em>', 'Fråga om <em>Retama Residences</em>')

# ---- FAQ -------------------------------------------------------------------------------------

a('.faq[0][1]',
  'El folleto indica que la promoción tiene 120 viviendas. La lista de precios del 14 de septiembre de 2026 muestra diez, todas disponibles: siete apartamentos de uno a tres dormitorios de {E341000} a {E595000} y tres áticos de {E780000} a {E885000}.',
  'La brochure indique 120 logements. La liste de prix du 14 septembre 2026 en présente dix, tous disponibles : sept appartements d’une à trois chambres de {E341000} à {E595000} et trois penthouses de {E780000} à {E885000}.',
  'Die Broschüre nennt 120 Wohnungen. Die Preisliste vom 14. September 2026 zeigt zehn, alle verfügbar: sieben Wohnungen mit einem bis drei Schlafzimmern von {E341000} bis {E595000} und drei Penthouses von {E780000} bis {E885000}.',
  'По буклету в комплексе 120 квартир. В прайс-листе от 14 сентября 2026 года их десять, все доступны: семь квартир с одной–тремя спальнями от {E341000} до {E595000} и три пентхауса от {E780000} до {E885000}.',
  'يذكر الكتيّب أن المشروع يضم 120 مسكناً. وتعرض قائمة الأسعار المؤرخة في 14 سبتمبر 2026 عشرة منها، كلها متاحة: سبع شقق بغرفة إلى ثلاث غرف نوم من {E341000} إلى {E595000}، وثلاث شقق بنتهاوس من {E780000} إلى {E885000}.',
  'Volgens de brochure telt het complex 120 woningen. De prijslijst van 14 september 2026 toont er tien, alle beschikbaar: zeven appartementen met één tot drie slaapkamers van {E341000} tot {E595000} en drie penthouses van {E780000} tot {E885000}.',
  'Według broszury osiedle liczy 120 lokali. Cennik z 14 września 2026 r. obejmuje dziesięć, wszystkie dostępne: siedem mieszkań z jedną do trzech sypialni od {E341000} do {E595000} i trzy penthouse’y od {E780000} do {E885000}.',
  'Ifølge brosjyren har anlegget 120 boliger. Prislisten av 14. september 2026 viser ti, alle ledige: sju leiligheter med ett til tre soverom fra {E341000} til {E595000} og tre toppleiligheter fra {E780000} til {E885000}.',
  'Enligt broschyren har området 120 bostäder. Prislistan av den 14 september 2026 visar tio, alla lediga: sju lägenheter med ett till tre sovrum från {E341000} till {E595000} och tre takvåningar från {E780000} till {E885000}.')
a('.faq[1][1]',
  'No. La lista de precios indica que sus precios son netos y no incluyen el {T} ni el impuesto de transmisiones. Se suman el {T} del 10 % y el AJD del 1,20 %, además de los gastos de notaría y registro.',
  'Non. La liste de prix indique que ses prix sont nets et n’incluent ni la {T} ni les droits de mutation. S’y ajoutent la {T} de 10 % et le droit de timbre de 1,20 %, ainsi que les frais de notaire et d’enregistrement.',
  'Nein. Die Preisliste gibt Nettopreise ohne {T} und Grunderwerbsteuer an. Hinzu kommen 10 % {T} und 1,20 % Stempelsteuer sowie Notar- und Grundbuchkosten.',
  'Нет. В прайс-листе сказано, что цены указаны нетто, без {T} и налога на передачу имущества. Добавляются {T} 10 % и гербовый сбор 1,20 %, а также расходы на нотариуса и регистрацию.',
  'لا. تذكر قائمة الأسعار أن أسعارها صافية ولا تشمل {T} ولا ضريبة نقل الملكية. وتُضاف {T} بنسبة 10% ورسم الدمغة بنسبة 1.20%، إلى جانب رسوم الكاتب العدل والسجل العقاري.',
  'Nee. De prijslijst vermeldt dat de prijzen netto zijn, exclusief {T} en overdrachtsbelasting. Daarbij komen {T} van 10 % en zegelrecht van 1,20 %, plus notaris- en registratiekosten.',
  'Nie. Cennik podaje, że ceny są netto i nie obejmują {T} ani podatku od przeniesienia własności. Dolicza się {T} 10% i opłatę skarbową 1,20% oraz koszty notariusza i rejestru.',
  'Nei. Prislisten oppgir at prisene er netto og ikke inkluderer {T} eller dokumentavgift. I tillegg kommer {T} på 10 % og stempelavgift på 1,20 %, samt notar- og tinglysingskostnader.',
  'Nej. Prislistan anger att priserna är nettopriser utan {T} och överlåtelseskatt. Till det kommer {T} på 10 % och stämpelskatt på 1,20 %, samt notarie- och inskrivningskostnader.')
a('.faq[2][1]',
  'Cada vivienda de la lista tiene una plaza de garaje y un trastero numerados en la misma línea que su precio, y la memoria describe el garaje y sus trasteros. Los documentos no dicen expresamente que ambos estén incluidos en el precio, así que lo confirmamos por escrito.',
  'Chaque logement de la liste a une place de parking et une cave numérotées sur la même ligne que son prix, et le descriptif décrit le garage et ses caves. Les documents ne disent pas expressément que les deux sont compris dans le prix, nous le confirmons donc par écrit.',
  'Jede gelistete Wohnung hat einen nummerierten Stellplatz und Abstellraum in derselben Zeile wie ihr Preis, und die Baubeschreibung beschreibt die Garage und ihre Abstellräume. Die Unterlagen sagen nicht ausdrücklich, dass beides im Preis enthalten ist, daher bestätigen wir es schriftlich.',
  'У каждой квартиры из списка в той же строке, что и цена, указаны номера машино-места и кладовой, а спецификация описывает гараж и кладовые. Прямо о том, что они входят в цену, в документах не сказано, поэтому мы подтверждаем это письменно.',
  'لكل مسكن في القائمة موقف سيارة ومخزن مرقّمان في السطر نفسه مع سعره، وتصف المواصفات المرآب ومخازنه. ولا تذكر الوثائق صراحةً أن كليهما مشمول في السعر، لذا نؤكد ذلك كتابةً.',
  'Elke woning op de lijst heeft een genummerde parkeerplaats en berging op dezelfde regel als haar prijs, en de technische beschrijving beschrijft de garage en de bergingen. De documenten zeggen niet uitdrukkelijk dat beide in de prijs zijn inbegrepen, dus wij bevestigen dat schriftelijk.',
  'Każdy lokal z cennika ma numerowane miejsce w garażu i komórkę w tym samym wierszu co cena, a specyfikacja opisuje garaż i komórki. Dokumenty nie mówią wprost, że oba są wliczone w cenę, dlatego potwierdzamy to na piśmie.',
  'Hver bolig på listen har en nummerert garasjeplass og bod på samme linje som prisen, og byggebeskrivelsen omtaler garasjen og bodene. Dokumentene sier ikke uttrykkelig at begge er inkludert i prisen, så vi bekrefter det skriftlig.',
  'Varje bostad på listan har en numrerad garageplats och ett förråd på samma rad som priset, och byggbeskrivningen beskriver garaget och förråden. Handlingarna säger inte uttryckligen att båda ingår i priset, så vi bekräftar det skriftligt.')
a('.faq[3][1]',
  'El portal del promotor indica la entrega en septiembre de 2028, con la licencia de obra concedida y las obras iniciadas el 11 de noviembre de 2025. Pedimos la fecha en el contrato y lo que ocurre si se retrasa.',
  'Le portail du promoteur indique une livraison en septembre 2028, avec le permis de construire accordé et les travaux commencés le 11 novembre 2025. Nous demandons la date dans le contrat et ce qui se passe en cas de retard.',
  'Das Portal des Bauträgers nennt die Fertigstellung im September 2028, mit erteilter Baugenehmigung und Baubeginn am 11. November 2025. Wir verlangen den Termin im Vertrag und die Regelung für den Fall einer Verzögerung.',
  'На портале застройщика указана сдача в сентябре 2028 года, разрешение на строительство получено, работы начались 11 ноября 2025 года. Мы требуем указать дату в договоре и последствия задержки.',
  'تذكر بوابة المطوّر أن الإنجاز في سبتمبر 2028، مع رخصة بناء ممنوحة وأعمال بدأت في 11 نوفمبر 2025. ونطلب إدراج الموعد في العقد وما يترتب على تأخره.',
  'Het portaal van de ontwikkelaar vermeldt oplevering in september 2028, met verleende bouwvergunning en start van de werken op 11 november 2025. Wij vragen de datum in het contract op te nemen, met wat er gebeurt bij vertraging.',
  'Portal dewelopera podaje odbiór we wrześniu 2028 r., przy wydanym pozwoleniu na budowę i pracach rozpoczętych 11 listopada 2025 r. Wymagamy wpisania terminu do umowy wraz z tym, co się dzieje w razie opóźnienia.',
  'Utbyggerens portal oppgir ferdigstillelse i september 2028, med byggetillatelse gitt og byggestart 11. november 2025. Vi ber om datoen i kontrakten og om hva som skjer hvis den glipper.',
  'Exploatörens portal anger färdigställande i september 2028, med beviljat bygglov och byggstart den 11 november 2025. Vi begär datumet i kontraktet och vad som gäller om det skjuts upp.')
a('.faq[4][1]',
  '{E10000} al reservar, el 30 % en el contrato privado, el 10 % seis meses después y el 60 % con la licencia de primera ocupación y la escritura, más el {T} en cada pago.',
  '{E10000} à la réservation, 30 % au contrat privé, 10 % six mois plus tard et 60 % à la licence de première occupation et à l’acte, plus la {T} sur chaque paiement.',
  '{E10000} bei der Reservierung, 30 % beim privaten Kaufvertrag, 10 % sechs Monate später und 60 % bei der Erstbezugsgenehmigung und der Beurkundung, jeweils zuzüglich {T}.',
  '{E10000} при бронировании, 30 % при частном договоре, 10 % через шесть месяцев и 60 % при лицензии на первое заселение и подписании купчей, плюс {T} к каждому платежу.',
  '{E10000} عند الحجز، و30% عند العقد الخاص، و10% بعد ستة أشهر، و60% عند رخصة الإشغال الأول وتوقيع سند الملكية، مع إضافة {T} إلى كل دفعة.',
  '{E10000} bij de reservering, 30 % bij het koopcontract, 10 % zes maanden later en 60 % bij de vergunning voor eerste bewoning en de akte, telkens plus {T}.',
  '{E10000} przy rezerwacji, 30% przy umowie prywatnej, 10% sześć miesięcy później i 60% przy pozwoleniu na pierwsze użytkowanie i akcie notarialnym, do każdej płatności plus {T}.',
  '{E10000} ved reservasjon, 30 % ved den private kontrakten, 10 % seks måneder senere og 60 % ved brukstillatelsen og skjøtet, med {T} på hver betaling.',
  '{E10000} vid reservationen, 30 % vid det privata köpekontraktet, 10 % sex månader senare och 60 % vid inflyttningslicensen och köpebrevet, med {T} på varje betalning.')
a('.faq[5][1]',
  'Dos piscinas exteriores, un spa con piscina climatizada y sauna, un gimnasio, un salón social con coworking, un salón exterior con barbacoa, un green de putting, una pista de arena, una zona infantil, huertos, un mirador y una zona de conserjería, tal como los recogen los documentos del promotor.',
  'Deux piscines extérieures, un spa avec piscine chauffée et sauna, une salle de sport, un salon commun avec coworking, un salon extérieur avec barbecue, un green de putting, un terrain de sable, un espace enfants, des potagers, un belvédère et une conciergerie, tels que les documents du promoteur les énumèrent.',
  'Zwei Außenpools, ein Spa mit beheiztem Pool und Sauna, ein Fitnessraum, eine Gemeinschaftslounge mit Coworking, eine Außenlounge mit Grill, ein Putting-Green, ein Sandplatz, ein Kinderbereich, Gemüsegärten, ein Aussichtspunkt und ein Concierge-Bereich, wie die Unterlagen des Bauträgers sie aufführen.',
  'Два открытых бассейна, спа с подогреваемым бассейном и сауной, тренажёрный зал, общая гостиная с коворкингом, уличная лаунж-зона с барбекю, паттинг-грин, песчаная площадка, детская зона, огороды, смотровая площадка и консьерж-зона — так их перечисляют документы застройщика.',
  'مسبحان خارجيان، وسبا بمسبح مُدفّأ وساونا، وصالة رياضية، وصالة اجتماعية مع مساحة عمل مشترك، وصالة خارجية مع شواء، وملعب للضربات القصيرة، وملعب رملي، ومنطقة للأطفال، وحدائق خضراوات، ونقطة إطلالة، ومنطقة كونسيرج، كما تذكرها وثائق المطوّر.',
  'Twee buitenzwembaden, een spa met verwarmd zwembad en sauna, een fitnessruimte, een sociale lounge met coworking, een buitenlounge met barbecue, een puttinggreen, een zandveld, een kinderhoek, moestuinen, een uitkijkpunt en een conciërgeruimte, zoals de documenten van de ontwikkelaar ze opsommen.',
  'Dwa baseny zewnętrzne, spa z podgrzewanym basenem i sauną, siłownia, salon wspólny z coworkingiem, zewnętrzny salon z grillem, putting green, piaszczyste boisko, strefa dla dzieci, ogródki warzywne, punkt widokowy i strefa recepcji — tak wymieniają je dokumenty dewelopera.',
  'To utendørs bassenger, et spa med oppvarmet basseng og badstue, treningsrom, en fellesstue med coworking, en utendørs lounge med grill, en puttinggreen, en sandbane, et barneområde, kjøkkenhager, et utsiktspunkt og et resepsjonsområde, slik utbyggerens dokumenter lister dem opp.',
  'Två utomhuspooler, ett spa med uppvärmd pool och bastu, ett gym, en sällskapslounge med coworking, en utomhuslounge med grill, en puttinggreen, en sandplan, en lekyta för barn, köksträdgårdar, en utsiktsplats och en conciergeyta, så som exploatörens handlingar räknar upp dem.')
a('.faq[6][1]',
  'La lista de precios es del promotor y puede revisarse mientras no se haya recibido el depósito inicial. Nueva Living vuelve a confirmar la cifra con el promotor antes de que usted se comprometa a nada.',
  'La liste de prix est celle du promoteur et peut être révisée tant que l’acompte initial n’a pas été reçu. Nueva Living reconfirme le chiffre auprès du promoteur avant que vous ne vous engagiez.',
  'Die Preisliste stammt vom Bauträger und kann geändert werden, solange die erste Anzahlung nicht eingegangen ist. Nueva Living bestätigt den Betrag beim Bauträger erneut, bevor Sie sich zu irgendetwas verpflichten.',
  'Прайс-лист принадлежит застройщику и может быть изменён, пока не получен первоначальный депозит. Nueva Living повторно подтверждает сумму у застройщика, прежде чем вы возьмёте на себя какие-либо обязательства.',
  'قائمة الأسعار صادرة عن المطوّر ويمكن تعديلها ما دامت الدفعة الأولى لم تُستلم. وتعيد Nueva Living تأكيد المبلغ مع المطوّر قبل أن تلتزموا بأي شيء.',
  'De prijslijst is van de ontwikkelaar en kan worden herzien zolang de eerste aanbetaling niet is ontvangen. Nueva Living bevestigt het bedrag opnieuw bij de ontwikkelaar voordat u zich ergens aan verbindt.',
  'Cennik należy do dewelopera i może zostać zmieniony, dopóki nie wpłynie pierwsza zaliczka. Nueva Living ponownie potwierdza kwotę u dewelopera, zanim Państwo podejmą jakiekolwiek zobowiązanie.',
  'Prislisten er utbyggerens og kan endres så lenge det første depositumet ikke er mottatt. Nueva Living bekrefter beløpet på nytt hos utbyggeren før du forplikter deg til noe.',
  'Prislistan är exploatörens och kan ändras så länge den första handpenningen inte har mottagits. Nueva Living bekräftar beloppet på nytt hos exploatören innan ni binder er till något.')

# ---- SEO -------------------------------------------------------------------------------------

a('.seo.title',
  'Retama Residences - Viviendas con spa y piscinas en Mijas Costa',
  'Retama Residences - Logements avec spa et piscines à Mijas Costa',
  'Retama Residences - Wohnungen mit Spa und Pools in Mijas Costa',
  'Retama Residences - квартиры со спа и бассейнами в Михас-Коста',
  'Retama Residences - مساكن مع سبا ومسابح في ميخاس كوستا',
  'Retama Residences - Woningen met spa en zwembaden in Mijas Costa',
  'Retama Residences - Lokale ze spa i basenami w Mijas Costa',
  'Retama Residences - Boliger med spa og bassenger i Mijas Costa',
  'Retama Residences - Bostäder med spa och pooler i Mijas Costa')
a('.seo.h1',
  'Retama Residences: viviendas con spa y piscinas en Mijas Costa',
  'Retama Residences : logements avec spa et piscines à Mijas Costa',
  'Retama Residences: Wohnungen mit Spa und Pools in Mijas Costa',
  'Retama Residences: квартиры со спа и бассейнами в Михас-Коста',
  'Retama Residences: مساكن مع سبا ومسابح في ميخاس كوستا',
  'Retama Residences: woningen met spa en zwembaden in Mijas Costa',
  'Retama Residences: lokale ze spa i basenami w Mijas Costa',
  'Retama Residences: boliger med spa og bassenger i Mijas Costa',
  'Retama Residences: bostäder med spa och pooler i Mijas Costa')
a('.seo.h1Context',
  'Viviendas con spa y piscinas en Mijas Costa', 'Logements avec spa et piscines à Mijas Costa', 'Wohnungen mit Spa und Pools in Mijas Costa',
  'Квартиры со спа и бассейнами в Михас-Коста', 'مساكن مع سبا ومسابح في ميخاس كوستا', 'Woningen met spa en zwembaden in Mijas Costa',
  'Lokale ze spa i basenami w Mijas Costa', 'Boliger med spa og bassenger i Mijas Costa', 'Bostäder med spa och pooler i Mijas Costa')

json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=0)
print('wrote', len(T), 'strings')
