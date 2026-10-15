"""Reproducible finite boundary structure; not an unbounded classification."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm
data=json.loads((ROOT/'work_g2_core_words/words_1023.json').read_text())
escapes=[tuple(e['word']) for e in data['edges'] if e['can_escape']]
table=vm.Xdata(1024,SMALL=1024)
def half_time(q):
    kind,H,Y,_=table[q-1]
    assert kind=='a' and sum(H)%2
    assert (H[1]-1)%6==0
    return (H[1]-1)//6
pairs=sorted(set(tuple(sorted(w[-2:])) for w in escapes))
families=[];expected=set()
for p,r in pairs:
    assert p in (5,8) and r>p
    kp,kr=half_time(p),half_time(r)
    modulus=1<<(p-1);residue=(1<<(p-2))-kp-1
    assert kr%modulus==residue
    templates={(p,r),(r,p),(p,r,p),(r,p,r),(p,r,p,r)}
    expected|=templates
    families.append(dict(small=p,large=r,k_small=kp,k_large=kr,
                         modulus=modulus,residue=residue,
                         source_fire_parameter=vm.v2(6*kr+4)))
assert set(escapes)==expected and len(escapes)==len(expected)==165
assert Counter(f['small'] for f in families)=={5:29,8:4}

# Exact affine identity for two consecutive odd a-returns.
# Coordinates: X0, Theta0, k0, k1, 1.
X0=(F(1),F(0),F(0),F(0),F(0));T0=(F(0),F(1),F(0),F(0),F(0))
X1=tuple(2*T0[i]-X0[i]/2+(6 if i==2 else 0) for i in range(5))
T1=tuple(T0[i]+(6 if i==2 else 3 if i==4 else 0) for i in range(5))
X2=tuple(2*T1[i]-X1[i]/2+(6 if i==3 else 0) for i in range(5))
T2=tuple(T1[i]+(6 if i==3 else 3 if i==4 else 0) for i in range(5))
assert T2==tuple(X2[i]-X0[i]/4-(3 if i==2 else 0) for i in range(5))

phase_rows=[dict(small=5,orientation='small_then_large',phase=5,modulus=16,shift_valuation=0,a_exception=9,bc_collision=1),
            dict(small=5,orientation='large_then_small',phase=14,modulus=16,shift_valuation=2,a_exception=6,bc_collision=3),
            dict(small=8,orientation='small_then_large',phase=58,modulus=128,shift_valuation=3,a_exception=2,bc_collision=4),
            dict(small=8,orientation='large_then_small',phase=73,modulus=128,shift_valuation=0,a_exception=13,bc_collision=1)]
phase_checks=0
for f in families:
    for orientation in ('small_then_large','large_then_small'):
        row=next(z for z in phase_rows if z['small']==f['small'] and z['orientation']==orientation)
        q0,k0=(f['small'],f['k_small']) if orientation=='small_then_large' else (f['large'],f['k_large'])
        for U in (1,3,5):
            x0=(1<<q0)*U;x2=1<<1100;theta2=x2-x0//4-3*k0
            assert theta2%row['modulus']==row['phase']
            assert vm.v2(theta2-2)==row['shift_valuation']
            for k in range(16):
                if k==row['a_exception']:continue
                assert vm.v2(2*theta2-x2//2+6*k)<=4
                phase_checks+=1

result=dict(result='PASS',cap=1023,escape_nodes=165,unordered_pairs=len(pairs),
            families_by_small_parameter=dict(Counter(f['small'] for f in families)),
            templates=['p,r','r,p','p,r,p','r,p,r','p,r,p,r'],
            half_time_conditions={'5':'k_r = 6 mod 16','8':'k_r = 61 mod 128'},
            two_a_identity='Theta2 = X2 - X0/4 - 3*k0',
            boundary_phase_table=phase_rows,phase_identity_checks=phase_checks,
            families=families,
            caveat='Finite necessary arithmetic boundary; neither reachability nor an all-scale classification')
Path(__file__).with_name('boundary_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='families'},indent=2))
