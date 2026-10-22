"""Trois directions artistiques, même contenu (G1 baromètre) — échantillons 1080x1350."""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
K = pathlib.Path.home() / "kit"
FS = D / "node_modules/@fontsource"
def ff(name, path, w, style="normal"):
    return f"@font-face{{font-family:{name};font-weight:{w};font-style:{style};src:url('file://{path}')}}"
FONTS = "".join([
    *(ff("M", K / f"fonts/woff2/montserrat-latin-{w}-normal.woff2", w) for w in (500, 600, 700, 800)),
    *(ff("PF", FS / f"playfair-display/files/playfair-display-latin-{w}-normal.woff2", w) for w in (400, 700, 900)),
    ff("PF", FS / "playfair-display/files/playfair-display-latin-400-italic.woff2", 400, "italic"),
    ff("AN", FS / "anton/files/anton-latin-400-normal.woff2", 400),
])
LOGO = "data:image/png;base64," + base64.b64encode((K / "logo/am-digital-logo-carre.png").read_bytes()).decode()
BASE = "*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden}"

# Direction 1 : Signature AM.Digital (aubergine + or, pixels, néon)
px = "".join(
    f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c};opacity:{o}"></div>'
    for x, y, s, c, o in [(820,90,70,"#f1bc18",1),(905,40,34,"#f1bc18",1),(910,175,34,"#c79613",1),(760,190,22,"#f1bc18",.6),
                          (980,250,18,"#f1bc18",.5),(70,1010,26,"#f1bc18",.5),(110,1050,14,"#f1bc18",.35)])
D1 = f"""<div style="position:relative;width:1080px;height:1350px;background:radial-gradient(120% 80% at 20% 30%,#5a0045 0%,#300024 55%,#1d0016 100%);font-family:M;color:#fff;padding:80px 78px">
{px}
<div style="font-size:22px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:#f1bc18">Le baromètre digital · Côte d'Ivoire</div>
<div style="margin-top:260px;font-size:300px;line-height:.9;font-weight:800;letter-spacing:-.04em;color:#f1bc18;text-shadow:0 0 60px rgba(241,188,24,.35)">8,4<span style="font-size:150px"> M</span></div>
<div style="margin-top:30px;font-size:46px;line-height:1.18;font-weight:700;max-width:820px">utilisateurs de Facebook en Côte d'Ivoire fin 2025.</div>
<div style="margin-top:46px;height:4px;width:120px;background:#f1bc18"></div>
<div style="margin-top:40px;font-size:34px;line-height:1.35;font-weight:500;color:#e8d6e2;max-width:830px">Votre client y est. La vraie question : <b style="color:#fff">comment y être bien ?</b></div>
<div style="position:absolute;left:78px;right:78px;bottom:64px;display:flex;align-items:center;justify-content:space-between;border-top:2px solid #5a2a4d;padding-top:26px">
<div style="display:flex;align-items:center;gap:18px"><img src="{LOGO}" style="width:64px;height:64px;border-radius:10px"><div style="font-size:18px;color:#bfa3b6;font-weight:600">Source : DataReportal, Digital 2026</div></div>
<div style="background:#f1bc18;color:#300024;font-size:22px;font-weight:800;padding:14px 28px;border-radius:999px">Enregistrez · Partagez</div></div></div>"""

# Direction 2 : Éditorial magazine (crème, Playfair, filets or)
D2 = f"""<div style="position:relative;width:1080px;height:1350px;background:#f6f0e6;color:#2a0020;font-family:M;padding:70px 80px">
<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #2a0020;padding-bottom:16px">
<div style="font-family:PF;font-weight:900;font-size:44px;letter-spacing:-.01em">AM.Digital <span style="font-style:italic;font-weight:400">Le Baromètre</span></div>
<div style="font-size:16px;font-weight:700;letter-spacing:.18em;text-transform:uppercase">N° 01 · Octobre 2026</div></div>
<div style="height:1px;background:#b8900f;margin-top:6px"></div>
<div style="margin-top:70px;font-size:20px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:#b8900f">Côte d'Ivoire · Réseaux sociaux</div>
<div style="margin-top:20px;font-family:PF;font-weight:900;font-size:330px;line-height:.85;letter-spacing:-.03em;color:#4a0038">8,4<span style="font-size:120px;font-weight:400;font-style:italic"> millions</span></div>
<div style="margin-top:36px;display:grid;grid-template-columns:1fr 1fr;gap:56px">
<div style="font-family:PF;font-size:40px;line-height:1.2;font-style:italic">d'utilisateurs de Facebook en Côte d'Ivoire, fin 2025.</div>
<div style="border-left:2px solid #b8900f;padding-left:28px;font-size:25px;line-height:1.5;font-weight:500;color:#4d3a46">Votre client y est déjà. La question n'est plus « faut-il y être ? » mais <b style="color:#2a0020">« comment y être bien ? »</b></div></div>
<div style="position:absolute;left:80px;right:80px;bottom:60px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #2a0020;padding-top:22px">
<div style="font-size:17px;font-weight:600;color:#6d5a66">Source : DataReportal, Digital 2026</div>
<div style="display:flex;align-items:center;gap:16px"><div style="font-family:PF;font-style:italic;font-size:24px">Enregistrez, partagez.</div><img src="{LOGO}" style="width:58px;height:58px;border-radius:8px"></div></div></div>"""

# Direction 3 : Pop audacieux (aplat or, condensée, motif géométrique inspiré du wax)
pattern = ("repeating-conic-gradient(from 45deg,#300024 0 25%,transparent 0 50%) 0 0/60px 60px")
D3 = f"""<div style="position:relative;width:1080px;height:1350px;background:#f1bc18;font-family:M;color:#300024;overflow:hidden">
<div style="position:absolute;right:-40px;top:0;width:250px;height:1350px;background:{pattern};opacity:.9"></div>
<div style="position:absolute;right:210px;top:0;width:34px;height:1350px;background:#66004a"></div>
<div style="position:absolute;left:70px;top:70px;background:#300024;color:#f1bc18;font-size:22px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;padding:12px 20px">Côte d'Ivoire · Le chiffre</div>
<div style="position:absolute;left:58px;top:170px;font-family:AN;font-size:370px;line-height:.9;letter-spacing:-.01em;color:#300024">8,4M</div>
<div style="position:absolute;left:70px;top:600px;width:640px;font-family:AN;font-size:78px;line-height:1.02;text-transform:uppercase">utilisateurs de Facebook fin 2025</div>
<div style="position:absolute;left:70px;top:860px;width:620px;background:#300024;color:#fff;font-size:32px;line-height:1.35;font-weight:600;padding:30px 34px">Votre client y est.<br><span style="color:#f1bc18;font-weight:800">Êtes-vous là où il regarde ?</span></div>
<div style="position:absolute;left:70px;bottom:64px;display:flex;align-items:center;gap:18px"><img src="{LOGO}" style="width:64px;height:64px;border-radius:10px"><div style="font-size:18px;font-weight:700">Source : DataReportal, Digital 2026</div></div></div>"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    for name, html in (("D1_signature", D1), ("D2_editorial", D2), ("D3_pop", D3)):
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        f = D / f"{name}.html"; f.write_text(f"<html><head><meta charset='utf-8'><style>{FONTS}{BASE}</style></head><body>{html}</body></html>", encoding="utf-8")
        pg.goto(f"file://{f}"); pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(600)
        pg.screenshot(path=str(D / f"{name}.png"))
        pg.close()
    b.close()
print("ok")
