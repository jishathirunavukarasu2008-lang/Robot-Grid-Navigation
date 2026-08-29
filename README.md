# Robot Grid Navigation Using BFS

## 1. Introduction

Robot Grid Navigation is an Artificial Intelligence search problem in which a robot must find a path from a starting position to a destination while avoiding obstacles.

This project models robot movement as a state-space search problem and uses Breadth-First Search (BFS) to find a shortest path.

## 2. Problem Statement

A robot is placed on a two-dimensional grid containing free cells and obstacles.

The robot must navigate from the starting position `S` to the destination `G` without passing through obstacles.

The objective is to find a valid and shortest path.

## 3. AI Search Problem Formulation

The robot navigation problem is represented using:

| Component | Description |
|---|---|
| Initial State | Robot's starting cell `S` |
| Goal State | Destination cell `G` |
| States | Valid positions of the robot |
| Actions | Move Up, Down, Left, or Right |
| Transition Model | Move to a valid neighbouring cell |
| Path Cost | 1 for each movement |
| Search Algorithm | Breadth-First Search (BFS) |

## 4. Why BFS?

Breadth-First Search explores the grid level by level.

Since every robot movement has the same cost, BFS guarantees that the first path found to the goal is a shortest path.

## 5. Grid Representation

Example:

    S . . # .
    . # . # .
    . # . . .
    . . # # .
    . . . . G

Where:

- `S` = Starting position
- `G` = Goal position
- `#` = Obstacle
- `.` = Free cell
- `*` = Path found by BFS

## 6. Example Result

For the obstacle grid, BFS successfully finds a path.

    S . . # .
    * # . # .
    * # . . .
    * . # # .
    * * * * G

Search results:

- Algorithm: BFS
- Path Found: Yes
- Path Length: 8
- Nodes Expanded: 18

## 7. Experiments

Three grid configurations were tested.

| Experiment | Grid Type | Path Found | Path Length | Nodes Expanded |
|---|---|---|---:|---:|
| 1 | Simple Grid | Yes | 6 | 14 |
| 2 | Obstacle Grid | Yes | 8 | 17 |
| 3 | No Path Grid | No | N/A | 1 |

## 8. Project Structure

    Robot-Grid-Navigation/
    │
    ├── docs/
    │   ├── problem_formulation.md
    │   ├── bfs_algorithm.md
    │   ├── complexity.md
    │   ├── results.md
    │   ├── reflection.md
    │   ├── flowchart.md
    │   └── bfs_nodes_expanded.png
    │
    ├── src/
    │   ├── main.py
    │   ├── bfs.py
    │   ├── experiments.py
    │   └── plot_results.py
    │
    └── tests/

## 9. Testing

The project includes automated tests to verify the BFS implementation.

All tests pass successfully.

## 10. Conclusion

The project demonstrates how a real-world robot navigation problem can be formulated as an Artificial Intelligence search problem.

BFS successfully finds the shortest path when a path exists and correctly identifies cases where the destination cannot be reached.