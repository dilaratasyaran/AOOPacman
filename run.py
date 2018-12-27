import pygame
from pygame.locals import *
from pacman import PacMan
from ghost import *
from nodes import NodeGroup
from pellets import PelletGroup
from constants import *

# gridUnit = 16 #16 square pixels
pygame.init()
# SCREENSIZE = (600, 400)
# SCREENSIZE = (28*gridUnit, 36*gridUnit)
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
clock = pygame.time.Clock()
x, y = (300, 200)
background = pygame.surface.Surface(SCREENSIZE).convert()
background.fill((0, 0, 0))

nodes = NodeGroup()
# nodes.createNodeListManually()
nodes.createNodeListFromFile("maze1.txt")
pellets = PelletGroup()
pellets.createPelletListFromFile("maze1.txt")

pacman = PacMan(nodes.nodeList[0])
ca = ChaseAggresive()
stl = ScatterTopLeft()
blinky = Blinky(nodes.nodeList[17], ca, stl)
ca2 = ChaseAmbush()
stl2 = ScatterTopRight()
pinky = Pinky(nodes.nodeList[17], ca2, stl2)
ca3 = ChasePatrol()
stl3 = ScatterBottomLeft()
inky = Inky(nodes.nodeList[17], ca3, stl3)
ca4 = RandomChase()
stl4 = ScatterBottomRight()
clyde = Clyde(nodes.nodeList[17], ca4, stl4)


scatterTime = 7
chaseTime = 20
dt = 0
mode = "scatter"

while True:
    time_passed = clock.tick(30) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pacman.get_pacman().update(time_passed)
    blinky.update(time_passed)
    inky.update(time_passed)
    pinky.update(time_passed)
    clyde.update(time_passed)

    dt += time_passed
    if mode == "scatter":
        if dt >= scatterTime:
            dt = 0
            mode = "chase"
    elif mode == "chase":
        if dt >= chaseTime:
            mode = "scatter"
            dt = 0

    # print mode
    if mode == "chase":
        blinky.perform_chase(pacman.get_pacman())
        inky.perform_chase(pacman.get_pacman())
        pinky.perform_chase(pacman.get_pacman())
        clyde.perform_chase(pacman.get_pacman())
    elif mode == "scatter":
        blinky.perform_scatter()
        inky.perform_scatter()
        pinky.perform_scatter()
        clyde.perform_scatter()

    screen.blit(background, (0, 0))
    nodes.render(screen)
    pellets.render(screen)
    pacman.get_pacman().render(screen)
    blinky.render(screen)
    inky.render(screen)
    pinky.render(screen)
    clyde.render(screen)
    pygame.display.update()

