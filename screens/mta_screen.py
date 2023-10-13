import os
from datetime import datetime, timezone
from underground import SubwayFeed
import threading
import time
from PIL import Image, ImageDraw, ImageFont, ImageOps
from screen_base import ScreenBase
from utils import get_text_size

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define fonts
departure_time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
stop_name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
metro_line_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
clock_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)  

class MTAScreen(ScreenBase):
    def __init__(self, mta_api_token, route, stop, width=250, height=122):
        super().__init__()

        self.api_token = mta_api_token
        self.route = route
        self.stop = stop

        self.width = width
        self.height = height

        # Define fonts
        self.stop_name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        self.metro_line_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        self.clock_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)

        self._last_list_update = None
        self.remaining_minutes_list = None
        self.departure_time_list = None

        self.image = None

        self.process_thread = None

    def __del__(self):
        self.deactivate()

    def get_image(self):
        # This method returns the image to be displayed on the screen
        if(self.image == None): # for the first run
            self.update_list()
            self.update_image()
        return self.image
    
    def update_image(self):
        WHITE = (255, 255, 255)  # Color constant
        BLACK = (0, 0, 0)  # Color constant

        # Create a new image
        image = Image.new("RGB", (self.width, self.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Square bar for the stop name and clock
        bar_width = self.width
        bar_height = 30
        bar_color = BLACK
        bar_position = (0, 0)
        stop_name = self.stop  # TODO: Replace with your stop name instead of stop code

        draw.rectangle([bar_position, (bar_position[0] + bar_width, bar_position[1] + bar_height)], fill=bar_color, outline=None)

        # Calculate the position for the stop name on the left
        stop_position_left = (bar_position[0] + 5, bar_position[1] + (bar_height - get_text_size(stop_name, font=stop_name_font)[1]) // 2)

        # Calculate the position for the clock on the right
        current_time = datetime.now(self.departure_time_list[0].tzinfo)  # Use the timezone from the first datetime object
        current_time_str = current_time.strftime("%I:%M %p")  # Format time in 12-hour format
        clock_width, clock_height = get_text_size(current_time_str, font=clock_font)
        clock_position = (bar_position[0] + self.width - clock_width - 2, bar_position[1] + (bar_height - clock_height) // 2)        
        
        # Draw the clock and stop name        
        draw.text(stop_position_left, stop_name, font=self.stop_name_font, fill=WHITE)
        draw.text(clock_position, current_time_str, font=self.clock_font, fill=WHITE)

        # Metro line in a filled circle
        circle_radius = 36
        circle_color = BLACK 
        circle_position = (circle_radius + 10, (self.height - bar_height) // 2 + bar_height)        

        draw.ellipse([(circle_position[0] - circle_radius, circle_position[1] - circle_radius),
                    (circle_position[0] + circle_radius, circle_position[1] + circle_radius)],
                    fill=circle_color, outline=None)

        # Use get_text_size to calculate text size
        metro_line = self.route
        text_width, text_height = get_text_size(metro_line, font=metro_line_font)
        text_position = (circle_position[0] - text_width // 2, circle_position[1] - text_height // 2)
        draw.text(text_position, metro_line, font=self.metro_line_font, fill=WHITE)

        # Sort the list of datetime objects representing train departure times
        departure_times = sorted(self.departure_time_list)  

        # Calculate the remaining times and print in the desired format
        remaining_times_y = bar_position[1] + bar_height + 10

        for departure_time in departure_times[:4]:
            # Calculate the time difference
            time_difference = departure_time - current_time
            # Extract remaining minutes as an integer
            minutes = int(time_difference.total_seconds() / 60)
            departure_time_str = departure_time.strftime("%I:%M %p")  # Format as "hh:mm AM/PM"
            remaining_time_str = f"{minutes} min"  # Format as "X min"

            text_width, text_height = get_text_size(departure_time_str, font=self.clock_font)
            text_x = self.width - text_width -2 # Right-align the text
            draw.text((text_x, remaining_times_y), departure_time_str, font=self.clock_font, fill=BLACK)

            text_width, text_height = get_text_size(remaining_time_str, font=self.clock_font)
            text_x = circle_position[0] * 2  # Center the text horizontally
            draw.text((text_x, remaining_times_y), remaining_time_str, font=self.clock_font, fill=BLACK)

            remaining_times_y += text_height  # Move the Y position down       

        self.image = image

    def update_list(self):
        feed = SubwayFeed.get(self.route, api_key=self.api_token)
        date_time_list = feed.extract_stop_dict()[self.route][self.stop]

        # Get the current time in the same timezone as datetime_list
        current_time = datetime.now(date_time_list[0].tzinfo)  # Use the timezone from the first datetime object

        remaining_minutes_list = []

        # Loop through the datetime values in the list
        for dt in date_time_list:
            # Calculate the time difference
            time_difference = dt - current_time
            # Extract remaining minutes as an integer
            remaining_minutes = int(time_difference.total_seconds() / 60)
            remaining_minutes_list.append(remaining_minutes)
        self.remaining_minutes_list = remaining_minutes_list
        self.departure_time_list = date_time_list
        self._last_list_update = time.monotonic()

    def activate(self):
        super().activate()
        self.active = True
        self.get_image()
        self.process_thread = threading.Thread(target=self.run)
        self.process_thread.daemon = True
        self.process_thread.start()

    def deactivate(self):
        super().deactivate()
        self.active = False
        if self.process_thread:
            self.process_thread.join()  # Wait for the process to finish
        self.image=None # clear the image to avoid double change at activate

    def run(self):
        while self.active:
            info_change = False

            if (not self._last_list_update) or (time.monotonic() - self._last_list_update) > 15:
                old_date_time_list = self.departure_time_list
                self.update_list()
                if(old_date_time_list != None and set(self.departure_time_list) == set(old_date_time_list)):
                    info_change = True            
            
            if time.localtime().tm_sec == 0:
                info_change = True

            if info_change:
                self.update_image()
                self.notify_change()
                   
            time.sleep(1)