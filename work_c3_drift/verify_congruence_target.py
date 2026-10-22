"""Verifier for CONGRUENCE_TARGET_NOTE.md (aud65 adversary note).

Finite exact checks only ([B]); the all-M statements are proved in the note.
Reads the accepted canonical calendar read-only from D:/math_cc; writes only
congruence_target_checks.json beside this file.
"""
from pathlib import Path
import sys, json, random

sys.path.insert(0, r'D:/math_cc/work_ext_roots')
from verify_low_deficit import Calendar, val, first_fire  # accepted calendar (B=512)

EXACT_GAP = [1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 8, 7]  # PROOF_SPECTRUM s2, P=1..15


def G(P):
    """Half-time gap bound: exact for P<=15, cubic (strict-record) bound P^3/2 above."""
    return EXACT_GAP[P - 1] if P <= 15 else P ** 3 // 2


def targetA(M, w=0):
    mod = 1 << M
    return (-pow(3, -1, mod)) % mod + w * mod      # 3k+1 = 0 mod 2^M


def targetB(M, w=1):
    return w << M                                   # k = 0 mod 2^M


def barrier_ok(k):
    """BARRIER(k): G(L(h)) <= k-h for all 1<=h<k, L(h)=v2(6h+4)."""
    return all(G(val(6 * h + 4)) <= k - h for h in range(1, k))


def main():
    cal = Calendar(512)
    out = {'status': 'PASS', 'scope': 'finite exact checks [B]; all-M proofs are in the note'}

    # 1. Lemma K(a)/(b) on random actual fires.
    random.seed(65)
    lk = 0
    for _ in range(400):
        t = random.randrange(2, 1 << random.randrange(4, 200))
        f = cal.preceding_fire_by_time(2 * t)
        a = cal.crossing(f['pointer']); b = cal.crossing(f['pointer'] + 1)
        assert a['odd'] and a['kind'] == 'a' and a['time'] == 2 * f['k']
        assert b['odd'] and b['kind'] == 'b' and b['omega'] == val(6 * f['k'] + 4)
        lk += 1
    out['lemmaK_fire_checks'] = lk

    # 2. Analytic inequalities of Lemma CT, checked on finite ranges.
    for P in range(2, 4097):
        r = P - 1
        sA = ((1 << r) + 1 + 2) // 3          # ceil((2^r+1)/3)
        sB = ((1 << r) + 2 + 2) // 3          # ceil((2^r+2)/3)
        assert sA >= G(P) and (P == 2 or sB >= G(P))
    for M in range(16, 4097):
        assert ((1 << M) + 1) * 2 >= 3 * (M + 2) ** 3   # case r>M, both classes
    out['inequality_ranges'] = 'P in [2,4096], M in [16,4096]'

    # 3. Pure-arithmetic barrier for the least targets, M=16..22.
    bar = {}
    for M in range(16, 23):
        assert barrier_ok(targetA(M)) and barrier_ok(targetB(M))
        bar[M] = 'ok'
    out['arithmetic_barrier_M16_22'] = bar

    # 4. Canonical occurrence of congruence targets, M<=249, w<=3 (both classes).
    hitsA = missA = hitsB = 0; misses = []
    for M in range(2, 250):
        for w in range(4):
            for cls, k in (('A', targetA(M, w)), ('B', targetB(M, w + 1))):
                if k < 1:
                    continue
                f = cal.preceding_fire_by_time(2 * k)
                if f['k'] == k:
                    if cls == 'A': hitsA += 1
                    else: hitsB += 1
                    assert cal.crossing(f['pointer'])['kind'] == 'a'
                else:
                    h = f['k']; P = val(6 * h + 4)
                    misses.append(dict(cls=cls, M=M, w=w, k=k, previous_fire=h,
                                       label=P, exact_gap=G(P), d=k - h,
                                       barrier_holds=barrier_ok(k)))
                    assert not barrier_ok(k) and M < 16
    out['targets'] = dict(A_hits=hitsA, B_hits=hitsB, misses=misses)

    # 5. epsilon=3 realisation at small scale: omega = v2(6k*+2) >= M+1, theta_1 = 1.
    eps3 = []
    for M in range(3, 12):
        for w in range(4):
            k = targetA(M, w)
            f = cal.preceding_fire_by_time(2 * k)
            if f['k'] != k or f['pointer'] + 1 > 300:
                continue
            P = f['pointer'] + 1
            FP = first_fire(cal, P)
            n = FP['pointer'] + 2
            c = cal.crossing(n); q = val(6 * k + 2)
            x0 = 6 * FP['k'] + 4
            assert val(x0) == P and q >= M + 1 and q < P - 1
            assert c['odd'] and c['kind'] == 'c' and c['epsilon'] == 3 and c['omega'] == q
            th1 = (1 - 1 - c['tail_lambda']) % (1 << (q + 1))      # Lemma 5.1 class at J=n+1
            assert th1 == 1 and (1 - x0 // 2) % (1 << (q + 1)) == 1   # RB phase 1-x0/2
            assert (3 * c['time'] + 4) % (1 << q) == 1              # Lemma 4.3 drift residue
            eps3.append(dict(M=M, w=w, P=P, q=q, n_bits=n.bit_length()))
    out['eps3_realisations'] = eps3

    # 6. BA formulas on all canonical BA sources P<=256 (history b then a).
    ba = []
    for P in range(5, 257):
        r = cal.crossing(P - 1)
        if not (r['odd'] and r['kind'] == 'b'):
            continue
        y = 3 * r['time'] + 4; p = val(y)
        r2 = cal.crossing(p - 1)
        if not (r2['odd'] and r2['kind'] == 'a'):
            continue
        k = r2['time'] // 2; q = val(6 * k)
        FP = first_fire(cal, P); x0 = 6 * FP['k'] + 4
        c = cal.crossing(FP['pointer'] + 2)
        assert c['odd'] and c['kind'] == 'c' and c['epsilon'] == 5 and c['omega'] == q < p - 1
        assert (-c['tail_lambda']) % (1 << (q + 1)) == 2                 # theta_1 = 2
        assert (2 - 5 * x0 // 8 - y // 2) % (1 << (q + 1)) == 2          # RB phase
        ba.append(dict(P=P, p=p, q=q))
    out['BA_sources'] = ba

    # 7. A copied b crossing has omega = copied fire parameter (p-chain of BA).
    cb = 0
    for p in range(5, 120):
        try:
            Fp = first_fire(cal, p)
        except AssertionError:
            continue
        b = cal.crossing(Fp['pointer'] + 1)
        assert b['kind'] == 'b' and b['omega'] == p
        cb += 1
    out['b_copy_checks'] = cb

    Path(__file__).with_name('congruence_target_checks.json').write_text(
        json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: (v if k != 'targets' else {kk: (vv if kk != 'misses' else len(vv)) for kk, vv in v.items()})
                      for k, v in out.items()}))


if __name__ == '__main__':
    main()
