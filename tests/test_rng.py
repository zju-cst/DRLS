import unittest

from drls.rng import RandomGenerator


class TestRng(unittest.TestCase):

    def test_GeneateRandom(self):
        r1 = RandomGenerator(1,10,1)
        ran1 = r1.GeneateRandom()
        r2 = RandomGenerator(1,10,1)
        ran2 = r2.GeneateRandom()
        self.assertEqual(ran1[0],ran2[0])

if __name__ == "__main__":
    t = TestRng()
    ran = t.test_GeneateRandom()