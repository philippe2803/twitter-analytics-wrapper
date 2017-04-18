import random
import time
from datetime import datetime, timedelta


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


class TweetDateSelector(object):

    """
    Class to handle filtering by dates of the tweet to export to Google Spreadsheet
    DEPRECATED: NEW LOGIC IMPLEMENTED
    """

    def __init__(self, tweets, days=4):
        self.tweets = tweets
        self.date_limit = datetime.today() - timedelta(days=days)
        self.tweets_to_keep = self.date_filter_tweets()

    def date_filter_tweets(self):
        """
        Function to filter out tweets with a date within {{days}} of current date.
        :param tweets: List of tweets
        :param days: Number of days threshold (default is 4).
        :return: New list of tweets after filtering out tweets within days threshold
        """
        tweets_to_keep = list()
        for tweet in self.tweets:
            if self.tweet_date(tweet) > self.date_limit:
                continue
            tweets_to_keep.append(tweet)
        return tweets_to_keep

    @staticmethod
    def tweet_date(tweet):
        """
        Takes a tweet and return the date of the tweet in datetime format.
        :param tweet: List of values (index 3 is the date string)
        :return: datetime object of the tweet
        """
        date_string = tweet[3].split(' ')[0]
        tweet_date = datetime.strptime(date_string, '%Y-%m-%d')
        return tweet_date

