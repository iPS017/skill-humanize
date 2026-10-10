<!-- humanize:ignore-file -->
# Code

## Sommaire
1. Priorité aux conventions du projet
2. Commentaires
3. Nommage des identifiants
4. Nommage des fichiers et dossiers
5. HTML et JSX
6. CSS et classes
7. Autres traces de génération
8. Commits, PR, README
9. Exemples avant/après

## 1. Priorité aux conventions du projet

Avant d'écrire ou de renommer quoi que ce soit, regarde :
- comment sont nommés les fichiers existants (kebab-case, PascalCase pour les composants, camelCase) ;
- la méthode CSS (BEM, CSS Modules, Tailwind, styled-components) ;
- la langue des identifiants (presque toujours l'anglais) ;
- la config du linter et du formateur (`.eslintrc`, `biome.json`, `.prettierrc`, `.editorconfig`) ;
- le format des commits dans `git log`.

Si le projet a une règle, elle gagne. Les règles ci-dessous servent quand il n'y en a pas.

## 2. Commentaires

Par défaut, pas de commentaire. Le code doit se lire grâce aux noms et à la structure.

À supprimer :
- les commentaires qui répètent la ligne (`// Set loading to true`, `# Increment counter`) ;
- les titres de section (`// ===== STATE =====`, `{/* Hero Section */}`, `<!-- Footer -->`) ;
- les commentaires qui expliquent un import, un export, un `return` ;
- les `// TODO: implement`, `// Add your logic here`, `// Rest of the code...` ;
- les commentaires en emoji ou en ton de tutoriel (`// 🎉 Now we can use it!`, `// Let's create our function`) ;
- le code commenté laissé « au cas où ».

À garder :
- licences et en-têtes légaux ;
- directives d'outils : `eslint-disable-next-line`, `@ts-expect-error`, `prettier-ignore`, `biome-ignore`, `noqa`, `type: ignore`, `istanbul ignore`, `webpackChunkName` ;
- la doc d'une API publique (JSDoc, docstrings) si le projet en écrit ailleurs ;
- un « pourquoi » qu'on ne devine pas en lisant : contournement d'un bug Safari, contrainte métier, lien vers une issue.

Un commentaire gardé est court, au présent, sans ponctuation décorative : `// Safari ignore scroll-padding sur html, voir #142`.

## 3. Nommage des identifiants

- **Variables** : ce qu'elles contiennent. `projects`, `activeProject`, `scrollProgress`. Pas `data`, `data2`, `temp`, `tmp`, `res`, `result`, `obj`, `item`, `value`, `info`, `stuff`, `thing`, `myVar`, `newData`.
- **Fonctions** : verbe + objet. `fetchProjects`, `formatDate`, `toggleMenu`. Pas `handle`, `doStuff`, `process`, `helper`, `func`.
- **Booléens** : `is`, `has`, `should`, `can`. `isMenuOpen`, `hasConsent`.
- **Handlers** : `handleSubmit` dans le composant, `onSubmit` pour la prop. Jamais `handleClick2` ou `handleClickNew`.
- **Composants React** : PascalCase, un nom métier. `ProjectCard`, `ContactForm`. Pas `MyComponent`, `Wrapper`, `CustomButton`, `NewHero`.
- **Constantes** : `SCREAMING_SNAKE_CASE` seulement pour de vraies constantes de config (`MAX_UPLOAD_SIZE`).
- **Pas de suffixes de version** : `v2`, `new`, `old`, `final`, `fixed`, `updated`, `copy`, `temp`.
- **Pas de type dans le nom** : `projectsArray`, `userObject`, `nameString`.
- **Index de boucle** : `i` est accepté pour une boucle courte, sinon un vrai nom (`project` dans `projects.map(project => …)`).

## 4. Nommage des fichiers et dossiers

- Suivre la convention du projet. Sans convention : fichiers en kebab-case (`project-card.tsx`, `use-scroll-progress.ts`), ou PascalCase pour les composants si c'est l'usage de l'écosystème.
- Le nom dit ce que contient le fichier. `format-date.ts` plutôt que `utils.ts` quand il n'y a qu'une fonction.
- Interdits : `final`, `final2`, `new`, `old`, `copy`, `backup`, `test2`, `untitled`, `temp`, `misc`, `stuff`, `utils2`, `helpers-new`, `(1)`, des espaces, des accents.
- Un dossier par fonctionnalité plutôt que des dossiers fourre-tout (`components/misc`).
- Un composant par fichier, nom du fichier = nom du composant.

## 5. HTML et JSX

Utiliser l'élément qui correspond au sens :

| Besoin | Élément |
|---|---|
| En-tête de page ou de section | `header` |
| Menu | `nav` avec `ul`/`li` |
| Contenu principal (un seul par page) | `main` |
| Bloc thématique avec un titre | `section` + `h2`/`h3` |
| Contenu autonome (carte projet, article) | `article` |
| Contenu annexe | `aside` |
| Pied | `footer` |
| Action | `button type="button"` |
| Navigation | `a href` (ou `Link`) |
| Image avec légende | `figure` + `figcaption` |
| Date | `time datetime` |
| Champ de formulaire | `label` lié à `input` |

À éviter :
- `div` cliquable (`<div onClick>`), utiliser `button` ;
- `div` qui n'apporte ni style ni structure, supprimer ou remplacer par un fragment ;
- les chaînes `wrapper > container > inner > content` ;
- les `section` sans titre ;
- sauter des niveaux de titre (`h1` puis `h4`) ;
- les `alt="image"` ou `alt="photo"`. Un `alt` décrit l'image, ou vaut `""` si elle est décorative ;
- les `aria-label` qui répètent le texte visible.

## 6. CSS et classes

- Classes nommées selon le rôle : `project-card`, `project-card__title`, `project-card--featured`. Pas `big-title`, `red-text`, `box1`, `div-wrapper`, `container-inner-2`.
- Avec Tailwind, extraire un composant plutôt qu'empiler trente classes copiées partout.
- Variables CSS pour les couleurs, espacements et durées (`--color-accent`, `--space-4`, `--ease-out`). Pas de valeur magique répétée.
- Pas de `!important` sauf pour surcharger un style tiers.
- Supprimer les règles et classes inutilisées.
- Pas de commentaires de section dans le CSS (`/* ===== Header ===== */`) si le fichier est déjà découpé par composant.

## 7. Autres traces de génération

- `console.log` de debug, surtout avec emoji (`console.log("🚀 Server started")`).
- Bloc « Example usage » ou `if __name__ == "__main__":` de démonstration ajouté à un module.
- `try/catch` autour de chaque appel, qui avale l'erreur ou affiche « An error occurred ».
- Vérifications de `null` sur des valeurs qui ne peuvent pas être nulles.
- Fonctions qui ne font qu'appeler une autre fonction.
- Annotations de type redondantes (`const count: number = 0`).
- Variables créées pour être retournées tout de suite (`const result = x; return result;`).
- Code mort, imports inutilisés, paramètres jamais lus.
- Textes d'interface génériques (« Welcome to our amazing website! », « Lorem ipsum » oublié).

## 8. Commits, PR, README

- **Commits** : suivre le format du repo. Sinon, une ligne courte à l'impératif, en anglais : `add contact form validation`, `fix menu focus trap on Safari`. Pas d'emoji, pas d'adjectif (« amazing », « awesome »), pas de point final.
- **PR** : ce qui change, pourquoi, comment tester. Pas de section « Summary ✨ ».
- **README** : à quoi sert le projet, comment l'installer, comment le lancer, comment le déployer. Pas de badges inutiles, pas d'emojis dans les titres, pas de liste « Features » remplie d'adjectifs.

## 9. Exemples avant/après

**Composant React**

Avant :
```tsx
// Import necessary dependencies
import React, { useState } from "react";

// ProjectCard component - displays a project
const MyComponent = ({ data }) => {
  // State to track hover
  const [isHovered, setIsHovered] = useState(false);

  // Handle click event
  const handleClick2 = () => {
    console.log("✅ Card clicked!");
    window.open(data.url);
  };

  return (
    <div className="wrapper">
      <div className="container">
        {/* Title */}
        <div className="big-title">{data.title}</div>
        <div onClick={handleClick2}>View project →</div>
      </div>
    </div>
  );
};

export default MyComponent;
```

Après :
```tsx
type ProjectCardProps = {
  project: { title: string; url: string };
};

export function ProjectCard({ project }: ProjectCardProps) {
  return (
    <article className="project-card">
      <h3 className="project-card__title">{project.title}</h3>
      <a className="project-card__link" href={project.url} target="_blank" rel="noreferrer">
        Voir le projet
      </a>
    </article>
  );
}
```
Le state `isHovered` n'était lu nulle part, il part. Le `div` cliquable qui ouvre une URL devient un lien. Le fichier s'appelle `project-card.tsx` ou `ProjectCard.tsx` selon la convention du projet.

**Fonction utilitaire**

Avant :
```ts
// Function to format the date
export const formatDateHelper = (date: Date): string => {
  try {
    // Format the date using Intl
    const result: string = new Intl.DateTimeFormat("fr-FR").format(date);
    // Return the formatted date
    return result;
  } catch (error) {
    console.error("An error occurred:", error);
    return "";
  }
};
```

Après :
```ts
const dateFormatter = new Intl.DateTimeFormat("fr-FR");

export function formatDate(date: Date) {
  return dateFormatter.format(date);
}
```
