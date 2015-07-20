import subprocess
import logging
import os
import datetime

# FFMPEG command--still dealing with deprecated pixel format issues:
#ffmpeg -r 24 -i img%05d.jpg -vf scale=640:480 -c:v libx264 -pix_fmt yuv420p testMovie.mp4

logDir = '../timelapseScratch/'
imageDir = '../timelapseScratch/imgFiles/'
tmpDir = '../timelapseScratch/tmpFiles/'

ffmpegCmd = ['ffmpeg', '-r', '24', '-i', tmpDir + 'img%05d.jpg', '-vf', 'scale=640:480', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', logDir + 'testMovie.mp4']

now = datetime.datetime.now()
dateString = now.strftime("%Y_%m_%d__%H%M")

# set up logging
logFile = logDir + 'log' + dateString + '.txt'
logging.basicConfig(filename = logFile, level=logging.DEBUG)
print('Logging file information to ' + logFile)
logging.info('Time of operation: ' + now.strftime("%Y/%m/%d, %H:%M:%S"))
logging.info('\tOld filename to new filename:')
filecount = 0

fileDictionary = {}

# create temporary folder for symbolic links
if not os.path.exists(tmpDir):
	os.makedirs(tmpDir)

# run through existing files
for fn in os.listdir(imageDir):
	if fn.endswith ('.jpg'):
		# TODO: test for brightness

		print ("Number " + str(filecount) + ": " + fn)
		# save the path name for original image file
		origName = imageDir + fn

		# create 5-digit numeric names
		tmpName = str(filecount).zfill(5)
		tmpName = 'img' + tmpName + '.jpg'

		# log tmpNames with original names
		print('temporary name: ' + tmpName)
		logging.info('\t' + fn + '\t\t' + tmpName)

		# create symbolic links using numeric names
		dest = tmpDir + '/' + tmpName
		os.symlink(os.path.abspath(origName), os.path.abspath(dest))

		filecount += 1
	else:
		print ("Not a jpg file: " + fn)

# Do FFMPEG magic
subprocess.call(ffmpegCmd)

# unlink the symbolic links
for link in os.listdir(tmpDir):
	os.unlink(tmpDir + link)

# delete empty folder
os.rmdir(tmpDir)
