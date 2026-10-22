# -*- coding: utf-8 -*-
"""Formal register fixes: sv (ni, not du/dig) and pl (Panstwo forms), applied to the translation sources and outputs."""
import glob
R = [
 ("innan du reserverar", "innan ni reserverar"),
 ("de villor som intresserar dig", "de villor som intresserar er"),
 ("tillsammans med dig och tar tiden", "tillsammans med er och tar tiden"),
 ("Berätta vad du behöver så återkommer vi", "Berätta vad ni behöver så återkommer vi"),
 ("Porównaj go z innymi projektami willi", "Zestawiamy tę inwestycję z innymi projektami willi"),
 ("Zobacz z nami teren i okolicę oraz porównaj rzuty z miejscem.", "Wspólnie oglądamy teren i okolicę oraz porównujemy rzuty z miejscem."),
 ("Przejdź się po działce i ulicy oraz drogą do plaży.", "Spacer po działce i ulicy oraz drogą do plaży."),
 ("Zapytaj o <em>", "Zapytanie o <em>"),
 ("Napisz, czego potrzebujesz, a wrócimy", "Proszę napisać, czego Państwo potrzebują, a wrócimy"),
]
for f in glob.glob('tr_[a-z].json') + glob.glob('k_*.py'):
    s = open(f, encoding='utf-8').read(); o = s
    for a, b in R: s = s.replace(a, b)
    if s != o: open(f, 'w', encoding='utf-8').write(s); print('patched', f)
