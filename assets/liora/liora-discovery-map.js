/* Map view of the developments page.

   Loaded only when a visitor asks for the map (see "List / Map toggle" in
   liora-discovery.js). Nothing here, and nothing it fetches, is on the wire
   for a visitor who stays on the list: Leaflet, protomaps-leaflet, their
   stylesheet and the map tiles all start from the first click on "Map".

   Self-hosted end to end. Leaflet and protomaps-leaflet are vendored under
   assets/liora/vendor/ (versions, licences and hashes in VENDOR.json), and the
   base map is a vector PMTiles archive of the Costa del Sol under
   assets/liora/tiles/, read with HTTP range requests and drawn to canvas in
   the visitor's browser. No tile server, no CDN, no third-party request.

   The filtered list stays owned by liora-discovery.js. This file is a second
   renderer of the same result: it reads `bridge.visible` (already filtered,
   already sorted), draws one pin per development, and hands a drawn polygon
   back as one more filter condition (`bridge.setArea`). The cards in the
   result rail are the real cards, left where they are; the rail is the
   accessible equivalent of the map. */
(function () {
  'use strict';

  /* The one place the tile source is named: a vector archive served from this
     site. It is replaced by rebuilding the archive (see assets/liora/vendor/
     VENDOR.json for how this one was made), never by pointing at someone
     else's server; the audit fails if a third-party host appears in this file. */
  var script = document.currentScript;
  var BASE = new URL(script && script.src ? script.src : '/assets/liora/liora-discovery-map.js', document.baseURI);
  var TILES_URL = new URL('tiles/costa-del-sol.pmtiles', BASE).href;
  var ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    + ' &middot; <a href="https://protomaps.com">Protomaps</a>';

  /* Vendored libraries. The hashes are checked by the browser (same-origin
     SRI) and by the audit against VENDOR.json and the files themselves, so a
     file edited by hand stops loading rather than quietly drifting. */
  var LEAFLET_VERSION = '1.9.4';
  var LEAFLET_CSS_SRI = 'sha384-sHL9NAb7lN7rfvG5lfHpm643Xkcjzp4jFvuavGOndn6pjVqS6ny56CAt3nsEVT4H';
  var LEAFLET_JS_SRI = 'sha384-cxOPjt7s7Iz04uaHJceBmS+qpjv2JkIHNVcuOrM+YHwZOmJGBXI00mdUXEq65HTH';
  var PROTOMAPS_VERSION = '5.1.0';
  var PROTOMAPS_JS_SRI = 'sha384-pAKrddYWxjFAIJwatOtmmtq9ebz3ZwluHCEg3pqOMpOporUofLqz/l5hs+0LAWaH';
  var LEAFLET_CSS_URL = new URL('vendor/leaflet/leaflet.css', BASE).href;
  var LEAFLET_JS_URL = new URL('vendor/leaflet/leaflet.js', BASE).href;
  var PROTOMAPS_JS_URL = new URL('vendor/protomaps-leaflet/protomaps-leaflet.js', BASE).href;

  /* Two pins closer than this (in screen pixels) would overlap, so they merge
     into a count bubble. A price pin is about 72 x 32. */
  var CLUSTER_DX = 78;
  var CLUSTER_DY = 46;
  /* The archive holds zoom 0-14. protomaps-leaflet draws a data tile at two
     display zoom levels (it renders the 512px data tile into 256px tiles), so
     15 is native detail, and 16 is one clean 2x vector enlargement: lines and
     labels stay sharp, there is just no further detail to show. */
  var MAX_ZOOM = 16;
  var MIN_ZOOM = 8;
  var DATA_MAX_ZOOM = 14;
  /* The archive's bounding box (south-west, north-east). Outside it there is
     no data, and a tile that straddles the edge would be painted as open sea,
     so everything outside it is covered by a plain ground (see the cover
     below). The view is not clamped to the box: on a phone the canvas is taller
     than the coast, and a clamp would fight the fit that frames the pins. */
  var BOUNDS = [[36.00, -5.75], [37.15, -3.80]];
  var FALLBACK_VIEW = [36.5, -4.95];

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var phone = window.matchMedia('(max-width: 640px)');

  function el(tag, className, attrs) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (attrs) Object.keys(attrs).forEach(function (name) { node.setAttribute(name, attrs[name]); });
    return node;
  }

  function svg(path, size, width) {
    var wrap = document.createElement('span');
    wrap.innerHTML = '<svg aria-hidden="true" width="' + size + '" height="' + size
      + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="' + (width || 1.8)
      + '" stroke-linecap="round" stroke-linejoin="round">' + path + '</svg>';
    return wrap.firstChild;
  }

  var ICON = {
    pen: '<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 7l3 3"/>',
    close: '<path d="M6 6l12 12M18 6L6 18"/>',
    prev: '<path d="M15 6l-6 6 6 6"/>',
    next: '<path d="M9 6l6 6-6 6"/>',
    filters: '<path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/>',
    list: '<path d="M5 7h14M5 12h14M5 17h14"/>',
    pin: '<path d="M12 21s6-5.2 6-10a6 6 0 10-12 0c0 4.8 6 10 6 10z"/><circle cx="12" cy="11" r="2.2"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>'
  };

  function loadStyle(href, integrity) {
    return new Promise(function (resolve, reject) {
      var css = el('link');
      css.rel = 'stylesheet';
      css.href = href;
      css.integrity = integrity;
      css.crossOrigin = 'anonymous';
      css.onload = resolve;
      css.onerror = function () { reject(new Error('Map stylesheet failed to load')); };
      document.head.appendChild(css);
    });
  }

  function loadScript(src, integrity) {
    return new Promise(function (resolve, reject) {
      var tag = el('script');
      tag.src = src;
      tag.integrity = integrity;
      tag.crossOrigin = 'anonymous';
      tag.onload = resolve;
      tag.onerror = function () { reject(new Error('Map library failed to load: ' + src)); };
      document.head.appendChild(tag);
    });
  }

  /* Leaflet is required: without it there is no map and the visitor stays on
     the list. protomaps-leaflet only draws the ground; if it fails the pins
     still work on a plain ground, so its failure is swallowed. */
  function loadLibraries() {
    var leaflet = (window.L && window.L.map)
      ? Promise.resolve()
      : Promise.all([loadStyle(LEAFLET_CSS_URL, LEAFLET_CSS_SRI), loadScript(LEAFLET_JS_URL, LEAFLET_JS_SRI)]);
    return leaflet.then(function () {
      if (window.protomapsL) return null;
      return loadScript(PROTOMAPS_JS_URL, PROTOMAPS_JS_SRI).catch(function () { return null; });
    });
  }

  /* ---- Base map style ------------------------------------------------------

     Drawn from the site palette (cream ground #f7f3ec, the card rule and gold
     tones), not a stock theme: land is the page's own cream, the sea a soft
     blue-grey, roads are tan hairlines that only appear where they help, and
     the only labels are towns and the sea. No points of interest, no shops,
     no transit, no borders: the price pins are the content. */

  var PALETTE = {
    water: '#c8dbe0',
    earth: '#f7f3ec',
    beach: '#f3ead6',
    green: '#eceedf',
    greenDeep: '#e6e9d6',
    built: '#ece5d8',
    roadMinor: '#e8dfce',
    roadMajor: '#dccfb6',
    roadHighway: '#cdbc9a',
    placeLabel: '#5a4e3d',
    placeHalo: '#f7f3ec',
    seaLabel: '#7b97a4'
  };

  function ramp(stops) {
    return function (z) {
      if (z <= stops[0][0]) return stops[0][1];
      for (var i = 1; i < stops.length; i += 1) {
        if (z <= stops[i][0]) {
          var a = stops[i - 1];
          var b = stops[i];
          return a[1] + (b[1] - a[1]) * ((z - a[0]) / (b[0] - a[0]));
        }
      }
      return stops[stops.length - 1][1];
    };
  }

  function basemapRules(P, lang) {
    var flavor = {
      background: PALETTE.water, earth: PALETTE.earth, water: PALETTE.water,
      park_a: PALETTE.green, park_b: PALETTE.green, wood_a: PALETTE.greenDeep, wood_b: PALETTE.greenDeep,
      scrub_a: PALETTE.green, scrub_b: PALETTE.green,
      hospital: PALETTE.earth, industrial: PALETTE.built, school: PALETTE.earth, zoo: PALETTE.green,
      beach: PALETTE.beach, sand: PALETTE.beach, glacier: PALETTE.earth, aerodrome: PALETTE.built,
      pedestrian: PALETTE.earth, pier: PALETTE.built, runway: PALETTE.built,
      buildings: PALETTE.built, major: PALETTE.roadMajor,
      landcover: {
        grassland: PALETTE.green, barren: PALETTE.earth, urban_area: PALETTE.earth,
        farmland: PALETTE.earth, glacier: PALETTE.earth, scrub: PALETTE.green, forest: PALETTE.greenDeep
      }
    };
    function road(kinds, color, stops) {
      return {
        dataLayer: 'roads',
        symbolizer: new P.LineSymbolizer({ color: color, width: ramp(stops), lineCap: 'round', lineJoin: 'round' }),
        filter: function (z, f) { return kinds.indexOf(f.props.kind) >= 0; }
      };
    }
    /* Landuse, water and buildings come from the library's own rules in the
       palette above; roads and boundaries are replaced by the hairlines below. */
    var paint = P.paintRules(flavor).filter(function (rule) {
      return rule.dataLayer !== 'roads' && rule.dataLayer !== 'boundaries';
    });
    paint.push(road(['other', 'path'], PALETTE.roadMinor, [[14, 0], [15, 0.4], [16, 0.8]]));
    paint.push(road(['minor_road'], PALETTE.roadMinor, [[12, 0], [13, 0.4], [14, 0.8], [16, 2]]));
    paint.push(road(['major_road'], PALETTE.roadMajor, [[8, 0], [10, 0.4], [12, 0.7], [14, 1.4], [16, 3]]));
    paint.push(road(['highway'], PALETTE.roadHighway, [[7, 0], [8, 0.5], [11, 0.9], [14, 2], [16, 4]]));

    var family = '"Montserrat", Arial, sans-serif';
    var names = ['name:' + lang, 'name'];
    var labels = [
      {
        dataLayer: 'water',
        symbolizer: new P.CenteredTextSymbolizer({
          labelProps: names, fill: PALETTE.seaLabel, fontFamily: family, fontStyle: 'italic', fontWeight: 400,
          fontSize: ramp([[8, 11], [12, 13]]), letterSpacing: 2, lineHeight: 1.5
        }),
        filter: function (z, f) {
          return f.geomType === P.GeomType.Point && ['sea', 'ocean', 'bay', 'strait'].indexOf(f.props.kind) >= 0;
        }
      },
      {
        dataLayer: 'places',
        minzoom: 9,
        symbolizer: new P.CenteredTextSymbolizer({
          labelProps: names, fill: PALETTE.placeLabel, stroke: PALETTE.placeHalo, width: 2.5,
          fontFamily: family, fontWeight: 500, lineHeight: 1.4,
          fontSize: function (z, f) {
            var detail = f && f.props.kind_detail;
            return detail === 'city' ? 15 : (detail === 'town' ? 13.5 : (detail === 'village' ? 12 : 11));
          }
        }),
        sort: function (a, b) { return (a.min_zoom || 0) - (b.min_zoom || 0); },
        /* Towns from the start, villages once the visitor is in close, hamlets
           only at street level: the map stays quiet until it is asked more. */
        filter: function (z, f) {
          if (f.props.kind !== 'locality') return false;
          var detail = f.props.kind_detail;
          if (detail === 'city' || detail === 'town') return true;
          return detail === 'village' ? z >= 11 : z >= 13;
        }
      },
      {
        dataLayer: 'places',
        maxzoom: 8,
        symbolizer: new P.GroupSymbolizer([
          new P.CircleSymbolizer({ radius: 2, fill: PALETTE.placeLabel, stroke: PALETTE.placeHalo, width: 1.5 }),
          new P.OffsetTextSymbolizer({
            labelProps: names, fill: PALETTE.placeLabel, stroke: PALETTE.placeHalo, width: 2.5,
            fontFamily: family, fontWeight: 500, fontSize: 12, offsetX: 6, offsetY: 4.5
          })
        ]),
        filter: function (z, f) { return f.props.kind === 'locality' && (f.props.kind_detail === 'city' || f.props.kind_detail === 'town'); }
      }
    ];
    return { paint: paint, label: labels, background: PALETTE.water };
  }

  /* The base map. Resolves to the layer once the archive's header has been
     read, or to null when the archive or the library is unavailable. The
     header is read through the same PMTiles instance the layer then uses, so
     the probe costs no extra request. */
  function createBasemap() {
    var P = window.protomapsL;
    if (!P || !P.leafletLayer || !P.PmtilesSource) return Promise.resolve(null);
    var lang = (document.documentElement.lang || 'en').toLowerCase().split('-')[0];
    var source;
    var rules;
    try {
      source = new P.PmtilesSource(TILES_URL, false);
      rules = basemapRules(P, lang);
    } catch (error) {
      return Promise.resolve(null);
    }
    var fonts = document.fonts && document.fonts.load
      ? [document.fonts.load('500 12px Montserrat'), document.fonts.load('italic 400 12px Montserrat')]
      : [];
    return source.p.getHeader().then(function () {
      return P.leafletLayer({
        url: source.p,
        paintRules: rules.paint,
        labelRules: rules.label,
        backgroundColor: rules.background,
        lang: lang,
        maxDataZoom: DATA_MAX_ZOOM,
        attribution: ATTRIBUTION,
        tasks: fonts,
        bounds: BOUNDS
      });
    }, function () { return null; });
  }

  function init(bridge) {
    return loadLibraries().then(function () { return build(bridge); });
  }

  function build(bridge) {
    var L = window.L;
    var t = bridge.i18n;
    var host = bridge.mapView;
    var grid = bridge.grid;
    var root = bridge.root;

    /* ---- DOM ---------------------------------------------------------- */

    var bar = el('div', 'dmap-bar');
    var back = el('button', 'dmap-icon-btn', { type: 'button', 'aria-label': t.backToFilters });
    back.appendChild(svg(ICON.filters, 18, 2));
    var heading = el('div', 'dmap-heading');
    var headingArea = el('span', 'dmap-heading-area');
    var headingCount = el('span', 'dmap-heading-count');
    heading.appendChild(headingArea);
    heading.appendChild(headingCount);
    var barView = el('div', 'discovery-view dmap-view', { role: 'group', 'aria-label': t.view });
    [['list', ICON.list, t.list], ['map', ICON.pin, t.map]].forEach(function (entry) {
      var button = el('button', 'discovery-view-btn', { type: 'button', 'data-view-mode': entry[0], 'aria-label': entry[2] });
      button.appendChild(svg(entry[1], 18));
      var label = el('span');
      label.textContent = entry[2];
      button.appendChild(label);
      barView.appendChild(button);
    });
    bar.appendChild(back);
    bar.appendChild(heading);
    bar.appendChild(barView);

    var stageBox = el('div', 'dmap-stage');
    var canvas = el('div', 'dmap-canvas', { role: 'region', 'aria-label': t.mapLabel });
    stageBox.appendChild(canvas);

    var zoomBox = el('div', 'dmap-zoom');
    var zoomIn = el('button', 'dmap-zoom-btn', { type: 'button', 'aria-label': t.zoomIn });
    zoomIn.appendChild(svg('<path d="M12 5v14M5 12h14"/>', 18, 2));
    var zoomOut = el('button', 'dmap-zoom-btn', { type: 'button', 'aria-label': t.zoomOut });
    zoomOut.appendChild(svg('<path d="M5 12h14"/>', 18, 2));
    zoomBox.appendChild(zoomIn);
    zoomBox.appendChild(zoomOut);
    stageBox.appendChild(zoomBox);

    var tools = el('div', 'dmap-tools');
    var drawBtn = el('button', 'dmap-tool-btn', { type: 'button', 'aria-pressed': 'false' });
    drawBtn.appendChild(svg(ICON.pen, 16));
    var drawLabel = el('span');
    drawLabel.textContent = t.drawArea;
    drawBtn.appendChild(drawLabel);
    var clearBtn = el('button', 'dmap-tool-btn dmap-tool-btn--clear', { type: 'button' });
    clearBtn.appendChild(svg(ICON.close, 14, 2.2));
    var clearLabel = el('span');
    clearLabel.textContent = t.clearArea;
    clearBtn.appendChild(clearLabel);
    clearBtn.hidden = true;
    tools.appendChild(drawBtn);
    tools.appendChild(clearBtn);
    stageBox.appendChild(tools);

    var hint = el('p', 'dmap-hint', { role: 'status' });
    hint.hidden = true;
    stageBox.appendChild(hint);

    var drawSurface = el('div', 'dmap-draw');
    drawSurface.hidden = true;
    var drawSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    drawSvg.setAttribute('aria-hidden', 'true');
    var drawPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    drawSvg.appendChild(drawPath);
    drawSurface.appendChild(drawSvg);
    stageBox.appendChild(drawSurface);

    var note = el('p', 'dmap-note');
    note.hidden = true;
    stageBox.appendChild(note);

    var empty = el('div', 'dmap-empty', { role: 'status' });
    var emptyTitle = el('p', 'dmap-empty-title');
    var emptyReset = el('button', 'dmap-empty-reset', { type: 'button' });
    empty.appendChild(emptyTitle);
    empty.appendChild(emptyReset);
    empty.hidden = true;
    stageBox.appendChild(empty);

    var cardBox = el('article', 'dmap-card');
    cardBox.hidden = true;
    stageBox.appendChild(cardBox);

    var carousel = el('div', 'dmap-carousel');
    carousel.hidden = true;

    host.appendChild(bar);
    host.appendChild(stageBox);
    host.appendChild(carousel);

    /* ---- Map ---------------------------------------------------------- */

    var animate = function () { return !reduceMotion.matches; };
    var map = L.map(canvas, {
      zoomControl: false,
      attributionControl: true,
      minZoom: MIN_ZOOM,
      maxZoom: MAX_ZOOM,
      zoomSnap: 1,
      /* Without this, tiles can stay at opacity 0 when fitBounds runs right
         after the layer is created (same note as nueva-location-map.js). */
      fadeAnimation: false,
      zoomAnimation: animate(),
      markerZoomAnimation: animate(),
      inertia: animate(),
      scrollWheelZoom: false
    });
    map.setView(FALLBACK_VIEW, 10, { animate: false });
    bridge.map = map; // read by tests and by anything that wants to drive the view

    /* The ground is added when the archive answers. If it never does (file
       missing, library blocked, offline) the canvas stays a plain ground: the
       pins, the rail and the draw tool do not depend on it. */
    createBasemap().then(function (layer) {
      if (!layer) { canvas.classList.add('has-tile-error'); return; }
      layer.addTo(map);
      /* The ground outside the archive: the page's own cream as a ring around
         the world with the archive's box cut out, and open sea to the south
         (the Mediterranean really is there). Under the pins, above the tiles. */
      map.createPane('nodata');
      map.getPane('nodata').style.zIndex = 250;
      map.getPane('nodata').style.pointerEvents = 'none';
      var cover = function (rings, color) {
        L.polygon(rings, { pane: 'nodata', stroke: false, fillColor: color, fillOpacity: 1, interactive: false }).addTo(map);
      };
      cover([
        [[-85, -180], [-85, 180], [85, 180], [85, -180]],
        [BOUNDS[0], [BOUNDS[0][0], BOUNDS[1][1]], BOUNDS[1], [BOUNDS[1][0], BOUNDS[0][1]]]
      ], PALETTE.earth);
      cover([[[-85, -180], [-85, 180], [BOUNDS[0][0], 180], [BOUNDS[0][0], -180]]], PALETTE.water);
    });

    /* The wheel only zooms the map once it has been used, so scrolling the
       page past it is never trapped. */
    canvas.addEventListener('pointerdown', function () { map.scrollWheelZoom.enable(); });
    canvas.addEventListener('mouseleave', function () { map.scrollWheelZoom.disable(); });

    zoomIn.addEventListener('click', function () { map.zoomIn(); });
    zoomOut.addEventListener('click', function () { map.zoomOut(); });

    var pinLayer = L.layerGroup().addTo(map);
    var areaLayer = null;

    /* ---- State -------------------------------------------------------- */

    var shown = false;
    var selected = null; // a card element
    var cardSet = []; // the cards the compact card pages through
    var pinFor = new Map(); // card -> pin element (price pins only)
    var lastSignature = null;

    function nameOf(card) {
      var node = card.querySelector('.dev-name');
      return node ? node.textContent.trim() : (card.dataset.title || '');
    }
    function textOf(card, selector) {
      var node = card.querySelector(selector);
      return node ? node.textContent.trim() : '';
    }
    function priceLabel(card) {
      var value = bridge.price(card);
      return value > 0 ? bridge.compactPrice(value) : textOf(card, '.dev-price-amount');
    }
    function mapped() {
      return bridge.visible.filter(function (card) { return bridge.cardPoint(card); });
    }

    /* ---- Pins and clusters -------------------------------------------- */

    function cluster(cards, zoom) {
      var groups = [];
      cards.forEach(function (card) {
        var ll = bridge.cardPoint(card);
        var p = map.project(L.latLng(ll[0], ll[1]), zoom);
        var home = null;
        for (var i = 0; i < groups.length; i += 1) {
          if (Math.abs(groups[i].x - p.x) < CLUSTER_DX && Math.abs(groups[i].y - p.y) < CLUSTER_DY) {
            home = groups[i];
            break;
          }
        }
        if (home) {
          home.cards.push(card);
          home.sx += p.x;
          home.sy += p.y;
          home.x = home.sx / home.cards.length;
          home.y = home.sy / home.cards.length;
        } else {
          groups.push({ cards: [card], sx: p.x, sy: p.y, x: p.x, y: p.y });
        }
      });
      return groups;
    }

    function pinButton(card) {
      var label = priceLabel(card);
      var button = el('button', 'dmap-pin', { type: 'button', 'aria-label': label + ', ' + nameOf(card) });
      var inner = el('span', 'dmap-pin-label', { dir: 'ltr' });
      inner.textContent = label;
      button.appendChild(inner);
      if (card === selected) button.classList.add('is-selected');
      button.addEventListener('click', function () {
        select(card, { open: true, pan: true, set: bridge.visible.filter(function (c) { return bridge.cardPoint(c); }) });
      });
      button.addEventListener('mouseenter', function () { highlight(card, true); });
      button.addEventListener('mouseleave', function () { highlight(card, false); });
      button.addEventListener('focus', function () { highlight(card, true); scrollRailTo(card); });
      button.addEventListener('blur', function () { highlight(card, false); });
      return button;
    }

    function clusterButton(group, latlng) {
      var count = group.cards.length;
      var label = t.clusterMany.replace('{n}', String(count));
      var button = el('button', 'dmap-cluster', { type: 'button', 'aria-label': label });
      var inner = el('span', null, { dir: 'ltr' });
      inner.textContent = String(count);
      button.appendChild(inner);
      if (group.cards.indexOf(selected) >= 0) button.classList.add('is-selected');
      button.addEventListener('click', function () { openCluster(group, latlng, button); });
      return button;
    }

    function addMarker(button, latlng, z) {
      var icon = L.divIcon({ className: 'dmap-marker', html: button, iconSize: [0, 0], iconAnchor: [0, 0] });
      L.marker(latlng, { icon: icon, keyboard: false, riseOnHover: false, zIndexOffset: z || 0 }).addTo(pinLayer);
    }

    function renderPins() {
      pinLayer.clearLayers();
      pinFor.clear();
      var cards = mapped();
      var zoom = map.getZoom();
      cluster(cards, zoom).forEach(function (group) {
        var latlng = map.unproject(L.point(group.x, group.y), zoom);
        if (group.cards.length === 1) {
          var card = group.cards[0];
          var button = pinButton(card);
          pinFor.set(card, button);
          var ll = bridge.cardPoint(card);
          addMarker(button, L.latLng(ll[0], ll[1]), card === selected ? 1000 : 0);
        } else {
          addMarker(clusterButton(group, latlng), latlng, group.cards.indexOf(selected) >= 0 ? 900 : 0);
        }
      });
    }

    function openCluster(group, latlng, button) {
      var bounds = L.latLngBounds(group.cards.map(function (card) {
        var ll = bridge.cardPoint(card);
        return L.latLng(ll[0], ll[1]);
      }));
      /* Pins that share a coordinate can never be pulled apart by zooming:
         page through them in the compact card instead. */
      var spread = map.project(bounds.getNorthEast(), MAX_ZOOM).distanceTo(map.project(bounds.getSouthWest(), MAX_ZOOM));
      if (spread < Math.min(CLUSTER_DX, CLUSTER_DY) / 2) {
        select(group.cards[0], { open: true, pan: true, set: group.cards });
        return;
      }
      /* At least one level in, however tight the frame: a bubble that fits
         the padded frame at the current zoom would otherwise never open. */
      var zoom = map.getBoundsZoom(bounds, false, L.point(60, 60));
      zoom = Math.min(Math.max(zoom, map.getZoom() + 1), MAX_ZOOM - 1);
      map.setView(bounds.getCenter(), zoom, { animate: animate() });
    }

    /* ---- Selection, rail and compact card ----------------------------- */

    var hovered = null;
    function highlight(card, on) {
      if (hovered && hovered !== card) hovered.classList.remove('is-map-hover');
      card.classList.toggle('is-map-hover', on);
      hovered = on ? card : null;
      var pin = pinFor.get(card);
      if (pin) pin.classList.toggle('is-hover', on);
    }

    function scrollRailTo(card) {
      if (phone.matches || !stageBox.parentNode.classList.contains('is-map')) return;
      var rail = grid;
      if (rail.scrollHeight <= rail.clientHeight + 4) return; // the rail is not its own scroller (stacked layout)
      var top = card.getBoundingClientRect().top - rail.getBoundingClientRect().top + rail.scrollTop - 12;
      rail.scrollTo({ top: Math.max(0, top), behavior: animate() ? 'smooth' : 'auto' });
    }

    function select(card, options) {
      options = options || {};
      var previous = selected;
      selected = card || null;
      if (previous && previous !== selected) previous.classList.remove('is-map-active');
      if (selected) selected.classList.add('is-map-active');
      if (options.set) cardSet = options.set;
      pinFor.forEach(function (pin, c) { pin.classList.toggle('is-selected', c === selected); });
      if (selected) {
        var ll = bridge.cardPoint(selected);
        if (options.pan && ll) {
          /* Keep the pin clear of whatever covers part of the map: the compact
             card (bottom-right corner) or the phone carousel (bottom). */
          var wide = canvas.clientWidth >= 720;
          var clearSide = phone.matches ? 40 : (wide ? 370 : 60);
          var clearBottom = phone.matches ? carousel.offsetHeight + 80 : (wide ? 60 : 390);
          /* The card sits at the inline end, which is the left in Arabic. */
          var rtl = getComputedStyle(host).direction === 'rtl';
          map.panInside(L.latLng(ll[0], ll[1]), {
            paddingTopLeft: [rtl ? clearSide : 60, 70],
            paddingBottomRight: [rtl ? 60 : clearSide, clearBottom],
            animate: animate()
          });
        }
        if (options.rail !== false) scrollRailTo(selected);
        if (phone.matches) {
          if (options.fromCarousel !== true) scrollCarouselTo(selected);
        } else if (options.open) {
          showCompact(selected);
        } else if (!cardBox.hidden) {
          showCompact(selected);
        }
      } else {
        hideCompact();
      }
      renderPinsSoon();
    }

    var pinsQueued = false;
    function renderPinsSoon() {
      /* A selection changes which marker is on top and which bubble is
         marked; re-drawing keeps that in one code path. The focus is put back
         on the same control afterwards. */
      if (pinsQueued) return;
      pinsQueued = true;
      requestAnimationFrame(function () {
        pinsQueued = false;
        var active = document.activeElement;
        var focusCard = null;
        pinFor.forEach(function (pin, c) { if (pin === active) focusCard = c; });
        renderPins();
        if (focusCard && pinFor.get(focusCard)) pinFor.get(focusCard).focus({ preventScroll: true });
      });
    }

    function compactNode(card, options) {
      var node = el(options.tag || 'div', 'dmap-compact');
      var picture = card.querySelector('.dev-img-wrap picture');
      var media = el('div', 'dmap-compact-media');
      if (picture) {
        var clone = picture.cloneNode(true);
        clone.querySelectorAll('source').forEach(function (source) { source.sizes = '340px'; });
        var image = clone.querySelector('img');
        if (image) {
          image.loading = 'lazy';
          image.decoding = 'async';
        }
        media.appendChild(clone);
      }
      media.appendChild(el('div', 'dmap-compact-scrim', { 'aria-hidden': 'true' }));
      var badges = el('div', 'dmap-compact-badges');
      [textOf(card, '.dev-badge'), textOf(card, '.dev-badge-units')].forEach(function (text, i) {
        if (!text) return;
        var badge = el('span', i === 0 ? 'dmap-badge' : 'dmap-badge dmap-badge--units');
        badge.textContent = text;
        badges.appendChild(badge);
      });
      var price = el('div', 'dmap-compact-price');
      var priceFrom = textOf(card, '.dev-price-label');
      if (priceFrom) {
        var fromNode = el('span', 'dmap-compact-from');
        fromNode.textContent = priceFrom;
        price.appendChild(fromNode);
      }
      var amount = el('span', 'dmap-compact-amount', { dir: 'ltr' });
      amount.textContent = textOf(card, '.dev-price-amount');
      price.appendChild(amount);
      var overlay = el('div', 'dmap-compact-overlay');
      overlay.appendChild(badges);
      overlay.appendChild(price);
      media.appendChild(overlay);
      node.appendChild(media);

      var body = el('div', 'dmap-compact-body');
      var top = el('div', 'dmap-compact-top');
      var name = el('h3', 'dmap-compact-name');
      name.textContent = nameOf(card);
      top.appendChild(name);
      if (options.counter) top.appendChild(options.counter);
      body.appendChild(top);
      var loc = textOf(card, '.dev-loc');
      if (loc) {
        var locNode = el('p', 'dmap-compact-loc');
        locNode.textContent = loc;
        body.appendChild(locNode);
      }
      var facts = el('div', 'dmap-compact-facts');
      card.querySelectorAll('.dev-fact').forEach(function (fact) {
        var label = fact.querySelector('.dev-fact-label');
        var value = fact.querySelector('.dev-fact-value');
        if (!label || !value) return;
        var cell = el('div', 'dmap-fact' + (fact.classList.contains('dev-fact--gold') ? ' is-gold' : ''));
        var l = el('span', 'dmap-fact-label');
        l.textContent = label.textContent.trim();
        var v = el('span', 'dmap-fact-value');
        v.textContent = value.textContent.trim();
        cell.appendChild(l);
        cell.appendChild(v);
        facts.appendChild(cell);
      });
      if (facts.children.length) body.appendChild(facts);
      var cta = card.querySelector('.dev-cta-link');
      if (cta) {
        var link = el('a', 'dmap-compact-cta', { href: cta.getAttribute('href') });
        var linkText = el('span');
        linkText.textContent = textOf(cta, '.dev-cta-label') || cta.textContent.trim();
        link.appendChild(linkText);
        link.appendChild(svg(ICON.arrow, 18, 1.6));
        link.setAttribute('aria-label', linkText.textContent + ': ' + nameOf(card));
        body.appendChild(link);
      }
      node.appendChild(body);
      return node;
    }

    function showCompact(card) {
      var index = cardSet.indexOf(card);
      if (index < 0) { cardSet = bridge.visible.filter(function (c) { return bridge.cardPoint(c); }); index = cardSet.indexOf(card); }
      var counter = null;
      if (cardSet.length > 1) {
        counter = el('span', 'dmap-compact-count', { dir: 'ltr' });
        counter.textContent = (index + 1) + ' / ' + cardSet.length;
      }
      cardBox.textContent = '';
      cardBox.setAttribute('aria-label', nameOf(card));
      var content = compactNode(card, { counter: counter });
      var media = content.querySelector('.dmap-compact-media');
      var nav = el('div', 'dmap-compact-nav');
      var closeBtn = el('button', 'dmap-round-btn dmap-compact-close', { type: 'button', 'aria-label': t.closeCard });
      closeBtn.appendChild(svg(ICON.close, 18, 2));
      closeBtn.addEventListener('click', function () { closeCompact(true); });
      media.appendChild(closeBtn);
      if (cardSet.length > 1) {
        [['prev', t.prevProject, -1], ['next', t.nextProject, 1]].forEach(function (entry) {
          var button = el('button', 'dmap-round-btn', { type: 'button', 'aria-label': entry[1] });
          button.appendChild(svg(ICON[entry[0]], 20, 2));
          button.addEventListener('click', function () {
            var to = cardSet[(index + entry[2] + cardSet.length) % cardSet.length];
            select(to, { open: true, pan: true });
            /* The compact card was rebuilt for the new project; keep the
               keyboard on the same arrow. */
            var arrows = cardBox.querySelectorAll('.dmap-compact-nav .dmap-round-btn');
            if (arrows[entry[2] < 0 ? 0 : 1]) arrows[entry[2] < 0 ? 0 : 1].focus({ preventScroll: true });
          });
          nav.appendChild(button);
        });
        media.appendChild(nav);
      }
      cardBox.appendChild(content);
      cardBox.hidden = false;
    }

    function hideCompact() {
      cardBox.hidden = true;
      cardBox.textContent = '';
    }

    function closeCompact(returnFocus) {
      var card = selected;
      select(null);
      if (returnFocus) {
        /* The pins are re-drawn on the next frame, so look for the one that
           stands for the same card then. */
        requestAnimationFrame(function () {
          requestAnimationFrame(function () {
            var pin = card && pinFor.get(card);
            if (pin) pin.focus({ preventScroll: true });
            else canvas.focus({ preventScroll: true });
          });
        });
      }
    }

    /* ---- Phone carousel ------------------------------------------------ */

    var carouselTimer = null;
    function buildCarousel() {
      carousel.textContent = '';
      if (!phone.matches) { carousel.hidden = true; return; }
      var cards = mapped();
      carousel.hidden = cards.length === 0;
      cards.forEach(function (card) {
        var item = compactNode(card, { tag: 'article' });
        item.classList.add('dmap-slide');
        item._card = card;
        item.addEventListener('click', function (event) {
          if (event.target.closest('a')) return;
          select(card, { pan: true, fromCarousel: true });
        });
        carousel.appendChild(item);
      });
      markSlides();
    }
    function markSlides() {
      Array.prototype.forEach.call(carousel.children, function (item) {
        item.classList.toggle('is-selected', item._card === selected);
      });
    }
    function scrollCarouselTo(card) {
      markSlides();
      var item = Array.prototype.find.call(carousel.children, function (c) { return c._card === card; });
      if (!item) return;
      carousel.scrollTo({ left: item.offsetLeft - (carousel.clientWidth - item.clientWidth) / 2, behavior: animate() ? 'smooth' : 'auto' });
    }
    /* Only the visitor's own swipe picks a project. The carousel also moves
       itself (when a pin is chosen), and that must not select anything. */
    var carouselTouched = false;
    ['pointerdown', 'touchstart', 'wheel', 'keydown'].forEach(function (type) {
      carousel.addEventListener(type, function () { carouselTouched = true; }, { passive: true });
    });
    carousel.addEventListener('scroll', function () {
      if (!carouselTouched) return;
      clearTimeout(carouselTimer);
      carouselTimer = setTimeout(function () {
        carouselTouched = false;
        var middle = carousel.scrollLeft + carousel.clientWidth / 2;
        var best = null;
        var bestDistance = Infinity;
        Array.prototype.forEach.call(carousel.children, function (item) {
          var distance = Math.abs(item.offsetLeft + item.clientWidth / 2 - middle);
          if (distance < bestDistance) { bestDistance = distance; best = item; }
        });
        if (best && best._card !== selected) select(best._card, { pan: true, fromCarousel: true });
      }, 140);
    }, { passive: true });

    /* ---- Drawing an area ----------------------------------------------- */

    var drawing = false;
    var trace = [];
    var drawPointer = null;

    function setDrawing(on) {
      drawing = on;
      drawBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      drawBtn.classList.toggle('is-on', on);
      drawSurface.hidden = !on;
      hint.hidden = !on;
      hint.textContent = on ? t.drawHint : '';
      stageBox.classList.toggle('is-drawing', on);
      drawPath.setAttribute('d', '');
      trace = [];
      if (on) { closeCompact(false); drawSurface.focus && drawSurface.focus(); }
    }

    function point(event) {
      var rect = drawSurface.getBoundingClientRect();
      return [event.clientX - rect.left, event.clientY - rect.top];
    }
    function pathOf(points, closed) {
      return points.map(function (p, i) { return (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join('') + (closed ? 'Z' : '');
    }

    drawSurface.addEventListener('pointerdown', function (event) {
      if (!drawing || (event.pointerType === 'mouse' && event.button !== 0)) return;
      event.preventDefault();
      drawPointer = event.pointerId;
      drawSurface.setPointerCapture(event.pointerId);
      trace = [point(event)];
      drawPath.setAttribute('d', pathOf(trace));
    });
    drawSurface.addEventListener('pointermove', function (event) {
      if (!drawing || event.pointerId !== drawPointer) return;
      var p = point(event);
      var last = trace[trace.length - 1];
      if (Math.abs(p[0] - last[0]) + Math.abs(p[1] - last[1]) < 5) return;
      trace.push(p);
      drawPath.setAttribute('d', pathOf(trace, false));
    });
    function finishDrawing(event) {
      if (!drawing || event.pointerId !== drawPointer) return;
      drawPointer = null;
      var points = trace;
      var cancelled = event.type === 'pointercancel';
      setDrawing(false);
      if (cancelled || points.length < 4) return;
      /* A shape this small is a slip of the finger, not an area. */
      var xs = points.map(function (p) { return p[0]; });
      var ys = points.map(function (p) { return p[1]; });
      if (Math.max.apply(null, xs) - Math.min.apply(null, xs) < 24 || Math.max.apply(null, ys) - Math.min.apply(null, ys) < 24) return;
      var step = Math.ceil(points.length / 140);
      var thinned = points.filter(function (p, i) { return i % step === 0; });
      var polygon = thinned.map(function (p) {
        var ll = map.containerPointToLatLng(L.point(p[0], p[1]));
        return [ll.lat, ll.lng];
      });
      bridge.setArea(polygon);
    }
    drawSurface.addEventListener('pointerup', finishDrawing);
    drawSurface.addEventListener('pointercancel', finishDrawing);

    drawBtn.addEventListener('click', function () { setDrawing(!drawing); });
    clearBtn.addEventListener('click', function () {
      bridge.setArea(null);
      drawBtn.focus({ preventScroll: true });
    });

    function syncArea() {
      var area = bridge.area;
      if (areaLayer) { map.removeLayer(areaLayer); areaLayer = null; }
      if (area) {
        areaLayer = L.polygon(area, {
          color: '#896a3f', weight: 2, dashArray: '8 6', fillColor: '#896a3f', fillOpacity: 0.08, interactive: false
        }).addTo(map);
      }
      clearBtn.hidden = !area;
      stageBox.classList.toggle('has-area', !!area);
    }

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape' || !shown) return;
      if (drawing) {
        event.preventDefault();
        setDrawing(false);
        drawBtn.focus({ preventScroll: true });
      } else if (!cardBox.hidden && (host.contains(document.activeElement) || !document.activeElement || document.activeElement === document.body)) {
        event.preventDefault();
        closeCompact(true);
      }
    });

    /* ---- Fitting the view ----------------------------------------------- */

    function fit() {
      var cards = mapped();
      if (!cards.length) return;
      var bounds = L.latLngBounds(cards.map(function (card) {
        var ll = bridge.cardPoint(card);
        return L.latLng(ll[0], ll[1]);
      }));
      /* On a phone the carousel covers the bottom of the map, so the pins are
         fitted into what is left above it. */
      map.fitBounds(bounds, {
        paddingTopLeft: phone.matches ? [40, 70] : [70, 70],
        paddingBottomRight: phone.matches ? [40, carousel.offsetHeight + 70] : [70, 70],
        maxZoom: 15,
        animate: false
      });
    }

    /* ---- One pass for everything that follows the result ------------------ */

    function refresh(visible) {
      if (!shown) return;
      var cards = mapped();
      /* The selection survives a filter change only if it is still a result. */
      if (selected && visible.indexOf(selected) < 0) {
        selected.classList.remove('is-map-active');
        selected = null;
        hideCompact();
      }
      cardSet = cardSet.filter(function (c) { return visible.indexOf(c) >= 0; });
      if (!cardBox.hidden && selected) showCompact(selected);

      syncArea();
      buildCarousel(); // before fitting: its height is what the fit leaves clear
      var signature = visible.map(function (c) { return c.id; }).join(',') + '|' + (bridge.area ? 'a' : '');
      if (signature !== lastSignature) {
        lastSignature = signature;
        /* A drawn area is the visitor's own framing; leave the view alone. */
        if (!bridge.area) fit();
      }
      renderPins();

      var count = root.querySelector('[data-result-count-summary]');
      headingArea.textContent = bridge.areaLabel();
      headingCount.textContent = count ? count.textContent.trim() : '';

      var unmapped = visible.length - cards.length;
      note.hidden = unmapped <= 0;
      note.textContent = unmapped > 0 ? t.unmapped.replace('{n}', String(unmapped)) : '';

      var none = visible.length === 0;
      empty.hidden = !none;
      if (none) {
        var title = root.querySelector('.discovery-empty-title');
        var reset = root.querySelector('[data-clear-filters]');
        emptyTitle.textContent = title ? title.textContent.trim() : '';
        emptyReset.textContent = reset ? reset.textContent.trim() : '';
      }
    }

    map.on('zoomend', function () {
      if (!shown) return;
      renderPins();
    });
    emptyReset.addEventListener('click', function () {
      var reset = root.querySelector('[data-clear-filters]');
      if (reset) reset.click();
    });
    back.addEventListener('click', function () { bridge.openFilters(back); });
    bridge.subscribe(refresh);

    /* Hovering or focusing a card in the rail lights its pin. */
    function cardAt(target) { return target.closest && target.closest('[data-project-card]'); }
    grid.addEventListener('mouseover', function (event) {
      if (!shown) return;
      var card = cardAt(event.target);
      if (card && pinFor.get(card)) highlight(card, true);
    });
    grid.addEventListener('mouseout', function (event) {
      var card = cardAt(event.target);
      if (card && !card.contains(event.relatedTarget)) highlight(card, false);
    });

    phone.addEventListener('change', function () {
      if (!shown) return;
      hideCompact();
      buildCarousel();
      map.invalidateSize();
    });

    return {
      show: function () {
        shown = true;
        lastSignature = null;
        map.invalidateSize();
        syncArea();
        refresh(bridge.visible);
        map.invalidateSize();
        if (!mapped().length) map.setView(FALLBACK_VIEW, 9, { animate: false });
        bar.querySelector('[data-view-mode="map"]').focus({ preventScroll: true });
      },
      hide: function () {
        shown = false;
        setDrawing(false);
        if (selected) selected.classList.remove('is-map-active');
        selected = null;
        hideCompact();
        if (hovered) hovered.classList.remove('is-map-hover');
      }
    };
  }

  window.NuevaDiscoveryMap = { init: init };
})();
