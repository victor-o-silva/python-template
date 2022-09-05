import pytest

from src.my_awesome_app.maths import get_semester


@pytest.mark.parametrize(
    "month_value, expected_semester",
    [
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (6, 1),
        (7, 2),
        (8, 2),
        (9, 2),
        (10, 2),
        (11, 2),
        (12, 2),
    ],
)
def test_get_semester(month_value: int, expected_semester: int):
    result = get_semester(month=month_value)
    assert result == expected_semester
