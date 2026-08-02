# Nueva Property Page Builder

Create one folder per project:

```text
content/liora-projects/altos-de-marbella/project.json
assets/liora/projects/altos-de-marbella/hero.jpg
assets/liora/projects/altos-de-marbella/architecture.jpg
assets/liora/projects/altos-de-marbella/private-viewing.jpg
```

Use `content/liora-projects/project-template.json` as the starting point. Copy it into a new project folder, rename the folder to the project slug, then replace the placeholder copy and image paths.

Then run:

```bash
node scripts/build_property_pages.mjs
```

The builder writes `property-*.html` pages and refreshes the managed project cards in `developments.html` using the existing Nueva shared CSS and JS:

- `assets/liora/liora-pages.css`
- `assets/liora/liora-property.css`
- `assets/liora/liora-property.js`

If `images.hero.src`, `images.architecture.src` or `images.privateViewing.src` are omitted, the builder looks for conventional image names in `assets/liora/projects/<slug>/`.

For the developments listing card, add an optional `card` block:

```json
{
  "card": {
    "order": 10,
    "label": "Marbella East",
    "description": "Short card copy.",
    "meta": [["From", "€1,250,000"], ["Type", "Penthouses & Villas"], ["Delivery", "Q4 2027"]]
  }
}
```

If `card.image.src` is omitted, the builder uses `assets/liora/projects/<slug>/card.jpg` when present, otherwise the hero image.

For the homepage's "Selected Residences" cards, the same `card` block is reused
automatically (no separate HTML edit needed). Two optional fields let you
diverge from the Developments-page copy where the homepage wants something
shorter or punchier:

```json
{
  "card": {
    "badge": "Current Release",
    "typeTag": "Golf Valley",
    "locExtended": "Marbella East — Elevated Coastline"
  }
}
```

`badge` defaults to the title-cased `discovery.status` if omitted. `typeTag`
defaults to the first `discovery.locationTags` entry. `locExtended` defaults
to `card.label`.

### Location map

`location.mapArea` controls where the project's marker lands on the location
map (`src/.../locationMap()` in `build_property_pages.mjs`) relative to a
fixed set of real Costa del Sol landmarks -- it does not use the actual
coordinates of the project, only which named area it belongs to. Valid
values: `estepona`, `newGoldenMile`, `sanPedro`, `benahavis`, `puertoBanus`,
`nuevaAndalucia`, `goldenMile`, `marbellaCentre`, `marbellaEast`,
`malagaAirport`. Omitting it falls back to `marbellaCentre`, so always set it
explicitly for anything not actually in central Marbella -- an earlier
version of this map hardcoded one fixed layout for every project, which
placed at least one real project on the wrong side of Puerto Banús.

### Construction timeline

`constructionTimeline` renders an optional "Timeline" band right after
Overview on the property page -- a horizontal line of year markers, with
a leaf icon and label on milestone points (e.g. "Phase I", "Phase II",
"End"). Omit the whole block if a project has no confirmed phase
schedule; the section simply doesn't render. Never invent dates -- only
add this once real phase/delivery years are confirmed from the
developer.

```json
{
  "constructionTimeline": {
    "kicker": "Timeline",
    "copy": "Short factual note about the build phases.",
    "points": [
      { "year": "2024", "label": "Phase I", "milestone": true, "icon": "start" },
      { "year": "2025" },
      { "year": "2026" },
      { "year": "2027", "label": "Phase II", "milestone": true, "icon": "construction" },
      { "year": "2028" },
      { "year": "2029", "label": "End", "milestone": true, "icon": "finish" }
    ]
  }
}
```

`milestone: true` points get an icon and (if present) the label above
the line; other points just get a plain dot and their year. `icon` is
optional -- one of `start` (flag), `construction` (crane) or `finish`
(key); omit it to fall back to the plain leaf mark. The whole track
animates in on scroll (line draws left to right, markers pop in one by
one) as part of the shared `.reveal-soft` scroll-reveal system.

An optional `paymentTerms` array renders a row of stat chips below the
track (same `[label, value]` tuple shape used elsewhere, e.g.
`["Reservation", "10%"]`). Omit it if the payment schedule isn't
confirmed yet -- same rule as the dates: never invent figures.

### Developments-page filters

The Developments page's primary filter bar (Location, Property Type, Status,
Price and Bedrooms) reads two fields on each project:

- `discovery.area` -- one of `marbella`, `estepona`, `benahavis`,
  `nueva-andalucia`, `mijas-fuengirola`. This drives the Location select only
  and is independent of `crm.area` below (which uses a different, CRM-side
  enum and may not exist for every project).
- `crm.propertyTypes`, `crm.bedroomsMin`, `crm.bedroomsMax` and
  `crm.constructionStatus` -- reused as-is for the Property Type, Bedrooms
  and Status filters. A project without a `crm` block is invisible to those
  three filters (it will only show for "Any"), so add one even when
  `CRM_WEBHOOK_SECRET` sync is disabled.

## CRM property data

The builder automatically syncs generated projects to the CRM when
`CRM_WEBHOOK_SECRET` is available in the server/build environment. Add the
project-specific fields that cannot be inferred reliably to the `crm` block:

```json
{
  "crm": {
    "developer": "Developer name",
    "area": "marbella",
    "address": "Project address",
    "priceMin": 850000,
    "priceMax": 1500000,
    "currency": "EUR",
    "bedroomsMin": 3,
    "bedroomsMax": 5,
    "propertyTypes": ["villa"],
    "totalUnits": 12,
    "availableUnits": 8,
    "deliveryDate": "2026-06-01",
    "constructionStatus": "off_plan",
    "brochureUrl": "https://example.com/brochure.pdf",
    "amenities": ["pool", "gym", "parking"]
  }
}
```

Allowed `area` values are `marbella`, `estepona`, `benahavis`, and `other`.
Allowed `constructionStatus` values are `off_plan`, `under_construction`, and
`completed`. Allowed `propertyTypes` values are `apartment`, `penthouse`,
`villa`, and `townhouse`.
