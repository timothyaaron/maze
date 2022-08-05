import time

import pygame

import maze

MEMORY_LENGTH = 8


# TODO: fade out walls
# TODO: re:build_maze, prefer neighboring cells that have fewer visited neighbors
# TODO: start small, finishing opens a harder one
# TODO: add random connections to add possibility of looping?
# TODO: show line-of-sight cells


maze.build_grid()
maze.build_maze()
pygame.display.update()

RUN = True
prev = []
x = y = 0
maze.grid[(x, y)].show_walls()
maze.grid[(x, y)].show_user()
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
            elif event.key == pygame.K_RIGHT and (x + 1, y) in maze.grid[(x, y)].connections:
                prev = [(x, y)] + prev
                x += 1
            elif event.key == pygame.K_LEFT and (x - 1, y) in maze.grid[(x, y)].connections:
                prev = [(x, y)] + prev
                x -= 1
            elif event.key == pygame.K_DOWN and (x, y + 1) in maze.grid[(x, y)].connections:
                prev = [(x, y)] + prev
                y += 1
            elif event.key == pygame.K_UP and (x, y - 1) in maze.grid[(x, y)].connections:
                prev = [(x, y)] + prev
                y -= 1

            if prev:
                maze.grid[prev[0]].hide_user()

            if len(prev) > MEMORY_LENGTH:
                maze.grid[prev[MEMORY_LENGTH]].hide_walls()
                prev = prev[:MEMORY_LENGTH]

            maze.grid[(x, y)].show_walls()
            maze.grid[(x, y)].show_user()
            pygame.display.update()

    if (x, y) == (maze.WIDTH - 1, maze.HEIGHT - 1):
        time.sleep(.5)
        RUN = False
