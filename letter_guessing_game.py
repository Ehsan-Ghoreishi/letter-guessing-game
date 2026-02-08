#!/usr/bin/env python3
"""
English Vocabulary Letter Guessing Game
A console-based educational game for learning English vocabulary.
Guess one letter at a time to reveal the hidden word.
"""

import json
import random
import time
import os
import sys
from datetime import datetime
from typing import Dict, List

try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama
except ImportError:
    print("Error: colorama is required. Install with: pip install colorama")
    sys.exit(1)

# Constants
MAX_ATTEMPTS = 6
ROUNDS_PER_GAME = 10
HIGH_SCORE_FILE = "letter_game_scores.json"

# Word database with 30 words organized by difficulty
WORD_DATABASE = {
    "easy": [
        {"word": "apple", "meaning": "سیب", "ipa": "/ˈæpəl/", "sentence": "I eat an apple every day."},
        {"word": "book", "meaning": "کتاب", "ipa": "/bʊk/", "sentence": "She is reading a book."},
        {"word": "cat", "meaning": "گربه", "ipa": "/kæt/", "sentence": "The cat is sleeping."},
        {"word": "dog", "meaning": "سگ", "ipa": "/dɔːɡ/", "sentence": "My dog is very friendly."},
        {"word": "house", "meaning": "خانه", "ipa": "/haʊs/", "sentence": "They live in a big house."},
        {"word": "water", "meaning": "آب", "ipa": "/ˈwɔːtər/", "sentence": "Please drink more water."},
        {"word": "friend", "meaning": "دوست", "ipa": "/frend/", "sentence": "He is my best friend."},
        {"word": "school", "meaning": "مدرسه", "ipa": "/skuːl/", "sentence": "The children go to school."},
        {"word": "happy", "meaning": "خوشحال", "ipa": "/ˈhæpi/", "sentence": "She looks very happy today."},
        {"word": "family", "meaning": "خانواده", "ipa": "/ˈfæməli/", "sentence": "My family is very important to me."},
    ],
    "medium": [
        {"word": "beautiful", "meaning": "زیبا", "ipa": "/ˈbjuːtɪfəl/", "sentence": "The sunset was beautiful."},
        {"word": "important", "meaning": "مهم", "ipa": "/ɪmˈpɔːrtənt/", "sentence": "This is an important decision."},
        {"word": "knowledge", "meaning": "دانش", "ipa": "/ˈnɑːlɪdʒ/", "sentence": "Knowledge is power."},
        {"word": "environment", "meaning": "محیط زیست", "ipa": "/ɪnˈvaɪrənmənt/", "sentence": "We must protect the environment."},
        {"word": "successful", "meaning": "موفق", "ipa": "/səkˈsesfəl/", "sentence": "She became a successful doctor."},
        {"word": "difficult", "meaning": "دشوار", "ipa": "/ˈdɪfɪkəlt/", "sentence": "The exam was very difficult."},
        {"word": "interesting", "meaning": "جالب", "ipa": "/ˈɪntrəstɪŋ/", "sentence": "The book is very interesting."},
        {"word": "necessary", "meaning": "ضروری", "ipa": "/ˈnesəseri/", "sentence": "Sleep is necessary for health."},
        {"word": "experience", "meaning": "تجربه", "ipa": "/ɪkˈspɪriəns/", "sentence": "Traveling is a great experience."},
        {"word": "government", "meaning": "دولت", "ipa": "/ˈɡʌvərnmənt/", "sentence": "The government announced new policies."},
    ],
    "hard": [
        {"word": "entrepreneur", "meaning": "کارآفرین", "ipa": "/ˌɑːntrəprəˈnɜːr/", "sentence": "The entrepreneur started a new company."},
        {"word": "consciousness", "meaning": "آگاهی", "ipa": "/ˈkɑːnʃəsnəs/", "sentence": "Human consciousness is complex."},
        {"word": "philosophical", "meaning": "فلسفی", "ipa": "/ˌfɪləˈsɑːfɪkəl/", "sentence": "They had a philosophical discussion."},
        {"word": "revolutionary", "meaning": "انقلابی", "ipa": "/ˌrevəˈluːʃəneri/", "sentence": "It was a revolutionary idea."},
        {"word": "extraordinary", "meaning": "استثنایی", "ipa": "/ɪkˈstrɔːrdəneri/", "sentence": "She has extraordinary talent."},
        {"word": "sophisticated", "meaning": "پیچیده و پیشرفته", "ipa": "/səˈfɪstɪkeɪtɪd/", "sentence": "The system is very sophisticated."},
        {"word": "unprecedented", "meaning": "بی‌سابقه", "ipa": "/ʌnˈpresɪdentɪd/", "sentence": "This is an unprecedented situation."},
        {"word": "psychological", "meaning": "روانشناختی", "ipa": "/ˌsaɪkəˈlɑːdʒɪkəl/", "sentence": "The study has psychological implications."},
        {"word": "infrastructure", "meaning": "زیرساخت", "ipa": "/ˈɪnfrəstrʌktʃər/", "sentence": "The city needs better infrastructure."},
        {"word": "communication", "meaning": "ارتباطات", "ipa": "/kəˌmjuːnɪˈkeɪʃən/", "sentence": "Good communication is essential."},
    ]
}

class LetterGuessingGame:
    """Main game class for the letter guessing vocabulary game."""
    
    def __init__(self):
        self.score = 0
        self.round = 0
        self.words_learned = []
        self.start_time = None
        self.total_attempts = 0
        self.correct_guesses = 0
        self.high_scores = self.load_high_scores()
        
    def load_high_scores(self) -> List[Dict]:
        """Load high scores from JSON file."""
        try:
            if os.path.exists(HIGH_SCORE_FILE):
                with open(HIGH_SCORE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return []
    
    def save_high_scores(self):
        """Save high scores to JSON file."""
        try:
            with open(HIGH_SCORE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.high_scores, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
    
    def add_high_score(self, name: str, score: int, difficulty: str):
        """Add a new high score."""
        self.high_scores.append({
            "name": name,
            "score": score,
            "difficulty": difficulty,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10
        self.save_high_scores()
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def animate_text(self, text: str, delay: float = 0.03):
        """Animate text appearance."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def show_countdown(self, seconds: int = 3):
        """Show animated countdown."""
        for i in range(seconds, 0, -1):
            print(f"{Fore.YELLOW}{Style.BRIGHT}{i}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(1)
            if i > 1:
                print('\r', end='', flush=True)
        print(f"\r{Fore.GREEN}GO!{Style.RESET_ALL}")
        time.sleep(0.5)
    
    def display_main_menu(self):
        """Display the main menu."""
        self.clear_screen()
        print(f"""
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

{Fore.CYAN}Choose an option (1-4): {Style.RESET_ALL}""", end="")
    
    def display_instructions(self):
        """Display game instructions."""
        self.clear_screen()
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

    def display_high_scores(self):
        """Display high scores."""
        self.clear_screen()
        print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                    🏆 HIGH SCORES 🏆                         ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

        if not self.high_scores:
            print(f"{Fore.YELLOW}No high scores yet. Be the first!{Style.RESET_ALL}")
        else:
            print(f"{'Rank':<6} {'Name':<15} {'Score':<8} {'Difficulty':<12} {'Date':<16}")
            print("-" * 60)
            for i, score_data in enumerate(self.high_scores[:10], 1):
                print(f"{i:<6} {score_data['name']:<15} {score_data['score']:<8} "
                      f"{score_data['difficulty']:<12} {score_data['date']:<16}")

        print(f"\n{Fore.CYAN}Press Enter to return to menu...{Style.RESET_ALL}")
        input()

    def get_difficulty(self) -> str:
        """Get difficulty level from user."""
        while True:
            self.clear_screen()
            print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                    🎯 SELECT DIFFICULTY 🎯                    ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.GREEN}1. Easy{Style.RESET_ALL}   (Simple words, 10 points each)
{Fore.YELLOW}2. Medium{Style.RESET_ALL} (Intermediate words, 20 points each)
{Fore.RED}3. Hard{Style.RESET_ALL}   (Advanced words, 30 points each)

{Fore.CYAN}Choose difficulty (1-3): {Style.RESET_ALL}""", end="")

            choice = input().strip()
            if choice == "1":
                return "easy"
            elif choice == "2":
                return "medium"
            elif choice == "3":
                return "hard"
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                time.sleep(1)

    def get_random_word(self, difficulty: str) -> Dict:
        """Get a random word from the specified difficulty level."""
        words = WORD_DATABASE[difficulty]
        return random.choice(words)

    def display_word_state(self, word: str, guessed_letters: set):
        """Display the current state of the word with underscores."""
        display = ""
        for letter in word:
            if letter in guessed_letters:
                display += f"{Fore.GREEN}{letter.upper()}{Style.RESET_ALL} "
            else:
                display += "_ "
        return display.strip()

    def display_guessed_letters(self, correct_letters: set, wrong_letters: set):
        """Display the letters that have been guessed."""
        print(f"\n{Fore.CYAN}Letters Guessed:{Style.RESET_ALL}")

        # Show correct letters
        if correct_letters:
            correct_display = " ".join([f"{Fore.GREEN}{letter}{Style.RESET_ALL}" for letter in sorted(correct_letters)])
            print(f"Correct: {correct_display}")

        # Show wrong letters
        if wrong_letters:
            wrong_display = " ".join([f"{Fore.RED}{letter}{Style.RESET_ALL}" for letter in sorted(wrong_letters)])
            print(f"Wrong: {wrong_display}")

    def display_word_info(self, word_data: Dict):
        """Display complete word information."""
        print(f"""
{Fore.CYAN}{Style.BRIGHT}═══ WORD INFORMATION ═══{Style.RESET_ALL}
{Fore.GREEN}Word:{Style.RESET_ALL} {word_data['word']}
{Fore.YELLOW}Meaning:{Style.RESET_ALL} {word_data['meaning']}
{Fore.BLUE}Pronunciation:{Style.RESET_ALL} {word_data['ipa']}
{Fore.MAGENTA}Example:{Style.RESET_ALL} {word_data['sentence']}
{Fore.CYAN}{'═' * 30}{Style.RESET_ALL}""")

    def is_word_complete(self, word: str, guessed_letters: set) -> bool:
        """Check if the word has been completely guessed."""
        return all(letter in guessed_letters for letter in word)

    def play_round(self, difficulty: str) -> bool:
        """Play a single round of the game."""
        word_data = self.get_random_word(difficulty)
        word = word_data['word'].upper()
        correct_letters = set()
        wrong_letters = set()
        attempts_left = MAX_ATTEMPTS

        print(f"\n{Fore.CYAN}Round {self.round + 1} of {ROUNDS_PER_GAME}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Word has {len(word)} letters{Style.RESET_ALL}")

        while attempts_left > 0:
            # Display current state
            print(f"\n{Fore.CYAN}Attempts left: {attempts_left}{Style.RESET_ALL}")
            print(f"Word: {self.display_word_state(word, correct_letters)}")
            self.display_guessed_letters(correct_letters, wrong_letters)

            # Get user letter guess
            while True:
                guess = input(f"{Fore.GREEN}Enter a letter: {Style.RESET_ALL}").strip().upper()
                if len(guess) == 1 and guess.isalpha():
                    if guess in correct_letters or guess in wrong_letters:
                        print(f"{Fore.YELLOW}You already guessed that letter!{Style.RESET_ALL}")
                        continue
                    break
                print(f"{Fore.RED}Please enter a single alphabet letter!{Style.RESET_ALL}")

            self.total_attempts += 1

            # Check if letter is in word
            if guess in word:
                print(f"{Fore.GREEN}✓ CORRECT! The letter '{guess}' exists in the word.{Style.RESET_ALL}")
                correct_letters.add(guess)
                self.correct_guesses += 1

                # Check if word is complete
                if self.is_word_complete(word, correct_letters):
                    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 WORD COMPLETED! 🎉{Style.RESET_ALL}")
                    points = {"easy": 10, "medium": 20, "hard": 30}[difficulty]
                    bonus = attempts_left * 5  # Bonus for remaining attempts
                    total_points = points + bonus
                    self.score += total_points
                    self.words_learned.append(word_data['word'])

                    print(f"{Fore.GREEN}You earned {total_points} points! ({points} + {bonus} bonus){Style.RESET_ALL}")
                    self.display_word_info(word_data)
                    return True
            else:
                print(f"{Fore.RED}✗ WRONG! The letter '{guess}' does not exist in the word.{Style.RESET_ALL}")
                wrong_letters.add(guess)
                attempts_left -= 1

        # Out of attempts
        print(f"\n{Fore.RED}{Style.BRIGHT}❌ GAME OVER ❌{Style.RESET_ALL}")
        print(f"{Fore.RED}The word was: {word}{Style.RESET_ALL}")
        self.display_word_info(word_data)
        return False

    def display_final_stats(self):
        """Display final game statistics."""
        if not self.start_time:
            return

        end_time = datetime.now()
        time_played = end_time - self.start_time
        accuracy = (self.correct_guesses / self.total_attempts * 100) if self.total_attempts > 0 else 0

        print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                      📊 FINAL STATS 📊                        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.GREEN}Final Score:{Style.RESET_ALL} {self.score}
{Fore.YELLOW}Words Learned:{Style.RESET_ALL} {len(self.words_learned)}
{Fore.BLUE}Time Played:{Style.RESET_ALL} {time_played}
{Fore.MAGENTA}Accuracy:{Style.RESET_ALL} {accuracy:.1f}%
{Fore.CYAN}Correct Guesses:{Style.RESET_ALL} {self.correct_guesses}/{self.total_attempts}

{Fore.YELLOW}Words you learned:{Style.RESET_ALL}
{', '.join(self.words_learned) if self.words_learned else 'None'}

{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}""")

    def play_game(self):
        """Main game loop."""
        difficulty = self.get_difficulty()
        player_name = input(f"{Fore.CYAN}Enter your name: {Style.RESET_ALL}").strip()

        self.clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}Get ready to play...{Style.RESET_ALL}")
        time.sleep(1)
        self.show_countdown()

        self.score = 0
        self.round = 0
        self.words_learned = []
        self.start_time = datetime.now()
        self.total_attempts = 0
        self.correct_guesses = 0

        for self.round in range(ROUNDS_PER_GAME):
            self.play_round(difficulty)

            if self.round < ROUNDS_PER_GAME - 1:
                input(f"\n{Fore.CYAN}Press Enter to continue to next round...{Style.RESET_ALL}")
                self.clear_screen()

        self.display_final_stats()

        # Check for high score
        if self.high_scores and self.score > self.high_scores[-1]['score'] or not self.high_scores:
            self.add_high_score(player_name, self.score, difficulty)
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🏆 NEW HIGH SCORE! 🏆{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to return to menu...{Style.RESET_ALL}")

    def run(self):
        """Run the main game loop."""
        while True:
            self.display_main_menu()
            choice = input().strip()

            if choice == "1":
                self.play_game()
            elif choice == "2":
                self.display_high_scores()
            elif choice == "3":
                self.display_instructions()
            elif choice == "4":
                print(f"\n{Fore.GREEN}Thank you for playing Letter Vocabulary Master!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Keep learning! 📚{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                time.sleep(1)

def main():
    """Main function to run the letter guessing vocabulary game."""
    try:
        game = LetterGuessingGame()
        game.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Game interrupted. Thanks for playing!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
