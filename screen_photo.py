from PIL import Image

class ScreenPhoto:
    def __init__(self, image_url):
        self.image = Image.open(image_url).convert("1").convert("L")
        self.active = False

    def render(self):
        return self.image

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False