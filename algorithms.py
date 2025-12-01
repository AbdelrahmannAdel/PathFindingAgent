from collections import deque

# bfs
def bfs(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    queue = deque()
    queue.append(start)

    # hashmap of each cell with its parent
    parents = {start: None}

    # visited cells
    visited_order = []

    # up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # while queue is not empty
    while queue:

        current_row, current_col = queue.popleft()
        visited_order.append((current_row, current_col))

        # goal reached
        if (current_row, current_col) == goal:
            break

        # explore neighbors, next (r, c) = direction + current (r, c)
        for row_direction, col_direction in directions:
            next_row = current_row + row_direction
            next_col = current_col + col_direction

            # bounds check
            # if the next (r, c) is out of bounds, try next direction
            if 0 <= next_row < rows and 0 <= next_col < cols:
                # if next (r, c)not a wall
                if grid[next_row][next_col] == 0:
                    # if next (r, c) is not a parent
                    if (next_row, next_col) not in parents:
                        # add current (r, c) as parent of next (r, c)
                        parents[(next_row, next_col)] = (current_row, current_col)
                        queue.append((next_row, next_col))  # add next (r, c) to the queue

    # no path
    if goal not in parents:
        return visited_order, []

    # reconstruct path
    path = []
    current_cell = goal
    while current_cell is not None:
        path.append(current_cell)
        current_cell = parents[current_cell]
    path.reverse()

    return visited_order, path
