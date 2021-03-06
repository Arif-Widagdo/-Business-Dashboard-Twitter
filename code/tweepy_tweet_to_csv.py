import tweepy
import csv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert

from textblob import TextBlob
from nltk.corpus import stopwords
import re

consumer_key = 'a76nBj6z3L9YZudQUAYM5rH9K'
consumer_secret = 'Oxd42VMcm5ZZPoD3S9M97ek2T6pNlxosWO4dsmtPQuqPZmrWic'
access_token = '210015757-Gb93f5McEd3TJ5Uld5HI6wCqFJAfSN5evm4Ufzgi'
access_secret = 'J1qvgXGy7PdlBjXEz8TE9OWq77e0y2madnP4EQQPs82RZ'
tweetsPerQry = 100
maxTweets = 100000
hashtag = "business"


#clean tweet text
def clean_text(text):
  ex_list = ['rt', 'http', 'RT']
  exc = '|'.join(ex_list)
  text = re.sub(exc, ' ' , text)
  text = text.lower()
  words = text.split()
  stopword_list = stopwords.words('english')
  words = [word for word in words if not word in stopword_list]
  clean_text = ' '.join(words)
  return clean_text

def sentiment_score(text):
  analysis = TextBlob(text)
  if analysis.sentiment.polarity > 0:
    return 1
  elif analysis.sentiment.polarity == 0:
    return 0
  else:
    return -1

authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True)
maxId = -1
tweetCount = 0

csvFile = open("tweet.csv","a+",newline="",encoding="utf-8")
csvWriter = csv.writer(csvFile)
i = []
ca = []
tt = []
rc = []
fc = []
rs = []

 
while tweetCount < maxTweets:
  if(maxId <= 0):
    newTweets = api.search_tweets(q=hashtag, count=tweetsPerQry,lang="id", result_type="recent", tweet_mode="extended")
  else:
    newTweets = api.search_tweets(q=hashtag, count=tweetsPerQry,lang="id", max_id=str(maxId - 1),result_type="recent", tweet_mode="extended")

  if not newTweets:
    print("Done")
    break

  for tweet in newTweets:
    id = tweet.id
    created_at = str(tweet.created_at)
    tweet_text = tweet.full_text
    tweet_text_sent = tweet.full_text
    retweet_count = tweet.retweet_count
    fav_count = tweet.favorite_count
    tweet_text_sent = clean_text(tweet_text_sent)
    result_score = sentiment_score(tweet_text_sent)

    print(tweet.id, str(tweet.created_at), clean_text(tweet_text_sent), tweet.retweet_count, tweet.favorite_count, sentiment_score(tweet_text_sent))
    i.append(id)
    ca.append(created_at)
    tt.append(tweet_text)
    rc.append(retweet_count)
    fc.append(fav_count)
    rs.append(result_score)
    tweets=[tweet.id, str(tweet.created_at), clean_text(tweet_text_sent),tweet.retweet_count, tweet.favorite_count, sentiment_score(tweet_text_sent)]
    csvWriter.writerow(tweets)

    data_dict = {
    "id":i,
    "created_at":ca,
    "tweet_text":tt,
    "retweet_count":rc,
    "fav_count":fc,
    "semtiment_score":rs
    }

 

