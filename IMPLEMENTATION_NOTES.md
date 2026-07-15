# Parameter and interface improvements — Phase 2

Phase 2 builds on the reliability foundation from Phase 1. The numerical problem
implementations still receive and return SI values, while both interfaces now use a
shared metadata catalogue to select appropriate controls and display units.

## What changed

- All 276 editable parameters across 65 registered exercises are enriched with stable
  metadata in `em_visualisering/parameter_catalog.py`.
- Hard physical/model limits are separated from UI-only editing ranges. Moving beyond
  a suggested slider range therefore does not make an otherwise valid value illegal.
- Supported controls are `number`, `slider`, `log`, and `select`.
- Counts and winding numbers are edited as integers; the circular-arc geometry is a
  named discrete selector instead of the previous `1`/`2` numeric convention.
- Repeated concepts receive consistent profiles: geometry uses bounded controls,
  relative permittivity uses linear controls, relative permeability and other wide
  positive quantities use logarithmic controls, and signed coordinates remain exact
  numerical inputs.
- Streamlit and Tkinter expose explicit engineering-unit selectors. A unit change only
  changes presentation; the stored and calculated value remains in SI.
- Streamlit keeps draft parameters separate from the applied plot parameters. Editing
  controls no longer recomputes the figures until **Uppdatera figurer** is pressed.
- Unchanged Matplotlib and Plotly renders are cached. The Plotly camera is preserved
  across reruns with `uirevision`.
- Current parameters can be exported as JSON or CSV. Main and geometry views can be
  downloaded as PNG, and the interactive 3-D view as HTML.
- Unit declarations, metadata contracts, all registered problem defaults, and every
  Matplotlib/Plotly rendering mode are covered by automated tests.

## Structured parameter fields

```python
ParameterSpec(
    key="radius",
    label="Radie [m]",
    default_si=0.2,
    minimum_si=0.0,       # hard validation bound
    ui_minimum_si=0.01,   # suggested control range only
    ui_maximum_si=1.0,
    step_si=0.01,
    control="slider",
    display_units=("mm", "cm", "m"),
    help_text="Geometrisk radie.",
)
```

Discrete controls use `choices` and optional `choice_labels`:

```python
ParameterSpec(
    key="geometry",
    label="Geometri",
    default_si=1.0,
    control="select",
    choices=(1.0, 2.0),
    choice_labels=("Kvartsbåge", "Hel slinga"),
    integer=True,
)
```

Legacy `(key, label, default_si)` tuples remain supported. They are normalized and
then enriched through the central catalogue, allowing exercise modules to remain
compact while exact exceptions are maintained in one place.

## Verification

```bash
python -m compileall -q em_visualisering streamlit_app.py
python -m pytest -q
streamlit run streamlit_app.py
```

The supplied snapshot passes **634 tests**. The Streamlit default exercise was also
executed with `streamlit.testing.v1.AppTest`, and the Tkinter application was launched
headlessly with Xvfb.
