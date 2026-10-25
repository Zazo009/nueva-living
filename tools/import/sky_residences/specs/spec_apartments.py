# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
# -*- coding: utf-8 -*-
"""Apartment quality specification groups (source: the developer's apartment quality specification, 12 pages).
The top-level villa penthouse is named without the development's own name."""
A = 'Apartments: '
SPEC_APARTMENTS = [
 (A+'Structure and walls', [
  'The foundations combine footings with a raised slab and piled foundations with pile caps.',
  'The structure is reinforced concrete walls and columns, using waffle slabs or solid concrete slabs as required, in accordance with current building regulations.',
  'Exterior walls are perforated solid brick, with a ventilated or non-ventilated cavity depending on position, thermal insulation in line with current regulations and a self-supporting plasterboard inner lining on an auxiliary frame.',
  'Interior partitions between rooms are laminated plasterboard, finished in wallpaper, wood or paint depending on the design.']),
 (A+'Finishes and paintwork', [
  'Exterior walls are finished in render or extruded aluminium slats, depending on the design.',
  'The slab edges of the overhangs follow an organic, wave-like geometry, clad in a continuous sequence of Corian solid-surface pieces, or similar.',
  'Interior walls and ceilings are finished in plaster, paint or wood panelling, depending on the design.',
  'False ceilings are plasterboard, with perimeter recesses for curtains and indirect LED lighting, according to the design.',
  'A continuous Aquapanel false ceiling, or similar, extends from the interior onto the terrace, creating visual continuity between inside and outside while standing up to outdoor conditions.',
  'The exterior is painted in white or cream exterior paint, or similar, according to the design.',
  'Interior walls and ceilings are painted in smooth white or cream plastic paint, or similar, where applicable.']),
 (A+'Flooring and wall cladding', [
  'The main living areas have natural wood parquet laid in a chevron pattern, by Gunni&Trentino, or similar.',
  'Bathrooms, WCs, laundry, plant room and porches have large-format porcelain flooring by Gunni&Trentino, or similar, laid continuously without breaks at doorways, with joints kept as discreet as possible.',
  'Bathroom and WC walls are clad in the same large-format Gunni&Trentino porcelain, or similar, in a cream travertine look, creating continuity between floor and walls. It is combined with three different porcelains to distinguish the guest WC, the secondary bathrooms and the main bathroom.',
  'All cladding is installed in floor-to-ceiling formats, according to the design.',
  'In two-level apartments, the staircase treads are finished in wood to match the flooring.']),
 (A+'Exterior joinery', [
  'Sliding doors to walkable terraces are slim-profile aluminium, Schüco or similar, metallic lacquered in a champagne tone, floor-to-ceiling, with concealed tracks flush with the floor, thermal break and double glazing with solar control, low emissivity and a clear polyvinyl butyral layer.',
  'All other doors and windows are also aluminium, with tilt-and-turn or sliding opening depending on the design, Schüco or similar, with the same finish and performance.']),
 (A+'Interior joinery', [
  'The entrance door is a floor-to-ceiling pivoting door, tall and wide, with no architrave, finished in natural oak, with concealed security hinges, acoustic seals, stainless steel hardware and a designer handle.',
  'Floor-to-ceiling interior doors (excluding the private basement) are lacquered wood, with concealed hinges, privacy lock, stainless steel hardware and a steel-finish designer handle.',
  'Decorative panelling and/or porcelain or wood mosaics in selected areas, according to the design.',
  'Bespoke floor-to-ceiling wardrobes designed by Gunni&Trentino, with handles integrated into aluminium profiles, fully finished interiors, a modular accessory system in leather- or textile-effect and LED lighting to highlight selected areas.',
  'In the master suite, a bespoke walk-in wardrobe by Poliform, or similar: a lightweight aluminium-profile structure, textile or leather finishes and floor-to-ceiling glass folding doors, with indirect LED lighting and full accessories for a sense of lightness.',
  'Flush skirting throughout, Filomur type or similar, in aluminium, wood or porcelain according to the design.']),
 (A+'Lighting, sound and telecommunications', [
  'The lighting design combines different moods and smart home controls tailored to each space, and the electrical connection boxes and electrical and telecoms cabinets are positioned to remain concealed.',
  'The main rooms have two lighting moods: indirect, recessed LED lighting with diffuser panels for a calm, even light, and, in kitchens and bathrooms, LED accents to highlight specific elements. This is combined, according to the design, with ceiling-level track lighting for different dimmable scenes, plus independent spotlights to highlight selected areas.',
  'Niessen smart controls, or similar, with a main touchscreen in the living room and master bedroom for control of lighting, air conditioning, underfloor heating, sound and access throughout the home. All other rooms have a Niessen smart keypad, or similar, for temperature and lighting.',
  'Everything can be managed from the central panel or from any fixed or mobile device with internet access, from anywhere in the world: simulate daily routines, adjust the temperature, schedule lighting and view the video-intercom camera.']),
 (A+'Plumbing, air conditioning and underfloor heating', [
  'Hot and cold water installations comply with current regulations, using first-quality pipework for cold water and thermally insulated pipework for hot water, with shut-off valves in every wet room and per fixture.',
  'An air-source heat pump (aerothermal) system produces domestic hot water and supplies underfloor heating in living areas and bedrooms.',
  'Ducted hot and cold air conditioning in the living room and bedrooms, individually zoned per room and integrated into the home-automation system, with linear diffusers flush-mounted to ceiling or wall.',
  'Water-based underfloor heating in living areas and bedrooms through embedded pipework that also improves sound insulation, and electric underfloor heating in the guest WC and in the secondary and main bathrooms.']),
 (A+'Bathrooms and WCs', [
  'Wall-hung toilets in matte white porcelain in the guest WC and bathrooms, Laufen or similar, with soft-close seat, concealed cistern and Geberit dual-flush front button, or similar.',
  'In the main bathroom, according to the design, a freestanding bathtub with a contemporary, minimalist design and Dornbracht taps, or similar.',
  'Shower trays fully flush with the floor, in the same porcelain as the flooring, with an anti-slip finish, drained through the joints, and a ceiling-mounted rain shower in all bathrooms, or similar, with floor-to-ceiling glass screens.',
  'Laufen washbasins, or similar, on Trentino Bath designer vanity units by Gunni&Trentino, with matching accessories.',
  'Dornbracht taps, or similar, in all bathrooms and WCs, with a thermostatic shower mixer.',
  'Custom-designed mirrors in bathrooms and the guest WC, with LED lighting where applicable.',
  'The top-level villa-type penthouse includes a private sauna and hammam by Effe, or similar, supplied by Gunni&Trentino.']),
 (A+'Kitchen and appliances', [
  'High-end kitchen open to the living area, Poliform or similar, personalised to the design and materials of the apartments, with water-resistant surfaces, finishes up to ceiling height where applicable and integrated handles or a push-to-open system, according to the design.',
  'Bora induction hob, or similar, with carbon-filter extraction integrated into the kitchen island.',
  'Gaggenau or Miele oven with microwave function and intuitive touch programmes.',
  'Gaggenau or Miele wine cooler, integrated fridge, integrated freezer and integrated dishwasher, or similar, and a Gessi pull-out single-lever tap in a copper tone, or similar.',
  'Gaggenau or Miele washing machine and dryer, or similar, in the private basement laundry room.']),
 (A+'Private basement, parking and lifts', [
  'Each ground-floor apartment has a fully finished private basement with direct garage access: an entrance hall, an en-suite bedroom, a laundry and a multi-purpose area where applicable.',
  'A private staircase connects the basement directly to the main floor of the apartment.',
  'Communal lifts serve all floors via the residential corridors.',
  'The basement flooring is identical to the apartment, with walls in white paint and a plaster false ceiling.',
  'Every apartment has covered parking for 2 cars, with direct access to the home and provision for electric vehicle charging in line with current regulations.']),
 (A+'Exterior areas and communal amenities', [
  'Two designer pedestrian gates lead to two lobbies with a security post and/or reception.',
  'Cobbled pathways for vehicle and pedestrian access within the complex.',
  'The plot perimeter is enclosed by a designer metal lattice fence, framed by planting, with a designer welcome wall in the central area of the plot.',
  'Four designer vehicle gates with automatic opening by smart key, or similar.',
  'Every apartment has its own private pool, according to the design.',
  'A communal outdoor pool with an organic design evoking a natural pool, with saline chlorination and lighting, alongside a solarium with synthetic decking by Gunni&Trentino, or similar.',
  'A communal indoor pool.',
  'A fully equipped gym and spa.',
  'A meeting room for residents.',
  'Concierge service and 24/7 security.']),
]
