import pygame
from main import CELL_SIZE

#colors
WHITE   = (55, 55, 55)         # free cells (medium-dark gray)
BLACK   = (15, 15, 15)         # walls (deep black)
GREEN   = (0, 200, 140)        # start (neon green)
RED     = (255, 90, 90)        # goal (neon red)
GRAY    = (85, 85, 85)         # grid lines
BLUE    = (40, 70, 200)        # solution path (bright neon blue)
VIOLET  = (190, 90, 255)        # exploration (neon violet)

#grid as gui
def draw_grid(window, grid, start, goal, visited=None, path=None):

    # if not passed in, default to empty set
    if visited is None:
        visited = set()
    if path is None:
        path = set()

    # rows and cols in the grid
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):

            # 0 or 1 (free or wall)
            cell_value = grid[r][c]

            # cell coordinates
            cell_pos = (r, c)

            # color of each type of cell, prioritized
            if cell_pos == start:
                color = GREEN
            elif cell_pos == goal:
                color = RED
            elif cell_pos in path:
                color = BLUE
            elif cell_pos in visited:
                color = VIOLET
            elif cell_value == 1:
                color = BLACK
            else:
                color = WHITE

            # create rectangle for each cell
            rect = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(window, color, rect)
            pygame.draw.rect(window, GRAY, rect, width=1)