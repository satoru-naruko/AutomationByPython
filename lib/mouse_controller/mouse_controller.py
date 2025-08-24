import pyautogui
from datetime import datetime
import time

class MouseController:
    def __init__(self):
        self.x = 0
        self.y = 0
        
        # Initialize and update current mouse position
        self.update_current_pos()

    def update_current_pos(self):
        """
        Update the current mouse position to self.x and self.y
        """
        try:
            self.x, self.y = pyautogui.position()
        except Exception as e:
            self._log(f"Error updating mouse position: {e}")

    def click(self, x=None, y=None):
        """
        Click at the specified coordinates. If coordinates are None, click at current position.
        Updates current position after click.
        """
        try:
            if x is not None and y is not None:
                x = int(x)
                y = int(y)
                pyautogui.click(x, y)

            else:
                pyautogui.click()
                
            self.update_current_pos()
        except Exception as e:
            self._log(f"Error clicking mouse: {e}")

    def move_to(self, x, y, duration=0.0):
        """
        Move the mouse from current position to specified coordinates.
        :param x: target X coordinate
        :param y: target Y coordinate
        :param duration: time in seconds for the movement
        """
        try:
            
            pyautogui.moveTo(x, y, duration)
            self.update_current_pos()
        except Exception as e:
            self._log(f"Error moving mouse: {e}")

    def move_from_to(self, start_x, start_y, end_x, end_y, duration=1.0, steps=100):
        """
        Move the mouse from point A to point B over a specified duration.
        Linear interpolation is used.
        :param start_x: starting X coordinate
        :param start_y: starting Y coordinate
        :param end_x: ending X coordinate
        :param end_y: ending Y coordinate
        :param duration: time in seconds for the movement
        :param steps: number of interpolation steps
        """
        try:
            for i in range(steps + 1):
                t = i / steps
                x = start_x + (end_x - start_x) * t
                y = start_y + (end_y - start_y) * t
                
                self.move_to(x, y)
                time.sleep(duration / steps)
            
            self.update_current_pos()
        except Exception as e:
            self._log(f"Error moving from point A to B: {e}")

    def _log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f"[{timestamp}] {message}")


# Example usage
# if __name__ == "__main__":
#     mouse = MouseController()
#     mouse.move_to(100, 100)                    # Move from current position to (100,100)
#     mouse.click()                               # Click at current position and update position
#     mouse.move_from_to(mouse.x, mouse.y, 500, 500, duration=2.0)  # Move over 2 seconds
