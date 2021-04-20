// Enumerate.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>

//输入:
//
// UnknowList -> 二维数组 长度是不确定的 1
// DelList 二维数组长度不一定 1
// NumList 二维度数组 长度不一定 1
// lStateMatrix 二维数组 长度一定 1
// 
// 输出:
// BlockCnt -> 一维数组， 长度由输入的 surplus 确定
// CellCnt -> 长宽确定, 深度由 surplus 确定, 在python 端将多个相加
//def Enumerate( UnknowList : list, DelList : list, NumList : list) :
//    nonlocal lStateMatrix, lBlockCnt, lCellCnt



#define UNIT_NUM        1000
#define UNIT_UNKNOWN    3000
#define UNIT_BOOM       4000
#define UNIT_SAFE       5000
#include <vector>
#include <iostream>
#include <math.h>
using namespace std;
class Node {
public:
    int x;
    int y;
    int value;
    int size;
    vector<Node*> *next;
    Node(int _x, int _y, int _value)
    {
        x = _x;
        y = _y;
        value = _value;
        next = new vector<Node*>(8);
        size = 0;
    }

    bool AddNode(Node* other)
    {
        this->next->push_back(other);
        this->size ++;

        other->next->push_back(this);
        other->size++;
        return true;
    }

    bool DelNode(Node* other)
    {
        vector<Node*>::iterator it;
        
        for (it = this->next->begin(); it != this->next->end();)
        {
            if (*it == other)it = this->next->erase(it);
        }
        for (it = other->next->begin(); it != other->next->end();)
        {
            if (*it == this)it = other->next->erase(it);
        }
        other->size--;
        this->size--;
    }
};
vector<Node*>* GetData(vector<vector<int>>& Matrix, int &ptr, vector<int> &argv, int size)
{
    vector<Node*> *DelList = new vector<Node*>(size);
    for (int i = 0; i < size; i++)
    {
        ptr++;
        int x = argv[ptr];
        ptr++;
        int y = argv[ptr];
        (*DelList)[i] = new Node(x, y, Matrix[x][y]);
    }
    return DelList;
}

bool CheckSum(int x, int y, vector<vector<int>>& Matrix)
{
    int s = 0;
    for (int i = max(x - 1, 0); i <= min(x + 1, (int)Matrix.size()-1); i++)
    {
        for (int j = max(y - 1, 0); j <= min(y + 1, (int)Matrix.size()-1); j++)
        {
            
            if (i == x && j == y)continue;
            s += (Matrix[i][j] == UNIT_BOOM);
        }
    }
    return s == Matrix[x][y];
        
}
long long poww(int a, int b) {
    long long ans = 1, base = a;
    while (b != 0) {
        if ((b & 1) != 0)
            ans *= base;
        base *= base;
        b >>= 1;
    }
    return ans;
}
void Enumerate(
    vector<Node*>* UnknowList,  vector<Node*>* DelList, 
    vector<Node*>* NumList,     vector<vector<int>> &Matrix, 
    vector<int>*BlockCnt,       vector<vector<vector<int>>>*CellCnt
)
{
    for (long long i = 0; i < poww(2, (UnknowList->size())); i++)
    {
        long long n = i;
        int BoomCnt = 0;
        for (int j = 0; j < (UnknowList->size()); j++)
        {
            int x = (*UnknowList)[j]->x;
            int y = (*UnknowList)[j]->y;
            if ((n & 1) == 1)
            {
                Matrix[x][y] = UNIT_BOOM;
                BoomCnt++;
            }
            else 
            {
                Matrix[x][y] = UNIT_SAFE;
            }
            n >>= 1;
        }
        bool flag = true;
        for (int j = 0; j < (NumList->size()); j++)
        {
            if (!CheckSum((*NumList)[j]->x, (*NumList)[j]->y, Matrix))
            {
                flag = false;
                break;
            }
        }
        if (flag)
        {
            (*BlockCnt)[BoomCnt]++;
            for (int j = 0; j < (UnknowList->size()); j++)
            {
                int x = (*UnknowList)[j]->x;
                int y = (*UnknowList)[j]->y;

                if (Matrix[x][y] == UNIT_BOOM)
                    (*CellCnt)[x][y][BoomCnt]++;
            }
            for (int j = 0; j < (DelList->size()); j++)
            {
                int x = (*DelList)[j]->x;
                int y = (*DelList)[j]->y;
                if (Matrix[x][y] == UNIT_BOOM)
                    (*CellCnt)[x][y][BoomCnt]++;
            }
        }
    }
}
int main(int argc, char* argv[])
{
    vector<int> argi(argc);
    for (int i = 0; i < argc; i++)
    {
        argi[i] = atoi(argv[i]);
    }
    //获取输入
    int inptr = 0;
    inptr++;
    int surplus = argi[inptr];
    
    inptr++;
    int size = argi[inptr];
    vector<vector<int>> lStateMatrix(size, vector<int>(size));
    //获取lStateMatrix
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++) 
        {
            inptr++;
            lStateMatrix[i][j] = argi[inptr];
        }
    }


    //UnknowList
    inptr++;
    vector<Node*>* UnknowList = GetData(lStateMatrix, inptr, argi, argi[inptr]);
    
    //DelList
    inptr++;
    vector<Node*>* DelList = GetData(lStateMatrix, inptr, argi, argi[inptr]);
    
    //NumList
    inptr++;
    vector<Node*>* NumList = GetData(lStateMatrix, inptr, argi, argi[inptr]);
    
    //几个列表是指针, 其余变量都是值
    vector<int> BlockCnt(surplus+1, 0);
    vector<vector<vector<int>>> CellCnt(size, vector<vector<int>>(size, vector<int>(surplus+1, 0)));

    Enumerate(UnknowList, DelList,NumList, lStateMatrix, &BlockCnt, &CellCnt);
    cout << BlockCnt.size() << " ";
    for (int i =0;i< BlockCnt.size(); i++)
    {
        cout << BlockCnt[i] << " ";
    }

    cout << size << " " << surplus << " ";
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            for (int k = 0; k < surplus; k++)
                cout << CellCnt[i][j][k] << " ";
        }
    }
}
