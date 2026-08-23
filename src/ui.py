"""Terminal rendering and input prompts for Letter Vocabulary Master."""

from __future__ import annotations

import os
import sys
import time

try:
    from colorama import Fore, Style, init

    init()
except ImportError:
    print("Error: colorama is required. Install with: pip install colorama")
    sys.exit(1)

from .scoreboard import ScoreEntry
from .word_bank import DIFFICULTIES, Word


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def animate_text(text: str, delay: float = 0.03) -> None:
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def show_countdown(seconds: int = 3) -> None:
    for i in range(seconds, 0, -1):
        print(f"{Fore.YELLOW}{Style.BRIGHT}{i}{Style.RESET_ALL}", end="", flush=True)
        time.sleep(1)
        if i > 1:
            print("\r", end="", flush=True)
    print(f"\r{Fore.GREEN}GO!{Style.RESET_ALL}")
    time.sleep(0.5)


def show_main_menu() -> None:
    clear_screen()
    print(
        f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                📚 LETTER VOCABULARY MASTER 📚                ║
║              English Learning Game - Letter Mode             ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.GREEN}1. Start New Game{Style.RESET_ALL}
{Fore.YELLOW}2. View High Scores{Style.RESET_ALL}
{Fore.BLUE}3. Instructions{Style.RESET_ALL}
{Fore.RED}4. Exit{Style.RESET_ALL}

{Fore.CYAN}Choose an option (1-4): {Style.RESET_ALL}""",
        end="",
    )


def show_instructions() -> None:
    clear_screen()
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                      📖 HOW TO PLAY 📖                       ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.YELLOW}OBJECTIVE:{Style.RESET_ALL}
Guess the hidden English word one letter at a time!

{Fore.YELLOW}GAME FEATURES:{Style.RESET_ALL}
• 10 rounds per game
• 3 difficulty levels (Easy/Medium/Hard)
• 30+ vocabulary words with Persian meanings
• IPA pronunciation guides
• Example sentences for context

{Fore.YELLOW}HOW TO PLAY:{Style.RESET_ALL}
1. Choose one alphabet letter at a time
2. The game will tell you if the letter exists in the word
3. Continue guessing until you complete the word or run out of attempts
4. Learn the word's meaning, pronunciation, and usage

{Fore.YELLOW}COLOR CODES:{Style.RESET_ALL}
{Fore.GREEN}• Green{Style.RESET_ALL} = Correct letter (exists in word)
{Fore.RED}• Red{Style.RESET_ALL} = Wrong letter (not in word)
{Fore.YELLOW}• Yellow{Style.RESET_ALL} = Already guessed letter

{Fore.YELLOW}SCORING:{Style.RESET_ALL}
• Easy words: 10 points
• Medium words: 20 points
• Hard words: 30 points
• Bonus points for fewer attempts

{Fore.CYAN}Press Enter to return to menu...{Style.RESET_ALL}""")
    input()


def show_high_scores(entries: list[ScoreEntry]) -> None:
    clear_screen()
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                    🏆 HIGH SCORES 🏆                         ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

    if not entries:
        print(f"{Fore.YELLOW}No high scores yet. Be the first!{Style.RESET_ALL}")
    else:
        print(f"{'Rank':<6} {'Name':<15} {'Score':<8} {'Difficulty':<12} {'Date':<16}")
        print("-" * 60)
        for i, entry in enumerate(entries[:10], 1):
            print(
                f"{i:<6} {entry.name:<15} {entry.score:<8} "
                f"{entry.difficulty:<12} {entry.date:<16}"
            )

    print(f"\n{Fore.CYAN}Press Enter to return to menu...{Style.RESET_ALL}")
    input()


def prompt_difficulty() -> str:
    labels = {
        "easy": (Fore.GREEN, "Easy", "Simple words, 10 points each"),
        "medium": (Fore.YELLOW, "Medium", "Intermediate words, 20 points each"),
        "hard": (Fore.RED, "Hard", "Advanced words, 30 points each"),
    }
    while True:
        clear_screen()
        print(
            f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                    🎯 SELECT DIFFICULTY 🎯                    ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        )
        for i, difficulty in enumerate(DIFFICULTIES, 1):
            color, name, desc = labels[difficulty]
            print(f"{color}{i}. {name}{Style.RESET_ALL} ({desc})")

        choice = input(f"\n{Fore.CYAN}Choose difficulty (1-3): {Style.RESET_ALL}").strip()
        if choice in ("1", "2", "3"):
            return DIFFICULTIES[int(choice) - 1]
        print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        time.sleep(1)


def prompt_player_name() -> str:
    return input(f"{Fore.CYAN}Enter your name: {Style.RESET_ALL}").strip()


def render_word_state(word: str, correct_letters: set[str]) -> str:
    display = ""
    for letter in word:
        if letter in correct_letters:
            display += f"{Fore.GREEN}{letter.upper()}{Style.RESET_ALL} "
        else:
            display += "_ "
    return display.strip()


def show_guessed_letters(correct_letters: set[str], wrong_letters: set[str]) -> None:
    print(f"\n{Fore.CYAN}Letters Guessed:{Style.RESET_ALL}")
    if correct_letters:
        correct_display = " ".join(
            f"{Fore.GREEN}{letter}{Style.RESET_ALL}" for letter in sorted(correct_letters)
        )
        print(f"Correct: {correct_display}")
    if wrong_letters:
        wrong_display = " ".join(
            f"{Fore.RED}{letter}{Style.RESET_ALL}" for letter in sorted(wrong_letters)
        )
        print(f"Wrong: {wrong_display}")


def show_round_header(round_num: int, total_rounds: int, word_length: int) -> None:
    print(f"\n{Fore.CYAN}Round {round_num} of {total_rounds}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Word has {word_length} letters{Style.RESET_ALL}")


def show_round_state(attempts_left: int, word: str, correct_letters: set[str], wrong_letters: set[str]) -> None:
    print(f"\n{Fore.CYAN}Attempts left: {attempts_left}{Style.RESET_ALL}")
    print(f"Word: {render_word_state(word, correct_letters)}")
    show_guessed_letters(correct_letters, wrong_letters)


def prompt_letter(correct_letters: set[str], wrong_letters: set[str]) -> str:
    while True:
        guess = input(f"{Fore.GREEN}Enter a letter: {Style.RESET_ALL}").strip().upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in correct_letters or guess in wrong_letters:
                print(f"{Fore.YELLOW}You already guessed that letter!{Style.RESET_ALL}")
                continue
            return guess
        print(f"{Fore.RED}Please enter a single alphabet letter!{Style.RESET_ALL}")


def show_guess_result(letter: str, is_correct: bool) -> None:
    if is_correct:
        print(f"{Fore.GREEN}✓ CORRECT! The letter '{letter}' exists in the word.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ WRONG! The letter '{letter}' does not exist in the word.{Style.RESET_ALL}")


def show_word_completed(base: int, bonus: int) -> None:
    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 WORD COMPLETED! 🎉{Style.RESET_ALL}")
    print(f"{Fore.GREEN}You earned {base + bonus} points! ({base} + {bonus} bonus){Style.RESET_ALL}")


def show_game_over(word: str) -> None:
    print(f"\n{Fore.RED}{Style.BRIGHT}❌ GAME OVER ❌{Style.RESET_ALL}")
    print(f"{Fore.RED}The word was: {word}{Style.RESET_ALL}")


def show_word_info(word: Word) -> None:
    print(f"""
{Fore.CYAN}{Style.BRIGHT}═══ WORD INFORMATION ═══{Style.RESET_ALL}
{Fore.GREEN}Word:{Style.RESET_ALL} {word.text}
{Fore.YELLOW}Meaning:{Style.RESET_ALL} {word.meaning}
{Fore.BLUE}Pronunciation:{Style.RESET_ALL} {word.ipa}
{Fore.MAGENTA}Example:{Style.RESET_ALL} {word.sentence}
{Fore.CYAN}{"═" * 30}{Style.RESET_ALL}""")


def show_final_stats(
    score: int,
    words_learned: list[str],
    time_played,
    correct_guesses: int,
    total_attempts: int,
) -> None:
    accuracy = (correct_guesses / total_attempts * 100) if total_attempts > 0 else 0
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                      📊 FINAL STATS 📊                        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.GREEN}Final Score:{Style.RESET_ALL} {score}
{Fore.YELLOW}Words Learned:{Style.RESET_ALL} {len(words_learned)}
{Fore.BLUE}Time Played:{Style.RESET_ALL} {time_played}
{Fore.MAGENTA}Accuracy:{Style.RESET_ALL} {accuracy:.1f}%
{Fore.CYAN}Correct Guesses:{Style.RESET_ALL} {correct_guesses}/{total_attempts}

{Fore.YELLOW}Words you learned:{Style.RESET_ALL}
{", ".join(words_learned) if words_learned else "None"}

{Fore.CYAN}{"═" * 60}{Style.RESET_ALL}""")


def show_new_high_score() -> None:
    print(f"\n{Fore.GREEN}{Style.BRIGHT}🏆 NEW HIGH SCORE! 🏆{Style.RESET_ALL}")


def press_enter_to_continue(message: str = "Press Enter to continue to next round...") -> None:
    input(f"\n{Fore.CYAN}{message}{Style.RESET_ALL}")


def show_farewell() -> None:
    print(f"\n{Fore.GREEN}Thank you for playing Letter Vocabulary Master!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Keep learning! 📚{Style.RESET_ALL}")


def show_invalid_choice() -> None:
    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
    time.sleep(1)
