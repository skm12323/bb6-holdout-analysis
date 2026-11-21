"""Check the calendar input and integer boundary constants for ALL_CHAINS.md."""
from verify_phase import Cal, longest_allowed
from cyc import step


def clock_bound(m):
    n = m - 1
    ceil_log = (6 * n * n + 4).bit_length()
    return n * (2 * ceil_log**2 + 1345)


def replay_return(cal, j, m, u):
    # Build a finite integer gate state. Use the scalar pair map twice,
    # independently of the NF update used by the induction.
    z = 2 ** (m - j + 1)
    o = 2 * z + (u + 2) % 4
    theta = 2 ** (j - 2) * o - 3 * cal.k(j)
    x = 2**j * (o - z)
    first = step(cal, j, theta, x)
    assert first["ev"] == "gate" and first["jn"] == m
    second = step(cal, m, first["Th"], first["x"])
    assert second["jn"] == j
    end_theta, end_x = second["Th"], second["x"]
    end_o, remainder = divmod(end_theta + 3 * cal.k(j), 2 ** (j - 2))
    assert not remainder and end_o % 2
    end_z = end_o - end_x // 2**j
    assert end_o - o == 6 * u
    assert 4 * (3 * end_z - 2 * end_o) == 3 * z - 2 * o + 6 * u


def base_certificate():
    cal = Cal()
    small_rows = [(m, cal.k(m)) for m in range(5, 32 + 4091)]
    lengths = {}
    for j, kj in small_rows:
        if j >= 32 or kj is None:
            continue
        assert cal.k(j + 1) is None
        labels = {}
        for m, km in small_rows:
            if j <= m <= j + 4091 and km is not None:
                u, remainder = divmod(kj + 1 + km, 2 ** (j - 2))
                if not remainder and u % 2:
                    labels[m] = u
        assert all(m >= j + 12 for m in labels)
        for m, u in labels.items():
            replay_return(cal, j, m, u)
        length = longest_allowed({u % 4096 for u in labels.values()}, 4096)
        lengths[j] = length
        print(j, len(labels), min(labels, default=None), length)
    assert lengths == {5: 7, 8: 6, 12: 1, 14: 1, 17: 1, 22: 1, 24: 1, 27: 1}
    assert clock_bound(8192) + 1 < 2**30
    cap = 2**4000
    bound = (clock_bound(cap) + 1) // 8
    assert 64 * bound < 2**4092 and bound < 3**2540
    assert 7 * (2 + 2539) + 1 < 18000 < 17**4


def induction_constants():
    for m in (2**4000 + 1, 2**4001, 2**4001 + 1, 2**12000 + 321):
        e = (m - 1).bit_length()
        h_bound = 21 * e
        period = 2 ** (16 * e)
        assert clock_bound(m) + 1 <= m**4
        assert h_bound**4 <= m**2
        assert 4 ** (2 * e) >= 3 * m**3 + 1
        assert period - 6 * m**3 > 12 * m**3 * (2 * m**2 + 1)
        assert 4 * m**2 + m**3 + 1 <= m**4


if __name__ == "__main__":
    print("j, eligible low outputs, minimum output, longest piece")
    base_certificate()
    induction_constants()
    print("PASS")
