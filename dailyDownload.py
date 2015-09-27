#!/usr/local/bin/python

import os
import paramiko

#################################################
# Daily job: download files, clean up if too full
#################################################

class dailyDownload():

	localImageDir = '/Users/SandlapperNYC/Desktop/timelapse'
	remoteImageDir = '/home/pi/camera/simpleCamPics'
	threshold = 78 # Percentage of use below which cleanup method will not run

	def __init__(self):
		self.logOntoRemote()
		self.iterateAllImgFiles()
		self.downloadNewFiles()

		# check if we're using too much space on Raspberry Pi
		capacityUsed = self.getUsePercentage()
		print 'Capacity used is : ', capacityUsed, '%'
		if (capacityUsed > self.threshold):
			self.eraseFiles()
		else:
			print 'Still plenty of space; not erasing files at this time'

		self.closeRemote()

		print 'Ta-dah!'

	##################################
	# Establish SSH connection
	##################################
	def logOntoRemote(self):
		self.sshClient = paramiko.SSHClient()
		self.sshClient.load_system_host_keys()
		self.sshClient.connect('10.0.1.11', username='pi')
		print 'Client connected: ', self.sshClient
		self.sftp = self.sshClient.open_sftp()

	##################################
	# Iterate over local and remote image directories
	##################################
	def iterateAllImgFiles(self):
		self.localFilenames = os.listdir(self.localImageDir)
		self.remoteFilenames = self.sftp.listdir(self.remoteImageDir)

	##################################
	# Download new files
	##################################
	def downloadNewFiles(self):
		print 'Checking for new files'
		count = 0
		for fn in self.remoteFilenames:
			if not fn in self.localFilenames:
				print 'Getting file', fn, 'from remote'
				self.sftp.get(self.remoteImageDir + '/' + fn, self.localImageDir + '/' + fn)
				count += 1
		if count == 0:
			print 'No new files to download'

	##################################
	# Get percentage of space used
	##################################
	def getUsePercentage(self):
		stdin, stdout, stderr = self.sshClient.exec_command('df -h')
		capacity = stdout.readlines()
		percentage = 0;
		for line in capacity:
			if line.startswith('rootfs'):
				information = line.rsplit(' ')
				for piece in information:
					if piece.endswith('%'):
						percentage = int(piece.split('%')[0])
		return percentage

	##################################
	# Erase files that exist locally
	##################################
	def eraseFiles(self):
		for fn in self.remoteFilenames:
			if fn in self.localFilenames:
				print fn, 'exists locally; removing from remote drive'
				self.sftp.remove(self.remoteImageDir + '/' + fn)
			else:
				print fn, 'does not exist locally. Keeping on remote drive.'

	##################################
	# Close remote connection
	##################################
	def closeRemote(self):
		self.sftp.close()
		self.sshClient.close()


if __name__ == "__main__":
	dailyDownload = dailyDownload();
