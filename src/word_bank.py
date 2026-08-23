"""Vocabulary data for Letter Vocabulary Master."""

from __future__ import annotations

import random
from dataclasses import dataclass

DIFFICULTIES = ("easy", "medium", "hard")


@dataclass(frozen=True)
class Word:
    """A single vocabulary entry."""

    text: str
    meaning: str
    ipa: str
    sentence: str


WORD_BANK: dict[str, list[Word]] = {
    "easy": [
        Word("apple", "سیب", "/ˈæpəl/", "I eat an apple every day."),
        Word("book", "کتاب", "/bʊk/", "She is reading a book."),
        Word("cat", "گربه", "/kæt/", "The cat is sleeping."),
        Word("dog", "سگ", "/dɔːɡ/", "My dog is very friendly."),
        Word("house", "خانه", "/haʊs/", "They live in a big house."),
        Word("water", "آب", "/ˈwɔːtər/", "Please drink more water."),
        Word("friend", "دوست", "/frend/", "He is my best friend."),
        Word("school", "مدرسه", "/skuːl/", "The children go to school."),
        Word("happy", "خوشحال", "/ˈhæpi/", "She looks very happy today."),
        Word("family", "خانواده", "/ˈfæməli/", "My family is very important to me."),
    ],
    "medium": [
        Word("beautiful", "زیبا", "/ˈbjuːtɪfəl/", "The sunset was beautiful."),
        Word("important", "مهم", "/ɪmˈpɔːrtənt/", "This is an important decision."),
        Word("knowledge", "دانش", "/ˈnɑːlɪdʒ/", "Knowledge is power."),
        Word("environment", "محیط زیست", "/ɪnˈvaɪrənmənt/", "We must protect the environment."),
        Word("successful", "موفق", "/səkˈsesfəl/", "She became a successful doctor."),
        Word("difficult", "دشوار", "/ˈdɪfɪkəlt/", "The exam was very difficult."),
        Word("interesting", "جالب", "/ˈɪntrəstɪŋ/", "The book is very interesting."),
        Word("necessary", "ضروری", "/ˈnesəseri/", "Sleep is necessary for health."),
        Word("experience", "تجربه", "/ɪkˈspɪriəns/", "Traveling is a great experience."),
        Word("government", "دولت", "/ˈɡʌvərnmənt/", "The government announced new policies."),
    ],
    "hard": [
        Word("entrepreneur", "کارآفرین", "/ˌɑːntrəprəˈnɜːr/", "The entrepreneur started a new company."),
        Word("consciousness", "آگاهی", "/ˈkɑːnʃəsnəs/", "Human consciousness is complex."),
        Word("philosophical", "فلسفی", "/ˌfɪləˈsɑːfɪkəl/", "They had a philosophical discussion."),
        Word("revolutionary", "انقلابی", "/ˌrevəˈluːʃəneri/", "It was a revolutionary idea."),
        Word("extraordinary", "استثنایی", "/ɪkˈstrɔːrdəneri/", "She has extraordinary talent."),
        Word("sophisticated", "پیچیده و پیشرفته", "/səˈfɪstɪkeɪtɪd/", "The system is very sophisticated."),
        Word("unprecedented", "بی‌سابقه", "/ʌnˈpresɪdentɪd/", "This is an unprecedented situation."),
        Word("psychological", "روانشناختی", "/ˌsaɪkəˈlɑːdʒɪkəl/", "The study has psychological implications."),
        Word("infrastructure", "زیرساخت", "/ˈɪnfrəstrʌktʃər/", "The city needs better infrastructure."),
        Word("communication", "ارتباطات", "/kəˌmjuːnɪˈkeɪʃən/", "Good communication is essential."),
    ],
}


def get_random_word(difficulty: str) -> Word:
    """Return a random word for the given difficulty."""
    return random.choice(WORD_BANK[difficulty])
