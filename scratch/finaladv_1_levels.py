"""finaladv_1_levels.py — ANGLE 1 (level-tracking soundness) + ANGLE 4 (no other
chains) + part of ANGLE 2 (deepest spike in E(1,5000)).

A. Build kpos/jpos (universal k at each fire position) by PURE INTEGER
   simulation with U=1 (no symbolic frame, no agentB table).
B. Independent replication of run15's headline: labeled U=3 infinite walk to
   maxpos 20000 — count rho-in-kpos run-chain events, check invariant
   x = 3*2^rho*U + 6k_rho+4 and j = j_rho at EVERY nesting level.
C. Cross-check my walk's fire stream against agentB's symbolic mu-Walker.
D. E(1,600) / E(1,3000) / E(1,5000) labeled excursions: classify every fire
   by lineage; invariant + safety at all run fires; inventory of fires at
   rho<=3 and at run positions not in kpos (the zones run15 skips silently);
   seam-pushed (mixed-lineage) runs; deepest spike + margin; deep-nesting
   manual verification dump (5 consecutive nested fires, raw arithmetic).
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\scratch')
import finaladv_0_core as C

N_KPOS = 20100


def build_kpos():
    eng, fires = C.universal_walk(1, N_KPOS)
    kpos, jpos = {}, {}
    for e in fires:
        if e['bl'][0] != 'H':
            continue
        rho = e['bl'][1]
        if rho in kpos:
            raise AssertionError('double fire at rho=%d' % rho)
        kpos[rho] = (e['x'] - 3 * (1 << rho) - 4) // 6
        jpos[rho] = e['j']
    return kpos, jpos, eng.steps, eng.fires


def check_invariant(eng, ev, kpos, jpos, U0):
    """returns (status, detail) for a chain event; status in
    {'INV-OK','INV-FAIL','LOWPOS','OFFPOS','NONRUN'}"""
    bl = ev['bl']
    rho = C.fire_position(bl)
    if rho is None:
        return 'NONRUN', bl
    U = C.level_base_of(bl, eng, U0)
    if (ev['b'] != (U << rho)):
        return 'INV-FAIL', ('label/value mismatch', bl, ev['b'], U, rho)
    if rho <= 3:
        return 'LOWPOS', (bl, ev['x'])
    if rho not in kpos:
        return 'OFFPOS', (bl, ev['x'], rho)
    exp = 3 * (1 << rho) * U + 6 * kpos[rho] + 4
    if ev['x'] == exp and ev['j'] == jpos[rho]:
        return 'INV-OK', None
    return 'INV-FAIL', (bl, ev['x'], exp, ev['j'], jpos[rho])


def walk_infinite(U, N, kpos, jpos):
    """labeled infinite-run walk; returns stats"""
    eng = C.Engine(U + 1, ((U << a, ('H', a)) for a in range(N + 50)))
    stats = {'INV-OK': 0, 'INV-FAIL': 0, 'LOWPOS': 0, 'OFFPOS': 0, 'NONRUN': 0}
    fails, lowpos, offpos = [], [], []
    stream = []   # (rho_or_None, j) of EVERY fire, run or not
    while eng.maxpos < N:
        ev = eng.step()
        if ev['type'] != 'C':
            continue
        st, det = check_invariant(eng, ev, kpos, jpos, U)
        rho = C.fire_position(ev['bl'])
        stream.append((rho, ev['j']))
        if st in stats:
            stats[st] += 1
        if st == 'INV-FAIL':
            fails.append((ev['bl'], det))
        elif st == 'LOWPOS':
            lowpos.append((ev['bl'], det[1]))
        elif st == 'OFFPOS':
            offpos.append(det)
    return eng, stats, fails, lowpos, offpos, stream


def classify_excursion(w, v, kpos, jpos, dump_cid=None):
    eng = C.Engine(3 * w + 1, C.E_entries(w, v))
    U0 = 3 * w
    cls = {'H': 0, 'm': 0, 'd': 0, 'T': 0, 'Z': 0}
    stats = {'INV-OK': 0, 'INV-FAIL': 0, 'LOWPOS': 0, 'OFFPOS': 0, 'NONRUN': 0}
    fails, lowpos, offpos = [], [], []
    minu = None
    seam_spikes = []       # chains with b in {d,T,Z} and j>=6 (push run>=5)
    mixed = {'n': 0, 'inv': 0}   # fires on runs pushed by seam chains
    spike_hosts = []       # (p, J, u, margin=p-J, depth) top-level spikes
    depth_of = {}          # cid -> nesting depth (1 = b is 'H')
    maxj = 0; maxj_ev = None
    dump = []
    while not eng.done():
        ev = eng.step()
        if ev['type'] != 'C':
            continue
        bl = ev['bl']
        cid = ev['cid']
        j = ev['j']
        cls[bl[0]] += 1
        if minu is None or ev['u'] < minu:
            minu = ev['u']
        # depth
        if bl[0] == 'H':
            depth_of[cid] = 1
        elif bl[0] == 'm':
            depth_of[cid] = depth_of.get(bl[1], 0) + 1
        else:
            depth_of[cid] = 0
        if j > maxj:
            maxj = j; maxj_ev = ev
        if j >= 5 and bl[0] == 'H':
            spike_hosts.append((bl[1], j, ev['u'], bl[1] - j, depth_of[cid]))
        if bl[0] in ('d', 'T', 'Z') and j >= 6:
            seam_spikes.append((cid, bl, j))
        st, det = check_invariant(eng, ev, kpos, jpos, U0)
        if bl[0] == 'm' and eng.chain_bclass[bl[1]] in ('d', 'T', 'Z'):
            mixed['n'] += 1
            if st == 'INV-OK':
                mixed['inv'] += 1
        if st in stats:
            stats[st] += 1
        if st == 'INV-FAIL':
            fails.append((bl, det))
        elif st == 'LOWPOS':
            lowpos.append((bl, det[1]))
        elif st == 'OFFPOS':
            offpos.append(det)
        if dump_cid is not None and bl[0] == 'm' and bl[1] == dump_cid:
            dump.append(ev)
    return dict(eng=eng, cls=cls, stats=stats, fails=fails, lowpos=lowpos,
                offpos=offpos, minu=minu, seam_spikes=seam_spikes,
                mixed=mixed, spike_hosts=spike_hosts, maxj=maxj,
                maxj_ev=maxj_ev, ell=eng.steps, dump=dump, depth_of=depth_of)


def main():
    t0 = time.time()
    print('=== A. kpos from pure U=1 integer walk (independent) ===')
    kpos, jpos, wsteps, wfires = build_kpos()
    print('walk steps=%d fires=%d kpos positions=%d max=%d'
          % (wsteps, wfires, len(kpos), max(kpos)))
    # table self-consistency of my kpos with the REPORT's printed (dk,dp) rows:
    bad = []
    ps = sorted(kpos)
    for a, b in zip(ps, ps[1:]):
        j = jpos[a]
        if j in C.REPORT_TABLE:
            dk, dp = C.REPORT_TABLE[j]
            if kpos[b] - kpos[a] != dk or b - a != dp:
                bad.append((a, b, j, kpos[b] - kpos[a], b - a))
        else:
            bad.append((a, b, j, 'NO TABLE ENTRY', None))
    print('kpos consecutive-gaps vs REPORT table (j<=20): %s'
          % ('ALL MATCH' if not bad else bad[:5]))

    print('=== B. labeled U=3 infinite walk to maxpos 20000 (replication of run15) ===')
    eng, stats, fails, lowpos, offpos, stream = walk_infinite(3, 20000, kpos, jpos)
    print('steps=%d fires=%d stats=%s' % (eng.steps, eng.fires, stats))
    print('run15 headline was: 6372 run-chain events, 0 failures, max j 14')
    if fails:
        print('INVARIANT FAILURES:', fails[:3])
    if lowpos:
        print('LOWPOS (rho<=3) run fires:', len(lowpos), lowpos[:5])
    if offpos:
        print('OFFPOS run fires (rho not a universal position):', len(offpos),
              offpos[:5])

    print('=== C. cross-check vs agentB symbolic mu-Walker (event streams) ===')
    import agentB_mu
    mw = agentB_mu.Walker(20050)
    mstream = []
    guard = 0
    while mw.maxpos < 20000 and guard < 20 * 20000 + 1000:
        r = mw.step()
        guard += 1
        if r[0] == 'C':
            lb = mw.events[-1][1]
            rho = lb[1] if lb[0] == 'R' else (lb[2] if lb[0] == 'M' else None)
            mstream.append((rho, r[1]))
    same = (mstream == stream)
    print('agentB walker steps=%d fires=%d; my fires=%d; full (rho|None,j) '
          'streams EQUAL=%s' % (guard, len(mstream), len(stream), same))
    if not same:
        for i, (a, b) in enumerate(zip(mstream, stream)):
            if a != b:
                print('first divergence at fire %d: agentB=%s mine=%s' % (i, a, b))
                break
    print('my walk: max j over all fires=%d (run15 reported 14)'
          % max(j for _, j in stream))

    print('=== D. labeled excursions (angle 4 classification + safety) ===')
    for (w, v) in [(1, 600), (1, 3000), (1, 5000), (3, 300), (5, 300)]:
        r = classify_excursion(w, v, kpos, jpos)
        print('E(%d,%d): ell=%d result=%s' % (w, v, r['ell'],
              'singleton' if r['eng'].done() else 'NOT DONE'))
        print('   b-classes H/m/d/T/Z:', r['cls'],
              'invariant:', r['stats'], 'min u:', r['minu'])
        if r['fails']:
            print('   FAILS:', r['fails'][:3])
        if r['lowpos']:
            print('   LOWPOS:', len(r['lowpos']), r['lowpos'][:3])
        if r['offpos']:
            print('   OFFPOS:', len(r['offpos']), r['offpos'][:3])
        if r['seam_spikes']:
            print('   SEAM SPIKES (b in d/T/Z, j>=6):', r['seam_spikes'][:5])
        print('   mixed-lineage run fires: %d, of which INV-OK: %d'
              % (r['mixed']['n'], r['mixed']['inv']))
        hs = r['spike_hosts']
        if hs:
            margins = sorted(set(h[3] for h in hs))
            print('   top-level spikes: %d, j-set %s, margin(p-J) min=%d '
                  'all-small=%s' % (len(hs), sorted(set(h[1] for h in hs)),
                                    margins[0], margins[:6]))
        print('   max j over ALL fires: %d (b-label %s, depth %d)'
              % (r['maxj'], r['maxj_ev']['bl'],
                 r['depth_of'].get(r['maxj_ev']['cid'], -1)))
    print('=== E. deep nesting (angle 1 core ask) ===')
    deep_nesting(kpos, jpos)
    print('elapsed %.1fs' % (time.time() - t0))
    return kpos, jpos, stream, stats


def _fmt(n):
    s = str(n)
    if len(s) <= 66:
        return s
    return s[:33] + '...' + s[-33:] + '(%d digits)' % len(s)


def dump_event(ev, U_level, kpos, jpos, note=''):
    bl = ev['bl']
    rho = C.fire_position(bl)
    print('  %s bl=%s rho=%s' % (note, bl, rho))
    print('    A=%s' % _fmt(ev['A']))
    print('    b=%s' % _fmt(ev['b']))
    print('    c=%s' % _fmt(ev['c']))
    print('    x = A+2b+3 = %s' % _fmt(ev['x']))
    if rho is not None and rho in kpos and U_level is not None:
        exp = 3 * (1 << rho) * U_level + 6 * kpos[rho] + 4
        print('    U has %d bits; 3*2^%d*U + 6*k_rho+4 (k_rho=%d) = %s'
              % (U_level.bit_length(), rho, kpos[rho], _fmt(exp)))
        print('    x==expected: %s   j=%d (jpos[rho]=%s)  u>3: %s'
              % (ev['x'] == exp, ev['j'], jpos[rho], ev['u'] > 3))
    else:
        print('    (non-run/off-position fire) j=%d u>3: %s'
              % (ev['j'], ev['u'] > 3))


def deep_nesting(kpos, jpos):
    # --- E1: deepest spike REAL in E(1,5000)
    eng = C.Engine(4, C.E_entries(1, 5000))
    all_evs = []
    spike_ev = None
    while not eng.done():
        ev = eng.step()
        if ev['type'] == 'C':
            all_evs.append(ev)
            if ev['bl'][0] == 'H' and ev['j'] >= 12:
                if spike_ev is None or ev['j'] > spike_ev['j']:
                    spike_ev = ev
    sp = spike_ev
    print("E1. deepest real spike in E(1,5000): j=%d at %s"
          % (sp['j'], sp['bl']))
    print('    spike u has %d bits (u=%d ...)' % (sp['u'].bit_length(),
                                                  sp['u'] >> (sp['u'].bit_length() - 30)))
    cid = sp['cid']
    nested = [e for e in all_evs if e['bl'][0] == 'm' and e['bl'][1] == cid]
    print('    nested fires in its replay: %d, at sub-positions %s'
          % (len(nested), [e['bl'][2] for e in nested]))
    idx0 = all_evs.index(nested[0])
    for i, e in enumerate(all_evs[idx0:idx0 + len(nested) + 3]):
        if e['bl'][0] == 'm' and e['bl'][1] == cid:
            dump_event(e, eng.chain_u[cid], kpos, jpos,
                       note='[real depth-2 fire]')
        else:
            Ul = 3 if e['bl'][0] == 'H' else None
            dump_event(e, Ul, kpos, jpos, note='[exit-window fire]')
    # --- E2: synthetic multi-hop nesting (L0/prefix-universality justified)
    print('E2. synthetic nesting hops (walk with base U = u of a spike = '
          'replay prefix of any spike with that u and j>=702):')
    U = sp['u']
    for hop in range(1, 4):
        e = C.Engine(U + 1, ((U << a, ('H', a)) for a in range(760)))
        evs = []
        while e.maxpos < 700:
            ev = e.step()
            if ev['type'] == 'C':
                evs.append(ev)
        stats = {'INV-OK': 0, 'INV-FAIL': 0, 'LOWPOS': 0, 'OFFPOS': 0, 'NONRUN': 0}
        depth = {}
        for ev in evs:
            bl = ev['bl']
            d = 1 if bl[0] == 'H' else (depth.get(bl[1], 0) + 1
                                        if bl[0] == 'm' else 0)
            depth[ev['cid']] = d
            st, det = check_invariant(e, ev, kpos, jpos, U)
            stats[st] += 1
            if st == 'INV-FAIL':
                print('    HOP %d INVARIANT FAIL: %s %s' % (hop, bl, det))
        dh = {}
        for ev in evs:
            bl = ev['bl']
            d = 1 if bl[0] == 'H' else (depth.get(bl[1], 0) + 1
                                        if bl[0] == 'm' else 0)
            dh[d] = dh.get(d, 0) + 1
        print('  hop %d: U %d bits; total fires %d; fires by depth %s; %s'
              % (hop, U.bit_length(), len(evs), sorted(dh.items()), stats))
        # 5 consecutive fires at one m-level (deepest available), manual dump
        runs, order = {}, []
        for ev in evs:
            bl = ev['bl']
            if bl[0] == 'm':
                runs.setdefault(bl[1], []).append(ev)
                if len(runs[bl[1]]) == 5:
                    order.append(bl[1])
        deep_levels = [(cid, depth.get(cid, 0)) for cid in order]
        if order:
            cid5, d5 = max(deep_levels, key=lambda t: t[1])
            print('    5 consecutive nested fires inside chain %d '
                  '(level depth %d), manual dump:' % (cid5, d5 + 1))
            for i, ev in enumerate(runs[cid5][:5]):
                dump_event(ev, e.chain_u[cid5], kpos, jpos,
                           note='  [hop%d depth%d fire %d]' % (hop, d5 + 1, i))
        # hop to the first spike (j>=5) at the HOST level
        nxt = None
        for ev in evs:
            if ev['bl'][0] == 'H' and ev['j'] >= 5:
                nxt = ev['u']
                print('    hop %d -> %d from host spike at %s (j=%d)'
                      % (hop + 1, hop + 1, ev['bl'], ev['j']))
                break
        if nxt is None:
            print('    no host spike to hop further')
            break
        U = nxt


if __name__ == '__main__':
    main()
