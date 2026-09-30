# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 4: architecture, lifestyle, location, FAQ.
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Eight blocks, <em>eight levels</em>",
 "Ocho bloques, <em>ocho niveles</em>","Huit blocs, <em>huit niveaux</em>","Acht Blöcke, <em>acht Ebenen</em>",
 "Восемь корпусов, <em>восемь уровней</em>","ثمانية مبانٍ، <em>ثمانية مستويات</em>","Acht blokken, <em>acht niveaus</em>",
 "Osiem budynków, <em>osiem poziomów</em>","Åtte blokker, <em>åtte nivåer</em>","Åtta huskroppar, <em>åtta nivåer</em>")

a("The street outside the site rises and falls sharply along its length, which made it awkward to sit eight blocks along it. Rather than cut the ground flat, the architects laid a private road inside the site, three metres in and lower, that smooths the gradient to no more than four per cent from one end to the other.",
 "La calle exterior sube y baja con fuerza a lo largo de su recorrido, lo que dificultaba alinear ocho bloques junto a ella. En lugar de allanar el terreno, los arquitectos trazaron un vial privado dentro de la parcela, tres metros hacia dentro y a cota inferior, que suaviza la pendiente hasta un máximo del cuatro por ciento de un extremo a otro.",
 "La rue qui borde le terrain monte et descend fortement sur toute sa longueur, ce qui rendait malaisé l'alignement de huit blocs. Plutôt que d'aplanir le sol, les architectes ont tracé une voie privée à l'intérieur de la parcelle, trois mètres en retrait et plus bas, qui ramène la pente à quatre pour cent au maximum d'un bout à l'autre.",
 "Die Straße vor dem Grundstück steigt und fällt auf ihrer Länge stark, was es schwierig machte, acht Blöcke daran zu reihen. Statt das Gelände abzutragen, legten die Architekten eine private Straße im Grundstück an, drei Meter zurückgesetzt und tiefer, die das Gefälle von einem Ende zum anderen auf höchstens vier Prozent glättet.",
 "Улица вдоль участка резко поднимается и опускается по всей длине, из-за чего выстроить вдоль неё восемь корпусов было неудобно. Вместо того чтобы срезать грунт, архитекторы проложили внутри участка частную дорогу — на три метра вглубь и ниже, — которая сглаживает уклон до не более четырёх процентов от края до края.",
 "الشارع المحاذي للموقع يرتفع وينخفض بحدّة على امتداده، ما جعل اصطفاف ثمانية مبانٍ عليه صعباً. وبدل تسوية الأرض، رسم المعماريون طريقاً خاصاً داخل الموقع، على بعد ثلاثة أمتار وبمنسوب أدنى، يخفّف الانحدار إلى أربعة بالمئة كحدّ أقصى من طرف إلى آخر.",
 "De straat langs het terrein stijgt en daalt scherp over haar lengte, waardoor acht blokken er moeilijk langs te zetten waren. In plaats van de grond vlak af te graven legden de architecten een private weg binnen het terrein aan, drie meter naar binnen en lager, die het verhang van het ene eind tot het andere afvlakt tot hoogstens vier procent.",
 "Ulica biegnąca wzdłuż działki mocno wznosi się i opada na całej długości, co utrudniało ustawienie przy niej ośmiu budynków. Zamiast wyrównywać teren, architekci poprowadzili wewnątrz działki drogę prywatną, trzy metry w głąb i niżej, która łagodzi spadek do najwyżej czterech procent od jednego końca do drugiego.",
 "Gaten utenfor tomta stiger og faller kraftig i hele sin lengde, noe som gjorde det tungvint å legge åtte blokker langs den. I stedet for å sprenge terrenget flatt la arkitektene en privat vei inne på tomta, tre meter inn og lavere, som jevner stigningen til høyst fire prosent fra ende til ende.",
 "Gatan utanför tomten stiger och faller kraftigt längs hela sin sträckning, vilket gjorde det besvärligt att ställa åtta huskroppar längs den. I stället för att schakta marken plan drog arkitekterna en privat väg inne på tomten, tre meter in och lägre, som jämnar ut lutningen till som mest fyra procent från ände till ände.")

a("Every block then sits at its own height off that road. The southernmost is lowest and they climb northwards, each one standing above the one below it. Nothing on the site needs a ramp to be reached, and no home looks into its neighbour's roof.",
 "Cada bloque se asienta entonces a su propia cota respecto de ese vial. El más meridional es el más bajo y ascienden hacia el norte, cada uno por encima del anterior. Nada en la parcela necesita rampa para ser accesible, y ninguna vivienda mira al tejado de la vecina.",
 "Chaque bloc s'installe alors à sa propre hauteur par rapport à cette voie. Le plus au sud est le plus bas et ils montent vers le nord, chacun dominant le précédent. Rien sur le terrain n'exige de rampe pour être atteint, et aucun logement ne donne sur le toit du voisin.",
 "Jeder Block sitzt dann auf seiner eigenen Höhe zu dieser Straße. Der südlichste liegt am tiefsten, und sie steigen nach Norden an, jeder über dem darunterliegenden. Nichts auf dem Gelände braucht eine Rampe, um erreicht zu werden, und keine Wohnung blickt auf das Dach der Nachbarwohnung.",
 "Каждый корпус затем стоит на своей высоте относительно этой дороги. Самый южный — ниже всех, и далее они поднимаются к северу, каждый над предыдущим. Ни к чему на участке не нужен пандус, и ни одна квартира не смотрит на крышу соседней.",
 "ثم يقوم كل مبنى على منسوبه الخاص بالنسبة إلى ذلك الطريق. أقصى المباني جنوباً هو الأدنى، ثم تتصاعد شمالاً، كل واحد فوق الذي تحته. لا شيء في الموقع يحتاج منحدراً للوصول إليه، ولا يطلّ أي مسكن على سطح جاره.",
 "Elk blok ligt vervolgens op zijn eigen hoogte ten opzichte van die weg. Het zuidelijkste ligt het laagst en ze klimmen naar het noorden, elk boven het voorgaande. Niets op het terrein heeft een hellingbaan nodig om bereikt te worden, en geen woning kijkt uit op het dak van de buren.",
 "Każdy budynek stoi następnie na własnym poziomie względem tej drogi. Najbardziej wysunięty na południe jest najniżej, a kolejne wznoszą się ku północy, każdy ponad poprzednim. Nic na działce nie wymaga pochylni, aby było dostępne, i żadne mieszkanie nie patrzy na dach sąsiada.",
 "Hver blokk ligger så på sin egen høyde i forhold til den veien. Den sørligste ligger lavest, og de stiger nordover, hver over den under. Ingenting på tomta krever rampe for å nås, og ingen bolig ser inn på taket til naboen.",
 "Varje huskropp ligger sedan på sin egen höjd i förhållande till den vägen. Den sydligaste ligger lägst och de stiger norrut, var och en ovanför den under. Ingenting på tomten kräver ramp för att nås, och ingen bostad tittar in i grannens tak.")

a("Eight blocks of ten homes, ground floor plus two and a tower level.",
 "Ocho bloques de diez viviendas, planta baja más dos y torreón.",
 "Huit blocs de dix logements, rez-de-chaussée plus deux niveaux et un attique.",
 "Acht Blöcke mit je zehn Wohnungen, Erdgeschoss plus zwei Etagen und Turmgeschoss.",
 "Восемь корпусов по десять квартир: первый этаж плюс два и мансардный уровень.",
 "ثمانية مبانٍ من عشرة مساكن لكل منها، طابق أرضي وطابقان وطابق علوي.",
 "Acht blokken van tien woningen, begane grond plus twee en een torenlaag.",
 "Osiem budynków po dziesięć mieszkań, parter plus dwie kondygnacje i poziom wieżyczki.",
 "Åtte blokker med ti boliger hver, første etasje pluss to og et tårnplan.",
 "Åtta huskroppar med tio bostäder vardera, bottenvåning plus två och ett tornplan.")

a("Blocks set back at least three metres, on a private internal road under a four per cent gradient.",
 "Bloques retranqueados al menos tres metros, sobre un vial interior privado con pendiente inferior al cuatro por ciento.",
 "Blocs implantés à au moins trois mètres de retrait, le long d'une voie interne privée à moins de quatre pour cent de pente.",
 "Blöcke mindestens drei Meter zurückgesetzt, an einer privaten inneren Straße mit weniger als vier Prozent Gefälle.",
 "Корпуса отступают не менее чем на три метра и стоят вдоль частной внутренней дороги с уклоном менее четырёх процентов.",
 "المباني مرتدّة ثلاثة أمتار على الأقل، على طريق داخلي خاص بانحدار دون أربعة بالمئة.",
 "Blokken minstens drie meter teruggelegd, aan een private interne weg met minder dan vier procent verhang.",
 "Budynki cofnięte o co najmniej trzy metry, przy prywatnej drodze wewnętrznej o spadku poniżej czterech procent.",
 "Blokkene trukket minst tre meter tilbake, langs en privat intern vei med under fire prosent stigning.",
 "Huskropparna indragna minst tre meter, längs en privat intern väg med under fyra procents lutning.")

a("One basement runs under the whole site for parking, storerooms and plant, with two separate entrances.",
 "Un único sótano recorre toda la parcela con garaje, trasteros e instalaciones, y dos accesos independientes.",
 "Un unique sous-sol court sous tout le terrain pour le parking, les débarras et les locaux techniques, avec deux accès distincts.",
 "Ein einziges Untergeschoss zieht sich unter dem gesamten Grundstück hin, für Parken, Abstellräume und Technik, mit zwei getrennten Zufahrten.",
 "Единый подземный уровень проходит под всем участком: парковка, кладовые и техпомещения, с двумя отдельными въездами.",
 "قبو واحد يمتدّ تحت الموقع بأكمله للمواقف والمخازن والتجهيزات، بمدخلين منفصلين.",
 "Eén kelderlaag loopt onder het hele terrein door voor parkeren, bergingen en techniek, met twee gescheiden toegangen.",
 "Jedna kondygnacja podziemna biegnie pod całą działką: parking, komórki i pomieszczenia techniczne, z dwoma osobnymi wjazdami.",
 "Én kjelleretasje går under hele tomta til parkering, boder og tekniske rom, med to atskilte innkjørsler.",
 "Ett enda källarplan löper under hela tomten för parkering, förråd och teknik, med två separata infarter.")

a("Mediterranean elevations in warm stone tones, with deep terraces cut into the mass.",
 "Alzados mediterráneos en tonos cálidos de piedra, con terrazas profundas recortadas en el volumen.",
 "Façades méditerranéennes dans des tons de pierre chauds, avec de profondes terrasses creusées dans le volume.",
 "Mediterrane Fassaden in warmen Steintönen, mit tiefen, aus dem Baukörper geschnittenen Terrassen.",
 "Средиземноморские фасады в тёплых каменных тонах с глубокими террасами, вырезанными в объёме.",
 "واجهات متوسطية بدرجات حجرية دافئة، وتراسات عميقة محفورة في الكتلة.",
 "Mediterrane gevels in warme steentinten, met diepe terrassen uit de bouwmassa gesneden.",
 "Śródziemnomorskie elewacje w ciepłych kamiennych tonach, z głębokimi tarasami wyciętymi w bryle.",
 "Middelhavsfasader i varme steintoner, med dype terrasser skåret inn i bygningskroppen.",
 "Medelhavsfasader i varma stentoner, med djupa terrasser inskurna i byggnadskroppen.")

a("A whole floor given to <em>the residents</em>",
 "Una planta entera para <em>los residentes</em>","Un étage entier pour <em>les résidents</em>",
 "Eine ganze Ebene für <em>die Bewohner</em>","Целый этаж отдан <em>жителям</em>",
 "طابق كامل مخصّص <em>للسكان</em>","Een hele verdieping voor <em>de bewoners</em>",
 "Całe piętro dla <em>mieszkańców</em>","En hel etasje til <em>beboerne</em>","Ett helt plan åt <em>de boende</em>")

a("An infinity pool and pool bar outside, and a heated lap pool, spa, gym, lounge and coworking room inside.",
 "Piscina infinita y bar de piscina en el exterior, y piscina de nado climatizada, spa, gimnasio, salón y sala de coworking en el interior.",
 "Une piscine à débordement et un bar de piscine à l'extérieur, un bassin de nage chauffé, un spa, une salle de sport, un salon et un espace de coworking à l'intérieur.",
 "Draußen ein Infinity-Pool und eine Poolbar, drinnen ein beheizter Schwimmkanal, Spa, Fitnessraum, Lounge und Coworking-Bereich.",
 "Снаружи бассейн-инфинити и бар у бассейна, внутри подогреваемый бассейн для плавания, спа, спортзал, лаунж и коворкинг.",
 "مسبح لا متناهٍ وبار مسبح في الخارج، ومسبح سباحة مُدفأ وسبا وصالة رياضة وصالة جلوس وغرفة عمل مشترك في الداخل.",
 "Buiten een infinityzwembad en poolbar, binnen een verwarmd baanzwembad, spa, fitnessruimte, lounge en coworkingruimte.",
 "Na zewnątrz basen infinity i bar przy basenie, w środku podgrzewany basen pływacki, spa, siłownia, salon i sala coworkingowa.",
 "Ute et infinity-basseng og en poolbar, inne et oppvarmet svømmebasseng, spa, treningsrom, lounge og coworking-rom.",
 "Ute en infinitypool och poolbar, inne en uppvärmd simbassäng, spa, gym, lounge och coworkingrum.")

a("Nueva Living arranges the appointment, walks the site with you and asks the questions that are awkward to ask a seller yourself.",
 "Nueva Living concierta la cita, recorre la promoción con usted y hace las preguntas que resultan incómodas de plantear uno mismo al vendedor.",
 "Nueva Living organise le rendez-vous, parcourt le site avec vous et pose les questions qu'il est délicat d'adresser soi-même au vendeur.",
 "Nueva Living vereinbart den Termin, geht das Gelände mit Ihnen ab und stellt die Fragen, die man einem Verkäufer selbst ungern stellt.",
 "Nueva Living назначает встречу, обходит площадку вместе с вами и задаёт вопросы, которые неловко задавать продавцу самому.",
 "تنسّق Nueva Living الموعد، وتتجوّل في الموقع معك، وتطرح الأسئلة التي يصعب توجيهها إلى البائع بنفسك.",
 "Nueva Living maakt de afspraak, loopt het terrein met u door en stelt de vragen die u zelf lastig aan een verkoper stelt.",
 "Nueva Living umawia spotkanie, obchodzi z Państwem teren i zadaje pytania, które trudno zadać sprzedającemu samemu.",
 "Nueva Living avtaler visningen, går over tomta sammen med deg og stiller spørsmålene det er ubehagelig å stille selgeren selv.",
 "Nueva Living bokar mötet, går platsen tillsammans med er och ställer de frågor som är obekväma att ställa säljaren själv.")

a("Which blocks are already sold out, and what that says about the views buyers are choosing.",
 "Qué bloques ya están vendidos y qué dice eso sobre las vistas que eligen los compradores.",
 "Quels blocs sont déjà vendus, et ce que cela révèle des vues que choisissent les acheteurs.",
 "Welche Blöcke bereits ausverkauft sind und was das über die Aussichten sagt, für die sich Käufer entscheiden.",
 "Какие корпуса уже распроданы и что это говорит о видах, которые выбирают покупатели.",
 "أي المباني بيعت بالكامل، وما يقوله ذلك عن الإطلالات التي يختارها المشترون.",
 "Welke blokken al uitverkocht zijn, en wat dat zegt over de uitzichten die kopers kiezen.",
 "Które budynki są już wyprzedane i co to mówi o widokach wybieranych przez nabywców.",
 "Hvilke blokker som allerede er utsolgt, og hva det sier om utsikten kjøperne velger.",
 "Vilka huskroppar som redan är slutsålda, och vad det säger om de utsikter köparna väljer.")

a("How the step between blocks reads on the ground rather than on the drawing.",
 "Cómo se percibe sobre el terreno el escalón entre bloques, y no solo en el plano.",
 "Comment le décrochement entre les blocs se lit sur le terrain plutôt que sur le plan.",
 "Wie sich der Versatz zwischen den Blöcken vor Ort und nicht nur auf dem Plan darstellt.",
 "Как перепад между корпусами читается на местности, а не на чертеже.",
 "كيف يبدو الفارق بين المباني على أرض الواقع لا على المخطط.",
 "Hoe het hoogteverschil tussen de blokken op het terrein overkomt in plaats van op de tekening.",
 "Jak uskok między budynkami odczytuje się w terenie, a nie na rysunku.",
 "Hvordan trinnet mellom blokkene leses på stedet snarere enn på tegningen.",
 "Hur steget mellan huskropparna läses på plats snarare än på ritningen.")

a("Whether the delivery date is contractual or indicative, in writing.",
 "Si la fecha de entrega es contractual o meramente orientativa, por escrito.",
 "Si la date de livraison est contractuelle ou simplement indicative, par écrit.",
 "Ob der Übergabetermin vertraglich bindend oder nur indikativ ist, schriftlich.",
 "Является ли дата передачи договорной или лишь ориентировочной — в письменном виде.",
 "هل تاريخ التسليم تعاقدي أم إرشادي فقط، كتابةً.",
 "Of de opleverdatum contractueel of slechts indicatief is, schriftelijk.",
 "Czy data odbioru jest umowna, czy tylko orientacyjna — na piśmie.",
 "Om overtakelsesdatoen er kontraktfestet eller bare veiledende, skriftlig.",
 "Om tillträdesdatumet är avtalat eller endast vägledande, skriftligt.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
