"""Proposition vidéo A — Direction 1 « Signature AM.Digital » — V1 « 3 secondes pour convaincre » (voix off)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "gen"))
import motion4 as m

GOLD, AUB, DEEP = "#f1bc18", "#3c0030", "#1d0016"
css = f"""
.bg{{position:absolute;inset:0;background:radial-gradient(110% 70% at 30% 25%,#5e0048 0%,{AUB} 50%,{DEEP} 100%)}}
.px{{position:absolute;background:{GOLD}}}
.k{{font-family:M;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:{GOLD};font-size:34px}}
.h{{font-family:M;font-weight:800;color:#fff;line-height:1.02;letter-spacing:-.02em}}
.g{{color:{GOLD}}}
.ring{{position:absolute;left:190px;top:470px;width:700px;height:700px;border-radius:50%;border:6px solid rgba(241,188,24,.25)}}
.arc{{position:absolute;left:190px;top:470px;width:700px;height:700px;border-radius:50%;border:10px solid transparent;border-top-color:{GOLD};border-right-color:{GOLD}}}
.card{{position:absolute;left:110px;right:110px;height:190px;border-radius:28px;background:rgba(255,255,255,.06);border:2px solid rgba(241,188,24,.35);display:flex;align-items:center;gap:40px;padding:0 50px}}
.tick{{width:96px;height:96px;border-radius:24px;background:{GOLD};display:flex;align-items:center;justify-content:center;font-family:M;font-weight:800;font-size:64px;color:{AUB};flex:none}}
.phone{{position:absolute;left:290px;top:380px;width:500px;height:960px;border-radius:64px;border:14px solid #120010;background:#2a0021;overflow:hidden;box-shadow:0 40px 120px rgba(0,0,0,.6)}}
.post{{margin:26px;height:250px;border-radius:22px;background:linear-gradient(135deg,#4a0039,#2a0021);border:2px solid rgba(255,255,255,.08);position:relative}}.post:before{{content:"";position:absolute;left:24px;top:24px;width:54px;height:54px;border-radius:50%;background:rgba(241,188,24,.55)}}.post:after{{content:"";position:absolute;left:24px;right:24px;top:100px;bottom:24px;border-radius:14px;background:linear-gradient(120deg,rgba(255,255,255,.10),rgba(255,255,255,.03))}}
.feed{{animation:feed 2.4s cubic-bezier(.6,0,.3,1) calc(var(--t0) + .5s) both}}@keyframes feed{{to{{transform:translateY(-820px)}}}}
@keyframes wordon{{from{{opacity:.25;color:#fff}}to{{opacity:1;color:{GOLD}}}}}
"""
sub_css = """.sub{position:absolute;left:90px;right:150px;bottom:330px;text-align:center;font-family:M;font-weight:700;font-size:44px;line-height:1.3;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.6)}"""
pix = "".join(f'<div class="px a pop float" style="--d:{d}s;left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:{o}"></div>'
              for x, y, s, o, d in [(860, 150, 64, 1, .1), (950, 90, 30, 1, .2), (950, 240, 30, .7, .3), (80, 1740, 34, .5, .2), (140, 1800, 16, .4, .3)])
bg = f'<div class="bg"></div>{pix}'
logo = f'<img src="{m.LOGO}" style="width:120px;height:120px;border-radius:20px">'

scenes = [
    dict(say="Vous avez trois secondes.", min=2.6, impacts=[0.5], html=f"""
<div class="k a fade" style="--d:.1s;position:absolute;left:110px;top:340px">30 secondes de marketing</div>
<div class="ring a fade" style="--d:.1s"></div><div class="arc a spin" style="--du:3s;--d:0s;animation-iteration-count:infinite"></div>
<div class="h a slam" style="--d:.35s;position:absolute;left:0;right:0;top:560px;text-align:center;font-size:420px;color:{GOLD};text-shadow:0 0 80px rgba(241,188,24,.45)">3</div>
<div class="h a rise" style="--d:.7s;position:absolute;left:0;right:0;top:1220px;text-align:center;font-size:84px">secondes.</div>"""),
    dict(say="Pas une de plus.", min=1.8, html=f"""
<div class="h a slam" style="--d:.15s;position:absolute;left:110px;right:110px;top:700px;font-size:150px">PAS UNE</div>
<div class="h a slam g" style="--d:.45s;position:absolute;left:110px;right:110px;top:880px;font-size:150px">DE PLUS.</div>"""),
    dict(say="C'est le temps qu'un client vous accorde, avant de passer à la publication suivante.", html=f"""
<div class="phone a rise" style="--d:.05s"><div class="feed">{''.join('<div class="post"></div>' for _ in range(7))}</div></div>
<div class="k a left" style="--d:.4s;position:absolute;left:110px;top:310px">Le pouce défile…</div>"""),
    dict(say="En trois secondes, il doit voir qui vous êtes, ce que vous vendez, et comment vous joindre.", html=f"""
<div class="k a fade" style="--d:.1s;position:absolute;left:110px;top:380px">En 3 secondes, il doit voir :</div>
<div class="card a left" style="--d:.5s;top:560px"><div class="h" style="font-size:64px">Qui vous êtes</div></div>
<div class="card a left" style="--d:1.6s;top:800px"><div class="h" style="font-size:64px">Ce que vous vendez</div></div>
<div class="card a left" style="--d:2.7s;top:1040px"><div class="h" style="font-size:64px">Comment vous joindre</div></div>"""),
    dict(say="Une photo claire. Une bio en une ligne. Un contact visible.", html=f"""
<div class="card a fade" style="--d:.0s;top:560px"><div class="tick a pop" style="--d:.35s">✓</div><div class="h" style="font-size:64px">Photo claire</div></div>
<div class="card a fade" style="--d:.0s;top:800px"><div class="tick a pop" style="--d:1.35s">✓</div><div class="h" style="font-size:64px">Bio en une ligne</div></div>
<div class="card a fade" style="--d:.0s;top:1040px"><div class="tick a pop" style="--d:2.35s">✓</div><div class="h" style="font-size:64px">Contact visible</div></div>"""),
    dict(say="Faites le test ce soir. Et enregistrez cette vidéo.", html=f"""
<div class="h a blurin" style="--d:.1s;position:absolute;left:110px;right:110px;top:660px;font-size:120px">Faites le test <span class="g">ce soir.</span></div>
<div class="a pop" style="--d:1.4s;position:absolute;left:110px;top:1040px;background:{GOLD};color:{AUB};font-family:M;font-weight:800;font-size:52px;padding:30px 54px;border-radius:999px">Enregistrez cette vidéo</div>"""),
    dict(say="Écrivez-nous sur ouatsape. Am Digital.", sub="Écrivez-nous sur WhatsApp. AM.Digital.", min=3.6, quiet_music=True, zoom=1.0, html=f"""
<div class="a pop" style="--d:.1s;position:absolute;left:0;right:0;top:700px;display:flex;justify-content:center">{logo.replace('120px', '220px')}</div>
<div class="h a rise" style="--d:.4s;position:absolute;left:0;right:0;top:970px;text-align:center;font-size:76px">AM.Digital</div>
<div class="k a rise" style="--d:.6s;position:absolute;left:0;right:0;top:1080px;text-align:center;font-size:30px">Agence de communication · Abidjan</div>
<div class="a pop" style="--d:1.0s;position:absolute;left:150px;right:150px;top:1200px;text-align:center;background:{GOLD};color:{AUB};font-family:M;font-weight:800;font-size:44px;padding:26px;border-radius:999px">WhatsApp +225 01 71 95 45 23</div>"""),
]
spec = dict(name="A_signature", css=css, sub_css=sub_css, bg=bg, transition="blur", music=dict(bpm=122, seed=0, gain=.6), scenes=scenes)
if __name__ == "__main__":
    print(m.build(spec, sys.argv[1], work=sys.argv[2] if len(sys.argv) > 2 else None)["total"])
