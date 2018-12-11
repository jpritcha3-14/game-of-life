import pygame
from collections import deque
from gameObjects import Grid, Button

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
    speed = 10
    clock = pygame.time.Clock()

    run = False 
    cellUpdateQueue = deque()
    grid = Grid(20, 10, cellUpdateQueue)
    startStopButton = Button((grid.get_left() + grid.get_right()) // 2 - 50 // 2, grid.get_bottom() + 10, 50, 20)
    killFirst = False

    # Create Background 
    background = pygame.Surface((500, 500))
    background.fill(BLUE)

    while True:
        if not run:
            clock.tick(clocktime) 

            # Handle Events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return False
                if (event.type == pygame.MOUSEBUTTONUP):
                    row = event.pos[1] // grid.cellSize
                    col = event.pos[0] // grid.cellSize
                    if row < grid.size and col < grid.size and (row, col) not in grid.dragCells:
                        grid.toggleAlive(row, col) 
                        cellUpdateQueue.appendleft(grid.getCell(row, col))
                    grid.dragCells.clear()
                    if startStopButton.collidepoint(event.pos):
                        startStopButton.press()
                if (event.type == pygame.MOUSEMOTION):
                    #print(event.pos, event.rel, event.buttons)
                    if event.buttons[0]:
                        row = event.pos[1] // grid.cellSize
                        col = event.pos[0] // grid.cellSize
                        if row < grid.size and col < grid.size and (row, col) not in grid.dragCells:
                            curState = grid.getState(row, col)
                            if not grid.dragCells:
                                killFirst = curState 
                            grid.dragCells.add((row, col))
                            grid.kill(row, col) if killFirst else grid.revive(row, col)
                            cellUpdateQueue.appendleft(grid.getCell(row, col))
        else:
            clock.tick(speed)

            # Handle events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return False
                if (event.type == pygame.MOUSEBUTTONUP):
                    if startStopButton.collidepoint(event.pos):
                        startStopButton.press()
            
            cellUpdateQueue.extendleft(grid.next_generation())

                        
        # Draw updated cells
        while cellUpdateQueue:
            curCell = cellUpdateQueue.pop()
            color = GREEN if grid.getState(*curCell.loc) else RED
            pygame.draw.rect(background, color, curCell)


        # Check and draw startStopButton
        if startStopButton.get_changed():
            startStopButton.reset_changed()
            run = startStopButton.get_state()
            color = RED if run else GREEN
            pygame.draw.rect(background, color, startStopButton)

        # Display background
        screen.blit(background, (0,0))
        pygame.display.flip()

if __name__ == '__main__':
    while(main()):
        pass
