import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pandas as pd
import json
import csv
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

ckey = ''
csecret = ''
atoken = ''
asecret = ''

def toDataFrame(tweets):
    # Convert to Dataframe
    DataSet = pd.DataFrame()

    DataSet['tweetID'] = [tweet.id for tweet in tweets]
    DataSet['tweetText'] = [tweet.text.encode('utf-8') for tweet in tweets]
    DataSet['tweetRetweetCt'] = [tweet.retweet_count for tweet in tweets]
    DataSet['tweetFavoriteCt'] = [tweet.favorite_count for tweet in tweets]
    DataSet['tweetSource'] = [tweet.source for tweet in tweets]
    DataSet['tweetCreated'] = [tweet.created_at for tweet in tweets]
    DataSet['userID'] = [tweet.user.id for tweet in tweets]
    DataSet['userScreen'] = [tweet.user.screen_name for tweet in tweets]
    DataSet['userName'] = [tweet.user.name for tweet in tweets]
    DataSet['userCreateDt'] = [tweet.user.created_at for tweet in tweets]
    DataSet['userDesc'] = [tweet.user.description for tweet in tweets]
    DataSet['userFollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    DataSet['userFriendsCt'] = [tweet.user.friends_count for tweet in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['userTimezone'] = [tweet.user.time_zone for tweet in tweets]
    DataSet['Coordinates'] = [tweet.coordinates for tweet in tweets]
    DataSet['GeoEnabled'] = [tweet.user.geo_enabled for tweet in tweets]
    DataSet['Language'] = [tweet.user.lang for tweet in tweets]
    tweets_place= []
    for tweet in tweets:
        if tweet.place:
            tweets_place.append(tweet.place.full_name)
        else:
            tweets_place.append('null')
    DataSet['TweetPlace'] = [i for i in tweets_place]
    return DataSet

OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret,'access_token_key':atoken, 'access_token_secret':asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
 
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
else:
    print " Scraping data now" # Enter lat and long and radius in Kms
    cursor = tweepy.Cursor(api.search, q='hello',geocode="-22.9122,-43.2302,1km",since= '2016-03-05',until='2016-03-08',lang='en')
    results=[]
    for item in cursor.items(1000): # Scrape 1000 tweets
            results.append(item)
        
    
    DataSet = toDataFrame(results)
    DataSet.to_csv('C:\\Users\\Vibhor Sehgal\\Desktop\\data.csv',index=False)