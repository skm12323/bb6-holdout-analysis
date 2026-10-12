"""agentB_run6.py — spike aftermath structure for large v + dk(j) table."""
import sys
sys.path.insert(0, r'D:\math_cc\scratch')
from agentB_lib import *
from agentB_run5 import full_chain_data, kmap

def main():
    v = int(sys.argv[1]) if len(sys.argv) > 1 else 7000
    chains, ell = full_chain_data(v)
    tchains = [c for c in chains if c['p'] is not None]
    print('v=%d ell=%d chains=%d tchains=%d' % (v, ell, len(chains), len(tchains)))
    # dk(j), dp(j) table
    from collections import defaultdict
    tab = defaultdict(set)
    for c1, c2 in zip(tchains, tchains[1:]):
        tab[c1['j']].add((c2['k'] - c1['k'], c2['p'] - c1['p']))
    for j in sorted(tab):
        print('j=%2d -> (dk,dp) in %s' % (j, sorted(tab[j])))
    # spikes: j>=5: print full aftermath until next T-chain with its k
    print()
    done = 0
    for i, c in enumerate(chains):
        if c['j'] >= 9 and done < 6:
            done += 1
            print('--- spike chain %d: j=%d p=%s k=%s' % (i, c['j'], c['p'], c['k']))
            j2 = i
            while j2 < len(chains) and (j2 == i or chains[j2]['p'] is None or chains[j2]['p'] < (c['p'] or 0) + 4):
                cc = chains[j2]
                print('    chain %4d j=%2d b=%-8s c=%-8s p=%s k=%s' %
                      (j2, cc['j'], cc['btag'], cc['ctag'], cc['p'], cc['k']))
                j2 += 1
    # j=7 aftermath (the anomaly)
    for i, c in enumerate(chains):
        if c['j'] == 7:
            print('--- j=7 spike chain %d: p=%s k=%s' % (i, c['p'], c['k']))
            for j2 in range(i, min(i + 5, len(chains))):
                cc = chains[j2]
                print('    chain %4d j=%2d b=%-8s c=%-8s p=%s k=%s' %
                      (j2, cc['j'], cc['btag'], cc['ctag'], cc['p'], cc['k']))
            break

if __name__ == '__main__':
    main()
