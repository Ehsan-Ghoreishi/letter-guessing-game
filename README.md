# Letter Vocabulary Master

A terminal-based English vocabulary learning game with colorized UI. Guess letters one by one to reveal hidden English words — with Persian translations, IPA pronunciation, and example sentences included.

## Features

- **3 difficulty levels** — Easy, Medium, Hard
- **30+ vocabulary words** each with Persian meaning, IPA pronunciation, and an example sentence
- **Scoring system** — 10 / 20 / 30 points per difficulty level + bonus for remaining attempts
- **High score table** — saves top 10 scores to a local JSON file
- **Colorful terminal UI** — animated countdown, color-coded feedback
- **Full statistics** — accuracy, time played, words learned at the end of each game

## Requirements

- Python 3.8 or higher
- `colorama` library

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Ehsan-Ghoreishi/learning-portfolio.git
cd learning-portfolio/letter_guessing_game

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the game
python letter_guessing_game.py
```

## Gameplay

1. Choose a difficulty level (Easy / Medium / Hard)
2. Enter your name
3. Guess one letter at a time to reveal the hidden English word
4. You have **6 attempts** per word and play **10 rounds** per game
5. After each word, learn its meaning, pronunciation, and usage

## Color Guide

| Color | Meaning |
|-------|---------|
| Green | Correct letter — exists in the word |
| Red | Wrong letter — not in the word |
| Yellow | Already guessed letter |

## Scoring

| Difficulty | Base Points | Bonus |
|------------|-------------|-------|
| Easy | 10 | +5 per remaining attempt |
| Medium | 20 | +5 per remaining attempt |
| Hard | 30 | +5 per remaining attempt |

## Project Structure

```
letter_guessing_game/
├── letter_guessing_game.py     # Entry point — python letter_guessing_game.py
├── src/
│   ├── word_bank.py            # Vocabulary data (Word dataclass + WORD_BANK)
│   ├── scoring.py               # Point/bonus calculation rules
│   ├── scoreboard.py           # High score persistence (Scoreboard class)
│   ├── ui.py                   # All terminal rendering and input prompts
│   └── game.py                 # GameSession orchestration and main loop
├── tests/                      # Unit tests for word bank, scoring, scoreboard
├── requirements.txt
├── requirements-dev.txt        # Adds pytest for running the test suite
└── README.md
```

The game logic is split from terminal I/O so the scoring and persistence
rules can be unit tested without simulating keyboard input.

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

## License

This is an educational project. Feel free to use and modify it.
