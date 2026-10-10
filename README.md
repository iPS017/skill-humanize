# skill-humanize

Plugin pour Claude qui retire les marqueurs d'écriture IA du texte, du code et des interfaces. Il contient deux skills et un hook.

- Le skill `humanize` traite le texte et le code : tirets cadratins, deux-points d'effet, emojis et flèches de décoration, formules toutes faites, commentaires dans le code, noms génériques, classes comme `main-wrapper` ou `content-container`, div soup, fichiers mal nommés.
- Le skill `humanize-ui` fait la review du rendu d'une interface. Il retire les néons, les dégradés de fond, le texte en dégradé, le glassmorphism, les taches floues, la palette violette par défaut, les animations en boucle et les petits textes inutiles (heure locale, « 01 / Services », « Scroll pour explorer »). Il corrige les espacements, les boutons et les raccourcis clavier en suivant les Human Interface Guidelines d'Apple.
- Le hook se déclenche après chaque fichier que Claude Code écrit ou modifie : le scanner tourne et renvoie à Claude ce qu'il doit corriger (commentaires, noms de classes, effets visuels). Les règles s'appliquent même quand le skill n'a pas été chargé.

## Contenu

```
.claude-plugin/
├── marketplace.json      déclare le marketplace pour Claude Code
└── plugin.json
hooks/
└── hooks.json            lance le scanner après chaque Write ou Edit
skills/humanize/
├── SKILL.md              règles principales, chargées quand le skill se déclenche
├── references/
│   ├── prose-fr.md       listes et exemples pour le français
│   ├── prose-en.md       listes et exemples pour l'anglais
│   └── code.md           commentaires, nommage, HTML sémantique, CSS, commits
└── scripts/
    ├── scan.py           scanner sans dépendance (Python 3.8+)
    └── hook.py           point d'entrée du hook
skills/humanize-ui/
├── SKILL.md              méthode de review et règles visuelles
├── references/
│   ├── ai-tells.md       catalogue des effets « IA » et leur correction
│   └── apple.md          espacements, typographie, boutons, couleurs, raccourcis (HIG)
└── scripts/
    └── scan_ui.py        scanner CSS, Tailwind, JSX, HTML
```

## Installation

### Claude Code (marketplace)

```
/plugin marketplace add iPS017/skill-humanize
/plugin install humanize@skill-humanize
```

Dans l'extension VS Code, ajoute `iPS017/skill-humanize` dans l'onglet Marketplaces de Manage Plugins, puis installe le plugin `humanize`.

### Claude Code (copie manuelle)

```bash
git clone https://github.com/iPS017/skill-humanize.git
cp -r skill-humanize/skills/humanize skill-humanize/skills/humanize-ui ~/.claude/skills/
```

Pour un seul projet, copie les deux dossiers dans `.claude/skills/` à la racine du repo. La copie manuelle n'installe pas le hook : passe par le marketplace pour l'avoir.

### Claude.ai et l'app Claude

Compresse chaque dossier (`skills/humanize` et `skills/humanize-ui`) dans son propre `.zip`, le dossier à la racine de l'archive, puis importe-les dans la section Skills des réglages.

## Utilisation

Rien à faire en temps normal. Pour forcer un skill : « passe ce texte au skill humanize », « nettoie ce composant avec humanize », « fais une review du rendu avec humanize-ui ».

Les scanners peuvent aussi tourner seuls :

```bash
python skills/humanize/scripts/scan.py src/ contenu/          # liste les problèmes
python skills/humanize/scripts/scan.py --fix src/             # corrige les cas sans ambiguïté
python skills/humanize/scripts/scan.py --strip-comments src/  # supprime les commentaires, sauf licences et directives d'outils
echo "Mon texte" | python skills/humanize/scripts/scan.py - --lang fr
```

`--fix` retire les caractères invisibles, remplace `…` et les guillemets courbes dans le code, et enlève l'espace avant la ponctuation en anglais. Les tirets cadratins et les tournures ne sont jamais corrigés automatiquement, parce que la bonne réécriture dépend de la phrase.

`--strip-comments` réécrit les fichiers. Fais un commit avant de le lancer.

```bash
python skills/humanize-ui/scripts/scan_ui.py src/        # néons, dégradés, focus, raccourcis, petits textes
python skills/humanize-ui/scripts/scan_ui.py --all src/  # ajoute les signaux faibles (palette, espacements hors grille)
```

Les deux scripts renvoient le code 1 s'il trouve des erreurs, ce qui permet de l'utiliser dans un hook de pre-commit ou en CI.

Pour exclure un fichier (du scanner comme du hook), ajoute `humanize:ignore-file` dans ses vingt premières lignes.

## Limites

Les scanners repèrent des motifs connus. Ils ne voient pas la composition d'une page : la review du rendu reste le travail de Claude.

Le scanner de texte repère des caractères et des tournures connus. Il ne juge ni le fond ni le ton, et certains mots signalés sont parfois légitimes (« robust » dans une doc technique, par exemple). Les avertissements sont des pistes, les erreurs sont à corriger. Un dégradé ou une couleur violette qui vient de la charte de la marque reste : le hook le signale, Claude le garde.

Le hook a besoin de Python 3 dans le PATH (`python3` ou `python`). Sans Python, il ne fait rien.
