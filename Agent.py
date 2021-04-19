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
            qTable1,
            qTable2,
            alpha=0.1,
            gamma=0.9,
            epsilon=0.1,
            debug=False,
    ):
        self.numStates = numStates
        self.numActions = numActions
        self.qTable1 = qTable1
        self.qTable2 = qTable2
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.debug = debug

    def getMaxQValue(self, state, agent):
        maxIndex = self.getMaxValuedAction(state, agent)
        if agent == 0:
            return self.qTable1[state][maxIndex]
        elif agent == 1:
            return self.qTable2[state][maxIndex]

    def getMaxValuedAction(self, state, agent):
        maxIndex = -1
        maxValue = -sys.float_info.max
        if agent == 0:
            for action in range(0, 4):
                # print(str(action)+" = "+str(self.qTable[state][action]))
                if self.qTable1[state][action] > maxValue:
                    # print(maxValue)
                    maxIndex = action
                    maxValue = self.qTable1[state][action]
                    # print(maxValue)
        elif agent == 1:
            for action in range(0, 4):
                # print(str(action)+" = "+str(self.qTable[state][action]))
                if self.qTable2[state][action] > maxValue:
                    # print(maxValue)
                    maxIndex = action
                    maxValue = self.qTable2[state][action]
                    # print(maxValue)

        return maxIndex

    def updateQValue(self, previousState, selectedAction, currentState, reward, agent, env):
        if agent == 0:

            oldQ = self.qTable1[previousState][selectedAction]
            maxQ = self.getMaxQValue(currentState, agent)
            newQ = oldQ + env.alpha * (reward + (env.gamma * maxQ) - oldQ)

            # print("Max Q =" + str(str(maxQ)))
            # print("Alpha = " + str(env.alpha))
            # print("Gamma = " + str(env.gamma))
            # print("Old Q = " + str(oldQ))
            # print("Previous state "+str(previousState))
            # print("selected action "+str(selectedAction))
            # print("Curr state " + str(currentState))
            # print("Reward " + str(reward))

            # print(newQ)
            # print("Old QTable -  " + str(self.qTable))

            self.qTable1[previousState][selectedAction] = newQ
        elif agent == 1:
            oldQ = self.qTable2[previousState][selectedAction]
            maxQ = self.getMaxQValue(currentState, agent)
            newQ = oldQ + env.alpha * (reward + (env.gamma * maxQ) - oldQ)
            self.qTable2[previousState][selectedAction] = newQ
        # print("New QTable -  " + str(self.qTable))

    def selectAction(self, state, agent):
        selectedAction = -1
        randomValue = random.uniform(0, 1)

        if randomValue < self.epsilon:
            selectedAction = self.selectRandomAction()
        else:
            selectedAction = self.getMaxValuedAction(state, agent)

        return selectedAction

    def selectRandomAction(self):
        return random.randint(0, self.numActions - 1)

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
        copyQTable = None
        if agent == 0:
            copyQTable = copy.deepcopy(self.qTable1)
        elif agent == 1:
            copyQTable = copy.deepcopy(self.qTable2)
        return copyQTable

    def setQtable(self, values):

        for s in range(0, self.numStates):
            for a in range(0, self.numActions):
                self.qTable1[s][a] = values[s][a]
