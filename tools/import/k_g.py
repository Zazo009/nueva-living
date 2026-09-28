# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Developer visual of the blocks stepped into the wooded hillside around the pool terrace",
 "Imagen del promotor de los bloques escalonados en la ladera arbolada alrededor de la terraza de la piscina",
 "Visuel du promoteur des immeubles étagés sur le coteau boisé autour de la terrasse de la piscine",
 "Bauträger-Visualisierung der gestaffelten Gebäude am bewaldeten Hang rund um die Poolterrasse",
 "Визуализация застройщика: корпуса уступами на лесистом склоне вокруг террасы бассейна",
 "تصور من المطور للمباني المتدرجة على المنحدر المشجّر حول تراس المسبح",
 "Beeld van de ontwikkelaar van de getrapte gebouwen op de beboste helling rond het zwembadterras",
 "Wizualizacja dewelopera przedstawiająca tarasowo ustawione budynki na zalesionym zboczu wokół tarasu basenowego",
 "Visualisering fra utbygger av de trappede byggene i den skogkledde skråningen rundt bassengterrassen",
 "Visualisering från utvecklaren av de trappade husen i den skogbevuxna sluttningen runt pooldäcket")
a("The scheme from above","La promoción desde el aire","Le programme vu d'en haut","Die Anlage von oben",
 "Комплекс сверху","المشروع من الأعلى","Het project van bovenaf","Inwestycja z góry","Prosjektet ovenfra","Projektet uppifrån")
a("Developer visual of the lagoon-shaped pool and solarium with the sea beyond",
 "Imagen del promotor de la piscina tipo laguna y el solárium con el mar al fondo",
 "Visuel du promoteur de la piscine en forme de lagune et du solarium avec la mer au fond",
 "Bauträger-Visualisierung des lagunenförmigen Pools und der Sonnenterrasse mit dem Meer dahinter",
 "Визуализация застройщика: бассейн в форме лагуны и солярий, а за ними море",
 "تصور من المطور للمسبح على شكل بحيرة والمصطبة الشمسية والبحر في الخلفية",
 "Beeld van de ontwikkelaar van het lagunevormige zwembad en het solarium met de zee erachter",
 "Wizualizacja dewelopera przedstawiająca basen w kształcie laguny i solarium z morzem w tle",
 "Visualisering fra utbygger av det laguneformede bassenget og solterrassen med havet bak",
 "Visualisering från utvecklaren av den lagunformade poolen och solterrassen med havet bakom")
a("The pool from above","La piscina desde el aire","La piscine vue d'en haut","Der Pool von oben",
 "Бассейн сверху","المسبح من الأعلى","Het zwembad van bovenaf","Basen z góry","Bassenget ovenfra","Poolen uppifrån")
a("Developer visual of the pool under palms, looking out over the hills to the sea",
 "Imagen del promotor de la piscina bajo las palmeras, con vistas sobre las colinas hasta el mar",
 "Visuel du promoteur de la piscine sous les palmiers, avec vue sur les collines jusqu'à la mer",
 "Bauträger-Visualisierung des Pools unter Palmen mit Blick über die Hügel zum Meer",
 "Визуализация застройщика: бассейн под пальмами с видом через холмы на море",
 "تصور من المطور للمسبح تحت النخيل مع إطلالة فوق التلال إلى البحر",
 "Beeld van de ontwikkelaar van het zwembad onder palmen, met uitzicht over de heuvels naar de zee",
 "Wizualizacja dewelopera przedstawiająca basen pod palmami z widokiem przez wzgórza na morze",
 "Visualisering fra utbygger av bassenget under palmer, med utsikt over åsene mot havet",
 "Visualisering från utvecklaren av poolen under palmerna, med utsikt över kullarna mot havet")
a("The pool and the view","La piscina y las vistas","La piscine et la vue","Der Pool und die Aussicht",
 "Бассейн и вид","المسبح والإطلالة","Het zwembad en het uitzicht","Basen i widok","Bassenget og utsikten","Poolen och utsikten")
a("Developer visual of the blocks above the pool terrace in the evening light",
 "Imagen del promotor de los bloques sobre la terraza de la piscina con la luz del atardecer",
 "Visuel du promoteur des immeubles au-dessus de la terrasse de la piscine dans la lumière du soir",
 "Bauträger-Visualisierung der Gebäude über der Poolterrasse im Abendlicht",
 "Визуализация застройщика: корпуса над террасой бассейна в вечернем свете",
 "تصور من المطور للمباني فوق تراس المسبح في ضوء المساء",
 "Beeld van de ontwikkelaar van de gebouwen boven het zwembadterras in het avondlicht",
 "Wizualizacja dewelopera przedstawiająca budynki nad tarasem basenowym w wieczornym świetle",
 "Visualisering fra utbygger av byggene over bassengterrassen i kveldslyset",
 "Visualisering från utvecklaren av husen ovanför pooldäcket i kvällsljuset")
a("Developer visual of the beach padel court between the blocks, in use",
 "Imagen del promotor de la pista de pádel playa entre los bloques, en uso",
 "Visuel du promoteur du terrain de beach padel entre les immeubles, en cours de partie",
 "Bauträger-Visualisierung des Beach-Padel-Platzes zwischen den Gebäuden, im Spiel",
 "Визуализация застройщика: корт для пляжного паделя между корпусами во время игры",
 "تصور من المطور لملعب البادل الشاطئي بين المباني أثناء اللعب",
 "Beeld van de ontwikkelaar van de beachpadelbaan tussen de gebouwen, in gebruik",
 "Wizualizacja dewelopera przedstawiająca kort do padla plażowego między budynkami, w trakcie gry",
 "Visualisering fra utbygger av beachpadelbanen mellom byggene, i bruk",
 "Visualisering från utvecklaren av beachpadelbanan mellan husen, under spel")
a("The padel court","La pista de pádel","Le terrain de padel","Der Padel-Platz","Корт для паделя",
 "ملعب البادل","De padelbaan","Kort do padla","Padelbanen","Padelbanan")
a("Developer visual of the events room, its long tables open to the terrace",
 "Imagen del promotor de la sala de eventos, con sus mesas largas abiertas a la terraza",
 "Visuel du promoteur de la salle de réception, ses longues tables ouvertes sur la terrasse",
 "Bauträger-Visualisierung des Veranstaltungsraums mit seinen langen Tischen zur Terrasse hin",
 "Визуализация застройщика: зал для мероприятий с длинными столами, открытый на террасу",
 "تصور من المطور لقاعة المناسبات بطاولاتها الطويلة المفتوحة على التراس",
 "Beeld van de ontwikkelaar van de evenementenruimte, met lange tafels open naar het terras",
 "Wizualizacja dewelopera przedstawiająca salę eventową z długimi stołami otwartą na taras",
 "Visualisering fra utbygger av selskapsrommet, med lange bord åpne mot terrassen",
 "Visualisering från utvecklaren av festlokalen, med långbord öppna mot terrassen")
a("The events room","La sala de eventos","La salle de réception","Der Veranstaltungsraum","Зал для мероприятий",
 "قاعة المناسبات","De evenementenruimte","Sala eventowa","Selskapsrommet","Festlokalen")
a("Developer visual of the gym under a timber ceiling, running machines facing the glass",
 "Imagen del promotor del gimnasio bajo un techo de madera, con las cintas de correr frente al cristal",
 "Visuel du promoteur de la salle de sport sous un plafond en bois, les tapis de course face à la baie vitrée",
 "Bauträger-Visualisierung des Fitnessraums unter einer Holzdecke, die Laufbänder zur Glasfront",
 "Визуализация застройщика: тренажёрный зал под деревянным потолком, беговые дорожки у стекла",
 "تصور من المطور لصالة الرياضة تحت سقف خشبي، مع أجهزة الجري أمام الزجاج",
 "Beeld van de ontwikkelaar van de fitnessruimte onder een houten plafond, loopbanden naar het glas",
 "Wizualizacja dewelopera przedstawiająca siłownię pod drewnianym sufitem, bieżnie zwrócone ku szybie",
 "Visualisering fra utbygger av treningsrommet under et tretak, med tredemøllene mot glasset",
 "Visualisering från utvecklaren av gymmet under ett trätak, med löpbanden mot glaset")
a("Developer visual of the coworking room, a long table and a counter at the window",
 "Imagen del promotor de la sala de coworking, con una mesa larga y una barra junto a la ventana",
 "Visuel du promoteur de l'espace de coworking, une longue table et un comptoir près de la fenêtre",
 "Bauträger-Visualisierung des Coworking-Raums mit langem Tisch und Tresen am Fenster",
 "Визуализация застройщика: коворкинг с длинным столом и стойкой у окна",
 "تصور من المطور لغرفة العمل المشترك بطاولة طويلة ومنضدة عند النافذة",
 "Beeld van de ontwikkelaar van de coworkingruimte, met een lange tafel en een balie bij het raam",
 "Wizualizacja dewelopera przedstawiająca salę coworkingową z długim stołem i ladą przy oknie",
 "Visualisering fra utbygger av coworking-rommet, med et langbord og en benk ved vinduet",
 "Visualisering från utvecklaren av coworking-rummet, med ett långbord och en bardisk vid fönstret")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
