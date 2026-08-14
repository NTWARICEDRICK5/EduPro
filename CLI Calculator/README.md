# CLI Calculator

A simple, dependency-free Python calculator that runs interactively in your terminal.

## Requirements

- Python 3.10 or later

## Run the calculator

From this project directory, run:

```bash
python3 calculator.py
```

## Example session

```text
=== CLI Calculator ===

Enter first number (or ans): 10
Choose operator (+, -, *, /, **, %, //): +
Enter second number (or ans): 5

Result: 15
Calculate again? (y/n, h for history, help, q): y

Enter first number (or ans): last
Choose operator (+, -, *, /, **, %): **
Enter second number (or ans): 2

Result: 225
Calculate again? (y/n, h for history): n
Goodbye!
```

## Supported operations

| Operator | Operation | Example |
| --- | --- | --- |
| `+` | Addition | `10 + 5 = 15` |
| `-` | Subtraction | `10 - 5 = 5` |
| `*` | Multiplication | `10 * 5 = 50` |
| `/` | Division | `10 / 4 = 2.5` |
| `**` | Exponentiation | `2 ** 3 = 8` |
| `%` | Modulo (remainder) | `10 % 3 = 1` |
| `//` | Floor division | `10 // 3 = 3` |

## Input handling

The calculator asks again when a number or operator is invalid. Division and modulo by zero are prevented with a clear error message.

Use `ans` or `last` instead of either number to reuse the previous result. Enter `help` for a command summary, `h` to display session history, `clear` at the first-number prompt to clear history, or `q` to exit. At the continuation prompt, enter `y` to calculate again or `n` to exit.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```
