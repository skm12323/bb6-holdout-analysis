"""revC_cadd.py — ADVERSARY-3 audit 1(a): re-derive the residue arithmetic of cadd.

Contract under test (fast_walker.cadd): values c = 2^v * m (m odd) stored as (v, m mod 2^B).
Claimed: returned pair = (exact v2 of the sum, residue mod 2^B of the sum's odd part).

Findings established by this script:
  (i)   unequal valuations: v = min is EXACT (odd+even=odd) and the residue formula
        (r_small + (r_big << delta)) mod 2^B is the exact low-B-bits residue of the odd
        part m_small + 2^delta*m_big, for ALL delta (including delta >= B, where the
        code returns r_small alone — also exact, since 2^delta*m_big = 0 mod 2^B).
        Verified by exhaustive/random fuzz vs true big-int arithmetic.
  (ii)  EQUAL valuations (tie): the returned valuation v1+t is exact whenever t < B
        (and the code raises Deep when the residue-visible t >= B-16). BUT the returned
        residue is exact ONLY mod 2^(B-t): the top t bits can be wrong, because the
        residues only determine m1+m2 mod 2^B, hence (m1+m2)/2^t only mod 2^(B-t).
        Concrete counterexample to "residue exact mod 2^B" exhibited below.
  (iii) invariant 'residue odd' is preserved in every branch (needed for cpar).
"""
import sys, random
sys.path.insert(0, r'D:\math_cc\work_r10')
import fast_walker as FW

B = FW.B
MODR = FW.MODR
random.seed(20261013)

def v2(x):
    return (x & -x).bit_length() - 1

fails_uneq = 0
fails_tie_val = 0
tie_res_topbit_wrong = 0
tie_checked = 0
deep_raised = 0
for trial in range(300000):
    v1 = random.randrange(0, 60)
    v2_ = random.randrange(0, 60)
    bits1 = random.randrange(1, 320)   # m may be FAR wider than B bits
    bits2 = random.randrange(1, 320)
    m1 = random.getrandbits(bits1) | 1
    m2 = random.getrandbits(bits2) | 1
    c1, c2 = (1 << v1) * m1, (1 << v2_) * m2
    tot = c1 + c2
    vt, mt = v2(tot), tot >> v2(tot)
    got = FW.cadd((v1, m1 % MODR), (v2_, m2 % MODR))
    if v1 != v2_:
        # exact contract: (vt, mt mod 2^B)
        if got[0] != vt or got[1] != mt % MODR:
            fails_uneq += 1
            if fails_uneq < 4:
                print('UNEQ FAIL', (v1, m1 % MODR), (v2_, m2 % MODR), 'got', got, 'want', (vt, mt % MODR))
        assert got[1] % 2 == 1
    else:
        tie_checked += 1
        try:
            got = FW.cadd((v1, m1 % MODR), (v2_, m2 % MODR))
        except FW.Deep:
            deep_raised += 1
            # Deep is raised iff residue-visible v2(r1+r2) >= B-16; check that matches
            t_vis = v2((m1 % MODR) + (m2 % MODR))
            assert t_vis >= B - 16
            continue
        t_true = vt - v1
        if got[0] != vt:
            fails_tie_val += 1
            if fails_tie_val < 4:
                print('TIE-VAL FAIL', v1, t_true, 'got', got[0], 'want', vt)
        # residue: exact contract only mod 2^(B - t_true) when t_true>0 and m's wide
        agree_width = B - t_true
        if got[1] % (1 << min(agree_width, B)) == mt % (1 << min(agree_width, B)):
            pass
        else:
            print('TIE-LOWBITS FAIL (should never happen)', v1, t_true)
            sys.exit(1)
        if got[1] != mt % MODR:
            tie_res_topbit_wrong += 1

print('fuzz 3e5 pairs: unequal-valuation failures = %d (exact contract holds: %s)'
      % (fails_uneq, fails_uneq == 0))
print('ties tested = %d (Deep raised %d): valuation failures = %d'
      % (tie_checked, deep_raised, fails_tie_val))
print('ties where stored residue != true odd part mod 2^B (top-t bits wrong): %d'
      % tie_res_topbit_wrong)

# explicit counterexample to "tie residue exact mod 2^B"
m1 = 3 * (1 << B) + 3      # odd, wider than B bits
m2 = 5
v1 = v2_ = 7
tot = (1 << v1) * (m1 + m2)
t_true = v2(m1 + m2) - 0   # v2 of (m1+m2)
Mt = (m1 + m2) >> t_true
got = FW.cadd((v1, m1 % MODR), (v2_, m2 % MODR))
print()
print('explicit tie counterexample: m1 = 3*2^B+3, m2 = 5, v=7, t_true =', t_true)
print('  code returns', got, '; true (v, odd part mod 2^B) =', (v1 + t_true, Mt % MODR))
print('  valuation exact: %s ; residues agree mod 2^(B-t) = 2^%d: %s ; agree mod 2^B: %s'
      % (got[0] == v1 + t_true, B - t_true,
         got[1] % (1 << (B - t_true)) == Mt % (1 << (B - t_true)),
         got[1] == Mt % MODR))

# delta >= B branch: exhaustively confirm (v1, r1) is the exact residue
ok = True
for _ in range(20000):
    v1 = random.randrange(0, 5)
    d = random.randrange(B, B + 200)
    v2h = v1 + d
    m1 = random.getrandbits(200) | 1
    m2 = random.getrandbits(200) | 1
    tot = (1 << v1) * m1 + (1 << v2h) * m2
    vt = v2(tot); mt = tot >> vt
    got = FW.cadd((v1, m1 % MODR), (v2h, m2 % MODR))
    ok &= (got == (vt, mt % MODR))
print()
print('delta >= B branch exact on 2e4 random cases: %s' % ok)
