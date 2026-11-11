// Fails if a secret is read with a cleaner that leaves whitespace inside it.
//
// clean() collapses runs of whitespace into a single space. For prose that is
// right. For a token it is a disaster, because the token stays broken and
// stops looking broken: a dataset token pasted into Netlify with a line break
// became a token with a space in the middle, and Meta answered
//
//   {"error":{"message":"Bad signature","type":"OAuthException","code":190}}
//
// which names neither the variable nor the whitespace. The same shape on a
// shared secret is a 401 that reads as "you typed the wrong value", and the
// hour after that is spent re-copying a string that was always correct.
//
// So every environment variable holding one opaque string -- a token, a
// dataset id, a shared secret -- must be read through credential(), which
// removes whitespace rather than tidying it.
import { readFileSync, readdirSync } from 'node:fs'
import { join } from 'node:path'

const DIR = 'netlify/functions'

// Names that are one opaque string. A URL is not one of these: it is read
// with clean() on purpose and a space in it is visible in the logs.
const CREDENTIALS = /^(.*_SECRET|.*_TOKEN|.*_KEY|META_.*_DATASET_ID|META_DATASET_ID)$/

const failures = []

// The name proves nothing -- cleanEnvironmentValue was the right name for a
// function that only trimmed the ends. So the body is what is checked: the
// definition in the same file, or in the library it is imported from, must
// replace every whitespace character with nothing.
const LIBRARIES = ['netlify/functions/lib/meta-capi.js', 'lib/nueva-property-sync.cjs']
const libraryText = LIBRARIES.map(f => readFileSync(f, 'utf8')).join('\n')

function stripsWhitespace(fn, text) {
  const body = new RegExp(`function ${fn}\\(|const ${fn} = `)
  for (const source of [text, libraryText]) {
    if (!body.test(source)) continue
    const from = source.search(body)
    // The whole-whitespace replacement has to appear inside the next few
    // lines of that definition, not anywhere in the file.
    if (/replace\(\/\\s\+\/g, ''\)/.test(source.slice(from, from + 600))) return true
  }
  return false
}


function walk(dir) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name)
    if (entry.isDirectory()) { walk(path); continue }
    if (!entry.name.endsWith('.js')) continue

    const text = readFileSync(path, 'utf8')
    for (const match of text.matchAll(/(\w+)\(\s*process\.env\.([A-Z][A-Z0-9_]+)\s*\)/g)) {
      const [, fn, name] = match
      if (!CREDENTIALS.test(name)) continue
      if (!stripsWhitespace(fn, text)) {
        failures.push(`${path}: ${name} is read with ${fn}(), which does not remove whitespace from inside the value`)
      }
    }
    // The header carrying the shared secret is the same kind of value.
    for (const match of text.matchAll(/(\w+)\(event\.headers\['x-webhook-secret'\]/g)) {
      if (!stripsWhitespace(match[1], text)) {
        failures.push(`${path}: the x-webhook-secret header is read with ${match[1]}(), which leaves whitespace in it`)
      }
    }
  }
}
walk(DIR)

if (failures.length) {
  console.error(`\nCredentials read with the wrong cleaner (${failures.length}):\n`)
  for (const failure of failures) console.error(`  ${failure}`)
  console.error('\nA credential with whitespace left in it fails as "Bad signature" or as a')
  console.error('401, and neither says which variable or that whitespace is the cause.\n')
  process.exit(1)
}

console.log('Credentials: every token, id and secret is read with credential(), which strips whitespace rather than tidying it.')
