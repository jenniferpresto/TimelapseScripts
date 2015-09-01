import sys
import subprocess
import logging
import os
import datetime
from PIL import Image
from PIL import ImageStat


# FFMPEG command--still dealing with deprecated pixel format issues:
#ffmpeg -r 24 -i img%05d.jpg -vf scale=640:480 -c:v libx264 -pix_fmt yuv420p testMovie.mp4

def main():
	logDir = '../timelapseScratch/'
	imageDir = '/Users/SandlapperNYC/Desktop/timelapse/'
	# imageDir = '../timelapseScratch/imgFiles/'
	tmpDir = '../timelapseScratch/tmpFiles/'

	darknessThreshold = 30.0

	now = datetime.datetime.now()
	dateString = now.strftime("%Y_%m_%d_%H%M")
	timeString = now.strftime("%Y/%m/%d, %H:%M:%S")

	ffmpegCmd = ['ffmpeg', '-r', '24', '-i', tmpDir + 'img%05d.jpg', '-vf', 'scale=640:480', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', logDir + dateString + 'Movie.mp4']


	# set up logging
	logFile = logDir + dateString + 'Log.txt'
	logging.basicConfig( filename = logFile, level=logging.DEBUG )
	print('####Logging file information to ' + logFile)
	logging.info('Beginning operation: ' + timeString)
	logging.info('Original filename\tFrame\t\tBrightness')
	filecount = 0

	# create temporary folder for symbolic links
	if not os.path.exists(tmpDir):
		os.makedirs(tmpDir)

	# run through existing files
	print('####Analyzing images')
	for fn in os.listdir(imageDir):

		# Skip files that aren't jpgs
		if not fn.endswith('.jpg'):
			continue

		imageFilePath = imageDir + fn

		# Test brightness
		level = testBrightness(imageFilePath)
		# Print basic progress to console
		sys.stdout.write('#')
		sys.stdout.flush()
		# Skip image files that are too dark
		if level < darknessThreshold:
			logging.info(fn + '\tToo dark' + '\tLevel: ' + str(level))
			continue

		# create symbolic links so ffmpeg command will have sequential numeric filenames
		createLinks(imageFilePath, tmpDir, filecount)
		logging.info(fn + '\timg' + str(filecount).zfill(5) + '\tLevel: ' + str(level))

		filecount += 1

	# Do FFMPEG magic
	print('\n####Building video: Num frames: ' + str(filecount))
	subprocess.call(ffmpegCmd)

	# Remove temporary links and directory
	print('####Cleaning up')
	cleanUp(tmpDir)

	# Log final information
	endtime = datetime.datetime.now()
	elapsed = endtime - now
	logging.info('Ending operation: ' + datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
	logging.info('Elapsed time: ' + str(elapsed))
	print('####Complete.')

##################################
# Create symbolic links for the image files that work
##################################
def createLinks(filepath, tempdirectory, framenum):
	# create 5-digit numeric names
	tmpName = str(framenum).zfill(5)
	tmpName = 'img' + tmpName + '.jpg'

	# create symbolic links using numeric names
	dest = tempdirectory + tmpName
	os.symlink(os.path.abspath(filepath), os.path.abspath(dest))

##################################
# Test overall brightness of each image
# http://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
##################################
def testBrightness( img_file ):
	img = Image.open(img_file).convert('L')
	stat = ImageStat.Stat(img)
	return stat.rms[0]

##################################
# Erase symbolic links and temporary directory
##################################
def cleanUp(tempdirectory):
	# unlink the symbolic links
	for link in os.listdir(tempdirectory):
		os.unlink(tempdirectory + link)

	# delete empty folder
	os.rmdir(tempdirectory)


if __name__ == "__main__":
	main()
