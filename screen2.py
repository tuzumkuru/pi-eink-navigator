# screen2.py
from screen_base import ScreenBase
from PIL import Image, ImageDraw
import threading
import time

class Screen2(ScreenBase):
    def __init__(self):
        super().__init__()
        self.image = Image.new("L", (250, 122), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.text = "Screen 2"
        self.active = False
        self.process_thread = None

    def get_image(self):
        self.draw.rectangle((0, 0, 250, 122), outline=0, fill=0)
        self.draw.text((10, 10), self.text, fill=255)
        return self.image

    def set_text(self, text):
        self.text = text

    def activate(self):
        super().activate()
        self.active = True
        self.process_thread = threading.Thread(target=self.run)
        self.process_thread.daemon = True
        self.process_thread.start()

    def deactivate(self):
        super().deactivate()
        self.active = False
        if self.process_thread:
            self.process_thread.join()  # Wait for the process to finish

    def run(self):
        while self.active:
            time.sleep(5)  # Update content every minute
            self.notify_change()  # Notify the controller of the change
