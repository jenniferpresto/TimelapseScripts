#!/bin/bash
YESTERDAY=$(date -v-1d +"%Y-%m-%d")
echo $YESTERDAY
scp pi@10.0.1.11:/home/pi/camera/simpleCamPics/$YESTERDAY* /Users/SandlapperNYC/Desktop/timelapse
