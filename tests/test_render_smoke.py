import matplotlib
matplotlib.use("Agg", force=True)

from matplotlib.figure import Figure
import pytest

from em_visualisering.modes import mode_options_for_problem
from em_visualisering.plotly_bridge import make_plotly_3d_figure
from em_visualisering.registry import PROBLEMS


CASES = [
    (problem, internal_mode)
    for problem in PROBLEMS
    for _label, internal_mode in mode_options_for_problem(problem)
]


def case_id(case):
    problem, mode = case
    return f"{problem.__class__.__name__}-{mode}"


@pytest.mark.parametrize("problem,mode", CASES, ids=[case_id(case) for case in CASES])
def test_default_matplotlib_rendering(problem, mode):
    params = problem.defaults()

    main = Figure(figsize=(4, 3), dpi=60)
    problem.plot(main, params, mode)
    assert main.axes

    geometry = Figure(figsize=(3, 3), dpi=60)
    problem.draw_geometry(geometry, params)
    assert geometry.axes

    view3d = Figure(figsize=(3, 3), dpi=60)
    problem.draw_3d(view3d, params, mode)
    assert view3d.axes


@pytest.mark.parametrize("problem,mode", CASES, ids=[case_id(case) for case in CASES])
def test_default_plotly_rendering(problem, mode):
    figure = make_plotly_3d_figure(problem, problem.defaults(), mode)
    assert figure is not None
    assert len(figure.data) >= 0
