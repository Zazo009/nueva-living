// Building blocks for a unit's floor label.
//
// UNIT_FLOORS enumerates whole strings -- "Block 2, Ground Floor", "Block 5,
// Ground Floor", "Block 6, Ground Floor" -- so every new combination of a
// block number and a level needed its own row, and 139 of the portfolio's 166
// floor values had none. The five earliest locales fell through to English on
// 18 projects as a result.
//
// These are the parts instead. localizedUnitFloor splits a label on commas and
// "&", translates each segment from here, and passes anything it does not
// recognise through untouched -- which is what you want for an identifier like
// "A1" or "(Olive Tree)".
export const FLOOR_PARTS = {
  'ground floor': { es: 'Planta baja', fr: 'Rez-de-chaussée', de: 'Erdgeschoss', ru: 'Первый этаж', ar: 'الطابق الأرضي', nl: 'Begane grond', pl: 'Parter', sv: 'Bottenvåning', no: 'Første etasje' },
  'first floor': { es: 'Planta primera', fr: 'Premier étage', de: 'Erster Stock', ru: 'Второй этаж', ar: 'الطابق الأول', nl: 'Eerste verdieping', pl: 'Pierwsze piętro', sv: 'Första våningen', no: 'Andre etasje' },
  'second floor': { es: 'Planta segunda', fr: 'Deuxième étage', de: 'Zweiter Stock', ru: 'Третий этаж', ar: 'الطابق الثاني', nl: 'Tweede verdieping', pl: 'Drugie piętro', sv: 'Andra våningen', no: 'Tredje etasje' },
  'third floor': { es: 'Planta tercera', fr: 'Troisième étage', de: 'Dritter Stock', ru: 'Четвёртый этаж', ar: 'الطابق الثالث', nl: 'Derde verdieping', pl: 'Trzecie piętro', sv: 'Tredje våningen', no: 'Fjerde etasje' },
  'fourth floor': { es: 'Planta cuarta', fr: 'Quatrième étage', de: 'Vierter Stock', ru: 'Пятый этаж', ar: 'الطابق الرابع', nl: 'Vierde verdieping', pl: 'Czwarte piętro', sv: 'Fjärde våningen', no: 'Femte etasje' },
  'semi-basement': { es: 'Semisótano', fr: 'Demi-sous-sol', de: 'Souterrain', ru: 'Цокольный этаж', ar: 'شبه قبو', nl: 'Souterrain', pl: 'Półsuterena', sv: 'Souterräng', no: 'Underetasje' },
  'garden': { es: 'Jardín', fr: 'Jardin', de: 'Garten', ru: 'Сад', ar: 'حديقة', nl: 'Tuin', pl: 'Ogród', sv: 'Trädgård', no: 'Hage' },
  'garden level': { es: 'Planta jardín', fr: 'Niveau jardin', de: 'Gartenebene', ru: 'Садовый уровень', ar: 'مستوى الحديقة', nl: 'Tuinniveau', pl: 'Poziom ogrodu', sv: 'Trädgårdsplan', no: 'Hagenivå' },
  'solarium': { es: 'Solárium', fr: 'Solarium', de: 'Solarium', ru: 'Солярий', ar: 'سولاريوم', nl: 'Solarium', pl: 'Solarium', sv: 'Solterrass', no: 'Solterrasse' },
  'penthouse': { es: 'Ático', fr: 'Penthouse', de: 'Penthaus', ru: 'Пентхаус', ar: 'بنتهاوس', nl: 'Penthouse', pl: 'Penthouse', sv: 'Takvåning', no: 'Toppleilighet' },
  'duplex penthouse': { es: 'Ático dúplex', fr: 'Penthouse duplex', de: 'Maisonette-Penthaus', ru: 'Двухуровневый пентхаус', ar: 'بنتهاوس دوبلكس', nl: 'Duplex penthouse', pl: 'Penthouse dwupoziomowy', sv: 'Duplex-takvåning', no: 'Duplex-toppleilighet' },
  'south building': { es: 'Edificio sur', fr: 'Bâtiment sud', de: 'Südgebäude', ru: 'Южный корпус', ar: 'المبنى الجنوبي', nl: 'Zuidgebouw', pl: 'Budynek południowy', sv: 'Södra huset', no: 'Sørbygget' },
  'north building': { es: 'Edificio norte', fr: 'Bâtiment nord', de: 'Nordgebäude', ru: 'Северный корпус', ar: 'المبنى الشمالي', nl: 'Noordgebouw', pl: 'Budynek północny', sv: 'Norra huset', no: 'Nordbygget' },
  'townhouse block': { es: 'Bloque de adosados', fr: 'Îlot de maisons de ville', de: 'Reihenhauszeile', ru: 'Блок таунхаусов', ar: 'مجموعة منازل متلاصقة', nl: 'Rij herenhuizen', pl: 'Zespół domów szeregowych', sv: 'Radhuslänga', no: 'Rekkehusrekke' },
  'premium villa': { es: 'Villa Premium', fr: 'Villa Premium', de: 'Premium-Villa', ru: 'Вилла Premium', ar: 'فيلا بريميوم', nl: 'Premium villa', pl: 'Willa Premium', sv: 'Premium-villa', no: 'Premium-villa' },
  'deluxe villa': { es: 'Villa Deluxe', fr: 'Villa Deluxe', de: 'Deluxe-Villa', ru: 'Вилла Deluxe', ar: 'فيلا ديلوكس', nl: 'Deluxe villa', pl: 'Willa Deluxe', sv: 'Deluxe-villa', no: 'Deluxe-villa' },
  'superior villa': { es: 'Villa Superior', fr: 'Villa Supérieure', de: 'Superior-Villa', ru: 'Вилла Superior', ar: 'فيلا سوبيريور', nl: 'Superior villa', pl: 'Willa Superior', sv: 'Superior-villa', no: 'Superior-villa' },
  'semi-detached villa': { es: 'Villa pareada', fr: 'Villa jumelée', de: 'Doppelhaushälfte', ru: 'Спаренная вилла', ar: 'فيلا شبه منفصلة', nl: 'Halfvrijstaande villa', pl: 'Willa bliźniacza', sv: 'Parhusvilla', no: 'Tomannsvilla' },
  'ground floor sky villa': { es: 'Sky Villa en planta baja', fr: 'Sky Villa au rez-de-chaussée', de: 'Sky Villa im Erdgeschoss', ru: 'Sky Villa на первом этаже', ar: 'سكاي فيلا في الطابق الأرضي', nl: 'Sky Villa op de begane grond', pl: 'Sky Villa na parterze', sv: 'Sky Villa på bottenvåningen', no: 'Sky Villa i første etasje' },
  'penthouse sky villa': { es: 'Sky Villa ático', fr: 'Sky Villa penthouse', de: 'Sky Villa Penthaus', ru: 'Sky Villa пентхаус', ar: 'سكاي فيلا بنتهاوس', nl: 'Sky Villa penthouse', pl: 'Sky Villa penthouse', sv: 'Sky Villa takvåning', no: 'Sky Villa toppleilighet' },
  'ground and first floor': { es: 'Planta baja y primera', fr: 'Rez-de-chaussée et premier étage', de: 'Erd- und Obergeschoss', ru: 'Первый и второй этаж', ar: 'الطابق الأرضي والأول', nl: 'Begane grond en eerste verdieping', pl: 'Parter i pierwsze piętro', sv: 'Botten- och första våningen', no: 'Første og andre etasje' }
};

// Words that take an identifier after them: "Block 4", "Building A1",
// "Portal 2", "Level 3". The identifier is never translated.
export const FLOOR_PREFIXES = {
  block: { es: 'Bloque', fr: 'Bloc', de: 'Block', ru: 'Блок', ar: 'مبنى', nl: 'Blok', pl: 'Blok', sv: 'Hus', no: 'Hus' },
  bloque: { es: 'Bloque', fr: 'Bloc', de: 'Block', ru: 'Блок', ar: 'مبنى', nl: 'Blok', pl: 'Blok', sv: 'Hus', no: 'Hus' },
  building: { es: 'Edificio', fr: 'Bâtiment', de: 'Gebäude', ru: 'Корпус', ar: 'مبنى', nl: 'Gebouw', pl: 'Budynek', sv: 'Byggnad', no: 'Bygg' },
  portal: { es: 'Portal', fr: 'Cage', de: 'Aufgang', ru: 'Подъезд', ar: 'مدخل', nl: 'Portiek', pl: 'Klatka', sv: 'Uppgång', no: 'Oppgang' },
  level: { es: 'Nivel', fr: 'Niveau', de: 'Ebene', ru: 'Уровень', ar: 'مستوى', nl: 'Niveau', pl: 'Poziom', sv: 'Plan', no: 'Plan' },
  townhouse: { es: 'Adosado', fr: 'Maison de ville', de: 'Reihenhaus', ru: 'Таунхаус', ar: 'منزل متلاصق', nl: 'Herenhuis', pl: 'Dom szeregowy', sv: 'Radhus', no: 'Rekkehus' },
  floor: { es: 'Planta', fr: 'Étage', de: 'Etage', ru: 'Этаж', ar: 'الطابق', nl: 'Verdieping', pl: 'Piętro', sv: 'Våning', no: 'Etasje' }
};
