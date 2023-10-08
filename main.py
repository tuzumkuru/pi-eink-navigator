# main.py
import time
import board
import busio
import digitalio
from screen1 import Screen1
from screen2 import Screen2
from controller import ScreenController
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from screen_photo import PhotoScreen

if __name__ == "__main__":
    button1_pin = 6 
    button2_pin = 5 

    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    ecs = digitalio.DigitalInOut(board.CE0)
    dc = digitalio.DigitalInOut(board.D22)
    rst = digitalio.DigitalInOut(board.D27)
    busy = digitalio.DigitalInOut(board.D17)

    display = Adafruit_SSD1680(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy)

    # Set the display rotation to 270 degrees
    display.rotation = 3

    screen1 = PhotoScreen("./1.png")
    screen2 = PhotoScreen("./2.png")
    screen3 = PhotoScreen("./3.jpg")
    screen4 = Screen1()
    screens = [screen1, screen2, screen3, screen4]

    controller = ScreenController(screens, display, button1_pin, button2_pin)

    try:
        while True:
            time.sleep(1)  # You can add any other main program logic here
    finally:
        print("Exiting") 
