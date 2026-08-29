# Complexity Analysis

## 1. Grid Representation

Let:

- R = number of rows in the grid
- C = number of columns in the grid

The total number of cells is:

V = R × C

Each cell can be considered as a state in the search problem.

## 2. Time Complexity

BFS visits each reachable cell at most once.

For each cell, the algorithm checks at most four neighbouring cells:

- Up
- Down
- Left
- Right

Therefore, the time complexity is:

O(R × C)

For a square grid of size N × N:

O(N²)

## 3. Space Complexity

BFS stores:

- Queue of cells waiting to be explored
- Visited cells
- Parent information
- Explored states

In the worst case, these structures may contain information for many cells.

Therefore, the space complexity is:

O(R × C)

For a square grid of size N × N:

O(N²)

## 4. Summary

| Measure | Complexity |
|---|---|
| Time Complexity | O(R × C) |
| Space Complexity | O(R × C) |
| Square Grid | O(N²) |

## 5. Interpretation

As the grid becomes larger, BFS may need to examine more cells.

Obstacles can reduce the number of reachable cells, while an open grid may require BFS to explore a larger portion of the search space.

BFS is appropriate for this project because every robot movement has equal cost and the algorithm guarantees a shortest path in terms of the number of movements.