from music_library import YoutubeLibrary
import subprocess
import tracery
from tracery.modifiers import base_english
import json
import secrets
import tweepy
from twitter_bot import TwitterBot
# import logger


class AnotherRoomBot():
    def __init__(self, **kwargs):
        super.__init__(kwargs)
        self.logger = kwargs.get('logger', logger.Logger())
        try:
            self.library = kwargs['library']
            self.twitter_bot = kwargs['twitter_bot']
            self.library.register('error', self.log_error)
            self.twitter_bot.register('reply', self.tweet_song)
            self.twitter_bot.register('error', self.log_error)
        except KeyError as key:
            logger.log('{} is a required keyword argument in the'
                       ' AnotherRoomBot.__init__ constructor'.format(key))

    def run(self):
        # set up scheduler
        pass

    def tweet_random_song(self):
        song = library.get_random_song()
        muffled_song = self.muffle(song['audio_file'])
        video = self.create_video(muffled_song)
        text = self.generate_tweet_text(song['info'])

        # self.twitter_bot.send_media_tweet(text, video)

    # Use sox utility to add muffled effect to audio
    # TODO: investigate volume levels
    def muffle(self, audio_file):
        output = subprocess.run([
            'bin/muffle',
            audio_file
        ], stdout=subprocess.PIPE)

        return output.stdout.decode('utf8')

    def create_video(self, audio_file, thumbnail):
        output = subprocess.run([
            'bin/create-video',
            thumbnail,
            audio_file
        ], stdout=subprocess.PIPE)

        return output.stdout.decode('utf8')

    # Flatten tracery grammar to tweet text, then use format to insert
    # song title and author
    def generate_tweet_text(self, info):
        with open('grammar.json', 'r') as f:
            rules = json.load(f)
        grammar = tracery.Grammar(rules)
        grammar.add_modifiers(base_english)
        return grammar.flatten('#origin#').format(**info)


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(
        secrets.twitter.consumer_key,
        secrets.twitter.consumer_secret
    )
    auth.set_access_token(
        secrets.twitter.access_token,
        secrets.twitter.access_token_secret
    )
    bot = AnotherRoomBot(
        library=YoutubeLibrary(secrets.youtube_api_key),
        twitter_bot=TwitterBot(api=tweepy.API(auth)),
    )
    bot.run()


# TODO:
# improve error handling (requests, lengths, etc.). retry stuff
# implement artist/title gathering
# delete files (either in code or via cron)
# add tweeting
# finish tests
# add interactivity (tweet: @anotherroombot can you play "keywords")
