"""Exact residue certificate for a pure-b reset prefix ending at 5."""
from pathlib import Path
import json
def val(n):return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9
records=[];checks=0
for r in range(16):
    # m=r+16h, Theta=46-m+32z, x=32(1+2a).
    # After a at 5: x'=82-2r-32h+64z-32a.
    beta=82-2*r
    if r!=9:
        j=val(beta)
        assert 1<=j<=4 and j==1+val(9-r)
        records.append(dict(depth_residue=r,terminal_parameter=j,
                            affine_coefficients=[beta,-32,64,-32]))
    else:
        assert beta%32==0
for m in list(range(1,257))+[2**100+r for r in range(16)]:
    for v in (1,3,17):
        z=m+v+100;T=46-m+32*z;x=32*v
        # The phase drift Theta=46-m+32z is set analytically (not simulated b-addition); bases arbitrary.
        # Formal inputs here are not claimed to be realized source records.
        result=2*T-x//2+6
        assert result%32==2*(9-m)%32
        if m%16!=9:assert val(result)==1+val(9-m)<=4
        checks+=1
result=dict(result='PASS',closed_residue_classes=15,unresolved_residue=9,
            modulus=16,integer_cross_checks=checks,records=records)
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
Path(__file__).with_name('depth_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
