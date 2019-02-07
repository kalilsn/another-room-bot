import json
import tracery
from tracery.modifiers import base_english
import csv
import random

def get_random_song_info():
    """
    Get a random song from top_songs.csv. Returns a dictionary of information
    about the selected song, for example:

        song['info'] = {
            'artist': 'Taylor Swift',
            'title': 'You Belong With Me',
            'year': '2008',
        }
    """
    with open('songs/top_songs.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        chosen_row = random.choice(list(reader))

    info = {
        'artist': chosen_row['artist'],
        'title': chosen_row['title'],
        'year': chosen_row['year'],
    }
    song = {'info':info}
    return song

def generate_tweet_text(info):
    with open('grammar.json', 'r') as f:
        rules = json.load(f)
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten('#origin#').format(**info)

song = get_random_song_info()
print(generate_tweet_text(song['info']))
