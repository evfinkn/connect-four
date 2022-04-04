import pygame
# https://www.pygame.org
import random

pygame.init()
random.seed()

# Create the variables for the size of the grid, extra space on sides, and screen
slotSize = 180
width = slotSize * 7
extraSpace = slotSize // 2
height = slotSize * 6

backgroundColor = (255, 255, 255)
# Surface for the coins
ballSurface = pygame.Surface((slotSize, slotSize))
ballSurface.fill(backgroundColor)

# Create grid, colors, and surfaces
grid = [[backgroundColor for x in range(7)] for y in range(6)]
gridColor = (0, 0, 122)
lighterGridColor = (0, 37, 161)
# gridSurface is a square in the color of the grid. It is then blotted onto the screen later in the drawBackground function. This forms the Connect 4 board
gridSurface = pygame.Surface((slotSize, slotSize))
gridSurface.fill(gridColor)
gridSurface.set_colorkey(backgroundColor)
pygame.draw.circle(gridSurface, backgroundColor, (slotSize // 2, slotSize // 2), (slotSize // 2) - (slotSize // 20))
# This is the line that is placed where the win is
lineSurface = pygame.Surface((width + extraSpace * 2, height + extraSpace * 2))
lineSurface.fill(backgroundColor)
lineSurface.set_colorkey(backgroundColor)

# Variables for the title text
titleFont = pygame.font.Font("freesansbold.ttf", slotSize)
title = titleFont.render("Connect Four", True, gridColor)
titleRect = title.get_rect()
titleRect.center = ((width + extraSpace * 2) // 2, (height + extraSpace * 2) // 4)

# Font for the text on buttons
buttonFont = pygame.font.Font("freesansbold.ttf", slotSize // 2)
# The text for the new game button
textNGButton = buttonFont.render("New Game", True, backgroundColor)
textNGButtonRect = textNGButton.get_rect()
textNGButtonRect.center = ((width + extraSpace * 2) // 2, (height + extraSpace * 2) // 2)
# The text for the load game button
textLGButton = buttonFont.render("Load Game", True, backgroundColor)
textLGButtonRect = textLGButton.get_rect()
textLGButtonRect.center = ((width + extraSpace * 2) // 2, (height + extraSpace * 2) // 2 + extraSpace * 3)

# The clock and FPS
clock = pygame.time.Clock()
FPS = 60

# The screen where buttons will be drawn
menuScreen = pygame.Surface((width + extraSpace * 2, height + extraSpace * 2))
menuScreen.fill(backgroundColor)
menuScreen.set_colorkey(backgroundColor)

# The rects and colors for the buttons and color
ngButton = pygame.Rect((width + extraSpace * 2) // 2 - int(slotSize * 1.5), (height + extraSpace * 2) // 2 - extraSpace, slotSize * 3, slotSize)
colorNGButton = gridColor
lgButton = pygame.Rect((width + extraSpace * 2) // 2 - int(slotSize * 1.5), (height + extraSpace * 2) // 2 + extraSpace * 2, slotSize * 3, slotSize)
colorLGButton = gridColor


# Draw the board
def drawBackground(screen):
    for i in range(6):
        for j in range(7):
            screen.blit(gridSurface, (slotSize * j + extraSpace, slotSize * i + extraSpace))


# Draws the coins
def drawGrid(screen, grid):
    for i in range(6):
        for j in range(7):
            pygame.draw.circle(ballSurface, grid[i][j], (slotSize // 2, slotSize // 2), (slotSize // 2) - (slotSize // 20))
            screen.blit(ballSurface, (slotSize * j + extraSpace, slotSize * i + extraSpace))


# Draw the new/load game buttons
def drawButton(screen, buttons, buttonColors):
    for x in range(len(buttons)):
        pygame.draw.rect(screen, buttonColors[x], buttons[x])
    screen.blit(screen, (0, 0))


# Finds the spot that the coin is placed on mouse click
def findSpot(grid, mousePos):
    if extraSpace < mousePos[0] < width + extraSpace:
        column = (mousePos[0] + extraSpace) // slotSize - 1
        for i in range(len(grid) - 1, -1, -1):
            if grid[i][column] == backgroundColor:
                return i, column
    return -1


# Searches for any wins (4 coins next to each other vertically, horizontally, or diagonally)
def findWin(grid):
    for i in range(len(grid) - 1, -1, -1):
        for j in range(len(grid[i]) - 1, -1, -1):
            if grid[i][j] != backgroundColor:
                # The if statements prevent out of bounds errors from the list
                if i <= 2 and j <= 3:
                    # Compare the slots next to each other
                    if grid[i][j] == grid[i + 1][j + 1] == grid[i + 2][j + 2] == grid[i + 3][j + 3]:
                        # Return the necessary information for the winScreen function if a win is found
                        return (i * slotSize + extraSpace + slotSize / 2, j * slotSize + extraSpace + slotSize / 2), ((i + 3) * slotSize + extraSpace + slotSize / 2, (j + 3) * slotSize + extraSpace + slotSize / 2), grid[i][j]
                if i <= 2 and j >= 3:
                    if grid[i][j] == grid[i + 1][j - 1] == grid[i + 2][j - 2] == grid[i + 3][j - 3]:
                        return (i * slotSize + extraSpace + slotSize / 2, j * slotSize + extraSpace + slotSize / 2), ((i + 3) * slotSize + extraSpace + slotSize / 2, (j - 3) * slotSize + extraSpace + slotSize / 2), grid[i][j]
                if i <= 2:
                    if grid[i][j] == grid[i + 1][j] == grid[i + 2][j] == grid[i + 3][j]:
                        return (i * slotSize + extraSpace + slotSize / 2, j * slotSize + extraSpace + slotSize / 2), ((i + 3) * slotSize + extraSpace + slotSize / 2, j * slotSize + extraSpace + slotSize / 2), grid[i][j]
                if j <= 3:
                    if grid[i][j] == grid[i][j + 1] == grid[i][j + 2] == grid[i][j + 3]:
                        return (i * slotSize + extraSpace + slotSize / 2, j * slotSize + extraSpace + slotSize / 2), (i * slotSize + extraSpace + slotSize / 2, (j + 3) * slotSize + extraSpace + slotSize / 2), grid[i][j]
    return None


# Writes the grid to a file in order to save the game
def fileWriter(file):
    global grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            file.write(str(grid[i][j][0]) + "\n")
            file.write(str(grid[i][j][1]) + "\n")
            file.write(str(grid[i][j][2]) + "\n")


# Reads the file in order to load the game
def fileReader(file):
    global grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            red = int(file.readline()[:-1])
            green = int(file.readline()[:-1])
            blue = int(file.readline()[:-1])
            grid[i][j] = (red, green, blue)


# The main game function
def mainGame(screen):
    global grid
    file = open("grid.txt", "w")
    mainloop = True
    turn = random.choice((-1, 1))

    while mainloop:
        clock.tick(FPS)
        # Change the coin color depending on whose turn it is
        if turn == -1:
            coinColor = (255, 0, 0)
        else:
            coinColor = (255, 255, 0)
        pygame.draw.circle(ballSurface, coinColor, (slotSize // 2, slotSize // 2), (slotSize // 2) - (slotSize // 20))
        for event in pygame.event.get():
            # If the game is exited out of, save and end the game
            if event.type == pygame.QUIT:
                mainloop = False
                fileWriter(file)
                file.close()
            # If ESC is pressed, save and end the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                    fileWriter(file)
                    file.close()
            # If mouseclick, find the location and set that spot to the color of the coin if it's valid
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    spot = findSpot(grid, pygame.mouse.get_pos())
                    if spot != -1:
                        grid[spot[0]][spot[1]] = coinColor
                        turn *= -1
        # Reset the screen
        screen.fill(backgroundColor)
        # Draw the coin hovering at the top of the screen
        screen.blit(ballSurface, (pygame.mouse.get_pos()[0] - slotSize // 2, -extraSpace))
        drawGrid(screen, grid)
        drawBackground(screen)
        pygame.display.flip()
        winner = findWin(grid)
        if winner is not None:
            mainloop = False
    endingGrid = grid
    grid = [[backgroundColor for x in range(7)] for y in range(6)]
    fileWriter(file)
    file.close()
    winScreen(screen, endingGrid, winner[2], winner[0], winner[1])


# The function to run the win screen
def winScreen(screen, grid, winner, startPos, endPos):
    global colorNGButton
    mainloop = True
    while mainloop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
            # If mouseclick on the New Game button, start the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if ngButton.collidepoint(pos):
                        mainGame(screen)
                        return
        # Make the color of the button lighter if the mouse is over it
        pos = pygame.mouse.get_pos()
        if ngButton.collidepoint(pos):
            colorNGButton = lighterGridColor
        elif colorNGButton != gridColor:
            colorNGButton = gridColor

        screen.fill(backgroundColor)
        drawGrid(screen, grid)
        drawBackground(screen)
        pygame.draw.line(screen, backgroundColor, (startPos[1], startPos[0]), (endPos[1], endPos[0]), 5)
        drawButton(screen, [ngButton], [colorNGButton])
        screen.blit(textNGButton, textNGButtonRect)
        pygame.display.flip()


# The function to run the main menu screen
def mainMenu(screen):
    global colorNGButton, colorLGButton, grid
    mainloop = True
    while mainloop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if ngButton.collidepoint(pos):
                        mainGame(screen)
                        return
                    # Load the saved game if click on Load Game button
                    if lgButton.collidepoint(pos):
                        file = open("grid.txt", "r")
                        fileReader(file)
                        file.close()
                        mainGame(screen)
                        return

        pos = pygame.mouse.get_pos()
        if ngButton.collidepoint(pos):
            colorNGButton = lighterGridColor
        elif colorNGButton != gridColor:
            colorNGButton = gridColor
        if lgButton.collidepoint(pos):
            colorLGButton = lighterGridColor
        elif colorLGButton != gridColor:
            colorLGButton = gridColor

        screen.fill(backgroundColor)
        screen.blit(title, titleRect)
        drawButton(screen, [ngButton, lgButton], [colorNGButton, colorLGButton])
        screen.blit(textNGButton, textNGButtonRect)
        screen.blit(textLGButton, textLGButtonRect)
        pygame.display.flip()


# Create the variable for the screen and start the game
win = pygame.display.set_mode((width + extraSpace * 2, height + extraSpace * 2))
pygame.display.set_caption("Connect Four")
mainMenu(win)
pygame.quit()