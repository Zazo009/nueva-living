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
