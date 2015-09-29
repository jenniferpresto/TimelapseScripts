##Timelapse scripts

Simplest&mdash;possibly the jenkiest&mdash;timelapse system ever created

###Quick summary

This depends on two main cron jobs: One is a bash script that runs on the Raspberry Pi, causing it to take pictures periodically, currently every 20 minutes. The other is a Python script that runs on the Mac, causing it to download pictures from the Raspberry Pi.

These scripts are

* ```simpleCam.sh```: Takes pictures on Raspberry Pi
* ```dailyDownload.py```: Downloads the newest images from the Raspberry Pi and deletes images if the Raspberry Pi is too full

To make the movie itself, there is a Python script that must be run manually:

* ```makeMovie.py```: Stitches still images into an .mp4 file


Other files, mostly obsolete:

* ```autoDownload.sh```: Original bash script for downloading the prior day's photos. No longer used.
* ```cleanRemote.py```: Deletes files from the Raspberry Pi if they exist locally. This functionality has been folded into ```dailyDownload.py```, so no longer used on its own.
* ```countFiles.py```: Acts as a check, counting the number of files in a folder per day for a given range of days, making it easier to confirm that all pictures have been downloaded. If the number is other than 72 (the number when taking a picture every 20 minutes), the output is bold red. (Still a nice check).

###Seting up cron jobs

####Cron job on Raspberry Pi
**```simpleCam.sh```** lives on the Raspberry Pi. This takes a picture and names it with the date/time format YYYY-MM-DD_HHMM. Some other files in the system require this naming convention.

The script can go where you like: I have it in ```/home/pi/camera```.

Make it executable:

```chmod +x simpleCam.sh```

Set up the cronjob. Open the cron table for editing:

```sudo crontab -e ```

Add the schedule at the bottom. The schedule below runs the bash script to take a picture every 20 minutes. (See more information [here](https://www.raspberrypi.org/documentation/linux/usage/cron.md)).

```0,20,40 * * * * /home/pi/camera/simpleCam.sh 2>&1```

####Cron job on Mac
**```dailyDownload.py```** lives on the Mac. It is set run once a day. When run, it logs into the Raspberry Pi and downloads any new files in the designated directory. It also checks to see if the Raspberry Pi has gotten too full (currently at over 78% capacity). If so, it deletes files from that directory.

This also must be exectuable:

```chmod +x dailyDownload.py```

The command for editing differs from the Raspberry Pi:

```env EDITOR=nano crontab -e```

Set up the Mac cronjob for once a day:

```9 11 * * * /Users/SandlapperNYC/Development/RaspberryPi/TimelapseScripts/dailyDownload.py```

This runs the job at 11:09 am every day. I also have the Mac scheduled, under **System Preferences > Energy Saver > Schedule...**, to come on or wake up every day at 11:00am and shut down at 11:30am.

This script requires SSH keys between the Mac and the Raspberry Pi, so that the Mac doesn't have to enter a password to access the Raspberry Pi. Instructions are available [here](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md).

###Creating the movie

**```makeMovie.py```** creates the movie. It does the following steps:

* creates a temporary directory
* iterates over the folder with the timelapse images
* skips files without the .jpg extension
* skips .jpg files that are too dark
* for all others, it creates symbolic links in the temporary directory with sequential numerical names
* runs an ffmpeg command to create the movie and save it
* deletes the symbolic links
* deletes the temporary directory

###Cleaning up
```dailyDownload.py``` deletes files from the Raspberry Pi if the capacity used is over 78%.

But there are legacy methods of deleting files from the Raspberry Pi to free space.

**```cleanRemote.py```** goes through images in the Raspberry Pi directory. If they exist on the local drive, it removes them from the Raspberry Pi. It will do this only if the capacity used is over 78%.

And before I wrote ```cleanRemote.py```, this is what I did:

* Test the amount of disk space on the Raspberry Pi by SSH-ing in and running ```df -h``` from the command line. If space is getting tight, remove the image files (after they've downloaded to the Mac).

* Make sure the files have downloaded correctly. If you take a picture every 20 minutes, there should be 72 pictures per day. Use ```countFiles.py``` for this.

* Manually remove files without prompt:

	```rm <file> --force```

	For example, to remove all photos from September 2015, type

	```rm 2015-09-*.jpg --force```


**```countFiles.py```** checks all the pictures within a specific date range, and if there aren't 72 pictures, it prints that date in red. I think it's still a handy check:

![screenshot](images/countFilesScreenshot.png)

Run the script with the start and end dates using the -s and -e flags:

```python countFiles.py -s 2015-08-20 -e 2015-09-07```

