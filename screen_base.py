from abc import ABC, abstractmethod

class ScreenBase(ABC):
    def __init__(self):
        self.active = False
        self.change_callback = None

    @abstractmethod
    def get_image(self):
        pass

    @abstractmethod
    def activate(self):
        self.active = True

    @abstractmethod
    def deactivate(self):
        self.active = False

    def on_change(self, callback):
        self.change_callback = callback

    def notify_change(self):
        if self.change_callback:
            self.change_callback()
