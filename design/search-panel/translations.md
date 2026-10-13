# Translations for the search, filter and map redesign

Final wording for all 9 languages. I checked each label against the vocabulary and tone your site already uses (informal tú in Spanish, vous in French, Sie in German, u in Dutch, informal in Polish/Swedish/Norwegian), so these read as the same voice as the rest of the site. A last read by someone who lives in each language is still good practice for marketing copy, but nothing here is a guess at your terminology.

## 1. Only 7 labels are new

| English | es | fr | de | ru | ar | nl | pl | sv | no |
|---|---|---|---|---|---|---|---|---|---|
| Map | Mapa | Carte | Karte | Карта | الخريطة | Kaart | Mapa | Karta | Kart |
| List | Lista | Liste | Liste | Список | قائمة | Lijst | Lista | Lista | Liste |
| Filters | Filtros | Filtres | Filter | Фильтры | الفلاتر | Filters | Filtry | Filter | Filtre |
| More filters | Más filtros | Plus de filtres | Weitere Filter | Ещё фильтры | المزيد من الفلاتر | Meer filters | Więcej filtrów | Fler filter | Flere filtre |
| Draw your area | Dibuja tu zona | Dessinez votre zone | Gebiet einzeichnen | Нарисовать область | ارسم منطقتك | Teken uw gebied | Narysuj obszar | Rita ditt område | Tegn ditt område |
| Show {n} developments (2 or more) | Ver {n} promociones | Voir {n} programmes | {n} Projekte anzeigen | Показать новостройки ({n}) | عرض المشاريع ({n}) | {n} projecten tonen | Pokaż inwestycje ({n}) | Visa {n} projekt | Vis {n} prosjekter |
| Show 1 development | Ver 1 promoción | Voir 1 programme | 1 Projekt anzeigen | Показать новостройки (1) | عرض المشاريع (1) | 1 project tonen | Pokaż inwestycje (1) | Visa 1 projekt | Vis 1 prosjekt |

Choices worth knowing:
- **List, not Grid.** Property portals in all nine markets label the two views List and Map, so the toggle follows that.
- **Show {n} developments** uses your own word for developments in each language (promociones, programmes, Projekte, новостройки, المشاريع, projecten, inwestycje, projekt, prosjekter), matching Explore Developments and Current Developments.
- **Russian, Polish and Arabic** put the number in brackets. These languages change the word after a number (1 / 2-4 / 5+), so a bracketed number is always correct without extra rules. Your site already does this (for example the Russian and Arabic view-all buttons). The other six need the two forms above, one for 1 and one for 2 or more.

## 2. Everything else reuses your existing translations (nothing new to translate)

Search, Location, Property Type, Price Range, Bedrooms, Any, All Locations, All Types, Any Status, Any Timing, Off-Plan, Under Construction, Completed, Ready Now, Within 1 Year, Within 2 Years, 2+ Years, Filter by Lifestyle and all lifestyle tags, Reset Filters, Sort and the sort options (Recommended order, Newest release, Price: low to high, Price: high to low, Completion soonest), the AI search placeholder and the 7 example chips, the results count line, Delivery, Homes, Available, Explore Project, From, Price on request, Current Release, N of M left, bedroom and quarter formats, the no-results text (No homes match these filters. / Try fewer filters...), Speak With Advisor.

## 3. Rules for the build

- Keep the Arabic rules you already have: no uppercase, no letter-spacing on labels, Cairo for card names, arrows mirrored.
- Wrap numeric ranges and prices in a left-to-right element in Arabic, otherwise a range like 154-306 can display reversed.
- The map itself does not mirror in Arabic (geography stays as it is); its buttons and cards do.
- Quarter formats follow your CLAUDE.md: T4 (es, fr), Q4 (de), K4 (nl, sv, no), 4 кв. (ru), IV kw. (pl), الربع الرابع (ar).
