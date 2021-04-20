
import traceback
import importlib

COMMAND_TYPE = 0
COMMAND_1 = 1
COMMAND_DISPLAY = 2
COMMAND_UNDISPLAY = 3
COMMAND_FLAG = 4


class CCommandManager:
    
    def __init__(self):
        self.InitCommand()

    def InitCommand(self):
        self.m_CommandSet = {
            COMMAND_1:("check", "CheckUnit"),
            COMMAND_DISPLAY:("debug", "display"),
            COMMAND_UNDISPLAY:("debug", "undisplay"),
            COMMAND_FLAG:("flag", "SetBoomFlag"),
        }
    
    def OnCommand(self, oGame, *args):

        if args[0] not in self.m_CommandSet:
            return
        
        try:
            oMoudle, oFunc = self.m_CommandSet[args[0]]
            oMoudle = importlib.import_module("game.cmdins." + oMoudle)
            oFunc = getattr(oMoudle, oFunc, None)
            
            return oFunc(oGame, *args[1:])
        
        except Exception as e:
            print("出现报错", traceback.format_exc())
    
    @staticmethod
    def CommandParser(CommList):
        CommList = CommList.split()
        try:
            CommList = list(map(int, CommList))
        
        except Exception as e:
            print("输入错误", traceback.format_exc())
        
        return CommList