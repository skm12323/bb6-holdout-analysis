"""gen.py -- level generator of PROOF_TIE2 section 3, re-implemented with exact Psi-family information
(REPORT.md sections 3-6).  Usage:  python -B gen.py LMAX [NPROC]
Differences from verify_tie2.py:
  * any-j families are keyed by (P,Q) (Fractions): Theta == P + Q 2^j lambda_u, lambda_u free (Lemma F1);
  * big-state representatives may be rationals P = p/q (NT by size checked: |p| small, q odd small);
  * a tie inside an any-j run is resolved by the exact Psi automaton (famlib.make_psi); a tie whose
    outcome depends on the free parameter EMITS a new any-j family Psi(.;P',Q') on j' >= jmin (Lemma F2(ii));
  * emitted families are fed back (fixpoint iteration inside the level), with landing ranges for j' >= N
    from Lemma M (catapult bound) -- only the case 'first-step tie after a big a-step with q(P_b) <= 3'
    is admitted; anything else is reported as a failure.
Writes gen_certificate.json.  Specific pairs and X records are handled exactly as in verify_tie2.py.
"""
import json, sys, time
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from pathlib import Path
import famlib as F
t2 = F.t2
N = F.N
CH = 25000
G = {}


def _init():
    Xt, typ, par, chain, real, steps = F.walk()
    G['run'] = F.ve.make_run(Xt, typ, par, chain)
    G['ext'] = t2.make_ext(Xt, typ, par, real)
    G['psi'] = F.make_psi(Xt, typ, par, real, G['ext'])
    t2.G['run'] = G['run']; t2.G['ext'] = G['ext']


def rr(P, j):
    P = Fr(P)
    return t2.ratrep(P.numerator, P.denominator, j) if P.denominator > 1 else P.numerator   # small integer rep.


def psi_entry(j, P, Q):
    """exact run of Psi(j;P,Q) after a tie was found by the plain automaton"""
    L = G['psi'](j, F.res(P), F.res(Q))
    xrec = set(); fail = None; emit = None; mx = len(L['path'])
    for (a, T, M, u, m) in L['aouts']:
        xrec.add(t2.xkey(a, T, M, u, m))
    if L['res'] == 'END':
        pass
    elif L['res'] == 'ANYJ':
        jm, Pn, Qn = L['anyj']
        emit = (jm, Pn, Qn, len(L['path']))
    elif L['res'] == 'EXT':
        _, xr, mx2, info = t2.finish(['psi', j, str(P)], L['ext'], None)
        xrec.update(xr); mx = len(L['path']) + mx2
        if info['FAIL']: fail = info
    else:
        fail = dict(res=L['res'])
    return xrec, mx, fail, emit


def task(t):
    kind, payload = t
    pairs = set(); xo = set(); dist = Counter(); fails = []; emits = []; nties = 0
    if kind == 'any':
        (pn, pd, qn, qd, j0, j1) = payload
        P = Fr(pn, pd); Q = Fr(qn, qd)
        for j in range(j0, j1):
            out, f = G['run'](j, rr(P, j))
            if f is None:
                pairs.update(t2.canon(a, b) for a, b, kd in out if kd == 'a'); dist[len(out)] += 1
                continue
            nties += 1
            xr, mx, fail, emit = psi_entry(j, P, Q)
            xo.update(xr); dist[mx] += 1
            if fail: fails.append(('any', str(P), str(Q), j, str(fail)[:300]))
            if emit:
                jm, Pn, Qn, depth = emit
                emits.append((P, Q, j, jm, Pn, Qn, depth))
    elif kind == 'pair':
        for (j, th), why in payload:
            ao, xr, mx, info = t2.go(j, th)
            pairs.update(ao); xo.update(xr); dist[mx] += 1
            if info:
                nties += 1
                if info['FAIL']: fails.append(('pair', j, th, str(why)[:200], str(info['leaves'][:2])[:300]))
    else:
        for key, why in payload:
            _, xr, mx, info = t2.gox(key)
            xo.update(xr); dist[mx] += 1; nties += 1
            if info['FAIL']: fails.append(('x', key[:2], str(why)[:200]))
    return pairs, xo, dist, fails, emits, nties


def ident(x, dens=(1, 3, 9, 27, 81, 243, 5, 15, 45, 11, 33, 21, 7), H=10**5):
    """recognise a 2-adic residue (mod 2^PREC) as a rational of small height (exact: PREC=2048 bits)"""
    for d in dens:
        y = (x * d) % F.MOD
        if y < H: return Fr(y, d)
        if F.MOD - y < H: return Fr(y - F.MOD, d)
    raise ValueError('unrecognised 2-adic number')


def nt_by_size(P):
    """(S-a) for a chain with j >= N and Theta == P (mod 2^j), P = p/q: 0 < |p+3qk| < 2^(j-2) for all
    (j-2)/4 <= k <= (j-1)^2/2 (k_n >= (n-1)/4 since the pointer advances <= 2 per step; (C1))."""
    p, q = P.numerator, P.denominator
    return abs(p) < 3 * q * (N - 2) // 4 - 1 and q < 10**4


def main():
    import multiprocessing as mp
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    NPROC = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    t0 = time.time()
    F.walk()
    pool = mp.Pool(NPROC, initializer=_init)

    def runall(tasks):
        pairs = set(); xo = set(); dist = Counter(); fails = []; emits = []; nt = 0
        for p, x, d, fl, em, n in pool.imap_unordered(task, tasks, chunksize=1):
            pairs |= p; xo |= x; dist.update(d); fails += fl; emits += em; nt += n
        return pairs, xo, dist, fails, emits, nt
    # level 0: fires (J,1), 2 <= J < N
    A0, _, d0, f0, e0, _ = runall([('any', (1, 1, 1, 1, j, min(j + CH, N))) for j in range(2, N, CH)])
    assert not f0 and not e0 and max(d0) <= 2
    AO = {0: (set(), set(A0), set())}
    report = {}
    for l in range(1, LMAX + 1):
        big = {i: defaultdict(list) for i in range(1, l)}
        small_any = defaultdict(list); small_spec = defaultdict(list); small_x = defaultdict(list)
        aany = set()

        def add(i, P, Q, why):
            P = Fr(P); Q = Fr(Q)
            if i == 0: small_any[(P, Q)].append(why)
            else: big[i][P].append(why)

        def addx(rec, shift, Mcap, why):
            j, T, M, u, m = rec
            M2 = min(M, Mcap)
            small_x[t2.xkey(j, (T + F.res(shift, M2)) % (1 << M2), M2, u, m)].append(why)
        for i in range(0, l):
            add(i, 2, 1, ('chain1-a', l)); add(i, 0, 1, ('chain1-b', l)); aany.add((i, Fr(2), Fr(1)))
        for lw in range(0, l):
            anyw, specw, xw = AO[lw]
            for (i, Pw, Qw) in anyw: add(i, Pw - 1, Qw, ('chain1-c-any', lw, i, str(Pw)))
            for (jw, tw) in specw: small_spec[t2.canon(jw, tw - 1)].append(('chain1-c', lw))
            for rec in xw: addx(rec, -1, 10**9, ('chain1-cX', lw))
        done_big = {i: set() for i in range(1, l)}
        done_small = set()
        allpairs = set(); allx = set(); dist = Counter(); fails = []; emits_all = []; nties = 0; nent = 0
        it = 0
        while True:
            it += 1
            # process big states (descending ranges), only new ones
            for i in range(l - 1, 0, -1):
                for P in sorted(set(big[i]) - done_big[i]):
                    done_big[i].add(P)
                    if not nt_by_size(P): fails.append(('big-not-NT', i, str(P)))
                    for i2 in range(0, i):
                        add(i2, 3 - P, 1, ('big-a', i, str(P))); aany.add((i2, 3 - P, Fr(1)))
                        add(i2, P - 1, 1, ('big-b', i, str(P)))
                    for lw in range(0, i):
                        anyw, specw, xw = AO[lw]
                        for (i2, Pw, Qw) in anyw: add(i2, P + Pw - 2, Qw, ('big-c-any', i, str(P), lw))
                        for (jw, tw) in specw:
                            small_spec[(jw, (rr(P, jw) + tw - 2) % (1 << jw))].append(('big-c', i, str(P), lw))
                        for rec in xw: addx(rec, P - 2, N, ('big-cX', i, str(P), lw))
            new_any = sorted(set(small_any) - done_small, key=lambda pq: (pq[0], pq[1]))
            tasks = []
            for (P, Q) in new_any:
                done_small.add((P, Q))
                tasks += [('any', (P.numerator, P.denominator, Q.numerator, Q.denominator, j, min(j + CH, N))) for j in range(1, N, CH)]
            if it == 1:
                sp = sorted((k, v[:3]) for k, v in small_spec.items())
                tasks += [('pair', sp[a:a + 20]) for a in range(0, len(sp), 20)]
                sx = sorted((k, v[:3]) for k, v in small_x.items())
                tasks += [('x', sx[a:a + 5]) for a in range(0, len(sx), 5)]
                spec_done = set(small_spec); x_done = set(small_x)
            else:
                sp = sorted((k, v[:3]) for k, v in small_spec.items() if k not in spec_done)
                tasks += [('pair', sp[a:a + 20]) for a in range(0, len(sp), 20)]
                sx = sorted((k, v[:3]) for k, v in small_x.items() if k not in x_done)
                tasks += [('x', sx[a:a + 5]) for a in range(0, len(sx), 5)]
                spec_done |= set(small_spec); x_done |= set(small_x)
            if not tasks: break
            pairs, xo, d, fl, em, nt = runall(tasks)
            allpairs |= pairs; allx |= xo; dist.update(d); fails += fl; nties += nt; nent += sum(d.values())
            # emissions: new any-j families (Lemma F2(ii)) and their landing ranges (Lemma M)
            byfam = defaultdict(list)
            for (P, Q, j, jm, Pn, Qn, depth) in em:
                byfam[(ident(Pn), ident(Qn))].append((str(P), str(Q), j, jm, depth))
            lands = defaultdict(set)
            for (Pn, Qn), lst in byfam.items():
                emits_all.append((str(Pn), str(Qn), sorted(set(lst))[:10], len(lst)))
                add(0, Pn, Qn, ('emit', sorted(set((a, b) for a, b, _, _, _ in lst))))
                aany.add((0, Pn, Qn))
                # landing for j' >= N (Lemma M): origin = big a-step from (R_i, P_b) or the fire (chain 1),
                # tie at the first step after it (depth 0), q(P_b) <= 3  ==>  j' < T_i  (ranges 1..i-1)
                for (sP, sQ, j, jm, depth) in lst:
                    for why in small_any[(Fr(sP), Fr(sQ))]:
                        if why[0] == 'big-a' and depth == 0 and Fr(why[2]).denominator <= 3:
                            for i2 in range(1, why[1]): lands[i2].add(Pn)
                        elif why[0] in ('chain1-a', 'chain1-b') and depth == 0:
                            for i2 in range(1, why[1]): lands[i2].add(Pn)
                        else:
                            fails.append(('emission-landing-unproved', str(Pn), str(Qn), sP, sQ, j, depth, str(why)[:120]))
            for i2, Ps in lands.items():
                for Pn in Ps:
                    big[i2][Pn].append(('catapult',))
                    for (Pe, Qe) in byfam:
                        if Pe == Pn: aany.add((i2, Pn, Qe))     # the catapulted chain is an a-output in R_i2
        AO[l] = (aany, allpairs, allx)
        rep = dict(level=l, iterations=it,
                   big={i: sorted(str(p) for p in big[i]) for i in big},
                   small_any=sorted('%s|Q=%s' % (str(p), str(q)) for (p, q) in small_any),
                   n_small_spec=len(small_spec), n_small_x=len(small_x), entries=nent,
                   dist=dict(sorted(dist.items())), max_further=max(dist), n_ties_resolved=nties,
                   n_fail=len(fails), fails=fails[:40], emissions=emits_all,
                   n_aout_pairs=len(allpairs), n_aout_x=len(allx),
                   aout_any=sorted('%d:%s|%s' % (i, str(p), str(q)) for (i, p, q) in aany),
                   seconds=round(time.time() - t0))
        report[l] = rep
        print('LEVEL', l, json.dumps({k: rep[k] for k in rep if k not in ('fails',)}, default=str), flush=True)
        for fl in fails[:12]: print('   FAIL', fl, flush=True)
        Path(__file__).with_name('gen_certificate.json').write_text(json.dumps(report, indent=1, default=str) + '\n')
    pool.close(); pool.join()


if __name__ == '__main__':
    main()
