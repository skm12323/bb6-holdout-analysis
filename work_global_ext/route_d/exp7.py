"""exp7 (Class B): every halting chain (synthetic defects and late-stage states) is at a type-a return."""
import tielab as T, collections, random
L=T.Lab(400); c=collections.Counter(); n=0
for J in range(3,41):
  for e in range(-300,301):
    for U in range(1,2000,2):
      if (U<<(J-1))-e<1: continue
      r=L.realrec(U,J,e); n+=1
      if r['st']=='HALT': c[(r['ch'][-1][0], len(r['ch']))]+=1
print('synthetic defects: runs',n,' halting chains by (return type, chain index):',dict(c))
