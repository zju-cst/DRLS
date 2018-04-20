# -*- coding: utf-8 -*-

import random

class RandomGenerator:

    def __init__(self,seed,range,num):
        self.seed = seed
        self.range = range
        self.list = []
        self.num = num

    def GeneateRandom(self):
        for i in range(self.num):
            random.seed(self.seed)
            ran = random.uniform(0,self.range)
            res = round(ran,2)
            self.list.append(res)
            self.seed = res
        return self.list