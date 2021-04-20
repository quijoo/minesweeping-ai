import os
import random
from game.defines import *
from game.unit import CUnit
from game.grids import CGrids
from game.command import CCommandManager
# Game api for using or testing
class CGame:

    def __init__(self, width, boom) -> None:

        self.m_Grids = CGrids(width, boom)
        self.m_CommandManager = CCommandManager()
        self.m_running = False
        self.m_lMsgBuf = []

    def Start(self):
        # g_Grids
        self.m_Grids.InitGrids()
        self.m_running = True
        self.Update()

    def Command(self, commd:str):
        if not self.m_running:
            return
        sCmd = self.m_CommandManager.CommandParser(commd)
        sMsg = self.m_CommandManager.OnCommand(self, *sCmd)
        
        self.Update()

        return sMsg
        

    def GetStateMatrix(self):
        # 状态矩阵
        return self.m_Grids.__repr__()

    def GetMineNum(self):
        # return g_Grids.m_leave
        return self.m_Grids.m_BoomNum
    
    def CheckWin(self):
        if self.m_Grids.CheckSuccess():
            
            self.running = False
            return True
        return False

    def AddMsg(self, msg):
        
        if len(self.m_lMsgBuf) == MSG_BUFF_SIZE:
            self.m_lMsgBuf.pop(0)
        
        self.m_lMsgBuf.append("[In Game] {}".format(msg))

    def Update(self):
        if  not DEBUG_MODE:os.system("cls")
        
        print(self.m_Grids)
        
        for sMsg in self.m_lMsgBuf:
            print(sMsg)

        

if __name__ == "__main__":
    pass