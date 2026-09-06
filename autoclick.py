
from config.config import Config
from lib.screen_comparator.screen_comparator import ScreenComparator
from lib.mouse_controller.mouse_controller import MouseController
from lib.esc_down_listener.esc_down_listener import EscDownListener
from lib.rect.rect import Rect

import sys
import pyautogui
from datetime import datetime
import time
import threading

enter_exit_sequence = False
mouse = MouseController()

def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(f"[{timestamp}] {message}")

def show_mouse_position():
    
    try:
        while True:
            if enter_exit_sequence:
                log_message("Exiting show_mouse_position...")
                sys.exit(1)
            else:    
                x, y = pyautogui.position()
                log_message(f"Mouse Position: x = {x}, y = {y}")
                time.sleep(1) 
    except KeyboardInterrupt:
        print("\n keybord interrupt!!! exit... ")

def click_at_position(x, y):
    try:
        # 指定した座標にクリック
        mouse.click( x, y)
    except Exception as e:
        log_message(f"Error: {e}")
        
def move_mouse_to(x, y, duration=0.0):
    """
    Move the mouse cursor to the specified (x, y) position.
    
    :param x: target x-coordinate
    :param y: target y-coordinate
    :param duration: time in seconds for the movement (optional)
    """
    try:
        mouse.move_to(x, y, duration)
    except Exception as e:
        log_message(f"Error moving mouse: {e}")

def execute_click(config):

    global enter_exit_sequence

    for index, click_config in enumerate(config, start=1):

        x, y, pre_click_delay = click_config["x"], click_config["y"], click_config["pre_click_delay"]
        time.sleep(pre_click_delay - 1 )

        move_mouse_to(x, y, duration=1.0)
        log_message(f"Move Mouse at ({x}, {y}) - Step: {index}")
        time.sleep(1)

        click_at_position(x, y)
        log_message(f"Clicked at ({x}, {y}) - Step: {index}")
        
def execute_single_click(x, y):
    click_at_position(x, y)
    log_message(f"Clicked at ({x}, {y})")
        
def register_expected_area(comparison_region=None, threshold=0.95, enable_debug=False):

    rect = Rect.from_dict(comparison_region)

    comparator = ScreenComparator(
        region=rect.to_region_tuple(),
        threshold=threshold
    )

    if enable_debug:
        comparator.enable_debug_mode()

    comparator.register_expected()
    return comparator

def execute_click_sequence(config_file):

    global enter_exit_sequence

    config_instance = Config(config_file)
    steps = config_instance.get_steps()
    loop_count = config_instance.get_loop_count()
    comparison_region = config_instance.get_comparison_region()
    standby_position = config_instance.get_standby_position()
    comparison_threshold = config_instance.get_comparison_threshold()
    retry_delay = config_instance.get_retry_delay_seconds()
    post_sequence_delay = config_instance.get_post_sequence_delay_seconds()
    screen_verification_enabled = config_instance.is_screen_verification_enabled()

    if screen_verification_enabled:
        comparator = register_expected_area(
            comparison_region=comparison_region,
            threshold=comparison_threshold,
            enable_debug=False
        )
    else:
        comparator = None
        log_message("Screen verification is disabled. Repeating steps without comparison.")

    if loop_count <= 0:
        log_message("Loop count is set to 0 or less. Exiting click sequence default value(1).")
        loop_count = 1

    for count in range(1, loop_count + 1):
        if enter_exit_sequence:
            log_message("Exit requested. Stopping click sequence...")
            return

        log_message(f"Starting click sequence... ({count})")
        execute_click(steps)
        time.sleep(post_sequence_delay)

        if comparator is None:
            continue

        while True:
            if comparator.compare():
                log_message("Screen matches expected area. Continuing...")
                break
            else:
                log_message("Screen does not match expected area. Clicking and retrying...")
                execute_single_click(standby_position["x"], standby_position["y"])
                time.sleep(retry_delay)

    log_message("Click sequence completed.")
    enter_exit_sequence = True
    
def exit_program():
    global enter_exit_sequence
    
    log_message("Exiting the program.")
    enter_exit_sequence = True

if __name__ == "__main__":
  
    # get commandline arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <argument>")
        sys.exit(1)

    keydownlistener = EscDownListener(exit_program)

    # start observe input thered
    keyboard_thread = threading.Thread(target=keydownlistener.watch_keyboard)
    keyboard_thread.daemon = True
    keyboard_thread.start()

    argument = sys.argv[1]
    
    if argument == "exec":

        config_file = sys.argv[2] if len(sys.argv) > 2 else "data/config.json"
        
        click_thread = threading.Thread(
            target=execute_click_sequence,
            args=(config_file,)
        )
        click_thread.daemon = True
        click_thread.start()
        
        while not enter_exit_sequence:
            time.sleep(1)

    elif argument == "show":
        show_mouse_position()
    else:
        print("unknown options...")
        
        
