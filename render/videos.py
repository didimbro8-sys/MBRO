import sys; sys.path.insert(0, "/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/render")
from motion import *
O = sys.argv[1]; which = sys.argv[2]
B = lambda t, s=92, w=800, c=WHITE, g=0: (t, s, w, c, g)
P = lambda t, s=46, w=500, c=SOFT, g=0: (t, s, w, c, g)
V = {
"manifeste": [
  Scene(3.2, "Jour 1 / 31", [B("Pendant *2 ans*, AM.Digital n'a rien publié.", 104)]),
  Scene(4.2, None, [B("Et pendant ce temps, à Abidjan…", 64, 700, SOFT, 40), B("des entreprises publient tous les jours… et *zéro client*.", 88)]),
  Scene(4.0, None, [B("Le problème n'est pas de publier.", 76, 700, SOFT, 32), B("C'est de publier *sans stratégie*.", 100)]),
  Scene(4.6, "Une page doit", [B("1. *Attirer*", 96, 800, WHITE, 18), B("2. *Convaincre*", 96, 800, WHITE, 18), B("3. Donner envie d'*écrire*", 96)]),
  Scene(4.4, "Notre mission", [B("Transformer votre présence en ligne en *clients*.", 96, 800, WHITE, 40), P("Stratégie · Contenus · Publicité · Résultats")]),
  Scene(4.2, "Pendant 30 jours", [B("On partage *tout* ce qu'on sait. Gratuitement.", 92, 800, WHITE, 40), P("Conseils, audits en direct, coulisses.")]),
  Scene(3.6, None, end=True)],
"5-erreurs": [
  Scene(3.0, "AM.Digital · Conseil", [B("5 erreurs qui font *fuir* vos clients", 112)]),
  Scene(4.2, "Erreur 1 / 5", [B("Une bio qui ne dit pas ce que vous *vendez*", 84, 800, WHITE, 36), P("Le visiteur a 3 secondes pour comprendre.")], num=1),
  Scene(4.2, "Erreur 2 / 5", [B("Pas de prix, pas de « à partir de »", 84, 800, WHITE, 36), P("Le client n'ose pas demander. Il va voir ailleurs.")], num=2),
  Scene(4.2, "Erreur 3 / 5", [B("Un numéro WhatsApp *introuvable*", 84, 800, WHITE, 36), P("Chaque clic en plus fait perdre un contact.")], num=3),
  Scene(4.2, "Erreur 4 / 5", [B("Publier seulement quand il y a une *promo*", 84, 800, WHITE, 36), P("Une page vide ne rassure personne.")], num=4),
  Scene(4.2, "Erreur 5 / 5", [B("Des visuels *illisibles* sur téléphone", 84, 800, WHITE, 36), P("Un visuel, un message, deux couleurs.")], num=5),
  Scene(4.0, "Combien sur votre page ?", [B("Écrivez AUDIT en commentaire, on regarde votre page.", 80)], cta="AUDIT"),
  Scene(3.2, None, end=True)],
"parcours-client": [
  Scene(3.2, "AM.Digital · Méthode", [B("On voit votre page… mais on *n'achète pas*", 104)]),
  Scene(3.8, "Étape 1 · Découverte", [B("Une accroche qui *arrête le pouce*", 88, 800, WHITE, 36), P("Parlez de leur problème, pas de vous.")], num=1),
  Scene(3.8, "Étape 2 · Confiance", [B("Des *preuves*", 96, 800, WHITE, 36), P("Avis, photos réelles, régularité, bio claire.")], num=2),
  Scene(3.8, "Étape 3 · Contact", [B("Un WhatsApp *à un clic*", 92, 800, WHITE, 36), P("Et une réponse rapide.")], num=3),
  Scene(3.8, "Étape 4 · Achat", [B("Un prix clair et une *raison d'agir*", 88, 800, WHITE, 36), P("Une date, une offre, un bonus.")], num=4),
  Scene(3.8, "Et vous ?", [B("À quelle étape perdez-vous vos *clients* ?", 88)], cta="1, 2, 3 ou 4 ?"),
  Scene(3.2, None, end=True)],
"30-secondes-1-la-bio": [
  Scene(3.0, "30 secondes de marketing · #1", [B("Votre bio doit dire ce que vous *vendez*", 104)]),
  Scene(4.4, "Ce qu'on voit souvent", [B("« Passionnée de mode | Abidjan | Bienvenue »", 72, 700, SOFT, 36), P("Belle bio. Mais on ne sait pas quoi acheter.", 50, 700, WHITE)]),
  Scene(5.2, "Ce qui fait vendre", [B("Robes en wax sur mesure · *Livraison* à Abidjan · Commandez sur WhatsApp", 70, 800, WHITE)]),
  Scene(4.6, "La règle", [B("*Quoi* · Pour *qui* · *Comment* commander", 86, 800, WHITE, 36), P("Trois infos. Une seule ligne chacune.")]),
  Scene(4.0, "À vous", [B("Collez votre bio en commentaire, on vous la *réécrit*.", 84)]),
  Scene(3.2, None, end=True)],
}
t = render(V[which], f"{O}/AM-Digital_{which}.mp4"); print(which, round(t,1), "s")
