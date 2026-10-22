# -*- coding: utf-8 -*-
"""Writes the English record content/liora-projects/san-pedro-seaside-villas/project.json (no i18n yet)."""
import json, os
SLUG = 'san-pedro-seaside-villas'
NAME = 'San Pedro Seaside Villas'
M = f'assets/liora/projects/{SLUG}/media/'
F = f'assets/liora/projects/{SLUG}/floorplans/'
ROOT = '/Users/sasanraftari/Projects/nueva-living'
shipped = json.load(open('/Users/sasanraftari/Downloads/Sotomar_work/shipped.json'))
from PIL import Image

def dims(path):
    im = Image.open(os.path.join(ROOT, path)); return im.width, im.height

def img(path, alt):
    w, h = dims(path); return {'src': path, 'alt': alt, 'width': w, 'height': h}

# ---- gallery -------------------------------------------------------------------------------
PHOTOS = [
 ('exterior-front-pool', 'Exteriors', 'A villa seen across its pool',
  'Computer-generated view of a white villa with a stone-clad ground floor and a projecting roof, seen across its pool among palms'),
 ('exterior-garden-facade', 'Exteriors', 'The garden facade',
  'Computer-generated view of the garden facade of a villa with a stone-clad ground floor, a rust-coloured chimney and a covered terrace with dining and lounge areas'),
 ('exterior-side-elevation-driveway', 'Exteriors', 'The side elevation and driveway',
  'Computer-generated view of the side of a white villa with a timber entrance door, a glass balustrade and a car on the driveway'),
 ('terrace-pool-firepit', 'Terraces', 'A sunken fire pit beside the pool',
  'Computer-generated view of a covered terrace with lounge furniture, a sunken seating area with a fire pit and a pool with sun loungers'),
 ('covered-terrace-pool', 'Terraces', 'The covered terrace and pool',
  'Computer-generated view from a covered terrace with an outdoor kitchen across a pool to a hedge and olive trees'),
 ('aerial-four-villas', 'Location', 'The four villas from above',
  'Computer-generated aerial view of four new villas with pools in a residential area, with a road and a car park beside them'),
 ('aerial-coastline', 'Location', 'The coast beside the villas',
  'Computer-generated aerial view of the coastline, the beach and the residential streets around the villas at sunset'),
 ('living-room-garden-views', 'Interiors', 'Living room with garden views',
  'Computer-generated double-height living room with a cream sofa, round coffee tables, a sculptural pendant light and glass walls to the garden'),
 ('living-room-open-plan-terrace', 'Interiors', 'Open-plan living, dining and kitchen',
  'Computer-generated open-plan living room with sofas and a dining table, floor-to-ceiling glass doors and the kitchen beyond'),
 ('living-room-travertine-fireplace', 'Interiors', 'Living room with a stone fireplace wall',
  'Computer-generated living room with a long sofa and a linear fireplace in a stone-clad wall with a television and shelves'),
 ('dining-double-height', 'Interiors', 'Dining area under a double-height ceiling',
  'Computer-generated round dining table with terracotta chairs under a double-height ceiling with sculptural pendant lights'),
 ('dining-room-pool-view', 'Interiors', 'Dining area facing the pool',
  'Computer-generated dining table with cream chairs beside a sofa, with glass walls to a pool and palm trees'),
 ('kitchen-marble-island', 'Interiors', 'Kitchen with a stone island',
  'Computer-generated kitchen with dark cabinetry, glass-fronted units, built-in ovens and a stone island with three stools'),
 ('kitchen-island-stools', 'Interiors', 'Kitchen island',
  'Computer-generated kitchen with a stone island, three black stools and a wall of ovens beside glass-fronted units'),
 ('master-bedroom-feature-wall', 'Bedrooms', 'Main bedroom with a feature wall',
  'Computer-generated main bedroom with a double bed, a panelled feature wall with backlighting and a walk-in wardrobe behind glass'),
 ('master-bedroom-round-mirror', 'Bedrooms', 'Main bedroom with a round mirror',
  'Computer-generated main bedroom with a patterned headboard wall, pendant lights and a round mirror above a floating dressing shelf'),
 ('guest-bedroom-soft-headboard', 'Bedrooms', 'Guest bedroom',
  'Computer-generated bedroom with a double bed, a sculpted headboard, an arched mirror and a built-in desk'),
 ('guest-bedroom-desk', 'Bedrooms', 'Guest bedroom with a desk',
  'Computer-generated bedroom with a double bed, a built-in dressing desk and wall lights'),
 ('master-bathroom-freestanding-bath', 'Bathrooms', 'Master bathroom with a freestanding bath',
  'Computer-generated bathroom with a dark stone vanity, a round mirror, a glazed shower and a freestanding bath beside a window'),
 ('master-bathroom-stone-basin', 'Bathrooms', 'Bathroom with a stone basin',
  'Computer-generated bathroom with a stone basin on a dark base, wall taps, a glazed shower and a freestanding bath'),
 ('master-bathroom-shower', 'Bathrooms', 'Shower',
  'Computer-generated walk-in shower lined in veined stone with a niche, a bench and a glass door'),
 ('basement-games-room-wine-cellar', 'Basement', 'Basement games room and wine cellar',
  'Computer-generated basement with a billiard table, a stone bar and a round glass wine cellar'),
 ('basement-lounge', 'Basement', 'Basement lounge',
  'Computer-generated basement lounge with a sectional sofa, armchairs and illuminated wall panels'),
 ('basement-bar', 'Basement', 'Basement bar',
  'Computer-generated basement bar with a stone counter, three stools and backlit bottle shelves'),
 ('basement-billiards-bar', 'Basement', 'Billiards and bar',
  'Computer-generated basement with a red-cloth billiard table, a wine display and a bar with stools'),
 ('basement-lounge-timber-ceiling', 'Basement', 'Lounge with a timber ceiling',
  'Computer-generated basement lounge with a sectional sofa, a slatted timber ceiling and a bar behind'),
 ('basement-wine-wall-lounge', 'Basement', 'Lounge with a glass wine wall',
  'Computer-generated basement lounge with a curved sofa, a glass wall of wine bottles and a window onto a courtyard'),
 ('home-office', 'Basement', 'Home office',
  'Computer-generated office with a wooden desk, armchairs, built-in shelving and sliding glass doors to a planted patio'),
]
PHOTO_ALT = {n: a for n, _, _, a in PHOTOS}
items = []
for name, cat, cap, alt in PHOTOS:
    d = img(M + name + '.jpg', alt); d['category'] = cat; d['caption'] = cap; items.append(d)
LEVELS = [('basement', 'basement'), ('ground-floor', 'ground floor'), ('first-floor', 'first floor'), ('solarium', 'solarium')]
for v in (1, 2, 4):
    for key, label in LEVELS:
        d = img(F + f'villa-{v}-{key}.jpg', f'Floorplan of Villa {v}, {label}')
        d['category'] = 'Floorplans'; d['caption'] = f'Villa {v}, {label}'; items.append(d)

# ---- quality specifications (the developer's own English version of the report, regrouped) ---------
Q = [
 ('Structure', [
  'Reinforced concrete structure, both vertical and horizontal elements, built to the Technical Building Code (CTE) and the applicable regulations, as per the project specifications.',
  'Foundations on a reinforced concrete slab, according to the geotechnical study.',
  'Reinforced concrete waffle slabs 35 cm deep (30 + 5 cm) with ribs at 84 cm centres, on reinforced concrete columns, all according to the structural calculations of the detailed design.']),
 ('Facades, roofs and insulation', [
  'Exterior walls: the outer leaf is perforated ceramic brickwork 11.5 cm thick with an internal cement mortar coat to limit thermal bridges. All walls are lined internally with rock wool thermal insulation and an air gap to optimise thermal comfort, and the inner face is finished with a double layer of 13 mm plasterboard on a 48 mm aluminium substructure with rock wool insulation inside.',
  'Accessible flat roof: a sloped base, a flexible waterproofing membrane, a protective M-5 cement mortar layer, rigid extruded polystyrene thermal insulation, a high-density polyethylene (HDPE) dimpled drainage sheet and an adjustable polypropylene pedestal substructure, finished with large-format, rectified, non-slip porcelain tiles, in line with the CTE and DIT.',
  'High-quality elastic exterior paint in three coats: a primer coat to reveal imperfections, an intermediate coat of filling and sanding to correct them, and a finish coat.']),
 ('Partition walls', [
  'Interior partitions between bedrooms and living areas: a double layer of 13 mm plasterboard on a 70 mm aluminium substructure with rock wool insulation inside. Total finished thickness 12.2 cm.',
  'Other interior partitions: a double layer of 13 mm plasterboard on a 48 mm aluminium substructure with rock wool insulation inside. Total finished thickness 10 cm.',
  'Interior partitions between the first-floor bedrooms and the living room, where there is double height: a double layer of 13 mm plasterboard on a 90 mm aluminium substructure with rock wool insulation inside. Total finished thickness 14.2 cm.',
  'Interior painting of all wall surfaces in three coats of premium-quality washable paint: a first coat to seal imperfections, a second coat with spackling and sanding to correct them, and a finishing coat.',
  'Continuous suspended false ceiling with a smooth finish, in 13 mm plasterboard screwed to a galvanised steel framework hung from the structural slab on threaded rod hangers at 500 mm intervals.',
  'Exterior false ceiling with a smooth finish on a metal framework, in 13 mm Knauf Aquapanel (or equivalent) board with tapered edges, finished in smooth matte white exterior-grade emulsion paint.']),
 ('Exterior joinery', [
  'Aluminium frames with a textured RAL 8002 lacquer finish and thermal break: fixed panels and operable balcony doors, with the Reynaers Slim Patio 68 series (or equivalent) for sliding units.',
  'Aluminium frames with a textured RAL 8002 lacquer finish and thermal break: the CS 77 series (or equivalent) for operable units.',
  'Security rating RC2 and RC3 on all window and door units.',
  'Interior and exterior railings in 15 mm tempered glass or 8+8 laminated safety glass (two 8 mm panes bonded with two colourless 0.38 mm polyvinyl butyral interlayers), installed on the parapets of the habitable first-floor terraces and at the fixed, walk-on skylight.',
  'Motorised vehicle access gate, Hörmann or equivalent.']),
 ('Interior joinery', [
  'Oak entrance door with a reinforced or armoured security locking system, 2.95 m high, with concealed hardware.',
  'Interior passage doors in lacquered MDF, in a colour to be determined by the project management, from floor to ceiling, with 4.5 cm thick leaves and concealed hardware.',
  'Wardrobe fronts in lacquered MDF with 3.00 cm thick leaves, from floor to ceiling; wardrobe interiors and fittings lined in melamine board, with 3000 K LED strip lighting.']),
 ('Flooring and paving', [
  'General interior flooring: Gunni Trentino Sand rectified porcelain tile, 1200 x 1200 mm, Class C1 or equivalent. Flush skirting recessed into the drywall, in moisture-resistant wood lacquered white (RAL 9010), 150 x 15 mm.',
  'Terrace flooring: Gunni Trentino Sand rectified porcelain tile, 1200 x 1200 mm, Class C3 or equivalent. Surface-mounted skirting in a special porcelain piece of the same material, 80 mm high.',
  'Acoustic insulation under interior floors: a flexible polyethylene sheet such as Impactodan, 10 mm thick, or equivalent.',
  'Exterior flooring of common areas: Gunni Trentino Sand rectified porcelain tile, 1200 x 1200 mm, Class C3 or equivalent. Surface-mounted skirting in a special porcelain piece of the same material, 80 mm high.']),
 ('Facade cladding', [
  'Exterior facade finish in screeded render (Weber brand or equivalent) and white silicate paint, except for specific facade areas clad in natural stone or natural wood.',
  'Interior finishes in plasterboard. Vertical and horizontal surfaces painted with emulsion paint in a colour chosen by the client and the project management, and washable paint in wet areas.',
  'Facade cladding in natural travertine marble (Cosentino / Scalea TravAbassi Terra or equivalent), 2.00 cm thick, with concealed mechanical fixings, according to the facade design in the detailed construction plans.']),
 ('Toilets and bathrooms', [
  'Mirror: custom-made Gunni & Trentino mirror, Omlam model, with a 15 mm sandblasted perimeter border and warm perimeter LED lighting, 110 cm high by 50 cm wide, or equivalent.',
  'Countertop: Gunni & Trentino solid surface bathroom countertop, 181 x 51 x 12 cm, double basin, including support brackets, or equivalent.',
  'Vanity unit: Gunni & Trentino vanity unit, 180 x 50 x 30 cm, in a matte natural walnut finish, with two 90 cm drawers, or equivalent.',
  'Basin mixer: Gunni & Trentino wall-mounted basin mixer (Zucchetti brand or equivalent), brushed finish trim set.',
  'Shower: Gunni & Trentino 2-way shower mixer (Zucchetti brand or equivalent), brushed finish trim set, with a flush-mounted 400 x 400 mm ceiling shower head in brushed stainless steel (PVD Long Life AISI 316L) and a Gunni & Trentino hand shower kit (Zucchetti brand or equivalent) with a brushed finish.',
  'Toilet: Villeroy & Boch ViClean I-200 rimless shower toilet, with a concealed cistern and flush plate by Geberit or an equivalent brand.',
  'Reversible shower channel, 80 cm.',
  'Bathroom floors and shower bases in rectified porcelain tile (Gunni & Trentino Sand model, 120 x 120 format, Class C3) or an equivalent product.',
  'Shower wall cladding in Calacatta Black tile (120 x 120 format) or equivalent, or San Pe Brown tile (120 x 120 format) or equivalent, depending on the villa type.']),
 ('Electricity and lighting', [
  'Mechanisms: Gira E2 in matte white, with Gira 95 touch-sensor push-buttons in white, or similar equivalent.',
  'Interior lighting: recessed ceiling lights, downlights or equivalent fixtures.',
  'Interior LED lighting with warm white lamps (2700 K, or 3000 K in bathrooms). IP33 rating throughout the home and IP65 in bathrooms.',
  'Lighting of pedestrian access along paths and stairways: recessed LEDS C4 fixtures, Tiny model or equivalent, finished in the same RAL colour as the aluminium joinery (reference image).',
  'General outdoor lighting: LEDS C4 wall-mounted fixtures, Afrodita model or equivalent, finished in the same RAL colour as the aluminium joinery (reference image).']),
 ('Low voltage', [
  'Centralised electrical panel in the plant room and sub-panels on each floor.',
  'Network and internet installation in Category 6 cabling for RJ45 outlets in bedrooms, the living room and living areas, with a switch, a router and a fibre-optic connection to the development’s main service line.',
  'TV outlets in the living room, the bedrooms and the basement playroom.',
  'Integrated technical interior lighting throughout the home, recessed in the ceiling, in LED technology with a 3000 K colour temperature.',
  'Exterior garden lighting using fixtures specified in the landscaping plan.',
  'Fire protection system, including emergency lighting and fire extinguishers.',
  'Video intercom for pedestrian access, integrated into the home automation system.',
  'Pre-installation for an 11 kW electric vehicle charging point, integrated into the home automation system.',
  'Photovoltaic pre-installation of 6 to 8 kW (the maximum allowed by the area available on the non-walkable parts of the solarium and first floor).',
  'Pre-installation for motorised curtains in all rooms.']),
 ('Plumbing, ventilation, air conditioning and heating', [
  'Cross-linked polyethylene (PEX) plumbing distribution for hot and cold water, insulated with Armaflex.',
  'Hot water recirculation to the points of use, with a pump controlled by the home automation system.',
  'Main shut-off valves in a utility cabinet: one for the home and one for the garden.',
  'Shut-off valves in all wet areas.',
  'Water supply shut-off system, split between the home and the garden and integrated into the home automation system.',
  'A 5,000-litre water storage tank (Rothagua brand or equivalent), with a filter, a pressure booster set with two variable-frequency pumps operating in parallel, and a water softener.',
  'Domestic hot water from an aerothermal heat pump (Daikin brand or equivalent) with a 500-litre storage tank.',
  'Indoor air renewal in wet areas and utility rooms by a single-flow mechanical ventilation system (Siber brand or equivalent).',
  'Air conditioning by a Mini VRV system (Daikin brand or equivalent) for heating and cooling, with zoning managed by Airzone.',
  'Hydronic underfloor heating on the main floors (Uponor brand or equivalent), powered by the heat pump system (Daikin brand or equivalent).']),
 ('Elevator', [
  'TKE (ThyssenKrupp) brand elevator or equivalent: basic finish in stainless steel and glass, with flooring matching that of the home and exterior doors lacquered to match the colour of the interior walls of the homes.']),
 ('Home automation', [
  'Basic home automation system with the following functions.',
  'Integrated management and control hub: a centralised system that unifies lighting, climate control and security in a single interface (an app or touch panels).',
  'Smart lighting: automatic control of intensity levels and scenes according to the time of day, presence or activity.',
  'Zoned climate control and air quality: independent temperature regulation for each room, covering heating, cooling and ventilation.',
  'Motorisation of curtains and awnings: automation of exterior and interior elements to manage natural light, privacy and energy savings.']),
 ('Solarium', [
  'Access to the solarium by an integrated staircase, as an additional level of the home.',
  'Glass railings at the front of the terrace to maximise the views of the garden area.',
  'A leisure area for sun loungers or terrace furniture, overlooking the garden.',
  'Pre-installation for an outdoor kitchen and/or barbecue, lighting and power outlets.',
  'Pre-installation for a jacuzzi.']),
 ('Gardening and pool', [
  'Landscaping according to the project’s garden and tree planting design.',
  'Zoned automatic irrigation, with sprinklers on lawn areas and drip irrigation on planted areas.',
  'Swimming pool with salt chlorination, pH control and RGB LED lighting integrated into the home automation system.',
  'Pre-installation for a pool heat pump.']),
 ('Wellness and luxury features', [
  'Pre-installation for a 2 x 2 m sauna and hammam.',
  'Pre-installation for a home cinema.',
  'Pre-installation for a climate-controlled wine cellar with integrated three-zone refrigeration units (red wine, white wine and sparkling wine).']),
 ('Kitchen furniture', [
  'Custom-designed and manufactured kitchen cabinetry by Modulnova, with base units, wall units and tall units, and fronts in a Milltech finish for a high-quality, contemporary aesthetic.',
  'Internal cabinet bodies in 19 mm laminate board with a Basic Grigio finish.',
  'Drawers and pull-out baskets in lacquered stainless steel, with full-extension runners and soft-close mechanisms for smooth, silent operation and high durability.',
  'Cabinet opening by an integrated lacquered gola profile, for a clean look without visible handles.',
  'Plinths in lacquered aluminium, coordinated with the cabinetry.',
  'Units and floor-to-ceiling tall units, to use the available space fully and give a continuous solution with ample storage. The configuration, layout and dimensions of the cabinetry follow the interior design plan and the final kitchen specification.']),
 ('Kitchen accessories, countertop and appliances', [
  'LED lighting under the wall units.',
  'A 12 mm thick porcelain countertop.',
  'Backsplash between base and wall units in the same 12 mm thick material, with cutouts for auxiliary power outlets; island side panels with mitred joints extending to the floor.',
  'Miele appliances or a similar equivalent.',
  'Shown in the report: an integrated fridge-freezer, a multifunction oven in Obsidian Black, an induction cooktop with flexible cooking zones for up to 5 cooking vessels, a downdraft extractor hood, a fully integrated dishwasher and a washing machine.']),
]
spec = {
 'headlineHtml': 'What the villas are <em>built with</em>',
 'copy': 'The developer’s own quality report, group by group, with the product brands as the report names them.',
 'sourceNote': 'Source: the developer’s quality report for this development, a 41-page document in Spanish and English that carries no date or version number. Where it says “or equivalent”, so does this page. It lists the sauna and hammam, the home cinema, the wine cellar, the jacuzzi, the pool heat pump, the electric vehicle charger, the photovoltaic system and the outdoor kitchen as pre-installations only; we ask what is supplied and what is provision for later. The brochure says underfloor heating throughout, while the report lists it on the main floors; we confirm which areas have it.',
 'groups': [{'name': n, 'items': i} for n, i in Q],
}

# ---- units ---------------------------------------------------------------------------------------
FLOOR = 'Lower level, ground floor, first floor & solarium'
units = [
 {'reference': 'Villa 1', 'floor': FLOOR, 'bedrooms': '4 bedrooms',
  'size': '808.34 sqm total built, 488.31 sqm usable, 92.55 sqm solarium, 889.06 sqm plot, 406.15 sqm garden', 'price': 'EUR 4,950,000', 'floorplan': F + 'villa-1-ground-floor.jpg'},
 {'reference': 'Villa 2', 'floor': FLOOR, 'bedrooms': '5 bedrooms',
  'size': '821.22 sqm total built, 527.01 sqm usable, 96.54 sqm solarium, 752 sqm plot', 'price': 'EUR 4,800,000', 'floorplan': F + 'villa-2-ground-floor.jpg'},
 {'reference': 'Villa 4', 'floor': FLOOR, 'bedrooms': '5 bedrooms',
  'size': '821.22 sqm total built, 527.01 sqm usable, 96.54 sqm solarium, 888.15 sqm plot', 'price': 'EUR 4,700,000', 'floorplan': F + 'villa-4-ground-floor.jpg'},
]

AMEN = ['Private pool', 'Private garden', 'Lift', 'Private garage', 'Games room', 'Solarium', 'Underfloor heating',
        'Aerothermal system', 'Air conditioning', 'Home automation', 'Automatic irrigation', 'Laundry room',
        'Pre-installation for electric vehicle charging']

d = {
 'slug': SLUG, 'output': f'property-{SLUG}.html', 'archived': False,
 'name': NAME, 'shortName': 'San Pedro Seaside', 'titleHtml': 'San Pedro Seaside <em>Villas</em>',
 'description': 'Four villas in the Cortijo Blanco area of Marbella, on the coast between San Pedro de Alcántara and Puerto Banús and a short walk from the beach. Each has a basement with a garage, a games room and an office, a lift, a private pool and a solarium; three are available, from EUR 4,700,000 plus VAT, and one is sold. The completion date is to be confirmed.',
 'canonical': f'https://nuevaliving.com/property-{SLUG}.html',
 'seoDescription': 'Four villas in Cortijo Blanco, Marbella, a short walk from the beach: 4 or 5 bedrooms, a basement, a lift, a private pool and a solarium. Three available, from EUR 4,700,000 plus VAT.',
 'twitterDescription': 'Four villas in Cortijo Blanco, Marbella, a short walk from the beach, each with a private pool, a lift and a solarium, from EUR 4,700,000 plus VAT.',
 'schema': {'price': '4700000', 'priceCurrency': 'EUR', 'category': 'Villa', 'areaServed': 'Marbella, Málaga, Spain'},
 'crm': {
  'realName': 'Sotomar by the Sea', 'developer': '',
  'realDeveloper': 'Not named in the supplied documents (architects: Huete Arquitectos; interior design: Aalto Exclusive Design)',
  'area': 'San Pedro de Alcantara', 'address': 'Cortijo Blanco, Marbella, Málaga',
  'priceMin': 4700000, 'priceMax': 4950000, 'currency': 'EUR', 'bedroomsMin': 4, 'bedroomsMax': 5, 'propertyTypes': ['villa'],
  'totalUnits': 4, 'availableUnits': 3,
  'constructionStatus': 'Off-plan on the documents we hold: no construction stage, building licence or completion date is stated',
  'brochureUrl': '', 'amenities': AMEN, 'reference': 'MA-SP-SEASIDEVILLAS'},
 'contact': {'whatsappNumber': '34645446624', 'whatsappMessage': f'Hello Nueva Living, I would like information about {NAME}.'},
 'hero': {'eyebrow': '3 of 4 villas available', 'location': 'Cortijo Blanco, Marbella', 'startingPrice': 'From EUR 4,700,000 + VAT',
          'type': 'Villas', 'delivery': 'Completion to be confirmed'},
 'card': {'order': 115, 'label': 'Cortijo Blanco', 'locExtended': 'Cortijo Blanco, Marbella',
          'description': 'Four villas in Cortijo Blanco, Marbella, a short walk from the beach, each with a basement, a private pool, a lift and a solarium. Three are available.',
          'meta': [['From', 'EUR 4,700,000 + VAT'], ['Type', 'Villas'], ['Delivery', 'Completion to be confirmed']],
          'badge': 'Off-Plan', 'typeTag': 'Cortijo Blanco'},
 'quickFacts': [
  ['Starting price', 'From EUR 4,700,000 + VAT'],
  ['Location', 'Cortijo Blanco, Marbella'],
  ['Property type', 'Villas'],
  ['Bedrooms', '4-5 bedrooms'],
  ['Total built area', '808.34 - 821.22 sqm'],
  ['Useful living area', '488.31 - 527.01 sqm'],
  ['Plot', '751 - 889.06 sqm'],
  ['Delivery', 'Completion to be confirmed'],
  ['Availability', '3 of 4 villas available'],
 ],
 'discovery': {
  'priority': 115, 'featured': False, 'releaseDate': '2026-10', 'price': '4700000', 'area': 'san-pedro-alcantara',
  'bedrooms': '4-5 bedrooms', 'status': 'Off-plan', 'availability': '3 of 4 villas available',
  'propertyTypes': ['villa'],
  'lifestyleTags': ['Walk to Beach', 'Family-Oriented', 'Entertaining'],
  'architectureTags': ['Contemporary', 'Double-Height Living', 'Rooftop Solarium'],
  'locationTags': ['Cortijo Blanco', 'San Pedro Alcántara'],
  'investmentTags': ['Second Home', 'Lifestyle Investment', 'International Buyer'],
  'practicalTags': ['Villas', 'Private Pool', 'Lift', 'Underfloor Heating', 'Private Garage'],
  'cardTags': ['Cortijo Blanco', 'Walk to Beach', 'Private Pool'],
  'advisoryBadge': 'Best for buyers who want a large villa with a basement, a pool and a lift close to the beach'},
 'images': {
  'hero': img(M + 'exterior-front-pool.jpg', PHOTO_ALT['exterior-front-pool']),
  'architecture': img(M + 'exterior-garden-facade.jpg', PHOTO_ALT['exterior-garden-facade']),
  'lifestyle': img(M + 'terrace-pool-firepit.jpg', PHOTO_ALT['terrace-pool-firepit']),
  'privateViewing': img(M + 'aerial-coastline.jpg', PHOTO_ALT['aerial-coastline'])},
 'media': {
  'headlineHtml': 'The villas <em>in detail</em>',
  'copy': 'Computer-generated views of the exteriors, the interiors, the basement and the surroundings, and the developer’s plans of every level of Villas 1, 2 and 4.',
  'note': 'All the photographs are computer-generated images, and the furniture, art and decoration in them are illustrative. The plans are the developer’s, with the room names in Spanish; Villa 3, which is sold, has none here.',
  'items': items},
 'overview': {
  'headlineHtml': 'Four villas, <em>three available</em>',
  'copy': [
   'San Pedro Seaside Villas is a collection of four villas in the Cortijo Blanco area of Marbella, on the coast between San Pedro de Alcántara and Puerto Banús. Each stands on its own plot of 751 to 889.06 sqm with a garden and a private pool.',
   'Every villa is laid out over a basement, a ground floor, a first floor and a solarium, with a lift serving the levels. The living, dining and kitchen area is on the ground floor beside the pool, and the basement holds a garage, a games room, an office, a recreation room and a laundry. The price list gives four bedrooms for Villa 1 and five for the other villas; the plans label three bedrooms and draw a basement recreation room with a bed.',
   'The brochure describes open-plan layouts, floor-to-ceiling windows, double-height ceilings, 1.20 by 1.20 m porcelain tiles and underfloor heating. The price list gives a price for each available villa, excluding VAT. The documents still give no building licence, no construction stage and no completion date, so those are to be confirmed and we confirm them in writing.'],
  'metrics': [['Development', '4 villas'], ['Available', '3 villas'], ['Total built area', '808.34 - 821.22 sqm'], ['Price range', 'EUR 4,700,000 - EUR 4,950,000 + VAT']]},
 'why': {
  'headlineHtml': 'Why this project <em>matters</em>',
  'copy': 'Four villas on their own plots a short walk from the beach, with the finishes written down product by product.',
  'points': [
   ['Who it is for', 'Buyers who want a large villa with a basement, a pool and a lift close to the beach, in an established part of Marbella between San Pedro de Alcántara and Puerto Banús.'],
   ['What makes it different', 'Each villa has a basement with a garage, a games room and an office, a solarium above the first floor, a lift to every level and a private pool, and the quality report names the products used.'],
   ['Why location matters', 'The brochure places the villas in the Cortijo Blanco area of Marbella, a short walk from the beach, with San Pedro de Alcántara and Puerto Banús on either side.'],
   ['Why check availability', 'Three of the four villas are available and one is sold, at EUR 4,700,000 to EUR 4,950,000 plus VAT. Nueva Living reconfirms price and availability with the developer before any viewing.']]},
 'architecture': {
  'headlineHtml': 'Contemporary lines, <em>natural materials</em>',
  'copy': [
   'The brochure describes each villa as contemporary architecture with clean lines and natural textures, with open-plan layouts, floor-to-ceiling windows and double-height ceilings to bring in natural light and link the house to its garden and pool.',
   'In the renders the facades are white with natural stone and timber cladding in places, and the upper floor projects over the terraces below.'],
  'highlights': [
   ['Structure', 'Reinforced concrete to the Technical Building Code, on a reinforced concrete slab foundation set by the geotechnical study, with 35 cm waffle slabs.'],
   ['Facade', 'Perforated ceramic brick with rock wool insulation and an air gap, finished in render and white silicate paint, with natural stone or natural timber on specified areas.'],
   ['Glazing', 'Thermally broken aluminium frames, security-rated RC2 and RC3, and glass railings in 15 mm tempered or 8+8 laminated glass.'],
   ['Flooring', '1200 x 1200 mm rectified porcelain tiles indoors and on the terraces.'],
   ['Ceilings', 'Smooth plasterboard false ceilings, and double height between the living room and the first-floor bedrooms.']]},
 'qualitySpecs': spec,
 'residences': {
  'headlineHtml': 'Four villas, <em>one concept</em>',
  'copy': 'Each card gives the price list\u2019s figures for that villa, then the brochure\u2019s. The price list gives a total built area and a useful living area; the brochure\u2019s built-area table splits the ground and first floors into enclosed, covered and uncovered areas, so its totals include terraces. Where the two differ, both figures are named.',
  'items': [
   {'name': 'Villa 1, on an 889.06 sqm plot', 'points': [
     'Price list: EUR 4,950,000 plus VAT, 4 bedrooms and 4+2 bathrooms, a total built area of 808.34 sqm, a useful living area of 488.31 sqm, a solarium of 92.55 sqm and a plot of 889.06 sqm.',
     'Brochure: ground floor 244.15 sqm, first floor 200.64 sqm, basement 271.00 sqm and solarium 92.55 sqm, a total of 808.35 sqm (the price list prints 808.34), with a garden of 406.15 sqm and a pool of 51.19 sqm.',
     'First floor: 91.09 sqm enclosed, 49.92 sqm covered and 59.63 sqm uncovered. The ground floor lists 126.22 sqm enclosed, 81.02 sqm covered and 41.67 sqm uncovered, which add up to 248.91 sqm against the 244.15 sqm printed, so we ask which is right.',
     'Basement, from the plan: a garage of 41.67 sqm, a living area of 37.15 sqm, a games room of 47.52 sqm, a bar of 16.68 sqm, an office of 20.28 sqm and a recreation room of 15.00 sqm.',
     'Upper levels, from the plans: a living, dining and kitchen area of 61.73 sqm and bedroom 1 of 16.79 sqm on the ground floor, a main bedroom of 24.70 sqm and bedroom 2 of 17.54 sqm on the first floor, and a solarium of 20.94 sqm with a barbecue area of 38.14 sqm.']},
   {'name': 'Villa 2, on a 752 sqm plot', 'points': [
     'Price list: EUR 4,800,000 plus VAT, 5 bedrooms and 5+2 bathrooms, a total built area of 821.22 sqm, a useful living area of 527.01 sqm, a solarium of 96.54 sqm and a plot of 752 sqm (the brochure prints 751 sqm).',
     'Brochure: ground floor 240.22 sqm, first floor 177.47 sqm and solarium 96.54 sqm, with a pool of 75.80 sqm. Ground floor: 129.04 sqm enclosed, 72.33 sqm covered and 38.85 sqm uncovered. First floor: 90.98 sqm enclosed, 43.30 sqm covered and 43.19 sqm uncovered.',
     'The brochure page also prints a basement of 306.99 sqm with a garage of 98.97 sqm and a garden of 276.62 sqm, identical to Villa 3, but Villa 2\u2019s own basement plan shows a garage of 65.58 sqm and a smaller games room. The price list\u2019s total of 821.22 sqm matches the brochure page, so we ask which basement figures apply and do not show the garden as a size above.',
     'Basement, from the plan: a games room of 76.70 sqm, an office of 13.23 sqm, a recreation room of 12.84 sqm and a garage of 65.58 sqm.',
     'Upper levels, from the plans: a living, dining and kitchen area of 72.93 sqm, bedroom 1 of 13.95 sqm and a chill-out area of 13.65 sqm on the ground floor, a main bedroom of 20.45 sqm with a bathroom of 7.55 sqm and a dressing room of 6.19 sqm, and bedroom 2 of 17.44 sqm on the first floor, and a solarium of 30.32 sqm with a barbecue area of 30.44 sqm.']},
   {'name': 'Villa 3, sold', 'points': [
     'Marked as sold in the price list and in the name of the brochure file the developer supplied. No document gives a date or a buyer.',
     'The price list gives it 5 bedrooms, 5+2 bathrooms, a total built area of 821.22 sqm, a useful living area of 527.01 sqm, a solarium of 96.54 sqm and a plot of 751 sqm; its plans and printed areas match Villa 4, with a basement garage of 98.97 sqm and a pool of 75.80 sqm.',
     'It is not counted among the available villas and has no row in the availability table.']},
   {'name': 'Villa 4, on an 888.15 sqm plot', 'points': [
     'Price list: EUR 4,700,000 plus VAT, 5 bedrooms and 5+2 bathrooms, a total built area of 821.22 sqm, a useful living area of 527.01 sqm, a solarium of 96.54 sqm and a plot of 888.15 sqm.',
     'Brochure: ground floor 240.22 sqm, first floor 177.47 sqm, basement 306.99 sqm with a garage of 98.97 sqm and solarium 96.54 sqm, a total of 821.22 sqm, with a pool of 75.80 sqm.',
     'The brochure page prints a garden of 276.62 sqm, the same as Villa 3, although Villa 4\u2019s plot is 137.15 sqm larger, so we ask for the garden area and do not show it as a size above.',
     'Basement, from the plan: a garage of 98.97 sqm, a games room of 78.13 sqm, an office of 13.12 sqm and a recreation room of 13.22 sqm.',
     'Upper levels, from the plans: the same as Villa 2, with a living, dining and kitchen area of 72.93 sqm on the ground floor and a main bedroom of 20.45 sqm and bedroom 2 of 17.44 sqm on the first floor.']}]},
 'lifestyle': {
  'headlineHtml': 'Pool, garden, <em>solarium and basement</em>',
  'copy': 'What the brochure, the plans and the quality report give for the outdoor areas and the lower level.',
  'panels': [
   ['Pool and garden', 'A private pool in each garden, 51.19 sqm on Villa 1 and 75.80 sqm on the other villas as printed. The report specifies a salt-chlorinated pool with pH control and RGB LED lighting, landscaping and zoned automatic irrigation.'],
   ['Solarium', 'Reached by an integrated staircase as an extra level of the home, with glass railings towards the garden, a leisure area, and pre-installations for an outdoor kitchen or barbecue and for a jacuzzi.'],
   ['Basement', 'A garage, a games room, an office, a recreation room and a laundry on the plans. The renders furnish it with a lounge, a billiard table, a bar and wine storage.'],
   ['Wellness and cinema', 'Pre-installations for a 2 x 2 m sauna and hammam, a home cinema and a climate-controlled wine cellar with three zones for red, white and sparkling wine.']]},
 'location': {
  'headlineHtml': 'Cortijo Blanco, <em>between San Pedro and Puerto Banús</em>',
  'copy': 'The villas are in the Cortijo Blanco area of Marbella, on the coast between San Pedro de Alcántara and Puerto Banús, a short walk from the beach. The brochure’s map also marks restaurants, Marbella old town, golf, a hospital and the Nueva Alcántara area within reach.',
  'mapLabelHtml': 'Cortijo Blanco, <em>Marbella</em>', 'mapLabelPlain': 'Cortijo Blanco, Marbella', 'mapArea': 'sanPedro',
  'site': [36.4849, -4.9777], 'siteSource': 'area-geocode',
  'distances': [['Beach', 'A short walk'], ['Puerto Banús', 'Nearby']]},
 'investment': {
  'headlineHtml': 'How the <em>purchase works</em>',
  'copy': 'The terms are those of the developer\u2019s price list. We confirm the current amounts and dates in writing before you reserve.',
  'cards': [
   ['Prices', 'EUR 4,800,000 for Villa 2, EUR 4,700,000 for Villa 4 and EUR 4,950,000 for Villa 1, excluding VAT. The price list does not say what the price includes, so we confirm that in writing.'],
   ['VAT', 'The price list says all payments carry 10% VAT on top, so the prices exclude VAT. We confirm the other taxes and purchase costs in writing.'],
   ['Payment schedule', 'A reservation of EUR 50,000, then 30% after 30 days (marked PPC in the price list), 20% after six months and 50% on completion, each plus 10% VAT. The list does not say whether the reservation counts towards the first 30% or explain PPC, and we ask for the guarantee on payments made before completion.'],
   ['Availability', 'Three villas are available and Villa 3 is sold. We reconfirm availability with the developer before any viewing or reservation.']]},
 'trustDossier': {
  'headlineHtml': 'What we check <em>before you commit</em>',
  'copy': 'We confirm the current status of each item with the developer before any reservation, and put the answers in writing.',
  'cards': [
   ['Licence, guarantees and completion', 'The documents do not state a building licence, a construction stage or a completion date. We ask for the licence, the bank guarantee that covers amounts paid on account and the contractual date.'],
   ['The areas', 'The price list and the brochure differ on Villa 1\u2019s total (808.34 and 808.35 sqm) and on Villa 2\u2019s plot (752 and 751 sqm). Inside the brochure, Villa 1\u2019s ground-floor parts add up to 248.91 sqm against 244.15 sqm printed, Villa 2\u2019s page repeats the basement of Villas 3 and 4 although its plan has a smaller garage, and Villa 4\u2019s garden equals Villa 3\u2019s on a larger plot. We ask for corrected figures and for the area the contract uses.'],
   ['Distances', 'The brochure\u2019s welcome text puts the beach 300 metres away and its map says 0.1 km from San Pedro Beach; it calls Puerto Ban\u00fas a short walk while its map says 2 km. We confirm the walking distances on site.'],
   ['Bedrooms', 'The price list gives 4 bedrooms for Villa 1 and 5 for the other villas, with 4+2 and 5+2 bathrooms. The plans label three bedrooms and draw a basement recreation room with a bed. We ask which rooms count and what each villa is sold as.']]},
 'availability': {
  'phase': '', 'headlineHtml': '3 villas <em>currently available</em>',
  'copy': 'Four villas in total: Villas 1, 2 and 4 are available, from EUR 4,700,000 to EUR 4,950,000 plus VAT, and Villa 3 has been sold. Nueva Living reconfirms price and availability with the developer before any viewing.',
  'startingPrice': 'EUR 4,700,000 + VAT', 'priceRange': 'EUR 4,700,000 - EUR 4,950,000 + VAT', 'checkedDate': 'October 2026',
  'sourceNote': 'Prices, bedrooms, bathrooms, total built areas, useful living areas, solariums and plots are transcribed from the developer\u2019s price list (three of four villas priced; Villa 3 is marked sold). Prices exclude VAT: the list says all payments carry 10% VAT on top. The price list is the commercial source; the brochures and plans supply the room areas and the garden. Where they differ, both are named: Villa 1\u2019s total built area is 808.34 sqm in the price list and 808.35 sqm in the brochure, and Villa 2\u2019s plot is 752 sqm in the price list and 751 sqm in the brochure; the price list is shown. The price list gives 4 bedrooms for Villa 1 and 5 for Villas 2, 3 and 4, with 4+2 and 5+2 bathrooms, where the plans label three bedrooms. The brochure\u2019s total built area includes covered and uncovered terraces, and the price list\u2019s useful living area is the interior figure. Villa 1\u2019s garden is the brochure\u2019s; Villas 2 and 4 show none because the brochure repeats Villa 3\u2019s garden figure for them. The documents give no delivery date. The room names on the plans are in Spanish.',
  'image': {'src': M + 'exterior-front-pool.jpg', 'alt': PHOTO_ALT['exterior-front-pool']},
  'units': units},
 'timeline': {'headlineHtml': 'What happens <em>next</em>', 'items': [
   ['01', 'Request the project file', 'The plans, the quality report and the price list for the villas that interest you.'],
   ['02', 'Compare the options', 'See this alongside the other villa projects we hold in Marbella and San Pedro.'],
   ['03', 'Private viewing', 'See the site and the area with us, and the plans against the site.'],
   ['04', 'Reserve', 'A reservation of EUR 50,000, then the payments in the developer\u2019s schedule, each plus 10% VAT, once we have confirmed the terms in writing.']]},
 'privateViewing': {
  'headlineHtml': 'See the <em>site and the area</em>',
  'copy': 'The documents do not say how far the build has gone, so a visit is about the location, the plans and the stage of the work.',
  'href': f'index.html#private-viewing=1&project={SLUG}',
  'insights': [
   ['On site', 'Walk the plot and the street, and the way to the beach.'],
   ['On foot', 'We walk to the beach and the restaurants with you and time it.'],
   ['On paper', 'Licence, guarantee and the contract, before anything is signed.']]},
 'enquiry': {
  'headlineHtml': f'Ask about <em>{NAME}</em>',
  'copy': 'Tell us what you need and we will come back with current availability, the plans and the price.',
  'message': f'Hello Nueva Living, I would like information about {NAME}.',
  'note': 'We reply personally, usually the same day.',
  'sentMessage': 'Thank you. We will come back to you shortly with the project file.'},
 'faq': [
  ['How many villas are available?', 'Four villas make up the collection and three are available: Villas 1, 2 and 4. Villa 3 is marked as sold in the developer\u2019s price list and brochure. We confirm the current position with the developer before any viewing.'],
  ['What do the villas cost?', 'According to the price list, EUR 4,950,000 for Villa 1, EUR 4,800,000 for Villa 2 and EUR 4,700,000 for Villa 4, each plus VAT. We confirm the price of each in writing before any viewing.'],
  ['Is VAT included?', 'No. The price list says all payments carry 10% VAT on top. We confirm the other taxes and purchase costs in writing.'],
  ['What is the payment schedule?', 'A reservation of EUR 50,000, then 30% after 30 days, 20% after six months and 50% on completion, each plus 10% VAT. The list marks the 30% as PPC and does not say whether the reservation counts towards it, so we confirm both.'],
  ['When will the villas be finished?', 'No document we hold gives a completion date or says how far the build has gone. We ask for the construction stage and the contractual date.'],
  ['How big are the villas?', 'According to the price list, the total built area is 808.34 sqm for Villa 1 and 821.22 sqm for Villas 2, 3 and 4, the useful living area is 488.31 and 527.01 sqm, the solariums are 92.55 and 96.54 sqm, and the plots are 889.06, 752, 751 and 888.15 sqm. The brochure prints 808.35 sqm and a 751 sqm plot for Villas 1 and 2. The total built area includes the basement, the solarium and covered and uncovered terraces; the useful living area is the interior figure.'],
  ['How many bedrooms are there?', 'The price list gives 4 bedrooms for Villa 1 and 5 for Villas 2, 3 and 4, with 4+2 and 5+2 bathrooms. The plans label three bedrooms and draw a basement recreation room with a bed, so we ask which rooms count.'],
  ['Is the heating underfloor throughout?', 'The brochure says underfloor heating throughout, while the quality report lists hydronic underfloor heating on the main floors. We confirm which areas have it.']],
 'seo': {
  'title': 'San Pedro Seaside Villas - Villas in Marbella',
  'description': 'Four villas in Cortijo Blanco, Marbella, a short walk from the beach, with a basement, a lift, a private pool and a solarium. Three available, from EUR 4,700,000 plus VAT.',
  'h1': 'San Pedro Seaside Villas: Four Villas in Cortijo Blanco, Marbella',
  'source': 'developer price list, brochures, floorplans and quality report',
  'h1Context': 'Four Villas in Cortijo Blanco, Marbella'},
}
out = f'{ROOT}/content/liora-projects/{SLUG}/project.json'
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(d, open(out, 'w'), ensure_ascii=False, indent=2)
print('items', len(items), 'spec groups', len(Q), 'spec lines', sum(len(i) for _, i in Q))
