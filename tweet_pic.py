import yaml
import tweepy


def _config(filename):
    with open(filename) as f:
        data = yaml.load(f)
    return data

def tweet_auth(twitter_secret):
    config = _config(twitter_secret)
    consumer_token = config['APIKey']
    consumer_secret = config['APISecret']
    access_token = config['access_token']
    access_token_secret = config['access_token_secret']
    auth = tweepy.OAuthHandler(consumer_token,  consumer_secret)
    auth.secure = True
    auth.set_access_token( access_token,  access_token_secret)
    api = tweepy.API(auth)
    return api


def update_pic(api,status="", filename=None):

    api.update_with_media(status=status, filename=filename)
    print("Tweet a pic!")