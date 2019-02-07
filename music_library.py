import random
import os
import subprocess
import requests
import time
import billboard
from observable import Observable


class YoutubeLibrary(Observable):
    def __init__(self, api_key, directory='.'):
        super().__init__()
        self.api_key = api_key
        self.directory = directory
        if not os.path.isdir(directory) and os.path.exists(directory):
            raise NotADirectoryError(directory)
        elif not os.path.exists(directory):
            os.makedirs(directory)

    def get_random_song(self):
        """
        Get a random song.

        Get a random song from the billboard top 100 charts, then search for
        it on youtube, and download the audio and thumbnail.

        Returns:
            dict: {
                'basename': base name of the file without extension
                'info': song information as returned by get_random_song_info
            }
        """
        while True:
            info = self.get_random_song_info()
            try:
                return self.get_song(info)
            except KeyError:
                print('No results, trying again')

    def get_random_song_info(self):
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
        return info

    def get_video_id(self, query):
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
            'key': self.api_key,
            'fields': 'items/id/videoId',
        }).json()
        print(response)

        return response['items'][0]['id']['videoId']

    def download_audio(self, video_id):
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
        url = 'https://www.youtube.com/watch?v=' + video_id
        print('downloading ' + url)
        output = subprocess.run([
            'bin/download-song',
            url,
            self.directory], stdout=subprocess.PIPE)
        return output.stdout.decode('utf8')

    def get_song(self, info):
        query = '{artist} {title}'.format(**info)
        print('query: ' + query)
        video_id = self.get_video_id(query)
        basename = self.download_audio(video_id)

        return {
            'basename': basename,
            'audio_file': os.path.join(self.directory, basename + '.mp3'),
            'thumbnail': os.path.join(self.directory, basename + '.jpg'),
            'info': info,
        }
