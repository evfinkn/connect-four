import pygame
# https://www.pygame.org
import pygameutil
import random
import os

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

title = pygameutil.Text((None, slot_size), "Connect Four", GRID_COLOR,
                        center=((width + extra_space * 2) // 2, (height + extra_space * 2) // 4))

# Font for the text on buttons
BUTTON_FONT = pygame.font.Font(pygame.font.get_default_font(), slot_size // 2)

new_game_text = pygameutil.Text(BUTTON_FONT, "New Game", BACKGROUND_COLOR,
                                center=((width + extra_space * 2) // 2,
                                        (height + extra_space * 2) // 2))
new_game_rect = pygame.Rect((width + extra_space * 2) // 2 - int(slot_size * 1.5),
                            (height + extra_space * 2) // 2 - extra_space,
                            slot_size * 3, slot_size)
new_game_button = pygameutil.Button(new_game_text, new_game_rect, GRID_COLOR, LIGHTER_GRID_COLOR)

load_game_text = pygameutil.Text(BUTTON_FONT, "Load Game", BACKGROUND_COLOR,
                                 center=((width + extra_space * 2) // 2,
                                         (height + extra_space * 2) // 2 + extra_space * 3))
load_game_text.center = ((width + extra_space * 2) // 2, (height + extra_space * 2) // 2 + extra_space * 3)
load_game_rect = pygame.Rect((width + extra_space * 2) // 2 - int(slot_size * 1.5),
                             (height + extra_space * 2) // 2 + extra_space * 2,
                             slot_size * 3, slot_size)
load_game_button = pygameutil.Button(load_game_text, load_game_rect, GRID_COLOR, LIGHTER_GRID_COLOR)

# The CLOCK and FPS
CLOCK = pygame.time.Clock()
FPS = 60


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
def save_game(file_path, board):
    with open(file_path, "w") as file:
        for i in range(len(board)):
            for j in range(len(board[i])):
                file.write(str(board[i][j][0]) + "\n")
                file.write(str(board[i][j][1]) + "\n")
                file.write(str(board[i][j][2]) + "\n")


# Reads the file in order to load the game
def load_game(file_path, screen):
    try:
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
    except FileNotFoundError:
        grid = [[BACKGROUND_COLOR for _ in range(7)] for _ in range(6)]
    main_game(screen, grid)


# The main game function
def main_game(screen, board=None):
    if board is None:
        board = [[BACKGROUND_COLOR for _ in range(7)] for _ in range(6)]
    main_loop = True
    turn = random.choice((-1, 1))

    while main_loop:
        CLOCK.tick(FPS)
        # Change the coin color depending on whose turn it is
        current_color = P1_COIN_COLOR if turn == -1 else P2_COIN_COLOR
        for event in pygame.event.get():
            # If the game is exited out of OR the esc key is pressed, save and end the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                save_game(FILE_PATH, board)
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
            try:
                os.remove(FILE_PATH)    # delete save file because game has been won
            except FileNotFoundError:
                pass    # file already doesn't exist, so we don't need to do anything
            win_screen(screen, board, winner["color"], winner["point1"], winner["point2"])
            main_loop = False


# The function to run the win screen
def win_screen(screen, winning_board, winner, start_pos, end_pos):
    global NEW_GAME_BUTTON_COLOR
    main_loop = True
    while main_loop:
        screen.fill(BACKGROUND_COLOR)
        draw_board(screen, winning_board)
        # pygame.draw.line(surface, color, start_pos, end_pos, width)
        pygame.draw.line(screen, BACKGROUND_COLOR, start_pos, end_pos, 5)
        new_game_button.draw(screen)
        pygame.display.flip()

        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                main_loop = False
            # If mouseclick on the New Game button, start the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and new_game_button:
                    new_game_button.click()
                    main_loop = False


# The function to run the main menu screen
def main_menu(screen):
    main_loop = True
    new_game_button.onclick = main_game
    new_game_button.args = (screen,)
    load_game_button.onclick = load_game
    load_game_button.args = (FILE_PATH, screen)
    while main_loop:
        CLOCK.tick(FPS)

        screen.fill(BACKGROUND_COLOR)
        title.draw(screen)
        new_game_button.draw(screen)
        load_game_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                main_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if new_game_button:
                    new_game_button.click()
                    main_loop = False
                # Load the saved game if click on Load Game button
                if load_game_button:
                    load_game_button.click()
                    main_loop = False


# Create the variable for the screen and start the game
window = pygame.display.set_mode((width + extra_space * 2, height + extra_space * 2))
pygame.display.set_caption("Connect Four")
main_menu(window)
pygame.quit()
