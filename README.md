# Nueva Living

Static luxury real estate website for Nueva Living, a new-development advisory brand for the Costa del Sol.

## Netlify

Build command:

```bash
node scripts/build_footer_pages.mjs && node scripts/build_property_pages.mjs && node scripts/build_dist.mjs
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
CRM_WEBHOOK_SECRET=change-me
ALLOWED_ORIGINS=https://nuevaliving.com,https://www.nuevaliving.com
```

The browser submits to `/.netlify/functions/nueva-lead`. The function adds the
webhook secret server-side before forwarding the lead to the CRM; never expose
`CRM_WEBHOOK_SECRET` in HTML or client-side JavaScript.

Successful CRM submissions show an inline confirmation. If client-side JavaScript
is unavailable, the HTML form posts to the same Netlify Function and redirects to
the thank-you page only after the CRM accepts the lead. CRM acceptance is the
authoritative success signal; the browser never receives the webhook secret.

## Local Preview

```bash
node scripts/build_footer_pages.mjs
node scripts/build_property_pages.mjs
node scripts/build_dist.mjs
python3 -m http.server 4199 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:4199/dist/index.html
```
