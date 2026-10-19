"""verify_shifted.py -- finite checks for work_claude_shifted/NOTES.md (UNREVIEWED).

Usage: python -B verify_shifted.py [N] [M_FAM] [N_SJ]
  N     table size for the theta-walk / certificate scan (default 2*10^7)
  M_FAM families G_delta(m), H_e(m) scanned for odd-a m < M_FAM (default 2*10^5)
  N_SJ  S(J) compared with the theta-walk for 5 <= J < N_SJ (default N)
Writes shifted_checks.json beside itself.  Finite computations only: nothing here proves EXT.
"""
import sys, json, time, random
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from shiftlib import Tables, DefectTable, dw, sym_beta, exact_tail, certify, symres, v2  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10**7
M_FAM = int(sys.argv[2]) if len(sys.argv) > 2 else 2 * 10**5
N_SJ = int(sys.argv[3]) if len(sys.argv) > 3 else N
WIN = range(-12, 16)          # defect window [-12, 15]
T0 = time.time(); RES = dict(N=N, M_FAM=M_FAM, N_SJ=N_SJ, window=[WIN.start, WIN.stop - 1])
T = Tables(N); DT = DefectTable(T)
def log(*a): print(round(time.time() - T0, 1), *a, flush=True)
log('tables')

# ---------------------------------------------------------------- V0 crossing facts used in the notes
odd_a = [(n + 1, T.tau[n] // 2) for n in range(0, 80) if T.odd[n] and T.kind(n) == 'a']
assert all(not T.odd[n] for n in range(4))                      # j <= 4 ends
assert odd_a[:2] == [(5, 1), (8, 2)] and (17, 6) in odd_a
RES['V0_small_odd_a_(j,k)'] = odd_a[:12]
RES['V0_tie_residue_r_j=2^(j-2)-3k_j'] = {j: (1 << (j - 2)) - 3 * k for j, k in odd_a[:8]}

# ---------------------------------------------------------------- V1 theorem SC on random exact states
random.seed(1)
v1 = Counter()
for _ in range(200000):
    j0 = random.randint(5, 60); u = random.getrandbits(80) | 1; x = u << j0
    th = x + random.randint(-40, 40) + (random.getrandbits(90) << (j0 + 1)) * random.choice((0, 1))
    path, st = dw(DT, j0, th - x)
    # exact walk
    xx, tt, G, js, recs = x, th, 0, [], []
    for step in range(len(path) + 1):
        j = v2(xx); js.append(j); recs.append(j + G)
        n = j - 1
        if j <= 4 or not T.odd[n]: break
        if T.kind(n) == 'a':
            xx = 2 * tt + 3 * T.tau[n] - (xx >> 1)
        else:
            xx = T.cW[n] * (xx >> j) + T.lam(n)
        tt += 3 + 3 * T.tau[n]; G += 1 + T.eps[n]
        if xx == 0: break
    pj = [p[0] for p in path]
    if st == 'ND':
        # exact walk agrees up to the tie chain; the exact next parameter is >= the tie parameter
        assert js[:len(pj)] == pj, (j0, th - x, pj, js)
        if len(js) > len(pj):
            assert js[len(pj)] >= pj[-1]; v1['ND_next>=j'] += 1
        v1['ND'] += 1
    else:
        assert js == pj[:len(js)] and (len(js) == len(pj) or pj[-1] <= 4), (j0, th - x, pj, js)
        assert all(recs[i + 1] <= recs[i] for i in range(len(recs) - 1))   # records non-increasing
        v1[st] += 1
RES['V1_SC_random_states'] = dict(v1)
log('V1', dict(v1))

# ---------------------------------------------------------------- V2 S(J) = theta-walk from (J, 1); DH/NT census
v2c = Counter(); res_at_a = Counter()
for J in range(5, N_SJ):
    if not T.odd[J - 1]:
        continue
    out, st = sym_beta(T, J); assert st == 'end'
    path, s2 = dw(DT, J, 1); assert s2 == 'end'
    assert [c[0] for c in out] == [p[0] for p in path], J
    for i in range(len(out) - 1):
        j, d, beta, G, k = out[i]
        if k == 'a':
            th = 3 * d + 1 - beta if i else 1
            r = symres(th, j); res_at_a[r] += 1
            z = 3 * (T.tau[j - 1] // 2) + r
            if v2(z) >= j - 2: v2c['DH_fail'] += 1
            if v2(z) == j - 2: v2c['NT_fail'] += 1
    v2c['J'] += 1
RES['V2_SJ'] = dict(v2c); RES['V2_theta_at_a_steps'] = dict(sorted(res_at_a.items()))
log('V2', dict(v2c), dict(res_at_a))

# ---------------------------------------------------------------- V3 reference families
fam = {}
ms = [n + 1 for n in range(4, min(M_FAM, N)) if T.odd[n] and T.kind(n) == 'a']
for name, c0 in (('G', 4), ('H', 6)):
    for dl in WIN:
        cnt = Counter()
        for m in ms:
            k = T.tau[m - 1] // 2; z = 6 * k + c0 - 2 * dl
            if z == 0:
                cnt['z=0'] += 1; continue
            j0 = v2(z)
            if j0 >= m - 1:
                cnt['j0>=m-1 (no reduction)'] += 1; continue
            st, w, r = exact_tail(T, z, z + dl, m - 1)
            closes = st == 'end'
            path, s2 = dw(DT, j0, dl)
            pj = [p[0] for p in path]
            if s2 != 'ND':
                assert w == pj[:len(w)] and r <= j0 and closes
                cnt['NT-good, closes, rec<=j0'] += 1
            else:
                assert w[:len(pj)] == pj
                cnt['NT-fail, closes' if closes else 'NT-fail, OPEN:' + st] += 1
            if 6 <= j0 < N or (j0 == 5 and dl % 16 != 5):
                ok, *_ = certify(T, j0, dl)
                assert ok and closes and r <= j0, (name, dl, m)
                cnt['certified'] += 1
        fam['%s_%d' % (name, dl)] = dict(cnt)
RES['V3_families_odd_a_m<M_FAM'] = fam
log('V3 done')

# ---------------------------------------------------------------- V4 NT-failure (Bad) table + certificate
SM = 3000; memo = {}
def bad_small(j, d):
    key = (j, symres(d, j))
    if key not in memo:
        memo[key] = dw(DT, j, d)[1] == 'ND'
    return memo[key]
bad = [(j, d) for j in range(5, SM) for d in WIN if bad_small(j, d)]
typ, odd, tau, lA, lY = T.typ, T.odd, T.tau, T.lA, T.lY
for n in range(SM - 1, N):
    if not odd[n]: continue
    j = n + 1
    if typ[n] == 97:
        k3 = 3 * (tau[n] // 2)
        for d in WIN:
            if bad_small(1 + v2(k3 + d), 3 - d): bad.append((j, d))
    else:
        lam = lA[n] + 2 * lY[n] + 3; om = v2(lam); ph = 3 * tau[n] + 5 - lam
        for d in WIN:
            if bad_small(om, d + ph - 2): bad.append((j, d))
log('V4 bad', len(bad))
cert = Counter(); unc = []
bydelta = Counter(d for _, d in bad)
for j, d in bad:
    ok, st, w, r = certify(T, j, d)
    cert[(d, ok)] += 1
    if not ok: unc.append((j, d, st, w))
# also certify every window pair with j < SM directly (NT-good pairs included)
direct = Counter()
for j in range(5, SM):
    for d in WIN:
        ok, *_ = certify(T, j, d); direct[ok] += 1
        if not ok: assert j == 5 and d % 16 == 5, (j, d)
RES['V4_bad_count_by_delta'] = dict(sorted(bydelta.items()))
RES['V4_bad_first_js'] = {d: [j for j, dd in bad if dd == d][:10] for d in sorted(bydelta)}
RES['V4_certificate_of_bad_pairs'] = {'%d_%s' % k: v for k, v in sorted(cert.items())}
RES['V4_uncertified'] = unc
RES['V4_direct_certificate_j<3000'] = dict(direct)
assert all(j == 5 and d % 16 == 5 for j, d, *_ in unc)
log('V4', dict(cert), unc)

# ---------------------------------------------------------------- V5 complete residues, small j
v5 = {}
for j in range(5, 19):
    M = 1 << (j + 1); un = []
    for rr in range(M):
        d = rr - M if rr >= M // 2 else rr
        ok, st, w, r = certify(T, j, d)
        if not ok: un.append((d, st, w))
    v5[j] = dict(residues=M, uncertified=len(un), examples=un[:8])
RES['V5_all_residues_mod_2^(j+1)'] = v5
log('V5')

# ---------------------------------------------------------------- V6 the accepted WITNESS tail (PROOF_SPECTRUM §4)
# (17,-2) is the b-copy state of the witness; check the tie, the DH failure and the safe resolution.
path, st = dw(DT, 17, -2)
assert [p[:2] for p in path] == [(17, -2), (5, 5)] and st == 'ND'
k5 = 1; assert v2(6 * k5 + 2 * 5) == 4 == 5 - 1          # DH fails at (5,5): v2(6k+2d) = j-1
ok, st, w, r = certify(T, 17, -2); assert ok and w == [17, 5, 6, 1]
# G_{-3}(5) = reference of the c crossing with history BBBAA: z = 16, v2 = 4 = m-1 -> no DR margin
z = 6 * 1 + 4 + 6; assert v2(z) == 4
RES['V6_witness'] = {'theta_walk': [p[:2] for p in path], 'status': 'ND at (5,5)', 'certified_word': w,
                     'record': r, 'DH_at_(5,5)': 'v2(6k+2d)=4=j-1 (fails)', 'G_-3(5)_z': z}
RES['seconds'] = round(time.time() - T0, 1); RES['result'] = 'PASS'; RES['review_status'] = 'UNREVIEWED'
RES['scope'] = ('Finite exact computations (tables from the certified lambda walk to index N). '
                'They certify the stated (j,delta) pairs for all scales of the outer index but say nothing about '
                'parameters >= N or defects outside the window; EXT is not claimed.')
HERE.joinpath('shifted_checks.json').write_text(json.dumps(RES, indent=1, default=str) + '\n', encoding='utf-8')
log('PASS')
