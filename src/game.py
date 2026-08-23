"""Game loop and session state for Letter Vocabulary Master."""

from __future__ import annotations

import sys
import time
from datetime import datetime

from . import ui
from .scoreboard import Scoreboard
from .scoring import compute_score
from .word_bank import get_random_word

MAX_ATTEMPTS = 6
ROUNDS_PER_GAME = 10


class GameSession:
    """Tracks state for a single play-through and drives round logic."""

    def __init__(self, difficulty: str, player_name: str):
        self.difficulty = difficulty
        self.player_name = player_name
        self.score = 0
        self.words_learned: list[str] = []
        self.total_attempts = 0
        self.correct_guesses = 0
        self.start_time = datetime.now()

    def play_round(self, round_num: int) -> None:
        """Play a single round, updating session state as it goes."""
        word = get_random_word(self.difficulty)
        target = word.text.upper()
        correct_letters: set[str] = set()
        wrong_letters: set[str] = set()
        attempts_left = MAX_ATTEMPTS

        ui.show_round_header(round_num, ROUNDS_PER_GAME, len(target))

        while attempts_left > 0:
            ui.show_round_state(attempts_left, target, correct_letters, wrong_letters)
            guess = ui.prompt_letter(correct_letters, wrong_letters)
            self.total_attempts += 1

            is_correct = guess in target
            ui.show_guess_result(guess, is_correct)

            if is_correct:
                correct_letters.add(guess)
                self.correct_guesses += 1
                if all(letter in correct_letters for letter in target):
                    breakdown = compute_score(self.difficulty, attempts_left)
                    self.score += breakdown.total
                    self.words_learned.append(word.text)
                    ui.show_word_completed(breakdown.base, breakdown.bonus)
                    ui.show_word_info(word)
                    return
            else:
                wrong_letters.add(guess)
                attempts_left -= 1

        ui.show_game_over(target)
        ui.show_word_info(word)

    def play(self, scoreboard: Scoreboard) -> None:
        """Run all rounds of the game and record a high score if earned."""
        ui.clear_screen()
        print("Get ready to play...")
        time.sleep(1)
        ui.show_countdown()

        for round_num in range(1, ROUNDS_PER_GAME + 1):
            self.play_round(round_num)
            if round_num < ROUNDS_PER_GAME:
                ui.press_enter_to_continue()
                ui.clear_screen()

        time_played = datetime.now() - self.start_time
        ui.show_final_stats(
            self.score, self.words_learned, time_played, self.correct_guesses, self.total_attempts
        )

        if scoreboard.qualifies(self.score):
            scoreboard.add(self.player_name, self.score, self.difficulty)
            ui.show_new_high_score()

        ui.press_enter_to_continue("Press Enter to return to menu...")


def run() -> None:
    """Run the main menu loop."""
    scoreboard = Scoreboard()
    while True:
        ui.show_main_menu()
        choice = input().strip()

        if choice == "1":
            difficulty = ui.prompt_difficulty()
            player_name = ui.prompt_player_name()
            session = GameSession(difficulty, player_name)
            session.play(scoreboard)
        elif choice == "2":
            ui.show_high_scores(scoreboard.entries)
        elif choice == "3":
            ui.show_instructions()
        elif choice == "4":
            ui.show_farewell()
            break
        else:
            ui.show_invalid_choice()


def main() -> None:
    """Entry point for the letter guessing vocabulary game."""
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
