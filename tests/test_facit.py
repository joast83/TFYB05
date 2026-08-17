from em_visualisering.facit import FACIT_BY_ID, facit_for_problem
from em_visualisering.registry import PROBLEMS
from em_visualisering.study_content import problem_id_from_name


def test_every_registered_problem_has_real_facit():
    registered_ids = [problem_id_from_name(problem.name) for problem in PROBLEMS]
    assert len(registered_ids) == 65
    assert len(set(registered_ids)) == 65
    assert set(registered_ids) == set(FACIT_BY_ID)
    for problem in PROBLEMS:
        answer = facit_for_problem(problem)
        assert answer is not None
        assert answer.strip()
