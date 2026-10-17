"""Root-anchored weighted phase grammar and its first non-NT family."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
states={0:{1:{''}}};ends_a={0:{}}
def add(table,theta,word):table.setdefault(theta,set()).add(word)
for W in (2,4,6,8):
    out={};aa={}
    for theta,words in states[W-2].items():
        for word in words:
            add(out,3-theta,word+'A');add(aa,3-theta,word+'A')
            add(out,theta-1,word+'B')
    for Ws in range(2,W-1,2):
        Wo=W-Ws-2
        for outer,words in states[Wo].items():
            for source,swords in ends_a[Ws].items():
                for word in words:
                    for sw in swords:add(out,outer+source-2,word+'C['+sw+']')
    states[W]=out;ends_a[W]=aa
    assert set(out)==set(range(1-W//2,2+W//2,2))
assert states[6][-2]=={'BBB'}
assert states[8][5]=={'BBBA'}

table=vm.Xdata(4096,SMALL=4096)
tau={n:(H[1]+(Y[1] if Y else 0)-1)//3 for n,(_,H,Y,_) in table.items()}
def val(n):return (abs(n)&-abs(n)).bit_length()-1 if n else 10**9
small_failures=[]
for j in range(5,10):
    typ,H,Y,e=table[j-1]
    if typ!='a' or sum(H)%2==0:continue
    k=tau[j-1]//2
    for theta in range(-3,6):
        if (theta+3*k-(1<<(j-2)))%(1<<(j-1))==0:small_failures.append((j,theta))
assert small_failures==[(5,5)]

families=[]
for p in range(5,4096):
    typ,H,Y,e=table[p-1]
    if typ!='a' or sum(H)%2==0:continue
    k=tau[p-1]//2
    if k%32!=6:continue
    assert p>=17 and 9*k+10<(1<<(p-2))
    q=val(9*k+10);assert 5<=q<p-2
    for z in (4 if p%2==0 else 2,7 if p%2==0 else 5):
        u=2*z-1;x=(1<<p)*u;T=(1<<p)*z-2
        assert T%3==2 and 2*T-x-5>=0 and x-T+1>=0
        x1=2*T-x//2+6*k;T1=T+3+6*k
        assert val(x1)==5
        x2=2*T1-x1//2+6;T2=T1+9
        assert x2==(1<<p)*z+(1<<(p-2))*u+9*k+10
        assert val(x2)==q
        assert (3*T2-2*x2-10)%(1<<(p-1))==0
    families.append(dict(p=p,k=k,output=q))

# Analytic inequalities are proved in the note; these check their bases
# and a finite segment, independently of the actual source-clock table.
for j in range(10,4096):assert 2*(1<<(j-2))>10+3*(j-1)**2
for p in range(17,4096):assert 2*(1<<(p-2))>9*(p-1)**2+20

result=dict(result='PASS',phase_sets={str(w):sorted(v) for w,v in states.items()},
            unique_weight8_top_phase=sorted(states[8][5]),
            small_nt_failures=small_failures,canonical_table_families=len(families),
            families=families,
            scope='Finite grammar/identities plus analytic all-parameter inequalities; no global exit bound')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='families'},indent=2))
