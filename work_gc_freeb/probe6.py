# probe6: verify reviewer's quantitative claims before patching
import sys
sys.path.insert(0, 'work_gc_freeb')
sys.path.insert(0, 'work_claude_cycle')
from fb import Rows, det_walk, fb4, Pc
from cyc import Cal, v2
from collections import Counter

cal = Cal(); rows = Rows(cal)

# (A) m=j two-step pairs: X(j-1) type a => E = 2k_j+1 odd => c1=1 => END
cnt = Counter()
for j in range(5, 400):
    k = cal.k(j)
    if k is None: continue
    m = j
    r = rows(m-1)
    if not r['odd']: continue
    if r['kind'] == 'a':
        E = k + 1 + r['tau']//2
        cnt['a_E_v2=%d' % v2(E)] += 1
    else:
        cnt['bc_m_eq_j'] += 1
print('(A) m=j pairs by first-step type / v2(E):', dict(cnt))

# (B) m=j+1 pairs: how many, types, outcomes
cnt2 = Counter()
for j in range(5, 400):
    k = cal.k(j)
    if k is None: continue
    m = j + 1
    r = rows(m-1)
    if not r['odd']: continue
    tr, st, _ = det_walk(rows, j, k, m, max_steps=m+3)
    cnt2[(r['kind'], st)] += 1
print('(B) m=j+1 pairs (kind, detstatus):', dict(cnt2))

# (C) P3 population: determined landing + a-step at c1, with/without c1<=j-2 filter
allc = le = 0; super_esc = 0
for j in range(5, 400):
    k = cal.k(j)
    if k is None: continue
    for m in range(j, 5000):
        r = rows(m-1)
        if not r['odd']: continue
        d4 = fb4(rows, j, k, m)
        if d4 and not d4.get('no_astep'):
            allc += 1
            if d4['c1'] <= j - 2: le += 1
            elif r['kind'] != 'a' and d4['c1'] >= j: super_esc += 1
print('(C) P3 population: all=%d, c1<=j-2: %d, bc-super-escape c1>=j: %d' % (allc, le, super_esc))

# (D) first odd type-c crossing with omega=5 and an a-step at c1: scan m
found = []
for n in range(5000, 12000):
    r = rows(n)
    if r['odd'] and r['kind'] == 'c':
        c1 = r['omega']
        r1 = rows(c1-1)
        if r1['odd'] and r1['kind'] == 'a':
            found.append((n+1, c1, r['eps']))
            if len(found) >= 8: break
print('(D) type-c candidates (m, omega, eps):', found)

# (E) j=24 type-b congruence class: 9*tau = -140 mod 2^22, c1=omega=5 family:
# search tau-labels kk = tau*/2 + i*2^21 for realized type-b crossings
j = 24; k = cal.k(j)
M = 1 << 21
tstar = (-(12*k + 32) * pow(9, -1, 1 << 22))  # tau* mod 2^22 (tau = 2 kk)
assert (9*tstar + 12*k + 32) % (1 << 22) == 0
kk0 = tstar // 2 if tstar % 2 == 0 else None
print('(E) tau* =', tstar, 'even:', tstar % 2 == 0)
hits = 0
if kk0 is not None:
    for i in range(3000):
        kk = kk0 + i * M
        try:
            f = cal.C.preceding_fire_by_time(2*kk)
        except ValueError:
            break
        if f['k'] != kk: continue
        m = f['pointer'] + 2
        row = rows(m-1)
        if row['kind'] == 'b' and row['tau'] == 2*kk:
            hits += 1
            print('   hit i=%d m=%d omega=%d' % (i, m, row['omega']))
            if hits >= 3: break
print('(E) j=24 b-class realized type-b crossings (i<3000):', hits)
