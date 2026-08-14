#!/usr/bin/env python3
"""An interactive command-line calculator."""

from decimal import Decimal, InvalidOperation
from typing import NamedTuple


OPERATIONS = {
    "+": lambda left, right: left + right,
    "-": lambda left, right: left - right,
    "*": lambda left, right: left * right,
    "/": lambda left, right: left / right,
    "**": lambda left, right: left**right,
    "%": lambda left, right: left % right,
    "//": lambda left, right: left // right,
}


class Calculation(NamedTuple):
    """A completed calculation stored for the current session."""

    left: Decimal
    operator: str
    right: Decimal
    result: Decimal


def format_result(value: Decimal) -> str:
    """Present a Decimal without unnecessary trailing zeroes."""
    if value == value.to_integral():
        return str(value.quantize(Decimal("1")))
    return format(value.normalize(), "f")


def read_number(prompt: str, previous_result: Decimal | None) -> Decimal | str:
    """Keep asking until the user enters a finite number or ``ans``."""
    while True:
        value = input(prompt).strip()
        if value.lower() in {"ans", "last"}:
            if previous_result is not None:
                return previous_result
            print("There is no previous result yet.")
            continue
        if value.lower() in {"h", "history"}:
            return "history"
        if value.lower() in {"help", "?"}:
            return "help"
        if value.lower() in {"q", "quit", "exit"}:
            return "quit"
        if value.lower() == "clear":
            return "clear"
        try:
            number = Decimal(value)
            if number.is_finite():
                return number
        except InvalidOperation:
            pass
        print("Please enter a valid number.")


def read_operator() -> str:
    """Keep asking until the user selects a supported operator."""
    while True:
        operator = input("Choose operator (+, -, *, /, **, %, //): ").strip()
        if operator in OPERATIONS:
            return operator
        print("Please choose one of: +, -, *, /, **, %, //.")


def calculate(left: Decimal, operator: str, right: Decimal) -> Decimal | None:
    """Calculate a result, returning None for invalid arithmetic."""
    if operator in {"/", "%", "//"} and right == 0:
        print("Error: cannot divide or take modulo by zero.")
        return None

    try:
        return OPERATIONS[operator](left, right)
    except (InvalidOperation, ValueError, ArithmeticError):
        print("Error: this calculation is not valid.")
        return None


def show_history(history: list[Calculation]) -> None:
    """Display completed calculations from the current session."""
    if not history:
        print("No calculations in this session yet.")
        return

    print("\nCalculation history:")
    for index, item in enumerate(history, start=1):
        print(
            f"{index}. {format_result(item.left)} {item.operator} "
            f"{format_result(item.right)} = {format_result(item.result)}"
        )


def calculate_again(history: list[Calculation]) -> bool:
    """Ask whether another calculation should be performed."""
    while True:
        answer = input("Calculate again? (y/n, h for history, help, q): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        if answer in {"h", "history"}:
            show_history(history)
            continue
        if answer in {"help", "?"}:
            print_help()
            continue
        if answer in {"q", "quit", "exit"}:
            return False
        print("Please enter y, n, h, help, or q.")


def print_help() -> None:
    print("\nCommands: ans/last reuse the previous result; h shows history; clear clears history; q exits.")
    print("Operators: +  -  *  /  **  %  //")


def main() -> int:
    print("=== CLI Calculator ===\n")
    history: list[Calculation] = []
    previous_result: Decimal | None = None
    try:
        while True:
            left_value = read_number("Enter first number (or ans): ", previous_result)
            if isinstance(left_value, str):
                if left_value == "history":
                    show_history(history)
                elif left_value == "help":
                    print_help()
                elif left_value == "clear":
                    history.clear()
                    print("History cleared.")
                else:
                    print("Goodbye!")
                    return 0
                continue
            left = left_value
            operator = read_operator()
            right_value = read_number("Enter second number (or ans): ", previous_result)
            if isinstance(right_value, str):
                print("Please enter a number for the second value.")
                continue
            right = right_value
            result = calculate(left, operator, right)

            if result is not None:
                print(f"\nResult: {format_result(result)}")
                history.append(Calculation(left, operator, right, result))
                previous_result = result

            if not calculate_again(history):
                print("Goodbye!")
                return 0
            print()
    except EOFError:
        print("\nGoodbye!")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
