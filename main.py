import configparser
import os
import time
from Utilities import *
from Environment import Environment
import pandas as pd
import matplotlib.pyplot as plt

exp0 = ["MA2-SD.txt"]
exp1 = ["MA-CL-1"]
exp2 = ["MA-CL-1", "MA-CL-2", "MA-CL-3", "MA-CL-4"]
exp3 = ["MA-CL-1", "MA-CL-2", "MA-CL-3", "MA-CL-4", "MA-CL-5", "MA-CL-6"]
exp = exp3


class Grid:
    def __init__(
            self,
            results1=None,
            results2=None,
            QTables1=None,
            QTables2=None,
            numRuns=10,
            experimentName="Gridworld_" + str(round(time.time() * 1000))
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

    def run(self):

        path = "out/" + self.experimentName

        if not os.path.exists(path):
            os.makedirs(path)

        env = Environment()
        env.initialiseAgents(exp)

        for e in range(0, len(exp)):
            print(f"\n*************** Experiment {e + 1} - " + str(exp[e]) + " starting **********")
            for run in range(0, self.numRuns):
                print("\n\t\tGridWorld: *************** Run " + str(run + 1) + " starting ***************")

                env.doExperiment(run, self.experimentName, exp, e)
                res1 = env.getMovesToGoal1()
                res2 = env.getMovesToGoal2()
                self.results1.append(res1)
                self.results2.append(res2)

                # if run == 0:
                #     df = pd.DataFrame(res1, columns=['Moves-to-Goal'])
                #     df.loc[0] = run, res1
                #     df.plot(y='Moves-to-Goal', kind='line')
                #     plt.title("Moves to Goal")
                #     plt.show()

                qTable1, qTable2 = env.getQTable()
                self.QTables1.append(qTable1)
                self.QTables2.append(qTable2)

        resultsToCSVFile(results1=self.results1, results2=self.results2, experimentName=self.experimentName)
        QTablesToFile(QTables1=self.QTables1, QTables2=self.QTables2,
                      basesForStateNo=[Environment.getXDimension(env), Environment.getYDimension(env)],
                      experimentName=self.experimentName, numAgents=env.numAgents, experiments=exp, numRuns=self.numRuns)


if __name__ == '__main__':
    g = Grid()
    g.run()
