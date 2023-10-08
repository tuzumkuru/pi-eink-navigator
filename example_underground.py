import os
from datetime import datetime
from underground import SubwayFeed
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("MTA_API_KEY")
print(API_KEY)
ROUTE = 'Q'
feed = SubwayFeed.get(ROUTE, api_key=API_KEY)


your_dict = feed.extract_stop_dict()

datetime_list = your_dict['Q']['D27S']

# Loop through the datetime values in the list
for dt in datetime_list:
    formatted_time = dt.strftime('%H:%M')  # Format as HH:MM
    print(formatted_time)

# Get the current time in the same timezone as datetime_list
current_time = datetime.now(datetime_list[0].tzinfo)  # Use the timezone from the first datetime object

# Initialize a list to hold remaining minutes
remaining_minutes_list = []

# Loop through the datetime values in the list
for dt in datetime_list:
    # Calculate the time difference
    time_difference = dt - current_time
    # Extract remaining minutes as an integer
    remaining_minutes = int(time_difference.total_seconds() / 60)
    remaining_minutes_list.append(remaining_minutes)

# Print the list of remaining minutes
for i, minutes in enumerate(remaining_minutes_list):
    print(f"Train {i + 1}: {minutes} minutes remaining")
