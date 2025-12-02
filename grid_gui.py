import pygame
import sys
import time

from grid import CELL_SIZE, GRID_ROWS, GRID_COLS, create_grid
from breadth_first import bfs

ANIMATION_SPEED = 10

#colors
WHITE    = (55, 55, 55)         # free cells (medium-dark gray)
BLACK    = (15, 15, 15)         # walls (deep black)
GREEN    = (0, 200, 140)        # start (neon green)
RED      = (255, 90, 90)        # goal (neon red)
GRAY     = (85, 85, 85)         # grid lines
BLUE     = (40, 70, 200)        # solution path (bright neon blue)
VIOLET  = (190, 90, 255)        # exploration (neon violet)

#grid as gui
def draw_grid(window, grid, start, goal, visited=None, path=None):

    # if not passsed in, default to empty set
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


def main():
    pygame.init()
    
    grid = create_grid()
    start = (0,0)
    goal = (GRID_ROWS -1, GRID_COLS -1)

    final_path = []     #final path
    visited_order = []  #list returned by bfs
    explore_index = 0   #how many explored cells are displayed
    exploring = False   #are we still animating?

    # calculate window size
    width = GRID_COLS * CELL_SIZE
    height = GRID_ROWS * CELL_SIZE

    # create window and set title
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pathfinding Grid")

    # fps
    clock = pygame.time.Clock()

    # main game loop
    running = True
    while running:

        #evet handling
        for event in pygame.event.get():
            
            # exit
            if event.type == pygame.QUIT:
                running = False
        
            # mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:       
                    
                    # clicked pixel coordinates
                    mouse_x, mouse_y = event.pos
                    #convert pixel coordinates to cell coordinates
                    col = mouse_x // CELL_SIZE  
                    row = mouse_y // CELL_SIZE
                
                    # if cell out of bounds
                    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                        # if cell is not start and not goal
                        if (row, col) != start and (row, col) != goal:
                            
                            # convert clicked to wall / free cell
                            if grid[row][col] == 0:
                                grid[row][col] = 1
                            else:
                                grid[row][col] = 0
                            
                            # reset visuals after mouse click
                            final_path = []     # final path
                            visited_order = []  # list returned by bfs
                            explore_index = 0   # how many we've shown
                            exploring = False   # are we still animating?
            
            # button press
            if event.type == pygame.KEYDOWN:

                # b (for bfs)
                if event.key == pygame.K_b:
                    
                    # run bfs
                    visited_order, final_path = bfs(grid, start, goal)
                    print("BFS visited nodes:", len(visited_order))
                    print("BFS path length:", len(final_path))
                    
                    #start exploring animation
                    explore_index = 0
                    exploring = True

        # rebuild sets for each frame
        visited_set = set()
        path_set = set()

        # if bfs worked (visited not empty)
        if visited_order:
            # and we're still exploring
            if exploring:                        
                #increment exploring index by how many we've displayed
                explore_index += ANIMATION_SPEED 

                # if exploring index exceeds size of visited, stop exploring 
                if explore_index >= len(visited_order):
                    explore_index = len(visited_order)
                    exploring = False
            
            visited_set = set(visited_order[:explore_index])

            if not exploring and final_path:
                path_set = set(final_path)

        #clear window (paint background)                
        window.fill((30,30,30))

        #draw cells on the grid
        draw_grid(window, grid, start, goal, visited_set, path_set)
        
        #display the grid
        pygame.display.flip()

        #limit loop to 60 fps
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
     main()