# AM.DIGITAL — Studio IA Créatif

Fiche de production des shorts générés avec **Claude Opus 5.5** (orchestration), **FLUX** (images + vidéo), **ElevenLabs** (voix off + montage). Kling était prévu mais sans crédits : FLUX vidéo (gratuit) l'a remplacé.

> Les liens de fichiers signés (FLUX / ElevenLabs) expirent sous 24 h. Les identifiants ci-dessous restent valables pour retrouver les médias dans votre historique FLUX et dans le flow ElevenLabs.

**Flow ElevenLabs (tout le projet)** : https://elevenlabs.io/app/flows/Yo47089I488Qj2bIyX7u

---

## Short 1 — Promo parfum (15 s, 9:16) — ✅ terminé

| Étape | Outil | ID | Statut |
|---|---|---|---|
| Image produit (flacon ambre, bouchon or, marbre noir) | FLUX 3 Image | `e78f4072-143b-46ca-b335-c69551aaef0f` | ✅ |
| Animation 15 s, orbite lente + fumée dorée, musique ambiante | FLUX 3 Video (i2v) | `7d5be951-0ff2-4dd1-9f89-4e34d8754ca7` | ✅ |
| Voix off « Clémence – Advertising » (10,8 s) | ElevenLabs v4 | génération `HGoNRX27LQ0krHxNpYbb` | ✅ |
| Montage vidéo + voix (15,06 s, 704×1280) | ElevenLabs Composition | nœud « Short final 15s » `FoOkJPMZGnMUhnpzif90`, génération `lMk0AYqW6kzuH8Gh8Bs7` | ✅ |

**Script voix off**
> Il y a des parfums qu'on porte… et d'autres qui vous révèlent. Des notes d'ambre, une touche d'or, une signature inoubliable. Osez laisser votre empreinte. Disponible dès maintenant.

**Prompt image**
> Luxury amber glass perfume bottle with a gold cap standing on a black reflective marble pedestal, premium studio product photography, dramatic warm rim lighting, soft golden smoke swirling around, dark elegant background, shallow depth of field, ultra sharp, no text, no logo

---

## Short 2 — Making-of « processus créatif » + signature AM.digital (15 s, 9:16) — ⏳ montage à relancer

| Étape | Outil | ID | Statut |
|---|---|---|---|
| Brief, script, storyboard, prompts | Claude Opus 5.5 | — | ✅ |
| Image studio (écran « Claude Opus 5.5 → FLUX → ElevenLabs → Montage ») | FLUX 3 Image | `761301d5-0ba7-4ea5-800b-e7de1cab0d1e` | ✅ |
| Image produit (réutilisée) | FLUX 3 Image | `e78f4072-143b-46ca-b335-c69551aaef0f` | ✅ |
| Carton final logo or **AM.digital** + « Agence créative IA » | FLUX 3 Image | `2f6f0bf0-bcf5-422f-9920-d94b101f6c4e` | ✅ |
| Vidéo storyboard 15 s (studio 0 s → flacon 5 s → AM.digital 11,5–15 s), musique électro | FLUX 3 Video (i2v, 3 keyframes) | `5c73b7f0-d6ef-43cf-880f-90b8778460ea` | ✅ |
| Voix off dynamique « Gabriel – Confident French Ads » (14,3 s) | ElevenLabs v4 | nœud `5fyfwRAYEgwVijtP959C`, génération `w0I0YjRK77Fp8vug4c2W` | ✅ |
| Montage final vidéo + voix | ElevenLabs Composition (gratuit) | nœud « Making-of AM.digital 15s » `6rW6MoZa5DOeIJ94wsps` | ⏳ refusé (file gratuite saturée) — cliquer **Run** sur ce nœud |

**Script voix off (dynamique)**
> Un simple brief… et Claude Opus 5.5 prend les commandes ! FLUX crée l'image, l'anime en vidéo, ElevenLabs pose la voix, et le montage tombe tout seul. Une pub pro en quelques minutes ! Votre prochaine campagne ? AM point digital.

**Storyboard / timing**
| Temps | Image | Voix |
|---|---|---|
| 0–5 s | Studio, écran du workflow IA, push-in | « Un simple brief… Claude Opus 5.5 prend les commandes ! » |
| 5–11,5 s | Flacon de parfum, orbite énergique, flares | « FLUX crée l'image… le montage tombe tout seul. Une pub pro en quelques minutes ! » |
| 11,5–15 s | Logo or AM.digital, particules | « Votre prochaine campagne ? AM point digital. » |

**Prompt vidéo**
> Dynamic making-of commercial for an AI creative agency. Opens on the glowing studio monitor with the AI workflow dashboard, fast push-in into the screen; the perfume thumbnail on screen fills the frame and transforms into the real amber perfume bottle on black marble, golden smoke swirling, quick energetic camera orbit with light flares. Golden smoke then sweeps across the frame and reveals the gold AM.digital logo end card, which holds steady and sharp until the end with drifting gold particles. Keep all on-screen text crisp and unchanged. Audio: punchy modern upbeat electronic music with whoosh transitions, no voice, no dialogue.

---

## Coûts

| Poste | Coût |
|---|---|
| FLUX : 4 images + 2 vidéos | gratuit (bonus : 16 images et 3 vidéos restantes) |
| ElevenLabs : 2 voix off | 205 + 255 crédits (≈ 0,05 $) |
| ElevenLabs : montages | gratuit |
| Kling | non utilisé (crédits insuffisants) |

## À faire
1. Relancer le montage du Short 2 (nœud `6rW6MoZa5DOeIJ94wsps`, bouton **Run**).
2. Télécharger les deux MP4 finaux (liens valables 24 h après rendu).
3. Vérifier à l'œil la lisibilité des textes « Claude Opus 5.5 » et « AM.digital » générés par l'IA.
