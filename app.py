from flask import Flask, render_template
from src.bfs import bfs

app = Flask(__name__)

DEFAULT_GRID = [
    ["S", ".", ".", "#", "."],
    [".", "#", ".", "#", "."],
    [".", "#", ".", ".", "."],
    [".", ".", "#", "#", "."],
    [".", ".", ".", ".", "G"]
]


@app.route("/")
def home():

    grid = [row[:] for row in DEFAULT_GRID]

    start = (0, 0)
    goal = (4, 4)

    path, explored = bfs(grid, start, goal)

    if path:
        for row, col in path:
            if grid[row][col] not in ("S", "G"):
                grid[row][col] = "*"

        path_found = "Yes"
        path_length = len(path) - 1
    else:
        path_found = "No"
        path_length = "N/A"

    result = {
        "path_found": path_found,
        "path_length": path_length,
        "nodes_expanded": len(explored)
    }

    return render_template(
        "index.html",
        grid=grid,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)