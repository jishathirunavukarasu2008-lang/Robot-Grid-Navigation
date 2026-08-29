import tkinter as tk
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

start = (0, 0)
goal = (4, 4)

CELL_SIZE = 70


# -----------------------------
# Window
# -----------------------------

root = tk.Tk()
root.title("Robot Grid Navigation - BFS")


rows = len(grid)
cols = len(grid[0])


# -----------------------------
# Canvas
# -----------------------------

canvas = tk.Canvas(
    root,
    width=cols * CELL_SIZE,
    height=rows * CELL_SIZE
)

canvas.pack(padx=20, pady=20)


# -----------------------------
# Draw Grid
# -----------------------------

def draw_grid():

    canvas.delete("all")

    for r in range(rows):

        for c in range(cols):

            x1 = c * CELL_SIZE
            y1 = r * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            cell = grid[r][c]

            if cell == '#':
                fill = "black"

            elif cell == 'S':
                fill = "green"

            elif cell == 'G':
                fill = "red"

            else:
                fill = "white"

            canvas.create_rectangle(
                x1, y1,
                x2, y2,
                fill=fill,
                outline="gray"
            )

            if cell == 'S':

                canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text="S",
                    font=("Arial", 20, "bold")
                )

            elif cell == 'G':

                canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text="G",
                    font=("Arial", 20, "bold")
                )


# -----------------------------
# Add / Remove Obstacles
# -----------------------------

def toggle_obstacle(event):

    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE

    if row >= rows or col >= cols:
        return

    if (row, col) == start or (row, col) == goal:
        return

    if grid[row][col] == '#':
        grid[row][col] = '.'

    else:
        grid[row][col] = '#'

    draw_grid()


# -----------------------------
# Find BFS Path
# -----------------------------

def find_path():

    path, explored = bfs(
        grid,
        start,
        goal
    )

    draw_grid()

    if path is None:

        result_label.config(
            text="❌ No path exists!"
        )

        return

    for row, col in path:

        if (row, col) == start or (row, col) == goal:
            continue

        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        canvas.create_rectangle(
            x1 + 3,
            y1 + 3,
            x2 - 3,
            y2 - 3,
            fill="yellow",
            outline="orange"
        )

        canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text="★",
            font=("Arial", 20, "bold")
        )

    result_label.config(
        text=(
            f"BFS | Path Length: {len(path) - 1} | "
            f"Nodes Expanded: {len(explored)}"
        )
    )


# -----------------------------
# Reset Grid
# -----------------------------

def reset_grid():

    global grid

    grid = [
        ['S', '.', '.', '#', '.'],
        ['.', '#', '.', '#', '.'],
        ['.', '#', '.', '.', '.'],
        ['.', '.', '#', '#', '.'],
        ['.', '.', '.', '.', 'G']
    ]

    result_label.config(
        text="Grid reset"
    )

    draw_grid()


# -----------------------------
# Button Area
# -----------------------------

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


find_button = tk.Button(
    button_frame,
    text="FIND PATH",
    command=find_path,
    font=("Arial", 11, "bold")
)

find_button.grid(
    row=0,
    column=0,
    padx=5
)


reset_button = tk.Button(
    button_frame,
    text="RESET",
    command=reset_grid,
    font=("Arial", 11)
)

reset_button.grid(
    row=0,
    column=1,
    padx=5
)


# -----------------------------
# Result
# -----------------------------

result_label = tk.Label(
    root,
    text="Click cells to add/remove obstacles",
    font=("Arial", 11)
)

result_label.pack(pady=5)


# -----------------------------
# Mouse Click
# -----------------------------

canvas.bind(
    "<Button-1>",
    toggle_obstacle
)


# -----------------------------
# Start
# -----------------------------

draw_grid()

root.mainloop()