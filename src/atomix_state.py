from copy import deepcopy
from collections import deque


BLANK_SPACE = '.'


class AtomixState:
    def __init__(self, board, molecule, atom_map, molecule_name_phase, move_history=[], cost=0):
        # board(list[list[int]]) - the state of the board
        # move_history(list[list[list[int]]]) - the history of the moves up until this state
        self.board = deepcopy(board)
        self.atomic_structure = self.find_atoms(molecule)
        self.molecule = deepcopy(molecule)
        self.atom_map = atom_map
        self.molecule_name = molecule_name_phase
        self.board_width = len(board[0])
        self.cost = cost

        # create an empty array and append move_history
        self.move_history = [] + move_history + [self.board]

    def children(self):
        # returns the possible moves
        functions = [self.up, self.down, self.left, self.right]

        # returns the possible atoms

        children = []
        for atom, (atom_pos_row, atom_pos_col) in self.atomic_structure['atoms'].items():
            for func in functions:
                child = func(atom, atom_pos_row, atom_pos_col)
                if child:
                    child.update_bonds(atom)
                    children.append(child)

        return children

    def find_atoms(self, molecule_struc):
        # finds the atoms and their positions
        molecule = {}
        atoms = {}
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != '.' and self.board[row][col] != '#':
                    atoms[self.board[row][col]] = (row, col)

        target_bonds = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for row in range(len(molecule_struc)):
            for col in range(len(molecule_struc[0])):
                if molecule_struc[row][col] != '.':
                    atom1 = molecule_struc[row][col]
                    for dr, dc in directions:
                        new_row = row + dr
                        new_col = col + dc
                        if 0 <= new_row < len(molecule_struc) and 0 <= new_col < len(molecule_struc[0]):
                            atom2 = molecule_struc[new_row][new_col]
                            if atom2 != '.':
                                bond = (min(atom1, atom2), max(atom1, atom2))
                                if bond not in target_bonds:
                                    target_bonds.append(bond)

        current_bonds = []
        # Check adjacent atoms for existing bonds using Manhattan distance
        for atom, position in atoms.items():
            for other_atom, other_position in atoms.items():
                if atom != other_atom:
                    manhattan_distance = abs(position[0] - other_position[0]) + abs(position[1] - other_position[1])
                    if manhattan_distance == 1:
                        bond_pair = (atom, other_atom) if atom < other_atom else (other_atom, atom)
                        if bond_pair in target_bonds and bond_pair not in current_bonds:
                            current_bonds.append(bond_pair)

        molecule["atoms"] = atoms
        molecule["target_bonds"] = target_bonds
        molecule["current_bonds"] = current_bonds

        return molecule

    def move(func):
        # decorator function to add to history everytime a move is made
        # functions with @move will apply this decorator
        def wrapper(self, atom, atom_pos_row, atom_pos_col):
            state = AtomixState(self.board, self.molecule, self.atom_map, self.molecule_name, self.move_history, self.cost)
            value = func(state, atom, atom_pos_row, atom_pos_col)
            if value:
                return state
            else:
                return None

        return wrapper

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


    @move
    def up(self, atom, atom_pos_row, atom_pos_col):
        # moves the atom upwards
        prev = self.board[atom_pos_row - 1][atom_pos_col]

        if prev != BLANK_SPACE:
            return False

        while prev == BLANK_SPACE:
            board_row = ""

            for i in range(self.board_width):
                if i == atom_pos_col:
                    board_row += self.board[atom_pos_row][atom_pos_col]
                    continue
                board_row += self.board[atom_pos_row - 1][i]

            self.board[atom_pos_row - 1] = board_row
            board_row = ""

            for i in range(self.board_width):
                if i == atom_pos_col:
                    board_row += '.'
                    continue
                board_row += self.board[atom_pos_row][i]

            self.board[atom_pos_row] = board_row

            # updating the atom coordinates
            self.atomic_structure['atoms'][atom] = (atom_pos_row - 1, atom_pos_col)

            atom_pos_row, atom_pos_col = self.atomic_structure['atoms'][atom]

            prev = self.board[atom_pos_row - 1][atom_pos_col]

        self.cost += 1

        self.update_bonds(atom)

        return True

    @move
    def down(self, atom, atom_pos_row, atom_pos_col):
        # moves the atom downwards
        prev = self.board[atom_pos_row + 1][atom_pos_col]

        if prev != BLANK_SPACE:
            return False

        while prev == BLANK_SPACE:
            board_row = ""

            for i in range(self.board_width):
                if i == atom_pos_col:
                    board_row += self.board[atom_pos_row][atom_pos_col]
                    continue
                board_row += self.board[atom_pos_row + 1][i]

            self.board[atom_pos_row + 1] = board_row
            board_row = ""

            for i in range(self.board_width):
                if i == atom_pos_col:
                    board_row += '.'
                    continue
                board_row += self.board[atom_pos_row][i]

            self.board[atom_pos_row] = board_row

            # updating the atom coordinates
            self.atomic_structure['atoms'][atom] = (atom_pos_row + 1, atom_pos_col)

            atom_pos_row, atom_pos_col = self.atomic_structure['atoms'][atom]

            prev = self.board[atom_pos_row + 1][atom_pos_col]

        self.cost += 1

        self.update_bonds(atom)

        return True


    @move
    def left(self, atom, atom_pos_row, atom_pos_col):
        # moves the atom leftwards
        prev = self.board[atom_pos_row][atom_pos_col - 1]

        if prev != BLANK_SPACE:
            return False

        while prev == BLANK_SPACE:
            board_row = ""

            for i in range(self.board_width):
                if i == atom_pos_col - 1:
                    board_row += self.board[atom_pos_row][atom_pos_col]
                    continue
                elif i == atom_pos_col:
                    board_row += '.'
                    continue
                board_row += self.board[atom_pos_row][i]

            self.board[atom_pos_row] = board_row

            # updating the atom coordinates
            self.atomic_structure['atoms'][atom] = (atom_pos_row, atom_pos_col - 1)

            atom_pos_row, atom_pos_col = self.atomic_structure['atoms'][atom]

            prev = self.board[atom_pos_row][atom_pos_col - 1]

        self.cost += 1

        self.update_bonds(atom)

        return True

    @move
    def right(self, atom, atom_pos_row, atom_pos_col):
        # moves the atom rightwards
        prev = self.board[atom_pos_row][atom_pos_col + 1]

        if prev != BLANK_SPACE:
            return False

        while prev == BLANK_SPACE:
            board_row = ""

            for i in range(self.board_width):
                if i == atom_pos_col + 1:
                    board_row += self.board[atom_pos_row][atom_pos_col]
                    continue
                elif i == atom_pos_col:
                    board_row += '.'
                    continue
                board_row += self.board[atom_pos_row][i]

            self.board[atom_pos_row] = board_row

            # updating the atom coordinates
            self.atomic_structure['atoms'][atom] = (atom_pos_row, atom_pos_col + 1)

            atom_pos_row, atom_pos_col = self.atomic_structure['atoms'][atom]

            prev = self.board[atom_pos_row][atom_pos_col + 1]

        self.cost += 1

        self.update_bonds(atom)

        return True

    def update_bonds(self, atom_moved):
        atoms = self.atomic_structure['atoms']
        moved_atom_position = atoms[atom_moved]
        target_bonds = self.atomic_structure['target_bonds']
        current_bonds = self.atomic_structure['current_bonds']

        for atom, position in atoms.items():
            if atom != atom_moved:
                row_diff = abs(moved_atom_position[0] - position[0])
                col_diff = abs(moved_atom_position[1] - position[1])

                # Check if the atoms are adjacent
                if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1):
                    bond_pair = (atom_moved, atom) if atom_moved < atom else (atom, atom_moved)
                    if bond_pair not in current_bonds:
                        if bond_pair in target_bonds:
                                current_bonds.append(bond_pair)

    def is_molecule_formed(self):
        return self.atomic_structure["current_bonds"] == self.atomic_structure["target_bonds"]

    # Add this method to the GameState class:
    def move_cursor(self, cursor_position, move_direction, cell_size, board_y_offset, board_x_offset):
        x, y = cursor_position
        dx, dy = move_direction
        new_x = max(board_x_offset, min(board_x_offset + (self.board_width - 1) * cell_size, x + dx * cell_size))
        new_y = max(board_y_offset, min(board_y_offset + (self.board_width - 1) * cell_size, y + dy * cell_size))

        return new_x, new_y

    def get_atom_at(self, position, cell_size, board_y_offset, board_x_offset):
        x, y = position
        row = (y - board_y_offset) // cell_size
        col = (x - board_x_offset) // cell_size

        if 0 <= row < len(self.board) and 0 <= col < len(self.board[0]):
            if self.board[row][col] != "." and self.board[row][col] != "#":
                return self.board[row][col]
        return None

    def __hash__(self):
        # to be able to use the state in a set
        return hash(str([item for sublist in self.board for item in sublist]))

    def __eq__(self, other):
        # compares the two matrices
        return [item for sublist in self.board for item in sublist] == [item for sublist in other.board for item in
                                                                        sublist]
