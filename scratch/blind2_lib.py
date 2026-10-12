"""Blind Auditor 2 — from-scratch engines (Python stdlib only).

Audited reduction (work_r1/RULES.md, GIVEN): top map on lists L=(A,b,c,S):
  A even -> (A+b+c+3, S);
  A odd  -> m := b+(A-3)/2; st := (c+(A+1)/2, S);
            while m odd and m>=3: st=[(m+3)/2]+st; m:=(m-3)/2;
            m==1 -> HALT; else (m+4, st).
HALT <=> a chain with x=A+2b+3 a power of two (u=1).

Excursion start: from the odd singleton A0=3*2^v*w-3 (w odd, v>=1) the first
step is a chain with b=c=0 (x=3*2^v*w, j=v, u=3w) that creates level 0:
run [3w*2^a, a=0..v-2] and defect D0=3w*2^(v-1)-1, i.e. E(w,v).

Every queue entry is tagged (val, level, kind, pos): kind RUN (run entry of
`level` at position pos) or DEF (defect/seam of `level`).  Each chain pushes a
new level (base u, run u,2u,...,2^(j-2)u, defect c+(A+1)/2).
"""
from collections import deque


def v2(n):
    """2-adic valuation (n != 0)."""
    return (n & -n).bit_length() - 1


def top_step_plain(L):
    """The audited top map, verbatim, on plain lists (missing b,c = 0).
    Returns (L2, None) or (None, 'HALT')."""
    A = L[0]
    if A % 2 == 0:
        b = L[1] if len(L) > 1 else 0
        c = L[2] if len(L) > 2 else 0
        return [A + b + c + 3] + L[3:], None
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    m = b + (A - 3) // 2
    st = [c + (A + 1) // 2] + L[3:]
    while m % 2 == 1 and m >= 3:
        st.insert(0, (m + 3) // 2)
        m = (m - 3) // 2
    if m == 1:
        return None, 'HALT'
    return [m + 4] + st, None


RUN, DEF = 0, 1


class Proc:
    """Tagged engine: state (A, queue, levels).  levels: id -> (base, depth,
    par_j, par_lvl).  step() returns an event tuple; Lemma-1 closed form of a
    chain is checked at every chain (recorded in self.probs)."""
    __slots__ = ('A', 'q', 'levels', 'nlvl', 'steps', 'probs')

    def __init__(self, A=0, q=None, levels=None, nlvl=0):
        self.A = A
        self.q = deque(q) if q is not None else deque()
        self.levels = levels if levels is not None else {}
        self.nlvl = nlvl
        self.steps = 0
        self.probs = []

    def step(self):
        q = self.q
        A = self.A
        if A % 2 == 0:
            b = q.popleft() if q else None
            c = q.popleft() if q else None
            self.A = A + (b[0] if b else 0) + (c[0] if c else 0) + 3
            self.steps += 1
            return ('E', b, c)
        b = q.popleft() if q else None
        c = q.popleft() if q else None
        bv = b[0] if b else 0
        cv = c[0] if c else 0
        x = A + 2 * bv + 3
        m = bv + (A - 3) // 2
        pushes = []
        while m % 2 == 1 and m >= 3:
            pushes.append((m + 3) // 2)
            m = (m - 3) // 2
        self.steps += 1
        if m == 1:
            return ('HALT', b, c, x)
        j = len(pushes) + 1
        u = m + 3
        ok = (x == (u << j)) and (u & 1 == 1) and (v2(x) == j) and \
             all(pushes[i] == x >> (i + 2) for i in range(j - 1))
        if not ok:
            self.probs.append(('LEMMA1', self.steps, A, bv, cv, x, j, u, m))
        nl = self.nlvl
        self.nlvl += 1
        depth = 0 if b is None else self.levels[b[1]][1] + 1
        self.levels[nl] = (u, depth, j, (b[1] if b is not None else None))
        q.appendleft((cv + (A + 1) // 2, nl, DEF, -1))
        for a in range(j - 2, -1, -1):
            q.appendleft((u << a, nl, RUN, a))
        self.A = u + 1
        return ('C', b, c, x, j, u, m, nl)


def brole(b, levels):
    """Role of consumed b at a fire: run entry / seam D (level>=1, = c+(A+1)/2
    of a prior fire) / tail T (defect D0 of the excursion) / zero."""
    if b is None:
        return 'zero'
    if b[2] == RUN:
        return 'run'
    return 'tail' if b[1] == 0 else 'seam'


def cinfo(b, c, levels):
    """Compact (kind, same_level_as_b, pos) description of consumed c."""
    if c is None:
        return ('0', False, -1)
    same = (b is not None and c[1] == b[1])
    return (('R' if c[2] == RUN else 'D'), same, c[3])


class Agg:
    """Cross-run aggregate checks (S2/S3/S4)."""

    def __init__(self):
        self.uni = {}            # rho -> (k, j): universal replay invariant
        self.uni_ctx = {}        # rho -> first context
        self.uni_viol = []       # (rho, (k,j), (k',j'), ctx)
        self.role_counts = {}
        self.role_min_u = {}
        self.role_max_j = {}
        self.n_fires = 0
        self.n_levels = 0
        self.min_u_all = (None, None)
        self.max_j = (0, None)
        self.max_j_over_rho = (0.0, None)
        self.max_k_over_rho = (0.0, None)
        self.viol_j_ge_rho = []      # run fires with j >= rho (any rho)
        self.viol_k_bound = []       # k > 0.4465*rho
        self.viol_j_bound = []       # j > 3*log2(rho)+3 (rho>=32)
        self.viol_nested = []        # nested level: j >= par_j or rho > par_j-2
        self.viol_c_role = []        # run fire with c not same-level run/D
        self.viol_rho_lt4 = []       # run fire with rho < 4
        self.viol_k_int = []         # run fire with x-3*2^rho*U-4 not = 6k, k>=0
        self.viol_j_formula = []     # run fire with j != 1+v2(3k+2)
        self.spike_list = []         # (J, rho, k, v, w, depth) run fires j>=5
        self.spike_nonrun = []       # (J, v, w, role) non-run fires j>=5
        self.host_seq = []           # ordered (rho,k,j) of level-depth-0 fires
        self.level_seqs = {}         # lvl -> [(rho,k,j)] (one run at a time)
        self.halts = []

    def add_fire(self, v, w, step, idx, ex, ev):
        b, c = ev[1], ev[2]
        x, j, u, nl = ev[3], ev[4], ev[5], ev[7]
        levels = ex.levels
        role = brole(b, levels)
        self.n_fires += 1
        self.role_counts[role] = self.role_counts.get(role, 0) + 1
        mu = self.role_min_u.get(role)
        if mu is None or u < mu[0]:
            self.role_min_u[role] = (u, (v, w, step, idx))
        if u < 3:
            self.halts.append(('u<3', v, w, step, idx, role, u))
        if self.min_u_all[0] is None or u < self.min_u_all[0]:
            self.min_u_all = (u, (v, w, step, idx, role))
        if j > self.max_j[0]:
            self.max_j = (j, (v, w, step, idx, role))
        if j > self.role_max_j.get(role, (0, None))[0]:
            self.role_max_j[role] = (j, (v, w, step, idx))
        ci = cinfo(b, c, levels)
        if j >= 5:
            if role == 'run':
                rho = b[3]
                U = levels[b[1]][0]
                t = x - 3 * (U << rho) - 4
                k = t // 6 if (t >= 0 and t % 6 == 0) else None
                self.spike_list.append((j, rho, k, v, w, levels[b[1]][1]))
            else:
                self.spike_nonrun.append((j, v, w, role))
        if role != 'run':
            return None
        # ---- run-chain checks (S3/S4) ----
        rho = b[3]
        blvl = b[1]
        base, depth, par_j, par_lvl = levels[blvl]
        t = x - 3 * (base << rho) - 4
        if t >= 0 and t % 6 == 0:
            k = t // 6
        else:
            k = None
            self.viol_k_int.append((v, w, step, rho, t))
        ctx = (v, w, step, idx, depth, blvl)
        if k is not None:
            if rho in self.uni:
                if self.uni[rho] != (k, j):
                    self.uni_viol.append((rho, self.uni[rho], (k, j), ctx,
                                          self.uni_ctx[rho]))
            else:
                self.uni[rho] = (k, j)
                self.uni_ctx[rho] = ctx
            if j != 1 + v2(3 * k + 2):
                self.viol_j_formula.append((v, w, step, rho, k, j, ctx))
            if 6 * k + 4 >= (1 << j) * 1:  # 2^J <= 6k+4 (margin identity)
                pass
            else:
                self.viol_k_bound.append(('2^J>6k+4', v, w, rho, k, j))
            if 20 * k > 893 * rho:  # k <= 0.4465*rho
                self.viol_k_bound.append((v, w, step, rho, k, j))
            if j >= rho:
                self.viol_j_ge_rho.append((v, w, step, rho, k, j, ctx))
            elif j / rho > self.max_j_over_rho[0]:
                self.max_j_over_rho = (j / rho, (v, w, rho, j, k))
            if k / rho > self.max_k_over_rho[0]:
                self.max_k_over_rho = (k / rho, (v, w, rho, j, k))
            if rho >= 32 and j > 3 * (rho - 1).bit_length() + 3:
                # crude: 3*log2(rho)+3, integer-safe upper bound
                self.viol_j_bound.append((v, w, step, rho, k, j))
        if rho < 4:
            self.viol_rho_lt4.append((v, w, step, rho, j))
        # c must be a same-level entry (run@rho+1 or the level's D)
        if not (ci[1] and (ci[0] == 'D' or ci[2] == rho + 1)):
            self.viol_c_role.append((v, w, step, rho, j, ci))
        # nested decrease
        if par_j is not None:
            if j >= par_j or rho > par_j - 2:
                self.viol_nested.append((v, w, step, rho, j, par_j))
        # sequences (host level = depth 0)
        rec = (rho, k, j)
        if depth == 0:
            self.host_seq.append(rec)
        self.level_seqs.setdefault(blvl, []).append(rec)
        return rec


def run_orbit(w, v, agg=None, full=False, cap=None, on_fire=None,
              level_seq_max=0):
    """Run from the odd singleton 3*2^v*w-3 to the next singleton/HALT/cap.
    Returns (ex, fires, fin, final_A, ell).  fires: full records if full=True.
    ell = steps minus the initial singleton chain (= excursion length)."""
    ex = Proc(A=3 * (1 << v) * w - 3)
    if cap is None:
        cap = 8 * v + 400
    fires = [] if full else None
    fin = None
    idx = 0
    first = True
    while True:
        if not first:
            if not ex.q:
                fin = 'singleton'
                break
            if ex.steps >= cap:
                fin = 'cap'
                break
        first = False
        ev = ex.step()
        if ev[0] == 'HALT':
            fin = 'HALT'
            if agg is not None:
                agg.halts.append(('HALT', v, w, ex.steps, ev[3]))
            break
        if ev[0] == 'C':
            if agg is not None:
                agg.add_fire(v, w, ex.steps, idx, ex, ev)
            if full:
                b = ev[1]
                levels = ex.levels
                role = brole(b, levels)
                x, j, u, nl = ev[3], ev[4], ev[5], ev[7]
                rho = b[3] if (b is not None and b[2] == RUN) else -1
                base, depth, par_j, par_lvl = (levels[b[1]] if b is not None
                                               else (0, 0, None, None))
                t = x - 3 * (base << rho) - 4 if role == 'run' else None
                k = (t // 6 if (t is not None and t >= 0 and t % 6 == 0)
                     else None)
                fires.append((idx, ex.steps, role, rho, j, x, u, k, depth,
                              par_j, cinfo(b, ev[2], levels)))
            if on_fire is not None:
                on_fire(ex, ev, idx)
            idx += 1
    return ex, fires, fin, ex.A, max(0, ex.steps - 1)


# ---------------- rule-level (R1..R5) cross-check ----------------

def rule_step(h, rs):
    """One macro rule from RULES.md section 3. rs normalized (no trailing 0).
    Returns (h2, rs2) or 'HALT'."""
    r1 = rs[0]
    k = len(rs)
    if k == 1:
        assert r1 >= 2
        return h + 1, [r1 - 2, 0, 1]          # R2
    r2 = rs[1]
    if r1 >= 2:
        if r2 >= 1:                            # R1
            out = [r1, r2 - 1] + rs[2:]
        else:                                  # R3 (k>=3 since rs[-1]>=1)
            out = [r1 - 2, 0, rs[2] + 1] + rs[3:]
    elif r1 == 1:
        assert r2 == 0
        if h == 0:
            return 'HALT'
        return 0, [h - 1, 0, 1, rs[2] + 1] + rs[3:]   # R4
    else:
        assert r1 == 0 and r2 == 0
        return 0, [h + rs[2] + 3] + rs[3:]     # R5
    while out and out[-1] == 0:
        out.pop()
    return h + 1, out


def norm_cfg(h, rs):
    while rs and rs[-1] == 0:
        rs.pop()
    return h, rs


def rule_run_topseq(n_top=300):
    """Rule-level run from (0;3); returns the list of top configs' L lists
    (h==0 and (k==1 or r2>=1)), padded with zeros to length>=3."""
    h, rs = 0, [3]
    tops = []
    guard = 0
    while len(tops) < n_top:
        guard += 1
        assert guard < 30_000_000
        if h == 0 and (len(rs) == 1 or rs[1] >= 1):
            tops.append(list(rs))
        r = rule_step(h, rs)
        if r == 'HALT':
            tops.append('HALT')
            return tops
        h, rs = norm_cfg(*r)
    return tops


def cross_check_top_vs_rules(n_top=300):
    """Iterate the top map from (3); compare with rule-level top configs."""
    tops = rule_run_topseq(n_top)
    L = [3]
    for i, T in enumerate(tops):
        if T == 'HALT':
            return (False, 'rule-level halted at top config %d' % i)
        if L != T:
            return (False, 'mismatch at top config %d: top=%s rules=%s'
                    % (i, L[:6], T[:6]))
        L, hlt = top_step_plain(L)
        if hlt == 'HALT':
            return (True, 'top map halted after %d configs (rules did not)'
                    % i) if i + 1 < len(tops) else (True, 'both halt')
    return True, 'first %d top configs identical' % n_top


if __name__ == '__main__':
    # quick self-tests
    # 1) top map vs rule level
    print(cross_check_top_vs_rules(400))
    # 2) E(w,v) structure from the singleton chain + ell(1..20)
    ell_expected = [1, 1, 2, 2, 5, 4, 4, 6, 7, 8, 8, 10, 10, 15, 12, 12, 14,
                    15, 15, 16]
    ells = []
    for v in range(1, 21):
        ex, fires, fin, A, ell = run_orbit(1, v)
        assert fin == 'singleton', (v, fin)
        ells.append(ell)
        # E-structure: after first step the state must be (3w+1; 3w,...,D0)
    print('ell(1..20) =', ells)
    print('ell matches expected:', ells == ell_expected)
    # 3) tagged vs plain, step by step, for a few (w,v)
    import random as _r
    for (w, v) in [(1, 30), (3, 41), (5, 17), (1, 120), (7, 63)]:
        ex = Proc(A=3 * (1 << v) * w - 3)
        L = [3 * (1 << v) * w - 3]
        while True:
            ev = ex.step()
            if ev[0] == 'HALT':
                break
            L, hlt = top_step_plain(L)
            assert hlt is None, (w, v)
            assert L == [ex.A] + [e[0] for e in ex.q], (w, v, ex.steps)
            if not ex.q:
                break
        assert not ex.probs, ex.probs[:3]
    print('tagged==plain ok; Lemma-1 closed form ok')
    # 4) sum invariant (mod 3) for v<=120, w in 1,3,5
    for w in (1, 3, 5):
        for v in range(1, 121):
            ex = Proc(A=3 * (1 << v) * w - 3)
            s0 = 3 * (1 << v) * w - 3
            while True:
                ev = ex.step()
                if ev[0] == 'HALT':
                    break
                s = ex.A + sum(e[0] for e in ex.q)
                assert s == s0 + 3 * ex.steps, (w, v, ex.steps)
                assert s % 3 == 0, (w, v, ex.steps)
                if not ex.q:
                    break
    print('sum = 3(n+1)+3*steps invariant ok (v<=120)')
