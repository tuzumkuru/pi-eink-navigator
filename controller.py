import time
import RPi.GPIO as GPIO
import threading
import queue

class ScreenController:
    def __init__(self, screens, display, button_prev_pin, button_next_pin):
        self.screens = screens
        self.display = display
        self.current_screen_index = 0
        self.button_prev_pin = button_prev_pin
        self.button_next_pin = button_next_pin
        self.button_queue = queue.Queue()
        self.transition_in_progress = False  # Flag to indicate a screen transition in progress
        self.image_refresh_requested = False    #A flag to inform the process that image has been changed

        # Register the controller as the screen change callback
        for screen in self.screens:
            screen.on_change(self.screen_changed_callback)

        # Add event listeners for buttons
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_prev_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_next_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_prev_pin, GPIO.FALLING, callback=self.button_prev_callback, bouncetime=200)
        GPIO.add_event_detect(self.button_next_pin, GPIO.FALLING, callback=self.button_next_callback, bouncetime=200)

        # Activate the initial screen
        self.activate_screen(self.current_screen_index)

        # Create a thread to process the button queue continuously
        self.is_running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def __del__(self):
        self.is_running = True
        if(self.thread):
            self.thread.join()


    def button_prev_callback(self, channel):
        if not self.transition_in_progress:
            self.button_queue.put(self.button_prev_pin)

    def button_next_callback(self, channel):
        if not self.transition_in_progress:
            self.button_queue.put(self.button_next_pin)

    def loop(self):
        while self.is_running:
            if not self.button_queue.empty():
                channel = self.button_queue.get()
                if channel == self.button_prev_pin:
                    self.prev_screen(channel)
                elif channel == self.button_next_pin:
                    self.next_screen(channel)
            elif self.image_refresh_requested:
                self.image_refresh_requested = False
                image = self.screens[self.current_screen_index].get_image()
                self.display_image(image)
            else:
                time.sleep(0.1)

    def prev_screen(self, channel):
        if not self.transition_in_progress:
            # self.transition_in_progress = True
            new_index = (self.current_screen_index - 1) % len(self.screens)
            self.deactivate_screen(self.current_screen_index)
            self.activate_screen(new_index)
            # self.transition_in_progress = False

    def next_screen(self, channel):
        if not self.transition_in_progress:
            # self.transition_in_progress = True
            new_index = (self.current_screen_index + 1) % len(self.screens)
            self.deactivate_screen(self.current_screen_index)
            self.activate_screen(new_index)
            # self.transition_in_progress = False

    def activate_screen(self, screen_index):
        self.screens[screen_index].activate()
        self.current_screen_index = screen_index
        image = self.screens[screen_index].get_image()
        self.display_image(image)

    def deactivate_screen(self, screen_index):
        self.screens[screen_index].deactivate()

    def screen_changed_callback(self):
        # This function will be called when a screen changes
        self.image_refresh_requested = True
        

    def display_image(self, image):
        self.transition_in_progress = True
        self.display.image(image)
        self.display.display()
        self.transition_in_progress = False
        
