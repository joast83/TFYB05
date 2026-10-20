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


def test_faraday_state_resolves_flux_by_coil_angle():
    from em_visualisering.theory_pages import _faraday_state

    args = (0.01, 2.0, 100, 0.02, 0.1)
    _, flux_normal, emf_normal = _faraday_state(*args, angle_deg=0.0)
    _, flux_perpendicular, emf_perpendicular = _faraday_state(*args, angle_deg=90.0)
    assert abs(flux_normal) > 0
    assert abs(emf_normal) > 0
    assert abs(flux_perpendicular) < 1e-15
    assert abs(emf_perpendicular) < 1e-12


def test_gauss_default_is_one_positive_charge_at_origin():
    from em_visualisering.theory_pages import GAUSS_DEFAULT_CHARGES

    assert GAUSS_DEFAULT_CHARGES == {(0.0, 0.0): 5.0}


def test_gauss_sphere_encloses_center_and_flags_boundary_charge():
    from em_visualisering.theory_pages import _gauss_enclosed_charge

    assert _gauss_enclosed_charge(1.0, {(0.0, 0.0): 5.0, (1.5, 0.0): -2.0}) == (5.0, False)
    assert _gauss_enclosed_charge(1.0, {(1.0, 0.0): 3.0}) == (0.0, True)


def test_gauss_grid_selection_parsing_and_coordinate_mapping():
    from em_visualisering.theory_pages import (
        _gauss_grid_index_from_selection,
        _gauss_grid_position,
        _toggle_gauss_charge,
        _selection_points,
    )

    assert _selection_points({"selection": {"points": [{"point_index": 220}]}}) == [
        {"point_index": 220}
    ]
    assert _gauss_grid_index_from_selection(
        [{"curve_number": 3, "customdata": [220]}], grid_trace_index=3
    ) == 220
    assert _gauss_grid_index_from_selection(
        [{"curveNumber": 2, "pointNumber": 14}], grid_trace_index=3
    ) is None
    assert _gauss_grid_index_from_selection(
        [{"point_number": 14}], grid_trace_index=3
    ) == 14
    assert _gauss_grid_position(220) == (0.0, 0.0)
    assert _gauss_grid_position(0) == (-2.5, -2.5)
    assert _gauss_grid_position(440) == (2.5, 2.5)
    charges = {(0.0, 0.0): 5.0}
    charges = _toggle_gauss_charge(charges, (0.25, 0.0), -3.0)
    assert charges == {(0.0, 0.0): 5.0, (0.25, 0.0): -3.0}
    charges = _toggle_gauss_charge(charges, (0.25, 0.0), 5.0)
    assert charges == {(0.0, 0.0): 5.0}


def test_gauss_detects_point_charge_on_surface_as_singular():
    from em_visualisering.theory_pages import _gauss_enclosed_charge

    enclosed, on_surface = _gauss_enclosed_charge(1.0, {(1.0, 0.0): 3.0})
    assert enclosed == 0.0
    assert on_surface


def test_electric_field_changes_with_charge_magnitude_and_sign():
    from em_visualisering.theory_pages import _electric_field_at

    positive = _electric_field_at(1.0, 0.0, {(0.0, 0.0): 2.0})
    doubled = _electric_field_at(1.0, 0.0, {(0.0, 0.0): 4.0})
    negative = _electric_field_at(1.0, 0.0, {(0.0, 0.0): -2.0})
    assert math.isclose(doubled[0], 2.0 * positive[0], rel_tol=1e-12)
    assert positive[0] > 0 and negative[0] < 0
