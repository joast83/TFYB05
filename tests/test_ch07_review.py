"""Independent physical checks and regressions for the chapter 7 review."""
import numpy as np
import pytest
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from em_visualisering.core import MU0
from em_visualisering.problems.ch07 import (
    ElectronOrbitDipoleMoment, CircularLoopTorqueUniformField, DipoleDipoleTorque,
    LoopDipoleApproximationError, AntarcticIceFlux, CopperWireMagneticLevitation,
    InfiniteWireRectangularLoopFlux,
)


def test_electron_moment_opposes_orbital_angular_momentum():
    e, v, a = 1.602176634e-19, 2e6, 5e-11
    period = 2*np.pi*a/v
    assert ElectronOrbitDipoleMoment._moment(v, a) == pytest.approx(-e/period*np.pi*a*a, rel=1e-14, abs=0)


@pytest.mark.parametrize('current,field', [(2., .3), (-2., .3), (2., -.3), (0., .3), (2., 0.)])
def test_loop_distributed_torque_matches_two_cross_products(current, field):
    p = CircularLoopTorqueUniformField()
    params = dict(p.defaults(), I=current, B=field)
    fig = Figure(); p.plot(fig, params, 'Field')
    phi, plotted = fig.axes[0].lines[0].get_data()
    a = params['a']
    r = a*np.stack([np.cos(phi), np.sin(phi), np.zeros_like(phi)], axis=-1)
    dl = a*np.stack([-np.sin(phi), np.cos(phi), np.zeros_like(phi)], axis=-1)
    force = current*np.cross(dl, [field, 0, 0])
    torque = np.cross(r, force)
    np.testing.assert_allclose(plotted, torque[:, 1], atol=1e-16)
    # A complete closed loop has no net force, but a finite torque.
    step = np.diff(phi)
    integral = lambda values: np.sum(.5*(values[1:]+values[:-1])*step[:, None], axis=0)
    np.testing.assert_allclose(integral(force), 0, atol=1e-15)
    np.testing.assert_allclose(integral(torque), [0, p._torque(current, field, a), 0], atol=1e-15)
    assert fig.axes[0].lines[1].get_ydata()[-1] == pytest.approx(p._torque(current, field, a), abs=1e-15)


@pytest.mark.parametrize('angle', [0., 45., 90., 135., 180.])
def test_dipole_torque_matches_vector_field_and_covers_full_angle_range(angle):
    p = DipoleDipoleTorque(); theta = np.radians(angle)
    moment = np.array([0., 0., 1.])
    direction = np.array([np.sin(theta), 0., np.cos(theta)])
    field = MU0/(4*np.pi)*(3*np.dot(moment, direction)*direction - moment)
    expected = np.cross(moment, field)
    assert p._torque(1., 1., theta) == pytest.approx(expected[1], abs=1e-20)
    np.testing.assert_allclose(expected[[0, 2]], 0, atol=1e-20)
    fig = Figure(); p.plot(fig, dict(p.defaults(), theta_deg=angle), 'Field')
    x = fig.axes[0].lines[0].get_xdata()
    assert min(x) <= angle <= max(x)


@pytest.mark.parametrize('tol', [1e-6, .01, .2])
@pytest.mark.parametrize('current', [0., -1., 1.])
def test_dipole_error_is_finite_for_zero_current_and_threshold_is_visible(tol, current):
    p = LoopDipoleApproximationError(); params = dict(p.defaults(), tol=tol, I=current)
    z = p.z_for_tol(params['a'], tol)
    ratio = (1+(params['a']/z)**2)**1.5 - 1
    assert ratio == pytest.approx(tol, rel=1e-8)
    fig = Figure(); p.plot(fig, params, 'Field')
    x, error = fig.axes[0].lines[0].get_data()
    assert np.all(np.isfinite(error)) and np.all(error > 0)
    assert min(x) < z/params['a'] < max(x)
    assert error[-1] < tol
    FigureCanvasAgg(fig).draw()


def test_antarctic_flux_matches_surface_integral_and_has_no_ineffective_height_control():
    p = AntarcticIceFlux(); params = p.defaults()
    theta_max = np.radians(20.)
    n = 10000; dtheta = theta_max/n; theta=(np.arange(n)+.5)*dtheta
    br = MU0*params['m']*np.cos(theta)/(2*np.pi*params['rJ']**3)
    outward = np.sum(br*params['rJ']**2*np.sin(theta)*dtheta*2*np.pi)
    assert p._flux(params['m'], params['rJ'], 70.) == pytest.approx(outward, rel=1e-9)
    assert outward == pytest.approx(9.5e8, rel=.002)
    assert 'ice_h' not in params
    assert p._flux(params['m'], params['rJ'], 90.) == 0


def test_wire_balance_and_units():
    p = CopperWireMagneticLevitation(); params = p.defaults()
    field = p._required_B(params['J'], params['rho_cu'], params['g'])
    assert field == pytest.approx(.029103)
    np.testing.assert_allclose(np.cross([params['J'],0,0], [0,field,0]), [0,0,params['rho_cu']*params['g']])
    fig=Figure();p.plot(fig,dict(params,Bmax=.001),'Field')
    assert fig.axes[0].lines[0].get_xdata()[-1] > field


@pytest.mark.parametrize('current', [-10., 0., 10.])
def test_rectangular_flux_matches_projected_surface_integral(current):
    a,b,c=.2,.1,.05
    n=10000; dy=b/n; y=(np.arange(n)+.5)*dy
    displacement=np.stack([np.zeros(n),y,np.full(n,c)],axis=-1)
    field=MU0*current/(2*np.pi)*np.cross([1,0,0],displacement)/np.sum(displacement**2,axis=-1)[:,None]
    expected=np.sum(field[:,2])*a*dy
    assert InfiniteWireRectangularLoopFlux.flux(current,a,b,c) == pytest.approx(expected,rel=1e-8,abs=1e-20)


def test_rectangular_flux_preserves_small_width_limit():
    a,b,c,current=.2,1e-10,1.,10.
    expected=MU0*current*a*b*b/(4*np.pi*c*c)
    assert InfiniteWireRectangularLoopFlux.flux(current,a,b,c) == pytest.approx(expected,rel=1e-14,abs=0)


@pytest.mark.parametrize('angle,sign', [(45., 1), (135., -1), (90., 0), (180., 0)])
def test_dipole_rendered_torque_arrow_points_along_y_or_vanishes(angle, sign):
    p = DipoleDipoleTorque(); fig = Figure()
    p.draw_3d(fig, dict(p.defaults(), theta_deg=angle), 'Field')
    segments = fig.axes[0].collections[-1]._segments3d
    if sign:
        vector = segments[0][0] - segments[0][1]
        np.testing.assert_allclose(vector, [0, sign*.4, 0], atol=1e-14)
    else:
        for segment in segments:
            np.testing.assert_allclose(segment[0], segment[1], atol=1e-14)


@pytest.mark.parametrize('current,field', [(-2., .3), (2., -.3), (0., .3)])
def test_loop_rendered_torque_arrow_matches_signed_inputs(current, field):
    p = CircularLoopTorqueUniformField(); fig = Figure()
    p.draw_3d(fig, dict(p.defaults(), I=current, B=field), 'Field')
    segments = fig.axes[0].collections[-1]._segments3d
    if current*field:
        vector = segments[0][0] - segments[0][1]
        np.testing.assert_allclose(vector, [0, np.sign(current*field)*p.defaults()['a'], 0], atol=1e-14)
    else:
        for segment in segments:
            np.testing.assert_allclose(segment[0], segment[1], atol=1e-14)


@pytest.mark.parametrize('problem,changes', [
    (CircularLoopTorqueUniformField(), {'I': -2., 'B': .3}),
    (CircularLoopTorqueUniformField(), {'I': 0., 'B': 0.}),
    (DipoleDipoleTorque(), {'theta_deg': 135., 'm': -1.}),
    (LoopDipoleApproximationError(), {'I': 0., 'tol': 1e-6}),
])
def test_changed_signed_and_zero_cases_render_in_plotly(problem, changes):
    from em_visualisering.plotly_bridge import make_plotly_3d_figure
    for mode in ['Field', 'Map']:
        figure = make_plotly_3d_figure(problem, dict(problem.defaults(), **changes), mode)
        figure.to_json(validate=True)
