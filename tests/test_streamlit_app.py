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


def test_explore_mode_exposes_parameter_controls_without_showing_graph_immediately():
    app = _run_app()
    _radio(app, "Arbetssätt").set_value("Utforska").run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert any(expander.label == "Parametrar för utforskning" for expander in app.expander)
    assert any(area.label == "Skriv vad du tror att figuren kommer att visa" for area in app.text_area)


def test_theory_page_runs_without_streamlit_exception():
    app = _run_app()
    _radio(app, "Arbetssätt").set_value("Teori").run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert any(selectbox.label == "Teoriavsnitt" for selectbox in app.selectbox)
