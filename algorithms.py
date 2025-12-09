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

        # remove current from current from queue
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
                        # noinspection PyTypeChecker
                        parents[(next_row, next_col)] = (current_row, current_col)
                        queue.append((next_row, next_col))  # add next (r, c) to the queue

    # no solution (didn't reach goal), return the explored cells
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

    # stack for DFS (LIFO)
    stack = [start]

    # dictionary: cell -> parent
    parents = {start: None}

    # visited cells in order
    visited_order = []

    # up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # while stack is not empty
    while stack:
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

    # no solution: goal never reached
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

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def Astar(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    # priority queue: (f_score, g_score, (row, col))
    open_heap = []
    start_h = heuristic(start, goal)
    heapq.heappush(open_heap, (start_h, 0, start))

    # # dictionary of cell -> parent
    parents = {start: None}

    # g_score: cost from start to this node
    g_score = {start: 0}

    # visited cells in order
    visited_order = []

    # directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_heap:
        f, g, current = heapq.heappop(open_heap)
        current_row, current_col = current

        # record expansion order
        visited_order.append(current)

        # goal reached
        if current == goal:
            break

        # explore neighbors
        for dr, dc in directions:
            nr = current_row + dr
            nc = current_col + dc

            # bounds check
            if 0 <= nr < rows and 0 <= nc < cols:
                # skip walls
                if grid[nr][nc] == 1:
                    continue

                neighbor = (nr, nc)
                possible_g = g + 1  # cost of one step

                # if this path to neighbor is better
                if neighbor not in g_score or possible_g < g_score[neighbor]:
                    
                    # record it
                    g_score[neighbor] = possible_g
                    parents[neighbor] = current
                    
                    # recalculate heuristic and f score
                    h = heuristic(neighbor, goal)
                    f_new = possible_g + h
                    
                    # add to open set
                    heapq.heappush(open_heap, (f_new, possible_g, neighbor))

    # no path found
    if goal not in parents:
        return visited_order, []

    # reconstruct path from goal back to start
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()

    return visited_order, path