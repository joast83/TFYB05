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


# Validate every student-facing help field, not merely one block per exercise.
# start_here is a legacy field: the optional first step uses starting_laws.py.
HELP_FIELDS = ("hints", "setup_hint", "geometry_hint", "self_checks", "common_pitfall")
MATH = re.compile(r"\$\$.*?\$\$|\$[^$\n]+\$", re.S)


def _help_texts():
    for guide in GUIDANCE_BY_CLASS.values():
        for field in HELP_FIELDS:
            values = getattr(guide, field)
            if isinstance(values, str):
                values = (values,)
            for index, value in enumerate(values):
                yield f"{guide.problem_id} {field}[{index}]", value


def test_formulas_in_all_help_fields_are_delimited_and_balanced():
    for location, text in _help_texts():
        prose = MATH.sub("", text)
        assert "$" not in prose, (location, "unmatched math delimiter")
        # Equals signs, calculus operators, inequalities and subscripts should
        # not leak into prose as compact Unicode/ASCII equations.
        assert not re.search(r"[=<>_∫∮∂∇√≤≥≠≈]", prose), (location, prose)
        assert not any(c in text for c in ("\a", "\b", "\f", "\t", "\v")), location
        for match in MATH.finditer(text):
            formula = match.group().strip("$")
            depth = 0
            for char in formula:
                depth += (char == "{") - (char == "}")
                assert depth >= 0, (location, formula)
            assert depth == 0, (location, formula)
            environments = []
            for action, name in re.findall(r"\\(begin|end)\{([^}]+)\}", formula):
                if action == "begin":
                    environments.append(name)
                else:
                    assert environments and environments.pop() == name, (location, formula)
            assert not environments, (location, formula)
            # A missing separator after \ell changes the control sequence.
            assert not re.search(r"\\ell[A-Za-z]", formula), (location, formula)


def test_source_integrals_are_displayed_in_hints_and_targeted_help():
    for guide in GUIDANCE_BY_CLASS.values():
        for text in (*guide.hints, guide.setup_hint):
            for match in MATH.finditer(text):
                if re.search(r"\\(?:int|oint)\b", match.group()):
                    assert match.group().startswith("$$"), guide.problem_id


def test_2_8_shows_the_charge_regions_and_potential_segments_separately():
    guide = GUIDANCE_BY_CLASS["ConcentricSphericalShells"]
    assert r"\begin{cases}" in guide.hints[0]
    assert all(region in guide.hints[0] for region in ("r<a", "a<r<b", "r>b"))
    assert r"\int_r^b" in guide.hints[1]
    assert r"\int_b^\infty" in guide.hints[1]
    assert "integrationsvariabeln" in guide.hints[1]


def test_resistivity_times_length_is_not_line_charge_density():
    guide = next(
        g for g in GUIDANCE_BY_CLASS.values() if g.problem_id == "5.2"
    )
    assert r"\rho\ell/A" in guide.common_pitfall
    assert r"\rho_\ell" not in guide.common_pitfall
