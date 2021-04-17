import os
import time
from Utilities import *
from Environment import Environment
import pandas as pd
import matplotlib.pyplot as plt


class Grid:
    def __init__(
            self,
            results1=None,
            results2=None,
            QTables=None,
            numRuns=10,
            experimentName="Gridworld_" + str(round(time.time() * 1000))
    ):
        if QTables is None:
            QTables = []
        if results1 is None:
            results1 = []
        if results2 is None:
            results2 = []

        self.numRuns = numRuns
        self.results1 = results1
        self.results2 = results2
        self.QTables = QTables
        self.experimentName = experimentName

    def run(self):

        path = "out/" + self.experimentName

        if not os.path.exists(path):
            os.makedirs(path)

        env = Environment()

        for run in range(0, self.numRuns):
            print("\nGridWorld: *************** Run " + str(run) + " starting ***************")

            env.doExperiment()
            res1 = env.getMovesToGoal1()
            res2 = env.getMovesToGoal2()
            self.results1.append(res1)
            self.results2.append(res2)

            if run == 0:
                df = pd.DataFrame(res1, columns=['Moves-to-Goal'])
                df.loc[run] = run, res1

            self.QTables.append(env.getQTable())

        resultsToCSVFile(results1=self.results1, results2=self.results2, experimentName=self.experimentName)
        QTablesToFile(QTables=self.QTables,
                      basesForStateNo=[Environment.getXDimension(env), Environment.getYDimension(env)],
                      experimentName=self.experimentName)
        print(df)
        df.plot(y='Moves-to-Goal', kind='line')
        plt.title("Moves to Goal")
        plt.show()


if __name__ == '__main__':
    g = Grid()
    g.run()
