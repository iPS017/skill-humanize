<!-- humanize:ignore-file -->
# Références inspirées des Human Interface Guidelines d'Apple

Ces règles reprennent les principes des Human Interface Guidelines (HIG) d'Apple, adaptés au web. Les valeurs Apple sont en points (pt) : sur le web, 1 pt correspond à 1 px CSS.

## Sommaire
1. Principes
2. Espacements et mise en page
3. Typographie
4. Couleurs
5. Boutons et contrôles
6. Rayons, ombres, matériaux
7. Animations
8. Raccourcis clavier
9. Focus et accessibilité
10. Tokens de départ

## 1. Principes

- **Clarté** : le texte se lit à toutes les tailles, les icônes sont précises, les ornements sont rares.
- **Déférence** : l'interface s'efface devant le contenu. Pas d'effet qui attire plus l'œil que le contenu lui-même.
- **Profondeur** : les couches (barres, feuilles, popovers) montrent la hiérarchie et aident à se repérer.
- **Cohérence** : un contrôle qui ressemble à un contrôle standard se comporte comme lui.

## 2. Espacements et mise en page

**Grille.** Toutes les marges, paddings et gaps sont des multiples de 4 px, et la plupart de 8 px. Échelle conseillée :

| Token | Valeur | Usage |
|---|---|---|
| `--space-1` | 4 px | icône et son libellé, espacement très serré |
| `--space-2` | 8 px | éléments d'un même groupe |
| `--space-3` | 12 px | padding vertical d'un bouton, entre deux boutons |
| `--space-4` | 16 px | marge latérale mobile, padding de carte compacte |
| `--space-6` | 24 px | padding de carte, entre deux groupes |
| `--space-8` | 32 px | entre un titre de section et son contenu |
| `--space-12` | 48 px | entre deux sections sur mobile |
| `--space-16` | 64 px | entre deux sections sur bureau |
| `--space-24` | 96 px | respiration autour d'un hero |

**Proximité.** L'espace exprime les relations : un libellé est plus proche de son champ que du champ suivant, un titre est plus proche de son paragraphe que de la section précédente. Si tout est espacé pareil, rien n'est groupé.

**Marges de page.** iOS utilise 16 pt de marge en largeur compacte et 20 pt en largeur normale. Sur le web : 16 px sous 600 px, 24 px jusqu'à 1024 px, puis un conteneur centré (1080 à 1280 px de large) avec au moins 32 px de marge.

**Largeur de lecture.** 60 à 75 caractères par ligne pour un paragraphe (`max-width: 65ch`).

**Alignement.** Un bord gauche commun pour le texte, les images et les boutons d'une même colonne. Le centrage est réservé aux blocs courts (titre de hero, état vide).

**Zones sûres.** Sur mobile, `padding: env(safe-area-inset-*)` pour les barres fixes, et rien d'interactif collé au bord bas de l'écran.

## 3. Typographie

**Police.** La police système (`font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`) donne SF Pro sur Apple. Une seule famille suffit, deux au maximum (une pour les titres, une pour le texte).

**Échelle.** Les styles de texte d'iOS (taille par défaut) servent de bonne base :

| Style | Taille | Graisse | Usage web |
|---|---|---|---|
| Large Title | 34 | Regular (Bold en titre de page) | h1 de page d'app |
| Title 1 | 28 | Regular | h1 / h2 |
| Title 2 | 22 | Regular | h2 / h3 |
| Title 3 | 20 | Regular | h3 |
| Headline | 17 | Semibold | titre de carte, libellé fort |
| Body | 17 | Regular | texte courant (16 à 17 px sur le web) |
| Callout | 16 | Regular | texte d'appui |
| Subheadline | 15 | Regular | sous-titre, métadonnée |
| Footnote | 13 | Regular | note, légende |
| Caption 1 | 12 | Regular | plus petit texte lisible |

Sur macOS le corps de texte est à 13 pt, mais c'est pour des apps de bureau denses : sur une page web, reste à 16 px minimum.

**Règles.**
- La hiérarchie passe par la taille et la graisse, pas par la couleur ni par des majuscules espacées.
- Interligne de 1.4 à 1.6 pour le texte courant, 1.1 à 1.2 pour les grands titres.
- Les grands titres ont un `letter-spacing` légèrement négatif (environ -0.02em), les petits textes un léger positif. Pas de `tracking-widest` en majuscules sur tous les sur-titres.
- Rien sous 12 px. Un texte qui devrait être plus petit est probablement inutile (voir `ai-tells.md`, section 8).
- Les tailles suivent les préférences de l'utilisateur : `rem`, pas de `px` figés sur le `html`.

## 4. Couleurs

Apple raisonne en couleurs **sémantiques**, pas en teintes. On nomme le rôle, la valeur change selon le thème.

| Rôle | Clair | Sombre |
|---|---|---|
| `--color-bg` | `#ffffff` | `#000000` ou `#1c1c1e` |
| `--color-bg-secondary` | `#f2f2f7` | `#1c1c1e` / `#2c2c2e` |
| `--color-bg-elevated` | `#ffffff` | `#2c2c2e` |
| `--color-text` | `#000000` / `#1d1d1f` | `#ffffff` / `#f5f5f7` |
| `--color-text-secondary` | `rgb(60 60 67 / .6)` | `rgb(235 235 245 / .6)` |
| `--color-separator` | `rgb(60 60 67 / .29)` | `rgb(84 84 88 / .6)` |
| `--color-accent` | la couleur de la marque | la même, un peu plus claire |
| `--color-destructive` | `#ff3b30` | `#ff453a` |

**Règles.**
- **Une couleur d'accent** (le « tint »), utilisée pour ce qui est interactif : liens, bouton principal, élément sélectionné, focus. Si tout est coloré, plus rien n'indique où cliquer.
- La couleur ne porte jamais seule une information : un état d'erreur a aussi un texte ou une icône.
- Contraste minimum 4.5:1 pour le texte courant, 3:1 pour le texte de 24 px et plus et pour les bordures de contrôles.
- En mode sombre, les surfaces surélevées sont plus claires que le fond, pas plus sombres, et l'accent est légèrement éclairci pour garder le contraste.

## 5. Boutons et contrôles

**Hiérarchie.** Apple propose quatre styles. Sur le web :

| Style | Rendu | Usage |
|---|---|---|
| Rempli (filled / prominent) | fond accent, texte blanc | l'action principale, **une seule par vue** |
| Teinté (tinted) | fond accent à 15 %, texte accent | action secondaire importante |
| Gris (gray / bordered) | fond neutre ou contour | actions secondaires |
| Texte (plain) | texte accent, sans fond | actions tertiaires, « Annuler », liens d'action |

**Taille.**
- Cible tactile de **44 × 44 px minimum** sur mobile, y compris pour un bouton icône. Le WCAG fixe 24 × 24 px en absolu, 44 reste la bonne valeur pour le tactile.
- Hauteur typique : 44 à 50 px pour un bouton principal mobile, 32 à 40 px sur bureau.
- Au moins 8 px entre deux cibles.

**Libellés.**
- Un verbe, ou verbe + objet : « Enregistrer », « Ajouter au panier », « Supprimer le projet ».
- Pas de « OK », « Oui », « Soumettre », « Cliquez ici », « En savoir plus » quand un libellé précis est possible.
- Majuscule au premier mot seulement en français (« Créer un compte »).
- Pas d'emoji, pas de flèche décorative. Un chevron est acceptable s'il indique une navigation.

**Comportements.**
- Dans un dialogue, l'action par défaut répond à Entrée, « Annuler » répond à Échap.
- Une action destructive est en rouge, n'est pas l'action par défaut, et demande confirmation si elle ne s'annule pas. Mieux : permettre l'annulation (« Projet supprimé. Annuler »).
- États visibles : repos, survol (sur pointeur uniquement, `@media (hover: hover)`), appui (légèrement assombri ou réduit à 0.97), focus, désactivé (opacité réduite, curseur normal, et `disabled` réel).
- Un bouton désactivé doit laisser comprendre pourquoi. Souvent il vaut mieux le laisser actif et afficher l'erreur au clic.

**Formulaires.** Un `label` visible au-dessus du champ (pas de placeholder qui sert de label), des champs de 44 px de haut sur mobile, `font-size` de 16 px minimum dans les champs (sinon Safari iOS zoome), les bons `type`, `inputmode` et `autocomplete`.

## 6. Rayons, ombres, matériaux

**Rayons.** Une petite échelle : 6 px (petits contrôles), 10 à 12 px (boutons, champs, cartes), 16 à 20 px (feuilles, grandes cartes). La forme pilule (`9999px`) pour les éléments vraiment pilules : tags, segmented controls, boutons isolés. Apple utilise des coins « continus » (courbure lissée) : sur le web, `border-radius` normal suffit, sans exagérer la valeur.

**Rayons concentriques.** Un élément arrondi dans un autre : `rayon intérieur = rayon extérieur - padding`. Une carte de 20 px de rayon et 8 px de padding contient une image de 12 px de rayon.

**Ombres.** Neutres, décalées vers le bas, discrètes, seulement sur ce qui flotte au-dessus du reste (menus, popovers, modales, éléments glissés). Jamais colorées.

**Matériaux (flou).** Le flou d'arrière-plan sert à montrer qu'une couche passe au-dessus d'un contenu qui bouge : barre de navigation collante, barre d'onglets, barre latérale, feuille modale. Le fond reste assez opaque pour que le texte soit lisible, et on prévoit `@supports not (backdrop-filter: blur())` avec un fond opaque.

## 7. Animations

- Une animation explique un changement : d'où vient un panneau, où part un élément supprimé, ce qui a été sélectionné.
- Durées courtes : 150 à 250 ms pour un retour de bouton ou un survol, 250 à 400 ms pour l'ouverture d'un panneau.
- Courbes : ease-out pour une entrée, ease-in pour une sortie, ou un ressort léger sans rebond visible (`cubic-bezier(.2, .8, .2, 1)`).
- Pas d'animation en boucle hors chargement. Pas d'animation qui bloque l'interaction.
- `@media (prefers-reduced-motion: reduce)` : les déplacements deviennent des fondus ou disparaissent.

## 8. Raccourcis clavier

**Modificateurs selon la plateforme.**
- Mac : ⌘ (Command) est le modificateur principal. ⇧ (Shift) et ⌥ (Option) servent de variantes. ⌃ (Control) est rarement utilisé seul.
- Windows et Linux : Ctrl remplace ⌘, Alt remplace ⌥.
- Sur le web, détecter la plateforme et lire le bon modificateur :

```ts
const isMac = /Mac|iPhone|iPad/.test(navigator.userAgentData?.platform ?? navigator.platform);

function isPrimaryModifier(event: KeyboardEvent) {
  return isMac ? event.metaKey && !event.ctrlKey : event.ctrlKey && !event.metaKey;
}
```

Tester seulement `metaKey` casse le raccourci sur Windows, tester seulement `ctrlKey` le rend faux sur Mac (⌃ y a d'autres usages).

**Raccourcis réservés.** Ne jamais les réaffecter dans une page ou une app web :

| Mac | Windows / Linux | Action |
|---|---|---|
| ⌘C, ⌘X, ⌘V | Ctrl+C, Ctrl+X, Ctrl+V | copier, couper, coller |
| ⌘Z, ⇧⌘Z | Ctrl+Z, Ctrl+Y / Ctrl+Shift+Z | annuler, rétablir |
| ⌘A | Ctrl+A | tout sélectionner |
| ⌘F, ⌘G | Ctrl+F, F3 | rechercher, suivant |
| ⌘T, ⌘N, ⌘W, ⇧⌘T | Ctrl+T, Ctrl+N, Ctrl+W | onglets et fenêtres du navigateur |
| ⌘L | Ctrl+L | barre d'adresse |
| ⌘R | Ctrl+R, F5 | recharger |
| ⌘Q, ⌘H, ⌘M | Alt+F4 | quitter, masquer, réduire |
| ⌘P | Ctrl+P | imprimer |
| ⌘+, ⌘-, ⌘0 | Ctrl+ +, Ctrl+ -, Ctrl+0 | zoom |
| ⌘Tab, ⌘Espace | Alt+Tab, Win | système |

Si l'app a ses propres équivalents (enregistrer, rechercher dans l'app), ils reprennent la même signification : ⌘S enregistre, ⌘F cherche dans le contenu de l'app, ⌘, ouvre les réglages, ⌘K ouvre une palette de commandes (convention web répandue, pas Apple).

**Raccourcis standards à respecter dans les composants.**
- Échap ferme le menu, la modale, la recherche, et annule l'édition en cours.
- Entrée valide l'action par défaut d'un dialogue ou d'un formulaire. ⌘Entrée (Ctrl+Entrée) envoie depuis un champ multiligne.
- Tab et ⇧Tab parcourent les éléments dans l'ordre visuel. Le focus reste piégé dans une modale ouverte, puis revient sur l'élément qui l'a ouverte.
- Flèches pour se déplacer dans une liste, un menu, des onglets, un groupe de boutons radio. Espace coche ou active.

**Raccourcis à une seule touche** (`/` pour chercher, `j`/`k`, `?` pour l'aide) :
- ils ne se déclenchent jamais quand le focus est dans un champ, une zone de texte ou un élément `contenteditable` ;
- ils peuvent être désactivés ou remappés (critère WCAG 2.1.4) ;
- on vérifie `event.isComposing` pour ne pas casser la saisie avec une méthode d'entrée (accents, japonais, chinois).

```ts
function isTyping(target: EventTarget | null) {
  return target instanceof HTMLElement &&
    (target.isContentEditable || target.closest("input, textarea, select") !== null);
}

window.addEventListener("keydown", (event) => {
  if (event.isComposing || isTyping(event.target)) return;
  if (event.key === "/") {
    event.preventDefault();
    searchInput.focus();
  }
});
```

Utiliser `event.key` pour la signification (lettre tapée, selon la disposition du clavier, important en AZERTY), `event.code` seulement pour une position physique (jeux, touches WASD).

**Affichage.**
- Les raccourcis sont visibles là où on cherche l'action : à droite d'un item de menu, dans l'infobulle d'un bouton, dans la palette de commandes, et dans une aide accessible par `?`.
- Sur Mac, symboles dans l'ordre Apple : ⌃ ⌥ ⇧ ⌘ puis la touche, sans séparateur (`⇧⌘K`). Sur Windows et Linux, noms en toutes lettres avec un `+` (`Ctrl+Shift+K`).
- La lettre est en majuscule (`⌘K`, pas `⌘k`), sans que ça implique ⇧.
- Utiliser `<kbd>` dans le HTML, avec un style discret (fond neutre, police de l'interface, pas de bordure en relief).
- Ne pas afficher « ⌘K » en dur : le libellé change selon la plateforme.
- Sur mobile et tablette sans clavier, les indications de raccourci sont masquées (`@media (hover: none)` ou détection d'un clavier physique).

**Ne pas abuser.** Un raccourci pour les actions fréquentes, pas pour tout. Pas de raccourci qui exige trois modificateurs. Pas de raccourci ⌥ seul + lettre sur Mac : ⌥ sert à taper des caractères (é, œ, ©).

## 9. Focus et accessibilité

- `:focus-visible` sur tous les éléments interactifs, avec un anneau de 2 à 3 px en couleur d'accent et un décalage (`outline-offset: 2px`). `outline: none` seulement si un autre indicateur visible le remplace.
- Ordre de tabulation = ordre visuel. Pas de `tabindex` positif.
- Les boutons icône ont un `aria-label`. Les icônes décoratives ont `aria-hidden="true"`.
- Rien n'apparaît seulement au survol : ce qui est révélé au survol l'est aussi au focus, et reste accessible au tactile.
- Respecter `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast` et le zoom du navigateur à 200 %.

## 10. Tokens de départ

À adapter au projet. Si le projet a déjà des tokens, utiliser les siens.

```css
:root {
  --space-1: 4px;  --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
  --space-6: 24px; --space-8: 32px;  --space-12: 48px; --space-16: 64px; --space-24: 96px;

  --radius-sm: 6px; --radius-md: 10px; --radius-lg: 16px;

  --text-xs: 0.75rem; --text-sm: 0.8125rem; --text-base: 1rem; --text-md: 1.0625rem;
  --text-lg: 1.25rem; --text-xl: 1.375rem;  --text-2xl: 1.75rem; --text-3xl: 2.125rem;

  --color-bg: #ffffff;
  --color-bg-secondary: #f2f2f7;
  --color-bg-elevated: #ffffff;
  --color-text: #1d1d1f;
  --color-text-secondary: rgb(60 60 67 / .6);
  --color-separator: rgb(60 60 67 / .29);
  --color-accent: #0071e3;
  --color-destructive: #ff3b30;

  --shadow-md: 0 4px 12px rgb(0 0 0 / .08);
  --ease-out: cubic-bezier(.2, .8, .2, 1);
  --duration-fast: 150ms; --duration-base: 250ms;

  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #000000;
    --color-bg-secondary: #1c1c1e;
    --color-bg-elevated: #2c2c2e;
    --color-text: #f5f5f7;
    --color-text-secondary: rgb(235 235 245 / .6);
    --color-separator: rgb(84 84 88 / .6);
    --color-accent: #2997ff;
    --color-destructive: #ff453a;
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

Le bleu `#0071e3` est l'accent d'apple.com, donné comme exemple : remplace-le par la couleur de la marque.
