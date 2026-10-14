"""Petit moteur de motion design AM.Digital : texte cinétique vertical 1080x1920, rendu en MP4 via ffmpeg."""
import math, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

S = "/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"
W, H, FPS = 1080, 1920, 30
BG = (48, 0, 36)          # aubergine-900
CARD = (60, 0, 48)        # aubergine-800
VIOLET = (102, 0, 74)     # violet-600
OR4 = (241, 188, 24)      # or-400
OR5 = (199, 150, 19)      # or-500
WHITE = (255, 255, 255)
SOFT = (217, 195, 210)    # texte-doux
LINE = (90, 42, 77)
_fonts = {}
def font(size, w=800):
    k = (size, w)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(f"{S}/fonts/Montserrat-{w}.ttf", size)
    return _fonts[k]

LOGO = Image.open(f"{S}/ds/project/assets/Logos/am-digital-logo-carre.png").convert("RGBA")

def ease_out(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def ease_in_out(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def rich_lines(text, f, maxw, color):
    """Texte avec *mots en or* -> lignes ; chaque mot = [(morceau, couleur)] pour coller la ponctuation."""
    gold = False; words = []; cur = []; buf = ""
    def flush_piece():
        nonlocal buf
        if buf: cur.append((buf, OR4 if gold else color)); buf = ""
    for ch in text:
        if ch == "*":
            flush_piece(); gold = not gold
        elif ch == " ":
            flush_piece()
            if cur: words.append(cur); cur = []
        else:
            buf += ch
    flush_piece()
    if cur: words.append(cur)
    wl = lambda w: sum(f.getlength(t) for t, _ in w)
    lines, line, lw = [], [], 0; sp = f.getlength(" ")
    for w in words:
        ww = wl(w)
        if line and lw + sp + ww > maxw:
            lines.append(line); line, lw = [], 0
        lw = lw + (sp if line else 0) + ww; line.append(w)
    if line: lines.append(line)
    return lines

def line_img(line, f):
    if line and isinstance(line[0], tuple): line = [[p] for p in line]
    sp = f.getlength(" ")
    wtot = int(sum(sum(f.getlength(t) for t, _ in w) for w in line) + sp * (len(line) - 1)) + 4
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (max(wtot, 1), asc + desc + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); x = 0
    for w in line:
        for t, c in w:
            d.text((x, 0), t, font=f, fill=c); x += f.getlength(t)
        x += sp
    return im

def spaced(text, f, color, tracking):
    asc, desc = f.getmetrics()
    wtot = int(sum(f.getlength(ch) + tracking for ch in text)) + 4
    im = Image.new("RGBA", (wtot, asc + desc + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 0
    for ch in text:
        d.text((x, 0), ch, font=f, fill=color); x += f.getlength(ch) + tracking
    return im

def with_alpha(im, a):
    if a >= 0.999: return im
    r = im.copy(); al = r.getchannel("A").point(lambda v: int(v * a)); r.putalpha(al); return r

class Scene:
    """Une scène : étiquette, blocs de texte qui entrent en décalé, éléments optionnels."""
    def __init__(self, dur, label=None, blocks=(), num=None, cta=None, end=False, center=True):
        self.dur, self.label, self.num, self.cta, self.end, self.center = dur, label, num, cta, end, center
        self.items = []  # (image, y_offset_in_block, delay)
        y = 0; delay = 0.15
        if num is not None:
            c = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
            d.ellipse((0, 0, 149, 149), fill=VIOLET)
            f = font(76); tw = f.getlength(str(num)); asc, desc = f.getmetrics()
            d.text(((150 - tw) / 2, (150 - asc - desc) / 2 + 4), str(num), font=f, fill=OR4)
            self.items.append((c, y, delay)); y += 150 + 56; delay += 0.12
        for text, size, weight, color, gap in blocks:
            f = font(size, weight)
            lh = int(size * (1.08 if weight >= 700 else 1.4))
            for ln in rich_lines(text, f, 920, color):
                self.items.append((line_img(ln, f), y, delay)); y += lh; delay += 0.09
            y += gap; delay += 0.1
        if cta:
            f = font(46, 800); tw = int(f.getlength(cta)); asc, desc = f.getmetrics()
            pill = Image.new("RGBA", (tw + 112, asc + desc + 64), (0, 0, 0, 0)); d = ImageDraw.Draw(pill)
            d.rounded_rectangle((0, 0, pill.width - 1, pill.height - 1), radius=pill.height // 2, fill=OR4)
            d.text((56, 30), cta, font=f, fill=BG)
            y += 24; self.items.append((pill, y, delay + 0.1)); y += pill.height
        self.height = y
        self.label_img = spaced(label.upper(), font(32, 700), OR4, 5) if label else None

    def draw(self, frame, t):
        out_t = self.dur - t
        exit_a = ease_in_out(out_t / 0.35) if out_t < 0.35 else 1.0
        exit_dy = (1 - exit_a) * -60
        if self.end:
            return draw_end(frame, t)
        top = (420 + (1080 - self.height) // 2) if self.center else 460
        if self.label_img is not None:
            a = ease_out(t / 0.4) * exit_a
            frame.alpha_composite(with_alpha(self.label_img, a), (80, int(top - 110 + exit_dy)))
        for im, yo, delay in self.items:
            p = ease_out((t - delay) / 0.5)
            if p <= 0: continue
            dy = (1 - p) * 70 + exit_dy
            frame.alpha_composite(with_alpha(im, p * exit_a), (80, int(top + yo + dy)))

def draw_pixels(frame, gt):
    d = ImageDraw.Draw(frame)
    sq = [(200, 230, 72, OR4, 0.0), (128, 178, 36, OR4, 0.8), (132, 340, 36, OR5, 1.6), (248, 362, 18, OR4, 2.2), (96, 280, 18, OR4, 3.1)]
    for rx, y, s, c, ph in sq:
        dy = math.sin(gt * 1.4 + ph) * 10; dx = math.cos(gt * 1.1 + ph) * 6
        x = W - rx - s + dx; d.rectangle((x, y + dy, x + s, y + s + dy), fill=c)

def draw_footer(frame, gt, total):
    lg = LOGO.resize((96, 96)); frame.alpha_composite(lg, (80, 1560))
    frame.alpha_composite(spaced("AGENCE MARKETING DIGITAL · ABIDJAN", font(28, 700), SOFT, 3), (196, 1592))
    d = ImageDraw.Draw(frame)
    d.rectangle((0, H - 10, W, H), fill=LINE)
    d.rectangle((0, H - 10, int(W * min(1, gt / total)), H), fill=OR4)

def draw_end(frame, t):
    p = ease_out(t / 0.6); s = int(360 + 40 * p)
    lg = with_alpha(LOGO.resize((s, s)), p); frame.alpha_composite(lg, ((W - s) // 2, 560 - (s - 360) // 2))
    for i, (txt, f, c, y) in enumerate([("Abonnez-vous", font(64, 800), WHITE, 1010), ("pour la suite de la série", font(40, 500), SOFT, 1094),
                                        ("WhatsApp +225 01 71 95 45 23", font(40, 700), OR4, 1210)]):
        q = ease_out((t - 0.3 - i * 0.15) / 0.5)
        if q <= 0: continue
        im = line_img([(txt, c)], f); frame.alpha_composite(with_alpha(im, q), ((W - im.width) // 2, int(y + (1 - q) * 40)))

def render(scenes, out, end_footer=False):
    total = sum(s.dur for s in scenes); n = int(total * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    base = Image.new("RGBA", (W, H), BG + (255,))
    for i in range(n):
        gt = i / FPS; acc = 0
        for sc in scenes:
            if gt < acc + sc.dur: break
            acc += sc.dur
        fr = base.copy()
        if not sc.end: draw_pixels(fr, gt)
        sc.draw(fr, gt - acc)
        if not sc.end: draw_footer(fr, gt, total)
        else:
            d = ImageDraw.Draw(fr); d.rectangle((0, H - 10, W, H), fill=OR4)
        pr.stdin.write(fr.convert("RGB").tobytes())
    pr.stdin.close(); pr.wait()
    return total
