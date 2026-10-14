import sys, time
from collections import Counter
import skeleton as S
from fdata import v2
PM=int(sys.argv[1])
prec=[]; rd=Counter(); pats=Counter(); ex3=[]; trans=Counter()
orig=S.exit_from
def on_exit(n,t,s_,js):
    r=len(js); rd[r]+=1
    if max(js)+8*len(js)+2>=n: prec.append(n)
    if r>=2: pats[(t,)+tuple(js)]+=1
    if r>=3: ex3.append((n,t,s_,js))
# monkeypatch: wrap run's on_cross by reimplementing exit hook
def exit_hook(Th,x):
    js,why=orig(Th,x); exit_hook.last=js; return js,why
S.exit_from=exit_hook
# patch run to call on_exit: simplest—re-run per crossing via rec is not enough; reimplement small loop
src=open('skeleton.py').read()
src=src.split("def run(")[1]
src="def run("+src.split('if __name__')[0]
src=src.replace("        js,why=exit_from(Th,x)\n","        js,why=exit_from(Th,x)\n        ON(n,t,s_,js)\n")
g=dict(S.__dict__); g['ON']=on_exit; exec(src,g)
t0=time.time(); g['run'](PM,report=0)
print("time %.0f"%(time.time()-t0)); print("r dist (chains after fire):",sorted(rd.items()))
for k,v in pats.most_common(40): print(k,v)
print("precision-flagged n (exit not certified by residues):",len(prec),"max",max(prec) if prec else None)
print("r>=3:",ex3[:20], len(ex3))
