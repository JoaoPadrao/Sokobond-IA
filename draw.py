import pygame
import sys
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sokobond")

class MainMenu(Game):
    def __init__(self):
        super().__init__()
        self.menu_items = ["Start Game", "Settings", "About", "Quit"]
        self.selected_item = 0
        self.background_image = pygame.image.load(os.path.join("data", "Sokobond.png")) 

    def draw(self):
        self.screen.fill(WHITE) 
        self.screen.blit(self.background_image, (self.screen_width // 2 - self.background_image.get_width() // 2, self.screen_height // 5 - self.background_image.get_height() // 2))
        font = pygame.font.Font(None, 36)
        for index, item in enumerate(self.menu_items):
            text = font.render(item, True, BLACK)
            text_rect = text.get_rect(center=(self.screen_width // 2, 300 + index * 50))
            if index == self.selected_item:
                pygame.draw.rect(self.screen, ORANGE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))  
            self.screen.blit(text, text_rect)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    if self.selected_item == 0:
                        choose_level = ChooseLevel()
                        choose_level.run()
                    elif self.selected_item == 1:
                        # Options menu
                        print("Options menu...")
                    elif self.selected_item == 3:
                        pygame.quit()
                        sys.exit()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.update()

class ChooseLevel(Game):
    def __init__(self):
        super().__init__()
        self.levels = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9", "Level 10"]
        self.selected_level = 0
        self.background_image = pygame.image.load(os.path.join("data", "Sokobond.png")) 

    def draw(self):
        self.screen.fill(WHITE) 
        self.screen.blit(self.background_image, (self.screen_width // 2 - self.background_image.get_width() // 2, self.screen_height // 5 - self.background_image.get_height() // 2))
        font = pygame.font.Font(None, 36)

        max_levels_visible = (self.screen_height - 100) // 50
        max_levels_per_column = max_levels_visible // 2

        # Draw 1-5 levels 
        for index in range(min(len(self.levels), max_levels_per_column)):
            level = self.levels[index]
            text = font.render(level, True, BLACK)
            text_rect = text.get_rect(center=(self.screen_width * 2 // 5, 300 + index * 50))
            if index == self.selected_level:
                pygame.draw.rect(self.screen, ORANGE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))  
            self.screen.blit(text, text_rect)

        # Draw 6-10 levels
        for index in range(min(len(self.levels) - max_levels_per_column, max_levels_per_column)):
            level = self.levels[index + max_levels_per_column]
            text = font.render(level, True, BLACK)
            text_rect = text.get_rect(center=(self.screen_width * 3 // 5, 300 + index * 50))
            if index + max_levels_per_column == self.selected_level:
                pygame.draw.rect(self.screen, ORANGE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))  
            self.screen.blit(text, text_rect)

            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_level = (self.selected_level - 1) % len(self.levels)
                elif event.key == pygame.K_DOWN:
                    self.selected_level = (self.selected_level + 1) % len(self.levels)
                elif event.key == pygame.K_RETURN:
                    print(f"Starting {self.levels[self.selected_level]}...")
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def run(self):
        running = True
        while running:
            running =self.handle_events()
            self.draw()
            pygame.display.update()
            
# Main entry point
if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
