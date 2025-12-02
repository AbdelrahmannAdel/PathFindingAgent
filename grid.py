CELL_SIZE = 30
GRID_ROWS = 15
GRID_COLS = 15

#the grid
def create_grid():

    grid = []

    for r in range(GRID_ROWS):
        row = []
        for cols in range(GRID_COLS):
            row.append(0)
        grid.append(row)

    return grid
