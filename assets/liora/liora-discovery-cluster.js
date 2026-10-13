/* Clustering for the developments map: a pure function, no DOM, no Leaflet.

   Loaded by liora-discovery-map.js next to it (browser: window.NuevaDiscoveryCluster)
   and imported by scripts/audit_site_consistency.mjs (node: module.exports), so
   the rule the visitor sees is the rule the audit tests.

   What a bubble promises. Every member of a bubble lies within `radius` screen
   pixels of the bubble's centre, and the bubble is drawn at the centroid of its
   members. A bubble is therefore an honest picture of what it holds: it is never
   a number floating over a long stretch of coast. The old rule (first card that
   fits a 78 x 46 px box) let a group grow by chaining, so a bubble could sit
   hundreds of pixels from some of its members.

   How. Cards that share one coordinate are one indivisible "atom" (five
   projects at one gate can never be pulled apart by zooming, so they stay one
   bubble at every zoom). Atoms are put in a canonical order (by position, then by
   coordinate), then the two closest groups are merged repeatedly, but only when
   the merged group still satisfies the radius rule around its new centroid.
   Merging stops when no pair can merge. The result depends on the set of
   coordinates and the zoom, never on the order of the cards. */
(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.NuevaDiscoveryCluster = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* Web-mercator pixels, the same projection Leaflet's default CRS uses
     (256 px tiles): pixel = 256 * 2^zoom * normalised coordinate. */
  var TILE = 256;
  function project(lat, lng, zoom) {
    var scale = TILE * Math.pow(2, zoom);
    var s = Math.sin(lat * Math.PI / 180);
    return { x: scale * (lng + 180) / 360, y: scale * (0.5 - Math.log((1 + s) / (1 - s)) / (4 * Math.PI)) };
  }
  function unproject(x, y, zoom) {
    var scale = TILE * Math.pow(2, zoom);
    var n = Math.PI * (1 - 2 * y / scale);
    return { lat: 180 / Math.PI * Math.atan(Math.sinh(n)), lng: x / scale * 360 - 180 };
  }

  /* Cards at one coordinate (to about 11 cm) are one atom. */
  function coordinateKey(lat, lng) {
    return lat.toFixed(6) + ',' + lng.toFixed(6);
  }

  /* points: [{ lat, lng }], in any order. Returns bubbles:
     [{ members: [indexes into points, ascending], x, y, lat, lng, colocated }]
     where x, y is the centroid in pixels at `zoom` and `colocated` says all
     members share one coordinate. */
  function cluster(points, zoom, radius) {
    var byKey = {};
    var atoms = [];
    points.forEach(function (point, index) {
      var key = coordinateKey(point.lat, point.lng);
      var atom = byKey[key];
      if (!atom) {
        var p = project(point.lat, point.lng, zoom);
        atom = byKey[key] = { key: key, x: p.x, y: p.y, members: [] };
        atoms.push(atom);
      }
      atom.members.push(index);
    });
    /* The canonical order: position first, the key as the final tie-break. */
    atoms.sort(function (a, b) {
      return a.x - b.x || a.y - b.y || (a.key < b.key ? -1 : a.key > b.key ? 1 : 0);
    });

    var groups = atoms.map(function (atom, rank) {
      atom.rank = rank;
      return { rank: rank, atoms: [atom], n: atom.members.length, sx: atom.x * atom.members.length, sy: atom.y * atom.members.length };
    });

    function fits(sx, sy, n, list) {
      var cx = sx / n;
      var cy = sy / n;
      for (var i = 0; i < list.length; i += 1) {
        if (Math.hypot(list[i].x - cx, list[i].y - cy) > radius) return false;
      }
      return true;
    }

    for (;;) {
      var best = null;
      for (var i = 0; i < groups.length; i += 1) {
        for (var j = i + 1; j < groups.length; j += 1) {
          var a = groups[i];
          var b = groups[j];
          var d = Math.hypot(a.sx / a.n - b.sx / b.n, a.sy / a.n - b.sy / b.n);
          if (d > 2 * radius) continue;
          /* Ties (equal distance) go to the pair with the lowest ranks: a
             rank is a canonical property of the coordinates, not an input
             position. */
          var lo = a.rank < b.rank ? a : b;
          var hi = lo === a ? b : a;
          if (best && (d > best.d || (d === best.d && (lo.rank > best.lo.rank || (lo.rank === best.lo.rank && hi.rank > best.hi.rank))))) continue;
          var merged = a.atoms.concat(b.atoms);
          if (!fits(a.sx + b.sx, a.sy + b.sy, a.n + b.n, merged)) continue;
          best = { d: d, a: a, b: b, lo: lo, hi: hi, merged: merged };
        }
      }
      if (!best) break;
      var a2 = best.a;
      var b2 = best.b;
      var group = { rank: Math.min(a2.rank, b2.rank), atoms: best.merged, n: a2.n + b2.n, sx: a2.sx + b2.sx, sy: a2.sy + b2.sy };
      groups = groups.filter(function (g) { return g !== a2 && g !== b2; });
      groups.push(group);
    }

    /* Closest-first merging can leave two bubbles whose centres are nearer
       than a bubble is wide, because merging them would break the radius rule.
       Move single locations from one bubble to a neighbour while that pulls
       the centres apart and both still satisfy the rule. Every step is chosen
       by canonical rank, so the order of the cards still does not matter. */
    var APART = 44;
    function overlap(g, h) {
      return Math.max(0, APART - Math.hypot(g.sx / g.n - h.sx / h.n, g.sy / g.n - h.sy / h.n));
    }
    function penalty(list) {
      var sum = 0;
      for (var i = 0; i < list.length; i += 1) for (var j = i + 1; j < list.length; j += 1) sum += overlap(list[i], list[j]);
      return sum;
    }
    function without(group, atom) {
      var atomsLeft = group.atoms.filter(function (a) { return a !== atom; });
      if (!atomsLeft.length) return null;
      var w = atom.members.length;
      return { rank: Math.min.apply(null, atomsLeft.map(function (a) { return a.rank; })), atoms: atomsLeft, n: group.n - w, sx: group.sx - atom.x * w, sy: group.sy - atom.y * w };
    }
    function withAtom(group, atom) {
      var w = atom.members.length;
      return { rank: Math.min(group.rank, atom.rank), atoms: group.atoms.concat([atom]), n: group.n + w, sx: group.sx + atom.x * w, sy: group.sy + atom.y * w };
    }
    for (var step = 0; step < 400; step += 1) {
      var base = penalty(groups);
      if (base === 0) break;
      var move = null;
      groups.slice().sort(function (p, q) { return p.rank - q.rank; }).forEach(function (from) {
        from.atoms.forEach(function (atom) {
          var nextFrom = without(from, atom);
          groups.forEach(function (to) {
            if (to === from) return;
            var nextTo = withAtom(to, atom);
            if (!fits(nextTo.sx, nextTo.sy, nextTo.n, nextTo.atoms)) return;
            if (nextFrom && !fits(nextFrom.sx, nextFrom.sy, nextFrom.n, nextFrom.atoms)) return;
            var after = groups.filter(function (g) { return g !== from && g !== to; });
            if (nextFrom) after.push(nextFrom);
            after.push(nextTo);
            var gain = base - penalty(after);
            if (gain <= 1e-9) return;
            if (!move || gain > move.gain + 1e-9 || (Math.abs(gain - move.gain) <= 1e-9 && (atom.rank < move.atom.rank || (atom.rank === move.atom.rank && to.rank < move.to.rank)))) {
              move = { gain: gain, atom: atom, from: from, to: to, groups: after };
            }
          });
        });
      });
      if (!move) break;
      groups = move.groups;
    }

    return groups.map(function (group) {
      var members = [];
      group.atoms.forEach(function (atom) { members.push.apply(members, atom.members); });
      members.sort(function (p, q) { return p - q; });
      var x = group.sx / group.n;
      var y = group.sy / group.n;
      var ll = unproject(x, y, zoom);
      return { members: members, x: x, y: y, lat: ll.lat, lng: ll.lng, colocated: group.atoms.length === 1 };
    }).sort(function (p, q) { return p.members[0] - q.members[0]; });
  }

  /* The first zoom, from `fromZoom` up to `maxZoom`, at which the given points
     no longer form one bubble; null when they never separate (two projects a few
     metres apart stay one bubble even at the closest zoom). A click on such a
     bubble cannot be answered by zooming, so it opens the compact card instead. */
  function splitZoom(points, fromZoom, maxZoom, radius) {
    for (var z = Math.max(0, Math.ceil(fromZoom)); z <= maxZoom; z += 1) {
      if (cluster(points, z, radius).length >= 2) return z;
    }
    return null;
  }

  return { cluster: cluster, splitZoom: splitZoom, project: project, unproject: unproject, coordinateKey: coordinateKey };
});
