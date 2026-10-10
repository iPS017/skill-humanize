---
name: humanize
description: >-
  Supprime les marqueurs d'écriture IA dans le texte et le code pour un rendu qui semble écrit par un humain :
  tirets cadratins, deux-points dramatiques, caractères spéciaux (… → ✅, guillemets courbes, espaces invisibles),
  formules toutes faites (« plongeons dans », « dans un monde où », delve, seamless), commentaires de code qui
  paraphrasent, noms génériques (data, temp, wrapper), div soup et fichiers mal nommés. À utiliser pour toute
  rédaction ou tout code destiné à être publié ou livré (article, post, mail, README, page web, composant, commit),
  même si l'utilisateur ne le demande pas explicitement, et dès qu'il parle de texte qui « fait IA », d'humaniser,
  de nettoyer du code généré, de clean code ou de nommage. Use for any writing or code the user will ship, and
  whenever they ask to humanize text, remove AI tells, or clean up generated code.
---
<!-- humanize:ignore-file -->

# Humanize

Un lecteur repère un texte généré en deux lignes, et à partir de là il lit tout le reste avec méfiance. Pour le code, c'est pareil : des commentaires qui racontent chaque ligne, des noms vagues et des `div` empilées signalent un copier-coller de chatbot, et rendent le projet plus pénible à maintenir. Ce skill sert à écrire directement sans ces marqueurs, ou à nettoyer un contenu qui en a.

Le but n'est pas de « tromper un détecteur ». Le but est un texte clair et un code propre, comme les écrirait quelqu'un qui connaît son sujet.

## Quand l'appliquer

Dès la rédaction, pas seulement en correction. Si tu écris un texte ou du code que l'utilisateur va publier, envoyer ou committer, applique ces règles pendant que tu écris. Si l'utilisateur te donne un contenu à nettoyer, réécris-le en suivant les mêmes règles.

## Méthode

1. Identifie ce que tu traites : prose, code, ou mélange (README, page HTML, MDX). Identifie la langue.
2. Lis la référence qui correspond, elle contient les listes complètes et des exemples avant/après :
   - prose en français : `references/prose-fr.md`
   - prose en anglais : `references/prose-en.md`
   - code, HTML, CSS, nommage, commits : `references/code.md`
3. Avant de toucher au code d'un projet existant, regarde ses conventions (nommage des fichiers, style CSS, langue des identifiants, linter). Les conventions du projet passent avant les règles de ce skill.
4. Écris ou réécris.
5. Si tu as accès à un terminal, lance le scanner sur le résultat et traite chaque alerte :
   ```bash
   python scripts/scan.py chemin/vers/fichier_ou_dossier
   python scripts/scan.py --fix chemin/   # corrige seulement les cas sans ambiguïté
   ```
   Le scanner trouve les caractères et tournures connus. Il ne juge pas le rythme ni le fond, ça reste ton travail.
6. Livre le résultat sans annoncer que tu l'as « humanisé » et sans liste des changements, sauf si on te la demande.

## Règles à garder en tête en permanence

### Prose

- **Aucun tiret cadratin (—)**, et pas de demi-cadratin (–) utilisé comme incise. Une incise prend deux virgules ou des parenthèses, une rupture prend un point. Le demi-cadratin reste correct dans un intervalle (2020–2024).
- **Deux-points avec parcimonie.** Pas de « Résultat : », « Le secret ? », « La bonne nouvelle : » pour créer un effet. Pas de série de lignes « **Mot-clé** : explication ». En anglais, jamais d'espace avant les deux-points. En français, l'espace avant `:` `;` `!` `?` est la typographie normale, garde-la sauf si le projet fait autrement.
- **Pas de caractères décoratifs**, qu'il s'agisse d'emojis de déco (✅ 🚀 ✨ 💡 👉), flèches (→ ⇒), caractère points de suspension (…) dans du texte technique, puces fantaisie, espaces invisibles.
- **Pas d'ouverture ni de conclusion toutes faites.** On attaque directement le sujet et on s'arrête quand c'est dit. Pas de « Dans un monde où », pas de « En conclusion », pas de « N'hésitez pas à ».
- **Pas de tics de structure**, comme la formule « ce n'est pas X, c'est Y », les énumérations systématiquement par trois, la question rhétorique suivie de sa réponse, la phrase choc en fin de paragraphe.
- **Rythme irrégulier.** Mélange phrases courtes et longues. Une phrase de trois mots, puis une de trente, c'est normal chez un humain.
- **Du concret et un avis.** Un chiffre, un exemple, un nom précis valent mieux qu'un adjectif. Quand il y a une meilleure option, dis laquelle au lieu de peser poliment le pour et le contre.
- **Mise en forme sobre.** Pas de titres pour un texte de trois paragraphes, peu de gras, des listes seulement quand le contenu est vraiment une liste.

### Code

- **Pas de commentaires qui paraphrasent le code.** Supprime `// Import React`, `// Fonction pour gérer le clic`, `# Boucle sur les éléments`. Garde uniquement : licences, directives d'outils (`eslint-disable`, `@ts-expect-error`, `prettier-ignore`, `noqa`), docs d'API publique si le projet en a, et le rare « pourquoi » qu'on ne peut pas deviner (contournement d'un bug de navigateur, contrainte métier).
- **Des noms précis.** Pas de `data`, `temp`, `result`, `item2`, `handleClick2`, `myComponent`. Une fonction commence par un verbe (`fetchProjects`), un booléen par `is`/`has`/`should`.
- **HTML sémantique.** `header`, `nav`, `main`, `section` avec un titre, `article`, `footer`, `button` pour une action, `a` pour une navigation, `ul`/`li` pour une liste. Pas de `div` cliquable, pas de chaînes `wrapper > container > inner`.
- **Classes nommées selon le rôle**, pas l'apparence : `project-card__title`, pas `big-blue-text`. Suis la méthode du projet (BEM, CSS Modules, Tailwind).
- **Fichiers bien nommés** selon la convention du projet. Jamais `final`, `new`, `old`, `copy`, `v2`, `test2`, `utils2`, `misc`.
- **Pas de traces de génération** : `console.log("✅ Success!")`, bloc « Example usage » en fin de fichier, `// TODO: implement`, `try/catch` autour de tout, messages d'erreur vagues, README rempli d'emojis.
- **Commits** au format du projet, courts, sans emoji ni adjectif (« add contact form validation », pas « ✨ Add amazing new validation feature »).

## Ce qu'il ne faut pas toucher

- Le sens, les faits, les chiffres, les noms propres et les citations.
- Le comportement du code. Un renommage doit être appliqué partout où l'identifiant est utilisé (imports, tests, styles). Si tu ne peux pas vérifier toutes les occurrences, signale-le au lieu de casser le projet.
- Le texte entre guillemets qui vient de quelqu'un d'autre.
- La voix de l'auteur quand il en a une. Si l'utilisateur écrit avec des tirets cadratins volontairement, c'est son style, demande avant de les retirer.
