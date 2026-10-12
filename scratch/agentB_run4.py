"""agentB_run4.py — analyze the spike-type sequence and skeleton periodicity."""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import *
from agentB_run3 import phase_run

def kind(tag):
    if tag == 'Z': return 'Z'
    if tag.startswith('T'): return 'T' if not tag.endswith('*') else 'T*'
    if tag.startswith('U'):
        parts = tag[1:].split('.')
        return 'U' + parts[1]      # U4 = 4th run entry (16u)
    if tag.startswith('D'): return 'D'
    return 'A'

def main():
    v = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    events, ell = phase_run(v)
    chains = []
    last_c = -1
    for ev in events:
        if ev[1] == 'C':
            t, _, j, u, D, btag, ctag, A = ev
            chains.append(dict(step=t, j=j, ub=u[1], ab=u[0], u=u, D=D,
                               bk=kind(btag), ck=kind(ctag), es=t - last_c - 1, A=A))
            last_c = t
    print('v=%d ell=%d nchains=%d' % (v, ell, len(chains)))
    jseq = [c['j'] for c in chains]
    print('jseq:', jseq)
    # spike positions: j >= 5
    spikes = [i for i, c in enumerate(chains) if c['j'] >= 5]
    print('spike chain indices:', spikes)
    print('spike j values   :', [chains[i]['j'] for i in spikes])
    print('spike spacing    :', [b - a for a, b in zip(spikes, spikes[1:])])
    # spike follow-up (next two j's)
    print('spike triples    :', [(chains[i]['j'], chains[i+1]['j'], chains[i+2]['j']) for i in spikes if i + 2 < len(chains)])
    # tail pointer at spikes: extract T index from btag
    def pidx(c):
        return c['bk']
    print('spike btags      :', )
    # skeleton check: j at positions mod 12 excluding spike slots
    # verify pattern: for i not in {7 mod 12 area}...
    # print detailed around first spikes
    print()
    print('first 30 chains: (j, bk, ck, Esteps)')
    for i, c in enumerate(chains[:30]):
        print('%3d j=%d %4s %4s es=%d  u=(%d)t+%d' % (i, c['j'], c['bk'], c['ck'], c['es'], c['u'][0], c['u'][1]))
    # event-kind sequence between chains for two consecutive periods
    print()
    ev_kinds = []
    ci = 0
    for ev in events:
        if ev[1] == 'E':
            ev_kinds.append(('E', kind(ev[2]), kind(ev[3])))
        else:
            ev_kinds.append(('C', ev[2], kind(ev[6]), kind(ev[7])))
    s0 = spikes[2] if len(spikes) > 2 else 0
    # find event index of chain s0 and s0+12
    def ev_index_of_chain(ci_target):
        cnt = 0
        for k, ek in enumerate(ev_kinds):
            if ek[0] == 'C':
                if cnt == ci_target:
                    return k
                cnt += 1
        return None
    a = ev_index_of_chain(spikes[1]); b = ev_index_of_chain(spikes[1] + 12); c2 = ev_index_of_chain(spikes[1] + 24)
    if a and b and c2:
        seg1 = ev_kinds[a:b]; seg2 = ev_kinds[b:c2]
        print('event segment lengths:', len(seg1), len(seg2))
        print('segments equal (ignoring spike j value)?:',
              [x if not (x[0]=='C' and x[1]>=5) else ('C','S') for x in seg1] ==
              [x if not (x[0]=='C' and x[1]>=5) else ('C','S') for x in seg2])
        print('seg1:', seg1)
        print('seg2:', seg2)

if __name__ == '__main__':
    main()
