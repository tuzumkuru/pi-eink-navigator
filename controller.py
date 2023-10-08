# controller.py
import RPi.GPIO as GPIO

class ScreenController:
    def __init__(self, screens, display, button1_pin, button2_pin):
        self.screens = screens
        self.display = display
        self.current_screen_index = 0
        self.button1_pin = button1_pin
        self.button2_pin = button2_pin

        # Add event listeners for buttons
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        GPIO.add_event_detect(self.button1_pin, GPIO.FALLING, callback=self.prev_screen, bouncetime=200)
        GPIO.add_event_detect(self.button2_pin, GPIO.FALLING, callback=self.next_screen, bouncetime=200)

        # Activate the initial screen
        self.activate_screen(self.current_screen_index)

    def prev_screen(self, channel):
        print("Previous Screen")
        self.deactivate_screen(self.current_screen_index)
        self.current_screen_index = (self.current_screen_index - 1) % len(self.screens)
        self.activate_screen(self.current_screen_index)

    def next_screen(self, channel):
        print("Next Screen")
        self.deactivate_screen(self.current_screen_index)
        self.current_screen_index = (self.current_screen_index + 1) % len(self.screens)
        self.activate_screen(self.current_screen_index)

    def activate_screen(self, screen_index):
        self.screens[screen_index].activate()
        image = self.screens[screen_index].render()
        self.display.image(image)
        self.display.display()

    def deactivate_screen(self, screen_index):
        self.screens[screen_index].deactivate()
