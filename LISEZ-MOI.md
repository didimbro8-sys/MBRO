# Kit de production AM.Digital (campagne 15 oct – 14 nov 2026)
- mp/data.py : calendrier éditorial (93 publications, 07h/12h/18h heure d'Abidjan)
- gen/lib.py : gabarits visuels (Playwright) ; gen/dXX_YY.py : visuels par période ; gen/vXX_YY.py : vidéos (render/motion.py)
- Médias publiés : branche am-digital-medias (URLs raw.githubusercontent.com utilisées par Metricool)
- Restauration : copier fonts/woff2 -> scratchpad/fonts/package/files, fonts/*.ttf -> scratchpad/fonts/, logo -> scratchpad/ds/project/assets/Logos/
- Journal de publication : JOURNAL.md

## Format de la veille (consigne du 14 oct., précisée)
Sujet : tendances MONDIALES de la communication et du marketing digital + outils d'IA pour les communicants. Public : communicants, agences, entreprises, entrepreneurs, PME. PAS de veille interne.
Forme : UNE infographie 1080x1350 aux couleurs AM.Digital (modèle gen/infog2.py) : 4 signaux (3 tendances + outils IA du jour), chacun avec Décryptage, « Décision pour votre entreprise » et Source sur la créa. Publiée à 15:00 Africa/Abidjan sur FB+IG avec une description de post (résumé + sources). Vérifier chaque fait (date, chiffre, statut) avant publication.
Publication de la veille (consigne du 14 oct., 19h54) : publier IMMÉDIATEMENT dès que la veille est prête (peu importe l'heure), sans attendre l'aval du propriétaire, uniquement sur Facebook + Instagram AM.Digital. Contenu : infographie + description + sources AVEC liens. Une information importante (actualité directe) = infographie + lien + description, publiée tout de suite. Date sur l'infographie = date de publication.

## Canal « Internet » : site https://am-digital.pages.dev (consigne du 15 oct.)
Le site est le dépôt didimbro8-sys/mbro, branche main (Eleventy + Cloudflare Pages, déploiement auto 1-2 min après push).
- Chaque veille : ajouter src/veille/veille-AAAA-MM-JJ.md (même format que veille-2026-10-14.md : titre, date, resume, couverture dans src/assets/uploads/, liens FB/IG, 4 signaux rubrique/titre/decryptage/decision/source, analyse).
- Chaque jour : 1 article dans src/journal/<slug>.md (title, date, resume ≤180 car., couverture 1200x700 aux couleurs AM.Digital, corps markdown avec H2/H3, sources avec liens, appel WhatsApp DIAGNOSTIC).
- Toujours `npm ci && npm run build` sans erreur avant de pousser ; vérifier la page en ligne après déploiement.
Objectif mensuel : ~400 publications (FB ~120, IG ~120, TikTok ~100 quand le compte @am.digital204 sera relié dans Metricool, site ~60).

## Son des vidéos (décision du 15 oct. 2026)
- PAS de voix off (demande explicite). Musique seule.
- Musique : vidiq_compose (vidéo GitHub raw → vidiq_video_upload → compose avec piste afro-house ou trap-afrobeat, volume 1). Coût 1 crédit / 4 s ; crédits gratuits renouvelés le 31 de chaque mois.
- Gratuit : TikTok autoAddMusic=true fonctionne UNIQUEMENT pour les carrousels photo (pas les vidéos). Utiliser des carrousels photo TikTok quand les crédits manquent.
- Moteur motion design : gen/motion2.py (exemples dans gen/mo_batch1.py).
