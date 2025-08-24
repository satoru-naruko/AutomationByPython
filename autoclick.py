
from config.config import Config
from lib.screen_comparator.screen_comparator import ScreenComparator
from lib.mouse_controller.mouse_controller import MouseController
from lib.esc_down_listener.esc_down_listener import EscDownListener

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
    
    for click_config in sorted(config, key=lambda x: x["index"]):

        x, y, delay_seconds = click_config["x"], click_config["y"], click_config["delay_seconds"]
        time.sleep(delay_seconds - 1 )

        move_mouse_to(x, y, duration=1.0)
        log_message(f"Move Mouse at ({x}, {y}) - Index: {click_config['index']}")
        time.sleep(1)

        click_at_position(x, y)
        log_message(f"Clicked at ({x}, {y}) - Index: {click_config['index']}")
        
def execute_single_click(x, y):
    click_at_position(x, y)
    log_message(f"Clicked at ({x}, {y})")
        
def register_expected_area(enable_debug=False):

    start_x = 2953
    start_y = 502
    end_x = 4072
    end_y = 735
    
    width = end_x - start_x
    height = end_y - start_y
    
    comparator = ScreenComparator(
        region=(start_x, start_y, width, height),
        threshold=0.95
    )
    
    if enable_debug:
        comparator.enable_debug_mode()
    
    comparator.register_expected()
    return comparator

def execute_click_sequence(config_file):
    config_instance = Config(config_file)
    steps = config_instance.get_steps()
    comparator = register_expected_area()
    
    for count in range(8):            
        log_message(f"Starting click sequence... ({count})")
        execute_click(steps)
        time.sleep(5)
        
        while True:
            if comparator.compare():
                log_message("Screen matches expected area. Continuing...")
                break
            else:
                log_message("Screen does not match expected area. Clicking and retrying...")
                execute_single_click(3490, 400)
                time.sleep(5)

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

        config_file = "data/click_config_20250824.json"
        
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
        
        
