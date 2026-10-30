"""Regressioner för de kontrollpunkter som verifierats mot original-PDF:en."""

from em_visualisering.guidance import guidance_for_class_name
from em_visualisering.modes import supports_3d_view
from em_visualisering.problems import SemiCircularSurfaceAxis
from em_visualisering.study_content import PROBLEM_STATEMENTS


def test_problem_2_4_has_no_off_axis_3d_model():
    assert not supports_3d_view(SemiCircularSurfaceAxis())
    assert "draw_3d" not in SemiCircularSurfaceAxis.__dict__


def test_problem_2_5_uses_source_integral_over_dq():
    question = PROBLEM_STATEMENTS["2.5"]
    assert "dQ" in question
    assert "källområdet" in question
    assert "Gauss sats" in question


def test_problem_2_10_source_figure_has_negative_cavity_shift():
    guide = guidance_for_class_name("OffsetCavitySphereExterior")
    assert "−d" in guide.geometry_hint
    assert "x+d" in guide.setup_hint


def test_problem_2_18_describes_two_alternative_experiments():
    question = PROBLEM_STATEMENTS["2.18"]
    assert "batteriet kopplas bort" in question
    assert "i stället för" in question


def test_problem_2_19_preserves_v0_boundary_condition():
    question = PROBLEM_STATEMENTS["2.19"]
    assert "V0" in question
    guide = guidance_for_class_name("UniformSpaceChargePlates")
    assert "0<x0<d" in guide.hints[2]
