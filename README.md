# Robot Grid Navigation & Multi-Robot Warehouse Planner

An Artificial Intelligence project that extends **Breadth-First Search (BFS) robot navigation** into a multi-robot warehouse planning system using Constraint Satisfaction Problems (CSP), STRIPS-style planning, safety rules, and movement uncertainty analysis.

## 1. Project Overview

Robot Grid Navigation models robot movement in a two-dimensional grid containing free cells and obstacles. The original implementation uses BFS to find a shortest path between a start position and a goal.

The extended project introduces multiple warehouse robots that must collect and deliver tasks while respecting task assignments, obstacle constraints, human-aware safety rules, and robot movement conflicts.

## 2. Key Features

- **BFS pathfinding:** Finds shortest paths on an obstacle grid when a route exists.
- **CSP task assignment:** Assigns warehouse tasks to robots using constraint propagation with AC-3 and backtracking.
- **Multi-robot scheduling:** Generates time-indexed robot movements and checks shared-cell and edge-swap conflicts.
- **STRIPS-style planning:** Represents Move, Pick, Drop, and Charge actions using preconditions and effects.
- **Safety reasoning:** Blocks cells that violate the simulated human-proximity safety rule.
- **Movement uncertainty:** Estimates expected movement attempts when each movement succeeds with a probability of 0.8.
- **Explanation logs:** Records robot movements, task pickups, deliveries, and waiting decisions.
- **Performance comparison:** Compares a hypothetical single-robot baseline with the multi-robot schedule.

## 3. AI Techniques Used

| Technique | Purpose |
|---|---|
| Breadth-First Search (BFS) | Find shortest grid paths with equal movement costs |
| Constraint Satisfaction Problem (CSP) | Assign tasks to eligible robots |
| AC-3 | Reduce inconsistent values in CSP domains |
| Backtracking | Search for a valid task assignment |
| STRIPS-style planning | Represent actions, preconditions, and effects |
| Rule-based reasoning | Enforce human-proximity safety constraints |
| Expected-cost analysis | Estimate movement attempts under uncertainty |

## 4. Warehouse Environment

The warehouse is represented as a two-dimensional grid.

- `.` — Free cell
- `#` — Obstacle
- Robot start positions — Initial robot locations
- Task locations — Pickup positions
- Drop location — Delivery destination

The warehouse configuration, task definitions, robot capacities, zone restrictions, and movement functions are defined in `src/warehouse.py`.

## 5. Multi-Robot Task Assignment

The warehouse contains three tasks: T1, T2, and T3.

The current CSP solution assigns:

| Task | Assigned Robot |
|---|---|
| T1 | R1 |
| T2 | R2 |
| T3 | R1 |

The assignment respects the configured robot capacities and zone restrictions. AC-3 reduces the CSP domains, while backtracking is used to search for a valid assignment.

## 6. Multi-Robot Scheduling and Safety

The scheduler generates a time-indexed schedule for each robot.

It checks for:
- Two robots occupying the same cell at the same time.
- Two robots swapping positions along the same edge during the same time interval.
- Unsafe cells near the simulated human position.
- Waiting when a reserved cell would otherwise create a conflict.

The safety model uses an illustrative human position in the grid. It is a simulation, not a connection to a real human-detection sensor.

## 7. STRIPS-Style Action Planning

The planning module represents warehouse actions using preconditions and effects.

| Action | Purpose |
|---|---|
| Move | Navigate to a neighboring cell |
| Pick | Collect a task at its pickup location |
| Drop | Deliver a collected task |
| Charge | Represent a charging action |

The planner also produces an explanation log describing the actions in a robot's plan.

## 8. Movement Uncertainty Analysis

The uncertainty experiment assumes that:
- Each movement succeeds independently with probability 0.8.
- A failed movement leaves the robot in its current cell.
- The robot retries until the required movement succeeds.

For a route containing \(d\) movement steps, the expected number of movement attempts is:

\[
E[\text{attempts}] = \frac{d}{0.8}
\]

For the six-step route from R1's starting position to T1:

- Required movement steps: 6
- Movement success probability: 80%
- Expected movement attempts: 7.50

This is an analytical estimate under the stated assumptions, not a measurement from a physical robot.

## 9. Single-Robot vs Multi-Robot Comparison

The current experiment reports:

| Metric | Result |
|---|---:|
| Hypothetical single-robot completion time | 37 time steps |
| Multi-robot schedule makespan | 27 time steps |
| Difference | 10 time steps |
| Relative reduction against baseline | 27.0% |

**Important:** The single-robot baseline ignores the configured zone restrictions. It is a hypothetical comparison, not a feasible task assignment under the current robot rules. The comparison uses deterministic schedule times and does not incorporate random movement failures.

## 10. Project Structure

```text
Robot-Grid-Navigation/
├── docs/
│   ├── problem_formulation.md
│   ├── bfs_algorithm.md
│   ├── complexity.md
│   ├── results.md
│   ├── reflection.md
│   └── flowchart.md
├── src/
│   ├── bfs.py
│   ├── main.py
│   ├── experiments.py
│   ├── plot_results.py
│   ├── visualizer.py
│   ├── warehouse.py
│   ├── csp_scheduler.py
│   ├── multi_robot.py
│   ├── safety_rules.py
│   ├── strips_planner.py
│   └── uncertainty_analysis.py
├── tests/
│   └── test_bfs.py
├── .gitignore
└── README.md
```

## 11. Requirements

- Python 3
- `pytest` for automated testing
- Any additional packages required by the existing visualization or Flask modules

Install pytest if needed:

```bash
python -m pip install pytest
```

## 12. How to Run

Run these commands from the project root directory.

**Run the original BFS application:**

```bash
python src/main.py
```

**Run the CSP task assignment and multi-robot scheduler:**

```bash
python src/multi_robot.py
```

**Run the STRIPS-style planner:**

```bash
python src/strips_planner.py
```

**Run the human-aware safety rules:**

```bash
python src/safety_rules.py
```

**Run movement uncertainty and completion-time analysis:**

```bash
python src/uncertainty_analysis.py
```

**Run the automated tests:**

```bash
python -m pytest tests -v
```

## 13. Test Results

The existing BFS test suite has been executed successfully.

- `test_path_exists` — Passed
- `test_no_path` — Passed
- `test_path_avoids_obstacles` — Passed

**Result: 3 tests passed.**

The Python source files also compiled successfully, and the multi-robot scheduler reported no shared-cell or edge-swap conflicts for the tested configuration.

## 14. Limitations and Future Improvements

- Integrate real sensor data for human detection instead of illustrative coordinates.
- Add stochastic simulation to observe actual movement failures and retries.
- Extend scheduling and reservation validation to larger numbers of robots.
- Integrate battery consumption, charging decisions, and dynamic obstacles into the active scheduler.
- Add more automated tests for CSP assignments, safety constraints, STRIPS actions, and multi-robot conflicts.
- Improve visualization of robot paths and time-indexed schedules.

## 15. Conclusion

This project demonstrates how AI search, constraint satisfaction, action planning, rule-based safety reasoning, and uncertainty analysis can be combined in a warehouse navigation problem.

It extends a basic BFS implementation into a multi-robot planning prototype while retaining the original grid-navigation functionality. The current results are simulation-based and provide a foundation for further testing and development.
