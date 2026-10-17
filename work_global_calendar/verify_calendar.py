"""Compare the compressed calendar with direct canonical pair evolution."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from calendar_oracle import Calendar,vm,val

calendar=Calendar(4096)
direct=vm.Xdata(8192,SMALL=8192)
for n,(typ,H,Y,e) in direct.items():
    row=calendar.crossing(n)
    t=(H[1]+(Y[1] if Y else 0)-1)//3
    odd=sum(H)%2==1
    assert row==dict(kind=typ,time=t,epsilon=e,odd=odd,
                    omega=val(H[1]+2*(Y[1] if Y else 0)+3) if odd else None,
                    head_ratio=F(H[0],1<<n),head_lambda=H[1],
                    tail_ratio=F(Y[0],1<<n) if Y else None,tail_lambda=Y[1] if Y else None),(n,row)

# Compare calendar fire indices against an ordinary finite kernel walk.
k=1;rho=4;finite_fires=0
while 2*k<20000:
    f=calendar.preceding_fire_by_time(2*k)
    assert (f['k'],f['pointer'],f['index'])==(k,rho,finite_fires)
    J=1+val(3*k+2);ker=calendar.kernels[J]
    k+=ker['delta'];rho+=ker['advance'];finite_fires+=1

# Run epoch_crossings (asserting delta, advance, mass) at one actual fire of every J<=B.
kernel_epochs_checked=0
for J in range(1,calendar.B+1):
    h=(-2*pow(3,-1,1<<max(J-1,1)))%(1<<max(J-1,1)) if J>1 else 1
    for t in range(16):
        kk=h+t*(1<<max(J-1,1))
        if kk<1 or 1+val(3*kk+2)!=J or 2*kk>=2*calendar.boundary_k: continue
        f=calendar.preceding_fire_by_time(2*kk)
        if f['k']==kk:
            calendar.epoch_crossings(f); kernel_epochs_checked+=1; break
assert kernel_epochs_checked==calendar.B,(kernel_epochs_checked,calendar.B)

large=[]
for bits,offset in ((64,123),(256,12345),(1024,54321),(4094,98765)):
    n=(1<<bits)+offset;f=calendar.preceding_fire_by_pointer(n);row=calendar.crossing(n)
    tf=calendar.preceding_fire_by_time(2*f['k'])
    assert tf['pointer']==f['pointer'] and tf['index']==f['index']
    assert row['time']>=2*f['k']
    raw=row['time'].to_bytes((row['time'].bit_length()+7)//8,'big')
    large.append(dict(pointer_power=bits,pointer_offset=offset,kind=row['kind'],
                      epsilon=row['epsilon'],omega=row['omega'],
                      time_bits=row['time'].bit_length(),time_sha256=hashlib.sha256(raw).hexdigest(),
                      enclosing_fire_parameter=f['J'],navigation_jumps=f['jumps']))

for n,t in ((122435,109228),(367353,327724)):
    row=calendar.crossing(n)
    assert row['kind']=='a' and row['time']==t and row['odd']
minimal_17_time=(5*(1<<17)-4)//3
record=calendar.preceding_fire_by_time(minimal_17_time)
assert 2*record['k']==minimal_17_time and record['J']==17
assert record['pointer']==244873
assert calendar.crossing(244874)['omega']==17

for J in range(1,257):
    projected=calendar.projected_epoch(J)
    expected=calendar.kernels[J]
    assert projected['status']=='closed'
    assert tuple(projected['word'])==expected['word']
    assert all(projected[k]==expected[k] for k in ('delta','advance','loss','types'))
large_kernels=[]
for bits,offset in ((64,124),(256,12346),(1024,54322)):
    J=(1<<bits)+offset;kernel=calendar.projected_epoch(J)
    assert kernel['status']=='closed'
    large_kernels.append(dict(parameter_power=bits,parameter_offset=offset,
                             later_parameters=kernel['word'][1:],types=kernel['types'],
                             total_loss=kernel['loss'],half_duration_bits=kernel['delta'].bit_length()))
result=dict(result='PASS',kernel_cutoff=calendar.B,max_kernel_loss=calendar.max_kernel_loss,
            direct_crossing_comparisons=len(direct),finite_fire_comparisons=finite_fires,
            boundary_time_bits=(2*calendar.boundary_k).bit_length(),
            boundary_pointer_bits=calendar.boundary_pointer.bit_length(),large_queries=large,
            known_large_source_checks=2,minimal_parameter17_fire=dict(time=minimal_17_time,pointer=record['pointer']),
            kernel_crosschecks=256,kernel_epochs_checked=kernel_epochs_checked,isolated_large_kernels=large_kernels,
            scope='Exact canonical data only before the first fire above the certified kernel cutoff; no global extension')
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
