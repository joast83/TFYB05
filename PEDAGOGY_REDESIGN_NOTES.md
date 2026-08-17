# TFYB05 pedagogy redesign – implementation of ideas 1–8

Copy the contents of this folder directly into the root of the TFYB05 repository.

Files:
- `streamlit_app.py` — replacement student interface.
- `em_visualisering/study_content.py` — problem statements plus method/mathematics metadata.
- `tests/test_streamlit_app.py` — replacement Streamlit UI tests for the new workflow.
- `tests/test_study_content.py` — coverage tests for the 65 registered exercises.
- `em_visualisering/guidance.py` — included unchanged from the all-65 hint version for convenience.

Implemented redesign ideas:

1. **Solve is the default mode.** Parameter controls, rendering quality and graph controls are absent.
2. **Actual problem text is shown.** Statements are transcribed from the supplied problem collection rather than using visualization-oriented `description` fields.
3. **Physics and mathematics are separated.** Each exercise shows its physics concepts and the mathematical move being trained.
4. **Help can be requested by type.** Students can say whether they are stuck on method choice, setup, vector/geometry reasoning, or checking.
5. **Self-checks require an active prediction first.** The authored check is gated until the student writes their own expectation.
6. **Explore requires a prediction before revealing figures.**
7. **Visualizations are pruned.** Only exercises whose authored guidance says a figure is useful are recommended for visualization. Other legacy plots require an explicit override, and 3-D is advanced/optional.
8. **Answer checking is separate from exploration.** A student must mark that they have a completed attempt before revealing the app's analytical/numerical control result.

The new sidebar is intentionally small in Solve mode: work mode, chapter and problem.

Notes:
- The problem statements come from the supplied 2024 problem collection. Figure-heavy exercises use the app's geometry sketch as a clean companion diagram.
- The answer section currently uses the repository's existing `result_summary()` and `physics_check()` functions. It is deliberately described as the app's control result rather than pretending to reproduce the printed facit verbatim.
- Existing plotting/problem implementation files are not changed by this package.
