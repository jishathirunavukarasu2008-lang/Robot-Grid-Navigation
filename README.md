# Robot Grid Navigation & Multi-Robot Warehouse Planner

An Artificial Intelligence project that combines BFS pathfinding, constraint-based task assignment, multi-robot scheduling, and a Flask web interface for warehouse navigation.

## Project Overview

Robots operating in a warehouse must navigate around obstacles, collect items, and deliver them to a destination. When multiple robots operate together, their task assignments and movements must also be coordinated to avoid collisions.

This project implements AI techniques to solve these problems and presents the results through a browser-based interface.

## Features

- **BFS Pathfinding:** Finds a shortest path through an unweighted grid while avoiding obstacles.
- **CSP Task Assignment:** Assigns tasks to robots based on capacity and warehouse-zone restrictions.
- **AC-3 and Backtracking:** Used in the constraint satisfaction process to reduce inconsistent domains and search for valid assignments.
- **Multi-Robot Scheduling:** Creates time-indexed robot schedules with movement, waiting, pickup, and delivery actions.
- **Collision Validation:** Checks shared-cell occupancy and opposite-direction edge-swap conflicts.
- **STRIPS-Style Planning:** Defines actions such as Move, Pick, Drop, and Charge.
- **Movement Uncertainty Analysis:** Separately estimates expected movement attempts using a specified movement-success probability.
- **Flask Web Interface:** Displays BFS results and a visual warehouse-planning summary in the browser.

## Technologies Used

- Python
- Flask
- Breadth-First Search (BFS)
- Constraint Satisfaction Problems (CSP)
- AC-3 and backtracking
- Time-indexed scheduling
- HTML and CSS
- Pytest

## Project Structure

```text
Robot-Grid-Navigation/
├── app.py
├── src/
│   ├── bfs.py
│   ├── main.py
│   ├── csp_scheduler.py
│   ├── multi_robot.py
│   ├── safety_rules.py
│   ├── strips_planner.py
│   ├── uncertainty_analysis.py
│   ├── visualizer.py
│   └── warehouse.py
├── templates/
│   ├── index.html
│   └── warehouse.html
├── tests/
│   └── test_bfs.py
├── docs/
│   └── report.pdf
└── README.md
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/jishathirunavukarasu2008-lang/Robot-Grid-Navigation.git
cd Robot-Grid-Navigation
```

### 2. Install Flask and pytest

```bash
python -m pip install flask pytest
```

If a `requirements.txt` file is available, you can install dependencies with:

```bash
python -m pip install -r src/requirements.txt
```

### 3. Start the web application

```bash
python app.py
```

Open these URLs in your browser:

- **BFS Pathfinding:** http://127.0.0.1:5000/
- **Multi-Robot Warehouse Planner:** http://127.0.0.1:5000/warehouse

### 4. Run the multi-robot scheduler in the terminal

```bash
python src/multi_robot.py
```

### 5. Run the STRIPS-style planner

```bash
python src/strips_planner.py
```

### 6. Run movement uncertainty analysis

```bash
python src/uncertainty_analysis.py
```

### 7. Run automated tests

```bash
python -m pytest tests -v
```

## Web Interface

### BFS Pathfinding

The original page displays the grid, start and goal positions, obstacles, the path found by BFS, path length, and nodes expanded.

### Multi-Robot Warehouse Planner

The warehouse page uses the CSP assignment and time-indexed scheduler to display:

- Warehouse obstacles, robot start positions, and task locations.
- Assigned tasks for each robot.
- Computed robot schedules and actions.
- Robot completion times and overall makespan.
- Conflict-validation status.
- Detailed route and action logs.

The warehouse page visualizes the computed schedule when loaded. It does not currently animate robots in real time.

## Current Results

The current verified run produced the following results:

| Metric | Result |
|---|---|
| R1 task assignment | T1, T3 |
| R2 task assignment | T2 |
| R1 completion time | 27 time steps |
| R2 completion time | 13 time steps |
| Overall makespan | 27 time steps |
| Schedule conflict validation | No shared-cell or edge-swap conflicts found |
| BFS automated tests | 3 passed |

Results depend on the configured warehouse, task assignments, and scheduling logic.

## Complexity Analysis

For BFS on a graph with \(V\) vertices and \(E\) edges:

- **Time complexity:** \(O(V + E)\)
- **Space complexity:** \(O(V)\)

For a grid with a constant number of neighboring cells per position, BFS time and space are linear in the number of traversable cells.

Multi-robot scheduling includes time-indexed pathfinding and constraint-based task assignment. Its practical cost depends on the grid size, time horizon, reservations, and number of tasks. General CSP search can be exponential in the worst case.

## Limitations

- The warehouse is a simulated grid rather than a physical robot environment.
- The browser shows computed schedules but does not provide real-time robot animation.
- Human-proximity safety rules use configured positions, not live sensor data.
- Movement uncertainty is analyzed separately and is not simulated as live random movement by the scheduler.
- The current automated tests cover BFS behavior; they do not constitute exhaustive verification of every multi-robot scenario.

## Future Improvements

- Add animated robot movement and a simulation control panel.
- Add dynamic obstacle and human detection using sensor input.
- Expand automated tests for task assignment and collision handling.
- Improve route optimization and compare different scheduling strategies.
- Integrate movement uncertainty directly into the simulation.

## Responsible Use of AI and Sources

AI assistance was used during development for coding guidance, debugging, documentation, and project explanation. The project was tested locally; reported results refer to the outputs observed during testing.

## Author

**Jisha**  
BE Computer Science and Engineering (Artificial Intelligence and Machine Learning)