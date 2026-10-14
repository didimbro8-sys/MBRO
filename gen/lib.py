import os, sys
from playwright.sync_api import sync_playwright
S="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"
sys.path.insert(0,S+"/render")
OUT=S+"/medias"
FONT="".join(f"@font-face{{font-family:M;font-weight:{w};src:url('file://{S}/fonts/package/files/montserrat-latin-{w}-normal.woff2')}}" for w in (500,600,700,800))
LOGO=f"file://{S}/ds/project/assets/Logos/am-digital-logo-carre.png"
G=lambda t:f'<span style="color:#f1bc18">{t}</span>'
BASE="position:relative;overflow:hidden;box-sizing:border-box;color:#fff;font-family:M,Arial,sans-serif;display:flex;flex-direction:column"
PX='''<div style="position:absolute;right:200px;top:150px;width:72px;height:72px;background:#f1bc18"></div><div style="position:absolute;right:120px;top:96px;width:36px;height:36px;background:#f1bc18"></div><div style="position:absolute;right:96px;top:250px;width:36px;height:36px;background:#c79613"></div><div style="position:absolute;right:168px;top:300px;width:18px;height:18px;background:#f1bc18"></div>'''
SIGN=f'<div style="margin-top:56px;display:flex;align-items:center;gap:20px"><img src="{LOGO}" style="width:88px;height:88px;border-radius:10px"><div style="font-size:26px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#d9c3d2">Agence marketing digital · Abidjan</div></div>'
BAR='<div style="position:absolute;left:0;right:0;bottom:0;height:20px;background:#66004a"></div>'
def post(lab,title,sub,size=108,deco=PX,extra=""):
    return f'<div style="width:1080px;height:1350px;padding:80px;background:#3c0030;{BASE}"><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div>{deco}{extra}<div style="margin-top:auto;font-size:{size}px;line-height:.98;font-weight:800;text-transform:uppercase">{title}</div><div style="margin-top:40px;font-size:40px;line-height:1.3;font-weight:600;color:#d9c3d2">{sub}</div>{SIGN}{BAR}</div>'
def big(lab,num,title,sub,src=""):
    return f'<div style="width:1080px;height:1350px;padding:80px;background:#3c0030;{BASE}"><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div>{PX}<div style="margin-top:auto;font-size:230px;line-height:.9;font-weight:800;color:#f1bc18;letter-spacing:-.03em">{num}</div><div style="margin-top:30px;font-size:64px;line-height:1.05;font-weight:800;text-transform:uppercase">{title}</div><div style="margin-top:32px;font-size:36px;line-height:1.35;font-weight:500;color:#d9c3d2">{sub}</div><div style="margin-top:20px;font-size:22px;color:#a88aa0">{src}</div>{SIGN}{BAR}</div>'
def quote(lab,text,author):
    return f'<div style="width:1080px;height:1350px;padding:80px;background:#300024;{BASE}"><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div><div style="margin-top:60px;font-size:300px;line-height:.6;font-weight:800;color:#66004a">“</div><div style="margin-top:auto;font-size:72px;line-height:1.12;font-weight:800">{text}</div><div style="margin-top:40px;font-size:34px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#f1bc18">{author}</div>{SIGN}{BAR}</div>'
def cover(lab,title,sub,size=110):
    return f'<div style="width:1080px;height:1350px;padding:80px;background:#3c0030;{BASE}"><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div>{PX}<div style="margin-top:auto;font-size:{size}px;line-height:.98;font-weight:800;text-transform:uppercase">{title}</div><div style="margin-top:40px;font-size:38px;font-weight:500;color:#d9c3d2">{sub}</div>{BAR}</div>'
def inner(n,tag,title,text):
    return f'<div style="width:1080px;height:1350px;padding:80px;gap:48px;background:#3c0030;{BASE}"><div style="display:flex;justify-content:space-between;align-items:center"><div style="width:132px;height:132px;border-radius:999px;background:#66004a;display:flex;align-items:center;justify-content:center;font-size:64px;font-weight:800;color:#f1bc18">{n}</div><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#d9c3d2">{tag}</div></div><div style="margin-top:auto;font-size:80px;line-height:1.08;font-weight:800">{title}</div><div style="margin-bottom:200px;font-size:42px;line-height:1.4;font-weight:500;color:#d9c3d2">{text}</div><img src="{LOGO}" style="position:absolute;right:80px;bottom:80px;width:120px;height:120px;border-radius:12px"></div>'
def cta(lab,title,text,btn):
    return f'<div style="width:1080px;height:1350px;padding:80px;gap:48px;background:#300024;{BASE}"><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div><div style="position:absolute;right:160px;top:96px;width:48px;height:48px;background:#f1bc18"></div><div style="position:absolute;right:96px;top:168px;width:24px;height:24px;background:#c79613"></div><div style="margin-top:auto;font-size:78px;line-height:1.06;font-weight:800">{title}</div><div style="font-size:40px;line-height:1.4;font-weight:500;color:#d9c3d2">{text}</div><div style="display:flex;align-items:flex-end;justify-content:space-between"><div style="display:flex;flex-direction:column;gap:16px"><div style="align-self:flex-start;background:#f1bc18;color:#300024;font-size:40px;font-weight:800;padding:28px 52px;border-radius:999px">{btn}</div><div style="font-size:28px;font-weight:600;color:#d9c3d2">WhatsApp +225 01 71 95 45 23</div></div><img src="{LOGO}" style="width:150px;height:150px;border-radius:14px"></div></div>'
def story(lab,title,lines,foot,size=110):
    rows="".join(f'<div style="display:flex;align-items:center;gap:32px;border:3px solid #5a2a4d;border-radius:24px;padding:36px 44px;font-size:44px;font-weight:700"><span style="color:#f1bc18">{n}</span>{t}</div>' for n,t in lines)
    return f'<div style="width:1080px;height:1920px;padding:260px 80px;gap:40px;background:#300024;{BASE}"><div style="font-size:32px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div><div style="font-size:{size}px;line-height:1;font-weight:800">{title}</div><div style="margin-top:24px;display:flex;flex-direction:column;gap:24px">{rows}</div><div style="margin-top:auto;font-size:38px;font-weight:600;color:#d9c3d2">{foot}</div><div style="position:absolute;right:150px;top:150px;width:56px;height:56px;background:#f1bc18"></div><div style="position:absolute;right:88px;top:110px;width:28px;height:28px;background:#c79613"></div><img src="{LOGO}" style="position:absolute;left:80px;bottom:120px;width:96px;height:96px;border-radius:10px"></div>'
def render(items):
    """items: list of (filename_without_ext, html)"""
    from PIL import Image
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1080,"height":1920})
        for name,html in items:
            tmp=f"{S}/gen/tmp.html"; open(tmp,"w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT}body{{margin:0}}</style></head><body>{html}</body></html>")
            pg.goto("file://"+tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(120)
            png=f"{S}/gen/{name}.png"; pg.query_selector("body>div").screenshot(path=png)
            Image.open(png).convert("RGB").save(f"{OUT}/{name}.jpg",quality=90,optimize=True)
        b.close()
