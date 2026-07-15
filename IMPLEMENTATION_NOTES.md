# Parameter and reliability improvements

This change set introduces the first reliability-focused improvement package without
requiring an immediate rewrite of every problem definition.

## What changed

- Legacy `(key, label, default_si)` parameter tuples remain supported.
- New problems can use `ParameterSpec` for explicit units, bounds, increments,
  controls, and help text.
- Generic finite-value and bound validation is combined with each problem's existing
  `validate()` implementation.
- Streamlit parameter editing uses a form, avoiding expensive plot regeneration on
  every input change.
- Streamlit can render all views or only one selected view and supports three
  Matplotlib quality levels.
- Tkinter and Streamlit now use the same parameter metadata and validation pipeline.
- Pytest contract and rendering tests cover every registered problem and mode.
- GitHub Actions runs compilation and tests on Python 3.10, 3.11, and 3.12.
- `.gitignore` and `pyproject.toml` establish basic repository hygiene and packaging.

## Defining a new structured parameter

```python
from ..core import ParameterSpec, ProblemBase


class ExampleProblem(ProblemBase):
    parameters = [
        ParameterSpec(
            key="Q",
            label="Laddning Q [C]",
            default_si=30e-9,
            minimum_si=0.0,
            maximum_si=1e-6,
            step_si=1e-9,
            control="slider",
            help_text="Total fri laddning på kroppen.",
        ),
        # Legacy tuples can remain alongside structured parameters.
        ("a", "Radie a [m]", 0.1),
    ]
```

Supported control values are `number`, `slider`, and `log`. Sliders require explicit
minimum and maximum values; otherwise the interfaces safely fall back to a numerical
input.

## Applying the files

Extract the replacement archive at the repository root and overwrite existing files.
Then run:

```bash
python -m pip install -r requirements.txt
python -m pip install "pytest>=8,<10"
python -m pytest -q
streamlit run streamlit_app.py
```

The automated suite contains 499 tests in the supplied repository snapshot.
