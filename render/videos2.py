import sys; sys.path.insert(0, "/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/render")
from motion import *
O = sys.argv[1]; which = sys.argv[2]
B = lambda t, s=92, w=800, c=WHITE, g=0: (t, s, w, c, g)
P = lambda t, s=46, w=500, c=SOFT, g=0: (t, s, w, c, g)
V = {
"3-communications": [
  Scene(3.4, "AM.Digital · Comprendre", [B("Institutionnelle, d'entreprise, digitale : *3 communications*, 3 missions", 92)]),
  Scene(4.6, "Communication institutionnelle", [B("Elle construit la *réputation*.", 92, 800, WHITE, 36), P("Qui vous êtes, ce que vous défendez : identité, relations presse, rapport annuel, engagements RSE.")], num=1),
  Scene(4.6, "Communication d'entreprise", [B("Elle fait *vendre* et elle fédère.", 92, 800, WHITE, 36), P("Offres, brochures, salons, communication interne : clients et équipes avancent dans le même sens.")], num=2),
  Scene(4.6, "Communication digitale", [B("Elle *amplifie* les deux.", 92, 800, WHITE, 36), P("Réseaux sociaux, site web, vidéo, e-mailing : plus de visibilité, plus d'échanges, plus de demandes.")], num=3),
  Scene(4.2, "La règle", [B("Un même *message*, trois canaux.", 96, 800, WHITE, 36), P("Une marque cohérente partout inspire confiance.")]),
  Scene(4.0, "Et vous ?", [B("Laquelle manque à votre *entreprise* ?", 88)], cta="1, 2 ou 3 ?"),
  Scene(3.2, None, end=True)],
"3-idees-boutique": [
  Scene(3.0, "AM.Digital · Idées", [B("3 idées de contenu pour une *boutique*", 104)]),
  Scene(4.4, "Idée 1", [B("Le produit *porté*, pas posé", 92, 800, WHITE, 36), P("10 secondes sur un client valent mieux que 10 photos sur une table.")], num=1),
  Scene(4.4, "Idée 2", [B("La *preuve* en image", 92, 800, WHITE, 36), P("Un avis client, une livraison en cours, un client satisfait (avec son accord).")], num=2),
  Scene(4.4, "Idée 3", [B("La commande en *3 étapes*", 92, 800, WHITE, 36), P("Message, paiement, livraison : montrez que c'est simple.")], num=3),
  Scene(3.8, "À vous", [B("Identifiez un commerçant qui doit *voir ça*.", 88)]),
  Scene(3.2, None, end=True)],
"ligne-editoriale": [
  Scene(3.4, "AM.Digital · Stratégie", [B("Votre entreprise a-t-elle une *ligne éditoriale* ?", 100)]),
  Scene(4.2, "Sans ligne éditoriale", [B("Des posts au hasard, un message *flou*.", 88, 800, WHITE, 36), P("On publie quand on a le temps, et personne ne retient rien.")]),
  Scene(4.4, "Avec une ligne éditoriale", [B("3 à 5 *piliers* qui reviennent chaque semaine.", 88)]),
  Scene(5.0, "Exemple de répartition", [B("30 % · *Éduquer*", 80, 800, WHITE, 14), B("25 % · *Prouver*", 80, 800, WHITE, 14), B("20 % · *Montrer les coulisses*", 80, 800, WHITE, 14), B("15 % · *Rassurer*", 80, 800, WHITE, 14), B("10 % · *Vendre*", 80)]),
  Scene(4.0, "Le résultat", [B("Un message *clair*, des abonnés qui reviennent, des clients qui écrivent.", 80)]),
  Scene(4.0, "À vous", [B("Écrivez LIGNE en commentaire, on vous envoie un *modèle*.", 84)], cta="LIGNE"),
  Scene(3.2, None, end=True)],
"challenge-visibilite": [
  Scene(3.4, "Challenge AM.Digital", [B("Challenge *visibilité*", 120)]),
  Scene(3.8, "Étape 1", [B("Présentez votre activité en *une phrase*", 92)], num=1),
  Scene(3.8, "Étape 2", [B("Ajoutez votre *objectif digital* du mois", 92)], num=2),
  Scene(3.8, "Étape 3", [B("Identifiez un entrepreneur qui doit *participer*", 88)], num=3),
  Scene(4.0, "La récompense", [B("Les *meilleures réponses* passent en Story chez AM.Digital.", 84)], cta="Je participe"),
  Scene(3.2, None, end=True)],
"30-secondes-2-appels-action": [
  Scene(3.0, "30 secondes de marketing · #2", [B("3 appels à l'action qui font *écrire*", 100)]),
  Scene(4.2, "Pour une boutique", [B("« Écrivez *TAILLE* pour connaître la disponibilité »", 80)], num=1),
  Scene(4.2, "Pour un service", [B("« Réservez avant *vendredi* : 5 places cette semaine »", 80)], num=2),
  Scene(4.2, "Pour un devis", [B("« Envoyez *PRIX* sur WhatsApp, réponse en 1 heure »", 80)], num=3),
  Scene(4.0, "La règle", [B("Un post, *une* action. Simple, précise, immédiate.", 84)]),
  Scene(3.2, None, end=True)],
}
t = render(V[which], f"{O}/AM-Digital_{which}.mp4"); print(which, round(t, 1), "s")
