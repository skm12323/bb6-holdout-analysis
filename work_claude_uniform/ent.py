"""E_NT: classes at chains 5<=j<=JMAX whose class-level walk meets an NT gate (Claude, direction A).
Class-level rules (Theorem A of work_landing_symbolic; Theorem S of work_claude_shift):
  a (k): t=3k+d; v2(t)<=j-3 -> descent j'=1+v2(t), d'=3-d;  v2(t)=j-2 -> NT gate;
         v2(t)>=j-1 -> catapult j'=j-1, d'=3-d-2^(j-1) (mod 2^j);
  b/c  : j'=omega(j-1), d'=d+3+3tau-lambda'_W (exact canonical shift);  even crossing: end.
d is a residue mod 2^(j+1).  Usage: python -B ent.py [JMAX]"""
import sys, json, time
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'work_ext_roots'))
from search_roots import Calendar
JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
cal = Calendar(512)
def v2i(t, cap):
    if t == 0: return cap
    v = 0
    while t % 2 == 0 and v < cap: t //= 2; v += 1
    return v
info = {}
for j in range(1, JMAX + 1):
    r = cal.crossing(j - 1)
    if not r['odd']: info[j] = ('end',)
    elif r['kind'] == 'a': info[j] = ('a', r['time'] // 2)
    else:
        lam = r['head_lambda'] + 2*r['tail_lambda'] + 3
        om = r['omega']; s = 3 + 3*r['time'] - lam
        assert s.denominator == 1 if hasattr(s, 'denominator') else True
        info[j] = ('bc', om, int(s), r['kind'])
# bad[j] : bytearray over residues mod 2^(j+1): 1 = class walk meets NT gate; also first-gate location
bad = {}; T0 = time.time(); stats = {}
for j in range(1, JMAX + 1):
    M = 1 << (j + 1); arr = bytearray(M); I = info[j]
    if j <= 4 or I[0] == 'end':
        bad[j] = arr; stats[j] = 0; continue
    if I[0] == 'a':
        k = I[1]
        for d in range(M):
            t = (3*k + d) % M
            v = v2i(t, j + 1)
            if v <= j - 3:
                jp = 1 + v; arr[d] = bad[jp][(3 - d) % (1 << (jp + 1))]
            elif v == j - 2:
                arr[d] = 1
            else:
                jp = j - 1; arr[d] = bad[jp][(3 - d - (1 << (j - 1))) % (1 << j)]
    else:
        _, om, s, kind = I
        assert om < j
        mm = 1 << (om + 1)
        for d in range(M):
            arr[d] = bad[om][(d + s) % mm]
    bad[j] = arr; stats[j] = sum(arr)
    print(j, I[0], stats[j], round(time.time()-T0, 1), flush=True)
def sym(d, j):
    M = 1 << (j + 1); d %= M
    return d - M if d >= M // 2 else d
out = {j: dict(kind=info[j][0], n_bad=stats[j], bad_classes=[sym(d, j) for d in range(1 << (j+1)) if bad[j][d]][:64])
       for j in range(5, JMAX + 1)}
HERE.joinpath('ent_checks.json').write_text(json.dumps(dict(JMAX=JMAX, by_j=out), indent=1), encoding='utf-8')
