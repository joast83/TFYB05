import math

import pytest

from em_visualisering.modes import mode_options_for_problem
from em_visualisering.registry import PROBLEMS
from em_visualisering.unit_scaling import display_scale_for


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda problem: problem.__class__.__name__)
def test_problem_defaults_satisfy_parameter_contract(problem):
    specs = problem.parameter_specs()
    defaults = problem.defaults()

    assert specs
    assert set(defaults) == {spec.key for spec in specs}
    assert len(defaults) == len(specs)
    assert all(math.isfinite(float(value)) for value in defaults.values())

    errors = [
        issue.message
        for issue in problem.validate_all(defaults)
        if issue.severity == "error"
    ]
    assert not errors


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda problem: problem.__class__.__name__)
def test_default_display_units_round_trip(problem):
    for spec in problem.parameter_specs():
        scale = display_scale_for(spec.label, spec.default_si)
        assert scale.to_si(scale.to_display(spec.default_si)) == pytest.approx(spec.default_si)


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda problem: problem.__class__.__name__)
def test_every_problem_has_at_least_one_mode(problem):
    options = mode_options_for_problem(problem)
    assert options
    assert len({internal for _label, internal in options}) == len(options)


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda problem: problem.__class__.__name__)
def test_metadata_driven_controls_are_internally_consistent(problem):
    for spec in problem.parameter_specs():
        if spec.ui_minimum_si is not None:
            assert spec.default_si >= spec.ui_minimum_si
        if spec.ui_maximum_si is not None:
            assert spec.default_si <= spec.ui_maximum_si
        if spec.control == "log":
            assert spec.default_si > 0
            assert spec.ui_minimum_si is not None and spec.ui_minimum_si > 0
            assert spec.ui_maximum_si is not None
        if spec.control == "slider":
            assert spec.ui_minimum_si is not None
            assert spec.ui_maximum_si is not None
            assert spec.step_si is not None and spec.step_si > 0
        if spec.integer:
            assert float(spec.default_si).is_integer()


def test_catalog_includes_discrete_geometry_selector():
    problem = next(problem for problem in PROBLEMS if problem.__class__.__name__ == "CircularArcOnAxis")
    loop = next(spec for spec in problem.parameter_specs() if spec.key == "loop")
    assert loop.control == "select"
    assert loop.choice_map == {"Kvartsbåge": 1.0, "Hel slinga": 2.0}
