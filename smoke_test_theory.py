"""Smoke test for the added theory pages.

This script intentionally avoids importing Streamlit. It validates that the
new theory-page helper module loads, and that both interactive Plotly figures
can be built numerically without errors.
"""

import sys

sys.path.insert(0, ".")

from em_visualisering.theory_pages import THEORY_PAGES, _gauss_figure, _stokes_figure


assert len(THEORY_PAGES) >= 2

gauss_fig = _gauss_figure("Sfär", 1.2, 5.0, 2.0, 2.6, False)
assert len(gauss_fig.data) >= 2

stokes_fig, circulation, curl_flux, _ = _stokes_figure(
    "Roterande fält F = (-ωy, ωx, 0)", 1.0, 1.1, 25, True, True
)
assert len(stokes_fig.data) >= 3
assert abs(circulation - curl_flux) < 1e-10

stokes_fig2, circulation2, curl_flux2, _ = _stokes_figure(
    "Virvelfritt gradientfält F = (x, y, 0)", 1.0, 1.1, 25, True, True
)
assert len(stokes_fig2.data) >= 2
assert circulation2 == 0.0
assert curl_flux2 == 0.0

print("theory pages ok", len(THEORY_PAGES), len(gauss_fig.data), len(stokes_fig.data), len(stokes_fig2.data))
