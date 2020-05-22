'''
The module etl.py extracts twitter data from a MongoDB database, transforms it
and loads it into a PostgreSQL database.
Thanks to Stefan!
'''

import time
import logging
import random
import re
import pymongo
from sqlalchemy import create_engine, exc
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#CLIENT = pymongo.MongoClient("mongodb://mongodb:27017/")
CLIENT = pymongo.MongoClient("mongodb")
DB = CLIENT.tweets

DATABASE_UP = True

#PG = create_engine('postgres://postgres:postgres@postgresdb:5432/postgres')
PG = create_engine('postgres://airflow:airflow@postgresdb:5432/airflow')
PG.execute('''CREATE TABLE IF NOT EXISTS tweets (
id BIGSERIAL,
text VARCHAR(512),
sentiment NUMERIC
); TRUNCATE TABLE tweets;
''')

s = SentimentIntensityAnalyzer()

def extract():
    """gets a random tweet"""
    tweets = list(DB.collections.tweets.find())
    if tweets:
        t = random.choice(tweets)
#        logging.critical("random tweet: " + t['text'])
        return str(t['text'])
        #return t['text']


def transform(tweet):
    #here we will insert the sentiment analysis results
#    text = re.sub("'", "", tweet["text"])
    text = tweet
    sentiment = s.polarity_scores(tweet)
    sentiment = sentiment['compound']
    sentiment = str(sentiment)
#    logging.critical("sentiment: " + str(sentiment))
    result = [text, sentiment]
    return result

def load(tweet, sentiment):
#    PG.execute(f"""INSERT INTO tweets (text, sentiment) VALUES ('{tweet}'', {sentiment});""")
    PG.execute(f"""INSERT INTO tweets (text, sentiment) VALUES ('{tweet}', '{sentiment}');""")
#    logging.critical("tweet + sentiment written to PG")


#logging.critical("Hello from the ETL job")

while True:
    tweet = re.sub( r"[^a-zA-Z0-9]", " ", extract())
#    tweet = extract()
#    tweet = re.sub( r"[^a-zA-Z0-9\!\?\.\,\@\:\#\\]", " ", extract())
    if tweet:
        result = transform(tweet)
        load(result[0], result[1])
    time.sleep(20)
