import pytest
from em_visualisering.problems.ch03 import BreakdownVoltageCases


@pytest.mark.parametrize('air_max,plexi_max,eps_r', [(3e6,20e6,3), (30e6,2e6,3)])
def test_mixed_stack_respects_both_limits_and_absent_materials(air_max, plexi_max, eps_r):
    d = .01
    model = BreakdownVoltageCases
    for t in (.001, .009):
        air_d, air, plexi, voltage, limiting = model._mixed_case(d,t,air_max,plexi_max,eps_r)
        assert air == pytest.approx(eps_r*plexi)
        assert air <= air_max and plexi <= plexi_max
        assert max(air/air_max,plexi/plexi_max) == pytest.approx(1)
        assert voltage == pytest.approx(air*air_d+plexi*t)
    assert model._mixed_case(d,0,air_max,plexi_max,eps_r)[3] == pytest.approx(air_max*d)
    assert model._mixed_case(d,d,air_max,plexi_max,eps_r)[3] == pytest.approx(plexi_max*d)


def test_printed_mixed_stack_case():
    assert BreakdownVoltageCases._mixed_case(.01,.009,3e6,20e6,3)[3] == pytest.approx(12000)


def test_electret_offers_axis_profiles_not_an_off_axis_map():
    from em_visualisering.modes import mode_options_for_problem, normalize_mode_for_problem
    from em_visualisering.problems.ch03 import ElectretCylinderAxis
    problem = ElectretCylinderAxis()
    assert {m for _, m in mode_options_for_problem(problem)} == {'Field', 'D'}
    assert normalize_mode_for_problem(problem, 'Map') == 'Field'
