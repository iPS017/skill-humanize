<!-- humanize:ignore-file -->
# Checklist d'audit complet (60 points)

Liste à parcourir pour un audit complet d'une application, en plus de `ai-tells.md` (détail des corrections visuelles) et `apple.md` (espacements, boutons, raccourcis). Un point isolé n'est pas forcément un défaut. Ce qui pose problème, c'est l'usage automatique, répété ou sans justification. Les points 36 à 60 sont des risques à vérifier dans le rendu et dans le code, pas des défauts présumés.

## Sommaire

1. Les 20 signes classiques (1 à 20)
2. Signature graphique et composition (21 à 35)
3. États, robustesse, accessibilité et finition (36 à 60)

## 1. Les 20 signes classiques

1. **Dégradés violet vers bleu** sans lien avec l'identité du produit.
2. **Titres en texte dégradé** ajoutés pour faire moderne.
3. **Emojis dans les titres**, les menus ou les descriptions.
4. **Inter partout**, ou une autre police générique choisie sans travail typographique.
5. **Cartes à bordure colorée** dont l'identité tient uniquement à cette bordure.
6. **Glassmorphism partout** : panneaux transparents, flou et bordure claire sur chaque surface.
7. **Mode sombre à faible contraste** : surfaces et textes secondaires difficiles à distinguer.
8. **Trois cartes à icône en ligne** (icône, titre, description) produites par réflexe.
9. **Badge au-dessus de chaque titre** pour simuler une hiérarchie.
10. **Icônes Lucide partout**, les mêmes icônes génériques posées sans réflexion.
11. **shadcn/ui non retouché** : composants de bibliothèque laissés tels quels, sans adaptation à l'identité.
12. **Fade-in au défilement** systématique, sans rôle fonctionnel.
13. **Halos qui suivent le curseur**, faisceaux ou lumières sans utilité.
14. **Boutons dont le seul survol est un changement d'opacité.**
15. **Espacements incohérents** entre composants, valeurs arbitraires.
16. **Tirets cadratins partout** dans les textes.
17. **Texte promotionnel à mots-clés** : vague, impersonnel, typique d'un texte généré.
18. **Accents en serif italique** placés pour faire éditorial.
19. **Space Grotesk + Instrument Serif**, ou tout duo de polices à la mode appliqué sans recherche.
20. **Grain sur un dégradé** pour imiter une direction artistique.

## 2. Signature graphique et composition

Ces points viennent de l'audit d'un lecteur de musique desktop. Ils valent pour toute application qui a une signature graphique forte.

21. **Formes décoratives répétées partout** (grosses taches organiques en fond de chaque page). Répétées, elles perdent leur caractère. Réduire leur fréquence et leur donner une fonction précise.
22. **Forme de marque surutilisée** : la forme du logo sert à la fois d'action et de décoration. La garder, mais séparer clairement usage fonctionnel et usage décoratif.
23. **Séparateurs ondulés répétés** dans la navigation, les sections et le lecteur. Une signature ne doit pas devenir un motif automatique.
24. **Tout est une pilule** : navigation, filtres, boutons, recherche, lecteur. Établir une hiérarchie de formes (rayons différents selon le rôle) pour éviter une interface uniformément gonflée.
25. **Vide sans intention** : une page avec deux éléments et une immense zone vide dessous. L'espace découle du contenu, pas d'un gabarit fixe.
26. **Hiérarchie des titres incohérente** d'une page à l'autre. Une échelle typographique commune, avec des variations voulues.
27. **Grande carte, contenu tronqué** : un conteneur qui prend beaucoup de place mais coupe l'information principale (titre du morceau). Le contenu prime sur le conteneur.
28. **Cartes de contenu toutes identiques** (mix, playlists, recommandations). Les différencier par des informations utiles, pas par une variété artificielle.
29. **Rectangles de catégories colorés** : même bloc, couleur différente. Rendre la présentation propre à l'univers du produit.
30. **Flou trop fort** (paroles non actives, arrière-plans) qui empêche de lire. L'effet de profondeur ne passe jamais avant la lisibilité.
31. **Élément flottant qui recouvre le contenu** (lecteur, barre d'action). Prévoir une zone de sécurité (padding en bas égal à sa hauteur) pour que tout reste accessible au défilement.
32. **Composants de styles différents** : menus déroulants et sliders standards à côté d'éléments expressifs. Tout appartient au même système, sans forcément utiliser les mêmes formes.
33. **Décor qui concurrence le contenu** : formes géantes et séparateurs plus visibles que les informations. La priorité va au contenu et aux commandes.
34. **Indicateurs de développement visibles** (« Lyrics: fixture », « TODO », « debug », identifiants internes). Les retirer de la version livrée.
35. **Langues mélangées** dans l'interface. Toutes les chaînes suivent la langue choisie par l'utilisateur, sauf noms propres et noms de services.

## 3. États, robustesse, accessibilité et finition

36. **Cartes dans des cartes** : panneaux, cartes, sous-cartes, bordures empilés. Une information n'a pas toujours besoin d'un conteneur.
37. **Composition-gabarit** sur chaque page : gros titre, description, barre de recherche, grille de cartes. Adapter la composition à l'objectif de l'écran.
38. **Remplacer un cliché par un autre** : quitter le violet pour le fond crème, le serif et le vert sauge, c'est adopter l'autre esthétique générée par défaut.
39. **Icônes étincelles** (✨) qui suggèrent l'IA, la magie ou la personnalisation. Une icône communique une fonction réelle.
40. **Faux look natif** : pastilles macOS simulées sur Windows et Linux, menus et raccourcis d'un autre système. Contrôles de fenêtre et comportements adaptés à l'OS réel.
41. **Visuels de remplacement génériques** (pochettes, illustrations provisoires). Prévoir un fallback cohérent pour une image manquante.
42. **Données factices répétées** : titres, descriptions et données de démo laissés en production.
43. **Titres impressionnants mais vides.** Un intitulé dit précisément le contenu ou l'action.
44. **Microcopie générique** (« Something went wrong », « Please try again », « Discover more »). Messages contextuels et précis.
45. **États vides négligés** : chaque liste, recherche, historique et bibliothèque a un état vide conçu, avec une indication utile.
46. **Faux chargements** : skeletons qui ne ressemblent pas au contenu, attentes prolongées, pourcentages inventés.
47. **Erreurs mal gérées** : dire ce qui a échoué (téléchargement, recherche, lecture, synchronisation) et proposer les actions réellement possibles.
48. **Pas d'échec partiel** : si une partie des données manque, garder le reste fonctionnel au lieu d'une page d'erreur entière.
49. **Permissions ignorées** : refus d'autorisation, intégration indisponible, fichier inaccessible, permission système refusée. Chaque cas a son écran.
50. **Interface pensée pour le cas idéal seulement.** Tester avec une bibliothèque immense, un titre très long, sans connexion, avec des fichiers corrompus et des données incomplètes.
51. **Clavier oublié** : ordre de tabulation logique, focus visible, interactions clavier attendues sur desktop.
52. **Boutons icône sans nom** : `aria-label` obligatoire, infobulle quand l'icône ne suffit pas.
53. **Action accessible seulement au survol.** Elle doit rester atteignable au clavier, au toucher et aux autres modes d'entrée.
54. **`prefers-reduced-motion` ignoré** : les animations décoratives se coupent ou se réduisent.
55. **Trop d'animations** : mouvements simultanés sans lien, rebonds, effets permanents, transitions qui retardent l'accès au contenu.
56. **Effets coûteux** : flous lourds, filtres SVG complexes, ombres animées, recalculs de géométrie inutiles. L'interface reste fluide sur une machine modeste.
57. **États d'interaction incomplets** : normal, survol, pressé, sélectionné, focus, désactivé, chargement, erreur. Comportement prévisible pour chaque composant.
58. **Typographie sans réglage fin** : hauteurs de ligne, graisses, longueur de ligne, interlettrage, alignements optiques, ellipses.
59. **Mise en page qui casse au redimensionnement** : fenêtre réduite, agrandie, maximisée, mise à l'échelle système. Aucun contrôle essentiel coupé ou masqué.
60. **Progression déconnectée du réel** : une barre de progression reflète l'état réel du processus. Durée inconnue : indicateur indéterminé, pas de faux pourcentage.
