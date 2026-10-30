"""Independent induction and energy checks for chapter 9."""
import numpy as np
import pytest
from matplotlib.figure import Figure
from em_visualisering.core import MU0
from em_visualisering.problems.ch09 import (
    MutualInductanceParallelWiresSquare, MutualInductanceCoaxialLoops,
    OpenSecondaryTransformerVoltage, MovingLoopFieldWork, MovingLoopDipoleEmf,
)


def test_two_wire_flux_integral_accounts_for_tapered_square_width():
    d=.1;n=100000;du=d/n;u=(np.arange(n)+.5)*du
    bz=MU0/(2*np.pi)*(1/u+1/(d-u))
    width=2*np.minimum(u,d-u)
    flux=np.sum(bz*width)*du
    assert MutualInductanceParallelWiresSquare.mutual(d)==pytest.approx(flux,rel=1e-9)


@pytest.mark.parametrize('distance', [.1,.3,1.])
def test_coaxial_methods_agree_with_nonuniform_dipole_surface_integral(distance):
    a,b=.001,.1;n=50000;dr=b/n;r=(np.arange(n)+.5)*dr
    moment=np.pi*a*a
    bz=MU0*moment/(4*np.pi)*(2*distance**2-r*r)/(r*r+distance**2)**2.5
    flux=np.sum(bz*2*np.pi*r*dr)
    model=MutualInductanceCoaxialLoops.mutual(a,b,distance)
    assert model==pytest.approx(flux,rel=1e-9)
    large_loop_field=MU0*b*b/(2*(b*b+distance**2)**1.5)
    assert model==pytest.approx(large_loop_field*np.pi*a*a,rel=1e-14)


@pytest.mark.parametrize('omega', [0.,2*np.pi*50])
@pytest.mark.parametrize('coefficient', [-1.,0.,1.])
def test_transformer_voltage_matches_negative_flux_derivative(omega,coefficient):
    p=OpenSecondaryTransformerVoltage();params=dict(p.defaults(),omega=omega,I0=coefficient)
    assert p.validate(params) is None
    fig=Figure();p.plot(fig,params,'Field')
    t_ms,voltage=fig.axes[0].lines[0].get_data();t=t_ms/1000
    constant=MU0*params['mu_r']*params['N1']*params['S']*coefficient/params['ell']
    dt=1e-7
    derivative=(constant*np.cos(omega*(t+dt))-constant*np.cos(omega*(t-dt)))/(2*dt)
    np.testing.assert_allclose(voltage,-params['N2']*derivative,rtol=1e-7,atol=1e-7)
    if omega==0:assert np.all(voltage==0)


@pytest.mark.parametrize('length', [.04,.1,.3])
@pytest.mark.parametrize('field', [-1.,0.,1.])
def test_passage_obeys_faraday_and_energy_balance_for_any_field_width(length,field):
    p=MovingLoopFieldWork();a=.1;v=10.;resistance=.05
    n=100000;dx=(length+a)/n;x=(np.arange(n)+.5)*dx
    overlap,emf,power,work=p.passage(x,field,a,v,resistance,length)
    assert np.all(overlap>=0) and np.all(overlap<=min(a,length)+1e-15)
    dt_position=1e-8
    area_plus=p.passage(x+dt_position,field,a,v,resistance,length)[0]*a
    area_minus=p.passage(x-dt_position,field,a,v,resistance,length)[0]*a
    np.testing.assert_allclose(emf,-field*v*(area_plus-area_minus)/(2*dt_position),rtol=1e-7,atol=1e-8)
    energy=np.sum(power)*dx/v
    total=p.work(field,a,v,resistance,length)
    assert energy==pytest.approx(total,rel=5e-5,abs=1e-14)
    assert p.passage(length+a,field,a,v,resistance,length)[3]==pytest.approx(total,abs=1e-14)
    assert np.all(np.diff(work)>=-1e-15)
    assert np.all(power>=0)


def test_passage_matches_course_answer_and_has_zero_power_on_plateau():
    p=MovingLoopFieldWork()
    assert p.work(1,.1,10,.05,.3)==pytest.approx(.4)
    assert p.work(1,.1,10,.05,.04)==pytest.approx(.16)
    for length in [.04,.3]:
        x=(length+.1)/2
        assert p.passage(x,1,.1,10,.05,length)[2]==0


@pytest.mark.parametrize('moment,speed', [(1.,1.),(-1.,1.),(1.,-1.),(1.,0.)])
def test_moving_dipole_emf_matches_motional_line_integral(moment,speed):
    a,z=1e-4,.1;n=1000;dphi=2*np.pi/n;phi=(np.arange(n)+.5)*dphi
    point=np.stack([a*np.cos(phi),a*np.sin(phi),np.full(n,z)],axis=-1)
    distance=np.linalg.norm(point,axis=-1);rhat=point/distance[:,None];m=np.array([0,0,moment])
    field=MU0/(4*np.pi)*(3*(rhat@m)[:,None]*rhat-m)/distance[:,None]**3
    dl=a*dphi*np.stack([-np.sin(phi),np.cos(phi),np.zeros(n)],axis=-1)
    integral=np.sum(np.cross([0,0,speed],field)*dl)
    assert MovingLoopDipoleEmf.emf(moment,a,speed,z)==pytest.approx(integral,rel=3e-6,abs=1e-22)


@pytest.mark.parametrize('problem,changes', [
    (OpenSecondaryTransformerVoltage(),{'omega':0.,'I0':-1.}),
    (MovingLoopFieldWork(),{'ell':.04,'B':-1.}),
    (MovingLoopDipoleEmf(),{'m':-1.,'v':-1.}),
])
def test_signed_and_zero_cases_render_in_plotly(problem,changes):
    from em_visualisering.plotly_bridge import make_plotly_3d_figure
    make_plotly_3d_figure(problem,dict(problem.defaults(),**changes),'Field').to_json(validate=True)
