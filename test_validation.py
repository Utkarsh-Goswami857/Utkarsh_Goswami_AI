# Tests for timetable validation

from data.sample_data import (
    DAYS,
    PERIODS,
    COURSES,
    ROOMS,
)

from ai.csp import create_variables, solve_csp
from ai.constraints import validate_timetable


def test_validator_accepts_valid_generated_timetable():
    """A valid generated timetable should have no violations."""

    result = solve_csp(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
    )

    if not result["success"]:
        assert result["timetable"] == {}
        return

    violations = validate_timetable(
        result["timetable"],
        result["variables"],
        ROOMS,
        COURSES,
    )

    assert violations == []


def test_validator_detects_unknown_variable():
    """An unknown timetable variable should be rejected."""

    variables = create_variables(COURSES)

    timetable = {
        "Unknown_Course_1": {
            "room": "VED-202",
            "day": "Monday",
            "period": "09:00-10:00",
        }
    }

    violations = validate_timetable(
        timetable,
        variables,
        ROOMS,
        COURSES,
    )

    assert len(violations) > 0


def test_validator_detects_unknown_room():
    """An assignment to an unknown room should be rejected."""

    variables = create_variables(COURSES)

    timetable = {
        "Mathematics_1": {
            "room": "UNKNOWN-ROOM",
            "day": "Monday",
            "period": "09:00-10:00",
        }
    }

    violations = validate_timetable(
        timetable,
        variables,
        ROOMS,
        COURSES,
    )

    assert len(violations) > 0
    
    