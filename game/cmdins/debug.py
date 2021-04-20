from game.defines import *
from game.unit import *

state = []
def display(oGame):
    for line in oGame.m_Grids.m_UnitMetrix:
        for item in line:
            if item.m_Boom:
                state.append(item.m_State)
                item.m_State = UNIT_BOOM
                
    return COMMAND_NORM

                

def undisplay(oGame):
    if not state:return
    for line in oGame.m_Grids.m_UnitMetrix:
        for item in line:
            if item.m_Boom:
                item.m_State = state.pop(0)
                
    return COMMAND_NORM
