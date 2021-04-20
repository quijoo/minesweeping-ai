import random
from  game.utils import CountToPostion
from game.unit import *
import time
class CGrids:
    
    def __init__(self, length, boomNum):
        self.m_UnitMetrix = [[None for _ in range(length) ] for _ in range(length)]
        
        CGrids.m_BoomNum = boomNum
        CGrids.m_leave = length * length
        self.m_Size = length
        self.InitGrids()
    
    def InitGrids(self):
        # 蓄水池抽样
        self.m_BoomNum = CGrids.m_BoomNum
        self.m_leave = CGrids.m_leave
        
        pool = []
        for index in range(self.m_Size**2):
            i, j = CountToPostion(index, self.m_Size)
            
            self.m_UnitMetrix[i][j] = CUnit(False)
            
            if index < self.m_BoomNum:
                pool.append(self.m_UnitMetrix[i][j])
                continue

            random.seed()
            rNum = random.randint(0, self.m_Size**2-1)
            if rNum < self.m_BoomNum:
                pool[rNum] = self.m_UnitMetrix[i][j]
        
        for item in pool:
            item.m_Boom = True

    def CheckSuccess(self):
        # 胜利条件：
        # 1. 标记了所有雷
        # 2. 剩余格子数等于雷数
        return self.m_leave <= self.m_BoomNum

    def __repr__(self):
        ReturnList = [[0 for _ in range(self.m_Size)] for _ in range(self.m_Size)]
        
        for i, line in enumerate(self.m_UnitMetrix): 
            ReturnList[i] = list(map(lambda x:x.__repr__(), self.m_UnitMetrix[i]))

        return ReturnList

    def __str__(self):
        return_str = ""
        # 打印头部
        for i in range(self.m_Size):
            return_str += str(i).ljust(2)
        return_str += "\n"
        
        # 分割线
        for _ in range(self.m_Size):
            return_str += "--".ljust(2)
        return_str += "\n"

        # 打印内容
        for index, line in enumerate(self.m_UnitMetrix):
            for item in line:
                return_str += "{} ".format(item.__str__())
            return_str += "|{}\n".format(str(index).ljust(2))
        
        return return_str

    def __getitem__(self, i):
        return self.m_UnitMetrix[i]

    def NeiborIter(self, x, y):
        # 返回除开自己的 8 个邻居
        for i in range(max(0, x-1), min(x+2, self.m_Size)):
            for j in range(max(0, y-1), min(y+2, self.m_Size)):
                
                if i == x and j == y:
                    continue
                yield i, j, self.m_UnitMetrix[i][j]