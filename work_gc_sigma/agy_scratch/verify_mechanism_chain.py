from fractions import Fraction

print("--- Step 1: Deep drift sets ---")
# BFS of Theta^E
T0 = {1}
T1 = {3 - 1, 1 - 1} | {1 + s for s in [-1, 0, 1]}
T2 = {3 - t for t in T1} | {t - 1 for t in T1} | {t + s for t in T1 for s in [-1, 0, 1]}
T3 = {3 - t for t in T2} | {t - 1 for t in T2} # S_2 is empty for level E

print("Theta^E_0:", sorted(T0))
print("Theta^E_1:", sorted(T1))
print("Theta^E_2:", sorted(T2))
print("Theta^E_3:", sorted(T3))
print("Is -2 in Theta^E_3?", -2 in T3)
print("a-landings 3 - theta for theta in Theta^E_3:", sorted({3 - t for t in T3}))
print("Is 5 in a-landings of Theta^E_3?", 5 in {3 - t for t in T3})

# Level C depth 1:
TC1 = {0, 1, 2}
print("a-landings of Theta^C_1:", sorted({3 - t for t in TC1}))
# Level D depth 2:
TD2 = set(range(-1, 4))
print("a-landings of Theta^D_2:", sorted({3 - t for t in TD2}))

print("\n--- Step 2: Gateway firing and recurrence ---")
delta_1 = Fraction(-1, 3)
print(f"delta_1 = {delta_1} = -3 + 8/3 = {Fraction(-3) + Fraction(8, 3)}")

d = delta_1
for r in range(1, 11):
    d_formula = Fraction(-3) + Fraction(8, 3**r)
    assert d == d_formula, f"Mismatch at r={r}: {d} vs {d_formula}"
    
    # Check mod 16
    # In Z/16Z:
    inv3 = pow(3, -1, 16)
    inv3_r = pow(inv3, r, 16)
    val_mod16 = (-3 + 8 * inv3_r) % 16
    assert val_mod16 == 5, f"mod 16 failure at r={r}: {val_mod16}"
    
    # Fire
    fire = (Fraction(15) - d) / Fraction(3)
    # Next delta (a-descendant)
    d_next = Fraction(3) - fire
    print(f"r={r:2d}: delta_r = {str(d):15s} mod 16 = {val_mod16} -> fire = {str(fire):18s} -> delta_{r+1} = {str(d_next):18s}")
    d = d_next

print("\nAll 10 steps verified exact and mod 16 == 5 holds universally!")
