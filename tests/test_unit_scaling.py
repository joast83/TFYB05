import math

import pytest

from em_visualisering.unit_scaling import (
    display_scale_for,
    display_scales_for,
    suggested_step,
)


@pytest.mark.parametrize(
    ("label", "value_si", "expected_unit", "expected_display"),
    [
        ("Laddning Q [C]", 30e-9, "nC", 30.0),
        ("Längd [m]", 0.15, "cm", 15.0),
        ("Area [m²]", 2e-4, "cm²", 2.0),
        ("Massa [kg]", 1e-3, "g", 1.0),
        ("Fält [V/m]", 2e8, "MV/m", 200.0),
    ],
)
def test_engineering_scale_and_round_trip(label, value_si, expected_unit, expected_display):
    scale = display_scale_for(label, value_si)
    assert scale.display_unit == expected_unit
    assert scale.to_display(value_si) == pytest.approx(expected_display)
    assert scale.to_si(scale.to_display(value_si)) == pytest.approx(value_si)


def test_unsupported_unit_is_left_unchanged():
    scale = display_scale_for("Vinkel [grader]", 12.0)
    assert scale.factor == 1.0
    assert scale.label == "Vinkel [grader]"


def test_all_scale_candidates_include_si():
    scales = display_scales_for("Laddning [C]")
    assert any(scale.display_unit == "C" and scale.factor == 1.0 for scale in scales)
    assert any(scale.display_unit == "nC" for scale in scales)


def test_suggested_step_is_positive_and_finite():
    for value in (0.0, 1e-12, 3.0, 4e9):
        step = suggested_step(value)
        assert step > 0
        assert math.isfinite(step)
