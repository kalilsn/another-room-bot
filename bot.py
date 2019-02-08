import secrets
import tweepy
from write_tweet import write_random_tweet

account = tweepy.OAuthHandler(
                    secrets.twitter_consumer_key,
                    secrets.twitter_consumer_secret
                    )

account.set_access_token(
                    secrets.twitter_access_token,
                    secrets.twitter_access_token_secret
                    )
bot = tweepy.API(account)

tweet = write_random_tweet()
print("Send tweet:\n" + tweet['text'] + "\nwith video at " + tweet['video'])

# media = bot.upload_chunked(tweet['video'])
# bot.update_status(status=tweet['text'], media_ids=[media.media_id])
# bot.update_status(tweet['text'])

# TODO
# Clean up files in tweet_media
# Add support for specifying song
# Tweet videos directly!
# Cut of random first few seconds of songs?
# Host this somewhere and running on its own
