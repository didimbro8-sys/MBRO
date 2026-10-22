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

## Son des vidéos (décision du 15 oct. 2026, REMPLACÉE le 22 oct. 2026)
- NOUVELLE RÈGLE (22 oct.) : voix off + fond sonore + sous-titres sur toutes les vidéos. Voir PROPOSITIONS_S44.md. L'ancienne règle « pas de voix off, musique seule » ne s'applique plus.
- Musique : vidiq_compose (vidéo GitHub raw → vidiq_video_upload → compose avec piste afro-house ou trap-afrobeat, volume 1). Coût 1 crédit / 4 s ; crédits gratuits renouvelés le 31 de chaque mois.
- Gratuit : TikTok autoAddMusic=true fonctionne UNIQUEMENT pour les carrousels photo (pas les vidéos). Utiliser des carrousels photo TikTok quand les crédits manquent.
- Moteur motion design : gen/motion2.py (exemples dans gen/mo_batch1.py).

## Vidéos « cinéma » (demande du 15 oct. 2026, 22h26) — RÈGLE POUR TOUTES LES VIDÉOS À VENIR
- Toutes les nouvelles vidéos utilisent gen/motion3.py (caméra 3D, sol néon, cubes 3D, typo lettre par lettre, flare, slam + onde de choc, transitions cube/iris/tranches/zoom, logo en pixels volants). Exemple : gen/v16_m3.py.
- Son : musique seule (pas de voix off). Par défaut musique afro-house synthétisée gen/music.py (gratuite, impacts calés sur les chiffres), normalisée à -14 LUFS ; ou pistes vidIQ si crédits.
- Avant publication : extraire 6-9 images de contrôle et vérifier lisibilité, chevauchements et transitions.
- Adobe (connecteur) : pas d'effets Premiere/After Effects disponibles ; option : importer la vidéo finie dans Firefly Video Editor (import-claude-motion-from-url) si le client veut retoucher.

## Dépôts GitHub connectés (20 oct. 2026, depuis les DM Instagram)
Clonés dans scratchpad/repos (git clone --depth 1 https://github.com/<dépôt>.git) :
- Instagram : Jakeschincariol/instagram-agent-skill (MIT) — 13 skills /ig-reel, /ig-viral, /ig-caption, /ig-carousel, /ig-story, /ig-profile, /ig-plan, /ig-human, /ig-comment, /ig-reply, /ig-dm, /ig-repurpose, /ig-audit + outils Python sans dépendance (hookscore.py, beats.py, caption.py, detect.py, humanize.py). Avant chaque légende : `python3 skills/ig-caption/caption.py fichier.txt` et `python3 skills/ig-human/detect.py fichier.txt`. Accroches de reels : `python3 skills/ig-reel/hookscore.py --hook "..."`.
- Motion / vidéo (envoyés par Simon De Lima) : heygen-com/hyperframes, AbubakrChan/product-launch-motion, charlie947/motion-graphics-skills, Barty-Bart/motion-graphics, cth9191/animate, whaleyxbt/claude-motion, motiondivision/motion, LottieFiles/motion-design-skill.
- Liens non lisibles sur le web (boutons ManyChat visibles seulement dans l'app mobile) : Henri ExplorIA (skills, lien GitHub « Claude », documents, guide montage), Louise Mourey (10 skills contenu, prompt), Titouan, Arms, Wissam, Dryxio (prompts, Buzzy), Wendy (Runway, code promo — pas GitHub).

## Vidéos avec voix off — moteur gen/motion4.py (22 oct. 2026)
- Rendu image par image d'un calque HTML/CSS animé (style After Effects), 1080x1920, 30 i/s ; voix off par scène, sous-titres mot à mot, musique gen/music.py abaissée sous la voix (sidechain), whooshs aux transitions, -14 LUFS.
- Voix de synthèse gratuite : Kokoro (voix française ff_siwis). Installation : `pip install --break-system-packages kokoro-onnx soundfile` puis télécharger dans ~/tts `kokoro-v1.0.onnx` (renommé kokoro.onnx) et `voices-v1.0.bin` depuis https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0.
- Prononciation : écrire « Am Digital », « ouatsape », « laïques » (likes), « boust » (boost), « Fèïsse-bouk » (Facebook), les nombres en lettres ; les sous-titres gardent l'orthographe correcte (champ `sub`).
- Vérification d'intelligibilité : Whisper base via sherpa-onnx (GitHub k2-fsa/sherpa-onnx, release asr-models), script dans le scratchpad (asr.py) ; planche de contrôle : gen/sheet.py.
- Voix du fondateur : champ `voice_file` d'une scène (fichier audio), remplace la synthèse.
- Échantillons validables : propositions/echantillons/ (vidéos A Signature, B Éditorial, C Pop ; visuels G4, G1, G11), scripts propositions/video_*.py et propositions/graphiques_3DA.py. Polices supplémentaires : fonts/extra (Playfair Display, Anton, licence OFL).
