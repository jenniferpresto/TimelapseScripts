###Timelapse scripts

Simplest--possibly the jenkiest--timelapse system ever created. Raspberry Pi is set up to take picture periodically. Once a day, the Mac downloads the prior day's pictures from the Raspberry Pi. The Python script goes through the images, removes the ones that are too dark (since the timelapse runs through the night, as well), and stitches the rest into a video.

More detailed readme to come.

* **simpleCam.sh**: Bash script set to run as cron job on Raspberry Pi
* **autoDownload.sh**: Logs into Raspberry Pi and downloads all pictures taken the prior day.
* **makeMovie.py**: Stitches still images together to mp4.
