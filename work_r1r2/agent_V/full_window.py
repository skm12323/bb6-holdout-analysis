"""Full independent scan of the window certificate: certify(j,delta) for every
5 <= j < 2e7 and -12 <= delta <= 15.  Writes full_window.json; prints progress.
Expected: only (5,5) and (5,-11) fail.
"""
import json, sys, time
sys.path.insert(0, r'D:\math_cc\work_r1r2\agent_V')
import vlib

M = int(sys.argv[1]) if len(sys.argv) > 1 else 2 * 10**7
TABLE = r'D:\math_cc_astra\deep1\table_20000000.pkl' if M > 1000000 else \
        r'D:\math_cc_astra\deep1\table_1000000.pkl'
t0 = time.time()
T = vlib.Tab(TABLE, NS=1024)
print('loaded %.1fs' % (time.time() - t0), flush=True)
fail = []
cnt = 0
bytype = {'end1': 0, 'walk': 0}
t1 = time.time()
for j in range(5, M):
    for d in range(-12, 16):
        ok, st, w, r = vlib.certify_fast(T, j, d)
        cnt += 1
        if len(w) == 1:
            bytype['end1'] += 1
        else:
            bytype['walk'] += 1
        if not ok:
            fail.append((j, d, st, w[:8], r))
            if len(fail) < 10:
                print('FAIL', j, d, st, w[:8], r, flush=True)
    if j % 2000000 == 0:
        print('j', j, 'cnt', cnt, 'fails', len(fail), '%.1fs' % (time.time() - t1), flush=True)
out = dict(M=M, cnt=cnt, fail=fail[:50], nfail=len(fail), bytype=bytype,
           t=round(time.time() - t0, 1))
with open(r'D:\math_cc\work_r1r2\agent_V\full_window.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1)[:1000])
