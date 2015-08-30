import os
import datetime

def main():
	imageDir = '/Users/sandlappernyc/Desktop/testpics'
	
	# Because these will be inputs, start with string
	startDate = '205-08-13'
	endDate = '2015-0-30'

	print 'Validating dateString:'
	startDateCheckOk = validateDateString(startDate)
	endDateCheckOk = validateDateString(endDate)

	# Parse date strings; stop if either failed
	if startDateCheckOk == False or endDateCheckOk == False:
		print 'Stopping script; fix dates and try again'
		return

	# Include function to correct order of dates

	# Loop through the directory
	loopcount = 0
	for root, dir, files in os.walk(imageDir):
		print 'Loop # ', loopcount
		for f in files:
			print 'printing file: ', os.path.join(root, f)
		for d in dir:
			print 'printing dir: ', os.path.join(root, d)
		loopcount += 1

def validateDateString(dateString):
	try:
		datetime.datetime.strptime(dateString, '%Y-%m-%d')
		print 'DateOk'
		return True

	except ValueError:
		print 'Incorrect date format:\n\tYou entered',  dateString , '\n\tShould be YYYY-MM-DD'
		return False

if __name__	== "__main__":
	main()