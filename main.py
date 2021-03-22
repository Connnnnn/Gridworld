import os
import time
from Agent import Agent
from Utilities import Utilities
from Environment import Environment


class Grid:
    def __init__(
            self,
            x=[],
            y=[],
            results=[],
            QTables=[],
            numRuns=10,
            experimentName="Gridworld_" + str(round(time.time() * 1000))
    ):
        self.numRuns = numRuns
        self.results = results
        self.QTables = QTables
        self.experimentName = experimentName
        self.x = x
        self.y = y

    def run(self):

        path = "out/" + self.experimentName

        if not os.path.exists(path):
            os.makedirs(path)

        env = Environment()

        for run in range(0, self.numRuns):
            print("\nExpRunner: *************** Run " + str(run) + " starting ***************")

            env.doExperiment()

            self.results.append(env.getMovesToGoal())
            self.QTables.append(env.getQTable())

        Utilities.resultsToCSVFile(self.results, self.experimentName)
        Utilities.QTablesToFile(self.QTables,
                                basesForStateNo=[Environment.getXDimension(env), Environment.getYDimension(env)],
                                experimentName=self.experimentName)


if __name__ == '__main__':
    g = Grid()
    g.run()
