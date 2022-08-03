import random
import time
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (235, 235, 235)

WIDTH, HEIGHT = 20, 15
CELL_WIDTH = 40
TRACER_WIDTH = 2
MARGIN = 10
DISPLAY_SIZE = (
    WIDTH * CELL_WIDTH + MARGIN * 2,
    HEIGHT * CELL_WIDTH + MARGIN * 2
)

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Maze generator")
win = pygame.display.set_mode(DISPLAY_SIZE)
win.fill(GREY)
pygame.display.update()
Fps = 30
clock = pygame.time.Clock()


grid = []
stack_list = []
closed_list = []

path = {}


def build_grid(width, height, cw=CELL_WIDTH):
    for n in range(height):
        y = cw * n + MARGIN
        for m in range(width):
            x = cw * m + MARGIN
            pygame.draw.line(win, BLACK, [x + cw, y], [x + cw, y + cw], 2) # East wall
            pygame.draw.line(win, BLACK, [x , y], [x, y + cw], 2) # West wall
            pygame.draw.line(win, BLACK, [x, y], [x + cw, y], 2) # North wall
            pygame.draw.line(win, BLACK, [x, y + cw], [x + cw, y + cw], 2) # South wall

            grid.append((x,y))
            pygame.display.update()


def knockdown_east_wall(x, y):
    pygame.draw.rect(win, WHITE, (x + 1, y + 1, (CELL_WIDTH*2 - 1), CELL_WIDTH-1), 0)
    pygame.display.update()


def knockdown_west_wall(x, y):
    pygame.draw.rect(win, WHITE, (x - CELL_WIDTH  + 1, y + 1, (CELL_WIDTH*2 - 1), CELL_WIDTH-1), 0)
    pygame.display.update()


def knockdown_north_wall(x, y):
    pygame.draw.rect(win, WHITE, (x + 1, y - CELL_WIDTH + 1, CELL_WIDTH-1, (CELL_WIDTH*2 - 1)), 0)
    pygame.display.update()


def knockdown_south_wall(x, y):
    pygame.draw.rect(win, WHITE, (x + 1, y + 1, CELL_WIDTH-1, (CELL_WIDTH*2 - 1)), 0)
    pygame.display.update()


def single_cell(x, y):
    pygame.draw.rect(win, BLUE, (x + 1, y + 1, CELL_WIDTH-2, CELL_WIDTH-2), 0)
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(win, WHITE, (x + 1, y+1, CELL_WIDTH-2, CELL_WIDTH-2), 0)
    pygame.display.update()


def maze(margin=MARGIN):
    x, y = margin, margin
    single_cell(x, y)
    stack_list.append((x,y))
    closed_list.append((x,y))

    while len(stack_list) > 0:
        cell = []

        if(x + CELL_WIDTH, y) not in closed_list and (x + CELL_WIDTH, y) in grid:
            cell.append("east")

        if (x - CELL_WIDTH, y) not in closed_list and (x - CELL_WIDTH, y) in grid:
            cell.append("west")

        if (x , y + CELL_WIDTH) not in closed_list and (x , y + CELL_WIDTH) in grid:
            cell.append("south")

        if (x, y - CELL_WIDTH) not in closed_list and (x , y - CELL_WIDTH) in grid:
            cell.append("north")

        if len(cell) > 0:
            current_cell = (random.choice(cell))

            if current_cell == "east":
                knockdown_east_wall(x,y)
                path[(x + CELL_WIDTH, y)] = x, y
                x = x + CELL_WIDTH
                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "west":
                knockdown_west_wall(x, y)
                path[(x - CELL_WIDTH, y)] = x, y
                x = x - CELL_WIDTH
                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "north":
                knockdown_north_wall(x, y)
                path[(x , y - CELL_WIDTH)] = x, y
                y = y - CELL_WIDTH
                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "south":
                knockdown_south_wall(x, y)
                path[(x , y + CELL_WIDTH)] = x, y
                y = y + CELL_WIDTH
                closed_list.append((x, y))
                stack_list.append((x, y))

            time.sleep(0.03)

        else:
            x, y = stack_list.pop()
            single_cell(x, y)
            time.sleep(0.03)
            backtracking_cell(x, y)


def path_tracker(x, y):
    pygame.draw.rect(
        win,
        BLUE,
        (
            x + CELL_WIDTH//2 - TRACER_WIDTH//2,
            y + CELL_WIDTH//2 - TRACER_WIDTH//2,
            TRACER_WIDTH,
            TRACER_WIDTH
        ),
        0
    )
    pygame.display.update()


def path_tracer(x, y):
    path_tracker(x,y)
    while (x, y) != (MARGIN, MARGIN):
        x, y = path[x, y]
        path_tracker(x,y)
        time.sleep(0.1)


build_grid(WIDTH, HEIGHT)
maze()
path_tracer(
    (WIDTH - 1) * CELL_WIDTH + MARGIN,
    (HEIGHT - 1) * CELL_WIDTH + MARGIN
)

# RUN = True
# while RUN:
#     clock.tick(Fps)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             RUN = False