# Results

## Experimental Evaluation

The BFS robot navigation system was tested using different grid configurations.

The experiments were designed to evaluate:

- Whether a path can be found
- Path length
- Number of nodes expanded
- Runtime

## Experiment Results

| Experiment | Grid Type | Path Found | Path Length | Nodes Expanded | Runtime |
|---|---|---|---:|---:|---:|
| 1 | Simple Grid | Yes | | | |
| 2 | Obstacle Grid | Yes | | | |
| 3 | No Path Grid | No | N/A | | |

## Observations

### Experiment 1

BFS successfully found a path from the starting position to the destination.

### Experiment 2

BFS successfully navigated through a grid containing obstacles while avoiding blocked cells.

### Experiment 3

BFS correctly reported that no path exists when the destination could not be reached.

## Conclusion

The experiments demonstrate that BFS can successfully solve the robot grid navigation problem when a valid path exists.

The algorithm also correctly handles cases where the destination is unreachable.

The number of nodes explored and runtime depend on the structure and size of the grid.