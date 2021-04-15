import csv


def getXYfromStateNo(stateNo, basesForStateNo):
    state = [0] * len(basesForStateNo)

    inputstateNo = stateNo

    for i in range(len(state) - 1, -1, -1):
        state[i] = (inputstateNo % basesForStateNo[i])
        inputstateNo = inputstateNo // basesForStateNo[i]

    return state


def qTableAsString(qTable, basesForStateNo):
    output = "State#	Xcoord	Ycoord	|	North	East	South	West"

    for s in range(len(qTable)):
        coord = getXYfromStateNo(stateNo=s, basesForStateNo=basesForStateNo)
        output += "\n " + str(s) + "		" + str(coord[0]) + "		" + str(coord[
                                                                                     1]) + "		|	" + f'{qTable[s][0]:.3g}' + "	" + f'{qTable[s][1]:.3g}' + "	" + f'{qTable[s][2]:.3g}' + "	" + f'{qTable[s][3]:.3g} '

    return output


def getStateNoFromXY(state, basesForStateNo):
    numStates = basesForStateNo[0] * basesForStateNo[1]
    stateNo = 0

    for i in range(0, len(state)):
        stateNo = stateNo * basesForStateNo[i] + state[i]

    if stateNo >= numStates or stateNo < 0:
        print("Vector Conversion Error - X: " + state[0] + " Y: " + state[1])
        print("Resultant State Number " + stateNo)
        print("max allowed states: " + numStates)

    return stateNo


# def resultsToCSVStr(results):
#     output = "Episode No.,"
#
#     for run in results:
#         output += "Run" + str(run) + "Steps,"
#
#     for time in range(len(results[0])):
#
#         output += "\n" + str(time) + ","
#         for run in range(len(results)):
#             output += "" + str(results[run][time]) + ","
#
#     return output


def resultsToCSVFile(results1, results2, experimentName):
    output = ["Episode No. "]

    # Include the Second results
    # And get the output correctly moving into their cells
    for run in results1:

        output[0] += f'Run{run} '

    for time in range(len(results1[0])):

        output.append(str(time) + str(" "))

        for run in range(1,len(results1)):
            output.append(str(results1[run][time]) + str(' '))

    # resultsTable = resultsToCSVStr(results1)

    with open("out/" + experimentName + "/" + experimentName + "_stepsToGoal.csv", mode='w') as out:
        writer = csv.writer(out, delimiter=" ")
        writer.writerow(output)


def QTablesToFile(QTables, basesForStateNo, experimentName):
    output = ""

    for run in range(len(QTables)):
        output += "*************** Q table for run " + str(run) + " ***************\n"
        output += qTableAsString(QTables[run], basesForStateNo) + "\n\n"

    file = open("out/" + experimentName + "/" + experimentName + "_QTables.txt", "w")
    file.write(output)
