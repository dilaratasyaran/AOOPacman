import pygame
from vectors import Vector2D
from constants import *
from numpy import loadtxt


class Pellet(object):
    def __init__(self, row, column):
        self.position = Vector2D(column * gridW, row * gridH)
        self.radius = 4

    def render(self, screen):
        pygame.draw.circle(screen, YELLOW, self.position.toTuple(), self.radius)


class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.radius = 8


class PelletGroup(object):
    def __init__(self):
        self.pelletList = []

    def createPelletListFromFile(self, filename):
        self.grid = loadtxt(filename, dtype=str)
        rows, cols = self.grid.shape
        for row in range(rows):
            for col in range(cols):
                if (self.grid[row][col] == "p" or
                        self.grid[row][col] == "n"):
                    self.pelletList.append(Pellet(row, col))
                if (self.grid[row][col] == "P" or
                        self.grid[row][col] == "N"):
                    self.pelletList.append(PowerPellet(row, col))

    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)
