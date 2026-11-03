from pathlib import Path

import pytest

from streamlit.testing.v1 import AppTest


def _run_app() -> AppTest:
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "streamlit_app.py", default_timeout=120)
    app.run()
    assert not app.exception, [exception.value for exception in app.exception]
    return app


def _radio(app: AppTest, label: str):
    return next(widget for widget in app.radio if widget.label == label)


def test_default_page_is_clean_solve_mode():
    app = _run_app()
    assert app.title[0].value == "EM-studiehjälp"
    assert not any(widget.label == "Arbetssätt" for widget in app.radio)
    assert not any(widget.label == "Teoriavsnitt" for widget in app.selectbox)
    assert any(selectbox.label == "Kapitel" for selectbox in app.selectbox)
    assert any(selectbox.label == "Uppgift" for selectbox in app.selectbox)
    # Parameter controls belong to Explore, not the default solving workflow.
    assert not app.number_input
    assert not any(selectbox.label.startswith("Enhet för") for selectbox in app.selectbox)


def test_solve_mode_has_no_required_solution_path_quiz():
    app = _run_app()
    assert not any(
        selectbox.label == "Vilken huvudmetod skulle du prova först?"
        for selectbox in app.selectbox
    )
    assert not any(
        markdown.value == "### Välj en lösningsväg"
        for markdown in app.markdown
    )


def test_self_checks_are_optional_expanders_not_fake_text_inputs():
    app = _run_app()
    assert any(expander.label == "Kontroll 1" for expander in app.expander)
    assert not any(
        widget.label.startswith("Kontrollpunkt")
        for widget in app.text_input
    )


def test_real_facit_is_a_simple_expander_without_fake_readiness_gate():
    app = _run_app()
    assert any(expander.label == "Visa facit" for expander in app.expander)
    assert not any(
        checkbox.label == "Jag har ett färdigt eget försök"
        for checkbox in app.checkbox
    )
    assert not any(
        button.label == "Visa appens kontrollresultat"
        for button in app.button
    )


def test_explore_mode_exposes_parameters_without_requiring_written_prediction(monkeypatch):
    monkeypatch.setenv("TFYB05_ENABLE_UNFINISHED_MODES", "1")
    app = _run_app()
    _radio(app, "Arbetssätt").set_value("Utforska").run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert any(expander.label == "Parametrar för utforskning" for expander in app.expander)
    assert not any(
        area.label == "Skriv vad du tror att figuren kommer att visa"
        for area in app.text_area
    )
    assert any(button.label == "Visa figur" for button in app.button)


def test_theory_page_runs_without_streamlit_exception(monkeypatch):
    monkeypatch.setenv("TFYB05_ENABLE_UNFINISHED_MODES", "1")
    app = _run_app()
    _radio(app, "Arbetssätt").set_value("Teori").run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert any(selectbox.label == "Teoriavsnitt" for selectbox in app.selectbox)


@pytest.mark.parametrize("chapter", range(2, 11))
def test_all_problems_show_specific_help_and_reset_on_navigation(chapter):
    from em_visualisering.guidance import guidance_for_problem
    from em_visualisering.registry import PROBLEMS

    app = _run_app()
    app.selectbox(key="selected-chapter").set_value(chapter).run()
    for problem in (p for p in PROBLEMS if p.name.startswith(f"{chapter}.")):
        app.selectbox(key="selected-problem").set_value(problem.name).run()
        assert not any(e.label == "Geometriskiss till uppgiften" for e in app.expander)
        guidance = guidance_for_problem(problem)
        key = f"stuck:{problem.__class__.__name__}"
        assert app.selectbox(key=key).value is None
        panel = next(e for e in app.expander if e.label == "Visa startlagen och hur du börjar")
        assert not panel.proto.expanded and panel.latex
        for index, expected in enumerate((
            guidance.setup_hint,
            guidance.geometry_hint, guidance.self_checks[0],
        )):
            app.selectbox(key=key).select_index(index).run()
            assert not app.exception, problem.name
            assert expected in app.info[-1].value, (problem.name, index)
            assert all(not e.proto.expanded for e in app.expander
                       if e.label.startswith(("Ledtråd", "Kontroll", "Visa facit")))
        # Clearing a choice must also remove its answer, without navigation.
        app.selectbox(key=key).set_value(None).run()
        assert not app.info
        app.selectbox(key=key).select_index(2).run()


def test_navigation_resets_disclosures_and_help_but_not_ordinary_reruns():
    app = _run_app()
    first_name = app.selectbox(key="selected-problem").value
    def law_panel():
        return next(e for e in app.expander if e.label == "Visa startlagen och hur du börjar")

    first_law = law_panel()._block_id
    first_panel = next(e for e in app.expander if e.label.startswith("Ledtråd 1 ·"))._block_id
    help_box = next(w for w in app.selectbox if w.label == "Vad behöver du hjälp med?")
    help_box.select_index(2).run()
    assert next(e for e in app.expander if e.label.startswith("Ledtråd 1 ·"))._block_id == first_panel

    app.selectbox(key="selected-problem").select_index(1).run()
    second_panel = next(e for e in app.expander if e.label.startswith("Ledtråd 1 ·"))._block_id
    assert law_panel()._block_id != first_law and not law_panel().proto.expanded
    assert second_panel != first_panel
    assert next(w for w in app.selectbox if w.label == "Vad behöver du hjälp med?").value is None

    app.selectbox(key="selected-problem").set_value(first_name).run()
    assert next(e for e in app.expander if e.label.startswith("Ledtråd 1 ·"))._block_id not in (first_panel, second_panel)
    assert next(w for w in app.selectbox if w.label == "Vad behöver du hjälp med?").value is None
    app.selectbox(key="selected-chapter").set_value(3).run()
    assert not app.exception
    assert all(not e.proto.expanded for e in app.expander if e.label.startswith(("Ledtråd", "Kontroll", "Visa facit")))


def test_navigation_hides_previously_revealed_figures(monkeypatch):
    monkeypatch.setenv("TFYB05_ENABLE_UNFINISHED_MODES", "1")
    app = _run_app()
    app.selectbox(key="selected-problem").select_index(1).run()
    _radio(app, "Arbetssätt").set_value("Utforska").run()
    first_name = app.selectbox(key="selected-problem").value
    next(b for b in app.button if b.label == "Visa figur").click().run()
    assert app.session_state["visualization-revealed:ChargedRingAxis:Field"] is True
    app.selectbox(key="selected-problem").select_index(2).run()
    app.selectbox(key="selected-problem").set_value(first_name).run()
    assert not app.exception
    assert "visualization-revealed:ChargedRingAxis:Field" not in app.session_state


def test_variable_conductivity_explore_views_are_named_and_renderable(monkeypatch):
    monkeypatch.setenv("TFYB05_ENABLE_UNFINISHED_MODES", "1")
    app = _run_app()
    app.selectbox(key="selected-chapter").set_value(5).run()
    problem_name = next(name for name in app.selectbox(key="selected-problem").options if name.startswith("5.7 "))
    app.selectbox(key="selected-problem").set_value(problem_name).run()
    _radio(app, "Arbetssätt").set_value("Utforska").run()
    labels = ["Elektriskt fält E", "Strömtäthet J", "Fri laddningstäthet ρ"]
    assert next(w for w in app.selectbox if w.label == "Vad vill du visualisera?").options == labels
    for label in labels:
        next(w for w in app.selectbox if w.label == "Vad vill du visualisera?").set_value(label).run()
        next(b for b in app.button if b.label == "Visa figur").click().run()
        assert not app.exception
        assert not any("kunde inte" in warning.value for warning in app.warning)


def test_chapter_2_4_has_no_obsolete_3d_visualization(monkeypatch):
    monkeypatch.setenv("TFYB05_ENABLE_UNFINISHED_MODES", "1")
    app = _run_app()
    problem_name = next(name for name in app.selectbox(key="selected-problem").options if name.startswith("2.4 "))
    app.selectbox(key="selected-problem").set_value(problem_name).run()
    _radio(app, "Arbetssätt").set_value("Utforska").run()
    next(c for c in app.checkbox if c.label == "Visa den äldre visualiseringen ändå").check().run()
    next(button for button in app.button if button.label == "Visa figur").click().run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert not any(expander.label == "Avancerat: visa äldre 3-D-vy" for expander in app.expander)
    assert not any(checkbox.label == "Rendera 3-D-vy" for checkbox in app.checkbox)


@pytest.mark.parametrize("pid", ["2.3", "2.4", "3.9", "9.13"])
def test_geometry_panels_are_hidden_but_main_plots_remain(monkeypatch, pid):
    monkeypatch.setenv("TFYB05_ENABLE_UNFINISHED_MODES", "1")
    app = _run_app()
    app.selectbox(key="selected-chapter").set_value(int(pid.split(".")[0])).run()
    problem_name = next(name for name in app.selectbox(key="selected-problem").options
                        if name.startswith(pid + " "))
    app.selectbox(key="selected-problem").set_value(problem_name).run()
    assert not app.exception
    assert not any(e.label == "Geometriskiss till uppgiften" for e in app.expander)

    _radio(app, "Arbetssätt").set_value("Utforska").run()
    override = next((c for c in app.checkbox if c.label == "Visa den äldre visualiseringen ändå"), None)
    if override is not None:
        override.check().run()
    next(b for b in app.button if b.label == "Visa figur").click().run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert not any(m.value == "#### Geometriskiss" for m in app.markdown)
    assert any(m.value == "#### Huvudvisualisering" for m in app.markdown)
