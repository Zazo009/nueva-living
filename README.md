# Nueva Living

Static luxury real estate website for Nueva Living, a new-development advisory brand for the Costa del Sol.

## Netlify

Build command:

```bash
node scripts/build_property_pages.mjs && node scripts/build_dist.mjs
```

Publish directory:

```text
dist
```

Functions directory:

```text
netlify/functions
```

Required production environment variables for lead forwarding:

```text
CRM_WEBHOOK_URL=https://marbella-crm.vercel.app/api/webhook/liora
WEBHOOK_SECRET=change-me
ALLOWED_ORIGINS=https://nueva-living.com,https://www.nueva-living.com
```

## Local Preview

```bash
node scripts/build_property_pages.mjs
node scripts/build_dist.mjs
python3 -m http.server 4199 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:4199/dist/index.html
```
