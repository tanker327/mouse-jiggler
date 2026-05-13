import pyautogui
import time
import random
import sys
from datetime import datetime, timedelta

MIN_SLEEP_MINUTES = 2
MAX_SLEEP_MINUTES = 4
MAX_MOVEMENT_PIXELS = 50

# Format: {day_of_week: (start_hour, end_hour)}. None = off.
WORK_SCHEDULE = {
    0: (8, 17),  # Monday: 8 AM - 5 PM
    1: (8, 17),  # Tuesday
    2: (8, 17),  # Wednesday
    3: (8, 17),  # Thursday
    4: (8, 17),  # Friday
    5: None,     # Saturday
    6: None,     # Sunday
}

USE_COLOR = sys.stdout.isatty()

def _c(code):
    return code if USE_COLOR else ""

DIM    = _c("\033[2m")
BOLD   = _c("\033[1m")
RESET  = _c("\033[0m")
GREEN  = _c("\033[32m")
CYAN   = _c("\033[36m")
YELLOW = _c("\033[33m")
RED    = _c("\033[31m")
BLUE   = _c("\033[34m")


def next_work_start(now):
    for offset in range(8):
        day = now + timedelta(days=offset)
        schedule = WORK_SCHEDULE[day.weekday()]
        if not schedule:
            continue
        candidate = day.replace(hour=schedule[0], minute=0, second=0, microsecond=0)
        if candidate > now:
            return candidate
    return None


def fmt_sleep(seconds):
    if seconds < 3600:
        return f"next in {seconds/60:.1f}m"
    return f"next in {seconds/3600:.2f}h"


def row(t, color, glyph, message, suffix=None):
    ts = t.strftime("%H:%M:%S")
    body = f"{message:<52}"
    line = f"{DIM}{ts}{RESET}  {color}{glyph}{RESET}  {body}"
    if suffix:
        line += f"  {DIM}{suffix}{RESET}"
    print(line)


def log_start():
    today = datetime.now().strftime("%a %d %b %Y")
    print(f"{BOLD}▶ mouse-jiggler started{RESET}  {DIM}— {today} — Ctrl+C to stop{RESET}")


def log_stop():
    print(f"{BOLD}■ stopped{RESET}")


def log_move(t, delta, recentered, sleep_seconds):
    if recentered:
        msg = f"re-centered, moved ({delta[0]:+d}, {delta[1]:+d})"
        row(t, CYAN, "↻", msg, fmt_sleep(sleep_seconds))
    else:
        msg = f"moved ({delta[0]:+d}, {delta[1]:+d})"
        row(t, GREEN, "→", msg, fmt_sleep(sleep_seconds))


def log_skip(t, reason, sleep_seconds):
    row(t, YELLOW, "~", f"skipped — {reason}", fmt_sleep(sleep_seconds))


def log_failsafe(t, sleep_seconds):
    row(t, RED, "!", "fail-safe triggered (mouse in corner)", fmt_sleep(sleep_seconds))


def log_offhours(t, next_start, sleep_seconds):
    wake = next_start.strftime("%a %d %b %H:%M")
    row(t, BLUE, "*", f"outside hours — sleeping until {wake}", fmt_sleep(sleep_seconds))


def log_no_schedule(t, sleep_seconds):
    row(t, BLUE, "*", "no work scheduled this week", fmt_sleep(sleep_seconds))


def main():
    log_start()
    last_position = None
    try:
        while True:
            current_time = datetime.now()
            schedule = WORK_SCHEDULE[current_time.weekday()]
            in_window = schedule and schedule[0] <= current_time.hour < schedule[1]

            if in_window:
                sleep_seconds = random.uniform(MIN_SLEEP_MINUTES, MAX_SLEEP_MINUTES) * 60
                try:
                    current_x, current_y = pyautogui.position()
                    if last_position is not None and (current_x, current_y) != last_position:
                        log_skip(current_time, "user active", sleep_seconds)
                    else:
                        screen_width, screen_height = pyautogui.size()
                        edge_threshold = MAX_MOVEMENT_PIXELS + 10
                        recentered = (current_x < edge_threshold or
                                      current_y < edge_threshold or
                                      current_x > screen_width - edge_threshold or
                                      current_y > screen_height - edge_threshold)
                        if recentered:
                            pyautogui.moveTo(screen_width // 2, screen_height // 2)

                        delta_x = random.randint(-MAX_MOVEMENT_PIXELS, MAX_MOVEMENT_PIXELS)
                        delta_y = random.randint(-MAX_MOVEMENT_PIXELS, MAX_MOVEMENT_PIXELS)
                        pyautogui.moveRel(delta_x, delta_y)
                        log_move(current_time, (delta_x, delta_y), recentered, sleep_seconds)

                    last_position = pyautogui.position()
                except pyautogui.FailSafeException:
                    log_failsafe(current_time, sleep_seconds)
                    last_position = None
            else:
                next_start = next_work_start(current_time)
                # Reset because the user is free to move the mouse off-hours;
                # comparing against a stale position would trigger a false "active" skip on resume.
                last_position = None
                if next_start is None:
                    sleep_seconds = 3600
                    log_no_schedule(current_time, sleep_seconds)
                else:
                    sleep_seconds = (next_start - current_time).total_seconds()
                    log_offhours(current_time, next_start, sleep_seconds)

            time.sleep(sleep_seconds)
    except KeyboardInterrupt:
        print()
        log_stop()


if __name__ == "__main__":
    main()
