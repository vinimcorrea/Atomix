from collections import deque
import heapq


def depth_first_search(problem, depth_limit=50):
    visited = set()
    stack = [(problem, 0)]
    max_memory = 0
    num_operations = 0

    while stack:
        num_operations += 1
        max_memory = max(max_memory, len(stack))

        state, depth = stack.pop()

        if state.is_molecule_formed():
            return state.move_history, num_operations, max_memory

        visited.add(state)

        if depth_limit is not None and depth >= depth_limit:
            continue

        for child in state.children():
            if child not in visited:
                stack.append((child, depth + 1))

    return None, num_operations, max_memory


def breadth_first_search(problem):
    queue = deque([problem])
    visited = set()
    max_memory = 0
    num_operations = 0

    while queue:
        num_operations += 1
        max_memory = max(max_memory, len(queue))

        node = queue.popleft()
        visited.add(node)

        if node.is_molecule_formed():
            return node.move_history, num_operations, max_memory

        for child in node.children():
            if child not in visited:
                queue.append(child)

    return None, num_operations, max_memory


def iterative_deepening(problem):
    depth = 0
    max_memory = 0
    num_operations = 0

    while True:
        result, depth_num_operations, depth_max_memory = depth_first_search(problem, depth_limit=depth)
        num_operations += depth_num_operations
        max_memory = max(max_memory, depth_max_memory)

        if result is not None:
            return result, num_operations, max_memory
        depth += 1


def uniform_cost(problem):
    visited = set()
    tie_breaker = 0  # added a tie-breaker
    queue = [(0, tie_breaker, problem)]
    max_memory = 0
    num_operations = 0

    while queue:
        num_operations += 1
        max_memory = max(max_memory, len(queue))

        cost, _, state = heapq.heappop(queue)

        if state.is_molecule_formed():
            return state.move_history, num_operations, max_memory

        visited.add(state)

        for child in state.children():
            if child not in visited:
                tie_breaker += 1  # increment the tie_breaker
                heapq.heappush(queue, (cost + 1, tie_breaker, child))

    return None, num_operations, max_memory







