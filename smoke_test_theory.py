"""Smoke test for theory pages.

Avoids importing Streamlit and validates that the Plotly figure builders and
numerical theorem checks can run in a deployment environment.
"""

import sys

sys.path.insert(0, ".")

from em_visualisering.theory_pages import (
    THEORY_PAGES,
    _gauss_figure,
    _stokes_magnetostatic_slider_figure,
    _charging_capacitor_figure,
)

assert len(THEORY_PAGES) >= 2

fig, report = _gauss_figure(
    case="Sluten yta: laddning innanför",
    radius=1.1,
    q_inside_nc=5.0,
    q_outside_nc=0.0,
    offset_fraction=0.25,
    show_field_arrows=True,
)
assert len(fig.data) >= 2
assert report["validity_short"] == "Ja"

fig2, report2 = _gauss_figure(
    case="Öppen yta: hemisfär utan lock",
    radius=1.1,
    q_inside_nc=5.0,
    q_outside_nc=0.0,
    offset_fraction=0.0,
    show_field_arrows=False,
)
assert len(fig2.data) >= 2
assert report2["validity_short"] == "Nej"

fig3, report3 = _stokes_magnetostatic_slider_figure(
    current=2.0,
    loop_radius=1.2,
    conductor_radius=0.25,
    center_ratio=0.0,
    show_h_arrows=True,
    show_surface_current=True,
)
assert len(fig3.data) >= 5
assert report3["case_label"] == "helt innanför"

fig4, report4 = _stokes_magnetostatic_slider_figure(
    current=2.0,
    loop_radius=1.2,
    conductor_radius=0.25,
    center_ratio=1.6,
    show_h_arrows=True,
    show_surface_current=True,
)
assert len(fig4.data) >= 4
assert report4["case_label"] == "helt utanför"

fig5, report5 = _charging_capacitor_figure(
    current=2.0,
    loop_radius=1.2,
)
assert len(fig5.data) >= 4
assert report5["case_label"] == "ej magnetostatik"

print("theory pages ok", len(THEORY_PAGES), len(fig.data), len(fig2.data), len(fig3.data), len(fig4.data), len(fig5.data))
