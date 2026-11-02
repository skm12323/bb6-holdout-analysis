"""c7_family.py -- the unique uncertified c landing below T4 (NOTES.md §5): data for the BBBA family.

[B] (a) the chains m0 < 2*10^7 with X(m0-1) odd type b and omega(m0-1) = 17 (the only chains where the entry
        (m0, -1) NT-fails); for each, the exact certified walk from (m0, -1) and its a-output (5, 5);
    (b) automaton bookkeeping of the nested source S(Q): word Q ->b j1 ->b m0 ->b 17 ->a 5, class 5 at chain 5,
        automaton precision 16 there (descent 17 -> 5 drops x/2 of valuation 16), eps = 9;
    (c) the landing (5, 5) is not certifiable from any fixed number of bits below the needed ones: for lifts
        Theta - x = 5 + 2^16 e (e = 0..63) of a chain-5 representative, the gate output and the following word vary.
Writes c7_family.json.
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rwalk as R

T = R.Table()
m0s = []
for n in range(4, T.N):
    if T.odd[n] and T.typ[n] == 98 and R.v2(int(T.lam[n])) == 17:
        m0s.append(n + 1)
rows = []
for m0 in m0s:
    c = R.certify(T, m0, -1)
    rows.append(dict(m0=m0, ok=c['ok'], word=c['word'], aouts=[(a, b) for a, b in c["aouts"]],
                     has_55=any(a == 5 and b % 64 == 5 for a, b in c['aouts'])))
print(len(m0s), m0s[:5], all(r['ok'] and r['has_55'] for r in rows))
# (b) automaton: 1 -B-> 0 -B-> -1 -B-> -2 -A(17->5)-> 5; precision after the descent 17->5 is 16
phi = 1
for L in 'BBB':
    phi -= 1
assert phi == -2
k17 = int(T.tau[16]) // 2
assert T.typ[16] == 97 and T.odd[16] and k17 == 6
assert 1 + R.v2(phi + 3 * k17) == 5
phi = 3 - phi
assert phi == 5
# (c) dependence of the chain-5 bare tie on high bits: representative x = 2^5 * u, Theta = x + 5 + 2^16 e
var = []
for u in (1, 3, 5, 7):
    for e in range(64):
        x = 32 * u; th = x + 5 + (e << 16)
        st, w, r, ao, nt = R.tail(T, x, th, 10 ** 6)
        var.append((u, e, tuple(w[:6]), st))
words = sorted({v[2] for v in var})
print('distinct words from (5, 5 + 2^16 e):', len(words), words[:8])
lt = [m0 for m0 in m0s if m0 < 10 ** 7]
out = dict(m0_list=m0s, n_m0=len(m0s), all_certified_with_55=all(r['ok'] and r['has_55'] for r in rows),
           examples=rows[:3], automaton=dict(word='BBBA', phi_chain5=5, shift=3, precision_chain5=16, eps=9),
           m0_below_1e7=len(lt), m0_between_499997_and_1e7=[m for m in lt if m > 499997],
           high_bit_dependence=dict(n_lifts=len(var), distinct_words=len(words), sample=words[:12]),
           note='log2^(4) J ~ m0 for the constructed J (NOTES.md §5); K_clock has log2^(4) ~ 499997, T4 ~ 10^7.')
HERE.joinpath('c7_family.json').write_text(json.dumps(out, indent=1, default=str) + '\n', encoding='utf-8')
