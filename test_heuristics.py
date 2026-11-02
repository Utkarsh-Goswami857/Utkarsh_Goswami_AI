# Tests for CSP heuristics

from ai.heuristics import select_unassigned_variable


def test_mrv_selects_variable_with_smallest_domain():
    """MRV should select the variable with the smallest domain."""

    unassigned_variables = [
        "Mathematics_1",
        "Artificial Intelligence_1",
        "Database Systems_1"
    ]

    domains = {
        "Mathematics_1": [
            {"room": "R1", "day": "Monday", "period": "09:00"}
        ] * 10,

        "Artificial Intelligence_1": [
            {"room": "R1", "day": "Monday", "period": "09:00"}
        ] * 2,

        "Database Systems_1": [
            {"room": "R1", "day": "Monday", "period": "09:00"}
        ] * 5
    }

    selected = select_unassigned_variable(
        unassigned_variables,
        domains,
        {},
    )

    assert selected == "Artificial Intelligence_1"


def test_mrv_ignores_already_assigned_variables():
    """MRV should not select an already assigned variable."""

    unassigned_variables = [
        "Mathematics_1",
        "Artificial Intelligence_1"
    ]

    domains = {
        "Mathematics_1": [{"slot": 1}],
        "Artificial Intelligence_1": [{"slot": 1}] * 3
    }

    timetable = {
        "Mathematics_1": {
            "room": "R1",
            "day": "Monday",
            "period": "09:00"
        }
    }

    selected = select_unassigned_variable(
        unassigned_variables,
        domains,
        timetable
    )

    assert selected == "Artificial Intelligence_1"


def test_mrv_returns_none_when_all_variables_are_assigned():
    """MRV should return None when no variables remain."""

    selected = select_unassigned_variable(
        [],
        {},
        {}
    )

    assert selected is None