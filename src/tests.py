from algortihms import *

class TestSuite:
    def __init__(self) -> None:
        self.BFS = BFS(0,0,0)
        self.DFS = DFS(0,0,0)
        self.IDDFS = IDDFS(0,0,0)
        self.GREEDY = GREEDY(0,0,0)
        self.ASTAR = ASTAR(0,0,0)
        self.WEIGHTEDASTAR = WEIGHTEDASTAR(0,0,0)

    def loadMap(level):
        return None

    def testMetrics(self):

        for i in range(1,5):

            map = self.loadMap("level"+i)

            self.BFS.algorithm(map)
            self.DFS.algorithm(map)
            self.IDDFS.algorithm(map)
            self.GREEDY.algorithm(map)
            self.ASTAR.algorithm(map)
            self.WEIGHTEDASTAR.algorithm(map)

            print("\n")
            print("\n")

            print("***TESTING METRICS FOR LEVEL " + i + " ***\n")

            print("\n")

            print("---BFS METRICS---\n")
            print("BFS TIME: " + self.BFS.getSolveTime + "\n")
            print("BFS MEMORY USAGE: " + self.BFS.getMaxMemory + "\n")
            print("BFS OPERATIONS: " + self.BFS.getNOperations + "\n")

            print("\n")

            print("---DFS METRICS---\n")
            print("DFS TIME: " + self.DFS.getSolveTime + "\n")
            print("DFS MEMORY USAGE: " + self.DFS.getMaxMemory + "\n")
            print("DFS OPERATIONS: " + self.DFS.getNOperations + "\n")

            print("\n")

            print("---IDDFS METRICS---\n")
            print("IDDFS TIME: " + self.IDDFS.getSolveTime + "\n")
            print("IDDFS MEMORY USAGE: " + self.IDDFS.getMaxMemory + "\n")
            print("IDDFS OPERATIONS: " + self.IDDFS.getNOperations + "\n")

            print("\n")

            print("---GREEDY METRICS---\n")
            print("GREEDY TIME: " + self.GREEDY.getSolveTime + "\n")
            print("GREEDY MEMORY USAGE: " + self.GREEDY.getMaxMemory + "\n")
            print("GREEDY OPERATIONS: " + self.GREEDY.getNOperations + "\n")

            print("\n")

            print("---A* METRICS---\n")
            print("A* TIME: " + self.ASTAR.getSolveTime + "\n")
            print("A* MEMORY USAGE: " + self.ASTAR.getMaxMemory + "\n")
            print("A* OPERATIONS: " + self.ASTAR.getNOperations + "\n")

            print("\n")

            print("---WEIGHTEDASTAR METRICS---\n")
            print("WEIGHTED A* TIME: " + self.WEIGHTEDASTAR.getSolveTime + "\n")
            print("WEIGHTED A* MEMORY USAGE: " + self.WEIGHTEDASTAR.getMaxMemory + "\n")
            print("WEIGHTED A* OPERATIONS: " + self.WEIGHTEDASTAR.getNOperations + "\n")

            print("\n")

            print("***END OF METRICS TEST FOR LEVEL " + i + " ***\n")

        return None


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