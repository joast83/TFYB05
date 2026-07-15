"""Webbversion av EM-visualiseringar.

Kör lokalt med:
    streamlit run streamlit_app.py
"""

from __future__ import annotations

from io import BytesIO, StringIO
import csv
import json
import math

import matplotlib
matplotlib.use("Agg", force=True)

import plotly.io as pio
import streamlit as st
from matplotlib.figure import Figure

from em_visualisering.modes import mode_options_for_problem, normalize_mode_for_problem
from em_visualisering.plotly_bridge import make_plotly_3d_figure
from em_visualisering.registry import PROBLEMS
from em_visualisering.theory_pages import THEORY_PAGES, render_theory_page
from em_visualisering.unit_scaling import (
    display_scale_by_unit,
    display_scale_for,
    selectable_display_scales,
    split_label,
    suggested_step,
)


st.set_page_config(
    page_title="EM-visualiseringar",
    page_icon="⚡",
    layout="wide",
)

problem_lookup = {problem.name: problem for problem in PROBLEMS}
problem_class_lookup = {problem.__class__.__name__: problem for problem in PROBLEMS}
theory_lookup = {page.title: page for page in THEORY_PAGES}


@st.cache_data(show_spinner=False, max_entries=256)
def _render_matplotlib_png(
    problem_class_name: str,
    params_items: tuple[tuple[str, float], ...],
    mode: str,
    view: str,
    dpi: int,
) -> bytes:
    """Render a deterministic Matplotlib view and cache the encoded PNG."""

    problem = problem_class_lookup[problem_class_name]
    params = dict(params_items)
    if view == "main":
        fig = Figure(figsize=(7.0, 6.0), dpi=dpi)
        problem.plot(fig, params, mode)
    elif view == "geometry":
        fig = Figure(figsize=(3.8, 6.0), dpi=dpi)
        problem.draw_geometry(fig, params)
    elif view == "3d":
        fig = Figure(figsize=(4.8, 6.0), dpi=dpi)
        problem.draw_3d(fig, params, mode)
    else:
        raise ValueError(f"Okänd vy: {view}")
    fig.tight_layout()
    output = BytesIO()
    fig.savefig(output, format="png", dpi=dpi, bbox_inches="tight")
    return output.getvalue()


@st.cache_data(show_spinner=False, max_entries=128)
def _render_plotly_json(
    problem_class_name: str,
    params_items: tuple[tuple[str, float], ...],
    mode: str,
) -> str:
    problem = problem_class_lookup[problem_class_name]
    figure = make_plotly_3d_figure(problem, dict(params_items), mode)
    figure.update_layout(uirevision=f"{problem_class_name}:{mode}")
    return figure.to_json()


def _state_prefix(problem) -> str:
    return f"parameter-state:{problem.__class__.__name__}"


def _draft_key(problem, parameter_key: str) -> str:
    return f"{_state_prefix(problem)}:draft-si:{parameter_key}"


def _applied_key(problem) -> str:
    return f"{_state_prefix(problem)}:applied"


def _initialize_problem_state(problem) -> None:
    defaults = {key: float(value) for key, value in problem.defaults().items()}
    for key, value in defaults.items():
        st.session_state.setdefault(_draft_key(problem, key), value)
    st.session_state.setdefault(_applied_key(problem), defaults)


def _clear_problem_widget_state(problem) -> None:
    prefix = _state_prefix(problem)
    for key in list(st.session_state):
        if key.startswith(prefix) and key != _applied_key(problem):
            del st.session_state[key]


def _current_draft(problem) -> dict[str, float]:
    return {
        spec.key: float(st.session_state[_draft_key(problem, spec.key)])
        for spec in problem.parameter_specs()
    }


def _unit_scale_for_widget(problem, spec):
    scales = selectable_display_scales(
        spec.label, spec.default_si, spec.display_units
    )
    preferred = display_scale_for(spec.label, spec.default_si)
    allowed_units = [scale.display_unit for scale in scales]
    default_unit = (
        preferred.display_unit
        if preferred.display_unit in allowed_units
        else allowed_units[0]
    )
    unit_key = f"{_state_prefix(problem)}:unit:{spec.key}"
    if st.session_state.get(unit_key) not in allowed_units:
        st.session_state[unit_key] = default_unit
    return scales, unit_key


def _render_parameter_control(problem, spec) -> float:
    """Render one metadata-driven control and return its SI value."""

    draft_key = _draft_key(problem, spec.key)
    draft_si = float(st.session_state[draft_key])

    if spec.control == "select":
        mapping = spec.choice_map
        labels = list(mapping)
        selected_label = min(labels, key=lambda label: abs(mapping[label] - draft_si))
        widget_key = f"{_state_prefix(problem)}:select:{spec.key}"
        if st.session_state.get(widget_key) not in labels:
            st.session_state[widget_key] = selected_label
        selected = st.selectbox(
            spec.label,
            labels,
            key=widget_key,
            help=spec.help_text or None,
        )
        return mapping[selected]

    scales, unit_key = _unit_scale_for_widget(problem, spec)
    text_label, _si_unit = split_label(spec.label)
    if len(scales) > 1:
        value_column, unit_column = st.columns([3.4, 1.0], vertical_alignment="bottom")
        with unit_column:
            selected_unit = st.selectbox(
                f"Enhet för {text_label}",
                [scale.display_unit for scale in scales],
                key=unit_key,
                label_visibility="collapsed",
                help=f"Visningsenhet. Intern beräkning sker alltid i {spec.si_unit}.",
            )
    else:
        value_column = st.container()
        selected_unit = scales[0].display_unit
        st.session_state[unit_key] = selected_unit

    scale = display_scale_by_unit(spec.label, selected_unit)
    displayed_value = scale.to_display(draft_si)
    min_display = (
        scale.to_display(spec.ui_minimum_si)
        if spec.ui_minimum_si is not None
        else None
    )
    max_display = (
        scale.to_display(spec.ui_maximum_si)
        if spec.ui_maximum_si is not None
        else None
    )
    step_display = (
        spec.step_si / scale.factor
        if spec.step_si is not None
        else suggested_step(displayed_value)
    )
    help_parts = [spec.help_text] if spec.help_text else []
    if scale.factor != 1.0:
        help_parts.append(
            f"Visas i {scale.display_unit}; fysikmodellen använder {scale.si_unit}."
        )
    widget_help = " ".join(help_parts) or None
    widget_key = (
        f"{_state_prefix(problem)}:value:{spec.key}:"
        f"{scale.display_unit or 'dimensionless'}"
    )

    bounded = (
        min_display is not None
        and max_display is not None
        and min_display <= displayed_value <= max_display
        and max_display > min_display
    )

    with value_column:
        if spec.control == "slider" and bounded:
            if spec.integer and scale.factor == 1.0:
                value_display = st.slider(
                    scale.label,
                    min_value=int(round(min_display)),
                    max_value=int(round(max_display)),
                    value=int(round(displayed_value)),
                    step=max(1, int(round(step_display))),
                    key=widget_key,
                    help=widget_help,
                )
            else:
                value_display = st.slider(
                    scale.label,
                    min_value=float(min_display),
                    max_value=float(max_display),
                    value=float(displayed_value),
                    step=float(step_display),
                    key=widget_key,
                    help=widget_help,
                )
        elif spec.control == "log" and bounded and min_display > 0:
            exponent_key = widget_key + ":log10"
            exponent = st.slider(
                scale.label,
                min_value=float(math.log10(min_display)),
                max_value=float(math.log10(max_display)),
                value=float(math.log10(displayed_value)),
                step=0.05,
                key=exponent_key,
                help=(widget_help or "") + " Logaritmisk skala.",
                format="10^%.2f",
            )
            value_display = 10.0**exponent
            st.caption(f"Aktuellt värde: {value_display:.6g} {scale.display_unit}")
        else:
            number_kwargs = {
                "label": scale.label,
                "value": int(round(displayed_value)) if spec.integer else float(displayed_value),
                "step": max(1, int(round(step_display))) if spec.integer else float(step_display),
                "key": widget_key,
                "help": widget_help,
            }
            if spec.integer:
                number_kwargs["format"] = "%d"
            else:
                number_kwargs["format"] = "%.12g"
            value_display = st.number_input(**number_kwargs)

    value_si = scale.to_si(value_display)
    if spec.integer:
        value_si = float(round(value_si))
    return value_si


def _configuration_json(problem, mode: str, params: dict[str, float]) -> bytes:
    payload = {
        "schema_version": 1,
        "problem": problem.name,
        "problem_class": problem.__class__.__name__,
        "mode": mode,
        "parameters_si": params,
        "units": {spec.key: spec.si_unit for spec in problem.parameter_specs()},
    }
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


def _configuration_csv(problem, params: dict[str, float]) -> bytes:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["parameter", "label", "value_si", "si_unit"])
    for spec in problem.parameter_specs():
        writer.writerow([spec.key, split_label(spec.label)[0], params[spec.key], spec.si_unit])
    return output.getvalue().encode("utf-8-sig")


st.title("EM-visualiseringar")
st.caption(
    "Interaktiva visualiseringar för elektrostatik, magnetostatik och "
    "teoriavsnitt med interaktiva figurer."
)

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
        _initialize_problem_state(problem)

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
            "Redigera ett utkast och tryck sedan på Uppdatera figurer. Enhetsvalet "
            "påverkar endast presentationen; fysikberäkningen använder SI."
        )

        for spec in problem.parameter_specs():
            value_si = _render_parameter_control(problem, spec)
            st.session_state[_draft_key(problem, spec.key)] = value_si

        draft_params = _current_draft(problem)
        applied_params = dict(st.session_state[_applied_key(problem)])
        has_pending_changes = any(
            not math.isclose(draft_params[key], applied_params[key], rel_tol=1e-12, abs_tol=0.0)
            for key in draft_params
        )
        if has_pending_changes:
            st.caption("● Det finns ändringar som ännu inte har ritats.")

        apply_column, reset_column = st.columns(2)
        with apply_column:
            apply_clicked = st.button(
                "Uppdatera figurer", type="primary", width="stretch"
            )
        with reset_column:
            reset_clicked = st.button("Återställ", width="stretch")

        if reset_clicked:
            defaults = {key: float(value) for key, value in problem.defaults().items()}
            _clear_problem_widget_state(problem)
            for key, value in defaults.items():
                st.session_state[_draft_key(problem, key)] = value
            st.session_state[_applied_key(problem)] = defaults
            st.rerun()

        if apply_clicked:
            draft_issues = problem.validate_all(draft_params)
            draft_errors = [issue for issue in draft_issues if issue.severity == "error"]
            if draft_errors:
                for issue in draft_errors:
                    st.error(issue.message)
            else:
                st.session_state[_applied_key(problem)] = dict(draft_params)
                st.rerun()

        params = dict(st.session_state[_applied_key(problem)])

        with st.expander("Exportera aktuell konfiguration"):
            safe_name = problem.__class__.__name__
            st.download_button(
                "Ladda ned JSON",
                _configuration_json(problem, mode, params),
                file_name=f"{safe_name}_parameters.json",
                mime="application/json",
                width="stretch",
            )
            st.download_button(
                "Ladda ned CSV",
                _configuration_csv(problem, params),
                file_name=f"{safe_name}_parameters.csv",
                mime="text/csv",
                width="stretch",
            )

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
params_items = tuple(sorted((key, float(value)) for key, value in params.items()))
problem_class_name = problem.__class__.__name__


def render_main_graph(container):
    try:
        png = _render_matplotlib_png(
            problem_class_name, params_items, mode, "main", quality_dpi
        )
        with container:
            st.markdown("#### Huvudgraf")
            st.image(png, width="stretch")
            st.download_button(
                "Ladda ned huvudgraf (PNG)",
                png,
                file_name=f"{problem_class_name}_{mode}_main.png",
                mime="image/png",
                key=f"download:main:{problem_class_name}:{mode}:{quality_dpi}",
            )
    except Exception as exc:
        with container:
            st.error(f"Fel i huvudgraf: {exc}")


def render_geometry(container):
    try:
        png = _render_matplotlib_png(
            problem_class_name, params_items, mode, "geometry", quality_dpi
        )
        with container:
            st.markdown("#### Geometriskiss")
            st.image(png, width="stretch")
            st.download_button(
                "Ladda ned geometriskiss (PNG)",
                png,
                file_name=f"{problem_class_name}_geometry.png",
                mime="image/png",
                key=f"download:geometry:{problem_class_name}:{quality_dpi}",
            )
    except Exception as exc:
        with container:
            st.error(f"Fel i geometriskiss: {exc}")


def render_3d(container):
    try:
        view3d_fig = pio.from_json(
            _render_plotly_json(problem_class_name, params_items, mode)
        )
        with container:
            st.markdown("#### 3-D-vy")
            st.caption("Rotera, zooma och panorera direkt i webbläsaren.")
            st.plotly_chart(
                view3d_fig,
                width="stretch",
                config={"displaylogo": False},
                key=f"plotly:{problem_class_name}:{mode}",
            )
            st.download_button(
                "Ladda ned 3-D-vy (HTML)",
                view3d_fig.to_html(include_plotlyjs="cdn"),
                file_name=f"{problem_class_name}_{mode}_3d.html",
                mime="text/html",
                key=f"download:3d:{problem_class_name}:{mode}",
            )
    except Exception as exc:
        with container:
            st.error(f"Fel i interaktiv 3-D-vy: {exc}")
            st.info(
                "Reservvisning med Matplotlib visas eftersom Plotly-renderingen misslyckades."
            )
            png = _render_matplotlib_png(
                problem_class_name, params_items, mode, "3d", quality_dpi
            )
            st.image(png, width="stretch")


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
