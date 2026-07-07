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
    radius=1.1,
    q_nc=5.0,
    position_ratio=0.25,
    surface_kind="Sluten sfär",
    show_field_arrows=True,
    show_position_axis=True,
)
assert len(fig.data) >= 2
assert report["status"] == "ok"

fig2, report2 = _gauss_figure(
    radius=1.1,
    q_nc=5.0,
    position_ratio=0.25,
    surface_kind="Öppen hemisfär utan lock",
    show_field_arrows=False,
    show_position_axis=True,
)
assert len(fig2.data) >= 2
assert report2["status"] == "warning"

fig3, report3 = _gauss_figure(
    radius=1.1,
    q_nc=5.0,
    position_ratio=1.0,
    surface_kind="Sluten sfär",
    show_field_arrows=False,
    show_position_axis=True,
)
assert len(fig3.data) >= 2
assert report3["status"] == "error"

fig4, report4 = _stokes_magnetostatic_slider_figure(
    current=2.0,
    loop_radius=1.2,
    conductor_radius=0.25,
    center_ratio=0.0,
    show_h_arrows=True,
    show_surface_current=True,
)
assert len(fig4.data) >= 5
assert report4["case_label"] == "helt innanför"

fig5, report5 = _stokes_magnetostatic_slider_figure(
    current=2.0,
    loop_radius=1.2,
    conductor_radius=0.25,
    center_ratio=1.0,
    show_h_arrows=True,
    show_surface_current=True,
)
assert len(fig5.data) >= 5
assert report5["case_label"] == "delvis genomskuren"

fig6, report6 = _stokes_magnetostatic_slider_figure(
    current=2.0,
    loop_radius=1.2,
    conductor_radius=0.25,
    center_ratio=1.8,
    show_h_arrows=True,
    show_surface_current=True,
)
assert len(fig6.data) >= 4
assert report6["case_label"] == "helt utanför"

fig7, report7 = _charging_capacitor_figure(
    current=2.0,
    loop_radius=1.2,
)
assert len(fig7.data) >= 4
assert report7["case_label"] == "ej magnetostatik"

print(
    "theory pages ok",
    len(THEORY_PAGES),
    len(fig.data),
    len(fig2.data),
    len(fig3.data),
    len(fig4.data),
    len(fig5.data),
    len(fig6.data),
    len(fig7.data),
)
