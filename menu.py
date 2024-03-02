import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = (1000, 600)
GRID_SIZE = 8  # 8x8 grid for simplicity
CELL_SIZE = WINDOW_SIZE[0] // GRID_SIZE
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sokobond")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)

# Define menu options
menu_font = pygame.font.Font(None, 36)
menu_options = ["Start Game", "Settings", "About", "Quit"]
selected_option = 0

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
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:  # Start Game
                    print("Starting game...")
                    exec(open('choose_level.py').read())
                elif selected_option == 1:  # Settings
                    print("Opening settings...")
                elif selected_option == 2:  # About
                    print("About Sokobond...")
                elif selected_option == 3:  # Quit
                    running = False

    # Fill the window with background color
    WINDOW.fill(WHITE)

    # Draw menu options
    for i, option in enumerate(menu_options):
        text = menu_font.render(option, True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + i * 50))
        if i == selected_option:
            pygame.draw.rect(WINDOW, ORANGE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
        WINDOW.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
