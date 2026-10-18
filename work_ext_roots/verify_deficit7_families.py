"""Finite check of the two correlated reference families for BAA/BBA.

Reference-family closure at all parameters is NOT asserted.
"""
from collections import Counter
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_global_ext'/'route_c'))
from fdata import lam_walk,small_full,v2
from verify_low_deficit import Calendar,first_fire


def follow(p,x,theta,table):
    G=0;word=[];max_record=0
    for _ in range(100):
        if x<=0:return dict(status='nonpositive',word=word)
        j=v2(x);word.append(j);max_record=max(max_record,j+G)
        if j+G>=p-1:return dict(status='ceiling',word=word)
        if j-1 not in table:return dict(status='missing source',word=word)
        r=table[j-1]
        if not r['odd']:return dict(status='end',word=word,margin=p-1-max_record)
        if r['typ']=='a':
            x=2*theta+3*r['tau']-x//2
        else:
            c,lam=r['x'];x=c*(x >> j)+lam
        theta+=3+3*r['tau'];G+=1+r['eps']
    return dict(status='work limit',word=word)


def main():
    N=1000000
    data=lam_walk(N);table=small_full(1024)
    results={}
    for family in ('BAA_minus','BBA_plus'):
        counts=Counter();longest=[];failures=[];minmargin=N;nonterminal=0;total=0
        for p in range(5,N):
            if data['typ'][p-1]!=97 or not data['odd'][p-1]:continue
            k=data['tau'][p-1]//2
            x=6*k+6 if family=='BAA_minus' else 6*k-2
            theta=x-1 if family=='BAA_minus' else x+3
            r=follow(p,x,theta,table);total+=1
            counts[r['status']]+=1
            if r['status']!='end':
                failures.append(dict(p=p,k=k,**r));continue
            minmargin=min(minmargin,r['margin'])
            if len(r['word'])>1:nonterminal+=1
            if len(r['word'])>len(longest):longest=r['word']
        results[family]=dict(cases=total,status_counts=dict(counts),longest=longest,
                             nonterminal_cases=nonterminal,minimum_margin=minmargin,
                             failures=failures[:20],failure_count=len(failures))
        assert not failures
    calendar=Calendar(512)
    deep={name:dict(cases=0,nonterminal=0,longest=[],examples=[]) for name in results}
    for fire_parameter in range(5,257):
        fire=first_fire(calendar,fire_parameter)
        k,rho=fire['k'],fire['pointer']
        for offset in range(12):
            p=rho+1
            for family in deep:
                x=6*k+6 if family=='BAA_minus' else 6*k-2
                theta=x-1 if family=='BAA_minus' else x+3
                r=follow(p,x,theta,table)
                assert r['status']=='end',(family,fire_parameter,offset,r)
                d=deep[family];d['cases']+=1
                if len(r['word'])>1:
                    d['nonterminal']+=1
                    if len(d['examples'])<5:
                        d['examples'].append(dict(start_fire_parameter=fire_parameter,
                                                 offset=offset,input_parameter_bits=p.bit_length(),
                                                 word=r['word']))
                if len(r['word'])>len(d['longest']):d['longest']=r['word']
            J=1+v2(3*k+2)
            kernel=calendar.kernels[J]
            k+=kernel['delta'];rho+=kernel['advance']
    assert deep['BBA_plus']['nonterminal']>0
    algebra=Counter()
    for p in range(5,257):
        row=table[p-1]
        if not row['odd'] or row['typ']!='a':continue
        k=row['tau']//2
        for U in (1,3,7):
            # BBA scalar identities; outer choices are algebraic, not canonical.
            p1=p+3;P=p1+3
            x0=(1 << P)*U;y1=(1 << p1)*(1 if p1%2==0 else 5)
            y2=(1 << p)*(1 if p%2==0 else 5)
            xb=3*x0//4+y1;tb=x0+y1
            xbb=3*xb//4+y2;tbb=tb+y2-1
            x=2*tbb+6*k-xbb//2;t=tbb+2+6*k
            z=6*k-2
            assert x-z==55*x0//32+13*y1//8+3*y2//2
            assert t-(z+3)==x0+y1+y2
            assert v2(x-z)==p-1 and v2(t-z-3)==p
            assert v2(x)==v2(z)<p-1
            algebra['BBA']+=1
            # BAA only when the intermediate parameter has an odd a return.
            r=1+v2(k)
            if r<5 or not table[r-1]['odd'] or table[r-1]['typ']!='a':continue
            l=table[r-1]['tau']//2;P=p+3;x0=(1 << P)*U
            y=(1 << p)*(1 if p%2==0 else 5)
            xb=3*x0//4+y;tb=x0+y
            xa=2*tb+6*k-xb//2;ta=tb+3+6*k
            x=2*ta+6*l-xa//2;t=ta+2+6*l;z=6*l+6
            assert x-z==19*x0//16+5*y//4+9*k
            assert t-(z-1)==x0+y+6*k
            assert v2(x-z)==r-1 and v2(t-z+1)==r
            assert v2(x)==v2(z)<r-1
            algebra['BAA']+=1
    result=dict(result='PASS',review_status='unreviewed',parameter_exclusive_max=N,
                families=results,
                deep_canonical_families=deep,
                noncanonical_outer_normal_form_checks=dict(algebra),
                scope='Finite correlated reference-family checks only; arbitrary p and all higher deficits remain open.')
    Path(__file__).with_name('deficit7_family_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
