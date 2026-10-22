"""Moteur motion design AM.Digital v4 : vidéos verticales 1080x1920 avec VOIX OFF + fond sonore + sous-titres mot à mot.

Principe (façon After Effects, rendu image par image) :
- chaque scène = une phrase de voix off + un calque HTML animé en CSS ; la durée de la scène suit la voix ;
- le rendu fige toutes les animations à l'instant t (Web Animations API) puis capture l'image (30 i/s) ;
- audio : voix (Kokoro, voix française ff_siwis, ou fichier du fondateur) + musique gen/music.py + whooshs,
  la musique baisse quand la voix parle (sidechain), mixage normalisé à -14 LUFS.

Usage : depuis un script de vidéo, appeler build(spec, sortie_mp4). Voir propositions/video_*.py.
"""
import base64, json, os, pathlib, re, subprocess, sys, tempfile
import numpy as np, soundfile as sf

K = pathlib.Path(__file__).resolve().parent.parent  # racine du kit
sys.path.insert(0, str(K / "gen"))
import music  # noqa: E402

W, H, FPS = 1080, 1920, 30
TTS_DIR = pathlib.Path(os.environ.get("AMD_TTS", pathlib.Path.home() / "tts"))  # kokoro.onnx + voices.bin
FONT_DIR = pathlib.Path(os.environ.get("AMD_FONTS", K / "fonts" / "woff2"))
EXTRA_FONTS = pathlib.Path(os.environ.get("AMD_EXTRA_FONTS", K / "fonts" / "extra"))  # playfair, anton (woff2)


def ff(name, path, w=400, style="normal"):
    return f"@font-face{{font-family:{name};font-weight:{w};font-style:{style};src:url('file://{path}')}}"


def fonts_css():
    css = [ff("M", FONT_DIR / f"montserrat-latin-{w}-normal.woff2", w) for w in (500, 600, 700, 800)]
    for w in (400, 700, 900):
        css.append(ff("PF", EXTRA_FONTS / f"playfair-display-latin-{w}-normal.woff2", w))
    css.append(ff("PF", EXTRA_FONTS / "playfair-display-latin-400-italic.woff2", 400, "italic"))
    css.append(ff("AN", EXTRA_FONTS / "anton-latin-400-normal.woff2", 400))
    return "".join(css)


LOGO = "data:image/png;base64," + base64.b64encode((K / "logo" / "am-digital-logo-carre.png").read_bytes()).decode()

# Bibliothèque d'animations (délai = début de scène --t0 + --d)
ANIM_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;overflow:hidden;background:#000}
.stage{position:absolute;inset:0;overflow:hidden}
.scene{position:absolute;inset:0}
.a{animation-fill-mode:both;animation-timing-function:cubic-bezier(.2,.9,.2,1);animation-delay:calc(var(--t0) + var(--d,0s));animation-duration:var(--du,.7s)}
.rise{animation-name:rise}@keyframes rise{from{opacity:0;transform:translateY(80px)}to{opacity:1;transform:none}}
.drop{animation-name:drop}@keyframes drop{from{opacity:0;transform:translateY(-90px)}to{opacity:1;transform:none}}
.pop{animation-name:pop;animation-timing-function:cubic-bezier(.3,1.6,.4,1)}@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:none}}
.slam{animation-name:slam;animation-timing-function:cubic-bezier(.2,1.4,.3,1)}@keyframes slam{from{opacity:0;transform:scale(2.6)}60%{opacity:1}to{opacity:1;transform:none}}
.fade{animation-name:fade}@keyframes fade{from{opacity:0}to{opacity:1}}
.blurin{animation-name:blurin}@keyframes blurin{from{opacity:0;filter:blur(30px);transform:scale(1.15)}to{opacity:1;filter:none;transform:none}}
.left{animation-name:left}@keyframes left{from{opacity:0;transform:translateX(-140px)}to{opacity:1;transform:none}}
.right{animation-name:right}@keyframes right{from{opacity:0;transform:translateX(140px)}to{opacity:1;transform:none}}
.wipe{animation-name:wipe;animation-timing-function:cubic-bezier(.7,0,.2,1)}@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.wipeup{animation-name:wipeup;animation-timing-function:cubic-bezier(.7,0,.2,1)}@keyframes wipeup{from{clip-path:inset(100% 0 0 0)}to{clip-path:inset(0 0 0 0)}}
.grow{animation-name:grow;transform-origin:left center}@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.growy{animation-name:growy;transform-origin:center bottom}@keyframes growy{from{transform:scaleY(0)}to{transform:scaleY(1)}}
.spin{animation-name:spin;animation-timing-function:linear;animation-iteration-count:infinite}@keyframes spin{to{transform:rotate(360deg)}}
.float{animation-name:float;animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}@keyframes float{from{transform:translateY(-14px)}to{transform:translateY(14px)}}
.strike{animation-name:strike;transform-origin:left center}@keyframes strike{from{transform:scaleX(0) rotate(-4deg)}to{transform:scaleX(1) rotate(-4deg)}}
.reel{display:inline-block;height:1.12em;overflow:hidden;vertical-align:top;line-height:1.12;font-variant-numeric:lining-nums tabular-nums}
.reel>span{display:block;animation-name:reel;animation-timing-function:cubic-bezier(.3,1.2,.4,1)}
@keyframes reel{from{transform:translateY(0)}to{transform:translateY(calc(var(--n) * -1.12em))}}
.reel>span>i{display:block;font-style:normal;height:1.12em}
.word{display:inline-block;animation-name:wordon;animation-duration:.18s;animation-fill-mode:both;animation-delay:calc(var(--t0) + var(--d,0s))}
"""


def reel(digit, d, du=1.2, w=None):
    """Chiffre en rouleau (compteur) qui s'arrête sur `digit` ; `w` = largeur forcée (ex. '.5em' pour un 1)."""
    nums = "".join(f"<i>{(i) % 10}</i>" for i in range(0, 20 + int(digit) + 1))
    n = 20 + int(digit)
    ws = f' style="width:{w};text-align:center"' if w else ""
    return f'<span class="reel"{ws}><span class="a" style="--d:{d}s;--du:{du}s;--n:{n}">{nums}</span></span>'


def tts(text, out, voice="ff_siwis", speed=1.0):
    from kokoro_onnx import Kokoro
    global _K
    try:
        _K
    except NameError:
        _K = Kokoro(str(TTS_DIR / "kokoro.onnx"), str(TTS_DIR / "voices.bin"))
    s, sr = _K.create(text, voice=voice, speed=speed, lang="fr-fr")
    # coupe les silences de début/fin
    a = np.abs(s); idx = np.where(a > 0.01)[0]
    if len(idx): s = s[max(0, idx[0] - 600): idx[-1] + 2400]
    sf.write(out, s, sr)
    return len(s) / sr, sr


def whoosh(sr=44100, dur=0.7, seed=0):
    rng = np.random.default_rng(seed); n = int(sr * dur); x = rng.normal(0, 1, n)
    t = np.linspace(0, 1, n); out = np.zeros(n); seg = 1024
    for i in range(0, n, seg):
        s = x[i:i + seg]; X = np.fft.rfft(s); fr = np.fft.rfftfreq(len(s), 1 / sr)
        c = 400 + 7000 * np.sin(np.pi * t[i]) ** 2; X[fr > c] = 0; X[fr < c * 0.25] *= 0.2
        out[i:i + len(s)] = np.fft.irfft(X, len(s))
    env = np.sin(np.pi * t) ** 3
    return out * env / (np.max(np.abs(out)) + 1e-9) * 0.5


def build(spec, out_mp4, work=None, keep=False):
    """spec = {name, css (style DA), bg (html de fond permanent), sub_css, transition ('blur'|'wipe'|'slide'),
    music:{bpm,seed}, voice:{voice,speed}, scenes:[{say, html, min, impacts:[s], voice_file?}], outro_pad}"""
    work = pathlib.Path(work or tempfile.mkdtemp(prefix="amd_v4_"))
    work.mkdir(parents=True, exist_ok=True)
    vcfg = spec.get("voice", {})
    # 1) voix par scène -> timeline
    t = 0.35; timeline = []
    for i, sc in enumerate(spec["scenes"]):
        if sc.get("say"):
            wav = work / f"v{i:02d}.wav"
            if sc.get("voice_file"):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", sc["voice_file"], "-ac", "1", "-ar", "24000", str(wav)], check=True)
                dur = sf.info(str(wav)).duration
            else:
                dur, _ = tts(sc["say"], str(wav), vcfg.get("voice", "ff_siwis"), vcfg.get("speed", 1.0))
        else:
            wav, dur = None, 0
        lead = sc.get("lead", 0.3)
        sdur = max(sc.get("min", 2.0), lead + dur + sc.get("tail", 0.45))
        timeline.append(dict(i=i, t0=t, dur=sdur, vstart=t + lead, vdur=dur, wav=wav))
        t += sdur
    total = t + spec.get("outro_pad", 0.3)
    json.dump(timeline, open(work / "timeline.json", "w"), default=str, indent=1)

    # 2) HTML
    tr = spec.get("transition", "blur")
    tkf = {
        "blur": ("opacity:0;filter:blur(24px);transform:scale(1.08)", "opacity:0;filter:blur(24px);transform:scale(.94)"),
        "wipe": ("clip-path:inset(0 0 100% 0)", "clip-path:inset(100% 0 0 0)"),
        "slide": ("transform:translateX(100%) skewX(-8deg)", "transform:translateX(-100%) skewX(-8deg)"),
    }[tr]
    scenes_html, kfs = [], []
    for tl, sc in zip(timeline, spec["scenes"]):
        i, t0, d = tl["i"], tl["t0"], tl["dur"]
        tin = min(0.45, d * 0.2) / d * 100; tout = 100 - tin
        first = i == 0; last = i == len(timeline) - 1
        a_from = "opacity:1" if first else tkf[0]
        a_to = "opacity:1" if last else tkf[1]
        kfs.append(f"@keyframes sc{i}{{0%{{{a_from}}}{tin:.2f}%{{opacity:1;filter:none;clip-path:inset(0 0 0 0);transform:none}}"
                   f"{tout:.2f}%{{opacity:1;filter:none;clip-path:inset(0 0 0 0);transform:none}}100%{{{a_to}}}}}"
                   f"@keyframes cam{i}{{from{{transform:scale(1)}}to{{transform:scale({sc.get('zoom', 1.05)})}}}}")
        # sous-titres mot à mot
        words = sc.get("sub", sc.get("say", "")).split()
        subs = ""
        if words and not sc.get("nosub"):
            tot = sum(len(w) + 1 for w in words); acc = 0; spans = []
            for w_ in words:
                dd = tl["vstart"] - t0 + acc / tot * tl["vdur"]; acc += len(w_) + 1
                spans.append(f'<span class="word" style="--d:{dd:.2f}s">{w_}</span>')
            subs = f'<div class="sub">{" ".join(spans)}</div>'
        scenes_html.append(
            f'<div class="scene" style="--t0:{t0:.3f}s;animation:sc{i} {d:.3f}s linear {t0:.3f}s both">'
            f'<div class="scene" style="animation:cam{i} {d:.3f}s linear {t0:.3f}s both">{sc["html"]}</div>{subs}</div>')
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{fonts_css()}{ANIM_CSS}{''.join(kfs)}"
            f"{spec.get('css', '')}{spec.get('sub_css', '')}</style></head><body><div class='stage' style='--t0:0s'>"
            f"{spec.get('bg', '')}{''.join(scenes_html)}{spec.get('overlay', '')}</div></body></html>")
    hp = work / "index.html"; hp.write_text(html, encoding="utf-8")

    # 3) rendu image par image
    from playwright.sync_api import sync_playwright
    vid = work / "video.mp4"
    nfr = int(total * FPS)
    ff_ = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), str(vid)],
                           stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto(f"file://{hp}"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
        for f in range(nfr):
            ms = f * 1000 / FPS
            pg.evaluate(f"document.getAnimations().forEach(a=>{{a.currentTime={ms}}})")
            ff_.stdin.write(pg.screenshot(type="jpeg", quality=92))
        b.close()
    ff_.stdin.close(); ff_.wait()

    # 4) audio : voix assemblée, musique, whooshs
    SRV = 24000
    voice = np.zeros(int(total * SRV) + SRV)
    for tl in timeline:
        if tl["wav"]:
            s, _ = sf.read(str(tl["wav"]))
            i = int(tl["vstart"] * SRV); voice[i:i + len(s)] += s[: len(voice) - i]
    sf.write(work / "voice_raw.wav", voice[: int(total * SRV)], SRV)
    impacts = [tl["t0"] + x for tl, sc in zip(timeline, spec["scenes"]) for x in sc.get("impacts", [])]
    m = spec.get("music", {})
    music.make(total, str(work / "music.wav"), bpm=m.get("bpm", 122), seed=m.get("seed", 0), impacts=impacts)
    quiet = [(tl["t0"], tl["t0"] + tl["dur"] + 1) for tl, sc in zip(timeline, spec["scenes"]) if sc.get("quiet_music")]
    if quiet:  # musique abaissée sur les scènes où la voix doit primer (ex. fin avec le contact)
        mu, msr = sf.read(str(work / "music.wav")); g = np.ones(len(mu))
        for a, b_ in quiet:
            i, j = int(a * msr), min(len(mu), int(b_ * msr)); ramp = min(int(.3 * msr), j - i)
            g[i:j] = 0.4; g[i:i + ramp] = np.linspace(1, .4, ramp)
        sf.write(str(work / "music.wav"), mu * g[:, None], msr)
    SR = 44100; fx = np.zeros((int(total * SR) + SR, 2))
    for k, tl in enumerate(timeline[1:]):
        w_ = whoosh(SR, 0.7, k); i = int(max(0, tl["t0"] - 0.35) * SR); j = min(len(fx), i + len(w_))
        fx[i:j, 0] += w_[: j - i] * (0.8 if k % 2 else 1); fx[i:j, 1] += w_[: j - i] * (1 if k % 2 else 0.8)
    sf.write(work / "fx.wav", fx[: int(total * SR)] * spec.get("fx_gain", 0.55), SR)
    vchain = ("highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=2.5,equalizer=f=10000:t=h:w=0.8:g=1.5,"
              "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,aresample=44100,aformat=channel_layouts=stereo")
    fc = (f"[1:a]{vchain},asplit=2[vo][sc];"
          f"[2:a]volume={m.get('gain', 0.75)}[mu];[3:a]volume=1[fx];[mu][fx]amix=inputs=2:normalize=0[bed];"
          f"[bed][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=400:makeup=1[bd];"
          f"[bd][vo]amix=inputs=2:duration=first:weights=0.5 1:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-i", str(work / "voice_raw.wav"), "-i", str(work / "music.wav"),
                    "-i", str(work / "fx.wav"), "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", str(out_mp4)], check=True)
    return dict(total=total, timeline=timeline, work=str(work))
