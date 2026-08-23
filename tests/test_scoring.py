import pytest

from src.scoring import BASE_POINTS, BONUS_PER_REMAINING_ATTEMPT, compute_score


@pytest.mark.parametrize("difficulty,points", BASE_POINTS.items())
def test_base_points_by_difficulty(difficulty, points):
    breakdown = compute_score(difficulty, attempts_left=0)
    assert breakdown.base == points
    assert breakdown.bonus == 0
    assert breakdown.total == points


def test_bonus_scales_with_remaining_attempts():
    breakdown = compute_score("easy", attempts_left=4)
    assert breakdown.bonus == 4 * BONUS_PER_REMAINING_ATTEMPT
    assert breakdown.total == breakdown.base + breakdown.bonus
