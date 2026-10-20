# Routine « Veille stratégique AM.Digital » (3 fois par jour)

Objectif : à chaque passage, publier une veille fraîche (4 signaux du secteur com / marketing / réseaux sociaux / outils IA) sur Facebook (page AM.Digital), Instagram (amdigital204), TikTok (@am.digital204 si connecté) et le site am-digital.pages.dev. Minimum 3 veilles par jour. Toujours en français.

## 1. Préparer l'espace de travail
```bash
cd ~ && git clone -q --depth 1 -b am-digital-kit https://github.com/didimbro8-sys/MBRO.git kit
git clone -q https://github.com/didimbro8-sys/MBRO.git site   # branche main = site Eleventy (déploiement automatique au push)
pip install --break-system-packages -q playwright pillow 2>/dev/null
```
Lire `kit/veilles/` : les JSON des veilles déjà publiées. Ne jamais reprendre un sujet déjà traité.

## 2. Recherche (WebSearch / WebFetch)
- Uniquement des informations des 7 derniers jours (de préférence 48 h), avec date et source vérifiables (ouvrir l'article).
- Sujets : nouveautés Meta / Instagram / Facebook / TikTok / WhatsApp / LinkedIn / YouTube, publicité en ligne, SEO et recherche IA, outils IA de création, chiffres du digital en Afrique et en Côte d'Ivoire.
- Sources fiables : Social Media Today, TechCrunch, MarTech, Search Engine Land, The Verge, blogs officiels Meta / TikTok / Google, DataReportal, Digital Business Africa, Digitalmag.ci.
- Le signal 4 est toujours « Outils IA du jour ».

## 3. Rédaction (JSON)
Créer `kit/veilles/AAAA-MM-JJ-HHh.json` (heure d'Abidjan) au format :
```json
{"date_label":"21 octobre 2026","titre":"Titre court avec *mots en or*","sous_titre":"Tendances com & marketing, décryptées pour les PME",
 "signaux":[{"rubrique":"Plateforme · Thème","titre":"Titre avec *or*","decryptage":"≤ 120 caractères, faits datés",
   "decision":"≤ 75 caractères, action concrète pour une PME d'Abidjan","source":"Média, date"}]}
```
4 signaux exactement. Pas de chiffres inventés : chaque fait vient de l'article lu.

## 4. Visuel
```bash
cd ~/kit && python3 gen/veille_gen.py veilles/FICHIER.json /mnt/user-data/uploads/amd/AM-Digital_veille_FICHIER.jpg
```
Si le script répond « DEBORDEMENT », raccourcir les textes et relancer. Ouvrir l'image (Read) et vérifier : pied de page visible, pas de faute.

## 5. Publication Facebook + Instagram (Chrome de l'utilisateur, extension Claude in Chrome)
- Ouvrir `https://business.facebook.com/latest/composer?asset_id=398083733395827&business_id=398095106728023` (« Publier dans : AM.Digital et amdigital204 »).
- Le bouton « Ajouter une photo/vidéo » ouvre un sélecteur natif : avant de cliquer, injecter ce JS pour récupérer l'input :
  `HTMLInputElement.prototype.click` remplacé pour, si `type==='file'`, l'ajouter au DOM avec `aria-label='AMD upload'` au lieu d'ouvrir la fenêtre. Puis cliquer le bouton en JS, `find` « AMD upload file input », et `file_upload` avec le chemin sous `/mnt/user-data/uploads/amd/`.
- Texte : coller via `ClipboardEvent('paste')` sur `[contenteditable=true]` (le `type` coupe aux retours à la ligne).
- Cliquer « Publier ». Vérifier dans `.../latest/posts/published_posts?...` que le post apparaît.
- Légende : accroche « 🔎 La veille AM.Digital du JJ mois », le titre, les 4 signaux en une ligne chacun (1️⃣…4️⃣), le conseil pour les PME d'Abidjan, « 📌 Enregistrez et partagez », les sources, puis #VeilleAMDigital #MarketingDigital #RéseauxSociaux #Abidjan #CôteDIvoire.
- TikTok : seulement si `tiktok.com/profile` redirige vers `/@am.digital204` ; sinon ne rien publier sur TikTok (le compte personnel didi00253 ne doit jamais recevoir de contenu AM.Digital).
- Si Chrome / l'ordinateur ne répond pas : ne pas réessayer en boucle ; noter la veille dans `kit/veilles/A_PUBLIER.md` et la publier au passage suivant.

## 6. Site
Créer `site/src/veille/veille-AAAA-MM-JJ-HHh.md` sur le modèle de `veille-2026-10-20.md` (front matter : title, date, publie, resume, couverture, couverture_alt, lien_facebook/lien_instagram si connus, signaux, puis un paragraphe « fil conducteur » et les sources en liens). Copier l'image dans `site/src/assets/uploads/`. `npx --yes @11ty/eleventy --quiet` doit passer, puis commit + push sur main.

## 7. Clôture
- Commit + push du JSON (et de A_PUBLIER.md) sur la branche am-digital-kit.
- E-mail de compte rendu à didimbro8@gmail.com (Gmail) : titre de la veille, où elle est publiée, ce qui est en attente.

Règles permanentes : ne jamais saisir de mot de passe ; aucun service payant ; aucune publicité boostée ; publier seulement sur les comptes AM.Digital.
