"""Checks for chapter 2 mathematical typesetting.

Presentation regression tests; they do not validate the physical derivations.
"""

import re

from em_visualisering.guidance import GUIDANCE_BY_CLASS


def _chapter_two_guides():
    return (g for g in GUIDANCE_BY_CLASS.values() if g.problem_id.startswith("2."))


def test_all_chapter_two_hints_and_setups_include_formatted_math():
    guides = list(_chapter_two_guides())
    assert len(guides) == 16
    for guide in guides:
        assert "$" in guide.setup_hint, guide.problem_id
        assert all("$" in hint for hint in guide.hints), guide.problem_id


def test_chapter_two_latex_delimiters_and_braces_are_balanced():
    for guide in _chapter_two_guides():
        fields = [guide.start_here, guide.setup_hint, guide.geometry_hint,
                  guide.common_pitfall, *guide.hints, *guide.self_checks]
        for text in fields:
            assert text.count("$") % 2 == 0, (guide.problem_id, text)
            for formula in re.findall(r"\$([^$]+)\$", text):
                assert "\f" not in formula and "\t" not in formula, (guide.problem_id, formula)
                depth = 0
                for char in formula:
                    if char == "{":
                        depth += 1
                    elif char == "}":
                        depth -= 1
                    assert depth >= 0, (guide.problem_id, formula)
                assert depth == 0, (guide.problem_id, formula)


def test_continuous_charge_hints_keep_the_problem_booklets_notation():
    by_id = {g.problem_id: g for g in _chapter_two_guides()}
    for pid in ("2.2", "2.3", "2.4"):
        assert r"\overline E(\overline r)" in by_id[pid].start_here
        assert r"\mathrm dQ^{\prime}" in by_id[pid].start_here
    assert r"\frac{\mathrm dQ^{\prime}}" in by_id["2.5"].start_here
    assert r"\rho_\ell" in by_id["2.2"].hints[0]
    assert r"\rho_s" in by_id["2.4"].hints[0]
    assert r"\int_0^d" in by_id["2.19"].start_here
