import pygame
import sys

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
DARK_YEALLOW = (255, 212, 82)

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
            elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                player_pos[0] -= 1
            elif event.key == pygame.K_RIGHT and player_pos[0] < GRID_SIZE - 1:
                player_pos[0] += 1
            elif event.key == pygame.K_UP and player_pos[1] > 0:
                player_pos[1] -= 1
            elif event.key == pygame.K_DOWN and player_pos[1] < GRID_SIZE - 1:
                player_pos[1] += 1

    # Fill the window with background color
    WINDOW.fill(WHITE)

    # Draw the custom board
    for y, row in enumerate(custom_board):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(WINDOW, DARK_YEALLOW, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == 'G':
                pygame.draw.rect(WINDOW, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == 'H':
                pygame.draw.rect(WINDOW, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == 'O':
                pygame.draw.rect(WINDOW, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw horizontal grid lines
    for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
        pygame.draw.line(WINDOW, WHITE, (0, y), (WINDOW_SIZE[0], y),3)
    
    # Draw vertical grid lines
    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
        pygame.draw.line(WINDOW, WHITE, (x, 0), (x, WINDOW_SIZE[1]),3)

    # Draw the player (is the X in the custom board)
    player_rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(WINDOW, BLUE, player_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
