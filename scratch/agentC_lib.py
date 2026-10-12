"""agentC library: TM '1RB1LA_0RC0RD_1LC1LA_1RE1RD_1LF0LA_---0LE'.

Machine (state,read)->(write,move,next), F0 = HALT:
  A0->1RB  A1->1LA   B0->0RC  B1->0RD   C0->1LC  C1->1LA
  D0->1RE  D1->1RD   E0->1LF  E1->0LA   F0->HALT F1->0LE

Encoding at moments state A reads 0: tape 0^inf 1^h [0]_A 1^r1 0 1^r2 0 ... 1^rk 0^inf
  <-> list (h, r1, ..., rk).  Interior runs r_i may be 0 (two adjacent 0 cells).

Top map T on lists (missing entries count as 0):
  A even: T(L) = (A+b+c+3, S)
  A odd:  m := b + (A-3)//2 ; stack := (c + (A+1)//2, S)
          while m odd and m >= 3: stack = [(m+3)//2] + stack ; m = (m-3)//2
          if m == 1: HALT ; else T(L) = (m+4, stack)
Orbit from L0 = (3); sum(L_n) = 3n+3; HALT <=> odd step with x = A+2b+3 = 2^k, k>=3.
"""
import sys

TM = {
    ('A', 0): (1, 1, 'B'), ('A', 1): (1, -1, 'A'),
    ('B', 0): (0, 1, 'C'), ('B', 1): (0, 1, 'D'),
    ('C', 0): (1, -1, 'C'), ('C', 1): (1, -1, 'A'),
    ('D', 0): (1, 1, 'E'), ('D', 1): (1, 1, 'D'),
    ('E', 0): (1, -1, 'F'), ('E', 1): (0, -1, 'A'),
    ('F', 1): (0, -1, 'E'),
}


def tm_moments(max_moments=10000, max_steps=10 ** 7):
    """Simulate TM from blank tape; return (moments, halted, steps_used) where
    moments[i] = tuple (h, r1..rk) at the i-th time state A reads 0."""
    tape = {0: 0}
    pos, st = 0, 'A'
    moments = []
    steps = 0
    halted = False
    while steps < max_steps and len(moments) < max_moments:
        cur = tape.get(pos, 0)
        if st == 'A' and cur == 0:
            p = pos - 1
            h = 0
            while tape.get(p, 0) == 1:
                h += 1
                p -= 1
            # right side: cells pos+1 .. max written cell; parse with 0-runs
            maxcell = max([k for k, v in tape.items() if v == 1] + [pos])
            seq = []
            p = pos + 1
            while p <= maxcell:
                seq.append(tape.get(p, 0))
                p += 1
            runs = []
            if 1 in seq:
                i = 0
                n = len(seq)
                # leading zeros => that many empty runs
                while seq[i] == 0:
                    runs.append(0)
                    i += 1
                while i < n:
                    j = i
                    while j < n and seq[j] == 1:
                        j += 1
                    runs.append(j - i)
                    z = 0
                    while j < n and seq[j] == 0:
                        z += 1
                        j += 1
                    if j < n:  # more 1s follow: z-1 empty runs between
                        runs.extend([0] * (z - 1))
                    i = j
            moments.append(tuple([h] + runs))
        if st == 'F' and cur == 0:
            halted = True
            break
        w, mv, ns = TM[(st, cur)]
        tape[pos] = w
        pos += mv
        st = ns
        steps += 1
    return moments, halted, steps


def top_step(L):
    A = L[0]
    b = L[1] if len(L) > 1 else 0
    c = L[2] if len(L) > 2 else 0
    if A % 2 == 0:
        return [A + b + c + 3] + list(L[3:])
    m = b + (A - 3) // 2
    stack = [c + (A + 1) // 2] + list(L[3:])
    while m >= 3 and m % 2 == 1:
        stack = [(m + 3) // 2] + stack
        m = (m - 3) // 2
    if m == 1:
        return None  # HALT
    return [m + 4] + stack


def v2(x):
    if x == 0:
        return -1
    v = 0
    while x % 2 == 0:
        x //= 2
        v += 1
    return v


def orbit(N, check=True):
    """Yield L_0..L_{N-1}; assert sum invariant and non-halting."""
    L = [3]
    if check:
        assert sum(L) == 3
    yield 0, L
    for n in range(1, N):
        L = top_step(L)
        if L is None:
            raise RuntimeError("HALT at step %d" % n)
        if check:
            assert sum(L) == 3 * n + 3, (n, L)
        yield n, L
