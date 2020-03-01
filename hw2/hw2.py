import numpy as np
import matplotlib.pyplot as plt
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


    def orientToState(self):
        values = [1,2,3,4]
        probabilities = [0.05, 0.05, 0.1, 0.8]
        randomActionVal = random.choices(values, probabilities)

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
        robot = Robot()

        robot.direction[actionSel(robot.curState)] = True
        while not robot.complete:
            robot.curAction = actionSel(robot.curState)
            state, complete, reward = robot.processState()
            robot.steps += 1
        rewardData.append(reward)
        # print("EPISODE", episode)

    # reports
    mean = np.mean(rewardData)
    sd = np.std(rewardData)
    max = np.max(rewardData)
    min = np.min(rewardData)
    reports = [mean, sd, max, min]
    print("mean:", mean, "sd:", sd, "max:", max, "min:", min)

    return rewardData, reports

def q1():
    def actionSel(state):
        direction = ["left", "right", "up", "down"]
        return random.choices(direction)[0]

    return process(actionSel)

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
    return process(actionSel)

def q4(randomP = [], optimalP = []):

    dataRandom_y = sorted(randomP)
    dataOptimal_y = sorted(optimalP)

    len_y1 = len(dataRandom_y)
    len_y2 = len(dataOptimal_y)

    dataRandom_x  = np.arange(1, len_y1+1) / len_y1
    dataOptimal_x = np.arange(1, len_y2+1) / len_y2


    return dataRandom_x, dataRandom_y, dataOptimal_x, dataOptimal_y


def q5(points = 0):

    for episode in range(10000):
        robot = Robot()
        maxSteps = 19 - 8
        robot.curState = 19
        direction = ["left", "right", "up", "down"]
        while not robot.complete:
            robot.curAction = random.choices(direction)[0]
            robot.processState()
            robot.steps += 1
            if robot.steps == maxSteps and robot.curState == 22:
                points += 1
                break
    pr = points / 10000
    return pr


def plotData():

    rewards1, reports1 = q1()
    rewards2, reports2 = q3()
    x1, y1, x2, y2 = q4(rewards1, rewards2)
    pr_q5 = q5()

    fig, ax = plt.subplots(3,1)
    ax[0].plot(x1, y1, label="Random")
    ax[0].plot(x2, y2, label="Optimal")
    ax[0].legend()
    ax[0].set_xlabel("Probability")
    ax[0].set_ylabel("Return")
    ax[0].set_title('Random vs Optimal Policy')

    clust_data = [["Mean",reports1[0],reports2[0]],
                  ["Standard Deviation",reports1[1],reports2[1]],
                  ["Max",reports1[2],reports2[2]],
                  ["Min",reports1[3],reports2[3]],
                  ["Random Seed", 100, 100]]
    collabel=("Report", "Random", "Optimal")
    ax[1].axis('tight')
    ax[1].axis('off')
    the_table = ax[1].table(cellText=clust_data,
                          colLabels=("Report", "Random", "Optimal"),
                          loc='center')

    ax[2].axis('tight')
    ax[2].axis('off')
    the_table = ax[2].table(cellText=[["Pr(S19 = 21|S8 = 18)", pr_q5]],loc='center')
    plt.show()
    return 0

def Main():
    random.seed(100)
    plotData()

if __name__ == '__main__':
    Main()
