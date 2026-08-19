# Outils de génération du dictionnaire de recherche

Ces scripts ne servent qu'à **régénérer** `data/keywords.yaml` quand Danfoss met à
jour ses PDF. Le site n'en a pas besoin pour fonctionner : tout est déjà compilé
dans le YAML.

Prérequis : `pip install pymupdf pyyaml` et `curl` (fourni avec Git pour Windows).

```bash
python scratchpad/dl_all.py      # 1. télécharge les PDF du catalogue (~500 Mo, une fois)
python scratchpad/gen_docs.py    # 2. relève le vocabulaire de chaque PDF
python scratchpad/emit_docs.py   # 3. écrit la section `documents:` dans data/keywords.yaml
python scratchpad/gen_alarms.py  # 4. réécrit la section `alarms:` (listes d'alarmes)
```

| Script | Rôle |
|---|---|
| `dl_all.py` | lit `data/catalog.yaml`, télécharge chaque PDF dans `all/` (version FR si elle existe) |
| `gen_docs.py` | sommaire (signets) des manuels/guides, intitulés des tableaux des fiches techniques ; écarte les brochures, les titres de service et les intitulés trop répandus |
| `emit_docs.py` | rend la section `documents:` et la remplace dans `data/keywords.yaml` |
| `gen_alarms.py` | rend la section `alarms:` à partir des listes d'alarmes relevées dans les guides de programmation FC, les guides d'application iC2/iC7 et le manuel MCD 600 |

Les fichiers de travail (`all/`, `*.json`, `*.txt`) restent hors du dépôt.
