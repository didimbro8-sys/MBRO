import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/gen")
from motion2 import build
S="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"
V={
"mo_ligne-editoriale":[
 {"dur":2.4,"label":"Le mot du jour","title":"Ligne *éditoriale*","size":124},
 {"dur":3.0,"num":"1","label":"Ce que vous racontez","title":"Vos *sujets*, pas vos humeurs","size":90,"wipe":True},
 {"dur":3.0,"num":"2","label":"À qui, comment","title":"Un *client* précis, un ton constant","size":86},
 {"dur":3.0,"num":"3","label":"À quel rythme","title":"Publier *régulièrement*, pas au hasard","size":86,"cta":"Écrivez LIGNE en commentaire"}],
"mo_quel-reseau":[
 {"dur":2.4,"label":"Le bon réseau","title":"Où est votre *client* ?","size":120},
 {"dur":2.2,"label":"Facebook","title":"Toucher *large*","size":120,"wipe":True},
 {"dur":2.2,"label":"TikTok","title":"Être *découvert*","size":120},
 {"dur":2.2,"label":"Instagram","title":"Soigner la *vitrine*","size":112},
 {"dur":2.2,"label":"WhatsApp","title":"*Vendre* et fidéliser","size":112},
 {"dur":2.6,"label":"La règle","title":"Le meilleur réseau est celui où votre *client* vous attend","size":78,"cta":"Enregistrez"}],
"mo_3-secondes":[
 {"dur":2.4,"label":"Le chiffre du jour","big":"3 s","bigSize":360,"title":"pour être *jugé*","size":90},
 {"dur":2.8,"num":"1","label":"Photo de profil","title":"*Nette* et reconnaissable","size":96,"wipe":True},
 {"dur":2.8,"num":"2","label":"Nom de page","title":"Ce que vous *faites*, en clair","size":90},
 {"dur":3.0,"num":"3","label":"Bio","title":"Une *promesse* + un contact","size":92,"cta":"Vérifiez votre profil"}],
"mo_plateforme-marque":[
 {"dur":2.6,"label":"Communication institutionnelle","title":"La *plateforme* de marque","size":112},
 {"dur":2.6,"label":"Étage 1","title":"*Mission* : pourquoi vous existez","size":90,"wipe":True},
 {"dur":2.6,"label":"Étage 2","title":"*Valeurs* : ce qui ne se négocie pas","size":86},
 {"dur":2.6,"label":"Étage 3","title":"*Messages* clés : ce que tout le monde répète","size":82},
 {"dur":2.8,"label":"Résultat","title":"Écrite *une fois*, elle guide tous vos supports","size":84,"cta":"Demandez conseil"}],
"mo_persona":[
 {"dur":2.4,"label":"Le mot du jour","title":"*Persona*","size":150},
 {"dur":2.8,"label":"Définition","title":"Le portrait de votre *client idéal*","size":92,"wipe":True},
 {"dur":3.0,"label":"Il a","title":"un âge, un *métier*, un *problème*","size":92},
 {"dur":3.0,"label":"La règle","title":"On ne parle pas à « *tout le monde* »","size":92,"cta":"Enregistrez"}],
"mo_interne-externe":[
 {"dur":2.6,"label":"Communication interne","title":"Vos équipes sont-elles *au courant* ?","size":96},
 {"dur":2.6,"big":"1","bigSize":320,"title":"seule *histoire*, dedans et dehors","size":84,"wipe":True},
 {"dur":3.0,"label":"Pourquoi","title":"Vos employés sont vos *premiers* ambassadeurs","size":84},
 {"dur":2.8,"label":"À faire","title":"Annoncez *d'abord* en interne, puis en ligne","size":84,"cta":"Commentez"}],
}
only=sys.argv[1:] or list(V)
for k in only:
    print(build(V[k], f"{S}/medias/AM-Digital_{k}.mp4", enddur=2.2), flush=True)
