(() => {
  document.querySelectorAll('[data-project-card-gallery]').forEach((gallery) => {
    const track = gallery.querySelector('[data-gallery-track]');
    const dots = Array.from(gallery.querySelectorAll('[data-gallery-dot]'));
    if (!track) return;

    const setActiveDot = () => {
      if (!dots.length || !track.clientWidth) return;
      const index = Math.round(track.scrollLeft / track.clientWidth);
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

    const url = gallery.getAttribute('data-card-url');
    if (!url) return;
    gallery.addEventListener('click', (event) => {
      if (event.target.closest('[data-gallery-dot]')) return;
      window.location.href = url;
    });
  });
})();
