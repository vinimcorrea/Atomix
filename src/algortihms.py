from queue import PriorityQueue
from collections import deque
import time
import tracemalloc

class Algorithm:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.nOperations = 0
        self.maxMemory = 0
        self.solveTime = 0
    
    def getNOperations(self):
        return self.nOperations
    
    def getMaxMemory(self):
        return self.maxMemory

    def getSolveTime(self):
        return self.solveTime

class BFS(Algorithm):
    def __init__(self):
        super().__init__()

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory()

    def getSolveTime(self):
        return super().getSolveTime()
    
    def algorithm(self, state):

        start = time.time()
        queue = deque([state])
        visited = set()  # to not visit the same state twice

        tracemalloc.start()

        while queue:
            node = queue.popleft()
            visited.add(node)
            self.nOperations += 1

            if node.is_molecule_formed():
                end = time.time()
                self.solveTime = end - start
                self.maxMemory = tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
                return node.move_history

            for child in node.children():
                if child not in visited:
                    queue.append(child)

        return "No Solution Found"

class DFS(Algorithm):
    def __init__(self):
        super().__init__()

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime
    
    def dfsaux(self, state, start):

        self.nOperations += 1

        if state.is_molecule_formed():
            end = time.time()
            self.getSolveTime = end - start
            self.maxMemory = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            return state.move_history

        for child in state.children():
            if child.board not in state.move_history:
                result = self.dfsaux(child, start)
                if result:
                    return result

        return None

    def algorithm(self, state):

        start = time.time()
        tracemalloc.start()

        result = self.dfsaux(state, start)

        return result

class IDDFS(Algorithm):
    def __init__(self):
        super().__init__()

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
            return None

        for child in node.children:
            solution =  self.DLS(child, target, limit)
            if solution is not None:
                return solution
    
    def algorithm(self, node, target, maxDepth):

        for limit in maxDepth:
            solution =  self.DLS(node, target, limit) == True
            if solution is not None:
                return True
        return False   

class GREEDY(Algorithm):
    def __init__(self):
        super().__init__()
    
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

class ASTAR(Algorithm):
    def __init__(self):
        super().__init__()

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

        start = time.time()
        tracemalloc.start()

        queue = PriorityQueue()
        currentCost = {}
        cameFrom = {}

        currentCost[state] = 0
        cameFrom[state] = None

        queue.put(state, 0)

        while not queue.empty():
            currentNode = queue.get()
            self.nOperations += 1

            if currentNode.is_molecule_formed():
                end = time.time()
                self.solveTime = end - start
                self.maxMemory = tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
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

    def __init__(self):
        super().__init__()
    
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
    
class IDASTAR(Algorithm):
    def __init__(self):
        super().__init__()
    
    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime
    
    def algorithm(self):
        return None
    
