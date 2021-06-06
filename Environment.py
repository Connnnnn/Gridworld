import ast
import configparser
import PBRSCalculator
from Agent import *
from Utilities import *


class Environment:

    def __init__(
            self,
            numActions=4,
            actionLabels=("North", "East", "South", "West"),
            xDimension=None,
            yDimension=None,
            numEpisodes=None,
            maxTimesteps=None,
            goalReachedA=False,
            goalReachedB=False,
            goal1LocationXY=None,
            goal2LocationXY=None,
            agent1StartXY=None,
            agent2StartXY=None,
            goalReward=10.0,
            stepPenalty=-1.0,
            QSPenalty=-2,
            obstaclePenalty=-2,
            deathPenalty=-10,
            probOfDeath=0.05,
            death=False,
            numAgents=None,
            debug=True,
            PBRS=False,

            currentAgent1Coords=None,
            previousAgent1Coords=None,
            currentAgent2Coords=None,
            previousAgent2Coords=None,
            alpha=None,
            alphaDecays=None,
            alphaDecayRate=None,
            gamma=None,
            epsilon=None,
            epsilonDecays=None,
            epsilonDecayRate=None,
            movesToGoal1=None,
            movesToGoal2=None,
            HeatMapA1=None,
            HeatMapA2=None,
            qTable1=None,
            qTable2=None,
            obstacles=None,
            PBRS1=None,
            PBRS2=None,
            hitObstacle=False,
            agent1Collisions=None,
            agent2Collisions=None,
            agent1CurrentCollisions=None,
            agent2CurrentCollisions=None
    ):

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

        if HeatMapA1 is None:
            HeatMapA1 = []
        if HeatMapA2 is None:
            HeatMapA2 = []

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
        self.QSPenalty = QSPenalty
        self.obstaclePenalty = obstaclePenalty
        self.probOfDeath = probOfDeath
        self.deathPenalty = deathPenalty
        self.death = death
        self.hitObstacle = hitObstacle
        self.PBRS = PBRS
        self.PBRS1 = PBRS1
        self.PBRS2 = PBRS2

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
        self.HeatMapA1 = HeatMapA1
        self.HeatMapA2 = HeatMapA2
        self.qTable1 = qTable1
        self.qTable2 = qTable2
        self.obstacles = obstacles
        self.agent1Collisions = agent1Collisions
        self.agent2Collisions = agent2Collisions
        self.agent1CurrentCollisions = agent1CurrentCollisions
        self.agent2CurrentCollisions = agent2CurrentCollisions

    def initialiseHeatmap(self):
        return [[0 for _ in range(self.xDimension)] for _ in range(self.yDimension)]

    def setupAgent(self):

        numStates = self.getNumStates()
        numActions = self.numActions
        self.agent = Agent(numStates, numActions, self.alpha, self.gamma, self.epsilon)

        self.agent.qTable1 = initialiseQvalues(numStates, numActions)
        self.agent.qTable2 = initialiseQvalues(numStates, numActions)

        if self.debug:
            self.agent.enableDebugging()

    def initialiseAgents(self, exp):
        self.configChange(0, exp)

        for a in range(self.numAgents):
            self.setupAgent()

    def doExperiment(self, run, experimentName, exp, e):

        self.configChange(e, exp)
        self.HeatMapA1 = self.initialiseHeatmap()
        self.HeatMapA2 = self.initialiseHeatmap()

        if self.debug is True:
            output = ""
            output += f"--------------Experiment {e + 1} ------------------------ \n"
            file = open("out/Test.txt", "a")
            file.write(output)

        for f in range(0, self.numEpisodes):
            self.doEpisode()

            if self.debug is True:
                output = ""
                output += f"--------------Episode {f} ------------------------ \n"
                file = open("out/Test.txt", "a")

                file.write(output)

        heatmapPrint(self.HeatMapA1, run, e, experimentName, 1)
        heatmapPrint(self.HeatMapA2, run, e, experimentName, 2)

    def configChange(self, e, exp):
        parser = configparser.ConfigParser()
        parser.read(exp[e])

        self.xDimension = int(parser.get("config", "xDimensions"))
        self.alpha = float(parser.get("config", "alpha"))
        self.gamma = float(parser.get("config", "gamma"))
        self.epsilon = float(parser.get("config", "epsilon"))
        self.yDimension = int(parser.get("config", "yDimensions"))
        self.numEpisodes = int(parser.get("config", "numEpisodes"))
        self.maxTimesteps = int(parser.get("config", "maxTimesteps"))
        self.numAgents = int(parser.get("config", "numAgents"))
        self.alphaDecays = bool(parser.get("config", "alphaDecays"))
        self.alphaDecayRate = float(parser.get("config", "alphaDecayRate"))
        self.epsilonDecays = bool(parser.get("config", "epsilonDecays"))
        self.epsilonDecayRate = float(parser.get("config", "epsilonDecayRate"))
        self.agent1StartXY = ast.literal_eval(parser.get("config", "agent1StartXY"))
        self.agent2StartXY = ast.literal_eval(parser.get("config", "agent2StartXY"))
        self.goal1LocationXY = ast.literal_eval(parser.get("config", "goal1LocationXY"))
        self.goal2LocationXY = ast.literal_eval(parser.get("config", "goal2LocationXY"))
        self.obstacles = ast.literal_eval(parser.get("config", "obstacles"))

        if not parser.has_option("config", "PBRS1"):
            self.PBRS1 = PBRSCalculator.main(self.xDimension, self.yDimension, self.goal1LocationXY, self.obstacles)
        else:
            self.PBRS1 = ast.literal_eval(parser.get("config", "PBRS1"))

        if not parser.has_option("config", "PBRS2"):
            self.PBRS2 = PBRSCalculator.main(self.xDimension, self.yDimension, self.goal2LocationXY, self.obstacles)
        else:
            self.PBRS2 = ast.literal_eval(parser.get("config", "PBRS2"))

    def doEpisode(self):
        stepsTaken = 0
        self.currentAgent1Coords[0] = self.agent1StartXY[0]
        self.currentAgent1Coords[1] = self.agent1StartXY[1]

        self.currentAgent2Coords[0] = self.agent2StartXY[0]
        self.currentAgent2Coords[1] = self.agent2StartXY[1]

        self.agent1CurrentCollisions = 0
        self.agent2CurrentCollisions = 0

        self.goalReachedA = False
        self.goalReachedB = False
        self.death = False

        for t in range(0, self.maxTimesteps, 1):
            if not self.goalReachedA and not self.goalReachedB:
                self.doTimestep()
                stepsTaken = stepsTaken + 1
            elif self.death:
                stepsTaken = self.maxTimesteps
                break
            else:
                break

        self.decayAlpha()
        self.decayEpsilon()
        for a in range(self.numAgents):
            if a == 0:
                self.movesToGoal1.append(stepsTaken)
                self.agent1Collisions.append(self.agent1CurrentCollisions)
            elif a == 1:
                self.movesToGoal2.append(stepsTaken)
                self.agent2Collisions.append(self.agent2CurrentCollisions)

    def doTimestep(self):

        output = ""

        for a in range(self.numAgents):
            QS1 = False
            QS2 = False
            if a == 0:
                currentStateNo = getStateNoFromXY(state=self.currentAgent1Coords,
                                                  basesForStateNo=[self.xDimension, self.yDimension])
                selectedAction = self.agent.selectAction(currentStateNo, a)
                previousAgentCoords = self.currentAgent1Coords
                self.currentAgent1Coords = self.getNextStateXY(previousAgentCoords, selectedAction, agentNum=a)

                if self.obstacles[self.currentAgent1Coords[0]][self.currentAgent1Coords[1]] == 2:
                    QS1 = True

                reward = self.calculateReward(self.currentAgent1Coords, a, QS1, previousAgentCoords)

                nextStateNo = getStateNoFromXY(state=self.currentAgent1Coords,
                                               basesForStateNo=[self.xDimension, self.yDimension])
                self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward, a, self)

                self.HeatMapA1[self.currentAgent1Coords[0]][self.currentAgent1Coords[1]] += 1

                if self.debug is True:
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

                if self.obstacles[self.currentAgent2Coords[0]][self.currentAgent2Coords[1]] == 2:
                    QS2 = True

                reward = self.calculateReward(self.currentAgent2Coords, a, QS2, previousAgentCoords)

                nextStateNo = getStateNoFromXY(state=self.currentAgent2Coords,
                                               basesForStateNo=[self.xDimension, self.yDimension])
                self.agent.updateQValue(currentStateNo, selectedAction, nextStateNo, reward, a, self)

                self.HeatMapA2[self.currentAgent2Coords[0]][self.currentAgent2Coords[1]] += 1
                if self.debug is True:
                    output += "-----\n"
                    output += "Previous Agent 2 Coords = " + str(previousAgentCoords) + "\n"
                    output += "Current Agent 2 Coords = " + str(self.currentAgent2Coords) + "\n"
                    output += "Agent 2 Reward = " + str(reward) + "\n"

        if self.debug is True:
            file = open("out/Test.txt", "a")
            file.write(output)

    def calc_pbrs_shaping(self, currentAgentCoords, previousAgentCoords):
        return self.gamma * self.PBRS1[currentAgentCoords[0]][currentAgentCoords[1]] - \
               self.PBRS1[previousAgentCoords[0]][previousAgentCoords[1]]

    def calculateReward(self, currentAgentCoords, agentNum, QS, previousAgentCoords):

        reward = 0
        if agentNum == 0:

            if currentAgentCoords[0] == self.goal1LocationXY[0] and currentAgentCoords[1] == self.goal1LocationXY[1]:
                reward = self.goalReward
                self.goalReachedA = True
            elif self.hitObstacle is True:
                reward = self.obstaclePenalty
            elif QS is True:
                reward = self.QSPenalty
                if decision(self.probOfDeath):
                    reward = -10
                    self.death = True
            else:
                reward = self.stepPenalty

        elif agentNum == 1:

            if currentAgentCoords[0] == self.goal2LocationXY[0] and currentAgentCoords[1] == self.goal2LocationXY[1]:
                reward = self.goalReward
                self.goalReachedB = True
            elif self.hitObstacle is True:
                reward = self.obstaclePenalty
            elif QS is True:
                reward = self.QSPenalty
                if decision(self.probOfDeath):
                    reward = 0
                    self.death = True
            else:
                reward = self.stepPenalty

        if self.PBRS:
            reward = reward + self.calc_pbrs_shaping(currentAgentCoords, previousAgentCoords)

        return reward

    def getNextStateXY(self, currentStateXY, action, agentNum):
        nextStateXY = [-1, -1]
        self.hitObstacle = False

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
            self.hitObstacle = True

        if agentNum == 0:
            if nextStateXY == self.currentAgent2Coords:
                nextStateXY = [currentStateXY[0], currentStateXY[1]]
                self.hitObstacle = True
                self.agent1CurrentCollisions += 1
        elif agentNum == 1:
            if nextStateXY == self.currentAgent1Coords:
                nextStateXY = [currentStateXY[0], currentStateXY[1]]
                self.hitObstacle = True
                self.agent2CurrentCollisions += 1

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
            self.agent.setEpsilon(self.epsilon)

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

    def getAgent1Collisions(self):
        return self.agent1Collisions

    def getAgent2Collisions(self):
        return self.agent2Collisions
