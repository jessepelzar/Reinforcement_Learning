import numpy as np
import matplotlib
from typing import Tuple
import random
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
        self.direction = {"left":False, "right":False, "up":False, "down":False}

    # def next(self, curState, curAction):


    def orientToState(self):
        values = [1,2,3,4]
        probabilities = [0.05, 0.05, 0.1, 0.8]
        randomActionVal = random.choices(values, probabilities)
        # print(randomActionVal)
        if self.curState == self.stateEnd:
            return self.curState

        if randomActionVal[0] == 1:
            if self.curAction == "left":
                self.direction = {"left":False, "right":False, "up":False, "down":True}
            elif self.curAction == "right":
                self.direction = {"left":False, "right":False, "up":True, "down":False}
            elif self.curAction == "up":
                self.direction = {"left":True, "right":False, "up":False, "down":False}
            elif self.curAction == "down":
                self.direction = {"left":True, "right":False, "up":False, "down":False}
            self.curAction = list(self.direction.keys())[list(self.direction.values()).index(True)]
        elif randomActionVal[0] == 2:
            if self.curAction == "left":
                self.direction = {"left":False, "right":False, "up":True, "down":False}
            elif self.curAction == "right":
                self.direction = {"left":False, "right":False, "up":False, "down":True}
            elif self.curAction == "up":
                self.direction = {"left":False, "right":True, "up":False, "down":False}
            elif self.curAction == "down":
                self.direction = {"left":False, "right":True, "up":False, "down":False}
            self.curAction = list(self.direction.keys())[list(self.direction.values()).index(True)]
        elif randomActionVal[0] == 3:
            return self.curState
        # elif randomActionVal[0] == 4:

        # print("inside act", self.curAction)
        stateNext = self.curState
        # perform moves
        if self.curAction == "left" and stateNext % 5 != 0:
            # print("A")
            stateNext = self.curState - 1
        elif self.curAction == "right" and stateNext+1 % 5 != 0:
            # print("B")
            stateNext = self.curState + 1
        elif self.curAction == "up" and stateNext-5 >= 0:
            # print("C")
            stateNext = self.curState - 5
        elif self.curAction == "down" and stateNext+5 < self.size:
            # print("D")
            stateNext = self.curState + 5

        if stateNext not in self.stateObsticle:
            # print(stateNext)
            return stateNext
        else:
            return self.curState



    def processState(self):
        stateNext = self.orientToState()
        self.curState = stateNext
        if stateNext in self.stateWater:
            # print("water")
            self.reward += (self.discount ** self.steps) * self.rewardWater
        elif stateNext == self.stateEnd:
            # print("done")
            self.reward += (self.discount ** self.steps) * self.rewardComplete

        if self.curState == self.stateEnd:
            self.complete = True

        return self.curState, self.complete, self.reward



def process(actionSel, episodes = 10000):

    rewardData = []
    for episode in range(episodes):
        states = []
        robot = Robot()

        robot.direction[actionSel(robot.curState)] = True
        while not robot.complete:
            robot.curAction = actionSel(robot.curState)
            state, complete, reward = robot.processState()
            robot.steps += 1
            states.append(state)
        rewardData.append(reward)
        # print("EPISODE", episode)

    # reports
    mean = np.mean(rewardData)
    sd = np.std(rewardData)
    max = np.max(rewardData)
    min = np.min(rewardData)
    print("mean:", mean, "sd:", sd, "max:", max, "min:", min)

def q1():
    def actionSel(state):
        direction = ["left", "right", "up", "down"]
        return random.choices(direction)[0]
    process(actionSel)

def q3():
    # > > > > v
    # ^ > > > v
    # ^ < x > v
    # ^ < x > v
    # ^ < > > ^
    def actionSel(state):
        stateDict = {0:"right",  1:"right",  2:"right",  3:"right",  4:"down",
                     5:"up",     6:"right",  7:"right",  8:"right",  9:"down",
                     10:"up",    11:"left",  12:"x",     13:"right", 14:"down",
                     15:"up",    16:"left",  17:"x",     18:"right", 19:"down",
                     20:"up",    21:"left",  22:"right", 23:"right", 24:"up"}
        return stateDict[state]
    process(actionSel)

# def q4():



def Main():
    random.seed(100)
    # grid = Grid()
    print(q1())
    print(q3())
    # print(grid.orientToState(0, 'R'))
    # print(np.random.uniform(0,1))




if __name__ == '__main__':
    Main()
