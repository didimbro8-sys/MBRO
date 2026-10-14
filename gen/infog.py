import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/gen")
from lib import *
def chip(t,c="#f1bc18",fg="#300024"): return f'<span style="display:inline-block;background:{c};color:{fg};font-size:20px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:6px 14px;border-radius:999px">{t}</span>'
def card(n,plat,status,title,reco,lab="Notre conseil"):
    return f'''<div style="display:flex;gap:26px;background:#300024;border-radius:22px;padding:28px 30px;align-items:flex-start">
<div style="flex:none;width:92px;height:92px;border-radius:18px;background:#66004a;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:800;color:#f1bc18">{n}</div>
<div style="flex:1;display:flex;flex-direction:column;gap:10px"><div style="display:flex;gap:10px;align-items:center"><span style="font-size:21px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#d9c3d2">{plat}</span>{status}</div>
<div style="font-size:38px;line-height:1.12;font-weight:800">{title}</div>
<div style="font-size:26px;line-height:1.35;font-weight:600;color:#fff"><span style="color:#f1bc18;font-weight:800">{lab} → </span>{reco}</div></div></div>'''
def infog(eyebrow,title,cards,stat,foot,src):
    return f'''<div style="width:1080px;height:1350px;padding:64px 64px 56px;gap:22px;background:#3c0030;{BASE}">
<div style="position:absolute;right:120px;top:70px;width:56px;height:56px;background:#f1bc18"></div><div style="position:absolute;right:68px;top:40px;width:28px;height:28px;background:#f1bc18"></div><div style="position:absolute;right:72px;top:150px;width:28px;height:28px;background:#c79613"></div>
<div style="font-size:23px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">{eyebrow}</div>
<div style="font-size:66px;line-height:1;font-weight:800;text-transform:uppercase;max-width:820px">{title}</div>
<div style="display:flex;flex-direction:column;gap:18px;margin-top:8px">{cards}</div>
<div style="display:flex;gap:18px;align-items:center;margin-top:auto">{stat}</div>
<div style="display:flex;justify-content:space-between;align-items:center;border-top:2px solid #5a2a4d;padding-top:18px"><div style="display:flex;align-items:center;gap:16px"><img src="{LOGO}" style="width:64px;height:64px;border-radius:8px"><div style="font-size:21px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#d9c3d2">{foot}</div></div><div style="font-size:17px;color:#a88aa0;text-align:right;max-width:470px;line-height:1.3">{src}</div></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:14px;background:#66004a"></div></div>'''
OK=chip("Disponible"); TEST=chip("En test","#66004a","#f1bc18"); DEP=chip("En déploiement","#c79613")
STAT=f'<div style="flex:none;font-size:92px;font-weight:800;color:#f1bc18;letter-spacing:-.03em">8,4 M</div><div style="font-size:27px;line-height:1.3;font-weight:600;color:#d9c3d2">d\'utilisateurs de Facebook en Côte d\'Ivoire fin 2025 : <span style="color:#fff">votre client y est.</span></div>'
SRC="Sources : Meta (Advertising Week NY, 6 oct. 2026) · SocialBee, nouveautés Meta et Instagram (oct. 2026) · DataReportal, Digital 2026 Côte d'Ivoire"
pub=infog("La Veille AM.Digital · 15 octobre 2026",f"Ce qui change sur {G('vos réseaux')}",
 card(1,"Meta · Publicité",OK,f"L'IA transforme vos {G('photos')} en vidéos pub","préparez des photos produits nettes, sur fond simple.")+
 card(2,"Instagram · Live",OK,f"Les lives peuvent être {G('boostés')}","un live par semaine, toujours le même jour.")+
 card(3,"Facebook · Engagement",DEP,f"Nouvelle fonction « {G('Créer un défi')} »","lancez un défi simple à votre communauté."),
 STAT,"Chaque jour à 15 h · Abonnez-vous",SRC)
inter=infog("Veille stratégique interne · 14 oct. 2026",f"Nos {G('décisions')} de la semaine",
 card(1,"Contenu",OK,f"Priorité aux {G('Reels')}","Instagram teste un flux qui commence par les Reels : au moins 1 vidéo par jour.","Décision")+
 card(2,"Événements",DEP,f"Challenge du 24 oct. + {G('lives')} 23 et 29 oct.","lancer le défi via « Créer un défi » ; une personne de l'équipe à l'écran en live.","Décision")+
 card(3,"Offre",TEST,f"Nouveau « {G('Pack photos produits')} »","l'IA de Meta transforme les photos en vidéos : la demande en photos propres va monter.","Décision"),
 '<div style="flex:none;font-size:92px;font-weight:800;color:#f1bc18;letter-spacing:-.03em">15 h</div><div style="font-size:27px;line-height:1.3;font-weight:600;color:#d9c3d2">Veille publique quotidienne : <span style="color:#fff">AM.Digital devient la référence qui décrypte le digital pour les entrepreneurs ivoiriens.</span></div>',
 "Document interne · AM.Digital",SRC)
render([("AM-Digital_veille_15oct_infographie",pub)])
import shutil
render([("AM-Digital_veille-interne_14oct_infographie",inter)])
print("ok")
