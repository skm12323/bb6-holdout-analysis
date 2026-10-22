"""Exact boundary checks for L3; the all-j argument is analytic in the note."""
from pathlib import Path
import json

N0=20_000_000
B=1<<(N0//2)

def clock_polynomial(n):
    g=(6*n*n+4).bit_length()
    return 2*g*g+1345

def L3(j):
    n=j-1;p=clock_polynomial(n)
    # Twice 3*(kappa+B), to avoid all rounding of kappa=3*n*p/2.
    numerator=9*n*p+6*B
    a=numerator.bit_length()-1
    b=(6*n*p+5).bit_length()-1
    assert numerator.bit_length()<=j-1  # SIZE3: numerator < 2^(j-1)
    assert max(a,b)<j
    return max(a,b)

def main():
    samples=sorted(set([N0+i for i in (0,1,2,3,15,31,63,127,1023)]
                       +[(1<<e)+d for e in (25,32,64,128,256,512,1024,2048,4096)
                         for d in (-1,0,1)]))
    records=[]
    for q in samples:
        j=q;path=[]
        while j>=N0:
            path.append(str(j) if j.bit_length()<128 else f'{j.bit_length()}-bit integer')
            z=L3(j)
            # Integer upper bound using ceil(log2 j), independent of floats.
            assert z<=max(2*(j-1).bit_length()+5,N0//2+4)
            j=z
        records.append(dict(input_bits=q.bit_length(),h3=len(path),end=j))
    out=dict(status='PASS',review_status='unreviewed',samples=len(samples),
             records=records,
             scope='Exact finite boundary checks only; all-scale SIZE3 follows from the split power bounds in RATIONAL_MODE.md.')
    Path(__file__).with_name('rational_size_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}))

if __name__=='__main__':main()
