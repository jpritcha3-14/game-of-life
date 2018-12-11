import pygame

class Cell(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super(Cell, self).__init__(*args, **kwargs)
        self.alive = False

    def toggleAlive(self):
        self.alive = not self.alive

    def kill(self):
        self.alive = False

    def revive(self):
        self.alive = True

class Grid:
    def __init__(self, size, cellSize, cellUpdateQueue):
        self.size = size
        self.cellSize = cellSize
        self.cells = [[] for _ in range(self.size)]
        for i in range(size**2):
            row = i // size
            col = i % size
            self.cells[row].append(Cell(col*cellSize, row*cellSize, cellSize, cellSize))
            cellUpdateQueue.append(self.cells[row][col])
