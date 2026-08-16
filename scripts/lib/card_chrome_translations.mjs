// Translations for the chrome on the unified listing card (lib/project_card.mjs).
//
// These strings used to exist only in the homepage table, because only the
// homepage card had a status badge, a price burned onto the image and the
// lbl/val meta chips. Now every grid on the site renders that card, so the
// same entries have to be applied by the developments, segment and area
// locale builds too -- otherwise those pages would show translated prose
// with an English "Off-Plan" badge and an English "From" over the price.
//
// Each entry is keyed on the class-name prefix that immediately precedes the
// text so it can never match the same words elsewhere in the page.

export const CARD_CHROME_ENTRIES = [
  // Status badge over the image
  { find: 'dev-badge">Completed, Ready To Move In', es: 'dev-badge">Finalizado, Listo para Entrar', fr: 'dev-badge">Terminé, Prêt à Emménager', de: 'dev-badge">Fertiggestellt, Bezugsfertig', ru: 'dev-badge">Завершено, Готово к Заселению', ar: 'dev-badge">مكتمل، جاهز للسكن' },
  { find: 'dev-badge">Current Release', es: 'dev-badge">Fase Actual', fr: 'dev-badge">Phase Actuelle', de: 'dev-badge">Aktuelle Phase', ru: 'dev-badge">Текущая Очередь', ar: 'dev-badge">المرحلة الحالية' },
  { find: 'dev-badge">Off-plan, Private Availability', es: 'dev-badge">Sobre Plano, Disponibilidad Privada', fr: 'dev-badge">Sur Plan, Disponibilité Privée', de: 'dev-badge">Off-Plan, Private Verfügbarkeit', ru: 'dev-badge">На Этапе Строительства, Закрытая Продажа', ar: 'dev-badge">على المخطط، إتاحة حصرية' },
  { find: 'dev-badge">Off-Plan', es: 'dev-badge">Sobre Plano', fr: 'dev-badge">Sur Plan', de: 'dev-badge">Off-Plan', ru: 'dev-badge">На Этапе Строительства', ar: 'dev-badge">على المخطط' },
  { find: 'dev-badge">Sea View Collection', es: 'dev-badge">Colección con Vistas al Mar', fr: 'dev-badge">Collection Vue Mer', de: 'dev-badge">Kollektion mit Meerblick', ru: 'dev-badge">Коллекция с Видом на Море', ar: 'dev-badge">مجموعة بإطلالة على البحر' },
  { find: 'dev-badge">Under Construction', es: 'dev-badge">En Construcción', fr: 'dev-badge">En Construction', de: 'dev-badge">Im Bau', ru: 'dev-badge">В Стадии Строительства', ar: 'dev-badge">قيد الإنشاء' },

  // "From EUR 1,250,000" burned onto the bottom corner of the image
  { find: 'dev-price-overlay">From ', es: 'dev-price-overlay">Desde ', fr: 'dev-price-overlay">À partir de ', de: 'dev-price-overlay">Ab ', ru: 'dev-price-overlay">От ', ar: 'dev-price-overlay">ابتداءً من ' },

  // Meta chips
  { find: '"lbl">Delivery<', es: '"lbl">Entrega<', fr: '"lbl">Livraison<', de: '"lbl">Übergabe<', ru: '"lbl">Сдача<', ar: '"lbl">التسليم<' },
  { find: '"lbl">From<', es: '"lbl">Desde<', fr: '"lbl">À Partir de<', de: '"lbl">Ab<', ru: '"lbl">От<', ar: '"lbl">ابتداءً من<' },
  { find: '"lbl">Status<', es: '"lbl">Estado<', fr: '"lbl">Statut<', de: '"lbl">Status<', ru: '"lbl">Статус<', ar: '"lbl">الحالة<' },
  { find: '"lbl">Type<', es: '"lbl">Tipo<', fr: '"lbl">Type<', de: '"lbl">Typ<', ru: '"lbl">Тип<', ar: '"lbl">النوع<' },
  { find: '"val">Completed<', es: '"val">Finalizado<', fr: '"val">Terminé<', de: '"val">Fertiggestellt<', ru: '"val">Завершено<', ar: '"val">مكتمل<' },
  { find: '"val">Current release<', es: '"val">Fase actual<', fr: '"val">Phase actuelle<', de: '"val">Aktuelle Phase<', ru: '"val">Текущая очередь<', ar: '"val">المرحلة الحالية<' },
  { find: '"val">Under construction<', es: '"val">En construcción<', fr: '"val">En construction<', de: '"val">Im Bau<', ru: '"val">В стадии строительства<', ar: '"val">قيد الإنشاء<' },
  { find: '"val">On request<', es: '"val">Bajo consulta<', fr: '"val">Sur demande<', de: '"val">Auf Anfrage<', ru: '"val">По запросу<', ar: '"val">عند الطلب<' },

  // CTA -- the card says "Explore Project" everywhere now (the homepage used
  // to say "Discover Project"). Keyed on the closing tag so it cannot match
  // the same words in body copy.
  { find: '>Explore Project</a>', es: '>Explorar Proyecto</a>', fr: '>Découvrir le Projet</a>', de: '>Projekt Entdecken</a>', ru: '>Смотреть Проект</a>', ar: '>استكشاف المشروع</a>' }
];
