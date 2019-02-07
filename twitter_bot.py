import tweepy
# from secrets import twitter
from observable import Observable

class TwitterBot(Observable, tweepy.StreamListener):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter(track=['twitter_api'], async_=True)

    def on_status(self, status):
        own_tweet = self.api.me().id == status.user.get('screen_name')
        if status.get('retweeted') or own_tweet:
            # Bail if status is a retweet or our own tweet
            return
