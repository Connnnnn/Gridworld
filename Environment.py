import ast
import configparser

from Agent import *
from Utilities import *

env0 = ["MA2-SD.txt"]
env1 = ["MA-CL-0"]
env2 = ["MA-CL-0", "MA-CL-1", "MA-CL-2", "MA-CL-3"]
parser = configparser.ConfigParser()
env = env0
parser.read(str(env[0]))


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
            movesToGoal1=None,
            movesToGoal2=None,
            qTable1=None,
            qTable2=None,
            obstacles=ast.literal_eval(parser.get("config", "obstacles"))
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

        if movesToGoal1 is None:
            movesToGoal1 = []
        if movesToGoal2 is None:
            movesToGoal2 = []

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
        self.movesToGoal1 = movesToGoal1
        self.movesToGoal2 = movesToGoal2
        self.qTable1 = qTable1
        self.qTable2 = qTable2
        self.obstacles = obstacles

    def setupAgent(self):

        numStates = self.getNumStates()
        numActions = self.numActions
        self.agent = Agent(numStates, numActions, self.alpha, self.gamma, self.epsilon)

        self.agent.qTable1 = initialiseQvalues(numStates, numActions)
        self.agent.qTable2 = initialiseQvalues(numStates, numActions)

        if self.debug:
            self.agent.enableDebugging()

    def doExperiment(self):
        for a in range(self.numAgents):
            self.setupAgent()
        # Do loop of number of experiments
        for e in range(0, len(env)):

            output = ""
            output += f"--------------Experiment {e + 1} ------------------------ \n"
            file = open("out/Test.txt", "a")
            file.write(output)

            if len(env) > 1:
                self.configChange(e)
            # Make method to change variables based on the file, have an array of environments file names, cycle through
            for f in range(0, self.numEpisodes):
                self.doEpisode()
                output = ""
                output += f"--------------Episode {f} ------------------------ \n"
                file = open("out/Test.txt", "a")

                file.write(output)

    def configChange(self, e):

        parse = configparser.ConfigParser()
        parse.read(str(env[e]))

        self.xDimension = int(parser.get("config", "xDimensions"))
        self.yDimension = int(parser.get("config", "yDimensions"))
        self.numEpisodes = int(parser.get("config", "numEpisodes"))
        self.maxTimesteps = int(parser.get("config", "maxTimesteps"))
        self.numAgents = int(parser.get("config", "numAgents"))
        self.alphaDecayRate = float(parser.get("config", "alphaDecayRate"))
        self.epsilonDecayRate = float(parser.get("config", "epsilonDecayRate"))
        self.agent1StartXY = ast.literal_eval(parser.get("config", "agent1StartXY"))
        self.agent2StartXY = ast.literal_eval(parser.get("config", "agent2StartXY"))
        self.goal1LocationXY = ast.literal_eval(parser.get("config", "goal1LocationXY"))
        self.goal2LocationXY = ast.literal_eval(parser.get("config", "goal2LocationXY"))
        self.obstacles = ast.literal_eval(parser.get("config", "obstacles"))

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

        self.decayAlpha()
        self.decayEpsilon()
        for a in range(self.numAgents):
            if a == 0:
                self.movesToGoal1.append(stepsTaken)
            elif a == 1:
                self.movesToGoal2.append(stepsTaken)

    def doTimestep(self):
        # loop this over each agent
        output = ""
        for a in range(self.numAgents):
            if a == 0:
                currentStateNo = getStateNoFromXY(state=self.currentAgent1Coords,
                                                  basesForStateNo=[self.xDimension, self.yDimension])
                selectedAction = self.agent.selectAction(currentStateNo, a)
                previousAgentCoords = self.currentAgent1Coords
                self.currentAgent1Coords = self.getNextStateXY(previousAgentCoords, selectedAction, agentNum=a)

                reward = self.calculateReward(self.currentAgent1Coords, a)

                nextStateNo = getStateNoFromXY(state=self.currentAgent1Coords,
                                               basesForStateNo=[self.xDimension, self.yDimension])
                self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward, a)

                output += "---------------------------------------- \n"
                output += "Previous Agent 1 Coords = " + str(previousAgentCoords) + "\n"
                output += "Current Agent 1 Coords = " + str(self.currentAgent1Coords) + "\n"
                output += "Agent 1 Reward = " + str(reward) + "\n"

            if a == 1:
                currentStateNo = getStateNoFromXY(state=self.currentAgent2Coords,
                                                  basesForStateNo=[self.xDimension, self.yDimension])

                selectedAction = self.agent.selectAction(currentStateNo, a)
                previousAgentCoords = self.currentAgent2Coords
                self.currentAgent2Coords = self.getNextStateXY(previousAgentCoords, selectedAction, a)

                reward = self.calculateReward(self.currentAgent2Coords, a)

                nextStateNo = getStateNoFromXY(state=self.currentAgent2Coords,
                                               basesForStateNo=[self.xDimension, self.yDimension])
                self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward, a)

                output += "-----\n"
                output += "Previous Agent 2 Coords = " + str(previousAgentCoords) + "\n"
                output += "Current Agent 2 Coords = " + str(self.currentAgent2Coords) + "\n"
                output += "Agent 2 Reward = " + str(reward) + "\n"
        file = open("out/Test.txt", "a")
        file.write(output)

    def calculateReward(self, currentAgentCoords, agentNum):
        output = ""
        reward = 0
        if agentNum == 0:

            if currentAgentCoords[0] == self.goal1LocationXY[0] and currentAgentCoords[1] == self.goal1LocationXY[1]:
                reward = self.goalReward
                output += "Reward = " + str(reward) + "\n"
                self.goalReachedA = True
            elif currentAgentCoords[0] == self.goal2LocationXY[0] and currentAgentCoords[1] == self.goal2LocationXY[1]:
                reward = self.stepPenalty
            else:
                reward = self.stepPenalty

        elif agentNum == 1:

            if currentAgentCoords[0] == self.goal2LocationXY[0] and currentAgentCoords[1] == self.goal2LocationXY[1]:

                reward = self.goalReward
                self.goalReachedB = True
            elif currentAgentCoords[0] == self.goal1LocationXY[0] and currentAgentCoords[1] == self.goal1LocationXY[1]:
                reward = self.stepPenalty
            else:
                reward = self.stepPenalty

        return reward

    def getNextStateXY(self, currentStateXY, action, agentNum):
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

        if self.obstacles[nextStateXY[0]][nextStateXY[1]] == 1:
            nextStateXY = [currentStateXY[0], currentStateXY[1]]

        if agentNum == 0:
            if nextStateXY == self.currentAgent2Coords:
                nextStateXY = [currentStateXY[0], currentStateXY[1]]
        elif agentNum == 1:
            if nextStateXY == self.currentAgent1Coords:
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
        qTable1 = None
        qTable2 = None
        for a in range(self.numAgents):
            if a == 0:
                qTable1 = self.agent.copyQTable(a)
            elif a == 1:
                qTable2 = self.agent.copyQTable(a)
        return qTable1, qTable2

    def getXDimension(self):
        return self.xDimension

    def getYDimension(self):
        return self.yDimension

    def getMovesToGoal1(self):
        return self.movesToGoal1

    def getMovesToGoal2(self):
        return self.movesToGoal2
