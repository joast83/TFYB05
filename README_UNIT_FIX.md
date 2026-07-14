# TFYB05 parameter unit fix

Extract this archive **at the root of the TFYB05 repository** and allow it to overwrite
`streamlit_app.py` and `em_visualisering/app.py`. The file
`em_visualisering/unit_scaling.py` is new.

## What changed

Problem definitions and physics calculations still use SI units internally. The web and
desktop interfaces now choose a practical display unit from each parameter's default
value, show the converted value, and convert user input back to SI before validation or
calculation.

Examples:

- `3e-8 C` is displayed and edited as `30 nC`.
- `0.15 m` is displayed and edited as `15 cm`.
- `2e8 V/m` is displayed and edited as `200 MV/m`.
- `2e-4 m²` is displayed and edited as `2 cm²`.
- `0.001 kg` is displayed and edited as `1 g`.

The selected display unit remains stable while the value is edited, so the input scale
does not jump between prefixes. Unsupported and dimensionless units remain unchanged.
The desktop interface also accepts either a decimal point or a decimal comma.

## Files

- `streamlit_app.py` — unit-aware Streamlit number inputs.
- `em_visualisering/app.py` — unit-aware Tkinter entries.
- `em_visualisering/unit_scaling.py` — display-unit selection and reversible conversion.
- `tests/test_unit_scaling.py` — checks example conversions and every problem default.

## Test

From the repository root:

```bash
python -m unittest discover -s tests -v
```
