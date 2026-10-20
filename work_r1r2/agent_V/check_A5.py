"""A5: independent check of the bare-tie gateway identities.

(a) symbolic/exact check of the two-step identities for both landing types and both bare ties,
    with arbitrary odd bases u_T, on REAL small crossings of the cached table;
(b) symbolic algebra for arbitrary k, u_T, theta (including theta outside the drift window);
(c) check m = v2(theta+12+9k) (a) / v2(2theta+10+9k) (b), the class formulas
    (10-2^m)/3 and (26-2^m)/3 mod 2^(m+1), and the record inequalities.
Writes check_A5.json.
"""
import json, sys
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
import vlib

T = vlib.Tab(r'D:\math_cc_astra\deep1\table_1000000.pkl', NS=1024)
res = {'cases': [], 'algebra_fail': [], 'real_fail': [], 'n_real': 0, 'n_alg': 0}

cW = T.cW  # my own pair-walk c' data, n<1024

def inv3mod(bits, c):
    return (c * pow(3, -1, 1 << bits)) % (1 << bits)

def check_case(tag, landing, jT, ThetaT, xT, tauT, kT, thetaT, cWn=None, lamn=None,
               tau_b=None):
    """Run the landing step and the j=5 a-step exactly; compare with A5."""
    D_T = ThetaT - xT
    uT = xT >> jT
    assert xT == (1 << jT) * uT and uT % 2 == 1
    if landing == 'a':
        # landing a-step at n=jT-1, tau = 2kT
        xu = 2 * ThetaT + 6 * kT - (xT >> 1)
        Thu = ThetaT + 3 + 6 * kT
        loss_u = 1
        mval = thetaT + 12 + 9 * kT
        mf = 'theta+12+9k'
    else:
        # landing b-step at n=jT-1
        xu = cWn * uT + lamn
        Thu = ThetaT + 3 + 3 * tau_b
        loss_u = 2
        mval = 2 * thetaT + 10 + 9 * kT
        mf = '2theta+10+9k'
    ju = vlib.v2(xu)
    Du = Thu - xu
    rec = {'tag': tag, 'landing': landing, 'jT': jT, 'uT_is_odd': uT % 2 == 1,
           'ju': ju, 'Du_mod64': Du % 64, 'thetaT': thetaT}
    # landing must be at j=5 and be the bare tie (5,5) or (5,-11)
    if ju != 5 or Du % 64 not in (5, 53):
        res['real_fail' if tag.startswith('real') else 'algebra_fail'].append(
            ('landing_not_bare', rec))
        return
    # exact two-step continuation (X(4): odd type a, tau=2, k=1)
    assert T.typ[4] == 97 and T.tau[4] == 2 and T.odd[4]
    x2 = 2 * Thu + 6 - (xu >> 1)
    Th2 = Thu + 3 + 6
    j2 = vlib.v2(x2)
    D2 = Th2 - x2
    m = vlib.v2(mval) if mval else None
    rec.update(x2_exact=x2 if abs(x2) < (1 << 80) else 'big', j2=j2, m=m,
               mval_nonzero=mval != 0, D2_mod=('big' if abs(D2) > (1 << 80) else D2))
    if m is None or j2 != m:
        rec['err'] = 'j2 != v2(mval)'
        res['real_fail' if tag.startswith('real') else 'algebra_fail'].append(rec); return
    # A5 formulas
    if landing == 'a':
        x2_f = 5 * (1 << (jT - 2)) * uT + (D_T + 12 + 9 * kT)
        D2_f = -(1 << (jT - 2)) * uT - 3 * kT
        rec['m_bound_ok'] = m <= jT - 3
        rec['rec_ok'] = (m + loss_u) <= jT - 1 + 0
    else:
        x2_f = 13 * (1 << (jT - 3)) * uT + 2 * D_T + 10 + 9 * kT
        D2_f = -5 * (1 << (jT - 3)) * uT - D_T + 2 - 3 * kT
        rec['m_bound_ok'] = m <= jT - 4
        rec['rec_ok'] = (m + loss_u + 1) <= jT - 1 + 0
    okx = (x2 == x2_f)
    okD = (D2 - D2_f) % (1 << (m + 1)) == 0
    # GENERAL class identity: 3 D2 = (theta_T+12)-2^m (a) or (16-theta_T)-2^m (b),
    # mod 2^(m+1).  This holds for every theta_T with mval != 0.
    bare = Du % 64  # 5 for (5,5), 53 for (5,-11)
    if landing == 'a':
        cgen = thetaT + 12
    else:
        cgen = 16 - thetaT
    # A5's specialization (10-2^m)/3 resp. (26-2^m)/3 needs the exact small value:
    if landing == 'a':
        spec = (thetaT == -2, 10) if bare == 5 else (thetaT == 14, 26)
    else:
        spec = (thetaT == 6, 10) if bare == 5 else (thetaT == -10, 26)
    okclass = (3 * D2 - (cgen - (1 << m))) % (1 << (m + 1)) == 0
    okspec = True
    if spec[0]:
        okspec = (3 * D2 - (spec[1] - (1 << m))) % (1 << (m + 1)) == 0
    rec.update(okx=okx, okD=okD, okclass=okclass, okspec=okspec,
               in_window=(abs(thetaT) <= 20), thetaT_mod64=thetaT % 64,
               D2_f_mod=(D2_f % (1 << (m + 1))))
    if not (okx and okD and okclass and okspec and rec['m_bound_ok'] and rec['rec_ok']):
        key = 'real_fail' if tag.startswith('real') else (
            'inwindow_fail' if abs(thetaT) <= 20 else 'outwindow_general_fail')
        res.setdefault(key, []).append(rec)
    else:
        res['cases'].append(rec)

# ---- real small crossings ---------------------------------------------------------------
# X(16): odd a, tau=12, k=6 (k=6 mod 32).  theta_T = -2 -> v2(3k-2)=4, bare tie (5,5)
# X(53): odd a, tau=44, k=22 (k=22 mod 32). theta_T = 14 -> v2(3k+14)=4, bare tie (5,-11)
# X(64): odd b, tau=52, lambda'=160, c'=3*2^63, omega=5.
for nT, thetaT, want_tie in ((16, -2, 5), (53, 14, 53)):
    jT = nT + 1
    k = T.tau[nT] // 2
    for uT in (1, 3, 5, 12345, (1 << 70) + 7):
        xT = (1 << jT) * uT
        ThT = xT + thetaT
        res['n_real'] += 1
        check_case('real_a_%d_%d' % (nT, uT % 97), 'a', jT, ThT, xT, T.tau[nT], k, thetaT)

nT = 64
jT = 65
tau_b = T.tau[nT]
lamn = T.lam(nT)
cWn = cW[nT]
assert T.typ[nT] == 98 and T.odd[nT] and vlib.v2(lamn) == 5
assert cWn == 3 * (1 << (nT - 1))
for thetaT in (6, -10):
    for uT in (1, 3, 7, 999, (1 << 80) + 3):
        xT = (1 << jT) * uT
        ThT = xT + thetaT
        res['n_real'] += 1
        check_case('real_b_%d_%d' % (thetaT, uT % 97), 'b', jT, ThT, xT, tau_b,
                   tau_b // 2, thetaT, cWn=cWn, lamn=lamn, tau_b=tau_b)

# ---- symbolic algebra: arbitrary k, uT, theta with v2(3k+theta)=4 -----------------------
rng_k = [1, 2, 3, 5, 6, 22, 25, 31, 32, 33, 100, 102, 1000, 10001, 65557]
for k in rng_k:
    for thetaT in (-2, -2 + 64, -2 - 64, -2 + (1 << 40), 14, 14 + 64, 14 - 64,
                   14 + (1 << 39)):
        # only keep cases d=v2(3k+theta)=4 (realizable landing at j=5)
        z = 3 * k + thetaT
        if z == 0 or vlib.v2(z) != 4:
            continue
        for uT in (1, 3, 17, (1 << 55) + 1):
            jT = 200
            xT = (1 << jT) * uT
            ThT = xT + thetaT
            res['n_alg'] += 1
            check_case('alg_a_%d_%d_%d' % (k, thetaT % 100000, uT % 89), 'a', jT, ThT,
                       xT, 2 * k, k, thetaT)
# b-landings need v2(6k+4)=5 (landing parameter 5) and theta_T = 6 mod 64 (bare tie)
for k in (26, 58, 90, 122, 1002, 65562):
    for thetaT in (6, 6 + 64, 6 - 64, 6 + (1 << 40), -10, -10 + 64, -10 - 64,
                   -10 + (1 << 39)):
        z = 6 * k + 4
        if vlib.v2(z) != 5:
            continue
        land_tie = (thetaT - 1) % 64
        if land_tie not in (5, 53):
            continue
        for uT in (1, 3, 17, (1 << 55) + 1):
            jT = 200
            xT = (1 << jT) * uT
            ThT = xT + thetaT
            res['n_alg'] += 1
            check_case('alg_b_%d_%d_%d' % (k, thetaT % 100000, uT % 89), 'b', jT, ThT,
                       xT, 2 * k, k, thetaT, cWn=3 * (1 << (jT - 2)),
                       lamn=z, tau_b=2 * k)

res['t'] = 0
with open(r'D:\math_cc\work_r1r2\agent_V\check_A5.json', 'w', encoding='utf-8') as f:
    json.dump({k: (v[:6] if isinstance(v, list) else v) for k, v in res.items()},
              f, indent=1)
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}, indent=1))
for x in res['real_fail'][:3]:
    print('REALFAIL', x)
for x in res['algebra_fail'][:3]:
    print('ALGFAIL', x)
