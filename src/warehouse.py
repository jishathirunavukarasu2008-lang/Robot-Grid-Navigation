
"""Warehouse environment for the multi-robot planning extension."""

ROWS = 6
COLS = 8

GRID = [
    "........",
    ".##...#.",
    "...#....",
    ".#......",
    "...##.#.",
    "........",
]

STARTS = {
    "R1": (0, 0),
    "R2": (5, 0),
}

DROP_LOCATION = (2, 7)
CHARGING_STATION = (5, 7)

# A and B are logical warehouse zones.
TASKS = {
    "T1": {
        "location": (0, 6),
        "weight": 2,
        "zone": "A",
        "deadline": 20,
    },
    "T2": {
        "location": (5, 6),
        "weight": 1,
        "zone": "B",
        "deadline": 20,
    },
    "T3": {
        "location": (2, 4),
        "weight": 1,
        "zone": "A",
        "deadline": 45,
    },
}

ROBOTS = {
    "R1": {
        "capacity": 3,
        "zones": {"A"},
    },
    "R2": {
        "capacity": 2,
        "zones": {"B"},
    },
}

DIRECTIONS = [
    (-1, 0),  # Up
    (1, 0),   # Down
    (0, -1),  # Left
    (0, 1),   # Right
]


def is_valid_cell(position):
    """Return True if a cell is inside the grid and not an obstacle."""
    row, col = position

    return (
        0 <= row < ROWS
        and 0 <= col < COLS
        and GRID[row][col] != "#"
    )


def get_neighbors(position):
    """Return all valid neighboring cells."""
    row, col = position
    neighbors = []

    for dr, dc in DIRECTIONS:
        candidate = (row + dr, col + dc)

        if is_valid_cell(candidate):
            neighbors.append(candidate)

    return neighbors


def shortest_path(start, goal):
    """Find a shortest obstacle-free path using BFS."""
    from collections import deque

    if not is_valid_cell(start) or not is_valid_cell(goal):
        return None

    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    if goal not in parent:
        return None

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    return list(reversed(path))


def display_grid():
    """Display the warehouse map."""
    print("WAREHOUSE GRID")
    print("S = Robot start | # = Obstacle | . = Free cell")
    print()

    for row in range(ROWS):
        cells = []

        for col in range(COLS):
            position = (row, col)

            if GRID[row][col] == "#":
                cells.append("#")
            elif position == DROP_LOCATION:
                cells.append("D")
            elif position == CHARGING_STATION:
                cells.append("C")
            elif position in STARTS.values():
                cells.append("S")
            elif position in [
                task["location"] for task in TASKS.values()
            ]:
                cells.append("P")
            else:
                cells.append(".")

        print(" ".join(cells))


if __name__ == "__main__":
    display_grid()

    print("\nPath test: R1 to T1")
    path = shortest_path(STARTS["R1"], TASKS["T1"]["location"])

    if path:
        print("Path:", path)
        print("Movement steps:", len(path) - 1)
    else:
        print("No path found.")
