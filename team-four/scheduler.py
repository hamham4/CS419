from collections import namedtuple
import logging

MINS_PER_DAY = 1440
FreeBlock = namedtuple("FreeBlock", "year, month, day, startTime, endTime")


def getAttendees( allFreeTimes, day, month, year, sTime, eTime ):
	avail = list()

	for key in sorted(allFreeTimes):
		for n in allFreeTimes[key]:
			for block in n:
				if int(block.year) == int(year) and int(block.month) == int(month) and int(block.day) == int(day) and int( block.startTime ) <= int(sTime) and int( block.endTime ) >= int(eTime):
					avail.append(key)

	return avail

def firstMark(n, timeArr, strt, endt):
	
	for block in n:
		startMins = int( timeToMins(strt) )
		logging.info("================START block min==================")
		logging.info(strt)
		logging.info("================START MIN==================")
		logging.info(startMins)

		endMins = int( timeToMins(endt) )
		logging.info("================END block MIN==================")
		logging.info(endt)
		logging.info("================END MIN==================")
		logging.info(endMins)

		for i in range(startMins, endMins + 1):
			timeArr[i] = 1

	return timeArr
	
def markTimes(n, timeArr):
	newArr = [0] * MINS_PER_DAY
	
	for block in n:
		startMins = int( timeToMins(block.startTime) )
		
		endMins = int( timeToMins(block.endTime) )
		print (minsToTime(endMins))

		for i in range(startMins, endMins + 1):
			newArr[i] = 1
	
	for pos in range( len( timeArr ) ):
		if timeArr[pos] == 1 and newArr[pos] == 0:
			timeArr[pos] = 0
			

	return timeArr

def timeToMins(time):
			hour = int( int(time) / 100)
			length = len(time)
			mins = int(time[(length - 2) : length])

			return ((60 * hour) + mins)

def minsToTime(numMins):
	hour = int(numMins / 60)
	str_hour = str(hour)
	if len(str_hour) < 2:
		str_hour = "0" + str_hour
	
	mins = int( numMins % 60 )
	str_mins = str(mins)
	if len(str_mins) < 2:
		str_mins = "0" + str_mins

	return (str_hour + str_mins)
	
def getCommonFreeTimes( lst, strt, endt ):
	
	commonFreeTimes = list()
	logging.info("================LIST==================")
	logging.info(lst)
	for dictionary in lst:
		logging.info("================DICTIONARY==================")
		logging.info(dictionary)
		timeArr = [0] * MINS_PER_DAY
		recordingFreeTime = False
		startTime = None
		endTime = None
		month = None
		day = None
		year = None
		flag = 0
		for key in sorted(dictionary):
			logging.info("================KEY==================")
			logging.info(key)
			for freeList in dictionary[key]:
				logging.info("================freeList==================")
				logging.info(freeList)
				if flag == 0:
					for block in freeList:
						logging.info("================BLOCK==================")
						logging.info(block)
						month = block.month
						day = block.day
						year = block.year
						break
					timeArr = firstMark( freeList, timeArr, strt, endt )
					flag = 1
				timeArr = markTimes( freeList, timeArr )

		for minute in range(0, MINS_PER_DAY):
			if timeArr[minute] == 1:
				if recordingFreeTime == False:
					recordingFreeTime = True
					startTime = minsToTime(minute)
			else:
				if recordingFreeTime == True:
					recordingFreeTime = False
					endTime = minsToTime(minute - 1)

			if startTime != None and endTime != None and (int(endTime) - int(startTime)) >= 30:
				sharedTime = FreeBlock(year, month, day, startTime, endTime)
				commonFreeTimes.append(sharedTime)
				startTime = None
				endTime = None

		#If the end time was the end of the day
		if startTime != None and endTime == None:
			endTime = "2359"
			sharedTime = FreeBlock(year, month, day, startTime, endTime)
			commonFreeTimes.append(sharedTime)

	return commonFreeTimes
	
#r = getCommonFreeTimes( lst, strt, endt )
#print(r)