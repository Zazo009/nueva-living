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

    let index = 0;
    // The native scroll container stays in the markup so the gallery still
    // works with no JS. Once we take over we turn scrolling off entirely and
    // move a transform instead: a horizontally scrollable element is exactly
    // what was swallowing vertical swipes, and `touch-action` alone did not
    // reliably stop it on real phones.
    gallery.classList.add('is-swipe');

    // Track width and writing direction were read on every paint -- so once per
    // gallery at startup, immediately after a class had just been written, and
    // again on every single pointermove of a drag. Reading layout after a write
    // forces the browser to reflow synchronously; with fourteen galleries on
    // the developments page that was the largest blocking cost on the page.
    // Measure once, reuse, and drop the cache when the viewport changes.
    //
    // In an RTL page the flex row lays the slides out right-to-left: slide 0
    // sits at the right edge and the rest run leftwards. Translating by a
    // negative offset there walks off the end of the track and lands on blank
    // space, so the sign of the base offset follows the writing direction.
    let metrics = null;
    const measure = () => {
      metrics = {
        width: track.clientWidth || 1,
        axis: getComputedStyle(track).direction === 'rtl' ? 1 : -1
      };
      return metrics;
    };
    const readMetrics = () => metrics || measure();

    const paint = (offset, animate) => {
      track.style.transition = animate ? 'transform 320ms cubic-bezier(0.22, 0.61, 0.36, 1)' : 'none';
      // Resting on the first slide is always zero, whatever the width or the
      // writing direction -- so startup needs no measurement at all.
      if (!index && !offset) {
        track.style.transform = 'translate3d(0px, 0, 0)';
        return;
      }
      const { width, axis } = readMetrics();
      track.style.transform = `translate3d(${axis * index * width + (offset || 0)}px, 0, 0)`;
    };

    const setActiveDot = () => {
      dots.forEach((dot, i) => dot.classList.toggle('is-active', i === index));
    };

    // Every slide ships `loading="lazy"`, which worked while the track was a
    // native scroller: the slides sat inside a scrollable box and the browser
    // fetched them as they came near. Driving the track with a transform under
    // `overflow: hidden` puts them outside the clip box instead, where that
    // heuristic never fires -- so slides three onward stayed at zero bytes and
    // swiping past the second image landed on an empty frame. Promote the
    // neighbours by hand: switching `loading` back to eager starts the fetch.
    const slides = Array.from(track.querySelectorAll('img'));
    const ensureLoaded = (target) => {
      for (const i of [target - 1, target, target + 1]) {
        const img = slides[i];
        if (img && img.loading === 'lazy') img.loading = 'eager';
      }
    };

    const go = (next, animate = true) => {
      index = Math.min(Math.max(next, 0), slideCount - 1);
      ensureLoaded(index);
      paint(0, animate);
      setActiveDot();
    };

    go(0, false);
    window.addEventListener('resize', () => {
      metrics = null;
      paint(0, false);
    });

    let startX = 0;
    let startY = 0;
    let axis = null;
    let travelled = 0;
    let pointerId = null;

    track.addEventListener('pointerdown', (event) => {
      if (!event.isPrimary || slideCount < 2) return;
      startX = event.clientX;
      startY = event.clientY;
      axis = null;
      travelled = 0;
      pointerId = event.pointerId;
      // A drag could go either way, so warm both neighbours as it begins.
      ensureLoaded(index);
    });

    track.addEventListener('pointermove', (event) => {
      if (pointerId !== event.pointerId) return;
      const dx = event.clientX - startX;
      const dy = event.clientY - startY;
      travelled = Math.max(travelled, Math.abs(dx), Math.abs(dy));

      if (axis === null) {
        if (Math.max(Math.abs(dx), Math.abs(dy)) < AXIS_THRESHOLD) return;
        // Vertical intent: let go completely. The page scrolls, the image
        // does not move, and nothing about this gesture is ours any more.
        axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
        if (axis === 'y') {
          pointerId = null;
          return;
        }
        // Throws if the pointer has already been released mid-gesture.
        try {
          track.setPointerCapture(event.pointerId);
        } catch (error) {
          /* capture is an optimisation, not a requirement */
        }
      }

      if (axis === 'x') {
        event.preventDefault();
        paint(dx, false);
      }
    });

    const finish = (event) => {
      if (pointerId !== event.pointerId) return;
      const dx = event.clientX - startX;
      pointerId = null;
      if (axis !== 'x') return;
      // Named apart from the gesture's `axis` above: destructuring a second
      // `axis` into this block put the first one in the temporal dead zone,
      // so every release threw and the track stayed stranded between slides.
      const { width: trackWidth, axis: trackAxis } = readMetrics();
      const commit = Math.abs(dx) > Math.max(trackWidth * COMMIT_RATIO, COMMIT_MIN);
      // Dragging content away from the reading direction advances: leftwards
      // in LTR, rightwards in RTL, which is what the native scroller did.
      go(commit ? index + (dx * trackAxis > 0 ? 1 : -1) : index);
    };

    track.addEventListener('pointerup', finish);
    track.addEventListener('pointercancel', (event) => {
      if (pointerId !== event.pointerId) return;
      pointerId = null;
      if (axis === 'x') go(index);
    });

    dots.forEach((dot, i) => {
      dot.addEventListener('click', (event) => {
        event.stopPropagation();
        go(i);
      });
    });

    gallery.querySelector('[data-gallery-prev]')?.addEventListener('click', (event) => {
      event.stopPropagation();
      go(index - 1);
    });
    gallery.querySelector('[data-gallery-next]')?.addEventListener('click', (event) => {
      event.stopPropagation();
      go(index + 1);
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
          viewer.open(images, index, name);
        });
      }
    }

    if (!url) return;
    gallery.addEventListener('click', (event) => {
      // A swipe that ends on the image would otherwise navigate away.
      if (travelled > CLICK_SLOP) {
        event.preventDefault();
        event.stopPropagation();
        travelled = 0;
        return;
      }
      if (event.target.closest('[data-gallery-dot], [data-gallery-prev], [data-gallery-next], .project-card-actions')) return;
      window.location.href = url;
    });
  });
})();
