"""Incremental exact pure-A clock cylinders, with no large Fraction slopes.

All integer lifts are retained. Sources must be supplied independently.
This is an arithmetic search, not a reachability or global certificate.
"""
from dataclasses import dataclass


def val(x):
    return (abs(x) & -abs(x)).bit_length()-1 if x else 10**30


@dataclass(frozen=True)
class Cylinder:
    i: int = 0
    B: int = 0
    C: int = 0
    elapsed: int = 0
    p: int = 0
    r: int = 0
    bits: int = 0
    clock: int = 0
    clock_bits: int = 0

    def append(self, q, k):
        """Constrain current valuation to q, then advance its a map."""
        sign = 1 if self.i % 2 == 0 else -1
        h = self.i+q+1
        p = -sign*self.B
        r = (sign*((1 << (h-1))-self.C)) & ((1 << h)-1)
        clock, cbits = self.clock, self.clock_bits
        if self.bits:
            common = min(h, self.bits)
            d = p-self.p
            e = (self.r-r) & ((1 << common)-1)
            s = min(val(d), common)
            if e & ((1 << s)-1):
                return None
            if s < common:
                nb = common-s
                overlap = min(nb, cbits)
                trial = (1 << min(overlap,64))-1
                trial_low = (((e >> s) & trial)*pow(d >> s,-1,trial+1)) & trial
                if trial_low != (clock & trial):
                    return None
                mask = (1 << overlap)-1
                low = (((e >> s) & mask)*pow(d >> s, -1, mask+1)) & mask
                if low != (clock & mask):
                    return None
                if nb > cbits:
                    nr = ((e >> s)*pow(d >> s, -1, 1 << nb)) & ((1 << nb)-1)
                    clock, cbits = nr, nb
        if self.bits > h:
            p, r, h = self.p, self.r, self.bits
        return Cylinder(self.i+1, -self.B+(1 << (self.i+2)),
                        -self.C+(6*self.elapsed+6*k)*(1 << (self.i+1)),
                        self.elapsed+1+2*k, p, r, h, clock, cbits)

    def fire(self):
        """The exact fire-rooted time cylinder, or None."""
        modulus = 1 << self.bits
        trial = (1 << min(self.clock_bits,64))-1
        trial_low = (((self.r+1) & trial)*pow(1-self.p,-1,trial+1)) & trial
        if trial_low != (self.clock & trial):
            return None
        cm = 1 << self.clock_bits
        low = ((self.r+1)*pow(1-self.p, -1, cm)) & (cm-1)
        if low != self.clock:
            return None
        theta = ((self.r+1)*pow(1-self.p, -1, modulus)) & (modulus-1)
        return ((theta-5)*pow(3, -1, modulus)) & (modulus-1), self.bits
