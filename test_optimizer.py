# Tests for timetable optimizer

from data.sample_data import (
    DAYS,
    PERIODS,
    COURSES,
    ROOMS,
    FACULTY_PREFERENCES,
)

from ai.optimizer import generate_optimized_timetable


def test_optimizer_returns_expected_result_structure():
    """The optimizer should return the expected result fields."""

    result = generate_optimized_timetable(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
        FACULTY_PREFERENCES,
        attempts=2,
    )

    assert "success" in result
    assert "timetable" in result
    assert "runtime" in result
    assert "attempts_completed" in result

    assert result["runtime"] >= 0
    assert result["attempts_completed"] >= 0


def test_optimizer_returns_a_complete_timetable_when_successful():
    """A successful result should contain every required session."""

    result = generate_optimized_timetable(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
        FACULTY_PREFERENCES,
        attempts=2,
    )

    if result["success"]:
        expected_sessions = sum(
            course["sessions_per_week"]
            for course in COURSES.values()
        )

        assert len(result["timetable"]) == expected_sessions
    else:
        assert result["timetable"] == {}


def test_optimizer_returns_quality_metrics_when_successful():
    """A successful result should include quality metrics."""

    result = generate_optimized_timetable(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
        FACULTY_PREFERENCES,
        attempts=2,
    )

    if result["success"]:
        assert "metrics" in result

        metrics = result["metrics"]

        assert "quality_score" in metrics
        assert "total_penalty" in metrics
        
        