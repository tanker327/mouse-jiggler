#  pip install pyautogui

import pyautogui
import time
import random
from datetime import datetime

MIN_SLEEP_MINUTES = 3
MAX_SLEEP_MINUTES = 7
MAX_MOVEMENT_PIXELS = 50  # Maximum pixels to move in any direction

# Format: {day_of_week: (start_hour, end_hour)}
WORK_SCHEDULE = {
    0: (9, 17),  # Monday: 9 AM - 5 PM
    1: (9, 17),  # Tuesday
    2: (9, 17),  # Wednesday
    3: (9, 17),  # Thursday
    4: (9, 17),  # Friday
    5: None,     # Saturday: off
    6: None      # Sunday: off
}

while True:
    current_time = datetime.now()
    current_day = current_time.weekday()
    current_hour = current_time.hour

    schedule = WORK_SCHEDULE[current_day]
    if schedule and schedule[0] <= current_hour < schedule[1]:
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Generate small random movement
        delta_x = random.randint(-MAX_MOVEMENT_PIXELS, MAX_MOVEMENT_PIXELS)
        delta_y = random.randint(-MAX_MOVEMENT_PIXELS, MAX_MOVEMENT_PIXELS)
        
        # Move relative to current position
        pyautogui.moveRel(delta_x, delta_y)
        result = current_time.strftime("%I:%M:%S %p")
        print(f'Moved at {result} (delta: {delta_x}, {delta_y})')
    else:
        print(f"Outside work hours. Sleeping until next check.")
    
    # Random sleep time between MIN and MAX
    sleep_time = random.uniform(MIN_SLEEP_MINUTES, MAX_SLEEP_MINUTES) * 60
    print(f"Sleeping for {sleep_time/60:.2f} minutes")
    time.sleep(sleep_time)
