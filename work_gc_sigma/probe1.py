"""probe1.py -- timing + aout-class probe for the key families (scratch, not a deliverable)."""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'work_gc_level_t5'))
sys.path.insert(0, str(ROOT / 'work_claude_residual'))
import rwalk as R
import rwalk_t5 as W

t0 = time.time()
T = R.Table()
print('table loaded', round(time.time()-t0, 1), 's, N =', T.N)

def classify(aout, maxden_pow=12, maxnum=400):
    """classify residues (c, r) as num/den (+ lift 2^m, m<=c) with small numerator."""
    out = {}
    for (c, r), (cnt, ex) in aout.items():
        if c < 5:
            continue
        found = []
        for e in range(0, maxden_pow+1):
            den = 3**e
            for m in [None] + list(range(5, min(c, 64)+1)):
                r2 = r if m is None else (r - (1 << m)) % (1 << (c+1))
                num = (r2 * den) % (1 << (c+1))     # num/den == r2 mod 2^{c+1}
                if num > (1 << c):
                    num -= (1 << (c+1))
                if abs(num) <= maxnum:
                    found.append((num, den, m))
        out[(c, r)] = (cnt, ex, found)
    return out

for fam in [(10, 3, True), (26, 3, True)]:
    t1 = time.time()
    d = W.family_cert_full = None
    # replicate family_cert from levels_t5 (scalar part + bulk)
    num, den, lift = fam
    t1 = time.time()
    unc_s = []; aout_s = {}
    for j in range(5, 64):
        c = W.certify_rat(T, j, num, den, lift)
        if not c['ok']:
            unc_s.append((j, c['status'], tuple(c['word'][:8])))
            continue
        ntout = {b for (_, b) in c['nt']}
        for (c2, r2) in c['aouts']:
            if c2 in ntout or c2 >= j+1:
                continue
            aout_s[(c2, r2)] = aout_s.get((c2, r2), 0) + 1
    print(fam, 'scalar done', round(time.time()-t1, 1), 'unc_s:', unc_s)
    t2 = time.time()
    B = W.bulk_rat(T, num, den, lift, 64, 400000)
    print(fam, 'bulk [64,4e5) done', round(time.time()-t2, 1), 's uncert:', len(B['uncert']), 'aout classes:', len(B['aout']))
    t3 = time.time()
    B2 = W.bulk_rat(T, num, den, lift, 64, T.N + 1)
    print(fam, 'bulk FULL done', round(time.time()-t3, 1), 's uncert:', len(B2['uncert']), 'aout classes:', len(B2['aout']))
    aa = dict(B2['aout']); 
    for k, v in aout_s.items():
        e = aa.setdefault(k, [0, 5]); e[0] += v
    cl = classify(aa)
    vals = {}
    for (c, r), (cnt, ex, found) in cl.items():
        for (num2, den2, m) in found:
            vals.setdefault((num2, den2, m), [0, c, r])
            vals[(num2, den2, m)][0] += cnt
    print('  classified distinct (num,den,lift) values:', len(vals))
    for k in sorted(vals, key=lambda x: (x[1], x[0], -1 if x[2] is None else x[2])):
        print('   ', k, 'count', vals[k][0], 'e.g. chain', vals[k][1])
