# Another Room Bot

## Dependencies

- Python 3.6.3
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
- [youtube-dl](https://github.com/rg3/youtube-dl/) – Command line program for downloading youtube videos
	- Mac:
	`brew install youtube-dl`
	- Linux:
	```bash
	sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
	sudo chmod a+rx /usr/local/bin/youtube-dl
	```
- [pip](https://pip.pypa.io/en/stable/) – Python package manager
	- [https://pip.pypa.io/en/stable/installing/](Installation instructions)
- Various PyPi packages
	- `pip install -r requirements.txt`
