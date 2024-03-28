import pygame
from constants import *

# Class for the Atom object
class Atom:
    def __init__(self, x, y, color,max_connection):
        self.x = x  #atom's x position
        self.y = y  #atom's y position
        self.color = color
        self.max_connection = max_connection #H: 1, O: 2, N: 3 C: 4
        self.target_x = x  
        self.target_y = y 
        self.connection = [] #list of atoms that are connected to this atom

    def add_connection(self, atom):
        if (atom in self.connection or len(self.connection) >= self.max_connection or len(atom.connection) >= atom.max_connection):
            return False  
        elif (len(self.connection) < self.max_connection and len(atom.connection) < atom.max_connection):
            self.connection.append(atom)
            atom.connection.append(self)
            print("Connection successfully added")
            return True  

    def remove_connection(self, atom):
        if atom in self.connection: # Remove the connection from both atoms
            self.connection.remove(atom)
            atom.connection.remove(self)

    #draws the atom on the screen and the number of connections it has
    def draw(self, screen, cell_size):
        pygame.draw.circle(screen, self.color, (self.x * cell_size + cell_size // 2, self.y * cell_size + cell_size // 2), cell_size // 3)  # Draw a circle in the center of the cell
        font = pygame.font.Font(None, 24)
        connection_text = font.render(str(len(self.connection)), True, WHITE)
        text_rect = connection_text.get_rect(center=(self.x * cell_size + cell_size // 2, self.y * cell_size + cell_size // 2))
        screen.blit(connection_text, text_rect)
        
    def move(self, dx, dy):
        self.target_x = self.x + dx
        self.target_y = self.y + dy

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y

    def get_position(self):
        return (self.x, self.y)


# Class for the GridElement object
class GridElement:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen, cell_size):
        pygame.draw.rect(screen, self.color, (self.x * cell_size, self.y * cell_size, cell_size, cell_size))

    def get_position(self):
        return (self.x, self.y)
