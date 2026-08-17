/* Builds the project location map from the data the page carries in
   data-locmap. Leaflet supplies real OSM geometry -- a hand-drawn coastline or a
   110m world atlas puts Marbella inland, which is useless at project scale.

   Each map is built only when it scrolls into view. Building several at once
   trips OSM's rate limit, which serves a white "Access blocked" tile straight
   into the middle of the design. */
(function () {
  'use strict';

  var TILE_URL = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
  var ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

  function buildMap(host) {
    if (host.dataset.locmapReady === '1') return;
    var payload;
    try {
      payload = JSON.parse(host.dataset.locmap);
    } catch (error) {
      return;
    }
    if (!payload || !payload.site || typeof L === 'undefined') return;
    host.dataset.locmapReady = '1';

    var map = L.map(host, {
      zoomControl: false,
      dragging: false,
      scrollWheelZoom: false,
      doubleClickZoom: false,
      boxZoom: false,
      keyboard: false,
      touchZoom: false,
      attributionControl: true,
      /* Required. With fade animation on, tiles can stay at opacity:0 forever
         when fitBounds runs synchronously right after the layer is created. */
      fadeAnimation: false
    });

    L.tileLayer(TILE_URL, {
      attribution: ATTRIBUTION,
      maxZoom: 19,
      className: 'locmap-tiles',
      crossOrigin: 'anonymous'
    }).addTo(map);

    /* Land reads sage green and the sea stays blue: a multiply veil over the
       tiles, then a cream lift that quiets OSM's own labels without hiding
       them. The sea is never tinted separately. */
    ['locmap-veil', 'locmap-veil-2'].forEach(function (className) {
      var veil = document.createElement('div');
      veil.className = className;
      host.appendChild(veil);
    });

    var site = payload.site;
    var bounds = [site, payload.sea];
    payload.labels.forEach(function (label) { bounds.push(label.ll); });

    /* Generous padding keeps every label plate inside the frame; the nudge east
       stops the right-most plate colliding with the edge. */
    map.fitBounds(L.latLngBounds(bounds), { padding: [118, 55], animate: false });
    map.panBy([15, 0], { animate: false });

    L.marker(site, {
      interactive: false,
      keyboard: false,
      icon: L.divIcon({
        className: 'locmap-pin',
        html: '<span class="locmap-pin-ring"></span><span class="locmap-pin-dot"></span>',
        iconSize: [0, 0],
        iconAnchor: [0, 0]
      })
    }).addTo(map);

    payload.labels.forEach(function (label) {
      var plate = '<span class="locmap-poi-dot' + (label.golf ? ' is-golf' : '') + '"></span>'
        + '<span class="locmap-poi-plate" style="margin-top:' + (label.dy || 0) + 'px">'
        + '<span class="locmap-poi-name"></span>'
        + '<span class="locmap-poi-sub"></span>'
        + '</span>';
      var marker = L.marker(label.ll, {
        interactive: false,
        keyboard: false,
        icon: L.divIcon({
          className: 'locmap-poi is-' + label.side,
          html: plate,
          iconSize: [0, 0],
          iconAnchor: [0, 0]
        })
      }).addTo(map);
      /* Written as text, not interpolated into the HTML above, so a place name
         carrying an apostrophe or an ampersand cannot break out of the markup. */
      var element = marker.getElement();
      if (element) {
        element.querySelector('.locmap-poi-name').textContent = label.name;
        element.querySelector('.locmap-poi-sub').textContent = label.sub;
      }
    });

    if (payload.seaLabel) {
      L.marker(payload.sea, {
        interactive: false,
        keyboard: false,
        icon: L.divIcon({ className: 'locmap-sea', html: '<span></span>', iconSize: [0, 0], iconAnchor: [0, 0] })
      }).addTo(map).getElement().querySelector('span').textContent = payload.seaLabel;
    }

    L.control.scale({ imperial: false, position: 'bottomright' }).addTo(map);
    host.classList.add('is-ready');
  }

  function init() {
    var hosts = [].slice.call(document.querySelectorAll('[data-locmap]'));
    if (!hosts.length) return;

    /* If Leaflet has not finished loading (it is deferred), wait for it rather
       than dropping the map. */
    if (typeof L === 'undefined') {
      window.addEventListener('load', init, { once: true });
      return;
    }

    if (!('IntersectionObserver' in window)) {
      hosts.forEach(buildMap);
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        buildMap(entry.target);
      });
    }, { rootMargin: '200px 0px', threshold: 0.01 });
    hosts.forEach(function (host) { observer.observe(host); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
