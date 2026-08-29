import time
from bfs import bfs


# -----------------------------
# Grid
# -----------------------------

grid = [
    ['S', '.', '.', '#', '.'],
    ['.', '#', '.', '#', '.'],
    ['.', '#', '.', '.', '.'],
    ['.', '.', '#', '#', '.'],
    ['.', '.', '.', '.', 'G']
]


# Start and goal
start = (0, 0)
goal = (4, 4)


# -----------------------------
# Run BFS and measure time
# -----------------------------

start_time = time.perf_counter()

path, explored = bfs(grid, start, goal)

end_time = time.perf_counter()

runtime = end_time - start_time


# -----------------------------
# Display Original Grid
# -----------------------------

print("\nROBOT GRID NAVIGATION")
print("=====================")

print("\nOriginal Grid:")

for row in grid:
    print(" ".join(row))


# -----------------------------
# Display Result
# -----------------------------

if path is None:

    print("\nNo path found!")

else:

    # Mark final path
    for row, col in path:

        if grid[row][col] not in ['S', 'G']:
            grid[row][col] = '*'

    print("\nFinal Path:")

    for row in grid:
        print(" ".join(row))


    # -----------------------------
    # Search Statistics
    # -----------------------------

    print("\nSearch Results")
    print("-------------")

    print("Algorithm       :", "BFS")
    print("Path Found      :", "Yes")
    print("Path Length     :", len(path) - 1)
    print("Nodes Expanded  :", len(explored))
    print("Runtime         :", f"{runtime:.6f}", "seconds")