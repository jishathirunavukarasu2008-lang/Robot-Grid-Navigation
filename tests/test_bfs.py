from src.bfs import bfs


# Test 1: A path should exist
def test_path_exists():

    grid = [
        ['S', '.', '.'],
        ['#', '#', '.'],
        ['.', '.', 'G']
    ]

    start = (0, 0)
    goal = (2, 2)

    path, explored = bfs(grid, start, goal)

    assert path is not None
    assert path[0] == start
    assert path[-1] == goal


# Test 2: No path should exist
def test_no_path():

    grid = [
        ['S', '#', '.'],
        ['#', '#', '#'],
        ['.', '.', 'G']
    ]

    start = (0, 0)
    goal = (2, 2)

    path, explored = bfs(grid, start, goal)

    assert path is None


# Test 3: Path must avoid obstacles
def test_path_avoids_obstacles():

    grid = [
        ['S', '.', '#'],
        ['.', '.', '#'],
        ['#', '.', 'G']
    ]

    start = (0, 0)
    goal = (2, 2)

    path, explored = bfs(grid, start, goal)

    assert path is not None

    for row, col in path:
        assert grid[row][col] != '#'