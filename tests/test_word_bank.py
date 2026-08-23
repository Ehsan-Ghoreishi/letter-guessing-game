from src.word_bank import DIFFICULTIES, WORD_BANK, get_random_word


def test_all_difficulties_present():
    assert set(WORD_BANK.keys()) == set(DIFFICULTIES)


def test_each_difficulty_has_ten_words():
    for difficulty in DIFFICULTIES:
        assert len(WORD_BANK[difficulty]) == 10


def test_words_have_complete_data():
    for words in WORD_BANK.values():
        for word in words:
            assert word.text.isalpha()
            assert word.meaning
            assert word.ipa
            assert word.sentence


def test_get_random_word_returns_word_from_requested_difficulty():
    word = get_random_word("easy")
    assert word in WORD_BANK["easy"]
