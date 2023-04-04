from uniformed_algortihms import *
from atomix_state import AtomixState
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

    def loadMap(self, level):
        # change filename to level + level
        filename = f"level1.txt"
        filepath = os.path.join("resources/test-levels", filename)

        level_map = []
        atom_map = {}
        molecule_name_phase = None

        is_molecule_read = False
        is_atom_map_read = False

        with open(filepath) as f:
            for line in f:
                line_strip = line.strip()
                if molecule_name_phase is None:
                    molecule_name_phase = line_strip
                    continue
                if line_strip.startswith('#'):
                    level_map.append(line_strip)
                    continue
                if line_strip == '' and not is_molecule_read:
                    is_molecule_read = True
                    continue
                if line_strip != '' and is_molecule_read and not is_atom_map_read:
                    molecule_to_form = ''
                    for c in line_strip:
                        if c.isdigit():
                            molecule_to_form += c
                        elif c.isalpha():
                            molecule_to_form += '.'
                        else:
                            molecule_to_form += '\n'
                if line_strip == '' and not is_atom_map_read:
                    is_atom_map_read = True
                if line_strip != '' and is_atom_map_read:
                    num, *atom_data = line_strip.split()
                    atom, links = atom_data[0], atom_data[1:]
                    atom_map[int(num)] = {"atom": atom, "connections": {}}
                    for l in links:
                        direction, neighbor_num = l[-1], int(l[:-1])
                        atom_map[int(num)]["connections"][direction] = neighbor_num

        return level_map, atom_map, molecule_name_phase, molecule_to_form

    def testMetrics(self):  

        bfsMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': []}
        dfsMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': []}
        iddfsMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': []}
        greedyMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': []}
        astarMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': []}
        wAstarMetrics = {'solveTime': [], 'maxMemory': [], 'nOperations': []}

        for i in range(1,5):

            game_dataset = self.loadMap(i)

            board, atom_map, molecule_name, molecule_structure = game_dataset

            map = AtomixState(board, molecule_structure)

            self.BFS.algorithm(map)
            # self.DFS.algorithm(map)
            # self.IDDFS.algorithm(map)
            # self.GREEDY.algorithm(map)
            # self.ASTAR.algorithm(map)
            # self.WEIGHTEDASTAR.algorithm(map)

            print("\n")
            print("\n")

            print("***TESTING METRICS FOR LEVEL " + str(i) + " ***\n")

            print("\n")

            print("---BFS METRICS---\n")
            print("BFS TIME: " + str(self.BFS.getSolveTime()) + " seconds\n")
            print("BFS MEMORY USAGE: " + str(self.BFS.getMaxMemory()) + "\n")
            print("BFS NUMBER OF OPERATIONS: " + str(self.BFS.getNOperations()) + "\n")

            bfsMetrics["solveTime"].append(self.BFS.getSolveTime())
            bfsMetrics["maxMemory"].append(self.BFS.getMaxMemory())
            bfsMetrics["nOperations"].append(self.BFS.getNOperations())

            print("\n")

            # print("---DFS METRICS---\n")
            # print("DFS TIME: " + str(self.DFS.getSolveTime()) + "\n")
            # print("DFS MEMORY USAGE: " + str(self.DFS.getMaxMemory()) + "\n")
            # print("DFS OPERATIONS: " + str(self.DFS.getNOperations()) + "\n")

            # dfsMetrics["solveTime"] = self.DFS.getSolveTime()
            # dfsMetrics["maxMemory"] = self.DFS.getMaxMemory()
            # dfsMetrics["nOperations"] = self.DFS.getNOperations()

            # print("\n")

            # print("---IDDFS METRICS---\n")
            # print("IDDFS TIME: " + str(self.IDDFS.getSolveTime()) + "\n")
            # print("IDDFS MEMORY USAGE: " + str(self.IDDFS.getMaxMemory()) + "\n")
            # print("IDDFS OPERATIONS: " + str(self.IDDFS.getNOperations()) + "\n")

            # print("\n")

            # print("---GREEDY METRICS---\n")
            # print("GREEDY TIME: " + str(self.GREEDY.getSolveTime()) + "\n")
            # print("GREEDY MEMORY USAGE: " + str(self.GREEDY.getMaxMemory()) + "\n")
            # print("GREEDY OPERATIONS: " + str(self.GREEDY.getNOperations()) + "\n")

            # print("\n")

            # print("---A* METRICS---\n")
            # print("A* TIME: " + str(self.ASTAR.getSolveTime()) + "\n")
            # print("A* MEMORY USAGE: " + str(self.ASTAR.getMaxMemory()) + "\n")
            # print("A* OPERATIONS: " + str(self.ASTAR.getNOperations()) + "\n")

            # print("\n")

            # print("---WEIGHTEDASTAR METRICS---\n")
            # print("WEIGHTED A* TIME: " + str(self.WEIGHTEDASTAR.getSolveTime()) + "\n")
            # print("WEIGHTED A* MEMORY USAGE: " + str(self.WEIGHTEDASTAR.getMaxMemory()) + "\n")
            # print("WEIGHTED A* OPERATIONS: " + str(self.WEIGHTEDASTAR.getNOperations()) + "\n")

            # print("\n")

            # print("***END OF METRICS TEST FOR LEVEL " + i + " ***\n")

        return bfsMetrics, dfsMetrics

    def bfsTest(self):
        expectedSolution = []

        calculatedSolution = self.BFS.algorithm(map)

        if expectedSolution == calculatedSolution:
            print("BFS TEST PASSED\n")
        else:
            print("BFS TEST FAILED\n")
            print("Expected Solution: " + expectedSolution + "\n")
            print("Calculated Solution: " + calculatedSolution + "\n")

        return None

    def dfsTest(self):
        expectedSolution = []

        calculatedSolution = self.DFS.algorithm(map)

        if expectedSolution == calculatedSolution:
            print("DFS TEST PASSED\n")
        else:
            print("DFS TEST FAILED\n")
            print("Expected Solution: " + expectedSolution + "\n")
            print("Calculated Solution: " + calculatedSolution + "\n")

        return None
    
    def iddfsTest(self):
        expectedSolution = []

        calculatedSolution = self.IDDFS.algorithm(map)

        if expectedSolution == calculatedSolution:
            print("IDDFS TEST PASSED\n")
        else:
            print("IDDFS TEST FAILED\n")
            print("Expected Solution: " + expectedSolution + "\n")
            print("Calculated Solution: " + calculatedSolution + "\n")

        return None

    def greedyTest(self):
        expectedSolution = []

        calculatedSolution = self.GREEDY.algorithm(map)

        if expectedSolution == calculatedSolution:
            print("GREEDY TEST PASSED\n")
        else:
            print("GREEDY TEST FAILED\n")
            print("Expected Solution: " + expectedSolution + "\n")
            print("Calculated Solution: " + calculatedSolution + "\n")

        return None
    
    def astarTest(self):
        expectedSolution = []

        calculatedSolution = self.ASTAR.algorithm(map)

        if expectedSolution == calculatedSolution:
            print("A* TEST PASSED\n")
        else:
            print("A* TEST FAILED\n")
            print("Expected Solution: " + expectedSolution + "\n")
            print("Calculated Solution: " + calculatedSolution + "\n")

        return None
    
    def weightedAstarTest(self):

        expectedSolution = []

        calculatedSolution = self.WEIGHTEDASTAR.algorithm(map)

        if expectedSolution == calculatedSolution:
            print("WEIGHTED A* TEST PASSED\n")
        else:
            print("WEIGHTED A* TEST FAILED\n")
            print("Expected Solution: " + expectedSolution + "\n")
            print("Calculated Solution: " + calculatedSolution + "\n")

        return None
    
def main():

    test = TestSuite()

    bfsMetrics, dfsMetrics = test.testMetrics()

    levels = [1, 2, 3, 4]

    figure, axis = plt.subplots(1, 3)

    axis[0].set_title("Solve Time")
    axis[1].set_title("Max Memory Usage")
    axis[2].set_title("Number of Operations")

    # /// TIME GRAPH PLOT FOR ALL ALGORITHMS FOR 5 LEVELS ///

    bfs_time_values = bfsMetrics["solveTime"]
    dfs_time_values = dfsMetrics["solveTime"]
    # iddfs_time_values = dfsMetrics["solveTime"]
    # greedy_time_values = greedyMetrics["solveTime"]
    # astar_time_values = astarMetrics["solveTime"]
    # wAstar_time_values = wAstarMetrics["solveTime"]

    axis[0].plot(levels, bfs_time_values)
    # plt.plot(levels, dfs_time_values)
    # plt.plot(levels, iddfs_time_values)
    # plt.plot(levels, greedy_time_values)
    # plt.plot(levels, astar_time_values)
    # plt.plot(levels, wAstar_time_values)

    # /// MAX MEMORY GRAPH PLOT FOR ALL ALGORITHMS FOR 5 LEVELS ///

    bfs_mem_values = bfsMetrics["maxMemory"]
    # dfs_mem_values = dfsMetrics["maxMemory"]
    # iddfs_mem_values = dfsMetrics["maxMemory"]
    # greedy_mem_values = greedyMetrics["maxMemory"]
    # astar_mem_values = astarMetrics["maxMemory"]
    # wAstar_mem_values = wAstarMetrics["maxMemory"]

    axis[1].plot(levels, bfs_mem_values)


    # /// NUMBER OF OPERATIONS GRAPH PLOT FOR ALL ALGORITHMS FOR 5 LEVELS ///

    bfs_op_values = bfsMetrics["nOperations"]
    # dfs_op_values = dfsMetrics["nOperations"]
    # iddfs_op_values = dfsMetrics["nOperations"]
    # greedy_op_values = greedyMetrics["nOperations"]
    # astar_op_values = astarMetrics["nOperations"]
    # wAstar_op_values = wAstarMetrics["nOperations"]

    axis[2].plot(levels, bfs_op_values)

    plt.show()

    return None

if __name__ == "__main__":
    main()

