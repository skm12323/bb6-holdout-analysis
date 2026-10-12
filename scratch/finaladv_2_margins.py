"""finaladv_2_margins.py — ANGLE 2: the mu-walker's MARGIN=900 assumption.

(a) Margin census: all top-level spike hosts in E(1,5000) with true p-J;
    the deepest spike; smallest margins (are there hosts with p-J in {12,50}?).
(b) MARGIN-patch equivalence: run agentB_mu.Walker with MARGIN in
    {900,50,20,12,8,4,2,1}; the event stream must be IDENTICAL.  If the
    stream is MARGIN-independent down to 1, every walker decision is free of
    the M-valuation, so the walk transfers to every host with true p-J >= 1
    (all of them: p > J at spike hosts since v2(6k+4)=J<v2(9*2^p w)=p), and
    to the excursion host U=3w=M+mu with M=3w-1 (margin v2(3w-1) >= 1).
(c) Vanishing-mu scan: v2_val returns min(v2(cmu), v2(e)) assuming
    cmu*mu + e != 0 for the ODD symbol mu.  If cmu*mu0 + e == 0 for an
    admissible host value mu0 (odd, >=1, 3∤mu0 — mu is always the odd part
    of 6k+4, hence not divisible by 3), the generic decision is wrong for
    that host.  mu0=1 is realized by the excursion host of EVERY w (mu=1
    iff M = 3w-1... i.e. U = 3w exactly) and by on-sequence spikes
    (k=10: 6k+4=64=2^6).  Scan all v2_val inputs of a 20000-walk.
(d) Required-margin computation: for each v2_val call, the true decision is
    safe at margin m iff s < m + v2(cM); report max(s - v2(cM)) over calls.
(e) Concrete transfer: at the smallest-margin hosts actually occurring in
    E(1,5000) (margins 20, 58, 91...), compare the CONCRETE cascade segment
    (fires inside the spike replay, from the excursion run) with the pure
    integer walk with base U = u_host (ground truth replay), fire by fire.
"""
import sys, time
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
import finaladv_0_core as C
import finaladv_1_levels as F1
import agentB_mu


def walker_stream(N, margin):
    agentB_mu.MARGIN = margin
    w = agentB_mu.Walker(N + 50)
    out = []
    guard = 0
    while w.maxpos < N and guard < 20 * N + 1000:
        r = w.step()
        guard += 1
        if r[0] == 'C':
            lb = w.events[-1][1]
            rho = lb[1] if lb[0] == 'R' else (lb[2] if lb[0] == 'M' else None)
            out.append((rho, r[1]))
    return out, guard


def admissible_mu(mu0):
    return mu0 >= 1 and mu0 % 2 == 1 and mu0 % 3 != 0


def scan_vanishing(N):
    """patch v2_val to log inputs; walk; flag vanishing admissible mu0."""
    orig = agentB_mu.v2_val
    log = []

    def spy(v):
        log.append(v)
        return orig(v)
    agentB_mu.v2_val = spy
    agentB_mu.MARGIN = 900
    try:
        w = agentB_mu.Walker(N + 50)
        guard = 0
        while w.maxpos < N and guard < 20 * N + 1000:
            w.step()
            guard += 1
    finally:
        agentB_mu.v2_val = orig
    bad = []
    monly = 0
    req = -10 ** 9   # max over calls of (s - v2(cM)); safe iff margin > req
    for v in log:
        a = agentB_mu.fv2(v.cmu)
        b = agentB_mu.fv2(v.e)
        if v.cmu == 0 and v.e == 0:
            monly += 1
            continue
        if a is not None and b is not None and a == b:
            continue    # tie (would have raised)
        s = a if b is None else (b if a is None else min(a, b))
        cm = agentB_mu.fv2(v.cM) if v.cM != 0 else None
        if cm is not None:
            req = max(req, s - cm)
        if v.cmu != 0:
            mu0f = -(v.e / v.cmu) if v.e != 0 else None
            if mu0f is not None and mu0f.denominator == 1:
                mu0 = int(mu0f)
                if admissible_mu(mu0):
                    bad.append((mu0, v.cM, v.cmu, v.e))
    return log, monly, bad, req


def main():
    t0 = time.time()
    kpos, jpos, _, _ = F1.build_kpos()

    print('=== (a) margin census on E(1,5000) ===')
    eng = C.Engine(4, C.E_entries(1, 5000))
    hosts = []
    while not eng.done():
        ev = eng.step()
        if ev['type'] == 'C' and ev['bl'][0] == 'H' and ev['j'] >= 5:
            hosts.append((ev['bl'][1], ev['j'], ev['bl'][1] - ev['j'], ev['u']))
    mg = sorted(set(h[2] for h in hosts))
    print('spike hosts: %d; margins p-J: min=%d, small ones=%s, max=%d'
          % (len(hosts), mg[0], mg[:8], mg[-1]))
    print('hosts with margin in {12,20,50}: %s'
          % ([h[:3] for h in hosts if h[2] in (12, 20, 50)],))
    deepest = max(hosts, key=lambda h: h[1])
    print('deepest top spike: p=%d J=%d margin=%d' % deepest[:3])

    print('=== (b) MARGIN-patch equivalence of agentB walker ===')
    base, _ = walker_stream(4000, 900)
    for m in (50, 20, 12, 8, 4, 2, 1):
        s, _ = walker_stream(4000, m)
        print('  MARGIN=%-4d vs 900 to N=4000: identical=%s (%d fires)'
              % (m, s == base, len(s)))
    s900, st = walker_stream(20000, 900)
    s1, _ = walker_stream(20000, 1)
    print('  MARGIN=1 vs 900 to N=20000: identical=%s (%d steps, %d fires)'
          % (s900 == s1, st, len(s900)))

    print('=== (c)+(d) vanishing-mu scan + required margin, N=20000 ===')
    log, monly, bad, req = scan_vanishing(20000)
    print('v2_val calls=%d; M-only (margin-SENSITIVE) calls=%d'
          % (len(log), monly))
    print('required margin (max s - v2(cM) over calls): %d  '
          '(walker sound for all true margins > %d)' % (req, req))
    if bad:
        print('VANISHING ADMISSIBLE MU0 FOUND: %s' % (bad[:10],))
        # is any bad mu0 realized on-sequence (spike hosts) or by excursion?
        onseq = set()
        for p in kpos:
            j = jpos[p]
            if j >= 5:
                onseq.add((6 * kpos[p] + 4) >> j)
        hit = [mu0 for (mu0, cM, cmu, e) in bad if mu0 == 1 or mu0 in onseq]
        print('on-sequence spike mu values (first 12): %s'
              % (sorted(onseq)[:12],))
        print('bad mu0 realized on-sequence or by excursion(mu=1): %s'
              % (sorted(set(hit)),))
    else:
        print('no vanishing admissible mu0 in any v2_val input: '
              'generic decisions valid for every host mu in range')

    print('=== (e) concrete transfer at smallest-margin hosts ===')
    for target_margin in (20, 58, 91):
        host = [h for h in hosts if h[2] == target_margin][0]
        p, J, mg_, u_host = host
        # concrete: rerun E(1,5000), collect fires from this spike until the
        # host level resumes (next H-fire at position > p)
        eng2 = C.Engine(4, C.E_entries(1, 5000))
        seg = []
        active = False
        while not eng2.done():
            ev = eng2.step()
            if ev['type'] != 'C':
                continue
            if ev['bl'] == ('H', p) and ev['j'] == J:
                active = True
            if active:
                seg.append(ev)
                if ev['bl'][0] == 'H' and ev['bl'][1] > p:
                    break
        # pure walk with base u_host
        eng3 = C.Engine(u_host + 1, ((u_host << a, ('H', a))
                                     for a in range(J + 40)))
        wseg = []
        while eng3.maxpos < J + 30:
            ev = eng3.step()
            if ev['type'] == 'C':
                wseg.append(ev)
        # compare: concrete sub-fires (b = m of this spike's cid) vs walk H-fires
        cid = seg[0]['cid']
        csub = [e for e in seg if e['bl'][0] == 'm' and e['bl'][1] == cid]
        wsub = [e for e in wseg if e['bl'][0] == 'H' and e['bl'][1] <= J - 2]
        posm = [e['bl'][2] for e in csub]
        posw = [e['bl'][1] for e in wsub]
        print('  margin %3d host (p=%d, J=%d): sub-fires concrete at %s, '
              'walk at %s; x/j EQUAL=%s'
              % (target_margin, p, J, posm, posw,
                 posm == posw and len(csub) == len(wsub)
                 and all(a['x'] == b['x'] and a['j'] == b['j']
                         for a, b in zip(csub, wsub))))
        # resumption: next H-fire after spike = table transition
        nxt = [e for e in seg if e['bl'][0] == 'H' and e['bl'][1] > p][0]
        dp = nxt['bl'][1] - p
        dk = (nxt['x'] - 3 * (1 << nxt['bl'][1]) * 3 - 4) // 6 - kpos[p]
        print('    resumption: dp=%d dk=%d  (report table for j=%d: %s)'
              % (dp, dk, J, C.REPORT_TABLE.get(J)))
    print('elapsed %.1fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
