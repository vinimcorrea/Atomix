from queue import PriorityQueue
from collections import deque
import time

class Algorithm:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, nOperations, maxMemory, solveTime):
        self.nOperations = nOperations
        self.maxMemory = maxMemory
        self.solveTime = solveTime
    
    def getNOperations(self):
        return self.nOperations
    
    def getMaxMemory(self):
        return self.maxMemory

    def getSolveTime(self):
        return self.solveTime

class BFS(Algorithm):
    def __init__(self, nOperations, maxMemory, solveTime):
        super.__init__(nOperations, maxMemory, solveTime)

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime
    
    def algorithm(state):
        queue = deque([state])
        visited = set()  # to not visit the same state twice

        while queue:
            node = queue.popleft()
            visited.add(node)

            if node.is_molecule_formed():
                return node.move_history

            for child in node.children():
                if child not in visited:
                    queue.append(child)

        return None

class DFS(Algorithm):
    def __init__(self, nOperations, maxMemory, solveTime):
        super.__init__(nOperations, maxMemory, solveTime)

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime

    def algorithm(self, state):

        if state.is_molecule_formed():
            return state.move_history

        for child in state.children:
            if child not in state.move_history:
                return self.dfs(child)

        return "No Solution Found"

class IDDFS(Algorithm):
    def __init__(self, nOperations, maxMemory, solveTime):
        super.__init__(nOperations, maxMemory, solveTime)

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime

    def DLS(self, node, target, limit):
        if node.is_molecule_formed():
            return node.move_history

        if (limit <= 0):
            return False

        for child in node.children:
            if self.DLS(child, target, limit):
                return True
    
    def algorithm(self, node, target, maxDepth):
        for limit in maxDepth:
            if self.DLS(node, target, limit) == True:
                return True
        return False   

    def __init__(self, nOperations, maxMemory, solveTime):
        super.__init__(nOperations, maxMemory, solveTime)

    def algorithm():
        return None

class GREEDY(Algorithm):
    def __init__(self, nOperations, maxMemory, solveTime):
        super.__init__(nOperations, maxMemory, solveTime)
    
    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime

    def heuristic(state):
        # Calculate the Manhattan distance between each atom and the nearest goal position
        dist = 0
        for i, row in enumerate(state):
            for j, val in enumerate(row):
                if val == 'H':
                    dist += min(abs(i - 1) + abs(j - 4), abs(i - 4) + abs(j - 1)) # Nearest goal position of H
                elif val == 'O':
                    dist += min(abs(i - 2) + abs(j - 3), abs(i - 3) + abs(j - 2)) # Nearest goal position of O
                elif val == 'N':
                    dist += min(abs(i - 3) + abs(j - 2), abs(i - 2) + abs(j - 3)) # Nearest goal position of N
                elif val == 'C':
                    dist += min(abs(i - 4) + abs(j - 1), abs(i - 1) + abs(j - 4)) # Nearest goal position of C
        return dist

    def algorithm():

        return None

class ASTAR(Algorithm):
    def __init__(self, nOperations, maxMemory, solveTime):
        super.__init__(nOperations, maxMemory, solveTime)

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime

    def heuristic(state):
        dist = 0
        # numbers 1-4 are placeholders for now, they should be the target coordinates for each atom 
        for i, row in enumerate(state):
            for j, val in enumerate(row):
                if val == 'H':
                    dist += abs(i - 1) + abs(j - 4) # Goal position of H
                elif val == 'O':
                    dist += abs(i - 2) + abs(j - 3) # Goal position of O
                elif val == 'N':
                    dist += abs(i - 3) + abs(j - 2) # Goal position of N
                elif val == 'C':
                    dist += abs(i - 4) + abs(j - 1) # Goal position of C
        return dist

    def algorithm(self, state):

        queue = PriorityQueue()
        currentCost = {}
        cameFrom = {}

        currentCost[state] = 0
        cameFrom[state] = None

        queue.put(state, 0)

        while not queue.empty():
            currentNode = queue.get()

            if currentNode.is_molecule_formed():
                return state.move_history

            for child in currentNode.children:
                childCost = currentCost[currentNode] + 1

                if child not in currentCost or childCost < currentCost[child]:
                    currentCost[child] = childCost
                    priority = childCost + self.heuristic(child)
                    queue.put(child, priority)
                    cameFrom[child] = currentNode

        return "Wasn't able to find a solution"

class WEIGHTEDASTAR(ASTAR):
    def __init__(self, nOperations, maxMemory, solveTime):
        super.__init__(nOperations, maxMemory, solveTime)
    
    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime

    def heuristic(state, weightFactor):
      
        return super().heuristic(state) * weightFactor # Multiply the heuristic cost by a weight factor

    def algorithm(state):
        return super().algorithm(state)