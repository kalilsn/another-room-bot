# Another Room Bot

## Dependencies
Another room bot is built for Python 3.7 and uses [pipenv](https://github.com/pypa/pipenv) to manage python dependencies. To install these dependencies, run `pipenv install`. In addition to the python dependencies, there are a few os-level dependencies:

- [sox](http://sox.sourceforge.net/sox.html) – Audio processing utility
	- Mac:
	`brew install sox --with-lame`
	- Ubuntu:
	`sudo apt-get install sox libsox-fmt-all`
- [ffmpeg](https://www.ffmpeg.org/) – Video utility
	- Mac:
	`brew install ffmpeg`
	- Ubuntu:
	`sudo apt-get install ffmpeg`
- [jq](https://stedolan.github.io/jq/) - Command line JSON processor
  - Mac: `brew install jq`

## Song Corpus

- [angrbrd](https://github.com/angrbrd)'s [top500-playlist](https://github.com/angrbrd/top5000-playlist)
- Bea's top 2017 and 2018 Spotify playlists
