from Agent import *
from Utilities import *

obstacles = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
]


# 0,2 and 4,2

# obstacles = [[[0], [0], [1], [0], [0]], [[0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0]], [[0], [0], [1], [0], [0]]]

class Environment:

    def __init__(
            self,
            numActions=4,
            actionLabels=("North", "East", "South", "West"),
            xDimension=5,
            yDimension=5,
            numEpisodes=1000,
            maxTimesteps=100,
            goalReached=False,
            goal1LocationXY=None,
            goal2LocationXY=None,
            agent1StartXY=None,
            agent2StartXY=None,
            goalReward=10.0,
            stepPenalty=-1.0,
            numAgents=2,
            debug=False,

            currentAgent1Coords=None,
            previousAgent1Coords=None,
            currentAgent2Coords=None,
            previousAgent2Coords=None,
            alpha=0.1,
            alphaDecays=False,
            alphaDecayRate=0.9,
            gamma=1.0,
            epsilon=0.1,
            epsilonDecays=False,
            epsilonDecayRate=0.9,
            movesToGoal=None
    ):

        if agent1StartXY is None:
            agent1StartXY = [4, 0]
        if agent2StartXY is None:
            agent2StartXY = [4, 4]

        if goal1LocationXY is None:
            goal1LocationXY = [0, 4]
        if goal2LocationXY is None:
            goal2LocationXY = [0, 0]

        if currentAgent1Coords is None:
            currentAgent1Coords = [-1, -1]
        if previousAgent1Coords is None:
            previousAgent1Coords = [-1 - 1]
        if currentAgent2Coords is None:
            currentAgent2Coords = [-1, -1]
        if previousAgent2Coords is None:
            previousAgent2Coords = [-1 - 1]

        if movesToGoal is None:
            movesToGoal = []

        self.agent = None
        self.numActions = numActions
        self.actionLabels = actionLabels
        self.xDimension = xDimension
        self.yDimension = yDimension
        self.numEpisodes = numEpisodes
        self.maxTimesteps = maxTimesteps
        self.debug = debug
        self.numAgents = numAgents
        self.goalReached = goalReached
        self.goal1LocationXY = goal1LocationXY
        self.agent1StartXY = agent1StartXY
        self.goal2LocationXY = goal2LocationXY
        self.agent2StartXY = agent2StartXY
        self.goalReward = goalReward
        self.stepPenalty = stepPenalty

        self.currentAgent1Coords = currentAgent1Coords
        self.previousAgent1Coords = previousAgent1Coords
        self.currentAgent2Coords = currentAgent2Coords
        self.previousAgent2Coords = previousAgent2Coords
        self.alpha = alpha
        self.alphaDecays = alphaDecays
        self.alphaDecayRate = alphaDecayRate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonDecays = epsilonDecays
        self.epsilonDecayRate = epsilonDecayRate
        self.movesToGoal = movesToGoal

    def setupAgent(self):

        numStates = self.getNumStates()
        numActions = self.numActions
        self.agent = Agent(numStates, numActions, self.alpha, self.gamma, self.epsilon)
        self.agent.qTable = initialiseQvalues(numStates, numActions)

        if self.debug:
            self.agent.enableDebugging()

    def doExperiment(self):
        for a in range(self.numAgents):
            self.setupAgent()

        for e in range(0, self.numEpisodes, 1):
            if self.debug:
                print("\nEnvironment: *************** Episode " + str(e) + " starting ***************")

            self.doEpisode()

    def doEpisode(self):
        stepsTaken = 0
        self.currentAgent1Coords[0] = self.agent1StartXY[0]
        self.currentAgent1Coords[1] = self.agent1StartXY[1]

        self.currentAgent2Coords[0] = self.agent2StartXY[0]
        self.currentAgent2Coords[1] = self.agent2StartXY[1]

        for t in range(0, self.maxTimesteps, 1):
            if not self.goalReached:
                if self.debug:
                    print("\nEnvironment: *************** Timestep " + str(t) + " starting ***************")

                self.doTimestep()
                stepsTaken = stepsTaken + 1
            else:
                break
        for a in range(self.numAgents):
            self.decayAlpha()
            self.decayEpsilon()
            self.movesToGoal.append(stepsTaken)

    def doTimestep(self):
        # loop this over each agent
        for a in range(self.numAgents):
            if a == 0:
                currentStateNo = getStateNoFromXY(state=self.currentAgent1Coords,
                                                  basesForStateNo=[self.xDimension, self.yDimension])

                selectedAction = self.agent.selectAction(currentStateNo)
                previousAgentCoords = self.currentAgent1Coords
                currentAgentCoords = self.getNextStateXY(previousAgentCoords, selectedAction)

                reward = self.calculateReward(previousAgentCoords, selectedAction, currentAgentCoords, a)

                nextStateNo = getStateNoFromXY(state=self.currentAgent1Coords,
                                               basesForStateNo=[self.xDimension, self.yDimension])
                self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward)
            if a == 1:
                currentStateNo = getStateNoFromXY(state=self.currentAgent2Coords,
                                                  basesForStateNo=[self.xDimension, self.yDimension])

                selectedAction = self.agent.selectAction(currentStateNo)
                #print(selectedAction)
                previousAgentCoords = self.currentAgent2Coords
                #print(previousAgentCoords)
                currentAgentCoords = self.getNextStateXY(previousAgentCoords, selectedAction)
                #print(currentAgentCoords)
                reward = self.calculateReward(previousAgentCoords, selectedAction, currentAgentCoords, a)

                nextStateNo = getStateNoFromXY(state=self.currentAgent2Coords,
                                               basesForStateNo=[self.xDimension, self.yDimension])
                self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward)

    def calculateReward(self, previousAgentCoords, selectedAction, currentAgentCoords, agentNum):
        if agentNum == 0:
            if currentAgentCoords[0] == self.goal1LocationXY[0] & currentAgentCoords[1] == self.goal1LocationXY[1]:
                reward = self.goalReward
                self.goalReached = True
            else:
                reward = self.stepPenalty
        else:
            if currentAgentCoords[0] == self.goal2LocationXY[0] & currentAgentCoords[1] == self.goal2LocationXY[1]:
                reward = self.goalReward
                self.goalReached = True
            else:
                reward = self.stepPenalty
        return reward

    def getNextStateXY(self, currentStateXY, action):
        nextStateXY = [-1, -1]

        if action == 0:
            if currentStateXY[1] < self.yDimension - 1:
                nextStateXY = [currentStateXY[0], currentStateXY[1] + 1]

            else:
                nextStateXY = [currentStateXY[0], currentStateXY[1]]
        elif action == 1:
            if currentStateXY[0] < self.xDimension - 1:
                nextStateXY = [currentStateXY[0] + 1, currentStateXY[1]]

            else:
                nextStateXY = [currentStateXY[0], currentStateXY[1]]
        elif action == 2:
            if currentStateXY[1] > 0:
                nextStateXY = [currentStateXY[0], currentStateXY[1] - 1]

            else:
                nextStateXY = [currentStateXY[0], currentStateXY[1]]

        elif action == 3:
            if currentStateXY[0] > 0:
                nextStateXY = [currentStateXY[0] - 1, currentStateXY[1]]

            else:
                nextStateXY = [currentStateXY[0], currentStateXY[1]]

        #print("  df "+str(obstacles[currentStateXY[0]][currentStateXY[1]]))
        if obstacles[currentStateXY[0]][currentStateXY[1]] == 1:
            print("not allowed")  # don't move agent into new position
            nextStateXY = [currentStateXY[0], currentStateXY[1]]
        #print(nextStateXY)
        return nextStateXY

    def getNumStates(self):
        return self.xDimension * self.yDimension

    def decayAlpha(self):
        if self.alphaDecays:
            self.alpha = self.alpha * self.alphaDecayRate
            self.agent.setAlpha(self.alpha)

    def decayEpsilon(self):
        if self.epsilonDecays:
            self.epsilon = self.epsilon * self.epsilonDecayRate
            self.agent.setEpsilon(self.agent, self.epsilon)

    def getQTable(self):
        return self.agent.copyQTable(self.agent)

    def getXDimension(self):
        return self.xDimension

    def getYDimension(self):
        return self.yDimension

    def getMovesToGoal(self):
        return self.movesToGoal
