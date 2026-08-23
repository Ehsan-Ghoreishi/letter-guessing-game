from src.scoreboard import MAX_ENTRIES, Scoreboard


def make_scoreboard(tmp_path):
    return Scoreboard(path=str(tmp_path / "scores.json"))


def test_empty_scoreboard_always_qualifies(tmp_path):
    board = make_scoreboard(tmp_path)
    assert board.qualifies(0) is True


def test_add_persists_and_reloads(tmp_path):
    board = make_scoreboard(tmp_path)
    board.add("Ehsan", 100, "hard")

    reloaded = Scoreboard(path=board.path)
    assert len(reloaded.entries) == 1
    assert reloaded.entries[0].name == "Ehsan"
    assert reloaded.entries[0].score == 100


def test_keeps_only_top_entries_sorted_descending(tmp_path):
    board = make_scoreboard(tmp_path)
    for i in range(MAX_ENTRIES + 5):
        board.add(f"player{i}", i, "easy")

    assert len(board.entries) == MAX_ENTRIES
    scores = [entry.score for entry in board.entries]
    assert scores == sorted(scores, reverse=True)


def test_qualifies_false_when_board_full_and_score_too_low(tmp_path):
    board = make_scoreboard(tmp_path)
    for i in range(MAX_ENTRIES):
        board.add(f"player{i}", score=10 + i, difficulty="easy")

    assert board.qualifies(5) is False
    assert board.qualifies(100) is True
