from streamlit.testing.v1 import AppTest


def _run_app() -> AppTest:
    app = AppTest.from_file("streamlit_app.py", default_timeout=120)
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
