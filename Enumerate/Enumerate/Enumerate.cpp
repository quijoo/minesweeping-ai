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
#include <list>
#include <iostream>
#include <math.h>
#include <time.h>
using namespace std;

class Node {
public:
    int x;
    int y;
    int value;
    int boom_count;
    list<Node*> next;
    Node(int _x, int _y, int _value)
    {
        x = _x;
        y = _y;
        value = _value;
        boom_count = 0;
    }

    void AddEdge(Node* other)
    {
        this->next.push_back(other);
    }

    void ChangeToSafe() 
    {
        list<Node*>::iterator ir;
        for (ir = this->next.begin(); ir != this->next.end(); ir++) {
            if (this->value == UNIT_BOOM) { (*ir)->boom_count--;}    
        }
        this->value = UNIT_SAFE;
        
    }
    void ChangeToBoom()
    {
        list<Node*>::iterator ir;
        for (ir = this->next.begin(); ir != this->next.end(); ir++) {
            if (this->value == UNIT_UNKNOWN || this->value == UNIT_SAFE) {
                (*ir)->boom_count++;
            }
        }
        

        this->value = UNIT_BOOM;
    }
};

vector<Node*>* GetData(vector<vector<Node*>>& Matrix, int &ptr, vector<int> &argv, int size)
{
    vector<Node*> *DelList = new vector<Node*>(size);
    for (int i = 0; i < size; i++)
    {
        ptr++;
        int x = argv[ptr];
        ptr++;
        int y = argv[ptr];
        (*DelList)[i] =  Matrix[x][y];
    }
    return DelList;
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
    vector<Node*>* NumList,     vector<vector<Node*>>&Matrix,
    vector<int>*BlockCnt,       vector<vector<vector<int>>>*CellCnt
)
{
    int x, y, j, BoomCnt;
    long long n, i;
    bool flag;
    for ( i = 0; i < poww(2, (UnknowList->size())); i++)
    {
        n = i;
        BoomCnt = 0;
        for (j = 0; j < (UnknowList->size()); j++)
        {
            x = (*UnknowList)[j]->x;
            y = (*UnknowList)[j]->y;
            if ((n & 1) == 1)
            {
                Matrix[x][y]->ChangeToBoom();
                BoomCnt++;
            }
            else 
            {
                Matrix[x][y]->ChangeToSafe();
            }
            n >>= 1;
        }
        flag = true;
        for (j = 0; j < (int)(NumList->size()); j++)
        {
            if ((*NumList)[j]->boom_count != (*NumList)[j]->value)
            {
                flag = false;
                break;
            }
        }
        if (flag)
        {
            (*BlockCnt)[BoomCnt]++;
            for (j = 0; j < (UnknowList->size()); j++)
            {
                x = (*UnknowList)[j]->x;
                y = (*UnknowList)[j]->y;

                if (Matrix[x][y]->value == UNIT_BOOM)
                    (*CellCnt)[x][y][BoomCnt]++;
            }
            for (j = 0; j < (DelList->size()); j++)
            {
                x = (*DelList)[j]->x;
                y = (*DelList)[j]->y;
                if (Matrix[x][y]->value == UNIT_BOOM)
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
    vector<vector<Node*>> lStateMatrix(size, vector<Node*>(size));
    //获取lStateMatrix
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++) 
        {
            inptr++;
            lStateMatrix[i][j] = new Node(i, j, argi[inptr]);
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
    
    // 建立连接, 将NUM周围的点与其建立连接
    for (int k = 0; k < (*NumList).size(); k++)
    {
        int i = (*NumList)[k]->x;
        int j = (*NumList)[k]->y;
        Node* NumNode = lStateMatrix[i][j];

        for (int x = max(i - 1, 0); x <= min(i + 1, (int)lStateMatrix.size() - 1); x++)
        {
            for (int y = max(j - 1, 0); y <= min(j + 1, (int)lStateMatrix.size() - 1); y++)
            {
                if (i == x && j == y) continue;
                Node* OtherNode = lStateMatrix[x][y];
                if (OtherNode->value == UNIT_UNKNOWN)
                {
                    OtherNode->AddEdge(NumNode);
                }
                if (OtherNode->value == UNIT_BOOM)
                {
                    OtherNode->AddEdge(NumNode);
                    NumNode->boom_count++;
                }
                if (OtherNode->value == UNIT_SAFE)
                {
                    OtherNode->AddEdge(NumNode);
                }
            }
        }
    }

    //几个列表是指针, 其余变量都是值
    vector<int> BlockCnt(surplus+1, 0);
    vector<vector<vector<int>>> CellCnt(size, vector<vector<int>>(size, vector<int>(surplus+1, 0)));

    // 枚举
    clock_t t = clock();
    Enumerate(UnknowList, DelList,NumList, lStateMatrix, &BlockCnt, &CellCnt);
    t = clock() - t;

    // 输出
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
    cout << t;
}
