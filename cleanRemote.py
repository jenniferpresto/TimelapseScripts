import os
import sys
import paramiko

def main():
	localImageDir = '/Users/SandlapperNYC/Desktop/timelapse'
	remoteImageDir = '/home/pi/camera/simpleCamPics'

	# Percentage of use below which script will not run
	threshold = 78

	# establish ssh connection
	sshClient = paramiko.SSHClient()
	sshClient.load_system_host_keys()
	sshClient.connect('10.0.1.11', username='pi')

	print 'Client connected: ', sshClient

	#See if the drive is low on space
	capacity = getUsePercentage(sshClient)
	print 'Capacity used on remote drive:', capacity, '%'

	if (capacity < threshold):
		print 'The capacity used is not high enough to remove files.'
		sshClient.close()
		return

	sftp = sshClient.open_sftp()

	# Compare remote and local directories
	localFilenames = os.listdir(localImageDir)
	remoteFilenames = sftp.listdir(remoteImageDir)
	for fn in remoteFilenames:
		if fn in localFilenames:
			print fn, 'exists locally; removing from remote drive'
			sftp.remove(remoteImageDir + '/' + fn)
		else:
			print fn, 'does not exist locally. Keeping on remote drive.'


	sftp.close()
	sshClient.close()



##################################
# Get percentage of space used
##################################
def getUsePercentage(sshClient):
	stdin, stdout, stderr = sshClient.exec_command('df -h')
	capacity = stdout.readlines()
	percentage = 0;
	for line in capacity:
		if line.startswith('rootfs'):
			information = line.rsplit(' ')
			for piece in information:
				if piece.endswith('%'):
					percentage = int(piece.split('%')[0])
	return percentage


if __name__	== "__main__":
	main()
