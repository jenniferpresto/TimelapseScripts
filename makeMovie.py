import subprocess
import logging
import os
import datetime

# FFMPEG command--still dealing with deprecated pixel format issues:
#ffmpeg -r 24 -i img%05d.jpg -vf scale=640:480 -c:v libx264 -pix_fmt yuv420p testMovie.mp4

origDir = 'imgFileTest/'
tmpDir = 'tmpFiles/'

ffmpegCmd = ['ffmpeg', '-r', '24', '-i', tmpDir + 'img%05d.jpg', '-vf', 'scale=640:480', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'testMovie.mp4']

now = datetime.datetime.now()
dateString = now.strftime("%Y_%m_%d__%H%M")
logFile = 'log' + dateString + '.txt'

logging.basicConfig(filename = logFile, level=logging.DEBUG)
print('Logging file information to ' + logFile)
logging.info('\tOld filename to new filename:')
filecount = 0

fileDictionary = {}

# create temporary folder for symbolic links
if not os.path.exists(tmpDir):
	os.makedirs(tmpDir)

# run through existing files
for fn in os.listdir(origDir):
	if fn.endswith ('.jpg'):
		print ("Number " + str(filecount) + ": " + fn)
		# create 5-digit numeric names
		tmpName = str(filecount).zfill(5)
		tmpName = 'img' + tmpName + '.jpg'

		origName = origDir + fn

		# log tmpNames with original names
		print('temporary name: ' + tmpName)
		logging.info('\t' + fn + '\t\t' + tmpName)

		# # create dictionary
		# fileDictionary[tmpName] = fn

		# create symbolic links using numeric names
		dest = tmpDir + '/' + tmpName
		os.symlink(os.path.abspath(origName), os.path.abspath(dest))

		filecount += 1
	else:
		print ("Not a jpg file: " + fn)

# Do FFMPEG magic
subprocess.call(ffmpegCmd)




# # change filenames back
# for entry in fileDictionary:
# 	print(fn)
# 	print(fileDictionary[entry])

# for keyname in fileDictionary.keys():
# 	print(keyname)
# 	os.rename(keyname, fileDictionary[keyname])
