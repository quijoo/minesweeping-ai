from game.defines import *


def SetBoomFlag(oGame, i, j):
    # assert

    if oGame.m_Grids.m_UnitMetrix[i][j].m_State == UNIT_BOOM:
        
        oGame.m_Grids.m_UnitMetrix[i][j].m_State = UNIT_UNKNOWN
    
    else:
        oGame.m_Grids.m_UnitMetrix[i][j].m_State = UNIT_BOOM
            
    return COMMAND_NORM