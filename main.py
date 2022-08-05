import time

import pygame

import maze


# TODO: fade out trail


maze.build_grid()
maze.build_maze()
pygame.display.update()

def _to_tracer(coord):
    return coord * maze.CELL_WIDTH + maze.MARGIN + (maze.CELL_WIDTH - maze.TRACER_WIDTH) // 2

RUN = True
x = y = 0
pygame.draw.rect(maze.win, (maze.BLUE), (_to_tracer(x), _to_tracer(y), 20, 20))
pygame.display.update()

while RUN:
    maze.clock.tick(maze.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUN = False
                break
            elif event.key == pygame.K_RIGHT and set([(x, y), (x + 1, y)]) in maze.connections:
                prev = (x, y)
                x += 1
            elif event.key == pygame.K_LEFT and set([(x, y), (x - 1, y)]) in maze.connections:
                prev = (x, y)
                x -= 1
            elif event.key == pygame.K_DOWN and set([(x, y), (x, y + 1)]) in maze.connections:
                prev = (x, y)
                y += 1
            elif event.key == pygame.K_UP and set([(x, y), (x, y - 1)]) in maze.connections:
                prev = (x, y)
                y -= 1

            pygame.draw.rect(maze.win, (maze.GREY), (_to_tracer(prev[0]), _to_tracer(prev[1]), 20, 20))
            pygame.draw.rect(maze.win, (maze.BLUE), (_to_tracer(x), _to_tracer(y), 20, 20))
            pygame.display.update()

    if (x, y) == (maze.WIDTH - 1, maze.HEIGHT - 1):
        time.sleep(.5)
        RUN = False
