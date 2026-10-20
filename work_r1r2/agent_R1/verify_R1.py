"""verify_R1.py -- DIRECTION B (R1: no deep->deep c-step) : canonical-table data + structural checks.

Read-only on the repository.  Uses the cached canonical lambda-walk crossing tables produced by
work_global_ext/route_c/fdata.py::lam_walk (cache: D:\\math_cc_astra\\deep1\\table_*.pkl).

Table fields (pickle dict, keys typ, odd, tau, eps, lY, lA):
  typ[n]  97 'a' / 98 'b' / 99 'c'   type of the crossing X(n)  (meaningful only where odd[n])
  odd[n]  parity of W's head at X(n)
  tau[n]  step at which E_n is first read
  eps[n]  deficit  eps(n) = n - v2(c_A)  at X(n)
  lY[n]   lambda part of the pending entry Y at a type-c crossing (0 otherwise)
  lA[n]   lambda part of the head at X(n)
Accepted laws used:  lA[n] + lY[n] = 3*tau[n] + 1 (mass identity at a type-c crossing);
  lambda'_W(n) := 3*tau[n] + 4 + lY[n] (type c),  = 3*tau[n] + 4 (type b);
  omega(n) := v2(lambda'_W(n));  a b/c step has  j' = omega(n).
Checked here (new, see NOTES Section 2):
  lambda'_W(n) = A - 2^{n'}*lambda_u,      A := 6*tau[n] + 4 - 3*tau[n'],
where n' = j_{t'}-1 is the index of the *source chain* t' (the chain of the epoch containing
tau(n) whose a-return is X(n)) and lambda_u its odd base; equivalently
  lA[n] = 2^{n'}*lambda_u + 3*tau[n'] + 1.

Parts
  D1  identity / source-chain decomposition for odd type-c crossings
  D2  omega distributions (type c; type b control), tau, lambda_Y bounds
  D3  congruence structure for large omega (>= 16)
  D4  landing-class / certify analysis for type-c crossings in [lo,N), theta_T in [-30,30]
  D5  exact big-integer walks at the deep boundary (a-steps) + exact walks with all step types

Usage:  python -B verify_R1.py <table.pkl> [lo] [--skip-d4] [--skip-d5]
Writes JSON beside this file.
"""
import sys, os, json, time, pickle

HERE = os.path.dirname(os.path.abspath(__file__))

def v2(x):
    return (x & -x).bit_length() - 1

def sym(e, bits):
    r = e & ((1 << bits) - 1)
    return r - (1 << bits) if r > (1 << (bits - 1)) else r

def load_table(path):
    t0 = time.time()
    with open(path, 'rb') as f:
        D = pickle.load(f)
    typ = D['typ'] if isinstance(D['typ'], bytes) else bytes(D['typ'])
    odd = D['odd'] if isinstance(D['odd'], bytes) else bytes(D['odd'])
    return dict(typ=typ, odd=odd, tau=D['tau'], eps=D['eps'], lY=D['lY'], lA=D['lA'],
                N=len(D['tau']), load_s=round(time.time() - t0, 1))

# ---------------------------------------------------------------- certify (work_claude_shifted Prop 3.2)
_CT = {}

def _cert_env(T, NS=1024):
    if _CT.get('ready'):
        return _CT
    sys.path.insert(0, r'D:\math_cc_astra\deep1')
    sys.path.insert(0, r'D:\math_cc\work_global_ext\route_c')
    import deep_lib
    from fdata import small_full
    t = deep_lib.Table.__new__(deep_lib.Table)
    t.typ = T['typ']; t.oddb = T['odd']; t.tau = T['tau']; t.eps = T['eps']
    t.lY = T['lY']; t.lA = T['lA']; t.N = T['N']
    S = small_full(NS)
    t.cW = {}
    for n, r in S.items():
        if r['odd'] and r['typ'] != 'a':
            t.cW[n] = r['x'][0]
            assert r['x'][1] == t.lam(n), ('lambda mismatch', n)
    t.NS = NS
    _CT.update(ready=True, T=t, deep_lib=deep_lib, small_full=small_full)
    return _CT

def certify(T, j, delta):
    C = _cert_env(T)
    ok, st, w, r = C['deep_lib'].certify(C['T'], j, delta)
    return bool(ok), st, int(r)

def bad_set(T, j):
    M = 1 << (j + 1)
    bad = []
    for d in range(M):
        ok, st, r = certify(T, j, d if d <= M // 2 else d - M)
        if not ok:
            bad.append(d)
    return bad

# ---------------------------------------------------------------- D1/D2/D3
def scan(T, lo, hi, want_sources=False, maxsrc=40):
    typ = T['typ']; odd = T['odd']; tau = T['tau']; lY = T['lY']; lA = T['lA']
    res = {}
    hist = {}
    cnt = 0; mass_bad = 0; ly_viol = 0
    max_tau = 0; max_tau_n = -1
    max_ratio = (0, 1); max_ratio_at = None
    max_ly_minus = None; max_ly_minus_at = None
    max_omega = -1; max_omega_at = None
    ge = {K: 0 for K in (5, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48, 64)}
    big = []
    src = dict(found=0, unique=0, none=0, multi=0, nonodd=0)
    hist_src = {}
    divA = 0; divA_ex = []
    vA_eq_np = 0
    max_A = 0; max_A_at = None; max_bits_A = 0
    examples = []
    pos = typ.find(b'c', lo)
    while 0 <= pos < hi:
        if odd[pos]:
            cnt += 1
            s = tau[pos]; la = lA[pos]; ly = lY[pos]
            lam = la + 2 * ly + 3
            om = v2(lam)
            if la + ly != 3 * s + 1:
                mass_bad += 1
            if ly > 3 * s + 1:
                ly_viol += 1
            hist[om] = hist.get(om, 0) + 1
            for K in ge:
                if om >= K:
                    ge[K] += 1
            if s > max_tau:
                max_tau = s; max_tau_n = pos
            num, den = ly, 3 * s + 4
            if num * max_ratio[1] > max_ratio[0] * den:
                max_ratio = (num, den); max_ratio_at = pos
            d = ly - 3 * s
            if max_ly_minus is None or d > max_ly_minus:
                max_ly_minus = d; max_ly_minus_at = pos
            if om > max_omega:
                max_omega = om; max_omega_at = pos
            if om >= 16 and len(big) < 400:
                big.append([pos, s, ly, om, lam & ((1 << 64) - 1)])
            if want_sources:
                cands = []
                for np_ in range(1, maxsrc + 1):
                    tn = tau[np_]
                    R = la - 3 * tn - 1
                    if R > 0 and v2(R) == np_:
                        cands.append((np_, tn, R >> np_, R))
                if len(cands) == 0:
                    src['none'] += 1
                else:
                    src['unique' if len(cands) == 1 else 'multi'] += 1
                    for (np_, tn, lu, R) in cands:
                        A = 6 * s + 4 - 3 * tn
                        if A - R == lam:
                            src['found'] += 1
                            hist_src[np_] = hist_src.get(np_, 0) + 1
                            if lu % 2 == 0:
                                src['nonodd'] += 1
                            if A > max_A:
                                max_A = A; max_A_at = pos
                            bl = A.bit_length() if A > 0 else 0
                            max_bits_A = max(max_bits_A, bl)
                            if A > 0 and A % (1 << np_) == 0:
                                divA += 1
                                if len(divA_ex) < 20:
                                    divA_ex.append([pos, np_, tn, lu, A, om])
                            if A > 0 and v2(A) == np_:
                                vA_eq_np += 1
                            break
            if om >= 24 and len(examples) < 12:
                examples.append([pos, s, ly, om, la])
        pos = typ.find(b'c', pos + 1)
    res['c'] = dict(count=cnt, omega_hist={str(k): v for k, v in sorted(hist.items())},
                    omega_max=max_omega, omega_max_at=max_omega_at,
                    ge=ge, tau_max=max_tau, tau_max_at=max_tau_n,
                    ly_ratio_max=list(max_ratio), ly_ratio_max_at=max_ratio_at,
                    ly_minus_3tau_max=max_ly_minus, ly_minus_3tau_at=max_ly_minus_at,
                    mass_bad=mass_bad, ly_viol=ly_viol,
                    big=big, big_count=len(big), examples=examples)
    if want_sources:
        res['c']['source'] = dict(src, hist={str(k): v for k, v in sorted(hist_src.items())},
                                  divA=divA, divA_examples=divA_ex, vA_eq_np=vA_eq_np,
                                  A_max=max_A, A_max_at=max_A_at, A_bits_max=max_bits_A)
    hist = {}; cnt = 0; max_om = -1; max_om_at = None
    ge_b = {K: 0 for K in (5, 8, 10, 12, 16, 20, 24, 28, 32, 40)}
    max_tau = 0; max_tau_n = -1
    pos = typ.find(b'b', lo)
    while 0 <= pos < hi:
        if odd[pos]:
            cnt += 1
            s = tau[pos]
            om = v2(3 * s + 4)
            hist[om] = hist.get(om, 0) + 1
            for K in ge_b:
                if om >= K:
                    ge_b[K] += 1
            if s > max_tau:
                max_tau = s; max_tau_n = pos
            if om > max_om:
                max_om = om; max_om_at = pos
        pos = typ.find(b'b', pos + 1)
    res['b'] = dict(count=cnt, omega_hist={str(k): v for k, v in sorted(hist.items())},
                    omega_max=max_om, omega_max_at=max_om_at, ge=ge_b,
                    tau_max=max_tau, tau_max_at=max_tau_n)
    return res

# ---------------------------------------------------------------- D4
def landing_classes(T, lo, hi, thetas=list(range(-30, 31))):
    typ = T['typ']; odd = T['odd']; tau = T['tau']; lY = T['lY']; lA = T['lA']
    badcache = {}
    stats = dict(count=0, bad_theta1=0, bad_anytheta=0, examples=[], bad_sets={},
                 omega_hist={}, theta_min=-30, theta_max=30)
    pos = typ.find(b'c', lo)
    while 0 <= pos < hi:
        if odd[pos]:
            s = tau[pos]; ly = lY[pos]
            lam = lA[pos] + 2 * ly + 3
            om = v2(lam)
            stats['count'] += 1
            k = str(om)
            stats['omega_hist'][k] = stats['omega_hist'].get(k, 0) + 1
            if om not in badcache:
                badcache[om] = bad_set(T, om)
                stats['bad_sets'][k] = badcache[om]
            M = 1 << (om + 1)
            base = (3 * s + 3 - (1 << om)) % M
            bad = badcache[om]
            if base in bad:
                stats['bad_theta1'] += 1
                if len(stats['examples']) < 12:
                    stats['examples'].append(dict(n=pos, tau=s, lY=ly, omega=om, base=base,
                                                  theta=1, sym=sym(base, om + 1), kind='theta1'))
            hit = False
            for b in bad:
                d = (b - base) % M
                if d <= 29 or d >= M - 31:
                    hit = True
                    stats.setdefault('hit_offsets', {})[str(d if d <= 29 else d - M)] = \
                        stats.get('hit_offsets', {}).get(str(d if d <= 29 else d - M), 0) + 1
                    break
            if hit:
                stats['bad_anytheta'] += 1
        pos = typ.find(b'c', pos + 1)
    return stats

# ---------------------------------------------------------------- D5
def exact_walk(tau, typ, odd, eps, lY, cW, j, delt, nmax, limit=8):
    """exact integer walk from (2^j, 2^j+delt).  cW[n] = c'_W(n) required at b/c steps."""
    x = 1 << j
    th = x + delt
    G = 0
    steps = []
    for _ in range(limit):
        if x == 0:
            steps.append(dict(st='zero')); break
        jj = v2(x)
        rec = jj + G
        n = jj - 1
        if n >= nmax:
            steps.append(dict(st='nodata', j=jj)); break
        if not odd[n]:
            steps.append(dict(st='end', j=jj, rec=rec)); break
        s = tau[n]
        if typ[n] == 97:
            k = s // 2
            z = 3 * k + (th - x)
            x = 2 * th + 3 * s - (x >> 1)
            th += 3 + 3 * s
            steps.append(dict(st='a', j=jj, rec=rec, n=n, tau=s, v2z=v2(z) if z else None,
                              z0=(z == 0), j_next=v2(x) if x else None))
        else:
            lam = 3 * s + 4 + (lY[n] if typ[n] == 99 else 0)
            om = v2(lam)
            if n not in cW:
                steps.append(dict(st='no-cW', j=jj, n=n)); break
            sig = n - eps[n]
            d_old = th - x
            x = cW[n] * (x >> jj) + lam
            th += 3 + 3 * s
            G += 1 + eps[n]
            steps.append(dict(st=chr(typ[n]), j=jj, rec=rec, n=n, tau=s, omega=om, sig=sig,
                              pred_rec_next=om + G, rec_next=v2(x) + G,
                              pred_drop=sig - om,
                              theta_pred=(d_old + 3 * s + 3) & ((1 << om) - 1),
                              theta_act=(th - x) & ((1 << om) - 1),
                              lamW_hi=(lam >> om) & 1))
        if len(steps) >= 4:
            break
    return steps

# ---------------------------------------------------------------- main
def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__); return
    path = args[0]
    N0 = 2 * 10 ** 7
    lo = int(args[1]) if len(args) > 1 else N0
    skip_d4 = '--skip-d4' in sys.argv
    skip_d5 = '--skip-d5' in sys.argv
    T = load_table(path)
    N = T['N']
    out = dict(table=path, N=N, N0=N0, load_s=T['load_s'])
    print('loaded', path, 'N=%d' % N, T['load_s'], 's', flush=True)
    t0 = time.time()
    out['all'] = scan(T, 1, N, want_sources=False)
    out['all']['seconds'] = round(time.time() - t0, 1)
    print('ALL done %.1fs' % (time.time() - t0), flush=True)
    print(json.dumps(out['all'], indent=1)[:5000], flush=True)
    if lo < N:
        t0 = time.time()
        out['deep'] = scan(T, lo, N, want_sources=False)
        out['deep']['seconds'] = round(time.time() - t0, 1)
        print('DEEP [%d,%d) done %.1fs' % (lo, N, time.time() - t0), flush=True)
        print(json.dumps(out['deep'], indent=1)[:5000], flush=True)
    t0 = time.time()
    if not skip_d4:
        out['landing'] = landing_classes(T, lo if lo < N else N // 2, N)
        out['landing']['seconds'] = round(time.time() - t0, 1)
        print('LANDING %.1fs' % (time.time() - t0),
              {k: out['landing'][k] for k in ('count', 'bad_theta1', 'bad_anytheta')}, flush=True)
        print(json.dumps({k: v for k, v in out['landing'].items() if k != 'bad_sets'})[:2000], flush=True)
    t0 = time.time()
    if not skip_d5:
        C = _cert_env(T)
        NS = 200001
        S = C['small_full'](NS)
        tau = T['tau']; typ = T['typ']; odd = T['odd']; eps = T['eps']; lY = T['lY']
        cW = {}
        for n, r in S.items():
            if r['odd'] and r['typ'] != 'a':
                cW[n] = r['x'][0]
        # (i) exact full walks from a moderate parameter (all step types available)
        ex = []
        for j in (200000, 199999, 123456):
            for d in (1, -1, 12345):
                if j - 1 < NS:
                    ex.append(dict(j=j, delta=d, steps=exact_walk(tau, typ, odd, eps, lY, cW, j, d, NS)))
        # (i-b) exact walks started at moderate type-c crossings (genuine c'_W available)
        cst = []
        posc = T['typ'].find(b'c', 100000)
        picksc = []
        while 0 <= posc < 199000 and len(picksc) < 4:
            if T['odd'][posc]:
                picksc.append(posc)
            posc = T['typ'].find(b'c', posc + 1)
        for n in picksc:
            if (n + 1) - 1 < NS:
                for d in (1, -1, 12345):
                    cst.append(dict(j=n + 1, n=n, delta=d,
                                    steps=exact_walk(tau, typ, odd, eps, lY, cW, n + 1, d, NS)))
        ex.append(dict(c_entries=cst))
        # (ii) exact big-integer walks at the deep boundary, on odd-a crossings (a-steps only needed)
        deep = []
        if lo < N:
            pos = typ.find(b'a', lo)
            picks = []
            while 0 <= pos < N and len(picks) < 3:
                if odd[pos]:
                    picks.append(pos)
                pos = typ.find(b'a', pos + 1)
            for n in picks:
                j = n + 1
                for d in (1, -3):
                    deep.append(dict(j=j, n=n, delta=d,
                                     steps=exact_walk(tau, typ, odd, eps, lY, cW, j, d, N)))
        out['exact'] = dict(moderate=ex, deep=deep)
        out['exact_seconds'] = round(time.time() - t0, 1)
        print(json.dumps(out['exact'], indent=1)[:4000], flush=True)
    fp = os.path.join(HERE, 'verify_R1_%s.json' % os.path.basename(path).replace('.pkl', ''))
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, default=str)
    print('wrote', fp, flush=True)

if __name__ == '__main__':
    main()
