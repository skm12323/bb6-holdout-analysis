"""Scratch 4: exact-leading-digits check of d=ceil(r log2 3) for the O1 r."""
from decimal import Decimal, getcontext
from pathlib import Path
import json
getcontext().prec = 80
r = 657306078883964
# 80-digit value of log2(3)
log2_3 = Decimal('1.584962500721156181453738943947816508759814407692481060455752654541098227794')
x = Decimal(r) * log2_3
import math
d_floor = int(x)              # floor (x not an integer to 80 digits)
d = d_floor + 1
# The float answer for comparison
d_float = math.ceil(r * 1.5849625007211562)
out = dict(r=r, r_log2_3=str(x), d_exact=d, d_float=d_float, delta=d - d_float)
Path(__file__).with_name('o1_digits.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out, indent=2))
