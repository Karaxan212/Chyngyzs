import pytest

from student import get_result


@pytest.mark.parametrize(
    ("score", "attendance", "expected"),
    [
        (90, 80, "Отлично"),
        (100, 100, "Отлично"),
        (70, 70, "Хорошо"),
        (89, 79, "Хорошо"),
        (50, 60, "Зачёт"),
        (69, 69, "Зачёт"),
        (0, 0, "Незачёт"),
        (49, 59, "Незачёт"),
    ],
)
def test_get_result_for_equivalence_classes(score, attendance, expected):
    assert get_result(score, attendance) == expected


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (-1, "Некорректный балл"),
        (0, "Незачёт"),
        (49, "Незачёт"),
        (50, "Зачёт"),
        (69, "Зачёт"),
        (70, "Хорошо"),
        (89, "Хорошо"),
        (90, "Отлично"),
        (100, "Отлично"),
        (101, "Некорректный балл"),
    ],
)
def test_score_boundary_values(score, expected):
    assert get_result(score, 100) == expected


@pytest.mark.parametrize(
    ("attendance", "expected"),
    [
        (-1, "Некорректная посещаемость"),
        (0, "Незачёт"),
        (59, "Незачёт"),
        (60, "Зачёт"),
        (69, "Зачёт"),
        (70, "Хорошо"),
        (79, "Хорошо"),
        (80, "Отлично"),
        (100, "Отлично"),
        (101, "Некорректная посещаемость"),
    ],
)
def test_attendance_boundary_values(attendance, expected):
    assert get_result(100, attendance) == expected


@pytest.mark.parametrize("score", ["90", None, [], {}, object()])
def test_invalid_score_type_raises_type_error(score):
    with pytest.raises(TypeError, match="Баллы должны быть числом"):
        get_result(score, 80)


@pytest.mark.parametrize("attendance", ["80", None, [], {}, object()])
def test_invalid_attendance_type_raises_type_error(attendance):
    with pytest.raises(TypeError, match="Посещаемость должна быть числом"):
        get_result(90, attendance)


@pytest.mark.parametrize("score", [-100, 100.1])
def test_invalid_score_returns_error_message(score):
    assert get_result(score, 80) == "Некорректный балл"


@pytest.mark.parametrize("attendance", [-100, 100.1])
def test_invalid_attendance_returns_error_message(attendance):
    assert get_result(90, attendance) == "Некорректная посещаемость"
