import sys
import copy
import random


def initialiseQvalues(numStates, numActions):
    return [[0.0 for _ in range(numActions)] for _ in range(numStates)]


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

    def getMaxQValue(self, state):
        maxIndex = self.getMaxValuedAction(state)
        return self.qTable[state][maxIndex]

    def getMaxValuedAction(self, state):
        maxIndex = -1
        maxValue = -sys.float_info.max

        for action in range(0, self.numActions):
            # print(str(action)+" = "+str(self.qTable[state][action]))
            if self.qTable[state][action] > maxValue:
                # print(maxValue)
                maxIndex = action
                maxValue = self.qTable[state][action]
                # print(maxValue)

        return maxIndex

    def updateQValue(self, previousState, selectedAction, currentState, reward):

        # All q values are initialised at zero and never have the chance to go higher
        # PROBLEM - MAX Q IS ALWAYS ZERO

        # print("Previous state "+str(previousState))
        # print("selected action "+str(selectedAction))
        # print("Curr state " + str(currentState))
        # print("Reward " + str(reward))

        oldQ = self.qTable[previousState][selectedAction]
        maxQ = self.getMaxQValue(currentState)
        newQ = oldQ + self.alpha * (reward + (self.gamma * maxQ) - oldQ)

        # print(oldQ)
        # print(self.alpha)
        # print(self.gamma)
        # print(str(maxQ))

        # print(newQ)
        # print(self.qTable)
        self.qTable[previousState][selectedAction] = newQ
        # print(self.qTable)

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

    def copyQTable(self):
        copyQTable = copy.deepcopy(self.qTable)
        return copyQTable

    def setQtable(self, values):
        for s in range(0, self.numStates):
            for a in range(0, self.numActions):
                self.qTable[s][a] = values[s][a]
