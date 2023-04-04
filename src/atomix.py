# import libraries
from enum import Enum
import pygame
from pygame import *
import os
import sys
from copy import deepcopy
import re
import time
from uniformed_algortihms import *
from heuristic_algorithms import *
from heuristics import *

# initialize pygame
pygame.init()

# set up the display
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Atomix")
WALL_TEXTURE = pygame.image.load('resources/assets/wall.jpg').convert()

# set up the clock
clock = pygame.time.Clock()
mixer.init()

# set up the game variables
FPS = 60
CELL_SIZE = 45
LINE_WIDTH = 4
WALL = "#"
BLANK_SPACE = "."
LEVEL = 2

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BG_COLOR = (50, 50, 50)  # dark gray
WALL_COLOR = (192, 192, 192)  # light gray
BOARD_COLOR = (220, 220, 220)  # light grey color
LINE_COLOR = (255, 255, 255)  # Bright white
CURSOR_COLOR = (255, 0, 0)  # red color for the cursor
BUTTON_COLOR = (128, 128, 0)
ATOM_COLORS = {
    'C': (0, 255, 0),  # green
    'H': (255, 255, 255),  # white
    'N': (255, 0, 0),  # red
    'O': (255, 255, 0)  # yellow
}

# set up the fonts
FONT_SMALL = pygame.font.SysFont('Arial', 22)
FONT_MEDIUM = pygame.font.SysFont('Arial', 30)


# Calculate the offset for the board to go down
board_y_offset = 150
board_x_offset = 50


# Define the Mode Enum
class Mode(Enum):
    NONE = 0
    COMPUTER = 1
    HUMAN = 2
    HOW_TO_PLAY = 3


win_sound = mixer.Sound('resources/sounds/win-sound.wav')
pygame.mixer.music.load('resources/sounds/game-loop-song.mp3')

pygame.mixer.music.play(-1)


background_image = pygame.image.load('resources/assets/atomix_wallpaper_menu.png')
scaled_background_image_1 = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

background_image = pygame.image.load('resources/assets/atomix_wallpaper_menu_2.png')
scaled_background_image_2 = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


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
    screen.blit(scaled_background_image_1, (0, 0))

    title_font = pygame.font.Font('resources/assets/atomix-font.otf', 80)
    title_text = title_font.render("Atomix", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    computer_text, computer_text_rect, computer_button_rect, computer_depth_rects = create_button("Computer Mode", WINDOW_WIDTH // 2, 250)
    for depth_rect in computer_depth_rects:
        pygame.draw.rect(screen, RED, depth_rect)
    screen.blit(computer_text, computer_text_rect)

    human_text, human_text_rect, human_button_rect, human_depth_rects = create_button("Human Mode", WINDOW_WIDTH // 2, 350)
    for depth_rect in human_depth_rects:
        pygame.draw.rect(screen, GREEN, depth_rect)
    screen.blit(human_text, human_text_rect)

    how_to_play_text, how_to_play_text_rect, how_to_play_button_rect, how_to_play_depth_rects = create_button("How to Play", WINDOW_WIDTH // 2, 550)
    for depth_rect in how_to_play_depth_rects:
        pygame.draw.rect(screen, YELLOW, depth_rect)
    screen.blit(how_to_play_text, how_to_play_text_rect)

    pygame.display.update()

    return computer_button_rect, human_button_rect, how_to_play_button_rect



def draw_back_to_menu_button():
    back_to_menu_text = FONT_MEDIUM.render("Back to Menu", True, BLACK)
    back_to_menu_rect = back_to_menu_text.get_rect(topleft=(20, 20))
    back_to_menu_button_rect = pygame.Rect(back_to_menu_rect.x - 5, back_to_menu_rect.y - 5, back_to_menu_rect.width + 10, back_to_menu_rect.height + 10)
    pygame.draw.rect(screen, WHITE, back_to_menu_button_rect, border_radius=5)
    pygame.draw.rect(screen, RED, back_to_menu_button_rect, width=2, border_radius=5)
    screen.blit(back_to_menu_text, back_to_menu_rect)
    return back_to_menu_button_rect


def back_to_menu_clicked(x, y, back_to_menu_rect):
    return back_to_menu_rect.collidepoint(x, y)


def reset_button_clicked(x, y, reset_button_rect):
    return reset_button_rect.collidepoint(x, y)


def read_level(level_number):
    filename = f"level{level_number}.txt"
    filepath = os.path.join("resources/levels", filename)

    level_map = []
    atom_map = {}
    molecule_name_phase = None

    molecule_to_form = []
    is_molecule_read = False
    is_atom_map_read = False

    with open(filepath) as f:
        for line in f:
            line_strip = line.strip()
            if molecule_name_phase is None:
                molecule_name_phase = line_strip
                continue
            if not is_molecule_read:
                if line_strip.startswith('#') or line_strip.startswith('.'):
                    level_map.append(line_strip)
                elif line_strip == '':
                    is_molecule_read = True
            elif not is_atom_map_read:
                if line_strip != '':
                    molecule_to_form.append(line_strip)
                elif line_strip == '':
                    is_atom_map_read = True
            else:
                num, *atom_data = line_strip.split()
                atom, links = atom_data[0], atom_data[1:]
                atom_map[int(num)] = {"atom": atom, "connections": {}}
                for l in links:
                    num_pattern = re.compile(r'\d+')
                    direction = l[-1]
                    neighbor_num = int(num_pattern.match(l).group())
                    atom_map[int(num)]["connections"][direction] = neighbor_num

    return AtomixState(level_map, molecule_to_form, atom_map, molecule_name_phase)


def draw_target_molecule(molecule_str, atom_map):
    molecule_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
    molecule_surf.fill((0, 0, 0, 0))

    offset_x = 0
    offset_y = 50

    for row_idx, row in enumerate(molecule_str):
        for col_idx, atom_num in enumerate(row):
            if atom_num.isdigit():
                atom_type = atom_map[int(atom_num)]["atom"]
                atom_connections = atom_map[int(atom_num)]['connections']
                cell_size = int(CELL_SIZE * 0.7)

                atom_rect = pygame.Rect(col_idx * CELL_SIZE + (CELL_SIZE - cell_size) // 2 + offset_x,
                                        row_idx * CELL_SIZE + (CELL_SIZE - cell_size) // 2 + offset_y,
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
                    pygame.draw.line(molecule_surf, GRAY, src_center,
                                     (src_center[0] + x_offset, src_center[1] + y_offset), width=13)

                # Draw diamond shape
                diamond_points = [(atom_rect.centerx, atom_rect.top), (atom_rect.right, atom_rect.centery),
                                  (atom_rect.centerx, atom_rect.bottom), (atom_rect.left, atom_rect.centery)]
                pygame.draw.polygon(molecule_surf, ATOM_COLORS[atom_type], diamond_points)

                text_surface = FONT_SMALL.render(atom_type, True, BLACK)
                text_rect = text_surface.get_rect(center=atom_rect.center)
                molecule_surf.blit(text_surface, text_rect)

    molecule_image_rect = molecule_surf.get_rect(center=(WINDOW_WIDTH - 150, 200))
    screen.blit(molecule_surf, molecule_image_rect)


def draw_mute_button(muted):
    x, y = WINDOW_WIDTH - 100, 20
    button_size = (64, 64)

    # Load the icon image based on the muted state
    if muted:
        mute_icon = pygame.image.load('resources/assets/unmute.png')
    else:
        mute_icon = pygame.image.load('resources/assets/mute.png')

    # Scale the icon to the desired size
    mute_icon = pygame.transform.scale(mute_icon, button_size)

    # Create a rect for the icon
    mute_icon_rect = mute_icon.get_rect(topleft=(x, y))

    # Draw the icon on the screen
    screen.blit(mute_icon, mute_icon_rect)

    return mute_icon_rect



def draw_reset_button():
    reset_button = pygame.Rect(WINDOW_WIDTH - 250, 350, 100, 40)
    pygame.draw.rect(screen, GREEN, reset_button)
    reset_font = pygame.font.Font('resources/assets/atomix-font.otf', 30)
    reset_text = reset_font.render("RESET", True, WHITE)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    screen.blit(reset_text, reset_text_rect)
    return reset_button


# Draws the game board and atoms on the screen into the respective level
def draw_level(state, cursor_position):
    screen.blit(scaled_background_image_2, (0, 0))

    # Load the state data
    board = state.board
    atom_map = state.atom_map
    molecule_name = state.molecule_name

    # Draw the title
    title_font = pygame.font.Font('resources/assets/atomix-font.otf', 40)
    title_text = title_font.render("Atomix", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    board_height = len(board)
    board_width = len(board[0])

    # Draw the molecule to be built
    molecule_font = pygame.font.Font('resources/assets/atomix-font.otf', 20)
    molecule_text = molecule_font.render(f"PHASE: {molecule_name}", True, WHITE)
    molecule_rect = molecule_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
    screen.blit(molecule_text, molecule_rect)

    # Draw the game board
    wall_texture = pygame.transform.scale(pygame.image.load("resources/assets/wall.jpg"), (CELL_SIZE, CELL_SIZE))
    cursor_col, cursor_row = cursor_position
    cursor_row = (cursor_row - board_y_offset) // CELL_SIZE
    cursor_col = (cursor_col - board_x_offset) // CELL_SIZE

    # Ensure the cursor is within the board boundaries
    cursor_row = max(0, min(board_height - 1, cursor_row))
    cursor_col = max(0, min(board_width - 1, cursor_col))

    draw_reset_button()
    draw_target_molecule(state.molecule, atom_map)
    draw_mute_button(False)
    draw_back_to_menu_button()

    for row in range(board_height):
        for col in range(board_width):
            cell_rect = pygame.Rect(col * CELL_SIZE + board_x_offset, row * CELL_SIZE + board_y_offset, CELL_SIZE, CELL_SIZE)
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
                atom_rect = pygame.Rect(col * CELL_SIZE + (CELL_SIZE - cell_size) // 2 + board_x_offset,
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

                text_surface = FONT_SMALL.render(atom_type, True, BLACK)
                text_rect = text_surface.get_rect(center=atom_rect.center)
                screen.blit(text_surface, text_rect)

                # Draw the cursor after drawing the atoms and walls
                cursor_rect = pygame.Rect(cursor_col * CELL_SIZE + board_x_offset, cursor_row *
                                          CELL_SIZE + board_y_offset, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, CURSOR_COLOR, cursor_rect, 3)  # 3 is the line width for the cursor rectangle

    pygame.display.flip()


def draw_algorithm_selection():
    screen.fill(BG_COLOR)

    # Add the title
    title_font = pygame.font.Font('resources/assets/atomix-font.otf', 80)
    title_text = title_font.render("Select Algorithm", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # Add the uniformed algorithms column
    uniformed_algorithms = ["DFS", "BFS", "Iterative Deepening", "Uniform Cost"]
    uniformed_algorithm_rects = []
    for i, algorithm in enumerate(uniformed_algorithms):
        text, text_rect, button_rect, depth_rects = create_button(algorithm, WINDOW_WIDTH // 4, 200 + i * 100)
        uniformed_algorithm_rects.append(button_rect)
        screen.blit(text, text_rect)

    # Add the heuristic algorithms column
    heuristic_algorithms = ["Greedy Search", "A* Search", "Weighted A* Search"]
    heuristic_algorithm_rects = []
    for i, algorithm in enumerate(heuristic_algorithms):
        text, text_rect, button_rect, depth_rects = create_button(algorithm, 3 * WINDOW_WIDTH // 4, 200 + i * 100)
        heuristic_algorithm_rects.append(button_rect)
        screen.blit(text, text_rect)

    pygame.display.update()

    return uniformed_algorithm_rects, heuristic_algorithm_rects


def display_win_message():
    # Create a semi-transparent black surface
    win_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    win_overlay.fill((0, 0, 0, 128))

    # Render the win message text
    win_message_font = pygame.font.Font(None, 60)
    win_message_text = "Congratulations! You win!"
    win_message_surface = win_message_font.render(win_message_text, True, WHITE)

    # Position the text at the center of the screen
    win_message_rect = win_message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    # Display the message on the screen
    screen.blit(win_overlay, (0, 0))
    screen.blit(win_message_surface, win_message_rect)
    pygame.display.update()


def display_algorithm_info_message(num_operations, max_memory, elapsed_time):
    # Create a semi-transparent black surface
    info_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    info_overlay.fill((0, 0, 0, 128))

    # Render the algorithm information text
    info_font = pygame.font.Font(None, 36)
    info_text = f"Computer completed the molecule!\nOperations: {num_operations}\nMax memory: {max_memory}\nTime: {elapsed_time:.2f} seconds"
    info_lines = info_text.split("\n")
    info_surfaces = [info_font.render(line, True, WHITE) for line in info_lines]

    # Position the text at the center of the screen
    info_rects = [surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 40)) for i, surface in enumerate(info_surfaces)]

    # Display the message on the screen
    screen.blit(info_overlay, (0, 0))
    for surface, rect in zip(info_surfaces, info_rects):
        screen.blit(surface, rect)
    pygame.display.update()


def update_game_state_human(game_state, move_count, cursor_position):
    if game_state.is_molecule_formed():

        game_state.game_won = True
        move_count = 0
        draw_level(game_state, cursor_position)
        pygame.mixer.music.pause()
        win_sound.play()
        pygame.display.update()
        pygame.time.delay(500)

        display_win_message()
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.mixer.music.unpause()

        return True, move_count
    return False, move_count


def update_game_state_computer(game_state, move_count, cursor_position):
    if game_state.is_molecule_formed():
        game_state.game_won = True
        move_count = 0
        draw_level(game_state, cursor_position)
        pygame.mixer.music.pause()
        win_sound.play()
        pygame.display.update()
        pygame.time.delay(500)

        display_algorithm_info_message(num_operations, max_memory, elapsed_time)
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.mixer.music.unpause()

        return True, move_count
    return False, move_count



solution = []
UNIFORMED_ALGORITHMS = [depth_first_search, breadth_first_search, iterative_deepening, uniform_cost]
HEURISTIC_ALGORITHMS = [greedy_search, a_star_search, weighted_a_star_search]
num_operations = 0
max_memory = 0
elapsed_time = 0

def computer_play(game_state, algorithm):
    global solution, num_operations, max_memory, elapsed_time

    if not solution:
        start_time = time.time()
        if algorithm in UNIFORMED_ALGORITHMS:
            move_history, num_operations, max_memory = algorithm(game_state)
        elif algorithm in HEURISTIC_ALGORITHMS:
            move_history, num_operations, max_memory = algorithm(game_state, heuristic)
        elapsed_time = time.time() - start_time

        if move_history:
            solution = move_history

    if solution:
        next_move = solution.pop(0)
        game_state = deepcopy(next_move)
        game_state.update_bonds()

    return game_state


def draw_how_to_play():
    screen.blit(scaled_background_image_2, (0, 0))

    title_font = pygame.font.Font('resources/assets/atomix-font.otf', 40)
    title_text = title_font.render("How to Play", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    instructions = [
        "Atomix is a puzzle game where the objective is to assemble molecules",
        "from separate atoms.",
        "Move atoms horizontally or vertically, they will not stop until they",
        "hit a wall or another atom.",
        "To win, you must form the target molecule shown at the beginning.",
        "",
        "Controls:",
        "Space Bar - Select Atom/Release Atom",
        "Arrow keys - Move atoms",
    ]

    instructions_font = pygame.font.Font('resources/assets/atomix-font.otf', 28)
    for i, line in enumerate(instructions):
        line_text = instructions_font.render(line, True, WHITE)
        line_rect = line_text.get_rect(center=(WINDOW_WIDTH // 2, 100 + i * 30))
        screen.blit(line_text, line_rect)

    return_button_text, return_button_text_rect, return_button_rect, return_button_depth_rects = create_button("Return to Menu", WINDOW_WIDTH // 2, 500)
    for depth_rect in return_button_depth_rects:
        pygame.draw.rect(screen, RED, depth_rect)
    screen.blit(return_button_text, return_button_text_rect)

    pygame.display.update()

    return return_button_rect


def how_to_play():
    return_button_rect = draw_how_to_play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if return_button_rect.collidepoint(x, y):
                    return


def menu():
    while True:
        mode = Mode.NONE
        algorithm = None
        computer_rect, human_rect, how_to_play_rect = draw_menu()
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
                elif how_to_play_rect.collidepoint(x, y):
                    mode = Mode.HOW_TO_PLAY

        if mode == Mode.COMPUTER:
            while algorithm is None:
                uniformed_algorithm_rects, heuristic_algorithm_rects = draw_algorithm_selection()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        for i, rect in enumerate(uniformed_algorithm_rects):
                            if rect.collidepoint(x, y):
                                if i == 0:
                                    algorithm = depth_first_search
                                elif i == 1:
                                    algorithm = breadth_first_search
                                elif i == 2:
                                    algorithm = iterative_deepening
                                elif i == 3:
                                    algorithm = uniform_cost

                        for i, rect in enumerate(heuristic_algorithm_rects):
                            if rect.collidepoint(x, y):
                                if i == 0:
                                    algorithm = greedy_search
                                elif i == 1:
                                    algorithm = a_star_search
                                elif i == 2:
                                    algorithm = weighted_a_star_search

            return mode, algorithm
        elif mode == Mode.HUMAN:
            return mode, None
        elif mode == Mode.HOW_TO_PLAY:
            how_to_play()
            continue


def play_game(mode, algorithm=None, level=1):
    game_over = False
    cursor_position = (1, 1)
    selected_atom = None
    game_state = read_level(level)
    move_count = 0
    muted = False

    while not game_over:
        clock.tick(FPS)

        mute_button_rect = draw_mute_button(muted)

        back_to_menu_rect = draw_back_to_menu_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                reset_button_rect = draw_reset_button()
                if mute_button_rect.collidepoint(x, y):
                    muted = not muted  # Toggle the mute status
                    if muted:
                        pygame.mixer.music.pause()  # Pause the music when muted
                    else:
                        pygame.mixer.music.unpause()  # Unpause the music when not muted
                if reset_button_clicked(x, y, reset_button_rect):
                    game_state = read_level(level)
                    cursor_position = (0, 0)
                    selected_atom = None
                    move_count = 0
                    continue
                if back_to_menu_clicked(x, y, back_to_menu_rect):
                    main()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    move_direction = {
                        pygame.K_UP: (0, -1),
                        pygame.K_DOWN: (0, 1),
                        pygame.K_LEFT: (-1, 0),
                        pygame.K_RIGHT: (1, 0),
                    }[event.key]

                    if selected_atom is None:
                        cursor_position = game_state.move_cursor(cursor_position, move_direction, CELL_SIZE,
                                                                 board_y_offset, board_x_offset)
                    else:
                        selected_atom_pos = game_state.atomic_structure['atoms'][selected_atom]
                        cursor_position = game_state.move_cursor(cursor_position, move_direction, CELL_SIZE, board_y_offset, board_x_offset,
                                                        selected_atom_pos)
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
                            game_state.update_bonds()
                            game_won, move_count = update_game_state_human(game_state, move_count, cursor_position)
                            if game_won:
                                level += 1
                                game_state = read_level(level)
                elif event.key == pygame.K_SPACE:
                    if selected_atom is None:
                        selected_atom = game_state.get_atom_at(cursor_position, CELL_SIZE, board_y_offset,
                                                               board_x_offset)
                    else:
                        selected_atom = None

        if mode == Mode.COMPUTER:
            game_state = computer_play(game_state, algorithm)
            game_won, move_count = update_game_state_computer(game_state, move_count, cursor_position)
            if game_won:
                level += 1
                game_state = read_level(level)
            pygame.time.delay(500)  # Add a delay (in milliseconds) between the computer's moves

        move_count_text = FONT_MEDIUM.render(f"Moves: {move_count}", True, BLACK)
        move_count_rect = move_count_text.get_rect(center=(WINDOW_WIDTH - 100, WINDOW_HEIGHT // 2 + 50))
        screen.blit(move_count_text, move_count_rect)

        draw_level(game_state, cursor_position)

        pygame.display.update()


def main():
    while True:
        mode, algorithm = menu()
        if mode != Mode.NONE:
            play_game(mode, algorithm)


if __name__ == "__main__":
    main()


