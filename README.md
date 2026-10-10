# humanize

Skill pour Claude qui retire les marqueurs d'écriture IA du texte et du code : tirets cadratins, deux-points d'effet, emojis et flèches de décoration, formules toutes faites, commentaires qui paraphrasent le code, noms génériques, div soup, fichiers mal nommés.

Claude l'utilise tout seul quand il écrit un texte ou du code à livrer, ou quand on lui demande de nettoyer un contenu.

## Contenu

```
.claude-plugin/
├── marketplace.json      déclare le marketplace pour Claude Code
└── plugin.json
skills/humanize/
├── SKILL.md              règles principales, chargées quand le skill se déclenche
├── references/
│   ├── prose-fr.md       listes et exemples pour le français
│   ├── prose-en.md       listes et exemples pour l'anglais
│   └── code.md           commentaires, nommage, HTML sémantique, CSS, commits
└── scripts/
    └── scan.py           scanner sans dépendance (Python 3.8+)
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
cp -r skill-humanize/skills/humanize ~/.claude/skills/
```

Pour un seul projet, copie `skills/humanize` dans `.claude/skills/` à la racine du repo.

### Claude.ai et l'app Claude

Compresse le dossier `skills/humanize` en `.zip` (le dossier doit être à la racine de l'archive), puis importe-le dans la section Skills des réglages.

## Utilisation

Rien à faire en temps normal. Pour forcer le skill : « passe ce texte au skill humanize », « nettoie ce composant avec humanize ».

Le scanner peut aussi tourner seul :

```bash
python skills/humanize/scripts/scan.py src/ contenu/          # liste les problèmes
python skills/humanize/scripts/scan.py --fix src/             # corrige les cas sans ambiguïté
python skills/humanize/scripts/scan.py --strip-comments src/  # supprime les commentaires, sauf licences et directives d'outils
echo "Mon texte" | python skills/humanize/scripts/scan.py - --lang fr
```

`--fix` retire les caractères invisibles, remplace `…` et les guillemets courbes dans le code, et enlève l'espace avant la ponctuation en anglais. Les tirets cadratins et les tournures ne sont jamais corrigés automatiquement, parce que la bonne réécriture dépend de la phrase.

`--strip-comments` réécrit les fichiers. Fais un commit avant de le lancer.

Le script renvoie le code 1 s'il trouve des erreurs, ce qui permet de l'utiliser dans un hook de pre-commit ou en CI.

Pour exclure un fichier, ajoute `humanize:ignore-file` dans ses vingt premières lignes.

## Limites

Le scanner repère des caractères et des tournures connus. Il ne juge ni le fond ni le ton, et certains mots signalés sont parfois légitimes (« robust » dans une doc technique, par exemple). Les avertissements sont des pistes, les erreurs sont à corriger.
