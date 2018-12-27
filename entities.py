import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *


class DynamicEntity(object):
    def __init__(self, node):
        self.node = node
        self.target = node
        self.direction = STOP
        self.speed = 100
        self.setPosition()
        self.keyDown = False
        self.color = (255, 255, 255)

    def setPosition(self):
        self.position = Vector2D(self.node.position.x, self.node.position.y)

    def continueDirection(self):
        '''When reaching a node, continue past the node if it
        is attached to another node in the same direction'''
        if self.direction == UP:
            self.getNextTarget(UP)
        elif self.direction == DOWN:
            self.getNextTarget(DOWN)
        elif self.direction == LEFT:
            self.getNextTarget(LEFT)
        elif self.direction == RIGHT:
            self.getNextTarget(RIGHT)
        else:
            self.restOnNode()

    def getNextTarget(self, direction):
        '''Get the next target as specified by the direction'''
        key = direction
        if self.node.neighbors[key] is not None:
            self.target = self.node.neighbors[key]
        else:
            self.restOnNode()

    def reverseDirection(self):
        tempNode = self.node
        self.node = self.target
        self.target = tempNode
        self.direction *= -1

    def overshotTarget(self):
        '''Returns True if moved passed target, False otherwise'''
        vec1 = self.target.position - self.node.position
        vec2 = self.position - self.node.position
        nodeToTarget = vec1.magnitudeSquared()
        nodeToSelf = vec2.magnitudeSquared()
        return nodeToSelf > nodeToTarget

    def restOnNode(self):
        '''Rest on self.node'''
        self.setPosition()
        self.direction = STOP

    def render(self, screen):
        px = int(self.position.x)
        py = int(self.position.y)
        pygame.draw.circle(screen, self.color, (px, py), 16)

