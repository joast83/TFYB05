"""Webbversion av EM-visualiseringar.

Kör lokalt med:
    streamlit run streamlit_app.py
"""

import matplotlib
matplotlib.use("Agg", force=True)

import streamlit as st
from matplotlib.figure import Figure

from em_visualisering.registry import PROBLEMS
from em_visualisering.modes import mode_options_for_problem, normalize_mode_for_problem


st.set_page_config(
    page_title="EM-visualiseringar",
    page_icon="⚡",
    layout="wide",
)

st.title("EM-visualiseringar")
st.caption("Interaktiva visualiseringar för elektrostatik och magnetostatik.")

problem_lookup = {problem.name: problem for problem in PROBLEMS}

with st.sidebar:
    problem_name = st.selectbox(
        "Uppgift",
        [problem.name for problem in PROBLEMS],
        index=0,
    )
    problem = problem_lookup[problem_name]

    mode_options = mode_options_for_problem(problem)
    mode_labels = [label for label, _internal in mode_options]
    mode_label = st.selectbox("Visningsläge", mode_labels, index=0)
    requested_mode = dict(mode_options)[mode_label]
    mode = normalize_mode_for_problem(problem, requested_mode)

    st.markdown("### Parametrar")
    defaults = problem.defaults()
    params = {}
    for key, label, _unit in problem.parameters:
        default_value = float(defaults[key])
        params[key] = st.number_input(
            label,
            value=default_value,
            format="%.12g",
            key=f"{problem.__class__.__name__}:{key}",
        )

st.subheader(problem.name)
st.write(problem.description)

with st.expander("Fysikalisk idé", expanded=True):
    st.write(problem.pedagogical_note())

validation_error = problem.validate(params)
if validation_error:
    st.error(validation_error)
    st.stop()

try:
    st.info(problem.result_summary(params, mode))
except Exception as exc:
    st.warning(f"Kunde inte beräkna sammanfattning: {exc}")

col1, col2, col3 = st.columns([5, 3, 4])

try:
    fig = Figure(figsize=(7.0, 6.0), dpi=110)
    problem.plot(fig, params, mode)
    fig.tight_layout()
    with col1:
        st.markdown("#### Huvudgraf")
        st.pyplot(fig, clear_figure=True)
except Exception as exc:
    with col1:
        st.error(f"Fel i huvudgraf: {exc}")

try:
    geometry_fig = Figure(figsize=(3.8, 6.0), dpi=110)
    problem.draw_geometry(geometry_fig, params)
    geometry_fig.tight_layout()
    with col2:
        st.markdown("#### Geometriskiss")
        st.pyplot(geometry_fig, clear_figure=True)
except Exception as exc:
    with col2:
        st.error(f"Fel i geometriskiss: {exc}")

try:
    view3d_fig = Figure(figsize=(4.8, 6.0), dpi=110)
    problem.draw_3d(view3d_fig, params, mode)
    view3d_fig.tight_layout()
    with col3:
        st.markdown("#### 3-D-vy")
        st.pyplot(view3d_fig, clear_figure=True)
except Exception as exc:
    with col3:
        st.error(f"Fel i 3-D-vy: {exc}")

with st.expander("Kontrollera formel/gränsfall"):
    try:
        st.write(problem.physics_check(params))
    except Exception as exc:
        st.error(f"Kontrollen misslyckades: {exc}")
