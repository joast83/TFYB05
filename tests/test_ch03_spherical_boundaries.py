"""Check physical constraints, not just the plotted formulas."""
import numpy as np
import pytest
from matplotlib.figure import Figure
from em_visualisering.core import EPS0
from em_visualisering.plotly_bridge import make_plotly_3d_figure
from em_visualisering.problems.ch03 import GroundedInnerSphereChargeSplit, DielectricFilledSphericalGap


@pytest.mark.parametrize('Q', [-2e-9, 0, 1e-9])
@pytest.mark.parametrize('eps_r', [1, 2.5, 8])
def test_surface_charges_conserve_outer_charge_and_ground_inner_sphere(Q, eps_r):
    inner, outer = GroundedInnerSphereChargeSplit.surface_charges(Q, eps_r)
    a = 0.13
    assert inner + outer == pytest.approx(Q, abs=1e-24)
    # Potential found by integrating the field through the dielectric and vacuum.
    potential = (-inner / eps_r * (1/a - 1/(3*a)) + outer/(3*a)) / (4*np.pi*EPS0)
    assert potential == pytest.approx(0, abs=1e-12)
    if Q:
        assert outer / inner == pytest.approx(2 / eps_r)


def test_grounded_sphere_plot_matches_answer_and_handles_uncharged_case():
    problem = GroundedInnerSphereChargeSplit()
    params = problem.defaults()
    fig = Figure()
    problem.plot(fig, params, 'Field')
    heights = [p.get_height() for p in fig.axes[0].patches]
    assert heights[1] / heights[0] == pytest.approx(0.8)
    params['Q'] = 0
    for render in (problem.plot, problem.draw_3d):
        fig = Figure()
        render(fig, params, 'Field')
        assert any('odefinierad' in t.get_text() for t in fig.axes[0].texts)
    make_plotly_3d_figure(problem, params, 'Field').to_json(validate=True)


@pytest.mark.parametrize('Q', [-1e-9, 1e-9])
def test_oppositely_charged_spheres_have_no_exterior_field(Q):
    problem = DielectricFilledSphericalGap()
    params = {**problem.defaults(), 'Q': Q}
    fig = Figure()
    problem.plot(fig, params, 'Field')
    r, e = fig.axes[0].lines[0].get_data()
    assert np.all(e[r >= params['b']] == 0)
    gap = r < params['b']
    flux = 2*np.pi*r[gap]**2*EPS0*(params['eps1']+params['eps2'])*e[gap]
    np.testing.assert_allclose(flux, Q)
    # The map uses field magnitude but must obey the same zero exterior condition.
    fig = Figure()
    problem.plot(fig, params, 'Map')
    image = fig.axes[0].images[0]
    data = np.asarray(image.get_array())
    x0, x1, z0, z1 = image.get_extent()
    x, z = np.meshgrid(np.linspace(x0, x1, data.shape[1]), np.linspace(z0, z1, data.shape[0]))
    assert np.all(data[np.hypot(x,z) > params['b']] == 0)
