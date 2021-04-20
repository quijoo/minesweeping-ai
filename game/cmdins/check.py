from game.defines import *
from game import utils
from game.unit import *

@utils.log(__name__)
def CheckUnit(oGame, a, b):

    oGame.AddMsg("Click {}, {}".format(a, b))

    if oGame.m_Grids[a][b].m_Boom:
        return COMMAND_FAILD
    
    if oGame.m_Grids[a][b].m_State in (UNIT_EMPTY, UNIT_NUM):
        return COMMAND_NORM

    visited = [[False for _ in range(oGame.m_Grids.m_Size)] for _ in range(oGame.m_Grids.m_Size)]
    
    def RecuCheck(i, j):
        nonlocal visited
        
        if visited[i][j]:
            return

        oGame.m_Grids.m_leave -= 1
        oGame.m_Grids[i][j].m_State = UNIT_EMPTY

        queue, boomCnt = [], 0
        for x, y, unit in oGame.m_Grids.NeiborIter(i, j):
            if unit.m_Boom:
                boomCnt += 1
            
            elif not visited[x][y]:
                queue.append((x, y))
 
        oGame.m_Grids[i][j].m_BoomCount = boomCnt
        visited[i][j] = True

        if oGame.m_Grids[i][j].m_BoomCount == 0:
            for x, y in queue:
                RecuCheck(x, y)
        else:
            oGame.m_Grids[i][j].m_State = UNIT_NUM
            
    
    RecuCheck(a, b)

    return COMMAND_NORM
    
