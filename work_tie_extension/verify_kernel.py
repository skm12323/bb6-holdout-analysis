"""Compare the residue engine against exact pair-crossing arithmetic.

Small crossing coefficients are obtained from the full bigint F implementation;
the engine's second lambda-only pass is not used as the arithmetic oracle.
These are checks of the abstract transition implementation, not orbit claims.
"""
import json
import random
from pathlib import Path
import sys
import explore_layers as ex
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'work_m'))
import verify_m as vm

N = 2048
Xt, typ, par, chain, _, _ = ex.ve.real_walk(N)
real = ex.sigma_walk(N, chain)
X = vm.Xdata(N, SMALL=N)
ext = ex.make_ext(Xt, typ, par, real)
crossings = 0
for n in range(N):
    kind, head, Y, eps = X[n]
    assert kind == typ[n] and (sum(head) & 1) == par[n]
    assert head[1]+(Y[1] if Y else 0) == 3*Xt[n]+1
    if kind in ('b','c') and par[n]:
        cx = head[0]+2*Y[0]
        lx = head[1]+2*Y[1]+3
        j = vm.v2(lx)
        assert (j, lx >> j, vm.v2(cx)) == real[Xt[n]]
        assert vm.v2(cx) == n-eps
        crossings += 1


def oracle(j, theta, u, h=100):
    out = []
    for _ in range(80):
        if j-1 not in X:
            return None
        kind, head, Y, eps = X[j-1]
        if sum(head) % 2 == 0:
            return out
        tau = Xt[j-1]
        oldj = j
        if kind == 'a':
            x = 2*theta+3*tau-(u << (j-1))
        else:
            # Direct M_u image of the full-pair crossing x; no margin shortcut.
            x = u*(head[0]+2*Y[0])+head[1]+2*Y[1]+3
        if x <= 0:
            return None
        j = vm.v2(x)
        u = x >> j
        theta += 3*tau+3
        h += oldj-j-1-eps
        out.append((j,theta,u,h))
    return None


rng = random.Random(20261013)
checked = non_descents = lifted = 0
cases = [(17,-2,17,1,1), (5,36,64,1,11), (6,45,64,1,9), (5,37,64,1,11)]
cases += [(rng.randrange(12,500),rng.randrange(-3,6),64,1,1) for _ in range(1000)]
for j,T,M,ur,m in cases:
    M = max(M,j)
    leaves = ext(j,T,M,ur,m,h=100)
    assert all(L['res'] == 'END' and L['hmin'] > 0 for L in leaves), (j,T,leaves[:1])
    for z in (1,3,11):
        theta = T+(z << M)
        u = ur+(rng.randrange(4) << m)
        out = oracle(j,theta,u)
        if out is None:
            continue
        def matches(L):
            if len(L['path']) != len(out):
                return False
            for (a,t,p,b,q,h,kd),(ja,ta,ua,ha) in zip(L['path'],out):
                if a != ja or h != ha or (ta-t) % (1 << p) or (ua-b) % (1 << q):
                    return False
            return True
        assert any(matches(L) for L in leaves), (j,T,out,leaves)
        old = j
        for a,_,_,_ in out:
            non_descents += a >= old
            old = a
        checked += 1
        lifted += M > j
result = dict(exact_crossing_time_checks=N, exact_crossing_checks=crossings, concrete_lift_checks=checked,
              non_descending_transitions=non_descents, higher_precision_entries=lifted,
              result='PASS', seed=20261013)
Path(__file__).with_name('kernel_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
