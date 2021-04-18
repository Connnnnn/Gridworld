import csv


def getXYfromStateNo(stateNo, basesForStateNo):
    state = [0] * len(basesForStateNo)

    inputstateNo = stateNo

    for i in range(len(state) - 1, -1, -1):
        state[i] = (inputstateNo % basesForStateNo[i])
        inputstateNo = inputstateNo // basesForStateNo[i]

    return state


def getStateNoFromXY(state, basesForStateNo):
    numStates = basesForStateNo[0] * basesForStateNo[1]
    stateNo = 0

    for i in range(0, len(state)):
        stateNo = stateNo * basesForStateNo[i] + state[i]

    if stateNo >= numStates or stateNo < 0:
        print("Vector Conversion Error - X: " + str(state[0]) + " Y: " + str(state[1]))
        print("Resultant State Number " + str(stateNo))
        print("max allowed states: " + str(numStates))

    return stateNo


def resultsToCSVFile(results1, results2, experimentName):
    output = ["Episode No. "]

    # Include the Second results
    # And get the output correctly moving into their cells
    for run in results1:
        output[0] += f'Run{run} '

    for time in range(len(results1[0])):

        output.append(str(time))

        for run in range(0, len(results1)):
            output.append(str(results1[run][time]))

    with open("out/" + experimentName + "/" + experimentName + "_stepsToGoal.csv", mode='w') as out:
        writer = csv.writer(out, delimiter=",")
        writer.writerows(output)


def qTableAsString(qTable1, qTable2, basesForStateNo):
    output = "State#	Xcoord	Ycoord	|	North	East	South	West \t\t\t\t\t\t\t\t\t| State#	Xcoord	Ycoord	|	North	East	South	West"

    for s in range(len(qTable1)):
        temp = ""
        coord = getXYfromStateNo(stateNo=s, basesForStateNo=basesForStateNo)
        temp += "\n " + str(s) + "\t\t" + str(coord[0]) + "\t\t" + str(coord[
                                                                           1]) + "\t\t|\t" + f'{qTable1[s][0]:.3g} \t' + "\t" + f'{qTable1[s][1]:.3g}\t' + "\t" + f'{qTable1[s][2]:.3g}\t' + "\t" + f'{qTable1[s][3]:.3g}'
        output += temp
        length = len(temp)

        if length > 42:
            output += "\t\t\t\t\t\t|\t"
        elif 42 >= length > 38:
            output += "\t\t\t\t\t\t|\t"
        elif 38 >= length > 34:
            output += "\t\t\t\t\t\t\t|\t"
        elif 34 >= length > 30:
            output += "\t\t\t\t\t\t\t\t|\t"
        elif 30 >= length:
            output += "\t\t\t\t\t\t\t\t\t\t|\t"

        output += str(s) + "\t\t" + str(coord[0]) + "\t\t"+str(coord[
                          1]) + "\t\t|\t" + f'{qTable2[s][0]:.3g}' + "\t\t" + f'{qTable2[s][1]:.3g}' + "\t\t" + f'{qTable2[s][2]:.3g}' + "\t\t" + f'{qTable2[s][3]:.3g}'

    return output


def QTablesToFile(QTables1, QTables2, basesForStateNo, experimentName, numAgents):
    output = ""

    for run in range(len(QTables1)):
        output += "*************** Q table for run " + str(run+1) + " ***************\n"
        for a in range(numAgents):
            output += f"|*************** Agent {a + 1} ***************| \t\t\t\t\t\t\t\t\t\t\t\t\t"
        output += "\n"
        output += qTableAsString(QTables1[run], QTables2[run], basesForStateNo) + "\n\n"

    file = open("out/" + experimentName + "/" + experimentName + "_QTables.txt", "w")
    file.write(output)
