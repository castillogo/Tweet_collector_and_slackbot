from config import config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
import pymongo

CLIENT = pymongo.MongoClient("mongodb")
DB = CLIENT.tweets

def authenticate():
    """Function for handling Twitter Authentication"""
    auth = OAuthHandler(config['consumer_key'], config['consumer_key_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #t is just a regular python dictionary.
        text_ext = 0
        if 'extended_tweet' in t:
            text_ext =  t['extended_tweet']['full_text']
        if 'retweeted_status' in t:
            r = t['retweeted_status']
            if 'extended_tweet' in r:
                text_ext =  r['extended_tweet']['full_text']
        tweet = {
        'text': text_ext,
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        DB.collections.tweets.insert_one(tweet)
        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')

    def on_error(self, status):

        if status == 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['corona'], languages=['en'])
