import os
from dotenv import load_dotenv
import json
import time
import logging
import tweepy
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import dataset
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StreamListener(tweepy.StreamListener):
    def __init__(self, api, table):
        self.api = api
        self.table = table
        super().__init__()

    def on_status(self, status):
        if status.retweeted:
            return

        description = status.user.description
        location = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        user_name = status.user.screen_name
        user_created = status.user.created_at
        user_followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color

        blob = TextBlob(text)
        sentiment = blob.sentiment

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        try:
            self.table.insert(dict(
                user_description=description,
                user_location=location,
                coordinates=coords,
                text=text,
                geo=geo,
                user_name=user_name,
                user_created=user_created,
                user_followers=user_followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                polarity=sentiment.polarity,
                subjectivity=sentiment.subjectivity
            ))
        except Exception as error:
            logger.error("Error inserting tweet: %s", error)

    def on_error(self, status_code):
        if status_code == 420:
            return False


def init_db() -> dataset.Database:
    db = dataset.connect(os.getenv("CONNECTION_STRING"))
    table = db[os.getenv("TABLE_NAME")]
    return db, table


def init_twitter() -> tweepy.API:
    auth = tweepy.OAuthHandler(os.getenv("TWITTER_APP_KEY"), os.getenv("TWITTER_APP_SECRET"))
    auth.set_access_token(os.getenv("TWITTER_KEY"), os.getenv("TWITTER_SECRET"))
    api = tweepy.API(auth)
    return api


def export_tweets_to_csv(table):
    dataset.freeze(table.all(), format='csv', filename=os.getenv("CSV_NAME"))


def main():
    try:
        load_dotenv()

        # Check for essential environment variables
        required_env_vars = ["CONNECTION_STRING", "TABLE_NAME", "TWITTER_APP_KEY",
                             "TWITTER_APP_SECRET", "TWITTER_KEY", "TWITTER_SECRET", "TRACK_TERMS"]

        for var in required_env_vars:
            if not os.getenv(var):
                logger.error(f"Missing essential environment variable: {var}")
                return

        db, table = init_db()

        api = init_twitter()

        listener = StreamListener(api, table)

        stream = tweepy.Stream(auth=api.auth, listener=listener)

        track_terms = os.getenv("TRACK_TERMS").split(",")
        stream.filter(track=track_terms)

        scheduler = BackgroundScheduler()
        scheduler.add_job(export_tweets_to_csv, 'interval', args=[table], minutes=30)
        scheduler.start()

        while True:
            time.sleep(60)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Cleanup resources here if necessary
        pass


if __name__ == "__main__":
    main()
