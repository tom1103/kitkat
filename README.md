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
« surtension », « défaut de terre »), un thème (« harmoniques », « STO »,
« PROFINET », « marche à sec », « derating ») ou coller un code produit
(« FC-302P1K1T5E20H2 ») : un bandeau indique ce qui a été reconnu et les
documents correspondants sont filtrés/classés.

Le dictionnaire est **compilé dans la page au build** puis indexé en mémoire :
aucune base de données, aucune requête réseau (compatible GitHub Pages),
~0,1 à 3 ms par frappe.

### Enrichir le dictionnaire

Tout se passe dans `data/keywords.yaml` (l'en-tête du fichier documente les règles) :

| Section | Rôle |
|---|---|
| `products` | alias de gammes et débuts de codes produits → catégorie du catalogue |
| `synonyms` | groupes de mots équivalents (`variateur` = `vfd` = `drive`…) |
| `topics` | thèmes techniques : `terms` (ce qu'on tape) → `scope` (documents ciblés) |
| `alarms` | codes de défauts et leurs libellés FR/EN → document qui les documente |

Un `scope` cible les documents par `family`, `cat`, `group`, `type`, `name`
(sous-chaîne) et `not` (exclusion). Ajouter un thème = ajouter un bloc à
`topics` ; aucun code à modifier.

> Les libellés d'alarmes sont une **aide à la recherche** : le PDF Danfoss
> reste la référence pour la cause exacte et la procédure.

---
*Ce portail est maintenu par MEDIA MESURES pour garantir un accès rapide et structuré aux ressources techniques officielles.*
