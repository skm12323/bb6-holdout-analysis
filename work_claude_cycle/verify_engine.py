"""verify_engine.py -- check cyc.py's exact walk against two existing implementations.
(1) Calendar.projected_epoch (class-based projection, work_global_calendar) on S(J): word, types, status.
(2) work_global_ext/route_b/core.symexit (full (alpha,beta) pair map, independent pair walk) for small J.
(3) Event classification identities at every a-step (desc -> 1+v, gate -> j'>=j, cat -> j'=j-1).
Writes verify_engine.json.  PYTHONUTF8=1 python -B work_claude_cycle/verify_engine.py"""
import sys, json, random, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cyc import Cal, SJ, v2  # noqa

ROOT = HERE.parent


def word_of(J, steps):
    return [J] + [s['jn'] for s in steps]


def main():
    t0 = time.time()
    cal = Cal()
    res = dict(proj_checked=0, proj_fail=0, core_checked=0, core_fail=0, event_checks=0, nondescents=0)
    rnd = random.Random(20261102)
    Js = list(range(5, 30001)) + [rnd.randrange(2 ** 20, 2 ** 500) for _ in range(3000)]
    for J in Js:
        steps, st = SJ(cal, J)
        p = cal.C.projected_epoch(J, limit=64)
        w = word_of(J, steps)
        ok = (st == 'END' and p['status'] == 'closed' and p['word'] == w and
              p['types'] == ''.join(s['kind'] for s in steps) + cal.row(w[-1] - 1)['kind']) if w[-1] > 4 else \
            (st == 'END' and p['status'] == 'closed')
        if not ok and w[-1] <= 4:
            ok = (st == 'END' and p['status'] == 'closed' and p['word'][:len(w) - 1] == w[:-1])
        res['proj_checked'] += 1
        if not ok:
            res['proj_fail'] += 1
            if res['proj_fail'] < 5:
                print('proj mismatch', J, w, st, p)
        for s in steps:
            if s['kind'] == 'a':
                res['event_checks'] += 1
                v = v2(s['Th'] - 3 - 6 * s['k'] + 3 * s['k'])
                if s['ev'] == 'desc':
                    assert s['jn'] == 1 + v, (J, s)
                elif s['ev'] == 'gate':
                    assert s['jn'] >= s['j'], (J, s); res['nondescents'] += 1
                else:
                    assert s['jn'] == s['j'] - 1, (J, s); res['nondescents'] += 1
    # independent full pair map (route_b core) for small J
    sys.path.insert(0, str(ROOT / 'work_global_ext' / 'route_b'))
    import core
    X, tau, chainW = core.walk(700)
    T = {}
    for n in X:
        typ, A, Q, i = X[n]
        T[n] = dict(typ=typ, A=A, Y=(Q[0] if Q else None), tau=tau[n], eps=n - core.v2(A[0]),
                    odd=((A[0] + A[1]) % 2 == 1) if n >= 2 else False, W=chainW.get(n))
    for J in range(5, 600):
        out, st = core.symexit(J, T)
        steps, st2 = SJ(cal, J)
        res['core_checked'] += 1
        a = [o['j'] for o in out]
        b = [s['jn'] for s in steps]
        ok = (a == b and st == st2 and all(o['x'][1] == s['x'] for o, s in zip(out, steps)))
        if not ok:
            res['core_fail'] += 1
            if res['core_fail'] < 5:
                print('core mismatch', J, a, b, st, st2)
    res['seconds'] = round(time.time() - t0, 1)
    res['status'] = 'PASS' if res['proj_fail'] == 0 and res['core_fail'] == 0 else 'FAIL'
    print(res)
    json.dump(res, open(HERE / 'verify_engine.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
