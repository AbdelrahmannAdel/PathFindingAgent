import sys
import time
from grid import *
from grid_gui import *
from algorithms import *

ANIMATION_SPEED = 3

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

        # -- for evet handling --
        
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
                    
                    # convert pixel coordinates to cell coordinates
                    col = mouse_x // CELL_SIZE  
                    row = mouse_y // CELL_SIZE
                
                    # if cell not out of bounds
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

                    # run and measure speed of bfs
                    start_time = time.perf_counter()                    # record start time
                    visited_order, final_path = bfs(grid, start, goal)  # run bfs
                    end_time = time.perf_counter()                      # record end time
                    time_taken = (end_time - start_time) * 1000         # calculate time taken

                    print("BFS visited nodes:", len(visited_order))
                    print("BFS path length:", len(final_path))
                    print(f"BFS time: {time_taken:.2f} ms")
                    
                    #start exploring animation
                    explore_index = 0
                    exploring = True
                    
                # d (for dfs)
                if event.key == pygame.K_d:
                    
                    # run and measure speed of dfs
                    start_time = time.perf_counter()                    # record start time
                    visited_order, final_path = dfs(grid, start, goal)  # run dfs
                    end_time = time.perf_counter()                      # record end time
                    time_taken = (end_time - start_time) * 1000         # calculate time taken

                    print("DFS visited nodes:", len(visited_order))
                    print("DFS path length:", len(final_path))
                    print(f"DFS time: {time_taken:.2f} ms")
                    
                    #start exploring animation
                    explore_index = 0
                    exploring = True
                    
                # a (for A*)
                if event.key == pygame.K_a:
                    
                    # run and measure speed of A*
                    start_time = time.perf_counter()                        # record start time
                    visited_order, final_path = astar(grid, start, goal)    # run A*
                    end_time = time.perf_counter()                          # record end time
                    time_taken = (end_time - start_time) * 1000             # calculate time taken
                    
                    print("A* visited nodes:", len(visited_order))
                    print("A* path length:", len(final_path))
                    print(f"A* time: {time_taken:.2f} ms")
                    
                    #start exploring animation
                    explore_index = 0
                    exploring = True

        # -- for graphics --

        # rebuild sets for each frame
        visited_set = set()
        path_set = set()

        # if search worked (visited not empty)
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