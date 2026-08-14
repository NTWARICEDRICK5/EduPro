#!/usr/bin/env python3
"""A small interactive number guessing game."""

from __future__ import annotations

import random
from collections.abc import Callable
from typing import NamedTuple


MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_ATTEMPTS = 7


class Difficulty(NamedTuple):
    """Settings for one style of play."""

    label: str
    minimum: int
    maximum: int
    attempts: int
    points: int


DIFFICULTIES = {
    "e": Difficulty("Easy", 1, 50, 10, 5),
    "m": Difficulty("Medium", 1, 100, 7, 10),
    "h": Difficulty("Hard", 1, 200, 6, 20),
}


def evaluate_guess(guess: int, secret_number: int) -> str:
    """Return feedback for a valid guess against the secret number."""
    if guess < secret_number:
        return "low"
    if guess > secret_number:
        return "high"
    return "correct"


def read_guess(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
    minimum: int = MIN_NUMBER,
    maximum: int = MAX_NUMBER,
) -> int | None:
    """Read a guess in range, returning None when the player chooses to quit."""
    while True:
        value = input_func(f"Enter a number from {minimum} to {maximum} (or q to quit): ").strip()
        if value.lower() in {"q", "quit", "exit"}:
            return None
        try:
            guess = int(value)
        except ValueError:
            output_func("Please enter a whole number.")
            continue

        if not minimum <= guess <= maximum:
            output_func(f"Please choose a number from {minimum} to {maximum}.")
            continue
        return guess


def play_round(
    secret_number: int,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
    minimum: int = MIN_NUMBER,
    maximum: int = MAX_NUMBER,
    max_attempts: int = MAX_ATTEMPTS,
) -> bool | None:
    """Play one round; return True for a win, False for a loss, None for quit."""
    previous_distance: int | None = None
    for attempt in range(1, max_attempts + 1):
        guesses_left = max_attempts - attempt
        output_func(f"\nAttempt {attempt} of {max_attempts}")
        guess = read_guess(input_func, output_func, minimum, maximum)
        if guess is None:
            return None

        result = evaluate_guess(guess, secret_number)
        if result == "correct":
            output_func(f"Correct! You guessed the number in {attempt} attempt{'s' if attempt != 1 else ''}.")
            return True

        hint = "Too low!" if result == "low" else "Too high!"
        distance = abs(secret_number - guess)
        if previous_distance is not None:
            hint += " Getting warmer!" if distance < previous_distance else " Getting colder!"
        previous_distance = distance
        suffix = f" You have {guesses_left} guess{'es' if guesses_left != 1 else ''} left." if guesses_left else ""
        output_func(hint + suffix)

    output_func(f"\nOut of guesses! The number was {secret_number}.")
    return False


def wants_to_play_again(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> bool:
    """Ask until the player gives a clear replay response."""
    while True:
        response = input_func("Play again? (y/n): ").strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no", "q", "quit", "exit"}:
            return False
        output_func("Please enter y or n.")


def choose_difficulty(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> Difficulty:
    """Let the player choose a range and number of attempts."""
    output_func("\nChoose your challenge:")
    output_func("  [E]asy   1–50   · 10 attempts · 5 points")
    output_func("  [M]edium 1–100  · 7 attempts  · 10 points")
    output_func("  [H]ard   1–200  · 6 attempts  · 20 points")
    while True:
        choice = input_func("Difficulty (e/m/h): ").strip().lower()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        output_func("Please choose e, m, or h.")


def main() -> int:
    """Run the interactive game."""
    print("=== Number Guessing Game ===")
    score = 0

    try:
        while True:
            difficulty = choose_difficulty()
            print(f"\n{difficulty.label} mode: find a number from {difficulty.minimum} to {difficulty.maximum}.")
            print(f"You have {difficulty.attempts} attempts. A win earns {difficulty.points} points!")
            outcome = play_round(
                random.randint(difficulty.minimum, difficulty.maximum),
                minimum=difficulty.minimum,
                maximum=difficulty.maximum,
                max_attempts=difficulty.attempts,
            )
            if outcome is None:
                print("Thanks for playing!")
                return 0
            if outcome:
                score += difficulty.points
                print(f"Score: {score} point{'s' if score != 1 else ''}.")
            if not wants_to_play_again():
                print(f"Thanks for playing! Final score: {score}.")
                return 0
            print("\nGreat choice — let’s go again!")
    except EOFError:
        print("\nThanks for playing!")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
