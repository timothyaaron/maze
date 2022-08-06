import pdb
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
WIDTH, HEIGHT = 30, 20
DISPLAY_SIZE = (
    WIDTH * CELL_WIDTH + MARGIN * 2,
    HEIGHT * CELL_WIDTH + MARGIN * 2
)
TRACER_WIDTH = 12
FPS = 30


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Maze generator")
win = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()

win.fill(WHITE)
pygame.display.update()

grid = {}
path = {}
connections = []


class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.possible_connections = set(
            [
                (i + 1, j),
                (i - 1, j),
                (i, j + 1),
                (i, j - 1),
            ]
        )

        self.connections = set()

    @property
    def walls(self):
        return self.possible_connections.difference(self.connections)

    def _to_tracer(self, coord):
        return coord * CELL_WIDTH + MARGIN + (CELL_WIDTH - TRACER_WIDTH) // 2

    def hide_user(self):
        pygame.draw.rect(win, (WHITE), (self._to_tracer(self.i), self._to_tracer(self.j), TRACER_WIDTH, TRACER_WIDTH))

    def show_user(self):
        pygame.draw.rect(win, (BLUE), (self._to_tracer(self.i), self._to_tracer(self.j), TRACER_WIDTH, TRACER_WIDTH))

    def hide_walls(self):
        cw = CELL_WIDTH
        pygame.draw.rect(win, WHITE, (self.i * cw + MARGIN, self.j * cw + MARGIN, cw, cw), 0) # walls

    def show_walls(self):
        cw = CELL_WIDTH
        pygame.draw.rect(win, BLACK, (self.i * cw + MARGIN, self.j * cw + MARGIN, cw, cw), 0) # walls
        pygame.draw.rect(win, WHITE, (self.i * cw + MARGIN + 1, self.j * cw + MARGIN + 1, cw - 2, cw - 2), 0) # walls
        for c in self.connections:
            midway = (self.i + c[0]) / 2, (self.j + c[1]) / 2
            pygame.draw.rect(win, WHITE, (midway[0] * cw + MARGIN + 1, midway[1] * cw + MARGIN + 1, cw - 2, cw - 2), 0)


def build_grid(width=WIDTH, height=HEIGHT, cw=CELL_WIDTH):
    global grid
    grid = {(i, j): Point(i, j) for j in range(height) for i in range(width)}

    # for j in range(height):
    #     y = cw * j + MARGIN
    #     for i in range(width):
    #         x = cw * i + MARGIN

    #         pygame.draw.line(win, BLACK, [x, y], [x + cw, y], 2) # North wall
    #         pygame.draw.line(win, BLACK, [x, y], [x, y + cw], 2) # West wall
    #         pygame.draw.line(win, BLACK, [x + cw, y], [x + cw, y + cw], 2) # East wall
    #         pygame.draw.line(win, BLACK, [x, y + cw], [x + cw, y + cw], 2) # South wall

    # #         # grid.append((i, j))


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

    while stack_list:
        # knockdown_cell(current)
        all_directions = grid[current].possible_connections
        valid_directions = [d for d in all_directions if _valid_direction(d)]

        if valid_directions:
            selected = random.choice(valid_directions)
            # midway = (current[0] + selected[0]) / 2, (current[1] + selected[1]) / 2
            # knockdown_cell(midway)
            path[selected] = current
            visited_cells.append(selected)
            stack_list.append(selected)
            grid[current].connections.add(selected)
            grid[selected].connections.add(current)
            current = selected

        else:
            current = stack_list.pop()
