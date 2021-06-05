import time
from Utilities import *
from Environment import Environment

exp0 = ["Configs/MA2-SD.txt"]
exp1 = ["Configs/CL/MA-CL-1"]
expTest = ["Configs/CL/MA-CL-1", "Configs/CL/MA-CL-2"]
exp2 = ["Configs/CL/MA-CL-1", "Configs/CL/MA-CL-2", "Configs/CL/MA-CL-3", "Configs/CL/MA-CL-4"]
expCL1To6 = ["Configs/CL/MA-CL-1", "Configs/CL/MA-CL-2", "Configs/CL/MA-CL-3", "Configs/CL/MA-CL-4",
             "Configs/CL/MA-CL-5", "Configs/CL/MA-CL-6"]
expOnly6 = ["Configs/CL/MA-CL-6"]
lavaExp = ["Configs/Lava/MA-QS-1", "Configs/Lava/MA-QS-2", "Configs/Lava/MA-QS-3", "Configs/Lava/MA-QS-4"]

expOnly5 = ["Configs/CL/MA-CL-5"]
expCL1To5 = ["Configs/CL/MA-CL-1", "Configs/CL/MA-CL-2", "Configs/CL/MA-CL-3", "Configs/CL/MA-CL-4",
             "Configs/CL/MA-CL-5"]

exp = exp0


class Grid:
    def __init__(
            self,
            results1=None,
            results2=None,
            QTables1=None,
            QTables2=None,
            numRuns=1,
            experimentName="Gridworld_" + str(round(time.time() * 1000)),
            agent1Collisions=None,
            agent2Collisions=None
    ):

        if QTables1 is None:
            QTables1 = []
        if QTables2 is None:
            QTables2 = []
        if results1 is None:
            results1 = []
        if results2 is None:
            results2 = []

        self.numRuns = numRuns
        self.results1 = results1
        self.results2 = results2
        self.QTables1 = QTables1
        self.QTables2 = QTables2
        self.experimentName = experimentName
        self.agent1Collisions = agent1Collisions
        self.agent2Collisions = agent2Collisions

    def run(self):

        path = "out/" + self.experimentName

        if not os.path.exists(path):
            os.makedirs(path)

        env = Environment()
        env.initialiseAgents(exp)
        env.agent1Collisions = []
        env.agent2Collisions = []

        for e in range(0, len(exp)):
            print(f"\n*************** Experiment {e + 1} - " + str(exp[e]) + " starting **********")
            for run in range(0, self.numRuns):
                print("\n\t\tGridWorld: *************** Run " + str(run + 1) + " starting ***************")

                env.doExperiment(run, self.experimentName, exp, e)

                qTable1, qTable2 = env.getQTable()
                self.QTables1.append(qTable1)
                self.QTables2.append(qTable2)

        self.results1.append(env.getMovesToGoal1())

        self.agent1Collisions = env.getAgent1Collisions()
        self.agent2Collisions = env.getAgent2Collisions()

        resultsToCSVFile(results1=self.results1, experimentName=self.experimentName,
                         numRuns=self.numRuns, numEpisodes=env.numEpisodes, experimentList=exp)

        QTablesToFile(QTables1=self.QTables1, QTables2=self.QTables2,
                      basesForStateNo=[Environment.getXDimension(env), Environment.getYDimension(env)],
                      experimentName=self.experimentName, numAgents=env.numAgents, experiments=exp,
                      numRuns=self.numRuns)

        CollisionGraphing(self.agent1Collisions, 1, env.numEpisodes, self.numRuns)
        CollisionGraphing(self.agent2Collisions, 2, env.numEpisodes, self.numRuns)

        MovesToGoalGraphing(self.results1)


if __name__ == '__main__':
    g = Grid()
    g.run()
