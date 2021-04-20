# AI 
# Input:    State Matrix
# Output:   Safe Point


from game.defines import *
from game.app import CGame
from ai.ai import AI
from game.defines import *

import time
# CGame API 

def Run():

    Game = CGame(width=16, boom=50)
    iWinNum, iTotalNum, lTimeAnalyze = 0, 0, []
    iAccTotal, iAccFaild = 0, 0
    for ith in range(1, 1001):
        Game.Start()
        t = time.time()
        while Game.m_running:    
            
            lStateMatrix = Game.GetStateMatrix()
            sState = "run"
            bRandom, lPoints = AI.Process(lStateMatrix, Game.GetMineNum())
            for tPoint in lPoints:
                # time.sleep(0.5)
                sMsg = Game.Command("1 {} {}".format(tPoint[0], tPoint[1]))
                
                print("[In AI] win: {}, total: {}.[{}/{}]".format(iWinNum, iTotalNum, iAccFaild, iAccTotal))
                
                if not bRandom:iAccTotal+=1
                
                if sMsg == COMMAND_FAILD:
                    iAccFaild += (not bRandom)
                    sState = "Faild"
                    break
                
                if Game.CheckWin():
                    iWinNum += 1
                    sState = "Win"
                    Game.Command("2")
                    break
                
            if sState == "Faild" or sState == "Win":
                iTotalNum += 1
                break  
        
        lTimeAnalyze.append(time.time() - t)
    print("[In AI] win rate: {}, avgTime: {}.".format(iWinNum/iTotalNum, sum(lTimeAnalyze)/len(lTimeAnalyze)))


def ManualRun():
    Game = CGame(10, 5)
    
    Game.Start()
    while Game.m_running:    
        
        sMsg = Game.Command(input())
        if sMsg == COMMAND_FAILD:
            print("Faild.")
            return False          
        
        if Game.CheckWin():
            print("Successful!")
            sMsg = Game.Command("2")
            return True
    return False

if __name__ == "__main__":
    import sys
    if sys.argv[1] == "ai":
        Run()
    elif sys.argv[1] == "manual":
        ManualRun()

        