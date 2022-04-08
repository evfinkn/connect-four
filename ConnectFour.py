import pygame
# https://www.pygame.org
import random
from copy import deepcopy

pygame.init()
random.seed()

FILE_PATH = "grid.txt"    # save file

# Colors
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 122)
LIGHTER_GRID_COLOR = (0, 37, 161)
NEW_GAME_BUTTON_COLOR = GRID_COLOR
LOAD_GAME_BUTTON_COLOR = GRID_COLOR
P1_COIN_COLOR = (255, 0, 0)
P2_COIN_COLOR = (255, 255, 0)
COLOR_NAMES = {P1_COIN_COLOR: "red", P2_COIN_COLOR: "yellow"}

EMPTY_GRID = [[BACKGROUND_COLOR for _ in range(7)] for _ in range(6)]

# Create the variables for the size of the grid, extra space on sides, and screen
slot_size = 50
width = slot_size * 7
extra_space = slot_size // 2
height = slot_size * 6

# Coin surfaces
coin_surfaces = {P1_COIN_COLOR: pygame.Surface((slot_size, slot_size)),
                 P2_COIN_COLOR: pygame.Surface((slot_size, slot_size))}
for coin_color, coin_surface in coin_surfaces.items():
    coin_surface.fill(BACKGROUND_COLOR)
    # pygame.draw.circle(surface, color, pos, radius)
    pygame.draw.circle(coin_surface, coin_color,
                       (slot_size // 2, slot_size // 2),
                       (slot_size // 2) - (slot_size // 20))

# Create grid, colors, and surfaces
# grid = [[BACKGROUND_COLOR for _ in range(7)] for _ in range(6)]

# grid_surface is a square in the color of the grid. It is then blotted onto the
# screen later in the drawBackground function. This forms the Connect 4 board
grid_surface = pygame.Surface((slot_size, slot_size))
grid_surface.fill(GRID_COLOR)
# Any pixels with BACKGROUND_COLOR will be transparent when blitted
grid_surface.set_colorkey(BACKGROUND_COLOR)

# pygame.draw.circle(surface, color, pos, radius)
# draw white circle to represent empty slot
pygame.draw.circle(grid_surface, BACKGROUND_COLOR,
                   (slot_size // 2, slot_size // 2),
                   (slot_size // 2) - (slot_size // 20))

# Variables for the title text
# pygame.font.Font(filename, size)
TITLE_FONT = pygame.font.Font("freesansbold.ttf", slot_size)
# Font.render(text, antialias, color)
title = TITLE_FONT.render("Connect Four", True, GRID_COLOR)
title_rect = title.get_rect(
    center=((width + extra_space * 2) // 2, (height + extra_space * 2) // 4))

# Font for the text on buttons
BUTTON_FONT = pygame.font.Font("freesansbold.ttf", slot_size // 2)

# The text for the new game button
ng_button_text = BUTTON_FONT.render("New Game", True, BACKGROUND_COLOR)
ng_button_text_rect = ng_button_text.get_rect(
    center=((width + extra_space * 2) // 2, (height + extra_space * 2) // 2))

# The text for the load game button
lg_button_text = BUTTON_FONT.render("Load Game", True, BACKGROUND_COLOR)
lg_button_text_rect = lg_button_text.get_rect(
    center=((width + extra_space * 2) // 2, (height + extra_space * 2) // 2 + extra_space * 3))

# The CLOCK and FPS
CLOCK = pygame.time.Clock()
FPS = 60

# The rects and colors for the buttons and color
# pygame.Rect(left, top, width, height
ng_button = pygame.Rect((width + extra_space * 2) // 2 - int(slot_size * 1.5),
                        (height + extra_space * 2) // 2 - extra_space,
                        slot_size * 3, slot_size)
lg_button = pygame.Rect((width + extra_space * 2) // 2 - int(slot_size * 1.5),
                        (height + extra_space * 2) // 2 + extra_space * 2,
                        slot_size * 3, slot_size)


# Draw the board
def draw_board(surface, board):
    for i in range(6):
        for j in range(7):
            if board[i][j] != (255, 255, 255):
                surface.blit(coin_surfaces[board[i][j]], (slot_size * j + extra_space, slot_size * i + extra_space))
            surface.blit(grid_surface, (slot_size * j + extra_space, slot_size * i + extra_space))


# Draw the new/load game buttons
def draw_button(surface, buttons, button_colors):
    for x in range(len(buttons)):
        # pygame.draw_rect(surface, color, rect)
        pygame.draw.rect(surface, button_colors[x], buttons[x])
    surface.blit(surface, (0, 0))


# Finds the spot that the coin is placed on mouse click
def find_spot(board, mouse_pos):
    if extra_space < mouse_pos[0] < width + extra_space:
        column = (mouse_pos[0] + extra_space) // slot_size - 1
        for i in range(len(board) - 1, -1, -1):
            if board[i][column] == BACKGROUND_COLOR:
                return i, column
    return -1


# Searches for any wins (4 coins next to each other vertically, horizontally, or diagonally)
def find_win(board):
    def compare_coins(i1, j1, i2, j2):
        change_i = (i2 - i1) // 3
        change_j = (j2 - j1) // 3
        return board[i1][j1] \
            == board[i1 + change_i][j1 + change_j] \
            == board[i1 + (2 * change_i)][j1 + (2 * change_j)] \
            == board[i2][j2]

    for i in range(len(board) - 1, -1, -1):
        for j in range(len(board[i]) - 1, -1, -1):
            if board[i][j] == BACKGROUND_COLOR:
                continue    # prevents another indentation level
            # The if statements prevent out of bounds errors
            if i <= 2:
                # vertical win
                if compare_coins(i, j, i + 3, j):
                    return {"color": board[i][j],
                            "point1": ((j + 1) * slot_size, (i + 1) * slot_size),
                            "point2": ((j + 1) * slot_size, (i + 4) * slot_size)
                            }
                elif j <= 3 and compare_coins(i, j, i + 3, j + 3):
                    # Negative slope diagonal win
                    return {"color": board[i][j],
                            "point1": ((j + 1) * slot_size, (i + 1) * slot_size),
                            "point2": ((j + 4) * slot_size, (i + 4) * slot_size)
                            }
                elif j >= 3 and compare_coins(i, j, i + 3, j - 3):
                    # Positive slope diagonal win
                    return {"color": board[i][j],
                            "point1": ((j + 1) * slot_size, (i + 1) * slot_size),
                            "point2": ((j - 2) * slot_size, (i + 4) * slot_size)
                            }
            elif j <= 3 and compare_coins(i, j, i, j + 3):
                # Horizontal win
                return {"color": board[i][j],
                        "point1": ((j + 1) * slot_size, (i + 1) * slot_size),
                        "point2": ((j + 4) * slot_size, (i + 1) * slot_size)
                        }
    return None


# Writes the grid to a file in order to save the game
def file_writer(file_path, board):
    with open(file_path, "w") as file:
        for i in range(len(board)):
            for j in range(len(board[i])):
                file.write(str(board[i][j][0]) + "\n")
                file.write(str(board[i][j][1]) + "\n")
                file.write(str(board[i][j][2]) + "\n")


# Reads the file in order to load the game
def file_reader(file_path):
    grid = []
    with open(file_path, "r") as file:
        for i in range(6):
            grid.append([])
            for j in range(7):
                # [:-1] to ignore \n
                red = int(file.readline()[:-1])
                green = int(file.readline()[:-1])
                blue = int(file.readline()[:-1])
                grid[i].append((red, green, blue))
    return grid


# The main game function
def main_game(screen, board=None):
    if board is None:
        board = deepcopy(EMPTY_GRID)
    main_loop = True
    turn = random.choice((-1, 1))

    while main_loop:
        CLOCK.tick(FPS)
        # Change the coin color depending on whose turn it is
        current_color = P1_COIN_COLOR if turn == -1 else P2_COIN_COLOR
        for event in pygame.event.get():
            # If the game is exited out of OR the esc key is pressed, save and end the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                file_writer(FILE_PATH, board)
                main_loop = False
            # If mouseclick, find the location and set that spot to the color of the coin if it's valid
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and (spot := find_spot(board, pygame.mouse.get_pos())) != -1:
                    board[spot[0]][spot[1]] = current_color
                    turn *= -1
        # Reset the screen
        screen.fill(BACKGROUND_COLOR)
        # Draw the coin hovering at the top of the screen
        screen.blit(coin_surfaces[current_color], (pygame.mouse.get_pos()[0] - slot_size // 2, -extra_space))
        draw_board(screen, board)
        pygame.display.flip()
        winner = find_win(board)
        if winner is not None:
            file_writer(FILE_PATH, EMPTY_GRID)  # write to file with
            win_screen(screen, board, winner["color"], winner["point1"], winner["point2"])
            main_loop = False


# The function to run the win screen
def win_screen(screen, winning_board, winner, start_pos, end_pos):
    global NEW_GAME_BUTTON_COLOR
    main_loop = True
    while main_loop:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                main_loop = False
            # If mouseclick on the New Game button, start the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and ng_button.collidepoint(pygame.mouse.get_pos()):
                    main_game(screen)
                    main_loop = False
        # Make the color of the button lighter if the mouse is over it
        pos = pygame.mouse.get_pos()
        if ng_button.collidepoint(pos):
            NEW_GAME_BUTTON_COLOR = LIGHTER_GRID_COLOR
        elif NEW_GAME_BUTTON_COLOR != GRID_COLOR:
            NEW_GAME_BUTTON_COLOR = GRID_COLOR

        screen.fill(BACKGROUND_COLOR)
        draw_board(screen, winning_board)
        # pygame.draw.line(surface, color, start_pos, end_pos, width)
        pygame.draw.line(screen, BACKGROUND_COLOR, start_pos, end_pos, 5)
        draw_button(screen, [ng_button], [NEW_GAME_BUTTON_COLOR])
        screen.blit(ng_button_text, ng_button_text_rect)
        pygame.display.flip()


# The function to run the main menu screen
def main_menu(screen):
    global NEW_GAME_BUTTON_COLOR, LOAD_GAME_BUTTON_COLOR
    main_loop = True
    while main_loop:
        CLOCK.tick(FPS)

        pos = pygame.mouse.get_pos()
        if ng_button.collidepoint(pos):
            NEW_GAME_BUTTON_COLOR = LIGHTER_GRID_COLOR
        elif NEW_GAME_BUTTON_COLOR != GRID_COLOR:
            NEW_GAME_BUTTON_COLOR = GRID_COLOR
        if lg_button.collidepoint(pos):
            LOAD_GAME_BUTTON_COLOR = LIGHTER_GRID_COLOR
        elif LOAD_GAME_BUTTON_COLOR != GRID_COLOR:
            LOAD_GAME_BUTTON_COLOR = GRID_COLOR

        screen.fill(BACKGROUND_COLOR)
        screen.blit(title, title_rect)
        draw_button(screen, [ng_button, lg_button], [NEW_GAME_BUTTON_COLOR, LOAD_GAME_BUTTON_COLOR])
        screen.blit(ng_button_text, ng_button_text_rect)
        screen.blit(lg_button_text, lg_button_text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                main_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if ng_button.collidepoint(pos):
                        main_game(screen)
                        main_loop = False
                    # Load the saved game if click on Load Game button
                    if lg_button.collidepoint(pos):
                        grid = file_reader(FILE_PATH)
                        main_game(screen, grid)
                        main_loop = False


# Create the variable for the screen and start the game
window = pygame.display.set_mode((width + extra_space * 2, height + extra_space * 2))
pygame.display.set_caption("Connect Four")
main_menu(window)
pygame.quit()
