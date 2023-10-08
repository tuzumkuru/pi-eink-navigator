import RPi.GPIO as GPIO
import time

# Define GPIO pin numbers for your buttons
button1_pin = 5
button2_pin = 6

# Set up GPIO mode and initial settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    if channel == button1_pin:
        print("Button 1 pressed")
    elif channel == button2_pin:
        print("Button 2 pressed")

# Add event listeners for button presses
GPIO.add_event_detect(button1_pin, GPIO.FALLING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(button2_pin, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    while True:
        # Your main program logic can go here
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

# Clean up GPIO on program exit
GPIO.cleanup()
