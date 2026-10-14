import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/gen")
from lib import *
I=[]
# 16 oct
I.append(("AM-Digital_16oct_0700_mot-du-fondateur", quote("Le mot du fondateur",
  f"Trop d'entreprises ivoiriennes publient beaucoup… et {G('vendent peu')}. Pendant 30 jours, on vous montre comment changer ça, {G('gratuitement')}, ici.","Le fondateur d'AM.Digital")))
I+= [("AM-Digital_16oct_1800_diagnostic_01_couverture", cover("AM.Digital · Convertir",f"Le diagnostic digital, {G('c&#8217;est quoi')} ?","Swipez : 4 étapes, 1 plan d'action →",100)),
 ("AM-Digital_16oct_1800_diagnostic_02", inner(1,"Symptômes",f"On écoute vos {G('blocages')}","Peu de messages ? Peu de ventes ? Une page qui ne décolle pas ? Tout part de là.")),
 ("AM-Digital_16oct_1800_diagnostic_03", inner(2,"Analyse",f"On passe tout au {G('crible')}","Réseaux sociaux, site web, supports, messages : ce qui marche, ce qui bloque.")),
 ("AM-Digital_16oct_1800_diagnostic_04", inner(3,"Ordonnance",f"3 à 5 {G('priorités')}","Pas 40 conseils : les quelques actions qui auront le plus d'effet, classées.")),
 ("AM-Digital_16oct_1800_diagnostic_05_appel-action", cta("En 1 à 2 semaines",f"Un {G('plan d&#8217;action')} clair pour votre entreprise.","Le point de départ de toute stratégie sérieuse.","Écrivez DIAGNOSTIC"))]
# 17 oct
I.append(("AM-Digital_17oct_0700_chiffre-8-4-millions", big("Le chiffre du jour","8,4 M",f"personnes touchables sur {G('Facebook')} en Côte d'Ivoire",
  "Votre client y est. La question n'est pas « faut-il y être ? » mais « comment y être bien ? »","Source : DataReportal, rapport Digital 2026 Côte d'Ivoire (fin 2025)")))
I+= [("AM-Digital_17oct_1200_auto-audit_01_couverture", cover("L'audit du jour · #1",f"Auditez votre page en {G('5 points')}","Faites-le maintenant, ça prend 2 minutes →",104)),
 ("AM-Digital_17oct_1200_auto-audit_02", inner(1,"Photo de profil",f"Votre logo est-il {G('lisible')} en petit ?","Sur mobile, il fait la taille d'un ongle. Simple, net, contrasté.")),
 ("AM-Digital_17oct_1200_auto-audit_03", inner(2,"Bio / À propos",f"Dit-elle {G('quoi, à qui, comment')} ?","Ce que vous vendez, pour qui, et comment commander. Trois lignes.")),
 ("AM-Digital_17oct_1200_auto-audit_04", inner(3,"Contact",f"Peut-on vous écrire en {G('1 clic')} ?","Bouton WhatsApp, numéro, adresse : chaque clic en plus fait perdre un client.")),
 ("AM-Digital_17oct_1200_auto-audit_05", inner(4,"Régularité",f"Dernier post : il y a {G('combien')} de jours ?","Une page muette depuis 3 semaines donne l'impression d'une boutique fermée.")),
 ("AM-Digital_17oct_1200_auto-audit_06", inner(5,"Appel à l'action",f"Vos posts disent-ils {G('quoi faire')} ?","« Écrivez PRIX », « Réservez avant vendredi » : une action précise par post.")),
 ("AM-Digital_17oct_1200_auto-audit_07_appel-action", cta("Votre score ?",f"Vous voulez qu'on audite {G('votre page')} ?","Écrivez AUDIT en commentaire : on choisit les prochaines pages auditées, avec votre accord.","Écrivez AUDIT"))]
I.append(("AM-Digital_17oct_1800_story-questions", story("Votre question, notre réponse",f"Posez-nous {G('vos questions')} marketing",
  [("?","Comment trouver des clients ?"),("?","Quoi publier cette semaine ?"),("?","Faut-il payer la publicité ?")],"Répondez à cette story : les meilleures questions deviennent des vidéos.",104)))
# 18 oct
I.append(("AM-Digital_18oct_0700_1-visuel-1-message", post("Règle d'or du visuel",f"1 visuel = {G('1 message')}",
  "Prix, promo, adresse, horaires, 4 photos… sur la même affiche ? Personne ne retient rien. Un visuel, une idée.",150)))
I+= [("AM-Digital_18oct_1800_methode_01_couverture", cover("AM.Digital · Notre méthode",f"Notre méthode en {G('5 étapes')}","Ce qui se passe quand vous travaillez avec nous →",108)),
 ("AM-Digital_18oct_1800_methode_02", inner(1,"Écouter",f"Comprendre votre {G('entreprise')}","Vos clients, vos offres, vos objectifs, vos contraintes. Avant toute création.")),
 ("AM-Digital_18oct_1800_methode_03", inner(2,"Diagnostiquer",f"Mesurer le {G('point de départ')}","Présence en ligne, image, supports : ce qui marche et ce qui bloque.")),
 ("AM-Digital_18oct_1800_methode_04", inner(3,"Concevoir",f"Une stratégie {G('sur mesure')}","Messages, ligne éditoriale, identité, canaux : un plan clair et réaliste.")),
 ("AM-Digital_18oct_1800_methode_05", inner(4,"Produire et publier",f"Des contenus {G('réguliers')}","Visuels, vidéos, textes, publications : une présence professionnelle, chaque semaine.")),
 ("AM-Digital_18oct_1800_methode_06_appel-action", cta("Étape 5 : mesurer et ajuster",f"Des {G('résultats')} suivis, chaque mois.","Enregistrez ce post, et écrivez-nous quand vous serez prêt.","Écrivez-nous"))]
# 19 oct
I.append(("AM-Digital_19oct_0700_lundi-objectif", post("Le lundi des pros",f"Votre {G('objectif')} de la semaine ?",
  "A · Plus d'abonnés &#160; B · Plus de messages &#160; C · Plus de ventes &#160; D · Une meilleure image<br>Votez en commentaire !",110)))
render(I); print(len(I),"visuels")
