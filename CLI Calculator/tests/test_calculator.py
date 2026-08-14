import pathlib
import subprocess
import sys
import unittest


PROJECT = pathlib.Path(__file__).resolve().parents[1]
CALCULATOR = PROJECT / "calculator.py"


def run_calculator(user_input: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CALCULATOR)],
        input=user_input,
        capture_output=True,
        text=True,
        check=False,
    )


class CalculatorTests(unittest.TestCase):
    def test_addition_flow(self) -> None:
        result = run_calculator("10\n+\n5\nn\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("=== CLI Calculator ===", result.stdout)
        self.assertIn("Result: 15", result.stdout)
        self.assertIn("Goodbye!", result.stdout)

    def test_calculates_again_when_requested(self) -> None:
        result = run_calculator("10\n+\n5\ny\n7\n*\n3\nn\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Result: 15", result.stdout)
        self.assertIn("Result: 21", result.stdout)

    def test_previous_answer_and_history_are_available(self) -> None:
        result = run_calculator("10\n+\n5\ny\nlast\n*\n2\nh\nn\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Result: 15", result.stdout)
        self.assertIn("Result: 30", result.stdout)
        self.assertIn("Calculation history:", result.stdout)
        self.assertIn("1. 10 + 5 = 15", result.stdout)
        self.assertIn("2. 15 * 2 = 30", result.stdout)

    def test_help_and_clear_commands(self) -> None:
        result = run_calculator("help\n10\n+\n2\ny\nclear\nq\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Commands:", result.stdout)
        self.assertIn("History cleared.", result.stdout)

    def test_invalid_entries_are_reprompted(self) -> None:
        result = run_calculator("not-a-number\n10\nx\n/\n0\ny\n6\n/\n2\nn\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Please enter a valid number.", result.stdout)
        self.assertIn("Please choose one of", result.stdout)
        self.assertIn("cannot divide", result.stdout)
        self.assertIn("Result: 3", result.stdout)


if __name__ == "__main__":
    unittest.main()
