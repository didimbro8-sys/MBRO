import re,glob,os,sys
from playwright.sync_api import sync_playwright
S="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"
OUT=sys.argv[1]
fonts="".join(f"@font-face{{font-family:'Montserrat';font-weight:{w};src:url('file://{S}/fonts/package/files/montserrat-latin-{w}-normal.woff2') format('woff2')}}" for w in (500,600,700,800))
fonts+="".join(f"@font-face{{font-family:'Montserrat';font-weight:{w};src:url('file://{S}/fonts/package/files/montserrat-latin-ext-{w}-normal.woff2') format('woff2');unicode-range:U+0100-02AF,U+2000-2BFF}}" for w in (500,600,700,800))
logo=f"file://{S}/ds/project/assets/Logos/am-digital-logo-carre.png"
names={"Main":"5-erreurs_01_couverture","Erreurs-2":"5-erreurs_02","Erreurs-3":"5-erreurs_03","Erreurs-4":"5-erreurs_04","Erreurs-5":"5-erreurs_05","Erreurs-6":"5-erreurs_06","Erreurs-7":"5-erreurs_07_appel-action",
"Parcours-1":"parcours-client_01_couverture","Parcours-2":"parcours-client_02","Parcours-3":"parcours-client_03","Parcours-4":"parcours-client_04","Parcours-5":"parcours-client_05","Parcours-6":"parcours-client_06_appel-action",
"Couv-Manifeste":"couverture_14oct_manifeste","Couv-Publier":"couverture_16oct_publier-ne-suffit-pas","Couv-Audit":"couverture_17oct_audit-du-jour-1","Couv-AvantApres":"couverture_18oct_avant-apres","Couv-30s":"couverture_30-secondes-de-marketing-1","Story-Sondage":"story_20oct_sondage"}
with sync_playwright() as p:
  b=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1080,"height":1920})
  for f in sorted(glob.glob(f"{S}/canvas/project/*.dc.html")):
    k=os.path.basename(f)[:-8]; src=open(f).read()
    body=re.search(r"<x-dc>(.*)</x-dc>",src,re.S).group(1)
    body=re.sub(r"<helmet>.*?</helmet>","",body,flags=re.S).replace("/_blob/316e587eab6e94595f3c0213602b543b",logo)
    html=f"<!doctype html><html><head><meta charset='utf-8'><style>{fonts}body{{margin:0}}</style></head><body>{body}</body></html>"
    tmp=f"{S}/render/{k}.html"; open(tmp,"w").write(html)
    pg.goto("file://"+tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
    el=pg.query_selector("body > div")
    # overflow check
    ov=pg.evaluate("""()=>{const r=document.querySelector('body>div');const R=r.getBoundingClientRect();let bad=[];r.querySelectorAll('*').forEach(e=>{const b=e.getBoundingClientRect();if(b.width&&(b.right>R.right+1||b.bottom>R.bottom+1))bad.push(e.textContent.slice(0,30))});return bad}""")
    sub=names[k]; d={"5-e":"01_Carrousel_5-erreurs_15oct","par":"02_Carrousel_Parcours-client_19oct","cou":"03_Couvertures_videos","sto":"04_Stories"}[sub[:3]]
    os.makedirs(f"{OUT}/{d}",exist_ok=True)
    el.screenshot(path=f"{OUT}/{d}/AM-Digital_{sub}.png")
    if ov: print(k,"OVERFLOW",ov)
  b.close()
print("done")
