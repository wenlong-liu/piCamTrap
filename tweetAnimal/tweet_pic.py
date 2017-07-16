import yaml
import tweepy


class TweetPic():
    def __init__(self,filename='config.yml'):
        with open(filename) as f:
            config = yaml.load(f)

        self.consumer_token = config['APIKey']
        self.consumer_secret = config['APISecret']
        self.access_token = config['access_token']
        self.access_token_secret = config['access_token_secret']
        self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
        self.auth.secure = True
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)

    def update_pic(self, status=status, media_ids=None ):

        self.api.update_with_media(status=status, medias_ids=media_ids)
        print("Tweet a pic!")