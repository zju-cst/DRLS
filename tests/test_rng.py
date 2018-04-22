import unittest

from drls.rng import RandomGenerator
from drls.utils import cal_range


if __name__ == "__main__":
    dict = {'21751117': 100.0,'21751114': 1.0,'21751115': 1.0, '21751110': 1.0,'21751111': 1.0, '21751464': 1.0, '21751465': 1.0, '21751462': 1.0, '21751463': 1.0}
    sum  = cal_range(dict)
    res = RandomGenerator(1,sum,1,dict)
    studs = res.GenerateResult()
    print studs