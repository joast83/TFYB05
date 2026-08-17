"""Grundtester för den progressiva lösningsvägledningen."""

from em_visualisering.guidance import GUIDANCE_BY_CLASS
from em_visualisering.registry import PROBLEMS


EXPECTED_CHAPTER_2_AND_3_CLASSES = {
    problem.__class__.__name__
    for problem in PROBLEMS
    if problem.name.split(maxsplit=1)[0].split(".", 1)[0] in {"2", "3"}
}


def test_all_registered_chapter_2_and_3_problems_have_guidance():
    assert EXPECTED_CHAPTER_2_AND_3_CLASSES <= set(GUIDANCE_BY_CLASS)


def test_guidance_entries_have_progressive_structure():
    for class_name, guidance in GUIDANCE_BY_CLASS.items():
        assert guidance.problem_id
        assert guidance.learning_goal
        assert guidance.concepts, class_name
        assert guidance.start_here, class_name
        assert len(guidance.hints) >= 3, class_name
        assert len(guidance.self_checks) >= 2, class_name
        assert all(text.strip() for text in guidance.hints), class_name
        assert all(text.strip() for text in guidance.self_checks), class_name
