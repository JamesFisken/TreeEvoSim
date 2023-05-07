
import sys

import pygame
from pygame.locals import *
import random
import numpy as np
pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1000, 500
screen = pygame.display.set_mode((width, height))

gridSquareSize = 1

map = np.zeros(round(width/gridSquareSize) * round(height/gridSquareSize)).reshape(round(width/gridSquareSize), round(height/gridSquareSize))
print()
class Organism:
    def __init__(self, genome, totalEnergy):
        self.genome = genome
        self.totalEnergy = totalEnergy
        self.childCells = []
        self.toBeChildCells = []
    def display(self):
        for cell in self.childCells:
            cell.display()
    def update(self):
        for cell in self.childCells:
            cell.grow()
        self.childCells.extend(self.toBeChildCells)
        self.toBeChildCells = []


class Cell:
    def __init__(self, cellType, cellSize, x, y, energy, genome, activeGene, parentOrganism):
        self.activeGene = activeGene
        self.genome = genome
        self.cellType = cellType
        self.energy = energy

        self.parentOrganism = parentOrganism

        self.cellSize = cellSize
        self.x = x
        self.y = y


    def grow(self):
        if self.cellType == "outgrowth":
            gene = self.genome[self.activeGene]

            for i, n in enumerate(gene):
                fail = False
                if n < len(self.genome):
                    if self.energy >= 10:
                        if i == 0:  # left
                            x = self.x - 1
                            y = self.y
                        elif i == 1:  # right
                            x = self.x + 1
                            y = self.y
                        elif i == 2:  # up
                            x = self.x
                            y = self.y + 1
                        elif i == 3:  # down
                            x = self.x
                            y = self.y - 1
                        try:
                            if map[x][y] == 0:
                                self.parentOrganism.toBeChildCells.append(Cell("outgrowth", gridSquareSize, x, y, 10, self.genome, n, self.parentOrganism))
                                self.cellType = "collecter"
                                map[x][y] = 1
                        except:
                            pass

    def display(self):
        if self.cellType == "collecter":
            self.COLOUR = (0, 100, 0)
        elif self.cellType == "outgrowth":
            self.COLOUR = (120, 120, 120)
        pygame.draw.rect(screen, (self.COLOUR), pygame.Rect(self.x*self.cellSize, self.y*self.cellSize, self.cellSize, self.cellSize))



organisms = []
#defaultGenome = [[0, 2, 1, 0], [4, 4, 4, 4], [1, 4, 2, 0], [0, 4, 4, 2]]
defaultGenome = [[random.randint(0, 60000) for _ in range(4)] for _ in range(30000)]
organisms.append(Organism(defaultGenome, 300))

organisms[0].childCells.append(Cell("outgrowth", gridSquareSize, 400, round(height/gridSquareSize)-1, 30, defaultGenome, 0, organisms[0]))
map[round(height/gridSquareSize)-1][400] = 1

print(height/gridSquareSize)

counter = 0
while True:
    counter += 1

    organisms[0].update()

    screen.fill((200, 200, 255))
    for organism in organisms:
        organism.display()


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update.

    # Draw.

    pygame.display.flip()
    fpsClock.tick(fps)