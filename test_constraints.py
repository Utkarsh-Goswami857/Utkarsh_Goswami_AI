# Tests for timetable hard constraints

import pytest

from data.sample_data import COURSES, ROOMS
from ai.csp import create_variables
from ai.constraints import is_valid_assignment


@pytest.fixture
def variables():
    """Create session variables for all courses."""
    return create_variables(COURSES)


@pytest.fixture
def empty_timetable():
    """Return an empty timetable."""
    return {}


def test_valid_mathematics_assignment(variables, empty_timetable):
    """A valid Mathematics assignment should be accepted."""

    result = is_valid_assignment(
        "Mathematics_1",
        "VED-202",
        "Monday",
        "09:00-10:00",
        empty_timetable,
        variables,
        ROOMS
    )

    assert result is True


def test_section_clash_is_rejected(variables):
    """Two classes from the same section cannot overlap."""

    timetable = {
        "Mathematics_1": {
            "room": "VED-202",
            "day": "Monday",
            "period": "09:00-10:00"
        }
    }

    result = is_valid_assignment(
        "Artificial Intelligence_1",
        "VED-203",
        "Monday",
        "09:00-10:00",
        timetable,
        variables,
        ROOMS
    )

    assert result is False


def test_insufficient_room_capacity_is_rejected(variables):
    """A room that is too small must be rejected."""

    result = is_valid_assignment(
        "Mathematics_1",
        "VED-203",
        "Tuesday",
        "09:00-10:00",
        {},
        variables,
        ROOMS
    )

    assert result is False


def test_laboratory_requires_lab_room(variables):
    """A laboratory session cannot use a classroom."""

    result = is_valid_assignment(
        "AI Laboratory_1",
        "VED-202",
        "Tuesday",
        "10:00-11:00",
        {},
        variables,
        ROOMS
    )

    assert result is False


def test_teacher_clash_is_rejected(variables):
    """A teacher cannot teach two sessions simultaneously."""

    timetable = {
        "Artificial Intelligence_1": {
            "room": "VED-202",
            "day": "Monday",
            "period": "09:00-10:00"
        }
    }

    result = is_valid_assignment(
        "AI Laboratory_1",
        "VED-505 LAB-1",
        "Monday",
        "09:00-10:00",
        timetable,
        variables,
        ROOMS
    )

    assert result is False


def test_room_clash_is_rejected(variables):
    """Two sessions cannot occupy the same room simultaneously."""

    timetable = {
        "Mathematics_1": {
            "room": "VED-202",
            "day": "Monday",
            "period": "09:00-10:00"
        }
    }

    result = is_valid_assignment(
        "Computer Networks_1",
        "VED-202",
        "Monday",
        "09:00-10:00",
        timetable,
        variables,
        ROOMS
    )

    assert result is False