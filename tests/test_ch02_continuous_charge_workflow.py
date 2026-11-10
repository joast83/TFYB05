"""Regression checks for the continuous-source method in exercises 2.2–2.5."""

import re

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
        ("ChargedRingAxis", r"\overline E(\overline r)"),
        ("FiniteLineCharge2D", r"\overline E(\overline r)"),
        ("SemiCircularSurfaceAxis", r"\overline E(\overline r)"),
        ("SphericalShellPotential", r"V(\overline r)"),
    ],
)
def test_guidance_starts_from_general_continuous_source_integral(class_name, equation):
    guide = guidance_for_class_name(class_name)
    assert equation in guide.start_here
    assert r"\mathrm dQ^{\prime}" in guide.start_here
    assert r"\overline r-\overline r^{\prime}" in guide.start_here
    assert r"|\overline r-\overline r^{\prime}|" in guide.start_here
    # First find the source charge element; then the separation and its norm.
    assert re.search(r"\\mathrm dQ\^{\\prime}\s*=", guide.hints[0])
    assert re.search(r"\\overline r-\\overline r\^{\\prime}\s*=", guide.hints[1])
    assert re.search(r"\|\\overline r-\\overline r\^{\\prime}\|\s*=", guide.hints[1])
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
        assert r"{|\overline r-\overline r^{\prime}|^3}" in guidance_for_class_name(cls).start_here
    assert r"\int\frac{\mathrm dQ^{\prime}}{|\overline r-\overline r^{\prime}|}" in guidance_for_class_name("SphericalShellPotential").start_here
