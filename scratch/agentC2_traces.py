"""agentC2 -- part 1b: detailed interlude traces to identify the general-k
endgame structure. For each k, print every fire (D, i, kfire, parent?) and the
number of even steps between fires; correlate with the universal fire
positions (t_n, i_n) and the last-child-fire parameters (N, t_N, i_N, k_N, g).
"""
import sys
sys.path.insert(0, r"D:\math_cc\scratch")
from agentC2_interlude import interlude, v2

table = {}
for _k in range(1, 65):
    _o = interlude(_k)
    table[_k] = (_o['dt'], _o['di'])


def trace(k):
    out = interlude(k)
    return out


# universal sequence from the table (only trust it where table is exact: k<=64)
def univ_seq(Tmax=100000):
    seq = [(2, 4)]
    t, i = 2, 4
    while t <= Tmax:
        k = v2(3 * t + 4)
        dt, di = table[k]
        t, i = t + dt, i + di
        seq.append((t, i))
        if k > 64:
            break
    return seq


U = univ_seq()
print("universal (t,i) first 40:", U[:40])
print()

def classify(k):
    out = interlude(k)
    fires = out['fires']
    # child fires: those with D == 3*tn+1 and i == in for universal (tn, in) with in == v2(e1)
    info = []
    for (D, ie, kf, isp, e1) in fires:
        hit = None
        for n, (tn, in_) in enumerate(U):
            if in_ == ie and D == 3 * tn + 1:
                hit = n
                break
        info.append((D, ie, kf, isp, hit))
    # last universal fire among non-parent fires
    child = [x for x in info if not x[3]]
    lastN = None
    for x in child:
        if x[4] is not None:
            lastN = x[4]
    return out, info, lastN


print("%-4s %-22s %-30s %s" % ("k", "(dt,di,loss)", "fires (D,i,kf,par,univ#)", "N,g,t_N,i_N,k_N"))
for k in list(range(5, 31)) + [32, 37, 46, 51, 64]:
    out, info, lastN = classify(k)
    if lastN is not None:
        tN, iN = U[lastN]
        kN = v2(3 * tN + 4)
        g = k - 2 - iN
        ng = "N=%d g=%d (tN=%d,iN=%d,kN=%d)" % (lastN, g, tN, iN, kN)
    else:
        ng = "N=none"
    fs = " ".join("%d/%d/%d%s%s" % (D, ie, kf, "P" if p else "", ("u%d" % h) if h is not None else "")
                  for (D, ie, kf, p, h) in info)
    print("%-4d %-22s %-60s %s" % (k, str((out['dt'], out['di'], out['dt'] - out['di'])), fs, ng))
