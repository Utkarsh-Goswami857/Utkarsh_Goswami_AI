# Tests for the CSP backtracking solver

from data.sample_data import DAYS, PERIODS, COURSES, ROOMS
from ai.csp import (
    create_variables,
    create_domains,
    solve_csp,
)


def test_create_variables():
    """Every required weekly session should become a variable."""

    variables = create_variables(COURSES)

    expected_sessions = sum(
        course["sessions_per_week"]
        for course in COURSES.values()
    )

    assert len(variables) == expected_sessions


def test_create_domains():
    """Each variable should have a domain of possible assignments."""

    variables = create_variables(COURSES)

    domains = create_domains(
        variables,
        ROOMS,
        DAYS,
        PERIODS,
    )

    assert len(domains) == len(variables)

    for variable, domain in domains.items():
        assert isinstance(domain, list), variable
        assert len(domain) > 0, variable


def test_solver_returns_expected_result_structure():
    """The solver should return its result and performance metrics."""

    result = solve_csp(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
        use_mrv=True,
        use_forward_checking=True,
    )

    assert "success" in result
    assert "timetable" in result
    assert "variables" in result
    assert "nodes" in result
    assert "runtime" in result

    assert isinstance(result["nodes"], int)
    assert result["nodes"] >= 0

    assert result["runtime"] >= 0


def test_successful_solution_schedules_every_session():
    """A successful solution should schedule every session."""

    result = solve_csp(
        COURSES,
        ROOMS,
        DAYS,
        PERIODS,
        use_mrv=True,
        use_forward_checking=True,
    )

    if not result["success"]:
        assert result["timetable"] == {}
        return

    assert len(result["timetable"]) == len(result["variables"])

    for variable in result["variables"]:
        assert variable in result["timetable"]
        
        