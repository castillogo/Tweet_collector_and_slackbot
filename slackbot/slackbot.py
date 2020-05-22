# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:48:35 2020

@author: casti
"""

import slack
#import pyjokes
from sqlalchemy import create_engine
import time

oauth_token = "insert your own token"

client = slack.WebClient(token=oauth_token)

#get a joke
#joke = pyjokes.get_joke()

#or get the results of the postgres tweet collection
# postgres_connection = ''
# pg = create_engine(postgres_connection)
#pg = create_engine('postgres://postgres:postgres@postgres:5432/postgres')
pg = create_engine('postgres://airflow:airflow@postgresdb:5432/airflow')
#tweet_result = pg.execute('''SELECT * FROM tweets LIMIT 1;''').fetchall()

#and post it
#response = client.chat_postMessage(channel='#zufällig', text=f"here is a tweet: {tweet_result}")

#SELECT (text) FROM tweets ORDER BY (id) DESC  LIMIT 1

counter=0
while True:
    tweet_result = pg.execute("""SELECT (text, sentiment) FROM tweets WHERE sentiment >0 ORDER BY (sentiment) DESC LIMIT 1;""").fetchall()
    #tweet_result = pg.execute("""SELECT (text) FROM tweets ORDER BY (id) DESC  LIMIT 1;""").fetchall()
    response = client.chat_postMessage(channel='#juanchatbot', text=f"This is the most positive corona related tweet of the last hours: {tweet_result}")
    counter = counter + 1
    time.sleep(30)
#counter=counter+1

#repeat automatically
# while True:
#     #do the slack post
#     time.sleep(60)
