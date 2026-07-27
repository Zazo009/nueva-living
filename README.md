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
CRM_PROPERTY_WEBHOOK_URL=https://marbella-crm.vercel.app/api/webhook/property
CRM_WEBHOOK_SECRET=change-me
PROPERTY_SYNC_TOKEN=use-a-separate-random-admin-to-server-token
ALLOWED_ORIGINS=https://nuevaliving.com,https://www.nuevaliving.com
```

`CRM_WEBHOOK_SECRET` must be available to both Netlify Functions and Builds.
Functions use it for lead/property forwarding, while the property builder uses it
to sync generated projects. Keep it out of HTML and client-side JavaScript.

The browser submits to `/.netlify/functions/nueva-lead`. The function adds the
webhook secret server-side before forwarding the lead to the CRM; never expose
`CRM_WEBHOOK_SECRET` in HTML or client-side JavaScript.

Successful CRM submissions show an inline confirmation. If client-side JavaScript
is unavailable, the HTML form posts to the same Netlify Function and redirects to
the thank-you page only after the CRM accepts the lead. CRM acceptance is the
authoritative success signal; the browser never receives the webhook secret.

## Property CRM Sync

The existing property creation path is file-based:

```text
content/liora-projects/<slug>/project.json
```

When `scripts/build_property_pages.mjs` runs with `CRM_WEBHOOK_SECRET` available,
every generated project is normalized and sent to the CRM property webhook.
The CRM updates matching `name + area` records, so repeat deploys do not create
duplicates. Set `CRM_PROPERTY_SYNC_STRICT=true` only if a CRM sync failure should
also fail the website build.

An external admin backend can trigger the same server-side flow by posting the
property JSON to:

```text
POST /.netlify/functions/nueva-property
X-Property-Sync-Token: <PROPERTY_SYNC_TOKEN>
Content-Type: application/json
```

The admin sync token is separate from the CRM webhook secret. A browser admin
must use authenticated Netlify Identity, or its backend must add the sync token
server-side. Never place either secret in public JavaScript.

## Website Tracking

Every production page loads the shared `assets/liora/nueva-tracking.js` file.
Browser events are posted to the same-origin Netlify endpoint:

```text
POST /.netlify/functions/nueva-track
```

The function forwards events to the CRM tracking API. The optional
`CRM_TRACKING_URL` environment variable can override the default
`https://marbella-crm.vercel.app/api/track` endpoint. No tracking secret or CRM
credential is exposed in browser JavaScript.

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
