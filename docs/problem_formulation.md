# Problem Formulation

## 1. Problem Description

The problem is to navigate a robot from a starting position to a destination on a two-dimensional grid while avoiding obstacles.

The robot can move one cell at a time in four directions: up, down, left, and right.

Breadth-First Search (BFS) is used to find a path from the starting position to the destination.

## 2. Initial State

The initial state represents the starting position of the robot.

Example:

Start = (0, 0)

## 3. State

A state represents the current position of the robot on the grid.

For example:

(2, 3)

means the robot is located at row 2 and column 3.

## 4. Actions

The robot has four possible actions:

- Move Up
- Move Down
- Move Left
- Move Right

An action is allowed only when the destination cell is inside the grid and is not an obstacle.

## 5. Transition Model

The transition model describes how the robot moves from one state to another.

For example:

Current State = (2, 2)

Move Right

Next State = (2, 3)

The robot cannot transition into an obstacle cell.

## 6. Goal Test

The goal test checks whether the robot has reached the destination.

Example:

Goal = (4, 4)

If the robot reaches (4, 4), the search is successful.

## 7. Path Cost

Each movement from one cell to another has a cost of 1.

Therefore, the total path cost is the number of movements required to reach the destination.

BFS finds the shortest path when all movement costs are equal.

## 8. Search Algorithm

Breadth-First Search (BFS) is used for this problem.

BFS explores states level by level using a queue.

The first time BFS reaches the goal, it has found a shortest path in terms of the number of movements.