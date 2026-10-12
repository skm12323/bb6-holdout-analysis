# U1: sibling equivalence.  Reuses the symbolic run-length core of work_q4/verify_q4.py (imported, NOT modified;
# only its module-global transition table V.T is swapped per machine) and adds case splitting on variables.
import sys, re, itertools
sys.path.insert(0, 'D:/math_cc/work_q4')
import verify_q4 as V

TMS = {'M0': '1RB0LE_0RC1RB_1LC1RD_1RF0LA_0RD1LE_1RB---',
       'M1': '1RB0LD_1LC1RD_0LE1LA_0RB1RD_---0LF_1RA1LF',
       'M2': '1RB1RA_1LC0RC_1RE0LD_0RE0LF_1RA---_1RB1LF',
       'M3': '1RB1RC_1LC0LE_1RD1RC_1LB0RA_---0LF_1RD1LF'}
DSTATE = {'M1': 'D', 'M2': 'B', 'M3': 'D'}

# ---------------- splitting prover ----------------
def sub_lf(lf, v, k):            # v:=0 (k None) or v:=v+1 (k=1)
    if lf == V.INF or v not in lf: return lf
    d = dict(lf); c = d.pop(v)
    if k is not None: d[v] = c; d[1] = d.get(1, 0) + c * k
    return {a: b for a, b in d.items() if b}
def sub_cfg(c, v, k):
    l, h, r = c; f = lambda rs: V.norm([[s, sub_lf(n, v, k)] for s, n in rs])
    return (f(l), h, f(r))
def canon(c):
    """same tape+head, written with the head reading the first cell of the right part"""
    l, (S, D), r = c
    if D == 'R': return V.show(c)
    l = [x[:] for x in l]; r = [x[:] for x in r]
    sym, n = l[-1]
    if not V.ge1(n): return V.show(c)
    if n != V.INF: l[-1][1] = V.add(n, {1: -1})
    r.insert(0, [sym, {1: 1}])
    return V.show((V.norm([x for x in l if x[1] == V.INF or not V.iszero(x[1])]), (S, 'R'), V.norm(r)))
def head_run(c):
    l, (S, D), r = c; return r[0] if D == 'R' else l[-1]
def trace(c, tgt=None, maxsteps=5000, maxdepth=6):
    """symbolic run with case splits. Leaves: (subs, outcome, steps); outcome = 'RHS' | 'HALT' | 'OUT..' | 'MAX'"""
    out = []; stack = [(c, tgt, {}, [], 0)]
    while stack:
        c, t, steps, subs, i = stack.pop()
        while True:
            if i > 0 and t is not None and canon(c) == canon(t): out.append((subs, 'RHS', steps)); break
            if i >= maxsteps: out.append((subs, 'MAX', steps)); break
            try: res = V.step(c)
            except Exception as e:
                if 'SPLIT' not in str(e): out.append((subs, 'OUT ' + V.show(c), steps)); break
                if len(subs) >= maxdepth: out.append((subs, 'DEPTH ' + V.show(c), steps)); break
                v = [x for x in head_run(c)[1] if x != 1][0]
                for k in (None, 1):
                    stack.append((sub_cfg(c, v, k), None if t is None else sub_cfg(t, v, k),
                                  sub_lf(steps, v, k), subs + [(v, k)], i))
                break
            if res == 'HALT': out.append((subs, 'HALT', steps)); break
            c, k = res; steps = V.add(steps, k); i += 1
    return out
def check(lhs, rhs, claim):
    """True iff every branch reaches RHS (rhs=None: reaches HALT) with steps == claim (substituted)"""
    leaves = trace(V.parse_cfg(lhs), None if rhs is None else V.parse_cfg(rhs))
    ok = True
    for subs, o, st in leaves:
        cl = V.L(claim)
        for v, k in subs: cl = sub_lf(cl, v, k)
        ok &= (o == ('RHS' if rhs else 'HALT')) and V.fmt(st) == V.fmt(cl)
    return ok, leaves

# ---------------- encodings (symbolic: rewrite M0's rule strings) ----------------
def inc(x, k): return V.fmt(V.add(V.L(x), {1: k}))
def conv(s, sib):
    s = ' ' + s + ' '
    if sib == 'M1':     # A-block stored as length b_i+1, single gap g_i under the head, state F
        s = s.replace(' 0 <A 0 0 0 ', ' F> 0 1 0 0 ')
        s = re.sub(r' 0 <A 0 1(\^(\S+))? ', lambda m: ' F> 0 1^' + inc(m.group(2) or '1', 1) + ' ', s)
    else:               # A-block stored as length b_i, single gap g_i under the head, state F
        s = s.replace(' 0 <A 0 ', ' F> 0 ')
        # D at i: gap g_{i+1} removed; head (state B resp. D) on the cell right after block i
        s = re.sub(r' 0 1 D> 1\^(\S+) 0\^inf ', lambda m: ' 0 1^' + inc(m.group(1), 1) + ' ' + DSTATE[sib] + '> 0^inf ', s)
        s = re.sub(r' 0 1 D> 1\^(\S+) 0 ', lambda m: ' 0 1^' + inc(m.group(1), 1) + ' ' + DSTATE[sib] + '> ', s)
    return s.strip()

def render(B, ph, sib):
    """encode_i(B,phase) -> (cells, head index, state); 4 padding zeros each side (cf. EQUIV.md Sec.1)"""
    kind, i = ph; cells = [0] * 4; head = None; m = len(B)
    for k, b in enumerate(B):
        if kind == 'A':
            if k == i: cells += [0]; head = len(cells) - 1           # single gap g_i under the head (k=0: left 0)
            elif k > 0: cells += [0] * (2 if k == i + 1 else 1)        # g_{i+1} doubled
            cells += [1] * (b + (1 if (k == i and sib == 'M1') else 0))
        else:
            if sib == 'M1':
                if k > 0: cells += [0]
                if k == i: head = len(cells) + 1                        # second cell of block i
            else:
                if k > 0 and k != i + 1: cells += [0]                  # g_{i+1} absent
                if k == i + 1: head = len(cells)                        # first cell of block i+1
            cells += [1] * b
    cells += [0] * 4
    if kind == 'D' and sib != 'M1' and i == m - 1: head = len(cells) - 4  # cell right after the last block
    st = 'F' if kind == 'A' else ('D' if sib == 'M1' else DSTATE[sib])
    return cells, head, st

# Proven step counts, in RULES.md Sec.2 parameters.  ('HALT',h): the sibling halts (reaches its halting
# transition) after h steps from this LHS instead of performing the row.
CLAIM = {
 'M1': {"R1": "2n+11", "R1'": "2n+11", "R2": "p+8", "R2'": ('HALT', '15'), "R3": "j+21", "R3'": "j+21",
        "R3''": "2j+25", "R3k": "6j+117", "R4": "a+3", "R5": "2a+6", "R6": "a+61", "X0": ('HALT', '15')},
 'M2': {"R1": "2n+9", "R1'": "2n+9", "R2": "p+4", "R2'": "j+12", "R3": "j+k+10", "R3'": "j+k+10",
        "R3''": "2j+9", "R3k": "6j+63", "R4": "b+5", "R5": "a+3", "R6": "28", "X0": "15"},
 'M3': {"R1": "2n+7", "R1'": "2n+7", "R2": "p+4", "R2'": ('HALT', '3'), "R3": "j+k+10", "R3'": "j+k+10",
        "R3''": "2j+11", "R3k": "6j+63", "R4": "b+3", "R5": "a+3", "R6": "30", "X0": ('HALT', '3')}}
HCLAIM = {'M1': {'H1': '15'}, 'M2': {'H1': '9', 'H2': 'j+7', "H2'": 'j+7', 'H3': '2'}, 'M3': {'H1': '3'}}
BASE = {'M1': ('0^inf F> 0 1^2 0 0 1 0^inf', 12), 'M2': ('0^inf F> 0 1 0 0 1 0^inf', 11),
        'M3': ('0^inf F> 0 1 0 0 1 0^inf', 9)}
X0ROW = ("X0", "0^inf 0 <A 0 0 0 1 0^inf", "0^inf 1^3 0 <A 0 1 0 0 1 0^inf", "25")

def fmt_leaves(leaves):
    return '; '.join(f"{','.join(v+('=0' if k is None else '>=1') for v,k in s) or 'all'}:{o.split()[0]}[{V.fmt(st)}]"
                     for s, o, st in leaves)

def sec1(sib):
    V.T = V.parse(TMS[sib])
    print(f'== {sib} = {TMS[sib]} ==\n-- Sec.1 macro rows (symbolic over all params >= 0; window principle as in Q4) --')
    for name, l, r, _ in V.RULES + [X0ROW]:
        if sib != 'M1' and re.search(r' D> 1\^\S+$', r): l, r = l + ' 0', r + ' 0'   # gap g_{i+1} joins the window
        L, R = conv(l, sib), conv(r, sib); cl = CLAIM[sib][name]
        if isinstance(cl, tuple): ok, leaves = check(L, None, cl[1]); what = f'HALTS after {cl[1]} (row NOT realised)'
        else: ok, leaves = check(L, R, cl); what = f'[{cl}]'
        print(f'  {name:5s} {L:44s} -> {R:46s} {what}  proved={ok}')
        assert ok, fmt_leaves(leaves)
    print('-- Sec.2 halting lemmas (H configurations) --')
    for name, l, _ in V.HALTS:
        nm = name.split()[0]; L = conv(l, sib)
        if nm in HCLAIM[sib]:
            ok, leaves = check(L, None, HCLAIM[sib][nm]); assert ok
            print(f'  {nm:4s} {L:44s} HALTS after {HCLAIM[sib][nm]} steps  proved=True')
        else:
            leaves = trace(V.parse_cfg(L))
            kinds = sorted(set(o.split()[0] for _, o, _ in leaves))
            print(f'  {nm:4s} {L:44s} NOT claimed (row differs from M or is undetermined); branch outcomes {kinds}: {fmt_leaves(leaves)[:110]}')
    l, t = BASE[sib]; ok, _ = check('0^inf <A 0^inf', l, str(t)); assert ok
    print(f'-- Sec.3 base: blank tape (state A) -> {l} = encode_{sib}([1,1],A,0) after {t} steps  proved={ok}')

# ---------------- abstract map with sibling step counts ----------------
def row(B, ph):
    """M's row (RULES.md Sec.3 decision tree) + Sec.2 parameters"""
    kind, i = ph; m = len(B)
    if kind == 'A':
        n = B[i]; p = B[i-1] if i >= 1 else 0
        if n >= 2: return ("R1" if i else "R1'"), dict(n=n-2, p=p, j=B[i+1])
        if n == 0:
            if i >= 1: return "R2", dict(p=p-1)
            if B[1] >= 2: return "R2'", dict(j=B[1]-2)
            return ("X0", {}) if m == 2 else ("H1", dict(c=B[2]-1))
        j = B[i+1]
        if i+1 == m-1: return "R3''", dict(p=p, j=j)
        k = B[i+2]
        if k >= 2: return ("R3" if i else "R3'"), dict(p=p, j=j, k=k-2)
        if i+2 == m-1: return "R3k", dict(p=p, j=j)
        return ("H2" if i else "H2'"), dict(p=p, j=j, c=B[i+3]-1)
    a = B[i]-2
    if i == m-1: return "R5", dict(a=a, q=B[i-1])
    if B[i+1] >= 2: return "R4", dict(a=a, b=B[i+1]-2)
    if i+1 == m-1: return "R6", dict(a=a)
    return "H3", dict(a=a, c=B[i+2]-1)
def ev(f, env): return eval(re.sub(r'(\d)([a-z])', r'\1*\2', f), {}, env)
class Halt(Exception): pass
def macro(B, ph, sib):
    """one step of M with sibling step counts; raises Halt(row, h or None) where M has H or sib halts instead"""
    nm, env = row(B, ph)
    if nm in ('H1', 'H2', "H2'", 'H3'):
        h = HCLAIM[sib].get(nm); raise Halt(nm, None if h is None else ev(h, env))
    cl = CLAIM[sib][nm]
    if isinstance(cl, tuple): raise Halt(nm, ev(cl[1], env))
    B2, ph2, _ = V.macro(B, ph)
    return B2, ph2, ev(cl, env)

def raw(sib):
    T = V.parse(TMS[sib]); return {k: (None if v is None else (v[0], 1 if v[1] == 'R' else -1, v[2])) for k, v in T.items()}
def cut(cells, head):
    ones = [k for k, x in enumerate(cells) if x]; a = min(ones + [head]); b = max(ones + [head])
    return ''.join(map(str, cells[a:b+1])), head - a

def sec4(sib, M=5, BMAX=4):
    """sanity [Class-C]: every Inv config with m<=M, blocks<=BMAX: raw sib from encode_sib(c) for the claimed
    step count lands exactly on encode_sib(M(c)) (or reaches its halting transition at the claimed step)"""
    T2 = raw(sib); n = 0; names = {}
    for m in range(2, M+1):
        for B in itertools.product(range(BMAX+1), repeat=m):
            B = list(B)
            for ph in [('A', i) for i in range(m-1)] + [('D', i) for i in range(1, m)]:
                if not V.inv(B, ph): continue
                c, h, s = render(B, ph, sib); pad = 400
                tape = dict(enumerate([0]*pad + c + [0]*pad)); p = h + pad
                try: B2, ph2, dt = macro(B, ph, sib); hal = False
                except Halt as e:
                    hal = True; dt = e.args[1]
                    if dt is None: continue           # unclaimed (M1/M3 on H2,H2',H3)
                st = 'RUN'
                for t in range(dt):
                    tr = T2[(s, tape.get(p, 0))]
                    if tr is None: st = 'HALT'; break
                    w, d, s = tr; tape[p] = w; p += d
                if hal:
                    assert st == 'RUN' and T2[(s, tape.get(p, 0))] is None, (sib, B, ph)
                else:
                    c2, h2, s2 = render(B2, ph2, sib); lo = min(tape)
                    cells = [tape.get(k, 0) for k in range(lo, max(tape)+1)]
                    assert st == 'RUN' and s == s2 and cut(cells, p - lo) == cut(c2, h2), (sib, B, ph, row(B, ph))
                nm = row(B, ph)[0]; names[nm] = names.get(nm, 0) + 1; n += 1
    print(f'-- Sec.4 sanity [Class-C]: {n} Inv configs (m<={M}, blocks<={BMAX}) behave exactly as claimed; rows: {names}')

def sec5(sib, N):
    """raw sib vs abstract orbit of M from c_0 [Class-C]"""
    T2 = raw(sib); t0 = BASE[sib][1]
    B, ph, t = [1, 1], ('A', 0), t0; cps = {}
    while t <= N:
        cps[t] = (B, ph)
        try: B, ph, dt = macro(B, ph, sib)
        except Halt as e: print('  abstract halt', e.args, 'at', t); break
        t += dt
    tape = bytearray(1 << 17); p = 1 << 16; s = 'A'; ok = 0
    for tt in range(N+1):
        if tt in cps:
            Bc, phc = cps[tt]; bt = bytes(tape)
            a = min(bt.find(1), p) if 1 in bt else p; b = max(bt.rfind(1), p)
            c2, h2, s2 = render(Bc, phc, sib); w = cut(c2, h2)
            assert (''.join(map(str, bt[a:b+1])), p - a, s) == (w[0], w[1], s2), ('MISMATCH', sib, tt, Bc, phc)
            ok += 1
        tr = T2[(s, tape[p])]
        if tr is None: print('  TM HALT at', tt); break
        w_, d, s = tr; tape[p] = w_; p += d
    last = max(cps)
    print(f'-- Sec.5 cross-check [Class-C]: {ok} checkpoints matched exactly, t in [{t0},{N}] {sib}-steps; '
          f'no halt; blocks at end {len(cps[last][0])}')
    return [cps[k] for k in sorted(cps)]

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3 * 10**6
    orbits = {}
    for sib in ['M1', 'M2', 'M3']:
        sec1(sib); sec4(sib); orbits[sib] = sec5(sib, N)
    B, ph = [1, 1], ('A', 0); ref = []
    for _ in range(max(len(o) for o in orbits.values())):
        ref.append((B, ph)); B, ph, _ = V.macro(B, ph)
    print('== Sec.6 same orbit ==')
    for sib, o in orbits.items():
        assert o == ref[:len(o)]
        print(f'  {sib}: checkpoint sequence = c_0..c_{len(o)-1} of the M-orbit of RULES.md Sec.5 (same as M0)')
