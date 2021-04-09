import os
import time
from Utilities import *
from Environment import Environment


class Grid:
    def __init__(
            self,
            results=None,
            QTables=None,
            numRuns=10,
            experimentName="Gridworld_" + str(round(time.time() * 1000))
    ):
        if QTables is None:
            QTables = []
        if results is None:
            results = []

        self.numRuns = numRuns
        self.results = results
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

            self.results.append(env.getMovesToGoal())
            self.QTables.append(env.getQTable())

        resultsToCSVFile(results=self.results, experimentName=self.experimentName)
        QTablesToFile(QTables=self.QTables,
                      basesForStateNo=[Environment.getXDimension(env), Environment.getYDimension(env)],
                      experimentName=self.experimentName)


if __name__ == '__main__':
    g = Grid()
    g.run()
