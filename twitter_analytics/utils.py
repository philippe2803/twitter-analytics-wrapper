import random
import time


def random_time_sleep(minim=4, maxim=9):
    """
    Function to make a time.sleep(x) with x being random each time to the 10th of a second.
    Useful to avoid being flagged as a scraper.

    :param minim: Minimum in secs
    :param maxim: Maximum in secs
    :return: Time sleep a random time.
    """
    choices = range(minim*10, maxim*10)
    choices = [float(x) / 10 for x in choices]
    return time.sleep(random.choice(choices))


def random_small_time_sleep(minim=3, maxim=8):
    """
    Function to make a time.sleep(x) with x being random each time to the 10th of a second.
    This is for small random sleep. Useful for daterange selector in a calendar.

    :param minim: Minimum in secs
    :param maxim: Maximum in secs
    :return: Time sleep a random time.
    """
    choices = [float(x) / 10 for x in range(minim, maxim)]
    return time.sleep(random.choice(choices))

