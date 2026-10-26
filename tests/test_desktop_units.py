"""Exercise desktop unit changes without requiring a display server."""
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

pytest.importorskip("tkinter")
from em_visualisering.app import ElectrostaticsApp
from em_visualisering.parameters import ParameterSpec
from em_visualisering.unit_scaling import display_scale_by_unit


class Value:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


def controller(value="20", unit="m"):
    spec = ParameterSpec("r", "Radie [m]", 0.2, control="slider",
                         ui_minimum_si=0.01, ui_maximum_si=1.0, step_si=0.01)
    return SimpleNamespace(
        param_specs={"r": spec},
        param_scales={"r": display_scale_by_unit(spec.label, "cm")},
        param_vars={"r": Value(value)},
        param_unit_vars={"r": Value(unit)},
        param_widgets={"r": Mock()},
    )


def test_unit_change_converts_value_bounds_and_increment():
    app = controller()
    ElectrostaticsApp._change_parameter_unit(app, "r")
    assert float(app.param_vars["r"].get()) == pytest.approx(0.2)
    assert app.param_scales["r"].display_unit == "m"
    assert app.param_widgets["r"].configure.call_args.kwargs == {
        "from_": 0.01, "to": 1.0, "increment": 0.01,
    }
    app.param_unit_vars["r"].set("mm")
    ElectrostaticsApp._change_parameter_unit(app, "r")
    assert float(app.param_vars["r"].get()) == pytest.approx(200.0)
    assert app.param_widgets["r"].configure.call_args.kwargs == {
        "from_": 10.0, "to": 1000.0, "increment": 10.0,
    }


def test_failed_unit_change_restores_label_and_preserves_input(monkeypatch):
    showerror = Mock()
    monkeypatch.setattr("em_visualisering.app.messagebox.showerror", showerror)
    app = controller(value="unfinished input")
    ElectrostaticsApp._change_parameter_unit(app, "r")
    assert app.param_unit_vars["r"].get() == "cm"
    assert app.param_scales["r"].display_unit == "cm"
    assert app.param_vars["r"].get() == "unfinished input"
    app.param_widgets["r"].configure.assert_not_called()
    showerror.assert_called_once()
