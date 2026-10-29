from pathlib import Path

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
    assert _radio(app, "Arbetssätt").value == "Lös uppgift"
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


def test_explore_mode_exposes_parameters_without_requiring_written_prediction():
    app = _run_app()
    _radio(app, "Arbetssätt").set_value("Utforska").run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert any(expander.label == "Parametrar för utforskning" for expander in app.expander)
    assert not any(
        area.label == "Skriv vad du tror att figuren kommer att visa"
        for area in app.text_area
    )
    assert any(button.label == "Visa figur" for button in app.button)


def test_theory_page_runs_without_streamlit_exception():
    app = _run_app()
    _radio(app, "Arbetssätt").set_value("Teori").run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert any(selectbox.label == "Teoriavsnitt" for selectbox in app.selectbox)


def test_targeted_help_uses_problem_specific_hints_and_keeps_legacy_fallback():
    from em_visualisering.guidance import guidance_for_problem
    from em_visualisering.registry import PROBLEMS

    app = _run_app()
    # Keep a real legacy fallback case as successive chapters are reviewed.
    legacy = next(p for p in PROBLEMS
                  if not guidance_for_problem(p).setup_hint
                  and not guidance_for_problem(p).geometry_hint)
    for pid in ("2.1", "2.8", legacy.name.split()[0]):
        app.selectbox(key="selected-chapter").set_value(int(pid.split(".")[0])).run()
        problem = next(p for p in PROBLEMS if p.name.split()[0] == pid)
        guidance = guidance_for_problem(problem)
        next(w for w in app.selectbox if w.label == "Uppgift").set_value(problem.name).run()
        for choice, expected in (
            ("Jag vet vilken idé jag vill använda men får inte upp matematiken",
             guidance.setup_hint or guidance.hints[0]),
            ("Jag fastnar på vektorer eller geometri",
             guidance.geometry_hint or guidance.hints[1]),
        ):
            next(w for w in app.selectbox if w.label == "Vad behöver du hjälp med?").set_value(choice).run()
            assert not app.exception
            assert any(expected in message.value for message in app.info)


def test_navigation_resets_disclosures_and_help_but_not_ordinary_reruns():
    app = _run_app()
    first_name = app.selectbox(key="selected-problem").value
    first_panel = next(e for e in app.expander if e.label == "Ledtråd 1")._block_id
    help_box = next(w for w in app.selectbox if w.label == "Vad behöver du hjälp med?")
    help_box.select_index(2).run()
    assert next(e for e in app.expander if e.label == "Ledtråd 1")._block_id == first_panel

    app.selectbox(key="selected-problem").select_index(1).run()
    second_panel = next(e for e in app.expander if e.label == "Ledtråd 1")._block_id
    assert second_panel != first_panel
    assert next(w for w in app.selectbox if w.label == "Vad behöver du hjälp med?").value is None

    app.selectbox(key="selected-problem").set_value(first_name).run()
    assert next(e for e in app.expander if e.label == "Ledtråd 1")._block_id not in (first_panel, second_panel)
    assert next(w for w in app.selectbox if w.label == "Vad behöver du hjälp med?").value is None
    app.selectbox(key="selected-chapter").set_value(3).run()
    assert not app.exception
    assert all(not e.proto.expanded for e in app.expander if e.label.startswith(("Ledtråd", "Kontroll", "Visa facit")))


def test_navigation_hides_previously_revealed_figures():
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



def test_all_chapter_four_problems_show_their_specific_targeted_help():
    from em_visualisering.guidance import guidance_for_problem
    from em_visualisering.registry import PROBLEMS

    app = _run_app()
    app.selectbox(key="selected-chapter").set_value(4).run()
    for problem in (p for p in PROBLEMS if p.name.startswith("4.")):
        app.selectbox(key="selected-problem").set_value(problem.name).run()
        guidance = guidance_for_problem(problem)
        for index, expected in ((1, guidance.setup_hint), (2, guidance.geometry_hint)):
            assert expected
            next(w for w in app.selectbox if w.label == "Vad behöver du hjälp med?").select_index(index).run()
            assert not app.exception
            assert any(expected in message.value for message in app.info)
