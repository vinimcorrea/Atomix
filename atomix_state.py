from copy import deepcopy


class AtomixState:
    def __init__(self, board, molecule, atom_connections, move_history=[]):
        # board(list[list[int]]) - the state of the board
        # move_history(list[list[list[int]]]) - the history of the moves up until this state
        self.board = deepcopy(board)
        self.atoms = self.find_atoms()
        self.molecule = deepcopy(molecule)
        self.atoms_connections = deepcopy(atom_connections)

        # create an empty array and append move_history
        self.move_history = [] + move_history + [self.board]

    def children(self):
        # returns the possible moves
        functions = [self.up, self.down, self.left, self.right]

        children = []
        for func in functions:
            child = func()
            if child:
                children.append(child)

        return children

    def find_atoms(self):
        # finds the atoms and their positions
        atoms = {}
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != '.' and self.board[row][col] != '#':
                    atoms[self.board[row][col]] = (row, col)
        return atoms

    def move(func):
        # decorator function to add to history everytime a move is made
        # functions with @move will apply this decorator
        def wrapper(self):
            state = AtomixState(self.board, self.move_history)
            value = func(state)
            if value:
                return state
            else:
                return None

        return wrapper

    @move
    def up(self):
        # moves the atom upwards
        prev = self.board[self.blank_row - 1][self.blank_col]

        if prev == '#' or prev.isdigit():
            return False

        self.board[self.blank_row][self.blank_col] = self.board[self.blank_row - 1][self.blank_col]
        self.board[self.blank_row - 1][self.blank_col] = '.'
        self.blank_row -= 1
        return True

    @move
    def down(self):
        # moves the atom downwards
        prev = self.board[self.blank_row + 1][self.blank_col]

        if prev == '#' or prev.isdigit():
            return False

        self.board[self.blank_row][self.blank_col] = self.board[self.blank_row + 1][self.blank_col]
        self.board[self.blank_row + 1][self.blank_col] = '.'
        self.blank_row += 1
        return True

    @move
    def left(self):
        # moves the atom leftwards
        prev = self.board[self.blank_row][self.blank_col - 1]

        if prev == '#' or prev.isdigit():
            return False

        self.board[self.blank_row][self.blank_col] = self.board[self.blank_row][self.blank_col - 1]
        self.board[self.blank_row][self.blank_col - 1] = '.'
        self.blank_col -= 1
        return True

    @move
    def right(self):
        # moves the atom rightwards
        prev = self.board[self.blank_row][self.blank_col + 1]

        if prev == '#' or prev.isdigit():
            return False

        self.board[self.blank_row][self.blank_col] = self.board[self.blank_row][self.blank_col + 1]
        self.board[self.blank_row][self.blank_col + 1] = '.'
        self.blank_col += 1
        return True

    def is_molecule_formed(self):
        molecule = ''.join(self.molecule)
        molecule_rows = molecule.split('\n')
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if i + len(molecule_rows) > len(self.board) or j + len(molecule_rows[0]) > len(self.board[0]):
                    continue
                is_match = True
                for k in range(len(molecule_rows)):
                    for l in range(len(molecule_rows[0])):
                        if molecule_rows[k][l] == '#':
                            continue
                        if molecule_rows[k][l] != '.' and molecule_rows[k][l] != self.board[i + k][j + l]:
                            is_match = False
                            break
                    if not is_match:
                        break
                if is_match:
                    return True
        return False

    def __hash__(self):
        # to be able to use the state in a set
        return hash(str([item for sublist in self.board for item in sublist]))

    def __eq__(self, other):
        # compares the two matrices
        return [item for sublist in self.board for item in sublist] == [item for sublist in other.board for item in
                                                                        sublist]
