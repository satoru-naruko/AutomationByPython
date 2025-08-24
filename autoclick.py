from pynput import keyboard
from config.config import Config
from lib.screen_comparator.screen_comparator import ScreenComparator
from lib.mouse_controller.mouse_controller import MouseController

import sys
import pyautogui
from datetime import datetime
import time
import threading

exit_flag = False
mouse = MouseController()

def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(f"[{timestamp}] {message}")

def show_mouse_position():
    global exit_flag
    
    try:
        while True:
            if exit_flag:
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

class EscDownListener:
    def __enter__(self):
        log_message("Listener: Entering the context")
        self.listener = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        log_message("Listener: Exiting the context")

    def on_press(self, key):
        global exit_flag
        try:
            if key == keyboard.Key.esc:
                log_message("ESC key pressed. Stopping listener.")
                self.listener.stop()
                exit_flag = True
        except Exception as e:
            log_message(f"Error: {e}")

    def watch_keyboard(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()

def execute_click(config):
    for click_config in sorted(config, key=lambda x: x["index"]):
        if exit_flag:
            exit(0)

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

if __name__ == "__main__":
  
      # get commandline arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <argument>")
        sys.exit(1)

    listener = EscDownListener()

    # start observe input thered
    keyboard_thread = threading.Thread(target=listener.watch_keyboard)
    keyboard_thread.daemon = True
    keyboard_thread.start()

    argument = sys.argv[1]
    
    if argument == "exec":

        config_file = "data/click_config_20250824.json"
        config_instance = Config(config_file)
        steps = config_instance.get_steps()
        print(steps)
        
        comparator = register_expected_area()
        
        for cound in range(8):
            log_message(f"Starting click sequence... ({cound})") 
            execute_click(steps)
            time.sleep(5)
            
            while True:
                if comparator.compare():
                    log_message("Screen matches expected area. Continuing...")
                    break  # Exit the loop when screen matches
                else:
                    log_message("Screen does not match expected area. Clicking and retrying...")
                    execute_single_click(3490, 400)
                    time.sleep(5)  # Wait before retrying

    elif argument == "show":
        show_mouse_position()
    else:
        print("unknown options...")
        
        
