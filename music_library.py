import random
import os
import subprocess
import requests
import time
import billboard


class YoutubeLibrary():
    def __init__(self, api_key, directory='.'):
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
        video_id = None
        while not video_id:
            try:
                info = self.get_random_song_info()
                print(info)
                query = '{artist} {title}'.format(**info)
                print('query: ' + query)
                video_id = self.get_video_id(query)
                print(video_id)
            except KeyError:
                print('no results, trying again')
                pass

        basename = self.download_song(video_id)
        return {
            'basename': basename,
            'audio_file': os.path.join(self.directory, basename + '.mp3'),
            'thumbnail': os.path.join(self.directory, basename + '.jpg'),
            'info': info,
        }

    def get_random_date(self, format='%Y-%m-%d'):
        """
        Generate a random date between the epoch and today.

        Based on https://stackoverflow.com/a/553320. Dates should be formatted
        as YYYY-MM-DD

        Args:
            format (str, optional): Output format as accepted by time.strftime.
            Defaults to %Y-%m-%d.

        Returns:
            Random date between the start and end date, formatted YYYY-MM-DD.
        """
        random_time = time.mktime(time.localtime()) * random.random()

        return time.strftime(format, time.localtime(random_time))

    def get_random_song_info(self):
        """
        Get a random song from the billboard hot 100.

        Only gets charts from after the epoch (hot 100 only started in 1958
        so ¯\_(ツ)_/¯). Uses https://github.com/guoguo12/billboard-charts.

        Returns:
            A dictionary of information about the selected song. Has all the
            properties of the ChartEntry object as keys (title, artist,
            peakPos, lastPos, weeks, rank) as well as billboardYear.
        """

        date = self.get_random_date()
        chart = billboard.ChartData('hot-100', date=date)
        entry = random.choice(chart)
        song = vars(entry)
        # Add the year from the randomly generated date to the dictionary
        song['billboardYear'] = date[:4]
        return song

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

    def download_song(self, video_id):
        """
        Download a song from youtube.

        Runs bin/download-song because the youtube-dl python module's
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

    def get_song_info(self, query):
        """
        Get information about a song.

        Uses the last

        Args:
            title (str): The youtube video's title.

        Returns:
            dict: Information about the song. For example:
            {
                'artist': 'Taylor Swift',
                'song': 'You Belong With Me'
            }

        TODO: Figure out a better way to get song information. Right now this
        strips everything after a ( or [ character, since videos often have
        (Original Video) in the title. Unfortunately this frequently loses
        information, since features are often in parentheses and (less often)
        song titles have parenthetical parts. Perhaps this could use a fuzzy
        matching song database service.
        """
