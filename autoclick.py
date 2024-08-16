from pynput import keyboard
from config.config import Config
from lib.line_notificator.line_notificator import LineNotificater

import sys
import pyautogui
import time
import threading



exit_flag = False

def show_mouse_position():
    global exit_flag
    
    try:
        while True:
            if exit_flag:
                sys.exit(1)
            else:    
                x, y = pyautogui.position()
                print(f"Mouse Position: x = {x}, y = {y}")
                time.sleep(1) 
    except KeyboardInterrupt:
        print("\n keybord interrupt!!! exit... ")

def click_at_position(x, y):
    try:
        # 指定した座標にクリック
        pyautogui.click(x, y)
    except Exception as e:
        print(f"Error: {e}")

class EscDownListener:
    def __enter__(self):
        print("Listener: Entering the context")
        self.listener = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Listener: Exiting the context")

    def on_press(self, key):
        global exit_flag
        try:
            if key == keyboard.Key.esc:
                print("ESC key pressed. Stopping listener.")
                self.listener.stop()
                exit_flag = True
        except Exception as e:
            print(f"Error: {e}")

    def watch_keyboard(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()

def execute_click(config):
    for click_config in sorted(config, key=lambda x: x["index"]):
        if exit_flag:
            exit(0)

        x, y, delay_seconds = click_config["x"], click_config["y"], click_config["delay_seconds"]
        time.sleep(delay_seconds)
        click_at_position(x, y)
        print(f"Clicked at ({x}, {y}) - Index: {click_config['index']}")

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

        config_file = "data/click_config.json"
        config_instance = Config(config_file)
        click_config = config_instance.get_config()
        print(click_config)
        
        for _ in range(1):
            execute_click(click_config)
            time.sleep(1)
        
        notifier = LineNotificater()
        status = notifier.notify('Helloworld!')
        print('メッセージ送信結果:', status)

    elif argument == "show":
        show_mouse_position()
    else:
        print("unknown options...")
        
        
