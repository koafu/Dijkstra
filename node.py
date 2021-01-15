from random import random

class Node:

    def __init__(self, x, y, diagonal=True):
        self.x = x
        self.y = y
        self.diagonal = diagonal

        self.score = 999999
        self.prev = None
        self.wall = False
        self.neighbors = []
        self.colour = 255,255,255

    def get_neighbors(self, grid):

        if self.diagonal:

            for x in range(-1,2,1):
                for y in range(-1,2,1):

                    try:
                        neighborX = self.x + x
                        neighborY = self.y + y
                        neighbor = grid[neighborX][neighborY]

                        if neighborX < 0 or neighborY < 0:
                            continue
                        if neighbor == self:
                            continue
                        if not neighbor.wall:
                            self.neighbors.append(neighbor)

                    except IndexError:
                        continue

        else:
            if self.y-1 >= 0 and not grid[self.x][self.y-1].wall:
                self.neighbors.append(grid[self.x][self.y-1])
            if self.y+1 <= len(grid[0])-1 and not grid[self.x][self.y+1].wall:
                self.neighbors.append(grid[self.x][self.y+1])
            if self.x-1 >= 0 and not grid[self.x-1][self.y].wall:
                self.neighbors.append(grid[self.x-1][self.y])
            if self.x+1 <= len(grid)-1 and not grid[self.x+1][self.y].wall:
                self.neighbors.append(grid[self.x+1][self.y])
