# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 8: the four images.*.alt texts.
# These sit outside media.items, and both scaffold and my own patch skipped
# "alt" as a non-translating key -- which is true for media captions and false
# here. Attribute text has no visible symptom when it stays English.
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("The eight blocks at dusk, stepping up the slope above the pool terrace",
 "Los ocho bloques al anochecer, ascendiendo por la ladera sobre la terraza de la piscina",
 "Les huit blocs au crépuscule, gravissant la pente au-dessus de la terrasse de la piscine",
 "Die acht Blöcke in der Dämmerung, den Hang über der Poolterrasse hinaufsteigend",
 "Восемь корпусов в сумерках, поднимающихся по склону над террасой бассейна",
 "المباني الثمانية عند الغسق، متدرّجة صعوداً على المنحدر فوق تراس المسبح",
 "De acht blokken in de schemering, de helling op boven het zwembadterras",
 "Osiem budynków o zmierzchu, wspinających się po zboczu nad tarasem basenowym",
 "De åtte blokkene i skumringen, trappende oppover skråningen over bassengterrassen",
 "De åtta huskropparna i skymningen, trappande uppför sluttningen ovanför poolterrassen")

a("The blocks in daylight, each set a level above the one below it",
 "Los bloques a la luz del día, cada uno situado un nivel por encima del anterior",
 "Les blocs en plein jour, chacun implanté un niveau au-dessus du précédent",
 "Die Blöcke bei Tageslicht, jeder eine Ebene über dem darunterliegenden",
 "Корпуса при дневном свете, каждый на уровень выше предыдущего",
 "المباني في ضوء النهار، كل منها على مستوى أعلى من الذي تحته",
 "De blokken bij daglicht, elk een niveau boven het voorgaande",
 "Budynki w świetle dnia, każdy osadzony o poziom wyżej niż poprzedni",
 "Blokkene i dagslys, hver satt ett nivå over den under",
 "Huskropparna i dagsljus, var och en satt en nivå ovanför den under")

a("The infinity pool on its terrace, the Mediterranean beyond the edge",
 "La piscina infinita en su terraza, con el Mediterráneo más allá del borde",
 "La piscine à débordement sur sa terrasse, la Méditerranée au-delà du bord",
 "Der Infinity-Pool auf seiner Terrasse, das Mittelmeer jenseits der Kante",
 "Бассейн-инфинити на своей террасе, Средиземное море за краем",
 "المسبح اللامتناهي على تراسه، والبحر المتوسط خلف الحافة",
 "Het infinityzwembad op zijn terras, de Middellandse Zee voorbij de rand",
 "Basen infinity na swoim tarasie, Morze Śródziemne za krawędzią",
 "Infinity-bassenget på terrassen sin, Middelhavet bak kanten",
 "Infinitypoolen på sin terrass, Medelhavet bortom kanten")

a("An open-plan kitchen and living room with the terrace beyond",
 "Una cocina y un salón en planta abierta con la terraza al fondo",
 "Une cuisine et un séjour ouverts avec la terrasse au-delà",
 "Eine offene Küche und ein Wohnzimmer mit der Terrasse dahinter",
 "Кухня-гостиная открытой планировки с террасой за ней",
 "مطبخ وصالة بتصميم مفتوح والتراس في الخلف",
 "Een open keuken en woonkamer met het terras erachter",
 "Otwarta kuchnia i salon z tarasem w tle",
 "Et åpent kjøkken og stue med terrassen bak",
 "Ett öppet kök och vardagsrum med terrassen bakom")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
