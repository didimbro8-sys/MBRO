# « Au cœur de notre culture » — Teaser cinématographique 20 s (9:16)

Kit de production prêt à lancer, dérivé du *Plan de production v1.0 (5 nov. 2026)*. Version **teaser 20 s** choisie pour tenir dans le gratuit.

## ✅ Résultat — rendu le 5 nov. 2026 (après abonnement ElevenLabs)

| Élément | Détail |
|---|---|
| Vidéo finale | **20,06 s, 1280×704 (16:9)** — montage ElevenLabs, nœud « Au cœur de notre culture – teaser 20s » `JKeaVKqD8zilBC8Gj8UZ`, génération `pBodzRfHrZJdvvYK30QP` |
| Plan-séquence | FLUX 3 Video i2v, 10 keyframes, `84f662da-2a0f-4009-ac7d-a8df4c25684a` (dernière vidéo FLUX gratuite) |
| Images K01–K10 | ElevenLabs `flux-3-image`, 290,88 crédits chacune — sorties en **16:9** (le réglage par défaut du nœud a écrasé le 9:16 du prompt) |
| Voix off | David, 19,2 s, 281 crédits, nœud `N5vPImPqtZAlxuCsqBbK` |
| Total ElevenLabs | ≈ 3 190 crédits ; montage gratuit |

**Format** : 16:9 choisi pour ne pas re-payer les images. Pour la version 9:16 (TikTok/Reels), régler `aspect_ratio: 9:16` **dans les paramètres du nœud image** (pas seulement dans le prompt), puis une vidéo payante (FLUX ou Kling).

## Statut avant rendu (5 nov. 2026, matin)

| Ressource | État | Conséquence |
|---|---|---|
| FLUX — images gratuites | 0 / 20 (épuisé) | Images à faire ailleurs |
| FLUX — vidéos gratuites | **1 / 5 restante** (20 s max, jusqu'à 10 images clés) | Sert au plan-séquence |
| ElevenLabs — images (forfait gratuit) | **limite quotidienne atteinte** | Réessayer demain (≈ 290 crédits/image en FLUX 3) |
| ElevenLabs — voix / montage gratuits | file gratuite saturée | Réessayer dans quelques minutes |
| Kling | crédits insuffisants | Non utilisé |

⚠️ **Conformité** (plan §2) : forfaits gratuits = pas d'usage commercial. Diffuser comme **démonstration non commerciale** (mention « visuels générés par IA » + « elevenlabs.io ») ou faire le rendu final sur un forfait payant d'un mois.

## Ordre de lancement (demain)
1. Générer les 10 images ci-dessous (ElevenLabs, modèle `flux-3-image`, 1 variante chacune, 9:16) dans le flow `Yo47089I488Qj2bIyX7u`.
2. Contrôle qualité culturel de chaque image (grille §11) avant d'aller plus loin.
3. Voix off (ElevenLabs v4, voix **David** `qGwq3bbZd3aOEpsBcuc6`, accent ivoirien, 1 prise).
4. Vidéo FLUX `i2v`, 20 s, 9:16, `hd`, 10 keyframes aux timestamps ci-dessous (dernière vidéo gratuite).
5. Montage ElevenLabs « Composition » (gratuit) : vidéo + voix.

## Bloc de style (copié en tête de chaque prompt)
> Vertical 9:16 cinematic photorealistic film still, shot on ARRI Alexa with anamorphic lens, golden hour light, warm amber and deep aubergine color grade, atmospheric haze, subtle film grain, shallow depth of field, no text.

## Storyboard — 10 images clés

| # | Temps | Culture | Prompt (après le bloc de style) |
|---|---|---|---|
| K01 | 0 s | Ouverture | Aerial dawn over Côte d'Ivoire: golden sun rising above misty savanna flowing into lush rainforest and a shimmering lagoon, god rays. At the top, small refined gold serif title text "AU CŒUR DE NOTRE CULTURE", perfectly spelled. *(seule image avec texte, avec K10)* |
| K02 | 2 s | Nord – Sénoufo (Korhogo) | Senufo traditional dancers performing in a village near Korhogo in full raffia fiber costumes and carved wooden helmet masks, balafon musicians behind, red laterite dust, medium-wide shot, respectful documentary feel. |
| K03 | 4 s | Nord-Ouest – Malinké (Odienné) | An elderly Malinke master weaver in a white boubou at a traditional narrow-strip wooden loom in Odienné, cotton threads catching the light, Sudano-Sahelian mud-brick mosque with protruding wooden beams blurred behind, medium shot. |
| K04 | 6 s | Ouest – Dan (Man) | A Dan stilt dancer of the Man region towering on tall stilts in a colorful fiber and fabric costume with a traditional mask, misty green Dent de Man mountain behind, low-angle wide shot, majestic. |
| K05 | 8 s | Ouest – Bété (Gagnoa, Daloa) | A traditional Bété village ceremony: drummers playing talking drums, villagers in patterned cloth gathered in a circle, rainforest edge behind, medium-wide shot. |
| K06 | 10 s | Centre – Baoulé (Bouaké) | A proud Baoulé woman wearing a vibrant handwoven kita cloth in gold, indigo and red with traditional gold jewelry, handwoven strips drying behind her in a village courtyard, medium shot, regal. |
| K07 | 12 s | Est – Agni (Abengourou) | The Agni yam festival: a traditional Agni king in rich kente-style cloth and gold regalia under a large ornate ceremonial umbrella, dignitaries and festive procession, medium-wide shot, majestic and respectful. |
| K08 | 14 s | Sud – Lagune Ébrié | A vibrant market on the shore of the Ébrié lagoon in Abidjan: women in wax-print pagnes selling attiéké and grilled fish, wooden pirogues on the water, skyline faint behind. |
| K09 | 16 s | Abidjan contemporain | Stylish young Ivorians dancing coupé-décalé on a rooftop in modern wax-print outfits, Plateau skyline and lagoon glowing at blue hour, dynamic medium-wide shot. |
| K10 | 17,5–20 s | Signature | *(sans bloc de style)* Premium brand end card, deep aubergine background, soft golden light rays and drifting gold particles. Centered large lowercase logo "am" in glossy gold and white. Below, white sans-serif "@am.digital". Underneath, small gold text "Boostez votre présence. Démarquez-vous. Gagnez plus." All text perfectly spelled. |

## Prompt vidéo FLUX (i2v, 20 s, 9:16, hd, `generate_audio: true`)
> Cinematic one-take journey across Côte d'Ivoire for a premium cultural film. Each keyframe flows into the next through elegant match cuts: drifting golden dust, swirling fabric and light flares carry the camera from one region to the next. Slow, graceful dolly and crane moves, subtle slow motion on dancers, fabrics and smoke; faces and hands stay natural and undistorted. The final am.digital end card holds steady and sharp for the last 2.5 seconds with drifting gold particles; keep all on-screen text crisp and unchanged. Audio: epic cinematic score blending balafon, djembé and warm strings, building to a bold finish, no voice, no dialogue.

## Voix off (≈ 20 s, ElevenLabs v4, voix David)
> [warm] Au lever du jour… la Côte d'Ivoire s'éveille. Sénoufo, Malinké, Dan, Bété, Baoulé, Agni… Des savanes du nord aux lagunes d'Abidjan : mille héritages, un seul cœur. [proud] Notre culture nous rassemble. A.M. point digital. Boostez votre présence. Démarquez-vous. Gagnez plus.

**Prononciation à vérifier à l'écoute** : Sénoufo, Malinké, Bété, Baoulé, Agni (« a-nyi »), « A.M. point digital ».

## Contrôle qualité avant publication
- Relecture par une personne connaissant chaque culture représentée (tenues, masques, danses).
- Lisibilité de « AU CŒUR DE NOTRE CULTURE », « am », « @am.digital » et du slogan.
- Mentions obligatoires si diffusion gratuite : « visuels générés par IA », « elevenlabs.io ».
