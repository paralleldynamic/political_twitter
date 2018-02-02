
import tweepy
import json
from pymongo import MongoClient
from sys import argv

db = MongoClient('localhost', 27017).political_twitter
tokens = db.tokens.find_one({'name': 'tokens'})

accounts = ['@SenSanders']

consumer_key = tokens['consumer_key']
consumer_secret = tokens['consumer_secret']
access_token = tokens['access_token']
access_secret = tokens['access_secret']

def extract_tweets(handle):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    tweets = []
    
    tweet_batch = api.user_timeline(screen_name=handle,count=10)
    tweets.extend(tweet_batch)
    oldest = tweets[-1].id - 1

#    while len(tweet_batch) > 0:
#        tweet_batch = api.user_timeline(screen_name=handle,count=200,max_id=oldest)
#        tweets.extend(tweet_batch)
#        oldest = tweets[-1].id - 1
    return tweets

def save_tweets(tweets, db_name):
    collection = db[db_name]

    for tweet in tweets:
        tweet_data = json.dumps(tweet._json)
        collection.insert(tweet_data)

if __name__ == '__main__':
    tweets = extract_tweets('SenSanders')
    save_tweets(tweets, 'bernie_sanders')