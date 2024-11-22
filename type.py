import pyautogui
import time
import sys

# Constants
COUNTDOWN_SECONDS = 5

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def type_file_content(file_path):
    content = read_file_content(file_path)

    print("Starting in...")
    for i in range(COUNTDOWN_SECONDS, 0, -1):
        print(i)
        time.sleep(1)

    print("*" * 20)
    print("Typing now!")
    print("*" * 20)

    pyautogui.typewrite(content, interval=0.1)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python type.py <file_path>")
        sys.exit(1)
        
    type_file_content(sys.argv[1])