"""TFYB05 study interface focused on problem-solving rather than plotting.

Run locally with:
    streamlit run streamlit_app.py

The default "Lös uppgift" mode shows the problem, method choice, progressive help,
active self-checks and a deliberately gated answer check. Parameter controls and
visualisations live in the separate "Utforska" mode.
"""

from __future__ import annotations

from io import BytesIO
import math

import matplotlib

matplotlib.use("Agg", force=True)

import plotly.io as pio
import streamlit as st
from matplotlib.figure import Figure

from em_visualisering.guidance import guidance_for_problem
from em_visualisering.facit import facit_for_problem
from em_visualisering.modes import mode_options_for_problem, normalize_mode_for_problem
from em_visualisering.plotly_bridge import make_plotly_3d_figure
from em_visualisering.registry import PROBLEMS
from em_visualisering.study_content import (
    CHAPTER_TITLES,
    chapter_number,
    method_key_for_problem,
    method_label,
    method_meta_for_problem,
    method_options_for_problem,
    problem_id_from_name,
    statement_for_problem,
)
from em_visualisering.theory_pages import THEORY_PAGES, render_theory_page
from em_visualisering.unit_scaling import (
    display_scale_by_unit,
    display_scale_for,
    selectable_display_scales,
    split_label,
    suggested_step,
)


st.set_page_config(
    page_title="EM-studiehjälp",
    page_icon="⚡",
    layout="wide",
)


problem_class_lookup = {problem.__class__.__name__: problem for problem in PROBLEMS}
theory_lookup = {page.title: page for page in THEORY_PAGES}


def _problems_by_chapter() -> dict[int, list]:
    grouped: dict[int, list] = {}
    for problem in PROBLEMS:
        pid = problem_id_from_name(problem.name)
        grouped.setdefault(chapter_number(pid), []).append(problem)
    return grouped


PROBLEMS_BY_CHAPTER = _problems_by_chapter()


@st.cache_data(show_spinner=False, max_entries=256)
def _render_matplotlib_png(
    problem_class_name: str,
    params_items: tuple[tuple[str, float], ...],
    mode: str,
    view: str,
    dpi: int,
) -> bytes:
    problem = problem_class_lookup[problem_class_name]
    params = dict(params_items)

    if view == "main":
        fig = Figure(figsize=(7.0, 5.6), dpi=dpi)
        problem.plot(fig, params, mode)
    elif view == "geometry":
        fig = Figure(figsize=(4.4, 4.6), dpi=dpi)
        problem.draw_geometry(fig, params)
    elif view == "3d":
        fig = Figure(figsize=(5.0, 5.6), dpi=dpi)
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


def _default_mode(problem) -> str:
    options = mode_options_for_problem(problem)
    requested = options[0][1]
    return normalize_mode_for_problem(problem, requested)


def _default_params(problem) -> dict[str, float]:
    return {key: float(value) for key, value in problem.defaults().items()}


def _params_items(params: dict[str, float]) -> tuple[tuple[str, float], ...]:
    return tuple(sorted((key, float(value)) for key, value in params.items()))


def _state_prefix(problem) -> str:
    return f"parameter-state:{problem.__class__.__name__}"


def _draft_key(problem, parameter_key: str) -> str:
    return f"{_state_prefix(problem)}:draft-si:{parameter_key}"


def _applied_key(problem) -> str:
    return f"{_state_prefix(problem)}:applied"


def _initialize_problem_state(problem) -> None:
    defaults = _default_params(problem)
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
                "value": int(round(displayed_value))
                if spec.integer
                else float(displayed_value),
                "step": max(1, int(round(step_display)))
                if spec.integer
                else float(step_display),
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


def _render_problem_statement(problem) -> str:
    statement = statement_for_problem(problem)
    st.markdown("### Uppgift")
    st.markdown(statement)
    return statement


def _render_geometry_if_needed(problem, statement: str) -> None:
    if "figur" not in statement.lower():
        return

    with st.expander("Geometriskiss till uppgiften", expanded=True):
        try:
            params = _default_params(problem)
            png = _render_matplotlib_png(
                problem.__class__.__name__,
                _params_items(params),
                _default_mode(problem),
                "geometry",
                95,
            )
            st.image(png, width="stretch")
            st.caption(
                "Skissen är appens rena geometrivisning. Själva uppgiftstexten ovan "
                "är hämtad från problemsamlingen."
            )
        except Exception as exc:
            st.warning(f"Geometriskissen kunde inte visas: {exc}")


def _render_method_choice(problem, guidance) -> None:
    st.markdown("### Välj en lösningsväg")
    st.caption(
        "Gör valet innan du öppnar ledtrådarna. Flera metoder kan i princip fungera; "
        "här tränar vi på att hitta den mest direkta vägen."
    )

    option_keys = method_options_for_problem(problem)
    labels = {method_label(key): key for key in option_keys}
    selected_label = st.selectbox(
        "Vilken huvudmetod skulle du prova först?",
        list(labels),
        index=None,
        placeholder="Välj metod efter att du har läst uppgiften",
        key=f"method-choice:{problem.__class__.__name__}",
    )
    if selected_label is None:
        return

    selected_key = labels[selected_label]
    recommended_key = method_key_for_problem(problem)
    recommended = method_meta_for_problem(problem)

    if selected_key == recommended_key:
        st.success(
            "Bra val. Den metoden passar problemets struktur och leder relativt direkt "
            "till den storhet som efterfrågas."
        )
    else:
        st.info(
            f"Den vägen kan innehålla användbara idéer, men en mer direkt start här är "
            f"**{recommended.label}**. {recommended.rationale}"
        )


def _render_training_focus(problem, guidance) -> None:
    meta = method_meta_for_problem(problem)
    st.markdown("### Det här tränar du")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Fysik**")
        st.write(" · ".join(guidance.concepts))
        st.caption(guidance.learning_goal)
    with col2:
        st.markdown("**Matematisk rörelse**")
        st.write(meta.math_focus)


def _render_targeted_help(problem, guidance) -> None:
    st.markdown("### Om du sitter fast")
    stuck = st.selectbox(
        "Var sitter du fast?",
        [
            "Välja metod",
            "Sätta upp matematiken",
            "Vektorer / geometri",
            "Kontrollera om svaret är rimligt",
        ],
        index=None,
        placeholder="Välj bara om du behöver hjälp",
        key=f"stuck:{problem.__class__.__name__}",
    )
    if stuck is None:
        return

    if stuck == "Välja metod":
        st.info(guidance.start_here)
    elif stuck == "Sätta upp matematiken":
        st.info(guidance.hints[0])
    elif stuck == "Vektorer / geometri":
        hint = guidance.hints[1] if len(guidance.hints) > 1 else guidance.hints[0]
        meta = method_meta_for_problem(problem)
        st.info(f"{meta.math_focus}\n\n{hint}")
    else:
        st.info(
            "Använd kontrollpunkterna längre ned på sidan. Försök först själv tänka på "
            "symmetri, tecken, enheter eller ett enkelt gränsfall och öppna sedan en "
            "kontroll i taget."
        )


def _render_progressive_hints(problem, guidance) -> None:
    st.markdown("#### Progressiva ledtrådar")
    st.caption(
        "Öppna endast nästa nivå när du inte kommer vidare. Målet är att behålla så "
        "mycket av lösningsarbetet som möjligt hos dig."
    )
    for index, hint in enumerate(guidance.hints, start=1):
        with st.expander(f"Ledtråd {index}", expanded=False):
            st.write(hint)

    if guidance.common_pitfall:
        with st.expander("Vanlig fallgrop", expanded=False):
            st.warning(guidance.common_pitfall)


def _render_solution_checks(problem, guidance) -> None:
    st.markdown("### Kontrollera ditt resultat")
    st.caption(
        "Det här är extra ledtrådar för att testa din färdiga eller nästan färdiga "
        "lösning. Försök själv tänka igenom kontrollen innan du öppnar den."
    )

    for index, check in enumerate(guidance.self_checks, start=1):
        with st.expander(f"Kontroll {index}", expanded=False):
            st.write(check)


def _render_facit(problem) -> None:
    st.markdown("### Facit")
    st.caption(
        "Detta är slutresultatet från problemsamlingens tryckta facit. "
        "Det är avsiktligt inte en fullständig lösning."
    )
    with st.expander("Visa facit", expanded=False):
        answer = facit_for_problem(problem)
        if answer:
            st.markdown(answer)
        else:
            st.warning("Inget facit är registrerat för den här uppgiften.")


def _render_solve_mode(problem) -> None:
    guidance = guidance_for_problem(problem)
    st.subheader(problem.name)
    statement = _render_problem_statement(problem)
    _render_geometry_if_needed(problem, statement)

    if guidance is None:
        st.warning("Specifik progressiv vägledning saknas för den här uppgiften.")
        with st.expander("Fysikalisk idé", expanded=True):
            st.write(problem.pedagogical_note())
        return

    _render_method_choice(problem, guidance)
    _render_training_focus(problem, guidance)

    st.markdown("### Börja här")
    st.info(guidance.start_here)

    _render_targeted_help(problem, guidance)
    _render_progressive_hints(problem, guidance)
    _render_solution_checks(problem, guidance)
    _render_facit(problem)


def _render_explore_parameters(problem) -> dict[str, float]:
    _initialize_problem_state(problem)

    with st.expander("Parametrar för utforskning", expanded=False):
        st.caption(
            "Ändra bara parametrar när du vill undersöka ett gränsfall eller en "
            "fysikalisk trend. De är inte en del av själva lösningssteget."
        )
        for spec in problem.parameter_specs():
            value_si = _render_parameter_control(problem, spec)
            st.session_state[_draft_key(problem, spec.key)] = value_si

        draft_params = _current_draft(problem)
        applied_params = dict(st.session_state[_applied_key(problem)])
        has_pending_changes = any(
            not math.isclose(
                draft_params[key],
                applied_params[key],
                rel_tol=1e-12,
                abs_tol=0.0,
            )
            for key in draft_params
        )
        if has_pending_changes:
            st.caption("● Parameterändringar väntar på att appliceras.")

        c1, c2 = st.columns(2)
        with c1:
            apply_clicked = st.button(
                "Applicera parametrar",
                type="primary",
                width="stretch",
                key=f"apply:{problem.__class__.__name__}",
            )
        with c2:
            reset_clicked = st.button(
                "Återställ",
                width="stretch",
                key=f"reset:{problem.__class__.__name__}",
            )

        if reset_clicked:
            defaults = _default_params(problem)
            _clear_problem_widget_state(problem)
            for key, value in defaults.items():
                st.session_state[_draft_key(problem, key)] = value
            st.session_state[_applied_key(problem)] = defaults
            st.rerun()

        if apply_clicked:
            draft_issues = problem.validate_all(draft_params)
            errors = [issue for issue in draft_issues if issue.severity == "error"]
            if errors:
                for issue in errors:
                    st.error(issue.message)
            else:
                st.session_state[_applied_key(problem)] = dict(draft_params)
                st.rerun()

    return dict(st.session_state[_applied_key(problem)])


def _render_main_graph(problem, params, mode, dpi) -> None:
    try:
        png = _render_matplotlib_png(
            problem.__class__.__name__, _params_items(params), mode, "main", dpi
        )
        st.markdown("#### Huvudvisualisering")
        st.image(png, width="stretch")
    except Exception as exc:
        st.error(f"Huvudvisualiseringen kunde inte visas: {exc}")


def _render_geometry(problem, params, mode, dpi) -> None:
    try:
        png = _render_matplotlib_png(
            problem.__class__.__name__, _params_items(params), mode, "geometry", dpi
        )
        st.markdown("#### Geometriskiss")
        st.image(png, width="stretch")
    except Exception as exc:
        st.error(f"Geometriskissen kunde inte visas: {exc}")


def _render_3d(problem, params, mode) -> None:
    try:
        fig = pio.from_json(
            _render_plotly_json(
                problem.__class__.__name__, _params_items(params), mode
            )
        )
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displaylogo": False},
            key=f"plotly:{problem.__class__.__name__}:{mode}",
        )
    except Exception as exc:
        st.warning(f"3-D-vyn kunde inte visas: {exc}")


def _render_explore_mode(problem) -> None:
    guidance = guidance_for_problem(problem)
    st.subheader(f"Utforska: {problem.name}")

    with st.expander("Visa uppgiftstext", expanded=False):
        st.markdown(statement_for_problem(problem))

    options = mode_options_for_problem(problem)
    labels = [label for label, _internal in options]
    selected_label = st.selectbox(
        "Vad vill du visualisera?",
        labels,
        index=0,
        key=f"explore-mode:{problem.__class__.__name__}",
    )
    mode = normalize_mode_for_problem(problem, dict(options)[selected_label])

    params = _render_explore_parameters(problem)

    st.markdown("### Förutsäg innan du tittar")
    st.info(
        "Gör en snabb mental förutsägelse innan du visar figuren: tänk till exempel "
        "på tecken, nollställen, symmetri, gränsfall eller hur en parameter bör påverka "
        "resultatet. Du behöver inte skriva ned svaret."
    )
    if guidance and guidance.visualization_note:
        st.caption("Varför figuren kan hjälpa: " + guidance.visualization_note)
        recommended = True
    else:
        st.warning(
            "Den här uppgiften har ingen rekommenderad visualisering i studieläget. "
            "För den är lösningsstrategin viktigare än en graf."
        )
        recommended = False

    override = False
    if not recommended:
        override = st.checkbox(
            "Visa den äldre visualiseringen ändå",
            key=f"override-visualization:{problem.__class__.__name__}",
        )

    can_reveal = recommended or override
    reveal_key = f"visualization-revealed:{problem.__class__.__name__}:{mode}"
    if st.button(
        "Visa figur",
        key=f"reveal-visualization:{problem.__class__.__name__}:{mode}",
        disabled=not can_reveal,
        type="primary",
    ):
        st.session_state[reveal_key] = True

    if not st.session_state.get(reveal_key, False):
        return

    quality = st.select_slider(
        "Återgivningskvalitet",
        options=["Snabb", "Normal", "Hög"],
        value="Normal",
        key=f"quality:{problem.__class__.__name__}",
    )
    dpi = {"Snabb": 82, "Normal": 110, "Hög": 145}[quality]

    col1, col2 = st.columns([3, 2])
    with col1:
        _render_main_graph(problem, params, mode, dpi)
    with col2:
        _render_geometry(problem, params, mode, dpi)

    st.caption(
        "Jämför nu figuren med din förutsägelse: stämde tecken, symmetri, nollställen "
        "och gränsfall med det du väntade dig?"
    )

    with st.expander("Avancerat: visa äldre 3-D-vy", expanded=False):
        st.caption(
            "3-D-vyn är inte en standarddel av studiegången. Öppna den bara om den "
            "hjälper dig att tolka geometrin eller fältstrukturen."
        )
        if st.checkbox(
            "Rendera 3-D-vy",
            key=f"render-3d:{problem.__class__.__name__}:{mode}",
        ):
            _render_3d(problem, params, mode)


    with st.expander("Avancerat: appens beräkning och interna kontroll", expanded=False):
        st.caption(
            "Det här är inte kursens facit. Det är appens egen beräkning för de "
            "parametrar du valt och kan användas vid teknisk utforskning."
        )
        try:
            st.info(problem.result_summary(params, mode))
        except Exception as exc:
            st.warning(f"Appens beräkning kunde inte utföras: {exc}")
        try:
            st.write(problem.physics_check(params))
        except Exception as exc:
            st.warning(f"Den interna kontrollen kunde inte utföras: {exc}")


st.title("EM-studiehjälp")
st.caption(
    "Lös först. Be om minsta möjliga ledtråd. Kontrollera sedan. "
    "Utforska med figurer först efter att du själv har försökt förutsäga vad de bör visa."
)


with st.sidebar:
    work_mode = st.radio(
        "Arbetssätt",
        ["Lös uppgift", "Utforska", "Teori"],
        index=0,
    )

    if work_mode == "Teori":
        theory_title = st.selectbox(
            "Teoriavsnitt",
            [page.title for page in THEORY_PAGES],
            index=0,
        )
        theory_page = theory_lookup[theory_title]
        st.caption(theory_page.short_description)
    else:
        chapters = sorted(PROBLEMS_BY_CHAPTER)
        selected_chapter = st.selectbox(
            "Kapitel",
            chapters,
            format_func=lambda ch: f"Kapitel {ch} – {CHAPTER_TITLES.get(ch, '')}",
            key="selected-chapter",
        )
        chapter_problems = PROBLEMS_BY_CHAPTER[selected_chapter]
        selected_problem_name = st.selectbox(
            "Uppgift",
            [problem.name for problem in chapter_problems],
            key="selected-problem",
        )
        problem = next(
            p for p in chapter_problems if p.name == selected_problem_name
        )


if work_mode == "Teori":
    render_theory_page(theory_page)
elif work_mode == "Utforska":
    _render_explore_mode(problem)
else:
    _render_solve_mode(problem)
