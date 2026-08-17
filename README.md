# TFYB05 guidance update — all registered problems

If you already installed the first hint-first prototype, copy this folder's contents into the root of the repository and replace the two existing files when prompted.

This update replaces:

- `em_visualisering/guidance.py`
- `tests/test_guidance.py`

It keeps the chapter 2–3 guidance from the first version and adds progressive guidance for every remaining currently registered exercise in chapters 4–10. The catalogue now contains all 65 registered exercises.

Run:

```bash
python -m pytest -q tests/test_guidance.py
streamlit run streamlit_app.py
```
