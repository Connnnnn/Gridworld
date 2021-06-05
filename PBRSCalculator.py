from collections import deque
import numpy as np


# This file is a utility used in order to create an array equal to the size of the environment
# The foundation of this file came from a breadth first search tutorial below
# https://www.geeksforgeeks.org/shortest-path-in-a-binary-maze/
# From there I find the Manhattan Distance from every location in the maze and make two 2d Arrays, one for each Agent
# This is then put into the configuration file for the environment

# If an environment doesnt have the PBRS Values in their configuration file then it will run this file when there is a configuration change in order to create the table


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class QueueNode:
    def __init__(self, pt: Point, dist: int):
        self.pt = pt
        self.dist = dist


def isValid(xDim, yDim, row: int, col: int):
    return (row >= 0) and (row < xDim) and (col >= 0) and (col < yDim)


rowNum = [-1, 0, 0, 1]
colNum = [0, -1, 1, 0]


def BFS(obstacles, xDim, yDim, src: Point, dest: Point):
    if obstacles[src.x][src.y] != 0 or obstacles[dest.x][dest.y] != 0:
        return -1

    visited = [[False for i in range(yDim)] for j in range(xDim)]

    visited[src.x][src.y] = True

    q = deque()
    s = QueueNode(src, 0)
    q.append(s)

    while q:

        curr = q.popleft()

        pt = curr.pt
        if pt.x == dest.x and pt.y == dest.y:
            return curr.dist

        for i in range(4):
            x = pt.x + rowNum[i]
            y = pt.y + colNum[i]

            if isValid(xDim, yDim, x, y) and obstacles[x][y] == 0 and not visited[x][y]:
                visited[x][y] = True
                Adjcell = QueueNode(Point(x, y), curr.dist + 1)
                q.append(Adjcell)

    return -1


def initialisePBRSMap(xDim, yDim):
    return [[0.0 for _ in range(xDim)] for _ in range(yDim)]


def calc_state_potential(x, y, dest, obstacles, xDim, yDim):
    dist = BFS(obstacles, xDim, yDim, src=Point(x, y), dest=dest)
    currDist = dist
    maxDist = xDim * yDim
    pbrs = maxDist - currDist

    if pbrs == 101:
        pbrs = 0

    return pbrs


def main(xDim, yDim, goalXY, obstacles):
    dest1 = Point(goalXY[0], goalXY[1])

    PBRSMap = initialisePBRSMap(xDim, yDim)

    for i in range(xDim):
        for j in range(yDim):
            PBRSMap[i][j] = calc_state_potential(i, j, dest1, obstacles, xDim, yDim)

    return PBRSMap


def manualMain():
    source1 = Point(0, 0)
    dest1 = Point(9, 9)
    source2 = Point(9, 0)
    dest2 = Point(0, 9)

    obstacles = [
        [0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    ]
    ROW = 10
    COL = 10

    dist1 = BFS(obstacles, ROW, COL, source1, dest1)
    dist2 = BFS(obstacles, ROW, COL, source2, dest2)

    if dist1 != -1:
        print("Shortest Path is for Agent 1 is", dist1)
    else:
        print("Shortest Path doesn't exist")

    if dist2 != -1:
        print("Shortest Path is for Agent 2 is", dist2)
    else:
        print("Shortest Path doesn't exist")

    if dist1 is not dist2:
        print("Error in map; one path longer")

    PBRSMap1 = initialisePBRSMap(ROW, COL)

    for i in range(ROW):
        for j in range(COL):
            PBRSMap1[i][j] = calc_state_potential(i, j, dest1, obstacles, ROW, COL)

    print(np.matrix(PBRSMap1))

    PBRSMap2 = initialisePBRSMap(ROW, COL)

    for i in range(ROW):
        for j in range(COL):
            PBRSMap2[i][j] = calc_state_potential(i, j, dest2, obstacles, ROW, COL)

    print(np.matrix(PBRSMap2))


if __name__ == "__main__":
    manualMain()
