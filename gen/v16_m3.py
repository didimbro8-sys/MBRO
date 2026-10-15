import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/gen")
import motion3 as M, json
S=M.S
SPEC=[
 {"dur":2.6,"label":"Le Midi Digital","title":"Publier ne *suffit* pas","size":124},
 {"dur":2.8,"big":"3","bigSize":420,"title":"étapes pour *vendre*","size":96},
 {"dur":2.9,"num":"1","label":"Étape 1","title":"La *vue*","size":150,"sub":"Être vu par la bonne personne, au bon moment."},
 {"dur":3.0,"num":"2","label":"Étape 2","title":"La *confiance*","size":124,"sub":"Avis, preuves, régularité : on achète à qui on fait confiance."},
 {"dur":3.0,"num":"3","label":"Étape 3","title":"L'*action*","size":150,"sub":"Un appel clair : écrivez-nous, commandez, réservez."},
 {"dur":3.2,"label":"Et vous ?","title":"Il vous manque *laquelle* ?","size":104,"cta":"Commentez 1, 2 ou 3"},
]
if __name__=="__main__":
    if sys.argv[1:]==["frames"]:
        from playwright.sync_api import sync_playwright
        total=sum(s["dur"] for s in SPEC)
        html=M.HTML.replace("%FONT%",M.FONT).replace("%LOGO%",M.LOGO).replace("%SCENES%",json.dumps(SPEC)).replace("%TOTAL%",str(total)).replace("%ENDDUR%","2.8").replace("%ENDT1%","Abonnez-vous").replace("%ENDT2%","@amdigital204 · Facebook · TikTok")
        open(S+"/chk/m3.html","w").write(html)
        ts=[0.3,1.2,2.3,2.75,3.1,3.6,4.2,5.2,6.0,8.0,8.5,10.5,13.5,15.0,17.0,18.4,19.5]
        with sync_playwright() as p:
            b=p.chromium.launch(args=["--allow-file-access-from-files"]);pg=b.new_page(viewport={"width":1080,"height":1920})
            pg.goto("file://"+S+"/chk/m3.html");pg.evaluate("document.fonts.ready");pg.wait_for_timeout(500)
            for t in ts:
                pg.evaluate(f"render({t})");pg.screenshot(path=f"{S}/chk/f_{t:05.2f}.png")
            b.close()
    else:
        print(M.build(SPEC, S+"/medias/AM-Digital_16oct_1200_publier-ne-suffit-pas_v3.mp4"))
