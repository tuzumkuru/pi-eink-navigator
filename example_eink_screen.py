import os
import time
import urllib.request
import urllib.parse
import digitalio
import busio
import board
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from datetime import datetime
import json
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD
from dotenv import load_dotenv
load_dotenv()

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

display = Adafruit_SSD1680(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy)

# image = Image.new("L", (display.width, display.height), color=0)
# image = Image.open("./lele.jpg")
# print(str(image.width) + "X" + str(image.height))

# image.save("1.jpg")

# image = image.transpose(Image.Transpose.ROTATE_90)

# image = image.rotate(90)

# image.transpose(Image.Transpose.ROTATE_90)

# print(str(image.width) + "X" + str(image.height))

# image.save("2.jpg")

# image.save("./rotated.jpg")

# display.hardware_reset()

image = Image.open("2.png")
# image = image.transpose(Image.Transpose.ROTATE_90)
image=image.rotate(90,expand=True)
image.save("2.png")

# print(str(image.width) + "X" + str(image.height))
# display.image(image)
# display.display()