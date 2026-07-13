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
