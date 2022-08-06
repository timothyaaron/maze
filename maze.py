import random
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (235, 235, 235)

MARGIN = 10
CELL_WIDTH = 20
WIDTH, HEIGHT = 24, 16
DISPLAY_SIZE = (
    WIDTH * CELL_WIDTH + MARGIN * 2,
    HEIGHT * CELL_WIDTH + MARGIN * 2
)
TRACER_WIDTH = 8
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


class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.directions = {
            (i + 1, j): "east",
            (i - 1, j): "west",
            (i, j + 1): "south",
            (i, j - 1): "north",
        }
        self.links = {}

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
        pygame.draw.rect(win, WHITE, (self.i * cw + MARGIN + 1, self.j * cw + MARGIN + 1, cw - 2, cw - 2), 0) # knockout
        for i, j in self.links.values():
            midway = (self.i + i) / 2, (self.j + j) / 2
            pygame.draw.rect(win, WHITE, (midway[0] * cw + MARGIN + 1, midway[1] * cw + MARGIN + 1, cw - 2, cw - 2), 0)


def build_grid(width=WIDTH, height=HEIGHT, cw=CELL_WIDTH):
    global grid
    grid = {(i, j): Point(i, j) for j in range(height) for i in range(width)}


def build_maze():

    def _valid_direction(cell):
        return cell not in visited_cells and cell in grid

    stack_list = []
    visited_cells = []

    idx = 0, 0
    stack_list.append(idx)
    visited_cells.append(idx)

    while stack_list:
        valid_directions = [d for d in grid[idx].directions if _valid_direction(d)]

        if valid_directions:
            new_idx = random.choice(valid_directions)

            path[new_idx] = idx  # do I need this?
            visited_cells.append(new_idx)
            stack_list.append(new_idx)

            # link from idx to new_idx
            absolute_direction = grid[idx].directions[new_idx]
            grid[idx].links[absolute_direction] = new_idx

            # link from new_idx to idx
            absolute_direction = grid[new_idx].directions[idx]
            grid[new_idx].links[absolute_direction] = idx

            idx = new_idx

        else:
            idx = stack_list.pop()
