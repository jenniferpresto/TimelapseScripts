import os
import datetime
import collections
import sys
import getopt

def main():
	imageDir = '/Users/sandlappernyc/Desktop/testpics'
	
	# Because these will be inputs, start with string
	startDateInput = ''
	endDateInput = ''

	# Get user input for dates
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hs:e:')
	except getopt.GetoptError as err:
		print err
		print 'Use format: countFiles.py -s <startdate YYYY-MM-DD> -e <enddate YYYY-MM-DD>'
		sys.exit(2)

	for o, a in opts:
		if o == '-s':
			startDateInput = a
		elif o == '-e':
			endDateInput = a
		elif o == '-h':
			print 'Use format: countFiles.py -s <startdate YYYY-MM-DD> -e <enddate YYYY-MM-DD>'

	# Make sure dates in correct format
	print 'Validating dateString:'
	startDateCheckOk = validateDateString(startDateInput)
	endDateCheckOk = validateDateString(endDateInput)

	# Parse date strings; stop if either failed
	if startDateCheckOk == False or endDateCheckOk == False:
		print 'Stopping script. Please fix dates.'
		return

	start = datetime.datetime.strptime(startDateInput, '%Y-%m-%d')
	end = datetime.datetime.strptime(endDateInput, '%Y-%m-%d')

	# create dictionary
	dateCountPairs = collections.OrderedDict()

	# Add each date string to dictionary with count 0
	for eachdate in dateRangeGenerator(start, end):
		datestr = eachdate.strftime('%Y-%m-%d')
		dateCountPairs[datestr] = 0

	# Loop through the directory
	print 'Looping through directory'
	for fn in os.listdir(imageDir):
		# Skip files that aren't jpgs
		if not fn.endswith('.jpg'):
			print fn, 'is not a jpg'
			continue

		# Extract file name before underscore
		fnbegin = fn.split('_')[0]
		
		# Check to see if in the dictonary
		# If so, add to count
		if fnbegin in dateCountPairs.keys():
			dateCountPairs[fnbegin] += 1
		# Otherwise, skip it and print warning
		else:
			print 'Found file in different format or outside range:', fn

	for eachDate in dateCountPairs:
		print eachDate, ': ', dateCountPairs[eachDate]

##################################
# Validate dates
##################################

def validateDateString(dateStringToCheck):
	try:
		datetime.datetime.strptime(dateStringToCheck, '%Y-%m-%d')
		print 'DateOk:', dateStringToCheck
		return True

	except ValueError:
		print 'Incorrect date format:\n\tYou entered',  dateStringToCheck, '\n\tShould be YYYY-MM-DD'
		return False

##################################
# Create generator for date range
# http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
# http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
##################################
def dateRangeGenerator(startdate, enddate):
	for n in range(int ((enddate - startdate).days) + 1):
		yield startdate + datetime.timedelta(n)


# def correctDateOrder(start, end):

if __name__	== "__main__":
	main()