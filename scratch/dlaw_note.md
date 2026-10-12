# The Delta-law (main-line note, R8 second wave)

Notation: canonical mid-excursion states (H+d, H, 2H, ..., 2^(r-1)H, J, Z...), with
d = 3t+1+Delta at canonical time t (t = top steps since excursion start, counting the
nested-excursion durations). Delta = d - (3t+1) tracked through exact compositional runs
(w symbolic, uniform) of E(w,v), v = 2..2000 (dlaw.py).

## The law [Class-B, v <= 2000; exact transition table below]

Delta(t) = 0 except on windows starting at **t ≡ 40 or 82 (mod 128)**:

- at t = 40 + 128j (j >= 0): Delta -> -( (3k+1)*2^7 + 1 )   [created by an sp=2, a=0 fire]
- at t = 82 + 128j:          Delta -> -( (3k+1)*2^7 + 127 ) [created by an sp=1, a=1 fire]
  where k = j (block index); the window clears (Delta -> 0) 5 or 7 steps later
  (t ≡ 87 or 89 mod 128; sp=1 fires clear in 5, sp=4 in 7).

Verified transition table (all 42 events for v <= 2000, max |Delta| = 5247 = 41*128-1):
  t=40: 0->-129;  t=82: 0->-255;  t=87: -255->0;  t=168: 0->-513;  t=210: 0->-639;
  t=215: -639->0; t=296: 0->-897; t=338: 0->-1023; t=345: -1023->0; t=424: 0->-1281;
  t=466: 0->-1407; t=471: -1407->0; ... continuing +128 per pair to t=1626: 0->-5247.
Values: -129,-255,-513,-639,-897,-1023,-1281,-1407,-1665,-1791,-2049,-2175,-2433,-2559,
-2817,-2943,-3201,-3327,-3585,-3711,-3969,... = -((3k+1)*2^7 + 1) and -((3k+1)*2^7 + 127).

Consequences:
1. **|Delta(t)| <= 3t + O(1)** for all t (law shape; verified to t ~ 1630).
2. Delta(t) is a function of t ALONE (independent of the excursion level v) — the entire
   fire sequence of every excursion is a function of t's binary expansion (2-adic
   transducer structure; cf. agentG's route).
3. Fire level bound: sp = v2(3t+4+Delta(t)) <= log2(3t+4+|Delta|) <= log2(6t+131).
4. **Well-foundedness (L-middle backbone)**: at a frame of level L, t <= ell(L) <= 2L
   (agentF's counting), hence sp <= log2(12L+131) < L for L >= 8; levels L < 8 have
   t <= ell(L) <= 10 and |Delta| <= 33 there, so sp <= v2(6*10+131)... <= 4 < L except
   L <= 4 which the exact certificates cover directly. Hence every nested excursion fired
   from a real frame has level sp < L: **the compositional recursion is well-founded on
   the real orbit.** (Remaining to make this [Class-A]: prove the Delta-law table closed
   for all t — the creation-time residues 40/82 mod 128 and the value pattern; this is
   exactly agentG's transducer-finiteness claim, or provable by the same sigma-cancellation
   algebra as agentC's landing formulas.)
