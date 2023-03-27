'''


def move_player(direction, player_pos):
    x, y = player_pos
    if direction == 'up':
        if y > 0:
            player_pos = (x, y - 1)
    elif direction == 'down':
        if y < BOARD_HEIGHT - 1:
            player_pos = (x, y + 1)
    elif direction == 'left':
        if x > 0:
            player_pos = (x - 1, y)
    elif direction == 'right':
        if x < BOARD_WIDTH - 1:
            player_pos = (x + 1, y)


def is_valid_move(row, col):


def make_move(row, col):


def check_game_over(): # if we want to difficult, add a limit of moves



def solve_game(algorithm, heuristic):
    # Solve the game using the specified algorithm and heuristic
    global board, game_over
    board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    game_over = False
    score = 0
    pieces_left = 10
    while not game_over and pieces_left > 0:
        if algorithm == "BFS":
            path = bfs(heuristic)
        elif algorithm == "DFS":
            path = dfs(heuristic)
        elif algorithm == "IDDFS":
            path = iddfs(heuristic)
        elif algorithm == "UCS":
            path = ucs(heuristic)
        elif algorithm == "GREEDY":
            path = greedy(heuristic)
        elif algorithm == "ASTAR":
            path = astar(heuristic)
        elif algorithm == "WA":
            path = weighted_astar(heuristic, 2.0)
        elif algorithm == "WA2":
            path = weighted_astar(heuristic, 3.0)
        else:
            raise ValueError("Invalid algorithm")
        if path is None:
            game_over = True
        else:
            for move in path:
                row, col = move
                if board[row][col] == 0:
                    make_move(row, col)
                    pieces_left -= 1
                    score += 1
        draw_board()
        draw_score(score)
        pygame.display.flip()
        pygame.time.wait(500)
'''


'''
 def select_atom(state):
    # Print the current game board
    os.system('clear')
    draw_level(state)

    # Get the current position of the atom cursor
    row, col = get_cursor_pos(state)

    while True:
        # Read input from the user
        key = get_key()
        print(key)

        if key == 'q':
            # Quit the game if the user presses 'q'
            return False

        if key in ['w', 'a', 's', 'd']:
            # Move the atom cursor using arrow keys
            new_row, new_col = move_cursor(row, col, key, state)
            if new_row != row or new_col != col:
                row, col = new_row, new_col
                os.system('clear')
                draw_level(new_state)

        if key == ' ':
            # Check if there is an atom in the selected cell
            if state[row][col].isupper():
                return True
            else:
                return False
'''

'''
    # game over, display message
    if check_game_over():
        draw_message("Congratulations, you won!")
    else:
        draw_message("Game over")
    '''

'''
def min_distance_to_bond(state):
    atoms = state.atomic_structure['atoms']
    bonds = state.atomic_structure['bonds']
    total_distance = 0
    for atom1, pos1 in atoms.items():
        closest_atom, closest_distance = None, float('inf')
        atom2 = get_closest_bonded_atom(atom1, state.atomic_structure)
        distance = manhattan_distance(pos1, atoms[atom2])
        if distance < closest_distance:
            closest_atom, closest_distance = atom2, distance
        direction = get_direction(pos1, atoms[closest_atom])
        if direction == 'up':
            total_distance += pos1[0] - 1
        elif direction == 'down':
            total_distance += state.grid_size - pos1[0]
        elif direction == 'left':
            total_distance += pos1[1] - 1
        elif direction == 'right':
            total_distance += state.grid_size - pos1[1]
    return total_distance
'''



import pygame

# Set up the game board
board = [
    "###########",
    "#..#......#",
    "#.3#......#",
    "#.##......#",
    "#.#..#.####",
    "#....#.2..#",
    "###.#.....#",
    "#1....#...#",
    "###########"
]

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Set up the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Atomix Game")

# Set up the font
font = pygame.font.SysFont(None, 24)

# Define a function to draw the game board
def draw_board(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "#":
                pygame.draw.rect(screen, BLACK, (col*50, row*50, 50, 50))
            elif board[row][col] == ".":
                pygame.draw.rect(screen, WHITE, (col*50, row*50, 50, 50))
            elif board[row][col] == "1":
                pygame.draw.rect(screen, BLUE, (col*50, row*50, 50, 50))
                text = font.render("H 1R", True, WHITE)
                screen.blit(text, (col*50, row*50))
            elif board[row][col] == "2":
                pygame.draw.rect(screen, BLUE, (col*50, row*50, 50, 50))
                text = font.render("O 1R 1L", True, WHITE)
                screen.blit(text, (col*50, row*50))
            elif board[row][col] == "3":
                pygame.draw.rect(screen, BLUE, (col*50, row*50, 50, 50))
                text = font.render("H 1L", True, WHITE)
                screen.blit(text, (col*50, row*50))

# Main game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(WHITE)

    # Draw the game board
    draw_board(board)

    # Update the display
    pygame.display.flip()

def distance(state):
    # calculate the total Manhattan distance between atoms in the state
    atoms = state.atomic_structure['atoms']
    total_distance = 0
    walls = map_walls(state)
    for atom1 in atoms.keys():
        atom2 = get_closest_bonded_atom(atom1, state.atomic_structure)
        total_distance += manhattan_distance(atoms[atom1], atoms[atom2], walls)
    return total_distance


def next_bond(state):
    # find the pair of atoms with the smallest distance that are not yet bonded
    atoms = state.atomic_structure['atoms']
    molecule = state.molecule
    bonds = set(state.atomic_structure['bonds'])
    min_distance = float('inf')
    min_pair = None
    for atom1 in atoms.keys():
        for atom2 in atoms.keys():
            if atom1 == atom2 or (atom1, atom2) in bonds or (atom2, atom1) in bonds:
                continue
            dist = shortest_path(state.board, atoms[atom1], atoms[atom2])
            structure_penalty = abs(molecule.index(atom1) - molecule.index(atom2)) - 1
            dist += structure_penalty
            if dist < min_distance:
                min_distance = dist
                min_pair = (atom1, atom2)
    return min_pair