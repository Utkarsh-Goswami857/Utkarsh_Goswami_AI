# Tests for new faculty constraints, value ordering, and enhanced optimization

import pytest
from data.sample_data import DAYS, PERIODS, COURSES, ROOMS, FACULTY_PREFERENCES
from ai.csp import create_variables, solve_csp
from ai.constraints import is_valid_assignment, validate_timetable, check_consecutive_violation
from ai.heuristics import order_domain_values
from utils.scoring import evaluate_timetable
from ai.optimizer import generate_optimized_timetable


@pytest.fixture
def variables():
    return create_variables(COURSES)


def test_consecutive_violation_helper():
    """Verify check_consecutive_violation detects sequences > max_consecutive."""
    assert check_consecutive_violation([0, 1, 2], max_consecutive=2) is True
    assert check_consecutive_violation([0, 1], max_consecutive=2) is False
    assert check_consecutive_violation([0, 2, 4], max_consecutive=2) is False
    assert check_consecutive_violation([0, 1, 3, 4], max_consecutive=2) is False
    assert check_consecutive_violation([0, 1, 2, 3], max_consecutive=3) is True


def test_teacher_daily_load_constraint(variables):
    """Teacher cannot exceed max_daily_teacher_sessions on the same day."""
    test_vars = variables.copy()
    test_vars["AI_Seminar_1"] = {
        "teacher": "Dr. Himani Sharma",
        "section": "CSE-B",
        "students": 30,
        "room_type": "Classroom",
        "course": "AI Seminar",
        "session": 1
    }

    # Dr. Himani Sharma teaches Artificial Intelligence and AI Laboratory
    timetable = {
        "Artificial Intelligence_1": {
            "room": "VED-202",
            "day": "Monday",
            "period": "09:00-10:00"
        },
        "AI Laboratory_1": {
            "room": "VED-505 LAB-1",
            "day": "Monday",
            "period": "11:15-12:15"
        }
    }

    # If limit is 2, third assignment on Monday must be rejected
    is_valid = is_valid_assignment(
        "AI_Seminar_1",
        "VED-202",
        "Monday",
        "14:00-15:00",
        timetable,
        test_vars,
        ROOMS,
        max_daily_teacher_sessions=2,
        periods_list=PERIODS
    )
    assert is_valid is False

    # But on Tuesday, it should be valid
    is_valid_tue = is_valid_assignment(
        "AI_Seminar_1",
        "VED-202",
        "Tuesday",
        "14:00-15:00",
        timetable,
        test_vars,
        ROOMS,
        max_daily_teacher_sessions=2,
        periods_list=PERIODS
    )
    assert is_valid_tue is True


def test_teacher_consecutive_limit_constraint(variables):
    """Teacher cannot teach more consecutive sessions than max_consecutive_teacher_sessions."""
    test_vars = variables.copy()
    test_vars["AI_Seminar_1"] = {
        "teacher": "Dr. Himani Sharma",
        "section": "CSE-B",
        "students": 30,
        "room_type": "Classroom",
        "course": "AI Seminar",
        "session": 1
    }

    # Dr. Himani Sharma in periods 0 and 1
    timetable = {
        "Artificial Intelligence_1": {
            "room": "VED-202",
            "day": "Tuesday",
            "period": "09:00-10:00"  # index 0
        },
        "AI Laboratory_1": {
            "room": "VED-505 LAB-1",
            "day": "Tuesday",
            "period": "10:00-11:00"  # index 1
        }
    }

    # Assigning period 2 (11:15-12:15) would make 3 consecutive sessions
    is_valid = is_valid_assignment(
        "AI_Seminar_1",
        "VED-202",
        "Tuesday",
        "11:15-12:15",  # index 2
        timetable,
        test_vars,
        ROOMS,
        max_consecutive_teacher_sessions=2,
        periods_list=PERIODS
    )
    assert is_valid is False

    # Assigning period 4 (14:00-15:00) with a gap should be valid
    is_valid_gap = is_valid_assignment(
        "AI_Seminar_1",
        "VED-202",
        "Tuesday",
        "14:00-15:00",  # index 4 (after gap)
        timetable,
        test_vars,
        ROOMS,
        max_consecutive_teacher_sessions=2,
        periods_list=PERIODS
    )
    assert is_valid_gap is True


def test_order_domain_values_prioritizes_faculty_preference(variables):
    """LCV value ordering puts faculty preferred slots first."""
    # Dr. Seema Yadav prefers ("Monday", "09:00-10:00")
    candidate_slots = [
        {"room": "VED-202", "day": "Friday", "period": "14:00-15:00"},
        {"room": "VED-202", "day": "Monday", "period": "09:00-10:00"},
        {"room": "VED-202", "day": "Wednesday", "period": "11:15-12:15"}
    ]

    ordered = order_domain_values(
        "Mathematics_1",
        candidate_slots,
        {},
        variables,
        ROOMS,
        faculty_preferences=FACULTY_PREFERENCES,
        periods=PERIODS
    )

    # First choice should be the preferred slot
    assert ordered[0]["day"] == "Monday"
    assert ordered[0]["period"] == "09:00-10:00"


def test_validator_catches_overloaded_teacher():
    """Validator detects when a teacher is overloaded if limits are checked."""
    variables = create_variables(COURSES)
    timetable = {
        "Mathematics_1": {"room": "VED-202", "day": "Monday", "period": "09:00-10:00"},
        "Mathematics_2": {"room": "VED-202", "day": "Tuesday", "period": "09:00-10:00"},
        "Mathematics_3": {"room": "VED-202", "day": "Wednesday", "period": "09:00-10:00"},
        "Artificial Intelligence_1": {"room": "VED-202", "day": "Monday", "period": "10:00-11:00"},
        "Artificial Intelligence_2": {"room": "VED-202", "day": "Tuesday", "period": "11:15-12:15"},
        "AI Laboratory_1": {"room": "VED-505 LAB-1", "day": "Monday", "period": "12:15-13:15"},
        "Data Structures_1": {"room": "VED-202", "day": "Thursday", "period": "09:00-10:00"},
        "Data Structures_2": {"room": "VED-202", "day": "Friday", "period": "09:00-10:00"},
        "Data Structures_3": {"room": "VED-202", "day": "Thursday", "period": "10:00-11:00"},
        "Database Systems_1": {"room": "VED-202", "day": "Tuesday", "period": "10:00-11:00"},
        "Database Systems_2": {"room": "VED-202", "day": "Wednesday", "period": "11:15-12:15"},
        "Computer Networks_1": {"room": "VED-203", "day": "Monday", "period": "09:00-10:00"},
        "Computer Networks_2": {"room": "VED-203", "day": "Tuesday", "period": "09:00-10:00"},
        "Operating Systems_1": {"room": "VED-203", "day": "Monday", "period": "10:00-11:00"},
        "Operating Systems_2": {"room": "VED-203", "day": "Wednesday", "period": "10:00-11:00"},
        "Networks Laboratory_1": {"room": "VED-505 LAB-1", "day": "Thursday", "period": "14:00-15:00"},
        "Communication Skills_1": {"room": "VED-202", "day": "Friday", "period": "11:15-12:15"},
        "Environmental Studies_1": {"room": "VED-203", "day": "Friday", "period": "14:00-15:00"},
    }

    # Dr. Himani Sharma has 2 sessions on Monday: AI_1 and AI_Lab_1
    # If limit is 1, it will trigger violation
    violations = validate_timetable(
        timetable,
        variables,
        ROOMS,
        COURSES,
        max_daily_teacher_sessions=1,  # limit to 1
        periods_list=PERIODS
    )
    assert any("workload limit exceeded" in v.lower() for v in violations)


def test_optimizer_achieves_high_faculty_satisfaction():
    """Optimizer achieves high faculty satisfaction and zero hard violations."""
    result = generate_optimized_timetable(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
        FACULTY_PREFERENCES,
        attempts=3
    )

    assert result["success"] is True
    metrics = result["metrics"]
    assert metrics["faculty_satisfaction_rate"] >= 75.0
    assert metrics["teachers_satisfied"] >= 7
    assert metrics["faculty_idle_gaps"] <= 2
