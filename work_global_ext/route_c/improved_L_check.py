"""[B]-style sanity check of the elementary inequalities in the improved Theorem L (REPORT section 9):
 (i)  2*log2(3n^2+4) <= 4*log2(l)+9   for all 2<=n<=2l+3, l>=10   (checked l=10..10^6, plus asymptotics in text)
 (ii) 1+(J-1)^2+(J/B)*(1+(2l+4)^2) <= 2J^2 for J=2^l, l>=10, B=4log2 l+9
 (iii) log2(12 J^2) < 2l+4."""
from math import log2
ok=True
for l in range(10,10**6+1):
    B=4*log2(l)+9
    if 2*log2(3*(2*l+3)**2+4)>B: ok=False; print('i fails',l); break
    if l<4000:
        J=2**l
        if (1+(J-1)**2)*9+J*(1+(2*l+4)**2)>18*J*J: ok=False; print('ii fails',l); break
        if log2(12)+2*l>=2*l+4: ok=False
print('all ok' if ok else 'FAIL')
