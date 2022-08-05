import pygame

import maze


maze.build_grid()
maze.build_maze()
pygame.display.update()

RUN = True
x = y = maze.MARGIN + (maze.CELL_WIDTH - maze.TRACER_WIDTH) // 2

while RUN:
    maze.clock.tick(maze.FPS)

    for event in pygame.event.get():
        prev_x, prev_y = x, y
        if event.type == pygame.QUIT:
            RUN = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_RIGHT:
                x += maze.CELL_WIDTH
            elif event.key == pygame.K_LEFT:
                x -= maze.CELL_WIDTH
            elif event.key == pygame.K_DOWN:
                y += maze.CELL_WIDTH
            elif event.key == pygame.K_UP:
                y -= maze.CELL_WIDTH

        pygame.draw.rect(maze.win, (maze.GREY), (prev_x, prev_y, 20, 20))
        pygame.draw.rect(maze.win, (maze.BLUE), (x, y, 20, 20))
        pygame.display.update()