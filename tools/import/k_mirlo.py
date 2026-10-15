# -*- coding: utf-8 -*-
"""Mirlo Residences: the strings the translation memory did not have.

Keyed by the English string, like k_olmo.py. Tokens: {E213000} money, {N64.46} decimal number, {U} the
area unit. Unit sizes, floorplan alts and captions are built from per-locale templates below.
    python3 tools/import/k_mirlo.py <scratch dir>      (writes <dir>/tr_m.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
T = {}
tm = json.load(open(f'{SP}/tm.json'))
FLOORS = json.load(open(f'{SP}/floor_parts.json'))['parts']


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


for s in ['Mirlo Residences', 'Mirlo', 'Mirlo <em>Residences</em>']:
    same(s)

# ---------------------------------------------------------------- identity, prices, date
a('17 of 29 one-, two- and three-bedroom apartments and penthouses in Las Lagunas, Mijas, with terraces and a rooftop pool. Delivery is shown as June 2028 on the developer’s portal. From EUR 213,000 plus VAT.',
  '17 de 29 apartamentos y áticos de uno, dos y tres dormitorios en Las Lagunas, Mijas, con terrazas y piscina en la azotea. El portal del promotor indica la entrega para junio de 2028. Desde {E213000} más IVA.',
  '17 des 29 appartements et penthouses de une, deux et trois chambres à Las Lagunas, Mijas, avec terrasses et piscine sur le toit. Le portail du promoteur indique une livraison en juin 2028. À partir de {E213000} hors TVA.',
  '17 von 29 Wohnungen und Penthäusern mit einem bis drei Schlafzimmern in Las Lagunas, Mijas, mit Terrassen und Dachpool. Das Portal des Bauträgers nennt Juni 2028 als Übergabetermin. Ab {E213000} zuzüglich MwSt.',
  '17 из 29 апартаментов и пентхаусов с одной, двумя и тремя спальнями в Лас-Лагунас, Михас, с террасами и бассейном на крыше. На портале застройщика сдача указана на июнь 2028 года. От {E213000} плюс НДС.',
  '17 من أصل 29 شقة وبنتهاوس بغرفة نوم أو غرفتين أو ثلاث غرف نوم في لاس لاغوناس، ميخاس، مع تراسات ومسبح على السطح. تذكر بوابة المطوّر أن موعد التسليم يونيو 2028. ابتداءً من {E213000} زائد ضريبة القيمة المضافة.',
  '17 van de 29 appartementen en penthouses met een, twee en drie slaapkamers in Las Lagunas, Mijas, met terrassen en een dakzwembad. Het portaal van de ontwikkelaar noemt juni 2028 als opleverdatum. Vanaf {E213000} plus btw.',
  '17 z 29 apartamentów i penthouse\'ów z jedną, dwiema i trzema sypialniami w Las Lagunas, Mijas, z tarasami i basenem na dachu. Portal dewelopera podaje termin oddania: czerwiec 2028 r. Od {E213000} plus VAT.',
  '17 av 29 leiligheter og toppleiligheter med ett, to og tre soverom i Las Lagunas, Mijas, med terrasser og takbasseng. Utbyggerens portal oppgir juni 2028 som overtakelsesdato. Fra {E213000} pluss mva.',
  '17 av 29 lägenheter och takvåningar med ett, två och tre sovrum i Las Lagunas, Mijas, med terrasser och takpool. Exploatörens portal anger juni 2028 som tillträdesdatum. Från {E213000} plus moms.')

a('17 of 29 one-, two- and three-bedroom apartments and penthouses in Las Lagunas, Mijas, with terraces and a rooftop pool, delivery listed for June 2028, from EUR 213,000 plus VAT.',
  '17 de 29 apartamentos y áticos de uno, dos y tres dormitorios en Las Lagunas, Mijas, con terrazas y piscina en la azotea, entrega indicada para junio de 2028, desde {E213000} más IVA.',
  '17 des 29 appartements et penthouses de une, deux et trois chambres à Las Lagunas, Mijas, avec terrasses et piscine sur le toit, livraison indiquée pour juin 2028, à partir de {E213000} hors TVA.',
  '17 von 29 Wohnungen und Penthäusern mit einem bis drei Schlafzimmern in Las Lagunas, Mijas, mit Terrassen und Dachpool, Übergabe laut Portal im Juni 2028, ab {E213000} zuzüglich MwSt.',
  '17 из 29 апартаментов и пентхаусов с одной, двумя и тремя спальнями в Лас-Лагунас, Михас, с террасами и бассейном на крыше, сдача указана на июнь 2028 года, от {E213000} плюс НДС.',
  '17 من أصل 29 شقة وبنتهاوس بغرفة نوم أو غرفتين أو ثلاث غرف نوم في لاس لاغوناس، ميخاس، مع تراسات ومسبح على السطح، والتسليم المذكور في يونيو 2028، ابتداءً من {E213000} زائد ضريبة القيمة المضافة.',
  '17 van de 29 appartementen en penthouses met een, twee en drie slaapkamers in Las Lagunas, Mijas, met terrassen en een dakzwembad, oplevering vermeld voor juni 2028, vanaf {E213000} plus btw.',
  '17 z 29 apartamentów i penthouse\'ów z jedną, dwiema i trzema sypialniami w Las Lagunas, Mijas, z tarasami i basenem na dachu, termin oddania podany na czerwiec 2028 r., od {E213000} plus VAT.',
  '17 av 29 leiligheter og toppleiligheter med ett, to og tre soverom i Las Lagunas, Mijas, med terrasser og takbasseng, overtakelse oppgitt til juni 2028, fra {E213000} pluss mva.',
  '17 av 29 lägenheter och takvåningar med ett, två och tre sovrum i Las Lagunas, Mijas, med terrasser och takpool, tillträde angivet till juni 2028, från {E213000} plus moms.')

a('One-, two- and three-bedroom apartments in Las Lagunas, Mijas, with terraces and a rooftop pool, from EUR 213,000 plus VAT.',
  'Apartamentos de uno, dos y tres dormitorios en Las Lagunas, Mijas, con terrazas y piscina en la azotea, desde {E213000} más IVA.',
  'Appartements de une, deux et trois chambres à Las Lagunas, Mijas, avec terrasses et piscine sur le toit, à partir de {E213000} hors TVA.',
  'Wohnungen mit einem bis drei Schlafzimmern in Las Lagunas, Mijas, mit Terrassen und Dachpool, ab {E213000} zuzüglich MwSt.',
  'Апартаменты с одной, двумя и тремя спальнями в Лас-Лагунас, Михас, с террасами и бассейном на крыше, от {E213000} плюс НДС.',
  'شقق بغرفة نوم أو غرفتين أو ثلاث غرف نوم في لاس لاغوناس، ميخاس، مع تراسات ومسبح على السطح، ابتداءً من {E213000} زائد ضريبة القيمة المضافة.',
  'Appartementen met een, twee en drie slaapkamers in Las Lagunas, Mijas, met terrassen en een dakzwembad, vanaf {E213000} plus btw.',
  'Apartamenty z jedną, dwiema i trzema sypialniami w Las Lagunas, Mijas, z tarasami i basenem na dachu, od {E213000} plus VAT.',
  'Leiligheter med ett, to og tre soverom i Las Lagunas, Mijas, med terrasser og takbasseng, fra {E213000} pluss mva.',
  'Lägenheter med ett, två och tre sovrum i Las Lagunas, Mijas, med terrasser och takpool, från {E213000} plus moms.')

a('From EUR 213,000 + VAT', 'Desde {E213000} + IVA', 'À partir de {E213000} + TVA', 'Ab {E213000} + MwSt.', 'От {E213000} + НДС',
  'ابتداءً من {E213000} + ضريبة القيمة المضافة', 'Vanaf {E213000} + btw', 'Od {E213000} + VAT', 'Fra {E213000} + mva.', 'Från {E213000} + moms')
a('EUR 213,000 + VAT', '{E213000} + IVA', '{E213000} + TVA', '{E213000} + MwSt.', '{E213000} + НДС',
  '{E213000} + ضريبة القيمة المضافة', '{E213000} + btw', '{E213000} + VAT', '{E213000} + mva.', '{E213000} + moms')
a('EUR 213,000 - EUR 429,000 + VAT', '{E213000} - {E429000} + IVA', '{E213000} - {E429000} + TVA', '{E213000} - {E429000} + MwSt.',
  '{E213000} - {E429000} + НДС', '{E213000} - {E429000} + ضريبة القيمة المضافة', '{E213000} - {E429000} + btw',
  '{E213000} - {E429000} + VAT', '{E213000} - {E429000} + mva.', '{E213000} - {E429000} + moms')
a('June 2028', 'junio 2028', 'juin 2028', 'Juni 2028', 'июнь 2028', 'يونيو 2028', 'juni 2028', 'czerwiec 2028', 'juni 2028', 'juni 2028')

a('17 of 29 one-, two- and three-bedroom apartments and penthouses in Las Lagunas, Mijas, with terraces and a rooftop pool.',
  '17 de 29 apartamentos y áticos de uno, dos y tres dormitorios en Las Lagunas, Mijas, con terrazas y piscina en la azotea.',
  '17 des 29 appartements et penthouses de une, deux et trois chambres à Las Lagunas, Mijas, avec terrasses et piscine sur le toit.',
  '17 von 29 Wohnungen und Penthäusern mit einem bis drei Schlafzimmern in Las Lagunas, Mijas, mit Terrassen und Dachpool.',
  '17 из 29 апартаментов и пентхаусов с одной, двумя и тремя спальнями в Лас-Лагунас, Михас, с террасами и бассейном на крыше.',
  '17 من أصل 29 شقة وبنتهاوس بغرفة نوم أو غرفتين أو ثلاث غرف نوم في لاس لاغوناس، ميخاس، مع تراسات ومسبح على السطح.',
  '17 van de 29 appartementen en penthouses met een, twee en drie slaapkamers in Las Lagunas, Mijas, met terrassen en een dakzwembad.',
  '17 z 29 apartamentów i penthouse\'ów z jedną, dwiema i trzema sypialniami w Las Lagunas, Mijas, z tarasami i basenem na dachu.',
  '17 av 29 leiligheter og toppleiligheter med ett, to og tre soverom i Las Lagunas, Mijas, med terrasser og takbasseng.',
  '17 av 29 lägenheter och takvåningar med ett, två och tre sovrum i Las Lagunas, Mijas, med terrasser och takpool.')

# ---------------------------------------------------------------- image alts and captions
a('Computer-generated view of a white corner building with planted balconies and a timber pergola on the roof',
  'Vista generada por ordenador de un edificio blanco en esquina con balcones con plantas y una pérgola de madera en la cubierta',
  'Vue générée par ordinateur d’un immeuble d’angle blanc avec des balcons plantés et une pergola en bois sur le toit',
  'Computergenerierte Ansicht eines weißen Eckgebäudes mit bepflanzten Balkonen und einer Holzpergola auf dem Dach',
  'Компьютерная визуализация белого углового здания с озеленёнными балконами и деревянной перголой на крыше',
  'منظر مولَّد بالحاسوب لمبنى زاوية أبيض بشرفات مزروعة وبرغولا خشبية على السطح',
  'Computergegenereerd beeld van een wit hoekgebouw met beplante balkons en een houten pergola op het dak',
  'Wygenerowany komputerowo widok białego narożnego budynku z obsadzonymi balkonami i drewnianą pergolą na dachu',
  'Datagenerert bilde av en hvit hjørnebygning med beplantede balkonger og en trepergola på taket',
  'Datorgenererad vy av en vit hörnbyggnad med planterade balkonger och en träpergola på taket')
a('Computer-generated view of the white facade with planted balconies and the top floor with its timber pergola',
  'Vista generada por ordenador de la fachada blanca con balcones con plantas y la última planta con su pérgola de madera',
  'Vue générée par ordinateur de la façade blanche avec des balcons plantés et le dernier étage et sa pergola en bois',
  'Computergenerierte Ansicht der weißen Fassade mit bepflanzten Balkonen und dem obersten Geschoss mit seiner Holzpergola',
  'Компьютерная визуализация белого фасада с озеленёнными балконами и верхним этажом с деревянной перголой',
  'منظر مولَّد بالحاسوب للواجهة البيضاء بشرفاتها المزروعة والطابق العلوي وبرغولته الخشبية',
  'Computergegenereerd beeld van de witte gevel met beplante balkons en de bovenste verdieping met houten pergola',
  'Wygenerowany komputerowo widok białej elewacji z obsadzonymi balkonami i górną kondygnacją z drewnianą pergolą',
  'Datagenerert bilde av den hvite fasaden med beplantede balkonger og toppetasjen med trepergolaen',
  'Datorgenererad vy av den vita fasaden med planterade balkonger och översta våningen med sin träpergola')
a('Computer-generated view of a rooftop pool and sun terrace with loungers, planting and the town beyond',
  'Vista generada por ordenador de una piscina en la azotea y una terraza solárium con tumbonas, plantas y la ciudad al fondo',
  'Vue générée par ordinateur d’une piscine sur le toit et d’une terrasse solarium avec des bains de soleil, des plantes et la ville au loin',
  'Computergenerierte Ansicht eines Dachpools und einer Sonnenterrasse mit Liegen, Bepflanzung und der Stadt dahinter',
  'Компьютерная визуализация бассейна на крыше и террасы для загара с шезлонгами, зеленью и городом вдали',
  'منظر مولَّد بالحاسوب لمسبح على السطح وتراس للتشمس بكراسي استلقاء ونباتات والمدينة في الخلفية',
  'Computergegenereerd beeld van een dakzwembad en een zonneterras met ligbedden, beplanting en de stad op de achtergrond',
  'Wygenerowany komputerowo widok basenu na dachu i tarasu do opalania z leżakami, zielenią i miastem w tle',
  'Datagenerert bilde av et takbasseng og en solterrasse med solsenger, beplantning og byen i bakgrunnen',
  'Datorgenererad vy av en takpool och en solterrass med solstolar, planteringar och staden i bakgrunden')
a('Computer-generated open-plan living and dining room with a white sofa, a television and two glazed doors',
  'Salón comedor de planta abierta generado por ordenador con un sofá blanco, un televisor y dos puertas acristaladas',
  'Séjour et salle à manger ouverts générés par ordinateur avec un canapé blanc, un téléviseur et deux portes vitrées',
  'Computergeneriertes offenes Wohn- und Esszimmer mit weißem Sofa, Fernseher und zwei verglasten Türen',
  'Компьютерная визуализация совмещённой гостиной-столовой с белым диваном, телевизором и двумя стеклянными дверями',
  'غرفة معيشة وطعام مفتوحة مولَّدة بالحاسوب مع أريكة بيضاء وتلفاز وبابين زجاجيين',
  'Computergegenereerde open woon- en eetkamer met een witte bank, een televisie en twee glazen deuren',
  'Wygenerowany komputerowo otwarty salon z jadalnią z białą sofą, telewizorem i dwojgiem przeszklonych drzwi',
  'Datagenerert åpen stue og spisestue med hvit sofa, TV og to glassdører',
  'Datorgenererat öppet vardagsrum med matplats, vit soffa, TV och två glasade dörrar')
a('Computer-generated views of the building and its interiors, and the floorplans of 13 of the 17 available homes.',
  'Vistas generadas por ordenador del edificio y de sus interiores, y los planos de 13 de las 17 viviendas disponibles.',
  'Vues générées par ordinateur de l’immeuble et de ses intérieurs, et plans de 13 des 17 logements disponibles.',
  'Computergenerierte Ansichten des Gebäudes und seiner Innenräume sowie die Grundrisse von 13 der 17 verfügbaren Wohnungen.',
  'Компьютерные визуализации здания и его интерьеров, а также планировки 13 из 17 доступных квартир.',
  'مناظر مولَّدة بالحاسوب للمبنى ولمساحاته الداخلية، ومخططات 13 من أصل 17 مسكنًا متاحًا.',
  'Computergegenereerde beelden van het gebouw en de interieurs, en de plattegronden van 13 van de 17 beschikbare woningen.',
  'Wygenerowane komputerowo widoki budynku i jego wnętrz oraz rzuty 13 z 17 dostępnych lokali.',
  'Datagenererte bilder av bygningen og interiørene, og plantegninger av 13 av de 17 ledige boligene.',
  'Datorgenererade vyer av byggnaden och dess interiörer samt planritningar för 13 av de 17 tillgängliga bostäderna.')
# the media note is the Agora note without its last sentence (about Spanish room names, which these plans do not carry)
_agora_note = 'All the photographs are computer-generated images, and the furniture and decoration in them are illustrative and not included. The floorplans are the developer’s and the areas on them are approximate and subject to the final project. The room names on the plans are in Spanish.'
_mine = _agora_note.rsplit('. ', 1)[0] + '.'
assert tm[_agora_note], 'the Agora media note is not in the translation memory'
T[_mine] = {l: tm[_agora_note][l].rsplit('. ', 1)[0] + '.' for l in LOCS}

a('The facade and its balconies', 'La fachada y sus balcones', 'La façade et ses balcons', 'Die Fassade und ihre Balkone', 'Фасад и его балконы',
  'الواجهة وشرفاتها', 'De gevel en de balkons', 'Elewacja i jej balkony', 'Fasaden og balkongene', 'Fasaden och dess balkonger')
a('Computer-generated aerial view of the top-floor terraces under a curved timber pergola, with planting along the edge',
  'Vista aérea generada por ordenador de las terrazas de la última planta bajo una pérgola de madera curva, con plantas a lo largo del borde',
  'Vue aérienne générée par ordinateur des terrasses du dernier étage sous une pergola en bois courbe, avec des plantes le long du bord',
  'Computergenerierte Luftansicht der Terrassen im obersten Geschoss unter einer gerundeten Holzpergola, mit Bepflanzung entlang der Kante',
  'Компьютерная визуализация с высоты: террасы верхнего этажа под изогнутой деревянной перголой с зеленью по краю',
  'منظر جوي مولَّد بالحاسوب لتراسات الطابق العلوي تحت برغولا خشبية منحنية مع نباتات على طول الحافة',
  'Computergegenereerd luchtbeeld van de terrassen op de bovenste verdieping onder een gebogen houten pergola, met beplanting langs de rand',
  'Wygenerowany komputerowo widok z lotu ptaka na tarasy górnej kondygnacji pod zakrzywioną drewnianą pergolą, z zielenią wzdłuż krawędzi',
  'Datagenerert luftbilde av terrassene i toppetasjen under en buet trepergola, med beplantning langs kanten',
  'Datorgenererad flygvy av terrasserna på översta våningen under en böjd träpergola, med planteringar längs kanten')
a('The top-floor terraces from above', 'Las terrazas de la última planta desde arriba', 'Les terrasses du dernier étage vues d’en haut',
  'Die Terrassen im obersten Geschoss von oben', 'Террасы верхнего этажа сверху', 'تراسات الطابق العلوي من الأعلى',
  'De terrassen op de bovenste verdieping van bovenaf', 'Tarasy górnej kondygnacji z góry', 'Terrassene i toppetasjen sett ovenfra',
  'Terrasserna på översta våningen uppifrån')
a('The rooftop pool and sun terrace', 'La piscina en la azotea y la terraza solárium', 'La piscine sur le toit et la terrasse solarium',
  'Der Dachpool und die Sonnenterrasse', 'Бассейн на крыше и терраса для загара', 'المسبح على السطح وتراس التشمس',
  'Het dakzwembad en het zonneterras', 'Basen na dachu i taras do opalania', 'Takbassenget og solterrassen', 'Takpoolen och solterrassen')
a('Computer-generated living room with a white sofa, two woven chairs and a view of the mountains',
  'Salón generado por ordenador con un sofá blanco, dos sillas de fibra trenzada y vistas a las montañas',
  'Salon généré par ordinateur avec un canapé blanc, deux fauteuils en rotin tressé et une vue sur les montagnes',
  'Computergeneriertes Wohnzimmer mit weißem Sofa, zwei Geflechtstühlen und Blick auf die Berge',
  'Компьютерная визуализация гостиной с белым диваном, двумя плетёными креслами и видом на горы',
  'غرفة معيشة مولَّدة بالحاسوب مع أريكة بيضاء وكرسيين مجدولين وإطلالة على الجبال',
  'Computergegenereerde woonkamer met een witte bank, twee rotan stoelen en uitzicht op de bergen',
  'Wygenerowany komputerowo salon z białą sofą, dwoma plecionymi krzesłami i widokiem na góry',
  'Datagenerert stue med hvit sofa, to flettede stoler og utsikt mot fjellene',
  'Datorgenererat vardagsrum med vit soffa, två flätade stolar och utsikt mot bergen')
a('Computer-generated white kitchen with a marble-effect island and two wooden stools',
  'Cocina blanca generada por ordenador con una isla de efecto mármol y dos taburetes de madera',
  'Cuisine blanche générée par ordinateur avec un îlot effet marbre et deux tabourets en bois',
  'Computergenerierte weiße Küche mit einer Kochinsel in Marmoroptik und zwei Holzhockern',
  'Компьютерная визуализация белой кухни с островом под мрамор и двумя деревянными барными стульями',
  'مطبخ أبيض مولَّد بالحاسوب مع جزيرة بمظهر الرخام وكرسيين خشبيين عاليين',
  'Computergegenereerde witte keuken met een eiland in marmerlook en twee houten krukken',
  'Wygenerowana komputerowo biała kuchnia z wyspą w wykończeniu imitującym marmur i dwoma drewnianymi stołkami',
  'Datagenerert hvitt kjøkken med en øy i marmorlook og to barstoler i tre',
  'Datorgenererat vitt kök med en köksö i marmorlook och två barstolar i trä')
a('Kitchen with an island', 'Cocina con isla', 'Cuisine avec îlot', 'Küche mit Kochinsel', 'Кухня с островом', 'مطبخ مع جزيرة',
  'Keuken met eiland', 'Kuchnia z wyspą', 'Kjøkken med øy', 'Kök med köksö')
a('Computer-generated white kitchen with built-in ovens and a dining table by a glazed door',
  'Cocina blanca generada por ordenador con hornos empotrados y una mesa de comedor junto a una puerta acristalada',
  'Cuisine blanche générée par ordinateur avec fours encastrés et une table à manger près d’une porte vitrée',
  'Computergenerierte weiße Küche mit Einbauöfen und einem Esstisch an einer verglasten Tür',
  'Компьютерная визуализация белой кухни со встроенными духовками и обеденным столом у стеклянной двери',
  'مطبخ أبيض مولَّد بالحاسوب مع أفران مدمجة وطاولة طعام قرب باب زجاجي',
  'Computergegenereerde witte keuken met inbouwovens en een eettafel bij een glazen deur',
  'Wygenerowana komputerowo biała kuchnia z piekarnikami do zabudowy i stołem jadalnianym przy przeszklonych drzwiach',
  'Datagenerert hvitt kjøkken med innebygde ovner og et spisebord ved en glassdør',
  'Datorgenererat vitt kök med inbyggda ugnar och ett matbord vid en glasad dörr')
a('Computer-generated bedroom with a double bed, white built-in wardrobes and a sliding glass door to the terrace',
  'Dormitorio generado por ordenador con una cama doble, armarios empotrados blancos y una puerta corredera de cristal a la terraza',
  'Chambre générée par ordinateur avec un lit double, des placards intégrés blancs et une porte coulissante vitrée sur la terrasse',
  'Computergeneriertes Schlafzimmer mit Doppelbett, weißen Einbauschränken und einer gläsernen Schiebetür zur Terrasse',
  'Компьютерная визуализация спальни с двуспальной кроватью, белыми встроенными шкафами и стеклянной раздвижной дверью на террасу',
  'غرفة نوم مولَّدة بالحاسوب مع سرير مزدوج وخزائن مدمجة بيضاء وباب زجاجي منزلق إلى التراس',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, witte inbouwkasten en een glazen schuifdeur naar het terras',
  'Wygenerowana komputerowo sypialnia z podwójnym łóżkiem, białymi szafami wnękowymi i przesuwnymi szklanymi drzwiami na taras',
  'Datagenerert soverom med dobbeltseng, hvite innebygde skap og en skyvedør i glass til terrassen',
  'Datorgenererat sovrum med dubbelsäng, vita inbyggda garderober och en glasskjutdörr till terrassen')
a('Bedroom with a terrace door', 'Dormitorio con puerta a la terraza', 'Chambre avec porte sur la terrasse', 'Schlafzimmer mit Terrassentür',
  'Спальня с дверью на террасу', 'غرفة نوم بباب إلى التراس', 'Slaapkamer met terrasdeur', 'Sypialnia z drzwiami na taras',
  'Soverom med terrassedør', 'Sovrum med terrassdörr')
a('Computer-generated bedroom with a double bed, a pendant lamp, a floating bedside shelf and a framed painting',
  'Dormitorio generado por ordenador con una cama doble, una lámpara colgante, una balda de cabecera flotante y un cuadro enmarcado',
  'Chambre générée par ordinateur avec un lit double, une suspension, une tablette de chevet flottante et un tableau encadré',
  'Computergeneriertes Schlafzimmer mit Doppelbett, einer Pendelleuchte, einem schwebenden Nachttisch und einem gerahmten Bild',
  'Компьютерная визуализация спальни с двуспальной кроватью, подвесным светильником, подвесной прикроватной полкой и картиной в раме',
  'غرفة نوم مولَّدة بالحاسوب مع سرير مزدوج ومصباح معلّق ورف عائم بجانب السرير ولوحة مؤطرة',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een hanglamp, een zwevende nachtplank en een ingelijst schilderij',
  'Wygenerowana komputerowo sypialnia z podwójnym łóżkiem, lampą wiszącą, wiszącą półką przy łóżku i obrazem w ramie',
  'Datagenerert soverom med dobbeltseng, en hengelampe, en svevende hylle ved sengen og et innrammet maleri',
  'Datorgenererat sovrum med dubbelsäng, en taklampa, en svävande hylla vid sängen och en inramad målning')
a('Computer-generated bathroom with a walk-in shower, a round lit mirror and a wall-hung vanity unit',
  'Baño generado por ordenador con una ducha a ras de suelo, un espejo redondo iluminado y un mueble de lavabo suspendido',
  'Salle de bain générée par ordinateur avec une douche à l’italienne, un miroir rond éclairé et un meuble vasque suspendu',
  'Computergeneriertes Badezimmer mit bodengleicher Dusche, einem runden beleuchteten Spiegel und einem wandhängenden Waschtischunterschrank',
  'Компьютерная визуализация ванной комнаты с душем без поддона, круглым зеркалом с подсветкой и подвесной тумбой с раковиной',
  'حمام مولَّد بالحاسوب مع دش مفتوح ومرآة دائرية مضاءة ووحدة مغسلة معلّقة على الجدار',
  'Computergegenereerde badkamer met een inloopdouche, een ronde verlichte spiegel en een zwevend badmeubel',
  'Wygenerowana komputerowo łazienka z prysznicem bez brodzika, okrągłym podświetlanym lustrem i wiszącą szafką pod umywalkę',
  'Datagenerert bad med åpen dusj, et rundt opplyst speil og en veggfast servantskap',
  'Datorgenererat badrum med en öppen dusch, en rund upplyst spegel och ett väggmonterat tvättställsskåp')
a('Computer-generated covered terrace with a timber ceiling, a lounger and planting along the edge',
  'Terraza cubierta generada por ordenador con un techo de madera, una tumbona y plantas a lo largo del borde',
  'Terrasse couverte générée par ordinateur avec un plafond en bois, un bain de soleil et des plantes le long du bord',
  'Computergenerierte überdachte Terrasse mit Holzdecke, einer Liege und Bepflanzung entlang der Kante',
  'Компьютерная визуализация террасы под навесом с деревянным потолком, шезлонгом и зеленью по краю',
  'تراس مسقوف مولَّد بالحاسوب بسقف خشبي وكرسي استلقاء ونباتات على طول الحافة',
  'Computergegenereerd overdekt terras met een houten plafond, een ligbed en beplanting langs de rand',
  'Wygenerowany komputerowo zadaszony taras z drewnianym sufitem, leżakiem i zielenią wzdłuż krawędzi',
  'Datagenerert overbygd terrasse med tretak, en solseng og beplantning langs kanten',
  'Datorgenererad övertäckt terrass med trätak, en solstol och planteringar längs kanten')
a('Computer-generated covered terrace with armchairs, a lounger and hedging along the edge',
  'Terraza cubierta generada por ordenador con butacas, una tumbona y setos a lo largo del borde',
  'Terrasse couverte générée par ordinateur avec des fauteuils, un bain de soleil et une haie le long du bord',
  'Computergenerierte überdachte Terrasse mit Sesseln, einer Liege und einer Hecke entlang der Kante',
  'Компьютерная визуализация террасы под навесом с креслами, шезлонгом и живой изгородью по краю',
  'تراس مسقوف مولَّد بالحاسوب مع كراسي بذراعين وكرسي استلقاء وسياج نباتي على طول الحافة',
  'Computergegenereerd overdekt terras met fauteuils, een ligbed en een haag langs de rand',
  'Wygenerowany komputerowo zadaszony taras z fotelami, leżakiem i żywopłotem wzdłuż krawędzi',
  'Datagenerert overbygd terrasse med lenestoler, en solseng og hekk langs kanten',
  'Datorgenererad övertäckt terrass med fåtöljer, en solstol och en häck längs kanten')
a('Computer-generated terrace under a timber pergola with a lounger and a sky view',
  'Terraza generada por ordenador bajo una pérgola de madera con una tumbona y vistas al cielo',
  'Terrasse générée par ordinateur sous une pergola en bois avec un bain de soleil et vue sur le ciel',
  'Computergenerierte Terrasse unter einer Holzpergola mit einer Liege und Blick in den Himmel',
  'Компьютерная визуализация террасы под деревянной перголой с шезлонгом и видом на небо',
  'تراس مولَّد بالحاسوب تحت برغولا خشبية مع كرسي استلقاء وإطلالة على السماء',
  'Computergegenereerd terras onder een houten pergola met een ligbed en uitzicht op de lucht',
  'Wygenerowany komputerowo taras pod drewnianą pergolą z leżakiem i widokiem na niebo',
  'Datagenerert terrasse under en trepergola med en solseng og utsikt mot himmelen',
  'Datorgenererad terrass under en träpergola med en solstol och utsikt mot himlen')
a('A terrace under the pergola', 'Una terraza bajo la pérgola', 'Une terrasse sous la pergola', 'Eine Terrasse unter der Pergola',
  'Терраса под перголой', 'تراس تحت البرغولا', 'Een terras onder de pergola', 'Taras pod pergolą', 'En terrasse under pergolaen',
  'En terrass under pergolan')

# floorplan alts and captions: "Floorplan of home 2, ground floor" / "Home 2, ground floor"
PLAN = {
    'es': ('Plano de la vivienda {n}, {f}', 'Vivienda {n}, {f}'),
    'fr': ('Plan du logement {n}, {f}', 'Logement {n}, {f}'),
    'de': ('Grundriss der Wohnung {n}, {f}', 'Wohnung {n}, {f}'),
    'ru': ('Планировка квартиры {n}, {f}', 'Квартира {n}, {f}'),
    'ar': ('مخطط المسكن {n}، {f}', 'المسكن {n}، {f}'),
    'nl': ('Plattegrond van woning {n}, {f}', 'Woning {n}, {f}'),
    'pl': ('Rzut lokalu {n}, {f}', 'Lokal {n}, {f}'),
    'no': ('Plantegning av bolig {n}, {f}', 'Bolig {n}, {f}'),
    'sv': ('Planritning för bostad {n}, {f}', 'Bostad {n}, {f}'),
}


def floor_word(en, l):
    w = FLOORS[en][l]
    # German keeps the noun capital (Erdgeschoss, Penthouse) but lowers the ordinal (erstes Obergeschoss)
    if l == 'de':
        return w[0].lower() + w[1:] if w.split()[0] in ('Erstes', 'Zweites') else w
    return w if l == 'ar' else w[0].lower() + w[1:]


proj = json.load(open('content/liora-projects/mirlo-residences/project.json'))
for it in proj['media']['items']:
    if it['category'] != 'Floorplans':
        continue
    m = re.fullmatch(r'Floorplan of home (\d+), (.+)', it['alt'])
    n, fl = m.groups()
    assert it['caption'] == f'Home {n}, {fl}'
    T[it['alt']] = {l: PLAN[l][0].format(n=n, f=floor_word(fl, l)) for l in LOCS}
    T[it['caption']] = {l: PLAN[l][1].format(n=n, f=floor_word(fl, l)) for l in LOCS}

# unit sizes: derived from the Sotavento overlays (built, interior, terrace), one template per language
sot = json.load(open('content/liora-projects/sotavento-residences/project.json'))
u0 = sot['availability']['units'][0]
assert u0['size'] == '182.65 sqm built, 125.62 sqm interior, 50.54 sqm terrace, 169.61 sqm garden'
SIZE = {}
for l in LOCS:
    s = sot['i18n'][l]['availability']['units'][0]['size']
    parts = [p.strip() for p in re.split(r'،|, ', s)]
    assert len(parts) == 4, (l, s)
    tmpl = [re.sub(r'\d+[.,]\d+', '{}', p) for p in parts]
    SIZE[l] = tmpl[:3]     # built, interior, terrace
for u in proj['availability']['units']:
    same(u['reference'])
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm interior(?:, ([\d.]+) sqm terrace)?', u['size'])
    assert m, u['size']
    b, i, t = m.groups()
    out = []
    for l in LOCS:
        val = [num(b, l), num(i, l)] + ([num(t, l)] if t else [])
        parts = [SIZE[l][k].format(val[k]) for k in range(len(val))]
        out.append(('، ' if l == 'ar' else ', ').join(parts))
    T[u['size']] = dict(zip(LOCS, out))

# ---------------------------------------------------------------- overview, why, architecture
a('Twenty-nine homes, <em>seventeen listed</em>', 'Veintinueve viviendas, <em>diecisiete en lista</em>', 'Vingt-neuf logements, <em>dix-sept en vente</em>',
  'Neunundzwanzig Wohnungen, <em>siebzehn gelistet</em>', 'Двадцать девять квартир, <em>семнадцать в продаже</em>',
  'تسعة وعشرون مسكنًا، <em>سبعة عشر منها معروضة</em>', 'Negenentwintig woningen, <em>zeventien vermeld</em>',
  'Dwadzieścia dziewięć lokali, <em>siedemnaście w ofercie</em>', 'Tjueni boliger, <em>sytten oppført</em>', 'Tjugonio bostäder, <em>sjutton listade</em>')
a('Mirlo Residences is a development of 29 homes with one, two and three bedrooms in Las Lagunas de Mijas, with terraces and a rooftop pool. The developer’s portal lists 17 as available, from a one-bedroom apartment on the ground floor to a two-bedroom penthouse with a 42.15 sqm terrace.',
  'Mirlo Residences es una promoción de 29 viviendas de uno, dos y tres dormitorios en Las Lagunas de Mijas, con terrazas y piscina en la azotea. El portal del promotor lista 17 como disponibles, desde un apartamento de un dormitorio en planta baja hasta un ático de dos dormitorios con una terraza de {N42.15} {U}.',
  'Mirlo Residences est un programme de 29 logements de une, deux et trois chambres à Las Lagunas de Mijas, avec terrasses et piscine sur le toit. Le portail du promoteur en indique 17 comme disponibles, d’un appartement d’une chambre au rez-de-chaussée à un penthouse de deux chambres avec une terrasse de {N42.15} {U}.',
  'Mirlo Residences ist ein Projekt mit 29 Wohnungen mit einem, zwei und drei Schlafzimmern in Las Lagunas de Mijas, mit Terrassen und Dachpool. Das Portal des Bauträgers führt 17 als verfügbar auf, von einem Apartment mit einem Schlafzimmer im Erdgeschoss bis zu einem Penthouse mit zwei Schlafzimmern und einer Terrasse von {N42.15} {U}.',
  'Mirlo Residences — комплекс из 29 квартир с одной, двумя и тремя спальнями в Лас-Лагунас-де-Михас, с террасами и бассейном на крыше. На портале застройщика 17 из них указаны как доступные: от апартаментов с одной спальней на первом этаже до пентхауса с двумя спальнями и террасой {N42.15} {U}.',
  'مشروع Mirlo Residences يضم 29 مسكنًا بغرفة نوم أو غرفتين أو ثلاث غرف نوم في لاس لاغوناس دي ميهاس، مع تراسات ومسبح على السطح. تعرض بوابة المطوّر 17 منها كمتاحة، من شقة بغرفة نوم واحدة في الطابق الأرضي إلى بنتهاوس بغرفتي نوم مع تراس مساحته {N42.15} {U}.',
  'Mirlo Residences is een project van 29 woningen met een, twee en drie slaapkamers in Las Lagunas de Mijas, met terrassen en een dakzwembad. Het portaal van de ontwikkelaar vermeldt er 17 als beschikbaar, van een appartement met een slaapkamer op de begane grond tot een penthouse met twee slaapkamers en een terras van {N42.15} {U}.',
  'Mirlo Residences to inwestycja obejmująca 29 lokali z jedną, dwiema i trzema sypialniami w Las Lagunas de Mijas, z tarasami i basenem na dachu. Portal dewelopera wymienia 17 jako dostępne, od apartamentu z jedną sypialnią na parterze po penthouse z dwiema sypialniami i tarasem o powierzchni {N42.15} {U}.',
  'Mirlo Residences er et prosjekt med 29 boliger med ett, to og tre soverom i Las Lagunas de Mijas, med terrasser og takbasseng. Utbyggerens portal oppfører 17 som ledige, fra en leilighet med ett soverom i første etasje til en toppleilighet med to soverom og en terrasse på {N42.15} {U}.',
  'Mirlo Residences är ett projekt med 29 bostäder med ett, två och tre sovrum i Las Lagunas de Mijas, med terrasser och takpool. Exploatörens portal listar 17 som lediga, från en lägenhet med ett sovrum på bottenvåningen till en takvåning med två sovrum och en terrass på {N42.15} {U}.')
a('The portal gives June 2028 as the delivery date. The documents say neither whether the building licence is granted nor how far the works have gone, so we ask for both before any reservation.',
  'El portal indica junio de 2028 como fecha de entrega. Los documentos no dicen si la licencia de obras está concedida ni hasta dónde han llegado las obras, por lo que pedimos ambas cosas antes de cualquier reserva.',
  'Le portail indique juin 2028 comme date de livraison. Les documents ne disent ni si le permis de construire est accordé ni où en sont les travaux ; nous demandons donc les deux avant toute réservation.',
  'Das Portal nennt Juni 2028 als Übergabetermin. Die Unterlagen sagen weder, ob die Baugenehmigung erteilt ist, noch, wie weit die Arbeiten sind; beides fragen wir daher vor jeder Reservierung an.',
  'На портале срок сдачи указан как июнь 2028 года. В документах не сказано ни о том, получено ли разрешение на строительство, ни о том, как далеко продвинулись работы, поэтому мы запрашиваем и то и другое перед любым бронированием.',
  'تذكر البوابة يونيو 2028 موعدًا للتسليم. ولا تذكر الوثائق ما إذا كانت رخصة البناء ممنوحة ولا إلى أي مرحلة وصلت الأعمال، لذلك نطلب الأمرين قبل أي حجز.',
  'Het portaal noemt juni 2028 als opleverdatum. De documenten vermelden niet of de bouwvergunning is verleend en ook niet hoe ver de werkzaamheden zijn, dus we vragen om beide vóór elke reservering.',
  'Portal podaje czerwiec 2028 r. jako termin oddania. Dokumenty nie mówią, czy pozwolenie na budowę zostało wydane, ani na jakim etapie są prace, dlatego przed każdą rezerwacją prosimy o jedno i drugie.',
  'Portalen oppgir juni 2028 som overtakelsesdato. Dokumentene sier verken om byggetillatelsen er gitt eller hvor langt arbeidene har kommet, så vi ber om begge deler før enhver reservasjon.',
  'Portalen anger juni 2028 som tillträdesdatum. Dokumenten säger varken om bygglovet är beviljat eller hur långt arbetena har kommit, så vi ber om båda före varje bokning.')
a('29 homes', '29 viviendas', '29 logements', '29 Wohnungen', '29 квартир', '29 مسكنًا', '29 woningen', '29 lokali', '29 boliger', '29 bostäder')
a('17 homes', '17 viviendas', '17 logements', '17 Wohnungen', '17 квартир', '17 مسكنًا', '17 woningen', '17 lokali', '17 boliger', '17 bostäder')
a('Terraces, and a rooftop pool and solarium', 'Terrazas, y piscina y solárium en la azotea', 'Terrasses, et piscine et solarium sur le toit',
  'Terrassen sowie Dachpool und Dachsolarium', 'Террасы, бассейн и солярий на крыше', 'تراسات، ومسبح وسولاريوم على السطح',
  'Terrassen, en een dakzwembad en solarium op het dak', 'Tarasy oraz basen i solarium na dachu', 'Terrasser, og takbasseng og solterrasse på taket',
  'Terrasser samt takpool och solterrass på taket')
a('New one-, two- and three-bedroom homes in Las Lagunas, in a building of 29 with a rooftop pool.',
  'Viviendas nuevas de uno, dos y tres dormitorios en Las Lagunas, en un edificio de 29 con piscina en la azotea.',
  'Des logements neufs de une, deux et trois chambres à Las Lagunas, dans un immeuble de 29 avec piscine sur le toit.',
  'Neue Wohnungen mit einem, zwei und drei Schlafzimmern in Las Lagunas, in einem Gebäude mit 29 Einheiten und Dachpool.',
  'Новые квартиры с одной, двумя и тремя спальнями в Лас-Лагунас, в здании на 29 квартир с бассейном на крыше.',
  'مساكن جديدة بغرفة نوم أو غرفتين أو ثلاث غرف نوم في لاس لاغوناس، ضمن مبنى من 29 مسكنًا مع مسبح على السطح.',
  'Nieuwe woningen met een, twee en drie slaapkamers in Las Lagunas, in een gebouw van 29 met een dakzwembad.',
  'Nowe lokale z jedną, dwiema i trzema sypialniami w Las Lagunas, w budynku z 29 lokalami i basenem na dachu.',
  'Nye boliger med ett, to og tre soverom i Las Lagunas, i en bygning med 29 boliger og takbasseng.',
  'Nya bostäder med ett, två och tre sovrum i Las Lagunas, i en byggnad med 29 bostäder och takpool.')
a('Buyers who want a new apartment with a terrace between Mijas Costa and Fuengirola, as a main home or a second home.',
  'Compradores que buscan un apartamento nuevo con terraza entre Mijas Costa y Fuengirola, como vivienda principal o segunda residencia.',
  'Acquéreurs qui recherchent un appartement neuf avec terrasse entre Mijas Costa et Fuengirola, comme résidence principale ou secondaire.',
  'Käufer, die eine neue Wohnung mit Terrasse zwischen Mijas Costa und Fuengirola suchen, als Hauptwohnsitz oder Zweitwohnung.',
  'Покупателям, которые ищут новые апартаменты с террасой между Михас-Коста и Фуэнхиролой — для постоянного проживания или как второе жильё.',
  'للمشترين الذين يبحثون عن شقة جديدة بتراس بين ميخاس كوستا وفوينخيرولا، كمسكن رئيسي أو ثانٍ.',
  'Kopers die een nieuw appartement met terras willen tussen Mijas Costa en Fuengirola, als hoofdverblijf of tweede woning.',
  'Dla kupujących, którzy szukają nowego apartamentu z tarasem między Mijas Costa a Fuengirolą, jako stałego miejsca zamieszkania lub drugiego domu.',
  'Kjøpere som vil ha en ny leilighet med terrasse mellom Mijas Costa og Fuengirola, som hovedbolig eller andrebolig.',
  'Köpare som vill ha en ny lägenhet med terrass mellan Mijas Costa och Fuengirola, som permanentbostad eller andra bostad.')
a('A building of only 29 homes with a rooftop pool and solarium, and a garage space and a storeroom assigned to each listed home.',
  'Un edificio de solo 29 viviendas con piscina y solárium en la azotea, y una plaza de garaje y un trastero asignados a cada vivienda de la lista.',
  'Un immeuble de seulement 29 logements avec piscine et solarium sur le toit, et une place de garage et un débarras attribués à chaque logement de la liste.',
  'Ein Gebäude mit nur 29 Wohnungen, mit Dachpool und Dachsolarium sowie einem Garagenstellplatz und einem Abstellraum für jede gelistete Wohnung.',
  'Здание всего на 29 квартир с бассейном и солярием на крыше; за каждой квартирой из списка закреплены место в гараже и кладовая.',
  'مبنى من 29 مسكنًا فقط مع مسبح وسولاريوم على السطح، وموقف في المرآب ومخزن مخصصان لكل مسكن مدرج في القائمة.',
  'Een gebouw van slechts 29 woningen met een dakzwembad en solarium op het dak, en een garageplaats en een berging die aan elke vermelde woning zijn toegewezen.',
  'Budynek zaledwie z 29 lokalami, z basenem i solarium na dachu oraz miejscem garażowym i komórką lokatorską przypisanymi do każdego lokalu z oferty.',
  'En bygning med bare 29 boliger, med takbasseng og solterrasse på taket, og en garasjeplass og en bod tildelt hver oppførte bolig.',
  'En byggnad med bara 29 bostäder, med takpool och solterrass på taket, samt en garageplats och ett förråd tilldelade varje listad bostad.')
a('Las Lagunas de Mijas is an established residential area, a few minutes from the beaches of Mijas Costa and next to the A-7 and AP-7 motorways.',
  'Las Lagunas de Mijas es una zona residencial consolidada, a pocos minutos de las playas de Mijas Costa y junto a las autovías A-7 y AP-7.',
  'Las Lagunas de Mijas est un quartier résidentiel établi, à quelques minutes des plages de Mijas Costa et à côté des autoroutes A-7 et AP-7.',
  'Las Lagunas de Mijas ist ein etabliertes Wohngebiet, wenige Minuten von den Stränden von Mijas Costa entfernt und direkt an den Autobahnen A-7 und AP-7.',
  'Лас-Лагунас-де-Михас — сложившийся жилой район в нескольких минутах от пляжей Михас-Коста, рядом с автомагистралями A-7 и AP-7.',
  'لاس لاغوناس دي ميهاس منطقة سكنية راسخة، على بعد بضع دقائق من شواطئ ميخاس كوستا وبجوار الطريقين السريعين A-7 وAP-7.',
  'Las Lagunas de Mijas is een gevestigde woonwijk, enkele minuten van de stranden van Mijas Costa en vlak bij de snelwegen A-7 en AP-7.',
  'Las Lagunas de Mijas to ugruntowana okolica mieszkalna, kilka minut od plaż Mijas Costa i przy autostradach A-7 i AP-7.',
  'Las Lagunas de Mijas er et etablert boligområde, noen få minutter fra strendene i Mijas Costa og ved motorveiene A-7 og AP-7.',
  'Las Lagunas de Mijas är ett etablerat bostadsområde, några minuter från stränderna i Mijas Costa och intill motorvägarna A-7 och AP-7.')
a('17 of the 29 homes are listed. Nueva Living reconfirms price and availability with the developer before any viewing.',
  'Hay 17 de las 29 viviendas en lista. Nueva Living vuelve a confirmar precio y disponibilidad con el promotor antes de cualquier visita.',
  '17 des 29 logements sont en vente. Nueva Living reconfirme le prix et la disponibilité auprès du promoteur avant toute visite.',
  '17 der 29 Wohnungen sind gelistet. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung erneut beim Bauträger.',
  'В продаже 17 из 29 квартир. Nueva Living повторно подтверждает цену и наличие у застройщика перед любым просмотром.',
  'تُعرض 17 من أصل 29 مسكنًا. وتعيد Nueva Living تأكيد السعر والتوافر مع المطوّر قبل أي معاينة.',
  '17 van de 29 woningen zijn vermeld. Nueva Living bevestigt prijs en beschikbaarheid opnieuw bij de ontwikkelaar vóór elke bezichtiging.',
  'W ofercie jest 17 z 29 lokali. Nueva Living ponownie potwierdza cenę i dostępność u dewelopera przed każdym oglądaniem.',
  '17 av de 29 boligene er oppført. Nueva Living bekrefter pris og tilgjengelighet på nytt hos utbyggeren før enhver visning.',
  '17 av de 29 bostäderna är listade. Nueva Living bekräftar pris och tillgänglighet på nytt hos exploatören före varje visning.')

a('White walls, <em>timber and planting</em>', 'Muros blancos, <em>madera y vegetación</em>', 'Murs blancs, <em>bois et plantations</em>',
  'Weiße Wände, <em>Holz und Bepflanzung</em>', 'Белые стены, <em>дерево и зелень</em>', 'جدران بيضاء، <em>وخشب ونباتات</em>',
  'Witte muren, <em>hout en beplanting</em>', 'Białe ściany, <em>drewno i zieleń</em>', 'Hvite vegger, <em>tre og beplantning</em>',
  'Vita väggar, <em>trä och planteringar</em>')
a('The brochure describes pure lines and Mediterranean white in dialogue with nature, with the design putting light and the use of space first. The renders show a timber pergola along the roof and planting along the balcony edges.',
  'El folleto describe líneas puras y blanco mediterráneo en diálogo con la naturaleza, con un diseño que da prioridad a la luz y al aprovechamiento del espacio. Las imágenes muestran una pérgola de madera a lo largo de la cubierta y vegetación en los bordes de los balcones.',
  'La brochure décrit des lignes pures et un blanc méditerranéen en dialogue avec la nature, une conception qui privilégie la lumière et l’optimisation de l’espace. Les images montrent une pergola en bois le long du toit et des plantes au bord des balcons.',
  'Die Broschüre beschreibt klare Linien und mediterranes Weiß im Dialog mit der Natur, wobei der Entwurf Licht und Raumnutzung an die erste Stelle setzt. Die Darstellungen zeigen eine Holzpergola entlang des Dachs und Bepflanzung an den Balkonkanten.',
  'В брошюре описаны чистые линии и средиземноморский белый цвет в диалоге с природой; в проекте на первом месте свет и рациональное использование пространства. На визуализациях видны деревянная пергола вдоль крыши и зелень по краям балконов.',
  'يصف الكتيّب خطوطًا نقية وبياضًا متوسطيًا في حوار مع الطبيعة، مع تصميم يعطي الأولوية للضوء وحسن استغلال المساحة. وتُظهر الصور برغولا خشبية على امتداد السطح ونباتات على حواف الشرفات.',
  'De brochure beschrijft zuivere lijnen en mediterraan wit in dialoog met de natuur, met een ontwerp waarin licht en ruimtegebruik voorop staan. De beelden tonen een houten pergola langs het dak en beplanting langs de randen van de balkons.',
  'Broszura opisuje czyste linie i śródziemnomorską biel w dialogu z naturą, a w projekcie na pierwszym miejscu stawia światło i optymalne wykorzystanie przestrzeni. Wizualizacje pokazują drewnianą pergolę wzdłuż dachu i zieleń na krawędziach balkonów.',
  'Brosjyren beskriver rene linjer og middelhavshvitt i dialog med naturen, med et design som setter lys og god bruk av plassen først. Bildene viser en trepergola langs taket og beplantning langs balkongkantene.',
  'Broschyren beskriver rena linjer och medelhavsvitt i dialog med naturen, med en design där ljus och god användning av ytan kommer först. Bilderna visar en träpergola längs taket och planteringar längs balkongkanterna.')
a('The images are computer-generated and the finished building may differ from them.',
  'Las imágenes están generadas por ordenador y el edificio terminado puede diferir de ellas.',
  'Les images sont générées par ordinateur et l’immeuble achevé peut différer de celles-ci.',
  'Die Bilder sind computergeneriert, und das fertige Gebäude kann davon abweichen.',
  'Изображения созданы на компьютере, и готовое здание может от них отличаться.',
  'الصور مولَّدة بالحاسوب وقد يختلف المبنى المكتمل عنها.',
  'De beelden zijn computergegenereerd en het voltooide gebouw kan ervan afwijken.',
  'Obrazy są wygenerowane komputerowo, a gotowy budynek może się od nich różnić.',
  'Bildene er datagenererte, og den ferdige bygningen kan avvike fra dem.',
  'Bilderna är datorgenererade och den färdiga byggnaden kan skilja sig från dem.')
a('Rendered mortar or exposed brick over an air cavity and mineral-wool insulation, finished in white, and grey on the terraces.',
  'Mortero monocapa o ladrillo visto sobre cámara de aire y aislamiento de lana mineral, acabado en blanco, y en gris en las terrazas.',
  'Enduit de mortier ou brique apparente sur lame d’air et isolation en laine minérale, finition blanche, et grise sur les terrasses.',
  'Mörtelputz oder Sichtmauerwerk über Luftschicht und Mineralwolldämmung, in Weiß gehalten, an den Terrassen in Grau.',
  'Штукатурка или облицовочный кирпич по воздушной прослойке и минераловатному утеплителю, отделка белая, на террасах — серая.',
  'ملاط مصبوب أو طوب ظاهر فوق فراغ هوائي وعزل بالصوف المعدني، بتشطيب أبيض وبلون رمادي في التراسات.',
  'Gepleisterde of onbepleisterde baksteen over een luchtspouw en isolatie van minerale wol, wit afgewerkt en grijs op de terrassen.',
  'Tynk lub cegła licowa na szczelinie powietrznej i izolacji z wełny mineralnej, w kolorze białym, a na tarasach w szarym.',
  'Pusset mur eller upusset teglstein over et luftrom og mineralullisolasjon, i hvitt, og grått på terrassene.',
  'Putsad fasad eller synligt tegel över en luftspalt och mineralullsisolering, i vitt, och i grått på terrasserna.')
a('PVC window frames with double glazing, and lacquered aluminium roller shutters that black out the bedrooms.',
  'Carpintería de PVC con doble acristalamiento y persianas de lamas de aluminio lacado que oscurecen por completo los dormitorios.',
  'Menuiseries en PVC avec double vitrage et volets roulants en lames d’aluminium laqué qui occultent complètement les chambres.',
  'Fensterrahmen aus PVC mit Doppelverglasung und Rollläden aus lackierten Aluminiumlamellen, die die Schlafzimmer vollständig abdunkeln.',
  'Оконные рамы из ПВХ с двойным остеклением и роллеты из лакированного алюминия, полностью затемняющие спальни.',
  'إطارات نوافذ من PVC بزجاج مزدوج، وستائر دوارة من شرائح الألومنيوم المطلية تحجب الضوء تمامًا في غرف النوم.',
  'Kozijnen van PVC met dubbel glas en rolluiken met gelakte aluminium lamellen die de slaapkamers volledig verduisteren.',
  'Ramy okienne z PVC z podwójnym szkleniem oraz rolety z lakierowanych lameli aluminiowych, które całkowicie zaciemniają sypialnie.',
  'Vindusrammer i PVC med dobbeltglass og rullegardiner med lakkerte aluminiumslameller som mørklegger soverommene helt.',
  'Fönsterkarmar i PVC med dubbelglas och rullgardiner med lackerade aluminiumlameller som helt mörklägger sovrummen.')
a('Flat roofs, paved in non-slip ceramic where they can be walked on and finished in gravel where they cannot.',
  'Cubiertas planas, pavimentadas con cerámica antideslizante donde son transitables y acabadas en grava donde no lo son.',
  'Toitures plates, revêtues de céramique antidérapante là où elles sont accessibles et finies en gravier là où elles ne le sont pas.',
  'Flachdächer, begehbare Bereiche mit rutschhemmender Keramik belegt, nicht begehbare mit Kies abgedeckt.',
  'Плоские кровли: на эксплуатируемых участках — противоскользящая керамика, на остальных — гравий.',
  'أسقف مسطحة، مبلّطة بالسيراميك المانع للانزلاق حيث يمكن المشي عليها ومكسوّة بالحصى حيث لا يمكن.',
  'Platte daken, waar ze begaanbaar zijn bestraat met antislipkeramiek en waar dat niet zo is afgewerkt met grind.',
  'Dachy płaskie, w miejscach dostępnych do chodzenia wyłożone ceramiką antypoślizgową, a w pozostałych pokryte żwirem.',
  'Flate tak, belagt med sklisikker keramikk der de kan brukes og dekket med grus der de ikke kan.',
  'Platta tak, belagda med halkfri keramik där de går att beträda och med grus där de inte gör det.')
a('A lift for six people serves every floor and connects directly to the garage levels.',
  'Un ascensor para seis personas da servicio a todas las plantas y comunica directamente con los niveles de garaje.',
  'Un ascenseur de six personnes dessert tous les étages et communique directement avec les niveaux du garage.',
  'Ein Aufzug für sechs Personen bedient alle Geschosse und ist direkt mit den Garagenebenen verbunden.',
  'Лифт на шесть человек обслуживает все этажи и напрямую связан с уровнями гаража.',
  'مصعد يتسع لستة أشخاص يخدم جميع الطوابق ويتصل مباشرة بمستويات المرآب.',
  'Een lift voor zes personen bedient alle verdiepingen en is rechtstreeks verbonden met de garageniveaus.',
  'Winda dla sześciu osób obsługuje wszystkie kondygnacje i łączy się bezpośrednio z poziomami garażu.',
  'En heis for seks personer betjener alle etasjer og går direkte til garasjenivåene.',
  'En hiss för sex personer trafikerar alla våningar och går direkt till garagenivåerna.')

# ---------------------------------------------------------------- quality specification
a('Source: the quality specification in the developer’s brochure. The brochure says it is indicative and that any material changed will be replaced by one of equal or higher quality.',
  'Fuente: la memoria de calidades del folleto del promotor. El folleto dice que es orientativa y que cualquier material modificado se sustituirá por otro de calidad igual o superior.',
  'Source : le descriptif de la brochure du promoteur. La brochure précise qu’il est indicatif et que tout matériau modifié sera remplacé par un autre de qualité égale ou supérieure.',
  'Quelle: die Baubeschreibung in der Broschüre des Bauträgers. Die Broschüre weist darauf hin, dass sie unverbindlich ist und jedes geänderte Material durch ein gleich- oder höherwertiges ersetzt wird.',
  'Источник: спецификация в брошюре застройщика. В брошюре сказано, что она носит ориентировочный характер и что любой изменённый материал будет заменён материалом равного или более высокого качества.',
  'المصدر: مواصفات البناء الواردة في كتيّب المطوّر. ويذكر الكتيّب أنها استرشادية وأن أي مادة يجري تغييرها ستُستبدل بأخرى بجودة مساوية أو أعلى.',
  'Bron: het lastenboek in de brochure van de ontwikkelaar. De brochure vermeldt dat het richtinggevend is en dat elk gewijzigd materiaal wordt vervangen door een materiaal van gelijke of hogere kwaliteit.',
  'Źródło: specyfikacja w broszurze dewelopera. Broszura zastrzega, że ma ona charakter orientacyjny i że każdy zmieniony materiał zostanie zastąpiony materiałem o takiej samej lub wyższej jakości.',
  'Kilde: spesifikasjonen i utbyggerens brosjyre. Brosjyren sier at den er veiledende og at ethvert endret materiale erstattes av et materiale av samme eller høyere kvalitet.',
  'Källa: specifikationen i exploatörens broschyr. Broschyren anger att den är vägledande och att varje ändrat material ersätts av ett material av samma eller högre kvalitet.')
a('Structure and foundations', 'Estructura y cimentación', 'Structure et fondations', 'Konstruktion und Fundament', 'Конструкция и фундамент',
  'الهيكل والأساسات', 'Structuur en fundering', 'Konstrukcja i fundamenty', 'Konstruksjon og fundament', 'Konstruktion och grund')
a('A reinforced concrete structure with waffle-slab floors, to the building code.',
  'Estructura de hormigón armado con forjados reticulares, conforme al Código Técnico de la Edificación.',
  'Une structure en béton armé avec planchers-dalles, conforme au code de la construction.',
  'Ein Stahlbetontragwerk mit Rippendecken nach dem Baurecht.',
  'Железобетонный каркас с кессонными перекрытиями в соответствии со строительными нормами.',
  'هيكل من الخرسانة المسلحة مع بلاطات مفرغة، وفق كود البناء.',
  'Een constructie van gewapend beton met wafelvloeren, volgens het bouwbesluit.',
  'Konstrukcja żelbetowa ze stropami kasetonowymi, zgodna z przepisami budowlanymi.',
  'Et bæresystem av armert betong med kassettdekker, etter byggeforskriften.',
  'En stomme av armerad betong med vaffelbjälklag, enligt byggnormen.')
a('Foundations designed from the geotechnical study, with reinforced concrete diaphragm walls and a reinforced concrete slab.',
  'Cimentación proyectada según el estudio geotécnico, con muros pantalla de hormigón armado y losa de hormigón armado.',
  'Fondations conçues d’après l’étude géotechnique, avec des parois moulées en béton armé et un radier en béton armé.',
  'Fundament nach dem Baugrundgutachten, mit Schlitzwänden aus Stahlbeton und einer Stahlbeton-Bodenplatte.',
  'Фундамент рассчитан по геотехническому исследованию: железобетонные стены в грунте и железобетонная плита.',
  'أساسات مصمَّمة وفق الدراسة الجيوتقنية، بجدران ساترة من الخرسانة المسلحة وبلاطة من الخرسانة المسلحة.',
  'Fundering ontworpen op basis van het grondonderzoek, met diepwanden van gewapend beton en een funderingsplaat van gewapend beton.',
  'Fundamenty zaprojektowane na podstawie badań geotechnicznych, ze żelbetowymi ścianami szczelinowymi i żelbetową płytą fundamentową.',
  'Fundament utformet etter den geotekniske undersøkelsen, med slissevegger i armert betong og en plate i armert betong.',
  'Grund utformad efter den geotekniska undersökningen, med slitsmurar i armerad betong och en platta i armerad betong.')
a('Partitions between homes and with the common areas in dry construction, lined on both sides over a self-supporting metal frame, with mineral-wool thermal and acoustic insulation.',
  'Tabiques entre viviendas y con las zonas comunes en construcción en seco, trasdosados por ambas caras sobre una estructura metálica autoportante, con aislamiento térmico y acústico de lana mineral.',
  'Cloisons entre logements et avec les parties communes en construction sèche, doublées sur les deux faces sur une ossature métallique autoportante, avec isolation thermique et acoustique en laine minérale.',
  'Trennwände zwischen den Wohnungen und zu den Gemeinschaftsflächen in Trockenbauweise, beidseitig beplankt auf einer selbsttragenden Metallkonstruktion, mit Wärme- und Schalldämmung aus Mineralwolle.',
  'Перегородки между квартирами и с общими зонами выполнены сухим способом: обшивка с двух сторон по самонесущему металлическому каркасу, тепло- и звукоизоляция из минеральной ваты.',
  'قواطع بين المساكن ومع المناطق المشتركة بالبناء الجاف، مكسوّة من الجانبين على هيكل معدني ذاتي الحمل، مع عزل حراري وصوتي بالصوف المعدني.',
  'Scheidingswanden tussen woningen en met de gemeenschappelijke ruimten in droogbouw, aan beide zijden bekleed op een zelfdragend metalen frame, met thermische en akoestische isolatie van minerale wol.',
  'Ścianki między lokalami i z częściami wspólnymi wykonane w technologii suchej zabudowy, obustronnie obłożone na samonośnym stelażu metalowym, z izolacją termiczną i akustyczną z wełny mineralnej.',
  'Skillevegger mellom boligene og mot fellesarealene i tørrbygg, kledd på begge sider over en selvbærende metallkonstruksjon, med varme- og lydisolasjon av mineralull.',
  'Skiljeväggar mellan bostäderna och mot de gemensamma ytorna i torrbyggnad, beklädda på båda sidor över en självbärande metallstomme, med värme- och ljudisolering av mineralull.')
a('Moisture-resistant plasterboard in the wet areas.', 'Placas de yeso laminado resistentes a la humedad en las zonas húmedas.',
  'Plaques de plâtre hydrofuges dans les pièces d’eau.', 'Feuchtraumbeständige Gipskartonplatten in den Nassbereichen.',
  'Влагостойкий гипсокартон во влажных зонах.', 'ألواح جبسية مقاومة للرطوبة في المناطق الرطبة.',
  'Vochtbestendige gipsplaten in de natte ruimtes.', 'Płyty gipsowo-kartonowe wodoodporne w pomieszczeniach mokrych.',
  'Fuktbestandige gipsplater i våtrommene.', 'Fuktbeständiga gipsskivor i de våta utrymmena.')
a('A solid entrance door lacquered white, with a security lock and an optical peephole, and interior doors lacquered white.',
  'Puerta de entrada maciza lacada en blanco, con cerradura de seguridad y mirilla óptica, y puertas interiores lacadas en blanco.',
  'Porte d’entrée pleine laquée blanc, avec serrure de sécurité et judas optique, et portes intérieures laquées blanc.',
  'Eine massive, weiß lackierte Wohnungseingangstür mit Sicherheitsschloss und optischem Spion sowie weiß lackierte Innentüren.',
  'Массивная входная дверь, лакированная в белый цвет, с замком безопасности и оптическим глазком, и межкомнатные двери, лакированные в белый цвет.',
  'باب دخول مصمت مطلي باللاكيه الأبيض مع قفل أمان وعين سحرية بصرية، وأبواب داخلية مطلية باللاكيه الأبيض.',
  'Een massieve, wit gelakte voordeur met veiligheidsslot en optisch kijkgat, en wit gelakte binnendeuren.',
  'Pełne drzwi wejściowe lakierowane na biało, z zamkiem zabezpieczającym i wizjerem optycznym, oraz drzwi wewnętrzne lakierowane na biało.',
  'En massiv inngangsdør lakkert hvit, med sikkerhetslås og optisk kikkhull, og innerdører lakkert hvite.',
  'En massiv ytterdörr lackerad i vitt, med säkerhetslås och optisk titthål, och innerdörrar lackerade i vitt.')
a('Built-in wardrobes in every bedroom, with sliding doors lacquered white, an inside lining, a luggage shelf and a hanging rail.',
  'Armarios empotrados en todos los dormitorios, con puertas correderas lacadas en blanco, forrado interior, maletero y barra de colgar.',
  'Placards intégrés dans toutes les chambres, avec portes coulissantes laquées blanc, habillage intérieur, rangement supérieur pour valises et barre de penderie.',
  'Einbauschränke in allen Schlafzimmern, mit weiß lackierten Schiebetüren, Innenverkleidung, Gepäckfach und Kleiderstange.',
  'Встроенные шкафы во всех спальнях с раздвижными дверями, лакированными в белый цвет, внутренней отделкой, антресолью для чемоданов и штангой для одежды.',
  'خزائن مدمجة في جميع غرف النوم بأبواب منزلقة مطلية باللاكيه الأبيض وبطانة داخلية ورف للحقائب وقضيب تعليق.',
  'Inbouwkasten in alle slaapkamers, met wit gelakte schuifdeuren, binnenbekleding, een bagageplank en een kledingroede.',
  'Szafy wnękowe we wszystkich sypialniach, z przesuwnymi drzwiami lakierowanymi na biało, wyłożeniem wewnętrznym, półką na bagaż i drążkiem na ubrania.',
  'Innebygde skap i alle soverom, med skyvedører lakkert hvite, innvendig kledning, bagasjehylle og kleshenger.',
  'Inbyggda garderober i alla sovrum, med skjutdörrar lackerade i vitt, invändig beklädnad, bagagehylla och klädstång.')
a('Large-format porcelain stoneware (at least 90 x 90 cm or 120 x 60 cm) in neutral grey, with a rectified edge and a satin finish, in the living room, the kitchen and the hallways.',
  'Gres porcelánico de gran formato (mínimo 90 x 90 cm o 120 x 60 cm) en gris neutro, con borde rectificado y acabado satinado, en el salón, la cocina y los pasillos.',
  'Grès cérame grand format (au moins 90 x 90 cm ou 120 x 60 cm) gris neutre, bords rectifiés et finition satinée, dans le séjour, la cuisine et les couloirs.',
  'Großformatiges Feinsteinzeug (mindestens 90 x 90 cm oder 120 x 60 cm) in neutralem Grau, mit rektifizierter Kante und seidenmatter Oberfläche, in Wohnzimmer, Küche und Fluren.',
  'Крупноформатный керамогранит (не менее 90 x 90 см или 120 x 60 см) нейтрального серого цвета, с ректифицированной кромкой и сатиновой поверхностью — в гостиной, кухне и коридорах.',
  'بورسلان كبير القياس (90 × 90 سم أو 120 × 60 سم على الأقل) بلون رمادي محايد، بحواف مقصوصة وتشطيب ساتان، في غرفة المعيشة والمطبخ والممرات.',
  'Grootformaat porseleinen tegels (minstens 90 x 90 cm of 120 x 60 cm) in neutraal grijs, met gerectificeerde rand en satijnen afwerking, in de woonkamer, de keuken en de gangen.',
  'Wielkoformatowy gres porcelanowy (co najmniej 90 x 90 cm lub 120 x 60 cm) w neutralnej szarości, z krawędziami rektyfikowanymi i satynowym wykończeniem, w salonie, kuchni i korytarzach.',
  'Storformat porselensfliser (minst 90 x 90 cm eller 120 x 60 cm) i nøytral grå, med rektifiserte kanter og satengfinish, i stuen, kjøkkenet og gangene.',
  'Storformat klinker (minst 90 x 90 cm eller 120 x 60 cm) i neutral grå, med rektifierad kant och satinfinish, i vardagsrummet, köket och hallarna.')
a('Non-slip porcelain stoneware from the same series on the terraces.',
  'Gres porcelánico antideslizante de la misma serie en las terrazas.',
  'Grès cérame antidérapant de la même série sur les terrasses.',
  'Rutschhemmendes Feinsteinzeug aus derselben Serie auf den Terrassen.',
  'Противоскользящий керамогранит из той же серии на террасах.',
  'بورسلان مانع للانزلاق من السلسلة نفسها في التراسات.',
  'Antislip porseleinen tegels uit dezelfde serie op de terrassen.',
  'Antypoślizgowy gres porcelanowy z tej samej serii na tarasach.',
  'Sklisikre porselensfliser fra samme serie på terrassene.',
  'Halkfri klinker från samma serie på terrasserna.')
a('Ceramic tiling in the bathrooms, in sand in the secondary bathroom and in grey in the main one.',
  'Alicatado cerámico en los baños, en tono arena en el baño secundario y en gris en el principal.',
  'Carrelage mural en céramique dans les salles de bain, sable dans la salle de bain secondaire et gris dans la principale.',
  'Keramikfliesen in den Bädern, in Sand im Nebenbad und in Grau im Hauptbad.',
  'Керамическая плитка в ванных комнатах: песочного цвета во второй ванной и серая в главной.',
  'تكسية خزفية في الحمامات، بلون رملي في الحمام الثانوي ورمادي في الحمام الرئيسي.',
  'Keramische tegels in de badkamers, in zandkleur in de tweede badkamer en in grijs in de hoofdbadkamer.',
  'Okładziny ceramiczne w łazienkach: w kolorze piasku w łazience dodatkowej i w szarym w głównej.',
  'Keramiske fliser på badene, i sand på det sekundære badet og i grått på hovedbadet.',
  'Keramiska kakel i badrummen, i sand i det sekundära badrummet och i grått i huvudbadrummet.')
a('Handleless cabinets in matt white with an anti-fingerprint finish, and a Calacatta-style porcelain worktop and island with a waterfall side. The brochure’s introductory text speaks of quartz worktops.',
  'Muebles sin tiradores en blanco mate con acabado antihuellas, y encimera e isla de porcelánico tipo Calacatta con lateral en cascada. El texto introductorio del folleto habla de encimeras de cuarzo.',
  'Meubles sans poignées en blanc mat avec finition anti-traces, plan de travail et îlot en grès cérame façon Calacatta avec côté en cascade. Le texte d’introduction de la brochure parle de plans de travail en quartz.',
  'Grifflose Schränke in mattem Weiß mit Anti-Fingerabdruck-Oberfläche sowie Arbeitsplatte und Kochinsel aus Feinsteinzeug in Calacatta-Optik mit Wasserfallkante. Der einleitende Text der Broschüre spricht von Quarz-Arbeitsplatten.',
  'Фасады без ручек матового белого цвета с покрытием против отпечатков, столешница и остров из керамогранита под «калакатту» с водопадом на боковой стороне. Во вступительном тексте брошюры говорится о кварцевых столешницах.',
  'خزائن بلا مقابض بالأبيض المطفي مع تشطيب مقاوم لبصمات الأصابع، وسطح عمل وجزيرة من البورسلان بنمط كالاكاتا مع جانب شلالي. ويتحدث النص التمهيدي في الكتيّب عن أسطح عمل من الكوارتز.',
  'Greeploze kasten in mat wit met een anti-vingerafdrukafwerking, en een werkblad en eiland van porselein in Calacatta-look met een watervalrand. De inleidende tekst van de brochure spreekt van kwartsen werkbladen.',
  'Szafki bez uchwytów w macie białym z powłoką antyodciskową oraz blat i wyspa z gresu w stylu Calacatta z bokiem w formie wodospadu. Tekst wprowadzający w broszurze mówi o blatach kwarcowych.',
  'Håndtaksfrie skap i matt hvitt med anti-fingeravtrykk-finish, og en benkeplate og en øy i porselen i Calacatta-stil med fossekant. Brosjyrens innledende tekst taler om benkeplater i kvarts.',
  'Handtagslösa skåp i matt vitt med anti-fingeravtrycksfinish samt bänkskiva och köksö i porslin i Calacatta-stil med vattenfallskant. Broschyrens inledande text talar om bänkskivor i kvarts.')
a('Appliances included: a built-in combined fridge-freezer, a multifunction oven and a microwave in a column, an induction hob, an extractor hood and a black undermount sink.',
  'Electrodomésticos incluidos: frigorífico combi integrado, horno multifunción y microondas en columna, placa de inducción, campana extractora y fregadero bajo encimera en negro.',
  'Électroménager inclus : réfrigérateur-congélateur intégré, four multifonction et micro-ondes en colonne, plaque à induction, hotte aspirante et évier sous plan noir.',
  'Geräte inklusive: ein eingebauter Kühl-Gefrier-Kombi, ein Multifunktionsofen und eine Mikrowelle im Hochschrank, ein Induktionskochfeld, eine Dunstabzugshaube und ein schwarzes Unterbauspülbecken.',
  'Техника входит в комплект: встроенный холодильник с морозильной камерой, многофункциональная духовка и микроволновая печь в колонне, индукционная варочная панель, вытяжка и чёрная врезная мойка.',
  'الأجهزة مشمولة: ثلاجة مع فريزر مدمجة، وفرن متعدد الوظائف وميكروويف في عمود، وموقد حثي، وشفاط، وحوض أسود مثبّت أسفل سطح العمل.',
  'Apparatuur inbegrepen: een ingebouwde koel-vriescombinatie, een multifunctionele oven en een magnetron in een kolom, een inductiekookplaat, een afzuigkap en een zwarte onderbouwspoelbak.',
  'W cenie sprzęt: wbudowana chłodziarko-zamrażarka, piekarnik wielofunkcyjny i kuchenka mikrofalowa w zabudowie słupkowej, płyta indukcyjna, okap oraz czarny zlew podwieszany.',
  'Hvitevarer inkludert: et innebygd kombinert kjøle-fryseskap, en multifunksjonsovn og en mikrobølgeovn i en søyle, en induksjonstopp, en avtrekkshette og en svart underlimt vask.',
  'Vitvaror ingår: en inbyggd kombinerad kyl-frys, en multifunktionsugn och en mikrovågsugn i en kolonn, en induktionshäll, en köksfläkt och en svart underlimmad diskho.')
a('A vanity unit, sink and mirror by Porcelanosa, a toilet, a resin shower tray and a shower screen, with single-lever chrome taps with flow control.',
  'Mueble de lavabo, lavabo y espejo de Porcelanosa, inodoro, plato de ducha de resina y mampara, con grifería monomando cromada con regulación de caudal.',
  'Meuble vasque, vasque et miroir Porcelanosa, WC, receveur de douche en résine et paroi de douche, avec robinetterie mitigeur chromée à réducteur de débit.',
  'Waschtischunterschrank, Waschbecken und Spiegel von Porcelanosa, ein WC, eine Duschwanne aus Kunstharz und eine Duschabtrennung, mit verchromten Einhebelarmaturen mit Durchflussbegrenzung.',
  'Тумба с раковиной и зеркало Porcelanosa, унитаз, душевой поддон из смолы и душевая перегородка, хромированные однорычажные смесители с ограничителем потока.',
  'وحدة مغسلة وحوض ومرآة من Porcelanosa، ومرحاض، وقاعدة دش من الراتنج، وحاجز دش، مع خلاطات كروم أحادية المقبض بتحكم في التدفق.',
  'Een badmeubel, wastafel en spiegel van Porcelanosa, een toilet, een douchebak van kunsthars en een douchewand, met verchroomde eengreepskranen met debietbegrenzing.',
  'Szafka z umywalką i lustro marki Porcelanosa, toaleta, brodzik żywiczny i kabina prysznicowa, z chromowanymi bateriami jednouchwytowymi z ogranicznikiem przepływu.',
  'Servantskap, servant og speil fra Porcelanosa, et toalett, en dusjbunn i harpiks og en dusjvegg, med forkrommede énhåndsbatterier med strømningsbegrenser.',
  'Tvättställsskåp, tvättställ och spegel från Porcelanosa, en toalett, en duschbrunn i harts och en duschvägg, med förkromade enhandsblandare med flödesbegränsare.')
a('Heat-pump air conditioning, ducted through a false ceiling with grilles in the living room, the kitchen and the bedrooms, and a thermostat in the living room.',
  'Aire acondicionado por bomba de calor, con distribución por conductos en falso techo y rejillas en el salón, la cocina y los dormitorios, y termostato en el salón.',
  'Climatisation par pompe à chaleur, avec gaines dans le faux plafond et grilles dans le séjour, la cuisine et les chambres, et un thermostat dans le séjour.',
  'Klimaanlage mit Wärmepumpe, über Kanäle in der Zwischendecke mit Auslässen in Wohnzimmer, Küche und Schlafzimmern, und ein Thermostat im Wohnzimmer.',
  'Кондиционирование на тепловом насосе с воздуховодами в подвесном потолке и решётками в гостиной, кухне и спальнях, термостат в гостиной.',
  'تكييف بمضخة حرارية، بتوزيع عبر مجارٍ في سقف مستعار مع فتحات في غرفة المعيشة والمطبخ وغرف النوم، وثرموستات في غرفة المعيشة.',
  'Airconditioning met warmtepomp, via kanalen in een verlaagd plafond met roosters in de woonkamer, de keuken en de slaapkamers, en een thermostaat in de woonkamer.',
  'Klimatyzacja z pompą ciepła, z kanałami w suficie podwieszanym i kratkami w salonie, kuchni i sypialniach oraz termostatem w salonie.',
  'Klimaanlegg med varmepumpe, med kanaler i et nedhengt tak og ventiler i stuen, kjøkkenet og soverommene, og en termostat i stuen.',
  'Luftkonditionering med värmepump, med kanaler i ett undertak och don i vardagsrummet, köket och sovrummen, samt en termostat i vardagsrummet.')
a('Hot water from solar thermal panels and a storage tank with an electric backup.',
  'Agua caliente a partir de paneles solares térmicos y un depósito de acumulación con apoyo eléctrico.',
  'Eau chaude produite par des panneaux solaires thermiques et un ballon de stockage avec appoint électrique.',
  'Warmwasser aus solarthermischen Kollektoren und einem Speicher mit elektrischer Nachheizung.',
  'Горячая вода от солнечных тепловых коллекторов и накопительного бака с электрическим резервом.',
  'ماء ساخن من ألواح شمسية حرارية وخزان تخزين مع تسخين كهربائي احتياطي.',
  'Warm water van zonnecollectoren en een opslagvat met elektrische bijverwarming.',
  'Ciepła woda z kolektorów słonecznych i zbiornika magazynującego z zasilaniem elektrycznym jako rezerwą.',
  'Varmtvann fra solfangere og en lagringstank med elektrisk reserve.',
  'Varmvatten från solfångare och en ackumulatortank med elektrisk reserv.')
a('Mechanical ventilation to the building code, with an individual duct to the roof for each home and a separate smoke outlet for the extractor hood.',
  'Ventilación mecánica conforme al Código Técnico de la Edificación, con un conducto individual hasta la cubierta para cada vivienda y una salida de humos independiente para la campana extractora.',
  'Ventilation mécanique conforme au code de la construction, avec un conduit individuel jusqu’au toit pour chaque logement et une évacuation de fumées séparée pour la hotte.',
  'Mechanische Lüftung nach dem Baurecht, mit einem eigenen Kanal bis zum Dach für jede Wohnung und einem separaten Abzug für die Dunstabzugshaube.',
  'Механическая вентиляция по строительным нормам: для каждой квартиры отдельный канал до кровли и отдельный дымоход для вытяжки.',
  'تهوية ميكانيكية وفق كود البناء، بمجرى مستقل لكل مسكن حتى السطح ومخرج دخان منفصل للشفاط.',
  'Mechanische ventilatie volgens het bouwbesluit, met voor elke woning een eigen kanaal naar het dak en een aparte rookafvoer voor de afzuigkap.',
  'Wentylacja mechaniczna zgodna z przepisami budowlanymi, z osobnym przewodem na dach dla każdego lokalu i oddzielnym wylotem dymu dla okapu.',
  'Mekanisk ventilasjon etter byggeforskriften, med en egen kanal til taket for hver bolig og et eget røykutløp for avtrekkshetten.',
  'Mekanisk ventilation enligt byggnormen, med en egen kanal till taket för varje bostad och ett separat rökutlopp för köksfläkten.')
a('The brochure shows an energy rating of B and says the values are pending verification by the site management.',
  'El folleto muestra una calificación energética B y dice que los valores están pendientes de verificación por la dirección facultativa.',
  'La brochure indique une classe énergétique B et précise que les valeurs sont en attente de vérification par la direction de chantier.',
  'Die Broschüre zeigt die Energieeffizienzklasse B und weist darauf hin, dass die Werte noch von der Bauleitung überprüft werden müssen.',
  'В брошюре указан класс энергоэффективности B с пометкой, что значения ожидают проверки руководством стройки.',
  'يعرض الكتيّب تصنيفًا للطاقة من الفئة B ويذكر أن القيم بانتظار التحقق منها من إدارة الموقع.',
  'De brochure toont energielabel B en vermeldt dat de waarden nog door de bouwdirectie moeten worden geverifieerd.',
  'Broszura podaje klasę energetyczną B i zaznacza, że wartości oczekują na weryfikację przez kierownictwo budowy.',
  'Brosjyren viser energimerke B og sier at verdiene venter på verifisering fra byggeledelsen.',
  'Broschyren visar energiklass B och anger att värdena väntar på verifiering av byggledningen.')
a('Electrical, lift and garage', 'Electricidad, ascensor y garaje', 'Électricité, ascenseur et garage', 'Elektro, Aufzug und Garage',
  'Электрика, лифт и гараж', 'الكهرباء والمصعد والمرآب', 'Elektriciteit, lift en garage', 'Elektryka, winda i garaż', 'Elektro, heis og garasje', 'El, hiss och garage')
a('A video intercom with a camera at the building entrance and a monitor in each home, and television, telephone and fibre-optic points, with internet wiring to the bedrooms and the living room.',
  'Videoportero con cámara en la entrada del edificio y monitor en cada vivienda, y tomas de televisión, teléfono y fibra óptica, con cableado de internet a los dormitorios y al salón.',
  'Visiophone avec caméra à l’entrée de l’immeuble et moniteur dans chaque logement, prises de télévision, de téléphone et de fibre optique, avec câblage internet vers les chambres et le séjour.',
  'Eine Videosprechanlage mit Kamera am Gebäudeeingang und Monitor in jeder Wohnung sowie TV-, Telefon- und Glasfaseranschlüsse, mit Internetverkabelung zu den Schlafzimmern und zum Wohnzimmer.',
  'Видеодомофон с камерой у входа в здание и монитором в каждой квартире, розетки для телевидения, телефона и оптоволокна, интернет-проводка в спальни и гостиную.',
  'جهاز اتصال مرئي بكاميرا عند مدخل المبنى وشاشة في كل مسكن، ومآخذ للتلفاز والهاتف والألياف الضوئية، مع كابلات إنترنت إلى غرف النوم وغرفة المعيشة.',
  'Een videofoon met camera bij de ingang van het gebouw en een monitor in elke woning, en aansluitingen voor televisie, telefoon en glasvezel, met internetbekabeling naar de slaapkamers en de woonkamer.',
  'Wideodomofon z kamerą przy wejściu do budynku i monitorem w każdym lokalu oraz gniazda telewizyjne, telefoniczne i światłowodowe, z okablowaniem internetowym do sypialni i salonu.',
  'Et videoanlegg med kamera ved bygningens inngang og en monitor i hver bolig, og uttak for TV, telefon og fiber, med internettkabling til soverommene og stuen.',
  'En videoporttelefon med kamera vid byggnadens entré och en monitor i varje bostad, samt uttag för TV, telefon och fiber, med internetkablage till sovrummen och vardagsrummet.')
a('A lift with automatic steel doors, accessible to people with disabilities.',
  'Ascensor con puertas automáticas de acero, accesible para personas con discapacidad.',
  'Ascenseur à portes automatiques en acier, accessible aux personnes handicapées.',
  'Ein Aufzug mit automatischen Stahltüren, barrierefrei zugänglich.',
  'Лифт с автоматическими стальными дверями, доступный для людей с ограниченными возможностями.',
  'مصعد بأبواب فولاذية أوتوماتيكية، ميسّر للأشخاص ذوي الإعاقة.',
  'Een lift met automatische stalen deuren, toegankelijk voor personen met een beperking.',
  'Winda z automatycznymi drzwiami stalowymi, dostępna dla osób z niepełnosprawnościami.',
  'En heis med automatiske ståldører, tilgjengelig for personer med nedsatt funksjonsevne.',
  'En hiss med automatiska ståldörrar, tillgänglig för personer med funktionsnedsättning.')
a('A garage with automated, remote-controlled entrance doors, forced ventilation, fire detection and emergency lighting, and pre-installation of charging points for electric vehicles.',
  'Garaje con puertas de acceso automáticas y con mando a distancia, ventilación forzada, detección de incendios y alumbrado de emergencia, y preinstalación de puntos de recarga para vehículos eléctricos.',
  'Garage avec portes d’accès automatiques télécommandées, ventilation forcée, détection incendie et éclairage de secours, et pré-installation de bornes de recharge pour véhicules électriques.',
  'Eine Garage mit automatischen, ferngesteuerten Einfahrtstoren, Zwangsbelüftung, Brandmeldeanlage und Notbeleuchtung sowie Vorinstallation von Ladepunkten für Elektrofahrzeuge.',
  'Гараж с автоматическими въездными воротами с дистанционным управлением, принудительной вентиляцией, пожарной сигнализацией и аварийным освещением, а также подготовкой под зарядные точки для электромобилей.',
  'مرآب بأبواب دخول أوتوماتيكية يُتحكّم بها عن بُعد، وتهوية قسرية، وكشف للحريق وإضاءة طوارئ، وتجهيز مسبق لنقاط شحن المركبات الكهربائية.',
  'Een garage met automatische, afstandsbediende toegangsdeuren, geforceerde ventilatie, brandmelding en noodverlichting, en voorbereiding voor laadpunten voor elektrische voertuigen.',
  'Garaż z automatycznymi bramami wjazdowymi sterowanymi pilotem, wentylacją wymuszoną, detekcją pożaru i oświetleniem awaryjnym oraz przygotowaniem pod punkty ładowania pojazdów elektrycznych.',
  'En garasje med automatiske, fjernstyrte innkjøringsporter, tvungen ventilasjon, brannvarsling og nødbelysning, og forberedelse for ladepunkter for elbiler.',
  'Ett garage med automatiska, fjärrstyrda infartsportar, forcerad ventilation, brandlarm och nödbelysning samt förberedelse för laddpunkter för elfordon.')

# ---------------------------------------------------------------- residences
a('From one bedroom <em>to a penthouse</em>', 'De un dormitorio <em>a un ático</em>', 'D’une chambre <em>à un penthouse</em>',
  'Von einem Schlafzimmer <em>bis zum Penthouse</em>', 'От одной спальни <em>до пентхауса</em>', 'من غرفة نوم واحدة <em>إلى بنتهاوس</em>',
  'Van een slaapkamer <em>tot een penthouse</em>', 'Od jednej sypialni <em>po penthouse</em>', 'Fra ett soverom <em>til en toppleilighet</em>',
  'Från ett sovrum <em>till en takvåning</em>')
a('The 17 listed homes are four one-bedroom apartments, eleven two-bedroom apartments, one three-bedroom apartment and one two-bedroom penthouse. The table below lists all of them with their prices.',
  'Las 17 viviendas en lista son cuatro apartamentos de un dormitorio, once apartamentos de dos dormitorios, un apartamento de tres dormitorios y un ático de dos dormitorios. La tabla siguiente las recoge todas con sus precios.',
  'Les 17 logements en vente sont quatre appartements d’une chambre, onze appartements de deux chambres, un appartement de trois chambres et un penthouse de deux chambres. Le tableau ci-dessous les présente tous avec leurs prix.',
  'Die 17 gelisteten Wohnungen sind vier Apartments mit einem Schlafzimmer, elf Apartments mit zwei Schlafzimmern, ein Apartment mit drei Schlafzimmern und ein Penthouse mit zwei Schlafzimmern. Die Tabelle unten führt alle mit ihren Preisen auf.',
  'В продаже 17 квартир: четыре апартамента с одной спальней, одиннадцать с двумя спальнями, один с тремя спальнями и пентхаус с двумя спальнями. В таблице ниже все они указаны с ценами.',
  'المساكن الـ17 المعروضة هي أربع شقق بغرفة نوم واحدة، وإحدى عشرة شقة بغرفتي نوم، وشقة واحدة بثلاث غرف نوم، وبنتهاوس بغرفتي نوم. ويعرضها الجدول أدناه جميعًا مع أسعارها.',
  'De 17 vermelde woningen zijn vier appartementen met een slaapkamer, elf appartementen met twee slaapkamers, een appartement met drie slaapkamers en een penthouse met twee slaapkamers. De tabel hieronder toont ze allemaal met hun prijzen.',
  '17 lokali w ofercie to cztery apartamenty z jedną sypialnią, jedenaście z dwiema sypialniami, jeden z trzema sypialniami i jeden penthouse z dwiema sypialniami. Tabela poniżej zawiera je wszystkie wraz z cenami.',
  'De 17 oppførte boligene er fire leiligheter med ett soverom, elleve leiligheter med to soverom, én leilighet med tre soverom og én toppleilighet med to soverom. Tabellen nedenfor viser alle med prisene.',
  'De 17 listade bostäderna är fyra lägenheter med ett sovrum, elva lägenheter med två sovrum, en lägenhet med tre sovrum och en takvåning med två sovrum. Tabellen nedan visar alla med deras priser.')
a('Homes 2, 3, 7 and 15, on the ground, first and second floors. Home 2 has a terrace of 6.54 sqm; Homes 3, 7 and 15 are listed without one.',
  'Las viviendas 2, 3, 7 y 15, en las plantas baja, primera y segunda. La vivienda 2 tiene una terraza de {N6.54} {U}; las viviendas 3, 7 y 15 figuran sin terraza.',
  'Les logements 2, 3, 7 et 15, au rez-de-chaussée et aux premier et deuxième étages. Le logement 2 a une terrasse de {N6.54} {U} ; les logements 3, 7 et 15 figurent sans terrasse.',
  'Die Wohnungen 2, 3, 7 und 15 im Erdgeschoss sowie im ersten und zweiten Obergeschoss. Wohnung 2 hat eine Terrasse von {N6.54} {U}; die Wohnungen 3, 7 und 15 sind ohne Terrasse aufgeführt.',
  'Квартиры 2, 3, 7 и 15 — на первом, втором и третьем этажах. У квартиры 2 есть терраса {N6.54} {U}; квартиры 3, 7 и 15 указаны без террасы.',
  'المساكن 2 و3 و7 و15، في الطوابق الأرضي والأول والثاني. للمسكن 2 تراس مساحته {N6.54} {U}، أما المساكن 3 و7 و15 فمدرجة بلا تراس.',
  'Woningen 2, 3, 7 en 15, op de begane grond en de eerste en tweede verdieping. Woning 2 heeft een terras van {N6.54} {U}; woningen 3, 7 en 15 staan zonder terras vermeld.',
  'Lokale 2, 3, 7 i 15, na parterze oraz pierwszym i drugim piętrze. Lokal 2 ma taras o powierzchni {N6.54} {U}; lokale 3, 7 i 15 są podane bez tarasu.',
  'Bolig 2, 3, 7 og 15, i første, andre og tredje etasje. Bolig 2 har en terrasse på {N6.54} {U}; bolig 3, 7 og 15 er oppført uten terrasse.',
  'Bostäderna 2, 3, 7 och 15, på bottenvåningen samt första och andra våningen. Bostad 2 har en terrass på {N6.54} {U}; bostäderna 3, 7 och 15 är listade utan terrass.')
a('Eleven homes on the ground, first and second floors, facing south, east or north, each listed with a terrace of 2.30 to 8.60 sqm.',
  'Once viviendas en las plantas baja, primera y segunda, orientadas al sur, al este o al norte, cada una con una terraza de {N2.30} a {N8.60} {U} según la lista.',
  'Onze logements au rez-de-chaussée et aux premier et deuxième étages, orientés au sud, à l’est ou au nord, chacun avec une terrasse de {N2.30} à {N8.60} {U} selon la liste.',
  'Elf Wohnungen im Erdgeschoss sowie im ersten und zweiten Obergeschoss, nach Süden, Osten oder Norden ausgerichtet, jeweils mit einer Terrasse von {N2.30} bis {N8.60} {U} laut Liste.',
  'Одиннадцать квартир на первом, втором и третьем этажах, с ориентацией на юг, восток или север; по прайс-листу у каждой есть терраса от {N2.30} до {N8.60} {U}.',
  'إحدى عشرة شقة في الطوابق الأرضي والأول والثاني، تتجه نحو الجنوب أو الشرق أو الشمال، ولكل منها تراس تتراوح مساحته بين {N2.30} و{N8.60} {U} بحسب القائمة.',
  'Elf woningen op de begane grond en de eerste en tweede verdieping, gericht op het zuiden, oosten of noorden, elk volgens de lijst met een terras van {N2.30} tot {N8.60} {U}.',
  'Jedenaście lokali na parterze oraz pierwszym i drugim piętrze, skierowanych na południe, wschód lub północ, każdy z tarasem o powierzchni od {N2.30} do {N8.60} {U} według cennika.',
  'Elleve boliger i første, andre og tredje etasje, vendt mot sør, øst eller nord, hver oppført med en terrasse på {N2.30} til {N8.60} {U}.',
  'Elva bostäder på bottenvåningen samt första och andra våningen, vända mot söder, öster eller norr, var och en listad med en terrass på {N2.30} till {N8.60} {U}.')
a('The three-bedroom apartment', 'El apartamento de tres dormitorios', 'L’appartement de trois chambres', 'Das Apartment mit drei Schlafzimmern',
  'Апартаменты с тремя спальнями', 'الشقة بثلاث غرف نوم', 'Het appartement met drie slaapkamers', 'Apartament z trzema sypialniami',
  'Leiligheten med tre soverom', 'Lägenheten med tre sovrum')
a('Home 9, on the ground floor and facing north, with 103.27 sqm built on the price list. The list gives it a terrace of 2.70 sqm; its plan shows none.',
  'La vivienda 9, en planta baja y orientada al norte, con {N103.27} {U} construidos según la lista de precios. La lista le asigna una terraza de {N2.70} {U}; su plano no muestra ninguna.',
  'Le logement 9, au rez-de-chaussée et orienté au nord, avec {N103.27} {U} construits selon la liste de prix. La liste lui attribue une terrasse de {N2.70} {U} ; son plan n’en montre aucune.',
  'Wohnung 9 im Erdgeschoss, nach Norden ausgerichtet, mit {N103.27} {U} bebauter Fläche laut Preisliste. Die Liste nennt dafür eine Terrasse von {N2.70} {U}; im Grundriss ist keine zu sehen.',
  'Квартира 9 — на первом этаже, окна на север, по прайс-листу {N103.27} {U} застроенной площади. В прайс-листе указана терраса {N2.70} {U}, а на плане террасы нет.',
  'المسكن 9 في الطابق الأرضي ويتجه نحو الشمال، بمساحة مبنية {N103.27} {U} بحسب قائمة الأسعار. وتذكر القائمة له تراسًا مساحته {N2.70} {U}، ولا يظهر مخططه أي تراس.',
  'Woning 9, op de begane grond en gericht op het noorden, met {N103.27} {U} bebouwd volgens de prijslijst. De lijst vermeldt een terras van {N2.70} {U}; op de plattegrond staat er geen.',
  'Lokal 9, na parterze i skierowany na północ, z powierzchnią zabudowy {N103.27} {U} według cennika. Cennik podaje taras o powierzchni {N2.70} {U}, a na rzucie żadnego nie widać.',
  'Bolig 9, i første etasje og vendt mot nord, med {N103.27} {U} bygd ifølge prislisten. Listen oppgir en terrasse på {N2.70} {U}; planen viser ingen.',
  'Bostad 9, på bottenvåningen och vänd mot norr, med {N103.27} {U} byggyta enligt prislistan. Listan anger en terrass på {N2.70} {U}; planritningen visar ingen.')
a('Home 27, facing east, with 91.12 sqm built and an uncovered terrace of 42.15 sqm.',
  'La vivienda 27, orientada al este, con {N91.12} {U} construidos y una terraza descubierta de {N42.15} {U}.',
  'Le logement 27, orienté à l’est, avec {N91.12} {U} construits et une terrasse découverte de {N42.15} {U}.',
  'Wohnung 27, nach Osten ausgerichtet, mit {N91.12} {U} bebauter Fläche und einer unüberdachten Terrasse von {N42.15} {U}.',
  'Квартира 27 — окна на восток, {N91.12} {U} застроенной площади и открытая терраса {N42.15} {U}.',
  'المسكن 27 يتجه نحو الشرق، بمساحة مبنية {N91.12} {U} وتراس مكشوف مساحته {N42.15} {U}.',
  'Woning 27, gericht op het oosten, met {N91.12} {U} bebouwd en een onoverdekt terras van {N42.15} {U}.',
  'Lokal 27, skierowany na wschód, z powierzchnią zabudowy {N91.12} {U} i nieosłoniętym tarasem o powierzchni {N42.15} {U}.',
  'Bolig 27, vendt mot øst, med {N91.12} {U} bygd og en åpen terrasse på {N42.15} {U}.',
  'Bostad 27, vänd mot öster, med {N91.12} {U} byggyta och en öppen terrass på {N42.15} {U}.')

# ---------------------------------------------------------------- lifestyle, location
a('Living in <em>Las Lagunas</em>', 'Vivir en <em>Las Lagunas</em>', 'Vivre à <em>Las Lagunas</em>', 'Leben in <em>Las Lagunas</em>',
  'Жизнь в <em>Лас-Лагунас</em>', 'العيش في <em>لاس لاغوناس</em>', 'Wonen in <em>Las Lagunas</em>', 'Życie w <em>Las Lagunas</em>',
  'Å bo i <em>Las Lagunas</em>', 'Att bo i <em>Las Lagunas</em>')
a('An established residential area of Mijas, with the coast and the motorways close by.',
  'Una zona residencial consolidada de Mijas, con la costa y las autovías cerca.',
  'Un quartier résidentiel établi de Mijas, avec la côte et les autoroutes à proximité.',
  'Ein etabliertes Wohngebiet von Mijas, mit der Küste und den Autobahnen in der Nähe.',
  'Сложившийся жилой район Михаса, рядом с побережьем и автомагистралями.',
  'منطقة سكنية راسخة في ميخاس، قريبة من الساحل والطرق السريعة.',
  'Een gevestigde woonwijk van Mijas, met de kust en de snelwegen dichtbij.',
  'Ugruntowana okolica mieszkalna w Mijas, w pobliżu wybrzeża i autostrad.',
  'Et etablert boligområde i Mijas, med kysten og motorveiene i nærheten.',
  'Ett etablerat bostadsområde i Mijas, med kusten och motorvägarna nära.')
a('On the roof', 'En la azotea', 'Sur le toit', 'Auf dem Dach', 'На крыше', 'على السطح', 'Op het dak', 'Na dachu', 'På taket', 'På taket')
a('The developer’s portal lists a rooftop pool and a solarium; the renders show a sun terrace with loungers and a planted edge.',
  'El portal del promotor menciona una piscina y un solárium en la azotea; las imágenes muestran una terraza solárium con tumbonas y un borde ajardinado.',
  'Le portail du promoteur mentionne une piscine et un solarium sur le toit ; les images montrent une terrasse solarium avec bains de soleil et un bord planté.',
  'Das Portal des Bauträgers nennt einen Dachpool und ein Solarium; die Darstellungen zeigen eine Sonnenterrasse mit Liegen und bepflanztem Rand.',
  'На портале застройщика упомянуты бассейн и солярий на крыше; на визуализациях — терраса для загара с шезлонгами и озеленённым краем.',
  'تذكر بوابة المطوّر مسبحًا وسولاريوم على السطح، وتُظهر الصور تراسًا للتشمس بكراسي استلقاء وحافة مزروعة.',
  'Het portaal van de ontwikkelaar noemt een dakzwembad en een solarium; de beelden tonen een zonneterras met ligbedden en een beplante rand.',
  'Portal dewelopera wymienia basen i solarium na dachu; wizualizacje pokazują taras do opalania z leżakami i obsadzoną krawędzią.',
  'Utbyggerens portal nevner et takbasseng og en solterrasse; bildene viser en solterrasse med solsenger og en beplantet kant.',
  'Exploatörens portal nämner en takpool och en solterrass; bilderna visar en solterrass med solstolar och en planterad kant.')
a('Around the building', 'Alrededor del edificio', 'Autour de l’immeuble', 'Rund um das Gebäude', 'Вокруг здания', 'حول المبنى',
  'Rond het gebouw', 'Wokół budynku', 'Rundt bygningen', 'Runt byggnaden')
a('The brochure describes the area as surrounded by schools, sports centres, shops and restaurants.',
  'El folleto describe la zona como rodeada de colegios, centros deportivos, comercios y restaurantes.',
  'La brochure décrit le quartier comme entouré d’écoles, de centres sportifs, de commerces et de restaurants.',
  'Die Broschüre beschreibt die Umgebung als umgeben von Schulen, Sportzentren, Geschäften und Restaurants.',
  'В брошюре район описан как окружённый школами, спортивными центрами, магазинами и ресторанами.',
  'يصف الكتيّب المنطقة بأنها محاطة بمدارس ومراكز رياضية ومتاجر ومطاعم.',
  'De brochure beschrijft de omgeving als omringd door scholen, sportcentra, winkels en restaurants.',
  'Broszura opisuje okolicę jako otoczoną szkołami, centrami sportowymi, sklepami i restauracjami.',
  'Brosjyren beskriver området som omgitt av skoler, idrettssentre, butikker og restauranter.',
  'Broschyren beskriver området som omgivet av skolor, idrottsanläggningar, butiker och restauranger.')
a('The beaches of Mijas Costa are a few minutes away, according to the brochure.',
  'Según el folleto, las playas de Mijas Costa están a pocos minutos.',
  'Selon la brochure, les plages de Mijas Costa sont à quelques minutes.',
  'Laut Broschüre sind die Strände von Mijas Costa nur wenige Minuten entfernt.',
  'По данным брошюры, пляжи Михас-Коста находятся в нескольких минутах.',
  'بحسب الكتيّب، تبعد شواطئ ميخاس كوستا بضع دقائق.',
  'Volgens de brochure liggen de stranden van Mijas Costa op enkele minuten.',
  'Według broszury plaże Mijas Costa są oddalone o kilka minut.',
  'Ifølge brosjyren er strendene i Mijas Costa noen få minutter unna.',
  'Enligt broschyren ligger stränderna i Mijas Costa några minuter bort.')
a('The A-7 and AP-7 are close by, which puts Fuengirola, Marbella and Málaga within reach.',
  'La A-7 y la AP-7 están cerca, lo que sitúa Fuengirola, Marbella y Málaga al alcance.',
  'L’A-7 et l’AP-7 sont proches, ce qui met Fuengirola, Marbella et Málaga à portée.',
  'Die A-7 und die AP-7 sind nah, sodass Fuengirola, Marbella und Málaga gut erreichbar sind.',
  'Автомагистрали A-7 и AP-7 рядом, поэтому Фуэнхирола, Марбелья и Малага легко доступны.',
  'الطريقان A-7 وAP-7 قريبان، مما يجعل فوينخيرولا ومربيا ومالقة في المتناول.',
  'De A-7 en AP-7 liggen dichtbij, zodat Fuengirola, Marbella en Málaga goed bereikbaar zijn.',
  'Autostrady A-7 i AP-7 są w pobliżu, dzięki czemu Fuengirola, Marbella i Málaga są w zasięgu.',
  'A-7 og AP-7 ligger like ved, så Fuengirola, Marbella og Málaga er lett tilgjengelige.',
  'A-7 och AP-7 ligger nära, vilket gör Fuengirola, Marbella och Málaga lättillgängliga.')
a('Las Lagunas de Mijas, <em>a few minutes from the beaches</em>',
  'Las Lagunas de Mijas, <em>a pocos minutos de las playas</em>', 'Las Lagunas de Mijas, <em>à quelques minutes des plages</em>',
  'Las Lagunas de Mijas, <em>wenige Minuten von den Stränden</em>', 'Лас-Лагунас-де-Михас, <em>в нескольких минутах от пляжей</em>',
  'لاس لاغوناس دي ميهاس، <em>على بعد بضع دقائق من الشواطئ</em>', 'Las Lagunas de Mijas, <em>enkele minuten van de stranden</em>',
  'Las Lagunas de Mijas, <em>kilka minut od plaż</em>', 'Las Lagunas de Mijas, <em>noen få minutter fra strendene</em>',
  'Las Lagunas de Mijas, <em>några minuter från stränderna</em>')
a('The development is in Las Lagunas de Mijas, an established residential area. The brochure places it a few minutes from the beaches of Mijas Costa, with immediate access to the A-7 and AP-7, between Fuengirola, Marbella and Málaga.',
  'La promoción está en Las Lagunas de Mijas, una zona residencial consolidada. El folleto la sitúa a pocos minutos de las playas de Mijas Costa, con acceso inmediato a la A-7 y la AP-7, entre Fuengirola, Marbella y Málaga.',
  'Le programme se trouve à Las Lagunas de Mijas, un quartier résidentiel établi. La brochure le situe à quelques minutes des plages de Mijas Costa, avec un accès immédiat à l’A-7 et à l’AP-7, entre Fuengirola, Marbella et Málaga.',
  'Das Projekt liegt in Las Lagunas de Mijas, einem etablierten Wohngebiet. Die Broschüre verortet es wenige Minuten von den Stränden von Mijas Costa entfernt, mit unmittelbarem Zugang zur A-7 und zur AP-7, zwischen Fuengirola, Marbella und Málaga.',
  'Комплекс находится в Лас-Лагунас-де-Михас — сложившемся жилом районе. По данным брошюры, до пляжей Михас-Коста несколько минут, а выезд на A-7 и AP-7 — сразу, между Фуэнхиролой, Марбельей и Малагой.',
  'يقع المشروع في لاس لاغوناس دي ميهاس، وهي منطقة سكنية راسخة. ويضعه الكتيّب على بعد بضع دقائق من شواطئ ميخاس كوستا، مع وصول مباشر إلى الطريقين A-7 وAP-7، بين فوينخيرولا ومربيا ومالقة.',
  'Het project ligt in Las Lagunas de Mijas, een gevestigde woonwijk. De brochure plaatst het enkele minuten van de stranden van Mijas Costa, met directe toegang tot de A-7 en de AP-7, tussen Fuengirola, Marbella en Málaga.',
  'Inwestycja znajduje się w Las Lagunas de Mijas, ugruntowanej okolicy mieszkalnej. Broszura umieszcza ją kilka minut od plaż Mijas Costa, z bezpośrednim dostępem do A-7 i AP-7, między Fuengirolą, Marbellą i Málagą.',
  'Prosjektet ligger i Las Lagunas de Mijas, et etablert boligområde. Brosjyren plasserer det noen få minutter fra strendene i Mijas Costa, med umiddelbar tilgang til A-7 og AP-7, mellom Fuengirola, Marbella og Málaga.',
  'Projektet ligger i Las Lagunas de Mijas, ett etablerat bostadsområde. Broschyren placerar det några minuter från stränderna i Mijas Costa, med omedelbar tillgång till A-7 och AP-7, mellan Fuengirola, Marbella och Málaga.')
a('Beaches of Mijas Costa', 'Playas de Mijas Costa', 'Plages de Mijas Costa', 'Strände von Mijas Costa', 'Пляжи Михас-Коста',
  'شواطئ ميخاس كوستا', 'Stranden van Mijas Costa', 'Plaże Mijas Costa', 'Strendene i Mijas Costa', 'Stränderna i Mijas Costa')
a('A-7 and AP-7', 'A-7 y AP-7', 'A-7 et AP-7', 'A-7 und AP-7', 'A-7 и AP-7', 'A-7 وAP-7', 'A-7 en AP-7', 'A-7 i AP-7', 'A-7 og AP-7', 'A-7 och AP-7')
a('Immediate access', 'Acceso inmediato', 'Accès immédiat', 'Unmittelbarer Zugang', 'Выезд рядом', 'وصول مباشر', 'Directe toegang', 'Bezpośredni dostęp',
  'Umiddelbar tilgang', 'Omedelbar tillgång')

# ---------------------------------------------------------------- purchase
a('The portal lists a reservation of EUR 3,000 plus VAT for national buyers and EUR 6,000 plus VAT for international buyers.',
  'El portal indica una reserva de {E3000} más IVA para compradores nacionales y de {E6000} más IVA para compradores internacionales.',
  'Le portail indique une réservation de {E3000} hors TVA pour les acquéreurs nationaux et de {E6000} hors TVA pour les acquéreurs internationaux.',
  'Das Portal nennt eine Reservierung von {E3000} zuzüglich MwSt. für nationale Käufer und von {E6000} zuzüglich MwSt. für internationale Käufer.',
  'На портале указано бронирование {E3000} плюс НДС для национальных покупателей и {E6000} плюс НДС для международных покупателей.',
  'تذكر البوابة حجزًا بمبلغ {E3000} زائد ضريبة القيمة المضافة للمشترين المحليين و{E6000} زائد ضريبة القيمة المضافة للمشترين الدوليين.',
  'Het portaal vermeldt een reservering van {E3000} plus btw voor nationale kopers en van {E6000} plus btw voor internationale kopers.',
  'Portal podaje rezerwację w wysokości {E3000} plus VAT dla nabywców krajowych i {E6000} plus VAT dla nabywców zagranicznych.',
  'Portalen oppgir en reservasjon på {E3000} pluss mva. for nasjonale kjøpere og {E6000} pluss mva. for internasjonale kjøpere.',
  'Portalen anger en reservation på {E3000} plus moms för nationella köpare och {E6000} plus moms för internationella köpare.')
a('For national buyers: 10% plus VAT on the purchase contract, 10% plus VAT deferred, and 80% plus VAT on the deed. For international buyers: 20% plus VAT on the purchase contract, 10% plus VAT deferred, and 70% plus VAT on the deed.',
  'Para compradores nacionales: el 10% más IVA con el contrato de compraventa, el 10% más IVA aplazado y el 80% más IVA en la escritura. Para compradores internacionales: el 20% más IVA con el contrato de compraventa, el 10% más IVA aplazado y el 70% más IVA en la escritura.',
  'Pour les acquéreurs nationaux : 10 % hors TVA au contrat de vente, 10 % hors TVA différés et 80 % hors TVA à l’acte notarié. Pour les acquéreurs internationaux : 20 % hors TVA au contrat de vente, 10 % hors TVA différés et 70 % hors TVA à l’acte notarié.',
  'Für nationale Käufer: 10 % zuzüglich MwSt. bei Abschluss des Kaufvertrags, 10 % zuzüglich MwSt. zurückgestellt und 80 % zuzüglich MwSt. bei der notariellen Beurkundung. Für internationale Käufer: 20 % zuzüglich MwSt. bei Abschluss des Kaufvertrags, 10 % zuzüglich MwSt. zurückgestellt und 70 % zuzüglich MwSt. bei der notariellen Beurkundung.',
  'Для национальных покупателей: 10 % плюс НДС при договоре купли-продажи, 10 % плюс НДС отсрочено и 80 % плюс НДС при нотариальном акте. Для международных покупателей: 20 % плюс НДС при договоре купли-продажи, 10 % плюс НДС отсрочено и 70 % плюс НДС при нотариальном акте.',
  'للمشترين المحليين: 10% زائد ضريبة القيمة المضافة عند عقد الشراء، و10% زائد الضريبة مؤجلة، و80% زائد الضريبة عند سند الملكية أمام كاتب العدل. للمشترين الدوليين: 20% زائد ضريبة القيمة المضافة عند عقد الشراء، و10% زائد الضريبة مؤجلة، و70% زائد الضريبة عند سند الملكية أمام كاتب العدل.',
  'Voor nationale kopers: 10% plus btw bij de koopovereenkomst, 10% plus btw uitgesteld en 80% plus btw bij de notariële akte. Voor internationale kopers: 20% plus btw bij de koopovereenkomst, 10% plus btw uitgesteld en 70% plus btw bij de notariële akte.',
  'Dla nabywców krajowych: 10% plus VAT przy umowie kupna-sprzedaży, 10% plus VAT odroczone i 80% plus VAT przy akcie notarialnym. Dla nabywców zagranicznych: 20% plus VAT przy umowie kupna-sprzedaży, 10% plus VAT odroczone i 70% plus VAT przy akcie notarialnym.',
  'For nasjonale kjøpere: 10 % pluss mva. ved kjøpekontrakten, 10 % pluss mva. utsatt og 80 % pluss mva. ved skjøtet. For internasjonale kjøpere: 20 % pluss mva. ved kjøpekontrakten, 10 % pluss mva. utsatt og 70 % pluss mva. ved skjøtet.',
  'För nationella köpare: 10 % plus moms vid köpeavtalet, 10 % plus moms uppskjutet och 80 % plus moms vid tillträdet hos notarien. För internationella köpare: 20 % plus moms vid köpeavtalet, 10 % plus moms uppskjutet och 70 % plus moms vid tillträdet hos notarien.')
a('The price list shows prices without VAT and does not give the rate. Nueva Living confirms the taxes and purchase costs in writing.',
  'La lista de precios muestra los precios sin IVA y no indica el tipo. Nueva Living confirma por escrito los impuestos y los gastos de compra.',
  'La liste de prix présente les prix hors TVA et n’en indique pas le taux. Nueva Living confirme par écrit les taxes et les frais d’achat.',
  'Die Preisliste nennt die Preise ohne MwSt. und gibt den Satz nicht an. Nueva Living bestätigt Steuern und Kaufnebenkosten schriftlich.',
  'В прайс-листе цены указаны без НДС, ставка не приведена. Nueva Living письменно подтверждает налоги и расходы на покупку.',
  'تعرض قائمة الأسعار الأسعار دون ضريبة القيمة المضافة ولا تذكر نسبتها. وتؤكد Nueva Living الضرائب ومصاريف الشراء كتابةً.',
  'De prijslijst toont de prijzen exclusief btw en geeft het tarief niet. Nueva Living bevestigt de belastingen en aankoopkosten schriftelijk.',
  'Cennik podaje ceny bez VAT i nie wskazuje stawki. Nueva Living potwierdza na piśmie podatki i koszty zakupu.',
  'Prislisten viser prisene uten mva. og oppgir ikke satsen. Nueva Living bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan visar priserna utan moms och anger inte skattesatsen. Nueva Living bekräftar skatter och köpkostnader skriftligen.')
a('Garage and storeroom', 'Garaje y trastero', 'Garage et débarras', 'Garage und Abstellraum', 'Гараж и кладовая', 'المرآب والمخزن',
  'Garage en berging', 'Garaż i komórka lokatorska', 'Garasje og bod', 'Garage och förråd')
a('The price list assigns each home a garage space and a storeroom but does not say whether they are in the price, so we confirm it in writing.',
  'La lista de precios asigna a cada vivienda una plaza de garaje y un trastero, pero no dice si están incluidos en el precio, por lo que lo confirmamos por escrito.',
  'La liste de prix attribue à chaque logement une place de garage et un débarras mais ne dit pas s’ils sont inclus dans le prix ; nous le confirmons donc par écrit.',
  'Die Preisliste ordnet jeder Wohnung einen Garagenstellplatz und einen Abstellraum zu, sagt aber nicht, ob sie im Preis enthalten sind; wir bestätigen das daher schriftlich.',
  'В прайс-листе за каждой квартирой закреплены место в гараже и кладовая, но не сказано, входят ли они в цену, поэтому мы подтверждаем это письменно.',
  'تخصص قائمة الأسعار لكل مسكن موقفًا في المرآب ومخزنًا لكنها لا تذكر ما إذا كانا مشمولين في السعر، لذلك نؤكد ذلك كتابةً.',
  'De prijslijst wijst elke woning een garageplaats en een berging toe, maar vermeldt niet of ze in de prijs zijn inbegrepen, dus we bevestigen dat schriftelijk.',
  'Cennik przypisuje każdemu lokalowi miejsce garażowe i komórkę lokatorską, ale nie podaje, czy są wliczone w cenę, dlatego potwierdzamy to na piśmie.',
  'Prislisten tildeler hver bolig en garasjeplass og en bod, men sier ikke om de er inkludert i prisen, så vi bekrefter det skriftlig.',
  'Prislistan tilldelar varje bostad en garageplats och ett förråd men anger inte om de ingår i priset, så vi bekräftar det skriftligen.')

# ---------------------------------------------------------------- what we check
a('The developer’s portal gives June 2028 and the brochure gives no date, so we ask for the contractual date.',
  'El portal del promotor indica junio de 2028 y el folleto no da ninguna fecha, por lo que pedimos la fecha contractual.',
  'Le portail du promoteur indique juin 2028 et la brochure ne donne aucune date ; nous demandons donc la date contractuelle.',
  'Das Portal des Bauträgers nennt Juni 2028, die Broschüre nennt kein Datum; wir fragen daher das vertragliche Datum an.',
  'На портале застройщика указан июнь 2028 года, а в брошюре даты нет, поэтому мы запрашиваем договорную дату.',
  'تذكر بوابة المطوّر يونيو 2028 ولا يذكر الكتيّب أي تاريخ، لذلك نطلب التاريخ التعاقدي.',
  'Het portaal van de ontwikkelaar noemt juni 2028 en de brochure noemt geen datum, dus we vragen naar de contractuele datum.',
  'Portal dewelopera podaje czerwiec 2028 r., a broszura nie podaje żadnej daty, dlatego prosimy o termin wskazany w umowie.',
  'Utbyggerens portal oppgir juni 2028 og brosjyren oppgir ingen dato, så vi ber om den kontraktsfestede datoen.',
  'Exploatörens portal anger juni 2028 och broschyren anger inget datum, så vi ber om det avtalade datumet.')
a('The documents do not say whether the building licence is granted. We ask for the licence and for the bank guarantee that covers amounts paid on account.',
  'Los documentos no dicen si la licencia de obras está concedida. Pedimos la licencia y el aval bancario que cubre las cantidades entregadas a cuenta.',
  'Les documents ne disent pas si le permis de construire est accordé. Nous demandons le permis et la garantie bancaire couvrant les sommes versées en acompte.',
  'Die Unterlagen sagen nicht, ob die Baugenehmigung erteilt ist. Wir fordern die Genehmigung und die Bankgarantie an, die geleistete Anzahlungen absichert.',
  'В документах не сказано, получено ли разрешение на строительство. Мы запрашиваем разрешение и банковскую гарантию, покрывающую суммы, внесённые в счёт покупки.',
  'لا تذكر الوثائق ما إذا كانت رخصة البناء ممنوحة. ونطلب الرخصة والضمان المصرفي الذي يغطي المبالغ المدفوعة على الحساب.',
  'De documenten vermelden niet of de bouwvergunning is verleend. We vragen om de vergunning en om de bankgarantie die de vooruitbetaalde bedragen dekt.',
  'Dokumenty nie mówią, czy pozwolenie na budowę zostało wydane. Prosimy o pozwolenie i gwarancję bankową zabezpieczającą wpłacone zaliczki.',
  'Dokumentene sier ikke om byggetillatelsen er gitt. Vi ber om tillatelsen og bankgarantien som dekker beløp betalt på forskudd.',
  'Dokumenten anger inte om bygglovet är beviljat. Vi ber om bygglovet och om bankgarantin som täcker belopp som betalats i förskott.')
a('The price list and the plans give different figures: for Home 2 the list gives 59.87 sqm interior and the plan 40.92 sqm. We confirm which figure the contract uses.',
  'La lista de precios y los planos dan cifras distintas: para la vivienda 2, la lista da {N59.87} {U} interiores y el plano {N40.92} {U}. Confirmamos qué cifra utiliza el contrato.',
  'La liste de prix et les plans donnent des chiffres différents : pour le logement 2, la liste indique {N59.87} {U} intérieurs et le plan {N40.92} {U}. Nous confirmons quel chiffre retient le contrat.',
  'Preisliste und Pläne nennen unterschiedliche Zahlen: Für Wohnung 2 nennt die Liste {N59.87} {U} Innenfläche und der Grundriss {N40.92} {U}. Wir klären, welche Zahl der Vertrag verwendet.',
  'В прайс-листе и на планах разные цифры: для квартиры 2 в прайс-листе {N59.87} {U} внутренней площади, а на плане {N40.92} {U}. Мы уточняем, какая цифра используется в договоре.',
  'تختلف الأرقام بين قائمة الأسعار والمخططات: للمسكن 2 تذكر القائمة {N59.87} {U} مساحة داخلية ويذكر المخطط {N40.92} {U}. نتحقق من الرقم الذي يعتمده العقد.',
  'De prijslijst en de plattegronden geven verschillende cijfers: voor woning 2 vermeldt de lijst {N59.87} {U} binnenoppervlakte en de plattegrond {N40.92} {U}. We bevestigen welk cijfer het contract hanteert.',
  'Cennik i rzuty podają różne wartości: dla lokalu 2 cennik podaje {N59.87} {U} powierzchni wewnętrznej, a rzut {N40.92} {U}. Potwierdzamy, którą wartość przyjmuje umowa.',
  'Prislisten og plantegningene oppgir ulike tall: for bolig 2 oppgir listen {N59.87} {U} innvendig og planen {N40.92} {U}. Vi bekrefter hvilket tall kontrakten bruker.',
  'Prislistan och planritningarna anger olika siffror: för bostad 2 anger listan {N59.87} {U} invändig yta och planritningen {N40.92} {U}. Vi bekräftar vilken siffra avtalet använder.')
a('The titles of seven plans name a floor one level above the floor on their own table and on the price list. We match each home by its number and confirm it in writing.',
  'Los títulos de siete planos nombran una planta un nivel por encima de la que figura en su propia tabla y en la lista de precios. Identificamos cada vivienda por su número y lo confirmamos por escrito.',
  'Les titres de sept plans désignent un étage situé un niveau au-dessus de celui de leur propre tableau et de la liste de prix. Nous identifions chaque logement par son numéro et le confirmons par écrit.',
  'Die Titel von sieben Plänen nennen ein Geschoss, das eine Ebene über dem Geschoss in ihrer eigenen Tabelle und in der Preisliste liegt. Wir ordnen jede Wohnung über ihre Nummer zu und bestätigen das schriftlich.',
  'В заголовках семи планов указан этаж на один выше, чем в их собственной таблице и в прайс-листе. Мы сопоставляем каждую квартиру по номеру и подтверждаем это письменно.',
  'تذكر عناوين سبعة مخططات طابقًا أعلى بمستوى واحد من الطابق المذكور في جدولها الخاص وفي قائمة الأسعار. نطابق كل مسكن برقمه ونؤكد ذلك كتابةً.',
  'De titels van zeven plattegronden noemen een verdieping één niveau hoger dan de verdieping in hun eigen tabel en op de prijslijst. We koppelen elke woning aan haar nummer en bevestigen dat schriftelijk.',
  'Tytuły siedmiu rzutów wskazują piętro o jeden poziom wyższe niż piętro w ich własnej tabeli i w cenniku. Dopasowujemy każdy lokal według numeru i potwierdzamy to na piśmie.',
  'Titlene på sju plantegninger oppgir en etasje ett nivå over etasjen i deres egen tabell og i prislisten. Vi knytter hver bolig til nummeret og bekrefter det skriftlig.',
  'Titlarna på sju planritningar anger en våning en nivå över våningen i deras egen tabell och i prislistan. Vi knyter varje bostad till dess nummer och bekräftar det skriftligen.')

# ---------------------------------------------------------------- availability
a('17 homes <em>currently listed</em>', '17 viviendas <em>actualmente en lista</em>', '17 logements <em>actuellement en vente</em>',
  '17 Wohnungen <em>aktuell gelistet</em>', '17 квартир <em>сейчас в продаже</em>', '17 مسكنًا <em>معروضة حاليًا</em>',
  '17 woningen <em>momenteel vermeld</em>', '17 lokali <em>aktualnie w ofercie</em>', '17 boliger <em>oppført nå</em>', '17 bostäder <em>listade just nu</em>')
a('Prices are those of the developer’s price list as shown on its portal in October 2026 and exclude VAT. Homes are numbered as on that list, and prices are confirmed before reservation.',
  'Los precios son los de la lista de precios del promotor tal como aparece en su portal en octubre de 2026 y no incluyen IVA. Las viviendas se numeran como en esa lista y los precios se confirman antes de la reserva.',
  'Les prix sont ceux de la liste de prix du promoteur telle qu’elle figure sur son portail en octobre 2026 et s’entendent hors TVA. Les logements sont numérotés comme sur cette liste et les prix sont confirmés avant la réservation.',
  'Die Preise stammen aus der Preisliste des Bauträgers, wie sie im Oktober 2026 auf dessen Portal zu sehen war, und verstehen sich zuzüglich MwSt. Die Wohnungen sind wie in dieser Liste nummeriert, und die Preise werden vor der Reservierung bestätigt.',
  'Цены взяты из прайс-листа застройщика, опубликованного на его портале в октябре 2026 года, и не включают НДС. Квартиры пронумерованы так же, как в этом списке, а цены подтверждаются перед бронированием.',
  'الأسعار هي أسعار قائمة المطوّر كما ظهرت على بوابته في أكتوبر 2026، ولا تشمل ضريبة القيمة المضافة. وترقيم المساكن كما في تلك القائمة، وتُؤكَّد الأسعار قبل الحجز.',
  'De prijzen komen uit de prijslijst van de ontwikkelaar zoals die in oktober 2026 op zijn portaal stond en zijn exclusief btw. De woningen zijn genummerd zoals op die lijst en de prijzen worden vóór de reservering bevestigd.',
  'Ceny pochodzą z cennika dewelopera widocznego na jego portalu w październiku 2026 roku i nie zawierają VAT. Lokale są numerowane tak jak w tym cenniku, a ceny są potwierdzane przed rezerwacją.',
  'Prisene er de i utbyggerens prisliste slik den sto på portalen i oktober 2026, og er eksklusive mva. Boligene er nummerert som i den listen, og prisene bekreftes før reservasjon.',
  'Priserna är de i exploatörens prislista så som den visades på dess portal i oktober 2026 och är exklusive moms. Bostäderna är numrerade som i den listan, och priserna bekräftas före bokning.')
a('Prices, areas, bedrooms and terraces are transcribed from the developer’s price list as shown on its portal in October 2026, which lists 17 homes as available and shows prices without VAT, without giving a rate. The list gives an interior area and a built area, the latter in a column headed built plus common areas, and the plans give different figures. For Home 2 the plan shows 64.46 sqm built, 106.18 sqm including the terrace, the storeroom, the garage space and a share of the common areas, and 40.92 sqm of interior, against 67.47 sqm built and 59.87 sqm interior on the list; for Home 27 it shows 74.10 sqm of interior against 62.84. The list gives a terrace of 2.70 sqm for Homes 9 and 10, whose plans show none. The garage space numbers on the plans differ from those on the list, so none are published. The plans of Homes 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 and 27 are attached to those homes; the other homes have no plan in the documents. The titles of the plans for Homes 9, 10, 11, 16, 18, 23 and 25 name a floor one level above the one on their own table and on the price list, and the table is followed here.',
  'Los precios, las superficies, los dormitorios y las terrazas están transcritos de la lista de precios del promotor tal como aparece en su portal en octubre de 2026, que lista 17 viviendas como disponibles y muestra los precios sin IVA, sin indicar el tipo. La lista da una superficie interior y una superficie construida, esta última en una columna titulada construida más zonas comunes, y los planos dan cifras distintas. Para la vivienda 2, el plano muestra {N64.46} {U} construidos, {N106.18} {U} incluyendo la terraza, el trastero, la plaza de garaje y una parte proporcional de zonas comunes, y {N40.92} {U} interiores, frente a {N67.47} {U} construidos y {N59.87} {U} interiores en la lista; para la vivienda 27 muestra {N74.10} {U} interiores frente a {N62.84}. La lista da una terraza de {N2.70} {U} para las viviendas 9 y 10, cuyos planos no muestran ninguna. Los números de plaza de garaje de los planos difieren de los de la lista, por lo que no se publica ninguno. Los planos de las viviendas 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 y 27 se asignan a esas viviendas; las demás no tienen plano en los documentos. Los títulos de los planos de las viviendas 9, 10, 11, 16, 18, 23 y 25 nombran una planta un nivel por encima de la que figura en su propia tabla y en la lista de precios, y aquí se sigue la tabla.',
  'Les prix, surfaces, nombres de chambres et terrasses sont transcrits de la liste de prix du promoteur telle qu’elle figure sur son portail en octobre 2026, qui indique 17 logements comme disponibles et présente les prix hors TVA, sans en donner le taux. La liste donne une surface intérieure et une surface construite, cette dernière dans une colonne intitulée construite plus parties communes, et les plans donnent des chiffres différents. Pour le logement 2, le plan indique {N64.46} {U} construits, {N106.18} {U} avec la terrasse, le débarras, la place de garage et une quote-part de parties communes, et {N40.92} {U} intérieurs, contre {N67.47} {U} construits et {N59.87} {U} intérieurs sur la liste ; pour le logement 27, il indique {N74.10} {U} intérieurs contre {N62.84}. La liste donne une terrasse de {N2.70} {U} pour les logements 9 et 10, dont les plans n’en montrent aucune. Les numéros de places de garage des plans diffèrent de ceux de la liste ; aucun n’est donc publié. Les plans des logements 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 et 27 sont rattachés à ces logements ; les autres n’ont pas de plan dans les documents. Les titres des plans des logements 9, 10, 11, 16, 18, 23 et 25 désignent un étage situé un niveau au-dessus de celui de leur propre tableau et de la liste de prix, et c’est le tableau qui est suivi ici.',
  'Preise, Flächen, Schlafzimmer und Terrassen sind der Preisliste des Bauträgers entnommen, wie sie im Oktober 2026 auf dessen Portal zu sehen war; sie führt 17 Wohnungen als verfügbar auf und nennt die Preise ohne MwSt., ohne den Satz anzugeben. Die Liste nennt eine Innenfläche und eine bebaute Fläche, Letztere in einer Spalte mit der Überschrift bebaut plus Gemeinschaftsflächen, und die Pläne nennen andere Zahlen. Für Wohnung 2 zeigt der Plan {N64.46} {U} bebaute Fläche, {N106.18} {U} einschließlich Terrasse, Abstellraum, Garagenstellplatz und eines Anteils an den Gemeinschaftsflächen sowie {N40.92} {U} Innenfläche, gegenüber {N67.47} {U} bebauter Fläche und {N59.87} {U} Innenfläche in der Liste; für Wohnung 27 zeigt er {N74.10} {U} Innenfläche gegenüber {N62.84}. Die Liste nennt für die Wohnungen 9 und 10 eine Terrasse von {N2.70} {U}, deren Pläne keine zeigen. Die Nummern der Garagenstellplätze in den Plänen weichen von denen der Liste ab, daher wird keine veröffentlicht. Die Pläne der Wohnungen 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 und 27 sind diesen Wohnungen zugeordnet; die übrigen Wohnungen haben in den Unterlagen keinen Plan. Die Titel der Pläne der Wohnungen 9, 10, 11, 16, 18, 23 und 25 nennen ein Geschoss, das eine Ebene über dem in ihrer eigenen Tabelle und in der Preisliste liegt, und hier wird die Tabelle zugrunde gelegt.',
  'Цены, площади, количество спален и террасы перенесены из прайс-листа застройщика, опубликованного на его портале в октябре 2026 года; в нём 17 квартир значатся доступными, а цены указаны без НДС, ставка не приведена. В прайс-листе указаны внутренняя и застроенная площади, причём вторая — в столбце с заголовком «застроенная плюс общие зоны», а на планах цифры другие. Для квартиры 2 на плане указаны {N64.46} {U} застроенной площади, {N106.18} {U} с учётом террасы, кладовой, места в гараже и доли общих зон и {N40.92} {U} внутренней площади, а в прайс-листе — {N67.47} {U} застроенной и {N59.87} {U} внутренней; для квартиры 27 на плане {N74.10} {U} внутренней площади против {N62.84}. В прайс-листе для квартир 9 и 10 указана терраса {N2.70} {U}, а на их планах террас нет. Номера мест в гараже на планах отличаются от номеров в прайс-листе, поэтому они не публикуются. Планы квартир 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 и 27 привязаны к этим квартирам; у остальных в документах плана нет. В заголовках планов квартир 9, 10, 11, 16, 18, 23 и 25 указан этаж на один выше, чем в их собственной таблице и в прайс-листе, и здесь используется таблица.',
  'الأسعار والمساحات وغرف النوم والتراسات منقولة من قائمة أسعار المطوّر كما ظهرت على بوابته في أكتوبر 2026، وهي تدرج 17 مسكنًا كمتاحة وتعرض الأسعار دون ضريبة القيمة المضافة من غير ذكر نسبتها. وتذكر القائمة مساحة داخلية ومساحة مبنية، الأخيرة في عمود عنوانه مبنية زائد المناطق المشتركة، وتذكر المخططات أرقامًا مختلفة. فللمسكن 2 يُظهر المخطط {N64.46} {U} مساحة مبنية، و{N106.18} {U} شاملة التراس والمخزن وموقف المرآب وحصة من المناطق المشتركة، و{N40.92} {U} مساحة داخلية، مقابل {N67.47} {U} مبنية و{N59.87} {U} داخلية في القائمة؛ وللمسكن 27 يُظهر {N74.10} {U} مساحة داخلية مقابل {N62.84}. وتذكر القائمة تراسًا مساحته {N2.70} {U} للمسكنين 9 و10 بينما لا يُظهر مخططاهما أي تراس. وتختلف أرقام مواقف المرآب في المخططات عن أرقامها في القائمة، لذلك لا يُنشر أي منها. وترتبط مخططات المساكن 2 و4 و6 و9 و10 و11 و13 و15 و16 و18 و23 و25 و27 بهذه المساكن؛ أما المساكن الأخرى فلا مخطط لها في الوثائق. وتذكر عناوين مخططات المساكن 9 و10 و11 و16 و18 و23 و25 طابقًا أعلى بمستوى واحد من الطابق المذكور في جدولها الخاص وفي قائمة الأسعار، ويُعتمد الجدول هنا.',
  'Prijzen, oppervlakten, slaapkamers en terrassen zijn overgenomen uit de prijslijst van de ontwikkelaar zoals die in oktober 2026 op zijn portaal stond; die vermeldt 17 woningen als beschikbaar en toont de prijzen exclusief btw, zonder het tarief te geven. De lijst geeft een binnenoppervlakte en een bebouwde oppervlakte, de laatste in een kolom met de kop bebouwd plus gemeenschappelijke ruimten, en de plattegronden geven andere cijfers. Voor woning 2 toont de plattegrond {N64.46} {U} bebouwd, {N106.18} {U} inclusief het terras, de berging, de garageplaats en een aandeel in de gemeenschappelijke ruimten, en {N40.92} {U} binnenoppervlakte, tegenover {N67.47} {U} bebouwd en {N59.87} {U} binnenoppervlakte op de lijst; voor woning 27 toont zij {N74.10} {U} binnenoppervlakte tegenover {N62.84}. De lijst geeft een terras van {N2.70} {U} voor de woningen 9 en 10, waarvan de plattegronden er geen tonen. De nummers van de garageplaatsen op de plattegronden wijken af van die op de lijst, dus er wordt er geen gepubliceerd. De plattegronden van de woningen 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 en 27 zijn aan die woningen gekoppeld; de overige woningen hebben in de documenten geen plattegrond. De titels van de plattegronden van de woningen 9, 10, 11, 16, 18, 23 en 25 noemen een verdieping één niveau hoger dan die in hun eigen tabel en op de prijslijst, en hier wordt de tabel gevolgd.',
  'Ceny, powierzchnie, liczba sypialni i tarasy zostały przepisane z cennika dewelopera widocznego na jego portalu w październiku 2026 roku; wymienia on 17 lokali jako dostępne i podaje ceny bez VAT, bez wskazania stawki. Cennik podaje powierzchnię wewnętrzną i powierzchnię zabudowy, tę drugą w kolumnie zatytułowanej zabudowa plus części wspólne, a rzuty podają inne wartości. Dla lokalu 2 rzut pokazuje {N64.46} {U} zabudowy, {N106.18} {U} wraz z tarasem, komórką lokatorską, miejscem garażowym i udziałem w częściach wspólnych oraz {N40.92} {U} powierzchni wewnętrznej, wobec {N67.47} {U} zabudowy i {N59.87} {U} powierzchni wewnętrznej w cenniku; dla lokalu 27 pokazuje {N74.10} {U} powierzchni wewnętrznej wobec {N62.84}. Cennik podaje taras o powierzchni {N2.70} {U} dla lokali 9 i 10, których rzuty żadnego nie pokazują. Numery miejsc garażowych na rzutach różnią się od numerów w cenniku, dlatego żaden nie jest publikowany. Rzuty lokali 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 i 27 przypisano do tych lokali; pozostałe lokale nie mają rzutu w dokumentach. Tytuły rzutów lokali 9, 10, 11, 16, 18, 23 i 25 wskazują piętro o jeden poziom wyższe niż w ich własnej tabeli i w cenniku, a tutaj przyjęto tabelę.',
  'Priser, arealer, soverom og terrasser er gjengitt fra utbyggerens prisliste slik den sto på portalen i oktober 2026; den oppfører 17 boliger som ledige og viser prisene uten mva., uten å oppgi satsen. Listen oppgir et innvendig areal og et bebygd areal, det siste i en kolonne med overskriften bygd pluss fellesarealer, og plantegningene oppgir andre tall. For bolig 2 viser planen {N64.46} {U} bygd, {N106.18} {U} inkludert terrassen, boden, garasjeplassen og en andel av fellesarealene, og {N40.92} {U} innvendig, mot {N67.47} {U} bygd og {N59.87} {U} innvendig i listen; for bolig 27 viser den {N74.10} {U} innvendig mot {N62.84}. Listen oppgir en terrasse på {N2.70} {U} for bolig 9 og 10, hvis planer ikke viser noen. Nummerne på garasjeplassene i planene avviker fra dem i listen, så ingen er publisert. Planene for bolig 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 og 27 er knyttet til disse boligene; de andre boligene har ingen plan i dokumentene. Titlene på planene for bolig 9, 10, 11, 16, 18, 23 og 25 oppgir en etasje ett nivå over den i deres egen tabell og i prislisten, og tabellen følges her.',
  'Priser, ytor, sovrum och terrasser är hämtade från exploatörens prislista så som den visades på dess portal i oktober 2026; den listar 17 bostäder som lediga och visar priserna utan moms, utan att ange skattesatsen. Listan anger en invändig yta och en byggyta, den senare i en kolumn med rubriken byggd plus gemensamma ytor, och planritningarna anger andra siffror. För bostad 2 visar planritningen {N64.46} {U} byggyta, {N106.18} {U} inklusive terrassen, förrådet, garageplatsen och en andel av de gemensamma ytorna samt {N40.92} {U} invändig yta, mot {N67.47} {U} byggyta och {N59.87} {U} invändig yta i listan; för bostad 27 visar den {N74.10} {U} invändig yta mot {N62.84}. Listan anger en terrass på {N2.70} {U} för bostäderna 9 och 10, vars planritningar inte visar någon. Numren på garageplatserna i planritningarna skiljer sig från dem i listan, så inget publiceras. Planritningarna för bostäderna 2, 4, 6, 9, 10, 11, 13, 15, 16, 18, 23, 25 och 27 är kopplade till dessa bostäder; övriga bostäder har ingen planritning i dokumenten. Titlarna på planritningarna för bostäderna 9, 10, 11, 16, 18, 23 och 25 anger en våning en nivå över den i deras egen tabell och i prislistan, och tabellen följs här.')

# ---------------------------------------------------------------- next steps, viewing, enquiry, faq
a('The floorplans of the homes that have one, the quality specification and the price list.',
  'Los planos de las viviendas que lo tienen, la memoria de calidades y la lista de precios.',
  'Les plans des logements qui en ont un, le descriptif et la liste de prix.',
  'Die Grundrisse der Wohnungen, für die einer vorliegt, die Baubeschreibung und die Preisliste.',
  'Планировки тех квартир, для которых они есть, спецификация и прайс-лист.',
  'مخططات المساكن التي لها مخطط، ومواصفات البناء، وقائمة الأسعار.',
  'De plattegronden van de woningen waarvoor er een is, het lastenboek en de prijslijst.',
  'Rzuty lokali, które je mają, specyfikacja techniczna i cennik.',
  'Plantegningene til boligene som har en, spesifikasjonen og prislisten.',
  'Planritningarna för de bostäder som har en, specifikationen och prislistan.')
a('A reservation, then the private purchase contract, with the amounts paid on account guaranteed by a bank.',
  'Una reserva y después el contrato privado de compraventa, con las cantidades entregadas a cuenta garantizadas por un banco.',
  'Une réservation, puis le contrat de vente privé, avec les sommes versées en acompte garanties par une banque.',
  'Eine Reservierung, dann der private Kaufvertrag, mit bankgesicherten Anzahlungen.',
  'Бронирование, затем предварительный договор купли-продажи; суммы, внесённые в счёт покупки, гарантируются банком.',
  'حجز، ثم عقد الشراء الخاص، مع ضمان مصرفي للمبالغ المدفوعة على الحساب.',
  'Een reservering, daarna de onderhandse koopovereenkomst, met een bankgarantie op de vooruitbetaalde bedragen.',
  'Rezerwacja, następnie umowa przedwstępna, z wpłaconymi zaliczkami gwarantowanymi przez bank.',
  'En reservasjon, deretter den private kjøpekontrakten, med beløp betalt på forskudd garantert av en bank.',
  'En reservation, sedan det privata köpeavtalet, med belopp som betalats i förskott garanterade av en bank.')
a('Stand on the plot and see the street and the surroundings.',
  'Sitúese en la parcela y vea la calle y el entorno.', 'Foulez le terrain et voyez la rue et les alentours.',
  'Betreten Sie das Grundstück und sehen Sie die Straße und die Umgebung.', 'Встаньте на участке и посмотрите на улицу и окрестности.',
  'قف على أرض المشروع وشاهد الشارع والمحيط.', 'Sta op het perceel en zie de straat en de omgeving.',
  'Spojrzenie z działki na ulicę i okolicę.', 'Stå på tomten og se gaten og omgivelsene.', 'Stå på tomten och se gatan och omgivningarna.')
a('We walk to the shops and the services with you and time it.',
  'Caminamos con usted hasta las tiendas y los servicios y cronometramos el trayecto.', 'Nous vous accompagnons à pied jusqu’aux commerces et aux services, et nous chronométrons le trajet.',
  'Wir gehen mit Ihnen zu den Geschäften und Dienstleistungen und messen die Zeit.', 'Мы пройдёмся с вами до магазинов и сервисов и засечём время в пути.',
  'نمشي معك إلى المتاجر والخدمات ونحسب زمن الطريق.', 'We lopen met u naar de winkels en voorzieningen en meten de looptijd.',
  'Idziemy z Państwem pieszo do sklepów i usług, mierząc czas.', 'Vi går til butikkene og tjenestene sammen med dere og tar tiden.',
  'Vi går med er till butikerna och servicen och tar tiden.')

a('Ask about <em>Mirlo Residences</em>', 'Pregunte por <em>Mirlo Residences</em>', 'Renseignez-vous sur <em>Mirlo Residences</em>',
  'Fragen Sie nach <em>Mirlo Residences</em>', 'Узнайте о <em>Mirlo Residences</em>', 'استفسر عن <em>Mirlo Residences</em>',
  'Vraag naar <em>Mirlo Residences</em>', 'Zapytanie o <em>Mirlo Residences</em>', 'Spør om <em>Mirlo Residences</em>', 'Fråga om <em>Mirlo Residences</em>')
a('Hello Nueva Living, I would like information about Mirlo Residences.',
  'Hola, Nueva Living, me gustaría recibir información sobre Mirlo Residences.',
  'Bonjour Nueva Living, je souhaiterais des informations sur Mirlo Residences.',
  'Guten Tag Nueva Living, ich möchte Informationen zu Mirlo Residences erhalten.',
  'Здравствуйте, Nueva Living! Хочу получить информацию о Mirlo Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Mirlo Residences.',
  'Goedendag Nueva Living, ik wil graag informatie over Mirlo Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje o Mirlo Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Mirlo Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Mirlo Residences.')
a('The development has 29 homes and 17 are listed on the developer’s portal: four one-bedroom apartments, eleven two-bedroom apartments, one three-bedroom apartment and a two-bedroom penthouse, from EUR 213,000 to EUR 429,000 plus VAT.',
  'La promoción tiene 29 viviendas y 17 figuran en el portal del promotor: cuatro apartamentos de un dormitorio, once de dos dormitorios, uno de tres dormitorios y un ático de dos dormitorios, de {E213000} a {E429000} más IVA.',
  'Le programme compte 29 logements et 17 figurent sur le portail du promoteur : quatre appartements d’une chambre, onze de deux chambres, un de trois chambres et un penthouse de deux chambres, de {E213000} à {E429000} hors TVA.',
  'Das Projekt hat 29 Wohnungen, davon sind 17 im Portal des Bauträgers gelistet: vier Apartments mit einem Schlafzimmer, elf mit zwei Schlafzimmern, eines mit drei Schlafzimmern und ein Penthouse mit zwei Schlafzimmern, von {E213000} bis {E429000} zuzüglich MwSt.',
  'В комплексе 29 квартир, 17 из них указаны на портале застройщика: четыре апартамента с одной спальней, одиннадцать с двумя спальнями, один с тремя спальнями и пентхаус с двумя спальнями, от {E213000} до {E429000} плюс НДС.',
  'يضم المشروع 29 مسكنًا، منها 17 معروضة على بوابة المطوّر: أربع شقق بغرفة نوم واحدة، وإحدى عشرة شقة بغرفتي نوم، وشقة واحدة بثلاث غرف نوم، وبنتهاوس بغرفتي نوم، من {E213000} إلى {E429000} زائد ضريبة القيمة المضافة.',
  'Het project telt 29 woningen, waarvan er 17 op het portaal van de ontwikkelaar staan: vier appartementen met een slaapkamer, elf met twee slaapkamers, een met drie slaapkamers en een penthouse met twee slaapkamers, van {E213000} tot {E429000} plus btw.',
  'Inwestycja liczy 29 lokali, z czego 17 jest na portalu dewelopera: cztery apartamenty z jedną sypialnią, jedenaście z dwiema, jeden z trzema oraz penthouse z dwiema sypialniami, od {E213000} do {E429000} plus VAT.',
  'Prosjektet har 29 boliger, og 17 er oppført på utbyggerens portal: fire leiligheter med ett soverom, elleve med to soverom, én med tre soverom og en toppleilighet med to soverom, fra {E213000} til {E429000} pluss mva.',
  'Projektet har 29 bostäder och 17 är listade på exploatörens portal: fyra lägenheter med ett sovrum, elva med två sovrum, en med tre sovrum och en takvåning med två sovrum, från {E213000} till {E429000} plus moms.')
a('No. The price list shows prices without VAT and does not give the rate. We confirm the taxes and purchase costs in writing.',
  'No. La lista de precios muestra los precios sin IVA y no indica el tipo. Confirmamos por escrito los impuestos y los gastos de compra.',
  'Non. La liste de prix présente les prix hors TVA et n’en indique pas le taux. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Die Preisliste nennt die Preise ohne MwSt. und gibt den Satz nicht an. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе цены указаны без НДС, ставка не приведена. Мы письменно подтверждаем налоги и расходы на покупку.',
  'لا. تعرض قائمة الأسعار الأسعار دون ضريبة القيمة المضافة ولا تذكر نسبتها. ونؤكد الضرائب ومصاريف الشراء كتابةً.',
  'Nee. De prijslijst toont de prijzen exclusief btw en geeft het tarief niet. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Nie. Cennik podaje ceny bez VAT i nie wskazuje stawki. Potwierdzamy na piśmie podatki i koszty zakupu.',
  'Nei. Prislisten viser prisene uten mva. og oppgir ikke satsen. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Nej. Prislistan visar priserna utan moms och anger inte skattesatsen. Vi bekräftar skatter och köpkostnader skriftligen.')
a('Are a garage space and a storeroom included?', '¿Se incluyen una plaza de garaje y un trastero?', 'Une place de garage et un débarras sont-ils inclus ?',
  'Sind ein Garagenstellplatz und ein Abstellraum enthalten?', 'Входят ли в цену место в гараже и кладовая?', 'هل يشمل السعر موقفًا في المرآب ومخزنًا؟',
  'Zijn een garageplaats en een berging inbegrepen?', 'Czy miejsce garażowe i komórka lokatorska są wliczone w cenę?',
  'Er en garasjeplass og en bod inkludert?', 'Ingår en garageplats och ett förråd?')
a('The price list assigns each home a garage space and a storeroom but does not say whether they are in the price. We confirm it in writing.',
  'La lista de precios asigna a cada vivienda una plaza de garaje y un trastero, pero no dice si están incluidos en el precio. Lo confirmamos por escrito.',
  'La liste de prix attribue à chaque logement une place de garage et un débarras mais ne dit pas s’ils sont inclus dans le prix. Nous le confirmons par écrit.',
  'Die Preisliste ordnet jeder Wohnung einen Garagenstellplatz und einen Abstellraum zu, sagt aber nicht, ob sie im Preis enthalten sind. Wir bestätigen das schriftlich.',
  'В прайс-листе за каждой квартирой закреплены место в гараже и кладовая, но не сказано, входят ли они в цену. Мы подтверждаем это письменно.',
  'تخصص قائمة الأسعار لكل مسكن موقفًا في المرآب ومخزنًا لكنها لا تذكر ما إذا كانا مشمولين في السعر. ونؤكد ذلك كتابةً.',
  'De prijslijst wijst elke woning een garageplaats en een berging toe, maar vermeldt niet of ze in de prijs zijn inbegrepen. We bevestigen dat schriftelijk.',
  'Cennik przypisuje każdemu lokalowi miejsce garażowe i komórkę lokatorską, ale nie podaje, czy są wliczone w cenę. Potwierdzamy to na piśmie.',
  'Prislisten tildeler hver bolig en garasjeplass og en bod, men sier ikke om de er inkludert i prisen. Vi bekrefter det skriftlig.',
  'Prislistan tilldelar varje bostad en garageplats och ett förråd men anger inte om de ingår i priset. Vi bekräftar det skriftligen.')
a('The developer’s portal gives June 2028 and the brochure gives no date. We ask for the contractual date.',
  'El portal del promotor indica junio de 2028 y el folleto no da ninguna fecha. Pedimos la fecha contractual.',
  'Le portail du promoteur indique juin 2028 et la brochure ne donne aucune date. Nous demandons la date contractuelle.',
  'Das Portal des Bauträgers nennt Juni 2028, die Broschüre nennt kein Datum. Wir fragen das vertragliche Datum an.',
  'На портале застройщика указан июнь 2028 года, а в брошюре даты нет. Мы запрашиваем договорную дату.',
  'تذكر بوابة المطوّر يونيو 2028 ولا يذكر الكتيّب أي تاريخ. نطلب التاريخ التعاقدي.',
  'Het portaal van de ontwikkelaar noemt juni 2028 en de brochure noemt geen datum. We vragen naar de contractuele datum.',
  'Portal dewelopera podaje czerwiec 2028 r., a broszura nie podaje żadnej daty. Prosimy o termin wskazany w umowie.',
  'Utbyggerens portal oppgir juni 2028 og brosjyren oppgir ingen dato. Vi ber om den kontraktsfestede datoen.',
  'Exploatörens portal anger juni 2028 och broschyren anger inget datum. Vi ber om det avtalade datumet.')
a('The portal lists two schedules. For national buyers: EUR 3,000 plus VAT to reserve, then 10% plus VAT on the purchase contract, 10% plus VAT deferred and 80% plus VAT on the deed. For international buyers: EUR 6,000 plus VAT to reserve, then 20%, 10% and 70%, all plus VAT.',
  'El portal indica dos calendarios. Para compradores nacionales: {E3000} más IVA para reservar, después el 10% más IVA con el contrato de compraventa, el 10% más IVA aplazado y el 80% más IVA en la escritura. Para compradores internacionales: {E6000} más IVA para reservar, después el 20%, el 10% y el 70%, todo más IVA.',
  'Le portail indique deux échéanciers. Pour les acquéreurs nationaux : {E3000} hors TVA pour réserver, puis 10 % hors TVA au contrat de vente, 10 % hors TVA différés et 80 % hors TVA à l’acte notarié. Pour les acquéreurs internationaux : {E6000} hors TVA pour réserver, puis 20 %, 10 % et 70 %, le tout hors TVA.',
  'Das Portal nennt zwei Zahlungspläne. Für nationale Käufer: {E3000} zuzüglich MwSt. zur Reservierung, dann 10 % zuzüglich MwSt. bei Abschluss des Kaufvertrags, 10 % zuzüglich MwSt. zurückgestellt und 80 % zuzüglich MwSt. bei der notariellen Beurkundung. Für internationale Käufer: {E6000} zuzüglich MwSt. zur Reservierung, dann 20 %, 10 % und 70 %, jeweils zuzüglich MwSt.',
  'На портале указаны два графика. Для национальных покупателей: {E3000} плюс НДС для бронирования, затем 10 % плюс НДС при договоре купли-продажи, 10 % плюс НДС отсрочено и 80 % плюс НДС при нотариальном акте. Для международных покупателей: {E6000} плюс НДС для бронирования, затем 20 %, 10 % и 70 %, все суммы плюс НДС.',
  'تذكر البوابة جدولين للدفعات. للمشترين المحليين: {E3000} زائد ضريبة القيمة المضافة للحجز، ثم 10% زائد الضريبة عند عقد الشراء، و10% زائد الضريبة مؤجلة، و80% زائد الضريبة عند سند الملكية أمام كاتب العدل. للمشترين الدوليين: {E6000} زائد ضريبة القيمة المضافة للحجز، ثم 20% و10% و70%، وكلها زائد الضريبة.',
  'Het portaal vermeldt twee schema’s. Voor nationale kopers: {E3000} plus btw om te reserveren, daarna 10% plus btw bij de koopovereenkomst, 10% plus btw uitgesteld en 80% plus btw bij de notariële akte. Voor internationale kopers: {E6000} plus btw om te reserveren, daarna 20%, 10% en 70%, alles plus btw.',
  'Portal podaje dwa harmonogramy. Dla nabywców krajowych: {E3000} plus VAT na rezerwację, następnie 10% plus VAT przy umowie kupna-sprzedaży, 10% plus VAT odroczone i 80% plus VAT przy akcie notarialnym. Dla nabywców zagranicznych: {E6000} plus VAT na rezerwację, następnie 20%, 10% i 70%, wszystko plus VAT.',
  'Portalen oppgir to betalingsplaner. For nasjonale kjøpere: {E3000} pluss mva. for å reservere, deretter 10 % pluss mva. ved kjøpekontrakten, 10 % pluss mva. utsatt og 80 % pluss mva. ved skjøtet. For internasjonale kjøpere: {E6000} pluss mva. for å reservere, deretter 20 %, 10 % og 70 %, alt pluss mva.',
  'Portalen anger två betalningsplaner. För nationella köpare: {E3000} plus moms för att reservera, därefter 10 % plus moms vid köpeavtalet, 10 % plus moms uppskjutet och 80 % plus moms vid tillträdet hos notarien. För internationella köpare: {E6000} plus moms för att reservera, därefter 20 %, 10 % och 70 %, allt plus moms.')

json.dump(T, open(f'{SP}/tr_m.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
