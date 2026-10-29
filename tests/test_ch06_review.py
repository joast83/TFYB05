"""Physics and rendering regressions found while reviewing chapter 6."""
import numpy as np
import pytest
from matplotlib.figure import Figure
from em_visualisering.core import MU0
from em_visualisering.problems.ch06 import (
    FiniteWireBiotSavart, SquareLoopOnAxis, RightAngleWireCorner,
    ThinCurrentStripField, CircularArcOnAxis, RotatingChargedDisk,
)


def defaults(problem):
    return {key: value for key, _, value in problem.parameters}


@pytest.mark.parametrize('current', [-10., 0., 10.])
def test_finite_wire_magnitude_plot_includes_nonnegative_reference(current):
    problem = FiniteWireBiotSavart()
    fig = Figure()
    problem.plot(fig, dict(defaults(problem), I=current), 'Field')
    assert all(np.all(line.get_ydata() >= 0) for line in fig.axes[0].lines)
    if current == 0:
        assert fig.axes[0].get_yscale() == 'linear'
    fig.canvas.draw()


@pytest.mark.parametrize('current', [-3., 3.])
def test_square_axis_matches_vector_biot_savart(current):
    z = np.array([-.8, 0., .8])
    bx, by, bz = SquareLoopOnAxis._field_xz(np.zeros_like(z), z, current, .3)
    np.testing.assert_allclose(bx, 0, atol=1e-20)
    np.testing.assert_allclose(by, 0, atol=1e-20)
    np.testing.assert_allclose(bz, SquareLoopOnAxis._bz_axis(current, .3, z), rtol=2e-5)


def test_corner_magnitude_is_unsigned_and_matches_stated_example():
    positive = RightAngleWireCorner._bmag(5., .05)
    assert positive == pytest.approx(np.sqrt(2) * 1e-5)
    assert RightAngleWireCorner._bmag(-5., .05) == positive


@pytest.mark.parametrize('current', [-10., 0., 10.])
def test_strip_vector_sum_matches_both_exact_observation_points(current):
    a = .02
    bx, by = ThinCurrentStripField._field_xy(current, a, np.array([2*a, 0]), np.array([0, 2*a]))
    np.testing.assert_allclose(bx, [0, -ThinCurrentStripField.B_normal_plane(current, a, 2*a)], atol=1e-20, rtol=2e-6)
    np.testing.assert_allclose(by, [ThinCurrentStripField.B_in_plane(current, a, 2*a), 0], atol=1e-20, rtol=2e-6)


@pytest.mark.parametrize('z', [-.4, 0., .4])
def test_quarter_arc_matches_independent_vector_quadrature(z):
    n, a, current = 2000, .15, -2.
    step = np.pi / (2*n)
    phi = (np.arange(n) + .5) * step
    source = np.stack([a*np.cos(phi), a*np.sin(phi), np.zeros(n)], axis=-1)
    dl = a*step*np.stack([-np.sin(phi), np.cos(phi), np.zeros(n)], axis=-1)
    displacement = np.array([0, 0, z]) - source
    expected = MU0*current/(4*np.pi)*np.sum(np.cross(dl, displacement)/np.linalg.norm(displacement, axis=-1)[:, None]**3, axis=0)
    np.testing.assert_allclose(CircularArcOnAxis._quarter_components(current, a, z), expected, rtol=1e-7, atol=1e-20)


def test_full_loop_magnitude_is_positive_for_negative_current():
    problem = CircularArcOnAxis()
    fig = Figure()
    problem.plot(fig, dict(defaults(problem), I=-10., loop=2), 'Magnitude')
    assert np.all(fig.axes[0].lines[0].get_ydata() > 0)
    assert fig.axes[0].get_ylabel() == '|B| [T]'


@pytest.mark.parametrize('omega', [-500., 0., 500.])
def test_disk_signed_rotation_center_and_ring_integral(omega):
    problem = RotatingChargedDisk()
    params = dict(defaults(problem), omega=omega)
    assert problem.validate(params) is None
    rho, a = params['rho_s'], params['a']
    assert problem._Bz_axis(rho, omega, a, 0.) == pytest.approx(MU0*rho*omega*a/2, abs=1e-20)
    z = np.array([[-.3, 0.], [.3, .8]])
    np.testing.assert_allclose(problem._Bz_axis(rho, omega, a, z), problem._analytic_Bz(rho, omega, a, z), rtol=4e-6, atol=1e-20)
    fig = Figure()
    problem.draw_3d(fig, params, 'Field')
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    FigureCanvasAgg(fig).draw()


def test_disk_far_field_retains_dipole_limit_without_cancellation():
    rho, omega, a, z = .0005, 500., .15, 1e6
    moment = np.pi*rho*omega*a**4/4
    expected = MU0*moment/(2*np.pi*z**3)
    assert RotatingChargedDisk._analytic_Bz(rho, omega, a, z) == pytest.approx(expected, rel=1e-12, abs=0)
    assert RotatingChargedDisk._analytic_Bz(rho, omega, a, -z) == pytest.approx(expected, rel=1e-12, abs=0)
