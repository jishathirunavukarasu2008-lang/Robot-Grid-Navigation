# Robot Grid Navigation Using Breadth-First Search

## 1. Aim

To develop an Artificial Intelligence based robot navigation system that finds a path from a starting position to a destination on a grid containing obstacles using Breadth-First Search.

## 2. Problem Statement

A robot is placed on a two-dimensional grid containing free cells, obstacles, a starting position, and a destination.

The robot must find a valid path from the starting position `S` to the destination `G` while avoiding obstacles.

The problem is formulated as a search problem and solved using Breadth-First Search (BFS).

## 3. Objectives

- Represent robot navigation as an AI search problem.
- Model the grid as a state space.
- Define valid robot movements as actions.
- Use BFS to search for a path.
- Avoid obstacle cells during navigation.
- Find the shortest path when a path exists.
- Test the algorithm using different grid configurations.
- Analyse the search results.

## 4. AI Problem Formulation

### Initial State

The initial state is the position of the robot represented by `S`.

### Goal State

The goal state is the destination represented by `G`.

### States

Each valid cell in the grid represents a possible state.

A state can be represented using:

(row, column)

### Actions

The robot can move in four directions:

- Up
- Down
- Left
- Right

Diagonal movement is not allowed.

### Transition Model

An action moves the robot from its current cell to a neighbouring valid cell.

A movement is valid when the new cell:

- lies inside the grid,
- is not an obstacle,
- and has not already been visited.

### Path Cost

Each movement has a cost of 1.

Therefore, the total path cost is equal to the number of movements.

### Goal Test

The search is successful when the robot reaches the destination cell `G`.

## 5. Search Algorithm

Breadth-First Search (BFS) is used for robot navigation.

BFS explores states level by level using a queue.

Since every movement has equal cost, BFS finds a shortest path when a path exists.

## 6. Algorithm Steps

1. Place the starting cell into the queue.
2. Mark the starting cell as visited.
3. Remove a cell from the front of the queue.
4. Check whether the current cell is the goal.
5. If it is the goal, reconstruct the path.
6. Otherwise, examine its valid neighbouring cells.
7. Mark unvisited neighbours as visited.
8. Store their parent information.
9. Add them to the queue.
10. Continue until the goal is found or the queue becomes empty.

## 7. Grid Representation

The grid contains:

- `S` – starting position
- `G` – goal position
- `#` – obstacle
- `.` – free cell
- `*` – path found by BFS

Example:

    S . . # .
    . # . # .
    . # . . .
    . . # # .
    . . . . G

## 8. Experimental Results

Three different grid configurations were tested.

| Experiment | Grid Type | Path Found | Path Length | Nodes Expanded | Runtime |
|---|---|---|---:|---:|---:|
| 1 | Simple Grid | Yes | 6 | 14 | 0.000081 s |
| 2 | Obstacle Grid | Yes | 8 | 17 | 0.000064 s |
| 3 | No Path Grid | No | N/A | 1 | 0.000010 s |

## 9. Result Analysis

### Simple Grid

BFS successfully found a path of length 6 while expanding 14 nodes.

### Obstacle Grid

BFS successfully navigated around obstacles and found a path of length 8 while expanding 17 nodes.

### No Path Grid

BFS correctly determined that no path was available.

## 10. Testing

The implementation was tested using automated tests.

All three tests passed successfully.

## 11. Conclusion

The project demonstrates how robot movement can be formulated as an Artificial Intelligence search problem.

The grid is represented as a state space, robot movements are represented as actions, and BFS is used to explore the possible states.

The experimental results demonstrate that BFS can find a shortest path when a valid path exists and can identify cases where the destination is unreachable.
