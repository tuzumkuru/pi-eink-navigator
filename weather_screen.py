from datetime import datetime
import json
import threading
import time
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageOps
from screen_base import ScreenBase
from utils import get_text_size

small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
icon_font = ImageFont.truetype("./meteocons.ttf", 48)

DATA_SOURCE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Map the OpenWeatherMap icon code to the appropriate font character
# See http://www.alessioatzeni.com/meteocons/ for icons
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class WeatherScreen(ScreenBase):
    def __init__(self, weather_api_token, location, width=250, height=122, am_pm=True, unit="C"):
        super().__init__()
        self.active = False

        self.api_token = weather_api_token
        self.location = location

        self.width = width
        self.height = height

        self.am_pm = am_pm
        self.unit = unit
        
        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font

        self._weather_icon = None
        self._city_name = None
        self._main_text = None
        self._temperature_text = None
        self._description = None
        self._time_text = None

        self._last_weather_refresh = None

        self.image = None

        self.process_thread = None

        self.update_time()
        self.update_weather()
        self.update_image()

    def __del__(self):
        self.deactivate()

    def get_image(self):
        # This method returns the image to be displayed on the screen
        if(self.image == None):
            self.update_image()
        return ImageOps.invert(self.image)
        
    
    def update_image(self):
        image = Image.new("RGB", (self.width, self.height), color=WHITE)
        draw = ImageDraw.Draw(image)        

        # Draw the city
        draw.text(
            (0, 0), self._city_name, font=self.medium_font, fill=BLACK,
        )

        # Draw the time
        (font_width, font_height) = get_text_size(self._time_text, medium_font)
        draw.text(
            (self.width-font_width, 0),
            self._time_text,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the Icon
        (font_width, font_height) = get_text_size(self._weather_icon, icon_font)
        draw.text(
            (
                5,
                (self.height-font_height)/2-8,
            ),
            self._weather_icon,
            font=icon_font,
            fill=BLACK,
        )

        next_text_x = 10 + font_width

        # Draw the main text
        (font_width, font_height) = get_text_size(self._main_text, large_font)
        draw.text(
            (next_text_x, self.height / 2 - font_height - 5),
            self._main_text,
            font=self.large_font,
            fill=BLACK,
        )

        # Draw the description
        (font_width, font_height) = get_text_size(self._description, small_font)
        draw.text(
            (next_text_x, self.height / 2 + 5),
            self._description,
            font=self.small_font,
            fill=BLACK,
        )

        # Draw the temperature
        (font_width, font_height) = get_text_size(self._temperature_text, large_font)
        draw.text(
            (
                (self.width - font_width)/2,
                self.height - font_height
            ),
            self._temperature_text,
            font=self.large_font,
            fill=BLACK,
        )

        self.image = image

    def update_weather(self):
        # Set up where we'll be fetching data from
        params = {"q": self.location, "appid": self.api_token}
        data_source = DATA_SOURCE_URL + "?" + urllib.parse.urlencode(params)

        response = urllib.request.urlopen(data_source)
        if response.getcode() == 200:
            weather = response.read()
            weather = json.loads(weather.decode("utf-8"))
            # set the icon/background
            self._weather_icon = ICON_MAP[weather["weather"][0]["icon"]]

            city_name = weather["name"] + ", " + weather["sys"]["country"]
            self._city_name = city_name

            main = weather["weather"][0]["main"]
            self._main_text = main

            temperature = weather["main"]["temp"] - 273.15  # its...in kelvin
            if self.unit == "C":
                self._temperature_text = "%d °C" % temperature
            elif self.unit == "F":
                self._temperature_text = "%d °F" % ((temperature * 9 / 5) + 32)
            else: 
                self._temperature_text = "%d °C | %d °F" % (temperature, (temperature * 9 / 5) + 32)

            description = weather["weather"][0]["description"]
            description = description[0].upper() + description[1:]
            self._description = description

            self._last_weather_refresh = time.monotonic()

    def update_time(self):
        now = datetime.now()
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

    def activate(self):
        super().activate()
        self.active = True
        self.process_thread = threading.Thread(target=self.run)
        self.process_thread.daemon = True
        self.process_thread.start()

    def deactivate(self):
        super().deactivate()
        self.active = False
        if self.process_thread:
            self.process_thread.join()  # Wait for the process to finish

    def run(self):
        while self.active:
            if (not self._last_weather_refresh) or (time.monotonic() - self._last_weather_refresh) > 300:
                self.update_weather()

            old_time_text = self._time_text            
            self.update_time()            
            if(old_time_text != self._time_text):
                self.update_image()
                self.notify_change()         
                   
            time.sleep(1)