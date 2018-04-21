# -*- coding: utf-8 -*-
from drls.rng import RandomGenerator
from drls.utils import read_excel, cal_range
from drls.utils import app_dir


#主程序测试
if __name__ == "__main__":
    #爬取所有数据并去重
    dict = read_excel(app_dir() + "/data/test.xls")
    #计算权重合
    sum = cal_range(dict)
    #初始化随机类
    #四个参数分别为 初始化随机种子，所有权重集合，选取的个数，以及学生集合
    res = RandomGenerator(1238,sum,10,dict)
    #产生结果
    studs = res.GenerateResult()
    #输出
    print studs
