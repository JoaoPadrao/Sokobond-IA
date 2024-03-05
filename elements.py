import pygame
from constants import *

# Class for the Atom object
class Atom:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.target_x = x  # Target x-coordinate for animation
        self.target_y = y  # Target y-coordinate for animation
        self.animation_speed = 0.1  # Speed of animation (adjust as needed)

    def draw(self, screen, cell_size):
        pygame.draw.circle(screen, self.color, (self.x * cell_size + cell_size // 2, self.y * cell_size + cell_size // 2), cell_size // 3)  # Draw a circle in the center of the cell

    def move(self, dx, dy):
        self.target_x = self.x + dx
        self.target_y = self.y + dy

    def update(self):
        # Update position gradually towards the target position
        if self.x < self.target_x:
            self.x += min(self.target_x - self.x, self.animation_speed)
        elif self.x > self.target_x:
            self.x -= min(self.x - self.target_x, self.animation_speed)
        if self.y < self.target_y:
            self.y += min(self.target_y - self.y, self.animation_speed)
        elif self.y > self.target_y:
            self.y -= min(self.y - self.target_y, self.animation_speed)

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
