from datetime import datetime, time
from PIL import ImageFont

def get_text_size(text, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text).getbbox()[2]
    text_height = font.getmask(text).getbbox()[3] + descent

    return (text_width, text_height)

def print_time_elapsed(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        print(f"{start_time} - Starting {func.__name__}")
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = end_time - start_time
        print(f"{end_time} - Finished {func.__name__} took {execution_time.total_seconds():.4f} seconds to run")
        return result
    return wrapper
