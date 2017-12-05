from music_library import YoutubeLibrary
import unittest
import os


class YoutubeLibraryTests(unittest.TestCase):
    def setUp(self):
        self.dir = 'tmpdir'
        self.library = YoutubeLibrary('AIzaSyACPLuKg4GhDLmvfJQ66dBHHi-o1kfkR5M', self.dir)

    def test_get_random_video_id(self):
        video_id = self.library.get_random_video_id()
        self.assertRegex(video_id, r'[A-z0-9\-]{11}')

    def test_get_video_info(self):
        filename = self.dir + '/Ed Sheeran - Lego House [Official Video]-c4BLVznuWnU.mp3'
        info = self.library.get_video_info(filename)
        self.assertIn('title', info)
        self.assertIn('artist', info)
        self.assertEqual(info, {'title': 'Lego House', 'artist': 'Ed Sheeran'})
        info = self.library.get_video_info('Black Tambourine - For Ex-Lovers Only-Wva074MGZi8.mp3')
        self.assertEqual(info, {'title': 'For Ex-Lovers Only', 'artist': 'Black Tambourine'})

    def test_get_random_song(self):
        song = self.library.get_random_song()
        print(song)
        self.assertTrue(os.path.isfile(song['filename']))
        self.assertTrue(os.path.isfile(os.path.splitext(song['filename'])[0] + '.jpg'))

    def test_download_song(self):
        filename = self.library.download_song('https://www.youtube.com/watch?v=Wva074MGZi8')
        print(filename)
        self.assertTrue(os.path.isfile(filename))
        self.assertEqual(filename, os.path.join(self.dir, 'Black Tambourine - For Ex-Lovers Only-Wva074MGZi8.mp3'))

class TwitterBotTests(unittest.TestCase):
    def setUp(self):
        self.dir = 'tmpdir'
        self.library = YoutubeLibrary('AIzaSyACPLuKg4GhDLmvfJQ66dBHHi-o1kfkR5M', self.dir)

if __name__ == '__main__':
    unittest.main()
