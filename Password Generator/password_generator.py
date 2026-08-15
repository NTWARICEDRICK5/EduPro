#!/usr/bin/env python3
"""Generate cryptographically secure passwords from the command line."""

from __future__ import annotations

import argparse
import secrets
import string
from collections.abc import Sequence


LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"
MINIMUM_LENGTH = 4


def build_character_groups(
    *,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> list[str]:
    """Return the enabled character groups, optionally removing look-alikes."""
    groups = []
    if lowercase:
        groups.append(LOWERCASE)
    if uppercase:
        groups.append(UPPERCASE)
    if digits:
        groups.append(DIGITS)
    if symbols:
        groups.append(SYMBOLS)

    if exclude_ambiguous:
        ambiguous = set("Il1O0o")
        groups = ["".join(character for character in group if character not in ambiguous) for group in groups]
    return groups


def generate_password(length: int, character_groups: Sequence[str]) -> str:
    """Generate a password containing at least one character from each group."""
    groups = [group for group in character_groups if group]
    if not groups:
        raise ValueError("Choose at least one character type.")
    if length < len(groups):
        raise ValueError(f"Length must be at least {len(groups)} for the selected character types.")

    password = [secrets.choice(group) for group in groups]
    pool = "".join(groups)
    password.extend(secrets.choice(pool) for _ in range(length - len(password)))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def strength_label(length: int, group_count: int) -> str:
    """Give a simple, transparent strength hint based on selected options."""
    if length >= 16 and group_count >= 3:
        return "Very strong"
    if length >= 12 and group_count >= 3:
        return "Strong"
    if length >= 8 and group_count >= 2:
        return "Good"
    return "Weak — use a longer password with more character types"


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Read a yes/no answer, returning the supplied default for an empty answer."""
    suffix = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{prompt} ({suffix}): ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.")


def ask_length() -> int:
    """Read a usable password length."""
    while True:
        answer = input("Password length [16]: ").strip()
        if not answer:
            return 16
        try:
            length = int(answer)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if length < MINIMUM_LENGTH:
            print(f"Please choose a length of at least {MINIMUM_LENGTH}.")
            continue
        return length


def interactive_options() -> tuple[int, list[str]]:
    """Collect password settings for the interactive interface."""
    print("\nChoose the character types to include:")
    lowercase = ask_yes_no("Lowercase letters", True)
    uppercase = ask_yes_no("Uppercase letters", True)
    digits = ask_yes_no("Numbers", True)
    symbols = ask_yes_no("Symbols", True)
    exclude_ambiguous = ask_yes_no("Exclude ambiguous characters (I, l, 1, O, 0)", False)
    groups = build_character_groups(
        lowercase=lowercase,
        uppercase=uppercase,
        digits=digits,
        symbols=symbols,
        exclude_ambiguous=exclude_ambiguous,
    )
    if not groups:
        print("At least one character type is required; using lowercase letters.")
        groups = [LOWERCASE]
    return ask_length(), groups


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a secure random password.")
    parser.add_argument("-l", "--length", type=int, help="Password length (minimum: 4)")
    parser.add_argument("--no-lowercase", action="store_true", help="Exclude lowercase letters")
    parser.add_argument("--no-uppercase", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    parser.add_argument("--exclude-ambiguous", action="store_true", help="Exclude I, l, 1, O, 0")
    return parser.parse_args()


def main() -> int:
    """Run interactively when no flags are passed, or generate from CLI flags."""
    args = parse_args()
    try:
        if args.length is None and len(__import__("sys").argv) == 1:
            print("=== Password Generator ===")
            while True:
                length, groups = interactive_options()
                password = generate_password(length, groups)
                print(f"\nYour password: {password}")
                print(f"Strength: {strength_label(length, len(groups))}")
                if not ask_yes_no("Generate another password", True):
                    print("Keep your password somewhere safe.")
                    return 0
        groups = build_character_groups(
            lowercase=not args.no_lowercase,
            uppercase=not args.no_uppercase,
            digits=not args.no_digits,
            symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous,
        )
        length = args.length if args.length is not None else 16
        print(generate_password(length, groups))
        return 0
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        return 0
    except ValueError as error:
        print(f"Error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
