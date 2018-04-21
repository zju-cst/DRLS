# -*- coding: utf-8 -*-

import random

class RandomGenerator:

    def __init__(self,initSeed,range,num,students):
        self.initSeed = initSeed
        self.range = range
        self.list = []
        self.num = num
        self.students = students

    def GenerateResult(self):
        count = 0
        seed = self.initSeed
        while (count < self.num):
            ran = self.GeneateRandom(seed)
            #print ran
            stud = self.GetStudetByRandom(ran)
            bol = self.QueryResult(stud)
            if bol :
                self.list.append(stud)
                count += 1
            seed = ran
        return self.list

    def GeneateRandom(self,seed):
        random.seed(seed)
        ran = random.uniform(0,self.range)
        return ran

    def GetStudetByRandom(self,ranNum):
        for key in self.students:
            res = ranNum - self.students[key]
            if res < 0 :
                return key
            ranNum = res

    def QueryResult(self,stud):
        for i in self.list:
            if i == stud:
                return False
        return True