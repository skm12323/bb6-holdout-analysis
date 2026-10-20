"""check_small.py -- exact finite checks for DIRECTION C (agent_C), small range.

  V1  c-landing class formula, exact big-int one-step check at every odd type-c
      crossing n < NS, for 11 defects x 6 arguments:
      Theta' = Theta+3+3 tau, x' = c'_W u + lambda'_W, j' = omega(n), and
      D' = Theta'-x'  ==  theta + 3 tau + 3 - 2^j'  (mod 2^(j'+1)).
  V2  exhaustive Bad_j = {delta mod 2^(j+1) : certify(j,delta) fails} for
      5 <= j <= JMAX (cost sum 2^(j+1) walks).
  V3  Bad_j vs first-chain tie classes; tau-residue form
      tau == tau_0 = 3^-1 (2^(j-2) - 3 k_(j-1) - theta - 3)  (mod 2^(j-1)).
  V4  gateway (b/c -> j=5 -> a) two-step identity, exact big ints, at canonical
      omega=5 type-c crossings.
  V5  parity/drift diagnostics of the canonical data (tau parity at odd type-c,
      omega distribution, lambda_Y parity).

Usage: python -B check_small.py [NS] [JMAX]
Writes check_small.json beside this script.  Read-only on the repository.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import clib  # noqa: E402

NS = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
JMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 22
CACHE = Path(r'D:\math_cc_astra\deep1')
RES = dict(NS=NS, JMAX=JMAX, stage_seconds={}, checks={})
T0 = time.time()


def log(*a):
    print(round(time.time() - T0, 2), *a, flush=True)


T = clib.Table(str(CACHE / 'table_1000000.pkl'), NS=max(NS, 2048))
log('table loaded, N =', T.N)

# ------------------------------------------------------------------ V5 first (cheap)
odd_c = [n for n in range(6, min(NS, T.N)) if T.odd(n) and T.typ[n] == 99]
odd_a = [n for n in range(4, min(NS, T.N)) if T.odd(n) and T.typ[n] == 97]
from collections import Counter
v5 = dict(
    odd_c_count=len(odd_c),
    odd_a_count=len(odd_a),
    tau_even_at_odd_a=sum(1 for n in odd_a if T.tau[n] % 2 == 0),
    omega_dist={str(k): v for k, v in sorted(Counter(clib.v2(T.lam(n)) for n in odd_c).items())},
    lam_even_at_odd_c=sum(1 for n in odd_c if T.lam(n) % 2 == 0),
    tau_parity_by_omega={str(k): dict(sorted(Counter(T.tau[n] % 2 for n in odd_c
                                                   if clib.v2(T.lam(n)) == k).items()))
                         for k in sorted(set(clib.v2(T.lam(n)) for n in odd_c))},
    lY_parity_by_tau_parity={str(k): v for k, v in
                             sorted(Counter((T.lY[n] % 2, T.tau[n] % 2) for n in odd_c).items())},
)
RES['checks']['V5_parity'] = v5
log('V5', {k: v5[k] for k in ('odd_c_count', 'omega_dist', 'tau_even_at_odd_a')})

# ------------------------------------------------------------------ V1 class formula
tested = 0
mism = []
for n in odd_c:
    j = n + 1
    om = clib.v2(T.lam(n))
    cW = T.cW[n]
    assert clib.v2(cW) == T.sigma(n), ('sigma mismatch', n)
    for th in (1, 0, -1, 2, -2, 3, -3, 5, -11, 17, -17):
        for u in (1, 3, 5, 7, 12345, (1 << 40) + 1):
            x = (1 << j) * u
            Th = x + th                 # exact defect theta at the deep chain
            xp = cW * u + T.lam(n)
            Thp = Th + 3 + 3 * T.tau[n]
            jp = clib.v2(xp)
            Dp = Thp - xp
            M = 1 << (jp + 1)
            lhs = Dp % M
            rhs = (th + 3 * T.tau[n] + 3 - (1 << jp)) % M
            tested += 1
            if lhs != rhs or jp != om:
                mism.append([n, th, u, jp, om, lhs, rhs])
RES['checks']['V1_class_formula'] = dict(tested=tested, mismatches=len(mism), first=mism[:3])
log('V1 class formula: tested', tested, 'mismatches', len(mism))

# ------------------------------------------------------------------ V2 exhaustive Bad_j
t = time.time()
Bad = {}
for j in range(5, JMAX + 1):
    Bad[j] = clib.bad_set(T, j)
RES['stage_seconds']['V2_bad_sets'] = round(time.time() - t, 1)
log('V2 Bad_j computed', {j: len(v) for j, v in Bad.items()}, 'in', RES['stage_seconds']['V2_bad_sets'], 's')
RES['checks']['V2_bad_sizes'] = {str(j): len(v) for j, v in Bad.items()}
RES['checks']['V2_bad_sets'] = {str(j): v for j, v in Bad.items()}

# ------------------------------------------------------------------ V3 structure of Bad_j
struct = {}
for j in range(5, JMAX + 1):
    M1 = 1 << (j - 1)
    tie = clib.first_chain_tie_class(T, j)
    tc = None if tie is None else tie % M1
    classes = sorted(set(d % M1 for d in Bad[j]))
    entry = dict(n_bad=len(Bad[j]), n_classes_mod_2j1=len(classes),
                 odd_a=T.odd(j - 1) and T.typ[j - 1] == 97,
                 tie_class=tc, classes=classes[:12])
    if tc is not None:
        entry['bad_iff_tie_class'] = (classes == [tc])
    else:
        entry['bad_iff_tie_class'] = (len(classes) == 0)
    # tau-residue form: tau_0(theta) mod 2^(j-1)
    if tc is not None:
        inv3 = pow(3, -1, M1)
        entry['tau0_theta'] = {str(th): (inv3 * (tc - th - 3 + (1 << j))) % M1 for th in range(-3, 4)}
        # every bad delta must realise the same tau residue mod 2^(j-1)
        entry['tau_residues_of_bad'] = sorted(set(
            (pow(3, -1, 1 << (j + 1)) * (d - 1 - 3 + (1 << j))) % M1 for d in Bad[j]))
    else:
        entry['tau_residues_of_bad'] = []
    struct[str(j)] = entry
RES['checks']['V3_structure'] = struct
log('V3 structure: odd-a j in range with Bad nonempty:',
    [j for j in range(5, JMAX + 1) if Bad[j]])

# ------------------------------------------------------------------ V4 gateway identity
gw = []
w5 = [n for n in odd_c if clib.v2(T.lam(n)) == 5]
for n in w5[:6]:
    cW = T.cW[n]
    lamW = T.lam(n)
    assert clib.v2(cW) == T.sigma(n) and T.sigma(n) >= 6
    for jp in (61, 1000, 20000 + 17):
        for th in (1, 0, -1, 2, -2, 4, -4, 5):
            for up in (1, 3, (1 << 30) + 1, (1 << 200) + 7):
                # state at the deep chain: (jp, Theta = 2^jp up + th, x = 2^jp up)
                x = (1 << jp) * up
                Th = x + th
                # c-step with omega = 5
                x5 = cW * up + lamW
                Th5 = Th + 3 + 3 * T.tau[n]
                j5 = clib.v2(x5)
                assert j5 == 5, (n, j5)
                # a-step at j=5 (X(4) odd type a, k=1)
                k5 = T.tau[4] // 2
                assert T.typ[4] == 97 and T.odd(4) and k5 == 1
                x2 = 2 * Th5 + 6 * k5 - (x5 >> 1)
                j2 = clib.v2(x2)
                Q = 2 * th + 12 + 6 * T.tau[n] - lamW // 2
                gap = clib.v2((1 << (jp + 1)) - cW // 2)
                gw.append(dict(n=n, jp=jp, th=th, j2=j2, v2Q=(clib.v2(abs(Q)) if Q else 999),
                               gap=gap, sigma=T.sigma(n),
                               size_ok=(abs(Q) < (1 << (T.sigma(n) - 1)))))
RES['checks']['V4_gateway'] = dict(
    n_cases=len(gw),
    v2Q_lt_gap=sum(1 for g in gw if g['v2Q'] < g['gap']),
    size_ok=sum(1 for g in gw if g['size_ok']),
    examples=gw[:4])
log('V4 gateway identity:', RES['checks']['V4_gateway']['n_cases'], 'cases,',
    RES['checks']['V4_gateway']['v2Q_lt_gap'], 'with v2(Q)<gap,' ,
    RES['checks']['V4_gateway']['size_ok'], 'with |Q|<2^(sigma-1)')

RES['seconds_total'] = round(time.time() - T0, 1)
with open(HERE / 'check_small.json', 'w', encoding='utf-8') as f:
    json.dump(RES, f, indent=1)
log('written check_small.json, total', RES['seconds_total'], 's')
