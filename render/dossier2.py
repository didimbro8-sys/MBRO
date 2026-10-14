import glob, html
S="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"
FF=f"file://{S}/fonts/package/files/montserrat-latin-"
LOGO=f"file://{S}/ds/project/assets/Logos/am-digital-logo-carre.png"
thumbs=lambda pat,w: "".join(f'<img src="file://{f}" style="width:{w}px;border-radius:4px">' for f in sorted(glob.glob(f"{S}/s2/visuels/{pat}/*.png")))
cal=[
("Mar. 21 oct.","Carrousel 6 diapos + vidéo","Les 3 communications","AM-Digital_3-communications.mp4 · carrousel 05","Institutionnelle, d'entreprise, digitale : trois communications, trois missions. Laquelle manque à votre entreprise ? Répondez 1, 2 ou 3. #CommunicationDentreprise #Abidjan #MarketingDigital","Commentez 1, 2 ou 3"),
("Mer. 22 oct.","Vidéo","3 idées de contenu pour une boutique","AM-Digital_3-idees-boutique.mp4","Trois idées à tester cette semaine. Identifiez un commerçant qui doit voir ça. #Commerce #Abidjan #Entrepreneur","Identifiez un commerçant"),
("Jeu. 23 oct.","Vidéo","La ligne éditoriale","AM-Digital_ligne-editoriale.mp4","Sans ligne éditoriale, on publie au hasard et personne ne retient rien. Écrivez LIGNE en commentaire : on vous envoie notre modèle. #Strategie #MarketingDigital","Écrivez LIGNE"),
("Ven. 24 oct.","Vidéo + Story","Challenge visibilité","AM-Digital_challenge-visibilite.mp4 · Story 08","Challenge visibilité : présentez votre activité en une phrase, ajoutez votre objectif du mois, identifiez un entrepreneur. Les meilleures réponses passent en Story.","Participez en commentaire"),
("Sam. 25 oct.","Carrousel 6 diapos","Nos offres","carrousel 06","De la réputation aux ventes : voici ce qu'AM.Digital fait pour votre entreprise. Écrivez DIAGNOSTIC sur WhatsApp pour commencer.","WhatsApp « DIAGNOSTIC »"),
("Dim. 26 oct.","Vidéo","30 secondes de marketing #2","AM-Digital_30-secondes-2-appels-action.mp4","Un post, une action. Voici 3 appels à l'action qui font écrire vos clients. Enregistrez pour vos prochains posts.","Enregistrez"),
("Lun. 27 oct.","Vidéo Q/R (à filmer)","FAQ : vos questions du challenge","À filmer : réponses aux meilleures questions reçues","Vos questions, nos réponses. Posez la vôtre en commentaire pour la prochaine vidéo.","Posez votre question")]
calrows="".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td class='f'>{d}</td><td>{html.escape(e)}</td><td>{f}</td></tr>" for a,b,c,d,e,f in cal)
offres=[
("Diagnostic digital","Toute entreprise qui veut savoir pourquoi sa présence ne rapporte pas.","Audit des réseaux, du site et des supports ; 3 à 5 priorités ; plan d'action à 90 jours.","1 à 2 semaines","Priorités validées, plan signé"),
("Communication institutionnelle","Entreprises établies, institutions, écoles, cliniques, ONG, entreprises en levée de fonds ou en appel d'offres.","Plateforme de marque (mission, valeurs, messages clés), identité visuelle, kit presse, discours et prises de parole, rapport d'activité, communication RSE.","1 à 3 mois","Notoriété, retombées presse, cohérence de marque"),
("Communication d'entreprise","PME qui vendent à d'autres entreprises ou recrutent.","Brochure et présentation commerciale, catalogue, supports de salon, communication interne (lettre interne, affichage, événements), marque employeur.","1 à 2 mois","Rendez-vous commerciaux, taux de réponse, engagement interne"),
("Communication digitale","TPE, PME, marques et professionnels qui veulent des clients en ligne.","Ligne éditoriale, calendrier, création de visuels et vidéos, gestion des réseaux, site ou page de contact, suivi mensuel des résultats.","Abonnement mensuel","Abonnés qualifiés, conversations WhatsApp, demandes de devis"),
("Pack Image & Croissance","Entreprises qui veulent tout aligner : réputation, supports et digital.","Les trois communications pilotées ensemble, un même message sur tous les canaux, un comité de suivi mensuel.","6 mois","Notoriété, demandes entrantes, chiffre d'affaires attribuable")]
offrows="".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td class='todo'>À fixer par AM.Digital</td></tr>" for a,b,c,d,e in offres)
secteurs=[
("Restaurant ou maquis à Abidjan","Peu de clients en semaine malgré une page active.","Digital : plats en vidéo courte chaque jour, menu et prix en Story, commande WhatsApp en un clic, avis clients en publication. Entreprise : carte imprimée et chevalets avec QR code WhatsApp.","Commandes WhatsApp par semaine"),
("École ou centre de formation privé","Les parents comparent et hésitent avant les inscriptions.","Institutionnel : valeurs, résultats aux examens, équipe pédagogique. Digital : témoignages de parents (avec accord), journées portes ouvertes en direct. Entreprise : brochure d'inscription.","Demandes d'inscription, visites"),
("PME de services aux entreprises (BTP, logistique, sécurité)","Dépend du bouche-à-oreille et répond mal aux appels d'offres.","Institutionnel : plaquette, références, certifications, page LinkedIn de l'entreprise. Entreprise : présentation commerciale type. Digital : études de cas de chantiers ou missions, publiées chaque mois.","Rendez-vous qualifiés, consultations")]
secrows="".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a,b,c,d in secteurs)
H=f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face{{font-family:M;font-weight:500;src:url('{FF}500-normal.woff2')}}@font-face{{font-family:M;font-weight:700;src:url('{FF}700-normal.woff2')}}@font-face{{font-family:M;font-weight:800;src:url('{FF}800-normal.woff2')}}
body{{font-family:M,Arial,sans-serif;font-weight:500;font-size:9.8pt;line-height:1.5;color:#22121d;margin:0}}
.cover{{background:#300024;color:#fff;height:255mm;padding:22mm 18mm;box-sizing:border-box;display:flex;flex-direction:column;position:relative;page-break-after:always;border-radius:4px}}
.cover img.l{{width:110px;border-radius:8px}} .cover h1{{font-size:34pt;line-height:1.02;font-weight:800;margin:auto 0 10px}} .cover h1 span,.g{{color:#f1bc18}}
.eye{{font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18;font-weight:700}}
.px{{position:absolute;background:#f1bc18}}
h2{{font-weight:800;font-size:15pt;color:#66004a;margin:0 0 6px;page-break-after:avoid}} h3{{font-weight:800;font-size:11pt;color:#66004a;margin:16px 0 4px}}
section{{page-break-before:always}} section:first-of-type{{page-break-before:auto}}
.lead{{font-size:10.5pt}}
table{{border-collapse:collapse;width:100%;font-size:8.6pt;margin:8px 0}} th,td{{text-align:left;padding:5px 6px;border-bottom:1px solid #ead9e3;vertical-align:top}} th{{background:#f3e3ee;color:#66004a;font-weight:700}} tr{{page-break-inside:avoid}}
td.f{{color:#6e5a66;font-size:8pt}} td.todo{{color:#a87a08;font-weight:700}}
.box{{border:1px solid #ead9e3;border-radius:6px;padding:9px 12px;margin:7px 0;page-break-inside:avoid}} .box b{{color:#66004a}}
.thumbs{{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}}
ol li,ul li{{margin:3px 0}}
</style></head><body>
<div class="cover"><img class="l" src="{LOGO}"><div class="px" style="right:30mm;top:30mm;width:18mm;height:18mm"></div><div class="px" style="right:20mm;top:22mm;width:9mm;height:9mm"></div><div class="px" style="right:22mm;top:52mm;width:9mm;height:9mm;background:#c79613"></div>
<div class="eye" style="margin-top:auto">Campagne 14 oct. – 14 nov. 2026 · Semaine 2</div>
<h1>Dossier de production et <span>propositions stratégiques</span></h1>
<div style="font-size:12pt;color:#d9c3d2;max-width:140mm">Contenus du 21 au 27 octobre, plan 100 % organique, offres de communication institutionnelle, d'entreprise et digitale pour les entreprises.</div>
<div style="margin-top:14mm;font-size:9pt;color:#d9c3d2">Préparé le 14 octobre 2026 · AM.Digital, agence marketing digital, Abidjan</div></div>

<section><h2>1. Sans budget publicitaire : le plan 100 % organique</h2>
<p class="lead">Sans publicité, la croissance viendra de trois moteurs : la régularité, la conversation et les partenariats. Chaque jour compte donc deux heures de présence active en plus de la publication.</p>
<div class="box"><b>Publier chaque jour, en natif.</b> Un format pensé pour chaque réseau : vidéo verticale pour TikTok et Reels, carrousel pour Facebook et Instagram, Stories quotidiennes. Facebook reste le canal n°1 (8,4 millions de personnes touchables en Côte d'Ivoire, contre 895 000 sur Instagram, source DataReportal 2026).</div>
<div class="box"><b>Commenter là où sont les entrepreneurs.</b> 30 minutes par jour de commentaires utiles (un conseil, pas une publicité) sous les publications de pages d'entrepreneurs ivoiriens et dans les groupes Facebook d'entrepreneurs d'Abidjan. C'est le levier organique le plus rapide pour faire visiter le profil.</div>
<div class="box"><b>Deux collaborations par semaine.</b> Publications en collaboration sur Instagram, duos et réponses vidéo sur TikTok, live à deux sur Facebook avec un entrepreneur ou un créateur dont l'audience correspond à la cible. Chacun présente l'autre à sa communauté.</div>
<div class="box"><b>Faire participer.</b> Le challenge visibilité (24 oct.), les audits gratuits en vidéo et les réponses vidéo aux commentaires transforment l'audience en contenu, et le contenu en prospects.</div>
<div class="box"><b>Activer le réseau existant.</b> Statuts WhatsApp quotidiens, partage des publications dans les groupes WhatsApp professionnels, invitation des contacts Facebook à aimer la page (fonction « Inviter » de la page).</div>
<h3>Objectif d'abonnés : la recommandation</h3>
<p>Partir de 18 abonnés pour atteindre 10 000 en 31 jours sans publicité demanderait plus de 300 nouveaux abonnés par jour : ce n'est pas un rythme qu'un compte qui démarre obtient en organique. Je recommande de garder 10 000 comme horizon à 90 jours, de viser pour le 14 novembre une cible de travail de 2 000 abonnés cumulés, et de faire des 10 clients signés l'objectif prioritaire. La cible sera confirmée au point du 23 octobre avec les chiffres réels du tableau de pilotage.</p>
</section>

<section><h2>2. Calendrier de la semaine 2 (21 – 27 octobre)</h2>
<p class="lead">La semaine 2 installe AM.Digital comme expert de la communication d'entreprise, au-delà des réseaux sociaux. Elle présente les offres le 25 octobre.</p>
<table><tr><th>Date</th><th>Format</th><th>Sujet</th><th>Fichier</th><th>Légende prête à copier</th><th>Action</th></tr>{calrows}</table>
<p>Chaque jour : 3 à 5 Stories (coulisses, sondage, partage du post), 30 minutes de commentaires, réponses aux messages en moins d'une heure. Un son tendance s'ajoute dans l'application au moment de publier chaque vidéo.</p>
<h3>Carrousel « Les 3 communications » (21 oct.)</h3><div class="thumbs">{thumbs('05_*',104)}</div>
<h3>Carrousel « Nos offres » (25 oct.)</h3><div class="thumbs">{thumbs('06_*',104)}</div>
<h3>Couvertures des vidéos et Story du challenge</h3><div class="thumbs">{thumbs('07_*',88)}{thumbs('08_*',88)}</div>
</section>

<section><h2>3. Propositions stratégiques pour les entreprises</h2>
<p class="lead">AM.Digital propose aux entreprises ivoiriennes une communication complète : la réputation (institutionnelle), les ventes et la cohésion (d'entreprise), la visibilité et les demandes (digitale). Le digital relie les trois.</p>
<table><tr><th>Offre</th><th>Pour qui</th><th>Livrables</th><th>Durée</th><th>Indicateurs suivis</th><th>Tarif</th></tr>{offrows}</table>
<h3>La méthode AM.Digital en 5 étapes</h3>
<ol><li><b>Diagnostic</b> : où en est l'entreprise, ce que disent ses clients, ce que font ses concurrents.</li><li><b>Stratégie</b> : objectifs mesurables, cibles, messages clés, canaux.</li><li><b>Création</b> : identité, supports, contenus, dans une charte unique.</li><li><b>Diffusion</b> : publication, relations presse, événements, présence digitale quotidienne.</li><li><b>Mesure</b> : rapport mensuel et ajustements.</li></ol>
<div style="page-break-inside:avoid"><h3>Trois exemples de stratégies par secteur (illustratifs)</h3>
<table><tr><th>Secteur</th><th>Problème fréquent</th><th>Stratégie proposée</th><th>Indicateur clé</th></tr>{secrows}</table></div>
<p style="font-size:8.5pt;color:#6e5a66">Exemples construits pour illustrer la méthode, pas des cas clients réels. Les tarifs restent à fixer par AM.Digital selon le temps de production, les charges et la marge.</p>
</section>

<section><h2>Annexe. Modèle de ligne éditoriale</h2>
<p class="lead">Le modèle promis aux personnes qui écrivent LIGNE en commentaire (vidéo du 23 octobre). À envoyer en image ou en PDF en message privé.</p>
<table><tr><th>Élément</th><th>À remplir</th><th>Exemple pour une boutique de prêt-à-porter</th></tr>
<tr><td><b>Promesse</b></td><td>Ce que vous apportez, à qui, en une phrase</td><td>Des tenues en wax sur mesure, livrées à Abidjan en 7 jours</td></tr>
<tr><td><b>Cible</b></td><td>Qui achète, et pourquoi</td><td>Femmes actives de 25 à 45 ans, pour le travail et les cérémonies</td></tr>
<tr><td><b>Ton</b></td><td>Trois mots</td><td>Chaleureux, élégant, direct</td></tr>
<tr><td><b>Pilier 1 · Éduquer (30 %)</b></td><td>Ce que vous apprenez à vos clients</td><td>Comment choisir son tissu, entretenir le wax</td></tr>
<tr><td><b>Pilier 2 · Prouver (25 %)</b></td><td>Avis, réalisations, résultats</td><td>Clientes en tenue (avec accord), avis WhatsApp</td></tr>
<tr><td><b>Pilier 3 · Coulisses (20 %)</b></td><td>Comment vous travaillez</td><td>L'atelier, la couture, la livraison</td></tr>
<tr><td><b>Pilier 4 · Rassurer (15 %)</b></td><td>Délais, paiement, garanties</td><td>Délais, retouches offertes, paiement à la livraison</td></tr>
<tr><td><b>Pilier 5 · Vendre (10 %)</b></td><td>Offres et appels à l'action</td><td>Nouvelle collection, « Écrivez TAILLE »</td></tr>
<tr><td><b>Rythme</b></td><td>Combien de publications par semaine</td><td>5 posts, Stories chaque jour</td></tr></table>
<div style="margin-top:16px;display:flex;align-items:center;gap:12px"><img src="{LOGO}" style="width:48px;border-radius:6px"><div style="font-size:9pt;color:#6e5a66">AM.Digital · Agence marketing digital · Abidjan · WhatsApp +225 01 71 95 45 23 · didimbro8@gmail.com</div></div>
</section></body></html>"""
open(f"{S}/render/dossier2.html","w").write(H)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=b.new_page(); pg.goto(f"file://{S}/render/dossier2.html"); pg.wait_for_timeout(500)
    pg.pdf(path=f"{S}/s2/AM-Digital_Dossier-semaine2_et_Propositions-strategiques.pdf",format="A4",print_background=True,margin={"top":"14mm","bottom":"14mm","left":"14mm","right":"14mm"}); b.close()
print("ok")
