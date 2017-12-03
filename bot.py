from music_library import YoutubeLibrary
import subprocess
import tracery
from tracery.modifiers import base_english
import json
import secrets


# Use sox utility to add muffled effect to audio
# TODO: investigate volume levels
def muffle(audio_file):
    output = subprocess.run([
        'bin/muffle',
        audio_file
    ], stdout=subprocess.PIPE)

    return output.stdout.decode('utf8')


def create_video(audio_file, thumbnail):
    output = subprocess.run([
        'bin/create-video',
        thumbnail,
        audio_file
    ], stdout=subprocess.PIPE)

    return output.stdout.decode('utf8')


# Flatten tracery grammar to tweet text, then use format to insert
# song title and author
def generate_tweet_text(rules, info):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten('#origin#').format(**info)


if __name__ == '__main__':
    library = YoutubeLibrary(secrets.youtube_api_key)
    song = library.get_random_song()
    muffled_song = muffle(song['audio_file'])
    video = create_video(muffled_song)
    with open('grammar.json', 'r') as f:
        tweet_text = generate_tweet_text(json.load(f), song['info'])
        print(tweet_text)


#TODO:
# improve error handling (requests, lengths, etc.). retry stuff
# improve artist/title gathering
# delete files (either in code or via cron)
# add tweeting
# finish tests
# add interactivity (tweet: @anotherroombot can you play "keywords")
