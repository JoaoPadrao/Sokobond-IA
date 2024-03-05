import pygame
import sys
from elements import Atom, GridElement  # Import the Atom and GridElement classes

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = (1000, 600)
GRID_SIZE = 20
CELL_SIZE = WINDOW_SIZE[0] // GRID_SIZE
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sokobond")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (240, 240, 240)
DARK_YELLOW = (255, 212, 82)

# Define player position (starting at the center)
player_pos = [9, 9]  # Set player position based on your custom board

# Define custom board
custom_board = [
    "....................",
    "........###.........",
    ".......##X##........",
    "......##GGG##.......",
    ".....##GHGHG##......",
    ".....#GGGGGGG#......",
    ".....##GHGHG##......",
    "......##GGG##.......",
    ".......##G##........",
    "........###.........",
    "....................",
    "....................",
]

# Convert custom board to Atom objects and GridElement objects
board_elements = []
for y, row in enumerate(custom_board):
    for x, cell in enumerate(row):
        if cell == '#':
            board_elements.append(GridElement(x, y, DARK_YELLOW))
        elif cell == 'G':
            board_elements.append(GridElement(x, y, GRAY))
        elif cell == 'H':
            board_elements.append(Atom(x, y, RED))
        elif cell == 'O':
            board_elements.append(Atom(x, y, BLUE))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                # Calculate the next position based on the key pressed
                next_pos = player_pos[:]
                if event.key == pygame.K_LEFT:
                    next_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    next_pos[0] += 1
                elif event.key == pygame.K_UP:
                    next_pos[1] -= 1
                elif event.key == pygame.K_DOWN:
                    next_pos[1] += 1
                
                # Check if the next position collides with a wall
                if custom_board[next_pos[1]][next_pos[0]] != '#':
                    player_pos = next_pos  # Move the player only if there's no collision

    # Fill the window with background color
    WINDOW.fill(WHITE)

    # Draw the custom board
    for element in board_elements:
        element.draw(WINDOW, CELL_SIZE)

    # Draw horizontal grid lines
    for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
        pygame.draw.line(WINDOW, WHITE, (0, y), (WINDOW_SIZE[0], y), 3)

    # Draw vertical grid lines
    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
        pygame.draw.line(WINDOW, WHITE, (x, 0), (x, WINDOW_SIZE[1]), 3)

    # Draw the player (is the X in the custom board)
    player_rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(WINDOW, BLUE, player_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

