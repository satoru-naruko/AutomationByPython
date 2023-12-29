from pynput import keyboard
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
        print(f"Click at Position: x = {x}, y = {y}")
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

        for i in range(2):
            centerX = 4582
            centerY = 820

            click_at_position(centerX, centerY)
            time.sleep(3)

        # クリックしたい座標
        posX = 4980
        posY = 796
        for _ in range(300):
            if exit_flag:
                exit(0)

            click_at_position(posX, posY)
            time.sleep(2)
    elif argument == "show":
        show_mouse_position()
    else:
        print("unknown options...")
