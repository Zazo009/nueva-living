# nueva-media

A Cloudflare Worker that answers requests for the site's videos and PDFs from R2
(bucket `nuevaliving`) at the URLs they have always had. Visitors reach Cloudflare
before Netlify, so it sits in front: a path on the allowlist is served from R2 and
everything else is handed to Netlify untouched. Netlify is not connected to R2 and
does not know it exists.

## Current state

The build still copies the files into `dist/` and they are still in git, so Netlify
holds a complete copy. R2 is therefore a layer on top, and switching the routes off
puts every URL back exactly where it was. The files have **not** been removed from
git or from the build.

## What is served

Only the keys in `src/published.json`, which `make-allowlist.mjs` generates from
`dist/`. A path being present in the bucket does not make it public.

This matters because the bucket holds more than the build ships: two hero videos
(`hero-desktop-v2.mp4`, `hero-mobile-v2.mp4`) are kept only as a revert path and are
deliberately not published. Uploading "every tracked mp4 and pdf" once made them
reachable for a few minutes; the allowlist is why that cannot happen again.

## Deploying

After a build, regenerate the list, then deploy:

```
node scripts/build_dist.mjs && node infra/media-worker/make-allowlist.mjs
cd infra/media-worker && npx wrangler deploy
```

Needs `npx wrangler login` once, as the Cloudflare account that owns the zone.

## Things that are not obvious

- **Route patterns cannot have a wildcard in the middle.** `projects/*/floorplans/*`
  is invalid, so there is one exact prefix per directory (37 of them). A new project
  directory that gains a PDF needs a route added in `wrangler.toml`, or its files
  keep coming from Netlify.
- **Wrangler never removes a route.** Dropping one from `wrangler.toml` and
  redeploying leaves it live. Remove it in the Cloudflare dashboard (Workers
  Routes), or the old route keeps invoking the worker.
- **A route outlives the files it was for.** Directories also hold thumbnails and
  images; the worker passes those to Netlify without reading R2.
- **R2 reports a range even for a plain read.** Answering 206 whenever it does broke
  ordinary GETs; 206 is only correct when the request carried a `Range` header.
- `x-media-source: r2` on a response says which origin answered. A file served by
  Netlify has no such header.
