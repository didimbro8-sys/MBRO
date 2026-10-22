"""Proposition vidéo B — Direction 2 « Éditorial magazine » — Le baromètre digital de la Côte d'Ivoire (voix off).
Chiffres : DataReportal, Digital 2026: Côte d'Ivoire (fin 2025), vérifiés le 22 oct. 2026 :
internet 13,4 M (40,7 % de la population) ; Facebook 8,40 M ; Instagram 895 000 (audiences publicitaires Meta)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "gen"))
import motion4 as m

INK, CREAM, GOLD, AUB = "#2a0020", "#f6f0e6", "#b8900f", "#4a0038"
css = f"""
.bg{{position:absolute;inset:0;background:{CREAM}}}
.grain{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(42,0,32,.025) 0 2px,transparent 2px 6px)}}
.mast{{position:absolute;left:80px;right:80px;top:150px;border-bottom:4px solid {INK};padding-bottom:16px;display:flex;justify-content:space-between;align-items:flex-end}}
.pf{{font-family:PF;color:{INK}}}
.m{{font-family:M;color:{INK}}}
.kk{{font-family:M;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:{GOLD};font-size:28px}}
.rule{{position:absolute;height:2px;background:{GOLD}}}
.bar{{position:absolute;left:80px;height:90px;background:{AUB}}}
.barbg{{position:absolute;left:80px;right:80px;height:90px;background:rgba(74,0,56,.10)}}
.quote{{font-family:PF;font-style:italic;color:{INK}}}
@keyframes wordon{{from{{opacity:.25}}to{{opacity:1}}}}
"""
sub_css = f""".sub{{position:absolute;left:90px;right:150px;bottom:300px;text-align:left;font-family:M;font-weight:600;font-size:40px;line-height:1.35;color:{INK};border-left:6px solid {GOLD};padding-left:26px}}"""
bg = f"""<div class="bg"></div><div class="grain"></div>
<div class="mast a fade" style="--d:.1s"><div class="pf" style="font-weight:900;font-size:52px">AM.Digital <span style="font-style:italic;font-weight:400">Le Baromètre</span></div>
<div class="m" style="font-weight:700;font-size:20px;letter-spacing:.18em">N° 01 · OCT. 2026</div></div>
<div class="rule a grow" style="--d:.3s;--du:1s;left:80px;right:80px;top:236px"></div>"""
logo = f'<img src="{m.LOGO}" style="width:110px;height:110px;border-radius:16px">'

scenes = [
    dict(say="Le baromètre Am Digital. Le digital en Côte d'Ivoire, à la fin de deux mille vingt-cinq.", sub="Le baromètre AM.Digital. Le digital en Côte d'Ivoire, à la fin de 2025.", min=4.2, html=f"""
<div class="kk a fade" style="--d:.4s;position:absolute;left:80px;top:570px">Côte d'Ivoire · Chiffres clés</div>
<div class="pf a wipeup" style="--d:.6s;--du:1s;position:absolute;left:80px;right:80px;top:650px;font-weight:900;font-size:150px;line-height:1">Le digital,</div>
<div class="pf a wipeup" style="--d:1.0s;--du:1s;position:absolute;left:80px;right:80px;top:810px;font-style:italic;font-size:130px;line-height:1">en chiffres.</div>
<div class="rule a grow" style="--d:1.6s;--du:1.2s;left:80px;width:300px;top:1010px;height:6px"></div>"""),
    dict(say="Treize virgule quatre millions de personnes utilisent internet.", sub="13,4 millions de personnes utilisent internet.", impacts=[0.6], html=f"""
<div class="kk a fade" style="--d:.1s;position:absolute;left:80px;top:570px">Internautes</div>
<div class="pf" style="position:absolute;left:70px;top:630px;font-weight:900;font-size:300px;line-height:1;color:{AUB}">{m.reel(1,.2,w=".5em")}{m.reel(3,.35)}<span style="margin-left:-.04em">,</span>{m.reel(4,.5)}</div>
<div class="quote a rise" style="--d:1.0s;position:absolute;left:80px;top:1000px;font-size:90px">millions</div>"""),
    dict(say="Soit quarante virgule sept pour cent de la population.", sub="Soit 40,7 % de la population.", html=f"""
<div class="kk a fade" style="--d:.1s;position:absolute;left:80px;top:570px">Part de la population en ligne</div>
<div class="pf a blurin" style="--d:.2s;position:absolute;left:80px;top:650px;font-weight:900;font-size:200px;color:{AUB}">40,7 %</div>
<div class="barbg" style="top:930px"></div><div class="bar a grow" style="--d:.5s;--du:1.6s;top:930px;width:{int(920*0.407)}px"></div>
<div class="m a fade" style="--d:1.8s;position:absolute;left:80px;top:1040px;font-size:28px;font-weight:600;color:#6d5a66">sur 100 % de la population</div>"""),
    dict(say="Fèïsse-bouk, c'est huit virgule quatre millions d'utilisateurs.", sub="Facebook, c'est 8,4 millions d'utilisateurs.", impacts=[0.7], html=f"""
<div class="kk a fade" style="--d:.1s;position:absolute;left:80px;top:570px">Facebook</div>
<div class="pf" style="position:absolute;left:70px;top:620px;font-weight:900;font-size:360px;line-height:1;color:{AUB}">{m.reel(8,.25)}<span style="margin-left:-.04em">,</span>{m.reel(4,.45)}</div>
<div class="quote a rise" style="--d:1.0s;position:absolute;left:80px;top:1030px;font-size:100px">millions</div>"""),
    dict(say="Instagram, huit cent quatre-vingt-quinze mille.", sub="Instagram : 895 000.", html=f"""
<div class="kk a fade" style="--d:.1s;position:absolute;left:80px;top:570px">Facebook face à Instagram</div>
<div class="m a fade" style="--d:.2s;position:absolute;left:80px;top:650px;font-weight:700;font-size:34px">Facebook · 8,4 M</div>
<div class="bar a grow" style="--d:.3s;--du:1.2s;top:706px;width:920px"></div>
<div class="m a fade" style="--d:.9s;position:absolute;left:80px;top:850px;font-weight:700;font-size:34px">Instagram · 895 000</div>
<div class="bar a grow" style="--d:1.0s;--du:1.2s;top:906px;width:{int(920*0.895/8.4)}px;background:{GOLD}"></div>
<div class="pf a rise" style="--d:1.8s;position:absolute;left:80px;top:1030px;font-size:64px;font-weight:700;color:{AUB}">Plus de 9 fois moins.</div><div class="m a fade" style="--d:2.0s;position:absolute;left:80px;top:1140px;font-size:28px;font-weight:600;color:#6d5a66">Audiences publicitaires Meta, fin 2025</div>"""),
    dict(say="Votre client y est déjà. La vraie question : comment y être bien ?", quiet_music=True, html=f"""
<div class="pf a fade" style="--d:.1s;position:absolute;left:70px;top:530px;font-size:260px;line-height:1;color:{GOLD}">«</div>
<div class="quote a wipeup" style="--d:.3s;--du:1s;position:absolute;left:80px;right:80px;top:730px;font-size:96px;line-height:1.1">Votre client y est déjà.</div>
<div class="pf a wipeup" style="--d:1.8s;--du:1s;position:absolute;left:80px;right:80px;top:990px;font-weight:900;font-size:96px;line-height:1.1;color:{AUB}">Comment y être bien ?</div>"""),
    dict(say="Enregistrez ce baromètre, et partagez-le à un entrepreneur.", min=5.0, quiet_music=True, zoom=1.0, html=f"""
<div class="m a fade" style="--d:.1s;position:absolute;left:80px;top:570px;font-size:30px;font-weight:600;color:#6d5a66">Source : DataReportal, Digital 2026 — Côte d'Ivoire</div>
<div class="a pop" style="--d:.6s;position:absolute;left:80px;top:710px">{logo}</div>
<div class="pf a rise" style="--d:.9s;position:absolute;left:230px;top:710px;font-weight:900;font-size:70px">AM.Digital</div>
<div class="m a rise" style="--d:1.1s;position:absolute;left:232px;top:800px;font-size:26px;font-weight:700;letter-spacing:.16em;color:{GOLD}">LE BAROMÈTRE DIGITAL</div>
<div class="a pop" style="--d:1.6s;position:absolute;left:80px;top:950px;border:3px solid {INK};font-family:M;font-weight:800;font-size:40px;padding:22px 34px;color:{INK}">Enregistrez · Partagez</div>
<div class="m a fade" style="--d:2.0s;position:absolute;left:80px;top:1090px;font-size:34px;font-weight:700">WhatsApp +225 01 71 95 45 23</div>"""),
]
spec = dict(name="B_editorial", css=css, sub_css=sub_css, bg=bg, transition="wipe", music=dict(bpm=100, seed=3, gain=.45), scenes=scenes, fx_gain=.35)
if __name__ == "__main__":
    print(m.build(spec, sys.argv[1], work=sys.argv[2] if len(sys.argv) > 2 else None)["total"])
