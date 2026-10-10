---
name: humanize-ui
description: >-
  Review et nettoyage du rendu visuel d'une interface pour retirer le style « généré par IA » : néons et glows,
  dégradés de fond inutiles, texte en dégradé, glassmorphism partout, taches floues décoratives, palette violet/indigo,
  animations infinies, boutons tous identiques, cartes en grille de trois avec icône, emojis dans l'interface.
  Corrige les espacements, la hiérarchie des boutons et les raccourcis clavier en suivant les Human Interface
  Guidelines d'Apple (grille de 4/8 px, cibles de 44 px, un seul bouton principal, modificateurs ⌘/Ctrl selon la
  plateforme, raccourcis standard non détournés). À utiliser pour toute page, landing, dashboard ou composant qu'on
  livre, dès que l'utilisateur demande une review de design ou d'un rendu, trouve que son site « fait IA » ou
  « template », ou parle de boutons, d'espacements, de raccourcis clavier ou de style Apple. Use when reviewing a
  rendered UI, removing AI-looking visuals, or fixing spacing, buttons and keyboard shortcuts Apple-style.
---
<!-- humanize:ignore-file -->

# Humanize UI

Les interfaces générées se ressemblent toutes : fond sombre avec un dégradé violet vers bleu, titre en texte dégradé, cartes en verre dépoli, halo néon autour des boutons, trois cartes avec une icône dans un carré arrondi, badge « ✨ New » au-dessus du titre. Un visiteur reconnaît ce gabarit en une seconde et en conclut que personne n'a vraiment pensé la page. Ce skill sert à faire la review d'un rendu, à retirer ces marqueurs et à remettre de l'ordre dans les espacements, les boutons et les raccourcis, en prenant les Human Interface Guidelines d'Apple comme référence.

La référence Apple ne veut pas dire copier macOS. Elle veut dire : la couleur et les effets servent à quelque chose, l'espace est régulier, la hiérarchie se lit sans effort, chaque contrôle se comporte comme l'utilisateur s'y attend.

## Quand l'appliquer

- Quand tu écris une interface (page, composant, dashboard) : applique les règles pendant l'écriture, pas après.
- Quand l'utilisateur demande une review de design, d'une page, d'un rendu ou d'une capture.
- Quand il trouve que son site « fait IA », « fait template », « fait Dribbble 2023 », ou qu'il veut un rendu plus sobre ou plus « Apple ».

Pour le texte de l'interface et la propreté du code, le skill `humanize` s'applique en plus de celui-ci.

## Méthode de review

1. **Regarde le rendu, pas seulement le code.** Si tu as un navigateur (outils DevTools, Playwright, capture d'écran), ouvre la page en 1440 px, 768 px et 375 px de large, en thème clair et sombre si les deux existent. Si l'utilisateur fournit une capture, travaille dessus. Sans rendu disponible, lis le CSS et le markup et dis que la review est faite sur le code seul.
2. **Lis les références** :
   - `references/ai-tells.md` : catalogue des effets « IA » avec la correction de chacun ;
   - `references/apple.md` : espacements, typographie, boutons, couleurs, matériaux, animations, raccourcis clavier.
3. **Repère les conventions du projet** : design tokens, variables CSS, config Tailwind, librairie de composants. Les corrections passent par ces tokens. Si le projet n'en a pas, propose une petite échelle (espacements, rayons, couleurs) au lieu de corriger valeur par valeur.
4. **Lance le scanner** si tu as un terminal :
   ```bash
   python scripts/scan_ui.py src/
   python scripts/scan_ui.py --all src/   # ajoute les signaux faibles
   ```
   Il trouve les motifs dans le code (glows, dégradés, texte dégradé, blur décoratif, focus supprimé, espacements hors grille, raccourcis mal gérés). Il ne voit pas la composition, la hiérarchie ni l'équilibre de la page, ça reste ton travail sur le rendu.
5. **Écris la review** dans ce format, du plus grave au moins grave :
   ```
   ## Review du rendu

   ### À corriger
   1. Hero : dégradé violet → bleu en fond et titre en texte dégradé (hero.css:12, hero.css:31).
      Fond uni `--color-bg`, titre en `--color-text`. La couleur d'accent reste sur le bouton principal.
   2. ...

   ### À améliorer
   ...

   ### Déjà bien
   - (deux ou trois points au maximum, seulement s'ils sont vrais)
   ```
   Chaque point donne l'endroit (section visible et fichier:ligne), ce qui ne va pas, et la correction précise avec les valeurs. Pas de « pourrait être amélioré », pas de note sur 10.
6. **Corrige** si l'utilisateur le demande ou si tu écris toi-même l'interface. Revérifie le rendu après correction, aux trois largeurs.

## Règles à garder en tête en permanence

### Ce qu'on retire

- **Néons et glows** : `box-shadow: 0 0 40px` coloré, `text-shadow` lumineux, `drop-shadow` violet, bordure qui brille au survol. Une ombre sert à montrer qu'un élément est au-dessus d'un autre, elle est neutre, courte et décalée vers le bas.
- **Dégradés de fond décoratifs** : fond de page ou de section en dégradé coloré, `radial-gradient` qui fait une lueur, maillage de couleurs, bordure en dégradé animée. Un fond est uni. Un dégradé reste acceptable s'il a une fonction : voile sombre pour lire un texte sur une photo, fondu en bord de zone qui défile.
- **Texte en dégradé** (`background-clip: text`) : le titre prend la couleur du texte. Si un mot doit ressortir, la graisse ou la taille suffisent.
- **Glassmorphism partout** : `backdrop-filter: blur` sur des cartes posées sur un fond uni ne sert à rien. Le flou est réservé aux barres qui passent au-dessus d'un contenu qui défile (barre de navigation collante, barre d'outils).
- **Taches floues décoratives** : `div` en position absolue avec `blur(100px)` et une couleur vive derrière le hero.
- **Palette violet/indigo/rose par défaut** (`#8b5cf6`, `#6366f1`, `#ec4899`, `purple-500`, `indigo-600`) quand elle ne vient pas de la marque. Une seule couleur d'accent, choisie pour le projet.
- **Animations infinies** : `animate-pulse`, `animate-bounce`, badge qui clignote, flèche qui sautille, gradient qui tourne. Une animation répond à une action ou montre un chargement, puis s'arrête.
- **Gabarits de composition** : badge « ✨ Nouveau » au-dessus du titre, trois cartes identiques avec une icône dans un carré arrondi coloré, section de logos « Ils nous font confiance » sans vrais clients, chiffres ronds inventés (« 10k+ utilisateurs »), témoignages génériques.
- **Emojis et icônes décoratives** dans les titres, les boutons et les listes.
- **Textes inutiles et mal placés**, souvent en tout petit, en majuscules espacées ou en police mono : heure locale ou fuseau horaire (« Paris, 14:32 GMT+2 »), coordonnées GPS, « Disponible pour missions » avec un point vert qui clignote, « Scroll pour explorer », numéros de section (« 01 / Services », « [ 02 ] »), numéro de version ou « Build 2026 » dans un portfolio, « Est. 2024 », « All systems operational », « Made with ❤️ », compteurs de visiteurs, mentions « Index », « Sélection », « Archive » posées au-dessus de titres qui disent déjà la même chose. Pour chaque petit texte, pose la question : est-ce qu'un visiteur en a besoin pour comprendre ou agir ? Si non, il part. Si oui, il est lisible (12 px au moins, contraste suffisant) et placé là où on le cherche.

### Ce qu'on applique (inspiré des Human Interface Guidelines)

- **Espacements sur une grille de 4 px**, en pratique une échelle courte : 4, 8, 12, 16, 24, 32, 48, 64, 96. Les éléments liés sont proches, les groupes sont séparés par un pas nettement plus grand. Marges latérales d'au moins 16 px sur mobile, 20 à 24 px sur tablette.
- **Cibles tactiles de 44 × 44 px minimum** sur mobile, même si l'icône dessinée fait 20 px (le padding compte).
- **Un seul bouton principal par vue** (rempli, couleur d'accent). Les autres actions sont secondaires (contour ou fond neutre) ou en texte. Le libellé est un verbe qui dit ce qui va se passer (« Enregistrer », « Envoyer le message »), pas « OK » ni « Cliquez ici ». Une action destructive est en rouge et demande confirmation si elle ne s'annule pas.
- **Typographie** : une famille (la police système va très bien), une échelle limitée (par exemple 13, 15, 17, 22, 28, 34 px), la hiérarchie par la taille et la graisse plutôt que par la couleur. Corps de texte à 16 ou 17 px sur le web, lignes de 60 à 75 caractères.
- **Couleur sémantique** : texte principal, texte secondaire, fond, fond surélevé, séparateur, accent, rouge pour la destruction. Le mode sombre n'est pas une inversion : les surfaces surélevées deviennent plus claires, l'accent est légèrement éclairci.
- **Rayons concentriques** : un élément arrondi dans un autre a un rayon égal au rayon extérieur moins le padding. Pas un `rounded-3xl` uniforme sur tout.
- **Animations courtes et utiles** (150 à 300 ms, une courbe de type ressort ou ease-out), et respect de `prefers-reduced-motion`.
- **Focus visible** sur chaque élément interactif (`:focus-visible`). Jamais `outline: none` sans remplacement.
- **Raccourcis clavier** : ⌘ sur Mac, Ctrl sur Windows et Linux, détecté à l'exécution. On ne détourne pas les raccourcis du système et du navigateur (⌘C, ⌘V, ⌘Z, ⌘W, ⌘T, ⌘L, ⌘R, ⌘Q). Échap ferme, Entrée valide l'action par défaut. Un raccourci à une seule touche ne se déclenche pas pendant la saisie dans un champ. Les raccourcis sont affichés dans les menus et les infobulles avec les symboles dans l'ordre ⌃ ⌥ ⇧ ⌘. Détail complet dans `references/apple.md`.

## Ce qu'il ne faut pas toucher

- **L'identité de la marque.** Si le violet ou un dégradé fait partie de la charte (logo, guide de marque, demande explicite), on le garde et on le limite à sa place au lieu de le supprimer. Demande en cas de doute.
- Le contenu, les textes et les images fournis par l'utilisateur.
- Le comportement : une correction visuelle ne casse ni la navigation, ni les formulaires, ni l'accessibilité.
- Un effet clairement voulu et maîtrisé (un site de jeu vidéo ou de musique électronique peut assumer le néon). La question est toujours : est-ce un choix, ou le réglage par défaut d'un générateur ?
