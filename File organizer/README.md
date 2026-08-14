# Intelligent File Organizer

A safe Python command-line tool that sorts the direct files in a selected
directory into category folders by their filename extensions.

## Safety behaviour

- Processes files only; it does not recurse into subdirectories.
- Skips hidden files by default (`--include-hidden` opts in).
- Never intentionally overwrites an existing destination. A collision such as
  `photo.jpg` becomes `photo_1.jpg`, then `photo_2.jpg`.
- Use `--dry-run` before organizing any real directory.

## Run it

```bash
python3 organizer.py /path/to/test-directory --dry-run
python3 organizer.py /path/to/test-directory
```

Optional flags:

```bash
python3 organizer.py ~/Downloads --dry-run --include-hidden --log-file organizer.log
```

## Safe manual test environment

Create an isolated directory, never use a personal folder for first tests:

```bash
mkdir -p /tmp/organizer-practice
touch /tmp/organizer-practice/photo.JPG
touch /tmp/organizer-practice/report.pdf
touch /tmp/organizer-practice/movie.mp4
touch /tmp/organizer-practice/script.py
touch /tmp/organizer-practice/mystery.xyz
python3 organizer.py /tmp/organizer-practice --dry-run
python3 organizer.py /tmp/organizer-practice
```

## Automated tests

Install the development dependency, then run the test suite:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest
```
