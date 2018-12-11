import pygame
from collections import deque
from gameObjects import Cell, Grid

if not pygame.mixer:
    print('Warning, sound disabled')
if not pygame.font:
    print('Warning, fonts disabled')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def main():
    # Initialize Everything
    pygame.mixer.pre_init(11025, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Game Of Life')
    pygame.mouse.set_visible(1)
    clocktime = 60
    clock = pygame.time.Clock()

    run = False 
    cellUpdateQueue = deque()
    grid = Grid(20, 10, cellUpdateQueue)
    dragCells = set()
    killFirst = False

    # Create Background 
    background = pygame.Surface((500, 500))
    background.fill(BLUE)

    while True:
        while not run:
            clock.tick(clocktime) 
            
            # Handle Events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return False
                if (event.type == pygame.MOUSEBUTTONUP):
                    row = event.pos[1] // grid.cellSize
                    col = event.pos[0] // grid.cellSize
                    if row < grid.size and col < grid.size and (row, col) not in dragCells:
                        grid.cells[row][col].toggleAlive() 
                        cellUpdateQueue.appendleft(grid.cells[row][col])
                    dragCells.clear()
                if (event.type == pygame.MOUSEMOTION):
                    print(event.pos, event.rel, event.buttons)
                    if event.buttons[0]:
                        row = event.pos[1] // grid.cellSize
                        col = event.pos[0] // grid.cellSize
                        if row < grid.size and col < grid.size and (row, col) not in dragCells:
                            curCell = grid.cells[row][col]
                            if not dragCells:
                                killFirst = curCell.alive
                            dragCells.add((row, col))
                            curCell.kill() if killFirst else curCell.revive()
                            cellUpdateQueue.appendleft(grid.cells[row][col])

                        
            # Draw updated cells
            while cellUpdateQueue:
                curCell = cellUpdateQueue.pop()
                color = GREEN if curCell.alive else RED
                pygame.draw.rect(background, color, curCell)

            # Display background
            screen.blit(background, (0,0))
            pygame.display.flip()

if __name__ == '__main__':
    while(main()):
        pass
