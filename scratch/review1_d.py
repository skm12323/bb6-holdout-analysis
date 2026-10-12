"""AUDITOR 1 / Task D -- cross-validate the deep-branch lineage arithmetic.

By hand (this is the whole content):
  At a canonical state (H+d, H, 2H, ..., 2^{r-1}H, J, Z...), A = H+d odd, deep branch
  (v2(q0) >= K, K = 8).  b, c are the next two entries; q0 = A + 2b + 3 = 2^{s'}o'.
  The chain step turns the state into the nested excursion frame
      (o'+1, o', 2o', ..., 2^{s'-2}o', 2^{s'-1}o' + kap_child, window...)
  with  kap_child = c' - 2^{s'-1}o' = c' - q0/2,   c' = c + (A+1)/2.
  Since q0 = A + 2b + 3:
      kap_child = c + (A+1)/2 - (A + 2b + 3)/2 = c + (A + 1 - A - 2b - 3)/2 = c - b - 1.
  -> r >= 2 (b = H, c = 2H):        kap_child = 2H - H - 1 = H - 1
  -> r = 1  (b = H, c = J = 2H+kap): kap_child = J - H - 1 = H + kap_parent - 1
  Note the value is INDEPENDENT of A, d, and s' (how deep the v2 goes): the child
  frame's J-offset class is determined by the parent geometry alone.

Numeric protocol (200 instances, 100 per case):
  random odd w, random j in 11..40 -> H = 3w*2^j (a "high" H, v2(H) = j >= 11);
  random t with t = 84 mod 256, d = 3t+1  (=> d odd, d + 3 = 0 mod 256);
  random r, kap_parent (both lineage classes), random tail entries.
  Checks per instance:
    (1) A = H+d odd and v2(q0) >= 8;
    (2) v2-tracking route: s' = v2(q0), o' = q0/2^s', kap_child = c' - 2^{s'-1}o'
        equals H-1 (r>=2) resp. H + kap_parent - 1 (r=1);
    (3) ground truth: run the concrete chain step (full while-loop) on the list,
        canonically re-encode the result, kap matches (2); and the result equals
        the constructed nested frame entrywise; and no HALT.
"""
import random


def v2(n):
    k = 0
    while n and n % 2 == 0:
        n //= 2
        k += 1
    return k


def cstep(L):
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    if A % 2 == 0:
        return [A + b + c + 3] + L[3:]
    m = b + (A - 3) // 2
    st = [c + (A + 1) // 2] + L[3:]
    while m % 2 == 1 and m >= 3:
        st = [(m + 3) // 2] + st
        m = (m - 3) // 2
    if m == 1:
        return 'HALT'
    return [m + 4] + st


def encode(L):
    """canonical (H, r, kap) of a concrete list (H, 2H, ..., 2^{r-1}H, 2^r H + kap, ...)"""
    assert len(L) >= 3
    H = L[1]
    assert L[2] == 2 * H
    r = 1
    while r + 1 < len(L) and L[r + 1] == H << r:
        r += 1
    assert r + 1 < len(L), 'no J entry'
    return H, r, L[r + 1] - (H << r)


def main(n_each=100, seed=424242):
    rng = random.Random(seed)
    ok_r2 = ok_r1 = 0
    for case in ('r>=2', 'r=1'):
        for i in range(n_each):
            w = 2 * rng.randrange(1, 10 ** 9) + 1                 # random odd w
            j = rng.randrange(11, 41)
            H = 3 * w * (1 << j)                                  # high H, v2(H) = j
            t = 84 + 256 * rng.randrange(0, 10 ** 6)              # t = 84 mod 256
            d = 3 * t + 1                                         # d = 3t+1, odd
            tails = [rng.randrange(0, 10 ** 12) for _ in range(rng.randrange(0, 3))]
            if case == 'r>=2':
                r = rng.randrange(2, 7)
                kapp = rng.choice([-1 + 2048 * rng.randrange(0, 64),
                                   -2 + 128 * rng.randrange(0, 1024)])
                L = [H + d] + [H << i for i in range(r)] + [(H << r) + kapp] + tails
            else:
                r = 1
                kapp = rng.choice([-1 + 2048 * rng.randrange(0, 64),
                                   -2 + 128 * rng.randrange(0, 1024),
                                   rng.randrange(-5, 40)])
                L = [H + d] + [H] + [2 * H + kapp] + tails
            A, b, c = L[0], L[1], L[2]
            assert A % 2 == 1
            q0 = A + 2 * b + 3
            assert q0 % 256 == 0 and v2(q0) >= 8, 'deepness failed'
            s = v2(q0)
            o1 = q0 >> s
            cprime = c + (A + 1) // 2
            kap_track = cprime - (q0 // 2)                 # v2-tracking route
            kap_id = c - b - 1                             # hand identity
            expect = H - 1 if case == 'r>=2' else H + kapp - 1
            assert kap_track == kap_id == expect, (case, kap_track, kap_id, expect)
            # ground truth: actually run the chain step and re-encode
            L2 = cstep(L)
            assert L2 != 'HALT'
            H2, r2, kap2 = encode(L2)
            assert H2 == o1 and r2 == s - 1, (H2, o1, r2, s)
            assert kap2 == expect, (case, kap2, expect)
            constructed = [o1 + 1] + [o1 << i for i in range(s - 1)] \
                          + [(o1 << (s - 1)) + kap2] + list(L[3:])
            assert L2 == constructed, 'frame construction mismatch'
            if case == 'r>=2':
                ok_r2 += 1
            else:
                ok_r1 += 1
    print('TaskD: r>=2 deep branches: %d/%d instances PASS (child kap = H-1 exactly, '
          'ground-truth re-encode agrees)' % (ok_r2, n_each))
    print('TaskD: r=1  deep branches: %d/%d instances PASS (child kap = H+kap_parent-1 '
          'exactly, ground-truth re-encode agrees)' % (ok_r1, n_each))
    print('TaskD: hand identity kap_child = c - b - 1 (independent of A and of v2 depth) '
          'confirmed on all %d instances' % (2 * n_each))


if __name__ == '__main__':
    main()
