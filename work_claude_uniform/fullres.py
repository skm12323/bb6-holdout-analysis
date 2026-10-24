"""Independent full-residue certify scan for 5<=j<=18 (Claude, direction A).
certify(j,delta): exact walk from (x,Theta)=(2^j, 2^j+delta) never hits x<=0, ends at an even crossing, and has
all records j_t+Gamma_t <= j (HP then transfers it to any real chain whose class mod 2^(j+1) is delta)."""
import sys, json, time
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(ROOT/'work_ext_roots'))
from search_roots import Calendar
cal = Calendar(512)
rows = {}
for n in range(0, 600):
    r = cal.crossing(n)
    if not r['odd']: rows[n] = None
    elif r['kind'] == 'a': rows[n] = ('a', r['time'])
    else:
        ratio = (r['head_ratio'] + 2*r['tail_ratio'])/2
        lam = r['head_lambda'] + 2*r['tail_lambda'] + 3
        rows[n] = ('bc', r['time'], ratio, lam, r['epsilon'])
def v2(n):
    return (n & -n).bit_length() - 1
def certify(j0, d):
    x = 1 << j0; th = x + d; j = j0; G = 0
    for _ in range(400):
        if x <= 0: return False
        r = rows[j - 1]
        if r is None: return True
        if r[0] == 'a':
            assert x % 2 == 0
            x = 2*th + 3*r[1] - x//2; th += 3 + 3*r[1]; G += 1
        else:
            _, tau, ratio, lam, eps = r
            xn = ratio*x + lam; assert xn.denominator == 1; x = int(xn)
            th += 3 + 3*tau; G += 1 + eps
        if x <= 0: return False
        j = v2(x)
        if j + G > j0: return False
    raise RuntimeError('limit')
T0 = time.time(); out = {}
for j in range(5, 19):
    if rows[j - 1] is None: continue
    M = 1 << (j + 1); fails = []
    for d in range(M):
        if not certify(j, d + (M << (j + 1))):     # positive lift of the class (x>0 throughout)
            fails.append(d - M if d >= M//2 else d)
    alt = [dd for dd in range(M) if not certify(j, dd + (M << (j + 7)) + M)]   # a second, different lift
    assert sorted((a - M if a >= M//2 else a) for a in alt) == sorted(fails), ('lift dependence', j)
    out[j] = fails
    print(j, len(fails), fails[:8], round(time.time() - T0, 1), flush=True)
HERE.joinpath('fullres_checks.json').write_text(json.dumps(dict(failures=out, total=sum(len(v) for v in out.values())), indent=1), encoding='utf-8')
