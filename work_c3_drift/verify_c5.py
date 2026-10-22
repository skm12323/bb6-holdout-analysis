"""Canonical AA/BA class checks and BA bare-tie algebra; no global claim."""
from pathlib import Path
from collections import Counter
import sys, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val

def main():
    cal = Calendar(512)
    counts = Counter()
    checks = 0
    for P in range(5, 257):
        r = cal.crossing(P-1)
        if not r['odd'] or r['kind'] not in ('a', 'b'):
            continue
        if r['kind'] == 'a':
            p = val(3*r['time']+2)
            kind = 'AA'
        else:
            p = val(3*r['time']+4)
            kind = 'BA'
        r2 = cal.crossing(p-1)
        if not r2['odd'] or r2['kind'] != 'a':
            continue
        fire = first_fire(cal, P)
        x0 = 6*fire['k']+4
        n = fire['pointer'] + (3 if kind == 'AA' else 2)
        row = cal.crossing(n)
        assert row['kind'] == 'c' and row['odd'] and row['epsilon'] == 5
        if kind == 'AA':
            assert row['tail_lambda'] == x0//4 + 3*r['time']//2 + 1
            q = val(3*r2['time']+4)
            shift = -1
        else:
            y = 3*r['time']+4
            assert row['tail_lambda'] == 5*x0//8+y//2-2
            q = val(3*r2['time'])
            shift = 1
        assert row['omega'] == q and q < p-1
        for theta in range(-30,31):
            assert (theta-1-row['tail_lambda']-theta-shift) % (1 << (q+1)) == 0
            checks += 1
        counts[kind] += 1
    small = [(p, cal.crossing(p-1)['time']//2) for p in range(5,15)
             if cal.crossing(p-1)['odd'] and cal.crossing(p-1)['kind']=='a']
    assert all(val(6*k) != 5 for _, k in small)
    # Exact reference gateway with k=16*v (v odd), plus errors of the
    # proved precision. These are algebra tests, not canonical witnesses.
    gateway = 0
    for v in range(1,2000,2):
        k = 16*v
        x, th = 6*k, 6*k+5
        xn, tn = 2*th+6-x//2, th+9
        m = val(xn)
        assert xn == 9*k+16 and tn == 6*k+14 and m >= 5
        assert (3*(tn-xn) - (10-(1<<m))) % (1 << (m+1)) == 0
        for p in (max(15,m+3), max(25,m+5)):
            for ex, et in ((1,1),(3,-1),(-1,3)):
                xx, tt = x+(1<<(p-1))*ex, th+(1<<(p-1))*et
                yy, uu = 2*tt+6-xx//2, tt+9
                assert val(yy) == m
                assert (uu-yy-(tn-xn)) % (1<<(m+1)) == 0
                gateway += 1
    # Integer form of 9*k+16 <= 4.5*(p-1)^2+16 < 2^(p-2).
    assert all(9*(p-1)**2+32 < 1<<(p-1) for p in range(15,4097))
    states = {1}
    drift = []
    for t in range(4):
        assert min(states) >= 1-t and max(states) <= t+1
        drift.append(sorted(states))
        states = {y for x in states for y in (3-x,x-1,x,x+1)}
    out = dict(status='PASS', review_status='unreviewed', canonical_sources=dict(counts),
               canonical_class_checks=checks, small_odd_a=small,
               algebra_gateway_checks=gateway, drift_through_T3=drift,
               scope='Canonical sources P<=256; synthetic gateway precision tests separately labeled.')
    Path(__file__).with_name('c5_checks.json').write_text(json.dumps(out,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(out))

if __name__ == '__main__': main()
