# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
# -*- coding: utf-8 -*-
"""Writes the English record content/liora-projects/la-quinta-summit-residences-villas/project.json (no i18n yet).
Every figure is traced to a document in OPEN_ITEMS.md. Run: python3 build_en.py"""
import json, os, sys
sys.path.insert(0, '/Users/sasanraftari/Downloads/SkyMarbella_work')
sys.path.insert(0, '/Users/sasanraftari/Downloads/SkyMarbella_work/specs')
from gallery_def import GALLERY
from units_data import apartments, villas
from spec_apartments import SPEC_APARTMENTS
from spec_villas import SPEC_VILLAS
from PIL import Image

SLUG = 'la-quinta-summit-residences-villas'
NAME = 'La Quinta Summit Residences & Villas'
ROOT = '/Users/sasanraftari/Projects/nueva-living'
M = f'assets/liora/projects/{SLUG}/media/'
F = f'assets/liora/projects/{SLUG}/floorplans/'
PLANS = json.load(open('/Users/sasanraftari/Downloads/SkyMarbella_work/plans_manifest.json'))


def dims(path):
    im = Image.open(os.path.join(ROOT, path)); return im.width, im.height


def img(path, alt):
    w, h = dims(path); return {'src': path, 'alt': alt, 'width': w, 'height': h}


# ---- gallery ---------------------------------------------------------------------------------
ALT = {}
items = []
for src, name, cat, cap, alt in GALLERY:
    alt = alt.replace('with each villa numbered from 1 to 18', 'with the villas numbered')
    ALT[name] = alt
    d = img(M + name + '.jpg', alt); d['category'] = cat; d['caption'] = cap; items.append(d)

# ---- quality specifications --------------------------------------------------------------------
GROUPS = SPEC_APARTMENTS + SPEC_VILLAS
spec = {
    'headlineHtml': 'What the homes are <em>built with</em>',
    'copy': 'The developer’s two quality specifications, one for the apartments and one for the villas, group by group, with the product brands as they name them.',
    'sourceNote': 'Source: the developer’s quality specification for the apartments (12 pages) and for the villas (18 pages). Both are marked provisional, not legally binding and subject to change, carry no date or version number, and say furniture is not part of the specification or the price. Where a line says “or similar”, so does this page. Three points differ between documents: the villa building-specifications summary names Florim Etoile Illusion porcelain for the secondary bathrooms, where the villa quality specification names Del Conca Premiere Amazzonite; an older apartment “memory of qualities” gives parking for 2, 3 or 4 cars depending on the home and a sauna and hammam for penthouses, where the quality specification gives 2 cars and a sauna and hammam for the top-level villa-type penthouse only; and the apartment price list gives every apartment two parking spaces and a storage room. We confirm which applies.',
    'groups': [{'name': n, 'items': i} for n, i in GROUPS],
}

# ---- units ---------------------------------------------------------------------------------------
def num(s):
    return s  # price-list decimals are already '216.02'


def eur(n):
    return f'EUR {n:,}'


units = []
for a in apartments:
    if not a['price']:
        continue
    t = a['type'].split('/')
    kind = t[1]
    if kind == 'GF':
        floor = f"Block {a['block']}, Ground floor & basement"
    elif kind == '1st':
        floor = f"Block {a['block']}, First floor"
    elif kind == 'PH':
        floor = f"Block {a['block']}, Duplex penthouse"
    else:
        floor = f"Block {a['block']}, Penthouse"
    size = f"{a['interior']} sqm built, {a['ext']} sqm terrace" + (f", {a['garden']} sqm garden" if a['garden'] else '')
    lv = PLANS['apt:' + a['door']]
    main = {'GF': 'ground-floor', '1st': 'first-floor', 'PH': 'penthouse-floor'}.get(kind, 'penthouse-floor')
    mainsrc = next(F + n for k, _, n in lv if k == main)
    u = {'reference': a['door'], 'floor': floor, 'bedrooms': f"{a['bed']} bedrooms", 'size': size,
         'price': eur(a['price']), 'floorplan': mainsrc}
    if len(lv) > 1:
        u['floorplans'] = [{'src': F + n, 'floor': label} for _, label, n in lv]
    units.append(u)
for v in villas:
    if not v['price']:
        continue
    lv = PLANS['villa:' + str(v['no'])]
    u = {'reference': f"Villa {v['no']}", 'floor': 'Basement, ground floor & first floor', 'bedrooms': f"{v['bed']} bedrooms",
         'size': f"{v['interior']} sqm built, {v['terr']} sqm terrace, {v['usable']} sqm usable, {v['plot']:,} sqm plot",
         'price': eur(v['price']),
         'floorplan': F + next(n for k, _, n in lv if k == 'ground-floor'),
         'floorplans': [{'src': F + n, 'floor': label} for _, label, n in lv]}
    units.append(u)
assert len(units) == 40

AMEN = ['Private pool', 'Communal outdoor pool', 'Indoor pool', 'Gym', 'Spa', 'Sauna', 'Hammam', 'Massage room', 'Lift',
        'Home automation', 'Underfloor heating', 'Aerothermal system', 'Air conditioning', 'Two parking spaces', 'Storage room',
        '24-hour security', 'Gated community', 'Concierge service', 'Sea and mountain views', 'Outdoor kitchen',
        'Pre-installation for electric vehicle charging', 'Walk-in dressing rooms']

d = {
    'slug': SLUG, 'output': f'property-{SLUG}.html', 'archived': False,
    'name': NAME, 'shortName': 'La Quinta Summit', 'titleHtml': 'La Quinta Summit <em>Residences &amp; Villas</em>',
    'description': 'Fifty apartments and penthouses and sixteen villas in a gated community at the top of La Quinta, in Benahavís, with sea and mountain views. Forty homes are available: apartments and penthouses from EUR 1,495,000 and villas from EUR 6,495,000, plus VAT. Delivery is given as the third quarter of 2027.',
    'canonical': f'https://nuevaliving.com/property-{SLUG}.html',
    'seoDescription': 'Fifty apartments and penthouses and sixteen villas at the top of La Quinta, Benahavís, in a gated community with sea views. 40 homes available, from EUR 1,495,000 plus VAT.',
    'twitterDescription': 'Apartments and penthouses with their own pools, and villas with a private basement and lift, in a gated community at the top of La Quinta, Benahavís. From EUR 1,495,000 plus VAT.',
    'schema': {'price': '1495000', 'priceCurrency': 'EUR', 'category': 'Apartment', 'areaServed': 'Benahavís, Málaga, Spain'},
    'crm': {
        'realName': 'The Sky Marbella', 'developer': '',
        'realDeveloper': 'Rivestia Costa del Sol, S.L. (named in the payment terms, the brochure and the plan sheets). Architects named in the documents: Manuel Burgos (villas) and Teodoro Cabrilla (apartments). Commercialiser (master agent): Palmera Advantage Alliance S.L., trading as Marlo Property.',
        'area': 'Benahavis', 'address': 'La Quinta, El Madroñal, Benahavís, Málaga',
        'priceMin': 1495000, 'priceMax': 8950000, 'currency': 'EUR', 'bedroomsMin': 2, 'bedroomsMax': 6,
        'propertyTypes': ['apartment', 'penthouse', 'villa'],
        'totalUnits': 66, 'availableUnits': 40,
        'constructionStatus': 'Under construction on the developer’s Word description (last saved June 2026); the PDF of October 2026 and the price lists do not state a stage',
        'brochureUrl': '', 'amenities': AMEN, 'reference': 'MA-BN-QUINTASUMMIT'},
    'contact': {'whatsappNumber': '34645446624', 'whatsappMessage': f'Hello Nueva Living, I would like information about {NAME}.'},
    'hero': {'eyebrow': '40 of 66 homes available', 'location': 'La Quinta, Benahavís', 'startingPrice': 'From EUR 1,495,000 + VAT',
             'type': 'Apartments, penthouses & villas', 'delivery': 'Q3 2027'},
    'card': {'order': 116, 'label': 'La Quinta', 'locExtended': 'La Quinta, Benahavís',
             'description': 'Fifty apartments and penthouses with private pools and sixteen villas with a private basement, in a gated community at the top of La Quinta. Forty homes are available.',
             'meta': [['From', 'EUR 1,495,000 + VAT'], ['Type', 'Apartments, penthouses & villas'], ['Delivery', 'Q3 2027']],
             'badge': 'Under Construction', 'typeTag': 'La Quinta'},
    'quickFacts': [
        ['Starting price', 'From EUR 1,495,000 + VAT'],
        ['Location', 'La Quinta, Benahavís'],
        ['Property type', 'Apartments, penthouses & villas'],
        ['Bedrooms', '2-6 bedrooms'],
        ['Built area, apartments', '129.22 - 362.93 sqm built'],
        ['Built area, villas', '811 - 937 sqm built'],
        ['Delivery', 'Q3 2027'],
        ['Availability', '40 of 66 homes available'],
    ],
    'discovery': {
        'priority': 116, 'featured': False, 'releaseDate': '2026-10', 'price': '1495000', 'area': 'benahavis',
        'bedrooms': '2-6 bedrooms', 'status': 'Under construction', 'availability': '40 of 66 homes available',
        'propertyTypes': ['apartment', 'penthouse', 'villa'],
        'lifestyleTags': ['Panoramic Views', 'Sea Views', 'Privacy & Security', 'Wellness'],
        'architectureTags': ['Contemporary', 'Duplex & Penthouse', 'Villas & Apartments'],
        'locationTags': ['Benahavís', 'Golden Triangle', 'Gated Community', 'Hillside Views'],
        'investmentTags': ['Second Home', 'Lifestyle Investment', 'International Buyer', 'Staged Payment Plan'],
        'practicalTags': ['Villas & Apartments', 'Private Pool', 'Lift', 'Underfloor Heating', 'Gym', 'Spa'],
        'cardTags': ['Sea Views', 'Private Pool', 'Gated Community'],
        'advisoryBadge': 'Best for buyers who want a private pool and sea views in a gated hilltop community'},
    'images': {
        'hero': img(M + 'villa-exterior-dusk-pool.jpg', ALT['villa-exterior-dusk-pool']),
        'architecture': img(M + 'apartments-exterior-curved-terraces.jpg', ALT['apartments-exterior-curved-terraces']),
        'lifestyle': img(M + 'villa-covered-terrace-lounge.jpg', ALT['villa-covered-terrace-lounge']),
        'privateViewing': img(M + 'villa-balcony-sea-view.jpg', ALT['villa-balcony-sea-view'])},
    'media': {
        'headlineHtml': 'The homes <em>in detail</em>',
        'copy': 'Photographs of the finished pilot villa, computer-generated views of the apartments and the shared amenities, and a photograph of the developer’s site model. The plans of every available home are on its card below.',
        'note': 'The villa photographs show the pilot villa (Villa 10), furnished and styled; the furniture, art and decoration are not included. The apartment and amenity pictures are computer-generated. The developer’s documents are provisional and subject to change.',
        'items': items},
    'overview': {
        'headlineHtml': 'Sixty-six homes, <em>forty available</em>',
        'copy': [
            'La Quinta Summit is a gated community of 50 apartments and penthouses and 16 villas at the top of La Quinta, in Benahavís, on the southern edge of El Madroñal. The developer describes panoramic views of the bay of Marbella, the Mediterranean and the mountains, 24-hour security and shared amenities.',
            'Every apartment has its own private pool, two covered parking spaces and a storage room. The apartments are duplex ground-floor homes with a private basement, middle-floor homes and duplex penthouses, with two to five bedrooms. The villas have five or six bedrooms over a basement, a ground floor and an upper floor, with a lift, a private pool and a basement that can hold a gym, a massage room, a sauna and a hammam.',
            'The price lists mark 26 homes as Reserved: 21 apartments and 5 villas. They are not listed here. The 40 homes still priced are listed with their plans, from EUR 1,495,000 to EUR 8,950,000, excluding VAT.'],
        'metrics': [['Development', '50 apartments and 16 villas'], ['Available', '40 homes'], ['Price range', 'EUR 1,495,000 - EUR 8,950,000 + VAT'], ['Delivery', 'Q3 2027']]},
    'why': {
        'headlineHtml': 'Why this project <em>matters</em>',
        'copy': 'Two product lines in one gated community: apartments from EUR 1,495,000 and villas from EUR 6,495,000, with the finishes written down product by product.',
        'points': [
            ['Who it is for', 'Buyers who want sea and mountain views, a private pool and a gated, secure setting in Benahavís, either in a pool-equipped apartment or in a villa with its own basement and lift.'],
            ['What makes it different', 'Every apartment has its own pool, and the shared amenities include an indoor pool, a gym and spa, a meeting room and a concierge. Each villa has a finished private basement with a lift.'],
            ['Why location matters', 'The community sits at the highest point of the urbanisation, at the top of La Quinta, with the golf courses of the Golden Triangle and the AP-7 motorway a few minutes away on the developer’s account.'],
            ['Why check availability', 'Of the 66 homes, 26 are marked Reserved in the price lists. Nueva Living reconfirms price and availability with the developer before any viewing.']]},
    'architecture': {
        'headlineHtml': 'Two designs, <em>one setting</em>',
        'copy': [
            'The apartments are a curved, terraced building with wave-shaped slab edges, glass balustrades and a private pool for each home. The villas are flat-roofed houses in render, porcelain and wood, with a pool, planted terraces and a covered outdoor living area.',
            'Each product line has its own specification: the apartments have chevron parquet throughout the living areas, the villas large-format porcelain downstairs and herringbone parquet upstairs. The full lists are in the specification section.'],
        'highlights': [
            ['Structure', 'Reinforced concrete walls and columns with waffle or solid slabs, on shallow and deep foundations as each plot requires.'],
            ['Facade', 'Perforated solid brick with insulated cavity, finished in render, porcelain, aluminium slats or natural wood according to the design.'],
            ['Glazing', 'Thermally broken aluminium with solar-control, low-emissivity double glazing and floor-level sliding doors.'],
            ['Climate', 'Aerothermal hot water, ducted air conditioning zoned room by room and water-based underfloor heating.'],
            ['Control', 'Home automation for lighting, climate and, in the apartments, sound and access, from a touchscreen or a mobile device.']]},
    'qualitySpecs': spec,
    'residences': {
        'headlineHtml': 'Five types of home, <em>one community</em>',
        'copy': 'Each card describes a type from the developer’s price lists. The areas are the price list’s figures for every home of the type, including those marked Reserved; the count and the prices are for the homes still listed. The plan sheets of the individual apartments give slightly different areas, so the figures are indicative.',
        'items': [
            {'name': 'Duplex ground-floor apartments, 3 and 4 bedrooms', 'points': [
                'The 3-bedroom homes have 216.02 to 216.63 sqm built, 131.71 to 291.63 sqm of terraces and porches and, for eight of the 14, a garden of 21.93 to 114.54 sqm. Twelve of the 14 are available, from EUR 1,950,000 to EUR 2,745,000.',
                'The 4-bedroom homes in blocks 4 to 6 have 316.15 to 316.20 sqm built, 429.61 to 484.62 sqm of terraces and porches and a garden of 101.36 to 276.12 sqm. One of the three is available, at EUR 3,300,000.',
                'Each has a ground floor and a fully finished private basement with direct garage access, a private pool, two covered parking spaces and a storage room.']},
            {'name': 'Middle-floor apartments, 2 bedrooms', 'points': [
                'On one level, with 129.22 to 129.24 sqm built and 92.97 to 150.75 sqm of terraces and porches, and a private pool.',
                'Five of the 14 are available, from EUR 1,495,000 to EUR 1,650,000.',
                'The price list also holds three 3-bedroom middle-floor homes of 187.71 to 187.87 sqm built in blocks 4 to 6, all marked Reserved.']},
            {'name': 'Duplex penthouses, 4 bedrooms', 'points': [
                'On two levels, with 253.01 to 253.07 sqm built and 270.17 to 360.98 sqm of terraces and porches, and a private pool.',
                'Ten of the 12 are available, from EUR 3,245,000 to EUR 3,595,000.']},
            {'name': 'Top-level penthouses, 5 bedrooms', 'points': [
                'Three of these have 362.93 to 402.05 sqm built and 567.14 to 619.24 sqm of terraces and porches; a fourth, of 538.97 sqm built, is marked Reserved with the others.',
                'Only one is available: a 362.93 sqm home with 567.14 sqm of terraces and porches, at EUR 4,950,000.',
                'The quality specification gives the villa-type penthouse a private sauna and hammam.']},
            {'name': 'Villas, 5 and 6 bedrooms', 'points': [
                'Sixteen villas on plots of 690 to 1,705 sqm, with 811 to 937 sqm built, 183 to 249 sqm of terraces and porches and 743.96 to 887.79 sqm usable.',
                'Eleven are available, from EUR 6,495,000 to EUR 8,950,000: five with 5 bedrooms and six with 6.',
                'Over three levels, with a lift, an infinity-edge pool, a finished private basement and covered parking for two cars.']}]},
    'lifestyle': {
        'headlineHtml': 'Pools, wellness, <em>views and security</em>',
        'copy': 'What the documents give for the private and shared amenities.',
        'panels': [
            ['Private pools', 'Every apartment has its own private pool. Each villa has an infinity-edge pool in glass mosaic with saline chlorination and lighting.'],
            ['Shared wellness', 'A communal indoor pool, a fully equipped gym and spa, a communal outdoor pool in an organic shape with a solarium, and a meeting room for residents. The brochure also lists a massage area, a hammam, a Turkish bath and a sauna.'],
            ['Villa basement', 'A finished private basement with an en-suite bedroom, a laundry and a multi-purpose area, and a space that can be converted into a gym beside a massage room, a sensory shower, a hammam and a sauna.'],
            ['Views and security', 'Panoramic views of the bay of Marbella, the Mediterranean and the mountains, a gated community, 24-hour security and a concierge service.']]},
    'location': {
        'headlineHtml': 'La Quinta, <em>Benahavís</em>',
        'copy': 'The community stands at the top of La Quinta in Benahavís, on the southern edge of El Madroñal, in the Golden Triangle of Marbella, Estepona and Benahavís. The developer’s brochure gives the AP-7 motorway and the first golf course as 5 minutes away, Puerto Banús as 15, Sotogrande as 30 and Málaga airport as 45, and names five golf courses 5 to 15 minutes by car: La Quinta, Los Arqueros, Los Naranjos, Las Brisas and Aloha. Its description gives Puerto Banús as ten minutes.',
        'mapLabelHtml': 'La Quinta, <em>Benahavís</em>', 'mapLabelPlain': 'La Quinta, Benahavís', 'mapArea': 'benahavis',
        'site': [36.5185, -5.002], 'siteSource': 'area-geocode',
        'distances': [['Puerto Banús', 'Nearby'], ['Málaga Airport', 'Approx. 45 min']]},
    'investment': {
        'headlineHtml': 'How the <em>purchase works</em>',
        'copy': 'The terms are those of the developer’s price lists and payment terms. We confirm the current amounts and dates in writing before you reserve.',
        'cards': [
            ['Prices', 'Apartments and penthouses from EUR 1,495,000 to EUR 4,950,000 and villas from EUR 6,495,000 to EUR 8,950,000, excluding VAT. Furniture is not included. The price lists are provisional and not legally binding.'],
            ['VAT and costs', 'The payment terms add VAT to every instalment. The documents do not state the rate or any other tax or purchase cost, so we confirm them in writing.'],
            ['Apartment payments', 'A reservation fee of EUR 20,000 for homes up to EUR 2m, EUR 35,000 from EUR 2m to EUR 4m or EUR 50,000 above EUR 4m. Then 35% at the private purchase contract (less the reservation), 15% two months later and the final 50% at the deed and delivery, each plus VAT.'],
            ['Villa payments', 'A reservation fee of EUR 50,000. Then 35% at the private purchase contract (less the reservation), 15% three months later and the final 50% at the deed and the handover of keys, each plus VAT.']]},
    'trustDossier': {
        'headlineHtml': 'What we check <em>before you commit</em>',
        'copy': 'We confirm the current status of each item with the developer before any reservation, and put the answers in writing.',
        'cards': [
            ['Stage, licence and delivery', 'The October 2026 description gives the third quarter of 2027 for villas and apartments. The Word version of June 2026 gives the second quarter for villas and the third for apartments and says the works are under way; a public sales listing gives the second quarter for villas and the fourth for apartments and says the structure is complete. No document gives a licence or a bank guarantee, so we ask for both and for the contractual date.'],
            ['Areas and counts', 'The apartment plan sheets give slightly different areas from the price list (home 11A is 216.61 sqm on its plan and 216.02 in the list), a few list rows do not add up to their own totals, and the sheets are headed as a basic project for 48 homes where the list has 50 apartments. The description gives apartments of 130 to 473 sqm where the list runs from 129.22 to 538.97. We ask for the figures the contract uses.'],
            ['Villa numbers and names', 'The villa plan files are numbered differently from the price list for five villas, the list has no plan for its sixteenth villa, and the brochure and the list give different names for the same villas. This page uses the price list’s numbers, checked against each plan’s own code and usable area.'],
            ['Prices and distances', 'The Word description gives villas from EUR 5,995,000; the PDF and the price list give EUR 6,495,000. Puerto Banús is ten minutes in the description and 15 in the brochure. We confirm both before any viewing.']]},
    'availability': {
        'phase': '', 'headlineHtml': '40 homes <em>currently available</em>',
        'copy': 'Forty of the 66 homes are listed: 29 apartments and penthouses from EUR 1,495,000 to EUR 4,950,000 and 11 villas from EUR 6,495,000 to EUR 8,950,000, all excluding VAT. The other 26 are marked Reserved in the price lists and are not shown. Nueva Living reconfirms price and availability with the developer before any viewing.',
        'startingPrice': 'EUR 1,495,000 + VAT', 'priceRange': 'EUR 1,495,000 - EUR 8,950,000 + VAT', 'checkedDate': 'October 2026',
        'sourceNote': 'Prices, bedrooms and areas are transcribed from the developer’s price lists: the apartment list (50 homes, dated by its file August 2026) and the villa list (16 villas, September 2026). Homes marked Reserved are not listed. Prices exclude VAT; the payment terms add VAT to each instalment and the rate is not stated. For the apartments, “built” is the list’s interior build and “terrace” is its exterior build, terraces plus porches; for 13C and 13D the list’s exterior figure differs from the sum of its terrace and porch columns, and we print the exterior figure. For the villas, “built” is the interior built area, “terrace” is terraces and porches, “usable” is the list’s usable area and the plot is the list’s. Every apartment has two parking spaces and a storage room in the list; the villa list gives two parking spaces, with extra figures written against some villas (2+2 for Villa 14, 6 for Villa 10) that it does not explain. The individual apartment plan sheets give slightly different areas. The plans are the developer’s, with room names in Spanish, and are provisional.',
        'image': {'src': M + 'villa-exterior-dusk-pool.jpg', 'alt': ALT['villa-exterior-dusk-pool']},
        'units': units},
    'timeline': {'headlineHtml': 'What happens <em>next</em>', 'items': [
        ['01', 'Request the project file', 'The plans, the specifications and the price lists for the homes that interest you.'],
        ['02', 'Compare the options', 'See this alongside the other projects we hold in Benahavís and the Golden Triangle.'],
        ['03', 'Private viewing', 'See the site and the area with us, and the plans against the site.'],
        ['04', 'Reserve', 'A reservation fee of EUR 20,000, EUR 35,000 or EUR 50,000 for apartments and EUR 50,000 for villas, then the staged payments in the developer’s schedule, plus VAT, once we have confirmed the terms in writing.']]},
    'privateViewing': {
        'headlineHtml': 'See the <em>site and the area</em>',
        'copy': 'The pack includes photographs of a finished pilot villa, Villa 10. We ask the developer whether it can be visited and how far the other homes have got, so a visit is about the location, the plans and the stage of the work.',
        'href': f'index.html#private-viewing=1&project={SLUG}',
        'insights': [
            ['On site', 'Walk the community, the access road and the views, and see the pilot villa if the developer allows it.'],
            ['In the area', 'We drive to Puerto Banús, the golf courses and the motorway with you and time it.'],
            ['On paper', 'Licence, guarantee and the contract, before anything is signed.']]},
    'enquiry': {
        'headlineHtml': f'Ask about <em>{NAME.replace("&", "&amp;")}</em>',
        'copy': 'Tell us what you need and we will come back with current availability, the plans and the price.',
        'message': f'Hello Nueva Living, I would like information about {NAME}.',
        'note': 'We reply personally, usually the same day.',
        'sentMessage': 'Thank you. We will come back to you shortly with the project file.'},
    'faq': [
        ['How many homes are available?', 'The development has 66 homes: 50 apartments and penthouses and 16 villas. Forty are listed as available, 29 apartments and penthouses and 11 villas, and 26 are marked Reserved in the developer’s price lists. We confirm the current position before any viewing.'],
        ['What do the homes cost?', 'According to the price lists, apartments and penthouses cost from EUR 1,495,000 to EUR 4,950,000 and villas from EUR 6,495,000 to EUR 8,950,000, each plus VAT. We confirm the price of each home in writing.'],
        ['Is VAT included?', 'No. The payment terms add VAT to every instalment. The documents do not state the rate or other purchase costs, so we confirm them in writing.'],
        ['What is the payment schedule?', 'For apartments, a reservation fee of EUR 20,000, EUR 35,000 or EUR 50,000 depending on the price band, then 35% at the private purchase contract (less the reservation), 15% two months later and 50% at the deed. For villas, EUR 50,000, then 35% (less the reservation), 15% three months later and 50% at the deed and handover. All plus VAT.'],
        ['When will the homes be finished?', 'The documents disagree: the October 2026 description gives the third quarter of 2027 for both, the Word version gives the second quarter for villas and the third for apartments, and a public sales listing gives the second and the fourth. We ask for the contractual date.'],
        ['What sizes are the homes?', 'The listed apartments run from 129.22 sqm built for a 2-bedroom middle-floor home to 362.93 sqm for the available 5-bedroom penthouse, with terraces and porches on top. The villas have 811 to 937 sqm built on plots of 690 to 1,705 sqm.'],
        ['Are the villa photographs of a real villa?', 'Yes. The villa pictures are photographs of a pilot villa that the developer supplies as Villa 10, furnished and styled. The apartment and amenity pictures are computer-generated, and furniture is not included in the price.'],
        ['What does Reserved mean?', 'The price lists mark 26 homes Reserved and give no price for them. We do not list them. If one becomes available again we confirm it with the developer.']],
    'seo': {
        'title': 'La Quinta Summit Residences & Villas - Benahavís',
        'description': 'Fifty apartments and penthouses and sixteen villas at the top of La Quinta, Benahavís, in a gated community with sea views. Forty available, from EUR 1,495,000 plus VAT.',
        'h1': 'La Quinta Summit Residences & Villas: Apartments and Villas in Benahavís',
        'source': 'developer price lists, payment terms, plans, quality specifications and description, with a public sales listing for corroboration',
        'h1Context': 'Apartments and Villas in Benahavís'},
}
out = f'{ROOT}/content/liora-projects/{SLUG}/project.json'
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(d, open(out, 'w'), ensure_ascii=False, indent=2)
print('units', len(units), 'media', len(items), 'groups', len(GROUPS), 'lines', sum(len(i) for _, i in GROUPS))
