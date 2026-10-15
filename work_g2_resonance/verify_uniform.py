"""Uniform affine certificates for the parameter-65 b-depth family.
Two independent positive odd symbols are retained. No residue representatives
are sampled to decide a branch: every decision is uniform over the symbols.
"""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm

X=vm.Xdata(128,SMALL=128)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in X.items()}
def val(n):
    return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9

assert min(n for n,(kind,H,_,_) in X.items()
           if kind=='a' and sum(H)%2 and val(H[1]+3)==5)==63

def certificate(q):
    # x=2^q*(1+2a), Theta=x/2+46+3*2^61*(1+2b).
    x=(1<<q,1<<(q+1),0)
    T=((1<<(q-1))+46+3*(1<<61),1<<q,3*(1<<62))
    j=q;sigma=63;duration=0;path=[];minimum=sigma-j
    for _ in range(64):
        assert j<sigma
        kind,H,Y,eps=X[j-1]
        path.append(dict(j=j,sigma=sigma,x=list(x),Theta=list(T),kind=kind))
        duration+=1+tau[j-1]
        if sum(H)%2==0:
            duration+=1 # final even return
            return dict(q=q,parameters=[p['j'] for p in path],min_margin=minimum,
                        tail_steps=duration,whole_65_tail_steps=56+duration,states=path)
        if kind=='a':
            assert all(z%2==0 for z in x)
            xn=tuple(2*T[i]-x[i]//2+(3*tau[j-1] if i==0 else 0) for i in range(3))
        else:
            cx=H[0]+2*Y[0];lx=H[1]+2*Y[1]+3
            assert all(z%(1<<j)==0 for z in x)
            xn=tuple(cx*(x[i]>>j)+(lx if i==0 else 0) for i in range(3))
        T=(T[0]+3*tau[j-1]+3,T[1],T[2])
        sigma-=1+eps
        # A strict valuation comparison proves one branch for ALL a,b.
        jn=val(xn[0]);assert jn<min(val(xn[1]),val(xn[2]))
        assert jn<sigma
        minimum=min(minimum,sigma-jn)
        j,x=jn,xn
    raise AssertionError('Unclosed symbolic family')

def concrete(m,z,u,sigma,stop_at_first_a=False):
    assert (2*z-m)%3==0 and u%2 and sigma>65
    T=(z<<65)+2-m;s=(T-5)//3;s0=s
    A=(1<<sigma,((2*z-u)<<65)-2*m-1)
    P=[(1<<sigma,((u-z)<<65)+m-1)]
    assert s>=0 and A[1]>=0 and P[0][1]>=0
    i=sigma+1;next_top=0;js=[];minimum=10**9
    while P:
        assert sum(c for c,l in [A]+P)==1<<i
        assert sum(l for c,l in [A]+P)==3*s+1
        ent=P[:2];ni=i
        while len(ent)<2:ent.append((1<<ni,0));ni+=1
        b,c=ent;tail=P[2:]
        if sum(A)%2:
            cx,lx=A[0]+2*b[0],A[1]+2*b[1]+3;j=val(lx)
            assert j<val(cx)
            minimum=min(minimum,val(cx)-j)
            if s-s0==next_top:
                js.append(j)
                if stop_at_first_a and len(js)==3:return js,s-s0,minimum
                next_top=s-s0+1+tau[j-1]
            base=(cx>>j,lx>>j);D=(c[0]+A[0]//2,c[1]+(A[1]+1)//2)
            A=(base[0],base[1]+1)
            P=[(base[0]<<t,base[1]<<t) for t in range(j-1)]+[D]+tail
        else:A=(A[0]+b[0]+c[0],A[1]+b[1]+c[1]+3);P=tail
        i=ni;s+=1
        assert s-s0<1000
    return js,s-s0,minimum

if __name__=='__main__':
    records=[certificate(q) for q in range(1,63)]
    concrete_cases=0
    depths=[124+(1<<(q-1)) for q in range(1,62)]+[124,124+(1<<62)]
    depths+=list(range(1,124))+[124+(1<<120),125+(1<<130)]
    for m in depths:
        z=3*m+1000
        while z%3!=(2*m)%3:z+=1
        u=z+1 if z%2==0 else z+2
        j=v=val(124-m)
        assert v!=61
        q=v+1 if v<61 else 62
        for sigma in (66,100):
            js,steps,margin=concrete(m,z,u,sigma)
            r=records[q-1]
            assert js==[65,5]+r['parameters']
            assert steps==r['whole_65_tail_steps']
            concrete_cases+=1

    # The exceptional class is genuinely unresolved with these local inputs:
    # at one fixed m, construct any output q=62+t, with adequate scale margin.
    exceptional=[];m=124+(1<<61)
    for t in (1,2,3,10,66,194):
        modulus=1<<(t+1);z=3*modulus
        residue=(-(1+(1<<t))*pow(3,-1,modulus))%modulus
        u=z+residue;q=62+t
        js,_,margin=concrete(m,z,u,q+4,stop_at_first_a=True)
        assert js==[65,5,q]
        exceptional.append(q)

    result=dict(result='PASS',symbolic_families=len(records),branches=0,
                min_margin=min(r['min_margin'] for r in records),
                max_post_reset_chains=max(len(r['parameters']) for r in records),
                max_65_tail_steps=max(r['whole_65_tail_steps'] for r in records),
                concrete_cases=concrete_cases,exceptional_sample_outputs=exceptional,
                excluded_class='m = 124+2^61 (mod 2^62)',families=records)
    Path(__file__).with_name('uniform_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='families'},indent=2))
