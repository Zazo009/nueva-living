# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("The project file, <em>as we hold it</em>","El dossier del proyecto, <em>tal como lo tenemos</em>",
 "Le dossier du programme, <em>tel que nous le détenons</em>","Die Projektunterlagen, <em>wie wir sie halten</em>",
 "Досье проекта, <em>как оно у нас есть</em>","ملف المشروع، <em>كما لدينا</em>",
 "Het projectdossier, <em>zoals wij het hebben</em>","Teczka inwestycji, <em>tak jak ją mamy</em>",
 "Prosjektmappen, <em>slik vi har den</em>","Projektmappen, <em>som vi har den</em>")
a("What Nueva Living sends when you ask about this scheme.","Lo que Nueva Living envía cuando pregunta por esta promoción.",
 "Ce que Nueva Living envoie lorsque vous posez une question sur ce programme.",
 "Was Nueva Living schickt, wenn Sie nach dieser Anlage fragen.",
 "Что Nueva Living присылает в ответ на вопрос об этом комплексе.",
 "ما ترسله Nueva Living عند السؤال عن هذا المشروع.",
 "Wat Nueva Living stuurt als u naar dit project vraagt.",
 "Co Nueva Living wysyła, gdy zapytają Państwo o tę inwestycję.",
 "Det Nueva Living sender når du spør om dette prosjektet.",
 "Det Nueva Living skickar när projektet efterfrågas.")
a("Availability list","Lista de disponibilidad","Liste de disponibilité","Verfügbarkeitsliste","Список наличия",
 "قائمة التوافر","Beschikbaarheidslijst","Lista dostępności","Tilgjengelighetsliste","Tillgänglighetslista")
a("Floors, areas and prices as the seller lists them.","Plantas, superficies y precios tal como los lista el vendedor.",
 "Étages, surfaces et prix tels que le vendeur les indique.","Geschosse, Flächen und Preise, wie der Verkäufer sie aufführt.",
 "Этажи, площади и цены в том виде, в каком их указывает продавец.",
 "الطوابق والمساحات والأسعار كما يدرجها البائع.",
 "Verdiepingen, oppervlakten en prijzen zoals de verkoper ze opgeeft.",
 "Kondygnacje, powierzchnie i ceny w postaci podanej przez sprzedającego.",
 "Etasjer, arealer og priser slik selgeren oppgir dem.","Våningar, ytor och priser som säljaren anger dem.")
a("The developer's quality specification.","La memoria de calidades del promotor.","Le descriptif technique du promoteur.",
 "Die Baubeschreibung des Bauträgers.","Спецификация качества от застройщика.","مواصفات الجودة الخاصة بالمطور.",
 "Het lastenboek van de ontwikkelaar.","Specyfikacja techniczna dewelopera.","Utbyggerens kvalitetsbeskrivelse.","Utvecklarens kvalitetsbeskrivning.")
a("Brochure","Folleto","Brochure","Broschüre","Буклет","الكتيّب","Brochure","Folder","Brosjyre","Broschyr")
a("The developer's own brochure.","El folleto del propio promotor.","La brochure du promoteur lui-même.",
 "Die Broschüre des Bauträgers selbst.","Собственный буклет застройщика.","الكتيّب الخاص بالمطور نفسه.",
 "De eigen brochure van de ontwikkelaar.","Własny folder dewelopera.","Utbyggerens egen brosjyre.","Utvecklarens egen broschyr.")
a("See it <em>in person</em>","Verlo <em>en persona</em>","Le voir <em>sur place</em>","<em>Vor Ort</em> ansehen",
 "Посмотреть <em>лично</em>","شاهده <em>على الطبيعة</em>","Bekijk het <em>ter plaatse</em>","Zobacz <em>na miejscu</em>",
 "Se det <em>på stedet</em>","Se det <em>på plats</em>")
a("Nueva Living arranges the appointment, walks the site with you and asks the questions that are easy to forget on the day.",
 "Nueva Living concierta la cita, recorre la parcela con usted y hace las preguntas que es fácil olvidar ese día.",
 "Nueva Living organise le rendez-vous, parcourt le terrain avec vous et pose les questions faciles à oublier le jour même.",
 "Nueva Living vereinbart den Termin, geht das Grundstück mit Ihnen ab und stellt die Fragen, die man vor Ort leicht vergisst.",
 "Nueva Living договаривается о встрече, обходит участок вместе с вами и задаёт вопросы, о которых легко забыть на месте.",
 "تنسّق Nueva Living الموعد، وتتجول معك في الموقع، وتطرح الأسئلة التي يسهل نسيانها في ذلك اليوم.",
 "Nueva Living maakt de afspraak, loopt het terrein met u door en stelt de vragen die je die dag makkelijk vergeet.",
 "Nueva Living umawia wizytę, obchodzi z Państwem teren i zadaje pytania, o których łatwo tego dnia zapomnieć.",
 "Nueva Living avtaler visningen, går tomten sammen med deg og stiller spørsmålene som er lette å glemme på dagen.",
 "Nueva Living bokar visningen, går tomten tillsammans med köparen och ställer frågorna som är lätta att glömma på plats.")
a("Aspect","Orientación","Exposition","Ausrichtung","Ориентация","الاتجاه","Oriëntatie","Ekspozycja","Retning","Läge")
a("Which blocks keep the view as the scheme fills out.","Qué bloques conservan las vistas a medida que la promoción se completa.",
 "Quels immeubles conservent la vue à mesure que le programme se remplit.",
 "Welche Gebäude die Aussicht behalten, wenn die Anlage sich füllt.",
 "Какие корпуса сохранят вид по мере застройки комплекса.",
 "أي المباني تحتفظ بالإطلالة مع اكتمال المشروع.",
 "Welke gebouwen het uitzicht houden naarmate het project volloopt.",
 "Które budynki zachowają widok w miarę zabudowy inwestycji.",
 "Hvilke bygg beholder utsikten etter hvert som prosjektet fylles opp.",
 "Vilka hus behåller utsikten allteftersom projektet fylls.")
a("What the ground-floor gardens and the penthouse terraces actually give you.",
 "Qué aportan realmente los jardines en planta baja y las terrazas de los áticos.",
 "Ce qu'apportent réellement les jardins en rez-de-chaussée et les terrasses des penthouses.",
 "Was die Erdgeschossgärten und die Penthouse-Terrassen tatsächlich bringen.",
 "Что на деле дают сады на первом этаже и террасы пентхаусов.",
 "ما تقدمه فعلياً حدائق الطابق الأرضي وشرفات البنتهاوس.",
 "Wat de tuinen op de begane grond en de penthouseterrassen werkelijk opleveren.",
 "Co naprawdę dają ogrody na parterze i tarasy penthouse'ów.",
 "Hva hagene i første etasje og toppleilighetenes terrasser faktisk gir.",
 "Vad trädgårdarna på bottenvåningen och takvåningarnas terrasser faktiskt ger.")
a("Costs","Costes","Coûts","Kosten","Расходы","التكاليف","Kosten","Koszty","Kostnader","Kostnader")
a("The community fee for a scheme with this much communal space.",
 "La cuota de comunidad de una promoción con tantas zonas comunes.",
 "Les charges de copropriété pour un programme doté d'autant d'espaces communs.",
 "Das Hausgeld für eine Anlage mit so vielen Gemeinschaftsflächen.",
 "Взнос на содержание комплекса с таким объёмом общих зон.",
 "رسوم الخدمات لمشروع بهذا القدر من المساحات المشتركة.",
 "De servicekosten voor een project met zoveel gemeenschappelijke ruimte.",
 "Czynsz wspólnoty przy inwestycji z tak dużą częścią wspólną.",
 "Fellesutgiftene for et prosjekt med så mye fellesareal.",
 "Samfällighetsavgiften för ett projekt med så mycket gemensam yta.")
a("Mijas, <em>between La Cala and Fuengirola</em>","Mijas, <em>entre La Cala y Fuengirola</em>",
 "Mijas, <em>entre La Cala et Fuengirola</em>","Mijas, <em>zwischen La Cala und Fuengirola</em>",
 "Михас, <em>между Ла-Калой и Фуэнхиролой</em>","ميخاس، <em>بين لا كالا وفوينخيرولا</em>",
 "Mijas, <em>tussen La Cala en Fuengirola</em>","Mijas, <em>między La Cala a Fuengirolą</em>",
 "Mijas, <em>mellom La Cala og Fuengirola</em>","Mijas, <em>mellan La Cala och Fuengirola</em>")
a("A gated scheme on a wooded slope in Mijas, with direct access to the A-7 and AP-7 and the beaches of Mijas Costa and Fuengirola a few minutes away.",
 "Una promoción cerrada en una ladera arbolada de Mijas, con acceso directo a la A-7 y la AP-7 y las playas de Mijas Costa y Fuengirola a pocos minutos.",
 "Une résidence fermée sur un coteau boisé de Mijas, avec accès direct à l'A-7 et à l'AP-7 et les plages de Mijas Costa et Fuengirola à quelques minutes.",
 "Eine geschlossene Anlage an einem bewaldeten Hang in Mijas, mit direkter Anbindung an die A-7 und AP-7 und den Stränden von Mijas Costa und Fuengirola wenige Minuten entfernt.",
 "Закрытый комплекс на лесистом склоне в Михасе, с прямым выездом на A-7 и AP-7 и пляжами Михас-Косты и Фуэнхиролы в нескольких минутах.",
 "مجمع مغلق على منحدر مشجّر في ميخاس، مع وصول مباشر إلى A-7 وAP-7 وشواطئ ميخاس كوستا وفوينخيرولا على بعد دقائق.",
 "Een besloten project op een beboste helling in Mijas, met directe aansluiting op de A-7 en AP-7 en de stranden van Mijas Costa en Fuengirola op enkele minuten.",
 "Zamknięta inwestycja na zalesionym zboczu w Mijas, z bezpośrednim dojazdem do A-7 i AP-7 oraz plażami Mijas Costa i Fuengiroli kilka minut dalej.",
 "Et lukket prosjekt i en skogkledd skråning i Mijas, med direkte adkomst til A-7 og AP-7 og strendene i Mijas Costa og Fuengirola noen minutter unna.",
 "Ett slutet projekt på en skogbevuxen sluttning i Mijas, med direkt anslutning till A-7 och AP-7 och stränderna i Mijas Costa och Fuengirola några minuter bort.")
a("Approx. 35 min","Aprox. 35 min","Env. 35 min","Ca. 35 Min.","Ок. 35 мин","حوالي 35 دقيقة","Ca. 35 min","Ok. 35 min","Ca. 35 min","Ca 35 min")
a("Approx. 25 min","Aprox. 25 min","Env. 25 min","Ca. 25 Min.","Ок. 25 мин","حوالي 25 دقيقة","Ca. 25 min","Ok. 25 min","Ca. 25 min","Ca 25 min")
a("Approx. 30 min","Aprox. 30 min","Env. 30 min","Ca. 30 Min.","Ок. 30 мин","حوالي 30 دقيقة","Ca. 30 min","Ok. 30 min","Ca. 30 min","Ca 30 min")
a("Puerto Banus","Puerto Banús","Puerto Banús","Puerto Banús","Пуэрто-Банус","بويرتو بانوس","Puerto Banús","Puerto Banús","Puerto Banús","Puerto Banús")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
