import math

def P(n):
    return 2 * math.ceil(math.log2(6 * n**2 + 5))**2 + 1345

def B_star(g):
    term1 = 2 + math.log2(30 * g * P(g) + 29)
    term2 = 2 * math.ceil(math.log2(3 * g**2 + 4))
    return term1 + term2

def check_g(g):
    Pg = P(g)
    B = B_star(g)
    
    # Bound (I): 3 + log2(6*g*P(g))
    bound_I = 3 + math.log2(6 * g * Pg)
    
    # Bound (II-a): 2 + log2(3*g*P(g) + 3)
    bound_IIa = 2 + math.log2(3 * g * Pg + 3)
    
    # Bound (II-b): 2 + log2(21*g*P(g) + 20)
    bound_IIb = 2 + math.log2(21 * g * Pg + 20)
    
    # Bound (II-c): with max eps1 = 2*ceil(log2(3*g^2+4)) - 1
    max_eps1 = 2 * math.ceil(math.log2(3 * g**2 + 4)) - 1
    bound_IIc = 1 + max_eps1 + math.log2(30 * g * Pg + 29)
    
    # Check all <= B
    diff_I = B - bound_I
    diff_IIa = B - bound_IIa
    diff_IIb = B - bound_IIb
    diff_IIc = B - bound_IIc
    
    return {
        'g': g,
        'B': B,
        'bound_I': bound_I, 'diff_I': diff_I,
        'bound_IIa': bound_IIa, 'diff_IIa': diff_IIa,
        'bound_IIb': bound_IIb, 'diff_IIb': diff_IIb,
        'bound_IIc': bound_IIc, 'diff_IIc': diff_IIc,
        'all_pass': (diff_I > 0 and diff_IIa > 0 and diff_IIb > 0 and diff_IIc >= 1.0)
    }

print("Checking small and medium g:")
for g in [5, 6, 7, 8, 10, 15, 20, 50, 100, 500, 1000, 10000, 100000, 10**6, 10**8, 10**12]:
    r = check_g(g)
    print(f"g={g:12d}: B*={r['B']:.2f}, diff_I={r['diff_I']:.2f}, diff_IIb={r['diff_IIb']:.2f}, diff_IIc={r['diff_IIc']:.2f}, pass={r['all_pass']}")

# Exhaustive check for g in [5, 10000]
fails = 0
for g in range(5, 10001):
    r = check_g(g)
    if not r['all_pass']:
        fails += 1
print(f"\nExhaustive check g in [5, 10000]: {fails} failures.")
