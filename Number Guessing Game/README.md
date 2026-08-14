# Number Guessing Game

A dependency-free command-line game with three challenge levels, warmer/colder clues, and a running score.

## Requirements

- Python 3.10 or later

## Run

From this directory:

```bash
python3 number_guessing_game.py
```

## How to play

1. Start the game and choose a difficulty:
   - **Easy**: guess from 1 to 50 in 10 attempts (5 points).
   - **Medium**: guess from 1 to 100 in 7 attempts (10 points).
   - **Hard**: guess from 1 to 200 in 6 attempts (20 points).
2. Enter a whole number inside the displayed range.
3. Use the clues to narrow it down. The game tells you **too high** or **too low**, then says whether your next guess is getting **warmer** or **colder**.
4. Guess the secret number before your attempts run out. Your score increases when you win.
5. Choose `y` to play another round or `n` to finish. Enter `q` at any guess prompt to quit immediately.

Invalid entries do not use an attempt, so take your time and enjoy the hunt!

## Example

```text
=== Number Guessing Game ===

Choose your challenge:
  [E]asy   1–50   · 10 attempts · 5 points
  [M]edium 1–100  · 7 attempts  · 10 points
  [H]ard   1–200  · 6 attempts  · 20 points
Difficulty (e/m/h): m

Medium mode: find a number from 1 to 100.
You have 7 attempts. A win earns 10 points!
```

## Run tests

```bash
python3 -m unittest discover -s tests -v
```
