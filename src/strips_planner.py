
"""STRIPS-style warehouse action planning and explanation log."""

from warehouse import (
    STARTS,
    TASKS,
    DROP_LOCATION,
    CHARGING_STATION,
)

from safety_rules import safe_shortest_path, explain_safety


ACTIONS = {
    "Move": {
        "preconditions": [
            "Destination is adjacent",
            "Destination is traversable",
            "Destination is not forbidden",
        ],
        "effects": [
            "Robot position changes to destination",
        ],
    },
    "Pick": {
        "preconditions": [
            "Robot is at the package location",
            "Robot is not already carrying a package",
            "Package weight does not exceed robot capacity",
        ],
        "effects": [
            "Package becomes carried",
            "Robot load increases",
        ],
    },
    "Drop": {
        "preconditions": [
            "Robot is at the drop-off location",
            "Robot is carrying a package",
        ],
        "effects": [
            "Package is delivered",
            "Robot load decreases",
        ],
    },
    "Charge": {
        "preconditions": [
            "Robot is at the charging station",
        ],
        "effects": [
            "Robot battery is restored",
        ],
    },
}


def explain_action(name):
    """Display an action's STRIPS-style preconditions and effects."""
    action = ACTIONS[name]

    print(f"\n{name.upper()} ACTION")
    print("Preconditions:")
    for condition in action["preconditions"]:
        print("  IF", condition)

    print("Effects:")
    for effect in action["effects"]:
        print("  THEN", effect)


def build_robot_plan(robot, task):
    """Build a safe nominal plan for one pickup and delivery."""
    start = STARTS[robot]
    pickup = TASKS[task]["location"]

    # First route: robot start to package.
    outbound = safe_shortest_path(start, pickup)

    if outbound is None:
        return None, [
            f"No safe route exists from {start} to pickup {pickup}."
        ]

    # Second route: package pickup to drop-off.
    delivery = safe_shortest_path(pickup, DROP_LOCATION)

    if delivery is None:
        return None, [
            f"No safe delivery route exists from {pickup} to "
            f"{DROP_LOCATION}."
        ]

    plan = []
    log = [
        f"Robot: {robot}",
        f"Task: {task}",
        f"Start: {start}",
        f"Pickup: {pickup}",
        f"Drop-off: {DROP_LOCATION}",
        "Reasoning: use safe shortest paths for both journey segments.",
    ]

    # Move to pickup.
    for cell in outbound[1:]:
        plan.append(("Move", cell))
        log.append(f"Move to {cell}: {explain_safety(cell)}")

    plan.append(("Pick", pickup))
    log.append(f"Pick package at {pickup}: robot has reached the pickup.")

    # Move to drop-off.
    for cell in delivery[1:]:
        plan.append(("Move", cell))
        log.append(f"Move to {cell}: {explain_safety(cell)}")

    plan.append(("Drop", DROP_LOCATION))
    log.append(
        f"Drop package at {DROP_LOCATION}: delivery goal reached."
    )

    return plan, log


def main():
    print("STRIPS ACTION DEFINITIONS")

    for action_name in ACTIONS:
        explain_action(action_name)

    # T1 is the first assigned task in the current warehouse setup.
    plan, explanation = build_robot_plan("R1", "T1")

    print("\nROBOT EXPLANATION LOG")
    for entry in explanation:
        print("-", entry)

    print("\nPLANNED ACTION SEQUENCE")

    if plan is None:
        print("No valid plan could be generated.")
        return

    for step, (action, location) in enumerate(plan, start=1):
        print(f"{step}. {action} at {location}")

    print("\nTotal planned actions:", len(plan))
    print(
        "Note: this is a nominal plan. Movement failures and "
        "multi-robot conflicts are handled in later modules."
    )


if __name__ == "__main__":
    main()
