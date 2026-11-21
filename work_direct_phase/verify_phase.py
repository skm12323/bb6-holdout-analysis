"""Canonical chain-5 direct returns. Run with python -B verify_phase.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "work_claude_cycle"))
from cyc import Cal


def low_labels(limit):
    cal = Cal()
    assert cal.k(5) == 1
    labels = {}
    for m in range(5, limit + 1):
        k = cal.k(m)
        if k is not None and (k + 2) % 16 == 8:
            labels[m] = (k + 2) // 8
    return labels


def longest_allowed(residues, modulus):
    # A walk can include one missing residue, but never two successive misses.
    inv = pow(3, -1, modulus)
    longest = 0
    for start in range(1, modulus, 2):
        current = start
        missing = False
        for length in range(1, modulus + 2):
            absent = current not in residues
            if absent and missing:
                longest = max(longest, length - 1)
                break
            missing = absent
            current = current * inv % modulus
        else:
            raise ValueError("a complete orbit avoids consecutive misses")
    return longest


if __name__ == "__main__":
    cutoff = 4096
    labels = low_labels(cutoff)
    assert min(labels) == 17
    modulus = 2 ** (min(labels) - 5)
    residues = {u % modulus for u in labels.values()}
    cap = 2 ** 4000
    n = cap - 1
    clock = n * (2 * ((6 * n * n + 5) - 1).bit_length() ** 2 + 1345)
    upper_u = (clock // 2 + 2) // 8
    assert 64 * upper_u < 2 ** (cutoff - 4)
    assert pow(3, 1024, modulus) == 1 and pow(3, 512, modulus) != 1
    longest = longest_allowed(residues, modulus)
    assert longest == 7
    # Independent orbit scan: deleting each adjacent-miss edge splits each
    # cycle into paths. The largest distance between deleted edges is 7.
    unseen = set(range(1, modulus, 2))
    gaps = []
    while unseen:
        orbit = []
        current = min(unseen)
        while current in unseen:
            unseen.remove(current)
            orbit.append(current)
            current = 3 * current % modulus
        cuts = [i for i, r in enumerate(orbit)
                if r not in residues and orbit[i - 1] not in residues]
        assert cuts
        gaps.extend(b - a for a, b in zip(cuts, cuts[1:] + [cuts[0] + len(orbit)]))
    assert max(gaps) == longest
    power, log_u = 1, 0
    while 3 * power <= upper_u:
        power *= 3
        log_u += 1
    print("low outputs:", len(labels), "distinct residues:", len(residues))
    print("maximum run without adjacent misses:", longest)
    print("floor(log3(U_bound)):", log_u, "maximum direct returns:", 7 * (log_u + 2) + 1)
