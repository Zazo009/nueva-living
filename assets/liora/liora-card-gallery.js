(() => {
  const locale = document.documentElement.getAttribute('lang') || 'en';

  const STRINGS = {
    share: { en: 'Share this project', es: 'Compartir este proyecto', fr: 'Partager ce projet', de: 'Dieses Projekt teilen', ru: 'Поделиться проектом', ar: 'مشاركة هذا المشروع' },
    linkCopied: { en: 'Link copied to clipboard.', es: 'Enlace copiado al portapapeles.', fr: 'Lien copié dans le presse-papiers.', de: 'Link in die Zwischenablage kopiert.', ru: 'Ссылка скопирована в буфер обмена.', ar: 'تم نسخ الرابط.' },
    linkCopyFailed: { en: 'Could not copy the link.', es: 'No se pudo copiar el enlace.', fr: 'Impossible de copier le lien.', de: 'Der Link konnte nicht kopiert werden.', ru: 'Не удалось скопировать ссылку.', ar: 'تعذّر نسخ الرابط.' },
    viewPhotos: { en: 'View all photos', es: 'Ver todas las fotos', fr: 'Voir toutes les photos', de: 'Alle Fotos ansehen', ru: 'Смотреть все фото', ar: 'عرض جميع الصور' },
    close: { en: 'Close', es: 'Cerrar', fr: 'Fermer', de: 'Schließen', ru: 'Закрыть', ar: 'إغلاق' },
    previous: { en: 'Previous image', es: 'Imagen anterior', fr: 'Image précédente', de: 'Vorheriges Bild', ru: 'Предыдущее фото', ar: 'الصورة السابقة' },
    next: { en: 'Next image', es: 'Imagen siguiente', fr: 'Image suivante', de: 'Nächstes Bild', ru: 'Следующее фото', ar: 'الصورة التالية' },
    counter: { en: '{index} of {total}', es: '{index} de {total}', fr: '{index} sur {total}', de: '{index} von {total}', ru: '{index} из {total}', ar: '{index} من {total}' }
  };

  const t = (key, vars) => {
    const entry = STRINGS[key];
    let value = (entry && (entry[locale] || entry.en)) || key;
    if (vars) {
      for (const [name, replacement] of Object.entries(vars)) {
        value = value.replaceAll(`{${name}}`, replacement);
      }
    }
    return value;
  };

  // Distance before a drag is treated as intentional rather than a sloppy tap.
  const AXIS_THRESHOLD = 10;
  // Distance before a drag counts as "change the image" rather than "snap back".
  const COMMIT_RATIO = 0.18;
  const COMMIT_MIN = 45;
  // A press that travels further than this is a swipe, not a click.
  const CLICK_SLOP = 8;

  function toast(message) {
    let node = document.querySelector('[data-shortlist-toast]');
    if (!node) {
      node = document.createElement('div');
      node.className = 'nueva-shortlist-toast';
      node.setAttribute('data-shortlist-toast', '');
      node.setAttribute('role', 'status');
      document.body.appendChild(node);
    }
    node.textContent = message;
    node.classList.add('is-visible');
    window.clearTimeout(node._hideTimer);
    node._hideTimer = window.setTimeout(() => node.classList.remove('is-visible'), 2400);
  }

  async function shareProject(url, name) {
    const absolute = new URL(url, location.href).href;
    if (navigator.share) {
      try {
        await navigator.share({ title: name || document.title, url: absolute });
        return;
      } catch (error) {
        // A cancelled share sheet is a normal outcome, not a failure to report.
        if (error && error.name === 'AbortError') return;
      }
    }
    try {
      await navigator.clipboard.writeText(absolute);
      toast(t('linkCopied'));
      return;
    } catch (error) {
      // The Clipboard API needs a secure context and, in some browsers, a
      // permission the user has not granted. Fall through.
    }
    toast(copyByExecCommand(absolute) ? t('linkCopied') : t('linkCopyFailed'));
  }

  // The pre-Clipboard-API way of copying: still the only thing that works
  // when the page is not on https or the permission is refused.
  function copyByExecCommand(text) {
    const field = document.createElement('textarea');
    field.value = text;
    field.setAttribute('readonly', '');
    field.style.cssText = 'position:fixed;top:0;left:-9999px;opacity:0';
    document.body.appendChild(field);
    field.select();
    let copied = false;
    try {
      copied = document.execCommand('copy');
    } catch (error) {
      copied = false;
    }
    field.remove();
    return copied;
  }

  // ---------- Fullscreen viewer ----------

  const viewer = (() => {
    let root = null;
    let lastFocus = null;
    let observer = null;
    let stack;
    let countEl;
    let titleEl;
    let images = [];

    function build() {
      root = document.createElement('div');
      root.className = 'card-lightbox';
      root.setAttribute('role', 'dialog');
      root.setAttribute('aria-modal', 'true');
      root.hidden = true;
      root.innerHTML = `
        <header class="card-lightbox-bar">
          <span class="card-lightbox-title" data-lightbox-title></span>
          <span class="card-lightbox-count" data-lightbox-count></span>
          <button type="button" class="card-lightbox-close" data-lightbox-close aria-label="${t('close')}">&#10005;</button>
        </header>
        <div class="card-lightbox-stack" data-lightbox-stack></div>`;
      document.body.appendChild(root);

      stack = root.querySelector('[data-lightbox-stack]');
      countEl = root.querySelector('[data-lightbox-count]');
      titleEl = root.querySelector('[data-lightbox-title]');

      root.querySelector('[data-lightbox-close]').addEventListener('click', close);
      document.addEventListener('keydown', (event) => {
        if (!root.hidden && event.key === 'Escape') close();
      });
    }

    function setCount(index) {
      countEl.textContent = t('counter', { index: index + 1, total: images.length });
    }

    function fill() {
      observer?.disconnect();
      stack.textContent = '';

      images.forEach((item, index) => {
        const figure = document.createElement('figure');
        figure.className = 'card-lightbox-item';
        figure.dataset.index = String(index);

        const img = document.createElement('img');
        // WebP where it exists, original as the fallback the browser keeps
        // if it cannot decode the source.
        img.src = item.w || item.s;
        img.alt = item.a || '';
        if (item.w) img.addEventListener('error', () => { img.src = item.s; }, { once: true });
        // Only the first couple are worth fetching eagerly; the rest arrive
        // as they scroll into view, which is why the whole project can ship
        // here without costing anything up front.
        img.loading = index < 2 ? 'eager' : 'lazy';
        img.decoding = 'async';
        figure.appendChild(img);

        if (item.a) {
          const caption = document.createElement('figcaption');
          caption.textContent = item.a;
          figure.appendChild(caption);
        }

        stack.appendChild(figure);
      });

      if ('IntersectionObserver' in window) {
        observer = new IntersectionObserver((entries) => {
          const visible = entries.filter((entry) => entry.isIntersecting);
          if (!visible.length) return;
          visible.sort((a, b) => b.intersectionRatio - a.intersectionRatio);
          setCount(Number(visible[0].target.dataset.index || 0));
        }, { root: stack, threshold: [0.4, 0.75] });
        stack.querySelectorAll('.card-lightbox-item').forEach((el) => observer.observe(el));
      }
    }

    function open(list, startIndex, name) {
      if (!root) build();
      images = list;
      lastFocus = document.activeElement;
      titleEl.textContent = name || '';
      root.hidden = false;
      document.body.classList.add('card-lightbox-open');
      fill();
      setCount(startIndex || 0);
      // Land on the image the card was showing, without animating past the
      // forty above it.
      const target = stack.children[startIndex || 0];
      if (target) stack.scrollTop = target.offsetTop - stack.offsetTop;
      root.querySelector('[data-lightbox-close]').focus();
    }

    function close() {
      if (!root || root.hidden) return;
      observer?.disconnect();
      root.hidden = true;
      stack.textContent = '';
      document.body.classList.remove('card-lightbox-open');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    return { open, close };
  })();

  // ---------- Card galleries ----------

  document.querySelectorAll('[data-project-card-gallery]').forEach((gallery) => {
    const track = gallery.querySelector('[data-gallery-track]');
    const dots = Array.from(gallery.querySelectorAll('[data-gallery-dot]'));
    if (!track) return;

    const slideCount = track.children.length;
    const url = gallery.getAttribute('data-card-url');
    const name = gallery.getAttribute('data-card-name') || '';

    const manifest = gallery.querySelector('template[data-card-images]');
    const images = manifest
      ? Array.from(manifest.content.querySelectorAll('img')).map((img) => ({
          s: img.getAttribute('data-src'),
          w: img.getAttribute('data-webp'),
          a: img.getAttribute('alt') || ''
        }))
      : [];

    // Marks the gallery as script-enhanced; the CSS behind it relaxes the
    // snapping that used to trap vertical gestures.
    gallery.classList.add('is-swipe');

    const slides = Array.from(track.querySelectorAll('img'));

    // Slides past the first sit outside the viewport, so the browser defers
    // them -- and a swipe brings one into view only for the download to start
    // then, which is a blank frame for as long as it takes. Flipping
    // `loading` to eager is not enough on its own: engines do not reliably
    // start an already-deferred fetch when only the attribute changes. So the
    // attribute is removed AND the same candidate the <picture> would choose
    // is fetched separately, which puts it in the HTTP cache; the element
    // then paints from cache the instant it is asked for.
    const warmSlide = (img) => {
      if (!img || img.dataset.warmed === '1') return;
      img.dataset.warmed = '1';
      img.removeAttribute('loading');

      const picture = img.closest('picture');
      const source = picture && picture.querySelector('source[srcset]');
      const preload = new Image();
      if (source) {
        preload.srcset = source.getAttribute('srcset') || '';
        preload.sizes = source.getAttribute('sizes') || '';
      }
      const fallback = img.getAttribute('src');
      if (fallback) preload.src = fallback;
    };

    const ensureLoaded = (target) => {
      for (const i of [target - 1, target, target + 1]) warmSlide(slides[i]);
    };

    // Warm the whole gallery once the card is near the viewport rather than
    // waiting for a swipe: six card-sized WebP files, and only for galleries
    // the visitor actually scrolls to.
    const warmAll = () => slides.forEach(warmSlide);
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        if (!entries.some((entry) => entry.isIntersecting)) return;
        warmAll();
        observer.disconnect();
      }, { rootMargin: '400px' });
      observer.observe(gallery);
    } else {
      warmAll();
    }

    // The browser is better at this than any gesture code I can write. The
    // original bug was never native scrolling -- it was `scroll-snap-type: x
    // mandatory` plus `scroll-snap-stop: always`, which makes the scroller
    // seize any gesture that starts on it and refuse to let go until it lands
    // on the next slide, so a vertical swipe froze the page. With proximity
    // snapping and no snap-stop the browser arbitrates normally: a sideways
    // drag scrolls the strip, a vertical one scrolls the page.
    //
    // Driving it by transform instead meant re-implementing that arbitration
    // in JS, and losing: `touch-action` does not reliably reserve horizontal
    // drags on a real phone, so the swipe died mid-gesture. Everything below
    // now just reads or sets scrollLeft.

    // clientWidth is a layout read. Called from the scroll handler, and
    // interleaved with the dot class writes below, it forced a synchronous
    // reflow on every scroll frame -- 36ms of it by PSI's measurement. The
    // width only changes on resize, so it is cached.
    let cachedSlideWidth = 0;
    const slideWidth = () => {
      if (!cachedSlideWidth) cachedSlideWidth = track.clientWidth || 1;
      return cachedSlideWidth;
    };
    window.addEventListener('resize', () => { cachedSlideWidth = 0; }, { passive: true });

    const currentIndex = () => Math.round(Math.abs(track.scrollLeft) / slideWidth());

    // Only write when the active slide actually changes; rewriting the same
    // classes each scroll frame invalidated layout for no reason.
    let lastActiveDot = -1;
    const setActiveDot = () => {
      const active = currentIndex();
      if (active === lastActiveDot) return;
      lastActiveDot = active;
      dots.forEach((dot, i) => dot.classList.toggle('is-active', i === active));
    };

    // Jumps are instant rather than smooth: `scroll-snap-stop: always` fights
    // a smooth programmatic scroll, and the first click of every pair was
    // being cancelled and snapped back, so arrows and dots only ever took
    // effect on the second press.
    const go = (next) => {
      const target = Math.min(Math.max(next, 0), slideCount - 1);
      ensureLoaded(target);
      track.scrollTo({ left: target * slideWidth(), behavior: 'auto' });
      setActiveDot();
    };

    // One gesture moves one image: `scroll-snap-stop: always` in the CSS
    // stops a fling from coasting over snap points, so no JavaScript has to
    // police the momentum. This listener only keeps the dots honest and warms
    // the neighbours.
    let pressScrollLeft = 0;
    track.addEventListener('pointerdown', () => { pressScrollLeft = track.scrollLeft; }, { passive: true });
    track.addEventListener('touchstart', () => { pressScrollLeft = track.scrollLeft; }, { passive: true });

    let scrollTimer = null;
    track.addEventListener('scroll', () => {
      window.clearTimeout(scrollTimer);
      scrollTimer = window.setTimeout(() => {
        setActiveDot();
        ensureLoaded(currentIndex());
      }, 80);
    }, { passive: true });

    setActiveDot();

    dots.forEach((dot, i) => {
      dot.addEventListener('click', (event) => {
        event.stopPropagation();
        go(i);
      });
    });

    gallery.querySelector('[data-gallery-prev]')?.addEventListener('click', (event) => {
      event.stopPropagation();
      go(currentIndex() - 1);
    });
    gallery.querySelector('[data-gallery-next]')?.addEventListener('click', (event) => {
      event.stopPropagation();
      go(currentIndex() + 1);
    });

    const shareButton = gallery.querySelector('[data-card-share]');
    if (shareButton) {
      shareButton.setAttribute('aria-label', t('share'));
      shareButton.title = t('share');
      shareButton.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        shareProject(url || location.href, name);
      });
    }

    const expandButton = gallery.querySelector('[data-card-expand]');
    if (expandButton) {
      expandButton.setAttribute('aria-label', t('viewPhotos'));
      expandButton.title = t('viewPhotos');
      if (!images.length) expandButton.remove();
      else {
        expandButton.addEventListener('click', (event) => {
          event.preventDefault();
          event.stopPropagation();
          viewer.open(images, currentIndex(), name);
        });
      }
    }

    if (!url) return;
    gallery.addEventListener('click', (event) => {
      // A swipe that ends on the image would otherwise navigate away.
      if (Math.abs(track.scrollLeft - pressScrollLeft) > CLICK_SLOP) {
        event.preventDefault();
        event.stopPropagation();
        return;
      }
      if (event.target.closest('[data-gallery-dot], [data-gallery-prev], [data-gallery-next], .project-card-actions')) return;
      window.location.href = url;
    });
  });
})();
