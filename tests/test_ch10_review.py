import numpy as np
import pytest
from em_visualisering.problems.ch10 import RadialChargeExpansionMaxwellTest


def test_radial_current_satisfies_continuity_independently():
    p=RadialChargeExpansionMaxwellTest();r=np.linspace(.01,.5,1000)
    rho0,s0,v,t=1e-6,.1,.05,1.
    dr=1e-6;dt=1e-5
    rho,j,jf=p.profiles(r,rho0,s0,v,t)
    derivative=(p.profiles(r,rho0,s0,v,t+dt)[0]-p.profiles(r,rho0,s0,v,t-dt)[0])/(2*dt)
    divergence=((r+dr)**2*p.profiles(r+dr,rho0,s0,v,t)[1]-(r-dr)**2*p.profiles(r-dr,rho0,s0,v,t)[1])/(2*dr*r*r)
    np.testing.assert_allclose(derivative+divergence,0,atol=1e-14)
    np.testing.assert_array_equal(j+jf,np.zeros_like(j))


def test_current_does_not_depend_on_grid_origin_or_sampling():
    p=RadialChargeExpansionMaxwellTest()
    r=np.array([.1,.2,2.])
    rho,j,_=p.profiles(r,1e-6,.1,.05,1.)
    np.testing.assert_allclose(j,rho*.05*r/.15)
    assert j[0]>0
    assert abs(j[-1])<1e-70
    assert p.profiles(0.,1e-6,.1,.05,1.)[1]==0


def test_nonpositive_width_is_rejected():
    p=RadialChargeExpansionMaxwellTest()
    assert p.validate(dict(p.defaults(),v=-.1,t=1.))
    with pytest.raises(ValueError):p.profiles(np.array([0.,.1]),1e-6,.1,-.1,1.)
