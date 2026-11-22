"""Independent forward phase/value-cylinder check of the mixed-word base."""
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "work_claude_cycle"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cyc import Cal, step
from audit_bridge import gap_polynomials


def valuation(v):
    return (v & -v).bit_length() - 1


@dataclass(frozen=True)
class Block:
    a: int
    loss: int
    c: int
    time: int  # increment of Theta, not elapsed pair steps


def blocks_for(cap):
    cal = Cal()
    blocks = {}
    for source in range(5, cap + 1):
        q = source
        ratio, offset, time, loss = Fraction(1), Fraction(0), 0, 0
        while True:
            row = cal.row(q - 1)
            if not row["odd"]:
                break
            increment = 3 * (1 + row["tau"])
            if row["kind"] == "a":
                a = -ratio / 2
                c = 2 * time + 3 * row["tau"] - offset / 2
                denom = 2 ** (loss + 1)
                assert a.denominator == denom and (c * denom).denominator == 1
                assert 0 <= c <= 2 * (time + increment)
                block = Block(a.numerator, loss + 1, int(c * denom), time + increment)
                blocks[source] = block
                # Replay a low and a high positive lift on the scalar map.
                for odd, theta in ((1, 1), (71, 10**12 + 1)):
                    x = odd << source
                    j, t, y = source, theta, x
                    while True:
                        action = step(cal, j, t, y)
                        j, t, y = action["jn"], action["Th"], action["x"]
                        if action["kind"] == "a":
                            break
                    assert denom * y == block.a * x + 2 * denom * theta + block.c
                    assert t - theta == block.time
                break
            ratio *= row["R"]
            offset = row["R"] * offset + row["lam"]
            time += increment
            loss += 1 + row["eps"]
            q = row["omega"]
            if q < 5:
                break
    return blocks


def base_check():
    blocks = blocks_for(1023)
    counts = Counter()
    alphabet = tuple(blocks)

    # State over the 2-adic integers:
    # Theta=t+2^b v, x=r+p v+2^a u with free u,v.
    # Odd factors on independent columns can be discarded in Z_2.
    def visit(t, b, r, p, a, depth):
        common = min(a, valuation(p)) if p else a
        if r % (1 << common):
            q = valuation(r)
            choices = (q,) if q in blocks else ()
        else:
            choices = (q for q in alphabet if q >= common)
        for q in choices:
            counts[depth + 1] += 1
            assert depth + 1 < 7
            n = q + 1
            overlap = min(a, n)
            vbits = max(0, overlap - common)
            vmod = 1 << vbits
            v0 = (((1 << q) - r) // (1 << common) *
                  pow(p >> common, -1, vmod)) % vmod if vbits else 0
            new_t = t + (v0 << b)
            new_b = b + vbits
            if n >= a:
                new_r, new_p, new_a = 1 << q, 0, n
            else:
                new_r, new_p, new_a = r + p*v0, p << vbits, a
            block = blocks[q]
            den = 1 << block.loss
            rn = block.a * new_r + den * 2 * new_t + block.c
            pn = block.a * new_p + (den << (1 + new_b))
            assert rn % den == pn % den == 0 and new_a >= block.loss
            bits = new_a - block.loss
            mask = (1 << bits) - 1
            visit(new_t + block.time, new_b, (rn // den) & mask,
                  (pn // den) & mask, bits, depth + 1)

    visit(0, 0, 0, 0, 0, 0)
    assert counts == {1: 325, 2: 105625, 3: 25438, 4: 17378, 5: 6271, 6: 504}
    losses = Counter(block.loss for block in blocks.values())
    assert losses == {1: 309, 3: 16}
    print("mixed-word counts:", sorted(counts.items()))
    print("losses over all productive inputs (no output cap):", sorted(losses.items()), "maximum:", max(losses))


def scale_checks():
    # Check the first enlargement and the tight end of the infinite
    # persistence estimates. The decreasing-ratio argument is in the proof.
    h, m = 1023, 2**20
    loss, time = 201, 42 * m**3
    assert 2 * loss + (12 * time).bit_length() <= h + 1
    # floor(log2(2T)) = 66 since 2T = 21*2^62, so (5) gives N <= 7*70.
    assert (2 * time).bit_length() - 1 == 66
    assert 7 * (4 + 66) == 490 <= 1024
    # All-scale obligations for every e >= 20: each gap polynomial is the
    # corresponding difference evaluated at the grid invariant r = 48e+64
    # (nonnegative coefficients with positive constant term), and each
    # difference is increasing in r beyond the invariant; both properties
    # are asserted inside gap_polynomials, with no sampling.
    assert len(gap_polynomials()) == 4
    for e in (20, 21, 40, 80, 160, 320, 640):
        # Numeric spot checks on the same grid, exact integers.
        # For odd e use the upper integer square root.
        h = 1 << e
        root = isqrt(h)
        root += root * root < h
        loss = 18 * e + 3 + (9 * e + 3) * root
        time = 6 * (root + 1) * h**6
        assert 4 * loss <= h and time <= h**7
        assert 2 * loss + (12 * time).bit_length() <= h + 1
        assert (root + 1) * (7 * e + 5) <= h
    print("separation and scale constants: PASS")


def three_high_replay():
    # An actual affine lift of the three-high subword appearing in the
    # previous broad cylinder search. The middle bridge has a different
    # clock coefficient from the first. This checks the sign in Z.
    cal = Cal()
    m, n = 661128, 857036
    k, low_k = cal.k(m), cal.k(17)
    p0 = 6 + 9 * k + 6 * low_k
    t0 = 6 + 6 * (k + low_k)
    p1 = 3 * k
    assert p0 == t0 + p1 and p0 <= 2 * t0
    middle = (1 << m) + (1 << (n + 1))
    initial = 3 * middle - (1 << (n + 1))
    theta = middle - initial // 4 - p0
    x = initial
    for q, next_q in ((m, 17), (17, m), (m, n)):
        action = step(cal, q, theta, x)
        assert action["kind"] == "a" and action["jn"] == next_q
        theta, x = action["Th"], action["x"]
    assert x == 1 << n
    print("three-high scalar replay: PASS", (p0, t0, p1))


if __name__ == "__main__":
    base_check()
    scale_checks()
    three_high_replay()
