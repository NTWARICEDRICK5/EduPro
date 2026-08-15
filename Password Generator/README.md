# Password Generator

A small command-line tool that creates cryptographically secure random passwords using Python's `secrets` module.

## Run it

```bash
python3 password_generator.py
```

The interactive mode lets you select a length, character types, and whether to exclude visually ambiguous characters.

You can also generate a password in one command:

```bash
python3 password_generator.py --length 20 --exclude-ambiguous
python3 password_generator.py --length 12 --no-symbols
```

## Test it

```bash
python3 -m pytest tests
```
