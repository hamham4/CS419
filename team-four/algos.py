from collections import namedtuple

MINS_PER_DAY = 1440
FreeBlock = namedtuple("FreeBlock", "year, month, day, startTime, endTime")
s1 = FreeBlock(year='2014', month='06', day='17', startTime=u'0900', endTime=u'1550')
s2 = FreeBlock(year='2014', month='09', day='27', startTime=u'1900', endTime=u'2050')
s3 = FreeBlock(year='2014', month='09', day='12', startTime=u'0900', endTime=u'1100')
s4 = FreeBlock(year='2014', month='09', day='12', startTime=u'1300', endTime=u'1500')
s5 = FreeBlock(year='2014', month='10', day='19', startTime=u'0000', endTime=u'2359')
s6 = FreeBlock(year='2014', month='09', day='12', startTime=u'1000', endTime=u'1200')
s7 = FreeBlock(year='2014', month='06', day='17', startTime=u'1100', endTime=u'1550')
s8 = FreeBlock(year='2014', month='06', day='17', startTime=u'0900', endTime=u'1200')

lst = list()
ft1 = dict()
ft1["smith"] = [[s3, s4]]  
ft1["jones"] = [[s3, s4]]
ft1["siple"] = [[s6]]
ft2 = dict()
ft2["smith"] = [[s1]]  
ft2["jones"] = [[s8]]
ft2["siple"] = [[s7]]

lst = [ft1, ft2]

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

def timeToMins(time):
			hour = int(time) / 100
			length = len(time)
			mins = int(time[(length - 2) : length])

			return (60 * hour + mins)

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
	
def commonFreeTime( lst ):
	
	commonFreeTimes = list()
	for item in lst:
		timeArr = [0] * MINS_PER_DAY
		recordingFreeTime = False
		startTime = None
		endTime = None
		month = None
		day = None
		year = None
		flag = 0
		for key in sorted(item):
			for n in item[key]:
				if flag == 0:
					for block in n:
						month = block.month
						day = block.day
						year = block.year
						break
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
	
r = commonFreeTime( lst )
print(r)