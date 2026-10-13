# -*- coding: utf-8 -*-
"""revC10_t2b_law.py -- TASK 2 (continued): law diagnostics + corrected class.

(a) literal class (i mod M, d, lamA mod M, lamfront mod M): collect ALL clashing
    pairs; check whether every clash is explained by h = (v-1)-i differing
    (h = number of queue slots between pointer and boundary incl. boundary).
(b) corrected class (+ h): test 'equal class => equal crossing decseq' over
    v = 1..8192, scan moduli for the minimal working one.
Appends results to revC10_t2.json (key 'law2').
"""
import json

import revC10_lib as L

VMAX = 8192


def main():
    d = json.load(open('revC10_t2.json'))
    cross = {int(k): v for k, v in d['cross'].items()}
    for v, cv in cross.items():
        i, dd, rA, rF = cv['cls']
        cv['h'] = (v - 1) - i          # queue slots from pointer to boundary inclusive

    # (a) all clashes of the literal class, M = 8192 (i within range -> i exact)
    M = 8192
    groups = {}
    clashes = []
    for v in sorted(cross):
        i, dd, rA, rF = cross[v]['cls']
        key = (i % M, dd, rA % M, rF % M)
        if key in groups:
            v0 = groups[key]
            if cross[v0]['seq'] != cross[v]['seq']:
                clashes.append((v0, v, cross[v0]['h'], cross[v]['h']))
        else:
            groups[key] = v
    nonh = [c for c in clashes if c[2] == c[3]]
    print('literal class M=8192: %d clashes; non-h-explained: %d' % (len(clashes), len(nonh)))
    print('  sample clashes (v0, v, h0, h):', clashes[:8])
    if nonh:
        print('  NON-H CLASHES:', nonh[:8])

    # (b) corrected class (+h)
    results = {}
    Ms = sorted(set(list(range(2, 66)) + [2**k for k in range(1, 19)]))
    for M in Ms:
        groups = {}
        clash = []
        for v in sorted(cross):
            i, dd, rA, rF = cross[v]['cls']
            key = (i % M, dd, rA % M, rF % M, cross[v]['h'])
            if key in groups:
                v0 = groups[key]
                if cross[v0]['seq'] != cross[v]['seq']:
                    clash.append((v0, v))
                    if len(clash) >= 3:
                        break
            else:
                groups[key] = v
        results[M] = dict(ok=not clash, nclasses=len(groups), clash=clash[:3])
    minM = None
    for M in Ms:
        if results[M]['ok']:
            minM = M
            break
    print('corrected class (i mod M, d, lamA mod M, lamfront mod M, h):')
    for M in (2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 2**18):
        if M in results:
            print('   M=%-6d ok=%-5s classes=%-5d %s' % (M, results[M]['ok'], results[M]['nclasses'],
                                                          results[M]['clash'][:1]))
    print('minimal working modulus (corrected class):', minM)
    d['law_literal'] = dict(nclash=len(clashes), nonh=len(nonh), sample=clashes[:10])
    d['law2'] = {str(M): results[M] for M in Ms}
    d['minM_corrected'] = minM
    with open('revC10_t2.json', 'w') as f:
        json.dump(d, f)
    print('updated revC10_t2.json')


if __name__ == '__main__':
    main()
