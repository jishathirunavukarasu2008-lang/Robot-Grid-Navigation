
import os
import sys
from flask import Flask, render_template
from src.bfs import bfs

# Allow the warehouse modules to be imported from src.
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from multi_robot import schedule_robot, reserve_schedule, validate_conflicts
from csp_scheduler import solve_csp
from warehouse import (
    GRID, ROWS, COLS, STARTS, TASKS,
    DROP_LOCATION, CHARGING_STATION
)

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
    path, explored = bfs(grid, (0, 0), (4, 4))

    if path:
        for r, c in path:
            if grid[r][c] not in ("S", "G"):
                grid[r][c] = "*"

    result = {
        "path_found": "Yes" if path else "No",
        "path_length": len(path) - 1 if path else "N/A",
        "nodes_expanded": len(explored)
    }

    return render_template("index.html", grid=grid, result=result)


@app.route("/warehouse")
def warehouse_page():
    assignment = solve_csp()

    if not assignment:
        return "CSP could not find a valid task assignment.", 500

    tasks_by_robot = {robot: [] for robot in STARTS}

    for task, robot in assignment.items():
        tasks_by_robot[robot].append(task)

    reservations = {}
    schedules = []
    completion_times = {}
    explanations = []

    for robot in STARTS:
        assigned_tasks = tasks_by_robot[robot]

        if not assigned_tasks:
            continue

        schedule, finish_time, messages = schedule_robot(
            robot, assigned_tasks, reservations
        )

        if schedule is None:
            return (
                "<h2>Scheduling failed</h2><pre>"
                + "\n".join(messages)
                + "</pre><p><a href='/'>Back to BFS</a></p>",
                500
            )

        schedules.append(schedule)
        completion_times[robot] = finish_time
        explanations.extend(messages)
        reserve_schedule(schedule, reservations)

    valid, conflict_message = validate_conflicts(schedules)

    # Collect the actual cells visited by each robot.
    robot_cells = {"R1": set(), "R2": set()}
    route_details = {"R1": [], "R2": []}

    for schedule in schedules:
        for time, robot, position, action in schedule:
            robot_cells.setdefault(robot, set()).add(position)
            route_details.setdefault(robot, []).append({
                "time": time,
                "row": position[0],
                "col": position[1],
                "action": action
            })

    # Build the display from the actual warehouse map.
    display_grid = []

    for r in range(ROWS):
        display_row = []

        for c in range(COLS):
            pos = (r, c)
            label = "."
            classes = []

            if GRID[r][c] == "#":
                label = "#"
                classes.append("wall")
            else:
                robots_here = [
                    robot for robot, start in STARTS.items()
                    if start == pos
                ]

                if robots_here:
                    label = "/".join(robots_here)
                    classes.extend(
                        "robot1" if robot == "R1" else "robot2"
                        for robot in robots_here
                    )
                elif pos in [info["location"] for info in TASKS.values()]:
                    task_names = [
                        task for task, info in TASKS.items()
                        if info["location"] == pos
                    ]
                    label = "/".join(task_names)
                    classes.append("task")
                elif pos == DROP_LOCATION:
                    label = "DROP"
                    classes.append("drop")
                elif pos == CHARGING_STATION:
                    label = "CHG"
                    classes.append("charge")
                else:
                    for robot, cells in robot_cells.items():
                        if pos in cells:
                            classes.append(
                                "route1" if robot == "R1" else "route2"
                            )

            display_row.append({
                "label": label,
                "classes": " ".join(classes)
            })

        display_grid.append(display_row)

    robots = []

    for robot in STARTS:
        robots.append({
            "name": robot,
            "tasks": tasks_by_robot[robot],
            "finish": completion_times.get(robot, "Not assigned"),
            "color_class": "robot1" if robot == "R1" else "robot2",
            "route": route_details.get(robot, [])
        })

    makespan = max(completion_times.values(), default=0)

    return render_template(
        "warehouse.html",
        grid=display_grid,
        robots=robots,
        makespan=makespan,
        conflict_message=conflict_message,
        conflicts_valid=valid,
        explanations=explanations
    )


if __name__ == "__main__":
    app.run(debug=True)
