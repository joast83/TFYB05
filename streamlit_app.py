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
st.caption(
    "Interaktiva visualiseringar för elektrostatik, magnetostatik och "
    "teoriavsnitt med interaktiva figurer."
)

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

        view_mode = st.selectbox(
            "Vyer",
            ["Alla", "Huvudgraf", "Geometriskiss", "3-D-vy"],
            index=0,
            help="Välj en enskild vy för snabbare uppdatering på långsamma datorer.",
        )
        quality = st.select_slider(
            "Återgivningskvalitet",
            options=["Snabb", "Normal", "Hög"],
            value="Normal",
            help="Påverkar upplösningen för Matplotlib-vyerna.",
        )

        st.markdown("### Parametrar")
        st.caption(
            "Värden visas i praktiska enheter; fysikberäkningen använder SI-enheter. "
            "Ändringar ritas först när du trycker på knappen."
        )
        defaults = problem.defaults()
        params = {}
        with st.form(
            key=f"parameters:{problem.__class__.__name__}",
            clear_on_submit=False,
        ):
            for spec in problem.parameter_specs():
                default_value_si = float(defaults[spec.key])
                scale = display_scale_for(spec.label, default_value_si)
                default_display = scale.to_display(default_value_si)
                min_display = (
                    scale.to_display(spec.minimum_si)
                    if spec.minimum_si is not None
                    else None
                )
                max_display = (
                    scale.to_display(spec.maximum_si)
                    if spec.maximum_si is not None
                    else None
                )
                step_display = (
                    spec.step_si / scale.factor
                    if spec.step_si is not None
                    else suggested_step(default_display)
                )
                help_parts = []
                if spec.help_text:
                    help_parts.append(spec.help_text)
                if scale.factor != 1.0:
                    help_parts.append(
                        f"Visas i {scale.display_unit}; beräkningen använder {scale.si_unit}."
                    )
                widget_help = " ".join(help_parts) or None
                widget_key = (
                    f"{problem.__class__.__name__}:{spec.key}:"
                    f"{scale.display_unit or 'dimensionless'}"
                )

                if (
                    spec.control == "slider"
                    and min_display is not None
                    and max_display is not None
                ):
                    value_display = st.slider(
                        scale.label,
                        min_value=float(min_display),
                        max_value=float(max_display),
                        value=float(default_display),
                        step=float(step_display),
                        key=widget_key,
                        help=widget_help,
                    )
                elif (
                    spec.control == "log"
                    and min_display is not None
                    and min_display > 0
                    and max_display is not None
                    and max_display > min_display
                ):
                    import math

                    exponent = st.slider(
                        scale.label,
                        min_value=float(math.log10(min_display)),
                        max_value=float(math.log10(max_display)),
                        value=float(math.log10(default_display)),
                        step=0.05,
                        key=widget_key,
                        help=(widget_help or "") + " Logaritmisk skala.",
                        format="10^%.2f",
                    )
                    value_display = 10.0 ** exponent
                else:
                    number_kwargs = {
                        "label": scale.label,
                        "value": float(default_display),
                        "step": float(step_display),
                        "format": "%.12g",
                        "key": widget_key,
                        "help": widget_help,
                    }
                    if min_display is not None:
                        number_kwargs["min_value"] = float(min_display)
                    if max_display is not None:
                        number_kwargs["max_value"] = float(max_display)
                    value_display = st.number_input(**number_kwargs)

                params[spec.key] = scale.to_si(value_display)

            st.form_submit_button("Uppdatera figurer", type="primary", use_container_width=True)

if content_type == "Teori":
    render_theory_page(theory_page)
    st.stop()

st.subheader(problem.name)
st.write(problem.description)

with st.expander("Fysikalisk idé", expanded=True):
    st.write(problem.pedagogical_note())

issues = problem.validate_all(params)
for issue in issues:
    if issue.severity == "error":
        st.error(issue.message)
    else:
        st.warning(issue.message)
if any(issue.severity == "error" for issue in issues):
    st.stop()

try:
    st.info(problem.result_summary(params, mode))
except Exception as exc:
    st.warning(f"Kunde inte beräkna sammanfattning: {exc}")

quality_dpi = {"Snabb": 82, "Normal": 110, "Hög": 145}[quality]


def render_main_graph(container):
    try:
        fig = Figure(figsize=(7.0, 6.0), dpi=quality_dpi)
        problem.plot(fig, params, mode)
        fig.tight_layout()
        with container:
            st.markdown("#### Huvudgraf")
            st.pyplot(fig, clear_figure=True)
    except Exception as exc:
        with container:
            st.error(f"Fel i huvudgraf: {exc}")


def render_geometry(container):
    try:
        geometry_fig = Figure(figsize=(3.8, 6.0), dpi=quality_dpi)
        problem.draw_geometry(geometry_fig, params)
        geometry_fig.tight_layout()
        with container:
            st.markdown("#### Geometriskiss")
            st.pyplot(geometry_fig, clear_figure=True)
    except Exception as exc:
        with container:
            st.error(f"Fel i geometriskiss: {exc}")


def render_3d(container):
    try:
        view3d_fig = make_plotly_3d_figure(problem, params, mode)
        with container:
            st.markdown("#### 3-D-vy")
            st.caption("Rotera, zooma och panorera direkt i webbläsaren.")
            st.plotly_chart(
                view3d_fig,
                use_container_width=True,
                config={"displaylogo": False},
                key=f"plotly:{problem.__class__.__name__}:{mode}",
            )
    except Exception as exc:
        with container:
            st.error(f"Fel i interaktiv 3-D-vy: {exc}")
            st.info(
                "Reservvisning med Matplotlib visas eftersom Plotly-renderingen misslyckades."
            )
            fallback_fig = Figure(figsize=(4.8, 6.0), dpi=quality_dpi)
            problem.draw_3d(fallback_fig, params, mode)
            fallback_fig.tight_layout()
            st.pyplot(fallback_fig, clear_figure=True)


if view_mode == "Alla":
    col1, col2, col3 = st.columns([5, 3, 4])
    render_main_graph(col1)
    render_geometry(col2)
    render_3d(col3)
elif view_mode == "Huvudgraf":
    render_main_graph(st.container())
elif view_mode == "Geometriskiss":
    render_geometry(st.container())
else:
    render_3d(st.container())

with st.expander("Kontrollera formel/gränsfall"):
    try:
        st.write(problem.physics_check(params))
    except Exception as exc:
        st.error(f"Kontrollen misslyckades: {exc}")
