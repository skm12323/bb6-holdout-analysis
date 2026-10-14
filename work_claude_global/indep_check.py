"""Independent check of the predicted r=3 exit at J=50148477 using the audited work_m code:
V2 (lambda walker) gives tau(n) and crossing type; sym_exit (V4 recursion) gives the exit."""
import sys, time
sys.path.insert(0, r'D:/math_cc/work_m')
import verify_m as M
n=50148476; J=n+1
M.CAP=n+8
t=time.time()
# reuse V2 but capture its locals: re-implement minimal hook by running V2 then reading Xt via closure is impossible,
# so patch: V2 stores Xt locally; we copy the function source with a return of Xt.
import inspect
from array import array
M.array=array
src=inspect.getsource(M.V2).replace("return st,rdist,pat","return st,rdist,pat,Xt,Xeps").replace("def V2(","def V2x(").replace("Xt=[None]*CAP; Xeps=[0]*CAP; Xpar=[0]*CAP","Xt=array('q',[-1])*CAP; Xeps=array('q',[0])*CAP; Xpar=None").replace("Xt[n] is None","Xt[n]<0").replace("Xt[j-1] is not None","Xt[j-1]>=0")
exec(src, M.__dict__)
st,rd,pat,Xt,Xeps=M.V2x(n+4, verbose=False)
print("V2 done %.0fs"%(time.time()-t), "rdist",sorted(rd.items()))
s=Xt[n]; e=Xeps[n]
print("tau(n)=",s,"eps(n)=",e,"(0 => type a)")
X=M.Xdata(200)
d=('a',(1<<n,3*s+1),None,0)
print("head parity (c+lam) odd?", (3*s+1)%2==1)
res=M.sym_exit(J,X,first=d)
print("sym_exit:",res)
