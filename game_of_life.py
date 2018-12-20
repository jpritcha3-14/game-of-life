import pygame
from collections import deque
from gameObjects import Grid, Button

if not pygame.mixer:
    print('Warning, sound disabled')
if not pygame.font:
    print('Warning, fonts disabled')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main():
    # Initialize Everything
    pygame.mixer.pre_init(11025, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((500, 525))
    pygame.display.set_caption('Game Of Life')
    pygame.mouse.set_visible(1)
    clocktime = 120 
    speed = 10
    clock = pygame.time.Clock()

    run = False 
    killFirst = False
    cellUpdateQueue = deque()
    gridWidth = 40
    cellWidth = 10
    offset = (500 - gridWidth*cellWidth) // 2
    grid = Grid(gridWidth, cellWidth, offset, cellUpdateQueue)
    startStopButton = Button((grid.get_left() + grid.get_right()) // 2 - (75 // 2) + offset, 
                              grid.get_bottom() + 30 + offset, 75, 30)
    clearButton = Button(startStopButton.left + startStopButton.get_width() + 10, 
                         startStopButton.top, 75, 30, 'CLEAR', BLACK)
    speedUp = Button(startStopButton.left - 10 - 30, startStopButton.top, 30, 30, '+', BLACK)
    speedDisplay = Button(speedUp.left - 10 - 30, startStopButton.top, 30, 30, str(speed), GREY, BLACK)
    speedDown = Button(speedDisplay.left - 10 - 30, startStopButton.top, 30, 30, '-', BLACK)
    speedLabel = Button(speedDown.left, speedDown.top - 25, 110, 30, 'SPEED', GREY, BLACK)

    # Create Background 
    background = pygame.Surface((500, 525))
    background.fill(GREY)
    background.blit(startStopButton, (startStopButton.left, startStopButton.top))
    background.blit(clearButton, (clearButton.left, clearButton.top))
    background.blit(speedLabel, (speedLabel.left, speedLabel.top))
    background.blit(speedUp, (speedUp.left, speedUp.top))
    background.blit(speedDown, (speedDown.left, speedDown.top))

    while True:
        if not run:
            clock.tick(clocktime) 

            # Handle Events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    return False
                if (event.type == pygame.MOUSEBUTTONUP):
                    if grid.area.collidepoint(event.pos):
                        row = (event.pos[1] - offset) // grid.cellSize
                        col = (event.pos[0] - offset) // grid.cellSize
                        if row < grid.size and col < grid.size and (row, col) not in grid.dragCells:
                            grid.toggleAlive(row, col) 
                            cellUpdateQueue.appendleft(grid.getCell(row, col))
                        grid.dragCells.clear()
                    if startStopButton.area.collidepoint(event.pos):
                        startStopButton.press()
                    if clearButton.area.collidepoint(event.pos):
                        clearButton.press()
                    if speedUp.area.collidepoint(event.pos):
                        speedUp.press()
                        speed = min(speed + 1, 20)
                    if speedDown.area.collidepoint(event.pos):
                        speedDown.press()
                        speed = max(speed - 1, 1)
                if (event.type == pygame.MOUSEMOTION):
                    #print(event.pos, event.rel, event.buttons)
                    if grid.area.collidepoint(event.pos) and  event.buttons[0]:
                        row = (event.pos[1] - offset) // grid.cellSize
                        col = (event.pos[0] - offset) // grid.cellSize
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
                    if startStopButton.area.collidepoint(event.pos):
                        startStopButton.press()
                    if clearButton.area.collidepoint(event.pos):
                        clearButton.press()
                        startStopButton.press()
                    if speedUp.area.collidepoint(event.pos):
                        speedUp.press()
                        speed = min(speed + 1, 20)
                    if speedDown.area.collidepoint(event.pos):
                        speedDown.press()
                        speed = max(speed - 1, 1)
            
            cellUpdateQueue.extendleft(grid.next_generation())

                        
        # Draw updated cells
        while cellUpdateQueue:
            curCell = cellUpdateQueue.pop()
            color = BLACK if grid.getState(*curCell.loc) else WHITE
            pygame.draw.rect(background, color, curCell)

        # Check clearButton
        if clearButton.get_changed():
            clearButton.reset_changed()
            cellUpdateQueue.clear()
            cellUpdateQueue.extend(grid.clear())

        # Check and draw startStopButton
        if startStopButton.get_changed():
            startStopButton.reset_changed()
            run = startStopButton.get_state()
            startStopButton.update(RED if run else BLACK, 'STOP' if run else 'START')
            background.blit(startStopButton, (startStopButton.left, startStopButton.top))

        # Update Speed Display
        speedDisplay.update(GREY, str(speed))
        background.blit(speedDisplay, (speedDisplay.left, speedDisplay.top))
        
        # Display background
        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    while(main()):
        pass
