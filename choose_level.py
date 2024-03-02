import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = (600, 400)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Choose Level")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)

# Define font
font = pygame.font.Font(None, 36)

# Define available levels
LEVELS = 10

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Main loop
def choose_level():
    selected_level = None

    while not selected_level:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click is within any of the level buttons
                for level in range(1, LEVELS + 1):
                    if level_rects[level].collidepoint(event.pos):
                        selected_level = level
                        break

        WINDOW.fill(WHITE)
        draw_text("Choose a Level", font, BLACK, WINDOW, 20, 20)

        # Draw level buttons
        level_rects = {}
        for level in range(1, LEVELS + 1):
            button_rect = pygame.Rect(50, 50 + level * 30, 100, 25)
            level_rects[level] = button_rect
            pygame.draw.rect(WINDOW, GRAY, button_rect)
            draw_text(f"Level {level}", font, BLACK, WINDOW, button_rect.x + 10, button_rect.y + 5)

        pygame.display.update()

    # Return the selected level
    return selected_level

# Example usage
if __name__ == "__main__":
    selected_level = choose_level()
    print("Selected level:", selected_level)

    # Call main.py with the selected level
    subprocess.run(["python", "game.py", str(selected_level)])
