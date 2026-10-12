"""agentG_mine.py -- Task 1: mine fire data.

A) Orbit from (3), 4e6 top steps: every fire's (n, fam, t, k, Delta, i, D).
   - Delta multiset; Delta as function of (fam, k);
   - exact law check k == v2(3t+4+Delta) at integral-t fires (integers);
   - no-deep-tie check v2(x_res) == k;
   - room stats i - t >= 2; D % 3 == 1 at R/T fires;
   - determinism scan: smallest m with (t mod 2^m, Delta) -> k well-defined.
B) Excursions E(1,v), v = 1..2000: same aggregates + per-v max k, ell.
   Determinism scan with context flags.
Outputs text report to agentG_mine_out.txt.
"""
import sys, time
from collections import Counter, defaultdict
sys.path.insert(0, r"D:\math_cc\scratch")
from agentG_lib import *

out = []
def P(*a):
    s = " ".join(str(x) for x in a)
    out.append(s)
    print(s)

t0 = time.time()

# ---------------- A) orbit ----------------
NSTEPS = 4 * 10**6
head, ents = 3, []
orbit_fires = []
excursions = []   # (v, w, n_start)
cur_exc = None
for n in range(NSTEPS):
    (head, ents), f = top_step_annot(head, ents)
    if f is not None:
        if f.get('HALT'):
            P("!!! HALT at n =", n, "x =", f['x']); break
        f['n'] = n
        f['fam'] = fire_family(f)
        orbit_fires.append(f)
        if f['fam'] == 'X':
            cur_exc = {'v': f['k'], 'w': f['q'], 'n0': n, 'nf': 0}
        elif cur_exc is not None:
            cur_exc['nf'] += 1
    else:
        if not ents and cur_exc is not None:
            excursions.append(cur_exc)
            cur_exc = None
    if n % 1000000 == 0:
        s = head + sum(v for (r, v) in ents)
        assert s == 3 * (n + 1) + 3, (n, s)
P("orbit: %d steps, %d fires, %d excursions, time %.1fs" % (
    NSTEPS, len(orbit_fires), len(excursions), time.time() - t0))

famc = Counter(f['fam'] for f in orbit_fires)
P("orbit fire families:", dict(famc))

# Delta multiset (integral-t fires)
dc = Counter((f['fam'], f['Delta']) for f in orbit_fires if f['ok_t'])
P("orbit (fam, Delta) counts:", dict(dc))
nokt = [f for f in orbit_fires if not f['ok_t']]
P("orbit non-integral-t fires:", len(nokt),
  "fams:", Counter(f['fam'] for f in nokt))

# exact law: k == v2(3t+4+Delta) as INTEGERS
bad = 0; badtie = 0
for f in orbit_fires:
    if f['ok_t']:
        N = 3 * f['t'] + 4 + f['Delta']
        if N <= 0 or v2(N) != f['k']:
            bad += 1
    if f['fam'] != 'X':
        if f['x_res'] <= 0 or v2(f['x_res']) != f['k']:
            badtie += 1
P("law violations k==v2(3t+4+Delta):", bad, " deep-tie violations v2(x_res)==k:", badtie)

# D mod 3 at R/T/S64 fires; room at R/T fires
dmod = Counter((f['fam'], (f['D'] - 1) % 3) for f in orbit_fires if f['fam'] != 'X')
P("(fam, (D-1)%3):", dict(dmod))
rooms = [(f['i'] - f['t'], f['n']) for f in orbit_fires if f['fam'] in ('R', 'T')]
P("room i-t: min =", min(r for r, n in rooms), " max =", max(r for r, n in rooms))
P("k distribution (orbit, R/T/S64 only):", dict(sorted(Counter(
    f['k'] for f in orbit_fires if f['fam'] != 'X').items())))
P("max k on orbit R/T:", max(f['k'] for f in orbit_fires if f['fam'] in ('R', 'T')))
P("max excursion v on orbit:", max(e['v'] for e in excursions))
P("min q on orbit (non-X):", min(f['q'] for f in orbit_fires if f['fam'] != 'X'))
P("ell check: sum nf per excursion vs ell: first 5:", [
    (e['v'], e['nf']) for e in excursions[:5]])

# determinism scan on orbit: key (t mod 2^m, Delta) -> k
def det_scan(fires, label, extra_key=None, mmax=20):
    for m in range(1, mmax + 1):
        tab = {}
        conflict = 0
        for f in fires:
            if not f['ok_t']:
                continue
            key = (f['t'] % (1 << m), f['Delta'])
            if extra_key is not None:
                key = key + extra_key(f)
            kk = (f['k'], f['fam'] in ('T',))
            if key in tab and tab[key] != kk:
                conflict += 1
            tab[key] = kk
        if conflict == 0:
            P(label, ": smallest m with (t mod 2^m, Delta) -> (k,isT) well-defined:", m,
              " (distinct keys: %d)" % len(tab))
            return m
    P(label, ": NO m <= %d works" % mmax)
    return None

det_scan(orbit_fires, "orbit")

# Delta update rule: Delta_{next} - Delta_{prev} as function of (fam)
trans = Counter()
prev = None
for f in orbit_fires:
    if prev is not None and f['ok_t'] and prev['ok_t']:
        trans[(prev['fam'], f['fam'], f['Delta'] - prev['Delta'])] += 1
    prev = f
P("orbit Delta transitions (prevfam, fam, dDelta):", dict(trans))

# fires per family with (t, i, k) top rows
byfam = defaultdict(Counter)
for f in orbit_fires:
    byfam[f['fam']][(f['t'], f['i'], f['k'])] += 1
for fam in ['R', 'T', 'S64', 'S63', 'X']:
    if fam in byfam:
        rows = sorted(byfam[fam].items())[:14]
        P("orbit %s (t,i,k) top:" % fam, rows)

# ---------------- B) excursions ----------------
t0 = time.time()
VMAX = 2000
exf_all = []
maxk_by_v = {}
ell_by_v = {}
for v in range(1, VMAX + 1):
    fs, ell, eh, hal = run_excursion(1, v)
    assert not hal
    for f in fs:
        f['v'] = v
    exf_all.extend(fs)
    maxk_by_v[v] = max((f['k'] for f in fs), default=0)
    ell_by_v[v] = ell
P("excursions v<=2000: %d fires, time %.1fs" % (len(exf_all), time.time() - t0))

dc2 = Counter((f['fam'], f['Delta']) for f in exf_all if f['ok_t'])
P("excursion (fam, Delta) counts:", dict(dc2))
P("excursion non-integral-t fams:", dict(Counter(f['fam'] for f in exf_all if not f['ok_t'])))
bad = sum(1 for f in exf_all if f['ok_t'] and (
    3 * f['t'] + 4 + f['Delta'] <= 0 or v2(3 * f['t'] + 4 + f['Delta']) != f['k']))
badtie = sum(1 for f in exf_all if f['fam'] != 'X' and f['x_res'] > 0
             and v2(f['x_res']) != f['k'])
P("excursion law violations:", bad, " deep-tie violations:", badtie)
rooms2 = [f['i'] - f['t'] for f in exf_all if f['fam'] in ('R', 'T')]
# safety condition k < i (valuation gap) on all non-X fires
unsafe = [f for f in exf_all if f['fam'] != 'X' and not f['k'] < f['i']]
P("excursion fires with k >= i (valuation-gap violation):", len(unsafe))
P("excursion room i-t: min =", min(rooms2), "max =", max(rooms2))
P("excursion k distribution:", dict(sorted(Counter(f['k'] for f in exf_all).items())))
P("max k over v<=2000:", max(f['k'] for f in exf_all),
  " at v =", max(maxk_by_v, key=lambda v: maxk_by_v[v]))
# max k vs v growth
P("maxk(v) at v = 100,200,...,2000:", [(v, maxk_by_v[v]) for v in range(100, 2001, 100)])
det_scan(exf_all, "excursions")
# with boundary context: does adding (v - i) clipped help separate T from R at same t?
det_scan(exf_all, "excursions+ctx", extra_key=lambda f: (f['fam'],), mmax=20)

# S63 deep fires: their D, i, k values
deep = [f for f in exf_all if f['fam'] == 'S63']
P("S63 deep fires: %d; (i,k) dist:" % len(deep),
  dict(Counter((f['i'], f['k']) for f in deep)))
P("S63 D mod 3:", dict(Counter(f['D'] % 3 for f in deep)))
P("S63 Delta (floor-t) values:", dict(Counter(f['Delta'] for f in deep)))
P("S63 sample D:", [f['D'] for f in deep[:8]])

with open(r"D:\math_cc\scratch\agentG_mine_out.txt", "w") as fh:
    fh.write("\n".join(out) + "\n")
print("written agentG_mine_out.txt")
