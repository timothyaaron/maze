import random
from tkinter.tix import CELL
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (235, 235, 235)

MARGIN = 10
CELL_WIDTH = 40
WIDTH, HEIGHT = 20, 15
DISPLAY_SIZE = (
    WIDTH * CELL_WIDTH + MARGIN * 2,
    HEIGHT * CELL_WIDTH + MARGIN * 2
)
TRACER_WIDTH = 20
FPS = 30


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Maze generator")
win = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()

win.fill(GREY)
pygame.display.update()

grid = []
path = {}
connections = []


def build_grid(width=WIDTH, height=HEIGHT, cw=CELL_WIDTH):
    for n in range(height):
        y = cw * n + MARGIN
        for m in range(width):
            x = cw * m + MARGIN
            pygame.draw.line(win, BLACK, [x, y], [x + cw, y], 2) # North wall
            pygame.draw.line(win, BLACK, [x, y], [x, y + cw], 2) # West wall
            pygame.draw.line(win, BLACK, [x + cw, y], [x + cw, y + cw], 2) # East wall
            pygame.draw.line(win, BLACK, [x, y + cw], [x + cw, y + cw], 2) # South wall

            grid.append((m, n))


def knockdown_cell(coord):
    cw = CELL_WIDTH
    pygame.draw.rect(win, WHITE, (coord[0] * cw + MARGIN + 1, coord[1] * cw + MARGIN + 1, cw - 1, cw - 1), 0)


def build_maze():

    def _valid_direction(cell):
        return cell not in visited_cells and cell in grid

    stack_list = []
    visited_cells = []

    current = 0, 0
    stack_list.append(current)
    visited_cells.append(current)

    while len(stack_list) > 0:
        knockdown_cell(current)
        all_directions = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
        ]
        valid_directions = [d for d in all_directions if _valid_direction(d)]

        if valid_directions:
            selected = random.choice(valid_directions)
            midway = (current[0] + selected[0]) / 2, (current[1] + selected[1]) / 2
            knockdown_cell(midway)
            path[selected] = current
            visited_cells.append(selected)
            stack_list.append(selected)
            connections.append(set([current, selected]))
            current = selected

        else:
            current = stack_list.pop()
