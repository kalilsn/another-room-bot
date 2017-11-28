import requests
import random
import os
import youtube_dl
import subprocess
import re


class YoutubeLibrary():
    search_api_base_url = 'https://www.googleapis.com/youtube/v3/search'
    channel_api_base_url = 'https://www.googleapis.com/youtube/v3/channels'
    video_base_url = 'https://www.youtube.com/watch?v='
    channel = 'UC-9-kyTW8ZkZNDHQJ6FgpwQ'
    max_pages = 9
    max_results = 50

    def __init__(self, api_key, directory='.'):
        self.api_key = api_key
        self.directory = directory
        if not os.path.isdir(directory) and os.path.exists(directory):
            raise NotADirectoryError(directory)
        elif not os.path.exists(directory):
            os.makedirs(directory)

    def get_topic_ids(self):
        params = {
            'part': 'topicDetails',
            'id': self.channel,
            'key': self.api_key,
        }
        return requests.get(self.channel_api_base_url, params=params).json()['items'][0]['topicDetails']['topicIds']

    def get_random_song(self):
        video_id = self.get_random_video_id()
        video_url = self.video_base_url + video_id
        filename = self.download_song(video_url)
        return {'filename': filename, 'info': self.get_video_info(filename)}

    def get_random_video_id(self):
        params = {
            'part': 'snippet',
            'maxResults': self.max_results,
            'topicId': random.choice(self.get_topic_ids()),
            'type': 'video',
            'fields': 'nextPageToken',
            'key': self.api_key,
        }
        response = requests.get(self.search_api_base_url, params).json()
        next_page_token = response['nextPageToken']
        i = random.randint(0, self.max_pages)
        while (i > 0):
            params['pageToken'] = next_page_token
            next_page_token = requests.get(self.search_api_base_url, params).json()['nextPageToken']
            i -= 1
        params['fields'] = 'items/id/videoId'
        response = requests.get(self.search_api_base_url, params).json()
        return random.choice(response['items'])['id']['videoId']

    def download_song(self, url):
        # uses subprocess.run instead because 'finished' hook is executed before postprocessing 🙄
        args = [
            'youtube-dl',
            '-x',
            '--audio-format', 'mp3',
            '--write-thumbnail',
        ]
        if (self.directory):
            args.extend(['-o', os.path.join(self.directory, youtube_dl.DEFAULT_OUTTMPL)])
        args.append(url)
        subprocess.run(args)
        return os.path.join(self.directory, os.path.splitext(subprocess.run(['youtube-dl', '--get-filename', url], stdout=subprocess.PIPE).stdout.decode('utf8'))[0]) + '.mp3'

    def get_video_info(self, filename):
        artist, title = (x.strip().title() for x in os.path.basename(filename).split(' - ')[:2])
        title = re.match(r'([^(\[]*)([(\[])?', title).group(1)
        return {'artist': artist.strip(), 'title': title.strip()}
