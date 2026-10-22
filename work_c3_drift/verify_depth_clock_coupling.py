"""Exact pair identity and source/depth congruences for the c_r orbit."""
from pathlib import Path
from fractions import Fraction as F
import json
from verify_orbit_shift_obstruction import discrete_log_three

def main():
    checks=0
    for x in (32,96,160,224):
        for theta in (37,53,69,101):
            for k in (1,6,22,70,819270):
                D=theta-x;y=-F(x,2)+2*theta+6
                xn=F(x,4)+theta+15+6*k;tn=theta+12+6*k
                yn=-xn/2+2*tn+6
                assert D==51+27*k+11*y/4-3*yn
                checks+=1
    # Cross-scale witness parameters; reconstruct only the needed residues.
    ka,kb=819270,229398;a,b=1836655,514273
    y0=1<<a;y1=(1<<b)+(1<<(a+10))
    theta=y1-y0//4-21-9*ka;x=4*theta+12-2*y0;D=theta-x
    E=min(a-2,b);u=(ka+2)//8
    assert (D-51-27*ka)%(1<<E)==0
    samples=[]
    for h in (3,6,12,16,32,64,128,256):
        target=pow(27*u,-1,1<<h)
        r=discrete_log_three(target,h)
        assert (pow(3,r+3,1<<h)*u-1)%(1<<h)==0
        assert r%1024==1019 if h>=12 else True
        samples.append(dict(modulus_bits=h,r_residue=str(r),exponent_period_bits=h-2))
    # Test the source residue exclusion directly over all 16 classes k=6 mod16.
    allowed=[];excluded=[]
    for k in range(6,262,16):
        uu=(k+2)//8
        (allowed if uu%8 in (1,3) else excluded).append(k%64)
    assert set(allowed)=={6,22} and set(excluded)=={38,54}
    # Each pair has its own precision E_i=min(m_i-2,m_(i+1)).
    # The first pair's large precision must not be reused at the second.
    r=int(samples[-1]['r_residue'])
    pair_checks=[]
    labels=(a,b,17,17)
    for i,k in enumerate((ka,kb,6)):
        Ei=min(labels[i]-2,labels[i+1]);h=min(128,Ei-3)
        assert (pow(3,r+i+3,1<<h)*((k+2)//8)-1)%(1<<h)==0
        pair_checks.append(dict(i=i,E=Ei,checked_modulus_bits=h))
    # Retain the rejected overprecision claim as a negative control.
    assert (pow(3,r+4,1<<128)*((kb+2)//8)-1)%(1<<128)!=0
    out=dict(status='PASS',review_status='unreviewed',pair_identity_checks=checks,
             cross_scale_required_E=E,source_unit=u,
             allowed_k_mod64=[6,22],excluded_k_mod64=[38,54],samples=samples,
             pair_precision_checks=pair_checks,overprecision_control_rejected=True,
             necessary_depth_lower_bound=samples[-1]['r_residue'],
             scope='Necessary coupling for a stated high-precision c_r representation. No proof that such depths or initial states are jointly reachable.')
    Path(__file__).with_name('depth_clock_coupling_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))

if __name__=='__main__':main()
