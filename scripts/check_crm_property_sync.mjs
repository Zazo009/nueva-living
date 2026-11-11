// Fails if any project would be refused by the CRM's property sync.
//
// Armani Residences Marbella carried "priceMax": 0 -- a placeholder for a
// figure the developer never gave us, since they quoted only a starting price.
// The sync reads `crm.priceMax ?? highestAvailabilityPrice(project)`, and 0 is
// not nullish, so the fallback never ran and the payload said this project
// costs at most nothing. Validation rejected it, correctly, with
//
//   CRM property sync skipped: Armani Residences Marbella: price_max must be
//   greater than or equal to price_min
//
// one grey line in a twelve-minute build log. The site kept publishing the
// project, the CRM simply never had a row for it, so it could not be searched,
// linked to a partner, or attached to a lead. It was 111 projects on the site
// against 110 in the CRM, and the missing one was invisible from both ends.
//
// This runs the real sync functions over every project, so anything the CRM
// would refuse -- an area outside the allowed list, a bad URL, bedrooms the
// wrong way round -- stops the build with the project named, rather than
// quietly dropping it.
//
// It is not enough on its own, and the first version of this guard proved it.
// Removing the placeholder ceiling from Armani made this pass, and the CRM
// still answered 422: name, area, price_min and price_max are required. The
// guard ran the SITE's validator, where price_max may be absent, while the
// CRM's webhook demanded it. Two validators, one boundary, and the guard
// watching the near side of it.
//
// So the CRM's own rules are stated below, deliberately as a copy. They live
// in another repository and a build here cannot import them; writing them out
// is what makes the divergence visible when someone changes one side. The CRM
// has a matching guard holding its webhook to the same list.
import { createRequire } from 'node:module'
import { readdirSync, readFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'

const require = createRequire(import.meta.url)
const {
  projectToPropertyPayload,
  normalizePropertyPayload,
  validatePropertyPayload,
} = require('../lib/nueva-property-sync.cjs')

// The CRM's property webhook, as of migration 045. Kept in step by hand with
// src/app/api/webhook/property/route.ts in the CRM repository.
//
//   required:  name, area, price_min
//   optional:  price_max -- a project may publish only a starting price, but
//              a ceiling below the floor is refused, and so is a non-number
//
// A rule relaxed there is harmless here; a rule tightened there and not
// copied here is a project that builds, deploys and never arrives.
function crmWebhookErrors(payload) {
  const errors = []
  for (const field of ['name', 'area', 'price_min']) {
    if (payload[field] === undefined || payload[field] === null || payload[field] === '') {
      errors.push(`the CRM requires ${field} and the payload has none`)
    }
  }
  const max = payload.price_max
  if (max !== undefined && max !== null) {
    if (!Number.isFinite(Number(max))) {
      errors.push(`the CRM requires price_max to be a number, and this is ${JSON.stringify(max)}`)
    } else if (Number(max) < Number(payload.price_min)) {
      errors.push(`the CRM refuses price_max ${max} below price_min ${payload.price_min}`)
    }
  }
  return errors
}

const DIR = 'content/liora-projects'

const failures = []
let checked = 0

for (const slug of readdirSync(DIR).sort()) {
  const file = join(DIR, slug, 'project.json')
  if (!existsSync(file)) continue

  const project = JSON.parse(readFileSync(file, 'utf8'))
  if (project.archived) continue
  checked++

  let errors
  let payload
  try {
    payload = normalizePropertyPayload(projectToPropertyPayload(project), { infer: true })
    errors = [...validatePropertyPayload(payload), ...crmWebhookErrors(payload)]
  } catch (error) {
    failures.push(`${slug}: the sync threw -- ${error.message}`)
    continue
  }
  for (const error of errors) failures.push(`${slug}: ${error}`)
}

if (!checked) {
  console.error(`\nNo projects found under ${DIR}/. This guard checked nothing.\n`)
  process.exit(1)
}

if (failures.length) {
  console.error(`\n${failures.length} project(s) the CRM would refuse:\n`)
  for (const failure of failures) console.error(`  ${failure}`)
  console.error('\nA refused project still publishes on the site. It just never reaches the')
  console.error('CRM, so it cannot be searched, linked to a partner, or attached to a lead --')
  console.error('and the only sign is one line in the build log.\n')
  process.exit(1)
}

console.log(`CRM property sync: all ${checked} projects produce a payload the CRM accepts.`)
