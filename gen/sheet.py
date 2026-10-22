"""Planche de contrôle : extrait une image au milieu (et à 80 %) de chaque scène d'une vidéo motion4 et les assemble."""
import json, subprocess, sys, pathlib
from PIL import Image
vid, work, out = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
tl = json.load(open(work / "timeline.json"))
ims = []
for s in tl:
    for frac in (0.45, 0.85):
        t = s["t0"] + s["dur"] * frac; p = work / f"chk_{s['i']}_{int(frac*100)}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", vid, "-frames:v", "1", "-q:v", "3", str(p)], check=True)
        ims.append(Image.open(p).resize((270, 480)))
cols = 7; rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 280, rows * 490), "white")
for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 280 + 5, (k // cols) * 490 + 5))
sheet.save(out); print(out, len(ims))
