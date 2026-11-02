"""Regression checks for the manually audited original-source corrections."""

from em_visualisering.facit import FACIT_BY_ID
from em_visualisering.study_content import (
    CHAPTER_METHOD_KEYS, METHOD_BY_ID, METHOD_META, PROBLEM_STATEMENTS,
)

REVIEWED = {
    2: (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 18, 19),
    3: (1, 3, 6, 7, 9, 11, 12, 13, 14, 18, 19),
    4: (1, 2, 3, 5, 6, 7),
    5: (1, 2, 7, 10, 15),
    6: (1, 2, 3, 5, 8, 13),
    7: (1, 2, 3, 5, 6, 7, 10),
    8: (1, 2, 4, 5, 6, 12, 13),
    9: (2, 4, 6, 13, 14),
}


def test_all_63_reviewed_exercises_have_statements_answers_and_methods():
    ids = {f"{ch}.{n}" for ch, nums in REVIEWED.items() for n in nums}
    assert len(ids) == 63
    assert ids <= set(PROBLEM_STATEMENTS)
    assert ids <= set(FACIT_BY_ID)
    assert ids <= set(METHOD_BY_ID)
    for pid in ids:
        key = METHOD_BY_ID[pid]
        assert key in METHOD_META
        assert key in CHAPTER_METHOD_KEYS[int(pid.split(".")[0])]


def test_method_names_are_physical_and_consistent():
    labels = [meta.label for meta in METHOD_META.values()]
    assert len(labels) == len(set(labels))
    assert all("Biot–Coulomb" not in name for name in labels)
    assert METHOD_META["direct_field_integral"].label.startswith("Coulombs lag")
    assert METHOD_META["biot_savart"].label == "Biot–Savarts lag"
    assert METHOD_BY_ID["7.5"] == "dipole_approximation"
    assert "gauss" not in CHAPTER_METHOD_KEYS[6]
    assert "ampere_magnetostatics" in CHAPTER_METHOD_KEYS[6]
    assert "vector_potential" in CHAPTER_METHOD_KEYS[6]


def test_original_8_1_table_and_question_are_complete():
    q = PROBLEM_STATEMENTS["8.1"]
    for token in ("0,00", "0,60", "0,83", "1,00", "1,20",
                  "−5000", "−4000", "−3000", "−2000",
                  "20 cm", "1 mm", "100 varv", "2,0 A"):
        assert token in q


def test_corrupted_transcriptions_have_been_restored():
    assert "magnetiska fältstyrkan" in PROBLEM_STATEMENTS["8.5"]
    assert "magnetiska ϕ̂ egenskaper" not in PROBLEM_STATEMENTS["8.13"]
    assert "sidan d/√2" in PROBLEM_STATEMENTS["9.2"]
    q = PROBLEM_STATEMENTS["9.13"]
    assert all(x in q for x in ("a = 10 cm", "ℓ = 30 cm", "Se figur"))


def test_source_answer_conflicts_are_not_silently_hidden():
    assert "Teckenkonvention" in FACIT_BY_ID["6.2"]
    assert "tryckta facit" in FACIT_BY_ID["7.5"]
    assert "12.258" in FACIT_BY_ID["7.5"]
