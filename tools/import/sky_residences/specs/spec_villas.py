# NOTE: working paths in this file (/Users/sasanraftari/Downloads/SkyMarbella_work, .../SkyMarbella_dropbox/x) are the importer's work dir and the unpacked Dropbox originals; re-point them to re-run. Written October 2026.
# -*- coding: utf-8 -*-
"""Villa quality specification groups (source: the developer's villa quality specification, 18 pages; the building-specifications summary is cross-checked in OPEN_ITEMS).
The lighting design firm is not named."""
V = 'Villas: '
SPEC_VILLAS = [
 (V+'Structure and walls', [
  'The foundations combine shallow and deep foundation solutions, depending on the requirements of each individual plot.',
  'The structure is reinforced concrete walls and columns, using waffle slabs or solid concrete slabs as required, in accordance with current building regulations.',
  'Exterior walls consist of a perforated solid brick outer leaf, a non-ventilated cavity with thermal insulation in line with current regulations, and a double hollow brick inner leaf. Interior and exterior finishes vary by design.',
  'Interior partition walls between rooms are perforated solid brick, finished in plaster, wallpaper or wood panelling depending on the design.',
  'The interior walls of the plant room are two perforated solid brick walls, one of them sound-resistant, with acoustic insulation between them to prevent sound transmission.']),
 (V+'Finishes and paintwork', [
  'Exterior surfaces are finished with rendering and porcelain tiling in various formats, depending on the design. The wall at the villa’s entrance is clad in wood alongside the front door, according to each villa’s design.',
  'Metal louvred shutters are used on certain bathroom windows for privacy, depending on the design.',
  'Upper-floor planters finished in rendering run along the bedroom terraces.',
  'Interior walls and vertical surfaces are finished in plaster, wallpaper or wood panelling, depending on the interior design scheme.',
  'False ceilings are plasterboard, with perimeter recesses for curtains and indirect LED strip lighting, according to the design. In certain wet areas, a wood-look removable ceiling is proposed.',
  'Wood-effect slatted ceilings are used on terraces and covered exterior areas.',
  'The exterior is finished with rendering and exterior paint in a range of light and dark tones, depending on the design.',
  'Interior walls and ceilings are painted with smooth white plastic paint where applicable.']),
 (V+'Flooring and wall cladding', [
  'For the ground floor and basement common areas, a large-format Inalco MDi is used, model Pacific Blanco Plus with a bush-hammered finish, supplied by Gunni&Trentino. It resembles a soft cream limestone. In wet areas, the same model is used with C2 specification as required by regulations.',
  'On the exterior flooring, both on the upper-floor bedroom terraces and the ground-floor living room terrace, the same large-format MDi used indoors is installed, with C3 specification per current regulations.',
  'Natural wood flooring is installed in the upper-floor hallway and bedrooms, laid in a herringbone pattern according to the design, model Carlac by Trentino Wood, supplied by Gunni&Trentino.',
  'Secondary bathroom wall cladding uses the same Inalco Pacific Blanco Plus bush-hammered MDi, combined with the large-format porcelain Premiere Amazzonite by Del Conca, also supplied by Gunni&Trentino. Both are installed floor-to-ceiling, depending on the design.',
  'The main bathroom cladding also uses Inalco Pacific Blanco Plus bush-hammered MDi, combined with the large-format porcelain Heritage Emerald by Florim, supplied by Gunni&Trentino. Both are installed floor-to-ceiling, depending on the design.',
  'The guest toilet cladding uses Inalco Pacific Blanco Plus bush-hammered MDi, combined with the large-format porcelain Heritage Flame by Florim, supplied by Gunni&Trentino. Both are installed floor-to-ceiling, depending on the design.',
  'The staircase treads between the ground and first floors are finished in wood, according to the design. The staircase treads between the ground floor and the basement are finished in Inalco.',
  'On the basement level, the hammam is finished with Zen Carrara mosaic by Ezarri, supplied by Gunni&Trentino.']),
 (V+'Exterior joinery', [
  'The sliding balcony doors to walkable terraces are slim-profile aluminium, Schüco brand, brown finish, with a flush floor-level threshold profile, thermal break and double glazing with solar control, low emissivity and a clear polyvinyl butyral layer.',
  'The remaining windows are also aluminium, with tilt-and-turn, hinged, pivoting or sliding opening systems depending on the design, Schüco brand, brown finish, with thermal break and the same double glazing.']),
 (V+'Interior joinery', [
  'A floor-to-ceiling pivoting entrance door, tall and wide, with no architrave, finished in natural iroko wood with a decorative grain pattern as per design, concealed security hinges and black-finished hardware.',
  'Interior doors finished in natural oak, with concealed black hinges, stainless steel hardware and a black-finished designer handle; depending on location, certain rooms include an interior privacy lock.',
  'Decorative panelling and/or porcelain or wood mosaics in selected areas of the home, depending on the design.',
  'Main bedroom walk-in wardrobes by Poliform, designed by Gunni&Trentino, with a lightweight aluminium-profile structure combining floor-to-ceiling graphic glass folding doors with metallic lacquered wood doors, depending on the design. Interiors are finished in a leather-effect material, with handles integrated into the aluminium profiles, indirect LED lighting and leather- or textile-effect accessories, designed to convey a sense of lightness.',
  'The remaining wardrobes throughout the home have an exclusive modular design for interior accessories, including LED lighting to highlight selected spaces.',
  'Flush wall skirting throughout the home, finished in wood or porcelain depending on the design.']),
 (V+'Lighting, sound and telecommunications', [
  'The lighting was designed in collaboration with a specialist lighting design firm, combining different moods and smart home controls tailored to each space’s needs, with the electrical connection boxes and the electrical and telecoms cabinets kept concealed.',
  'Two distinct lighting moods are created in the main rooms: LED lighting with a diffuser panel for indirect, recessed illumination, and, in kitchens and bathrooms, focused LED lighting to add subtlety to specific elements.',
  'General lighting is provided, depending on the design, by dimmable spotlights. In the living room and kitchen, a magnetic track lighting system allows the homeowner to personalise and reposition the light fittings in future.',
  'Both wireless and wired home-automation keypads are by Lutron, with a main touchscreen panel in the living room and master bedroom for smart control of lighting, climate and underfloor heating. The system also includes a video intercom for the development.',
  'All other rooms are fitted with a Lutron smart keypad, configurable to control temperature and lighting. Everything can be managed from the central panel or from any fixed or mobile device with internet or WiFi access: simulate daily-use routines, adjust the temperature, programme lighting schedules and view the entry-phone camera, among other features.',
  'Pre-installation for WiFi access points is included, providing full coverage throughout the house, with data and TV points in all bedrooms and the living room.']),
 (V+'Plumbing, air conditioning and underfloor heating', [
  'All hot and cold water installations comply with current regulations, using first-quality pipework for cold water and thermally insulated pipework for hot water, with partial flow shut-off valves in every wet room and individualised per fixture.',
  'An air-source heat pump (aerothermal) system produces domestic hot water and supplies water-based underfloor heating in common areas and bedrooms.',
  'Hot and cold air conditioning in the living room and bedrooms via ducting, with a multi-split VRF system individualised per room and integrated into the home-automation control, and linear diffusers flush-mounted to ceiling or wall depending on each area’s technical needs.',
  'Underfloor heating in common areas, bedrooms and the main bathroom (excluding the gym), via embedded hot-water pipework that also improves sound insulation, and electric underfloor heating in the guest toilet, secondary bathrooms and massage room.']),
 (V+'Bathrooms and WCs', [
  'Wall-hung porcelain toilets in matte white in the guest toilet and the main and secondary bathrooms, Laufen brand, with soft-close seat, concealed cistern and Geberit dual-flush front button, supplied by Gunni.',
  'In the main bathroom, depending on the design, a freestanding bathtub, model Carlota Trentino Solid, with a contemporary, minimalist design.',
  'Dornbracht taps in matte platinum finish, supplied by Gunni&Trentino, throughout all bathrooms and WCs, with a two-way independent thermostatic mixer and ceiling-mounted shower head, available wall-mounted, countertop-mounted or freestanding depending on each villa’s design.',
  'Shower trays flush with the home’s flooring, in an anti-slip finish and rectangular format, drained via a floor channel, with shower screens, dimensions and model according to the design.',
  'Laufen washbasins on a Trentino Bath designer vanity unit by Gunni&Trentino, with matching accessories by Windish (Gunni&Trentino) in a finish to match the taps.',
  'Mirrors in the bathrooms and guest WC, custom-designed for each space, with LED lighting and an anti-fog system as per design, by Gunni&Trentino.',
  'For the basement-level sauna and hammam, models Sky and Nuvola by Effe, supplied by Gunni&Trentino.']),
 (V+'Kitchens and appliances', [
  'A high-end living room kitchen, Poliform brand, in a metallic lacquered finish, personalised and adapted to the design and materials of the villas, with water-resistant surfaces, finishes up to ceiling height as per design, an integrated handle or push-up system and impact-resistant edges, a flat plinth, latest-generation hardware, soft-close hinges and concealed shelf supports, supplied and installed by Gunni&Trentino.',
  'Drawer units and cabinetry are built with an internal structure, fully fitted with accessories and concealed power outlets where applicable.',
  'The worktop is by Inalco, in MDi with a natural-stone-effect finish in a light limestone tone, depending on the design.',
  'A concealed secondary kitchen by Gunni&Trentino, of top specification and quality, in a high-durability laminate finish with an MDi worktop.',
  'A bar by Gunni&Trentino, of top specification and quality, in a lacquered finish, with decorative metal shelving with high-durability glass backing and a Dekton worktop in Sirus / Enzo Matte finish.',
  'Laundry rooms by Gunni&Trentino, custom-fitted to the space, in a high-durability laminate finish with a white Silk MDi worktop with a bush-hammered finish.',
  'A fully outdoor-rated exterior kitchen clad in Novara-brand MDi, supplied by Gunni&Trentino, with marine-grade stainless steel hardware and outdoor-specific appliances.',
  'In the living-room kitchen: a Bora induction hob with carbon-filter extraction integrated into the kitchen island; a Gaggenau 400 series oven, wine cooler, integrated fridge and microwave, each with Home Connect; a Gaggenau 200 series integrated dishwasher; and a Gessi kitchen tap.',
  'In the concealed secondary kitchen: a 90 cm Gaggenau oven with Home Connect; a Siemens induction hob, fridge and dishwasher, with extraction via a Pando-brand hood; Gessi taps; and a Veravent sink.',
  'In the bar: a Siemens fridge, a Siemens freezer, an integrated Siemens dishwasher and a Shock-brand sink.',
  'In the laundry rooms: a 9 kg Miele washing machine and a 9 kg Miele dryer, supplied by Gunni&Trentino.',
  'On the basement level, a purpose-designed wine cellar by Gunni&Trentino, with sliding glass doors and stainless steel metal framing, a capacity of 55 to 70 bottles depending on the villa, a +14/16 °C temperature control system and LED lighting.']),
 (V+'Private basement and garage', [
  'A fully finished individual private basement for each home, with an entrance hall, en-suite bedroom, WC, plant room, laundry and a multi-purpose area where applicable, with direct access from the garage.',
  'A space that can be converted into a gym, directly connected to the massage room, sensory shower, hammam and sauna.',
  'Direct access to the home from the private basement via a private staircase and lift, connecting the basement to every floor of the house.',
  'The basement flooring is identical to that of the main home, with walls finished in white paint and a false ceiling.',
  'Each home has covered parking for 2 cars (except Villa 10), with direct access to the home and provision for electric vehicle charging in line with current regulations.']),
 (V+'Exterior areas', [
  'Entrance to the residential complex with a security post, and paved roads for vehicle and pedestrian access throughout the development.',
  'The plot perimeter is delimited by Hercules-type fencing or a brick wall, depending on the design, accompanied by landscaping.',
  'A designer welcome wall at each home’s entrance, finished in stone or metal depending on the villa, and designer pedestrian access gates.',
  'An infinity-edge outdoor pool built in glass mosaic, Ezarri brand, pearl iris colour, supplied by Gunni&Trentino, rectangular with a “sun shelf” area, with saline chlorination and interior lighting.',
  'In some villas, depending on the design, a poolside sun deck built from Exterpark-brand synthetic decking or similar.']),
]
