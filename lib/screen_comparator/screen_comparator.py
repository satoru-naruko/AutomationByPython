import cv2
import numpy as np
from datetime import datetime
import os
import mss

class ScreenComparator:
    def __init__(self, region, threshold=0.95):
        """
        :param region: Capture region (x, y, width, height)
        :param threshold: Similarity threshold (0.0 ~ 1.0)
        :param debug_dir: Directory to save debug images
        """
        self.region = region
        self.threshold = threshold
        self.expected_image = None
        self.enable_debug = False 
        self.debug_dir = ""

    def enable_debug_mode(self, debug_dir="debug_capture_images"):
        """Enable debug mode and set the directory to save debug images"""
        self.enable_debug = True
        self.debug_dir = debug_dir
        os.makedirs(debug_dir, exist_ok=True)
        
    def _capture_region(self):
        """Capture the region using MSS (works for multi-monitor setups)"""
        x, y, w, h = self.region
        with mss.mss() as sct:
            monitor = {"left": x, "top": y, "width": w, "height": h}
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert BGRA to BGR

        # Save raw capture for debug
        if self.enable_debug:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_path = f"{self.debug_dir}/raw_capture_{ts}.png"
            cv2.imwrite(raw_path, img)
            print(f"[DEBUG] Raw capture saved: {raw_path}")

        return img

    def register_expected(self):
        """Capture the current region and store it as the expected image"""
        self.expected_image = self._capture_region()
        
        if self.enable_debug:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            expected_path = f"{self.debug_dir}/expected_{ts}.png"
            cv2.imwrite(expected_path, self.expected_image)
            print(f"[INFO] Expected image registered and saved: {expected_path}")

    def compare(self):
        """
        Capture the region and compare it with the expected image.
        Returns True if similarity >= threshold, otherwise False.
        """
        if self.expected_image is None:
            raise ValueError("Expected image is not registered. Call register_expected() first.")

        captured = self._capture_region()

        # Resize if shapes differ (usually should be the same)
        if captured.shape != self.expected_image.shape:
            expected_resized = cv2.resize(self.expected_image,
                                          (captured.shape[1], captured.shape[0]))
        else:
            expected_resized = self.expected_image

        # Compute similarity using template matching
        result = cv2.matchTemplate(captured, expected_resized, cv2.TM_CCOEFF_NORMED)
        similarity = result.max()
        print(f"[DEBUG] Similarity: {similarity:.4f}")

        if self.enable_debug:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            captured_path = f"{self.debug_dir}/captured_{ts}.png"
            expected_path = f"{self.debug_dir}/expected_resized_{ts}.png"
            cv2.imwrite(captured_path, captured)
            cv2.imwrite(expected_path, expected_resized)

            # Generate difference mask
            diff = cv2.absdiff(captured, expected_resized)
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, diff_mask = cv2.threshold(diff_gray, 50, 255, cv2.THRESH_BINARY)
            diff_path = f"{self.debug_dir}/diff_{ts}.png"
            cv2.imwrite(diff_path, diff_mask)

            print(f"[INFO] Debug images saved: {captured_path}, {expected_path}, {diff_path}")

        return similarity >= self.threshold
