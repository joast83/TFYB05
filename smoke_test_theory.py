"""Smoke test for theory pages.

Avoids importing Streamlit and validates that the Plotly figure builders and
numerical theorem checks can run in a deployment environment.
"""

import sys

sys.path.insert(0, ".")

from em_visualisering.theory_pages import (
    THEORY_PAGES,
    _gauss_figure,
    _stokes_magnetostatic_figure,
)

assert len(THEORY_PAGES) >= 2

fig, report = _gauss_figure(
    radius=1.1,
    q_nc=5.0,
    position_ratio=0.45,
    surface_kind="Sluten sfär",
    show_field_arrows=True,
    show_position_axis=True,
)
assert len(fig.data) >= 3
assert report["status"] == "ok"
assert "innanför" in report["position_text"]

fig2, report2 = _gauss_figure(
    radius=1.1,
    q_nc=5.0,
    position_ratio=1.35,
    surface_kind="Sluten sfär",
    show_field_arrows=False,
    show_position_axis=True,
)
assert len(fig2.data) >= 3
assert report2["status"] == "ok"
assert "utanför" in report2["position_text"]
assert report2["q_enclosed_text"].startswith("0")

fig3, report3 = _gauss_figure(
    radius=1.1,
    q_nc=5.0,
    position_ratio=1.0,
    surface_kind="Sluten sfär",
    show_field_arrows=False,
    show_position_axis=False,
)
assert report3["status"] == "error"

fig4, report4 = _gauss_figure(
    radius=1.1,
    q_nc=5.0,
    position_ratio=0.45,
    surface_kind="Öppen hemisfär utan lock",
    show_field_arrows=False,
    show_position_axis=False,
)
assert report4["validity_short"] == "Nej"

fig5, report5 = _stokes_magnetostatic_figure(
    case="Stationär ström: hela strömtuben omsluts",
    current=2.0,
    loop_radius=1.2,
    conductor_radius=0.25,
    show_h_arrows=True,
    show_surface_current=True,
)
assert len(fig5.data) >= 4
assert report5["validity_short"] == "Ja"

fig6, report6 = _stokes_magnetostatic_figure(
    case="Inte magnetostatik: laddande kondensator",
    current=2.0,
    loop_radius=1.2,
    conductor_radius=0.25,
    show_h_arrows=True,
    show_surface_current=True,
)
assert len(fig6.data) >= 4
assert report6["validity_short"] == "Nej"

print("theory pages ok", len(THEORY_PAGES), len(fig.data), len(fig2.data), len(fig3.data), len(fig4.data), len(fig5.data), len(fig6.data))
