from abc import ABC, abstractmethod

import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *
from entities import DynamicEntity
from random import randint


class Ghost(DynamicEntity):
    def __init__(self, node, chase_behaviour, scatter_behaviour):
        DynamicEntity.__init__(self, node)
        self.color = BLUE
        self.direction = RIGHT
        self.target = self.node.neighbors[self.direction]
        self.poi = Vector2D()
        self.chase_behaviour = chase_behaviour
        self.scatter_behaviour = scatter_behaviour
        self.frightened = Frightened
        self.radiusSquared = (gridUnit * 8) ** 2

    def update(self, dt):
        self.position += self.direction * self.speed * dt
        overshot = self.overshotTarget()
        if overshot:
            self.node = self.target
            if self.node.portalNode:
                self.node = self.node.portalNode
            self.position = self.node.position

            validDirections = self.getValidDirections()
            index = self.getClosestNode(validDirections)
            self.direction = validDirections[index]
            self.target = self.node.neighbors[self.direction]

    def move(self, direction):
        pass

    def getClosestNode(self, validDirections):
        distances = []
        for key in validDirections:
            diffVec = self.node.neighbors[key].position - self.poi
            distances.append(diffVec.magnitudeSquared())
        return distances.index(min(distances))

    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if not key == self.direction * -1:
                    validDirections.append(key)
        return validDirections

    def perform_chase(self, pacman):
        self.chase_behaviour.chase(pacman, self)

    def perform_scatter(self):
        self.scatter_behaviour.scatter(self)

    def perform_frightened(self):
        self.frightened.frightened()


class Blinky(Ghost):
    def __init__(self, node, chase_behaviour, scatter_behaviour):
        super().__init__(node, chase_behaviour, scatter_behaviour)
        self.color = RED


class Pinky(Ghost):
    def __init__(self, node, chase_behaviour, scatter_behaviour):
        Ghost.__init__(self, node, chase_behaviour, scatter_behaviour)
        self.color = PINK


class Inky(Ghost):
    def __init__(self, node, chase_behaviour, scatter_behaviour):
        Ghost.__init__(self, node, chase_behaviour, scatter_behaviour)
        self.color = TEAL


class Clyde(Ghost):
    def __init__(self, node, chase_behaviour, scatter_behaviour):
        Ghost.__init__(self, node, chase_behaviour, scatter_behaviour)
        self.color = ORANGE


class ChaseBehaviour(ABC):

    @abstractmethod
    def chase(self):
        raise NotImplementedError("Missing Chase Implementation.")


class ScatterBehaviour(ABC):

    @abstractmethod
    def scatter(self):
        raise NotImplementedError("Missing Scatter Implementation.")


class FrigtenedBehaviour(ABC):

    @abstractmethod
    def frightened(self):
        raise NotImplementedError("Missing Frightened Implementation.")


class ChaseAggresive(ChaseBehaviour):
    def chase(self, pacman, ghost):
        self.poi = pacman.position


class ChasePatrol(ChaseBehaviour):
    def chase(self, pacman, ghost):
        pass


        # vec1 = pacman.position + pacman.direction * gridUnit * 2
        # vec2 = vec1 - kwargs['blinky'].position
        # vec2 *= 2
        # self.poi = kwargs['blinky'].position + vec2


class ChaseAmbush(ChaseBehaviour):
    def chase(self, pacman, ghost):
        self.poi = pacman.position + pacman.direction * gridUnit * 4


class RandomChase(ChaseBehaviour):
    def chase(self, pacman, ghost):
        distanceVector = pacman.position - ghost.position
        distanceSquared = distanceVector.magnitudeSquared()
        if distanceSquared <= ghost.radiusSquared:
            ghost.scatter_behaviour.scatter()
        else:
            ghost.poi = pacman.position

class ScatterBottomLeft(ScatterBehaviour):
    def scatter(self, ghost):
        ghost.poi = Vector2D(0, 576)


class ScatterBottomRight(ScatterBehaviour):
    def scatter(self, ghost):
        ghost.poi = Vector2D(448, 576)


class ScatterTopLeft(ScatterBehaviour):
    def scatter(self, ghost):
        ghost.poi = Vector2D(448, 0)


class ScatterTopRight(ScatterBehaviour):
    def scatter(self, ghost):
        ghost.poi = Vector2D()


class Frightened(FrigtenedBehaviour):
    def frightened(self):
        pass