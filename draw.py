import pygame
import sys
import os
from boards import BOARDS  # Import predefined levels from boards.py
from elements import Atom, GridElement  # Import the Atom and GridElement classes

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (240, 240, 240)
DARK_YELLOW = (255, 212, 82)

WINDOW_SIZE = (1000, 600)
GRID_SIZE = 20
CELL_SIZE = WINDOW_SIZE[0] // GRID_SIZE

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
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
                        print("Settings")
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
                    level_number = self.selected_level + 1
                    game_level = GameLevel(level_number)    
                    game_level.run()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def run(self):
        running = True
        while running:
            running =self.handle_events()
            self.draw()
            pygame.display.update()
    
class GameLevel(Game):
    def __init__(self, level_number):
        super().__init__()
        self.level_number = level_number
        self.level_data = BOARDS[level_number]  
        self.cell_size = CELL_SIZE
        self.player_position = self.find_player_position() 
        self.boad_elements = self.create_board_elements()
        self.player = Atom(self.player_position[0], self.player_position[1],DARK_YELLOW )

    def find_player_position(self):
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == 'X':
                    return (x, y)
        return None  # Return None if player position is not found

    def create_board_elements(self):
        board_elements = []
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == '#':
                    board_elements.append(GridElement(x, y, DARK_YELLOW))
                elif cell == 'G':
                    board_elements.append(GridElement(x, y, GRAY))
                elif cell == 'H':
                    board_elements.append(Atom(x, y, RED))
                elif cell == 'O':
                    board_elements.append(Atom(x, y, BLUE))

        return board_elements
    
    def draw(self):
        self.screen.fill(WHITE)
        for element in self.boad_elements:
            element.draw(self.screen, self.cell_size)

        for y in range(0, self.screen.get_height(), self.cell_size):
            pygame.draw.line(self.screen, WHITE, (0, y), (self.screen.get_width(), y), 3)

        for x in range(0, self.screen.get_width(), self.cell_size):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, self.screen.get_height()), 3)



        #draw the player
        self.player.draw(self.screen, self.cell_size)

        pygame.display.flip()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True


    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            pygame.display.update()

# Main entry point
if __name__ == "__main__":
    menu = MainMenu()
    menu.run()