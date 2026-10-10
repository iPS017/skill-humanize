<!-- humanize:ignore-file -->
# Marqueurs visuels d'une interface générée

## Sommaire
1. Comment juger un effet
2. Lumière : néons, glows, ombres colorées
3. Dégradés
4. Verre dépoli et flou
5. Couleurs
6. Animations
7. Composition et gabarits
8. Textes inutiles
9. Boutons
10. Détails de finition
11. Exemples avant/après

## 1. Comment juger un effet

Un effet visuel est légitime quand on peut dire à quoi il sert : montrer une profondeur, attirer l'œil sur l'action principale, signaler un état, rendre un texte lisible sur une image. S'il est là « pour faire moderne », c'est un réglage par défaut et il part.

Deux questions pour chaque élément :
- Si je l'enlève, est-ce qu'un visiteur perd une information ou une capacité ?
- Est-ce que ce choix vient du projet (marque, contenu, public) ou de n'importe quel template ?

## 2. Lumière : néons, glows, ombres colorées

À retirer :
- `box-shadow: 0 0 20px rgba(139, 92, 246, .5)` et toutes les ombres sans décalage avec une couleur vive ;
- plusieurs ombres colorées empilées pour faire un halo ;
- `text-shadow` lumineux sur les titres ;
- `filter: drop-shadow(0 0 8px #a855f7)` sur les icônes ;
- bordures qui « s'allument » au survol, bordures en dégradé animé (`conic-gradient` qui tourne) ;
- en Tailwind : `shadow-purple-500/50`, `shadow-[0_0_30px_...]`, `ring-violet-500/30` décoratif.

Ce qui remplace : une ombre neutre, décalée vers le bas, avec peu d'opacité, seulement sur ce qui flotte (menu, popover, modale, carte au survol si elle est cliquable).

```css
--shadow-sm: 0 1px 2px rgb(0 0 0 / .06);
--shadow-md: 0 4px 12px rgb(0 0 0 / .08);
--shadow-lg: 0 12px 32px rgb(0 0 0 / .12);
```

En mode sombre, les ombres se voient peu : la profondeur se montre par une surface un peu plus claire et un séparateur fin.

## 3. Dégradés

À retirer :
- fond de page ou de hero en dégradé violet vers bleu, rose vers orange, « aurora », mesh gradient ;
- `radial-gradient` coloré qui fait une lueur derrière le titre ;
- dégradé sur chaque carte, sur chaque bouton, sur les icônes ;
- texte en dégradé (`background-clip: text`, `bg-clip-text text-transparent`) ;
- grille de points ou de lignes avec masque en dégradé derrière le hero, quand elle n'apporte rien.

Dégradés acceptables :
- un voile pour lire un texte sur une photo (`linear-gradient(to top, rgb(0 0 0 / .6), transparent)`) ;
- un fondu en bord de zone qui défile horizontalement ;
- un dégradé très léger, presque invisible, dans une teinte unique, s'il appartient à la marque ;
- une illustration ou une image qui contient naturellement des dégradés.

Ce qui remplace : un fond uni (`--color-bg`), une surface légèrement différente pour séparer une section (`--color-bg-secondary`), et l'accent réservé aux éléments interactifs.

## 4. Verre dépoli et flou

À retirer :
- `backdrop-filter: blur()` sur des cartes posées sur un fond uni (le flou ne floute rien) ;
- cartes semi-transparentes avec bordure blanche à 10 % empilées partout ;
- taches de couleur floues en position absolue (`blur-3xl`, `filter: blur(120px)`) derrière le contenu.

Acceptable : une barre de navigation ou d'outils collante qui passe au-dessus d'un contenu qui défile, avec un fond assez opaque pour garder le texte lisible. C'est l'usage des « matériaux » chez Apple : le flou indique qu'une couche est au-dessus d'une autre.

## 5. Couleurs

Signaux d'une palette par défaut :
- violet, indigo, fuchsia, cyan (`#8b5cf6`, `#7c3aed`, `#a855f7`, `#6366f1`, `#4f46e5`, `#ec4899`, `#d946ef`, `#06b6d4`, `purple-500`, `violet-600`, `indigo-500`) sans lien avec la marque ;
- plusieurs couleurs d'accent qui se disputent l'attention ;
- fond quasi noir `#0a0a0a` avec texte gris très clair et accent violet, le combo le plus courant ;
- couleur posée sur les icônes, les titres, les badges et les bordures en même temps.

Ce qui remplace : une palette sémantique (voir `apple.md`), une seule couleur d'accent qui vient du projet, utilisée sur les liens, le bouton principal, l'état sélectionné et le focus. Le reste est en neutres.

## 6. Animations

À retirer :
- `animate-pulse`, `animate-bounce`, `animate-ping` décoratifs, `animation: ... infinite` sur autre chose qu'un indicateur de chargement ;
- apparition en fondu et glissement de chaque bloc au scroll, avec un délai en cascade ;
- texte qui se tape lettre par lettre, compteurs qui défilent jusqu'à un chiffre ;
- curseur personnalisé qui suit la souris avec un halo ;
- effets 3D au survol (tilt) sur des cartes qui ne sont pas des objets.

Acceptable : une transition courte en réponse à une action (ouverture de menu, changement d'onglet, survol d'un bouton), un indicateur de chargement, une animation qui explique un changement d'état. Toujours avec `@media (prefers-reduced-motion: reduce)`.

## 7. Composition et gabarits

Le gabarit de landing générée, dans l'ordre :
1. badge pilule « ✨ Nouveau : ... → » au-dessus du titre ;
2. titre de deux lignes dont la fin est en dégradé ;
3. sous-titre gris centré ;
4. deux boutons côte à côte de même poids ;
5. capture de l'app inclinée avec un halo violet ;
6. bandeau de logos en gris ;
7. trois ou six cartes « Features » identiques avec une icône dans un carré coloré ;
8. section de chiffres ronds ;
9. témoignages avec avatars générés ;
10. trois offres tarifaires dont celle du milieu « Populaire » avec un glow ;
11. FAQ en accordéon, gros CTA final en dégradé.

Il ne s'agit pas d'interdire chaque section, mais de vérifier qu'elle a un vrai contenu. Une section sans contenu réel part. Les cartes identiques peuvent devenir une liste, un tableau, ou une vraie démonstration. Tout centrer par défaut fatigue : un texte long s'aligne à gauche.

## 8. Textes inutiles

C'est le marqueur le plus discret et l'un des plus fréquents. Le générateur remplit les coins vides avec de petits textes qui donnent un air « éditorial » ou « tech » sans rien dire.

À retirer :
- **heure locale, fuseau, date du jour** affichés en direct (« Paris, 14:32 », « Local time 09:41 GMT+1 », horloge dans le header ou le footer) ;
- **coordonnées GPS** (« 48.8566° N, 2.3522° E ») ;
- **statut décoratif** : « Disponible pour missions » avec un point vert qui pulse, « All systems operational », « Currently building... » ;
- **numéros de section** et étiquettes techniques : « 01 / Services », « [ 02 ] », « § 03 », « Index », « (Sélection) », « Section 4 of 7 » ;
- **méta inventée** : « v2.4.1 », « Build 2026 », « Est. 2024 », « Since 2019 » sur un site personnel, « Ref. 0042 », « Fig. 1 » sans figure ;
- **instructions évidentes** : « Scroll pour explorer », « Cliquez pour en savoir plus », flèche « ↓ Scroll » ;
- **signatures** : « Made with ❤️ in Paris », « Designed & built by », « Powered by Next.js » ;
- **compteurs** de visiteurs, nombre de lignes de code, « 1 247 tasses de café » ;
- **étiquette qui répète le titre** : un « À propos » en petites majuscules au-dessus d'un titre « À propos de moi » ;
- **marqueurs de mode** : « Dark mode on », « EN / FR » quand le site n'a qu'une langue.

Le style qui les trahit : `font-size` de 10 ou 11 px, `text-transform: uppercase`, `letter-spacing` large, police mono, gris clair à faible contraste, positionnés dans un coin ou en haut de chaque section.

Règle : chaque texte doit aider à comprendre ou à agir. Un texte utile mais petit (mention légale, légende) reste lisible : 12 px minimum, contraste d'au moins 4.5:1 pour du texte de cette taille, placé à côté de ce qu'il décrit. Le copyright en pied de page est utile, il reste, sans « All rights reserved » obligatoire.

## 9. Boutons

Problèmes fréquents :
- tous les boutons en dégradé avec glow, au même poids ;
- deux boutons principaux côte à côte (« Commencer » et « Voir la démo » remplis tous les deux) ;
- flèche ou emoji dans chaque libellé (« Commencer → », « 🚀 Lancer ») ;
- libellés vagues : « En savoir plus », « Cliquez ici », « Découvrir », « Soumettre » ;
- `scale(1.05)` au survol sur tout ;
- forme pilule partout, y compris dans les formulaires d'une app ;
- bouton icône sans libellé accessible.

Ce qui remplace : voir la hiérarchie des boutons dans `apple.md`, section 5.

## 10. Détails de finition

- `rounded-2xl` ou `rounded-3xl` partout, sans rayons concentriques ;
- bordures `border-white/10` sur chaque bloc ;
- icônes Lucide ou Heroicons à côté de chaque titre, de chaque item de liste ;
- texte gris sur gris sous le contraste requis (`text-gray-500` sur `bg-gray-900`) ;
- `outline: none` ou `focus:outline-none` sans remplacement ;
- espacements irréguliers (13 px, 18 px, 22 px, 30 px) au lieu d'une échelle ;
- largeur de texte non limitée (paragraphes de 150 caractères sur grand écran).

## 11. Exemples avant/après

**Hero**

Avant :
```html
<section class="relative overflow-hidden bg-gradient-to-br from-purple-900 via-indigo-900 to-black py-32">
  <div class="absolute -top-40 left-1/2 h-96 w-96 rounded-full bg-purple-500 opacity-30 blur-3xl"></div>
  <p class="font-mono text-[10px] uppercase tracking-[0.3em] text-white/40">01 / Intro · Paris 14:32</p>
  <span class="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs backdrop-blur">✨ Nouveau : la v2 est là →</span>
  <h1 class="text-6xl font-bold">
    Créez des sites <span class="bg-gradient-to-r from-pink-500 to-violet-500 bg-clip-text text-transparent">extraordinaires</span>
  </h1>
  <button class="rounded-full bg-gradient-to-r from-purple-500 to-pink-500 px-8 py-4 shadow-[0_0_40px_rgba(168,85,247,0.5)] animate-pulse">
    Commencer 🚀
  </button>
  <button class="rounded-full bg-gradient-to-r from-indigo-500 to-cyan-500 px-8 py-4">Voir la démo →</button>
</section>
```

Après :
```html
<section class="hero">
  <h1 class="hero__title">Créez le site de votre atelier en une après-midi</h1>
  <p class="hero__lead">Choisissez une mise en page, ajoutez vos photos, publiez. Pas de code.</p>
  <div class="hero__actions">
    <a class="button button--primary" href="/inscription">Créer mon site</a>
    <a class="button button--plain" href="/exemples">Voir des exemples</a>
  </div>
</section>
```
```css
.hero { padding-block: var(--space-24) var(--space-16); background: var(--color-bg); }
.hero__title { font-size: clamp(2.25rem, 5vw, 3.5rem); line-height: 1.1; max-width: 18ch; color: var(--color-text); }
.hero__lead { margin-top: var(--space-4); max-width: 52ch; color: var(--color-text-secondary); }
.hero__actions { display: flex; gap: var(--space-3); margin-top: var(--space-8); }
```
Le fond est uni, la tache floue, le badge et la ligne « 01 / Intro · Paris 14:32 » partent, le titre dit ce que fait le produit au lieu d'un adjectif, un seul bouton principal, le second est en texte.

**Carte**

Avant :
```css
.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 0 30px rgba(99, 102, 241, 0.3);
}
.card:hover { transform: scale(1.05) rotate(1deg); box-shadow: 0 0 60px rgba(99, 102, 241, 0.6); }
```

Après :
```css
.card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-separator);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}
.card:has(a:hover) { box-shadow: var(--shadow-md); }
```
