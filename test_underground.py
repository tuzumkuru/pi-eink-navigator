import os

from underground import SubwayFeed

API_KEY = os.getenv('MTA_API_KEY')
ROUTE = 'Q'
feed = SubwayFeed.get(ROUTE, api_key=API_KEY)

# request will read from $MTA_API_KEY if a key is not provided
feed = SubwayFeed.get(ROUTE)

your_dict = feed.extract_stop_dict()


datetime_list = your_dict['Q']['D27N']


# Loop through the datetime values in the list
for dt in datetime_list:
    formatted_time = dt.strftime('%H:%M')  # Format as HH:MM
    print(formatted_time)

