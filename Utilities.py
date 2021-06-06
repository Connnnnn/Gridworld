import csv
import os
import random
import matplotlib.pyplot as plt


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


def resultsToCSVFile(results1, experimentName, numRuns, numEpisodes, experimentList):
    output = [["" for _ in range(numRuns * len(experimentList) + len(experimentList))] for _ in range(numEpisodes)]

    output[0][0] = "Episode No. "
    for exp in range(len(experimentList)):

        for run in range(numRuns):
            output[0][(run + 1 + (exp * (numRuns + 1)))] = 'Run' + str(exp + 1) + "_" + str(run + 1)

        for run in range(numRuns + 1):
            for episode in range(0, numEpisodes):
                if run == 0 and episode > 0:
                    output[episode][0] = episode
                elif episode == 0:
                    continue
                else:
                    output[episode][run + exp * (numRuns + 1)] = results1[0][
                        ((episode - 1) + numEpisodes * (run - 1) + exp * numRuns * numEpisodes)]

    with open("out/" + experimentName + "/" + experimentName + "_stepsToGoal.csv", mode='w', newline='') as out:
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

        output += str(s) + "\t\t" + str(coord[0]) + "\t\t" + str(coord[
                                                                     1]) + "\t\t|\t" + f'{qTable2[s][0]:.3g}' + "\t\t" + f'{qTable2[s][1]:.3g}' + "\t\t" + f'{qTable2[s][2]:.3g}' + "\t\t" + f'{qTable2[s][3]:.3g}'

    return output


def QTablesToFile(QTables1, QTables2, basesForStateNo, experimentName, numAgents, experiments, numRuns):
    output = ""

    for e in range(0, len(experiments)):
        output += "*************** Experiment " + str(e + 1) + " ***************\n"
        for run in range(numRuns):
            output += "*************** Q table for Run " + str(run + 1) + " ***************\n"
            for a in range(numAgents):
                output += f"|*************** Agent {a + 1} ***************| \t\t\t\t\t\t\t\t\t\t\t\t\t"
            output += "\n"
            output += qTableAsString(QTables1[run], QTables2[run], basesForStateNo) + "\n\n"

    file = open("out/" + experimentName + "/" + experimentName + "_QTables.txt", "w")
    file.write(output)


def decision(probability):
    return random.random() < probability


def heatmapPrint(Heatmap, run, e, experimentName, agentNum):
    plt.title(f'Run {run + 1}\n Heatmap Agent {agentNum} - Experiment {e + 1}')
    plt.imshow(Heatmap, cmap='hot', interpolation='nearest')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')

    path = "out/" + experimentName + "/Heatmaps/Agent" + str(agentNum) + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    filename = path + "Agent" + str(agentNum) + "-Experiment" + str(e + 1) + "Run" + str(run + 1) + ".png"
    plt.savefig(filename)
    plt.clf()
    plt.close()


def CollisionGraphing(collisions, agentNum, numEpisodes, numRuns):
    for i in range(len(collisions)):
        if i % (numEpisodes * numRuns) == 0 and i != 0:
            plt.axvline(x=i, ymin=0.05, ymax=0.95, color='black', label='axvline - % of full height')

    plt.title(f'Agent Collisions for Agent {agentNum}')
    plt.xlabel('Episodes')
    plt.ylabel('Number of Collisions')

    plt.plot(collisions)
    plt.show()
    plt.clf()
    plt.close()


def MovesToGoalGraphing(results):
    plt.title(f'Steps to Goal')
    plt.xlabel('Episodes')
    plt.ylabel('Number of Steps')

    plt.plot(results[0])
    plt.show()
    plt.clf()
    plt.close()


def ManualGraphMaker():

    map = [
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    ]

    plt.title(f'Quick Sand Experiment 4')
    plt.imshow(map, cmap='hot', interpolation='nearest')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')

    plt.show()
    plt.clf()
    plt.close()
