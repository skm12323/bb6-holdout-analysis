# trace_top_map.py
from independent_verify import top_step

# For v = 5, w = 1:
# E(w, v) from work_r4/PROOF.md lines 20-22:
# n+2 = 2^v * w = 2^5 * 1 = 32 => n = 30
# E(w, v) = (3w+1, 3w, 6w, ..., 3w*2^(v-2), 3w*2^(v-1) - 1)
# For v=5, w=1:
# 3w+1 = 4
# 3w = 3
# 6w = 6
# 3w*2^1 = 6*2 = 12
# 3w*2^2 = 24
# 3w*2^3 - 1 = 48 - 1 = 47
# Wait! Let's check S3 formula:
# L_{n+1} = E(w,v) := (3w+1, 3w, 6w, ..., 3w*2^(v-2), 3w*2^(v-1) - 1)
# For v=5, w=1:
# 3w*2^0 = 3
# 3w*2^1 = 6
# 3w*2^2 = 12
# 3w*2^3 = 24
# 3w*2^4 - 1 = 48 - 1 = 47
# Wait, how many entries?
# Let's check n=30 in our top map simulation!

L = [3]
for n in range(31):
    status, L = top_step(L)
    if n == 30:
        print(f"At n={n}, L_{n} = {L}")
    if n == 31:
        print(f"At n={n} (excursion start), L_{n} = {L}")

# Now trace from L_31 until singleton:
step = 0
while True:
    print(f"step {step}: L = {L}, len = {len(L)}")
    if len(L) == 1 and step > 0:
        print(f"Reached singleton at step {step}!")
        break
    status, L = top_step(L)
    step += 1
