"""Générateur portable de l'infographie « Veille AM.Digital » (1080x1350).
Usage : python3 gen/veille_gen.py veille.json sortie.jpg
veille.json = {"date_label": "21 octobre 2026", "titre": "Texte avec *mot en or*", "sous_titre": "...",
               "signaux": [{"rubrique": "...", "titre": "... *or* ...", "decryptage": "...", "decision": "...", "source": "..."} x4]}
Les mots entre *étoiles* s'affichent en or. Textes courts : décryptage <= 120 caractères, décision <= 75.
Dépend uniquement de playwright (chromium) + Pillow ; polices et logo lus dans le kit (dossier parent).
"""
import json, os, re, sys, html as H
from playwright.sync_api import sync_playwright
from PIL import Image

K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "".join(f"@font-face{{font-family:M;font-weight:{w};src:url('file://{K}/fonts/woff2/montserrat-latin-{w}-normal.woff2')}}" for w in (500, 600, 700, 800))
LOGO = f"file://{K}/logo/am-digital-logo-carre.png"
BASE = "position:relative;overflow:hidden;box-sizing:border-box;color:#fff;font-family:M,Arial,sans-serif;display:flex;flex-direction:column"

def g(t):
    t = H.escape(t, quote=False)
    return re.sub(r"\*(.+?)\*", r'<span style="color:#f1bc18">\1</span>', t)

def card(n, s):
    return f'''<div style="display:flex;gap:22px;background:#300024;border-radius:20px;padding:15px 24px;align-items:flex-start">
<div style="flex:none;width:64px;height:64px;border-radius:14px;background:#66004a;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:800;color:#f1bc18">{n}</div>
<div style="flex:1;display:flex;flex-direction:column;gap:5px">
<div style="font-size:16px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#d9c3d2">{g(s['rubrique'])}</div>
<div style="font-size:28px;line-height:1.1;font-weight:800">{g(s['titre'])}</div>
<div style="font-size:19.5px;line-height:1.33;font-weight:500;color:#d9c3d2"><span style="color:#fff;font-weight:700">Décryptage · </span>{g(s['decryptage'])}</div>
<div style="font-size:19.5px;line-height:1.33;font-weight:600;color:#fff"><span style="color:#f1bc18;font-weight:800">Décision pour votre entreprise · </span>{g(s['decision'])}</div>
<div style="font-size:14px;color:#a88aa0">Source : {g(s['source'])}</div></div></div>'''

def page(v):
    cards = "".join(card(i + 1, s) for i, s in enumerate(v["signaux"][:4]))
    return f'''<div style="width:1080px;height:1350px;padding:52px 60px 40px;gap:14px;background:#3c0030;{BASE}">
<div style="position:absolute;right:120px;top:56px;width:52px;height:52px;background:#f1bc18"></div><div style="position:absolute;right:70px;top:30px;width:26px;height:26px;background:#f1bc18"></div><div style="position:absolute;right:72px;top:124px;width:26px;height:26px;background:#c79613"></div>
<div style="font-size:21px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">Veille AM.Digital · {g(v['date_label'])}</div>
<div style="font-size:50px;line-height:1;font-weight:800;text-transform:uppercase;max-width:860px">{g(v['titre'])}</div>
<div style="font-size:25px;font-weight:600;color:#d9c3d2;margin-bottom:6px">{g(v.get('sous_titre','Tendances com & marketing, décryptées pour les PME'))}</div>
<div style="display:flex;flex-direction:column;gap:12px">{cards}</div>
<div style="margin-top:auto;display:flex;justify-content:space-between;align-items:center;border-top:2px solid #5a2a4d;padding-top:14px;margin-bottom:8px"><div style="display:flex;align-items:center;gap:16px"><img src="{LOGO}" style="width:60px;height:60px;border-radius:8px"><div style="font-size:20px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#d9c3d2">La veille AM.Digital · chaque jour</div></div><div style="background:#f1bc18;color:#300024;font-size:22px;font-weight:800;padding:12px 26px;border-radius:999px">Enregistrez · Partagez</div></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:12px;background:#66004a"></div></div>'''

def main(src, out):
    v = json.load(open(src, encoding="utf-8"))
    tmp = os.path.abspath(out) + ".html"
    open(tmp, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT}body{{margin:0}}</style></head><body>{page(v)}</body></html>")
    with sync_playwright() as p:
        exe = "/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") and os.path.isfile("/opt/pw-browsers/chromium") else None
        b = p.chromium.launch(args=["--allow-file-access-from-files"], **({"executable_path": exe} if exe else {}))
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        # contrôle de débordement : le pied de page doit tenir dans 1350 px
        over = pg.evaluate("(()=>{const r=document.body.firstElementChild; return r.scrollHeight>r.clientHeight+2})()")
        png = out + ".png"; pg.query_selector("body>div").screenshot(path=png); b.close()
    Image.open(png).convert("RGB").save(out, quality=90, optimize=True); os.remove(png); os.remove(tmp)
    print("DEBORDEMENT : raccourcir les textes" if over else "ok", out)
    return 1 if over else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
