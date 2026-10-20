"""verify_R1_src.py -- instrumented canonical lambda-walk: exact source chain of every type-c crossing.

Copy of work_global_ext/route_c/fdata.py::lam_walk with two additions:
  * retmap[return step] = (j_chain, u_chain)  for every TOP-LEVEL odd step (the chain it starts);
  * every recorded type-c crossing X(n) at step s is tagged with the source chain
    (the chain whose a-return is that step), giving n' = j_chain-1 and lambda_u = u_chain.
Then the following EXACT identities (NOTES Section 2, Lemma S) are checked for every type-c crossing:
  lambda_A[n]      = 2^{n'} * lambda_u + 3*tau[n'] + 1
  lambda'_W(n)     = A - 2^{n'} * lambda_u,   A := 6*tau[n] + 4 - 3*tau[n']
(the second is equivalent to the first by the mass identity).
Saves a compact source map (n' and lambda_u per type-c crossing) in the scratch dir.

Usage: python -B verify_R1_src.py <N> [out.pkl]
"""
import sys, os, json, time, pickle
from array import array

def v2(x): return (x & -x).bit_length() - 1

def lam_walk_src(N, check=True):
    typ = bytearray(b'?' * N); tau = array('q', [-1]) * N; eps = array('h', [0]) * N
    odd = bytearray(N); lY = array('q', [0]) * N; lA = array('q', [0]) * N
    la = 1; S = []; i = 0; s = 0; calls = []; sig_last = None; jl = None; first = True
    seen = -1
    retmap = {}
    C_n = array('i'); C_np = array('i'); C_lu = array('q'); C_A = array('q')
    stat = dict(c_count=0, src_found=0, src_missing=0, idA=0, idW=0, bad=0,
                top_chains=0, retmap_left=0)
    while seen < N - 1:
        while calls and calls[-1] < s:
            calls.pop()
        k = len(S)
        if k >= 2: lb = S[-1]; lc = S[-2]; reads = ()
        elif k == 1: lb = S[-1]; lc = 0; reads = (i,)
        else: lb = lc = 0; reads = (i, i + 1)
        par = (la + (1 if first else 0)) & 1
        for n in reads:
            if n > seen and n < N:
                seen = n
                assert not calls
                tau[n] = s; odd[n] = par; lA[n] = la
                if k == 0 and i == n:
                    typ[n] = 97; eps[n] = 0
                elif k == 0:
                    typ[n] = 98; eps[n] = 1
                else:
                    typ[n] = 99; eps[n] = n - (sig_last - 1); lY[n] = lb
                    if par:
                        stat['c_count'] += 1
                    sm = retmap.pop(s, None) if par else None
                    if sm is None:
                        stat['src_missing'] += 1
                    else:
                        jc, uc = sm
                        np_ = jc - 1
                        tn = tau[np_] if 0 <= np_ < N else -1
                        stat['src_found'] += 1
                        R = la - 3 * tn - 1 if tn >= 0 else -1
                        if R > 0 and v2(R) == np_ and (R >> np_) == uc:
                            stat['idA'] += 1
                        lamW = lA[n] + 2 * lb + 3
                        A = (6 * s + 4 - 3 * tn) if tn >= 0 else 0
                        if R > 0 and A - R == lamW:
                            stat['idW'] += 1
                        else:
                            stat['bad'] += 1
                        lamW = lA[n] + 2 * lb + 3
                        if par:
                            C_n.append(n); C_np.append(np_); C_lu.append(uc); C_A.append(A)
                            stat['om'] = stat.get('om', {})
                            o = v2(lamW)
                            stat['om'][o] = stat['om'].get(o, 0) + 1
                            stat['src_hist'] = stat.get('src_hist', {})
                            stat['src_hist'][np_] = stat['src_hist'].get(np_, 0) + 1
                            if A > 0 and A % (1 << np_) == 0:
                                stat['divA'] = stat.get('divA', 0) + 1
                            if A > 0 and v2(A) == np_:
                                stat['vA_eq'] = stat.get('vA_eq', 0) + 1
                            stat['A_max'] = max(stat.get('A_max', 0), A)
                            stat['omA_max'] = max(stat.get('omA_max', 0), v2(A) if A else -1)
        if par == 0:
            la = la + lb + lc + 3; push = None
        else:
            lx = la + 2 * lb + 3; j = v2(lx); u = lx >> j
            top = not calls
            if top:
                if k == 0: sg = i
                else: sg = sig_last - 1 - eps[jl - 1]
                if check: assert j < sg, ('S1 fails', i, s, j, sg)
                sig_last = sg; jl = j
            T = tau[j - 1]; assert T >= 0
            push = (u, j, lc + (la + 1) // 2); la = u + 1
            if T > 0:
                calls.append(s + T)
            if top:
                # Lemma 2.3: the return step of this chain is s + 1 + tau(j-1)
                retmap[s + T + 1] = (j, u)
                stat['top_chains'] += 1
        if k >= 2: del S[-2:]
        else: i += 2 - k; S.clear()
        if push:
            u, j, D = push; S.append(D)
            for t in range(j - 2, -1, -1): S.append(u << t)
        s += 1; first = False
    stat['retmap_left'] = len(retmap)
    return dict(typ=bytes(typ), tau=tau, eps=eps, odd=bytes(odd), lY=lY, lA=lA, N=N), \
           (C_n, C_np, C_lu, C_A), stat

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10 ** 7
    outp = sys.argv[2] if len(sys.argv) > 2 else r'D:\math_cc_astra\r1r2\agent_R1\src_%d.pkl' % N
    t0 = time.time()
    D, (Cn, Cnp, Clu, CA), stat = lam_walk_src(N)
    el = round(time.time() - t0, 1)
    print('walk', N, el, 's', stat, flush=True)
    with open(outp, 'wb') as f:
        pickle.dump(dict(N=N, Cn=Cn, Cnp=Cnp, Clu=Clu, CA=CA, stat=stat, seconds=el),
                    f, protocol=pickle.HIGHEST_PROTOCOL)
    print('wrote', outp, flush=True)

if __name__ == '__main__':
    main()
