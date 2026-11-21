"""Overapproximate all finite, canonical a-only runs with input chains <= 256."""
from functools import lru_cache
from verify_phase import Cal
from cyc import step


def certificate(bits=10):
    cal = Cal()
    labels = {q: k for q in range(5, 257) if (k := cal.k(q)) is not None}
    modulus = 1 << bits
    bound = 3 * (max(labels.values()) + 2) + 1
    deep = tuple(k for q, k in labels.items() if q >= 2 + bits)
    visiting = set()

    @lru_cache(None)
    def length(d, phase):
        state = (d, phase)
        if state in visiting:
            raise ValueError(f"cycle at {state}")
        visiting.add(state)
        residue = (phase + d) % modulus
        if residue:
            q = 1 + (residue & -residue).bit_length()
            choices = (labels[q],) if q in labels else ()
        else:
            choices = deep
        best = 0
        for k in choices:
            best = max(best, 1)
            numerator = -d - 3 * (k + 2)
            if numerator % 2:
                continue
            child = numerator // 2
            assert abs(child) <= bound
            next_phase = (phase + 3 + 6 * k) % modulus
            if (child + next_phase) % 8 == 0:
                best = max(best, 1 + length(child, next_phase))
        visiting.remove(state)
        return best

    longest = max(length(d, phase) for d in range(-bound, bound + 1)
                  for phase in range(-d % 8, modulus, 8))
    assert bound == 343 and longest == 7
    print("bits, bound, states, longest:", bits, bound, length.cache_info().currsize, longest)


def exact_words():
    # Work with cylinders of initial Theta, using exact q instead of merging
    # deep rows. Theta_0 == -d_0 mod 3 makes the initial x an integer.
    cal = Cal()
    rows = [(q, cal.k(q)) for q in range(5, 257) if cal.k(q) is not None]
    best = ()
    witness = None

    def extend(d0, d, delta, residue, modulus, word):
        nonlocal best, witness
        for q, k in rows:
            mod = 1 << (q - 1)
            want = ((mod // 2) - d - delta) % mod
            if (residue - want) % min(modulus, mod):
                continue
            r, period = (want, mod) if mod > modulus else (residue, modulus)
            path = word + (q,)
            if len(path) > len(best):
                best = path
                theta = r + period * ((-d0 - r) * pow(period, -1, 3) % 3)
                witness = (theta, 4 * (theta + d0) // 3)
            assert len(path) < 8
            num = -d - 3 * (k + 2)
            if num % 2 == 0:
                extend(d0, num // 2, delta + 3 + 6 * k, r, period, path)

    for d in range(-343, 344):
        extend(d, d, 0, 0, 1, ())
    assert len(best) == 5
    theta, x = witness
    for q in best:
        assert x and (abs(x) & -abs(x)).bit_length() - 1 == q
        action = step(cal, q, theta, x)
        assert action["kind"] == "a"
        assert action["x"].denominator == 1
        theta, x = action["Th"], int(action["x"])
    print("exact longest and scalar witness:", len(best), best)


if __name__ == "__main__":
    certificate()
    certificate(12)
    exact_words()
