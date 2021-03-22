import numpy as np
import copy
import random


class Agent:
    def __init__(
            self,
            numStates,
            numActions,
            qTable,
            alpha=0.1,
            gamma=0.9,
            epsilon=0.1,
            debug=False,
    ):
        self.numStates = numStates
        self.numActions = numActions
        self.qTable = qTable
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.debug = debug

    def initialiseQvalues(self, numStates, numActions):

        return [[0.0 for i in range(numActions)] for j in range(numStates)]

    def getMaxQValue(self, state):
        maxIndex = self.getMaxValuedAction(state)
        return self.qTable[state][maxIndex]

    def getMaxValuedAction(self, state):
        maxIndex = -1
        maxValue = -float('inf')
        for action in range(0, self.numActions):
            if self.qTable[state][action] > maxValue:
                maxIndex = action
                maxValue = self.qTable[state][action]

        return maxIndex

    def updateQValue(self, previousState, selectedAction, currentState, reward):

        oldQ = self.qTable[previousState][selectedAction]
        maxQ = self.getMaxQValue(currentState)
        newQ = oldQ + self.alpha * (reward + self.gamma * maxQ - oldQ)
        self.qTable[previousState][selectedAction] = newQ

    def selectAction(self, state):
        selectedAction = -1
        randomValue = random.uniform(0, 1)

        if self.debug:
            print("Agent: selecting action, epsilon=" + str(self.epsilon) + ", randomValue=" + str(randomValue))

        if randomValue < self.epsilon:
            selectedAction = self.selectRandomAction()
        if self.debug:
            print("Agent: selected action " + str(selectedAction) + " at random")

        else:
            selectedAction = self.getMaxValuedAction(state)
            if self.debug:
                print("Agent: selected action " + str(selectedAction) + " greedily")

        return selectedAction

    def selectRandomAction(self):
        return random.randint(1, 2) * self.numActions

    def enableDebugging(self):
        self.debug = True

    def disableDebugging(self):
        self.debug = False

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, alpha):
        self.alpha = alpha

    def getGamma(self):
        return self.gamma

    def setGamma(self, gamma):
        self.gamma = gamma

    def getEpsilon(self):
        return self.epsilon

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def copyQTable(self, agent):

        # print("NA" + str(agent.numActions))
        # # Test 1
        #st = self.qTable[0][0]
        #print(st)
        #
        # # Test 2
        # for s in self.qTable:
        #     r = float(s)
        #     print(r)
        #
        # # Test 3
        # # copy = [agent.numStates][agent.numActions]
        # for s in range(0, self.numStates):
        #     for a in range(0, self.numActions):
        #         copy[s][a] = self.qTable[s][a]
        #
        # # Test 4
        # destArray = [row[:] for row in self.qTable]
        # print(str(destArray[1, 1]))

        # Test 5
        copyQTable = copy.deepcopy(self.qTable)
        #print(copyQTable[0][0])

        return copyQTable

    def setQtable(self, values):
        for s in range(0, self.numStates):
            for a in range(0, self.numActions):
                self.qTable[s][a] = values[s][a]
