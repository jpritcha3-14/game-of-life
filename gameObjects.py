import pygame
from collections import namedtuple

Location = namedtuple('Location', ['row', 'col'])
pygame.font.init()
font = pygame.font.Font(None, 30)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Button(pygame.Surface):
    def __init__(self, left, top, width, height, text='', color=RED, textColor=WHITE):
        super(Button, self).__init__((width, height))
        self.area = pygame.Rect(left, top, width, height)
        self.state = False
        self.stateChanged = True
        self.left = left
        self.top = top
        self.textColor = textColor
        self.update(color, text)

    def update(self, color, text):
        self.fill(color)
        textSurf = font.render(text, False, self.textColor)
        horizOffset = abs(self.get_width() - textSurf.get_width()) // 2
        vertOffset = abs(self.get_height() - textSurf.get_height()) // 2
        self.blit(textSurf, (horizOffset, vertOffset))

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
    def __init__(self, size, cellSize, offset, cellUpdateQueue):
        self.size = size
        self.cellSize = cellSize
        self.area = pygame.Rect(offset, offset, size*cellSize, size*cellSize)
        self.dragCells = set()
        self.cells = [[] for _ in range(size)]
        self.states = [[False for _ in range(size)] for _ in range(size)]
        for i in range(size**2):
            row = i // size
            col = i % size
            self.cells[row].append(Cell(col*cellSize + offset, row*cellSize + offset, cellSize, cellSize, Location(row, col)))
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

    def clear(self):
        self.states = [[False for _ in range(self.size)] for _ in range(self.size)]
        return [cell for row in self.cells for cell in row]

    def next_generation(self):
        nextGen = [[False for _ in range(self.size)] for _ in range(self.size)]
        updatedCells = []
        for row in range(self.size):
            for col in range(self.size):
                neighbors = sum((self.states[row-1][col-1], 
                                self.states[row-1][col],
                                self.states[row-1][(col + 1) % self.size], 
                                self.states[row][col-1],
                                self.states[row][(col + 1) % self.size], 
                                self.states[(row + 1) % self.size][col-1],
                                self.states[(row + 1) % self.size][col], 
                                self.states[(row + 1) % self.size][(col + 1) % self.size]))
                if (self.states[row][col] and neighbors == 2) or neighbors == 3:
                    nextGen[row][col] = True    
                if self.states[row][col] != nextGen[row][col]:
                    updatedCells.append(self.cells[row][col])
        self.states = nextGen
        return updatedCells
