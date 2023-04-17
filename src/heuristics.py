from collections import deque
import math


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

def pairwise_distance(state):
    atoms = state.atomic_structure['atoms']
    target_bonds = state.atomic_structure['target_bonds']
    total_distance = 0
    for bond in target_bonds:
        atom1, atom2 = bond
        distance = shortest_path(state.board, atoms[atom1], atoms[atom2])

        # Find the indices of the atoms in the molecule
        atom1_index = sum([row.index(atom1) for row in state.molecule if atom1 in row])
        atom2_index = sum([row.index(atom2) for row in state.molecule if atom2 in row])

        required_distance = abs(atom1_index - atom2_index) - 1
        total_distance += abs(distance - required_distance)
    return total_distance


def distance(state):
    atoms = state.atomic_structure['atoms']
    target_bonds = state.atomic_structure['target_bonds']
    total_distance = 0
    for bond in target_bonds:
        atom1, atom2 = bond
        total_distance += shortest_path(state.board, atoms[atom1], atoms[atom2])
    return total_distance


def openness(state):
    # Calculate the "openness" of the state
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

                    # Find the indices of the atoms in the molecule
                    atom_index = sum([row.index(atom) for row in state.molecule if atom in row])
                    other_atom_index = sum([row.index(other_atom) for row in state.molecule if other_atom in row])

                    required_distance = abs(atom_index - other_atom_index) - 1
                    if distance == required_distance:
                        can_connect = True
                        break
        if can_connect:
            open_atoms += 1
    return open_atoms


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


def heuristic(state, weight_distance=1, weight_openness=1, weight_unbonded_pairs_distance=4, weight_pairwise_distance=1):
    """Calculate the heuristic value of a molecule."""
    unbonded_pairs_distance = 0
    atoms = state.atomic_structure['atoms']
    current_bonds = set(state.atomic_structure['current_bonds'])
    target_bonds = set(state.atomic_structure['target_bonds'])
    missing_bonds = target_bonds - current_bonds

    for bond in missing_bonds:
        atom1, atom2 = bond
        unbonded_pairs_distance += shortest_path(state.board, atoms[atom1], atoms[atom2])

    return (weight_distance * distance(state) +
            weight_openness * openness(state) +
            weight_unbonded_pairs_distance * unbonded_pairs_distance +
            weight_pairwise_distance * pairwise_distance(state))

