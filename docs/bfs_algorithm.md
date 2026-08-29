# BFS Algorithm

## 1. What is BFS?

Breadth-First Search (BFS) is an uninformed search algorithm that explores states level by level.

For the robot navigation problem, BFS starts from the robot's initial position and explores all reachable neighbouring cells before moving to the next level.

## 2. Why BFS?

BFS is suitable for this problem because:

- The robot moves one cell at a time.
- Every movement has the same cost.
- BFS finds the shortest path in an unweighted grid.
- Obstacles can be treated as blocked states.

## 3. Data Structures

The implementation uses:

- Queue: Stores states that need to be explored.
- Visited Set: Prevents the same cell from being explored repeatedly.
- Parent Dictionary: Stores how each cell was reached so that the final path can be reconstructed.

## 4. BFS Procedure

1. Add the starting position to the queue.
2. Mark the starting position as visited.
3. Remove the first position from the queue.
4. Check whether it is the goal.
5. Generate its valid neighbouring cells.
6. Ignore cells outside the grid.
7. Ignore obstacle cells.
8. Ignore already visited cells.
9. Add valid cells to the queue.
10. Store the parent of each newly discovered cell.
11. Continue until the goal is reached or the queue becomes empty.
12. Reconstruct the path using the parent information.

## 5. Pseudocode

START

Create an empty queue

Add START to queue

Mark START as visited

Set parent of START to NULL

WHILE queue is not empty:

    Remove the first cell from queue

    IF current cell is GOAL:

        Stop search

    Generate neighbouring cells

    FOR each neighbour:

        IF neighbour is inside the grid
        AND neighbour is not an obstacle
        AND neighbour is not visited:

            Mark neighbour as visited

            Store current cell as its parent

            Add neighbour to queue

IF GOAL was not reached:

    Return no path

ELSE:

    Start from GOAL

    Follow parent cells backwards

    Reverse the resulting path

    Return the path

END