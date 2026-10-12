"""V1 scan: exact dynamics from E(w,v), w in {1,3,5,7}, v = 1..400.

Verifies (all measured on the concrete run with frame tracking):
 (1a) at every canonical odd state with r >= 2: window L[3:] =
      [4H, 8H, .., 2^{r-1}H, J] + Z, where Z equals the caller's *remaining*
      window W[j:] (the real content of "no other shapes");
 (1b) a <= 2 for nested excursions (entries absorbed), split by fire tag;
 (1c) margin v2(H) - v2(d+3) >= 1 at every canonical fire with t >= 1;
 (1d) Delta = d - (3t+1) in {0} u {negative odd} at every canonical fire.
 Also collected:
 (2b) V2 in dynamics: at fires with r >= 1 and v2(H) >= 11,
      v2(q0) >= 8  <=>  (d+3) % 256 == 0;
      and every fire-state H has the form 3*odd*2^j;
 (4b) V4 occurrence data: classes of kap / Z0 and of the child kap
      kap_child = c' - q0/2 at r=0, r=1, r>=2 fires (deep and shallow),
      family = {0,-1 mod 2^11} u {-2 mod 2^7}.
"""
import sys, time
from collections import defaultdict
sys.path.insert(0, r'D:\math_cc\scratch')
from review2_engine import run_tracked, excursion_start, v2, top

S = defaultdict(int)
EX = defaultdict(list)
SETS = defaultdict(set)
AHIST = defaultdict(int)


def fam(x):
    return (x % 2048 in (0, 2047)) or (x % 128 == 126)


def sink(kind, info):
    S['ev_' + kind] += 1
    if kind == 'fire':
        L, H, d, r, kap = info['L'], info['H'], info['d'], info['r'], info['kap']
        sp, t = info['sp'], info['t']
        S['fires'] += 1
        S['fires_tag_' + info['tag']] += 1
        S['rhist_r%d' % r] += 1
        S['sphist_%d' % sp] += 1
        S['sphist_max'] = max(S['sphist_max'], sp)
        if r >= 2:
            win = L[3:]
            okw = (len(win) >= r - 1
                   and all(win[i] == (H << (i + 2)) for i in range(r - 2))
                   and win[r - 2] == (H << r) + kap)
            if not okw:
                S['winbad'] += 1
                if len(EX['winbad']) < 5:
                    EX['winbad'].append((r, [x // H if H else 0 for x in win[:8]]))
            zb = (win[r - 1:] == info['W'][info['j_after']:])
            if not zb:
                S['zbad'] += 1
                if len(EX['zbad']) < 5:
                    EX['zbad'].append(('r', r, 'winTail', [x for x in win[r - 1:r + 3]],
                                       'Wj', [x for x in info['W'][info['j_after']:info['j_after'] + 3]]))
        jH = v2(H)
        s2 = v2(d + 3)
        if d + 3 == 0:
            S['dplus3_zero'] += 1
        if t >= 1:
            if jH - s2 < S['min_margin']:
                S['min_margin'] = jH - s2
        else:
            S['fires_t0'] += 1
        if (H >> jH) % 6 != 3:
            S['Hform_bad'] += 1
            if len(EX['Hform']) < 5:
                EX['Hform'].append((H, jH))
        Delta = d - (3 * t + 1)
        if not (Delta == 0 or (Delta < 0 and Delta % 2 in (1, -1))):
            S['deltabad'] += 1
            if len(EX['deltabad']) < 8:
                EX['deltabad'].append((r, d, t, Delta))
        S['delta_min'] = min(S['delta_min'], Delta)
        # ---- V2 dynamics check (r >= 1: b = H so q0 = 3H + d + 3) ----
        if r >= 1 and jH >= 11:
            S['v2chk'] += 1
            lhs = sp >= 8
            rhs = ((d + 3) & 255) == 0
            if lhs != rhs:
                S['v2bad'] += 1
                if len(EX['v2bad']) < 5:
                    EX['v2bad'].append((r, d, jH, sp))
        # ---- V4 occurrence data ----
        A = L[0]
        c = L[2] if len(L) > 2 else 0
        ck_exact = c + (A + 1) // 2 - info['q0'] // 2
        if r >= 2:
            ck_alg = H - 1
        elif r == 1:
            ck_alg = H + kap - 1
        else:
            Z0 = c
            ck_alg = Z0 - H - kap - 1
        if ck_alg != ck_exact:
            S['ck_alg_bad'] += 1
        ck = ck_exact
        deep = sp >= 8
        SETS['kap_r%d' % r].add(kap % 2048)
        SETS['kap128_r%d' % r].add(kap % 128)
        if r == 0:
            S['r0_fires'] += 1
            SETS['Z0_r0'].add(c % 2048)
        if deep:
            S['deep_fires'] += 1
            S['deep_r%d' % r] += 1
            SETS['deep_child_r%d' % r].add(ck % 2048)
            SETS['deep_kap_r%d' % r].add(kap % 2048)
            if r == 0:
                SETS['deep_Z0_r0'].add(c % 2048)
            if not fam(ck):
                S['deep_outside'] += 1
                if len(EX['deep_outside']) < 8:
                    EX['deep_outside'].append((r, kap % 2048, c % 2048, sp, ck % 2048, H % 2048))
            if r in (0, 1) and kap % 128 == 126:
                S['deep_short_neg2'] += 1
                if len(EX['deep_short_neg2']) < 8:
                    EX['deep_short_neg2'].append((r, kap, c % 2048, sp, ck, H % 2048))
    elif kind == 'pop':
        if not info['root']:
            S['pops'] += 1
            a = info['a']
            AHIST[(info['tag'], a)] += 1
            for tag in ('enc', 'short'):
                if info['tag'] == tag:
                    S['amax_' + tag] = max(S['amax_' + tag], a)
        SETS['frame_kap_class'].add(info['kap0'] % 2048)
    elif kind == 'coinc':
        S['coinc'] += 1
    elif kind == 'reclass':
        S['reclass'] += 1


def main():
    t0 = time.time()
    S['min_margin'] = 999
    S['delta_min'] = 1 << 60
    tot_ell = 0
    for w in (1, 3, 5, 7):
        for v in range(1, 401):
            res = run_tracked(excursion_start(w, v), 3 * w, 1, -1, v, sink, 200000)
            assert res['end'] == 'done', (w, v, res)
            assert res['head'] == (3 * w << v) + 3 * res['steps'], (w, v, res)
            tot_ell += res['steps']
        print('  w=%d done [%.1fs]' % (w, time.time() - t0), file=sys.stderr)
    print('=== V1 scan: w in {1,3,5,7}, v = 1..400 ===')
    print('excursions: 1600, total top() steps: %d, fires: %d (enc %d / short %d), pops(nested): %d'
          % (tot_ell, S['fires'], S['fires_tag_enc'], S['fires_tag_short'], S['pops']))
    print('r-histogram at fires:', {k: v for k, v in sorted(S.items()) if k.startswith('rhist_')})
    print('sp (level) histogram:', {k: v for k, v in sorted(S.items()) if k.startswith('sphist_') and k != 'sphist_max'},
          'max sp =', S['sphist_max'])
    print('(1a) window-shape violations winbad =', S['winbad'], '; Z-boundary violations zbad =', S['zbad'],
          '; examples:', dict(EX['winbad']), dict(EX['zbad']))
    print('(1b) a histogram (tag, a):', dict(AHIST), '; amax enc =', S['amax_enc'], 'amax short =', S['amax_short'])
    print('(1c) min margin v2(H)-v2(d+3) over fires t>=1 =', S['min_margin'],
          '; fires with t=0:', S['fires_t0'], '; d+3 == 0 occurrences:', S['dplus3_zero'])
    print('(1d) Delta violations =', S['deltabad'], '; min Delta =', S['delta_min'], '; examples:', EX['deltabad'])
    print('contract coinc-suffix matches skipped:', S['coinc'], '; short-state reclassifications:', S['reclass'])
    print('(2b) H-form violations (not 3*odd*2^j):', S['Hform_bad'], EX['Hform'],
          '; V2 dyn checks:', S['v2chk'], 'mismatches:', S['v2bad'], EX['v2bad'])
    print('(4b) deep fires (sp>=8):', S['deep_fires'],
          {k: v for k, v in sorted(S.items()) if k.startswith('deep_r')})
    print('     deep fires with OUTSIDE-family child class:', S['deep_outside'], EX['deep_outside'])
    print('     deep r in {0,1} fires with parent kap == -2 mod 128:', S['deep_short_neg2'], EX['deep_short_neg2'])
    print('     kap classes (mod 2048) at fires: r0:', sorted(SETS['kap_r0']), ' r1:', sorted(SETS['kap_r1']))
    print('     kap mod 128 at r1 fires:', sorted(SETS['kap128_r1']), ' at r0 fires:', sorted(SETS['kap128_r0']))
    print('     Z0 classes (mod 2048) at r0 fires:', sorted(SETS['Z0_r0']))
    print('     deep child classes r0:', sorted(SETS['deep_child_r0']),
          ' r1:', sorted(SETS['deep_child_r1']), ' r>=2:', sorted(SETS['deep_child_r2']))
    print('     deep kap classes r0:', sorted(SETS['deep_kap_r0']), ' r1:', sorted(SETS['deep_kap_r1']))
    print('     deep Z0 classes r0:', sorted(SETS['deep_Z0_r0']))
    print('     algebraic child-kap identity mismatches:', S['ck_alg_bad'])
    print('frame kap0 classes (mod 2048) seen at pops:', sorted(SETS['frame_kap_class'])[:40],
          '... total', len(SETS['frame_kap_class']))
    print('elapsed %.1fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
