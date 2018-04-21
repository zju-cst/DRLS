# About

## 开发人员

- [terasum](https://github.com/terasum)
- [kjzz](https://github.com/kjzz)

## 算法说明

本程序采用随机区间算法，因为需要结合权重进行随机计算，并且要求给定随机种子的前提下，所有结果能够重现，因此设计采用坐标映射并随机取值的方式实现。

简要概括之，即：

首先将不同权重的学号，按照权重分配到一维坐标系上，例如权重为`1`的第`1`个同学，其随机范围为`[0,1)``,而权重为`1.3`的第2个同学，其随机范围为`[1,2.3)`依次类推。

首先利用给定的随机种子计算第一个随机数，判断其所在的区间，得到的第一个同学的学号，然后再利用这个同学得到的随机数作为下一轮随机的随机种子，计算第二个随机数，判断其所在的随机区间，得到第二个同学的学号，
依次类推。

如果随机到相同的同学，则利用新算出来的随机数作为新的种子，并跳过该同学，直到得到目标。

核心算法代码：


    def GetStudetByRandom(self,ranNum):
      for key in self.students:
        res = ranNum - self.students[key]
        if res < 0 :
          return key
        ranNum = res


本项目耗时两天，项目比较仓促，如有疑问，欢迎提[issue](https://github.com/zju-cst/DRLS/issues)
