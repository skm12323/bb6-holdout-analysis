"""revC_scope.py — ADVERSARY-3 audit 1(b) precision-loss + 5(d) j-scope + §2 re-verify.

Refined correctness model for the residue arithmetic. Every value carries
(v, r, w, e): r agrees with the true odd part m mod 2^w; e=True means r == m EXACTLY
(m < 2^B). Originals have m = 1 (e=True). Operation rules (proved + fuzz-verified in
revC_cadd.py):
  tie, both exact  : s = m1+m2 computed exactly; M = s>>t exact; stays EXACT.
  tie otherwise    : agreement width = min(w1 or B if e1, w2 or B if e2);
                     the tie depth t is EXACT iff t < that width (asserted);
                     new width = width - t.
  unequal, delta<B : agreement mod 2^(delta + w2) from the big side, w1 from the
                     small side; exact if both exact and the true sum fits in B bits.
  unequal, delta>=B: code returns (v_small, r_small): correct; agreement min(B, w_small).
The certificate: at every tie, computed t < agreement width  ==>  by induction every
valuation and every decision of the run is exact (no silent corruption; Deep never
needed beyond its conservative B-16 guard).
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\work_r10')

B = 192
MODR = 1 << B

def v2i(x):
    return (x & -x).bit_length() - 1

class Deep(Exception):
    pass

ties = {'n': 0, 'n_exact': 0, 'max_t': 0, 'min_margin': 10**9, 'min_at': None, 'hist': {}}
min_live_width = [10**9]
n_exact_vals = [0]
n_width_vals = [0]

def cadd_w(c1, c2):
    v1, r1, w1, e1 = c1; v2, r2, w2, e2 = c2
    if v1 == v2:
        s = r1 + r2
        t = v2i(s)
        if t >= B - 16:
            raise Deep('tie depth %d beyond guard at v=%d' % (t, v1))
        if e1 and e2:
            ties['n_exact'] += 1
            return (v1 + t, s >> t, 0, True)     # s>>t < 2^B since s < 2^(B+1), t>=1
        m = min(B if e1 else w1, B if e2 else w2)
        marg = m - t
        if marg < ties['min_margin']:
            ties['min_margin'] = marg; ties['min_at'] = (v1, t, w1, e1, w2, e2)
        if marg <= 0:
            raise AssertionError('SILENT CORRUPTION: tie t=%d >= agreement width %d' % (t, m))
        ties['n'] += 1
        ties['max_t'] = max(ties['max_t'], t)
        ties['hist'][min(t, 16)] = ties['hist'].get(min(t, 16), 0) + 1
        return (v1 + t, (s >> t) % MODR, m - t, False)
    if v1 < v2:
        d = v2 - v1
        if d >= B:
            # code returns (v1, r1): correct residue (2^d m2 = 0 mod 2^B), but the true
            # odd part is m1 + 2^d m2 >= 2^B, so NOT exact: agreement width min(B, w1).
            return (v1, r1, min(B, B if e1 else w1), False)
        if e1 and e2:
            M = r1 + (r2 << d)
            if M < MODR: return (v1, M, 0, True)
            return (v1, M % MODR, B, False)
        w = min(B if e1 else w1, (B if e2 else w2) + d)
        return (v1, (r1 + (r2 << d)) % MODR, w, False)
    if v1 > v2:
        d = v1 - v2
        if d >= B:
            return (v2, r2, min(B, B if e2 else w2), False)
        if e1 and e2:
            M = r2 + (r1 << d)
            if M < MODR: return (v2, M, 0, True)
            return (v2, M % MODR, B, False)
        w = min(B if e2 else w2, (B if e1 else w1) + d)
        return (v2, (r2 + (r1 << d)) % MODR, w, False)

def run(N, verbose=True):
    t0 = time.time()
    A = (0, 1, 1, 0, True)               # (v, r, l, w, exact); c=1 exactly
    P = []                                # [v, r, l, tag, w, exact]
    i = 0; s = 0
    st = {'chains': 0, 'level': 0, 'maxdef': 0, 'd_events': [], 'maxstall': 0,
          'maxs': 0.0, 'maxj_all': 0, 'maxj_all_at': None, 'maxj_lvl': 0,
          'exit5': [], 'firstj': {}, 'firstj_k': {}, 'Dfire': 0, 'maxjD': 0,
          'maxgap': 0, 'lvl_last': 0, 'maxj_by_kind': {}, 'maxj_at': {}}
    last_i = 0; last_move = 0
    while i <= N:
        if len(P) >= 2:
            b, c_ = P[0], P[1]
        elif len(P) == 1:
            b = P[0]; c_ = [i, 1, 0, ('E', i), 0, True]
        else:
            b = [i, 1, 0, ('E', i), 0, True]; c_ = [i + 1, 1, 0, ('E', i + 1), 0, True]
        cpar = 0 if A[0] >= 1 else (A[1] & 1)
        if (cpar + A[2]) % 2 == 0:
            t1 = cadd_w((A[0], A[1], A[3], A[4]), (b[0], b[1], b[4], b[5]))
            cA = cadd_w(t1, (c_[0], c_[1], c_[4], c_[5]))
            A = (cA[0], cA[1], A[2] + b[2] + c_[2] + 3, cA[2], cA[3]); newp = []
        else:
            tx = cadd_w((A[0], A[1], A[3], A[4]), (b[0] + 1, b[1], b[4], b[5]))
            vcx, rcx, wcx, ecx = tx
            lx = A[2] + 2 * b[2] + 3
            vlx = v2i(lx)
            assert vlx < vcx and A[0] >= 1 and A[2] % 2 == 1, (i, s)
            j = vlx
            vu = vcx - j; lu = lx >> j
            assert vu >= 1 and lu % 2 == 1 and lu >= 1, (i, s)
            st['chains'] += 1
            bt = b[3][0]
            key = 'lvl' if bt == 'E' else bt
            if j > st['maxj_by_kind'].get(key, 0):
                st['maxj_by_kind'][key] = j; st['maxj_at'][key] = (i, s)
            if j > st['maxj_all']: st['maxj_all'] = j; st['maxj_all_at'] = (i, s, key)
            if bt == 'E':
                st['level'] += 1
                if j > st['maxj_lvl']: st['maxj_lvl'] = j
                if j not in st['firstj']: st['firstj'][j] = b[3][1]; st['firstj_k'][j] = s // 2
                gap = s - st['lvl_last']
                if gap > st['maxgap']: st['maxgap'] = gap
                st['lvl_last'] = s
            else:
                if j >= 5 and len(st['exit5']) < 8:
                    st['exit5'].append((i, s, j, bt))
                if bt == 'D':
                    st['Dfire'] += 1
                    st['maxjD'] = max(st['maxjD'], j)
            tD = cadd_w((c_[0], c_[1], c_[4], c_[5]), (A[0] - 1, A[1], A[3], A[4]))
            lD = c_[2] + (A[2] + 1) // 2
            newp = [[vu + t, rcx, lu << t, ('M', s), wcx, ecx] for t in range(j - 1)] + \
                   [[tD[0], tD[1], lD, ('D', s), tD[2], tD[3]]]
            A = (vu, rcx, lu + 1, wcx, ecx)
        k = len(P)
        if k >= 2: P = P[2:]
        else: i += 2 - k; P = []
        P = newp + P; s += 1
        if i != last_i:
            st['maxstall'] = max(st['maxstall'], s - last_move); last_i = i; last_move = s
        m = A[0]
        for p in P:
            if p[0] < m: m = p[0]
            if not p[5]: n_width_vals[0] += 1
            else: n_exact_vals[0] += 1
        d = i - m
        if d > st['maxdef']:
            st['maxdef'] = d; st['d_events'].append((d, i, s))
        if s > st['maxs']: st['maxs'] = s
        for vv in [(A[3], A[4])] + [(p[4], p[5]) for p in P]:
            if not vv[1] and vv[0] < min_live_width[0]:
                min_live_width[0] = vv[0]
    el = time.time() - t0
    if verbose:
        print('run to i=%d in %.0fs: %d steps, %d chains, %d level fires' % (N, el, s, st['chains'], st['level']))
        print('TIE CERTIFICATE: %s ties with inexact operands (max t=%d, min margin width-t=%d at %s); %s ties with exact operands'
              % (ties['n'], ties['max_t'], ties['min_margin'], ties['min_at'], ties['n_exact']))
        print('  inexact-tie depth histogram (t capped 16):', dict(sorted(ties['hist'].items())))
        print('  min width among live inexact values = %s (B=%d)' % (min_live_width[0], B))
        print('  REGIME CERTIFICATE: maxdef = %d <= 95  => every live odd part <= 2^96 and'
              % st['maxdef'])
        print('     every valuation gap < 96, so residues are exact and Deep is unreachable: %s'
              % (st['maxdef'] <= 95))
        print('j census by b-entry kind: %s ; at: %s' % (st['maxj_by_kind'], st['maxj_at']))
        print('j census: max j ALL chains = %d at %s ; max level j = %d ; D-fires = %d (max j_D = %d)'
              % (st['maxj_all'], st['maxj_all_at'], st['maxj_lvl'], st['Dfire'], st['maxjD']))
        print('  first exit chains j>=5:', st['exit5'])
        print('deficit records:', st['d_events'])
        print('max s = %d ; max stall = %d ; max level-fire gap = %d' % (st['maxs'], st['maxstall'], st['maxgap']))
        print('first-j level positions (i):', dict(sorted(st['firstj'].items())))
        print('first-j level k:', dict(sorted(st['firstj_k'].items())))
    return st

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000000
    run(N)
