"""reviewB_probe5.py -- ATTACK 5: margins arithmetic (section 4).

(i) "p - J >= 900 whenever J >= 60 and p >= 2^18": derive from the two k-bounds
    (machine linear k<=0.4465p verified p<4e5; structural cubic k<=rho^3):
        p >= ((2^J-4)/6)/bound.  Check numerically for J=60,61; find the true
        minimum J for which the cubic bound forces p-J >= 900; check whether
        J>=60 alone already forces p >= 2^18.
(ii) what the abstract verifiers actually need: ctx.p >= max(200,j+100), i.e.
    v2(P-part) >= 100 > max small-part v2; check that the real events satisfy
    p - j >= 100 via the structural bound j_rho <= 3 log2 rho + 3 (for which
    minimum rho?), and via the measured j on the universal sequence.
(iii) "min v2(cM) = +3, never degrades": run the mu-walker with instrumentation
    of v2(cM) over every chain u, to position 4000 (and beyond to 20000), and
    also over nested levels.
"""
import sys, time, math
from fractions import Fraction as Fr
sys.path.insert(0, r'D:\math_cc\scratch')
import agentB_mu as mu
from agentB_mu import Walker, Val, Amb
from agentB_lib import v2i

def fv2f(fr):
    if fr == 0:
        return None
    return v2i(abs(fr.numerator)) - v2i(abs(fr.denominator))

def main():
    # (i)
    print('(i) margin p-J from the two k-bounds:')
    cbrt6 = 6 ** (1.0 / 3.0)
    for J in (33, 40, 45, 50, 55, 58, 59, 60, 61, 64):
        pmin_lin = ((1 << J) - 4) / 6 / 0.4465
        pmin_cub = 2 ** (J / 3.0) / cbrt6
        print('    J=%2d: linear-bound p >= %.3g (margin %.3g), '
              'cubic-bound p >= %.4g (margin %.4g) -> p>=2^18 %s'
              % (J, pmin_lin, pmin_lin - J, pmin_cub, pmin_cub - J,
                 'yes' if pmin_cub >= 262144 else ('lin-yes' if pmin_lin >= 262144 else 'NO')))
    print('    NOTE: linear bound (k<=0.4465p) is machine-verified only p<4e5,')
    print('    where J<=20 spikes live; J>=60 needs the WRITTEN cubic bound.')
    # (ii)
    print('(ii) verifier p-floor vs real events:')
    print('    run7/run13 assume p >= max(200, j+100).')
    for rho in (200, 1000, 2000, 2001, 10**6, 2**20):
        jstruct = 3 * math.log2(rho) + 3
        print('    rho=%8d: structural j_rho <= %.1f, rho-j >= %.1f'
              % (rho, jstruct, rho - jstruct))
    # measured j on the universal sequence vs p (max j for given p-window)
    from reviewB_lib import tab
    p, k = 4, 1
    jmax = 0
    marks = {}
    while p < 400000:
        j = 1 + v2i(3 * k + 2)
        jmax = max(jmax, j)
        for m in (2000, 20000, 100000, 400000):
            if p >= m and m not in marks:
                marks[m] = (jmax, p - jmax)
        dk, dp = tab(j)
        p += dp
        k += dk
    print('    measured: max j and min p-j on universal seq:',
          {m: marks[m] for m in sorted(marks)})
    # (iii) walker: min v2(cM) over chain u's, nested too
    for N in (4000, 20000):
        t0 = time.time()
        try:
            w = Walker(N + 50)
            minv = 10 ** 9
            argmin = None
            steps = 0
            while w.maxpos < N:
                w.step()
                steps += 1
                (cid, lb, j, u) = w.events[-1] if w.events else None, None, None, None
                if w.events:
                    (cid, lb, j, u) = w.events[-1]
                    c = u.cM
                    if c != 0:
                        v = fv2f(c)
                        if v < minv:
                            minv, argmin = v, (cid, lb)
            print('(iii) walker N=%d: %d steps, %d chains, min v2(cM) over '
                  'chain u = %+d at %s [%.1fs]'
                  % (N, steps, len(w.events), minv, argmin, time.time() - t0))
        except Amb as ex:
            print('(iii) walker N=%d AMBIGUITY: %s' % (N, ex))

if __name__ == '__main__':
    main()
