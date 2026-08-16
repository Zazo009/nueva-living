(() => {
  const storageKey = 'nueva-living-shortlist-v1';
  const projectPathPattern = /property-[a-z0-9-]+(?:\.html)?/i;
  let savedProjects = readShortlist();
  let previousFocus = null;
  let toastTimer = 0;
  let renderedCount = null;

  const locale = document.documentElement.getAttribute('lang') || 'en';

  // Locale pages carry <base href="../">, so a bare "developments.html"
  // written from JS resolves to the ENGLISH page and silently drops the
  // reader out of their language. Prefix links injected at runtime with the
  // locale directory, mirroring what the build does for server-rendered
  // markup. Derived from the URL rather than <html lang> so it stays right
  // even if the two ever disagree.
  const LOCALE_DIRS = ['es', 'fr', 'de', 'ru', 'ar'];
  const localeDir = LOCALE_DIRS.find((dir) => location.pathname.startsWith('/' + dir + '/')) || '';
  const localeHref = (page) => (localeDir ? localeDir + '/' + page : page);
  const STRINGS = {
    saveProject: { en: 'Save Project', es: 'Guardar Proyecto', fr: 'Enregistrer le Projet', de: 'Projekt Speichern', ru: 'Сохранить проект', ar: 'حفظ المشروع' },
    savedToShortlist: { en: 'Saved to Shortlist', es: 'Guardado en tu Lista', fr: 'Enregistré dans la Liste', de: 'Zur Merkliste hinzugefügt', ru: 'Сохранено в списке', ar: 'تم الحفظ في القائمة' },
    removeFromShortlistTitle: { en: 'Remove from shortlist', es: 'Quitar de la lista', fr: 'Retirer de la liste', de: 'Von der Merkliste entfernen', ru: 'Удалить из списка', ar: 'إزالة من القائمة' },
    saveToShortlistTitle: { en: 'Save to shortlist', es: 'Guardar en la lista', fr: 'Ajouter à la liste', de: 'Zur Merkliste hinzufügen', ru: 'Сохранить в список', ar: 'حفظ في القائمة' },
    openShortlistTitle: { en: 'Open shortlist', es: 'Abrir lista', fr: 'Ouvrir la liste', de: 'Merkliste öffnen', ru: 'Открыть список', ar: 'فتح القائمة' },
    closeShortlist: { en: 'Close shortlist', es: 'Cerrar lista', fr: 'Fermer la liste', de: 'Merkliste schließen', ru: 'Закрыть список', ar: 'إغلاق القائمة' },
    yourShortlist: { en: 'Your Shortlist', es: 'Tu Lista', fr: 'Votre Liste', de: 'Ihre Merkliste', ru: 'Ваш список', ar: 'قائمتك' },
    savedProjectsTitle: { en: 'Saved Projects', es: 'Proyectos Guardados', fr: 'Projets Enregistrés', de: 'Gespeicherte Projekte', ru: 'Сохранённые проекты', ar: 'المشاريع المحفوظة' },
    viewProject: { en: 'View Project', es: 'Ver Proyecto', fr: 'Voir le Projet', de: 'Projekt Ansehen', ru: 'Смотреть проект', ar: 'عرض المشروع' },
    defaultSelectionLabel: { en: 'Nueva Living selection', es: 'Selección de Nueva Living', fr: 'Sélection Nueva Living', de: 'Nueva Living Auswahl', ru: 'Подборка Nueva Living', ar: 'اختيار Nueva Living' },
    emptyText: {
      en: 'Tap the heart on any project to build a private shortlist you can keep, compare and send to us.',
      es: 'Toca el corazón de cualquier proyecto para crear una lista privada que podrás guardar, comparar y enviarnos.',
      fr: "Appuyez sur le cœur d'un projet pour créer une liste privée que vous pourrez conserver, comparer et nous envoyer.",
      de: 'Tippen Sie auf das Herz eines Projekts, um eine private Merkliste zu erstellen, die Sie speichern, vergleichen und uns senden können.',
      ru: 'Нажмите на сердечко у любого проекта, чтобы создать личный список, который можно сохранить, сравнить и отправить нам.',
      ar: 'اضغط على أيقونة القلب في أي مشروع لإنشاء قائمة خاصة يمكنك حفظها ومقارنتها وإرسالها إلينا.'
    },
    browseDevelopments: { en: 'Browse Developments', es: 'Ver Promociones', fr: 'Voir les Programmes', de: 'Projekte Durchsuchen', ru: 'Смотреть проекты', ar: 'تصفح المشاريع' },
    compareSaved: { en: 'Compare Saved Projects', es: 'Comparar Proyectos Guardados', fr: 'Comparer les Projets Enregistrés', de: 'Gespeicherte Projekte Vergleichen', ru: 'Сравнить сохранённые проекты', ar: 'مقارنة المشاريع المحفوظة' },
    sendYourShortlist: { en: 'Send Your Shortlist', es: 'Enviar tu Lista', fr: 'Envoyer votre Liste', de: 'Merkliste Senden', ru: 'Отправить список', ar: 'إرسال قائمتك' },
    sendShortlistIntro: {
      en: 'Share the projects you saved and we will come back with current availability, useful comparisons and the right next step.',
      es: 'Comparte los proyectos que has guardado y te responderemos con la disponibilidad actual, comparativas útiles y el siguiente paso adecuado.',
      fr: "Partagez les projets que vous avez enregistrés et nous reviendrons vers vous avec la disponibilité actuelle, des comparaisons utiles et la prochaine étape adaptée.",
      de: 'Teilen Sie die von Ihnen gespeicherten Projekte, und wir melden uns mit aktueller Verfügbarkeit, hilfreichen Vergleichen und dem passenden nächsten Schritt.',
      ru: 'Поделитесь сохранёнными проектами, и мы свяжемся с вами, сообщив актуальную доступность, полезные сравнения и следующий шаг.',
      ar: 'شارك المشاريع التي حفظتها وسنعاود التواصل معك بمعلومات التوفر الحالية ومقارنات مفيدة والخطوة التالية المناسبة.'
    },
    firstName: { en: 'First Name', es: 'Nombre', fr: 'Prénom', de: 'Vorname', ru: 'Имя', ar: 'الاسم الأول' },
    lastName: { en: 'Last Name', es: 'Apellidos', fr: 'Nom', de: 'Nachname', ru: 'Фамилия', ar: 'اسم العائلة' },
    email: { en: 'Email', es: 'Correo Electrónico', fr: 'E-mail', de: 'E-Mail', ru: 'Email', ar: 'البريد الإلكتروني' },
    phone: { en: 'Phone / WhatsApp', es: 'Teléfono / WhatsApp', fr: 'Téléphone / WhatsApp', de: 'Telefon / WhatsApp', ru: 'Телефон / WhatsApp', ar: 'الهاتف / واتساب' },
    anythingWeShouldKnow: { en: 'Anything We Should Know?', es: '¿Algo Más que Debamos Saber?', fr: 'Autre Chose à Savoir ?', de: 'Gibt es Etwas, das Wir Wissen Sollten?', ru: 'Что нам стоит знать?', ar: 'هل هناك ما ينبغي أن نعرفه؟' },
    consent: {
      en: 'I agree to be contacted and for my data to be stored.',
      es: 'Acepto ser contactado/a y que mis datos sean almacenados.',
      fr: 'J’accepte d’être contacté(e) et que mes données soient conservées.',
      de: 'Ich stimme zu, kontaktiert zu werden und dass meine Daten gespeichert werden.',
      ru: 'Я согласен(на) на связь со мной и на хранение моих данных.',
      ar: 'أوافق على التواصل معي وعلى تخزين بياناتي.'
    },
    sendShortlistButton: { en: 'Send Shortlist', es: 'Enviar Lista', fr: 'Envoyer la Liste', de: 'Liste Senden', ru: 'Отправить список', ar: 'إرسال القائمة' },
    addedToShortlist: { en: '{name} added to your shortlist.', es: '{name} añadido a tu lista.', fr: '{name} ajouté à votre liste.', de: '{name} zur Merkliste hinzugefügt.', ru: '{name} добавлен в ваш список.', ar: 'تمت إضافة {name} إلى قائمتك.' },
    removedFromShortlist: { en: '{name} removed from your shortlist.', es: '{name} eliminado de tu lista.', fr: '{name} retiré de votre liste.', de: '{name} von der Merkliste entfernt.', ru: '{name} удалён из вашего списка.', ar: 'تمت إزالة {name} من قائمتك.' },
    shortlistMessageIntro: {
      en: 'I would like to discuss my Nueva Living shortlist:',
      es: 'Me gustaría hablar sobre mi lista de Nueva Living:',
      fr: 'J’aimerais discuter de ma liste Nueva Living :',
      de: 'Ich möchte gerne über meine Nueva Living Merkliste sprechen:',
      ru: 'Я хотел(а) бы обсудить свой список Nueva Living:',
      ar: 'أود مناقشة قائمتي في Nueva Living:'
    },
    openShortlistAria: { en: 'Open shortlist ({count} saved)', es: 'Abrir lista ({count} guardados)', fr: 'Ouvrir la liste ({count} enregistrés)', de: 'Merkliste öffnen ({count} gespeichert)', ru: 'Открыть список ({count} сохранено)', ar: 'فتح القائمة ({count} محفوظ)' },
    removeProjectAria: { en: 'Remove {name} from shortlist', es: 'Quitar {name} de la lista', fr: 'Retirer {name} de la liste', de: '{name} von der Merkliste entfernen', ru: 'Удалить {name} из списка', ar: 'إزالة {name} من القائمة' },
    saveProjectAria: { en: 'Save {name} to shortlist', es: 'Guardar {name} en la lista', fr: 'Ajouter {name} à la liste', de: '{name} zur Merkliste hinzufügen', ru: 'Сохранить {name} в список', ar: 'حفظ {name} في القائمة' }
  };

  function t(key, vars) {
    const entry = STRINGS[key];
    let value = (entry && (entry[locale] || entry.en)) || key;
    if (vars) {
      for (const [name, replacement] of Object.entries(vars)) {
        value = value.replaceAll(`{${name}}`, replacement);
      }
    }
    return value;
  }

  function clean(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function normalizedProjectUrl(value) {
    const match = clean(value).match(projectPathPattern);
    return match ? match[0] : '';
  }

  function projectIdFromUrl(value) {
    return normalizedProjectUrl(value)
      .replace(/^property-/, '')
      .replace(/\.html$/i, '');
  }

  function safeProject(project) {
    const url = normalizedProjectUrl(project?.url);
    const id = clean(project?.id) || projectIdFromUrl(url);
    const name = clean(project?.name);
    if (!id || !url || !name) return null;

    return {
      id,
      name,
      url,
      location: clean(project?.location),
      image: clean(project?.image),
      price: clean(project?.price),
      type: clean(project?.type)
    };
  }

  function readShortlist() {
    try {
      const value = JSON.parse(localStorage.getItem(storageKey) || '[]');
      if (!Array.isArray(value)) return [];
      return value.map(safeProject).filter(Boolean).slice(0, 24);
    } catch {
      return [];
    }
  }

  function writeShortlist() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(savedProjects));
    } catch {
      // The shortlist remains usable for this page even if storage is unavailable.
    }
  }

  function heartIcon() {
    return '<svg class="nueva-heart-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78Z"/></svg>';
  }

  function projectFromCard(card) {
    const link = card.querySelector('.project-link[href*="property-"], .dev-cta-link[href*="property-"]');
    const url = normalizedProjectUrl(link?.getAttribute('href') || card.dataset.cardUrl);
    const image = card.querySelector('img');
    const metaValues = [...card.querySelectorAll('.meta strong, .dev-meta-item .val')].map((node) => clean(node.textContent));
    return safeProject({
      id: card.id || projectIdFromUrl(url),
      name: card.dataset.title || card.querySelector('.dev-name, h3, [data-project-name]')?.textContent,
      url,
      location: card.querySelector('.dev-loc, .project-body > .label')?.textContent,
      image: image?.getAttribute('src'),
      // The card carries these explicitly. The redesign replaced the old
      // FROM / TYPE / STATUS grid with Delivery / Homes / Available, so
      // reading the fact columns by index would now save a delivery date
      // as the price. metaValues stays as the fallback so cards rendered
      // before that change still resolve correctly.
      price: card.dataset.cardPrice || metaValues[0],
      type: card.dataset.cardType || metaValues[1]
    });
  }

  function projectFromPage() {
    const name = clean(document.body?.dataset?.projectName);
    const url = normalizedProjectUrl(window.location.pathname);
    if (!name || !url) return null;

    const facts = [...document.querySelectorAll('.hero-fact')];
    const factValue = (label) => facts.find((fact) => clean(fact.querySelector('span')?.textContent).toLowerCase().includes(label))
      ?.querySelector('strong')?.textContent;

    return safeProject({
      id: projectIdFromUrl(url),
      name,
      url,
      location: factValue('location'),
      price: factValue('price'),
      type: factValue('type'),
      image: document.querySelector('.project-hero-img')?.getAttribute('src')
    });
  }

  function isSaved(id) {
    return savedProjects.some((project) => project.id === id);
  }

  function track(eventName, project) {
    window.lioraTrack?.(eventName, {
      shortlist_count: savedProjects.length,
      project: project?.name,
      project_id: project?.id
    });
  }

  function showToast(message) {
    const toast = document.querySelector('[data-shortlist-toast]');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('is-visible');
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => toast.classList.remove('is-visible'), 2400);
  }

  function toggleProject(project) {
    const existingIndex = savedProjects.findIndex((item) => item.id === project.id);
    const added = existingIndex === -1;

    if (added) savedProjects.push(project);
    else savedProjects.splice(existingIndex, 1);

    writeShortlist();
    render();
    showToast(added ? t('addedToShortlist', { name: project.name }) : t('removedFromShortlist', { name: project.name }));
    track(added ? 'shortlist_add' : 'shortlist_remove', project);
  }

  function favoriteButton(project, extraClass = '') {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `nueva-favorite-button ${extraClass}`.trim();
    button.dataset.shortlistId = project.id;
    button.innerHTML = `${heartIcon()}${extraClass ? `<span data-save-project-label>${t('saveProject')}</span>` : ''}`;
    button.addEventListener('pointerdown', (event) => event.stopPropagation());
    button.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      toggleProject(project);
    });
    return button;
  }

  function enhanceProjectCards() {
    document.querySelectorAll('[data-project-card], .dev-card[data-card-url]').forEach((card) => {
      if (card.dataset.shortlistReady === 'true') return;
      const project = projectFromCard(card);
      if (!project) return;

      // The card gallery ships an action cluster (share, fullscreen). When
      // it is there the heart joins it as the first item instead of floating
      // on its own, so the three controls read as one group.
      const cluster = card.querySelector('[data-card-actions]');
      const target = cluster || (card.matches('.dev-card') ? card.querySelector('.dev-img-wrap') : card);
      if (!target) return;
      const button = favoriteButton(project);
      if (cluster) cluster.insertBefore(button, cluster.firstElementChild);
      else target.appendChild(button);
      card.dataset.shortlistReady = 'true';
    });
  }

  function enhanceProjectPage() {
    const project = projectFromPage();
    const actions = document.querySelector('.project-hero .hero-actions');
    if (!project || !actions || actions.querySelector('[data-shortlist-id]')) return;
    actions.appendChild(favoriteButton(project, 'nueva-save-project'));
  }

  function triggerMarkup(className) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `nueva-shortlist-trigger ${className}`;
    button.setAttribute('aria-haspopup', 'dialog');
    button.setAttribute('aria-controls', 'nuevaShortlistDrawer');
    button.setAttribute('aria-label', t('openShortlistAria', { count: 0 }));
    button.title = t('openShortlistTitle');
    button.innerHTML = `${heartIcon()}<span class="nueva-shortlist-count" data-shortlist-count aria-hidden="true">0</span>`;
    button.addEventListener('click', openDrawer);
    return button;
  }

  function enhanceNavigation() {
    const nav = document.querySelector('.site-nav, #nav');
    if (!nav || nav.dataset.shortlistReady === 'true') return;

    const rightLinks = nav.querySelector('.nav-links-right');
    if (rightLinks) {
      const desktopTrigger = triggerMarkup('nueva-shortlist-nav-trigger');
      if (rightLinks.tagName === 'UL') {
        const item = document.createElement('li');
        item.className = 'nueva-shortlist-nav-item';
        item.appendChild(desktopTrigger);
        rightLinks.appendChild(item);
      } else {
        rightLinks.appendChild(desktopTrigger);
      }
    }

    const burger = nav.querySelector('.nav-burger, #burgerBtn');
    const mobileTrigger = triggerMarkup('nueva-shortlist-mobile-trigger');
    if (burger) nav.insertBefore(mobileTrigger, burger);
    else nav.appendChild(mobileTrigger);

    nav.dataset.shortlistReady = 'true';
  }

  function drawerTemplate() {
    const scrim = document.createElement('button');
    scrim.type = 'button';
    scrim.className = 'nueva-shortlist-scrim';
    scrim.dataset.shortlistScrim = '';
    scrim.setAttribute('aria-label', t('closeShortlist'));
    scrim.addEventListener('click', closeDrawer);

    const drawer = document.createElement('aside');
    drawer.className = 'nueva-shortlist-drawer';
    drawer.id = 'nuevaShortlistDrawer';
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-modal', 'true');
    drawer.setAttribute('aria-labelledby', 'nuevaShortlistTitle');
    drawer.setAttribute('aria-hidden', 'true');
    drawer.innerHTML = `
      <header class="nueva-shortlist-head">
        <div>
          <span class="nueva-shortlist-eyebrow">${t('yourShortlist')}</span>
          <h2 class="nueva-shortlist-title" id="nuevaShortlistTitle">${t('savedProjectsTitle')}</h2>
        </div>
        <button class="nueva-shortlist-close" type="button" data-shortlist-close aria-label="${t('closeShortlist')}">&times;</button>
      </header>
      <div class="nueva-shortlist-body" data-shortlist-body></div>`;
    drawer.querySelector('[data-shortlist-close]').addEventListener('click', closeDrawer);
    drawer.addEventListener('keydown', trapFocus);

    const toast = document.createElement('div');
    toast.className = 'nueva-shortlist-toast';
    toast.dataset.shortlistToast = '';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');

    document.body.append(scrim, drawer, toast);
  }

  function shortlistMessage() {
    const lines = savedProjects.map((project, index) => {
      const details = [project.location, project.price].filter(Boolean).join(' | ');
      return `${index + 1}. ${project.name}${details ? ` - ${details}` : ''}`;
    });
    return `${t('shortlistMessageIntro')}\n\n${lines.join('\n')}`;
  }

  function itemMarkup(project) {
    return `
      <li class="nueva-shortlist-item">
        ${project.image
          ? `<img class="nueva-shortlist-item-image" src="${escapeHtml(project.image)}" alt="" width="216" height="162" loading="lazy" decoding="async">`
          : '<span class="nueva-shortlist-item-image" aria-hidden="true"></span>'}
        <div class="nueva-shortlist-item-copy">
          <span>${escapeHtml(project.location || project.type || t('defaultSelectionLabel'))}</span>
          <strong>${escapeHtml(project.name)}</strong>
          <a href="${escapeHtml(project.url)}">${t('viewProject')}</a>
        </div>
        <button class="nueva-shortlist-remove" type="button" data-remove-shortlist="${escapeHtml(project.id)}" aria-label="${escapeHtml(t('removeProjectAria', { name: project.name }))}">
          ${heartIcon()}
        </button>
      </li>`;
  }

  function emptyMarkup() {
    return `
      <div class="nueva-shortlist-empty">
        <span class="nueva-shortlist-empty-icon">${heartIcon()}</span>
        <p>${t('emptyText')}</p>
        <a class="nueva-shortlist-browse" href="${localeHref('developments.html')}">${t('browseDevelopments')}</a>
      </div>`;
  }

  function formMarkup() {
    const names = savedProjects.map((project) => project.name).join(', ');
    return `
      <div class="nueva-shortlist-form-shell">
        <h3>${t('sendYourShortlist')}</h3>
        <p>${t('sendShortlistIntro')}</p>
        <form class="nueva-shortlist-form" name="nueva-shortlist" method="POST" data-crm-lead action="/.netlify/functions/nueva-lead">
          <input type="hidden" name="request_context" value="Nueva Living shortlist: ${escapeHtml(names)}">
          <input type="hidden" name="project" value="${escapeHtml(names)}">
          <div class="nueva-shortlist-field">
            <label for="shortlistFirstName">${t('firstName')}</label>
            <input id="shortlistFirstName" name="first_name" type="text" autocomplete="given-name" required>
          </div>
          <div class="nueva-shortlist-field">
            <label for="shortlistLastName">${t('lastName')}</label>
            <input id="shortlistLastName" name="last_name" type="text" autocomplete="family-name" required>
          </div>
          <div class="nueva-shortlist-field">
            <label for="shortlistEmail">${t('email')}</label>
            <input id="shortlistEmail" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="nueva-shortlist-field">
            <label for="shortlistPhone">${t('phone')}</label>
            <input id="shortlistPhone" name="phone" type="tel" autocomplete="tel">
          </div>
          <div class="nueva-shortlist-field">
            <label for="shortlistMessage">${t('anythingWeShouldKnow')}</label>
            <textarea id="shortlistMessage" name="message">${escapeHtml(shortlistMessage())}</textarea>
          </div>
          <label class="nueva-shortlist-consent">
            <input name="consent" type="checkbox" required>
            <span>${t('consent')}</span>
          </label>
          <button class="nueva-shortlist-submit" type="submit">${t('sendShortlistButton')}</button>
          <span class="form-response" role="status" aria-live="polite"></span>
        </form>
      </div>`;
  }

  function renderDrawer() {
    const body = document.querySelector('[data-shortlist-body]');
    if (!body) return;

    body.innerHTML = savedProjects.length
      ? `<ol class="nueva-shortlist-items">${savedProjects.map(itemMarkup).join('')}</ol>${
          savedProjects.length >= 2 ? `<a class="nueva-shortlist-compare" href="${localeHref('compare.html')}">${t('compareSaved')}</a>` : ''
        }${formMarkup()}`
      : emptyMarkup();

    body.querySelectorAll('[data-remove-shortlist]').forEach((button) => {
      button.addEventListener('click', () => {
        const project = savedProjects.find((item) => item.id === button.dataset.removeShortlist);
        if (project) toggleProject(project);
      });
    });

    const form = body.querySelector('form[data-crm-lead]');
    if (form) {
      window.nuevaRegisterLeadForms?.(body);
      form.addEventListener('submit', () => track('shortlist_send', { name: 'Shortlist' }), { capture: true });
    }
  }

  function updateControls() {
    const count = savedProjects.length;
    const countChanged = renderedCount !== null && renderedCount !== count;

    document.querySelectorAll('[data-shortlist-count]').forEach((node) => {
      node.textContent = String(count);
      const trigger = node.closest('.nueva-shortlist-trigger');
      if (!trigger) return;

      trigger.classList.toggle('has-saved', count > 0);
      trigger.setAttribute('aria-label', t('openShortlistAria', { count }));

      if (countChanged) {
        trigger.classList.remove('is-updated');
        void trigger.offsetWidth;
        trigger.classList.add('is-updated');
        window.setTimeout(() => trigger.classList.remove('is-updated'), 360);
      }
    });
    renderedCount = count;

    document.querySelectorAll('[data-shortlist-id]').forEach((button) => {
      const saved = isSaved(button.dataset.shortlistId);
      const projectName = projectFromPage()?.name || projectFromCard(button.closest('[data-project-card], .dev-card'))?.name || 'project';
      button.classList.toggle('is-saved', saved);
      button.setAttribute('aria-pressed', String(saved));
      button.setAttribute('aria-label', saved ? t('removeProjectAria', { name: projectName }) : t('saveProjectAria', { name: projectName }));
      button.title = saved ? t('removeFromShortlistTitle') : t('saveToShortlistTitle');
      const label = button.querySelector('[data-save-project-label]');
      if (label) label.textContent = saved ? t('savedToShortlist') : t('saveProject');
    });
  }

  function render() {
    updateControls();
    renderDrawer();
  }

  function openDrawer() {
    const drawer = document.getElementById('nuevaShortlistDrawer');
    const scrim = document.querySelector('[data-shortlist-scrim]');
    if (!drawer || !scrim) return;

    previousFocus = document.activeElement;
    renderDrawer();
    drawer.classList.add('is-open');
    scrim.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    document.body.classList.add('nueva-shortlist-open');
    drawer.querySelector('[data-shortlist-close]')?.focus({ preventScroll: true });
    track('shortlist_open');
  }

  function closeDrawer() {
    const drawer = document.getElementById('nuevaShortlistDrawer');
    const scrim = document.querySelector('[data-shortlist-scrim]');
    if (!drawer || !scrim) return;

    drawer.classList.remove('is-open');
    scrim.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('nueva-shortlist-open');
    previousFocus?.focus?.({ preventScroll: true });
  }

  function trapFocus(event) {
    if (event.key === 'Escape') {
      event.preventDefault();
      closeDrawer();
      return;
    }
    if (event.key !== 'Tab') return;

    const focusable = [...event.currentTarget.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled])')]
      .filter((node) => node.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable.at(-1);

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function initialize() {
    drawerTemplate();
    enhanceNavigation();
    enhanceProjectCards();
    enhanceProjectPage();
    render();

    window.addEventListener('storage', (event) => {
      if (event.key !== storageKey) return;
      savedProjects = readShortlist();
      render();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})();
