import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *
from entities import DynamicEntity


class PacMan(DynamicEntity):
    __instance = None
    @staticmethod
    def get_pacman():
        if PacMan.__instance is None:
            PacMan()
        return PacMan.__instance

    def __init__(self, node):
        if PacMan.__instance is not None:
            raise Exception("Singleton Error")
        else:
            PacMan.__instance = self
        DynamicEntity.__init__(self, node)
        self.color = (255, 255, 0)

    def update(self, dt):
        self.position += self.direction * self.speed * dt
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            self.move(UP)
        elif key_pressed[K_DOWN]:
            self.move(DOWN)
        elif key_pressed[K_LEFT]:
            self.move(LEFT)
        elif key_pressed[K_RIGHT]:
            self.move(RIGHT)
        else:  # invalid or no key press
            overshot = self.overshotTarget()
            if overshot:
                self.node = self.target
                if self.node.portalNode:
                    self.node = self.node.portalNode
                    self.position = self.node.position
                self.continueDirection()

    def move(self, direction):
        keyedDirection = direction
        if self.direction == STOP:
            if self.node.neighbors[keyedDirection] is not None:
                self.direction = keyedDirection
                self.target = self.node.neighbors[keyedDirection]
        if self.direction == keyedDirection * -1:
            self.reverseDirection()
        overshot = self.overshotTarget()
        if overshot:
            self.node = self.target
            if self.node.portalNode:
                self.node = self.node.portalNode
                self.position = self.node.position
            if self.node.neighbors[keyedDirection] is not None:
                if self.direction is not keyedDirection:
                    self.restOnNode()
                self.direction = keyedDirection
                self.target = self.node.neighbors[keyedDirection]
            else:
                self.continueDirection()



