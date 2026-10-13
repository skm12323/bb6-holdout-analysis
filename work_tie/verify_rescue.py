"""Exact local checks and finite entry certificate for PROOF_RESCUE.md.

Only standard library. Existing verification modules are imported read-only.
Run: python -B work_tie/verify_rescue.py
"""
from collections import Counter
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_m'))
sys.path.insert(0, str(ROOT / 'work_el'))
import verify_m as vm
import verify_el as ve


def exact_local(z, u, sigma):
    """Synthetic mass-compatible top-level state, not claimed reachable in F.

    Theta=2^17*z-2, lambda(run base)=u, v2(c_x)=sigma.
    Integers: z=2 mod 3, z<=u<2z, u odd, sigma>=18.
    Run full bigint F steps until the epoch closes; no compressed returns.
    """
    assert z % 3 == 2 and z <= u < 2*z and u % 2 and sigma >= 18
    s = ((1 << 17)*z-7)//3
    A = (1 << sigma, (1 << 17)*(2*z-u)-9)
    P = [(1 << sigma, (1 << 17)*(u-z)+3)]
    i = sigma+1
    initial_s = s
    all_js = []
    top_js = []
    top_times = {0, 13, 16, 19}
    while True:
        assert sum(c for c, _ in [A]+P) == 1 << i
        assert sum(l for _, l in [A]+P) == 3*s+1
        if not P:
            assert s-initial_s == 21, (s-initial_s, all_js, top_js)
            break
        E = P[:2]
        ni = i
        while len(E) < 2:
            E.append((1 << ni, 0))
            ni += 1
        b, c = E
        tail = P[2:]
        elapsed = s-initial_s
        if sum(A) % 2 == 0:
            A = (A[0]+b[0]+c[0], A[1]+b[1]+c[1]+3)
            P = tail
        else:
            cx, lx = A[0]+2*b[0], A[1]+2*b[1]+3
            j = vm.v2(lx)
            assert j < vm.v2(cx) and A[0] % 2 == 0
            all_js.append(j)
            if elapsed in top_times:
                top_js.append(j)
            base = (cx >> j, lx >> j)
            D = (c[0]+A[0]//2, c[1]+(A[1]+1)//2)
            A = (base[0], base[1]+1)
            P = [(base[0] << t, base[1] << t) for t in range(j-1)]+[D]+tail
        i = ni
        s += 1
        assert s-initial_s <= 21
    assert top_js == [17, 5, 6, 1]
    return len(all_js)


def local_checks():
    X = vm.Xdata(18, SMALL=18)
    assert X[16] == ('a', (65536, 37), None, 0)
    assert X[4] == ('a', (16, 7), None, 0)
    assert X[5] == ('b', (16, 7), (16, 0), 1)
    assert X[0] == ('a', (1, 1), None, 0)
    count = 0
    for z in list(range(2, 302, 3))+[3*(1 << 100)+2]:
        us = {u for u in (z, z+1, 2*z-1, (3*z)//2) if z <= u < 2*z and u % 2}
        for u in us:
            theta = (1 << 17)*z-2
            x1 = 2*(theta+18-(u << 15))
            assert vm.v2(x1) == 5
            u1 = x1 >> 5
            assert u1 == 1+(1 << 11)*(4*z-u)
            x2 = 2*(theta+39+3-8*u1)
            assert x2 == 64*(1+512*(4*z+u))
            assert vm.v2(x2) == 6
            for sigma in (18, 19, 32, 128):
                exact_local(z, u, sigma)
                count += 1
    print('LOCAL:', count, 'full bigint synthetic epochs, 21 steps each; all safe', flush=True)
    return count


def certificate(N=10**6):
    Xt, typ, par, chain, stats, steps = ve.real_walk(N)
    run = ve.make_run(Xt, typ, par, chain)
    A0 = set()
    for j in range(2, N):
        out, failure = run(j, 1)
        assert failure is None and len(out) <= 2
        A0.update((a,b) for a,b,k in out if k == 'a')
    A1 = set()
    level1_count = 0
    for th in (0,2):
        for j in range(1,N):
            out, failure = run(j, th)
            assert failure is None and len(out) <= 3
            A1.update((a,b) for a,b,k in out if k == 'a')
            level1_count += 1
    for j, th in sorted(A0):
        out, failure = run(j, th-1)
        assert failure is None and len(out) <= 3
        A1.update((a,b) for a,b,k in out if k == 'a')
        level1_count += 1
    print('TABLE: exact walk steps', steps, 'A0', len(A0), 'A1', len(A1), flush=True)

    # Complete level-2 coverage, including first route-c entries A1-1.
    # Existing E6 is informational; do not assume its entry set is sufficient.
    specific = {(j,th-1) for j,th in A0 | A1}
    specific |= {(j,th+shift) for j,th in A0 for shift in (-2,0)}
    distribution = Counter()
    rescues = []
    def check(j, th, family):
        out, failure = run(j, th)
        if failure is None:
            distribution[len(out)] += 1
            return
        path = [(j,th)] + [(a,b) for a,b,_ in out]
        assert failure == ('TIE',5,5), (j,th,out,failure)
        assert path[-2:] == [(17,-2),(5,5)], path
        # Macro theorem gives TWO further chains after j=5: 6,1, then even return.
        distribution[len(out)+2] += 1
        rescues.append(dict(entry=[j,th], family=family, path=path, repaired_j=[6,1]))
    for th in (-1,0,1,2,3):
        for j in range(1,N):
            check(j,th,'any')
    for j,th in sorted(specific):
        check(j,th,'specific')
    assert max(distribution) <= 8
    result = dict(N=N, walk_steps=steps, A0=sorted(A0), A1=sorted(A1),
                  level1_count=level1_count, specific_entries=sorted(specific),
                  checked_entries=sum(distribution.values()),
                  continuation_distribution=dict(sorted(distribution.items())),
                  max_further_chains=max(distribution), rescues=rescues)
    print(json.dumps({k:v for k,v in result.items() if k not in ('A0','A1','specific_entries')}, indent=2), flush=True)
    return result


if __name__ == '__main__':
    result = {'local_cases': local_checks(), 'certificate': certificate()}
    output = Path(__file__).with_name('certificate.json')
    output.write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
