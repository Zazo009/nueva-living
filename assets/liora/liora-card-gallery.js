(() => {
  document.querySelectorAll('[data-project-card-gallery]').forEach((gallery) => {
    const track = gallery.querySelector('[data-gallery-track]');
    const dots = Array.from(gallery.querySelectorAll('[data-gallery-dot]'));
    if (!track) return;

    const slideCount = track.children.length;

    const currentIndex = () => (track.clientWidth ? Math.round(track.scrollLeft / track.clientWidth) : 0);

    const setActiveDot = () => {
      if (!dots.length || !track.clientWidth) return;
      const index = currentIndex();
      dots.forEach((dot, i) => dot.classList.toggle('is-active', i === index));
    };

    let scrollTimer = null;
    track.addEventListener('scroll', () => {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(setActiveDot, 80);
    }, { passive: true });

    dots.forEach((dot, index) => {
      dot.addEventListener('click', (event) => {
        event.stopPropagation();
        track.scrollTo({ left: index * track.clientWidth, behavior: 'smooth' });
      });
    });

    const prevButton = gallery.querySelector('[data-gallery-prev]');
    const nextButton = gallery.querySelector('[data-gallery-next]');
    const step = (delta) => {
      const target = Math.min(Math.max(currentIndex() + delta, 0), slideCount - 1);
      track.scrollTo({ left: target * track.clientWidth, behavior: 'smooth' });
    };
    prevButton?.addEventListener('click', (event) => {
      event.stopPropagation();
      step(-1);
    });
    nextButton?.addEventListener('click', (event) => {
      event.stopPropagation();
      step(1);
    });

    const url = gallery.getAttribute('data-card-url');
    if (!url) return;
    gallery.addEventListener('click', (event) => {
      if (event.target.closest('[data-gallery-dot]')) return;
      window.location.href = url;
    });
  });
})();
