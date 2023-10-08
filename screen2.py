# screen2.py
from PIL import Image, ImageDraw
import threading
import time

class Screen2:
    def __init__(self):
        self.image = Image.new("L", (122, 250), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.text = "Screen 2"
        self.active = False
        self.process_thread = None

    def render(self):
        self.draw.rectangle((0, 0, 122, 250), outline=0, fill=255)
        self.draw.text((10, 10), self.text, fill=0)
        return self.image

    def set_text(self, text):
        self.text = text

    def activate(self):
        self.active = True
        self.process_thread = threading.Thread(target=self.run)
        self.process_thread.daemon = True
        self.process_thread.start()

    def deactivate(self):
        self.active = False
        if self.process_thread:
            self.process_thread.join()  # Wait for the process to finish

    def run(self):
        while self.active:
            time.sleep(1)  # Update content every minute
