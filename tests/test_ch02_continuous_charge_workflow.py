"""Regression checks for the continuous-source method in exercises 2.2–2.5."""

import pytest

from em_visualisering.guidance import guidance_for_class_name
from em_visualisering.modes import supports_geometry_view
from em_visualisering.problems.ch02 import (
    ChargedRingAxis,
    FiniteLineCharge2D,
    SemiCircularSurfaceAxis,
    SphericalShellPotential,
)
from em_visualisering.study_content import PROBLEM_STATEMENTS


@pytest.mark.parametrize(
    "class_name,equation",
    [
        ("ChargedRingAxis", "E(r)"),
        ("FiniteLineCharge2D", "E(r)"),
        ("SemiCircularSurfaceAxis", "E(r)"),
        ("SphericalShellPotential", "V(r)"),
    ],
)
def test_guidance_starts_from_general_continuous_source_integral(class_name, equation):
    guide = guidance_for_class_name(class_name)
    assert equation in guide.start_here
    assert "dQ′" in guide.start_here
    assert "r−r′" in guide.start_here
    assert "|r−r′|" in guide.start_here
    # First find the source charge element; then the separation and its norm.
    assert "dQ′=" in guide.hints[0]
    assert "r−r′=" in guide.hints[1]
    assert "|r−r′|=" in guide.hints[1]
    assert guide.setup_hint and guide.geometry_hint


def test_2_3_deprecated_geometry_is_not_offered():
    problem = FiniteLineCharge2D()
    assert not supports_geometry_view(problem)
    assert "draw_geometry" not in FiniteLineCharge2D.__dict__
    assert "Se figur nedan" not in PROBLEM_STATEMENTS["2.3"]
    for cls in (ChargedRingAxis, SemiCircularSurfaceAxis, SphericalShellPotential):
        assert supports_geometry_view(cls())


def test_integral_expressions_are_physically_distinct_for_field_and_potential():
    for cls in ("ChargedRingAxis", "FiniteLineCharge2D", "SemiCircularSurfaceAxis"):
        assert "/|r−r′|³" in guidance_for_class_name(cls).start_here
    assert "∫ dQ′/|r−r′|" in guidance_for_class_name("SphericalShellPotential").start_here
