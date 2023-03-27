# import libraries

import sys
from enum import Enum
import itertools
import random
import pygame
from pygame import *
import os
import sys
import time
import heapq  # we'll be using a heap to store the states
import math
from copy import deepcopy

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
WALL_TEXTURE = pygame.image.load('resources/assets/wall.jpg').convert()

# set up the clock
clock = pygame.time.Clock()

# set up the game variables
FPS = 60
CELL_SIZE = 60
LINE_WIDTH = 4
WALL = "#"
BLANK_SPACE = "."
LEVEL = 1

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
CURSOR_COLOR = (255, 0, 0)  # red color for the cursor
BUTTON_COLOR = (128, 128, 0)
ATOM_COLORS = {
    'C': (0, 0, 0),  # black
    'H': (255, 255, 255),  # white
    'N': (255, 0, 0),  # red
    'O': (255, 255, 0)  # yellow
}

# set up the fonts
FONT_SMALL =  pygame.font.SysFont('Arial', 15)
FONT_MEDIUM = pygame.font.SysFont('Arial', 30)


# Calculate the offset for the board to go down
board_y_offset = 100


# Define the Mode Enum
class Mode(Enum):
    NONE = 0
    COMPUTER = 1
    HUMAN = 2


def create_button(text, center_x, center_y, font_size=40, padding=20, depth=4):
    font = pygame.font.Font('resources/assets/atomix-font.otf', font_size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    button_rect = pygame.Rect(text_rect.left - padding, text_rect.top - padding,
                              text_rect.width + padding * 2, text_rect.height + padding * 2)

    depth_rects = []
    for i in range(depth):
        depth_rect = pygame.Rect(button_rect.left - i, button_rect.top - i,
                                 button_rect.width + i * 2, button_rect.height + i * 2)
        depth_rects.append(depth_rect)

    return text_surface, text_rect, button_rect, depth_rects


def draw_menu():
    screen.fill((20, 20, 80))  # dark blue background

    title_font = pygame.font.Font('resources/assets/atomix-font.otf', 80)
    title_text = title_font.render("Atomix", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
    screen.blit(title_text, title_rect)

    computer_text, computer_text_rect, computer_button_rect, computer_depth_rects = create_button("Computer Mode", WINDOW_WIDTH // 2, 350)
    for depth_rect in computer_depth_rects:
        pygame.draw.rect(screen, RED, depth_rect)
    screen.blit(computer_text, computer_text_rect)

    human_text, human_text_rect, human_button_rect, human_depth_rects = create_button("Human Mode", WINDOW_WIDTH // 2, 450)
    for depth_rect in human_depth_rects:
        pygame.draw.rect(screen, GREEN, depth_rect)
    screen.blit(human_text, human_text_rect)

    pygame.display.update()

    return computer_button_rect, human_button_rect


def draw_reset_button():
    reset_button = pygame.Rect(WINDOW_WIDTH - 110, 300, 100, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, reset_button)
    reset_text = FONT_MEDIUM.render("Reset", True, BLACK)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    screen.blit(reset_text, reset_text_rect)
    return reset_button


def reset_button_clicked(x, y, reset_button_rect):
    return reset_button_rect.collidepoint(x, y)


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

    return AtomixState(level_map, molecule_to_form, atom_map, molecule_name_phase)


def draw_target_molecule(state, atom_map):
    molecule_rect = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2 * len(state.molecule)))
    molecule_rect.fill(WHITE)

    for idx, atom in enumerate(state.molecule):
        atom_type = atom_map[atom]["atom"]
        atom_connections = atom_map[atom]['connections']
        cell_size = int(CELL_SIZE * 0.7)

        atom_image = pygame.image.load(ATOM_SPRITES[atom_type])
        atom_image = pygame.transform.scale(atom_image, (cell_size, cell_size))

        atom_rect = atom_image.get_rect(center=(CELL_SIZE, idx * 2 * CELL_SIZE + CELL_SIZE))
        molecule_rect.blit(atom_image, atom_rect.topleft)

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
            pygame.draw.line(molecule_rect, GRAY, src_center,
                             (src_center[0] + x_offset, src_center[1] + y_offset), width=13)

    molecule_image_rect = molecule_rect.get_rect(topright=(WINDOW_WIDTH - 10, 150))
    screen.blit(molecule_rect, molecule_image_rect)


# Draws the game board and atoms on the screen into the respective level
def draw_level(state, cursor_position):
    # Clear the screen
    screen.fill(BG_COLOR)

    # Load the state data
    board = state.board
    atom_map = state.atom_map
    molecule_name = state.molecule_name

    # Draw the title
    title_font = pygame.font.Font('resources/assets/atomix-font.otf', 40)
    title_text = title_font.render("Atomix", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    board_height = len(board)
    board_width = len(board[0])

    # Draw the molecule to be built
    molecule_font = pygame.font.Font('resources/assets/atomix-font.otf', 20)
    molecule_text = molecule_font.render(f"Build {molecule_name}", True, BLACK)
    molecule_rect = molecule_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
    screen.blit(molecule_text, molecule_rect)

    # Draw the game board
    wall_texture = pygame.transform.scale(pygame.image.load("resources/assets/wall.jpg"), (CELL_SIZE, CELL_SIZE))
    cursor_col, cursor_row = cursor_position
    cursor_row = (cursor_row - board_y_offset) // CELL_SIZE
    cursor_col = cursor_col // CELL_SIZE

    # Ensure the cursor is within the board boundaries
    cursor_row = max(0, min(board_height - 1, cursor_row))
    cursor_col = max(0, min(board_width - 1, cursor_col))

    draw_reset_button()


    for row in range(board_height):
        for col in range(board_width):
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

                # Draw the cursor after drawing the atoms and walls
                cursor_rect = pygame.Rect(cursor_col * CELL_SIZE, cursor_row * CELL_SIZE + board_y_offset, CELL_SIZE,
                                          CELL_SIZE)
                pygame.draw.rect(screen, CURSOR_COLOR, cursor_rect, 3)  # 3 is the line width for the cursor rectangle

    pygame.display.flip()


def draw_reset_button():
    reset_button = pygame.Rect(WINDOW_WIDTH - 110, 300, 100, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, reset_button)
    reset_text = FONT_MEDIUM.render("Reset", True, BLACK)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    screen.blit(reset_text, reset_text_rect)
    return reset_button



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


def map_walls(state):
    walls = []
    for row_idx, row in enumerate(state.board):
        for col_idx, char in enumerate(row):
            if char == "#":
                walls.append((row_idx, col_idx))
    return walls


def pairwise_distance(state):
    atoms = state.atomic_structure['atoms']
    target_bonds = state.atomic_structure['target_bonds']
    total_distance = 0
    for bond in target_bonds:
        atom1, atom2 = bond
        distance = shortest_path(state.board, atoms[atom1], atoms[atom2])
        required_distance = abs(state.molecule.index(atom1) - state.molecule.index(atom2)) - 1
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



def greedy_search(problem, heuristic):
    # problem (NPuzzleState) - the initial state
    # heuristic (function) - the heuristic function that takes a board (matrix), and returns an integer
    setattr(AtomixState, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
    states = [problem]
    visited = set()  # to not visit the same state twice

    while states:
        state = heapq.heappop(states)

        if state.is_molecule_formed():
            return state.move_history

        visited.add(state)

        for child in state.children():
            if child not in visited:
                heapq.heappush(states, child)

    return None


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


def draw_algorithm_selection():
    screen.fill((20, 20, 80))  # dark blue background

    title_font = pygame.font.Font('resources/assets/atomix-font.otf', 80)
    title_text = title_font.render("Select Algorithm", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
    screen.blit(title_text, title_rect)

    algorithm1_text, algorithm1_text_rect, algorithm1_button_rect, algorithm1_depth_rects = create_button("Greedy Search", WINDOW_WIDTH // 2, 350)
    for depth_rect in algorithm1_depth_rects:
        pygame.draw.rect(screen, RED, depth_rect)
    screen.blit(algorithm1_text, algorithm1_text_rect)

    algorithm2_text, algorithm2_text_rect, algorithm2_button_rect, algorithm2_depth_rects = create_button("A* Search", WINDOW_WIDTH // 2, 450)
    for depth_rect in algorithm2_depth_rects:
        pygame.draw.rect(screen, GREEN, depth_rect)
    screen.blit(algorithm2_text, algorithm2_text_rect)

    pygame.display.update()

    return algorithm1_button_rect, algorithm2_button_rect



def main():
    mode = Mode.NONE
    while mode == Mode.NONE:
        computer_rect, human_rect = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if computer_rect.collidepoint(x, y):
                    mode = Mode.COMPUTER
                elif human_rect.collidepoint(x, y):
                    mode = Mode.HUMAN

    if mode == Mode.COMPUTER:
        algorithm = None
        while algorithm is None:
            algorithm1_rect, algorithm2_rect = draw_algorithm_selection()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if algorithm1_rect.collidepoint(x, y):
                        algorithm = greedy_search
                    elif algorithm2_rect.collidepoint(x, y):
                        algorithm = a_star_search
    else:
        algorithm = None

    game_over = False
    cursor_position = (0, 0)
    selected_atom = None
    game_state = read_level(LEVEL)
    move_count = 0

    # game loop
    while not game_over:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                reset_button_rect = draw_reset_button()
                if reset_button_clicked(x, y, reset_button_rect):
                    game_state = read_level(LEVEL)
                    cursor_position = (0, 0)
                    selected_atom = None
                    move_count = 0
                    continue
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    move_direction = {
                        pygame.K_UP: (0, -1),
                        pygame.K_DOWN: (0, 1),
                        pygame.K_LEFT: (-1, 0),
                        pygame.K_RIGHT: (1, 0),
                    }[event.key]

                    if selected_atom is None:
                        cursor_position = game_state.move_cursor(cursor_position, move_direction, CELL_SIZE, board_y_offset)
                    else:
                        atom_row, atom_col = game_state.atomic_structure["atoms"][selected_atom]
                        move_function = {
                            (0, -1): game_state.up,
                            (0, 1): game_state.down,
                            (-1, 0): game_state.left,
                            (1, 0): game_state.right,
                        }[move_direction]
                        new_state = move_function(selected_atom, atom_row, atom_col)
                        if new_state:
                            move_count += 1
                            game_state = deepcopy(new_state)
                            selected_atom = None
                elif event.key == pygame.K_SPACE:
                    if selected_atom is None:
                        selected_atom = game_state.get_atom_at(cursor_position, CELL_SIZE, board_y_offset)
                    else:
                        selected_atom = None

        # draw the level
        draw_level(game_state, cursor_position)

        # display move count
        move_count_text = FONT_MEDIUM.render(f"Moves: {move_count}", True, BLACK)
        move_count_rect = move_count_text.get_rect(topleft=(20, WINDOW_HEIGHT - 40))
        screen.blit(move_count_text, move_count_rect)

        pygame.display.update()

        if game_state.is_molecule_formed():
            game_over = True
            print("Congratulations, you've formed the molecule!")

        pygame.display.update()


if __name__ == "__main__":
    main()


def print_sequence(sequence):
    print("Steps:", len(sequence) - 1)
    # prints the sequence of states
    for state in sequence:
        for row in state:
            print(row)
        print()


def bfs(problem):
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

def a_star_search(problem, heuristic):
    # problem (AtomixState) - the initial state
    # heuristic (function) - the heuristic function that takes a board (matrix), and returns an integer

    # this is very similar to greedy, the difference is that it takes into account the cost of the path so far
    return greedy_search(problem, lambda state: heuristic(state) + state.cost)

def ida_star_search(problem, heuristic):
    def search(path, g, threshold):
        state = path[-1]
        f = g + heuristic(state)
        if f > threshold:
            return f
        if state.is_molecule_formed():
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

    threshold = heuristic(problem)
    path = [problem]
    while True:
        t = search(path, 0, threshold)
        if t is None:
            return path[1:]
        threshold = t


