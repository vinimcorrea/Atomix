# import libraries
import random
import numpy as np

import pygame
import os
import sys
import time

from atomix_state import AtomixState
from collections import deque
from queue import PriorityQueue

# initialize pygame
pygame.init()

# set up the display
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Atomix")
WALL_TEXTURE = pygame.image.load('assets/wall.jpg').convert()

# set up the clock
clock = pygame.time.Clock()

# set up the game variables
FPS = 60
CELL_SIZE = 50
NUM_ATOMS = 1
LINE_WIDTH = 4
WALL = "#"
BLANK_SPACE = "."

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (50, 50, 50)  # dark gray
WALL_COLOR = (192, 192, 192)  # light gray
BOARD_COLOR = (220, 220, 220)  # light grey color
LINE_COLOR = (255, 255, 255)  # Bright white
ATOM_COLORS = {
    'C': (0, 0, 0),  # black
    'H': (255, 255, 255),  # white
    'N': (255, 0, 0),  # red
    'O': (255, 255, 0)  # yellow
}

# set up the fonts
FONT_SMALL = pygame.font.SysFont('comicsans', 20)
FONT_MEDIUM = pygame.font.SysFont('Arial', 30)
FONT_LARGE = pygame.font.SysFont('comicsans', 50)


def read_level(level_number):
    filename = f"level{level_number}-water.txt"
    filepath = os.path.join("resources/levels", filename)

    level_map = []
    atom_map = {}
    molecule_name_phase = None

    is_molecule_read = False
    is_atom_map_read = False

    with open(filepath) as f:
        for line in f:
            line_strip = line.strip()
            if molecule_name_phase is None:
                molecule_name_phase = line_strip
                continue
            if line_strip.startswith('#'):
                level_map.append(line_strip)
                continue
            if line_strip == '' and not is_molecule_read:
                is_molecule_read = True
                continue
            if line_strip != '' and is_molecule_read and not is_atom_map_read:
                molecule_to_form = ''
                for c in line_strip:
                    if c.isdigit():
                        molecule_to_form += c
                    elif c.isalpha():
                        molecule_to_form += '.'
                    else:
                        molecule_to_form += '\n'
            if line_strip == '' and not is_atom_map_read:
                is_atom_map_read = True
            if line_strip != '' and is_atom_map_read:
                num, *atom_data = line_strip.split()
                atom, links = atom_data[0], atom_data[1:]
                atom_map[int(num)] = {"atom": atom, "connections": {}}
                for l in links:
                    direction, neighbor_num = l[-1], int(l[:-1])
                    atom_map[int(num)]["connections"][direction] = neighbor_num

    return level_map, atom_map, molecule_name_phase, molecule_to_form


# Draws the game board and atoms on the screen into the respective level
def draw_level(level):
    # Clear the screen
    screen.fill(BG_COLOR)

    # Load the game data
    dataset_game = read_level(level)
    board, atom_map, molecule_name, molecule_structure = dataset_game

    # Draw the title
    title_font = pygame.font.Font('assets/atomix-font.otf', 40)
    title_text = title_font.render("Atomix", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    BOARD_HEIGHT = len(board)
    BOARD_WIDTH = len(board[0])

    # Calculate the offset for the board to go down
    board_y_offset = 100

    # Draw the molecule to be built
    molecule_font = pygame.font.Font('assets/atomix-font.otf', 20)
    molecule_text = molecule_font.render(f"Build {molecule_name}", True, BLACK)
    molecule_rect = molecule_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
    screen.blit(molecule_text, molecule_rect)

    # Draw the game board
    wall_texture = pygame.transform.scale(pygame.image.load("assets/wall.jpg"), (CELL_SIZE, CELL_SIZE))
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + board_y_offset, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BOARD_COLOR, cell_rect, 1)
            if board[row][col] == BLANK_SPACE:
                continue
            elif board[row][col] == WALL:
                screen.blit(wall_texture, cell_rect)
            else:
                # Dealing with an atom
                atom_num = int(board[row][col])
                atom_type = atom_map[atom_num]["atom"]
                atom_connections = atom_map[atom_num]['connections']
                cell_size = int(CELL_SIZE * 0.7)
                atom_rect = pygame.Rect(col * CELL_SIZE + (CELL_SIZE - cell_size) // 2,
                                        row * CELL_SIZE + (CELL_SIZE - cell_size) // 2 + board_y_offset,
                                        cell_size, cell_size)

                # Draw lines between atoms based on their connections
                for direction, distance in atom_connections.items():
                    x_offset, y_offset = 0, 0
                    if direction == "U":
                        y_offset = -distance * CELL_SIZE // 2
                    elif direction == "D":
                        y_offset = distance * CELL_SIZE // 2
                    elif direction == "L":
                        x_offset = -distance * CELL_SIZE // 2
                    elif direction == "R":
                        x_offset = distance * CELL_SIZE // 2

                    src_center = atom_rect.center
                    pygame.draw.line(screen, GRAY, src_center,
                                     (src_center[0] + x_offset, src_center[1] + y_offset), width=13)

                # Draw diamond shape
                diamond_points = [(atom_rect.centerx, atom_rect.top), (atom_rect.right, atom_rect.centery),
                                  (atom_rect.centerx, atom_rect.bottom), (atom_rect.left, atom_rect.centery)]
                pygame.draw.polygon(screen, ATOM_COLORS[atom_type], diamond_points)

                text_surface = FONT_MEDIUM.render(atom_type, True, BLACK)
                text_rect = text_surface.get_rect(center=atom_rect.center)
                screen.blit(text_surface, text_rect)


def main():
    game_over = False

    # randomly place atoms on the board

    # game loop
    while not game_over:
        clock.tick(FPS)

        # handle player movement
        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            move_player("up", player_pos)
        elif keys[pygame.K_DOWN]:
            move_player("down", player_pos)
        elif keys[pygame.K_LEFT]:
            move_player("left", player_pos)
        elif keys[pygame.K_RIGHT]:
            move_player("right", player_pos)

        # check if game is over
        if check_game_over():
            game_over = True
        '''

        # draw the level
        dataset_game = read_level(1)
        board, atom_map, molecule_name, molecule_structure = dataset_game

        af = bfs(AtomixState(board, molecule_structure, atom_map))
        # prints the sequence for the first problem using bfs
        print_sequence(af)

        pygame.display.update()

    '''
    # game over, display message
    if check_game_over():
        draw_message("Congratulations, you won!")
    else:
        draw_message("Game over")
    '''

    # wait for a bit before closing the window
    time.sleep(2)
    pygame.quit()
    sys.exit()


def print_sequence(sequence):
    print("Steps:", len(sequence) - 1)
    # prints the sequence of states
    for state in sequence:
        for row in state:
            print(row)
        print()


def bfs(problem):
    # problem(NPuzzleState) - the initial state
    queue = deque([problem])
    visited = set()  # to not visit the same state twice

    while queue:
        node = queue.popleft()
        visited.add(node)

        if node.is_molecule_formed():
            return node.move_history

        for child in node.children():
            if child not in visited:
                queue.append(child)

    return None



main()


'''
def draw_game(board, atoms):
    """
    Draws the game board and atoms on the screen
    """
    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw the game board
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BOARD_COLOR, cell_rect, 1)
            if board[row][col] == WALL:
                pygame.draw.rect(screen, WALL_COLOR, cell_rect)

    # Draw the atoms
    for atom in atoms:
        row, col, atom_type, direction = atom
        atom_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, ATOM_COLORS[atom_type], atom_rect)
        if direction == UP:
            pygame.draw.line(screen, LINE_COLOR, atom_rect.midTop, atom_rect.top, LINE_WIDTH)
        elif direction == DOWN:
            pygame.draw.line(screen, LINE_COLOR, atom_rect.midBottom, atom_rect.bottom, LINE_WIDTH)
        elif direction == LEFT:
            pygame.draw.line(screen, LINE_COLOR, atom_rect.midLeft, atom_rect.left, LINE_WIDTH)
        elif direction == RIGHT:
            pygame.draw.line(screen, LINE_COLOR, atom_rect.midRight, atom_rect.right, LINE_WIDTH)

    # Draw the message
    draw_message()

    # Update the screen
    pygame.display.update()



# set up the game variables
FPS = 60
CELL_SIZE = 100
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
NUM_ATOMS = 1
LINE_WIDTH = 4
WALL = "#"

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (80, 0, 0)      # burgundy
WALL_COLOR = (16, 22, 73)  # deep blue
BOARD_COLOR = (220, 220, 220)  # light grey color
LINE_COLOR = (255, 255, 255) # Bright white
ATOM_COLORS = {
    'C': (0, 0, 0),   # black
    'H': (255, 255, 255),   # white
    'N': (255, 0, 0),   # red
    'O': (255, 255, 0)   # yellow
}


# set up the fonts
FONT_SMALL = pygame.font.SysFont('comicsans', 20)
FONT_MEDIUM = pygame.font.SysFont('comicsans', 30)
FONT_LARGE = pygame.font.SysFont('comicsans', 50)

# Define the game board as a two-dimensional list of integers
# 0 = empty cell, 1 = atom
board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# Define the game pieces as a dictionary of image files
# set up the atom images
ATOM_IMAGES = []
for i in range(NUM_ATOMS):
    img = pygame.image.load(os.path.join('assets', f'atom{i + 1}.png')).convert_alpha()
    img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
    ATOM_IMAGES.append(img)

# Define the game state variables
game_over = False
selected_atom = None
selected_pos = None
player_pos = (0, 0)


# Crosshair Sprite

def draw_board():
    # Draw the game board
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)


def draw_atoms():
    # Draw the atoms on the game board
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 1:
                atom_img = ATOM_IMAGES[random.randint(0, NUM_ATOMS - 1)]
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                screen.blit(atom_img, rect)


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


def draw_message(message):
    # Draw a message on the screen
    text = FONT_MEDIUM.render(message, True, WHITE)
    rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    pygame.draw.rect(screen, BLUE, rect.inflate(20, 20))
    screen.blit(text, rect)


def is_valid_move(row, col):
    # Check if a move is valid
    if selected_atom is None:
        return False
    if board[row][col] == 1:
        return False
    if row == selected_atom[0] and col == selected_atom[1]:
        return False
    if row != selected_atom[0] and col != selected_atom[1]:
        return False
    if abs(row - selected_atom[0]) > 1 or abs(col - selected_atom[1]) > 1:
        return False
    return True


def make_move(row, col):
    # Make a move on the game board
    board[row][col] = 1
    board[selected_atom[0]][selected_atom[1]] = 0


def check_game_over():
    # Check if the game is over
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] == 0:
                return False
            if row > 0 and board[row][col] == board[row - 1][col]:
                return False
            if row < BOARD_HEIGHT - 1 and board[row][col] == board[row + 1][col]:
                return False
            if col > 0 and board[row][col] == board[row][col - 1]:
                return False
            if col < BOARD_WIDTH - 1 and board[row][col] == board[row][col + 1]:
                return False
    return True


def place_atoms():
    # Randomly place atoms on the board
    for i in range(NUM_ATOMS):
        while True:
            row = random.randint(0, BOARD_HEIGHT - 1)
            col = random.randint(0, BOARD_WIDTH - 1)
            if board[row][col] == 0:
                board[row][col] = 1
                break


def draw_game():
    screen.fill(WHITE)
    draw_board()
    draw_atoms()
    pygame.draw.rect(screen, GRAY, (0, WINDOW_HEIGHT - CELL_SIZE, WINDOW_WIDTH, CELL_SIZE))
    draw_message(f"ATOMIX")
    #draw_message(f"Select an atom and move it to an empty cell")
    pygame.display.update()


def main():
    global game_over, selected_atom, selected_pos, player_pos

    # randomly place atoms on the board
    place_atoms()

    # game loop
    while not game_over:
        clock.tick(FPS)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                # handle_click(x, y)

        # handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            move_player("up", player_pos)
        elif keys[pygame.K_DOWN]:
            move_player("down", player_pos)
        elif keys[pygame.K_LEFT]:
            move_player("left", player_pos)
        elif keys[pygame.K_RIGHT]:
            move_player("right", player_pos)

        # check if game is over
        if check_game_over():
            game_over = True

        # draw the game
        draw_game()

    # game over, display message
    if check_game_over():
        draw_message("Congratulations, you won!")
    else:
        draw_message("Game over")

    # wait for a bit before closing the window
    time.sleep(2)
    pygame.quit()
    sys.exit()


main()


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

def bfs(heuristic):
    # Breadth-first search algorithm
    visited = set()
    queue = [(0, board, None)]
    while queue:
        depth, state, path = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        if check_game_over(state):
            return path
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if state[row][col] == 0:
                    for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_row, new_col = row+drow, col+dcol
                        if new_row >= 0 and new_row < BOARD_HEIGHT and new_col >= 0 and new_col < BOARD_WIDTH and state[new_row][new_col] == 1:
                            new_state = [[state[r][c] for c in range(BOARD_WIDTH)] for r in range(BOARD_HEIGHT)]
                            new_state[row][col] = 1
                            new_state[new_row][new_col] = 0
                            new_path = path + [(row, col)]
                            queue.append((depth+1, new_state, new_path))
    return None

def dfs(heuristic):
    # Depth-first search algorithm
    visited = set()
    stack = [(0, board, None)]
    while stack:
        depth, state, path = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        if check_game_over(state):
            return path
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if state[row][col] == 0:
                    for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_row, new_col = row+drow, col+dcol
                        if 0 <= new_row < BOARD_HEIGHT and 0 <= new_col < BOARD_WIDTH and state[new_row][new_col] == 1:
                            new_state = [[state[r][c] for c in range(BOARD_WIDTH)] for r in range(BOARD_HEIGHT)]
                            new_state[row][col] = 1
                            new_state[new_row][new_col] = 0
                            new_path = path + [(row, col)]
                            stack.append((depth + 1, new_state, new_path))
                        return None


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_game(board, atoms):
    """
    Draws the game board and atoms on the screen
    """
    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw the game board
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BOARD_COLOR, cell_rect, 1)
            if board[row][col] == WALL:
                pygame.draw.rect(screen, WALL_COLOR, cell_rect)

    # Draw the atoms
    for atom in atoms:
        row, col, atom_type, direction = atom
        atom_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, ATOM_COLORS[atom_type], atom_rect)
        if direction == UP:
            pygame.draw.line(screen, LINE_COLOR, atom_rect.midtop, atom_rect.top, LINE_WIDTH)
        elif direction == DOWN:
            pygame.draw.line(screen, LINE_COLOR, atom_rect.midbottom, atom_rect.bottom, LINE_WIDTH)
        elif direction == LEFT:
            pygame.draw.line(screen, LINE_COLOR, atom_rect.midleft, atom_rect.left, LINE_WIDTH)
        elif direction == RIGHT:
            pygame.draw.line(screen, LINE_COLOR, atom_rect.midright, atom_rect.right, LINE_WIDTH)

    # Draw the message
    draw_message()

    # Update the screen
    pygame.display.update()

'''
