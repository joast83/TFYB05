"""Smoke-test the browser-interactive Plotly 3-D renderer.

Run with:
    python smoke_test_plotly.py
"""

from em_visualisering.modes import mode_options_for_problem, normalize_mode_for_problem
from em_visualisering.plotly_bridge import make_plotly_3d_figure
from em_visualisering.registry import PROBLEMS


def main() -> int:
    failures = []
    tested = 0
    for problem in PROBLEMS:
        params = problem.defaults()
        for _label, requested_mode in mode_options_for_problem(problem):
            mode = normalize_mode_for_problem(problem, requested_mode)
            tested += 1
            try:
                fig = make_plotly_3d_figure(problem, params, mode)
                payload = fig.to_plotly_json()
                if not payload.get("data"):
                    raise RuntimeError("Plotly figure contains no traces")
            except Exception as exc:  # pragma: no cover - diagnostic script
                failures.append((problem.__class__.__name__, mode, repr(exc)))

    print(f"plotly 3-D modes tested {tested} failures {len(failures)}")
    for failure in failures:
        print("FAIL", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
