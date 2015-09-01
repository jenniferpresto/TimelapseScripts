###Timelapse scripts

Simplest--possibly the jenkiest--timelapse system ever created. Raspberry Pi is set up to take pictures periodically. Once a day, the Mac downloads the prior day's pictures from the Raspberry Pi. The Python script, which is run manually, goes through the images, removes the ones that are too dark (since the timelapse also runs through the night), and stitches the rest into a video.

More detailed readme to come.

* **simpleCam.sh**: Bash script set to run as cron job on Raspberry Pi
* **autoDownload.sh**: Logs into Raspberry Pi and downloads all pictures taken the prior day.
* **makeMovie.py**: Stitches still images together to mp4.
