import numpy as np
import matplotlib
from typing import Tuple
from random import choices
class Robot():

    def __init__(self):
        self.size = 25
        self.curAction = ""
        self.stateBegin = 0
        self.curState = 0
        self.stateEnd = 24
        self.stateWater = (6, 18, 22)
        self.stateObsticle = (12, 17)
        self.prSpecifiedDir = 0.8
        self.prConfusedDir = 0.05
        self.prFreezePos = 0.1
        self.reward = 0
        self.discount = 0.9
        self.steps = 0
        self.complete = False
        self.rewardComplete = 10
        self.rewardWater = -10
        self.direction = {"left":False, "right":True, "up":False, "down":False}

    # def next(self, curState, curAction):


    def orientToState(self, curState):
        # randomActionVal = np.random.uniform(0,1)
        values = [1,2,3,4]
        probabilities = [0.05, 0.05, 0.1, 0.8]
        move = False
        # values2 = [1,2,3]
        # probabilities = [0.05, 0.05, 0.1, 0.8]
        randomActionVal = choices(values, probabilities)
        # randomActionVal = random.choice(1,2,3,3,3,3,3,3,3,3)
        # 10% of the random numbers is L or R  -> 1
        # 10% is stop -> 2
        # 80% is go -> 3
        # print(randomActionVal)
        if curState == self.stateEnd:
            return curState

        if randomActionVal[0] == 1:
            curAction = 'L'
        elif randomActionVal[0] == 2:
            curAction = 'R'
        elif randomActionVal[0] == 3:
            # curAction = 'F'
            return curState
        elif randomActionVal[0] == 4:
            if self.curAction != "":
                 curAction = self.curAction
            else:
                return curState

        # print(curAction)
        stateNext = self.curState
        # /////////////


        # /////////////

        if self.direction["left"] == True:
            # print("left")
            if curAction == 'L':
                self.direction = {"left":False, "right":False, "up":False, "down":True}
                stateNext = self.curState + 5
            elif curAction == 'R':
                self.direction = {"left":False, "right":False, "up":True, "down":False}
                stateNext = self.curState - 5
            # elif curAction == 'F':
            #     stateNext = self.curState

        elif self.direction["right"] == True:
            # print("right")
            if curAction == 'L':
                self.direction = {"left":False, "right":False, "up":True, "down":False}
                stateNext = self.curState - 5
            elif curAction == 'R':
                self.direction = {"left":False, "right":False, "up":False, "down":True}
                stateNext = self.curState + 5
            # elif curAction == 'F':
            #     stateNext = self.curState

        elif self.direction["up"] == True:
            # print("up")
            if curAction == 'L' and stateNext % 5 != 0:
                self.direction = {"left":True, "right":False, "up":False, "down":False}
                stateNext = self.curState - 1
            elif curAction == 'R' and stateNext+1 % 5 != 0:
                self.direction = {"left":False, "right":True, "up":False, "down":False}
                stateNext = self.curState + 1
            # elif curAction == 'F':
            #     stateNext = self.curState

        elif self.direction["down"] == True:
            # print("down")
            if curAction == 'L' and stateNext+1 % 5 != 0:
                self.direction = {"left":True, "right":False, "up":False, "down":False}
                stateNext = self.curState + 1
            elif curAction == 'R' and stateNext % 5 != 0:
                self.direction = {"left":False, "right":True, "up":False, "down":False}
                stateNext = self.curState - 1
            # elif curAction == 'F':
            #     stateNext = self.curState

        if (stateNext < self.size) and (stateNext >= 0) and (stateNext not in self.stateObsticle):
            # print("A")
            # print("curState", self.curState)
            # print("stateNext", stateNext)
            return stateNext

        else:
            stateNext = self.curState
            return self.curState



    def processState(self, curState):
        stateNext = self.orientToState(curState)
        # print(stateNext)
        if str(stateNext) in str(self.stateWater):
            # print("1")
            self.reward += (self.discount ** self.steps) * self.rewardWater
        elif str(stateNext) in str(self.stateEnd):
            # print("2")
            self.reward += (self.discount ** self.steps) * self.rewardComplete
        self.curState = stateNext
        if self.curState == self.stateEnd:
            self.complete = True
        # print(self.curState)
        return self.curState, self.complete, self.reward





def process(episodes = 10000):

    rewardData = []
    for episode in range(episodes):
        robot = Robot()
        while not robot.complete:
            # print(state)
            state, complete, reward = robot.processState(robot.curState)
            robot.steps += 1
            # print(state)
            # print(state, complete, reward)
        rewardData.append(reward)
        print("DONE EPISODE {}", episode)

    # reports
    mean = np.mean(rewardData)
    sd = np.std(rewardData)
    max = np.max(rewardData)
    min = np.min(rewardData)
    print("mean:", mean, "sd:", sd, "max:", max, "min:", min)
    # print(rewardData)




def Main():
    # grid = Grid()
    print(process())
    # print(grid.orientToState(0, 'R'))
    # print(np.random.uniform(0,1))




if __name__ == '__main__':
    Main()
