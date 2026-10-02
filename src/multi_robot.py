
"""Time-indexed multi-robot warehouse scheduler."""

from collections import deque

from warehouse import (
    ROBOTS,
    TASKS,
    STARTS,
    DROP_LOCATION,
    get_neighbors,
)
from csp_scheduler import solve_csp
from safety_rules import is_forbidden


MAX_TIME = 200


def find_time_path(start, goal, start_time, reservations):
    """Find a path that avoids reserved cells and opposite-direction swaps."""
    if is_forbidden(start) or is_forbidden(goal):
        return None

    initial = (start, start_time)
    queue = deque([initial])
    parent = {initial: None}
    final_state = None

    while queue:
        position, time = queue.popleft()

        if position == goal:
            # Ensure the destination is free for the next Pick/Drop action.
            if reservations.get(time + 1) != goal:
                final_state = (position, time)
                break

        if time >= MAX_TIME:
            continue

        for next_position in get_neighbors(position) + [position]:
            next_time = time + 1

            if is_forbidden(next_position):
                continue

            # Avoid another robot's reserved cell.
            if reservations.get(next_time) == next_position:
                continue

            # Avoid two robots swapping cells in the same time step.
            if (
                reservations.get(time) == next_position
                and reservations.get(next_time) == position
            ):
                continue

            state = (next_position, next_time)

            if state not in parent:
                parent[state] = (position, time)
                queue.append(state)

    if final_state is None:
        return None

    path = []
    current = final_state

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def schedule_robot(robot, assigned_tasks, reservations):
    """Build a time-indexed schedule for one robot."""
    position = STARTS[robot]
    time = 0
    schedule = [(0, robot, position, "Start")]
    explanation = [
        f"{robot} starts at {position}.",
        f"Assigned tasks: {assigned_tasks}.",
    ]

    for task in assigned_tasks:
        pickup = TASKS[task]["location"]

        # Travel to the pickup location.
        route = find_time_path(position, pickup, time, reservations)

        if route is None:
            return None, None, [
                f"{robot}: no safe route to pickup {task}."
            ]

        previous_cell = position

        for cell, arrival_time in route[1:]:
            action = "Wait" if cell == previous_cell else "Move"
            schedule.append((arrival_time, robot, cell, action))

            if action == "Wait":
                explanation.append(
                    f"Time {arrival_time}: {robot} waits at {cell} "
                    "to avoid a conflict."
                )
            else:
                explanation.append(
                    f"Time {arrival_time}: {robot} moves to {cell} "
                    f"en route to {task}."
                )

            previous_cell = cell

        time = route[-1][1]
        position = pickup

        # Pick action occupies the pickup cell for one time step.
        time += 1
        schedule.append((time, robot, position, f"Pick {task}"))
        explanation.append(
            f"Time {time}: {robot} picks up {task} at {position}."
        )

        # Travel to the drop-off location.
        route = find_time_path(
            position, DROP_LOCATION, time, reservations
        )

        if route is None:
            return None, None, [
                f"{robot}: no safe delivery route for {task}."
            ]

        previous_cell = position

        for cell, arrival_time in route[1:]:
            action = "Wait" if cell == previous_cell else "Move"
            schedule.append((arrival_time, robot, cell, action))

            if action == "Wait":
                explanation.append(
                    f"Time {arrival_time}: {robot} waits at {cell} "
                    "to avoid a conflict."
                )
            else:
                explanation.append(
                    f"Time {arrival_time}: {robot} moves to {cell} "
                    f"carrying {task}."
                )

            previous_cell = cell

        time = route[-1][1]
        position = DROP_LOCATION

        # Drop action occupies the drop-off cell for one time step.
        time += 1
        schedule.append((time, robot, position, f"Drop {task}"))
        explanation.append(
            f"Time {time}: {robot} delivers {task} at {position}."
        )

    return schedule, time, explanation


def expand_occupancy(schedule):
    """Include a robot's stationary occupancy between scheduled actions."""
    if not schedule:
        return {}

    occupancy = {}
    previous_time, _, previous_cell, _ = schedule[0]
    occupancy[previous_time] = previous_cell

    for time, robot, cell, action in schedule[1:]:
        for t in range(previous_time + 1, time):
            occupancy[t] = previous_cell

        occupancy[time] = cell
        previous_time = time
        previous_cell = cell

    return occupancy


def validate_conflicts(schedules):
    """Validate cell occupancy and opposite-direction movement conflicts."""
    occupied = {}
    expanded = []

    for schedule in schedules:
        robot = schedule[0][1]
        occupancy = expand_occupancy(schedule)
        expanded.append((robot, occupancy))

        for time, cell in occupancy.items():
            key = (time, cell)

            if key in occupied and occupied[key] != robot:
                return False, (
                    f"Shared-cell conflict: {occupied[key]} and {robot} "
                    f"both occupy {cell} at time {time}."
                )

            occupied[key] = robot

    # Check for robots swapping positions across a time step.
    for i in range(len(expanded)):
        robot_a, positions_a = expanded[i]

        for j in range(i + 1, len(expanded)):
            robot_b, positions_b = expanded[j]

            common_times = set(positions_a) & set(positions_b)

            for time in common_times:
                next_time = time + 1

                if (
                    next_time in positions_a
                    and next_time in positions_b
                    and positions_a[time] == positions_b[next_time]
                    and positions_b[time] == positions_a[next_time]
                    and positions_a[time] != positions_b[time]
                ):
                    return False, (
                        f"Edge-swap conflict between {robot_a} and "
                        f"{robot_b} from time {time} to {next_time}."
                    )

    return True, "No shared-cell or edge-swap conflicts found."


def reserve_schedule(schedule, reservations):
    """Reserve each cell occupied by a robot at each time step."""
    occupancy = expand_occupancy(schedule)

    for time, cell in occupancy.items():
        if time in reservations and reservations[time] == cell:
            raise ValueError(
                f"Reservation conflict at time {time}, cell {cell}."
            )

        reservations[time] = cell


def main():
    print("=" * 55)
    print("MULTI-ROBOT WAREHOUSE PLANNER")
    print("=" * 55)

    assignment = solve_csp()

    if not assignment:
        print("CSP could not find a valid task assignment.")
        return

    tasks_by_robot = {robot: [] for robot in ROBOTS}

    for task, robot in assignment.items():
        tasks_by_robot[robot].append(task)

    print("\nCSP TASK ASSIGNMENT")
    for task, robot in assignment.items():
        print(f"{task} -> {robot}")

    reservations = {}
    all_schedules = []
    all_explanations = []
    completion_times = {}

    for robot in ROBOTS:
        tasks = tasks_by_robot[robot]

        if not tasks:
            continue

        schedule, finish_time, explanation = schedule_robot(
            robot, tasks, reservations
        )

        if schedule is None:
            print("\nSCHEDULING FAILED")
            for message in explanation:
                print("-", message)
            return

        all_schedules.append(schedule)
        all_explanations.extend(explanation)
        completion_times[robot] = finish_time

        reserve_schedule(schedule, reservations)

    print("\nTIME-INDEXED ROBOT SCHEDULES")

    for schedule in all_schedules:
        print()
        for time, robot, cell, action in schedule:
            print(
                f"Time {time:>3} | {robot} | "
                f"Position {cell} | {action}"
            )

    valid, message = validate_conflicts(all_schedules)

    print("\nCONFLICT VALIDATION")
    print(message)

    print("\nROBOT COMPLETION TIMES")
    for robot, finish_time in completion_times.items():
        print(f"{robot}: {finish_time} time steps")

    if completion_times:
        print(
            "Overall completion time (makespan):",
            max(completion_times.values()),
        )

    print("\nROBOT EXPLANATION LOG")
    for message in all_explanations:
        print("-", message)

    print(
        "\nNote: this is a deterministic schedule. "
        "Movement uncertainty and single-versus-multi-robot "
        "comparison will be added separately."
    )


if __name__ == "__main__":
    main()
