"""Shows the A5 -> A6 gap is not vacuous: the congruences defining an a-type bare tie (5,5)
and a resolved parameter m >= 2e7 are simultaneously solvable for arbitrary large j_T.

Existence only: 9 is invertible mod 2^K (K = 2e7+1), so k0 = -10/9 mod 2^K exists and is
unique.  Its residue mod 64 (computed from the inverse mod 64) shows k0 = 6 or 38 mod 64,
hence v2(3k0-2)=4, and 9k0+10 = 0 mod 2^K gives m >= K.  No large integer is materialised.
Writes gap_m.json.
"""
import json, sys

def v2(x):
    return (x & -x).bit_length() - 1

K = 2 * 10**7 + 1
k0_64 = (-10 * pow(9, -1, 1 << 64)) % (1 << 64)
res = {'K': K, 'k0_mod_64': k0_64, 'k0_mod_32': k0_64 % 32,
       'three_k_minus_2_mod_64': (3 * k0_64 - 2) % 64,
       'v2_3k_minus_2': v2((3 * k0_64 - 2) % (1 << 64)),
       'existence': 'gcd(9,2^K)=1: unique k0 with 9k0 = -10 (mod 2^K); k0 mod 64 as above',
       'm_lower_bound': K,
       'a_landing_param': 1 + 4,
       'theta_u_bare_tie': 5,
       'theta_after_gateway': 3 - 5,
       'reentry_note': ('chain u+1 has theta=-2 and j=m>=2e7+1 (deep again); after l deep '
                        'a/b steps |theta| <= 2+3l, so a later landing delta=3-theta can be '
                        'as low as 1-3l, outside [-12,15] already for l>=5')}
res['a_landing_is_5'] = res['v2_3k_minus_2'] == 4 and res['k0_mod_32'] == 6
with open(r'D:\math_cc\work_r1r2\agent_V\gap_m.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1))
