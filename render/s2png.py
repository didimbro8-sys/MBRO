import os
from playwright.sync_api import sync_playwright
S="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"; OUT=f"{S}/s2/visuels"
FONT="".join(f"@font-face{{font-family:M;font-weight:{w};src:url('file://{S}/fonts/package/files/montserrat-latin-{w}-normal.woff2')}}" for w in (500,600,700,800))
LOGO=f"file://{S}/ds/project/assets/Logos/am-digital-logo-carre.png"
G=lambda t:f'<span style="color:#f1bc18">{t}</span>'
PX='''<div style="position:absolute;right:200px;top:150px;width:72px;height:72px;background:#f1bc18"></div><div style="position:absolute;right:120px;top:96px;width:36px;height:36px;background:#f1bc18"></div><div style="position:absolute;right:96px;top:250px;width:36px;height:36px;background:#c79613"></div><div style="position:absolute;right:168px;top:300px;width:18px;height:18px;background:#f1bc18"></div>'''
BASE="position:relative;overflow:hidden;box-sizing:border-box;color:#fff;font-family:M,Arial,sans-serif;display:flex;flex-direction:column"
def cover(lab,title,sub,size=116):
    return f'<div style="width:1080px;height:1350px;padding:80px;background:#3c0030;{BASE}"><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div>{PX}<div style="margin-top:auto;font-size:{size}px;line-height:.98;font-weight:800;text-transform:uppercase">{title}</div><div style="margin-top:40px;font-size:38px;font-weight:500;color:#d9c3d2">{sub}</div><div style="position:absolute;left:0;right:0;bottom:0;height:20px;background:#66004a"></div></div>'
def inner(n,tag,title,text):
    return f'<div style="width:1080px;height:1350px;padding:80px;gap:48px;background:#3c0030;{BASE}"><div style="display:flex;justify-content:space-between;align-items:center"><div style="width:132px;height:132px;border-radius:999px;background:#66004a;display:flex;align-items:center;justify-content:center;font-size:64px;font-weight:800;color:#f1bc18">{n}</div><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#d9c3d2">{tag}</div></div><div style="margin-top:auto;font-size:84px;line-height:1.08;font-weight:800">{title}</div><div style="margin-bottom:200px;font-size:44px;line-height:1.4;font-weight:500;color:#d9c3d2">{text}</div><img src="{LOGO}" style="position:absolute;right:80px;bottom:80px;width:120px;height:120px;border-radius:12px"></div>'
def cta(lab,title,text,btn):
    return f'<div style="width:1080px;height:1350px;padding:80px;gap:48px;background:#300024;{BASE}"><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div><div style="position:absolute;right:160px;top:96px;width:48px;height:48px;background:#f1bc18"></div><div style="position:absolute;right:96px;top:168px;width:24px;height:24px;background:#c79613"></div><div style="margin-top:auto;font-size:80px;line-height:1.06;font-weight:800">{title}</div><div style="font-size:40px;line-height:1.4;font-weight:500;color:#d9c3d2">{text}</div><div style="display:flex;align-items:flex-end;justify-content:space-between"><div style="display:flex;flex-direction:column;gap:16px"><div style="align-self:flex-start;background:#f1bc18;color:#300024;font-size:40px;font-weight:800;padding:28px 52px;border-radius:999px">{btn}</div><div style="font-size:28px;font-weight:600;color:#d9c3d2">WhatsApp +225 01 71 95 45 23</div></div><img src="{LOGO}" style="width:150px;height:150px;border-radius:14px"></div></div>'
def vcover(lab,title,sub,size=112):
    return f'<div style="width:1080px;height:1920px;background:#300024;{BASE}"><div style="position:absolute;left:0;top:420px;width:1080px;height:1080px;box-sizing:border-box;padding:80px;display:flex;flex-direction:column;justify-content:center;gap:36px"><div style="font-size:32px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{lab}</div><div style="font-size:{size}px;line-height:.98;font-weight:800;text-transform:uppercase">{title}</div><div style="font-size:40px;font-weight:500;color:#d9c3d2">{sub}</div></div><div style="position:absolute;right:160px;top:500px;width:72px;height:72px;background:#f1bc18"></div><div style="position:absolute;right:96px;top:452px;width:36px;height:36px;background:#f1bc18"></div><div style="position:absolute;right:100px;top:600px;width:36px;height:36px;background:#c79613"></div><div style="position:absolute;left:80px;bottom:300px;display:flex;align-items:center;gap:20px"><img src="{LOGO}" style="width:96px;height:96px;border-radius:10px"><div style="font-size:30px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#d9c3d2">Agence marketing digital · Abidjan</div></div></div>'
def story():
    steps="".join(f'<div style="display:flex;align-items:center;gap:32px;border:3px solid #5a2a4d;border-radius:24px;padding:36px 44px;font-size:44px;font-weight:700"><span style="color:#f1bc18">{n}</span>{t}</div>' for n,t in [("1","Votre activité en une phrase"),("2","Votre objectif digital du mois"),("3","Identifiez un entrepreneur")])
    return f'<div style="width:1080px;height:1920px;padding:260px 80px;gap:40px;background:#300024;{BASE}"><div style="font-size:32px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">Challenge AM.Digital · 24 oct.</div><div style="font-size:120px;line-height:1;font-weight:800">Challenge {G("visibilité")}</div><div style="margin-top:24px;display:flex;flex-direction:column;gap:24px">{steps}</div><div style="margin-top:auto;font-size:38px;font-weight:600;color:#d9c3d2">Les meilleures réponses passent en Story.</div><div style="position:absolute;right:150px;top:150px;width:56px;height:56px;background:#f1bc18"></div><div style="position:absolute;right:88px;top:110px;width:28px;height:28px;background:#c79613"></div></div>'
J={
"05_Carrousel_3-communications_21oct":[
 ("01_couverture",cover("AM.Digital · Comprendre",f"Institutionnelle, d'entreprise, digitale : ne les {G('confondez')} plus","Swipez : 3 communications, 3 missions →",96)),
 ("02",inner(1,"Communication institutionnelle",f"Elle construit la {G('réputation')}","Identité, prises de parole, relations presse, rapport annuel, engagements RSE.")),
 ("03",inner(2,"Communication d'entreprise",f"Elle fait {G('vendre')} et elle fédère","Offres, brochures, salons, événements, communication interne.")),
 ("04",inner(3,"Communication digitale",f"Elle {G('amplifie')} les deux","Réseaux sociaux, site web, vidéo, e-mailing : visibilité, échanges, demandes.")),
 ("05",inner(4,"La règle",f"Un même {G('message')}, trois canaux","Une marque cohérente partout inspire confiance, aux clients comme aux partenaires.")),
 ("06_appel-action",cta("Et vous ?",f"Laquelle manque à votre {G('entreprise')} ?","Répondez 1, 2 ou 3 en commentaire. On vous dit par où commencer.","Répondez 1, 2 ou 3"))],
"06_Carrousel_Nos-offres_25oct":[
 ("01_couverture",cover("AM.Digital · Nos offres",f"Ce qu'AM.Digital fait pour votre {G('entreprise')}","De la réputation aux ventes →",100)),
 ("02",inner(1,"Diagnostic digital",f"Savoir {G('où')} vous en êtes","Analyse de votre présence, 3 à 5 priorités, plan d'action. Le point de départ de tout.")),
 ("03",inner(2,"Communication institutionnelle",f"Une image {G('solide')}","Plateforme de marque, identité visuelle, discours, relations presse, rapport d'activité.")),
 ("04",inner(3,"Communication d'entreprise",f"Des supports qui {G('vendent')}","Brochures, présentations commerciales, communication interne, événements.")),
 ("05",inner(4,"Communication digitale",f"Une présence qui {G('rapporte')}","Ligne éditoriale, contenus, gestion des réseaux, site web, suivi des résultats.")),
 ("06_appel-action",cta("Par où commencer ?",f"Commencez par un {G('diagnostic')}.","Écrivez DIAGNOSTIC sur WhatsApp : on vous répond rapidement.","Écrivez DIAGNOSTIC"))],
"07_Couvertures_videos_semaine2":[
 ("21oct_3-communications",vcover("AM.Digital · Comprendre",f"3 communications, {G('3 missions')}","Institutionnelle, d'entreprise, digitale.",92)),
 ("22oct_3-idees-boutique",vcover("AM.Digital · Idées",f"3 idées pour une {G('boutique')}","À tester cette semaine.")),
 ("23oct_ligne-editoriale",vcover("AM.Digital · Stratégie",f"Avez-vous une {G('ligne éditoriale')} ?","Sinon, voici comment faire.",100)),
 ("24oct_challenge-visibilite",vcover("Challenge AM.Digital",f"Challenge {G('visibilité')}","Participez en commentaire.",120)),
 ("30-secondes-de-marketing-2",vcover("30 secondes de marketing · #2",f"3 appels à l'action qui font {G('écrire')}","Un conseil, 30 secondes.",100))],
"08_Stories_semaine2":[("24oct_challenge",story())]}
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=b.new_page(viewport={"width":1080,"height":1920})
    for d,items in J.items():
        os.makedirs(f"{OUT}/{d}",exist_ok=True)
        for name,html in items:
            tmp=f"{S}/render/tmp.html"; open(tmp,"w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT}body{{margin:0}}</style></head><body>{html}</body></html>")
            pg.goto("file://"+tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(120)
            pre=d.split("_",2)[2] if d.count("_")>=2 else d
            pg.query_selector("body>div").screenshot(path=f"{OUT}/{d}/AM-Digital_{d.split('_',1)[1]}_{name}.png")
    b.close()
print("ok")
