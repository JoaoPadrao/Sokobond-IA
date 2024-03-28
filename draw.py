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
        self.trackMoves = []
        self.lastAtomConnected = [self.atom_player]

    def find_atom_player_position(self): #iterates over the level data and returns the position of the player (represented by 'X') as a tuple of (x, y) coordinates
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == 'X':
                    return (x, y)
        return None  

    def get_atom_player(self):
        atom_mapping = ATOM_MAPPING.get(self.level_number) # get the atom mapping for the current level defined in game level function: def __init__(self, level_number)
        atom_player_attributes = atom_mapping.get('X') #por exemplo se level_number = 1, atom_mapping = {1: {'X' : [RED,1]}}
        #from class Atom (defined in elements.py) -> (x, y, color, max_connection)
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


        for element in self.board_elements:
            if isinstance(element, Atom):
                element.draw(self.screen, self.cell_size)

        self.atom_player.draw(self.screen, self.cell_size)
        
        #game and atoms info
        font = pygame.font.Font(None, 24) # Initialize font

        info_x = 20
        info_y = 20

        game_info = {
            'Z': 'Press Z to undo connection',
            'I': ' ',
            'H': 'H (red): 1 bond',
            'O': 'O (blue): 2 bonds',
            'N': 'N (green): 3 bonds',
            'C': 'C (yellow): 4 bonds',
        }

        # Render and display each piece of text
        for atom_type, text in game_info.items():
            text_surface = font.render(text, True, (128,128,128))  # Black text
            self.screen.blit(text_surface, (info_x, info_y))
            info_y += 30  # Move down before rendering the next piece of text

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
                elif event.key == pygame.K_z:
                    self.undo_last_action() 
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def undo_last_action(self):
        if len(self.trackMoves) > 0:    
            if self.trackMoves[-1][0] == "connection":
                self.trackMoves[-1][1].remove_connection(self.trackMoves[-1][2])
                self.trackMoves.pop()

    def move_atom_player(self, dx, dy):

        if self.is_valid_move(self.atom_player, dx, dy): #vai verificar se a nova posção é valida para todos os atomos considerando o delta x e y
            #VERIFICAR PRIMEIRO SE HA UM ATOMO NA POSIÇÃO E SO DEPOIS ACTUALIZAR A POSIÇAO DO PLAYER

            #SINGLE ATOM CASE
            if len(self.atom_player.connection) == 0: #check if the player's atom is NOT connected to any other atoms
                #target position é em relação ao player
                new_x = self.atom_player.x + dx
                new_y = self.atom_player.y + dy
                #checks if there is an atom at the new position that can be connected to the player's atom
                atom = self.is_atom_connection(new_x, new_y) #estamos a adicionar uma conexao na mesma celula que o player ???
                if atom is not None and atom not in self.atom_player.connection:
                    #no updates on the player's position since there's an atom there
                    if self.atom_player.add_connection(atom): #adicionar nova conexao SE respeitar as condições
                        print("New atom connection:", self.atom_player.connection)
                        self.trackMoves.append(("connection", self.atom_player, atom))
                        self.lastAtomConnected.append(atom)
                    else: #PUSH the atom
                        print("Can not connect Atom")
                        valid_move = self.is_valid_move(atom, dx, dy)
                        if valid_move: ## Move the atom if the move is valid
                            self.update_positions(atom, dx, dy,set())
                            self.atom_player.x = new_x
                        self.atom_player.y = new_y

                else: #there's no atom at the new position
                    #updates the x and y coordinates of the player's atom to the new position
                    self.atom_player.x = new_x
                    self.atom_player.y = new_y

            #MOLECULE CASE
            elif len(self.atom_player.connection) > 0:
                #Gather all atoms in the molecule
                all_atoms = self.gather_molecule_atoms(self.atom_player)
                # Get a LIST of atoms on the edge of the molecule
                edge_atom = self.get_extreme_atoms(all_atoms, dx, dy)

                if len(edge_atom) == 1:
                    #target position é em relação ao edge_atom
                    print("One single edge")
                    new_x = edge_atom[0].x + dx
                    new_y = edge_atom[0].y + dy
                    #checks if there is an atom at the new position that can be connected to the edge_atom
                    atom = self.is_atom_connection(new_x, new_y)
                    if atom is not None and atom not in all_atoms:
                        #no updates on the player's position since there's an atom there
                        if edge_atom[0].add_connection(atom): #adicionar nova conexao se respeitar as condições
                            print("New molecule connection")
                            self.trackMoves.append(("connection", edge_atom[0], atom))
                            self.lastAtomConnected.append(atom)
                        else: #PUSH
                            print("Can not connect Atom")
                            valid_move = self.is_valid_move(atom, dx, dy)
                            if valid_move: ## Move the atom if the move is valid
                                self.update_positions(atom, dx, dy,set())
                                self.update_positions(edge_atom[0], dx, dy,set())
                    else: #there's no atom at the new position
                    #updates the x and y coordinates of all atoms in the molecule to the new position            
                        visited = set()
                        self.update_positions(self.atom_player, dx, dy, visited)

                elif len(edge_atom) > 1:
                    print("Multiple edge atoms")
                    atom_found = False
                    for atom_element in edge_atom:
                        #target position é em relação a todos os atomos na borda
                        new_x = atom_element.x + dx
                        new_y = atom_element.y + dy
                        #checks if there is an atom at the new position that can be connected
                        atom = self.is_atom_connection(new_x, new_y)
                        if atom is not None and atom not in all_atoms:
                            atom_found = True
                            if atom_element.add_connection(atom): #adicionar nova conexao se respeitar as condições
                                print("New molecule connection")
                                self.trackMoves.append(("connection", atom_element, atom))
                                self.lastAtomConnected.append(atom)
                            else:
                                print("Can not connect Atom")
                                valid_move = self.is_valid_move(atom, dx, dy)
                                if valid_move: ## Move the atom if the move is valid
                                    print("Atom is being pushed")
                                    self.update_positions(atom, dx, dy,set())
                                    self.update_positions(self.atom_player, dx, dy, set())
                    if not atom_found:
                        #updates the x and y coordinates of all atoms in the molecule to the new position            
                        visited = set()
                        self.update_positions(self.atom_player, dx, dy, visited)
                        #next: talvez for loop em todos os atomos da molecula?
                        #FOR ATOM IN ALL_ATOMS -> update_positions(atom, dx, dy, visited)

            # After all movements made, check if all connections are filled
            if self.check_all_connections_filled():
                self.show_message("Level complete! Press Enter to choose the next level.")
                ChooseLevel().run()

        else:
            print("No moves possible at the moment")

    ############################################################ AUX FUNCTIONS ############################################################
    #FUNCTION TO SHOW A POP-UP MESSAGE
    def show_message(self, message):

        font = pygame.font.Font(None, 26) # to define the font and size
        text = font.render(message, True, (255, 255, 255))  # render a white text
        # to define the text rectangle and position it at the center of the screen
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        # Draw a semi-transparent rectangle as the background of the pop-up
        background_rect = pygame.Rect(text_rect.x - 20, text_rect.y - 20, text_rect.width + 40, text_rect.height + 40)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), background_rect)  # Black semi-transparent background

        self.screen.blit(text, text_rect) # to draw (blit) the text on the screen

        pygame.display.flip()  # to update the display

        # Wait for the player to press Enter
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

    ### FUNCTION TO VERIFY IF CONNECTIONS IN ALL ATOMS ARE FILLED AND LEVEL OVER ###
    def check_all_connections_filled(self):
        # Iterate over all atom elements in the game grid
        for element in self.board_elements:
            # Check if the element is an instance of Atom
            if isinstance(element, Atom):
                # Check if the atom's connections are less than its max connections
                if len(element.connection) < element.max_connection:
                    # Found an atom that doesn't have all connections filled
                    return False
        # All atoms have their connections filled
        return True
        
    ### FUNCTION TO GATHER ALL ATOMS IN THE MOLECULE ###
    def gather_molecule_atoms(self, atom, visited=None):
        if visited is None:
            visited = set()
    
        visited.add(atom)
    
        for connected_atom in atom.connection:
            if connected_atom not in visited:
                self.gather_molecule_atoms(connected_atom, visited)
    
        return visited
        
    ### GET ATOM ON THE EDGE OF THE MOLECULE FUNCTIONS ###
    def get_extreme_atoms(self, atoms, dx, dy):
        if dx < 0:  # left (-1,0)
            min_x = min(atom.x for atom in atoms)
            return [atom for atom in atoms if atom.x == min_x]
        elif dx > 0:  # right (1,0)
            max_x = max(atom.x for atom in atoms)
            return [atom for atom in atoms if atom.x == max_x]
        elif dy < 0:  # up (0,-1)
            min_y = min(atom.y for atom in atoms)
            return [atom for atom in atoms if atom.y == min_y]
        else:  # down
            max_y = max(atom.y for atom in atoms)
            return [atom for atom in atoms if atom.y == max_y]

    ### UPDATE POSITIONS OF ALL ATOMS FUNCTIONS ###
    def update_positions(self, atom, dx, dy, visited):
        # Update the position of the current atom
        atom.x += dx
        atom.y += dy

        # Add the current atom to the set of visited atoms
        visited.add(atom)

        # Recursively update the positions of all connected atoms that haven't been visited yet
        for connected_atom in atom.connection:
            if connected_atom not in visited:
                self.update_positions(connected_atom, dx, dy, visited)        

    ### VALIDATE MOVES FUNCTIONS ###
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
        for connected_atom in atom.connection:
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