"""Scoring rules for Letter Vocabulary Master."""

from __future__ import annotations

from dataclasses import dataclass

BASE_POINTS = {"easy": 10, "medium": 20, "hard": 30}
BONUS_PER_REMAINING_ATTEMPT = 5


@dataclass(frozen=True)
class ScoreBreakdown:
    base: int
    bonus: int

    @property
    def total(self) -> int:
        return self.base + self.bonus


def compute_score(difficulty: str, attempts_left: int) -> ScoreBreakdown:
    """Compute the points earned for completing a word.

    ``attempts_left`` is the number of wrong guesses still available
    when the word was completed; it is rewarded as a bonus.
    """
    return ScoreBreakdown(
        base=BASE_POINTS[difficulty],
        bonus=attempts_left * BONUS_PER_REMAINING_ATTEMPT,
    )
