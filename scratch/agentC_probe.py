"""Inspect orbit segments around interesting fires and segment into excursions."""
import agentC_lib as lib
import sys

def seg(lo, hi):
    L = [3]
    for n in range(1, hi + 1):
        L = lib.top_step(L)
        if lo <= n:
            a = L[0]
            b = L[1] if len(L) > 1 else 0
            x = a + 2 * b + 3 if a % 2 == 1 else None
            tag = ""
            if a % 2 == 1:
                k = lib.v2(x)
                q = x >> k
                tag = "FIRE k=%d q=%d" % (k, q)
            print("n=%-4d %s  %s" % (n, L, tag))

print("=== segment 28..44 ===")
seg(28, 44)
print()
print("=== segment 90..106 ===")
seg(90, 106)
print()
print("=== segment 508..522 ===")
seg(508, 522)
print()
print("=== segment 1022..1034 ===")
seg(1022, 1034)
