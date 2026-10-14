import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/gen")
from lib import *
def card(n,tag,title,dec,act,src):
    return f'''<div style="display:flex;gap:22px;background:#300024;border-radius:20px;padding:18px 24px;align-items:flex-start">
<div style="flex:none;width:64px;height:64px;border-radius:14px;background:#66004a;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:800;color:#f1bc18">{n}</div>
<div style="flex:1;display:flex;flex-direction:column;gap:5px">
<div style="font-size:16px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#d9c3d2">{tag}</div>
<div style="font-size:28px;line-height:1.1;font-weight:800">{title}</div>
<div style="font-size:19.5px;line-height:1.33;font-weight:500;color:#d9c3d2"><span style="color:#fff;font-weight:700">Décryptage · </span>{dec}</div>
<div style="font-size:19.5px;line-height:1.33;font-weight:600;color:#fff"><span style="color:#f1bc18;font-weight:800">Décision pour votre entreprise · </span>{act}</div>
<div style="font-size:14px;color:#a88aa0">Source : {src}</div></div></div>'''
def infog(eyebrow,title,sub,cards,foot):
    return f'''<div style="width:1080px;height:1350px;padding:52px 60px 40px;gap:14px;background:#3c0030;{BASE}">
<div style="position:absolute;right:120px;top:56px;width:52px;height:52px;background:#f1bc18"></div><div style="position:absolute;right:70px;top:30px;width:26px;height:26px;background:#f1bc18"></div><div style="position:absolute;right:72px;top:124px;width:26px;height:26px;background:#c79613"></div>
<div style="font-size:21px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{eyebrow}</div>
<div style="font-size:58px;line-height:1;font-weight:800;text-transform:uppercase;max-width:860px">{title}</div>
<div style="font-size:25px;font-weight:600;color:#d9c3d2;margin-bottom:6px">{sub}</div>
<div style="display:flex;flex-direction:column;gap:12px">{cards}</div>
<div style="margin-top:auto;display:flex;justify-content:space-between;align-items:center;border-top:2px solid #5a2a4d;padding-top:14px;margin-bottom:8px"><div style="display:flex;align-items:center;gap:16px"><img src="{LOGO}" style="width:60px;height:60px;border-radius:8px"><div style="font-size:20px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#d9c3d2">{foot}</div></div><div style="background:#f1bc18;color:#300024;font-size:22px;font-weight:800;padding:12px 26px;border-radius:999px">Enregistrez · Partagez</div></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:12px;background:#66004a"></div></div>'''
C=(card(1,"Tendance · Recherche & IA",f"Google répond désormais {G('à la place des sites')}",
  "les résumés IA de Google s'affichent sur plus de 80 % des recherches de marque fin septembre (26 % début septembre).",
  "soignez votre fiche Google et publiez des réponses claires aux questions clients (FAQ).",
  "Search Engine Land, données DemandSphere, 30 sept.–5 oct. 2026")+
 card(2,"Tendance · IA & commerce",f"Les IA recommandent d'abord les {G('grandes enseignes')}",
  "sans recherche web, ChatGPT et Gemini citent les grandes chaînes 63 à 70 % du temps, les indépendants environ 10 %.",
  "affichez « entreprise indépendante à Abidjan » partout (bio, site, fiche Google) et collectez des avis.",
  "étude Vaer AI pour Lightspeed Commerce, via Search Engine Land, oct. 2026")+
 card(3,"Tendance · Qualité des contenus",f"Google exige une {G('relecture humaine')} des contenus IA",
  "Google juge « critique » de vérifier manuellement tout contenu généré par IA avant de le publier.",
  "l'IA rédige, l'humain vérifie : chiffres, noms, prix, promesses.",
  "Google Search Central, guide sur les contenus générés par IA, oct. 2026")+
 card(4,"Outils IA du jour · Création",f"Vos photos deviennent des {G('vidéos pub')}",
  "Meta crée des vidéos pub à partir de vos visuels fixes (6 oct.) ; Adobe crée et retouche vos visuels dans ChatGPT (1er oct.).",
  "produisez plus vite, mais gardez votre charte : couleurs, logo, ton.",
  "Meta, Advertising Week New York, 6 oct. 2026 · MarTech, 1er oct. 2026"))
pub=infog("Veille AM.Digital · 15 octobre 2026",f"Quand l'IA décide {G('qui on voit')}","Tendances mondiales com & marketing, décryptées pour les pros et les PME",C,"La veille AM.Digital · chaque jour à 15 h")
render([("AM-Digital_veille_15oct_infographie-v2",pub)]); print("ok")
