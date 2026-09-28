# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("The houses are under construction and the show house is finished and furnished, but the developer publishes no completion date in its dossier, its specification or its availability system. Nueva Living asks for the date in writing and puts it in the contract rather than quoting one.",
 "Las viviendas están en obra y la casa piloto está terminada y amueblada, pero la promotora no publica fecha de entrega ni en su dossier, ni en su memoria de calidades, ni en su sistema de disponibilidad. Nueva Living pide la fecha por escrito y la lleva al contrato en lugar de citar ninguna.",
 "Les maisons sont en chantier et la maison témoin est achevée et meublée, mais le promoteur ne publie aucune date de livraison, ni dans son dossier, ni dans son descriptif, ni dans son système de disponibilité. Nueva Living demande la date par écrit et l’inscrit au contrat plutôt que d’en avancer une.",
 "Die Häuser sind im Bau und das Musterhaus ist fertig und möbliert, doch der Bauträger veröffentlicht weder im Exposé noch in der Baubeschreibung noch in seinem Verfügbarkeitssystem ein Fertigstellungsdatum. Nueva Living lässt sich das Datum schriftlich geben und nimmt es in den Vertrag auf, statt eines zu nennen.",
 "Дома строятся, шоу-хаус завершён и меблирован, но застройщик не публикует дату сдачи ни в буклете, ни в спецификации, ни в своей системе наличия. Nueva Living запрашивает её письменно и вносит в договор, а не называет сама.",
 "المنازل قيد الإنشاء والمنزل النموذجي مكتمل ومفروش، لكن الشركة المطوّرة لا تنشر تاريخ تسليم في كتيّبها ولا في مواصفاتها ولا في نظام التوافر لديها. تطلب Nueva Living التاريخ كتابةً وتدرجه في العقد بدل ذكر تاريخ من عندها.",
 "De huizen zijn in aanbouw en de modelwoning is af en gemeubileerd, maar de ontwikkelaar publiceert geen opleverdatum, niet in het dossier, niet in de bouwbeschrijving en niet in het beschikbaarheidssysteem. Nueva Living vraagt de datum schriftelijk op en legt die vast in het contract in plaats van er een te noemen.",
 "Domy są w budowie, a dom pokazowy jest ukończony i umeblowany, ale deweloper nie podaje daty odbioru ani w broszurze, ani w standardzie wykończenia, ani w swoim systemie dostępności. Nueva Living prosi o datę na piśmie i wpisuje ją do umowy, zamiast podawać własną.",
 "Husene er under bygging og visningshuset er ferdig og møblert, men utbygger publiserer ingen ferdigstillelsesdato i dossieret, beskrivelsen eller tilgjengelighetssystemet. Nueva Living ber om datoen skriftlig og tar den inn i kontrakten i stedet for å oppgi en.",
 "Husen är under byggnation och visningshuset är färdigt och möblerat, men byggherren publicerar inget färdigställandedatum i broschyren, beskrivningen eller tillgänglighetssystemet. Nueva Living begär datumet skriftligt och för in det i avtalet i stället för att ange ett.")

a("Thirty-six townhouses on a hillside at El Higuerón, thirteen still available, each with its own rooftop pool.",
 "Treinta y seis adosados en una ladera de El Higuerón, trece todavía disponibles, cada uno con su piscina en la azotea.",
 "Trente-six maisons de ville sur un coteau d’El Higuerón, treize encore disponibles, chacune avec sa piscine en toiture.",
 "Sechsunddreißig Reihenhäuser an einem Hang in El Higuerón, dreizehn noch verfügbar, jedes mit eigenem Dachpool.",
 "Тридцать шесть таунхаусов на склоне в Эль-Игероне, тринадцать ещё доступны, у каждого свой бассейн на крыше.",
 "ستة وثلاثون منزلاً متلاصقاً على منحدر في إل إيغيرون، ثلاثة عشر منها ما زالت متاحة، ولكل منها مسبحه على السطح.",
 "Zesendertig herenhuizen op een helling in El Higuerón, dertien nog beschikbaar, elk met een eigen dakzwembad.",
 "Trzydzieści sześć domów szeregowych na zboczu w El Higuerón, trzynaście wciąż dostępnych, każdy z własnym basenem na dachu.",
 "Trettiseks rekkehus i en skråning i El Higuerón, tretten fortsatt ledige, hvert med eget takbasseng.",
 "Trettiosex radhus i en sluttning i El Higuerón, tretton fortfarande lediga, vart och ett med egen takpool.")

a("Buyers who want a house with a pool and a garden but not the upkeep of a detached villa, within a few minutes of the beach and the train.",
 "Compradores que quieren una casa con piscina y jardín pero sin el mantenimiento de una villa independiente, a pocos minutos de la playa y del tren.",
 "Des acquéreurs qui veulent une maison avec piscine et jardin sans l’entretien d’une villa individuelle, à quelques minutes de la plage et du train.",
 "Käufer, die ein Haus mit Pool und Garten wollen, aber nicht den Unterhalt einer freistehenden Villa, wenige Minuten von Strand und Bahn entfernt.",
 "Покупателей, которым нужен дом с бассейном и садом, но без забот об отдельной вилле, в нескольких минутах от пляжа и поезда.",
 "المشترين الذين يريدون منزلاً بمسبح وحديقة دون أعباء صيانة فيلا مستقلة، على بُعد دقائق من الشاطئ والقطار.",
 "Kopers die een huis met zwembad en tuin willen maar niet het onderhoud van een vrijstaande villa, op een paar minuten van het strand en de trein.",
 "Kupujących, którzy chcą domu z basenem i ogrodem, ale bez utrzymania wolnostojącej willi, kilka minut od plaży i pociągu.",
 "Kjøpere som vil ha et hus med basseng og hage, men ikke vedlikeholdet av en frittliggende villa, noen minutter fra stranda og toget.",
 "Köpare som vill ha ett hus med pool och trädgård men inte underhållet av en fristående villa, några minuter från stranden och tåget.")

a("A private pool on the roof of every house, which almost no townhouse scheme on this coast offers.",
 "Piscina privada en la azotea de todas las viviendas, algo que casi ninguna promoción de adosados de esta costa ofrece.",
 "Une piscine privative sur le toit de chaque maison, ce que presque aucun programme de maisons de ville de cette côte ne propose.",
 "Ein eigener Pool auf dem Dach jedes Hauses, was fast keine Reihenhausanlage an dieser Küste bietet.",
 "Собственный бассейн на крыше каждого дома — то, чего почти нет ни в одном таунхаус-проекте на этом побережье.",
 "مسبح خاص على سطح كل منزل، وهو ما لا يكاد يوفّره أي مشروع منازل متلاصقة على هذا الساحل.",
 "Een eigen zwembad op het dak van elk huis, wat vrijwel geen enkel herenhuisproject aan deze kust biedt.",
 "Prywatny basen na dachu każdego domu, czego nie oferuje niemal żadna inwestycja szeregowa na tym wybrzeżu.",
 "Eget basseng på taket av hvert hus, noe nesten ingen rekkehusprosjekter på denne kysten tilbyr.",
 "Egen pool på taket av varje hus, vilket nästan inget radhusprojekt på den här kusten erbjuder.")

a("The Carvajal train station and two beaches are under five minutes away, and Málaga airport about twenty.",
 "La estación de Cercanías de Carvajal y dos playas quedan a menos de cinco minutos, y el aeropuerto de Málaga a unos veinte.",
 "La gare de Carvajal et deux plages sont à moins de cinq minutes, et l’aéroport de Málaga à une vingtaine.",
 "Der Bahnhof Carvajal und zwei Strände liegen unter fünf Minuten entfernt, der Flughafen Málaga etwa zwanzig.",
 "Станция Карвахаль и два пляжа — меньше чем в пяти минутах, аэропорт Малаги — примерно в двадцати.",
 "محطة قطار كارباخال وشاطئان على بُعد أقل من خمس دقائق، ومطار مالقة على نحو عشرين دقيقة.",
 "Het treinstation Carvajal en twee stranden liggen op minder dan vijf minuten, en de luchthaven van Málaga op ongeveer twintig.",
 "Stacja kolejowa Carvajal i dwie plaże są niecałe pięć minut stąd, a lotnisko w Maladze około dwudziestu.",
 "Togstasjonen Carvajal og to strender ligger under fem minutter unna, og Málaga lufthavn rundt tjue.",
 "Tågstationen Carvajal och två stränder ligger under fem minuter bort, och Málaga flygplats ungefär tjugo.")

a("An <em>El Higuerón address</em>","Una <em>dirección en El Higuerón</em>","Une <em>adresse à El Higuerón</em>","Eine <em>Adresse in El Higuerón</em>",
 "Адрес <em>в Эль-Игероне</em>","عنوان <em>في إل إيغيرون</em>","Een <em>adres in El Higuerón</em>","Adres <em>w El Higuerón</em>","En <em>adresse i El Higuerón</em>","En <em>adress i El Higuerón</em>")

a("Twenty-three of the thirty-six are already gone, and only two of the nine three-bedroom houses remain.",
 "Veintitrés de las treinta y seis ya están colocadas, y de las nueve de tres dormitorios solo quedan dos.",
 "Vingt-trois des trente-six sont déjà parties, et il ne reste que deux des neuf maisons de trois chambres.",
 "Dreiundzwanzig der sechsunddreißig sind bereits weg, und von den neun Dreizimmerhäusern sind nur zwei übrig.",
 "Двадцать три из тридцати шести уже ушли, а из девяти домов с тремя спальнями осталось только два.",
 "ثلاثة وعشرون من الستة والثلاثين نفدت بالفعل، ولم يبقَ من المنازل التسعة بثلاث غرف نوم سوى اثنين.",
 "Drieëntwintig van de zesendertig zijn al weg, en van de negen huizen met drie slaapkamers zijn er nog twee.",
 "Dwadzieścia trzy z trzydziestu sześciu już odeszły, a z dziewięciu domów trzypokojowych zostały dwa.",
 "Tjuetre av de trettiseks er allerede borte, og bare to av de ni treromshusene står igjen.",
 "Tjugotre av de trettiosex är redan borta, och bara två av de nio trerumshusen återstår.")

a("El Higuerón is one of the few hillside positions on this stretch with a train station at the bottom of it, which supports demand year round.",
 "El Higuerón es una de las pocas posiciones en ladera de este tramo con una estación de tren al pie, lo que sostiene la demanda todo el año.",
 "El Higuerón est l’une des rares positions de coteau de cette portion de côte avec une gare à son pied, ce qui soutient la demande toute l’année.",
 "El Higuerón ist eine der wenigen Hanglagen an diesem Abschnitt mit einem Bahnhof am Fuß, was die Nachfrage das ganze Jahr stützt.",
 "Эль-Игерон — одна из немногих склоновых позиций на этом отрезке, у подножия которой есть железнодорожная станция, что поддерживает спрос круглый год.",
 "إل إيغيرون من المواقع القليلة على المنحدرات في هذا الامتداد التي تقع محطة قطار عند سفحها، ما يدعم الطلب طوال العام.",
 "El Higuerón is een van de weinige hellingposities op dit stuk kust met een treinstation aan de voet, wat de vraag het hele jaar ondersteunt.",
 "El Higuerón to jedna z niewielu lokalizacji zboczowych na tym odcinku ze stacją kolejową u podnóża, co podtrzymuje popyt przez cały rok.",
 "El Higuerón er en av få skråningsbeliggenheter på denne strekningen med togstasjon ved foten, noe som holder etterspørselen oppe hele året.",
 "El Higuerón är ett av få sluttningslägen på den här sträckan med en tågstation vid foten, vilket håller efterfrågan uppe året om.")

a("Which house is which","Qué vivienda es cuál","Quelle maison est laquelle","Welches Haus welches ist","Какой дом какой","أي منزل هو أي","Welk huis welk is","Który dom jest który","Hvilket hus som er hvilket","Vilket hus som är vilket")

a("That the house number, the orientation and the areas on the contract match both the availability system and the floorplan.",
 "Que el número de vivienda, la orientación y las superficies del contrato coinciden tanto con el sistema de disponibilidad como con el plano.",
 "Que le numéro de maison, l’orientation et les surfaces du contrat correspondent à la fois au système de disponibilité et au plan.",
 "Dass Hausnummer, Ausrichtung und Flächen im Vertrag sowohl mit dem Verfügbarkeitssystem als auch mit dem Plan übereinstimmen.",
 "Что номер дома, ориентация и площади в договоре совпадают и с системой наличия, и с планировкой.",
 "أنّ رقم المنزل والاتجاه والمساحات في العقد تطابق نظام التوافر والمخطط معاً.",
 "Dat het huisnummer, de oriëntatie en de oppervlakten in het contract overeenkomen met zowel het beschikbaarheidssysteem als de plattegrond.",
 "Czy numer domu, orientacja i powierzchnie w umowie zgadzają się zarówno z systemem dostępności, jak i z rzutem.",
 "At husnummeret, himmelretningen og arealene i kontrakten stemmer med både tilgjengelighetssystemet og planløsningen.",
 "Att husnumret, väderstrecket och ytorna i avtalet stämmer med både tillgänglighetssystemet och ritningen.")

a("Stone, stepped <em>down the hill</em>","Piedra, escalonada <em>por la ladera</em>","La pierre, en gradins <em>sur le coteau</em>","Stein, gestaffelt <em>den Hang hinab</em>",
 "Камень, уступами <em>по склону</em>","الحجر متدرّجاً <em>على المنحدر</em>","Steen, getrapt <em>de helling af</em>","Kamień, schodkowo <em>w dół zbocza</em>","Stein, trappet <em>nedover åsen</em>","Sten, trappad <em>ned för backen</em>")

a("Four terraces of houses follow the contour of the hillside, each row set back above the one below so that no house looks into its neighbour and every roof keeps its view. Natural stone is used in the cladding, and the scheme is built to a BREEAM environmental assessment, with the insulation and glazing specified to cut both energy use and the sound of the coast road below.",
 "Cuatro terrazas de viviendas siguen la curva de nivel de la ladera, cada hilera retranqueada sobre la inferior para que ninguna casa mire a la vecina y todas las azoteas conserven sus vistas. El revestimiento emplea piedra natural y la promoción se construye bajo la evaluación ambiental BREEAM, con el aislamiento y el acristalamiento definidos para reducir tanto el consumo energético como el ruido de la carretera de la costa.",
 "Quatre terrasses de maisons suivent la courbe de niveau du coteau, chaque rangée en retrait au-dessus de celle du dessous afin qu’aucune maison ne regarde chez sa voisine et que chaque toit garde sa vue. La pierre naturelle est utilisée en parement et le programme est construit selon l’évaluation environnementale BREEAM, avec une isolation et des vitrages définis pour réduire à la fois la consommation d’énergie et le bruit de la route côtière en contrebas.",
 "Vier Terrassen von Häusern folgen der Höhenlinie des Hangs, jede Reihe über der darunterliegenden zurückgesetzt, sodass kein Haus zum Nachbarn hineinblickt und jedes Dach seine Aussicht behält. Für die Verkleidung wird Naturstein verwendet, und die Anlage entsteht nach der Umweltbewertung BREEAM, mit Dämmung und Verglasung, die sowohl den Energieverbrauch als auch den Lärm der Küstenstraße darunter senken.",
 "Четыре уступа домов следуют горизонтали склона, каждый ряд отступает над нижним, так что ни один дом не смотрит к соседу и каждая крыша сохраняет вид. В облицовке использован натуральный камень, комплекс строится по экологической оценке BREEAM, а утепление и остекление подобраны так, чтобы снизить и энергопотребление, и шум прибрежной дороги внизу.",
 "أربع مصاطب من المنازل تتبع خط تسوية المنحدر، كل صف مرتدّ فوق الذي تحته بحيث لا يطلّ منزل على جاره ويحتفظ كل سطح بإطلالته. ويُستخدم الحجر الطبيعي في التكسية، ويُبنى المشروع وفق تقييم BREEAM البيئي، مع عزل وتزجيج محدّدين لخفض استهلاك الطاقة وضجيج الطريق الساحلي في الأسفل معاً.",
 "Vier terrassen met huizen volgen de hoogtelijn van de helling, elke rij teruggelegd boven de onderliggende zodat geen huis bij de buren naar binnen kijkt en elk dak zijn uitzicht houdt. In de bekleding is natuursteen gebruikt en het project wordt gebouwd volgens de BREEAM-milieubeoordeling, met isolatie en beglazing die zowel het energieverbruik als het geluid van de kustweg eronder terugbrengen.",
 "Cztery tarasy domów podążają za warstwicą zbocza, każdy rząd cofnięty nad tym poniżej, tak by żaden dom nie patrzył do sąsiada, a każdy dach zachował widok. W okładzinie zastosowano kamień naturalny, a inwestycja powstaje według oceny środowiskowej BREEAM, z izolacją i przeszkleniami dobranymi tak, by ograniczyć zarówno zużycie energii, jak i hałas drogi nadmorskiej poniżej.",
 "Fire terrasser med hus følger høydekurven i skråningen, hver rad trukket tilbake over den under slik at ingen hus ser inn til naboen og hvert tak beholder utsikten. Naturstein er brukt i kledningen, og prosjektet bygges etter miljøvurderingen BREEAM, med isolasjon og glass valgt for å redusere både energibruk og støyen fra kystveien nedenfor.",
 "Fyra terrasser med hus följer sluttningens nivåkurva, varje rad indragen ovanför den nedanför så att inget hus ser in till grannen och varje tak behåller sin utsikt. Natursten används i beklädnaden, och projektet byggs enligt miljöbedömningen BREEAM, med isolering och glas valda för att minska både energianvändning och ljudet från kustvägen nedanför.")

a("Three living levels plus the roof solarium, with a basement level on the upper terrace.",
 "Tres plantas de vivienda más el solárium, con un sótano en la terraza superior.",
 "Trois niveaux de vie plus le solarium, avec un sous-sol sur la terrasse supérieure.",
 "Drei Wohnebenen plus Dachsolarium, auf der oberen Terrasse zusätzlich ein Untergeschoss.",
 "Три жилых уровня плюс солярий, на верхнем уступе — ещё цокольный этаж.",
 "ثلاثة مستويات معيشة إضافة إلى السولاريوم، مع مستوى قبو في المصطبة العليا.",
 "Drie woonlagen plus het dakterras, met een kelderniveau op het bovenste terras.",
 "Trzy kondygnacje mieszkalne plus solarium, z poziomem piwnicy na górnym tarasie.",
 "Tre boligplan pluss solterrassen, med et kjellerplan på den øverste terrassen.",
 "Tre bostadsplan plus solterrassen, med ett källarplan på den övre terrassen.")

a("Large-format Porcelanosa flooring throughout, including the staircases, and full-height tiling in the bathrooms.",
 "Solería Porcelanosa de gran formato en toda la vivienda, incluidas las escaleras, y alicatado de suelo a techo en los baños.",
 "Un sol Porcelanosa grand format dans tout le logement, escaliers compris, et un carrelage toute hauteur dans les salles de bains.",
 "Großformatiger Porcelanosa-Boden im ganzen Haus, auch auf den Treppen, und raumhohe Fliesen in den Bädern.",
 "Крупноформатный пол Porcelanosa по всему дому, включая лестницы, и плитка во всю высоту в ванных.",
 "أرضيات Porcelanosa كبيرة الحجم في كامل المسكن بما فيها الدرج، وتكسية بارتفاع كامل في الحمّامات.",
 "Porcelanosa-vloeren in groot formaat door het hele huis, inclusief de trappen, en tegels tot plafondhoogte in de badkamers.",
 "Wielkoformatowa podłoga Porcelanosa w całym domu, łącznie ze schodami, i płytki od podłogi do sufitu w łazienkach.",
 "Storformat Porcelanosa-gulv i hele huset, også i trappene, og fliser i full høyde på badene.",
 "Storformatigt Porcelanosa-golv i hela huset, även i trapporna, och kakel i full höjd i badrummen.")

a("The roof","La azotea","Le toit","Das Dach","Крыша","السطح","Het dak","Dach","Taket","Taket")

a("A private pool, a sun terrace and, on the show house, an outdoor kitchen and a fire pit.",
 "Piscina privada, terraza de sol y, en la casa piloto, cocina exterior y brasero.",
 "Une piscine privative, une terrasse de bains de soleil et, sur la maison témoin, une cuisine d’extérieur et un foyer.",
 "Ein eigener Pool, eine Sonnenterrasse und, im Musterhaus, eine Außenküche und eine Feuerstelle.",
 "Собственный бассейн, солнечная терраса и, в шоу-хаусе, уличная кухня с очагом.",
 "مسبح خاص وتراس للتشمّس، وفي المنزل النموذجي مطبخ خارجي وموقد.",
 "Een eigen zwembad, een zonneterras en, in de modelwoning, een buitenkeuken en een vuurtafel.",
 "Prywatny basen, taras słoneczny, a w domu pokazowym kuchnia zewnętrzna i palenisko.",
 "Eget basseng, soldekk og, i visningshuset, utekjøkken og bålfat.",
 "Egen pool, soldäck och, i visningshuset, utekök och eldstad.")

a("BREEAM certified, aerothermal heating and cooling, and pre-installation for photovoltaic panels and a home battery.",
 "Certificación BREEAM, climatización por aerotermia y preinstalación de placas fotovoltaicas y batería doméstica.",
 "Certifié BREEAM, chauffage et rafraîchissement aérothermiques, et pré-installation de panneaux photovoltaïques et d’une batterie domestique.",
 "BREEAM-zertifiziert, aerothermes Heizen und Kühlen sowie Vorinstallation für Photovoltaikmodule und einen Hausspeicher.",
 "Сертификация BREEAM, аэротермальное отопление и охлаждение, преднастройка под фотоэлектрические панели и домашний накопитель.",
 "شهادة BREEAM، وتدفئة وتبريد بالطاقة الحرارية الهوائية، وتجهيز مسبق لألواح كهروضوئية وبطارية منزلية.",
 "BREEAM-gecertificeerd, aerothermisch verwarmen en koelen, en voorbereiding voor zonnepanelen en een thuisbatterij.",
 "Certyfikat BREEAM, ogrzewanie i chłodzenie z pompy powietrznej oraz przygotowanie pod fotowoltaikę i domowy magazyn energii.",
 "BREEAM-sertifisert, luft-til-vann-basert varme og kjøling, og forberedelse for solcellepaneler og hjemmebatteri.",
 "BREEAM-certifierat, luftvärmepumpsbaserad värme och kyla, och förberedelse för solceller och hembatteri.")

a("El Higuerón, <em>above Carvajal</em>","El Higuerón, <em>sobre Carvajal</em>","El Higuerón, <em>au-dessus de Carvajal</em>","El Higuerón, <em>über Carvajal</em>",
 "Эль-Игерон, <em>над Карвахалем</em>","إل إيغيرون، <em>فوق كارباخال</em>","El Higuerón, <em>boven Carvajal</em>","El Higuerón, <em>ponad Carvajal</em>","El Higuerón, <em>over Carvajal</em>","El Higuerón, <em>ovanför Carvajal</em>")

a("The scheme sits on the hillside above Carvajal, with Fuengirola on one side and Benalmádena on the other.",
 "La promoción se sitúa en la ladera sobre Carvajal, con Fuengirola a un lado y Benalmádena al otro.",
 "Le programme se situe sur le coteau au-dessus de Carvajal, avec Fuengirola d’un côté et Benalmádena de l’autre.",
 "Die Anlage liegt am Hang über Carvajal, auf der einen Seite Fuengirola, auf der anderen Benalmádena.",
 "Комплекс расположен на склоне над Карвахалем: с одной стороны Фуэнхирола, с другой Бенальмадена.",
 "يقع المشروع على المنحدر فوق كارباخال، وفوينخيرولا من جهة وبينالمادينا من الأخرى.",
 "Het project ligt op de helling boven Carvajal, met Fuengirola aan de ene kant en Benalmádena aan de andere.",
 "Inwestycja leży na zboczu ponad Carvajal, z Fuengirolą po jednej stronie i Benalmádeną po drugiej.",
 "Prosjektet ligger i skråningen over Carvajal, med Fuengirola på den ene siden og Benalmádena på den andre.",
 "Projektet ligger i sluttningen ovanför Carvajal, med Fuengirola på ena sidan och Benalmádena på den andra.")

a("Three communal pools, a gym, a spa with an indoor pool and a relaxation room, a co-working lounge and more than 100,000 sqm of Mediterranean gardens.",
 "Tres piscinas comunitarias, gimnasio, spa con piscina cubierta y sala de relax, sala de coworking y más de 100.000 m² de jardín mediterráneo.",
 "Trois piscines communes, une salle de sport, un spa avec piscine intérieure et salle de relaxation, un salon de coworking et plus de 100 000 m² de jardins méditerranéens.",
 "Drei Gemeinschaftspools, ein Fitnessraum, ein Spa mit Hallenbad und Ruheraum, eine Coworking-Lounge und über 100.000 m² mediterrane Gärten.",
 "Три общих бассейна, спортзал, спа с крытым бассейном и комнатой отдыха, коворкинг-лаундж и более 100 000 м² средиземноморских садов.",
 "ثلاثة مسابح مشتركة وصالة رياضة وسبا بمسبح داخلي وغرفة استرخاء وصالة عمل مشترك وأكثر من 100,000 م² من الحدائق المتوسطية.",
 "Drie gemeenschappelijke zwembaden, een fitnessruimte, een spa met binnenbad en relaxruimte, een coworkinglounge en meer dan 100.000 m² mediterrane tuinen.",
 "Trzy baseny wspólne, siłownia, spa z basenem krytym i salą relaksu, salon coworkingowy oraz ponad 100 000 m² ogrodów śródziemnomorskich.",
 "Tre fellesbassenger, treningsrom, spa med innendørsbasseng og relaksrom, coworking-lounge og mer enn 100 000 m² middelhavshager.",
 "Tre gemensamma pooler, gym, spa med inomhuspool och avkopplingsrum, coworkinglounge och mer än 100 000 m² medelhavsträdgårdar.")

a("The Carvajal train station, Carvajal and Torreblanca beaches and Benalmádena town centre are all under five minutes away.",
 "La estación de Carvajal, las playas de Carvajal y Torreblanca y el centro de Benalmádena quedan todos a menos de cinco minutos.",
 "La gare de Carvajal, les plages de Carvajal et de Torreblanca et le centre de Benalmádena sont tous à moins de cinq minutes.",
 "Der Bahnhof Carvajal, die Strände von Carvajal und Torreblanca und das Zentrum von Benalmádena liegen alle unter fünf Minuten entfernt.",
 "Станция Карвахаль, пляжи Карвахаль и Торребланка и центр Бенальмадены — всё менее чем в пяти минутах.",
 "محطة كارباخال وشاطئا كارباخال وتوريبلانكا ووسط بينالمادينا، جميعها على بُعد أقل من خمس دقائق.",
 "Het treinstation Carvajal, de stranden van Carvajal en Torreblanca en het centrum van Benalmádena liggen allemaal op minder dan vijf minuten.",
 "Stacja Carvajal, plaże Carvajal i Torreblanca oraz centrum Benalmádeny są niecałe pięć minut stąd.",
 "Togstasjonen Carvajal, strendene Carvajal og Torreblanca og Benalmádena sentrum ligger alle under fem minutter unna.",
 "Tågstationen Carvajal, stränderna Carvajal och Torreblanca och Benalmádenas centrum ligger alla under fem minuter bort.")

a("Fuengirola centre, its marina, Mijas Pueblo and the Miramar shopping centre are about ten minutes, and Málaga and Marbella fifteen to twenty.",
 "El centro de Fuengirola, su puerto deportivo, Mijas Pueblo y el centro comercial Miramar quedan a unos diez minutos, y Málaga y Marbella entre quince y veinte.",
 "Le centre de Fuengirola, son port de plaisance, Mijas Pueblo et le centre commercial Miramar sont à une dizaine de minutes, et Málaga et Marbella à quinze ou vingt.",
 "Das Zentrum von Fuengirola, sein Yachthafen, Mijas Pueblo und das Einkaufszentrum Miramar liegen etwa zehn Minuten entfernt, Málaga und Marbella fünfzehn bis zwanzig.",
 "Центр Фуэнхиролы, её марина, Михас-Пуэбло и торговый центр Мирамар — примерно в десяти минутах, Малага и Марбелья — в пятнадцати-двадцати.",
 "وسط فوينخيرولا ومرساها وميخاس بويبلو ومركز ميرامار التجاري على نحو عشر دقائق، ومالقة وماربيا بين خمس عشرة وعشرين دقيقة.",
 "Het centrum van Fuengirola, de jachthaven, Mijas Pueblo en winkelcentrum Miramar liggen op ongeveer tien minuten, en Málaga en Marbella op vijftien tot twintig.",
 "Centrum Fuengiroli, jej marina, Mijas Pueblo i centrum handlowe Miramar są około dziesięciu minut stąd, a Malaga i Marbella piętnaście do dwudziestu.",
 "Fuengirola sentrum, gjestehavna, Mijas Pueblo og kjøpesenteret Miramar ligger rundt ti minutter unna, og Málaga og Marbella femten til tjue.",
 "Fuengirolas centrum, dess småbåtshamn, Mijas Pueblo och köpcentret Miramar ligger omkring tio minuter bort, och Málaga och Marbella femton till tjugo.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
