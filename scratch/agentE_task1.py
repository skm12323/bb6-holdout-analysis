"""agentE_task1.py -- Task 1: reachable (level, rho) set from exact symbolic E(w,v).

Runs E(w,v) exactly and symbolically (single-symbol affine forms in u, w = 2u+1,
T_list/encode from verify_r8) for v = 1..VMAX (default 600).  At every
canonical A-odd state it collects
    (level = r+1, rho := d mod 256  [and (d+3) mod 256], kap class,
     Delta = d - (3t+1), t).
Canonical = encode() success (r >= 2) plus short-canonical r in {0,1} tracked
statefully from their births (E-macros at r in {2,3} give r-2; chain children
with sp = v2(q0) <= 2 give r = 1) -- auditor-2's 'enc'/'short' tags.
At every fire with v2(q0) >= 8 (uniform in w) it records the full deep context
(r, level, sp, child kap class, j = v2(H)).

Outputs: R(L) for each level <= 10, joint (L, rho) statistics, the deep-fire
census, and the claim check "(L <= 5, rho = -3 mod 256) never occurs"
(rho = -3 mod 256 in template convention, i.e. d = 253 mod 256, i.e.
(d+3) mod 256 = 0 in the task's rho convention).  Writes agentE_R.json.
"""
import os
import sys
import json
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from agentE_lib import (Undecided, Halt, add, sc, sub, par, half, v2f, halfn,
                        Z0, T_list, encode)


def main(vmax):
    t_start = time.time()
    joint = defaultdict(int)      # (Lcap, rho_d) -> count     rho_d = d mod 256
    joint3 = defaultdict(int)     # (Lcap, rho3)  -> count     rho3 = (d+3) mod 256
    rho_sets = defaultdict(set)   # true level -> set(rho_d)
    fire_tag = defaultdict(int)   # (tag, r) -> count
    kapc = defaultdict(int)       # (kap const mod 128, ucoeff%128==0) -> count
    dmin = {}                     # level -> min Delta
    dmax = {}                     # level -> max Delta
    tmaxL = defaultdict(int)      # level -> max t at fire
    firesL = defaultdict(int)     # capped level -> fire count
    deep = []
    glue_deep_n = 0
    glue_deep_ex = []
    bad_uc = 0                    # fires where d has nonzero u-coefficient
    birth_fail = 0                # short-canonical birth tracker mismatches
    undec = []
    halts = []
    total_steps = 0
    fires = 0
    for v in range(1, vmax + 1):
        w3 = (6, 3)
        L = [add(w3, (0, 1))] + [sc(w3, 1 << i) for i in range(v - 1)] + \
            [add(sc(w3, 1 << (v - 1)), (0, -1))]
        t = 0
        short = None      # (H, d, r, kap) if current state is short-canonical
        try:
            while len(L) > 1:
                enc = encode(L) if len(L) >= 3 else None
                H = d = r = kap = None
                tag = None
                if enc is not None:
                    H, d, r, kap = enc
                    tag = 'c'
                elif short is not None:
                    H, d, r, kap = short
                    tag = 's'
                fire_sp = None
                fire_op = None
                fire_cpr = None
                pA = None
                if tag is not None:
                    A = add(H, d)
                    pA = par(A)
                    if pA == 1:
                        fires += 1
                        lev = r + 1
                        lc = min(lev, 11)
                        if d[0] != 0:
                            bad_uc += 1
                        dc = d[1]
                        rho_d = dc % 256
                        joint[(lc, rho_d)] += 1
                        joint3[(lc, (dc + 3) % 256)] += 1
                        rho_sets[lev].add(rho_d)
                        fire_tag[(tag, r)] += 1
                        firesL[lc] += 1
                        Dl = dc - (3 * t + 1)
                        if lev not in dmin or Dl < dmin[lev]:
                            dmin[lev] = Dl
                        if lev not in dmax or Dl > dmax[lev]:
                            dmax[lev] = Dl
                        if t > tmaxL[lev]:
                            tmaxL[lev] = t
                        if kap is not None:
                            kapc[(kap[1] % 128, kap[0] % 128 == 0)] += 1
                        b = L[1]
                        c = L[2] if len(L) > 2 else Z0
                        q0 = add(A, b, b, (0, 3))
                        sp = v2f(q0)
                        fire_sp = sp
                        fire_op = fire_cpr = None
                        if sp <= 2:
                            fire_op = halfn(q0, sp)
                            fire_cpr = add(c, half(add(A, (0, 1))))
                        if sp >= 8:
                            o_p = halfn(q0, sp)
                            cpr = add(c, half(add(A, (0, 1))))
                            kapn = sub(cpr, sc(o_p, 1 << (sp - 1)))
                            deep.append({
                                'v': v, 't': t, 'tag': tag, 'r': r, 'L': lev,
                                'rho_d': rho_d, 'sp': sp, 'j': v2f(H),
                                'kapn_c128': kapn[1] % 128,
                                'kapn_u128ok': kapn[0] % 128 == 0,
                                'kapn_c2048': kapn[1] % 2048,
                                'kapn_u2048ok': kapn[0] % 2048 == 0,
                                'ok_op': (o_p[0] >= 0 and o_p[1] >= 3),
                            })
                else:
                    # odd glue state: deep census only
                    if L[0][0] % 2 == 0 and L[0][1] % 2 == 1:
                        b = L[1] if len(L) > 1 else Z0
                        q0 = add(L[0], b, b, (0, 3))
                        if v2f(q0) >= 8:
                            glue_deep_n += 1
                            if len(glue_deep_ex) < 20:
                                glue_deep_ex.append((v, t))
                # ---- one exact symbolic step; track short-canonical births
                pH, pd, pr, pkap, ptag, ppA = H, d, r, kap, tag, pA
                L = T_list(L)
                t += 1
                total_steps += 1
                short = None
                if ptag is not None and ppA == 1:
                    # chain birth: the child frame Phi_sp(o'; K'; Z')
                    if fire_sp == 1:
                        # no pushes: child = [o'+1, c', Z] -> r=0 short
                        short = (fire_op, (0, 1), 0, sub(fire_cpr, fire_op))
                        if L[0] != add(fire_op, (0, 1)) or L[1] != fire_cpr:
                            birth_fail += 1
                    elif fire_sp == 2:
                        # one push: child = [o'+1, o', c', Z] -> r=1 short
                        short = (L[1], sub(L[0], L[1]), 1, sub(L[2], sc(L[1], 2)))
                        if short[1] != (0, 1) or L[1] != fire_op or L[2] != fire_cpr:
                            birth_fail += 1
                elif ptag == 'c' and ppA == 0 and pr == 2:
                    # E-macro at r=2 -> short r=0: [4H+d+3, 4H+kap, Z]
                    short = (sc(pH, 4), add(pd, (0, 3)), 0, pkap)
                    if L[0] != add(sc(pH, 4), pd, (0, 3)) or L[1] != add(sc(pH, 4), pkap):
                        birth_fail += 1
                elif ptag == 'c' and ppA == 0 and pr == 3:
                    # E-macro at r=3 -> short r=1: [4H+d+3, 4H, J, Z]
                    if len(L) >= 3:
                        short = (L[1], sub(L[0], L[1]), 1, sub(L[2], sc(L[1], 2)))
                        if L[0] != add(sc(pH, 4), pd, (0, 3)) or L[1] != sc(pH, 4):
                            birth_fail += 1
        except (Undecided, Halt) as e:
            undec.append((v, t, repr(e)))
            continue

    # ---------------- summary ----------------
    print('== TASK 1: reachable-set scan, E(w,v) v=1..%d, symbolic w == ' % vmax)
    print('total top steps: %d; fires: %d; Undecided/Halt events: %d; '
          'd-ucoeff anomalies: %d; birth-tracker mismatches: %d'
          % (total_steps, fires, len(undec), bad_uc, birth_fail))
    if undec:
        print('  UNDECIDED/HALT EVENTS (first 10):', undec[:10])
    for L in sorted(rho_sets):
        rs = sorted(rho_sets[L])
        print('R(%d): |rho set| = %d' % (L, len(rs)))
    # claim: (L <= 5, rho = -3 mod 256)
    cl = sum(n for (Lc, rho), n in joint.items() if Lc <= 5 and rho == 253)
    cl3 = sum(n for (Lc, rho), n in joint3.items() if Lc <= 5 and rho == 0)
    print('CLAIM (L<=5, d = -3 mod 256 [= rho3 0]): canonical fires found: %d '
          '(template conv. count %d, task conv. count %d)' % (cl, cl, cl3))
    for rho in (241, 244, 247, 250, 253):
        row = [sum(n for (Lc, rr), n in joint.items() if Lc == L and rr == rho)
               for L in range(1, 11)]
        print('  fires with d mod 256 = %3d by level 1..10: %s' % (rho, row))
    # level stats
    print('fires per capped level:', {k: firesL[k] for k in sorted(firesL)})
    print('Delta min/max per level:',
          {L: (dmin.get(L), dmax.get(L)) for L in sorted(dmin)})
    print('t max per level:', {L: tmaxL[L] for L in sorted(tmaxL)})
    print('fire tag census (tag, r) top:',
          sorted(fire_tag.items(), key=lambda kv: -kv[1])[:15])
    print('kap class census (const mod 128, ucoeff 0 mod 128):',
          dict(kapc))
    # deep census
    by_r = defaultdict(int)
    by_sp = defaultdict(int)
    by_kc = defaultdict(int)
    for e in deep:
        by_r[e['r']] += 1
        by_sp[e['sp']] += 1
        by_kc[(e['tag'], e['r'], e['kapn_c128'], e['kapn_u128ok'],
               e['kapn_c2048'] if e['kapn_u2048ok'] else 'u-dep')] += 1
    print('DEEP fires (v2(q0)>=8, uniform in w): %d' % len(deep))
    print('  by r (run length at fire):', dict(sorted(by_r.items())))
    print('  by sp (child level):', dict(sorted(by_sp.items())))
    print('  child kap class census:', dict(by_kc))
    print('  all deep o_ok:', all(e['ok_op'] for e in deep))
    print('GLUE-shape deep moments (uniform): %d (examples %s)'
          % (glue_deep_n, glue_deep_ex[:5]))
    # persist
    out = {
        'vmax': vmax,
        'rho_sets': {str(L): sorted(rho_sets[L]) for L in rho_sets},
        'joint': {'%d,%d' % kv: n for kv, n in joint.items()},
        'joint3': {'%d,%d' % kv: n for kv, n in joint3.items()},
        'fire_tag': {'%s,%d' % kv: n for kv, n in fire_tag.items()},
        'dmin': {str(L): dmin[L] for L in dmin},
        'dmax': {str(L): dmax[L] for L in dmax},
        'tmaxL': {str(L): tmaxL[L] for L in tmaxL},
        'firesL': {str(L): firesL[L] for L in firesL},
        'deep': deep,
        'glue_deep_n': glue_deep_n,
        'counts': {'steps': total_steps, 'fires': fires, 'undec': len(undec),
                   'bad_uc': bad_uc, 'birth_fail': birth_fail,
                   'claim_L5_253': cl},
        'undec_ex': undec[:20],
    }
    with open(os.path.join(HERE, 'agentE_R.json'), 'w') as f:
        json.dump(out, f)
    print('wrote agentE_R.json  [%.1fs]' % (time.time() - t_start))


if __name__ == '__main__':
    VMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    main(VMAX)
