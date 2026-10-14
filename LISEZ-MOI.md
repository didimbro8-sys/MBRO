# Site AM.Digital — guide du webmaster

Ce dossier contient votre site complet. Coût d'hébergement : 0 F CFA.
Vous publiez vos réalisations et vos articles vous-même, depuis un espace d'administration, sans écrire de code.

## Comment fonctionne le site

```
Vous (espace d'administration Pages CMS)
        │  « Enregistrer »
        ▼
GitHub (coffre-fort qui garde chaque version du site)
        │  mise à jour détectée automatiquement
        ▼
Cloudflare Pages (fabrique les pages et les sert au monde entier, HTTPS inclus)
        │  1 à 2 minutes plus tard
        ▼
https://am-digital.pages.dev  (votre site en ligne)
```

## Mise en place (une seule fois, environ 45 minutes)

### Étape 1 — Créer vos trois comptes gratuits
1. **GitHub** : https://github.com/signup
2. **Cloudflare** : https://dash.cloudflare.com/sign-up
3. **Web3Forms** (formulaire de contact) : https://web3forms.com, saisissez votre e-mail, vous recevez une clé.

Activez la double authentification (2FA) sur GitHub, Cloudflare et Gmail avant d'aller plus loin. C'est la protection n° 1 de votre site : si quelqu'un vole votre mot de passe GitHub, il peut modifier votre site.

### Étape 2 — Déposer le site sur GitHub
1. Sur GitHub : bouton **New repository**, nom `am-digital`, visibilité **Public**, puis **Create repository**.
2. Cliquez **uploading an existing file**, glissez tout le contenu de ce dossier (y compris le fichier `.pages.yml` et le dossier `src`), puis **Commit changes**.
   Astuce : sur Mac, appuyez sur Cmd + Maj + . pour afficher les fichiers qui commencent par un point.

### Étape 3 — Mettre le site en ligne avec Cloudflare Pages
1. Cloudflare → **Workers & Pages** → **Create** → onglet **Pages** → **Connect to Git** → autorisez GitHub → choisissez `am-digital`.
2. Réglages de construction :
   - Framework preset : **Eleventy**
   - Build command : `npm run build`
   - Build output directory : `_site`
3. **Save and Deploy**. Après 1 à 2 minutes, le site est en ligne sur `https://am-digital.pages.dev`.

Si l'adresse `am-digital` est déjà prise, Cloudflare en propose une autre. Notez-la, vous la saisirez à l'étape 4 dans « Adresse du site ».

### Étape 4 — Ouvrir votre espace d'administration
1. Allez sur https://app.pagescms.org et cliquez **Sign in with GitHub**.
2. Autorisez l'accès au dépôt `am-digital`, puis ouvrez-le.
3. Menu **Réglages du site** : remplacez `[Prénom Nom]` par votre nom, collez la clé Web3Forms, vérifiez l'adresse du site. **Save**.
4. Menu **Mon profil et parcours** : complétez les étiquettes jaunes (années, établissement). Ajoutez votre CV en PDF si vous le souhaitez.

Votre site est terminé. Chaque étiquette jaune visible sur le site signale une information à compléter : quand il n'en reste plus aucune, le site est prêt à être envoyé aux recruteurs.

## Au quotidien : publier une réalisation

1. https://app.pagescms.org → `am-digital` → **Réalisations** → **Add an entry**.
2. Remplissez les champs dans l'ordre. Ils suivent la grille d'un dossier de communication :
   - **Résumé** : une phrase, c'est elle que Google affiche.
   - **Contexte** : la situation de départ.
   - **Objectif** : chiffré et daté si possible (« Gagner 500 abonnés en 3 mois »).
   - **Dispositif** : une action par ligne.
   - **Résultats chiffrés** : un chiffre + ce qu'il mesure.
   - **Image de couverture** + sa description (obligatoire pour l'accessibilité et le référencement).
3. Cochez **Afficher sur la page d'accueil** pour vos 3 meilleures réalisations.
4. **Save**. La réalisation est en ligne 1 à 2 minutes plus tard, avec sa propre page.

Pour préparer une réalisation sans la montrer : décochez **Publier sur le site**. Elle reste en brouillon, invisible partout.

Autres réglages utiles d'une réalisation :
- **Ordre sur la page d'accueil** : 1 = affichée en premier. Les chiffres de la réalisation n° 1 apparaissent dans la bande « En chiffres » sous le titre du site.
- **Montrer sa galerie dans « Créations »** : la galerie s'affiche sur l'accueil, dans la section Créations.
- **Galerie** : chaque élément accepte une image, une vidéo MP4 (moins de 25 Mo) et un lien vers la publication TikTok, Instagram ou Facebook.

## Remplacer les visuels par leur version haute définition
Les visuels du site ont été récupérés depuis les aperçus Canva (environ 600 pixels de large). Ils sont nets sur la plupart des écrans, mais la version haute définition rend mieux sur les grands écrans :
1. Dans Canva : **Partager → Télécharger → JPG**, qualité 85, largeur 1600 px.
2. Dans l'administration, ouvrez la réalisation, cliquez sur l'image et remplacez-la par le fichier téléchargé. Gardez la même légende.

Pour le logo animé : téléchargez-le depuis Canva en **MP4**, puis ajoutez-le dans le champ **Vidéo** du premier élément de la galerie « Conceptions graphiques et motion design ».

## Travaux réalisés pour une organisation (OSEP)
Avant d'envoyer le site aux recruteurs, faites valider par votre ancien responsable à l'OSEP la publication de l'étude de cas et de ses chiffres. Si un élément doit rester interne, retirez-le de la réalisation ou mettez-la en brouillon.

## Publier une veille stratégique
Menu **Veille stratégique** de l'administration : une entrée par veille publiée sur Facebook ou Instagram.
- **Titre** : l'idée qui relie les signaux (« Quand l'IA décide qui on voit »).
- **Visuel publié** : le carrousel ou l'affiche tel qu'il est paru sur les réseaux, avec les liens Facebook et Instagram.
- **Signaux** (3 ou 4) : rubrique, titre, décryptage chiffré et daté, décision pour l'entreprise, source.
- **Analyse** (facultatif) : le fil conducteur de la veille.
La veille apparaît sur la page d'accueil (la plus récente) et dans le menu **Veille**.

## Publier un article dans le Journal
Même principe, menu **Journal (articles)**. Visez un article par mois : c'est ce qui fait progresser le site sur Google.

## Règles d'or du webmaster
| À faire | Pourquoi |
|---|---|
| Images en JPG ou WebP, moins de 500 Ko | Le site reste rapide sur mobile et en 3G |
| Toujours remplir la description de l'image | Accessibilité et référencement |
| Ne publier un visuel client qu'avec son accord écrit | Droit à l'image et confidentialité |
| Vérifier le site sur téléphone après chaque publication | La majorité des recruteurs le verront sur mobile |
| Un titre clair par réalisation (« Relance de la page Facebook de X ») | C'est ce que Google indexe |

## En cas de problème
- **Le site ne s'est pas mis à jour** : Cloudflare → Workers & Pages → `am-digital` → onglet **Deployments**. Une ligne rouge indique une erreur ; cliquez dessus pour lire le message.
- **Revenir en arrière** : dans ce même onglet, choisissez un déploiement précédent → **Rollback**. Le site revient à l'état d'avant en quelques secondes.
- **Un fichier modifié par erreur** : sur GitHub, chaque version est conservée (onglet **History** du fichier).

## Référencement : à faire une fois le site en ligne
1. **Google Search Console** (https://search.google.com/search-console) : ajoutez le site, puis soumettez `https://am-digital.pages.dev/sitemap.xml`.
2. **Bing Webmaster Tools** : importez depuis Search Console.
3. **Google Business Profile** : créez la fiche « AM.Digital » à Abidjan.
4. Mettez le lien du site dans la bio Facebook, Instagram, TikTok, LinkedIn et dans votre signature e-mail.

## Contenu du dossier (pour information)
| Élément | Rôle |
|---|---|
| `.pages.yml` | Définit les menus de l'espace d'administration |
| `src/realisations/` | Vos réalisations (un fichier par projet) |
| `src/journal/` | Vos articles |
| `src/_data/` | Réglages du site et profil |
| `src/assets/uploads/` | Images que vous envoyez depuis l'administration |
| `src/_includes/` | Gabarits des pages (ne pas modifier sans raison) |
| `src/_headers` | Boucliers de sécurité du navigateur |
| `eleventy.config.js`, `package.json` | Moteur de fabrication du site |
