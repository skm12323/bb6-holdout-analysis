"""work_r10/fast_walker.py — residue-arithmetic walker for the formal map F (work_g6 §5).

F states: A=(cA,lA); P=[(c,l,tag)...]; original suffix E_a=(2^a,0), a>=i. One step:
  parity = (cA+lA)%2;  even: A += b+c (l-part +3);
  chain: cx=cA+2cb, lx=lA+2lb+3; REQUIRE v2(lx)<v2(cx) (S1), cA even, lA odd;
         j=v2(lx); u=(cx>>j, lx>>j); push u<<t (t=0..j-2), D=(cc+cA/2, lc+(lA+1)/2);
         A=(cu, lu+1);  consume 2 from front (or advance i).

FAST REPRESENTATION: each c = 2^v * m (m odd) stored as (v, m mod 2^B), B=192.
  add: unequal valuations -> min (exact, residue of the smaller); equal -> the sum's
  valuation from the residues; if that valuation >= B-16 the residue is unreliable
  (Deep) and we raise (counted; expected never).  lambda kept exact (<= 3s+1).
Cross-validated against an exact-bigint walker on a prefix (same (rho,k,j) stream,
same (i,s) trace).

Usage: python fast_walker.py [N=10**7] [XCHECK=2*10**5]
"""
import sys, time

B = 192
MODR = 1 << B
def v2i(x):
    return (x & -x).bit_length() - 1

class Deep(Exception):
    pass

def cadd(c1, c2):
    v1, r1 = c1; v2, r2 = c2
    if v1 == v2:
        s = r1 + r2                   # both odd -> even
        t = v2i(s)
        if t >= B - 16:
            raise Deep('tie resolves beyond residue width at v=%d' % v1)
        return (v1 + t, (s >> t) % MODR)
    if v1 < v2:
        if v2 - v1 >= B: return (v1, r1)
        return (v1, (r1 + (r2 << (v2 - v1))) % MODR)
    if v1 - v2 >= B: return (v2, r2)
    return (v2, (r2 + (r1 << (v1 - v2))) % MODR)

def fast_walker(N, collect_lvl=True):
    st = {'s': 0, 'chains': 0, 'level': 0, 'maxdef': 0, 'maxdef_at': None,
          'maxdeft': 0, 'maxdeft_at': None, 'maxstall': 0, 'maxs_ov_i': 0.0,
          'deep': 0, 'lvl_last': 0, 'maxlvlgap': 0, 'd_events': [], 'lvl': []}
    A = (0, 1, 1)                     # (v2(cA), residue(cA), lA); cA = 1
    P = []
    i = 0; s = 0
    last_i = 0; last_move = 0
    while i <= N:
        if len(P) >= 2:
            (vb, rb, lb, tb) = P[0]; (vc_, rc_, lc_, tc_) = P[1]
        elif len(P) == 1:
            (vb, rb, lb, tb) = P[0]; (vc_, rc_, lc_, tc_) = (i, 1, 0, ('E', i))
        else:
            (vb, rb, lb, tb) = (i, 1, 0, ('E', i)); (vc_, rc_, lc_, tc_) = (i + 1, 1, 0, ('E', i + 1))
        cpar = 0 if A[0] >= 1 else (A[1] & 1)   # cA = 2^v * odd: even iff v >= 1
        if (cpar + A[2]) % 2 == 0:
            t1 = cadd((A[0], A[1]), (vb, rb))
            cA = cadd(t1, (vc_, rc_))
            A = (cA[0], cA[1], A[2] + lb + lc_ + 3)
            newp = []
        else:
            tx = cadd((A[0], A[1]), (vb + 1, rb))
            lx = A[2] + 2 * lb + 3
            vcx, rcx = tx
            vlx = v2i(lx)
            if not (vlx < vcx):
                raise AssertionError('margin S1 fails at i=%d s=%d (vlx=%d vcx=%d)' % (i, s, vlx, vcx))
            if A[0] < 1 or A[2] % 2 != 1:
                raise AssertionError('parity invariant fails at i=%d s=%d' % (i, s))
            j = vlx
            vu = vcx - j; ru = rcx; lu = lx >> j
            if vu < 1 or lu % 2 != 1 or lu < 1:
                raise AssertionError('u-form fails at i=%d s=%d (vu=%d lu=%d)' % (i, s, vu, lu))
            st['chains'] += 1
            dch = i - vcx
            if dch > st['maxdeft']:
                st['maxdeft'] = dch; st['maxdeft_at'] = (i, s)
            tD = cadd((vc_, rc_), (A[0] - 1, A[1]))
            lD = lc_ + (A[2] + 1) // 2
            if tb[0] == 'E':
                st['level'] += 1
                rho = tb[1]
                if not (vcx == rho and rcx == 3 and lx == 3 * s + 4 and s % 2 == 0 and len(P) == 0):
                    raise AssertionError('I(rho) fails at rho=%d s=%d' % (rho, s))
                gap = s - st['lvl_last']
                if gap > st['maxlvlgap']: st['maxlvlgap'] = gap
                st['lvl_last'] = s
                if collect_lvl: st['lvl'].append((rho, s // 2, j))
            newp = [[vu + t, ru, lu << t, ('M', s)] for t in range(j - 1)] + \
                   [[tD[0], tD[1], lD, ('D', s)]]
            A = (vu, ru, lu + 1)
        k = len(P)
        if k >= 2:
            P = P[2:]
        else:
            i += 2 - k; P = []
        P = newp + P
        s += 1
        if i != last_i:
            stall = s - last_move
            if stall > st['maxstall']: st['maxstall'] = stall
            last_i = i; last_move = s
        m = A[0]
        for p in P:
            if p[0] < m: m = p[0]
        d = i - m
        if d > st['maxdef']:
            st['maxdef'] = d; st['maxdef_at'] = (i, s)
            st['d_events'].append((d, i, s))
        if i > 0 and s / i > st['maxs_ov_i']:
            st['maxs_ov_i'] = s / i
    st['final'] = (i, s)
    return st

def exact_walker(N, collect_lvl=True):
    """Exact big-int walker (mirrors work_g6 F_walk, no per-step mass assert)."""
    A = (1, 1); P = []; i = 0; s = 0
    lvl = []
    while i <= N:
        ents = [(p[0], p[1], p[2]) for p in P[:2]]
        a = i
        while len(ents) < 2:
            ents.append((1 << a, 0, ('E', a))); a += 1
        (cb, lb, tb), (cc, lc, tc) = ents
        if (A[0] + A[1]) % 2 == 0:
            A = (A[0] + cb + cc, A[1] + lb + lc + 3); newp = []
        else:
            cx = A[0] + 2 * cb; lx = A[1] + 2 * lb + 3
            vc, vl = v2i(cx), v2i(lx)
            assert vl < vc and A[0] % 2 == 0 and A[1] % 2 == 1, (i, s)
            j = vl; u = (cx >> j, lx >> j)
            if tb[0] == 'E' and collect_lvl:
                lvl.append((tb[1], s // 2, j))
            newp = [(u[0] << t, u[1] << t, ('M', s)) for t in range(j - 1)] + \
                   [(cc + A[0] // 2, lc + (A[1] + 1) // 2, ('D', s))]
            A = (u[0], u[1] + 1)
        k = len(P)
        if k >= 2: P = P[2:]
        else: i += 2 - k; P = []
        P = newp + P; s += 1
    return lvl

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7
    XC = int(sys.argv[2]) if len(sys.argv) > 2 else 2 * 10 ** 5
    t0 = time.time()
    st = fast_walker(N)
    el = time.time() - t0
    i_fin, s_fin = st['final']
    print('fast walker to i=%d (%d steps, %d chains, %d level fires) [%.0fs]'
          % (i_fin, s_fin, st['chains'], st['level'], el))
    print('  max deficit i-min(v2 c) = %d at (i,s)=%s ; chain-value deficit max = %d at %s'
          % (st['maxdef'], st['maxdef_at'], st['maxdeft'], st['maxdeft_at']))
    print('  (M1p): maxdef=%d vs floor(log2 i)^2=%d -> %s'
          % (st['maxdef'], (i_fin.bit_length() - 1) ** 2, st['maxdef'] <= (i_fin.bit_length() - 1) ** 2))
    print('  (M2p): max s/i = %.4f -> %s' % (st['maxs_ov_i'], st['maxs_ov_i'] <= 1))
    print('  max stall = %d steps ; max level-fire gap = %d steps' % (st['maxstall'], st['maxlvlgap']))
    print('  deficit records (d, i, s):', st['d_events'])
    # cross-validate the (rho, k, j) stream on the prefix
    lfx = exact_walker(XC)
    n = len(lfx)
    assert st['lvl'][:n] == lfx, 'prefix mismatch between fast and exact walkers'
    print('cross-check OK: fast walker equals exact walker on all %d prefix level fires (i<=%d)'
          % (n, XC))
