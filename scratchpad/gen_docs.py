# -*- coding: utf-8 -*-
"""Genere la section `documents:` de data/keywords.yaml : le vocabulaire propre a
chaque PDF, releve dans son sommaire (manuels/guides) ou dans les intitules de ses
tableaux de caracteristiques (fiches techniques)."""
import fitz, json, re, os, collections, unicodedata

os.chdir(os.path.dirname(os.path.abspath(__file__)))
docs = json.load(open('doclist.json', encoding='utf-8'))

# titres de service, presents partout : sans valeur pour la recherche
BOILER = re.compile(r'^(table des matieres|sommaire|contents|introduction|presentation|'
                    r'securite|safety|abreviations|abbreviations|marques|trademarks|'
                    r'historique des versions|version history|glossaire|glossary|index|'
                    r'annexe|appendix|mentions legales|copyright|avertissements? generaux|'
                    r'a propos de ce|about this|objet (de|du) ce|purpose of this|'
                    r'ressources supplementaires|additional resources|symboles de securite|'
                    r'utilisation prevue|intended use|personnel qualifie|qualified personnel|'
                    r'danfoss|conventions|notes?|remarques?)\b')
NUMPFX = re.compile(r'^\s*(?:\d+(?:[.\-]\d+)*\.?|[A-Z]\.|[ivxlc]+\.)\s+')
UNITE = re.compile(r'\d|\b(V|A|Hz|kW|kg|mm|m|%|CA|CC|AC|DC)\b|°C')
PROSE = re.compile(r'\b(vous|nos|notre|leur|est|sont|offre|offrent|permet|grace|plus que|'
                   r'ainsi|cela|celle|celui|qui|que)\b')
FINPREP = ('et', 'de', 'du', 'la', 'le', 'des', 'pour', 'avec', 'dans', 'sur', 'en', 'a')


def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(c for c in s if not unicodedata.combining(c))


def clean(t):
    t = NUMPFX.sub('', t.replace(' ', ' ').replace('’', "'"))
    return re.sub(r'\s+', ' ', t).strip(' .:;-–—')


def keep(t):
    if not (4 <= len(t) <= 45):
        return False
    n = norm(t)
    if BOILER.match(n) or not re.search(r'[a-z]{3}', n):
        return False
    return len(t.split()) <= 7


def from_toc(doc):
    return [clean(titre) for lvl, titre, _ in doc.get_toc() if lvl <= 3]


def from_text(doc):
    """Fiches techniques (sans signets) : intitules des tableaux de caracteristiques.
    Un intitule est une ligne courte suivie d'une valeur (chiffre ou unite) ; la
    premiere page, purement commerciale, est ignoree."""
    first = 1 if doc.page_count >= 3 else 0
    out = []
    for p in range(first, min(16, doc.page_count)):
        lignes = [x for x in (clean(l) for l in doc[p].get_text().split(chr(10))) if x]
        for i, t in enumerate(lignes):
            if not (4 <= len(t) <= 40) or len(t.split()) > 5 or not t[0].isupper():
                continue
            if t.endswith((',', ':', '(')) or t.split()[-1].lower() in FINPREP:
                continue
            if PROSE.search(norm(t)) or sum(c.isdigit() for c in t) > 2:
                continue
            suivante = lignes[i + 1] if i + 1 < len(lignes) else ''
            if not UNITE.search(suivante):          # un intitule est suivi d'une valeur
                continue
            out.append(t)
    return out


profiles = []
for d in docs:
    if d['type'] in ('brochure', 'list'):    # documents commerciaux : pas de vocabulaire technique
        continue
    try:
        doc = fitz.open(d['file'])
    except Exception as e:
        print('ERR', d['name'], e)
        continue
    raw = from_toc(doc) or from_text(doc)
    seen, phrases = set(), []
    for t in raw:
        n = norm(t)
        if not keep(t) or n in seen:
            continue
        seen.add(n)
        phrases.append(t)
    if phrases:
        profiles.append({**{k: d[k] for k in ('cat', 'grp', 'name', 'type')}, 'phrases': phrases})
    print('%-22s %-36s %4d -> %3d' % (d['cat'][:22], d['name'][:36], len(raw), len(phrases)))

# une phrase presente dans trop de documents ne distingue rien
df = collections.Counter()
for p in profiles:
    for t in set(norm(x) for x in p['phrases']):
        df[t] += 1
LIMIT = max(3, int(len(profiles) * 0.20))
for p in profiles:
    ordre = {t: i for i, t in enumerate(p['phrases'])}
    gardes = [t for t in p['phrases'] if df[norm(t)] <= LIMIT]
    gardes.sort(key=lambda t: (df[norm(t)], ordre[t]))
    p['phrases'] = sorted(gardes[:90], key=lambda t: ordre[t])

json.dump(profiles, open('docprofiles.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(chr(10) + '%d documents profiles (seuil df=%d)' % (len(profiles), LIMIT))
print('phrases totales :', sum(len(p['phrases']) for p in profiles))
