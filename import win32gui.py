"""
Crazy Drift Auto Key Holder - Customizable Script
================================================

This script holds down two keys (default: 's' and 'd') continuously for a web game
running inside the Opera GX browser (or any window matching the target window title).
It also attempts to keep the target browser window focused periodically so the game
keeps receiving input, even if you switch tabs or minimize.

Controls:
- Toggle key (default: ']'): Starts/stops holding the keys.
- Exit key (default: 'esc'): Releases keys and exits the script.

Customization:
-------------
- TARGET_WINDOW_TITLE: Partial or full title of the target window (case-insensitive).
- KEYS_TO_HOLD: List of keys to hold down when toggled on.
- TOGGLE_HOTKEY: The key to start/stop holding keys.
- EXIT_HOTKEY: The key to exit the script.
- FOCUS_INTERVAL: Time in seconds between refocusing the target window when holding keys.

Usage:
------
1. Install dependencies:
   pip install keyboard pygetwindow

2. Run this script.

3. Focus the Opera GX browser with your game loaded.

4. Press the toggle hotkey (']' by default) to start holding keys.

5. Press it again to stop.

6. Press the exit hotkey ('esc' by default) to quit.

Notes:
------
- Due to OS and browser limitations, the window must be visible for reliable input.
- The script tries to keep the window focused but will steal focus if you switch tabs/apps.
- Customize keys and timings below as you wish!

"""

import keyboard
import pygetwindow as gw
import time
import threading

# ======= CUSTOMIZABLE SETTINGS =======

TARGET_WINDOW_TITLE = "Opera"        # Part of the browser window title (case-insensitive)
KEYS_TO_HOLD = ['s', 'd']             # Keys to hold down continuously
TOGGLE_HOTKEY = ']'                   # Key to toggle holding keys on/off
EXIT_HOTKEY = 'esc'                   # Key to exit the script gracefully
FOCUS_INTERVAL = 1.0                  # Seconds between attempts to refocus the window when holding keys

# =====================================

holding = False
stop_thread = False

def hold_keys():
    """Press and hold all keys in KEYS_TO_HOLD."""
    for key in KEYS_TO_HOLD:
        keyboard.press(key)

def release_keys():
    """Release all keys in KEYS_TO_HOLD."""
    for key in KEYS_TO_HOLD:
        keyboard.release(key)

def focus_target_window():
    """
    Finds and activates the target window matching TARGET_WINDOW_TITLE.
    Returns True if successful, False otherwise.
    """
    for window in gw.getWindowsWithTitle(TARGET_WINDOW_TITLE):
        if window.visible:
            try:
                window.activate()
                return True
            except Exception:
                pass
    return False

def keep_focus_loop():
    """
    Background thread function that refocuses the target window at intervals
    while keys are held, to keep the game receiving input.
    """
    while not stop_thread:
        if holding:
            focused = focus_target_window()
            if not focused:
                print(f"⚠️ Warning: Target window '{TARGET_WINDOW_TITLE}' not found or not visible.")
        time.sleep(FOCUS_INTERVAL)

def toggle_keys():
    """Toggle holding or releasing keys and print status."""
    global holding
    holding = not holding
    if holding:
        print(f"▶ Holding keys: {KEYS_TO_HOLD}")
        if focus_target_window():
            time.sleep(0.3)  # small delay to ensure focus before holding keys
            hold_keys()
        else:
            print(f"❌ Could not find window with title containing '{TARGET_WINDOW_TITLE}'. Stopping.")
            holding = False
    else:
        print(f"⏹ Releasing keys: {KEYS_TO_HOLD}")
        release_keys()

def main():
    global stop_thread
    print("=== Crazy Drift Auto Key Holder ===")
    print(f"Toggle keys: '{TOGGLE_HOTKEY}' | Exit: '{EXIT_HOTKEY}'")
    print(f"Target window title contains: '{TARGET_WINDOW_TITLE}'")
    print(f"Holding keys: {KEYS_TO_HOLD}")
    print(f"Refocusing every {FOCUS_INTERVAL} seconds while holding.")
    print("Make sure your game tab is open and visible in the target browser window.")
    print()

    # Start background thread to keep refocusing window
    focus_thread = threading.Thread(target=keep_focus_loop, daemon=True)
    focus_thread.start()

    # Register hotkeys
    keyboard.add_hotkey(TOGGLE_HOTKEY, toggle_keys)
    keyboard.wait(EXIT_HOTKEY)

    # Cleanup on exit
    stop_thread = True
    if holding:
        release_keys()
    print("\nExiting... keys released.")

if __name__ == "__main__":
    main()
