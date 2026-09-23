# Kitkat - Portail de Ressources Danfoss

Ce site centralise l'ensemble de la documentation technique et des ressources logicielles relatives aux solutions d'automatisation et de variation de vitesse Danfoss.

## Contenu du Portail

Le portail est organisé par gammes de produits pour faciliter l'accès aux informations critiques :

### Variateurs de Fréquence
- **iC7 Automation** : Brochures, manuels de configuration et d'utilisation STO, guides d'applications industrielles et fiches techniques.
- **iC2 Micro** : Documentation technique complète pour la gamme compacte.
- **VLT FC-302 / FC-202 / FC-102** : Guides de dimensionnement (par puissance), manuels de programmation et encombrements.

### Options et Accessoires
- Accès direct aux fiches techniques des cartes optionnelles (MCB, MCA).
- Documentation sur la sécurité (STO) et la surveillance conditionnelle (CBM).
- Filtres de sortie.

### Logiciels et Bibliothèques
- **My Drive Insight** & **MCT-10** : Liens directs vers les dernières versions des outils de paramétrage.
- **Librairies PLC** : Ressources pour l'intégration dans les contrôleurs logiques.

## Recherche par thème et par alarme

La recherche ne se limite pas au nom des documents : un dictionnaire métier
(`data/keywords.yaml`) relie le vocabulaire technique aux documents du catalogue.
On peut donc taper un défaut lu sur l'afficheur (« alarme 14 », « A29 »,
« surtension », « courroie cassée »), un numéro d'événement iC7 (« 4160 »,
« 3130h »), un thème (« harmoniques », « STO », « PROFINET », « marche à sec »,
« derating ») ou coller un code produit (« FC-302P1K1T5E20H2 ») : un bandeau
indique ce qui a été reconnu et les documents correspondants sont filtrés/classés.

Les 568 codes du dictionnaire sont **relevés dans les guides officiels** :
liste des codes d'alarme/avertissement des guides de programmation
FC-102 / FC-202 / FC-302 (y compris les alarmes propres à chaque application,
ex. 92 « Abs. de débit » ou 95 « Courroie cassée » sur AQUA/HVAC), événements
d'avertissement et de défaut du guide d'application iC2, tableau récapitulatif
des événements des guides d'application iC7 (numéro, groupe hexadécimal et type :
avertissement / défaut / défaut bloquant) et messages de déclenchement du manuel
MCD 600. Le libellé français des VLT et de l'iC2 est le texte affiché sur le
panneau de commande ; `terms` ajoute les mots complets utiles à la recherche.

Le dictionnaire est **compilé dans la page au build** puis indexé en mémoire :
aucune base de données, aucune requête réseau (compatible GitHub Pages),
~0,1 à 3 ms par frappe.

### Enrichir le dictionnaire

Tout se passe dans `data/keywords.yaml` (l'en-tête du fichier documente les règles) :

| Section | Rôle |
|---|---|
| `products` | alias de gammes (`cat:` ou `family:`) et débuts de codes produits |
| `synonyms` | groupes de mots équivalents (`variateur` = `vfd` = `drive`…) |
| `topics` | thèmes techniques : `terms` (ce qu'on tape) → `scope` (documents ciblés) |
| `alarms` | groupes de codes par gamme : `n`, `fr`, `en`, `kind`, `grp`, `terms` → `scope` |
| `documents` | vocabulaire propre à chaque PDF, relevé dans son sommaire ou ses tableaux de caractéristiques (section générée, comme `alarms`) |

C'est la section `documents` qui fait que « refroidissement iC7 » répond par la
fiche technique (températures, altitude) et le manuel de configuration (« Débit
d'air et niveaux sonores », « Refroidissement et perte de puissance ») au lieu de
la brochure commerciale : un document qui consacre une section au sujet passe
devant un document qui ne fait que l'évoquer. Brochures et listes de liens ne
remontent que si la recherche porte sur leur nom.

### Ouverture à la bonne page

Chaque intitulé relevé porte sa page (`intitulé@page`), et chaque code d'alarme
la page du paragraphe qui le décrit (`alarmes: "14@831 …"`). Sous chaque résultat,
la recherche affiche donc **pourquoi** ce document sort et ouvre le PDF au bon
endroit :

| Recherche | Ce qui s'affiche sous le résultat |
|---|---|
| `débit d'air ic7` | Manuel de configuration → *Débit d'air et niveaux sonores* **p. 74** |
| `alarme 14` | Guide de programmation FC-302 → *Alarme 14 · Défaut terre* **p. 831** |
| `4160` | Guide d'application iC7 → *Événement 4160 · Absence de phase réseau* **p. 348** |
| `couple de serrage` | Guide de dimensionnement → *Couple de serrage* **p. 7** |

Les pages ne valent que pour la version du PDF qui a été indexée (`lang:`), donc
le lien direct n'est proposé que sur cette version-là.

Un `scope` cible les documents par `family`, `cat`, `group`, `type`, `name`
(sous-chaîne) et `not` (exclusion). Ajouter un thème = ajouter un bloc à
`topics` ; aucun code à modifier.

> Les libellés d'alarmes sont une **aide à la recherche** : le PDF Danfoss
> reste la référence pour la cause exacte et la procédure.

---
*Ce portail est maintenu par MEDIA MESURES pour garantir un accès rapide et structuré aux ressources techniques officielles.*
