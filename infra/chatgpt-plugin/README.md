# Nueva Living in the ChatGPT and Claude directories

The MCP server (`netlify/functions/nueva-mcp.js`, live at https://nuevaliving.com/mcp) already works as a
custom connector. This folder holds what the two public directories ask for on top of that, so it can be
listed and found by people who have never heard of Nueva Living.

Both submissions are made by the account owner in the providers' own portals. The policy acknowledgements
are theirs to give.

## What the reviews check, and where we stand

| Requirement | Where |
| --- | --- |
| Every tool has a title and explicit `readOnlyHint` / `destructiveHint` / `openWorldHint` | `nueva-mcp.js`; `request_details` is `destructiveHint: true`, so both hosts ask before an enquiry is sent |
| Read and write are separate tools; no catch-all tool | three tools, two read-only |
| Descriptions say what a tool does and do not promote | `nueva-mcp.js` |
| Collect only what the task needs; contact details only with consent | `request_details` requires `consent: true`; searches carry no personal data |
| Privacy policy with categories, purposes, recipients, retention and rights | `privacy-policy.html`, section "Nueva Living in ChatGPT and Claude"; enquiries kept 24 months after the last contact |
| Support contact, terms | `contact.html`, `legal-notice.html` |
| Widget CSP is declared and narrow | `WIDGET_META` in `nueva-mcp.js` (own domain and Google Fonts only, no iframes) |
| Public documentation | https://nuevaliving.com/ai.html |

A reviewer who runs the contact test case creates a real enquiry in the CRM, named "Review Tester". It is
not a lead; delete it when it arrives.

## Claude: connectors directory

Portal: https://claude.ai/directory/manage → Submit new → MCP connector. Paid plan; on Team/Enterprise an
Owner submits.

- **URL:** `https://nuevaliving.com/mcp`
- **Authentication:** none (public data)
- **Name:** Nueva Living
- **One-liner (≤200):** Search new-build and off-plan homes on the Costa del Sol, Spain, with developers' list prices, delivery dates, floor plans and a map.
- **Description (≤2000):** use `longDescription` from `plugin.json`
- **Categories:** Lifestyle; Search (or the closest the portal offers)
- **Documentation URL:** https://nuevaliving.com/ai.html
- **Privacy policy URL:** https://nuevaliving.com/privacy-policy.html
- **Support contact:** contact@nuevaliving.com
- **Icon:** `assets/logo.png` (512 × 512)
- **Reads or writes:** both. Two read-only search tools; one tool that sends an enquiry, only after the user agrees.
- **What users need before connecting:** nothing; no account.
- **Data handling:** first-party API (our own site data); no health data; no sponsored content.
- **Test & launch:** every tool has been run in Claude as a custom connector.
- **Screenshots (MCP Apps, 3–5 PNG, ≥1000 px wide, cropped to the app's response, each with its prompt):** take them from the prompts in `plugin.json`.

## ChatGPT: plugin directory

Portal: https://platform.openai.com/plugins → Upload plugin. First verify the organisation
(Settings → Organization → General → individual or business verification).

1. Replace `REPLACE_WITH_DEMO_VIDEO_URL` in `plugin.json` with a link to a short screen recording of the
   five positive test cases in ChatGPT (developer mode), viewable without signing in.
2. Zip the contents of this folder, not the folder itself:
   `cd infra/chatgpt-plugin && zip -r ../../nueva-living-chatgpt.zip plugin.json mcp.json assets`
3. Upload, then in MCPs → Connect, complete the domain verification. The portal shows a token that has to
   be served as plain text at `https://nuevaliving.com/.well-known/openai-apps-challenge`. That needs a
   deploy (`build_dist.mjs` writes it), so send the token over and it goes out with the next build.
4. Run each test case, then Submit for review. Publishing is a separate step after approval.
