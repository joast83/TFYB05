"""Webbversion av EM-visualiseringar.

Kör lokalt med:
    streamlit run streamlit_app.py
"""

import matplotlib
matplotlib.use("Agg", force=True)

import streamlit as st
from matplotlib.figure import Figure

from em_visualisering.plotly_bridge import make_plotly_3d_figure
from em_visualisering.registry import PROBLEMS
from em_visualisering.modes import mode_options_for_problem, normalize_mode_for_problem
from em_visualisering.theory_pages import THEORY_PAGES, render_theory_page
from em_visualisering.unit_scaling import display_scale_for, suggested_step


st.set_page_config(
    page_title="EM-visualiseringar",
    page_icon="⚡",
    layout="wide",
)

st.title("EM-visualiseringar")
st.caption("Interaktiva visualiseringar för elektrostatik, magnetostatik och teoriavsnitt med interaktiva figurer.")

problem_lookup = {problem.name: problem for problem in PROBLEMS}
theory_lookup = {page.title: page for page in THEORY_PAGES}

with st.sidebar:
    content_type = st.radio("Innehåll", ["Övningsuppgifter", "Teori"], index=0)

    if content_type == "Teori":
        theory_title = st.selectbox(
            "Teoriavsnitt",
            [page.title for page in THEORY_PAGES],
            index=0,
        )
        theory_page = theory_lookup[theory_title]
        st.markdown("### Om sidan")
        st.write(theory_page.short_description)
    else:
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
        st.caption("Värden visas i praktiska enheter; fysikberäkningen använder SI-enheter.")
        defaults = problem.defaults()
        params = {}
        for key, label, _default in problem.parameters:
            default_value_si = float(defaults[key])
            scale = display_scale_for(label, default_value_si)
            default_value_display = scale.to_display(default_value_si)
            value_display = st.number_input(
                scale.label,
                value=default_value_display,
                step=suggested_step(default_value_display),
                format="%.12g",
                key=(
                    f"{problem.__class__.__name__}:{key}:"
                    f"{scale.display_unit or 'dimensionless'}"
                ),
                help=(
                    f"Visas i {scale.display_unit}; beräkningen använder {scale.si_unit}."
                    if scale.factor != 1.0
                    else None
                ),
            )
            params[key] = scale.to_si(value_display)

if content_type == "Teori":
    render_theory_page(theory_page)
    st.stop()

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
    view3d_fig = make_plotly_3d_figure(problem, params, mode)
    with col3:
        st.markdown("#### 3-D-vy")
        st.caption("Rotera, zooma och panorera direkt i webbläsaren.")
        st.plotly_chart(view3d_fig, use_container_width=True, config={"displaylogo": False})
except Exception as exc:
    with col3:
        st.error(f"Fel i interaktiv 3-D-vy: {exc}")
        st.info("Reservvisning med Matplotlib visas eftersom Plotly-renderingen misslyckades.")
        fallback_fig = Figure(figsize=(4.8, 6.0), dpi=110)
        problem.draw_3d(fallback_fig, params, mode)
        fallback_fig.tight_layout()
        st.pyplot(fallback_fig, clear_figure=True)

with st.expander("Kontrollera formel/gränsfall"):
    try:
        st.write(problem.physics_check(params))
    except Exception as exc:
        st.error(f"Kontrollen misslyckades: {exc}")
