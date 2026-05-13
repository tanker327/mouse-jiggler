# Mouse Jiggler

A simple Python script that simulates human mouse movement during work hours to prevent screen locks and "away" status.

## Features

- Small random mouse movements (±50 pixels)
- Random intervals between movements (2-4 minutes)
- Configurable work schedule for each day of the week
- Only runs during defined work hours
- Logs movement times and distances

## Requirements

This project uses [uv](https://docs.astral.sh/uv/) (Python 3.12+):

```bash
uv sync
```


## Configuration

The script can be configured by modifying these variables at the top of the file:

- `MIN_SLEEP_MINUTES`: Minimum time between movements (default: 2 minutes)
- `MAX_SLEEP_MINUTES`: Maximum time between movements (default: 4 minutes)
- `MAX_MOVEMENT_PIXELS`: Maximum distance mouse will move in any direction (default: 50 pixels)
- `WORK_SCHEDULE`: Dictionary defining work hours for each day
  - Keys are weekday numbers (0-6, Monday-Sunday)
  - Values are tuples of (start_hour, end_hour) in 24h format
  - Use `None` for off days

Example schedule:


```python
WORK_SCHEDULE = {
    0: (9, 17),  # Monday: 9 AM - 5 PM
    1: (9, 17),  # Tuesday
    # ...
}
```

## Usage

```bash
uv run python main.py
```

## Bonus: `type.py`

A companion one-shot script that auto-types text into the focused window after a 5-second countdown. Useful for pasting into apps that block clipboard paste.

```bash
uv run python type.py "hello world"        # type literal text
uv run python type.py @path/to/file.txt    # type the contents of a file
```

Note: `pyautogui.typewrite` only supports printable ASCII — non-ASCII characters in the input will be skipped.

## Any idea or Suggestion?

Feel free to open an issue or a PR.