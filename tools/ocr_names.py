"""Reads the text printed inside images and reports any that looks like one of the given names.

    python3 tools/ocr_names.py "Helvet Green" "Top Gestión" -- img1.jpg img2.jpg

Prints one JSON object per hit and exits 3 if there is any. The anonymisation guard reads project
text and cannot read pixels; this is the pixel half, used by scripts/review_project_images.mjs.
Needs `pip3 install rapidocr-onnxruntime`; exits 0 silently with a note on stderr when it is missing,
so a machine without it (Netlify) is unaffected.
"""
import difflib, json, re, sys
STOP = {'RESIDENCES', 'RESIDENCE', 'VILLAS', 'HOMES', 'BY', 'THE', 'GRUPO', 'INMOBILIARIO', 'PROMOTER', 'RECORD',
        'COSTA', 'SOL', 'MARBELLA', 'ESTEPONA', 'LIVING', 'NUEVA', 'GOLF', 'VALLEY', 'BAY', 'SPAIN', 'GROUP', 'DEVELOPMENT',
        'CONSTRUCTION', 'DESIGN', 'BUILDING', 'CAPITAL', 'ESTATE', 'GREEN', 'CLUB', 'SL', 'SLU'}
def main():
    i = sys.argv.index('--')
    names, files = sys.argv[1:i], sys.argv[i + 1:]
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        print('ocr_names: rapidocr-onnxruntime not installed, text-in-image check skipped', file=sys.stderr); return 0
    words = set()
    for n in names:
        whole = re.sub(r'[^A-ZÁÉÍÓÚÑ]', '', n.upper())
        if len(whole) >= 5: words.add(whole)
        for w in re.findall(r'[A-Za-zÁÉÍÓÚÑáéíóúñ]{4,}', n):
            if w.upper() not in STOP: words.add(w.upper())
    ocr, hits = RapidOCR(), 0
    for f in files:
        result, _ = ocr(f)
        for _, text, conf in (result or []):
            t = re.sub(r'[^A-ZÁÉÍÓÚÑ]', '', text.upper())
            if len(t) < 4 or float(conf) < 0.5: continue
            for w in words:
                if w in t or difflib.SequenceMatcher(None, w, t).ratio() >= 0.72:
                    print(json.dumps({'file': f, 'text': text, 'name': w})); hits += 1; break
    return 3 if hits else 0
sys.exit(main())
