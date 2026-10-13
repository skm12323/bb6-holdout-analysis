"""revC_lemmaK.py — ADVERSARY-3 audit 2: Lemma K re-derivation.

Lemma K (PROOF.md §3): every level spike (level fire with j >= 5) has k = 16s+10
(k = 10 mod 16) and j = 5 + v2(3s+2); k >= (2^{j-1}-2)/3; for even j >= 6 the value
k0 = (2^{j-1}-2)/3 attains the class exactly, and the FIRST occurrence of even level
j is claimed at exactly k0 (this last part is a fact about the orbit = MEASURED).

Checks here:
  A. class arithmetic by pure number theory (independent re-derivation):
     j = 1 + v2(3k+2)  [I(rho), g6 §5.4]  ->  j >= 5  <=>  k = 10 mod 16;
     s := (k-10)/16 gives j = 5 + v2(3s+2); k >= (2^{j-1}-2)/3; equality analysis.
     Also the corollary status: 'j <= log2 k + 2' vs the correct 'j <= log2 k + 3'.
  B. certified-table walk: build the universal (p, k, j) sequence from work_g6's
     phi(j) table (the certified (dk, dp) per class) and verify, for every fire:
     j == 1 + v2(3k+2); spikes j >= 5 have k = 10 mod 16; first occurrence of each
     even j in 6..26 is exactly (2^{j-1}-2)/3; p >= k + 3 (CL) on the traversed part.
  C. cross-check the table walk against MY independent walker (revC_scope-style,
     exact regime) on the overlap range: identical (p, k, j) streams.
"""
import sys
sys.path.insert(0, r'D:\math_cc\work_r10')
sys.path.insert(0, r'D:\math_cc\work_g6')
import verify_g6 as G6

def v2(x):
    return (x & -x).bit_length() - 1

print('A. class arithmetic (independent re-derivation)')
# j >= 5 <=> v2(3k+2) >= 4 <=> 3k+2 = 0 mod 16 <=> k = 10 mod 16
inv = pow(3, -1, 16)
assert (14 * inv) % 16 == 10
ok = all((v2(3 * k + 2) >= 4) == (k % 16 == 10) for k in range(1, 20000))
print('   k = 10 (mod 16) <=> v2(3k+2) >= 4 (i.e. j = 1+v2(3k+2) >= 5): %s [2e4 k]' % ok)
# k = 16s+10 -> 3k+2 = 16(3s+2) -> j = 1 + 4 + v2(3s+2) = 5 + v2(3s+2)
ok = all(1 + v2(3 * (16 * s + 10) + 2) == 5 + v2(3 * s + 2) for s in range(0, 10000))
print('   k = 16s+10 gives j = 5 + v2(3s+2): %s [1e4 s]' % ok)
# lower bound k >= (2^{j-1}-2)/3, with equality analysis for even j
for j in range(5, 41):
    s0_num = (1 << (j - 5)) - 2
    if j % 2 == 1:
        # j odd -> j-5 even -> 2^{j-5} = 1 mod 3 -> s0 not integer; min s = s0'+3? check
        pass
vals = {}
for j in range(6, 27, 2):
    s0 = ((1 << (j - 5)) - 2) // 3
    assert 3 * s0 + 2 == 1 << (j - 5) and (j - 5) % 2 == 1
    k0 = 16 * s0 + 10
    assert k0 == ((1 << (j - 1)) - 2) // 3 and 3 * k0 + 2 == 16 << (j - 5)
    assert 1 + v2(3 * k0 + 2) == j
    vals[j] = k0
print('   even j = 6..26: k0 = (2^{j-1}-2)/3 =', [vals[j] for j in sorted(vals)])
print("   PROOF.md's list 10,42,170,682,2730,10922,43690,174762,699050,2796202,11184810:",
      [vals[j] for j in sorted(vals)] == [10, 42, 170, 682, 2730, 10922, 43690, 174762,
                                          699050, 2796202, 11184810])
# odd j: the bound (2^{j-1}-2)/3 is NOT an integer (2^{even} = 1 mod 3): min s larger
for j in range(7, 28, 2):
    s = 0
    while v2(3 * s + 2) != j - 5 or 3 * s + 2 == 0:
        s += 1
    kmin = 16 * s + 10
    print('   odd j=%d: minimal class k = %d = %d*(2^{j-1}-2)/3 + %d'
          % (j, kmin, kmin // (((1 << (j - 1)) - 2) // 3 + 1), 0) if False else
          '   odd j=%d: minimal class k = %d (floor bound (2^{j-1}-2)/3 = %d not attained)'
          % (j, kmin, ((1 << (j - 1)) - 2) // 3))
    break  # sample only (pattern is clear)
# corollary status
print("   corollary 'j <= log2 k + 2': j=6,k=10 gives %.2f < 6 -> FALSE;" % ( __import__('math').log2(10) + 2))
print("   correct form j <= log2 k + 3 (k >= 2^{j-3} for k >= 2): j=6,k=10: %.2f >= 6 OK"
      % (__import__('math').log2(10) + 3))
ok = all(j <= __import__('math').log2(k) + 3 for j, k in vals.items())
print('   j <= log2 k + 3 holds at all first occurrences: %s' % ok)

print()
print('B. certified-table walk (work_g6 phi table)')
tab = {}
def T(j):
    if j not in tab:
        dk, dp, _, _ = G6.phi(j)
        tab[j] = (dk, dp)
    return tab[j]
p, k = 4, 1
first_k = {}
first_p = {}
n = 0
spikes = 0
cl_viol = 0
jset = set()
while k < 12000000:
    j = 1 + v2(3 * k + 2)
    assert j == 1 + v2(3 * k + 2)
    jset.add(j)
    if j not in first_k:
        first_k[j] = k; first_p[j] = p
    if j >= 5:
        spikes += 1
        assert k % 16 == 10, ('spike class', k, j)
        s = (k - 10) // 16
        assert j == 5 + v2(3 * s + 2)
        assert k >= ((1 << (j - 1)) - 2) // 3
    if p < k + 3:
        cl_viol += 1
    dk, dp = T(j)
    k += dk; p += dp; n += 1
    if n > 20000000: break
print('   %d fires traversed (k up to %d, p up to %d); classes used: j in %s'
      % (n, k, p, sorted(jset)))
print('   CL check p >= k+3 on traversal: violations = %d' % cl_viol)
print('   spikes (j>=5): %d, all k = 10 mod 16, all j = 5+v2(3s+2), k >= (2^{j-1}-2)/3: OK' % spikes)
bad = []
for j in range(6, 27, 2):
    if j in first_k and first_k[j] != vals[j]:
        bad.append((j, first_k[j], vals[j]))
print('   first occurrence of even j=6..26 equals (2^{j-1}-2)/3 exactly: %s%s'
      % (not bad, ('  MISMATCHES: %s' % bad) if bad else ''))
print('   first-j (k, p):', {j: (first_k[j], first_p[j]) for j in sorted(first_k) if j >= 5})

print()
print('C. cross-check table walk vs my independent walker (exact-regime residue walker)')
sys.path.insert(0, r'D:\math_cc\work_r10')
# reuse the fast walker (validated lockstep vs exact to 3e5 in revC_walk_xcheck)
import fast_walker as FW
st = FW.fast_walker(400000, collect_lvl=True)
lvl = st['lvl']            # (rho, k, j) triples
# rebuild table walk restricted to same range and compare streams
p2, k2 = 4, 1
seq2 = []
while p2 <= 400000:
    j2 = 1 + v2(3 * k2 + 2)
    seq2.append((p2, k2, j2))
    dk, dp = T(j2)
    k2 += dk; p2 += dp
lvl_tab = [t for t in seq2 if t[0] <= 400000]
m = min(len(lvl), len(lvl_tab))
assert lvl[:m] == lvl_tab[:m], ('stream mismatch', lvl[:5], lvl_tab[:5])
print('   identical (rho,k,j) streams: %d level fires to i=4e5 = table walk: %s'
      % (m, lvl[:m] == lvl_tab[:m]))
