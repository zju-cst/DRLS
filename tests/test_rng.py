import unittest

from drls.rng import RandomGenerator


if __name__ == "__main__":
    dict = {'21751117': 1.0,'21751114': 1.0,'21751115': 1.0, '21751110': 1.0,'21751111': 1.0, '21751464': 1.0, '21751465': 1.0, '21751462': 1.0, '21751463': 1.0}
    res = RandomGenerator(1,9,5,dict)
    studs = res.GenerateResult()
    print studs