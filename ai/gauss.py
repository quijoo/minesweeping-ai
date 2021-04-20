# https://blog.csdn.net/u011815404/article/details/88890702
# 高斯消元法

from game.defines import UNIT_BOOM


def GCD(a:int, b:int):
    return a if not b else GCD(b, a%b)

def LCM(a:int, b:int):
    return a*b/GCD(a, b)

# 函数包装器, 延后执行
class Function:
    def __init__(self, func, *args) -> None:
        self.func = func
        self.args = args
    def __call__(self, free_list):
        return self.func(free_list, *self.args)

    def __str__(self) -> str:
        return "func"
    
    def __repr__(self) -> str:
        return self.__str__()

def Gauss(a:list):
    # 转化为阶梯型
    equ, var = len(a), len(a[0])-1
    col, row = 0, 0
    while row < equ and col < var:
        maxRow = row
        for i in range(row+1, equ):
            if abs(a[i][col]) > abs(a[maxRow][col]):
                maxRow = i
        if maxRow != row:
            a[row],a[maxRow] = a[maxRow], a[row]

        if a[row][col]==0:
            col+=1
            continue


        for i in range(row+1, equ):
            if a[i][col]:
                # lcm=LCM(abs(a[i][col]),abs(a[row][col]))
                # ta=lcm/abs(a[i][col])
                # tb=lcm/abs(a[row][col])
                # if a[i][col]*a[row][col]<0:
                #     tb=-tb

                temp=a[i][col]/a[row][col]
                for j in range(col, var+1):
                    a[i][j]-=a[row][j]*temp
                    # a[i][j]=a[i][j]*ta-a[row][j]*tb

        row += 1
        col += 1
    return a


def Regular(A):
    freeX = [True for _ in range(len(A[0])-1)]
    for curent_line_index, curent_line in enumerate(A):
        first = 0
        while first < len(curent_line)-1 and curent_line[first] == 0:
            first+=1
        
        
        if first == len(curent_line) - 1:
            if curent_line[-1] != 0:
                PrintMatrix(A)
                print("wrong.")
            break
        
        freeX[first] = False
        
        first_value = curent_line[first]
        
        # 主元归一化
        for i in range(first, len(curent_line)):
            curent_line[i] /= first_value 
        first_value = 1
        
        for back_line_index in range(0, curent_line_index):
            back_value = A[back_line_index][first]

            for thro in range(len(A[back_line_index])):
                A[back_line_index][thro] -= A[curent_line_index][thro] / first_value * back_value
    return freeX, A

# 依赖函数
def _func(free_value_list, b, free_dep_list):
    for index, parm in free_dep_list:
        b -= parm * free_value_list[index]
    return b

def SolveReMatrix(A, freeX):
    equ, var = len(A), len(A[0]) - 1
    cur_line_index = 0
    cur_var_index = 0
    X = [-1 for _ in range(len(A[0]) - 1)]
    while cur_line_index < equ:
        dep_list = []
        k = cur_var_index
        # 1. 找到第一个 1 且不是自由元的x, 并记录当前x下标(不可能有无解的情况)
        while k < var:
            if A[cur_line_index][k] == 1 and not freeX[k]:
                break
            k +=1
        if k == var:
            # 该问题不可能无解, 如果当前行为空, 直接进行下一行
            cur_line_index += 1
            continue

        cur_var_index = k
        k += 1
        # 2. 找到 该非自由元依赖的所有变量(可能是固定值/自由元)
        while k < var:
            if A[cur_line_index][k] != 0:
                dep_list.append((k, A[cur_line_index][k]))
            k += 1
        
        # 3. 如果依赖的变量为空, 那么他是一个确定值
        if not dep_list:
            X[cur_var_index] = A[cur_line_index][-1]
        
        # 4. 否则 构建依赖函数
        else:
            X[cur_var_index] = Function(_func, A[cur_line_index][-1], dep_list)

        cur_line_index += 1
    return X
import time
def BuildAugmentedMatrix(NumList, UnknowList, DelList, lStateMatrix):
    AMatrix = [[0 for _ in range(len(UnknowList) + 1)] for _ in range(len(NumList))]

    for i, (xi, yi) in enumerate(NumList):
        for j, (xj, yj) in enumerate(UnknowList):
            if -1 <= xi - xj <= 1 and -1 <= yi - yj <= 1:
                AMatrix[i][j] = 1

        AMatrix[i][-1] += lStateMatrix[xi][yi]
        

        for j, (xj, yj) in enumerate(DelList):
            if -1 <= xi - xj <= 1 and -1 <= yi - yj <= 1:
                if lStateMatrix[xj][yj] == UNIT_BOOM:
                    AMatrix[i][-1] -= 1

    
    # del_queue = []
    # for i in range(len(AMatrix)):
    #     for j in range(len(AMatrix[0])):
    #         if AMatrix[i][j] != 0:
    #             break
    #     else:
    #         del_queue.append(i)
    # del_queue.reverse()
    # for i in del_queue:AMatrix.pop(i)
    return AMatrix

# def GetX():
#     A = [[0 for _ in range(24)] for _ in range(16)]
#     A[0][0],A[0][1],A[0][2],A[0][3],A[0][4]=1,1,1,1,1
#     A[1][3],A[1][4],A[1][5]=1,1,1
#     A[2][4],A[2][5],A[2][6]=1,1,1
#     A[3][5],A[3][6],A[3][7]=1,1,1
#     A[4][6],A[4][7],A[4][8]=1,1,1
#     A[5][7],A[5][8],A[5][9],A[5][10],A[5][11] =1,1,1,1,1
#     A[6][10],A[6][11],A[6][12]=1,1,1
#     A[7][11],A[7][12],A[7][13],A[7][14],A[7][15]=1,1,1,1,1
#     A[8][14],A[8][15],A[8][16]=1,1,1
#     A[9][15],A[9][16]=1,1
#     A[10][16]=1

#     A[11][16],A[11][17],A[11][18],A[11][19]=1,1,1,1

#     A[12][18],A[12][19],A[12][20]=1,1,1
#     A[13][19],A[13][20],A[13][21],A[13][22],A[13][23]=1,1,1,1,1
#     A[14][22],A[14][23],A[14][0]=1,1,1
#     A[15][23],A[15][0],A[15][1]=1,1,1

#     b = [2, 1,2,2,2,2,1,2,2,1,1,2,2,3,2,2]
#     for index, item in enumerate(A):
#         item.append(b[index])
#     return A

def PrintMatrix(A):

    s = ""
    for line in A:
        for v in line:
            s += str(v).split(".")[0].rjust(2) + " "
        s += "\n"
    print(s)



def GuassSolve(lStateMatrix, Unk, Num, Del):
    # 如果存在 确定的安全格子, 那么直接返回
    # 如果不存在, 则返回枚举器
    A = BuildAugmentedMatrix(Num, Unk, Del, lStateMatrix)
    # if not A:return []
    A = Gauss(A)

    freeX, A = Regular(A)

    X = SolveReMatrix(A, freeX)
    if 0 in X or sum(freeX) > 18:
        resList = []
        for i in range(len(X)):
            if X[i] == 0:
                resList.append(Unk[i])
        return resList
    else:
        return EnumerateIter(X, freeX)

def EnumerateIter(X, freeX):

    X_tmp= X[:]
    for i in range(2**sum(freeX)):
        n = i
        flag = True
        for j in range(len(freeX)):
            if freeX[j]:
                X_tmp[j] = (n & 1)
                n >>= 1

        for j in range(len(freeX)):
            if isinstance(X[j], Function):
                tmp = X[j](X_tmp)
                if tmp in (0, 1):
                    X_tmp[j] = tmp
                else:
                    flag = False
        if flag:
            yield X_tmp
    yield X_tmp

if __name__ == "__main__":
    
    

    lStateMatrix = [[3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 1, 1, 1, 3, 3000], [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 4, 3, 3000, 5, 3000], [2, 4, 3000, 3, 3, 
3000, 3, 3, 3000, 3000, 3000, 3000, 3000, 3, 3000, 3000], [1, 3000, 2, 1, 1, 1, 1, 1, 2, 3, 4, 4, 3, 2, 2, 2], [1, 1, 1, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1, 3000, 1, 2000, 1, 1], [2000, 
2000, 2000, 2000, 1, 1, 1, 2000, 2000, 2000, 1, 1, 1, 2000, 1, 3000], [2000, 2000, 2000, 1, 2, 3000, 1, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2, 2], [2000, 2000, 2000, 1, 3000, 2, 1, 2000, 1, 1, 1, 2000, 2000, 2000, 2, 3000], [2000, 2000, 2000, 1, 1, 1, 2000, 2000, 1, 3000, 1, 1, 1, 1, 3, 3000], [2000, 2000, 2000, 2000, 1, 1, 1, 1, 2, 2, 1, 1, 3000, 1, 2, 3000], [1, 1, 2, 1, 2, 3000, 2, 2, 3000, 2, 2, 2, 2, 1, 1, 1], [1, 3000, 2, 3000, 3, 2, 2, 3000, 4, 3000, 2, 3000, 2, 1, 2000, 2000], [1, 1, 2, 3, 3000, 2, 1, 2, 3000, 2, 2, 2, 3000, 2, 1, 2000], [1, 1, 2000, 2, 3000, 2, 2000, 1, 1, 1, 1, 2, 3, 3000, 1, 2000], [3000, 1, 2000, 1, 1, 1, 2000, 2000, 2000, 2000, 1, 3000, 3, 3, 3, 1], [1, 1, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1, 1, 2, 3000, 3000, 1]]
    Unk = [(1, 3), (2, 8), (1, 15), (1, 6), (0, 10), (2, 12), (2, 5), (1, 2), (2, 9), (0, 15), (1, 5), (2, 2), (1, 10), (1, 1), (1, 13), (1, 4), (2, 10), (1, 0), (2, 14), (4, 11), (3, 1), (2, 11), (1, 8), 
(1, 7), (2, 15)]
    Num = [(3, 15), (3, 0), (0, 14), (3, 11), (2, 1), (4, 12), (3, 7), (1, 11), (3, 14), (4, 0), (3, 3), (3, 10), (5, 12), (1, 14), (0, 11), (2, 13), (3, 6), (4, 1), (4, 10), (3, 2), (2, 6), (5, 11), (3, 13), (0, 12), (3, 9), (2, 3), (4, 2), (3, 5), (2, 7), (3, 12), (5, 10), (1, 12), (0, 13), (3, 8), (2, 0), (3, 4), (2, 4)]
    


    A = BuildAugmentedMatrix(Num, Unk, lStateMatrix)
    
    A = Gauss(A)

    freeX, A = Regular(A)

    X = SolveReMatrix(A, freeX)


    X_tmp= X[:]
    for i in range(2**sum(freeX)):
        flag = True
        n = i
        
        for j in range(len(freeX)):
            if freeX[j]:
                X_tmp[j] = (n & 1)
                n >>= 1

        for j in range(len(freeX)):
            if isinstance(X[j], Function):
                tmp = X[j](X_tmp)
                if tmp in (0.0, 1.0):
                    X_tmp[j] = tmp
                else:
                    flag = False
        if flag:
            print(X_tmp)
                
