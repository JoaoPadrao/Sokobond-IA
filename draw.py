import pygame
import sys
import os
from boards import BOARDS, ATOM_MAPPING 
from elements import Atom, GridElement  
from constants import *  

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
        for index, item in enumerate(self.menu_items): #menu_items = ["Start Game", "Settings", "About", "Quit"]
            text = font.render(item, True, BLACK)
            ##The get_rect() method is called on the text object, which is a Pygame Surface object created from rendering text.
            #The get_rect() method returns a new rectangle that completely covers the surface
            text_rect = text.get_rect(center=(self.screen_width // 2, 300 + index * 50)) #center the text on the screen
            if index == self.selected_item:
                pygame.draw.rect(self.screen, ORANGE, (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))  
            self.screen.blit(text, text_rect)
            
    def handle_events(self): #for handling user interactions 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the user clicks the close button
                pygame.quit() #cleanly exit the Pygame
                sys.exit() #terminate the Python script
            elif event.type == pygame.KEYDOWN: #if the user presses a key
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN: #if the user presses the Enter key
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
  
class GameLevel(Game): #represents a level in a game
    def __init__(self, level_number):
        super().__init__()
        self.level_number = level_number
        self.level_data = BOARDS[level_number]  
        self.cell_size = CELL_SIZE
        self.atom_player_position = self.find_atom_player_position() 
        self.board_elements = self.create_board_elements()
        self.atom_player = self.get_atom_player()

    def find_atom_player_position(self): #iterates over the level data and returns the position of the player (represented by 'X') as a tuple of (x, y) coordinates
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == 'X':
                    return (x, y)
        return None  

    def get_atom_player(self):
        atom_mapping = ATOM_MAPPING.get(self.level_number) # get the atom mapping for the current level defined in game level function: def __init__(self, level_number)
        atom_player_attributes = atom_mapping.get('X') #por exemplo se level_number = 1, atom_mapping = {1: {'X' : [RED,1]}}
        #from class Atom (defined in elements.py) ->  def __init__(self, x, y, color,max_connection):
        return Atom(self.atom_player_position[0], self.atom_player_position[1], atom_player_attributes[0], atom_player_attributes[1])


    def create_board_elements(self):
        board_elements = []
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == '#':
                    board_elements.append(GridElement(x, y, DARK_YELLOW))
                elif cell == 'G':
                    board_elements.append(GridElement(x, y, GRAY))
                elif cell == 'H':
                    board_elements.append(Atom(x, y, RED,1))
                elif cell == 'O':
                    board_elements.append(Atom(x, y, BLUE,2))
                elif cell == 'C':
                    board_elements.append(Atom(x, y, DARK_YELLOW,4))
        return board_elements
    
    def draw(self):
        self.screen.fill(WHITE)
        
        for element in self.board_elements:
            element.draw(self.screen, self.cell_size)

        for y in range(0, self.screen.get_height(), self.cell_size):
            pygame.draw.line(self.screen, WHITE, (0, y), (self.screen.get_width(), y), 3)

        for x in range(0, self.screen.get_width(), self.cell_size):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, self.screen.get_height()), 3)

        # Draw connected atoms
        for connected_atom in self.atom_player.connection:
            # For each connected atom, it calls the draw method, passing in the game screen and the size of each cell
            connected_atom.draw(self.screen, self.cell_size)

        self.atom_player.draw(self.screen, self.cell_size)
        pygame.display.flip() #Pygame function that updates the entire display

   
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_atom_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_atom_player(1, 0)
                elif event.key == pygame.K_UP:
                    self.move_atom_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.move_atom_player(0, 1)
                elif event.key == pygame.K_b: #"if the user presses the 'b' key, the game will go back to the main menu"
                    goback = MainMenu()
                    goback.run()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def move_atom_player(self, dx, dy):
        new_x = self.atom_player.x + dx
        new_y = self.atom_player.y + dy

        if self.is_valid_move(self.atom_player, dx, dy): #vai verificar se a nova posção é valida para todos os atomos considerando o delta x e y
            #VERIFICAR PRIMEIRO SE HA UM ATOMO NA POSIÇÃO E SO DEPOIS ACTUALIZAR A POSIÇAO DO PLAYER
            
            #SINGLE ATOM CASE
            if len(self.atom_player.connection) == 0: #check if the player's atom is NOT connected to any other atoms
                #checks if there is an atom at the new position that can be connected to the player's atom
                atom = self.is_atom_connection(new_x, new_y) #estamos a adicionar uma conexao na mesma celula que o player ???
                if atom is not None and atom not in self.atom_player.connection:
                    #no updates on the player's position since there's an atom there
                    if self.atom_player.add_connection(atom): #adicionar nova conexao SE respeitar as condições
                        print("New atom connection:", self.atom_player.connection)
                else: #there's no atom at the new position
                    #updates the x and y coordinates of the player's atom to the new position
                    self.atom_player.x = new_x
                    self.atom_player.y = new_y

            #MOLECULE CASE
            elif len(self.atom_player.connection) > 0:
                #checks if there is an atom at the new position that can be connected to the molecule
                atom = self.is_atom_connection(new_x, new_y) #estamos a adicionar uma conexao na mesma celula que o player ???
                if atom is not None and atom not in self.atom_player.connection:
                    #no updates on the player's position since there's an atom there
                    if self.atom_player.add_connection(atom): #adicionar nova conexao se respeitar as condições
                        print("New connection to molecule:", self.atom_player.connection)
                else: #there's no atom at the new position
                    #updates the x and y coordinates of all atoms in the molecule to the new position
                    for connected_atom in self.atom_player.connection:
                        connected_atom.x += dx
                        connected_atom.y += dy
                        self.atom_player.x = new_x
                        self.atom_player.y = new_y      
        else:
            print("Invalid move")

    ############################################################ HERE
    def is_valid_move(self, atom, dx, dy, visited=None):
        if visited is None:
            visited = set()

        new_x = atom.x + dx
        new_y = atom.y + dy

        # Check if new position is outside the grid
        if new_x < 0 or new_x >= GRID_SIZE or new_y < 0 or new_y >= GRID_SIZE:
            print("Invalid move: Outside Grid")
            return False

        # Check if new position is a wall
        if self.level_data[new_y][new_x] == '#':
            print("Invalid move: Wall")
            return False

        # Check for all connected atoms
        for connected_atom in self.atom_player.connection:
            if connected_atom not in visited:
                visited.add(connected_atom)
                # Recursive call to check the move for each connected atom
                if not self.is_valid_move(connected_atom, dx, dy, visited):
                    print("Connected atom invalid move")
                    return False
        # If all checks pass, the move is valid
        return True

   
    #used to check if there's an atom at a specific location on the game board that can be connected to the player's atom
    def is_atom_connection(self, target_x, target_y):
        for element in self.board_elements: #iterates over the board elements and checks if there's an atom at the target location
            if isinstance(element, Atom) and element != self.atom_player and element.x == target_x and element.y == target_y:
                return element  #returning an atom object if it's found at the target location
        return None
    
    
  
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            pygame.display.update()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run()