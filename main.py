import os
import time
import board
import busio
import digitalio
from screens.mta_screen import MTAScreen
from controller import ScreenController
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from screens.photo_screen import PhotoScreen
from screens.weather_screen import WeatherScreen
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    button_prev_pin = 6 
    button_next_pin = 5 

    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    ecs = digitalio.DigitalInOut(board.CE0)
    dc = digitalio.DigitalInOut(board.D22)
    rst = digitalio.DigitalInOut(board.D27)
    busy = digitalio.DigitalInOut(board.D17)

    display = Adafruit_SSD1680(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy)
    # Set the display rotation to 270 degrees
    display.rotation = 3

    # Create screens list to be navigated in the controller
    screens = []
    screens.append(PhotoScreen("./files/mountain.jpg"))
    screens.append(MTAScreen(os.environ.get("MTA_API_KEY"),os.environ.get("MTA_TRAIN_LINE"),os.environ.get("MTA_TRAIN_STOP")))
    screens.append(WeatherScreen(os.environ.get("OPEN_WEATHER_TOKEN"),os.environ.get("OPEN_WEATHER_CITY"),am_pm=False,unit="B"))

    controller = ScreenController(screens, display, button_prev_pin, button_next_pin)

    try:
        while True:
            time.sleep(1)  # You can add any other main program logic here
    finally:
        print("Exiting") 
