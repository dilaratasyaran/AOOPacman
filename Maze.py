import pygame
from pygame.locals import *
from tiles import Tile
from numpy import loadtxt
from pacman import PacMan

pygame.init()
layout = loadtxt('maze.txt', dtype=str)
rows, cols = layout.shape
width, height = (16, 16)
SCREEN_SIZE = (width*cols, height*rows)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
tiles = []
for col in range(cols):
    for row in range(rows):
        value = layout[row][col]
        if value != '0':
            pos = (col*width, row*height)
            tiles.append(Tile((width, height), pos))

background = pygame.surface.Surface(SCREEN_SIZE).convert()
background.fill((0,0,0))
pacman = PacMan((width,height), [32*2,32*4])

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    pacman.move()
    for tile in tiles:
        pacman.collide(tile)
    screen.blit(background, (0,0))
    for tile in tiles:
        tile.draw(screen)
    pacman.draw(screen)
    pygame.display.update()