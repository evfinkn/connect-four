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
P1_COIN_COLOR = (255, 0, 0)
P2_COIN_COLOR = (255, 255, 0)
COLOR_NAMES = {P1_COIN_COLOR: "red", P2_COIN_COLOR: "yellow"}   # Dictionary of names of colors for winning color text

# Create the variables for the size of the grid, extra space on sides, and screen
slot_size = 50
width = slot_size * 7
extra_space = slot_size // 2
height = slot_size * 6

# Coin surfaces
coin_surfaces = {   # Dictionary for simplier access, with color as key and Surface as value
    P1_COIN_COLOR: pygame.Surface((slot_size, slot_size)),
    P2_COIN_COLOR: pygame.Surface((slot_size, slot_size)),
    BACKGROUND_COLOR: pygame.Surface((slot_size, slot_size))
}
for coin_color, coin_surface in coin_surfaces.items():  # Make surfaces transparent and draw the coin on it
    coin_surface.fill(BACKGROUND_COLOR)
    coin_surface.set_colorkey(BACKGROUND_COLOR)
    pygame.draw.circle(
        coin_surface, coin_color,
        (slot_size // 2, slot_size // 2),
        (slot_size // 2) - (slot_size // 20)
    )

# slot_surface is
slot_surface = pygame.Surface((slot_size, slot_size))   # one empty square of the board, used to form GRID_SURFACE
slot_surface.fill(GRID_COLOR)
pygame.draw.circle(
    slot_surface, BACKGROUND_COLOR,
    (slot_size // 2, slot_size // 2),
    (slot_size // 2) - (slot_size // 20)
)
GRID_SURFACE = pygame.Surface((width, height))      # The actual Connect Four board
GRID_SURFACE.fill(BACKGROUND_COLOR)
GRID_SURFACE.set_colorkey(BACKGROUND_COLOR)
for x in range(6):
    for y in range(7):
        GRID_SURFACE.blit(slot_surface, (slot_size * y, slot_size * x))

title = pygameutil.Text(
    (pygame.font.get_default_font(), slot_size), "Connect Four", GRID_COLOR,
    center=((width + extra_space * 2) // 2, (height + extra_space * 2) // 4)
)

BUTTON_FONT = pygame.font.Font(pygame.font.get_default_font(), slot_size // 2)

# Creating the button for starting a new game
new_game_text = pygameutil.Text(
    BUTTON_FONT, "New Game", BACKGROUND_COLOR,
    center=((width + extra_space * 2) // 2, (height + extra_space * 2) // 2)
)
new_game_rect = pygame.Rect(
    (width + extra_space * 2) // 2 - int(slot_size * 1.5),
    (height + extra_space * 2) // 2 - extra_space, slot_size * 3, slot_size
)
new_game_button = pygameutil.Button(new_game_text, new_game_rect, GRID_COLOR, LIGHTER_GRID_COLOR)

# Creating the button for loading the game
load_game_text = pygameutil.Text(
    BUTTON_FONT, "Load Game", BACKGROUND_COLOR,
    center=((width + extra_space * 2) // 2, (height + extra_space * 2) // 2 + extra_space * 3)
)
load_game_rect = pygame.Rect(
    (width + extra_space * 2) // 2 - int(slot_size * 1.5),
    (height + extra_space * 2) // 2 + extra_space * 2, slot_size * 3, slot_size
)
load_game_button = pygameutil.Button(load_game_text, load_game_rect, GRID_COLOR, LIGHTER_GRID_COLOR)

CLOCK = pygame.time.Clock()
FPS = 60


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
        if (board[i1][j1]
                == board[i1 + change_i][j1 + change_j]
                == board[i1 + (2 * change_i)][j1 + (2 * change_j)]
                == board[i2][j2]):
            return {
                "color": COLOR_NAMES[board[i][j]],
                "point1": ((j1 + 1) * slot_size, (i1 + 1) * slot_size),
                "point2": ((j2 + 1) * slot_size, (i2 + 1) * slot_size)
            }
        return None

    for i in range(len(board) - 1, -1, -1):
        for j in range(len(board[i]) - 1, -1, -1):
            if board[i][j] == BACKGROUND_COLOR:
                continue    # prevents another indentation level
            # The if statements prevent out of bounds errors
            if i <= 2:
                if (win := compare_coins(i, j, i + 3, j)) is not None:    # vertical win
                    return win
                elif j <= 3 and (win := compare_coins(i, j, i + 3, j + 3)) is not None:  # Negative slope diagonal win
                    return win
                elif j >= 3 and (win := compare_coins(i, j, i + 3, j - 3)) is not None:  # Positive slope diagonal win
                    return win
            elif j <= 3 and (win := compare_coins(i, j, i, j + 3)) is not None:     # Horizontal win
                return win
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
                elif load_game_button:
                    load_game_button.click()
                    main_loop = False


# The main game function
def main_game(screen, board=None):
    if board is None:
        board = [[BACKGROUND_COLOR for _ in range(7)] for _ in range(6)]
    board_surface = GRID_SURFACE.copy()
    for i in range(6):
        for j in range(7):
            board_surface.blit(coin_surfaces[board[i][j]], (slot_size * j, slot_size * i))
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
                    board_surface.blit(coin_surfaces[board[spot[0]][spot[1]]], (slot_size * spot[1], slot_size * spot[0]))
                    turn *= -1
        screen.fill(BACKGROUND_COLOR)
        # Draw the coin hovering at the top of the screen
        screen.blit(coin_surfaces[current_color], (pygame.mouse.get_pos()[0] - slot_size // 2, -extra_space))
        screen.blit(board_surface, (extra_space, extra_space))
        pygame.display.flip()
        if (win := find_win(board)) is None:
            continue
        try:
            os.remove(FILE_PATH)    # delete save file because game has been won
        except FileNotFoundError:
            pass    # file already doesn't exist, so we don't need to do anything
        winning_surface = screen.copy()
        pygame.draw.line(winning_surface, BACKGROUND_COLOR, win["point1"], win["point2"], 5)
        pygame.draw.circle(     # draws over the hovering coin at top of screen since game is over
            winning_surface, BACKGROUND_COLOR,
            (pygame.mouse.get_pos()[0], 0),
            (slot_size // 2) - (slot_size // 20)
        )
        win_screen(screen, winning_surface, win["color"])
        main_loop = False


# The function to run the win screen
def win_screen(screen, winning_surface, winner):
    main_loop = True
    while main_loop:
        screen.fill(BACKGROUND_COLOR)       # reset the screen to be redraw
        screen.blit(winning_surface, (0, 0))    # draw the board from when the game was won
        new_game_button.draw(screen)
        pygame.display.flip()      # updates the screen to display what was drawn

        CLOCK.tick(FPS)
        for event in pygame.event.get():
            # if the user quits, exit the loop
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                main_loop = False
            # If mouseclick on the New Game button, start the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and new_game_button:
                    new_game_button.click()
                    main_loop = False


# Create the variable for the screen and start the game
window = pygame.display.set_mode((width + extra_space * 2, height + extra_space * 2))
pygame.display.set_caption("Connect Four")
main_menu(window)
pygame.quit()
