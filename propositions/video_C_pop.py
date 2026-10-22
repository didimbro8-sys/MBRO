"""Proposition vidéo C — Direction 3 « Pop audacieux » — V2 « Booster : bonne ou mauvaise idée ? » (voix off)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "gen"))
import motion4 as m

GOLD, AUB, PLUM = "#f1bc18", "#300024", "#66004a"
css = f"""
.bg{{position:absolute;inset:0;background:{GOLD}}}
.wax{{position:absolute;right:-30px;top:-40px;width:260px;height:2000px;background:repeating-conic-gradient(from 45deg,{AUB} 0 25%,transparent 0 50%) 0 0/64px 64px;opacity:.95}}
.stripe{{position:absolute;right:230px;top:0;width:34px;height:1920px;background:{PLUM}}}
.an{{font-family:AN;color:{AUB};text-transform:uppercase;line-height:.92}}
.tag{{position:absolute;left:70px;top:230px;background:{AUB};color:{GOLD};font-family:M;font-weight:800;font-size:30px;letter-spacing:.14em;text-transform:uppercase;padding:14px 22px}}
.box{{position:absolute;left:70px;width:700px;background:{AUB};color:#fff;font-family:M;font-weight:700;font-size:42px;line-height:1.3;padding:34px 40px}}
.band{{position:absolute;left:70px;width:720px;height:150px;display:flex;align-items:center;gap:28px;padding:0 34px;font-family:AN;font-size:96px;text-transform:uppercase}}
.n{{font-family:AN;font-size:70px;width:84px;height:84px;display:flex;align-items:center;justify-content:center;border-radius:50%}}
.bill{{position:absolute;width:420px;height:210px;border-radius:18px;background:#2f7d4f;border:8px solid #e9f1e6;display:flex;align-items:center;justify-content:center;font-family:AN;font-size:80px;color:#e9f1e6;box-shadow:0 30px 60px rgba(48,0,36,.35)}}
.fly{{animation-name:fly;animation-timing-function:cubic-bezier(.5,0,.8,.4)}}@keyframes fly{{from{{transform:translate(0,0) rotate(-6deg)}}to{{transform:translate(520px,-1300px) rotate(38deg)}}}}
.back{{animation-name:back;animation-timing-function:cubic-bezier(.2,.9,.3,1)}}@keyframes back{{from{{transform:translate(520px,-1300px) rotate(38deg)}}to{{transform:translate(0,0) rotate(-6deg)}}}}
.like{{position:absolute;font-family:M;font-weight:800;color:{AUB};width:120px;height:120px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:44px;box-shadow:0 14px 30px rgba(48,0,36,.25)}}
.rain{{animation-name:rain;animation-timing-function:linear}}@keyframes rain{{from{{transform:translateY(-500px)}}to{{transform:translateY(1500px)}}}}
.x{{position:absolute;height:22px;background:#d6332a}}
@keyframes wordon{{from{{opacity:.3}}to{{opacity:1}}}}
"""
sub_css = f""".sub{{position:absolute;left:70px;right:330px;bottom:300px;font-family:M;font-weight:800;font-size:42px;line-height:1.3;color:{AUB}}}
.sub .word{{background:transparent}}"""
bg = f'<div class="bg"></div><div class="wax a fade" style="--d:0s"></div><div class="stripe a growy" style="--d:.1s;--du:.8s"></div>'
logo = f'<img src="{m.LOGO}" style="width:120px;height:120px;border-radius:18px">'
likes = "".join(f'<div class="like a rain" style="--d:{d}s;--du:2.6s;left:{x}px;top:0">+1</div>' for x, d in [(90, .0), (330, .4), (560, .15), (200, .9), (470, 1.2)])

scenes = [
    dict(say="Vous payez pour des laïques ?", sub="Vous payez pour des likes ?", min=2.6, impacts=[0.25], html=f"""
{likes}<div class="tag a drop" style="--d:.05s">Publicité · Le vrai coût</div>
<div class="an a slam" style="--d:.2s;position:absolute;left:62px;top:420px;font-size:205px">VOUS<br>PAYEZ<br>POUR DES</div>
<div class="an a slam" style="--d:.7s;position:absolute;left:62px;top:1010px;font-size:230px;color:#fff;-webkit-text-stroke:6px {AUB}">LIKES ?</div>"""),
    dict(say="Bouster une publication sans objectif, c'est jeter de l'argent par la fenêtre.", sub="Booster une publication sans objectif, c'est jeter de l'argent par la fenêtre.", html=f"""
<div class="bill a fly" style="--d:1.6s;--du:1.6s;left:200px;top:880px">FCFA</div>
<div class="an a left" style="--d:.1s;position:absolute;left:62px;top:330px;font-size:170px">BOOSTER<br>SANS<br>OBJECTIF</div>
<div class="x a strike" style="--d:1.2s;--du:.4s;left:50px;top:560px;width:640px"></div>
<div class="box a rise" style="--d:2.0s;top:1180px">= de l'argent jeté par la fenêtre.</div>"""),
    dict(say="Avant de dépenser un seul franc, fixez cinq choses.", impacts=[1.2], html=f"""
<div class="an a left" style="--d:.1s;position:absolute;left:62px;top:330px;font-size:120px">AVANT DE<br>DÉPENSER,<br>FIXEZ</div>
<div class="an a slam" style="--d:1.1s;position:absolute;left:40px;top:690px;font-size:620px;color:{PLUM}">5</div>
<div class="an a right" style="--d:1.5s;position:absolute;left:390px;top:1060px;font-size:120px">CHOSES</div>"""),
    dict(say="Un objectif. Une audience. Une offre. Un budget. Une mesure.", tail=.7, html="".join(
        f'<div class="band a left" style="--d:{.25 + k*0.78:.2f}s;top:{360 + k*175}px;background:{AUB if k % 2 == 0 else "#fff"};color:{GOLD if k % 2 == 0 else AUB}">'
        f'<div class="n" style="background:{GOLD if k % 2 == 0 else AUB};color:{AUB if k % 2 == 0 else GOLD}">{k+1}</div>{w}</div>'
        for k, w in enumerate(["Objectif", "Audience", "Offre", "Budget", "Mesure"]))),
    dict(say="Sans ces cinq réponses, gardez votre argent.", impacts=[1.0], html=f"""
<div class="bill a back" style="--d:.0s;--du:1.1s;left:200px;top:880px">FCFA</div>
<div class="an a slam" style="--d:.9s;position:absolute;left:62px;top:360px;font-size:170px">GARDEZ<br>VOTRE<br>ARGENT.</div>"""),
    dict(say="Enregistrez cette vidéo, avant votre prochain boust.", sub="Enregistrez cette vidéo, avant votre prochain boost.", html=f"""
<div class="an a slam" style="--d:.1s;position:absolute;left:62px;top:430px;font-size:158px">ENREGISTREZ</div>
<div class="box a rise" style="--d:.7s;top:700px;font-size:48px">avant votre prochain boost.</div>"""),
    dict(say="Écrivez-nous sur ouatsape. Am Digital.", sub="Écrivez-nous sur WhatsApp. AM.Digital.", min=3.6, quiet_music=True, zoom=1.0, html=f"""
<div class="a pop" style="--d:.1s;position:absolute;left:70px;top:520px">{logo.replace('120px', '200px')}</div>
<div class="an a left" style="--d:.4s;position:absolute;left:70px;top:770px;font-size:150px">AM.DIGITAL</div>
<div class="box a rise" style="--d:.9s;top:960px;font-size:44px;width:720px">WhatsApp<br><span style="color:{GOLD};font-size:52px">+225 01 71 95 45 23</span></div>"""),
]
spec = dict(name="C_pop", css=css, sub_css=sub_css, bg=bg, transition="slide", music=dict(bpm=128, seed=7, gain=.6), scenes=scenes)
if __name__ == "__main__":
    print(m.build(spec, sys.argv[1], work=sys.argv[2] if len(sys.argv) > 2 else None)["total"])
