"""Canonical predecessor and duration normalization for MINUS/PLUS.

The duration-family condition is only tested finitely, not proved globally.
"""
from collections import Counter
from pathlib import Path
import json

from verify_low_deficit import Calendar,first_fire
from verify_deficit7_families import follow,lam_walk,small_full,v2


def main():
    calendar=Calendar(8208);table=small_full(1024)
    delta=[None]+[calendar.kernels[h]['delta'] for h in range(1,8193)]
    assert delta[1:5]==[1,1,2,2]
    incoming=[]
    for r in range(16):
        if r==10:continue
        H=1+v2(3*r+2)
        assert 1<=H<=4
        landing=(r+delta[H])%16
        assert landing not in (11,15)
        incoming.append((r,H,landing))
    counts=Counter();examples=[]
    def check(k0,rho0,k,rho,tag):
        H=1+v2(3*k0+2);D=k-k0
        assert D==calendar.kernels[H]['delta']
        assert rho-rho0==calendar.kernels[H]['advance']
        x0=6*k0+4
        for name in ('minus','plus'):
            x=6*k+6 if name=='minus' else 6*k-2
            theta=x-1 if name=='minus' else x+3
            if v2(x)<5:continue
            assert H>=5 and k0%16==10
            assert k%16==(15 if name=='minus' else 11)
            assert D%16==(5 if name=='minus' else 1)
            z=6*D+2 if name=='minus' else 6*D-6
            tr=z-1 if name=='minus' else z+3
            assert 0<z<1 << H
            assert x-z==theta-tr==x0 and v2(x0)==H
            assert v2(x)==v2(z)<H<rho
            a=follow(rho+1,x,theta,table)
            b=follow(H+1,z,tr,table)
            assert a['status']==b['status']=='end' and a['word']==b['word']
            counts[tag+'_'+name]+=1
            if len(examples)<8 or (name=='plus' and not any(e['family']=='plus' for e in examples)):
                examples.append(dict(family=name,H=H,delta=D,reduced_x=z,
                                     word=b['word'],input_pointer_bits=rho.bit_length()))
    data=lam_walk(1000000)
    fires=[(data['tau'][n]//2,n) for n in range(4,data['N'])
           if data['typ'][n]==97 and data['odd'][n]]
    for (k0,rho0),(k,rho) in zip(fires,fires[1:]):
        check(k0,rho0,k,rho,'direct')
    for H in range(5,257):
        fire=first_fire(calendar,H)
        k0,rho0=fire['k'],fire['pointer'];kernel=calendar.kernels[H]
        check(k0,rho0,k0+kernel['delta'],rho0+kernel['advance'],'deep')
    duration=Counter();longest={}
    for H in range(5,8193):
        D=delta[H]
        assert D>1 and 6*D+2<1 << H
        for name,residue in (('minus',5),('plus',1)):
            if D%16!=residue:continue
            z=6*D+2 if name=='minus' else 6*D-6
            r=follow(H+1,z,z-1 if name=='minus' else z+3,table)
            assert r['status']=='end',(H,D,name,r)
            duration[name]+=1
            if len(r['word'])>len(longest.get(name,[])):longest[name]=r['word']
    for H in range(16,4097):assert 6*H**3+2<1 << H
    result=dict(result='PASS',review_status='unreviewed',
                small_kernel_residue_transitions=incoming,
                predecessor_shadow_cases=dict(counts),examples=examples,
                finite_duration_cases=dict(duration),longest_duration_words=longest,
                duration_parameter_max=8192,
                scope='All-scale predecessor/normal-form argument is separate; duration-family termination is checked only in this finite range.')
    Path(__file__).with_name('duration_reduction_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
