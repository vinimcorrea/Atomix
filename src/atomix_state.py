from copy import deepcopy

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
        self.game_won = False
        self.cost = cost

        # create an empty array and append move_history
        self.move_history = [] + move_history + [self]

    def children(self):
        # returns the possible moves
        functions = [self.up, self.down, self.left, self.right]

        # returns the possible atoms

        children = []
        for atom, (atom_pos_row, atom_pos_col) in self.atomic_structure['atoms'].items():
            for func in functions:
                child = func(atom, atom_pos_row, atom_pos_col)
                if child:
                    child.update_bonds()
                    children.append(child)

        return children

    def goal_positions(self):
        goal_positions = {}
        for row_idx, row in enumerate(self.molecule):
            for col_idx, atom in enumerate(row):
                if atom != '.':
                    goal_positions[atom] = (row_idx, col_idx)
        return goal_positions

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
            state = AtomixState(self.board, self.molecule, self.atom_map,
                                self.molecule_name, self.move_history, self.cost)
            value = func(state, atom, atom_pos_row, atom_pos_col)
            if value:
                return state
            else:
                return None

        return wrapper

    @move
    def up(self, atom, atom_pos_row, atom_pos_col):
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

        self.update_bonds()

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

        self.update_bonds()

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

        self.update_bonds()

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

        self.update_bonds()

        return True

    def update_bonds(self):
        new_bonds = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for atom, position in self.atomic_structure["atoms"].items():
            for dr, dc in directions:
                new_row = position[0] + dr
                new_col = position[1] + dc
                if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                    other_atom = self.board[new_row][new_col]
                    if other_atom != '.' and other_atom != '#':
                        bond_pair = (atom, other_atom) if atom < other_atom else (other_atom, atom)
                        if bond_pair in self.atomic_structure["target_bonds"] and bond_pair not in new_bonds:
                            new_bonds.append(bond_pair)

        self.atomic_structure["current_bonds"] = new_bonds

    def is_molecule_formed(self):
        atoms = self.atomic_structure['atoms']
        target_bonds = self.atomic_structure['target_bonds']

        # Check if all required bonds are formed
        if set(target_bonds) != set(self.atomic_structure['current_bonds']):
            return False

        # Check if the atoms are in the correct order and in the same row
        atom_positions = [atoms[atom] for atom in sorted(atoms.keys())]
        same_row = all(atom_positions[i][0] == atom_positions[i + 1][0] for i in range(len(atom_positions) - 1))

        # Check if the atoms form the correct substring of the board
        row = atom_positions[0][0]
        board_row = ''.join(self.board[row][col] for col in range(len(self.board[row])))
        if self.molecule[0] not in board_row:
            return False

        return True

    # Add this method to the GameState class:
    def move_cursor(self, cursor_position, move_direction, cell_size, board_y_offset, board_x_offset,
                    selected_atom_pos=None):
        x, y = cursor_position
        dx, dy = move_direction

        if selected_atom_pos is not None:
            # If an atom is selected, make the cursor follow the atom
            new_x, new_y = selected_atom_pos[1] * cell_size + board_x_offset, selected_atom_pos[
                0] * cell_size + board_y_offset
        else:
            # If no atom is selected, move the cursor as usual
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
