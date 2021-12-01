import tweepy
import csv

from textblob import TextBlob


consumer_key = 'a76nBj6z3L9YZudQUAYM5rH9K'
consumer_secret = 'Oxd42VMcm5ZZPoD3S9M97ek2T6pNlxosWO4dsmtPQuqPZmrWic'
access_token = '210015757-Gb93f5McEd3TJ5Uld5HI6wCqFJAfSN5evm4Ufzgi'
access_secret = 'J1qvgXGy7PdlBjXEz8TE9OWq77e0y2madnP4EQQPs82RZ'
tweetsPerQry = 100
maxTweets = 100000
hashtag = "business"


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

csvFile = open("user.csv","a+",newline="",encoding="utf-8")
csvWriter = csv.writer(csvFile)
i = []
u = []
ms = []


 
while tweetCount < maxTweets:
  if(maxId <= 0):
    newTweets = api.search_tweets(q=hashtag, count=tweetsPerQry, result_type="recent", tweet_mode="extended")
  else:
    newTweets = api.search_tweets(q=hashtag, count=tweetsPerQry, max_id=str(maxId - 1), result_type="recent", tweet_mode="extended")

  if not newTweets:
    print("Done")
    break

  for tweet in newTweets:
    id_tweet = tweet.id
    username = tweet.user.name
    media_source = tweet.source

    print(tweet.id, tweet.user.name)
   
    i.append(id_tweet)
    u.append(username)
    ms.append(media_source)
   
    tweets=[tweet.id, tweet.user.name, tweet.source]
    csvWriter.writerow(tweets)

    data_dict = {
    "id":i,
    "username":u,
    "media_source":ms
    }

 


