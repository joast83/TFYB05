import math

from em_visualisering.theory_pages import _circle_overlap_fraction


def test_circle_overlap_fraction_full():
    assert _circle_overlap_fraction(1.0, 0.0, 0.2) == 1.0


def test_circle_overlap_fraction_zero():
    assert _circle_overlap_fraction(1.0, 1.4, 0.2) == 0.0


def test_circle_overlap_fraction_partial():
    value = _circle_overlap_fraction(1.0, 1.0, 1.0)
    expected = 2.0 / 3.0 - math.sqrt(3.0) / (2.0 * math.pi)
    assert math.isclose(value, expected, rel_tol=1e-12)
