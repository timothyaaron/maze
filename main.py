import time

import pygame

import maze

MEMORY_LENGTH = 8


# TODO: fade out walls
# TODO: re:build_maze, prefer neighboring cells that have fewer visited neighbors
# TODO: start small, finishing opens a harder one
# TODO: add random connections to add possibility of looping?
# TODO: cleanup line-of-sight history


maze.build_grid()
maze.build_maze()
pygame.display.update()

RUN = True
history = []
idx = (0, 0)
grid = maze.grid
grid[idx].show_walls()
grid[idx].show_user()
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
            elif event.key == pygame.K_RIGHT and (idx[0] + 1, idx[1]) in grid[idx].links.values():
                history = [idx] + history
                idx = (idx[0] + 1, idx[1])
            elif event.key == pygame.K_LEFT and (idx[0] - 1, idx[1]) in grid[idx].links.values():
                history = [idx] + history
                idx = (idx[0] - 1, idx[1])
            elif event.key == pygame.K_DOWN and (idx[0], idx[1] + 1) in grid[idx].links.values():
                history = [idx] + history
                idx = (idx[0], idx[1] + 1)
            elif event.key == pygame.K_UP and (idx[0], idx[1] - 1) in grid[idx].links.values():
                history = [idx] + history
                idx = (idx[0], idx[1] - 1)

            if history:
                grid[history[0]].hide_user()

            if len(history) > MEMORY_LENGTH:
                grid[history[MEMORY_LENGTH]].hide_walls()
                history = history[:MEMORY_LENGTH]

            grid[idx].show_walls()

            # line of sight
            for d, coord in grid[idx].links.items():
                while coord:
                    grid[coord].show_walls()
                    coord = grid[coord].links.get(d)

            grid[idx].show_user()
            pygame.display.update()

    if idx == (maze.WIDTH - 1, maze.HEIGHT - 1):
        time.sleep(.5)
        RUN = False
