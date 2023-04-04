from atomix_state import AtomixState
import heapq

def greedy_search(problem, heuristic):
    setattr(AtomixState, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
    states = [problem]
    visited = set()
    max_memory = 0
    num_operations = 0

    while states:
        num_operations += 1
        max_memory = max(max_memory, len(states))

        state = heapq.heappop(states)

        if state.is_molecule_formed():
            return state.move_history, num_operations, max_memory

        visited.add(state)

        for child in state.children():
            if child not in visited:
                heapq.heappush(states, child)

    return None, num_operations, max_memory


def a_star_search(problem, heuristic):
    setattr(AtomixState, "__lt__", lambda self, other: heuristic(self) + self.cost < heuristic(other) + other.cost)
    states = [(0, problem)]
    visited = set()
    max_memory = 0
    num_operations = 0

    while states:
        num_operations += 1
        max_memory = max(max_memory, len(states))

        _, state = heapq.heappop(states)

        if state.is_molecule_formed():
            return state.move_history, num_operations, max_memory

        visited.add(state)

        for child in state.children():
            if child not in visited:
                heapq.heappush(states, (heuristic(child) + child.cost, child))

    return None, num_operations, max_memory


def weighted_a_star_search(problem, heuristic, weight=1):
    visited = set()
    tie_breaker = 0  # added a tie-breaker
    queue = [(heuristic(problem) * weight, 0, tie_breaker, problem)]
    max_memory = 0
    num_operations = 0

    while queue:
        num_operations += 1
        max_memory = max(max_memory, len(queue))

        heuristic_value, cost, _, state = heapq.heappop(queue)

        if state.is_molecule_formed():
            return state.move_history, num_operations, max_memory

        visited.add(state)

        for child in state.children():
            if child not in visited:
                tie_breaker += 1  # increment the tie_breaker
                heapq.heappush(queue, (heuristic(child) * weight + len(child.move_history), cost + 1, tie_breaker, child))

    return None, num_operations, max_memory


