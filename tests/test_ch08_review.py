"""Physical balance, boundary and signed-input regressions for chapter 8."""
import numpy as np
import pytest
from matplotlib.figure import Figure
from em_visualisering.core import MU0
from em_visualisering.problems.ch08 import (
    PermanentMagnetAirGapBHCurve, NonlinearIronMagneticCircuit, MagneticBridgeCircuit,
    CurrentCarryingMagneticTube, HorseshoeMagnetAnchorForce,
    PermanentlyMagnetizedCylinderAxis, MagnetizationCurrentsCylinder,
)


@pytest.mark.parametrize('current', [-5., 0., 2., 8.])
def test_magnet_interpolated_solution_satisfies_ampere_balance(current):
    p=PermanentMagnetAirGapBHCurve()
    b=p.solve_B(.2,.001,100,current)
    assert p.Hmat(b)*(.2-.001)+b*.001/MU0 == pytest.approx(100*current, abs=1e-10)


@pytest.mark.parametrize('current', [-20., 20.])
def test_magnet_does_not_invent_an_endpoint_solution(current):
    p=PermanentMagnetAirGapBHCurve()
    with pytest.raises(ValueError, match='tabellen'):
        p.solve_B(.2,.001,100,current)
    assert p.validate(dict(p.defaults(),I=current))


@pytest.mark.parametrize('current', [0., .1, 2., 20.])
def test_nonlinear_solution_stays_on_valid_branch(current):
    p=NonlinearIronMagneticCircuit()
    b=p.solve_B(.5,.001,100,current,2.,400.)
    assert 0 <= b < 2.
    h=400*b/(2-b)
    assert h*.5+b*.001/MU0 == pytest.approx(100*current,abs=1e-9)
    if current==0:assert b==0


def test_nonlinear_rejects_negative_current_and_other_root_has_negative_h():
    p=NonlinearIronMagneticCircuit()
    assert p.validate(dict(p.defaults(),I=-2))
    with pytest.raises(ValueError):p.solve_B(.5,.001,100,-2,2.,400.)
    roots=np.roots([.001/MU0, -(.5*400+.001*2/MU0+200), 200*2])
    rejected=max(roots)
    assert rejected>2 and 400*rejected/(2-rejected)<0


@pytest.mark.parametrize('current', [-.002, 0., .002])
def test_bridge_flux_satisfies_both_branch_balances(current):
    p=MagneticBridgeCircuit();d=.15;sr=1.2e-4;sb=8e-5;mu=MU0*150
    rhalf=np.pi*d/(2*mu*sr);rb=d/(mu*sb)
    bridge=p.bridge_flux(d,sr,sb,150,160,current)
    potential=rb*bridge;right=potential/rhalf
    assert rhalf*(bridge+right)+potential == pytest.approx(160*current,abs=1e-15)
    assert p.validate(dict(p.defaults(),I=current)) is None


def test_tube_fields_work_on_scalar_integer_and_array_inputs():
    p=CurrentCarryingMagneticTube()
    for radii in [0., np.array([0,1,2,3]), np.array([0., .01, .03, .07])]:
        h,b,m=p.fields(radii,10,.02,.05,100)
        np.testing.assert_allclose(b,MU0*(h+m),atol=1e-15)
    r=np.array([.01,.03,.07]);h,b,m=p.fields(r,10,.02,.05,100)
    enclosed=np.array([0,10*(.03**2-.02**2)/(.05**2-.02**2),10])
    np.testing.assert_allclose(2*np.pi*r*h,enclosed)
    np.testing.assert_allclose(p.fields(r,10,.02,.05,1)[0],h)
    assert p.fields(.03,10,.02,.05,1)[2]==0


def test_tube_boundary_h_continuity_and_b_jump():
    p=CurrentCarryingMagneticTube();b=.05
    h,field,_=p.fields(np.array([np.nextafter(b,0),np.nextafter(b,np.inf)]),10,.02,b,100)
    assert h[0]==pytest.approx(h[1],rel=1e-14)
    assert field[0]/field[1]==pytest.approx(100)


def test_tube_modes_have_separate_units():
    p=CurrentCarryingMagneticTube()
    for mode,label in [('Field','Hφ [A/m]'),('Potential','Bφ [T]'),('Map','Mφ [A/m]')]:
        fig=Figure();p.plot(fig,p.defaults(),mode)
        assert fig.axes[0].get_ylabel()==label


@pytest.mark.parametrize('flux', [-3e-4,0,3e-4])
def test_anchor_force_sums_two_positive_pole_forces(flux):
    p=HorseshoeMagnetAnchorForce();area=2.8e-4
    pressure=(flux/area)**2/(2*MU0)
    assert p.force(flux,area)==pytest.approx(2*pressure*area)
    fig=Figure();p.plot(fig,dict(p.defaults(),Phi0=flux),'Field')
    assert fig.axes[0].collections[0].get_offsets()[0,0]>=0


def test_cylinder_field_matches_ring_integration_symmetry_and_far_field():
    p=PermanentlyMagnetizedCylinderAxis();m=8e5;a=.05;h=.12
    n=20000;dz=h/n;sources=(np.arange(n)+.5)*dz
    z=np.array([-.1, .03, .06, .09, .22])
    expected=MU0*m/2*np.sum(a*a/(a*a+(z[:,None]-sources)**2)**1.5,axis=1)*dz
    np.testing.assert_allclose(p._Bz(m,a,h,z),expected,rtol=1e-9)
    np.testing.assert_allclose(p._Bz(m,a,h,z),p._Bz(m,a,h,h-z),rtol=1e-14)
    distant=1e6
    dipole=MU0*(m*np.pi*a*a*h)/(2*np.pi*(distant-h/2)**3)
    assert p._Bz(m,a,h,distant)==pytest.approx(dipole,rel=1e-12,abs=0)


def test_cylinder_h_jumps_and_wide_slab_limit():
    p=PermanentlyMagnetizedCylinderAxis();m=8e5;a=.05;h=.12
    inside=p._Hz(m,a,h,np.nextafter(0.,np.inf));outside=p._Hz(m,a,h,np.nextafter(0.,-np.inf))
    assert inside-outside==pytest.approx(-m)
    assert p._Bz(m,1e9,h,h/2)==pytest.approx(0,abs=1e-9)
    assert p._Hz(m,1e9,h,h/2)==pytest.approx(-m,rel=1e-9)


@pytest.mark.parametrize('current,mur', [(10.,100.),(-10.,100.),(10.,.5),(10.,1.),(0.,100.)])
def test_magnetization_volume_and_surface_currents_cancel(current,mur):
    p=MagnetizationCurrentsCylinder();a=.02;fig=Figure()
    p.plot(fig,dict(p.defaults(),I=current,mu_r=mur),'Field')
    density=fig.axes[0].lines[0].get_ydata()[0]
    surface=-current*(mur-1)/(2*np.pi*a)
    assert density*np.pi*a*a+surface*2*np.pi*a==pytest.approx(0,abs=1e-12)
    fig=Figure();p.draw_3d(fig,dict(p.defaults(),I=current,mu_r=mur),'Field')
    arrows=fig.axes[0].collections[-5:]
    volume=arrows[0]._segments3d[0][0]-arrows[0]._segments3d[0][1]
    assert np.sign(volume[2])==np.sign(current*(mur-1))
    for arrow in arrows[1:]:
        vec=arrow._segments3d[0][0]-arrow._segments3d[0][1]
        np.testing.assert_allclose(vec,-volume,atol=1e-15)


@pytest.mark.parametrize('problem,changes,modes', [
    (PermanentMagnetAirGapBHCurve(), {'I': 8.}, ['Field']),
    (NonlinearIronMagneticCircuit(), {'I': 0.}, ['Field']),
    (CurrentCarryingMagneticTube(), {'I': -10.}, ['Field','Potential','Map']),
    (PermanentlyMagnetizedCylinderAxis(), {'M': 0.}, ['Field','Potential','Map']),
    (PermanentlyMagnetizedCylinderAxis(), {'M': -8e5}, ['Field','Potential','Map']),
    (MagnetizationCurrentsCylinder(), {'mu_r': .5}, ['Field']),
])
def test_reviewed_edge_cases_render_in_plotly(problem,changes,modes):
    from em_visualisering.plotly_bridge import make_plotly_3d_figure
    for mode in modes:
        figure=make_plotly_3d_figure(problem,dict(problem.defaults(),**changes),mode)
        figure.to_json(validate=True)


def test_cylinder_parameter_surface_is_b_not_h():
    p=PermanentlyMagnetizedCylinderAxis();fig=Figure()
    p.draw_3d(fig,p.defaults(),'Map')
    assert fig.axes[0].get_zlabel()=='Bz [T]'
    assert fig.axes[0].get_ylabel()=='Cylinderradie a [m]'
