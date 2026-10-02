
"""Movement uncertainty and single-versus-multi-robot analysis.

Assumption: a failed movement attempt leaves the robot in its
current cell, and the robot retries until the move succeeds.
"""

import heapq

from warehouse import STARTS, TASKS, DROP_LOCATION, ROBOTS, get_neighbors
from safety_rules import safe_shortest_path, is_forbidden
from csp_scheduler import solve_csp
from multi_robot import schedule_robot, reserve_schedule


SUCCESS_PROBABILITY = 0.8
NUMBER_OF_ROUTES = 3


def find_alternative_routes(start, goal, limit=NUMBER_OF_ROUTES):
    """Return up to limit shortest simple routes that obey safety rules."""
    if is_forbidden(start) or is_forbidden(goal):
        return []

    # Heap entries: movement steps, route.
    queue = [(0, [start])]
    routes = []

    while queue and len(routes) < limit:
        cost, path = heapq.heappop(queue)
        current = path[-1]

        if current == goal:
            routes.append(path)
            continue

        for neighbor in get_neighbors(current):
            if is_forbidden(neighbor) or neighbor in path:
                continue

            new_path = path + [neighbor]
            heapq.heappush(
                queue,
                (len(new_path) - 1, new_path),
            )

    return routes


def expected_movement_cost(path):
    """Expected movement attempts when failed moves are retried."""
    if path is None:
        return float("inf")

    movement_steps = len(path) - 1
    return movement_steps / SUCCESS_PROBABILITY


def route_uncertainty_analysis():
    print("\n" + "=" * 55)
    print("MOVEMENT UNCERTAINTY AND ROUTE COST ANALYSIS")
    print("=" * 55)
    print(f"Movement success probability: {SUCCESS_PROBABILITY:.0%}")
    print(
        "Assumption: a failed move leaves the robot in place "
        "and it retries."
    )

    start = STARTS["R1"]
    goal = TASKS["T1"]["location"]
    routes = find_alternative_routes(start, goal)

    if not routes:
        print("No safe alternative routes were found.")
        return

    print(f"\nRoute: R1 start {start} -> T1 pickup {goal}")

    results = []

    for index, route in enumerate(routes, start=1):
        steps = len(route) - 1
        expected_cost = expected_movement_cost(route)
        results.append((expected_cost, index, route, steps))

        print(f"\nAlternative {index}:")
        print("  Path:", route)
        print("  Movement steps:", steps)
        print(f"  Expected movement attempts: {expected_cost:.2f}")

    best = min(results, key=lambda result: result[0])
    print(
        f"\nLowest expected movement cost: Alternative {best[1]} "
        f"({best[0]:.2f} attempts)."
    )


def single_robot_baseline():
    """Estimate one robot's sequential time for all tasks.

    This is a hypothetical baseline: it ignores the assigned-zone
    restrictions because no existing robot is allowed to handle
    every task.
    """
    position = STARTS["R1"]
    movement_steps = 0
    action_steps = 0

    for task in ("T1", "T2", "T3"):
        pickup = TASKS[task]["location"]

        route_to_pickup = safe_shortest_path(position, pickup)
        if route_to_pickup is None:
            return None

        route_to_drop = safe_shortest_path(pickup, DROP_LOCATION)
        if route_to_drop is None:
            return None

        movement_steps += len(route_to_pickup) - 1
        movement_steps += len(route_to_drop) - 1

        # One time step for picking and one for dropping each task.
        action_steps += 2
        position = DROP_LOCATION

    return movement_steps + action_steps


def multi_robot_baseline():
    """Calculate makespan using the existing multi-robot scheduler."""
    assignment = solve_csp()

    if not assignment:
        return None

    tasks_by_robot = {robot: [] for robot in ROBOTS}

    for task, robot in assignment.items():
        tasks_by_robot[robot].append(task)

    reservations = {}
    completion_times = []

    for robot in ROBOTS:
        tasks = tasks_by_robot[robot]

        if not tasks:
            continue

        schedule, finish_time, explanation = schedule_robot(
            robot, tasks, reservations
        )

        if schedule is None:
            print("Could not calculate multi-robot completion time:")
            for message in explanation:
                print("-", message)
            return None

        reserve_schedule(schedule, reservations)
        completion_times.append(finish_time)

    return max(completion_times) if completion_times else None


def completion_time_comparison():
    print("\n" + "=" * 55)
    print("SINGLE-ROBOT VS MULTI-ROBOT COMPLETION TIME")
    print("=" * 55)

    single_time = single_robot_baseline()
    multi_time = multi_robot_baseline()

    if single_time is None or multi_time is None:
        print("Could not calculate both completion times.")
        return

    print(
        f"Hypothetical single robot, all tasks sequentially: "
        f"{single_time} time steps"
    )
    print(
        f"Multi-robot schedule makespan: {multi_time} time steps"
    )
    print(
        "Note: the single-robot baseline ignores zone restrictions "
        "for comparison. It is not a feasible assignment under the "
        "current robot rules."
    )

    if single_time > 0:
        reduction = (single_time - multi_time) / single_time * 100
        print(f"Difference relative to single-robot baseline: {reduction:.1f}%")
        print(
            "A positive percentage means the multi-robot makespan "
            "is lower than this hypothetical baseline."
        )


def main():
    route_uncertainty_analysis()
    completion_time_comparison()


if __name__ == "__main__":
    main()
