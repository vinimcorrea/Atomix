import heapq
import math
from queue import PriorityQueue
from collections import deque
import time
import tracemalloc
from atomix_state import AtomixState

def shortest_path(board, start, end):
    rows = len(board)
    columns = len(board[0])
    visited = [[False for _ in range(columns)] for _ in range(rows)]
    queue = deque([(start, 0)])  # (coordinates, path_length)
    visited[start[0]][start[1]] = True

    while queue:
        current, path_length = queue.popleft()

        if current == end:
            return path_length

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = current[0] + dr, current[1] + dc

            if (0 <= nr < rows) and (0 <= nc < columns) and not visited[nr][nc] and board[nr][nc] != '#':
                visited[nr][nc] = True
                queue.append(((nr, nc), path_length + 1))

    return float('inf')

def get_closest_bonded_atom(atom, molecule):
        closest_distance = float('inf')
        closest_bonded_atom = None
        atom_x, atom_y = molecule['atoms'][atom]
        for bond in molecule['bonds']:
            if atom in bond:
                other_atom = bond[0] if bond[1] == atom else bond[1]
                other_x, other_y = molecule['atoms'][other_atom]
                distance = math.sqrt((atom_x - other_x) ** 2 + (atom_y - other_y) ** 2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_bonded_atom = other_atom
        return closest_bonded_atom

def openness(state):
    # calculate the "openness" of the state
    # as the number of atoms that can be connected to the existing bonds
    molecule = state.atomic_structure
    open_atoms = 0
    for atom in molecule['atoms']:
        can_connect = False
        for bond in molecule['current_bonds']:
            if atom in bond:
                other_atom = bond[0] if bond[1] == atom else bond[1]
                if other_atom in molecule['atoms']:
                    distance = shortest_path(state.board, molecule['atoms'][atom], molecule['atoms'][other_atom])
                    required_distance = abs(state.molecule.index(atom) - state.molecule.index(other_atom)) - 1
                    if distance == required_distance:
                        can_connect = True
                        break
        if can_connect:
            open_atoms += 1
    return open_atoms

def distance(state):
    atoms = state.atomic_structure['atoms']
    target_bonds = state.atomic_structure['target_bonds']
    total_distance = 0
    for bond in target_bonds:
        atom1, atom2 = bond
        total_distance += shortest_path(state.board, atoms[atom1], atoms[atom2])
    return total_distance

def pairwise_distance(state):
    atoms = state.atomic_structure['atoms']
    target_bonds = state.atomic_structure['target_bonds']
    total_distance = 0
    for bond in target_bonds:
        atom1, atom2 = bond
        distance = shortest_path(state.board, atoms[atom1], atoms[atom2])
        print(state.molecule)
        print(type(atom1))
        required_distance = abs(state.molecule.index(atom1.strip()) - state.molecule.index(atom2.strip())) - 1
        total_distance += abs(distance - required_distance)
    return total_distance

def heuristic(state):
    """Calculate the heuristic value of a molecule."""
    unbonded_pairs_distance = 0
    atoms = state.atomic_structure['atoms']
    current_bonds = set(state.atomic_structure['current_bonds'])
    target_bonds = set(state.atomic_structure['target_bonds'])
    missing_bonds = target_bonds - current_bonds

    for bond in missing_bonds:
        atom1, atom2 = bond
        unbonded_pairs_distance += shortest_path(state.board, atoms[atom1], atoms[atom2])

    return distance(state) + openness(state) + unbonded_pairs_distance + pairwise_distance(state)

class Algorithm:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.nOperations = 0
        self.maxMemory = 0
        self.solveTime = 0
        self.nMoves = 0
    
    def getNOperations(self):
        return self.nOperations
    
    def getMaxMemory(self):
        return self.maxMemory

    def getSolveTime(self):
        return self.solveTime
    
    def getNMoves(self):
        return self.nMoves

class BFS(Algorithm):
    def __init__(self):
        super().__init__()

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory()

    def getSolveTime(self):
        return super().getSolveTime()
    
    def getNMoves(self):
        return super().getNMoves()
    
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
                self.nMoves = len(node.move_history)
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
    
    def getNMoves(self):
        return super().getNMoves()
    
    def algorithm(self, state):
        start = time.time()
        tracemalloc.start()
        stack = [(state, start)]
        visited = set()

        while stack:
            node, node_start = stack.pop()
            self.nOperations += 1

            if node.is_molecule_formed():
                end = time.time()
                self.getSolveTime = end - start
                self.maxMemory = tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
                self.nMoves = len(node.move_history)
                return node.move_history


            for child in node.children():
                if child.board not in node.move_history:
                    stack.append((child, node_start))

        return None

class IDDFS(Algorithm):
    def __init__(self):
        super().__init__()

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime
    
    def getNMoves(self):
        return super().getNMoves()

    def algorithm(self, node, maxDepth):

        start = time.time()
        tracemalloc.start()

        for depth in range(maxDepth + 1):
            stack = [(node, 0)]
            while stack:
                self.nOperations += 1
                current, currentDepth = stack.pop()
                if currentDepth > depth:
                    continue
                if current.is_molecule_formed():
                    end = time.time()
                    self.getSolveTime = end - start
                    self.maxMemory = tracemalloc.get_traced_memory()[1]
                    tracemalloc.stop()
                    self.nMoves = len(current.move_history)
                    return current.move_history
                if currentDepth < depth:
                    for child in current.children():
                        if child.board not in current.move_history:
                            stack.append((child, currentDepth + 1))
        return None

class GREEDY(Algorithm):
    def __init__(self):
        super().__init__()
    
    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime
    
    def getNMoves(self):
        return super().getNMoves()
    
    def algorithm(self, node):
        # problem (NPuzzleState) - the initial state
        # heuristic (function) - the heuristic function that takes a board (matrix), and returns an integer
        setattr(AtomixState, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
        states = [node]
        visited = set()  # to not visit the same state twice

        start = time.time()
        tracemalloc.start()


        while states:
            state = heapq.heappop(states)
            self.nOperations += 1

            if state.is_molecule_formed():
                end = time.time()
                self.getSolveTime = end - start
                self.maxMemory = tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
                self.nMoves = len(state.move_history)
                return state.move_history

            visited.add(state)

            for child in state.children():
                if child not in visited:
                    heapq.heappush(states, child)

        return None

class ASTAR(GREEDY):
    def __init__(self):
        super().__init__()

    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime
    
    def getNMoves(self):
        return super().getNMoves()

    def heuristic(state):
        return lambda: super().heuristic(state) + state.cost

    def algorithm(self, state):
        return super().algorithm(state, self.heuristic(state))

class WEIGHTEDASTAR(ASTAR):

    def __init__(self):
        super().__init__()
    
    def getNOperations(self):
        return super().getNOperations()
    
    def getMaxMemory(self):
        return super().getMaxMemory

    def getSolveTime(self):
        return super().getSolveTime
    
    def getNMoves(self):
        return super().getNMoves()

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
    
    def getNMoves(self):
        return super().getNMoves()
    
    def algorithm(self, node):
        def search(path, g, threshold):
            state = path[-1]
            f = g + heuristic(state)
            if f > threshold:
                return f
            if state.is_molecule_formed():
                end = time.time()
                self.getSolveTime = end - start
                self.maxMemory = tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
                self.nMoves = len(state.move_history)
                return state.move_history
            min_threshold = float('inf')
            for child in state.children():
                if child not in path:
                    path.append(child)
                    t = search(path, g + 1, threshold)
                    if t is None:
                        return None
                    if t < min_threshold:
                        min_threshold = t
                    path.pop()
            return min_threshold

        threshold = heuristic(node)
        path = [node]

        start = time.time()
        tracemalloc.start()

        while True:
            self.nOperations += 1
            t = search(path, 0, threshold)
            if t is None:
                return path[1:]
            threshold = t
    
