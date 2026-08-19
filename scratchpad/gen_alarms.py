# -*- coding: utf-8 -*-
"""Genere la section `alarms:` de data/keywords.yaml a partir des guides officiels."""
import json, re, io, sys

# ---------------------------------------------------------------- FC (VLT)
codes = json.load(open('codes.json', encoding='utf-8'))
H = {k: {int(n): v for n, v in d['head'].items()} for k, d in codes.items()}
T = {k: {int(n): v for n, v in d['table'].items()} for k, d in codes.items()}
UNIV = sorted(set(H['fc302']) | set(H['fc202']) | set(H['fc102']))
present = lambda g, n: n in H[g] or n in T[g]

# termes de recherche supplementaires (les libelles officiels FR sont abreges sur le LCP)
FC_TERMS = {
    1: "tension 10v basse borne 50", 2: "erreur zero live signal 4-20ma absent 6-01",
    3: "pas de moteur non connecte 1-80", 4: "perte de phase secteur reseau desequilibre 14-12",
    5: "tension bus cc elevee", 6: "tension bus cc basse",
    7: "surtension bus cc deceleration trop rapide freinage", 8: "sous-tension bus cc coupure reseau",
    9: "surcharge onduleur variateur", 10: "surtemperature moteur etr surcharge thermique 1-90",
    11: "surtemperature thermistance moteur ptc sonde", 12: "limite de couple 4-16 4-17",
    13: "surintensite surcourant pic de courant", 14: "defaut de terre masse isolement moteur",
    15: "materiel incompatible hardware", 16: "court-circuit moteur phase a phase",
    17: "depassement temps mot de controle timeout bus communication perdue 8-04",
    20: "erreur entree de temperature", 21: "erreur de parametre",
    22: "frein mecanique de levage 2-2", 23: "defaut ventilateur interne 14-53",
    24: "defaut ventilateur externe 14-53", 25: "court-circuit resistance de freinage",
    26: "limite de puissance resistance de freinage 2-12 2-13", 27: "hacheur de freinage court-circuite igbt",
    28: "echec test de frein 2-15", 29: "temperature dissipateur radiateur surchauffe",
    30: "phase moteur u manquante absente", 31: "phase moteur v manquante absente",
    32: "phase moteur w manquante absente", 33: "defaut de charge precharge soft charge",
    34: "defaut communication bus de terrain profibus profinet", 35: "defaut option carte",
    36: "panne secteur coupure reseau 14-10", 37: "desequilibre de phase",
    38: "defaut interne", 39: "capteur dissipateur radiateur", 40: "surcharge sortie digitale borne 27",
    41: "surcharge sortie digitale borne 29", 42: "surcharge sortie digitale x30",
    43: "alimentation externe 24v", 45: "defaut de terre 2 masse",
    46: "alimentation carte de puissance commande de gachette", 47: "alimentation 24v basse",
    48: "alimentation 1.8v basse", 49: "limite de vitesse 4-11 4-13", 50: "echec etalonnage ama",
    51: "ama verifier unom inom 1-20 1-22", 52: "ama courant nominal trop bas",
    53: "ama moteur trop gros", 54: "ama moteur trop petit", 55: "ama parametre hors plage",
    56: "ama interrompue par l'utilisateur", 57: "ama depassement de temps timeout",
    58: "ama defaut interne", 59: "limite de courant 4-18", 60: "verrouillage externe interlock",
    61: "erreur de retour encodeur trainee 4-30 4-31", 62: "limite frequence de sortie",
    63: "frein mecanique bas courant", 64: "limite de tension", 65: "surtemperature carte de commande",
    66: "temperature dissipateur basse", 67: "configuration option modifiee",
    68: "arret de securite sto safe torque off borne 37", 69: "temperature carte de puissance",
    70: "configuration variateur interdite", 71: "arret de securite ptc 1 mcb112",
    72: "panne dangereuse sto securite", 73: "redemarrage automatique arret de securite",
    74: "thermistance ptc", 76: "configuration unite de puissance", 77: "mode puissance reduite derating 14-59",
    79: "configuration puissance interdite", 80: "variateur initialise valeurs usine reset 14-22",
    83: "combinaison options interdite", 84: "pas d'option de securite",
    88: "detection option", 89: "glissement frein de levage", 90: "surveillance retour codeur",
    91: "reglages entree analogique 54 pt100 switch a54", 92: "absence de debit no flow marche a vide",
    93: "pompe a sec marche a sec dry pump", 94: "fin de courbe end of curve",
    95: "courroie cassee broken belt", 96: "demarrage retarde", 97: "arret retarde",
    98: "defaut horloge rtc", 99: "rotor bloque verrouille 30-22", 104: "ventilateur de brassage",
    122: "rotation moteur inattendue", 123: "modification du moteur",
    154: "surcharge sortie digitale", 163: "atex etr limite de courant avertissement",
    164: "atex etr limite de courant alarme", 165: "atex etr limite de frequence avertissement",
    166: "atex etr limite de frequence alarme", 200: "mode incendie fire mode actif",
    201: "mode incendie a ete actif", 202: "hors limites mode incendie",
    203: "moteur manquant", 204: "rotor bloque",
    243: "igbt de freinage", 244: "temperature dissipateur", 245: "capteur dissipateur",
    246: "alimentation carte de puissance", 247: "temperature carte de puissance",
    248: "configuration puissance interdite", 249: "temperature basse redresseur",
    250: "nouvelle piece de rechange", 251: "nouveau code type",
    500: "enroulement stator moteur cbm", 501: "enveloppe de charge cbm",
    502: "surveillance vibration cbm", 510: "enroulement stator moteur cbm",
    541: "filtre sinus cbm", 531: "filtre sinus cbm",
}
FC_FIX_EN = {46: "Power card supply / Gate drive voltage fault"}


def fc_entry(n):
    fr = H['fc102'].get(n, '').strip(' .')
    en = FC_FIX_EN.get(n) or H['fc302'].get(n) or H['fc202'].get(n) or ''
    en = en.strip(' .')
    if fr and en and fr.lower() == en.lower():
        fr = ''                                    # le guide FR a garde le texte anglais
    return {'n': n, 'fr': fr, 'en': en, 'terms': FC_TERMS.get(n, '')}


GROUPS = []
part = {}
for n in UNIV:
    key = tuple(g for g in ('fc302', 'fc202', 'fc102') if present(g, n))
    part.setdefault(key, []).append(n)

CATSCOPE = {'fc302': '{ cat: "FC-302", type: guide, name: "guide de programmation" }',
            'fc202': '{ cat: "FC-202", type: guide, name: "guide de programmation" }',
            'fc102': '{ cat: "FC-102", type: guide, name: "guide de programmation" }'}
LABEL = {'fc302': 'FC-301 / FC-302 (AutomationDrive)', 'fc202': 'FC-202 (AQUA Drive)',
         'fc102': 'FC-102 (HVAC Drive)'}
SECTION = "chapitre « Liste des codes d'alarme/avertissement » du guide de programmation"

order = sorted(part, key=lambda k: (-len(k), k))
for key in order:
    if not key:
        continue
    if len(key) == 3:
        gid, lab = 'vlt-commun', 'VLT FC-102 / FC-202 / FC-302'
        scope = ['{ family: vlt, type: guide, name: "guide de programmation" }']
    else:
        gid = 'vlt-' + '-'.join(k[2:] for k in key)
        lab = 'VLT ' + ' / '.join(LABEL[k] for k in key)
        scope = [CATSCOPE[k] for k in key]
    GROUPS.append({'id': gid, 'label': lab, 'section': SECTION, 'scope': scope,
                   'codes': [fc_entry(n) for n in part[key]]})

# ---------------------------------------------------------------- iC2
# Guide d'application iC2-Micro, tableau « Resume des evenements d'avertissement et de defaut ».
IC2 = [
    (2, "Déf.zéro signal", "signal absent borne 33 34 zero live 4-20ma"),
    (3, "Pas de moteur", "moteur non connecte"),
    (4, "Perte de phase réseau", "phase secteur desequilibre alimentation"),
    (7, "Surtension CC", "surtension bus cc"),
    (8, "Soustension CC", "sous-tension bus cc"),
    (9, "Surcharge onduleur", "surcharge variateur 100%"),
    (10, "Surtempérature moteur ETR", "surcharge thermique moteur etr"),
    (11, "Surtempérature thermistance moteur", "thermistance ptc sonde moteur"),
    (12, "Limite de couple", "limite couple moteur regenerateur"),
    (13, "Surcourant", "surintensite courant de pointe"),
    (14, "Défaut terre", "defaut de terre masse fuite"),
    (16, "Court-circuit", "court-circuit moteur bornes"),
    (17, "Tempo. mot ctrl", "timeout mot de controle communication"),
    (18, "Échec au démar.", "echec au demarrage moteur bloque"),
    (25, "Court-circuit rés. frein.", "court-circuit resistance de freinage"),
    (26, "Frein surcharge", "surcharge resistance de freinage"),
    (27, "Court-circuit IGBT frein / hacheur de freinage", "hacheur de freinage transistor"),
    (28, "Contrôle freinage", "resistance de freinage non connectee test de frein"),
    (30, "Perte de phase U", "phase moteur u absente"),
    (31, "Perte de phase V", "phase moteur v absente"),
    (32, "Perte de phase W", "phase moteur w absente"),
    (36, "Défaut réseau", "perte de puissance reseau alimentation"),
    (38, "Défaut interne", "contacter le fournisseur"),
    (40, "Surcharge T15", "surcharge borne 15 court-circuit"),
    (46, "Défaut de tension de commande de gâchette", "gate drive"),
    (47, "Alim. 24 V bas.", "alimentation 24v surchargee"),
    (50, "L'étalonnage AMA a échoué", "ama etalonnage"),
    (51, "AMA, vérifier Unom et Inom", "ama tension courant moteur"),
    (52, "AMA Inom bas", "ama courant moteur trop bas"),
    (53, "AMA gros moteur", "ama puissance moteur trop importante"),
    (54, "AMA petit moteur", "ama puissance moteur trop faible"),
    (55, "Plage de paramètres AMA", "ama parametres hors plage"),
    (56, "AMA interrompue", "ama interrompue"),
    (57, "Dépas. tps AMA", "ama depassement de temps timeout"),
    (58, "AMA interne", "ama defaut interne"),
    (59, "Limite de courant", "surcharge limite de courant"),
    (60, "Verrouillage externe", "verrouillage externe interlock"),
    (61, "Erreur retour", "erreur de retour feedback"),
    (63, "Frein mécanique bas", "frein mecanique courant d'activation"),
    (69, "T carte puis.", "temperature carte de puissance"),
    (80, "Init. variateur", "initialisation reglages usine"),
    (87, "Freinage CC auto", "freinage cc automatique reseau it"),
    (95, "Détection perte de charge", "perte de charge"),
    (99, "Rotor bloqué", "rotor bloque"),
    (126, "Moteur en rotation", "moteur pm tourne pendant ama"),
    (127, "FCEM trop élevée", "force contre electromotrice moteur pm"),
]
GROUPS.append({'id': 'ic2', 'label': 'iC2-Micro',
               'section': "chapitre « Événements d'avertissement et de défaut » du guide d'application",
               'scope': ['{ cat: "iC2", type: guide, name: "guide d\'application" }',
                         '{ cat: "iC2", name: "manuel de configuration" }',
                         '{ cat: "iC2", name: "manuel d\'utilisation" }'],
               'codes': [{'n': n, 'fr': fr, 'en': '', 'terms': t} for n, fr, t in IC2]})

# ---------------------------------------------------------------- iC7
IC7_FIX = {
    '4416': "Entrée analogique zéro signal",
    '4198': "Zero Pulse Error", '4284': "No BACnet MS/TP Connection",
    '4285': "BACnet Connection Timeout", '4367': "Imax User", '4385': "Audit Log Stopped",
    '4731': "Imax2 Gate Driver", '4732': "Iearth2 Sd", '5155': "No Flow", '5156': "Dry Run",
}
KIND = {'info': 'information', 'avertissement': 'avertissement', 'defaut': 'défaut',
        'defaut bloquant': 'défaut bloquant'}
ev = {k: {e['n']: e for e in json.load(open(f, encoding='utf-8'))}
      for k, f in (('auto', 'ic7_auto_events.json'), ('aqua', 'ic7_aqua_events.json'),
                   ('hvacr', 'ic7_hvacr_events.json'))}
for d in ev.values():
    for n, e in d.items():
        e['nom'] = IC7_FIX.get(n, e['nom'])

IC7_TERMS = {
    '4160': "absence de phase reseau perte de phase secteur",
    '4161': "surtension reseau", '4162': "pics de tension reseau",
    '4352': "defaut de terre masse", '4353': "defaut de terre masse",
    '4354': "defaut de terre masse", '4355': "defaut de terre masse",
    '4356': "court-circuit onduleur", '4097': "surcharge onduleur",
    '4175': "moteur deconnecte", '4176': "absence de phase moteur",
    '5155': "absence de debit no flow", '5156': "marche a sec pompe a sec dry run",
    '6111': "fin de courbe end of curve", '4888': "confirmation de debit",
    '4644': "commande de gachette gate drive", '4645': "alimentation carte de puissance",
    '5170': "limite de courant", '4372': "injection de courant",
}
IC7SCOPE = {'auto': '{ cat: "iC7 Automation" }', 'aqua': '{ cat: "iC-7 AQUA" }',
            'hvacr': '{ cat: "iC7-HVACR" }'}
IC7LABEL = {'auto': 'iC7 Automation (Industry)', 'aqua': 'iC7 AQUA', 'hvacr': 'iC7 HVACR'}
ic7part = {}
for n in sorted(set(ev['auto']) | set(ev['aqua']) | set(ev['hvacr']), key=int):
    key = tuple(k for k in ('auto', 'aqua', 'hvacr') if n in ev[k])
    ic7part.setdefault(key, []).append(n)

for key in sorted(ic7part, key=lambda k: (-len(k), k)):
    codes = []
    for n in ic7part[key]:
        fr = ev['auto'][n]['nom'] if 'auto' in key else ''
        en = (ev['aqua'][n]['nom'] if 'aqua' in key else
              ev['hvacr'][n]['nom'] if 'hvacr' in key else '')
        if fr and en and fr.lower() == en.lower():
            en = ''
        src = ev[key[0]][n]
        kind = ' / '.join(KIND[t] for t in src['type'] if t in KIND)
        codes.append({'n': int(n), 'fr': fr, 'en': en, 'terms': IC7_TERMS.get(n, ''),
                      'kind': kind, 'grp': src['grp']})
    gid = 'ic7-' + '-'.join(key) if len(key) < 3 else 'ic7-commun'
    lab = 'iC7 (toutes applications)' if len(key) == 3 else ' / '.join(IC7LABEL[k] for k in key)
    scope = ['{ family: ic7, name: "guide d\'application" }',
             '{ family: ic7, name: "manuel de configuration" }'] if len(key) == 3 else \
            [IC7SCOPE[k] for k in key]
    GROUPS.append({'id': gid, 'label': lab,
                   'section': "chapitre « Tableau récapitulatif des événements » du guide d'application",
                   'scope': scope, 'codes': codes})

# ---------------------------------------------------------------- MCD 600
MCD = [l.strip() for l in open('mcd600_trips.txt', encoding='utf-8') if l.strip()]
GROUPS.append({'id': 'mcd600', 'label': 'Démarreur progressif MCD 600',
               'section': "chapitre « Messages de déclenchement » du manuel d'utilisation",
               'scope': ['{ cat: "MCD 600" }'],
               'codes': [{'n': None, 'fr': m, 'en': '', 'terms': ''} for m in MCD]})

# ---------------------------------------------------------------- rendu YAML
def q(s):
    s = s.replace('"', "'")
    return '"%s"' % s

out = io.StringIO()
w = out.write
w("""# ---------------------------------------------------------------------------
# 4. Alarmes, defauts et evenements
#    Libelles releves dans les guides officiels Danfoss (voir `section`) :
#      - VLT FC-102/202/302 : guide de programmation, liste des codes
#        d'alarme/avertissement (le libelle FR est le texte affiche sur le LCP)
#      - iC2-Micro : guide d'application, evenements d'avertissement et de defaut
#      - iC7 : guide d'application, tableau recapitulatif des evenements
#        (numero d'evenement + groupe hexadecimal + type : avertissement,
#        defaut, defaut bloquant)
#      - MCD 600 : manuel d'utilisation, messages de declenchement
#    `terms` = mots de recherche supplementaires (les libelles LCP sont abreges).
#    Le PDF reste la reference pour la cause exacte et la procedure.
# ---------------------------------------------------------------------------
alarms:
""")
for g in GROUPS:
    w('  - id: %s\n' % g['id'])
    w('    label: %s\n' % q(g['label']))
    w('    section: %s\n' % q(g['section']))
    w('    scope:\n')
    for s in g['scope']:
        w('      - %s\n' % s)
    w('    codes:\n')
    for c in g['codes']:
        bits = []
        if c['n'] is not None:
            bits.append('n: %d' % c['n'])
        if c.get('grp'):
            bits.append('grp: %s' % q(c['grp']))
        if c['fr']:
            bits.append('fr: %s' % q(c['fr']))
        if c['en']:
            bits.append('en: %s' % q(c['en']))
        if c.get('kind'):
            bits.append('kind: %s' % q(c['kind']))
        if c['terms']:
            bits.append('terms: %s' % q(c['terms']))
        w('      - { %s }\n' % ', '.join(bits))
    w('\n')

open('alarms_section.yaml', 'w', encoding='utf-8').write(out.getvalue())
print('groupes :', len(GROUPS))
for g in GROUPS:
    print('  %-22s %3d codes  scope=%s' % (g['id'], len(g['codes']), ' + '.join(g['scope'])[:70]))
print('total codes :', sum(len(g['codes']) for g in GROUPS))
