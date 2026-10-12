"""reviewB_probe3.py -- ATTACK 3: the j > 1200 hole.

agentB's per-J abstract transition verifier was run for j = 1..1200 ("ALL OK").
Here we extend it: j = 1201..1400 and j = 2000, 5000.  If verification cannot
be run beyond the table (guard/cap/split explosion), that IS the gap; we then
quantify which v it affects via the structural bound j_rho <= 3 log2 rho + 3.
"""
import sys, time
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_run7 import verify
from agentB_lib import v2i
from reviewB_lib import tab

def main():
    # 1) timing calibration
    for j in (100, 600, 1200):
        t0 = time.time()
        res, err = verify(j)
        print('j=%4d: %.2fs res=%s err=%s' % (j, time.time() - t0, res, err))
        sys.stdout.flush()
    # 2) the extension
    t_all = time.time()
    bad = []
    for j in list(range(1201, 1401)) + [2000, 5000, 10000, 20000]:
        t0 = time.time()
        res, err = verify(j)
        dt = time.time() - t0
        if err or dt > 300:
            bad.append((j, err or 'timeout', dt))
            print('j=%4d: %.1fs PROBLEM: %s' % (j, dt, err))
            if len(bad) > 5:
                break
        else:
            if j % 25 == 0 or j in (1201, 2000, 5000):
                print('j=%4d: %.1fs OK (%s)' % (j, dt, res))
                sys.stdout.flush()
    print('extension j=1201..1400,2000,5000: %s (%.1fs total)'
          % ('ALL OK' if not bad else bad[:6], time.time() - t_all))
    # 3) quantify the hole: structural bound j <= 3 log2 rho + 3
    #    j > 1200 requires rho > 2^((1200-3)/3) = 2^399 (structural),
    #    and via actual k: k >= (2^(j-1)-2)/3, rho >= k/0.4465.
    import math
    for J in (1200, 1201, 2000, 5000):
        kmin = ((1 << (J - 1)) - 2) // 3
        rho_lin_log = math.log10(kmin) - math.log10(0.4465)
        rho_cub = 1 << ((J - 3) // 3)
        print('J=%d: min k=%d (log10 %.2f) -> rho >= 10^%.2f (linear bound) '
              'or 2^%d (cubic bound)' % (J, kmin, math.log10(kmin),
                                         rho_lin_log, (J - 3) // 3))
    # max j reached on the universal sequence up to position 4.4e3 / 2e5 / 4e5
    p, k = 4, 1
    jmax = 0
    while p < 400000:
        j = 1 + v2i(3 * k + 2)
        jmax = max(jmax, j)
        dk, dp = tab(j)
        p += dp
        k += dk
        if p in (4400, 200000, 400000):
            print('at p=%d: max j on universal seq = %d' % (p, jmax))

if __name__ == '__main__':
    main()
