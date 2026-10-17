"""Compare clock projection with the existing independent 2D lattice solver."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,sys
from clock_words import (clock_projection,lift,v2,fire_projection,floor_sum,
                         count_entry_lifts,failure_pointer_interval,
                         all_last_failure_candidates)

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
table=vm.Xdata(64,SMALL=64)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
blocks={}
for q in range(5,64):
    j=q;alpha=F(1);B=F(0);d=G=0
    while True:
        typ,H,Y,eps=table[j-1]
        if sum(H)%2==0:break
        if typ=='a':
            k=tau[j-1]//2
            blocks[q]=dict(alpha=alpha,B=B,d=d,G=G,k=k,T=d+1+2*k)
            break
        ratio=F(H[0]+2*Y[0],1<<j);c=H[1]+2*Y[1]+3
        alpha*=ratio;B=ratio*B+c;d+=1+tau[j-1];G+=1+eps;j=v2(c)

# Load only the existing pure lattice function, avoiding the old script's
# top-level experiment and writes to its accepted certificate files.
tree=ast.parse((ROOT/'work_g2_core_repeats/period_two.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='constrain')
namespace={'val':v2}
exec(compile(ast.Module(body=[fn],type_ignores=[]),'existing_constrain','exec'),namespace)
constrain=namespace['constrain']

def independent(word):
    q,r=word[:2]
    xs=[(F(0),F(1<<q),F(0)),(F(0),F(0),F(1<<r))]
    base=(1,1);cols=[(2,0),(0,2)]
    for i in range(2,len(word)):
        b0=blocks[word[i-2]];b1=blocks[word[i-1]]
        C=b0['B']/2+6+6*b0['k']+6*b1['k']+6*b1['d']-b1['B']/2
        xx=tuple(b0['alpha']*xs[-2][z]/2+(1-b1['alpha']/2)*xs[-1][z]+(C if z==0 else 0)
                 for z in range(3))
        den=max(z.denominator for z in xx);c,A,B=(int(z*den) for z in xx)
        ans=constrain(base,cols,A,B,den*(1<<word[i])-c,den*(1<<(word[i]+1)))
        if ans is None:return None
        base,cols=ans;xs.append(xx)
    b0=blocks[q];const=6*b0['d']+6*b0['k']-b0['B']/2
    def clock(u,v,constant=True):
        return ((1<<r)*v+b0['alpha']*(1<<q)*u/2-(const if constant else 0))/2
    theta=clock(*base);slopes=[clock(*col,constant=False) for col in cols]
    assert theta.denominator==1 and all(s.denominator==1 for s in slopes)
    h=min(map(v2,slopes));return int(theta)%(1<<h),h

alphabet=sorted(blocks)
frontier=[(q,r) for q in alphabet for r in alphabet]
counts={2:len(frontier)};checked=0;lift_checks=0;max_h=0;failure_candidates=[]
feasible_words=[]
def check(word):
    global checked,lift_checks,max_h
    p=clock_projection(word,blocks);ref=independent(word);checked+=1
    assert (p is None)==(ref is None),word
    if p is None:return False
    feasible_words.append(word)
    assert (p['theta_residue'],p['theta_bits'])==ref,(word,p,ref)
    analytic=0
    for i in range(len(word)-1):
        E=0;G=blocks[word[i]]['G']
        for j in range(i+1,len(word)):
            E+=blocks[word[j-1]]['G']+1
            analytic=max(analytic,min(word[i]-G-1,word[j]+E-G-1))
    assert p['theta_bits']==analytic
    if (candidate:=failure_pointer_interval(word,blocks)) is not None:
        failure_candidates.append(dict(word=word,candidate=candidate))
    max_h=max(max_h,analytic)
    for t,u in ((0,0),(1,0),(2,1)):
        x,theta=map(F,lift(p,t,u))
        for i,q in enumerate(word):
            assert x.denominator==1 and v2(x)==q
            if i+1<len(word):
                b=blocks[q]
                x=2*theta-b['alpha']*x/2+6*b['d']+6*b['k']-b['B']/2
                theta+=3*b['T']
        lift_checks+=1
    return True

for word in frontier:assert check(word)
for length in range(3,8):
    frontier=[w+(q,) for w in frontier for q in alphabet if check(w+(q,))]
    counts[length]=len(frontier)
    if not frontier:break
assert counts=={2:324,3:80,4:59,5:21,6:2,7:0}

examples=[]
for word in ((5,17),(17,5,17),(5,17,5,17),(8,5,17)):
    p=clock_projection(word,blocks)
    first=None
    if p is not None:
        hi=1
        while count_entry_lifts(p,hi)==0:hi*=2
        lo=0
        while lo<hi:
            mid=(lo+hi)//2
            if count_entry_lifts(p,mid):hi=mid
            else:lo=mid+1
        first=lo
    examples.append(dict(word=word,projection=p,fire_projection=fire_projection(p),
                         entry_lifts_through_100000=count_entry_lifts(p,100000),
                         first_mass_compatible_step=first))

floor_checks=0
for n in range(12):
    for m in range(1,10):
        for a,b in ((-17,5),(8,-13),(0,2),(21,33),(-3,-2)):
            assert floor_sum(n,m,a,b)==sum((a*i+b)//m for i in range(n))
            floor_checks+=1
height_checks=0
for word in ((5,17),(17,5,17),(5,17,5,17),(8,5,17)):
    p=clock_projection(word,blocks)
    brute=0
    for s in range(100001):
        if p is None:continue
        theta=3*s+5
        if (theta-p['theta_residue'])%(1<<p['theta_bits']):continue
        M=1<<p['anchor_bits'];r=(p['anchor_slope']*theta+p['anchor_offset'])%M
        lo=theta-1;hi=2*theta-5
        brute+=max(0,(hi-r)//M-((lo-r-1)//M))
    assert brute==count_entry_lifts(p,100000)
    height_checks+=1

fire_checks=0
for q in alphabet:
    for u in range(1,16,2):
        x=F((1<<q)*u);theta=x+1;theta_initial=theta
        word=[q]
        for _ in range(12):
            j=word[-1]
            if j not in blocks:break
            b=blocks[j]
            x=2*theta-b['alpha']*x/2+6*b['d']+6*b['k']-b['B']/2
            theta+=3*b['T'];word.append(v2(x))
            assert word[-1]<64
        else:raise AssertionError('unexpected long local fire lift')
        f=fire_projection(clock_projection(word,blocks))
        assert f is not None and (theta_initial-f['theta_residue'])%(1<<f['bits'])==0
        fire_checks+=1

# Exercise the filter's nonempty branch with an explicitly invented
# clock, never as canonical data: k(7)=21 instead of its actual value 2.
# This clock obeys the numeric C1 inequality, so C1 alone cannot replace
# the exact canonical source-clock relation in a global use of the filter.
fake={8:dict(alpha=F(1),B=F(0),d=0,G=0,k=21,T=43)}
assert 2*fake[8]['k']<=7**2
assert failure_pointer_interval((8,9),fake)==dict(
    min_pointer=10,max_pointer=10,unique_fire_step=84,total_loss=1,final_parameter=9)
assert blocks[8]['k']==2
assert failure_pointer_interval((8,9),blocks) is None

complete_last_checks=0;complete_last_candidates=[];max_last_bound=0
for prefix in [(q,) for q in alphabet]+feasible_words:
    result=all_last_failure_candidates(prefix,blocks)
    complete_last_checks+=1
    max_last_bound=max(max_last_bound,result['last_parameter_bound'])
    if result['candidates']:
        complete_last_candidates.append(dict(prefix=prefix,result=result))
assert complete_last_candidates==[]
fake_result=all_last_failure_candidates((8,),fake)
assert any(c['final_parameter']==9 for c in fake_result['candidates'])
# The all-q proof uses 12q^2<2^(q-1), starting at 12; verify the base
# and a finite tail. Monotonicity supplies the infinite tail in the note.
for q in range(12,4096):assert 12*q*q<1<<(q-1)
for q in range(18,4096):assert 24*(q+1)*q*q+6*q+5<1<<q
result=dict(result='PASS',parameter_cap=63,word_counts=counts,
            independent_projection_comparisons=checked,lift_checks=lift_checks,
            maximum_clock_bits=max_h,examples=examples,
            floor_sum_checks=floor_checks,height_count_checks=height_checks,
            fire_projection_checks=fire_checks,
            necessary_failure_candidates=failure_candidates,
            synthetic_nonempty_filter_check='Invented k(7)=21, not canonical; interval [10,10], fire step 84',
            complete_last_prefix_checks=complete_last_checks,
            maximum_unsafe_last_parameter_bound=max_last_bound,
            complete_last_candidates=complete_last_candidates,
            scope='Exact integer affine-word projection; no positivity or canonical reachability claim')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
