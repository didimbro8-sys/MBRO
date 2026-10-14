S="/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad"
FF=f"file://{S}/fonts/package/files/montserrat-latin-"
LOGO=f"file://{S}/ds/project/assets/Logos/am-digital-logo-carre.png"
def table(head,rows,cls=""):
    h="".join(f"<th>{x}</th>" for x in head)
    b="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<table class="{cls}"><tr>{h}</tr>{b}</table>'
G=lambda t:f'<span class="g">{t}</span>'
personas=table(["Persona","Qui","Ce qui la bloque","Ce qu'elle doit trouver chez AM.Digital"],[
["<b>Awa, commerçante en ligne</b>","Boutique de mode, cosmétiques ou restauration ; vend par Facebook et WhatsApp.","Publie beaucoup, vend peu ; pas de temps ; visuels faits au téléphone.","Des conseils applicables tout de suite, des exemples de son secteur, un contact WhatsApp simple."],
["<b>Konan, dirigeant de PME</b>","Services aux entreprises, BTP, logistique, formation ; 10 à 100 salariés.","Dépend du bouche-à-oreille ; supports commerciaux datés ; pas de présence en ligne structurée.","Une méthode, des études de cas, une offre claire de communication d'entreprise et digitale."],
["<b>Mariam, responsable communication</b>","École privée, clinique, ONG, institution ou grande entreprise.","Doit défendre une image et rendre des comptes ; manque de bras et de cohérence entre canaux.","De l'expertise en communication institutionnelle, de la rigueur, des indicateurs de suivi."]])
piliers=table(["Pilier","Part","Rôle","Exemples de contenus","Séries"],[
["<b>Éduquer</b>","30 %","Faire découvrir et enregistrer","Erreurs fréquentes, règles simples, checklists, définitions (les 3 communications)","30 secondes de marketing"],
["<b>Démontrer</b>","25 %","Prouver l'expertise","Audits de pages en vidéo, avant/après, analyse de campagnes connues","L'audit du jour · Avant/après"],
["<b>Incarner</b>","20 %","Créer la relation","Coulisses, face caméra, réponses vidéo aux commentaires, lives","Coulisses · FAQ"],
["<b>Rassurer</b>","15 %","Lever les objections","Méthode en 5 étapes, témoignages autorisés, résultats réels, délais et tarifs-types","Études de cas"],
["<b>Convertir</b>","10 %","Faire écrire sur WhatsApp","Offres, diagnostic, places limitées, challenge","Offre de la semaine"]])
plateformes=table(["Plateforme","Rôle","Cadence","Formats prioritaires","Indicateur clé"],[
["<b>Facebook</b> (canal n°1)","Portée, confiance, contacts","1 à 2 posts/jour + Stories","Carrousels, vidéos courtes, lives, partage dans les groupes","Abonnés, partages, messages"],
["<b>TikTok</b>","Découverte, audience jeune et entrepreneuriale","1 à 2 vidéos/jour","Vidéos de 15 à 45 s, séries, réponses vidéo","Vues, abonnés, visites de profil"],
["<b>Instagram</b>","Vitrine et portfolio","1 Reel/jour + Stories","Reels, carrousels, Stories interactives","Visites de profil, enregistrements"],
["<b>LinkedIn</b> (à ouvrir, jour 60)","Décideurs, communication institutionnelle et d'entreprise","3 posts/semaine","Études de cas, analyses, documents PDF","Demandes de rendez-vous"],
["<b>Statuts WhatsApp</b>","Réseau existant, relances","Chaque jour","Reprise du post du jour, offre","Réponses, conversations"]])
semaine=table(["Jour","Pilier","Format principal","Série / sujet type","Appel à l'action"],[
["Lundi","Éduquer","Carrousel","Un concept clé (ex. ligne éditoriale)","Enregistrez"],
["Mardi","Démontrer","Vidéo écran commenté","L'audit du jour","Écrivez AUDIT"],
["Mercredi","Éduquer","Vidéo courte","30 secondes de marketing","Commentez"],
["Jeudi","Incarner","Face caméra ou live","Coulisses, FAQ, réponse à un commentaire","Posez votre question"],
["Vendredi","Démontrer","Transformation","Avant/après d'un visuel ou d'une page","Partagez"],
["Samedi","Rassurer","Carrousel ou témoignage","Méthode, étude de cas, résultat réel","Demandez conseil"],
["Dimanche","Convertir","Visuel offre + Story","Offre de la semaine, diagnostic","WhatsApp « DIAGNOSTIC »"]])
kpi=table(["Indicateur","Pourquoi","Objectif de travail","Fréquence"],[
["Abonnés nets cumulés","Taille de l'audience","2 000 au 14 nov. · 10 000 à 90 jours","Quotidienne"],
["Taux d'enregistrement + partage","Utilité perçue du contenu","Au moins 3 % des personnes touchées","Par publication"],
["Visites de profil","Intérêt suscité","En hausse chaque semaine","Hebdomadaire"],
["Conversations WhatsApp entrantes","Passage à l'acte","15 à 20 par semaine dès la semaine 3","Quotidienne"],
["Prospects qualifiés","Besoin, interlocuteur, capacité d'achat","150 sur la campagne","Hebdomadaire"],
["Clients signés","Résultat commercial","10 sur la campagne","Hebdomadaire"]])
road=table(["Période","Priorité","Livrables"],[
["Jours 1 à 30 (14 oct. – 14 nov.)","Lancer et prouver","Publication quotidienne, séries installées, 5 audits du jour, challenge visibilité, offres présentées, premiers clients"],
["Jours 31 à 60","Convertir et fidéliser","Études de cas des premiers clients, témoignages autorisés, offre diagnostic récurrente, partenariats réguliers"],
["Jours 61 à 90","Monter en gamme","Page LinkedIn active, contenus de communication institutionnelle, webinaire ou atelier, site vitrine avec portfolio"]])
amp=["<b>Commenter chaque jour</b> 30 minutes sous les publications d'entrepreneurs et dans les groupes Facebook d'entrepreneurs ivoiriens : un conseil utile, jamais une publicité.",
"<b>Deux collaborations par semaine</b> : posts en collaboration Instagram, duos TikTok, lives à deux avec des entrepreneurs ou créateurs dont l'audience correspond.",
"<b>Les audits gratuits</b> transforment des entreprises réelles en contenu, et leurs abonnés en audience : chaque page auditée partage sa vidéo.",
"<b>Le challenge visibilité</b> fait commenter et identifier d'autres entrepreneurs.",
"<b>Le réseau personnel</b> : statuts WhatsApp quotidiens, invitations à aimer la page Facebook, partage dans les groupes professionnels.",
"<b>Recycler intelligemment</b> : un carrousel devient une vidéo, une vidéo devient trois extraits, une question devient un épisode."]
H=f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face{{font-family:M;font-weight:500;src:url('{FF}500-normal.woff2')}}@font-face{{font-family:M;font-weight:700;src:url('{FF}700-normal.woff2')}}@font-face{{font-family:M;font-weight:800;src:url('{FF}800-normal.woff2')}}
body{{font-family:M,Arial,sans-serif;font-weight:500;font-size:9.8pt;line-height:1.5;color:#22121d;margin:0}}
.cover{{background:#300024;color:#fff;height:255mm;padding:22mm 18mm;box-sizing:border-box;display:flex;flex-direction:column;position:relative;page-break-after:always;border-radius:4px}}
.cover img{{width:110px;border-radius:8px}} .cover h1{{font-size:36pt;line-height:1.02;font-weight:800;margin:auto 0 10px}} .g{{color:#f1bc18}} .cover .g{{color:#f1bc18}}
.eye{{font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:#f1bc18;font-weight:700}}
.px{{position:absolute;background:#f1bc18}}
h2{{font-weight:800;font-size:14pt;color:#66004a;margin:18px 0 6px;page-break-after:avoid}} h2 small{{color:#a87a08;font-size:9pt;font-weight:700;letter-spacing:.1em;display:block;text-transform:uppercase}}
.lead{{font-size:10.5pt}}
table{{border-collapse:collapse;width:100%;font-size:8.6pt;margin:8px 0}} th,td{{text-align:left;padding:5px 6px;border-bottom:1px solid #ead9e3;vertical-align:top}} th{{background:#f3e3ee;color:#66004a;font-weight:700}} tr{{page-break-inside:avoid}}
.box{{border:1px solid #ead9e3;border-radius:6px;padding:9px 12px;margin:7px 0;page-break-inside:avoid}} .box b{{color:#66004a}}
.funnel{{display:flex;gap:6px;margin:10px 0;page-break-inside:avoid}} .funnel div{{flex:1;background:#3c0030;color:#fff;border-radius:6px;padding:9px 10px;font-size:8.5pt}} .funnel b{{display:block;color:#f1bc18;font-size:9.5pt}}
.keep{{page-break-inside:avoid}} .pb{{page-break-before:always}}
ul li{{margin:3px 0}}
</style></head><body>
<div class="cover"><img src="{LOGO}"><div class="px" style="right:30mm;top:30mm;width:18mm;height:18mm"></div><div class="px" style="right:20mm;top:22mm;width:9mm;height:9mm"></div><div class="px" style="right:22mm;top:52mm;width:9mm;height:9mm;background:#c79613"></div>
<div class="eye" style="margin-top:auto">Document de référence · Octobre 2026</div>
<h1>Stratégie de <span class="g">contenu digital</span> AM.Digital</h1>
<div style="font-size:12pt;color:#d9c3d2;max-width:140mm">Faire d'AM.Digital l'agence de référence en communication institutionnelle, d'entreprise et digitale à Abidjan, par des contenus utiles publiés chaque jour.</div>
<div style="margin-top:14mm;font-size:9pt;color:#d9c3d2">Facebook · TikTok · Instagram · LinkedIn · WhatsApp — 100 % organique</div></div>

<h2><small>1 · Synthèse</small>La stratégie en une page</h2>
<p class="lead">AM.Digital gagnera sa place en {G('montrant')} son expertise plutôt qu'en l'affirmant : audits en direct, conseils applicables, preuves. Chaque contenu sert un des cinq piliers, s'adresse à un des trois profils de clients et se termine par une seule action, le plus souvent écrire sur WhatsApp.</p>
<div class="box"><b>Promesse.</b> Nous transformons votre présence en ligne en clients, et votre communication en image solide.</div>
<div class="box"><b>Territoire.</b> Les trois communications d'une entreprise (institutionnelle, d'entreprise, digitale), reliées par le digital, expliquées simplement avec des exemples ivoiriens.</div>
<div class="box"><b>Mécanique.</b> 1 à 2 publications par jour en organique, 5 séries récurrentes, 30 minutes de conversation par jour, 2 collaborations par semaine.</div>
<div class="box"><b>Objectifs.</b> 10 clients signés et 150 prospects qualifiés sur la campagne ; 2 000 abonnés au 14 novembre, 10 000 à 90 jours.</div>

<h2><small>2 · Diagnostic</small>Le point de départ</h2>
<p>Le 14 octobre, AM.Digital comptait 18 abonnés (Facebook 3, Instagram 3, TikTok 12), après plus de deux ans sans publication. La charte (aubergine, or, pixels) est forte et reconnaissable ; les bios renvoyaient vers une page d'administration Blogger, corrigée par un lien WhatsApp.</p>
<p>En Côte d'Ivoire, Facebook touche 8,4 millions de personnes (+22,6 % en un an), Instagram 895 000 (−11,6 %), LinkedIn compte 1,8 million de membres (+12,5 %) (DataReportal, Digital 2026). Le marché des agences est fragmenté, dominé par des indépendants : une agence régulière et pédagogique peut s'y distinguer vite.</p>

<h2 class="pb"><small>3 · Cibles</small>Trois profils de clients</h2>
{personas}
<p>Awa fait l'audience (TikTok, Facebook) ; Konan et Mariam font le chiffre d'affaires (Facebook, LinkedIn, rendez-vous). Le contenu parle aux trois, l'offre se décline pour chacun.</p>

<h2><small>4 · Ligne éditoriale</small>Cinq piliers</h2>
{piliers}
<div class="box"><b>Ton.</b> On vouvoie. Professionnel, pédagogique, concret, chaleureux. Exemples ivoiriens, chiffres réels, jamais de promesse de résultat invérifiable ni de « N°1 ». Un emoji au plus par légende.</div>

<h2 class="pb"><small>5 · Plateformes</small>Un rôle par réseau</h2>
{plateformes}

<h2><small>6 · Semaine type</small>Le rythme qui revient</h2>
{semaine}
<p>Chaque jour en plus : 3 à 5 Stories, 30 minutes de commentaires, réponses aux messages en moins d'une heure entre 8 h et 20 h. Le calendrier détaillé, semaine par semaine, s'ajuste à chaque point de contrôle.</p>

<h2 class="pb"><small>7 · Conversion</small>Du contenu au client</h2>
<div class="funnel"><div><b>Découvrir</b>Vidéo, carrousel, collaboration, commentaire</div><div><b>Visiter</b>Bio claire, épinglés : offres, méthode, preuves</div><div><b>Écrire</b>WhatsApp en un clic, mots-clés AUDIT, LIGNE, DIAGNOSTIC</div><div><b>Qualifier</b>Besoin, interlocuteur, budget, délai</div><div><b>Signer</b>Proposition sous 48 h, relance à J+3 et J+7</div></div>
<p>Trois publications épinglées sur chaque profil : « Nos offres », « Notre méthode », et la meilleure preuve du moment. Chaque mot-clé déclenche une réponse type déjà rédigée, puis l'entrée du contact dans le tableau de prospection.</p>

<h2><small>8 · Amplification</small>Grandir sans publicité</h2>
<ul>{''.join(f'<li>{a}</li>' for a in amp)}</ul>

<h2 class="pb"><small>9 · Production</small>Tenir le rythme</h2>
<div class="box"><b>Par lots.</b> Une séance d'écriture le lundi pour la semaine, deux séances de tournage de 2 h (mardi et vendredi), montage au fil de l'eau.</div>
<div class="box"><b>Gabarits.</b> Carrousels, couvertures de vidéos et Stories dans la charte AM.Digital : on change le texte, pas la mise en page.</div>
<div class="box"><b>Déclinaison.</b> Une idée par jour, adaptée à chaque réseau : jamais le même fichier copié partout.</div>
<div class="box"><b>Validation.</b> Relecture de l'orthographe, du chiffre cité et de l'appel à l'action avant chaque publication ; accord écrit avant de montrer un client.</div>

<h2><small>10 · Pilotage</small>Ce qu'on mesure</h2>
{kpi}
<p>Règle de décision : beaucoup de vues et peu d'abonnés, on clarifie la bio ; beaucoup d'abonnés et peu de messages, on renforce les preuves et les offres ; beaucoup de messages et peu de contrats, on revoit la qualification et les propositions.</p>

<h2 class="keep"><small>11 · Feuille de route</small>90 jours</h2>
{road}
<div style="margin-top:16px;display:flex;align-items:center;gap:12px"><img src="{LOGO}" style="width:48px;border-radius:6px"><div style="font-size:9pt;color:#6e5a66">AM.Digital · Agence marketing digital · Abidjan · WhatsApp +225 01 71 95 45 23 · didimbro8@gmail.com</div></div>
</body></html>"""
open(f"{S}/render/strategie.html","w").write(H)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=["--allow-file-access-from-files"]); pg=b.new_page(); pg.goto(f"file://{S}/render/strategie.html"); pg.wait_for_timeout(500)
    pg.pdf(path=f"{S}/s2/AM-Digital_Strategie-de-contenu-digital.pdf",format="A4",print_background=True,margin={"top":"14mm","bottom":"14mm","left":"14mm","right":"14mm"}); b.close()
print("ok")
