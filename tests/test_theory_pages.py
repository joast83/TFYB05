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


def test_theory_registry_includes_the_four_new_topics():
    from em_visualisering.theory_pages import THEORY_PAGES

    keys = {page.key for page in THEORY_PAGES}
    assert {"potential_field", "dielectric_boundary", "biot_savart", "faraday_lenz"} <= keys


def test_dielectric_boundary_fields_satisfy_boundary_conditions():
    from em_visualisering.core import EPS0
    from em_visualisering.theory_pages import _dielectric_boundary_fields

    eps1, eps2, sigma_nc_m2 = 2.0, 5.0, 8.0
    e1n, e1t, e2n, e2t = _dielectric_boundary_fields(
        eps1, eps2, 4.0, 35.0, sigma_nc_m2
    )
    assert math.isclose(e1t, e2t, abs_tol=1e-12)
    displacement_jump = EPS0 * (eps2 * e2n - eps1 * e1n) * 1000
    assert math.isclose(displacement_jump, sigma_nc_m2 * 1e-9, rel_tol=1e-12)


def test_loop_axis_field_has_correct_center_and_reversal_limits():
    from em_visualisering.core import MU0
    from em_visualisering.theory_pages import _loop_axis_field

    assert math.isclose(_loop_axis_field(2.0, 0.5, 0.0), MU0 * 2.0 / (2 * 0.5))
    assert _loop_axis_field(-2.0, 0.5, 0.0) < 0
    assert math.isclose(
        _loop_axis_field(2.0, 0.5, 0.5), MU0 * 2.0 / (2 * 0.5 * 2**1.5)
    )


def test_faraday_state_obeys_lenz_sign_and_zero_crossings():
    from em_visualisering.theory_pages import _faraday_state

    b0, frequency, turns, area = 0.005, 2.0, 50, 0.01
    b_start, flux_start, emf_start = _faraday_state(b0, frequency, turns, area, 0.0)
    assert b_start == 0.0
    assert flux_start == 0.0
    assert emf_start < 0.0  # Increasing positive B produces a field in the -z direction.

    b_peak, flux_peak, emf_peak = _faraday_state(
        b0, frequency, turns, area, 1.0 / (4.0 * frequency)
    )
    assert math.isclose(b_peak, b0, rel_tol=1e-12)
    assert math.isclose(flux_peak, b0 * area, rel_tol=1e-12)
    assert abs(emf_peak) < 1e-12
