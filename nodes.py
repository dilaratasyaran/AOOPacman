"""Position is just an (x, y) position in a grid.  Width and height are the width and height of a single grid unit.  So if the inputted position is (3,5) that refers to the 3rd column and 5th row.  To get actual pixel position you need to multiply by the width and height of the grid unit."""
import pygame
from vectors import Vector2D
from numpy import loadtxt
from stacks import Stack
from constants import *

class Node(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}
        self.target = None
        self.position = Vector2D(self.col*gridW, self.row*gridH)
        self.visited = False
        self.portalNode = None

    def render(self, screen):
        '''Draw the nodes and the links between nodes'''
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                pygame.draw.line(screen, RED, \
                                 self.position.toTuple(), \
                                 self.neighbors[n].position.toTuple(), 2)
        pygame.draw.circle(screen, RED, self.position.toTuple(), 10)


class NodeGroup(object):
    def __init__(self):
        '''width and height are the minimum distance between nodes'''
        self.nodeList = []
        self.grid = None
        self.nodeStack = Stack()
        self.fRows = 0
        self.fCols = 0

    def getNode(self, row, col):
        '''Get the node from the nodeList given the row and col'''
        for node in self.nodeList:
            if node.row == row and node.col == col:
                return node
        return None

    def getNodeFromNode(self, node):
        '''Checks list of node already exists, if so get that node.
           If node does not exist, then return the input node'''
        if node is not None:
            for inode in self.nodeList:
                if node.row == inode.row and node.col == inode.col:
                    return inode
        return node

    def findFirstNodeInGrid(self, rows, cols):
        '''Searches grid until it runs into a node, return that Node'''
        nodeFound = False
        for row in range(rows):
            for col in range(cols):
                if (self.grid[row][col] == "+" or
                    self.grid[row][col] == "n" or
                    self.grid[row][col] == "N"):
                    return Node(row, col)
        return None

    def addNode(self, node):
        '''Add a node to the nodeList if not already in the list'''
        nodeInList = self.nodeInList(node)
        if not nodeInList:
            self.nodeList.append(node)

    def nodeInList(self, node):
        '''Return True if the node is already in nodeList'''
        for inode in self.nodeList:
            if node.row == inode.row and node.col == inode.col:
                return True
        return False

    def createNodeListFromFile(self, filename):
        '''Creates a connected nodelist from a properly formatted file'''
        self.grid = loadtxt(filename, dtype=str)
        self.fRows, self.fCols = self.grid.shape
        startNode = self.findFirstNodeInGrid(self.fRows, self.fCols)
        self.nodeStack.push(startNode)
        print(self.grid.shape)
        while not self.nodeStack.isEmpty():
            node = self.nodeStack.pop()
            self.addNode(node)
            leftNode = self.followPath(LEFT, node.row, node.col)
            rightNode = self.followPath(RIGHT, node.row, node.col)
            upNode = self.followPath(UP, node.row, node.col)
            downNode = self.followPath(DOWN, node.row, node.col)
            leftNode = self.getNodeFromNode(leftNode)
            rightNode = self.getNodeFromNode(rightNode)
            upNode = self.getNodeFromNode(upNode)
            downNode = self.getNodeFromNode(downNode)
            node.neighbors[LEFT] = leftNode
            node.neighbors[RIGHT] = rightNode
            node.neighbors[UP] = upNode
            node.neighbors[DOWN] = downNode
            if leftNode is not None and not self.nodeInList(leftNode):
                self.nodeStack.push(leftNode)
            if rightNode is not None and not self.nodeInList(rightNode):
                self.nodeStack.push(rightNode)
            if upNode is not None and not self.nodeInList(upNode):
                self.nodeStack.push(upNode)
            if downNode is not None and not self.nodeInList(downNode):
                self.nodeStack.push(downNode)
        self.setupPortalNodes()


    def followPath(self, direction, row, col):
        if direction == LEFT and col-1 >= 0:
            if (self.grid[row][col-1] == "-" or
                self.grid[row][col-1] == "+" or
                self.grid[row][col-1] == "p" or
                self.grid[row][col-1] == "P"):
                while (self.grid[row][col-1] != "+" and
                       self.grid[row][col-1] != "n" and
                       self.grid[row][col-1] != "N"):
                    col -= 1
                return Node(row, col-1)
            else:
                return None

        elif direction == RIGHT and col+1 < self.fCols:
            if (self.grid[row][col+1] == "-" or
                self.grid[row][col+1] == "+" or
                self.grid[row][col+1] == "p" or
                self.grid[row][col+1] == "P"):
                while (self.grid[row][col+1] != "+" and
                       self.grid[row][col+1] != "n" and
                       self.grid[row][col+1] != "N"):
                    col += 1
                return Node(row, col+1)
            else:
                return None

        elif direction == UP and row-1 >= 0:
            if (self.grid[row-1][col] == "|" or
                self.grid[row-1][col] == "+" or
                self.grid[row-1][col] == "p" or
                self.grid[row-1][col] == "P"):
                while (self.grid[row-1][col] != "+" and
                       self.grid[row-1][col] != "n" and
                       self.grid[row-1][col] != "N"):
                    row -= 1
                return Node(row-1, col)
            else:
                return None

        elif direction == DOWN and row+1 < self.fRows:
            if (self.grid[row+1][col] == "|" or
                self.grid[row+1][col] == "+" or
                self.grid[row+1][col] == "p" or
                self.grid[row+1][col] == "P"):
                while (self.grid[row+1][col] != "+" and
                       self.grid[row+1][col] != "n" and
                       self.grid[row+1][col] != "N"):
                    row += 1
                return Node(row+1, col)
            else:
                return None
        else:
            return None

    def setupPortalNodes(self):
        '''Manually set up the portal nodes'''
        portalNode1 = self.getNode(17, 0)
        portalNode2 = self.getNode(17, 27)
        portalNode1.portalNode = portalNode2
        portalNode2.portalNode = portalNode1

    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)
