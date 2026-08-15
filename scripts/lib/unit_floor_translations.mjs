// Availability-table `unit.floor` values. These are a small, closed set of
// data strings (~30 distinct values across all 13 projects), so they are
// translated by exact match rather than parsed. Anything not listed here
// passes through unchanged -- including values already authored in Spanish
// in the source data ("Bloque 3"), which are left exactly as the developer
// supplied them.
export const UNIT_FLOORS = {
  'Ground Floor': { es: 'Planta Baja', fr: 'Rez-de-chaussée', de: 'Erdgeschoss', ru: 'Первый этаж', ar: 'الطابق الأرضي' },
  'Ground floor': { es: 'Planta baja', fr: 'Rez-de-chaussée', de: 'Erdgeschoss', ru: 'Первый этаж', ar: 'الطابق الأرضي' },
  'First floor': { es: 'Primera planta', fr: 'Premier étage', de: 'Erstes Obergeschoss', ru: 'Второй этаж', ar: 'الطابق الأول' },
  '1st Floor': { es: '1.ª Planta', fr: '1er Étage', de: '1. Obergeschoss', ru: '2-й этаж', ar: 'الطابق الأول' },
  'Second floor': { es: 'Segunda planta', fr: 'Deuxième étage', de: 'Zweites Obergeschoss', ru: 'Третий этаж', ar: 'الطابق الثاني' },
  '2nd Floor': { es: '2.ª Planta', fr: '2e Étage', de: '2. Obergeschoss', ru: '3-й этаж', ar: 'الطابق الثاني' },
  'Third floor': { es: 'Tercera planta', fr: 'Troisième étage', de: 'Drittes Obergeschoss', ru: 'Четвёртый этаж', ar: 'الطابق الثالث' },
  'Fourth floor': { es: 'Cuarta planta', fr: 'Quatrième étage', de: 'Viertes Obergeschoss', ru: 'Пятый этаж', ar: 'الطابق الرابع' },
  '4th Floor': { es: '4.ª Planta', fr: '4e Étage', de: '4. Obergeschoss', ru: '5-й этаж', ar: 'الطابق الرابع' },
  'Penthouse': { es: 'Ático', fr: 'Penthouse', de: 'Penthouse', ru: 'Пентхаус', ar: 'بنتهاوس' },
  'Basement, Ground & First Floor': { es: 'Sótano, planta baja y primera planta', fr: 'Sous-sol, rez-de-chaussée et premier étage', de: 'Untergeschoss, Erdgeschoss und erstes Obergeschoss', ru: 'Цокольный, первый и второй этажи', ar: 'الطابق السفلي والأرضي والأول' },
  'Block 1 (Palm Tree)': { es: 'Bloque 1 (Palmera)', fr: 'Bloc 1 (Palmier)', de: 'Block 1 (Palme)', ru: 'Корпус 1 (Пальма)', ar: 'المبنى 1 (النخلة)' },
  'Block 2 (Olive Tree)': { es: 'Bloque 2 (Olivo)', fr: 'Bloc 2 (Olivier)', de: 'Block 2 (Olivenbaum)', ru: 'Корпус 2 (Олива)', ar: 'المبنى 2 (شجرة الزيتون)' },
  'Block 1, Ground Floor': { es: 'Bloque 1, planta baja', fr: 'Bloc 1, rez-de-chaussée', de: 'Block 1, Erdgeschoss', ru: 'Корпус 1, первый этаж', ar: 'المبنى 1، الطابق الأرضي' },
  'Block 2, Ground Floor': { es: 'Bloque 2, planta baja', fr: 'Bloc 2, rez-de-chaussée', de: 'Block 2, Erdgeschoss', ru: 'Корпус 2, первый этаж', ar: 'المبنى 2، الطابق الأرضي' },
  'Block 5, Ground Floor': { es: 'Bloque 5, planta baja', fr: 'Bloc 5, rez-de-chaussée', de: 'Block 5, Erdgeschoss', ru: 'Корпус 5, первый этаж', ar: 'المبنى 5، الطابق الأرضي' },
  'Block 6, Ground Floor': { es: 'Bloque 6, planta baja', fr: 'Bloc 6, rez-de-chaussée', de: 'Block 6, Erdgeschoss', ru: 'Корпус 6, первый этаж', ar: 'المبنى 6، الطابق الأرضي' },
  'Block 2, First Floor': { es: 'Bloque 2, primera planta', fr: 'Bloc 2, premier étage', de: 'Block 2, erstes Obergeschoss', ru: 'Корпус 2, второй этаж', ar: 'المبنى 2، الطابق الأول' },
  'Block 5, First Floor': { es: 'Bloque 5, primera planta', fr: 'Bloc 5, premier étage', de: 'Block 5, erstes Obergeschoss', ru: 'Корпус 5, второй этаж', ar: 'المبنى 5، الطابق الأول' },
  'Block 6, First Floor': { es: 'Bloque 6, primera planta', fr: 'Bloc 6, premier étage', de: 'Block 6, erstes Obergeschoss', ru: 'Корпус 6, второй этаж', ar: 'المبنى 6، الطابق الأول' },
  'Block 1, First Floor Duplex': { es: 'Bloque 1, dúplex en primera planta', fr: 'Bloc 1, duplex au premier étage', de: 'Block 1, Duplex im ersten Obergeschoss', ru: 'Корпус 1, дуплекс на втором этаже', ar: 'المبنى 1، دوبلكس في الطابق الأول' },
  'Block 1, Penthouse Duplex': { es: 'Bloque 1, ático dúplex', fr: 'Bloc 1, penthouse duplex', de: 'Block 1, Duplex-Penthouse', ru: 'Корпус 1, двухуровневый пентхаус', ar: 'المبنى 1، بنتهاوس دوبلكس' },
  'Block 3, Penthouse Duplex': { es: 'Bloque 3, ático dúplex', fr: 'Bloc 3, penthouse duplex', de: 'Block 3, Duplex-Penthouse', ru: 'Корпус 3, двухуровневый пентхаус', ar: 'المبنى 3، بنتهاوس دوبلكس' },
  'Block 5, Penthouse Duplex': { es: 'Bloque 5, ático dúplex', fr: 'Bloc 5, penthouse duplex', de: 'Block 5, Duplex-Penthouse', ru: 'Корпус 5, двухуровневый пентхаус', ar: 'المبنى 5، بنتهاوس دوبلكس' },
  'Block 6, Penthouse Duplex': { es: 'Bloque 6, ático dúplex', fr: 'Bloc 6, penthouse duplex', de: 'Block 6, Duplex-Penthouse', ru: 'Корпус 6, двухуровневый пентхаус', ar: 'المبنى 6، بنتهاوس دوبلكس' },
  'Skyline Duplex Penthouse': { es: 'Ático dúplex Skyline', fr: 'Penthouse duplex Skyline', de: 'Skyline-Duplex-Penthouse', ru: 'Двухуровневый пентхаус Skyline', ar: 'بنتهاوس دوبلكس Skyline' },
  'Garden-Level Duplex': { es: 'Dúplex a nivel de jardín', fr: 'Duplex de plain-pied sur jardin', de: 'Duplex auf Gartenebene', ru: 'Дуплекс на садовом уровне', ar: 'دوبلكس بمستوى الحديقة' }
};
