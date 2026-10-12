"""agentB_run11.py — big verification battery (background).
(1) symbolic engine v=1..2000 (independent replication of prior work's range)
(2) numeric w in {1,3,5,7} v=1..1000
(3) abstract per-j transition verification j=1..600
(4) universal-sequence bounds up to p < 400000
(5) ell closed form ell(v)=2*k_b+e on v=1..3000"""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import v2i, excursion, excursion_sym
from agentB_run7 import verify
from agentB_run8 import cascade

def main():
    # (1)
    for v in range(1, 2001):
        r = excursion_sym(v)
        if r['result'] != 'singleton':
            print('SYM ISSUE v=%d: %s %s' % (v, r['result'], r.get('msg'))); break
    else:
        print('(1) symbolic engine: v=1..2000 all safe, singleton, no halt [OK]')
    # (2)
    bad = 0
    for v in range(1, 1001):
        for w in (1, 3, 5, 7):
            r = excursion(w, v)
            if r['result'] != 'singleton':
                bad += 1; print('(2) ISSUE v,w', v, w, r['result'])
    print('(2) numeric w in {1,3,5,7}, v=1..1000: all singleton, bad =', bad)
    # (3)
    fails = []
    for j in range(1, 601):
        res, err = verify(j)
        if err:
            fails.append((j, err)); break
    print('(3) abstract transitions j=1..600:', 'ALL OK' if not fails else fails[:1])
    # (4)
    TAB = {}
    for j in range(1, 121):
        res, err = verify(j)
        assert not err
        TAB[j] = res[0]
    p, k = 4, 1
    ok_k = True; ok_j = True; maxratio = 0
    while p < 400000:
        j = 1 + v2i(3 * k + 2)
        if k > (p + 4) // 2: ok_k = False; break
        if j >= p - 1: ok_j = False; break
        maxratio = max(maxratio, k / p)
        p += TAB[j][1]; k += TAB[j][0]
    print('(4) universal seq to p<400000: k<=(p+4)/2:', ok_k, ' j<p-1:', ok_j,
          ' max k/p ratio: %.4f' % maxratio)
    # (5)
    L = {}
    for j in range(1, 121):
        ev, end = cascade(j)
        assert len(ev) + 1 == 2 * TAB[j][0], (j, len(ev), TAB[j])
    print('(5) L(j) = 2*dk(j) for j=1..120 [OK]')
    ellbad = []
    for v in range(3, 3001):
        r = excursion(1, v)
        assert r['result'] == 'singleton'
        ell = r['ell']
        steps = 2; p, k = 4, 1
        while True:
            j = 1 + v2i(3 * k + 2)
            dp = TAB[j][1]
            if p + dp > v - 1: break
            steps += 2 * TAB[j][0]
            p += dp; k += TAB[j][0]
        if not (0 <= ell - steps <= 10):
            ellbad.append((v, ell, steps))
    print('(5) ell(v) - (2 + 2*sum dk) in [0,10] for v=3..3000:',
          'OK' if not ellbad else ellbad[:5])

if __name__ == '__main__':
    main()
