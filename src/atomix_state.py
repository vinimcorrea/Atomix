from copy import deepcopy

BLANK_SPACE = '.'


class AtomixState:
    def __init__(self, board, molecule, atom_map, molecule_name_phase, move_history=[], cost=0):
        # board(list[list[int]]) - the state of the board
        # move_history(list[list[list[int]]]) - the history of the moves up until this state
        self.board = deepcopy(board)
        self.atom_map = atom_map
        self.molecule = deepcopy(molecule)
        self.molecule_name = molecule_name_phase
        self.board_width = len(board[0])
        self.game_won = False
        self.cost = cost
        self.atomic_structure = self.find_atoms(molecule)

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

    def target_bonds(self, molecule_struc):
        target_bonds = []
        for index, atom_num in enumerate(molecule_struc[0]):
            atom_info = self.atom_map[int(atom_num)]
            atom_bond = [atom_num]
            for connection in atom_info['connections']:
                if connection == 'R' and index + 1 < len(molecule_struc[0]):
                    atom_bond.append(molecule_struc[0][index + 1])
                elif connection == 'L' and index - 1 >= 0:
                    atom_bond.append(molecule_struc[0][index - 1])
            self.target_bonds.append(tuple(atom_bond))

    def find_atoms(self, molecule_struc):
        molecule = {}
        atoms = {}
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != '.' and self.board[row][col] != '#':
                    atoms[self.board[row][col]] = (row, col)

        target_bonds = set()
        directions = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1),
            "UR": (-1, 1),
            "DR": (1, 1),
            "UL": (-1, -1),
            "DL": (1, -1)
        }

        for row in range(len(molecule_struc)):
            for col in range(len(molecule_struc[0])):
                atom_num = molecule_struc[row][col]
                if atom_num != '.':
                    atom_info = self.atom_map[int(atom_num)]
                    for connection_str in atom_info['connections']:
                        connection = connection_str[-1]
                        dr, dc = directions[connection]
                        new_row = row + dr
                        new_col = col + dc
                        if 0 <= new_row < len(molecule_struc) and 0 <= new_col < len(molecule_struc[0]):
                            adjacent_atom = molecule_struc[new_row][new_col]
                            if adjacent_atom != '.':
                                if connection in ['L', 'U']:
                                    bond = (adjacent_atom, atom_num)
                                elif connection in ['R', 'D']:
                                    bond = (atom_num, adjacent_atom)
                                target_bonds.add(bond)

        current_bonds = set()
        for atom_num, (atom_position_x, atom_position_y) in atoms.items():
            atom_info = self.atom_map[int(atom_num)]
            for connection_str in atom_info['connections']:
                connection = connection_str[-1]
                dr, dc = directions[connection]
                atom_bond = None  # Add this line to initialize atom_bond
                if 0 <= atom_position_x + dr < len(self.board) and 0 <= atom_position_y + dc < len(self.board[0]):
                    atom_bond = (self.board[atom_position_x][atom_position_y],
                                 self.board[atom_position_x + dr][atom_position_y + dc])
                if atom_bond is not None:
                    current_bonds.add(atom_bond)

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

        directions = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1),
            "UR": (-1, 1),
            "DR": (1, 1),
            "UL": (-1, -1),
            "DL": (1, -1)
        }

        current_bonds = set()
        for atom_num, (atom_position_x, atom_position_y) in self.atomic_structure['atoms'].items():
            atom_info = self.atom_map[int(atom_num)]
            for connection, (dr, dc) in directions.items():
                if connection in atom_info['connections']:
                    new_row = atom_position_x + dr
                    new_col = atom_position_y + dc
                    if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                        adjacent_cell = self.board[new_row][new_col]
                        atom_bond = None
                        if connection in ['L', 'U']:
                            atom_bond = (adjacent_cell, atom_num)
                        elif connection in ['R', 'D']:
                            atom_bond = (atom_num, adjacent_cell)
                        if atom_bond not in current_bonds:
                            current_bonds.add(atom_bond)

        self.atomic_structure["current_bonds"] = current_bonds

    def is_molecule_formed(self):
        return self.atomic_structure['target_bonds'] == self.atomic_structure['current_bonds']

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
