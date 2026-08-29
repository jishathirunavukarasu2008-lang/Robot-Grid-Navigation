from collections import deque 
def bfs(grid, start, goal):

    rows = len(grid)
    cols = len(grid[0])

    queue = deque([start])
    visited = {start}
    parent = {start: None}

    explored = []

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:

        current = queue.popleft()

        explored.append(current)

        if current == goal:
            break

        row, col = current

        for dr, dc in directions:

            new_row = row + dr
            new_col = col + dc

            if not (0 <= new_row < rows and 0 <= new_col < cols):
                continue

            if grid[new_row][new_col] == '#':
                continue

            new_position = (new_row, new_col)

            if new_position in visited:
                continue

            visited.add(new_position)

            parent[new_position] = current

            queue.append(new_position)

    if goal not in parent:
        return None, explored

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path, explored