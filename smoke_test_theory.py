"""Build and validate all current theory figures without starting Streamlit.

Run from the repository root: python smoke_test_theory.py
"""

from em_visualisering.theory_pages import (
    GAUSS_DEFAULT_CHARGES,
    _ampere_figure,
    _biot_savart_figures,
    _biot_savart_section,
    _dielectric_boundary_fields,
    _dielectric_figure,
    _faraday_figures,
    _faraday_state,
    _gauss_cross_section_figure,
    _potential_figures,
)

figures = [
    _gauss_cross_section_figure(1.0, GAUSS_DEFAULT_CHARGES, False, show_grid=True),
    _ampere_figure(1.0, 0.0, 0.15, 1, 2.0),
    *_potential_figures(2.0, -2.0, 1.0),
    _dielectric_figure(*_dielectric_boundary_fields(2.0, 5.0, 4.0, 35, 0.0), 2.0, 5.0),
    _biot_savart_section(3.0, 0.75, 0.5),
    *_biot_savart_figures(3.0, 0.75, 0.5),
    *_faraday_figures(0.020, 4.5, 450, 0.045, 0.1, 0.0,
                     _faraday_state(0.020, 4.5, 450, 0.045, 0.1 / 4.5)[2]),
]
for figure in figures:
    assert figure.data
    figure.to_json(validate=True)
print(f"Validated {len(figures)} theory figures with Plotly.")
