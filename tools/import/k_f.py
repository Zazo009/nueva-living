# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Ten apartments available in a gated scheme on a wooded Mijas hillside between La Cala and Fuengirola, with saltwater pools, a gym, padel and pickleball courts and a coworking room.",
 "Diez apartamentos disponibles en una promoción cerrada sobre una ladera arbolada de Mijas, entre La Cala y Fuengirola, con piscinas de agua salada, gimnasio, pistas de pádel y pickleball y sala de coworking.",
 "Dix appartements disponibles dans une résidence fermée sur un coteau boisé de Mijas, entre La Cala et Fuengirola, avec piscines d'eau salée, salle de sport, terrains de padel et de pickleball et espace de coworking.",
 "Zehn verfügbare Wohnungen in einer geschlossenen Anlage an einem bewaldeten Hang in Mijas, zwischen La Cala und Fuengirola, mit Salzwasserpools, Fitnessraum, Padel- und Pickleball-Plätzen und Coworking-Raum.",
 "Десять доступных квартир в закрытом комплексе на лесистом склоне в Михасе, между Ла-Калой и Фуэнхиролой, с бассейнами на солёной воде, тренажёрным залом, кортами для паделя и пиклбола и коворкингом.",
 "عشر شقق متاحة في مجمع مغلق على منحدر مشجّر في ميخاس، بين لا كالا وفوينخيرولا، مع مسابح بالمياه المالحة وصالة رياضية وملاعب بادل وبيكل بول وغرفة عمل مشترك.",
 "Tien beschikbare appartementen in een besloten project op een beboste helling in Mijas, tussen La Cala en Fuengirola, met zoutwaterzwembaden, een fitnessruimte, padel- en pickleballbanen en een coworkingruimte.",
 "Dziesięć dostępnych apartamentów w zamkniętej inwestycji na zalesionym zboczu w Mijas, między La Cala a Fuengirolą, z basenami słonowodnymi, siłownią, kortami do padla i pickleballa oraz salą coworkingową.",
 "Ti tilgjengelige leiligheter i et lukket prosjekt i en skogkledd skråning i Mijas, mellom La Cala og Fuengirola, med saltvannsbassenger, treningsrom, padel- og pickleballbaner og et coworking-rom.",
 "Tio tillgängliga lägenheter i ett slutet projekt på en skogbevuxen sluttning i Mijas, mellan La Cala och Fuengirola, med saltvattenpooler, gym, padel- och pickleballbanor och ett coworking-rum.")

a("Explore Mijas Pinewood Residences, 2-3 bed apartments in Mijas from EUR 376,000.",
 "Descubra Mijas Pinewood Residences, apartamentos de 2-3 dormitorios en Mijas desde 376.000 €.",
 "Découvrez Mijas Pinewood Residences, des appartements de 2-3 chambres à Mijas à partir de 376 000 €.",
 "Entdecken Sie Mijas Pinewood Residences, Wohnungen mit 2-3 Schlafzimmern in Mijas ab 376.000 €.",
 "Откройте для себя Mijas Pinewood Residences — апартаменты с 2-3 спальнями в Михасе от 376 000 €.",
 "اكتشف Mijas Pinewood Residences، شقق بغرفتين إلى ثلاث غرف نوم في ميخاس تبدأ من 376,000 €.",
 "Ontdek Mijas Pinewood Residences, appartementen met 2-3 slaapkamers in Mijas vanaf € 376.000.",
 "Poznaj Mijas Pinewood Residences, apartamenty z 2-3 sypialniami w Mijas od 376 000 €.",
 "Oppdag Mijas Pinewood Residences, leiligheter med 2-3 soverom i Mijas fra 376 000 €.",
 "Upptäck Mijas Pinewood Residences, lägenheter med 2-3 sovrum i Mijas från 376 000 €.")

a("10 homes available","10 viviendas disponibles","10 logements disponibles","10 verfügbare Wohnungen",
 "10 доступных квартир","10 منازل متاحة","10 beschikbare woningen","10 dostępnych mieszkań",
 "10 tilgjengelige boliger","10 tillgängliga bostäder")

a("Mijas, between La Cala and Fuengirola","Mijas, entre La Cala y Fuengirola","Mijas, entre La Cala et Fuengirola",
 "Mijas, zwischen La Cala und Fuengirola","Михас, между Ла-Калой и Фуэнхиролой","ميخاس، بين لا كالا وفوينخيرولا",
 "Mijas, tussen La Cala en Fuengirola","Mijas, między La Cala a Fuengirolą","Mijas, mellom La Cala og Fuengirola",
 "Mijas, mellan La Cala och Fuengirola")

a("Completion Q3 2029","Entrega T3 2029","Livraison T3 2029","Fertigstellung Q3 2029",
 "Сдача 3 кв. 2029","الإنجاز الربع الثالث 2029","Oplevering K3 2029","Zakończenie III kw. 2029",
 "Ferdigstilling K3 2029","Färdigställande K3 2029")

a("Ten apartments available on a wooded Mijas hillside between La Cala and Fuengirola, with saltwater pools, a gym, padel and pickleball courts and a coworking room.",
 "Diez apartamentos disponibles en una ladera arbolada de Mijas, entre La Cala y Fuengirola, con piscinas de agua salada, gimnasio, pistas de pádel y pickleball y sala de coworking.",
 "Dix appartements disponibles sur un coteau boisé de Mijas, entre La Cala et Fuengirola, avec piscines d'eau salée, salle de sport, terrains de padel et de pickleball et espace de coworking.",
 "Zehn verfügbare Wohnungen an einem bewaldeten Hang in Mijas, zwischen La Cala und Fuengirola, mit Salzwasserpools, Fitnessraum, Padel- und Pickleball-Plätzen und Coworking-Raum.",
 "Десять доступных квартир на лесистом склоне в Михасе, между Ла-Калой и Фуэнхиролой, с бассейнами на солёной воде, тренажёрным залом, кортами для паделя и пиклбола и коворкингом.",
 "عشر شقق متاحة على منحدر مشجّر في ميخاس، بين لا كالا وفوينخيرولا، مع مسابح بالمياه المالحة وصالة رياضية وملاعب بادل وبيكل بول وغرفة عمل مشترك.",
 "Tien beschikbare appartementen op een beboste helling in Mijas, tussen La Cala en Fuengirola, met zoutwaterzwembaden, een fitnessruimte, padel- en pickleballbanen en een coworkingruimte.",
 "Dziesięć dostępnych apartamentów na zalesionym zboczu w Mijas, między La Cala a Fuengirolą, z basenami słonowodnymi, siłownią, kortami do padla i pickleballa oraz salą coworkingową.",
 "Ti tilgjengelige leiligheter i en skogkledd skråning i Mijas, mellom La Cala og Fuengirola, med saltvannsbassenger, treningsrom, padel- og pickleballbaner og et coworking-rom.",
 "Tio tillgängliga lägenheter på en skogbevuxen sluttning i Mijas, mellan La Cala och Fuengirola, med saltvattenpooler, gym, padel- och pickleballbanor och ett coworking-rum.")

a("The scheme in <em>pictures</em>","La promoción en <em>imágenes</em>","Le programme en <em>images</em>",
 "Die Anlage in <em>Bildern</em>","Комплекс <em>в изображениях</em>","المشروع <em>بالصور</em>",
 "Het project in <em>beeld</em>","Inwestycja w <em>obrazach</em>","Prosjektet i <em>bilder</em>","Projektet i <em>bilder</em>")

a("Developer visuals of the homes, the pools and the communal spaces.",
 "Imágenes del promotor de las viviendas, las piscinas y las zonas comunes.",
 "Visuels du promoteur des logements, des piscines et des espaces communs.",
 "Bauträger-Visualisierungen der Wohnungen, der Pools und der Gemeinschaftsbereiche.",
 "Визуализации застройщика: квартиры, бассейны и общие зоны.",
 "تصورات من المطور للمنازل والمسابح والمساحات المشتركة.",
 "Beelden van de ontwikkelaar van de woningen, de zwembaden en de gemeenschappelijke ruimten.",
 "Wizualizacje dewelopera mieszkań, basenów i przestrzeni wspólnych.",
 "Visualiseringer fra utbygger av boligene, bassengene og fellesarealene.",
 "Visualiseringar från utvecklaren av bostäderna, poolerna och de gemensamma ytorna.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
