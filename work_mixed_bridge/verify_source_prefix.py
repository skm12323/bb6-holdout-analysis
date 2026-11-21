"""Verify the small source prefix and the strict-EXT induction start.

The raw universal pair walk supplies rows in chronological order. Compare
each one with the calendar used for the mixed-word base, and compare the
full symbolic exit with the scalar exit using only the reached rows.
"""
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from verify_bridge import Cal, step

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "work_m"))
from verify_m import Xdata, sym_exit


class Prefix:
    def __init__(self):
        self.raw = {}
        self.rows = {}
        self.calendar = Cal()
        self.lengths = Counter()
        self.maximum_loss = 0

    def row(self, n):
        return self.rows[n]

    def record(self, n, data):
        assert n == len(self.rows)
        self.raw[n] = data
        kind, head, tail, eps = data
        row = self.calendar.row(n)
        self.rows[n] = row
        tau, remainder = divmod(head[1] + (tail[1] if tail else 0) - 1, 3)
        odd = bool(sum(head) % 2)
        assert remainder == 0 and 0 <= tau <= n
        assert (kind, tau, eps, odd) == (row["kind"], row["tau"], row["eps"], row["odd"])
        if kind != "a" and odd:
            ratio = Fraction(head[0] + 2*tail[0], 1 << (n+1))
            offset = head[1] + 2*tail[1] + 3
            omega = (offset & -offset).bit_length() - 1
            assert (ratio, offset, omega) == (row["R"], row["lam"], row["omega"])

        root = n + 1
        expected, kinds, length, expected_loss = sym_exit(root, self.raw)
        q, theta, x, loss = root, 1, 0, 0
        chains, source_types = [q], []
        while True:
            source = self.row(q-1)
            source_types.append(source["kind"])
            if not source["odd"]:
                break
            action = step(self, q, theta, x)
            assert action is not None and action["x"] > 0 and action["x"].denominator == 1
            q, theta, x = action["jn"], action["Th"], action["x"]
            loss += action["loss"]
            assert 0 < q < root - loss
            chains.append(q)
        assert (tuple(chains), "".join(source_types), len(chains)-1, loss) == (
            expected, kinds, length, expected_loss)
        self.lengths[length] += 1
        self.maximum_loss = max(self.maximum_loss, loss)


def arithmetic_endpoints():
    # All persistence inequalities used here compare a degree <= 2
    # positive-coefficient polynomial with a power of two. For k >= 3
    # each of 1, k, k^2 increases by a factor strictly below two.
    for n in (1022, 1023):
        g = (6*n*n+4).bit_length()
        assert g == 23 and 4*g*g+3435 < 3*(2*n+1)
    assert 4*(2*10+5)**2+3435 < 3*2**11
    assert 1+(2*10+4)**2 <= 1024
    assert 1+(2*11+4)**2 <= 2**10
    assert 10*10+37 < 2**8 and 32*510**2 < 2**508
    assert 2*509+4 <= 1023 < 2*510+4
    assert 3*32**2+4 < 2**32


if __name__ == "__main__":
    arithmetic_endpoints()
    prefix = Prefix()
    Xdata(1023, cb=prefix.record)
    assert len(prefix.raw) == 1023
    assert prefix.lengths == {0: 389, 1: 586, 2: 48}
    assert prefix.maximum_loss == 4
    assert max(prefix.row(n)["tau"] for n in range(63)) == 51
    assert prefix.row(1022)["tau"] == 910
    print("1023 row interfaces and symbolic exits agree; lengths:", dict(sorted(prefix.lengths.items())))
    print("maximum exit loss: 4; maximum small clock: 51; tau(1022): 910")
