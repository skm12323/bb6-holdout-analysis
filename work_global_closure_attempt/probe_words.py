"""Targeted exact pure-A word search; not a global/canonical certificate."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
for directory in ('work_global_ext/route_c', 'work_g2_core_words',
                  'work_global_clock_words', 'work_global_calendar'):
    sys.path.insert(0, str(ROOT / directory))
from fdata import lam_walk, small_full
from word_search import constrain, val
from clock_words import clock_projection, fire_projection
from calendar_oracle import Calendar


def main():
    start = time.monotonic()
    data = lam_walk(1000000)
    small = small_full(129)
    ks = {}
    for q in range(5, 129):
        rec = small[q-1]
        if q in (5, 8, 14, 17, 27, 65) and rec['typ'] == 'a' and rec['odd']:
            assert rec['tau'] == data['tau'][q-1]
            ks[q] = rec['tau']//2
    special = []
    for q in range(129, data['N']):
        n = q-1
        if data['typ'][n] != 97 or not data['odd'][n]:
            continue
        k = data['tau'][n]//2
        if q in (48979, 122436, 367354):
            ks[q] = k
            special.append(q)
    assert ks[122436] == 54614 and ks[367354] == 163862
    calendar = Calendar(64)
    for q, k in ks.items():
        independent = calendar.crossing(q-1)
        assert independent['kind'] == 'a' and independent['odd']
        assert independent['time'] == 2*k and independent['epsilon'] == 0
        assert independent['head_lambda'] == 6*k+1
        assert independent['head_ratio'] == 1
    blocks = {q: dict(alpha=F(1), B=F(0), d=0, G=0, k=k, T=1+2*k)
              for q, k in ks.items()}
    alphabet = sorted(ks)
    print('alphabet', len(alphabet), 'special', special, flush=True)
    counts = Counter()
    escapes = Counter()
    maxword = ()
    longest = []
    depth_cap = 12
    last = time.monotonic()
    for q in alphabet:
        for r in alphabet:
            stack = [((q, r), (F(0), F(1 << q), F(0)),
                      (F(0), F(0), F(1 << r)), (1, 1), [(2, 0), (0, 2)])]
            while stack:
                word, x0, x1, base, cols = stack.pop()
                length = len(word)
                counts[length] += 1
                if length > len(maxword):
                    maxword = word
                    longest = [word]
                elif length == len(maxword) and len(longest) < 20:
                    longest.append(word)
                if length == depth_cap:
                    continue
                const = 6+6*ks[word[-2]]+6*ks[word[-1]]
                x = tuple((x0[z]+x1[z])/2 + (const if z == 0 else 0)
                          for z in range(3))
                den = max(v.denominator for v in x)
                shift = val(den)
                c, a, b = (int(v*den) for v in x)
                origin = c+a*base[0]+b*base[1]
                precision = min(val(a*v[0]+b*v[1]) for v in cols)
                if val(origin) < precision:
                    output = val(origin)-shift
                    possible = [output] if output in ks else []
                    if output >= 5 and output not in ks:
                        escapes[length] += 1
                else:
                    possible = [p for p in alphabet if p >= precision-shift]
                    escapes[length] += 1
                for p in possible:
                    answer = constrain(base, cols, a, b,
                                       den*(1 << p)-c, den*(1 << (p+1)))
                    assert answer is not None
                    nb, nc = answer
                    stack.append((word+(p,), x1, x, nb, nc))
                now = time.monotonic()
                if now-last > 15:
                    print('progress', dict(counts), 'max', maxword, flush=True)
                    last = now
    witnesses = []
    for word in longest:
        projection = clock_projection(word, blocks)
        assert projection is not None
        fire = fire_projection(projection)
        modulus = 1 << projection['anchor_bits']
        theta_period = 1 << projection['theta_bits']
        theta = projection['theta_residue'] + 8*modulus
        while theta % 3 != 2:
            theta += theta_period
        residue = (projection['anchor_slope']*theta + projection['anchor_offset']) % modulus
        x = residue + ((theta+1-residue+modulus-1)//modulus)*modulus
        assert theta-1 < x < 2*theta-5
        initial_x, initial_theta = x, theta
        sigma = max(word)+len(word)+4
        gap = 2*max(word)+1
        pointer = sigma+gap
        head = (((1 << gap)-1) << sigma, 2*theta-x-5)
        tail = (1 << sigma, x-theta+1)
        margins = []
        for q in word:
            assert val(x) == q
            assert x == head[1]+2*tail[1]+3
            assert head[0]+tail[0] == 1 << pointer
            assert head[1]+tail[1] == theta-4
            assert min(head+tail) > 0
            cx = head[0]+2*tail[0]
            margins.append(val(cx)-q)
            assert margins[-1] > 0
            k = ks[q]
            old_head = head
            head = ((1 << (q-1))*(cx >> q),
                    (1 << (q-1))*(x >> q)+6*k+1)
            tail = ((1 << pointer)+old_head[0]//2, (old_head[1]+1)//2)
            pointer += 1
            x, theta = 2*theta-x//2+6*k, theta+6*k+3
            assert theta-1 < x < 2*theta-5
        def digest(number):
            return hashlib.sha256(number.to_bytes((number.bit_length()+7)//8, 'big')).hexdigest()
        witnesses.append(dict(word=word,
                              clock_bits=projection['theta_bits'],
                              root_bits=projection['anchor_bits'],
                              fire_compatible=fire is not None,
                              positive_pair_macro_checks=len(word),
                              minimum_margin=min(margins),
                              following_parameter=val(x),
                              initial_clock_bits=((initial_theta-5)//3).bit_length(),
                              initial_x_sha256=digest(initial_x),
                              initial_theta_sha256=digest(initial_theta)))
    result = dict(result='PASS', alphabet=alphabet,
                  high_sources=[dict(q=q, k=ks[q]) for q in special],
                  independent_calendar_source_checks=len(ks),
                  depth_cap=depth_cap, feasible_counts=dict(sorted(counts.items())),
                  omitted_parameter_branches=dict(sorted(escapes.items())),
                  depth_cap_reached=bool(counts[depth_cap]),
                  max_length=len(maxword), longest_samples=witnesses,
                  seconds=round(time.monotonic()-start, 2),
                  scope='Exact congruence search in a selected pure-A alphabet only; omitted parameters and canonical ancestry remain open.')
    Path(__file__).with_name('word_probe.json').write_text(
        json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
