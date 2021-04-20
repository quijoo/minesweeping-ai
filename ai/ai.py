
from random import random
import time
import random

from game.defines import *
from game import utils
import subprocess
from ai import  gauss
# utils
def NeiborIter(i, j, size):
    for x in range(max(0, i-1), min(i+2, size)):
        for y in range(max(0, j-1), min(j+2, size)):
            if x == i and y ==j:continue
            yield (x, y)

class AI:
    RandomCounter = 0
    @staticmethod
    def Process(lStateMatrix:list, iBoom)->list:
        """
        1. 剩余 unknown 数量为 n
        2. 剩余 雷 数量为 iBoom
        """
        random.seed(time.time())
        # 1. 拆分区域 list(set(tuple(x, y)))
        lBlockList = AI.BlockSplit(lStateMatrix)
        if AI.RandomCounter < 2 or len(lBlockList) == 0:
            AI.RandomCounter += 1
            return AI.RandomSelect(AI.RandomCounter, len(lStateMatrix))

        DelSetList, ReturnList = AI.Pruning(lBlockList, lStateMatrix)
        if ReturnList:return True, ReturnList

        # 有安全解直接返回
        ReturnList, lBlockCnt, lCellCnt = AI.SituationEnumerate(lStateMatrix, lBlockList, iBoom, DelSetList)
        if ReturnList:return True, ReturnList
        
        if not lBlockCnt:
            AI.RandomCounter += 1
            return AI.RandomSelect(AI.RandomCounter, len(lStateMatrix)) 

        dp = AI.SituationCombin(lBlockCnt)
        
        res = AI.GlobalProbability(dp, lBlockList, lBlockCnt, lCellCnt, iBoom)

        return AI.ResultClear(res, len(lStateMatrix))

    @staticmethod
    def RandomSelect(RandomCounter, size):
        x, y = -1, -1

        if RandomCounter % 4 == 0:
            x = random.randint(0, size/2-1)
            y = random.randint(0, size/2-1)
        elif RandomCounter% 4 == 1:
            x = random.randint(size/2, size-1)
            y = random.randint(size/2, size-1)
            
        elif RandomCounter% 4 == 2:
            x = random.randint(size/2, size-1)
            y = random.randint(0, size/2-1)
            
        elif RandomCounter% 4 == 3:
            x = random.randint(0, size/2-1)
            y = random.randint(size/2, size-1)
        return True, [(x, y)]

    @staticmethod
    def ResultClear(lResPoint:list, iSize):
        ReturnList= []
        min, xi, yi = 100, -1, -1
        for x, y, up, down in lResPoint:
            if down:
                if up == 0:ReturnList.append((x, y))
                if min > up/down:
                    min = up/down
                    xi, yi = x, y

        if not ReturnList:
            if xi == -1:
                return True, [(random.randint(0, iSize-1), random.randint(0, iSize-1))]
            else:
                return True, [(xi, yi)]
        else:
            return False, ReturnList

    @staticmethod
    @utils.timer
    def BlockSplit(lStateMatrix)->list:
        # 能通过一个 Number 相连接的 Unknown 单元格在同一个block 内
        iWidth = len(lStateMatrix)
        lVisit = [[False for _ in range(iWidth)] for _ in range(iWidth)]
        lBlockList = []
        # 深度优先
        def Visit(x, y, state):
            nonlocal lVisit, lStateMatrix, lBlockList

            if lVisit[x][y]:return

            lVisit[x][y] = True
            
            if state == UNIT_UNKNOWN:
                lBlockList[-1]["unknown"].add((x, y))
                
                for x_i, y_i in NeiborIter(x, y, iWidth):
                    if lStateMatrix[x_i][y_i] < UNIT_NUM:
                        Visit(x_i, y_i, lStateMatrix[x_i][y_i])

            if state < UNIT_NUM:                
                lBlockList[-1]["num"].add((x, y))
                
                for x_i, y_i in NeiborIter(x, y, iWidth):
                    if lStateMatrix[x_i][y_i] == UNIT_UNKNOWN:
                        Visit(x_i, y_i, lStateMatrix[x_i][y_i])
            
        # 对每一个未访问的 num 进行深度优先搜索
        for i, line in enumerate(lStateMatrix):
            for j, state in enumerate(line):
                if state < UNIT_NUM and not lVisit[i][j]:
                    lBlockList.append({"unknown":set(), "num":set()})
                    Visit(i, j, state)
                    if not lBlockList[-1]["num"]:lBlockList.pop()
        return lBlockList

    @staticmethod
    def CheckSum(i, j, Matrix):
        s = 0
        for xx, yy in NeiborIter(i, j, len(Matrix)):
            s += (Matrix[xx][yy] == UNIT_BOOM)
        
        return s == Matrix[i][j]

    @staticmethod
    @utils.timer
    def Pruning(BlockList, lStateMatrix):

        def _Pruning(NumList):
            nonlocal lStateMatrix
            CntSet, iSize = set(), -1
            while len(CntSet) != iSize:
                iSize = len(CntSet)
                for x, y in NumList:
                    
                    UnknowCnt, BoomCnt = 0, 0
                    for i, j in NeiborIter(x, y, len(lStateMatrix)):
                        UnknowCnt += (lStateMatrix[i][j] == UNIT_UNKNOWN)
                        BoomCnt += (lStateMatrix[i][j] == UNIT_BOOM)
                    
                    if lStateMatrix[x][y] == UnknowCnt + BoomCnt:
                        for i, j in NeiborIter(x, y, len(lStateMatrix)):
                            if lStateMatrix[i][j] == UNIT_UNKNOWN:
                                lStateMatrix[i][j] = UNIT_BOOM
                                CntSet.add((i, j))
                    
                    if lStateMatrix[x][y] == BoomCnt:
                        for i, j in NeiborIter(x, y, len(lStateMatrix)):
                            if lStateMatrix[i][j] == UNIT_UNKNOWN:
                                lStateMatrix[i][j] = UNIT_SAFE
                                CntSet.add((i, j))
            return CntSet
        
        DelSetList = []
        ReturnList = []
        for lBlock in BlockList:
            DelSet = _Pruning(lBlock["num"])
            DelSetList.append(DelSet)
            for x, y in DelSet:
                if lStateMatrix[x][y] == UNIT_SAFE:
                    ReturnList.append((x, y))
        return DelSetList, ReturnList
    
    @staticmethod
    @utils.timer
    def SituationEnumerate(lStateMatrix:list ,BlockList:list, surplus:int, DelSetList)->list:  
        # 有安全解进行下一步， 没有安全解就枚举
        lBlockCnt = [[0 for _ in range(surplus + 1)] for _ in range(len(BlockList))]
        
        lCellCnt = [[[0 for _ in range(surplus + 1)] for _ in range(len(lStateMatrix))] for _ in range(len(lStateMatrix))]
        
        def _Enumerate(ii, Unk, Num, Matrix, DelSet):
            # 如果有安全解则返回安全解， 如果没有安全解进行枚举 
            nonlocal lCellCnt, lBlockCnt, surplus
            iter = gauss.GuassSolve(Unk=Unk, Num=Num, lStateMatrix=Matrix, Del=DelSet)
            
            if isinstance(iter, list):return iter
            
            for situation in iter:
                for index, value in enumerate(situation):
                    x, y = Unk[index]
                    Matrix[x][y] = UNIT_BOOM if value else UNIT_SAFE
                for x, y in Num:
                    if not AI.CheckSum(x, y, Matrix):
                        break
                else:
                    sur = sum(situation)
                    lBlockCnt[ii][int(sur)] += 1
                    for x, y in Unk:
                        lCellCnt[x][y][int(sur)] += Matrix[x][y] == UNIT_BOOM
                    for x, y in DelSet:
                        lCellCnt[x][y][int(sur)] += Matrix[x][y] == UNIT_BOOM
            return []
                            
        # 在 Enumerate 枚举部分交给 cpp
        for ii, lBlock in enumerate(BlockList):
            UnknowSet = lBlock["unknown"]
            NumSet = lBlock["num"]
            DelSet= DelSetList[ii]    
            UnknowSet -= DelSet


            if CPP_ENUMERATE:

                if len(UnknowSet) > 24:
                    return None, None
                sCmdLineArg = AI.CppInerface(surplus, lStateMatrix, UnknowSet, DelSet, NumSet)
                
                _, out= subprocess.getstatusoutput("Enumerate.exe " + sCmdLineArg)
                
                AI.CppUnpack(ii, out, lBlockCnt, lCellCnt)

            elif GAUSS_ENUMERATE:
                ReturnList = _Enumerate(ii, list(UnknowSet), list(NumSet), lStateMatrix, list(DelSet))
                if ReturnList:return ReturnList, None, None

        return [], lBlockCnt, lCellCnt

    # dp
    @staticmethod
    @utils.timer
    def SituationCombin(lBlockCnt:list):
        dps = []
        surplus = len(lBlockCnt[0])
        if len(lBlockCnt) == 1:
            return [[[1 for _ in range(surplus)]]]
        for ii in range(len(lBlockCnt)):
            tmp = lBlockCnt.pop(ii)
            n = len(lBlockCnt)
            
            dp = [[0 for _ in range(surplus)] for _ in range(n)]
            dp[0] = lBlockCnt[0]
            for i in range(1, n):
                for j in range(surplus):
                    for s in range(0, j+1):
                        dp[i][j] += dp[i-1][j-s] * lBlockCnt[i][s]
            lBlockCnt.insert(ii, tmp)
            dps.append(dp)
        return dps

    @staticmethod
    @utils.timer
    def GlobalProbability(dp, BlockList, lBlockCnt, lCellCnt, surplus)->list:
        lProbability = []
        for ii, lBlock in enumerate(BlockList):
            UnknowList = lBlock["unknown"]

            for x, y in UnknowList:
                iFracUp, iFracDown = 0, 0
                for mine in range(surplus + 1):
                    for s in range(mine + 1):
                        iFracUp += lCellCnt[x][y][s] * dp[ii][-1][mine-s]
                        iFracDown += lBlockCnt[ii][s] * dp[ii][-1][mine-s]
                lProbability.append((x, y, iFracUp , iFracDown))

        return lProbability


    @staticmethod
    def CppInerface(surplus, Matrix, UnknowList, DelList, NumList):
        sMatrix = []
        for line in Matrix:
            for v in line:
                sMatrix.append(str(v))
        sMatrix = " ".join(sMatrix)
        
        sUnknowList = []
        for x, y in UnknowList:
            sUnknowList.append(str(x))
            sUnknowList.append(str(y))
        sUnknowList = " ".join(sUnknowList)

        sDelList = []
        for x, y in DelList:
            sDelList.append(str(x))
            sDelList.append(str(y))
        sDelList = " ".join(sDelList)

        sNumList = []
        for x, y in NumList:
            sNumList.append(str(x))
            sNumList.append(str(y))
        sNumList = " ".join(sNumList)


        data = "{surplus} {size} {Matrix} {Usize} {UnknowList} {Dsize} {DelList} {Nsize} {NumList}".format(
            surplus=surplus, size = len(Matrix), Matrix = sMatrix, 
            Usize=len(UnknowList), UnknowList = sUnknowList, 
            Dsize=len(DelList), DelList=sDelList,
            Nsize=len(NumList),NumList=sNumList 
        )
        return data

    @staticmethod
    def CppUnpack(BlockIndex, sData, lBlockCnt, lCellCnt):
        lData = list(map(int, sData.split()))
        BlockCntSize = lData[0]
        lBlockCnt[BlockIndex] = lData[1:BlockCntSize+1]
        size = lData[BlockCntSize+1]
        surplus = lData[BlockCntSize+2]
        
        lData, cnt = lData[BlockCntSize+3:-1], 0
        for i in range(size):
            for j in range(size):
                for k in range(surplus):
                    lCellCnt[i][j][k] += lData[cnt]
                    cnt += 1
        CppTime = lData[-1] / 1000
        print("[Timer analyze] CppInterface cost {}s.".format(CppTime))


def main():
    lStateMatrix = [[3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 1, 1, 1, 3, 3000], [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 4, 3, 3000, 5, 3000], [2, 4, 3000, 3, 3, 3000, 3, 3, 3000, 3000, 3000, 3000, 3000, 3, 3000, 3000], [1, 3000, 2, 1, 1, 1, 1, 1, 2, 3, 4, 4, 3, 2, 2, 2], [1, 1, 1, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1, 3000, 1, 2000, 1, 1], [2000, 2000, 2000, 2000, 1, 1, 1, 2000, 2000, 2000, 1, 1, 1, 2000, 1, 3000], [2000, 2000, 2000, 1, 2, 3000, 1, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2, 2], [2000, 2000, 2000, 1, 3000, 2, 1, 2000, 1, 1, 1, 2000, 2000, 2000, 2, 3000], [2000, 2000, 2000, 1, 1, 1, 2000, 2000, 1, 3000, 1, 1, 1, 1, 3, 3000], [2000, 2000, 2000, 2000, 1, 1, 1, 1, 2, 2, 1, 1, 3000, 1, 2, 3000], [1, 1, 2, 1, 2, 3000, 2, 2, 3000, 2, 2, 2, 2, 1, 1, 1], [1, 3000, 2, 3000, 3, 2, 2, 3000, 4, 3000, 2, 3000, 2, 1, 2000, 2000], [1, 1, 2, 3, 3000, 2, 1, 2, 3000, 2, 2, 2, 3000, 2, 1, 2000], [1, 1, 2000, 2, 3000, 2, 2000, 1, 1, 1, 1, 2, 3, 3000, 1, 2000], [3000, 1, 2000, 1, 1, 1, 2000, 2000, 2000, 2000, 1, 3000, 3, 3, 3, 1], [1, 1, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1, 1, 2, 3000, 3000, 1]]

    for line in lStateMatrix:
        for v in line:
            if v == UNIT_EMPTY:print(" ", end=" ")
            elif v == UNIT_UNKNOWN:print("?", end=" ")
            else:print(v, end=" ")
        print()
    print(lStateMatrix)
    lBlockList = AI.BlockSplit(lStateMatrix)

    DelSetList, ReturnList = AI.Pruning(lBlockList, lStateMatrix)
    if ReturnList:
        return ReturnList
    
    # Surplus is a max value.
    lBlockCnt, lCellCnt = AI.SituationEnumerate(lStateMatrix, lBlockList, 50, DelSetList)
    
    dp = AI.SituationCombin(lBlockCnt)
    
    res = AI.GlobalProbability(dp, lBlockList, lBlockCnt, lCellCnt, 50)
    return res

if __name__ == "__main__":
    print(main())

