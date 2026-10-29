"""Physical regression checks for the chapter-4 review."""
import numpy as np
import pytest
from matplotlib.figure import Figure
from em_visualisering.core import EPS0
from em_visualisering.problems.ch04 import (
    SphericalShellChargingEnergy, ParallelPlateForceDistance,
    CylindricalCapacitorDielectricPullIn, PointChargeConductingPlane,
)


@pytest.mark.parametrize('Q', [-1e-9, 0, 1e-9])
def test_charging_work_and_signed_potential_profile(Q):
    problem = SphericalShellChargingEnergy()
    a = 0.1
    # Numerical charging work, with signed charge steps.
    q = np.linspace(0, Q, 1001)
    potential = q / (4*np.pi*EPS0*a)
    work = np.sum((potential[1:]+potential[:-1])*np.diff(q)/2)
    assert problem.energy(Q,a) == pytest.approx(work, abs=1e-24)
    fig = Figure()
    problem.plot(fig, {'Q':Q,'a':a}, 'Field')
    plotted_q, plotted_v = fig.axes[0].lines[0].get_data()
    assert min(plotted_q) <= Q <= max(plotted_q)
    np.testing.assert_allclose(plotted_v, plotted_q/(4*np.pi*EPS0*a))
    if Q < 0:
        assert np.all(plotted_v <= 0)


def test_zero_voltage_cannot_balance_a_positive_plate_force():
    problem = ParallelPlateForceDistance()
    assert problem.validate({**problem.defaults(),'V':0}) is not None
    for V in (-450,450):
        params = {**problem.defaults(),'V':V}
        assert problem.validate(params) is None
        d = problem.distance(params['A'],V,params['F'])
        assert d == pytest.approx(0.0002994, rel=1e-3)


@pytest.mark.parametrize('eps_r', [1, 2.5, 8])
@pytest.mark.parametrize('V', [-1000, 1000])
def test_pull_in_force_matches_source_work_minus_field_energy(eps_r,V):
    a,b,L,x,dx = .03,.05,1.,.4,1e-5
    def capacitance(position):
        return 2*np.pi*EPS0*(eps_r*position+L-position)/np.log(b/a)
    c0,c1 = capacitance(x),capacitance(x+dx)
    source_work = V*(c1*V-c0*V)
    field_energy_increase = .5*(c1-c0)*V**2
    force = CylindricalCapacitorDielectricPullIn.force(a,b,eps_r,V)
    assert force*dx == pytest.approx(source_work-field_energy_increase, abs=1e-18)
    assert force >= 0


@pytest.mark.parametrize('q', [-1e-9,1e-9])
@pytest.mark.parametrize('ratio', [1.01,3,20])
def test_induced_charge_integral_uses_distance_from_charge(q,ratio):
    a=.1
    b=ratio*a
    radius=np.sqrt(b*b-a*a)
    nodes,weights=np.polynomial.legendre.leggauss(128)
    r=(nodes+1)*radius/2
    # Both charge and image contribute to the normal field at the plane.
    e_normal=-2*q*a/(4*np.pi*EPS0*(r*r+a*a)**1.5)
    numerical_charge=np.sum(weights*EPS0*e_normal*2*np.pi*r)*radius/2
    assert PointChargeConductingPlane.induced_within(q,a,b) == pytest.approx(numerical_charge, rel=1e-10, abs=1e-24)


def test_zero_charge_plot_does_not_label_zero_as_a_defined_ratio():
    problem=PointChargeConductingPlane()
    fig=Figure()
    problem.plot(fig,{**problem.defaults(),'q':0},'Field')
    assert 'Qind/q' not in fig.axes[0].get_ylabel()
    assert np.all(fig.axes[0].lines[0].get_ydata()==0)
