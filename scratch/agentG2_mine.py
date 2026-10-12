"""agentG2_mine.py -- Task 1 (agentG2 rebuild): mine the canonical fire stream.

Canonical coordinates (this route, fixed once):
  * An excursion E(w,v) starts at n = 0 in state (3w+1; 3w, 6w, ..., 3w*2^(v-2), 3w*2^(v-1)-1).
  * n = number of top steps since excursion start (counts nested steps too).
  * At any state with nonempty list, front entry e1 with role in {R,T,S}:
        sigma = e1      (role R/S),   sigma = e1+1    (role T, e1 = sigma-1)
        d     = head - sigma,   Delta = d - (3n+1),   t_w = (d-1)/3 if (d-1)%3==0.
  * A FIRE is a state with odd head. Its record: (n, gen, role, t_w, Delta, k, i, x).
    gen = nesting generation of the faced entry (0 = the excursion's own E-block).

Checks:
  A) every excursion E(1,v), v<=VMAX ends at a singleton, never halts; sum rule.
  B) universality: the fire stream of E(1,v) agrees with the stream of E(1,VMAX)
     fire-by-fire up to the start of v's endgame (last gen-0 fire) -- one universal stream.
  C) host-law: at every gen-0 R fire: Delta=0, t_w=n, k=v2(3n+4), gap to next gen-0
     fire = dt(k) (agentG table); T fire (gen 0): k=v2(3t_w+2); room i-t_w>=2.
  D) Delta!=0 fires (=nested/interlude fires): Delta = 3*(t_w - n) at integral-t fires;
     taxonomy of non-integral (S63) fires; Delta mod 2^(m+7) structure.
  E) det-scan: (n mod 2^m, Delta [exact and mod 2^(m+7)]) -> (k, family) over
     {universal stream} U {endgame fires of all v<=VMAX}: smallest m; exhibit conflicts.
  F) endgame templates: fires after the last gen-0 fire; template = f(v mod 2^c), find c.
  G) safety pre-check on w=1 data: k < i at R fires etc. (full alpha/gamma fit in
     agentG2_safety.py).

Output: agentG2_mine_out.txt; universal stream saved to agentG2_univ.json;
endgame records to agentG2_endgames.json.
"""
import sys, time, json
from collections import Counter, defaultdict
sys.path.insert(0, r"D:\math_cc\scratch")
from agentG_lib import v2, make_E

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)

def trace(w, v, cap=None):
    """Run E(w,v); return (fires, ell). fires = list of dicts (see header)."""
    ents = [('R', 3 * w << a, 0) for a in range(v - 1)] + [('T', (3 * w << (v - 1)) - 1, 0)]
    head = 3 * w + 1
    if cap is None:
        cap = 4 * v + 400
    n = 0
    fires = []
    while n < cap:
        if not ents:
            return fires, n
        role, val, gen = ents[0]
        sig = val + (1 if role == 'T' else 0)
        d = head - sig
        odd = (head & 1) == 1
        if odd:
            x = head + 2 * val + 3
            ok_t = ((d - 1) % 3 == 0)
            fires.append({
                'n': n, 'gen': gen, 'role': role,
                't': (d - 1) // 3 if ok_t else None,
                'Delta': d - (3 * n + 1),
                'k': v2(x), 'i': v2(sig) if sig > 0 else None,
                'd': d, 'x': x,
            })
        if not odd:
            e1 = ents[0][1]
            e2 = ents[1][1] if len(ents) > 1 else 0
            head += e1 + e2 + 3
            ents = ents[2:]
        else:
            e1 = ents[0][1]
            x = head + 2 * e1 + 3
            k = v2(x)
            q = x >> k
            c = ents[1][1] if len(ents) > 1 else 0
            seam = c + (head + 1) // 2
            run = [('R', q << a, gen + 1) for a in range(k - 1)]
            srole = 'T' if len(ents) == 1 else 'S'
            ents = run + [(srole, seam, gen + 1)] + ents[2:]
            head = q + 1
        n += 1
    raise RuntimeError("E(%d,%d) did not end within %d steps" % (w, v, cap))

def famof(f):
    r = f['role']
    if r == 'R':
        return 'R'
    if r == 'T':
        return 'T'
    return 'S64' if f['t'] is not None else 'S63'

VMAX = 4000
t0 = time.time()

# ---------- reference stream ----------
univ, ell_ref = trace(1, VMAX)
P("reference E(1,%d): ell = %d, fires = %d, time %.1fs" % (VMAX, ell_ref, len(univ), time.time() - t0))
maxk_univ = max(f['k'] for f in univ)
P("universal stream: max k = %d; k-dist: %s" % (maxk_univ,
  dict(sorted(Counter(f['k'] for f in univ).items()))))
maxn_univ = max(f['n'] for f in univ)
P("max n on stream = %d; gen dist: %s; role dist: %s" % (
    maxn_univ, dict(sorted(Counter(f['gen'] for f in univ).items())),
    dict(Counter(f['role'] for f in univ))))

# ---------- A+B: all excursions, universality ----------
t0 = time.time()
endgames = {}          # v -> list of endgame fire records (after last gen-0 fire)
nuniv = 0
viol_univ = 0
maxk_all = 0
ell_small = {}
for v in range(1, VMAX + 1):
    fs, ell = trace(1, v)
    # last gen-0 fire index
    last0 = -1
    for j, f in enumerate(fs):
        if f['gen'] == 0:
            last0 = j
    # universality: fires strictly before the last gen-0 fire must match univ
    # elementwise; the last gen-0 fire itself matches only when it is an R fire
    # (when the block runs out the R fire at that walk slot is REPLACED by the
    # tail fire T with same n, t, Delta but role/k per the T-law).
    upto = last0 if (last0 >= 0 and fs[last0]['role'] == 'R') else last0
    for j in range(upto):
        a, b = fs[j], univ[j]
        if not (a['n'] == b['n'] and a['gen'] == b['gen'] and a['role'] == b['role']
                and a['t'] == b['t'] and a['Delta'] == b['Delta'] and a['k'] == b['k']):
            viol_univ += 1
            if viol_univ <= 5:
                P("  universality VIOLATION v=%d idx=%d: %r vs %r" % (v, j, a, b))
    nuniv += upto
    endgames[v] = [(f['n'], f['gen'], f['role'], f['k'], f['i'], f['t'],
                    f['Delta'] if abs(f['Delta']) < 10**15 else None) for f in fs[last0 + 1:]]
    maxk_all = max(maxk_all, max((f['k'] for f in fs), default=0))
    ell_small[v] = ell
P("A) all E(1,v), v<=%d end at singletons; no halt; universality violations: %d "
  "(%.1fs)" % (VMAX, viol_univ, time.time() - t0))
P("   total fires classified universal-prefix: %d; max k over all v: %d" % (nuniv, maxk_all))

# ---------- C) host law ----------
TAB = {}
for line in open(r"D:\math_cc\scratch\agentG_table.txt"):
    a, b, c = line.split()
    TAB[int(a)] = (int(b), int(c))
t0 = time.time()
host = [f for f in univ if f['gen'] == 0]
badhost = 0
badgap = 0
minroom = 10**9
for j, f in enumerate(host):
    if f['role'] != 'R':
        continue
    if not (f['Delta'] == 0 and f['t'] == f['n'] and f['k'] == v2(3 * f['n'] + 4)):
        badhost += 1
    if f['i'] is not None and f['t'] is not None:
        minroom = min(minroom, f['i'] - f['t'])
    # gap to next host fire
    if j + 1 < len(host):
        gap = host[j + 1]['n'] - f['n']
        if gap != TAB[f['k']][0]:
            badgap += 1
            if badgap <= 3:
                P("  gap violation at n=%d k=%d gap=%d expected=%d" % (
                    f['n'], f['k'], gap, TAB[f['k']][0]))
# T fires (gen 0): k = v2(3 t + 2)
badT = sum(1 for f in host if f['role'] == 'T' and f['k'] != v2(3 * f['t'] + 2))
P("C) host R fires: %d; Delta!=0 or k!=v2(3n+4) or t!=n: %d; gap!=dt(k): %d; "
  "gen-0 T fires: %d, k-law bad: %d; min room i-t: %d" % (
    sum(1 for f in host if f['role'] == 'R'), badhost, badgap,
    sum(1 for f in host if f['role'] == 'T'), badT, minroom))
# walk agreement (independent recomputation)
t, i = 2, 4
wpos = [(2, 4)]
for _ in range(len(host) + 5):
    k = v2(3 * t + 4)
    dt, di = TAB[k]
    t += dt; i += di
    wpos.append((t, i))
wr = [(f['n'], f['i']) for f in host if f['role'] == 'R']
P("   walk (t,i) reproduces host R stream: %s" % (wr == wpos[:len(wr)]))

# ---------- D) Delta structure ----------
t0 = time.time()
nested = [f for f in univ if f['Delta'] != 0]
P("D) fires with Delta!=0 on the stream: %d of %d" % (len(nested), len(univ)))
badd = sum(1 for f in nested if f['t'] is not None and f['Delta'] != 3 * (f['t'] - f['n']))
P("   integral-t fires with Delta == 3*(t_w - n): violations %d / %d" % (
    badd, sum(1 for f in nested if f['t'] is not None)))
P("   nested role dist: %s; gen dist: %s" % (
    dict(Counter(f['role'] for f in nested)), dict(sorted(Counter(f['gen'] for f in nested).items()))))
# S63 fires (non-integral): i and k dist, d mod 3
s63 = [f for f in univ if f['t'] is None]
P("   S63 fires: %d; (i,k) dist: %s; d mod 3 dist: %s" % (
    len(s63), dict(Counter((f['i'], f['k']) for f in s63)),
    dict(Counter(f['d'] % 3 for f in s63))))
# windows: group Delta!=0 fires by (n mod 128, Delta mod 2^7): the creation law
win = Counter((f['n'] % 128, f['Delta'] % 128, f['role'], f['t'] if f['t'] is not None else -1)
              for f in nested)
P("   (n mod 128, Delta mod 128, role, t_w) of nested fires, top 16: %s" % (
    sorted(win.items(), key=lambda kv: -kv[1])[:16]))

# ---------- E) det scans ----------
t0 = time.time()
def scan(fires, label, dmod=None, mmax=16):
    """smallest m with (n mod 2^m, Delta [mod dmod if given]) -> (k, fam) well-defined."""
    res = []
    for m in range(1, mmax + 1):
        tab = {}
        conflict = []
        for f in fires:
            D = f.Delta if dmod is None else f.Delta % dmod(m)
            key = (f.n % (1 << m), D)
            val = (f.k, f.fam)
            if key in tab and tab[key] != val and len(conflict) < 3:
                conflict.append((key, tab[key], val, f.n))
            tab[key] = val
        res.append((m, len(tab), conflict))
        if not conflict:
            P("%s: smallest m = %d (distinct keys %d) [no conflict]" % (label, m, len(tab)))
            return m, res
    P("%s: NO m <= %d works; conflicts at top m: %s" % (label, mmax, res[-1][2][:2]))
    for m, nk, cf in res:
        P("   m=%2d keys=%5d conflict=%s" % (m, nk, "Y" if cf else "."))
    return None, res

# fire set = universal stream + all endgame fires (Delta small stored exactly; big -> mod)
class EF:  # lightweight endgame fire wrapper
    __slots__ = ('n', 'Delta', 'k', 'fam')
    def __init__(self, n, Delta, k, fam):
        self.n = n; self.Delta = Delta; self.k = k; self.fam = fam

egf = []
for v, recs in endgames.items():
    base_n = None
    for (n, gen, role, k, i, t, Del) in recs:
        if Del is None:
            continue  # huge-Delta endgame fires handled with mod below
        egf.append(EF(n, Del, k, role if role != 'S' else ('S64' if t is not None else 'S63')))
P("E) endgame fires with small |Delta|: %d" % len(egf))

class FF:  # lightweight wrapper: attribute access
    __slots__ = ('n', 'Delta', 'k', 'fam')
    def __init__(self, n, Delta, k, fam):
        self.n = n; self.Delta = Delta; self.k = k; self.fam = fam

strf = [FF(f['n'], f['Delta'], f['k'], famof(f)) for f in univ]
m1, _ = scan(strf, "scan(stream, Delta exact)")
m2, _ = scan(strf + egf, "scan(stream+endgames, Delta exact)")
m3, _ = scan(strf, "scan(stream, Delta mod 2^(m+7))", dmod=lambda m: 1 << (m + 7))
m4, _ = scan(strf + egf, "scan(stream+endgames, Delta mod 2^(m+7))", dmod=lambda m: 1 << (m + 7))
P("   (prior agent, v<=2000 semantics t=(D-1)/3: m=11; here t=n canonical time)")
P("   scans took %.1fs" % (time.time() - t0))

# also: t_w-based key (prior agent's): (t_w mod 2^m, Delta) for integral fires only
def scan_tw(fires, label, dmod=None, mmax=16):
    for m in range(1, mmax + 1):
        tab = {}
        conflict = 0
        for f in fires:
            if f['t'] is None:
                continue
            D = f['Delta'] if dmod is None else f['Delta'] % dmod(m)
            key = (f['t'] % (1 << m), D)
            val = (f['k'], famof(f))
            if key in tab and tab[key] != val:
                conflict += 1
            tab[key] = val
        if conflict == 0:
            P("%s: smallest m = %d (keys %d)" % (label, m, len(tab)))
            return m
    P("%s: no m <= %d" % (label, mmax))
    return None
scan_tw(univ, "scan_tw(stream)")

# ---------- F) endgame templates ----------
t0 = time.time()
# template = tuple of (role, k, i, integral?) for endgame fires + ell tail; find c: template = f(v mod 2^c)
def templ(v):
    recs = endgames[v]
    return tuple((r[2], r[3], r[4], r[5] is not None) for r in recs)
tcache = {}
ok_c = None
for c in range(0, 8):
    bad = 0
    for v in range(1, VMAX + 1):
        key = (v % (1 << c), templ(v))
        if key in tcache and tcache[key] != v:
            pass
        tcache.setdefault(key, v)
    # well-defined: same v mod 2^c -> same template?
    byr = defaultdict(set)
    for v in range(1, VMAX + 1):
        byr[v % (1 << c)].add(templ(v))
    bad = sum(1 for r, s in byr.items() if len(s) > 1)
    if bad == 0:
        ok_c = c
        break
P("F) endgame template determined by v mod 2^c: smallest c = %s; distinct templates: %d" % (
    ok_c, len(set(templ(v) for v in range(1, VMAX + 1)))))
P("   template size dist: %s" % dict(sorted(Counter(len(templ(v)) for v in range(1, VMAX + 1)).items())))
P("   (ell(v) - n of last gen-0 fire) dist: %s" % dict(sorted(Counter(
    ell_small[v] - max([f['n'] for f in []] or [0]) for v in [1]).items())))
P("   scans %.1fs" % (time.time() - t0))

# ---------- G) quick safety on stream ----------
t0 = time.time()
badg = sum(1 for f in univ if f['role'] == 'R' and f['i'] is not None and not f['k'] < f['i'])
badt = sum(1 for f in univ if f['role'] == 'T' and f['i'] is not None and not f['k'] < f['i'])
P("G) stream fires with k >= i (R: %d, T: %d) [S fires handled in safety script]" % (badg, badt))
qs = [f['x'] >> f['k'] for f in univ]
P("   min q on stream fires: %d" % min(qs))

# ---------- save ----------
json.dump([{k: f[k] for k in ('n', 'gen', 'role', 't', 'Delta', 'k', 'i', 'x')}
           for f in univ], open(r"D:\math_cc\scratch\agentG2_univ.json", "w"))
json.dump({str(v): endgames[v] for v in range(1, VMAX + 1)},
          open(r"D:\math_cc\scratch\agentG2_endgames.json", "w"))
json.dump({str(v): ell_small[v] for v in range(1, VMAX + 1)},
          open(r"D:\math_cc\scratch\agentG2_ell.json", "w"))
with open(r"D:\math_cc\scratch\agentG2_mine_out.txt", "w") as fh:
    fh.write("\n".join(OUT) + "\n")
print("saved agentG2_univ.json / agentG2_endgames.json / agentG2_ell.json / agentG2_mine_out.txt")
