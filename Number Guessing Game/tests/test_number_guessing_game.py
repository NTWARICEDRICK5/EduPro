import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).parents[1] / "number_guessing_game.py"
SPEC = importlib.util.spec_from_file_location("number_guessing_game", MODULE_PATH)
game = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(game)


class NumberGuessingGameTests(unittest.TestCase):
    def test_evaluate_guess(self):
        self.assertEqual(game.evaluate_guess(24, 50), "low")
        self.assertEqual(game.evaluate_guess(76, 50), "high")
        self.assertEqual(game.evaluate_guess(50, 50), "correct")

    def test_read_guess_retries_invalid_values(self):
        answers = iter(["abc", "101", "42"])
        messages = []

        result = game.read_guess(lambda _: next(answers), messages.append)

        self.assertEqual(result, 42)
        self.assertEqual(messages, ["Please enter a whole number.", "Please choose a number from 1 to 100."])

    def test_play_round_wins(self):
        messages = []

        result = game.play_round(20, lambda _: "20", messages.append)

        self.assertTrue(result)
        self.assertIn("Correct! You guessed the number in 1 attempt.", messages)

    def test_play_round_loses_after_max_attempts(self):
        guesses = iter(["1"] * game.MAX_ATTEMPTS)
        messages = []

        result = game.play_round(50, lambda _: next(guesses), messages.append)

        self.assertFalse(result)
        self.assertEqual(messages[-1], "\nOut of guesses! The number was 50.")

    def test_play_round_can_quit(self):
        self.assertIsNone(game.play_round(50, lambda _: "q", lambda _: None))


if __name__ == "__main__":
    unittest.main()
