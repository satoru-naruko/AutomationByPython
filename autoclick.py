from pynput import keyboard
import pyautogui
import time
import threading

exit_flag = False

def show_mouse_position():
    try:
        while True:
            # 現在のマウス座標を取得
            x, y = pyautogui.position()
            print(f"Mouse Position: x = {x}, y = {y}")
            time.sleep(1)  # 1秒ごとに座標を表示
    except KeyboardInterrupt:
        print("\n終了します。")

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
        # キーボードが押されたときの処理
        if key == keyboard.Key.esc:
            exit_flag = True
    except Exception as e:
        print(f"Error: {e}")

def watch_keyboard():
    # キーボード監視用のリスナーを作成
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    # キーボード監視用のスレッドを開始
    keyboard_thread = threading.Thread(target=watch_keyboard)
    keyboard_thread.daemon = True  # デーモンスレッドに設定
    keyboard_thread.start()

    click_at_position(4949, 796)  # ここにクリックしたい座標を指定

    # 10回クリックする
    for _ in range(500):
        if exit_flag:
            exit(0)

        click_at_position(4980, 796)  # ここにクリックしたい座標を指定
        time.sleep(2)  # 10second wait

    # マウス座標の表示を開始
    # show_mouse_position()

    # キーボード監視スレッドが終了するまで待機
    keyboard_thread.join()