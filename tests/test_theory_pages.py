import math
import numpy as np

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
        GAUSS_DEFAULT_CHARGES,
        _gauss_grid_index_from_selection,
        _gauss_cross_section_figure,
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
    figure = _gauss_cross_section_figure(1.0, GAUSS_DEFAULT_CHARGES, False, show_grid=True)
    grid_trace_index = len(figure.data) - 1
    assert figure.data[grid_trace_index].name == "Laddningsrutnät"
    assert _gauss_grid_index_from_selection(
        [{"curve_number": grid_trace_index, "customdata": [220]}], grid_trace_index
    ) == 220
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


def test_default_theory_figures_are_legible_on_fixed_references():
    from em_visualisering.theory_pages import (
        _ampere_figure,
        _biot_savart_figures,
        _faraday_figures,
    )

    ampere = _ampere_figure(1.0, 0.0, 0.15, 1, 2.0)
    assert list(ampere.layout.xaxis.range) == [-2.4, 2.4]
    assert list(ampere.layout.yaxis.range) == [-2.4, 2.4]
    assert ampere.layout.legend.orientation == "h"

    _, contributions, profile = _biot_savart_figures(3.0, 0.75, 0.5)
    assert list(contributions.layout.yaxis.range) == [-0.5, 0.5]
    assert list(profile.layout.yaxis.range) == [-7, 7]
    assert max(abs(value) for value in contributions.data[0].y) < 0.5

    waveform, _ = _faraday_figures(0.020, 4.5, 450, 0.045, 0.1, 0.0, -1.0)
    assert list(waveform.layout.yaxis.range) == [-22, 22]
    assert list(waveform.layout.yaxis2.range) == [-17, 17]
    assert max(abs(value) for value in waveform.data[1].y) > 10


def test_potential_changes_while_axes_remain_fixed():
    from em_visualisering.theory_pages import _potential_figures

    field_initial, _ = _potential_figures(2.0, -2.0, 1.0)
    field_changed, _ = _potential_figures(4.0, -2.0, 1.0)
    assert list(field_initial.layout.xaxis.range) == [-3, 3]
    assert list(field_changed.layout.xaxis.range) == [-3, 3]
    assert np.nanmax(np.abs(np.asarray(field_changed.data[0].z) - np.asarray(field_initial.data[0].z))) > 0


def test_zero_charges_do_not_mask_potential_or_field():
    from em_visualisering.theory_pages import _potential_figures

    field, profile = _potential_figures(0.0, 0.0, 1.0)
    assert np.isfinite(field.data[0].z).all()
    assert np.count_nonzero(field.data[0].z) == 0
    for trace in profile.data:
        assert np.isfinite(trace.y).all()
        assert np.count_nonzero(trace.y) == 0
    # Removing the right charge leaves a smooth, finite single-charge profile there.
    _, single = _potential_figures(2.0, 0.0, 1.0)
    near_removed = np.abs(np.asarray(single.data[0].x) - 0.5) < 0.08
    assert np.isfinite(np.asarray(single.data[0].y)[near_removed]).all()


def test_segment_contributions_sum_to_analytic_field():
    from em_visualisering.theory_pages import _biot_savart_figures, _loop_axis_field

    for current in (-5.0, 0.0, 5.0):
        for radius, z in ((0.5, 0.0), (1.0, -1.5), (0.75, 0.5)):
            _, bars, _ = _biot_savart_figures(current, radius, z)
            assert math.isclose(sum(bars.data[0].y),
                                _loop_axis_field(current, radius, z) * 1e6,
                                rel_tol=1e-12, abs_tol=1e-12)


def test_dielectric_zero_field_remains_labelled_and_vectors_stay_in_material():
    from em_visualisering.theory_pages import _dielectric_figure

    for e2n in (-126.0, 0.0, 126.0):
        fig = _dielectric_figure(4.0, 0.0, e2n, 0.0, 2.0, 5.0)
        assert any("E₂" in (a.text or "") for a in fig.layout.annotations)
        for a in fig.layout.annotations:
            if a.showarrow:
                assert a.ax * a.x > 0  # vectors stay in their own material
                assert abs(a.x) < 1.7


def test_all_theory_pages_render_with_streamlit():
    from streamlit.testing.v1 import AppTest
    from em_visualisering.theory_pages import THEORY_PAGES

    for page in THEORY_PAGES:
        app = AppTest.from_string(
            "from em_visualisering.theory_pages import THEORY_PAGES, render_theory_page\n"
            f"render_theory_page(THEORY_PAGES[{THEORY_PAGES.index(page)}])"
        ).run(timeout=30)
        assert not app.exception, page.key
        assert len(app.get("plotly_chart")) >= 1
        if page.key in ("gauss_flux", "stokes_magnetostatics"):
            app.radio[0].set_value("Testlabb").run()
        for extreme in ("max", "min"):
            for slider in app.slider:
                slider.set_value(getattr(slider, extreme))
            app.run(timeout=30)
            assert not app.exception, (page.key, extreme)


def test_gauss_coordinate_add_remove_and_reset():
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_string(
        "from em_visualisering.theory_pages import THEORY_PAGES, render_theory_page\n"
        "render_theory_page(THEORY_PAGES[0])"
    ).run(timeout=30)
    app.radio(key="gauss_section").set_value("Testlabb").run()
    assert app.session_state.gauss_charges == {(0.0, 0.0): 5.0}
    app.number_input(key="gauss_x").set_value(0.25).run()
    app.button(key="gauss_coordinate_toggle").click().run()
    assert app.session_state.gauss_charges[(0.25, 0.0)] == 5.0
    app.button(key="gauss_coordinate_toggle").click().run()
    assert (0.25, 0.0) not in app.session_state.gauss_charges
    app.button(key="gauss_clear_charges").click().run()
    assert app.session_state.gauss_charges == {}
    app.button(key="gauss_reset_charges").click().run()
    assert app.session_state.gauss_charges == {(0.0, 0.0): 5.0}
    assert not app.exception


def test_biot_cross_section_obeys_right_hand_rule():
    from em_visualisering.theory_pages import _biot_savart_section

    for current in (-3.0, 0.0, 3.0):
        fig = _biot_savart_section(current, 0.75, 0.5)
        arrows = [a for a in fig.layout.annotations if a.showarrow]
        if current == 0:
            assert not arrows
        else:
            assert (arrows[0].y - arrows[0].ay) * current > 0
            assert fig.data[0].text[1] == ("⊗" if current > 0 else "⊙")
