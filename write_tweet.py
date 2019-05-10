import csv
import random
import json
import tracery
from tracery.modifiers import base_english
import requests
import subprocess
import os

media_directory = 'tweet_media'

def get_random_song_info():
    """
    Get a random song from top_songs.csv. Returns a dictionary of information
    about the selected song, for example:

        info = {
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
    print("Random song info: " + str(info))
    return info

# Flatten tracery grammar to tweet text, then use format to insert
# song title and author
def generate_tweet_text(info):
    with open('grammar.json', 'r') as f:
        rules = json.load(f)
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    tweet_text = grammar.flatten('#origin#').format(**info)

    if 'requester' in info.keys():
        tweet_text = "For " + info['requester'] + ": " + tweet_text

    print(tweet_text)
    return tweet_text

def get_youtube_id(query):
    """
    Search youtube for a query and return the first result.

    Args:
        query (str): The search query (ideally song title and artist)

    Returns:
        str: Youtube video ID, as in

    Raises:
        KeyError if no videos are returned for the given query
    """
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    response = requests.get(base_url, {
        'part': 'id',
        'maxResults': 1,
        'q': query,
        'key': os.environ['YOUTUBE_API_KEY'],
        'fields': 'items/id/videoId',
    }).json()
    print(response)
    youtube_id = response['items'][0]['id']['videoId']
    return youtube_id

def get_audio(youtube_id, directory):
    """
    Download audio from youtube.

    Runs bin/download-audio because the youtube-dl python module's
    'finished' hook is executed after the video downloads, but before
    postprocessing (in our case, separating the audio).

    Args:
        url (id): The youtube video's id.

    Returns:
        str: stdout from bin/download-song, which should be the youtube
        video title.

    """
    url = 'https://www.youtube.com/watch?v=' + youtube_id
    print('Downloading ' + url + "...")
    output = subprocess.run([
        'bin/download-audio',
        url,
        directory], stdout=subprocess.PIPE)
    return output.stdout.decode('utf8')

def download_song(info):
    query = '{artist} {title}'.format(**info)
    youtube_id = get_youtube_id(query)
    get_audio(youtube_id, media_directory)

    return {
        'youtube_id': youtube_id,
        'audio_file': os.path.join(media_directory, youtube_id + '.mp3'),
        'thumbnail': os.path.join(media_directory, youtube_id + '.jpg'),
        'info': info
    }

# Use sox utility to add muffled effect to audio
# TODO: investigate volume levels
def muffle(audio_file):
    output = subprocess.run([
        'bin/muffle',
        audio_file
    ], stdout=subprocess.PIPE)

    return output.stdout.decode('utf8')

def create_video(audio_file, thumbnail):
    audio_file = audio_file.strip()
    print("Audio file: " + audio_file)
    print("Thumbnail: " + thumbnail)
    output = subprocess.run([
        'bin/create-video',
        thumbnail,
        audio_file
    ], stdout=subprocess.PIPE)

    return output.stdout.decode('utf8')

def create_tweet_media(info):
    """
    Get video and generated text for a song randomly chosen from top_songs.csv
    """
    text = generate_tweet_text(info)
    song = download_song(info)
    muffled_song = muffle(song['audio_file'])
    video = create_video(muffled_song, song['thumbnail']).strip("\n")

    print("Creating tweet media......")
    print(video)
    print(text)

    return {
        'video': video,
        'text': text
    }

def write_tweet(info):
    """
    Get video and generated text for a song randomly chosen from top_songs.csv
    """
    if info == {}:
        info = get_random_song_info()

    return create_tweet_media(info)
    # except KeyError:
    #     print('No results, trying again')
