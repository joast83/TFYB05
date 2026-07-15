import pytest

from streamlit.testing.v1 import AppTest


def _run_app() -> AppTest:
    app = AppTest.from_file("streamlit_app.py", default_timeout=120)
    app.run()
    assert not app.exception, [exception.value for exception in app.exception]
    return app


def _selectbox(app: AppTest, label_prefix: str):
    return next(widget for widget in app.selectbox if widget.label.startswith(label_prefix))


def _number_input(app: AppTest, label_fragment: str):
    return next(widget for widget in app.number_input if label_fragment in widget.label)


def _button(app: AppTest, label: str):
    return next(widget for widget in app.button if widget.label == label)


def test_default_exercise_page_runs_without_streamlit_exception():
    app = _run_app()
    assert app.title[0].value == "EM-visualiseringar"
    assert _button(app, "Uppdatera figurer")
    assert _button(app, "Återställ")


def test_charge_unit_switch_apply_and_reset_round_trip():
    app = _run_app()

    _selectbox(app, "Enhet för Laddning").select("µC").run()
    assert not app.exception, [exception.value for exception in app.exception]
    charge_input = _number_input(app, "Laddning")
    assert charge_input.value == pytest.approx(0.03)

    charge_input.set_value(0.05).run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert any("ännu inte har ritats" in caption.value for caption in app.caption)

    _button(app, "Uppdatera figurer").click().run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert _number_input(app, "Laddning").value == pytest.approx(0.05)

    _button(app, "Återställ").click().run()
    assert not app.exception, [exception.value for exception in app.exception]
    assert _selectbox(app, "Enhet för Laddning").value == "nC"
    assert _number_input(app, "Laddning").value == pytest.approx(30.0)


def test_theory_page_runs_without_streamlit_exception():
    app = _run_app()
    content_selector = next(widget for widget in app.radio if widget.label == "Innehåll")
    content_selector.set_value("Teori").run()
    assert not app.exception, [exception.value for exception in app.exception]
