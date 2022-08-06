import os

import pygame

from algorithms import prim

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (235, 235, 235)

MARGIN = 10
CELL_WIDTH = 30
WIDTH, HEIGHT = 30, 30
DISPLAY_SIZE = (
    WIDTH * CELL_WIDTH + MARGIN * 2,
    HEIGHT * CELL_WIDTH + MARGIN * 2
)
TRACER_WIDTH = 8
FPS = 30

SHOW_MAZE = True
BG_COLOR = GREY

os.environ['SDL_VIDEO_WINDOW_POS'] ="1200,100"


pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Maze generator")
win = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()

win.fill(BG_COLOR)
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

    @property
    def idx(self):
        return self.i, self.j

    def _to_tracer(self, coord):
        return coord * CELL_WIDTH + MARGIN + round((CELL_WIDTH - TRACER_WIDTH) / 2)

    def hide_user(self):
        pygame.draw.rect(win, (WHITE), (self._to_tracer(self.i), self._to_tracer(self.j), TRACER_WIDTH, TRACER_WIDTH))

    def show_user(self):
        pygame.draw.rect(win, (BLUE), (self._to_tracer(self.i), self._to_tracer(self.j), TRACER_WIDTH, TRACER_WIDTH))

    def hide_walls(self):
        cw = CELL_WIDTH
        pygame.draw.rect(win, BG_COLOR, (self.i * cw + MARGIN, self.j * cw + MARGIN, cw, cw), 0) # walls

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
    prim.build_maze(grid, path, SHOW_MAZE)
