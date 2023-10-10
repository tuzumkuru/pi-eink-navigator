from screen_base import ScreenBase
from PIL import Image

class PhotoScreen(ScreenBase):
    def __init__(self, image_url):
        super().__init__()
        self.image = Image.open(image_url)

    def get_image(self):
        return self.image.copy()

    def activate(self):
        super().activate()
        # Additional activation logic specific to PhotoScreen, if needed

    def deactivate(self):
        super().deactivate()
        # Additional deactivation logic specific to PhotoScreen, if needed
