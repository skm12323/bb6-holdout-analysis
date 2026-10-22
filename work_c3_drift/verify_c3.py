"""Exact canonical checks for the epsilon=3 identity; not an EXT proof."""
from pathlib import Path
import sys, json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val

def main():
    cal = Calendar(512)
    hist = Counter()
    examples = []
    classes = 0
    for P in range(5, 257):
        source = cal.crossing(P - 1)
        if not source['odd'] or source['kind'] != 'a':
            continue
        fire = first_fire(cal, P)
        n = fire['pointer'] + 2
        row = cal.crossing(n)
        x0 = 6 * fire['k'] + 4
        z = 3 * source['time'] + 2
        q = val(z)
        assert q < P - 1
        assert row['odd'] and row['kind'] == 'c' and row['epsilon'] == 3
        assert row['tail_lambda'] == x0 // 2 - 1
        assert 3 * row['time'] + 4 + row['tail_lambda'] == 3 * x0 // 2 + z
        assert row['omega'] == q
        mod = 1 << (q + 1)
        for theta in range(-30, 31):
            delta = (theta + 3 * row['time'] + 3 - (1 << q)) % mod
            assert delta == theta % mod
            classes += 1
        hist[q] += 1
        if q > 5:
            examples.append(dict(P=P, q=q, n=str(n), time=str(row['time']),
                                 fire_k=str(fire['k']), pointer=str(fire['pointer']),
                                 tail_lambda=str(row['tail_lambda'])))
    # Exhaustive reachable drift states for a,b,c3 words, merging equal states.
    # c3 leaves theta unchanged; count only a/b letters for the parity invariant.
    states = {(1, 0)}
    counts = []
    for depth in range(14):
        for theta, h in states:
            assert 1-h <= theta <= h+1 and (theta-h-1) % 2 == 0
            assert abs(theta) <= depth+1
        counts.append(len(states))
        states = {(nt, nh) for theta, h in states
                  for nt, nh in ((3-theta, h+1), (theta-1, h+1), (theta, h))}
    result = dict(status='PASS', review_status='unreviewed', calendar_B=512,
                  root_parameters=[5,256], sources=sum(hist.values()),
                  omega_histogram=dict(sorted(hist.items())), class_checks=classes,
                  drift_state_counts=counts, omega_above_five=examples,
                  scope='Finite canonical source checks and finite drift checks; no global EXT claim.')
    Path(__file__).with_name('checks.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k != 'omega_above_five'}))
    print('first omega>5 witness:', examples[0])

if __name__ == '__main__':
    main()
