# main.py
import time
import board
import busio
import digitalio
from screen1 import Screen1
from screen2 import Screen2
from controller import ScreenController
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from photo_screen import PhotoScreen

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

    screens = []
    screens.append(PhotoScreen("./1.png"))
    screens.append(PhotoScreen("./2.png"))
    screens.append(PhotoScreen("./3.jpg"))
    screens.append(Screen1())
    screens.append(Screen2())

    controller = ScreenController(screens, display, button_prev_pin, button_next_pin)

    try:
        while True:
            time.sleep(1)  # You can add any other main program logic here
    finally:
        print("Exiting") 