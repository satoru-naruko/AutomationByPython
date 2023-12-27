from pynput import keyboard
import pyautogui
import time
import threading

exit_flag = False

def show_mouse_position():
    try:
        while True:
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

def on_press(key):
    global exit_flag
    try:
        if key == keyboard.Key.esc:
            exit_flag = True
    except Exception as e:
        print(f"Error: {e}")

def watch_keyboard():
    # create keyboard lestner 
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    # start observe input thered
    keyboard_thread = threading.Thread(target=watch_keyboard)
    keyboard_thread.daemon = True  # デーモンスレッドに設定
    keyboard_thread.start()

    # クリックしたい座標
    posX = 4980
    posY = 796

    click_at_position(posX, posY)

    for _ in range(500):
        if exit_flag:
            exit(0)

        click_at_position(posX, posY)
        time.sleep(2)

    # show_mouse_position()

    # wait end of the keyboatd thread 
    keyboard_thread.join()