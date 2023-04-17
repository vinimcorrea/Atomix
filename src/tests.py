from uniformed_algortihms import *
from atomix_state import AtomixState
from atomix import read_level, bfs
import os
import matplotlib.pyplot as plt


class TestSuite:
    def __init__(self) -> None:
        self.BFS = BFS()
        self.DFS = DFS()
        self.IDDFS = IDDFS()
        self.GREEDY = GREEDY()
        self.ASTAR = ASTAR()
        self.WEIGHTEDASTAR = WEIGHTEDASTAR()
        self.IDASTAR = IDASTAR()

    
    def testMetrics(self):  

        bfsMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': [], 'nMoves':[]}
        # dfsMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': [], 'nMoves':[]}
        iddfsMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': [], 'nMoves':[]}
        greedyMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': [], 'nMoves':[]}
        astarMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': [], 'nMoves':[]}
        wAstarMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': [], 'nMoves':[]}
        IdAstarMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': [], 'nMoves':[]}

        for i in range(1,4):

            map = read_level(i)

            print("RUNNING BFS\n")
            self.BFS.algorithm(map)
            # print("RUNNING DFS\n")
            # self.DFS.algorithm(map)
            print("RUNNING IDDFS\n")
            self.IDDFS.algorithm(map, 1000)
            print("RUNNING GREEDY\n")
            self.GREEDY.algorithm(map, heuristic)
            print("RUNNING ASTAR\n")
            self.ASTAR.algorithm(map, heuristic)
            print("RUNNING WEIGHTED ASTAR\n")
            self.WEIGHTEDASTAR.algorithm(map)
            self.IDASTAR.algorithm(map)

            print("\n")
            print("\n")

            print("***TESTING METRICS FOR LEVEL " + str(i) + " ***\n")

            print("\n")

            print("---BFS METRICS---\n")
            print("BFS TIME: " + str(self.BFS.getSolveTime()) + " seconds\n")
            print("BFS MEMORY USAGE: " + str(self.BFS.getMaxMemory()) + "\n")
            print("BFS NUMBER OF OPERATIONS: " + str(self.BFS.getNOperations()) + "\n")
            print("BFS NUMBER OF MOVES: " + str(self.BFS.getNMoves()) + "\n")

            bfsMetrics["solveTime"].append(self.BFS.getSolveTime())
            bfsMetrics["maxMemory"].append(self.BFS.getMaxMemory())
            bfsMetrics["nOperations"].append(self.BFS.getNOperations())
            bfsMetrics["nMoves"].append(self.BFS.getNMoves())

            print("\n")

            # print("---DFS METRICS---\n")
            # print("DFS TIME: " + str(self.DFS.getSolveTime) + "\n")
            # print("DFS MEMORY USAGE: " + str(self.DFS.getMaxMemory()) + "\n")
            # print("DFS OPERATIONS: " + str(self.DFS.getNOperations()) + "\n")
            # print("DFS NUMBER OF MOVES: " + str(self.DFS.getNMoves()) + "\n")

            # dfsMetrics["solveTime"].append(self.DFS.getSolveTime)
            # dfsMetrics["maxMemory"].append(self.DFS.getMaxMemory())
            # dfsMetrics["nOperations"].append(self.DFS.getNOperations())
            # dfsMetrics["nMoves"].append(self.DFS.getNMoves())

            # print("\n")

            print("---IDDFS METRICS---\n")
            print("IDDFS TIME: " + str(self.IDDFS.getSolveTime()) + "\n")
            print("IDDFS MEMORY USAGE: " + str(self.IDDFS.getMaxMemory()) + "\n")
            print("IDDFS OPERATIONS: " + str(self.IDDFS.getNOperations()) + "\n")
            print("IDDFS NUMBER OF MOVES: " + str(self.IDDFS.getNMoves()) + "\n")

            iddfsMetrics["solveTime"].append(self.IDDFS.getSolveTime())
            iddfsMetrics["maxMemory"].append(self.IDDFS.getMaxMemory())
            iddfsMetrics["nOperations"].append(self.IDDFS.getNOperations())
            iddfsMetrics["nMoves"].append(self.IDDFS.getNMoves())

            print("\n")

            print("---GREEDY METRICS---\n")
            print("GREEDY TIME: " + str(self.GREEDY.getSolveTime) + "\n")
            print("GREEDY MEMORY USAGE: " + str(self.GREEDY.getMaxMemory()) + "\n")
            print("GREEDY OPERATIONS: " + str(self.GREEDY.getNOperations()) + "\n")
            print("GREEDY NUMBER OF MOVES: " + str(self.GREEDY.getNMoves()) + "\n")

            greedyMetrics["solveTime"].append(self.GREEDY.getSolveTime)
            greedyMetrics["maxMemory"].append(self.GREEDY.getMaxMemory())
            greedyMetrics["nOperations"].append(self.GREEDY.getNOperations())
            greedyMetrics["nMoves"].append(self.GREEDY.getNMoves())

            print("\n")

            print("---A* METRICS---\n")
            print("A* TIME: " + str(self.ASTAR.getSolveTime) + "\n")
            print("A* MEMORY USAGE: " + str(self.ASTAR.getMaxMemory()) + "\n")
            print("A* OPERATIONS: " + str(self.ASTAR.getNOperations()) + "\n")
            print("A* NUMBER OF MOVES: " + str(self.ASTAR.getNMoves()) + "\n")

            astarMetrics["solveTime"].append(self.ASTAR.getSolveTime)
            astarMetrics["maxMemory"].append(self.ASTAR.getMaxMemory())
            astarMetrics["nOperations"].append(self.ASTAR.getNOperations())
            astarMetrics["nMoves"].append(self.ASTAR.getNMoves())

            print("\n")

            print("---WEIGHTEDASTAR METRICS---\n")
            print("WEIGHTED A* TIME: " + str(self.WEIGHTEDASTAR.getSolveTime) + "\n")
            print("WEIGHTED A* MEMORY USAGE: " + str(self.WEIGHTEDASTAR.getMaxMemory()) + "\n")
            print("WEIGHTED A* OPERATIONS: " + str(self.WEIGHTEDASTAR.getNOperations()) + "\n")
            print("WEIGHTED A* NUMBER OF MOVES: " + str(self.WEIGHTEDASTAR.getNMoves()) + "\n")

            wAstarMetrics["solveTime"].append(self.WEIGHTEDASTAR.getSolveTime)
            wAstarMetrics["maxMemory"].append(self.WEIGHTEDASTAR.getMaxMemory())
            wAstarMetrics["nOperations"].append(self.WEIGHTEDASTAR.getNOperations())
            wAstarMetrics["nMoves"].append(self.WEIGHTEDASTAR.getNMoves())

            print("\n")

            # print("---IDAASTAR METRICS---\n")
            # print("IDA* TIME: " + str(self.IDAASTAR.getSolveTime()) + "\n")
            # print("IDA* MEMORY USAGE: " + str(self.IDASTAR.getMaxMemory()) + "\n")
            # print("IDA* OPERATIONS: " + str(self.IDASTAR.getNOperations()) + "\n")
            # print("IDA* NUMBER OF MOVES: " + str(self.IDASTAR.getNMoves()) + "\n")

            # IdAstarMetrics["solveTime"].append(self.IDASTAR.getSolveTime())
            # IdAstarMetrics["maxMemory"].append(self.IDASTAR.getMaxMemory())
            # IdAstarMetrics["nOperations"].append(self.IDASTAR.getNOperations())
            # IdAstarMetrics["nMoves"].append(self.IDASTAR.getNMoves())

            # print("\n")

            print("***END OF METRICS TEST FOR LEVEL " + str(i) + " ***\n")

        return bfsMetrics, iddfsMetrics, greedyMetrics, astarMetrics, wAstarMetrics

    
def main():

    test = TestSuite()

    bfsMetrics, iddfsMetrics, greedyMetrics, astarMetrics, wastarMetrics = test.testMetrics()

    levels = [1, 2, 3, 4]

    figure, axis = plt.subplots(2, 2)

    axis[0,0].set_title("Solve Time")
    axis[0,1].set_title("Max Memory Usage")
    axis[1,0].set_title("Number of Operations")
    axis[1,1].set_title("Number of Operations")

    # /// TIME GRAPH PLOT FOR ALL ALGORITHMS FOR 4 LEVELS ///

    bfs_time_values = bfsMetrics["solveTime"]
    # dfs_time_values = dfsMetrics["solveTime"]
    iddfs_time_values = iddfsMetrics["solveTime"]
    greedy_time_values = greedyMetrics["solveTime"]
    astar_time_values = astarMetrics["solveTime"]
    wAstar_time_values = wastarMetrics["solveTime"]
    # idastar_time_values = idastarMetrics["solveTime"]

    axis[0,0].plot(levels, bfs_time_values, 'b')
    # axis[0,0].plot(levels, dfs_time_values, 'r')
    axis[0,0].plot(levels, iddfs_time_values, 'c')
    axis[0,0].plot(levels, greedy_time_values, 'm')
    axis[0,0].plot(levels, astar_time_values, 'y')
    axis[0,0].plot(levels, wAstar_time_values, 'k')
    # axis[0,0].plot(levels, idastar_time_values, 'g')

    # /// MAX MEMORY GRAPH PLOT FOR ALL ALGORITHMS FOR 4 LEVELS ///

    bfs_mem_values = bfsMetrics["maxMemory"]
    # dfs_mem_values = dfsMetrics["maxMemory"]
    iddfs_mem_values = iddfsMetrics["maxMemory"]
    greedy_mem_values = greedyMetrics["maxMemory"]
    astar_mem_values = astarMetrics["maxMemory"]
    wAstar_mem_values = wastarMetrics["maxMemory"]
    # idastar_mem_values = idastarMetrics["maxMemory"]

    axis[0,1].plot(levels, bfs_mem_values, 'b')
    # axis[0,1].plot(levels, dfs_mem_values, 'r')
    axis[0,1].plot(levels, iddfs_mem_values, 'c')
    axis[0,1].plot(levels, greedy_mem_values, 'm')
    axis[0,1].plot(levels, astar_mem_values, 'y')
    axis[0,1].plot(levels, wAstar_mem_values, 'k')
    # axis[0,1].plot(levels, idastar_mem_values, 'g')


    # /// NUMBER OF OPERATIONS GRAPH PLOT FOR ALL ALGORITHMS FOR 4 LEVELS ///

    bfs_op_values = bfsMetrics["nOperations"]
    # dfs_op_values = dfsMetrics["nOperations"]
    iddfs_op_values = iddfsMetrics["nOperations"]
    greedy_op_values = greedyMetrics["nOperations"]
    astar_op_values = astarMetrics["nOperations"]
    wAstar_op_values = wastarMetrics["nOperations"]
    # idastar_op_values = idastarMetrics["nOperation"]

    axis[1,0].plot(levels, bfs_op_values, 'b')
    # axis[1,0].plot(levels, dfs_op_values, 'r')
    axis[1,0].plot(levels, iddfs_op_values, 'c')
    axis[1,0].plot(levels, greedy_op_values, 'm')
    axis[1,0].plot(levels, astar_op_values, 'y')
    axis[1,0].plot(levels, wAstar_op_values, 'k')
    # axis[1,0].plot(levels, idastar_op_values, 'g')


    # /// NUMBER OF MOVES GRAPH PLOT FOR ALL ALGORITHMS FOR 4 LEVELS ///

    bfs_moves = bfsMetrics["nMoves"]
    # dfs_moves = dfsMetrics["nMoves"]
    iddfs_moves = iddfsMetrics["nMoves"]
    greedy_moves = greedyMetrics["nMoves"]
    astar_moves = astarMetrics["nMoves"]
    wAstar_moves = wastarMetrics["nMoves"]
    # idastar_moves = idastarMetrics["nMoves"]
    
    axis[1,1].plot(levels, bfs_moves, 'b')
    # axis[1,1].plot(levels, dfs_moves, 'r')
    axis[1,1].plot(levels, iddfs_moves, 'c')
    axis[1,1].plot(levels, greedy_moves, 'm')
    axis[1,1].plot(levels, astar_moves, 'y')
    axis[1,1].plot(levels, wAstar_moves, 'k')
    # axis[1,1].plot(levels, idastar_moves, 'g')

    plt.show()

    return None

if __name__ == "__main__":
    main()

