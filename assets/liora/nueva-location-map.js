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

    /* The card is a still graphic on desktop, where the frame is wide enough to
       hold every label. On a phone the same map is only ~330px across with
       plates up to 143px wide, so it needs to be explorable. */
    var touch = window.matchMedia('(max-width: 960px)').matches
      || (window.matchMedia('(pointer: coarse)').matches);

    var map = L.map(host, {
      zoomControl: touch,
      /* Dragging stays off until the visitor zooms in. One-finger drag on a map
         that fills the width would swallow the page scroll, which is the classic
         way to trap someone mid-page; at the default framing there is nothing to
         pan to anyway. */
      dragging: false,
      scrollWheelZoom: false,
      doubleClickZoom: touch,
      boxZoom: false,
      keyboard: false,
      touchZoom: touch,
      attributionControl: true,
      /* Required. With fade animation on, tiles can stay at opacity:0 forever
         when fitBounds runs synchronously right after the layer is created. */
      fadeAnimation: false
    });
    if (touch) map.zoomControl.setPosition('bottomleft');

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

    /* Generous padding keeps every label plate inside the frame, and the nudge
       east stops the right-most plate colliding with the edge. A phone frame
       cannot carry that padding without shrinking the map to nothing, so it gets
       a tighter frame and the visitor zooms in for detail instead. */
    /* Leaflet padding is [x, y]. A phone frame is ~330px wide against plates up
       to 143px, so the horizontal padding matters far more than on desktop --
       too little and the outermost plates are sliced by the frame edge. */
    map.fitBounds(L.latLngBounds(bounds), { padding: touch ? [76, 28] : [118, 55], animate: false });
    map.panBy([touch ? 0 : 15, 0], { animate: false });

    var baseZoom = map.getZoom();
    var baseCentre = map.getCenter();

    /* Two levels of pull-back below the composed view, so the project can be
       seen against the wider coast on a narrow screen. Below that the frame
       drifts into empty sea and the pin stops meaning anything. */
    map.setMinZoom(baseZoom - 2);
    if (touch) {
      map.on('zoomend', function () {
        /* Panning belongs to the zoomed-in state only: one-finger drag at the
           composed framing would swallow the page scroll for no gain. Coming
           back to or below that framing re-centres and re-locks. */
        if (map.getZoom() > baseZoom) {
          map.dragging.enable();
        } else {
          map.dragging.disable();
          map.setView(baseCentre, map.getZoom(), { animate: false });
        }
      });
    }

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

    /* Under ~420px four plates cannot sit apart from each other. The payload is
       already in priority order (beach, marina, town, golf), so the last one is
       the one to drop. */
    var narrow = window.matchMedia('(max-width: 420px)').matches;
    var labels = narrow ? payload.labels.slice(0, 3) : payload.labels;

    labels.forEach(function (label) {
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

    /* A plate sits on the side its place is on, which is right until the place
       is near the frame edge -- then the frame slices it. On a 330px phone a
       143px plate hung 47px outside. Flipping a plate inward fixes that but can
       drop it on top of a neighbour, so both constraints are resolved together:
       try its own side, then the flipped side, and if neither is clear, hide the
       plate and keep the dot. Half a place name, or two printed over each other,
       is worse than one label fewer. */
    function overlaps(a, b) {
      return a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
    }

    function keepPlatesInFrame() {
      var box = host.getBoundingClientRect();
      var placed = [];
      /* DOM order is the payload's priority order, so when something has to go
         it is the least important label that goes. */
      host.querySelectorAll('.locmap-poi').forEach(function (poi) {
        var plate = poi.querySelector('.locmap-poi-plate');
        if (!plate) return;
        plate.style.visibility = '';

        var fits = function () {
          var rect = plate.getBoundingClientRect();
          if (rect.left < box.left || rect.right > box.right) return null;
          for (var i = 0; i < placed.length; i += 1) {
            if (overlaps(rect, placed[i])) return null;
          }
          return rect;
        };

        var rect = fits();
        if (!rect) {
          poi.classList.toggle('is-left');
          poi.classList.toggle('is-right');
          rect = fits();
          if (!rect) {
            /* Put the side back so the next reflow starts from the geographic
               placement rather than from a rejected flip. */
            poi.classList.toggle('is-left');
            poi.classList.toggle('is-right');
            plate.style.visibility = 'hidden';
            return;
          }
        }
        placed.push(rect);
      });
    }
    requestAnimationFrame(keepPlatesInFrame);
    map.on('zoomend', function () { requestAnimationFrame(keepPlatesInFrame); });

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
