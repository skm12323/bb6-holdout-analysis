"""Integer checks for the unreviewed CAP and conditional word-bound theorem."""
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'work_global_ext'/'route_c'))
from fdata import lam_walk, small_full
from sj import sym_beta


def main():
    rng = random.Random(20261018)
    checks = 0
    for l in list(range(64, 4097))+[8192, 16384]:
        b = (l-1).bit_length()
        g = l+2*b+7
        B = 1 << ((g+1)//2)
        C = (B+2)*(g+1)+2
        assert g+1 <= 2*l
        assert 8*l*l+24*l+1363 <= 9*l*l
        assert 768*l**3 < 1 << (l//2)
        for J in ((1 << (l-1))+1, 1 << l,
                  rng.randrange((1 << (l-1))+1, (1 << l)+1)):
            assert (J-1).bit_length() == l
            assert 1+9*J*l*l+J*(1+g*g) <= 16*J*l*l
            assert 96*J*l*l < 1 << g
            assert C <= J//(3*l)
            assert g < J and J//(3*l)+1 <= J
            checks += 1
    # Independently inspect actual beta histories with the proposed cap.
    # l<64 here is empirical only; no all-scale small-l claim is needed.
    N = 10000
    data = lam_walk(N+2)
    full = small_full(256)
    chains = 0
    for J in range(10, N+1):
        walk = sym_beta(J, data, full, 256)
        assert walk['status'] == 'end'
        l = (J-1).bit_length()
        g = l+2*(l-1).bit_length()+7
        assert all(j <= g for j in walk['js'][1:])
        chains += len(walk['js'])-1
    result = dict(result='PASS', review_status='unreviewed',
                  integer_parameter_checks=checks,
                  actual_symbolic_exits=N-9, actual_exit_chains=chains,
                  scope='CAP constants and finite beta runs only; the required all-Q word bound W is unproved.')
    Path(__file__).with_name('cap_checks.json').write_text(
        json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
