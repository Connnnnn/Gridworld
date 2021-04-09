import ast
import configparser

from Agent import *
from Utilities import *

# obstacles = [
#     [0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0],
# ]



# Start pos = (4,0), (4,4)
# End pos = (0, 4), (0,0)
# Obstacles = (0,2), (4,2)

env = "MA2-SD.txt"
parser = configparser.ConfigParser()
parser.read(env)

obstacles = ast.literal_eval(parser.get("config", "obstacles"))


class Environment:

    def __init__(
            self,
            numActions=4,
            actionLabels=("North", "East", "South", "West"),
            xDimension=int(parser.get("config", "xDimensions")),
            yDimension=int(parser.get("config", "yDimensions")),
            numEpisodes=int(parser.get("config", "numEpisodes")),
            maxTimesteps=int(parser.get("config", "maxTimesteps")),
            goalReachedA=False,
            goalReachedB=False,
            goal1LocationXY=None,
            goal2LocationXY=None,
            agent1StartXY=None,
            agent2StartXY=None,
            goalReward=10.0,
            stepPenalty=-1.0,
            numAgents=int(parser.get("config", "numAgents")),
            debug=False,

            currentAgent1Coords=None,
            previousAgent1Coords=None,
            currentAgent2Coords=None,
            previousAgent2Coords=None,
            alpha=float(parser.get("config", "alpha")),
            alphaDecays=False,
            alphaDecayRate=float(parser.get("config", "alphaDecayRate")),
            gamma=float(parser.get("config", "gamma")),
            epsilon=float(parser.get("config", "epsilon")),
            epsilonDecays=False,
            epsilonDecayRate=float(parser.get("config", "epsilonDecayRate")),
            movesToGoal=None
    ):

        if agent1StartXY is None:
            agent1StartXY = ast.literal_eval(parser.get("config", "agent1StartXY"))
        if agent2StartXY is None:
            agent2StartXY = ast.literal_eval(parser.get("config", "agent2StartXY"))

        if goal1LocationXY is None:
            goal1LocationXY = ast.literal_eval(parser.get("config", "goal1LocationXY"))
        if goal2LocationXY is None:
            goal2LocationXY = ast.literal_eval(parser.get("config", "goal2LocationXY"))

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
        self.goalReachedA = goalReachedA
        self.goalReachedB = goalReachedB
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

        for e in range(0, self.numEpisodes):
            self.doEpisode()

    def doEpisode(self):
        stepsTaken = 0
        self.currentAgent1Coords[0] = self.agent1StartXY[0]
        self.currentAgent1Coords[1] = self.agent1StartXY[1]

        self.currentAgent2Coords[0] = self.agent2StartXY[0]
        self.currentAgent2Coords[1] = self.agent2StartXY[1]

        self.goalReachedA = False
        self.goalReachedB = False

        for t in range(0, self.maxTimesteps, 1):
            if not self.goalReachedA and not self.goalReachedB:
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
                self.currentAgent1Coords = self.getNextStateXY(previousAgentCoords, selectedAction)
                reward = self.calculateReward(self.currentAgent1Coords, a)

                #print(self.currentAgent1Coords)
                #print(reward)

                nextStateNo = getStateNoFromXY(state=self.currentAgent1Coords,
                                               basesForStateNo=[self.xDimension, self.yDimension])
                self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward)

            if a == 1:
                currentStateNo = getStateNoFromXY(state=self.currentAgent2Coords,
                                                  basesForStateNo=[self.xDimension, self.yDimension])

                selectedAction = self.agent.selectAction(currentStateNo)
                previousAgentCoords = self.currentAgent2Coords
                self.currentAgent2Coords = self.getNextStateXY(previousAgentCoords, selectedAction)
                reward = self.calculateReward(self.currentAgent2Coords, a)

                nextStateNo = getStateNoFromXY(state=self.currentAgent2Coords,
                                               basesForStateNo=[self.xDimension, self.yDimension])
                self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward)

    def calculateReward(self, currentAgentCoords, agentNum):
        if agentNum == 0:
            #print(currentAgentCoords[0])
            #print(self.goal1LocationXY[0])
            if currentAgentCoords[0] == self.goal1LocationXY[0] & currentAgentCoords[1] == self.goal1LocationXY[1]:
                reward = self.goalReward
                self.goalReachedA = True
            else:
                reward = self.stepPenalty
        else:
            if currentAgentCoords[0] == self.goal2LocationXY[0] & currentAgentCoords[1] == self.goal2LocationXY[1]:
                reward = self.goalReward
                self.goalReachedB = True
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


        if obstacles[currentStateXY[0]][currentStateXY[1]] == 1:
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
