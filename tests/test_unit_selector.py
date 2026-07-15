import pytest

from em_visualisering.registry import PROBLEMS
from em_visualisering.unit_scaling import (
    display_scale_by_unit,
    display_scale_for,
    selectable_display_scales,
)


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda problem: problem.__class__.__name__)
def test_declared_display_units_are_valid_and_round_trip(problem):
    for spec in problem.parameter_specs():
        scales = selectable_display_scales(
            spec.label, spec.default_si, spec.display_units
        )
        assert scales
        for scale in scales:
            assert scale.to_si(scale.to_display(spec.default_si)) == pytest.approx(
                spec.default_si
            )
            assert display_scale_by_unit(spec.label, scale.display_unit) == scale


def test_charge_selector_prefers_engineering_units_and_keeps_si_available():
    scales = selectable_display_scales(
        "Laddning Q [C]",
        30e-9,
        ("pC", "nC", "µC", "mC", "C"),
    )
    assert [scale.display_unit for scale in scales] == ["pC", "nC", "µC", "mC", "C"]
    assert display_scale_for("Laddning Q [C]", 30e-9).display_unit == "nC"


def test_unknown_declared_display_unit_fails_early():
    with pytest.raises(ValueError, match="stöds inte"):
        selectable_display_scales("Längd [m]", 1.0, ("inch",))
