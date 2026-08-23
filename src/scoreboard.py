"""Persistence for the local high score table."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime

HIGH_SCORE_FILE = "letter_game_scores.json"
MAX_ENTRIES = 10


@dataclass
class ScoreEntry:
    name: str
    score: int
    difficulty: str
    date: str


class Scoreboard:
    """Loads, ranks, and persists the top high scores."""

    def __init__(self, path: str = HIGH_SCORE_FILE):
        self.path = path
        self.entries: list[ScoreEntry] = self._load()

    def _load(self) -> list[ScoreEntry]:
        try:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                return [ScoreEntry(**entry) for entry in raw]
        except (OSError, json.JSONDecodeError, TypeError):
            pass
        return []

    def _save(self) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(
                    [asdict(entry) for entry in self.entries],
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
        except OSError:
            pass

    def qualifies(self, score: int) -> bool:
        """Whether a score would earn a spot on the table."""
        if len(self.entries) < MAX_ENTRIES:
            return True
        return score > self.entries[-1].score

    def add(self, name: str, score: int, difficulty: str) -> None:
        """Record a new score, keeping only the top entries."""
        entry = ScoreEntry(
            name=name,
            score=score,
            difficulty=difficulty,
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        self.entries.append(entry)
        self.entries.sort(key=lambda e: e.score, reverse=True)
        self.entries = self.entries[:MAX_ENTRIES]
        self._save()
