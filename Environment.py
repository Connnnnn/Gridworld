from Agent import Agent
from Utilities import Utilities


class Environment:

    def __init__(
            self,
            numActions=4,
            actionLabels=("North", "East", "South", "West"),
            xDimension=10,
            yDimension=10,
            numEpisodes=1000,
            maxTimesteps=100,
            goalReached=False,
            goalLocationXY=(6, 6),
            agentStartXY=[2, 2],
            goalReward=10.0,
            stepPenalty=-1.0,

            debug=False,

            currentAgentCoords=[-1, -1],
            previousAgentCoords=(-1. - 1),
            alpha=0.1,
            alphaDecays=False,
            alphaDecayRate=0.9,
            gamma=1.0,
            epsilon=0.1,
            epsilonDecays=False,
            epsilonDecayRate=0.9,
            movesToGoal=[]
    ):

        self.agent = None
        self.numActions = numActions
        self.actionLabels = actionLabels
        self.xDimension = xDimension
        self.yDimension = yDimension
        self.numEpisodes = numEpisodes
        self.maxTimesteps = maxTimesteps
        self.debug = debug
        self.goalReached = goalReached
        self.goalLocationXY = goalLocationXY
        self.agentStartXY = agentStartXY
        self.goalReward = goalReward
        self.stepPenalty = stepPenalty

        self.currentAgentCoords = currentAgentCoords
        self.previousAgentCoords = previousAgentCoords
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
        self.agent.qTable = Agent.initialiseQvalues(self.agent, numStates, numActions)

        if self.debug:
            self.agent.enableDebugging()

    def doExperiment(self):
        self.setupAgent()

        for e in range(0, self.numEpisodes, 1):
            if self.debug:
                print("\nEnvironment: *************** Episode " + str(e) + " starting ***************")

            self.doEpisode()

    def doEpisode(self):
        stepsTaken = 0
        self.currentAgentCoords[0] = self.agentStartXY[0]
        self.currentAgentCoords[1] = self.agentStartXY[1]
        goalReached = False

        for t in range(0, self.maxTimesteps, 1):
            if not self.goalReached:
                if self.debug:
                    print("\nEnvironment: *************** Timestep " + str(t) + " starting ***************")

                self.doTimestep()
                stepsTaken = stepsTaken + 1
            else:
                break
        self.decayAlpha()
        self.decayEpsilon()
        self.movesToGoal.append(stepsTaken)

    def doTimestep(self):

        currentStateNo = Utilities.getStateNoFromXY(self.currentAgentCoords, [self.xDimension, self.yDimension])

        selectedAction = self.agent.selectAction(currentStateNo)
        previousAgentCoords = self.currentAgentCoords
        currentAgentCoords = self.getNextStateXY(previousAgentCoords, selectedAction)

        reward = self.calculateReward(previousAgentCoords, selectedAction, currentAgentCoords)

        nextStateNo = Utilities.getStateNoFromXY(self.currentAgentCoords, [self.xDimension, self.yDimension])
        self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward)
        if self.debug:
            print(
                "Environment: previousState [" + str(previousAgentCoords[0]) + "," + str(previousAgentCoords[1]) + "]; "
                                                                                                                   "selected "
                                                                                                                   "move " +
                self.actionLabels[selectedAction] + "; currentState [" + self.currentAgentCoords[0] + "," +
                self.currentAgentCoords[1] + "];")

    def calculateReward(self, previousAgentCoords, selectedAction, currentAgentCoords):

        if currentAgentCoords[0] == self.goalLocationXY[0] & currentAgentCoords[1] == self.goalLocationXY[1]:
            reward = self.goalReward
            self.goalReached = True
        else:
            reward = self.stepPenalty
        return reward

    def getNextStateXY(self, currentStateXY, action):
        nextStateXY = (-1, -1)

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
