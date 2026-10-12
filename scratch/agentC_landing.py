"""Verify the landing formulas for mid-block R-fires (c = run i+1):

  fire at (D=3t+1, i), k = v2(3t+4):
    k odd :  land before run i+3 with D_land = 3t + (3k+11)/2
    k even:  land before run i+2 with D_land = 3t + (3k+8)/2
  (then if D_land even, one more step: D+3, i+2.)

Also verify the fire value law x = 3*sigma + D + 3 (R), +1 (T), and the
chain base q = (3 sigma + R)/2^k odd."""
import agentC_lib as lib
from collections import Counter

def E(w, v):
    if v == 1:
        return [3 * w + 1, 3 * w - 1], [('T', 3 * w)]
    vals = [3 * w + 1] + [3 * w << i for i in range(v - 1)] + [(3 * w << (v - 1)) - 1]
    ann = [('R', 3 * w, i) for i in range(v - 1)] + [('T', 3 * w << (v - 2))]
    return vals, ann

def step_ann(L, ann):
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    if A % 2 == 0:
        return [A + b + c + 3] + L[3:], ann[2:]
    x = A + 2 * b + 3
    k = lib.v2(x)
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

checked = 0
formok = Counter()
formbad = 0
xlaw_bad = 0
qodd_bad = 0
for w in (1, 3, 5, 17, 41):
    for v in range(7, 260):
        L, ann = E(w, v)
        hist = []   # (role, D, i, sigma) sequence
        for s in range(10 ** 5):
            if len(L) == 1:
                break
            role = ann[0][0]
            # c is a plain E-run iff role R and ann[1] is R with beta 3w and idx+1
            c_is_run = (role == 'R' and len(ann) > 1 and ann[1][0] == 'R'
                        and ann[1][1] == ann[0][1] and ann[1][2] == ann[0][2] + 1)
            sig = L[1] + 1 if role == 'T' else L[1]
            i = lib.v2(sig)
            D = L[0] - sig
            fire = L[0] % 2 == 1
            rec = None
            if fire:
                x = L[0] + 2 * L[1] + 3
                k = lib.v2(x)
                R = D + (3 if role == 'R' else 1)
                if x != 3 * sig + R:
                    xlaw_bad += 1
                if (x >> k) % 2 != 1:
                    qodd_bad += 1
                rec = (role, D, i, k, c_is_run, t_idx := s)
            hist.append((s, role, D, i, fire, rec, c_is_run))
            L, ann = step_ann(L, ann)
            if L is None:
                break
        # check landing formulas: for each fire with c_is_run in the E-block
        # (beta == 3w: identified by sig being 3w<<i ... approximate: just
        #  use c_is_run and next fire in same block = next R/T fire whose
        #  sigma = 4^j*3w; simpler: verify prediction of next fire D,i)
        for idx in range(len(hist)):
            s, role, D, i, fire, rec, c_is_run = hist[idx]
            if not fire or role == 'S' or not c_is_run:
                continue
            rrole, rD, ri, rk, _, _ = rec
            if rrole != 'R':
                continue  # only R mid-block fires
            t = (rD - 1) // 3
            k = rk
            # find next R/T fire after idx
            nxt = None
            for j2 in range(idx + 1, len(hist)):
                s2, role2, D2, i2, fire2, rec2, c2 = hist[j2]
                if fire2 and role2 in ('R', 'T'):
                    # skip fires inside the spawned chain: they have small i
                    if i2 <= 4 and i2 <= ri:
                        # could be chain fire; skip if within few steps
                        if j2 - idx <= 4 and i2 < ri:
                            continue
                    nxt = (role2, D2, i2, j2 - idx)
                    break
            if nxt is None:
                continue
            nrole, nD, ni, gap = nxt
            checked += 1
            if k % 2 == 1:
                Dp = 3 * t + (3 * k + 11) // 2
                ip = ri + 3
            else:
                Dp = 3 * t + (3 * k + 8) // 2
                ip = ri + 2
            # allow one extra +3/+2 step if Dp even, and chain-internal fires
            cands = [(Dp, ip), (Dp + 3, ip + 2)]
            formok["k%d" % (k % 2)] += 1
            if (nD, ni) not in cands:
                formbad += 1
                if formbad <= 10:
                    print("LANDING MISMATCH w=%d v=%d: fire (t=%d,i=%d,k=%d) pred %s got (%d,%d) role=%s gap=%d"
                          % (w, v, t, ri, k, cands, nD, ni, nrole, gap))
print("mid-block fires checked:", checked, "dict:", dict(formok), "bad:", formbad)
print("x-law violations:", xlaw_bad, " q-odd violations:", qodd_bad)
