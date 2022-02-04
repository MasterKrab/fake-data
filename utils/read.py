import re
from math import ceil

WORDS_PER_MINUTE = 255


def get_read_time(text, words_per_minute=WORDS_PER_MINUTE):
    words = re.findall("\w+", text)

    return ceil(len(words) / words_per_minute)
