"""Scratch: print canonical crossing data at small n, especially n=4 (parameter five).

Read-only use of the accepted calendar oracle. No files outside this scratch dir.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_global_calendar'))
from calendar_oracle import Calendar, val

cal = Calendar(64)
print('crossings n=0..12 (n = parameter-1):')
for n in range(0, 13):
    r = cal.crossing(n)
    print(f'n={n:2d} j={n+1:2d} odd={r["odd"]} kind={r["kind"]!r} '
          f'time={r["time"]} epsilon={r["epsilon"]} omega={r["omega"]}')
r4 = cal.crossing(4)
print('\nX(4):', r4)
print('claim: X(4) odd type a, half-time k_5 = tau(4)/2 =', r4['time'] // 2,
      ', tau(4)=', r4['time'])
print('3*time % 2 == 0 (so integer half-time):', r4['time'] % 2 == 0)
# Parameter-five a-step constant check: x=32u -> y = 48u + 2D + 6, D' = 3-D-16u.
# identity 3D' = 15-D-y
for u in (1, 3, 5, 7):
    for D in (0, 1, -1, 5, 1234567, -(1 << 20)):
        x = 32 * u
        th = x + D
        y = 2 * th + 6 - x // 2
        t = th + 9
        assert 3 * (t - y) == 15 - D - y
print('\nidentity 3D\'=15-D-y verified on 24 exact states')
