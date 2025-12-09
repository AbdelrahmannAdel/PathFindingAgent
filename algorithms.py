from collections import deque
import heapq
# breadth first search
def bfs(grid, start, goal):
    
    rows = len(grid)
    cols = len(grid[0])

    # create the queue, add start cell - FIFO
    queue = deque()
    queue.append(start)

    # dictionary of cell -> parent
    parents = {start: None}

    # visited cells
    visited_order = []

    # up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # while queue is not empty
    while queue:

        # current coordinates = poped cell's coordinates
        current_row, current_col = queue.popleft()

        # add to visited
        visited_order.append((current_row, current_col))

        # goal reached
        if (current_row, current_col) == goal:
            break

        # explore neighbors, next (r, c) = direction + current (r, c)
        for row_dir, col_dir in directions:
            next_row = current_row + row_dir
            next_col = current_col + col_dir

            # bounds check
            # if the next (r, c) is out of bounds, try next direction
            if 0 <= next_row < rows and 0 <= next_col < cols:
                # if next (r, c) not a wall
                if grid[next_row][next_col] == 0:
                    # if next (r, c) is not a parent
                    if (next_row, next_col) not in parents:
                        # add current (r, c) as parent of next (r, c)
                        parents[(next_row, next_col)] = (current_row, current_col)
                        queue.append((next_row, next_col))  # add next (r, c) to the queue

    # no solution path, return explored cells
    if goal not in parents:
        return visited_order, []

    # if goal reached, build the solution path
    path = []
    current_cell = goal
    while current_cell is not None:
        path.append(current_cell)
        current_cell = parents[current_cell]
    path.reverse()

    return visited_order, path

# depth first search
def dfs(grid, start, goal):
   
    rows = len(grid)
    cols = len(grid[0])

    # stack for dfs - LIFO, add start
    stack = [start]

    # dictionary: cell -> parent
    parents = {start: None}

    # visited cells in order
    visited_order = []

    # up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # while stack is not empty
    while stack:
        
        # current coordinates = poped cell's coordinates
        current_row, current_col = stack.pop()

        # record visit
        visited_order.append((current_row, current_col))

        # goal reached
        if (current_row, current_col) == goal:
            break

        # explore neighbors
        for row_direction, col_direction in directions:
            next_row = current_row + row_direction
            next_col = current_col + col_direction

            # bounds check
            if 0 <= next_row < rows and 0 <= next_col < cols:
                # not a wall
                if grid[next_row][next_col] == 0:
                    # not visited yet (not in parents)
                    if (next_row, next_col) not in parents:
                        parents[(next_row, next_col)] = (current_row, current_col)
                        stack.append((next_row, next_col))

    # no solution path, return explored cells
    if goal not in parents:
        return visited_order, []

    # build path from goal back to start
    path = []
    current_cell = goal
    while current_cell is not None:
        path.append(current_cell)
        current_cell = parents[current_cell]
    path.reverse()

    return visited_order, path

# heuristic function for A*
def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* search
def astar(grid, start, goal):
    
    rows = len(grid)
    cols = len(grid[0])
    
    # calculate start heuristic
    start_h = heuristic(start, goal)
    
    # open set (priority queue)
    # takes tuples of (f, g, cell)
    open_set = []
    heapq.heappush(open_set, (start_h, 0, start))
    
    # best known g_cost from start to each cell
    g_cost = {start: 0}

    # dictionary: cell -> parent
    parents = {start: None}

    # visited cells in order (also closed set)
    visited_order = []
    
    # closed set
    closed_set = set()

    # up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while open_set:

        # get node with lowest f_score
        current_f, current_g, current = heapq.heappop(open_set)
        
        # if current is in closed set, skip it
        if current in closed_set:
            continue
        # if current is worse than best known g, skip it
        if current_g > g_cost.get(current, float("inf")):
            continue
        
        # add current to closed set
        closed_set.add(current)
        
        # add to visited
        visited_order.append(current)
        
        # goal reached
        if current == goal:
            break
        
        # get current coordinates
        current_row, current_col = current
        
        # explore neighbors
        for row_direction, col_direction in directions:
            next_row = current_row + row_direction
            next_col = current_col + col_direction
            
            # bounds check
            if 0 <= next_row < rows and 0 <= next_col < cols:
                # skip if a wall
                if grid[next_row][next_col] == 1:
                    continue
                
                # next cell
                neighbor = (next_row, next_col)

                if neighbor in closed_set:
                    continue
                    
                # new g, one step
                new_g = current_g + 1
                
                # if this path to neighbor is better than any other previous path                    
                if new_g < g_cost.get(neighbor, float("inf")):
                    
                    # update best known cost, update parent pointer
                    g_cost[neighbor] = new_g
                    parents[neighbor] = current
                    
                    # calculate f score for the neighbor
                    h = heuristic(neighbor, goal)
                    new_f = new_g + h
                    
                    # add neighbor to open set
                    heapq.heappush(open_set, (new_f, new_g, neighbor))
                    
    # no solution path, return explored cells
    if goal not in parents:
        return visited_order, []

    # build path from goal back to start
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
    
    return visited_order, path
