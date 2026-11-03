"""Display-math consistency for every exercise in the student guide.

Keep important equations readable as their own Markdown math blocks while
leaving the actual solution steps and physics to each exercise's guidance.
"""

import re

from em_visualisering.guidance import GUIDANCE_BY_CLASS


DISPLAY = re.compile(r"(?m)^\$\$\n([\s\S]*?)\n\$\$$")


def test_every_registered_exercise_has_standalone_math():
    guides = list(GUIDANCE_BY_CLASS.values())
    assert len(guides) == 65
    assert {int(g.problem_id.split(".")[0]) for g in guides} == set(range(2, 11))

    for guide in guides:
        assert any(DISPLAY.search(hint) for hint in guide.hints), guide.problem_id


def test_math_blocks_are_balanced_and_the_formulas_are_well_delimited():
    for guide in GUIDANCE_BY_CLASS.values():
        for hint in guide.hints:
            blocks = DISPLAY.findall(hint)
            assert hint.count("$$") == 2 * len(blocks), guide.problem_id

            for expression in blocks:
                depth = 0
                for char in expression:
                    if char == "{":
                        depth += 1
                    elif char == "}":
                        depth -= 1
                    assert depth >= 0, (guide.problem_id, expression)
                assert depth == 0, (guide.problem_id, expression)

                opening = re.findall(r"\\begin\{([^}]+)\}", expression)
                closing = re.findall(r"\\end\{([^}]+)\}", expression)
                assert opening == closing, (guide.problem_id, expression)


def test_continuous_charge_method_in_chapter_2_is_preserved():
    by_id = {g.problem_id: g for g in GUIDANCE_BY_CLASS.values()}
    for problem_id in ("2.2", "2.3", "2.4", "2.5"):
        assert all(DISPLAY.search(h) for h in by_id[problem_id].hints)
    assert r"\sqrt{R^2+z^2}" in by_id["2.4"].hints[1]


def test_unrevised_chapter_ten_also_uses_display_math():
    by_id = {g.problem_id: g for g in GUIDANCE_BY_CLASS.values()}
    for problem_id in ("10.2", "10.3"):
        assert all(DISPLAY.search(h) for h in (by_id[problem_id].hints[0], by_id[problem_id].hints[-1]))
