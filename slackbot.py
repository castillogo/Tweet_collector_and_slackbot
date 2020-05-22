# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:48:35 2020

@author: casti
"""

import slack
import pyjokes
from sqlalchemy import create_engine

oauth_token = 'xoxb-944156563620-1029593474371-o7KS9Tn5un5Zz0XBB4mp9YHN'

client = slack.WebClient(token=oauth_token)

#CHALLENGE 2: REPEAT OFTEN
#repeat automatically
prev_tweet = ''
while True:
    #do the slack post
    tweet_result = pg.execute('''SELECT tweets."col1" FROM tweets LIMIT 1;''').fetchall()
    #logic to check if the tweet has already been posted, only post if its not already been posted
    if tweet_result != prev_tweet:
        prev_tweet = tweet_result
        response = client.chat_postMessage(channel='#zufällig', text=f"Here is a tweet we scraped: {tweet_result}")
    #delay for one minute
    time.sleep(60)
