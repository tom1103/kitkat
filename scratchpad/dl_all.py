# -*- coding: utf-8 -*-
"""Telecharge tous les PDF du catalogue (une seule fois, pour extraire leurs sommaires)."""
import json, subprocess, hashlib, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
os.makedirs('all', exist_ok=True)

docs = json.load(open('doclist.json', encoding='utf-8'))
for i, d in enumerate(docs):
    key = hashlib.md5((d['cat'] + '|' + d['grp'] + '|' + d['name']).encode()).hexdigest()[:10]
    d['file'] = 'all/%s.pdf' % key
    if os.path.exists(d['file']) and os.path.getsize(d['file']) > 10000:
        continue
    subprocess.run(['curl', '-sL', '--max-time', '300', '-o', d['file'], d['url']])
    size = os.path.getsize(d['file']) if os.path.exists(d['file']) else 0
    print('%2d/%d  %-22s %-38s %8d' % (i + 1, len(docs), d['cat'][:22], d['name'][:38], size), flush=True)

json.dump(docs, open('doclist.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('FINI', sum(1 for d in docs if os.path.exists(d['file'])), 'fichiers')
