# Tests for timetable quality scoring

from data.sample_data import (
    DAYS,
    PERIODS,
    COURSES,
    ROOMS,
    FACULTY_PREFERENCES,
)

from ai.csp import create_variables, solve_csp
from utils.scoring import evaluate_timetable


def test_scoring_returns_expected_metrics():
    """Scoring should return all expected metric fields."""

    variables = create_variables(COURSES)

    result = solve_csp(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
    )

    if not result["success"]:
        assert result["timetable"] == {}
        return

    metrics = evaluate_timetable(
        result["timetable"],
        variables,
        FACULTY_PREFERENCES,
        PERIODS,
    )

    expected_keys = {
        "quality_score",
        "total_penalty",
        "empty_periods",
        "consecutive_difficult",
        "faculty_violations",
        "course_distribution_penalty",
    }

    assert expected_keys.issubset(metrics.keys())


def test_quality_score_is_between_zero_and_one_hundred():
    """The quality score should remain within its defined range."""

    variables = create_variables(COURSES)

    result = solve_csp(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
    )

    if not result["success"]:
        return

    metrics = evaluate_timetable(
        result["timetable"],
        variables,
        FACULTY_PREFERENCES,
        PERIODS,
    )

    assert 0 <= metrics["quality_score"] <= 100


def test_penalty_is_non_negative():
    """The total soft-constraint penalty cannot be negative."""

    variables = create_variables(COURSES)

    result = solve_csp(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
    )

    if not result["success"]:
        return

    metrics = evaluate_timetable(
        result["timetable"],
        variables,
        FACULTY_PREFERENCES,
        PERIODS,
    )

    assert metrics["total_penalty"] >= 0