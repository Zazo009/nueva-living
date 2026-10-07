// Serves the site's videos and PDFs from R2 at the URLs they always had.
//
// Visitors reach Cloudflare before Netlify, so this sits in front of it: a request
// for a path that exists in the bucket is answered from R2, and anything else is
// handed on to Netlify untouched. Netlify never learns that R2 exists.
//
// That fall-through is the safety property. The route patterns are deliberately
// broader than the files (a floorplans/ directory also holds thumbnails that stay
// on Netlify), so a miss is normal, and so is a bucket that is empty or offline:
// the worst case is that the request behaves exactly as it did before this existed.
//
// Keys are the repository paths, with no transformation: assets/liora/video/x.mp4
// is the object assets/liora/video/x.mp4.
//
// Only files in published.json are ever served. The bucket holds more than the
// build publishes -- two hero videos are kept as a revert path and are not shipped --
// and a path that is merely present in R2 is not thereby public. The list is
// generated from dist/ by make-allowlist.mjs, so it follows the build.
import published from './published.json';

const PUBLISHED = new Set(published);

export default {
  async fetch(request, env) {
    if (request.method !== 'GET' && request.method !== 'HEAD') return fetch(request);

    const url = new URL(request.url);
    // Key is the URL path, nothing more: a request can only ever read the object
    // whose name is its own path. An earlier test route that mapped /__r2test/<key>
    // to <key> let any object in the bucket be read by name, including files the
    // build deliberately does not publish, and is gone for that reason.
    const key = decodeURIComponent(url.pathname.slice(1));
    // Not on the list: not ours to serve. Hand it on, which costs no R2 read, so
    // the thumbnails and images that share a directory with a PDF pass straight through.
    if (!PUBLISHED.has(key)) return fetch(request);

    let object;
    try {
      // Range and conditional headers go straight to R2, which implements them.
      object = await env.MEDIA.get(key, { range: request.headers, onlyIf: request.headers });
    } catch {
      return fetch(request);          // never let a bucket error take the media down
    }
    if (object === null) return fetch(request);

    const headers = new Headers();
    object.writeHttpMetadata(headers);          // content-type and cache-control as stored
    headers.set('etag', object.httpEtag);
    headers.set('accept-ranges', 'bytes');
    // Which origin answered, so a check can tell R2 from Netlify without guessing.
    headers.set('x-media-source', 'r2');

    // A failed precondition (If-None-Match and friends) comes back without a body.
    if (!('body' in object) || object.body === undefined) {
      return new Response(null, { status: 304, headers });
    }

    // 206 only when the client asked for a range. R2 reports a range on the object
    // even for a plain read, and trusting that answered every ordinary GET -- a PDF
    // in a browser, say -- with "partial content" for a body that was the whole file.
    let status = 200;
    if (request.headers.has('range') && object.range) {
      const { offset = 0, length = object.size - offset } = object.range;
      headers.set('content-range', `bytes ${offset}-${offset + length - 1}/${object.size}`);
      headers.set('content-length', String(length));
      status = 206;
    } else {
      headers.set('content-length', String(object.size));
    }

    return new Response(request.method === 'HEAD' ? null : object.body, { status, headers });
  },
};
