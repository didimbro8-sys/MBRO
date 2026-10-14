import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/render")
from motion import *
O="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/medias"
B = lambda t, s=92, w=800, c=WHITE, g=0: (t, s, w, c, g)
P = lambda t, s=46, w=500, c=SOFT, g=0: (t, s, w, c, g)
V={
"16oct_1200_publier-ne-suffit-pas":[
  Scene(3.2,"AM.Digital · Éduquer",[B("Pourquoi *publier* ne suffit pas",108)]),
  Scene(4.2,"Étape 1",[B("*Vue* : on vous remarque",92,800,WHITE,36),P("Un visuel clair, un message simple, au bon moment.")],num=1),
  Scene(4.2,"Étape 2",[B("*Confiance* : on vous croit",92,800,WHITE,36),P("Avis clients, coulisses, réponses rapides, régularité.")],num=2),
  Scene(4.2,"Étape 3",[B("*Action* : on vous écrit",92,800,WHITE,36),P("Un appel à l'action précis : « Écrivez PRIX sur WhatsApp ».")],num=3),
  Scene(4.0,"Et vous ?",[B("Laquelle manque sur *votre page* ?",92)],cta="Commentez"),
  Scene(3.2,None,end=True)],
"18oct_1200_avant-apres":[
  Scene(2.6,"Avant / après",[B("Le même visuel, *deux* résultats",100)]),
  Scene(3.6,"Avant",[B("Prix, promo, adresse, horaires, *4 photos*",86,800,WHITE,36),P("Tout est dit… donc rien n'est retenu.")]),
  Scene(3.6,"Après",[B("*Un* produit. *Un* prix. *Une* action.",92,800,WHITE,36),P("« -20 % ce week-end · Écrivez PROMO »")]),
  Scene(3.2,"La règle",[B("1 visuel = *1 message*",110)],cta="Partagez"),
  Scene(3.0,None,end=True)],
"19oct_1800_repondre-en-1h":[
  Scene(3.0,"30 secondes de marketing",[B("Répondez en moins d'*1 heure*",108)]),
  Scene(4.0,"Pourquoi",[B("Un client qui attend va *ailleurs*.",92,800,WHITE,36),P("Sur WhatsApp et Messenger, il écrit souvent à 3 vendeurs en même temps.")]),
  Scene(4.0,"Astuce 1",[B("Activez les *réponses automatiques*",88,800,WHITE,36),P("« Merci ! On vous répond dans l'heure. » Le client sait qu'il est entendu.")],num=1),
  Scene(4.0,"Astuce 2",[B("Préparez vos *réponses types*",88,800,WHITE,36),P("Prix, livraison, paiement : copiez, personnalisez, envoyez.")],num=2),
  Scene(3.4,"À retenir",[B("La vitesse *vend*.",116)],cta="Enregistrez"),
  Scene(3.0,None,end=True)],
}
for k,s in V.items():
    t=render(s,f"{O}/AM-Digital_{k}.mp4"); print(k,round(t,1),"s")
