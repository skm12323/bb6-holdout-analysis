"""Blind audit 19: independent bigint run of the formal pair map F (machine #1).

F reconstructed from PROOF_M/PROOF_EL/PROOF_RESCUE text only:
  state (A; P; i); originals E_a=(2^a,0); a step reads b,c = first two of P ++ [E_i,...].
  parity = (c_A+lam_A) mod 2.
  even: A' = A+b+c+(0,3), P' = rest.
  odd (chain): x = A+2b+(0,3), j=v2(lam_x), require v2(c_x)>j (S1), c_A even (S2);
       u = x/2^j, A' = u+(0,1), P' = [u<<a : a=0..j-2] + [c+(A+(0,1))/2] + rest.
Usage: python -B audit19.py NMAX
"""
import sys, math
from collections import deque


def v2(x):
    return (x & -x).bit_length() - 1


def run(NMAX):
    A = (1, 1); P = deque(); i = 0; s = 0
    tau = {}; typ = {}; hpar = {}; hlam = {}; eps = {}
    steps = []  # per step: (s, Pempty, i_before, odd, j, lam_x, |P| before)
    while i < NMAX:
        # gather b,c
        pe = len(P)
        need = 2 - min(pe, 2)
        if pe == 0:
            # reads E_i, E_{i+1}
            for n, t in ((i, 'a'), (i + 1, 'b')):
                tau[n] = s; typ[n] = t
            cr = [i, i + 1]
        elif pe == 1:
            tau[i] = s; typ[i] = 'c'; cr = [i]
        else:
            cr = []
        par = (A[0] + A[1]) & 1
        cA = v2(A[0]) if A[0] else None
        for n in cr:
            hpar[n] = par; hlam[n] = A[1]; eps[n] = n - cA
        if pe >= 2:
            b = P.popleft(); c = P.popleft()
        elif pe == 1:
            b = P.popleft(); c = (1 << i, 0); i += 1
        else:
            b = (1 << i, 0); c = (1 << (i + 1), 0); i += 2
        if par == 0:
            A = (A[0] + b[0] + c[0], A[1] + b[1] + c[1] + 3)
            steps.append((s, pe == 0, i, False, 0, 0, pe))
        else:
            assert A[0] % 2 == 0, ("S2", s)
            xc = A[0] + 2 * b[0]; xl = A[1] + 2 * b[1] + 3
            j = v2(xl)
            assert v2(xc) > j, ("S1", s)
            uc = xc >> j; ul = xl >> j
            D = (c[0] + (A[0] >> 1), c[1] + ((A[1] + 1) >> 1))
            new = [(uc << a, ul << a) for a in range(j - 1)] + [D]
            P.extendleft(reversed(new))
            A = (uc, ul + 1)
            steps.append((s, pe == 0, i, True, j, xl, pe))
        s += 1
        # mass identity check at sampled steps
        if s % 5000 == 0:
            assert A[0] + sum(p[0] for p in P) == 1 << i
            assert A[1] + sum(p[1] for p in P) == 3 * s + 1
    return tau, typ, hpar, hlam, eps, steps, i


def Kof(g):
    return math.ceil(math.log2(6 * g * g + 6))


def main():
    NMAX = int(sys.argv[1])
    tau, typ, hpar, hlam, eps, steps, ifin = run(NMAX)
    S = len(steps)
    print("steps", S, "pointer", ifin)
    nmax = max(n for n in tau if n < ifin)
    print("max tau/n (n>=1):", max(tau[n] / n for n in range(1, nmax)))
    print("C1 tau<=n^2 viol:", sum(1 for n in range(1, nmax) if tau[n] > n * n))
    print("eps values:", sorted(set(eps[n] for n in range(nmax))))
    print("odd type-a n<40:", [n for n in range(40) if typ[n] == 'a' and hpar[n]])
    print("X(4),X(5),X(16):", [(n, typ[n], hpar[n], hlam[n], tau[n], eps[n]) for n in (4, 5, 16)])
    # epochs
    epochs = []
    s = 0
    while s < S:
        st = steps[s]
        assert st[1], ("epoch start not P=empty", s)
        rho = st[2] - 2  # pointer before reading
        if not st[3]:
            s += 1; continue
        chains = []  # (s_t, j_t, lam_x)
        cur = s
        complete = True
        while True:
            _, _, _, odd, j, xl, _ = steps[cur]
            chains.append((cur, j, xl))
            n = j - 1
            nxt = cur + 1 + tau[n]
            if nxt >= S:
                complete = False; break
            if steps[nxt][3]:
                # must be a return reading D_t: |P| in {1,2}
                assert steps[nxt][6] == (1 if typ[n] == 'a' else 2), ("ret", nxt)
                assert hpar[n] == 1
                cur = nxt
            else:
                assert hpar[n] == 0
                end = nxt + 1
                break
        if not complete:
            break
        assert end >= S or steps[end][1], ("epoch end not P=empty", end)
        epochs.append((rho, chains))
        s = end
    print("complete fire epochs:", len(epochs))
    from collections import Counter
    rdist = Counter(len(c) - 1 for _, c in epochs)
    print("r distribution:", dict(sorted(rdist.items())))
    # checks
    npos = 0; posbad = 0; nsame = 0; samebad = 0; nph = 0; phbad = 0; coll = 0
    viol_b = 0; nonvac_b = 0; viol_after2 = 0; viol_count = 0; viol_r = 0; viol_jg = 0
    maxm_ratio = 0; maxm = 0; mrec = None; Kset = Counter()
    for rho, ch in epochs:
        g = 2 * math.log2(rho) + 4
        K = Kof(g); Kset[K] += 1
        js = [c[1] for c in ch]
        if max(js) > g: viol_jg += 1
        types = [typ[j - 1] for j in js[:-1]]  # return type after chain t (odd)
        for t in range(len(ch) - 2):
            if types[t] == 'a' and types[t + 1] == 'a':
                npos += 1
                x0, x1, x2 = ch[t][2], ch[t + 1][2], ch[t + 2][2]
                k = tau[js[t] - 1] // 2; l = tau[js[t + 1] - 1] // 2
                Th = 3 * ch[t][0] + 5
                ok = (x2 == (x0 + x1) // 2 + 6 * (k + l + 1) and (x0 + x1) % 2 == 0
                      and x1 == 2 * Th + 6 * k - x0 // 2 and 3 * ch[t + 1][0] + 5 == Th + 3 + 6 * k)
                if not ok: posbad += 1
                if (k - l) % 2 == 0:
                    nsame += 1
                    if js[t + 2] != 1: samebad += 1
                elif js[t] != js[t + 1]:
                    p = min(js[t], js[t + 1]) - 1; h = 1 + v2(k + l + 1)
                    if p != h:
                        nph += 1
                        if js[t + 2] != min(p, h): phbad += 1
                    else:
                        coll += 1
        # (b) no three consecutive > K; after two large, next < K
        run_ = 0
        for t, j in enumerate(js):
            if j > K:
                run_ += 1
                if run_ >= 3: viol_b += 1
                if run_ == 2: nonvac_b += 1
            else:
                if run_ >= 2 and not j < K: viol_after2 += 1
                run_ = 0
        m = sum(1 for j in js if j <= K)
        Nc = len(js)
        if Nc > 3 * m + 2: viol_count += 1
        if Nc - 1 > 3 * m + 1: viol_r += 1
        if m > maxm: maxm = m; mrec = (rho, js, K)
        if m / (g * g) > maxm_ratio: maxm_ratio = m / (g * g)
    print("(a) two-a identities:", npos, "bad:", posbad,
          "| same-parity cases:", nsame, "bad:", samebad,
          "| p!=h cases:", nph, "bad:", phbad, "| p=h collisions:", coll)
    print("(b) K values:", dict(sorted(Kset.items())), "3-run viol:", viol_b,
          "2-runs (nonvacuous):", nonvac_b, "after-2 not <K:", viol_after2, "j>g:", viol_jg)
    print("(c) N<=3m+2 viol:", viol_count, " r<=3m+1 viol:", viol_r)
    print("(d) max m:", maxm, "at", mrec, " max m/g^2:", maxm_ratio)
    nonc = sum(1 for rho, ch in epochs for c in ch if c[1] > Kof(2*math.log2(rho)+4))
    na = sum(1 for rho, ch in epochs for c in ch[:-1] if typ[c[1]-1] == 'a')
    nbc = sum(1 for rho, ch in epochs for c in ch[:-1] if typ[c[1]-1] != 'a')
    print("noncore chains:", nonc, " odd a-returns:", na, " odd b/c-returns:", nbc)
    print("max j over chains:", max(c[1] for _, ch in epochs for c in ch))
    return tau, typ, hpar, steps


def fstep(A, P, i):
    pe = len(P)
    if pe >= 2: bb = P.popleft(); cc = P.popleft()
    elif pe == 1: bb = P.popleft(); cc = (1 << i, 0); i += 1
    else: bb = (1 << i, 0); cc = (1 << (i + 1), 0); i += 2
    if (A[0] + A[1]) & 1 == 0:
        return (A[0] + bb[0] + cc[0], A[1] + bb[1] + cc[1] + 3), i, None
    assert A[0] % 2 == 0
    xc = A[0] + 2 * bb[0]; xl = A[1] + 2 * bb[1] + 3
    j = v2(xl); sig = v2(xc); assert sig > j, "S1"
    uc, ul = xc >> j, xl >> j
    D = (cc[0] + (A[0] >> 1), cc[1] + ((A[1] + 1) >> 1))
    P.extendleft(reversed([(uc << q, ul << q) for q in range(j - 1)] + [D]))
    return (uc, ul + 1), i, (j, sig, xl)


def synthetic(seq=(17, 5, 17, 17, 1), I=300, cexp=200):
    """Mass-compatible top-level state (A;[D];I), c_A=2^cexp; evolve full bigint F
    until P empty; return top-level chain parameters."""
    tau = run(64)[0]
    hits = []; tried = 0
    for a in range(1, 4001, 2):
        for b in range(1, 64):
            Th = (b << 17) - 66 - (a << 15)
            if Th % 3 != 2 or Th < 5: continue
            s0 = (Th - 5) // 3; xl = a << 17
            lamA = 6 * s0 + 5 - xl; lamD = 3 * s0 + 1 - lamA
            if lamA <= 0 or lamD < 0: continue   # keep entries nonnegative
            tried += 1
            cA = 1 << cexp
            A = (cA, lamA); P = deque([((1 << I) - cA, lamD)]); i = I
            chain = {}; st = 0
            while len(P) > 0:
                A, i, ch = fstep(A, P, i)
                if ch: chain[st] = ch
                st += 1
                assert A[0] + sum(p[0] for p in P) == 1 << i
                assert A[1] + sum(p[1] for p in P) == 3 * (s0 + st) + 1
            top = []; t = 0
            while t in chain:
                top.append(chain[t][:2]); t = t + 1 + tau[chain[t][0] - 1]
            if tuple(x[0] for x in top) == seq:
                hits.append((a, b, s0, top, st))
    return tried, hits


if __name__ == "__main__" and len(sys.argv) > 2:
    tried, hits = synthetic()
    print("synthetic states tried:", tried, "hits for 17,5,17,17,1:", len(hits))
    for h in hits[:3]: print(h)
    print("K(17)=", Kof(17))
    sys.exit()
if __name__ == "__main__":
    main()
