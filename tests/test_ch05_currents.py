"""Checks for signed currents, separate units and stationary conservation."""
import numpy as np
import pytest
from matplotlib.figure import Figure
from em_visualisering.core import EPS0
from em_visualisering.modes import mode_options_for_problem
from em_visualisering.problems.ch05 import (
    ConductiveCoaxialElectrodes, CoaxialCableLeakage,
    VariableSigmaCoaxialElectrolyte, SemicylindricalRingResistor,
    SteadyCurrentInterfaceCharge,
)


@pytest.mark.parametrize('voltage', [-120,0,120])
@pytest.mark.parametrize('mode', ['Field','Magnitude'])
def test_leakage_plot_keeps_signed_current_and_nonnegative_power(voltage,mode):
    problem=CoaxialCableLeakage()
    params={**problem.defaults(),'V':voltage}
    fig=Figure()
    problem.plot(fig,params,mode)
    ax=fig.axes[0]
    resistivity,values=ax.lines[0].get_data()
    current,power=problem.leakage(resistivity,params['ell'],params['a'],params['b'],voltage)
    np.testing.assert_allclose(values,power if mode=='Magnitude' else current)
    assert ax.get_yscale()=='linear'  # zero and negative currents must be visible
    assert np.all(np.isfinite(values))
    assert np.all(power>=0)
    if voltage==0:
        assert np.all(values==0)
    elif mode=='Field':
        assert np.all(np.sign(values)==np.sign(voltage))


def test_zero_current_does_not_imply_infinite_resistance():
    problem=ConductiveCoaxialElectrodes()
    report=problem.physics_check({**problem.defaults(),'U':0})
    assert 'OK' in report
    assert 'inf' not in report.lower() and 'nan' not in report.lower()


@pytest.mark.parametrize('voltage',[-1,0,1])
def test_variable_conductivity_views_obey_continuity_and_gauss(voltage):
    problem=VariableSigmaCoaxialElectrolyte()
    params={**problem.defaults(),'U':voltage}
    data={}
    for mode in ('Field','Magnitude','D'):
        fig=Figure()
        problem.plot(fig,params,mode)
        assert len(fig.axes[0].lines)==1
        r,values=fig.axes[0].lines[0].get_data()
        data[mode]=np.asarray(values)
    e,j,rho=data['Field'],data['Magnitude'],data['D']
    current=voltage/problem.resistance(params['k'],params['ell'],params['a'],params['b'])
    np.testing.assert_allclose(2*np.pi*r*params['ell']*j,current,atol=1e-15)
    np.testing.assert_allclose(j,params['k']/r**2*e,atol=1e-15)
    # A finite shell must obey integral Gauss law as well as current conservation.
    enclosed_flux=2*np.pi*params['ell']*EPS0*params['eps_r']*(r[-1]*e[-1]-r[0]*e[0])
    enclosed_charge=rho[0]*np.pi*(r[-1]**2-r[0]**2)*params['ell']
    assert enclosed_flux==pytest.approx(enclosed_charge,abs=1e-22)
    labels=dict((mode,label) for label,mode in mode_options_for_problem(problem))
    assert 'Strömtäthet' in labels['Magnitude']
    assert 'laddningstäthet' in labels['D']


def test_half_ring_parallel_path_integral_matches_resistance():
    problem=SemicylindricalRingResistor()
    p=problem.defaults()
    nodes,weights=np.polynomial.legendre.leggauss(100)
    r=(p['b']-p['a'])*(nodes+1)/2+p['a']
    conductance=np.sum(weights*p['sigma']*p['h']/(np.pi*r))*(p['b']-p['a'])/2
    assert 1/conductance==pytest.approx(problem.resistance(p['sigma'],p['h'],p['a'],p['b']))


def test_interface_charge_from_normal_current_and_tangential_field():
    for alpha in (-1,0,1):
        eps1,eps2,sigma1,sigma2=2.,5.,1.,4.
        # Continuity of J_n fixes E_n separately in the two media.
        jump_d=EPS0*(eps2*alpha/sigma2-eps1*alpha/sigma1)
        assert SteadyCurrentInterfaceCharge.rho_s(alpha,eps1,eps2,sigma1,sigma2)==pytest.approx(jump_d,abs=1e-24)
        assert SteadyCurrentInterfaceCharge.rho_s(alpha,2,8,1,4)==pytest.approx(0,abs=1e-24)
    assert SteadyCurrentInterfaceCharge.rho_s(0,eps1,eps2,sigma1,sigma2)==0
