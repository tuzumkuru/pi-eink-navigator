from PIL import ImageFont

def get_text_size(text, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text).getbbox()[2]
    text_height = font.getmask(text).getbbox()[3] + descent

    return (text_width, text_height)