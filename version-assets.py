"""Haengt an Bilder und Stylesheet in docs/*.html ein ?v=<hash> an, damit Browser nach einer
Aenderung sofort die neue Datei laden statt der zwischengespeicherten. Vor jedem Push ausfuehren:
    python3 version-assets.py
Der Hash kommt aus dem Dateiinhalt, unveraenderte Dateien behalten ihre Nummer."""
import hashlib, pathlib, re

DOCS = pathlib.Path(__file__).parent / "docs"
REF = re.compile(r'(assets/(?:img/[\w.-]+|style\.css))(\?v=[0-9a-f]+)?')

def stamp(m):
    path = m.group(1)
    digest = hashlib.sha1((DOCS / path).read_bytes()).hexdigest()[:8]
    return f"{path}?v={digest}"

for page in sorted(DOCS.glob("*.html")):
    old = page.read_text()
    new = REF.sub(stamp, old)
    if new != old:
        page.write_text(new)
        print("aktualisiert", page.name)
