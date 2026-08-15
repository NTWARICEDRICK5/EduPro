"""Tests for the password generator."""

import importlib.util
from pathlib import Path
import string


MODULE_PATH = Path(__file__).parents[1] / "password_generator.py"
SPEC = importlib.util.spec_from_file_location("password_generator", MODULE_PATH)
password_generator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(password_generator)


def test_generated_password_has_requested_length_and_all_groups():
    groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#"]
    password = password_generator.generate_password(20, groups)

    assert len(password) == 20
    assert any(character in string.ascii_lowercase for character in password)
    assert any(character in string.ascii_uppercase for character in password)
    assert any(character in string.digits for character in password)
    assert any(character in "!@#" for character in password)


def test_password_generation_rejects_impossible_options():
    try:
        password_generator.generate_password(3, ["abc", "XYZ", "123", "!@#"])
    except ValueError as error:
        assert "at least 4" in str(error)
    else:
        raise AssertionError("Expected a ValueError")


def test_ambiguous_characters_can_be_excluded():
    groups = password_generator.build_character_groups(exclude_ambiguous=True)

    assert not set("Il1O0o").intersection("".join(groups))
