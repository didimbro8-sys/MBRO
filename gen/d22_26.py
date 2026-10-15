import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/gen")
from lib import *
I=[]
def car(prefix, cov, inners, c):
    I.append((f"{prefix}_01_couverture", cover(*cov)))
    for k,(tag,t,x) in enumerate(inners,2):
        I.append((f"{prefix}_{k:02d}", inner(k-1,tag,t,x)))
    I.append((f"{prefix}_{len(inners)+2:02d}_appel-action", cta(*c)))
# 22 oct 18h : décrypter une campagne (méthode)
car("AM-Digital_22oct_1800_decrypter-campagne",
 ("Le Prime · Décryptage", f"Décrypter une {G('campagne')} en 4 questions", "La méthode qu'on utilise pour analyser n'importe quelle pub."),
 [("Question 1","Quel est le message ?","En une phrase. Si on ne peut pas le résumer, le public non plus."),
  ("Question 2","À qui parle-t-elle ?","Âge, métier, ville, problème. Une campagne qui parle à tout le monde ne parle à personne."),
  ("Question 3","Sur quel canal ?","Affiche, TikTok, radio, WhatsApp : le canal doit être celui où la cible passe son temps."),
  ("Question 4","Quelle action attend-elle ?","Appeler, acheter, s'abonner, partager. Pas d'action claire = budget perdu.")],
 ("Votre tour", f"Quelle campagne doit-on {G('décrypter')} ?", "Proposez une campagne vue à Abidjan en commentaire : on l'analyse avec cette méthode.", "Commentez"))
# 23 oct 12h : ligne éditoriale en 4 étapes
car("AM-Digital_23oct_1200_ligne-editoriale",
 ("Le Midi Digital", f"Votre ligne éditoriale en {G('4 étapes')}", "Arrêtez de publier au hasard."),
 [("Étape 1","Votre objectif","Être connu, vendre, recruter, rassurer ? Un objectif principal par trimestre."),
  ("Étape 2","Votre cible","Le portrait précis de votre client idéal : son métier, ses problèmes, ses réseaux."),
  ("Étape 3","Vos 3 piliers","Exemple : conseils, coulisses, preuves clients. Chaque post entre dans un pilier."),
  ("Étape 4","Votre rythme","3 posts par semaine tenus 3 mois valent mieux que 3 posts par jour pendant 1 semaine.")],
 ("Modèle gratuit", f"Écrivez {G('LIGNE')} en commentaire", "On vous envoie notre modèle de ligne éditoriale à remplir.", "Écrivez LIGNE"))
# 23 oct 18h : vos questions
I.append(("AM-Digital_23oct_1800_vos-questions", post("Le Prime · Vos questions", f"Une question {G('marketing')} ?", "Posez-la en commentaire : on répond à chacune, en commentaire ou en vidéo cette semaine.")))
# 24 oct 07h story
I.append(("AM-Digital_24oct_0700_story-challenge", story("Aujourd'hui · 12 h", f"Challenge {G('visibilité')}", [("1","Votre activité en 1 phrase"),("2","Votre objectif du mois"),("3","Identifiez un entrepreneur")], "Rendez-vous à midi sur nos pages")))
# 24 oct 18h règles du challenge
car("AM-Digital_24oct_1800_challenge-regles",
 ("Challenge visibilité", f"Comment {G('participer')} ?", "3 étapes, 2 minutes, une vraie visibilité."),
 [("Étape 1","Une phrase","Ce que vous faites et pour qui. Exemple : « Je livre des repas sains aux bureaux du Plateau. »"),
  ("Étape 2","Un objectif","Ce que vous voulez ce mois-ci : 50 clients, une boutique en ligne, plus de messages…"),
  ("Étape 3","Un entrepreneur","Identifiez un entrepreneur qui mérite d'être connu. Les meilleures réponses passent en Story.")],
 ("À vous", f"Participez en {G('commentaire')}", "Les meilleures réponses seront mises en avant sur nos pages.", "Participez"))
# 25 oct 07h citation (AM.Digital)
I.append(("AM-Digital_25oct_0700_inspiration", quote("Le dimanche inspiration", f"Une marque, c'est ce que vos clients {G('racontent')} quand vous n'êtes pas là.", "AM.Digital")))
# 25 oct 18h besoin -> solution
car("AM-Digital_25oct_1800_besoin-solution",
 ("Le Prime", f"Quelle prestation pour quel {G('besoin')} ?", "Le bon choix part toujours d'un diagnostic."),
 [("Besoin → Solution","Pas de visibilité ?","Un audit digital : on trouve ce qui bloque et par où commencer."),
  ("Besoin → Solution","Image incohérente ?","Une identité visuelle : logo, couleurs, typographies, règles d'usage."),
  ("Besoin → Solution","Publications irrégulières ?","Un community management : calendrier, création, publication, réponses."),
  ("Besoin → Solution","Besoin de décideurs ?","Une communication institutionnelle : plateforme de marque, discours, supports.")],
 ("Par où commencer ?", f"Le {G('diagnostic')} digital", "Écrivez DIAGNOSTIC sur WhatsApp : +225 01 71 95 45 23", "WhatsApp « DIAGNOSTIC »"))
# 26 oct 07h
I.append(("AM-Digital_26oct_0700_1-tache-15-min", post("Le lundi des pros", f"1 tâche, {G('15 minutes')}", "Épinglez vos 3 meilleures publications en haut de votre page. Votre profil gagne en clarté.")))
# 26 oct 18h audit express
car("AM-Digital_26oct_1800_audit-express",
 ("L'audit du jour #2", f"L'audit {G('express')} en 5 points", "Faites-le sur votre page en 5 minutes."),
 [("Point 1","Photo de profil","Nette, reconnaissable, lisible même en petit."),
  ("Point 2","Bio","Ce que vous vendez, à qui, comment commander."),
  ("Point 3","Contact","Un numéro WhatsApp ou un bouton visible en un clic."),
  ("Point 4","Régularité","Au moins 3 publications par semaine sur le dernier mois."),
  ("Point 5","Appel à l'action","Chaque post dit au client quoi faire ensuite.")],
 ("Votre score", f"Combien sur {G('5')} ?", "Dites-le en commentaire. Écrivez AUDIT pour un audit offert de votre page (avec votre accord).", "Écrivez AUDIT"))
render(I); print(len(I))
