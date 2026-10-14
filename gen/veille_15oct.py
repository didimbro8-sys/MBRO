import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/gen")
from lib import *
def news(n,tag,title,fact,reco,src):
    return f'<div style="width:1080px;height:1350px;padding:80px;gap:30px;background:#3c0030;{BASE}"><div style="display:flex;justify-content:space-between;align-items:center"><div style="width:120px;height:120px;border-radius:999px;background:#66004a;display:flex;align-items:center;justify-content:center;font-size:58px;font-weight:800;color:#f1bc18">{n}</div><div style="font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#d9c3d2">{tag}</div></div><div style="margin-top:40px;font-size:66px;line-height:1.08;font-weight:800">{title}</div><div style="font-size:36px;line-height:1.4;font-weight:500;color:#d9c3d2">{fact}</div><div style="margin-top:auto;background:#300024;border-left:10px solid #f1bc18;border-radius:14px;padding:34px 38px"><div style="font-size:24px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18">Notre recommandation</div><div style="margin-top:14px;font-size:36px;line-height:1.38;font-weight:600">{reco}</div></div><div style="font-size:22px;color:#a88aa0">{src}</div></div>'
I=[
("AM-Digital_veille_15oct_01_couverture", cover("La Veille AM.Digital · 15 octobre 2026",f"Ce qui change cette semaine sur {G('vos réseaux')}","3 nouveautés, 3 recommandations pour votre entreprise →",96)),
("AM-Digital_veille_15oct_02", news(1,"Meta · Publicité",f"L'IA de Meta transforme vos {G('photos en vidéos')}",
 "Annoncé le 6 octobre : dans les publicités Meta, l'IA peut créer une vidéo à partir de vos visuels fixes. Un paiement direct dans Messenger est aussi en test.",
 "Préparez dès maintenant des photos produits nettes, sur fond simple. Ce sont elles qui nourriront vos futures vidéos.","Source : Meta, Advertising Week New York, 6 oct. 2026")),
("AM-Digital_veille_15oct_03", news(2,"Instagram · Live",f"Les lives Instagram peuvent être {G('boostés')}",
 "Instagram permet désormais de promouvoir un live, comme une publication. Le direct devient un format à part entière pour toucher de nouveaux clients.",
 "Faites un live par semaine, toujours le même jour : présentation produit, questions-réponses, coulisses. La régularité crée le rendez-vous.","Source : récapitulatif des nouveautés Instagram, octobre 2026 (SocialBee)")),
("AM-Digital_veille_15oct_04", news(3,"Facebook · Engagement",f"Facebook lance « {G('Créer un défi')} »",
 "Une fonction pour lancer des défis est en déploiement sur iPhone, avec un nouveau format de Story « Canvas ».",
 "Un défi simple fait participer votre communauté : « Montrez-nous comment vous portez notre produit ». On teste avec notre Challenge visibilité du 24 octobre.","Source : récapitulatif des nouveautés Meta, octobre 2026 (SocialBee)")),
("AM-Digital_veille_15oct_05_appel-action", cta("La Veille AM.Digital · chaque jour à 15 h",f"Ne ratez plus ce qui {G('change')}.","Abonnez-vous et enregistrez ce post. Une question sur une nouveauté ? Posez-la en commentaire.","Abonnez-vous")),
]
render(I); print("ok")
