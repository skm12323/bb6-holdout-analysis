"""Independent check of the canonical source data used in
work_c3_drift/ORBIT_SHIFT_OBSTRUCTION.md (background for the review of
SHIFT_TRANSPORT).  Does not run that document's verifier (which would write
into work_c3_drift/); recomputes the same canonical quantities read-only.
"""
from pathlib import Path
from fractions import Fraction as F
import sys, json

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'work_ext_roots'))
from verify_low_deficit import Calendar, first_fire, val


def main():
    cal = Calendar(512)
    inner = cal.preceding_fire_by_time(40)
    P = 49
    fire = first_fire(cal, P)
    sigma = fire['pointer']
    x0 = 6 * fire['k'] + 4
    y = 3 * x0 // 2 + 122
    A = (y - 10) // 16
    out = dict(
        inner_pointer=inner['pointer'], inner_k=inner['k'],
        fire_k=str(fire['k']), sigma=str(sigma), x0=str(x0),
        x0_is_5_2_49=(x0 == 5 * (1 << 49)),
        y=str(y), val_y=val(y), y_mod_128=int(y % 128),
        A=str(A), A_mod_8=int(A % 8), A_plus_1_below_2_48=(A + 1 < (1 << 48)),
        sigma_minus_5=str(sigma - 5),
        r_lower_bound=str(5 * (sigma - 53) // 8 + 1),
        r_lower_bound_quoted='657306078883964',
        consistent=(5 * (sigma - 53) // 8 + 1 == 657306078883964),
        eta_r_example_r0=str(F(-5) + F(8, 1)), eta_r_height='|eta_r|<=5 for r>=0 (r=0: 3)',
    )
    out['status'] = 'PASS' if (out['x0_is_5_2_49'] and out['A_mod_8'] == 7 and
                               out['val_y'] == 1 and out['consistent']) else 'FAIL'
    Path(__file__).with_name('orbit_source_recheck.json').write_text(
        json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
