from music_library import YoutubeLibrary
import os
import subprocess
import random
import tracery
import json


# Use sox utility to add muffled effect to audio
def muffle(infile, outfile):
    subprocess.run([
        'sox',
        infile,
        outfile,
        'reverb', '50', '50', '30',
        # run  audio through lowpass filters to cut out high frequencies which
        # are heavily attenuated by dense materials
        'lowpass', '200',
        'sinc', '-1k',
        # pan slightly to left or right by adjusting relative volumes
        'remix', '1p-{} 2'.format(random.randint(0, 3))
    ])
    return outfile


def create_video(audio_file, thumbnail, basename):
    outfile = basename + '.mp4'
    subprocess.run([
        'ffmpeg',
        '-i', thumbnail,
        '-i', audio_file,
        outfile,
    ])
    return outfile


# Flatten tracery grammar to tweet text, then use format to insert
# song title and author
def generate_tweet_text(rules, info):
    grammar = tracery.Grammar(rules).add_modifiers(tracery.base_english)
    return grammar.flatten('#origin#').format(info)


if __name__ == '__main__':
    library = YoutubeLibrary('AIzaSyACPLuKg4GhDLmvfJQ66dBHHi-o1kfkR5M')
    # library = YoutubeLibrary(os.environ['YOUTUBE_API_KEY'])
    song = library.getRandomSong()
    base, ext = os.path.splitext(song['filename'])
    muffled_song = muffle(song['filename'], base + '-muffled' + ext)
    video = create_video(muffled_song, base + '.jpg', base)
    with open('grammar.json', 'r') as f:
        tweet_text = generate_tweet_text(json.load(f), song['info'])
