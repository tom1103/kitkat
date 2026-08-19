# -*- coding: utf-8 -*-
"""Ecrit la section `documents:` (vocabulaire propre a chaque PDF) et la rattache
a data/keywords.yaml."""
import json, os, io, collections

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open('docprofiles.json', encoding='utf-8'))

# le couple (categorie, nom) suffit-il a identifier un document ?
c = collections.Counter((p['cat'], p['name']) for p in P)
ambigus = [k for k, v in c.items() if v > 1]
print('doublons cat+nom :', ambigus)

out = io.StringIO()
out.write("""
# ---------------------------------------------------------------------------
# 5. Vocabulaire propre a chaque document
#    Releve automatiquement dans le PDF lui-meme : sommaire (manuels et guides)
#    ou intitules des tableaux de caracteristiques (fiches techniques).
#    C'est ce qui permet de repondre a « refroidissement ic7 » par le manuel de
#    configuration (« Debit d'air et niveaux sonores », « Refroidissement et
#    perte de puissance ») plutot que par la brochure commerciale.
#    Regenere par scratchpad/gen_docs.py + emit_docs.py.
# ---------------------------------------------------------------------------
documents:
""")
for p in sorted(P, key=lambda x: (x['cat'], x['grp'], x['name'])):
    q = lambda s: '"%s"' % s.replace('"', "'")
    out.write('  - cat: %s\n' % q(p['cat']))
    if p['grp'] and ambigus:
        out.write('    grp: %s\n' % q(p['grp']))
    out.write('    name: %s\n' % q(p['name']))
    out.write('    kw: %s\n' % q(' ; '.join(p['phrases'])))

section = out.getvalue()
open('documents_section.yaml', 'w', encoding='utf-8').write(section)

KW = r'C:\Users\ThomasMONCHATRE\OneDrive - MEDIA MESURES\Documents\IT\Dev\kitkat\data\keywords.yaml'
txt = io.open(KW, encoding='utf-8').read()
marqueur = '\n# ---------------------------------------------------------------------------\n# 5. Vocabulaire propre a chaque document'
if marqueur in txt:
    txt = txt[:txt.index(marqueur)]
io.open(KW, 'w', encoding='utf-8', newline='').write(txt.rstrip() + '\n' + section)
print('%d documents, %d phrases, section de %d Ko'
      % (len(P), sum(len(p['phrases']) for p in P), len(section) // 1024))
