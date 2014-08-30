from collections import namedtuple

MINS_PER_DAY = 1440
FreeBlock = namedtuple("FreeBlock", "year, month, day, startTime, endTime")

def whoIsFree( allFreeTimes, day, month, year, sTime, eTime ):
	avail = list()

	for key in sorted(allFreeTimes):
		for n in allFreeTimes[key]:
			for block in n:
				if int(block.year) == int(year) and int(block.month) == int(month) and int(block.day) == int(day) and int( block.startTime ) <= int(sTime) and int( block.endTime ) >= int(eTime):
					avail.append(key)

	return avail

def firstMark(n, timeArr):
	
	for block in n:
		startMins = int( timeToMins(block.startTime) )
		endMins = int( timeToMins(block.endTime) )
		for i in range(startMins, endMins + 1):
			timeArr[i] = 1

	return timeArr
	
def markTimes(n, timeArr):
	newArr = [0] * MINS_PER_DAY
	
	for block in n:
		startMins = int( timeToMins(block.startTime) )
		endMins = int( timeToMins(block.endTime) )
		for i in range(startMins, endMins + 1):
			newArr[i] = 1
	
	for pos in range( len( timeArr ) ):
		if timeArr[pos] == 1 and newArr[pos] == 0:
			timeArr[pos] = 0

	return timeArr
	
def commonFreeTime( allFreeTimes, year, month, day ):
	timeArr = [0] * MINS_PER_DAY
	recordingFreeTime = False
	startTime = None
	endTime = None
	commonFreeTimes = list()
	
	flag = 0
	for key in sorted(allFreeTimes):
		for n in allFreeTimes[key]:
			if flag == 0:
				timeArr = firstMark( n, timeArr )
				flag = 1
			else:
				timeArr = markTimes( n, timeArr )

	for minute in range(0, MINS_PER_DAY):
		if timeArr[minute] == 1:
			if recordingFreeTime == False:
				recordingFreeTime = True
				startTime = minsToTime(minute)
		else:
			if recordingFreeTime == True:
				recordingFreeTime = False
				endTime = minsToTime(minute - 1)

		if startTime != None and endTime != None:
			sharedTime = FreeBlock(year, month, day, startTime, endTime)
			commonFreeTimes.append(sharedTime)
			startTime = None
			endTime = None
	return commonFreeTimes