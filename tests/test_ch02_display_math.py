"""The displayed math in chapter 2 must be *block equations*, not inline formulas.

These tests protect the visual layout of student hints and the general pedagogy
of keeping equations in the hint where they were originally introduced.
"""

from em_visualisering.guidance import GUIDANCE_BY_CLASS


def _chapter_two_guides():
    return {
        guide.problem_id: guide
        for guide in GUIDANCE_BY_CLASS.values()
        if guide.problem_id.startswith("2.")
    }


def test_every_chapter_two_exercise_has_at_least_one_display_equation():
    guides = _chapter_two_guides()
    assert len(guides) == 16
    for pid, guide in guides.items():
        assert any("\n$$\n" in hint for hint in guide.hints), pid
        for hint in guide.hints:
            assert hint.count("$$") % 2 == 0, (pid, hint)
            assert "\n$\n" not in hint, (pid, hint)


def test_continuous_charge_exercises_have_display_math_at_each_step():
    guides = _chapter_two_guides()
    for pid in ("2.2", "2.3", "2.4", "2.5"):
        assert all("\n$$\n" in hint for hint in guides[pid].hints), pid
    half_disk = guides["2.4"]
    assert half_disk.hints[0].count("$$") == 4
    assert half_disk.hints[1].count("$$") == 4
    assert half_disk.hints[2].count("$$") == 2
    assert r"\overline r-\overline r^{\prime}" in half_disk.hints[1]
    assert r"\sqrt{R^2+z^2}" in half_disk.hints[1]
