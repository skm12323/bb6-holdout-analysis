"""verify_R1_summary.py -- summarise the source-map pickles written by verify_R1_src.py.

For every odd type-c crossing n < N the source map stores (n, n', lambda_u, A) with
  n'     = j_{t'}-1            (source chain parameter minus 1)
  lambda_u                     (odd base of the source chain)
  A      = 6*tau(n)+4-3*tau(n')
and Lemma S (NOTES Section 4) asserts lambda'_W(n) = A - 2^{n'}*lambda_u.
This script reports, per range, the cancellation statistic 2^{n'} | A and v2(A).

Usage: python -B verify_R1_summary.py src_100000000.pkl [src_20000000.pkl ...]
Writes verify_R1_src_summary.json beside itself.
"""
import sys, os, json, pickle
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
N0 = 2 * 10 ** 7

def v2(x):
    return (x & -x).bit_length() - 1

def go(path):
    with open(path, 'rb') as f:
        D = pickle.load(f)
    Cn, Cnp, Clu, CA = D['Cn'], D['Cnp'], D['Clu'], D['CA']
    stat = D['stat']
    out = dict(table=os.path.basename(path), N=D['N'], seconds=D['seconds'],
               walk_stat={k: v for k, v in stat.items() if k not in ('om', 'src_hist')},
               omega_hist={str(k): v for k, v in sorted(stat.get('om', {}).items())},
               src_hist={str(k): v for k, v in sorted(stat.get('src_hist', {}).items())})
    for label, cond in (('all', lambda n: True), ('deep', lambda n: n >= N0)):
        cnt = div = veq = 0; maxA = 0; maxvA = -1; marg = None
        h = Counter(); hnp = Counter(); joint = Counter()
        for k, n in enumerate(Cn):
            if not cond(n):
                continue
            np_ = Cnp[k]; A = CA[k]
            cnt += 1
            va = v2(A)
            if A % (1 << np_) == 0:
                div += 1
            if va == np_:
                veq += 1
            maxA = max(maxA, A); maxvA = max(maxvA, va)
            marg = np_ - va if marg is None else min(marg, np_ - va)
            h[va] += 1; hnp[np_] += 1; joint[(np_, va)] += 1
        out[label] = dict(count=cnt, divA=div, v2A_eq_np=veq, A_max=maxA, A_bits=maxA.bit_length(),
                          v2A_hist={str(k): v for k, v in sorted(h.items())},
                          src_hist={str(k): v for k, v in sorted(hnp.items())},
                          joint={str(k): v for k, v in sorted(joint.items())},
                          min_np_minus_v2A=marg, omega_max=maxvA)
    return out

def main():
    out = {}
    for p in sys.argv[1:]:
        key = os.path.basename(p).replace('.pkl', '')
        out[key] = go(p)
        print(key, json.dumps({k: out[key][k] for k in ('all', 'deep') if k in out[key]})[:1600], flush=True)
    fp = os.path.join(HERE, 'verify_R1_src_summary.json')
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1)
    print('wrote', fp)

if __name__ == '__main__':
    main()
