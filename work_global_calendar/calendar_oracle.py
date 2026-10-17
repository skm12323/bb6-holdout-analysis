"""Exact finite-prefix canonical calendar, using certified small kernels.

No query beyond the first unresolved high-parameter fire is permitted.
Large coefficient powers 2^pointer are kept as normalized fractions.
"""
from fractions import Fraction as F
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_m'))
import verify_m as vm

def val(x):
    x=F(x)
    if not x:return 10**30
    a=abs(x.numerator);b=x.denominator
    return (a&-a).bit_length()-(b&-b).bit_length()

def bitsum(n,weights):
    total=0
    while n:
        bit=n&-n;total+=weights[bit.bit_length()-1];n-=bit
    return total

class Calendar:
    def __init__(self,B):
        if B<2:raise ValueError('cutoff must be >=2')
        self.B=B
        self.base=vm.Xdata(2*B+16,SMALL=2*B+16)
        self.tau={n:(H[1]+(Y[1] if Y else 0)-1)//3
                  for n,(_,H,Y,_) in self.base.items()}
        self.kernels={};max_loss=0
        for J in range(1,B+1):
            result=vm.sym_exit(J,self.base)
            if isinstance(result[0],str):raise ValueError(('unresolved kernel',J,result))
            js,types,r,G=result
            cost=sum(1+self.tau[j-1] for j in js)+1
            delta=(cost+1)//2
            advance=2+types.count('a')+2*(cost%2)
            assert delta>0 and advance>0
            assert delta.bit_length()<J or delta==1<<(J-1)
            assert max(js)<=B
            self.kernels[J]=dict(delta=delta,advance=advance,word=js,types=types,loss=G)
            max_loss=max(max_loss,G)
        assert B+max_loss<2*B+16
        self.max_kernel_loss=max_loss
        self.weights=[];self.counts=[];S=C=0
        for r in range(B):
            kernel=self.kernels[r+1];skip=kernel['delta']-1
            W=kernel['advance']+S-bitsum(skip,self.weights)
            N=1+C-bitsum(skip,self.counts)
            assert W>0 and N>0
            self.weights.append(W);self.counts.append(N);S+=W;C+=N
        modulus=1<<B
        self.boundary_k=(-2*pow(3,-1,modulus))%modulus
        assert self.boundary_k>1
        self.initial_distance=self.boundary_k-1
        self.boundary_pointer=4+bitsum(self.initial_distance,self.weights)
        self.fire_count=bitsum(self.initial_distance,self.counts)
        self._cached=None

    def preceding_fire_by_pointer(self,n):
        if not 4<=n<self.boundary_pointer:raise ValueError('outside certified calendar')
        D=self.initial_distance;k=1;rho=4;count=0;jumps=0
        while True:
            r=val(D);kernel=self.kernels[r+1]
            if rho+self.weights[r]<=n:
                D-=1<<r;k+=1<<r;rho+=self.weights[r];count+=self.counts[r]
            elif rho+kernel['advance']<=n:
                D-=kernel['delta'];k+=kernel['delta'];rho+=kernel['advance'];count+=1
            else:
                assert 1+val(3*k+2)==r+1
                return dict(k=k,pointer=rho,J=r+1,index=count,jumps=jumps)
            jumps+=1

    def preceding_fire_by_time(self,s):
        if not 2<=s<2*self.boundary_k:raise ValueError('outside certified calendar')
        target=s//2;D=self.initial_distance;k=1;rho=4;count=0;jumps=0
        while True:
            r=val(D);kernel=self.kernels[r+1]
            if k+(1<<r)<=target:
                D-=1<<r;k+=1<<r;rho+=self.weights[r];count+=self.counts[r]
            elif k+kernel['delta']<=target:
                D-=kernel['delta'];k+=kernel['delta'];rho+=kernel['advance'];count+=1
            else:
                return dict(k=k,pointer=rho,J=r+1,index=count,jumps=jumps)
            jumps+=1

    def epoch_crossings(self,fire):
        rho=fire['pointer'];s=2*fire['k'];offset=0
        head=(F(1),3*s+1);pending=[];first=True;rows={}
        def record(n,kind,Y):
            scale=1<<(n-rho)
            Hratio=head[0]/scale;Yratio=Y[0]/scale if Y else None
            eps=n-rho-val(head[0]);odd=head[1]%2==1
            omega=val(head[1]+2*(Y[1] if Y else 0)+3) if odd else None
            rows[n]=dict(kind=kind,time=s,epsilon=eps,odd=odd,omega=omega,
                         head_ratio=Hratio,head_lambda=head[1],
                         tail_ratio=Yratio,tail_lambda=Y[1] if Y else None)
        while first or pending or s%2:
            assert head[0]+sum(p[0] for p in pending)==1<<offset
            assert head[1]+sum(p[1] for p in pending)==3*s+1
            if not pending:
                record(rho+offset,'a',None)
                record(rho+offset+1,'b',(F(1<<offset),0))
            elif len(pending)==1:
                record(rho+offset,'c',pending[0])
            entries=pending[:2];o=offset
            while len(entries)<2:entries.append((F(1<<o),0));o+=1
            (cb,lb),(cc,lc)=entries
            used=max(0,2-len(pending))
            if head[1]%2==0:
                head=(head[0]+cb+cc,head[1]+lb+lc+3);pending=[]
                offset+=used;s+=1
            else:
                cx,lx=head[0]+2*cb,head[1]+2*lb+3;j=val(lx)
                assert j<rho+val(cx)
                u_c,u_l=cx/(1<<j),lx>>j
                D=(cc+head[0]/2,lc+(head[1]+1)//2)
                typ,H,Y,e=self.base[j-1]
                image=lambda p:(p[0]*u_c,p[0]*u_l+p[1])
                head=image(H);pending=([image(Y)] if Y else [])+[D]
                offset+=used;s+=1+self.tau[j-1]
            first=False
        kernel=self.kernels[fire['J']]
        assert s==2*(fire['k']+kernel['delta']) and offset==kernel['advance']
        assert sorted(rows)==list(range(rho,rho+offset))
        return rows

    def crossing(self,n):
        if n<4:
            typ,H,Y,e=self.base[n];s=self.tau[n]
            return dict(kind=typ,time=s,epsilon=e,odd=False,omega=None,
                        head_ratio=F(H[0],1<<n),head_lambda=H[1],
                        tail_ratio=F(Y[0],1<<n) if Y else None,tail_lambda=Y[1] if Y else None)
        if self._cached is not None and n in self._cached:return self._cached[n]
        fire=self.preceding_fire_by_pointer(n)
        self._cached=self.epoch_crossings(fire)
        return self._cached[n]

    def projected_epoch(self,J,limit=32):
        """Project a root epoch from actual source data until even or NT tie.
        This may certify isolated huge J values; it never treats a tie or
        missing source as a completed kernel. The limit is a work bound.
        """
        j=J;theta=1;word=[];types='';duration=loss=0
        for _ in range(limit):
            row=self.crossing(j-1);t=row['time'];kind=row['kind']
            word.append(j);types+=kind;duration+=1+t
            if not row['odd']:
                duration+=1
                return dict(status='closed',word=word,types=types,loss=loss,
                            delta=(duration+1)//2,
                            advance=2+types.count('a')+2*(duration%2))
            loss+=1+row['epsilon']
            if kind=='a':
                assert t%2==0 and j>=5
                v=theta+3*(t//2)
                if v>0 and v.bit_length()<=j-2:
                    nxt=1+val(v)
                else:
                    rem=(v-(1<<(j-2)))%(1<<(j-1))
                    if not rem:return dict(status='NT tie',word=word,types=types)
                    nxt=1+val(rem)
                assert nxt<j
                theta=(3-theta)%(1<<nxt);j=nxt
            else:
                nxt=row['omega'];assert nxt<j
                theta=(theta+3*t+3)%(1<<nxt);j=nxt
        return dict(status='work limit',word=word,types=types)
