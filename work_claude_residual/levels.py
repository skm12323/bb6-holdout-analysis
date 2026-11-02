"""levels.py -- scale-by-scale a-output class sets and certification of every possible entry (Claude, residual).

[B] exhaustive over the canonical table (indices < N_T = 2*10^7 = N0), with the over-approximations of NOTES.md §3.
A class set is (E, G): E = {(chain, residue mod 2^(chain+1))} of a-outputs at specific chains, G = small integer
classes that may occur as a-outputs at ANY chain (route-a chain 1, deep->shallow a-steps).
  A   : sources S(Q), 5 <= Q <= N_T, exact (entry (Q,1) at every Q).
  B   : N_T < Q < T1   : chain-1 entries a:2, b:0 (any chain), root-c (w, D-1), D in A.            G_B={2}
  C   : T1 <= Q < T2   : + deep chain 1 (D1 in {0,2}): 3-D1, D1-1 (any chain), (w, D1+D-2), D in A.   G_C={1,2,3}
  D   : T2 <= Q < T3   : root-c (w,D-1) D in ABC; depth-2 (w,D1+D-2) D1 in {0,1,2}, D in AB;
                         depth-3 (w,D2+D-2) D2 in {-1..3}, D in A; a/b landings in [-2,4].              G_D={0..4}
  OUT : H5_res entries of a source epoch P < T3 with L <= 2 large-phase letters: identical shape to D.
  C7  : c landings of S(J), J < T4: from deep chain t with theta_t in [1-t,t+1]: (w, theta+D-2), D in
        ABCD (t=0), ABC (t=1), AB (t=2), A (t=3);  a/b landings 3-theta, theta-1 reported too.
Integer entries at all chains use exhaustive bulk runs; specific (chain, residue) entries are certified one by one.
Uncertified entries are reported with provenance, never dropped.
Usage: python -B levels.py [jmax]      (jmax default = table size; writes levels_<jmax>.json)
"""
import sys, json, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rwalk as R

T0 = time.time()
T = R.Table()
JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else T.N
INTS = range(-8, 11)


def sym(r, c):
    M = 1 << (c + 1); r %= M
    return r - M if r > M // 2 else r


# ---- bulk runs: entries (j, delta) for every 5 <= j <= JMAX, integer delta in INTS
E = {}; UNC = {}; NT = {}
for d in INTS:
    agg = {}; unc = []; ntc = {}
    for j in range(5, min(R.BIG, JMAX + 1)):
        c = R.certify(T, j, d)
        if not c['ok']:
            unc.append(j)
        for a in c['aouts']:
            e = agg.setdefault(a, [0, ('bulk', d, j)]); e[0] += 1
        for q in c['nt']:
            ntc[q] = ntc.get(q, 0) + 1
    if JMAX >= R.BIG:
        B = R.bulk(T, d, R.BIG, JMAX + 1)
        unc += B['uncert']
        for k, v in B['aout'].items():
            e = agg.setdefault(k, [0, ('bulk', d, v[1])]); e[0] += v[0]
        for q, v in B['nt'].items():
            ntc[q] = ntc.get(q, 0) + v
    E[d] = agg; UNC[d] = unc; NT[d] = ntc
    print('delta', d, 'aouts', len(agg), 'uncert', len(unc), unc[:6], 'nt', sum(ntc.values()),
          round(time.time() - T0, 1), flush=True)

memo = {}


def cert_specific(c, r):
    key = (c, r % (1 << (c + 1)))
    if key not in memo:
        memo[key] = R.certify(T, c, sym(r, c))
    return memo[key]


summary = {}


def level(name, plan, ints, generic_out):
    """plan: list of (E_prev, G_prev, dset, tag).  ints: integer entry classes at every chain (deep a/b landings).
    Returns (E_out, G_out)."""
    all_ints = {}            # delta -> provenance (entries at every chain)
    spec = {}                # (chain, residue) -> provenance
    for d in ints:
        all_ints.setdefault(d, (name, 'a/b-landing'))
    for Ep, Gp, ds, tag in plan:
        for d in ds:
            for g in Gp:
                all_ints.setdefault(d + g - 2, (name, tag, 'generic', d, g))
            for (c, D), prov in Ep.items():
                if c < 5:
                    continue
                r = (d + D - 2) % (1 << (c + 1))
                spec.setdefault((c, r), (name, tag, d, c, sym(D, c), prov))
    unc = []; Eo = {}
    for d, prov in sorted(all_ints.items()):
        assert d in INTS, ('integer entry outside bulk range', d)
        if UNC[d]:
            unc.append(dict(kind='all-chain integer', cls=d, chains=UNC[d][:10], why=prov))
        for k, v in E[d].items():
            Eo.setdefault(k, v[1])
    n_spec = 0
    for (c, r), prov in spec.items():
        s = sym(r, c)
        if s in INTS and s in all_ints:
            continue                                   # covered by the all-chain bulk run
        n_spec += 1
        q = cert_specific(c, r)
        if not q['ok']:
            unc.append(dict(kind='specific', chain=c, cls=s, status=q['status'], word=q['word'][:12], why=prov))
            continue
        for a in q['aouts']:
            Eo.setdefault(a, ('spec', name, c, s))
    summary[name] = dict(n_classes=len(Eo), generic_out=sorted(generic_out), all_chain_integer_entries=sorted(all_ints),
                         n_specific_entries=n_spec, uncert=unc,
                         chain5=sorted({sym(r, c) for (c, r) in Eo if c == 5}),
                         exotic=sorted({(c, sym(r, c)) for (c, r) in Eo if sym(r, c) not in range(-20, 21)}))
    print(name, 'classes', len(Eo), 'specific', n_spec, 'uncert', unc, round(time.time() - T0, 1), flush=True)
    return Eo, set(generic_out)


def U(*Es):
    out = {}
    for Ed in Es:
        for k, v in Ed.items():
            out.setdefault(k, v)
    return out


EA = {k: v[1] for k, v in E[1].items()}; GA = set()
summary['A'] = dict(n_classes=len(EA), classes_sym=sorted({sym(r, c) for (c, r) in EA}),
                    chain5=sorted({sym(r, c) for (c, r) in EA if c == 5}), uncert_Q=UNC[1][:20])
EB, GB = level('B', [(EA, GA, [1], 'root-c')], [2, 0], {2})
EAB, GAB = U(EA, EB), GA | GB
EC, GC = level('C', [(EAB, GAB, [1], 'root-c'), (EA, GA, [0, 2], 'depth2-c')], [2, 0, 3, 1, -1], {1, 2, 3})
EABC, GABC = U(EAB, EC), GAB | GC


def shapeD(tag):
    return [(EABC, GABC, [1], tag + '0'), (EAB, GAB, [0, 1, 2], tag + '1'), (EA, GA, [-1, 0, 1, 2, 3], tag + '2')]


EO, GO = level('OUT', shapeD('L'), list(range(-2, 5)), {0, 1, 2, 3, 4})
ED, GD = level('D', shapeD('depth'), list(range(-2, 5)), {0, 1, 2, 3, 4})
EABCD, GABCD = U(EABC, ED), GABC | GD
EL, GL = level('C7', [(EABCD, GABCD, [1], 't0'), (EABC, GABC, [0, 1, 2], 't1'), (EAB, GAB, [-1, 0, 1, 2, 3], 't2'),
                      (EA, GA, list(range(-2, 5)), 't3')], [], set())
abl = sorted({3 - t for t in range(-2, 5)} | {t - 1 for t in range(-2, 5)})
summary['C7_ab_landings_uncert'] = {str(d): UNC[d][:10] for d in abl}
summary['bulk'] = {str(d): dict(aouts=len(E[d]), n_uncert=len(UNC[d]), uncert=UNC[d][:30],
                                nt={'%d->%d' % k: v for k, v in sorted(NT[d].items())}) for d in INTS}
for name, S, Gs in (('A', EA, GA), ('B', EB, GB), ('C', EC, GC), ('D', ED, GD)):
    sig = {}
    for (c, r) in S:
        if c >= 5:
            sig.setdefault(c, set()).add(sym(r - 2, c))
    summary['sigma_' + name] = dict(generic_all_chains=sorted(g - 2 for g in Gs),
                                    by_chain={str(c): sorted(v) for c, v in sorted(sig.items())})
    summary['chain_hist_' + name] = {str(c): len({r for (cc, r) in S if cc == c}) for c in sorted({c for c, _ in S})}
summary.update(jmax=JMAX, seconds=round(time.time() - T0, 1),
               scope='[B] canonical table indices < 2*10^7 (chains < N0); over-approximated entry sets (NOTES.md §3).')
HERE.joinpath('levels_%d.json' % JMAX).write_text(json.dumps(summary, indent=1, default=str) + '\n', encoding='utf-8')
print(json.dumps({k: summary[k] for k in ('A', 'B', 'C', 'OUT', 'D', 'C7', 'C7_ab_landings_uncert')}, default=str)[:9000])
