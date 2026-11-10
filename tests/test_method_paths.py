"""Explicit method comparisons should be discoverable without opening all laws."""
import pytest
from streamlit.testing.v1 import AppTest
from pathlib import Path
from em_visualisering.guidance import GUIDANCE_BY_CLASS
from em_visualisering.starting_laws import STARTING_PATHS, starting_law_choices, starting_law_label


@pytest.mark.parametrize('pid', ['6.1', '7.2', '9.4', '9.14'])
def test_method_choices_are_separate_closed_panels_and_reset(pid):
    app=AppTest.from_file(Path(__file__).resolve().parents[1]/'streamlit_app.py',default_timeout=120).run()
    app.selectbox(key='selected-chapter').set_value(int(pid.split('.')[0])).run()
    selector=app.selectbox(key='selected-problem')
    name=next(n for n in selector.options if n.startswith(pid+' '))
    selector.set_value(name).run()
    assert not app.exception
    panels=[e for e in app.expander if e.label.startswith('Visa startlag')]
    assert len(panels)==len(STARTING_PATHS[pid])
    assert all(not p.proto.expanded for p in panels)
    for panel,(title,equation,prompt) in zip(panels,starting_law_choices(pid),strict=True):
        assert panel.label==starting_law_label(pid,title)
        assert panel.latex[0].value == f"$$\n{equation}\n$$"
        assert any(m.value==prompt for m in panel.markdown)
    keys=[p._block_id for p in panels]
    app.selectbox(key='selected-chapter').set_value(2).run()
    app.selectbox(key='selected-chapter').set_value(int(pid.split('.')[0])).run()
    app.selectbox(key='selected-problem').set_value(name).run()
    returned=[e for e in app.expander if e.label.startswith('Visa startlag')]
    assert all(not p.proto.expanded for p in returned)
    assert [p._block_id for p in returned]!=keys


def test_vector_potential_is_integrated_before_taking_its_curl():
    g=GUIDANCE_BY_CLASS['FiniteWireBiotSavart']
    assert len(g.hints)==len(g.hint_titles)==6
    assert r'\int' in g.hints[2] and r'A_z(R,z)' in g.hints[2]
    assert r'\nabla\times\overline A' in g.hints[3]
    assert r'A_R=A_\phi=0' in g.hints[3]
    assert r'\oint' in g.hints[4] and 'oändligt lång' in g.hints[4]
    assert 'returledningen' in g.hints[5]


def test_default_problem_retains_one_starting_law():
    assert len(starting_law_choices('2.8'))==1
    assert starting_law_label('2.8','Gauss lag')=='Visa startlagen och hur du börjar'
