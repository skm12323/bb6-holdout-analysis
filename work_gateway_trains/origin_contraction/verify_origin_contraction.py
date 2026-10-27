"""Exact checks for PROOF.md. New work, not independently reviewed.

Only this directory receives output. Canonical call data is imported read-only;
constructed ancestor states and arbitrary-data words are NOT actual S(J) states.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import json
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from work_global_ext.route_c.fdata import lam_walk, small_full
from work_global_calendar.calendar_oracle import Calendar


def val(x):
    x = F(x)
    if not x:
        raise ValueError('zero has no finite valuation')
    a, b = abs(x.numerator), x.denominator
    return (a & -a).bit_length() - (b & -b).bit_length()


def ceil_log2(n):
    return (n - 1).bit_length()


def check_data(N=200000):
    table = lam_walk(N)
    counts = Counter()
    for n in range(N):
        A, Y, t = table['lA'][n], table['lY'][n], table['tau'][n]
        assert A >= 0 and Y >= 0 and A + Y == 3*t + 1
        if table['odd'][n]:
            lam = A + 2*Y + 3
            assert 0 < lam <= 6*t + 5 < 9*t + 9
            counts[chr(table['typ'][n])] += 1
    full = small_full(1024)
    ratio_counts = Counter()
    for n, row in full.items():
        assert row['tau'] == table['tau'][n]
        assert row['A'][1] == table['lA'][n]
        if row['odd'] and row['typ'] in ('b', 'c'):
            ratio = F(row['x'][0], 1 << (n+1))
            if row['typ'] == 'b':
                assert ratio == F(3, 4)
            else:
                assert row['A'][0] + row['Y'][0] == 1 << n
                assert F(1, 2) < ratio < 1
            ratio_counts[row['typ']] += 1
    return dict(crossings=N, odd=dict(counts), full_pair_ratio_checks=dict(ratio_counts))


def update(q, b, t, kind, tau, ratio=None, lam=None):
    if kind == 'a':
        q, b = 2-q/2, 6*t+3*tau-b/2
    else:
        q, b = ratio*q, ratio*b+lam
    t += 1+tau
    assert 0 <= q <= 2 and 0 <= b <= 6*t
    return q, b, t


def check_cone():
    rng = random.Random(20261027)
    count = 0
    for _ in range(1500):
        q, b, t = F(0), F(0), 0
        D = F(rng.randrange(-1000, 1001), 3**rng.randrange(5))
        beta, theta = F(0), F(D)
        for _ in range(50):
            tau = 2*rng.randrange(1, 1000)
            if rng.randrange(2):
                beta, theta = 2*theta+3*tau-beta/2, theta+3+3*tau
                q, b, t = update(q, b, t, 'a', tau)
            else:
                # Includes endpoints of a larger envelope than canonical b/c data.
                ratio = F(rng.randrange(1, 17), 16)
                lam = rng.randrange(6*tau+6)
                beta, theta = ratio*beta+lam, theta+3+3*tau
                q, b, t = update(q, b, t, 'c', tau, ratio, lam)
            assert beta == q*D+b and theta == D+3*t
            tau_gate = 2*rng.randrange(1, 1000)
            S = 2-q/2
            Z = 2*theta+3*tau_gate-beta/2
            assert 1 <= S <= 2
            assert 3*t+3*tau_gate-2*abs(D) <= Z <= 6*t+3*tau_gate+2*abs(D)
            if abs(D) <= 5:
                assert Z > 0
            count += 1
    return dict(arbitrary_data_word_steps=count, seed=20261027,
                scope='Algebra checks; these words are not claimed canonical or reachable.')


def check_uniform_arithmetic():
    checks = 0
    for L in range(16, 4097):
        E = 4*L+128
        # Uniform dyadic estimates used in the all-y proof, not sampling y alone.
        poly = 2*(2*L+3)**2+1345
        assert poly < 1 << (L-1)
        assert (3*L+3)*(E+1) < (1 << (L-1))-1
        assert 2*(2*(L+1)+3)**2+1345 < 2*poly
        assert (3*(L+1)+3)*(4*(L+1)+129) < 2*(3*L+3)*(4*L+129)
        for y in sorted({1 << L, (1 << (L-1))+1}):
            if y < 65536:
                continue
            rmax = (y-5)//2
            rstar = max(1, (y-5)//(E+1))
            for r in sorted({1, rmax, rstar, rstar+1, 3*L}):
                if not 1 <= r <= rmax:
                    continue
                mu_lower = max(r+4, y-1-r*E)
                assert mu_lower > 3*L+3
                bound = F(6*r*(1+y*y)+3*y*y)+F(y,2)
                assert 0 < bound < 8*y**3 <= 1 << (3*L+3)
                hmax = (y+4*E-2)//(E+1)-3*L-3
                if hmax >= 0:
                    assert (E+1)*(hmax+3*L+3) < y+4*E-1
                    assert mu_lower > hmax+3*L+3
                checks += 1
    return dict(dyadic_exponents=[16,4096], integer_comparisons=checks)


def affine_prefix(cal, y, D, limit=100):
    """Keep the coefficient of 2^y U normalized; no huge 2^y is materialized."""
    D = F(D)
    alpha, beta, q, b = F(1), F(0), F(0), F(0)
    j, t, loss = y, 0, 0
    word, types = [y], ''
    for r in range(limit):
        row = cal.crossing(j-1)
        if not row['odd']:
            return dict(status='end', word=word, types=types)
        kind, tau = row['kind'], row['time']
        theta = D+3*t
        if kind == 'a':
            an = 2-alpha/2
            bn = 2*theta+3*tau-beta/2
            step_loss = 1
        else:
            ratio = (row['head_ratio']+2*row['tail_ratio'])/2
            lam = row['head_lambda']+2*row['tail_lambda']+3
            assert F(1,2) < ratio < 1
            assert 0 < lam <= 6*tau+5
            an, bn = ratio*alpha, ratio*beta+lam
            step_loss = 1+row['epsilon']
        assert bn != 0
        avaluation = y+val(an)
        assert avaluation == y-loss-step_loss
        m = val(bn)
        if m >= avaluation:
            return dict(status='coefficient_boundary', word=word+[m], types=types+kind)
        if kind == 'a' and m >= j:
            assert r >= 1  # no gate from the initial large/small-defect starts tested
            assert 3*t+3*tau-2*abs(D) <= bn <= 6*t+3*tau+2*abs(D)
            assert bn > 0
            assert avaluation >= r+4
            if y >= 65536 and abs(D) <= F(y,4):
                L = ceil_log2(y)
                h = ceil_log2(D.denominator)
                E = 4*L+128
                if (E+1)*(h+3*L+3) < y+4*E-1:
                    assert m < h+3*L+3 < avaluation
                    assert loss+1+m < y
            return dict(status='gate', word=word+[m], types=types+kind,
                        y=y, D=str(D), gate_input=j, gate_output=m, run_steps=r,
                        duration=t, Z=str(bn), mu=avaluation, loss=loss+1,
                        record=loss+1+m)
        if kind == 'a' and m == j-1:
            return dict(status='one_step_descent', word=word+[m], types=types+kind)
        assert m <= j-2
        if y >= 65536:
            assert step_loss <= 4*ceil_log2(y)+128
        if kind == 'a':
            q, b, t = update(q,b,t,kind,tau)
        else:
            q, b, t = update(q,b,t,kind,tau,ratio,lam)
        assert bn == q*D+b
        alpha, beta, j = an, bn, m
        loss += step_loss
        word.append(j)
        types += kind
    return dict(status='limit', word=word, types=types)


def check_exact_replays():
    cal = Calendar(256)
    counts = Counter()
    gates = []
    # Synthetic anchors, canonical call table; not actual S(J) trajectories.
    anchors = [(y,D) for y in range(64,2049) for D in range(-5,6)]
    # Add genuine source calls at huge canonical pointers, but synthetic ancestors.
    for exponent in (16,20,30,60,120):
        for z in range(64):
            k = (1 << exponent)+6+16*z
            fire = cal.preceding_fire_by_time(2*k)
            if fire['k'] == k:
                y = fire['pointer']+1
                anchors.append((y,-2))
                if z >= 3:
                    break
    fire = cal.preceding_fire_by_time(2*((1 << 20)+32761))
    assert fire['k'] == (1 << 20)+32761
    anchors.append((fire['pointer']+1,-32747))
    independent = 0
    for y,D in anchors:
        result = affine_prefix(cal,y,D)
        counts[result['status']] += 1
        assert result['status'] not in ('coefficient_boundary','limit')
        if result['status'] == 'gate':
            gates.append(result)
        if y <= 256:
            for u in (1,3,17):
                x,theta = (1<<y)*u,(1<<y)*u+D
                observed = [y]
                for j in result['word'][:-1]:
                    row = cal.crossing(j-1)
                    assert row['odd']
                    if row['kind'] == 'a':
                        x = 2*theta+3*row['time']-x//2
                    else:
                        cW = (row['head_ratio']+2*row['tail_ratio'])*(1<<(j-1))
                        assert cW.denominator == 1
                        lam = row['head_lambda']+2*row['tail_lambda']+3
                        x = int(cW)*(x>>j)+lam
                    theta += 3+3*row['time']
                    assert x > 0
                    observed.append(val(x))
                assert observed == result['word']
                independent += 1
    huge = [g for g in gates if g['y'] >= 65536]
    assert huge and max(g['y'] for g in huge).bit_length() >= 120
    return dict(anchors=len(anchors), statuses=dict(counts),
                full_integer_replays=independent, gates=len(gates),
                huge_gate_examples=huge,
                scope='Non-canonical ancestor states using certified canonical call data.')


def check_lift_transfer():
    cal = Calendar(256)
    tested, statuses = 0, Counter()
    examples = []
    cases = [(y,D) for y in (65536,65537,65554,100000,100001,131073)
             for D in (F(10,3),F(26,3),F(-16383),F(16383),
                       F(-3)+F(8,3**10),F(1,3**100))]
    fire5 = cal.preceding_fire_by_time(2*65542)
    assert fire5['k'] == 65542
    cases.extend((fire5['pointer']+1,D) for D in
                 (F(-2),F(-2)+F(64,3),F(-2)+F(64,3**10)))
    fire17 = cal.preceding_fire_by_time(2*((1 << 20)+32761))
    cases.append((fire17['pointer']+1,F(-32747)))
    for y,D in cases:
        reference = affine_prefix(cal,y,D)
        assert reference['status'] not in ('coefficient_boundary','limit')
        modulus = 1 << y
        residue = D.numerator*pow(D.denominator,-1,modulus) % modulus
        for lift in (0,1,3):
            x = 1 << y
            theta = x+residue+lift*modulus
            observed, loss = [y], 0
            for j, expected in zip(reference['word'],reference['word'][1:]):
                row = cal.crossing(j-1)
                if row['kind'] == 'a':
                    x = 2*theta+3*row['time']-x//2
                else:
                    ratio = (row['head_ratio']+2*row['tail_ratio'])/2
                    xx = ratio*x+row['head_lambda']+2*row['tail_lambda']+3
                    assert xx.denominator == 1
                    x = int(xx)
                theta += 3+3*row['time']
                loss += 1+row['epsilon']
                assert val(x) == expected and expected+loss < y
                observed.append(val(x))
            assert observed == reference['word']
            statuses[reference['status']] += 1
            tested += 1
        if reference['status'] == 'gate':
            examples.append(reference)
    assert any(e['gate_input'] == 17 for e in examples)
    assert any(F(e['D']).denominator > 1 for e in examples)
    # Known small-gateway precision obstruction: the theorem deliberately excludes y=5.
    boundary_checks = 0
    for m in range(6,257,2):
        u = ((1 << (m-4))-1)//3
        x,theta = 32*u,32*u+5
        assert val(x) == 5
        assert 2*theta+6-x//2 == 1 << m
        assert val(16) == 4  # small part Z and coefficient have equal valuation
        boundary_checks += 1
    return dict(integer_lift_replays=tested, statuses=dict(statuses), gate_examples=examples,
                excluded_small_gateway_boundary_checks=boundary_checks,
                scope='Rational reference vs constructed integer phase lifts; not real orbit reachability.')


def main():
    out = dict(status='PASS', review_status='unreviewed',
               canonical_mass=check_data(), cone=check_cone(),
               uniform_arithmetic=check_uniform_arithmetic(),
               replay=check_exact_replays(), lift_transfer=check_lift_transfer(),
               scope='Checks for local origin-contraction theorem; no global EXT proof; K_clock unchanged.')
    (HERE/'checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='replay'},indent=2))
    print(json.dumps({k:v for k,v in out['replay'].items() if k!='huge_gate_examples'},indent=2))


if __name__ == '__main__':
    main()
