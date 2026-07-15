import math

from em_visualisering.core import ProblemBase
from em_visualisering.parameters import ParameterSpec, normalize_parameter_specs


class ExampleProblem(ProblemBase):
    parameters = [
        ("q", "Laddning q [C]", 30e-9),
        ParameterSpec(
            key="radius",
            label="Radie [m]",
            default_si=0.2,
            minimum_si=0.01,
            maximum_si=2.0,
            step_si=0.01,
            control="slider",
            help_text="Geometrisk radie.",
        ),
    ]

    def validate(self, params):
        if params["q"] == 0:
            return "Laddningen får inte vara noll i denna exempelmodell."
        return None


def test_legacy_and_structured_parameters_can_coexist():
    specs = ExampleProblem().parameter_specs()
    assert [spec.key for spec in specs] == ["q", "radius"]
    assert specs[0].si_unit == "C"
    assert specs[1].control == "slider"
    assert ExampleProblem().defaults() == {"q": 30e-9, "radius": 0.2}


def test_generic_and_problem_specific_validation_are_combined():
    problem = ExampleProblem()
    issues = problem.validate_all({"q": 0.0, "radius": -1.0})
    messages = [issue.message for issue in issues]
    assert any("mindre än" in message for message in messages)
    # Generic errors short-circuit model-specific validation to avoid invalid calculations.
    assert not any("Laddningen" in message for message in messages)

    issues = problem.validate_all({"q": 0.0, "radius": 0.2})
    assert any("Laddningen" in issue.message for issue in issues)


def test_non_finite_values_are_rejected():
    problem = ExampleProblem()
    issues = problem.validate_all({"q": math.nan, "radius": 0.2})
    assert any(issue.severity == "error" and "ändligt" in issue.message for issue in issues)


def test_mapping_definitions_are_supported():
    specs = normalize_parameter_specs(
        [
            {
                "key": "frequency",
                "label": "Frekvens [Hz]",
                "default_si": 50.0,
                "minimum_si": 0.0,
            }
        ]
    )
    assert specs[0].key == "frequency"
    assert specs[0].minimum_si == 0.0


def test_ui_bounds_do_not_become_hard_validation_bounds():
    spec = ParameterSpec(
        key="length",
        label="Längd [m]",
        default_si=1.0,
        minimum_si=0.0,
        ui_minimum_si=0.1,
        ui_maximum_si=2.0,
        control="slider",
    )
    assert spec.validate(5.0) == []


def test_discrete_parameter_contract():
    spec = ParameterSpec(
        key="geometry",
        label="Geometri",
        default_si=1.0,
        control="select",
        choices=(1.0, 2.0),
        choice_labels=("Båge", "Slinga"),
        integer=True,
    )
    assert spec.choice_map == {"Båge": 1.0, "Slinga": 2.0}
    assert spec.validate(1.5)[0].severity == "error"
