
"""Rule-based safety reasoning for warehouse robots."""

from warehouse import is_valid_cell, get_neighbors


# Example human-detection input for simulation.
# These coordinates are illustrative, not real sensor detections.
HUMAN_POSITIONS = {(3, 5)}

SAFETY_MARGIN = 1


def manhattan_distance(a, b):
    """Calculate grid distance between two cells."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def human_nearby(cell, human_positions=None):
    """Rule premise: HumanNearby(cell)."""
    if human_positions is None:
        human_positions = HUMAN_POSITIONS

    return any(
        manhattan_distance(cell, human) <= SAFETY_MARGIN
        for human in human_positions
    )


def is_forbidden(cell, human_positions=None):
    """Apply HumanNearby(c) -> Forbidden(c)."""
    return not is_valid_cell(cell) or human_nearby(
        cell, human_positions
    )


def safe_neighbors(cell, human_positions=None):
    """Return adjacent cells that satisfy the safety rules."""
    return [
        neighbor
        for neighbor in get_neighbors(cell)
        if not is_forbidden(neighbor, human_positions)
    ]


def safe_shortest_path(start, goal, human_positions=None):
    """Find a shortest path while avoiding forbidden cells."""
    from collections import deque

    if is_forbidden(start, human_positions):
        return None

    if is_forbidden(goal, human_positions):
        return None

    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in safe_neighbors(current, human_positions):
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

    path.reverse()
    return path


def explain_safety(cell, human_positions=None):
    """Return a human-readable explanation of the safety decision."""
    if not is_valid_cell(cell):
        return f"Cell {cell} is forbidden because it is outside the free grid."

    if human_nearby(cell, human_positions):
        return (
            f"Cell {cell} is forbidden: HumanNearby({cell}) is true, "
            "so the safety rule blocks entry."
        )

    return (
        f"Cell {cell} is permitted: no human is detected within "
        f"the safety margin of {SAFETY_MARGIN} grid step(s)."
    )


if __name__ == "__main__":
    print("WAREHOUSE SAFETY RULE TEST")

    test_cells = [(2, 5), (2, 4), (0, 0)]

    for cell in test_cells:
        print(explain_safety(cell))

    start = (0, 0)
    goal = (2, 4)

    print("\nSafe route test:", start, "to", goal)
    path = safe_shortest_path(start, goal)

    if path:
        print("Safe path:", path)
        print("Movement steps:", len(path) - 1)
    else:
        print("No safe path found.")
