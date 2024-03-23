import pygame
from constants import *

# Class for the Atom object
class Atom:
    def __init__(self, x, y, color,max_connection):
        self.x = x
        self.y = y
        self.color = color
        self.max_connection = max_connection
        self.target_x = x  
        self.target_y = y 
        self.connection = []

    def add_connection(self, atom):
        if self.max_connection > 0 and atom.max_connection > 0:
            self.connection.append(atom)
            atom.connection.append(self)
            self.max_connection -= 1
            atom.max_connection -= 1
    
    def remove_connection(self, atom):
        if atom in self.connection:
            self.connection.remove(atom)
            atom.connection.remove(self)
            self.max_connection += 1
            atom.max_connection += 1

    def draw(self, screen, cell_size):
        pygame.draw.circle(screen, self.color, (self.x * cell_size + cell_size // 2, self.y * cell_size + cell_size // 2), cell_size // 3)  # Draw a circle in the center of the cell
        font = pygame.font.Font(None, 24)
        connection_text = font.render(str(self.max_connection), True, BLACK)
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

# Class for the Molecule object
class Molecule:
    def __init__(self):
        self.atoms = []

    def add_atom(self, atom):
        self.atoms.append(atom)

    def remove_atom(self, atom):
        self.atoms.remove(atom)

    def move(self, dx, dy):
        for atom in self.atoms:
            atom.move(dx, dy)

    def draw(self, screen, cell_size):
        for atom in self.atoms:
            atom.draw(screen, cell_size)

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
