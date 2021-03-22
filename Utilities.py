import csv


class Utilities:

    def qTableAsString(self, qTable, basesForStateNo):
        output = "State#	Xcoord	Ycoord	|	North	East	South	West"

        for s in range(len(qTable)):
            coord = self.getXYfromStateNo(self=self, stateNo=s, basesForStateNo=basesForStateNo)
            output += "\n " + str(s) + "		" + str(coord[0]) + "		" + str(coord[1]) + "		|	" + f'{qTable[s][0]:.3g}' + "	" + f'{qTable[s][1]:.3g}' + "	" + f'{qTable[s][2]:.3g}' + "	" + f'{qTable[s][3]:.3g}'

        return output

    def qTableToConsole(self, qTable, basesForStateNo):
        print(self.qTableAsString(qTable, basesForStateNo))

    def qTableToFile(self, qTable, basesForStateNo, fileName):
        print(self.qTableAsString(qTable, basesForStateNo))

    @classmethod
    def getStateNoFromXY(cls, state, basesForStateNo):

        numStates = basesForStateNo[0] * basesForStateNo[1]
        stateNo = 0

        for i in range(0, len(state)):
            stateNo = stateNo * basesForStateNo[i] + state[i]

        if stateNo >= numStates or stateNo < 0:
            print("Vector Conversion Error - X: " + state[0] + " Y: " + state[1])
            print("Resultant State Number " + stateNo)
            print("max allowed states: " + numStates)

        return stateNo

    def getXYfromStateNo(self, stateNo, basesForStateNo):

        state = [0] * 3
        inputstateNo = stateNo
        for i in range(len(state) - 1, -1):
            state[i] = inputstateNo % basesForStateNo[i]
            inputstateNo = inputstateNo / basesForStateNo[i]

        return state

    @classmethod
    def resultsToCSVStr(cls, results):
        output = "Episode No.,"

        for run in results:
            output += "Run" + str(run) + "steps,"

        for time in range(len(results[0])):

            output += "\n" + str(time) + ","
            for run in range(len(results)):
                output += "" + str(results[run][time]) + ","

        return output

    @classmethod
    def resultsToCSVFile(cls, results, experimentName):
        resultsTable = Utilities.resultsToCSVStr(results)
        with open("out/" + experimentName + "/" + experimentName + "_stepsToGoal.csv", mode='w') as out:
            writer = csv.writer(out)
            writer.writerows(resultsTable)

    @classmethod
    def QTablesToFile(cls, QTables, basesForStateNo, experimentName):
        output = ""

        for run in range(len(QTables)):
            output += "*************** Q table for run " + str(run) + " ***************\n"
            output += cls.qTableAsString(cls, QTables[run], basesForStateNo) + "\n\n"

        file = open("out/" + experimentName + "/" + experimentName + "_QTables.txt", "w")
        file.write(output)

