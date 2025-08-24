from pynput import keyboard
from datetime import datetime

class EscDownListener:
    def __init__(self, on_esc_keydown_callback=None):
        self.x = 0
        self.y = 0
        self.listener = None
        self.pressed_esc = False
        self.on_esc_keydown_callback = on_esc_keydown_callback
                
    def __enter__(self):
        self._log_message("Listener: Entering the context")
        self.listener = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._log_message("Listener: Exiting the context")

    def on_press(self, key):
        try:
            if key == keyboard.Key.esc:
                self._log_message("ESC key pressed. Stopping listener.")
                self.pressed_esc = True
                self.listener.stop()
                if self.on_esc_keydown_callback:
                    self._log_message("Calling the ESC keydown callback.")
                    self.on_esc_keydown_callback()
                    
        except Exception as e:
            self._log_message(f"Error: {e}")

    def watch_keyboard(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()
        
    def _log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")