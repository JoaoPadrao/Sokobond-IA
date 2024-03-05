import pygame
import sys
from constants import *

class Menu:
    def __init__(self, options, font_size=36):
        self.options = options
        self.selected_option = 0
        self.font = pygame.font.Font(None, font_size)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_option
        return None     

    def draw(self, screen, window_size):
        screen.fill((255, 255, 255))  

        # Draw menu options
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0))  
            text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 + i * 50))
            if i == self.selected_option:
                pygame.draw.rect(screen, ORANGE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))  # Orange border
            screen.blit(text, text_rect)

    def get_selected_option(self):
        return self.selected_option

class SettingsMenu(Menu):
    def __init__(self, options):
        super().__init__(options, font_size=24)

    def draw(self, screen, window_size):
        super().draw(screen, window_size)
        text = self.font.render("Settings Menu", True, (0, 0, 0))
        text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 100))
        screen.blit(text, text_rect)
    

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the window
    window_size = (1000, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Sokobond")

    # Define menu options
    menu = Menu(["Start Game", "Settings", "About", "Quit",])

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle menu input
            selected_option = menu.handle_input(event)
            if selected_option is not None:
                if selected_option == 0:  # Start Game
                    print("Starting game...")
                    # Call your game initialization function here
                    menu = SettingsMenu(["Option 1", "Option 2", "Option 3"])
                    menu.draw(window, window_size)
                    #if click option do fullscreen
                    if selected_option == 0:
                        pygame.display.toggle_fullscreen()
                elif selected_option == 1:  # Settings
                    print("Opening settings...")
                elif selected_option == 2:  # About
                    print("About Sokobond...")
                elif selected_option == 3:  # Quit
                    running = False

        # Draw menu
        menu.draw(window, window_size)
        
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
