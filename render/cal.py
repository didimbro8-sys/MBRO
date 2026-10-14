import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
OUT="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/livraison/03_Calendrier_editorial/AM-Digital_Calendrier-editorial_14oct-14nov-2026.xlsx"
F="Arial"; VIO="66004A"
J=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
def ph(d):
    if d<=dt.date(2026,10,16): return "1. Lancement"
    if d<=dt.date(2026,10,23): return "2. Découverte"
    if d<=dt.date(2026,10,30): return "3. Accélération"
    if d<=dt.date(2026,11,6): return "4. Conversion"
    return "5. Sprint final"
P="01_Affiches_PNG/"; V="02_Videos_MP4/"
# (date, plateformes, format, sujet, fichier, légende, CTA, 2e TikTok)
R=[
("2026-10-14","FB, IG, TikTok","Vidéo face caméra (ou version motion)","Manifeste : le retour d'AM.Digital",V+"AM-Digital_manifeste.mp4 · "+P+"03_Couvertures_videos/AM-Digital_couverture_14oct_manifeste.png","Deux ans de silence. Aujourd'hui, AM.Digital est de retour. Pendant 30 jours, on partage gratuitement tout ce qui aide une entreprise ivoirienne à transformer sa page en clients. Abonnez-vous pour ne rien manquer. #MarketingDigital #Abidjan #CôteDIvoire #Entrepreneur","Abonnez-vous","Coulisses muettes « Jour 1 / 31 »"),
("2026-10-15","IG, TikTok (FB déjà publié le 14)","Carrousel 7 diapos + Reel","5 erreurs qui font fuir vos clients",P+"01_Carrousel_5-erreurs_15oct/ · "+V+"AM-Digital_5-erreurs.mp4","Combien de ces erreurs sur votre page ? Répondez avec un chiffre de 0 à 5 en commentaire, on vous dit par quoi commencer. Enregistrez pour vérifier ce soir. #MarketingDigital #Abidjan #PME","Commentez 0 à 5","30 secondes de marketing #1 — la bio ("+V+"AM-Digital_30-secondes-1-la-bio.mp4)"),
("2026-10-16","FB, IG, TikTok","Face caméra 35 s","Pourquoi publier ne suffit pas",P+"03_Couvertures_videos/AM-Digital_couverture_16oct_publier-ne-suffit-pas.png","Vue, confiance, action. Il manque laquelle sur votre page ? Dites-nous ce que vous vendez en commentaire, on vous répond avec un appel à l'action adapté.","Commentez votre activité","30 secondes de marketing #2 — 3 appels à l'action pour une boutique"),
("2026-10-17","FB, IG, TikTok","Enregistrement d'écran commenté 45 s","L'audit du jour #1",P+"03_Couvertures_videos/AM-Digital_couverture_17oct_audit-du-jour-1.png","L'audit du jour #1 : [nom de la page, avec son accord]. Vous voulez que votre page soit la prochaine ? Écrivez AUDIT en commentaire.","Écrivez AUDIT","30 secondes de marketing #3 — la règle des 3 secondes"),
("2026-10-18","FB, IG, TikTok","Transformation 15 s","Avant / après d'un visuel",P+"03_Couvertures_videos/AM-Digital_couverture_18oct_avant-apres.png","Même produit, même message. Seule la mise en page a changé. Partagez à un commerçant qui devrait voir ça.","Partagez","30 secondes de marketing #4 — 1 visuel = 1 message"),
("2026-10-19","FB, IG, TikTok","Carrousel 6 diapos + Reel","Le parcours du client en ligne",P+"02_Carrousel_Parcours-client_19oct/ · "+V+"AM-Digital_parcours-client.mp4","Soyez honnête : à quelle étape perdez-vous vos clients ? Répondez 1, 2, 3 ou 4.","Commentez 1 à 4","30 secondes de marketing #5 — répondre en moins d'une heure"),
("2026-10-20","FB, IG (Story), TikTok","Sondage","Votre plus gros défi sur les réseaux ?",P+"04_Stories/AM-Digital_story_20oct_sondage.png","Entrepreneurs : quel est votre plus gros défi sur les réseaux en ce moment ? A. Idées de contenu · B. Abonnés qui achètent · C. Pub sans perdre d'argent · D. Le temps. Répondez A, B, C ou D.","Votez","30 secondes de marketing #6 — réponse à la meilleure question"),
("2026-10-21","FB, IG, TikTok","Vidéo coulisses","Comment se prépare un contenu professionnel","À produire (kit semaine 2)","Du brief à la publication : voici ce qui se passe avant qu'un post soit en ligne.","Abonnez-vous","Série selon la lettre gagnante du sondage"),
("2026-10-22","FB, IG, TikTok","Reel / TikTok","3 idées de contenu pour une boutique","À produire (kit semaine 2)","Présentez, prouvez la valeur, facilitez l'achat. Identifiez un commerçant qui devrait voir ça.","Identifiez un commerçant","Série sondage"),
("2026-10-23","FB, IG, TikTok","Vidéo","Pourquoi une publicité échoue","À produire (kit semaine 2)","Une publicité relie une audience, une offre et un objectif. Il en manque un ? Elle échoue.","Écrivez sur WhatsApp","Point de contrôle n°2"),
("2026-10-24","FB, IG, TikTok","Vidéo participative","Challenge visibilité","À produire","Présentez votre activité et votre objectif digital en commentaire : on met en avant les meilleures réponses.","Participez","Duo / collaboration créateur"),
("2026-10-25","FB, IG","Carrousel","Nos services, de la stratégie au suivi","À produire","Stratégie, contenus, publicité, résultats. Demandez le catalogue sur WhatsApp.","Demandez le catalogue","Coulisses"),
("2026-10-26","FB, IG, TikTok","Étude de cas illustrative","Stratégie pour une PME (exemple)","À produire","Exemple : partir d'un problème commercial pour construire un plan en 30 jours.","Demandez conseil","Audit du jour #2"),
("2026-10-27","FB, IG, TikTok","Vidéo Q/R","FAQ marketing digital","À produire","Vos questions, nos réponses en vidéo. Posez la vôtre en commentaire.","Posez votre question","Réponse vidéo à un commentaire"),
("2026-10-28","FB, IG, TikTok","Écran commenté","L'audit du jour #2","À produire","L'audit du jour #2. Votre page est la prochaine ? Écrivez AUDIT.","Écrivez AUDIT","30 secondes de marketing #7"),
("2026-10-29","FB, IG, TikTok","Transformation","Avant / après #2","À produire","Même message, autre impact.","Partagez","30 secondes de marketing #8"),
("2026-10-30","FB, IG, TikTok","Carrousel","Publicité Meta : les bases avant de dépenser","À produire","Objectif, audience, visuel, suivi : les 4 réglages à vérifier avant de booster.","Enregistrez","Point de contrôle n°3"),
("2026-10-31","FB, IG, TikTok","Vidéo + visuel offre","Offre : le diagnostic digital","À produire","Vous ne savez pas pourquoi votre page ne vend pas ? Le diagnostic digital AM.Digital identifie vos 3 à 5 priorités. Écrivez DIAGNOSTIC sur WhatsApp.","WhatsApp « DIAGNOSTIC »","30 secondes de marketing #9"),
("2026-11-01","FB, IG","Témoignage (avec accord)","Ce que dit un client","À produire, selon accord client","[Témoignage réel autorisé]","Demandez un devis","Coulisses"),
("2026-11-02","FB, IG, TikTok","Carrousel offre","Pack Visibilité digitale","À produire","Calendrier, visuels, vidéos, gestion des réseaux et suivi : votre communication tenue chaque semaine.","Demandez un devis","Audit du jour #3"),
("2026-11-03","FB, IG, TikTok","Vidéo","Notre méthode en 4 étapes","À produire","Diagnostic, stratégie, production, résultats.","Écrivez sur WhatsApp","30 secondes de marketing #10"),
("2026-11-04","FB, IG, TikTok","Écran commenté","L'audit du jour #3","À produire","L'audit du jour #3.","Écrivez AUDIT","Réponse à un commentaire"),
("2026-11-05","FB, IG","Carrousel offre","Pack Acquisition & Performance","À produire","Des campagnes Meta pensées pour générer des demandes, suivies chaque semaine.","Demandez un devis","30 secondes de marketing #11"),
("2026-11-06","FB, IG, TikTok","Live / Q&R","Questions-réponses en direct","À produire","En direct ce soir : posez toutes vos questions marketing.","Rejoignez le live","Point de contrôle n°4"),
("2026-11-07","FB, IG, TikTok","Vidéo","3 erreurs de publicité Meta","À produire","Booster sans objectif, viser tout le monde, ne rien mesurer.","Enregistrez","Audit du jour #4"),
("2026-11-08","FB, IG, TikTok","Transformation","Avant / après #3","À produire","Avant / après.","Partagez","30 secondes de marketing #12"),
("2026-11-09","FB, IG, TikTok","Coulisses chiffrées","Bilan à mi-parcours (chiffres réels)","À produire avec les données du tableau de pilotage","Ce qu'on a appris en 26 jours de publication, chiffres réels à l'appui.","Abonnez-vous","Réponse à un commentaire"),
("2026-11-10","FB, IG, TikTok","Vidéo","Combien coûte une stratégie digitale ?","À produire","Ce qui fait varier un tarif, et comment choisir.","Demandez un devis","30 secondes de marketing #13"),
("2026-11-11","FB, IG, TikTok","Écran commenté","L'audit du jour #5","À produire","L'audit du jour #5.","Écrivez AUDIT","Coulisses"),
("2026-11-12","FB, IG, TikTok","Visuel offre","Diagnostics de novembre : places limitées","À produire","Nous prenons [nombre] diagnostics ce mois-ci. Écrivez DIAGNOSTIC sur WhatsApp.","WhatsApp « DIAGNOSTIC »","30 secondes de marketing #14"),
("2026-11-13","FB, IG, TikTok","Coulisses","31 jours de publication : les coulisses","À produire","Ce qu'il a fallu pour publier tous les jours pendant un mois.","Abonnez-vous","Réponse à un commentaire"),
("2026-11-14","FB, IG, TikTok","Vidéo","Merci et suite","À produire","Merci à vous. La suite commence lundi.","Abonnez-vous","Bilan final"),
]
wb=Workbook(); ws=wb.active; ws.title="Calendrier"
ws["A1"]="Calendrier éditorial AM.Digital — 14 oct. au 14 nov. 2026"; ws["A1"].font=Font(name=F,bold=True,size=16,color=VIO)
ws["A2"]="Semaine 1 : visuels et vidéos livrés dans ce dossier. Semaines suivantes : sujets planifiés, ajustés à chaque point de contrôle selon les résultats. Colonne Statut en jaune à tenir à jour."; ws["A2"].font=Font(name=F,italic=True,size=10,color="6E5A66")
H=["Date","Jour","Phase","Plateformes","Format","Sujet","Fichier(s) du dossier","Légende prête à copier","Appel à l'action","2e TikTok du jour","Statut"]
for j,h in enumerate(H,1):
    c=ws.cell(4,j,h); c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor=VIO); c.alignment=Alignment(wrap_text=True,vertical="center")
for i,r in enumerate(R,5):
    d=dt.date.fromisoformat(r[0])
    vals=[d,J[d.weekday()],ph(d)]+list(r[1:])+["Prêt" if d<=dt.date(2026,10,20) else "À produire"]
    for j,v in enumerate(vals,1):
        c=ws.cell(i,j,v); c.font=Font(name=F,size=10); c.alignment=Alignment(wrap_text=True,vertical="top"); c.border=Border(bottom=Side(style="thin",color="EAD9E3"))
    ws.cell(i,1).number_format="DD/MM/YYYY"; ws.cell(i,11).fill=PatternFill("solid",fgColor="FFF6D6")
    if d<=dt.date(2026,10,20):
        for j in range(1,11): ws.cell(i,j).fill=PatternFill("solid",fgColor="F7EEF4")
last=4+len(R)
dv=DataValidation(type="list",formula1='"À produire,Prêt,Validé,Publié,Reporté"',allow_blank=True); ws.add_data_validation(dv); dv.add(f"K5:K{last}")
for col,w in zip("ABCDEFGHIJK",[12,10,15,20,22,32,40,60,20,30,12]): ws.column_dimensions[col].width=w
ws.freeze_panes="C5"; ws.auto_filter.ref=f"A4:K{last}"; ws.sheet_view.showGridLines=False
s=last+2
ws.cell(s,6,"Publications prêtes").font=Font(name=F,bold=True,size=10)
ws.cell(s,7,f'=COUNTIF(K5:K{last},"Prêt")+COUNTIF(K5:K{last},"Validé")+COUNTIF(K5:K{last},"Publié")').font=Font(name=F,size=10)
ws.cell(s+1,6,"Publications publiées").font=Font(name=F,bold=True,size=10)
ws.cell(s+1,7,f'=COUNTIF(K5:K{last},"Publié")').font=Font(name=F,size=10)
ws.cell(s+2,6,"Total planifié").font=Font(name=F,bold=True,size=10)
ws.cell(s+2,7,f"=COUNTA(F5:F{last})").font=Font(name=F,size=10)
wb.save(OUT); print(len(R))
