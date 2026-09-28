# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}
a("Ten new-build apartments available on a wooded Mijas hillside between La Cala and Fuengirola: two and three bedrooms, 92.81 to 136.53 sqm built, from EUR 376,000 net of tax.",
 "Diez apartamentos de obra nueva disponibles en una ladera arbolada de Mijas, entre La Cala y Fuengirola: dos y tres dormitorios, de 92,81 a 136,53 m² construidos, desde 376.000 € más impuestos.",
 "Dix appartements neufs disponibles sur un coteau boisé de Mijas, entre La Cala et Fuengirola : deux et trois chambres, de 92,81 à 136,53 m² construits, à partir de 376 000 € hors taxes.",
 "Zehn verfügbare Neubauwohnungen an einem bewaldeten Hang in Mijas, zwischen La Cala und Fuengirola: zwei und drei Schlafzimmer, 92,81 bis 136,53 m² Wohnfläche, ab 376.000 € zuzüglich Steuern.",
 "Десять новых квартир на лесистом склоне в Михасе, между Ла-Калой и Фуэнхиролой: две и три спальни, от 92,81 до 136,53 м² построенной площади, от 376 000 € без учёта налогов.",
 "عشر شقق جديدة متاحة على منحدر مشجّر في ميخاس، بين لا كالا وفوينخيرولا: غرفتان وثلاث غرف نوم، من 92.81 إلى 136.53 م² مبنية، تبدأ من 376,000 € دون الضرائب.",
 "Tien beschikbare nieuwbouwappartementen op een beboste helling in Mijas, tussen La Cala en Fuengirola: twee en drie slaapkamers, 92,81 tot 136,53 m² bouwoppervlak, vanaf € 376.000 exclusief belastingen.",
 "Dziesięć dostępnych nowych apartamentów na zalesionym zboczu w Mijas, między La Cala a Fuengirolą: dwie i trzy sypialnie, od 92,81 do 136,53 m² powierzchni zabudowanej, od 376 000 € bez podatków.",
 "Ti tilgjengelige nye leiligheter i en skogkledd skråning i Mijas, mellom La Cala og Fuengirola: to og tre soverom, 92,81 til 136,53 m² bygget, fra 376 000 € eksklusive avgifter.",
 "Tio tillgängliga nyproducerade lägenheter på en skogbevuxen sluttning i Mijas, mellan La Cala och Fuengirola: två och tre sovrum, 92,81 till 136,53 m² byggyta, från 376 000 € exklusive skatter.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
