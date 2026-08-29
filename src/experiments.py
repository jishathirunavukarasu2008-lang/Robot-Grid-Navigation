import time
from bfs import bfs


def run_experiment(name, grid, start, goal):

    print("\n" + "=" * 45)
    print(name)
    print("=" * 45)

    start_time = time.perf_counter()

    path, explored = bfs(grid, start, goal)

    end_time = time.perf_counter()

    runtime = end_time - start_time

    if path is None:

        print("Path Found     : No")
        print("Nodes Expanded :", len(explored))
        print("Runtime        :", f"{runtime:.6f} seconds")

    else:

        print("Path Found     : Yes")
        print("Path Length    :", len(path) - 1)
        print("Nodes Expanded :", len(explored))
        print("Runtime        :", f"{runtime:.6f} seconds")


# --------------------------------
# Experiment 1: Simple Grid
# --------------------------------

grid1 = [
    ['S', '.', '.', '.'],
    ['.', '.', '#', '.'],
    ['.', '.', '#', '.'],
    ['.', '.', '.', 'G']
]

run_experiment(
    "Experiment 1 - Simple Grid",
    grid1,
    (0, 0),
    (3, 3)
)


# --------------------------------
# Experiment 2: More Obstacles
# --------------------------------

grid2 = [
    ['S', '.', '#', '.', '.'],
    ['.', '#', '#', '.', '.'],
    ['.', '.', '.', '.', '#'],
    ['#', '#', '.', '.', '.'],
    ['.', '.', '.', '#', 'G']
]

run_experiment(
    "Experiment 2 - Obstacle Grid",
    grid2,
    (0, 0),
    (4, 4)
)


# --------------------------------
# Experiment 3: No Path
# --------------------------------

grid3 = [
    ['S', '#', '.'],
    ['#', '#', '#'],
    ['.', '.', 'G']
]

run_experiment(
    "Experiment 3 - No Path",
    grid3,
    (0, 0),
    (2, 2)
)