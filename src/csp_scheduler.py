
"""CSP task allocation using AC-3 and backtracking."""

from collections import deque
from warehouse import ROBOTS, TASKS, shortest_path, STARTS, DROP_LOCATION


def task_cost(robot, task):
    """Estimate movement steps from robot start, to pickup, then drop-off."""
    pickup = TASKS[task]["location"]
    first = shortest_path(STARTS[robot], pickup)
    second = shortest_path(pickup, DROP_LOCATION)

    if first is None or second is None:
        return float("inf")

    return len(first) - 1 + len(second) - 1


def compatible(robot, task):
    """Check capacity, zone and estimated deadline for an individual task."""
    info = TASKS[task]
    robot_info = ROBOTS[robot]

    return (
        info["weight"] <= robot_info["capacity"]
        and info["zone"] in robot_info["zones"]
        and task_cost(robot, task) <= info["deadline"]
    )


def build_domains():
    """Create possible robot assignments for each task."""
    return {
        task: [
            robot for robot in ROBOTS
            if compatible(robot, task)
        ]
        for task in TASKS
    }


def pair_compatible(task_a, robot_a, task_b, robot_b):
    """Check whether two tasks can be assigned to the same robot."""
    if robot_a != robot_b:
        return True

    combined_weight = (
        TASKS[task_a]["weight"] + TASKS[task_b]["weight"]
    )

    return combined_weight <= ROBOTS[robot_a]["capacity"]


def revise(domains, task_a, task_b):
    """Remove assignments without support in a neighboring task domain."""
    revised = False

    for robot_a in domains[task_a][:]:
        supported = any(
            pair_compatible(task_a, robot_a, task_b, robot_b)
            for robot_b in domains[task_b]
        )

        if not supported:
            domains[task_a].remove(robot_a)
            revised = True

    return revised


def ac3(domains):
    """Enforce arc consistency over every pair of task variables."""
    queue = deque(
        (a, b)
        for a in domains
        for b in domains
        if a != b
    )

    while queue:
        task_a, task_b = queue.popleft()

        if revise(domains, task_a, task_b):
            if not domains[task_a]:
                return False

            for other in domains:
                if other != task_a and other != task_b:
                    queue.append((other, task_a))

    return True


def assignment_is_valid(assignment):
    """Check all assigned tasks and aggregate robot capacities."""
    for task, robot in assignment.items():
        if not compatible(robot, task):
            return False

    for robot in ROBOTS:
        assigned_tasks = [
            task for task, owner in assignment.items()
            if owner == robot
        ]

        total_weight = sum(
            TASKS[task]["weight"] for task in assigned_tasks
        )

        if total_weight > ROBOTS[robot]["capacity"]:
            return False

    return True


def backtracking(domains, assignment=None):
    """Search for a complete valid task assignment."""
    if assignment is None:
        assignment = {}

    if len(assignment) == len(TASKS):
        return assignment.copy() if assignment_is_valid(assignment) else None

    unassigned = [
        task for task in TASKS if task not in assignment
    ]

    # Choose the task with the fewest available robots.
    task = min(unassigned, key=lambda t: len(domains[t]))

    for robot in domains[task]:
        candidate = {**assignment, task: robot}

        if not assignment_is_valid(candidate):
            continue

        # Check binary constraints against already assigned tasks.
        valid = all(
            pair_compatible(task, robot, other_task, other_robot)
            for other_task, other_robot in assignment.items()
        )

        if not valid:
            continue

        result = backtracking(domains, candidate)

        if result is not None:
            return result

    return None


def solve_csp():
    domains = build_domains()

    print("INITIAL CSP DOMAINS")
    for task, robots in domains.items():
        print(f"{task}: {robots}")

    if any(not values for values in domains.values()):
        print("\nNo solution: a task has no eligible robot.")
        return None

    if not ac3(domains):
        print("\nNo solution found by AC-3.")
        return None

    print("\nDOMAINS AFTER AC-3")
    for task, robots in domains.items():
        print(f"{task}: {robots}")

    assignment = backtracking(domains)

    print("\nCSP TASK ASSIGNMENT")

    if assignment is None:
        print("No valid assignment satisfies the constraints.")
        return None

    for task, robot in assignment.items():
        print(f"{task} -> {robot}")

    print("\nVALIDATION")
    print("All tasks assigned:", len(assignment) == len(TASKS))
    print("All task restrictions satisfied:", assignment_is_valid(assignment))

    for robot in ROBOTS:
        tasks = [
            task for task, owner in assignment.items()
            if owner == robot
        ]
        weight = sum(TASKS[t]["weight"] for t in tasks)

        print(
            f"{robot}: tasks={tasks}, "
            f"load={weight}/{ROBOTS[robot]['capacity']}"
        )

    return assignment


if __name__ == "__main__":
    solve_csp()
