import pygame
import sys
import time
from collections import deque

#size
CELL_SIZE = 50
GRID_ROWS = 10
GRID_COLS = 10

#colors
WHITE = (220, 220, 220)     #free cells
BLACK = (0, 0, 0)           #wall
GREEN = (0, 200, 0)         #start
RED = (200, 0, 0)           #goal
GRAY = (80, 80, 80)         #grid lines
BLUE = (0, 120, 255)        #path
YELLOW = (255, 215, 0)      #explored path

ANIMATION_SPEED = 5

#the grid
def create_grid():

    grid = []

    for r in range(GRID_ROWS):
        row = []
        for cols in range(GRID_COLS):
            row.append(0)
        grid.append(row)

    return grid

#bfs
def bfs(grid, start, goal):
    
    rows = len(grid)
    cols = len(grid[0])

    queue = deque()
    queue.append(start)

    #hashmap of each cell with its parent
    parents = {start: None}

    #visited cells
    visited_order = []

    #up, down, left, right
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    #while queue is not empty
    while queue:

        current_row, current_col = queue.popleft()
        visited_order.append((current_row, current_col))

        #goal reached
        if (current_row, current_col) == goal:
            break

        #explore neighbors, next (r, c) = direction + current (r, c)
        for row_direction, col_direction in directions:
            next_row = current_row + row_direction
            next_col = current_col + col_direction

            #bounds check
            #if the next (r, c) is out of bounds, try next direction
            if 0 <= next_row < rows and 0 <= next_col < cols:
                #if next (r, c)not a wall
                if grid[next_row][next_col] == 0:
                    #if next (r, c) is not a parent
                    if (next_row, next_col) not in parents:
                        #add current (r, c) as parent of next (r, c)
                        parents[(next_row, next_col)] = (current_row, current_col)
                        queue.append((next_row, next_col))  #add next (r, c) to the queue
    
    #no path
    if goal not in parents:
        return visited_order, []
    
    #reconstruct path
    path = []
    current_cell = goal
    while current_cell is not None:
        path.append(current_cell)
        current_cell = parents[current_cell]
    path.reverse()

    return visited_order, path

#grid as gui
def draw_grid(window, grid, start, goal, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = set()

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            cell_value = grid[r][c]
            cell_pos = (r, c)

            # PRIORITY: start/goal > path > visited > wall > empty
            if cell_pos == start:
                color = GREEN
            elif cell_pos == goal:
                color = RED
            elif cell_pos in path:
                color = BLUE          # final path
            elif cell_pos in visited:
                color = (255, 215, 0) # exploration
            elif cell_value == 1:
                color = BLACK
            else:
                color = WHITE

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

    current_path = []   #final path
    visited_order = []  #list returned by bfs
    explore_index = 0   #how many we've shown
    exploring = False   #are we still animating?

    width = GRID_COLS * CELL_SIZE
    height = GRID_ROWS * CELL_SIZE
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pathfinding Grid")

    clock = pygame.time.Clock()

    running = True
    while running:

        #evet handling
        for event in pygame.event.get():
            
            #handle exit
            if event.type == pygame.QUIT:
                running = False
        
            #handle mouse click to add walls
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos

                    col = mouse_x // CELL_SIZE
                    row = mouse_y // CELL_SIZE
                
                    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                        if (row, col) != start and (row, col) != goal:
                            if grid[row][col] == 0:
                                grid[row][col] = 1
                            else:
                                grid[row][col] = 0
                            
                            #reset visuals after mouse click
                            current_path = []   #final path
                            visited_order = []  #list returned by bfs
                            explore_index = 0   #how many we've shown
                            exploring = False   #are we still animating?
            
            #button for bfs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    visited_order, current_path = bfs(grid, start, goal)
                    print("BFS visited nodes:", len(visited_order))
                    print("BFS path length:", len(current_path))
                    
                    #start exploring
                    explore_index = 0
                    exploring = True

        visited_set = set()
        path_set = set()

        if visited_order:
            if exploring:
                explore_index += ANIMATION_SPEED
                if explore_index >= len(visited_order):
                    explore_index = len(visited_order)
                    exploring = False
            
            visited_set = set(visited_order[:explore_index])

            if not exploring and current_path:
                path_set = set(current_path)

        #clear window (paint background)                
        window.fill((30,30,30))

        #draw cells on the grid
        draw_grid(window, grid, start, goal, visited_set, current_path)
        
        #display the grid
        pygame.display.flip()

        #limit loop to 60 fps
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
     main()