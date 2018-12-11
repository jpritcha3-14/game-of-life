import pygame
from collections import namedtuple

Location = namedtuple('Location', ['row', 'col'])

class Button(pygame.Rect):
    def __init__(self, left, top, width, height):
        super(Button, self).__init__(left, top, width, height)
        self.state = False
        self.stateChanged = True

    def press(self):
        self.state = not self.state
        self.stateChanged = True

    def get_changed(self):
        return self.stateChanged

    def get_state(self):
        return self.state
    
    def reset_changed(self):
        self.stateChanged = False


class Cell(pygame.Rect):
    def __init__(self, left, top, width, height, loc):
        super(Cell, self).__init__(left, top, width, height)
        self.loc = loc


class Grid:
    def __init__(self, size, cellSize, cellUpdateQueue):
        self.size = size
        self.cellSize = cellSize
        self.dragCells = set()
        self.cells = [[] for _ in range(size)]
        self.states = [[False for _ in range(size)] for _ in range(size)]
        for i in range(size**2):
            row = i // size
            col = i % size
            self.cells[row].append(Cell(col*cellSize, row*cellSize, cellSize,
                cellSize, Location(row, col)))
            cellUpdateQueue.append(self.cells[row][col])

    def getState(self, row, col):
        return self.states[row][col]

    def getCell(self, row, col):
        return self.cells[row][col]

    def toggleAlive(self, row, col):
        self.states[row][col] = not self.states[row][col]

    def kill(self, row, col):
        self.states[row][col] = False

    def revive(self, row, col):
        self.states[row][col] = True

    def get_left(self):
        return 0 

    def get_bottom(self):
        return self.size*self.cellSize 
    
    def get_right(self):
        return self.size*self.cellSize 


