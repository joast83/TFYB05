from em_visualisering.guidance import GUIDANCE_BY_CLASS
from em_visualisering.study_content import (
    CHAPTER_METHOD_KEYS,
    METHOD_BY_ID,
    PROBLEM_STATEMENTS,
    method_options_for_problem,
    problem_id_from_name,
)
from em_visualisering.registry import PROBLEMS


def test_every_registered_problem_has_student_facing_statement_and_method():
    assert len(PROBLEMS) == 65
    for problem in PROBLEMS:
        pid = problem_id_from_name(problem.name)
        assert pid in PROBLEM_STATEMENTS
        assert len(PROBLEM_STATEMENTS[pid].strip()) >= 20
        assert pid in METHOD_BY_ID


def test_every_guided_problem_has_matching_registered_problem():
    registered_classes = {problem.__class__.__name__ for problem in PROBLEMS}
    assert set(GUIDANCE_BY_CLASS) == registered_classes


def test_recommended_method_is_always_offered_in_method_choice():
    for problem in PROBLEMS:
        pid = problem_id_from_name(problem.name)
        assert METHOD_BY_ID[pid] in method_options_for_problem(problem)


def test_chapter_method_options_cover_registered_chapters():
    registered_chapters = {int(problem_id_from_name(p.name).split(".", 1)[0]) for p in PROBLEMS}
    assert registered_chapters <= set(CHAPTER_METHOD_KEYS)
