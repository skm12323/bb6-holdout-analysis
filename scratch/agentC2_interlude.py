"""agentC2 -- Second pass, part 1: the general-k interlude.

A mid-block R-fire at dive position (t, i) (head = sigma + 3t+1, sigma = beta*2^i,
k = v2(3t+4) = v2(x), x = 3*sigma + (3t+4)) leaves the exact post-fire list

    (q+1; q, 2q, ..., 2^(k-2) q; s; 4sigma, 8sigma, 16sigma, ...)

with q = x/2^k (odd) and s = (5*sigma + 3t + 2)/2 (the seam).  This script
constructs that state EXACTLY for arbitrary k (choosing 3t+4 = r*2^k with odd r,
t even, and sigma = 3*2^i with i = 2k+pad so that every congruence used by the
dynamics is faithful to genuine dive positions), runs the exact top map until
the next fire whose first entry is a PARENT run (4*sigma*2^j), and records

  * (dt, di)(k) = (t' - t, i' - i) of that next parent fire  [the dive map]
  * the full fire trace of the interlude (child fires, seam fires).

Checks: r-independence, pad(room)-independence, agreement with the report's
k<=10 table, agreement with the actual excursion E(1, 3000) dive sequence.
"""
import sys
sys.path.insert(0, r"D:\math_cc\scratch")
from agentC_lib import v2 as _v2


def v2(x):
    return _v2(x)


def pick_r(k, idx):
    """odd r with r*2^k =: 4 (mod 6) so that t=(r*2^k-4)/3 is an even integer."""
    base = 1 if k % 2 == 0 else 5
    out = []
    c = base
    while len(out) <= idx:
        if c % 2 == 1:
            out.append(c)
        c += 6
    return out[idx]


def interlude(k, r=None, pad=120, maxsteps=100000, trace=False):
    """Exact simulation of the interlude after a mid-block fire with parameter k.
    Returns dict(dt, di, tprime, fires, steps, halt). fires: list of
    (D, i_entry, kfire, isparent, e1)."""
    if r is None:
        r = pick_r(k, 0)
    assert r % 2 == 1
    t = (r << k) - 4
    assert t % 3 == 0, (k, r)
    t //= 3
    assert 3 * t + 4 == (r << k)
    assert t % 2 == 0, "t must be even (fires have t even)"
    i = 2 * k + pad
    sigma = 3 << i
    a = sigma + 3 * t + 1
    x = 3 * sigma + (3 * t + 4)
    assert a % 2 == 1 and v2(x) == k, (v2(x), k)
    q = x >> k
    s = (5 * sigma + 3 * t + 2) >> 1
    assert s * 2 == 5 * sigma + 3 * t + 2
    NTAIL = 8 * k + 64
    parent = set(sigma << j for j in range(2, 2 + NTAIL))
    L = [q + 1] + [q << p for p in range(k - 1)] + [s] + \
        [sigma << j for j in range(2, 2 + NTAIL)]
    fires = []
    steps = 0
    while steps < maxsteps:
        A = L[0]
        if A % 2 == 0:
            L = [A + L[1] + L[2] + 3] + L[3:]
            steps += 1
            continue
        e1 = L[1]
        xe = A + 2 * e1 + 3
        kf = v2(xe)
        isp = e1 in parent
        D = A - e1
        fires.append((D, v2(e1), kf, isp, e1))
        if isp:
            # parent-block fire: decode t', i'
            assert D == 3 * ((D - 1) // 3) + 1 and (D - 1) % 3 == 0
            tp = (D - 1) // 3
            ip = v2(e1)
            out = dict(dt=tp - t, di=ip - i, tprime=tp, iprime=ip, kfire=kf,
                       fires=fires, steps=steps, halt=False, t=t, i=i, q=q, s=s)
            if trace:
                out['trace'] = fires
            return out
        # odd step (fire) -- exact top-map odd branch
        b, c = L[1], L[2]
        m = b + (A - 3) // 2
        seam = c + (A + 1) // 2
        chain = []
        while m >= 3 and m % 2 == 1:
            chain.append((m + 3) // 2)
            m = (m - 3) // 2
        if m == 1:
            return dict(dt=None, di=None, fires=fires, steps=steps, halt=True)
        chain.reverse()
        L = [m + 4] + chain + [seam] + L[3:]
        steps += 1
    raise RuntimeError("interlude did not close for k=%d r=%d" % (k, r))


# ---------------------------------------------------------------- table
if __name__ == "__main__":
    REPORT_TABLE = {1: (2, 3), 2: (2, 2), 3: (4, 5), 4: (4, 4), 5: (6, 4),
                    6: (6, 5), 7: (6, 4), 8: (8, 6), 9: (8, 2), 10: (10, 5)}

    print("=== dive-map table (dt, di, loss=dt-di) by k, exact simulation ===")
    table = {}
    for k in range(1, 65):
        out = interlude(k)
        table[k] = (out['dt'], out['di'])
        nf = len(out['fires'])
        print("k=%-3d dt=%-4d di=%-4d loss=%-4d  inter-fires=%d" %
              (k, out['dt'], out['di'], out['dt'] - out['di'], nf))

    print()
    print("=== agreement with prior report table (k<=10) ===")
    bad = [(k, REPORT_TABLE[k], table[k]) for k in REPORT_TABLE
           if REPORT_TABLE[k] != table[k]]
    print("mismatches:", bad if bad else "NONE")

    # ------------------------------------------------- r-independence
    print()
    print("=== r-independence (k=1..48, r = 8 odd choices) ===")
    bad = []
    for k in range(1, 49):
        ref = table[k]
        for idx in range(8):
            r = pick_r(k, idx)
            out = interlude(k, r=r)
            if (out['dt'], out['di']) != ref:
                bad.append((k, r, ref, (out['dt'], out['di'])))
    print("r-dependence found:", bad if bad else "NONE (all r give same (dt,di))")

    # ------------------------------------------------- room/pad-independence
    print()
    print("=== room-independence (k=1..48, pad in {40, 200}) ===")
    bad = []
    for k in range(1, 49):
        ref = table[k]
        for pad in (40, 200):
            out = interlude(k, pad=pad)
            if (out['dt'], out['di']) != ref:
                bad.append((k, pad, ref, (out['dt'], out['di'])))
    print("pad-dependence found:", bad if bad else "NONE")

    # ------------------------------------------------- excursion cross-check
    print()
    print("=== cross-check vs genuine excursion E(1, 3000) ===")

    def step_ann(L, ann):
        A = L[0]
        b = L[1] if len(L) > 1 else 0
        c = L[2] if len(L) > 2 else 0
        if A % 2 == 0:
            return [A + b + c + 3] + L[3:], ann[2:]
        x = A + 2 * b + 3
        k = v2(x)
        q = x >> k
        m = b + (A - 3) // 2
        seam_val = c + (A + 1) // 2
        chain = []
        while m >= 3 and m % 2 == 1:
            chain.append((m + 3) // 2)
            m = (m - 3) // 2
        chain.reverse()
        if m == 1:
            return None, None
        cann = [('R', q, i) for i in range(k - 1)]
        sann = ('T', chain[-1]) if chain and seam_val == 2 * chain[-1] - 1 else ('S',)
        return [m + 4] + chain + [seam_val] + L[3:], cann + [sann] + ann[2:]

    def E(w, v):
        vals = [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]
        ann = [('R', 3 * w, i) for i in range(v - 1)] + [('T', 3 * w << (v - 2))]
        return vals, ann

    v = 3000
    L, ann = E(1, v)
    dive = []
    for s in range(10 ** 6):
        if len(L) == 1:
            break
        if ann[0][0] == 'R' and ann[0][1] == 3 and L[0] % 2 == 1:
            sig = L[1]
            t = (L[0] - sig - 1) // 3
            k = v2(L[0] + 2 * L[1] + 3)
            dive.append((t, v2(sig), k))
        L, ann = step_ann(L, ann)
        if L is None:
            break
    print("E-block fires in E(1,%d): %d;  k range: %d..%d" %
          (v, len(dive), min(d[2] for d in dive), max(d[2] for d in dive)))
    bad = []
    for j in range(len(dive) - 1):
        (t1, i1, k1), (t2, i2, k2) = dive[j], dive[j + 1]
        if k1 in table and (t2 - t1, i2 - i1) != table[k1]:
            bad.append((t1, i1, k1, (t2 - t1, i2 - i1), table[k1]))
    print("dive-map mismatches vs table:", bad if bad else "NONE (%d transitions checked)" % (len(dive) - 1))
    mind = min(i - t for t, i, k in dive)
    print("min i-t on excursion:", mind, "final:", dive[-1])
