"""Step 2 checks (Claude, 2026-10-27).
(1) HL1 on the canonical table: every odd b/c crossing n has omega(n) <= floor(log2(6 tau(n)+5)) (MASS) [B check of an A fact].
(2) Band width: A_max(J) bound for the automaton height before the first non-descent of S(J), and the largest chain j at
    which a non-descent is arithmetically possible: 2^(j-2) <= 3^r (3 k_j + A + 3/2), using exact k_j (j<400) / CLOCK.
Usage: python -B band.py N"""
import sys, math, pickle, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'work_ext_roots'))
from search_roots import Calendar
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
D = pickle.load(open(r'D:/math_cc_astra/deep1/table_%d.pkl' % N, 'rb'))
typ, odd, tau, lY, lA = D['typ'], D['odd'], D['tau'], D['lY'], D['lA']
def v2(x): return (x & -x).bit_length() - 1
bad = 0; cnt = 0; tight = 0
for n in range(4, N):
    if not odd[n] or typ[n] == 97: continue
    lam = lA[n] + 2*lY[n] + 3; cnt += 1
    assert 0 < lam <= 6*tau[n] + 5
    om = v2(lam)
    if om > math.floor(math.log2(6*tau[n] + 5)): bad += 1
    if lam == 6*tau[n] + 5: tight += 1
print('HL1', cnt, 'violations', bad, 'lambda=6tau+5 cases', tight, flush=True)
cal = Calendar(512)
oddA = [(j, cal.crossing(j-1)['time']//2) for j in range(5, 400)
        if cal.crossing(j-1)['odd'] and cal.crossing(j-1)['kind'] == 'a']
P = lambda n: 2*math.ceil(math.log2(6*n*n+5))**2 + 1345
def G2log(lJ):          # log2 of 6 J P(J) + 5 for J=2^lJ (float)
    return lJ + math.log2(6*(2*math.ceil(2*lJ + 3)**2 + 1345))
def amax(lJ, c=19.5):
    """automaton height bound before the first non-descent: 1/2 + first-step shift + later shifts, worst chain path."""
    A = 0.5 + (4*lJ + 4 + 1)/2 + c          # first step: c copy with 1+eps <= 4 log2 J + 4
    y = G2log(lJ)                           # next chain <= 6JP(J)+5 in log2 (worst case)
    while y > 5:
        A += (4*math.log2(max(y, 2)) + 5)/2 + c
        y = math.log2(6*y*P(int(y)+1) + 5)
        if y > 1e6: break
        if y < 30: A += 30; break           # small-chain tail: crude allowance
    return A
def band(A, r):
    best = 4
    for j, k in oddA:
        if 2**(j-2) <= 3**r*(3*k + A + 1.5): best = j
    return best
rows = []
for lJ in (10, 20, 40, 100, 1000, 10**4, 10**5, 10**6, 10**9, 10**12):
    A = amax(lJ)
    rows.append(dict(log2J=lJ, A_max=round(A, 1), band_r0=band(A, 0), band_r1=band(A, 1), band_r4=band(A, 4),
                     band_r8=band(A, 8)))
for r in rows: print(r)
HERE.joinpath('band_checks.json').write_text(json.dumps(dict(N=N, HL1=dict(crossings=cnt, violations=bad), band=rows,
    note='A_max is a crude worst-case automaton height (shift bound |s|<=(eps+1)/2+19.5); band = largest odd-a chain where a non-descent is arithmetically possible.'),
    indent=1), encoding='utf-8')
