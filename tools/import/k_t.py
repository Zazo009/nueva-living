# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Eight of 70 south-facing apartments on the slope above Benalmádena Pueblo, with a pool, a gym and a chill-out terrace, and two parking spaces with every home.",
 "Ocho de 70 apartamentos orientados al sur en la ladera sobre Benalmádena Pueblo, con piscina, gimnasio y terraza chill-out, y dos plazas de garaje en cada vivienda.",
 "Huit appartements sur 70, orientés au sud, sur le coteau au-dessus de Benalmádena Pueblo, avec piscine, salle de sport et terrasse chill-out, et deux places de parking par logement.",
 "Acht von 70 nach Süden orientierten Wohnungen am Hang über Benalmádena Pueblo, mit Pool, Fitnessraum und Chill-out-Terrasse und zwei Stellplätzen je Wohnung.",
 "Восемь из 70 квартир южной ориентации на склоне над Бенальмадена-Пуэбло: бассейн, спортзал и терраса чил-аут, а также два машиноместа в каждой квартире.",
 "ثمانٍ من أصل 70 شقة موجّهة جنوباً على المنحدر فوق بينالمادينا بويبلو، مع مسبح وصالة رياضة وتراس استرخاء، وموقفي سيارات لكل مسكن.",
 "Acht van de 70 op het zuiden gerichte appartementen op de helling boven Benalmádena Pueblo, met zwembad, fitnessruimte en chill-outterras, en twee parkeerplaatsen bij elke woning.",
 "Osiem z 70 mieszkań o południowej ekspozycji na zboczu nad Benalmádena Pueblo, z basenem, siłownią i tarasem chill-out oraz dwoma miejscami postojowymi przy każdym mieszkaniu.",
 "Åtte av 70 sørvendte leiligheter i hellingen over Benalmádena Pueblo, med basseng, treningsrom og chill-out-terrasse, og to parkeringsplasser til hver bolig.",
 "Åtta av 70 södervända lägenheter på sluttningen ovanför Benalmádena Pueblo, med pool, gym och chill-out-terrass, och två parkeringsplatser till varje bostad.")

a("Eight of 70 new-build apartments available above Benalmádena Pueblo: two and three bedrooms, 85 to 110 sqm built, terraces to 77.60 sqm, from EUR 338,900 net of tax.",
 "Ocho de 70 apartamentos de obra nueva disponibles sobre Benalmádena Pueblo: dos y tres dormitorios, de 85 a 110 m² construidos, terrazas hasta 77,60 m², desde 338.900 € más impuestos.",
 "Huit appartements neufs sur 70 disponibles au-dessus de Benalmádena Pueblo : deux et trois chambres, de 85 à 110 m² construits, terrasses jusqu'à 77,60 m², à partir de 338 900 € hors taxes.",
 "Acht von 70 Neubauwohnungen über Benalmádena Pueblo verfügbar: zwei und drei Schlafzimmer, 85 bis 110 m² bebaut, Terrassen bis 77,60 m², ab 338.900 € zzgl. Steuern.",
 "Восемь из 70 новых квартир доступны над Бенальмадена-Пуэбло: две и три спальни, от 85 до 110 м² застройки, террасы до 77,60 м², от 338 900 € без налогов.",
 "ثمانٍ من أصل 70 شقة جديدة متاحة فوق بينالمادينا بويبلو: غرفتا نوم وثلاث، من 85 إلى 110 م² مبنية، تراسات حتى 77.60 م²، ابتداءً من 338,900 € قبل الضرائب.",
 "Acht van de 70 nieuwbouwappartementen beschikbaar boven Benalmádena Pueblo: twee en drie slaapkamers, 85 tot 110 m² bebouwd, terrassen tot 77,60 m², vanaf € 338.900 exclusief belastingen.",
 "Osiem z 70 nowych mieszkań dostępnych nad Benalmádena Pueblo: dwie i trzy sypialnie, od 85 do 110 m² powierzchni zabudowy, tarasy do 77,60 m², od 338 900 € bez podatków.",
 "Åtte av 70 nye leiligheter ledige over Benalmádena Pueblo: to og tre soverom, 85 til 110 m² bruksareal, terrasser opptil 77,60 m², fra 338 900 € uten avgifter.",
 "Åtta av 70 nybyggda lägenheter lediga ovanför Benalmádena Pueblo: två och tre sovrum, 85 till 110 m² byggyta, terrasser upp till 77,60 m², från 338 900 € exklusive skatter.")

a("Benalmádena Pueblo","Benalmádena Pueblo","Benalmádena Pueblo","Benalmádena Pueblo","Бенальмадена-Пуэбло","بينالمادينا بويبلو","Benalmádena Pueblo","Benalmádena Pueblo","Benalmádena Pueblo","Benalmádena Pueblo")

a("Completion Q4 2027","Entrega T4 2027","Livraison T4 2027","Fertigstellung Q4 2027","Сдача 4 кв. 2027","التسليم الربع الرابع 2027","Oplevering K4 2027","Odbiór IV kw. 2027","Ferdigstilling K4 2027","Färdigställande K4 2027")

a("Eight of 70 south-facing apartments above Benalmádena Pueblo, with a pool, a gym and a chill-out terrace.",
 "Ocho de 70 apartamentos orientados al sur sobre Benalmádena Pueblo, con piscina, gimnasio y terraza chill-out.",
 "Huit appartements sur 70, orientés au sud, au-dessus de Benalmádena Pueblo, avec piscine, salle de sport et terrasse chill-out.",
 "Acht von 70 nach Süden orientierten Wohnungen über Benalmádena Pueblo, mit Pool, Fitnessraum und Chill-out-Terrasse.",
 "Восемь из 70 квартир южной ориентации над Бенальмадена-Пуэбло: бассейн, спортзал и терраса чил-аут.",
 "ثمانٍ من أصل 70 شقة موجّهة جنوباً فوق بينالمادينا بويبلو، مع مسبح وصالة رياضة وتراس استرخاء.",
 "Acht van de 70 op het zuiden gerichte appartementen boven Benalmádena Pueblo, met zwembad, fitnessruimte en chill-outterras.",
 "Osiem z 70 mieszkań o południowej ekspozycji nad Benalmádena Pueblo, z basenem, siłownią i tarasem chill-out.",
 "Åtte av 70 sørvendte leiligheter over Benalmádena Pueblo, med basseng, treningsrom og chill-out-terrasse.",
 "Åtta av 70 södervända lägenheter ovanför Benalmádena Pueblo, med pool, gym och chill-out-terrass.")

a("Developer visuals of the homes, the pool, the gym and the chill-out terrace.",
 "Imágenes de la promotora de las viviendas, la piscina, el gimnasio y la terraza chill-out.",
 "Images du promoteur des logements, de la piscine, de la salle de sport et de la terrasse chill-out.",
 "Visualisierungen des Bauträgers von den Wohnungen, dem Pool, dem Fitnessraum und der Chill-out-Terrasse.",
 "Визуализации застройщика: квартиры, бассейн, спортзал и терраса чил-аут.",
 "تصاميم المطور للمساكن والمسبح وصالة الرياضة وتراس الاسترخاء.",
 "Impressies van de ontwikkelaar van de woningen, het zwembad, de fitnessruimte en het chill-outterras.",
 "Wizualizacje dewelopera mieszkań, basenu, siłowni i tarasu chill-out.",
 "Utviklerens visualiseringer av boligene, bassenget, treningsrommet og chill-out-terrassen.",
 "Byggherrens visualiseringar av bostäderna, poolen, gymmet och chill-out-terrassen.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
