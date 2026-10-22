"""Trois créations graphiques 1080x1350, une par direction artistique (charte AM.Digital : aubergine, or, Montserrat, logo).
G4 Flyer « Pack Visibilité digitale » (Signature) · G1 Infographie « Le baromètre digital » (Éditorial) · G11 « Le bulletin de notes de votre page » (Pop).
Chiffres G1 : DataReportal, Digital 2026: Côte d'Ivoire (fin 2025), vérifiés le 22 oct. 2026."""
import base64, io, pathlib, sys
import qrcode
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "gen"))
import motion4 as m

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
GOLD, AUB, DEEP, CREAM, INK, OR2 = "#f1bc18", "#3c0030", "#1d0016", "#f6f0e6", "#2a0020", "#b8900f"
buf = io.BytesIO(); qrcode.make("https://wa.me/2250171954523?text=DIAGNOSTIC", border=1, box_size=10).save(buf, format="PNG")
QR = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
LOGO = m.LOGO
BASE = "*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden}"

# ---------- D1 Signature : flyer offre ----------
items = ["Calendrier éditorial du mois", "Visuels et carrousels à votre charte", "Vidéos motion design avec voix off", "Gestion de vos pages et réponses", "Suivi mensuel des résultats"]
lis = "".join(f'<div style="display:flex;align-items:center;gap:20px;margin-bottom:22px"><div style="flex:none;width:46px;height:46px;border-radius:12px;background:{GOLD};color:{AUB};font-weight:800;font-size:30px;display:flex;align-items:center;justify-content:center">✓</div><div style="font-size:30px;font-weight:600;color:#fff">{t}</div></div>' for t in items)
post = lambda h: f'<div style="margin:16px;height:{h}px;border-radius:16px;background:linear-gradient(135deg,#5a0045,#2a0021);position:relative"><div style="position:absolute;left:16px;top:16px;width:36px;height:36px;border-radius:50%;background:{GOLD}"></div><div style="position:absolute;left:62px;top:22px;width:120px;height:10px;border-radius:5px;background:rgba(255,255,255,.35)"></div><div style="position:absolute;left:16px;right:16px;top:66px;bottom:16px;border-radius:10px;background:linear-gradient(120deg,rgba(241,188,24,.35),rgba(255,255,255,.05))"></div></div>'
D1 = f"""<div style="position:relative;width:1080px;height:1350px;background:radial-gradient(110% 70% at 25% 20%,#5e0048 0%,{AUB} 50%,{DEEP} 100%);font-family:M;color:#fff;overflow:hidden">
<div style="position:absolute;left:820px;top:70px;width:70px;height:70px;background:{GOLD}"></div><div style="position:absolute;left:905px;top:30px;width:34px;height:34px;background:{GOLD}"></div><div style="position:absolute;left:905px;top:160px;width:34px;height:34px;background:#c79613"></div>
<div style="position:absolute;left:70px;top:70px;font-size:22px;font-weight:800;letter-spacing:.2em;color:{GOLD}">OFFRE AM.DIGITAL</div>
<div style="position:absolute;left:70px;top:120px;font-size:92px;font-weight:800;line-height:.98;letter-spacing:-.02em">Pack<br><span style="color:{GOLD}">Visibilité</span><br>digitale</div>
<div style="position:absolute;left:70px;top:440px;width:560px;font-size:30px;line-height:1.4;color:#e8d6e2;font-weight:500">Votre communication tenue chaque semaine, sans y passer vos soirées.</div>
<div style="position:absolute;left:70px;top:600px;width:600px">{lis}</div>
<div style="position:absolute;left:690px;top:330px;width:330px;height:640px;border-radius:46px;border:12px solid #120010;background:#2a0021;overflow:hidden;transform:rotate(6deg);box-shadow:0 40px 90px rgba(0,0,0,.55)">
<div style="padding:18px 16px 4px;font-size:15px;font-weight:700;color:{GOLD};letter-spacing:.1em">PAGE EXEMPLE</div>{post(170)}{post(170)}{post(170)}</div>
<div style="position:absolute;left:70px;right:70px;bottom:70px;height:190px;border-radius:28px;background:rgba(255,255,255,.07);border:2px solid rgba(241,188,24,.4);display:flex;align-items:center;gap:30px;padding:0 30px">
<img src="{QR}" style="width:140px;height:140px;border-radius:10px;background:#fff;padding:6px">
<div style="flex:1"><div style="font-size:24px;font-weight:600;color:#e8d6e2">Scannez ou écrivez <b style="color:{GOLD}">DIAGNOSTIC</b> sur WhatsApp</div><div style="font-size:42px;font-weight:800;margin-top:6px">+225 01 71 95 45 23</div></div>
<img src="{LOGO}" style="width:96px;height:96px;border-radius:16px"></div></div>"""

# ---------- D2 Éditorial : infographie baromètre ----------
def bar(label, val, frac, color):
    return (f'<div style="margin-bottom:26px"><div style="display:flex;justify-content:space-between;font-family:M;font-weight:700;font-size:24px;color:{INK}"><span>{label}</span><span>{val}</span></div>'
            f'<div style="margin-top:10px;height:34px;background:rgba(74,0,56,.10)"><div style="height:34px;width:{frac*100:.1f}%;background:{color}"></div></div></div>')
D2 = f"""<div style="position:relative;width:1080px;height:1350px;background:{CREAM};color:{INK};font-family:M;padding:60px 70px">
<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:4px solid {INK};padding-bottom:12px">
<div style="font-family:PF;font-weight:900;font-size:44px">AM.Digital <span style="font-style:italic;font-weight:400">Le Baromètre</span></div>
<div style="font-size:17px;font-weight:700;letter-spacing:.18em">N° 01 · OCTOBRE 2026</div></div>
<div style="height:1px;background:{OR2};margin-top:5px"></div>
<div style="margin-top:40px;font-size:19px;font-weight:700;letter-spacing:.22em;color:{OR2}">CÔTE D'IVOIRE · LE DIGITAL FIN 2025</div>
<div style="margin-top:10px;font-family:PF;font-weight:900;font-size:76px;line-height:1">Qui est en ligne&nbsp;?</div>
<div style="margin-top:44px;display:grid;grid-template-columns:1fr 1fr;gap:0 60px">
<div style="border-right:1px solid rgba(42,0,32,.25);padding-right:40px">
<div style="font-size:19px;font-weight:700;letter-spacing:.16em;color:{OR2}">INTERNAUTES</div>
<div style="font-family:PF;font-weight:900;font-size:150px;line-height:1;color:#4a0038">13,4<span style="font-style:italic;font-weight:400;font-size:60px"> M</span></div>
<div style="font-family:PF;font-style:italic;font-size:30px;margin-top:6px">soit 40,7 % de la population</div></div>
<div><div style="font-size:19px;font-weight:700;letter-spacing:.16em;color:{OR2}">FACEBOOK</div>
<div style="font-family:PF;font-weight:900;font-size:150px;line-height:1;color:#4a0038">8,4<span style="font-style:italic;font-weight:400;font-size:60px"> M</span></div>
<div style="font-family:PF;font-style:italic;font-size:30px;margin-top:6px">47,8 % des adultes</div></div></div>
<div style="margin-top:50px;font-size:19px;font-weight:700;letter-spacing:.16em;color:{OR2}">AUDIENCES DES RÉSEAUX (MILLIONS)</div>
<div style="margin-top:20px">{bar("Facebook", "8,4 M", 8.4/8.4, "#4a0038")}{bar("Instagram", "0,895 M", 0.895/8.4, OR2)}</div>
<div style="margin-top:14px;display:flex;gap:40px;align-items:center">
<div style="width:200px;height:200px;border-radius:50%;background:conic-gradient(#4a0038 0 61.3%,{OR2} 61.3% 100%);display:flex;align-items:center;justify-content:center"><div style="width:120px;height:120px;border-radius:50%;background:{CREAM}"></div></div>
<div><div style="font-size:19px;font-weight:700;letter-spacing:.16em;color:{OR2}">PROFILS SUR LES RÉSEAUX SOCIAUX</div>
<div style="font-family:PF;font-size:40px;margin-top:10px"><b style="color:#4a0038">61,3 %</b> d'hommes · <b style="color:{OR2}">38,7 %</b> de femmes</div>
<div style="font-family:PF;font-style:italic;font-size:28px;margin-top:10px;color:#4d3a46">Votre client y est. Reste à y être bien.</div></div></div>
<div style="position:absolute;left:70px;right:70px;bottom:50px;border-top:1px solid {INK};padding-top:16px;display:flex;justify-content:space-between;align-items:center">
<div style="font-size:16px;font-weight:600;color:#6d5a66;max-width:760px">Source : DataReportal, Digital 2026 : Côte d'Ivoire (données fin 2025). Audiences publicitaires Meta, non comparables aux utilisateurs actifs.</div>
<img src="{LOGO}" style="width:62px;height:62px;border-radius:10px"></div></div>"""

# ---------- D3 Pop : bulletin de notes ----------
rows = [("Photo de profil", "16"), ("Bio", "09"), ("Régularité", "07"), ("Réponses aux messages", "05"), ("Appel à l'action", "08")]
trs = "".join(f'<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:3px dashed rgba(48,0,36,.35);padding:8px 0"><div style="font-family:M;font-weight:800;font-size:32px">{a}</div><div style="font-family:AN;font-size:54px;color:{"#d6332a" if int(b) < 10 else AUB}">{b}<span style="font-size:32px;color:{AUB}">/20</span></div></div>' for a, b in rows)
D3 = f"""<div style="position:relative;width:1080px;height:1350px;background:{GOLD};font-family:M;color:{AUB};overflow:hidden">
<div style="position:absolute;right:-30px;top:-40px;width:200px;height:1500px;background:repeating-conic-gradient(from 45deg,{'#300024'} 0 25%,transparent 0 50%) 0 0/60px 60px"></div>
<div style="position:absolute;right:170px;top:0;width:30px;height:1350px;background:#66004a"></div>
<div style="position:absolute;left:60px;top:50px;font-family:AN;font-size:116px;line-height:.9;text-transform:uppercase">Le bulletin<br>de votre page</div>
<div style="position:absolute;left:60px;top:275px;background:{AUB};color:{GOLD};font-weight:800;font-size:22px;letter-spacing:.14em;padding:10px 18px">TRIMESTRE 4 · EXEMPLE</div>
<div style="position:absolute;left:60px;top:350px;width:740px;background:#fffaf0;border:5px solid {AUB};padding:24px 36px;box-shadow:16px 16px 0 {AUB};transform:rotate(-1.2deg)">{trs}
<div style="display:flex;justify-content:space-between;align-items:center;padding-top:18px"><div style="font-family:AN;font-size:48px">MOYENNE</div><div style="font-family:AN;font-size:72px;color:#d6332a">09<span style="font-size:36px;color:{AUB}">/20</span></div></div>
<div style="margin-top:6px;font-family:PF;font-style:italic;font-size:30px">Appréciation : « Peut mieux faire. »</div></div>
<div style="position:absolute;left:690px;top:225px;width:170px;height:170px;border-radius:50%;border:8px solid #d6332a;color:#d6332a;transform:rotate(-14deg);display:flex;align-items:center;justify-content:center;text-align:center;font-family:AN;font-size:34px;line-height:1;background:rgba(255,250,240,.0)">À<br>REVOIR</div>
<div style="position:absolute;left:60px;top:1150px;width:560px;background:{AUB};color:#fff;font-weight:700;font-size:30px;line-height:1.3;padding:24px 28px">Et votre page, combien sur 20 ?<br><span style="color:{GOLD}">Notez-la en commentaire.</span></div>
<div style="position:absolute;left:660px;top:1240px;font-weight:800;font-size:22px;display:flex;align-items:center;gap:12px"><img src="{LOGO}" style="width:54px;height:54px;border-radius:10px">AM.Digital</div></div>"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    for name, html in (("G4_flyer_signature", D1), ("G1_infographie_editorial", D2), ("G11_bulletin_pop", D3)):
        f = OUT / f"{name}.html"; f.write_text(f"<html><head><meta charset='utf-8'><style>{m.fonts_css()}{BASE}</style></head><body>{html}</body></html>", encoding="utf-8")
        pg = b.new_page(viewport={"width": 1080, "height": 1350}); pg.goto(f"file://{f}"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"{name}.png")); pg.close(); f.unlink()
    b.close()
print("ok")
